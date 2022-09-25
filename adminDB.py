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
    </tr>
  </thead>
  <tbody> 
    """
    for row in rows:
        
        ris += f"""
        <tr>
         <th scope="row">{row["id_utente"]}</th>
         <td>{row["username"]}</td>
         <td>{row["email"]}</td>
        </tr>
         """
    ris += """</tbody>
    </table>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-u1OknCvxWvY5kfmNBILK2hRnQC3Pr17a+RTT6rIHI7NnikvbZlHgTPOOmMi466C8" crossorigin="anonymous"></script>
    </body>
    </html>
    """
    return ris

def vediAdmin(conn):
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
    </tr>
  </thead>
  <tbody> 
    """
    for row in rows:
        
        ris += f"""
        <tr>
         <th scope="row">{row["id_admin"]}</th>
         <td>{row["user"]}</td>
         <td>{row["lvl_permessi"]}</td>
        </tr>
         """
    ris += """</tbody>
    </table>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-u1OknCvxWvY5kfmNBILK2hRnQC3Pr17a+RTT6rIHI7NnikvbZlHgTPOOmMi466C8" crossorigin="anonymous"></script>
    </body>
    </html>
    """
    return ris


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

def adminLogin(conn, user, psw):
    cur = conn.cursor()
    sql = f"SELECT * FROM admin WHERE user = '{user}' AND password = '{psw}'"
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        if row["user"] == user and row["password"] == psw:
            permessi = row["lvl_permessi"]
            return True, permessi
        return False