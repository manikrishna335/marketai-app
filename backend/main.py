from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from seo_agent import keyword_cluster, verify_intent
from content_agent import generate_landing_page, generate_blog_post
from ads_agent import generate_google_ads, generate_meta_ads, generate_image_prompts

app = FastAPI(title="MarketAI Phase 1 API")

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
    style: str  # minimalist, tech, academic
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
    angle: str  # emotional, logical, scarcity

@app.get("/")
def root():
    return {"status": "MarketAI Phase 1 API", "version": "1.0", "agents": ["seo_agent", "content_agent", "ads_agent"]}

@app.post("/api/keyword-cluster")
async def api_keyword_cluster(req: KeywordRequest):
    result = await keyword_cluster(req.keyword, req.persona, req.country)
    return {**result, "generated_at": datetime.now().isoformat()}

@app.post("/api/verify-intent")
async def api_verify_intent(req: KeywordRequest):
    result = await verify_intent(req.keyword, req.persona)
    return {**result, "generated_at": datetime.now().isoformat()}

@app.post("/api/landing-page")
async def api_landing_page(req: LandingPageRequest):
    result = await generate_landing_page(req.keyword, req.style, req.persona)
    return {"keyword": req.keyword, "style": req.style, "landing_page": result, "generated_at": datetime.now().isoformat()}

@app.post("/api/blog-post")
async def api_blog_post(req: BlogRequest):
    result = await generate_blog_post(req.keyword, req.secondary_keywords, req.persona)
    return {"keyword": req.keyword, "blog_post": result, "generated_at": datetime.now().isoformat()}

@app.post("/api/google-ads")
async def api_google_ads(req: GoogleAdsRequest):
    result = await generate_google_ads(req.keyword, req.business, req.budget, req.location, req.avg_cpc)
    return {"keyword": req.keyword, "business": req.business, "google_ads": result, "generated_at": datetime.now().isoformat()}

@app.post("/api/meta-ads")
async def api_meta_ads(req: MetaAdsRequest):
    result = await generate_meta_ads(req.business, req.product, req.budget, req.target_age, req.location)
    return {"business": req.business, "meta_ads": result, "generated_at": datetime.now().isoformat()}

@app.post("/api/image-prompts")
async def api_image_prompts(req: ImageRequest):
    result = await generate_image_prompts(req.keyword, req.angle)
    return {"keyword": req.keyword, "angle": req.angle, "image_prompts": result, "generated_at": datetime.now().isoformat()}

@app.post("/api/full-campaign")
async def api_full_campaign(req: KeywordRequest):
    """Generate everything at once — keyword cluster + all 3 landing pages"""
    cluster = await keyword_cluster(req.keyword, req.persona, req.country)
    lp_min = await generate_landing_page(req.keyword, "minimalist", req.persona)
    lp_tech = await generate_landing_page(req.keyword, "tech", req.persona)
    lp_acad = await generate_landing_page(req.keyword, "academic", req.persona)
    return {
        "keyword": req.keyword,
        "keyword_cluster": cluster["cluster"],
        "landing_pages": {
            "minimalist": lp_min,
            "tech": lp_tech,
            "academic": lp_acad
        },
        "generated_at": datetime.now().isoformat()
    }

# ─── BACKLINK OUTREACH SYSTEM ──────────────────────────────────────────────
from backlink_agent import find_competitors, find_contacts, generate_outreach_email, full_backlink_research

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
