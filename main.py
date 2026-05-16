"""
JARVIS - Terminal-based AI Voice Assistant
A powerful voice-controlled assistant with AI capabilities
Features: Voice recognition, Gemini AI, system commands, terminal interface
"""

import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import threading
import webbrowser
import subprocess
import os
import time
import datetime
import ctypes
import sys
from typing import Optional

# ==================== CONFIGURATION ====================

# Configure Google Gemini API - REPLACE WITH YOUR KEY
genai.configure(api_key="AIzaSyC3awtol_VX3Md2d-kL9z2XH1JAOOpJpW8")

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 200)  # Speech speed (100-300, increased for faster response)
engine.setProperty('volume', 0.9)  # Volume level (0-1)

# Initialize speech recognizer
recognizer = sr.Recognizer()
recognizer.energy_threshold = 4000  # Microphone sensitivity

# ==================== GLOBAL VARIABLES ====================

is_listening = False  # Flag for continuous listening
is_active = False  # Flag for being awake
inactivity_timer = None  # Timer for auto-sleep
wake_word = "jarvis"  # Wake word to activate
inactivity_timeout = 15  # Seconds to stay active (reduced for faster sleep)


# ==================== UTILITY FUNCTIONS ====================

def print_status(message: str, status_type: str = "INFO") -> None:
    """
    Print formatted status messages to terminal
    
    Args:
        message: The message to print
        status_type: Type of message (INFO, LISTENING, THINKING, ERROR, SUCCESS)
    """
    status_symbols = {
        "INFO": "ℹ️ ",
        "LISTENING": "🎤 ",
        "THINKING": "💭 ",
        "ERROR": "❌ ",
        "SUCCESS": "✅ ",
        "COMMAND": "⚡ ",
        "RESPONSE": "🤖 "
    }
    
    symbol = status_symbols.get(status_type, "▸ ")
    print(f"{symbol} [{status_type}] {message}")


def speak(text: str) -> None:
    """
    Convert text to speech using pyttsx3
    
    Args:
        text: The text to speak
    """
    try:
        print_status("Speaking...", "RESPONSE")
        engine.say(text)
        engine.runAndWait()
        print_status("Ready to listen", "LISTENING")
    except Exception as e:
        print_status(f"Text-to-speech error: {e}", "ERROR")


def listen() -> Optional[str]:
    """
    Listen for voice input and convert to text
    
    Returns:
        Recognized text or None if recognition failed
    """
    try:
        print_status("Listening for your command...", "LISTENING")
        
        with sr.Microphone() as source:
            # Adjust for ambient noise (fast detection)
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            
            # Listen for up to 6 seconds with 6 second phrase limit (optimized for speed)
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=6)
        
        print_status("Processing audio...", "THINKING")
        text = recognizer.recognize_google(audio)
        text = text.lower()
        
        print_status(f"You said: {text}", "COMMAND")
        return text
    
    except sr.UnknownValueError:
        print_status("Didn't catch that, please repeat", "INFO")
        return None
    except sr.RequestError as e:
        print_status(f"Could not request results; check internet: {e}", "ERROR")
        return None
    except sr.WaitTimeoutError:
        print_status("No speech detected (timeout)", "INFO")
        return None
    except Exception as e:
        print_status(f"Microphone error: {e}", "ERROR")
        return None


def listen_for_wake_word() -> bool:
    """
    Listen for wake word "Jarvis"
    
    Returns:
        True if wake word detected, False otherwise
    """
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            # Fast timeout for wake word detection (optimized)
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
        
        text = recognizer.recognize_google(audio).lower()
        return wake_word in text
    
    except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
        return False
    except Exception as e:
        print_status(f"Wake word listening error: {e}", "ERROR")
        return False


def reset_inactivity_timer() -> None:
    """Reset the inactivity timer (auto-sleep after 20 seconds)"""
    global inactivity_timer, is_active
    
    # Cancel existing timer if any
    if inactivity_timer:
        inactivity_timer.cancel()
    
    # Create new timer
    inactivity_timer = threading.Timer(inactivity_timeout, deactivate_assistant)
    inactivity_timer.daemon = True
    inactivity_timer.start()
    
    print_status(f"Active listening for {inactivity_timeout} seconds", "LISTENING")


