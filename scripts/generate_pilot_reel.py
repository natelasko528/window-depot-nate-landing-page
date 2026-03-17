#!/usr/bin/env python3
"""
Viral Pilot Reel Generator V2 — Post #1: Triple-Pane Comfort
Window Depot USA of Milwaukee

Produces one 18-second 9:16 reel (1080x1920, 30fps, H.264+AAC) with:
  - Voiceover (edge-tts)
  - Cinematic background music (synthesized)
  - Kinetic typography + camera movement

Phases:
  0.0–0.5s   Hook (thumb-stop)
  0.5–4.0s   Problem recognition
  4.0–9.0s   Value + offer stack
  9.0–14.0s  Trust proof + local relevance
  14.0–18.0s CTA close
"""

import asyncio, hashlib, math, os, struct, subprocess, sys, time, wave
import numpy as np
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from scipy.signal import butter, sosfilt

# ── Dimensions & timing ──────────────────────────────────────────────
W, H = 1080, 1920
FPS = 30
DURATION = 18.0
TOTAL_FRAMES = int(FPS * DURATION)
SR = 44100

# ── Brand palette ─────────────────────────────────────────────────────
NAVY        = (18, 32, 64)
BRAND_BLUE  = (30, 80, 160)
LIGHT_BLUE  = (100, 160, 220)
WHITE       = (255, 255, 255)
GOLD        = (212, 175, 55)
DARK_NAVY   = (10, 22, 40)
BLACK       = (0, 0, 0)

# ── Reels safe zones ─────────────────────────────────────────────────
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
AUDIO_DIR   = os.path.join(OUTPUT_DIR, "audio_tmp")

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


# ══════════════════════════════════════════════════════════════════════
#  AUDIO PIPELINE
# ══════════════════════════════════════════════════════════════════════

VO_SEGMENTS = [
    {
        "id": "problem",
        "text": "Milwaukee, your windows are costing you.",
        "rate": "+25%",
        "start": 0.6,
        "max_dur": 3.0,
    },
    {
        "id": "value",
        "text": "Triple-pane at dual-pane prices. Free estimate. Gift card. Price lock.",
        "rate": "+28%",
        "start": 4.5,
        "max_dur": 4.2,
    },
    {
        "id": "trust",
        "text": "Wisconsin's most trusted choice. Five stars. A thousand reviews.",
        "rate": "+22%",
        "start": 9.3,
        "max_dur": 4.2,
    },
    {
        "id": "cta",
        "text": "Text Nate. Four one four, three one two, fifty-two thirteen.",
        "rate": "+18%",
        "start": 14.3,
        "max_dur": 3.5,
    },
]


def wav_to_numpy(path):
    """Read a WAV file into a float64 numpy array, mono."""
    with wave.open(path, 'r') as wf:
        frames = wf.readframes(wf.getnframes())
        dtype = np.int16 if wf.getsampwidth() == 2 else np.int32
        arr = np.frombuffer(frames, dtype=dtype).astype(np.float64)
        if wf.getnchannels() == 2:
            arr = arr.reshape(-1, 2).mean(axis=1)
        arr /= np.iinfo(dtype).max
        return arr, wf.getframerate()


def numpy_to_wav(path, arr, sr=SR):
    """Write a float64 numpy array to a 16-bit mono WAV."""
    arr = np.clip(arr, -1.0, 1.0)
    pcm = (arr * 32767).astype(np.int16)
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


def mp3_to_wav(mp3_path, wav_path, target_sr=SR):
    """Convert mp3 to mono WAV at target sample rate."""
    subprocess.run([
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-i', mp3_path,
        '-ac', '1', '-ar', str(target_sr),
        '-acodec', 'pcm_s16le', wav_path
    ], check=True)


def time_stretch_wav(in_path, out_path, target_dur):
    """Speed up/slow down a WAV to exactly target_dur seconds."""
    r = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
         '-of', 'csv=p=0', in_path],
        capture_output=True, text=True)
    src_dur = float(r.stdout.strip())
    if abs(src_dur - target_dur) < 0.05:
        if in_path != out_path:
            subprocess.run(['cp', in_path, out_path])
        return
    ratio = src_dur / target_dur
    ratio = max(0.5, min(2.0, ratio))
    subprocess.run([
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-i', in_path,
        '-filter:a', f'atempo={ratio}',
        '-ac', '1', '-ar', str(SR),
        '-acodec', 'pcm_s16le', out_path
    ], check=True)


