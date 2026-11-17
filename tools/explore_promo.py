#!/usr/bin/env python3
"""
MAGICKMICA - explore_promo.py  ·  the "NEW!" promo for the Explore section

Two pieces, shared by tools/build_index.py (the homepage template) and by
running this file directly (which patches the live homepages in place):

  1. A grocery-store "NEW!" starburst banner linking to explore/, on
     index.html only, just above the Y3K MAGAZINE section.
  2. A small "NEW!" tag next to "Explore the Notes" in THE TRANSMISSION MAP,
     on index.html and every index-*.html variant.
  3. An "On this day" strip on index.html, right under the banner: the
     most-loved note from today's date in an earlier year, how many went out
     on this date, and a button into the Y3K Almanac. Its data is
     almanac/today.js, written by almanac/build_almanac.py; the strip loads it
     only when it scrolls into view. Turn it off with SHOW_ON_THIS_DAY = False.

    python3 tools/explore_promo.py            # add both to the live pages (safe to re-run)
    python3 tools/explore_promo.py --remove   # take them off again

Everything sits between <!-- mm-explore-new --> markers, so re-running never
doubles it, and --remove takes it all out cleanly. The update workflow edits
other parts of these pages in place and leaves these alone.

To retire the promo later: run with --remove, and set SHOW_PROMO = False below
so tools/build_index.py stops adding it.
"""
import glob
import math
import os
import re
import sys

SHOW_PROMO = True
SHOW_ON_THIS_DAY = True
NEW_LINKS = {"explore/"}            # Transmission Map links that get a NEW! tag

M_CSS = ("<!-- mm-explore-new:css -->", "<!-- /mm-explore-new:css -->")
M_CTA = ("<!-- mm-explore-new:cta -->", "<!-- /mm-explore-new:cta -->")
M_OTD = ("<!-- mm-onthisday -->", "<!-- /mm-onthisday -->")


def _burst(points=16, inner=0.80):
    """CSS clip-path polygon for a price-sticker starburst."""
    pts = []
    for i in range(points * 2):
        r = 50 if i % 2 == 0 else 50 * inner
        a = math.pi * i / points - math.pi / 2
        pts.append(f"{50 + r * math.cos(a):.1f}% {50 + r * math.sin(a):.1f}%")
    return "polygon(" + ",".join(pts) + ")"


BURST = _burst()

CSS = """
.xnew{position:relative;display:flex;align-items:center;gap:22px;margin:30px 0 8px;padding:20px 26px 20px 120px;
  border-radius:18px;text-decoration:none;color:#f4eefc;overflow:visible;
  background:linear-gradient(115deg,rgba(47,47,112,.92),rgba(19,28,63,.94) 55%,rgba(81,70,162,.9));
  border:1px solid rgba(213,194,220,.35);box-shadow:0 14px 40px rgba(0,0,0,.45)}
.xnew:hover{border-color:#ffd400;box-shadow:0 14px 44px rgba(0,0,0,.5),0 0 0 2px rgba(255,212,0,.25)}
.xnew:focus-visible{outline:3px solid #ffd400;outline-offset:4px}
.xnew-burst{position:absolute;left:-14px;top:50%;width:122px;height:122px;margin-top:-61px;transform:rotate(-12deg);
  filter:drop-shadow(0 6px 10px rgba(0,0,0,.5));transition:transform .25s cubic-bezier(.2,.8,.3,1.4)}
.xnew-burst::before,.xnew-burst::after{content:"";position:absolute;inset:0;clip-path:BURST}
.xnew-burst::before{background:#e3001b}
.xnew-burst::after{inset:7px;background:radial-gradient(circle at 35% 30%,#fff7a8,#ffd400 55%,#ffb800)}
.xnew-burst span{position:absolute;inset:0;z-index:1;display:grid;place-items:center;
  font:900 27px/1 "Arial Black","Helvetica Neue",Arial,sans-serif;letter-spacing:-.02em;color:#e3001b;
  text-shadow:1px 1px 0 #fff}
.xnew:hover .xnew-burst{transform:rotate(-4deg) scale(1.07)}
.xnew-body{display:flex;flex-direction:column;gap:4px;min-width:0;flex:1}
.xnew-k{font:700 11px/1.2 "IBM Plex Mono",monospace;letter-spacing:.18em;color:#ffd400;text-transform:uppercase}
.xnew-t{font:700 clamp(20px,3.4vw,30px)/1.05 Orbitron,"Arial Black",sans-serif;letter-spacing:.04em;color:#fff}
.xnew-s{font:400 14px/1.45 "IBM Plex Mono",monospace;color:#d5c2dc}
.xnew-go{flex:none;font:700 13px/1 "IBM Plex Mono",monospace;letter-spacing:.08em;text-transform:uppercase;
  color:#120418;background:#ffd400;padding:12px 18px;border-radius:999px;white-space:nowrap}
.xnew:hover .xnew-go{background:#fff06a}
@media(max-width:640px){
  .xnew{flex-direction:column;align-items:flex-start;gap:12px;padding:72px 18px 18px;margin-top:40px}
  .xnew-burst{left:auto;right:-8px;top:-34px;margin-top:0;width:100px;height:100px}
  .xnew-burst span{font-size:22px}
}
.tmap-new{display:inline-block;margin-left:6px;padding:1px 6px 2px;border-radius:3px;transform:rotate(-4deg);
  font:900 9px/1.4 "Arial Black",Arial,sans-serif;letter-spacing:.04em;color:#e3001b;background:#ffd400;
  box-shadow:0 0 0 1px #e3001b;vertical-align:1px}
@media(prefers-reduced-motion:reduce){.xnew-burst{transition:none}.xnew:hover .xnew-burst{transform:rotate(-12deg)}}
""".replace("BURST", BURST).strip()

