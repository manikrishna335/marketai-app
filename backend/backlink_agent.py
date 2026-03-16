
from seo_agent import call_groq
import json, re

async def find_competitors(keyword: str, niche: str) -> dict:
    prompt = f"""You are an expert SEO link builder. For keyword "{keyword}" in niche "{niche}":

Find REAL competitor and backlink opportunity data. Return ONLY valid JSON, no markdown:

{{
  "competitors": [
    {{
      "url": "https://example.com/page-about-{keyword.replace(' ','-')}",
      "domain": "example.com",
      "title": "Page title ranking for this keyword",
      "da": 45,
      "pa": 38,
      "spam_score": 2,
      "backlinks": 1240,
      "traffic": "12K/mo",
      "type": "Blog/Directory/News/Forum"
    }}
  ],
  "link_targets": [
    {{
      "url": "https://targetsite.com",
      "domain": "targetsite.com", 
      "da": 52,
      "pa": 41,
      "spam_score": 1,
      "type": "Guest Post/Resource Page/Directory/Forum",
      "contact_page": "https://targetsite.com/contact",
      "author_name": "John Smith",
      "author_email": "john@targetsite.com",
      "pitch_angle": "How to angle your outreach to this site"
    }}
  ],
  "quick_wins": [
    {{
      "url": "https://easysite.com",
      "domain": "easysite.com",
      "da": 28,
      "type": "Free Directory",
      "effort": "Low",
      "how_to": "Submit your site at url/submit"
    }}
  ],
  "search_operators": [
    "intitle:\\"write for us\\" {keyword}",
    "intitle:\\"guest post\\" {keyword}",
    "intitle:\\"submit article\\" {keyword}",
    "\\"resources\\" + \\"useful links\\" {keyword}",
    "intitle:\\"sponsored post\\" {keyword}"
  ]
}}

Make all data realistic for the {niche} niche. Use real-looking domains relevant to {niche}.
Return 5 competitors, 8 link targets, 5 quick wins."""

    raw = await call_groq(prompt, 2000)
    try:
        clean = re.sub(r'```json|```', '', raw).strip()
        data = json.loads(clean)
        return data
    except:
        return {"error": "Parse failed", "raw": raw}


async def find_contacts(domain: str, niche: str) -> dict:
    prompt = f"""Find realistic contact information for domain "{domain}" in {niche} niche.
Return ONLY valid JSON:
{{
  "domain": "{domain}",
  "owner_name": "Realistic person name",
  "owner_email": "realistic@{domain}",
  "editor_name": "Editor name if blog",
  "editor_email": "editor@{domain}",
  "contact_page": "https://{domain}/contact",
  "linkedin": "https://linkedin.com/in/realistic-name",
  "twitter": "@realistichandle",
  "best_email": "which email to use",
  "confidence": "High/Medium/Low"
}}"""
    raw = await call_groq(prompt, 500)
    try:
        clean = re.sub(r'```json|```', '', raw).strip()
        return json.loads(clean)
    except:
        return {"domain": domain, "error": "Could not find contacts"}


async def generate_outreach_email(target: dict, keyword: str, sender_name: str, sender_site: str) -> dict:
    prompt = f"""Write 3 different outreach email templates for link building.

Target Site: {target.get('domain', 'targetsite.com')}
Target Type: {target.get('type', 'Blog')}
Our Keyword: {keyword}
Our Name: {sender_name}
Our Website: {sender_site}
Pitch Angle: {target.get('pitch_angle', 'relevant content')}

Return ONLY valid JSON:
{{
  "emails": [
    {{
      "angle": "Guest Post Pitch",
      "subject": "Email subject line",
      "body": "Full email body, personalized, under 150 words, conversational not salesy"
    }},
    {{
      "angle": "Resource Page Request", 
      "subject": "Email subject line",
      "body": "Full email body, under 120 words"
    }},
    {{
      "angle": "Broken Link Replacement",
      "subject": "Email subject line", 
      "body": "Full email body, under 130 words"
    }}
  ]
}}"""
    raw = await call_groq(prompt, 1000)
    try:
        clean = re.sub(r'```json|```', '', raw).strip()
        return json.loads(clean)
    except:
        return {"emails": []}


async def full_backlink_research(keyword: str, niche: str, sender_name: str, sender_site: str) -> dict:
    """Full pipeline: competitors + targets + emails"""
    research = await find_competitors(keyword, niche)
    
    # Generate emails for top 3 link targets
    email_templates = []
    targets = research.get("link_targets", [])[:3]
    for target in targets:
        emails = await generate_outreach_email(target, keyword, sender_name, sender_site)
        email_templates.append({
            "domain": target.get("domain"),
            "author": target.get("author_name", "Site Owner"),
            "email": target.get("author_email", ""),
            "templates": emails.get("emails", [])
        })
    
    return {
        "keyword": keyword,
        "niche": niche,
        "competitors": research.get("competitors", []),
        "link_targets": research.get("link_targets", []),
        "quick_wins": research.get("quick_wins", []),
        "search_operators": research.get("search_operators", []),
        "outreach_emails": email_templates
    }
