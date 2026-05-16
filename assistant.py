"""
Assistant Module - Handles AI, Voice Input/Output, and Command Processing
This module manages all the core functionality of the Jarvis assistant
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
from typing import Callable, Optional
import platform

# Configure Google Gemini API (Replace with your API key)
genai.configure(api_key="AIzaSyC4KDqHTfcucww4oVU1x7stDxxfEBy75KE")

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Speech rate
tts_engine.setProperty('volume', 0.9)  # Volume level

# Initialize speech recognizer
recognizer = sr.Recognizer()
recognizer.energy_threshold = 4000  # Adjust for background noise

# Initialize Gemini model
gemini_model = genai.GenerativeModel('gemini-pro')


class JarvisAssistant:
    """Main Assistant Class - Handles all AI and command operations"""
    
    def __init__(self, status_callback: Optional[Callable] = None):
        """
        Initialize the Jarvis Assistant
        
        Args:
            status_callback: Function to update GUI status label
        """
        self.status_callback = status_callback
        self.listening = False
        self.is_active = False
        self.wake_word = "jarvis"
        self.inactivity_timer = None
        self.inactivity_timeout = 20  # Seconds to stay active after wake word
        
    def update_status(self, message: str) -> None:
        """Update the status label in the GUI"""
        if self.status_callback:
            self.status_callback(message)
    
    def speak(self, text: str) -> None:
        """
        Convert text to speech
        
        Args:
            text: Text to speak
        """
        try:
            self.update_status("Speaking...")
            tts_engine.say(text)
            tts_engine.runAndWait()
            self.update_status("Listening..." if self.is_active else "Sleeping...")
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
            self.update_status("Error: TTS Failed")
    
    def listen(self) -> Optional[str]:
        """
        Listen for voice input and convert to text
        
        Returns:
            Transcribed text or None if listening failed
        """
        try:
            self.update_status("Listening...")
            with sr.Microphone() as source:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen with timeout of 10 seconds
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                
            self.update_status("Processing...")
            text = recognizer.recognize_google(audio)
            return text.lower()
        
        except sr.UnknownValueError:
            self.update_status("Sorry, I didn't understand that")
            return None
        except sr.RequestError:
            self.update_status("Error: Microphone or internet issue")
            return None
        except Exception as e:
            print(f"Error in listening: {e}")
            self.update_status("Error: Listening Failed")
            return None
    
    def reset_inactivity_timer(self) -> None:
        """Reset the inactivity timer"""
        if self.inactivity_timer:
            self.inactivity_timer.cancel()
        
        self.inactivity_timer = threading.Timer(
            self.inactivity_timeout,
            self.deactivate_assistant
        )
        self.inactivity_timer.daemon = True
        self.inactivity_timer.start()
    
    def activate_assistant(self) -> None:
        """Activate the assistant for continuous listening"""
        self.is_active = True
        self.update_status("Listening...")
        self.reset_inactivity_timer()
    
    def deactivate_assistant(self) -> None:
        """Deactivate the assistant and return to sleep mode"""
        self.is_active = False
        self.update_status("Sleeping...")
    
    def process_command(self, command: str, callback: Optional[Callable] = None) -> None:
        """
        Process voice commands and execute appropriate actions
        
        Args:
            command: The command text to process
            callback: Function to add messages to chat history
        """
        command = command.lower().strip()
        
        if callback:
            callback("You", command)
        
        # Open Applications
        if "open chrome" in command:
            self.open_application("chrome")
            self.speak("Opening Chrome")
        
        elif "open google" in command:
            self.open_application("chrome", "https://www.google.com")
            self.speak("Opening Google")
        
        elif "open youtube" in command:
            self.open_application("chrome", "https://www.youtube.com")
            self.speak("Opening YouTube")
        
        elif "open vscode" in command or "open vs code" in command:
            self.open_application("code")
            self.speak("Opening Visual Studio Code")
        
        elif "open calculator" in command or "open calc" in command:
            self.open_application("calc")
            self.speak("Opening Calculator")
        
        elif "open notepad" in command:
            self.open_application("notepad")
            self.speak("Opening Notepad")
        
        # Search Commands
        elif "search" in command:
            search_query = command.replace("search", "").strip()
            if search_query:
                self.search_google(search_query)
                self.speak(f"Searching for {search_query}")
            else:
                self.speak("What would you like me to search for?")
        
        # Time and Date
        elif "what is the time" in command or "current time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {current_time}")
            if callback:
                callback("Jarvis", f"The time is {current_time}")
        
        elif "what is the date" in command or "current date" in command:
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            self.speak(f"Today is {current_date}")
            if callback:
                callback("Jarvis", f"Today is {current_date}")
        
        # System Commands
        elif "lock laptop" in command or "lock screen" in command or "lock" in command:
            self.lock_laptop()
            self.speak("Locking your laptop")
        
        elif "shutdown laptop" in command or "shutdown" in command:
            self.speak("Shutting down your laptop in 30 seconds")
            self.shutdown_laptop()
        
        elif "restart laptop" in command or "restart" in command:
            self.speak("Restarting your laptop in 30 seconds")
            self.restart_laptop()
        
        # AI Chat (using Gemini)
        else:
            self.get_ai_response(command, callback)
    
    def get_ai_response(self, user_input: str, callback: Optional[Callable] = None) -> None:
        """
        Get AI response from Google Gemini
        
        Args:
            user_input: User's input text
            callback: Function to add messages to chat history
        """
        try:
            self.update_status("Thinking...")
            
            # Generate response from Gemini
            response = gemini_model.generate_content(user_input)
            ai_response = response.text
            
            # Limit response length for speaking
            speak_response = ai_response[:500] if len(ai_response) > 500 else ai_response
            
            if callback:
                callback("Jarvis", ai_response)
            
            self.speak(speak_response)
            
        except Exception as e:
            error_msg = f"Error getting AI response: {str(e)}"
            print(error_msg)
            if "API_KEY" in str(e) or "api_key" in str(e):
                error_msg = "Please configure your Gemini API key in assistant.py"
            if callback:
                callback("Jarvis", error_msg)
            self.speak("Sorry, I encountered an error getting an AI response")
            self.update_status("Error: AI Response Failed")
    
    def open_application(self, app_name: str, url: Optional[str] = None) -> None:
        """
        Open an application
        
        Args:
            app_name: Name of the application to open
            url: Optional URL to open (for browsers)
        """
        try:
            system = platform.system()
            
            if url:
                # Open URL in default browser
                webbrowser.open(url)
            else:
                if system == "Windows":
                    # Common Windows applications
                    apps = {
                        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                        "code": "C:\\Users\\sriram\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
                        "notepad": "notepad.exe",
                        "calc": "calc.exe",
                        "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                    }
                    
                    if app_name in apps:
                        subprocess.Popen(apps[app_name])
                    else:
                        # Try to run it directly
                        subprocess.Popen(app_name)
        
        except Exception as e:
            print(f"Error opening application: {e}")
            self.speak(f"Could not open {app_name}")
    
    def search_google(self, query: str) -> None:
        """
        Search Google for a query
        
        Args:
            query: Search query string
        """
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
        except Exception as e:
            print(f"Error searching Google: {e}")
    
    def lock_laptop(self) -> None:
        """Lock the laptop"""
        try:
            if platform.system() == "Windows":
                os.system("rundll32.exe user32.dll,LockWorkStation")
        except Exception as e:
            print(f"Error locking laptop: {e}")
    
    def shutdown_laptop(self) -> None:
        """Shutdown the laptop"""
        try:
            if platform.system() == "Windows":
                os.system("shutdown /s /t 30")
        except Exception as e:
            print(f"Error shutting down: {e}")
    
    def restart_laptop(self) -> None:
        """Restart the laptop"""
        try:
            if platform.system() == "Windows":
                os.system("shutdown /r /t 30")
        except Exception as e:
            print(f"Error restarting: {e}")
    
    def listen_for_wake_word(self) -> bool:
        """
        Listen for the wake word "Jarvis"
        
        Returns:
            True if wake word detected, False otherwise
        """
        try:
            self.update_status("Sleeping... Say 'Jarvis' to activate")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            
            text = recognizer.recognize_google(audio).lower()
            return self.wake_word in text
        
        except (sr.UnknownValueError, sr.RequestError):
            return False
        except Exception as e:
            print(f"Error listening for wake word: {e}")
            return False
    
    def continuous_listen(self, chat_callback: Optional[Callable] = None) -> None:
        """
        Continuously listen for voice input while assistant is active
        
        Args:
            chat_callback: Function to add messages to chat history
        """
        while self.is_active:
            command = self.listen()
            if command:
                self.reset_inactivity_timer()
                # Process command in a separate thread to keep listening responsive
                threading.Thread(
                    target=self.process_command,
                    args=(command, chat_callback),
                    daemon=True
                ).start()
                time.sleep(1)  # Small delay between listens
            else:
                time.sleep(0.5)
