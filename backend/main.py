from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import httpx
import os
import json
import re
from datetime import datetime

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

app = FastAPI(title="AI Marketing Automation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Models ───────────────────────────────────────────────────────────────────

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
    platform: str  # google or meta

class ReportRequest(BaseModel):
    client_name: str
    website_url: str
    period: str  # e.g. "March 2025"

class OutreachRequest(BaseModel):
    prospect_name: str
    prospect_business: str
    your_agency_name: str
    service_offered: str

# ─── Gemini API Call Helper ────────────────────────────────────────────────

async def call_claude(prompt: str, system: str = "") -> str:
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    body = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {"maxOutputTokens": 1500, "temperature": 0.7}
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, json=body)
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "AI Marketing Automation API running"}

# 1. SEO Automation
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

    result = await call_claude(prompt, system="You are a top SEO expert who gives precise, actionable advice to rank websites in Google top 10.")
    return {
        "keyword": req.keyword,
        "website": req.website_url,
        "seo_strategy": result,
        "generated_at": datetime.now().isoformat()
    }

# 2. Backlink Automation
@app.post("/api/backlinks")
async def backlink_automation(req: BacklinkRequest):
    prompt = f"""Create a complete backlink building plan for a "{req.niche}" business at "{req.website_url}".

1. GUEST POST OUTREACH EMAIL - ready to send template
2. TOP 20 BACKLINK SOURCES - specific websites/directories in {req.niche} niche
3. RESOURCE PAGE OUTREACH - email template + how to find resource pages
4. BROKEN LINK BUILDING - step by step process
5. HARO/PR STRATEGY - how to get high DA backlinks
6. SOCIAL PROFILE LINKS - top 10 platforms to create profiles on
7. WEEKLY BACKLINK SCHEDULE - what to do each day

Make it 100% actionable with real tactics."""

    result = await call_claude(prompt, system="You are a link building expert. Give specific, white-hat backlink strategies that actually work in 2025.")
    return {
        "niche": req.niche,
        "website": req.website_url,
        "backlink_plan": result,
        "generated_at": datetime.now().isoformat()
    }

# 3. Paid Ads Automation
@app.post("/api/ads")
async def ads_automation(req: AdsRequest):
    prompt = f"""Create a complete {req.platform.upper()} ads campaign strategy for:
- Business: {req.business_type}
- Target Audience: {req.target_audience}
- Budget: {req.budget}/month

Provide:
1. CAMPAIGN STRUCTURE - campaigns, ad sets, targeting breakdown
2. 5 AD COPIES - headlines, descriptions, CTAs (ready to use)
3. AUDIENCE TARGETING - exact demographics, interests, behaviors
4. BIDDING STRATEGY - which bidding type and why
5. KEYWORDS LIST (if Google) or INTEREST TARGETS (if Meta) - 20 specific ones
6. AD BUDGET SPLIT - how to distribute the {req.budget}
7. OPTIMIZATION CHECKLIST - what to check daily/weekly
8. KPIs TO TRACK - benchmarks for success

Make ads ready to copy-paste into the ads manager."""

    result = await call_claude(prompt, system=f"You are a certified {req.platform} ads expert managing $1M+ in ad spend. Give precise, high-converting ad strategies.")
    return {
        "platform": req.platform,
        "business": req.business_type,
        "ads_strategy": result,
        "generated_at": datetime.now().isoformat()
    }

# 4. Client Report Generator
@app.post("/api/report")
async def report_automation(req: ReportRequest):
    prompt = f"""Generate a professional monthly marketing report for:
- Client: {req.client_name}
- Website: {req.website_url}
- Period: {req.period}

Create a complete report with:
1. EXECUTIVE SUMMARY - key wins this month
2. SEO PERFORMANCE - traffic overview, ranking improvements, top keywords
3. PAID ADS PERFORMANCE - impressions, clicks, CTR, conversions, ROAS
4. BACKLINK PROGRESS - new links acquired, DA improvements
5. SOCIAL MEDIA METRICS - engagement, followers, reach
6. CONTENT PUBLISHED - articles, pages created
7. NEXT MONTH PLAN - top 5 priorities
8. RECOMMENDATIONS - 3 strategic improvements

Format as a professional agency report. Use placeholder numbers but realistic ones."""

    result = await call_claude(prompt, system="You are a marketing agency account manager creating impressive client reports that demonstrate value and retain clients.")
    return {
        "client": req.client_name,
        "period": req.period,
        "report": result,
        "generated_at": datetime.now().isoformat()
    }

# 5. Outreach Email Generator
@app.post("/api/outreach")
async def outreach_automation(req: OutreachRequest):
    prompt = f"""Write 3 different cold outreach email variants for:
- Prospect: {req.prospect_name} at {req.prospect_business}
- Our Agency: {req.your_agency_name}
- Service: {req.service_offered}

For each email write:
- Subject line (5 options)
- Email body (personalized, not salesy)
- Follow-up email (send after 3 days)

Also provide:
- LinkedIn connection message (under 300 chars)
- LinkedIn follow-up DM
- Cold call script (30 seconds)

Make them human, genuine, and conversion-focused. Not robotic."""

    result = await call_claude(prompt, system="You are a top sales copywriter who writes outreach that gets 40%+ reply rates. Never sound like an AI or generic agency.")
    return {
        "prospect": req.prospect_name,
        "service": req.service_offered,
        "outreach_kit": result,
        "generated_at": datetime.now().isoformat()
    }

# 6. Full Organic Strategy
@app.post("/api/organic-strategy")
async def organic_strategy(req: SEORequest):
    prompt = f"""Build a complete organic growth strategy to get "{req.website_url}" ranking in Google Top 10 for "{req.keyword}".

Cover ALL organic channels:
1. BLOG CONTENT CALENDAR - 12 weeks of topics
2. YOUTUBE SEO - video titles, descriptions for 5 videos
3. GOOGLE BUSINESS PROFILE - optimization checklist
4. REDDIT/QUORA STRATEGY - how to drive traffic
5. PINTEREST SEO - board and pin strategy
6. LINKEDIN ORGANIC - post ideas for authority building
7. GUEST BLOGGING PIPELINE - outreach to 10 sites
8. SCHEMA MARKUP - which schemas to add
9. CORE WEB VITALS - how to improve page speed
10. INTERNAL LINKING MAP - how to structure site links

Give a 90-day roadmap at the end."""

    result = await call_claude(prompt, system="You are a holistic organic growth expert. Give a complete multi-channel strategy that dominates search results.")
    return {
        "keyword": req.keyword,
        "website": req.website_url,
        "organic_strategy": result,
        "generated_at": datetime.now().isoformat()
    }
