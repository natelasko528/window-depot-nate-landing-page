#!/usr/bin/env python3
"""
GHL Social Planner — Create Draft Posts (v2)
=============================================
Creates 18 draft posts for the RevolutionAi Marketing Group
(Facebook, Instagram, LinkedIn) modeled on previously published
Window Depot posts pulled from GHL as reference.

Captions mirror the style, format, and voice of the best-performing
published posts (bold unicode headers, ✅ bullets, Nate's voice,
$500 gift card CTA, phone + URL).

Media re-uses existing CDN URLs already in GHL — no new uploads.

All posts use status:"draft" — nothing auto-publishes.
Review at: https://app.gohighlevel.com/location/Rkjt05VeS56IUr5caLBD/social-planner

Run:
  python3 scripts/create_ghl_drafts.py
"""

import os
import sys
import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

GHL_API_TOKEN   = os.environ.get("GHL_API_TOKEN")
GHL_LOCATION_ID = os.environ.get("GHL_LOCATION_ID")
USER_ID         = "5x0U1s3UwojNVv9aK78P"   # Nate Lasko

BASE_URL = "https://services.leadconnectorhq.com"
HEADERS  = {
    "Authorization": f"Bearer {GHL_API_TOKEN}",
    "Version": "2021-07-28",
    "Content-Type": "application/json",
}

CDN = "https://assets.cdn.filesafe.space/Rkjt05VeS56IUr5caLBD/media"

# RevolutionAi Marketing Group — account IDs
FACEBOOK  = "69338440ffbf8adc5de6ef3e_Rkjt05VeS56IUr5caLBD_999513493239724_page"
INSTAGRAM = "69338466e84b5e031adc0e6b_Rkjt05VeS56IUr5caLBD_17841428950943404"
LINKEDIN  = "69338480b97205c2da5810ab_Rkjt05VeS56IUr5caLBD_ppTjrCc6FX_profile"

# Existing CDN assets (already uploaded, no re-upload needed)
IMG = {
    # Windows
    "win_fb":  {"url": f"{CDN}/c71827d7-de42-46a3-84c1-df49cf601887.png",     "type": "image/png"},
    "win_ig":  {"url": f"{CDN}/dbedb3a2-6905-4a34-af21-31e61c3ac9a5.png",     "type": "image/png"},
    "win_li":  {"url": f"{CDN}/7d19e489-095a-48fb-8c29-e3b14904746d.png",     "type": "image/png"},
    # Doors
    "door_fb": {"url": f"{CDN}/bef69a81-cf56-45c4-901d-031014e24f7c.png",     "type": "image/png"},
    "door_ig": {"url": f"{CDN}/0d7bad0b-7c94-49fb-9477-4ce60559a5b3.png",     "type": "image/png"},
    "door_li": {"url": f"{CDN}/8a970467-3d01-4185-a417-936c51f3e9e4.png",     "type": "image/png"},
    # Siding / Roofing / Flooring / Bathrooms — existing service videos
    "siding":  {"url": f"{CDN}/37e574a1-f977-46b9-83de-f76073eb8fc9.mp4",    "type": "video/mp4"},
    "roofing": {"url": f"{CDN}/26a67e41-acdf-44e6-a533-f8465512741e.mp4",    "type": "video/mp4"},
    "floor":   {"url": f"{CDN}/91283598-5294-4083-bf12-abcbff4d7a52.mp4",    "type": "video/mp4"},
    "bath":    {"url": f"{CDN}/e62e77e3-c544-4608-b572-99447e440c65.mp4",    "type": "video/mp4"},
}

# ---------------------------------------------------------------------------
# Post content — 18 posts: 6 services × 3 platforms
# Captions modeled on best-performing published posts:
#   • Bold unicode opener  • Personal Nate voice  • ✅ bullet benefits
#   • 🎁 offer / CTA      • 📲 phone + 🌐 URL    • Hashtags
# ---------------------------------------------------------------------------

