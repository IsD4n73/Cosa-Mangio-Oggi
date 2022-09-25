from operator import truediv
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

def adminLogin(conn, user, psw):
    cur = conn.cursor()
    sql = f"SELECT * FROM admin WHERE user = '{user}' AND password = '{psw}'"
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        if row["user"] == user and row["password"] == psw:
            return True
        return False