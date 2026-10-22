# Industrial Health Monitor AI - Backend

## Présentation
Backend Django REST pour la supervision technique et l'évaluation de santé de composants informatiques (données simulées).

## Fonctionnalités
- Gestion des composants, métriques, contrôles de santé, alertes, diagnostics, rapports.
- Moteur de règles déterministe (CPU, mémoire, disponibilité, latence).
- Collecteur simulé.
- Intégration LLM isolée (ne modifie jamais le statut officiel).

## Architecture
Voir structure ackend/monitoring/.

## Prérequis
- Python 3.10+
- MySQL/MariaDB (WAMP) en marche
- Environnement virtuel

## Installation (PowerShell)
`powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
`

## Configuration MySQL
Créer la base industrial_health_monitor (utf8mb4).

## Variables d'environnement
Copier .env.example vers ackend/.env et remplir.

## Migrations
`powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo_data
`

## Démarrage
`powershell
python manage.py runserver
`

## Tests
`powershell
python -m pytest -q
`

## Qualité
`powershell
ruff check .
bandit -r .
`

## API
Préfixe /api/v1/. Docs : /api/docs/, schéma : /api/schema/.

## Sécurité
- Secrets via env, DEBUG configurable, ALLOWED_HOSTS, CORS restrictif.
- Auth par session, permissions côté serveur.
- LLM clé uniquement côté serveur.

## Limites
- Données simulées uniquement.
- LLM placeholder HTTP.
- Pas de rôles granulaires encore.
