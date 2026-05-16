# 🔧 Troubleshooting Guide

Comprehensive troubleshooting for common Jarvis issues.

## 🚨 Common Problems & Solutions

---

## 1. Application Won't Start

### Error: "ModuleNotFoundError: No module named 'customtkinter'"

**Cause**: Dependencies not installed

**Solution**:
```bash
pip install -r requirements.txt
```

If error continues:
```bash
pip install customtkinter==5.2.0
```

---

### Error: "ModuleNotFoundError: No module named 'speech_recognition'"

**Cause**: SpeechRecognition not installed

**Solution**:
```bash
pip install SpeechRecognition==3.10.0
```

---

### Error: "ModuleNotFoundError: No module named 'pyaudio'"

**Cause**: PyAudio (microphone access) not installed

**Solution on Windows**:
```bash
pip install pipwin
pipwin install pyaudio
```

**Alternative (if above fails)**:
1. Go to: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. Download wheel matching your Python version (e.g., `PyAudio‑0.2.13‑cp39‑cp39‑win_amd64.whl`)
3. Run:
```bash
pip install C:\path\to\PyAudio-0.2.13-cp39-cp39-win_amd64.whl
```

**Replace cp39 with your Python version!**

---

## 2. GUI Appears But Nothing Happens

### Problem: Window opens but no response when speaking

**Cause**: Often a Google API issue

**Solution**:
1. Check your API key in `assistant.py` (line 18)
2. Verify key format (should start with "AIzaSy")
3. Visit https://aistudio.google.com/app/apikey to confirm key is valid
4. Check internet connection

**Test**:
```bash
python main.py
```
Check console for error messages

---

### Problem: Status shows "Sleeping" but won't respond to "Jarvis"

**Cause**: Microphone not working or voice recognition failing

**Solution 1 - Check Microphone**:
1. Open Windows Sound Settings
2. Test microphone with other apps (Discord, Teams, etc.)
3. Ensure microphone is not muted
4. Check volume is not too low

**Solution 2 - Check Volume Threshold**:
In `assistant.py`, around line 16, adjust:
```python
recognizer.energy_threshold = 4000  # Try 3000-6000
```
- Higher number = less sensitive (good for loud rooms)
- Lower number = more sensitive (good for quiet rooms)

**Solution 3 - Speak More Clearly**:
- Speak louder and clearer
- Say "Jarvis" explicitly at start
- Wait for response before continuing

**Solution 4 - Check Internet**:
```bash
ping google.com
```
Must have internet for voice recognition API

---

## 3. Microphone Issues

### Error: "No default input device found"

**Cause**: Microphone not detected

**Solution**:
1. Connect microphone to computer
2. Right-click Sound icon (system tray)
3. Select "Open Sound Settings"
4. Check microphone under "Input devices"
5. Set as default if needed
6. Restart Jarvis application

---

### Problem: "Listening..." but nothing happens

**Cause**: Microphone too quiet or not detected

**Solution**:
```python
# In assistant.py, increase timeout
audio = recognizer.listen(source, timeout=15, phrase_time_limit=10)
# Was timeout=10, now 15 seconds
```

---

### Error: "WavFile error during microphone listen"

**Cause**: Microphone access issue

**Solution**:
```python
# In assistant.py around line 17, adjust:
recognizer.energy_threshold = 3000  # Lower sensitivity
recognizer.dynamic_energy_threshold = True
```

---

## 4. Speech Recognition Issues

### Problem: "I didn't understand that" (always)

**Cause**: Voice not clear or background noise

**Solution 1 - Quieter Environment**:
- Close doors and windows
- Stop other applications
- Speak clearly and directly to microphone

**Solution 2 - Adjust Timeout**:
```python
# In assistant.py:
audio = recognizer.listen(source, timeout=12, phrase_time_limit=10)
```

**Solution 3 - Lower Threshold**:
```python
recognizer.energy_threshold = 3000  # Lower = more sensitive
```

---

### Problem: Only hears beginning of speech

**Cause**: phrase_time_limit too short

**Solution** in `assistant.py`:
```python
audio = recognizer.listen(
    source, 
    timeout=10,
    phrase_time_limit=15  # Increased from 10 to 15 seconds
)
```

---

## 5. AI Response Issues

### Error: "API key invalid"

**Cause**: Wrong or expired API key

**Solution**:
1. Go to: https://aistudio.google.com/app/apikey
2. Create a new API key
3. Copy the ENTIRE key (no spaces)
4. Update `assistant.py` line 18:
```python
genai.configure(api_key="YOUR_NEW_KEY_HERE")
```

---

### Error: "Error getting AI response"

**Cause**: Could be API key, internet, or API issue

**Solution**:
1. Check API key is correct
2. Test internet: `ping google.com`
3. Check if Google API is down: https://status.cloud.google.com/
4. Try a simple question first

**Debug**:
Add this to `assistant.py` in `get_ai_response()`:
```python
print(f"API Key configured: {genai.api_key}")
print(f"Model available: {gemini_model}")
```

---

### Problem: Very slow AI responses

**Cause**: Internet speed or API latency

**Solution**:
1. Check internet speed: speedtest.net
2. Try simpler questions first
3. Restart application
4. Clear browser cache
5. Close other internet-using apps

---

## 6. Voice Output Issues

### Problem: "Speaking..." shows but no sound

