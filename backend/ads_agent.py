from seo_agent import call_groq

async def generate_google_ads(keyword: str, business: str, budget: str, location: str, cpc: str = "1.00") -> str:
    # Auto-bidding: 10% above average CPC
    try:
        base_cpc = float(cpc.replace("$", "").replace("₹", "").strip())
        starting_bid = round(base_cpc * 1.10, 2)
    except:
        starting_bid = "Set 10% above your average CPC"

    prompt = f"""You are a Google Ads expert. Create a COMPLETE ready-to-launch campaign.

Business: {business}
Target Keyword: {keyword}
Monthly Budget: {budget}
Location: {location}
STARTING BID LOGIC: {starting_bid} (10% above average CPC to win auction immediately)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CAMPAIGN SETTINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Campaign Name:
Campaign Type: Search
Goal:
Daily Budget: [calculate from {budget}]
Bidding Strategy: [recommend with reason]
Target CPA/ROAS: [realistic number]
Starting Bid: {starting_bid} [10% above avg CPC — auction win strategy]
Location: {location}
Ad Schedule: [best hours/days for this keyword]
Negative Keywords (20): [list them]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AD GROUP 1 — ANGLE A: EMOTIONAL (The Pain)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ad Group Name:
Keywords (10 exact match): ["keyword1", "keyword2"...]
Keywords (10 phrase match): ["keyword1", "keyword2"...]

AD 1A:
Headline 1 (30 chars): [Addresses pain point emotionally]
Headline 2 (30 chars): [Empathy + solution]
Headline 3 (30 chars): [CTA]
Description 1 (90 chars): [Story-based, emotional hook]
Description 2 (90 chars): [Benefit + urgency]
Display Path: /keyword/solution

AD 1B:
Headline 1 (30 chars):
Headline 2 (30 chars):
Headline 3 (30 chars):
Description 1 (90 chars):
Description 2 (90 chars):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AD GROUP 2 — ANGLE B: LOGICAL (The Solution)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ad Group Name:
Keywords (10 exact match):
Keywords (10 phrase match):

AD 2A:
Headline 1 (30 chars): [Feature-driven]
Headline 2 (30 chars): [Statistics/proof]
Headline 3 (30 chars): [CTA]
Description 1 (90 chars): [Feature list]
Description 2 (90 chars): [Logic + benefit]

AD 2B:
Headline 1 (30 chars):
Headline 2 (30 chars):
Headline 3 (30 chars):
Description 1 (90 chars):
Description 2 (90 chars):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AD GROUP 3 — ANGLE C: SCARCITY (The Deadline)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ad Group Name:
Keywords (10 exact match):
Keywords (10 phrase match):

AD 3A:
Headline 1 (30 chars): [Urgency/scarcity]
Headline 2 (30 chars): [Limited time/spots]
Headline 3 (30 chars): [CTA with deadline]
Description 1 (90 chars): [Scarcity + fear of missing out]
Description 2 (90 chars): [What they lose if they don't act]

AD 3B:
Headline 1 (30 chars):
Headline 2 (30 chars):
Headline 3 (30 chars):
Description 1 (90 chars):
Description 2 (90 chars):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALL AD EXTENSIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sitelinks (4):
1. Title: | Desc 1: | Desc 2:
2. Title: | Desc 1: | Desc 2:
3. Title: | Desc 1: | Desc 2:
4. Title: | Desc 1: | Desc 2:

Callouts (4): [short phrases]
Structured Snippets: Type: | Values:
Call Extension: [when to show]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BIDDING STRATEGY EXPLAINED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Starting Bid: {starting_bid} (10% above avg CPC)
Why 10% above: [explain auction dynamics]
Week 1-2: [manual CPC strategy]
Week 3-4: [when to switch to Smart Bidding]
Scale trigger: [when to increase budget]

30-DAY OPTIMIZATION CALENDAR:
Week 1: [tasks]
Week 2: [tasks]
Week 3: [tasks]
Week 4: [tasks]"""

    return await call_groq(prompt, 2000)

