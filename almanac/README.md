# The Y3K Almanac (preview build)

A book of days: every calendar date has a page holding what Magick Mica TV
transmitted on that date in every year. It lives in its own folder and does not
change, replace or re-link any existing page on the site.

Once uploaded, it lives at **https://magickmica.github.io/almanac/** and opens on today's date.

| File | What it is |
| --- | --- |
| `index.html` | The almanac page |
| `almanac.js` | Up to 16 most-loved notes per calendar date, with counts and articles (generated, about 670 KB) |
| `build_almanac.py` | Rebuilds `almanac.js` from `_data/` |

**Install:** drag the `almanac` folder into the repo root on GitHub.

**Refresh** after the usual update, from the repo root:

```bash
python3 almanac/build_almanac.py
```

It reads `_data/notes_with_media_compact.json`, `_data/magazine_articles.json` and
`minimags.html` and never writes to them. It writes only `almanac/almanac.js`.

**Link to a day:** add `#d` plus month and day, e.g. `/almanac/#d08-12`.

Each page links out to pages that already exist: `notes.html?from=…&to=…` for every
note from that date, and the matching `week-….html` issue.

The moon phase shown on each page is calculated for that date in the current year.

**Building from a different data copy:** set `MM_DATA` to that folder, e.g.
`MM_DATA=/path/to/_data python3 almanac/build_almanac.py`. Without it, the repo's `_data/` is used.
