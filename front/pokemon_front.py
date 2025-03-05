import streamlit as st
import requests
import os
import json

# Chargement des icônes de type
with open("app/type_icons.json", "r") as f:
    TYPE_ICONS = json.load(f)

API_URL_POKEMON = os.getenv("API_URL_POKEMON")

def pokemon_page():
    """Affichage de la page de recherche de Pokémon"""
    st.header("Recherche d'un Pokémon")
    
    if "access_token" not in st.session_state or not st.session_state["access_token"]:
        st.warning("⚠️ Vous devez être connecté pour accéder aux Pokémon.")
        return
    
    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
    response = requests.get(f"{API_URL_POKEMON}/list_name", headers=headers)
    
    if response.status_code == 200:
        pokemon_lst_name = response.json()
    else:
        st.error("Impossible de récupérer la liste des Pokémon.")
        return
    
    selected_pokemon = st.selectbox("Recherchez un Pokémon :", pokemon_lst_name)
    
    if st.button("Afficher les informations"):
        response = requests.get(f"{API_URL_POKEMON}/{selected_pokemon.lower()}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            st.subheader(f"⭐ {data['name'].capitalize()} ⭐")
            st.image(data["image"], caption=f"{data['name'].capitalize()}")
            st.write(f"**Taille :** {data['height']} dm")
            st.write(f"**Poids :** {data['weight']} hg")
            
            st.write("**Type(s) du Pokémon :**")
            cols = st.columns(len(data["types"]))
            for i, type_name in enumerate(data["types"]):
                with cols[i]:
                    type_image = TYPE_ICONS.get(type_name.lower(), None)
                    if type_image:
                        st.image(type_image, width=100)

        #chaine d'evolution
        response = requests.get(f"{API_URL_POKEMON}/species/{selected_pokemon.lower()}", headers=headers)
        if response.status_code == 200:
            st.write("### Chaine d'évolution:")
            species_data = response.json()
            cols = st.columns(len(species_data))

            for i, pokemon_name in enumerate(species_data):
                pokemon_response = requests.get(f"{API_URL_POKEMON}/{pokemon_name.lower()}", headers=headers)
                if pokemon_response.status_code == 200:
                    pokemon_data = pokemon_response.json()
                    with cols[i]:
                        st.image(pokemon_data["image"], width=100)
                        st.write(pokemon_data["name"].capitalize())
        else:
            st.error("Pokémon non trouvé. 😢")