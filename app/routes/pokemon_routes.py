from flask import Blueprint, jsonify
from app.service.pokemon_service import fetch_pokemon, fetch_lst_pokemon, fetch_evolution_chain, fetch_list_pokemon_pagine, fetch_pokemon_name_list_pagine
from flask_jwt_extended import jwt_required

pokemon_bp = Blueprint('pokemon', __name__)

@pokemon_bp.route('/<name>', methods=['GET'])
#@jwt_required()
def get_pokemon(name):
    """Route pour récupérer les infos d'un Pokémon"""
    data = fetch_pokemon(name)
    if data:
        return jsonify(data)
    return jsonify({"error": "Pokémon non trouvé"}), 404


@pokemon_bp.route('/list_name',methods=['GET']) # pas opti 
@jwt_required()
def get_list_pokemon():
    data = fetch_lst_pokemon()
    if data:
        return data
    
@pokemon_bp.route('/pokemon_list_pagine/<n>', methods=['GET'])
#@jwt_required()
def get_list_pokemon_pagine(n):
    data = fetch_list_pokemon_pagine(n)
    if data:
        return jsonify(data)
    return jsonify({"error": "Eurreur l'or de la recuperation des pokemons"}), 404

@pokemon_bp.route('/pokemon_name_list_pagine/<n>', methods=['GET'])
#@jwt_required()
def get_list_pokemon_name_pagine(n):
    data = fetch_pokemon_name_list_pagine(n)
    if data:
        return jsonify(data)
    return jsonify({"error": "Eurreur l'or de la recuperation des noms des pokemons"}), 404


@pokemon_bp.route('/species/<name>', methods=['GET'])
@jwt_required()
def get_evolution_chain(name):
    data = fetch_evolution_chain(name)
    if data:
        return jsonify(data)
    return jsonify({"error": "impossible d'accédé a la chaine evolution"}), 404