async def generate_voiceover_segments():
    """Generate VO segments with edge-tts, time-stretch to fit."""
    import edge_tts
    os.makedirs(AUDIO_DIR, exist_ok=True)
    segments = {}

    for seg in VO_SEGMENTS:
        mp3 = os.path.join(AUDIO_DIR, f"vo_{seg['id']}.mp3")
        wav_raw = os.path.join(AUDIO_DIR, f"vo_{seg['id']}_raw.wav")
        wav_fit = os.path.join(AUDIO_DIR, f"vo_{seg['id']}.wav")

        comm = edge_tts.Communicate(
            seg["text"],
            voice="en-US-AndrewNeural",
            rate=seg["rate"],
            pitch="-2Hz",
        )
        await comm.save(mp3)
        mp3_to_wav(mp3, wav_raw)

        r = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
             '-of', 'csv=p=0', wav_raw],
            capture_output=True, text=True)
        raw_dur = float(r.stdout.strip())

        if raw_dur > seg["max_dur"]:
            time_stretch_wav(wav_raw, wav_fit, seg["max_dur"])
        else:
            subprocess.run(['cp', wav_raw, wav_fit])

        segments[seg["id"]] = {
            "path": wav_fit,
            "start": seg["start"],
        }
        print(f"  [vo] {seg['id']}: {raw_dur:.2f}s → fit in {seg['max_dur']:.1f}s window")

    return segments


def synthesize_music(duration=DURATION, sr=SR):
    """Build a cinematic background music bed from scratch."""
    n = int(sr * duration)
    t = np.linspace(0, duration, n, endpoint=False)
    music = np.zeros(n, dtype=np.float64)

    bpm = 82
    beat_s = 60.0 / bpm

    # ── Sub-bass pulse (heartbeat-style 55 Hz) ────────────────────────
    sub_env = np.exp(-6 * (t % beat_s) / beat_s)
    sub = 0.22 * np.sin(2 * np.pi * 55 * t) * sub_env
    music += sub

    # ── Warm pad (Cmaj: C3 + E3 + G3, slow filter sweep) ─────────────
    pad_raw = (
        0.06 * np.sin(2 * np.pi * 130.81 * t) +
        0.05 * np.sin(2 * np.pi * 164.81 * t * 1.001) +
        0.05 * np.sin(2 * np.pi * 196.00 * t * 0.999) +
        0.03 * np.sin(2 * np.pi * 261.63 * t)
    )
    pad_env = 0.4 + 0.6 * np.clip((t - 0.5) / 2.0, 0, 1)
    pad_lfo = 1.0 + 0.15 * np.sin(2 * np.pi * 0.08 * t)
    pad = pad_raw * pad_env * pad_lfo
    cutoff_sweep = 800 + 1200 * np.clip(t / duration, 0, 1)
    chunk_size = sr // 4
    for i in range(0, n, chunk_size):
        end = min(i + chunk_size, n)
        fc = cutoff_sweep[i] / (sr / 2)
        fc = min(fc, 0.99)
        sos = butter(2, fc, btype='low', output='sos')
        pad[i:end] = sosfilt(sos, pad[i:end])
    music += pad

    # ── Rhythmic tick (16th-note hi-hat feel) ─────────────────────────
    tick_interval = beat_s / 2
    tick = np.zeros(n)
    rng = np.random.default_rng(42)
    for beat_t in np.arange(0, duration, tick_interval):
        idx = int(beat_t * sr)
        tick_len = min(int(0.01 * sr), n - idx)
        if tick_len > 0 and idx < n:
            tick[idx:idx + tick_len] = rng.normal(0, 0.03, tick_len)
    sos_hp = butter(3, 4000 / (sr / 2), btype='high', output='sos')
    tick = sosfilt(sos_hp, tick)
    music += tick * 0.6

    # ── Impact hits at phase transitions ──────────────────────────────
    impact_times = [0.10, 4.0, 9.0, 14.0]
    for hit_t in impact_times:
        idx = int(hit_t * sr)
        hit_len = min(int(0.4 * sr), n - idx)
        if hit_len > 0:
            ht = np.linspace(0, 0.4, hit_len)
            hit = 0.35 * np.sin(2 * np.pi * 42 * ht) * np.exp(-7 * ht)
            hit += 0.15 * rng.normal(0, 1, hit_len) * np.exp(-15 * ht)
            music[idx:idx + hit_len] += hit

    # ── CTA riser (last 4 seconds) ───────────────────────────────────
    riser_start = int(14.0 * sr)
    riser_len = n - riser_start
    rt = np.linspace(0, 4.0, riser_len)
    riser_freq = 200 + 600 * (rt / 4.0) ** 2
    riser_phase = np.cumsum(2 * np.pi * riser_freq / sr)
    riser = 0.08 * np.sin(riser_phase) * (rt / 4.0) ** 2
    noise_riser = 0.04 * rng.normal(0, 1, riser_len) * (rt / 4.0) ** 2.5
    sos_bp = butter(2, [1000 / (sr / 2), 6000 / (sr / 2)], btype='band', output='sos')
    noise_riser = sosfilt(sos_bp, noise_riser)
    music[riser_start:] += riser + noise_riser

    # ── Fade in/out ──────────────────────────────────────────────────
    fade_in_samples = int(0.3 * sr)
    fade_out_samples = int(0.5 * sr)
    music[:fade_in_samples] *= np.linspace(0, 1, fade_in_samples)
    music[-fade_out_samples:] *= np.linspace(1, 0, fade_out_samples)

    # ── Normalize ────────────────────────────────────────────────────
    peak = np.max(np.abs(music))
    if peak > 0:
        music = music / peak * 0.7

    return music


