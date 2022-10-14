from flask import Flask, render_template, request, session, redirect
from connection import create_connection
from operazioniDB import getDomande, getVite, login,  register, getProfile, getSingolaDomanda, rimuoviVita, editCoins
from operazioniDB import getCountDomande, addVittoria, getIdUtente, getUserFromQuest, getProfilePic, addXP, xpToLvl
from operazioniDB import getProfileEdit, profileEdit, checkUsername
from adminDB import addAdmin, rimuoviAdmin, rimuoviUtente, svuotaTabella, vediAdmin, vediLogin, adminLogin, getAdminPerm
from variabili import database, goodCoins, xpToAdd
from json import loads

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
     try:
          user = session["logged-user"]
     except:
          return  render_template("presentazione.html")

     conn = create_connection(database)
     with conn:
          id = getIdUtente(conn, user)
          lunghezza = getCountDomande(conn, id)
          lista = loads(getDomande(conn, id))
          return render_template("index.html", domande=lista, lun=lunghezza)
     
# MODIFICA PROFILO GET
@app.route('/profilo/modifica', methods=["GET"])
def editProf():
     try:
          username = session["logged-user"]
     except:
          return redirect("/login")

     conn = create_connection(database)
     with conn:
          user, email, psw, pic = getProfileEdit(conn, username)
     return render_template("editProfilo.html", user=user, email=email, psw=psw, pic=pic)


# MODIFICA PROFILO POST
@app.route('/profilo/modifica', methods=["POST"])
def editProfPost():
     try:
          username = session["logged-user"]
     except:
          return redirect("/login")

     try:
          user = request.form["username"]
          email = request.form["email"]
          psw = request.form["password"]
          vecchioUser = request.form["vecchioUser"]
          if len(request.form["link-pic"]) > 5:
               pic = request.form["link-pic"]
          else:
               pic = "NULL"
     except:
          return redirect("/profilo")
     conn = create_connection(database)
     with conn:
          if checkUsername(conn, user) == False:
               profileEdit(conn, vecchioUser, user, email, psw, pic)
               session["logged-user"] = user

          return redirect("/profilo")


     


# PROFILO
@app.route('/profilo')
def prof():
     try:
          username = session["logged-user"]
     except:
          return redirect("/login")

     conn = create_connection(database)
     with conn:
          user, coins, domande, risposte, vite, xp = getProfile(conn, username)
          pic = getProfilePic(conn, username)
          lvl = xpToLvl(conn, username)
          return render_template("profilo.html", coins=coins, domande=domande, risposte=risposte, username=user, vite=vite, propic=pic, lvl=lvl)


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


# CONTROLLO PAROLA INSERITA
@app.route("/indovina/risposta/<id>", methods=["POST", "GET"])
def provaIndovina(id):
     parola = ""
     try: 
          if session["logged-user"] == None:
               return redirect("/login")
     except:
          return redirect("/login")
     
     conn = create_connection(database)

     try:
          parola = request.form["inp-word"].lower()
          if getVite(conn, session["logged-user"]) == 0:
               return redirect("/") 
     except:
          redirect("/")  
           
     with conn:
          messaggio, risposta, user = getSingolaDomanda(conn, id)

          if parola == risposta.lower():
               editCoins(conn, session["logged-user"], goodCoins)
               addVittoria(conn, session["logged-user"])
               addXP(conn, session["logged-user"], xpToAdd)
               return render_template("status.html", stat=True, id=id)
          else:
               rimuoviVita(conn, session["logged-user"])
               return render_template("status.html", stat=False, id=id)


# CARICA SCHERMATA INSERIMENTO PAROLA
@app.route("/indovina/<id>")
def indovinaParola(id):
     
     try: 
          if session["logged-user"] == None:
               return redirect("/login")
     except:
          return redirect("/login")

     conn = create_connection(database)
     with conn:
          username = getUserFromQuest(conn, id)
          

          if getVite(conn, session["logged-user"]) == 0:
               return redirect("/")
          else:
               messaggio, risposta, user = getSingolaDomanda(conn, id)
               
               if user == username:
                    return redirect("/")
     return render_template("indovina.html", msg=messaggio, ris=risposta, id=id, lunRis=len(risposta))





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
     return render_template("loading.html")



if __name__== "__main__":
    app.run()
