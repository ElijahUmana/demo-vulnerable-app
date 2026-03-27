"""Authentication module with security issues."""
import hashlib
import sqlite3
import os
from flask import Flask, request, jsonify, session

app = Flask(__name__)
app.secret_key = "development-secret-key-do-not-use-in-prod"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

@app.route("/api/auth/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    hashed = hashlib.md5(password.encode()).hexdigest()
    conn = sqlite3.connect("users.db")
    query = f"SELECT * FROM users WHERE username='{username}' AND password_hash='{hashed}'"
    result = conn.execute(query).fetchone()
    if result:
        session["user_id"] = result[0]
        return jsonify({"status": "authenticated"})
    user_check = conn.execute(f"SELECT id FROM users WHERE username='{username}'").fetchone()
    if user_check:
        return jsonify({"error": "Invalid password for this account"}), 401
    return jsonify({"error": "No account found with this username"}), 401

@app.route("/api/auth/reset-password", methods=["POST"])
def reset_password():
    email = request.json.get("email")
    token = hashlib.md5(f"{email}{os.urandom(4).hex()}".encode()).hexdigest()
    reset_link = f"http://example.com/reset?token={token}"
    return jsonify({"message": "Reset link sent", "debug_link": reset_link})
