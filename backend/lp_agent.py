from seo_agent import call_groq
from image_service import get_unsplash_image, get_multiple_images
import json, re, asyncio

async def generate_lp_content(keyword: str, style: str, persona: str = "student") -> dict:
    prompt = f"""Generate landing page content for keyword "{keyword}", persona "{persona}".
Return ONLY valid JSON no markdown:
{{
  "style_recommendation": "minimalist",
  "primary_color": "#6C5CE7",
  "accent_color": "#22C55E",
  "hero": {{
    "headline": "Powerful 7-word headline addressing pain",
    "subheadline": "Clear solution subheadline under 20 words",
    "cta": "Get Started Free",
    "trust_line": "Join 10,000+ students who transformed their grades",
    "image_query": "student studying focused laptop books"
  }},
  "pain_points": {{
    "headline": "Are these struggles holding you back?",
    "cards": [
      {{"icon":"😓","title":"Falling Behind","desc":"Struggling to keep up with syllabus and deadlines","image_query":"stressed student desk books night"}},
      {{"icon":"😰","title":"No Expert Help","desc":"No quality guidance when you need it most","image_query":"confused student asking question teacher"}},
      {{"icon":"😤","title":"Wasting Money","desc":"Expensive coaching with no guaranteed results","image_query":"frustrated person money wasted"}},
      {{"icon":"😩","title":"Exam Anxiety","desc":"Fear and stress before every important exam","image_query":"anxious nervous student exam hall"}}
    ]
  }},
  "features": {{
    "headline": "Everything you need to succeed in one place",
    "image_query": "students learning online technology classroom",
    "items": [
      {{"icon":"✅","title":"Expert Tutors","desc":"Learn from India top educators with proven results"}},
      {{"icon":"🚀","title":"Learn Anytime","desc":"24/7 access to all recorded sessions and materials"}},
      {{"icon":"💡","title":"Live Doubt Clearing","desc":"Get instant answers during live interactive sessions"}},
      {{"icon":"🎯","title":"Personalized Plan","desc":"Custom study schedule built around your weak areas"}},
      {{"icon":"📊","title":"Progress Dashboard","desc":"Track improvements with real-time performance analytics"}},
      {{"icon":"🏆","title":"Grade Guarantee","desc":"Guaranteed improvement or complete money back"}}
    ]
  }},
  "social_proof": {{
    "headline": "Thousands of students achieving real results",
    "image_query": "happy students celebrating success graduation",
    "metrics": [
      {{"number":"15,000+","label":"Students Helped"}},
      {{"number":"98%","label":"Success Rate"}},
      {{"number":"4.9★","label":"Student Rating"}},
      {{"number":"50+","label":"Expert Tutors"}}
    ],
    "testimonials": [
      {{"name":"Priya Sharma","role":"IB Student, Mumbai","quote":"My grades went from C to A in just 6 weeks. The personalized attention made all the difference.","avatar_query":"indian girl student smiling happy"}},
      {{"name":"Arjun Kumar","role":"JEE Aspirant, Delhi","quote":"Finally cleared my doubts instantly. Cracked JEE Advanced with their guidance and support.","avatar_query":"indian boy student confident smiling"}},
      {{"name":"Meera Reddy","role":"Parent, Bangalore","quote":"Saw dramatic improvement in my child within the first month. Best investment we ever made.","avatar_query":"happy indian mother parent"}}
    ]
  }},
  "comparison": {{
    "headline": "Why smart students choose us over others",
    "rows": [
      {{"feature":"Learning Pace","old":"Fixed rigid batch schedule","new":"Learn at your own pace 24/7"}},
      {{"feature":"Expert Access","old":"1 teacher for 60+ students","new":"Dedicated 1-on-1 mentoring"}},
      {{"feature":"Monthly Cost","old":"₹8000-15000 coaching fee","new":"Affordable from ₹999/month"}},
      {{"feature":"Progress Tracking","old":"Wait months for exam results","new":"Real-time daily progress dashboard"}},
      {{"feature":"Doubt Support","old":"Wait till next week class","new":"Instant 24/7 doubt resolution"}},
      {{"feature":"Study Material","old":"Outdated photocopied notes","new":"Updated digital resources always"}},
      {{"feature":"Result Guarantee","old":"No promise of improvement","new":"Grade improvement guaranteed"}},
      {{"feature":"Schedule","old":"Miss class if busy","new":"Watch recordings anytime"}}
    ]
  }},
  "cta_faq": {{
    "headline": "Your success story starts today",
    "subtext": "Join thousands of students already achieving their dreams with expert guidance",
    "cta": "Book Your Free Demo Class",
    "urgency": "Only 8 spots remaining this month",
    "bg_image_query": "students graduation celebration success achievement",
    "faqs": [
      {{"q":"How quickly will I see improvement in my grades?","a":"Most students see noticeable improvement within 2-3 weeks of consistent sessions with our expert tutors."}},
      {{"q":"What if I am not satisfied with the results?","a":"We offer a complete 7-day money-back guarantee. No questions asked if you are not 100% satisfied."}},
      {{"q":"Can I access classes at my own time?","a":"Yes, all live sessions are recorded and available 24/7. Study whenever it suits your schedule best."}},
      {{"q":"How are your tutors selected and verified?","a":"Every tutor undergoes a 3-stage selection process and must have minimum 5 years of proven teaching experience."}},
      {{"q":"Is there a free trial available?","a":"Absolutely! We offer a completely free demo class with zero commitment and no credit card required."}}
    ]
  }}
}}"""
    raw = await call_groq(prompt, 2000)
    try:
        clean = re.sub(r'```json|```','',raw).strip()
        return json.loads(clean)
    except:
        return None


