#!/usr/bin/env python3
"""
Build the link-preview cards for the Cosmic Circus and Winter Carnival pages.

Each page gets its own 1200x630 card in og/ (striped circus awning, the
game's name in the circus holo lettering, its line from the page, and a big
icon in a ring of marquee bulbs), and its og:image / twitter:image tags are
pointed at that card. Run from the repo root:

    python3 tools/build_circus_og.py          # images + tags
    python3 tools/build_circus_og.py --only ticket-booth

To add a page, add a line to PAGES. Fonts live in tools/fonts (OFL).
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import html, math, pathlib, random, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT / 'tools' / 'fonts'
SITE = 'https://magickmica.github.io/'
W, H = 1200, 630
STAR_FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

# colours from carnival.css
VOID = (4, 5, 9); NAVY = (19, 28, 63); INDIGO = (47, 47, 112); IRIS = (81, 70, 162)
ORCHID = (150, 103, 186); LILAC = (213, 194, 220); AQUA = (95, 243, 232)
PINK = (255, 79, 163); GOLD = (255, 209, 102); WHITE = (255, 255, 255)
ICE = (176, 226, 255)

# page: (title on the card, icon, winter?)
PAGES = {
    'arcade':                 ('The Cosmic Circus', '🎪', False),
    'cosmic-circus-broadcast': ('The Cosmic Circus Broadcast', '🎪', False),
    'ticket-booth':           ('Circus Ticket Booth', '🎟️', False),
    'my-prizes':              ('My Prizes', '🏆', False),
    'cosmic-clown-splash':    ('Cosmic Clown Splash', '🤡', False),
    'claw-machine':           ('Cosmic Claw Machine', '🧸', False),
    'coin-pusher':            ('Cosmic Coin Pusher', '🪙', False),
    'duck-pond':              ('Cosmic Duck Pond', '🦆', False),
    'ferris-wheel':           ('Cosmic Ferris Wheel', '🎡', False),
    'fortune-teller':         ("Madame Nebula's Fortunes", '🔮', False),
    'hoop-shot':              ('Big Top Hoop Shot', '🏀', False),
    'moon-striker':           ('Moon Striker', '🌙', False),
    'photo-booth':            ('Cosmic Photo Booth', '📸', False),
    'prize-wheel':            ('Cosmic Prize Wheel', '🎁', False),
    'ring-toss':              ('Saturn Ring Toss', '🪐', False),
    'shooting-gallery':       ('Star Blaster Gallery', '🛸', False),
    'skee-ball':              ('Skee-Ball to the Moon', '🎳', False),
    'star-darts':             ('Star Darts', '🎯', False),
    'whack-an-alien':         ('Whack-an-Alien', '👽', False),
    'winter-carnival':        ('Winter Carnival', '🎪', True),
    'crystal-chaos':          ('Crystal Chaos', '💎', True),
    'sled-hill':              ('Sled Hill', '🛷', True),
    'snowman-builder':        ('Snowman Builder', '⛄', True),
    'snowball-splat':         ('Snowball Splat', '❄️', True),
    'cocoa-catch':            ('Cocoa Catch', '☕', True),
}

TAGLINES = {  # used where the page's own description is too long for a card
    'arcade': 'Carnival games, a Ferris wheel ride and almost a hundred prizes.',
    'cosmic-circus-broadcast': 'A Magick Mica TV spectacle under the big top.',
    'winter-carnival': 'Sledding, snowmen, hot cocoa and 24 holiday prizes.',
}


def font(name, size, var=None):
    f = ImageFont.truetype(str(FONTS / name), size)
    if var:
        f.set_variation_by_name(var)
    return f


def mix(a, b, t):
    return tuple(int(a[k] + (b[k] - a[k]) * t) for k in range(3))


HOLO = [AQUA, LILAC, PINK, ORCHID, AQUA]


def holo(t):
    t = max(0.0, min(1.0, t)) * (len(HOLO) - 1)
    i = min(int(t), len(HOLO) - 2)
    return mix(HOLO[i], HOLO[i + 1], t - i)


def _add(a, b):
    from PIL import ImageChops
    return ImageChops.add(a, b)


def emoji(ch, size):
    """Noto Color Emoji only draws at 109px; draw there and scale."""
    f = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
    im = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((80, 80), ch, font=f, embedded_color=True, anchor='mm')
    im = im.crop(im.getbbox())
    s = size / max(im.size)
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines


def page_meta(slug):
    src = (ROOT / f'{slug}.html').read_text(encoding='utf-8')
    m = re.search(r'<meta (?:property|name)="og:description" content="([^"]*)"', src)
    return html.unescape(m.group(1)) if m else ''


def build(slug):
    title, icon, winter = PAGES[slug]
    tag = TAGLINES.get(slug) or page_meta(slug)
    stripe_a, stripe_b = (ICE, WHITE) if winter else (PINK, LILAC)
    accent = ICE if winter else PINK
    eyebrow = '✦ WINTER CARNIVAL ✦' if winter else '✦ COSMIC CIRCUS ✦'

    img = Image.new('RGB', (W, H), VOID)
    img = _add(img, _pool(W // 2, -40, 620, ORCHID, 0.55))
    img = _add(img, _pool(0, int(H * .55), 420, accent, 0.22))
    img = _add(img, _pool(W, int(H * .7), 420, AQUA, 0.18))
    d = ImageDraw.Draw(img)

    rnd = random.Random(slug)
    for _ in range(170):
        x, y = rnd.randint(0, W), rnd.randint(110, H)
        a = rnd.random()
        s = 1 if a < .8 else 2
        v = int(110 + 140 * a)
        d.ellipse([x, y, x + s, y + s], fill=(v, v, min(255, v + 14)))
    if winter:  # a little snowfall
        for _ in range(70):
            x, y, r = rnd.randint(0, W), rnd.randint(110, H), rnd.choice([2, 2, 3, 4])
            if x < 720 and 150 < y < H - 20:
                continue  # keep the flakes off the lettering
            d.ellipse([x - r, y - r, x + r, y + r], fill=mix(VOID, WHITE, rnd.uniform(.35, .8)))

    # awning: stripes, then scallops, then a bulb rail
    AW, SW = 74, 60
    for i in range(0, W // SW + 2):
        d.rectangle([i * SW, 0, i * SW + SW, AW], fill=stripe_a if i % 2 == 0 else stripe_b)
    shade = Image.new('L', (W, AW), 0)
    sd = ImageDraw.Draw(shade)
    for y in range(AW):
        sd.line([(0, y), (W, y)], fill=int(70 * (y / AW) ** 2))
    img.paste((0, 0, 0), (0, 0, W, AW), shade)
    d = ImageDraw.Draw(img)
    R = SW // 2
    for i in range(0, W // SW + 2):
        cx = i * SW + R
        d.ellipse([cx - R, AW - R + 2, cx + R, AW + R - 6], fill=stripe_a if i % 2 == 0 else stripe_b)
    rail_y = AW + R + 2
    d.rectangle([0, rail_y - 9, W, rail_y + 9], fill=NAVY)
    for i, x in enumerate(range(18, W, 36)):
        col = GOLD if i % 2 == 0 else AQUA
        _bulb(img, x, rail_y, 5, col)
    d = ImageDraw.Draw(img)

    # icon in a marquee ring (right)
    cx, cy, rr = 935, 360, 170
    img = _add(img, _pool(cx, cy, 300, accent, .45, 50))
    d = ImageDraw.Draw(img)
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=NAVY, outline=INDIGO, width=10)
    d.ellipse([cx - rr + 16, cy - rr + 16, cx + rr - 16, cy + rr - 16], outline=mix(NAVY, LILAC, .25), width=2)
    for k in range(24):
        a = k / 24 * math.tau
        _bulb(img, cx + (rr - 1) * math.cos(a), cy + (rr - 1) * math.sin(a), 6, GOLD if k % 2 == 0 else accent)
    em = emoji(icon, 210)
    shadow = Image.new('RGBA', em.size, (0, 0, 0, 0))
    shadow.putalpha(em.getchannel('A').point(lambda v: int(v * .55)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    img.paste(shadow, (cx - em.width // 2 + 6, cy - em.height // 2 + 12), shadow)
    img.paste(em, (cx - em.width // 2, cy - em.height // 2), em)
    d = ImageDraw.Draw(img)

    # text (left)
    x0, maxw = 70, 640
    # Silkscreen has no ✦, so the sparkles come from DejaVu
    ef, sf = font('Silkscreen-Regular.ttf', 26), ImageFont.truetype(STAR_FONT, 26)
    ex = x0
    for part in eyebrow.split(' '):
        f = sf if part == '✦' else ef
        d.text((ex, 170), part, font=f, fill=AQUA)
        ex += d.textlength(part + ' ', font=f) + 6
    for size in (92, 84, 76, 68, 60, 54):
        tf = font('Orbitron-VF.ttf', size, 'Black')
        lines = wrap(d, title.upper(), tf, maxw)
        if len(lines) <= 2 and all(d.textlength(l, font=tf) <= maxw for l in lines):
            break
    y = 214
    lh = int(size * 1.08)
    text_h = lh * len(lines)
    # holo-filled title with a pink glow behind it
    mask = Image.new('L', (W, H), 0)
    md = ImageDraw.Draw(mask)
    for i, l in enumerate(lines):
        md.text((x0, y + i * lh), l, font=tf, fill=255)
    glow = Image.new('RGB', (W, H), (0, 0, 0))
    glow.paste(accent, (0, 0), mask.filter(ImageFilter.GaussianBlur(14)))
    img = _add(img, glow.point(lambda v: int(v * .45)))
    grad = Image.new('RGB', (W, H))
    gd = ImageDraw.Draw(grad)
    for gx in range(x0, x0 + maxw + 1):
        gd.line([(gx, 0), (gx, H)], fill=holo((gx - x0) / maxw))
    img.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(img)

    ty = y + text_h + 22
    tagf = font('IBMPlexMono-Medium.ttf', 27)
    for l in wrap(d, tag, tagf, maxw - 20)[:3]:
        d.text((x0, ty), l, font=tagf, fill=LILAC)
        ty += 38

    # footer ticket strip
    fy = H - 66
    foot = font('Silkscreen-Regular.ttf', 22)
    label = 'MAGICK MICA ARCADE'
    lw = d.textlength(label, font=foot)
    d.rounded_rectangle([x0 - 4, fy - 10, x0 + lw + 34, fy + 34], radius=8, fill=accent)
    d.text((x0 + 15, fy - 2), label, font=foot, fill=VOID)
    d.text((x0 + lw + 54, fy + 2), 'magickmica.github.io', font=font('IBMPlexMono-Medium.ttf', 22), fill=mix(LILAC, VOID, .3))

    out = ROOT / 'og' / f'{slug}.png'
    img.save(out, 'PNG', optimize=True)
    return out


def _pool(cx, cy, r, col, strength, blur=40):
    layer = Image.new('RGB', (W, H), (0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i in range(r, 0, -8):
        f = (1 - i / r) ** 2 * strength
        d.ellipse([cx - i, cy - i, cx + i, cy + i], fill=mix((0, 0, 0), col, f))
    return layer.filter(ImageFilter.GaussianBlur(blur))


def _bulb(img, x, y, r, col):
    g = Image.new('RGBA', (r * 8, r * 8), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    c = r * 4
    gd.ellipse([c - r * 3, c - r * 3, c + r * 3, c + r * 3], fill=col + (70,))
    g = g.filter(ImageFilter.GaussianBlur(r))
    gd = ImageDraw.Draw(g)
    gd.ellipse([c - r, c - r, c + r, c + r], fill=col + (255,))
    gd.ellipse([c - r // 2 - 1, c - r // 2 - 1, c, c], fill=mix(col, WHITE, .7) + (255,))
    img.paste(g, (int(x - c), int(y - c)), g)


def retag(slug):
    """Point og:image at the card and make sure twitter:image + size tags exist."""
    path = ROOT / f'{slug}.html'
    src = path.read_text(encoding='utf-8')
    url = f'{SITE}og/{slug}.png'
    alt = f'{PAGES[slug][0]} · Magick Mica Arcade'
    src = re.sub(r'\n?<meta (?:property|name)="(?:og:image(?::width|:height|:alt)?|twitter:image(?::alt)?)" content="[^"]*">', '', src)
    tags = (f'<meta property="og:image" content="{url}">\n'
            f'<meta property="og:image:width" content="1200">\n'
            f'<meta property="og:image:height" content="630">\n'
            f'<meta property="og:image:alt" content="{html.escape(alt)}">\n'
            f'<meta name="twitter:image" content="{url}">')
    src, n = re.subn(r'(<meta name="twitter:card" content="[^"]*">)', tags + r'\n\1', src, count=1)
    if not n:
        src, n = re.subn(r'(</head>)', tags + r'\n\1', src, count=1)
    path.write_text(src, encoding='utf-8')


if __name__ == '__main__':
    only = sys.argv[sys.argv.index('--only') + 1:] if '--only' in sys.argv else list(PAGES)
    (ROOT / 'og').mkdir(exist_ok=True)
    for slug in only:
        out = build(slug)
        if '--no-tags' not in sys.argv:
            retag(slug)
        print(f'{out.relative_to(ROOT)} · {out.stat().st_size // 1024} KB')
