import streamlit as st
import requests
import os
import random

API_URL_POKEMON = os.getenv("API_URL_POKEMON")

def game_page():
    """Affichage du jeu Pokédle"""
    st.header("🎮 Pokédle - Devinez le Pokémon !")

    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}

    if "pokemon_list" not in st.session_state:
        all_pokemon_response = requests.get(f"{API_URL_POKEMON}/list_name", headers=headers)
        if all_pokemon_response.status_code == 200:
            all_pokemon = all_pokemon_response.json()
            all_pokemon = [pokemon for pokemon in all_pokemon if " " not in pokemon or "-" not in pokemon]  # Exclure les Pokémon avec espaces
            st.session_state["pokemon_list"] = all_pokemon
        else:
            st.error("Impossible de récupérer la liste des Pokémon.")
            st.stop()


    if "random_pokemon" not in st.session_state:
        st.session_state["random_pokemon"] = random.choice(st.session_state["pokemon_list"])
        st.session_state["guesses"] = []  # Stocke les tentatives précédentes

    # Récupérer les informations du Pokémon secret
    random_pokemon_name = st.session_state["random_pokemon"]
    response = requests.get(f"{API_URL_POKEMON}/{random_pokemon_name.lower()}", headers=headers)

    if response.status_code == 200:
        secret_pokemon = response.json()  # Stocke les informations du Pokémon secret

        # Sélection du Pokémon à deviner
        guess = st.selectbox("Recherchez un Pokémon :", st.session_state["pokemon_list"])

        if st.button("Valider"):
            guess_response = requests.get(f"{API_URL_POKEMON}/{guess.lower()}", headers=headers)
            if guess_response.status_code == 200:
                guessed_pokemon = guess_response.json()  # Récupération des infos du Pokémon deviné
                
                # Ajouter cette tentative à la liste des essais précédents
                st.session_state["guesses"].append(guessed_pokemon)

            else:
                st.error("❌ Pokémon non trouvé. Essayez encore !")

        # Fonction pour colorer les cases
        def colorize(value, correct_value):
            """Détermine la couleur de la case (Vert = correct, Jaune = partiellement, Rouge = incorrect)."""
            if value == correct_value:
                return "✅"
            elif value in correct_value if isinstance(correct_value, list) else []:
                return "🟡"  
            else:
                return "❌"  

        # Fonction pour indiquer si c'est plus haut ou plus bas
        def higher_or_lower(value, correct_value):
            if value < correct_value:
                return "⬆️ Plus haut"
            elif value > correct_value:
                return "⬇️ Plus bas"
            return "✅"

        # Affichage des tentatives précédentes
        if st.session_state["guesses"]:
            st.write("### Vos tentatives :")
            for guessed_pokemon in st.session_state["guesses"]:
                cols = st.columns(8)

                with cols[0]:
                    st.image(guessed_pokemon["image"], width=100)
                    st.write(guessed_pokemon["name"].capitalize())

                with cols[1]:
                    st.write(f"{colorize(guessed_pokemon['types'][0], secret_pokemon['types'])} Type 1 : {guessed_pokemon['types'][0].capitalize()}")

                with cols[2]:
                    type2 = guessed_pokemon["types"][1] if len(guessed_pokemon["types"]) > 1 else "Aucun"
                    st.write(f"{colorize(type2, secret_pokemon['types'])} Type 2 : {type2.capitalize()}")

                with cols[3]:
                    st.write(f"{colorize(guessed_pokemon['color'], secret_pokemon['color'])} Couleur : {guessed_pokemon['color'].capitalize()}")

                with cols[4]:
                    st.write(f"{higher_or_lower(guessed_pokemon['height'], secret_pokemon['height'])} Hauteur : {guessed_pokemon['height']}m")

                with cols[5]:
                    st.write(f"{higher_or_lower(guessed_pokemon['weight'], secret_pokemon['weight'])} Poids : {guessed_pokemon['weight']}kg")

                with cols[6]:
                    st.write(f"{higher_or_lower(guessed_pokemon['generation'], secret_pokemon['generation'])} Génération : {guessed_pokemon['generation']}")

                with cols[7]:
                    if guessed_pokemon["name"] == secret_pokemon["name"]:
                        st.success("🎉 Bravo ! Vous avez trouvé le bon Pokémon ! 🎉")
                        if st.button("Rejouer"):
                            st.session_state["random_pokemon"] = random.choice(st.session_state["pokemon_list"])
                            st.session_state["guesses"] = []
                            st.rerun()