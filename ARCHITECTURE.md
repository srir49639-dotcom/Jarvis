# 📐 JARVIS Architecture & Code Overview

Complete guide to understanding the Jarvis codebase structure and flow.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     JARVIS AI ASSISTANT                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │   GUI Layer  │────────▶│ Assistant    │                  │
│  │   (gui.py)   │         │  Layer       │                  │
│  └──────────────┘         │ (assistant.py)                  │
│         △                 └──────────────┘                  │
│         │                        │                           │
│         │                        ▼                           │
│         │         ┌──────────────────────────────┐           │
│         │         │   Google Gemini AI API       │           │
│         │         │   Speech Recognition         │           │
│         │         │   Text-to-Speech (pyttsx3)   │           │
│         │         │   System Commands            │           │
│         │         └──────────────────────────────┘           │
│         │                                                     │
│         └─────────────────────────────────────────           │
│                                                               │
│  ┌──────────────┐                                            │
│  │  main.py     │ (Orchestrator & Controller)                │
│  │  - Initialize                                             │
│  │  - Thread Management                                      │
│  │  - Event Handling                                         │
│  └──────────────┘                                            │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 📁 File Structure & Responsibilities

### main.py (Entry Point & Controller)
**Purpose**: Orchestrates the entire application

**Key Classes**:
```python
class JarvisApp:
    - __init__()              # Initialize app components
    - run()                   # Start application
    - voice_listening_thread()# Start voice listening
    - voice_listening_loop()  # Main listening loop for wake word
    - continuous_listening_mode()  # Active listening after wake word
    - process_voice_command() # Process recognized commands
    - on_closing()            # Cleanup on exit
```

**Flow**:
1. Create GUI window
2. Initialize Assistant
3. Start voice listening thread
4. Listen for wake word "Jarvis"
5. Activate continuous listening mode
6. Process commands and send to assistant
7. Update GUI with responses

### gui.py (User Interface)
**Purpose**: Create modern dark neon GUI using CustomTkinter

**Key Classes**:
```python
class JarvisGUI:
    - create_layout()         # Main layout structure
    - create_top_section()    # Title and header
    - create_sidebar()        # Status and quick commands
    - create_chat_area()      # Chat display
    - create_bottom_section() # Input and controls
    - add_message_to_chat()   # Display messages
    - update_status()         # Update status label
```

**UI Components**:
- **Top Section**: Title "◆ JARVIS ◆" with neon styling
- **Left Sidebar**: Status display, quick command buttons, info
- **Main Chat Area**: Scrollable text display with timestamps
- **Bottom Section**: Text input field and send/listen buttons

