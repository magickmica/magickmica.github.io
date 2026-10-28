#!/usr/bin/env python3
"""
MAGICKMICA - tools/build_whatsnew.py  ·  the "New this week" upgrade for the homepage

Adds a NEW THIS WEEK section to the homepage, right under the big tile mosaic:
  - the newest article as a large picture card, plus the next two
  - this week's notes per day, as a little signal band
  - a reel of this week's most-loved notes, each a tiny TV screen
and gives the CH 02 "This Week" tile the cover of the newest Y3K issue.

Two modes, chosen automatically:
  PREVIEW  index.html has no <!--ONAIR:new--> marker yet.
           index.html is left alone; a copy with the new section is written to
           home-preview.html, so you can look at it first.
  LIVE     index.html contains <!--ONAIR:new--><!--/ONAIR:new-->.
           The section between those markers is refilled in place.
           Going live = paste that one marker line into index.html where the
           section should sit (under the mosaic), then delete home-preview.html.

Run by tools/update_all.py on every update (after update_pages and update_home),
so the section always shows the newest notes and articles. Only writes when
something changed.
"""
import datetime as dt
import html
import json
import os
import re
import sys
from urllib.parse import quote, unquote

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)
DATA = os.path.join(REPO, "_data")
HOME = os.path.join(REPO, "index.html")
PREVIEW = os.path.join(REPO, "home-preview.html")

REEL = 12
COVER_CDN = ("https://substackcdn.com/image/fetch/"
             "$s_!G4Yk!,w_600,c_limit,f_webp,q_auto:good,fl_progressive:steep/")
S3 = "https://substack-post-media.s3.amazonaws.com/public/images/"
MARK = re.compile(r"(<!--ONAIR:new-->).*?(<!--/ONAIR:new-->)", re.S)
ANCHOR = '<div class="sect"><h2 class="holo">Y3K MAGAZINE</h2>'
CH02 = re.compile(r'(<a class="tile w2 h2" href="minimags\.html">)'
                  r'(?:<img class="nw-cov" src="[^"]*" alt="" loading="lazy" onerror="this\.remove\(\)"><div class="scrim"></div>)?')
FIRST_ISSUE_IMG = re.compile(r'<div class="mag-card-cover">\s*<img[^>]*?src="([^"]+)"')

e = lambda s: html.escape(str(s or ""), quote=True)


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def cover_600(url):
    if not url:
        return ""
    raw = unquote(url.rsplit("/https%3A", 1)[-1]) if "/https%3A" in url else url
    if not raw.startswith("http"):
        raw = "https:" + raw
    return COVER_CDN + quote(raw, safe="") if raw.startswith(S3) else url


def day(s):
    return dt.date.fromisoformat(s[:10])


def md(d):
    return d.strftime("%b ").upper() + str(d.day)


def clean(t, n):
    t = re.sub(r"\s+", " ", t or "").strip()
    return t if len(t) <= n else t[: n - 1].rsplit(" ", 1)[0] + "…"


