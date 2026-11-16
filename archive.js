/* ============================================================
   MAGICK MICA · ARCHIVE TOOLKIT                    archive.js
   ------------------------------------------------------------
   Shared, data-agnostic helpers for notes.html and minimags.html.
   It holds no archive content: each page hands it the real data
   it already has (the NOTES list, or the issue cards on the page).

   Load with a plain tag before the page's own script:
       <script src="archive.js?v=1"></script>
   Everything lives on window.MMArchive. No dependencies.

   Contents
     dates      local-time ISO dates, ranges, presets, labels
     url        filter state in the address bar (keeps old ?q= &from= &to= links working)
     announce   polite screen-reader status updates
     random     pick a real entry, short tuning effect, open it
     timeline   year/month buckets for the Archive Time Machine
     timeMachine  renders the Time Machine from those buckets
     util       escapeHtml, debounce, reduced-motion check
   ============================================================ */
(function (root) {
  'use strict';

  /* ── util ─────────────────────────────────────────────────── */
  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  function debounce(fn, ms) {
    var t;
    return function () {
      var self = this, args = arguments;
      clearTimeout(t);
      t = setTimeout(function () { fn.apply(self, args); }, ms);
    };
  }
  function reducedMotion() {
    if (document.documentElement.getAttribute('data-ar-motion') === 'off') return true;
    return !!(root.matchMedia && root.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  /* ── dates ────────────────────────────────────────────────────
     Archive dates are plain YYYY-MM-DD strings with no time zone.
     Everything here works in the visitor's LOCAL calendar, so
     "Today" means today where they are. (The old page used
     toISOString(), which is UTC and could be a day off.) */
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function iso(d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  function parse(s) {                       /* 'YYYY-MM-DD' -> local Date at noon (DST-safe) */
    var p = String(s).split('-');
    return new Date(+p[0], (+p[1] || 1) - 1, +p[2] || 1, 12);
  }
  function addDays(d, n) { var x = new Date(d.getTime()); x.setDate(x.getDate() + n); return x; }
  function mondayOf(d) { return addDays(d, -((d.getDay() + 6) % 7)); }   /* ISO week start, same as build_digests.py */
  function isValid(s) { return /^\d{4}-\d{2}-\d{2}$/.test(s) && !isNaN(parse(s).getTime()); }

  /* preset -> {from, to} as ISO strings, relative to `now` (default: today, local) */
  function preset(name, now) {
    var t = now ? new Date(now.getTime()) : new Date();
    t.setHours(12, 0, 0, 0);
    var today = iso(t), mon = mondayOf(t);
    switch (name) {
      case 'today':    return { from: today, to: today };
      case 'week':     return { from: iso(mon), to: today };
      case 'lastweek': return { from: iso(addDays(mon, -7)), to: iso(addDays(mon, -1)) };
      case 'month':    return { from: iso(new Date(t.getFullYear(), t.getMonth(), 1, 12)), to: today };
      default:         return null;
    }
  }
  /* which preset (if any) a range matches, so buttons can show as pressed after a reload */
  function presetOf(from, to, now) {
    var names = ['today', 'week', 'lastweek', 'month'];
    for (var i = 0; i < names.length; i++) {
      var r = preset(names[i], now);
      if (r.from === from && r.to === to) return names[i];
    }
    return '';
  }
  function inRange(d, from, to) { return (!from || d >= from) && (!to || d <= to); }

  var LOCALE = 'en-US';
  function label(s, style) {                /* style: 'short' | 'long' | 'month' | 'monthShort' */
    var d = parse(s), o;
    if (style === 'long') o = { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' };
    else if (style === 'month') o = { month: 'long', year: 'numeric' };
    else if (style === 'monthShort') o = { month: 'short' };
    else o = { month: 'short', day: 'numeric', year: 'numeric' };
    return d.toLocaleDateString(LOCALE, o);
  }
  function monthLabel(ym) { return label(ym + '-01', 'month'); }

  var dates = { iso: iso, parse: parse, addDays: addDays, mondayOf: mondayOf, isValid: isValid,
                preset: preset, presetOf: presetOf, inRange: inRange, label: label, monthLabel: monthLabel };

  /* ── url ──────────────────────────────────────────────────────
     Reads and writes filter state in the query string with
     history.replaceState (no reloads, no extra history entries).
     `schema` maps a state key to its default; only non-default
     values are written, so shared links stay short. Existing links
     (notes.html?q=…&from=…&to=…) keep working because those keys
     keep their names. */
  function readState(schema, search) {
    var p = new URLSearchParams(search == null ? root.location.search : search), out = {};
    Object.keys(schema).forEach(function (k) {
      var def = schema[k], v = p.get(k);
      if (v == null || v === '') { out[k] = def; return; }
      if (typeof def === 'boolean') out[k] = v === '1' || v === 'true';
      else if (typeof def === 'number') out[k] = isNaN(+v) ? def : +v;
      else out[k] = v;
    });
    return out;
  }
  function toQuery(state, schema) {
    var p = new URLSearchParams();
    Object.keys(schema).forEach(function (k) {
      var v = state[k], def = schema[k];
      if (v === def || v == null || v === '' || v === false) return;
      p.set(k, typeof v === 'boolean' ? '1' : String(v));
    });
    var s = p.toString();
    return s ? '?' + s : '';
  }
  function writeState(state, schema) {
    try {
      history.replaceState(history.state, '', root.location.pathname + toQuery(state, schema) + root.location.hash);
    } catch (e) { /* file:// previews can refuse; harmless */ }
  }
  function shareUrl(state, schema) {
    return root.location.origin + root.location.pathname + toQuery(state, schema);
  }
  function copyText(text) {
    if (navigator.clipboard && root.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy') ? resolve() : reject(new Error('copy failed')); }
      catch (e) { reject(e); }
      finally { document.body.removeChild(ta); }
    });
  }
  var url = { read: readState, write: writeState, toQuery: toQuery, share: shareUrl, copy: copyText };

  /* ── announce ─────────────────────────────────────────────────
     One shared polite live region. Repeated identical messages are
     still read, because the text is cleared first. */
  var liveEl = null, liveT;
  function announce(msg) {
    if (!liveEl) {
      liveEl = document.createElement('div');
      liveEl.className = 'ar-sr-only';
      liveEl.setAttribute('role', 'status');
      liveEl.setAttribute('aria-live', 'polite');
      document.body.appendChild(liveEl);
    }
    clearTimeout(liveT);
    liveEl.textContent = '';
    liveT = setTimeout(function () { liveEl.textContent = msg; }, 60);
  }

  /* ── random ───────────────────────────────────────────────────
     pick(list, isValid) returns a random entry that passes isValid
     (e.g. has an id / an href), or null when none does. It never
     invents an entry. tune(label) shows the short tuning overlay
     and resolves when done; with reduced motion it resolves at once.
     go(href, opts) opens the real destination. */
  function pick(list, ok) {
    if (!list || !list.length) return null;
    var pool = ok ? list.filter(ok) : list;
    if (!pool.length) return null;
    var buf = new Uint32Array(1), i;
    if (root.crypto && root.crypto.getRandomValues) { root.crypto.getRandomValues(buf); i = buf[0] % pool.length; }
    else i = Math.floor(Math.random() * pool.length);
    return pool[i];
  }
  function tune(text) {
    return new Promise(function (resolve) {
      if (reducedMotion()) { resolve(); return; }
      var el = document.createElement('div');
      el.className = 'ar-tune';
      el.setAttribute('aria-hidden', 'true');
      el.innerHTML = '<div><div class="ar-tune__dial">' + escapeHtml(text || 'Tuning in…') +
                     '</div><span class="ar-tune__bars"></span></div>';
      document.body.appendChild(el);
      requestAnimationFrame(function () { el.classList.add('is-on'); });
      setTimeout(function () {
        el.classList.remove('is-on');
        setTimeout(function () { el.remove(); resolve(); }, 240);
      }, 650);
    });
  }
  /* opts.newTab: open in a new tab via a real rel="noopener" link
     click. Call it within a second or so of the visitor's click
     (the tuning effect is 0.9s) so browsers treat it as theirs. */
  function go(href, opts) {
    opts = opts || {};
    if (!opts.newTab) { root.location.href = href; return; }
    var a = document.createElement('a');
    a.href = href; a.target = '_blank'; a.rel = 'noopener';
    a.style.display = 'none';
    document.body.appendChild(a); a.click(); a.remove();
  }
  var random = { pick: pick, tune: tune, go: go };

  /* ── timeline ─────────────────────────────────────────────────
     build(dates) takes an array of real 'YYYY-MM-DD' (or 'YYYY-MM')
     strings and returns every year from the first to the last, each
     with all 12 months, so empty months are shown as empty rather
     than hidden or invented. Months outside the data's own first and
     last month are marked `outside`. */
  function buildTimeline(list) {
    var counts = {}, min = null, max = null;
    (list || []).forEach(function (s) {
      if (!s) return;
      var ym = String(s).slice(0, 7);
      if (!/^\d{4}-\d{2}$/.test(ym)) return;
      counts[ym] = (counts[ym] || 0) + 1;
      if (!min || ym < min) min = ym;
      if (!max || ym > max) max = ym;
    });
    if (!min) return { years: [], max: 0, first: null, last: null, total: 0 };
    var peak = 0, total = 0;
    Object.keys(counts).forEach(function (k) { peak = Math.max(peak, counts[k]); total += counts[k]; });
    var years = [];
    for (var y = +min.slice(0, 4); y <= +max.slice(0, 4); y++) {
      var months = [], ycount = 0;
      for (var m = 1; m <= 12; m++) {
        var key = y + '-' + pad(m), c = counts[key] || 0;
        ycount += c;
        months.push({ key: key, month: m, count: c, outside: key < min || key > max });
      }
      years.push({ year: y, count: ycount, months: months });
    }
    return { years: years, max: peak, first: min, last: max, total: total };
  }
  /* 1-4 brightness for a month with content; 0 for none */
  function level(count, peak) {
    if (!count) return 0;
    if (!peak) return 1;
    var r = count / peak;
    return r > .75 ? 4 : r > .5 ? 3 : r > .25 ? 2 : 1;
  }
  var timeline = { build: buildTimeline, level: level };

  /* ── timeMachine ──────────────────────────────────────────────
     render(container, tl, opts) draws the Archive Time Machine:
       - a <select> fallback (always present: keyboard, screen reader and phone friendly)
       - a row of year blocks with 12 month markers each
     opts.onSelect(ym)  called with 'YYYY-MM', or '' for "all time"
     opts.selected      currently selected 'YYYY-MM' or ''
     opts.noun          e.g. 'notes' or 'editions', used in labels
     Returns { setSelected(ym) }. */
  function renderTimeMachine(container, tl, opts) {
    opts = opts || {};
    var noun = opts.noun || 'entries';
    var onSelect = opts.onSelect || function () {};
    container.innerHTML = '';
    if (!tl || !tl.years.length) {
      container.innerHTML = '<p class="ar-meta">No dated ' + escapeHtml(noun) + ' yet.</p>';
      return { setSelected: function () {} };
    }

    /* select fallback */
    var selWrap = document.createElement('div');
    var selId = 'ar-tm-select-' + Math.random().toString(36).slice(2, 8);
    selWrap.innerHTML = '<label class="ar-label" for="' + selId + '">Jump to a month</label>';
    var sel = document.createElement('select');
    sel.className = 'ar-select'; sel.id = selId;
    var optAll = document.createElement('option');
    optAll.value = ''; optAll.textContent = 'All time (' + tl.total.toLocaleString(LOCALE) + ' ' + noun + ')';
    sel.appendChild(optAll);
    tl.years.slice().reverse().forEach(function (y) {
      var g = document.createElement('optgroup');
      g.label = y.year + ' · ' + y.count.toLocaleString(LOCALE) + ' ' + noun;
      y.months.slice().reverse().forEach(function (m) {
        if (!m.count) return;                  /* only real months are selectable */
        var o = document.createElement('option');
        o.value = m.key;
        o.textContent = monthLabel(m.key) + ' (' + m.count.toLocaleString(LOCALE) + ')';
        g.appendChild(o);
      });
      if (g.children.length) sel.appendChild(g);
    });
    sel.addEventListener('change', function () { setSelected(sel.value); onSelect(sel.value); });
    selWrap.appendChild(sel);
    container.appendChild(selWrap);

    /* visual strip: decorative duplicate of the select, still keyboard-usable */
    var strip = document.createElement('div');
    strip.className = 'ar-tm';
    strip.setAttribute('role', 'group');
    strip.setAttribute('aria-label', 'Archive timeline by month');
    tl.years.forEach(function (y) {
      var yb = document.createElement('div');
      yb.className = 'ar-tm__year';
      yb.innerHTML = '<div class="ar-tm__ylabel">' + y.year +
        ' <span class="ar-meta">' + y.count.toLocaleString(LOCALE) + ' ' + escapeHtml(noun) + '</span></div>';
      var grid = document.createElement('div');
      grid.className = 'ar-tm__months';
      y.months.forEach(function (m) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'ar-tm__m';
        b.dataset.ym = m.key;
        b.textContent = label(m.key + '-01', 'monthShort');
        var lv = level(m.count, tl.max);
        if (lv) {
          b.dataset.level = lv;
          b.setAttribute('aria-pressed', 'false');
          b.setAttribute('aria-label', monthLabel(m.key) + ', ' + m.count.toLocaleString(LOCALE) + ' ' + noun);
          b.addEventListener('click', function () {
            var next = b.getAttribute('aria-pressed') === 'true' ? '' : m.key;   /* click again to clear */
            setSelected(next); onSelect(next);
          });
        } else {
          b.disabled = true;
          b.setAttribute('aria-label', monthLabel(m.key) + ', no ' + noun);
          b.title = m.outside ? 'Outside the archive' : 'No ' + noun + ' this month';
        }
        grid.appendChild(b);
      });
      yb.appendChild(grid);
      strip.appendChild(yb);
    });
    container.appendChild(strip);

    function setSelected(ym) {
      sel.value = ym || '';
      strip.querySelectorAll('.ar-tm__m[data-level]').forEach(function (b) {
        b.setAttribute('aria-pressed', b.dataset.ym === ym ? 'true' : 'false');
      });
    }
    setSelected(opts.selected || '');
    /* open on the newest year */
    strip.scrollLeft = strip.scrollWidth;
    return { setSelected: setSelected, select: sel };
  }

  root.MMArchive = {
    version: '1',
    dates: dates,
    url: url,
    announce: announce,
    random: random,
    timeline: timeline,
    timeMachine: { render: renderTimeMachine },
    util: { escapeHtml: escapeHtml, debounce: debounce, reducedMotion: reducedMotion }
  };
})(window);
