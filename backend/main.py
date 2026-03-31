# ============================================================
# MarketMind AI — COMPLETE main.py (ALL endpoints)
# Version: 3.0 FINAL
# Includes: SEO, Landing Page, Blog, Google Ads, Meta Ads,
#           Image Prompts, Backlink CRM, Lead Generation
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os, httpx, json, re, asyncio

# ── GROQ API ─────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
UNSPLASH_KEY = "uzuoQOhJhBAPA3oZLUrM5caab91nTcIwrB92kEbX87k"

app = FastAPI(title="MarketMind AI API", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── HELPERS ───────────────────────────────────────────────────
async def call_groq(prompt: str, max_tokens: int = 2000) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    body = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": 0.7}
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, headers=headers, json=body)
            data = r.json()
            if "choices" in data:
                return data["choices"][0]["message"]["content"]
            return f"Error: {data.get('error', {}).get('message', str(data))}"
    except Exception as e:
        return f"Error: {str(e)}"

async def get_image(query: str, w: int = 1200, h: int = 628, orientation: str = "landscape") -> str:
    try:
        params = {"query": query, "client_id": UNSPLASH_KEY, "orientation": orientation}
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get("https://api.unsplash.com/photos/random", params=params)
            if r.status_code == 200:
                data = r.json()
                url = data.get("urls", {}).get("regular", "")
                if url:
                    return f"{url}&w={w}&h={h}&fit=crop&crop=center"
    except:
        pass
    seed = abs(hash(query)) % 1000
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"

def parse_json(raw: str):
    try:
        clean = re.sub(r'```json|```', '', raw).strip()
        return json.loads(clean)
    except:
        return None

# ── MODELS ────────────────────────────────────────────────────
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

class LeadRequest(BaseModel):
    service: str
    location: Optional[str] = "India"
    company_name: Optional[str] = "Our Company"

class OutreachRequest(BaseModel):
    company: str
    contact: str
    role: str
    pain_point: str
    service: str
    sender_company: Optional[str] = "Our Company"

class ImgProxyRequest(BaseModel):
    query: str
    width: Optional[int] = 1200
    height: Optional[int] = 628
    orientation: Optional[str] = "landscape"

# ── ROOT ──────────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "status": "MarketMind AI API",
        "version": "3.0",
        "endpoints": [
            "/api/keyword-cluster",
            "/api/landing-page",
            "/api/blog-post",
            "/api/google-ads",
            "/api/meta-ads",
            "/api/image-prompts",
            "/api/backlink-research",
            "/api/find-contacts",
            "/api/lead-research",
            "/api/competitors",
            "/api/find-leads",
            "/api/generate-outreach",
            "/api/get-image"
        ]
    }

# ── IMAGE PROXY ───────────────────────────────────────────────
@app.post("/api/get-image")
async def api_get_image(req: ImgProxyRequest):
    url = await get_image(req.query, req.width, req.height, req.orientation)
    return {"url": url, "query": req.query}

@app.get("/api/get-image")
async def api_get_image_get(query: str, w: int = 1200, h: int = 628, ori: str = "landscape"):
    url = await get_image(query, w, h, ori)
    return {"url": url}

# ═══════════════════════════════════════════════════════════════
# 1. KEYWORD CLUSTER
# ═══════════════════════════════════════════════════════════════
@app.post("/api/keyword-cluster")
async def api_keyword_cluster(req: KeywordRequest):
    prompt = f"""SEO keyword researcher. Analyze "{req.keyword}" for {req.country} market. Target persona: {req.persona}.

KEYWORD OVERVIEW:
- Main Keyword: {req.keyword}
- Estimated Monthly Search Volume: [realistic number]
- Keyword Difficulty (KD): [0-100]
- Search Intent: [Informational/Commercial/Transactional]
- CPC: [realistic USD]
- Competition: [Low/Medium/High]
- Persona Match: [verify matches {req.persona}]

1+4 KEYWORD CLUSTER:
PRIMARY (Transactional): {req.keyword} | Vol: | KD: | CPC:
HOW-TO: "how to {req.keyword}" | Vol: | KD: | CPC:
COST: "{req.keyword} cost price" | Vol: | KD: | CPC:
COMPARISON: "best {req.keyword} vs" | Vol: | KD: | CPC:
BENEFITS: "{req.keyword} benefits" | Vol: | KD: | CPC:

LONG TAIL KEYWORDS (10): [list with Vol, KD, Intent]
QUICK WIN KEYWORDS (5 low KD): [under KD 30]
COMPETITOR SITES (top 5): [likely ranking sites]
CONTENT GAP OPPORTUNITIES (3): [missing angles]
RECOMMENDED STRATEGY: [3-step plan]"""

    result = await call_groq(prompt, 2000)
    return {"keyword": req.keyword, "persona": req.persona, "country": req.country, "cluster": result, "generated_at": datetime.now().isoformat()}

