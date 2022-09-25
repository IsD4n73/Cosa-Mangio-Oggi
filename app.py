from flask import Flask, render_template, request, Response, jsonify
from connection import create_connection
from operazioniDB import login,  register
from adminDB import svuotaTabella, vediLogin

app = Flask(__name__)
app.config["DEBUG"] = True

database = r"./data/cosamangio.db"



#                   URLS     
############################################################

@app.route('/')
def main():
     return "App.py"

@app.route('/login', methods=["POST"])
def entrata():

     email = request.form['email']
     password = request.form['password']

     conn = create_connection(database)
     with conn:
          loged = login(conn, email, password)
          return render_template("index.html")


@app.route('/registrati', methods=["POST"])
def regi():
     
     email = request.form['email']
     password = request.form['password']
     username = request.form['username']

     conn = create_connection(database)
     with conn:
          registrato = register(conn, email, password, username)
          return registrato


#                   GESTIONE URL     
############################################################

@app.route("/login", methods=["GET"])
def logget():
     return render_template("index.html")

@app.route("/registrati", methods=["GET"])
def regget():
     return render_template("index.html")


#                   ADMIN     
############################################################

@app.route("/admin/rimuovi", methods=["GET"])
def adminRem():
     conn = create_connection(database)
     with conn:
          svuotaTabella(conn, "login")
     return "Operazione compleata."

@app.route("/admin/vedi", methods=["GET"])
def vedLog():
     conn = create_connection(database)
     with conn:
          return vediLogin(conn)



















if __name__== "__main__":
    app.run()