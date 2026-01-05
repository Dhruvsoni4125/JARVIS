#!/usr/bin/env python3
"""
Demo script showing how to integrate APIs into JARVIS
This script demonstrates working API integration without external dependencies
"""

import os
import json

def load_config():
    """Load configuration from .env file or environment variables"""
    config = {}
    
    # Try to load from .env file first
    try:
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
            print("✅ Loaded configuration from .env file")
        else:
            print("⚠️  .env file not found, using environment variables")
    except Exception as e:
        print(f"Error reading .env file: {e}")
    
    # Also check environment variables (they override .env)
    api_keys = [
        'OPENWEATHER_API_KEY', 'NEWS_API_KEY', 'OPENAI_API_KEY',
        'EMAIL_USERNAME', 'EMAIL_PASSWORD', 'YOUTUBE_API_KEY',
        'SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_SECRET',
        'GOOGLE_SPEECH_API_KEY', 'AZURE_SPEECH_KEY', 'AZURE_SPEECH_REGION'
    ]
    
    for key in api_keys:
        env_value = os.getenv(key)
        if env_value:
            config[key] = env_value
    
    return config

def demo_weather_integration():
    """Demo how weather API would be integrated"""
    print("\n🌤️  Weather API Integration Demo")
    print("-" * 40)
    
    config = load_config()
    api_key = config.get('OPENWEATHER_API_KEY')
    
    if not api_key or api_key == 'your_openweather_api_key_here':
        print("❌ Weather API key not configured")
        print("👉 Get your free API key from: https://openweathermap.org/api")
        print("👉 Add it to your .env file as: OPENWEATHER_API_KEY=your_actual_key")
        return False
    
    print(f"✅ Weather API key configured: {api_key[:8]}...")
    print("🔧 Integration ready! Commands that would work:")
    print("   - 'What's the weather in Delhi?'")
    print("   - 'Weather forecast for Mumbai'")
    print("   - 'Tell me today's weather'")
    
    # Here's how you would integrate it into JARVIS:
    sample_code = '''
# In your command processing function:
elif "weather" in query:
    from engine.weather_api import get_weather
    city = extract_city_from_query(query)  # You'd implement this
    weather_info = get_weather(city, api_key)
    speak(weather_info)
    '''
    print("\n💻 Sample integration code:")
    print(sample_code)
    return True

def demo_news_integration():
    """Demo how news API would be integrated"""
    print("\n📰 News API Integration Demo")
    print("-" * 40)
    
    config = load_config()
    api_key = config.get('NEWS_API_KEY')
    
    if not api_key or api_key == 'your_news_api_key_here':
        print("❌ News API key not configured")
        print("👉 Get your free API key from: https://newsapi.org/")
        print("👉 Add it to your .env file as: NEWS_API_KEY=your_actual_key")
        return False
    
    print(f"✅ News API key configured: {api_key[:8]}...")
    print("🔧 Integration ready! Commands that would work:")
    print("   - 'Get me the latest news'")
    print("   - 'What are today's headlines?'")
    print("   - 'Tell me technology news'")
    
    sample_code = '''
# In your command processing function:
elif "news" in query or "headlines" in query:
    from engine.news_api import get_latest_news
    category = extract_category_from_query(query)  # general, tech, sports, etc.
    news_items = get_latest_news(category, api_key)
    for i, headline in enumerate(news_items[:3], 1):
        speak(f"News {i}: {headline}")
    '''
    print("\n💻 Sample integration code:")
    print(sample_code)
    return True

def demo_openai_integration():
    """Demo how OpenAI API would be integrated"""
    print("\n🤖 OpenAI API Integration Demo")
    print("-" * 40)
    
    config = load_config()
    api_key = config.get('OPENAI_API_KEY')
    
    if not api_key or api_key == 'your_openai_api_key_here':
        print("❌ OpenAI API key not configured")
        print("👉 Get your API key from: https://platform.openai.com/")
        print("👉 Add it to your .env file as: OPENAI_API_KEY=sk-your_actual_key")
        return False
    
    print(f"✅ OpenAI API key configured: {api_key[:12]}...")
    print("🔧 Integration ready! Commands that would work:")
    print("   - 'Ask AI: How does photosynthesis work?'")
    print("   - 'AI explain quantum computing'")
    print("   - 'Generate a poem about technology'")
    
    sample_code = '''
# In your command processing function:
elif query.startswith("ask ai") or query.startswith("ai "):
    import openai
    openai.api_key = api_key
    
    prompt = query.replace("ask ai:", "").replace("ai ", "").strip()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    ai_answer = response.choices[0].message.content
    speak(ai_answer)
    '''
    print("\n💻 Sample integration code:")
    print(sample_code)
    return True

