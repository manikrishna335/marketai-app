# MarketAI — AI Marketing Automation App

Built for Mani's AI Marketing Agency.
Stack: Python FastAPI (backend) + HTML/CSS/JS (frontend)
Deploy: Railway (backend) + Netlify (frontend)

---

## WHAT THIS APP DOES

6 automation tools in one dashboard:
1. SEO Strategy — Top-10 ranking plan for any keyword
2. Organic Strategy — 10-channel content & growth plan
3. Backlink Automation — Outreach emails + link building plan
4. Paid Ads — Google & Meta campaign strategy + ad copies
5. Client Reports — Auto-generate monthly reports
6. Outreach Kit — Cold email + LinkedIn + call scripts

---

## STEP 1 — Get Your API Key (Free $5 Credit)

1. Go to https://console.anthropic.com
2. Sign up / log in
3. Click "API Keys" → "Create Key"
4. Copy your key (starts with sk-ant-...)

---

## STEP 2 — Deploy Backend on Railway (Free)

1. Go to https://railway.app and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Upload/push the `backend/` folder to a GitHub repo
4. In Railway dashboard → your project → "Variables" tab
5. Add this environment variable:
   ANTHROPIC_API_KEY = sk-ant-your-key-here
6. Railway auto-deploys. Copy your URL e.g.:
   https://marketai-backend.up.railway.app

---

## STEP 3 — Deploy Frontend on Netlify (Free)

1. Go to https://netlify.com and sign up
2. Drag and drop the ENTIRE project folder onto Netlify
   (or connect GitHub repo)
3. Netlify will auto-detect netlify.toml and deploy
4. Your app goes live at: https://marketai-xxx.netlify.app

---

## STEP 4 — Connect Frontend to Backend

1. Open your Netlify app in browser
2. In the orange config bar at top, paste your Railway URL:
   https://marketai-backend.up.railway.app
3. Click Save
4. Done! All 6 tools now work.

---

## LOCAL DEVELOPMENT

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key
uvicorn main:app --reload --port 8000

# Frontend
# Just open frontend/index.html in browser
# Set backend URL to http://localhost:8000
```

---

## PROJECT STRUCTURE

```
ai-marketing-app/
├── frontend/
│   └── index.html          ← Full app (deploy to Netlify)
├── backend/
│   ├── main.py             ← FastAPI with all 6 endpoints
│   ├── requirements.txt    ← Python dependencies
│   ├── .env.example        ← Copy to .env for local dev
│   └── railway.toml        ← Railway deployment config
├── netlify.toml            ← Netlify deployment config
└── README.md
```

---

## API ENDPOINTS

POST /api/seo             → SEO strategy
POST /api/organic-strategy → Full organic plan
POST /api/backlinks       → Backlink building plan
POST /api/ads             → Paid ads strategy
POST /api/report          → Client monthly report
POST /api/outreach        → Cold outreach kit

---

## COSTS

- Railway free tier: $5/month free credit (enough for ~200 requests/day)
- Anthropic API: ~$0.01-0.03 per generation
- Netlify: 100% free for frontend
- Total monthly cost: $5-15 depending on usage

---

## SCALE UP LATER

- Add authentication (Clerk.dev - free)
- Add database to save outputs (Supabase - free)
- Add PDF export for reports
- Add scheduling (send weekly reports automatically)
- Add Google Search Console API for real keyword data