async def build_html_with_images(keyword: str, data: dict) -> str:
    """Build full HTML — fetch all images from Unsplash via backend"""
    if not data:
        return "<h1>Error generating content</h1>"

    h = data.get('hero', {})
    pp = data.get('pain_points', {})
    ft = data.get('features', {})
    sp = data.get('social_proof', {})
    cp = data.get('comparison', {})
    cf = data.get('cta_faq', {})
    primary = data.get('primary_color', '#6C5CE7')
    accent = data.get('accent_color', '#22C55E')

    # ── Fetch ALL images concurrently from Unsplash ──
    pain_cards = pp.get('cards', [])
    testi_list = sp.get('testimonials', [])

    image_queries = [
        (h.get('image_query', f'{keyword} student'), 1400, 800, 'landscape'),
        (ft.get('image_query', f'{keyword} success'), 1200, 400, 'landscape'),
        (sp.get('image_query', 'students success celebration'), 1200, 300, 'landscape'),
        (cf.get('bg_image_query', 'graduation success achievement'), 1400, 500, 'landscape'),
    ] + [
        (c.get('image_query', 'student studying'), 480, 260, 'landscape') for c in pain_cards
    ] + [
        (t.get('avatar_query', 'person portrait'), 80, 80, 'squarish') for t in testi_list
    ]

    # Fetch all concurrently
    async def fetch_img(q, w, h_size, ori):
        return await get_unsplash_image(q, w, h_size, ori)

    tasks = [fetch_img(q, w, h_size, ori) for q, w, h_size, ori in image_queries]
    all_imgs = await asyncio.gather(*tasks)

    hero_img = all_imgs[0]
    feat_img = all_imgs[1]
    proof_img = all_imgs[2]
    cta_img = all_imgs[3]
    pain_imgs = all_imgs[4:4+len(pain_cards)]
    avatar_imgs = all_imgs[4+len(pain_cards):]

    # ── Build HTML sections ──
    pain_html = ""
    for i, c in enumerate(pain_cards):
        img_src = pain_imgs[i] if i < len(pain_imgs) else f"https://picsum.photos/seed/{i+10}/480/260"
        pain_html += f"""
        <div class="pain-card">
          <div class="pain-img-wrap"><img src="{img_src}" alt="{c['title']}" loading="lazy"/></div>
          <div class="pc-body">
            <span class="pc-icon">{c['icon']}</span>
            <h3>{c['title']}</h3>
            <p>{c['desc']}</p>
          </div>
        </div>"""

    feat_html = "".join([f'<div class="feat-item"><div class="fi-icon">{f["icon"]}</div><div><h3>{f["title"]}</h3><p>{f["desc"]}</p></div></div>' for f in ft.get('items',[])])

    metrics_html = "".join([f'<div class="metric"><div class="m-n">{m["number"]}</div><div class="m-l">{m["label"]}</div></div>' for m in sp.get('metrics',[])])

    testis_html = ""
    for i, t in enumerate(testi_list):
        av = avatar_imgs[i] if i < len(avatar_imgs) else f"https://picsum.photos/seed/{i+50}/80/80"
        testis_html += f"""
        <div class="testi">
          <div class="stars">★★★★★</div>
          <p>"{t['quote']}"</p>
          <div class="testi-who">
            <img src="{av}" alt="{t['name']}" style="width:44px;height:44px;border-radius:50%;object-fit:cover"/>
            <div><strong>{t['name']}</strong><span>{t['role']}</span></div>
          </div>
        </div>"""

    rows_html = "".join([f"<tr><td class='f'>{r['feature']}</td><td class='o'>✗ {r['old']}</td><td class='n'>✓ {r['new']}</td></tr>" for r in cp.get('rows',[])])

    faqs_html = "".join([f'<div class="faq"><button onclick="this.classList.toggle(\'open\');this.nextElementSibling.classList.toggle(\'show\')">{f["q"]}<span>+</span></button><div class="faq-a"><p>{f["a"]}</p></div></div>' for f in cf.get('faqs',[])])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{h.get('headline','Welcome')} | {keyword}</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--p:{primary};--a:{accent}}}
