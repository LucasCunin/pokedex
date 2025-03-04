import requests

def fetch_ability(name):
    url = f"https://pokeapi.co/api/v2/ability/{name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "name": name,
            "effet": next((effect['effect'] for effect in data['effect_entries'] if effect["language"]["name"] == 'en'), ""),
            "description": next((description['flavor_text'] for description in data['flavor_text_entries'] if description["language"]["name"] == 'en'), ""),
            "pokemon": [pokemon['pokemon']['name'] for pokemon in data['pokemon']]
        }
    return None

def fetch_all_abilities():
    """Récupère la liste de toutes les abilities depuis PokéAPI."""
    response = requests.get("https://pokeapi.co/api/v2/ability?limit=10000")
    if response.status_code == 200:
        data = response.json()
        return [ability["name"] for ability in data["results"]]
    return []