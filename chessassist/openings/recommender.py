"""
Système de recommandations d'ouvertures d'échecs
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class Difficulty(Enum):
    """Niveaux de difficulté des ouvertures"""
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4

class Color(Enum):
    """Couleurs aux échecs"""
    WHITE = "white"
    BLACK = "black"

@dataclass
class Opening:
    """Représente une ouverture d'échecs"""
    name: str
    eco_code: str
    moves: str
    difficulty: Difficulty
    color: Color
    description: str
    success_rate: float
    popularity: int
    key_ideas: List[str]
    typical_plans: List[str]

class OpeningRecommender:
    """Système de recommandation d'ouvertures"""
    
    def __init__(self):
        """Initialise le système avec une base d'ouvertures"""
        self.openings = self._load_opening_database()
    
    def _load_opening_database(self) -> List[Opening]:
        """Charge la base de données des ouvertures"""
        return [
            # Ouvertures pour les blancs
            Opening(
                name="Défense italienne",
                eco_code="C50",
                moves="1.e4 e5 2.Nf3 Nc6 3.Bc4",
                difficulty=Difficulty.BEGINNER,
                color=Color.WHITE,
                description="Ouverture classique développant rapidement les pièces",
                success_rate=0.85,
                popularity=95,
                key_ideas=[
                    "Développement rapide",
                    "Contrôle du centre",
                    "Sécurité du roi"
                ],
                typical_plans=[
                    "Petit roque rapide",
                    "Attaque sur l'aile roi",
                    "Contrôle de la diagonale a2-g8"
                ]
            ),
            
            Opening(
                name="Ouverture anglaise",
                eco_code="A10",
                moves="1.c4",
                difficulty=Difficulty.INTERMEDIATE,
                color=Color.WHITE,
                description="Ouverture flexible contrôlant d5",
                success_rate=0.78,
                popularity=75,
                key_ideas=[
                    "Contrôle des cases centrales",
                    "Jeu positionnel",
                    "Flexibilité de structure"
                ],
                typical_plans=[
                    "Fianchetto du fou roi",
                    "Pression sur la colonne c",
                    "Jeu sur l'aile dame"
                ]
            ),
            
            Opening(
                name="Partie espagnole",
                eco_code="C60",
                moves="1.e4 e5 2.Nf3 Nc6 3.Bb5",
                difficulty=Difficulty.INTERMEDIATE,
                color=Color.WHITE,
                description="Ouverture classique avec pression sur le cavalier c6",
                success_rate=0.82,
                popularity=90,
                key_ideas=[
                    "Pression sur e5",
                    "Développement harmonieux",
                    "Plans à long terme"
                ],
                typical_plans=[
                    "Maintien de la tension centrale",
                    "Jeu sur l'aile roi",
                    "Avantage positionnel durable"
                ]
            ),
            
            Opening(
                name="Gambit du roi",
                eco_code="C30",
                moves="1.e4 e5 2.f4",
                difficulty=Difficulty.ADVANCED,
                color=Color.WHITE,
                description="Ouverture agressive sacrifiant un pion",
                success_rate=0.65,
                popularity=45,
                key_ideas=[
                    "Attaque rapide",
                    "Initiative",
                    "Sacrifice de matériel"
                ],
                typical_plans=[
                    "Attaque directe sur le roi",
                    "Ouverture des lignes",
                    "Jeu tactique complexe"
                ]
            ),
            
            # Ouvertures pour les noirs
            Opening(
                name="Défense sicilienne",
                eco_code="B20",
                moves="1.e4 c5",
                difficulty=Difficulty.INTERMEDIATE,
                color=Color.BLACK,
                description="Défense la plus populaire contre 1.e4",
                success_rate=0.82,
                popularity=98,
                key_ideas=[
                    "Contre-jeu actif",
                    "Déséquilibre positionnel",
                    "Chances de gain"
                ],
                typical_plans=[
                    "Pression sur la colonne c",
                    "Attaque sur l'aile dame",
                    "Contre-attaque centrale"
                ]
            ),
            
            Opening(
                name="Défense française",
                eco_code="C00",
                moves="1.e4 e6",
                difficulty=Difficulty.BEGINNER,
                color=Color.BLACK,
                description="Défense solide avec structure de pions caractéristique",
                success_rate=0.75,
                popularity=70,
                key_ideas=[
                    "Structure de pions solide",
                    "Jeu positionnel",
                    "Patience stratégique"
                ],
                typical_plans=[
                    "Percée avec f6 ou f5",
                    "Jeu sur l'aile dame",
                    "Échange du fou cases blanches"
                ]
            ),
            
            Opening(
                name="Défense Caro-Kann",
                eco_code="B10",
                moves="1.e4 c6",
                difficulty=Difficulty.INTERMEDIATE,
                color=Color.BLACK,
                description="Défense solide évitant les complications",
                success_rate=0.77,
                popularity=65,
                key_ideas=[
                    "Développement sûr",
                    "Structure équilibrée",
                    "Jeu sans faiblesse"
                ],
                typical_plans=[
                    "Égalisation tranquille",
                    "Jeu de pièces actif",
                    "Finales favorables"
                ]
            ),
            
            Opening(
                name="Défense nimzo-indienne",
                eco_code="E20",
                moves="1.d4 Nf6 2.c4 e6 3.Nc3 Bb4",
                difficulty=Difficulty.ADVANCED,
                color=Color.BLACK,
                description="Défense hypermoderne avec clouage du cavalier",
                success_rate=0.79,
                popularity=85,
                key_ideas=[
                    "Contrôle des cases blanches",
                    "Pression sur c3",
                    "Jeu hypermoderne"
                ],
                typical_plans=[
                    "Dommage à la structure adverse",
                    "Contrôle positionnel",
                    "Complexité stratégique"
                ]
            ),
            
            Opening(
                name="Défense slave",
                eco_code="D10",
                moves="1.d4 d5 2.c4 c6",
                difficulty=Difficulty.BEGINNER,
                color=Color.BLACK,
                description="Défense classique du gambit dame",
                success_rate=0.74,
                popularity=80,
                key_ideas=[
                    "Défense du pion d5",
                    "Développement naturel",
                    "Solidité"
                ],
                typical_plans=[
                    "Développement harmonieux",
                    "Égalisation confortable",
                    "Jeu de pièces équilibré"
                ]
            )
        ]
    
    def get_recommendations(
        self, 
        color: Color, 
        max_difficulty: Difficulty = Difficulty.INTERMEDIATE,
        min_success_rate: float = 0.70,
        count: int = 5
    ) -> List[Opening]:
        """
        Recommande des ouvertures selon les critères
        
        Args:
            color: Couleur pour laquelle recommander
            max_difficulty: Difficulté maximale acceptée
            min_success_rate: Taux de succès minimal
            count: Nombre de recommandations
            
        Returns:
            Liste des ouvertures recommandées
        """
        # Filtre selon les critères
        candidates = [
            opening for opening in self.openings
            if (opening.color == color and
                opening.difficulty.value <= max_difficulty.value and
                opening.success_rate >= min_success_rate)
        ]
        
        # Trie par popularité et taux de succès
        candidates.sort(
            key=lambda x: (x.popularity, x.success_rate), 
            reverse=True
        )
        
        return candidates[:count]
    
    def get_opening_details(self, eco_code: str) -> Opening:
        """
        Récupère les détails d'une ouverture par son code ECO
        
        Args:
            eco_code: Code ECO de l'ouverture
            
        Returns:
            Ouverture correspondante ou None
        """
        for opening in self.openings:
            if opening.eco_code == eco_code:
                return opening
        return None
    
    def analyze_opening_repertoire(self, played_openings: Dict[str, int]) -> Dict:
        """
        Analyse le répertoire d'ouvertures d'un joueur
        
        Args:
            played_openings: Dictionnaire {nom_ouverture: fréquence}
            
        Returns:
            Analyse du répertoire avec recommandations
        """
        total_games = sum(played_openings.values())
        
        analysis = {
            "diversity_score": len(played_openings) / max(total_games, 1),
            "main_openings": [],
            "gaps": [],
            "recommendations": []
        }
        
        # Ouvertures principales (>10% des parties)
        for opening_name, count in played_openings.items():
            percentage = count / total_games
            if percentage > 0.10:
                analysis["main_openings"].append({
                    "name": opening_name,
                    "frequency": percentage,
                    "games": count
                })
        
        # Détection des lacunes
        played_eco_codes = set()
        for opening_name in played_openings.keys():
            # Simplifié: recherche par nom
            for opening in self.openings:
                if opening.name.lower() in opening_name.lower():
                    played_eco_codes.add(opening.eco_code)
        
        # Recommandations pour combler les lacunes
        for color in [Color.WHITE, Color.BLACK]:
            color_openings = [o for o in self.openings if o.color == color]
            popular_openings = [
                o for o in color_openings 
                if o.popularity > 80 and o.eco_code not in played_eco_codes
            ]
            
            for opening in popular_openings[:2]:
                analysis["recommendations"].append({
                    "opening": opening.name,
                    "reason": f"Ouverture populaire manquante pour les {color.value}s",
                    "difficulty": opening.difficulty.name
                })
        
        return analysis
    
    def get_opening_by_moves(self, moves: str) -> Opening:
        """
        Identifie une ouverture par ses premiers coups
        
        Args:
            moves: Notation des coups (ex: "1.e4 e5 2.Nf3")
            
        Returns:
            Ouverture correspondante ou None
        """
        # Normalise les coups
        normalized_moves = moves.strip().lower()
        
        for opening in self.openings:
            if opening.moves.lower() in normalized_moves:
                return opening
        
        return None