from flask import Blueprint, request
from database import SessionLocal
from models import User

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.post("/signup")
def signup():
    db = SessionLocal()
    data = request.json

    new_user = User(
        username=data["username"], password=data["password"], email=data["email"]
    )
    db.add(new_user)
    db.commit()

    return {"message": "User created successfully"}


@auth_blueprint.post("/login")
def login():
    db = SessionLocal()
    data = request.json

    user = (
        db.query(User)
        .filter_by(username=data["username"], password=data["password"])
        .first()
    )

    if not user:
        return {"error": "Invalid credentials"}, 401

    return {"message": "Login successful", "user_id": user.id}
