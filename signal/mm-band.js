/* ============================================================
   MAGICKVISION SIGNAL BAND
   ------------------------------------------------------------
   Needs signal.js loaded first (const SIGNAL).
   Put <div class="mm-band" data-mode="home"></div> on a page,
   and optionally <div class="mm-receive"></div> for the panel.
   Self-contained: no dependencies, every class prefixed .mmb- / .mmr-
   ============================================================ */
(function () {
  'use strict';
  if (typeof SIGNAL === 'undefined') return;

  var S = SIGNAL, W = S.weeks, N = W.length, LAST = N - 1;
  var ON_SITE = /magickmica\.github\.io$/.test(location.hostname);
  var SITE = ON_SITE ? '../' : 'https://magickmica.github.io/';
  var reduce = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var MONTH = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var MAX = Math.max.apply(null, W.map(function (w) { return w.n; }));

  /* ---------- dates (string math, no timezone drift) ---------- */
  function parts(iso) { return iso.split('-').map(Number); }
  function addDays(iso, n) {
    var p = parts(iso);
    return new Date(Date.UTC(p[0], p[1] - 1, p[2] + n)).toISOString().slice(0, 10);
  }
  function fmt(iso, year) { var p = parts(iso); return MON[p[1] - 1] + ' ' + p[2] + (year ? ', ' + p[0] : ''); }
  function range(w) {
    var e = addDays(w, 6), a = parts(w), b = parts(e);
    if (a[1] === b[1]) return MON[a[1] - 1] + ' ' + a[2] + ' – ' + b[2] + ', ' + b[0];
    return fmt(w, a[0] !== b[0]) + ' – ' + fmt(e, true);
  }
  function num(n) { return n.toLocaleString('en-US'); }
  function plural(n, one, many) { return num(n) + ' ' + (n === 1 ? one : many); }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function indexOfWeek(w) { for (var i = 0; i < N; i++) if (W[i].w === w) return i; return -1; }

  /* ---------- styles ---------- */
  var CSS = [
    '.mmb{--mmb-glass:#0b0614;--mmb-ink:#f4eefe;--mmb-quiet:#a597c0;--mmb-needle:#fff4dc;--mmb-tv:#ff6ef7;--mmb-art:#6ef7ff;',
    'font-family:"Share Tech Mono",ui-monospace,Menlo,Consolas,monospace;color:var(--mmb-ink)}',
    '.mmb-housing{position:relative;border-radius:16px;padding:10px 10px 12px;',
    'background:linear-gradient(115deg,#2b2140 0%,#140c22 30%,#1a2433 55%,#2c1631 80%,#1b1428 100%);',
    'box-shadow:inset 0 1px 0 rgba(255,255,255,.14),inset 0 -1px 0 rgba(0,0,0,.6),0 0 0 1px rgba(214,190,255,.16),0 24px 48px -28px rgba(0,0,0,.9)}',
    '.mmb-glass{position:relative;border-radius:9px;background:radial-gradient(120% 140% at 50% 0%,#170c26 0%,var(--mmb-glass) 60%,#05020a 100%);',
    'box-shadow:inset 0 0 0 1px rgba(0,0,0,.7),inset 0 3px 14px rgba(0,0,0,.85);overflow:hidden;cursor:pointer;touch-action:pan-x}',
    '.mmb-glass:focus{outline:none}',
    '.mmb-glass:focus-visible{outline:2px solid var(--mmb-needle);outline-offset:3px}',
    '.mmb-glass::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:5;',
    'background:repeating-linear-gradient(to bottom,rgba(255,255,255,.04) 0 1px,transparent 1px 3px)}',
    '.mmb-scroll{overflow-x:auto;overflow-y:hidden;scrollbar-width:thin;scrollbar-color:#3a2d52 transparent}',
    '.mmb-track{position:relative;height:136px;min-width:calc(var(--mmb-n) * 9px + 28px)}',
    '.mmb-plot{position:absolute;left:14px;right:14px;top:0;bottom:0}',
    '.mmb-bars{position:absolute;left:0;right:0;top:30px;height:82px;display:flex;align-items:flex-end;gap:2px}',
    '.mmb-bar{flex:1 1 0;min-width:0;height:var(--h);background:var(--c);border-radius:2px 2px 0 0;opacity:.42;transition:opacity .15s,box-shadow .15s}',
    '.mmb-bar.is-empty{height:1px;background:var(--mmb-quiet);opacity:.35}',
    '.mmb-bar.is-on{opacity:1;box-shadow:0 0 14px 1px var(--c),0 0 3px var(--c)}',
    '.mmb-axis{position:absolute;left:0;right:0;top:112px;height:1px;background:rgba(214,190,255,.18)}',
    '.mmb-tick{position:absolute;top:4px;padding-left:5px;font-size:10.5px;letter-spacing:.12em;color:var(--mmb-quiet);white-space:nowrap}',
    '.mmb-tick::before{content:"";position:absolute;left:0;top:3px;width:1px;height:var(--th);background:rgba(244,238,254,.55);transform:rotate(var(--rot));transform-origin:top}',
    '.mmb-early{position:absolute;top:36px;font-size:10px;letter-spacing:.16em;color:var(--mmb-quiet);border-bottom:1px dashed rgba(165,151,192,.45);padding-bottom:3px;white-space:nowrap;overflow:hidden;text-overflow:clip}',
    '.mmb-dia{position:absolute;top:119px;width:6px;height:6px;margin-left:-3px;transform:rotate(45deg);background:var(--mmb-tv)}',
    '.mmb-dia.is-art{background:var(--mmb-art)}',
    '.mmb-needle{position:absolute;top:20px;bottom:4px;width:2px;margin-left:-1px;background:var(--mmb-needle);z-index:3;',
    'box-shadow:0 0 10px rgba(255,244,220,.75);pointer-events:none}',
    '.mmb-needle::before{content:"";position:absolute;top:-1px;left:-5px;border:6px solid transparent;border-top-color:var(--mmb-needle);border-bottom:0}',
    '.is-travel .mmb-needle{transition:left .25s cubic-bezier(.3,.7,.2,1)}',
    '.is-moving .mmb-needle{box-shadow:-2px 0 0 rgba(255,46,99,.9),2px 0 0 rgba(46,233,255,.9),0 0 12px rgba(255,244,220,.6)}',
    '.mmb-static{position:absolute;inset:0;width:100%;height:100%;z-index:4;pointer-events:none;opacity:0;transition:opacity .15s;image-rendering:pixelated;mix-blend-mode:screen}',
    '.is-moving .mmb-static{opacity:.3}',
    '.mmb-tip{position:absolute;top:44px;transform:translateX(-50%);z-index:6;pointer-events:none;background:rgba(5,2,10,.92);',
    'border:1px solid rgba(214,190,255,.3);border-radius:6px;padding:5px 8px;font-size:12px;white-space:nowrap;color:var(--mmb-ink)}',
    '.mmb-readout{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 18px;padding:12px 6px 2px}',
    '.mmb-state{display:inline-flex;align-items:center;gap:7px;font-size:12px;letter-spacing:.2em;color:var(--mmb-quiet)}',
    '.mmb-dot{width:8px;height:8px;border-radius:50%;border:1.5px solid var(--mmb-quiet)}',
    '.is-live .mmb-dot{background:#ff3b5c;border-color:#ff3b5c;animation:mmb-pulse 1.6s ease-in-out infinite}',
    '.is-live .mmb-state{color:#ff8fa3}',
    '@keyframes mmb-pulse{50%{box-shadow:0 0 0 5px rgba(255,59,92,0)}0%,100%{box-shadow:0 0 0 0 rgba(255,59,92,.55)}}',
    '.mmb-week{font-family:VT323,"Share Tech Mono",ui-monospace,monospace;font-size:27px;line-height:1;color:var(--mmb-needle);letter-spacing:.03em}',
    '.mmb-stats{font-family:VT323,"Share Tech Mono",ui-monospace,monospace;font-size:21px;line-height:1;color:var(--mmb-quiet);font-variant-numeric:tabular-nums}',
    '.mmb-controls{display:flex;flex-wrap:wrap;gap:8px;padding:12px 6px 0}',
    '.mmb-btn{font:inherit;font-size:12.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--mmb-ink);background:rgba(255,255,255,.03);',
    'border:1px solid rgba(214,190,255,.24);border-radius:7px;padding:9px 14px;min-height:40px;cursor:pointer}',
    '.mmb-btn:hover:not(:disabled){background:rgba(255,255,255,.08);border-color:rgba(214,190,255,.45)}',
    '.mmb-btn:focus-visible{outline:2px solid var(--mmb-needle);outline-offset:2px}',
    '.mmb-btn:disabled{opacity:.35;cursor:default}',
    '.mmb-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}',
    '@media (max-width:640px){.mmb-btn{min-height:44px;flex:1 1 auto}.mmb-week{font-size:24px}.mmb-stats{font-size:18px}.mmb-readout{gap:6px 12px}}',
    '@media (prefers-reduced-motion:reduce){.is-live .mmb-dot{animation:none}.mmb-bar{transition:none}}',

    /* receive panel */
    '.mmr{--mmr-ink:#f4eefe;--mmr-quiet:#a597c0;--mmr-panel:#110a1c;--mmr-line:rgba(214,190,255,.14);color:var(--mmr-ink);',
    'display:grid;grid-template-columns:minmax(0,1fr);gap:22px 36px;margin-top:30px}',
    '@media (min-width:860px){.mmr{grid-template-columns:minmax(0,1.75fr) minmax(0,1fr)}.mmr-head{grid-column:1/-1}}',
    '.mmr-eyebrow{margin:0 0 6px;font:12px/1.4 "Share Tech Mono",ui-monospace,monospace;letter-spacing:.2em;color:var(--wk)}',
    '.mmr-head h2{margin:0;font:600 clamp(28px,4vw,38px)/1.1 "Cormorant Garamond",Georgia,serif;text-wrap:balance}',
    '.mmr-sub{margin:8px 0 0;font:13px/1.5 "Share Tech Mono",ui-monospace,monospace;color:var(--mmr-quiet);font-variant-numeric:tabular-nums}',
    '.mmr-top{list-style:none;margin:0;padding:0;display:grid;gap:12px}',
    '.mmr-card{display:grid;grid-template-columns:auto minmax(0,1fr);gap:16px;align-items:start;padding:16px;background:var(--mmr-panel);border:1px solid var(--mmr-line);border-radius:10px}',
    '.mmr-card img{width:84px;height:84px;object-fit:cover;border-radius:6px;display:block;background:#1b1229}',
    '.mmr-card:first-child img{width:132px;height:132px}',
    '.mmr-card:not(:has(img)){grid-template-columns:minmax(0,1fr)}',
    '.mmr-q{margin:0;font:500 21px/1.25 "Cormorant Garamond",Georgia,serif;text-wrap:pretty;overflow-wrap:anywhere}',
    '.mmr-card:first-child .mmr-q{font-size:clamp(24px,3.2vw,31px);line-height:1.15}',
    '.mmr-q.is-glyph{font-size:30px;letter-spacing:.1em}',
    '.mmr-meta{margin:10px 0 0;font:12.5px/1.5 "Share Tech Mono",ui-monospace,monospace;color:var(--mmr-quiet);display:flex;flex-wrap:wrap;gap:4px 14px}',
    '.mmr-meta a{color:var(--wk);text-decoration:none}',
    '.mmr-meta a:hover,.mmr-meta a:focus-visible{text-decoration:underline}',
    '.mmr-side{display:flex;flex-direction:column;gap:22px;min-width:0}',
    '.mmr-label{margin:0 0 10px;font:12px/1.4 "Share Tech Mono",ui-monospace,monospace;letter-spacing:.18em;color:var(--mmr-quiet)}',
    '.mmr-arts{list-style:none;margin:0;padding:0;display:grid;gap:10px}',
    '.mmr-arts a{color:var(--mmr-ink);text-decoration:none;font:500 19px/1.25 "Cormorant Garamond",Georgia,serif}',
    '.mmr-arts a:hover,.mmr-arts a:focus-visible{text-decoration:underline;text-decoration-color:var(--wk)}',
    '.mmr-tag{display:inline-block;margin-right:8px;padding:1px 6px;border-radius:4px;font:11px/1.6 "Share Tech Mono",ui-monospace,monospace;letter-spacing:.1em;vertical-align:3px;color:#07020f}',
    '.mmr-tag.tv{background:#ff6ef7}.mmr-tag.art{background:#6ef7ff}',
    '.mmr-none{margin:0;font:13px/1.5 "Share Tech Mono",ui-monospace,monospace;color:var(--mmr-quiet)}',
    '.mmr-echo{margin:0;padding:12px 14px;border:1px dashed rgba(214,190,255,.25);border-radius:8px;font:italic 13px/1.55 "Share Tech Mono",ui-monospace,monospace;color:var(--mmr-quiet)}',
    '.mmr-echo b{font-style:normal;letter-spacing:.18em;color:var(--mmr-ink);font-weight:400}',
    '.mmr-echo button{font:inherit;font-style:normal;color:var(--wk);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline}',
    '.mmr-go{display:grid;gap:8px}',
    '.mmr-go a{display:block;padding:12px 14px;border-radius:8px;text-decoration:none;font:13px/1.3 "Share Tech Mono",ui-monospace,monospace;letter-spacing:.08em;',
    'color:var(--mmr-ink);border:1px solid rgba(214,190,255,.24)}',
    '.mmr-go a:first-child{background:var(--wk);border-color:var(--wk);color:#07020f}',
    '.mmr-go a:hover{filter:brightness(1.1)}',
    '.mmr-go a:focus-visible,.mmr-arts a:focus-visible,.mmr-meta a:focus-visible,.mmr-echo button:focus-visible{outline:2px solid #fff4dc;outline-offset:2px}',
    '.mmr-empty{padding:28px;border:1px dashed rgba(214,190,255,.25);border-radius:10px}',
    '.mmr-empty p{margin:0 0 14px;font:500 24px/1.2 "Cormorant Garamond",Georgia,serif}'
  ].join('');

  function injectStyle() {
    if (document.getElementById('mmb-style')) return;
    var st = document.createElement('style');
    st.id = 'mmb-style';
    st.textContent = CSS;
    document.head.appendChild(st);
    if (!document.querySelector('link[href*="VT323"]')) {
      var l = document.createElement('link');
      l.rel = 'stylesheet';
      l.href = 'https://fonts.googleapis.com/css2?family=VT323&family=Share+Tech+Mono&family=Cormorant+Garamond:wght@500;600&display=swap';
      document.head.appendChild(l);
    }
  }

  /* deterministic jitter for the hand-etched ticks */
  function jitter(i) { var x = Math.sin(i * 12.9898) * 43758.5453; return x - Math.floor(x); }

  /* ============================================================ */
  function Band(host) {
    var mode = host.getAttribute('data-mode') || 'home';
    var receive = document.querySelector('.mm-receive');
    var cur = LAST, moving = false, settleT = 0, travelT = 0, raf = 0, dragging = false;

    /* ---- build ---- */
    var bars = '', ticks = '', dias = '';
    W.forEach(function (w, i) {
      var h = w.n ? Math.max(4, w.n / MAX * 100) : 0;
      bars += '<div class="mmb-bar' + (w.n ? '' : ' is-empty') + '" data-i="' + i + '" style="--h:' + h.toFixed(1) + '%;--c:' + w.c + '"></div>';
      var nls = {};
      w.a.forEach(function (a) { nls[a.nl] = 1; });
      var keys = Object.keys(nls), cx = (i + 0.5) / N * 100;
      keys.forEach(function (k, j) {
        var off = keys.length > 1 ? (j ? 4 : -4) : 0;
        dias += '<span class="mmb-dia' + (k === 'Art' ? ' is-art' : '') + '" style="left:calc(' + cx.toFixed(3) + '% + ' + off + 'px)"></span>';
      });
      // month tick on the week that contains the 1st of a month
      for (var d = 0; d < 7; d++) {
        var day = addDays(w.w, d), dp = parts(day);
        if (dp[2] !== 1 && !(i === 0 && d === 0)) continue;
        if (i === 0 && d === 0 && dp[2] > 10) continue;   // band starts mid-month: the next tick is too close
        var x = (i + d / 7) / N * 100;
        // January is labelled with its year, so the turn of the year reads at a glance
        var lab = dp[1] === 1 ? String(dp[0]) : MON[dp[1] - 1].toUpperCase();
        ticks += '<span class="mmb-tick" style="left:' + x.toFixed(3) + '%;--th:' + (6 + jitter(i) * 7).toFixed(1) +
          'px;--rot:' + ((jitter(i + 7) - 0.5) * 8).toFixed(1) + 'deg">' + lab + '</span>';
      }
    });
    var early = -1;
    for (var k = 0; k < N; k++) { if (W[k].n >= 10) break; early = k; }
    var earlyHtml = early >= 3 ? '<span class="mmb-early" style="left:0;width:' + ((early + 1) / N * 100).toFixed(2) + '%">EARLY SIGNALS</span>' : '';

    host.innerHTML =
      '<div class="mmb">' +
        '<div class="mmb-housing">' +
          '<div class="mmb-glass" role="slider" tabindex="0" aria-label="Tune to a week" aria-valuemin="0" aria-valuemax="' + LAST + '">' +
            '<div class="mmb-scroll"><div class="mmb-track" style="--mmb-n:' + N + '"><div class="mmb-plot">' +
              ticks + '<div class="mmb-bars">' + bars + '</div>' + earlyHtml + '<div class="mmb-axis"></div>' + dias +
              '<div class="mmb-needle"></div><div class="mmb-tip" hidden></div>' +
            '</div></div></div>' +
            '<canvas class="mmb-static" aria-hidden="true"></canvas>' +
          '</div>' +
          '<div class="mmb-readout">' +
            '<span class="mmb-state"><i class="mmb-dot"></i><span class="mmb-state-t">LIVE</span></span>' +
            '<span class="mmb-week"></span><span class="mmb-stats"></span>' +
          '</div>' +
          '<div class="mmb-controls">' +
            '<button type="button" class="mmb-btn" data-act="prev">◂ Prev week</button>' +
            '<button type="button" class="mmb-btn" data-act="next">Next week ▸</button>' +
            '<button type="button" class="mmb-btn" data-act="live">Live</button>' +
            '<button type="button" class="mmb-btn" data-act="random">Random week</button>' +
          '</div>' +
          '<p class="mmb-sr" aria-live="polite"></p>' +
        '</div>' +
      '</div>';

    var root = host.querySelector('.mmb'), glass = host.querySelector('.mmb-glass');
    var scroller = host.querySelector('.mmb-scroll'), plot = host.querySelector('.mmb-plot');
    var needle = host.querySelector('.mmb-needle'), tip = host.querySelector('.mmb-tip');
    var cv = host.querySelector('.mmb-static'), ctx = cv.getContext('2d');
    var barEls = host.querySelectorAll('.mmb-bar');
    var weekEl = host.querySelector('.mmb-week'), statsEl = host.querySelector('.mmb-stats');
    var stateT = host.querySelector('.mmb-state-t'), sr = host.querySelector('.mmb-sr');
    var btn = {};
    host.querySelectorAll('.mmb-btn').forEach(function (b) { btn[b.getAttribute('data-act')] = b; });

    /* ---- static ---- */
    function sizeCanvas() {
      cv.width = Math.max(1, Math.ceil(glass.clientWidth / 3));
      cv.height = Math.max(1, Math.ceil(glass.clientHeight / 3));
    }
    function drawStatic() {
      if (!moving) { raf = 0; return; }
      var img = ctx.createImageData(cv.width, cv.height), d = img.data;
      for (var i = 0; i < d.length; i += 4) {
        var v = Math.random() * 255 | 0;
        d[i] = d[i + 1] = d[i + 2] = v;
        d[i + 3] = Math.random() < 0.55 ? 255 : 0;
      }
      ctx.putImageData(img, 0, 0);
      raf = requestAnimationFrame(drawStatic);
    }
    function startMove() {
      if (reduce.matches) return;
      if (!moving) { moving = true; root.classList.add('is-moving'); if (!raf) raf = requestAnimationFrame(drawStatic); }
    }
    function endMove() { moving = false; root.classList.remove('is-moving'); }

    /* ---- visual state (cheap, runs while moving) ---- */
    function setVisual(i) {
      cur = Math.max(0, Math.min(LAST, i));
      var w = W[cur];
      needle.style.left = ((cur + 0.5) / N * 100) + '%';
      for (var j = 0; j < N; j++) {
        var d = Math.abs(j - cur), b = barEls[j];
        b.classList.toggle('is-on', d === 0);
        if (!b.classList.contains('is-empty')) b.style.opacity = d === 0 ? 1 : d <= 4 ? (0.9 - d * 0.11).toFixed(2) : '';
      }
      var live = cur === LAST;
      root.classList.toggle('is-live', live);
      stateT.textContent = live ? 'LIVE' : 'TUNED';
      weekEl.textContent = 'WEEK OF ' + fmt(w.w, true).toUpperCase();
      statsEl.textContent = moving ? 'TUNING…' : statLine(w);
      glass.setAttribute('aria-valuenow', cur);
      glass.setAttribute('aria-valuetext', spoken(w));
      btn.prev.disabled = cur === 0;
      btn.next.disabled = live;
      btn.live.disabled = live;
    }
    function statLine(w) {
      if (!w.n) return 'NO TRANSMISSIONS';
      var s = plural(w.n, 'TRANSMISSION', 'TRANSMISSIONS') + ' · ' + num(w.l) + ' ♥';
      if (w.a.length) s += ' · ' + plural(w.a.length, 'ARTICLE', 'ARTICLES');
      return s;
    }
    function spoken(w) {
      var s = 'Week of ' + fmt(w.w, true) + ', ' + (w.n ? plural(w.n, 'transmission', 'transmissions') : 'no transmissions');
      if (w.a.length) s += ', ' + plural(w.a.length, 'article', 'articles');
      return s + (cur === LAST ? ', live' : '');
    }

    /* ---- settle: the expensive part, once the needle rests ---- */
    function settle() {
      endMove();
      root.classList.remove('is-travel');
      setVisual(cur);
      sr.textContent = spoken(W[cur]);
      try { history.replaceState(null, '', '#w' + W[cur].w); } catch (e) { /* preview frames */ }
      revealBar();
      if (receive) renderReceive(receive, cur, tune);
    }
    function revealBar() {
      if (scroller.scrollWidth <= scroller.clientWidth + 2) return;
      var pr = plot.getBoundingClientRect(), sr2 = scroller.getBoundingClientRect();
      var x = pr.left + (cur + 0.5) / N * pr.width - sr2.left + scroller.scrollLeft;
      var target = x - scroller.clientWidth / 2;
      scroller.scrollTo({ left: target, behavior: reduce.matches ? 'auto' : 'smooth' });
    }

    /* ---- tuning entry points ---- */
    function tune(i) {           // a jump: buttons, clicks, echo link
      i = Math.max(0, Math.min(LAST, i));
      clearTimeout(travelT); clearTimeout(settleT);
      if (reduce.matches || i === cur) { setVisual(i); settle(); return; }
      root.classList.add('is-travel');
      startMove();
      setVisual(i);
      travelT = setTimeout(settle, 260);
    }
    function nudge(i) {          // keyboard: follow instantly, settle when keys stop
      root.classList.remove('is-travel');
      startMove();
      setVisual(i);
      clearTimeout(settleT);
      settleT = setTimeout(settle, 200);
    }
    function indexAt(clientX) {
      var r = plot.getBoundingClientRect();
      return Math.max(0, Math.min(LAST, Math.floor((clientX - r.left) / r.width * N)));
    }

    /* ---- input ---- */
    glass.addEventListener('keydown', function (e) {
      var k = e.key, i = cur;
      if (k === 'ArrowLeft' || k === 'ArrowDown') i--;
      else if (k === 'ArrowRight' || k === 'ArrowUp') i++;
      else if (k === 'PageDown') i -= 4;
      else if (k === 'PageUp') i += 4;
      else if (k === 'Home') i = 0;
      else if (k === 'End') i = LAST;
      else if (k === 'Enter' && mode !== 'home' && W[cur].iss) { location.href = SITE + 'week-' + W[cur].w + '.html'; return; }
      else return;
      e.preventDefault();
      nudge(i);
    });
    glass.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse' || e.button !== 0) return;
      dragging = true;
      glass.setPointerCapture(e.pointerId);
      root.classList.remove('is-travel');
      tip.hidden = true;
      startMove();
      setVisual(indexAt(e.clientX));
      e.preventDefault();
      glass.focus({ preventScroll: true });
    });
    glass.addEventListener('pointermove', function (e) {
      if (dragging) { setVisual(indexAt(e.clientX)); return; }
      if (e.pointerType !== 'mouse') return;
      var i = indexAt(e.clientX), w = W[i], r = plot.getBoundingClientRect();
      tip.hidden = false;
      tip.textContent = range(w.w) + ' · ' + (w.n ? plural(w.n, 'note', 'notes') : 'no signal');
      var x = (i + 0.5) / N * r.width, half = tip.offsetWidth / 2 + 4;
      tip.style.left = Math.max(half, Math.min(r.width - half, x)) + 'px';
    });
    glass.addEventListener('pointerleave', function () { tip.hidden = true; });
    function endDrag() { if (!dragging) return; dragging = false; settle(); }
    glass.addEventListener('pointerup', endDrag);
    glass.addEventListener('pointercancel', endDrag);
    glass.addEventListener('click', function (e) {    // touch and pen: tap a bar to tune
      if (e.pointerType === 'mouse' || dragging) return;
      if (e.detail === 0) return;                     // keyboard "click"
      tune(indexAt(e.clientX));
    });

    btn.prev.addEventListener('click', function () { tune(cur - 1); });
    btn.next.addEventListener('click', function () { tune(cur + 1); });
    btn.live.addEventListener('click', function () { tune(LAST); });
    btn.random.addEventListener('click', function () {
      var pool = [];
      for (var i = 0; i < N; i++) if (W[i].n && i !== cur) pool.push(i);
      tune(pool[Math.floor(Math.random() * pool.length)]);
    });
    window.addEventListener('hashchange', function () {
      var i = fromHash();
      if (i >= 0 && i !== cur) tune(i);
    });

    sizeCanvas();
    window.addEventListener('resize', sizeCanvas);

    function fromHash() {
      var m = /^#w(\d{4}-\d{2}-\d{2})$/.exec(location.hash || '');
      return m ? indexOfWeek(m[1]) : -1;
    }
    var start = fromHash();
    setVisual(start >= 0 ? start : LAST);
    settle();
  }

  /* ============================================================
     RECEIVE PANEL — what aired in the tuned week
     ============================================================ */
  function img(src) { return src.indexOf('http') === 0 ? src : S.imgPrefix + src; }

  function renderReceive(el, i, tune) {
    var w = W[i], end = addDays(w.w, 6);
    el.style.setProperty('--wk', w.c);
    var head = '<div class="mmr-head"><p class="mmr-eyebrow">' + (i === LAST ? 'NOW BROADCASTING' : 'RECEIVED') +
      ' · CH 01</p><h2>' + esc(range(w.w)) + '</h2>' +
      '<p class="mmr-sub">' + (w.n ? plural(w.n, 'transmission', 'transmissions') + ' · ' + num(w.l) + ' hearts · ' +
        num(w.img) + ' with images' : 'Dead air') + '</p></div>';

    var main;
    if (!w.n) {
      var before = i - 1, after = i + 1;
      while (before >= 0 && !W[before].n) before--;
      while (after <= LAST && !W[after].n) after++;
      main = '<div class="mmr-empty"><p>No transmissions this week.</p><div class="mmr-go">' +
        (before >= 0 ? '<a href="#w' + W[before].w + '">◂ Week of ' + fmt(W[before].w, true) + '</a>' : '') +
        (after <= LAST ? '<a href="#w' + W[after].w + '">Week of ' + fmt(W[after].w, true) + ' ▸</a>' : '') +
        '</div></div>';
    } else {
      main = '<ol class="mmr-top" aria-label="Most-loved transmissions this week">' + w.top.map(function (t) {
        var glyph = !/[A-Za-z0-9]/.test(t.x);
        return '<li class="mmr-card">' +
          (t.i ? '<img src="' + esc(img(t.i)) + '" alt="" loading="lazy" decoding="async">' : '') +
          '<div><p class="mmr-q' + (glyph ? ' is-glyph' : '') + '">' + (t.x ? esc(t.x) : '<em>(image only)</em>') + '</p>' +
          '<p class="mmr-meta"><span>♥ ' + num(t.l) + '</span><span>' + fmt(t.d) + '</span>' +
          '<a href="https://substack.com/@magickmica/note/c-' + t.id + '" target="_blank" rel="noopener">Open on Substack ↗</a></p>' +
          '</div></li>';
      }).join('') + '</ol>';
    }

    var side = '<div class="mmr-side">';
    side += '<section><h3 class="mmr-label">ARTICLES THIS WEEK</h3>' + (w.a.length
      ? '<ul class="mmr-arts">' + w.a.map(function (a) {
          return '<li><span class="mmr-tag ' + (a.nl === 'Art' ? 'art' : 'tv') + '">' + (a.nl === 'Art' ? 'ART' : 'TV') + '</span>' +
            '<a href="' + esc(a.u) + '" target="_blank" rel="noopener">' + esc(a.t) + '</a></li>';
        }).join('') + '</ul>'
      : '<p class="mmr-none">No articles aired this week.</p>') + '</section>';

    if (i === 0 && S.preSignal.length) {
      side += '<section><h3 class="mmr-label">BEFORE THE FIRST NOTE</h3><ul class="mmr-arts">' + S.preSignal.map(function (a) {
        return '<li><span class="mmr-tag ' + (a.nl === 'Art' ? 'art' : 'tv') + '">' + (a.nl === 'Art' ? 'ART' : 'TV') + '</span>' +
          '<a href="' + esc(a.u) + '" target="_blank" rel="noopener">' + esc(a.t) + '</a> <span class="mmr-none">' + fmt(a.d, true) + '</span></li>';
      }).join('') + '</ul></section>';
    }

    var ei = indexOfWeek(addDays(w.w, -364));
    if (ei >= 0 && W[ei].n) {
      var ew = W[ei], et = ew.top[0] && ew.top[0].x;
      side += '<p class="mmr-echo"><b>↺ ECHO</b> · one year earlier, ' +
        '<button type="button" data-echo="' + ei + '">week of ' + fmt(ew.w, true) + '</button>: ' +
        plural(ew.n, 'transmission', 'transmissions') + (et ? '. “' + esc(et) + '”' : '.') + '</p>';
    }

    var p = parts(w.w), mkey = w.w.slice(0, 7), month = null;
    S.months.forEach(function (m) { if (m.m === mkey) month = m; });
    var go = '';
    if (w.iss) go += '<a href="' + SITE + 'week-' + w.w + '.html">Watch the full broadcast →</a>';
    if (w.n) go += '<a href="' + SITE + 'notes.html?from=' + w.w + '&amp;to=' + end + '">Search this week’s notes →</a>';
    if (month && month.iss) go += '<a href="' + SITE + 'month-' + mkey + '.html">Open the ' + MONTH[p[1] - 1] + ' issue →</a>';
    if (go) side += '<nav class="mmr-go" aria-label="Go deeper">' + go + '</nav>';
    side += '</div>';

    el.innerHTML = '<div class="mmr">' + head + '<div>' + main + '</div>' + side + '</div>';
    el.querySelectorAll('.mmr-card img').forEach(function (im) {
      im.addEventListener('error', function () { im.remove(); });
    });
    var eb = el.querySelector('[data-echo]');
    if (eb) eb.addEventListener('click', function () { tune(+eb.getAttribute('data-echo')); });
  }

  /* ---------- boot ---------- */
  function boot() {
    injectStyle();
    document.querySelectorAll('.mm-band').forEach(function (h) { Band(h); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
