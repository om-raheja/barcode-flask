#!/usr/bin/env python3
import sqlite3
from flask import Flask, request, jsonify, send_from_directory
from flask import make_response
from os import urandom
from base64 import b64encode

app = Flask(__name__)

def get_db():
    db = sqlite3.connect("main.sqlite")
    return db

@app.route("/users", methods=["POST"])
def create_user():
    db = get_db()
    cursor = db.cursor()
    user = request.form["user"]
    password = request.form["password"]
    salt = request.form["salt"]
    cursor.execute("INSERT INTO users (user, password, salt) \
            VALUES (?, ?, ?)"
            , (user, password, salt))
    db.commit()
    return jsonify({"message": "User created successfully"})

@app.route("/login", methods=["POST"])
def login():
    db = get_db()
    cursor = db.cursor()
    
    user = request.form["user"]
    password = request.form.get("password", None)
    if password is None:
        cursor.execute("SELECT salt FROM users WHERE user = ?", (user,))
        user = cursor.fetchone()
        if user is None:
            return jsonify({}), 404

        print(user[0])

        return make_response(user[0], 200)
        

    cursor.execute("SELECT id FROM users WHERE user = ? AND password = ?",
                   (user, password))

    user_id = cursor.fetchone()

    if user_id is None:
        return jsonify({}), 403


    token = b64encode(urandom(16)).decode('utf-8')
    cursor.execute("INSERT INTO token (id, token, expiry) VALUES (?,?,\
            unixepoch(datetime(\"NOW\", \"+30 days\"))) \
            RETURNING expiry;", 
                   (user_id[0], token))
    response = make_response("", 204)
    response.set_cookie("token", value=token, expires=cursor.fetchone()[0])

    return response

@app.route("/products.json")
def products():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products;")

    return jsonify(cursor.fetchall())


@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/<path:path>")
def serve_static_path(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(debug=True)