CTA = (
    '<a class="xnew" href="explore/" aria-label="New: Explore the Notes. Eight ways to wander the archive.">'
    '<span class="xnew-burst" aria-hidden="true"><span>NEW!</span></span>'
    '<span class="xnew-body"><span class="xnew-k">Just opened · 8 rooms</span>'
    '<span class="xnew-t">EXPLORE THE NOTES</span>'
    '<span class="xnew-s">A book, a gallery, a tape library, a sky map, theme rooms, a hall of fame, '
    'the Y3K Almanac and Transmission Reader 98, built from every transmission.</span></span>'
    '<span class="xnew-go">Step inside →</span></a>'
)

OTD_CSS = """
.otd{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:18px 22px;margin:14px 0 8px;padding:18px 22px;
  border-radius:18px;color:#f4eefc;background:linear-gradient(115deg,rgba(19,28,63,.92),rgba(37,22,64,.92));
  border:1px solid rgba(213,194,220,.28)}
.otd-moon{font:400 34px/1 Georgia,serif;color:#ffd400;text-shadow:0 0 18px rgba(255,212,0,.45)}
.otd-k{font:700 11px/1.2 "IBM Plex Mono",monospace;letter-spacing:.18em;color:#9fe8ff;text-transform:uppercase;margin:0 0 6px}
.otd-note{display:flex;gap:12px;align-items:center;color:#f4eefc;text-decoration:none;min-width:0}
.otd-note:hover .otd-text,.otd-note:focus-visible .otd-text{text-decoration:underline;text-underline-offset:3px}
.otd-note:focus-visible,.otd-go:focus-visible{outline:3px solid #ffd400;outline-offset:3px;border-radius:6px}
.otd-note img{flex:none;width:56px;height:56px;object-fit:cover;border-radius:8px;border:1px solid rgba(213,194,220,.3)}
.otd-when{display:block;font:700 12px/1.3 "IBM Plex Mono",monospace;color:#ffd400;letter-spacing:.06em;text-transform:uppercase}
.otd-text{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;
  font:400 16px/1.4 Georgia,"Times New Roman",serif;font-style:italic;color:#f4eefc;overflow-wrap:anywhere}
.otd-count{margin:6px 0 0;font:400 12px/1.4 "IBM Plex Mono",monospace;color:#d5c2dc}
.otd-go{flex:none;font:700 13px/1 "IBM Plex Mono",monospace;letter-spacing:.08em;text-transform:uppercase;text-decoration:none;
  color:#120418;background:#9fe8ff;padding:12px 18px;border-radius:999px;white-space:nowrap}
.otd-go:hover{background:#d4f6ff}
@media(max-width:640px){.otd{grid-template-columns:1fr;padding:16px 18px}.otd-moon{display:none}.otd-go{justify-self:start}}
""".strip()

OTD_HTML = (
    '<section class="otd" id="otd" aria-labelledby="otd-k">'
    '<span class="otd-moon" aria-hidden="true">☽</span>'
    '<div class="otd-body"><p class="otd-k" id="otd-k">On this day</p>'
    '<div id="otd-fill"><p class="otd-count">Every date of the year has a page in the Y3K Almanac.</p></div></div>'
    '<a class="otd-go" id="otd-go" href="almanac/">Open the Almanac →</a></section>'
)

