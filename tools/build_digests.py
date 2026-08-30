#!/usr/bin/env python3
"""
MAGICKMICA - build_digests.py
Regenerates every week-YYYY-MM-DD.html and month-YYYY-MM.html digest
from the master notes archive, plus the minimags.html hub.

Design is taken verbatim from the existing digests: same six chapters,
same class names, same CSS. Only the content is rebuilt.

Weeks are ISO (Monday-start).
"""
import json, os, re, html, datetime, calendar, glob
from collections import Counter

NOTE_URL = "https://substack.com/@magickmica/note/c-{}"
SITE = "https://magickmica.github.io/"

# Accent palettes, reverse-engineered from the existing digests and
# verified against every file that carries an --accent (41/41 weeks,
# 10/10 months). Months cycle by absolute month number; weeks cycle by
# their position in the sorted list of week files.
MONTH_PALETTE = ["#b06eff", "#ff9d6e", "#ff6e9d", "#ffd76e",
                 "#ff6ef7", "#6ef7ff", "#f7ff6e", "#6effa0"]
WEEK_PALETTE = ["#ff6ef7", "#6ef7ff", "#f7ff6e", "#6effa0",
                "#b06eff", "#ff9d6e", "#ff6e9d", "#ffd76e"]


def month_accent(year, month):
    return MONTH_PALETTE[(year * 12 + month) % 8]


def week_accent(index):
    return WEEK_PALETTE[index % 8]

ORD = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX"]


def esc(s):
    return html.escape(s or "", quote=True)


def clip(text, n):
    t = (text or "").strip()
    return t[:n]


def first_line(text, n=90):
    t = (text or "").strip().split("\n")[0].strip()
    return t[:n] if t else "(untitled transmission)"


# ---------------------------------------------------------------- pieces
def timeline_html(notes):
    """Day-grouped timeline. Handles hundreds of notes per month."""
    out = []
    for day, group in group_by_day(notes):
        label = datetime.date.fromisoformat(day).strftime("%b %-d, %Y")
        out.append(f'<div class="timeline-day-label">{label}</div>')
        for n in group:
            if n.get("t"):
                alt = esc(first_line(n.get("b"), 80)) or "Magick Mica note"
                thumb = (
                    f'<img class="timeline-thumb" src="{esc(n["t"])}" alt="{alt}" loading="lazy" '
                    f'''onerror="this.outerHTML='&lt;div class=&quot;timeline-thumb-placeholder&quot;&gt;\u2728&lt;/div&gt;'" />'''
                )
            else:
                thumb = '<div class="timeline-thumb-placeholder">\u2728</div>'
            out.append(
                f'<a class="timeline-item" href="{NOTE_URL.format(n["id"])}" '
                f'target="_blank" rel="noopener">{thumb}'
                f'<div class="timeline-content"><div class="timeline-text">'
                f'{esc(clip(n.get("b"), 110))}</div>'
                f'<div class="timeline-stats">\u2764 {n.get("l",0)} \u00b7 \u21a9 {n.get("r",0)}</div>'
                f"</div></a>"
            )
    return "".join(out)


def group_by_day(notes):
    days = {}
    for n in notes:
        days.setdefault(n["d"], []).append(n)
    for day in sorted(days):
        yield day, sorted(days[day], key=lambda x: x["id"])


def quote_cards(notes, limit=6):
    top = sorted(notes, key=lambda n: (-(n.get("l") or 0), n["id"]))[:limit]
    out = []
    for n in top:
        img = ""
        if n.get("t"):
            img = (
                f'<div class="quote-card-img"><img src="{esc(n["t"])}" '
                f'alt="{esc(first_line(n.get("b"), 80)) or "Magick Mica note"}" loading="lazy" '
                f"""onerror="this.closest('.quote-card').style.display='none'"/></div>"""
            )
        out.append(
            f'<a class="quote-card" href="{NOTE_URL.format(n["id"])}" target="_blank" '
            f'rel="noopener">{img}'
            f'<div class="quote-card-body">{esc(clip(n.get("b"), 100))}</div>'
            f'<div class="quote-card-footer"><span>\u2764 {n.get("l",0)}</span>'
            f"<span>VIEW \u2192</span></div></a>"
        )
    return "".join(out)


