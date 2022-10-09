import sqlite3
from json import dumps

# LOGIN UTENTE
def login(conn, email, psw):
    log = False
    user = ""
    cur = conn.cursor()
    sql = f"SELECT * FROM login WHERE email = '{email}' AND password = '{psw}'"
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        if row["email"] == email and row["password"] == psw:
            log = True
            user = row["username"]
    return log, user



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


# PROFILO UTENTE
def getProfile(conn, user):
    cur = conn.cursor()

    sql = f"SELECT * FROM login WHERE username = '{user}'"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        username = row["username"]
        coins = row["coins"]
        domande = row["domande_pubblicate"]
        risposte = row["risposte_date"]
        vite = row["vite"]
    return username, coins, domande, risposte, vite




# OTTIENI DOMANDE
def getSingolaDomanda(conn, id):
    cur = conn.cursor()

    sql = f"SELECT * FROM domande WHERE id_domanda = {id}"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        messaggio = row["messaggio"]
        risposta = row["risposta"]

    return messaggio, risposta


# RIMUOVI VITA
def rimuoviVita(conn, user):
    cur = conn.cursor()
    sql = f"UPDATE login SET vite = vite - 1 WHERE username = '{user}'"
    cur.execute(sql)
    conn.commit()

# MODIFICA COINS
def editCoins(conn, user, coins):
    cur = conn.cursor()
    sql = f"UPDATE login SET coins = coins + {coins} WHERE username = '{user}'"
    cur.execute(sql)
    conn.commit()


# OTTIEN VITE DA UTENTE
def getVite(conn, user):
    cur = conn.cursor()

    sql = f"SELECT * FROM login WHERE username = '{user}'"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        return row["vite"]


# OTTIENI DOMANDE
def getDomande(conn, idUtente):
    cur = conn.cursor()

    sql = f"SELECT * FROM domande WHERE utente IS NOT {idUtente} ORDER BY RANDOM()"
    cur.execute(sql)
    rows = cur.fetchall()
    data = []

    for row in rows:
        ris = {
            "id" : row["id_domanda"],
            "risposta" : row["risposta"],
            "messaggio" : row["messaggio"],
            "utente" : row["utente"],
        }
        data.append(ris)
    
    return dumps(data)

# OTTIENI COUN DOMANDE
def getCountDomande(conn, idUtente):
    cur = conn.cursor()

    sql = f"SELECT COUNT(*) AS tot FROM domande WHERE utente IS NOT {idUtente}"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        return row["tot"]


# GESTIONE CORRETTE
def addVittoria(conn, user):
    cur = conn.cursor()
    sql = f"UPDATE login SET risposte_date = risposte_date + 1 WHERE username = '{user}'"
    cur.execute(sql)
    conn.commit()


# GET ID UTENTE
def getIdUtente(conn, user):
    cur = conn.cursor()

    sql = f"SELECT * FROM login WHERE username = '{user}'"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        return row["id_utente"]