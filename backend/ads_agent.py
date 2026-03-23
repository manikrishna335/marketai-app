from seo_agent import call_groq
import json, re

UNSPLASH_KEY = "uzuoQOhJhBAPA3oZLUrM5caab91nTcIwrB92kEbX87k"

def img_api_url(query):
    """Returns Unsplash API URL — frontend JS fetches actual photo from this"""
    q = re.sub(r'[^\w\s]', '', query).strip().replace(' ', '+')
    return f"__UNSPLASH__{q}"  # Frontend will replace this

async def generate_google_ads(keyword: str, business: str, budget: str, location: str, cpc: str = "1.00") -> dict:
    try:
        base_cpc = float(cpc.replace("$","").replace("₹","").strip())
        starting_bid = round(base_cpc * 1.10, 2)
    except:
        starting_bid = 1.10

    prompt = f"""Google Ads expert. Create complete campaign for:
Business: {business}, Keyword: "{keyword}", Budget: {budget}, Location: {location}

Return ONLY valid JSON:
{{
  "campaign_name": "{business} - {keyword} Campaign",
  "objective": "Lead Generation",
  "daily_budget": "₹{int(budget.replace('₹','').replace(',','').replace(' ','').replace('/month','').strip() or 20000) // 30 if budget else 667}",
  "starting_bid": {starting_bid},
  "bidding_strategy": "Target CPA",
  "ad_formats": [
    {{
      "format": "Search Ad",
      "objective": "Lead Generation",
      "headline1": "Max 30 chars here",
      "headline2": "Max 30 chars here",
      "headline3": "Max 30 chars here",
      "description1": "Max 90 chars compelling description for this ad",
      "description2": "Max 90 chars second description with CTA",
      "cta": "Get Free Quote",
      "image_query": "{keyword} education student",
      "display_url": "yoursite.com/{keyword.replace(' ', '-').lower()}"
    }},
    {{
      "format": "Display Ad",
      "objective": "Awareness",
      "headline1": "Display headline here",
      "headline2": "Supporting text here",
      "headline3": "",
      "description1": "Display ad description max 90 chars with benefit",
      "description2": "",
      "cta": "Learn More",
      "image_query": "{keyword} professional success",
      "display_url": "yoursite.com"
    }},
    {{
      "format": "Responsive Display",
      "objective": "Retargeting",
      "headline1": "Come back headline",
      "headline2": "Special offer text",
      "headline3": "",
      "description1": "Retargeting description reminding them of benefit",
      "description2": "",
      "cta": "Book Now",
      "image_query": "{keyword} results achievement",
      "display_url": "yoursite.com/offer"
    }}
  ],
  "ad_groups": [
    {{
      "name": "Emotional - Pain Points",
      "angle": "Emotional Pain",
      "keywords_exact": ["{keyword}", "best {keyword}", "top {keyword}", "{keyword} online", "affordable {keyword}"],
      "keywords_phrase": ["best {keyword} near me", "{keyword} for students", "learn {keyword} fast"],
      "negative_keywords": ["free", "jobs", "salary", "download", "pdf", "how to"],
      "ads": [
        {{"headline1":"Struggling With {keyword[:20]}?","headline2":"Expert Help Available Now","headline3":"Start Free Today","desc1":"Tired of falling behind? Our experts help you succeed faster. Join 10000+ students.","desc2":"98% success rate. Money back guarantee. Book your free demo class now.","cta":"Book Free Demo"}}
      ]
    }},
    {{
      "name": "Logical - Features",
      "angle": "Feature Driven",
      "keywords_exact": ["{keyword} classes", "{keyword} course", "{keyword} coaching", "online {keyword}", "{keyword} tutor"],
      "keywords_phrase": ["{keyword} classes online", "best {keyword} course", "{keyword} coaching center"],
      "negative_keywords": ["free", "cheap", "diy", "yourself"],
      "ads": [
        {{"headline1":"#1 Rated {keyword[:18]} Course","headline2":"Live Sessions + Recordings","headline3":"Try 7 Days Free","desc1":"Expert tutors, personalized plans, real-time progress tracking. Proven results.","desc2":"From ₹999/month. 50+ expert tutors. 24/7 doubt support. Start today.","cta":"Start Free Trial"}}
      ]
    }},
    {{
      "name": "Urgency - Scarcity",
      "angle": "Scarcity FOMO",
      "keywords_exact": ["{keyword} near me", "{keyword} admission", "join {keyword}", "{keyword} enrollment", "enroll {keyword}"],
      "keywords_phrase": ["enroll in {keyword}", "{keyword} open admission", "limited seats {keyword}"],
      "negative_keywords": ["free", "cheap"],
      "ads": [
        {{"headline1":"Only 8 Seats Left!","headline2":"{keyword[:22]} Batch Closing","headline3":"Enroll Before It Fills","desc1":"Last few spots available for this month batch. 47 students enrolled this week.","desc2":"Don't miss out. Secure your spot now before batch is full. No regrets.","cta":"Claim Your Seat"}}
      ]
    }}
  ],
  "extensions": {{
    "sitelinks": [
      {{"title":"Free Demo Class","desc1":"Try before you buy","desc2":"No credit card needed"}},
      {{"title":"View Success Stories","desc1":"See real student results","desc2":"98 percent success rate"}},
      {{"title":"Pricing Plans","desc1":"Plans from 999 per month","desc2":"No hidden charges"}},
      {{"title":"About Our Tutors","desc1":"50+ verified experts","desc2":"5+ years experience"}}
    ],
    "callouts": ["No Registration Fee", "Free Demo Available", "Money Back Guarantee", "24/7 Support"],
    "structured_snippets": {{"type":"Courses","values":["{keyword}", "Exam Prep", "Doubt Clearing", "Mock Tests"]}}
  }},
  "bidding_guide": "Start at ${starting_bid} (10% above avg CPC to win auction). Week 1-2: Manual CPC. Week 3+: Switch to Target CPA once 20+ conversions collected.",
  "image_query": "{keyword} student education success"
}}"""

    raw = await call_groq(prompt, 2000)
    try:
        clean = re.sub(r'```json|```','',raw).strip()
        data = json.loads(clean)
        # Add image queries for frontend to load
        data['_unsplash_key'] = UNSPLASH_KEY
        for fmt in data.get('ad_formats', []):
            fmt['_img_query'] = fmt.get('image_query', keyword + ' education')
        return data
    except Exception as e:
        return {"error": str(e), "raw": raw[:500], "_unsplash_key": UNSPLASH_KEY}


