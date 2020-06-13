from app import app
from flask import request, render_template, jsonify
from .engine import ask_bot


@app.route("/index")
def index():
    return "Welcome to Doc Chat Bot!!!"


@app.route("/", methods=["GET"])
def query_form():
    return render_template("query_form.html")

@app.route("/", methods=['POST'])
def query_form_post():
    text =  request.form['message']
    processed_text = text.upper()
    response = ask_bot(processed_text)
    return render_template("reply.html", bot=response)
