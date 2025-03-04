from flask import Blueprint, jsonify
from app.service.ability_service import fetch_ability, fetch_all_abilities

ability_bp = Blueprint('ability', __name__)

@ability_bp.route('/<name>', methods=['GET'])
def get_ability(name):
    data = fetch_ability(name)
    if data:
        return jsonify(data)
    return jsonify({"error": "attaque non trouvé"}), 404


@ability_bp.route('/list', methods=['GET'])
def get_ability_list():
    abilities = fetch_all_abilities()
    return jsonify(abilities)