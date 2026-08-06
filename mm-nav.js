/* ============================================================
   MAGICKMICA · SHARED NAVIGATION
   ------------------------------------------------------------
   Drop one line into any page, just before </body>:
       <script src="mm-nav.js" defer></script>

   Injects a sticky top bar plus a full directory drawer, so every
   page reaches every other page. Edit the LINKS map below once and
   the whole site updates.

   Self-contained: no dependencies, all class names prefixed .mm-
   so it cannot collide with a page's own styles. Sticky rather than
   fixed, so it never needs body padding on pages that already have
   their own header.
   ============================================================ */
(function () {
  'use strict';

  var SECTIONS = [
    { name: 'Read', items: [
      ['notes.html', 'Notes'],
      ['articles.html', 'Magazine'],
      ['blog.html', 'Blog'],
      ['archive.html', 'Archive'],
      ['newsstand.html', 'Newsstand'],
      ['minimags.html', 'Y3K Magazine'],
      ['random-note.html', 'Random Note']
    ]},
    { name: 'Play', items: [
      ['arcade.html', 'Arcade'],
      ['songmaker.html', 'Song Maker'],
      ['daily-sigil.html', 'Daily Sigil'],
      ['haunted-house.html', 'The Hollow House'],
      ['stardust.html', 'Stardust Foundry'],
      ['cosmic-echo.html', 'Cosmic Echo'],
      ['moon-shot.html', 'Moon Shot'],
      ['blender.html', 'The Astral Blender'],
      ['sunrise.html', 'Win the Morning'],
      ['cosmic-phone.html', 'The Cosmic Phone'],
      ['transmissions.html', 'Transmissions'],
      ['quest.html', 'Dream Quest'],
      ['dream-journal.html', 'Dream Journal'],
      ['affirmations.html', 'Daily Affirmation'],
      ['https://magickmica.github.io/oracle', 'Oracle'],
      ['https://magickmica.github.io/musicbox/', 'Music Box']
    ]},
    { name: '\u2726 Signs', items: [
      ['abundance-portal-one.html', 'The Portal'],
      ['abundance-notebook.html', 'The Notebook'],
      ['abundance-scratch.html', 'Scratch a Sign'],
      ['abundance-globe.html', 'The Globe'],
      ['abundance-oracle.html', 'The Oracle'],
      ['affirmations-100.html', 'Fortune Machine']
    ]},
    { name: '\uD83D\uDC8E Crystal Vaults', items: [
      ['herkimer-vault.html', 'Herkimer Vault'],
      ['labradorite-vault.html', 'Labradorite Vault'],
      ['opal-vault.html', 'Opal Vault'],
      ['quartz-vault.html', 'Quartz Vault'],
      ['watermelon-vault.html', 'Watermelon Vault'],
      ['quartz-amulets.html', 'Quartz Amulets'],
      ['copper-jewelry.html', 'Copper Jewelry']
    ]},
    { name: '\uD83D\uDEF8 Beyond the Signal', items: [
      ['https://substack.com/@magickmica', 'Substack'],
      ['https://ko-fi.com/magickmica/tiers', 'Ko-fi Memberships'],
      ['https://www.themysticalspiralstore.com/', 'Mystical Spiral']
    ]}
  ];

  // shown inline on wide screens; everything else lives in the drawer
  var PRIMARY = [
    ['index.html', 'Home'],
    ['notes.html', 'Notes'],
    ['articles.html', 'Magazine'],
    ['arcade.html', 'Arcade'],
    ['songmaker.html', 'Songs']
  ];

  var CSS = ''
    + '.mm-bar{position:sticky;top:0;z-index:9000;display:flex;align-items:center;gap:10px;'
    +   'padding:9px 14px;background:rgba(7,6,14,.93);backdrop-filter:blur(9px);'
    +   '-webkit-backdrop-filter:blur(9px);border-bottom:1px solid rgba(255,68,204,.28);'
    +   'font-family:"IBM Plex Mono",ui-monospace,monospace;}'
    + '.mm-brand{font-family:"Orbitron","IBM Plex Mono",monospace;font-weight:700;font-size:12px;'
    +   'letter-spacing:.14em;text-decoration:none;color:transparent;white-space:nowrap;'
    +   'background:linear-gradient(96deg,#a020f0,#ff44cc 30%,#ffd166 60%,#22e0ff);'
    +   '-webkit-background-clip:text;background-clip:text;}'
    + '.mm-links{display:none;gap:4px;flex:1;min-width:0;}'
    + '.mm-links a{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#b8b0d4;'
    +   'text-decoration:none;padding:8px 10px;border-radius:999px;white-space:nowrap;}'
    + '.mm-links a:hover{color:#ffd166;background:rgba(255,209,102,.1);}'
    + '.mm-links a[aria-current="page"]{color:#ffd166;background:rgba(255,209,102,.14);}'
    + '.mm-spacer{flex:1}'
    + '.mm-menu{margin-left:auto;display:inline-flex;align-items:center;gap:7px;cursor:pointer;'
    +   'font-family:inherit;font-size:11px;letter-spacing:.14em;text-transform:uppercase;'
    +   'color:#07060e;background:linear-gradient(96deg,#ffd166,#ffe9b5 55%,#ffd166);'
    +   'border:0;border-radius:999px;padding:9px 15px;min-height:38px;}'
    + '.mm-menu:hover{box-shadow:0 0 18px rgba(255,209,102,.45)}'
    + '.mm-menu b{display:grid;gap:3px}'
    + '.mm-menu i{display:block;width:13px;height:2px;background:#07060e;border-radius:2px}'
    + '.mm-drawer{position:fixed;inset:0;z-index:9500;display:none;}'
    + '.mm-drawer[data-open="true"]{display:block}'
    + '.mm-scrim{position:absolute;inset:0;background:rgba(4,3,10,.82);'
    +   'backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);}'
    + '.mm-sheet{position:absolute;top:0;right:0;bottom:0;width:min(400px,88vw);'
    +   'background:#0b0818;border-left:1px solid rgba(255,68,204,.3);'
    +   'overflow-y:auto;-webkit-overflow-scrolling:touch;padding:16px 18px 40px;'
    +   'box-shadow:-14px 0 44px rgba(0,0,0,.6);}'
    + '.mm-sheet-top{display:flex;align-items:center;justify-content:space-between;'
    +   'margin-bottom:14px;position:sticky;top:0;background:#0b0818;padding:4px 0 10px;}'
    + '.mm-close{background:transparent;border:1px solid rgba(184,176,212,.34);color:#b8b0d4;'
    +   'border-radius:999px;width:40px;height:40px;font-size:17px;cursor:pointer;line-height:1;}'
    + '.mm-close:hover{border-color:#ffd166;color:#ffd166}'
    + '.mm-sec{margin:0 0 18px}'
    + '.mm-sec h3{margin:0 0 7px;font-size:10px;letter-spacing:.28em;text-transform:uppercase;'
    +   'color:#6f6890;font-weight:500;font-family:inherit;}'
    + '.mm-sec a{display:block;padding:11px 12px;margin:0 -12px;border-radius:9px;'
    +   'font-size:14px;color:#d9d2ee;text-decoration:none;font-family:inherit;}'
    + '.mm-sec a:hover{background:rgba(255,68,204,.13);color:#fff}'
    + '.mm-sec a[aria-current="page"]{color:#ffd166;background:rgba(255,209,102,.12)}'
    + '@media(min-width:900px){.mm-links{display:flex}.mm-spacer{display:none}}'
    + '@media(prefers-reduced-motion:reduce){.mm-bar{backdrop-filter:none}}';

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text) e.textContent = text;
    return e;
  }

  var here = (location.pathname.split('/').pop() || 'index.html').toLowerCase();

  function link(href, label) {
    var a = el('a', null, label);
    a.href = href;
    if (href.toLowerCase() === here) a.setAttribute('aria-current', 'page');
    if (/^https?:/.test(href) && href.indexOf('magickmica.github.io') === -1) {
      a.target = '_blank';
      a.rel = 'noopener';
      a.textContent = label + ' \u2197';
    }
    return a;
  }

  function build() {
    if (document.querySelector('.mm-bar')) return;   // never inject twice

    var style = el('style');
    style.textContent = CSS;
    document.head.appendChild(style);

    /* ---------------- bar ---------------- */
    var bar = el('nav', 'mm-bar');
    bar.setAttribute('aria-label', 'Site');

    var brand = el('a', 'mm-brand', '\u2726 MAGICKMICA');
    brand.href = 'index.html';
    bar.appendChild(brand);

    var links = el('div', 'mm-links');
    PRIMARY.forEach(function (p) { links.appendChild(link(p[0], p[1])); });
    bar.appendChild(links);
    bar.appendChild(el('div', 'mm-spacer'));

    var btn = el('button', 'mm-menu');
    btn.type = 'button';
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', 'mm-drawer');
    var bars = el('b');
    bars.appendChild(el('i')); bars.appendChild(el('i')); bars.appendChild(el('i'));
    btn.appendChild(bars);
    btn.appendChild(document.createTextNode('Menu'));
    bar.appendChild(btn);

    /* ---------------- drawer ---------------- */
    var drawer = el('div', 'mm-drawer');
    drawer.id = 'mm-drawer';
    drawer.setAttribute('data-open', 'false');

    var scrim = el('div', 'mm-scrim');
    var sheet = el('div', 'mm-sheet');
    sheet.setAttribute('role', 'dialog');
    sheet.setAttribute('aria-modal', 'true');
    sheet.setAttribute('aria-label', 'Site directory');

    var top = el('div', 'mm-sheet-top');
    var title = el('span', 'mm-brand', '\u2726 EVERYTHING');
    var close = el('button', 'mm-close', '\u2715');
    close.type = 'button';
    close.setAttribute('aria-label', 'Close menu');
    top.appendChild(title); top.appendChild(close);
    sheet.appendChild(top);

    var home = el('div', 'mm-sec');
    home.appendChild(link('index.html', 'Home'));
    sheet.appendChild(home);

    SECTIONS.forEach(function (sec) {
      var box = el('div', 'mm-sec');
      box.appendChild(el('h3', null, sec.name));
      sec.items.forEach(function (it) { box.appendChild(link(it[0], it[1])); });
      sheet.appendChild(box);
    });

    drawer.appendChild(scrim);
    drawer.appendChild(sheet);

    document.body.insertBefore(bar, document.body.firstChild);
    document.body.appendChild(drawer);

    /* ---------------- behaviour ---------------- */
    var lastFocus = null;

    function open() {
      lastFocus = document.activeElement;
      drawer.setAttribute('data-open', 'true');
      btn.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
      close.focus();
    }
    function shut() {
      drawer.setAttribute('data-open', 'false');
      btn.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    btn.addEventListener('click', open);
    close.addEventListener('click', shut);
    scrim.addEventListener('click', shut);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.getAttribute('data-open') === 'true') shut();
    });
    // keep focus inside the sheet while it is open
    sheet.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab') return;
      var f = sheet.querySelectorAll('a[href],button');
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