**Color Scheme**:
- Primary: Cyan (#00d9ff)
- Secondary: Pink (#ff006e)
- Background: Dark (#0a0e27)
- Hover: Dark blue (#1a1f3a)

### assistant.py (Core Logic)
**Purpose**: AI responses, voice processing, command handling

**Key Classes**:
```python
class JarvisAssistant:
    # Initialization & State
    - __init__(status_callback)
    - update_status()         # Callback to update GUI
    - activate_assistant()    # Wake up for listening
    - deactivate_assistant()  # Return to sleep
    
    # Voice I/O
    - listen()                # Speech-to-text
    - speak()                 # Text-to-speech
    - listen_for_wake_word()  # Detect "Jarvis"
    - continuous_listen()     # Keep listening while active
    
    # Command Processing
    - process_command()       # Route commands appropriately
    - get_ai_response()       # Use Gemini API
    
    # System Commands
    - open_application()      # Open Chrome, VS Code, etc.
    - search_google()         # Web search
    - lock_laptop()           # Lock Windows
    - shutdown_laptop()       # Shutdown with 30s delay
    - restart_laptop()        # Restart with 30s delay
    
    # Timer Management
    - reset_inactivity_timer() # Reset 20-second timeout
```

**Global Components**:
```python
tts_engine = pyttsx3.init()         # Text-to-speech
recognizer = sr.Recognizer()        # Speech recognition
gemini_model = genai.GenerativeModel()  # AI API
```

## 🔄 Execution Flow

### Application Startup
```
main.py starts
    ↓
JarvisApp.__init__()
    ├─ Create CTk window (gui.py)
    ├─ Create JarvisAssistant instance
    ├─ Create JarvisGUI instance
    └─ Set event handlers
    ↓
app.run()
    ├─ Start voice_listening_thread (daemon)
    └─ Enter GUI main loop (blocking)
```

### Wake Word Detection Loop
```
voice_listening_loop() runs continuously
    ↓
listen_for_wake_word() (5 second timeout)
    ├─ No audio detected
    │   └─ Try again
    ├─ Audio recognized but not "Jarvis"
    │   └─ Try again
    └─ "Jarvis" detected!
        ↓
        activate_assistant()
        ├─ Set is_active = True
        ├─ Start 20-second inactivity timer
        └─ Speak greeting
        ↓
        continuous_listening_mode()
```

### Active Listening Loop
```
continuous_listening_mode() runs while is_active=True
    ↓
listen() (10 second timeout, captures full sentence)
    ├─ No audio
    │   └─ Continue listening
    └─ Audio captured
        ↓
        reset_inactivity_timer() (restart 20-second countdown)
        ↓
        Add message to GUI
        ↓
        process_voice_command() in separate thread
            ├─ Check for built-in commands
            │   ├─ "open chrome"
            │   ├─ "search..."
            │   ├─ "lock laptop"
            │   └─ etc.
            └─ Or call Gemini API
                ↓
                get_ai_response()
                ├─ Send to Gemini
                ├─ Receive response
                ├─ Add to chat GUI
                └─ Speak response
        ↓
        Return to listening
```

### Inactivity Timeout
```
After 20 seconds with no voice input
    ↓
inactivity_timer triggers
    ↓
deactivate_assistant()
    ├─ Set is_active = False
    └─ Update status to "Sleeping..."
    ↓
Exit continuous_listening_mode()
    ↓
Return to wake_word detection loop
```

## 🎤 Voice Recognition Pipeline

```
Audio Input (Microphone)
    ↓
recognizer.adjust_for_ambient_noise()
    ↓
recognizer.listen(timeout=10, phrase_time_limit=10)
    ├─ Waits up to 10 seconds for audio
    └─ Records up to 10 seconds of speech
    ↓
recognizer.recognize_google(audio)
    ├─ Sends to Google Speech API
    └─ Returns text string
    ↓
Text processing
    └─ Convert to lowercase
    ↓
Return to assistant for processing
```

## 🧠 AI Response Pipeline

```
User command text
    ↓
process_command() analyzes text
    ├─ Check for built-in commands
    │   └─ Execute system command
    └─ No match → call get_ai_response()
        ↓
        gemini_model.generate_content(user_input)
        ├─ Sends to Google Gemini API
        ├─ Receives AI response
        └─ Returns full text (potentially >500 chars)
        ↓
        Limit response to 500 chars for speaking
        ↓
        Add full response to chat
        ↓
        Speak limited response
```

## 🔀 Threading Architecture

**Main Thread**:
- GUI event loop (blocking)
- Handles user interactions
- Updates display elements

**Voice Listening Thread** (daemon):
```
voice_listening_thread()
    ├─ wake_word_detection (continuous)
    ├─ continuous_listening_mode() (when active)
    └─ Never blocks GUI
```

**Command Processing Threads** (daemon):
```
process_voice_command()
    ├─ Check for built-in command
    ├─ Or call get_ai_response()
    └─ Add response to GUI (thread-safe)
```

**Benefits**:
- GUI stays responsive
- Voice listening doesn't freeze UI
- AI API calls don't block listening
- Multiple tasks run simultaneously

## 🛠️ Command Processing Logic

### Built-in Commands (Hard-coded)

```
"open chrome" → subprocess.Popen(chrome_path)
"open youtube" → webbrowser.open("https://youtube.com")
"search [query]" → webbrowser.open("google.com/search?q=...")
"what is the time" → Get current time, speak it
"lock laptop" → os.system("rundll32.exe user32.dll,LockWorkStation")
"shutdown" → os.system("shutdown /s /t 30")
"restart" → os.system("shutdown /r /t 30")
```

### AI-Powered Commands

```
Anything else → Send to Gemini API
    ↓
gemini_model.generate_content(command)
    ↓
Return natural language response
```

## 🔌 API Integration

### Google Gemini API

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(user_input)
answer = response.text
```

**Requirements**:
- Active internet connection
- Valid API key
- Free tier available at https://aistudio.google.com

### Google Speech Recognition API

```python
import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    audio = recognizer.listen(source)
    text = recognizer.recognize_google(audio)
```

**Requirements**:
- Microphone connected
- Internet connection
- Free to use

## 🎯 Key Design Patterns

### 1. **Observer Pattern**
- GUI registers callback with Assistant
- Assistant calls callback to update status
- Loose coupling between GUI and logic

### 2. **Command Pattern**
- Voice command → Command object
- Process based on command type
- Easy to add new commands

### 3. **Strategy Pattern**
- Built-in commands vs AI responses
- Different processing strategies
- Selected at runtime

### 4. **Singleton Pattern** (implicit)
- Single AssistantInstance
- Single GUI instance
- Centralized state management

## 🔧 Configuration Points

**In assistant.py**:
```python
# Wake word
self.wake_word = "jarvis"

# Inactivity timeout
self.inactivity_timeout = 20

# Speech rate
tts_engine.setProperty('rate', 150)

# Audio threshold
recognizer.energy_threshold = 4000

# Gemini API key
genai.configure(api_key="YOUR_KEY")
```

**In gui.py**:
```python
# Colors
self.primary_color = "#00d9ff"
self.secondary_color = "#ff006e"
self.bg_color = "#0a0e27"

# Window size
self.root.geometry("1000x700")
```

## 📊 Data Flow Summary

```
User says "Jarvis"
    ↓
Wake word detected
    ↓
Assistant activates
    ↓
GUI shows "Listening..."
    ↓
User says command
    ↓
Speech-to-text converts to text
    ↓
Process command logic decides route
    ├─ Built-in → Execute immediately
    └─ General → Send to Gemini
    ↓
Get response (speech + text)
    ↓
Add to chat history
    ↓
Speak response
    ↓
Return to listening
```

## 🚀 Performance Considerations

1. **Threading**: All blocking operations in separate threads
2. **Timeouts**: Prevent infinite waiting
3. **Caching**: Could cache common queries
4. **API Calls**: Depend on internet speed
5. **GUI Updates**: Safe from separate threads

## 🔐 Security Considerations

1. **API Key**: Never hardcode in production
2. **Microphone Access**: Requires user permission
3. **System Commands**: Only safe operations allowed
4. **Input Validation**: Text from speech recognition
5. **Error Handling**: Graceful failure modes

---

**Understanding this architecture helps with**:
- Debugging issues
- Adding new commands
- Customizing behavior
- Scaling the project
- Contributing improvements

