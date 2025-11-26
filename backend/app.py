from flask import Flask
from flask_cors import CORS
from routes.auth import auth_blueprint
from database import init_db

app = Flask(__name__)
CORS(app)

init_db()

app.register_blueprint(auth_blueprint, url_prefix="/api/auth")


@app.get("/")
def home():
    return {"message": "Backend is running!"}


if __name__ == "__main__":
    app.run(debug=True)
