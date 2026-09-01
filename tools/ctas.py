# Generated from the CTA designs. Edit preview/ctas.html, then re-extract.
CTA_CSS = r'''.cta{position:relative;display:block;border-radius:20px;padding:32px 30px 28px;overflow:hidden;
text-decoration:none;transition:transform .28s cubic-bezier(.2,.9,.3,1.2),box-shadow .28s,border-color .28s}
.cta:hover{transform:translateY(-4px)}
.cta .in{position:relative;z-index:3;display:flex;align-items:center;gap:24px}
.cta .eyebrow{font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.26em;text-transform:uppercase}
.cta h3{font-family:Orbitron,monospace;font-size:26px;line-height:1.1;margin:9px 0 8px}
.cta .sub{font-size:13px;line-height:1.62;max-width:330px}
.cta .go{display:inline-flex;align-items:center;gap:9px;margin-top:15px;padding:11px 20px;
border-radius:999px;font-size:12px;letter-spacing:.13em;text-transform:uppercase;font-weight:500}
.cta .go span:last-child{transition:transform .25s}
.cta:hover .go span:last-child{transform:translateX(4px)}
.art{flex:0 0 auto;width:104px;height:104px;position:relative;display:grid;place-items:center}
.sheen{position:absolute;inset:0;z-index:2;pointer-events:none;
background:linear-gradient(104deg,transparent 38%,rgba(255,255,255,.14) 48%,transparent 58%);
transform:translateX(-120%);transition:transform .85s cubic-bezier(.3,.8,.3,1)}
.cta:hover .sheen{transform:translateX(120%)}

/* ── THE HEARTH ── */
.hearth{--cold:#0d111b;--slate:#1a2130;--ember:#ff7b3a;--flame:#ffc45c;--cream:#f5ece0;
background:radial-gradient(120% 100% at 22% 88%,rgba(255,123,58,.42),transparent 62%),
radial-gradient(90% 80% at 78% 14%,rgba(255,196,92,.18),transparent 60%),
linear-gradient(160deg,var(--slate) 0%,var(--cold) 68%);
border:1px solid rgba(255,196,92,.32);box-shadow:0 16px 44px rgba(0,0,0,.5)}
.hearth:hover{border-color:rgba(255,196,92,.72);box-shadow:0 22px 58px rgba(255,123,58,.26)}
.hearth .eyebrow{color:var(--flame)}
.hearth h3{color:var(--cream)}
.hearth .sub{color:#cdbca8}
.hearth .go{background:linear-gradient(96deg,var(--flame),var(--ember));color:#1a0d04;
box-shadow:0 5px 18px rgba(255,123,58,.4)}
.emb{position:absolute;inset:0;z-index:1;pointer-events:none;overflow:hidden}
.emb i{position:absolute;bottom:-8px;width:4px;height:4px;border-radius:50%;
background:var(--ember);box-shadow:0 0 8px 2px rgba(255,123,58,.7);animation:rise 5.5s ease-in infinite}
.emb i:nth-child(3n){background:var(--flame);box-shadow:0 0 9px 2px rgba(255,196,92,.7);width:3px;height:3px}
@keyframes rise{0%{opacity:0;transform:translateY(0) translateX(0) scale(.6)}
15%{opacity:1}70%{opacity:.7}
100%{opacity:0;transform:translateY(-150px) translateX(22px) scale(.3)}}
.hstack{width:96px;height:78px;position:relative;display:grid;place-items:end center}
.pool{position:absolute;bottom:6px;left:50%;transform:translateX(-50%);width:78px;height:16px;
border-radius:50%;background:radial-gradient(ellipse,rgba(255,123,58,.6),transparent 70%);filter:blur(3px)}
.log{position:absolute;height:12px;border-radius:7px;
background:linear-gradient(180deg,#6b4a30,#3a2718);border:1px solid rgba(255,196,92,.25)}
.log.a{width:70px;bottom:8px;left:13px;transform:rotate(-7deg)}
.log.b{width:62px;bottom:14px;left:18px;transform:rotate(6deg)}
.fire{position:absolute;bottom:16px;left:50%;margin-left:-22px;width:44px;height:56px;z-index:2;border-radius:50% 50% 46% 46%;
background:radial-gradient(ellipse at 50% 82%,var(--cream) 0%,var(--flame) 32%,var(--ember) 62%,transparent 78%);
animation:flicker 1.5s ease-in-out infinite;filter:blur(.4px)}
@keyframes flicker{0%,100%{transform:scaleY(1) scaleX(1);opacity:.95}
33%{transform:scaleY(1.13) scaleX(.93);opacity:1}
66%{transform:scaleY(.93) scaleX(1.06);opacity:.88}}

/* ── THE GLOBE ── */
.globe{--void:#07060e;--violet:#a020f0;--magenta:#ff44cc;--gold:#ffd166;--cyan:#22e0ff;--mist:#b8b0d4;
background:radial-gradient(120% 95% at 26% 20%,rgba(160,32,240,.42),transparent 62%),
radial-gradient(100% 85% at 82% 84%,rgba(255,68,204,.32),transparent 62%),
linear-gradient(158deg,#1d0b33 0%,#12061F 72%);
border:1px solid rgba(255,209,102,.3);box-shadow:0 16px 44px rgba(0,0,0,.5)}
.globe:hover{border-color:rgba(255,209,102,.7);box-shadow:0 22px 58px rgba(160,32,240,.3)}
.globe .eyebrow{color:var(--gold)}
.globe h3{background:linear-gradient(100deg,#fff,var(--gold) 38%,var(--magenta) 72%,var(--cyan));
-webkit-background-clip:text;background-clip:text;color:transparent}
.globe .sub{color:var(--mist)}
.globe .go{background:linear-gradient(96deg,var(--gold),#fff0c4 45%,var(--magenta));color:#1a0426;
box-shadow:0 5px 18px rgba(255,68,204,.36)}
.orb{width:92px;height:92px;border-radius:50%;position:relative;overflow:hidden;
background:radial-gradient(circle at 34% 28%,rgba(255,255,255,.6),rgba(160,32,240,.5) 40%,rgba(7,6,14,.9) 78%);
border:1px solid rgba(255,209,102,.45);
box-shadow:inset 0 0 26px rgba(255,68,204,.45),0 0 24px rgba(160,32,240,.4)}
.orb:before{content:'';position:absolute;inset:-38%;border-radius:45%;
background:conic-gradient(from 0deg,transparent,rgba(255,68,204,.42),transparent 42%,rgba(34,224,255,.36),transparent 78%);
animation:swirl 9s linear infinite}
@keyframes swirl{to{transform:rotate(360deg)}}
.orb:after{content:'';position:absolute;top:14%;left:22%;width:26%;height:18%;border-radius:50%;
background:rgba(255,255,255,.6);filter:blur(4px)}
.stand{position:absolute;bottom:-2px;left:50%;transform:translateX(-50%);width:52px;height:11px;
border-radius:0 0 12px 12px;background:linear-gradient(180deg,#ffd166,#8a5a12)}

/* ── MUSIC BOX ── */
.mbox{--plum:#2a1030;--rose:#ff8fc7;--gold:#ffd98a;--mint:#7bf1e4;--cream:#fdeaf6;
background:radial-gradient(120% 95% at 20% 18%,rgba(255,143,199,.36),transparent 62%),
radial-gradient(100% 85% at 84% 86%,rgba(123,241,228,.26),transparent 62%),
linear-gradient(158deg,var(--plum) 0%,#150719 72%);
border:1px solid rgba(255,217,138,.32);box-shadow:0 16px 44px rgba(0,0,0,.5)}
.mbox:hover{border-color:rgba(255,217,138,.72);box-shadow:0 22px 58px rgba(255,143,199,.26)}
.mbox .eyebrow{color:var(--gold)}
.mbox h3{color:var(--cream)}
.mbox .sub{color:#e0cfe0}
.mbox .go{background:linear-gradient(96deg,var(--gold),var(--cream) 45%,var(--rose));color:#2a0d20;
box-shadow:0 5px 18px rgba(255,143,199,.36)}
.notes{position:absolute;inset:0;z-index:1;pointer-events:none;overflow:hidden}
.notes i{position:absolute;font-style:normal;font-size:15px;color:var(--rose);opacity:0;
animation:float 6s ease-in-out infinite}
.notes i:nth-child(2n){color:var(--mint);font-size:12px}
.notes i:nth-child(3n){color:var(--gold);font-size:17px}
@keyframes float{0%{opacity:0;transform:translateY(10px) rotate(-8deg)}
20%{opacity:.9}100%{opacity:0;transform:translateY(-96px) rotate(14deg)}}
.box{width:88px;height:66px;position:relative}
.lid{position:absolute;z-index:2;top:0;left:0;width:88px;height:22px;border-radius:6px 6px 2px 2px;
background:linear-gradient(160deg,#5c2547,#3a1430);border:1px solid rgba(255,217,138,.5);
transform-origin:left bottom;animation:lift 4.2s ease-in-out infinite}
@keyframes lift{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(-26deg)}}
.base{position:absolute;z-index:1;bottom:0;width:88px;height:46px;border-radius:3px 3px 7px 7px;
background:linear-gradient(160deg,#4a1c3a,#2a1030);border:1px solid rgba(255,217,138,.42)}
.ballerina{position:absolute;z-index:3;bottom:42px;left:50%;width:9px;height:22px;margin-left:-4.5px;
background:linear-gradient(180deg,var(--cream),var(--rose));border-radius:50% 50% 30% 30%;
transform-origin:50% 100%;animation:twirl 3.1s linear infinite;
box-shadow:0 0 12px rgba(255,143,199,.8)}
@keyframes twirl{to{transform:rotateY(360deg)}}


.two{--night:#0b1026;--night2:#141b3d;--gold:#e0b64c;--lit:#ffe6a6;--turq:#3fb3a6;
--carn:#c05a3c;--papyrus:#e9dcbb;--sand:#c9b489;
background:radial-gradient(120% 95% at 24% 16%,rgba(224,182,76,.26),transparent 60%),
radial-gradient(100% 85% at 82% 88%,rgba(63,179,166,.24),transparent 62%),
linear-gradient(158deg,var(--night2) 0%,var(--night) 74%);
border:1px solid rgba(224,182,76,.36);box-shadow:0 16px 44px rgba(0,0,0,.55)}
.two:hover{border-color:rgba(255,230,166,.75);box-shadow:0 22px 58px rgba(224,182,76,.24)}
.two .eyebrow{color:var(--turq)}
.two h3{color:var(--papyrus)}
.two .sub{color:var(--sand)}
.two .go{background:linear-gradient(96deg,var(--gold),var(--lit) 48%,var(--carn));color:#1b1405;
box-shadow:0 5px 18px rgba(224,182,76,.36)}
.shrine{width:96px;height:96px;position:relative;display:grid;place-items:center}
.col{position:absolute;top:6px;width:11px;height:84px;border-radius:2px;
background:linear-gradient(180deg,var(--sand),#6b5a38);border:1px solid rgba(224,182,76,.4)}
.col.l{left:2px}.col.r{right:2px}
.col:before{content:'';position:absolute;top:-5px;left:-3px;width:17px;height:7px;border-radius:2px;
background:var(--gold)}
.eye{width:52px;height:52px;position:relative}
.eye svg{width:52px;height:52px;filter:drop-shadow(0 0 12px rgba(224,182,76,.65));
animation:gaze 5s ease-in-out infinite}
@keyframes gaze{0%,100%{opacity:.82;transform:translateY(0)}50%{opacity:1;transform:translateY(-4px)}}
.rays{position:absolute;inset:0;z-index:1;pointer-events:none;overflow:hidden}
.rays i{position:absolute;width:2px;height:2px;border-radius:50%;background:var(--lit);
box-shadow:0 0 7px 2px rgba(255,230,166,.6);animation:drift 6s ease-in-out infinite;opacity:0}
@keyframes drift{0%{opacity:0;transform:translateY(8px)}25%{opacity:.9}
100%{opacity:0;transform:translateY(-70px)}}

@media(max-width:560px){.cta .in{flex-direction:column;text-align:center;gap:18px}
.cta .sub{max-width:none}.cta h3{font-size:22px}}
@media(prefers-reduced-motion:reduce){
.emb i,.notes i,.fire,.orb:before,.lid,.ballerina{animation:none}
.cta,.sheen,.cta .go span:last-child{transition:none}}
.wand-cta{
  --void:#190522; --plum:#45114a; --rose:#ff5fa8; --lilac:#c48cff;
  --gold:#ffd9a0; --cream:#fdeaf6; --slab:#26082c;
  position:relative; display:block; max-width:640px; margin:0 auto;
  border-radius:20px; padding:34px 30px 30px; overflow:hidden; text-decoration:none;
  background:
    radial-gradient(120% 90% at 18% 12%, rgba(196,140,255,.34), transparent 60%),
    radial-gradient(110% 90% at 84% 88%, rgba(255,95,168,.30), transparent 62%),
    linear-gradient(158deg, var(--plum) 0%, var(--slab) 58%, var(--void) 100%);
  border:1px solid rgba(255,217,160,.34);
  box-shadow:0 0 0 1px rgba(196,140,255,.12) inset, 0 18px 46px rgba(0,0,0,.5);
  transition:transform .28s cubic-bezier(.2,.9,.3,1.2), box-shadow .28s ease, border-color .28s ease;
}
.wand-cta:hover{
  transform:translateY(-4px);
  border-color:rgba(255,217,160,.75);
  box-shadow:0 0 0 1px rgba(255,217,160,.2) inset, 0 24px 60px rgba(255,95,168,.28);
}

/* glitter: three drifting layers of tiny sparks */
.glit{position:absolute;inset:-20%;pointer-events:none;z-index:0;opacity:.85}
.glit i{position:absolute;width:3px;height:3px;border-radius:50%;background:var(--cream);
  box-shadow:0 0 6px 1px currentColor;animation:twinkle 3.4s ease-in-out infinite}
.glit i:nth-child(3n){background:var(--gold);color:var(--gold);width:4px;height:4px}
.glit i:nth-child(3n+1){background:var(--rose);color:var(--rose)}
.glit i:nth-child(3n+2){background:var(--lilac);color:var(--lilac)}
@keyframes twinkle{
  0%,100%{opacity:0;transform:translateY(0) scale(.5)}
  40%{opacity:1;transform:translateY(-7px) scale(1.15)}
  70%{opacity:.5;transform:translateY(-12px) scale(.8)}
}

/* the sweep of light that crosses on hover */
.sheen{position:absolute;inset:0;z-index:1;pointer-events:none;
  background:linear-gradient(104deg,transparent 38%,rgba(253,234,246,.20) 48%,transparent 58%);
  transform:translateX(-120%);transition:transform .85s cubic-bezier(.3,.8,.3,1)}
.wand-cta:hover .sheen{transform:translateX(120%)}

.cta .in{position:relative;z-index:3;display:flex;align-items:center;gap:24px}

.orb{flex:0 0 auto;width:96px;height:96px;border-radius:50%;display:grid;place-items:center;
  background:radial-gradient(circle at 34% 30%, rgba(253,234,246,.5), rgba(196,140,255,.28) 42%, transparent 70%);
  border:1px solid rgba(255,217,160,.4);position:relative}
.orb:after{content:'';position:absolute;inset:-9px;border-radius:50%;
  border:1px dashed rgba(196,140,255,.4);animation:spin 15s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.orb svg{width:46px;height:46px;animation:wave 3.6s ease-in-out infinite;transform-origin:70% 78%}
@keyframes wave{0%,100%{transform:rotate(-13deg)}50%{transform:rotate(13deg)}}

.eyebrow{font-family:Silkscreen,monospace;font-size:9px;letter-spacing:.26em;
  color:var(--gold);text-transform:uppercase}
h3{font-family:Orbitron,monospace;font-size:27px;line-height:1.1;margin:9px 0 8px;
  background:linear-gradient(100deg,var(--cream),var(--gold) 35%,var(--rose) 68%,var(--lilac));
  -webkit-background-clip:text;background-clip:text;color:transparent}
.sub{font-size:13px;line-height:1.62;color:#e3cfe6;max-width:330px}

.go{display:inline-flex;align-items:center;gap:9px;margin-top:16px;padding:11px 20px;
  border-radius:999px;font-size:12px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--void);font-weight:500;
  background:linear-gradient(96deg,var(--gold),var(--cream) 45%,var(--rose));
  box-shadow:0 5px 18px rgba(255,95,168,.34)}
.wand-cta:hover .go{box-shadow:0 7px 26px rgba(255,217,160,.5)}
.go span:last-child{transition:transform .25s ease}
.wand-cta:hover .go span:last-child{transform:translateX(4px)}

@media(max-width:560px){
  .cta .in{flex-direction:column;text-align:center;gap:18px}
  .sub{max-width:none}
  h3{font-size:23px}
}
@media(prefers-reduced-motion:reduce){
  .glit i,.orb:after,.orb svg{animation:none}
  .wand-cta,.sheen,.go span:last-child{transition:none}
  .glit i{opacity:.8}
}

/* ── THE VISITOR (alien.html) ── */
.ship{--deep:#04070f;--navy:#0d1a35;--acid:#7dff9b;--cyan:#5ce1ff;--mist:#9fb6cf;
background:radial-gradient(115% 95% at 50% 96%,rgba(125,255,155,.24),transparent 58%),
radial-gradient(95% 80% at 78% 12%,rgba(92,225,255,.20),transparent 62%),
linear-gradient(162deg,var(--navy) 0%,var(--deep) 72%);
border:1px solid rgba(125,255,155,.28);box-shadow:0 16px 44px rgba(0,0,0,.55)}
.ship:hover{border-color:rgba(125,255,155,.66);box-shadow:0 22px 58px rgba(92,225,255,.24)}
.ship .eyebrow{color:var(--acid)}
.ship h3{background:linear-gradient(100deg,#fff,var(--cyan) 44%,var(--acid));
-webkit-background-clip:text;background-clip:text;color:transparent}
.ship .sub{color:var(--mist)}
.ship .go{background:linear-gradient(96deg,var(--acid),var(--cyan));color:#04140b;
box-shadow:0 5px 18px rgba(125,255,155,.36)}
.saucer{width:104px;height:88px;position:relative;animation:bob 3.6s ease-in-out infinite}
.beam{position:absolute;left:50%;top:46px;margin-left:-31px;width:62px;height:44px;
clip-path:polygon(31% 0,69% 0,100% 100%,0 100%);filter:blur(.5px);
background:linear-gradient(180deg,rgba(125,255,155,.55),transparent 80%);
animation:beamPulse 2.6s ease-in-out infinite}
.hull{position:absolute;left:50%;top:36px;margin-left:-52px;width:104px;height:25px;border-radius:50%;
background:linear-gradient(180deg,#e6eef8,#7c93b3 52%,#3d4f66);box-shadow:0 0 18px rgba(92,225,255,.42)}
.dome{position:absolute;left:50%;top:12px;margin-left:-27px;width:54px;height:37px;
border-radius:50% 50% 42% 42%;border:1px solid rgba(255,255,255,.34);
background:radial-gradient(ellipse at 38% 26%,rgba(255,255,255,.92),rgba(92,225,255,.38) 48%,rgba(16,54,84,.72))}
.pilot{position:absolute;left:50%;top:23px;margin-left:-9px;width:18px;height:21px;
border-radius:50% 50% 44% 44%;background:var(--acid);box-shadow:0 0 11px rgba(125,255,155,.85)}
.pilot:before,.pilot:after{content:"";position:absolute;top:8px;width:4px;height:6px;
border-radius:50%;background:#07130b}
.pilot:before{left:3px}.pilot:after{right:3px}
.blinks{position:absolute;top:45px;left:50%;margin-left:-40px;width:80px;display:flex;justify-content:space-between}
.blinks i{width:7px;height:7px;border-radius:50%;background:var(--cyan);
box-shadow:0 0 9px var(--cyan);animation:blink 1.4s ease-in-out infinite}
.blinks i:nth-child(2){animation-delay:.45s}
.blinks i:nth-child(3){animation-delay:.9s}
/* The Visitor sits beside the tall Wand card. Instead of the usual art-left /
   text-right layout it stacks: a big ship centred at the top with its beam
   reaching down, and the text under it, so the card fills rather than
   trailing off into empty space. */
.cta-row .ship .in{flex-direction:column;text-align:center;gap:14px}
.cta-row .ship .art{width:176px;height:196px;overflow:visible;display:grid;
place-items:start center;margin-top:2px}
.cta-row .ship .sub{max-width:34ch;margin:0 auto}
.ship .saucer{width:104px;height:122px;transform-origin:top center;
animation:bobship 3.6s ease-in-out infinite}
.ship .beam{top:46px;margin-left:-31px;width:62px;height:74px;
background:linear-gradient(180deg,rgba(125,255,155,.5),rgba(125,255,155,.14) 58%,transparent 94%)}
.ship .glow{position:absolute;left:50%;bottom:0;margin-left:-31px;width:62px;height:13px;border-radius:50%;
background:radial-gradient(ellipse,rgba(125,255,155,.45),transparent 72%);filter:blur(3px);
animation:beamPulse 2.6s ease-in-out infinite}

/* ── SEND A VISITOR (ecard.html) ── */
.ecard{--ink:#0a0d24;--plum:#2b1a52;--acid:#7dff9b;--rose:#ff8fd0;--paper:#f6efe2;--mist:#c3b6dc;
background:radial-gradient(110% 92% at 24% 16%,rgba(255,143,208,.26),transparent 60%),
radial-gradient(100% 85% at 84% 88%,rgba(125,255,155,.20),transparent 62%),
linear-gradient(158deg,var(--plum) 0%,var(--ink) 74%);
border:1px solid rgba(255,143,208,.30);box-shadow:0 16px 44px rgba(0,0,0,.5)}
.ecard:hover{border-color:rgba(255,143,208,.68);box-shadow:0 22px 58px rgba(255,143,208,.24)}
.ecard .eyebrow{color:var(--rose)}
.ecard h3{background:linear-gradient(100deg,#fff,var(--rose) 46%,var(--acid));
-webkit-background-clip:text;background-clip:text;color:transparent}
.ecard .sub{color:var(--mist)}
.ecard .go{background:linear-gradient(96deg,var(--rose),var(--acid));color:#1a0716;
box-shadow:0 5px 18px rgba(255,143,208,.36)}
.env{width:104px;height:86px;position:relative}
.envb{position:absolute;bottom:4px;left:50%;margin-left:-46px;width:92px;height:54px;border-radius:7px;
background:linear-gradient(180deg,var(--paper),#d6c9b2);box-shadow:0 7px 20px rgba(0,0,0,.45)}
.flap{position:absolute;bottom:30px;left:50%;margin-left:-46px;width:92px;height:28px;z-index:4;
clip-path:polygon(0 0,50% 100%,100% 0);background:linear-gradient(180deg,#e9dfc9,#c9baa0)}
.mini{position:absolute;top:15px;left:50%;margin-left:-23px;width:46px;height:14px;border-radius:50%;z-index:2;
background:linear-gradient(180deg,#e6eef8,#7c93b3);box-shadow:0 0 16px rgba(125,255,155,.7);
animation:lift 3.4s ease-in-out infinite}
.mini:before{content:"";position:absolute;left:50%;margin-left:-11px;top:-11px;width:22px;height:15px;
border-radius:50% 50% 40% 40%;border:1px solid rgba(255,255,255,.4);
background:radial-gradient(ellipse at 40% 28%,#fff,rgba(125,255,155,.55))}
.mini:after{content:"";position:absolute;left:50%;margin-left:-4px;top:-6px;width:8px;height:9px;
border-radius:50% 50% 44% 44%;background:var(--acid);box-shadow:0 0 7px rgba(125,255,155,.9)}
.trail{position:absolute;top:30px;left:50%;margin-left:-2px;width:4px;height:22px;z-index:1}
.trail i{position:absolute;left:0;width:4px;height:4px;border-radius:50%;background:var(--acid);
opacity:.5;animation:trail 2.2s ease-in-out infinite}
.trail i:nth-child(1){top:0}
.trail i:nth-child(2){top:8px;animation-delay:.35s}
.trail i:nth-child(3){top:16px;animation-delay:.7s}

@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
@keyframes bobship{0%,100%{transform:scale(1.62) translateY(0)}
50%{transform:scale(1.62) translateY(-5px)}}
@keyframes blink{0%,100%{opacity:.32}50%{opacity:1}}
@keyframes beamPulse{0%,100%{opacity:.42}50%{opacity:.88}}
@keyframes lift{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
@keyframes trail{0%,100%{opacity:.15;transform:scale(.7)}50%{opacity:.75;transform:scale(1)}}
/* ── THE CONE (cone.html) ── */
.cone{--cream:#fff1e2;--peach:#ffd3bd;--sorbet:#ffb8a8;--mint:#58c9a8;--berry:#ff5d7e;
background:radial-gradient(115% 95% at 24% 16%,rgba(255,184,168,.30),transparent 60%),
radial-gradient(100% 85% at 84% 88%,rgba(88,201,168,.22),transparent 62%),
linear-gradient(158deg,#3f231a 0%,#180c08 74%);
border:1px solid rgba(255,184,168,.30);box-shadow:0 16px 44px rgba(0,0,0,.5)}
.cone:hover{border-color:rgba(255,184,168,.70);box-shadow:0 22px 58px rgba(255,93,126,.24)}
.cone .eyebrow{color:var(--sorbet)}
.cone h3{background:linear-gradient(100deg,var(--cream),var(--peach) 42%,var(--berry));
-webkit-background-clip:text;background-clip:text;color:transparent}
.cone .sub{color:#d9bfae}
.cone .go{background:linear-gradient(96deg,var(--berry),var(--sorbet));color:#2a0a12;
box-shadow:0 5px 18px rgba(255,93,126,.38)}
.cone-art{width:104px;height:94px;position:relative;animation:wobble 4.2s ease-in-out infinite;
transform-origin:50% 92%}
.cherry{position:absolute;top:0;left:50%;margin-left:-7px;width:14px;height:14px;border-radius:50%;
background:radial-gradient(circle at 34% 28%,#ff9fb2,var(--berry));
box-shadow:0 0 9px rgba(255,93,126,.65)}
.scoop{position:absolute;left:50%;border-radius:50%;box-shadow:inset 0 -5px 10px rgba(0,0,0,.14)}
.scoop.b{top:11px;margin-left:-23px;width:46px;height:39px;
background:radial-gradient(ellipse at 34% 26%,#b6f3de,var(--mint))}
.scoop.a{top:33px;margin-left:-30px;width:60px;height:43px;
background:radial-gradient(ellipse at 34% 26%,#ffe2d6,var(--sorbet))}
.drip{position:absolute;top:64px;left:50%;margin-left:16px;width:10px;height:15px;
border-radius:0 0 60% 60%;background:var(--sorbet);opacity:.9;
animation:melt 3.8s ease-in-out infinite}
.waffle{position:absolute;top:68px;left:50%;margin-left:-23px;width:46px;height:26px;
clip-path:polygon(0 0,100% 0,50% 100%);
background:linear-gradient(180deg,#e8a866,#a9622c),
repeating-linear-gradient(58deg,rgba(90,45,18,.35) 0 2px,transparent 2px 7px)}
.waffle:after{content:"";position:absolute;inset:0;
background:repeating-linear-gradient(-58deg,rgba(90,45,18,.30) 0 2px,transparent 2px 7px)}

@keyframes wobble{0%,100%{transform:rotate(-3.5deg)}50%{transform:rotate(3.5deg)}}
@keyframes melt{0%,100%{transform:scaleY(.72);opacity:.75}50%{transform:scaleY(1.1);opacity:1}}
/* ── MOON SHOT (moon-shot.html) ── */
.moon{--ink:#050818;--indigo:#141d47;--silver:#e8eeff;--gold:#ffd166;--cyan:#22e0ff;--mist:#a6b0d8;
background:radial-gradient(110% 92% at 76% 16%,rgba(232,238,255,.18),transparent 58%),
radial-gradient(100% 85% at 18% 88%,rgba(34,224,255,.18),transparent 62%),
linear-gradient(158deg,var(--indigo) 0%,var(--ink) 74%);
border:1px solid rgba(255,209,102,.28);box-shadow:0 16px 44px rgba(0,0,0,.55)}
.moon:hover{border-color:rgba(255,209,102,.66);box-shadow:0 22px 58px rgba(34,224,255,.22)}
.moon .eyebrow{color:var(--gold)}
.moon h3{background:linear-gradient(100deg,#fff,var(--silver) 40%,var(--gold));
-webkit-background-clip:text;background-clip:text;color:transparent}
.moon .sub{color:var(--mist)}
.moon .go{background:linear-gradient(96deg,var(--gold),var(--cyan));color:#0a1020;
box-shadow:0 5px 18px rgba(255,209,102,.34)}
.luna{width:96px;height:88px;position:relative}
.rock{position:absolute;top:6px;right:4px;width:56px;height:56px;border-radius:50%;
background:radial-gradient(circle at 34% 28%,#fbfdff,#c3cde8 52%,#7f8bb4);
box-shadow:0 0 22px rgba(232,238,255,.34)}
.rock:before,.rock:after{content:"";position:absolute;border-radius:50%;background:rgba(96,108,150,.42)}
.rock:before{top:14px;left:12px;width:13px;height:13px}
.rock:after{bottom:12px;right:14px;width:9px;height:9px}
.pellet{position:absolute;bottom:10px;left:6px;width:11px;height:11px;border-radius:50%;
background:var(--gold);box-shadow:0 0 12px rgba(255,209,102,.9);
animation:shoot 3.2s cubic-bezier(.4,0,.7,1) infinite}
.arc{position:absolute;bottom:14px;left:14px;width:58px;height:44px}
.arc i{position:absolute;width:3px;height:3px;border-radius:50%;background:var(--cyan);opacity:.5}
.arc i:nth-child(1){left:6%;bottom:6%}
.arc i:nth-child(2){left:28%;bottom:36%}
.arc i:nth-child(3){left:54%;bottom:60%}
.arc i:nth-child(4){left:80%;bottom:76%}

/* ── SONG MAKER (songmaker.html) ── */
.song{--ink:#08061a;--deep:#1d0f3d;--magenta:#ff44cc;--cyan:#22e0ff;--gold:#ffd166;--mist:#bdb2dc;
background:radial-gradient(112% 92% at 22% 18%,rgba(255,68,204,.26),transparent 60%),
radial-gradient(100% 85% at 82% 86%,rgba(34,224,255,.20),transparent 62%),
linear-gradient(158deg,var(--deep) 0%,var(--ink) 74%);
border:1px solid rgba(34,224,255,.28);box-shadow:0 16px 44px rgba(0,0,0,.5)}
.song:hover{border-color:rgba(34,224,255,.66);box-shadow:0 22px 58px rgba(255,68,204,.24)}
.song .eyebrow{color:var(--cyan)}
.song h3{background:linear-gradient(100deg,#fff,var(--cyan) 42%,var(--magenta));
-webkit-background-clip:text;background-clip:text;color:transparent}
.song .sub{color:var(--mist)}
.song .go{background:linear-gradient(96deg,var(--cyan),var(--magenta));color:#0b0518;
box-shadow:0 5px 18px rgba(34,224,255,.34)}
.seq{width:92px;height:88px;position:relative;display:grid;grid-template-columns:repeat(4,1fr);
grid-template-rows:repeat(4,1fr);gap:5px;padding:5px;border-radius:11px;
background:rgba(255,255,255,.05);border:1px solid rgba(34,224,255,.22)}
.seq i{border-radius:4px;background:rgba(255,255,255,.07)}
.seq i.on{background:var(--magenta);box-shadow:0 0 9px rgba(255,68,204,.75);
animation:step 2.4s ease-in-out infinite}
.seq i.on.c{background:var(--cyan);box-shadow:0 0 9px rgba(34,224,255,.75)}
.seq i:nth-child(2).on{animation-delay:.3s}
.seq i:nth-child(7).on{animation-delay:.6s}
.seq i:nth-child(12).on{animation-delay:.9s}
.seq i:nth-child(13).on{animation-delay:1.2s}

/* keep the taller art pieces inside a two-up row */
.cta-row .cone-art{transform:scale(.86);transform-origin:center}
.cta-row .shrine{transform:scale(.82);transform-origin:center}

@keyframes shoot{0%{transform:translate(0,0) scale(1);opacity:1}
70%{transform:translate(52px,-46px) scale(.55);opacity:.85}
100%{transform:translate(56px,-50px) scale(.2);opacity:0}}
@keyframes step{0%,100%{opacity:.5;transform:scale(.9)}50%{opacity:1;transform:scale(1)}}
@media(prefers-reduced-motion:reduce){
  .saucer,.blinks i,.beam,.mini,.trail i,.cone-art,.drip,.pellet,.seq i.on{animation:none}
  .ship .saucer{animation:none;transform:scale(1.62)}
}'''