def mix_audio(vo_segments, music, duration=DURATION, sr=SR):
    """Mix voiceover + music with ducking."""
    n = int(sr * duration)
    vo_track = np.zeros(n, dtype=np.float64)
    vo_mask = np.zeros(n, dtype=np.float64)

    for seg_info in vo_segments.values():
        arr, seg_sr = wav_to_numpy(seg_info["path"])
        if seg_sr != sr:
            from scipy.signal import resample
            arr = resample(arr, int(len(arr) * sr / seg_sr))
        start_sample = int(seg_info["start"] * sr)
        end_sample = min(start_sample + len(arr), n)
        copy_len = end_sample - start_sample
        vo_track[start_sample:end_sample] = arr[:copy_len] * 0.95
        pre_duck = int(0.1 * sr)
        post_duck = int(0.3 * sr)
        duck_start = max(0, start_sample - pre_duck)
        duck_end = min(n, end_sample + post_duck)
        vo_mask[duck_start:duck_end] = 1.0

    # Smooth the ducking mask
    from scipy.ndimage import uniform_filter1d
    vo_mask = uniform_filter1d(vo_mask, int(0.15 * sr))

    # Duck music under VO (music at 30% when VO active, 70% otherwise)
    music_ducked = music[:n].copy()
    if len(music_ducked) < n:
        music_ducked = np.pad(music_ducked, (0, n - len(music_ducked)))
    duck_level = 1.0 - 0.55 * vo_mask
    music_ducked *= duck_level * 0.5

    mixed = vo_track + music_ducked

    # Final limiter
    peak = np.max(np.abs(mixed))
    if peak > 0.95:
        mixed = mixed / peak * 0.95

    return mixed


def build_audio():
    """Generate the complete audio track."""
    print("[audio] Generating voiceover…")
    vo_segments = asyncio.run(generate_voiceover_segments())

    print("[audio] Synthesizing background music…")
    music = synthesize_music()

    print("[audio] Mixing VO + music…")
    mixed = mix_audio(vo_segments, music)

    audio_path = os.path.join(OUTPUT_DIR, "post_01_audio.wav")
    numpy_to_wav(audio_path, mixed)
    print(f"[audio] Saved → {audio_path}")
    return audio_path


# ══════════════════════════════════════════════════════════════════════
#  CAMERA SYSTEM
# ══════════════════════════════════════════════════════════════════════

CAMERA_KF = [
    (0.00, 0.50, 0.52, 2.40),
    (0.50, 0.50, 0.52, 2.40),
    (2.00, 0.50, 0.50, 1.60),
    (3.80, 0.50, 0.49, 1.40),
    (4.00, 0.50, 0.49, 1.40),
    (4.30, 0.50, 0.42, 1.80),
    (4.60, 0.50, 0.42, 1.80),
    (8.80, 0.50, 0.46, 1.30),
    (9.00, 0.50, 0.48, 1.20),
    (13.8, 0.50, 0.48, 1.15),
    (14.0, 0.50, 0.48, 1.15),
    (18.0, 0.50, 0.48, 1.15),
]


