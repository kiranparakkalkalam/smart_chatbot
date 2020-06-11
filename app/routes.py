from app import app
from flask import request, render_template, jsonify
from chatbot import ask_bot


@app.route("/index")
def index():
    return "Welcome to Doc Chat Bot!!!"


@app.route("/")
def query_form():
    return render_template("query_form.html")

@app.route("/", methods=['POST'])
def query_form_post():
    text =  request.form['text']
    processed_text = text.upper()
    response = ask_bot(processed_text)
    return jsonify(response) 
