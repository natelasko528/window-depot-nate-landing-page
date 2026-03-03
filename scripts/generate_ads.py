import os
import json
import time
from google import genai
from PIL import Image
from io import BytesIO

client = genai.Client(api_key=os.environ.get("Gemini API Key"))

MODEL = "gemini-3.1-flash-image-preview"

AD_COPY = {
    "facebook": [
        {
            "id": "FB-01",
            "angle": "Energy Savings",
            "headline": "Cut Energy Bills Up to 40%",
            "primary_text": "Wisconsin winters hit hard — and your old windows are letting heat (and money) escape. Window Depot USA of Milwaukee offers triple-pane windows at dual-pane prices. Backed by US Dept. of Energy RESFEN data, not empty promises. Get your FREE in-home estimate + $500 gift card. Price locked for 12 months.",
            "description": "Triple Pane. Real Savings.",
            "cta": "Get Free Estimate"
        },
        {
            "id": "FB-02",
            "angle": "Trust / Social Proof",
            "headline": "4.9 Stars. 1,000+ Reviews.",
            "primary_text": "Over a thousand SE Wisconsin homeowners trust Window Depot USA — and they're not shy about saying so. Rated #3 nationally by Qualified Remodeler. A+ BBB. Your neighbors chose us for a reason. Book your FREE zero-pressure estimate with Nate and see why.",
            "description": "Milwaukee's Most Trusted.",
            "cta": "Book Free Estimate"
        },
        {
            "id": "FB-03",
            "angle": "Seasonal Urgency (Spring)",
            "headline": "Spring Is Here — Upgrade Now",
            "primary_text": "Spring is the perfect time to replace those drafty windows before another Wisconsin summer and winter cycle. Right now, get a FREE in-home estimate + a $500 gift card from Window Depot USA of Milwaukee. Triple-pane windows at dual-pane prices. Your quote is locked for a full year — zero risk.",
            "description": "Free Estimate + $500 Gift Card",
            "cta": "Schedule Now"
        },
        {
            "id": "FB-04",
            "angle": "Comfort / Home Improvement",
            "headline": "Feel the Difference Inside",
            "primary_text": "No more cold spots by the windows. No more condensation. No more cranking the thermostat. Window Depot USA's triple-pane windows keep your Milwaukee home comfortable year-round — warmer winters, cooler summers, quieter rooms. Custom-made for your exact home. FREE estimate, no pressure.",
            "description": "Comfort You Can Feel.",
            "cta": "Get Started"
        },
        {
            "id": "FB-05",
            "angle": "Curb Appeal / Value",
            "headline": "Transform Your Home's Look",
            "primary_text": "New windows, doors, or siding can completely transform your home's curb appeal — and boost its value. Window Depot USA of Milwaukee offers ProVia products rated #1 in quality. 7 showrooms across SE Wisconsin. Book a FREE consultation with Nate and get a $500 gift card just for meeting.",
            "description": "ProVia Quality. Local Service.",
            "cta": "Free Consultation"
        },
    ],
    "instagram": [
        {
            "id": "IG-01",
            "angle": "Energy Savings",
            "caption": "Your old windows are costing you more than you think. \u2744\ufe0f\n\nTriple-pane windows at dual-pane prices. That's the Window Depot USA difference.\n\nWe don't just promise energy savings — we prove it with US Dept. of Energy data. Milwaukee homeowners save 12-40% on energy bills.\n\nFREE estimate + $500 gift card \ud83d\udc47\nLink in bio or call Nate: (414) 312-5213",
            "hashtags": "#WindowDepotUSA #MilwaukeeHome #TriplePaneWindows #EnergySavings #WisconsinHomeowner #HomeImprovement #ReplacementWindows #MilwaukeeWI #SEWisconsin #CurbAppeal"
        },
        {
            "id": "IG-02",
            "angle": "Before/After Transformation",
            "caption": "The transformation is real. \ud83c\udfe0\u2728\n\nNew windows don't just save energy — they change how your entire home feels. More light. Less noise. Zero drafts.\n\n4.9 stars \u2b50 | 1,000+ reviews | #3 national remodeler\n\nYour quote is locked for 12 months. No pressure. No gimmicks.\n\nBook your FREE in-home estimate today \ud83d\udc47",
            "hashtags": "#HomeTransformation #BeforeAndAfter #WindowReplacement #MilwaukeeHomes #ProVia #HomeUpgrade #WisconsinLiving #EnergyEfficient #HomeMakeover #WindowDepotMilwaukee"
        },
        {
            "id": "IG-03",
            "angle": "Family / Trust",
            "caption": "We're not a faceless corporation. We're your neighbors. \ud83e\udd1d\n\nNate and his family have been serving SE Wisconsin homeowners for over a decade. No pushy sales. No gimmicks. Just honest advice and the best windows in the business.\n\nTriple-pane at dual-pane prices. Price locked for a year.\n\nText Nate: (414) 312-5213",
            "hashtags": "#FamilyBusiness #MilwaukeeBusiness #LocalBusiness #TrustWorthy #HomeImprovement #WindowDepotUSA #SEWisconsin #SupportLocal #HomeSweetHome #WisconsinFamily"
        },
        {
            "id": "IG-04",
            "angle": "Spring Seasonal",
            "caption": "Spring cleaning? Start with your windows. \ud83c\udf37\n\nThose old, foggy, drafty windows aren't just an eyesore — they're driving up your energy bills. Spring is the perfect time to upgrade.\n\n\u2705 Free in-home estimate\n\u2705 $500 gift card\n\u2705 Price locked 12 months\n\u2705 Triple-pane at dual-pane prices\n\nBook now \ud83d\udc47 Link in bio",
            "hashtags": "#SpringUpgrade #SpringHomeImprovement #MilwaukeeSpring #NewWindows #HomeRenovation #WindowDepotUSA #FreeEstimate #WisconsinHome #EnergyEfficiency #SmartHome"
        },
        {
            "id": "IG-05",
            "angle": "Product Showcase",
            "caption": "America's Triple Pane Company. \ud83c\uddfa\ud83c\uddf8\n\nWhy do we push triple-pane so hard? Because the difference is massive:\n\n\ud83d\udd39 Up to 52% better insulation than dual-pane\n\ud83d\udd39 Superior sound reduction\n\ud83d\udd39 Drastically less condensation\n\ud83d\udd39 Custom-made for YOUR home\n\nAnd we offer it at dual-pane prices. No one else can say that.\n\n7 showrooms across SE WI \ud83d\udccd",
            "hashtags": "#TriplePane #WindowTechnology #EnergyStarWindows #ProViaWindows #AmericasTriplePaneCompany #MilwaukeeWI #HomeExpert #WindowUpgrade #SmartInvestment #QualityMatters"
        },
    ],
    "instagram_stories": [
        {
            "id": "IGS-01",
            "angle": "Quick CTA",
            "text": "FREE estimate + $500 gift card \ud83c\udf81\n\nTriple-pane windows\nDual-pane prices\n\nSwipe up or call Nate\n(414) 312-5213",
        },
        {
            "id": "IGS-02",
            "angle": "Social Proof",
            "text": "4.9 \u2b50 on Google\n1,000+ reviews\n#3 National Remodeler\n\nMilwaukee trusts Window Depot USA\n\nBook your FREE estimate \u2192",
        },
        {
            "id": "IGS-03",
            "angle": "Seasonal Push",
            "text": "Spring = window season \ud83c\udf3b\n\nDon't waste another summer\nwith drafty windows\n\nFREE estimate\nPrice locked 12 months\n\nTap to book \u2192",
        },
    ]
}

