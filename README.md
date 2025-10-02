# ChessAssist

Un assistant intelligent pour aider à progresser.

## Fonctionnalités

- 🔍 **Analyse de parties** : Analysez vos parties avec Stockfish
- 📊 **Évaluation de positions** : Obtenez des évaluations précises de positions
- 📖 **Recommandations d'ouvertures** : Suggestions d'ouvertures basées sur votre style
- 📈 **Statistiques de progression** : Suivez vos progrès au fil du temps
- 🎯 **Détection d'erreurs** : Identifiez et corrigez vos erreurs typiques

## Installation

1. Clonez ce repository
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Configurez votre environnement (voir Configuration)

## Configuration


## Utilisation

```bash
# Analyser une partie récente
python -m chessassist analyze-last-game

# Obtenir des recommandations d'ouvertures
python -m chessassist openings --color white

# Voir vos statistiques
python -m chessassist stats
```

## Structure du projet

```
chessassist/
├── core/           # Logique métier principale
├── analysis/       # Modules d'analyse des parties
├── openings/       # Système de recommandations d'ouvertures
├── chess_com/      # Interface avec chess.com API
├── cli/           # Interface en ligne de commande
└── utils/         # Utilitaires
```

## Développement

Ce projet utilise Python 3.8+ et les bibliothèques suivantes :
- `python-chess` pour la manipulation des parties
- `stockfish` pour l'analyse de positions
- `requests` pour l'API chess.com
- `click` pour l'interface CLI
- `rich` pour l'affichage enrichi