def activate_assistant() -> None:
    """Activate the assistant for continuous listening"""
    global is_active, is_listening
    
    is_active = True
    is_listening = True
    
    print_status("🎉 Waking up...", "SUCCESS")
    speak("Hello! I'm awake. How can I help you?")
    reset_inactivity_timer()


def deactivate_assistant() -> None:
    """Deactivate assistant and return to sleep"""
    global is_active
    
    is_active = False
    print_status("Sleeping... Say 'Jarvis' to wake me up", "INFO")
    speak("Going to sleep. Wake me up anytime.")


# ==================== COMMAND EXECUTION ====================

def open_application(app_name: str, url: Optional[str] = None) -> None:
    """
    Open an application or website
    
    Args:
        app_name: Name of application
        url: Optional URL to open in browser
    """
    try:
        if url:
            # Open URL in default browser
            webbrowser.open(url)
            print_status(f"Opening {url}", "SUCCESS")
        else:
            # Windows application paths
            apps = {
                "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                "code": "C:\\Users\\sriram\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
                "notepad": "notepad.exe",
                "calc": "calc.exe",
                "calculator": "calc.exe",
            }
            
            path = apps.get(app_name.lower())
            if path:
                subprocess.Popen(path)
                print_status(f"Opening {app_name}", "SUCCESS")
                speak(f"Opening {app_name}")
            else:
                print_status(f"Application '{app_name}' not found", "ERROR")
                speak(f"I don't know how to open {app_name}")
    
    except Exception as e:
        print_status(f"Error opening {app_name}: {e}", "ERROR")
        speak(f"Could not open {app_name}")


def search_google(query: str) -> None:
    """
    Search Google for a query
    
    Args:
        query: Search query string
    """
    try:
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        print_status(f"Searching for: {query}", "SUCCESS")
        speak(f"Searching Google for {query}")
    except Exception as e:
        print_status(f"Search error: {e}", "ERROR")


def get_current_time() -> None:
    """Get and speak current time"""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    message = f"The time is {current_time}"
    print_status(message, "RESPONSE")
    speak(message)


def get_current_date() -> None:
    """Get and speak current date"""
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    message = f"Today is {current_date}"
    print_status(message, "RESPONSE")
    speak(message)


def lock_laptop() -> None:
    """Lock the laptop using Windows API"""
    try:
        print_status("Locking laptop...", "COMMAND")
        speak("Locking your laptop")
        ctypes.windll.user32.LockWorkStation()
    except Exception as e:
        print_status(f"Lock error: {e}", "ERROR")
        speak("Could not lock laptop")


def shutdown_laptop() -> None:
    """Shutdown laptop with 30 second delay"""
    try:
        print_status("Shutting down in 30 seconds...", "COMMAND")
        speak("Shutting down your laptop in 30 seconds")
        os.system("shutdown /s /t 30")
    except Exception as e:
        print_status(f"Shutdown error: {e}", "ERROR")
        speak("Could not shutdown laptop")


def restart_laptop() -> None:
    """Restart laptop with 30 second delay"""
    try:
        print_status("Restarting in 30 seconds...", "COMMAND")
        speak("Restarting your laptop in 30 seconds")
        os.system("shutdown /r /t 30")
    except Exception as e:
        print_status(f"Restart error: {e}", "ERROR")
        speak("Could not restart laptop")


def sleep_laptop() -> None:
    """Put laptop into sleep mode"""
    try:
        print_status("Putting laptop to sleep...", "COMMAND")
        speak("Putting laptop to sleep")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    except Exception as e:
        print_status(f"Sleep error: {e}", "ERROR")
        speak("Could not put laptop to sleep")


# ==================== AI RESPONSE ====================

