"""Configuration management for the LLM Quiz application."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""
    
    # Student credentials
    STUDENT_EMAIL = os.getenv("STUDENT_EMAIL", "")
    STUDENT_SECRET = os.getenv("STUDENT_SECRET", "")
    
    # OpenAI API
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Server settings
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    # Timeout settings
    QUIZ_TIMEOUT = int(os.getenv("QUIZ_TIMEOUT", "180"))  # 3 minutes
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.STUDENT_EMAIL:
            raise ValueError("STUDENT_EMAIL not set in environment")
        if not cls.STUDENT_SECRET:
            raise ValueError("STUDENT_SECRET not set in environment")
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in environment")
        return True