# fills the strip from almanac/today.js once it scrolls near the screen
OTD_JS = r"""
(function(){var box=document.getElementById('otd');if(!box)return;
var now=new Date(),y=now.getFullYear(),md=('0'+(now.getMonth()+1)).slice(-2)+'-'+('0'+now.getDate()).slice(-2);
var day=now.toLocaleDateString('en-US',{month:'long',day:'numeric'});
document.getElementById('otd-k').textContent='On this day · '+day;
var go=document.getElementById('otd-go');go.href='almanac/#d'+md;go.textContent='Open '+day+' in the Almanac →';
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function fill(){var D=window.MM_ONTHISDAY,d=D&&D.days[md],f=document.getElementById('otd-fill');if(!d||!f)return;
var past=d.top.filter(function(r){return +r[0].slice(0,4)<y}),r=(past.length?past:d.top)[past.length?past.length-1:0];
var ry=+r[0].slice(0,4),when=ry===y?'Earlier today':ry===y-1?'A year ago today':'On this day in '+ry;
var img=r[3]?(/^https?:/.test(r[3])?r[3]:D.imgPrefix+r[3]):'';
var tot=0,parts=[];Object.keys(d.n).sort().forEach(function(k){tot+=d.n[k];parts.push(k+': '+d.n[k])});
f.innerHTML='<a class="otd-note" href="https://substack.com/@magickmica/note/c-'+r[1]+'" target="_blank" rel="noopener">'+
(img?'<img src="'+esc(img)+'" alt="" loading="lazy" decoding="async" onerror="this.remove()">':'')+
'<span><span class="otd-when">'+when+(r[4]?' · video':'')+'</span><span class="otd-text">'+(r[2]?'“'+esc(r[2])+'”':'(a picture note)')+'</span></span></a>'+
'<p class="otd-count">'+tot+' transmission'+(tot===1?'':'s')+' on '+day+(parts.length>1?' · '+parts.join(' · '):'')+'</p>'}
function load(){if(window.MM_ONTHISDAY)return fill();var s=document.createElement('script');s.src='almanac/today.js';s.onload=fill;document.head.appendChild(s)}
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(e){if(e[0].isIntersecting){io.disconnect();load()}},{rootMargin:'400px'});io.observe(box)}else load()})();
""".strip()

TAG = '<span class="tmap-new">NEW!</span>'
Y3K_ANCHOR = '<div class="sect"><h2 class="holo">Y3K MAGAZINE</h2>'


def css_block():
    return f"{M_CSS[0]}<style>{CSS}</style>{M_CSS[1]}" if SHOW_PROMO else ""


def cta_block():
    return f"{M_CTA[0]}{CTA}{M_CTA[1]}\n" if SHOW_PROMO else ""


def otd_block():
    if not SHOW_ON_THIS_DAY:
        return ""
    return (f"{M_OTD[0]}<style>{OTD_CSS}</style>{OTD_HTML}<script>{OTD_JS}</script>{M_OTD[1]}\n")


def tag_for(href):
    return TAG if SHOW_PROMO and href in NEW_LINKS else ""


def _strip(text):
    for a, b in (M_CSS, M_CTA, M_OTD):
        text = re.sub(re.escape(a) + r".*?" + re.escape(b) + r"\n?", "", text, flags=re.S)
    for href in NEW_LINKS:
        text = text.replace(f'<a href="{href}">Explore the Notes{TAG}</a>',
                            f'<a href="{href}">Explore the Notes</a>')
    return text


def patch(text, is_home, remove=False):
    text = _strip(text)
    if remove:
        return text
    if not SHOW_PROMO:
        return _add_otd(text, is_home)
    if "</head>" in text:
        text = text.replace("</head>", css_block() + "\n</head>", 1)
    if is_home and Y3K_ANCHOR in text:
        text = text.replace(Y3K_ANCHOR, cta_block() + Y3K_ANCHOR, 1)
    # the map link: add it after Y3K Magazine if a page predates the menu entry
    if '<a href="explore/">' not in text and '<a href="minimags.html">Y3K Magazine</a>' in text:
        text = text.replace('<a href="minimags.html">Y3K Magazine</a>',
                            '<a href="minimags.html">Y3K Magazine</a><a href="explore/">Explore the Notes</a>', 1)
    text = text.replace('<a href="explore/">Explore the Notes</a>',
                        f'<a href="explore/">Explore the Notes{TAG}</a>')
    return _add_otd(text, is_home)


def _add_otd(text, is_home):
    # the strip goes right under the NEW! banner, just above Y3K MAGAZINE
    if is_home and Y3K_ANCHOR in text:
        text = text.replace(Y3K_ANCHOR, otd_block() + Y3K_ANCHOR, 1)
    return text


def main(argv):
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    remove = "--remove" in argv
    pages = [os.path.join(repo, "index.html")] + sorted(glob.glob(os.path.join(repo, "index-*.html")))
    changed = 0
    for p in pages:
        if not os.path.exists(p):
            continue
        old = open(p, encoding="utf-8").read()
        if 'class="tmap"' not in old:
            continue
        new = patch(old, os.path.basename(p) == "index.html", remove)
        if new != old:
            open(p, "w", encoding="utf-8").write(new)
            changed += 1
    print(f"explore promo {'removed from' if remove else 'on'} {changed} page(s) changed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