def get_ai_response(user_input: str) -> None:
    """
    Get response from Google Gemini AI
    
    Args:
        user_input: User's question or statement
    """
    try:
        print_status("Thinking...", "THINKING")
        
        # Create model and generate response
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_input)
        ai_response = response.text
        
        # Print response
        print_status(f"Jarvis: {ai_response}", "RESPONSE")
        
        # Speak response (limit to first 500 chars to avoid long speaking)
        speak_text = ai_response[:500] if len(ai_response) > 500 else ai_response
        speak(speak_text)
    
    except Exception as e:
        error_msg = str(e)
        
        if "API_KEY" in error_msg or "api_key" in error_msg:
            print_status("API key not configured. Set it in main.py line 22", "ERROR")
            speak("Please configure your Gemini API key")
        else:
            print_status(f"AI error: {e}", "ERROR")
            speak("Sorry, I encountered an error getting a response")


# ==================== COMMAND PROCESSING ====================

def process_command(command: str) -> None:
    """
    Process voice command and execute appropriate action
    
    Args:
        command: The recognized voice command
    """
    command = command.lower().strip()
    
    # OPEN APPLICATIONS
    if "open chrome" in command:
        open_application("chrome")
    
    elif "open youtube" in command:
        open_application("chrome", "https://www.youtube.com")
    
    elif "open google" in command:
        open_application("chrome", "https://www.google.com")
    
    elif "open vscode" in command or "open vs code" in command:
        open_application("code")
    
    elif "open calculator" in command or "open calc" in command:
        open_application("calc")
    
    elif "open notepad" in command:
        open_application("notepad")
    
    # SEARCH
    elif "search" in command:
        query = command.replace("search", "").strip()
        if query:
            search_google(query)
        else:
            speak("What would you like me to search for?")
    
    # TIME AND DATE
    elif "what is the time" in command or "current time" in command or "what time" in command:
        get_current_time()
    
    elif "what is the date" in command or "current date" in command or "what date" in command:
        get_current_date()
    
    # SYSTEM CONTROL
    elif "lock" in command or "lock laptop" in command or "lock screen" in command:
        lock_laptop()
    
    elif "shutdown" in command or "shut down" in command:
        shutdown_laptop()
    
    elif "restart" in command or "reboot" in command:
        restart_laptop()
    
    elif "sleep" in command or "sleep mode" in command:
        sleep_laptop()
    
    # STOP COMMAND
    elif "stop" in command or "stop jarvis" in command or "goodbye" in command:
        print_status("Stopping Jarvis...", "INFO")
        speak("Goodbye! Thanks for using me.")
        sys.exit(0)
    
    # DEFAULT - USE AI
    else:
        get_ai_response(command)


# ==================== MAIN LISTENING LOOPS ====================

def wake_word_detection_loop() -> None:
    """
    Continuously listen for wake word "Jarvis"
    This runs when the assistant is in sleep mode
    """
    global is_active, is_listening
    
    print_status("Waiting for wake word 'Jarvis'...", "LISTENING")
    
    while is_listening:
        try:
            if listen_for_wake_word():
                print_status("Wake word detected!", "SUCCESS")
                activate_assistant()
                continuous_listening_loop()
            
            time.sleep(0.2)  # Faster loop (reduced from 0.5)
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print_status(f"Wake word detection error: {e}", "ERROR")
            time.sleep(0.2)  # Faster retry


def continuous_listening_loop() -> None:
    """
    Continuously listen for commands while assistant is active
    Runs for 20 seconds after wake word or until inactivity timeout
    """
    global is_active
    
    while is_active and is_listening:
        try:
            command = listen()
            
            if command:
                # Reset inactivity timer (stay awake for another 20 seconds)
                reset_inactivity_timer()
                
                # Process command in separate thread to keep listening responsive
                threading.Thread(
                    target=process_command,
                    args=(command,),
                    daemon=True
                ).start()
            
            time.sleep(0.2)  # Faster loop (reduced from 0.5)
        
        except Exception as e:
            print_status(f"Listening error: {e}", "ERROR")
            time.sleep(0.3)  # Faster retry (reduced from 1)


# ==================== MAIN APPLICATION ====================

