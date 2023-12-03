# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
The SQL Connector downloads data from remote servers and converts them
to pyarrow tables so they can be processed as per any other data source.
"""
from decimal import Decimal
from typing import Generator

import pyarrow
from orso import DataFrame
from orso import Row
from orso.schema import FlatColumn
from orso.schema import RelationSchema
from orso.types import PYTHON_TO_ORSO_MAP

from opteryx.connectors.base.base_connector import DEFAULT_MORSEL_SIZE
from opteryx.connectors.base.base_connector import INITIAL_CHUNK_SIZE
from opteryx.connectors.base.base_connector import BaseConnector
from opteryx.exceptions import MissingDependencyError
from opteryx.exceptions import UnmetRequirementError
from opteryx.third_party.query_builder import Query


class SqlConnector(BaseConnector):
    __mode__ = "Sql"

    def __init__(self, *args, connection: str = None, engine=None, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            from sqlalchemy import MetaData
            from sqlalchemy import create_engine
        except ImportError as err:  # pragma: nocover
            raise MissingDependencyError(err.name) from err

        if engine is None and connection is None:
            raise UnmetRequirementError(
                "SQL Connections require either a SQL Alchemy connection string in the 'connection' parameter, or a SQL Alchemy Engine in the 'engine' parameter."
            )

        # create the SqlAlchemy engine
        if engine is None:
            self._engine = create_engine(connection)
        else:
            self._engine = engine

        self.schema = None
        self.metadata = MetaData()

    def read_dataset(
        self, columns: list = None, chunk_size: int = INITIAL_CHUNK_SIZE
    ) -> Generator[pyarrow.Table, None, None]:
        from sqlalchemy.sql import text

        self.chunk_size = chunk_size
        result_schema = self.schema

        query_builder = Query().FROM(self.dataset)

        # Update the SQL and the target morsel schema if projecting
        if columns:
            column_names = [col.name for col in columns]
            query_builder.add("SELECT", *column_names)
            result_schema.columns = [col for col in self.schema.columns if col.name in column_names]
        else:
            query_builder.add("SELECT", "*")

        # Use orso as an intermediatary, it's row-based so is well suited to processing
        # records coming back from a SQL query, and it has a well-optimized to arrow
        # converter to create pyarrow Tables
        morsel = DataFrame(schema=result_schema)
        row_factory = Row.create_class(result_schema, tuples_only=True)

        with self._engine.connect() as conn:
            # DEBUG: log ("READ DATASET\n", str(query_builder))
            result = conn.execute(text(str(query_builder)))

            while True:
                batch_rows = result.fetchmany(self.chunk_size)
                if not batch_rows:
                    break

                # convert each SqlAlchemy Row to an orso Row
                for row in batch_rows:
                    morsel._rows.append(row_factory(row))
                yield morsel.arrow()

                # Dynamically adjust chunk size based on the data size, we start by downloading
                # 500 records to get an idea of the row size, assuming these 500 are
                # representative, we work out how many rows fit into 8Mb.
                # Don't keep recalculating, this is not a cheap operation and it's predicting
                # the future so isn't going to ever be 100% correct
                if self.chunk_size == INITIAL_CHUNK_SIZE and morsel.nbytes() > 0:
                    self.chunk_size = int(len(morsel) // (morsel.nbytes() / DEFAULT_MORSEL_SIZE))
                    # DEBUG: log (f"CHANGING CHUNK SIZE TO {self.chunk_size} was {INITIAL_CHUNK_SIZE}.")

                morsel = DataFrame(schema=result_schema)

    def get_dataset_schema(self) -> RelationSchema:
        from sqlalchemy import Table

        if self.schema:
            return self.schema

        # Try to read the schema from the metastore
        self.schema = self.read_schema_from_metastore()
        if self.schema:
            return self.schema

        # get the schema from the dataset
        # DEBUG: log ("GET SQL SCHEMA:", self.dataset)
        try:
            table = Table(self.dataset, self.metadata, autoload_with=self._engine)

            self.schema = RelationSchema(
                name=table.name,
                columns=[
                    FlatColumn(
                        name=column.name,
                        type=PYTHON_TO_ORSO_MAP[column.type.python_type],
                        precision=None
                        if column.type.python_type != Decimal
                        else column.type.precision,
                        scale=None if column.type.python_type != Decimal else column.type.scale,
                        nullable=column.nullable,
                    )
                    for column in table.columns
                ],
            )
        except Exception as err:
            # Fall back to getting the schema from the first row, this is the column names, and where
            # possible, column types.
            # DEBUG: log (f"APPROXIMATING SCHEMA OF {self.dataset} BECAUSE OF {type(err).__name__}({err})")
            from sqlalchemy.sql import text

            with self._engine.connect() as conn:
                query = Query().SELECT("*").FROM(self.dataset).LIMIT("1")
                # DEBUG: log ("READ ROW\n", str(query))
                row = conn.execute(text(str(query))).fetchone()._asdict()
                # DEBUG: log ("ROW:", row)
                self.schema = RelationSchema(
                    name=self.dataset,
                    columns=[
                        FlatColumn(
                            name=column,
                            type=0 if value is None else PYTHON_TO_ORSO_MAP[type(value)],
                        )
                        for column, value in row.items()
                    ],
                )

        return self.schema
