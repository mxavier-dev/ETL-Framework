import sqlite3
from pathlib import Path

from src.loaders.Loader import Loader

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

    def load(self, data, destination, schema, write_mode):
        path = destination['path']
        table_name = destination['table']

        if not Path(path).is_dir():
            raise ValueError(
                f'The path "{path}" is not a directory'
            )

        with sqlite3.connect(f'{path}/data_transformed.db') as conn:
            cursor = conn.cursor()

            column_and_type = self.dynamic_table(schema)
            query = f'CREATE TABLE IF NOT EXISTS {table_name} ({column_and_type})'
            cursor.execute(query)
            columns = ', '.join([*schema])
            placeholders = ", ".join(['?']*len(schema))

            match write_mode:
                case 'append':
                    query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
                case 'overwrite':
                    cursor.execute(f'DELETE FROM {table_name}')
                    query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
                case 'upsert':
                    query = f'''
                        INSERT INTO {table_name} ({columns}) VALUES ({placeholders})
                        ON CONFLICT(id) DO UPDATE SET

                        '''


            for line in data:
                values = [line[field] for field in schema]
                cursor.execute(query, values)
