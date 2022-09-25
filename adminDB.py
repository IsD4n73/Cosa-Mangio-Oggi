import sqlite3

# Il file contiene tutte le funzioni per operazioni sul DB da admin 
# ad esempio svuotare una tabella oppure eliminare una riga specifica

def svuotaTabella(conn, tabella):
    cur = conn.cursor()

    sql = f"DELETE FROM {tabella}"
    cur.execute(sql)

def vediLogin(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM login")
    rows = cur.fetchall()

    ris = ""
    for row in rows:
        
        ris += f"""
         <b>ID:</b> {row["id_utente"]} <br>
         <b>USERNAME:</b> {row["username"]}<br>
         <b>EMAIL:</b> {row["email"]}<br>
         
         <br><br>
         """
    return ris