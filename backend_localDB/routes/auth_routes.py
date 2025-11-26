from flask import Blueprint, request, jsonify
from backend_localDB.db import get_connection

import bcrypt

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data["username"]
    email = data["email"]
    password = data["password"]

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, user_type)
            VALUES (%s, %s, %s, 'resident')
        """,
            (username, email, hashed_pw.decode()),
        )

        conn.commit()
        return jsonify({"message": "Signup successful"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return jsonify({"message": "Login successful", "user": user})
    else:
        return jsonify({"error": "Incorrect password"}), 401
