# Super Magick Emoji + Magick Mica Emoji Playground: source

The live page is the single file `emoji/index.html`. It's built from the files in this folder.
Edit these files, then rebuild. Don't edit `emoji/index.html` by hand.

| File | What's in it |
| --- | --- |
| `index.html` | Page shell, menu, footer and all the styles |
| `emoji-data.js` | All 1,914 standard emojis: names, groups, versions, keywords (unicode-emoji-json + emojilib, MIT) |
| `symbols.js` | Special symbols and combined-emoji sets |
| `substack.js` | Substack category: script letters, writing, journals, reading, podcasting |
| `app.js` | Directory pages, search, copy, favorites, routing (`#/…` links) |
| `playground-data.js` | Playground data only: Shuffler categories, the tool list, counts |
| `playground.js` | Playground page and the Emoji Shuffler |
| `egyptian-data.js` | Egyptian combos and the hieroglyph range |
| `extras.js` | Egyptian and A–Z Letters pages, saving combos (♡) and the Bookmark button |
| `../fonts/hieroglyphs.woff2` | Noto Sans Egyptian Hieroglyphs (OFL); only downloaded on pages that show hieroglyphs |

## Rebuild

```
python3 emoji/src/build.py
```

This writes `emoji/index.html`. Commit both, and GitHub Pages serves the new version. There's no server and nothing to install.

## Add a Shuffler category

Add an entry to `SHUFFLE_CATEGORIES` in `playground-data.js` (an id, name, icon, blurb and a `pool` of emojis separated by spaces). Any emoji that isn't in `emoji-data.js` is skipped automatically.

## Add a Playground tool

Each tool has an entry in `PLAYGROUND_TOOLS`. `status: "soon"` shows a Coming soon card. When the tool is built, write its panel in `playground.js` (with an element whose id matches the tool id), add it to `pagePlayground`, and set `status: "live"`.

## What's saved in the visitor's browser

Everything is in localStorage; bad or old saved data is ignored safely.

- `sme-favs`: favorites
- `sme-recent`: recently copied
- `sme-tone`: skin tone
- `sme-shuffler`: the Shuffler's category, count, mix and locks
- `sme-saved`: saved combos, mixes and letters (shown on Favorites)
- `sme-az-style`: the A–Z page's alphabet style