def interp_camera(t):
    for i in range(len(CAMERA_KF) - 1):
        t0, cx0, cy0, z0 = CAMERA_KF[i]
        t1, cx1, cy1, z1 = CAMERA_KF[i + 1]
        if t0 <= t <= t1:
            p = ease_in_out_cubic(progress(t, t0, t1))
            return (lerp(cx0, cx1, p), lerp(cy0, cy1, p), lerp(z0, z1, p))
    last = CAMERA_KF[-1]
    return (last[1], last[2], last[3])


def shake_offset(frame, amplitude=4):
    h = hashlib.md5(struct.pack('i', frame)).digest()
    ox = (h[0] / 255 - 0.5) * 2 * amplitude
    oy = (h[1] / 255 - 0.5) * 2 * amplitude
    return int(ox), int(oy)


# ══════════════════════════════════════════════════════════════════════
#  TEXT HELPERS
# ══════════════════════════════════════════════════════════════════════

def draw_text_shadow(draw, pos, text, font, fill=WHITE, shadow_color=(0, 0, 0, 160),
                     offset=(3, 3), **kw):
    sx, sy = pos[0] + offset[0], pos[1] + offset[1]
    draw.text((sx, sy), text, font=font, fill=shadow_color, **kw)
    draw.text(pos, text, font=font, fill=fill, **kw)


def draw_checkmark(draw, cx, cy, size=20, color=GOLD, width=4):
    pts = [
        (cx - size * 0.4, cy),
        (cx - size * 0.1, cy + size * 0.35),
        (cx + size * 0.5, cy - size * 0.35),
    ]
    draw.line([pts[0], pts[1]], fill=color, width=width)
    draw.line([pts[1], pts[2]], fill=color, width=width)


def text_glow(img, pos, text, font, glow_color, radius=12):
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


# ══════════════════════════════════════════════════════════════════════
#  VISUAL RENDERER
# ══════════════════════════════════════════════════════════════════════

