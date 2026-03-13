from seo_agent import call_groq

UNSPLASH_TOPICS = {
    "student": "studying,education,student,learning,books",
    "professional": "business,office,professional,work,corporate",
    "parent": "family,parenting,children,education,home",
    "business owner": "entrepreneur,startup,business,success,office"
}

def unsplash_url(query: str, w: int = 1200, h: int = 600) -> str:
    q = query.replace(" ", ",")
    return f"https://source.unsplash.com/{w}x{h}/?{q}"

def unsplash_small(query: str, w: int = 600, h: int = 400) -> str:
    q = query.replace(" ", ",")
    return f"https://source.unsplash.com/{w}x{h}/?{q}"

async def generate_lp_content(keyword: str, style: str, persona: str = "student") -> dict:
    """Generate all text content for landing page"""
    prompt = f"""You are a conversion copywriter. Generate landing page content for:
Keyword: "{keyword}"
Style: {style.upper()}
Persona: {persona.upper()}

Return ONLY this exact JSON structure (no markdown, no extra text):
{{
  "hero": {{
    "headline": "Short powerful headline max 8 words addressing pain point",
    "subheadline": "Solution-focused subheadline max 20 words",
    "cta": "CTA button text",
    "trust_line": "Trust line like Join 10000+ students",
    "image_query": "2-3 word Unsplash image query e.g. student studying"
  }},
  "pain_points": {{
    "headline": "Section headline",
    "cards": [
      {{"icon": "😓", "title": "Pain title", "desc": "15 word description of this student struggle"}},
      {{"icon": "😰", "title": "Pain title", "desc": "15 word description"}},
      {{"icon": "😤", "title": "Pain title", "desc": "15 word description"}},
      {{"icon": "😩", "title": "Pain title", "desc": "15 word description"}}
    ]
  }},
  "features": {{
    "headline": "Features section headline",
    "items": [
      {{"icon": "✅", "title": "Feature title", "desc": "20 word benefit description"}},
      {{"icon": "🚀", "title": "Feature title", "desc": "20 word benefit description"}},
      {{"icon": "💡", "title": "Feature title", "desc": "20 word benefit description"}},
      {{"icon": "🎯", "title": "Feature title", "desc": "20 word benefit description"}},
      {{"icon": "📊", "title": "Feature title", "desc": "20 word benefit description"}},
      {{"icon": "🏆", "title": "Feature title", "desc": "20 word benefit description"}}
    ]
  }},
  "social_proof": {{
    "headline": "Social proof headline",
    "metrics": [
      {{"number": "10,000+", "label": "Students helped"}},
      {{"number": "98%", "label": "Success rate"}},
      {{"number": "4.9★", "label": "Average rating"}}
    ],
    "testimonials": [
      {{"name": "Student name", "role": "Grade/Role", "quote": "30 word genuine testimonial", "avatar_query": "student portrait"}},
      {{"name": "Student name", "role": "Grade/Role", "quote": "30 word genuine testimonial", "avatar_query": "student smiling"}},
      {{"name": "Student name", "role": "Grade/Role", "quote": "30 word genuine testimonial", "avatar_query": "young person"}}
    ]
  }},
  "comparison": {{
    "headline": "Why we're better headline",
    "rows": [
      {{"feature": "Feature name", "old": "Old way", "new": "Our way"}},
      {{"feature": "Feature name", "old": "Old way", "new": "Our way"}},
      {{"feature": "Feature name", "old": "Old way", "new": "Our way"}},
      {{"feature": "Feature name", "old": "Old way", "new": "Our way"}},
      {{"feature": "Feature name", "old": "Old way", "new": "Our way"}},
      {{"feature": "Feature name", "old": "Old way", "new": "Our way"}},
      {{"feature": "Feature name", "old": "Old way", "new": "Our way"}},
      {{"feature": "Feature name", "old": "Old way", "new": "Our way"}}
    ]
  }},
  "cta_faq": {{
    "headline": "Closing headline",
    "subtext": "20 word closing subtext",
    "cta": "Final CTA button",
    "urgency": "Scarcity line e.g. Only 12 spots left this month",
    "faqs": [
      {{"q": "Real objection question", "a": "Reassuring 30 word answer"}},
      {{"q": "Real objection question", "a": "Reassuring 30 word answer"}},
      {{"q": "Real objection question", "a": "Reassuring 30 word answer"}},
      {{"q": "Real objection question", "a": "Reassuring 30 word answer"}},
      {{"q": "Real objection question", "a": "Reassuring 30 word answer"}}
    ]
  }}
}}"""

    raw = await call_groq(prompt, 2000)
    import json, re
    try:
        # Strip any markdown fences
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

    hero_img = unsplash_url(h.get("image_query", "education student"), 1400, 700)
    pain_imgs = [unsplash_small(c.get("title","student"), 400, 300) for c in pp["cards"]]
    feature_img = unsplash_url("learning success education", 1200, 500)

    pain_cards = ""
    for i, c in enumerate(pp["cards"]):
        pain_cards += f"""
        <div class="pain-card">
          <img src="{pain_imgs[i]}" alt="{c['title']}" loading="lazy"/>
          <div class="pain-content">
            <div class="pain-icon">{c['icon']}</div>
            <h3>{c['title']}</h3>
            <p>{c['desc']}</p>
          </div>
        </div>"""

    feature_items = ""
    for f in ft["items"]:
        feature_items += f"""
        <div class="feature-item">
          <div class="f-icon">{f['icon']}</div>
          <h3>{f['title']}</h3>
          <p>{f['desc']}</p>
        </div>"""

    metrics = ""
    for m in sp["metrics"]:
        metrics += f'<div class="metric"><div class="m-num">{m["number"]}</div><div class="m-lbl">{m["label"]}</div></div>'

    testimonials = ""
    for t in sp["testimonials"]:
        av = unsplash_small(t.get("avatar_query","person portrait"), 80, 80)
        testimonials += f"""
        <div class="testi">
          <p>"{t['quote']}"</p>
          <div class="testi-author">
            <img src="{av}" alt="{t['name']}"/>
            <div><strong>{t['name']}</strong><span>{t['role']}</span></div>
          </div>
        </div>"""

    comp_rows = ""
    for r in cp["rows"]:
        comp_rows += f"""
        <tr>
          <td class="feat-col">{r['feature']}</td>
          <td class="old-col">❌ {r['old']}</td>
          <td class="new-col">✅ {r['new']}</td>
        </tr>"""

    faqs = ""
    for f in cf["faqs"]:
        faqs += f"""
        <div class="faq-item">
          <button class="faq-q" onclick="this.classList.toggle('open');this.nextElementSibling.classList.toggle('show')">{f['q']} <span>+</span></button>
          <div class="faq-a"><p>{f['a']}</p></div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{h['headline']} | {keyword}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#1a1a1a;line-height:1.6}}
/* HERO */
.hero{{position:relative;min-height:90vh;display:flex;align-items:center;justify-content:center;text-align:center;overflow:hidden}}
.hero-bg{{position:absolute;inset:0;background:url('{hero_img}') center/cover no-repeat;filter:brightness(.35)}}
.hero-content{{position:relative;z-index:2;max-width:750px;padding:40px 24px;color:#fff}}
.hero-tag{{display:inline-block;background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);padding:6px 18px;border-radius:20px;font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;margin-bottom:20px;backdrop-filter:blur(8px)}}
.hero h1{{font-size:clamp(2rem,5vw,3.5rem);font-weight:800;line-height:1.1;margin-bottom:18px;letter-spacing:-.02em}}
.hero p{{font-size:1.1rem;opacity:.9;margin-bottom:30px;max-width:560px;margin-left:auto;margin-right:auto}}
.hero-cta{{display:inline-block;background:#fff;color:#1a1a1a;padding:16px 36px;border-radius:50px;font-weight:700;font-size:1rem;text-decoration:none;transition:all .2s;cursor:pointer;border:none}}
.hero-cta:hover{{transform:translateY(-2px);box-shadow:0 12px 30px rgba(0,0,0,.3)}}
.trust{{margin-top:18px;font-size:.8rem;opacity:.7}}
/* PAIN */
.pain-section{{padding:80px 24px;background:#f8f9fa}}
.section-center{{text-align:center;margin-bottom:40px}}
.section-center h2{{font-size:clamp(1.5rem,3vw,2.2rem);font-weight:700;margin-bottom:10px}}
.section-center p{{color:#666;max-width:500px;margin:0 auto}}
.pain-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:24px;max-width:1100px;margin:0 auto}}
.pain-card{{background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.06);transition:all .2s}}
.pain-card:hover{{transform:translateY(-4px);box-shadow:0 12px 30px rgba(0,0,0,.1)}}
.pain-card img{{width:100%;height:180px;object-fit:cover}}
.pain-content{{padding:20px}}
.pain-icon{{font-size:1.8rem;margin-bottom:8px}}
.pain-content h3{{font-size:1rem;font-weight:700;margin-bottom:6px}}
.pain-content p{{font-size:.85rem;color:#666}}
/* FEATURES */
.features-section{{padding:80px 24px;background:#fff}}
.features-hero-img{{width:100%;max-width:1000px;height:320px;object-fit:cover;border-radius:20px;margin:0 auto 50px;display:block;box-shadow:0 20px 60px rgba(0,0,0,.1)}}
.features-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:28px;max-width:1100px;margin:0 auto}}
.feature-item{{padding:28px;border:1px solid #eee;border-radius:16px;transition:all .2s}}
.feature-item:hover{{border-color:#6366f1;box-shadow:0 8px 25px rgba(99,102,241,.1)}}
.f-icon{{font-size:2rem;margin-bottom:12px}}
.feature-item h3{{font-size:1rem;font-weight:700;margin-bottom:8px}}
.feature-item p{{font-size:.85rem;color:#666}}
/* SOCIAL PROOF */
.proof-section{{padding:80px 24px;background:#f8f9fa}}
.metrics-row{{display:flex;justify-content:center;gap:48px;flex-wrap:wrap;margin-bottom:50px}}
.metric{{text-align:center}}
.m-num{{font-size:2.5rem;font-weight:800;color:#6366f1}}
.m-lbl{{font-size:.8rem;color:#666;margin-top:4px}}
.testi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;max-width:1000px;margin:0 auto}}
.testi{{background:#fff;padding:28px;border-radius:16px;box-shadow:0 4px 20px rgba(0,0,0,.06)}}
.testi p{{font-size:.9rem;color:#444;font-style:italic;margin-bottom:18px;line-height:1.7}}
.testi-author{{display:flex;align-items:center;gap:12px}}
.testi-author img{{width:44px;height:44px;border-radius:50%;object-fit:cover}}
.testi-author strong{{display:block;font-size:.85rem;font-weight:700}}
.testi-author span{{font-size:.75rem;color:#888}}
/* COMPARISON */
.compare-section{{padding:80px 24px;background:#fff}}
.compare-table{{width:100%;max-width:800px;margin:0 auto;border-collapse:collapse;border-radius:16px;overflow:hidden;box-shadow:0 4px 30px rgba(0,0,0,.08)}}
.compare-table thead{{background:#1a1a1a;color:#fff}}
.compare-table th{{padding:16px 20px;text-align:left;font-size:.85rem;letter-spacing:.05em}}
.feat-col{{background:#f8f9fa;font-weight:600;font-size:.85rem;padding:14px 20px}}
.old-col{{background:#fff5f5;color:#dc2626;font-size:.85rem;padding:14px 20px}}
.new-col{{background:#f0fdf4;color:#16a34a;font-size:.85rem;padding:14px 20px;font-weight:600}}
.compare-table tr:not(:last-child) td{{border-bottom:1px solid #eee}}
/* CTA + FAQ */
.cta-section{{padding:80px 24px;background:linear-gradient(135deg,#6366f1,#8b5cf6);text-align:center;color:#fff}}
.cta-section h2{{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:800;margin-bottom:14px}}
.cta-section p{{opacity:.9;margin-bottom:28px;font-size:1rem;max-width:500px;margin-left:auto;margin-right:auto}}
.cta-btn-white{{display:inline-block;background:#fff;color:#6366f1;padding:16px 40px;border-radius:50px;font-weight:700;font-size:1rem;cursor:pointer;border:none;transition:all .2s}}
.cta-btn-white:hover{{transform:translateY(-2px);box-shadow:0 12px 30px rgba(0,0,0,.2)}}
.urgency{{margin-top:14px;font-size:.8rem;opacity:.75}}
.faq-section{{padding:60px 24px;background:#f8f9fa;max-width:700px;margin:0 auto}}
.faq-section h2{{text-align:center;font-size:1.6rem;font-weight:700;margin-bottom:30px}}
.faq-item{{background:#fff;border-radius:10px;margin-bottom:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.04)}}
.faq-q{{width:100%;padding:16px 20px;background:none;border:none;text-align:left;font-size:.9rem;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;align-items:center;font-family:inherit}}
.faq-q span{{font-size:1.2rem;transition:transform .2s}}
.faq-q.open span{{transform:rotate(45deg)}}
.faq-a{{display:none;padding:0 20px 16px;font-size:.85rem;color:#555;line-height:1.7}}
.faq-a.show{{display:block}}
/* FOOTER */
footer{{background:#1a1a1a;color:#888;text-align:center;padding:24px;font-size:.78rem}}
@media(max-width:600px){{.metrics-row{{gap:24px}}.hero h1{{font-size:1.8rem}}}}
</style>
</head>
<body>
<!-- HERO -->
<section class="hero">
  <div class="hero-bg"></div>
  <div class="hero-content">
    <div class="hero-tag">{keyword}</div>
    <h1>{h['headline']}</h1>
    <p>{h['subheadline']}</p>
    <button class="hero-cta">{h['cta']}</button>
    <div class="trust">{h['trust_line']}</div>
  </div>
</section>
<!-- PAIN POINTS -->
<section class="pain-section">
  <div class="section-center"><h2>{pp['headline']}</h2></div>
  <div class="pain-grid">{pain_cards}</div>
</section>
<!-- FEATURES -->
<section class="features-section">
  <div class="section-center"><h2>{ft['headline']}</h2></div>
  <img class="features-hero-img" src="{feature_img}" alt="features"/>
  <div class="features-grid">{feature_items}</div>
</section>
<!-- SOCIAL PROOF -->
<section class="proof-section">
  <div class="section-center"><h2>{sp['headline']}</h2></div>
  <div class="metrics-row">{metrics}</div>
  <div class="testi-grid">{testimonials}</div>
</section>
<!-- COMPARISON -->
<section class="compare-section">
  <div class="section-center"><h2>{cp['headline']}</h2></div>
  <table class="compare-table">
    <thead><tr><th>Feature</th><th>Old Way ❌</th><th>With Us ✅</th></tr></thead>
    <tbody>{comp_rows}</tbody>
  </table>
</section>
<!-- CTA -->
<section class="cta-section">
  <h2>{cf['headline']}</h2>
  <p>{cf['subtext']}</p>
  <button class="cta-btn-white">{cf['cta']}</button>
  <div class="urgency">⚡ {cf['urgency']}</div>
</section>
<!-- FAQ -->
<section class="faq-section">
  <h2>Frequently Asked Questions</h2>
  {faqs}
</section>
<footer>© 2025 · {keyword} · All rights reserved</footer>
<script>
// Smooth scroll for CTA buttons
document.querySelectorAll('.hero-cta,.cta-btn-white').forEach(b=>b.addEventListener('click',()=>{{
  document.querySelector('.faq-section').scrollIntoView({{behavior:'smooth'}});
}}));
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

    hero_img = unsplash_url(h.get("image_query","technology dark"), 1400, 700)

    pain_cards = ""
    for c in pp["cards"]:
        pain_cards += f"""<div class="pain-card"><div class="pain-icon">{c['icon']}</div><h3>{c['title']}</h3><p>{c['desc']}</p></div>"""

    feature_items = ""
    for f in ft["items"]:
        feature_items += f"""<div class="feature-item"><span class="fi">{f['icon']}</span><div><h3>{f['title']}</h3><p>{f['desc']}</p></div></div>"""

    metrics = ""
    for m in sp["metrics"]:
        metrics += f'<div class="metric"><div class="m-num">{m["number"]}</div><div class="m-lbl">{m["label"]}</div></div>'

    testimonials = ""
    for t in sp["testimonials"]:
        av = unsplash_small(t.get("avatar_query","person"), 60, 60)
        testimonials += f"""<div class="testi"><div class="testi-stars">★★★★★</div><p>"{t['quote']}"</p><div class="testi-author"><img src="{av}" alt="{t['name']}"/><div><strong>{t['name']}</strong><span>{t['role']}</span></div></div></div>"""

    comp_rows = ""
    for r in cp["rows"]:
        comp_rows += f"""<tr><td>{r['feature']}</td><td class="bad">✗ {r['old']}</td><td class="good">✓ {r['new']}</td></tr>"""

    faqs = ""
    for f in cf["faqs"]:
        faqs += f"""<div class="faq-item"><button class="faq-q" onclick="this.classList.toggle('open');this.nextElementSibling.classList.toggle('show')">{f['q']}<span>▼</span></button><div class="faq-a"><p>{f['a']}</p></div></div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{h['headline']} | {keyword}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#080b0f;--surface:#0f1419;--card:#131b24;--border:#1e2d3d;--accent:#00d4ff;--green:#00ff88;--text:#e2eaf3;--muted:#4a6080}}
