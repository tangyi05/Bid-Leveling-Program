# Bid Leveling AI - Project Structure

## 📁 Directory Overview

```
bid-leveling-ai/
│
├── README.md                    # Main documentation and quick start guide
├── DEPLOYMENT.md                # Comprehensive deployment guide
├── .gitignore                   # Git ignore file
├── quick_start.sh               # Unix/Mac quick start script
├── quick_start.bat              # Windows quick start script
│
├── backend/                     # Python Flask API
│   ├── app.py                   # Main Flask application with AI analysis
│   ├── requirements.txt         # Python dependencies
│   ├── .env.template           # Environment variables template
│   └── generate_sample_bids.py  # Script to create test PDF bids
│
└── frontend/                    # React web application
    ├── BidLevelingApp.jsx      # Main React component
    ├── index.html              # Standalone HTML for quick testing
    ├── package.json            # Node.js dependencies
    └── vite.config.js          # Vite build configuration
```

## 🚀 Getting Started - Three Ways

### 1. Quickest Start (Standalone HTML)

**Time: ~5 minutes**

```bash
# 1. Install Python dependencies
cd backend
pip install -r requirements.txt

# 2. Set your API key
cp .env.template .env
# Edit .env and add your ANTHROPIC_API_KEY

# 3. Start backend
python app.py

# 4. Open frontend
# Open frontend/index.html in your browser
```

### 2. Quick Start Script (Recommended)

**Time: ~5 minutes**

```bash
# Unix/Mac
chmod +x quick_start.sh
./quick_start.sh

# Windows
quick_start.bat
```

This script:
- Installs all dependencies
- Sets up your API key
- Generates sample bid PDFs for testing
- Gives you next steps

### 3. Full React Development Setup

**Time: ~10 minutes**

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.template .env
# Edit .env with your API key
python app.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
# Opens on http://localhost:3000
```

## 📄 File Descriptions

### Backend Files

| File | Purpose | Key Features |
|------|---------|--------------|
| `app.py` | Main Flask API server | PDF processing, Claude AI integration, REST endpoints |
| `requirements.txt` | Python dependencies | Flask, Anthropic SDK, PDF tools |
| `.env.template` | Config template | API key storage (copy to `.env`) |
| `generate_sample_bids.py` | Test data generator | Creates realistic construction bid PDFs |

### Frontend Files

| File | Purpose | Key Features |
|------|---------|--------------|
| `BidLevelingApp.jsx` | React component | Complete UI with blueprint design theme |
| `index.html` | Standalone version | Works without build tools (easiest) |
| `package.json` | npm configuration | React dependencies |
| `vite.config.js` | Build tool config | Development server, proxy setup |

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Complete usage guide, API docs, troubleshooting |
| `DEPLOYMENT.md` | Production deployment for Heroku, AWS, GCP, etc. |
| `.gitignore` | Excludes API keys, node_modules, etc. from git |

## 🎯 Core Functionality

### Backend API Endpoints

**POST `/api/analyze-bid`**
- Analyzes a single bid PDF
- Returns: summary, pros/cons, risks, score, recommendation

**POST `/api/compare-bids`**  
- Compares 2+ bid PDFs
- Returns: individual analyses + comparison summary

**GET `/api/health`**
- Health check endpoint
- Returns: server status

### Frontend Features

- **Single Bid Analysis**: Upload one PDF for detailed analysis
- **Multiple Bid Comparison**: Upload 2+ PDFs for side-by-side comparison
- **Blueprint-Inspired Design**: Professional construction management aesthetic
- **Responsive Layout**: Works on desktop and tablets
- **Real-time Analysis**: Instant AI-powered insights

## 🔧 Customization Points

### Backend Customization

**Change AI Model** (`app.py`):
```python
model="claude-sonnet-4-20250514"  # Current
# or
model="claude-opus-4-20250514"    # More powerful, slower
```

**Adjust Analysis Depth** (`app.py`):
```python
max_tokens=4000  # Current
max_tokens=8000  # More detailed analysis
```

**Add Database Storage** (future):
- Uncomment DATABASE_URL in .env
- Add SQLAlchemy to requirements.txt
- Store bid history for comparison

### Frontend Customization

**Change API Endpoint** (`BidLevelingApp.jsx`):
```javascript
const API_URL = 'http://localhost:5000/api';  // Development
const API_URL = 'https://your-api.com/api';   // Production
```

**Modify Design Theme** (`BidLevelingApp.jsx`):
- Line 14-18: Background colors and grid
- Line 69-78: Blueprint colors
- Line 500-600: Typography and spacing

**Add Features**:
- Email notifications
- PDF report generation
- Historical bid tracking
- User authentication

## 📊 Technology Stack

### Backend
- **Framework**: Flask (Python web framework)
- **AI**: Anthropic Claude API
- **PDF Processing**: pdfplumber
- **HTTP**: CORS enabled for frontend communication

### Frontend
- **UI**: React 18
- **Styling**: Inline styles (no CSS files needed)
- **Build Tool**: Vite (optional, for development)
- **Design**: Blueprint/technical drawing aesthetic

## 🧪 Testing

### Generate Sample Bids

```bash
cd backend
python generate_sample_bids.py
```

This creates 3 sample bids in `backend/sample_bids/`:
1. **Acme Construction**: Balanced, competitive bid
2. **Budget Builders**: Lower cost, less experience  
3. **Premier Construction**: Premium quality, higher cost

### Test the API

```bash
# Make sure backend is running
curl http://localhost:5000/api/health

# Test bid analysis (use a sample bid)
curl -X POST http://localhost:5000/api/analyze-bid \
  -F "file=@sample_bids/acme_construction_bid.pdf" \
  -F "bidder_name=Acme Construction"
```

## 🚢 Deployment Options

Quick comparison:

| Platform | Cost | Complexity | Best For |
|----------|------|------------|----------|
| Heroku | $0-7/mo | ⭐ Easy | Prototypes |
| Google Cloud Run | $5-10/mo | ⭐⭐ Medium | Production |
| AWS EC2 | $10-15/mo | ⭐⭐⭐ Advanced | Full control |
| DigitalOcean | $5-10/mo | ⭐⭐ Medium | Simplicity |

See `DEPLOYMENT.md` for detailed instructions.

## 📈 Next Steps After Setup

1. **Test with sample bids** - Use `generate_sample_bids.py`
2. **Try your own PDFs** - Upload real construction bids
3. **Customize the UI** - Match your company's branding
4. **Deploy to production** - Follow `DEPLOYMENT.md`
5. **Add features** - Database, notifications, etc.

## 🆘 Common Issues

**"ModuleNotFoundError"**
- Solution: Run `pip install -r requirements.txt`

**"API key not found"**  
- Solution: Create `.env` file with your `ANTHROPIC_API_KEY`

**"CORS error"**
- Solution: Make sure backend is running on port 5000

**"Could not extract text from PDF"**
- Solution: PDF might be scanned image - add OCR preprocessing

## 📞 Support

1. Check `README.md` troubleshooting section
2. Review `DEPLOYMENT.md` for deployment issues  
3. Examine backend logs for errors
4. Check browser console for frontend errors

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Anthropic Claude API](https://docs.anthropic.com/claude/docs)
- [React Documentation](https://react.dev/)
- [pdfplumber Guide](https://github.com/jsvine/pdfplumber)

---

**You're all set!** Start with the Quick Start script and you'll have a working bid analysis system in minutes.
