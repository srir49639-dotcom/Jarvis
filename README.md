# 🤖 JARVIS - Terminal-based AI Voice Assistant

A powerful, terminal-based AI voice assistant with voice recognition, natural speech output, and intelligent AI responses powered by Google Gemini.

## 🌟 Features

- **🎤 Voice Recognition**: Say "Jarvis" to wake up the assistant
- **🧠 AI Chat**: Powered by Google Gemini API for intelligent responses
- **🔊 Text-to-Speech**: Natural voice output with pyttsx3
- **🖥️ System Commands**: Open applications, control laptop (lock, shutdown, restart, sleep)
- **🌐 Web Integration**: Open websites, search Google
- **⏰ Utilities**: Tell time and date
- **🎯 Continuous Listening**: 20-second active listening window after wake word
- **😴 Auto Sleep**: Returns to sleep mode after inactivity
- **💬 Terminal Interface**: Clean, simple terminal-based UI with status messages

## 📋 Requirements

- Python 3.8 or higher
- Microphone connected to your computer
- Internet connection
- Google Gemini API key (free)

## 🚀 Installation

### 1. Navigate to Project Directory

```bash
cd c:\Users\sriram\OneDrive\Desktop\jarvis
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: If you encounter PyAudio issues on Windows:

```bash
pip install pipwin
pipwin install pyaudio
```

### 3. Get Gemini API Key

1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy your new API key
4. Open `main.py` and find line 22
5. Replace `YOUR_API_KEY_HERE` with your actual API key

### 4. Run the Application

```bash
python main.py
```

## 🎤 Voice Commands

### System Commands

```
"open chrome"           → Open Chrome browser
"open youtube"          → Open YouTube
"open google"           → Open Google Search
"open vscode"           → Open Visual Studio Code
"open calculator"       → Open Calculator
"open notepad"          → Open Notepad
```

### Web & Search

```
"search [anything]"     → Search Google for anything
"search python"         → Search for Python tutorials
```

### Information

```
"what is the time"      → Current time
"what is the date"      → Current date
```

### System Control

```
"lock laptop"           → Lock your computer
"shutdown laptop"       → Shutdown in 30 seconds
"restart laptop"        → Restart in 30 seconds
"sleep laptop"          → Put computer to sleep
"stop jarvis"           → Stop the assistant
```

### AI Chat

```
"tell me a joke"
"what is machine learning"
"how do I learn Python"
"who is Albert Einstein"
"write a poem about technology"
```

## 🔄 How It Works

1. **Run** the application with `python main.py`
2. **Listen** for "Sleeping..." message (assistant waits for wake word)
3. **Say "JARVIS"** to activate the assistant
4. **Listen** for confirmation message
5. **Give commands** - you have 20 seconds of active listening
6. **Respond** - Jarvis will execute your command or use AI to answer
7. **Return to sleep** automatically after 20 seconds of silence

## ✅ Status Messages

| Symbol | Status | Meaning |
|--------|--------|---------|
| 🎤 | LISTENING | Waiting for voice input |
| 💭 | THINKING | Processing your command |
| 🤖 | RESPONSE | Jarvis is responding |
| ✅ | SUCCESS | Command executed successfully |
| ❌ | ERROR | An error occurred |
| ⚡ | COMMAND | You said a command |

## 📝 Code Structure

The complete application is in `main.py` with the following sections:

- **Configuration**: API and engine setup
- **Utility Functions**: Status printing, speaking, listening
- **Command Execution**: Opening apps, searching, system control
- **AI Response**: Gemini API integration
- **Command Processing**: Route commands to appropriate handlers
- **Listening Loops**: Wake word detection and continuous listening
- **Main Application**: Entry point and initialization

## 🛠️ Configuration

All settings are in `main.py`:

```python
# Change wake word
wake_word = "jarvis"  # Change to any word

# Adjust active listening time
inactivity_timeout = 20  # Seconds

# Change speech rate
engine.setProperty('rate', 150)  # 100-300, lower=slower, higher=faster

# Adjust microphone sensitivity
recognizer.energy_threshold = 4000  # Higher=less sensitive
```

## 🔐 API Setup

### Google Gemini API

**Free tier includes:**
- 60 requests per minute
- 10,000+ requests per month
- All features
- No credit card required

**Setup:**
1. Visit: https://aistudio.google.com/app/apikey
2. Create new API key
3. Add to `main.py` line 22
4. Done!

## 🐛 Troubleshooting

### Microphone not working
- Check Windows Sound Settings
- Test microphone in other applications
- Ensure microphone is not muted

### "I didn't understand that"
- Speak louder and clearer
- Reduce background noise
- Try again

### API key error
- Verify API key is copied correctly
- Check internet connection
- Ensure key is active at https://aistudio.google.com/app/apikey

### No sound output
- Check Windows volume is not muted
- Test speakers with other applications
- Verify pyttsx3 installation: `pip install --upgrade pyttsx3`

### PyAudio issues
```bash
pip install pipwin
pipwin install pyaudio
```

## 📊 Requirements

| Package | Version | Purpose |
|---------|---------|---------|
| SpeechRecognition | 3.10.0 | Voice-to-text |
| pyttsx3 | 2.90 | Text-to-speech |
| pyaudio | 0.2.13 | Microphone access |
| google-generativeai | 0.3.0 | Gemini API |

## 💡 Tips for Best Experience

1. Use in a quiet environment for better recognition
2. Speak clearly and naturally
3. Keep sentences simple
4. Have stable internet connection
5. Ensure microphone is properly configured
6. Wait for "Listening..." before speaking

## 🎓 Learning Value

This project teaches:
- Voice processing and speech recognition
- AI API integration
- System programming
- Threading and async operations
- Clean Python code practices

## 📞 Support

For issues:
1. Check the Troubleshooting section above
2. Verify API key is configured
3. Check console output for error messages
4. Ensure all dependencies are installed

## 🚀 Quick Start Summary

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Get API key from https://aistudio.google.com/app/apikey
# 3. Edit main.py line 22 with your API key

# 4. Run application
python main.py

# 5. Say "Jarvis" to activate
# 6. Give your command!
```

---

**Enjoy your powerful terminal-based AI assistant! 🚀**