class ReelRenderer:
    def __init__(self):
        print("[init] Loading assets…")
        self._load_assets()
        self._build_plate()
        self._build_vignette()
        self._build_snow_particles()
        print(f"[init] Ready — {TOTAL_FRAMES} frames @ {W}x{H}")

    def _load_assets(self):
        self.source = Image.open(SOURCE_IMG).convert('RGB')
        nate_raw = Image.open(NATE_IMG).convert('RGB')
        self.nate_circle = circular_crop(nate_raw, 200, GOLD, 8)

        self.font_headline   = ImageFont.truetype(FONT_PATH, 88, index=4)
        self.font_big        = ImageFont.truetype(FONT_PATH, 72, index=1)
        self.font_medium     = ImageFont.truetype(FONT_PATH, 56, index=1)
        self.font_body       = ImageFont.truetype(FONT_PATH, 48, index=0)
        self.font_small      = ImageFont.truetype(FONT_PATH, 40, index=0)
        self.font_phone      = ImageFont.truetype(FONT_PATH, 80, index=1)
        self.font_cta_button = ImageFont.truetype(FONT_PATH, 52, index=1)
        self.font_brand      = ImageFont.truetype(FONT_PATH, 36, index=4)
        self.font_hook       = ImageFont.truetype(FONT_PATH, 96, index=4)
        self.font_problem    = ImageFont.truetype(FONT_PATH, 76, index=1)

    def _build_plate(self):
        pw, ph = W * 2, H * 2
        self.plate = Image.new('RGB', (pw, ph), DARK_NAVY)
        src_up = self.source.resize((pw, pw), Image.LANCZOS)
        sy = (ph - pw) // 2
        self.plate.paste(src_up, (0, sy))

        grad = Image.new('RGBA', (pw, 200), (0, 0, 0, 0))
        for y in range(200):
            a = int(255 * (1 - y / 200))
            for x in range(pw):
                grad.putpixel((x, y), (*DARK_NAVY, a))

        plate_rgba = self.plate.convert('RGBA')
        top_blend = grad.copy()
        plate_rgba.paste(Image.alpha_composite(
            plate_rgba.crop((0, sy, pw, sy + 200)), top_blend), (0, sy))
        bot_blend = grad.transpose(Image.FLIP_TOP_BOTTOM)
        by = sy + pw - 200
        plate_rgba.paste(Image.alpha_composite(
            plate_rgba.crop((0, by, pw, by + 200)), bot_blend), (0, by))
        self.plate = plate_rgba.convert('RGB')
        self.plate_w, self.plate_h = pw, ph

    def _build_vignette(self):
        self.vignette = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        vd = ImageDraw.Draw(self.vignette)
        for i in range(80):
            a = int(90 * (i / 80) ** 1.5)
            vd.rectangle([0, i, W, i + 1], fill=(0, 0, 0, a))
            vd.rectangle([0, H - 1 - i, W, H - i], fill=(0, 0, 0, a))
            vd.rectangle([i, 0, i + 1, H], fill=(0, 0, 0, a // 2))
            vd.rectangle([W - 1 - i, 0, W - i, H], fill=(0, 0, 0, a // 2))

    def _build_snow_particles(self):
        rng = np.random.default_rng(99)
        self.snow_particles = []
        for _ in range(35):
            self.snow_particles.append({
                'x': rng.uniform(0, W),
                'y': rng.uniform(0, H),
                'speed': rng.uniform(40, 120),
                'drift': rng.uniform(-15, 15),
                'size': rng.uniform(2, 5),
                'alpha': rng.uniform(60, 160),
            })

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

    def _draw_snow(self, draw, t, alpha_mult=1.0):
        """Draw falling snow particles for winter atmosphere."""
        for p in self.snow_particles:
            py = (p['y'] + p['speed'] * t) % (H + 100) - 50
            px = p['x'] + p['drift'] * math.sin(t * 0.5 + p['x'] * 0.01)
            px = px % W
            a = int(p['alpha'] * alpha_mult)
            if a > 0:
                r = int(p['size'])
                draw.ellipse([px - r, py - r, px + r, py + r],
                             fill=(255, 255, 255, a))

    def _apply_color_grade(self, img, t):
        """Phase-based color temperature shift."""
        arr = np.array(img, dtype=np.float32)
        if t < 0.5:
            arr[:, :, 2] = np.clip(arr[:, :, 2] * 1.1, 0, 255)  # cool blue
            arr[:, :, 0] = np.clip(arr[:, :, 0] * 0.92, 0, 255)
        elif t < 4.0:
            desat = 0.92
            gray = arr.mean(axis=2, keepdims=True)
            arr = arr * desat + gray * (1 - desat)
        elif 4.0 <= t < 9.0:
            arr[:, :, 0] = np.clip(arr[:, :, 0] * 1.05, 0, 255)  # warm
            arr[:, :, 2] = np.clip(arr[:, :, 2] * 0.95, 0, 255)
        elif 14.0 <= t:
            warmth = ease_out_cubic(progress(t, 14.0, 15.0))
            arr[:, :, 0] = np.clip(arr[:, :, 0] * (1 + 0.06 * warmth), 0, 255)
            arr[:, :, 1] = np.clip(arr[:, :, 1] * (1 + 0.02 * warmth), 0, 255)
        return Image.fromarray(arr.astype(np.uint8))

    # ── Render single frame ───────────────────────────────────────────
    def render_frame(self, frame_num):
        t = frame_num / FPS
        canvas = Image.new('RGBA', (W, H), (*DARK_NAVY, 255))

        if t < 0.10:
            return canvas.convert('RGB')
        if t < 0.17:
            flash_a = int(255 * ease_out_expo(progress(t, 0.10, 0.17)))
            flash = Image.new('RGBA', (W, H), (255, 255, 255, flash_a))
            canvas = Image.alpha_composite(canvas, flash)
            return canvas.convert('RGB')

        # Phase-transition flash at 0.48s
        if 0.48 <= t < 0.55:
            flash_p = 1 - abs(progress(t, 0.48, 0.55) - 0.3) / 0.7
            if flash_p > 0:
                flash = Image.new('RGBA', (W, H),
                                  (255, 255, 255, int(180 * max(0, flash_p))))
                canvas = Image.alpha_composite(canvas, flash)

        # Background
        cx, cy, zoom = interp_camera(t)
        bg = self._crop_plate(cx, cy, zoom)

        if 4.0 <= t <= 4.3:
            blur_amount = 1 - abs(progress(t, 4.0, 4.3) - 0.5) * 2
            if blur_amount > 0.1:
                bg = bg.filter(ImageFilter.GaussianBlur(radius=int(40 * blur_amount)))
                bg = ImageEnhance.Brightness(bg).enhance(1 + 0.3 * blur_amount)
        elif t < 4.0:
            bg = bg.filter(ImageFilter.GaussianBlur(radius=4 if t < 0.5 else 3))

        canvas.paste(bg, (0, 0))
        canvas = canvas.convert('RGBA')

        # Darken overlay (adaptive)
        if t >= 0.17:
            da = 140
            if t < 0.5:
                da = int(160 * ease_out_cubic(progress(t, 0.17, 0.5)))
            elif t < 4.0:
                da = 155
            elif t < 9.0:
                da = 140
            elif t < 14.0:
                da = 155
            else:
                da = int(lerp(155, 210, ease_out_cubic(progress(t, 14.0, 14.5))))
            overlay = Image.new('RGBA', (W, H), (0, 0, 0, da))
            canvas = Image.alpha_composite(canvas, overlay)

        draw = ImageDraw.Draw(canvas)

        # Snow particles (hook + problem phases)
        if t < 4.0 and t >= 0.17:
            snow_alpha = 1.0
            if t > 3.5:
                snow_alpha = 1 - ease_in_cubic(progress(t, 3.5, 4.0))
            self._draw_snow(draw, t, snow_alpha)

        # ── PHASE 1: Hook (0.17–0.5s) ────────────────────────────────
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
            header_alpha = int(255 * ease_out_cubic(progress(t, 0.5, 1.0)))
            hdr = "MILWAUKEE HOMEOWNERS"
            hdr_x = centered_x(hdr, self.font_medium)
            draw.text((hdr_x, SAFE_TOP + 40), hdr, font=self.font_medium,
                      fill=(*WHITE, header_alpha))

            if t >= 0.8:
                line_w = int(500 * ease_out_cubic(progress(t, 0.8, 1.2)))
                lx = W // 2
                ly = SAFE_TOP + 115
                draw.line([(lx - line_w // 2, ly), (lx + line_w // 2, ly)],
                          fill=(*GOLD, header_alpha), width=3)

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

            if 3.0 <= t < 4.0:
                p_better = ease_out_cubic(progress(t, 3.2, 3.6))
                fade_out = 1 - ease_in_cubic(progress(t, 3.7, 4.0))
                alpha_b = int(255 * p_better * fade_out)
                better = "There's a better way."
                bx = centered_x(better, self.font_big)
                by = H // 2 + 60
                draw_text_shadow(draw, (bx, by), better, self.font_big,
                                 (*GOLD, alpha_b), (*BLACK, int(alpha_b * 0.6)), (3, 3))

        # ── PHASE 3: Value + Offer (4.0–9.0s) ────────────────────────
        if 4.0 <= t < 9.0:
            if t >= 4.3:
                panel_alpha = int(170 * ease_out_cubic(progress(t, 4.3, 4.8)))
                panel = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                pd = ImageDraw.Draw(panel)
                pd.rounded_rectangle(
                    [SAFE_SIDE, SAFE_TOP + 10, W - SAFE_SIDE, H - SAFE_BOTTOM - 10],
                    radius=24, fill=(*NAVY, panel_alpha))
                canvas = Image.alpha_composite(canvas, panel)
                draw = ImageDraw.Draw(canvas)

            if t >= 4.5:
                h_p = ease_out_cubic(progress(t, 4.5, 5.0))
                h_alpha = int(255 * h_p)
                for txt, y_off in [("TRIPLE-PANE", 60), ("COMFORT", 155)]:
                    hx = centered_x(txt, self.font_headline)
                    draw.text((hx, SAFE_TOP + y_off), txt,
                              font=self.font_headline, fill=(*WHITE, h_alpha))

            if t >= 5.0:
                sp = ease_out_cubic(progress(t, 5.0, 5.5))
                sub = "Triple-pane windows at dual-pane prices."
                sx = centered_x(sub, self.font_body)
                draw.text((sx, SAFE_TOP + 270), sub, font=self.font_body,
                          fill=(*LIGHT_BLUE, int(255 * sp)))

            if t >= 5.3:
                div_p = ease_out_cubic(progress(t, 5.3, 5.6))
                dw = int(500 * div_p)
                dy = SAFE_TOP + 340
                draw.line([(W // 2 - dw // 2, dy), (W // 2 + dw // 2, dy)],
                          fill=(*GOLD, int(200 * div_p)), width=3)

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

            if 7.0 <= t <= 7.8:
                sweep_p = progress(t, 7.0, 7.8)
                sweep_x = int(lerp(-200, W + 200, sweep_p))
                sweep = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                sd = ImageDraw.Draw(sweep)
                for dx in range(-100, 101):
                    a = int(50 * (1 - abs(dx) / 100))
                    sd.line([(sweep_x + dx, SAFE_TOP + 360),
                             (sweep_x + dx, SAFE_TOP + 640)],
                            fill=(255, 255, 255, a))
                canvas = Image.alpha_composite(canvas, sweep)
                draw = ImageDraw.Draw(canvas)

            if t >= 7.5:
                tag_p = ease_out_cubic(progress(t, 7.5, 8.0))
                for txt, y_off in [
                    ("Built for real Wisconsin winters", 700),
                    ("and summers.", 750),
                ]:
                    tx = centered_x(txt, self.font_small)
                    draw.text((tx, SAFE_TOP + y_off), txt, font=self.font_small,
                              fill=(*LIGHT_BLUE, int(200 * tag_p)))

        # ── PHASE 4: Trust (9.0–14.0s) ───────────────────────────────
        if 9.0 <= t < 14.0:
            tp_alpha = int(160 * ease_out_cubic(progress(t, 9.0, 9.5)))
            trust_panel = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            tpd = ImageDraw.Draw(trust_panel)
            tpd.rounded_rectangle(
                [SAFE_SIDE, SAFE_TOP, W - SAFE_SIDE, H - SAFE_BOTTOM],
                radius=24, fill=(*NAVY, tp_alpha))
            canvas = Image.alpha_composite(canvas, trust_panel)
            draw = ImageDraw.Draw(canvas)

            if t >= 9.3:
                tp = ease_out_cubic(progress(t, 9.3, 9.8))
                for txt, y_off, col in [
                    ("SE WISCONSIN'S", 60, WHITE),
                    ("TRUSTED CHOICE", 155, GOLD),
                ]:
                    ttx = centered_x(txt, self.font_headline)
                    draw.text((ttx, SAFE_TOP + y_off), txt,
                              font=self.font_headline, fill=(*col, int(255 * tp)))

            if t >= 9.8:
                dp = ease_out_cubic(progress(t, 9.8, 10.1))
                dw = int(600 * dp)
                dy = SAFE_TOP + 270
                draw.line([(W // 2 - dw // 2, dy), (W // 2 + dw // 2, dy)],
                          fill=(*GOLD, int(200 * dp)), width=3)

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
                bw = int(self.font_medium.getlength(text)) + 60
                badge_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                bd = ImageDraw.Draw(badge_layer)
                scale_w = int(bw * bp)
                scale_x = (W - scale_w) // 2
                bd.rounded_rectangle(
                    [scale_x, by - 10, scale_x + scale_w, by + 70],
                    radius=12,
                    fill=(*BRAND_BLUE, int(180 * bp)),
                    outline=(*LIGHT_BLUE, int(100 * bp)), width=2)
                canvas = Image.alpha_composite(canvas, badge_layer)
                draw = ImageDraw.Draw(canvas)
                btx = centered_x(text, self.font_medium)
                draw.text((btx, by), text, font=self.font_medium,
                          fill=(*WHITE, ba))

            if t >= 12.0:
                lp = ease_out_cubic(progress(t, 12.0, 12.5))
                local_text = "Window Depot USA of Milwaukee"
                lx = centered_x(local_text, self.font_body)
                ly = badge_y_base + 4 * 95 + 40
                draw.text((lx, ly), local_text, font=self.font_body,
                          fill=(*LIGHT_BLUE, int(255 * lp)))

            if t >= 12.5:
                lp2 = ease_out_cubic(progress(t, 12.5, 13.0))
                motto = "National Strength. Local Service."
                mx = centered_x(motto, self.font_small)
                my = badge_y_base + 4 * 95 + 110
                draw.text((mx, my), motto, font=self.font_small,
                          fill=(*GOLD, int(255 * lp2)))

        # ── PHASE 5: CTA (14.0–18.0s) ────────────────────────────────
        if t >= 14.0:
            cta_y_offset = int(H * (1 - ease_out_cubic(progress(t, 14.0, 14.6))))
            cta = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            cd = ImageDraw.Draw(cta)
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

            if t >= 14.8:
                tp = ease_out_cubic(progress(t, 14.8, 15.3))
                talk = "Talk directly with Nate"
                talk_x = centered_x(talk, self.font_medium)
                talk_y = SAFE_TOP + 330 + cta_y_offset
                draw.text((talk_x, talk_y), talk, font=self.font_medium,
                          fill=(*WHITE, int(255 * tp)))

            if t >= 15.0:
                pp = ease_out_cubic(progress(t, 15.0, 15.5))
                phone = "(414) 312-5213"
                phone_x = centered_x(phone, self.font_phone)
                phone_y = SAFE_TOP + 410 + cta_y_offset
                pulse = 0.6 + 0.4 * math.sin((t - 15.0) * 3.5)
                glow_a = int(120 * pp * pulse)
                text_glow(canvas, (phone_x, phone_y), phone,
                          self.font_phone, (*LIGHT_BLUE, glow_a), radius=20)
                draw = ImageDraw.Draw(canvas)
                draw.text((phone_x, phone_y), phone, font=self.font_phone,
                          fill=(*LIGHT_BLUE, int(255 * pp)))

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
                    radius=40, fill=(*BRAND_BLUE, btn_alpha))
                canvas = Image.alpha_composite(canvas, btn_layer)
                draw = ImageDraw.Draw(canvas)
                draw.text((btn_x + 40, btn_y + 12), btn_text,
                          font=self.font_cta_button, fill=(*WHITE, btn_alpha))

            if t >= 16.0:
                rp = ease_out_cubic(progress(t, 16.0, 16.5))
                for txt, y_off in [
                    ("FREE estimate  +  $500 gift card", 640),
                    ("Price locked 1 year", 690),
                ]:
                    rx = centered_x(txt, self.font_small)
                    draw.text((rx, SAFE_TOP + y_off + cta_y_offset), txt,
                              font=self.font_small, fill=(*GOLD, int(220 * rp)))

            if t >= 16.3:
                brp = ease_out_cubic(progress(t, 16.3, 16.8))
                brand = "WINDOW DEPOT USA OF MILWAUKEE"
                brx = centered_x(brand, self.font_brand)
                bry = SAFE_TOP + 770 + cta_y_offset
                draw.text((brx, bry), brand, font=self.font_brand,
                          fill=(*WHITE, int(180 * brp)))
                tag = "We Create Happy Customers"
                tagx = centered_x(tag, self.font_small)
                draw.text((tagx, bry + 50), tag, font=self.font_small,
                          fill=(*LIGHT_BLUE, int(160 * brp)))

        # ── Post-processing ───────────────────────────────────────────
        canvas = Image.alpha_composite(canvas, self.vignette)

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

        rgb = canvas.convert('RGB')

        # Color grading
        rgb = self._apply_color_grade(rgb, t)

        # Film grain
        rng = np.random.default_rng(frame_num)
        noise = rng.normal(0, 3, (H, W, 3)).astype(np.int16)
        arr = np.array(rgb, dtype=np.int16)
        arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(arr, 'RGB')

    # ── Render all frames + mux with audio ────────────────────────────
    def render(self, audio_path=None):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(CONTACT_DIR, exist_ok=True)

        cmd = [
            'ffmpeg', '-y', '-hide_banner', '-loglevel', 'warning',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24',
            '-s', f'{W}x{H}', '-r', str(FPS),
            '-i', 'pipe:0',
        ]
        if audio_path and os.path.exists(audio_path):
            cmd += ['-i', audio_path]
            cmd += [
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '23',
                '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '192k',
                '-t', str(DURATION),
                '-movflags', '+faststart',
                '-shortest',
                OUTPUT_FILE,
            ]
        else:
            cmd += [
                '-f', 'lavfi', '-i',
                f'anullsrc=channel_layout=mono:sample_rate={SR}',
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '23',
                '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '128k',
                '-t', str(DURATION),
                '-movflags', '+faststart',
                '-shortest',
                OUTPUT_FILE,
            ]

        print(f"[render] Starting FFmpeg…")
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
            if f % 60 == 0:
                elapsed = time.time() - t0
                fps_actual = (f + 1) / elapsed if elapsed > 0 else 0
                pct = (f + 1) / TOTAL_FRAMES * 100
                print(f"  [{f:>4}/{TOTAL_FRAMES}] {pct:5.1f}%  ({fps_actual:.1f} fps)")

        proc.stdin.close()
        proc.wait()
        print(f"[render] Done in {time.time() - t0:.1f}s → {OUTPUT_FILE}")
        return proc.returncode


# ══════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    audio_path = build_audio()
    renderer = ReelRenderer()
    rc = renderer.render(audio_path)
    sys.exit(rc)
