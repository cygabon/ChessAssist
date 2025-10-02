"""
Tests pour les recommandations d'ouvertures
"""

import unittest
from chessassist.openings.recommender import OpeningRecommender, Color, Difficulty

class TestOpeningRecommender(unittest.TestCase):
    """Tests pour OpeningRecommender"""
    
    def setUp(self):
        """Préparation des tests"""
        self.recommender = OpeningRecommender()
    
    def test_get_recommendations_white(self):
        """Test des recommandations pour les blancs"""
        recommendations = self.recommender.get_recommendations(
            Color.WHITE, 
            Difficulty.BEGINNER,
            count=3
        )
        
        self.assertGreater(len(recommendations), 0)
        self.assertLessEqual(len(recommendations), 3)
        
        # Vérifie que toutes les recommandations sont pour les blancs
        for opening in recommendations:
            self.assertEqual(opening.color, Color.WHITE)
            self.assertLessEqual(opening.difficulty.value, Difficulty.BEGINNER.value)
    
    def test_get_recommendations_black(self):
        """Test des recommandations pour les noirs"""
        recommendations = self.recommender.get_recommendations(
            Color.BLACK,
            Difficulty.INTERMEDIATE
        )
        
        self.assertGreater(len(recommendations), 0)
        
        # Vérifie que toutes les recommandations sont pour les noirs
        for opening in recommendations:
            self.assertEqual(opening.color, Color.BLACK)
    
    def test_get_opening_details(self):
        """Test de récupération des détails d'ouverture"""
        # Test avec une ouverture existante
        opening = self.recommender.get_opening_details("C50")
        self.assertIsNotNone(opening)
        self.assertEqual(opening.eco_code, "C50")
        
        # Test avec un code inexistant
        opening = self.recommender.get_opening_details("Z99")
        self.assertIsNone(opening)
    
    def test_analyze_opening_repertoire(self):
        """Test d'analyse du répertoire d'ouvertures"""
        played_openings = {
            "Défense sicilienne": 15,
            "Défense française": 8,
            "Défense italienne": 12
        }
        
        analysis = self.recommender.analyze_opening_repertoire(played_openings)
        
        self.assertIn("diversity_score", analysis)
        self.assertIn("main_openings", analysis)
        self.assertIn("recommendations", analysis)
        self.assertGreater(analysis["diversity_score"], 0)

if __name__ == '__main__':
    unittest.main()