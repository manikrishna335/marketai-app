from seo_agent import call_groq
import json, re

# Picsum photos - always reliable, beautiful, free
def img(w, h, seed):
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"

# Curated seeds for different contexts
SEEDS = {
    "hero": ["student1","library2","study3","campus4","education5"],
    "pain": ["tired1","stress2","confused3","overwhelmed4"],
    "feature": ["success1","growth2","learning3"],
    "avatar": ["face1","face2","face3","face4","face5","face6"],
    "section": ["classroom1","laptop2","books3"]
}

async def generate_lp_content(keyword: str, style: str, persona: str = "student") -> dict:
    prompt = f"""You are a world-class conversion copywriter. Generate landing page content for:
Keyword: "{keyword}"
Style: {style.upper()}
Persona: {persona.upper()}

Return ONLY valid JSON, no markdown, no extra text:
{{
  "hero": {{
    "headline": "Powerful 6-8 word headline addressing pain point",
    "subheadline": "Solution-focused subheadline under 20 words",
    "cta": "CTA button text",
    "trust_line": "Social proof line e.g. Join 50000+ students"
  }},
  "pain_points": {{
    "headline": "Relatable section headline",
    "cards": [
      {{"icon": "😓", "title": "Pain title 3 words", "desc": "Relatable 12 word description of this struggle"}},
      {{"icon": "😰", "title": "Pain title 3 words", "desc": "Relatable 12 word description"}},
      {{"icon": "😤", "title": "Pain title 3 words", "desc": "Relatable 12 word description"}},
      {{"icon": "😩", "title": "Pain title 3 words", "desc": "Relatable 12 word description"}}
    ]
  }},
  "features": {{
    "headline": "Features section headline",
    "items": [
      {{"icon": "✅", "title": "Feature name", "desc": "Clear 15 word benefit description"}},
      {{"icon": "🚀", "title": "Feature name", "desc": "Clear 15 word benefit description"}},
      {{"icon": "💡", "title": "Feature name", "desc": "Clear 15 word benefit description"}},
      {{"icon": "🎯", "title": "Feature name", "desc": "Clear 15 word benefit description"}},
      {{"icon": "📊", "title": "Feature name", "desc": "Clear 15 word benefit description"}},
      {{"icon": "🏆", "title": "Feature name", "desc": "Clear 15 word benefit description"}}
    ]
  }},
  "social_proof": {{
    "headline": "Results headline",
    "metrics": [
      {{"number": "10,000+", "label": "Students Helped"}},
      {{"number": "98%", "label": "Success Rate"}},
      {{"number": "4.9★", "label": "Average Rating"}},
      {{"number": "50+", "label": "Expert Tutors"}}
    ],
    "testimonials": [
      {{"name": "Priya S.", "role": "IB Student, Mumbai", "quote": "Genuine 25 word student testimonial about results"}},
      {{"name": "Arjun K.", "role": "Grade 12, Delhi", "quote": "Genuine 25 word student testimonial about experience"}},
      {{"name": "Meera R.", "role": "Parent, Bangalore", "quote": "Genuine 25 word parent testimonial about child progress"}}
    ]
  }},
  "comparison": {{
    "headline": "Why students choose us headline",
    "rows": [
      {{"feature": "Learning Pace", "old": "Fixed schedule, no flexibility", "new": "Learn at your own pace, anytime"}},
      {{"feature": "Expert Access", "old": "One teacher for 40 students", "new": "1-on-1 sessions with top educators"}},
      {{"feature": "Progress Tracking", "old": "Wait for exam results", "new": "Real-time progress dashboard"}},
      {{"feature": "Cost", "old": "Expensive coaching centres", "new": "Affordable plans from ₹999/month"}},
      {{"feature": "Study Material", "old": "Outdated printed notes", "new": "Updated digital resources always"}},
      {{"feature": "Doubt Solving", "old": "Wait till next class", "new": "Instant doubt resolution 24/7"}},
      {{"feature": "Results", "old": "No guarantee of improvement", "new": "Guaranteed grade improvement"}},
      {{"feature": "Support", "old": "On your own after class", "new": "Dedicated mentor support always"}}
    ]
  }},
  "cta_faq": {{
    "headline": "Start your journey today headline",
    "subtext": "Compelling 15 word closing statement",
    "cta": "Final CTA button text",
    "urgency": "Scarcity line e.g. Only 8 spots left this month",
    "faqs": [
      {{"q": "Real student objection question?", "a": "Reassuring 20 word answer"}},
      {{"q": "Real student objection question?", "a": "Reassuring 20 word answer"}},
      {{"q": "Real student objection question?", "a": "Reassuring 20 word answer"}},
      {{"q": "Real student objection question?", "a": "Reassuring 20 word answer"}},
      {{"q": "Real student objection question?", "a": "Reassuring 20 word answer"}}
    ]
  }}
}}"""

    raw = await call_groq(prompt, 2000)
    try:
        clean = re.sub(r'```json|```', '', raw).strip()
        return json.loads(clean)
    except:
        return None


