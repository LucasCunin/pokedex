from flask import Flask

def create_app():
    """Création de l'application Flask"""
    app = Flask(__name__)

    from app.routes.pokemon_routes import pokemon_bp
    from app.routes.ability_route import ability_bp 
    app.register_blueprint(pokemon_bp, url_prefix='/api')
    app.register_blueprint(ability_bp, url_prefix='/api')

    return app
