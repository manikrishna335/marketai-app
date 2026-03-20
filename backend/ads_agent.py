from seo_agent import call_groq
import json, re

UNSPLASH_KEY = "uzuoQOhJhBAPA3oZLUrM5caab91nTcIwrB92kEbX87k"

def img_url(query, w=1200, h=628):
    q = query.replace(" ", ",").replace("/", ",")
    return f"https://source.unsplash.com/{w}x{h}/?{q}"

async def generate_google_ads(keyword: str, business: str, budget: str, location: str, cpc: str = "1.00") -> dict:
    try:
        base_cpc = float(cpc.replace("$","").replace("₹","").strip())
        starting_bid = round(base_cpc * 1.10, 2)
    except:
        starting_bid = 1.10

    prompt = f"""You are a Google Ads expert. Create a COMPLETE campaign for:
Business: {business}
Keyword: "{keyword}"
Budget: {budget}
Location: {location}
Starting Bid: ${starting_bid} (10% above avg CPC)

Return ONLY valid JSON, no markdown:
{{
  "campaign_name": "Campaign name",
  "objective": "Lead Generation",
  "ad_formats": [
    {{
      "format": "Search Ad",
      "objective": "Lead Generation",
      "headline1": "30 char headline",
      "headline2": "30 char headline",
      "headline3": "30 char headline",
      "description1": "90 char description",
      "description2": "90 char description",
      "cta": "Get Free Quote",
      "image_query": "2-3 word image query for this ad",
      "display_url": "yoursite.com/keyword"
    }},
    {{
      "format": "Display Ad",
      "objective": "Awareness",
      "headline1": "Display headline",
      "headline2": "Supporting text",
      "headline3": "",
      "description1": "Display ad description under 90 chars",
      "description2": "",
      "cta": "Learn More",
      "image_query": "relevant image query",
      "display_url": "yoursite.com"
    }},
    {{
      "format": "Responsive Display Ad",
      "objective": "Retargeting",
      "headline1": "Retargeting headline",
      "headline2": "Come back offer",
      "headline3": "",
      "description1": "Retargeting description",
      "description2": "",
      "cta": "Book Now",
      "image_query": "relevant image query",
      "display_url": "yoursite.com"
    }}
  ],
  "ad_groups": [
    {{
      "name": "Ad Group 1 - Emotional",
      "angle": "Emotional Pain",
      "keywords_exact": ["keyword1","keyword2","keyword3","keyword4","keyword5"],
      "keywords_phrase": ["phrase keyword 1","phrase keyword 2","phrase keyword 3"],
      "negative_keywords": ["free","jobs","salary","course pdf"],
      "ads": [
        {{"headline1":"30 char","headline2":"30 char","headline3":"30 char","desc1":"90 char description","desc2":"90 char description","cta":"Get Started"}}
      ]
    }},
    {{
      "name": "Ad Group 2 - Logical",
      "angle": "Feature Driven",
      "keywords_exact": ["keyword1","keyword2","keyword3"],
      "keywords_phrase": ["phrase keyword 1","phrase keyword 2"],
      "negative_keywords": ["free","cheap","diy"],
      "ads": [
        {{"headline1":"30 char","headline2":"30 char","headline3":"30 char","desc1":"90 char description","desc2":"90 char description","cta":"Learn More"}}
      ]
    }},
    {{
      "name": "Ad Group 3 - Urgency",
      "angle": "Scarcity FOMO",
      "keywords_exact": ["keyword1","keyword2","keyword3"],
      "keywords_phrase": ["phrase keyword 1","phrase keyword 2"],
      "negative_keywords": ["free","cheap"],
      "ads": [
        {{"headline1":"30 char","headline2":"30 char","headline3":"30 char","desc1":"90 char description","desc2":"90 char description","cta":"Claim Offer"}}
      ]
    }}
  ],
  "extensions": {{
    "sitelinks": [
      {{"title":"Sitelink 1","desc1":"Description","desc2":"Description"}},
      {{"title":"Sitelink 2","desc1":"Description","desc2":"Description"}},
      {{"title":"Sitelink 3","desc1":"Description","desc2":"Description"}},
      {{"title":"Sitelink 4","desc1":"Description","desc2":"Description"}}
    ],
    "callouts": ["callout1","callout2","callout3","callout4"],
    "structured_snippets": {{"type":"Services","values":["Service 1","Service 2","Service 3"]}}
  }},
  "bidding": {{
    "strategy": "Target CPA",
    "starting_bid": {starting_bid},
    "daily_budget": "calculate from {budget}",
    "target_cpa": "realistic number",
    "scale_trigger": "When ROAS exceeds 3x"
  }},
  "image_query": "best image query for {keyword} ads"
}}"""

    raw = await call_groq(prompt, 2000)
    try:
        clean = re.sub(r'```json|```','',raw).strip()
        data = json.loads(clean)
        data['image_url'] = img_url(data.get('image_query', keyword + ' advertising'), 1200, 628)
        data['square_url'] = img_url(data.get('image_query', keyword), 400, 400)
        for fmt in data.get('ad_formats', []):
            fmt['image_url'] = img_url(fmt.get('image_query', keyword), 1200, 628)
            fmt['square_url'] = img_url(fmt.get('image_query', keyword), 400, 400)
        return data
    except:
        return {"raw": raw, "image_url": img_url(keyword, 1200, 628)}