def print_welcome():
    """Print welcome banner"""
    print("\n" + "="*50)
    print("   🤖 JARVIS - AI VOICE ASSISTANT 🤖   ")
    print("="*50)
    print("\n📋 Commands Available:")
    print("  • Open Applications: 'open chrome', 'open vscode', etc.")
    print("  • Web Search: 'search [anything]'")
    print("  • Info: 'what is the time', 'what is the date'")
    print("  • System: 'lock laptop', 'shutdown', 'restart', 'sleep'")
    print("  • Stop: Say 'stop jarvis' to exit")
    print("  • AI Chat: Ask anything else!\n")
    print("🎤 Say 'JARVIS' to activate the assistant")
    print("⏰ You have 20 seconds of active listening\n")
    print("="*50 + "\n")


def main():
    """Main application entry point"""
    global is_listening
    
    try:
        # Print welcome message
        print_welcome()
        
        # Check if API key is configured
        try:
            test_model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            print_status("WARNING: Gemini API key not configured!", "ERROR")
            print_status("Set your API key in main.py line 22", "ERROR")
            print_status("Get free key at: https://aistudio.google.com/app/apikey\n", "INFO")
        
        # Start listening for wake word
        is_listening = True
        print_status("Jarvis started. Listening for wake word...", "SUCCESS")
        
        # Run wake word detection loop
        wake_word_detection_loop()
    
    except KeyboardInterrupt:
        print_status("\nJarvis shutting down...", "INFO")
        is_listening = False
        speak("Goodbye!")
        sys.exit(0)
    
    except Exception as e:
        print_status(f"Fatal error: {e}", "ERROR")
        sys.exit(1)


if __name__ == "__main__":
    main()

# -----------------------------------
# SHUTDOWN PC
# -----------------------------------

def shutdown_pc():

    speak("Shutting down your laptop")

    os.system("shutdown /s /t 5")

# -----------------------------------
# RESTART PC
# -----------------------------------

def restart_pc():

    speak("Restarting your laptop")

    os.system("shutdown /r /t 5")

# -----------------------------------
# SLEEP PC
# -----------------------------------

def sleep_pc():

    speak("Putting laptop to sleep")

    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

# -----------------------------------
# COMMAND HANDLER
# -----------------------------------

def run_command(command):

    # OPEN WEBSITES
    if "open youtube" in command:

        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")

    elif "open google" in command:

        webbrowser.open("https://google.com")
        speak("Opening Google")

    # OPEN APPS
    elif "open chrome" in command:

        os.startfile(
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        )

        speak("Opening Chrome")

    elif "open notepad" in command:

        os.system("notepad")
        speak("Opening Notepad")

    elif "open calculator" in command:

        os.system("calc")
        speak("Opening Calculator")

    elif "open vscode" in command or "open vs code" in command:

        os.startfile(
            "C:\\Users\\sriram\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        )

        speak("Opening VS Code")

    # TIME
    elif "time" in command:

        current_time = datetime.datetime.now().strftime("%I:%M %p")

        speak(f"The time is {current_time}")

    # SEARCH
    elif "search" in command:

        query = command.replace("search", "")

        webbrowser.open(
            f"https://www.google.com/search?q={query}"
        )

        speak(f"Searching for {query}")

    # LOCK LAPTOP
    elif "lock laptop" in command or "lock pc" in command:

        lock_pc()

    # SHUTDOWN
    elif "shutdown laptop" in command or "shutdown pc" in command:

        shutdown_pc()

    # RESTART
    elif "restart laptop" in command or "restart pc" in command:

        restart_pc()

    # SLEEP
    elif "sleep laptop" in command:

        sleep_pc()

    # STOP ASSISTANT
    elif "stop jarvis" in command or "exit" in command:

        speak("Goodbye")
        exit()

    # AI CHAT
    else:

        ask_ai(command)

# -----------------------------------
# MAIN PROGRAM
# -----------------------------------

speak("Jarvis is online")

active_mode = False
last_command_time = 0

while True:

    # Wake word needed only once
    if not active_mode:

        print("\nWaiting for wake word...")

        text = listen()

        if "jarvis" in text:

            active_mode = True

            speak("I am listening")

            last_command_time = time.time()

    # Continuous listening mode
    else:

        command = listen()

        if command != "":

            last_command_time = time.time()

            run_command(command)

        # Auto sleep after inactivity
        if time.time() - last_command_time > 20:

            active_mode = False

            speak("Going back to sleep")