# Mac Setup Guide for Bid Leveling Program

## ✅ Complete Setup Instructions for Mac

### Step 1: Open Terminal
1. Press `Cmd + Space` to open Spotlight
2. Type "Terminal" and press Enter

### Step 2: Navigate to Project
```bash
cd ~/Downloads/Bidleveling
```

### Step 3: Create Virtual Environment (First Time Only)
```bash
python3 -m venv venv
```

### Step 4: Activate Virtual Environment
```bash
source venv/bin/activate
```
You should see `(venv)` appear at the start of your terminal prompt.

### Step 5: Install Dependencies (First Time Only)
```bash
pip install -r requirements.txt
```

### Step 6: Create .env File
```bash
cp .env.template .env
```

Then edit the .env file:
```bash
nano .env
```

Replace `your_api_key_here` with your actual Anthropic API key.

Press `Ctrl + X`, then `Y`, then `Enter` to save.

### Step 7: Run the Application
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```

### Step 8: Open in Browser
Open your web browser and go to:
```
http://localhost:5000/bid-compare.html
```

---

## 🔄 Daily Use (After Initial Setup)

Every time you want to use the app:

1. Open Terminal
2. Navigate to project:
   ```bash
   cd ~/Downloads/Bidleveling
   ```
3. Activate virtual environment:
   ```bash
   source venv/bin/activate
   ```
4. Run the app:
   ```bash
   python app.py
   ```
5. Open browser: `http://localhost:5000/bid-compare.html`

---

## 🛑 To Stop the Server
Press `Ctrl + C` in the Terminal window

---

## ❓ Troubleshooting

### "No module named 'flask'"
- Make sure virtual environment is activated (you should see `(venv)` in terminal)
- Run: `pip install -r requirements.txt`

### "API key not found"
- Check that .env file exists: `ls -la .env`
- Make sure it contains: `ANTHROPIC_API_KEY=sk-ant-...`

### "Connection refused" in browser
- Make sure Flask server is running (check Terminal)
- Use `http://localhost:5000/bid-compare.html` not `http://127.0.0.1:5000`

### Port already in use
- Kill existing process: `lsof -ti:5000 | xargs kill -9`
- Then restart: `python app.py`

---

## 📁 File Structure
```
Bidleveling/
├── app.py                 # Flask server (backend)
├── bid-compare.html       # Simplified comparison interface ⭐
├── bid-analyzer.html      # Original analyzer interface
├── requirements.txt       # Python dependencies
├── .env                   # API key (DO NOT COMMIT)
└── venv/                  # Virtual environment folder
```

---

## 🎯 Features

### Simple Bid Comparison (bid-compare.html)
- Upload multiple PDF files
- Real-time progress tracking (5 steps)
- Excel-style table comparison
- Total cost row at bottom
- AI-powered recommendation

### Original Analyzer (bid-analyzer.html)
- Single or multiple bid analysis
- Card view and Table view toggle
- Detailed pros/cons breakdown
- Risk assessment
