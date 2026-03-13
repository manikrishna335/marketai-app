import httpx
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

async def call_groq(prompt: str, max_tokens: int = 2000) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.6
    }
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, headers=headers, json=body)
            data = r.json()
            if "choices" in data:
                return data["choices"][0]["message"]["content"]
            return f"Error: {data.get('error', {}).get('message', str(data))}"
    except Exception as e:
        return f"Error: {str(e)}"

async def keyword_cluster(keyword: str, persona: str = "student", country: str = "India") -> dict:
    prompt = f"""You are an expert SEO keyword researcher. Analyze keyword: "{keyword}" for {country} market.

TARGET PERSONA: {persona}

IMPORTANT: Filter out any keywords with "{
    'corporate' if persona == 'student' else 'student'
}" intent. Focus only on {persona}-focused keywords.

Return EXACTLY this structured data:

═══ KEYWORD INTELLIGENCE REPORT ═══

PRIMARY KEYWORD:
- Keyword: {keyword}
- Monthly Search Volume: [realistic number for {country}]
- Keyword Difficulty (KD): [0-100, based on typical top-10 competitor domain authority]
- Search Intent: [Informational/Commercial/Transactional/Navigational]
- CPC Average: [realistic USD]
- Competition: [Low/Medium/High]
- Persona Match: [Student/Professional/Corporate] — VERIFY this matches {persona}
- Trend: [Growing/Stable/Declining]

1+4 KEYWORD CLUSTER:

PRIMARY (High-Intent Transactional):
→ [keyword] | Vol: [X] | KD: [X] | Intent: Transactional | CPC: $[X]

SECONDARY CLUSTER (4 LSI Variations):
→ HOW-TO: "how to [keyword]" | Vol: [X] | KD: [X] | Intent: Informational | CPC: $[X]
→ COST: "[keyword] cost/price/fees" | Vol: [X] | KD: [X] | Intent: Commercial | CPC: $[X]
→ COMPARISON: "best [keyword] vs [alternative]" | Vol: [X] | KD: [X] | Intent: Commercial | CPC: $[X]
→ BENEFITS: "[keyword] benefits/advantages" | Vol: [X] | KD: [X] | Intent: Informational | CPC: $[X]

LONG TAIL KEYWORDS (10):
[List 10 long tail keywords with Vol, KD, Intent]

QUICK WIN KEYWORDS (5 low KD, good volume):
[List 5 keywords with KD under 30]

COMPETITOR ANALYSIS (Top 5 ranking sites):
[List 5 types of sites likely ranking for this keyword with estimated DA]

KD CALCULATION METHOD:
[Explain how KD was estimated based on competitor strength]

CONTENT GAP OPPORTUNITIES:
[3 specific angles competitors are missing]

RECOMMENDED STRATEGY:
[Specific 3-step plan to rank for this cluster]"""

    result = await call_groq(prompt, 2000)
    return {"keyword": keyword, "persona": persona, "country": country, "cluster": result}

async def verify_intent(keyword: str, persona: str) -> dict:
    prompt = f"""Verify if keyword "{keyword}" matches the {persona} persona.

Check:
1. INTENT MATCH: Does this keyword show {persona} search behavior? (Yes/No + reason)
2. PERSONA SCORE: Rate 1-10 how well this matches {persona} intent
3. RED FLAGS: Any corporate/professional intent signals to filter?
4. RECOMMENDATION: Use as-is / Modify / Reject
5. BETTER ALTERNATIVE: If reject, suggest better keyword for {persona} persona

Be concise and direct."""
    result = await call_groq(prompt, 500)
    return {"keyword": keyword, "persona": persona, "verification": result}
