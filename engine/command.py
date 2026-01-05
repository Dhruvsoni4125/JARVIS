import pyttsx3
import speech_recognition as sr
import eel
import time


def speak(text):    
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)
    eel.DisplayMessage(text)  # type: ignore
    engine.say(text)
    eel.receiverText(text)  # type: ignore
    engine.runAndWait()

@eel.expose

def takeCommand():

    r= sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")  # type: ignore
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source,10,6)
    
    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")  # type: ignore
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)  # type: ignore
        time.sleep(2)
        

    except Exception as e:
        print("Say that again please...")
        return ""
    
    return query.lower()

@eel.expose
def allCommand(message=1):
    
    if message == 1:
        # Voice mode - continuous listening
        while True:
            try:
                query = takeCommand().strip()
                print(query)    
                eel.senderText(query)
                if query == "":   # silence
                    eel.ShowHood()  # type: ignore
                    break
                    

                elif "stop listening" in query:
                    speak("Okay, I will stop listening.")
                    eel.ShowHood()  # type: ignore
                    break
                    
                else:
                    # Process the command
                    processCommand(query)
                    
                    
            except Exception as e:
                print("error:", e)
                eel.ShowHood()  # type: ignore
                break
    else:
        # Text mode - single command processing
        query = str(message).strip().lower()
        print(f"Text input received: {query}")
        eel.senderText(query)
        
        if query:
            # Process the command and return to main screen
            processCommand(query)
            eel.ShowHood()  # type: ignore
        else:
            print("Empty message received")
            eel.ShowHood()  # type: ignore

def processCommand(query):
    """Process a single command from either voice or text input"""
    try:
        if query.startswith("open "):
            from engine.features import openCommand
            openCommand(query)

        elif query.startswith("play ") and "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takeCommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query: 
                        speak("what message to send")
                        message = takeCommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("what message to send")
                        query = takeCommand()
                                        
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name)

        elif "weather" in query:
            # Handle weather commands with API
            try:
                from engine.api_examples import handle_weather_command
                handle_weather_command(query)
            except ImportError:
                speak("Weather API feature not available. Please check your configuration.")

        elif "news" in query or "headlines" in query:
            # Handle news commands with API
            try:
                from engine.api_examples import handle_news_command
                handle_news_command(query)
            except ImportError:
                speak("News API feature not available. Please check your configuration.")

        elif "api status" in query or "check apis" in query:
            # Check API configuration status
            try:
                from engine.api_examples import handle_api_status_command
                handle_api_status_command()
            except ImportError:
                speak("API management feature not available.")

        else:
            speak(f"I'm not sure how to handle: {query}")
            print("Command not recognized")
            
    except Exception as e:
        print(f"Error processing command '{query}': {e}")
        speak("Sorry, I encountered an error processing that command.")
