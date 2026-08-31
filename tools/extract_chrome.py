#!/usr/bin/env python3
"""
MAGICKMICA - extract_chrome.py
Lifts the ambient decoration layer out of each original index-*.html so the
mosaic template can keep it.

Every frequency page carries its own hand-built effects behind a two-letter
class prefix: hw- for halloween (bats, fog, ghosts, spiders, webs), se- for
sea (bubbles, fish, jellyfish, crabs, caustics), wn- for winter (flakes,
aurora, frost, icicles), and so on. Rebuilding that by hand would lose the
detail, so this pulls the real CSS, markup and keyframes straight from the
live pages.

    python3 tools/extract_chrome.py <repo> > tools/chrome.py
"""
import re, os, glob, json, sys

PREFIX = {
    "index-alien.html": "al", "index-arcade.html": "ar", "index-candy.html": "cd",
    "index-cottage.html": "ct", "index-dream.html": "dr", "index-fall.html": "fl",
    "index-halloween.html": "hw", "index-sea.html": "se", "index-summer.html": "sm",
    "index-vhs.html": "vh", "index-winter.html": "wn", "index-witches.html": "wg",
    "index-witching.html": "wt", "index-wonderland.html": "wl",
}

NAME = {
    "index-alien.html": "alien", "index-arcade.html": "arcade", "index-candy.html": "candy",
    "index-cottage.html": "cottage", "index-dream.html": "dream", "index-fall.html": "fall",
    "index-halloween.html": "halloween", "index-sea.html": "sea", "index-summer.html": "summer",
    "index-vhs.html": "vhs", "index-winter.html": "winter", "index-witches.html": "witches",
    "index-witching.html": "witching", "index-wonderland.html": "wonderland",
}


def split_rules(css):
    """Yield (selector, body) for top-level rules, keeping @media/@keyframes whole."""
    out, i, n = [], 0, len(css)
    while i < n:
        brace = css.find("{", i)
        if brace == -1:
            break
        sel = css[i:brace].strip()
        depth, j = 1, brace + 1
        while j < n and depth:
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
            j += 1
        out.append((sel, css[brace + 1:j - 1], css[i:j]))
        i = j
    return out


def extract(path, prefix):
    html = open(path, encoding="utf-8").read()
    blocks = re.findall(r"<style>(.*?)</style>", html, re.DOTALL)

    keep, anims = [], set()
    for block in blocks:
        for sel, body, whole in split_rules(block):
            if sel.startswith("@keyframes"):
                continue
            if sel.startswith("@media"):
                inner = [w for s2, b2, w in split_rules(body) if f".{prefix}-" in s2]
                if inner:
                    keep.append(sel + "{" + "".join(inner) + "}")
                    for b2 in inner:
                        anims.update(re.findall(r"animation(?:-name)?\s*:\s*([\w-]+)", b2))
                continue
            if f".{prefix}-" in sel:
                keep.append(whole)
                anims.update(re.findall(r"animation(?:-name)?\s*:\s*([\w-]+)", body))
                anims.update(re.findall(r"animation\s*:[^;]*?\b([a-zA-Z]\w+)\b", body))

    # pull in every keyframe those rules reference
    for block in blocks:
        for sel, body, whole in split_rules(block):
            if not sel.startswith("@keyframes"):
                continue
            name = sel.split()[-1].strip()
            if name in anims or name.lower().startswith(prefix):
                keep.append(whole)

    css = "\n".join(keep)

    # markup: every top-level element in the body carrying the prefix
    # the decoration markup sits between style blocks on these pages,
    # not after the last one, so scan the whole document body
    body_html = html[html.find("<body"):]
    nodes = []
    for m in re.finditer(r'<(\w+)[^>]*class="[^"]*\b' + prefix + r'-[^"]*"[^>]*>', body_html):
        tag, start = m.group(1), m.start()
        if any(start < e for _, e in nodes):
            continue
        depth, j = 1, m.end()
        if body_html[m.end() - 2] == "/":
            nodes.append((start, m.end()))
            continue
        while j < len(body_html) and depth:
            nxt = re.search(r"<(/?)" + tag + r"\b", body_html[j:])
            if not nxt:
                break
            j += nxt.end()
            depth += -1 if nxt.group(1) else 1
        end = body_html.find(">", j) + 1
        nodes.append((start, end))
    markup = "\n".join(body_html[s:e] for s, e in nodes)
    return css, markup


if __name__ == "__main__":
    repo = sys.argv[1] if len(sys.argv) > 1 else "livecheck/magickmica.github.io-main"
    result = {}
    for fname, prefix in PREFIX.items():
        p = os.path.join(repo, fname)
        if not os.path.exists(p):
            continue
        css, markup = extract(p, prefix)
        result[NAME[fname]] = {"css": css, "html": markup, "js": ""}
        sys.stderr.write(f"{NAME[fname]:12} css {len(css):6}  markup {len(markup):5}\n")
    json.dump(result, open("/tmp/chrome_raw.json", "w", encoding="utf-8"))
    sys.stderr.write(f"\nwrote /tmp/chrome_raw.json with {len(result)} themes\n")