def build_minimalist_html(keyword: str, data: dict) -> str:
    h = data["hero"]
    pp = data["pain_points"]
    ft = data["features"]
    sp = data["social_proof"]
    cp = data["comparison"]
    cf = data["cta_faq"]

    pain_cards = ""
    for i, c in enumerate(pp["cards"]):
        pain_cards += f"""
        <div class="pain-card">
          <div class="pain-img"><img src="{img(480,300,SEEDS['pain'][i%4])}" alt="{c['title']}" loading="lazy"/></div>
          <div class="pain-body">
            <div class="pain-icon">{c['icon']}</div>
            <h3>{c['title']}</h3>
            <p>{c['desc']}</p>
          </div>
        </div>"""

    feat_items = ""
    for f in ft["items"]:
        feat_items += f"""
        <div class="feat-card">
          <div class="feat-icon">{f['icon']}</div>
          <h3>{f['title']}</h3>
          <p>{f['desc']}</p>
        </div>"""

    metrics = "".join([f'<div class="metric"><div class="m-n">{m["number"]}</div><div class="m-l">{m["label"]}</div></div>' for m in sp["metrics"]])

    testis = ""
    for i, t in enumerate(sp["testimonials"]):
        testis += f"""
        <div class="testi">
          <div class="stars">★★★★★</div>
          <p>"{t['quote']}"</p>
          <div class="testi-who">
            <img src="{img(56,56,SEEDS['avatar'][i])}" alt="{t['name']}"/>
            <div><strong>{t['name']}</strong><span>{t['role']}</span></div>
          </div>
        </div>"""

    rows = "".join([f"<tr><td class='f'>{r['feature']}</td><td class='o'>✗ {r['old']}</td><td class='n'>✓ {r['new']}</td></tr>" for r in cp["rows"]])

    faqs = ""
    for f in cf["faqs"]:
        faqs += f"""<div class="faq"><button onclick="toggle(this)">{f['q']}<span>+</span></button><div class="ans"><p>{f['a']}</p></div></div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{h['headline']}</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--ink:#0f0f0f;--muted:#6b7280;--line:#e5e7eb;--bg:#fafaf8;--white:#ffffff;--accent:#2563eb;--accent-light:#eff6ff}}
body{{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--ink);line-height:1.6}}

/* NAV */
nav{{position:fixed;top:0;left:0;right:0;z-index:100;padding:16px 48px;display:flex;align-items:center;justify-content:space-between;background:rgba(250,250,248,.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}}
.nav-logo{{font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700}}
.nav-cta{{background:var(--ink);color:#fff;padding:9px 22px;border-radius:6px;font-size:.82rem;font-weight:600;border:none;cursor:pointer;transition:all .2s}}
.nav-cta:hover{{background:#1a1a1a;transform:translateY(-1px)}}

/* HERO */
.hero{{min-height:100vh;display:grid;grid-template-columns:1fr 1fr;align-items:center;padding:120px 48px 80px;gap:64px;max-width:1200px;margin:0 auto}}
.hero-text h1{{font-family:'Playfair Display',serif;font-size:clamp(2.4rem,4.5vw,3.8rem);font-weight:800;line-height:1.08;letter-spacing:-.03em;margin-bottom:20px}}
.hero-text h1 em{{font-style:italic;color:var(--accent)}}
.hero-text p{{font-size:1.05rem;color:var(--muted);margin-bottom:32px;max-width:440px;line-height:1.7}}
.hero-btns{{display:flex;gap:12px;align-items:center;flex-wrap:wrap}}
.btn-primary{{background:var(--accent);color:#fff;padding:14px 28px;border-radius:8px;font-weight:600;font-size:.9rem;border:none;cursor:pointer;transition:all .2s}}
.btn-primary:hover{{background:#1d4ed8;transform:translateY(-2px);box-shadow:0 8px 24px rgba(37,99,235,.3)}}
.btn-sec{{color:var(--muted);font-size:.85rem;text-decoration:underline;cursor:pointer;background:none;border:none}}
.trust{{margin-top:20px;font-size:.78rem;color:var(--muted);display:flex;align-items:center;gap:8px}}
.trust-avatars{{display:flex}}
.trust-avatars img{{width:28px;height:28px;border-radius:50%;border:2px solid #fff;margin-right:-8px;object-fit:cover}}
.hero-img{{border-radius:20px;overflow:hidden;box-shadow:0 32px 80px rgba(0,0,0,.12);position:relative}}
.hero-img img{{width:100%;height:520px;object-fit:cover;display:block}}
.hero-img-badge{{position:absolute;bottom:20px;left:20px;background:#fff;border-radius:10px;padding:12px 16px;box-shadow:0 8px 24px rgba(0,0,0,.1);display:flex;align-items:center;gap:10px}}
.badge-icon{{font-size:1.4rem}}
.badge-text strong{{display:block;font-size:.82rem;font-weight:700}}
.badge-text span{{font-size:.7rem;color:var(--muted)}}

/* LOGOS */
.logos{{padding:32px 48px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:center;gap:48px;flex-wrap:wrap;background:var(--white)}}
.logo-item{{font-size:.8rem;font-weight:600;color:#c4c4c4;letter-spacing:.05em;text-transform:uppercase}}

/* PAIN */
.pain-section{{padding:96px 48px;max-width:1200px;margin:0 auto}}
.sec-label{{font-size:.65rem;text-transform:uppercase;letter-spacing:.15em;color:var(--accent);font-weight:600;margin-bottom:10px}}
.sec-title{{font-family:'Playfair Display',serif;font-size:clamp(1.8rem,3vw,2.8rem);font-weight:700;margin-bottom:48px;max-width:600px;line-height:1.2}}
.pain-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px}}
.pain-card{{background:var(--white);border-radius:16px;overflow:hidden;border:1px solid var(--line);transition:all .3s}}
.pain-card:hover{{transform:translateY(-4px);box-shadow:0 20px 40px rgba(0,0,0,.08);border-color:transparent}}
.pain-img img{{width:100%;height:170px;object-fit:cover;display:block}}
.pain-body{{padding:20px}}
.pain-icon{{font-size:1.5rem;margin-bottom:8px}}
.pain-body h3{{font-size:.95rem;font-weight:700;margin-bottom:6px}}
.pain-body p{{font-size:.82rem;color:var(--muted);line-height:1.6}}

/* FEATURES */
.feat-section{{padding:96px 48px;background:var(--ink);color:#fff}}
.feat-inner{{max-width:1200px;margin:0 auto}}
.feat-section .sec-label{{color:#60a5fa}}
.feat-section .sec-title{{color:#fff;margin-bottom:16px}}
.feat-sub{{color:rgba(255,255,255,.5);font-size:.9rem;margin-bottom:48px;max-width:500px}}
.feat-img{{width:100%;height:300px;object-fit:cover;border-radius:16px;margin-bottom:48px;display:block}}
.feat-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}}
.feat-card{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:24px;transition:all .2s}}
.feat-card:hover{{background:rgba(255,255,255,.09);border-color:rgba(255,255,255,.15)}}
.feat-icon{{font-size:1.8rem;margin-bottom:12px}}
.feat-card h3{{font-size:.92rem;font-weight:700;margin-bottom:6px;color:#fff}}
.feat-card p{{font-size:.8rem;color:rgba(255,255,255,.5);line-height:1.6}}

/* PROOF */
.proof-section{{padding:96px 48px;max-width:1200px;margin:0 auto}}
.metrics-row{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:64px}}
.metric{{background:var(--white);border:1px solid var(--line);border-radius:14px;padding:24px;text-align:center}}
.m-n{{font-family:'Playfair Display',serif;font-size:2.2rem;font-weight:700;color:var(--accent);margin-bottom:4px}}
.m-l{{font-size:.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}}
.testi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}}
.testi{{background:var(--white);border:1px solid var(--line);border-radius:16px;padding:28px}}
.stars{{color:#f59e0b;font-size:.9rem;margin-bottom:12px}}
.testi p{{font-size:.88rem;color:var(--ink);line-height:1.7;margin-bottom:20px;font-style:italic}}
.testi-who{{display:flex;align-items:center;gap:12px}}
.testi-who img{{width:44px;height:44px;border-radius:50%;object-fit:cover}}
.testi-who strong{{display:block;font-size:.82rem;font-weight:700}}
.testi-who span{{font-size:.72rem;color:var(--muted)}}

/* COMPARE */
.compare-section{{padding:96px 48px;background:var(--accent-light)}}
.compare-inner{{max-width:860px;margin:0 auto}}
.compare-table{{width:100%;border-collapse:separate;border-spacing:0;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.06)}}
thead tr{{background:var(--ink)}}
th{{padding:16px 20px;text-align:left;font-size:.75rem;font-weight:600;color:#fff;text-transform:uppercase;letter-spacing:.08em}}
td{{padding:14px 20px;font-size:.84rem;background:#fff;border-bottom:1px solid var(--line)}}
td.f{{font-weight:600;color:var(--ink)}}
td.o{{color:#dc2626}}
td.n{{color:#16a34a;font-weight:600}}
tr:last-child td{{border-bottom:none}}

/* CTA */
.cta-section{{padding:96px 48px;text-align:center;background:var(--white)}}
.cta-section h2{{font-family:'Playfair Display',serif;font-size:clamp(2rem,4vw,3rem);font-weight:700;margin-bottom:14px}}
.cta-section p{{color:var(--muted);margin-bottom:32px;font-size:.95rem}}
.urgency{{margin-top:16px;font-size:.78rem;color:var(--muted)}}
.urgency span{{color:var(--accent);font-weight:600}}

/* FAQ */
.faq-section{{padding:64px 48px;max-width:720px;margin:0 auto}}
.faq-section h2{{font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:700;text-align:center;margin-bottom:32px}}
.faq{{border-bottom:1px solid var(--line);padding:4px 0}}
.faq button{{width:100%;padding:16px 0;background:none;border:none;text-align:left;font-size:.9rem;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;font-family:'DM Sans',sans-serif;color:var(--ink)}}
.faq button span{{color:var(--accent);font-size:1.2rem;transition:transform .2s;flex-shrink:0}}
.faq button.open span{{transform:rotate(45deg)}}
.ans{{display:none;padding:0 0 16px;font-size:.85rem;color:var(--muted);line-height:1.7}}
.ans.show{{display:block}}

/* FOOTER */
footer{{background:var(--ink);color:rgba(255,255,255,.4);text-align:center;padding:24px;font-size:.75rem}}

@media(max-width:768px){{
  .hero{{grid-template-columns:1fr;padding:100px 24px 60px;gap:40px}}
  .hero-img{{order:-1}}
  .hero-img img{{height:300px}}
  nav,.logos,.pain-section,.proof-section,.faq-section,.compare-section,.cta-section{{padding-left:24px;padding-right:24px}}
  .feat-section{{padding:60px 24px}}
  .metrics-row{{grid-template-columns:1fr 1fr}}
}}
</style>
</head>
<body>

<nav>
  <div class="nav-logo">{keyword[:20]}</div>
  <button class="nav-cta" onclick="document.querySelector('.cta-section').scrollIntoView({{behavior:'smooth'}})">{h['cta']}</button>
</nav>

<!-- HERO -->
<section style="background:var(--white)">
<div class="hero">
  <div class="hero-text">
    <h1>{h['headline']}</h1>
    <p>{h['subheadline']}</p>
    <div class="hero-btns">
      <button class="btn-primary">{h['cta']}</button>
      <button class="btn-sec">See how it works →</button>
    </div>
    <div class="trust">
      <div class="trust-avatars">
        <img src="{img(28,28,'av1')}" alt="student"/>
        <img src="{img(28,28,'av2')}" alt="student"/>
        <img src="{img(28,28,'av3')}" alt="student"/>
      </div>
      {h['trust_line']}
    </div>
  </div>
  <div class="hero-img">
    <img src="{img(600,520,'study-hero')}" alt="Study"/>
    <div class="hero-img-badge">
      <div class="badge-icon">🏆</div>
      <div class="badge-text"><strong>98% Success Rate</strong><span>Verified Results</span></div>
    </div>
  </div>
</div>
</section>

<!-- LOGOS -->
<div class="logos">
  <div class="logo-item">Times of India</div>
  <div class="logo-item">Education World</div>
  <div class="logo-item">India Today</div>
  <div class="logo-item">NDTV Education</div>
  <div class="logo-item">The Hindu</div>
</div>

<!-- PAIN -->
<section class="pain-section">
  <div class="sec-label">The Problem</div>
  <div class="sec-title">{pp['headline']}</div>
  <div class="pain-grid">{pain_cards}</div>
</section>

<!-- FEATURES -->
<section class="feat-section">
  <div class="feat-inner">
    <div class="sec-label">Our Solution</div>
    <div class="sec-title">{ft['headline']}</div>
    <p class="feat-sub">Everything you need to succeed, in one place.</p>
    <img class="feat-img" src="{img(1200,300,'learning-success')}" alt="Learning"/>
    <div class="feat-grid">{feat_items}</div>
  </div>
</section>

<!-- PROOF -->
<section class="proof-section">
  <div class="sec-label">Results</div>
  <div class="sec-title">{sp['headline']}</div>
  <div class="metrics-row">{metrics}</div>
  <div class="testi-grid">{testis}</div>
</section>

<!-- COMPARE -->
<section class="compare-section">
  <div class="compare-inner">
    <div class="sec-label" style="margin-bottom:10px">Comparison</div>
    <div class="sec-title" style="margin-bottom:32px">{cp['headline']}</div>
    <table class="compare-table">
      <thead><tr><th>Feature</th><th>Traditional Way</th><th>With Us</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</section>

<!-- CTA -->
<section class="cta-section">
  <h2>{cf['headline']}</h2>
  <p>{cf['subtext']}</p>
  <button class="btn-primary" style="font-size:1rem;padding:16px 40px">{cf['cta']}</button>
  <div class="urgency">⚡ <span>{cf['urgency']}</span></div>
</section>

<!-- FAQ -->
<section class="faq-section">
  <h2>Frequently Asked Questions</h2>
  {faqs}
</section>

<footer>© 2025 · {keyword} · All rights reserved · Built with MarketAI</footer>

<script>
function toggle(btn){{
  btn.classList.toggle('open');
  btn.nextElementSibling.classList.toggle('show');
}}
</script>
</body>
</html>"""


