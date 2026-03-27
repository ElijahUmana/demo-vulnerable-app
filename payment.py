"""Payment processing endpoint with security issues."""
import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# CWE-798: Hardcoded credentials (obfuscated for demo)
STRIPE_KEY = os.environ.get("STRIPE_KEY", "PLACEHOLDER_REPLACE_ME")
DB_PASSWORD = "admin123"  # Hardcoded DB password

@app.route("/api/payments/charge", methods=["POST"])
def charge():
    amount = request.json.get("amount")
    card = request.json.get("card_number")

    # CWE-89: SQL injection via string formatting
    conn = sqlite3.connect("payments.db")
    conn.execute(f"INSERT INTO transactions (amount, card) VALUES ({amount}, '{card}')")
    conn.commit()

    # CWE-209: Leaking internal paths
    return jsonify({
        "status": "charged",
        "amount": amount,
        "db_path": os.path.abspath("payments.db"),
    })

@app.route("/api/payments/refund", methods=["POST"])
def refund():
    txn_id = request.json.get("transaction_id")
    # CWE-78: Command injection via user input
    os.system(f"curl -X POST https://api.example.com/refund/{txn_id}")
    return jsonify({"status": "refunded"})

@app.route("/api/payments/export", methods=["GET"])
def export():
    filename = request.args.get("file")
    # CWE-22: Path traversal
    with open(f"/data/exports/{filename}") as f:
        return f.read()
