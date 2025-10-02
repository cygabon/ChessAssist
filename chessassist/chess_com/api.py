"""
Client pour l'API chess.com
"""

import requests
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class GameInfo:
    """Informations sur une partie"""
    game_id: str
    url: str
    pgn: str
    white_player: str
    black_player: str
    white_rating: int
    black_rating: int
    time_control: str
    end_time: datetime
    result: str
    rated: bool

class ChessComAPI:
    """Client pour l'API chess.com"""
    
    BASE_URL = "https://api.chess.com/pub"
    
    def __init__(self, rate_limit_delay: float = 1.0):
        """
        Initialise le client API
        
        Args:
            rate_limit_delay: Délai entre les requêtes (en secondes)
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ChessAssist/0.1.0 (Educational Tool)'
        })
        self.rate_limit_delay = rate_limit_delay
        self.last_request_time = 0
    
    def _make_request(self, endpoint: str) -> Dict:
        """
        Effectue une requête à l'API avec gestion du rate limiting
        
        Args:
            endpoint: Point de terminaison de l'API
            
        Returns:
            Réponse JSON de l'API
        """
        # Gestion du rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            self.last_request_time = time.time()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Erreur API chess.com: {e}")
    
    def get_player_profile(self, username: str) -> Dict:
        """
        Récupère le profil d'un joueur
        
        Args:
            username: Nom d'utilisateur chess.com
            
        Returns:
            Données du profil joueur
        """
        return self._make_request(f"/player/{username}")
    
    def get_player_stats(self, username: str) -> Dict:
        """
        Récupère les statistiques d'un joueur
        
        Args:
            username: Nom d'utilisateur chess.com
            
        Returns:
            Statistiques du joueur
        """
        return self._make_request(f"/player/{username}/stats")
    
    def get_monthly_games(self, username: str, year: int, month: int) -> List[Dict]:
        """
        Récupère les parties d'un mois donné
        
        Args:
            username: Nom d'utilisateur chess.com
            year: Année
            month: Mois (1-12)
            
        Returns:
            Liste des parties du mois
        """
        formatted_month = f"{year:04d}/{month:02d}"
        data = self._make_request(f"/player/{username}/games/{formatted_month}")
        return data.get("games", [])
    
    def get_recent_games(self, username: str, limit: int = 10) -> List[GameInfo]:
        """
        Récupère les parties récentes d'un joueur
        
        Args:
            username: Nom d'utilisateur chess.com
            limit: Nombre maximum de parties à récupérer
            
        Returns:
            Liste des parties récentes
        """
        # Commence par le mois actuel
        now = datetime.now()
        games = []
        
        for months_back in range(3):  # Regarde les 3 derniers mois
            check_date = now - timedelta(days=30 * months_back)
            monthly_games = self.get_monthly_games(
                username, 
                check_date.year, 
                check_date.month
            )
            
            for game_data in monthly_games:
                if len(games) >= limit:
                    break
                
                game_info = self._parse_game_data(game_data)
                if game_info:
                    games.append(game_info)
            
            if len(games) >= limit:
                break
        
        # Trie par date décroissante et limite
        games.sort(key=lambda g: g.end_time, reverse=True)
        return games[:limit]
    
    def get_game_pgn(self, game_url: str) -> str:
        """
        Extrait le PGN d'une partie depuis son URL
        
        Args:
            game_url: URL de la partie chess.com
            
        Returns:
            PGN de la partie
        """
        # Cette méthode nécessiterait du web scraping
        # Pour l'instant, on utilise le PGN déjà disponible dans les données
        # Une implémentation complète pourrait utiliser selenium ou requests-html
        return ""
    
    def _parse_game_data(self, game_data: Dict) -> Optional[GameInfo]:
        """
        Parse les données d'une partie depuis l'API
        
        Args:
            game_data: Données brutes de la partie
            
        Returns:
            Objet GameInfo ou None si parsing échoue
        """
        try:
            # Extraction des informations de base
            game_id = game_data.get("uuid", "")
            url = game_data.get("url", "")
            pgn = game_data.get("pgn", "")
            
            # Joueurs et ratings
            white = game_data.get("white", {})
            black = game_data.get("black", {})
            
            white_player = white.get("username", "Unknown")
            black_player = black.get("username", "Unknown")
            white_rating = white.get("rating", 0)
            black_rating = black.get("rating", 0)
            
            # Détails de la partie
            time_control = game_data.get("time_control", "")
            end_time = datetime.fromtimestamp(game_data.get("end_time", 0))
            result = white.get("result", "unknown")
            rated = game_data.get("rated", False)
            
            return GameInfo(
                game_id=game_id,
                url=url,
                pgn=pgn,
                white_player=white_player,
                black_player=black_player,
                white_rating=white_rating,
                black_rating=black_rating,
                time_control=time_control,
                end_time=end_time,
                result=result,
                rated=rated
            )
        except Exception as e:
            print(f"Erreur lors du parsing de la partie: {e}")
            return None
    
    def analyze_player_openings(self, username: str, limit: int = 50) -> Dict[str, int]:
        """
        Analyse les ouvertures préférées d'un joueur
        
        Args:
            username: Nom d'utilisateur chess.com
            limit: Nombre de parties à analyser
            
        Returns:
            Dictionnaire des ouvertures avec leur fréquence
        """
        games = self.get_recent_games(username, limit)
        opening_counts = {}
        
        for game in games:
            if game.pgn:
                # Extraction simplifiée de l'ouverture depuis le PGN
                # Une implémentation plus sophistiquée analyserait les premiers coups
                opening = self._extract_opening_from_pgn(game.pgn)
                if opening:
                    opening_counts[opening] = opening_counts.get(opening, 0) + 1
        
        return opening_counts
    
    def _extract_opening_from_pgn(self, pgn: str) -> Optional[str]:
        """
        Extrait le nom de l'ouverture depuis un PGN
        
        Args:
            pgn: Partie au format PGN
            
        Returns:
            Nom de l'ouverture ou None
        """
        # Recherche dans les métadonnées du PGN
        lines = pgn.split('\n')
        for line in lines:
            if '[ECO ' in line or '[Opening ' in line:
                # Extraction du nom entre guillemets
                start = line.find('"') + 1
                end = line.rfind('"')
                if start > 0 and end > start:
                    return line[start:end]
        
        return None