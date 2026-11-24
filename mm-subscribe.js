/* MAGICKMICA - mm-subscribe.js  (v3, 24 Nov 2026)
 * Every Substack subscribe call-to-action on the site, from one file.
 *
 * Put a placeholder where a box should go, and load this file once:
 *
 *   <div data-mm-subscribe="full"></div>      big teaser box (homepage)
 *   <div data-mm-subscribe="compact"></div>   slim strip (notes, blog sidebar)
 *   <div data-mm-subscribe="banner" data-theme="circus"></div>
 *                                             themed end-of-page banner
 *   <script src="mm-subscribe.js?v=2" defer></script>
 *
 * Banner themes (data-theme): signal (default), circus, tapes, sky, y3k, archive.
 * Each theme has its own wording in THEMES below; a page can override it with
 * data-eyebrow / data-title / data-sub / data-button / data-art on the placeholder.
 *
 * Moving a box up into the page:
 *   data-after="#grid" data-rows="2"
 *     puts the box inside that grid or list, after its first 2 rows (6 cards on
 *     a 3-column desktop, 4 on a phone). Rows are counted from the live layout,
 *     so it holds at any width, and it follows the grid when the page redraws it
 *     (filters, searches). If there are too few cards, the box stays where it
 *     was put in the page. data-min="4" (the default) is the fewest cards
 *     shown before the box, so a one-column phone layout still shows a few.
 *
 * Other options on any placeholder:
 *   data-pub="art"     point it at Magick Mica Art instead of Magick Mica TV
 *   data-mode="embed"  show Substack's own white sign-up box instead of the styled form
 *
 * After-game prompt: on any page that also loads mm-prizes.js (the circus
 * games), a small card slides in a moment after the first round that pays
 * out tickets. It shows at most once per visit, "Not now" hides it for a
 * week, and anyone who subscribes through it never sees it again.
 * Add data-no-subscribe-prompt to <body> to switch it off on a page.
 *
 * The forms send the visitor to Substack's own subscribe page with their
 * email filled in, so Substack does the actual sign-up and confirmation.
 * tools/add_subscribe.py puts the placeholders into the pages, and
 * update_all.py runs it on every site update.
 */
