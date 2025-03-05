# Pokédex API + Interface Streamlit

🚀 Ce projet permet d'afficher un Pokédex interactif avec **Flask** pour l'API et **Streamlit** pour l'interface utilisateur.

## 📦 Installation

### 1️⃣ Cloner le projet :
```bash
git clone https://github.com/LucasCunin/pokedex.git
cd pokedex
```

### 2️⃣ Installation des dépendances :
```bash
make env
```

### 3️⃣ Lancer l'application :
```bash
make run
```

## ⚠️ Remarque importante

Si vous changez de session ou redémarrez votre terminal, vous devez réactiver l'environnement virtuel et réexporter les variables d'environnement :

```bash
source .pokenv/bin/activate
export API_URL_POKEMON="http://127.0.0.1:5000/api/pokemon"
export API_URL_ABILITY="http://127.0.0.1:5000/api/ability"
export API_URL_AUTH="http://127.0.0.1:5000/api/auth"
```

## 🛠️ Nettoyage
Si besoin, vous pouvez nettoyer l'environnement et supprimer les fichiers temporaires :
```bash
make clean
```

## 📂 Structure du projet
```
/mon_projet/
│──  app
│   ├── __init__.py
│   ├── model
│   │   └── user.py
│   ├── routes
│   │   ├── ability_route.py
│   │   ├── auth_routes.py
│   │   └── pokemon_routes.py
│   ├── service
│   │   ├── ability_service.py
│   │   └── pokemon_service.py
│── front/
│   ├── auth_front.py
│   ├── pokemon_front.py
│   ├── ability_front.py
│   ├── pokedle_front.py
│── main.py
│── requirements.txt
│── Makefile
│── README.md
```

