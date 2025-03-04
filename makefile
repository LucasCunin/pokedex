PROJECT_NAME=pokedex
VENV=.env
ACTIVATE=$(VENV)/bin/activate

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


