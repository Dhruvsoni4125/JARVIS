#!/usr/bin/env python3
"""
Test script to verify API configuration for JARVIS
Run this script to check which APIs are properly configured
"""

import os
import sys

def load_env_file():
    """Load environment variables from .env file"""
    try:
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        env_vars = {}
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
        
        return env_vars
    except FileNotFoundError:
        print("❌ .env file not found!")
        return {}
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return {}

def test_weather_api(api_key):
    """Test OpenWeatherMap API"""
    if not api_key:
        return False, "API key not provided"
    
    try:
        import requests
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {"q": "London", "appid": api_key, "units": "metric"}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            return True, f"Working! London temperature: {temp}°C"
        elif response.status_code == 401:
            return False, "Invalid API key"
        else:
            return False, f"API error: {response.status_code}"
    
    except ImportError:
        return False, "requests module not installed (pip install requests)"
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_news_api(api_key):
    """Test News API"""
    if not api_key:
        return False, "API key not provided"
    
    try:
        import requests
        url = "https://newsapi.org/v2/top-headlines"
        params = {"apiKey": api_key, "country": "us", "pageSize": 1}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("articles"):
                title = data["articles"][0]["title"][:50] + "..."
                return True, f"Working! Latest headline: {title}"
            else:
                return True, "Working! (No articles found)"
        elif response.status_code == 401:
            return False, "Invalid API key"
        else:
            return False, f"API error: {response.status_code}"
    
    except ImportError:
        return False, "requests module not installed (pip install requests)"
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_openai_api(api_key):
    """Test OpenAI API"""
    if not api_key:
        return False, "API key not provided"
    
    try:
        import openai
        openai.api_key = api_key
        
        # Simple test request
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'API test successful'"}],
            max_tokens=10
        )
        
        return True, "Working! OpenAI API is accessible"
    
    except ImportError:
        return False, "openai module not installed (pip install openai)"
    except Exception as e:
        error_msg = str(e)
        if "invalid_api_key" in error_msg:
            return False, "Invalid API key"
        elif "insufficient_quota" in error_msg:
            return False, "API key valid but no credits remaining"
        else:
            return False, f"Error: {error_msg}"

def main():
    print("🤖 JARVIS API Configuration Test")
    print("=" * 50)
    
    # Load environment variables
    env_vars = load_env_file()
    
    if not env_vars:
        print("\n❌ No .env file found or file is empty!")
        print("Please create a .env file with your API keys.")
        print("See API_SETUP_GUIDE.md for instructions.")
        return
    
    print(f"✅ Found .env file with {len(env_vars)} variables")
    
    # Test each API
    apis_to_test = [
        ("Weather API (OpenWeatherMap)", "OPENWEATHER_API_KEY", test_weather_api),
        ("News API", "NEWS_API_KEY", test_news_api),
        ("OpenAI API", "OPENAI_API_KEY", test_openai_api),
    ]
    
    print("\n🧪 Testing APIs...")
    print("-" * 30)
    
    working_apis = 0
    total_apis = len(apis_to_test)
    
    for api_name, env_key, test_func in apis_to_test:
        api_key = env_vars.get(env_key, "").strip()
        
        if not api_key:
            print(f"⚪ {api_name}: Not configured")
            continue
        
        print(f"🔍 Testing {api_name}...")
        success, message = test_func(api_key)
        
        if success:
            print(f"✅ {api_name}: {message}")
            working_apis += 1
        else:
            print(f"❌ {api_name}: {message}")
    
    # Configuration summary
    configured_apis = sum(1 for key in ["OPENWEATHER_API_KEY", "NEWS_API_KEY", "OPENAI_API_KEY"] 
                         if env_vars.get(key, "").strip())
    
    other_configs = [
        ("Email Username", "EMAIL_USERNAME"),
        ("Email Password", "EMAIL_PASSWORD"),
        ("Google Speech API", "GOOGLE_SPEECH_API_KEY"),
        ("Azure Speech API", "AZURE_SPEECH_KEY"),
        ("YouTube API", "YOUTUBE_API_KEY"),
        ("Spotify Client ID", "SPOTIFY_CLIENT_ID"),
        ("Porcupine Access Key", "PORCUPINE_ACCESS_KEY"),
    ]
    
    print(f"\n📊 Summary:")
    print(f"Working APIs: {working_apis}/{total_apis}")
    print(f"Configured APIs: {configured_apis}/{total_apis}")
    
    print(f"\n📋 Other Configurations:")
    for config_name, env_key in other_configs:
        value = env_vars.get(env_key, "").strip()
        status = "✅ Set" if value else "⚪ Not set"
        print(f"{status} {config_name}")
    
    print(f"\n🎯 Next Steps:")
    
    if working_apis == 0:
        print("1. Add API keys to your .env file")
        print("2. Check API_SETUP_GUIDE.md for instructions")
        print("3. Run this test again")
    elif working_apis < total_apis:
        print("1. Some APIs are working! 🎉")
        print("2. Add remaining API keys for full functionality")
        print("3. Check the error messages above")
    else:
        print("🎉 All APIs are working! JARVIS is ready for enhanced features!")
    
    print(f"\n💡 Tips:")
    print("- Keep your .env file secure and don't share it")
    print("- Some APIs have usage limits")
    print("- Restart JARVIS after updating .env file")

if __name__ == "__main__":
    main()