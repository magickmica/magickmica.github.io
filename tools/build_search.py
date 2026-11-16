#!/usr/bin/env python3
"""
MAGICKMICA - build_search.py  ·  the site-wide search index

    python3 tools/build_search.py            # run from anywhere

Writes search-index.json at the repo root. The search box on index.html
(mm-search.js) loads that file the first time someone clicks into it, and
searches it entirely in the browser. No outside service, no accounts.

What gets indexed:
  pages     every public .html page in the repo: its <title>, description,
            headings and the start of its visible text
  articles  every Substack article in _data/magazine_articles.json
  notes     every note in _data/notes_with_media_compact.json, linked to
            Substack and to the on-site weekly issue it appears in

What is kept OUT (edit the lists just below to change it):
  - PRIVATE pages: never indexed, even if they are uploaded to the repo
  - homepage copies (index.html, index-*.html, index2.html), 404, the
    Google verification stub, previews
  - any page with <meta name="robots" content="noindex">
  - reader/ issue pages (duplicates of the week-*/month-* issues)
  - folders that are not site pages (tools/, _data/, incoming/, data/, .github/)

It also makes sure index.html has the search box: if the box or its
<script> tag is missing (say a homepage was rebuilt without it), it puts
them back, right under the header. Nothing else on the page is touched.

When to run it: tools/update_all.py runs it after every update, and the
"Search index" workflow runs it on GitHub whenever a .html page is uploaded.
So normally nothing needs doing by hand.

Index format (compact arrays, to keep the download small):
  {"v":1, "built":"...", "img":<note image URL prefix>,
   "pages":    [[url, title, kind, description, text], ...],
   "articles": [[url, title, subtitle, date, newsletter, cover], ...],
   "notes":    [[id, date, text, image_key, week_page], ...]}
"""
import datetime
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(TOOLS)
DATA = os.path.join(REPO, "_data")
OUT = os.path.join(REPO, "search-index.json")

# ---- never index these, even if they exist in the repo -------------------
PRIVATE = {
    "get-products.html",
}
PRIVATE_PREFIX = ("get-products",)

# ---- not useful as search results ---------------------------------------
SKIP = {"404.html", "index.html", "index2.html", "home-preview.html"}
SKIP_PREFIX = ("google", "index-")
SKIP_DIRS = {"tools", "_data", "incoming", "data", "node_modules", "build", "reader/issues"}
# reader/ keeps its own copies of the weekly and monthly issues
SKIP_PATTERNS = (re.compile(r"^reader/(week|month)-.*\.html$"),)

NOTE_IMG = ("https://substackcdn.com/image/fetch/$s_!G4Yk!,w_400,c_limit,f_webp,"
            "q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media."
            "s3.amazonaws.com%2Fpublic%2Fimages%2F")

PAGE_TEXT = 700      # characters of visible text kept per page
NOTE_TEXT = 600      # characters kept per note (the full note is on Substack)

TITLE_TAIL = re.compile(r"\s*[—|·-]\s*(Magick ?Mica( TV)?|MAGICKMICA)\s*$", re.I)


