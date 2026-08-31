#!/usr/bin/env python3
"""
MAGICKMICA - recurate_issue.py
Re-picks the notes on a themed Y3K issue page (gothic.html etc.) from the
master archive, so the page actually matches its theme.

gothic.html was pulling six notes about sugar, sunshine, the sea and solar
spirits, with a mouse GIF for a cover. The layout was fine; the curation
was not. This scores every image note against a theme vocabulary, with a
ban list so bright/sunny notes can't score in, then rewrites the cards
and the cover in place. The page's own design is untouched.
"""
import json, re, html, os

THEMES = {
    "gothic": {
        "strong": ["gothic", "goth", "vampire", "crypt", "coffin", "raven", "graveyard",
                   "tomb", "mourning", "funeral", "obsidian", "onyx", "cobweb", "nocturne",
                   "requiem", "victorian", "cathedral", "crimson", "haunted", "haunting",
                   "midnight", "shadow", "skull", "ghost", "witch", "velvet",
                   "candlelit", "candlelight"],
        "soft": ["moth", "lace", "veil", "dusk", "eclipse", "thorn", "black", "dark",
                 "moon", "spider", "bat", "bone", "wither", "grim", "spell", "curse", "omen"],
        "ban": ["sunshine", "sunny", "summer", "beach", "ice cream", "rainbow", "glitter",
                "candy", "sugar", "bright", "solar", "tropical", "pastel"],
    },
}

NOTE_URL = "https://substack.com/@magickmica/note/c-{}"


def esc(s):
    return html.escape(s or "", quote=True)


def score(note, theme):
    b = (note.get("b") or "").lower()
    s = sum(4 for k in theme["strong"] if k in b)
    s += sum(1 for k in theme["soft"] if k in b)
    s -= sum(5 for k in theme["ban"] if k in b)
    return s


def pick(notes, theme, n, minimum=4):
    scored = [(score(x, theme), x) for x in notes if x.get("t")]
    good = [(s, x) for s, x in scored if s >= minimum]
    good.sort(key=lambda t: (-t[0], -(t[1].get("l") or 0)))
    return [x for _, x in good[:n]]


def quote_card(note):
    body = (note.get("b") or "").strip()[:100]
    return (f'<a class="quote-card" href="{NOTE_URL.format(note["id"])}" target="_blank" '
            f'rel="noopener"><div class="quote-card-img">'
            f'<img src="{esc(note["t"])}" alt="{esc(body[:70])}" loading="lazy" '
            f"""onerror="this.closest('.quote-card').style.display='none'"/></div>"""
            f'<div class="quote-card-body">{esc(body)}</div>'
            f'<div class="quote-card-footer"><span>\u2764 {note.get("l",0)}</span>'
            f'<span>VIEW \u2192</span></div></a>')


def recurate(path, out_path, notes, theme_key):
    theme = THEMES[theme_key]
    with open(path, encoding="utf-8") as f:
        page = f.read()

    grids = list(re.finditer(r'<div class="quote-grid">(.*?)</div>\s*</section>',
                             page, re.DOTALL))
    if not grids:
        grids = list(re.finditer(r'<div class="quote-grid">(.*?)</div>', page, re.DOTALL))

    needed = sum(max(1, g.group(1).count('class="quote-card"')) for g in grids)
    chosen = pick(notes, theme, needed + 1)
    if len(chosen) < needed:
        return None, 0, ""

    cover = chosen[0]
    pool = chosen[1:] if len(chosen) > needed else chosen
    idx = 0
    out = page
    for g in reversed(grids):
        count = max(1, g.group(1).count('class="quote-card"'))
        take = pool[max(0, len(pool) - idx - count):len(pool) - idx] if idx else pool[-count:]
        idx += count
        cards = "".join(quote_card(n) for n in take)
        out = out[:g.start(1)] + cards + out[g.end(1):]

    # cover image
    out = re.sub(r'(<img class="cover-img" src=")[^"]*(")',
                 lambda m: m.group(1) + cover["t"] + m.group(2), out, count=1)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    return chosen, needed, cover["t"]


if __name__ == "__main__":
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else "livecheck/magickmica.github.io-main/gothic.html"
    out = sys.argv[2] if len(sys.argv) > 2 else "preview/gothic.html"
    data = sys.argv[3] if len(sys.argv) > 3 else "_data/notes_with_media_compact.json"
    key = sys.argv[4] if len(sys.argv) > 4 else "gothic"

    notes = json.load(open(data, encoding="utf-8"))
    chosen, needed, cover = recurate(src, out, notes, key)
    if not chosen:
        print("not enough matching notes")
    else:
        print(f"recurated {needed} cards from {len(chosen)} candidates")
        for n in chosen[:10]:
            print(f'   \u2764{n["l"]:3} {(n.get("b") or "").splitlines()[0][:58]}')
