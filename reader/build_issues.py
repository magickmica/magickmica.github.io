"""
TRANSMISSION READER 98 — issue pages
------------------------------------
Writes one Reader-styled page per week and per month into reader/issues/:
    reader/issues/week-YYYY-MM-DD.html
    reader/issues/month-YYYY-MM.html
Each page carries the same six chapters as the classic Y3K issues (Recap,
Most Loved, In Their Words, Timeline, By the Numbers, Related Reading).
Called by build_reader.py; nothing outside reader/issues/ is written.
"""
import datetime as dt
import html
import os
import re

SITE = "https://magickmica.github.io/"
URL_RE = re.compile(r"https?://[^\s<>\"']+")
ORD = ["One", "Two", "Three", "Four", "Five", "Six"]
FONTS = "https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400;600&display=swap"

ICON_APP = ('<svg viewBox="0 0 12 12" aria-hidden="true"><rect x="4" y="1" width="4" height="1" fill="#fff"/>'
            '<rect x="2" y="2" width="8" height="1" fill="#fff"/><rect x="1" y="3" width="10" height="5" fill="#fff"/>'
            '<rect x="2" y="8" width="8" height="1" fill="#fff"/><rect x="3" y="3" width="2" height="2" fill="#6ef7ff"/>'
            '<rect x="5" y="5" width="3" height="2" fill="#ff6ef7"/><rect x="7" y="3" width="2" height="1" fill="#ffd76e"/>'
            '<rect x="3" y="9" width="6" height="1" fill="#c9a6ff"/><rect x="2" y="10" width="8" height="1" fill="#8a6bd6"/></svg>')


def icon(color):
    return (f'<svg viewBox="0 0 8 8" aria-hidden="true"><rect x="1" y="0" width="6" height="8" fill="{color}"/>'
            f'<rect x="2" y="2" width="4" height="1" fill="rgba(255,255,255,.7)"/>'
            f'<rect x="2" y="4" width="4" height="1" fill="rgba(255,255,255,.7)"/></svg>')


CHAPTERS = [  # id, title, toc icon colour
    ("recap", "The Recap", "#2b1f72"),
    ("loved", "Most-Loved Transmissions", "#c24c9e"),
    ("words", "In Their Words", "#6a3bb0"),
    ("timeline", "Every Transmission, In Order", "#3f8fc0"),
    ("numbers", "By the Numbers", "#b8962a"),
    ("reading", "Related Reading", "#2b8f86"),
]


def e(s):
    return html.escape(s or "", quote=True)


def d(iso):
    return dt.date.fromisoformat(iso)


def short(iso):
    x = d(iso)
    return f"{x.strftime('%b')} {x.day}, {x.year}"


def long(iso):
    x = d(iso)
    return f"{x.strftime('%A')}, {x.strftime('%B')} {x.day}, {x.year}"


def week_label(w):
    a, b = d(w), d(w) + dt.timedelta(days=6)
    if a.month == b.month:
        return f"{a.strftime('%b')} {a.day} – {b.day}, {b.year}"
    if a.year == b.year:
        return f"{a.strftime('%b')} {a.day} – {b.strftime('%b')} {b.day}, {b.year}"
    return f"{a.strftime('%b')} {a.day}, {a.year} – {b.strftime('%b')} {b.day}, {b.year}"


def month_label(m):
    x = d(m + "-01")
    return f"{x.strftime('%B')} {x.year}"


def subject(n):
    first = next((ln.strip() for ln in URL_RE.sub("", n["b"]).split("\n") if ln.strip()), "")
    if first:
        return first
    return "(picture)" if n["t"] else "(video)" if n["m"] else "(no words)"


def linkify(text):
    out, last = [], 0
    for m in URL_RE.finditer(text):
        out.append(e(text[last:m.start()]))
        url = m.group(0).rstrip(".,);")
        out.append(f'<a href="{e(url)}" target="_blank" rel="noopener">{e(url)}</a>')
        out.append(e(m.group(0)[len(url):]))
        last = m.end()
    out.append(e(text[last:]))
    return "".join(out)


