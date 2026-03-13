from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import httpx
import os
from datetime import datetime

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

app = FastAPI(title="AI Marketing Automation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SEORequest(BaseModel):
    keyword: str
    website_url: Optional[str] = ""

class BacklinkRequest(BaseModel):
    niche: str
    website_url: str
    contact_email: Optional[str] = ""

class AdsRequest(BaseModel):
    business_type: str
    target_audience: str
    budget: str
    platform: str

class ReportRequest(BaseModel):
    client_name: str
    website_url: str
    period: str

class OutreachRequest(BaseModel):
    prospect_name: str
    prospect_business: str
    your_agency_name: str
    service_offered: str

async def call_groq(prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1500,
        "temperature": 0.7
    }
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, headers=headers, json=body)
            data = r.json()
            if "choices" in data:
                return data["choices"][0]["message"]["content"]
            else:
                return f"API Error: {data.get('error', {}).get('message', str(data))}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.get("/")
def root():
    return {"status": "AI Marketing Automation API running", "model": "Groq Llama 3.3 70B"}

@app.post("/api/seo")
async def seo_automation(req: SEORequest):
    prompt = f"""You are an expert SEO strategist. For the keyword "{req.keyword}" and website "{req.website_url}", provide:
1. TOP 10 RANKING STRATEGY - exact steps to rank in top 10
2. CONTENT BRIEF - title, meta description, H1, H2s, word count, LSI keywords
3. ON-PAGE SEO CHECKLIST - 10 specific action items
4. BACKLINK TARGETS - 5 types of sites to get backlinks from
5. TECHNICAL SEO FIXES - 5 common fixes needed
6. TIMELINE - realistic weeks to reach top 10
Format clearly with headers. Be specific and actionable."""
    result = await call_groq(prompt)
    return {"keyword": req.keyword, "website": req.website_url, "seo_strategy": result, "generated_at": datetime.now().isoformat()}

@app.post("/api/backlinks")
async def backlink_automation(req: BacklinkRequest):
    prompt = f"""Create a complete backlink building plan for a "{req.niche}" business at "{req.website_url}".
1. GUEST POST OUTREACH EMAIL - ready to send template
2. TOP 20 BACKLINK SOURCES - specific websites in {req.niche} niche
3. RESOURCE PAGE OUTREACH - email template
4. BROKEN LINK BUILDING - step by step
5. HARO/PR STRATEGY
6. SOCIAL PROFILE LINKS - top 10 platforms
7. WEEKLY BACKLINK SCHEDULE"""
    result = await call_groq(prompt)
    return {"niche": req.niche, "website": req.website_url, "backlink_plan": result, "generated_at": datetime.now().isoformat()}

@app.post("/api/ads")
async def ads_automation(req: AdsRequest):
    prompt = f"""Create a complete {req.platform.upper()} ads campaign for:
Business: {req.business_type}, Audience: {req.target_audience}, Budget: {req.budget}/month
1. CAMPAIGN STRUCTURE
2. 5 AD COPIES ready to use
3. AUDIENCE TARGETING
4. BIDDING STRATEGY
5. 20 KEYWORDS/INTERESTS
6. BUDGET SPLIT
7. OPTIMIZATION CHECKLIST
8. KPIs"""
    result = await call_groq(prompt)
    return {"platform": req.platform, "business": req.business_type, "ads_strategy": result, "generated_at": datetime.now().isoformat()}

@app.post("/api/report")
async def report_automation(req: ReportRequest):
    prompt = f"""Generate a professional monthly marketing report for client: {req.client_name}, website: {req.website_url}, period: {req.period}.
Include: Executive Summary, SEO Performance, Paid Ads Performance, Backlink Progress, Social Media, Content Published, Next Month Plan, Recommendations."""
    result = await call_groq(prompt)
    return {"client": req.client_name, "period": req.period, "report": result, "generated_at": datetime.now().isoformat()}

@app.post("/api/outreach")
async def outreach_automation(req: OutreachRequest):
    prompt = f"""Write 3 cold outreach email variants for prospect: {req.prospect_name} at {req.prospect_business}.
Our agency: {req.your_agency_name}, Service: {req.service_offered}.
For each: 5 subject line options, email body, follow-up email.
Also include: LinkedIn message, LinkedIn DM, 30-second cold call script."""
    result = await call_groq(prompt)
    return {"prospect": req.prospect_name, "service": req.service_offered, "outreach_kit": result, "generated_at": datetime.now().isoformat()}

@app.post("/api/organic-strategy")
async def organic_strategy(req: SEORequest):
    prompt = f"""Build complete organic growth strategy for "{req.website_url}" for keyword "{req.keyword}".
1. BLOG CONTENT CALENDAR - 12 weeks
2. YOUTUBE SEO - 5 video ideas
3. GOOGLE BUSINESS PROFILE checklist
4. REDDIT/QUORA STRATEGY
5. PINTEREST SEO
6. LINKEDIN ORGANIC posts
7. GUEST BLOGGING PIPELINE
8. SCHEMA MARKUP
9. CORE WEB VITALS improvements
10. INTERNAL LINKING MAP
Give 90-day roadmap at end."""
    result = await call_groq(prompt)
    return {"keyword": req.keyword, "website": req.website_url, "organic_strategy": result, "generated_at": datetime.now().isoformat()}
