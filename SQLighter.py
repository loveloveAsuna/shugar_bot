# Database work with class
# each single request open single connection
import sqlite3


class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()  # объект для выполнения запросов

    def select_all(self):
        # Get all rows
        with self.connection:
            return self.cursor.execute('SELECT * FROM music').fetchall()

    def select_single(self, rownum):
        # Get 1 row with rownum
        with self.connection:
            return self.cursor.execute('SELECT * FROM music WHERE id = ?', (rownum,)).fetchall()[0]

    def counts_rows(self):
        # Calculate quantity of rows
        with self.connection:
            result = self.cursor.execute('SELECT * FROM music').fetchall()
            return len(result)

    def close(self):
        # Close connection with database
        self.connection.close()

