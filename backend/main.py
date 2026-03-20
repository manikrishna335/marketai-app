from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os

from seo_agent import keyword_cluster, verify_intent
from content_agent import generate_blog_post
from ads_agent import generate_google_ads, generate_meta_ads, generate_image_prompts
from lp_agent import generate_lp_content, build_html
from backlink_agent import find_competitors, find_contacts, generate_outreach_email, full_backlink_research

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

app = FastAPI(title="MarketMind AI API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class KeywordRequest(BaseModel):
    keyword: str
    persona: Optional[str] = "student"
    country: Optional[str] = "India"

class LandingPageRequest(BaseModel):
    keyword: str
    style: Optional[str] = "auto"
    persona: Optional[str] = "student"

class BlogRequest(BaseModel):
    keyword: str
    secondary_keywords: Optional[list] = []
    persona: Optional[str] = "student"

class GoogleAdsRequest(BaseModel):
    keyword: str
    business: str
    budget: str
    location: Optional[str] = "India"
    avg_cpc: Optional[str] = "1.00"

class MetaAdsRequest(BaseModel):
    business: str
    product: str
    budget: str
    target_age: Optional[str] = "18-35"
    location: Optional[str] = "India"

class ImageRequest(BaseModel):
    keyword: str
    angle: str

class BacklinkRequest(BaseModel):
    keyword: str
    niche: str
    sender_name: Optional[str] = "Our Agency"
    sender_site: Optional[str] = "https://oursite.com"

class ContactRequest(BaseModel):
    domain: str
    niche: str

class OutreachRequest(BaseModel):
    domain: str
    domain_type: Optional[str] = "Blog"
    pitch_angle: Optional[str] = "relevant content"
    keyword: str
    sender_name: str
    sender_site: str

@app.get("/")
def root():
    return {"status": "MarketMind AI API", "version": "2.0", "agents": ["seo","content","ads","lp","backlink"]}

@app.post("/api/keyword-cluster")
async def api_keyword_cluster(req: KeywordRequest):
    result = await keyword_cluster(req.keyword, req.persona, req.country)
    return {**result, "generated_at": datetime.now().isoformat()}

@app.post("/api/verify-intent")
async def api_verify_intent(req: KeywordRequest):
    result = await verify_intent(req.keyword, req.persona)
    return {**result, "generated_at": datetime.now().isoformat()}

# Landing page returns FULL HTML
@app.post("/api/landing-page")
async def api_landing_page(req: LandingPageRequest):
    data = await generate_lp_content(req.keyword, req.style or "auto", req.persona)
    if not data:
        return {"keyword": req.keyword, "landing_page": "Error generating content", "html": ""}
    html = build_html(req.keyword, data)
    return {
        "keyword": req.keyword,
        "style": data.get("style_recommendation", "auto"),
        "landing_page": html,
        "html": html,
        "generated_at": datetime.now().isoformat()
    }

# Live landing page URL endpoint - returns actual HTML page
@app.get("/lp/{keyword}")
async def live_landing_page(keyword: str, persona: str = "student"):
    kw = keyword.replace("-", " ")
    data = await generate_lp_content(kw, "auto", persona)
    if not data:
        return HTMLResponse("<h1>Error generating page</h1>", status_code=500)
    html = build_html(kw, data)
    return HTMLResponse(content=html)

@app.post("/api/blog-post")
async def api_blog_post(req: BlogRequest):
    result = await generate_blog_post(req.keyword, req.secondary_keywords, req.persona)
    return {"keyword": req.keyword, "blog_post": result, "generated_at": datetime.now().isoformat()}

# Google Ads returns structured JSON with images
@app.post("/api/google-ads")
async def api_google_ads(req: GoogleAdsRequest):
    result = await generate_google_ads(req.keyword, req.business, req.budget, req.location, req.avg_cpc)
    return {"keyword": req.keyword, "business": req.business, "google_ads": result, "generated_at": datetime.now().isoformat()}

# Meta Ads returns structured JSON with images
@app.post("/api/meta-ads")
async def api_meta_ads(req: MetaAdsRequest):
    result = await generate_meta_ads(req.business, req.product, req.budget, req.target_age, req.location)
    return {"business": req.business, "meta_ads": result, "generated_at": datetime.now().isoformat()}

@app.post("/api/image-prompts")
async def api_image_prompts(req: ImageRequest):
    result = await generate_image_prompts(req.keyword, req.angle)
    return {"keyword": req.keyword, "angle": req.angle, "image_prompts": result, "generated_at": datetime.now().isoformat()}

@app.post("/api/backlink-research")
async def api_backlink_research(req: BacklinkRequest):
    data = await full_backlink_research(req.keyword, req.niche, req.sender_name, req.sender_site)
    return {**data, "generated_at": datetime.now().isoformat()}

@app.post("/api/find-contacts")
async def api_find_contacts(req: ContactRequest):
    data = await find_contacts(req.domain, req.niche)
    return {**data, "generated_at": datetime.now().isoformat()}

@app.post("/api/outreach-emails")
async def api_outreach_emails(req: OutreachRequest):
    target = {"domain": req.domain, "type": req.domain_type, "pitch_angle": req.pitch_angle}
    data = await generate_outreach_email(target, req.keyword, req.sender_name, req.sender_site)
    return {**data, "generated_at": datetime.now().isoformat()}
