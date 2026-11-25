/* ============================================================
   MAGICK MICA · CRYSTAL HUNT + TODAY'S GEODE
   ------------------------------------------------------------
   Two small games that show the shop's crystals inside the site
   instead of in an ad strip.

   CRYSTAL HUNT  One glinting shard hides somewhere on the page.
                 It moves every day. Tap it and it turns into a
                 real stone from the shop, which goes into the
                 visitor's Crystal Pouch. Seven finds fill the
                 pouch and pay 50 circus tickets.

   TODAY'S GEODE Tap it three times and it cracks open to show the
                 stone of the day. One geode a day, +5 tickets.
                 Drawn into any element with data-mm-geode, or,
                 when the script tag carries data-geode, placed
                 automatically before the shop strip / footer.

   Use:  <script src="crystal-hunt.js?v=1" defer></script>
         <script src="crystal-hunt.js?v=1" data-geode defer></script>
   Pages outside the root (explore/) use ../crystal-hunt.js; the
   script finds products.js next to itself if the page has not
   loaded it. Saved only in the visitor's browser (localStorage).
   Tickets go into the same jar as the arcade (mm_tickets_v1).
   ============================================================ */
(function () {
  'use strict';
  var me = document.currentScript;
  var ROOT = me && me.src ? me.src.replace(/[^/]*$/, '') : '';
  var AUTO_GEODE = !!(me && me.hasAttribute('data-geode'));
  var STORE = 'https://www.themysticalspiralstore.com/product-page/';
  var HUNT = 'mm_crystal_hunt_v1', GEO = 'mm_geode_v1', TIX = 'mm_tickets_v1', SLOTS = 7;
  var IMG = function (f, w, h) {
    return 'https://static.wixstatic.com/media/' + f + '/v1/fill/w_' + w + ',h_' + h + ',al_c,q_80,enc_auto/file.jpg';
  };

  function get(k, d) { try { var v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } }
  function put(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
  function today() { var d = new Date(); return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate(); }
  function hash(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function rng(seed) { var a = hash(seed); return function () { a = (a + 0x6D2B79F5) | 0; var t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  var PAGE = location.pathname.replace(/index\.html$/, '') || '/';

  function addTickets(n, why) {
    if (window.MMPrizes && MMPrizes.addTickets) { MMPrizes.addTickets(n, why); return; }
    put(TIX, Math.min(99999, (+get(TIX, 0) || 0) + n));
    try { window.dispatchEvent(new CustomEvent('mm-prizes')); } catch (e) {}
  }

  /* ---------- styles ---------- */
  var CSS = ''
    + '.mmch-shard{position:absolute;z-index:40;width:24px;height:30px;padding:0;border:0;background:none;cursor:pointer;'
    +   'animation:mmch-glint 2.8s ease-in-out infinite;-webkit-tap-highlight-color:transparent}'
    + '.mmch-shard::before{content:"";position:absolute;inset:-10px}' /* bigger tap target, same tiny look */
    + '.mmch-shard svg{width:100%;height:100%;display:block;filter:drop-shadow(0 0 5px rgba(177,125,255,.95)) drop-shadow(0 0 12px rgba(70,229,200,.5))}'
    + '@keyframes mmch-glint{0%,100%{opacity:.5;transform:rotate(-10deg) scale(.9)}45%{opacity:1;transform:rotate(8deg) scale(1.1)}55%{opacity:1;transform:rotate(8deg) scale(1.1)}}'
    + '.mmch-burst{position:fixed;z-index:9601;pointer-events:none;width:8px;height:8px;border-radius:50%;'
    +   'background:#fff;box-shadow:0 0 10px #b17dff;animation:mmch-burst .7s ease-out forwards}'
    + '@keyframes mmch-burst{to{transform:translate(var(--dx),var(--dy)) scale(.2);opacity:0}}'
    + '.mmch-sheet{position:fixed;left:50%;bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:9600;width:min(380px,calc(100vw - 24px));'
    +   'transform:translate(-50%,140%);transition:transform .5s cubic-bezier(.2,1.35,.4,1);'
    +   'background:#0d0b22;color:#ece9ff;border:1px solid rgba(180,170,255,.34);border-radius:18px;padding:14px;'
    +   'box-shadow:0 18px 60px rgba(0,0,0,.6),0 0 0 1px rgba(255,255,255,.03) inset;font:15px/1.45 "Space Grotesk",system-ui,sans-serif}'
    + '.mmch-sheet.show{transform:translate(-50%,0)}'
    + '.mmch-sheet h4{margin:0 34px 10px 0;font:600 1.02rem/1.2 Fraunces,Georgia,serif;color:#ece9ff}'
    + '.mmch-x{position:absolute;top:6px;right:6px;width:36px;height:36px;border:0;background:none;color:#a39ed0;font-size:22px;cursor:pointer;border-radius:50%}'
    + '.mmch-stone{display:flex;gap:12px;align-items:center;text-decoration:none;color:inherit}'
    + '.mmch-stone img{width:76px;height:95px;object-fit:cover;border-radius:10px;flex:none;background:#05040c}'
    + '.mmch-stone b{display:block;font-weight:500;font-size:.95rem;line-height:1.25}'
    + '.mmch-pr{margin-top:4px;white-space:nowrap}.mmch-pr s{color:#8d88b8;margin-left:6px;font-size:.85em}'
    + '.mmch-pr i{font-style:normal;color:#ff6fae;font-weight:700;margin-left:6px;font-size:.85em}'
    + '.mmch-go{display:inline-block;margin-top:6px;font-weight:700;color:#46e5c8;font-size:.9rem}'
    + '.mmch-slots{display:flex;gap:6px;align-items:center;margin-top:12px;font-size:.85rem;color:#a39ed0}'
    + '.mmch-slots span{width:12px;height:15px;clip-path:polygon(50% 0,100% 30%,80% 100%,20% 100%,0 30%);background:rgba(180,170,255,.22)}'
    + '.mmch-slots span.on{background:linear-gradient(#46e5c8,#b17dff)}.mmch-slots em{font-style:normal;margin-left:4px}'
    + '.mmch-list{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;max-height:50vh;overflow:auto}'
    + '.mmch-list a{display:block;border-radius:10px;overflow:hidden;aspect-ratio:4/5;background:#05040c}'
    + '.mmch-list img{width:100%;height:100%;object-fit:cover;display:block}'
    + '.mmch-pouch{position:fixed;left:14px;bottom:calc(14px + env(safe-area-inset-bottom,0px));z-index:9400;width:46px;height:46px;border-radius:50%;'
    +   'border:1px solid rgba(180,170,255,.4);background:#0d0b22;color:#ece9ff;cursor:pointer;padding:0;'
    +   'box-shadow:0 6px 20px rgba(0,0,0,.45),0 0 14px rgba(177,125,255,.35);display:grid;place-items:center}'
    + '.mmch-pouch svg{width:20px;height:25px}'
    + '.mmch-pouch b{position:absolute;right:-4px;top:-4px;min-width:20px;height:20px;border-radius:10px;background:#ff6fae;color:#08071a;'
    +   'font:700 11px/20px "Space Grotesk",system-ui,sans-serif;text-align:center;padding:0 5px}'
    /* the geode */
    + '.mmch-geode{position:relative;overflow:hidden;max-width:640px;margin:40px auto;padding:26px 22px;border-radius:22px;text-align:center;'
    +   'background:radial-gradient(70% 60% at 50% 30%,rgba(177,125,255,.16),transparent 70%),#0c0a20;'
    +   'border:1px solid rgba(180,170,255,.26);color:#ece9ff;font:15px/1.5 "Space Grotesk",system-ui,sans-serif}'
    + '.mmch-geode h3{margin:0;font:300 1.7rem/1.1 Fraunces,Georgia,serif;letter-spacing:-.01em;color:#ece9ff}'
    + '.mmch-geode h3 em{font-style:italic;font-weight:400}'
    + '.mmch-geode p{margin:6px auto 0;color:#a39ed0;max-width:44ch}'
    + '.mmch-rock{display:block;margin:14px auto 4px;width:min(240px,64vw);aspect-ratio:1;border:0;background:none;padding:0;cursor:pointer;-webkit-tap-highlight-color:transparent}'
    + '.mmch-rock svg{width:100%;height:100%;overflow:visible}'
    + '.mmch-rock.shake{animation:mmch-shake .32s}'
    + '@keyframes mmch-shake{25%{transform:rotate(-5deg)}75%{transform:rotate(5deg)}}'
    + '.mmch-crack{opacity:0;transition:opacity .2s}.mmch-crack.on{opacity:1}'
    + '.mmch-half{transition:transform .8s cubic-bezier(.3,1.25,.5,1);transform-box:fill-box}'
    + '.mmch-l{transform-origin:100% 100%}.mmch-r{transform-origin:0 100%}'
    + '.open .mmch-l{transform:translate(-28px,4px) rotate(-32deg)}.open .mmch-r{transform:translate(28px,4px) rotate(32deg)}'
    + '.mmch-in{opacity:0;transition:opacity .5s .25s}.open .mmch-in{opacity:1}.open .mmch-crack{opacity:0}'
    + '.mmch-hint{font-size:.92rem;color:#a39ed0;min-height:1.5em}'
    + '.mmch-geode .mmch-stone{max-width:420px;margin:12px auto 0;text-align:left;padding:12px;border-radius:14px;border:1px solid rgba(180,170,255,.22);background:rgba(255,255,255,.03)}'
    + '@media (prefers-reduced-motion:reduce){.mmch-shard,.mmch-rock.shake,.mmch-burst{animation:none}.mmch-sheet,.mmch-half,.mmch-in{transition:none}}';

  function gem(a, b) {
    return '<svg viewBox="0 0 64 80" aria-hidden="true"><defs><linearGradient id="mmchg' + a.slice(1) + '" x1="0" y1="0" x2="1" y2="1">'
      + '<stop offset="0" stop-color="' + a + '"/><stop offset="1" stop-color="' + b + '"/></linearGradient></defs>'
      + '<polygon points="32,2 56,26 46,76 18,76 8,26" fill="url(#mmchg' + a.slice(1) + ')"/>'
      + '<polygon points="32,2 56,26 32,32 8,26" fill="#fff" opacity=".45"/>'
      + '<polygon points="32,32 46,76 18,76" fill="#000" opacity=".15"/></svg>';
  }
  function price(p) {
    return '<div class="mmch-pr">$' + p.price.toFixed(2)
      + (p.was ? '<s>$' + p.was.toFixed(2) + '</s><i>' + Math.round((p.was - p.price) / p.was * 100) + '% off</i>' : '') + '</div>';
  }
  function stoneHTML(p) {
    return '<a class="mmch-stone" href="' + STORE + encodeURIComponent(p.slug) + '" target="_blank" rel="noopener">'
      + '<img src="' + IMG(p.img, 240, 300) + '" alt="" loading="lazy" onerror="this.style.visibility=\'hidden\'">'
      + '<span><b>' + esc(p.name) + '</b>' + price(p) + '<span class="mmch-go">See it on the store →</span></span></a>';
  }

  /* ---------- the sheet (one, reused) ---------- */
  var sheet, sheetTimer;
  function openSheet(html, ms) {
    if (!sheet) {
      sheet = document.createElement('div'); sheet.className = 'mmch-sheet'; sheet.setAttribute('role', 'dialog'); sheet.setAttribute('aria-live', 'polite');
      document.body.appendChild(sheet);
      sheet.addEventListener('click', function (e) { if (e.target.closest('.mmch-x')) closeSheet(); });
      sheet.addEventListener('mouseenter', function () { clearTimeout(sheetTimer); });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeSheet(); });
    }
    clearTimeout(sheetTimer);
    sheet.innerHTML = '<button class="mmch-x" aria-label="Close">×</button>' + html;
    requestAnimationFrame(function () { sheet.classList.add('show'); });
    if (ms) sheetTimer = setTimeout(closeSheet, ms);
  }
  function closeSheet() { if (sheet) sheet.classList.remove('show'); }

  function slots(n) {
    var s = ''; for (var i = 0; i < SLOTS; i++) s += '<span class="' + (i < n ? 'on' : '') + '"></span>';
    return '<div class="mmch-slots">' + s + '<em>' + n + ' of ' + SLOTS + ' in your Crystal Pouch</em></div>';
  }

  /* ---------- the pouch button ---------- */
  var pouchBtn;
  function drawPouch(state) {
    var n = state.pouch.length;
    if (!n) { if (pouchBtn) pouchBtn.hidden = true; return; }
    if (!pouchBtn) {
      pouchBtn = document.createElement('button'); pouchBtn.className = 'mmch-pouch';
      pouchBtn.addEventListener('click', function () {
        var st = load(), byS = {};
        LIVE.concat(ALL).forEach(function (p) { byS[p.slug] = p; });
        openSheet('<h4>Your Crystal Pouch</h4><div class="mmch-list">' + st.pouch.map(function (f) {
          var p = byS[f.s]; if (!p) return '';
          return '<a href="' + STORE + encodeURIComponent(p.slug) + '" target="_blank" rel="noopener" title="' + esc(p.name) + '">'
            + '<img src="' + IMG(p.img, 160, 200) + '" alt="' + esc(p.name) + '" loading="lazy"></a>';
        }).join('') + '</div>' + slots(st.pouch.length)
          + '<div class="mmch-slots" style="margin-top:6px">A new shard hides on every page each day. Fill the pouch for 50 tickets.</div>');
      });
      document.body.appendChild(pouchBtn);
    }
    pouchBtn.hidden = false;
    pouchBtn.setAttribute('aria-label', 'Crystal Pouch, ' + n + ' of ' + SLOTS + ' found');
    pouchBtn.innerHTML = gem('#46e5c8', '#b17dff') + '<b>' + n + '</b>';
  }

  /* ---------- state ---------- */
  function load() {
    var s = get(HUNT, null);
    if (!s || !Array.isArray(s.pouch)) s = {pouch: [], seen: {}, filled: 0};
    s.seen = s.seen || {};
    var d = today(); // keep only today's "already found here" marks
    Object.keys(s.seen).forEach(function (k) { if (k.split('|')[1] !== d) delete s.seen[k]; });
    return s;
  }

  var ALL = [], LIVE = [];

  /* ---------- the hunt ---------- */
  var SKIP_IN = 'header,nav,footer,.mm-ads,.mm-store,.mm-nav,.mm-drawer,.mmch-geode,.mmch-sheet,form,button,select,input,textarea,[aria-hidden="true"],dialog';
  function candidates() {
    var out = [], min = Math.min(window.innerHeight * 0.6, 500);
    var els = document.querySelectorAll('main article,main section,article,figure,li,div,img,[class*="card"],[class*="tile"],[class*="note"],[class*="issue"]');
    for (var i = 0; i < els.length && out.length < 600; i++) {
      var el = els[i];
      if (el.tagName === 'IMG') el = el.parentElement;
      if (!el || el === document.body || el.closest(SKIP_IN)) continue;
      if (/^(A|SPAN|BUTTON|svg|CANVAS|VIDEO|IFRAME|PICTURE)$/i.test(el.tagName)) continue;
      var r = el.getBoundingClientRect();
      if (r.width < 150 || r.height < 56 || r.width > 1100 || r.height > 900) continue;
      var top = r.top + window.scrollY;
      if (top < min) continue; // below the first screen, so it's a hunt
      var cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'contents' || cs.position === 'fixed' || cs.position === 'sticky') continue;
      out.push(el);
    }
    // prefer things that look like cards (a border or a fill), so the shard
    // can sit on the card's edge instead of on top of words
    var cards = out.filter(function (el) {
      var cs = getComputedStyle(el);
      return parseFloat(cs.borderTopWidth) > 0 || cs.backgroundImage !== 'none' || !/rgba\(0, 0, 0, 0\)|transparent/.test(cs.backgroundColor);
    });
    return cards.length >= 3 ? cards : out;
  }

  function hide(state, tries) {
    var list = candidates();
    if (list.length < 3 && tries < 4) { setTimeout(function () { hide(state, tries + 1); }, 1800); return; }
    if (!list.length) return;
    var r = rng(PAGE + '|' + today());
    var host = list[Math.floor(r() * list.length)];
    if (getComputedStyle(host).position === 'static') host.style.position = 'relative';
    var b = document.createElement('button');
    b.className = 'mmch-shard'; b.type = 'button';
    b.setAttribute('aria-label', 'A hidden crystal shard. Tap to find it');
    b.innerHTML = gem('#ece9ff', '#b17dff');
    var corner = Math.floor(r() * 4);
    // sit on the card's edge, half over the border, so it never covers words;
    // tuck it inside the corner when the card clips its overflow
    var clips = getComputedStyle(host).overflow !== 'visible';
    b.style[corner < 2 ? 'top' : 'bottom'] = clips ? '4px' : '-15px';
    b.style[corner % 2 ? 'left' : 'right'] = (6 + Math.floor(r() * 28)) + '%';
    host.appendChild(b);
    b.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); found(b); }, true);
  }

  function burst(x, y) {
    for (var i = 0; i < 12; i++) {
      var s = document.createElement('i'); s.className = 'mmch-burst';
      var a = i / 12 * Math.PI * 2, d = 40 + Math.random() * 30;
      s.style.left = x + 'px'; s.style.top = y + 'px';
      s.style.setProperty('--dx', Math.cos(a) * d + 'px'); s.style.setProperty('--dy', Math.sin(a) * d + 'px');
      if (i % 3 === 1) s.style.background = '#46e5c8'; else if (i % 3 === 2) s.style.background = '#ff6fae';
      document.body.appendChild(s);
      setTimeout(function (n) { return function () { n.remove(); }; }(s), 800);
    }
  }

  function found(b) {
    var r = b.getBoundingClientRect(); burst(r.left + r.width / 2, r.top + r.height / 2); b.remove();
    var st = load(), have = {};
    st.pouch.forEach(function (f) { have[f.s] = 1; });
    var pool = LIVE.filter(function (p) { return !have[p.slug]; }); if (!pool.length) pool = LIVE;
    var p = pool[Math.floor(Math.random() * pool.length)];
    st.seen[PAGE + '|' + today()] = 1;
    st.pouch.push({s: p.slug, d: today()});
    var full = st.pouch.length >= SLOTS, n = st.pouch.length;
    if (full) { st.filled = (st.filled || 0) + 1; st.pouch = []; }
    put(HUNT, st);
    openSheet('<h4>' + (full ? 'Pouch full! +50 tickets' : 'You found a crystal!') + '</h4>' + stoneHTML(p) + slots(full ? SLOTS : n)
      + (full ? '<div class="mmch-slots">Spend them at the Ticket Booth. Your pouch is empty again for a new hunt.</div>'
              : '<div class="mmch-slots">Another shard hides on a different page.</div>'), 9000);
    if (full) addTickets(50, 'Crystal Hunt');
    drawPouch(st);
  }

  /* ---------- the geode ---------- */
  function stoneOfDay() {
    var deals = LIVE.filter(function (p) { return p.was && (p.was - p.price) / p.was >= 0.2; });
    var pool = deals.length > 12 ? deals : LIVE;
    return pool[Math.floor(rng('geode|' + today())() * pool.length)];
  }
  function geodeSVG(p) {
    var rays = '';
    for (var i = 0; i < 10; i++) {
      var a = i * Math.PI / 5;
      rays += '<polygon points="100,104 ' + (100 + Math.cos(a) * 54).toFixed(1) + ',' + (104 + Math.sin(a) * 62).toFixed(1) + ' '
        + (100 + Math.cos(a + .3) * 54).toFixed(1) + ',' + (104 + Math.sin(a + .3) * 62).toFixed(1) + '" fill="#fff" opacity=".13"/>';
    }
    return '<svg viewBox="0 0 200 200" aria-hidden="true"><defs>'
      + '<radialGradient id="mmchgi" cx=".5" cy=".5" r=".55"><stop offset="0" stop-color="#fff"/><stop offset=".3" stop-color="#ff6fae"/><stop offset=".65" stop-color="#b17dff"/><stop offset="1" stop-color="#2c1f5c"/></radialGradient>'
      + '<clipPath id="mmchgc"><ellipse cx="100" cy="104" rx="40" ry="48"/></clipPath></defs>'
      + '<ellipse cx="100" cy="184" rx="72" ry="9" fill="rgba(0,0,0,.45)"/>'
      + '<g class="mmch-in"><ellipse cx="100" cy="104" rx="56" ry="64" fill="url(#mmchgi)"/>' + rays
      + '<image href="' + IMG(p.img, 200, 240) + '" x="60" y="56" width="80" height="96" preserveAspectRatio="xMidYMid slice" clip-path="url(#mmchgc)"/>'
      + '<ellipse cx="100" cy="104" rx="40" ry="48" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="2"/></g>'
      + '<g class="mmch-half mmch-l"><path d="M100,20 C54,20 24,62 26,108 C28,152 60,180 100,180 L92,152 L106,124 L90,96 L104,70 L94,46 Z" fill="#716c86"/>'
      + '<path d="M98,26 C60,28 36,60 36,98" stroke="#a7a3ba" stroke-width="6" fill="none" opacity=".55" stroke-linecap="round"/>'
      + '<circle cx="58" cy="132" r="4" fill="#5e5a72"/><circle cx="72" cy="58" r="3" fill="#8a86a0"/></g>'
      + '<g class="mmch-half mmch-r"><path d="M100,20 C146,20 176,62 174,108 C172,152 140,180 100,180 L92,152 L106,124 L90,96 L104,70 L94,46 Z" fill="#5a566c"/>'
      + '<circle cx="146" cy="88" r="5" fill="#4d4a5e"/><circle cx="132" cy="150" r="3" fill="#4d4a5e"/></g>'
      + '<path class="mmch-crack mmch-c1" d="M94,46 L104,70 L90,96" stroke="#fff" stroke-width="2.5" fill="none" style="filter:drop-shadow(0 0 4px #b17dff)"/>'
      + '<path class="mmch-crack mmch-c2" d="M90,96 L106,124 L92,152" stroke="#fff" stroke-width="2.5" fill="none" style="filter:drop-shadow(0 0 4px #b17dff)"/></svg>';
  }

  function geode(box) {
    var p = stoneOfDay(); if (!p) return;
    var st = get(GEO, {}), done = st.d === today();
    box.classList.add('mmch-geode');
    box.innerHTML = '<h3>Today’s <em>geode</em></h3>'
      + '<p>Every day a new one turns up. Crack it open to see which stone is hiding inside.</p>'
      + '<button class="mmch-rock" type="button" aria-label="Tap the geode to crack it open">' + geodeSVG(p) + '</button>'
      + '<div class="mmch-hint" aria-live="polite"></div><div class="mmch-out"></div>';
    var rock = box.querySelector('.mmch-rock'), svg = rock.querySelector('svg'),
        hint = box.querySelector('.mmch-hint'), out = box.querySelector('.mmch-out'), taps = 0;
    function reveal(fresh) {
      svg.classList.add('open'); rock.disabled = true; rock.style.cursor = 'default';
      hint.textContent = fresh ? 'Cracked! +5 tickets. A new geode turns up tomorrow.' : 'You cracked today’s geode. A new one turns up tomorrow.';
      out.innerHTML = stoneHTML(p);
    }
    if (done) { reveal(false); return; }
    hint.textContent = 'Tap it three times';
    rock.addEventListener('click', function () {
      if (taps >= 3) return; taps++;
      rock.classList.remove('shake'); void rock.offsetWidth; rock.classList.add('shake');
      if (taps >= 1) svg.querySelector('.mmch-c1').classList.add('on');
      if (taps >= 2) svg.querySelector('.mmch-c2').classList.add('on');
      if (taps < 3) { hint.textContent = taps === 1 ? 'Two more…' : 'One more…'; return; }
      var r = rock.getBoundingClientRect(); burst(r.left + r.width / 2, r.top + r.height / 2);
      put(GEO, {d: today(), s: p.slug});
      addTickets(5, 'Today’s geode');
      reveal(true);
    });
  }

  function placeGeodes() {
    var boxes = [].slice.call(document.querySelectorAll('[data-mm-geode]'));
    if (!boxes.length && AUTO_GEODE) {
      var box = document.createElement('section');
      var nav = document.querySelector('.adjacent-nav'), strip = document.querySelector('.mm-ads'), foot = document.querySelector('footer');
      if (nav) nav.parentNode.insertBefore(box, nav.nextSibling);
      else if (strip) strip.parentNode.insertBefore(box, strip);
      else if (foot) foot.parentNode.insertBefore(box, foot);
      else document.body.appendChild(box);
      boxes = [box];
    }
    boxes.forEach(geode);
  }

  /* ---------- start ---------- */
  function start() {
    ALL = PRODUCTS;
    LIVE = PRODUCTS.filter(function (p) { return !p.soldOut && p.price != null && p.img && p.cat !== 'Readings'; });
    if (!LIVE.length) return;
    var s = document.createElement('style'); s.textContent = CSS; document.head.appendChild(s);
    var st = load(); drawPouch(st);
    placeGeodes();
    if (!st.seen[PAGE + '|' + today()]) {
      if (document.readyState === 'complete') setTimeout(function () { hide(st, 0); }, 1200);
      else window.addEventListener('load', function () { setTimeout(function () { hide(st, 0); }, 1200); });
    }
  }
  function ready() { return typeof PRODUCTS !== 'undefined' && Array.isArray(PRODUCTS) && PRODUCTS.length; }
  function go() {
    if (ready()) { start(); return; }
    var sc = document.createElement('script'); sc.src = ROOT + 'products.js';
    sc.onload = function () { if (ready()) start(); };
    document.head.appendChild(sc);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();
