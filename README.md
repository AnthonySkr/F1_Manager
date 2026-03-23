# F1 Manager 🏎️

Un jeu de gestion de Formule 1 en interface CLI Python. Gérez votre équipe, optimisez vos voitures, et pilotez votre écurie vers le championnat du monde.

## 📋 Table des matières

- [À propos](#-à-propos)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Initialisation](#-initialisation)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Tests](#-tests)
- [Développement](#-développement)
- [Architecture](#-architecture)

## 📖 À propos

F1 Manager est un simulateur de Formule 1 permettant de :
- Gérer une équipe de F1 avec des pilotes
- Optimiser les performances des voitures
- Simuler des courses sur différents circuits
- Gérer les upgrades et le budget de l'équipe

### Modèles principaux

- **Car** : Représente une voiture avec ses stats (downforce, aéro, châssis, puissance moteur, fiabilité, refroidissement des pneus)
- **Track** : Représente un circuit avec ses caractéristiques (type de piste, tours, dégradation des pneus, zones DRS)
- **Driver** : Pilote avec ses compétences (en développement)
- **Team** : Équipe de F1 avec ses ressources (en développement)

## 🔧 Prérequis

- **Python** : 3.13 ou supérieur
- **pip** : Gestionnaire de paquets Python
- **Git** : Pour la gestion de versions

Vérifiez votre version Python :
```bash
python --version
```

## 📦 Installation

### 1. Cloner le repository
```bash
git clone <votre-url-repo>
cd F1_Manager
```

### 2. Créer un environnement virtuel (recommandé)

**Sur Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

**Sur Mac/Linux :**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Installer le projet en mode développement

```bash
pip install taskipy
task install
```

Cela installe :
- Les dépendances de base
- Les dépendances de test (pytest, pytest-cov)
- Les outils de formatage (black, ruff, isort)
- Les outils de gestion de versions (commitizen, pre-commit)
- taskipy pour l'automatisation des tâches

## 🚀 Initialisation

### Vérifier l'installation
```bash
task run
```

Vous devriez voir les stats d'une voiture de test s'afficher :
```
downforce    : 90/100
aero_efficiency : 92/100
chassis      : 91/100
power_unit   : 89/100
reliability  : 90/100
tire_cooling : 92/100
overall      : 90/100
```

### Initialiser dans votre code

```python
from src.models import Car, Track, TrackType

# Créer une voiture
car = Car(90, 92, 91, 89, 90, 92)

# Créer un circuit
track = Track(
    name="Monaco",
    country="Monaco",
    city="Monte-Carlo",
    track_type=TrackType.STREET,
    laps=78,
    base_lap_time=74.5,
    pit_loss_time=25.0,
    overtaking_difficulty=10,
    tire_degradation=0.8,
    drs_zones=0
)

# Afficher les stats
print(car.get_stats_display())
print(track.get_info_display())
```

## 💻 Utilisation

### Lancer le jeu
```bash
python src/main.py
```

### Commandes utiles (avec taskipy)

| Commande | Description |
|----------|-------------|
| `task lint` | Vérifier le style du code |
| `task format` | Formater le code |
| `task test` | Lancer les tests |
| `task test-cov` | Tests avec couverture de code |
| `task commit` | Créer un commit interactif |

## 📁 Structure du projet

```
F1_Manager/
├── src/                          # Code source principal
│   ├── main.py                  # Point d'entrée du jeu
│   ├── __init__.py
│   └── models/                  # Modèles de données
│       ├── __init__.py
│       ├── car.py              # Modèle de voiture
│       ├── driver.py           # Modèle de pilote (WIP)
│       ├── team.py             # Modèle d'équipe (WIP)
│       └── track.py            # Modèle de circuit
├── tests/                       # Tests unitaires
│   ├── conftest.py             # Configuration pytest
│   ├── __init__.py
│   └── models/
│       ├── __init__.py
│       ├── test_car.py         # Tests pour Car
│       └── test_track.py       # Tests pour Track
├── pyproject.toml              # Configuration du projet (dépendances, tools)
├── README.md                   # Ce fichier
└── .pre-commit-config.yaml    # Configuration des hooks git
```

## 🧪 Tests

### Lancer tous les tests
```bash
pytest
```

### Lancer les tests avec couverture
```bash
pytest --cov=src --cov-report=html
```

### Tests d'un fichier spécifique
```bash
pytest tests/models/test_car.py -v
```

### Mode watch (relancer les tests automatiquement)
```bash
pytest-watch
```

## 🛠️ Développement

### Formatage et linting du code

**Formater le code (black + isort) :**
```bash
black src/ tests/
isort src/ tests/
```

**Vérifier les lint errors (ruff) :**
```bash
ruff check src/ tests/
```

**Tout en une commande :**
```bash
black src/ tests/ && isort src/ tests/ && ruff check src/ tests/
```

### Conventionnel Commits

Utilisez commitizen pour les commits respectant le standard Conventional Commits :
```bash
cz commit
```

Options disponibles :
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage
- `refactor:` Refactorisation
- `test:` Ajout/modification de tests
- `chore:` Maintenance

### Ajouter une nouvelle dépendance

```bash
pip install <package-name>
# Puis ajouter dans pyproject.toml sous [project] dependencies
```

## 🏗️ Architecture

### Modèle Car
Les voitures ont 6 stats principales (0-100) :
- **Downforce** (18%) : Grip en courbe
- **Aero Efficiency** (18%) : Équilibre aéro
- **Chassis** (22%) : Maniabilité générale
- **Power Unit** (18%) : Puissance moteur
- **Reliability** (12%) : Fiabilité (réduit les abandons)
- **Tire Cooling** (12%) : Gestion thermique des pneus

### Modèle Track
Les circuits varient par type :
- **HIGH_DOWNFORCE** : Downforce crucial
- **POWER** : Puissance moteur cruciale
- **STREET** : Châssis crucial
- **BALANCED** : Équilibre général

## 📝 Prochaines étapes

- [ ] Implémenter le modèle Driver (compétences, expérience)
- [ ] Implémenter le modèle Team (budget, staff)
- [ ] Créer le moteur de simulation de course
- [ ] Interface utilisateur interactive
- [ ] Système de progression et de saison
- [ ] Gestion du budget et des upgrades