POSTS = [

    # ── WINDOWS ────────────────────────────────────────────────────────────

    {
        "label":    "Windows — Facebook",
        "account":  FACEBOOK,
        "media":    IMG["win_fb"],
        "caption":  (
            "𝗬𝗼𝘂𝗿 𝘄𝗶𝗻𝗱𝗼𝘄𝘀 𝗮𝗿𝗲 𝘄𝗼𝗿𝗸𝗶𝗻𝗴 𝗮𝗴𝗮𝗶𝗻𝘀𝘁 𝘆𝗼𝘂 𝗿𝗶𝗴𝗵𝘁 𝗻𝗼𝘄. 🪟\n\n"
            "I'm Nate with Window Depot USA of Milwaukee — and I want to come to YOUR home, show you what "
            "triple-pane technology actually looks and feels like, and give you a FREE estimate that's "
            "locked in for a full 12 months. No pressure. No expiration. Just honest pricing.\n\n"
            "✅ ProVia® Triple Pane — up to 30% lower energy bills\n"
            "✅ Eliminates drafts, condensation & cold spots\n"
            "✅ Installed in 1 day by our crew\n"
            "✅ Lifetime warranty, A+ BBB, 4.9★ Google\n"
            "🎁 $𝟱𝟬𝟬 𝗚𝗶𝗳𝘁 𝗖𝗮𝗿𝗱 𝘄𝗶𝘁𝗵 𝗲𝘃𝗲𝗿𝘆 𝗲𝘀𝘁𝗶𝗺𝗮𝘁𝗲 𝗯𝗼𝗼𝗸𝗲𝗱!\n\n"
            "📲 Text or call me: (414) 312-5213\n"
            "🌐 https://wdusa-nate-landing.vercel.app/#booking\n\n"
            "#WindowDepotMilwaukee #ReplacementWindows #TriplePaneWindows "
            "#MilwaukeeHomes #FreeEstimate #WeCreateHappyCustomers #Wisconsin"
        ),
    },
    {
        "label":    "Windows — Instagram",
        "account":  INSTAGRAM,
        "media":    IMG["win_ig"],
        "caption":  (
            "Drafty windows? Fogged glass? Heating bill through the roof? I can fix all three. 🪟❄️\n\n"
            "I'm Nate — your local Window Depot rep in SE Wisconsin. "
            "When you book directly with me your estimate is LOCKED IN for 1 full year.\n\n"
            "✅ ProVia® Triple Pane windows\n"
            "✅ Energy Star certified\n"
            "✅ Installed in 1 day\n"
            "✅ Lifetime warranty\n"
            "🎁 $500 Gift Card included with every estimate!\n\n"
            "📲 (414) 312-5213\n"
            "🌐 Link in bio to book\n\n"
            "#WindowDepot #Milwaukee #NewWindows #EnergyEfficient #BookWithNate "
            "#FreeEstimate #MilwaukeeHomes #TriplePaneWindows #Wisconsin #HomeImprovement "
            "#ReplacementWindows #WindowReplacement #MilwaukeeWI #SEWisconsin #WeCreateHappyCustomers"
        ),
    },
    {
        "label":    "Windows — LinkedIn",
        "account":  LINKEDIN,
        "media":    IMG["win_li"],
        "caption":  (
            "𝗠𝗶𝗹𝘄𝗮𝘂𝗸𝗲𝗲-𝗮𝗿𝗲𝗮 𝗵𝗼𝗺𝗲𝗼𝘄𝗻𝗲𝗿𝘀 — 𝗜'𝗺 𝗻𝗼𝘄 𝗯𝗼𝗼𝗸𝗶𝗻𝗴 𝗳𝗿𝗲𝗲 𝗶𝗻-𝗵𝗼𝗺𝗲 𝘄𝗶𝗻𝗱𝗼𝘄 𝗰𝗼𝗻𝘀𝘂𝗹𝘁𝗮𝘁𝗶𝗼𝗻𝘀.\n\n"
            "I represent Window Depot USA of Milwaukee — one of the fastest-growing home improvement "
            "companies in SE Wisconsin. We install ProVia® Endure Triple Pane windows that reduce "
            "heating and cooling costs by up to 30%, eliminate drafts, and increase your home's value.\n\n"
            "Book directly with me and your estimate is valid for a full 12 months — no pressure, no games.\n\n"
            "📊 Up to 30% energy savings\n"
            "🏆 Qualified Remodeler Top 500 — Ranked #3 Nationally\n"
            "⭐ 4.9 Google Rating | A+ BBB | 1,000+ reviews\n"
            "📍 7 showrooms across SE Wisconsin\n\n"
            "🎁 𝗕𝗼𝗼𝗸 𝗬𝗼𝘂𝗿 𝗙𝗥𝗘𝗘 𝗖𝗼𝗻𝘀𝘂𝗹𝘁𝗮𝘁𝗶𝗼𝗻 𝗮𝗻𝗱 𝗚𝗲𝘁 $𝟱𝟬𝟬 𝗢𝗙𝗙 𝗬𝗢𝗨𝗥 𝗘𝗦𝗧𝗜𝗠𝗔𝗧𝗘 𝗧𝗼𝗱𝗮𝘆!\n\n"
            "📲 (414) 312-5213\n"
            "🌐 https://wdusa-nate-landing.vercel.app/#booking\n\n"
            "#HomeImprovement #Milwaukee #ReplacementWindows #HomeValue "
            "#EnergyEfficiency #WeCreateHappyCustomers #Wisconsin"
        ),
    },

    # ── DOORS ──────────────────────────────────────────────────────────────

    {
        "label":    "Doors — Facebook",
        "account":  FACEBOOK,
        "media":    IMG["door_fb"],
        "caption":  (
            "𝗜𝘀 𝘆𝗼𝘂𝗿 𝗳𝗿𝗼𝗻𝘁 𝗱𝗼𝗼𝗿 𝗹𝗲𝘁𝘁𝗶𝗻𝗴 𝗶𝗻 𝗰𝗼𝗹𝗱 𝗮𝗶𝗿 — 𝗼𝗿 𝗷𝘂𝘀𝘁 𝗹𝗼𝗼𝗸𝗶𝗻𝗴 𝘁𝗶𝗿𝗲𝗱? 🚪\n\n"
            "I'm Nate with Window Depot USA Milwaukee, and I'm booking FREE in-home door consultations "
            "across SE Wisconsin. I'll bring samples directly to your home and show you our full lineup "
            "of ProVia® Signet® fiberglass and Legacy® steel entry and patio doors.\n\n"
            "Book with me and your estimate is 𝗹𝗼𝗰𝗸𝗲𝗱 𝗶𝗻 𝗳𝗼𝗿 𝟭 𝗙𝗨𝗟𝗟 𝗬𝗘𝗔𝗥.\n\n"
            "✅ Fiberglass & steel options\n"
            "✅ Custom colors & styles\n"
            "✅ Energy-efficient & weather-tight\n"
            "✅ Lifetime warranty\n"
            "🎁 $𝟱𝟬𝟬 𝗚𝗶𝗳𝘁 𝗖𝗮𝗿𝗱 𝗜𝗳 𝗬𝗼𝘂 𝗕𝗼𝗼𝗸 𝗧𝗼𝗱𝗮𝘆!\n\n"
            "📲 (414) 312-5213\n"
            "🌐 https://wdusa-nate-landing.vercel.app/#booking\n\n"
            "#WindowDepotMilwaukee #NewFrontDoor #EntryDoor #PatioDoor "
            "#MilwaukeeHomes #FreeEstimate #CurbAppeal #WeCreateHappyCustomers"
        ),
    },
    {
        "label":    "Doors — Instagram",
        "account":  INSTAGRAM,
        "media":    IMG["door_ig"],
        "caption":  (
            "𝙔𝙤𝙪𝙧 𝙛𝙧𝙤𝙣𝙩 𝙙𝙤𝙤𝙧 𝙞𝙨 𝙩𝙝𝙚 𝙛𝙞𝙧𝙨𝙩 𝙩𝙝𝙞𝙣𝙜 𝙥𝙚𝙤𝙥𝙡𝙚 𝙨𝙚𝙚. 𝙈𝙖𝙠𝙚 𝙞𝙩 𝙨𝙩𝙪𝙣𝙣𝙞𝙣𝙜. 🚪✨\n\n"
            "Book directly with me — Nate, your Window Depot rep in SE Wisconsin. "
            "I'll come to you with samples and your FREE estimate is price-locked for 1 full year.\n\n"
            "✅ ProVia® fiberglass & steel\n"
            "✅ Custom colors & hardware\n"
            "✅ Lifetime warranty\n"
            "🎁 $500 Gift Card with every estimate!\n\n"
            "📲 (414) 312-5213\n"
            "🌐 Link in bio to book\n\n"
            "#NewDoor #HomeUpgrade #Milwaukee #BookWithNate #WindowDepot "
            "#FreeEstimate #CurbAppeal #EntryDoor #Wisconsin #HomeImprovement "
            "#PatioDoor #MilwaukeeHomes #ProVia #WeCreateHappyCustomers #SEWisconsin"
        ),
    },
    {
        "label":    "Doors — LinkedIn",
        "account":  LINKEDIN,
        "media":    IMG["door_li"],
        "caption":  (
            "𝗗𝗼𝗼𝗿 𝗿𝗲𝗽𝗹𝗮𝗰𝗲𝗺𝗲𝗻𝘁 𝗰𝗼𝗻𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗹𝘆 𝗿𝗮𝗻𝗸𝘀 𝗮𝘀 𝗼𝗻𝗲 𝗼𝗳 𝘁𝗵𝗲 𝗵𝗶𝗴𝗵𝗲𝘀𝘁 𝗥𝗢𝗜 𝗵𝗼𝗺𝗲 𝗶𝗺𝗽𝗿𝗼𝘃𝗲𝗺𝗲𝗻𝘁𝘀 𝗳𝗼𝗿 𝗠𝗶𝗹𝘄𝗮𝘂𝗸𝗲𝗲-𝗮𝗿𝗲𝗮 𝗵𝗼𝗺𝗲𝗼𝘄𝗻𝗲𝗿𝘀.\n\n"
            "I'm Nate with Window Depot USA of Milwaukee. I offer free in-home consultations for "
            "ProVia® Signet® fiberglass and Legacy® steel entry doors — recognized as best-in-class "
            "for energy performance, security ratings, and durability in northern climates.\n\n"
            "Book directly with me and your estimate stays valid for 12 months.\n\n"
            "🏠 Locally owned | 7 SE Wisconsin showrooms\n"
            "⭐ A+ BBB | 4.9★ Google Rating\n"
            "🎁 $500 Gift Card with every estimate!\n\n"
            "📲 (414) 312-5213\n"
            "🌐 https://wdusa-nate-landing.vercel.app/#booking\n\n"
            "#EntryDoor #HomeImprovement #Milwaukee #ProVia "
            "#HomeValue #WeCreateHappyCustomers #Wisconsin"
        ),
    },

    # ── SIDING ─────────────────────────────────────────────────────────────

    {
        "label":    "Siding — Facebook",
        "account":  FACEBOOK,
        "media":    IMG["siding"],
        "caption":  (
            "𝗡𝗲𝘄 𝘀𝗶𝗱𝗶𝗻𝗴 𝗱𝗼𝗲𝘀 𝘁𝘄𝗼 𝘁𝗵𝗶𝗻𝗴𝘀 𝗮𝘁 𝗼𝗻𝗰𝗲 — 𝗯𝗼𝗼𝘀𝘁𝘀 𝗰𝘂𝗿𝗯 𝗮𝗽𝗽𝗲𝗮𝗹 𝗮𝗻𝗱 𝗽𝗿𝗼𝘁𝗲𝗰𝘁𝘀 𝘆𝗼𝘂𝗿 𝗵𝗼𝗺𝗲. 🏠\n\n"
            "I'm Nate with Window Depot USA of Milwaukee. We install premium CraneBoard, Market Square, "
            "and ASCEND composite cladding — products engineered for Wisconsin's freeze-thaw extremes "
            "and backed by warranties that actually mean something.\n\n"
            "✅ CraneBoard & ASCEND composite — premium durability\n"
            "✅ Dozens of colors & profiles\n"
            "✅ Reduces outside noise & moisture intrusion\n"
            "✅ Locally installed by our certified crew\n"
            "🎁 FREE in-home estimate + $500 Gift Card!\n\n"
            "📲 (414) 312-5213\n"
            "🌐 https://wdusa-nate-landing.vercel.app/#booking\n\n"
            "#WindowDepotMilwaukee #Siding #CurbAppeal #MilwaukeeHomes "
            "#HomeImprovement #FreeEstimate #WeCreateHappyCustomers #Wisconsin"
        ),
    },
    {
        "label":    "Siding — Instagram",
        "account":  INSTAGRAM,
        "media":    IMG["siding"],
        "caption":  (
            "Your home's exterior is working HARD every Wisconsin winter. Is your siding up to it? 🏡❄️\n\n"
            "I'm Nate — your Window Depot rep in SE Wisconsin. "
            "We install premium composite siding that stands up to anything the Midwest throws at it, "
            "and your FREE estimate is price-locked for 12 months.\n\n"
            "✅ CraneBoard & ASCEND composite\n"
            "✅ Custom colors & styles\n"
            "✅ Certified local installation\n"
            "🎁 $500 Gift Card with every estimate!\n\n"
            "📲 (414) 312-5213\n"
            "🌐 Link in bio to book\n\n"
            "#NewSiding #HomeExterior #MilwaukeeHomes #CurbAppeal #WindowDepot "
            "#FreeEstimate #Wisconsin #HomeImprovement #BookWithNate #SEWisconsin "
            "#CompositeSiding #HomeRenovation #WeCreateHappyCustomers #MilwaukeeWI #SidingReplacement"
        ),
    },
    {
        "label":    "Siding — LinkedIn",
        "account":  LINKEDIN,
        "media":    IMG["siding"],
        "caption":  (
            "New siding transforms your home's look and adds a protective barrier against Wisconsin's harsh seasons.\n\n"
            "Window Depot USA of Milwaukee offers CraneBoard, Market Square, and ASCEND composite cladding "
            "— premium products backed by real warranties from a company with 4.9 stars and 1,000+ reviews.\n\n"
            "Book directly with Nate and your FREE estimate is locked in for 12 months — no pressure.\n\n"
            "🏠 Locally owned | 7 SE Wisconsin showrooms\n"
            "⭐ A+ BBB | 4.9★ Google Rating\n"
            "🎁 $500 Gift Card with every estimate!\n\n"
            "📲 (414) 312-5213 | 🌐 windowdepotmilwaukee.com\n\n"
            "#SidingReplacement #HomeExterior #MilwaukeeContractor "
            "#CurbAppeal #WeCreateHappyCustomers"
        ),
    },

    # ── ROOFING ────────────────────────────────────────────────────────────

    {
        "label":    "Roofing — Facebook",
        "account":  FACEBOOK,
        "media":    IMG["roofing"],
        "caption":  (
            "𝗗𝗼𝗻'𝘁 𝘄𝗮𝗶𝘁 𝗳𝗼𝗿 𝗮 𝗹𝗲𝗮𝗸 𝘁𝗼 𝘁𝗲𝗹𝗹 𝘆𝗼𝘂 𝗶𝘁'𝘀 𝘁𝗶𝗺𝗲 𝗳𝗼𝗿 𝗮 𝗻𝗲𝘄 𝗿𝗼𝗼𝗳. 🏠\n\n"
            "I'm Nate with Window Depot USA of Milwaukee. We install NorthGate asphalt shingles and "
            "ProVia metal roofing — products rated for Wisconsin's climate and backed by warranties "
            "that actually protect you. No hidden fees, no games, no pressure.\n\n"
            "✅ NorthGate asphalt & ProVia metal options\n"
            "✅ Rated for extreme northern climates\n"
            "✅ A+ BBB | 4.9★ Google | 1,000+ reviews\n"
            "✅ FREE in-home estimate — 12-month price lock\n"
            "🎁 $500 Gift Card with every estimate!\n\n"
            "📲 (414) 312-5213\n"
            "🌐 https://wdusa-nate-landing.vercel.app/#booking\n\n"
            "#WindowDepotMilwaukee #Roofing #RoofReplacement #MilwaukeeHomes "
            "#FreeEstimate #WeCreateHappyCustomers #Wisconsin #HomeImprovement"
        ),
    },
    {
        "label":    "Roofing — Instagram",
        "account":  INSTAGRAM,
        "media":    IMG["roofing"],
        "caption":  (
            "Your roof doesn't complain. Until it does. 🏠⚡\n\n"
            "I'm Nate — your Window Depot rep in SE Wisconsin. "
            "We install NorthGate asphalt and ProVia metal roofing built for our climate, "
            "and your FREE estimate is price-locked for 12 months.\n\n"
            "✅ NorthGate & ProVia metal options\n"
            "✅ Certified installation crew\n"
            "✅ 4.9★ Google | A+ BBB\n"
            "🎁 $500 Gift Card with every estimate!\n\n"
            "📲 (414) 312-5213\n"
            "🌐 Link in bio\n\n"
            "#Roofing #NewRoof #MilwaukeeHomes #WindowDepot #FreeEstimate "
            "#Wisconsin #HomeImprovement #RoofReplacement #BookWithNate "
            "#NorthGate #WeCreateHappyCustomers #MilwaukeeWI #SEWisconsin #HomeProtection #ProVia"
        ),
    },
    {
        "label":    "Roofing — LinkedIn",
        "account":  LINKEDIN,
        "media":    IMG["roofing"],
        "caption":  (
            "A leaking roof doesn't give you a warning. It just leaks.\n\n"
            "Window Depot USA of Milwaukee installs NorthGate asphalt shingles and ProVia metal roofing "
            "— products rated for our climate and backed by warranties that actually mean something.\n\n"
            "FREE estimate + $500 Gift Card. No obligation, no pressure.\n\n"
            "🏠 Locally owned | 7 SE Wisconsin showrooms\n"
            "⭐ A+ BBB | 4.9★ Google | 1,000+ reviews\n\n"
            "📲 Call Nate: (414) 312-5213\n"
            "🌐 windowdepotmilwaukee.com\n\n"
            "#Roofing #RoofReplacement #MilwaukeeContractor "
            "#HomeProtection #WeCreateHappyCustomers"
        ),
    },

    # ── FLOORING ───────────────────────────────────────────────────────────

    {
        "label":    "Flooring — Facebook",
        "account":  FACEBOOK,
        "media":    IMG["floor"],
        "caption":  (
            "𝗡𝗲𝘄 𝗳𝗹𝗼𝗼𝗿𝘀 𝗰𝗵𝗮𝗻𝗴𝗲 𝗵𝗼𝘄 𝘆𝗼𝘂𝗿 𝗲𝗻𝘁𝗶𝗿𝗲 𝗵𝗼𝗺𝗲 𝗳𝗲𝗲𝗹𝘀 — 𝗳𝗿𝗼𝗺 𝘁𝗵𝗲 𝗳𝗶𝗿𝘀𝘁 𝘀𝘁𝗲𝗽. 🏡\n\n"
            "I'm Nate with Window Depot USA of Milwaukee. Tired of dated or damaged floors? "
            "We offer hardwood, LVP, laminate, and carpet — and our crew handles everything from "
            "measurement to installation with zero hassle on your end.\n\n"
            "✅ Hardwood, LVP, laminate & carpet\n"
            "✅ Any room, any budget\n"
            "✅ Full-service installation — no subcontractors\n"
            "✅ FREE in-home consultation & measure\n"
            "🎁 $500 Gift Card with every estimate!\n\n"
            "📲 (414) 312-5213\n"
            "🌐 https://wdusa-nate-landing.vercel.app/#booking\n\n"
            "#WindowDepotMilwaukee #Flooring #NewFloors #MilwaukeeHomes "
            "#HomeImprovement #FreeEstimate #WeCreateHappyCustomers #Wisconsin"
        ),
    },
    {
        "label":    "Flooring — Instagram",
        "account":  INSTAGRAM,
        "media":    IMG["floor"],
        "caption":  (
            "Dated floors? Scratched hardwood? Worn carpet? Time for an upgrade. 🪵✨\n\n"
            "I'm Nate — your local Window Depot rep. "
            "We install hardwood, LVP, laminate, and carpet with zero hassle. "
            "FREE in-home estimate, price locked 12 months.\n\n"
            "✅ Hardwood, LVP, laminate & carpet\n"
            "✅ Full installation crew\n"
            "✅ Any style, any budget\n"
            "🎁 $500 Gift Card with every estimate!\n\n"
            "📲 (414) 312-5213 | 🌐 Link in bio\n\n"
            "#Flooring #NewFloors #LVP #HardwoodFloors #MilwaukeeHomes #HomeRenovation "
            "#WindowDepot #FreeEstimate #BookWithNate #Wisconsin #HomeImprovement "
            "#MilwaukeeWI #InteriorDesign #HomeUpgrade #WeCreateHappyCustomers"
        ),
    },
    {
        "label":    "Flooring — LinkedIn",
        "account":  LINKEDIN,
        "media":    IMG["floor"],
        "caption":  (
            "New floors change how your entire home feels — from the moment you walk in.\n\n"
            "Window Depot USA of Milwaukee offers hardwood, LVP, laminate, and carpet to match any style "
            "and budget. Our team handles everything from measurement to installation with zero hassle.\n\n"
            "FREE consultation available now. Price locked 12 months.\n\n"
            "🎁 $500 Gift Card with every estimate!\n\n"
            "📲 (414) 312-5213 | 🌐 windowdepotmilwaukee.com\n\n"
            "#Flooring #HomeRenovation #MilwaukeeHomes "
            "#WeCreateHappyCustomers #HomeImprovement"
        ),
    },

    # ── BATHROOMS ──────────────────────────────────────────────────────────

    {
        "label":    "Bathrooms — Facebook",
        "account":  FACEBOOK,
        "media":    IMG["bath"],
        "caption":  (
            "𝗔 𝗯𝗿𝗮𝗻𝗱-𝗻𝗲𝘄 𝗯𝗮𝘁𝗵𝗿𝗼𝗼𝗺 𝗶𝗻 𝗢𝗡𝗘 𝗱𝗮𝘆. 𝗦𝗲𝗿𝗶𝗼𝘂𝘀𝗹𝘆. 🚿\n\n"
            "I'm Nate with Window Depot USA of Milwaukee. Our Bath Makeover acrylic remodels are "
            "custom-measured, professionally installed, and built to last — all completed in a single "
            "day with minimal disruption to your home. No weeks of torn-up bathrooms. Just one day.\n\n"
            "✅ Custom acrylic systems — exact fit for your space\n"
            "✅ Installed in 1 day by our crew\n"
            "✅ Low maintenance — never grout again\n"
            "✅ Lifetime warranty\n"
            "🎁 FREE estimate + $500 Gift Card!\n\n"
            "📲 (414) 312-5213\n"
            "🌐 https://wdusa-nate-landing.vercel.app/#booking\n\n"
            "#WindowDepotMilwaukee #BathroomRemodel #BathMakeover #MilwaukeeHomes "
            "#HomeImprovement #FreeEstimate #WeCreateHappyCustomers #OneDayInstall #Wisconsin"
        ),
    },
    {
        "label":    "Bathrooms — Instagram",
        "account":  INSTAGRAM,
        "media":    IMG["bath"],
        "caption":  (
            "Brand new bathroom. ONE day. Zero mess. 🚿✨\n\n"
            "Yep — our Bath Makeover installs are custom-measured, completed in a single day, "
            "and built to last with zero grout maintenance. I'm Nate, your local Window Depot rep.\n\n"
            "✅ Custom acrylic system\n"
            "✅ Installed in 1 day\n"
            "✅ Low maintenance\n"
            "✅ Lifetime warranty\n"
            "🎁 $500 Gift Card with every estimate!\n\n"
            "📲 (414) 312-5213 | 🌐 Link in bio\n\n"
            "#BathroomRemodel #BathMakeover #OneDayBathroom #MilwaukeeHomes #HomeUpgrade "
            "#WindowDepot #FreeEstimate #BookWithNate #Wisconsin #HomeRenovation "
            "#MilwaukeeWI #InteriorDesign #WeCreateHappyCustomers #BathroomUpgrade #SEWisconsin"
        ),
    },
    {
        "label":    "Bathrooms — LinkedIn",
        "account":  LINKEDIN,
        "media":    IMG["bath"],
        "caption":  (
            "A brand-new bathroom in ONE day. Yes, really.\n\n"
            "Our Bath Makeover acrylic remodels are custom-measured, professionally installed, "
            "and designed to last — all completed in a single day with minimal disruption.\n\n"
            "No weeks of construction. No sub-contractors. No surprises.\n\n"
            "🎁 FREE estimate + $500 Gift Card.\n\n"
            "📲 Window Depot USA of Milwaukee | (414) 312-5213\n"
            "🌐 windowdepotmilwaukee.com\n\n"
            "#BathroomRemodel #MilwaukeeContractor "
            "#HomeImprovement #WeCreateHappyCustomers"
        ),
    },
]