IMAGE_PROMPTS = {
    "fb_energy_savings": {
        "filename": "ad-drafts/facebook/fb_01_energy_savings.png",
        "prompt": (
            "Professional marketing advertisement photograph for a window replacement company. "
            "Split composition: left side shows an old, foggy, frost-covered single-pane window "
            "with visible cold drafts and condensation on a gray winter day. Right side shows a "
            "beautiful modern triple-pane window with warm golden interior lighting, a cozy living "
            "room visible inside, and snow outside. The contrast between old and new is dramatic. "
            "Clean, high-contrast, professional real estate photography style. "
            "Landscape orientation 16:9 aspect ratio. No text overlays."
        )
    },
    "fb_trust_reviews": {
        "filename": "ad-drafts/facebook/fb_02_trust_reviews.png",
        "prompt": (
            "Professional marketing photograph showing a beautiful, well-maintained Milwaukee "
            "suburban home exterior with brand new modern replacement windows, pristine siding, "
            "and a manicured lawn. The home looks warm and inviting. Golden hour lighting. "
            "A friendly homeowner family (man, woman, and child) standing proudly in front of "
            "their renovated home, smiling naturally. Real estate photography style, aspirational, "
            "warm Midwest suburban feel. Landscape orientation 16:9. No text overlays."
        )
    },
    "fb_spring_seasonal": {
        "filename": "ad-drafts/facebook/fb_03_spring_seasonal.png",
        "prompt": (
            "Professional advertisement photograph of a charming Milwaukee-style craftsman home "
            "in spring. Cherry blossom trees blooming in the front yard, green grass, blue sky "
            "with soft clouds. The home features beautiful new modern replacement windows that "
            "catch the spring sunlight. Flowers in window boxes. Fresh, vibrant, optimistic mood. "
            "Real estate photography, aspirational spring scene. Landscape 16:9. No text overlays."
        )
    },
    "fb_comfort": {
        "filename": "ad-drafts/facebook/fb_04_comfort.png",
        "prompt": (
            "Professional interior photograph of a beautiful modern living room in a Milwaukee home "
            "during winter. Large triple-pane replacement windows showing a snowy landscape outside. "
            "Inside is warm and cozy: soft lighting, comfortable furniture, a hot cup of coffee on "
            "the windowsill. The windows are crystal clear with zero condensation despite the cold "
            "outside. Warm color palette, inviting, professional interior photography. "
            "Landscape 16:9 aspect ratio. No text overlays."
        )
    },
    "fb_curb_appeal": {
        "filename": "ad-drafts/facebook/fb_05_curb_appeal.png",
        "prompt": (
            "Professional exterior photograph of a stunning home exterior renovation featuring new "
            "ProVia windows, a beautiful fiberglass entry door, and fresh vinyl siding. The home "
            "is a classic Midwest style updated with modern touches. Lush landscaping, driveway, "
            "warm sunset lighting creating beautiful shadows and highlights on the new exterior. "
            "Dramatic curb appeal transformation. Real estate photography style. "
            "Landscape 16:9 aspect ratio. No text overlays."
        )
    },
    "ig_energy": {
        "filename": "ad-drafts/instagram/ig_01_energy_savings.png",
        "prompt": (
            "Professional square-format photograph for social media. Close-up of a beautiful "
            "modern triple-pane replacement window from inside a cozy home. Through the window, "
            "a snowy Wisconsin winter scene is visible. Inside, the room is warm with golden "
            "lighting. A hand touches the glass showing it's warm despite the cold outside. "
            "Clean, crisp, professional product photography with aspirational lifestyle feel. "
            "Square 1:1 aspect ratio. No text overlays."
        )
    },
    "ig_transformation": {
        "filename": "ad-drafts/instagram/ig_02_transformation.png",
        "prompt": (
            "Professional square photograph showing a dramatic home exterior transformation. "
            "Side-by-side or before/after feel: a beautiful Milwaukee home with gleaming new "
            "windows, fresh siding, and a stunning entry door. The renovation is complete and "
            "the home looks brand new. Perfect landscaping, blue sky, golden sunlight. "
            "Aspirational, clean, modern but classic Midwest charm. "
            "Square 1:1 aspect ratio. No text overlays."
        )
    },
    "ig_family": {
        "filename": "ad-drafts/instagram/ig_03_family_trust.png",
        "prompt": (
            "Professional photograph of a friendly, approachable home improvement consultant "
            "showing window samples to a happy homeowner couple at their dining table. The scene "
            "is warm, natural, and genuine — not staged or corporate. Bright, well-lit home "
            "interior. The consultant is dressed casually-professional. Everyone is smiling and "
            "engaged. Authentic, trust-building imagery. "
            "Square 1:1 aspect ratio. No text overlays."
        )
    },
    "ig_spring": {
        "filename": "ad-drafts/instagram/ig_04_spring.png",
        "prompt": (
            "Professional square photograph of an open casement window on a beautiful spring day. "
            "Fresh spring breeze flowing through sheer curtains. View of a blooming garden and "
            "green lawn through the open window. Bright, fresh, optimistic spring mood. "
            "The window is modern, clean, white-framed triple-pane. Interior has fresh flowers "
            "on the windowsill. Lifestyle photography, aspirational. "
            "Square 1:1 aspect ratio. No text overlays."
        )
    },
    "ig_product": {
        "filename": "ad-drafts/instagram/ig_05_product_showcase.png",
        "prompt": (
            "Professional product photography of a cross-section cutaway showing the technology "
            "inside a triple-pane window. Three glass panes visible with gas-filled chambers "
            "between them, Low-E coatings shown as subtle blue/purple reflective layers, thermal "
            "spacers, and solid vinyl frame. Clean white background, studio lighting, "
            "technical but beautiful product visualization. Educational feel. "
            "Square 1:1 aspect ratio. No text overlays."
        )
    },
    "igs_cta": {
        "filename": "ad-drafts/instagram-stories/igs_01_cta.png",
        "prompt": (
            "Professional vertical photograph for Instagram Stories. A beautiful modern home "
            "at golden hour with stunning new replacement windows glowing with warm interior "
            "light. The sky is dramatic sunset colors. The home exterior is immaculate. "
            "Portrait/vertical orientation 9:16 aspect ratio. Aspirational, dramatic, clean. "
            "Real estate photography style. No text overlays."
        )
    },
    "igs_reviews": {
        "filename": "ad-drafts/instagram-stories/igs_02_reviews.png",
        "prompt": (
            "Professional vertical photograph for Instagram Stories. Interior of a gorgeous "
            "renovated Milwaukee home featuring floor-to-ceiling modern windows overlooking "
            "a winter landscape. The interior is warm, modern, and beautifully furnished. "
            "The windows are the clear hero of the shot. Warm, inviting, luxurious feel. "
            "Portrait/vertical 9:16 aspect ratio. No text overlays."
        )
    },
    "igs_seasonal": {
        "filename": "ad-drafts/instagram-stories/igs_03_seasonal.png",
        "prompt": (
            "Professional vertical photograph for Instagram Stories. A charming home exterior "
            "in spring with blooming flowers, green trees, and beautiful new windows reflecting "
            "the blue sky. Fresh, vibrant, energetic spring mood. The home looks perfectly "
            "maintained with new windows as the focal point. "
            "Portrait/vertical 9:16 aspect ratio. No text overlays."
        )
    },
}