def build_tech_html(keyword: str, data: dict) -> str:
    h = data["hero"]
    pp = data["pain_points"]
    ft = data["features"]
    sp = data["social_proof"]
    cp = data["comparison"]
    cf = data["cta_faq"]

    pain_cards = "".join([f'<div class="pain-card"><div class="pi">{c["icon"]}</div><h3>{c["title"]}</h3><p>{c["desc"]}</p></div>' for c in pp["cards"]])
    feat_items = "".join([f'<div class="feat-item"><span>{f["icon"]}</span><div><h3>{f["title"]}</h3><p>{f["desc"]}</p></div></div>' for f in ft["items"]])
    metrics = "".join([f'<div class="metric"><div class="mn">{m["number"]}</div><div class="ml">{m["label"]}</div></div>' for m in sp["metrics"]])
    testis = "".join([f'<div class="testi"><div class="ts">★★★★★</div><p>"{t["quote"]}"</p><div class="ta"><img src="{img(40,40,SEEDS["avatar"][i])}" alt="{t["name"]}"/><div><strong>{t["name"]}</strong><span>{t["role"]}</span></div></div></div>' for i,t in enumerate(sp["testimonials"])])
    rows = "".join([f"<tr><td>{r['feature']}</td><td class='bad'>✗ {r['old']}</td><td class='good'>✓ {r['new']}</td></tr>" for r in cp["rows"]])
    faqs = "".join([f'<div class="faq"><button onclick="toggle(this)">{f["q"]}<span>▾</span></button><div class="ans"><p>{f["a"]}</p></div></div>' for f in cf["faqs"]])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{h['headline']}</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#050810;--s1:#080d1a;--s2:#0c1220;--border:#1a2540;--a:#00d4ff;--g:#00ff88;--text:#e8f0f7;--muted:#4a6080}}