**Cause**: Volume muted or text-to-speech not working

**Solution 1 - Check Volume**:
1. Check Windows volume (system tray)
2. Adjust application volume
3. Test speakers with Windows sounds
4. Check speaker is not muted

**Solution 2 - Check pyttsx3**:
```bash
pip install --upgrade pyttsx3
```

**Test text-to-speech**:
```python
import pyttsx3
engine = pyttsx3.init()
engine.say("Hello, this is a test")
engine.runAndWait()
```

---

### Problem: Voice sounds robotic or wrong voice

**Cause**: Voice engine settings or installed voices

**Solution**:
In `assistant.py`, adjust:
```python
engine = pyttsx3.init()
engine.setProperty('rate', 150)      # Speech speed (100-300)
engine.setProperty('volume', 0.9)    # Volume (0-1)
```

---

## 7. Command Execution Issues

### Problem: "Open Chrome" doesn't work

**Cause**: Chrome not installed or path incorrect

**Solution 1 - Verify Chrome installed**:
```bash
where chrome
```
or open Chrome manually

**Solution 2 - Update path in assistant.py**:
```python
"chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
```

**Solution 3 - Try Google instead**:
Say "open google" (uses default browser)

---

### Problem: "Shutdown" countdown won't start

**Cause**: Command syntax issue or system settings

**Solution**:
```python
# In assistant.py, the shutdown command uses:
os.system("shutdown /s /t 30")
```

To test manually:
```bash
shutdown /s /t 60  # Shutdown in 60 seconds
shutdown /a        # Abort shutdown
```

---

### Problem: "Lock laptop" doesn't lock

**Cause**: Windows lock function not working

**Solution**:
Use Windows Lock shortcut instead:
- Press: **Windows Key + L**

Or test the command:
```bash
rundll32.exe user32.dll,LockWorkStation
```

---

## 8. GUI Issues

### Problem: Text in chat area is too small/large

**Cause**: Font size settings in gui.py

**Solution** in `gui.py`:
```python
self.chat_display = ctk.CTkTextbox(
    chat_display_frame,
    font=("Courier", 12)  # Change 10 to 12 for larger
)
```

---

### Problem: Colors look wrong or glitchy

**Cause**: CustomTkinter theme issue

**Solution** in `gui.py`:
```python
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
```

Try different themes:
```python
ctk.set_default_color_theme("blue")
ctk.set_default_color_theme("green")
```

---

### Problem: Window won't resize or is too small

**Solution** in `gui.py`:
```python
self.root.geometry("1200x800")  # Change default size
self.root.resizable(True, True)  # Allow resizing
```

---

## 9. Threading/Performance Issues

### Problem: GUI freezes when listening

**Cause**: Voice recognition running on main thread

**Solution**: Already implemented in code via threading. If still freezing:
```python
# Make sure voice_listening_thread is set as daemon
threading.Thread(target=self.voice_listening_loop, daemon=True).start()
```

---

### Problem: Multiple voice commands at once

**Cause**: Threading issue or microphone sensitivity

**Solution**:
1. Wait for response before speaking again
2. Let the "Listening..." status appear
3. Pause between commands

---

## 10. File and Path Issues

### Error: "File not found" for applications

**Cause**: Incorrect file paths in code

**Solution** in `assistant.py`:
```python
apps = {
    "code": "C:\\Users\\sriram\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
}
```

**To find correct path**:
1. Right-click app shortcut
2. Select "Properties"
3. Copy "Target" path
4. Use in code

---

### Problem: Can't find main.py location

**Solution**:
```bash
cd C:\Users\sriram\OneDrive\Desktop\jarvis
python main.py
```

Or create shortcut:
```
Create .bat file with:
@echo off
cd C:\Users\sriram\OneDrive\Desktop\jarvis
python main.py
```

---

## 📋 Debugging Checklist

When something doesn't work:

- [ ] Check console output for error messages
- [ ] Verify internet connection
- [ ] Test microphone works
- [ ] Check speaker volume
- [ ] Reinstall dependencies: `pip install -r requirements.txt`
- [ ] Verify API key is correct
- [ ] Read error messages completely (they help!)
- [ ] Restart application
- [ ] Restart computer (if still stuck)
- [ ] Check file paths are correct

---

## 🆘 If Nothing Works

1. **Read the Error Message**: It usually tells you exactly what's wrong
2. **Search Error Online**: Someone probably had the same issue
3. **Check System Requirements**: Python 3.8+, Windows 10+
4. **Reinstall from Scratch**:
   ```bash
   pip uninstall -r requirements.txt
   pip install -r requirements.txt
   ```
5. **Check Internet**: Must be connected for most features
6. **Test Individual Components**:
   - Microphone: Test in Discord/Teams
   - API Key: Test in https://aistudio.google.com/app/
   - Internet: `ping google.com`

---

## 📊 System Information

To help diagnose issues, provide:
- Python version: `python --version`
- OS: Windows version
- Error message (exact text)
- What were you trying to do
- Steps to reproduce

---

## 🆘 Still Need Help?

1. Read SETUP.md for installation help
2. Check README.md for features overview
3. Review API_KEY_SETUP.md for API issues
4. Check ARCHITECTURE.md to understand code flow

**Good luck! Most issues are easily fixable once diagnosed.** 🚀
