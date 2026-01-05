from urllib.parse import quote
import struct
import subprocess
import time
from playsound import playsound
import eel
import pvporcupine
import pyaudio
import pyautogui
from engine.config import ASSISTANT_NAME
import os
from engine.command import speak
import pywhatkit as kit
import webbrowser
import sqlite3
import re

from engine.helper import extract_yt_term, remove_words
#Playing Assitant Sound 

conn= sqlite3.connect('JARVIS.db')
cursor= conn.cursor()


@eel.expose

def playAssistantSound():
    music_dir= "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)


def openCommand(query):
    # Use regex to find what to open, e.g., "open google" -> "google"
    match = re.search(r'open\s+(.*)', query, re.IGNORECASE)
    if not match:
        speak("I'm not sure what you want me to open.")
        return

    app_name = match.group(1).strip().lower()

    if app_name != "":
        try:
            # First, check for a system command (local application)
            cursor.execute(
                'SELECT path FROM sys_command WHERE LOWER(name) = ?', (app_name.lower(),))
            sys_results = cursor.fetchone() # Use fetchone() as name should be unique

            if sys_results:
                speak("Opening "+ app_name)
                os.startfile(sys_results[0])
                return

            # If not a system command, check for a web command
            cursor.execute(
                'SELECT url FROM web_command WHERE LOWER(name)  = ?', (app_name.lower(),))
            web_results = cursor.fetchone()

            if web_results:
                speak("Opening "+ app_name)
                webbrowser.open(web_results[0])
                return

            # If not found in DB, try to open it directly as a fallback
            speak(f"I couldn't find {app_name} in my database, but I'll try to open it.")
            os.system(f'start {app_name}')

        except Exception as e:
            print(f"Error in openCommand: {e}")
            speak("Sorry, something went wrong while trying to open that.")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak(f"Playing {search_term} on YouTube")
    try:
        # Try using pywhatkit's playonyt function
        kit.playonyt(search_term)
    except AttributeError:
        # Fallback to manual YouTube search
        search_url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
        webbrowser.open(search_url)
    except Exception as e:
        print(f"YouTube error: {e}")
        speak("Sorry, I couldn't play that on YouTube")

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=[ASSISTANT_NAME]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


#find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0


def whatsApp(mobile_no, message, flag, name):
    """Send WhatsApp message, make call, or start video call"""
    
    try:
        if flag == 'call':
            # Handle phone call
            whatsapp_url = f"whatsapp://call?phone={mobile_no}"
            subprocess.run(f'start "" "{whatsapp_url}"', shell=True)
            jarvis_message = f"Calling {name} on WhatsApp"
            speak(jarvis_message)
            return
            
        elif flag == 'video call':
            # Handle video call - try to open WhatsApp and initiate video call
            whatsapp_url = f"whatsapp://send?phone={mobile_no}"
            subprocess.run(f'start "" "{whatsapp_url}"', shell=True)
            time.sleep(3)
            # Video call option is usually accessible via Ctrl+Shift+V in WhatsApp Desktop
            # But we'll just open the chat and let user initiate manually
            jarvis_message = f"Opening chat with {name} for video call"
            speak(jarvis_message)
            return
            
        elif flag == 'message':
            # Handle message sending using web WhatsApp approach
            if message and message.strip():
                try:
                    # Use web-based approach - more reliable
                    import webbrowser
                    encoded_message = quote(message)
                    whatsapp_web_url = f"https://web.whatsapp.com/send?phone={mobile_no}&text={encoded_message}"
                    
                    # Open WhatsApp Web
                    webbrowser.open(whatsapp_web_url)
                    
                    # Give time for page to load
                    time.sleep(5)
                    
                    # Try to click and send (more reliable than complex tab navigation)
                    try:
                        # Click in the center of screen to focus, then send
                        pyautogui.click(pyautogui.size()[0] // 2, pyautogui.size()[1] // 2)
                        time.sleep(2)
                        pyautogui.press('enter')
                        jarvis_message = f"Message sent successfully to {name}"
                    except Exception as gui_error:
                        print(f"GUI automation error: {gui_error}")
                        jarvis_message = f"WhatsApp Web opened for {name}. Please send the message manually."
                    
                    speak(jarvis_message)
                    
                except Exception as web_error:
                    print(f"Web WhatsApp error: {web_error}")
                    # Fallback to desktop app URL method
                    encoded_message = quote(message)
                    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
                    subprocess.run(f'start "" "{whatsapp_url}"', shell=True)
                    
                    # Simple automation - just press enter after a delay
                    time.sleep(3)
                    try:
                        pyautogui.press('enter')
                        jarvis_message = f"Message sent to {name}"
                    except:
                        jarvis_message = f"WhatsApp opened for {name}. Please send the message manually."
                    speak(jarvis_message)
            else:
                speak("No message to send")
                return
        else:
            speak("Invalid WhatsApp operation")
            return
            
    except Exception as e:
        print(f"WhatsApp error: {e}")
        speak(f"Sorry, I couldn't complete the WhatsApp operation for {name}. Please make sure WhatsApp is installed.")