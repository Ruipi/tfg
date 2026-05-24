import sqlite3
import gzip
import json

from tqdm import tqdm

INPUT_DB = (
    "data/raw/datasets_positive.db"
)

OUTPUT_DB = (
    "data/discard/strategic.db"
)

input_conn = sqlite3.connect(
    INPUT_DB
)

output_conn = sqlite3.connect(
    OUTPUT_DB
)

output_conn.execute("""
CREATE TABLE IF NOT EXISTS Discard (

    Id INTEGER PRIMARY KEY,

    Data BLOB
)
""")

output_conn.execute(
    "DELETE FROM Discard"
)

count_query = """
SELECT COUNT(*)
FROM Discard
"""

num_rows = input_conn.execute(
    count_query
).fetchone()[0]

print(num_rows)

kept = 0
discarded = 0

for offset in tqdm(range(num_rows)):

    query = f"""
    SELECT Data
    FROM Discard
    LIMIT 1 OFFSET {offset}
    """

    row = input_conn.execute(
        query
    ).fetchone()

    blob = row[0]

    decoded = json.loads(
        gzip.decompress(blob)
    )

    discard_actions = [
        action
        for action in decoded[
            "valid_actions"
        ]
        if action["type"] == 1
    ]

    if len(discard_actions) <= 1:

        discarded += 1

        continue

    output_conn.execute(
        """
        INSERT INTO Discard (Data)
        VALUES (?)
        """,
        (blob,)
    )

    kept += 1

    if offset % 10000 == 0:

        output_conn.commit()

output_conn.commit()

input_conn.close()

output_conn.close()

print()

print("Finished")

print()

print(
    f"Kept: {kept}"
)

print(
    f"Discarded: {discarded}"
)

print(
    f"Retention: "
    f"{kept / num_rows:.3f}"
)