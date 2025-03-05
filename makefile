PROJECT_NAME=pokedex
VENV=.pokenv
ACTIVATE=$(VENV)/bin/activate

# Création de l'environnement virtuel et installation des dépendances
env:
	@echo "🚀 Création de l'environnement virtuel..."
	python3 -m venv $(VENV)
	@echo "📦 Téléchargement des dépendances..."
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

	@echo "🌍 Création et export des variables d'environnement..."
	export API_URL_POKEMON="http://127.0.0.1:5000/api/pokemon"
	export API_URL_ABILITY="http://127.0.0.1:5000/api/ability"
	export API_URL_AUTH="http://127.0.0.1:5000/api/auth"

# Lancement du back-end Flask
run_back:
	@echo "🚀 Lancement du back..."
	$(VENV)/bin/python app.py &

# Lancement du front-end Streamlit
run_front:
	@echo "🚀 Lancement du front..."
	$(VENV)/bin/streamlit run main.py &

# Lancement global (Back + Front)
run:
	@echo "🚀 Lancement complet de l'application..."
	make run_back
	make run_front

# Nettoyage des fichiers inutiles
clean:
	@echo "🧹 Suppression des fichiers temporaires..."
	rm -rf $(VENV) __pycache__ instance/*.db *.log
	@echo "✅ Nettoyage terminé."
