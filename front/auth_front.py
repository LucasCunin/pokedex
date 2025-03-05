import streamlit as st
import requests
import os

API_URL_AUTH = os.getenv("API_URL_AUTH")

def login():
    """Affichage du formulaire de connexion"""
    st.sidebar.subheader("🔑 Connexion")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Mot de passe", type="password")
    
    if st.sidebar.button("Se connecter"):
        response = requests.post(f"{API_URL_AUTH}/login", json={"email": email, "password": password})
        if response.status_code == 200:
            st.session_state["access_token"] = response.json()["access_token"]
            st.sidebar.success("✅ Connexion réussie")
            st.rerun()
        else:
            st.sidebar.error("❌ Identifiants incorrects")

def logout():
    """Déconnexion de l'utilisateur"""
    st.session_state["access_token"] = None
    st.sidebar.warning("Déconnecté")
