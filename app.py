from flask import Flask, render_template, request, session, jsonify, redirect
from connection import create_connection
from operazioniDB import login,  register
from adminDB import addAdmin, rimuoviAdmin, rimuoviUtente, svuotaTabella, vediAdmin, vediLogin, adminLogin
from variabili import database

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "COsaMangioOggKeySecret23"




#                   URLS     
############################################################

# HOMEPAGE
@app.route('/')
def main():
     return """
     App.py <br>
     <a href='/admin'> Admin </a> <br>
     <a href='/login'> Login </a> <br>
     <a href='/registrati'> Registrati </a> <br>
     """

# LOGIN GET
@app.route('/login', methods=["GET"])
def userlog():
     return render_template("login.html")

# LOGIN POST
@app.route('/login', methods=["POST"])
def entrata():

     email = request.form['email']
     password = request.form['password']

     conn = create_connection(database)
     with conn:
          loged = login(conn, email, password)
          if loged:
               return redirect("/user")
          else:
               return redirect("/login")

# REGISTRATI GET
@app.route('/registrati', methods=["GET"])
def regiget():
     return render_template("register.html")

# REGISTRATI POST
@app.route('/registrati', methods=["POST"])
def regi():
     
     email = request.form['email']
     password = request.form['password']
     username = request.form['username']

     conn = create_connection(database)
     with conn:
          registrato = register(conn, email, password, username)
          return render_template("register.html", mess=registrato)


#                   ADMIN     
############################################################

# ADMIN LOGIN
@app.route("/admin")
def adminLog():
     return render_template("admin-login.html")

# ADMIN DASHBOARD
@app.route("/admin/dashboard", methods=["POST"])
def adminDash():
     username = request.form["user"]
     psw = request.form["psw"]

     conn = create_connection(database)
     with conn:
          login, permessi = adminLogin(conn, username, psw)
          if login:
               session["logged-admin"] = username
               return render_template("admin-dash.html", lvlPermessi=permessi)
          else:
               return redirect("/admin")

# ADMIN LOGOUT
@app.route("/admin/logout")
def adminout():
     session.pop("username", None)
     return redirect("/")

# AGGIUNGI ADMIN
@app.route("/admin/add-admin", methods=["POST"])
def adminAdd():
     conn = create_connection(database)
     with conn:
          addAdmin(conn, request.form["username"], request.form["password"], request.form["lvl"])
          return redirect("/admin/dashboard")


# SVUOTA TABELLA
@app.route("/admin/rimuovi", methods=["POST"])
def adminRem():
     conn = create_connection(database)
     with conn:
          svuotaTabella(conn,request.form["nomeTabella"])
     return redirect("/admin/dashboard")

# RIMUOVI ADMIN 
@app.route("/admin/rimuovi-admin/<id>", methods=["GET"])
def rimuoviAdminID(id):
     conn = create_connection(database)
     with conn:
          rimuoviAdmin(conn, id)
     return redirect("/admin/dashboard")

# RIMUOVI UTENTE
@app.route("/admin/rimuovi-utente/<id>", methods=["GET"])
def rimuoviUserID(id):
     conn = create_connection(database)
     with conn:
          rimuoviUtente(conn, id)
     return redirect("/admin/dashboard")


#VEDI TABELLA
@app.route("/admin/vedi", methods=["POST"])
def vedLog():
     conn = create_connection(database)
     with conn:
          if request.form["nomeTabella"] == "login":
               return vediLogin(conn)
          elif request.form["nomeTabella"]  == "admin":
               return vediAdmin(conn)
          else:
               return redirect("/admin/dashboard")









#                   GESTIONE URL     
############################################################

@app.route("/admin/dashboard", methods=["GET"])
def dashget():
     return redirect("/")









if __name__== "__main__":
    app.run()