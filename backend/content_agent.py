from seo_agent import call_groq

async def generate_landing_page(keyword: str, style: str, persona: str = "student") -> str:
    style_guide = {
        "minimalist": "Clean, white space, minimal colors (black/white/one accent), Apple-like design language",
        "tech": "Dark mode, neon accents, futuristic feel, code-like typography, Matrix/tech aesthetic",
        "academic": "University/institution feel, navy/gold colors, formal but approachable, trust-focused"
    }
    style_desc = style_guide.get(style, style_guide["minimalist"])

    prompt = f"""You are an expert conversion copywriter. Generate a complete 6-section landing page for:

Keyword: "{keyword}"
Style: {style.upper()} — {style_desc}
Target Persona: {persona.upper()}

Write ALL 6 SECTIONS with full copy. Make it conversion-optimized and {persona}-focused.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 1: HERO (Above the Fold)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Headline (max 8 words, addresses primary pain point):
Sub-headline (max 20 words, presents the solution):
Primary CTA Button Text:
Supporting Trust Line (e.g. "Join 10,000+ students"):
Hero Image Description (environment-based, realistic, NO stock photo style):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 2: PAIN POINT GALLERY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Section Headline:
Card 1 - Title: | Description (15 words):
Card 2 - Title: | Description (15 words):
Card 3 - Title: | Description (15 words):
Card 4 - Title: | Description (15 words):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3: FEATURE/BENEFIT GRID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Section Headline:
Feature 1 - Icon: | Title: | Benefit description (20 words):
Feature 2 - Icon: | Title: | Benefit description (20 words):
Feature 3 - Icon: | Title: | Benefit description (20 words):
Feature 4 - Icon: | Title: | Benefit description (20 words):
Feature 5 - Icon: | Title: | Benefit description (20 words):
Feature 6 - Icon: | Title: | Benefit description (20 words):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 4: SOCIAL PROOF / TRUST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Section Headline:
Metric 1: [Number] + [What it means]
Metric 2: [Number] + [What it means]
Metric 3: [Number] + [What it means]
Testimonial 1 - Name: | Role: | Quote (30 words):
Testimonial 2 - Name: | Role: | Quote (30 words):
Testimonial 3 - Name: | Role: | Quote (30 words):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 5: COMPARISON TABLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Table Headline:
| Feature | Old Way | Our Solution |
|---------|---------|--------------|
[8 rows comparing old vs new approach]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 6: CLOSING CTA + FAQ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Closing Headline:
Closing Sub-text (20 words):
Final CTA Button:
Urgency Line (scarcity element):

FAQ (5 questions handling real objections):
Q1: | A1:
Q2: | A2:
Q3: | A3:
Q4: | A4:
Q5: | A5:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HUMAN-SCORE CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tone Verification: Does copy sound like a {persona} advisor? [Yes/Needs revision]
Readability Level: [Grade level]
Key Emotion Triggered: [Primary emotion this copy evokes]"""

    return await call_groq(prompt, 2000)

async def generate_blog_post(keyword: str, cluster_keywords: list, persona: str = "student") -> str:
    secondary = ", ".join(cluster_keywords) if cluster_keywords else f"how to {keyword}, best {keyword}, {keyword} benefits"

    prompt = f"""You are an expert SEO blog writer. Write a complete, publish-ready blog post.

PRIMARY KEYWORD: {keyword}
SECONDARY KEYWORDS: {secondary}
PERSONA: {persona}
TONE: Conversational advisor — sounds like a helpful {persona} mentor, NOT a robot

━━━ SEO META DATA ━━━
Title Tag (55-60 chars, includes keyword):
Meta Description (145-155 chars, includes keyword + CTA):
URL Slug:
Primary Keyword:
Secondary Keywords (5):
Reading Time:
Word Count Target: 1500+

━━━ FULL BLOG POST ━━━

[H1 - Main Title]

[INTRODUCTION - 150 words]
Hook sentence. Include primary keyword in first 100 words. Address {persona} pain point immediately.

[H2 - Section 1 Title]
[200 words of valuable content]

[H2 - Section 2 Title]
[200 words of valuable content]

[H2 - Section 3 Title]
[200 words of valuable content]

[H2 - Section 4 Title]
[200 words of valuable content]

[H2 - FAQ Section]
5 questions and detailed answers that {persona}s actually ask

[CONCLUSION - 100 words]
Summary + clear CTA

━━━ ON-PAGE SEO CHECKLIST ━━━
[10 specific on-page tasks for this post]

━━━ HUMAN-SCORE VERIFICATION ━━━
Perplexity Check: [Does each paragraph vary in structure? Yes/No]
{persona.capitalize()} Voice Check: [Reads like a {persona} advisor? Yes/No]
Keyword Density: [Primary keyword appears X times — within 1-2% range?]"""

    return await call_groq(prompt, 2000)