CSS = """<style>
/* ---- NEW THIS WEEK (tools/build_whatsnew.py) ---- */
.nw-grid{display:grid;grid-template-columns:1.55fr 1fr;gap:12px}
.nw-noimg{background:radial-gradient(circle at 30% 30%,color-mix(in srgb,var(--pink) 30%,transparent),transparent 60%),
  linear-gradient(135deg,color-mix(in srgb,var(--purple) 40%,var(--deep)),color-mix(in srgb,var(--cyan) 22%,var(--deep)))!important}
.nw-lead{position:relative;display:flex;flex-direction:column;justify-content:flex-end;min-height:400px;border-radius:20px;overflow:hidden;
  border:1px solid color-mix(in srgb,var(--pink) 45%,transparent);background:var(--surface);padding:26px 26px 24px;
  box-shadow:0 0 40px -14px color-mix(in srgb,var(--pink) 60%,transparent);transition:transform .2s ease}
.nw-lead:hover{transform:translateY(-3px)}
.nw-lead>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;transition:transform .8s ease}
.nw-lead:hover>img{transform:scale(1.04)}
.nw-lead .scrim{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,transparent 20%,color-mix(in srgb,var(--deep) 94%,transparent) 88%)}
.nw-lead .in{position:relative;z-index:3}
.nw-lead .eyebrow{font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.24em;text-transform:uppercase;color:var(--gold);margin-top:12px}
.nw-lead h3{font-family:Orbitron,monospace;font-size:28px;line-height:1.15;margin:8px 0;max-width:640px;
  background:linear-gradient(100deg,#fff 10%,var(--gold) 45%,var(--pink) 75%,var(--cyan));-webkit-background-clip:text;background-clip:text;
  color:transparent;-webkit-text-fill-color:transparent;filter:drop-shadow(0 2px 10px rgba(0,0,0,.7))}
.nw-lead .sub{font-size:13px;line-height:1.6;color:#d9cfee;max-width:520px}
.nw-go{display:inline-flex;align-items:center;gap:9px;margin-top:14px;padding:11px 20px;border-radius:999px;font-family:Silkscreen,monospace;
  font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#1a0710;background:linear-gradient(90deg,var(--gold),var(--pink));
  box-shadow:0 0 22px -4px color-mix(in srgb,var(--pink) 70%,transparent)}
.nw-lead:hover .nw-go span:last-child{transform:translateX(4px)}
.nw-lead:hover .sheen{transform:translateX(120%)}
.nw-lead .live{margin-bottom:0;background:color-mix(in srgb,var(--deep) 55%,transparent)}
.nw-reelhd .live{margin:0 8px 0 0;padding:3px 8px}
.nw-go span:last-child{transition:transform .25s}
.nw-side{display:grid;grid-template-rows:1fr 1fr auto;gap:12px}
.nw-art{position:relative;display:flex;flex-direction:column;justify-content:flex-end;min-height:128px;border-radius:14px;overflow:hidden;padding:14px 15px;
  border:1px solid color-mix(in srgb,var(--purple) 30%,transparent);background:var(--surface);transition:transform .18s,border-color .18s}
.nw-art:hover{transform:translateY(-2px);border-color:color-mix(in srgb,var(--gold) 55%,transparent)}
.nw-art>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.62;z-index:0}
.nw-art .scrim{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,transparent 15%,color-mix(in srgb,var(--deep) 92%,transparent))}
.nw-art .in{position:relative;z-index:2}
.nw-art .lab{font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.2em;color:var(--cyan)}
.nw-art .ttl{font-size:14px;font-weight:500;margin-top:5px;line-height:1.3}
.nw-band{border-radius:14px;border:1px solid color-mix(in srgb,var(--purple) 30%,transparent);background:var(--surface);padding:13px 15px 10px}
.nw-band .hd{display:flex;justify-content:space-between;gap:8px;font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.18em;color:#8e85ad}
.nw-band .hd b{color:var(--gold);font-weight:400}
.nw-bars{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;align-items:end;height:74px;margin-top:10px}
.nw-bars a{display:flex;flex-direction:column;justify-content:flex-end;align-items:stretch;height:100%;text-align:center}
.nw-bars i{display:block;border-radius:3px 3px 0 0;min-height:3px;background:linear-gradient(0deg,var(--purple),var(--pink) 55%,var(--gold));
  box-shadow:0 0 10px color-mix(in srgb,var(--pink) 50%,transparent)}
.nw-bars a:hover i{background:linear-gradient(0deg,var(--cyan),var(--gold))}
.nw-bars small{font-family:Silkscreen,monospace;font-size:8px;letter-spacing:.1em;color:#7a6f9e;padding-top:5px}
.nw-reelhd{display:flex;align-items:center;gap:12px;margin:18px 0 10px}
.nw-reelhd .lab{font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.22em;color:#8e85ad}
.nw-reelhd a.all{margin-left:auto;font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.18em;color:var(--gold)}
.nw-reelhd button{width:30px;height:30px;border-radius:50%;cursor:pointer;color:var(--ink);font-size:12px;
  border:1px solid color-mix(in srgb,var(--purple) 40%,transparent);background:var(--surface)}
.nw-reelhd button:hover{border-color:var(--gold);color:var(--gold)}
.nw-reel{display:grid;grid-auto-flow:column;grid-auto-columns:calc((100% - 5*12px)/6);gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;
  padding:4px 2px 10px;scrollbar-width:thin;scrollbar-color:color-mix(in srgb,var(--purple) 50%,transparent) transparent}
.nw-crt{position:relative;display:block;scroll-snap-align:start;aspect-ratio:4/3;border-radius:12px;overflow:hidden;background:#05040c;
  border:3px solid #1c1424;box-shadow:0 0 0 1px color-mix(in srgb,var(--purple) 30%,transparent),0 10px 22px -12px #000;transition:transform .2s,box-shadow .2s}
.nw-crt:hover{transform:translateY(-3px);box-shadow:0 0 0 1px var(--pink),0 0 22px -4px color-mix(in srgb,var(--pink) 70%,transparent)}
.nw-crt img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.92}
.nw-crt::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:repeating-linear-gradient(0deg,rgba(0,0,0,.28) 0 1px,transparent 1px 3px),radial-gradient(120% 100% at 50% 50%,transparent 55%,rgba(0,0,0,.6))}
.nw-crt .ch{position:absolute;z-index:2;top:6px;left:8px;font-family:Silkscreen,monospace;font-size:8px;letter-spacing:.14em;color:var(--lime);text-shadow:0 0 6px var(--lime)}
.nw-crt .hv{position:absolute;z-index:2;bottom:6px;right:8px;font-family:Silkscreen,monospace;font-size:9px;color:#fff;text-shadow:0 1px 4px #000}
.nw-crt .q{position:absolute;z-index:2;left:8px;right:8px;bottom:22px;font-size:10.5px;line-height:1.35;color:#fff;text-shadow:0 1px 6px #000;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;opacity:0;transition:opacity .2s}
.nw-crt:hover .q,.nw-crt:focus-visible .q,.nw-crt.nw-noimg .q{opacity:1}
.tile>img.nw-cov{opacity:.62}
@media(max-width:820px){
  .nw-grid{grid-template-columns:1fr}
  .nw-lead{min-height:330px;padding:20px}
  .nw-lead h3{font-size:21px}
  .nw-side{grid-template-rows:none;grid-template-columns:1fr 1fr}
  .nw-band{grid-column:1/-1}
  .nw-reel{grid-auto-columns:42%}
  .nw-reelhd{flex-wrap:wrap;gap:8px}
  .nw-reelhd button{display:none}
  .nw-reelhd .lab{flex-basis:100%;order:2}
  .nw-reelhd a.all{order:1;margin-left:auto}
}
@media(prefers-reduced-motion:reduce){.nw-lead,.nw-lead>img,.nw-art,.nw-crt{transition:none}}
</style>"""

