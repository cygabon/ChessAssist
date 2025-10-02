#!/usr/bin/env python3
"""
Exemple d'utilisation de ChessAssist
"""

from chessassist.core.analyzer import GameAnalyzer
from chessassist.openings.recommender import OpeningRecommender, Color, Difficulty
from chessassist.chess_com.api import ChessComAPI
from chessassist.utils.config import config_manager
from rich.console import Console
from rich.table import Table

console = Console()

def example_opening_recommendations():
    """Exemple de recommandations d'ouvertures"""
    console.print("\n[bold blue]🚀 Recommandations d'ouvertures[/bold blue]")
    
    recommender = OpeningRecommender()
    
    # Recommandations pour les blancs (niveau débutant)
    white_openings = recommender.get_recommendations(
        Color.WHITE, 
        Difficulty.BEGINNER,
        count=3
    )
    
    table = Table(title="Ouvertures recommandées pour les Blancs (Débutant)")
    table.add_column("Ouverture", style="cyan")
    table.add_column("ECO", style="yellow")
    table.add_column("Coups", style="green")
    table.add_column("Succès", style="magenta")
    
    for opening in white_openings:
        table.add_row(
            opening.name,
            opening.eco_code,
            opening.moves[:20] + "..." if len(opening.moves) > 20 else opening.moves,
            f"{opening.success_rate:.0%}"
        )
    
    console.print(table)
    
    # Recommandations pour les noirs (niveau intermédiaire)
    black_openings = recommender.get_recommendations(
        Color.BLACK,
        Difficulty.INTERMEDIATE,
        count=3
    )
    
    table_black = Table(title="Ouvertures recommandées pour les Noirs (Intermédiaire)")
    table_black.add_column("Ouverture", style="cyan")
    table_black.add_column("ECO", style="yellow")
    table_black.add_column("Coups", style="green")
    table_black.add_column("Succès", style="magenta")
    
    for opening in black_openings:
        table_black.add_row(
            opening.name,
            opening.eco_code,
            opening.moves[:20] + "..." if len(opening.moves) > 20 else opening.moves,
            f"{opening.success_rate:.0%}"
        )
    
    console.print(table_black)

def example_chess_com_integration():
    """Exemple d'intégration chess.com"""
    console.print("\n[bold green]♟️ Intégration Chess.com[/bold green]")
    
    # Note: nécessite un nom d'utilisateur valide
    api = ChessComAPI()
    
    console.print("Pour utiliser cette fonctionnalité:")
    console.print("1. Configurez votre nom d'utilisateur chess.com dans .env")
    console.print("2. Exécutez: python -m chessassist analyze-last-game --username votre_nom")
    
    # Exemple d'analyse de répertoire
    example_repertoire = {
        "Défense sicilienne": 25,
        "Défense française": 12,
        "Ouverture italienne": 18,
        "Partie espagnole": 8
    }
    
    recommender = OpeningRecommender()
    analysis = recommender.analyze_opening_repertoire(example_repertoire)
    
    console.print(f"\n[bold]Score de diversité:[/bold] {analysis['diversity_score']:.2f}")
    console.print(f"[bold]Ouvertures principales:[/bold] {len(analysis['main_openings'])}")

def example_game_analysis():
    """Exemple d'analyse de partie"""
    console.print("\n[bold red]🔍 Analyse de partie[/bold red]")
    
    sample_pgn = '''[Event "Exemple"]
[Site "ChessAssist"]
[Date "2023.10.03"]
[White "Joueur1"]
[Black "Joueur2"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 1-0'''
    
    console.print("[yellow]Note:[/yellow] L'analyse nécessite Stockfish installé")
    console.print("Installation Ubuntu/Debian: [code]sudo apt install stockfish[/code]")
    console.print("Installation macOS: [code]brew install stockfish[/code]")
    
    # Simulation d'analyse sans Stockfish
    console.print("\n[bold]Résultats d'analyse simulés:[/bold]")
    
    results_table = Table(title="Analyse des coups")
    results_table.add_column("Coup", style="cyan")
    results_table.add_column("Évaluation", style="green")
    results_table.add_column("Classification", style="yellow")
    results_table.add_column("Précision", style="magenta")
    
    results_table.add_row("1. e4", "+0.2", "Excellent", "100%")
    results_table.add_row("1... e5", "+0.2", "Excellent", "98%")
    results_table.add_row("2. Nf3", "+0.3", "Excellent", "100%")
    results_table.add_row("5... Be7", "+0.4", "Bon", "92%")
    
    console.print(results_table)

def main():
    """Fonction principale d'exemple"""
    console.print("[bold magenta]ChessAssist - Exemples d'utilisation[/bold magenta]")
    console.print("=" * 50)
    
    # Vérification de la configuration
    if not config_manager.validate_config():
        console.print("\n[yellow]Configuration incomplète détectée.[/yellow]")
        console.print("Exécutez [code]python -c 'from chessassist.utils.config import config_manager; config_manager.setup_interactive()'[/code]")
    
    # Exemples
    example_opening_recommendations()
    example_chess_com_integration()
    example_game_analysis()
    
    console.print("\n[bold green]✅ Exemples terminés![/bold green]")
    console.print("\nPour commencer:")
    console.print("• [code]python -m chessassist --help[/code] - Aide générale")
    console.print("• [code]python -m chessassist openings --color white[/code] - Recommandations d'ouvertures")
    console.print("• [code]python -m chessassist stats --username votre_nom[/code] - Statistiques")

if __name__ == "__main__":
    main()