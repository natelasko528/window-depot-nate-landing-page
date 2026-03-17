#!/usr/bin/env python3
"""
Viral Pilot Reel Generator — Post #1: Triple-Pane Comfort
Window Depot USA of Milwaukee

Produces one 18-second 9:16 reel (1080x1920, 30fps, H.264+AAC)
using FFmpeg cinematic compositing driven by Python/Pillow frame generation.

Phases:
  0.0–0.5s   Hook (thumb-stop)
  0.5–4.0s   Problem recognition
  4.0–9.0s   Value + offer stack
  9.0–14.0s  Trust proof + local relevance
  14.0–18.0s CTA close
"""

import math, os, struct, subprocess, sys, time
import numpy as np
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# ── Dimensions & timing ──────────────────────────────────────────────
W, H = 1080, 1920
FPS = 30
DURATION = 18.0
TOTAL_FRAMES = int(FPS * DURATION)  # 540

# ── Brand palette ─────────────────────────────────────────────────────
NAVY        = (18, 32, 64)
BRAND_BLUE  = (30, 80, 160)
LIGHT_BLUE  = (100, 160, 220)
WHITE       = (255, 255, 255)
GOLD        = (212, 175, 55)
DARK_NAVY   = (10, 22, 40)
BLACK       = (0, 0, 0)

# ── Reels safe zones (px from edge) ──────────────────────────────────
SAFE_TOP    = 260
SAFE_BOTTOM = 280
SAFE_SIDE   = 60

# ── Paths ─────────────────────────────────────────────────────────────
ROOT        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_IMG  = os.path.join(ROOT, "ad-drafts/30-posts/branded-v3/post_01_branded_v3.png")
NATE_IMG    = os.path.join(ROOT, "brand-assets/nate-profile.png")
FONT_PATH   = "/usr/share/fonts/truetype/macos/Helvetica.ttc"
OUTPUT_DIR  = os.path.join(ROOT, "ad-drafts/reels")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "post_01_reel_pilot.mp4")
CONTACT_DIR = os.path.join(OUTPUT_DIR, "contact_sheet")

# ── Easing ────────────────────────────────────────────────────────────
def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))

def lerp(a, b, t):
    return a + (b - a) * clamp(t)

