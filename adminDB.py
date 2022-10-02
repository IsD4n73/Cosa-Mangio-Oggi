from operator import truediv
import sqlite3

# Il file contiene tutte le funzioni per operazioni sul DB da admin 
# ad esempio svuotare una tabella oppure eliminare una riga specifica

# SVUOTA TABELLA
def svuotaTabella(conn, tabella):
    cur = conn.cursor()

    sql = f"DELETE FROM {tabella}"
    cur.execute(sql)

# VEDI TABELLA LOGIN
def vediLogin(conn, perm):
    cur = conn.cursor()
    cur.execute("SELECT * FROM login")
    rows = cur.fetchall()

    ris = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Visualizza Login</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">
    </head>
    <body>
        
        <table class="table m-4 table-striped table-hover">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">Username</th>
      <th scope="col">Email</th>
      <th scope="col">ELIMINA</th>
    </tr>
  </thead>
  <tbody> 
    """
    for row in rows:
        
        ris += f"""
        <tr>
         <th scope="row">{row["id_utente"]}</th>
         <td>{row["username"]}</td>
         <td>{row["email"]}</td>"""
        if perm >= 2:
            ris += f"""<td><a class="nav-link" style="color:red;" href="/admin/rimuovi-utente/{row["id_utente"]}">Elimina</a></td>"""
        ris += """</tr>
         """
    ris += """</tbody>
    </table>
    <div class="d-grid gap-2 col-6 mx-auto">
        <a class="btn btn-primary" apparence="button" href="/admin/dashboard">Torna Indietro</a>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-u1OknCvxWvY5kfmNBILK2hRnQC3Pr17a+RTT6rIHI7NnikvbZlHgTPOOmMi466C8" crossorigin="anonymous"></script>
    </body>
    </html>
    """
    return ris

# VEDI TABELLA ADMIN
def vediAdmin(conn, perm):
    cur = conn.cursor()
    cur.execute("SELECT * FROM admin")
    rows = cur.fetchall()
    ris = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Visualizza Admin</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">
    </head>
    <body>
        
        <table class="table m-4 table-striped table-hover">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">Username</th>
      <th scope="col">Permessi</th>
      <th scope="col">ELIMINA</th>
    </tr>
  </thead>
  <tbody> 
    """
    for row in rows:
        
        ris += f"""
        <tr>
         <th scope="row">{row["id_admin"]}</th>
         <td>{row["user"]}</td>
         <td>{row["lvl_permessi"]}</td>"""
        if perm >= 3:
            ris += f"""<td><a class="nav-link" style="color:red;" href="/admin/rimuovi-admin/{row["id_admin"]}">Elimina</a></td>"""
        ris +="""</tr>
         """
    ris += """</tbody>
    </table>
    <div class="d-grid gap-2 col-6 mx-auto">
        <a class="btn btn-primary" aparence="button" href="/admin/dashboard">Torna Indietro</a>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-u1OknCvxWvY5kfmNBILK2hRnQC3Pr17a+RTT6rIHI7NnikvbZlHgTPOOmMi466C8" crossorigin="anonymous"></script>
    </body>
    </html>
    """
    return ris


# AGGIUNGI ADMIN
def addAdmin(conn, user, psw, lvl):
    cur = conn.cursor()

    sql = f"SELECT * FROM admin WHERE user = '{user}'"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
            if row["user"] == user:
                return f"Admin ({user}) gia esistente..."

    sql = f"INSERT INTO admin (user, password, lvl_permessi) VALUES ('{user}', '{psw}','{lvl}')"
    cur.execute(sql)
    conn.commit()
    return "Admin inserito"

# LOGIN 
def adminLogin(conn, user, psw):
    cur = conn.cursor()
    sql = f"SELECT * FROM admin WHERE user = '{user}' AND password = '{psw}'"
    cur.execute(sql)
    rows = cur.fetchall()
    permessi = 0
    for row in rows:
        if row["user"] == user and row["password"] == psw:
            permessi = row["lvl_permessi"]
            return True, permessi
        return False, permessi

# RIMUOVI UTENTE
def rimuoviUtente(conn, id):
    cur = conn.cursor()

    sql = f"DELETE FROM login WHERE id_utente = '{id}'"
    cur.execute(sql)
    conn.commit()

# RIMUOVI ADMIN
def rimuoviAdmin(conn, id):
    cur = conn.cursor()

    sql = f"DELETE FROM admin WHERE id_admin = '{id}'"
    cur.execute(sql)
    conn.commit()


# PERMESSI ADMIN
def getAdminPerm(conn, admin):
    cur = conn.cursor()
    sql = f"SELECT * FROM admin WHERE user = '{admin}'"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        if row["user"] == admin:
            return row["lvl_permessi"]