# JARVIS API Setup Guide

This guide shows you how to add API keys to your JARVIS assistant for enhanced functionality.

## Quick Start

1. **Edit the `.env` file** in your project root
2. **Add your API keys** (see examples below)
3. **Restart JARVIS** to use the new features

## Available API Integrations

### 1. Weather API (OpenWeatherMap)
Get weather information for any city.

**Setup:**
1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Get your API key
4. Add to `.env` file:
```
OPENWEATHER_API_KEY=your_api_key_here
```

**Usage:**
- "What's the weather in Delhi?"
- "Weather in Mumbai"
- "Tell me the weather"

### 2. News API
Get latest news headlines.

**Setup:**
1. Go to https://newsapi.org/
2. Sign up for a free account
3. Get your API key
4. Add to `.env` file:
```
NEWS_API_KEY=your_api_key_here
```

**Usage:**
- "Get me the latest news"
- "What are today's headlines?"
- "Tell me the news"

### 3. OpenAI API (ChatGPT)
Get AI-powered responses for complex queries.

**Setup:**
1. Go to https://platform.openai.com/
2. Create an account
3. Get your API key
4. Add to `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

**Usage:**
- "Ask AI: How does photosynthesis work?"
- "AI explain quantum computing"

### 4. Email Integration
Send emails through JARVIS.

**Setup (Gmail):**
1. Enable 2-factor authentication on Gmail
2. Generate an App Password
3. Add to `.env` file:
```
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

**Usage:**
- "Send email to john@example.com"
- "Email my report to boss"

### 5. Enhanced Speech Recognition
Use premium speech recognition services.

**Setup (Google Cloud):**
1. Go to Google Cloud Console
2. Enable Speech-to-Text API
3. Create credentials
4. Add to `.env` file:
```
GOOGLE_SPEECH_API_KEY=your_google_speech_key
```

**Setup (Azure):**
1. Go to Azure Portal
2. Create Speech Service
3. Get key and region
4. Add to `.env` file:
```
AZURE_SPEECH_KEY=your_azure_key
AZURE_SPEECH_REGION=your_region
```

### 6. YouTube Data API
Better YouTube search and control.

**Setup:**
1. Go to Google Cloud Console
2. Enable YouTube Data API v3
3. Create credentials
4. Add to `.env` file:
```
YOUTUBE_API_KEY=your_youtube_api_key
```

**Usage:**
- "Search YouTube for python tutorials"
- "Play the latest music videos"

### 7. Spotify Integration
Control Spotify playback.

**Setup:**
1. Go to Spotify Developer Dashboard
2. Create an app
3. Get Client ID and Secret
4. Add to `.env` file:
```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

**Usage:**
- "Play music on Spotify"
- "Skip to next song"
- "What's playing?"

### 8. Porcupine Wake Word (Commercial)
For commercial use of wake word detection.

**Setup:**
1. Go to Picovoice Console
2. Create account and get access key
3. Add to `.env` file:
```
PORCUPINE_ACCESS_KEY=your_porcupine_key
```

## How to Use Your .env File

Your `.env` file should look like this:

```bash
# Weather API
OPENWEATHER_API_KEY=abcd1234567890

# News API  
NEWS_API_KEY=xyz9876543210

# OpenAI API
OPENAI_API_KEY=sk-1234567890abcdef

# Email Configuration
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Speech Recognition
GOOGLE_SPEECH_API_KEY=your_google_key
AZURE_SPEECH_KEY=your_azure_key
AZURE_SPEECH_REGION=eastus

# YouTube API
YOUTUBE_API_KEY=your_youtube_key

# Spotify API
SPOTIFY_CLIENT_ID=your_spotify_id
SPOTIFY_CLIENT_SECRET=your_spotify_secret

# Porcupine (Commercial)
PORCUPINE_ACCESS_KEY=your_porcupine_key

# WhatsApp Business API (if available)
WHATSAPP_BUSINESS_API_KEY=your_whatsapp_key
```

## Testing Your Setup

1. **Check API Status:**
   - Say: "Check APIs" or "API status"
   - JARVIS will tell you which APIs are configured

2. **Test Individual APIs:**
   - Weather: "What's the weather?"
   - News: "Get me the news"
   - Each API can be tested individually

## Security Notes

⚠️ **Important:**
- Never commit your `.env` file to version control
- Keep your API keys secret
- Use environment variables in production
- Some APIs have rate limits and costs

## Troubleshooting

### Common Issues:

1. **"API key not found"**
   - Check your `.env` file spelling
   - Restart JARVIS after adding keys

2. **"Module not found"**
   - Install required packages:
   ```
   pip install requests python-dotenv openai
   ```

3. **"API request failed"**
   - Check your internet connection
   - Verify API key is correct
   - Check API service status

### Getting Help:

1. Check the console output for detailed error messages
2. Verify API keys are valid on the respective websites
3. Test APIs individually using online tools first

## Next Steps

1. **Start with free APIs** like OpenWeatherMap and News API
2. **Test each integration** before adding more
3. **Customize commands** in the code to match your preferences
4. **Add more APIs** as needed for your use case

## Free vs Paid APIs

**Free Options:**
- OpenWeatherMap (limited requests)
- News API (limited requests)
- Google Speech Recognition (basic)

**Paid Options (with free tiers):**
- OpenAI API (pay per use)
- Google Cloud Speech (pay per use)
- Azure Speech Services (free tier available)

Choose based on your usage needs and budget!