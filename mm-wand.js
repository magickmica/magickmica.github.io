/* ==========================================================
   mm-wand.js · the Magick wand from the Crystal Stress Index
   A wand cursor, a sparkle trail that follows it, a burst of
   stars on every click or tap, and soft spell chimes that stay
   off until the visitor turns sound on (remembered as mm-sound).
   Drop in with: <script src="mm-wand.js" defer></script>
   ========================================================== */
(function () {
  if (window.MM_WAND) return; window.MM_WAND = true;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var css = "@media (hover:hover) and (pointer:fine){\n  html,body,a,button,summary,label,input{\n    cursor:url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='36' height='36' viewBox='0 0 36 36'%3E%3Cdefs%3E%3ClinearGradient id='s' x1='0' x2='1'%3E%3Cstop offset='0' stop-color='%23FFF6FB'/%3E%3Cstop offset='1' stop-color='%23B79CFF'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cpath d='M11 11 L33 33' stroke='%230B0417' stroke-width='6' stroke-linecap='round'/%3E%3Cpath d='M11 11 L33 33' stroke='url(%23s)' stroke-width='3.2' stroke-linecap='round'/%3E%3Cpath d='M29 29 L33 33' stroke='%23F5C044' stroke-width='3.2' stroke-linecap='round'/%3E%3Cpath d='M8 1 L9.8 6.2 L15 8 L9.8 9.8 L8 15 L6.2 9.8 L1 8 L6.2 6.2 Z' fill='%23F5C044' stroke='%230B0417' stroke-width='1'/%3E%3C/svg%3E\") 8 8, auto;\n  }\n  input{cursor:url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='36' height='36' viewBox='0 0 36 36'%3E%3Cpath d='M11 11 L33 33' stroke='%230B0417' stroke-width='6' stroke-linecap='round'/%3E%3Cpath d='M11 11 L33 33' stroke='%235FE8D0' stroke-width='3.2' stroke-linecap='round'/%3E%3Cpath d='M8 1 L9.8 6.2 L15 8 L9.8 9.8 L8 15 L6.2 9.8 L1 8 L6.2 6.2 Z' fill='%235FE8D0' stroke='%230B0417' stroke-width='1'/%3E%3C/svg%3E\") 8 8, text}\n}\n" +
    '#mmWandFx{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:9500}' +
    '.mm-wand-sound{position:fixed;right:16px;bottom:16px;z-index:9550;padding:9px 14px;border-radius:999px;cursor:pointer;' +
    'font:500 11px/1 "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.14em;text-transform:uppercase;color:#efe6ff;' +
    'background:rgba(11,4,23,.78);border:1px solid rgba(183,156,255,.55);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}' +
    '.mm-wand-sound:hover{border-color:#fff}.mm-wand-sound[aria-pressed="true"]{color:#1b0a2e;background:#5fe8d0;border-color:#5fe8d0}' +
    '.mm-wand-sound:focus-visible{outline:3px solid #ffce5c;outline-offset:3px}';
  var st = document.createElement('style'); st.id = 'mm-wand-css'; st.textContent = css; document.head.appendChild(st);

  var cv = document.createElement('canvas'); cv.id = 'mmWandFx'; cv.setAttribute('aria-hidden', 'true');
  document.body.appendChild(cv);
  var ctx = cv.getContext('2d');
  var COLS = ['245,192,68', '255,122,200', '183,156,255', '95,232,208', '255,246,251'];
  var parts = [], W = 0, H = 0, running = false;
  function size() { var d = Math.min(2, window.devicePixelRatio || 1); W = innerWidth; H = innerHeight;
    cv.width = W * d; cv.height = H * d; ctx.setTransform(d, 0, 0, d, 0, 0); }
  size(); addEventListener('resize', size);
  function star(x, y, r, rot) { ctx.beginPath();
    for (var i = 0; i < 8; i++) { var a = rot + i * Math.PI / 4, rr = i % 2 ? r * .38 : r;
      ctx[i ? 'lineTo' : 'moveTo'](x + Math.cos(a) * rr, y + Math.sin(a) * rr); }
    ctx.closePath(); ctx.fill(); }
  function emit(x, y, n, speed) {
    if (reduce) return;
    for (var i = 0; i < n; i++) { var a = Math.random() * Math.PI * 2, s = (Math.random() * .7 + .3) * speed;
      parts.push({ x: x, y: y, vx: Math.cos(a) * s, vy: Math.sin(a) * s - speed * .2, r: 1.5 + Math.random() * 3.5,
        life: 1, decay: .012 + Math.random() * .02, rot: Math.random() * 6, c: COLS[(Math.random() * COLS.length) | 0] }); }
    if (parts.length > 500) parts.splice(0, parts.length - 500);
    if (!running) { running = true; requestAnimationFrame(tick); }
  }
  function tick() {
    ctx.clearRect(0, 0, W, H);
    parts = parts.filter(function (p) { return (p.life -= p.decay) > 0; });
    for (var i = 0; i < parts.length; i++) { var p = parts[i];
      p.x += p.vx; p.y += p.vy; p.vy += .03; p.vx *= .985; p.rot += .08;
      ctx.fillStyle = 'rgba(' + p.c + ',' + p.life + ')'; ctx.shadowColor = ctx.fillStyle; ctx.shadowBlur = 8;
      star(p.x, p.y, p.r * (.6 + p.life * .4), p.rot); }
    if (parts.length) requestAnimationFrame(tick); else { running = false; ctx.clearRect(0, 0, W, H); }
  }
  var lx = 0, ly = 0;
  addEventListener('pointermove', function (e) {
    if (e.pointerType !== 'mouse') return;
    var d = Math.hypot(e.clientX - lx, e.clientY - ly);
    if (d > 6) { emit(e.clientX - 2, e.clientY - 2, Math.min(3, 1 + d / 30), .6); lx = e.clientX; ly = e.clientY; }
  }, { passive: true });
  addEventListener('pointerdown', function (e) { emit(e.clientX, e.clientY, 18, 2.4); tap(); }, { passive: true });

  /* sound: synthesized chimes, off until turned on */
  var on = false, ac = null;
  try { on = localStorage.getItem('mm-sound') === 'on'; } catch (e) {}
  function A() { if (!ac) { try { ac = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { return null; } }
    if (ac.state === 'suspended') ac.resume(); return ac; }
  function tone(f, t0, dur, type, vol) { var a = A(); if (!a) return;
    var o = a.createOscillator(), g = a.createGain(), t = a.currentTime + t0;
    o.type = type || 'sine'; o.frequency.setValueAtTime(f, t); g.gain.setValueAtTime(0, t);
    g.gain.linearRampToValueAtTime(vol || .08, t + .01); g.gain.exponentialRampToValueAtTime(.0001, t + dur);
    o.connect(g).connect(a.destination); o.start(t); o.stop(t + dur + .05); }
  function tap() { if (on) { tone(1568, 0, .25, 'sine', .04); tone(2093, .03, .3, 'triangle', .025); } }
  function cast() { if (!on) return; [523.25, 659.25, 783.99, 880, 1174.66].forEach(function (f, i) { tone(f, i * .07, .6, 'sine', .06); });
    tone(1568, .38, 1.4, 'triangle', .05); }
  var btn = document.createElement('button'); btn.type = 'button'; btn.className = 'mm-wand-sound';
  function paint() { btn.textContent = on ? '♪ Sound on' : '♪ Sound off'; btn.setAttribute('aria-pressed', on ? 'true' : 'false'); }
  paint(); document.body.appendChild(btn);
  btn.addEventListener('click', function () { on = !on; paint();
    try { localStorage.setItem('mm-sound', on ? 'on' : 'off'); } catch (e) {} if (on) cast(); });
  window.MM_FX = window.MM_FX || { emit: emit };
})();
