# SEMJUST - API d'Optimisation Équitable de la Distribution des Semences au Sénégal

## Description
SEMJUST est une API sophistiquée d'allocation équitable des semences agricoles entre les 14 régions et 45 départements du Sénégal. Le système intègre une visualisation cartographique interactive et utilise un algorithme d'optimisation multi-paramétrique pour analyser les facteurs agro-écologiques, démographiques et historiques.

## Fonctionnalités Principales
- Optimisation multi-paramétrique de la distribution des semences
- Visualisation cartographique interactive
- Analyse des facteurs d'influence
- Simulation de scénarios en temps réel
- Suivi des allocations historiques
- Exportation de rapports détaillés

## Prérequis
- Python 3.11+
- PostgreSQL 15+ avec PostGIS 3.3+
- Redis 7.0+
- Docker et Docker Compose

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/votre-organisation/semjust.git
cd semjust
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement :
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

5. Initialiser la base de données :
```bash
alembic upgrade head
```

## Démarrage

1. Lancer l'API en mode développement :
```bash
uvicorn app.main:app --reload
```

2. Lancer avec Docker Compose :
```bash
docker-compose up -d
```

## Documentation API
La documentation interactive de l'API est disponible aux endpoints suivants :
- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`

## Structure du Projet
```
semjust/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   └── deps.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   └── session.py
│   ├── models/
│   ├── schemas/
│   └── services/
├── tests/
├── alembic/
├── .env.example
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Tests
```bash
pytest
```

## Contribution
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.