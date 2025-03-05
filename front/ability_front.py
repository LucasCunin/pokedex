import streamlit as st
import requests
import os

API_URL_ABILITY = os.getenv("API_URL_ABILITY")
API_URL_POKEMON = os.getenv("API_URL_POKEMON")

def ability_page():
    """Affichage de la page de recherche des abilities"""
    st.header("Recherche d'une Ability")
    
    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"} if "access_token" in st.session_state else {}
    
    @st.cache_data
    def get_ability_list():
        response = requests.get(f"{API_URL_ABILITY}/list")
        return response.json() if response.status_code == 200 else []
    
    ability_lst_name = get_ability_list()
    if not ability_lst_name:
        st.error("Impossible de récupérer la liste des abilities.")
        return
    
    selected_ability = st.selectbox("Recherchez une Ability (en anglais) :", ability_lst_name)
    
    response = requests.get(f"{API_URL_ABILITY}/{selected_ability.lower()}")
    if response.status_code == 200:
        data = response.json()
        st.subheader(f"⭐ Ability : {data['name'].capitalize()} ⭐")
        st.write(f"**Effet :** {data['effet']}")
        st.write(f"**Description :** {data['description']}")
        
        if st.button("Afficher les Pokémon associés"):
            st.subheader("📌 Pokémon possédant cette Ability :")
            if data["pokemon"]:
                for pokemon in data["pokemon"]:
                    pokemon_response = requests.get(f"{API_URL_POKEMON}/{pokemon.lower()}", headers=headers)
                    if pokemon_response.status_code == 200:
                        pokemon_data = pokemon_response.json()
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.image(pokemon_data["image"], width=100)
                        with col2:
                            st.write(f"**{pokemon_data['name'].capitalize()}**")
                            st.write(f"Taille : {pokemon_data['height']} dm")
                            st.write(f"Poids : {pokemon_data['weight']} hg")
                            st.write(f"Type(s) : {', '.join(pokemon_data['types'])}")
                    else:
                        st.write(f"❌ Impossible de récupérer les infos de {pokemon.capitalize()}")