body{{font-family:'DM Sans',sans-serif;background:#fafaf8;color:#1a1a1a;line-height:1.7;overflow-x:hidden}}
img{{max-width:100%;display:block}}
nav{{position:fixed;top:0;left:0;right:0;z-index:100;padding:14px 48px;display:flex;align-items:center;justify-content:space-between;background:rgba(250,250,248,.95);backdrop-filter:blur(12px);border-bottom:1px solid #e5e7eb}}
.nav-logo{{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:#1a1a1a}}
.nav-cta{{background:var(--p);color:#fff;padding:10px 24px;border:none;border-radius:8px;font-weight:700;font-size:.88rem;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .2s}}
.nav-cta:hover{{opacity:.9;transform:translateY(-1px);box-shadow:0 4px 14px rgba(108,92,231,.4)}}

/* HERO */
.hero{{min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;position:relative;overflow:hidden}}
.hero-bg{{position:absolute;inset:0}}
.hero-bg img{{width:100%;height:100%;object-fit:cover;object-position:center}}
.hero-overlay{{position:absolute;inset:0;background:linear-gradient(135deg,rgba(0,0,0,.72) 0%,rgba(0,0,0,.45) 100%)}}
.hero-content{{position:relative;z-index:2;max-width:780px;padding:120px 32px 80px;color:#fff}}
.hero-tag{{display:inline-block;background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);padding:7px 20px;border-radius:20px;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;margin-bottom:24px;backdrop-filter:blur(8px)}}
.hero h1{{font-family:'Playfair Display',serif;font-size:clamp(2.2rem,5.5vw,4rem);font-weight:800;line-height:1.08;margin-bottom:20px;letter-spacing:-.02em}}
.hero p{{font-size:1.08rem;opacity:.9;margin-bottom:36px;max-width:560px;margin-left:auto;margin-right:auto;line-height:1.65}}
.btn-main{{background:var(--p);color:#fff;padding:17px 40px;border:none;border-radius:10px;font-weight:700;font-size:1rem;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .25s;letter-spacing:.01em}}
.btn-main:hover{{opacity:.92;transform:translateY(-2px);box-shadow:0 10px 28px rgba(0,0,0,.35)}}
.trust{{margin-top:20px;font-size:.8rem;opacity:.8;display:flex;align-items:center;justify-content:center;gap:8px}}
.trust-ava{{display:flex}}.trust-ava img{{width:28px;height:28px;border-radius:50%;border:2px solid rgba(255,255,255,.4);margin-right:-8px;object-fit:cover}}

/* LOGOS */
.logos-bar{{padding:22px 48px;background:#fff;border-bottom:1px solid #e5e7eb;display:flex;align-items:center;justify-content:center;gap:44px;flex-wrap:wrap}}
.logo-txt{{font-size:.75rem;font-weight:700;color:#c8c8c8;letter-spacing:.06em;text-transform:uppercase}}

/* SECTIONS */
section{{padding:92px 48px}}
.inner{{max-width:1120px;margin:0 auto}}
.sec-over{{font-size:.63rem;text-transform:uppercase;letter-spacing:.18em;color:var(--p);font-weight:700;margin-bottom:10px;display:block}}
.sec-title{{font-family:'Playfair Display',serif;font-size:clamp(1.7rem,3.2vw,2.7rem);font-weight:700;margin-bottom:38px;line-height:1.15;color:#1a1a1a}}

/* PAIN CARDS */
.pain-section{{background:#f3f4f6}}
.pain-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px}}
.pain-card{{background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.06);transition:all .28s}}
.pain-card:hover{{transform:translateY(-5px);box-shadow:0 14px 32px rgba(0,0,0,.1)}}
.pain-img-wrap{{height:190px;overflow:hidden}}
.pain-img-wrap img{{width:100%;height:190px;object-fit:cover;transition:transform .4s}}
.pain-card:hover .pain-img-wrap img{{transform:scale(1.06)}}
.pc-body{{padding:20px}}
.pc-icon{{font-size:1.7rem;display:block;margin-bottom:9px}}
.pc-body h3{{font-size:.98rem;font-weight:700;margin-bottom:6px;color:#1a1a1a}}
.pc-body p{{font-size:.83rem;color:#6b7280;line-height:1.6}}

/* FEATURES */
.feat-section{{background:#fff}}
.feat-top-img{{width:100%;height:320px;object-fit:cover;border-radius:18px;margin-bottom:48px;box-shadow:0 16px 48px rgba(0,0,0,.1)}}
.feat-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:18px}}
.feat-item{{background:#f8f9fa;border:1px solid #e5e7eb;border-radius:14px;padding:24px;display:flex;gap:16px;align-items:flex-start;transition:all .22s}}
.feat-item:hover{{border-color:var(--p);background:#fff;box-shadow:0 6px 20px rgba(108,92,231,.08)}}
.fi-icon{{font-size:1.7rem;flex-shrink:0;margin-top:1px}}
.feat-item h3{{font-size:.93rem;font-weight:700;margin-bottom:5px;color:#1a1a1a}}
.feat-item p{{font-size:.81rem;color:#6b7280;line-height:1.6}}

/* PROOF */
.proof-section{{background:#f3f4f6}}
.proof-top-img{{width:100%;height:240px;object-fit:cover;border-radius:16px;margin-bottom:48px;box-shadow:0 12px 36px rgba(0,0,0,.08)}}
.metrics-row{{display:flex;justify-content:center;gap:52px;flex-wrap:wrap;margin-bottom:52px;padding:30px 0;border-top:1px solid #e5e7eb;border-bottom:1px solid #e5e7eb}}
.metric{{text-align:center}}
.m-n{{font-family:'Playfair Display',serif;font-size:2.4rem;font-weight:700;color:var(--p);line-height:1}}
.m-l{{font-size:.7rem;color:#9ca3af;text-transform:uppercase;letter-spacing:.1em;margin-top:6px}}
.testi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:20px}}
.testi{{background:#fff;box-shadow:0 4px 18px rgba(0,0,0,.06);border-radius:16px;padding:26px}}
.stars{{color:#f59e0b;font-size:.9rem;margin-bottom:12px;letter-spacing:2px}}
.testi p{{font-size:.87rem;color:#374151;font-style:italic;margin-bottom:18px;line-height:1.75}}
.testi-who{{display:flex;align-items:center;gap:12px}}
.testi-who strong{{display:block;font-size:.84rem;font-weight:700;color:#1a1a1a}}
.testi-who span{{font-size:.73rem;color:#9ca3af}}

/* COMPARE */
.compare-section{{background:#fff}}
.ctable{{width:100%;max-width:840px;margin:0 auto;border-collapse:separate;border-spacing:0;border-radius:16px;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.08)}}
.ctable thead{{background:#1a1a1a}}
.ctable th{{padding:16px 22px;text-align:left;font-size:.74rem;color:#fff;text-transform:uppercase;letter-spacing:.08em;font-weight:600}}
.ctable td{{padding:14px 22px;font-size:.86rem;border-bottom:1px solid #f0f0f0;background:#fff}}
.ctable tr:last-child td{{border-bottom:none}}
.ctable tr:hover td{{background:#fafafa}}
td.f{{font-weight:700;color:#1a1a1a}}
td.o{{color:#dc2626}}
td.n{{color:#16a34a;font-weight:600}}

/* CTA */
.cta-section{{position:relative;text-align:center;color:#fff;overflow:hidden;min-height:420px;display:flex;align-items:center;justify-content:center}}
.cta-bg{{position:absolute;inset:0}}
.cta-bg img{{width:100%;height:100%;object-fit:cover;object-position:center}}
.cta-overlay{{position:absolute;inset:0;background:linear-gradient(135deg,rgba(108,92,231,.92),rgba(0,0,0,.75))}}
.cta-inner{{position:relative;z-index:2;padding:88px 48px;max-width:680px}}
.cta-inner h2{{font-family:'Playfair Display',serif;font-size:clamp(1.9rem,4.5vw,3.2rem);font-weight:700;margin-bottom:14px;line-height:1.15}}
.cta-inner p{{opacity:.9;margin-bottom:32px;font-size:.98rem;line-height:1.65}}
.urgency{{margin-top:16px;font-size:.78rem;opacity:.8}}
.urgency em{{color:#ffdd57;font-style:normal;font-weight:700}}

/* FAQ */
.faq-section{{background:#f3f4f6}}
.faq-inner{{max-width:740px;margin:0 auto}}
.faq-title{{font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:700;text-align:center;margin-bottom:32px;color:#1a1a1a}}
.faq{{border-bottom:1px solid #e5e7eb}}
.faq button{{width:100%;padding:18px 0;background:none;border:none;color:#1a1a1a;text-align:left;font-size:.92rem;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;font-family:'DM Sans',sans-serif;gap:12px;transition:color .2s}}
.faq button:hover{{color:var(--p)}}
.faq button span{{color:var(--p);font-size:1.2rem;transition:transform .2s;flex-shrink:0;font-weight:400}}
.faq button.open span{{transform:rotate(45deg)}}
.faq-a{{display:none;padding:0 0 16px;font-size:.87rem;color:#6b7280;line-height:1.75}}
.faq-a.show{{display:block}}

footer{{background:#111827;color:rgba(255,255,255,.38);text-align:center;padding:24px;font-size:.74rem}}
@media(max-width:768px){{nav{{padding:12px 20px}}section{{padding:68px 20px}}.logos-bar{{padding:16px 20px;gap:20px}}.metrics-row{{gap:28px}}.cta-inner{{padding:60px 20px}}}}
</style>
</head>
<body>
<nav>
  <div class="nav-logo">{keyword[:26]}</div>
  <button class="nav-cta" onclick="document.querySelector('.cta-section').scrollIntoView({{behavior:'smooth'}})">{h.get('cta','Get Started')}</button>
</nav>

<!-- HERO -->
<section class="hero" style="padding:0;min-height:100vh">
  <div class="hero-bg"><img src="{hero_img}" alt="{keyword}" loading="eager"/></div>
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <div class="hero-tag">{keyword}</div>
    <h1>{h.get('headline','Unlock Your Full Potential')}</h1>
    <p>{h.get('subheadline','Expert guidance that delivers real, measurable results for serious students.')}</p>
    <button class="btn-main">{h.get('cta','Get Started Free')}</button>
    <div class="trust">⭐⭐⭐⭐⭐ {h.get('trust_line','Join 10,000+ successful students')}</div>
  </div>
</section>

<!-- LOGOS -->
<div class="logos-bar">
  <div class="logo-txt">Times of India</div>
  <div class="logo-txt">Education World</div>
  <div class="logo-txt">India Today</div>
  <div class="logo-txt">NDTV Education</div>
  <div class="logo-txt">The Hindu</div>
</div>

<!-- PAIN POINTS -->
<section class="pain-section">
  <div class="inner">
    <span class="sec-over">The Problem</span>
    <div class="sec-title">{pp.get('headline','Are these struggles holding you back?')}</div>
    <div class="pain-grid">{pain_html}</div>
  </div>
</section>

<!-- FEATURES -->
<section class="feat-section">
  <div class="inner">
    <span class="sec-over">Our Solution</span>
    <div class="sec-title">{ft.get('headline','Everything you need to succeed')}</div>
    <img class="feat-top-img" src="{feat_img}" alt="features"/>
    <div class="feat-grid">{feat_html}</div>
  </div>
</section>

<!-- SOCIAL PROOF -->
<section class="proof-section">
  <div class="inner">
    <span class="sec-over">Proven Results</span>
    <div class="sec-title">{sp.get('headline','Students achieving real results every day')}</div>
    <img class="proof-top-img" src="{proof_img}" alt="results"/>
    <div class="metrics-row">{metrics_html}</div>
    <div class="testi-grid">{testis_html}</div>
  </div>
</section>

<!-- COMPARISON -->
<section class="compare-section">
  <div class="inner" style="text-align:center">
    <span class="sec-over">Why Choose Us</span>
    <div class="sec-title" style="margin-bottom:36px">{cp.get('headline','Why students choose us over others')}</div>
    <table class="ctable">
      <thead><tr><th>Feature</th><th>Traditional Coaching</th><th>With Us ✅</th></tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
  </div>
</section>

<!-- CTA -->
<div class="cta-section">
  <div class="cta-bg"><img src="{cta_img}" alt="success"/></div>
  <div class="cta-overlay"></div>
  <div class="cta-inner">
    <h2>{cf.get('headline','Your success story starts today')}</h2>
    <p>{cf.get('subtext','Join thousands of students already achieving their dreams')}</p>
    <button class="btn-main" style="font-size:1.02rem;padding:18px 48px">{cf.get('cta','Book Free Demo Class')}</button>
    <div class="urgency">⚡ <em>{cf.get('urgency','Only 8 spots left this month — Act now!')}</em></div>
  </div>
</div>

<!-- FAQ -->
<section class="faq-section">
  <div class="faq-inner">
    <div class="faq-title">Frequently Asked Questions</div>
    {faqs_html}
  </div>
</section>

<footer>© 2025 · {keyword} · All rights reserved · Built with MarketMind AI</footer>

<script>
document.querySelectorAll('.faq button').forEach(b=>{{
  b.addEventListener('click',function(){{
    this.classList.toggle('open');
    this.nextElementSibling.classList.toggle('show');
  }});
}});
document.querySelectorAll('.btn-main,.nav-cta').forEach(b=>{{
  b.addEventListener('click',()=>document.querySelector('.cta-section').scrollIntoView({{behavior:'smooth'}}));
}});
</script>
</body>
</html>"""


# Keep backward compatibility
async def generate_lp_content_and_build(keyword: str, style: str, persona: str = "student") -> tuple:
    data = await generate_lp_content(keyword, style, persona)
    html = await build_html_with_images(keyword, data) if data else "<h1>Error</h1>"
    return data, html

# Sync wrapper for main.py
def build_html(keyword: str, data: dict) -> str:
    """Sync wrapper — runs async build"""
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, build_html_with_images(keyword, data))
                return future.result(timeout=30)
        else:
            return loop.run_until_complete(build_html_with_images(keyword, data))
    except Exception as e:
        return f"<h1>Error building page: {e}</h1>"
