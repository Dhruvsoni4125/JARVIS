import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ASSISTANT_NAME = "jarvis"

# API Keys Configuration
class APIKeys:
    # Speech Recognition
    GOOGLE_SPEECH_API_KEY = os.getenv('GOOGLE_SPEECH_API_KEY')
    AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
    AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Additional LLM Providers
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')  # Claude
    GOOGLE_AI_API_KEY = os.getenv('GOOGLE_AI_API_KEY')  # Google AI Studio
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  # Gemini API
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
    COHERE_API_KEY = os.getenv('COHERE_API_KEY')
    
    # Weather
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    
    # News
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    
    # Spotify
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    # Email
    EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    
    # Porcupine
    PORCUPINE_ACCESS_KEY = os.getenv('PORCUPINE_ACCESS_KEY')
    
    # YouTube
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    
    # WhatsApp Business
    WHATSAPP_BUSINESS_API_KEY = os.getenv('WHATSAPP_BUSINESS_API_KEY')
    
    @classmethod
    def validate_keys(cls):
        """Validate that required API keys are present"""
        missing_keys = []
        
        # Add validation for required keys here
        if not cls.GOOGLE_SPEECH_API_KEY:
            print("Warning: Google Speech API key not found. Using free tier.")
            
        if not cls.PORCUPINE_ACCESS_KEY:
            print("Warning: Porcupine access key not found. Using default wake word.")
            
        return missing_keys