class PageText(HTMLParser):
    """Pulls title, description, robots, headings and visible text out of a page."""
    SKIP_TAGS = {"script", "style", "noscript", "svg", "template", "nav", "footer", "head"}
    HEADS = {"h1", "h2", "h3"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.desc = ""
        self.ogdesc = ""
        self.noindex = False
        self.heads = []
        self.text = []
        self._skip = 0
        self._in_title = False
        self._head = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta":
            name = (a.get("name") or a.get("property") or "").lower()
            content = a.get("content") or ""
            if name == "description":
                self.desc = content
            elif name == "og:description":
                self.ogdesc = content
            elif name == "robots" and "noindex" in content.lower():
                self.noindex = True
            return
        if tag == "title":
            self._in_title = True
        if tag in self.SKIP_TAGS:
            self._skip += 1
        elif tag in self.HEADS and not self._skip:
            self._head = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in self.SKIP_TAGS and self._skip:
            self._skip -= 1
        elif tag in self.HEADS and self._head is not None:
            h = squash(" ".join(self._head))
            if h and h not in self.heads:
                self.heads.append(h)
            self._head = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
            return
        if self._skip:
            return
        if self._head is not None:
            self._head.append(data)
        self.text.append(data)


def squash(s):
    """One line of plain text. Unescapes leftover entities (the exports hold
    some as literal "&amp;") so the search box does not show them."""
    return re.sub(r"\s+", " ", html.unescape(s or "")).strip()


def clip(s, n):
    s = squash(s)
    if len(s) <= n:
        return s
    cut = s[:n].rsplit(" ", 1)[0]
    return cut + "…"


def nav_kinds():
    """Section name for each page, from the drawer menu (_data/sitemap_nav.json,
    then the older copy at the repo root for pages the current menu leaves out)."""
    kinds = {}
    for path in (os.path.join(DATA, "sitemap_nav.json"), os.path.join(REPO, "sitemap_nav.json")):
        try:
            with open(path, encoding="utf-8") as f:
                nav = json.load(f)
        except (OSError, ValueError):
            continue
        for group, items in nav.items():
            if group.startswith("_"):
                continue
            for href, _label in items:
                kinds.setdefault(href, group)
    return kinds


def kind_for(rel, kinds):
    name = os.path.basename(rel)
    url = rel[:-len("index.html")] if rel.endswith("/index.html") else rel
    if url in kinds:
        return kinds[url]
    if name.startswith("week-"):
        return "Weekly issue"
    if name.startswith("month-"):
        return "Monthly issue"
    if "vault" in name:
        return "Vault"
    if "broadcast" in name:
        return "Broadcast"
    if rel.endswith("/index.html"):
        return rel.split("/")[0].capitalize()
    return "Page"


def wanted(rel):
    name = os.path.basename(rel)
    if name in PRIVATE or name.startswith(PRIVATE_PREFIX):
        return False
    if "/" not in rel and (name in SKIP or name.startswith(SKIP_PREFIX)):
        return False
    if any(p.match(rel) for p in SKIP_PATTERNS):
        return False
    return True


def collect_pages():
    kinds = nav_kinds()
    pages, skipped = [], []
    for root, dirs, files in os.walk(REPO):
        relroot = os.path.relpath(root, REPO).replace(os.sep, "/")
        relroot = "" if relroot == "." else relroot
        dirs[:] = sorted(
            d for d in dirs
            if not d.startswith((".", "_")) and
            (f"{relroot}/{d}" if relroot else d) not in SKIP_DIRS)
        for name in sorted(files):
            if not name.endswith(".html"):
                continue
            rel = f"{relroot}/{name}" if relroot else name
            if not wanted(rel):
                skipped.append(rel)
                continue
            with open(os.path.join(root, name), encoding="utf-8", errors="replace") as f:
                src = f.read()
            p = PageText()
            try:
                p.feed(src)
            except Exception:  # a malformed page still gets its title
                pass
            if p.noindex:
                skipped.append(rel)
                continue
            title = TITLE_TAIL.sub("", squash(html.unescape(p.title))) or name[:-5]
            desc = squash(p.desc or p.ogdesc)
            heads = " · ".join(h for h in p.heads[:12] if h.lower() != title.lower())
            text = " ".join([heads, squash(" ".join(p.text))]).strip()
            url = rel[:-len("index.html")] if rel.endswith("/index.html") else rel
            pages.append([url, title, kind_for(rel, kinds), clip(desc, 240), clip(text, PAGE_TEXT)])
    return pages, skipped


def collect_articles():
    try:
        with open(os.path.join(DATA, "magazine_articles.json"), encoding="utf-8") as f:
            arts = json.load(f)
    except (OSError, ValueError):
        return []
    out = []
    for a in sorted(arts, key=lambda a: a.get("date") or "", reverse=True):
        if not a.get("url") or not a.get("title"):
            continue
        out.append([a["url"], squash(a["title"]),
                    clip(a.get("subtitle") or a.get("preview") or "", 240),
                    a.get("date") or "", a.get("newsletter") or "",
                    a.get("cover_url") or ""])
    return out


def week_page(date, existing):
    try:
        d = datetime.date.fromisoformat(date)
    except (TypeError, ValueError):
        return ""
    monday = d - datetime.timedelta(days=d.weekday())
    name = f"week-{monday.isoformat()}.html"
    return name if name in existing else ""


def collect_notes():
    try:
        with open(os.path.join(DATA, "notes_with_media_compact.json"), encoding="utf-8") as f:
            notes = json.load(f)
    except (OSError, ValueError):
        return []
    existing = set(os.listdir(REPO))
    out = []
    for n in sorted(notes, key=lambda n: (n.get("d") or "", n.get("id") or 0), reverse=True):
        body = squash(n.get("b") or "")
        if not body or not n.get("id"):
            continue
        img = n.get("t") or ""
        img = img[len(NOTE_IMG):] if img.startswith(NOTE_IMG) else img
        out.append([n["id"], n.get("d") or "", clip(body, NOTE_TEXT), img,
                    week_page(n.get("d"), existing)])
    return out


HOME = os.path.join(REPO, "index.html")
BOX = '<div id="mm-search"></div>'
TAG = '<script src="mm-search.js?v=1" defer></script>'


def ensure_home_box():
    """Put the search box and its script into index.html if either is missing."""
    try:
        with open(HOME, encoding="utf-8") as f:
            page = f.read()
    except OSError:
        return
    before = page
    if 'id="mm-search"' not in page and "</header>" in page:
        page = page.replace("</header>", "</header>\n" + BOX, 1)
    if "mm-search.js" not in page and "</body>" in page:
        i = page.rfind("</body>")
        page = page[:i] + TAG + "\n" + page[i:]
    if page != before:
        with open(HOME, "w", encoding="utf-8") as f:
            f.write(page)
        print("index.html: search box added")


def main():
    ensure_home_box()
    pages, skipped = collect_pages()
    articles = collect_articles()
    notes = collect_notes()
    index = {
        "v": 1,
        "built": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "img": NOTE_IMG,
        "pages": pages,
        "articles": articles,
        "notes": notes,
    }
    payload = json.dumps(index, ensure_ascii=False, separators=(",", ":"))
    # Leave the file alone when only the timestamp would change, so the
    # workflow does not make empty commits.
    try:
        with open(OUT, encoding="utf-8") as f:
            old = json.load(f)
        old["built"] = index["built"]
        if json.dumps(old, ensure_ascii=False, separators=(",", ":")) == payload:
            print(f"search-index.json already up to date "
                  f"({len(pages)} pages, {len(articles)} articles, {len(notes):,} notes)")
            return 0
    except (OSError, ValueError, KeyError):
        pass
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(payload)
    print(f"search-index.json: {len(pages)} pages, {len(articles)} articles, "
          f"{len(notes):,} notes, {len(payload.encode('utf-8')) / 1024:,.0f} KB")
    print(f"left out {len(skipped)} pages: {', '.join(skipped[:12])}"
          f"{' …' if len(skipped) > 12 else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
