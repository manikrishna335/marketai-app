from seo_agent import call_groq
import json, re

def img(query, w=1200, h=600):
    q = query.replace(" ", ",").replace("/",",")
    return f"https://source.unsplash.com/{w}x{h}/?{q}"

def img_sq(query, size=400):
    q = query.replace(" ", ",")
    return f"https://source.unsplash.com/{size}x{size}/?{q}"

async def generate_lp_content(keyword: str, style: str, persona: str = "student") -> dict:
    prompt = f"""Generate landing page content for keyword "{keyword}", persona "{persona}".
Return ONLY valid JSON:
{{
  "style_recommendation": "minimalist OR tech OR academic — pick best for this keyword",
  "primary_color": "#hex color that fits this industry",
  "accent_color": "#hex accent color",
  "hero": {{
    "headline": "Powerful 7-word headline",
    "subheadline": "Solution subheadline under 20 words",
    "cta": "CTA button text",
    "trust_line": "Join 10000+ students",
    "image_query": "3 word image query e.g. student studying laptop"
  }},
  "pain_points": {{
    "headline": "Pain section headline",
    "cards": [
      {{"icon":"😓","title":"3 word pain","desc":"12 word relatable description","image_query":"pain image"}},
      {{"icon":"😰","title":"3 word pain","desc":"12 word description","image_query":"stress image"}},
      {{"icon":"😤","title":"3 word pain","desc":"12 word description","image_query":"frustrated image"}},
      {{"icon":"😩","title":"3 word pain","desc":"12 word description","image_query":"overwhelmed image"}}
    ]
  }},
  "features": {{
    "headline": "Features headline",
    "image_query": "solution success image",
    "items": [
      {{"icon":"✅","title":"Feature","desc":"15 word benefit"}},
      {{"icon":"🚀","title":"Feature","desc":"15 word benefit"}},
      {{"icon":"💡","title":"Feature","desc":"15 word benefit"}},
      {{"icon":"🎯","title":"Feature","desc":"15 word benefit"}},
      {{"icon":"📊","title":"Feature","desc":"15 word benefit"}},
      {{"icon":"🏆","title":"Feature","desc":"15 word benefit"}}
    ]
  }},
  "social_proof": {{
    "headline": "Results headline",
    "image_query": "happy students success",
    "metrics": [
      {{"number":"10,000+","label":"Students Helped"}},
      {{"number":"98%","label":"Success Rate"}},
      {{"number":"4.9★","label":"Average Rating"}},
      {{"number":"50+","label":"Expert Tutors"}}
    ],
    "testimonials": [
      {{"name":"Priya S.","role":"IB Student Mumbai","quote":"25 word genuine quote","avatar_query":"indian student girl"}},
      {{"name":"Arjun K.","role":"Grade 12 Delhi","quote":"25 word genuine quote","avatar_query":"indian student boy"}},
      {{"name":"Meera R.","role":"Parent Bangalore","quote":"25 word parent quote","avatar_query":"indian parent"}}
    ]
  }},
  "comparison": {{
    "headline": "Why choose us headline",
    "rows": [
      {{"feature":"Learning Pace","old":"Fixed rigid schedule","new":"Learn anytime your pace"}},
      {{"feature":"Expert Access","old":"40 students per teacher","new":"1-on-1 personal sessions"}},
      {{"feature":"Cost","old":"₹5000/month coaching","new":"Plans from ₹999/month"}},
      {{"feature":"Progress","old":"Wait for exam results","new":"Real-time dashboard"}},
      {{"feature":"Support","old":"Office hours only","new":"24/7 doubt resolution"}},
      {{"feature":"Material","old":"Outdated printed notes","new":"Updated digital resources"}},
      {{"feature":"Results","old":"No improvement guarantee","new":"Grade improvement assured"}},
      {{"feature":"Flexibility","old":"Fixed batch timings","new":"Choose your schedule"}}
    ]
  }},
  "cta_faq": {{
    "headline": "Start today headline",
    "subtext": "15 word compelling close",
    "cta": "Final CTA",
    "urgency": "Only 8 spots left this month",
    "bg_image_query": "success celebration graduation",
    "faqs": [
      {{"q":"Real objection?","a":"Reassuring 20 word answer"}},
      {{"q":"Real objection?","a":"Reassuring 20 word answer"}},
      {{"q":"Real objection?","a":"Reassuring 20 word answer"}},
      {{"q":"Real objection?","a":"Reassuring 20 word answer"}},
      {{"q":"Real objection?","a":"Reassuring 20 word answer"}}
    ]
  }}
}}"""
    raw = await call_groq(prompt, 2000)
    try:
        clean = re.sub(r'```json|```','',raw).strip()
        return json.loads(clean)
    except:
        return None

