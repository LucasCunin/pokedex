PROJECT_NAME=pokedex
VENV=.venv
ACTIVATE=$(VENV)/bin/activate

# Création du fichier `.env`
env:
	@echo "📄 Création du fichier .env..."
	@if [ ! -f .env ]; then \
		echo "API_URL_POKEMON=http://127.0.0.1:5000/api/pokemon" > .env; \
		echo "API_URL_ABILITY=http://127.0.0.1:5000/api/ability" >> .env; \
		echo "API_URL_AUTH=http://127.0.0.1:5000/api/auth" >> .env; \
		echo "JWT_SECRET_KEY=super-secret-key" >> .env; \
		echo "✅ Fichier .env généré."; \
		set -a && source .env && set +a
	else \
		echo ".env existe déjà, pas de modification."; \
	fi


# Installation des dépendances
install:
	@echo "🚀 Création de l'environnement virtuel..."
	python3 -m venv $(VENV)
	@echo "📦 Installation des dépendances..."
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt
	@echo "✅ Installation terminée !"

# Lancement de l'API Flask et de Streamlit
run:
	@echo "🚀 Lancement de l'application..."
	@source $(ACTIVATE) && flask run & streamlit run interface.py

# Nettoyage des fichiers inutiles
clean:
	@echo "🧹 Suppression des fichiers temporaires..."
	rm -rf $(VENV) __pycache__ instance/*.db *.log
	@echo "✅ Nettoyage terminé."