body{{background:var(--bg);color:var(--text);font-family:'Space Grotesk',sans-serif;line-height:1.6;overflow-x:hidden}}
body::before{{content:'';position:fixed;inset:0;background-image:radial-gradient(ellipse 80% 50% at 50% -20%,rgba(0,212,255,.08),transparent);pointer-events:none;z-index:0}}

nav{{position:fixed;top:0;left:0;right:0;z-index:100;padding:14px 48px;display:flex;align-items:center;justify-content:space-between;background:rgba(5,8,16,.85);backdrop-filter:blur(12px);border-bottom:1px solid var(--border)}}
.nav-logo{{font-family:'JetBrains Mono',monospace;font-size:1rem;color:var(--a)}}
.nav-cta{{background:var(--a);color:#000;padding:8px 20px;border:none;border-radius:4px;font-weight:700;font-size:.8rem;cursor:pointer;font-family:'Space Grotesk',sans-serif;transition:all .2s}}
.nav-cta:hover{{box-shadow:0 0 20px rgba(0,212,255,.4)}}

.hero{{min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:120px 48px 80px;position:relative}}
.hero-grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(0,212,255,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(0,212,255,.025) 1px,transparent 1px);background-size:48px 48px}}
.hero-img-wrap{{position:absolute;inset:0;overflow:hidden}}
.hero-img-wrap img{{width:100%;height:100%;object-fit:cover;opacity:.08;filter:saturate(0)}}
.hero-content{{position:relative;z-index:2;max-width:800px}}
.hero-tag{{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:.68rem;color:var(--a);border:1px solid rgba(0,212,255,.3);padding:5px 16px;border-radius:2px;margin-bottom:24px;letter-spacing:.1em;background:rgba(0,212,255,.05)}}
.hero h1{{font-size:clamp(2.2rem,5vw,4rem);font-weight:700;line-height:1.05;letter-spacing:-.03em;margin-bottom:18px}}
.hero h1 em{{font-style:normal;color:var(--a)}}
.hero p{{color:var(--muted);font-size:1rem;margin-bottom:36px;max-width:520px;margin-left:auto;margin-right:auto}}
.hero-btns{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}}
.btn-main{{background:var(--a);color:#000;padding:14px 32px;border:none;border-radius:4px;font-weight:700;font-size:.9rem;cursor:pointer;font-family:'Space Grotesk',sans-serif;transition:all .2s}}
.btn-main:hover{{box-shadow:0 0 30px rgba(0,212,255,.4);transform:translateY(-2px)}}
.btn-ghost{{background:transparent;color:var(--text);padding:14px 32px;border:1px solid var(--border);border-radius:4px;font-weight:500;font-size:.9rem;cursor:pointer;font-family:'Space Grotesk',sans-serif;transition:all .2s}}
.btn-ghost:hover{{border-color:var(--a);color:var(--a)}}
.trust{{margin-top:20px;font-size:.75rem;color:var(--muted);display:flex;align-items:center;justify-content:center;gap:8px}}
.trust-dot{{width:5px;height:5px;border-radius:50%;background:var(--g);animation:blink 2s infinite}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}

section{{padding:80px 48px;position:relative}}
.inner{{max-width:1100px;margin:0 auto}}
.tag{{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:var(--a);letter-spacing:.12em;text-transform:uppercase;margin-bottom:10px}}
.stitle{{font-size:clamp(1.6rem,3vw,2.4rem);font-weight:700;margin-bottom:32px;letter-spacing:-.02em}}

.pain-section{{background:var(--s1)}}
.pain-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}}
.pain-card{{background:var(--s2);border:1px solid var(--border);border-radius:8px;padding:24px;transition:all .2s}}
.pain-card:hover{{border-color:rgba(0,212,255,.3);box-shadow:0 0 20px rgba(0,212,255,.06);transform:translateY(-2px)}}
.pi{{font-size:2rem;margin-bottom:12px}}
.pain-card h3{{font-size:.9rem;font-weight:700;margin-bottom:6px;color:var(--a)}}
.pain-card p{{font-size:.78rem;color:var(--muted);line-height:1.6}}

