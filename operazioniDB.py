import sqlite3

# LOGIN UTENTE
def login(conn, email, psw):
    log = False
    cur = conn.cursor()
    sql = f"SELECT * FROM login WHERE email = '{email}' AND password = '{psw}'"
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        if row["email"] == email and row["password"] == psw:
            log = True
    return log



# REGISTRA UTENTE
def register(conn, email, psw, user):
    cur = conn.cursor()

    sql = f"SELECT * FROM login WHERE email = '{email}' OR username = '{user}'"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
            if row["email"] == email:
                return f"Email ({email}) gia esistente..."
            if row["username"] == user:
                return f"Username ({user}) gia esistente..."

    sql = f"INSERT INTO login (username, email, password) VALUES ('{user}', '{email}','{psw}')"
    cur.execute(sql)
    conn.commit()
    return "Utente registrato!"


# OTTIENI DOMANDE
def getDomande(conn):
    cur = conn.cursor()

    sql = f"SELECT * FROM domande ORDER BY RANDOM()"
    cur.execute(sql)
    rows = cur.fetchall()
    ris = ""
    for row in rows:
        ris += f"""
        {row["id_domanda"]} \n
        {row["risposta"]} \n
        {row["messaggio"]} \n
        {row["utente"]} \n\n
        """
    print(ris)
    return ris