"""SQLLoader.

A utility class for loading SQL tables into pandas DataFrames using SQLAlchemy.
"""

__version__ = "0.1.0"

from .data_loader import SQLLoader

__all__ = ["SQLLoader"]