JS = """<script>
(function(){
  var r=document.getElementById('nw-reel');if(!r)return;
  function step(d){var c=r.querySelector('.nw-crt');var w=c?c.getBoundingClientRect().width+12:200;
    r.scrollBy({left:d*w*2,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});}
  var p=document.getElementById('nw-prev'),n=document.getElementById('nw-next');
  p&&p.addEventListener('click',function(){step(-1)});n&&n.addEventListener('click',function(){step(1)});
})();
</script>"""

FB = "this.parentElement.classList.add('nw-noimg');this.remove()"


def section(notes, articles):
    last = max(day(n["d"]) for n in notes)
    first = last - dt.timedelta(days=6)
    week = [n for n in notes if first <= day(n["d"]) <= last]
    loves = sum(n.get("l", 0) for n in week)

    arts = sorted(articles, key=lambda a: (a.get("date", ""), a.get("published", "")), reverse=True)
    a0 = arts[0]
    d0 = day(a0["date"])

    def img(url, extra=""):
        return f'<img src="{e(url)}" alt="" loading="lazy" onerror="{FB}"{extra}>' if url else ""

    c0 = cover_600(a0.get("cover_url"))
    lead = (f'<a class="nw-lead{"" if c0 else " nw-noimg"}" href="{e(a0.get("url"))}" target="_blank" rel="noopener">'
            f'{img(c0)}<div class="scrim"></div><div class="sheen" aria-hidden="true"></div><div class="in">'
            f'<div class="live"><b></b>Just aired · {e(a0.get("newsletter") or "Substack")}</div>'
            f'<div class="eyebrow">✦ {d0.strftime("%A").upper()} · {md(d0)} ✦</div>'
            f'<h3>{e(a0.get("title", "").strip())}</h3>'
            f'<div class="sub">{e(clean(a0.get("subtitle") or a0.get("preview"), 200))}</div>'
            f'<div class="nw-go"><span>Read it</span><span>→</span></div></div></a>')

    side = []
    for a in arts[1:3]:
        c = cover_600(a.get("cover_url"))
        side.append(f'<a class="nw-art{"" if c else " nw-noimg"}" href="{e(a.get("url"))}" target="_blank" rel="noopener">{img(c)}'
                    f'<div class="scrim"></div><div class="in"><div class="lab">{e((a.get("newsletter") or "").upper())} · {md(day(a["date"]))}</div>'
                    f'<div class="ttl">{e(a.get("title", "").strip())}</div></div></a>')

    days = [first + dt.timedelta(days=k) for k in range(7)]
    per = {d: sum(1 for n in week if day(n["d"]) == d) for d in days}
    top = max(per.values()) or 1
    bars = "".join(f'<a href="notes.html" title="{per[d]} notes on {d.strftime("%A %b ")}{d.day}">'
                   f'<i style="height:{max(3, round(54 * per[d] / top))}px"></i><small>{d.strftime("%a").upper()}</small></a>'
                   for d in days)
    band = (f'<div class="nw-band"><div class="hd"><span>THIS WEEK ON THE SIGNAL</span>'
            f'<span><b>{len(week)}</b> NOTES · <b>{loves:,}</b> ♥</span></div><div class="nw-bars">{bars}</div></div>')

    pics = sorted((n for n in week if n.get("t")), key=lambda n: (-n.get("l", 0), -n.get("r", 0), n["d"]))
    if len(pics) < REEL:
        seen = {n["id"] for n in pics}
        pics += sorted((n for n in notes if n.get("t") and n["id"] not in seen and day(n["d"]) < first),
                       key=lambda n: n["d"], reverse=True)[: REEL - len(pics)]
    reel = []
    for k, n in enumerate(pics[:REEL]):
        q = clean(n.get("b"), 90)
        reel.append(f'<a class="nw-crt" href="https://substack.com/@magickmica/note/c-{n["id"]}" target="_blank" rel="noopener" '
                    f'aria-label="Note from {md(day(n["d"]))}: {e(q or "image")}">'
                    f'<img src="{e(n["t"])}" alt="" loading="lazy" onerror="{FB}">'
                    f'<span class="ch">CH {k + 1:02d} · {md(day(n["d"]))}</span>'
                    f'{f"<span class=q>{e(q)}</span>" if q else ""}<span class="hv">♥ {n.get("l", 0)}</span></a>')

    rng = f'{md(first)}–{md(last) if last.month != first.month else last.day}'
    return (f'{CSS}<section class="nw" aria-label="New this week">'
            f'<div class="sect"><h2 class="holo">✦ NEW THIS WEEK</h2><div class="rule"></div>'
            f'<span class="meta">{rng} · {len(week)} TRANSMISSIONS</span></div>'
            f'<div class="nw-grid">{lead}<div class="nw-side">{"".join(side)}{band}</div></div>'
            f'<div class="nw-reelhd"><span class="lab"><span class="live"><b></b>On air</span>THIS WEEK\'S MOST-LOVED NOTES</span>'
            f'<a class="all" href="notes.html">ALL NOTES →</a>'
            f'<button type="button" id="nw-prev" aria-label="Scroll notes back">◀</button>'
            f'<button type="button" id="nw-next" aria-label="Scroll notes forward">▶</button></div>'
            f'<div class="nw-reel" id="nw-reel">{"".join(reel)}</div></section>{JS}')


