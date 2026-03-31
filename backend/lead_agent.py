from seo_agent import call_groq
import json, re, asyncio

async def research_competitors(service: str, location: str = "India") -> dict:
    prompt = f"""You are a B2B competitive intelligence expert. Research competitors for "{service}" in {location}.
Return ONLY valid JSON:
{{
  "competitors": [
    {{
      "company": "Real company name",
      "website": "https://website.com",
      "da": 42,
      "pa": 36,
      "founded": "2016",
      "employees": "50-200",
      "location": "Bangalore, India",
      "services": ["Service 1", "Service 2", "Service 3"],
      "pricing_model": "Project-based",
      "pricing_range": "$25-50/hr",
      "key_clients": ["Client 1", "Client 2", "Client 3"],
      "case_studies": ["Case study brief 1", "Case study brief 2"],
      "tech_stack": ["Tech 1", "Tech 2"],
      "contact_person": "CEO Name",
      "guessed_email": "ceo@website.com",
      "linkedin": "https://linkedin.com/company/name",
      "strengths": ["Strength 1", "Strength 2"],
      "weaknesses": ["Weakness 1", "Weakness 2"],
      "opportunity": "How to compete or partner"
    }}
  ],
  "market_insights": {{
    "market_size": "₹5000 Cr",
    "growth_rate": "18% YoY",
    "avg_project_value": "₹10-50 Lakhs",
    "top_buying_triggers": ["Digital transformation", "Cost reduction", "Scale up"],
    "common_pain_points": ["Lack of in-house expertise", "Budget constraints", "Timeline pressure"]
  }},
  "your_positioning": "Position as AI-powered full-stack agency with faster delivery"
}}
Generate 8 realistic competitors for {service} in {location}."""

    raw = await call_groq(prompt, 2000)
    try:
        clean = re.sub(r'```json|```', '', raw).strip()
        return json.loads(clean)
    except:
        return {"competitors": [], "error": raw[:200]}


async def find_leads(service: str, location: str = "India", lead_type: str = "client") -> dict:
    target = "potential clients who need to buy" if lead_type == "client" else "potential agency partners"
    prompt = f"""Find 10 {target} for a company offering "{service}" in {location}.
Return ONLY valid JSON:
{{
  "leads": [
    {{
      "company": "Company name",
      "website": "https://website.com",
      "industry": "E-commerce",
      "size": "SME",
      "employees": "50-200",
      "location": "Mumbai, India",
      "why_they_need": "Specific reason they need {service}",
      "pain_point": "Their exact pain point",
      "decision_maker": "CTO",
      "contact_name": "Person name",
      "email": "name@company.com",
      "linkedin": "https://linkedin.com/in/name",
      "phone": "+91-9XXXXXXXXX",
      "budget_estimate": "₹5-20 Lakhs",
      "buying_stage": "Consideration",
      "best_channel": "LinkedIn",
      "pitch_angle": "Specific pitch for this company",
      "urgency": "High"
    }}
  ],
  "outreach_strategy": "Best strategy for this segment"
}}"""

    raw = await call_groq(prompt, 2000)
    try:
        clean = re.sub(r'```json|```', '', raw).strip()
        return json.loads(clean)
    except:
        return {"leads": [], "error": raw[:200]}


async def generate_outreach(company: str, contact: str, role: str, pain: str, service: str, sender: str) -> dict:
    prompt = f"""Write personalized B2B outreach for:
Lead: {company}, Contact: {contact}, Role: {role}
Pain Point: {pain}, Service: {service}, Sender: {sender}

Return ONLY valid JSON:
{{
  "email": {{
    "subject": "Subject under 50 chars",
    "body": "Personalized email 120 words. Reference their pain point specifically."
  }},
  "linkedin": {{
    "connection_note": "Connection request under 300 chars",
    "follow_up": "Follow-up message under 200 chars"
  }},
  "whatsapp": {{
    "message": "WhatsApp message under 80 words"
  }},
  "call_script": {{
    "opener": "Opening 10 seconds",
    "pitch": "30 second pitch",
    "objection": "Handle not interested",
    "close": "Ask for meeting"
  }}
}}"""

    raw = await call_groq(prompt, 1000)
    try:
        clean = re.sub(r'```json|```', '', raw).strip()
        return json.loads(clean)
    except:
        return {"error": "Parse failed"}


async def full_lead_research(service: str, location: str, company_name: str) -> dict:
    comp_task = research_competitors(service, location)
    lead_task = find_leads(service, location, "client")
    partner_task = find_leads(service, location, "partner")
    competitors, leads, partners = await asyncio.gather(comp_task, lead_task, partner_task)
    return {
        "service": service, "location": location, "company": company_name,
        "competitors": competitors, "leads": leads, "partners": partners
    }
