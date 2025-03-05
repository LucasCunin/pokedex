import streamlit as st
import requests
import json
import os

with open("app/type_icons.json", "r") as f:
    TYPE_ICONS = json.load(f)


API_URL_POKEMON = os.getenv("API_URL_POKEMON")
API_URL_ABILITY = os.getenv("API_URL_ABILITY")
API_URL_AUTH = os.getenv("API_URL_AUTH")

# --- Stocker le token JWT dans la session ---
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

# --- Page de connexion ---
st.sidebar.title("🔐 Connexion")

if st.session_state["access_token"]:
    st.sidebar.success("✅ Connecté")
    if st.sidebar.button("Se déconnecter"):
        st.session_state["access_token"] = None
        st.session_state["pokemon_list_loaded"] = False
        st.sidebar.warning("Déconnecté")
        st.rerun()
else:
    st.sidebar.subheader("🔑 Connexion")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Mot de passe", type="password")

    if st.sidebar.button("Se connecter"):
        response = requests.post(f"{API_URL_AUTH}/login", json={"email": email, "password": password})
        if response.status_code == 200:
            st.session_state["access_token"] = response.json()["access_token"]
            st.session_state["pokemon_list_loaded"] = False
            st.sidebar.success("✅ Connexion réussie")
            st.rerun()
        else:
            st.sidebar.error("❌ Identifiants incorrects")

####PAge PRINCIPALE####
#Barre latérale pour la navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisissez une recherche :", ["🔍 Pokémon", "⚡ Ability", "📜 Liste Pokémon"])

st.title("Pokédex LC")

####Partie Recherche Pokémon####
if page == "🔍 Pokémon":
    st.header("Recherche d'un Pokémon")

    def get_pokemon_list():
        if not st.session_state["access_token"]:
            return []  # Si pas connecté, on retourne une liste vide
    
        headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
        response = requests.get(f"{API_URL_POKEMON}/list_name", headers=headers)
        if response.status_code == 200:
            return response.json()
        return []


    if "pokemon_list_loaded" not in st.session_state or not st.session_state["pokemon_list_loaded"]:
        pokemon_lst_name = get_pokemon_list()
        st.session_state["pokemon_list_loaded"] = True
        st.session_state["pokemon_lst_name"] = pokemon_lst_name
    else:
        pokemon_lst_name = st.session_state.get("pokemon_lst_name", [])

    if not pokemon_lst_name:
        st.warning("⚠️ Impossible de charger la liste des Pokémon. Vérifiez votre connexion.")
        st.stop()

    selected_pokemon = st.selectbox("Recherchez un Pokémon :", pokemon_lst_name)

    if st.button("Afficher les informations"):
        headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
        response = requests.get(f"{API_URL_POKEMON}/{selected_pokemon.lower()}",headers=headers)

        if response.status_code == 200:
            data = response.json()
            st.subheader(f"⭐ {data['name'].capitalize()} ⭐")
            st.image(data["image"], caption=f"{data['name'].capitalize()}")
            st.write(f"**Taille :** {data['height']} dm")
            st.write(f"**Poids :** {data['weight']} hg")
            
            # ✅ Affichage des types avec icônes
            st.write("**Type(s) du Pokémon :**")
            cols = st.columns(len(data["types"]))  # ✅ Une colonne par type
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
                        st.write(f"❌ Impossible de récupérer {pokemon_name.capitalize()}")


        else:
            st.error("Pokémon non trouvé. 😢")


####Partie Recherche Ability####
elif page == "⚡ Ability":
    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
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
                    pokemon_response = requests.get(f"{API_URL_POKEMON}/{pokemon.lower()}",headers=headers)
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


#### Liste Pokémon paginée ####
elif page == "📜 Liste Pokémon":
    st.header("📜 Liste des Pokémon avec pagination")

    # Sélection du nombre de Pokémon par page
    per_page = st.slider("Nombre de Pokémon par page", min_value=1, max_value=25, value=10, step=1)

    # Numéro de page stocké dans la session
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = 1


    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
    response = requests.get(f"{API_URL_POKEMON}/pokemon_name_list_pagine/{per_page}", headers=headers)

    if response.status_code == 200:
        paginated_pokemon_names = response.json()
        total_pages = len(paginated_pokemon_names)

        current_page_key = str(st.session_state["current_page"])  
        if current_page_key in paginated_pokemon_names:
            pokemon_names_on_page = paginated_pokemon_names[current_page_key]

            pokemon_details = []
            for pokemon_name in pokemon_names_on_page:
                detail_response = requests.get(f"{API_URL_POKEMON}/{pokemon_name}", headers=headers)
                if detail_response.status_code == 200:
                    pokemon_details.append(detail_response.json())

            st.subheader(f"📄 Page {st.session_state['current_page']} / {total_pages}")

            for pokemon in pokemon_details:
                st.subheader(f"⭐ {pokemon['name'].capitalize()}")
                st.image(pokemon["image"], width=100)
                st.write(f"**Taille :** {pokemon['height']} dm")
                st.write(f"**Poids :** {pokemon['weight']} hg")
                st.write(f"**Type(s) :** {', '.join(pokemon['types'])}")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.session_state["current_page"] > 1:
                if st.button("⬅️ Page précédente"):
                    st.session_state["current_page"] -= 1
                    st.rerun()
        with col3:
            if st.session_state["current_page"] < total_pages:
                if st.button("➡️ Page suivante"):
                    st.session_state["current_page"] += 1
                    st.rerun()

    else:
        st.error("Impossible de récupérer la liste des Pokémon.")


#### pokedle #####



