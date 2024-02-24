#!/usr/bin/env python3
import sqlite3
from flask import Flask, request, jsonify
from flask import render_template
import data

app = Flask(__name__)

def get_db():
    db = sqlite3.connect("example.db")
    return db

@app.route("/users", methods=["GET"])
def get_users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify(users)

@app.route("/users", methods=["POST"])
def create_user():
    db = get_db()
    cursor = db.cursor()
    name = request.form["name"]
    email = request.form["email"]
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    db.commit()
    return jsonify({"message": "User created successfully"})

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    return jsonify(user)

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    db = get_db()
    cursor = db.cursor()
    name = request.form["name"]
    email = request.form["email"]
    cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
    db.commit()
    return jsonify({"message": "User updated successfully"})

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    return jsonify({"message": "User deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
