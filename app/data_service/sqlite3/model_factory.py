import sqlite3


def fetch_query_results_as_model(cursor: sqlite3.Cursor, model_class: type[object]) -> list[object]:

    column_names = map(
        lambda t: t[0],
        cursor.description
    )  # cursor.description provides an odd format of column names

    return [
        model_class(**{key: value for key, value in zip(column_names, row)})
        for row in cursor.fetchall()
    ]