def build_html(keyword: str, data: dict) -> str:
    """Auto-pick best style based on AI recommendation and build full HTML"""
    style = data.get('style_recommendation', 'minimalist').lower()
    primary = data.get('primary_color', '#6C5CE7')
    accent = data.get('accent_color', '#22C55E')

    h = data['hero']
    pp = data['pain_points']
    ft = data['features']
    sp = data['social_proof']
    cp = data['comparison']
    cf = data['cta_faq']

    hero_img = img(h.get('image_query', keyword + ' student'), 1400, 700)
    feat_img = img(ft.get('image_query', keyword + ' success'), 1200, 400)
    proof_img = img(sp.get('image_query', 'students success'), 1200, 300)
    cta_bg = img(cf.get('bg_image_query', 'success graduation'), 1400, 500)

    pain_cards_html = ""
    for c in pp['cards']:
        pain_cards_html += f"""
        <div class="pain-card">
          <img src="{img(c.get('image_query','student'), 480, 260)}" alt="{c['title']}" loading="lazy"/>
          <div class="pc-body">
            <span class="pc-icon">{c['icon']}</span>
            <h3>{c['title']}</h3>
            <p>{c['desc']}</p>
          </div>
        </div>"""

    feat_items_html = ""
    for f in ft['items']:
        feat_items_html += f"""
        <div class="feat-item">
          <div class="fi-icon">{f['icon']}</div>
          <div><h3>{f['title']}</h3><p>{f['desc']}</p></div>
        </div>"""

    metrics_html = "".join([f'<div class="metric"><div class="m-n">{m["number"]}</div><div class="m-l">{m["label"]}</div></div>' for m in sp['metrics']])

    testis_html = ""
    for t in sp['testimonials']:
        testis_html += f"""
        <div class="testi">
          <div class="stars">★★★★★</div>
          <p>"{t['quote']}"</p>
          <div class="testi-who">
            <img src="{img_sq(t.get('avatar_query','person portrait'), 44)}" alt="{t['name']}"/>
            <div><strong>{t['name']}</strong><span>{t['role']}</span></div>
          </div>
        </div>"""

    rows_html = "".join([f"<tr><td class='f'>{r['feature']}</td><td class='o'>✗ {r['old']}</td><td class='n'>✓ {r['new']}</td></tr>" for r in cp['rows']])

    faqs_html = "".join([f'<div class="faq"><button onclick="this.classList.toggle(\'open\');this.nextElementSibling.classList.toggle(\'show\')">{f["q"]}<span>+</span></button><div class="faq-a"><p>{f["a"]}</p></div></div>' for f in cf['faqs']])

    # Pick font and style based on recommendation
    if style == 'academic':
        font_url = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Outfit:wght@300;400;500;600&display=swap"
        heading_font = "'Cormorant Garamond', serif"
        body_font = "'Outfit', sans-serif"
    elif style == 'tech':
        font_url = "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap"
        heading_font = "'Space Grotesk', sans-serif"
        body_font = "'Space Grotesk', sans-serif"
    else:
        font_url = "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=DM+Sans:wght@300;400;500;600&display=swap"
        heading_font = "'Playfair Display', serif"
        body_font = "'DM Sans', sans-serif"

    dark_bg = style == 'tech'
    bg_color = '#050810' if dark_bg else '#ffffff'
    text_color = '#e8f0f7' if dark_bg else '#1a1a1a'
    card_bg = '#0c1220' if dark_bg else '#ffffff'
    section_bg = '#080d1a' if dark_bg else '#f8f9fa'
    muted = 'rgba(255,255,255,0.5)' if dark_bg else '#666666'
    border_color = '#1a2540' if dark_bg else '#e5e7eb'
    nav_bg = 'rgba(5,8,16,0.92)' if dark_bg else 'rgba(255,255,255,0.95)'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{h['headline']} | {keyword}</title>
