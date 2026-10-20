# Transmission Reader 98 (preview build)

Every Magick Mica transmission, received in a recovered late-90s mail reader:
folders, sortable columns, Find, a preview pane, and new messages marked unread
since your last visit. It lives in its own folder and does not change, replace or
re-link any existing page on the site.

Once uploaded, it lives at **https://magickmica.github.io/reader/**

| File | What it is |
| --- | --- |
| `index.html` | The reader |
| `mailbox.js` | Every note, issue and article (generated, about 990 KB) |
| `build_reader.py` | Rebuilds `mailbox.js` from `_data/` |

**Install:** drag the `reader` folder into the repo root on GitHub.

**Refresh** after the usual update, from the repo root:

```bash
python3 reader/build_reader.py
```

It reads `_data/notes_with_media_compact.json`, `_data/magazine_articles.json` and
`minimags.html` and never writes to them. It writes only `reader/mailbox.js`.

**Folders:** Inbox, Most Loved, With Pictures, Words Only; the ten theme tags already
on 1,083 notes (Cosmic, Queens, Animals, Wonderland and the rest); Weekly and Monthly
Y3K issues; MagickMica TV and MagickMica Art articles.

**Link to a folder:** `/reader/#loved`, `/reader/#weekly`, `/reader/#theme-egypt`, …

**Unread:** on a first visit, the latest week arrives unread. After that, only notes
added since the last visit are marked new. This is remembered in the visitor's own
browser only.

**Building from a different data copy:** set `MM_DATA` to that folder, e.g.
`MM_DATA=/path/to/_data python3 reader/build_reader.py`. Without it, the repo's `_data/` is used.
