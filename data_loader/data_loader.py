"""Utility class for loading SQL tables into pandas DataFrames.

Module: data_loader.py
Author: Josue Cavazos Jr.
Last edited: May 27, 2026
E-mail: jcavazos@burnsmcd.com

Dependencies:
    - pandas
    - sqlalchemy
    - pyodbc
    - python-dotenv

Usage Example:
    loader = SQLLoader()
    projects_df = loader.load_table("projects")
"""

import logging
import os
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class SQLLoader:
    """Utility class for loading SQL tables into pandas DataFrames using SQLAlchemy."""

    def __init__(
        self,
        connection_string: str = None,
    ) -> None:
        """Initialize the SQLLoader with a connection string.

        Args:
            connection_string (str, optional): The Azure SQL connection string.
            If not provided, loads from environment variable
            'AZURE_SQL_CONNECTION_STRING'.

        Raises:
            ValueError: If no connection string is provided.

        """
        # Set up logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        load_dotenv()

        self.connection_string = connection_string or os.getenv(
            "AZURE_SQL_CONNECTION_STRING",
        )

        if not self.connection_string:
            raise ValueError("Azure SQL connection string not provided")

        self.engine = self._create_engine()
        self.logger.info("Successfully connected to the database.")

    def _create_engine(self) -> Engine:
        """Create a SQLAlchemy engine using the connection string.

        Returns:
            Engine: SQLAlchemy engine instance.

        """
        encoded = quote_plus(self.connection_string)

        return create_engine(
            f"mssql+pyodbc:///?odbc_connect={encoded}",
            fast_executemany=True,
        )

    def load_table(
        self,
        table_name: str,
        schema: str = "dbo",
        columns: list[str] | None = None,
    ) -> pd.DataFrame:
        """Load a table from the SQL database into a pandas DataFrame.

        Args:
            table_name (str): Name of the table to load.
            schema (str, optional): Schema name. Defaults to 'dbo'.
            columns (list[str], optional): List of columns to select.
            Defaults to all columns.

        Returns:
            pd.DataFrame: DataFrame containing the table data.

        """
        if columns:
            column_sql = ", ".join(f"[{column}]" for column in columns)
        else:
            column_sql = "*"

        query = f"""
            SELECT {column_sql}
            FROM [{schema}].[{table_name}]
        """

        df = pd.read_sql(query, self.engine)
        self.logger.info(
            f"Loaded table '{table_name}' from schema '{schema}'"
            f" with columns: {columns if columns else 'ALL'}.",
        )
        return df

    def load_where(
        self,
        table_name: str,
        where_clause: str,
        params: tuple | None = None,
        schema: str = "dbo",
    ) -> pd.DataFrame:
        """Load rows from a table with a WHERE clause into a pandas DataFrame.

        Args:
            table_name (str): Name of the table to load.
            where_clause (str): SQL WHERE clause (without 'WHERE').
            params (tuple, optional): Parameters for the WHERE clause. Defaults to None.
            schema (str, optional): Schema name. Defaults to 'dbo'.

        Returns:
            pd.DataFrame: DataFrame containing the filtered data.

        """
        query = f"""
            SELECT *
            FROM [{schema}].[{table_name}]
            WHERE {where_clause}
        """

        df = pd.read_sql(
            query,
            self.engine,
            params=params,
        )
        self.logger.info(
            f"Loaded table '{table_name}' from schema '{schema}'"
            f" with WHERE clause: {where_clause}.",
        )
        return df

    def load_multiple_tables(
        self,
        table_names: list[str],
        schema: str = "dbo",
    ) -> dict[str, pd.DataFrame]:
        """Load multiple tables into a dictionary of DataFrames.

        Args:
            table_names (list[str]): List of table names to load.
            schema (str, optional): Schema name. Defaults to 'dbo'.

        Returns:
            dict[str, pd.DataFrame]: Dictionary mapping table names to DataFrames.

        """
        results = {
            table_name: self.load_table(table_name=table_name, schema=schema)
            for table_name in table_names
        }
        self.logger.info(
            f"Loaded multiple tables: {table_names} from schema '{schema}'.",
        )
        return results
