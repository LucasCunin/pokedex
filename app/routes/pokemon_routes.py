from flask import Blueprint, jsonify
from app.service.pokemon_service import fetch_pokemon, fetch_lst_pokemon, fetch_evolution_chain

pokemon_bp = Blueprint('pokemon', __name__)

@pokemon_bp.route('/pokemon/<name>', methods=['GET'])
def get_pokemon(name):
    """Route pour récupérer les infos d'un Pokémon"""
    data = fetch_pokemon(name)
    if data:
        return jsonify(data)
    return jsonify({"error": "Pokémon non trouvé"}), 404


@pokemon_bp.route('pokemon/list_name',methods=['GET']) # pas opti 
def get_list_pokemon():
    data = fetch_lst_pokemon()
    if data:
        return data
    

@pokemon_bp.route('pokemon/species/<name>', methods=['GET'])
def get_evolution_chain(name):
    data = fetch_evolution_chain(name)
    if data:
        return jsonify(data)
    return jsonify({"error": "impossible d'accédé a la chaine evolution"}), 404