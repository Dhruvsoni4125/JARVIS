<<<<<<< HEAD
# JARVIS
=======
# JARVIS – Voice Assistant  

A Python + JavaScript desktop voice assistant built with **Eel** that supports voice/text commands, system operations, YouTube playback, WhatsApp integration, and more.  

## 🚀 Features
- 🎤 **Voice & Text Commands** – interact using speech recognition or type commands.  
- 🖥️ **System Commands** – open local apps and files.  
- 🌐 **Web Commands** – open websites directly from commands.  
- 🎵 **YouTube Playback** – play songs/videos via voice.  
- 📱 **WhatsApp Integration** – send messages, make calls, start video calls.  
- 🔊 **Text-to-Speech (TTS)** – natural voice responses using `pyttsx3`.  
- 🎧 **Hotword Detection** – wake word support with Porcupine.  
- 💬 **Chat UI** – interactive frontend built with HTML/CSS/JS.  

---

## 📂 Project Structure
```
.
├── run.py              # Entry point (runs JARVIS + hotword listener)
├── main.py             # Initializes eel & starts UI
├── engine/
│   ├── features.py     # Core assistant features (YouTube, WhatsApp, open apps, etc.)
│   ├── command.py      # Voice & text command handling
│   ├── helper.py       # Utility functions (YouTube term extraction, word filtering)
│   └── config.py       # Configuration (assistant name, etc.)
├── controller.js       # Frontend logic (JS, chat rendering, eel bindings)
├── www/                # UI assets (HTML, CSS, audio, etc.)
└── JARVIS.db           # SQLite database for system + web commands & contacts
```

---

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/your-username/jarvis-assistant.git
cd jarvis-assistant
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
python -m venv .venv
source .venv/bin/activate   # On Linux/Mac
.venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Dependencies include:
- `eel`
- `speechrecognition`
- `pyttsx3`
- `pyaudio`
- `playsound`
- `pyautogui`
- `pywhatkit`
- `pvporcupine`

(You may need extra setup for `pyaudio` & `pvporcupine` depending on your OS.)

---

## ▶️ Usage

### Start JARVIS
```bash
python run.py
```

This will:
1. Start the Eel web UI (`localhost:8000`)  
2. Open the assistant in Chrome app window  
3. Begin hotword detection in a parallel process  

### Example Commands
- **"Open YouTube"** → launches YouTube in browser  
- **"Play Believer on YouTube"** → plays the song on YouTube  
- **"Send message to Alex"** → WhatsApp integration  
- **"Stop listening"** → pause command recognition  

---

## 🎯 Roadmap
- [ ] Add Google Calendar & Email integration  
- [ ] Improve NLP command processing  
- [ ] Cross-platform packaging (PyInstaller / Electron wrapper)  

---

## 🤝 Contributing
Pull requests are welcome! Please fork this repo and create a new branch for your feature or bugfix.  

---

## 📜 License
This project is licensed under the MIT License.  
>>>>>>> 1e83922 (Initial commit)
