import sqlite3

from staff import MIDIPitch
from staff.db import DB_PATH
from staff.orchestration.instrument import Articulation, Instrument, InstrumentRange


def create_tables(db_path: str = DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS instruments (
                id TEXT PRIMARY KEY,
                name TEXT,
                section TEXT,
                bottom INTEGER,
                top INTEGER,
                is_continuous INTEGER,
                abbreviation TEXT,
                category TEXT,
                description TEXT,
                UNIQUE (name, category),
                CHECK (is_continuous IN (0, 1)),
                CHECK (bottom <= top),
                CHECK (category != ''),
                CHECK (name != '')
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS articulations (
                name TEXT,
                instrument_id TEXT,
                key_switch INTEGER,
                abbreviation TEXT,
                description TEXT,
                FOREIGN KEY (instrument_id) REFERENCES instruments (id),
                UNIQUE (name, instrument_id),
                CHECK (key_switch >= 0),
                CHECK (key_switch <= 127),
                CHECK (name != '')
            ) 
            """
        )


def load_instrument(
    name: str,
    db_path: str = DB_PATH,
    category: str = "Default",
) -> Instrument:
    """Load an instrument from a database.

    Args:
        name: The name of the instrument to load.
        db_path: The path to the database.
        category: The name of the category the instrument belongs to.

    Returns:
        The instrument.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                name,
                bottom,
                top,
                section,
                is_continuous,
                abbreviation,
                category,
                description
            FROM instruments
            WHERE category = ? AND name = ?
            """,
            (category, name),
        )
        (
            name,
            bottom,
            top,
            section,
            is_continuous,
            abbreviation,
            category,
            description,
        ) = cursor.fetchone()
        cursor.execute(
            """
            SELECT
                name,
                key_switch,
                abbreviation,
                description
            FROM articulations
            WHERE instrument_id = ?
            """,
            (f"{category} - {name}",),
        )
        articulations = [
            Articulation(
                name=name,
                key_switch=MIDIPitch(key_switch),
                abbreviation=abbreviation,
                description=description,
            )
            for name, key_switch, abbreviation, description in cursor.fetchall()
        ]
    return Instrument(
        category=category,
        name=name,
        section=section,
        range=InstrumentRange(
            bottom=MIDIPitch(bottom),
            top=MIDIPitch(top),
        ),
        articulations=articulations,
        is_continuous=bool(is_continuous),
        abbreviation=abbreviation,
        description=description,
    )


def store_instrument(
    instrument: Instrument,
    db_path: str = DB_PATH,
) -> None:
    """Add the instrument to the database.

    Args:
        db_path: The path to the database.
    """
    create_tables(db_path)
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO instruments (
                    id,
                    name,
                    section,
                    bottom,
                    top,
                    is_continuous,
                    abbreviation,
                    category,
                    description
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"{instrument.category} - {instrument.name}",
                    instrument.name,
                    instrument.section,
                    instrument.range.bottom.number,
                    instrument.range.top.number,
                    instrument.is_continuous,
                    instrument.abbreviation,
                    instrument.category,
                    instrument.description,
                ),
            )
            for articulation in instrument.articulations:
                cursor.execute(
                    """
                    INSERT INTO articulations (
                        name,
                        instrument_id,
                        key_switch,
                        abbreviation,
                        description
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        articulation.name,
                        f"{instrument.category} - {instrument.name}",
                        articulation.key_switch.number,
                        articulation.abbreviation,
                        articulation.description,
                    ),
                )
            conn.commit()
    except sqlite3.IntegrityError as error:
        instrument_id = f"{instrument.category} - {instrument.name}"
        raise ValueError(
            f"Instrument `{instrument_id}` already exists in the database."
        ) from error


def delete_instrument(
    name: str,
    db_path: str = DB_PATH,
    category: str = "Default",
) -> None:
    """Delete an instrument from the database.

    Args:
        name: The name of the instrument to delete.
        db_path: The path to the database.
        category: The name of the category to delete the instrument from.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM instruments
            WHERE category = ? AND name = ?
            """,
            (category, name),
        )
        cursor.execute(
            """
            DELETE FROM articulations
            WHERE instrument = ?
            """,
            (f"{category} - {name}",),
        )
        conn.commit()
