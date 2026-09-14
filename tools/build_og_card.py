#!/usr/bin/env python3
"""
Build og-card.png — the fallback social share image.

1200x630 is what Facebook, X, Discord, iMessage and Slack all crop to,
so the card is built at exactly that size with the important content
kept well inside the edges.

Painted rather than screenshotted because the site's own look comes from
webfonts and CSS gradients that don't survive a headless capture cleanly.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, pathlib

W, H = 1200, 630
VOID = (7, 6, 14)
PINK = (255, 155, 228)
CYAN = (123, 241, 228)
VIOLET = (155, 123, 255)
GOLD = (255, 217, 138)
PEARL = (236, 233, 247)

card = Image.new('RGB', (W, H), VOID)

# ── background: three soft colour pools, the same arrangement the pages use ──
glow = Image.new('RGB', (W, H), VOID)
gd = ImageDraw.Draw(glow)
for cx, cy, r, col, strength in [
    (int(W * 0.82), int(H * 0.06), 520, VIOLET, 0.34),
    (int(W * 0.10), int(H * 0.20), 430, PINK, 0.26),
    (int(W * 0.50), int(H * 1.02), 560, CYAN, 0.20),
]:
    for i in range(r, 0, -8):
        f = (1 - i / r) ** 2 * strength
        gd.ellipse([cx - i, cy - i, cx + i, cy + i],
                   fill=tuple(int(VOID[k] + (col[k] - VOID[k]) * f) for k in range(3)))
glow = glow.filter(ImageFilter.GaussianBlur(42))
card = Image.blend(card, glow, 0.95)

d = ImageDraw.Draw(card)

# ── starfield ──
import random
random.seed(7)
for _ in range(180):
    x, y = random.randint(0, W), random.randint(0, H)
    a = random.random()
    s = 1 if a < 0.8 else 2
    v = int(120 + 135 * a)
    d.ellipse([x, y, x + s, y + s], fill=(v, v, min(255, v + 12)))

# ── the character logo, with a halo so it reads on any backdrop ──
logo_path = pathlib.Path('magickmica-character-logo.png')
if logo_path.exists():
    logo = Image.open(logo_path).convert('RGBA')
    target_h = 300
    logo = logo.resize((int(logo.width * target_h / logo.height), target_h), Image.LANCZOS)
    lx, ly = 92, (H - target_h) // 2 - 10

    halo = Image.new('RGB', (W, H), VOID)
    hd = ImageDraw.Draw(halo)
    hcx, hcy, hr = lx + logo.width // 2, ly + target_h // 2, 220
    for i in range(hr, 0, -6):
        f = (1 - i / hr) ** 2 * 0.5
        hd.ellipse([hcx - i, hcy - i, hcx + i, hcy + i],
                   fill=tuple(int(VOID[k] + (PINK[k] - VOID[k]) * f) for k in range(3)))
    halo = halo.filter(ImageFilter.GaussianBlur(50))
    card = Image.blend(card, halo, 0.55)
    card.paste(logo, (lx, ly), logo)
    text_x = lx + logo.width + 56
else:
    text_x = 92

d = ImageDraw.Draw(card)
F = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
FM = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
title = ImageFont.truetype(F, 88)
sub = ImageFont.truetype(FM, 27)
kick = ImageFont.truetype(FM, 22)

# ── wordmark, letter by letter so it can carry the spectrum ──
ramp = [VIOLET, PINK, GOLD, CYAN, PINK, VIOLET]
def spectrum(n, i):
    t = i / max(1, n - 1) * (len(ramp) - 1)
    a, b = ramp[int(t)], ramp[min(len(ramp) - 1, int(t) + 1)]
    f = t - int(t)
    return tuple(int(a[k] + (b[k] - a[k]) * f) for k in range(3))

def draw_spectrum(text, x, y, font):
    for i, ch in enumerate(text):
        d.text((x, y), ch, font=font, fill=spectrum(len(text), i))
        x += d.textlength(ch, font=font)
    return x

ty = 196
d.text((text_x, ty - 46), '\u2726  MAGICK MICA  \u2726', font=kick, fill=CYAN)
draw_spectrum('MAGICK', text_x, ty, title)
draw_spectrum('MICA', text_x, ty + 96, title)

# ── spectrum rule ──
ry = ty + 206
for i in range(520):
    d.rectangle([text_x + i, ry, text_x + i + 1, ry + 3], fill=spectrum(520, i))

d.text((text_x, ry + 26), 'Where magic meets the pixel', font=sub, fill=PEARL)
d.text((text_x, ry + 64), 'magickmica.github.io', font=kick, fill=(157, 150, 184))

card.save('og-card.png', 'PNG', optimize=True)
print(f'og-card.png written · {card.size[0]}x{card.size[1]} · '
      f'{pathlib.Path("og-card.png").stat().st_size // 1024} KB')