async def generate_meta_ads(business: str, product: str, budget: str, age: str, location: str) -> dict:
    prompt = f"""You are a Meta Ads expert. Create complete Facebook/Instagram campaign for:
Business: {business}
Product: {product}
Budget: {budget}
Age: {age}
Location: {location}

Return ONLY valid JSON, no markdown:
{{
  "campaign_name": "Campaign name",
  "objective": "Lead Generation",
  "ad_formats": [
    {{
      "format": "Single Image Ad",
      "platform": "Facebook Feed",
      "objective": "Awareness",
      "primary_text": "125 char emotional hook text",
      "headline": "40 char headline",
      "description": "30 char description",
      "cta": "Learn More",
      "image_query": "relevant 3 word image query",
      "ratio": "1.91:1",
      "dimensions": "1200x628px"
    }},
    {{
      "format": "Carousel Ad",
      "platform": "Facebook + Instagram",
      "objective": "Consideration",
      "primary_text": "Carousel primary text",
      "headline": "Carousel headline",
      "description": "Carousel description",
      "cta": "Shop Now",
      "image_query": "relevant image query",
      "ratio": "1:1",
      "dimensions": "1080x1080px",
      "cards": [
        {{"title":"Card 1","desc":"Card 1 description","image_query":"card 1 image"}},
        {{"title":"Card 2","desc":"Card 2 description","image_query":"card 2 image"}},
        {{"title":"Card 3","desc":"Card 3 description","image_query":"card 3 image"}},
        {{"title":"Card 4","desc":"Card 4 description","image_query":"card 4 image"}}
      ]
    }},
    {{
      "format": "Story Ad",
      "platform": "Instagram Stories",
      "objective": "Lead Generation",
      "primary_text": "Story hook text",
      "headline": "Story headline",
      "description": "",
      "cta": "Swipe Up",
      "image_query": "vertical story image query",
      "ratio": "9:16",
      "dimensions": "1080x1920px"
    }},
    {{
      "format": "Video Ad",
      "platform": "Facebook + Instagram Reels",
      "objective": "Awareness",
      "primary_text": "Video primary text",
      "headline": "Video headline",
      "description": "Video description",
      "cta": "Watch More",
      "image_query": "video thumbnail image query",
      "ratio": "9:16",
      "dimensions": "1080x1920px",
      "video_script": {{
        "hook": "First 3 seconds hook text",
        "problem": "Pain point (5 sec)",
        "solution": "Solution reveal (10 sec)",
        "proof": "Social proof (5 sec)",
        "cta": "Call to action (5 sec)"
      }}
    }}
  ],
  "ad_sets": [
    {{
      "name": "Cold Audience - Emotional",
      "objective": "Awareness",
      "age": "{age}",
      "interests": ["interest1","interest2","interest3","interest4","interest5","interest6","interest7","interest8","interest9","interest10"],
      "behaviors": ["behavior1","behavior2"],
      "exclude": ["existing customers","competitors audience"],
      "budget_split": "40%",
      "placement": ["Facebook Feed","Instagram Feed","Stories"],
      "primary_text": "Emotional hook ad copy 125 chars",
      "headline": "40 char headline",
      "cta": "Learn More",
      "image_query": "emotional relatable image"
    }},
    {{
      "name": "Lookalike 1-3% - Logical",
      "objective": "Consideration",
      "lookalike_source": "Website visitors",
      "lookalike_percent": "1-3%",
      "budget_split": "35%",
      "placement": ["Facebook Feed","Instagram Feed"],
      "primary_text": "Feature benefit ad copy",
      "headline": "Feature headline",
      "cta": "Learn More",
      "image_query": "solution professional image"
    }},
    {{
      "name": "Retargeting - Scarcity",
      "objective": "Conversion",
      "custom_audience": "Website visitors 30 days",
      "retargeting_window": "30 days",
      "budget_split": "25%",
      "placement": ["Facebook Feed","Instagram Stories"],
      "primary_text": "Urgency retargeting copy",
      "headline": "Scarcity headline",
      "cta": "Book Now",
      "image_query": "urgency deadline image"
    }}
  ],
  "pixel_events": ["PageView","Lead","CompleteRegistration","Purchase","InitiateCheckout"],
  "ab_test": {{
    "week1": "Test creative format: image vs carousel",
    "week2": "Test audience: interest vs lookalike",
    "week3": "Test CTA: Learn More vs Book Now",
    "week4": "Scale winner, kill loser"
  }},
  "image_query": "best image for {product} facebook ad"
}}"""

    raw = await call_groq(prompt, 2000)
    try:
        clean = re.sub(r'```json|```','',raw).strip()
        data = json.loads(clean)
        data['image_url'] = img_url(data.get('image_query', product + ' facebook ad'), 1200, 628)
        for fmt in data.get('ad_formats', []):
            fmt['image_url'] = img_url(fmt.get('image_query', product), 1200, 628 if fmt.get('ratio','') != '9:16' else 1080)
            fmt['square_url'] = img_url(fmt.get('image_query', product), 400, 400)
            if 'cards' in fmt:
                for card in fmt['cards']:
                    card['image_url'] = img_url(card.get('image_query', product), 400, 400)
        for ads in data.get('ad_sets', []):
            ads['image_url'] = img_url(ads.get('image_query', product), 1200, 628)
        return data
    except:
        return {"raw": raw, "image_url": img_url(product, 1200, 628)}


async def generate_image_prompts(keyword: str, angle: str) -> str:
    prompt = f"""Generate 3 realistic environment-based image prompts for ads about "{keyword}". Angle: {angle}.

IMAGE PROMPT 1 (Facebook/Instagram Feed 1:1):
Scene: [detailed real scene, not stock photo]
Subject: [who/what]
Mood: [emotion]
Lighting: [type of lighting]
Colors: [color palette]
Canva tip: [how to overlay text]

IMAGE PROMPT 2 (Instagram Story 9:16):
Scene:
Subject:
Mood:
Lighting:
Colors:
Canva tip:

IMAGE PROMPT 3 (Google Display 16:9):
Scene:
Subject:
Mood:
Lighting:
Colors:
Canva tip:

CANVA DESIGN GUIDE:
Font: [recommended font]
CTA button color: [hex]
Text overlay position:
Background overlay: [opacity]"""
    return await call_groq(prompt, 800)
