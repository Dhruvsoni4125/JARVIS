import os
import eel
from engine.features import *
from engine.command import *
 
def start():
    eel.init('www')

    playAssistantSound()



    os.system('start chrome.exe --app="http://localhost:8000"')
    eel.start('index.html', mode=None, port=8000)  # You can change 'chrome-app' to your preferred browser