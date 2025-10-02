"""
Gestion de la configuration de ChessAssist
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

@dataclass
class Config:
    """Configuration de l'application"""
    chess_com_username: Optional[str] = None
    stockfish_path: Optional[str] = None
    analysis_depth: int = 15
    analysis_time: float = 2.0
    api_rate_limit: float = 1.0
    
class ConfigManager:
    """Gestionnaire de configuration"""
    
    def __init__(self, config_file: str = ".env"):
        """
        Initialise le gestionnaire de configuration
        
        Args:
            config_file: Chemin vers le fichier de configuration
        """
        self.config_file = Path(config_file)
        self.config = Config()
        self.load_config()
    
    def load_config(self):
        """Charge la configuration depuis le fichier .env et les variables d'environnement"""
        # Charge depuis les variables d'environnement
        self.config.chess_com_username = os.getenv("CHESS_COM_USERNAME")
        self.config.stockfish_path = os.getenv("STOCKFISH_PATH")
        
        # Paramètres optionnels avec valeurs par défaut
        try:
            self.config.analysis_depth = int(os.getenv("ANALYSIS_DEPTH", "15"))
            self.config.analysis_time = float(os.getenv("ANALYSIS_TIME", "2.0"))
            self.config.api_rate_limit = float(os.getenv("API_RATE_LIMIT", "1.0"))
        except ValueError:
            # Garde les valeurs par défaut en cas d'erreur
            pass
        
        # Charge depuis le fichier .env s'il existe
        if self.config_file.exists():
            self._load_from_file()
    
    def _load_from_file(self):
        """Charge la configuration depuis le fichier .env"""
        try:
            with open(self.config_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        
                        # Met à jour la configuration
                        if key == "CHESS_COM_USERNAME":
                            self.config.chess_com_username = value
                        elif key == "STOCKFISH_PATH":
                            self.config.stockfish_path = value
                        elif key == "ANALYSIS_DEPTH":
                            self.config.analysis_depth = int(value)
                        elif key == "ANALYSIS_TIME":
                            self.config.analysis_time = float(value)
                        elif key == "API_RATE_LIMIT":
                            self.config.api_rate_limit = float(value)
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {e}")
    
    def save_config(self):
        """Sauvegarde la configuration dans le fichier .env"""
        try:
            with open(self.config_file, 'w') as f:
                f.write("# Configuration ChessAssist\n\n")
                
                if self.config.chess_com_username:
                    f.write(f"CHESS_COM_USERNAME={self.config.chess_com_username}\n")
                
                if self.config.stockfish_path:
                    f.write(f"STOCKFISH_PATH={self.config.stockfish_path}\n")
                
                f.write(f"ANALYSIS_DEPTH={self.config.analysis_depth}\n")
                f.write(f"ANALYSIS_TIME={self.config.analysis_time}\n")
                f.write(f"API_RATE_LIMIT={self.config.api_rate_limit}\n")
                
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la configuration: {e}")
    
    def validate_config(self) -> bool:
        """
        Valide la configuration
        
        Returns:
            True si la configuration est valide
        """
        errors = []
        
        # Vérifie Stockfish
        if self.config.stockfish_path:
            if not os.path.exists(self.config.stockfish_path):
                errors.append(f"Stockfish introuvable: {self.config.stockfish_path}")
        else:
            # Tente de trouver Stockfish automatiquement
            stockfish_paths = [
                "/usr/local/bin/stockfish",
                "/usr/bin/stockfish",
                "/opt/homebrew/bin/stockfish"
            ]
            
            found = False
            for path in stockfish_paths:
                if os.path.exists(path):
                    self.config.stockfish_path = path
                    found = True
                    break
            
            if not found:
                errors.append("Stockfish non trouvé. Installez-le ou spécifiez le chemin.")
        
        # Affiche les erreurs
        if errors:
            print("Erreurs de configuration:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True
    
    def setup_interactive(self):
        """Configuration interactive"""
        print("=== Configuration ChessAssist ===\n")
        
        # Nom d'utilisateur chess.com
        if not self.config.chess_com_username:
            username = input("Nom d'utilisateur chess.com (optionnel): ").strip()
            if username:
                self.config.chess_com_username = username
        
        # Chemin Stockfish
        if not self.config.stockfish_path:
            stockfish_path = input("Chemin vers Stockfish (optionnel, auto-détection): ").strip()
            if stockfish_path:
                self.config.stockfish_path = stockfish_path
        
        # Sauvegarde
        save = input("Sauvegarder la configuration? (y/N): ").strip().lower()
        if save in ['y', 'yes', 'oui']:
            self.save_config()
            print("Configuration sauvegardée dans .env")
        
        print("Configuration terminée!")

# Instance globale de configuration
config_manager = ConfigManager()
config = config_manager.config