body{{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;line-height:1.6}}
.hero{{min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;position:relative;overflow:hidden}}
.hero-bg{{position:absolute;inset:0;background:url('{hero_img}') center/cover;filter:brightness(.2) saturate(0.5)}}
.hero-bg::after{{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(0,212,255,.08),rgba(0,255,136,.04))}}
.hero-grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(0,212,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,212,255,.03) 1px,transparent 1px);background-size:40px 40px}}
.hero-content{{position:relative;z-index:2;max-width:750px;padding:40px 24px}}
.hero-tag{{display:inline-block;border:1px solid rgba(0,212,255,.3);color:var(--accent);padding:6px 18px;border-radius:4px;font-size:.7rem;letter-spacing:.15em;text-transform:uppercase;margin-bottom:24px;background:rgba(0,212,255,.05)}}
.hero h1{{font-size:clamp(2rem,5vw,3.5rem);font-weight:800;line-height:1.1;margin-bottom:16px;letter-spacing:-.02em}}
.hero h1 em{{font-style:normal;color:var(--accent)}}
.hero p{{color:var(--muted);font-size:1rem;margin-bottom:32px;max-width:500px;margin-left:auto;margin-right:auto}}
.hero-cta{{background:var(--accent);color:#000;padding:15px 36px;border:none;border-radius:4px;font-weight:700;font-size:.95rem;cursor:pointer;transition:all .2s;letter-spacing:.05em}}
.hero-cta:hover{{box-shadow:0 0 30px rgba(0,212,255,.4);transform:translateY(-2px)}}
.trust{{margin-top:16px;font-size:.72rem;color:var(--muted)}}
section{{padding:80px 24px}}
.sec-head{{text-align:center;margin-bottom:40px}}
.sec-head h2{{font-size:clamp(1.4rem,3vw,2rem);font-weight:700;margin-bottom:8px}}
.sec-head p{{color:var(--muted);font-size:.85rem}}
.pain-section{{background:var(--surface)}}
.pain-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;max-width:1000px;margin:0 auto}}
.pain-card{{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:24px;transition:all .2s}}
.pain-card:hover{{border-color:var(--accent);box-shadow:0 0 20px rgba(0,212,255,.1)}}
.pain-icon{{font-size:2rem;margin-bottom:12px}}
.pain-card h3{{font-size:.95rem;font-weight:700;margin-bottom:8px;color:var(--accent)}}
.pain-card p{{font-size:.8rem;color:var(--muted)}}
.features-section{{background:var(--bg)}}
.features-list{{max-width:800px;margin:0 auto;display:flex;flex-direction:column;gap:16px}}
.feature-item{{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:20px 24px;display:flex;gap:16px;align-items:flex-start;transition:all .2s}}
.feature-item:hover{{border-color:var(--green);box-shadow:0 0 15px rgba(0,255,136,.08)}}
.fi{{font-size:1.5rem;flex-shrink:0;margin-top:2px}}
.feature-item h3{{font-size:.9rem;font-weight:700;margin-bottom:4px;color:var(--green)}}
.feature-item p{{font-size:.8rem;color:var(--muted)}}
.proof-section{{background:var(--surface)}}
.metrics-row{{display:flex;justify-content:center;gap:48px;flex-wrap:wrap;margin-bottom:40px}}
.metric{{text-align:center}}
.m-num{{font-size:2.2rem;font-weight:800;color:var(--accent)}}
.m-lbl{{font-size:.7rem;color:var(--muted);margin-top:4px;text-transform:uppercase;letter-spacing:.08em}}
.testi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;max-width:1000px;margin:0 auto}}
.testi{{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:22px}}
.testi-stars{{color:#f59e0b;font-size:.85rem;margin-bottom:10px}}
.testi p{{font-size:.82rem;color:var(--muted);font-style:italic;margin-bottom:16px}}
.testi-author{{display:flex;align-items:center;gap:10px}}
.testi-author img{{width:36px;height:36px;border-radius:50%;object-fit:cover;border:2px solid var(--border)}}
.testi-author strong{{font-size:.8rem;display:block}}
.testi-author span{{font-size:.7rem;color:var(--muted)}}
.compare-section{{background:var(--bg)}}
.compare-table{{width:100%;max-width:800px;margin:0 auto;border-collapse:collapse}}
.compare-table thead tr{{background:var(--card);border:1px solid var(--border)}}
.compare-table th{{padding:14px 20px;text-align:left;font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:var(--accent)}}
.compare-table td{{padding:12px 20px;font-size:.82rem;border-bottom:1px solid var(--border)}}
.compare-table td:first-child{{color:var(--text);font-weight:600}}
td.bad{{color:#ef4444}}.td.good{{color:var(--green)}}
td.good{{color:var(--green);font-weight:600}}
.cta-section{{background:var(--surface);text-align:center;border-top:1px solid var(--border);border-bottom:1px solid var(--border)}}
.cta-section h2{{font-size:clamp(1.6rem,4vw,2.5rem);font-weight:800;margin-bottom:12px}}
.cta-section p{{color:var(--muted);margin-bottom:26px;max-width:480px;margin-left:auto;margin-right:auto}}
.cta-btn{{background:var(--accent);color:#000;padding:15px 40px;border:none;border-radius:4px;font-weight:700;font-size:.95rem;cursor:pointer;transition:all .2s}}
.cta-btn:hover{{box-shadow:0 0 30px rgba(0,212,255,.4)}}
.urgency{{margin-top:14px;font-size:.72rem;color:var(--muted)}}
.faq-section{{background:var(--bg);max-width:700px;margin:0 auto}}
.faq-section h2{{text-align:center;font-size:1.5rem;font-weight:700;margin-bottom:28px}}
.faq-item{{border:1px solid var(--border);border-radius:8px;margin-bottom:8px;overflow:hidden}}
.faq-q{{width:100%;padding:14px 18px;background:var(--card);border:none;color:var(--text);text-align:left;font-size:.85rem;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;font-family:inherit}}
.faq-q span{{color:var(--accent);font-size:.8rem;transition:transform .2s}}
.faq-q.open span{{transform:rotate(180deg)}}
.faq-a{{display:none;padding:0 18px 14px;background:var(--card);font-size:.82rem;color:var(--muted);line-height:1.7}}
.faq-a.show{{display:block}}
footer{{background:var(--surface);border-top:1px solid var(--border);text-align:center;padding:20px;font-size:.72rem;color:var(--muted)}}
@media(max-width:600px){{.metrics-row{{gap:20px}}}}
</style>
</head>
<body>
<section class="hero">
  <div class="hero-bg"></div><div class="hero-grid"></div>
  <div class="hero-content">
    <div class="hero-tag">{keyword}</div>
    <h1>{h['headline'].replace(keyword, f'<em>{keyword}</em>', 1)}</h1>
    <p>{h['subheadline']}</p>
    <button class="hero-cta">{h['cta']}</button>
    <div class="trust">{h['trust_line']}</div>
  </div>
</section>
<section class="pain-section"><div class="sec-head"><h2>{pp['headline']}</h2></div><div class="pain-grid">{pain_cards}</div></section>
<section class="features-section"><div class="sec-head"><h2>{ft['headline']}</h2></div><div class="features-list">{feature_items}</div></section>
<section class="proof-section"><div class="sec-head"><h2>{sp['headline']}</h2></div><div class="metrics-row">{metrics}</div><div class="testi-grid">{testimonials}</div></section>
<section class="compare-section"><div class="sec-head"><h2>{cp['headline']}</h2></div><table class="compare-table"><thead><tr><th>Feature</th><th>Old Way</th><th>With Us</th></tr></thead><tbody>{comp_rows}</tbody></table></section>
<section class="cta-section"><h2>{cf['headline']}</h2><p>{cf['subtext']}</p><button class="cta-btn">{cf['cta']}</button><div class="urgency">⚡ {cf['urgency']}</div></section>
<section class="faq-section"><h2>FAQ</h2>{faqs}</section>
<footer>© 2025 · {keyword} · Built with MarketAI</footer>
</body>
</html>"""


def build_academic_html(keyword: str, data: dict) -> str:
    h = data["hero"]
    pp = data["pain_points"]
    ft = data["features"]
    sp = data["social_proof"]
    cp = data["comparison"]
    cf = data["cta_faq"]

    hero_img = unsplash_url(h.get("image_query","university campus library"), 1400, 700)
    section_img = unsplash_url("students studying classroom", 1200, 500)

    pain_cards = ""
    for c in pp["cards"]:
        pain_cards += f"""<div class="pain-card"><div class="pain-icon">{c['icon']}</div><h3>{c['title']}</h3><p>{c['desc']}</p></div>"""

    feature_items = ""
    for f in ft["items"]:
        feature_items += f"""<div class="feature-item"><div class="fi-wrap"><span>{f['icon']}</span></div><div><h3>{f['title']}</h3><p>{f['desc']}</p></div></div>"""

    metrics = ""
    for m in sp["metrics"]:
        metrics += f'<div class="metric"><div class="m-num">{m["number"]}</div><div class="m-lbl">{m["label"]}</div></div>'

    testimonials = ""
    for t in sp["testimonials"]:
        av = unsplash_small(t.get("avatar_query","student"), 60, 60)
        testimonials += f"""<div class="testi"><p>"{t['quote']}"</p><div class="testi-author"><img src="{av}" alt="{t['name']}"/><div><strong>{t['name']}</strong><span>{t['role']}</span></div></div></div>"""

    comp_rows = ""
    for r in cp["rows"]:
        comp_rows += f"""<tr><td class="feat">{r['feature']}</td><td class="bad">✗ {r['old']}</td><td class="good">✓ {r['new']}</td></tr>"""

    faqs = ""
    for f in cf["faqs"]:
        faqs += f"""<div class="faq-item"><button class="faq-q" onclick="this.classList.toggle('open');this.nextElementSibling.classList.toggle('show')">{f['q']}<span>+</span></button><div class="faq-a"><p>{f['a']}</p></div></div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{h['headline']} | {keyword}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--navy:#1e3a5f;--gold:#c9a227;--light:#f5f7fa;--white:#ffffff;--text:#2d3748;--muted:#718096;--border:#e2e8f0}}
body{{font-family:'Georgia',serif;color:var(--text);line-height:1.7}}
.hero{{min-height:92vh;display:flex;align-items:center;position:relative;overflow:hidden}}
.hero-img{{position:absolute;inset:0;background:url('{hero_img}') center/cover;filter:brightness(.3)}}
.hero-overlay{{position:absolute;inset:0;background:linear-gradient(135deg,rgba(30,58,95,.9),rgba(30,58,95,.6))}}
.hero-content{{position:relative;z-index:2;max-width:800px;padding:60px 40px;color:#fff}}
.hero-badge{{display:inline-block;background:var(--gold);color:var(--navy);padding:6px 20px;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;font-family:'Segoe UI',sans-serif;font-weight:700;margin-bottom:22px}}
.hero h1{{font-size:clamp(2rem,4.5vw,3.2rem);font-weight:700;line-height:1.2;margin-bottom:16px}}
.hero p{{font-size:1.05rem;opacity:.88;margin-bottom:32px;max-width:550px;font-family:'Segoe UI',sans-serif}}
.hero-cta{{background:var(--gold);color:var(--navy);padding:16px 40px;border:none;font-family:'Segoe UI',sans-serif;font-weight:700;font-size:.95rem;cursor:pointer;transition:all .2s;letter-spacing:.03em}}
.hero-cta:hover{{background:#e6b82a;box-shadow:0 8px 24px rgba(201,162,39,.4);transform:translateY(-2px)}}
.trust{{margin-top:16px;font-size:.78rem;opacity:.7;font-family:'Segoe UI',sans-serif}}
section{{padding:80px 40px}}
.sec-head{{text-align:center;margin-bottom:44px}}
.sec-head .overline{{font-size:.65rem;text-transform:uppercase;letter-spacing:.15em;color:var(--gold);font-family:'Segoe UI',sans-serif;margin-bottom:8px}}
.sec-head h2{{font-size:clamp(1.5rem,3vw,2.2rem);font-weight:700;color:var(--navy)}}
.pain-section{{background:var(--light)}}
.pain-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;max-width:1000px;margin:0 auto}}
.pain-card{{background:var(--white);border-top:4px solid var(--gold);padding:24px;box-shadow:0 2px 12px rgba(0,0,0,.05)}}
.pain-icon{{font-size:2rem;margin-bottom:10px}}
.pain-card h3{{font-size:.95rem;font-weight:700;margin-bottom:8px;color:var(--navy);font-family:'Segoe UI',sans-serif}}
.pain-card p{{font-size:.82rem;color:var(--muted);font-family:'Segoe UI',sans-serif}}
.features-section{{background:var(--white)}}
.features-img{{width:100%;max-width:900px;height:280px;object-fit:cover;display:block;margin:0 auto 40px;border:4px solid var(--border)}}
.features-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px;max-width:1000px;margin:0 auto}}
.feature-item{{display:flex;gap:16px;padding:20px;border:1px solid var(--border);background:var(--light)}}
.fi-wrap{{width:40px;height:40px;background:var(--navy);display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0}}
.feature-item h3{{font-size:.88rem;font-weight:700;margin-bottom:5px;color:var(--navy);font-family:'Segoe UI',sans-serif}}
.feature-item p{{font-size:.8rem;color:var(--muted);font-family:'Segoe UI',sans-serif}}
.proof-section{{background:var(--navy);color:#fff}}
.proof-section .sec-head h2{{color:#fff}}
.metrics-row{{display:flex;justify-content:center;gap:60px;flex-wrap:wrap;margin-bottom:44px;padding:28px 0;border-top:1px solid rgba(255,255,255,.15);border-bottom:1px solid rgba(255,255,255,.15)}}
.metric{{text-align:center}}
.m-num{{font-size:2.4rem;font-weight:700;color:var(--gold)}}
.m-lbl{{font-size:.7rem;color:rgba(255,255,255,.6);text-transform:uppercase;letter-spacing:.08em;font-family:'Segoe UI',sans-serif;margin-top:4px}}
.testi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;max-width:1000px;margin:0 auto}}
.testi{{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);padding:24px}}
.testi p{{font-size:.85rem;color:rgba(255,255,255,.8);font-style:italic;margin-bottom:16px}}
.testi-author{{display:flex;align-items:center;gap:12px}}
.testi-author img{{width:40px;height:40px;border-radius:50%;object-fit:cover;border:2px solid var(--gold)}}
.testi-author strong{{font-size:.82rem;display:block;font-family:'Segoe UI',sans-serif;color:#fff}}
.testi-author span{{font-size:.72rem;color:rgba(255,255,255,.5);font-family:'Segoe UI',sans-serif}}
.compare-section{{background:var(--light)}}
.compare-table{{width:100%;max-width:800px;margin:0 auto;border-collapse:collapse}}
.compare-table thead{{background:var(--navy);color:#fff}}
.compare-table th{{padding:14px 20px;text-align:left;font-size:.78rem;letter-spacing:.05em;font-family:'Segoe UI',sans-serif}}
.compare-table td{{padding:12px 20px;font-size:.82rem;border-bottom:1px solid var(--border);font-family:'Segoe UI',sans-serif}}
td.feat{{font-weight:700;color:var(--navy)}}.td.bad{{color:#dc2626}}td.bad{{color:#dc2626}}td.good{{color:#15803d;font-weight:600}}
.cta-section{{background:var(--white);text-align:center;border-top:4px solid var(--gold)}}
.cta-section h2{{font-size:clamp(1.6rem,4vw,2.5rem);color:var(--navy);margin-bottom:12px}}
.cta-section p{{color:var(--muted);margin-bottom:28px;font-family:'Segoe UI',sans-serif;max-width:480px;margin-left:auto;margin-right:auto}}
.cta-btn{{background:var(--navy);color:#fff;padding:16px 44px;border:none;font-family:'Segoe UI',sans-serif;font-weight:700;font-size:.95rem;cursor:pointer;transition:all .2s}}
.cta-btn:hover{{background:#162d4a;box-shadow:0 8px 20px rgba(30,58,95,.3)}}
.urgency{{margin-top:14px;font-size:.76rem;color:var(--muted);font-family:'Segoe UI',sans-serif}}
.faq-section{{background:var(--light);max-width:720px;margin:0 auto}}
.faq-section h2{{text-align:center;font-size:1.6rem;color:var(--navy);margin-bottom:28px}}
.faq-item{{background:var(--white);border:1px solid var(--border);margin-bottom:8px}}
.faq-q{{width:100%;padding:15px 20px;background:none;border:none;text-align:left;font-size:.88rem;font-weight:700;cursor:pointer;display:flex;justify-content:space-between;color:var(--navy);font-family:'Segoe UI',sans-serif}}
.faq-q span{{color:var(--gold);font-size:1.1rem;transition:transform .2s}}
.faq-q.open span{{transform:rotate(45deg)}}
.faq-a{{display:none;padding:0 20px 15px;font-size:.83rem;color:var(--muted);font-family:'Segoe UI',sans-serif;line-height:1.7}}
.faq-a.show{{display:block}}
footer{{background:var(--navy);color:rgba(255,255,255,.5);text-align:center;padding:22px;font-size:.72rem;font-family:'Segoe UI',sans-serif}}
@media(max-width:600px){{.hero-content{{padding:40px 20px}}.metrics-row{{gap:24px}}}}
</style>
</head>
<body>
<section class="hero">
  <div class="hero-img"></div><div class="hero-overlay"></div>
  <div class="hero-content">
    <div class="hero-badge">{keyword}</div>
    <h1>{h['headline']}</h1>
    <p>{h['subheadline']}</p>
    <button class="hero-cta">{h['cta']}</button>
    <div class="trust">{h['trust_line']}</div>
  </div>
</section>
<section class="pain-section"><div class="sec-head"><div class="overline">The Problem</div><h2>{pp['headline']}</h2></div><div class="pain-grid">{pain_cards}</div></section>
<section class="features-section"><div class="sec-head"><div class="overline">Our Solution</div><h2>{ft['headline']}</h2></div><img class="features-img" src="{section_img}" alt="features"/><div class="features-grid">{feature_items}</div></section>
<section class="proof-section"><div class="sec-head"><div class="overline" style="color:var(--gold)">Results</div><h2>{sp['headline']}</h2></div><div class="metrics-row">{metrics}</div><div class="testi-grid">{testimonials}</div></section>
<section class="compare-section"><div class="sec-head"><div class="overline">Comparison</div><h2>{cp['headline']}</h2></div><table class="compare-table"><thead><tr><th>Feature</th><th>Traditional Approach</th><th>Our Approach</th></tr></thead><tbody>{comp_rows}</tbody></table></section>
<section class="cta-section"><h2>{cf['headline']}</h2><p>{cf['subtext']}</p><button class="cta-btn">{cf['cta']}</button><div class="urgency">⚡ {cf['urgency']}</div></section>
<section class="faq-section"><h2>Frequently Asked Questions</h2>{faqs}</section>
<footer>© 2025 · {keyword} · All rights reserved</footer>
</body>
</html>"""
