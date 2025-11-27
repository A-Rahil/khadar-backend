from flask import Flask
from flask_cors import CORS
from backend_localDB.routes.auth_routes import auth


app = Flask(__name__)
CORS(app)

app.register_blueprint(auth, url_prefix="/auth")


@app.route("/")
def home():
    return {"status": "API is running"}


if __name__ == "__main__":
    app.run(debug=True, port=5000)  # your teammate will call this port
