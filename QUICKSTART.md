# Guide de démarrage rapide - ChessAssist

## 🚀 Installation et lancement

ChessAssist est maintenant installé et prêt à l'emploi !

### Commandes disponibles

```bash
# Aide générale
python -m chessassist --help

# Recommandations d'ouvertures
python -m chessassist openings --color white
python -m chessassist openings --color black  
python -m chessassist openings --color both --level beginner

# Statistiques (nécessite un nom d'utilisateur chess.com)
python -m chessassist stats --username votre_nom

# Analyse de parties (nécessite Stockfish)
python -m chessassist analyze --username votre_nom
```

### Configuration recommandée

1. **Installer Stockfish** (pour l'analyse de parties) :
   ```bash
   # Ubuntu/Debian
   sudo apt install stockfish
   
   # macOS
   brew install stockfish
   
   # Windows
   # Télécharger depuis https://stockfishchess.org/download/
   ```

2. **Configurer votre profil** (optionnel) :
   ```bash
   # Copier le fichier d'exemple
   cp .env.example .env
   
   # Éditer avec votre nom d'utilisateur chess.com
   # CHESS_COM_USERNAME=votre_nom_utilisateur
   ```

### Exemples d'utilisation

```bash
# Démo complète
python examples/demo.py

# Recommandations pour débuter
python -m chessassist openings --color white --level beginner

# Voir les statistiques de progression
python -m chessassist stats --period month
```

### Fonctionnalités disponibles

✅ **Recommandations d'ouvertures**
- Base de données d'ouvertures intégrée
- Filtrage par couleur et niveau
- Conseils stratégiques pour chaque ouverture

✅ **Interface CLI interactive**
- Affichage enrichi avec Rich
- Tableaux formatés et couleurs
- Messages d'aide détaillés

🔄 **Analyse de parties** (nécessite Stockfish)
- Évaluation précise des positions
- Détection des erreurs et imprécisions
- Calcul de la précision globale

🔄 **Intégration chess.com** (nécessite configuration)
- Récupération automatique des parties
- Analyse du répertoire d'ouvertures
- Suivi des statistiques de progression

### Structure du projet

```
chessassist/
├── core/           # Analyseur Stockfish et logique métier
├── cli/            # Interface en ligne de commande
├── chess_com/      # Intégration API chess.com
├── openings/       # Système de recommandations
├── utils/          # Configuration et utilitaires
└── tests/          # Tests unitaires
```

### Développement

Pour contribuer au projet :

```bash
# Tests
python -m pytest tests/

# Linting (si installé)
flake8 chessassist/
black chessassist/

# Installation en mode développement (déjà fait)
pip install -e .
```

### Aide et support

- 📖 Documentation complète : `README.md`
- 🐛 Problèmes : Vérifiez les prérequis (Python 3.8+, Stockfish)
- 🎯 Configuration : Utilisez le fichier `.env` pour personnaliser

**Bon jeu d'échecs ! ♟️**