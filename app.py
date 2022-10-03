from flask import Flask, render_template, request, session, jsonify, redirect
from connection import create_connection
from operazioniDB import getDomande, login,  register, getProfile
from adminDB import addAdmin, rimuoviAdmin, rimuoviUtente, svuotaTabella, vediAdmin, vediLogin, adminLogin, getAdminPerm
from variabili import database

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "COsaMangioOggKeySecret23"


#                   ERRORI     
############################################################

# 404 PAGINA NON TROVATA
@app.errorhandler(404)
def paginaNonTrovata(e):
     return render_template("error.html", cod="404", msg="PAGE NOT FOUND"), 404

# 405 NETODO NON PERMESSO
@app.errorhandler(405)
def paginaNonTrovata(e):
     return render_template("error.html", cod="405", msg="METHOD NOT ALLOWED"), 405


#                   URLS     
############################################################

# HOMEPAGE
@app.route('/')
def main():
     return """
     <a href='/admin'> Admin </a> <br>
     <a href='/login'> Login </a> <br>
     <a href='/registrati'> Registrati </a> <br>
     <a href='/profilo'> Profilo </a> <br>
     """


# PROFILO
@app.route('/profilo')
def prof():
     
     conn = create_connection(database)
     try:
          username = session["logged-user"]
     except:
          return redirect("/login")

     with conn:
          user, coins, domande, risposte, vite = getProfile(conn, username)
          return render_template("profilo.html", coins=coins, domande=domande, risposte=risposte, username=user, vite=vite)


# LOGOUT
@app.route('/logout')
def userLogout():
     session.pop("logged-user", None)
     return redirect("/")


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
          loged, username = login(conn, email, password)
          if loged:
               session["logged-user"] = username
               return redirect("/profilo")
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
@app.route("/admin/dashboard", methods=["GET", "POST"])
def adminDash():
     try:
          username = session["logged-admin"]
          psw = session["admin-psw"] 
     except:
          try:
               username = request.form["user"]
               psw = request.form["psw"]
          except:
               redirect("/admin")

     conn = create_connection(database)
     with conn:
          try:
               login, permessi = adminLogin(conn, username, psw)
          except:
               return redirect("/admin")
               
          if login:
               session["logged-admin"] = username
               session["admin-psw"] = psw
               return render_template("admin-dash.html", lvlPermessi=permessi)
          else:
               return redirect("/admin")

# ADMIN LOGOUT
@app.route("/admin/logout")
def adminout():
     session.pop("logged-admin", None)
     session.pop("admin-psw", None)
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
     permessi = getAdminPerm(conn, session["logged-admin"])
     print(permessi)
     with conn:
          if request.form["nomeTabella"] == "login":
               return vediLogin(conn, permessi)
          elif request.form["nomeTabella"]  == "admin":
               return vediAdmin(conn, permessi)
          else:
               return redirect("/admin/dashboard")





#                   GESTIONE URL     
############################################################






#                   TEST URL     
############################################################

@app.route("/test")
def test():
     conn = create_connection(database)
     with conn:
          domande = getDomande(conn)
          return domande


@app.route("/test2")
def test2():
     return render_template("indovina.html")

if __name__== "__main__":
    app.run()