async def generate_meta_ads(business: str, product: str, budget: str, age: str, location: str) -> str:
    prompt = f"""You are a Meta Ads expert. Create a COMPLETE Facebook/Instagram campaign.

Business: {business}
Product/Service: {product}
Monthly Budget: {budget}
Target Age: {age}
Location: {location}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CAMPAIGN STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Campaign Name:
Objective: [best for this business]
Budget Type: CBO
Daily Budget: [from {budget}]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AD SET 1 — ANGLE A: EMOTIONAL (Cold Audience)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Targeting:
- Age: {age} | Location: {location}
- 20 Specific Interests: [list them]
- Behaviors: [relevant behaviors]
- Exclude: [who to exclude]
Placements: [which placements]
Budget Split: [% of total]

CREATIVE A1 — IMAGE AD:
Format: Single Image
Primary Text (125 chars): [Emotional hook — addresses pain]
Headline (40 chars): [Empathy-based]
Description (30 chars):
CTA Button:
Image Prompt (environment-based, realistic): [Describe real scene, e.g. "Student at messy desk at 2am, coffee cup, textbooks, stressed expression, warm lamp light, candid photo style"]

CREATIVE A2 — VIDEO AD:
Hook (first 3 seconds): [What they see and hear]
Script (30 seconds): [Full video script]
CTA:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AD SET 2 — ANGLE B: LOGICAL (Lookalike)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Lookalike Source:
Lookalike %: 1-3%
Additional targeting:
Budget Split:

CREATIVE B1 — CAROUSEL AD:
Card 1: Image prompt | Headline | Description
Card 2: Image prompt | Headline | Description
Card 3: Image prompt | Headline | Description
Card 4: Image prompt | Headline | Description
Primary Text: [Feature/benefit driven]
CTA:

CREATIVE B2 — IMAGE AD:
Primary Text: [Logic + stats]
Headline:
Image Prompt: [Clean, solution-focused environment]
CTA:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AD SET 3 — ANGLE C: SCARCITY (Retargeting)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Custom Audience: Website visitors (30 days)
Retargeting Window: 30 days
Budget Split:

CREATIVE C1 — IMAGE AD:
Primary Text: [Urgency — they already know you]
Headline: [Scarcity/deadline]
Image Prompt: [Urgency visual]
CTA:

CREATIVE C2 — STORY AD:
Story Script (15 seconds):
Swipe Up Text:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PIXEL EVENTS TO TRACK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[List 6 key pixel events to set up]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
A/B TEST PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Week 1 Test: [what to test]
Week 2 Test: [what to test]
Week 3 Test: [what to test]
Week 4: [scale winner]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCALING STRATEGY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scale trigger (ROAS/CPA threshold):
How to scale: [vertical vs horizontal]
Budget increase %: [safe scaling rule]"""

    return await call_groq(prompt, 2000)

async def generate_image_prompts(keyword: str, angle: str) -> str:
    prompt = f"""Generate 3 realistic, environment-based image prompts for ads about "{keyword}".
Angle: {angle}

RULES:
- NO stock photo style (no smiling people in suits)
- Environment-based and candid (real life situations)
- Emotionally resonant
- Zero copyright issues (original scene descriptions)

IMAGE PROMPT 1 (Facebook/Instagram Feed — 1:1):
Scene description: [detailed environment, lighting, emotion, composition]
Subject: [who/what is in frame]
Mood: [emotional tone]
Style: [candid/documentary/lifestyle]

IMAGE PROMPT 2 (Instagram Story — 9:16):
Scene description:
Subject:
Mood:
Style:

IMAGE PROMPT 3 (Google Display — 16:9):
Scene description:
Subject:
Mood:
Style:

CANVA/DESIGN NOTES:
- Color palette suggestion:
- Font style:
- Overlay text placement:"""

    return await call_groq(prompt, 800)