.feat-section{{background:var(--bg)}}
.feat-img{{width:100%;height:260px;object-fit:cover;border-radius:10px;margin-bottom:36px;border:1px solid var(--border);display:block;filter:brightness(.8) saturate(.7)}}
.feat-list{{display:flex;flex-direction:column;gap:12px}}
.feat-item{{background:var(--s1);border:1px solid var(--border);border-radius:8px;padding:18px 22px;display:flex;gap:14px;align-items:flex-start;transition:all .2s}}
.feat-item:hover{{border-color:var(--g);box-shadow:0 0 16px rgba(0,255,136,.06)}}
.feat-item span{{font-size:1.4rem;flex-shrink:0;margin-top:2px}}
.feat-item h3{{font-size:.88rem;font-weight:700;color:var(--g);margin-bottom:3px}}
.feat-item p{{font-size:.78rem;color:var(--muted)}}

.proof-section{{background:var(--s1)}}
.metrics-row{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:40px}}
.metric{{background:var(--s2);border:1px solid var(--border);border-radius:8px;padding:20px;text-align:center}}
.mn{{font-size:2rem;font-weight:700;color:var(--a);margin-bottom:4px}}
.ml{{font-size:.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}}
.testi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}}
.testi{{background:var(--s2);border:1px solid var(--border);border-radius:8px;padding:22px}}
.ts{{color:#f59e0b;font-size:.8rem;margin-bottom:8px}}
.testi p{{font-size:.82rem;color:var(--muted);font-style:italic;margin-bottom:14px;line-height:1.7}}
.ta{{display:flex;align-items:center;gap:10px}}
.ta img{{width:36px;height:36px;border-radius:50%;object-fit:cover;border:2px solid var(--border)}}
.ta strong{{font-size:.8rem;display:block;color:var(--text)}}
.ta span{{font-size:.7rem;color:var(--muted)}}

.compare-section{{background:var(--bg)}}
.ctable{{width:100%;border-collapse:collapse;border-radius:10px;overflow:hidden}}
.ctable thead{{background:var(--s2);border:1px solid var(--border)}}
.ctable th{{padding:14px 20px;text-align:left;font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;color:var(--a);font-family:'JetBrains Mono',monospace}}
.ctable td{{padding:12px 20px;font-size:.82rem;border-bottom:1px solid var(--border);background:var(--s1)}}
.ctable td:first-child{{color:var(--text);font-weight:600}}
td.bad{{color:#ef4444}}td.good{{color:var(--g);font-weight:600}}

.cta-section{{background:linear-gradient(135deg,var(--s2),var(--s1));text-align:center;border-top:1px solid var(--border)}}
.cta-section h2{{font-size:clamp(1.8rem,4vw,3rem);font-weight:700;margin-bottom:12px;letter-spacing:-.02em}}
.cta-section p{{color:var(--muted);margin-bottom:28px;max-width:480px;margin-left:auto;margin-right:auto}}
.urgency{{margin-top:14px;font-size:.75rem;color:var(--muted)}}
.urgency em{{color:var(--a);font-style:normal;font-weight:600}}

.faq-section{{background:var(--bg);max-width:700px!important}}
.faq-section h2{{font-size:1.6rem;font-weight:700;margin-bottom:24px;text-align:center}}
.faq{{border-bottom:1px solid var(--border)}}
.faq button{{width:100%;padding:14px 0;background:none;border:none;color:var(--text);text-align:left;font-size:.86rem;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;font-family:'Space Grotesk',sans-serif;gap:12px}}
.faq button span{{color:var(--a);font-size:.9rem;transition:transform .2s;flex-shrink:0}}
.faq button.open span{{transform:rotate(180deg)}}
.ans{{display:none;padding:0 0 14px;font-size:.82rem;color:var(--muted);line-height:1.7}}
.ans.show{{display:block}}

footer{{background:var(--s1);border-top:1px solid var(--border);text-align:center;padding:20px;font-size:.72rem;color:var(--muted)}}
@media(max-width:768px){{nav,section{{padding-left:20px;padding-right:20px}}.metrics-row{{grid-template-columns:1fr 1fr}}.hero{{padding:100px 20px 60px}}}}
</style>
</head>
<body>
<nav><div class="nav-logo">// {keyword[:16]}</div><button class="nav-cta">{h['cta']}</button></nav>
<section class="hero">
  <div class="hero-grid"></div>
  <div class="hero-img-wrap"><img src="{img(1400,900,'tech-dark')}" alt=""/></div>
  <div class="hero-content">
    <div class="hero-tag">// {keyword}</div>
    <h1>{h['headline'].replace(keyword.split()[0], f'<em>{keyword.split()[0]}</em>', 1)}</h1>
    <p>{h['subheadline']}</p>
    <div class="hero-btns">
      <button class="btn-main">{h['cta']}</button>
      <button class="btn-ghost">See Demo →</button>
    </div>
    <div class="trust"><div class="trust-dot"></div>{h['trust_line']}</div>
  </div>
</section>
<section class="pain-section"><div class="inner"><div class="tag">// The Problem</div><div class="stitle">{pp['headline']}</div><div class="pain-grid">{pain_cards}</div></div></section>
<section class="feat-section"><div class="inner"><div class="tag">// Our Solution</div><div class="stitle">{ft['headline']}</div><img class="feat-img" src="{img(1100,260,'technology-learning')}" alt=""/><div class="feat-list">{feat_items}</div></div></section>
<section class="proof-section"><div class="inner"><div class="tag">// Results</div><div class="stitle">{sp['headline']}</div><div class="metrics-row">{metrics}</div><div class="testi-grid">{testis}</div></div></section>
<section class="compare-section"><div class="inner"><div class="tag">// Comparison</div><div class="stitle">{cp['headline']}</div><table class="ctable"><thead><tr><th>Feature</th><th>Old Way</th><th>With Us</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section class="cta-section"><div class="inner"><h2>{cf['headline']}</h2><p>{cf['subtext']}</p><button class="btn-main" style="font-size:.95rem;padding:14px 36px">{cf['cta']}</button><div class="urgency">⚡ <em>{cf['urgency']}</em></div></div></section>
<section class="faq-section"><div class="inner" style="max-width:700px"><h2>FAQ</h2>{faqs}</div></section>
<footer>© 2025 · {keyword} · Built with MarketAI</footer>
<script>function toggle(b){{b.classList.toggle('open');b.nextElementSibling.classList.toggle('show')}}</script>
</body></html>"""


def build_academic_html(keyword: str, data: dict) -> str:
    h = data["hero"]
    pp = data["pain_points"]
    ft = data["features"]
    sp = data["social_proof"]
    cp = data["comparison"]
    cf = data["cta_faq"]

    pain_cards = "".join([f'<div class="pain-card"><div class="pi">{c["icon"]}</div><h3>{c["title"]}</h3><p>{c["desc"]}</p></div>' for c in pp["cards"]])
    feat_items = "".join([f'<div class="feat-item"><div class="fi">{f["icon"]}</div><div><h3>{f["title"]}</h3><p>{f["desc"]}</p></div></div>' for f in ft["items"]])
    metrics = "".join([f'<div class="metric"><div class="mn">{m["number"]}</div><div class="ml">{m["label"]}</div></div>' for m in sp["metrics"]])
    testis = "".join([f'<div class="testi"><p>"{t["quote"]}"</p><div class="ta"><img src="{img(44,44,SEEDS["avatar"][i])}" alt="{t["name"]}"/><div><strong>{t["name"]}</strong><span>{t["role"]}</span></div></div></div>' for i,t in enumerate(sp["testimonials"])])
    rows = "".join([f"<tr><td class='f'>{r['feature']}</td><td class='o'>✗ {r['old']}</td><td class='n'>✓ {r['new']}</td></tr>" for r in cp["rows"]])
    faqs = "".join([f'<div class="faq"><button onclick="toggle(this)">{f["q"]}<span>+</span></button><div class="ans"><p>{f["a"]}</p></div></div>' for f in cf["faqs"]])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{h['headline']}</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,600&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--navy:#1a2744;--navy2:#243058;--gold:#b8962e;--gold2:#d4af5a;--cream:#faf8f3;--white:#ffffff;--text:#1a2744;--muted:#6b7a99;--line:#dde3f0}}
body{{font-family:'Outfit',sans-serif;background:var(--cream);color:var(--text);line-height:1.7}}

nav{{position:fixed;top:0;left:0;right:0;z-index:100;background:var(--navy);padding:14px 60px;display:flex;align-items:center;justify-content:space-between}}
.nav-logo{{font-family:'Cormorant Garamond',serif;font-size:1.2rem;font-weight:600;color:#fff;letter-spacing:.05em}}
.nav-badge{{font-size:.62rem;color:var(--gold2);letter-spacing:.12em;text-transform:uppercase}}
.nav-cta{{background:var(--gold);color:var(--navy);padding:9px 22px;border:none;font-weight:600;font-size:.8rem;cursor:pointer;font-family:'Outfit',sans-serif;transition:all .2s;letter-spacing:.03em}}
.nav-cta:hover{{background:var(--gold2);transform:translateY(-1px)}}

.hero{{min-height:100vh;display:grid;grid-template-columns:1.1fr 0.9fr;align-items:center;padding:120px 60px 80px}}
.hero-left{{padding-right:60px}}
.overline{{font-size:.65rem;text-transform:uppercase;letter-spacing:.2em;color:var(--gold);font-weight:600;margin-bottom:14px;display:block}}
.hero h1{{font-family:'Cormorant Garamond',serif;font-size:clamp(2.4rem,4.5vw,4rem);font-weight:700;line-height:1.08;margin-bottom:18px;color:var(--navy)}}
.hero p{{font-size:.95rem;color:var(--muted);margin-bottom:32px;max-width:440px;line-height:1.8}}
.btn-gold{{background:var(--gold);color:var(--navy);padding:14px 32px;border:none;font-weight:600;font-size:.88rem;cursor:pointer;font-family:'Outfit',sans-serif;transition:all .2s;letter-spacing:.03em}}
.btn-gold:hover{{background:var(--gold2);box-shadow:0 8px 24px rgba(184,150,46,.3);transform:translateY(-2px)}}
.trust{{margin-top:18px;font-size:.76rem;color:var(--muted);display:flex;align-items:center;gap:8px}}
.trust-imgs{{display:flex}}
.trust-imgs img{{width:26px;height:26px;border-radius:50%;border:2px solid var(--cream);margin-right:-7px;object-fit:cover}}
.hero-right{{position:relative}}
.hero-right img{{width:100%;height:500px;object-fit:cover;display:block}}
.hero-accent{{position:absolute;top:-16px;right:-16px;width:80%;height:80%;border:2px solid var(--gold);z-index:-1;opacity:.4}}
.hero-stat{{position:absolute;bottom:-20px;left:-20px;background:var(--white);padding:16px 20px;box-shadow:0 8px 32px rgba(26,39,68,.12)}}
.hero-stat strong{{display:block;font-family:'Cormorant Garamond',serif;font-size:1.8rem;font-weight:700;color:var(--navy)}}
.hero-stat span{{font-size:.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}}

.divider{{height:4px;background:linear-gradient(90deg,var(--navy),var(--gold),var(--navy))}}

section{{padding:88px 60px}}
.sec-over{{font-size:.62rem;text-transform:uppercase;letter-spacing:.18em;color:var(--gold);margin-bottom:10px;display:block}}
.sec-title{{font-family:'Cormorant Garamond',serif;font-size:clamp(1.8rem,3vw,2.8rem);font-weight:700;color:var(--navy);margin-bottom:36px;line-height:1.15}}

.pain-section{{background:var(--navy)}}
.pain-section .sec-title{{color:#fff}}
.pain-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;max-width:1100px;margin:0 auto}}
.pain-card{{background:rgba(255,255,255,.06);border-top:3px solid var(--gold);padding:24px;transition:all .2s}}
.pain-card:hover{{background:rgba(255,255,255,.1);transform:translateY(-3px)}}
.pi{{font-size:2rem;margin-bottom:10px}}
.pain-card h3{{font-size:.9rem;font-weight:600;margin-bottom:7px;color:var(--gold2)}}
.pain-card p{{font-size:.8rem;color:rgba(255,255,255,.5);line-height:1.6}}

.feat-section{{background:var(--cream);max-width:1200px;margin:0 auto}}
.feat-img{{width:100%;height:280px;object-fit:cover;margin-bottom:40px;display:block}}
.feat-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}}
.feat-item{{background:var(--white);border-left:3px solid var(--gold);padding:22px;display:flex;gap:14px;box-shadow:0 2px 12px rgba(26,39,68,.04)}}
.fi{{font-size:1.4rem;flex-shrink:0;margin-top:3px}}
.feat-item h3{{font-size:.88rem;font-weight:600;margin-bottom:5px;color:var(--navy)}}
.feat-item p{{font-size:.8rem;color:var(--muted);line-height:1.6}}

.proof-section{{background:var(--navy);color:#fff}}
.proof-section .sec-title{{color:#fff}}
.metrics-row{{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.1);margin-bottom:44px}}
.metric{{background:var(--navy);padding:24px;text-align:center}}
.mn{{font-family:'Cormorant Garamond',serif;font-size:2.4rem;font-weight:700;color:var(--gold2)}}
.ml{{font-size:.65rem;color:rgba(255,255,255,.4);text-transform:uppercase;letter-spacing:.1em;margin-top:4px}}
.testi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}}
.testi{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);padding:24px}}
.testi p{{font-size:.85rem;color:rgba(255,255,255,.7);font-style:italic;margin-bottom:16px;line-height:1.7}}
.ta{{display:flex;align-items:center;gap:10px}}
.ta img{{width:40px;height:40px;border-radius:50%;object-fit:cover;border:2px solid var(--gold)}}
.ta strong{{font-size:.82rem;color:#fff;display:block}}
.ta span{{font-size:.72rem;color:rgba(255,255,255,.4)}}

.compare-section{{background:var(--cream)}}
.ctable{{width:100%;max-width:860px;margin:0 auto;border-collapse:collapse}}
.ctable thead{{background:var(--navy)}}
.ctable th{{padding:14px 22px;text-align:left;font-size:.72rem;color:var(--gold2);text-transform:uppercase;letter-spacing:.1em;font-family:'Outfit',sans-serif}}
.ctable td{{padding:13px 22px;font-size:.84rem;border-bottom:1px solid var(--line);background:var(--white)}}
td.f{{font-weight:600;color:var(--navy)}}
td.o{{color:#c0392b}}
td.n{{color:#1a7a4a;font-weight:600}}

.cta-section{{background:var(--navy);text-align:center;color:#fff;position:relative;overflow:hidden}}
.cta-section::before{{content:'';position:absolute;inset:0;background:url('{img(1400,400,"ceremony-graduation")}') center/cover;opacity:.08}}
.cta-inner{{position:relative;z-index:1}}
.cta-section h2{{font-family:'Cormorant Garamond',serif;font-size:clamp(2rem,4vw,3.2rem);font-weight:700;margin-bottom:12px}}
.cta-section p{{color:rgba(255,255,255,.65);margin-bottom:28px;max-width:480px;margin-left:auto;margin-right:auto}}
.urgency{{margin-top:14px;font-size:.75rem;color:rgba(255,255,255,.4)}}
.urgency em{{color:var(--gold2);font-style:normal}}

.faq-section{{background:var(--cream);max-width:720px;margin:0 auto}}
.faq-section h2{{font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:700;text-align:center;color:var(--navy);margin-bottom:28px}}
.faq{{border-bottom:1px solid var(--line)}}
.faq button{{width:100%;padding:16px 0;background:none;border:none;text-align:left;font-size:.9rem;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;color:var(--navy);font-family:'Outfit',sans-serif;gap:12px}}
.faq button span{{color:var(--gold);font-size:1.1rem;transition:transform .2s;flex-shrink:0}}
.faq button.open span{{transform:rotate(45deg)}}
.ans{{display:none;padding:0 0 14px;font-size:.84rem;color:var(--muted);line-height:1.7}}
.ans.show{{display:block}}

footer{{background:var(--navy);color:rgba(255,255,255,.3);text-align:center;padding:22px;font-size:.72rem;border-top:2px solid var(--gold)}}

@media(max-width:768px){{
  .hero{{grid-template-columns:1fr;padding:100px 24px 60px}}
  .hero-left{{padding-right:0;margin-bottom:32px}}
  .hero-accent{{display:none}}
  nav,section{{padding-left:24px;padding-right:24px}}
  .metrics-row{{grid-template-columns:1fr 1fr}}
}}
</style>
</head>
<body>
<nav>
  <div>
    <div class="nav-logo">{keyword[:22]}</div>
    <div class="nav-badge">Excellence in Education</div>
  </div>
  <button class="nav-cta">{h['cta']}</button>
</nav>

<section class="hero" style="padding-top:100px">
  <div class="hero-left">
    <span class="overline">{keyword}</span>
    <h1>{h['headline']}</h1>
    <p>{h['subheadline']}</p>
    <button class="btn-gold">{h['cta']}</button>
    <div class="trust">
      <div class="trust-imgs">
        <img src="{img(26,26,'av1')}" alt=""/><img src="{img(26,26,'av2')}" alt=""/><img src="{img(26,26,'av3')}" alt=""/>
      </div>
      {h['trust_line']}
    </div>
  </div>
  <div class="hero-right">
    <div class="hero-accent"></div>
    <img src="{img(560,500,'university-library')}" alt="Education"/>
    <div class="hero-stat"><strong>98%</strong><span>Success Rate</span></div>
  </div>
</section>

<div class="divider"></div>

<section class="pain-section">
  <div style="max-width:1100px;margin:0 auto">
    <span class="sec-over" style="color:var(--gold)">The Challenge</span>
    <div class="sec-title" style="color:#fff">{pp['headline']}</div>
    <div class="pain-grid">{pain_cards}</div>
  </div>
</section>

<section style="padding:88px 60px;background:var(--cream)">
  <div style="max-width:1100px;margin:0 auto">
    <span class="sec-over">Our Approach</span>
    <div class="sec-title">{ft['headline']}</div>
    <img class="feat-img" src="{img(1100,280,'classroom-students')}" alt="Learning"/>
    <div class="feat-grid">{feat_items}</div>
  </div>
</section>

<section class="proof-section">
  <div style="max-width:1100px;margin:0 auto">
    <span class="sec-over" style="color:var(--gold)">Proven Results</span>
    <div class="sec-title">{sp['headline']}</div>
    <div class="metrics-row">{metrics}</div>
    <div class="testi-grid">{testis}</div>
  </div>
</section>

<section class="compare-section">
  <div style="max-width:900px;margin:0 auto">
    <span class="sec-over">Comparison</span>
    <div class="sec-title">{cp['headline']}</div>
    <table class="ctable">
      <thead><tr><th>Feature</th><th>Traditional Method</th><th>Our Approach</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</section>

<section class="cta-section">
  <div class="cta-inner">
    <h2>{cf['headline']}</h2>
    <p>{cf['subtext']}</p>
    <button class="btn-gold" style="font-size:.95rem;padding:15px 40px">{cf['cta']}</button>
    <div class="urgency">⚡ <em>{cf['urgency']}</em></div>
  </div>
</section>

<section class="faq-section">
  <h2>Frequently Asked Questions</h2>
  {faqs}
</section>

<footer>© 2025 · {keyword} · All rights reserved · Built with MarketAI</footer>
<script>function toggle(b){{b.classList.toggle('open');b.nextElementSibling.classList.toggle('show')}}</script>
</body>
</html>"""
