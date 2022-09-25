from flask import Flask, render_template, request, Response, jsonify
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
app.config["DEBUG"] = True



@app.route('/')
def main():
     return "App.py"


if __name__=="__main__":
    app.run()