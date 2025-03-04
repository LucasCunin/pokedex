from flask import Flask
from flask_jwt_extended import JWTManager
from app.model.user import db
from app.routes.auth_routes import auth_bp
from app.routes.pokemon_routes import pokemon_bp
from app.routes.ability_route import ability_bp

def create_app():
    """Création de l'application Flask"""
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokedex.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = "super-secret-key"  # 🔐 Clé secrète pour JWT

    db.init_app(app)
    jwt = JWTManager(app)  # Initialisation de JWT

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(pokemon_bp, url_prefix='/api/pokemon')
    app.register_blueprint(ability_bp, url_prefix='/api/ability')

    return app
