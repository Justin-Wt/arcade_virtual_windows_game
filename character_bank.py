import sqlite3 as sq

VALID_COLUMNS = {"name", "hp", "attack", "rarity", "type", "faction", "id"}
VALID_SORT = {"ASC", "DESC"}
conn = sq.connect("character.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS
players (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    level INTEGER,
    hp INTEGER,
    attack INTEGER,
    type TEXT,
    rarity INTEGER,
    faction TEXT,
    awaken BOOL
)
""")
cursor.executemany(
    """
INSERT OR IGNORE INTO players
(name, level, hp, attack, type, rarity, faction, awaken)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""",
    [
        ("Yvonne", 1, 800, 200, "mage", 6, "player", 0),
        ("Ember", 1, 2300, 120, "defender", 6, "player", 0),
        ("Fluorite", 1, 800, 120, "ranged", 5, "player", 0),
        ("Last_Rite", 1, 1800, 180, "striker", 6, "player", 0),
        ("Mona", 1, 800, 120, "ranged", 6, "player", 0),
    ],
)
conn.commit()


def sort_data(order="id", sort_dir="ASC", rarity_var=None, type_var=None):
    if order not in VALID_COLUMNS:
        order = "id"
    if sort_dir not in VALID_SORT:
        sort_dir = "DESC"
    conditions = []
    params = []
    if rarity_var is not None:
        placeholders = ",".join("?" for _ in rarity_var)
        conditions.append(f"rarity IN ({placeholders})")
        params.extend(rarity_var)
    if type_var:
        placeholders = ",".join("?" for _ in type_var)
        conditions.append(f"type IN ({placeholders})")
        params.extend(type_var)
    query = (
        "SELECT id, name, level, hp, attack, type, rarity, faction, awaken FROM players"
    )
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += f" ORDER BY {order} {sort_dir}"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    return [
        {
            "id": r[0],
            "name": r[1],
            "level": r[2],
            "hp": r[3],
            "attack": r[4],
            "type": r[5],
            "rarity": r[6],
            "faction": r[7],
            "awaken": r[8],
        }
        for r in rows
    ]


def add_character(name, hp, attack, types, rarity, faction, awaken=0):
    cursor.execute(
        """
    INSERT OR IGNORE INTO players
    (name, hp, attack, type, rarity, faction, awaken)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        [name, hp, attack, types, rarity, faction, awaken],
    )
    conn.commit()


def upgrade_character(name, hp, attack):
    cursor.execute(
        """
    UPDATE players
    SET level = level + 1,
        hp = hp + ?,
        attack = attack + ?
    WHERE name= ?
    """,
        [hp, attack, name],
    )
    conn.commit()


def character_awaken(name, hp, attack):
    cursor.execute(
        """
    UPDATE players
    SET hp = hp + ?,
        attack = attack + ?,
        awaken = 1
    WHERE name= ?
    """,
        [hp, attack, name],
    )
    conn.commit()
