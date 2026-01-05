"""
Simple API integration examples for JARVIS
This shows how to add different API services to your assistant
"""

import requests
import os
from engine.command import speak

class APIManager:
    """Simple API manager for JARVIS"""
    
    def __init__(self):
        # Load API keys from environment variables or .env file
        self.load_api_keys()
    
    def load_api_keys(self):
        """Load API keys from environment or .env file"""
        try:
            # Try to load from .env file
            import dotenv
            dotenv.load_dotenv()
        except ImportError:
            print("python-dotenv not installed. Using environment variables only.")
        except Exception as e:
            print(f"Could not load .env file: {e}. Using environment variables only.")
        
        # Set API keys
        self.weather_api_key = os.getenv('OPENWEATHER_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.email_username = os.getenv('EMAIL_USERNAME')
        self.email_password = os.getenv('EMAIL_PASSWORD')
    
    def get_weather(self, city):
        """Get weather for a city using OpenWeatherMap API"""
        if not self.weather_api_key:
            speak("Weather API key not found. Please add OPENWEATHER_API_KEY to your .env file")
            print("Get your free API key from: https://openweathermap.org/api")
            return None
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": self.weather_api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"]
                
                weather_info = f"Weather in {city}: {description}, {temp} degrees Celsius"
                speak(weather_info)
                return weather_info
            else:
                speak(f"Could not get weather for {city}")
                return None
                
        except Exception as e:
            print(f"Weather API error: {e}")
            speak("Error getting weather information")
            return None
    
    def get_news(self, count=3):
        """Get latest news using News API"""
        if not self.news_api_key:
            speak("News API key not found. Please add NEWS_API_KEY to your .env file")
            print("Get your free API key from: https://newsapi.org/")
            return None
        
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                "apiKey": self.news_api_key,
                "country": "in",
                "pageSize": count
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])
                
                if articles:
                    speak(f"Here are the top {len(articles)} news headlines:")
                    for i, article in enumerate(articles, 1):
                        headline = article["title"]
                        speak(f"News {i}: {headline}")
                        print(f"{i}. {headline}")
                    return articles
                else:
                    speak("No news found")
                    return None
            else:
                speak("Could not get news")
                return None
                
        except Exception as e:
            print(f"News API error: {e}")
            speak("Error getting news")
            return None
    
    def check_api_status(self):
        """Check which APIs are configured"""
        status = {
            "Weather API": bool(self.weather_api_key),
            "News API": bool(self.news_api_key),
            "OpenAI API": bool(self.openai_api_key),
            "Email": bool(self.email_username and self.email_password)
        }
        
        print("\n=== API Status ===")
        for api, configured in status.items():
            status_text = "✓ Ready" if configured else "✗ Not configured"
            print(f"{api}: {status_text}")
        
        configured_count = sum(status.values())
        print(f"\n{configured_count}/{len(status)} APIs configured")
        
        if configured_count == 0:
            print("\nTo add API keys:")
            print("1. Edit the .env file")
            print("2. Add your API keys")
            print("3. Restart JARVIS")
        
        return status

# Global API manager instance
api_manager = APIManager()

# Functions that can be called from command.py
def handle_weather_command(query):
    """Handle weather-related commands"""
    try:
        # Extract city name from query
        words = query.split()
        if "weather" in words:
            city_index = words.index("weather") + 1
            if city_index < len(words):
                city = " ".join(words[city_index:])
            else:
                city = "Delhi"  # Default city
        else:
            city = "Delhi"
        
        api_manager.get_weather(city)
        
    except Exception as e:
        print(f"Weather command error: {e}")
        speak("Sorry, I couldn't get the weather information")

def handle_news_command(query):
    """Handle news-related commands"""
    try:
        api_manager.get_news(count=3)
    except Exception as e:
        print(f"News command error: {e}")
        speak("Sorry, I couldn't get the news")

def handle_api_status_command():
    """Show API configuration status"""
    try:
        status = api_manager.check_api_status()
        
        configured = sum(status.values())
        total = len(status)
        
        speak(f"I have {configured} out of {total} API services configured")
        
        if configured == 0:
            speak("No API keys are configured. Please check the .env file for setup instructions")
        elif configured < total:
            speak("Some API services are available. Check the console for details")
        else:
            speak("All API services are ready to use")
            
    except Exception as e:
        print(f"API status error: {e}")
        speak("Error checking API status")

# Example of how to add this to your existing command processing
def process_api_commands(query):
    """Process API-related commands"""
    query = query.lower().strip()
    
    if "weather" in query:
        handle_weather_command(query)
        return True
    
    elif "news" in query or "headlines" in query:
        handle_news_command(query)
        return True
    
    elif "api status" in query or "check apis" in query:
        handle_api_status_command()
        return True
    
    return False  # Command not handled