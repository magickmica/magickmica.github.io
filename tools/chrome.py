"""Ambient per-theme page chrome — the decorative layer behind everything.

Each frequency had its own hand-built effects on the original pages, behind a
two-letter class prefix (hw- halloween bats and fog, se- sea bubbles and fish,
wn- winter flakes and aurora, and so on). The mosaic template dropped them, so
they were lifted back out by tools/extract_chrome.py and live here.

A theme opts in with "chrome": "<name>" in _data/themes.json.
"""

CHROME = {
  "crystal": {
    "css": r'''
/* crystal chrome: drifting shards, prism motes, a slow aurora wash */
.cr-aurora{position:fixed;inset:-30% -10% auto -10%;height:70vh;z-index:0;pointer-events:none;
background:radial-gradient(50% 60% at 22% 30%,color-mix(in srgb,var(--purple) 22%,transparent),transparent 70%),
radial-gradient(46% 55% at 76% 22%,color-mix(in srgb,var(--cyan) 18%,transparent),transparent 70%),
radial-gradient(40% 50% at 50% 60%,color-mix(in srgb,var(--pink) 14%,transparent),transparent 72%);
filter:blur(30px);animation:crAurora 24s ease-in-out infinite}
@keyframes crAurora{0%,100%{transform:translateX(-3%) scale(1);opacity:.85}
50%{transform:translateX(3%) scale(1.06);opacity:1}}

.cr-shard{position:fixed;z-index:1;pointer-events:none;opacity:0;
width:22px;height:40px;clip-path:polygon(50% 0,100% 32%,78% 100%,22% 100%,0 32%);
background:linear-gradient(150deg,color-mix(in srgb,var(--cyan) 85%,transparent),
color-mix(in srgb,var(--purple) 70%,transparent) 46%,color-mix(in srgb,var(--pink) 65%,transparent));
box-shadow:0 0 18px color-mix(in srgb,var(--purple) 55%,transparent);
animation:crDrift linear infinite}
.cr-shard:after{content:'';position:absolute;inset:0;
background:linear-gradient(112deg,transparent 34%,rgba(255,255,255,.55) 40%,transparent 46%,
transparent 62%,rgba(255,255,255,.3) 67%,transparent 72%)}
.cr-shard.b{width:14px;height:26px;
background:linear-gradient(150deg,color-mix(in srgb,var(--gold) 80%,transparent),
color-mix(in srgb,var(--pink) 60%,transparent))}
.cr-shard.c{width:30px;height:52px;
background:linear-gradient(150deg,color-mix(in srgb,var(--lime) 55%,transparent),
color-mix(in srgb,var(--cyan) 70%,transparent) 60%,color-mix(in srgb,var(--purple) 60%,transparent))}
@keyframes crDrift{0%{opacity:0;transform:translateY(6vh) rotate(0) scale(.7)}
12%{opacity:.75}
60%{opacity:.55}
100%{opacity:0;transform:translateY(-88vh) rotate(220deg) scale(1.05)}}

.cr-mote{position:fixed;z-index:1;pointer-events:none;width:3px;height:3px;border-radius:50%;
background:#fff;box-shadow:0 0 8px 2px color-mix(in srgb,var(--cyan) 70%,transparent);
opacity:0;animation:crTwinkle 5s ease-in-out infinite}
.cr-mote.g{box-shadow:0 0 8px 2px color-mix(in srgb,var(--gold) 75%,transparent)}
.cr-mote.p{box-shadow:0 0 8px 2px color-mix(in srgb,var(--pink) 75%,transparent)}
@keyframes crTwinkle{0%,100%{opacity:0;transform:scale(.4)}
45%{opacity:.95;transform:scale(1.25)}
75%{opacity:.35;transform:scale(.8)}}

.cr-prism{position:fixed;top:0;left:0;right:0;height:2px;z-index:2;pointer-events:none;
background:linear-gradient(90deg,transparent,var(--purple),var(--pink) 30%,var(--gold) 52%,
var(--cyan) 74%,transparent);opacity:.55;animation:crSweep 11s ease-in-out infinite}
@keyframes crSweep{0%,100%{opacity:.3;filter:blur(0)}50%{opacity:.75;filter:blur(1px)}}

@media(prefers-reduced-motion:reduce){
 .cr-aurora,.cr-shard,.cr-mote,.cr-prism{animation:none!important}
 .cr-shard{display:none}.cr-mote{opacity:.6}}
''',
    "html": r'''<div class="cr-prism" aria-hidden="true"></div>
<div class="cr-aurora" aria-hidden="true"></div>
<div class="cr-field" aria-hidden="true"></div>''',
    "js": r'''
(function(){
  var f=document.querySelector('.cr-field'); if(!f) return;
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var h='',i;
  for(i=0;i<(reduce?0:14);i++){
    var cls=['','b','c'][i%3];
    h+='<div class="cr-shard '+cls+'" style="left:'+(3+Math.random()*94).toFixed(1)+'%;bottom:-8vh;'+
       'animation-duration:'+(16+Math.random()*14).toFixed(1)+'s;'+
       'animation-delay:'+(Math.random()*18).toFixed(1)+'s"></div>';
  }
  for(i=0;i<(reduce?10:34);i++){
    var m=['','g','p'][i%3];
    h+='<div class="cr-mote '+m+'" style="left:'+(2+Math.random()*96).toFixed(1)+'%;'+
       'top:'+(4+Math.random()*92).toFixed(1)+'%;'+
       'animation-delay:'+(Math.random()*5).toFixed(2)+'s"></div>';
  }
  f.innerHTML=h;
})();
''',
  },
  'alien': {
    "css": r'''
  /* ── THE SAUCER: hovering top-center, blinking lights ── */
  .al-ufo { position:fixed; top:10px; left:50%; transform:translateX(-50%); z-index:52; pointer-events:none;
    width:120px; height:44px; animation:alHover 4.5s ease-in-out infinite; }

  .al-ufo .dome { position:absolute; top:0; left:50%; transform:translateX(-50%);
    width:52px; height:30px; border-radius:26px 26px 4px 4px;
    background:linear-gradient(180deg, rgba(125,255,234,0.85), rgba(77,255,230,0.25));
    box-shadow:0 0 16px rgba(77,255,230,0.6), inset 0 4px 8px rgba(255,255,255,0.5); }

  .al-ufo .hull { position:absolute; top:20px; left:0; width:120px; height:24px; border-radius:50%;
    background:linear-gradient(180deg, #b8c9c2, #5e6f68 55%, #2e3a34);
    box-shadow:0 6px 18px rgba(0,0,0,0.55), inset 0 2px 4px rgba(255,255,255,0.5); }

  .al-ufo .lite { position:absolute; top:29px; width:8px; height:8px; border-radius:50%;
    background:#eaff5c; box-shadow:0 0 10px rgba(234,255,92,0.95);
    animation:alBlink 1.2s steps(1) infinite; }

  .al-ufo .lite.l1 { left:14px; }
 .al-ufo .lite.l2 { left:41px; animation-delay:0.3s; }

  .al-ufo .lite.l3 { left:69px; animation-delay:0.6s; }
 .al-ufo .lite.l4 { left:97px; animation-delay:0.9s; }


  /* ── TRACTOR BEAM: cone sweeping beneath the saucer ── */
  .al-beam { position:fixed; top:52px; left:50%; z-index:1; pointer-events:none;
    width:280px; height:46vh; transform:translateX(-50%);
    background:linear-gradient(180deg, rgba(77,255,230,0.32), rgba(82,255,110,0.10) 60%, transparent);
    clip-path:polygon(44% 0, 56% 0, 100% 100%, 0 100%);
    animation:alBeamPulse 3.2s ease-in-out infinite, alBeamSweep 11s ease-in-out infinite;
    filter:blur(1px); }


  /* ── ABDUCTEES: things rising up the beam into the saucer ── */
  .al-up { position:fixed; left:50%; z-index:2; pointer-events:none; font-size:1.7rem; opacity:0;
    animation:alAbduct 18s ease-in infinite; filter:drop-shadow(0 0 10px rgba(77,255,230,0.7)); }

  .al-up.u2 { animation-delay:6s; font-size:1.5rem; }

  .al-up.u3 { animation-delay:12s; font-size:1.4rem; }


  /* ── alien glyph rain columns ── */
  .al-glyphs { position:fixed; top:-4%; z-index:1; pointer-events:none;
    font-family:'Space Mono', monospace; font-size:0.8rem; line-height:1.6; letter-spacing:0.1em;
    color:rgba(82,255,110,0.5); text-shadow:0 0 6px rgba(82,255,110,0.6);
    writing-mode:vertical-rl; text-orientation:upright; opacity:0;
    animation:alRain linear infinite; }

  .al-glyphs.r1 { left:5%;  animation-duration:14s; }

  .al-glyphs.r2 { left:26%; animation-duration:19s; animation-delay:5s;  font-size:0.65rem; }

  .al-glyphs.r3 { left:72%; animation-duration:16s; animation-delay:9s; }

  .al-glyphs.r4 { left:93%; animation-duration:21s; animation-delay:2s;  font-size:0.65rem; }


  /* ── little scout saucers crossing in the distance ── */
  .al-scout { position:fixed; z-index:1; pointer-events:none; font-size:1.1rem; opacity:0;
    animation:alScout linear infinite; filter:drop-shadow(0 0 8px rgba(77,255,230,0.6)); }

  .al-scout.s2 { animation-delay:10s; animation-duration:26s; font-size:0.85rem; }

  .al-scout { animation-duration:20s; }


  /* ── radar ping, bottom-left ── */
  .al-radar { position:fixed; bottom:1rem; left:1rem; z-index:51; pointer-events:none;
    width:64px; height:64px; border-radius:50%;
    border:1px solid rgba(82,255,110,0.5);
    background:radial-gradient(circle, rgba(82,255,110,0.10), transparent 70%); }

  .al-radar::before { /* sweep arm */
    content:''; position:absolute; inset:0; border-radius:50%;
    background:conic-gradient(from 0deg, rgba(82,255,110,0.55) 0 18deg, transparent 60deg 360deg);
    animation:alSweep 3s linear infinite; }

  .al-radar::after { /* expanding ping */
    content:''; position:absolute; inset:0; border-radius:50%;
    border:1px solid rgba(82,255,110,0.7);
    animation:alPing 3s ease-out infinite; }


  /* ── interference band sweeping the page now and then ── */
  .al-interfere { position:fixed; left:0; right:0; height:9vh; z-index:53; pointer-events:none; opacity:0;
    background:repeating-linear-gradient(0deg, rgba(82,255,110,0.10) 0 2px, transparent 2px 5px);
    mix-blend-mode:screen; animation:alStatic 13s linear infinite; }


  /* ── return to earth ── */
  .al-return { position:fixed; bottom:1.1rem; right:1.1rem; z-index:60; text-decoration:none;
    display:flex; align-items:center; gap:0.5rem;
    font-family:'VT323', monospace; font-size:1.05rem; letter-spacing:0.08em; color:#fff;
    background:rgba(4,20,12,0.88); border:1.5px solid #52ff6e; border-radius:999px;
    padding:0.45rem 0.95rem; box-shadow:0 0 18px rgba(82,255,110,0.5);
    transition:box-shadow .2s ease, transform .2s ease; }

  .al-return:hover { transform:translateY(-2px); box-shadow:0 0 30px rgba(77,255,230,0.85); border-color:#4dffe6; }

  .al-return .ic { font-size:1.25rem; animation:alWobble 3s ease-in-out infinite; display:inline-block; }
@media (max-width:600px){
    .al-ufo { width:88px; } .al-ufo .hull { width:88px; }
    .al-ufo .lite.l3 { left:52px; } .al-ufo .lite.l4 { left:72px; }
    .al-beam { width:190px; }
    .al-glyphs.r2, .al-glyphs.r4 { display:none; }
    .al-radar { width:46px; height:46px; }}
@media (prefers-reduced-motion: reduce){
    .al-ufo,.al-ufo .lite,.al-beam,.al-up,.al-glyphs,.al-scout,.al-radar::before,.al-radar::after,.al-interfere,.al-return .ic { animation:none !important; }
    .al-up,.al-glyphs,.al-scout,.al-interfere { display:none; }}

  @keyframes alHover { 0%,100% { transform:translateX(-50%) translateY(0); } 50% { transform:translateX(-52%) translateY(6px); } }

  @keyframes alBlink { 0%,49% { opacity:1; } 50%,100% { opacity:0.25; } }

  @keyframes alBeamPulse { 0%,100% { opacity:0.55; } 50% { opacity:0.95; } }

  @keyframes alBeamSweep { 0%,100% { transform:translateX(-50%) rotate(0deg); }
    25% { transform:translateX(-54%) rotate(-3deg); } 75% { transform:translateX(-46%) rotate(3deg); } }

  @keyframes alAbduct {
    0%,55% { opacity:0; top:calc(52px + 44vh); transform:translateX(-50%) rotate(0deg) scale(1); }
    57% { opacity:0.95; }
    70% { transform:translateX(-46%) rotate(140deg) scale(0.85); }
    84% { opacity:0.95; transform:translateX(-53%) rotate(290deg) scale(0.5); }
    88%,100% { opacity:0; top:64px; transform:translateX(-50%) rotate(380deg) scale(0.2); }
  }

  @keyframes alRain {
    0% { opacity:0; transform:translateY(-30%); }
    8% { opacity:0.7; } 88% { opacity:0.7; }
    100% { opacity:0; transform:translateY(110vh); }
  }

  @keyframes alScout {
    0%   { opacity:0; left:-5%; top:70%; transform:rotate(-8deg); }
    8%   { opacity:0.6; }
    50%  { top:56%; transform:rotate(6deg); }
    92%  { opacity:0.6; }
    100% { opacity:0; left:104%; top:64%; transform:rotate(-4deg); }
  }

  @keyframes alSweep { to { transform:rotate(360deg); } }

  @keyframes alPing { 0% { transform:scale(0.2); opacity:1; } 100% { transform:scale(1.25); opacity:0; } }

  @keyframes alStatic {
    0%,86% { opacity:0; top:-10%; }
    87% { opacity:0.9; top:-10%; }
    96% { opacity:0.9; top:104%; }
    97%,100% { opacity:0; top:104%; }
  }

  @keyframes alWobble { 0%,100% { transform:translateY(0) rotate(-6deg); } 50% { transform:translateY(-4px) rotate(8deg); } }''',
    "html": r'''<div class="al-ufo" aria-hidden="true">
  <span class="dome"></span><span class="hull"></span>
  <span class="lite l1"></span><span class="lite l2"></span><span class="lite l3"></span><span class="lite l4"></span>
</div>
<div class="al-beam" aria-hidden="true"></div>
<span class="al-up"    aria-hidden="true">🐄</span>
<span class="al-up u2" aria-hidden="true">📺</span>
<span class="al-up u3" aria-hidden="true">🌵</span>
<div class="al-glyphs r1" aria-hidden="true">⏃⎅⏚⋔☌⟒⌰⍜⋏⏁⟟⎐</div>
<div class="al-glyphs r2" aria-hidden="true">⍀⏁⟒⋔⍜⎅⏃⌰⟟⋏☌⎐</div>
<div class="al-glyphs r3" aria-hidden="true">⌰⟟⋏⏃☌⟒⎅⋔⍜⏚⎐⏁</div>
<div class="al-glyphs r4" aria-hidden="true">⋔⍜⏚⟒⏃⌰☌⟟⎅⏁⎐⋏</div>
<span class="al-scout"    aria-hidden="true">🛸</span>
<span class="al-scout s2" aria-hidden="true">🛸</span>
<div class="al-radar" aria-hidden="true"></div>
<div class="al-interfere" aria-hidden="true"></div>
<a class="al-return" href="index.html" title="Return to Earth"><span class="ic">🛸</span> Return to Earth</a>''',
    "js": "",
  },
  'arcade': {
    "css": r'''
  /* CRT scanline sheen */
  .ar-crt { position:fixed; inset:0; z-index:53; pointer-events:none; opacity:0.22;
    background:repeating-linear-gradient(0deg, rgba(0,0,0,0.35) 0 1px, transparent 1px 3px); }


  /* INSERT COIN blinking, top-center */
  .ar-insert { position:fixed; top:12px; left:50%; transform:translateX(-50%); z-index:54; pointer-events:none;
    font-family:'VT323', monospace; font-size:1.25rem; letter-spacing:0.3em; color:#ffcc00;
    text-shadow:0 0 12px rgba(255,204,0,0.9), 2px 2px 0 rgba(255,32,121,0.6);
    animation:arBlink 1.1s steps(1) infinite; }


  /* lives, top-left */
  .ar-lives { position:fixed; top:12px; left:14px; z-index:54; pointer-events:none;
    font-family:'VT323', monospace; font-size:1.1rem; letter-spacing:0.2em; color:#ff2079;
    text-shadow:0 0 10px rgba(255,32,121,0.8); }

  .ar-lives .low { animation:arBlink 0.8s steps(1) infinite; }


  /* live score, top-right */
  .ar-score { position:fixed; top:12px; right:14px; z-index:54; pointer-events:none; text-align:right;
    font-family:'VT323', monospace; line-height:1.2; }

  .ar-score .hi { font-size:0.8rem; letter-spacing:0.2em; color:#00e5ff; text-shadow:0 0 8px rgba(0,229,255,0.8); }

  .ar-score .p1 { font-size:1.15rem; letter-spacing:0.18em; color:#39ff14; text-shadow:0 0 10px rgba(57,255,20,0.8); }


  /* PONG: ball ricocheting around the viewport + two paddles */
  .ar-ball { position:fixed; width:12px; height:12px; z-index:2; pointer-events:none; background:#fff;
    box-shadow:0 0 12px rgba(255,255,255,0.9);
    animation:arBallX 7.3s linear infinite alternate, arBallY 5.1s linear infinite alternate; }

  .ar-paddle { position:fixed; width:9px; height:74px; z-index:2; pointer-events:none;
    border-radius:3px; }

  .ar-paddle.pl { left:8px; background:#ff2079; box-shadow:0 0 14px rgba(255,32,121,0.8);
    animation:arPaddle 5.1s linear infinite alternate; }

  .ar-paddle.pr { right:8px; background:#00e5ff; box-shadow:0 0 14px rgba(0,229,255,0.8);
    animation:arPaddle 5.1s linear infinite alternate-reverse; }


  /* pixel invaders marching across (box-shadow sprite) */
  .ar-invader { position:fixed; z-index:1; pointer-events:none; width:4px; height:4px; opacity:0;
    background:transparent; animation:arMarch linear infinite, arHop 0.6s steps(1) infinite; color:#39ff14;
    box-shadow:
      8px 0 0 currentColor, 16px 0 0 currentColor,
      4px 4px 0 currentColor, 8px 4px 0 currentColor, 12px 4px 0 currentColor, 16px 4px 0 currentColor, 20px 4px 0 currentColor,
      0 8px 0 currentColor, 4px 8px 0 currentColor, 12px 8px 0 currentColor, 20px 8px 0 currentColor, 24px 8px 0 currentColor,
      0 12px 0 currentColor, 8px 12px 0 currentColor, 16px 12px 0 currentColor, 24px 12px 0 currentColor,
      4px 16px 0 currentColor, 20px 16px 0 currentColor;
    filter:drop-shadow(0 0 6px rgba(57,255,20,0.6)); }

  .ar-invader.i2 { color:#a45cff; animation-delay:9s, 0.3s; top:24% !important;
    filter:drop-shadow(0 0 6px rgba(164,92,255,0.6)); }

  .ar-invader { animation-duration:22s, 0.6s; top:16%; }

  .ar-invader.i2 { animation-duration:28s, 0.6s; }


  /* coins popping up with +100 */
  .ar-coin { position:fixed; z-index:2; pointer-events:none; font-size:1.2rem; opacity:0;
    animation:arCoin 8s ease-out infinite; filter:drop-shadow(0 0 10px rgba(255,204,0,0.8)); }

  .ar-coin::after { content:'+100'; position:absolute; top:-16px; left:14px;
    font-family:'VT323', monospace; font-size:0.85rem; color:#ffcc00; text-shadow:0 0 8px rgba(255,204,0,0.9); }

  .ar-coin.c1 { left:22%; bottom:18%; }

  .ar-coin.c2 { left:58%; bottom:26%; animation-delay:2.7s; }

  .ar-coin.c3 { left:82%; bottom:14%; animation-delay:5.4s; }


  /* warp home */
  .ar-return { position:fixed; bottom:1.1rem; right:1.1rem; z-index:60; text-decoration:none;
    display:flex; align-items:center; gap:0.5rem;
    font-family:'VT323', monospace; font-size:1.05rem; letter-spacing:0.08em; color:#fff;
    background:rgba(6,6,22,0.9); border:1.5px solid #39ff14; border-radius:999px;
    padding:0.45rem 0.95rem; box-shadow:0 0 18px rgba(57,255,20,0.5);
    transition:box-shadow .2s ease, transform .2s ease; }

  .ar-return:hover { transform:translateY(-2px); box-shadow:0 0 30px rgba(255,204,0,0.85); border-color:#ffcc00; }

  .ar-return .ic { font-size:1.25rem; animation:arJoy 2.2s ease-in-out infinite; display:inline-block; }
@media (max-width:600px){
    .ar-insert { font-size:0.95rem; } .ar-paddle { height:52px; }
    .ar-invader.i2 { display:none; } .ar-lives { top:34px; }}
@media (prefers-reduced-motion: reduce){
    .ar-insert,.ar-lives .low,.ar-ball,.ar-paddle,.ar-invader,.ar-coin,.ar-return .ic { animation:none !important; }
    .ar-ball,.ar-paddle,.ar-invader,.ar-coin { display:none; }}

  @keyframes arBlink { 0%,55% { opacity:1; } 56%,100% { opacity:0.12; } }

  @keyframes arBallX { 0% { left:3%; } 100% { left:calc(97% - 12px); } }

  @keyframes arBallY { 0% { top:8%; } 100% { top:calc(92% - 12px); } }

  @keyframes arPaddle { 0% { top:10%; } 100% { top:calc(86% - 74px); } }

  @keyframes arMarch {
    0% { opacity:0; left:-4%; } 6% { opacity:0.8; } 94% { opacity:0.8; } 100% { opacity:0; left:103%; } }

  @keyframes arHop { 0%,49% { margin-top:0; } 50%,100% { margin-top:5px; } }

  @keyframes arCoin {
    0%,74% { opacity:0; transform:translateY(0) rotateY(0deg); }
    76% { opacity:1; }
    88% { opacity:1; transform:translateY(-46px) rotateY(540deg); }
    96%,100% { opacity:0; transform:translateY(-70px) rotateY(720deg); } }

  @keyframes arJoy { 0%,100% { transform:rotate(-10deg); } 50% { transform:rotate(12deg); } }''',
    "html": r'''<div class="ar-crt" aria-hidden="true"></div>
<div class="ar-insert" aria-hidden="true">INSERT COIN</div>
<div class="ar-lives" aria-hidden="true">♥ ♥ <span class="low">♥</span></div>
<div class="ar-score" aria-hidden="true">
  <div class="hi">HI-SCORE 999999</div>
  <div class="p1" id="ar-p1">1UP 000000</div>
</div>
<span class="ar-ball" aria-hidden="true"></span>
<span class="ar-paddle pl" aria-hidden="true"></span>
<span class="ar-paddle pr" aria-hidden="true"></span>
<span class="ar-invader" aria-hidden="true"></span>
<span class="ar-invader i2" aria-hidden="true"></span>
<span class="ar-coin c1" aria-hidden="true">🪙</span>
<span class="ar-coin c2" aria-hidden="true">🪙</span>
<span class="ar-coin c3" aria-hidden="true">🪙</span>
<a class="ar-return" href="index.html" title="Warp back to the home frequency"><span class="ic">🕹️</span> Warp to Home Frequency</a>''',
    "js": "",
  },
  'candy': {
    "css": r'''
  /* ── candy-stripe barber bar across the very top ── */
  .cd-stripe { position:fixed; top:0; left:0; right:0; height:8px; z-index:52; pointer-events:none;
    background:repeating-linear-gradient(115deg, #ff4fb8 0 14px, #fff 14px 28px, #3dffd6 28px 42px, #fff 42px 56px, #ffd93b 56px 70px, #fff 70px 84px);
    background-size:84px 100%; animation:cdStripe 2.5s linear infinite;
    box-shadow:0 2px 12px rgba(255,79,184,0.4); }


  /* ── the time portal: a spinning lollipop swirl in the corner ── */
  .cd-portal { position:fixed; top:-80px; left:-80px; width:260px; height:260px; z-index:1; pointer-events:none;
    border-radius:50%; opacity:0.5;
    background:conic-gradient(from 0deg,
      #ff4fb8 0 30deg, #2a0d45 30deg 60deg, #3dffd6 60deg 90deg, #2a0d45 90deg 120deg,
      #ffd93b 120deg 150deg, #2a0d45 150deg 180deg, #ff4fb8 180deg 210deg, #2a0d45 210deg 240deg,
      #c47dff 240deg 270deg, #2a0d45 270deg 300deg, #3dffd6 300deg 330deg, #2a0d45 330deg 360deg);
    -webkit-mask:radial-gradient(circle, transparent 18%, #000 19% 62%, transparent 70%);
    mask:radial-gradient(circle, transparent 18%, #000 19% 62%, transparent 70%);
    animation:cdSpin 14s linear infinite;
    filter:blur(1px) drop-shadow(0 0 30px rgba(255,79,184,0.5)); }


  /* ── giant faint clock face turning behind everything ── */
  .cd-clockbg { position:fixed; bottom:-160px; right:-160px; width:440px; height:440px; z-index:0; pointer-events:none;
    border-radius:50%; border:2px dashed rgba(255,217,59,0.14); opacity:0.8;
    animation:cdSpin 60s linear infinite reverse; }

  .cd-clockbg::before { content:''; position:absolute; top:50%; left:50%; width:42%; height:2px;
    background:rgba(255,217,59,0.16); transform-origin:left center; animation:cdSpin 12s linear infinite; }

  .cd-clockbg::after { content:''; position:absolute; top:50%; left:50%; width:30%; height:2px;
    background:rgba(61,255,214,0.16); transform-origin:left center; animation:cdSpin 45s linear infinite; }


  /* ── falling candy tumbling through time ── */
  .cd-drop { position:fixed; top:-8%; z-index:1; pointer-events:none; opacity:0;
    animation:cdFall linear infinite; filter:drop-shadow(0 2px 6px rgba(0,0,0,0.4)); }

  .cd-drop.d1 { left:9%;  font-size:1.4rem; animation-duration:13s; }

  .cd-drop.d2 { left:24%; font-size:1.1rem; animation-duration:17s; animation-delay:4s; }

  .cd-drop.d3 { left:41%; font-size:1.6rem; animation-duration:15s; animation-delay:8s; }

  .cd-drop.d4 { left:58%; font-size:1.2rem; animation-duration:19s; animation-delay:2s; }

  .cd-drop.d5 { left:74%; font-size:1.5rem; animation-duration:14s; animation-delay:10s; }

  .cd-drop.d6 { left:90%; font-size:1.2rem; animation-duration:18s; animation-delay:6s; }


  /* ── clocks drifting sideways through the stream ── */
  .cd-clock { position:fixed; z-index:1; pointer-events:none; opacity:0;
    animation:cdDrift linear infinite; filter:drop-shadow(0 0 12px rgba(255,217,59,0.45)); }

  .cd-clock.c1 { font-size:1.6rem; animation-duration:28s; }

  .cd-clock.c2 { font-size:1.2rem; animation-duration:36s; animation-delay:12s; }

  .cd-clock.c3 { font-size:1.9rem; animation-duration:32s; animation-delay:21s; }


  /* ── THE GOLDEN TICKET: shimmers across the sky once in a while ── */
  .cd-ticket { position:fixed; z-index:51; pointer-events:none; opacity:0;
    width:88px; height:44px; border-radius:6px;
    background:linear-gradient(120deg, #b8860b, #ffd93b 35%, #fff6c9 50%, #ffd93b 65%, #b8860b);
    background-size:220% 100%;
    border:2px dashed rgba(120,80,0,0.55);
    box-shadow:0 0 22px rgba(255,217,59,0.8), 0 4px 12px rgba(0,0,0,0.45);
    display:flex; align-items:center; justify-content:center;
    font-family:'VT323', monospace; font-size:0.72rem; letter-spacing:0.14em; color:#4a3000;
    animation:cdTicket 24s ease-in-out infinite, cdShine 2.2s linear infinite; }


  /* ── gumballs bouncing along the bottom ── */
  .cd-gum { position:fixed; bottom:8px; z-index:2; pointer-events:none; border-radius:50%;
    background:radial-gradient(circle at 32% 28%, #fff 4%, var(--g) 20%, color-mix(in srgb, var(--g) 55%, #000) 100%);
    box-shadow:0 3px 8px rgba(0,0,0,0.45); animation:cdBounce ease-in-out infinite; }

  .cd-gum.g1 { --g:#ff4fb8; left:12%; width:16px; height:16px; animation-duration:1.7s; }

  .cd-gum.g2 { --g:#3dffd6; left:34%; width:12px; height:12px; animation-duration:2.1s; animation-delay:0.4s; }

  .cd-gum.g3 { --g:#ffd93b; left:57%; width:18px; height:18px; animation-duration:1.9s; animation-delay:0.9s; }

  .cd-gum.g4 { --g:#c47dff; left:79%; width:13px; height:13px; animation-duration:2.3s; animation-delay:0.2s; }


  /* ── sugar sparkle time-dust ── */
  .cd-dust { position:fixed; z-index:1; pointer-events:none; font-size:0.7rem; opacity:0;
    animation:cdTwinkleDust ease-in-out infinite; color:#fff6c9;
    text-shadow:0 0 8px rgba(255,217,59,0.9); }

  .cd-dust.s1 { left:18%; top:34%; animation-duration:4s; }

  .cd-dust.s2 { left:47%; top:20%; animation-duration:5.5s; animation-delay:1.5s; }

  .cd-dust.s3 { left:69%; top:44%; animation-duration:4.6s; animation-delay:3s; }

  .cd-dust.s4 { left:87%; top:28%; animation-duration:6s;   animation-delay:2.2s; }


  /* ── back to the present ── */
  .cd-return { position:fixed; bottom:1.1rem; right:1.1rem; z-index:60; text-decoration:none;
    display:flex; align-items:center; gap:0.5rem;
    font-family:'VT323', monospace; font-size:1.05rem; letter-spacing:0.08em; color:#fff;
    background:rgba(26,5,36,0.88); border:1.5px solid #ff4fb8; border-radius:999px;
    padding:0.45rem 0.95rem; box-shadow:0 0 18px rgba(255,79,184,0.5);
    transition:box-shadow .2s ease, transform .2s ease; }

  .cd-return:hover { transform:translateY(-2px); box-shadow:0 0 30px rgba(61,255,214,0.8); border-color:#3dffd6; }

  .cd-return .ic { font-size:1.25rem; animation:cdTick 2s steps(8) infinite; display:inline-block; }
@media (max-width:600px){
    .cd-portal { width:170px; height:170px; top:-55px; left:-55px; }
    .cd-clockbg { width:280px; height:280px; bottom:-110px; right:-110px; }
    .cd-gum { display:none; }}
@media (prefers-reduced-motion: reduce){
    .cd-stripe,.cd-portal,.cd-clockbg,.cd-clockbg::before,.cd-clockbg::after,.cd-drop,.cd-clock,.cd-ticket,.cd-gum,.cd-dust,.cd-return .ic { animation:none !important; }
    .cd-drop,.cd-clock,.cd-ticket,.cd-gum,.cd-dust { display:none; }}

  @keyframes cdStripe { to { background-position:84px 0; } }

  @keyframes cdSpin { to { transform:rotate(360deg); } }

  @keyframes cdFall {
    0%   { opacity:0; transform:translateY(0) rotate(0deg); }
    6%   { opacity:0.9; }
    50%  { transform:translateY(55vh) translateX(20px) rotate(190deg); }
    94%  { opacity:0.9; }
    100% { opacity:0; transform:translateY(112vh) translateX(-14px) rotate(370deg); }
  }

  @keyframes cdDrift {
    0%   { opacity:0; left:-5%; top:60%; transform:rotate(-12deg) scale(1); }
    7%   { opacity:0.55; }
    35%  { transform:rotate(10deg) scale(1.12); }
    65%  { transform:rotate(-8deg) scale(0.94); top:36%; }
    93%  { opacity:0.55; }
    100% { opacity:0; left:104%; top:50%; transform:rotate(6deg) scale(1); }
  }

  @keyframes cdShine { to { background-position:-220% 0; } }

  @keyframes cdTicket {
    0%,62% { opacity:0; left:-10%; top:26%; transform:rotate(-8deg) translateY(0); }
    64% { opacity:1; }
    72% { transform:rotate(6deg) translateY(-18px); }
    82% { transform:rotate(-5deg) translateY(8px); }
    94% { opacity:1; }
    100% { opacity:0; left:105%; top:18%; transform:rotate(4deg) translateY(-10px); }
  }

  @keyframes cdBounce {
    0%,100% { transform:translateY(0) scaleY(1); }
    12% { transform:translateY(2px) scaleY(0.82); }
    50% { transform:translateY(-46px) scaleY(1.06); }
    88% { transform:translateY(2px) scaleY(0.82); }
  }

  @keyframes cdTwinkleDust {
    0%,100% { opacity:0; transform:scale(0.6) rotate(0deg); }
    50% { opacity:0.9; transform:scale(1.2) rotate(45deg); }
  }

  @keyframes cdTick { to { transform:rotate(360deg); } }''',
    "html": r'''<div class="cd-stripe" aria-hidden="true"></div>
<div class="cd-portal" aria-hidden="true"></div>
<div class="cd-clockbg" aria-hidden="true"></div>
<span class="cd-drop d1" aria-hidden="true">🍬</span>
<span class="cd-drop d2" aria-hidden="true">🍭</span>
<span class="cd-drop d3" aria-hidden="true">🍫</span>
<span class="cd-drop d4" aria-hidden="true">🧁</span>
<span class="cd-drop d5" aria-hidden="true">🍬</span>
<span class="cd-drop d6" aria-hidden="true">🍩</span>
<span class="cd-clock c1" aria-hidden="true">🕰️</span>
<span class="cd-clock c2" aria-hidden="true">⏰</span>
<span class="cd-clock c3" aria-hidden="true">⌛</span>
<div class="cd-ticket" aria-hidden="true">GOLDEN&nbsp;TICKET</div>
<span class="cd-gum g1" aria-hidden="true"></span>
<span class="cd-gum g2" aria-hidden="true"></span>
<span class="cd-gum g3" aria-hidden="true"></span>
<span class="cd-gum g4" aria-hidden="true"></span>
<span class="cd-dust s1" aria-hidden="true">✦</span>
<span class="cd-dust s2" aria-hidden="true">✧</span>
<span class="cd-dust s3" aria-hidden="true">✦</span>
<span class="cd-dust s4" aria-hidden="true">✧</span>
<a class="cd-return" href="index.html" title="Return to the present timeline"><span class="ic">⏰</span> Back to the Present</a>''',
    "js": "",
  },
  'cottage': {
    "css": r'''
  /* flower garland swaying along the top */
  .ct-garland { position:fixed; top:2px; left:0; right:0; z-index:50; pointer-events:none;
    display:flex; justify-content:center; gap:clamp(0.5rem,2.6vw,1.4rem); font-size:1rem; }

  .ct-garland span { display:inline-block; animation:ctSway 5s ease-in-out infinite;
    filter:drop-shadow(0 2px 6px rgba(0,0,0,0.4)); transform-origin:top center; }

  .ct-garland span:nth-child(even) { animation-delay:1.2s; font-size:0.85rem; margin-top:6px; }

  .ct-garland span:nth-child(3n) { animation-delay:2.4s; }


  /* mushrooms sprouting along the bottom */
  .ct-shroom { position:fixed; bottom:0.4rem; z-index:2; pointer-events:none; font-size:1.4rem;
    animation:ctSprout 9s ease-in-out infinite; transform-origin:bottom center;
    filter:drop-shadow(0 0 8px rgba(232,137,158,0.5)); }

  .ct-shroom.m1 { left:8%; }
  .ct-shroom.m2 { left:27%; animation-delay:3s; font-size:1.1rem; }

  .ct-shroom.m3 { left:55%; animation-delay:6s; }
 .ct-shroom.m4 { left:78%; animation-delay:1.5s; font-size:1.2rem; }


  /* fireflies blinking + wandering at dusk */
  .ct-fly { position:fixed; z-index:1; pointer-events:none; width:6px; height:6px; border-radius:50%;
    background:radial-gradient(circle, #fff3b0, rgba(242,193,78,0.5) 60%, transparent);
    animation:ctWander ease-in-out infinite, ctBlink steps(1) infinite; }

  .ct-fly.y1 { left:16%; top:48%; animation-duration:12s, 2.1s; }

  .ct-fly.y2 { left:41%; top:32%; animation-duration:15s, 2.7s; animation-delay:3s, 0.8s; }

  .ct-fly.y3 { left:68%; top:56%; animation-duration:13s, 1.8s; animation-delay:6s, 1.4s; }

  .ct-fly.y4 { left:87%; top:38%; animation-duration:16s, 2.4s; animation-delay:1.5s, 0.3s; }


  /* butterflies fluttering across on wavy paths */
  .ct-butterfly { position:fixed; z-index:1; pointer-events:none; font-size:1.15rem; opacity:0;
    animation:ctFlutter linear infinite; filter:drop-shadow(0 2px 5px rgba(0,0,0,0.35)); }

  .ct-butterfly.bf2 { animation-delay:11s; animation-duration:31s; font-size:0.95rem; }

  .ct-butterfly { animation-duration:24s; }


  /* a bee zigzagging by */
  .ct-bee { position:fixed; z-index:1; pointer-events:none; font-size:0.95rem; opacity:0;
    animation:ctBee 17s linear infinite; animation-delay:5s; }


  /* petals drifting down */
  .ct-petal { position:fixed; top:-6%; z-index:1; pointer-events:none; opacity:0; font-size:1rem;
    animation:ctPetal linear infinite; }

  .ct-petal.p1 { left:20%; animation-duration:18s; }

  .ct-petal.p2 { left:47%; animation-duration:23s; animation-delay:7s; font-size:0.85rem; }

  .ct-petal.p3 { left:73%; animation-duration:20s; animation-delay:13s; }


  /* the kettle in the corner, always on */
  .ct-kettle { position:fixed; bottom:0.9rem; left:1rem; z-index:51; pointer-events:none; font-size:2.1rem;
    filter:drop-shadow(0 0 12px rgba(242,193,78,0.6)); animation:ctKettle 4s ease-in-out infinite; }

  .ct-steam { position:fixed; bottom:3.6rem; left:1.7rem; z-index:51; pointer-events:none; }

  .ct-steam i { position:absolute; bottom:0; width:7px; height:30px; border-radius:999px;
    background:linear-gradient(180deg, transparent, rgba(255,248,230,0.5), transparent);
    filter:blur(2.5px); opacity:0; animation:ctSteam 4s ease-in-out infinite; }

  .ct-steam i:nth-child(2) { left:8px; animation-delay:1.4s; height:38px; }

  .ct-steam i:nth-child(3) { left:-5px; animation-delay:2.7s; height:24px; }


  /* return to the cottage gate */
  .ct-return { position:fixed; bottom:1.1rem; right:1.1rem; z-index:60; text-decoration:none;
    display:flex; align-items:center; gap:0.5rem;
    font-family:'VT323', monospace; font-size:1.05rem; letter-spacing:0.08em; color:#fff;
    background:rgba(23,28,13,0.88); border:1.5px solid #e8899e; border-radius:999px;
    padding:0.45rem 0.95rem; box-shadow:0 0 18px rgba(232,137,158,0.5);
    transition:box-shadow .2s ease, transform .2s ease; }

  .ct-return:hover { transform:translateY(-2px); box-shadow:0 0 30px rgba(242,193,78,0.85); border-color:#f2c14e; }

  .ct-return .ic { font-size:1.25rem; animation:ctBob 3.4s ease-in-out infinite; display:inline-block; }
@media (max-width:600px){ .ct-garland { font-size:0.8rem; } .ct-shroom.m2 { display:none; }}
@media (prefers-reduced-motion: reduce){
    .ct-garland span,.ct-shroom,.ct-fly,.ct-butterfly,.ct-bee,.ct-petal,.ct-kettle,.ct-steam i,.ct-return .ic { animation:none !important; }
    .ct-fly,.ct-butterfly,.ct-bee,.ct-petal,.ct-steam { display:none; }}

  @keyframes ctSway { 0%,100% { transform:rotate(-7deg); } 50% { transform:rotate(8deg); } }

  @keyframes ctSprout {
    0% { transform:scale(0.9); } 8% { transform:scale(1.08); } 14% { transform:scale(1); }
    50% { transform:scale(1) translateY(-2px); } 100% { transform:scale(0.9); } }

  @keyframes ctWander {
    0%,100% { transform:translate(0,0); } 25% { transform:translate(28px,-22px); }
    50% { transform:translate(-12px,-44px); } 75% { transform:translate(-30px,-14px); } }

  @keyframes ctBlink { 0%,55% { opacity:0.9; } 56%,100% { opacity:0.1; } }

  @keyframes ctFlutter {
    0%   { opacity:0; left:-4%; top:40%; transform:rotate(-12deg); }
    6%   { opacity:0.85; }
    20%  { top:30%; transform:rotate(10deg); }
    40%  { top:44%; transform:rotate(-10deg); }
    60%  { top:26%; transform:rotate(12deg); }
    80%  { top:38%; transform:rotate(-8deg); }
    94%  { opacity:0.85; }
    100% { opacity:0; left:104%; top:32%; transform:rotate(6deg); } }

  @keyframes ctBee {
    0%,60% { opacity:0; left:-4%; top:22%; }
    62% { opacity:0.9; }
    68% { top:18%; } 74% { top:26%; } 80% { top:16%; } 86% { top:24%; }
    96% { opacity:0.9; }
    100% { opacity:0; left:104%; top:20%; } }

  @keyframes ctPetal {
    0%   { opacity:0; transform:translateY(0) translateX(0) rotate(0deg); }
    7%   { opacity:0.75; }
    30%  { transform:translateY(30vh) translateX(-26px) rotate(120deg); }
    65%  { transform:translateY(68vh) translateX(20px) rotate(240deg); }
    93%  { opacity:0.75; }
    100% { opacity:0; transform:translateY(110vh) translateX(-8px) rotate(340deg); } }

  @keyframes ctKettle { 0%,86%,100% { transform:rotate(0deg); } 90% { transform:rotate(-4deg); } 94% { transform:rotate(3deg); } }

  @keyframes ctSteam {
    0% { opacity:0; transform:translateY(6px) rotate(0deg) scaleY(0.7); }
    28% { opacity:0.85; }
    100% { opacity:0; transform:translateY(-44px) rotate(10deg) scaleY(1.3); } }

  @keyframes ctBob { 0%,100% { transform:translateY(0) rotate(-4deg); } 50% { transform:translateY(-3px) rotate(5deg); } }''',
    "html": r'''<div class="ct-garland" aria-hidden="true">
  <span>🌿</span><span>🌼</span><span>🌿</span><span>🌷</span><span>🌿</span><span>🌼</span><span>🌿</span><span>🌸</span><span>🌿</span><span>🌼</span><span>🌿</span>
</div>
<span class="ct-shroom m1" aria-hidden="true">🍄</span>
<span class="ct-shroom m2" aria-hidden="true">🍄</span>
<span class="ct-shroom m3" aria-hidden="true">🍄</span>
<span class="ct-shroom m4" aria-hidden="true">🍄</span>
<span class="ct-fly y1" aria-hidden="true"></span>
<span class="ct-fly y2" aria-hidden="true"></span>
<span class="ct-fly y3" aria-hidden="true"></span>
<span class="ct-fly y4" aria-hidden="true"></span>
<span class="ct-butterfly" aria-hidden="true">🦋</span>
<span class="ct-butterfly bf2" aria-hidden="true">🦋</span>
<span class="ct-bee" aria-hidden="true">🐝</span>
<span class="ct-petal p1" aria-hidden="true">🌸</span>
<span class="ct-petal p2" aria-hidden="true">🌼</span>
<span class="ct-petal p3" aria-hidden="true">🌸</span>
<span class="ct-kettle" aria-hidden="true">🫖</span>
<div class="ct-steam" aria-hidden="true"><i></i><i></i><i></i></div>
<a class="ct-return" href="index.html" title="Back through the garden gate"><span class="ic">🍄</span> Back Through the Garden Gate</a>''',
    "js": "",
  },
  'dream': {
    "css": r'''
  /* sleepy moon with soft halo */
  .dr-moon { position:fixed; top:26px; right:5%; z-index:1; pointer-events:none; font-size:3.2rem;
    filter:drop-shadow(0 0 24px rgba(255,233,176,0.7)); animation:drMoon 9s ease-in-out infinite; }


  /* soft clouds drifting at different depths */
  .dr-cloud { position:fixed; z-index:1; pointer-events:none; opacity:0; filter:blur(4px);
    background:radial-gradient(ellipse, rgba(212,184,255,0.30), transparent 70%);
    border-radius:50%; animation:drCloud linear infinite; }

  .dr-cloud.c1 { width:220px; height:70px; top:16%; animation-duration:46s; }

  .dr-cloud.c2 { width:150px; height:50px; top:38%; animation-duration:62s; animation-delay:18s;
    background:radial-gradient(ellipse, rgba(168,216,255,0.28), transparent 70%); }

  .dr-cloud.c3 { width:280px; height:86px; top:62%; animation-duration:54s; animation-delay:32s;
    background:radial-gradient(ellipse, rgba(255,168,217,0.22), transparent 70%); }


  /* counting sheep: hop across in little arcs */
  .dr-sheep { position:fixed; bottom:14%; z-index:2; pointer-events:none; font-size:1.6rem; opacity:0;
    animation:drSheep 17s linear infinite; filter:drop-shadow(0 3px 8px rgba(0,0,0,0.4)); }

  .dr-sheep.s2 { animation-delay:8.5s; font-size:1.3rem; }


  /* Zzz's rising and fading */
  .dr-zzz { position:fixed; z-index:1; pointer-events:none; opacity:0;
    font-family:'Dancing Script', cursive, 'VT323', monospace; color:#c2e8ff;
    text-shadow:0 0 10px rgba(168,216,255,0.7); animation:drZzz ease-out infinite; }

  .dr-zzz.z1 { left:18%; bottom:20%; font-size:1.3rem; animation-duration:6s; }

  .dr-zzz.z2 { left:48%; bottom:30%; font-size:1rem;   animation-duration:8s; animation-delay:2.5s; }

  .dr-zzz.z3 { left:76%; bottom:24%; font-size:1.6rem; animation-duration:7s; animation-delay:5s; }


  /* pastel bokeh dream-orbs breathing */
  .dr-orb { position:fixed; z-index:1; pointer-events:none; border-radius:50%; filter:blur(3px);
    animation:drOrb ease-in-out infinite; }

  .dr-orb.o1 { left:10%; top:46%; width:20px; height:20px; animation-duration:9s;
    background:radial-gradient(circle, rgba(255,168,217,0.7), transparent 70%); }

  .dr-orb.o2 { left:34%; top:24%; width:13px; height:13px; animation-duration:12s; animation-delay:3s;
    background:radial-gradient(circle, rgba(168,216,255,0.7), transparent 70%); }

  .dr-orb.o3 { left:62%; top:52%; width:24px; height:24px; animation-duration:10s; animation-delay:6s;
    background:radial-gradient(circle, rgba(255,233,176,0.6), transparent 70%); }

  .dr-orb.o4 { left:88%; top:34%; width:15px; height:15px; animation-duration:13s; animation-delay:1.5s;
    background:radial-gradient(circle, rgba(212,184,255,0.7), transparent 70%); }


  /* feathers drifting down */
  .dr-feather { position:fixed; top:-8%; z-index:1; pointer-events:none; opacity:0; font-size:1.15rem;
    animation:drFeather linear infinite; filter:drop-shadow(0 0 8px rgba(255,255,255,0.35)); }

  .dr-feather.fe1 { left:28%; animation-duration:23s; }

  .dr-feather.fe2 { left:57%; animation-duration:29s; animation-delay:9s; }

  .dr-feather.fe3 { left:81%; animation-duration:26s; animation-delay:17s; }


  /* a wishing star that streaks by softly */
  .dr-wish { position:fixed; z-index:1; pointer-events:none; width:100px; height:1.5px; opacity:0;
    background:linear-gradient(90deg, transparent, #fff8e0, transparent);
    filter:drop-shadow(0 0 8px rgba(255,233,176,0.9)); transform:rotate(-20deg);
    animation:drWish 21s linear infinite; }


  /* wake up button */
  .dr-return { position:fixed; bottom:1.1rem; right:1.1rem; z-index:60; text-decoration:none;
    display:flex; align-items:center; gap:0.5rem;
    font-family:'VT323', monospace; font-size:1.05rem; letter-spacing:0.08em; color:#fff;
    background:rgba(18,12,38,0.88); border:1.5px solid #ffa8d9; border-radius:999px;
    padding:0.45rem 0.95rem; box-shadow:0 0 18px rgba(255,168,217,0.5);
    transition:box-shadow .2s ease, transform .2s ease; }

  .dr-return:hover { transform:translateY(-2px); box-shadow:0 0 30px rgba(255,233,176,0.85); border-color:#ffe9b0; }

  .dr-return .ic { font-size:1.25rem; animation:drSun 5s ease-in-out infinite; display:inline-block; }
@media (max-width:600px){ .dr-moon { font-size:2.3rem; } .dr-cloud.c3 { display:none; }}
@media (prefers-reduced-motion: reduce){
    .dr-moon,.dr-cloud,.dr-sheep,.dr-zzz,.dr-orb,.dr-feather,.dr-wish,.dr-return .ic { animation:none !important; }
    .dr-cloud,.dr-sheep,.dr-zzz,.dr-feather,.dr-wish { display:none; }}

  @keyframes drift {
    0%   { transform: translateY(100vh) rotate(0deg); opacity: 0; }
    5%   { opacity: 1; }
    95%  { opacity: 0.3; }
    100% { transform: translateY(-30px) rotate(540deg); opacity: 0; }
  }

  @keyframes drMoon { 0%,100% { transform:translateY(0) rotate(-6deg); } 50% { transform:translateY(-8px) rotate(4deg); } }

  @keyframes drCloud {
    0% { opacity:0; left:-24%; } 8% { opacity:1; } 92% { opacity:1; } 100% { opacity:0; left:104%; } }

  @keyframes drSheep {
    0%,55% { opacity:0; left:-6%; transform:scaleX(-1) translateY(0); }
    57% { opacity:0.9; }
    62% { transform:scaleX(-1) translateY(-34px); }
    67% { transform:scaleX(-1) translateY(0); }
    72% { transform:scaleX(-1) translateY(-34px); }
    77% { transform:scaleX(-1) translateY(0); }
    82% { transform:scaleX(-1) translateY(-34px); }
    87% { transform:scaleX(-1) translateY(0); }
    96% { opacity:0.9; }
    100% { opacity:0; left:105%; transform:scaleX(-1) translateY(-10px); } }

  @keyframes drZzz {
    0% { opacity:0; transform:translateY(0) rotate(0deg) scale(0.8); }
    18% { opacity:0.85; }
    100% { opacity:0; transform:translateY(-120px) rotate(14deg) scale(1.25); } }

  @keyframes drOrb {
    0%,100% { transform:translate(0,0) scale(1); opacity:0.4; }
    50% { transform:translate(18px,-26px) scale(1.25); opacity:0.85; } }

  @keyframes drFeather {
    0%   { opacity:0; transform:translateY(0) translateX(0) rotate(0deg); }
    6%   { opacity:0.7; }
    25%  { transform:translateY(26vh) translateX(-34px) rotate(60deg); }
    50%  { transform:translateY(54vh) translateX(26px) rotate(-40deg); }
    75%  { transform:translateY(82vh) translateX(-28px) rotate(50deg); }
    94%  { opacity:0.7; }
    100% { opacity:0; transform:translateY(112vh) translateX(8px) rotate(-20deg); } }

  @keyframes drWish {
    0%,80% { opacity:0; left:-10%; top:14%; } 81% { opacity:1; }
    92% { opacity:1; left:70%; top:36%; } 93%,100% { opacity:0; left:70%; top:36%; } }

  @keyframes drSun { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-3px) rotate(8deg); } }''',
    "html": r'''<span class="dr-moon" aria-hidden="true">🌙</span>
<div class="dr-cloud c1" aria-hidden="true"></div>
<div class="dr-cloud c2" aria-hidden="true"></div>
<div class="dr-cloud c3" aria-hidden="true"></div>
<span class="dr-sheep" aria-hidden="true">🐑</span>
<span class="dr-sheep s2" aria-hidden="true">🐑</span>
<span class="dr-zzz z1" aria-hidden="true">z z Z</span>
<span class="dr-zzz z2" aria-hidden="true">z Z</span>
<span class="dr-zzz z3" aria-hidden="true">Z z z</span>
<span class="dr-orb o1" aria-hidden="true"></span>
<span class="dr-orb o2" aria-hidden="true"></span>
<span class="dr-orb o3" aria-hidden="true"></span>
<span class="dr-orb o4" aria-hidden="true"></span>
<span class="dr-feather fe1" aria-hidden="true">🪶</span>
<span class="dr-feather fe2" aria-hidden="true">🪶</span>
<span class="dr-feather fe3" aria-hidden="true">🪶</span>
<div class="dr-wish" aria-hidden="true"></div>
<a class="dr-return" href="index.html" title="Wake up and return home"><span class="ic">🌅</span> Wake Up · Home Frequency</a>''',
    "js": "",
  },
  'fall': {
    "css": r'''
  /* ── string of warm café lights along the top ── */
  .fl-lights { position:fixed; top:0; left:0; right:0; height:26px; z-index:50; pointer-events:none; }

  .fl-lights::before { /* the wire */
    content:''; position:absolute; left:-2%; right:-2%; top:6px; height:14px;
    border-bottom:1.5px solid rgba(255,223,174,0.25); border-radius:0 0 100% 100%;
  }

  .fl-lights span {
    position:absolute; top:16px; width:7px; height:9px; border-radius:50% 50% 55% 55%;
    background:radial-gradient(circle at 40% 30%, #fff4d8, #ffb347 65%, #e0454f);
    box-shadow:0 0 10px rgba(255,179,71,0.8), 0 0 18px rgba(255,179,71,0.4);
    animation:flGlow 2.8s ease-in-out infinite;
  }

  .fl-lights span:nth-child(odd) { animation-delay:1.4s; }

  .fl-lights span:nth-child(3n) { animation-delay:0.7s; }


  /* ── steaming mug tucked in the corner ── */
  .fl-mug { position:fixed; bottom:1rem; left:1rem; z-index:51; pointer-events:none;
    font-size:2.4rem; filter:drop-shadow(0 4px 10px rgba(0,0,0,0.5)); }

  .fl-steam { position:fixed; bottom:3.4rem; left:1.55rem; z-index:51; pointer-events:none; }

  .fl-steam i {
    position:absolute; bottom:0; width:8px; height:26px; border-radius:999px;
    background:linear-gradient(180deg, transparent, rgba(255,232,200,0.55), transparent);
    filter:blur(2.5px); opacity:0; animation:flSteam 3.6s ease-in-out infinite;
  }

  .fl-steam i:nth-child(1) { left:0; }

  .fl-steam i:nth-child(2) { left:9px; animation-delay:1.2s; height:32px; }

  .fl-steam i:nth-child(3) { left:18px; animation-delay:2.3s; height:22px; }


  /* ── falling leaves, tumbling with sway ── */
  .fl-leaf { position:fixed; top:-8%; z-index:1; pointer-events:none; opacity:0;
    animation:flFall linear infinite; filter:drop-shadow(0 2px 6px rgba(0,0,0,0.35)); }

  .fl-leaf.l1 { left:6%;  font-size:1.5rem; animation-duration:12s; }

  .fl-leaf.l2 { left:20%; font-size:1.1rem; animation-duration:16s; animation-delay:3s; }

  .fl-leaf.l3 { left:37%; font-size:1.7rem; animation-duration:14s; animation-delay:7s; }

  .fl-leaf.l4 { left:55%; font-size:1.2rem; animation-duration:18s; animation-delay:1.5s; }

  .fl-leaf.l5 { left:72%; font-size:1.5rem; animation-duration:13s; animation-delay:9s; }

  .fl-leaf.l6 { left:88%; font-size:1.3rem; animation-duration:17s; animation-delay:5s; }

  .fl-leaf.l7 { left:47%; font-size:1rem;   animation-duration:21s; animation-delay:11s; }


  /* ── drifting cozy bits (mid-page, like the seasons before) ── */
  .fl-float { position:fixed; z-index:1; pointer-events:none; opacity:0;
    animation:flDrift linear infinite; filter:drop-shadow(0 0 10px rgba(255,179,71,0.35)); }

  .fl-float.f1 { font-size:1.5rem; animation-duration:30s; }

  .fl-float.f2 { font-size:1.2rem; animation-duration:37s; animation-delay:12s; }

  .fl-float.f3 { font-size:1.6rem; animation-duration:33s; animation-delay:22s; }


  /* ── maple branches leaning into top corners ── */
  .fl-branch { position:fixed; top:-12px; z-index:50; font-size:3.8rem; pointer-events:none;
    filter:drop-shadow(0 4px 10px rgba(0,0,0,0.45)); animation:flSway 7s ease-in-out infinite; transform-origin:top center; }

  .fl-branch.bl { left:-12px; transform:rotate(120deg); }

  .fl-branch.br { right:-12px; transform:rotate(-120deg) scaleX(-1); animation-delay:2s; }


  /* ── hearth glow breathing at the bottom ── */
  .fl-hearth { position:fixed; left:0; right:0; bottom:0; height:160px; z-index:1; pointer-events:none;
    background:linear-gradient(0deg, rgba(224,110,60,0.14), rgba(255,179,71,0.06) 50%, transparent);
    animation:flHearth 5s ease-in-out infinite; }


  /* ── warm dust motes floating in the light ── */
  .fl-mote { position:fixed; z-index:1; pointer-events:none; border-radius:50%;
    background:radial-gradient(circle, rgba(255,232,190,0.8), transparent 70%);
    animation:flMote ease-in-out infinite; }

  .fl-mote.m1 { left:14%; top:30%; width:5px; height:5px; animation-duration:9s; }

  .fl-mote.m2 { left:64%; top:22%; width:4px; height:4px; animation-duration:12s; animation-delay:3s; }

  .fl-mote.m3 { left:83%; top:48%; width:6px; height:6px; animation-duration:10s; animation-delay:6s; }


  /* ── back-to-main portal ── */
  .fl-return { position:fixed; bottom:1.1rem; right:1.1rem; z-index:60; text-decoration:none;
    display:flex; align-items:center; gap:0.5rem;
    font-family:'VT323', monospace; font-size:1.05rem; letter-spacing:0.08em; color:#fff;
    background:rgba(26,15,7,0.88); border:1.5px solid #ffb347; border-radius:999px;
    padding:0.45rem 0.95rem; box-shadow:0 0 18px rgba(255,179,71,0.45);
    transition:box-shadow .2s ease, transform .2s ease; }

  .fl-return:hover { transform:translateY(-2px); box-shadow:0 0 30px rgba(255,179,71,0.8); }

  .fl-return .ic { font-size:1.25rem; animation:flBob 3s ease-in-out infinite; display:inline-block; }
@media (max-width:600px){
    .fl-branch { font-size:2.6rem; }
    .fl-mug { font-size:1.9rem; }
    .fl-steam { bottom:2.9rem; left:1.4rem; }}
@media (prefers-reduced-motion: reduce){
    .fl-leaf,.fl-float,.fl-steam i,.fl-lights span,.fl-hearth,.fl-mote,.fl-branch,.fl-return .ic { animation:none !important; }
    .fl-leaf,.fl-float,.fl-steam,.fl-mote { display:none; }}

  @keyframes flGlow { 0%,100% { opacity:1; } 50% { opacity:0.45; } }

  @keyframes flSteam {
    0% { opacity:0; transform:translateY(6px) scaleY(0.7) rotate(0deg); }
    30% { opacity:0.9; }
    100% { opacity:0; transform:translateY(-34px) scaleY(1.25) rotate(8deg); }
  }

  @keyframes flFall {
    0%   { opacity:0; transform:translateY(0) translateX(0) rotate(0deg); }
    6%   { opacity:0.85; }
    25%  { transform:translateY(28vh) translateX(-28px) rotate(95deg); }
    50%  { transform:translateY(55vh) translateX(22px) rotate(200deg); }
    75%  { transform:translateY(82vh) translateX(-20px) rotate(290deg); }
    94%  { opacity:0.85; }
    100% { opacity:0; transform:translateY(112vh) translateX(10px) rotate(380deg); }
  }

  @keyframes flDrift {
    0%   { opacity:0; left:-5%; top:66%; transform:rotate(-8deg); }
    7%   { opacity:0.45; }
    50%  { top:42%; transform:rotate(10deg); }
    93%  { opacity:0.45; }
    100% { opacity:0; left:104%; top:58%; transform:rotate(-6deg); }
  }

  @keyframes flSway { 0%,100% { margin-top:0; } 50% { margin-top:4px; } }

  @keyframes flHearth { 0%,100% { opacity:0.65; } 33% { opacity:1; } 66% { opacity:0.8; } }

  @keyframes flMote {
    0%,100% { transform:translate(0,0); opacity:0.25; }
    50% { transform:translate(16px,-22px); opacity:0.7; }
  }

  @keyframes flBob { 0%,100% { transform:translateY(0) rotate(-5deg); } 50% { transform:translateY(-3px) rotate(6deg); } }''',
    "html": r'''<div class="fl-lights" aria-hidden="true">
  <span style="left:4%"></span><span style="left:12%"></span><span style="left:20%"></span>
  <span style="left:28%"></span><span style="left:36%"></span><span style="left:44%"></span>
  <span style="left:52%"></span><span style="left:60%"></span><span style="left:68%"></span>
  <span style="left:76%"></span><span style="left:84%"></span><span style="left:92%"></span>
</div>
<span class="fl-branch bl" aria-hidden="true">🍁</span>
<span class="fl-branch br" aria-hidden="true">🍁</span>
<span class="fl-leaf l1" aria-hidden="true">🍁</span>
<span class="fl-leaf l2" aria-hidden="true">🍂</span>
<span class="fl-leaf l3" aria-hidden="true">🍁</span>
<span class="fl-leaf l4" aria-hidden="true">🍃</span>
<span class="fl-leaf l5" aria-hidden="true">🍂</span>
<span class="fl-leaf l6" aria-hidden="true">🍁</span>
<span class="fl-leaf l7" aria-hidden="true">🍂</span>
<span class="fl-float f1" aria-hidden="true">🌰</span>
<span class="fl-float f2" aria-hidden="true">🥧</span>
<span class="fl-float f3" aria-hidden="true">🧣</span>
<span class="fl-mote m1" aria-hidden="true"></span>
<span class="fl-mote m2" aria-hidden="true"></span>
<span class="fl-mote m3" aria-hidden="true"></span>
<div class="fl-hearth" aria-hidden="true"></div>
<span class="fl-mug" aria-hidden="true">☕</span>
<div class="fl-steam" aria-hidden="true"><i></i><i></i><i></i></div>
<a class="fl-return" href="index.html" title="Return to the home frequency"><span class="ic">🍁</span> Back to Home Frequency</a>''',
    "js": "",
  },
  'halloween': {
    "css": r'''
  /* cobwebs pinned in the corners */
  .hw-web { position:fixed; z-index:50; font-size:4.2rem; opacity:0.5; pointer-events:none;
    filter:drop-shadow(0 0 8px rgba(192,132,252,0.4)); }

  .hw-web.tl { top:-12px; left:-10px; transform:rotate(-15deg); }

  .hw-web.tr { top:-12px; right:-10px; transform:scaleX(-1) rotate(-15deg); }


  /* drifting ghosts */
  .hw-ghost { position:fixed; z-index:1; pointer-events:none; font-size:1.9rem; opacity:0;
    animation:hwDrift 18s linear infinite; filter:drop-shadow(0 0 10px rgba(125,255,94,0.5)); }

  .hw-ghost.g2 { animation-delay:6s; animation-duration:22s; font-size:1.4rem; }

  .hw-ghost.g3 { animation-delay:12s; animation-duration:26s; font-size:2.3rem; }


  /* a bat that swoops across now and then */
  .hw-bat { position:fixed; z-index:51; pointer-events:none; font-size:1.7rem; opacity:0;
    animation:hwBat 13s ease-in-out infinite; filter:drop-shadow(0 0 6px rgba(255,122,26,0.6)); }


  /* jack-o-lantern flicker glow at page bottom + fog */
  .hw-fog { position:fixed; left:0; right:0; bottom:0; height:150px; z-index:1; pointer-events:none;
    background:linear-gradient(0deg, rgba(255,122,26,0.10), rgba(192,132,252,0.05) 55%, transparent);
    animation:hwFog 7s ease-in-out infinite; }


  /* dangling spider on a thread */
  .hw-spider { position:fixed; top:0; left:12%; z-index:51; pointer-events:none; text-align:center;
    animation:hwBob 5s ease-in-out infinite; transform-origin:top center; }

  .hw-spider::before { content:''; display:block; margin:0 auto; width:1px; height:110px;
    background:linear-gradient(180deg, rgba(255,255,255,0.35), rgba(255,255,255,0.08)); }

  .hw-spider span { font-size:1.3rem; display:block; margin-top:-4px;
    filter:drop-shadow(0 0 6px rgba(57,255,20,0.5)); }


  /* pumpkin back-to-normal portal */
  .hw-return { position:fixed; bottom:1.1rem; right:1.1rem; z-index:60; text-decoration:none;
    display:flex; align-items:center; gap:0.5rem;
    font-family:'VT323', monospace; font-size:1.05rem; letter-spacing:0.08em; color:#fff;
    background:rgba(13,7,24,0.85); border:1.5px solid #ff7a1a; border-radius:999px;
    padding:0.45rem 0.95rem; box-shadow:0 0 18px rgba(255,122,26,0.5);
    transition:box-shadow .2s ease, transform .2s ease; }

  .hw-return:hover { transform:translateY(-2px); box-shadow:0 0 30px rgba(255,122,26,0.85); }

  .hw-return .pk { font-size:1.25rem; animation:hwFlicker 2.4s steps(1) infinite; }
@media (max-width:600px){ .hw-web{ font-size:3rem; } .hw-spider{ left:6%; } .hw-spider::before{ height:70px; }}
@media (prefers-reduced-motion: reduce){
    .hw-ghost,.hw-bat,.hw-fog,.hw-spider,.hw-return .pk { animation:none !important; }
    .hw-ghost,.hw-bat { display:none; }}

  @keyframes hwDrift {
    0%   { opacity:0; left:-6%;  top:78%; transform:translateY(0) rotate(-6deg); }
    8%   { opacity:0.55; }
    50%  { transform:translateY(-90px) rotate(5deg); }
    92%  { opacity:0.55; }
    100% { opacity:0; left:104%; top:30%; transform:translateY(-140px) rotate(-4deg); }
  }

  @keyframes hwBat {
    0%,72% { opacity:0; left:-6%; top:18%; transform:scale(1) rotate(0deg); }
    74% { opacity:1; }
    80% { top:9%;  transform:scale(1.25) rotate(-14deg); }
    86% { top:24%; transform:scale(0.9) rotate(10deg); }
    94% { opacity:1; }
    100%{ opacity:0; left:104%; top:12%; transform:scale(1.1) rotate(-8deg); }
  }

  @keyframes hwFog { 0%,100% { opacity:0.7; } 50% { opacity:1; } }

  @keyframes hwBob { 0%,100% { transform:translateY(-14px) rotate(2deg); } 50% { transform:translateY(6px) rotate(-2deg); } }

  @keyframes hwFlicker { 0%,74%,78%,100% { opacity:1; } 75%,77% { opacity:0.4; } 90% { opacity:0.75; } }''',
    "html": r'''<span class="hw-web tl" aria-hidden="true">🕸️</span>
<span class="hw-web tr" aria-hidden="true">🕸️</span>
<span class="hw-ghost" aria-hidden="true">👻</span>
<span class="hw-ghost g2" aria-hidden="true">👻</span>
<span class="hw-ghost g3" aria-hidden="true">🎃</span>
<span class="hw-bat" aria-hidden="true">🦇</span>
<div class="hw-spider" aria-hidden="true"><span>🕷️</span></div>
<div class="hw-fog" aria-hidden="true"></div>
<a class="hw-return" href="index.html" title="Return to the normal frequency"><span class="pk">🎃</span> Exit the Haunting</a>''',
    "js": "",
  },
  'sea': {
    "css": r'''
  /* sunbeams shafting down from the surface */
  .se-beam { position:fixed; top:-6%; z-index:1; pointer-events:none; width:110px; height:60vh;
    background:linear-gradient(180deg, rgba(125,238,255,0.14), transparent 80%);
    clip-path:polygon(38% 0, 62% 0, 100% 100%, 0 100%); filter:blur(2px);
    animation:seBeam 9s ease-in-out infinite; transform-origin:top center; }

  .se-beam.b1 { left:14%; }
 .se-beam.b2 { left:44%; animation-delay:3s; width:150px; }

  .se-beam.b3 { left:76%; animation-delay:6s; width:90px; }


  /* caustic light ripples wandering over the page */
  .se-caustic { position:fixed; inset:0; z-index:1; pointer-events:none; opacity:0.5; mix-blend-mode:screen;
    background:
      radial-gradient(240px 130px at 20% 30%, rgba(46,230,255,0.10), transparent 70%),
      radial-gradient(300px 160px at 70% 60%, rgba(125,238,255,0.08), transparent 70%);
    animation:seCaustic 14s ease-in-out infinite alternate; }


  /* fish crossing at various depths */
  .se-fish { position:fixed; z-index:1; pointer-events:none; opacity:0;
    animation:seSwim linear infinite; filter:drop-shadow(0 2px 6px rgba(0,0,0,0.4)); }

  .se-fish.f1 { font-size:1.3rem; animation-duration:19s; }

  .se-fish.f2 { font-size:1rem;   animation-duration:26s; animation-delay:7s; }

  .se-fish.f3 { font-size:1.5rem; animation-duration:22s; animation-delay:13s; }

  .se-fish.rev { animation-name:seSwimRev; }


  /* the whale: enormous, deep, rare */
  .se-whale { position:fixed; z-index:0; pointer-events:none; font-size:5rem; opacity:0;
    animation:seWhale 52s linear infinite; filter:blur(1px) brightness(0.7) drop-shadow(0 6px 16px rgba(0,0,0,0.5)); }


  /* hand-built jellyfish drifting upward */
  .se-jelly { position:fixed; z-index:1; pointer-events:none; opacity:0; width:34px;
    animation:seJellyRise linear infinite; }

  .se-jelly .bell { width:34px; height:24px; border-radius:17px 17px 6px 6px;
    background:radial-gradient(ellipse at 50% 20%, rgba(255,157,148,0.9), rgba(160,125,255,0.5) 70%, rgba(160,125,255,0.2));
    box-shadow:0 0 16px rgba(160,125,255,0.6); animation:sePulse 2.4s ease-in-out infinite; }

  .se-jelly i { position:absolute; top:22px; width:2px; height:22px; border-radius:999px;
    background:linear-gradient(180deg, rgba(255,157,148,0.7), transparent);
    animation:seTent 2.4s ease-in-out infinite; transform-origin:top center; }

  .se-jelly i:nth-child(2) { left:6px; }
 .se-jelly i:nth-child(3) { left:13px; animation-delay:0.3s; }

  .se-jelly i:nth-child(4) { left:20px; animation-delay:0.15s; }
 .se-jelly i:nth-child(5) { left:27px; animation-delay:0.4s; }

  .se-jelly.j1 { left:22%; animation-duration:26s; }

  .se-jelly.j2 { left:66%; animation-duration:33s; animation-delay:12s; transform:scale(0.7); }

  .se-jelly.j3 { left:87%; animation-duration:29s; animation-delay:21s; transform:scale(1.2); }


  /* bubbles */
  .se-bub { position:fixed; bottom:-30px; z-index:1; pointer-events:none; border-radius:50%;
    background:radial-gradient(circle at 32% 30%, rgba(255,255,255,0.75), rgba(125,238,255,0.25) 55%, transparent 75%);
    border:1px solid rgba(125,238,255,0.35); animation:seRise linear infinite; }

  .se-bub.u1 { left:10%; width:12px; height:12px; animation-duration:12s; }

  .se-bub.u2 { left:38%; width:8px;  height:8px;  animation-duration:16s; animation-delay:4s; }

  .se-bub.u3 { left:61%; width:15px; height:15px; animation-duration:13s; animation-delay:8s; }

  .se-bub.u4 { left:83%; width:9px;  height:9px;  animation-duration:18s; animation-delay:2s; }


  /* seaweed swaying at the bottom edge */
  .se-weed { position:fixed; bottom:-6px; z-index:2; pointer-events:none; font-size:1.7rem;
    animation:seSway 4.5s ease-in-out infinite; transform-origin:bottom center;
    filter:drop-shadow(0 0 8px rgba(99,230,164,0.5)); }

  .se-weed.w1 { left:6%; }
 .se-weed.w2 { left:30%; animation-delay:1.2s; font-size:1.3rem; }

  .se-weed.w3 { left:52%; animation-delay:2.4s; }
 .se-weed.w4 { left:71%; animation-delay:0.7s; font-size:1.4rem; }

  .se-weed.w5 { left:93%; animation-delay:1.8s; }


  /* crab scuttling side to side */
  .se-crab { position:fixed; bottom:6px; left:40%; z-index:2; pointer-events:none; font-size:1.3rem;
    animation:seScuttle 11s ease-in-out infinite; filter:drop-shadow(0 2px 5px rgba(0,0,0,0.5)); }


  /* surface button */
  .se-return { position:fixed; bottom:1.1rem; right:1.1rem; z-index:60; text-decoration:none;
    display:flex; align-items:center; gap:0.5rem;
    font-family:'VT323', monospace; font-size:1.05rem; letter-spacing:0.08em; color:#fff;
    background:rgba(4,24,38,0.88); border:1.5px solid #2ee6ff; border-radius:999px;
    padding:0.45rem 0.95rem; box-shadow:0 0 18px rgba(46,230,255,0.5);
    transition:box-shadow .2s ease, transform .2s ease; }

  .se-return:hover { transform:translateY(-2px); box-shadow:0 0 30px rgba(255,223,138,0.8); border-color:#ffdf8a; }

  .se-return .ic { font-size:1.25rem; animation:seBob 3s ease-in-out infinite; display:inline-block; }
@media (max-width:600px){ .se-whale { font-size:3.2rem; } .se-beam.b3, .se-weed.w4 { display:none; }}
@media (prefers-reduced-motion: reduce){
    .se-beam,.se-caustic,.se-fish,.se-whale,.se-jelly,.se-jelly .bell,.se-jelly i,.se-bub,.se-weed,.se-crab,.se-return .ic { animation:none !important; }
    .se-fish,.se-whale,.se-jelly,.se-bub,.se-crab { display:none; }}

  @keyframes seBeam { 0%,100% { opacity:0.5; transform:rotate(-3deg); } 50% { opacity:1; transform:rotate(3deg); } }

  @keyframes seCaustic { 0% { background-position:0 0, 0 0; } 100% { background-position:70px 40px, -60px -30px; } }

  @keyframes seSwim {
    0% { opacity:0; left:-5%; top:44%; transform:scaleX(-1) translateY(0); }
    7% { opacity:0.85; } 50% { transform:scaleX(-1) translateY(-26px); }
    93% { opacity:0.85; } 100% { opacity:0; left:104%; top:38%; transform:scaleX(-1) translateY(0); } }

  @keyframes seSwimRev {
    0% { opacity:0; left:104%; top:64%; transform:translateY(0); }
    7% { opacity:0.85; } 50% { transform:translateY(22px); }
    93% { opacity:0.85; } 100% { opacity:0; left:-5%; top:58%; transform:translateY(0); } }

  @keyframes seWhale {
    0%,58% { opacity:0; left:-14%; top:72%; transform:scaleX(-1); }
    60% { opacity:0.45; }
    78% { top:66%; }
    96% { opacity:0.45; }
    100% { opacity:0; left:110%; top:70%; transform:scaleX(-1); } }

  @keyframes sePulse { 0%,100% { transform:scaleX(1) scaleY(1); } 50% { transform:scaleX(0.86) scaleY(1.12); } }

  @keyframes seTent { 0%,100% { transform:rotate(4deg); } 50% { transform:rotate(-6deg); } }

  @keyframes seJellyRise {
    0% { opacity:0; top:106%; } 6% { opacity:0.85; }
    50% { margin-left:18px; } 94% { opacity:0.85; } 100% { opacity:0; top:-12%; margin-left:-10px; } }

  @keyframes seRise {
    0% { transform:translateY(0) translateX(0); opacity:0; } 8% { opacity:0.8; }
    50% { transform:translateY(-55vh) translateX(16px); } 88% { opacity:0.6; }
    100% { transform:translateY(-108vh) translateX(-12px); opacity:0; } }

  @keyframes seSway { 0%,100% { transform:rotate(-8deg); } 50% { transform:rotate(9deg); } }

  @keyframes seScuttle {
    0%,100% { transform:translateX(0); } 12% { transform:translateX(-4px) translateY(-2px); }
    45% { transform:translateX(-150px); } 57% { transform:translateX(-146px) translateY(-2px); }
    95% { transform:translateX(0); } }

  @keyframes seBob { 0%,100% { transform:translateY(0) rotate(-5deg); } 50% { transform:translateY(-3px) rotate(6deg); } }''',
    "html": r'''<div class="se-beam b1" aria-hidden="true"></div>
<div class="se-beam b2" aria-hidden="true"></div>
<div class="se-beam b3" aria-hidden="true"></div>
<div class="se-caustic" aria-hidden="true"></div>
<span class="se-whale" aria-hidden="true">🐋</span>
<span class="se-fish f1" aria-hidden="true">🐠</span>
<span class="se-fish f2 rev" aria-hidden="true">🐟</span>
<span class="se-fish f3" aria-hidden="true">🐡</span>
<div class="se-jelly j1" aria-hidden="true"><div class="bell"></div><i></i><i></i><i></i><i></i></div>
<div class="se-jelly j2" aria-hidden="true"><div class="bell"></div><i></i><i></i><i></i><i></i></div>
<div class="se-jelly j3" aria-hidden="true"><div class="bell"></div><i></i><i></i><i></i><i></i></div>
<span class="se-bub u1" aria-hidden="true"></span>
<span class="se-bub u2" aria-hidden="true"></span>
<span class="se-bub u3" aria-hidden="true"></span>
<span class="se-bub u4" aria-hidden="true"></span>
<span class="se-weed w1" aria-hidden="true">🌿</span>
<span class="se-weed w2" aria-hidden="true">🌿</span>
<span class="se-weed w3" aria-hidden="true">🌿</span>
<span class="se-weed w4" aria-hidden="true">🌿</span>
<span class="se-weed w5" aria-hidden="true">🌿</span>
<span class="se-crab" aria-hidden="true">🦀</span>
<a class="se-return" href="index.html" title="Surface to the home frequency"><span class="ic">🐚</span> Surface to Home Frequency</a>''',
    "js": "",
  },
  'summer': {
    "css": r'''
  /* ── THE SUN: glowing core + rotating rays + heat pulse ── */
  .sm-sun { position:fixed; top:-70px; right:-70px; width:230px; height:230px; z-index:1; pointer-events:none; }

  .sm-sun::before { /* rays */
    content:''; position:absolute; inset:-45px;
    background:conic-gradient(from 0deg,
      rgba(255,221,51,0.22) 0 8deg, transparent 8deg 24deg,
      rgba(255,221,51,0.22) 24deg 32deg, transparent 32deg 48deg,
      rgba(255,221,51,0.22) 48deg 56deg, transparent 56deg 72deg,
      rgba(255,221,51,0.22) 72deg 80deg, transparent 80deg 96deg,
      rgba(255,221,51,0.22) 96deg 104deg, transparent 104deg 120deg,
      rgba(255,221,51,0.22) 120deg 128deg, transparent 128deg 144deg,
      rgba(255,221,51,0.22) 144deg 152deg, transparent 152deg 168deg,
      rgba(255,221,51,0.22) 168deg 176deg, transparent 176deg 192deg,
      rgba(255,221,51,0.22) 192deg 200deg, transparent 200deg 216deg,
      rgba(255,221,51,0.22) 216deg 224deg, transparent 224deg 240deg,
      rgba(255,221,51,0.22) 240deg 248deg, transparent 248deg 264deg,
      rgba(255,221,51,0.22) 264deg 272deg, transparent 272deg 288deg,
      rgba(255,221,51,0.22) 288deg 296deg, transparent 296deg 312deg,
      rgba(255,221,51,0.22) 312deg 320deg, transparent 320deg 336deg,
      rgba(255,221,51,0.22) 336deg 344deg, transparent 344deg 360deg);
    border-radius:50%; animation:smSpin 40s linear infinite;
  }

  .sm-sun::after { /* core */
    content:''; position:absolute; inset:0; border-radius:50%;
    background:radial-gradient(circle, rgba(255,240,150,0.9) 0%, rgba(255,221,51,0.55) 40%, rgba(255,158,60,0.25) 65%, transparent 72%);
    animation:smBreath 6s ease-in-out infinite;
  }


  /* ── THE OCEAN: three layered waves rolling at different speeds ── */
  .sm-sea { position:fixed; left:0; right:0; bottom:0; height:110px; z-index:2; pointer-events:none; overflow:hidden; }

  .sm-wave { position:absolute; bottom:-6px; left:0; width:200%; height:100%;
    background-repeat:repeat-x; background-position:bottom; background-size:50% 100%; }

  .sm-wave.w1 { animation:smWave 13s linear infinite; opacity:0.5;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 110' preserveAspectRatio='none'%3E%3Cpath d='M0,70 C150,30 300,30 450,70 C600,110 750,110 900,70 C1050,30 1150,40 1200,70 L1200,110 L0,110 Z' fill='%2300e0c6' fill-opacity='0.35'/%3E%3C/svg%3E"); }

  .sm-wave.w2 { animation:smWave 9s linear infinite reverse; opacity:0.45;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 110' preserveAspectRatio='none'%3E%3Cpath d='M0,80 C200,50 350,100 600,80 C850,60 1000,95 1200,75 L1200,110 L0,110 Z' fill='%235ee8ff' fill-opacity='0.35'/%3E%3C/svg%3E"); }

  .sm-wave.w3 { animation:smWave 7s linear infinite; opacity:0.55;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 110' preserveAspectRatio='none'%3E%3Cpath d='M0,92 C250,72 450,105 700,90 C950,75 1050,100 1200,88 L1200,110 L0,110 Z' fill='%23b78bff' fill-opacity='0.3'/%3E%3C/svg%3E"); }


  /* ── things riding the waves ── */
  .sm-sail { position:fixed; bottom:78px; z-index:2; pointer-events:none; font-size:2rem;
    animation:smSail 34s linear infinite; filter:drop-shadow(0 4px 8px rgba(0,0,0,0.4)); }

  .sm-surf { position:fixed; bottom:66px; z-index:3; pointer-events:none; font-size:1.7rem; opacity:0;
    animation:smSurf 21s ease-in-out infinite; animation-delay:8s; filter:drop-shadow(0 3px 6px rgba(0,0,0,0.4)); }


  /* ── pool bubbles rising the whole page ── */
  .sm-bub { position:fixed; bottom:-30px; z-index:1; pointer-events:none; border-radius:50%;
    background:radial-gradient(circle at 32% 30%, rgba(255,255,255,0.75), rgba(94,232,255,0.25) 55%, transparent 75%);
    border:1px solid rgba(94,232,255,0.35); animation:smRise linear infinite; }

  .sm-bub.b1 { left:8%;  width:14px; height:14px; animation-duration:11s; }

  .sm-bub.b2 { left:22%; width:8px;  height:8px;  animation-duration:15s; animation-delay:3s; }

  .sm-bub.b3 { left:47%; width:18px; height:18px; animation-duration:13s; animation-delay:6s; }

  .sm-bub.b4 { left:71%; width:10px; height:10px; animation-duration:17s; animation-delay:1.5s; }

  .sm-bub.b5 { left:88%; width:13px; height:13px; animation-duration:12s; animation-delay:8s; }

  .sm-bub.b6 { left:33%; width:7px;  height:7px;  animation-duration:19s; animation-delay:10s; }


  /* ── drifting tropical goodies ── */
  .sm-float { position:fixed; z-index:1; pointer-events:none; opacity:0;
    animation:smDrift linear infinite; filter:drop-shadow(0 0 10px rgba(255,221,51,0.35)); }

  .sm-float.f1 { font-size:1.6rem; animation-duration:26s; }

  .sm-float.f2 { font-size:1.3rem; animation-duration:33s; animation-delay:9s; }

  .sm-float.f3 { font-size:1.9rem; animation-duration:29s; animation-delay:17s; }

  .sm-float.f4 { font-size:1.4rem; animation-duration:37s; animation-delay:23s; }


  /* ── palm fronds leaning into the top corners ── */
  .sm-palm { position:fixed; top:-14px; z-index:50; font-size:4rem; pointer-events:none;
    filter:drop-shadow(0 4px 10px rgba(0,0,0,0.45)); animation:smSway 6s ease-in-out infinite; transform-origin:top center; }

  .sm-palm.pl { left:-14px; transform:rotate(115deg); }

  .sm-palm.pr { right:-14px; transform:rotate(-115deg) scaleX(-1); animation-delay:1.5s; }


  /* ── heat shimmer sweep across the page (very subtle) ── */
  .sm-shimmer { position:fixed; inset:0; z-index:1; pointer-events:none;
    background:linear-gradient(105deg, transparent 44%, rgba(255,255,255,0.035) 50%, transparent 56%);
    background-size:300% 100%; animation:smHeat 10s ease-in-out infinite; }


  /* ── back-to-main portal ── */
  .sm-return { position:fixed; bottom:1.1rem; right:1.1rem; z-index:60; text-decoration:none;
    display:flex; align-items:center; gap:0.5rem;
    font-family:'VT323', monospace; font-size:1.05rem; letter-spacing:0.08em; color:#fff;
    background:rgba(4,22,36,0.85); border:1.5px solid #ffdd33; border-radius:999px;
    padding:0.45rem 0.95rem; box-shadow:0 0 18px rgba(255,221,51,0.45);
    transition:box-shadow .2s ease, transform .2s ease; }

  .sm-return:hover { transform:translateY(-2px); box-shadow:0 0 30px rgba(255,221,51,0.8); }

  .sm-return .ic { font-size:1.25rem; animation:smBob 2.6s ease-in-out infinite; display:inline-block; }
@media (max-width:600px){
    .sm-sun { width:150px; height:150px; top:-50px; right:-50px; }
    .sm-palm { font-size:2.8rem; }
    .sm-sea { height:70px; }
    .sm-sail { bottom:48px; font-size:1.5rem; }
    .sm-surf { bottom:40px; font-size:1.3rem; }}
@media (prefers-reduced-motion: reduce){
    .sm-sun::before,.sm-sun::after,.sm-wave,.sm-sail,.sm-surf,.sm-bub,.sm-float,.sm-palm,.sm-shimmer,.sm-return .ic { animation:none !important; }
    .sm-sail,.sm-surf,.sm-bub,.sm-float,.sm-shimmer { display:none; }}

  @keyframes smSpin { to { transform:rotate(360deg); } }

  @keyframes smBreath { 0%,100% { transform:scale(1); } 50% { transform:scale(1.08); } }

  @keyframes smWave { to { transform:translateX(-50%); } }

  @keyframes smSail {
    0% { left:-6%; transform:translateY(0) rotate(-2deg); }
    25% { transform:translateY(-7px) rotate(2deg); }
    50% { transform:translateY(0) rotate(-2deg); }
    75% { transform:translateY(-7px) rotate(2deg); }
    100% { left:104%; transform:translateY(0) rotate(-2deg); }
  }

  @keyframes smSurf {
    0%,55% { opacity:0; right:-6%; transform:translateY(0) rotate(8deg) scaleX(-1); }
    57% { opacity:1; }
    65% { transform:translateY(-16px) rotate(-6deg) scaleX(-1); }
    75% { transform:translateY(-2px) rotate(6deg) scaleX(-1); }
    85% { transform:translateY(-14px) rotate(-8deg) scaleX(-1); }
    96% { opacity:1; }
    100% { opacity:0; right:104%; transform:translateY(0) rotate(0deg) scaleX(-1); }
  }

  @keyframes smRise {
    0% { transform:translateY(0) translateX(0); opacity:0; }
    8% { opacity:0.8; }
    50% { transform:translateY(-55vh) translateX(14px); }
    88% { opacity:0.6; }
    100% { transform:translateY(-108vh) translateX(-10px); opacity:0; }
  }

  @keyframes smDrift {
    0%   { opacity:0; left:-5%; top:64%; transform:rotate(-10deg); }
    7%   { opacity:0.5; }
    50%  { top:38%; transform:rotate(12deg); }
    93%  { opacity:0.5; }
    100% { opacity:0; left:104%; top:55%; transform:rotate(-8deg); }
  }

  @keyframes smSway {
    0%,100% { margin-top:0; } 50% { margin-top:5px; }
  }

  @keyframes smHeat { 0% { background-position:120% 0; } 100% { background-position:-120% 0; } }

  @keyframes smBob { 0%,100% { transform:translateY(0) rotate(-6deg); } 50% { transform:translateY(-3px) rotate(6deg); } }''',
    "html": r'''<div class="sm-sun" aria-hidden="true"></div>
<div class="sm-shimmer" aria-hidden="true"></div>
<span class="sm-palm pl" aria-hidden="true">🌴</span>
<span class="sm-palm pr" aria-hidden="true">🌴</span>
<span class="sm-float f1" aria-hidden="true">🍉</span>
<span class="sm-float f2" aria-hidden="true">🍹</span>
<span class="sm-float f3" aria-hidden="true">🦩</span>
<span class="sm-float f4" aria-hidden="true">🐚</span>
<span class="sm-bub b1" aria-hidden="true"></span>
<span class="sm-bub b2" aria-hidden="true"></span>
<span class="sm-bub b3" aria-hidden="true"></span>
<span class="sm-bub b4" aria-hidden="true"></span>
<span class="sm-bub b5" aria-hidden="true"></span>
<span class="sm-bub b6" aria-hidden="true"></span>
<div class="sm-sea" aria-hidden="true">
  <div class="sm-wave w1"></div>
  <div class="sm-wave w2"></div>
  <div class="sm-wave w3"></div>
</div>
<span class="sm-sail" aria-hidden="true">⛵</span>
<span class="sm-surf" aria-hidden="true">🏄‍♀️</span>
<a class="sm-return" href="index.html" title="Return to the home frequency"><span class="ic">🍉</span> Back to Home Frequency</a>''',
    "js": "",
  },
  'vhs': {
    "css": r'''
  /* fullscreen scanlines + faint noise */
  .vh-scan { position:fixed; inset:0; z-index:53; pointer-events:none; opacity:0.35;
    background:repeating-linear-gradient(0deg, rgba(0,0,0,0.32) 0 1px, transparent 1px 3px); }

  .vh-noise { position:fixed; inset:0; z-index:53; pointer-events:none; opacity:0.06; mix-blend-mode:screen;
    background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    animation:vhNoise 0.4s steps(3) infinite; }


  /* chromatic fringe on the edges */
  .vh-fringe { position:fixed; inset:0; z-index:52; pointer-events:none; mix-blend-mode:screen; opacity:0.5;
    background:linear-gradient(90deg, rgba(255,63,174,0.14) 0%, transparent 5%, transparent 95%, rgba(39,232,245,0.14) 100%); }


  /* rolling tracking band — thick warped bar drifting down */
  .vh-track { position:fixed; left:0; right:0; height:34px; z-index:54; pointer-events:none; opacity:0;
    background:linear-gradient(180deg, transparent, rgba(255,255,255,0.14) 30%, rgba(255,63,174,0.10) 50%, rgba(39,232,245,0.10) 70%, transparent);
    filter:blur(1px); animation:vhTrack 8s linear infinite; }

  .vh-track.t2 { animation-delay:4s; animation-duration:12s; height:16px; }


  /* VCR on-screen display */
  .vh-osd { position:fixed; top:14px; left:16px; z-index:55; pointer-events:none;
    font-family:'VT323', monospace; color:#fff; text-shadow:2px 0 rgba(255,63,174,0.8), -2px 0 rgba(39,232,245,0.8);
    line-height:1.2; }

  .vh-osd .play { font-size:1.4rem; letter-spacing:0.14em; animation:vhBlink 1.4s steps(1) infinite; }

  .vh-osd .cnt { font-size:1.05rem; letter-spacing:0.18em; opacity:0.9; }

  .vh-sp { position:fixed; top:14px; right:16px; z-index:55; pointer-events:none;
    font-family:'VT323', monospace; font-size:1.15rem; letter-spacing:0.2em; color:#fff;
    text-shadow:2px 0 rgba(255,63,174,0.8), -2px 0 rgba(39,232,245,0.8); }


  /* handwritten tape label, bottom-left */
  .vh-label { position:fixed; bottom:1rem; left:1rem; z-index:55; pointer-events:none;
    background:linear-gradient(160deg,#efe8d8,#ddd2ba); color:#2c2417;
    border-radius:3px; padding:0.45rem 0.8rem; transform:rotate(-2deg);
    box-shadow:0 4px 12px rgba(0,0,0,0.55); border:1px solid #c4b795; max-width:200px; }

  .vh-label::before { content:''; position:absolute; top:4px; left:8px; right:8px; height:1.5px;
    background:repeating-linear-gradient(90deg,#ff3fae 0 8px, #27e8f5 8px 16px, #ffe14d 16px 24px); }

  .vh-label .l1 { font-family:'VT323', monospace; font-size:0.95rem; letter-spacing:0.06em; margin-top:4px; }

  .vh-label .l2 { font-family:'Space Mono', monospace; font-size:0.5rem; letter-spacing:0.14em; text-transform:uppercase; opacity:0.7; }


  /* occasional whole-signal stutter (fixed layers only) */
  .vh-stutter { position:fixed; inset:0; z-index:51; pointer-events:none; opacity:0; mix-blend-mode:screen;
    background:linear-gradient(0deg, rgba(255,63,174,0.06), rgba(39,232,245,0.06));
    animation:vhStut 9s steps(1) infinite; }


  /* eject button */
  .vh-return { position:fixed; bottom:1.1rem; right:1.1rem; z-index:60; text-decoration:none;
    display:flex; align-items:center; gap:0.5rem;
    font-family:'VT323', monospace; font-size:1.05rem; letter-spacing:0.08em; color:#fff;
    background:rgba(10,10,14,0.9); border:1.5px solid #ffe14d; border-radius:999px;
    padding:0.45rem 0.95rem; box-shadow:0 0 18px rgba(255,225,77,0.4);
    text-shadow:1.5px 0 rgba(255,63,174,0.7), -1.5px 0 rgba(39,232,245,0.7);
    transition:box-shadow .2s ease, transform .2s ease; }

  .vh-return:hover { transform:translateY(-2px); box-shadow:0 0 30px rgba(255,225,77,0.8); }

  .vh-return .ic { animation:vhBlink 1.4s steps(1) infinite; }
@media (max-width:600px){ .vh-label { max-width:150px; } .vh-osd .play { font-size:1.15rem; }}
@media (prefers-reduced-motion: reduce){
    .vh-noise,.vh-track,.vh-osd .play,.vh-stutter,.vh-return .ic { animation:none !important; }
    .vh-track,.vh-stutter { display:none; }}

  @keyframes vhNoise { 0% { transform:translate(0,0); } 50% { transform:translate(-3px,2px); } 100% { transform:translate(3px,-2px); } }

  @keyframes vhTrack {
    0% { opacity:0; top:-6%; } 5% { opacity:1; }
    46% { transform:scaleY(1); } 48% { transform:scaleY(2.6); } 50% { transform:scaleY(1); }
    95% { opacity:1; } 100% { opacity:0; top:104%; } }

  @keyframes vhBlink { 0%,60% { opacity:1; } 61%,100% { opacity:0.25; } }

  @keyframes vhStut { 0%,91%,94%,100% { opacity:0; } 92%,93% { opacity:1; } }''',
    "html": r'''<div class="vh-scan" aria-hidden="true"></div>
<div class="vh-noise" aria-hidden="true"></div>
<div class="vh-fringe" aria-hidden="true"></div>
<div class="vh-track" aria-hidden="true"></div>
<div class="vh-track t2" aria-hidden="true"></div>
<div class="vh-stutter" aria-hidden="true"></div>
<div class="vh-osd" aria-hidden="true">
  <div class="play">▶ PLAY</div>
  <div class="cnt" id="vh-counter">SP 0:00:00</div>
</div>
<div class="vh-sp" aria-hidden="true">CH 03</div>
<div class="vh-label" aria-hidden="true">
  <div class="l1">MAGICK MICA — home recording ✦</div>
  <div class="l2">Do not erase · Rewind after use</div>
</div>
<a class="vh-return" href="index.html" title="Eject back to the home frequency"><span class="ic">⏏</span> Eject to Home Frequency</a>''',
    "js": "",
  },
  'winter': {
    "css": r'''
  /* ── AURORA BOREALIS rippling across the sky ── */
  .wn-aurora { position:fixed; top:0; left:-20%; right:-20%; height:46vh; z-index:1; pointer-events:none;
    background:
      radial-gradient(60% 100% at 20% 0%, rgba(140,224,200,0.22), transparent 65%),
      radial-gradient(55% 100% at 55% 0%, rgba(168,184,255,0.20), transparent 65%),
      radial-gradient(50% 100% at 85% 0%, rgba(255,123,168,0.16), transparent 65%);
    filter:blur(28px); animation:wnAurora 18s ease-in-out infinite alternate; }

  .wn-aurora.a2 { height:38vh; animation-duration:26s; animation-delay:5s; opacity:0.75;
    background:
      radial-gradient(55% 100% at 35% 0%, rgba(194,240,255,0.18), transparent 65%),
      radial-gradient(50% 100% at 70% 0%, rgba(140,224,200,0.20), transparent 65%); }


  /* ── icicle lights strung along the top ── */
  .wn-lights { position:fixed; top:0; left:0; right:0; height:30px; z-index:50; pointer-events:none; }

  .wn-lights::before { content:''; position:absolute; left:-2%; right:-2%; top:5px; height:16px;
    border-bottom:1.5px solid rgba(194,240,255,0.3); border-radius:0 0 100% 100%; }

  .wn-lights span { position:absolute; top:14px; width:6px; border-radius:3px 3px 60% 60%;
    background:linear-gradient(180deg, rgba(255,255,255,0.95), rgba(159,232,255,0.5));
    box-shadow:0 0 10px rgba(194,240,255,0.9); animation:wnGlow 3.2s ease-in-out infinite; }

  .wn-lights span:nth-child(even) { animation-delay:1.6s; }

  .wn-lights span:nth-child(3n) { animation-delay:0.8s; }


  /* ── SNOW: three layers at different depths/speeds ── */
  .wn-flake { position:fixed; top:-6%; z-index:1; pointer-events:none; color:#fff; opacity:0;
    text-shadow:0 0 8px rgba(194,240,255,0.9); animation:wnFall linear infinite; }

  .wn-flake.near { font-size:1.05rem; }

  .wn-flake.mid  { font-size:0.75rem; opacity:0; filter:blur(0.4px); }

  .wn-flake.far  { font-size:0.5rem;  filter:blur(1px); }

  .wn-flake.f1  { left:4%;  animation-duration:11s; }

  .wn-flake.f2  { left:13%; animation-duration:16s; animation-delay:2s; }

  .wn-flake.f3  { left:22%; animation-duration:9s;  animation-delay:5s; }

  .wn-flake.f4  { left:31%; animation-duration:14s; animation-delay:1s; }

  .wn-flake.f5  { left:40%; animation-duration:12s; animation-delay:7s; }

  .wn-flake.f6  { left:49%; animation-duration:18s; animation-delay:3s; }

  .wn-flake.f7  { left:58%; animation-duration:10s; animation-delay:9s; }

  .wn-flake.f8  { left:67%; animation-duration:15s; animation-delay:4s; }

  .wn-flake.f9  { left:76%; animation-duration:13s; animation-delay:11s; }

  .wn-flake.f10 { left:85%; animation-duration:17s; animation-delay:6s; }

  .wn-flake.f11 { left:94%; animation-duration:11s; animation-delay:8s; }

  .wn-flake.f12 { left:36%; animation-duration:20s; animation-delay:13s; }


  /* ── snow drift piled along the bottom edge ── */
  .wn-drift { position:fixed; left:0; right:0; bottom:0; height:70px; z-index:2; pointer-events:none;
    background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 70' preserveAspectRatio='none'%3E%3Cpath d='M0,44 C120,20 200,52 330,40 C460,28 520,58 660,46 C800,34 900,60 1030,44 C1120,33 1170,50 1200,42 L1200,70 L0,70 Z' fill='%23ffffff' fill-opacity='0.9'/%3E%3C/svg%3E") repeat-x bottom;
    background-size:100% 100%; filter:drop-shadow(0 -4px 14px rgba(194,240,255,0.35)); }

  .wn-drift::after { content:''; position:absolute; inset:0;
    background:linear-gradient(180deg, rgba(159,232,255,0.25), transparent 60%); }


  /* ── frost creeping in from the corners ── */
  .wn-frost { position:fixed; inset:0; z-index:52; pointer-events:none; opacity:0.55;
    background:
      radial-gradient(340px 240px at 0% 0%,     rgba(194,240,255,0.16), transparent 70%),
      radial-gradient(340px 240px at 100% 0%,   rgba(194,240,255,0.16), transparent 70%),
      radial-gradient(300px 220px at 0% 100%,   rgba(194,240,255,0.12), transparent 70%),
      radial-gradient(300px 220px at 100% 100%, rgba(194,240,255,0.12), transparent 70%);
    animation:wnBreathe 9s ease-in-out infinite; }


  /* ── hanging icicles in the top corners ── */
  .wn-icicles { position:fixed; top:0; z-index:51; pointer-events:none; display:flex; gap:5px; }

  .wn-icicles.il { left:8px; }
 .wn-icicles.ir { right:8px; }

  .wn-icicles i { display:block; width:7px; border-radius:0 0 50% 50%;
    background:linear-gradient(180deg, rgba(255,255,255,0.9), rgba(159,232,255,0.35), transparent);
    box-shadow:0 0 8px rgba(194,240,255,0.6); animation:wnDrip 5s ease-in-out infinite; }

  .wn-icicles i:nth-child(1) { height:26px; }
 .wn-icicles i:nth-child(2) { height:40px; animation-delay:1.2s; }

  .wn-icicles i:nth-child(3) { height:20px; animation-delay:2.4s; }
 .wn-icicles i:nth-child(4) { height:33px; animation-delay:0.6s; }

  .wn-icicles i:nth-child(5) { height:16px; animation-delay:3.1s; }


  /* ── pine trees dusted with snow, along the bottom ── */
  .wn-tree { position:fixed; bottom:26px; z-index:2; pointer-events:none;
    filter:drop-shadow(0 4px 10px rgba(0,0,0,0.45)); animation:wnTree 7s ease-in-out infinite; transform-origin:bottom center; }

  .wn-tree.t1 { left:5%;  font-size:2.3rem; }

  .wn-tree.t2 { left:17%; font-size:1.6rem; animation-delay:1.5s; opacity:0.75; }

  .wn-tree.t3 { left:83%; font-size:1.9rem; animation-delay:3s; }

  .wn-tree.t4 { left:93%; font-size:1.4rem; animation-delay:2.2s; opacity:0.7; }


  /* ── a snowman keeping watch ── */
  .wn-snowman { position:fixed; bottom:24px; left:34%; z-index:2; pointer-events:none; font-size:1.9rem;
    filter:drop-shadow(0 4px 8px rgba(0,0,0,0.4)); animation:wnBob 5.5s ease-in-out infinite; }


  /* ── cocoa steaming in the corner ── */
  .wn-cocoa { position:fixed; bottom:1rem; left:1rem; z-index:51; pointer-events:none; font-size:2rem;
    filter:drop-shadow(0 0 12px rgba(255,233,168,0.6)); }

  .wn-steam { position:fixed; bottom:3.5rem; left:1.6rem; z-index:51; pointer-events:none; }

  .wn-steam i { position:absolute; bottom:0; width:7px; height:28px; border-radius:999px;
    background:linear-gradient(180deg, transparent, rgba(255,245,220,0.5), transparent);
    filter:blur(2.5px); opacity:0; animation:wnSteam 4.2s ease-in-out infinite; }

  .wn-steam i:nth-child(2) { left:8px; animation-delay:1.5s; height:36px; }

  .wn-steam i:nth-child(3) { left:-5px; animation-delay:2.9s; height:22px; }


  /* ── return home ── */
  .wn-return { position:fixed; bottom:1.1rem; right:1.1rem; z-index:60; text-decoration:none;
    display:flex; align-items:center; gap:0.5rem;
    font-family:'VT323', monospace; font-size:1.05rem; letter-spacing:0.08em; color:#fff;
    background:rgba(8,18,34,0.9); border:1.5px solid #9fe8ff; border-radius:999px;
    padding:0.45rem 0.95rem; box-shadow:0 0 18px rgba(159,232,255,0.5);
    transition:box-shadow .2s ease, transform .2s ease; }

  .wn-return:hover { transform:translateY(-2px); box-shadow:0 0 30px rgba(255,233,168,0.85); border-color:#ffe9a8; }

  .wn-return .ic { font-size:1.25rem; animation:wnSpin 9s linear infinite; display:inline-block; }
@media (max-width:600px){
    .wn-tree.t2, .wn-tree.t4, .wn-snowman { display:none; }
    .wn-icicles i:nth-child(4), .wn-icicles i:nth-child(5) { display:none; }
    .wn-drift { height:46px; }}
@media (prefers-reduced-motion: reduce){
    .wn-aurora,.wn-flake,.wn-lights span,.wn-frost,.wn-icicles i,.wn-tree,.wn-snowman,.wn-steam i,.wn-return .ic { animation:none !important; }
    .wn-flake,.wn-steam { display:none; }}

  @keyframes wnAurora {
    0%   { transform:translateX(-4%) skewX(-4deg) scaleY(1); opacity:0.75; }
    50%  { transform:translateX(3%) skewX(3deg) scaleY(1.15); opacity:1; }
    100% { transform:translateX(-2%) skewX(-2deg) scaleY(0.95); opacity:0.8; } }

  @keyframes wnGlow { 0%,100% { opacity:1; } 50% { opacity:0.4; } }

  @keyframes wnFall {
    0%   { opacity:0; transform:translateY(0) translateX(0) rotate(0deg); }
    6%   { opacity:0.95; }
    25%  { transform:translateY(28vh) translateX(22px) rotate(90deg); }
    50%  { transform:translateY(55vh) translateX(-18px) rotate(180deg); }
    75%  { transform:translateY(82vh) translateX(24px) rotate(270deg); }
    94%  { opacity:0.95; }
    100% { opacity:0; transform:translateY(112vh) translateX(-10px) rotate(360deg); } }

  @keyframes wnBreathe { 0%,100% { opacity:0.45; } 50% { opacity:0.75; } }

  @keyframes wnDrip { 0%,100% { transform:scaleY(1); opacity:1; } 50% { transform:scaleY(1.06); opacity:0.8; } }

  @keyframes wnTree { 0%,100% { transform:rotate(-1.5deg); } 50% { transform:rotate(1.5deg); } }

  @keyframes wnBob { 0%,100% { transform:translateY(0) rotate(-2deg); } 50% { transform:translateY(-3px) rotate(2deg); } }

  @keyframes wnSteam {
    0% { opacity:0; transform:translateY(6px) rotate(0deg) scaleY(0.7); }
    28% { opacity:0.85; }
    100% { opacity:0; transform:translateY(-42px) rotate(10deg) scaleY(1.3); } }

  @keyframes wnSpin { to { transform:rotate(360deg); } }''',
    "html": r'''<div class="wn-aurora" aria-hidden="true"></div>
<div class="wn-aurora a2" aria-hidden="true"></div>
<div class="wn-frost" aria-hidden="true"></div>
<div class="wn-lights" aria-hidden="true">
  <span style="left:5%;height:14px"></span><span style="left:13%;height:20px"></span><span style="left:21%;height:11px"></span>
  <span style="left:29%;height:18px"></span><span style="left:37%;height:13px"></span><span style="left:45%;height:21px"></span>
  <span style="left:53%;height:12px"></span><span style="left:61%;height:19px"></span><span style="left:69%;height:15px"></span>
  <span style="left:77%;height:22px"></span><span style="left:85%;height:12px"></span><span style="left:93%;height:17px"></span>
</div>
<div class="wn-icicles il" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
<div class="wn-icicles ir" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
<span class="wn-flake near f1" aria-hidden="true">❅</span>
<span class="wn-flake mid  f2" aria-hidden="true">❄</span>
<span class="wn-flake far  f3" aria-hidden="true">❆</span>
<span class="wn-flake near f4" aria-hidden="true">❄</span>
<span class="wn-flake mid  f5" aria-hidden="true">❅</span>
<span class="wn-flake far  f6" aria-hidden="true">❄</span>
<span class="wn-flake near f7" aria-hidden="true">❆</span>
<span class="wn-flake mid  f8" aria-hidden="true">❄</span>
<span class="wn-flake far  f9" aria-hidden="true">❅</span>
<span class="wn-flake near f10" aria-hidden="true">❄</span>
<span class="wn-flake mid  f11" aria-hidden="true">❆</span>
<span class="wn-flake far  f12" aria-hidden="true">❅</span>
<span class="wn-tree t1" aria-hidden="true">🌲</span>
<span class="wn-tree t2" aria-hidden="true">🌲</span>
<span class="wn-tree t3" aria-hidden="true">🌲</span>
<span class="wn-tree t4" aria-hidden="true">🌲</span>
<span class="wn-snowman" aria-hidden="true">⛄</span>
<div class="wn-drift" aria-hidden="true"></div>
<span class="wn-cocoa" aria-hidden="true">☕</span>
<div class="wn-steam" aria-hidden="true"><i></i><i></i><i></i></div>
<a class="wn-return" href="index.html" title="Return to the home frequency"><span class="ic">❄️</span> Back to Home Frequency</a>''',
    "js": "",
  },
  'witches': {
    "css": r'''
  /* dripping potion ribbon along the top */
  .wg-drip { position:fixed; top:0; left:0; right:0; height:12px; z-index:52; pointer-events:none;
    background:
      radial-gradient(6px 11px at 10px 100%, #9be23f 0 60%, transparent 61%),
      radial-gradient(5px 8px  at 46px 100%, #9be23f 0 60%, transparent 61%),
      radial-gradient(7px 13px at 82px 100%, #7fc434 0 60%, transparent 61%),
      linear-gradient(180deg, #0a1108 0 6px, rgba(155,226,63,0.55) 6px 8px, transparent 8px);
    background-size:120px 12px, 120px 12px, 120px 12px, 100% 12px;
    filter:drop-shadow(0 2px 6px rgba(155,226,63,0.45));
    animation:wgDrip 9s linear infinite; }


  /* falling brooms, bats & toadstools */
  .wg-fall { position:fixed; top:-8%; z-index:1; pointer-events:none; opacity:0;
    font-size:1.35rem; animation:wgFall linear infinite; }

  .wg-fall.f1 { left:12%; animation-duration:17s; }

  .wg-fall.f2 { left:34%; animation-duration:22s; animation-delay:5s; }

  .wg-fall.f3 { left:58%; animation-duration:19s; animation-delay:10s; }

  .wg-fall.f4 { left:79%; animation-duration:24s; animation-delay:3s; }

  .wg-fall.f5 { left:93%; animation-duration:20s; animation-delay:14s; }


  /* goblin eyes blinking in the dark */
  .wg-eyes { position:fixed; top:22%; right:7%; z-index:1; pointer-events:none;
    width:96px; height:30px; opacity:0; animation:wgLurk 21s ease-in-out infinite; }

  .wg-eyes .eye { position:absolute; top:0; width:20px; height:13px; border-radius:50% 50% 45% 45%;
    background:#9be23f; box-shadow:0 0 16px rgba(155,226,63,0.9);
    animation:wgBlink 4.3s steps(1) infinite; }

  .wg-eyes .eye.el { left:16px; transform:rotate(-12deg); }

  .wg-eyes .eye.er { right:16px; transform:rotate(12deg); }

  .wg-eyes .eye::after { content:''; position:absolute; top:3px; left:50%; margin-left:-2px;
    width:4px; height:8px; border-radius:50%; background:#0a1108; }


  /* scurrying goblin */
  .wg-goblin { position:fixed; bottom:10px; z-index:2; pointer-events:none; font-size:1.7rem;
    opacity:0; animation:wgScurry 26s ease-in-out infinite; }

  .wg-goblin::after { content:'✨'; position:absolute; top:-12px; right:-14px; font-size:0.8rem; }


  /* drifting apothecary bits */
  .wg-float { position:fixed; z-index:1; pointer-events:none; opacity:0;
    animation:wgDrift linear infinite; }

  .wg-float.d1 { font-size:1.5rem; animation-duration:31s; }

  .wg-float.d2 { font-size:1.2rem; animation-duration:37s; animation-delay:12s; }

  .wg-float.d3 { font-size:1.6rem; animation-duration:34s; animation-delay:22s; }


  /* bubbling cauldrons along the bottom */
  .wg-cauldron { position:fixed; bottom:0.6rem; z-index:2; pointer-events:none; font-size:1.2rem;
    animation:wgBubble 3.4s ease-in-out infinite; }

  .wg-cauldron.c1 { left:22%; }
 .wg-cauldron.c2 { left:52%; animation-delay:1.2s; }

  .wg-cauldron.c3 { left:76%; animation-delay:2.4s; }


  /* return to the hub */
  .wg-return { position:fixed; bottom:4.6rem; right:1.1rem; z-index:60; text-decoration:none;
    font-family:'VT323', monospace; font-size:1.1rem; letter-spacing:0.08em; color:#0a1108;
    background:#9be23f; border:1px solid #9be23f; border-radius:999px; padding:0.4rem 1.05rem;
    box-shadow:0 0 22px rgba(155,226,63,0.55); transition:transform .2s, box-shadow .2s; }

  .wg-return:hover { transform:translateY(-2px); box-shadow:0 0 32px rgba(155,226,63,0.9); }

  .wg-return .ic { display:inline-block; animation:wgHop 1.7s ease-in-out infinite; }
@media (max-width:700px){
    .wg-eyes { transform:scale(0.7); right:2%; }
    .wg-fall.f5 { display:none; }
    .wg-return .lbl { display:none; }
    .wg-return { bottom:4.9rem; width:44px; height:44px; padding:0; border-radius:50%;
      display:inline-flex; align-items:center; justify-content:center; }
    .wg-return .ic { font-size:1.35rem; }}
@media (prefers-reduced-motion: reduce){
    .wg-drip,.wg-fall,.wg-eyes,.wg-goblin,.wg-float,.wg-cauldron,.wg-return .ic { animation:none !important; }
    .wg-fall,.wg-eyes,.wg-goblin,.wg-float { display:none; }}

  @keyframes wgDrip { to { background-position:120px 0, -120px 0, 120px 0, 0 0; } }

  @keyframes wgFall {
    0%   { transform:translateY(0) rotate(0deg);      opacity:0; }
    8%   { opacity:0.75; }
    92%  { opacity:0.6; }
    100% { transform:translateY(112vh) rotate(320deg); opacity:0; }
  }

  @keyframes wgLurk { 0%,72%,100% { opacity:0; } 80%,92% { opacity:0.9; } }

  @keyframes wgBlink { 0%,94% { transform:scaleY(1); } 96%,100% { transform:scaleY(0.1); } }

  @keyframes wgScurry {
    0%,100% { left:-8%;  opacity:0; transform:scaleX(1); }
    6%      { opacity:1; }
    46%     { left:104%; opacity:1; transform:scaleX(1); }
    52%     { left:104%; opacity:0; transform:scaleX(-1); }
  }

  @keyframes wgDrift {
    0%   { left:-6%;  top:74%; opacity:0; transform:rotate(0deg); }
    10%  { opacity:0.65; }
    90%  { opacity:0.5; }
    100% { left:104%; top:24%; opacity:0; transform:rotate(28deg); }
  }

  @keyframes wgBubble { 0%,100% { transform:translateY(0) scale(1); } 50% { transform:translateY(-5px) scale(1.08); } }

  @keyframes wgHop { 0%,100% { transform:translateY(0) rotate(0deg); } 50% { transform:translateY(-4px) rotate(-12deg); } }''',
    "html": r'''<div class="wg-drip" aria-hidden="true"></div>
<span class="wg-fall f1" aria-hidden="true">🧹</span>
<span class="wg-fall f2" aria-hidden="true">🦇</span>
<span class="wg-fall f3" aria-hidden="true">🍄</span>
<span class="wg-fall f4" aria-hidden="true">🦇</span>
<span class="wg-fall f5" aria-hidden="true">🧹</span>
<div class="wg-eyes" aria-hidden="true"><span class="eye el"></span><span class="eye er"></span></div>
<span class="wg-float d1" aria-hidden="true">🧪</span>
<span class="wg-float d2" aria-hidden="true">🕸️</span>
<span class="wg-float d3" aria-hidden="true">🌙</span>
<span class="wg-cauldron c1" aria-hidden="true">🕯️</span>
<span class="wg-cauldron c2" aria-hidden="true">🕯️</span>
<span class="wg-cauldron c3" aria-hidden="true">🕯️</span>
<span class="wg-goblin" aria-hidden="true">👹</span>
<a class="wg-return" href="index.html" title="Back to the hub" aria-label="Back to the hub"><span class="ic">🧹</span><span class="lbl"> Back to the Broadcast</span></a>''',
    "js": "",
  },
  'witching': {
    "css": r'''
  /* ── moon phase garland across the top ── */
  .wt-phases { position:fixed; top:8px; left:0; right:0; z-index:50; pointer-events:none;
    display:flex; justify-content:center; gap:clamp(0.9rem,4vw,2.2rem); font-size:1.05rem; opacity:0.8; }

  .wt-phases span { filter:grayscale(0.3) drop-shadow(0 0 6px rgba(201,216,255,0.4)); }

  .wt-phases .full { font-size:1.5rem; filter:drop-shadow(0 0 14px rgba(255,247,214,0.95));
    animation:wtMoonGlow 4s ease-in-out infinite; }


  /* ── great crescent moon with halo, top-right ── */
  .wt-moon { position:fixed; top:34px; right:4%; z-index:1; pointer-events:none;
    width:120px; height:120px; border-radius:50%;
    background:radial-gradient(circle at 62% 38%, #fdf6d8 0%, #e8ddb0 55%, #c9bd8a 100%);
    box-shadow:0 0 40px rgba(255,247,214,0.5), 0 0 90px rgba(201,216,255,0.25),
      inset -16px -10px 24px rgba(120,110,70,0.35);
    animation:wtBreath 8s ease-in-out infinite; }

  .wt-moon::before { /* shadow bite → crescent */
    content:''; position:absolute; top:-8%; left:-14%; width:82%; height:82%; border-radius:50%;
    background:#070313; filter:blur(2px); }


  /* ── tarot cards drifting down, flipping ── */
  .wt-card { position:fixed; top:-10%; z-index:1; pointer-events:none; opacity:0;
    width:30px; height:48px; border-radius:4px;
    background:linear-gradient(150deg,#1e1240,#0d0722);
    border:1.5px solid rgba(255,207,110,0.7);
    box-shadow:0 0 12px rgba(180,92,255,0.5), inset 0 0 8px rgba(180,92,255,0.3);
    display:flex; align-items:center; justify-content:center;
    color:#ffcf6e; font-size:0.85rem; text-shadow:0 0 6px rgba(255,207,110,0.8);
    animation:wtCardFall linear infinite; }

  .wt-card.c1 { left:12%; animation-duration:19s; }

  .wt-card.c2 { left:38%; animation-duration:24s; animation-delay:7s; }

  .wt-card.c3 { left:63%; animation-duration:21s; animation-delay:13s; }

  .wt-card.c4 { left:85%; animation-duration:26s; animation-delay:3s; }


  /* ── will-o-wisp orbs wandering ── */
  .wt-wisp { position:fixed; z-index:1; pointer-events:none; border-radius:50%;
    background:radial-gradient(circle, rgba(110,231,200,0.9) 0%, rgba(110,231,200,0.25) 45%, transparent 70%);
    filter:blur(1px); animation:wtWisp ease-in-out infinite; }

  .wt-wisp.w1 { left:16%; top:52%; width:14px; height:14px; animation-duration:11s; }

  .wt-wisp.w2 { left:58%; top:30%; width:9px;  height:9px;  animation-duration:14s; animation-delay:4s; }

  .wt-wisp.w3 { left:80%; top:60%; width:12px; height:12px; animation-duration:12s; animation-delay:8s; }


  /* ── candles flickering in the bottom corners ── */
  .wt-candle { position:fixed; bottom:0.9rem; z-index:51; pointer-events:none; font-size:2rem;
    filter:drop-shadow(0 0 14px rgba(255,207,110,0.75)); animation:wtFlicker 3s steps(1) infinite; }

  .wt-candle.cl { left:1rem; }

  .wt-candle.cr { right:1rem; bottom:4.3rem; animation-delay:1.3s; font-size:1.6rem; }


  /* ── incense smoke curling up from the left candle ── */
  .wt-smoke { position:fixed; bottom:3.4rem; left:1.6rem; z-index:51; pointer-events:none; }

  .wt-smoke i { position:absolute; bottom:0; width:7px; height:34px; border-radius:999px;
    background:linear-gradient(180deg, transparent, rgba(201,167,255,0.4), transparent);
    filter:blur(3px); opacity:0; animation:wtSmoke 5s ease-in-out infinite; }

  .wt-smoke i:nth-child(2) { left:7px; animation-delay:1.7s; height:44px; }

  .wt-smoke i:nth-child(3) { left:-6px; animation-delay:3.4s; height:28px; }


  /* ── crystals pulsing along the bottom ── */
  .wt-gem { position:fixed; bottom:0.7rem; z-index:2; pointer-events:none; font-size:1.15rem;
    animation:wtGem 3.4s ease-in-out infinite; }

  .wt-gem.g1 { left:26%; animation-delay:0s;   filter:drop-shadow(0 0 10px rgba(180,92,255,0.9)); }

  .wt-gem.g2 { left:49%; animation-delay:1.1s; filter:drop-shadow(0 0 10px rgba(110,231,200,0.9)); }

  .wt-gem.g3 { left:71%; animation-delay:2.2s; filter:drop-shadow(0 0 10px rgba(201,216,255,0.9)); }


  /* ── starlight veil: tiny stars twinkling at fixed spots ── */
  .wt-star { position:fixed; z-index:1; pointer-events:none; color:#e6ecff; font-size:0.65rem; opacity:0;
    text-shadow:0 0 8px rgba(201,216,255,0.9); animation:wtTwinkle ease-in-out infinite; }

  .wt-star.s1 { left:8%;  top:22%; animation-duration:4.4s; }

  .wt-star.s2 { left:30%; top:14%; animation-duration:5.8s; animation-delay:1.2s; }

  .wt-star.s3 { left:52%; top:26%; animation-duration:4.9s; animation-delay:2.6s; }

  .wt-star.s4 { left:73%; top:40%; animation-duration:6.4s; animation-delay:0.7s; }

  .wt-star.s5 { left:91%; top:52%; animation-duration:5.2s; animation-delay:3.4s; }


  /* ── return portal ── */
  .wt-return { position:fixed; bottom:1.1rem; right:1.1rem; z-index:60; text-decoration:none;
    display:flex; align-items:center; gap:0.5rem;
    font-family:'VT323', monospace; font-size:1.05rem; letter-spacing:0.08em; color:#fff;
    background:rgba(13,7,34,0.88); border:1.5px solid #b45cff; border-radius:999px;
    padding:0.45rem 0.95rem; box-shadow:0 0 18px rgba(180,92,255,0.5);
    transition:box-shadow .2s ease, transform .2s ease; }

  .wt-return:hover { transform:translateY(-2px); box-shadow:0 0 30px rgba(255,207,110,0.8); border-color:#ffcf6e; }

  .wt-return .ic { font-size:1.25rem; animation:wtOrb 3.2s ease-in-out infinite; display:inline-block; }
@media (max-width:600px){
    .wt-moon { width:76px; height:76px; }
    .wt-phases { font-size:0.85rem; } .wt-phases .full { font-size:1.15rem; }
    .wt-candle.cr { display:none; }}
@media (prefers-reduced-motion: reduce){
    .wt-card,.wt-wisp,.wt-smoke i,.wt-gem,.wt-star,.wt-candle,.wt-moon,.wt-phases .full,.wt-return .ic { animation:none !important; }
    .wt-card,.wt-wisp,.wt-smoke,.wt-star { display:none; }}

  @keyframes wtMoonGlow { 0%,100% { filter:drop-shadow(0 0 10px rgba(255,247,214,0.7)); }
    50% { filter:drop-shadow(0 0 22px rgba(255,247,214,1)); } }

  @keyframes wtBreath { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-6px); } }

  @keyframes wtCardFall {
    0%   { opacity:0; transform:translateY(0) rotateY(0deg) rotate(-8deg); }
    6%   { opacity:0.8; }
    30%  { transform:translateY(30vh) rotateY(180deg) rotate(6deg); }
    60%  { transform:translateY(62vh) rotateY(360deg) rotate(-6deg); }
    94%  { opacity:0.8; }
    100% { opacity:0; transform:translateY(112vh) rotateY(540deg) rotate(8deg); }
  }

  @keyframes wtWisp {
    0%,100% { transform:translate(0,0); opacity:0.35; }
    25% { transform:translate(26px,-34px); opacity:0.85; }
    50% { transform:translate(-14px,-58px); opacity:0.5; }
    75% { transform:translate(-32px,-20px); opacity:0.8; }
  }

  @keyframes wtFlicker {
    0%,52%,58%,100% { filter:drop-shadow(0 0 14px rgba(255,207,110,0.75)); }
    53%,57% { filter:drop-shadow(0 0 7px rgba(255,207,110,0.45)); }
    80% { filter:drop-shadow(0 0 20px rgba(255,207,110,0.95)); }
  }

  @keyframes wtSmoke {
    0% { opacity:0; transform:translateY(8px) rotate(0deg) scaleY(0.7); }
    25% { opacity:0.8; }
    100% { opacity:0; transform:translateY(-52px) rotate(14deg) scaleY(1.3); }
  }

  @keyframes wtGem { 0%,100% { transform:translateY(0) scale(1); opacity:0.75; }
    50% { transform:translateY(-5px) scale(1.12); opacity:1; } }

  @keyframes wtTwinkle { 0%,100% { opacity:0; transform:scale(0.6); } 50% { opacity:0.95; transform:scale(1.25); } }

  @keyframes wtOrb { 0%,100% { transform:translateY(0); filter:drop-shadow(0 0 4px rgba(180,92,255,0.6)); }
    50% { transform:translateY(-3px); filter:drop-shadow(0 0 12px rgba(180,92,255,1)); } }''',
    "html": r'''<div class="wt-phases" aria-hidden="true">
  <span>🌑</span><span>🌒</span><span>🌓</span><span>🌔</span><span class="full">🌕</span><span>🌖</span><span>🌗</span><span>🌘</span>
</div>
<div class="wt-moon" aria-hidden="true"></div>
<div class="wt-card c1" aria-hidden="true">☽</div>
<div class="wt-card c2" aria-hidden="true">✦</div>
<div class="wt-card c3" aria-hidden="true">☀</div>
<div class="wt-card c4" aria-hidden="true">♆</div>
<span class="wt-wisp w1" aria-hidden="true"></span>
<span class="wt-wisp w2" aria-hidden="true"></span>
<span class="wt-wisp w3" aria-hidden="true"></span>
<span class="wt-star s1" aria-hidden="true">✦</span>
<span class="wt-star s2" aria-hidden="true">✧</span>
<span class="wt-star s3" aria-hidden="true">✦</span>
<span class="wt-star s4" aria-hidden="true">✧</span>
<span class="wt-star s5" aria-hidden="true">✦</span>
<span class="wt-gem g1" aria-hidden="true">🔮</span>
<span class="wt-gem g2" aria-hidden="true">💎</span>
<span class="wt-gem g3" aria-hidden="true">🔮</span>
<span class="wt-candle cl" aria-hidden="true">🕯️</span>
<span class="wt-candle cr" aria-hidden="true">🕯️</span>
<div class="wt-smoke" aria-hidden="true"><i></i><i></i><i></i></div>
<a class="wt-return" href="index.html" title="Return to the home frequency"><span class="ic">🔮</span> Back to Home Frequency</a>''',
    "js": "",
  },
  'wonderland': {
    "css": r'''
  /* checkerboard ribbon along the top */
  .wl-check { position:fixed; top:0; left:0; right:0; height:10px; z-index:52; pointer-events:none;
    background:repeating-conic-gradient(#fff 0 25%, #120418 0 50%) 0 0/20px 20px;
    opacity:0.85; animation:wlCheck 3s linear infinite; box-shadow:0 2px 10px rgba(0,0,0,0.5); }


  /* falling playing cards */
  .wl-card { position:fixed; top:-10%; z-index:1; pointer-events:none; opacity:0;
    width:30px; height:44px; border-radius:4px; background:#fdf8ee;
    border:1px solid #c9bfa8; box-shadow:0 4px 10px rgba(0,0,0,0.4);
    display:flex; align-items:center; justify-content:center;
    font-size:1rem; animation:wlFall linear infinite; }

  .wl-card.red { color:#ff2440; }
 .wl-card.blk { color:#1a1a1a; }

  .wl-card.k1 { left:10%; animation-duration:15s; }

  .wl-card.k2 { left:31%; animation-duration:20s; animation-delay:6s; }

  .wl-card.k3 { left:56%; animation-duration:17s; animation-delay:11s; }

  .wl-card.k4 { left:78%; animation-duration:22s; animation-delay:3s; }

  .wl-card.k5 { left:92%; animation-duration:19s; animation-delay:15s; }


  /* the cheshire grin: appears, blinks, dissolves */
  .wl-cheshire { position:fixed; top:20%; right:7%; z-index:1; pointer-events:none;
    width:110px; height:70px; opacity:0; animation:wlCheshire 16s ease-in-out infinite; }

  .wl-cheshire .grin { position:absolute; bottom:0; left:0; width:110px; height:46px;
    border-radius:0 0 60px 60px;
    background:linear-gradient(180deg, #d06bff, #ff2440);
    -webkit-mask:radial-gradient(ellipse 90px 60px at 50% -20%, transparent 60%, #000 61%);
    mask:radial-gradient(ellipse 90px 60px at 50% -20%, transparent 60%, #000 61%);
    box-shadow:0 0 26px rgba(208,107,255,0.7); }

  .wl-cheshire .grin::before { /* teeth stripes */
    content:''; position:absolute; inset:0; border-radius:inherit;
    background:repeating-linear-gradient(90deg, transparent 0 12px, rgba(255,255,255,0.85) 12px 14px);
    -webkit-mask:inherit; mask:inherit; }

  .wl-cheshire .eye { position:absolute; top:0; width:22px; height:14px; border-radius:50% 50% 40% 40%;
    background:#ffe14d; box-shadow:0 0 12px rgba(255,206,92,0.9); animation:wlBlink 5s steps(1) infinite; }

  .wl-cheshire .eye.el { left:22px; transform:rotate(-14deg); }

  .wl-cheshire .eye.er { right:22px; transform:rotate(14deg); }


  /* white rabbit dashing along the bottom */
  .wl-rabbit { position:fixed; bottom:10px; z-index:2; pointer-events:none; font-size:1.8rem; opacity:0;
    animation:wlDash 14s ease-in infinite; filter:drop-shadow(0 3px 6px rgba(0,0,0,0.5)); }

  .wl-rabbit::after { content:'⌚'; position:absolute; top:-14px; right:-12px; font-size:0.85rem;
    animation:wlSwing 0.5s ease-in-out infinite alternate; }


  /* tea time drifting through */
  .wl-float { position:fixed; z-index:1; pointer-events:none; opacity:0;
    animation:wlDrift linear infinite; filter:drop-shadow(0 0 10px rgba(255,206,92,0.4)); }

  .wl-float.t1 { font-size:1.5rem; animation-duration:29s; }

  .wl-float.t2 { font-size:1.2rem; animation-duration:35s; animation-delay:11s; }

  .wl-float.t3 { font-size:1.6rem; animation-duration:32s; animation-delay:20s; }


  /* roses along the bottom, one flickering white→red (freshly painted) */
  .wl-rose { position:fixed; bottom:0.6rem; z-index:2; pointer-events:none; font-size:1.15rem;
    animation:wlRose 4s ease-in-out infinite; filter:drop-shadow(0 0 8px rgba(255,36,64,0.7)); }

  .wl-rose.r1 { left:24%; }
 .wl-rose.r2 { left:50%; animation-delay:1.3s; }
 .wl-rose.r3 { left:74%; animation-delay:2.6s; }

  .wl-rose.paint { animation:wlPaint 6s steps(1) infinite; }


  /* return through the looking glass */
  .wl-return { position:fixed; bottom:1.1rem; right:1.1rem; z-index:60; text-decoration:none;
    display:flex; align-items:center; gap:0.5rem;
    font-family:'VT323', monospace; font-size:1.05rem; letter-spacing:0.08em; color:#fff;
    background:rgba(24,8,24,0.88); border:1.5px solid #ff2440; border-radius:999px;
    padding:0.45rem 0.95rem; box-shadow:0 0 18px rgba(255,36,64,0.5);
    transition:box-shadow .2s ease, transform .2s ease; }

  .wl-return:hover { transform:translateY(-2px); box-shadow:0 0 30px rgba(111,195,255,0.85); border-color:#6fc3ff; }

  .wl-return .ic { font-size:1.25rem; animation:wlHop 1.6s ease-in-out infinite; display:inline-block; }
@media (max-width:600px){ .wl-cheshire { transform:scale(0.7); right:2%; } .wl-card.k5 { display:none; }}
@media (prefers-reduced-motion: reduce){
    .wl-check,.wl-card,.wl-cheshire,.wl-rabbit,.wl-float,.wl-rose,.wl-return .ic { animation:none !important; }
    .wl-card,.wl-cheshire,.wl-rabbit,.wl-float { display:none; }}

  @keyframes wlCheck { to { background-position:40px 0; } }

  @keyframes wlFall {
    0%   { opacity:0; transform:translateY(0) rotate(-12deg); }
    6%   { opacity:0.9; }
    35%  { transform:translateY(36vh) translateX(-24px) rotate(160deg); }
    70%  { transform:translateY(74vh) translateX(18px) rotate(300deg); }
    94%  { opacity:0.9; }
    100% { opacity:0; transform:translateY(112vh) rotate(400deg); }
  }

  @keyframes wlBlink { 0%,88%,96%,100% { transform:scaleY(1); } 90%,94% { transform:scaleY(0.1); } }

  @keyframes wlCheshire {
    0%,55% { opacity:0; filter:blur(6px); }
    62%,86% { opacity:0.85; filter:blur(0); }
    94%,100% { opacity:0; filter:blur(8px); }
  }

  @keyframes wlSwing { from { transform:rotate(-18deg); } to { transform:rotate(18deg); } }

  @keyframes wlDash {
    0%,68% { opacity:0; left:-7%; transform:scaleX(-1) translateY(0); }
    70% { opacity:1; }
    76% { transform:scaleX(-1) translateY(-9px); }
    82% { transform:scaleX(-1) translateY(0); }
    88% { transform:scaleX(-1) translateY(-9px); }
    97% { opacity:1; }
    100% { opacity:0; left:105%; transform:scaleX(-1) translateY(0); }
  }

  @keyframes wlDrift {
    0%   { opacity:0; left:-5%; top:62%; transform:rotate(-10deg); }
    7%   { opacity:0.5; }
    50%  { top:38%; transform:rotate(12deg); }
    93%  { opacity:0.5; }
    100% { opacity:0; left:104%; top:54%; transform:rotate(-8deg); }
  }

  @keyframes wlRose { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-4px); } }

  @keyframes wlPaint { 0%,45% { filter:grayscale(1) brightness(1.9) drop-shadow(0 0 8px rgba(255,255,255,0.7)); }
    50%,100% { filter:none; } }

  @keyframes wlHop { 0%,100% { transform:translateY(0); } 30% { transform:translateY(-4px); } 55% { transform:translateY(0); } }''',
    "html": r'''<div class="wl-check" aria-hidden="true"></div>
<div class="wl-card red k1" aria-hidden="true">♥</div>
<div class="wl-card blk k2" aria-hidden="true">♠</div>
<div class="wl-card red k3" aria-hidden="true">♦</div>
<div class="wl-card blk k4" aria-hidden="true">♣</div>
<div class="wl-card red k5" aria-hidden="true">♥</div>
<div class="wl-cheshire" aria-hidden="true">
  <span class="eye el"></span><span class="eye er"></span><span class="grin"></span>
</div>
<span class="wl-float t1" aria-hidden="true">🫖</span>
<span class="wl-float t2" aria-hidden="true">🍄</span>
<span class="wl-float t3" aria-hidden="true">🧁</span>
<span class="wl-rose r1" aria-hidden="true">🌹</span>
<span class="wl-rose r2 paint" aria-hidden="true">🌹</span>
<span class="wl-rose r3" aria-hidden="true">🌹</span>
<span class="wl-rabbit" aria-hidden="true">🐇</span>
<a class="wl-return" href="index.html" title="Back through the looking glass"><span class="ic">🐇</span> Back Through the Looking Glass</a>''',
    "js": "",
  },
}


def chrome_for(theme):
    d = CHROME.get(theme.get("chrome") or "", {})
    return {"css": d.get("css", ""), "html": d.get("html", ""), "js": d.get("js", "")}
