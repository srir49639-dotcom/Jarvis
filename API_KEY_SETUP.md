# 🔑 Google Gemini API Key Setup Guide

Step-by-step guide to get your free Google Gemini API key.

## 🚀 Quick Setup (3 minutes)

### Step 1: Visit Google AI Studio

Go to: https://aistudio.google.com/app/apikey

(Or Google → "AI Studio" → API Keys)

### Step 2: Create New API Key

1. Click **"Create API Key"** button
2. Select **"Create API key in new project"**
3. Wait a moment for key to generate

### Step 3: Copy Your API Key

1. You'll see a long string (looks like: `AIzaSy...`)
2. Click **"Copy"** button
3. **Save this safely** (like a text file or password manager)

### Step 4: Add to Jarvis

Open `assistant.py` in the jarvis folder:

**Find this line** (around line 18):
```python
genai.configure(api_key="YOUR_API_KEY_HERE")
```

**Replace with your actual key**:
```python
genai.configure(api_key="AIzaSyC3awtol_VX3Md2d-kL9z2XH1JAOOpJpW8")
```

⚠️ **Example above is not real - use your own key!**

### Step 5: Test It Works

```bash
python main.py
```

Say "Jarvis, who are you?" to test AI response.

---

## 📋 Pre-requisites Check

Before starting, verify:

- ✅ Google account (Gmail, etc.)
- ✅ Internet connection
- ✅ Web browser open

## 🔍 Finding Your API Key

### If you already have one:

1. Go to: https://aistudio.google.com/app/apikey
2. Your existing keys are listed
3. Click the key you want to copy
4. Click **"Copy"** icon

### If you lost your key:

1. Create a new one (follow steps above)
2. Old keys become invalid
3. You can have multiple keys

## 🆓 Free Tier Limits

**Good news**: The free tier is generous!

- ✅ **60 requests per minute**
- ✅ **10,000 requests per month** (approximately)
- ✅ **All features included**
- ✅ **No credit card required**

For Jarvis usage (a few questions per day), you'll never hit these limits.

## ⚠️ Common Issues

### Issue: "API key invalid"

**Solution**:
1. Double-check you copied the ENTIRE key
2. Make sure no extra spaces at start/end
3. Visit Google AI Studio to verify key still exists
4. Try creating a new key

### Issue: "quota exceeded"

**Very unlikely** with the free tier, but:
1. Check your usage at: https://console.cloud.google.com/apis/dashboard
2. Create a new project if needed
3. Generate a new API key

### Issue: "Access denied"

**Possible causes**:
1. API not enabled in Google Cloud
2. Try accessing https://aistudio.google.com/app/apikey again
3. May need to sign in with Google account

## 🔐 Security Best Practices

### DO:
- ✅ Keep API key private
- ✅ Regenerate if you think it's compromised
- ✅ Use environment variables for production
- ✅ Never share your key publicly

### DON'T:
- ❌ Commit API key to GitHub/public repos
- ❌ Share with anyone else
- ❌ Put in screenshots or documents
- ❌ Hardcode in production apps (use env vars)

## 🔄 Environment Variable Setup (Advanced)

**For better security**, use environment variables:

### On Windows:

**Create `.env` file in jarvis folder:**
```
GEMINI_API_KEY=AIzaSy...your_key_here
```

**Modify assistant.py** (around line 18):
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
```

**Install python-dotenv:**
```bash
pip install python-dotenv
```

**Add to requirements.txt:**
```
python-dotenv
```

## ✅ Verify Setup Works

1. **Run Jarvis**:
   ```bash
   python main.py
   ```

2. **Say "Jarvis"** to wake it up

3. **Ask a question**:
   - "What is Python?"
   - "Tell me a joke"
   - "Who is Albert Einstein?"

4. **Check for response**:
   - You should hear a voice response
   - Response appears in chat area

## 🎯 If It Still Doesn't Work

### Check 1: Internet Connection
```
Try visiting google.com in your browser
```

### Check 2: Microphone Works
```
Test microphone in other apps first
```

### Check 3: Python Packages
```bash
pip install google-generativeai
```

### Check 3: Check Console for Errors
```
Look at command prompt for error messages
Read the error text carefully
```

### Check 4: Try Simpler Command
```
Instead of complex question, try:
"What is 2 plus 2?"
```

## 🆘 Still Having Issues?

1. **Console Error Messages**: Read them carefully, they explain the problem
2. **Check API Status**: https://status.cloud.google.com/
3. **Verify Key Format**: Should start with "AIzaSy"
4. **Test with curl**: Verify key works via command line
5. **Read Python traceback**: Shows exactly where error occurs

## 📚 Additional Resources

- Google AI Studio: https://aistudio.google.com/
- Gemini API Docs: https://ai.google.dev/
- Pricing Info: https://ai.google.dev/pricing

---

**You're all set! Your Jarvis is ready to chat with Gemini AI.** 🤖

Any questions about setup? Check SETUP.md or README.md.
