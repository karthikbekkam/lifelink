from flask import Flask
import os

from config import Config

from extensions import db
from extensions import bcrypt
from extensions import login_manager
from extensions import mail

app = Flask(__name__)

app.config.from_object(Config)

app.config["UPLOAD_FOLDER"] = os.path.join(
    app.root_path,
    "static",
    "uploads"
)

os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

from routes.home import home_bp
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.donor import donor_bp
from routes.needer import needer_bp

app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(donor_bp)
app.register_blueprint(needer_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)