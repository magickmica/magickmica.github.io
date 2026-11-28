"""Build the single-file site (emoji/index.html) from the source files in this folder."""
import sys, os
SRC = os.path.dirname(os.path.abspath(__file__)) + "/"
ORDER = ["emoji-data.js", "symbols.js", "substack.js", "app.js", "playground-data.js", "playground.js"]
h = open(SRC + "index.html", encoding="utf8").read()
for f in ORDER:
    tag = f'<script src="{f}"></script>'
    assert tag in h, f
    js = open(SRC + f, encoding="utf8").read().replace("</script", "<\\/script")
    h = h.replace(tag, "<script>\n" + js + "\n</script>")
lic = ("<!--\n  Super Magick Emoji + Magick Mica Emoji Playground: a single-file emoji site.\n"
       "  Emoji names/groups: unicode-emoji-json (MIT). Keywords: emojilib (MIT).\n\n"
       + open(SRC + "licenses/unicode-emoji-json.txt").read() + "\n\n" + open(SRC + "licenses/emojilib.txt").read() + "\n-->\n")
h = h.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n" + lic, 1)
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SRC, "..", "index.html")
open(out, "w", encoding="utf8").write(h)
print("built", out, len(h))
