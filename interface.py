import streamlit as st
import requests

API_URL_POKEMON = "http://127.0.0.1:5000/api/pokemon"
API_URL_ABILITY = "http://127.0.0.1:5000/api/ability"

#Barre latérale pour la navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisissez une recherche :", ["🔍 Pokémon", "⚡ Ability"])

st.title("Pokédex LC")

####Partie Recherche Pokémon####
if page == "🔍 Pokémon":
    st.header("Recherche d'un Pokémon")

    @st.cache_data
    def get_pokemon_list():
        response = requests.get(f"{API_URL_POKEMON}/list_name")
        if response.status_code == 200:
            return response.json()
        return []


    pokemon_lst_name = get_pokemon_list()
    selected_pokemon = st.selectbox("Recherchez un Pokémon :", pokemon_lst_name)

    if st.button("Afficher les informations"):
        response = requests.get(f"{API_URL_POKEMON}/{selected_pokemon.lower()}")
        if response.status_code == 200:
            data = response.json()
            st.subheader(f"⭐ {data['name'].capitalize()} ⭐")
            st.image(data["image"], caption=f"{data['name'].capitalize()}")
            st.write(f"**Taille :** {data['height']} dm")
            st.write(f"**Poids :** {data['weight']} hg")
            st.write(f"**Type(s) :** {', '.join(data['types'])}")

            response = requests.get(f"{API_URL_POKEMON}/species/{selected_pokemon.lower()}")
            if response.status_code == 200:
                st.write("### Chaine d'évolution:")
                species_data = response.json()
                cols = st.columns(len(species_data))

                for i, pokemon_name in enumerate(species_data):
                    pokemon_response = requests.get(f"{API_URL_POKEMON}/{pokemon_name.lower()}")
                    if pokemon_response.status_code == 200:
                        pokemon_data = pokemon_response.json()
                        with cols[i]:
                            st.image(pokemon_data["image"], width=100)
                            st.write(pokemon_data["name"].capitalize())
                    else:
                        st.write(f"❌ Impossible de récupérer {pokemon_name.capitalize()}")


        else:
            st.error("Pokémon non trouvé. 😢")


####Partie Recherche Ability####
elif page == "⚡ Ability":
    st.header("Recherche d'une Ability")

    @st.cache_data
    def get_ability_list():
        response = requests.get(f"{API_URL_ABILITY}/list")
        if response.status_code == 200:
            return response.json()
        return []

    ability_lst_name = get_ability_list()
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
                    pokemon_response = requests.get(f"{API_URL_POKEMON}/{pokemon.lower()}")
                    if pokemon_response.status_code == 200:
                        pokemon_data = pokemon_response.json()
                        col1, col2 = st.columns([1, 3])  
                        with col1:
                            st.image(pokemon_data["image"], width=100)  # ✅ Affichage de l'image
                        with col2:
                            st.write(f"**{pokemon_data['name'].capitalize()}**")
                            st.write(f"Taille : {pokemon_data['height']} dm")
                            st.write(f"Poids : {pokemon_data['weight']} hg")
                            st.write(f"Type(s) : {', '.join(pokemon_data['types'])}")
                    else:
                        st.write(f"❌ Impossible de récupérer les infos de {pokemon.capitalize()}")
            else:
                st.write("Aucun Pokémon ne possède cette Ability.")
    else:
        st.error("Ability non trouvée. 😢")
