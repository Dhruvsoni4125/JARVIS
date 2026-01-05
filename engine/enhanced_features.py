"""
Enhanced features for JARVIS with API key support
This file demonstrates how to integrate various APIs
"""

import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from engine.config import APIKeys
from engine.command import speak

# Weather Feature using OpenWeatherMap API
def get_weather(city):
    """Get weather information for a city"""
    if not APIKeys.OPENWEATHER_API_KEY:
        speak("Weather API key not configured. Please add your OpenWeatherMap API key.")
        return
    
    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": APIKeys.OPENWEATHER_API_KEY,
            "units": "metric"
        }
        
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            
            weather_report = f"The weather in {city} is {description} with a temperature of {temp} degrees Celsius and humidity of {humidity} percent."
            speak(weather_report)
            return weather_report
        else:
            speak(f"Sorry, I couldn't get weather information for {city}")
            return None
            
    except Exception as e:
        print(f"Weather API error: {e}")
        speak("Sorry, there was an error getting weather information")
        return None

# News Feature using News API
def get_latest_news(category="general", count=5):
    """Get latest news headlines"""
    if not APIKeys.NEWS_API_KEY:
        speak("News API key not configured. Please add your News API key.")
        return
    
    try:
        base_url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": APIKeys.NEWS_API_KEY,
            "country": "in",  # India
            "category": category,
            "pageSize": count
        }
        
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200 and data["status"] == "ok":
            articles = data["articles"]
            
            if articles:
                speak(f"Here are the top {len(articles)} {category} news headlines:")
                for i, article in enumerate(articles, 1):
                    headline = article["title"]
                    speak(f"News {i}: {headline}")
                    print(f"{i}. {headline}")
                return articles
            else:
                speak("No news articles found")
                return None
        else:
            speak("Sorry, I couldn't fetch the latest news")
            return None
            
    except Exception as e:
        print(f"News API error: {e}")
        speak("Sorry, there was an error getting news information")
        return None