def stat_boxes(notes):
    likes = sum(n.get("l", 0) for n in notes)
    restacks = sum(n.get("r", 0) for n in notes)
    imgs = sum(1 for n in notes if n.get("t"))
    busiest = Counter(n["d"] for n in notes).most_common(1)
    busy_label = (
        datetime.date.fromisoformat(busiest[0][0]).strftime("%b %-d, %Y")
        if busiest else "\u2014"
    )
    boxes = [
        (f"{len(notes):,}", "Notes"),
        (f"{likes:,}", "Likes"),
        (f"{restacks:,}", "Restacks"),
        (f"{imgs:,}", "With Images"),
        (busy_label, "Busiest Day"),
    ]
    return "".join(
        f'<div class="stat-box"><div class="stat-num">{v}</div>'
        f'<div class="stat-label">{k}</div></div>'
        for v, k in boxes
    )


def related_articles(articles, start, end):
    hits = [a for a in articles if start <= a.get("date", "")[:10] <= end]
    if not hits:
        return ('<p style="color:rgba(255,255,255,0.3);'
                "font-family:'Share Tech Mono',monospace;\">No posts this period.</p>")
    out = []
    for a in hits[:6]:
        img = ""
        if a.get("cover_url"):
            img = (f'<div class="related-img"><img src="{esc(a["cover_url"])}" '
                   f'alt="{esc(a.get("title",""))}" loading="lazy"/></div>')
        out.append(
            f'<a class="related-card" href="{esc(a.get("url",""))}" target="_blank" '
            f'rel="noopener">{img}<div class="related-title">{esc(a.get("title",""))}</div></a>'
        )
    return "".join(out)


def recap_paragraphs(notes):
    likes = sum(n.get("l", 0) for n in notes)
    restacks = sum(n.get("r", 0) for n in notes)
    top = sorted(notes, key=lambda n: -(n.get("l") or 0))[:2]
    ps = [f"<p>This period, {len(notes):,} transmissions went out, gathering "
          f"{likes:,} hearts and {restacks:,} restacks.</p>"]
    for n in top:
        body = clip(n.get("b"), 160)
        if body:
            ps.append(
                '<p><a style="color:inherit;border-bottom:1px dotted;text-decoration:none;" '
                f'href="{NOTE_URL.format(n["id"])}" target="_blank">\u201c{esc(body)}\u201d</a></p>'
            )
    return "".join(ps)


def cover_image(notes):
    withimg = [n for n in notes if n.get("t")]
    if not withimg:
        return ""
    return sorted(withimg, key=lambda n: -(n.get("l") or 0))[0]["t"]


# ---------------------------------------------------------------- template
def load_template(repo):
    """Pull CSS + <head> shell from an existing digest so design is preserved."""
    src = os.path.join(repo, "month-2026-08.html")
    with open(src, encoding="utf-8") as f:
        h = f.read()
    css = re.search(r"<style>(.*?)</style>", h, re.DOTALL).group(1)
    css = re.sub(r":root\{[^}]*\}", "__ROOT__", css, count=1)
    head_links = "".join(re.findall(r'<link[^>]+>', h))
    return css, head_links


