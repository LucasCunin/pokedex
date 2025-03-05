import requests

def fetch_pokemon(name):
    """Récupère les informations détaillées d'un Pokémon."""
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        species_url = data["species"]["url"]
        species_response = requests.get(species_url)
        if species_response.status_code == 200:
            species_data = species_response.json()
            color = species_data["color"]["name"]
            origin_game = species_data["generation"]["name"]
        else:
            color = "Inconnu"
            origin_game = "Inconnu"

        return {
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data["types"]],
            "image": data["sprites"]["front_default"],
            "color": color,
            "generation": len(origin_game.split('-')[1])
        }
    return None


def fetch_lst_pokemon():
    lst = []
    url = "https://pokeapi.co/api/v2/pokemon?limit=10000"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for pokemon in data['results']:
            lst.append(pokemon["name"])
            lst.sort()
        return lst
    return None

def fetch_list_pokemon_pagine(n):
    dic = {}
    page_num = 1
    n = int(n)
    url = "https://pokeapi.co/api/v2/pokemon?limit=10000"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        all_pokemon = data['results']  
        dic[page_num] = []  
        
        for pokemon in all_pokemon:
            poke_name = pokemon['name']
            data_pokemon = fetch_pokemon(poke_name)
            if data_pokemon:
                dic[page_num].append(data_pokemon) 
                
                if len(dic[page_num]) >= n:  
                    page_num += 1  
                    dic[page_num] = [] 
        return dic
    return None

def fetch_pokemon_name_list_pagine(n):
    dic = {}
    page_num = 1
    n = int(n)
    url = "https://pokeapi.co/api/v2/pokemon?limit=10000"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        all_pokemon = data['results']  
        dic[page_num] = []  
        
        for pokemon in all_pokemon:
            dic[page_num].append(pokemon['name'])

            if len(dic[page_num]) >= n:  
                    page_num += 1  
                    dic[page_num] = []
        return dic
    return None

def fetch_evolution_chain(name):
    """
    Récupère la liste complète des Pokémon dans la chaîne d'évolution.
    Retourne une liste contenant tous les Pokémon de la ligne évolutive.
    """
    buf_url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}"
    response = requests.get(buf_url)

    if response.status_code == 200:
        buf_data = response.json()
        evolution_chain_url = buf_data["evolution_chain"]["url"]

        response = requests.get(evolution_chain_url)
        if response.status_code == 200:
            data = response.json()

            evolution_list = []

            # Fonction récursive pour parcourir la chaîne d'évolution
            def parse_evolution_chain(chain):
                evolution_list.append(chain["species"]["name"])  # Ajoute le Pokémon actuel
                for evolution in chain["evolves_to"]:
                    parse_evolution_chain(evolution)  # Parcours récursif

            # Début du parsing à partir de la racine
            parse_evolution_chain(data["chain"])

            return evolution_list
    
    return None