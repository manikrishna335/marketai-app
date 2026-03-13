from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import httpx
import os
from datetime import datetime

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

app = FastAPI(title="AI Marketing Execution API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class KeywordRequest(BaseModel):
    keyword: str
    country: Optional[str] = "India"

class BlogRequest(BaseModel):
    keyword: str
    website_url: Optional[str] = ""
    tone: Optional[str] = "professional"

class GoogleAdsRequest(BaseModel):
    business: str
    keyword: str
    budget: str
    location: Optional[str] = "India"

class MetaAdsRequest(BaseModel):
    business: str
    product: str
    budget: str
    target_age: Optional[str] = "25-45"
    location: Optional[str] = "India"

class BacklinkRequest(BaseModel):
    keyword: str
    website_url: str
    niche: str

async def call_groq(prompt: str, max_tokens: int = 2000) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, headers=headers, json=body)
            data = r.json()
            if "choices" in data:
                return data["choices"][0]["message"]["content"]
            else:
                return f"Error: {data.get('error', {}).get('message', str(data))}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.get("/")
def root():
    return {"status": "AI Marketing Execution API running", "version": "2.0"}

# 1. KEYWORD RESEARCH
@app.post("/api/keyword-research")
async def keyword_research(req: KeywordRequest):
    prompt = f"""You are an expert SEO keyword researcher. Analyze the keyword "{req.keyword}" for {req.country} market.

Provide EXACTLY this data in a structured format:

KEYWORD OVERVIEW:
- Main Keyword: {req.keyword}
- Estimated Monthly Search Volume: [give realistic number]
- Keyword Difficulty (KD): [0-100 score]
- Search Intent: [Informational/Navigational/Commercial/Transactional]
- CPC (Cost Per Click): [realistic USD amount]
- Competition Level: [Low/Medium/High]

TOP 10 RELATED KEYWORDS:
[List 10 related keywords with their estimated volume, KD, intent and CPC in a table format]

LONG TAIL KEYWORDS (15):
[List 15 long tail variations with volume and KD]

LSI KEYWORDS (10):
[List 10 LSI keywords]

CONTENT IDEAS (5):
[List 5 blog/content ideas based on this keyword]

QUICK WIN KEYWORDS (5):
[List 5 low KD, decent volume keywords to rank quickly]

Be specific with numbers. Format clearly."""
    result = await call_groq(prompt, 2000)
    return {"keyword": req.keyword, "country": req.country, "research": result, "generated_at": datetime.now().isoformat()}

# 2. BLOG WRITER
@app.post("/api/blog-writer")
async def blog_writer(req: BlogRequest):
    prompt = f"""You are an expert SEO blog writer. Write a complete, publish-ready SEO blog post for the keyword "{req.keyword}".

Website: {req.website_url}
Tone: {req.tone}

Write the COMPLETE blog post with:

SEO META DATA:
- Title Tag (60 chars max): 
- Meta Description (155 chars max):
- URL Slug:
- Focus Keyword:
- Secondary Keywords (5):

COMPLETE BLOG POST:
- H1 Title
- Introduction (150 words, hook + keyword in first 100 words)
- H2 Section 1 with full content (200 words)
- H2 Section 2 with full content (200 words)  
- H2 Section 3 with full content (200 words)
- H2 Section 4 with full content (200 words)
- FAQ Section (5 questions with answers)
- Conclusion with CTA (100 words)

ON-PAGE SEO CHECKLIST:
[10 specific on-page SEO tasks for this post]

INTERNAL LINKING SUGGESTIONS:
[5 internal link anchor text ideas]

Write the FULL blog post — do not summarize, write the actual content."""
    result = await call_groq(prompt, 2000)
    return {"keyword": req.keyword, "blog_post": result, "generated_at": datetime.now().isoformat()}

