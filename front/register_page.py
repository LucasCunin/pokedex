import streamlit as st
import requests
import os

API_URL_AUTH = os.getenv("API_URL_AUTH")

def register_page():
    """Affichage du formulaire d'inscription"""
    st.header("📝 Inscription")
    
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Mot de passe", type="password", key="register_password")
    confirm_password = st.text_input("Confirmer le mot de passe", type="password", key="register_confirm_password")
    
    if st.button("S'inscrire", key="register_button"):
        if not email or not password or not confirm_password:
            st.error("❌ Tous les champs sont requis !")
            return
        
        if password != confirm_password:
            st.error("❌ Les mots de passe ne correspondent pas !")
            return
        
        response = requests.post(f"{API_URL_AUTH}/register", json={"email": email, "password": password})
        
        if response.status_code == 201:
            st.success("✅ Inscription réussie ! Vous pouvez maintenant vous connecter.")
        elif response.status_code == 400:
            st.error("❌ Cet utilisateur existe déjà.")
        else:
            st.error("❌ Une erreur est survenue. Veuillez réessayer.")