def demo_email_integration():
    """Demo how email would be integrated"""
    print("\n📧 Email Integration Demo")
    print("-" * 40)
    
    config = load_config()
    username = config.get('EMAIL_USERNAME')
    password = config.get('EMAIL_PASSWORD')
    
    if not username or not password:
        print("❌ Email credentials not configured")
        print("👉 For Gmail:")
        print("   1. Enable 2-factor authentication")
        print("   2. Generate an App Password")
        print("   3. Add to .env file:")
        print("      EMAIL_USERNAME=your_email@gmail.com")
        print("      EMAIL_PASSWORD=your_app_password")
        return False
    
    print(f"✅ Email configured: {username}")
    print("🔧 Integration ready! Commands that would work:")
    print("   - 'Send email to john@example.com'")
    print("   - 'Email my report to boss'")
    print("   - 'Compose email'")
    
    sample_code = '''
# In your command processing function:
elif "send email" in query or "email" in query:
    import smtplib
    from email.mime.text import MIMEText
    
    # Extract recipient and message from query
    recipient = extract_email_from_query(query)
    speak("What should I write in the email?")
    message = takeCommand()  # Your existing function
    
    # Send email
    msg = MIMEText(message)
    msg['Subject'] = "Message from JARVIS"
    msg['From'] = username
    msg['To'] = recipient
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
    
    speak(f"Email sent to {recipient}")
    '''
    print("\n💻 Sample integration code:")
    print(sample_code)
    return True

def show_integration_summary():
    """Show summary of how to integrate all APIs"""
    print("\n🚀 Complete Integration Summary")
    print("=" * 50)
    
    print("\n1. 📁 File Structure for API Integration:")
    structure = """
JARVIS/
├── .env                    # Your API keys (keep secure!)
├── engine/
│   ├── config.py          # Updated with API key loading
│   ├── api_weather.py     # Weather API functions
│   ├── api_news.py        # News API functions
│   ├── api_openai.py      # OpenAI API functions
│   ├── api_email.py       # Email functions
│   └── command.py         # Updated with new commands
└── test_api_setup.py      # Test your API configuration
"""
    print(structure)
    
    print("\n2. 🔧 Integration Steps:")
    steps = [
        "Add your API keys to the .env file",
        "Create individual API modules (weather, news, etc.)",
        "Update command.py to recognize new commands",
        "Test each API integration individually",
        "Add error handling for API failures"
    ]
    
    for i, step in enumerate(steps, 1):
        print(f"   {i}. {step}")
    
    print("\n3. 🎯 New Commands You'll Have:")
    commands = [
        "Weather: 'What's the weather?', 'Weather in Tokyo'",
        "News: 'Get latest news', 'Technology headlines'",
        "AI: 'Ask AI about...', 'Explain quantum physics'",
        "Email: 'Send email to...', 'Compose message'",
        "API Status: 'Check APIs', 'API status'"
    ]
    
    for command in commands:
        print(f"   • {command}")
    
    print("\n4. 💡 Pro Tips:")
    tips = [
        "Start with free APIs (Weather, News)",
        "Test each API with the test_api_setup.py script",
        "Keep API keys secure - never commit them to git",
        "Add error handling for when APIs are down",
        "Consider API rate limits in your implementation"
    ]
    
    for tip in tips:
        print(f"   💡 {tip}")

def main():
    """Main demo function"""
    print("🤖 JARVIS API Integration Demo")
    print("=" * 50)
    print("This demo shows you exactly how to add API keys to JARVIS")
    
    # Run each demo
    demos = [
        demo_weather_integration,
        demo_news_integration,
        demo_openai_integration,
        demo_email_integration
    ]
    
    working_apis = 0
    for demo_func in demos:
        if demo_func():
            working_apis += 1
    
    # Show summary
    show_integration_summary()
    
    print(f"\n📊 Demo Results:")
    print(f"APIs ready for integration: {working_apis}/{len(demos)}")
    
    if working_apis == 0:
        print("\n🔧 Getting Started:")
        print("1. Edit your .env file and add real API keys")
        print("2. Run 'python test_api_setup.py' to verify")
        print("3. Look at the sample code above for integration")
    else:
        print(f"\n🎉 Great! You have {working_apis} APIs ready to integrate!")
        print("Follow the sample code above to add them to JARVIS")

if __name__ == "__main__":
    main()