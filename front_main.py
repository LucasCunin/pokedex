import streamlit as st
from front.auth_front import login, logout
from front.pokemon_front import pokemon_page
from front.ability_front import ability_page
from front.pokedle_front import game_page

# Chargement du Token dans la session
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

# Barre latérale
st.sidebar.title("🔐 Connexion")
if st.session_state["access_token"]:
    st.sidebar.success("✅ Connecté")
    if st.sidebar.button("Se déconnecter"):
        logout()
        st.rerun()
else:
    login()

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisissez une recherche :", ["🔍 Pokémon", "⚡ Ability", "🎮 Pokédle"])

# Chargement des pages correspondantes
if page == "🔍 Pokémon":
    pokemon_page()
elif page == "⚡ Ability":
    ability_page()
elif page == "🎮 Pokédle":
    game_page()
