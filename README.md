# Bid Leveling AI - Construction Management System

An AI-powered bid analysis and comparison tool for construction management using Claude AI.

## 🎯 Features

- **PDF Extraction**: Automatically extract text from bid PDF documents
- **AI Analysis**: Comprehensive bid analysis using Claude's advanced AI
- **Comparison**: Side-by-side comparison of multiple bids
- **Risk Assessment**: Automated risk identification and scoring
- **Cost Breakdown**: Categorize and analyze cost structures
- **Recommendations**: AI-driven bidder recommendations

## 🏗️ Architecture

**Frontend** → React single-page application with blueprint-inspired design
**Backend** → Flask Python API with PDF processing
**AI Engine** → Anthropic Claude API for intelligent analysis

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+ (for React development)
- Anthropic API Key ([Get one here](https://console.anthropic.com/))

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
# Create .env file
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env

# Or export directly
export ANTHROPIC_API_KEY="your_api_key_here"
```

4. **Run the Flask server:**
```bash
python app.py
```

The backend will start on `http://localhost:5000`

### Frontend Setup

#### Option 1: Quick Test (Standalone HTML)

1. Open `frontend/index.html` in your browser
2. Make sure the backend is running on port 5000

#### Option 2: React Development Server

1. **Install dependencies:**
```bash
cd frontend
npm install
npm install react react-dom
```

2. **Create a development server:**
```bash
# If using Vite
npm create vite@latest . -- --template react
# Copy BidLevelingApp.jsx into src/

# If using Create React App
npx create-react-app .
# Import BidLevelingApp component in App.js
```

3. **Start development server:**
```bash
npm start
```

## 📖 Usage

### Single Bid Analysis

1. Select "SINGLE BID ANALYSIS" mode
2. Upload one PDF bid document
3. Enter the bidder's name (optional)
4. Click "ANALYZE BIDS"
5. Review the comprehensive analysis including:
   - Overall score (1-10)
   - Executive summary
   - Strengths and weaknesses
   - Risk assessment
   - Cost breakdown
   - Final recommendation

### Multiple Bid Comparison

1. Select "COMPARE MULTIPLE BIDS" mode
2. Upload 2 or more PDF bid documents
3. Name each bidder for easy identification
4. Click "ANALYZE BIDS"
5. Review:
   - Individual analysis for each bid
   - Comparison summary
   - Winner recommendation
   - Key differentiators

## 🔧 Configuration

### Backend Configuration

Edit `backend/app.py` to customize:

```python
# Change port
app.run(debug=True, port=5000)

# Adjust Claude model
model="claude-sonnet-4-20250514"  # or claude-opus-4-20250514 for even better analysis

# Modify analysis parameters
max_tokens=4000  # Increase for more detailed analysis
```

### Frontend Configuration

Edit `frontend/BidLevelingApp.jsx` to customize:

```javascript
// Change API endpoint
const API_URL = 'http://localhost:5000/api';

// Modify styling (blueprint theme is default)
// Colors, fonts, and layout can be customized in the component
```

## 📊 API Endpoints

### POST `/api/analyze-bid`
Analyze a single bid document

**Request:**
- `file`: PDF file (multipart/form-data)
- `bidder_name`: Name of the bidder (string)

**Response:**
```json
{
  "summary": "...",
  "categories": [...],
  "pros": [...],
  "cons": [...],
  "risks": {...},
  "recommendation": "RECOMMEND",
  "overall_score": 8,
  ...
}
```

### POST `/api/compare-bids`
Compare multiple bid documents

**Request:**
- `files`: Multiple PDF files (multipart/form-data)
- `bidder_names`: Array of bidder names (strings)

**Response:**
```json
{
  "individual_analyses": [...],
  "comparison": {
    "recommended_bidder": "...",
    "comparison_summary": "...",
    "key_differentiators": [...]
  }
}
```

### GET `/api/health`
Health check endpoint

## 🎨 Design Features

The frontend features a distinctive **blueprint-inspired** aesthetic:

- **Grid Background**: Technical drawing grid pattern
- **Monospaced Fonts**: JetBrains Mono for data-driven feel
- **Blue Color Scheme**: Reminiscent of traditional blueprints
- **Professional Layout**: Clean, structured, construction-focused
- **Responsive Design**: Works on desktop and tablet

## 🚢 Deployment

### Backend Deployment (Options)

1. **Heroku:**
```bash
# Create Procfile
echo "web: python app.py" > Procfile

# Deploy
heroku create your-app-name
heroku config:set ANTHROPIC_API_KEY=your_key
git push heroku main
```

2. **Google Cloud Run:**
```bash
gcloud run deploy bid-analyzer \
  --source . \
  --set-env-vars ANTHROPIC_API_KEY=your_key
```

3. **AWS EC2:**
- Launch Ubuntu instance
- Install Python and dependencies
- Run with `gunicorn app:app`

### Frontend Deployment (Options)

1. **Vercel/Netlify:**
```bash
# Build static site
npm run build

# Deploy to Vercel
vercel deploy

# Or Netlify
netlify deploy --prod
```

2. **GitHub Pages:**
- Build React app
- Deploy to gh-pages branch

3. **Same server as backend:**
- Serve static files from Flask

## 🔒 Security Considerations

1. **API Key Protection:**
   - Never commit API keys to git
   - Use environment variables
   - Consider using a secret manager in production

2. **CORS Configuration:**
   - Update CORS settings for production domains
   - Restrict allowed origins

3. **File Upload Security:**
   - Validate PDF files
   - Limit file size (add to backend)
   - Scan for malware in production

4. **Rate Limiting:**
   - Add rate limiting to prevent abuse
   - Use Flask-Limiter or similar

## 🐛 Troubleshooting

### Backend Issues

**"ModuleNotFoundError: No module named 'flask'"**
- Run: `pip install -r requirements.txt`

**"API key not found"**
- Set environment variable: `export ANTHROPIC_API_KEY=your_key`

**"Could not extract text from PDF"**
- Ensure PDF contains actual text (not just images)
- Try OCR preprocessing if needed

### Frontend Issues

**"Failed to fetch"**
- Check backend is running on port 5000
- Verify CORS is enabled
- Check browser console for errors

**"TypeError: Cannot read property 'individual_analyses'"**
- Backend analysis might have failed
- Check network tab in browser dev tools

## 📈 Future Enhancements

- [ ] Add OCR for scanned PDFs
- [ ] Database integration for bid history
- [ ] User authentication and project management
- [ ] Export reports to PDF/Excel
- [ ] Email notifications
- [ ] Budget variance analysis
- [ ] Historical bid data comparison
- [ ] Multi-language support
- [ ] Mobile app version

## 🤝 Contributing

Contributions are welcome! This is a prototype that can be extended for production use.

## 📄 License

MIT License - feel free to use and modify for your construction management needs.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Examine backend logs: `python app.py` output
4. Check browser console for frontend errors

---

**Built with:**
- [Anthropic Claude AI](https://www.anthropic.com/claude)
- [Flask](https://flask.palletsprojects.com/)
- [React](https://react.dev/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)

**Perfect for:**
- Construction companies
- General contractors
- Project managers
- Procurement teams
- Cost estimators