def note_url(n):
    return f"https://substack.com/@magickmica/note/c-{n['id']}"


def plural(n, one, many=None):
    return f"{n:,} {one if n == 1 else (many or one + 's')}"


# ---------------------------------------------------------------- chapters

def ch_recap(notes, label, kind):
    likes = sum(n["l"] for n in notes)
    rs = sum(n["r"] for n in notes)
    top = sorted(notes, key=lambda n: (n["l"], n["r"]), reverse=True)
    cover = next((n for n in top if n["t"]), None)
    pulls = [n for n in top if n["b"].strip() and re.search(r"[A-Za-z]", n["b"])][:2]
    body = (f'<p class="lede">This {kind} {plural(len(notes), "transmission")} went out, '
            f'gathering {plural(likes, "heart")} and {plural(rs, "restack")}.</p>')
    body += "".join(f'<blockquote class="pull"><a href="#n{n["id"]}">{e(subject(n))}</a></blockquote>' for n in pulls)
    if cover:
        img = (f'<img class="cover" src="{e(cover["t"])}" alt="" loading="eager" '
               f'data-fallback="The cover picture shows on Substack.">')
        return f'<div class="recap has-cover">{img}<div>{body}</div></div>', cover
    return f'<div class="recap"><div>{body}</div></div>', None


def ch_loved(notes):
    top = sorted(notes, key=lambda n: (n["l"], n["r"]), reverse=True)[:6]
    cards = []
    for n in top:
        img = (f'<img src="{e(n["t"])}" alt="" loading="lazy" data-fallback="Picture shows on Substack.">'
               if n["t"] else "")
        cards.append(
            f'<article class="card">{img}<p>{e(subject(n))}</p>'
            f'<div class="foot"><span>♥ {n["l"]:,}</span><span>↻ {n["r"]:,}</span>'
            f'<span>{short(n["d"])}</span><a href="#n{n["id"]}">Read</a></div></article>')
    return f'<div class="cards">{"".join(cards)}</div>'


def ch_words(notes):
    pool = [n for n in notes if not n["t"] and len(n["b"].strip()) >= 20 and re.search(r"[A-Za-z]", n["b"])]
    pool = sorted(pool, key=lambda n: (n["l"], n["r"]), reverse=True)[:4]
    if not pool:
        return '<p class="none">Every transmission this time came with a picture.</p>'
    return '<ul class="words">' + "".join(
        f'<li>{e(subject(n))}<small>♥ {n["l"]:,} · {short(n["d"])} · '
        f'<a href="#n{n["id"]}">in the timeline</a></small></li>' for n in pool) + "</ul>"


def msg(n, themes):
    text = n["b"].strip()
    glyph = text and not re.search(r"[A-Za-z0-9]", text)
    parts = []
    if text:
        parts.append(f'<p class="text{" glyph" if glyph else ""}">{linkify(text)}</p>')
    if n["t"]:
        parts.append(f'<img class="pic" src="{e(n["t"])}" alt="Picture attached to this transmission" '
                     f'loading="lazy" data-fallback="This picture could not be received here. It shows on Substack.">')
    if n["m"]:
        parts.append('<div class="att">This transmission carries a video. Play it on Substack.</div>')
    tags = ", ".join(themes.get(t, t) for t in n["c"])
    parts.append(f'<div class="acts"><a class="btn primary" href="{note_url(n)}" target="_blank" rel="noopener">'
                 f'Open on Substack ↗</a><span>{long(n["d"])}</span>'
                 + (f'<span>Themes: {e(tags)}</span>' if tags else "") + "</div>")
    return (f'<details class="msg" id="n{n["id"]}"><summary><span class="s">{e(subject(n))}</span>'
            f'<span class="num">♥ {n["l"]:,}</span><span class="num rs">↻ {n["r"]:,}</span></summary>'
            f'<div class="body">{"".join(parts)}</div></details>')


