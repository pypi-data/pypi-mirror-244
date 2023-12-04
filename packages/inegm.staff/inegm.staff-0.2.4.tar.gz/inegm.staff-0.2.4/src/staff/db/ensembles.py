import sqlite3

from staff.db import DB_PATH


def create_tables(db_path: str = DB_PATH) -> None:
    """Create the tables in the database.

    Args:
        db_path: The path to the database.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ensembles (
                id TEXT PRIMARY KEY,
                name TEXT,
                category TEXT,
                description TEXT
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ensemble_instruments (
                ensemble_id TEXT,
                instrument_id TEXT,
                role TEXT,
                FOREIGN KEY (ensemble_id) REFERENCES ensembles (id),
                FOREIGN KEY (instrument_id) REFERENCES instruments (id),
                PRIMARY KEY (ensemble_id, instrument_id)
            )
            """
        )
