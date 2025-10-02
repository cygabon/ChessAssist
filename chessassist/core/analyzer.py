"""
Analyseur de parties d'échecs utilisant Stockfish
"""

import chess
import chess.engine
import chess.pgn
from typing import List, Dict, Optional, Tuple
import os
from dataclasses import dataclass

@dataclass
class MoveAnalysis:
    """Résultat d'analyse d'un coup"""
    move: str
    evaluation: float
    best_move: str
    accuracy: float
    classification: str  # "excellent", "good", "inaccuracy", "mistake", "blunder"

class GameAnalyzer:
    """Analyseur de parties d'échecs"""
    
    def __init__(self, stockfish_path: Optional[str] = None):
        """
        Initialise l'analyseur
        
        Args:
            stockfish_path: Chemin vers l'exécutable Stockfish
        """
        self.stockfish_path = stockfish_path or self._find_stockfish()
        self.engine = None
    
    def _find_stockfish(self) -> str:
        """Trouve automatiquement le chemin vers Stockfish"""
        common_paths = [
            "/usr/local/bin/stockfish",
            "/usr/bin/stockfish",
            "/opt/homebrew/bin/stockfish",
            "stockfish"
        ]
        
        for path in common_paths:
            if os.path.exists(path) or os.system(f"which {path} > /dev/null 2>&1") == 0:
                return path
        
        raise FileNotFoundError("Stockfish introuvable. Installez-le ou spécifiez le chemin.")
    
    def __enter__(self):
        """Démarre le moteur Stockfish"""
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
            return self
        except Exception as e:
            raise RuntimeError(f"Impossible de démarrer Stockfish: {e}")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ferme le moteur Stockfish"""
        if self.engine:
            self.engine.quit()
    
    def analyze_position(self, board: chess.Board, time_limit: float = 1.0) -> Dict:
        """
        Analyse une position donnée
        
        Args:
            board: Position à analyser
            time_limit: Temps d'analyse en secondes
            
        Returns:
            Dictionnaire contenant l'évaluation et le meilleur coup
        """
        if not self.engine:
            raise RuntimeError("Moteur Stockfish non initialisé")
        
        try:
            info = self.engine.analyse(board, chess.engine.Limit(time=time_limit))
            
            evaluation = info.get("score", chess.engine.Cp(0))
            if evaluation.is_mate():
                eval_value = float('inf') if evaluation.mate() > 0 else float('-inf')
            else:
                eval_value = evaluation.relative.cp / 100.0 if evaluation.relative.cp else 0.0
            
            best_move = info.get("pv", [None])[0]
            
            return {
                "evaluation": eval_value,
                "best_move": str(best_move) if best_move else None,
                "depth": info.get("depth", 0),
                "nodes": info.get("nodes", 0)
            }
        except Exception as e:
            return {
                "evaluation": 0.0,
                "best_move": None,
                "error": str(e)
            }
    
    def analyze_game(self, pgn_text: str, time_per_move: float = 1.0) -> List[MoveAnalysis]:
        """
        Analyse complète d'une partie
        
        Args:
            pgn_text: Partie au format PGN
            time_per_move: Temps d'analyse par coup en secondes
            
        Returns:
            Liste des analyses de chaque coup
        """
        game = chess.pgn.read_game(chess.pgn.StringIO(pgn_text))
        if not game:
            raise ValueError("Format PGN invalide")
        
        board = game.board()
        analyses = []
        
        for move_num, move in enumerate(game.mainline_moves()):
            # Analyse avant le coup
            position_before = self.analyze_position(board, time_per_move)
            
            # Joue le coup
            board.push(move)
            
            # Analyse après le coup
            position_after = self.analyze_position(board, time_per_move)
            
            # Calcule la précision du coup
            accuracy = self._calculate_accuracy(
                position_before.get("evaluation", 0),
                position_after.get("evaluation", 0),
                board.turn  # Couleur qui vient de jouer
            )
            
            classification = self._classify_move(accuracy)
            
            analysis = MoveAnalysis(
                move=str(move),
                evaluation=position_after.get("evaluation", 0),
                best_move=position_before.get("best_move", ""),
                accuracy=accuracy,
                classification=classification
            )
            
            analyses.append(analysis)
        
        return analyses
    
    def _calculate_accuracy(self, eval_before: float, eval_after: float, turn: bool) -> float:
        """
        Calcule la précision d'un coup
        
        Args:
            eval_before: Évaluation avant le coup
            eval_after: Évaluation après le coup
            turn: True si c'est aux blancs de jouer
            
        Returns:
            Précision entre 0 et 100
        """
        # Ajuste l'évaluation selon la couleur
        if not turn:  # Si c'est aux noirs
            eval_before = -eval_before
            eval_after = -eval_after
        
        # Calcule la perte d'évaluation
        eval_loss = eval_before - eval_after
        
        # Convertit en pourcentage de précision
        if eval_loss <= 0:
            return 100.0  # Coup parfait ou meilleur que prévu
        elif eval_loss <= 0.1:
            return 95.0   # Excellent
        elif eval_loss <= 0.3:
            return 85.0   # Bon
        elif eval_loss <= 0.6:
            return 70.0   # Imprécision
        elif eval_loss <= 1.0:
            return 50.0   # Erreur
        else:
            return 25.0   # Gaffe
    
    def _classify_move(self, accuracy: float) -> str:
        """Classifie un coup selon sa précision"""
        if accuracy >= 95:
            return "excellent"
        elif accuracy >= 85:
            return "good"
        elif accuracy >= 70:
            return "inaccuracy"
        elif accuracy >= 50:
            return "mistake"
        else:
            return "blunder"