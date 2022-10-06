from connection import create_connection
from variabili import database

# RESET VITE
def resetVite():
    conn = create_connection(database)
    cur = conn.cursor()

    sql = f"UPDATE login SET vite = 5"
    cur.execute(sql)
    conn.commit()

    print("\nLe vite sono state resettate.")


if __name__== "__main__":
    resetVite()