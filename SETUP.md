# 🚀 JARVIS Terminal Assistant - Quick Setup Guide

Get your terminal-based AI voice assistant running in 5 minutes!

## What is JARVIS?

JARVIS is a powerful, voice-controlled AI assistant that runs in your terminal. Simply say "Jarvis" to activate it, then give voice commands. It uses Google's Gemini AI for intelligent responses.

## Step 1: Prerequisites Check

Before starting, make sure you have:

- ✅ Python 3.8+ installed
- ✅ Microphone connected to your PC
- ✅ Active internet connection
- ✅ Google Gemini API key (free)

## Step 2: Get Your Free Gemini API Key (2 minutes)

1. Go to: https://aistudio.google.com/app/apikey
2. Click **"Create API Key"** button
3. Copy your new API key (looks like: `AIzaSy...`)
4. Keep it somewhere safe

## Step 3: Install Dependencies (1 minute)

Open Command Prompt and navigate to jarvis folder:

```
cd C:\Users\sriram\OneDrive\Desktop\jarvis
pip install -r requirements.txt
```

**If PyAudio fails**, run:
```
pip install pipwin
pipwin install pyaudio
```

## Step 4: Add Your API Key (1 minute)

1. Open `main.py` in any text editor
2. Find **line 22**: `genai.configure(api_key="YOUR_API_KEY_HERE")`
3. Replace with your actual key:
   ```python
   genai.configure(api_key="AIzaSy_YOUR_REAL_KEY_HERE")
   ```
4. **Save the file**

## Step 5: Run JARVIS! (1 minute)

```
python main.py
```

You should see:

```
==================================================
   🤖 JARVIS - AI VOICE ASSISTANT 🤖   
==================================================

🎤 Say 'JARVIS' to activate the assistant
⏰ You have 20 seconds of active listening
```

## 🎤 Your First Command

1. **Say "JARVIS"** clearly
2. Wait for confirmation message
3. **Say a command** like:
   - "what is the time"
   - "open chrome"
   - "search python tutorials"
   - "tell me a joke"

4. Jarvis will respond with voice!

## 📋 Available Commands

| Command | What It Does |
|---------|-------------|
| "open chrome" | Opens Chrome browser |
| "open youtube" | Opens YouTube |
| "open vscode" | Opens Visual Studio Code |
| "open calculator" | Opens Calculator |
| "search [anything]" | Searches Google |
| "what is the time" | Tells current time |
| "what is the date" | Tells current date |
| "lock laptop" | Locks your computer |
| "shutdown" | Shutdown in 30 seconds |
| "restart" | Restart in 30 seconds |
| "sleep" | Put computer to sleep |
| "stop jarvis" | Exit the program |

## ⚡ Pro Tips

1. **Speak Clearly**: Better recognition with clear pronunciation
2. **Quiet Room**: Less background noise = better accuracy
3. **Microphone Close**: Speak within 1-2 feet of microphone
4. **Short Commands**: "Open chrome" works better than complex sentences
5. **Wait for Response**: Let Jarvis finish before speaking again

## 🎯 How It Works

1. **Sleeping**: Waits for you to say "Jarvis"
2. **Listening**: After wake word, listens for 20 seconds
3. **Processing**: Executes command or uses AI
4. **Speaking**: Responds with voice
5. **Sleep Again**: Returns to sleep after silence

## 🆘 Troubleshooting

### "No module named ..." error
```bash
pip install -r requirements.txt
```

### Microphone not working
- Test microphone in Windows Sound Settings
- Make sure microphone is not muted
- Check microphone is selected as default

### Can't understand "Jarvis"
- Speak louder and clearer
- Reduce background noise
- Say "Jarvis" distinctly

### No sound output
- Check Windows volume (not muted)
- Test speakers with other apps
- Check speaker isn't muted

### API key error
- Verify key is copied correctly (no extra spaces)
- Check internet connection
- Get new key at: https://aistudio.google.com/app/apikey

## 📊 System Requirements

| Requirement | Details |
|------------|---------|
| OS | Windows 10+ |
| Python | 3.8 or higher |
| RAM | 2GB minimum |
| Internet | Required for APIs |
| Microphone | Connected & working |

## 🔐 Keep Your API Key Safe

- ⚠️ **DO NOT** share your API key publicly
- ⚠️ **DO NOT** commit it to GitHub
- ⚠️ **DO NOT** share in screenshots
- ✅ Keep it private and secure

## 📚 Need More Help?

- **README.md** - Full documentation of all features
- **TROUBLESHOOTING.md** - Common issues and solutions
- **API_KEY_SETUP.md** - Detailed API key setup

## ✅ Quick Checklist

Before first use:

- [ ] Python 3.8+ installed
- [ ] Microphone connected
- [ ] Internet working
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Gemini API key obtained
- [ ] API key added to `main.py` line 22
- [ ] Saved `main.py`

## 🎉 You're Ready!

Everything is set up. Time to use JARVIS!

```bash
python main.py
```

**Say "JARVIS" and enjoy your AI assistant!**

---

**Questions?** Check the documentation files or test your setup step by step.

**Enjoy!** 🚀