# ═══════════════════════════════════════════════════════════════
# 2. LANDING PAGE — Full HTML with Real Images
# ═══════════════════════════════════════════════════════════════
@app.post("/api/landing-page")
async def api_landing_page(req: LandingPageRequest):
    prompt = f"""Generate landing page content for "{req.keyword}", persona "{req.persona}". Return ONLY valid JSON:
{{
  "primary_color": "#6C5CE7",
  "hero": {{"headline": "7-word headline", "subheadline": "20-word solution", "cta": "Get Started Free", "trust_line": "Join 10,000+ students", "image_query": "student studying laptop focused"}},
  "pain_points": {{"headline": "Pain headline", "cards": [{{"icon":"😓","title":"Pain 1","desc":"12 word desc","image_query":"stressed student"}},{{"icon":"😰","title":"Pain 2","desc":"12 word desc","image_query":"confused student"}},{{"icon":"😤","title":"Pain 3","desc":"12 word desc","image_query":"frustrated person"}},{{"icon":"😩","title":"Pain 4","desc":"12 word desc","image_query":"anxious student"}}]}},
  "features": {{"headline": "Features headline", "image_query": "learning success", "items": [{{"icon":"✅","title":"Feature","desc":"15 word benefit"}},{{"icon":"🚀","title":"Feature","desc":"15 word benefit"}},{{"icon":"💡","title":"Feature","desc":"15 word benefit"}},{{"icon":"🎯","title":"Feature","desc":"15 word benefit"}},{{"icon":"📊","title":"Feature","desc":"15 word benefit"}},{{"icon":"🏆","title":"Feature","desc":"15 word benefit"}}]}},
  "social_proof": {{"headline": "Proof headline", "image_query": "happy students success", "metrics": [{{"number":"10,000+","label":"Students"}},{{"number":"98%","label":"Success Rate"}},{{"number":"4.9★","label":"Rating"}},{{"number":"50+","label":"Tutors"}}], "testimonials": [{{"name":"Priya S.","role":"IB Student","quote":"25 word quote","avatar_query":"indian girl student"}},{{"name":"Arjun K.","role":"Grade 12","quote":"25 word quote","avatar_query":"indian boy student"}},{{"name":"Meera R.","role":"Parent","quote":"25 word quote","avatar_query":"indian parent"}}]}},
  "comparison": {{"headline": "Why us headline", "rows": [{{"feature":"Speed","old":"Slow old way","new":"Fast new way"}},{{"feature":"Cost","old":"Expensive","new":"Affordable"}},{{"feature":"Support","old":"Limited","new":"24/7"}},{{"feature":"Results","old":"No guarantee","new":"Guaranteed"}},{{"feature":"Access","old":"Fixed hours","new":"Anytime"}},{{"feature":"Quality","old":"Generic","new":"Personalized"}},{{"feature":"Progress","old":"Unknown","new":"Tracked"}},{{"feature":"Flexibility","old":"Fixed","new":"Flexible"}}]}},
  "cta_faq": {{"headline": "Start today headline", "subtext": "15-word close", "cta": "Book Free Demo", "urgency": "Only 8 spots left", "bg_image_query": "graduation success", "faqs": [{{"q":"How fast results?","a":"20-word answer"}},{{"q":"Satisfaction guarantee?","a":"20-word answer"}},{{"q":"Own schedule?","a":"20-word answer"}},{{"q":"Tutor quality?","a":"20-word answer"}},{{"q":"Free trial?","a":"20-word answer"}}]}}
}}"""

    raw = await call_groq(prompt, 2000)
    data = parse_json(raw)
    if not data:
        return {"keyword": req.keyword, "html": "<h1>Error generating content. Try again.</h1>", "style": "auto"}

    # Fetch ALL images via backend
    h = data.get('hero', {})
    pp = data.get('pain_points', {})
    ft = data.get('features', {})
    sp = data.get('social_proof', {})
    cf = data.get('cta_faq', {})
    primary = data.get('primary_color', '#6C5CE7')

    pain_cards = pp.get('cards', [])
    testis = sp.get('testimonials', [])

    queries = [(h.get('image_query','student studying'),1400,800,'landscape'),(ft.get('image_query','learning success'),1200,400,'landscape'),(sp.get('image_query','students success'),1200,300,'landscape'),(cf.get('bg_image_query','graduation'),1400,500,'landscape')] + [(c.get('image_query','student'),480,260,'landscape') for c in pain_cards] + [(t.get('avatar_query','person'),80,80,'squarish') for t in testis]

    imgs = await asyncio.gather(*[get_image(q,w,h_,o) for q,w,h_,o in queries])
    hero_img,feat_img,proof_img,cta_img = imgs[0],imgs[1],imgs[2],imgs[3]
    pain_imgs = imgs[4:4+len(pain_cards)]
    av_imgs = imgs[4+len(pain_cards):]

    pain_html = "".join([f'<div class="pain-card"><div class="pain-img"><img src="{pain_imgs[i] if i<len(pain_imgs) else ""}" alt="{c["title"]}" loading="lazy"/></div><div class="pc-body"><span class="pc-icon">{c["icon"]}</span><h3>{c["title"]}</h3><p>{c["desc"]}</p></div></div>' for i,c in enumerate(pain_cards)])
    feat_html = "".join([f'<div class="feat-item"><div class="fi">{f["icon"]}</div><div><h3>{f["title"]}</h3><p>{f["desc"]}</p></div></div>' for f in ft.get('items',[])])
    metrics_html = "".join([f'<div class="metric"><div class="mn">{m["number"]}</div><div class="ml">{m["label"]}</div></div>' for m in sp.get('metrics',[])])
    testis_html = "".join([f'<div class="testi"><div class="stars">★★★★★</div><p>"{t["quote"]}"</p><div class="tw"><img src="{av_imgs[i] if i<len(av_imgs) else ""}" alt="{t["name"]}"/><div><strong>{t["name"]}</strong><span>{t["role"]}</span></div></div></div>' for i,t in enumerate(testis)])
    rows_html = "".join([f"<tr><td class='f'>{r['feature']}</td><td class='o'>✗ {r['old']}</td><td class='n'>✓ {r['new']}</td></tr>" for r in data.get('comparison',{}).get('rows',[])])
    faqs_html = "".join([f'<div class="faq"><button onclick="this.classList.toggle(\'o\');this.nextElementSibling.classList.toggle(\'s\')">{f["q"]}<span>+</span></button><div class="fa"><p>{f["a"]}</p></div></div>' for f in cf.get('faqs',[])])

    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/><title>{h.get('headline',req.keyword)}</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'DM Sans',sans-serif;background:#fafaf8;color:#1a1a1a;line-height:1.7;overflow-x:hidden}}
