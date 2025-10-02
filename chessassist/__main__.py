#!/usr/bin/env python3
"""
Point d'entrée principal pour ChessAssist CLI
"""

import click
from rich.console import Console
from rich.panel import Panel
from chessassist.cli.commands import analyze, openings, stats

console = Console()

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """ChessAssist - Votre assistant pour progresser aux échecs sur chess.com"""
    console.print(Panel(
        "[bold blue]ChessAssist[/bold blue]\n"
        "Assistant intelligent pour améliorer votre jeu d'échecs",
        title="♟️ Bienvenue",
        border_style="blue"
    ))

# Ajouter les commandes
cli.add_command(analyze)
cli.add_command(openings) 
cli.add_command(stats)

if __name__ == "__main__":
    cli()