def generate_image(prompt_key, prompt_data, retries=2):
    filepath = os.path.join("/workspace", prompt_data["filename"])
    if os.path.exists(filepath):
        print(f"  [SKIP] {filepath} already exists")
        return True

    for attempt in range(retries + 1):
        try:
            print(f"  [GEN] {prompt_key} (attempt {attempt+1})...")
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt_data["prompt"],
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    image = Image.open(BytesIO(part.inline_data.data))
                    image.save(filepath, "PNG")
                    print(f"  [OK]  Saved: {filepath} ({image.size[0]}x{image.size[1]})")
                    return True

            print(f"  [WARN] No image data in response for {prompt_key}")
            if attempt < retries:
                time.sleep(3)

        except Exception as e:
            print(f"  [ERR] {prompt_key}: {e}")
            if attempt < retries:
                time.sleep(5)

    return False


def main():
    print("=" * 60)
    print("WINDOW DEPOT USA — AD CAMPAIGN BULK GENERATOR")
    print("Using Nano Banana 2 (Gemini 3.1 Flash Image)")
    print("=" * 60)

    copy_path = "/workspace/ad-drafts/ad_copy.json"
    with open(copy_path, "w", encoding="utf-8") as f:
        json.dump(AD_COPY, f, indent=2, ensure_ascii=True)
    print(f"\n[COPY] Ad copy saved to {copy_path}")

    print(f"\n[IMAGES] Generating {len(IMAGE_PROMPTS)} ad images...\n")
    results = {"success": [], "failed": []}

    for key, data in IMAGE_PROMPTS.items():
        ok = generate_image(key, data)
        if ok:
            results["success"].append(key)
        else:
            results["failed"].append(key)
        time.sleep(2)

    print("\n" + "=" * 60)
    print(f"RESULTS: {len(results['success'])} succeeded, {len(results['failed'])} failed")
    if results["failed"]:
        print(f"Failed: {', '.join(results['failed'])}")
    print("=" * 60)

    return results


if __name__ == "__main__":
    main()
