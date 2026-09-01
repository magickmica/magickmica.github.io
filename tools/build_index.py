#!/usr/bin/env python3
"""
MAGICKMICA - build_index.py
Generates index.html and all 15 index-*.html from ONE mosaic template
plus _data/themes.json.

Direction C: a tile grid where tile size signals importance. Big tiles
carry artwork, small tiles stay text. Collapses to one column on mobile
without a separate layout.

To restyle every frequency at once, edit TEMPLATE / CSS here and rerun.
To retheme one page, edit its entry in _data/themes.json.

    python3 tools/build_index.py <repo> _data build
"""
import json, os, html, datetime
from ctas import CTA_CSS, CTA_JS, CTAS
from chrome import chrome_for

SITE = "https://magickmica.github.io/"


def esc(s):
    return html.escape(str(s or ""), quote=True)


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
a{color:inherit;text-decoration:none}
body{background:var(--deep);color:var(--ink);font-family:'IBM Plex Mono',ui-monospace,monospace;
-webkit-font-smoothing:antialiased;overflow-x:hidden}
#stars{position:fixed;inset:0;pointer-events:none;z-index:0;
background-image:radial-gradient(1px 1px at 20% 30%,rgba(255,255,255,.5),transparent),
radial-gradient(1px 1px at 70% 60%,rgba(255,255,255,.35),transparent),
radial-gradient(1px 1px at 45% 85%,rgba(255,255,255,.4),transparent);background-size:300px 300px}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px 64px;position:relative;z-index:1}
.holo{background:linear-gradient(115deg,var(--purple),var(--pink) 30%,var(--gold) 55%,var(--cyan) 80%,var(--purple));
-webkit-background-clip:text;background-clip:text;color:transparent}
.top{display:flex;align-items:center;gap:16px;padding:14px 0 18px;flex-wrap:wrap}
.brand{font-family:Orbitron,monospace;font-weight:700;font-size:15px;letter-spacing:.16em}
.top nav{display:flex;gap:14px;font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:#9d94bd}
.top nav a:hover{color:var(--gold)}
.chnow{margin-left:auto;font-family:Silkscreen,monospace;font-size:10px;letter-spacing:.16em;color:var(--gold)}
.mos{display:grid;grid-template-columns:repeat(6,1fr);grid-auto-rows:104px;gap:12px}
.tile{position:relative;overflow:hidden;border-radius:14px;padding:15px;display:flex;flex-direction:column;
justify-content:flex-end;border:1px solid color-mix(in srgb,var(--purple) 30%,transparent);
background:var(--surface);transition:transform .18s ease,border-color .18s ease}
.tile:hover{transform:translateY(-2px);border-color:color-mix(in srgb,var(--pink) 55%,transparent)}
.tile .lab{font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.2em;color:#8e85ad}
.tile .ttl{font-size:15px;font-weight:500;margin-top:5px;line-height:1.25}
.tile .sm{font-size:11px;color:#9d94bd;margin-top:4px;line-height:1.5}
.tile>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.5;z-index:0}
.tile .in{position:relative;z-index:2}
.tile .scrim{position:absolute;inset:0;z-index:1;
background:linear-gradient(180deg,transparent 25%,color-mix(in srgb,var(--deep) 88%,transparent) 100%)}
.hero{grid-column:span 4;grid-row:span 4}
.hero .ttl{font-family:Orbitron,monospace;font-size:clamp(22px,3vw,32px);line-height:1.03;color:#fff}
.hero-logo{width:min(44%,244px);height:auto;display:block;margin:0 0 10px;
filter:drop-shadow(0 0 26px color-mix(in srgb,var(--pink) 42%,transparent))
drop-shadow(0 0 54px color-mix(in srgb,var(--cyan) 22%,transparent));
animation:logoGlow 4.6s ease-in-out infinite}
@keyframes logoGlow{0%,100%{filter:drop-shadow(0 0 22px color-mix(in srgb,var(--pink) 38%,transparent))
drop-shadow(0 0 46px color-mix(in srgb,var(--cyan) 18%,transparent))}
50%{filter:drop-shadow(0 0 34px color-mix(in srgb,var(--purple) 52%,transparent))
drop-shadow(0 0 70px color-mix(in srgb,var(--gold) 26%,transparent))}}
.live{display:inline-flex;align-items:center;gap:7px;font-size:9px;letter-spacing:.24em;
text-transform:uppercase;color:var(--lime);border:1px solid color-mix(in srgb,var(--lime) 34%,transparent);
border-radius:99px;padding:4px 10px;margin-bottom:12px;width:max-content}
.live b{width:6px;height:6px;border-radius:50%;background:var(--lime);animation:pulse 1.7s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.7)}}
.hero .sm{font-size:12.5px;color:#d9cfff;max-width:420px}
.tv{grid-column:span 2;grid-row:span 4;border-color:color-mix(in srgb,var(--cyan) 40%,transparent)}
.w2{grid-column:span 2}
.w3{grid-column:span 3}
.h2{grid-row:span 2}
.pill{position:absolute;top:12px;right:12px;z-index:3;font-size:9px;letter-spacing:.16em;
padding:4px 9px;border-radius:99px;border:1px solid color-mix(in srgb,var(--cyan) 50%,transparent);color:var(--cyan)}
.sect{display:flex;align-items:baseline;gap:12px;margin:34px 0 14px}
.sect h2{font-family:Orbitron,monospace;font-size:13px;letter-spacing:.18em}
.sect .rule{flex:1;height:1px;background:color-mix(in srgb,var(--purple) 28%,transparent)}
.sect .meta{font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.16em;color:#7a6f9e}
.mag-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.mag-card{border:1px solid color-mix(in srgb,var(--purple) 26%,transparent);border-radius:12px;overflow:hidden;background:var(--surface)}
.mag-card:hover{border-color:color-mix(in srgb,var(--gold) 55%,transparent)}
.mag-card-cover{position:relative;aspect-ratio:1;overflow:hidden}
.mag-card-cover img{width:100%;height:100%;object-fit:cover}
.mag-card-overlay{position:absolute;inset:0;background:linear-gradient(180deg,transparent 55%,rgba(0,0,0,.72))}
.mag-card-count{position:absolute;left:10px;bottom:9px;font-family:Silkscreen,monospace;font-size:9px;
letter-spacing:.14em;color:var(--gold)}
.mag-card-label{padding:9px 11px;font-size:12px}
.mag-card-cover.no-img{background:color-mix(in srgb,var(--purple) 22%,var(--deep))}
/* Random Note TV: a real screen, not an empty panel */
.tv{padding:0;overflow:hidden}
#mtv{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:flex-end;
padding:0;background:#05040c;cursor:pointer}
#mtv .screen{position:absolute;inset:0;overflow:hidden;background:#05040c}
#mtv .screen img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.92}
#mtv .static{position:absolute;inset:-60%;opacity:.2;pointer-events:none;mix-blend-mode:screen;
background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)' opacity='0.7'/%3E%3C/svg%3E");
background-size:180px 180px;animation:tvNoise .22s steps(3) infinite;transition:opacity .18s}
@keyframes tvNoise{0%{transform:translate(0,0)}25%{transform:translate(-3%,2%)}
50%{transform:translate(2%,-3%)}75%{transform:translate(-2%,-1%)}100%{transform:translate(1%,3%)}}
#mtv .scan{position:absolute;inset:0;pointer-events:none;
background:repeating-linear-gradient(0deg,rgba(0,0,0,.34) 0 1px,transparent 1px 3px)}
#mtv .sweep{position:absolute;left:0;right:0;height:64px;pointer-events:none;
background:linear-gradient(180deg,transparent,rgba(255,255,255,.07) 45%,transparent);
animation:tvSweep 5.5s linear infinite}
@keyframes tvSweep{0%{top:-64px}100%{top:100%}}
#mtv .vig{position:absolute;inset:0;pointer-events:none;
box-shadow:inset 0 0 60px rgba(0,0,0,.75);border-radius:14px}
#mtv .cap{position:relative;z-index:3;margin:14px;padding:12px 13px;border-radius:10px;
background:rgba(5,4,12,.78);backdrop-filter:blur(4px);
border:1px solid color-mix(in srgb,var(--cyan) 26%,transparent)}
#mtv .body{font-size:13.5px;line-height:1.5}
#mtv .meta{font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.16em;color:var(--cyan)}
#mtv .meta+.body{margin-top:5px}
#mtv .body+.meta{margin-top:6px}
@media(prefers-reduced-motion:reduce){#mtv .static,#mtv .sweep{animation:none}}
footer{margin-top:44px;padding-top:20px;border-top:1px solid color-mix(in srgb,var(--purple) 24%,transparent);
font-size:11px;color:#8e85ad;line-height:1.9}
footer a{color:var(--pink)}
.strip3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.cta-row{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.cta-row .cta{padding:26px 24px 22px}
.cta-row .cta h3{font-size:21px}
.cta-row .cta .sub{font-size:12px;max-width:none}
.cta-row .art{width:84px;height:84px;overflow:visible}
.cta-row .box{transform:scale(.86);transform-origin:center}
.cta-row .hstack{transform:scale(.88);transform-origin:center}
.cta-row .in{gap:18px}
.scard{border:1px solid color-mix(in srgb,var(--purple) 26%,transparent);border-radius:12px;
padding:16px;background:var(--surface)}
.scard:hover{border-color:color-mix(in srgb,var(--gold) 50%,transparent)}
.scard .lab{font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.2em;color:#8e85ad}
.scard .ttl{font-size:15px;font-weight:500;margin-top:6px}
.scard .sm{font-size:11px;color:#9d94bd;margin-top:4px;line-height:1.5}
.star{display:block;text-align:center;border-radius:14px;padding:22px;
border:1px solid color-mix(in srgb,var(--gold) 45%,transparent);background:var(--surface)}
.star .big{font-family:Orbitron,monospace;font-size:19px;color:var(--gold);margin:8px 0 6px}
.star .sm{font-size:12px;color:#9d94bd}
.tmap{margin-top:36px;padding:26px 22px;border-radius:18px;
border:1px solid color-mix(in srgb,var(--purple) 30%,transparent);background:var(--surface)}
.tmap h2{font-family:Orbitron,monospace;font-size:13px;letter-spacing:.18em;margin-bottom:16px}
.tmap-cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));gap:20px 22px;align-items:start}
.tmap-col{break-inside:avoid}
.tmap-col.wide{grid-column:span 2}
.tmap-col.wide .links{columns:2;column-gap:22px}
.tmap-col h3{font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.22em;color:var(--gold);
margin-bottom:9px;text-transform:uppercase}
.tmap-col a{display:block;font-size:12px;color:#b8b0d4;padding:3px 0;line-height:1.5}
.tmap-col a:hover{color:var(--pink)}
@media(max-width:820px){.mos{grid-template-columns:repeat(2,1fr);grid-auto-rows:96px}
.hero{grid-column:span 2;grid-row:span 3}.tv{grid-column:span 2;grid-row:span 2}
.w2,.w3{grid-column:span 2}.mag-grid{grid-template-columns:repeat(2,1fr)}.strip3{grid-template-columns:1fr}.cta-row{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){.tile{transition:none}
.hero-logo,.live b{animation:none}}
"""

MTV_JS = """
(function(){
 var el=document.getElementById('mtv');
 if(!el||typeof MTV_NOTES==='undefined'||!MTV_NOTES.length)return;
 // prefer notes that have artwork so the screen actually shows something
 var withArt=MTV_NOTES.filter(function(n){return n.t;});
 var pool=withArt.length>8?withArt:MTV_NOTES;
 el.innerHTML='<div class="screen"><img alt="" /><div class="static"></div>'+
  '<div class="scan"></div><div class="sweep"></div></div><div class="vig"></div>'+
  '<div class="cap"><div class="meta">CH 01 \\u00b7 RANDOM NOTE TV</div>'+
  '<div class="body"></div><div class="meta st"></div></div>';
 var img=el.querySelector('img'), body=el.querySelector('.body'), st=el.querySelector('.st');
 function pick(){
  var n=pool[Math.floor(Math.random()*pool.length)];
  // brief burst of static as the channel changes
  el.querySelector('.static').style.opacity='.5';
  setTimeout(function(){el.querySelector('.static').style.opacity='';},220);
  if(n.t){img.src=n.t;img.style.display='';}else{img.removeAttribute('src');img.style.display='none';}
  body.textContent=(n.b||'').split('\\n')[0].slice(0,150)||'\\u2014 transmission received \\u2014';
  st.textContent='\\u2764 '+(n.l||0)+' \\u00b7 \\u21a9 '+(n.r||0)+' \\u00b7 '+(n.d||'');
 }
 img.addEventListener('error',function(){img.style.display='none';});
 pick();
 el.addEventListener('click',function(e){e.preventDefault();pick();});
 setInterval(pick,9000);
})();
"""


def tile(cls, lab, ttl, sm="", href="#", pill="", img=""):
    im = f'<img src="{esc(img)}" alt="" loading="lazy" onerror="this.remove()"><div class="scrim"></div>' if img else ""
    p = f'<span class="pill">{esc(pill)}</span>' if pill else ""
    s = f'<div class="sm">{esc(sm)}</div>' if sm else ""
    return (f'<a class="tile {cls}" href="{esc(href)}">{im}{p}'
            f'<div class="in"><div class="lab">{esc(lab)}</div>'
            f'<div class="ttl">{esc(ttl)}</div>{s}</div></a>')


def dial(themes, current):
    rows = []
    for t in sorted(themes.values(), key=lambda x: x["ch"]):
        if t["file"] == current:
            continue
        rows.append(f'<a href="{t["file"]}"><span class="em">{t["emoji"]}</span> '
                    f'{esc(t["label"])} <span class="ch">CH {t["ch"]}</span></a>')
    return ("<details class=\"chdial\"><summary title=\"Change the channel\">"
            "<span class=\"dial-ico\">\U0001F4FA</span>"
            "<span class=\"dial-label\"><small>Change Channel</small>Pick a Frequency</span></summary>"
            "<div class=\"chdial-panel\"><div class=\"chdial-title\">\U0001F4E1 Channel Dial</div>"
            + "".join(rows) + "</div></details>")


DIAL_CSS = """
.chdial{position:fixed;right:14px;bottom:70px;z-index:9600;font-family:'IBM Plex Mono',monospace}
.chdial summary{list-style:none;cursor:pointer;display:inline-flex;align-items:center;gap:9px;
padding:10px 15px;border-radius:99px;background:var(--surface);
border:1px solid color-mix(in srgb,var(--gold) 55%,transparent);color:var(--gold);font-size:11px}
.chdial summary::-webkit-details-marker{display:none}
.chdial .dial-label small{display:block;font-size:8px;letter-spacing:.2em;color:#9d94bd}
.chdial-panel{position:absolute;right:0;bottom:52px;width:250px;max-height:60vh;overflow:auto;
background:var(--surface);border:1px solid color-mix(in srgb,var(--purple) 45%,transparent);
border-radius:12px;padding:10px}
.chdial-title{font-family:Silkscreen,monospace;font-size:10px;letter-spacing:.18em;color:var(--gold);padding:6px 8px}
.chdial-panel a{display:flex;align-items:center;gap:9px;padding:8px;border-radius:8px;font-size:13px;color:var(--ink)}
.chdial-panel a:hover{background:color-mix(in srgb,var(--pink) 16%,transparent)}
.chdial-panel .ch{margin-left:auto;font-family:Silkscreen,monospace;font-size:9px;color:#7a6f9e}
"""


def hero_tile(theme, name, img):
    """Hero carries the real Magick Mica TV logo, then the frequency name."""
    im = (f'<img src="{esc(img)}" alt="" loading="eager" onerror="this.remove()">'
          f'<div class="scrim"></div>') if img else ""
    return (f'<a class="tile hero" href="articles.html">{im}'
            f'<div class="in">'
            f'<div class="live"><b></b>Now broadcasting \u00b7 CH {theme["ch"]}</div>'
            f'<img class="hero-logo" src="magick-mica-tv-logo.png" '
            f'alt="Magick Mica TV" decoding="async" fetchpriority="high">'
            f'<div class="ttl">{esc(name)}</div>'
            f'<div class="sm">5,615 transmissions and counting. Daily art notes, '
            f'cosmic curiosities, and a small universe of games.</div></div></a>')


def scard(href, lab, ttl, sm=""):
    return (f'<a class="scard" href="{esc(href)}"><div class="lab">{esc(lab)}</div>'
            f'<div class="ttl">{esc(ttl)}</div><div class="sm">{esc(sm)}</div></a>')


def tmap(nav):
    cols = []
    for group, items in nav.items():
        links = "".join(f'<a href="{esc(h)}">{esc(l)}</a>' for h, l in items)
        # long groups get a double-width column with two text columns, so one
        # list of 17 doesn't drop to its own full-width row
        wide = " wide" if len(items) > 12 else ""
        cols.append(f'<div class="tmap-col{wide}"><h3>{esc(group)}</h3>'
                    f'<div class="links">{links}</div></div>')
    return ('<section class="tmap"><h2 class="holo">\u2726 THE TRANSMISSION MAP</h2>'
            f'<div class="tmap-cols">{"".join(cols)}</div></section>')


def render(theme, themes, articles, nav):
    c = dict(theme["colors"])
    c.setdefault("ink", "#efe6ff")
    root = ":root{" + "".join(f"--{k}:{v};" for k, v in c.items()) + "}"
    deco = chrome_for(theme)
    css = root + CSS + DIAL_CSS + CTA_CSS + deco['css']
    name = theme["name"]
    fname = theme["file"]
    is_home = fname == "index.html"
    canon = SITE if is_home else SITE + fname
    title = f"Magick Mica TV \u2014 {name} {theme['emoji']}".strip()
    desc = ("Daily cosmic art notes, AI artwork, games and interactive oddities "
            "from Magick Mica. Curiosities, dreams and delightful nonsense.")

    latest = articles[0] if articles else None
    second = articles[1] if len(articles) > 1 else None

    tiles = [
        hero_tile(theme, name, (latest or {}).get("cover_url", "")),
        f'<a class="tile tv" href="random-note.html"><span class="pill">CH 01</span>'
        f'<div class="in" id="mtv"><div class="lab">RANDOM NOTE TV</div>'
        f'<div class="ttl">Tune in \u2192</div></div></a>',
        tile("w2 h2", "CH 02 \u00b7 Y3K MAGAZINE", "This Week",
             "Weekly + monthly issues", "minimags.html"),
        tile("w2", "CH 03", "The Arcade", "Six games from the archive", "arcade.html"),
        tile("w2", "CH 04", "The Vaults", "Crystals, amulets, copper", "herkimer-vault.html"),
        tile("w2", "CH 05 \u00b7 NEWSSTAND", "Nine issues", "On the rack now", "newsstand.html"),
        tile("w2", "CH 06", "Blog & Archive",
             (second or {}).get("title", "Every transmission by date"), "blog.html"),
    ]

    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(SITE if not is_home else SITE)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Magick Mica">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canon)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=IBM+Plex+Mono:wght@400;500&family=Silkscreen&display=swap" rel="stylesheet">
<style>{css}</style></head>
<body><div id="stars"></div>
{deco['html']}
<div class="wrap">
<header class="top">
  <a class="brand holo" href="index.html">\u2726 MAGICKMICA</a>
  <span class="chnow">CH {theme['ch']} \u00b7 {esc(theme['label'])}</span>
</header>

<div class="mos">{''.join(tiles)}</div>

<div class="sect"><h2 class="holo">Y3K MAGAZINE</h2><div class="rule"></div>
<span class="meta">WEEKLY ISSUES</span></div>
<div class="mag-grid"></div>

<div class="sect"><h2 class="holo">PLAY &amp; LISTEN</h2><div class="rule"></div>
<span class="meta">CH 03</span></div>
<div class="strip3">
{scard("arcade.html","CH 03 \u00b7 ARCADE","The Arcade","Jigsaw, memory, slots, object hunt")}
{scard("quest.html","CH 03b","Dream Quest","Ten realms, forty artifacts")}
{scard("songmaker.html","CH 03c","Song Maker","Build a tune from the signal")}
</div>
<div class="cta-row" style="margin-top:16px">{CTAS["oracle"]}{CTAS["mbox"]}</div>

<div class="sect"><h2 class="holo">THE SIGNAL SHOP</h2><div class="rule"></div>
<span class="meta">CRYSTALS &amp; COPPER</span></div>
<div class="strip3">
{scard("crystals.html","LIVE","Every Crystal","The whole shelf, priced and sorted")}
{scard("herkimer-vault.html","VAULT","Herkimer and Friends","Seven crystal vaults, curated")}
{scard("https://www.themysticalspiralstore.com/","STORE \u2197","Mystical Spiral","The full shop")}
</div>

<div class="sect"><h2 class="holo">SUBSTACK ARCHIVE</h2><div class="rule"></div>
<span class="meta">{len(articles)} ARTICLES</span></div>
<div class="strip3">
{scard("https://magickmica.substack.com","TV \u2197","MagickMica TV","The main broadcast")}
{scard("https://magickmicaart.substack.com","ART \u2197","MagickMica Art","The art channel")}
{scard("articles.html","ON SITE","Every Article","Searchable, with covers")}
</div>

<div class="sect"><h2 class="holo">SUPPORT THE SIGNAL</h2><div class="rule"></div>
<span class="meta">KEEP IT BROADCASTING</span></div>
<a class="star" href="https://ko-fi.com/magickmica/tip" target="_blank" rel="noopener">
<div class="lab" style="font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.2em;color:#8e85ad">ONE-TIME TIP</div>
<div class="big">\u2726 Send Me a Star \u2726</div>
<div class="sm">ko-fi.com/magickmica</div></a>

<div class="sect"><h2 class="holo">EXTENDED UNIVERSE</h2><div class="rule"></div>
<span class="meta">SIDE TRANSMISSIONS</span></div>
<div class="cta-row">{CTAS["wand"]}{CTAS["hearth"]}</div>
<div class="cta-row" style="margin-top:16px">{CTAS["ship"]}{CTAS["ecard"]}</div>
<div class="cta-row" style="margin-top:16px">{CTAS["cone"]}{CTAS["moon"]}</div>
<div class="cta-row" style="margin-top:16px">{CTAS["song"]}{CTAS["two"]}</div>

{tmap(nav)}

<footer>\u2726 <a href="https://magickmica.substack.com" target="_blank" rel="noopener">Magick Mica TV</a>
\u00b7 where magick meets the pixel \u2726<br>
<a href="notes.html">Notes</a> \u00b7 <a href="articles.html">Magazine</a> \u00b7
<a href="blog.html">Blog</a> \u00b7 <a href="minimags.html">Y3K</a> \u00b7
<a href="arcade.html">Arcade</a> \u00b7 <a href="archive.html">Archive</a>
</footer>
</div>
{dial(themes, fname)}
<script src="pools.js"></script>
<script src="mm-grid.js" defer></script>
<script>{MTV_JS}</script>
<script>{CTA_JS}</script>
<script>{deco.get('js','')}</script>
<script src="mm-nav.js" defer></script>
</body></html>"""


if __name__ == "__main__":
    import sys
    repo = sys.argv[1] if len(sys.argv) > 1 else "livecheck/magickmica.github.io-main"
    data_dir = sys.argv[2] if len(sys.argv) > 2 else "_data"
    out_dir = sys.argv[3] if len(sys.argv) > 3 else "build"

    themes = json.load(open(os.path.join(data_dir, "themes.json"), encoding="utf-8"))
    articles = json.load(open(os.path.join(data_dir, "magazine_articles.json"), encoding="utf-8"))
    nav = json.load(open(os.path.join(data_dir, "sitemap_nav.json"), encoding="utf-8"))
    os.makedirs(out_dir, exist_ok=True)

    for fname, theme in themes.items():
        page = render(theme, themes, articles, nav)
        open(os.path.join(out_dir, fname), "w", encoding="utf-8").write(page)
    print(f"generated {len(themes)} index pages from one template")
