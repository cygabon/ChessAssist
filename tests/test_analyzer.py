"""
Tests pour le module d'analyse
"""

import unittest
from unittest.mock import patch, MagicMock
from chessassist.core.analyzer import GameAnalyzer, MoveAnalysis

class TestGameAnalyzer(unittest.TestCase):
    """Tests pour GameAnalyzer"""
    
    def setUp(self):
        """Préparation des tests"""
        self.test_pgn = '''
[Event "Test Game"]
[Site "chess.com"]
[Date "2023.01.01"]
[White "Player1"]
[Black "Player2"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 1-0
'''
    
    @patch('chessassist.core.analyzer.chess.engine.SimpleEngine.popen_uci')
    def test_analyzer_initialization(self, mock_engine):
        """Test d'initialisation de l'analyseur"""
        mock_engine.return_value = MagicMock()
        
        with GameAnalyzer("fake_stockfish_path") as analyzer:
            self.assertIsNotNone(analyzer.engine)
    
    def test_classify_move(self):
        """Test de classification des coups"""
        analyzer = GameAnalyzer.__new__(GameAnalyzer)
        
        # Test des différentes classifications
        self.assertEqual(analyzer._classify_move(100), "excellent")
        self.assertEqual(analyzer._classify_move(90), "good")
        self.assertEqual(analyzer._classify_move(75), "inaccuracy")
        self.assertEqual(analyzer._classify_move(55), "mistake")
        self.assertEqual(analyzer._classify_move(20), "blunder")
    
    def test_calculate_accuracy(self):
        """Test du calcul de précision"""
        analyzer = GameAnalyzer.__new__(GameAnalyzer)
        
        # Coup parfait (pas de perte d'évaluation)
        accuracy = analyzer._calculate_accuracy(1.0, 1.0, True)
        self.assertEqual(accuracy, 100.0)
        
        # Petite perte d'évaluation
        accuracy = analyzer._calculate_accuracy(1.0, 0.95, True)
        self.assertEqual(accuracy, 95.0)
        
        # Grosse erreur
        accuracy = analyzer._calculate_accuracy(1.0, -0.5, True)
        self.assertEqual(accuracy, 25.0)

if __name__ == '__main__':
    unittest.main()