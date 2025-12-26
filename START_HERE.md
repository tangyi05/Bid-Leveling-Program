# 🚀 START HERE - Quick Setup Checklist

## ✅ Setup Checklist (Do this once on each computer)

### Step 1: Install Python ✓
- **Mac:** Python 3 is usually pre-installed. Check with: `python3 --version`
- **Windows:** Download from https://www.python.org/ (make sure to check "Add Python to PATH")

### Step 2: Create Virtual Environment ✓
**Mac:**
```bash
cd ~/Downloads/Bidleveling
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
cd C:\Users\YourUsername\Downloads\Bidleveling
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies ✓
```bash
pip install -r requirements.txt
```

### Step 4: Create .env File ⚠️ REQUIRED
**Mac:**
```bash
cp .env.template .env
nano .env
```

**Windows:**
```cmd
copy .env.template .env
notepad .env
```

**Add your Anthropic API key:**
```
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
```

Save and close.

---

## 🎯 Daily Use (Every time you want to run the app)

### Mac:
```bash
cd ~/Downloads/Bidleveling
source venv/bin/activate
python app.py
```

### Windows:
```cmd
cd C:\Users\YourUsername\Downloads\Bidleveling
venv\Scripts\activate
python app.py
```

### Then open your browser:
```
http://localhost:5000/bid-compare.html
```

---

## 📚 Need More Help?

- **Mac users:** Open `MAC_SETUP_GUIDE.md`
- **Windows users:** Open `WINDOWS_SETUP_GUIDE.md`
- **Current status:** See `CURRENT_STATUS.md`

---

## 🎉 You Have Two Tools to Choose From:

### Option 1: Simple Comparison (Recommended) ⭐
**URL:** `http://localhost:5000/bid-compare.html`
- Best for comparing multiple bids side-by-side
- Excel-style table view
- Quick AI recommendation

### Option 2: Detailed Analysis
**URL:** `http://localhost:5000/bid-analyzer.html`
- Best for in-depth single bid analysis
- Card or Table view
- Detailed pros/cons breakdown

---

**That's it! You're ready to start analyzing bids!** 🎊