<link href="{font_url}" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--primary:{primary};--accent:{accent};--bg:{bg_color};--text:{text_color};--card:{card_bg};--section:{section_bg};--muted:{muted};--border:{border_color}}}
body{{font-family:{body_font};background:var(--bg);color:var(--text);line-height:1.7;overflow-x:hidden}}
img{{max-width:100%;height:auto}}

nav{{position:fixed;top:0;left:0;right:0;z-index:100;padding:14px 48px;display:flex;align-items:center;justify-content:space-between;background:{nav_bg};backdrop-filter:blur(12px);border-bottom:1px solid var(--border)}}
.nav-logo{{font-family:{heading_font};font-size:1.2rem;font-weight:700;color:var(--text)}}
.nav-cta{{background:var(--primary);color:#fff;padding:9px 22px;border:none;border-radius:6px;font-weight:700;font-size:.85rem;cursor:pointer;transition:all .2s;font-family:{body_font}}}
.nav-cta:hover{{opacity:.9;transform:translateY(-1px)}}

.hero{{min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;position:relative;overflow:hidden;padding:100px 24px 60px}}
.hero-bg{{position:absolute;inset:0;background:url('{hero_img}') center/cover;{'filter:brightness(.2)' if dark_bg else 'filter:brightness(.35)'}}}
.hero-overlay{{position:absolute;inset:0;background:{'linear-gradient(135deg,rgba(5,8,16,0.95),rgba(12,18,32,0.8))' if dark_bg else f'linear-gradient(135deg,rgba(0,0,0,0.75),rgba(0,0,0,0.5))'}}}
.hero-content{{position:relative;z-index:2;max-width:760px;color:#fff}}
.hero-tag{{display:inline-block;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.25);padding:6px 18px;border-radius:20px;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;margin-bottom:22px;backdrop-filter:blur(8px)}}
.hero h1{{font-family:{heading_font};font-size:clamp(2rem,5vw,3.8rem);font-weight:700;line-height:1.1;margin-bottom:18px;letter-spacing:-.02em}}
.hero h1 em{{font-style:normal;color:var(--primary)}}
.hero p{{font-size:1.05rem;opacity:.88;margin-bottom:32px;max-width:560px;margin-left:auto;margin-right:auto}}
.btn-main{{background:var(--primary);color:#fff;padding:16px 36px;border:none;border-radius:8px;font-weight:700;font-size:.95rem;cursor:pointer;transition:all .2s;font-family:{body_font}}}
.btn-main:hover{{opacity:.9;transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.3)}}
.trust{{margin-top:18px;font-size:.78rem;opacity:.7;display:flex;align-items:center;justify-content:center;gap:8px}}
.trust-avs{{display:flex}}.trust-avs img{{width:26px;height:26px;border-radius:50%;border:2px solid rgba(255,255,255,.3);margin-right:-7px;object-fit:cover}}

section{{padding:88px 48px}}
.inner{{max-width:1100px;margin:0 auto}}
.sec-over{{font-size:.62rem;text-transform:uppercase;letter-spacing:.16em;color:var(--primary);font-weight:700;margin-bottom:10px;display:block}}
.sec-title{{font-family:{heading_font};font-size:clamp(1.6rem,3vw,2.6rem);font-weight:700;margin-bottom:36px;line-height:1.15}}

.pain-section{{background:var(--section)}}
.pain-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px}}
.pain-card{{background:var(--card);border-radius:14px;overflow:hidden;{'border:1px solid #1a2540' if dark_bg else 'box-shadow:0 4px 20px rgba(0,0,0,.06)'};transition:all .25s}}
.pain-card:hover{{transform:translateY(-4px);{'box-shadow:0 0 20px rgba(108,92,231,.15)' if dark_bg else 'box-shadow:0 12px 30px rgba(0,0,0,.1)'}}}
.pain-card img{{width:100%;height:170px;object-fit:cover;display:block}}
.pc-body{{padding:18px}}
.pc-icon{{font-size:1.6rem;display:block;margin-bottom:8px}}
.pc-body h3{{font-size:.95rem;font-weight:700;margin-bottom:6px}}
.pc-body p{{font-size:.82rem;color:var(--muted)}}

.feat-section{{background:var(--bg)}}
.feat-img{{width:100%;height:300px;object-fit:cover;border-radius:16px;margin-bottom:44px;display:block;{'filter:brightness(.7) saturate(.8)' if dark_bg else ''}}}
.feat-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}}
.feat-item{{background:var(--card);{'border:1px solid #1a2540' if dark_bg else 'border:1px solid #eee'};border-radius:12px;padding:22px;display:flex;gap:14px;align-items:flex-start;transition:all .2s}}
.feat-item:hover{{border-color:var(--primary)}}
.fi-icon{{font-size:1.6rem;flex-shrink:0;margin-top:2px}}
.feat-item h3{{font-size:.9rem;font-weight:700;margin-bottom:5px}}
.feat-item p{{font-size:.8rem;color:var(--muted)}}