def ch_timeline(days, themes):
    out = []
    for day, group in days:
        out.append(f'<h3 class="day" id="d{day}">{long(day)}<span>{plural(len(group), "transmission")}</span></h3>')
        out.extend(msg(n, themes) for n in group)
    return "".join(out)


def ch_numbers(notes, days, all_days):
    likes = sum(n["l"] for n in notes)
    rs = sum(n["r"] for n in notes)
    imgs = sum(1 for n in notes if n["t"])
    counts = {k: len(v) for k, v in days}
    busiest = max(days, key=lambda kv: len(kv[1]))[0]
    props = [("Transmissions", f"{len(notes):,}"), ("Hearts", f"{likes:,}"), ("Restacks", f"{rs:,}"),
             ("With pictures", f"{imgs:,}"), ("Busiest day", short(busiest)[:-6])]
    html_props = "".join(f'<div class="prop"><label>{k}</label><output>{v}</output></div>' for k, v in props)
    mx = max(counts.values())
    weekly = len(all_days) <= 7
    bars, labels = [], []
    for day in all_days:
        c = counts.get(day, 0)
        x = d(day)
        cls = "bar" + (" top" if day == busiest else "") + ("" if c else " zero")
        name = x.strftime("%a") if weekly else str(x.day)
        title = f"{long(day)}: {plural(c, 'transmission')}"
        inner = f'<b>{c}</b><i style="--h:{(c / mx * 100) if mx else 0:.1f}%"></i>'
        bars.append(f'<a class="{cls}" href="#d{day}" title="{title}" aria-label="{title}">{inner}</a>' if c
                    else f'<span class="{cls}" title="{title}">{inner}</span>')
        labels.append(f"<span>{name if weekly or x.day == 1 or x.day % 5 == 0 else ''}</span>")
    return (f'<div class="props">{html_props}</div>'
            f'<div class="bars" role="img" aria-label="Transmissions per day">{"".join(bars)}</div>'
            f'<div class="bar-labels" aria-hidden="true">{"".join(labels)}</div>'
            f'<p class="bars-cap">Transmissions per day. The busiest day is highlighted; choose a bar to jump to that day.</p>')


def ch_reading(arts, extra):
    items = []
    for a in arts:
        nl = "art" if "Art" in a.get("newsletter", "") else "tv"
        hearts = f'<small>♥ {a["likes"]:,}</small>' if a.get("likes") is not None else ""
        items.append(f'<li><span class="tag {nl}">{"ART" if nl == "art" else "TV"}</span>'
                     f'<a href="{e(a["url"])}" target="_blank" rel="noopener">{e(a["title"].strip())}</a>'
                     f'<small>{short(a["date"])}</small>{hearts}</li>')
    out = ('<ul class="reading">' + "".join(items) + "</ul>") if items else \
        '<p class="none">No articles were published in this stretch.</p>'
    return out + extra


# ---------------------------------------------------------------- page

