import sqlite3
from typing import TypeVar

T = TypeVar('T')

def fetch_query_results_as_model(
        cursor: sqlite3.Cursor,
        model_class: type[T],
) -> list[T]:

    results = cursor.fetchall()
    if len(results) == 0:
        return []
    
    column_names = tuple(map(
        lambda t: t[0],
        cursor.description
    ))  # cursor.description provides an odd format of column names

    return [
        model_class(**{key: row[key] for key in column_names})
        for row in results
    ]
