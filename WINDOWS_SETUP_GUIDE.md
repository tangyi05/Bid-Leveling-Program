# Windows Setup Guide for Bid Leveling Program

## ✅ Complete Setup Instructions for Windows

### Step 1: Open Command Prompt
1. Press `Win + R`
2. Type `cmd` and press Enter

### Step 2: Navigate to Project
```cmd
cd C:\Users\YourUsername\Downloads\Bidleveling
```
(Replace `YourUsername` with your actual username)

### Step 3: Create Virtual Environment (First Time Only)
```cmd
python -m venv venv
```

### Step 4: Activate Virtual Environment
```cmd
venv\Scripts\activate
```
You should see `(venv)` appear at the start of your command prompt.

### Step 5: Install Dependencies (First Time Only)
```cmd
pip install -r requirements.txt
```

### Step 6: Create .env File
```cmd
copy .env.template .env
```

Then edit the .env file:
```cmd
notepad .env
```

Replace `your_api_key_here` with your actual Anthropic API key.

Save and close Notepad.

### Step 7: Run the Application
```cmd
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

1. Open Command Prompt (Win + R, type `cmd`, press Enter)
2. Navigate to project:
   ```cmd
   cd C:\Users\YourUsername\Downloads\Bidleveling
   ```
3. Activate virtual environment:
   ```cmd
   venv\Scripts\activate
   ```
4. Run the app:
   ```cmd
   python app.py
   ```
5. Open browser: `http://localhost:5000/bid-compare.html`

---

## 🛑 To Stop the Server
Press `Ctrl + C` in the Command Prompt window

---

## ❓ Troubleshooting

### "pip is not recognized"
- Python is not installed or not in PATH
- Download Python from: https://www.python.org/downloads/
- **Important:** Check "Add Python to PATH" during installation

### "No module named 'flask'"
- Make sure virtual environment is activated (you should see `(venv)`)
- Run: `pip install -r requirements.txt`

### "API key not found"
- Check that .env file exists: `dir .env`
- Make sure it contains: `ANTHROPIC_API_KEY=sk-ant-...`

### "Connection refused" in browser
- Make sure Flask server is running (check Command Prompt)
- Use `http://localhost:5000/bid-compare.html`

### Port already in use
- Find process using port 5000:
  ```cmd
  netstat -ano | findstr :5000
  ```
- Kill the process (replace PID with actual number):
  ```cmd
  taskkill /PID <PID> /F
  ```
- Then restart: `python app.py`

---

## 📁 File Structure
```
Bidleveling\
├── app.py                 # Flask server (backend)
├── bid-compare.html       # Simplified comparison interface ⭐
├── bid-analyzer.html      # Original analyzer interface
├── requirements.txt       # Python dependencies
├── .env                   # API key (DO NOT COMMIT)
└── venv\                  # Virtual environment folder
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