def page(kind, key, label, notes, arts, themes, prev, nxt, built, extra_reading, up_link, classic):
    notes = sorted(notes, key=lambda n: (n["d"], n["id"]))
    by_day = {}
    for n in notes:
        by_day.setdefault(n["d"], []).append(n)
    days = sorted(by_day.items())
    if kind == "week":
        start = key
        span = [(d(key) + dt.timedelta(days=i)).isoformat() for i in range(7)]
    else:
        start = key + "-01"
        first = d(start)
        nxt_m = (first.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        span = [(first + dt.timedelta(days=i)).isoformat() for i in range((nxt_m - first).days)]
    end = span[-1]
    Kind = "Weekly" if kind == "week" else "Monthly"
    title = f"Y3K {Kind} · {label}"
    likes = sum(n["l"] for n in notes)
    rs = sum(n["r"] for n in notes)

    recap, cover = ch_recap(notes, label, "week" if kind == "week" else "month")
    toc_days = ""
    if kind == "week":
        toc_days = "<ul>" + "".join(
            f'<li><a href="#d{dd}">{d(dd).strftime("%a %b")} {d(dd).day}<span class="n">{len(g)}</span></a></li>'
            for dd, g in days) + "</ul>"
    else:
        weeks = {}
        for dd, g in days:
            wk = (d(dd) - dt.timedelta(days=d(dd).weekday())).isoformat()
            weeks.setdefault(wk, [dd, 0])
            weeks[wk][1] += len(g)
        toc_days = "<ul>" + "".join(
            f'<li><a href="#d{v[0]}">Week of {d(wk).strftime("%b")} {d(wk).day}<span class="n">{v[1]}</span></a></li>'
            for wk, v in sorted(weeks.items())) + "</ul>"

    bodies = {
        "recap": recap,
        "loved": ch_loved(notes),
        "words": ch_words(notes),
        "timeline": ch_timeline(days, themes),
        "numbers": ch_numbers(notes, days, span),
        "reading": ch_reading(arts, extra_reading),
    }
    counts = {"timeline": len(notes), "reading": len(arts)}
    toc_items = "".join(
        f'<li><a href="#{cid}">{icon(col)}<span>{name}</span>'
        + (f'<span class="n">{counts[cid]}</span>' if cid in counts else "") + "</a>"
        + (toc_days if cid == "timeline" else "") + "</li>"
        for cid, name, col in CHAPTERS)
    toc = f'<h2>In this issue</h2><ul>{toc_items}</ul>'
    sections = "".join(
        f'<section class="group" id="{cid}" aria-labelledby="h-{cid}"><h2 id="h-{cid}"><small>Chapter {ORD[i]}</small>{name}</h2>'
        f'{bodies[cid]}</section>'
        for i, (cid, name, _) in enumerate(CHAPTERS))

    def nav_btn(target, text, rel):
        if not target:
            return f'<span class="btn off" aria-disabled="true">{text}</span>'
        return f'<a class="btn" href="{target[0]}" rel="{rel}">{text}</a>'

    prev_btn = nav_btn(prev, "◂ Previous issue", "prev")
    next_btn = nav_btn(nxt, "Next issue ▸", "next")
    folder = "weekly" if kind == "week" else "monthly"
    desc_quote = next((subject(n) for n in sorted(notes, key=lambda n: n["l"], reverse=True)
                       if re.search(r"[A-Za-z]", n["b"])), "")
    desc = f"{plural(len(notes), 'transmission')} from {label}, received in Transmission Reader 98. {desc_quote}"[:300]
    fname = f"{kind}-{key}.html"
    og_img = f'<meta property="og:image" content="{e(cover["t"])}">' if cover else ""
    status_extra = f'<span><a href="{classic}">Classic edition</a></span>' if classic else ""

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)} · Transmission Reader 98</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}reader/issues/{fname}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Magick Mica">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}reader/issues/{fname}">
{og_img}
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="issue.css">
</head>
<body>
<div class="desk">
  <div class="win out">
    <div class="title">{ICON_APP}<h1>{e(title)}</h1><span class="app">Transmission Reader 98</span></div>
    <nav class="tools" aria-label="Issue">
      <a class="btn" href="../index.html#{folder}">◂ Back to Reader</a>
      {prev_btn}
      {next_btn}
      {up_link}
      <details class="toc-pick"><summary class="btn">In this issue ▾</summary><div class="toc-pop out">{toc}</div></details>
    </nav>
    <div class="panes">
      <nav class="toc in" aria-label="In this issue">{toc}</nav>
      <main class="doc in" id="doc">
        <header class="ph">
          <h2>{e(title)}</h2>
          <dl class="meta">
            <dt>From:</dt><dd>Y3K Magazine · Magick Mica TV</dd>
            <dt>Covers:</dt><dd>{long(start)} to {long(end)}</dd>
            <dt>Contains:</dt><dd>{plural(len(notes), "transmission")} · ♥ {likes:,} hearts · ↻ {rs:,} restacks</dd>
          </dl>
        </header>
        <div class="pb">
          {sections}
          <nav class="endnav" aria-label="More issues">{prev_btn}<a class="btn" href="../index.html#{folder}">All {folder} issues</a>{next_btn}</nav>
        </div>
      </main>
    </div>
    <div class="status"><span>{plural(len(notes), "transmission")} · ♥ {likes:,} · ↻ {rs:,}</span><span>Y3K {Kind}</span>{status_extra}<span>Built {built}</span></div>
  </div>
  <div class="below">
    <span>Transmission Reader 98 · Magick Mica TV</span>
    <nav aria-label="Magick Mica"><a href="{SITE}">Home</a><a href="../index.html">Reader 98</a><a href="{SITE}notes.html">All Notes</a><a href="{SITE}articles.html">Magazine</a></nav>
  </div>
