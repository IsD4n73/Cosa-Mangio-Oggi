from math import sqrt
from json import dumps

from numpy import true_divide
from variabili import moltiplicaXp

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

# OTTIENI VALORI MODIFICA
def getProfileEdit(conn, user):
    cur = conn.cursor()

    sql = f"SELECT * FROM login WHERE username = '{user}'"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        username = row["username"]
        email = row["email"]
        psw = row["password"]
        pic = row["link_pic"]
    return username, email, psw, pic

# MODIFICA PROFILO
def profileEdit(conn, vecchioUser, username, email, psw, pic):
    cur = conn.cursor()
    sql = f"UPDATE login SET username = '{username}', email = '{email}', password = '{psw}', link_pic = '{pic}' WHERE username = '{vecchioUser}'"
    cur.execute(sql)
    conn.commit()


# CONTROLLO USERNAME
def checkUsername(conn, user):
    cur = conn.cursor()

    sql = f"SELECT * FROM login WHERE username = '{user}'"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        if row["username"] == user:
            return True
    return False

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
        xp = row["xp"]
    return username, coins, domande, risposte, vite, xp




# OTTIENI DOMANDE
def getSingolaDomanda(conn, id):
    cur = conn.cursor()

    sql = f"SELECT * FROM domande WHERE id_domanda = {id}"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        messaggio = row["messaggio"]
        risposta = row["risposta"]
        user = row["utente"]

    return messaggio, risposta, user


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

# OTTIENI COUNT DOMANDE
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

# GET UTENTE DALLA DOMANDA
def getUserFromQuest(conn, id):
    cur = conn.cursor()
    sql = f"SELECT * FROM login L, domande D WHERE D.id_domanda = {id} AND L.id_utente = D.utente"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        return row["id_utente"]

# GET PIC URL
def getProfilePic(conn, username):
    cur = conn.cursor()

    sql = f"SELECT * FROM login WHERE username = '{username}'"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        return row["link_pic"]

# GET XP UTENTE
def getXP(conn, user):
    cur = conn.cursor()

    sql = f"SELECT xp FROM login WHERE username = '{user}'"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        return row["xp"]
    

# XP TO LVL
def xpToLvl(conn, user):
    lvl = moltiplicaXp * sqrt(getXP(conn, user))
    return int(lvl)

# LVL TO XP
def lvlToXp(conn, user):
    return pow((xpToLvl(conn, user) / moltiplicaXp), 2)

# ADD XP TO USER
def addXP(conn, user, ammount):
    cur = conn.cursor()
    sql = f"UPDATE login SET xp = xp + {ammount} WHERE username = '{user}'"
    cur.execute(sql)
    conn.commit()

