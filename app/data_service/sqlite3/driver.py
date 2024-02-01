import sqlite3


class Sqlite3Driver:

    def __init__(self, db_file):

        self._connection = sqlite3.connect(db_file)
        self._connection.row_factory = sqlite3.Row

        # Ensure foreign key constraints are enforced on every connection
        cursor = self._connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

    
    def get_open_surveys(self):

        query = (
            f"SELECT * FROM survey WHERE is_open IS TRUE;"
        )
        cursor = self._connection.cursor()
        result = cursor.execute(query).fetchall()

        return result
        
        
