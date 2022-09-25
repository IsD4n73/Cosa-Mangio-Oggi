from flask import Flask, render_template, request, Response, jsonify
from connection import login, create_connection, register

app = Flask(__name__)
app.config["DEBUG"] = True

database = r"./data/cosamangio.db"


@app.route('/')
def main():
     return "App.py"

@app.route('/login')
def entrata():
     email = request.form['email']
     password = request.form['password']
     conn = create_connection(database)
     with conn:
          loged = login(conn, email, password)


@app.route('/registrati')
def regi():
     # email = request.form['email']
     # password = request.form['password']
     # username = request.form['username']
     email = "d4n73@gmail.com"
     username = "D4n73"
     password = "Admin"
     conn = create_connection(database)
     with conn:
          registrato = register(conn, email, password, username)
          return registrato


if __name__=="__main__":
    app.run()