</div>
<script src="issue.js"></script>
</body>
</html>
"""


def write_issues(notes, articles, out_dir, themes, note_prefix, issued):
    """notes: compact records from _data. Returns (weekly, monthly) summaries, newest first."""
    os.makedirs(out_dir, exist_ok=True)
    built = dt.date.today().isoformat()

    def full_img(t):
        return t or ""

    recs = [{"id": n["id"], "d": n["d"], "l": n.get("l", 0), "r": n.get("r", 0), "b": n.get("b") or "",
             "t": full_img(n.get("t")), "m": 1 if n.get("m") else 0, "c": n.get("c") or []} for n in notes]
    weeks, months = {}, {}
    for n in recs:
        wk = (d(n["d"]) - dt.timedelta(days=d(n["d"]).weekday())).isoformat()
        weeks.setdefault(wk, []).append(n)
        months.setdefault(n["d"][:7], []).append(n)

    def arts_between(a, b):
        return sorted([x for x in articles if a <= x["date"] <= b], key=lambda x: x["date"])

    written = set()
    summaries = {}
    for kind, bucket in (("week", weeks), ("month", months)):
        keys = sorted(bucket)
        out = []
        for i, k in enumerate(keys):
            if kind == "week":
                a, b = k, (d(k) + dt.timedelta(days=6)).isoformat()
                label = week_label(k)
                mk = [m for m in sorted({k[:7], b[:7]})]
                up = " ".join(f'<a class="btn" href="month-{m}.html">{d(m + "-01").strftime("%B")} issue</a>' for m in mk if m in months)
                extra = ""
            else:
                a = k + "-01"
                first = d(a)
                b = ((first.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)).isoformat()
                label = month_label(k)
                up = ""
                wks = [w for w in sorted(weeks) if w <= b and (d(w) + dt.timedelta(days=6)).isoformat() >= a]
                extra = ('<h3 class="day" style="margin-top:18px">Weekly issues in this month</h3><ul class="reading">' + "".join(
                    f'<li><a href="week-{w}.html">Y3K Weekly · {week_label(w)}</a><small>{plural(len(weeks[w]), "transmission")}</small></li>'
                    for w in wks) + "</ul>")
            prev = (f"{kind}-{keys[i - 1]}.html",) if i else None
            nxt = (f"{kind}-{keys[i + 1]}.html",) if i + 1 < len(keys) else None
            classic = f"{SITE}{kind}-{k}.html" if f"{kind}-{k}" in issued else ""
            html_text = page(kind, k, label, bucket[k], arts_between(a, b), themes, prev, nxt, built, extra, up, classic)
            fname = f"{kind}-{k}.html"
            with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
                f.write(html_text)
            written.add(fname)
            grp = bucket[k]
            out.append({"k": k, "n": len(grp), "l": sum(n["l"] for n in grp),
                        "top": [n["id"] for n in sorted(grp, key=lambda n: (n["l"], n["r"]), reverse=True)[:3]]})
        summaries[kind] = list(reversed(out))

    # remove pages for periods that no longer exist (never touches issue.css / issue.js)
    for f in os.listdir(out_dir):
        if re.match(r"(week|month)-[\d-]+\.html$", f) and f not in written:
            os.remove(os.path.join(out_dir, f))
    return summaries["week"], summaries["month"], len(written)