async def generate_meta_ads(business: str, product: str, budget: str, age: str, location: str) -> dict:
    prompt = f"""Meta Ads expert. Complete Facebook/Instagram campaign:
Business: {business}, Product: {product}, Budget: {budget}, Age: {age}, Location: {location}

Return ONLY valid JSON:
{{
  "campaign_name": "{business} - Meta Campaign",
  "objective": "Lead Generation",
  "ad_formats": [
    {{
      "format": "Single Image Ad",
      "platform": "Facebook + Instagram Feed",
      "objective": "Awareness",
      "primary_text": "Are you struggling with {product}? Thousands of students just like you found the solution. Don't let another month go by without making progress.",
      "headline": "Transform Your {product[:30]} Results",
      "description": "Expert guidance. Real results.",
      "cta": "Learn More",
      "image_query": "{product} student success happy",
      "ratio": "1.91:1",
      "dimensions": "1200x628px"
    }},
    {{
      "format": "Carousel Ad",
      "platform": "Facebook + Instagram",
      "objective": "Consideration",
      "primary_text": "Here is what our students achieve with us. Swipe to see their journey.",
      "headline": "Real Students, Real Results",
      "description": "Join 10000+ success stories",
      "cta": "Sign Up",
      "image_query": "{product} education achievement",
      "ratio": "1:1",
      "dimensions": "1080x1080px",
      "cards": [
        {{"title":"Week 1: Foundation","desc":"Build strong fundamentals fast","image_query":"{product} beginner learning"}},
        {{"title":"Week 2: Practice","desc":"Hands-on exercises daily","image_query":"{product} student practice"}},
        {{"title":"Week 3: Progress","desc":"Measurable grade improvement","image_query":"{product} progress chart"}},
        {{"title":"Week 4: Results","desc":"Achieve your target score","image_query":"{product} success achievement"}}
      ]
    }},
    {{
      "format": "Story Ad",
      "platform": "Instagram + Facebook Stories",
      "objective": "Lead Generation",
      "primary_text": "Swipe up for free demo",
      "headline": "Get Free Demo Today",
      "description": "Limited spots left",
      "cta": "Swipe Up",
      "image_query": "{product} mobile student vertical",
      "ratio": "9:16",
      "dimensions": "1080x1920px"
    }},
    {{
      "format": "Video Ad",
      "platform": "Instagram Reels + Facebook",
      "objective": "Awareness",
      "primary_text": "This student went from failing to top of class in 60 days. Here is how.",
      "headline": "From Failing to Top Class",
      "description": "Watch the transformation",
      "cta": "Watch More",
      "image_query": "{product} transformation before after",
      "ratio": "9:16",
      "dimensions": "1080x1920px",
      "video_script": {{
        "hook": "Show student looking stressed at desk with failing grade",
        "problem": "Voiceover: Most students waste months with wrong approach",
        "solution": "Cut to: Same student with tutor, understanding content clearly",
        "proof": "Show: Grade card improvement, happy parent reaction",
        "cta": "Text overlay: Book your free demo now. Link in bio."
      }}
    }}
  ],
  "ad_sets": [
    {{
      "name": "Cold Audience - Emotional",
      "objective": "Awareness",
      "age": "{age}",
      "location": "{location}",
      "interests": ["Education","Online Learning","IB Curriculum","CBSE","Academic tutoring","Khan Academy","Byju's","Unacademy","Study skills","Academic performance"],
      "behaviors": ["Parents of school-age children","Recently enrolled in education"],
      "exclude": ["Competitors customers"],
      "budget_split": "40%",
      "placement": ["Facebook Feed","Instagram Feed","Stories"],
      "primary_text": "Is your child struggling with {product}? 10,000+ students found success with our expert tutors. Book a free demo today.",
      "headline": "Expert {product[:25]} Help",
      "cta": "Book Free Demo",
      "image_query": "{product} student struggling then succeeding"
    }},
    {{
      "name": "Lookalike 1-3% - Logical",
      "objective": "Consideration",
      "lookalike_source": "Past customers",
      "lookalike_percent": "1-3%",
      "budget_split": "35%",
      "placement": ["Facebook Feed","Instagram Feed"],
      "primary_text": "Join 10,000+ students who improved grades with our AI-powered personalized learning. Expert tutors, live sessions, guaranteed results.",
      "headline": "Personalized {product[:25]} Plan",
      "cta": "Get Started",
      "image_query": "{product} personalized learning technology"
    }},
    {{
      "name": "Retargeting - Urgency",
      "objective": "Conversion",
      "custom_audience": "Website visitors last 30 days",
      "retargeting_window": "30 days",
      "budget_split": "25%",
      "placement": ["Facebook Feed","Instagram Stories","Messenger"],
      "primary_text": "You visited us but haven't started yet. Only 8 spots remaining this month. Don't miss out on the batch that starts Monday.",
      "headline": "Only 8 Spots Left!",
      "cta": "Claim Your Spot",
      "image_query": "{product} urgency deadline last chance"
    }}
  ],
  "pixel_events": ["PageView","ViewContent","Lead","InitiateCheckout","Purchase","CompleteRegistration"],
  "ab_test": {{
    "week1": "Creative format: Single image vs Carousel — Test which drives more link clicks",
    "week2": "Audience: Interest targeting vs Lookalike — Compare cost per lead",
    "week3": "Copy angle: Emotional pain vs Logical features — Test which gets more conversions",
    "week4": "Scale winner by 20% budget, pause loser"
  }},
  "scaling_strategy": "When ROAS exceeds 3x or CPL drops 30% below target, increase budget by 20% every 3-5 days",
  "image_query": "{product} facebook instagram ad education"
}}"""

    raw = await call_groq(prompt, 2000)
    try:
        clean = re.sub(r'```json|```','',raw).strip()
        data = json.loads(clean)
        data['_unsplash_key'] = UNSPLASH_KEY
        for fmt in data.get('ad_formats', []):
            fmt['_img_query'] = fmt.get('image_query', product + ' education')
            if 'cards' in fmt:
                for card in fmt['cards']:
                    card['_img_query'] = card.get('image_query', product)
        for ads in data.get('ad_sets', []):
            ads['_img_query'] = ads.get('image_query', product)
        return data
    except Exception as e:
        return {"error": str(e), "raw": raw[:500], "_unsplash_key": UNSPLASH_KEY}


async def generate_image_prompts(keyword: str, angle: str) -> str:
    prompt = f"""Generate 3 realistic environment-based image prompts for ads about "{keyword}". Angle: {angle}.

IMAGE PROMPT 1 (Facebook/Instagram Feed 1:1 square):
Scene: [detailed real candid scene description]
Subject: [who is in the image]
Mood: [emotional tone]
Lighting: [natural/warm/dramatic]
Canva tip: [how to add text overlay]

IMAGE PROMPT 2 (Instagram Story 9:16 vertical):
Scene:
Subject:
Mood:
Lighting:
Canva tip:

IMAGE PROMPT 3 (Google Display 16:9 landscape):
Scene:
Subject:
Mood:
Lighting:
Canva tip:

CANVA DESIGN GUIDE:
Recommended font: [specific font name]
CTA button color: [hex code]
Text position: [where to place text]
Overlay opacity: [percentage]
Color palette: [3 hex codes]"""
    return await call_groq(prompt, 800)