def render(css, head_links, *, filename, title, kind, issue_label, accent, cover_url,
           cover_title, cover_sub, notes, articles, start, end,
           prev_link, next_link, prev_label, next_label):
    root = (f":root{{--accent:{accent};--accent2:#6ef7ff;--dark:#07020f;"
            f"--panel:rgba(18,6,32,0.88);--ink:#efe6ff;}}")
    style = css.replace("__ROOT__", root)

    cover = ""
    if cover_url:
        cover = (f'<img class="cover-img" src="{esc(cover_url)}" '
                 f'alt="{esc(cover_title)} \u2014 Magick Mica" '
                 f"onerror=\"this.style.display='none'\" />")

    nav_prev = (f'<a class="adj-link" href="{prev_link}">\u2190 {esc(prev_label)}</a>'
                if prev_link else
                f'<span class="adj-link disabled">\u2190 {esc(prev_label)}</span>')
    nav_next = (f'<a class="adj-link" href="{next_link}">{esc(next_label)} \u2192</a>'
                if next_link else
                f'<span class="adj-link disabled">{esc(next_label)} \u2192</span>')

    chapters = [
        ("RECAP", "The Recap", f"The {kind} in Review", "",
         f'<div class="chapter-body">{recap_paragraphs(notes)}</div>'),
        ("HIGHLIGHTS", "Highlights", "Most-Loved Transmissions",
         "The notes everyone couldn&apos;t stop liking.",
         f'<div class="quote-grid">{quote_cards(notes)}</div>'),
        ("WORDS", "In Their Words", "What Was Said", "",
         f'<div class="quote-grid">{quote_cards([n for n in notes if not n.get("t")], 4)}</div>'),
        ("TIMELINE", "The Full Timeline", "Every Transmission, In Order", "",
         f'<div class="timeline">{timeline_html(notes)}</div>'),
        ("BY THE NUMBERS", "By the Numbers", f"{cover_title} in Stats", "",
         f'<div class="stats-grid">{stat_boxes(notes)}</div>'),
        ("RELATED READING", "Related Reading", "Articles From This Period", "",
         f'<div class="related-articles">{related_articles(articles, start, end)}</div>'),
    ]
    body = []
    for i, (marker, eyebrow, htitle, lede, content) in enumerate(chapters):
        tag = "h1" if i == 0 else "h2"
        lede_html = f'<p class="chapter-lede">{lede}</p>' if lede else ""
        body.append(
            f'<section class="chapter" id="ch{i+1}">'
            f'<div class="chapter-marker">CHAPTER {ORD[i]} &middot; {marker}</div>'
            f'<span class="chapter-eyebrow">{eyebrow}</span>\n'
            f'<{tag} class="chapter-title">{htitle}</{tag}>{lede_html}{content}</section>\n'
        )

    # ---- SEO head -------------------------------------------------
    top = sorted(notes, key=lambda n: -(n.get("l") or 0))[:3]
    teaser = " \u00b7 ".join(first_line(n.get("b"), 45) for n in top if n.get("b"))
    likes = sum(n.get("l", 0) for n in notes)
    desc = (f"{len(notes):,} notes from {cover_title} by Magick Mica \u2014 "
            f"{likes:,} likes. {teaser}")[:300]
    canon = SITE + filename
    og_img = cover_url or ""

    jsonld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": f"{cover_title} \u2014 Y3K Magazine",
        "description": desc,
        "url": canon,
        "isPartOf": {"@type": "WebSite", "name": "Magick Mica",
                     "url": SITE},
        "author": {"@type": "Person", "name": "Magick Mica",
                   "url": "https://substack.com/@magickmica"},
        "datePublished": start,
        "numberOfItems": len(notes),
    }
    if og_img:
        jsonld["image"] = og_img

    seo = (
        f'<meta name="description" content="{esc(desc)}">\n'
        f'<link rel="canonical" href="{esc(canon)}">\n'
        f'<meta property="og:type" content="article">\n'
        f'<meta property="og:site_name" content="Magick Mica">\n'
        f'<meta property="og:title" content="{esc(cover_title)} \u2726 Y3K Magazine">\n'
        f'<meta property="og:description" content="{esc(desc)}">\n'
        f'<meta property="og:url" content="{esc(canon)}">\n'
        + (f'<meta property="og:image" content="{esc(og_img)}">\n' if og_img else "")
        + f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{esc(cover_title)} \u2726 Y3K Magazine">\n'
        f'<meta name="twitter:description" content="{esc(desc)}">\n'
        + (f'<meta name="twitter:image" content="{esc(og_img)}">\n' if og_img else "")
        + f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n'
    )

    return (
        f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
        f'<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f"<title>&#x2726; {esc(cover_title)} &#x2726; Y3K Magazine</title>\n"
        f"{seo}"
        f"{head_links}<style>{style}</style></head>\n"
        f'<body><div id="stars"></div>\n'
        f'<nav class="mag-nav"><a class="mag-logo" href="minimags.html">Y3K</a>'
        f'<span class="mag-issue">{esc(issue_label)}</span>\n'
        f'<div class="mag-toc"><a href="#ch1">Recap</a><a href="#ch2">Highlights</a>'
        f'<a href="#ch3">Words</a><a href="#ch4">Timeline</a><a href="#ch5">Stats</a>'
        f'<a href="#ch6">Reading</a></div></nav>\n'
        f'<div class="cover-wrap">{cover}<div class="cover-overlay"></div>\n'
        f'<div class="cover-content"><div class="cover-eyebrow">&#x2726; Y3K MAGAZINE &#x2726;</div>'
        f'<div class="cover-title">{esc(cover_title)}</div>\n'
        f'<div class="cover-sub">{esc(cover_sub)}</div></div></div>\n'
        f'<div class="scroll-cue">&#x25BE; SCROLL TO CATCH UP &#x25BE;</div>\n'
        + "".join(body) +
        f'<div class="closing-wrap"><div class="closing-tagline">&#x2726; THAT&apos;S A WRAP &#x2726;</div>\n'
        f'<div class="closing-sub">{esc(cover_sub)}</div>\n'
        f'<div class="divider-row">&#x2726; &#x2727; &#x2726; &#x2735; &#x2726; &#x2727; &#x2726;</div></div>\n'
        f'<div class="adjacent-nav">{nav_prev}{nav_next}</div>\n'
        f'<footer>&#x2726; <a href="https://magickmica.substack.com" target="_blank">Magick Mica TV</a>'
        f' &#x2726; where magic meets the pixel &#x2726;<br>\n'
        f'<a href="minimags.html">&larr; Back to All Issues</a> &nbsp;|&nbsp; '
        f'<a href="blog.html">Blog Home</a></footer>\n</body></html>'
    )


