import sqlite3
from sqlite3 import Error



def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error:
        print(Error)
    conn.row_factory = sqlite3.Row 
    return conn
