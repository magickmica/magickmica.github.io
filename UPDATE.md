# MAGICKMICA — UPDATE RUNBOOK

Everything needed to refresh the site lives in `tools/`. Commit that folder
to the repo so it can never go missing again.

---

## THE 5-MINUTE REFRESH

### 1. Collect your notes
Go to `https://substack.com/@magickmica/notes` (logged in).
Press F12 → Console. Type `allow pasting`, press Enter.
Paste the contents of `tools/collect_notes.js`, press Enter.

It pages backwards to `CUTOFF` (default `2026-07-15`), then downloads
`notes_refresh.json`. Overlap is safe — duplicates are merged by note id.

### 2. Export both newsletters
Substack → Settings → Export, for **MagickMica TV** and **MagickMica Art**.
Two `.zip` files arrive by email.

### 3. Hand all three to Claude
Upload `notes_refresh.json` + both zips, plus `tools/` and `_data/`,
and say **"run the update."**

Claude runs, in order:

```bash
python3 tools/merge_notes.py    <repo> _data notes_refresh.json
python3 tools/build_articles.py _data <tv_export> <art_export>
python3 tools/build_digests.py  <repo> _data build
python3 tools/update_pages.py   <repo> _data build
```

### 4. Upload the changed files
Claude hands back a ZIP. Drag its contents into the repo root on GitHub.

---

## WHAT EACH TOOL DOES

| Tool | Job |
|---|---|
| `collect_notes.js` | Browser-console collector. Downloads `notes_refresh.json`. |
| `merge_notes.py` | Merges new notes into `_data/notes_with_media_compact.json`, deduped by id. Fresh like/restack counts win. Falls back to the `NOTES` blob in `notes.html` if the master is missing. |
| `build_articles.py` | Rebuilds `_data/magazine_articles.json` from the two exports. |
| `build_digests.py` | Regenerates every `week-*.html` and `month-*.html`. |
| `update_pages.py` | Swaps the embedded JSON pools in the core + frequency pages, and rebuilds the `minimags.html` grids. |

---

## RULES THAT MUST NOT BE BROKEN

**1. JSON injection uses a lambda.** Never a plain replacement string —
Python interprets `\n` and backslashes in the replacement and corrupts the
JS with "Invalid or unexpected token".

```python
pat.sub(lambda m: f"const {name} = {payload};", html_text, count=1)
```

**2. Image URL formats differ by use.**
- Notes: CDN wrapper at `w_400`
- Article covers: CDN wrapper at `w_600`

Signature `$s_!G4Yk!` is constant. Verified: 168/168 note URLs and 70/71
covers match what the site already serves.

**3. Cover picker.** Blacklist any image appearing in ≥3 posts (logos,
banners, footers), then take the first substantial image, skipping
thin banners (height <100 or aspect >4) and icons (min dimension <400).

**4. Cross-posted articles.** Five posts exist in *both* exports; the TV
copy is an empty stub with no body file. `dedupe()` keeps whichever copy
has real content. Without it, five covers silently vanish.

**5. Curated pools are never auto-regenerated.** `QUEST`, `POS`,
`AFFIRMATIONS`, `DREAM_POOL`, `PROMPTS`, `SYMBOLS`, `MOODS` are
hand-themed, not top-N-by-likes. They're in `update_pages.CURATED`.

**6. Accent colours are derived, not invented.** Months cycle by absolute
month number `(year*12 + month) % 8`; weeks cycle by position in the
sorted week list. Verified 51/51 against existing digests.

---

## KNOWN STATE (as of 2026-08-30)

- **Notes: 5,615** through Aug 30 2026, 3,762 with images
- **Articles: 86 published** (48 TV + 38 Art)
- **Digests: 65** — 13 monthly + 52 weekly
- **Index variants: 16** — `index.html` plus 15 `index-*.html`
  (briefing said 12; the extras are `index-NEW`, `index-winter`, `index-witches`)
- `analytics.html` was built but **never pushed** — it is not in the repo
- Articles without covers: `we-fly-free`,
  `the-goddess-on-the-phone-cosmic-tarot` (only image is 600×334, below
  the 400px minimum). "THE DAILY ENCHANTMENT" now *has* a cover.
- `files.zip` in the repo root is a stale June 20 snapshot containing a
  `queen.html` that isn't live — safe to delete.

---

## NEXT: THE POOLS REFACTOR (not yet done)

All 16 index variants each embed their own 150-note `MTV_NOTES` blob.
That's why a content refresh touches 23+ files.

**Fix:** move the shared pools into one `pools.json` and have each page
`fetch()` it at load (same-origin on GitHub Pages, so it just works).
Keep a small inline fallback so a failed fetch degrades gracefully.

After that, a refresh writes *one small JSON file* and the 16 index
variants never change again — changed files drop from ~70 to about 5.