.proof-section{{background:var(--section)}}
.proof-img{{width:100%;height:200px;object-fit:cover;border-radius:14px;margin-bottom:44px;display:block;opacity:.9}}
.metrics-row{{display:flex;justify-content:center;gap:48px;flex-wrap:wrap;margin-bottom:48px;padding:28px 0;border-top:1px solid var(--border);border-bottom:1px solid var(--border)}}
.metric{{text-align:center}}
.m-n{{font-family:{heading_font};font-size:2.2rem;font-weight:700;color:var(--primary)}}
.m-l{{font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-top:4px}}
.testi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}}
.testi{{background:var(--card);{'border:1px solid #1a2540' if dark_bg else 'box-shadow:0 4px 16px rgba(0,0,0,.05)'};border-radius:14px;padding:24px}}
.stars{{color:#f59e0b;font-size:.85rem;margin-bottom:10px}}
.testi p{{font-size:.86rem;color:var(--muted);font-style:italic;margin-bottom:16px;line-height:1.7}}
.testi-who{{display:flex;align-items:center;gap:10px}}
.testi-who img{{width:40px;height:40px;border-radius:50%;object-fit:cover}}
.testi-who strong{{display:block;font-size:.82rem;font-weight:700}}
.testi-who span{{font-size:.72rem;color:var(--muted)}}

.compare-section{{background:var(--bg)}}
.ctable{{width:100%;max-width:820px;margin:0 auto;border-collapse:collapse;border-radius:14px;overflow:hidden;{'box-shadow:none' if dark_bg else 'box-shadow:0 4px 24px rgba(0,0,0,.07)'}}}
.ctable thead{{background:{'#0c1220' if dark_bg else '#1a1a1a'}}}
.ctable th{{padding:14px 20px;text-align:left;font-size:.72rem;color:{'#9AA4C7' if dark_bg else '#fff'};text-transform:uppercase;letter-spacing:.07em}}
.ctable td{{padding:13px 20px;font-size:.84rem;border-bottom:1px solid var(--border);background:var(--card)}}
td.f{{font-weight:700}}
td.o{{color:#dc2626}}
td.n{{color:#16a34a;font-weight:600}}

.cta-section{{position:relative;text-align:center;color:#fff;overflow:hidden}}
.cta-bg{{position:absolute;inset:0;background:url('{cta_bg}') center/cover;filter:brightness(.25)}}
.cta-overlay{{position:absolute;inset:0;background:linear-gradient(135deg,rgba({','.join(str(int(primary.lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.9),rgba(0,0,0,.7))}}
.cta-inner{{position:relative;z-index:2;padding:88px 48px}}
.cta-section h2{{font-family:{heading_font};font-size:clamp(1.8rem,4vw,3rem);font-weight:700;margin-bottom:12px}}
.cta-section p{{opacity:.88;margin-bottom:28px;max-width:480px;margin-left:auto;margin-right:auto;font-size:.95rem}}
.urgency{{margin-top:14px;font-size:.76rem;opacity:.7}}
.urgency em{{color:{'#22C55E' if dark_bg else '#ffdd57'};font-style:normal;font-weight:700}}

.faq-section{{background:var(--section)}}
.faq-inner{{max-width:720px;margin:0 auto}}
.faq-title{{font-family:{heading_font};font-size:1.8rem;font-weight:700;text-align:center;margin-bottom:28px}}
.faq{{border-bottom:1px solid var(--border)}}
.faq button{{width:100%;padding:16px 0;background:none;border:none;color:var(--text);text-align:left;font-size:.9rem;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;font-family:{body_font};gap:10px}}
.faq button span{{color:var(--primary);font-size:1.1rem;transition:transform .2s;flex-shrink:0}}
.faq button.open span{{transform:rotate(45deg)}}
.faq-a{{display:none;padding:0 0 14px;font-size:.85rem;color:var(--muted);line-height:1.7}}
.faq-a.show{{display:block}}
.logos-bar{{padding:24px 48px;{'background:#080d1a' if dark_bg else 'background:#fff'};border-top:1px solid var(--border);border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:center;gap:40px;flex-wrap:wrap}}
.logo-text{{font-size:.75rem;font-weight:700;color:{'rgba(255,255,255,.2)' if dark_bg else '#d0d0d0'};letter-spacing:.06em;text-transform:uppercase}}
footer{{background:{'#030508' if dark_bg else '#1a1a1a'};color:rgba(255,255,255,.4);text-align:center;padding:22px;font-size:.72rem}}

@media(max-width:768px){{
  nav,section{{padding-left:20px;padding-right:20px}}
  .logos-bar{{padding:16px 20px;gap:20px}}
  .metrics-row{{gap:24px}}
  .cta-inner{{padding:60px 20px}}
}}
</style>
</head>
<body>

<nav>
  <div class="nav-logo">{keyword[:22]}</div>
  <button class="nav-cta" onclick="document.querySelector('.cta-section').scrollIntoView({{behavior:'smooth'}})">{h['cta']}</button>
</nav>

<section class="hero" style="padding:0">
  <div class="hero-bg"></div>
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <div class="hero-tag">{keyword}</div>
    <h1>{h['headline']}</h1>
    <p>{h['subheadline']}</p>
    <button class="btn-main">{h['cta']}</button>
    <div class="trust">
      <div class="trust-avs">
        <img src="{img_sq('student portrait', 26)}" alt=""/>
        <img src="{img_sq('person smiling', 26)}" alt=""/>
        <img src="{img_sq('young student', 26)}" alt=""/>
      </div>
      {h['trust_line']}
    </div>
  </div>
</section>

<div class="logos-bar">
  <div class="logo-text">Times of India</div>
  <div class="logo-text">Education World</div>
  <div class="logo-text">India Today</div>
  <div class="logo-text">NDTV Education</div>
  <div class="logo-text">The Hindu</div>
</div>

<section class="pain-section">
  <div class="inner">
    <span class="sec-over">The Problem</span>
    <div class="sec-title">{pp['headline']}</div>
    <div class="pain-grid">{pain_cards_html}</div>
  </div>
</section>

<section class="feat-section">
  <div class="inner">
    <span class="sec-over">Our Solution</span>
    <div class="sec-title">{ft['headline']}</div>
    <img class="feat-img" src="{feat_img}" alt="features"/>
    <div class="feat-grid">{feat_items_html}</div>
  </div>
</section>

<section class="proof-section">
  <div class="inner">
    <span class="sec-over">Proven Results</span>
    <div class="sec-title">{sp['headline']}</div>
    <img class="proof-img" src="{proof_img}" alt="results"/>
    <div class="metrics-row">{metrics_html}</div>
    <div class="testi-grid">{testis_html}</div>
  </div>
</section>

<section class="compare-section">
  <div class="inner" style="text-align:center">
    <span class="sec-over">Why Choose Us</span>
    <div class="sec-title" style="margin-bottom:32px">{cp['headline']}</div>
    <table class="ctable">
      <thead><tr><th>Feature</th><th>Traditional Way</th><th>With Us</th></tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
  </div>
</section>

<div class="cta-section">
  <div class="cta-bg"></div>
  <div class="cta-overlay"></div>
  <div class="cta-inner">
    <h2>{cf['headline']}</h2>
    <p>{cf['subtext']}</p>
    <button class="btn-main">{cf['cta']}</button>
    <div class="urgency">⚡ <em>{cf['urgency']}</em></div>
  </div>
</div>

<section class="faq-section">
  <div class="faq-inner">
    <div class="faq-title">Frequently Asked Questions</div>
    {faqs_html}
  </div>
</section>

<footer>© 2025 · {keyword} · All rights reserved · Built with MarketMind AI</footer>
<script>
document.querySelectorAll('.btn-main,.nav-cta').forEach(b=>b.addEventListener('click',()=>{{
  document.querySelector('.cta-section').scrollIntoView({{behavior:'smooth'}});
}}));
</script>
</body>
</html>"""
