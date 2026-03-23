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
from lp_agent import generate_lp_content, build_html_with_images
from backlink_agent import find_competitors, find_contacts, generate_outreach_email, full_backlink_research
from image_service import get_unsplash_image

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

class ImgProxyRequest(BaseModel):
    query: str
    width: Optional[int] = 1200
    height: Optional[int] = 628
    orientation: Optional[str] = "landscape"

@app.get("/")
def root():
    return {"status": "MarketMind AI API", "version": "2.0"}

# Image proxy endpoint - frontend calls this to get real image URLs
@app.post("/api/get-image")
async def api_get_image(req: ImgProxyRequest):
    url = await get_unsplash_image(req.query, req.width, req.height, req.orientation)
    return {"url": url, "query": req.query}

@app.get("/api/get-image")
async def api_get_image_get(query: str, w: int = 1200, h: int = 628, ori: str = "landscape"):
    url = await get_unsplash_image(query, w, h, ori)
    return {"url": url}

@app.post("/api/keyword-cluster")
async def api_keyword_cluster(req: KeywordRequest):
    result = await keyword_cluster(req.keyword, req.persona, req.country)
    return {**result, "generated_at": datetime.now().isoformat()}

@app.post("/api/landing-page")
async def api_landing_page(req: LandingPageRequest):
    data = await generate_lp_content(req.keyword, req.style or "auto", req.persona)
    if not data:
        return {"keyword": req.keyword, "html": "<h1>Error generating content</h1>", "style": "auto"}
    html = await build_html_with_images(req.keyword, data)
    return {
        "keyword": req.keyword,
        "style": data.get("style_recommendation", "auto"),
        "html": html,
        "landing_page": html,
        "generated_at": datetime.now().isoformat()
    }

@app.get("/lp/{keyword}")
async def live_landing_page(keyword: str, persona: str = "student"):
    kw = keyword.replace("-", " ")
    data = await generate_lp_content(kw, "auto", persona)
    if not data:
        return HTMLResponse("<h1>Error</h1>", status_code=500)
    html = await build_html_with_images(kw, data)
    return HTMLResponse(content=html)

@app.post("/api/blog-post")
async def api_blog_post(req: BlogRequest):
    result = await generate_blog_post(req.keyword, req.secondary_keywords, req.persona)
    return {"keyword": req.keyword, "blog_post": result, "generated_at": datetime.now().isoformat()}

@app.post("/api/google-ads")
async def api_google_ads(req: GoogleAdsRequest):
    result = await generate_google_ads(req.keyword, req.business, req.budget, req.location, req.avg_cpc)
    # Fetch real images for each ad format
    if isinstance(result, dict) and 'ad_formats' in result:
        import asyncio
        for fmt in result['ad_formats']:
            q = fmt.get('_img_query') or fmt.get('image_query', req.keyword)
            fmt['image_url'] = await get_unsplash_image(q, 1200, 628, 'landscape')
            fmt['square_url'] = await get_unsplash_image(q, 400, 400, 'squarish')
    return {"keyword": req.keyword, "business": req.business, "google_ads": result, "generated_at": datetime.now().isoformat()}

@app.post("/api/meta-ads")
async def api_meta_ads(req: MetaAdsRequest):
    result = await generate_meta_ads(req.business, req.product, req.budget, req.target_age, req.location)
    # Fetch real images for formats and ad sets
    if isinstance(result, dict):
        for fmt in result.get('ad_formats', []):
            q = fmt.get('_img_query') or fmt.get('image_query', req.product)
            ori = 'portrait' if fmt.get('ratio','') == '9:16' else 'landscape'
            fmt['image_url'] = await get_unsplash_image(q, 1200, 628, ori)
            if 'cards' in fmt:
                import asyncio
                for card in fmt['cards']:
                    cq = card.get('_img_query') or card.get('image_query', req.product)
                    card['image_url'] = await get_unsplash_image(cq, 400, 400, 'squarish')
        for adset in result.get('ad_sets', []):
            q = adset.get('_img_query') or adset.get('image_query', req.product)
            adset['image_url'] = await get_unsplash_image(q, 800, 420, 'landscape')
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
