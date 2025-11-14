import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config(BaseModel):
    """Configuration class for the AI Code Auditor"""
    
    # API Configuration
    api_key: str
    model: str = "gpt-4o"
    max_tokens: int = 4000
    temperature: float = 0.1
    
    # Analysis Configuration
    max_file_size_mb: int = 5
    supported_languages: list = [
        'python', 'javascript', 'typescript', 'java', 'cpp', 'c', 
        'go', 'rust', 'php', 'ruby', 'swift', 'kotlin', 'scala'
    ]
    
    # Scoring Configuration
    score_weights: dict = {
        'quality': 0.4,
        'security': 0.35,
        'performance': 0.25
    }
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        return cls(
            api_key=api_key,
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            max_tokens=int(os.getenv("MAX_TOKENS", "4000")),
            temperature=float(os.getenv("TEMPERATURE", "0.1"))
        )
    
    def get_file_extension_language(self, filename: str) -> Optional[str]:
        """Get language from file extension"""
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.jsx': 'javascript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.hpp': 'cpp',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php',
            '.rb': 'ruby',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala'
        }
        
        ext = os.path.splitext(filename)[1].lower()
        return extension_map.get(ext)