import sqlite3


def fetch_query_results_as_model(cursor: sqlite3.Cursor, model_class: type[object]) -> list[object]:

    results = cursor.fetchall()
    if len(results) == 0:
        return []
    
    column_names = tuple(map(
        lambda t: t[0],
        cursor.description
    ))  # cursor.description provides an odd format of column names

    print(f"{results = }, {column_names = }")
    return [
        model_class(**{key: row[key] for key in column_names})
        for row in results
    ]