def ease_out_cubic(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3

def ease_in_cubic(t):
    return clamp(t) ** 3

def ease_in_out_cubic(t):
    t = clamp(t)
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2

def ease_out_back(t, s=1.70158):
    t = clamp(t) - 1
    return t * t * ((s + 1) * t + s) + 1

def ease_out_expo(t):
    t = clamp(t)
    return 1 if t == 1 else 1 - 2 ** (-10 * t)

def progress(t, start, end):
    if end <= start:
        return 1.0 if t >= start else 0.0
    return clamp((t - start) / (end - start))


# ── Camera keyframes: (time_s, cx, cy, zoom) ─────────────────────────
# cx,cy are normalised (0-1) positions within the plate.
CAMERA_KF = [
    # Hook: tight on the warm-glowing windows (lower in source, avoids headline text)
    (0.00, 0.50, 0.52, 2.40),
    (0.50, 0.50, 0.52, 2.40),
    # Problem: slowly pull back to reveal more house
    (2.00, 0.50, 0.50, 1.60),
    (3.80, 0.50, 0.49, 1.40),
    # Pre-whip-pan
    (4.00, 0.50, 0.49, 1.40),
    # Post-whip: reframe on upper headline area for value phase
    (4.30, 0.50, 0.42, 1.80),
    (4.60, 0.50, 0.42, 1.80),
    # Value phase: slow drift showing branded image
    (8.80, 0.50, 0.46, 1.30),
    # Trust phase: wide view
    (9.00, 0.50, 0.48, 1.20),
    (13.8, 0.50, 0.48, 1.15),
    # CTA: settle
    (14.0, 0.50, 0.48, 1.15),
    (18.0, 0.50, 0.48, 1.15),
]


def interp_camera(t):
    """Interpolate camera keyframes with ease-in-out."""
    for i in range(len(CAMERA_KF) - 1):
        t0, cx0, cy0, z0 = CAMERA_KF[i]
        t1, cx1, cy1, z1 = CAMERA_KF[i + 1]
        if t0 <= t <= t1:
            p = ease_in_out_cubic(progress(t, t0, t1))
            return (lerp(cx0, cx1, p), lerp(cy0, cy1, p), lerp(z0, z1, p))
    last = CAMERA_KF[-1]
    return (last[1], last[2], last[3])


# ── Pseudo-random camera shake ───────────────────────────────────────
import hashlib

def shake_offset(frame, amplitude=4):
    h = hashlib.md5(struct.pack('i', frame)).digest()
    ox = (h[0] / 255 - 0.5) * 2 * amplitude
    oy = (h[1] / 255 - 0.5) * 2 * amplitude
    return int(ox), int(oy)


# ── Text helpers ──────────────────────────────────────────────────────

def draw_text_shadow(draw, pos, text, font, fill=WHITE, shadow_color=(0, 0, 0, 160),
                     offset=(3, 3), **kw):
    sx, sy = pos[0] + offset[0], pos[1] + offset[1]
    draw.text((sx, sy), text, font=font, fill=shadow_color, **kw)
    draw.text(pos, text, font=font, fill=fill, **kw)


def draw_checkmark(draw, cx, cy, size=20, color=GOLD, width=4):
    """Draw a hand-crafted checkmark at (cx, cy)."""
    pts = [
        (cx - size * 0.4, cy),
        (cx - size * 0.1, cy + size * 0.35),
        (cx + size * 0.5, cy - size * 0.35),
    ]
    draw.line([pts[0], pts[1]], fill=color, width=width)
    draw.line([pts[1], pts[2]], fill=color, width=width)


def text_glow(img, pos, text, font, glow_color, radius=12):
    """Draw glowing text on an RGBA image."""
    tw = font.getlength(text)
    bbox = font.getbbox(text)
    th = bbox[3] - bbox[1]
    pad = radius * 3
    glow_layer = Image.new('RGBA', (int(tw) + pad * 2, th + pad * 2), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    gd.text((pad, pad), text, font=font, fill=glow_color)
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius))
    img.paste(Image.alpha_composite(
        Image.new('RGBA', glow_layer.size, (0, 0, 0, 0)), glow_layer),
        (int(pos[0]) - pad, int(pos[1]) - pad), glow_layer)


def centered_x(text, font, canvas_w=W):
    return (canvas_w - font.getlength(text)) / 2


def rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


# ── Circular crop for Nate headshot ───────────────────────────────────
def circular_crop(img, size, border_color=GOLD, border_w=6):
    img = img.resize((size, size), Image.LANCZOS)
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    out = Image.new('RGBA', (size + border_w * 2, size + border_w * 2), (0, 0, 0, 0))
    od = ImageDraw.Draw(out)
    od.ellipse((0, 0, size + border_w * 2, size + border_w * 2), fill=border_color)
    circle = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    circle.paste(img, mask=mask)
    out.paste(circle, (border_w, border_w), circle)
    return out


