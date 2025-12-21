# Deployment Guide - Bid Leveling AI

This guide covers various deployment options for the Bid Leveling AI system in production environments.

## Table of Contents

1. [Production Preparation](#production-preparation)
2. [Backend Deployment](#backend-deployment)
3. [Frontend Deployment](#frontend-deployment)
4. [Full Stack Deployment](#full-stack-deployment)
5. [Security Hardening](#security-hardening)
6. [Monitoring & Maintenance](#monitoring--maintenance)

## Production Preparation

### 1. Environment Variables

Create a `.env` file with production settings:

```bash
# Required
ANTHROPIC_API_KEY=your_production_api_key

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False

# Server Configuration
PORT=5000
HOST=0.0.0.0

# CORS (update with your domain)
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Optional: Database (for future enhancements)
# DATABASE_URL=postgresql://user:password@localhost/bidleveling
```

### 2. Dependencies

Update `requirements.txt` for production:

```bash
cd backend
pip install -r requirements.txt

# Additional production packages
pip install gunicorn  # Production WSGI server
pip install python-dotenv  # Already in requirements
```

### 3. Security Checklist

- [ ] API keys in environment variables (never in code)
- [ ] HTTPS/SSL enabled
- [ ] CORS configured for specific domains only
- [ ] Rate limiting implemented
- [ ] File upload size limits set
- [ ] Input validation on all endpoints
- [ ] Error messages don't leak sensitive info
- [ ] Security headers configured

---

## Backend Deployment

### Option 1: Heroku (Easiest)

#### Setup

1. **Install Heroku CLI:**
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

2. **Create Heroku App:**
```bash
heroku login
heroku create your-bid-analyzer-api
```

3. **Create Procfile:**
```bash
# In project root
echo "web: gunicorn --chdir backend app:app" > Procfile
```

4. **Set Environment Variables:**
```bash
heroku config:set ANTHROPIC_API_KEY=your_key
heroku config:set FLASK_ENV=production
```

5. **Deploy:**
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

6. **Scale:**
```bash
heroku ps:scale web=1
```

Your API will be available at: `https://your-bid-analyzer-api.herokuapp.com`

#### Cost: Free tier available, ~$7/month for hobby tier

---

### Option 2: Google Cloud Run (Serverless)

#### Setup

1. **Create Dockerfile:**
```dockerfile
# In backend directory
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
```

2. **Deploy:**
```bash
# Install gcloud CLI first
gcloud init
gcloud config set project your-project-id

# Deploy to Cloud Run
gcloud run deploy bid-analyzer \
  --source backend/ \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=your_key,FLASK_ENV=production
```

Your API will be available at: `https://bid-analyzer-xxxxx.run.app`

#### Cost: Pay per use, generous free tier

---

### Option 3: AWS EC2 (Traditional VPS)

#### Setup

1. **Launch EC2 Instance:**
   - Ubuntu Server 22.04 LTS
   - t2.small or larger
   - Open ports 22 (SSH), 80 (HTTP), 443 (HTTPS)

2. **Connect and Setup:**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Clone your code
git clone https://github.com/yourusername/bid-leveling-ai.git
cd bid-leveling-ai/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

3. **Configure Gunicorn:**
```bash
# Create systemd service
sudo nano /etc/systemd/system/bidanalyzer.service
```

Add:
```ini
[Unit]
Description=Bid Analyzer Gunicorn
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/bid-leveling-ai/backend
Environment="PATH=/home/ubuntu/bid-leveling-ai/backend/venv/bin"
Environment="ANTHROPIC_API_KEY=your_key"
Environment="FLASK_ENV=production"
ExecStart=/home/ubuntu/bid-leveling-ai/backend/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

4. **Configure Nginx:**
```bash
sudo nano /etc/nginx/sites-available/bidanalyzer
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # File upload size limit
    client_max_body_size 50M;
}
```

5. **Enable and Start:**
```bash
sudo ln -s /etc/nginx/sites-available/bidanalyzer /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl start bidanalyzer
sudo systemctl enable bidanalyzer
sudo systemctl restart nginx
```

6. **Setup SSL (Let's Encrypt):**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

#### Cost: ~$10-15/month for t2.small

---

### Option 4: DigitalOcean App Platform

#### Setup

1. **Connect GitHub:**
   - Go to DigitalOcean App Platform
   - Connect your GitHub repository

2. **Configure:**
   - Select `backend` directory as source
   - Choose Python as runtime
   - Set build command: `pip install -r requirements.txt`
   - Set run command: `gunicorn --bind 0.0.0.0:$PORT app:app`

3. **Environment Variables:**
   - Add `ANTHROPIC_API_KEY`
   - Add `FLASK_ENV=production`

4. **Deploy:**
   - Click "Deploy"

#### Cost: Starting at $5/month

---

## Frontend Deployment

### Option 1: Vercel (Recommended for React)

#### Using React Build

1. **Create React App:**
```bash
cd frontend
npx create-react-app bid-leveling-ui
cd bid-leveling-ui

# Copy your component
cp ../BidLevelingApp.jsx src/App.js
```

2. **Update API URL:**
```javascript
// In App.js
const API_URL = process.env.REACT_APP_API_URL || 'https://your-backend.com/api';
```

3. **Build:**
```bash
npm run build
```

4. **Deploy to Vercel:**
```bash
npm i -g vercel
vercel --prod
```

5. **Set Environment Variable:**
```bash
vercel env add REACT_APP_API_URL
# Enter your backend URL
```

#### Using Standalone HTML

If using the standalone HTML file:

```bash
cd frontend
vercel --prod
```

Update the API_URL in BidLevelingApp.jsx before deploying.

#### Cost: Free for personal projects

---

### Option 2: Netlify

#### Setup

1. **Build React app** (if using React):
```bash
npm run build
```

2. **Deploy:**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd frontend  # or build directory
netlify deploy --prod
```

3. **Environment Variables:**
   - Go to Site Settings > Build & Deploy > Environment
   - Add `REACT_APP_API_URL=https://your-backend.com/api`

#### Cost: Free tier available

---

### Option 3: GitHub Pages

For standalone HTML:

1. **Create gh-pages branch:**
```bash
git checkout -b gh-pages
git push origin gh-pages
```

2. **Enable GitHub Pages:**
   - Repository Settings > Pages
   - Source: gh-pages branch

3. **Update API URL** in the code before pushing

#### Cost: Free

---

### Option 4: Serve from Same Server (EC2/VPS)

If you deployed backend to EC2, serve frontend from Nginx:

```bash
# Copy frontend files
sudo mkdir -p /var/www/bidanalyzer
sudo cp frontend/* /var/www/bidanalyzer/

# Update Nginx config
sudo nano /etc/nginx/sites-available/bidanalyzer
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/bidanalyzer;
        try_files $uri $uri/ /index.html;
    }

    # API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    client_max_body_size 50M;
}
```

---

## Full Stack Deployment

### Option 1: Single Server (Cost Effective)

Deploy both frontend and backend on one EC2 instance:

```
┌─────────────────────────────┐
│       EC2 Instance          │
│  ┌──────────────────────┐   │
│  │   Nginx (Port 80)    │   │
│  └──────────────────────┘   │
│           │                 │
│     ┌─────┴─────┐           │
│     │           │           │
│  Frontend    Backend         │
│  (Static)  (Gunicorn:5000)  │
└─────────────────────────────┘
```

### Option 2: Microservices (Scalable)

```
┌──────────────┐     ┌──────────────┐
│   Vercel     │────▶│  Cloud Run   │
│  (Frontend)  │     │  (Backend)   │
└──────────────┘     └──────────────┘
```

---

## Security Hardening

### 1. Rate Limiting

```python
# In app.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/analyze-bid', methods=['POST'])
@limiter.limit("10 per minute")
def analyze_bid():
    # ... existing code
```

### 2. File Upload Limits

```python
# In app.py
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max
```

### 3. CORS Security

```python
# In app.py
from flask_cors import CORS

CORS(app, origins=os.environ.get('ALLOWED_ORIGINS', '').split(','))
```

### 4. Security Headers

```python
from flask_talisman import Talisman

Talisman(app, 
    force_https=True,
    strict_transport_security=True,
    content_security_policy={
        'default-src': "'self'",
        'script-src': ["'self'", "'unsafe-inline'"],
        'style-src': ["'self'", "'unsafe-inline'"]
    }
)
```

---

## Monitoring & Maintenance

### 1. Logging

```python
# In app.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bid_analyzer.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 2. Error Tracking

Consider integrating:
- **Sentry**: Error tracking and monitoring
- **LogRocket**: Frontend monitoring
- **CloudWatch**: AWS monitoring

### 3. Backups

If you add database functionality:
```bash
# Automated PostgreSQL backups
0 2 * * * pg_dump bidleveling > /backups/bidleveling-$(date +\%Y\%m\%d).sql
```

### 4. Updates

```bash
# Regular security updates
sudo apt update && sudo apt upgrade -y

# Python package updates
pip list --outdated
pip install --upgrade package-name
```

---

## Cost Comparison

| Option | Monthly Cost | Best For |
|--------|-------------|----------|
| Heroku Free | $0 | Testing/Demo |
| Heroku Hobby | $7 | Small teams |
| Google Cloud Run | ~$5-10 | Variable traffic |
| DigitalOcean | $10-15 | Predictable traffic |
| AWS EC2 t2.small | $10-15 | Full control |
| Vercel + Cloud Run | $0-15 | Production ready |

---

## Recommended Production Stack

For most use cases:

**Frontend:** Vercel (Free)  
**Backend:** Google Cloud Run ($5-10/month)  
**Total:** ~$5-10/month

This provides:
- ✅ Automatic scaling
- ✅ HTTPS included
- ✅ Global CDN (Vercel)
- ✅ Pay only for usage
- ✅ Easy deployment

---

## Support

For deployment issues:
1. Check application logs
2. Verify environment variables
3. Test API endpoints directly
4. Check CORS configuration
5. Review security group/firewall rules

---

**Need Help?**

Common issues and solutions in the main README.md troubleshooting section.
