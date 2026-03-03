"""
KINGMODE Ad Image Generator — Gemini API (Nano Banana 2)
Budget: <$3 total. Strategy: generate 6 images max.
  - 3 hero ads (FB, IG Feed, IG Story) 
  - 3 backup variations if budget allows
Estimated cost: ~$0.05-0.15/image = $0.30-0.90 total.
"""
import os
import sys
import base64
from io import BytesIO
from google import genai
from google.genai import types
from PIL import Image

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY")
if not API_KEY:
    print("ERROR: No Gemini API key found.")
    print("Set one of: GEMINI_API_KEY, GOOGLE_API_KEY, GOOGLE_GENERATIVE_AI_API_KEY")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUT, exist_ok=True)

MODELS = [
    "gemini-2.0-flash-preview-image-generation",
]

BRAND_CONTEXT = """You are creating a professional paid social media advertisement for Window Depot USA of Milwaukee, a top-rated home improvement company in SE Wisconsin.

BRAND RULES:
- Company: Window Depot USA of Milwaukee
- Colors: Dark navy blue (#0A1628) and gold (#D4AF37) are the brand colors
- The company rep is named Nate — friendly, professional, no-pressure
- 4.9 stars on Google with 1,000+ reviews, A+ BBB rated
- They offer Triple-Pane windows at Dual-Pane prices
- Current offer: FREE in-home estimate (price locked 1 year) + $500 Gift Card
- Services: Windows, Doors, Siding, Roofing, Flooring, Bathroom Remodels
- Phone: (414) 312-5213
- Landing page: wdusa-nate-landing.vercel.app
- Style: Premium, trustworthy, local family business feel
- The ad must look like a real, professional paid advertisement — not AI-generated clip art

CRITICAL: Generate a photorealistic, high-quality marketing image. It should look like it was shot by a professional photographer and designed by a professional graphic designer. Clean composition, strong visual hierarchy, readable text. Do NOT include any people or faces in the image."""


def generate_image(prompt, filename, retries=2):
    """Generate a single image, trying available models with retry logic."""
    full_prompt = f"{BRAND_CONTEXT}\n\n{prompt}"
    
    for model in MODELS:
        for attempt in range(retries):
            try:
                print(f"  Generating with {model} (attempt {attempt+1})...")
                response = client.models.generate_content(
                    model=model,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=["TEXT", "IMAGE"],
                    ),
                )
                
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        img = Image.open(BytesIO(part.inline_data.data))
                        path = os.path.join(OUT, filename)
                        img.save(path, quality=95)
                        print(f"  Saved: {path} ({img.size[0]}x{img.size[1]})")
                        return path
                    if part.text:
                        print(f"  Model text: {part.text[:200]}")
                
                print(f"  No image in response, retrying...")
            except Exception as e:
                print(f"  Error with {model}: {e}")
                if attempt < retries - 1:
                    print(f"  Retrying...")
                continue
    
    print(f"  FAILED to generate {filename}")
    return None


def main():
    print("=" * 60)
    print("KINGMODE Ad Generator — Gemini API")
    print("Window Depot USA of Milwaukee")
    print("Budget target: <$3 (est. ~$0.50 for 6 images)")
    print("=" * 60)
    
    ads = [
        {
            "name": "Facebook Feed Ad (1200x628)",
            "file": "fb_ad_hero_gemini.png",
            "prompt": """Create a professional Facebook advertisement image (landscape orientation, 16:9 aspect ratio).

SCENE: A beautiful Craftsman-style Milwaukee home exterior at golden hour. New white triple-pane windows with warm golden interior light glowing through them. Manicured front yard, mature trees, classic Wisconsin neighborhood feel. No people in the image.

TEXT OVERLAYS (must be crisp, readable, professionally typeset):
- Top-left bold headline in white: "YOUR WINDOWS ARE COSTING YOU MONEY"
- Below in gold (#D4AF37): "Triple-Pane at Dual-Pane Prices"
- Three bullet points in white: "✓ Save up to 30% on Energy Bills" / "✓ FREE Estimate — Price Locked 1 Year" / "✓ $500 Gift Card with Every Appointment"
- Bottom navy banner spanning full width with: "WINDOW DEPOT USA of MILWAUKEE" on left, "Book FREE Estimate → wdusa-nate-landing.vercel.app" on right
- Thin gold line above bottom banner

STYLE: Premium real estate photography quality. Warm, inviting, aspirational. High contrast text for mobile readability. No people."""
        },
        {
            "name": "Instagram Feed Ad (1:1 Square)",
            "file": "ig_feed_ad_hero_gemini.png",
            "prompt": """Create a professional Instagram advertisement image (square 1:1 aspect ratio).

SCENE: Stunning modern living room interior with large new triple-pane windows. Warm natural light streaming in. Hardwood floors, tasteful furniture, cozy Wisconsin home feel. Green trees visible outside. No people in the image.

TEXT OVERLAYS (must be crisp, large, high-contrast for mobile):
- Very top: Small gold text "WINDOW DEPOT USA OF MILWAUKEE"
- Large bold white headline centered: "STOP PAYING FOR DRAFTY WINDOWS"
- Gold divider line
- Below: "Triple-Pane at Dual-Pane Prices" in white
- Three gold checkmark bullets: "✓ Save up to 30% on energy bills" / "✓ FREE estimate — locked for 1 full year" / "✓ $500 Gift Card included"
- Bottom gold (#D4AF37) banner: "Book FREE Estimate → wdusa-nate-landing.vercel.app" in navy text, "(414) 312-5213" large below

STYLE: Scroll-stopping, bold typography, dark navy background with warm photo. Magazine-quality interior photography. No people."""
        },
        {
            "name": "Instagram Story Ad (9:16 Vertical)",
            "file": "ig_story_ad_hero_gemini.png",
            "prompt": """Create a professional Instagram Stories advertisement (vertical 9:16 portrait orientation).

SCENE: Dramatic twilight/dusk photo of a beautiful Wisconsin home exterior. New windows glow warmly from inside against a dusky blue sky. Spring landscaping, dramatic lighting. Shot from slight low angle. No people.

TEXT OVERLAYS (large, bold, vertical-optimized for mobile):
- Top: "WINDOW DEPOT USA OF MILWAUKEE" small gold text with gold line below
- Center: Massive stacked headline "YOUR ENERGY BILLS ARE TOO HIGH" in bold white, one word per line, "TOO HIGH" in gold
- Middle: Semi-transparent dark card with gold border: "TRIPLE-PANE WINDOWS / at Dual-Pane Prices / SAVE UP TO 30%"
- Below card: "★ FREE In-Home Estimate" / "★ Price Locked 1 Year" / "★ $500 Gift Card" in white
- Large gold rounded button: "BOOK WITH NATE"
- Below button: "(414) 312-5213" in white
- Very bottom: "wdusa-nate-landing.vercel.app" in gold, "Swipe Up ↑"

STYLE: Cinematic, dramatic lighting, premium home exterior photography. Thumb-stopping vertical impact. No people."""
        },
    ]
    
    results = []
    for i, ad in enumerate(ads):
        print(f"\n[{i+1}/{len(ads)}] {ad['name']}")
        path = generate_image(ad["prompt"], ad["file"])
        results.append({"name": ad["name"], "file": ad["file"], "path": path})
    
    print("\n" + "=" * 60)
    print("RESULTS:")
    for r in results:
        status = "✅" if r["path"] else "❌"
        print(f"  {status} {r['name']}: {r['path'] or 'FAILED'}")
    
    successful = sum(1 for r in results if r["path"])
    print(f"\n{successful}/{len(results)} images generated successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()
