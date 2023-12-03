from prettytable import PrettyTable
import sqlite3 as sq
from logging import info, error
from .User import User
import os


class DbTools:
    def __init__(self, db_location, table_name):
        self.db_name = os.path.abspath(db_location)
        self.table_name = table_name
        self.conn = self.connect_db()
        self.Ctext = User.Ctext
        self.Choice = User.Choice

    def connect_db(self):
        try:
            conn = sq.connect(self.db_name)
            info("Database opened successfully")
            return conn
        except sq.Error as e:
            error(f"Error connecting to the database: {e}")
            return None

    def close_db(self):
        if self.conn is not None:
            self.conn.close()
            info("Database closed")

    def execute_query(self, query, params=None):
        with self.conn:
            cursor = self.conn.cursor()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                self.conn.commit()
                return cursor
            except sq.Error as e:
                error(f"Error executing query: {e}")
                return None

    def create_table(self, columns):
        column_definitions = ", ".join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({column_definitions})"
        self.execute_query(query)
        info(f"Table "
        {self.table_name}
        " created")

    def insert_data(self, data):
        placeholders = ", ".join(["?"] * len(data))
        columns = ", ".join(data.keys())
        values = list(data.values())

        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, values)
        info("Data inserted into the table")

    def view_data(self, page_size=50):
        try:
            if self.conn is None:
                print("Database connection is not available.")
                return

            cursor = self.conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
            total_rows = cursor.fetchone()[0]
            total_pages = (total_rows + page_size - 1) // page_size

            for page in range(1, total_pages + 1):
                offset = (page - 1) * page_size
                cursor.execute(f"SELECT * FROM {self.table_name} LIMIT ? OFFSET ?", (page_size, offset))
                data = cursor.fetchall()

                if len(data) == 0:
                    print(f"No data found in the {self.table_name}.")
                else:
                    table = PrettyTable()
                    table.field_names = list(data[0].keys())

                    for row in data:
                        table.add_row(row.values())

                    print(table)

                    if total_pages > 1:
                        print(f"Page {page} of {total_pages}")
                        print("Press Escape to exit, or any other key to continue...")

        except sq.Error as e:
            error(f"Error viewing data: {e}")

    def remove_data(self, condition):
        if self.conn is None:
            print("Database connection is not available.")
            return

        query = f"DELETE FROM {self.table_name} WHERE {condition}"
        cursor = self.execute_query(query)
        if cursor.rowcount == 0:
            print("No data found for the given condition.")
        else:
            info(f"{cursor.rowcount} row(s) deleted from the {self.table_name}.")

    def search_data(self, condition):
        if self.conn is None:
            print("Database connection is not available.")
            return

        query = f"SELECT * FROM {self.table_name} WHERE {condition}"
        cursor = self.execute_query(query)

        if cursor is None:
            print("Error executing the search query.")
            return

        column_names = [description[0] for description in cursor.description]

        table = PrettyTable()
        table.field_names = column_names

        for row in cursor:
            table.add_row(row)

        return table
