from src.loaders.Loader import Loader
import sqlite3

SQL_TYPES = {
    "str": "TEXT",
    "string": "TEXT",
    "int": "INTEGER",
    "float": "REAL",
    None: "TEXT"
}

class SQLiteLoader(Loader):
    def dynamic_table(self, schema):
        columns = []
        for field, config in schema.items():
            columns.append(f'{field} {SQL_TYPES.get(config["type"])}')

        return ', '.join(columns)

    def load(self, data, database, schema):
        destination = database[0]
        table = database[1]
        conn = sqlite3.connect(destination)
        cursor = conn.cursor()

        column_and_type = self.dynamic_table(schema)
        query = f'CREATE TABLE IF NOT EXISTS {table} ({column_and_type})'
        cursor.execute(query)
        conn.commit()

        columns = ', '.join(schema.keys())
        placeholders = ", ".join(['?']*len(schema))
        query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'

        for line in data:
            values = [line[field] for field in schema]
            cursor.execute(query, values)

        conn.commit()
        conn.close()