# ═══════════════════════════════════════════════════════════════════════
class ReelRenderer:
    def __init__(self):
        print("[init] Loading assets…")
        self._load_assets()
        self._build_plate()
        self._build_vignette()
        print(f"[init] Ready. Rendering {TOTAL_FRAMES} frames at {W}x{H} @ {FPS}fps")

    # ── Asset loading ─────────────────────────────────────────────────
    def _load_assets(self):
        self.source = Image.open(SOURCE_IMG).convert('RGB')
        nate_raw = Image.open(NATE_IMG).convert('RGB')
        self.nate_circle = circular_crop(nate_raw, 200, GOLD, 8)

        self.font_headline   = ImageFont.truetype(FONT_PATH, 88, index=4)  # Condensed Bold
        self.font_big        = ImageFont.truetype(FONT_PATH, 72, index=1)  # Bold
        self.font_medium     = ImageFont.truetype(FONT_PATH, 56, index=1)
        self.font_body       = ImageFont.truetype(FONT_PATH, 48, index=0)  # Regular
        self.font_small      = ImageFont.truetype(FONT_PATH, 40, index=0)
        self.font_phone      = ImageFont.truetype(FONT_PATH, 80, index=1)
        self.font_cta_button = ImageFont.truetype(FONT_PATH, 52, index=1)
        self.font_brand      = ImageFont.truetype(FONT_PATH, 36, index=4)
        self.font_hook       = ImageFont.truetype(FONT_PATH, 96, index=4)
        self.font_problem    = ImageFont.truetype(FONT_PATH, 76, index=1)
        self.font_badge      = ImageFont.truetype(FONT_PATH, 38, index=1)

    # ── Build extended plate from source (1080x1080 → canvas for zoom) ─
    def _build_plate(self):
        pw, ph = W * 2, H * 2  # 2160×3840
        self.plate = Image.new('RGB', (pw, ph), DARK_NAVY)

        src_up = self.source.resize((pw, pw), Image.LANCZOS)
        sy = (ph - pw) // 2  # center vertically: (3840-2160)/2 = 840
        self.plate.paste(src_up, (0, sy))

        # Blend edges into dark navy with gradient
        grad = Image.new('RGBA', (pw, 200), (0, 0, 0, 0))
        for y in range(200):
            a = int(255 * (1 - y / 200))
            for x in range(pw):
                grad.putpixel((x, y), (*DARK_NAVY, a))

        # Top blend
        top_blend = grad.copy()
        plate_rgba = self.plate.convert('RGBA')
        plate_rgba.paste(Image.alpha_composite(
            plate_rgba.crop((0, sy, pw, sy + 200)),
            top_blend), (0, sy))

        # Bottom blend (flipped)
        bot_blend = grad.transpose(Image.FLIP_TOP_BOTTOM)
        by = sy + pw - 200
        plate_rgba.paste(Image.alpha_composite(
            plate_rgba.crop((0, by, pw, by + 200)),
            bot_blend), (0, by))

        self.plate = plate_rgba.convert('RGB')
        self.plate_w, self.plate_h = pw, ph
        print(f"[plate] Built {pw}×{ph} background plate")

    def _build_vignette(self):
        self.vignette = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        vd = ImageDraw.Draw(self.vignette)
        for i in range(80):
            a = int(90 * (i / 80) ** 1.5)
            vd.rectangle([0, i, W, i + 1], fill=(0, 0, 0, a))
            vd.rectangle([0, H - 1 - i, W, H - i], fill=(0, 0, 0, a))
            vd.rectangle([i, 0, i + 1, H], fill=(0, 0, 0, a // 2))
            vd.rectangle([W - 1 - i, 0, W - i, H], fill=(0, 0, 0, a // 2))

    # ── Camera → crop from plate ──────────────────────────────────────
    def _crop_plate(self, cx, cy, zoom):
        vw = int(self.plate_w / zoom)
        vh = int(self.plate_h / zoom)
        pcx = int(cx * self.plate_w)
        pcy = int(cy * self.plate_h)
        x0 = max(0, pcx - vw // 2)
        y0 = max(0, pcy - vh // 2)
        x1 = min(self.plate_w, x0 + vw)
        y1 = min(self.plate_h, y0 + vh)
        if x1 - x0 < vw:
            x0 = max(0, x1 - vw)
        if y1 - y0 < vh:
            y0 = max(0, y1 - vh)
        crop = self.plate.crop((x0, y0, x1, y1))
        return crop.resize((W, H), Image.LANCZOS)

    # ── Render single frame ───────────────────────────────────────────
    def render_frame(self, frame_num):
        t = frame_num / FPS
        canvas = Image.new('RGBA', (W, H), (*DARK_NAVY, 255))

        # Phase 1: Hook (flash + slam)
        if t < 0.10:
            return canvas.convert('RGB')  # black
        if t < 0.17:
            flash_a = int(255 * ease_out_expo(progress(t, 0.10, 0.17)))
            flash = Image.new('RGBA', (W, H), (255, 255, 255, flash_a))
            canvas = Image.alpha_composite(canvas, flash)
            return canvas.convert('RGB')

        # Pattern-interrupt flash at phase transitions
        if 0.48 <= t < 0.55:
            flash_p = 1 - abs(progress(t, 0.48, 0.55) - 0.3) / 0.7
            if flash_p > 0:
                flash = Image.new('RGBA', (W, H),
                                  (255, 255, 255, int(180 * max(0, flash_p))))
                canvas = Image.alpha_composite(canvas, flash)

        # Background: camera-tracked plate crop
        cx, cy, zoom = interp_camera(t)
        bg = self._crop_plate(cx, cy, zoom)

        # Whip-pan motion blur during 4.0-4.3s
        if 4.0 <= t <= 4.3:
            blur_amount = 1 - abs(progress(t, 4.0, 4.3) - 0.5) * 2
            if blur_amount > 0.1:
                bg = bg.filter(ImageFilter.GaussianBlur(radius=int(40 * blur_amount)))
                enhancer = ImageEnhance.Brightness(bg)
                bg = enhancer.enhance(1 + 0.3 * blur_amount)
        # Soft blur during hook/problem phases to suppress source branding text
        elif t < 4.0:
            blur_r = 4 if t < 0.5 else 3
            bg = bg.filter(ImageFilter.GaussianBlur(radius=blur_r))

        canvas.paste(bg, (0, 0))
        canvas = canvas.convert('RGBA')

        # Darken overlay for text readability — adaptive per phase
        if t >= 0.17:
            dark_alpha = 140
            if t < 0.5:
                dark_alpha = int(160 * ease_out_cubic(progress(t, 0.17, 0.5)))
            elif 0.5 <= t < 4.0:
                dark_alpha = 155
            elif 4.0 <= t < 9.0:
                dark_alpha = 140
            elif 9.0 <= t < 14.0:
                dark_alpha = 155
            elif t >= 14.0:
                dark_alpha = int(lerp(155, 210, ease_out_cubic(progress(t, 14.0, 14.5))))
            overlay = Image.new('RGBA', (W, H), (0, 0, 0, dark_alpha))
            canvas = Image.alpha_composite(canvas, overlay)

        draw = ImageDraw.Draw(canvas)

        # ── PHASE 1: Hook text (0.17–0.5s) ───────────────────────────
        if 0.17 <= t < 0.5:
            p = ease_out_back(progress(t, 0.17, 0.40))
            hook_text = "MILWAUKEE"
            hook_x = centered_x(hook_text, self.font_hook)
            target_y = H * 0.42
            hook_y = lerp(H * 0.7, target_y, p)
            draw_text_shadow(draw, (hook_x, hook_y), hook_text,
                             self.font_hook, WHITE, (0, 0, 0, 220), (5, 5))

            p2 = ease_out_cubic(progress(t, 0.25, 0.45))
            sub = "THIS ONE MATTERS."
            sub_x = centered_x(sub, self.font_medium)
            sub_alpha = int(255 * p2)
            draw_text_shadow(draw, (sub_x, hook_y + 115), sub,
                             self.font_medium, (*GOLD, sub_alpha),
                             (0, 0, 0, int(sub_alpha * 0.7)), (3, 3))

        # ── PHASE 2: Problem (0.5–4.0s) ──────────────────────────────
        if 0.5 <= t < 4.0:
            # "MILWAUKEE HOMEOWNERS" header
            header_alpha = int(255 * ease_out_cubic(progress(t, 0.5, 1.0)))
            hdr = "MILWAUKEE HOMEOWNERS"
            hdr_x = centered_x(hdr, self.font_medium)
            draw.text((hdr_x, SAFE_TOP + 40), hdr, font=self.font_medium,
                      fill=(*WHITE, header_alpha))

            # Gold divider line
            if t >= 0.8:
                line_w = int(500 * ease_out_cubic(progress(t, 0.8, 1.2)))
                lx = W // 2
                ly = SAFE_TOP + 115
                draw.line([(lx - line_w // 2, ly), (lx + line_w // 2, ly)],
                          fill=(*GOLD, header_alpha), width=3)

            # Problem texts with staggered slam-in — centered in viewport
            problems = [
                (1.2, "Drafts?", -1),
                (1.6, "Fogging?", 1),
                (2.0, "Higher energy bills?", 0),
            ]
            base_y = H // 2 - 180
            for i, (t_start, text, direction) in enumerate(problems):
                if t < t_start:
                    continue
                p_in = ease_out_back(progress(t, t_start, t_start + 0.3))
                tx = centered_x(text, self.font_problem)
                ty = base_y + i * 110

                if direction == -1:
                    tx = lerp(-600, tx, p_in)
                elif direction == 1:
                    tx = lerp(W + 100, tx, p_in)

                alpha = 255
                if t > 3.2:
                    alpha = int(255 * (1 - ease_in_cubic(progress(t, 3.2, 3.8))))

                draw_text_shadow(draw, (tx, ty), text, self.font_problem,
                                 (*WHITE, alpha), (*BLACK, min(alpha, 200)), (4, 4))

            # "There's a better way." transition text
            if 3.0 <= t < 4.0:
                p_better = ease_out_cubic(progress(t, 3.2, 3.6))
                fade_out = 1 - ease_in_cubic(progress(t, 3.7, 4.0))
                alpha_b = int(255 * p_better * fade_out)
                better = "There's a better way."
                bx = centered_x(better, self.font_big)
                by = H // 2 + 60
                draw_text_shadow(draw, (bx, by), better, self.font_big,
                                 (*GOLD, alpha_b), (*BLACK, int(alpha_b * 0.6)),
                                 (3, 3))

        # ── PHASE 3: Value + Offer (4.0–9.0s) ────────────────────────
        if 4.0 <= t < 9.0:
            # Semi-transparent overlay panel
            if t >= 4.3:
                panel_alpha = int(170 * ease_out_cubic(progress(t, 4.3, 4.8)))
                panel = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                pd = ImageDraw.Draw(panel)
                pd.rounded_rectangle(
                    [SAFE_SIDE, SAFE_TOP + 10, W - SAFE_SIDE, H - SAFE_BOTTOM - 10],
                    radius=24, fill=(*NAVY, panel_alpha))
                canvas = Image.alpha_composite(canvas, panel)
                draw = ImageDraw.Draw(canvas)

            # Headline: TRIPLE-PANE COMFORT
            if t >= 4.5:
                h_p = ease_out_cubic(progress(t, 4.5, 5.0))
                headline = "TRIPLE-PANE"
                headline2 = "COMFORT"
                h_alpha = int(255 * h_p)
                hx = centered_x(headline, self.font_headline)
                hy = SAFE_TOP + 60
                draw.text((hx, hy), headline, font=self.font_headline,
                          fill=(*WHITE, h_alpha))
                hx2 = centered_x(headline2, self.font_headline)
                draw.text((hx2, hy + 95), headline2, font=self.font_headline,
                          fill=(*WHITE, h_alpha))

            # Sub: dual-pane pricing
            if t >= 5.0:
                sp = ease_out_cubic(progress(t, 5.0, 5.5))
                sub = "Triple-pane windows at dual-pane prices."
                sx = centered_x(sub, self.font_body)
                draw.text((sx, SAFE_TOP + 270), sub, font=self.font_body,
                          fill=(*LIGHT_BLUE, int(255 * sp)))

            # Divider
            if t >= 5.3:
                div_p = ease_out_cubic(progress(t, 5.3, 5.6))
                div_w = int(500 * div_p)
                div_y = SAFE_TOP + 340
                draw.line([(W // 2 - div_w // 2, div_y), (W // 2 + div_w // 2, div_y)],
                          fill=(*GOLD, int(200 * div_p)), width=3)

            # Offer stack
            offers = [
                (5.5, "FREE In-Home Estimate"),
                (5.9, "$500 Gift Card"),
                (6.3, "Price Locked 12 Months"),
            ]
            for i, (t_start, text) in enumerate(offers):
                if t < t_start:
                    continue
                op = ease_out_back(progress(t, t_start, t_start + 0.35))
                ox = int(lerp(-W, SAFE_SIDE + 100, op))
                oy = SAFE_TOP + 380 + i * 90

                check_alpha = int(255 * op)
                draw_checkmark(draw, ox - 35, oy + 28, size=22,
                               color=(*GOLD, check_alpha), width=5)
                draw.text((ox, oy), text, font=self.font_medium,
                          fill=(*WHITE, check_alpha))

            # Glow sweep across offers (7.0-7.5s)
            if 7.0 <= t <= 7.8:
                sweep_p = progress(t, 7.0, 7.8)
                sweep_x = int(lerp(-200, W + 200, sweep_p))
                sweep = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                sd = ImageDraw.Draw(sweep)
                for dx in range(-100, 101):
                    a = int(40 * (1 - abs(dx) / 100))
                    sd.line([(sweep_x + dx, SAFE_TOP + 360),
                             (sweep_x + dx, SAFE_TOP + 640)],
                            fill=(255, 255, 255, a))
                canvas = Image.alpha_composite(canvas, sweep)
                draw = ImageDraw.Draw(canvas)

            # "Built for real Wisconsin winters" tagline
            if t >= 7.5:
                tag_p = ease_out_cubic(progress(t, 7.5, 8.0))
                tag = "Built for real Wisconsin winters"
                tag2 = "and summers."
                tx = centered_x(tag, self.font_small)
                ty = SAFE_TOP + 700
                draw.text((tx, ty), tag, font=self.font_small,
                          fill=(*LIGHT_BLUE, int(200 * tag_p)))
                tx2 = centered_x(tag2, self.font_small)
                draw.text((tx2, ty + 50), tag2, font=self.font_small,
                          fill=(*LIGHT_BLUE, int(200 * tag_p)))

        # ── PHASE 4: Trust proof (9.0–14.0s) ─────────────────────────
        if 9.0 <= t < 14.0:
            # Dark overlay panel
            if t >= 9.0:
                tp_alpha = int(160 * ease_out_cubic(progress(t, 9.0, 9.5)))
                trust_panel = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                tpd = ImageDraw.Draw(trust_panel)
                tpd.rounded_rectangle(
                    [SAFE_SIDE, SAFE_TOP, W - SAFE_SIDE, H - SAFE_BOTTOM],
                    radius=24, fill=(*NAVY, tp_alpha))
                canvas = Image.alpha_composite(canvas, trust_panel)
                draw = ImageDraw.Draw(canvas)

            # "SE WISCONSIN'S TRUSTED CHOICE"
            if t >= 9.3:
                tp = ease_out_cubic(progress(t, 9.3, 9.8))
                tr_title = "SE WISCONSIN'S"
                tr_title2 = "TRUSTED CHOICE"
                ttx = centered_x(tr_title, self.font_headline)
                draw.text((ttx, SAFE_TOP + 60), tr_title,
                          font=self.font_headline, fill=(*WHITE, int(255 * tp)))
                ttx2 = centered_x(tr_title2, self.font_headline)
                draw.text((ttx2, SAFE_TOP + 155), tr_title2,
                          font=self.font_headline, fill=(*GOLD, int(255 * tp)))

            # Divider
            if t >= 9.8:
                dp = ease_out_cubic(progress(t, 9.8, 10.1))
                dw = int(600 * dp)
                dy = SAFE_TOP + 270
                draw.line([(W // 2 - dw // 2, dy), (W // 2 + dw // 2, dy)],
                          fill=(*GOLD, int(200 * dp)), width=3)

            # Trust badges
            badges = [
                (10.0, "4.9 / 5  Google Rating"),
                (10.5, "1,000+  Verified Reviews"),
                (11.0, "#3  National Remodeler"),
                (11.5, "A+  BBB Accredited"),
            ]
            badge_y_base = SAFE_TOP + 310
            for i, (t_start, text) in enumerate(badges):
                if t < t_start:
                    continue
                bp = ease_out_back(progress(t, t_start, t_start + 0.35))
                ba = int(255 * bp)
                by = badge_y_base + i * 95

                # Badge background
                bw = int(self.font_medium.getlength(text)) + 60
                bx = (W - bw) // 2
                badge_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                bd = ImageDraw.Draw(badge_layer)
                scale_w = int(bw * bp)
                scale_x = (W - scale_w) // 2
                bd.rounded_rectangle(
                    [scale_x, by - 10, scale_x + scale_w, by + 70],
                    radius=12,
                    fill=(*BRAND_BLUE, int(180 * bp)),
                    outline=(*LIGHT_BLUE, int(100 * bp)),
                    width=2)
                canvas = Image.alpha_composite(canvas, badge_layer)
                draw = ImageDraw.Draw(canvas)

                # Badge text
                btx = centered_x(text, self.font_medium)
                draw.text((btx, by), text, font=self.font_medium,
                          fill=(*WHITE, ba))

            # Local proof line
            if t >= 12.0:
                lp = ease_out_cubic(progress(t, 12.0, 12.5))
                local_text = "Window Depot USA of Milwaukee"
                lx = centered_x(local_text, self.font_body)
                ly = badge_y_base + 4 * 95 + 40
                draw.text((lx, ly), local_text, font=self.font_body,
                          fill=(*LIGHT_BLUE, int(255 * lp)))

            # "National Strength. Local Service."
            if t >= 12.5:
                lp2 = ease_out_cubic(progress(t, 12.5, 13.0))
                motto = "National Strength. Local Service."
                mx = centered_x(motto, self.font_small)
                my = badge_y_base + 4 * 95 + 110
                draw.text((mx, my), motto, font=self.font_small,
                          fill=(*GOLD, int(255 * lp2)))

        # ── PHASE 5: CTA close (14.0–18.0s) ──────────────────────────
        if t >= 14.0:
            # Full CTA card overlay (slides up)
            cta_y_offset = int(H * (1 - ease_out_cubic(progress(t, 14.0, 14.6))))
            cta = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            cd = ImageDraw.Draw(cta)

            # Navy gradient background
            for y in range(H):
                gy = y - cta_y_offset
                if gy < 0:
                    continue
                alpha = min(230, int(230 * ease_out_cubic(clamp(gy / 400))))
                r = int(lerp(DARK_NAVY[0], NAVY[0], clamp(gy / H)))
                g = int(lerp(DARK_NAVY[1], NAVY[1], clamp(gy / H)))
                b = int(lerp(DARK_NAVY[2], NAVY[2], clamp(gy / H)))
                cd.line([(0, y), (W, y)], fill=(r, g, b, alpha))

            canvas = Image.alpha_composite(canvas, cta)
            draw = ImageDraw.Draw(canvas)

            # Nate headshot
            if t >= 14.4:
                nate_p = ease_out_back(progress(t, 14.4, 15.0))
                nate_s = int(self.nate_circle.width * nate_p)
                if nate_s > 10:
                    nate_resized = self.nate_circle.resize((nate_s, nate_s), Image.LANCZOS)
                    nx = W // 2 - nate_s // 2
                    ny = SAFE_TOP + 80 + cta_y_offset
                    if ny + nate_s > 0:
                        canvas.paste(nate_resized, (nx, ny), nate_resized)
                        draw = ImageDraw.Draw(canvas)

            # "Talk directly with Nate"
            if t >= 14.8:
                tp = ease_out_cubic(progress(t, 14.8, 15.3))
                talk = "Talk directly with Nate"
                talk_x = centered_x(talk, self.font_medium)
                talk_y = SAFE_TOP + 330 + cta_y_offset
                draw.text((talk_x, talk_y), talk, font=self.font_medium,
                          fill=(*WHITE, int(255 * tp)))

            # Phone number with glow
            if t >= 15.0:
                pp = ease_out_cubic(progress(t, 15.0, 15.5))
                phone = "(414) 312-5213"
                phone_x = centered_x(phone, self.font_phone)
                phone_y = SAFE_TOP + 410 + cta_y_offset

                # Pulsing glow
                pulse = 0.6 + 0.4 * math.sin((t - 15.0) * 3.5)
                glow_a = int(120 * pp * pulse)
                text_glow(canvas, (phone_x, phone_y), phone,
                          self.font_phone, (*LIGHT_BLUE, glow_a), radius=20)
                draw = ImageDraw.Draw(canvas)
                draw.text((phone_x, phone_y), phone, font=self.font_phone,
                          fill=(*LIGHT_BLUE, int(255 * pp)))

            # CTA button
            if t >= 15.5:
                btn_p = ease_out_back(progress(t, 15.5, 16.0))
                btn_text = "Book Free Estimate"
                btn_tw = int(self.font_cta_button.getlength(btn_text))
                btn_w = btn_tw + 80
                btn_h = 80
                btn_x = (W - btn_w) // 2
                btn_y = SAFE_TOP + 530 + cta_y_offset
                btn_alpha = int(255 * btn_p)

                btn_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                bd = ImageDraw.Draw(btn_layer)
                bd.rounded_rectangle(
                    [btn_x, btn_y, btn_x + btn_w, btn_y + btn_h],
                    radius=40,
                    fill=(*BRAND_BLUE, btn_alpha))
                canvas = Image.alpha_composite(canvas, btn_layer)
                draw = ImageDraw.Draw(canvas)
                draw.text((btn_x + 40, btn_y + 12), btn_text,
                          font=self.font_cta_button, fill=(*WHITE, btn_alpha))

            # Offer reminder lines (split for safe zones)
            if t >= 16.0:
                rp = ease_out_cubic(progress(t, 16.0, 16.5))
                r1 = "FREE estimate  +  $500 gift card"
                r2 = "Price locked 1 year"
                r1x = centered_x(r1, self.font_small)
                r2x = centered_x(r2, self.font_small)
                ry = SAFE_TOP + 640 + cta_y_offset
                draw.text((r1x, ry), r1, font=self.font_small,
                          fill=(*GOLD, int(220 * rp)))
                draw.text((r2x, ry + 50), r2, font=self.font_small,
                          fill=(*GOLD, int(220 * rp)))

            # Brand line
            if t >= 16.3:
                brp = ease_out_cubic(progress(t, 16.3, 16.8))
                brand = "WINDOW DEPOT USA OF MILWAUKEE"
                brx = centered_x(brand, self.font_brand)
                bry = SAFE_TOP + 770 + cta_y_offset
                draw.text((brx, bry), brand, font=self.font_brand,
                          fill=(*WHITE, int(180 * brp)))

                tag = "We Create Happy Customers"
                tagx = centered_x(tag, self.font_small)
                tagy = bry + 50
                draw.text((tagx, tagy), tag, font=self.font_small,
                          fill=(*LIGHT_BLUE, int(160 * brp)))

        # ── Vignette ──────────────────────────────────────────────────
        canvas = Image.alpha_composite(canvas, self.vignette)

        # ── Camera shake ──────────────────────────────────────────────
        amp = 3
        if 0.17 <= t < 0.5:
            amp = 7
        elif 4.0 <= t < 4.3:
            amp = 10
        elif t >= 14.0:
            amp = 2
        ox, oy = shake_offset(frame_num, amp)
        if ox != 0 or oy != 0:
            shifted = Image.new('RGBA', (W, H), (*DARK_NAVY, 255))
            shifted.paste(canvas, (ox, oy))
            canvas = shifted

        # ── Subtle film grain (light, compressor-friendly) ─────────────
        rgb = canvas.convert('RGB')
        rng = np.random.default_rng(frame_num)
        noise = rng.normal(0, 3, (H, W, 3)).astype(np.int16)
        arr = np.array(rgb, dtype=np.int16)
        arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(arr, 'RGB')

    # ── Render all frames → pipe to FFmpeg ────────────────────────────
    def render(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(CONTACT_DIR, exist_ok=True)

        cmd = [
            'ffmpeg', '-y', '-hide_banner', '-loglevel', 'warning',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24',
            '-s', f'{W}x{H}', '-r', str(FPS),
            '-i', 'pipe:0',
            '-f', 'lavfi', '-i', f'anullsrc=channel_layout=mono:sample_rate=44100',
            '-c:v', 'libx264', '-preset', 'slow', '-crf', '23',
            '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '128k',
            '-t', str(DURATION),
            '-movflags', '+faststart',
            '-shortest',
            OUTPUT_FILE,
        ]

        print(f"[render] Starting FFmpeg: {' '.join(cmd[:8])}…")
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

        contact_frames = {
            int(0.25 * FPS): "01_hook",
            int(2.0 * FPS):  "02_problem",
            int(6.5 * FPS):  "03_offer",
            int(11.5 * FPS): "04_trust",
            int(16.0 * FPS): "05_cta",
        }

        t0 = time.time()
        for f in range(TOTAL_FRAMES):
            img = self.render_frame(f)
            proc.stdin.write(img.tobytes())

            if f in contact_frames:
                img.save(os.path.join(CONTACT_DIR, f"{contact_frames[f]}.png"))
                print(f"  [contact] Saved frame {f} → {contact_frames[f]}.png")

            if f % 60 == 0:
                elapsed = time.time() - t0
                fps_actual = (f + 1) / elapsed if elapsed > 0 else 0
                pct = (f + 1) / TOTAL_FRAMES * 100
                print(f"  [frame {f:>4}/{TOTAL_FRAMES}] {pct:5.1f}%  "
                      f"({fps_actual:.1f} frames/s)")

        proc.stdin.close()
        proc.wait()
        elapsed = time.time() - t0
        print(f"[render] Done in {elapsed:.1f}s  →  {OUTPUT_FILE}")
        return proc.returncode


# ═══════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    renderer = ReelRenderer()
    rc = renderer.render()
    sys.exit(rc)
