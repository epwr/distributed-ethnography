import sqlite3


class Sqlite3Driver:

    def __init__(self, db_file):

        self._connection = sqlite3.connect(db_file)
        cursor = self._connection.cursor()

        # Ensure foreign key constraints are enforced on every connection
        cursor.execute("PRAGMA foreign_keys = ON;")

    