# ---------------------------------------------------------------- main
def build_all(repo, data_dir, out_dir):
    with open(os.path.join(data_dir, "notes_with_media_compact.json"), encoding="utf-8") as f:
        notes = json.load(f)
    apath = os.path.join(data_dir, "magazine_articles.json")
    articles = []
    if os.path.exists(apath):
        with open(apath, encoding="utf-8") as f:
            articles = json.load(f)

    css, head_links = load_template(repo)
    os.makedirs(out_dir, exist_ok=True)
    written = []

    # ---- months -------------------------------------------------
    by_month = {}
    for n in notes:
        by_month.setdefault(n["d"][:7], []).append(n)
    months = sorted(by_month)

    for i, m in enumerate(months):
        y, mo = int(m[:4]), int(m[5:7])
        group = by_month[m]
        last = calendar.monthrange(y, mo)[1]
        name = datetime.date(y, mo, 1).strftime("%B %Y")
        prev_l = f"month-{months[i-1]}.html" if i else None
        next_l = f"month-{months[i+1]}.html" if i + 1 < len(months) else None
        pl = (datetime.date(int(months[i-1][:4]), int(months[i-1][5:7]), 1)
              .strftime("%B") if i else "Prev")
        nl = (datetime.date(int(months[i+1][:4]), int(months[i+1][5:7]), 1)
              .strftime("%B") if i + 1 < len(months) else "Next Month")
        page = render(
            css, head_links,
            filename=f"month-{m}.html",
            title=name, kind="Month", issue_label=f"MONTHLY \u00b7 {name}",
            accent=month_accent(y, mo), cover_url=cover_image(group),
            cover_title=name,
            cover_sub=f"{len(group):,} notes \u00b7 a month of cosmic transmissions",
            notes=group, articles=articles,
            start=f"{m}-01", end=f"{m}-{last:02d}",
            prev_link=prev_l, next_link=next_l, prev_label=pl, next_label=nl,
        )
        p = os.path.join(out_dir, f"month-{m}.html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(page)
        written.append(p)

    # ---- weeks (ISO, Monday-start) ------------------------------
    by_week = {}
    for n in notes:
        d = datetime.date.fromisoformat(n["d"])
        wk = (d - datetime.timedelta(days=d.weekday())).isoformat()
        by_week.setdefault(wk, []).append(n)
    weeks = sorted(by_week)

    for i, w in enumerate(weeks):
        group = by_week[w]
        start = datetime.date.fromisoformat(w)
        end = start + datetime.timedelta(days=6)
        label = f"{start.strftime('%b %-d')} \u2013 {end.strftime('%b %-d, %Y')}"
        prev_l = f"week-{weeks[i-1]}.html" if i else None
        next_l = f"week-{weeks[i+1]}.html" if i + 1 < len(weeks) else None
        page = render(
            css, head_links,
            filename=f"week-{w}.html",
            title=label, kind="Week", issue_label=f"WEEKLY \u00b7 {label}",
            accent=week_accent(i), cover_url=cover_image(group),
            cover_title=label,
            cover_sub=f"{len(group):,} notes \u00b7 a week of cosmic transmissions",
            notes=group, articles=articles,
            start=w, end=end.isoformat(),
            prev_link=prev_l, next_link=next_l,
            prev_label="Prev Week", next_label="Next Week",
        )
        p = os.path.join(out_dir, f"week-{w}.html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(page)
        written.append(p)

    return written, months, weeks


if __name__ == "__main__":
    import sys
    repo = sys.argv[1] if len(sys.argv) > 1 else "magickmica.github.io-main"
    data_dir = sys.argv[2] if len(sys.argv) > 2 else "_data"
    out_dir = sys.argv[3] if len(sys.argv) > 3 else "build"
    written, months, weeks = build_all(repo, data_dir, out_dir)
    print(f"wrote {len(written)} digests ({len(months)} months, {len(weeks)} weeks)")
    print("months:", months[0], "->", months[-1])
    print("weeks :", weeks[0], "->", weeks[-1])