CTA_JS = r'''(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var e = document.querySelector('.emb');
  if (e) { var h=''; for (var i=0;i<(reduce?0:26);i++){
    h += '<i style="left:'+(6+Math.random()*88).toFixed(1)+'%;animation-delay:'
      +(Math.random()*5.5).toFixed(2)+'s;animation-duration:'+(4+Math.random()*3).toFixed(1)+'s"></i>'; }
    e.innerHTML=h; }
  var r = document.querySelector('.rays');
  if (r) { var h3=''; for (var k=0;k<(reduce?0:20);k++){
    h3 += '<i style="left:'+(6+Math.random()*88).toFixed(1)+'%;bottom:'+(8+Math.random()*40).toFixed(0)
      +'%;animation-delay:'+(Math.random()*6).toFixed(2)+'s"></i>'; }
    r.innerHTML=h3; }
  var n = document.querySelector('.notes');
  if (n) { var g=['\u266a','\u266b','\u266c','\u2669'], h2='';
    for (var j=0;j<(reduce?0:16);j++){
      h2 += '<i style="left:'+(8+Math.random()*84).toFixed(1)+'%;bottom:'
        +(10+Math.random()*30).toFixed(0)+'%;animation-delay:'+(Math.random()*6).toFixed(2)+'s">'
        +g[j%4]+'</i>'; }
    n.innerHTML=h2; }
})();
(function(){
  var g = document.querySelector('.glit');
  if (!g) return;
  var n = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 14 : 46;
  var html = '';
  for (var i = 0; i < n; i++) {
    html += '<i style="left:' + (Math.random()*100).toFixed(2) + '%;top:'
         + (Math.random()*100).toFixed(2) + '%;animation-delay:'
         + (Math.random()*3.4).toFixed(2) + 's"></i>';
  }
  g.innerHTML = html;
})();'''

