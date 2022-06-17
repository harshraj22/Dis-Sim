import sqlite3
from typing import List

DB_NAME = './db/monitor.db'
TABLE_NAME = 'monitor'


# Create table
def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (id INTEGER PRIMARY KEY AUTOINCREMENT, avg_pixel INTEGER)")
    conn.commit()
    conn.close()


def list_tables(db_name: str) -> List[str]:
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    conn.close()
    return tables


def insert_data(avg_pixel: float):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f"INSERT INTO {TABLE_NAME} (avg_pixel) VALUES ({avg_pixel})") 
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_table()
    print(f'Successfully created table {TABLE_NAME} in database {DB_NAME}')
    print(f'List of tables in database {DB_NAME}: {list_tables(DB_NAME)}')