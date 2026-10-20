# MagickVision Signal Band (preview build)

A standalone page that lives in its own folder. It does not change, replace or
re-link any existing page on the site.

Once uploaded, it lives at **https://magickmica.github.io/signal/**

## What's in the folder

| File | What it is |
| --- | --- |
| `index.html` | The Signal Band page |
| `mm-band.js` | The band and the "received" panel (no libraries) |
| `signal.js` | Week-by-week summary of every note and article (generated, about 48 KB) |
| `build_signal.py` | Rebuilds `signal.js` from `_data/` |

## Installing

Drag the whole `signal` folder into the repo root on GitHub, next to `index.html`.
Nothing else needs to change.

## Refreshing the data

After the usual update (`merge_notes.py`, `build_articles.py`, `build_digests.py`,
`update_pages.py`), run one more command from the repo root:

```bash
python3 signal/build_signal.py
```

It reads, and never writes to, `_data/notes_with_media_compact.json`,
`_data/magazine_articles.json`, `minimags.html` and the issue pages (for each
issue's accent colour). It writes only `signal/signal.js`.

## Linking to a week

Add `#w` plus the week's Monday to the address, for example
`https://magickmica.github.io/signal/#w2026-08-10`. The address updates as you tune,
so any week can be shared.

## How it connects to the existing site

The page only links out to pages that already exist:

- "Watch the full broadcast" → `week-YYYY-MM-DD.html`
- "Search this week's notes" → `notes.html?from=…&to=…`, which the Notes page already supports
- "Open the … issue" → `month-YYYY-MM.html`
- Notes and articles → Substack

On the live site it also loads the shared top bar (`mm-nav.js`). To give it a place
in the site menu later, add `signal/` to the menu.

**Building from a different data copy:** set `MM_DATA` to that folder, e.g.
`MM_DATA=/path/to/_data python3 signal/build_signal.py`. Without it, the repo's `_data/` is used.