# Email Feature
def send_email(to_email, subject, message):
    """Send email using configured email credentials"""
    if not APIKeys.EMAIL_USERNAME or not APIKeys.EMAIL_PASSWORD:
        speak("Email credentials not configured. Please add your email settings.")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = APIKeys.EMAIL_USERNAME
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(message, 'plain'))
        
        # Gmail SMTP configuration
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(APIKeys.EMAIL_USERNAME, APIKeys.EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(APIKeys.EMAIL_USERNAME, to_email, text)
        server.quit()
        
        speak(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"Email error: {e}")
        speak("Sorry, there was an error sending the email")
        return False

# OpenAI Integration (for advanced AI responses)
def get_ai_response(prompt):
    """Get AI response using OpenAI API"""
    if not APIKeys.OPENAI_API_KEY:
        speak("OpenAI API key not configured. Please add your OpenAI API key for advanced AI features.")
        return None
    
    try:
        import openai
        openai.api_key = APIKeys.OPENAI_API_KEY
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are JARVIS, a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content.strip()
        speak(ai_response)
        return ai_response
        
    except ImportError:
        speak("OpenAI library not installed. Please install it with: pip install openai")
        return None
    except Exception as e:
        print(f"OpenAI API error: {e}")
        speak("Sorry, there was an error getting AI response")
        return None

# YouTube API Integration (for better YouTube control)
def search_youtube_videos(query, max_results=5):
    """Search YouTube videos using YouTube Data API"""
    if not APIKeys.YOUTUBE_API_KEY:
        speak("YouTube API key not configured. Using fallback method.")
        # Fallback to existing method
        from engine.features import PlayYoutube
        PlayYoutube(f"play {query} on youtube")
        return
    
    try:
        base_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "key": APIKeys.YOUTUBE_API_KEY,
            "q": query,
            "part": "snippet",
            "type": "video",
            "maxResults": max_results
        }
        
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            videos = data.get("items", [])
            if videos:
                speak(f"Found {len(videos)} videos for {query}")
                for i, video in enumerate(videos, 1):
                    title = video["snippet"]["title"]
                    video_id = video["id"]["videoId"]
                    print(f"{i}. {title} - https://www.youtube.com/watch?v={video_id}")
                
                # Play the first video
                first_video_id = videos[0]["id"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={first_video_id}"
                import webbrowser
                webbrowser.open(video_url)
                speak(f"Playing {videos[0]['snippet']['title']}")
                return videos
            else:
                speak("No videos found")
                return None
        else:
            speak("Error searching YouTube videos")
            return None
            
    except Exception as e:
        print(f"YouTube API error: {e}")
        speak("Sorry, there was an error searching YouTube")
        return None

# Enhanced Speech Recognition with multiple providers
def enhanced_speech_recognition():
    """Use different speech recognition APIs based on availability"""
    import speech_recognition as sr
    
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Enhanced listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)
    
    try:
        # Try Google Speech API with key if available
        if APIKeys.GOOGLE_SPEECH_API_KEY:
            query = r.recognize_google(audio, key=APIKeys.GOOGLE_SPEECH_API_KEY, language='en-in')
            print("Used Google Speech API with key")
        else:
            # Fall back to free Google Speech Recognition
            query = r.recognize_google(audio, language='en-in')
            print("Used free Google Speech Recognition")
        
        print(f"Enhanced recognition result: {query}")
        return query.lower()
        
    except sr.RequestError as e:
        print(f"Speech recognition request error: {e}")
        # Try Azure Speech if available
        if APIKeys.AZURE_SPEECH_KEY:
            try:
                query = r.recognize_azure(audio, key=APIKeys.AZURE_SPEECH_KEY, location=APIKeys.AZURE_SPEECH_REGION)
                print("Used Azure Speech Recognition")
                return query.lower()
            except Exception as azure_error:
                print(f"Azure Speech error: {azure_error}")
        
        speak("Sorry, I couldn't understand that")
        return ""
    
    except sr.UnknownValueError:
        print("Could not understand audio")
        speak("Sorry, I couldn't understand that")
        return ""

# Function to validate all API keys
def validate_all_apis():
    """Check which APIs are configured and working"""
    print("\n=== API Configuration Status ===")
    
    # Check each API
    apis_status = {
        "Google Speech API": bool(APIKeys.GOOGLE_SPEECH_API_KEY),
        "Azure Speech API": bool(APIKeys.AZURE_SPEECH_KEY and APIKeys.AZURE_SPEECH_REGION),
        "OpenAI API": bool(APIKeys.OPENAI_API_KEY),
        "OpenWeather API": bool(APIKeys.OPENWEATHER_API_KEY),
        "News API": bool(APIKeys.NEWS_API_KEY),
        "Spotify API": bool(APIKeys.SPOTIFY_CLIENT_ID and APIKeys.SPOTIFY_CLIENT_SECRET),
        "Email Configuration": bool(APIKeys.EMAIL_USERNAME and APIKeys.EMAIL_PASSWORD),
        "YouTube API": bool(APIKeys.YOUTUBE_API_KEY),
        "WhatsApp Business API": bool(APIKeys.WHATSAPP_BUSINESS_API_KEY),
        "Porcupine Access Key": bool(APIKeys.PORCUPINE_ACCESS_KEY)
    }
    
    configured_count = sum(apis_status.values())
    total_apis = len(apis_status)
    
    for api_name, status in apis_status.items():
        status_text = "✓ Configured" if status else "✗ Not configured"
        print(f"{api_name}: {status_text}")
    
    print(f"\nTotal: {configured_count}/{total_apis} APIs configured")
    
    if configured_count == 0:
        print("No API keys configured. JARVIS will use basic functionality only.")
    elif configured_count < total_apis:
        print("Some API keys are missing. Add them to .env file for full functionality.")
    else:
        print("All APIs configured! JARVIS has full functionality.")
    
    return apis_status