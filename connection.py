from sqlite3 import Error, connect, Row


# CREA CONNESSIONE
def create_connection(db_file):
    conn = None
    try:
        conn = connect(db_file)
    except Error:
        print(Error)
    conn.row_factory = Row 
    return conn
