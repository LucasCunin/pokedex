from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from datetime import timedelta
from app.model.user import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Créer un nouvel utilisateur."""
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email et mot de passe requis"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Cet utilisateur existe déjà"}), 400

    new_user = User(email=data['email'])
    new_user.set_password(data['password'])  # Hash le mot de passe
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "Utilisateur cree avec succes"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authentification et retour d'un token JWT."""
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email et mot de passe requis"}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.verify_password(data['password']):
        return jsonify({"error": "Identifiants invalides"}), 401

    # Générer un token JWT valide pour 1 heure
    access_token = create_access_token(identity=user.email, expires_delta=timedelta(hours=1))
    return jsonify({"access_token": access_token}), 200
