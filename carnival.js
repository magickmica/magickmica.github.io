/* MAGICKMICA · carnival.js
   Shared bits for the Cosmic Circus midway games: sound, canvas sizing,
   particles, starfield, little drawing helpers. No network, no tracking. */
(function () {
  'use strict';
  var reduce = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);

  /* ---------------- per-game saved stats (this browser only) */
  function store(key, defaults) {
    var data = Object.assign({}, defaults);
    try { Object.assign(data, JSON.parse(localStorage.getItem(key) || '{}')); } catch (e) {}
    return { data: data, save: function () { try { localStorage.setItem(key, JSON.stringify(data)); } catch (e) {} } };
  }
  var prefs = store('mm_carnival_prefs_v1', { sound: true });

  /* ---------------- sound */
  var Sound = (function () {
    var ac = null, master = null, noiseBuf = null;
    function boot() {
      if (ac) { if (ac.state === 'suspended') ac.resume(); return; }
      var AC = window.AudioContext || window.webkitAudioContext; if (!AC) return;
      ac = new AC(); master = ac.createGain(); master.gain.value = prefs.data.sound ? .7 : 0; master.connect(ac.destination);
      var len = ac.sampleRate, buf = ac.createBuffer(1, len, ac.sampleRate), d = buf.getChannelData(0);
      for (var i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
      noiseBuf = buf;
    }
    function tone(f, at, dur, peak, type, glideTo) {
      if (!ac) return; var t = ac.currentTime + (at || 0);
      var o = ac.createOscillator(), g = ac.createGain(); o.type = type || 'triangle'; o.frequency.setValueAtTime(f, t);
      if (glideTo) o.frequency.exponentialRampToValueAtTime(glideTo, t + dur);
      g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(peak || .2, t + .012); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      o.connect(g); g.connect(master); o.start(t); o.stop(t + dur + .05);
    }
    function noise(dur, peak, freq, type, at) {
      if (!ac) return; var t = ac.currentTime + (at || 0), s = ac.createBufferSource(), g = ac.createGain(), f = ac.createBiquadFilter();
      s.buffer = noiseBuf; f.type = type || 'lowpass'; f.frequency.value = freq || 3000;
      g.gain.setValueAtTime(peak || .3, t); g.gain.exponentialRampToValueAtTime(0.001, t + dur);
      s.connect(f); f.connect(g); g.connect(master); s.start(t); s.stop(t + dur + .05);
    }
    return {
      boot: boot, tone: tone, noise: noise,
      setOn: function (on) { if (master) master.gain.value = on ? .7 : 0; },
      click: function () { tone(1800 + Math.random() * 300, 0, .03, .06, 'square'); },
      ding: function (hi) { tone(hi ? 1568 : 1046, 0, .5, .22, 'sine'); tone(hi ? 2093 : 1318, .02, .4, .08, 'sine'); },
      whoosh: function () { noise(.25, .12, 1800, 'bandpass'); },
      clink: function () { tone(2400, 0, .12, .1, 'sine'); tone(3300, .01, .1, .05, 'sine'); },
      thud: function () { tone(140, 0, .18, .25, 'sine', 60); noise(.08, .1, 600); },
      pop: function (big) { noise(big ? .35 : .2, big ? .8 : .4, big ? 5000 : 3200); tone(big ? 120 : 200, 0, .2, big ? .4 : .2, 'sine', 50); },
      bell: function () { [880, 1320, 1760].forEach(function (f, i) { tone(f, 0, 1.6 - i * .3, .18 / (i + 1), 'sine'); }); },
      fanfare: function () { [523, 659, 784, 1046, 784, 1046].forEach(function (f, i) { tone(f, i * .11, i === 5 ? .6 : .16, .16, 'square'); tone(f / 2, i * .11, .16, .06, 'triangle'); }); },
      womp: function () { [392, 370, 349, 294].forEach(function (f, i) { tone(f, i * .32, i === 3 ? .9 : .3, .14, 'sawtooth', i === 3 ? 220 : f * .97); }); }
    };
  })();
  function soundButton(btn) {
    if (!btn) return;
    function label() { btn.textContent = '♪ Sound: ' + (prefs.data.sound ? 'on' : 'off'); }
    label();
    btn.addEventListener('click', function () { prefs.data.sound = !prefs.data.sound; prefs.save(); label(); Sound.boot(); Sound.setOn(prefs.data.sound); });
  }

  /* ---------------- canvas sizing */
  function canvas(cv, stage, heightFor) {
    var ctx = cv.getContext('2d'), view = { W: 0, H: 0, ctx: ctx, onResize: null };
    function fit() {
      var w = stage.clientWidth, h = heightFor(w), dpr = Math.min(window.devicePixelRatio || 1, 2);
      view.W = w; view.H = h; cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); cv.style.height = h + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      if (view.onResize) view.onResize();
    }
    view.fit = fit; fit();
    addEventListener('resize', fit);
    return view;
  }
  function pt(cv, e) { var r = cv.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }

  /* ---------------- particles */
  function Bits() {
    var list = [];
    return {
      list: list,
      burst: function (x, y, col, big) {
        var n = reduce ? 16 : (big ? 60 : 24);
        for (var i = 0; i < n; i++) {
          var a = Math.random() * 6.28, sp = (big ? 260 : 150) * (.4 + Math.random());
          list.push({ x: x, y: y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - 60, g: 520, life: 1, decay: big ? .8 : 1.3,
            s: big ? 4 + Math.random() * 6 : 3 + Math.random() * 3, c: Math.random() < .75 ? col : '#ffffff', rot: Math.random() * 6, vr: (Math.random() - .5) * 14, kind: 'shred' });
        }
      },
      sparkle: function (x, y, col, n) {
        for (var i = 0; i < (n || 10); i++) list.push({ x: x, y: y, vx: (Math.random() - .5) * 160, vy: -Math.random() * 160 - 20, g: 400,
          life: 1, decay: 2, s: 1.5 + Math.random() * 2, c: col, rot: 0, vr: 0, kind: 'dot' });
      },
      confetti: function (W, H) {
        if (reduce) return;
        var cols = ['#ff4fa3', '#5ff3e8', '#ffd166', '#9667ba', '#d5c2dc', '#ffffff'];
        for (var i = 0; i < 140; i++) list.push({ x: Math.random() * W, y: -20 - Math.random() * H * .5, vx: (Math.random() - .5) * 80, vy: 60 + Math.random() * 120,
          g: 60, life: 1, decay: .22, s: 4 + Math.random() * 5, c: cols[i % cols.length], rot: Math.random() * 6, vr: (Math.random() - .5) * 10, kind: 'conf' });
      },
      step: function (dt, H) {
        for (var j = list.length - 1; j >= 0; j--) {
          var q = list[j]; q.life -= dt * q.decay; q.vy += q.g * dt; q.x += q.vx * dt; q.y += q.vy * dt; q.rot += q.vr * dt;
          if (q.life <= 0 || q.y > H + 30) list.splice(j, 1);
        }
      },
      draw: function (ctx) {
        list.forEach(function (q) {
          ctx.globalAlpha = Math.max(0, Math.min(1, q.life)); ctx.fillStyle = q.c;
          if (q.kind === 'dot') { ctx.beginPath(); ctx.arc(q.x, q.y, q.s, 0, 6.28); ctx.fill(); }
          else { ctx.save(); ctx.translate(q.x, q.y); ctx.rotate(q.rot); ctx.fillRect(-q.s / 2, -q.s / 4, q.s, q.s / 2); ctx.restore(); }
        });
        ctx.globalAlpha = 1;
      }
    };
  }

  /* ---------------- drawing helpers */
  var stars = [];
  for (var s = 0; s < 70; s++) stars.push({ x: Math.random(), y: Math.random(), r: Math.random() * 1.3 + .3, t: Math.random() * 6 });
  function sky(ctx, W, H, t) {
    var g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#131c3f'); g.addColorStop(.7, '#0b1029'); g.addColorStop(1, '#040509');
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    stars.forEach(function (st) {
      ctx.globalAlpha = reduce ? .6 : .35 + .35 * Math.sin(t * 1.5 + st.t); ctx.fillStyle = '#fff';
      ctx.beginPath(); ctx.arc(st.x * W, st.y * H, st.r, 0, 6.28); ctx.fill();
    });
    ctx.globalAlpha = 1;
  }
  function rr(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
  function shade(hex, amt) {
    var n = parseInt(hex.slice(1), 16), r = n >> 16, g = (n >> 8) & 255, b = n & 255;
    function f(c) { return Math.max(0, Math.min(255, Math.round(amt < 0 ? c * (1 + amt) : c + (255 - c) * amt))); }
    return 'rgb(' + f(r) + ',' + f(g) + ',' + f(b) + ')';
  }
  function star(ctx, x, y, r, pts, inner) {
    ctx.beginPath();
    for (var i = 0; i < pts * 2; i++) { var a = i * Math.PI / pts - Math.PI / 2, rad = i % 2 ? r * inner : r; ctx.lineTo(x + Math.cos(a) * rad, y + Math.sin(a) * rad); }
    ctx.closePath();
  }
  function bigText(ctx, txt, x, y, size, glow) {
    ctx.save(); ctx.font = '900 ' + Math.round(size) + 'px Orbitron, sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.lineWidth = Math.max(4, size / 10); ctx.strokeStyle = '#2f2f70'; ctx.strokeText(txt, x, y);
    ctx.shadowColor = glow || '#ff4fa3'; ctx.shadowBlur = 22; ctx.fillStyle = '#fff'; ctx.fillText(txt, x, y); ctx.restore();
  }
  function label(ctx, txt, x, y, col, size, align) {
    ctx.font = (size || 10) + 'px Silkscreen, monospace'; ctx.textAlign = align || 'center'; ctx.textBaseline = 'alphabetic'; ctx.fillStyle = col || '#d5c2dc'; ctx.fillText(txt, x, y);
  }
  function loop(fn) {
    var last = performance.now();
    function f(now) { var dt = Math.min(.05, (now - last) / 1000); last = now; fn(dt, now / 1000); requestAnimationFrame(f); }
    requestAnimationFrame(function (n) { last = n; f(n); });
  }
  if (document.fonts && document.fonts.load) { document.fonts.load('10px Silkscreen'); document.fonts.load('900 40px Orbitron'); }

  /* ---------------- prize helper for the end screen */
  function prizeCard(prize) {
    return '<div class="prize"><span class="em">' + prize.e + '</span><span><span class="tier">' + prize.tier.toUpperCase() +
      ' PRIZE</span><span class="nm">' + prize.n + '</span></span></div>';
  }
  function award(tier, game) {
    if (!window.MMPrizes) return null;
    var p = MMPrizes.pick(tier); MMPrizes.add(p, game); MMPrizes.addToken(1); return p;
  }
  function shelf(el) {
    if (!el || !window.MMPrizes) return;
    MMPrizes.render(el);
    addEventListener('mm-prizes', function () { MMPrizes.render(el); });
  }

  window.MMC = { reduce: reduce, store: store, Sound: Sound, soundButton: soundButton, canvas: canvas, pt: pt, Bits: Bits,
    sky: sky, rr: rr, shade: shade, star: star, bigText: bigText, label: label, loop: loop, prizeCard: prizeCard, award: award, shelf: shelf };
})();
