/* MAGICKMICA - mm-search.js  ·  site-wide search
 *
 * Renders a search box into <div id="mm-search"></div> and searches
 * search-index.json (built by tools/build_search.py) right in the browser.
 * The index is only downloaded the first time someone clicks into the box.
 *
 * Extras: press "/" anywhere to jump to the box, Esc to clear,
 * and links like index.html?q=moon open with results already showing.
 */
(function () {
  'use strict';
  var mount = document.getElementById('mm-search');
  if (!mount) return;

  var INDEX_URL = 'search-index.json';
  var NOTE_URL = 'https://substack.com/@magickmica/note/c-';
  var FIRST = { pages: 6, articles: 6, notes: 12 };
  var MORE = 24;

  /* ---------- styles: uses the page's own colour variables ---------- */
  var css = [
    '#mm-search{margin:0 0 18px;position:relative;scroll-margin-top:72px}',
    '.mms-box{display:flex;align-items:center;gap:10px;border:1px solid color-mix(in srgb,var(--purple,#d06bff) 34%,transparent);',
    'border-radius:14px;padding:4px 6px 4px 14px;background:var(--surface,rgba(255,255,255,.03));transition:border-color .18s ease,box-shadow .18s ease}',
    '.mms-box:focus-within{border-color:color-mix(in srgb,var(--gold,#ffce5c) 60%,transparent);box-shadow:0 0 0 3px color-mix(in srgb,var(--gold,#ffce5c) 14%,transparent)}',
    '.mms-ico{font-family:Silkscreen,monospace;font-size:10px;letter-spacing:.2em;color:var(--gold,#ffce5c);white-space:nowrap}',
    '.mms-in{flex:1;min-width:0;background:transparent;border:0;outline:0;color:var(--ink,#efe6ff);',
    "font:500 15px/1.4 'IBM Plex Mono',ui-monospace,monospace;padding:10px 0}",
    '.mms-in::placeholder{color:#8e85ad}',
    '.mms-in::-webkit-search-cancel-button{display:none}',
    '.mms-x{background:none;border:0;color:#8e85ad;font:16px/1 monospace;padding:8px 10px;cursor:pointer;border-radius:10px}',
    '.mms-x:hover,.mms-x:focus-visible{color:var(--ink,#efe6ff);outline:0;background:rgba(255,255,255,.06)}',
    '.mms-x[hidden]{display:none}',
    '.mms-key{font-family:Silkscreen,monospace;font-size:9px;color:#8e85ad;border:1px solid rgba(255,255,255,.14);border-radius:5px;padding:2px 6px;margin-right:6px}',
    '.mms-status{font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.16em;color:#8e85ad;margin:8px 2px 0;min-height:13px}',
    '.mms-res{margin-top:6px}',
    '.mms-res[hidden]{display:none}',
    '.mms-grp{margin-top:14px}',
    '.mms-gh{display:flex;align-items:baseline;gap:10px;margin:0 0 8px}',
    '.mms-gh h3{margin:0;font-family:Orbitron,monospace;font-size:11px;letter-spacing:.18em;color:var(--cyan,#6fc3ff)}',
    '.mms-gh .r{flex:1;height:1px;background:color-mix(in srgb,var(--purple,#d06bff) 24%,transparent)}',
    '.mms-gh .n{font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.14em;color:#8e85ad}',
    '.mms-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}',
    '.mms-it{display:flex;gap:12px;align-items:flex-start;border:1px solid color-mix(in srgb,var(--purple,#d06bff) 22%,transparent);',
    'border-radius:12px;padding:12px;background:var(--surface,rgba(255,255,255,.03));color:inherit;text-decoration:none;min-width:0}',
    '.mms-it:hover,.mms-it:focus-visible{border-color:color-mix(in srgb,var(--gold,#ffce5c) 55%,transparent);outline:0}',
    '.mms-it img{width:56px;height:56px;object-fit:cover;border-radius:8px;flex:none;background:rgba(255,255,255,.04)}',
    '.mms-tx{min-width:0;flex:1}',
    '.mms-lab{font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.18em;color:#8e85ad;text-transform:uppercase}',
    '.mms-tt{font-size:14px;font-weight:500;margin-top:4px;line-height:1.3;color:#fff;overflow-wrap:anywhere}',
    '.mms-sn{font-size:11.5px;color:#9d94bd;margin-top:4px;line-height:1.5;overflow-wrap:anywhere;',
    'display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}',
    '.mms-wk{display:inline-block;margin-top:6px;font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.14em;color:var(--cyan,#6fc3ff)}',
    '.mms-it mark{background:color-mix(in srgb,var(--gold,#ffce5c) 30%,transparent);color:#fff;border-radius:3px;padding:0 1px}',
    '.mms-more{margin-top:10px;background:none;border:1px dashed color-mix(in srgb,var(--purple,#d06bff) 40%,transparent);color:var(--ink,#efe6ff);',
    'font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.18em;padding:9px 14px;border-radius:10px;cursor:pointer;width:100%}',
    '.mms-more:hover,.mms-more:focus-visible{border-color:var(--gold,#ffce5c);outline:0}',
    '.mms-none{font-size:12.5px;color:#9d94bd;margin-top:12px}',
    '@media(max-width:560px){.mms-list{grid-template-columns:1fr}.mms-key{display:none}.mms-in{font-size:16px}}'
  ].join('');
  var st = document.createElement('style');
  st.textContent = css;
  document.head.appendChild(st);

  /* ---------- markup ---------- */
  mount.innerHTML =
    '<form class="mms-box" role="search" action="index.html" method="get">' +
    '<label class="mms-ico" for="mms-in">✦ SEARCH</label>' +
    '<input class="mms-in" id="mms-in" name="q" type="search" autocomplete="off" spellcheck="false" ' +
    'placeholder="Notes, articles, games…" aria-describedby="mms-status" aria-controls="mms-res">' +
    '<button class="mms-x" type="button" aria-label="Clear search" hidden>✕</button>' +
    '<span class="mms-key" aria-hidden="true">/</span>' +
    '</form>' +
    '<div class="mms-status" id="mms-status" aria-live="polite"></div>' +
    '<div class="mms-res" id="mms-res" hidden></div>';

  var form = mount.querySelector('form');
  var input = mount.querySelector('.mms-in');
  var clearBtn = mount.querySelector('.mms-x');
  var keyHint = mount.querySelector('.mms-key');
  var statusEl = mount.querySelector('.mms-status');
  var resEl = mount.querySelector('.mms-res');

  /* ---------- loading the index ---------- */
  var DB = null, loading = null;

  function norm(s) {
    s = String(s || '').toLowerCase();
    if (s.normalize) s = s.normalize('NFD').replace(/[̀-ͯ]/g, '');
    return s.replace(/[’‘`]/g, "'").replace(/[“”]/g, '"');
  }

  function load() {
    if (DB) return Promise.resolve(DB);
    if (loading) return loading;
    statusEl.textContent = 'TUNING IN…';
    loading = fetch(INDEX_URL, { cache: 'no-cache' })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) {
        var items = [];
        (d.pages || []).forEach(function (p) {
          items.push({ g: 'pages', url: p[0], title: p[1], lab: p[2], snip: p[3] || p[4], text: p[4],
            T: norm(p[1] + ' ' + p[0].replace(/[-_/.]/g, ' ')), D: norm(p[2] + ' ' + p[3]), X: norm(p[4]), date: '' });
        });
        (d.articles || []).forEach(function (a) {
          items.push({ g: 'articles', url: a[0], title: a[1], lab: (a[4] || 'Article') + ' · ' + fmtDate(a[3]),
            snip: a[2], img: a[5], ext: true, T: norm(a[1]), D: norm(a[2] + ' ' + a[4]), X: '', date: a[3] });
        });
        (d.notes || []).forEach(function (n) {
          var img = n[3] ? (/^https?:/.test(n[3]) ? n[3] : d.img + n[3]) : '';
          items.push({ g: 'notes', url: NOTE_URL + n[0], title: '', lab: 'Note · ' + fmtDate(n[1]), snip: n[2],
            img: img, week: n[4], ext: true, T: '', D: '', X: norm(n[2]), date: n[1] });
        });
        DB = { items: items, counts: { pages: d.pages.length, articles: d.articles.length, notes: d.notes.length } };
        statusEl.textContent = '';
        return DB;
      })
      .catch(function () {
        loading = null;
        statusEl.textContent = 'SIGNAL LOST · COULD NOT LOAD THE SEARCH INDEX';
        throw new Error('index');
      });
    return loading;
  }

  /* ---------- scoring ---------- */
  function terms(q) {
    return norm(q).split(/[^\p{L}\p{N}']+/u).filter(function (t) { return t.length > 0; });
  }

  function wordStart(hay, t) {
    var i = hay.indexOf(t);
    while (i !== -1) {
      if (i === 0 || !/[\p{L}\p{N}]/u.test(hay.charAt(i - 1))) return true;
      i = hay.indexOf(t, i + 1);
    }
    return false;
  }

  function score(it, ts, phrase) {
    var s = 0;
    for (var i = 0; i < ts.length; i++) {
      var t = ts[i], hit = 0;
      if (it.T.indexOf(t) !== -1) hit = wordStart(it.T, t) ? 12 : 6;
      if (it.D.indexOf(t) !== -1) hit = Math.max(hit, wordStart(it.D, t) ? 6 : 3);
      if (it.X.indexOf(t) !== -1) hit = Math.max(hit, wordStart(it.X, t) ? 3 : 1);
      if (!hit) return 0;            // every word has to appear somewhere
      s += hit;
    }
    if (ts.length > 1) {
      if (it.T.indexOf(phrase) !== -1) s += 15;
      else if ((it.D + ' ' + it.X).indexOf(phrase) !== -1) s += 6;
    }
    if (it.T && it.T.indexOf(ts[0]) === 0) s += 4;
    return s;
  }

  function search(q) {
    var ts = terms(q);
    var out = { pages: [], articles: [], notes: [] };
    if (!ts.length) return out;
    var phrase = ts.join(' ');
    DB.items.forEach(function (it) {
      var s = score(it, ts, phrase);
      if (s) out[it.g].push({ it: it, s: s });
    });
    Object.keys(out).forEach(function (g) {
      out[g].sort(function (a, b) {
        return (b.s - a.s) || (b.it.date > a.it.date ? 1 : b.it.date < a.it.date ? -1 : 0);
      });
    });
    out.terms = ts;
    return out;
  }

  /* ---------- rendering ---------- */
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function fmtDate(d) {
    var m = /^(\d{4})-(\d{2})-(\d{2})/.exec(d || '');
    return m ? MONTHS[+m[2] - 1] + ' ' + (+m[3]) + ', ' + m[1] : '';
  }

  function esc(s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function reEsc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

  function mark(text, ts) {
    var safe = esc(text);
    if (!ts.length) return safe;
    var use = ts.filter(function (t) { return t.length > 1 || ts.length === 1; });
    if (!use.length) return safe;
    var re = new RegExp('(' + use.sort(function (a, b) { return b.length - a.length; })
      .map(function (t) { return reEsc(esc(t)); }).join('|') + ')', 'gi');
    return safe.replace(re, '<mark>$1</mark>');
  }

  // Show the part of a long note around the first matching word.
  function around(text, ts) {
    if (!text || text.length < 200) return text;
    var n = norm(text), at = -1;
    for (var i = 0; i < ts.length && at === -1; i++) at = n.indexOf(ts[i]);
    if (at < 90) return text;
    var start = text.lastIndexOf(' ', at - 60);
    return '…' + text.slice(start === -1 ? at - 60 : start + 1);
  }

  var LABEL = { pages: 'PAGES & GAMES', articles: 'ARTICLES', notes: 'NOTES' };
  var shown = {};

  function card(it, ts) {
    var attrs = it.ext ? ' target="_blank" rel="noopener"' : '';
    var img = it.img ? '<img src="' + esc(it.img) + '" alt="" loading="lazy" decoding="async" onerror="this.remove()">' : '';
    var title = it.title ? '<div class="mms-tt">' + mark(it.title, ts) + (it.ext ? ' ↗' : '') + '</div>' : '';
    var snip = it.snip ? '<div class="mms-sn">' + mark(around(it.snip, ts), ts) + '</div>' : '';
    var lab = '<div class="mms-lab">' + esc(it.lab) + (it.g === 'notes' ? ' ↗' : '') + '</div>';
    var html = '<a class="mms-it" href="' + esc(it.url) + '"' + attrs + '>' + img +
      '<div class="mms-tx">' + lab + title + snip + '</div></a>';
    if (it.week) {
      // the on-site weekly issue this note is in, as a second link under the card
      html = '<div>' + html + '<a class="mms-wk" href="' + esc(it.week) + '">IN THIS WEEK’S Y3K ISSUE →</a></div>';
    }
    return html;
  }

  var last = null;
  function render(res) {
    last = res;
    var total = res.pages.length + res.articles.length + res.notes.length;
    if (!total) {
      resEl.hidden = false;
      resEl.innerHTML = '<div class="mms-none">No transmissions match that. Try one word, like “moon” or “alice”.</div>';
      statusEl.textContent = '0 RESULTS';
      return;
    }
    statusEl.textContent = total.toLocaleString() + ' RESULT' + (total === 1 ? '' : 'S');
    var html = '';
    ['pages', 'articles', 'notes'].forEach(function (g) {
      var list = res[g];
      if (!list.length) return;
      var n = shown[g] || FIRST[g];
      html += '<section class="mms-grp"><div class="mms-gh"><h3>' + LABEL[g] + '</h3><div class="r"></div>' +
        '<span class="n">' + list.length.toLocaleString() + '</span></div><div class="mms-list">';
      for (var i = 0; i < Math.min(n, list.length); i++) html += card(list[i].it, res.terms);
      html += '</div>';
      if (list.length > n) {
        html += '<button class="mms-more" type="button" data-g="' + g + '">SHOW ' +
          Math.min(MORE, list.length - n) + ' MORE ' + LABEL[g] + '</button>';
      }
      html += '</section>';
    });
    resEl.innerHTML = html;
    resEl.hidden = false;
  }

  resEl.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.mms-more');
    if (!b || !last) return;
    var g = b.getAttribute('data-g');
    shown[g] = (shown[g] || FIRST[g]) + MORE;
    render(last);
  });

  /* ---------- wiring ---------- */
  var timer = null;
  function run() {
    var q = input.value.trim();
    clearBtn.hidden = !q;
    keyHint.style.display = q ? 'none' : '';
    syncUrl(q);
    if (!q) {
      resEl.hidden = true;
      resEl.innerHTML = '';
      statusEl.textContent = '';
      return;
    }
    shown = {};
    load().then(function () {
      if (input.value.trim() === q) render(search(q));
    }, function () {});
  }

  function syncUrl(q) {
    try {
      var u = new URL(location.href);
      if (q) u.searchParams.set('q', q); else u.searchParams.delete('q');
      history.replaceState(history.state, '', u.pathname + u.search + u.hash);
    } catch (e) { /* file:// previews */ }
  }

  input.addEventListener('focus', function () { load().catch(function () {}); });
  input.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(run, 140);
  });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { input.value = ''; run(); }
  });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    clearTimeout(timer);
    run();
    var first = resEl.querySelector('.mms-it');
    if (first && window.matchMedia('(max-width:560px)').matches) input.blur();
  });
  clearBtn.addEventListener('click', function () { input.value = ''; run(); input.focus(); });

  document.addEventListener('keydown', function (e) {
    if (e.key !== '/' || e.ctrlKey || e.metaKey || e.altKey) return;
    var t = e.target, tag = t && t.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (t && t.isContentEditable)) return;
    e.preventDefault();
    input.focus();
    mount.scrollIntoView({ block: 'start', behavior: 'smooth' });
  });

  // index.html?q=moon opens with results showing
  try {
    var q0 = new URLSearchParams(location.search).get('q');
    if (q0) { input.value = q0; run(); }
  } catch (e) { /* old browsers */ }
})();