(function () {
  "use strict";

  var PUBS = {
    tv:  { url: "https://magickmica.substack.com",    name: "Magick Mica TV" },
    art: { url: "https://magickmicaart.substack.com", name: "Magick Mica Art" }
  };

  var COPY = {
    label: "✦ JOIN THE SIGNAL · FREE",
    title: "Get the transmissions before anyone else",
    lede: "The site is the archive. The inbox is where it lands first.",
    perksHead: "Subscribers get",
    perks: [
      ["📺", "Every new broadcast, sent the moment it airs"],
      ["🔮", "Subscriber-only transmissions that never get posted here"]
    ],
    button: "Subscribe",
    fine: "Free on Substack · unsubscribe anytime",
    compactTitle: "Like these? Get the next ones in your inbox.",
    compactSub: "Subscribers get new broadcasts first, plus subscriber-only transmissions.",
    alsoArt: "Also: Magick Mica Art ↗",
    alsoTv: "Also: Magick Mica TV ↗",
    notes: "New circus games: follow my Notes ↗",
    notesUrl: "https://substack.com/@magickmica",
    done: "✦ Almost there: confirm on the Substack tab that just opened."
  };

  /* One entry per banner theme: wording + colours. a/b are the two accents,
     glow is an "r,g,b" for shadows, bg the card background, ink the body text. */
  var THEMES = {
    signal: {
      art: "📡", eyebrow: "✦ JOIN THE SIGNAL · FREE",
      title: "Get the next transmission in your inbox",
      sub: "Every new broadcast the moment it airs, plus subscriber-only transmissions that never get posted here.",
      button: "Subscribe",
      a: "#ffce5c", b: "#ff4fa3", glow: "208,107,255", ink: "#c9c0e4",
      bg: "radial-gradient(120% 140% at 0% 0%,rgba(208,107,255,.26),transparent 55%),radial-gradient(120% 140% at 100% 100%,rgba(255,36,64,.16),transparent 55%),#140419"
    },
    circus: {
      art: "🎪", eyebrow: "🎟 FROM THE CIRCUS · FREE",
      title: "Get my new articles in your inbox",
      sub: "Subscribers get every new article the day it's published. New circus games get announced in my Notes.",
      button: "Subscribe", notes: true,
      a: "#ffd166", b: "#ff3d6e", glow: "255,61,110", ink: "#f0d7c8",
      bg: "repeating-linear-gradient(90deg,rgba(255,61,110,.10) 0 28px,transparent 28px 56px),radial-gradient(120% 120% at 50% 0%,rgba(255,209,102,.22),transparent 60%),#1b0716"
    },
    tapes: {
      art: "📼", eyebrow: "● REC · NEW TAPES WEEKLY",
      title: "Catch the next tape the night it airs",
      sub: "This shelf is the reruns. Subscribers get every new transmission in their inbox the moment it goes out.",
      button: "Start recording",
      a: "#27e8f5", b: "#ff3fae", glow: "39,232,245", ink: "#bcd3e6",
      bg: "repeating-linear-gradient(0deg,rgba(255,255,255,.025) 0 2px,transparent 2px 4px),radial-gradient(120% 140% at 0% 100%,rgba(255,63,174,.2),transparent 55%),radial-gradient(120% 140% at 100% 0%,rgba(39,232,245,.16),transparent 55%),#0a0d1d"
    },
    sky: {
      art: "🌌", eyebrow: "✧ A NEW STAR EVERY NIGHT",
      title: "Let the next transmission find you",
      sub: "A new constellation rises here every day. New broadcasts land in your inbox the moment they air, free.",
      button: "Follow the stars",
      a: "#a8d8ff", b: "#ffe9b0", glow: "120,160,255", ink: "#bcc6e6",
      bg: "radial-gradient(1.5px 1.5px at 12% 30%,#fff,transparent),radial-gradient(1px 1px at 38% 70%,#fff,transparent),radial-gradient(1.5px 1.5px at 66% 22%,#fff,transparent),radial-gradient(1px 1px at 88% 64%,#fff,transparent),radial-gradient(120% 140% at 100% 0%,rgba(120,160,255,.22),transparent 60%),#070b1f"
    },
    y3k: {
      art: "📰", eyebrow: "✦ ENJOYED THIS ISSUE? · FREE",
      title: "Get the next transmission in your inbox",
      sub: "Every new broadcast the moment it airs, plus subscriber-only transmissions that never get posted here.",
      button: "Subscribe",
      a: "#ffd250", b: "#ff2d9b", glow: "255,45,155", ink: "#d2c6e8",
      bg: "radial-gradient(120% 140% at 0% 0%,rgba(255,45,155,.22),transparent 55%),radial-gradient(120% 140% at 100% 100%,rgba(0,240,255,.12),transparent 55%),#10031a"
    },
    archive: {
      art: "🔮", eyebrow: "✦ YOU FOUND THE ARCHIVE",
      title: "Get the new ones before they're archived",
      sub: "Everything here aired first in the newsletter. Subscribe free and the next transmission comes straight to you.",
      button: "Subscribe",
      a: "#ffd166", b: "#22e0ff", glow: "160,32,240", ink: "#c3bbde",
      bg: "radial-gradient(120% 95% at 20% 10%,rgba(160,32,240,.34),transparent 62%),radial-gradient(100% 85% at 90% 90%,rgba(34,224,255,.14),transparent 62%),#12061f"
    }
  };

  var GAME = {
    eyebrow: "🎟 NICE ROUND!",
    title: "Enjoying the circus?",
    sub: "New circus games get announced in my Notes. Subscribe free and my new articles land in your inbox.",
    button: "Subscribe",
    later: "Not now"
  };

  var STORE_DONE = "mm_sub_done_v1", STORE_SNOOZE = "mm_sub_snooze_v1", SESSION_SHOWN = "mm_sub_prompt_v1";

  var CSS = [
    ".mmsub{--mmsub-a:var(--pink,#ff4fa3);--mmsub-b:var(--gold,#ffce5c);--mmsub-c:var(--cyan,#6fc3ff);",
    "position:relative;box-sizing:border-box;border-radius:18px;color:#efe6ff;",
    "font-family:'IBM Plex Mono',ui-monospace,monospace;text-align:left;overflow:hidden;",
    "background:radial-gradient(120% 140% at 0% 0%,rgba(208,107,255,.22),transparent 55%),",
    "radial-gradient(120% 140% at 100% 100%,rgba(255,36,64,.16),transparent 55%),rgba(18,4,24,.82);",
    "border:1px solid rgba(208,107,255,.38);box-shadow:0 0 0 1px rgba(255,206,92,.06) inset,0 18px 50px -24px rgba(208,107,255,.55)}",
    ".mmsub *{box-sizing:border-box}",
    ".mmsub::before{content:'';position:absolute;inset:0 0 auto 0;height:2px;z-index:2;",
    "background:linear-gradient(90deg,var(--mmsub-a),var(--mmsub-b),var(--mmsub-c),var(--mmsub-a));background-size:200% 100%;",
    "animation:mmsub-sheen 6s linear infinite}",
    "@keyframes mmsub-sheen{to{background-position:200% 0}}",
    "@media (prefers-reduced-motion:reduce){.mmsub::before{animation:none}}",
    ".mmsub-lab{font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.22em;color:var(--mmsub-b);margin:0 0 10px}",
    ".mmsub-ttl{font-family:Orbitron,monospace;font-weight:700;letter-spacing:.04em;line-height:1.25;margin:0;",
    "background:linear-gradient(90deg,#fff,#f6d9ff 40%,var(--mmsub-b));-webkit-background-clip:text;background-clip:text;color:transparent}",
    ".mmsub-lede{color:#b8b0d4;font-size:13px;line-height:1.6;margin:10px 0 0}",
    ".mmsub-perks{list-style:none;margin:16px 0 0;padding:0;display:grid;gap:9px}",
    ".mmsub-perks li{display:flex;gap:10px;align-items:flex-start;font-size:13px;line-height:1.5;color:#e6dcff}",
    ".mmsub-perks .ic{flex:0 0 auto;width:26px;height:26px;display:grid;place-items:center;border-radius:8px;",
    "background:rgba(255,255,255,.05);border:1px solid rgba(208,107,255,.25);font-size:13px}",
    ".mmsub-ph{font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.2em;color:#8e85ad;margin:18px 0 0}",
    ".mmsub-form{display:flex;gap:8px;flex-wrap:wrap;margin:0}",
    ".mmsub-in{flex:1 1 180px;min-width:0;height:46px;padding:0 14px;border-radius:12px;",
    "border:1px solid rgba(208,107,255,.45);background:rgba(8,2,14,.7);color:#fff;",
    "font:inherit;font-size:14px;outline:none;transition:border-color .2s,box-shadow .2s}",
    ".mmsub-in::placeholder{color:#7a6f9e}",
    ".mmsub-in:focus{border-color:var(--mmsub-b);box-shadow:0 0 0 3px rgba(255,206,92,.18)}",
    ".mmsub-btn{flex:0 0 auto;height:46px;padding:0 20px;border:0;border-radius:12px;cursor:pointer;",
    "font-family:Orbitron,monospace;font-weight:700;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#1a0820;",
    "background:linear-gradient(135deg,#ffe7a3,var(--mmsub-b) 45%,#ff9fd2);box-shadow:0 8px 22px -10px rgba(255,206,92,.8);",
    "transition:transform .15s,filter .15s}",
    ".mmsub-btn:hover{transform:translateY(-1px);filter:brightness(1.06)}",
    ".mmsub-btn:focus-visible{outline:2px solid #fff;outline-offset:2px}",
    ".mmsub-fine{font-size:11px;color:#8e85ad;margin:10px 0 0;display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center}",
    ".mmsub-fine a{color:var(--mmsub-c);text-decoration:none}",
    ".mmsub-fine a:hover{color:var(--mmsub-a)}",
    ".mmsub-done{display:none;font-size:13px;color:var(--mmsub-b);margin:10px 0 0}",
    ".mmsub.sent .mmsub-done{display:block}",
    ".mmsub-embed{display:block;width:100%;max-width:480px;height:150px;border:0;border-radius:12px;background:#fff}",
    /* full */
    ".mmsub-full{display:grid;grid-template-columns:1.25fr 1fr;gap:28px;padding:30px 30px 28px;margin:34px 0 8px}",
    ".mmsub-full .mmsub-ttl{font-size:clamp(20px,2.6vw,28px)}",
    ".mmsub-full .mmsub-side{align-self:center;padding:22px;border-radius:14px;background:rgba(255,255,255,.035);",
    "border:1px solid rgba(255,255,255,.07)}",
    ".mmsub-full .mmsub-side .mmsub-cta{font-family:Orbitron,monospace;font-size:13px;letter-spacing:.08em;margin:0 0 12px;color:#fff}",
    ".mmsub-orb{position:absolute;right:-60px;top:-60px;width:220px;height:220px;border-radius:50%;pointer-events:none;",
    "background:radial-gradient(circle at 35% 35%,rgba(255,231,163,.35),rgba(208,107,255,.18) 45%,transparent 70%);filter:blur(2px)}",
    "@media (max-width:760px){.mmsub-full{grid-template-columns:1fr;gap:18px;padding:22px 18px}.mmsub-full .mmsub-side{padding:16px}.mmsub-full .mmsub-btn{flex:1 1 100%}}",
    /* compact */
    ".mmsub-compact{display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;padding:16px 18px;margin:14px 0}",
    ".mmsub-compact .mmsub-copy{flex:1 1 260px;min-width:0}",
    ".mmsub-compact .mmsub-ttl{font-size:14px}",
    ".mmsub-compact .mmsub-lede{font-size:12px;margin-top:4px}",
    ".mmsub-compact .mmsub-act{flex:1 1 300px;min-width:0}",
    ".mmsub-compact .mmsub-in,.mmsub-compact .mmsub-btn{height:42px}",
    ".mmsub-compact .mmsub-fine{margin-top:6px}",
    ".mmsub-compact.narrow{display:block;padding:16px}",
    ".mmsub-compact.narrow .mmsub-act{margin-top:12px}",
    ".mmsub-compact.narrow .mmsub-btn{flex:1 1 100%}",
    /* banner: themed, art + copy + form in one row, stacks on phones */
    ".mmsub-wrap{max-width:1120px;margin:40px auto;padding:0 18px}",
    ".mmsub-banner{display:grid;grid-template-columns:auto minmax(0,1.2fr) minmax(0,1fr);gap:26px;align-items:center;",
    "padding:28px 30px;background:var(--mmsub-bg);border-color:rgba(var(--mmsub-glow),.45);",
    "box-shadow:0 0 0 1px rgba(255,255,255,.04) inset,0 22px 60px -26px rgba(var(--mmsub-glow),.7)}",
    ".mmsub-banner::before{background:linear-gradient(90deg,var(--mmsub-a),var(--mmsub-b),var(--mmsub-a));background-size:200% 100%}",
    ".mmsub-banner .mmsub-lab{color:var(--mmsub-a);margin-bottom:8px}",
    ".mmsub-banner .mmsub-ttl{font-size:clamp(19px,2.3vw,25px);background:linear-gradient(90deg,#fff,#fff 35%,var(--mmsub-a));",
    "-webkit-background-clip:text;background-clip:text;color:transparent}",
    ".mmsub-banner .mmsub-lede{color:var(--mmsub-ink);margin-top:8px}",
    ".mmsub-banner .mmsub-in{border-color:rgba(var(--mmsub-glow),.5)}",
    ".mmsub-banner .mmsub-in:focus{border-color:var(--mmsub-a);box-shadow:0 0 0 3px rgba(var(--mmsub-glow),.22)}",
    ".mmsub-banner .mmsub-btn,.mmsub-pop .mmsub-btn{background:linear-gradient(135deg,var(--mmsub-a),var(--mmsub-b));",
    "box-shadow:0 8px 22px -10px rgba(var(--mmsub-glow),.9)}",
    ".mmsub-banner .mmsub-done{color:var(--mmsub-a)}",
    ".mmsub-art{width:92px;height:92px;border-radius:50%;display:grid;place-items:center;font-size:44px;line-height:1;",
    "background:radial-gradient(circle at 34% 28%,rgba(255,255,255,.28),rgba(var(--mmsub-glow),.28) 45%,rgba(0,0,0,.35) 80%);",
    "border:1px solid rgba(255,255,255,.18);box-shadow:0 0 30px rgba(var(--mmsub-glow),.45),inset 0 0 18px rgba(var(--mmsub-glow),.4);",
    "animation:mmsub-bob 4.5s ease-in-out infinite}",
    "@keyframes mmsub-bob{50%{transform:translateY(-5px) rotate(-3deg)}}",
    "@media (prefers-reduced-motion:reduce){.mmsub-art{animation:none}}",
    "@media (max-width:860px){.mmsub-banner{grid-template-columns:auto minmax(0,1fr);gap:16px 18px;padding:22px 18px}",
    ".mmsub-banner .mmsub-act{grid-column:1 / -1}.mmsub-art{width:64px;height:64px;font-size:30px}}",
    "@media (max-width:520px){.mmsub-banner{grid-template-columns:1fr;gap:14px}.mmsub-art{width:54px;height:54px;font-size:27px}",
    ".mmsub-banner .mmsub-btn{flex:1 1 100%}.mmsub-wrap{margin:28px auto;padding:0 14px}}",
    /* after-game pop-up */
    ".mmsub-pop{position:fixed;right:18px;bottom:18px;z-index:9400;width:min(360px,calc(100vw - 24px));padding:20px 18px 16px;",
    "background:var(--mmsub-bg);border-color:rgba(var(--mmsub-glow),.55);",
    "box-shadow:0 24px 60px -18px rgba(0,0,0,.8),0 0 40px -12px rgba(var(--mmsub-glow),.8);",
    "transform:translateY(24px);opacity:0;transition:transform .45s cubic-bezier(.2,.9,.3,1.2),opacity .3s}",
    ".mmsub-pop.on{transform:none;opacity:1}",
    ".mmsub-pop .mmsub-lab{color:var(--mmsub-a);margin-bottom:6px}",
    ".mmsub-pop .mmsub-ttl{font-size:17px;padding-right:22px}",
    ".mmsub-pop .mmsub-lede{font-size:12px;margin:6px 0 12px;color:var(--mmsub-ink)}",
    ".mmsub-pop .mmsub-in,.mmsub-pop .mmsub-btn{height:42px}",
    ".mmsub-pop .mmsub-btn{flex:1 1 100%}",
    ".mmsub-x{position:absolute;top:10px;right:10px;width:30px;height:30px;border-radius:50%;border:1px solid rgba(255,255,255,.2);",
    "background:rgba(0,0,0,.3);color:#ddd;cursor:pointer;font-size:14px;line-height:1}",
    ".mmsub-later{background:none;border:0;color:#a59cc4;font:inherit;font-size:11px;cursor:pointer;padding:8px 0 0;text-decoration:underline}",
    "@media (max-width:480px){.mmsub-pop{right:12px;left:12px;bottom:12px;width:auto}}",
    "@media (prefers-reduced-motion:reduce){.mmsub-pop{transition:none}}",
    /* a box moved up into a grid spans the full row and drops its own gutters */
    ".mmsub-ingrid{grid-column:1 / -1;column-span:all;min-width:0;width:100%;flex:1 1 100%;list-style:none}",
    ".mmsub-ingrid .mmsub-wrap{max-width:none;margin:10px 0;padding:0}"
  ].join("");

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function store(k, v) {
    try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) {}
    return null;
  }

  function pageName() {
    var parts = location.pathname.replace(/\/$/, "/index.html").split("/").filter(Boolean);
    var p = (parts.pop() || "index.html").replace(/\.html$/, "");
    var dir = parts.pop();
    return (dir ? dir + "-" : "") + (p || "index");
  }

  function form(pub, tag, button) {
    // A plain GET form to Substack's subscribe page, so it still works if
    // this script's submit handler never runs.
    return '<form class="mmsub-form" action="' + pub.url + '/subscribe" method="get" target="_blank" rel="noopener">' +
      '<input type="hidden" name="utm_source" value="magickmica.github.io">' +
      '<input type="hidden" name="utm_medium" value="site">' +
      '<input type="hidden" name="utm_campaign" value="subscribe-box">' +
      '<input type="hidden" name="utm_content" value="' + esc(tag + "-" + pageName()) + '">' +
      '<input class="mmsub-in" type="email" name="email" required autocomplete="email" ' +
      'placeholder="your@email.com" aria-label="Email address">' +
      '<button class="mmsub-btn" type="submit">' + esc(button || COPY.button) + '</button></form>' +
      '<p class="mmsub-done" role="status">' + esc(COPY.done) + '</p>';
  }

  function embed(pub) {
    return '<iframe class="mmsub-embed" src="' + pub.url + '/embed" title="Subscribe to ' +
      esc(pub.name) + '" loading="lazy" scrolling="no"></iframe>';
  }

  function fine(key, notes) {
    var other = key === "art" ? PUBS.tv : PUBS.art;
    var otherTxt = key === "art" ? COPY.alsoTv : COPY.alsoArt;
    return '<p class="mmsub-fine"><span>' + esc(COPY.fine) + '</span>' +
      '<a href="' + other.url + '?utm_source=magickmica.github.io&utm_medium=site" target="_blank" rel="noopener">' +
      esc(otherTxt) + '</a>' + (notes ? notesLink() : '') + '</p>';
  }

  function notesLink() {
    return '<a href="' + COPY.notesUrl + '" target="_blank" rel="noopener">' + esc(COPY.notes) + '</a>';
  }

  function paint(box, t) {
    box.style.setProperty("--mmsub-a", t.a);
    box.style.setProperty("--mmsub-b", t.b);
    box.style.setProperty("--mmsub-glow", t.glow);
    box.style.setProperty("--mmsub-ink", t.ink);
    box.style.setProperty("--mmsub-bg", t.bg);
  }

  function wire(box) {
    var f = box.querySelector("form");
    if (f) f.addEventListener("submit", function () {
      // let the GET go through to Substack in a new tab; just show the hint here
      box.classList.add("sent");
      store(STORE_DONE, "1");
    });
  }

  function render(el) {
    if (el.getAttribute("data-mmsub-done")) return;
    el.setAttribute("data-mmsub-done", "1");
    var variant = el.getAttribute("data-mm-subscribe");
    if (variant !== "compact" && variant !== "banner") variant = "full";
    var key = el.getAttribute("data-pub") === "art" ? "art" : "tv";
    var pub = PUBS[key];
    var useEmbed = el.getAttribute("data-mode") === "embed";
    var box = document.createElement("section");
    box.setAttribute("aria-label", "Subscribe to " + pub.name);

    if (variant === "banner") {
      var name = el.getAttribute("data-theme") || "signal";
      var t = THEMES[name] || THEMES.signal;
      var o = function (k) { return el.getAttribute("data-" + k) || t[k]; };
      box.className = "mmsub mmsub-banner mmsub-t-" + name;
      paint(box, t);
      box.innerHTML =
        '<div class="mmsub-art" aria-hidden="true">' + esc(o("art")) + '</div>' +
        '<div class="mmsub-copy"><p class="mmsub-lab">' + esc(o("eyebrow")) + '</p>' +
        '<h2 class="mmsub-ttl">' + esc(o("title")) + '</h2>' +
        '<p class="mmsub-lede">' + esc(o("sub")) + '</p></div>' +
        '<div class="mmsub-act">' + (useEmbed ? embed(pub) : form(pub, "banner-" + name, o("button"))) + fine(key, t.notes) + '</div>';
      var wrap = document.createElement("div");
      wrap.className = "mmsub-wrap";
      wrap.appendChild(box);
      el.innerHTML = "";
      el.appendChild(wrap);
      wire(box);
      return;
    }

    var action = useEmbed ? embed(pub) : form(pub, variant);
    if (variant === "full") {
      var perks = COPY.perks.map(function (p) {
        return '<li><span class="ic" aria-hidden="true">' + p[0] + '</span><span>' + esc(p[1]) + '</span></li>';
      }).join("");
      box.className = "mmsub mmsub-full";
      box.innerHTML =
        '<div class="mmsub-orb" aria-hidden="true"></div>' +
        '<div><p class="mmsub-lab">' + esc(COPY.label) + '</p>' +
        '<h2 class="mmsub-ttl">' + esc(COPY.title) + '</h2>' +
        '<p class="mmsub-lede">' + esc(COPY.lede) + '</p>' +
        '<p class="mmsub-ph">' + esc(COPY.perksHead).toUpperCase() + '</p>' +
        '<ul class="mmsub-perks">' + perks + '</ul></div>' +
        '<div class="mmsub-side"><p class="mmsub-cta">Tune in to ' + esc(pub.name) + '</p>' +
        action + fine(key) + '</div>';
    } else {
      box.className = "mmsub mmsub-compact";
      box.innerHTML =
        '<div class="mmsub-copy"><p class="mmsub-lab" style="margin-bottom:6px">' + esc(COPY.label) + '</p>' +
        '<h2 class="mmsub-ttl">' + esc(COPY.compactTitle) + '</h2>' +
        '<p class="mmsub-lede">' + esc(COPY.compactSub) + '</p></div>' +
        '<div class="mmsub-act">' + action + fine(key) + '</div>';
    }

    el.innerHTML = "";
    el.appendChild(box);

    if (variant === "compact") {
      var fit = function () { box.classList.toggle("narrow", box.clientWidth < 520); };
      fit();
      if (window.ResizeObserver) new ResizeObserver(fit).observe(box);
    }
    wire(box);
  }

  /* ---------- moving a box up into the page ---------- */
  function placeInGrid(el) {
    var grid = document.querySelector(el.getAttribute("data-after"));
    if (!grid) return;
    var rows = parseInt(el.getAttribute("data-rows"), 10) || 2;
    var items = [].filter.call(grid.children, function (k) {
      return k !== el && !k.hasAttribute("data-mm-subscribe") && !k.classList.contains("mms-wrap") &&
        k.offsetParent !== null && k.offsetHeight > 0;
    });
    var cols = 1;
    if (items.length) {
      var top0 = items[0].offsetTop, left0 = items[0].offsetLeft;
      cols = items.filter(function (k) { return k.offsetTop === top0; }).length || 1;
      // CSS columns (masonry) stack down, not across: count the columns instead
      if (cols === 1 && items.length > 1 && items[1].offsetLeft !== left0)
        cols = items.filter(function (k) { return k.offsetLeft !== left0; }).length ? 2 : 1;
    }
    var min = parseInt(el.getAttribute("data-min"), 10);
    var after = Math.max(cols * rows, isNaN(min) ? 4 : min);
    var mark = el.__mmsubMark;
    if (items.length > after) {
      if (el.parentNode === grid && el.nextElementSibling === items[after]) return;
      el.classList.add("mmsub-ingrid");
      el.__mmsubMoving = true;
      grid.insertBefore(el, items[after]);
      el.__mmsubMoving = false;
    } else if (mark && mark.parentNode && el.previousSibling !== mark) {
      el.classList.remove("mmsub-ingrid");
      el.__mmsubMoving = true;
      mark.parentNode.insertBefore(el, mark.nextSibling);
      el.__mmsubMoving = false;
    }
  }

  function setupPlace(el) {
    if (!el.getAttribute("data-after")) return;
    el.__mmsubMark = document.createComment(" subscribe box home ");
    el.parentNode.insertBefore(el.__mmsubMark, el);
    var t = null;
    var later = function () { clearTimeout(t); t = setTimeout(function () { placeInGrid(el); }, 60); };
    placeInGrid(el);
    window.addEventListener("load", later);
    window.addEventListener("resize", later);
    var grid = document.querySelector(el.getAttribute("data-after"));
    if (grid && window.MutationObserver) {
      new MutationObserver(function () { if (!el.__mmsubMoving) later(); })
        .observe(grid, { childList: true });
    }
  }

  /* ---------- after-game prompt ---------- */
  var popTimer = null;

  function promptAllowed() {
    if (document.body && document.body.hasAttribute("data-no-subscribe-prompt")) return false;
    if (store(STORE_DONE) === "1") return false;
    if (+store(STORE_SNOOZE) > Date.now()) return false;
    try { if (sessionStorage.getItem(SESSION_SHOWN)) return false; } catch (e) {}
    return !document.querySelector(".mmsub-pop");
  }

  function showPrompt() {
    if (!promptAllowed()) return;
    try { sessionStorage.setItem(SESSION_SHOWN, "1"); } catch (e) {}
    var pub = PUBS.tv;
    var box = document.createElement("section");
    box.className = "mmsub mmsub-pop";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-label", "Subscribe to " + pub.name);
    paint(box, THEMES.circus);
    box.innerHTML =
      '<button type="button" class="mmsub-x" aria-label="Close">✕</button>' +
      '<p class="mmsub-lab">' + esc(GAME.eyebrow) + '</p>' +
      '<h2 class="mmsub-ttl">' + esc(GAME.title) + '</h2>' +
      '<p class="mmsub-lede">' + esc(GAME.sub) + '</p>' +
      form(pub, "after-game", GAME.button) +
      '<p class="mmsub-fine">' + notesLink() + '</p>' +
      '<button type="button" class="mmsub-later">' + esc(GAME.later) + '</button>';
    document.body.appendChild(box);
    requestAnimationFrame(function () { requestAnimationFrame(function () { box.classList.add("on"); }); });
    var onKey = function (e) { if (e.key === "Escape") close(false); };
    var close = function (snooze) {
      if (snooze) store(STORE_SNOOZE, String(Date.now() + 7 * 864e5));
      document.removeEventListener("keydown", onKey);
      box.classList.remove("on");
      setTimeout(function () { if (box.parentNode) box.parentNode.removeChild(box); }, 450);
    };
    document.addEventListener("keydown", onKey);
    box.querySelector(".mmsub-x").addEventListener("click", function () { close(false); });
    box.querySelector(".mmsub-later").addEventListener("click", function () { close(true); });
    box.querySelector("form").addEventListener("submit", function () {
      box.classList.add("sent");
      store(STORE_DONE, "1");
      setTimeout(function () { close(false); }, 6000);
    });
  }

  function onRoundPaid(game) {
    if (/daily|trade|booth/i.test(String(game || ""))) return;   // visit prizes and swaps are not a round
    if (popTimer || !promptAllowed()) return;
    popTimer = setTimeout(showPrompt, 2200);                      // let the win animation play first
  }

  function hookPrizes(tries) {
    var P = window.MMPrizes;
    if (!P) { if (tries < 20) setTimeout(function () { hookPrizes(tries + 1); }, 500); return; }
    if (P.__mmsub) return;
    P.__mmsub = true;
    ["addTickets", "add"].forEach(function (fn) {
      var orig = P[fn];
      if (typeof orig !== "function") return;
      P[fn] = function (a, game) {
        var r = orig.apply(this, arguments);
        try { onRoundPaid(game); } catch (e) {}
        return r;
      };
    });
  }

  function init() {
    if (!document.getElementById("mmsub-css")) {
      var st = document.createElement("style");
      st.id = "mmsub-css";
      st.textContent = CSS;
      document.head.appendChild(st);
    }
    var els = document.querySelectorAll("[data-mm-subscribe]");
    for (var i = 0; i < els.length; i++) { render(els[i]); setupPlace(els[i]); }
    hookPrizes(0);
  }

  window.MMSubscribe = { prompt: showPrompt, themes: THEMES };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
