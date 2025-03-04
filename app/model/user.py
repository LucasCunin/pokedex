from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Hash et stocke le mot de passe."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Vérifie si le mot de passe entré correspond au hash enregistré."""
        return check_password_hash(self.password_hash, password)