# ---------------------------------------------------------------------------
# API helper
# ---------------------------------------------------------------------------

def create_draft(post: dict) -> dict:
    """
    Create a DRAFT post. status:'draft' means it will NEVER auto-publish.
    Nate must manually approve and publish from the GHL Social Planner UI.
    """
    payload = {
        "accountIds": [post["account"]],
        "summary":    post["caption"],
        "type":       "post",
        "status":     "draft",      # CRITICAL — prevents any publishing
        "media":      [post["media"]],
        "userId":     USER_ID,
    }
    resp = requests.post(
        f"{BASE_URL}/social-media-posting/{GHL_LOCATION_ID}/posts",
        headers=HEADERS,
        json=payload,
    )
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"Failed for '{post['label']}': {data}")
    return data


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not GHL_API_TOKEN or not GHL_LOCATION_ID:
        print("ERROR: GHL_API_TOKEN and GHL_LOCATION_ID must be set.")
        sys.exit(1)

    print(f"Creating {len(POSTS)} draft posts for RevolutionAi Marketing Group...\n")
    created = 0

    for post in POSTS:
        print(f"  {post['label']} ... ", end="", flush=True)
        create_draft(post)
        print("✓ draft saved")
        created += 1

    print(f"\n{'=' * 55}")
    print(f"✅  Done! {created} draft posts created — nothing is live.")
    print(f"\n   Facebook  : {sum(1 for p in POSTS if p['account'] == FACEBOOK)} drafts")
    print(f"   Instagram : {sum(1 for p in POSTS if p['account'] == INSTAGRAM)} drafts")
    print(f"   LinkedIn  : {sum(1 for p in POSTS if p['account'] == LINKEDIN)} drafts")
    print(f"\nReview and publish at:")
    print(f"  https://app.gohighlevel.com/location/{GHL_LOCATION_ID}/social-planner")


if __name__ == "__main__":
    main()
