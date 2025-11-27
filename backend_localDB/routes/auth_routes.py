import re
import uuid
import bcrypt
import mysql.connector
from flask import Blueprint, request, jsonify
from backend_localDB.db import get_connection

auth = Blueprint("auth", __name__)

ALLOWED_TYPES = {
    "building_owner",
    "private_firm",
    "technician"
}

EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
PHONE_REGEX = r"^[+]?[0-9]{10,15}$"


# ----------------------------------------------------------
#                           SIGNUP
# ----------------------------------------------------------
@auth.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    # REQUIRED FIELDS
    required = ["username", "email", "password", "user_type"]
    for field in required:
        if field not in data or not data[field]:
            return jsonify({"error": f"{field} is required"}), 400

    username = data["username"].strip()
    email = data["email"].strip()
    phone = data.get("phone_number")
    password = data["password"]
    user_type = data["user_type"]
    uae_pass_id = data.get("uae_pass_id")  # OPTIONAL

    # VALIDATION
    if not re.match(EMAIL_REGEX, email):
        return jsonify({"error": "Invalid email format"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    if phone and not re.match(PHONE_REGEX, phone):
        return jsonify({"error": "Invalid phone number format"}), 400

    if user_type not in ALLOWED_TYPES:
        return (
            jsonify({"error": f"Invalid user_type. Allowed: {list(ALLOWED_TYPES)}"}),
            400,
        )

    # HASH PASSWORD
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user_id = str(uuid.uuid4())

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # ----------------------------------------------------
        # INSERT INTO USERS
        # ----------------------------------------------------
        cursor.execute(
            """
            INSERT INTO users (
                user_id, username, email, phone_number, password_hash,
                uae_pass_id, user_type
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
            (user_id, username, email, phone, password_hash, uae_pass_id, user_type),
        )

        # ----------------------------------------------------
        # INSERT INTO ROLE-SPECIFIC TABLES
        # ----------------------------------------------------
        if user_type == "building_owner":
            cursor.execute(
                """
                INSERT INTO building_owners (buildingOwner_id, user_id)
                VALUES (%s, %s)
            """,
                (str(uuid.uuid4()), user_id),
            )

        elif user_type == "private_firm":
            cursor.execute(
                """
                INSERT INTO private_firm (privateFirm_id, user_id)
                VALUES (%s, %s)
            """,
                (str(uuid.uuid4()), user_id),
            )

        elif user_type == "technician":
            cursor.execute(
                """
                INSERT INTO technicians (technician_id, user_id, experience_level)
                VALUES (%s, %s, %s)
            """,
                (str(uuid.uuid4()), user_id, 0),
            )

        elif user_type == "government_official":
            return jsonify({"error": "government_official table not implemented"}), 500

        conn.commit()

        return (
            jsonify(
                {
                    "message": "User registered successfully",
                    "user_id": user_id,
                    "user_type": user_type,
                }
            ),
            201,
        )

    except mysql.connector.Error as err:
        err_msg = str(err)

        if "Duplicate entry" in err_msg:
            if "username" in err_msg:
                return jsonify({"error": "Username already exists"}), 409
            if "email" in err_msg:
                return jsonify({"error": "Email already exists"}), 409
            if "phone_number" in err_msg:
                return jsonify({"error": "Phone number already exists"}), 409
            if "uae_pass_id" in err_msg:
                return jsonify({"error": "UAE Pass ID already exists"}), 409

        return jsonify({"error": err_msg}), 500

    finally:
        cursor.close()
        conn.close()


# ----------------------------------------------------------
#                           LOGIN
# ----------------------------------------------------------
@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            return jsonify({"error": "Incorrect password"}), 401

        cursor.execute(
            """
            UPDATE users SET last_login_date = NOW()
            WHERE user_id = %s
        """,
            (user["user_id"],),
        )
        conn.commit()

        del user["password_hash"]

        return jsonify({"message": "Login successful", "user": user}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