def ch02_cover(page):
    m = FIRST_ISSUE_IMG.search(page)
    if not m:
        return page
    tag = (f'<img class="nw-cov" src="{m.group(1)}" alt="" loading="lazy" onerror="this.remove()">'
           f'<div class="scrim"></div>')
    return CH02.sub(lambda x: x.group(1) + tag, page, count=1)


def main():
    notes = load("notes_with_media_compact.json")
    articles = load("magazine_articles.json")
    block = section(notes, articles)
    with open(HOME, encoding="utf-8") as f:
        home = f.read()

    if MARK.search(home):                       # LIVE: refill index.html in place
        new = ch02_cover(MARK.sub(lambda m: m.group(1) + block + m.group(2), home, count=1))
        target = HOME
    else:                                       # PREVIEW: index.html untouched
        if ANCHOR not in home:
            print("whatsnew: couldn't find the Y3K MAGAZINE heading in index.html; nothing written")
            return 1
        new = home.replace(ANCHOR, "<!--ONAIR:new-->" + block + "<!--/ONAIR:new-->\n\n" + ANCHOR, 1)
        new = ch02_cover(new)
        new = new.replace("<head>", '<head><meta name="robots" content="noindex">', 1)
        target = PREVIEW

    old = ""
    if os.path.exists(target):
        with open(target, encoding="utf-8") as f:
            old = f.read()
    name = os.path.basename(target)
    if new != old:
        with open(target, "w", encoding="utf-8") as f:
            f.write(new)
        print(f"whatsnew: {name} updated")
    else:
        print(f"whatsnew: {name} already current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