img{{max-width:100%;display:block}}
nav{{position:fixed;top:0;left:0;right:0;z-index:100;padding:14px 48px;display:flex;align-items:center;justify-content:space-between;background:rgba(250,250,248,.96);backdrop-filter:blur(12px);border-bottom:1px solid #e5e7eb}}
.nav-logo{{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700}}
.nav-cta{{background:{primary};color:#fff;padding:10px 24px;border:none;border-radius:8px;font-weight:700;font-size:.88rem;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .2s}}
.nav-cta:hover{{opacity:.9;transform:translateY(-1px)}}
.hero{{min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;position:relative;overflow:hidden}}
.hero-bg{{position:absolute;inset:0}}.hero-bg img{{width:100%;height:100%;object-fit:cover}}
.hero-ov{{position:absolute;inset:0;background:linear-gradient(135deg,rgba(0,0,0,.72),rgba(0,0,0,.45))}}
.hero-c{{position:relative;z-index:2;max-width:780px;padding:120px 32px 80px;color:#fff}}
.hero-tag{{display:inline-block;background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);padding:7px 20px;border-radius:20px;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;margin-bottom:24px}}
.hero h1{{font-family:'Playfair Display',serif;font-size:clamp(2.2rem,5.5vw,4rem);font-weight:800;line-height:1.08;margin-bottom:20px}}
.hero p{{font-size:1.05rem;opacity:.9;margin-bottom:36px;max-width:560px;margin-left:auto;margin-right:auto}}
.btn{{background:{primary};color:#fff;padding:17px 40px;border:none;border-radius:10px;font-weight:700;font-size:1rem;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .25s}}
.btn:hover{{opacity:.92;transform:translateY(-2px);box-shadow:0 10px 28px rgba(0,0,0,.3)}}
.trust{{margin-top:20px;font-size:.8rem;opacity:.8}}
.logos{{padding:22px 48px;background:#fff;border-bottom:1px solid #e5e7eb;display:flex;align-items:center;justify-content:center;gap:44px;flex-wrap:wrap}}
.lt{{font-size:.75rem;font-weight:700;color:#c8c8c8;letter-spacing:.06em;text-transform:uppercase}}
section{{padding:88px 48px}}
.inner{{max-width:1120px;margin:0 auto}}
.so{{font-size:.63rem;text-transform:uppercase;letter-spacing:.18em;color:{primary};font-weight:700;margin-bottom:10px;display:block}}
.st{{font-family:'Playfair Display',serif;font-size:clamp(1.7rem,3.2vw,2.7rem);font-weight:700;margin-bottom:38px;line-height:1.15}}
.pain-section{{background:#f3f4f6}}
.pain-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px}}
.pain-card{{background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.06);transition:all .28s}}
.pain-card:hover{{transform:translateY(-5px);box-shadow:0 14px 32px rgba(0,0,0,.1)}}
.pain-img{{height:190px;overflow:hidden}}.pain-img img{{width:100%;height:190px;object-fit:cover;transition:transform .4s}}
.pain-card:hover .pain-img img{{transform:scale(1.06)}}
.pc-body{{padding:20px}}.pc-icon{{font-size:1.7rem;display:block;margin-bottom:9px}}
.pc-body h3{{font-size:.98rem;font-weight:700;margin-bottom:6px}}.pc-body p{{font-size:.83rem;color:#6b7280}}
.feat-section{{background:#fff}}
.feat-img{{width:100%;height:320px;object-fit:cover;border-radius:18px;margin-bottom:48px;box-shadow:0 16px 48px rgba(0,0,0,.1)}}
.feat-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:18px}}
.feat-item{{background:#f8f9fa;border:1px solid #e5e7eb;border-radius:14px;padding:24px;display:flex;gap:16px;align-items:flex-start;transition:all .22s}}
.feat-item:hover{{border-color:{primary};background:#fff}}.fi{{font-size:1.7rem;flex-shrink:0}}
.feat-item h3{{font-size:.93rem;font-weight:700;margin-bottom:5px}}.feat-item p{{font-size:.81rem;color:#6b7280}}
.proof-section{{background:#f3f4f6}}
.proof-img{{width:100%;height:240px;object-fit:cover;border-radius:16px;margin-bottom:48px;box-shadow:0 12px 36px rgba(0,0,0,.08)}}
.metrics-row{{display:flex;justify-content:center;gap:52px;flex-wrap:wrap;margin-bottom:52px;padding:30px 0;border-top:1px solid #e5e7eb;border-bottom:1px solid #e5e7eb}}
.metric{{text-align:center}}.mn{{font-family:'Playfair Display',serif;font-size:2.4rem;font-weight:700;color:{primary}}}.ml{{font-size:.7rem;color:#9ca3af;text-transform:uppercase;letter-spacing:.1em;margin-top:6px}}
.testi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:20px}}
.testi{{background:#fff;box-shadow:0 4px 18px rgba(0,0,0,.06);border-radius:16px;padding:26px}}
.stars{{color:#f59e0b;font-size:.9rem;margin-bottom:12px;letter-spacing:2px}}
.testi p{{font-size:.87rem;color:#374151;font-style:italic;margin-bottom:18px;line-height:1.75}}
.tw{{display:flex;align-items:center;gap:12px}}.tw img{{width:44px;height:44px;border-radius:50%;object-fit:cover}}
.tw strong{{display:block;font-size:.84rem;font-weight:700}}.tw span{{font-size:.73rem;color:#9ca3af}}
.compare-section{{background:#fff}}
.ctable{{width:100%;max-width:840px;margin:0 auto;border-collapse:separate;border-spacing:0;border-radius:16px;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.08)}}
.ctable thead{{background:#1a1a1a}}.ctable th{{padding:16px 22px;text-align:left;font-size:.74rem;color:#fff;text-transform:uppercase;letter-spacing:.08em}}
.ctable td{{padding:14px 22px;font-size:.86rem;border-bottom:1px solid #f0f0f0;background:#fff}}
.ctable tr:last-child td{{border-bottom:none}}.ctable tr:hover td{{background:#fafafa}}
td.f{{font-weight:700}}td.o{{color:#dc2626}}td.n{{color:#16a34a;font-weight:600}}
.cta-section{{position:relative;text-align:center;color:#fff;overflow:hidden;min-height:420px;display:flex;align-items:center;justify-content:center}}
.cta-bg{{position:absolute;inset:0}}.cta-bg img{{width:100%;height:100%;object-fit:cover}}
.cta-ov{{position:absolute;inset:0;background:linear-gradient(135deg,rgba(108,92,231,.92),rgba(0,0,0,.75))}}
.cta-inner{{position:relative;z-index:2;padding:88px 48px;max-width:680px}}
.cta-inner h2{{font-family:'Playfair Display',serif;font-size:clamp(1.9rem,4.5vw,3.2rem);font-weight:700;margin-bottom:14px}}
.cta-inner p{{opacity:.9;margin-bottom:32px;font-size:.98rem}}
.urgency{{margin-top:16px;font-size:.78rem;opacity:.8}}.urgency em{{color:#ffdd57;font-style:normal;font-weight:700}}
.faq-section{{background:#f3f4f6}}
.faq-inner{{max-width:740px;margin:0 auto}}
.faq-title{{font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:700;text-align:center;margin-bottom:32px}}
.faq{{border-bottom:1px solid #e5e7eb}}
.faq button{{width:100%;padding:18px 0;background:none;border:none;color:#1a1a1a;text-align:left;font-size:.92rem;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;font-family:'DM Sans',sans-serif;gap:12px}}
.faq button:hover{{color:{primary}}}
.faq button span{{color:{primary};font-size:1.2rem;transition:transform .2s;flex-shrink:0}}
.faq button.o span{{transform:rotate(45deg)}}
.fa{{display:none;padding:0 0 16px;font-size:.87rem;color:#6b7280;line-height:1.75}}.fa.s{{display:block}}
footer{{background:#111827;color:rgba(255,255,255,.38);text-align:center;padding:24px;font-size:.74rem}}
@media(max-width:768px){{nav{{padding:12px 20px}}section{{padding:68px 20px}}.logos{{padding:16px 20px;gap:20px}}.metrics-row{{gap:28px}}.cta-inner{{padding:60px 20px}}}}
</style></head><body>
<nav><div class="nav-logo">{req.keyword[:26]}</div><button class="nav-cta">{h.get('cta','Get Started')}</button></nav>
<section class="hero" style="padding:0;min-height:100vh"><div class="hero-bg"><img src="{hero_img}" alt="{req.keyword}"/></div><div class="hero-ov"></div>
<div class="hero-c"><div class="hero-tag">{req.keyword}</div><h1>{h.get('headline','Unlock Your Potential')}</h1><p>{h.get('subheadline','Expert guidance that delivers real results.')}</p><button class="btn">{h.get('cta','Get Started Free')}</button><div class="trust">⭐⭐⭐⭐⭐ {h.get('trust_line','Join 10,000+ students')}</div></div></section>
<div class="logos"><div class="lt">Times of India</div><div class="lt">Education World</div><div class="lt">India Today</div><div class="lt">NDTV Education</div><div class="lt">The Hindu</div></div>
<section class="pain-section"><div class="inner"><span class="so">The Problem</span><div class="st">{pp.get('headline','What is holding you back?')}</div><div class="pain-grid">{pain_html}</div></div></section>
<section class="feat-section"><div class="inner"><span class="so">Our Solution</span><div class="st">{ft.get('headline','Everything you need')}</div><img class="feat-img" src="{feat_img}" alt="features"/><div class="feat-grid">{feat_html}</div></div></section>
<section class="proof-section"><div class="inner"><span class="so">Proven Results</span><div class="st">{sp.get('headline','Real students, real results')}</div><img class="proof-img" src="{proof_img}" alt="results"/><div class="metrics-row">{metrics_html}</div><div class="testi-grid">{testis_html}</div></div></section>
<section class="compare-section"><div class="inner" style="text-align:center"><span class="so">Why Choose Us</span><div class="st" style="margin-bottom:36px">{data.get('comparison',{}).get('headline','Why students choose us')}</div><table class="ctable"><thead><tr><th>Feature</th><th>Traditional Way</th><th>With Us ✅</th></tr></thead><tbody>{rows_html}</tbody></table></div></section>
<div class="cta-section"><div class="cta-bg"><img src="{cta_img}" alt="success"/></div><div class="cta-ov"></div><div class="cta-inner"><h2>{cf.get('headline','Start your journey today')}</h2><p>{cf.get('subtext','Join thousands achieving their dreams')}</p><button class="btn" style="font-size:1.02rem;padding:18px 48px">{cf.get('cta','Book Free Demo')}</button><div class="urgency">⚡ <em>{cf.get('urgency','Only 8 spots left!')}</em></div></div></div>
<section class="faq-section"><div class="faq-inner"><div class="faq-title">Frequently Asked Questions</div>{faqs_html}</div></section>
<footer>© 2025 · {req.keyword} · Built with MarketMind AI</footer>
<script>document.querySelectorAll('.faq button').forEach(b=>b.addEventListener('click',function(){{this.classList.toggle('o');this.nextElementSibling.classList.toggle('s')}}));document.querySelectorAll('.btn,.nav-cta').forEach(b=>b.addEventListener('click',()=>document.querySelector('.cta-section').scrollIntoView({{behavior:'smooth'}})));</script>
</body></html>"""

    return {"keyword": req.keyword, "style": "auto", "html": html, "landing_page": html, "generated_at": datetime.now().isoformat()}

# ═══════════════════════════════════════════════════════════════
# 3. BLOG POST
# ═══════════════════════════════════════════════════════════════
@app.post("/api/blog-post")
async def api_blog_post(req: BlogRequest):
    secondary = ", ".join(req.secondary_keywords) if req.secondary_keywords else f"how to {req.keyword}, best {req.keyword}"
    prompt = f"""Expert SEO blog writer. Write full blog post for "{req.keyword}", persona: {req.persona}.

SEO META:
Title Tag (60 chars): 
Meta Description (155 chars): 
URL Slug: 
Primary Keyword: {req.keyword}
Secondary Keywords: {secondary}

FULL BLOG POST (1500+ words):
[H1 Title]
[Introduction 150 words — keyword in first 100 words]
[H2 Section 1 — 200 words]
[H2 Section 2 — 200 words]
[H2 Section 3 — 200 words]
[H2 Section 4 — 200 words]
[H2 FAQ — 5 questions with answers]
[Conclusion 100 words with CTA]

ON-PAGE SEO CHECKLIST: [10 tasks]
HUMAN SCORE: [tone check, readability, keyword density]"""
    result = await call_groq(prompt, 2000)
    return {"keyword": req.keyword, "blog_post": result, "generated_at": datetime.now().isoformat()}

# ═══════════════════════════════════════════════════════════════
# 4. GOOGLE ADS
# ═══════════════════════════════════════════════════════════════
@app.post("/api/google-ads")
async def api_google_ads(req: GoogleAdsRequest):
    try:
        starting_bid = round(float(req.avg_cpc.replace("$","").replace("₹","").strip()) * 1.10, 2)
    except:
        starting_bid = 1.10

    prompt = f"""Google Ads expert. Complete campaign for: Business: {req.business}, Keyword: "{req.keyword}", Budget: {req.budget}, Location: {req.location}, Starting bid: ${starting_bid} (10% above avg CPC).
Return ONLY valid JSON:
{{"campaign_name":"{req.business} - {req.keyword}","objective":"Lead Generation","daily_budget":"calculate from {req.budget}","starting_bid":{starting_bid},"bidding_strategy":"Target CPA",
"ad_formats":[
  {{"format":"Search Ad","objective":"Lead Generation","headline1":"30 char max","headline2":"30 char max","headline3":"30 char max","description1":"90 char description","description2":"90 char description","cta":"Get Free Quote","image_query":"{req.keyword} education student","display_url":"yoursite.com/{req.keyword[:20].replace(' ','-').lower()}"}},
  {{"format":"Display Ad","objective":"Awareness","headline1":"Display headline","headline2":"Supporting text","headline3":"","description1":"Display description 90 chars","description2":"","cta":"Learn More","image_query":"{req.keyword} professional success","display_url":"yoursite.com"}},
  {{"format":"Responsive Display","objective":"Retargeting","headline1":"Come back offer","headline2":"Special deal","headline3":"","description1":"Retargeting copy 90 chars","description2":"","cta":"Book Now","image_query":"{req.keyword} achievement results","display_url":"yoursite.com/offer"}}
],
"ad_groups":[
  {{"name":"Emotional - Pain","angle":"Emotional Pain","keywords_exact":["{req.keyword}","best {req.keyword}","top {req.keyword}","{req.keyword} online","affordable {req.keyword}"],"keywords_phrase":["best {req.keyword} near me","{req.keyword} for beginners","learn {req.keyword} fast"],"negative_keywords":["free","jobs","salary","download","pdf"],"ads":[{{"headline1":"Struggling? We Can Help","headline2":"Expert Help Available Now","headline3":"Start Free Today","desc1":"Tired of falling behind? Our experts help you succeed. Join 10,000+ satisfied clients.","desc2":"98% success rate. Money-back guarantee. Book your free demo now.","cta":"Book Free Demo"}}]}},
  {{"name":"Logical - Features","angle":"Feature Driven","keywords_exact":["{req.keyword} service","{req.keyword} company","hire {req.keyword}","professional {req.keyword}","{req.keyword} agency"],"keywords_phrase":["{req.keyword} services online","best {req.keyword} company","top {req.keyword} agency"],"negative_keywords":["free","cheap","diy"],"ads":[{{"headline1":"#1 Rated {req.keyword[:18]}","headline2":"Certified Experts Ready","headline3":"Try 7 Days Free","desc1":"Expert team, personalized approach, real-time tracking. Proven results guaranteed.","desc2":"From ₹999/month. 50+ experts. 24/7 support. Start today.","cta":"Start Free Trial"}}]}},
  {{"name":"Urgency - Scarcity","angle":"FOMO Scarcity","keywords_exact":["{req.keyword} near me","best {req.keyword} 2024","top {req.keyword} india","{req.keyword} admission","enroll {req.keyword}"],"keywords_phrase":["enroll in {req.keyword}","limited seats {req.keyword}","{req.keyword} open now"],"negative_keywords":["free","cheap"],"ads":[{{"headline1":"Only 8 Seats Left!","headline2":"Batch Closing This Week","headline3":"Enroll Before It Fills","desc1":"Last few spots available. 47 clients enrolled this week already.","desc2":"Don't miss out. Secure your spot before batch is full.","cta":"Claim Your Seat"}}]}}
],
"extensions":{{"sitelinks":[{{"title":"Free Demo","desc1":"Try before you buy","desc2":"No credit card"}},{{"title":"Success Stories","desc1":"See real results","desc2":"98% success"}},{{"title":"Pricing Plans","desc1":"From ₹999/month","desc2":"No hidden fees"}},{{"title":"Our Experts","desc1":"50+ verified experts","desc2":"5+ years exp"}}],"callouts":["No Registration Fee","Free Demo","Money Back Guarantee","24/7 Support"]}},
"bidding_guide":"Start at ${starting_bid}. Week 1-2 manual CPC. Week 3+ switch to Target CPA after 20 conversions.",
"image_query":"{req.keyword} student education"}}"""

    raw = await call_groq(prompt, 2000)
    data = parse_json(raw) or {"raw": raw}

    if isinstance(data, dict) and 'ad_formats' in data:
        for fmt in data['ad_formats']:
            q = fmt.get('image_query', req.keyword + ' education')
            fmt['image_url'] = await get_image(q, 1200, 628, 'landscape')
            fmt['square_url'] = await get_image(q, 400, 400, 'squarish')

    return {"keyword": req.keyword, "business": req.business, "google_ads": data, "generated_at": datetime.now().isoformat()}

# ═══════════════════════════════════════════════════════════════
# 5. META ADS
# ═══════════════════════════════════════════════════════════════
@app.post("/api/meta-ads")
async def api_meta_ads(req: MetaAdsRequest):
    prompt = f"""Meta Ads expert. Complete Facebook/Instagram campaign: Business: {req.business}, Product: {req.product}, Budget: {req.budget}, Age: {req.target_age}, Location: {req.location}.
Return ONLY valid JSON:
{{"campaign_name":"{req.business} Meta Campaign","objective":"Lead Generation",
"ad_formats":[
  {{"format":"Single Image Ad","platform":"Facebook + Instagram Feed","objective":"Awareness","primary_text":"Are you struggling with {req.product}? Join thousands who found the solution. Don't let another month go by without progress.","headline":"Transform Your {req.product[:28]} Results","description":"Expert guidance. Real results.","cta":"Learn More","image_query":"{req.product} student success happy","ratio":"1.91:1","dimensions":"1200x628px"}},
  {{"format":"Carousel Ad","platform":"Facebook + Instagram","objective":"Consideration","primary_text":"Here is what our clients achieve. Swipe to see the journey.","headline":"Real Clients Real Results","description":"Join 10,000+ success stories","cta":"Sign Up","image_query":"{req.product} education achievement","ratio":"1:1","dimensions":"1080x1080px","cards":[{{"title":"Week 1: Foundation","desc":"Build strong base fast","image_query":"{req.product} beginner learning"}},{{"title":"Week 2: Practice","desc":"Hands-on daily exercises","image_query":"{req.product} practice"}},{{"title":"Week 3: Progress","desc":"Measurable improvement","image_query":"{req.product} progress"}},{{"title":"Week 4: Results","desc":"Hit your target goal","image_query":"{req.product} success"}}]}},
  {{"format":"Story Ad","platform":"Instagram + Facebook Stories","objective":"Lead Generation","primary_text":"Swipe up for free demo","headline":"Get Free Demo Today","description":"Limited spots left","cta":"Swipe Up","image_query":"{req.product} mobile vertical","ratio":"9:16","dimensions":"1080x1920px"}},
  {{"format":"Video Ad","platform":"Instagram Reels + Facebook","objective":"Awareness","primary_text":"This client went from struggling to top results in 60 days.","headline":"From Struggling to Top Results","description":"Watch the transformation","cta":"Watch More","image_query":"{req.product} transformation","ratio":"9:16","dimensions":"1080x1920px","video_script":{{"hook":"Show person looking stressed with failing results","problem":"Voiceover: Most people waste months with wrong approach","solution":"Cut to: Same person with expert, understanding clearly","proof":"Show: Results improvement, happy reaction","cta":"Text: Book free demo now. Link in bio."}}}}
],
"ad_sets":[
  {{"name":"Cold Audience Emotional","objective":"Awareness","age":"{req.target_age}","interests":["{req.product}","Online Learning","Professional Development","Industry Skills","Career Growth","Self Improvement","Business Education","Digital Skills","Expert Training","Certification"],"budget_split":"40%","placement":["Facebook Feed","Instagram Feed","Stories"],"primary_text":"Is your team struggling with {req.product}? 10,000+ clients found success with our experts. Book a free demo today.","headline":"Expert {req.product[:25]} Help","cta":"Book Free Demo","image_query":"{req.product} success professional"}},
  {{"name":"Lookalike Logical","objective":"Consideration","lookalike_source":"Past customers","lookalike_percent":"1-3%","budget_split":"35%","placement":["Facebook Feed","Instagram Feed"],"primary_text":"Join 10,000+ who improved results with our AI-powered personalized approach. Expert team, live sessions, guaranteed results.","headline":"Personalized {req.product[:22]} Plan","cta":"Get Started","image_query":"{req.product} technology learning"}},
  {{"name":"Retargeting Urgency","objective":"Conversion","custom_audience":"Website visitors 30 days","budget_split":"25%","placement":["Facebook Feed","Instagram Stories"],"primary_text":"You visited us but haven't started yet. Only 8 spots remaining this month. Don't miss out.","headline":"Only 8 Spots Left!","cta":"Claim Your Spot","image_query":"{req.product} urgency deadline"}}
],
"pixel_events":["PageView","ViewContent","Lead","InitiateCheckout","Purchase"],
"ab_test":{{"week1":"Image vs Carousel format","week2":"Interest vs Lookalike audience","week3":"Emotional vs Logical copy","week4":"Scale winner 20%, pause loser"}},
"image_query":"{req.product} facebook ad education"}}"""

    raw = await call_groq(prompt, 2000)
    data = parse_json(raw) or {"raw": raw}

    if isinstance(data, dict):
        for fmt in data.get('ad_formats', []):
            q = fmt.get('image_query', req.product)
            ori = 'portrait' if fmt.get('ratio','') == '9:16' else 'landscape'
            fmt['image_url'] = await get_image(q, 1200, 628, ori)
            if 'cards' in fmt:
                for card in fmt['cards']:
                    card['image_url'] = await get_image(card.get('image_query', req.product), 400, 400, 'squarish')
        for adset in data.get('ad_sets', []):
            adset['image_url'] = await get_image(adset.get('image_query', req.product), 800, 420, 'landscape')

    return {"business": req.business, "meta_ads": data, "generated_at": datetime.now().isoformat()}

# ═══════════════════════════════════════════════════════════════
# 6. IMAGE PROMPTS
# ═══════════════════════════════════════════════════════════════
@app.post("/api/image-prompts")
async def api_image_prompts(req: ImageRequest):
    prompt = f"""3 realistic environment-based ad image prompts for "{req.keyword}", angle: {req.angle}.

IMAGE 1 (Instagram Feed 1:1):
Scene: [real candid scene, not stock photo]
Subject: [who/what]
Mood: [emotion]
Lighting: [type]
Canva tip: [text overlay guide]

IMAGE 2 (Instagram Story 9:16):
Scene: Subject: Mood: Lighting: Canva tip:

IMAGE 3 (Google Display 16:9):
Scene: Subject: Mood: Lighting: Canva tip:

CANVA DESIGN GUIDE:
Font: | CTA color: | Text position: | Overlay: | Palette:"""
    result = await call_groq(prompt, 800)
    return {"keyword": req.keyword, "angle": req.angle, "image_prompts": result, "generated_at": datetime.now().isoformat()}

# ═══════════════════════════════════════════════════════════════
# 7. BACKLINK RESEARCH
# ═══════════════════════════════════════════════════════════════
@app.post("/api/backlink-research")
async def api_backlink_research(req: BacklinkRequest):
    prompt = f"""SEO link builder. For keyword "{req.keyword}" in {req.niche} niche. Return ONLY valid JSON:
{{"competitors":[{{"url":"https://example.com","domain":"example.com","title":"Page title","da":45,"pa":38,"spam_score":2,"backlinks":1240,"traffic":"12K/mo","type":"Blog"}},{{"url":"https://site2.com","domain":"site2.com","title":"Title","da":38,"pa":32,"spam_score":1,"backlinks":890,"traffic":"8K/mo","type":"Directory"}},{{"url":"https://site3.com","domain":"site3.com","title":"Title","da":52,"pa":44,"spam_score":2,"backlinks":2100,"traffic":"20K/mo","type":"News"}},{{"url":"https://site4.com","domain":"site4.com","title":"Title","da":35,"pa":29,"spam_score":3,"backlinks":540,"traffic":"5K/mo","type":"Forum"}},{{"url":"https://site5.com","domain":"site5.com","title":"Title","da":48,"pa":41,"spam_score":1,"backlinks":1560,"traffic":"15K/mo","type":"Blog"}}],
"link_targets":[{{"url":"https://target1.com","domain":"target1.com","da":52,"pa":44,"spam_score":1,"type":"Guest Post","contact_page":"https://target1.com/contact","author_name":"John Smith","author_email":"john@target1.com","pitch_angle":"Relevant content angle"}},{{"url":"https://target2.com","domain":"target2.com","da":45,"pa":38,"spam_score":2,"type":"Resource Page","author_name":"Jane Doe","author_email":"jane@target2.com","pitch_angle":"Resource page pitch"}},{{"url":"https://target3.com","domain":"target3.com","da":38,"pa":32,"spam_score":1,"type":"Blog","author_name":"Mike Johnson","author_email":"mike@target3.com","pitch_angle":"Blog collab"}},{{"url":"https://target4.com","domain":"target4.com","da":60,"pa":52,"spam_score":1,"type":"News","author_name":"Sarah Lee","author_email":"sarah@target4.com","pitch_angle":"News mention"}},{{"url":"https://target5.com","domain":"target5.com","da":42,"pa":36,"spam_score":2,"type":"Directory","author_name":"Tom Brown","author_email":"tom@target5.com","pitch_angle":"Directory listing"}},{{"url":"https://target6.com","domain":"target6.com","da":35,"pa":29,"spam_score":3,"type":"Forum","author_name":"Emma Wilson","author_email":"emma@target6.com","pitch_angle":"Forum contribution"}},{{"url":"https://target7.com","domain":"target7.com","da":55,"pa":47,"spam_score":1,"type":"Guest Post","author_name":"David Clark","author_email":"david@target7.com","pitch_angle":"Expert article"}},{{"url":"https://target8.com","domain":"target8.com","da":28,"pa":24,"spam_score":2,"type":"Blog","author_name":"Lisa Davis","author_email":"lisa@target8.com","pitch_angle":"Collab piece"}}],
"quick_wins":[{{"url":"https://dir1.com","domain":"dir1.com","da":40,"type":"Free Directory","effort":"Low","how_to":"Submit at domain/submit"}},{{"url":"https://dir2.com","domain":"dir2.com","da":35,"type":"Free Directory","effort":"Low","how_to":"Create free listing"}},{{"url":"https://dir3.com","domain":"dir3.com","da":45,"type":"Profile Link","effort":"Low","how_to":"Create profile page"}},{{"url":"https://dir4.com","domain":"dir4.com","da":38,"type":"Forum Profile","effort":"Low","how_to":"Register and add site to profile"}},{{"url":"https://dir5.com","domain":"dir5.com","da":30,"type":"Q&A Site","effort":"Low","how_to":"Answer questions with link"}}],
"search_operators":["intitle:\\"write for us\\" {req.keyword}","intitle:\\"guest post\\" {req.keyword}","intitle:\\"submit article\\" {req.keyword}","\\"resources\\" + \\"useful links\\" {req.keyword}","intitle:\\"sponsored post\\" {req.keyword}"],
"outreach_emails":[{{"domain":"target1.com","author":"John Smith","email":"john@target1.com","templates":[{{"angle":"Guest Post Pitch","subject":"Guest Post Proposal for target1.com","body":"Hi John,\\n\\nI came across target1.com and love the content on {req.keyword}.\\n\\nI am a specialist in this space and would love to contribute a high-quality guest post your audience would find genuinely valuable.\\n\\nWould you be open to it?\\n\\nBest,\\n{req.sender_name}"}},{{"angle":"Resource Page","subject":"Resource Addition for target1.com","body":"Hi John,\\n\\nYour resource page on {req.keyword} is great. I have a resource at {req.sender_site} that your readers would love.\\n\\nWould you consider adding it?\\n\\nThanks,\\n{req.sender_name}"}},{{"angle":"Collaboration","subject":"Collaboration Opportunity","body":"Hi John,\\n\\nWe both cover {req.keyword}. I think there is a great collaboration opportunity between us.\\n\\nInterested?\\n\\n{req.sender_name}"}}]}},{{"domain":"target2.com","author":"Jane Doe","email":"jane@target2.com","templates":[{{"angle":"Guest Post","subject":"Guest Article Proposal","body":"Hi Jane,\\n\\nLove the content on target2.com. I would love to contribute a guest article on {req.keyword}.\\n\\nReady when you are!\\n\\n{req.sender_name}"}},{{"angle":"Link Exchange","subject":"Link Exchange Proposal","body":"Hi Jane,\\n\\nI run {req.sender_site} covering {req.keyword}. Want to explore a link exchange?\\n\\n{req.sender_name}"}},{{"angle":"Resource","subject":"Useful Resource for Your Readers","body":"Hi Jane,\\n\\nI have a resource on {req.keyword} that would be perfect for your audience at target2.com.\\n\\n{req.sender_name}"}}]}},{{"domain":"target3.com","author":"Mike Johnson","email":"mike@target3.com","templates":[{{"angle":"Guest Post","subject":"Expert Content Proposal","body":"Hi Mike,\\n\\nBig fan of target3.com. Would love to write a guest post on {req.keyword} for your readers.\\n\\n{req.sender_name}"}},{{"angle":"Broken Link","subject":"Broken Link on target3.com","body":"Hi Mike,\\n\\nFound a broken link on your {req.keyword} page. I have updated content at {req.sender_site} that could replace it.\\n\\n{req.sender_name}"}},{{"angle":"Collab","subject":"Content Collaboration","body":"Hi Mike,\\n\\nLet us collaborate on a {req.keyword} piece. I think it would do well for both our audiences.\\n\\n{req.sender_name}"}}]}}]}}"""

    raw = await call_groq(prompt, 2000)
    data = parse_json(raw) or {"competitors":[],"link_targets":[],"quick_wins":[],"search_operators":[],"outreach_emails":[]}
    return {**data, "keyword": req.keyword, "generated_at": datetime.now().isoformat()}

# ═══════════════════════════════════════════════════════════════
# 8. FIND CONTACTS
# ═══════════════════════════════════════════════════════════════
@app.post("/api/find-contacts")
async def api_find_contacts(req: ContactRequest):
    prompt = f"""Find contact info for "{req.domain}" in {req.niche} niche. Return ONLY valid JSON:
{{"domain":"{req.domain}","owner_name":"Realistic person name","owner_email":"name@{req.domain}","editor_name":"Editor name","editor_email":"editor@{req.domain}","contact_page":"https://{req.domain}/contact","linkedin":"https://linkedin.com/in/name","twitter":"@handle","best_email":"owner@{req.domain}","confidence":"Medium"}}"""
    raw = await call_groq(prompt, 400)
    data = parse_json(raw) or {"domain": req.domain, "confidence": "Low"}
    return {**data, "generated_at": datetime.now().isoformat()}

# ═══════════════════════════════════════════════════════════════
# 9. LEAD GENERATION
# ═══════════════════════════════════════════════════════════════
@app.post("/api/lead-research")
async def api_lead_research(req: LeadRequest):
    comp_prompt = f"""B2B competitive intelligence for "{req.service}" in {req.location}. Return ONLY valid JSON:
{{"competitors":[{{"company":"Company 1","website":"https://co1.com","da":45,"pa":38,"founded":"2015","employees":"50-200","location":"Bangalore","services":["{req.service}","Consulting","Support"],"pricing_model":"Project-based","pricing_range":"$20-50/hr","key_clients":["Client A","Client B","Client C"],"case_studies":["Helped company reduce bugs by 60%","Delivered project 2 weeks early"],"tech_stack":["Selenium","Python","JIRA"],"contact_person":"CEO Name","guessed_email":"ceo@co1.com","linkedin":"https://linkedin.com/company/co1","strengths":["Strong portfolio","Good client retention"],"weaknesses":["Limited AI automation","Higher pricing"],"opportunity":"Compete on AI-powered approach and faster delivery"}},{{"company":"Company 2","website":"https://co2.com","da":38,"pa":32,"founded":"2018","employees":"20-50","location":"Hyderabad","services":["{req.service}","QA","Development"],"pricing_model":"Retainer","pricing_range":"$15-35/hr","key_clients":["Client D","Client E"],"case_studies":["95% defect detection rate","Reduced testing time by 40%"],"tech_stack":["Appium","Java","TestNG"],"contact_person":"Founder Name","guessed_email":"founder@co2.com","linkedin":"https://linkedin.com/company/co2","strengths":["Affordable rates","Quick turnaround"],"weaknesses":["Small team","Limited expertise"],"opportunity":"Win on expertise and technology"}},{{"company":"Company 3","website":"https://co3.com","da":52,"pa":44,"founded":"2012","employees":"200-500","location":"Mumbai","services":["{req.service}","DevOps","Cloud"],"pricing_model":"Enterprise","pricing_range":"$50-100/hr","key_clients":["Fortune 500","MNC","Startup"],"case_studies":["Zero defect deployment","100% test coverage achieved"],"tech_stack":["Cypress","TypeScript","AWS"],"contact_person":"VP Sales","guessed_email":"sales@co3.com","linkedin":"https://linkedin.com/company/co3","strengths":["Enterprise clients","Strong brand"],"weaknesses":["Too expensive for SMEs","Slow response"],"opportunity":"Target their unhappy SME clients with better pricing"}}],
"market_insights":{{"market_size":"₹5000 Cr","growth_rate":"22% YoY","avg_project_value":"₹10-50 Lakhs","top_buying_triggers":["Digital transformation push","Failed in-house attempts","Regulatory compliance needs"],"common_pain_points":["Lack of in-house expertise","Budget constraints","Tight deadlines"]}},
"your_positioning":"Position as AI-powered {req.service} agency offering 50% faster delivery at competitive pricing with guaranteed quality"}}"""

    lead_prompt = f"""Find 8 potential clients needing "{req.service}" in {req.location}. Return ONLY valid JSON:
{{"leads":[{{"company":"E-commerce Co","website":"https://eco.com","industry":"E-commerce","size":"SME","employees":"50-200","location":"Mumbai","why_they_need":"Rapid product launches need thorough testing","pain_point":"Manual testing slowing releases","decision_maker":"CTO","contact_name":"Rahul Sharma","email":"rahul@eco.com","linkedin":"https://linkedin.com/in/rahul","phone":"+91-9876543210","budget_estimate":"₹5-15 Lakhs","buying_stage":"Consideration","best_channel":"LinkedIn","pitch_angle":"Automated testing will cut their release cycle by 60%","urgency":"High"}},{{"company":"Fintech Startup","website":"https://finco.com","industry":"Fintech","size":"Startup","employees":"20-50","location":"Bangalore","why_they_need":"RBI compliance requires thorough security testing","pain_point":"No dedicated QA team","decision_maker":"CEO","contact_name":"Priya Menon","email":"priya@finco.com","linkedin":"https://linkedin.com/in/priya","phone":"+91-9765432109","budget_estimate":"₹3-8 Lakhs","buying_stage":"Decision","best_channel":"Email","pitch_angle":"Compliance testing expertise will save them from RBI penalties","urgency":"High"}},{{"company":"Healthcare App","website":"https://health.com","industry":"Healthcare","size":"SME","employees":"100-300","location":"Delhi","why_they_need":"HIPAA compliance and patient data security","pain_point":"Recent security incident shook confidence","decision_maker":"VP Engineering","contact_name":"Amit Kumar","email":"amit@health.com","linkedin":"https://linkedin.com/in/amit","phone":"+91-9654321098","budget_estimate":"₹8-20 Lakhs","buying_stage":"Awareness","best_channel":"Call","pitch_angle":"Post-incident security testing with compliance guarantee","urgency":"Medium"}}],
"outreach_strategy":"Focus on pain-specific cold emails. Lead with the cost of NOT fixing the problem. Target CTOs and VPs of Engineering."}}"""

    partner_prompt = f"""Find 5 potential agency partners for "{req.service}" in {req.location}. Return ONLY valid JSON:
{{"leads":[{{"company":"Web Dev Agency","website":"https://wda.com","industry":"IT Services","size":"SME","employees":"50-100","location":"Bangalore","why_they_need":"Need QA partner for their dev projects","pain_point":"Clients demanding quality guarantee","decision_maker":"Director","contact_name":"Suresh Patel","email":"suresh@wda.com","linkedin":"https://linkedin.com/in/suresh","phone":"+91-9543210987","budget_estimate":"Revenue share","buying_stage":"Consideration","best_channel":"LinkedIn","pitch_angle":"White-label QA partnership — they win bigger deals, we do the testing","urgency":"Medium"}},{{"company":"Digital Marketing Agency","website":"https://dma.com","industry":"Marketing","size":"SME","employees":"30-80","location":"Mumbai","why_they_need":"Clients need web app testing","pain_point":"Losing deals to full-service agencies","decision_maker":"CEO","contact_name":"Neha Gupta","email":"neha@dma.com","linkedin":"https://linkedin.com/in/neha","phone":"+91-9432109876","budget_estimate":"Project basis","buying_stage":"Awareness","best_channel":"Email","pitch_angle":"Add QA to their service portfolio without hiring","urgency":"Low"}}]}}"""

    comps, leads, partners = await asyncio.gather(
        (lambda: call_groq(comp_prompt, 2000))(),
        (lambda: call_groq(lead_prompt, 2000))(),
        (lambda: call_groq(partner_prompt, 1000))()
    )

    return {
        "service": req.service,
        "location": req.location,
        "company": req.company_name,
        "competitors": parse_json(comps) or {"competitors": [], "market_insights": {}},
        "leads": parse_json(leads) or {"leads": []},
        "partners": parse_json(partners) or {"leads": []},
        "generated_at": datetime.now().isoformat()
    }

@app.post("/api/competitors")
async def api_competitors(req: LeadRequest):
    result = await api_lead_research(req)
    return {"competitors": result.get("competitors", {}), "generated_at": datetime.now().isoformat()}

@app.post("/api/find-leads")
async def api_find_leads(req: LeadRequest):
    result = await api_lead_research(req)
    return {"leads": result.get("leads", {}), "generated_at": datetime.now().isoformat()}

@app.post("/api/generate-outreach")
async def api_generate_outreach(req: OutreachRequest):
    prompt = f"""Personalized B2B outreach for: Company: {req.company}, Contact: {req.contact}, Role: {req.role}, Pain: {req.pain_point}, Service: {req.service}, Sender: {req.sender_company}.
Return ONLY valid JSON:
{{"email":{{"subject":"Compelling subject under 50 chars","body":"Hi {req.contact},\\n\\nI noticed {req.company} might be facing {req.pain_point}.\\n\\nAt {req.sender_company}, we specialize in {req.service} and have helped similar companies solve exactly this.\\n\\nWould you be open to a 15-minute call this week?\\n\\nBest,\\n{req.sender_company} Team"}},
"linkedin":{{"connection_note":"Hi {req.contact}, I work with {req.role}s in your space on {req.service}. Would love to connect and share insights. No sales pitch!","follow_up":"Thanks for connecting {req.contact}! Noticed {req.company} is growing fast. We help companies like yours with {req.service}. Worth a quick chat?"}},
"whatsapp":{{"message":"Hi {req.contact}! This is from {req.sender_company}. We specialize in {req.service} and saw that {req.company} might benefit from our work. Can I share a quick case study?"}},
"call_script":{{"opener":"Hi, is this {req.contact}? Great, I am calling from {req.sender_company}. I will take just 30 seconds of your time — is now okay?","pitch":"We help companies like {req.company} solve {req.pain_point} through our {req.service} solutions. We recently helped a similar company achieve [result]. I think we could do the same for you.","objection_handler":"I completely understand. Most of our best clients said the same thing initially. Can I just send you one case study? Takes 2 minutes to read and you can decide from there.","close":"Would Tuesday or Wednesday work for a 15-minute call? I can show you exactly how we would approach {req.company}'s situation."}}}}"""

    raw = await call_groq(prompt, 1000)
    data = parse_json(raw) or {}
    return {**data, "generated_at": datetime.now().isoformat()}

# ═══════════════════════════════════════════════════════════════
# 10. LIVE LANDING PAGE URL
# ═══════════════════════════════════════════════════════════════
@app.get("/lp/{keyword}")
async def live_landing_page(keyword: str, persona: str = "student"):
    kw = keyword.replace("-", " ")
    req = LandingPageRequest(keyword=kw, style="auto", persona=persona)
    result = await api_landing_page(req)
    return HTMLResponse(content=result.get("html", "<h1>Error</h1>"))