# 3. GOOGLE ADS SETUP
@app.post("/api/google-ads")
async def google_ads_setup(req: GoogleAdsRequest):
    prompt = f"""You are a Google Ads expert. Create a COMPLETE, ready-to-launch Google Ads campaign for:

Business: {req.business}
Main Keyword: {req.keyword}
Monthly Budget: {req.budget}
Location: {req.location}

Provide EVERYTHING needed to set up the campaign:

CAMPAIGN SETTINGS:
- Campaign Name:
- Campaign Type: Search
- Goal:
- Budget per day: [calculate from monthly]
- Bidding Strategy: [recommend best one]
- Target CPA or ROAS: [realistic number]
- Location targeting:
- Language:
- Ad Schedule: [best hours/days]

AD GROUPS (3 ad groups):
For each ad group:
- Ad Group Name:
- Match Type Keywords (10 exact, 10 phrase, 5 broad match modifier)
- Negative Keywords (10)

AD COPIES (3 ads per ad group = 9 total ads):
For each ad:
- Headline 1 (30 chars):
- Headline 2 (30 chars):
- Headline 3 (30 chars):
- Description 1 (90 chars):
- Description 2 (90 chars):
- Display URL path 1:
- Display URL path 2:

AD EXTENSIONS:
- 4 Sitelink extensions (title + description)
- 4 Callout extensions
- 2 Call extensions
- Structured snippets

BIDDING SETUP:
- Starting bid per keyword: [amount]
- Budget split across ad groups:
- When to increase/decrease bids:

CONVERSION TRACKING:
- What to track
- How to set up

OPTIMIZATION CHECKLIST (first 30 days):
[10 weekly tasks]

Make everything specific and ready to copy-paste into Google Ads."""
    result = await call_groq(prompt, 2000)
    return {"business": req.business, "keyword": req.keyword, "google_ads_setup": result, "generated_at": datetime.now().isoformat()}

# 4. META ADS SETUP
@app.post("/api/meta-ads")
async def meta_ads_setup(req: MetaAdsRequest):
    prompt = f"""You are a Meta Ads (Facebook/Instagram) expert. Create a COMPLETE ready-to-launch Meta Ads campaign for:

Business: {req.business}
Product/Service: {req.product}
Monthly Budget: {req.budget}
Target Age: {req.target_age}
Location: {req.location}

Provide EVERYTHING:

CAMPAIGN STRUCTURE:
- Campaign Name:
- Campaign Objective: [best objective for this business]
- Budget type: CBO or ABO [recommend]
- Daily budget: [calculate]

AD SETS (3 ad sets with different audiences):

AD SET 1 - Cold Audience:
- Name:
- Audience size target:
- Age range:
- Gender:
- Detailed targeting interests (20 specific interests):
- Behaviors:
- Exclude audiences:
- Placement: [automatic or manual - which placements]
- Budget allocation: [% of total]
- Bidding: 

AD SET 2 - Lookalike Audience:
- Name:
- Source audience:
- Lookalike %:
- Additional targeting:
- Budget allocation:

AD SET 3 - Retargeting:
- Name:
- Custom audience:
- Retargeting window:
- Budget allocation:

AD CREATIVES (3 per ad set = 9 total):

For each ad:
- Format: [Image/Video/Carousel/Story]
- Primary Text (125 chars):
- Headline (40 chars):
- Description (30 chars):
- CTA Button:
- Image description: [describe what image should look like]
- Hook (first 3 seconds if video):

PIXEL EVENTS TO TRACK:
[List all events to set up]

A/B TESTING PLAN:
[What to test in week 1, 2, 3, 4]

BUDGET SCALING STRATEGY:
[When and how to scale budget]

MONTHLY OPTIMIZATION CHECKLIST:
[10 tasks]

Make everything specific and ready to set up in Meta Ads Manager."""
    result = await call_groq(prompt, 2000)
    return {"business": req.business, "product": req.product, "meta_ads_setup": result, "generated_at": datetime.now().isoformat()}

# 5. BACKLINK FINDER
@app.post("/api/backlink-finder")
async def backlink_finder(req: BacklinkRequest):
    prompt = f"""You are a link building expert. Find REAL backlink opportunities for:

Keyword: {req.keyword}
Website: {req.website_url}
Niche: {req.niche}

Provide REAL, SPECIFIC websites and opportunities:

GUEST POST OPPORTUNITIES (20 sites):
[List 20 real websites in {req.niche} niche that accept guest posts with their DA and contact method]

DIRECTORY SUBMISSIONS (15):
[List 15 real business/niche directories to submit to]

RESOURCE PAGE OPPORTUNITIES (10):
[List 10 types of resource pages to target with search operators to find them]

BROKEN LINK BUILDING:
- Search operators to find broken links in {req.niche}:
- Tools to use:
- Outreach template:

COMPETITOR BACKLINK SOURCES:
[List 10 types of sites that link to {req.niche} competitors]

READY-TO-SEND OUTREACH EMAILS (3 templates):
1. Guest post pitch
2. Resource page request  
3. Broken link replacement

SOCIAL PROFILE LINKS (15 platforms):
[List 15 platforms to create profiles on for backlinks]

FORUM & COMMUNITY LINKS (10):
[List 10 real forums/communities in {req.niche}]

30-DAY LINK BUILDING CALENDAR:
[Day by day action plan]

Be specific with real website names."""
    result = await call_groq(prompt, 2000)
    return {"keyword": req.keyword, "website": req.website_url, "backlink_opportunities": result, "generated_at": datetime.now().isoformat()}
