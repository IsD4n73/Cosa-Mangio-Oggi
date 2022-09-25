from flask import Flask, render_template, request, Response


app = Flask(__name__)
app.config["DEBUG"] = True



@app.route('/')
def main():
     return "App.py"


if __name__=="__main__":
    app.run()