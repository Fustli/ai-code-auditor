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
    api_provider: str = "openai"  # "openai" or "gemini"
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
        # Check for API provider
        api_provider = os.getenv("API_PROVIDER", "openai").lower()
        
        # Get appropriate API key
        if api_provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable is required when using Gemini")
            default_model = "models/gemini-2.0-flash"  # Use v1beta API naming
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required when using OpenAI")
            default_model = "gpt-4o"
        
        return cls(
            api_key=api_key,
            api_provider=api_provider,
            model=os.getenv("AI_MODEL", default_model),
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