CTAS = {
  'hearth': r'''<a class="cta hearth" href="fireplace.html">
  <div class="emb" aria-hidden="true"></div><div class="sheen" aria-hidden="true"></div>
  <div class="in">
    <div class="art"><div class="hstack"><div class="pool"></div><div class="log a"></div><div class="log b"></div><div class="fire"></div></div></div>
    <div>
      <div class="eyebrow">✦ Extended Universe ✦</div>
      <h3>The Hearth</h3>
      <div class="sub">Pull up a chair. The fire's going, the room is warm,
        and nothing out there needs you for a while.</div>
      <div class="go"><span>Sit by the fire</span><span>→</span></div>
    </div>
  </div>
</a>''',
  'oracle': r'''<a class="cta globe" href="https://magickmica.github.io/oracle/">
  <div class="sheen" aria-hidden="true"></div>
  <div class="in">
    <div class="art"><div class="orb"></div><div class="stand"></div></div>
    <div>
      <div class="eyebrow">✦ 🕯️ Ancient starlight · modern pixels 🕯️ ✦</div>
      <h3>Cosmic Crystal Oracle</h3>
      <div class="sub">Think of a yes or no question. Don't say it out loud —
        the universe is already listening. Then touch the crystal.</div>
      <div class="go"><span>Touch the crystal</span><span>→</span></div>
    </div>
  </div>
</a>''',
  'mbox': r'''<a class="cta mbox" href="https://magickmica.github.io/musicbox/">
  <div class="notes" aria-hidden="true"></div><div class="sheen" aria-hidden="true"></div>
  <div class="in">
    <div class="art"><div class="box">
      <div class="ballerina"></div><div class="lid"></div><div class="base"></div>
    </div></div>
    <div>
      <div class="eyebrow">✦ Play &amp; Listen ✦</div>
      <h3>The Music Box</h3>
      <div class="sub">Lift the lid and something starts turning. Small sounds,
        slow spins, and a tune that knows where it's going.</div>
      <div class="go"><span>Wind it up</span><span>→</span></div>
    </div>
  </div>
</a>''',
  'two': r'''<a class="cta two" href="abundance-oracle.html">
  <div class="rays" aria-hidden="true"></div><div class="sheen" aria-hidden="true"></div>
  <div class="in">
    <div class="art"><div class="shrine">
      <div class="col l"></div><div class="col r"></div>
      <div class="eye"><svg viewBox="0 0 64 40" fill="none" aria-hidden="true">
        <path d="M4 22 C16 6, 44 6, 58 20" stroke="#e0b64c" stroke-width="2.6" stroke-linecap="round"/>
        <circle cx="31" cy="20" r="9.5" fill="#3fb3a6"/>
        <circle cx="31" cy="20" r="4" fill="#0b1026"/>
        <path d="M31 30 l-4 9" stroke="#e0b64c" stroke-width="2.4" stroke-linecap="round"/>
        <path d="M40 29 c4 5, 6 8, 5 11" stroke="#c05a3c" stroke-width="2.4" stroke-linecap="round"/>
      </svg></div>
    </div></div>
    <div>
      <div class="eyebrow">✦ 100 Signs ✦</div>
      <h3>Oracle of the Two Lands</h3>
      <div class="sub">Step between the columns and put your question to the old gods.
        They answer in signs, and they have a hundred of them.</div>
      <div class="go"><span>Enter the shrine</span><span>→</span></div>
    </div>
  </div>
</a>''',
  'wand': r'''<a class="wand-cta" href="wand.html">
  <div class="glit" aria-hidden="true"></div>
  <div class="sheen" aria-hidden="true"></div>
  <div class="in">
    <div class="orb">
      <svg viewBox="0 0 24 24" fill="none" stroke="#fdeaf6" stroke-width="1.6"
           stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M4 20 L15 9"/>
        <path d="M15 9 l1.6-1.6 2.4 2.4 L17.4 11.4 z" fill="#ffd9a0" stroke="#ffd9a0"/>
        <path d="M18.4 3.2l.6 1.5 1.5.6-1.5.6-.6 1.5-.6-1.5-1.5-.6 1.5-.6z" fill="#ff5fa8" stroke="none"/>
        <path d="M7.6 4.4l.45 1.1 1.1.45-1.1.45-.45 1.1-.45-1.1L6.05 5.95l1.1-.45z" fill="#c48cff" stroke="none"/>
        <path d="M20.6 12.6l.4 1 1 .4-1 .4-.4 1-.4-1-1-.4 1-.4z" fill="#fdeaf6" stroke="none"/>
      </svg>
    </div>
    <div>
      <div class="eyebrow">✦ Extended Universe · CH 07 ✦</div>
      <h3>Wave the Wand</h3>
      <div class="sub">One flick and the screen remembers it's magic. Sparks, shimmer,
        and a little chaos — go make something glitter.</div>
      <div class="go"><span>Cast a spell</span><span>→</span></div>
    </div>
  </div>
</a>''',
  'ship': r'''<a class="cta ship" href="alien.html">
  <div class="sheen" aria-hidden="true"></div>
  <div class="in">
    <div class="art"><div class="saucer">
      <div class="beam"></div><div class="hull"></div>
      <div class="dome"></div><div class="pilot"></div>
      <div class="blinks"><i></i><i></i><i></i></div>
      <div class="glow"></div>
    </div></div>
    <div>
      <div class="eyebrow">✦ Extended Universe ✦</div>
      <h3>The Visitor</h3>
      <div class="sub">Parked above the field again. Small green pilot, no explanation.</div>
      <div class="go"><span>Look up</span><span>→</span></div>
    </div>
  </div>
</a>''',
  'ecard': r'''<a class="cta ecard" href="ecard.html">
  <div class="sheen" aria-hidden="true"></div>
  <div class="in">
    <div class="art"><div class="env">
      <div class="mini"></div><div class="trail"><i></i><i></i><i></i></div>
      <div class="envb"></div><div class="flap"></div>
    </div></div>
    <div>
      <div class="eyebrow">✦ Send a Transmission ✦</div>
      <h3>Send a Visitor</h3>
      <div class="sub">Pick a messenger, write a line, beam it into somebody's day.</div>
      <div class="go"><span>Send one out</span><span>→</span></div>
    </div>
  </div>
</a>''',
  'cone': r'''<a class="cta cone" href="cone.html">
  <div class="sheen" aria-hidden="true"></div>
  <div class="in">
    <div class="art"><div class="cone-art">
      <div class="cherry"></div>
      <div class="scoop b"></div><div class="scoop a"></div>
      <div class="drip"></div><div class="waffle"></div>
    </div></div>
    <div>
      <div class="eyebrow">✦ Extended Universe ✦</div>
      <h3>The Cone</h3>
      <div class="sub">Spin it, pick a flavor, don't leave it in the sun.</div>
      <div class="go"><span>Spin the cone</span><span>→</span></div>
    </div>
  </div>
</a>''',
  'moon': r'''<a class="cta moon" href="moon-shot.html">
  <div class="sheen" aria-hidden="true"></div>
  <div class="in">
    <div class="art"><div class="luna">
      <div class="rock"></div>
      <div class="arc"><i></i><i></i><i></i><i></i></div>
      <div class="pellet"></div>
    </div></div>
    <div>
      <div class="eyebrow">✦ Play ✦</div>
      <h3>Moon Shot</h3>
      <div class="sub">Drag back from the moon and let go. Three misses ends the night.</div>
      <div class="go"><span>Take the shot</span><span>→</span></div>
    </div>
  </div>
</a>''',
  'song': r'''<a class="cta song" href="songmaker.html">
  <div class="sheen" aria-hidden="true"></div>
  <div class="in">
    <div class="art"><div class="seq">
      <i></i><i class="on"></i><i></i><i class="on c"></i>
      <i></i><i></i><i class="on"></i><i></i>
      <i class="on c"></i><i></i><i></i><i class="on"></i>
      <i class="on"></i><i></i><i class="on c"></i><i></i>
    </div></div>
    <div>
      <div class="eyebrow">✦ Play &amp; Listen ✦</div>
      <h3>Cosmic Song Maker</h3>
      <div class="sub">Tap the grid, build a loop, let the whole thing run.</div>
      <div class="go"><span>Make a song</span><span>→</span></div>
    </div>
  </div>
</a>''',
}
