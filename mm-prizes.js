/* MAGICKMICA · mm-prizes.js
   One prize shelf for every Cosmic Circus midway game. Saved only in the
   visitor's own browser (localStorage), so nothing is sent anywhere.

   MMPrizes.pick(tier)            -> {e, n, tier}   a random prize of that size
   MMPrizes.add(prize, game)      -> stores it, fires a "mm-prizes" event
   MMPrizes.read()                -> every prize won, oldest first
   MMPrizes.tokens() / addToken() / useToken()   bonus spins for the Prize Wheel
   MMPrizes.render(el, opts)      -> draws a shelf into el
*/
(function () {
  'use strict';
  var KEY = 'mm_prizes_v1', TOK = 'mm_prize_tokens_v1', OLD = 'mm_clownsplash_v1', MAX = 150;

  var CAT = {
    small:  [['🛸','UFO keychain'],['⭐','Glow-in-the-dark star'],['💎','Pocket crystal'],['☄️','Comet sticker'],
             ['🍦','Mini cosmic cone'],['🔮','Tiny crystal ball'],['🌙','Moon charm'],['🍬','Stardust candy'],
             ['🎀','Holo hair bow'],['🪀','Glitter yo-yo']],
    medium: [['👽','Plush Visitor'],['🪐','Squishy Saturn'],['🦄','Holo unicorn'],['🐙','Space octopus plush'],
             ['🧸','Starlight bear'],['🦋','Moth of many colors'],['🐸','Cosmic frog plush']],
    jumbo:  [['🌈','JUMBO rainbow worm'],['🐉','GIANT dream dragon'],['🦩','ENORMOUS flamingo'],
             ['🐳','Whale of a whale'],['🦖','Space dino, extra large']]
  };

  function get(key, fallback) {
    try { var v = localStorage.getItem(key); return v == null ? fallback : JSON.parse(v); } catch (e) { return fallback; }
  }
  function set(key, val) { try { localStorage.setItem(key, JSON.stringify(val)); } catch (e) {} }

  function read() {
    var list = get(KEY, null);
    if (!Array.isArray(list)) {
      // first visit since the shared shelf: bring over Clown Splash prizes
      list = [];
      var old = get(OLD, {});
      (old && old.prizes || []).forEach(function (p) { list.push({e: p.e, n: p.n, tier: p.tier, g: 'Clown Splash'}); });
      set(KEY, list);
    }
    return list;
  }
  function pick(tier) {
    var l = CAT[tier] || CAT.small, p = l[Math.floor(Math.random() * l.length)];
    return {e: p[0], n: p[1], tier: CAT[tier] ? tier : 'small'};
  }
  function add(prize, game) {
    var list = read();
    list.push({e: prize.e, n: prize.n, tier: prize.tier, g: game || '', t: Date.now()});
    while (list.length > MAX) list.shift();
    set(KEY, list);
    fire();
    return prize;
  }
  function tokens() { return +get(TOK, 0) || 0; }
  function addToken(n) { set(TOK, Math.min(99, tokens() + (n || 1))); fire(); }
  function useToken() { var t = tokens(); if (t <= 0) return false; set(TOK, t - 1); fire(); return true; }
  function fire() { try { window.dispatchEvent(new CustomEvent('mm-prizes')); } catch (e) {} }

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function render(el, opts) {
    if (!el) return;
    opts = opts || {};
    var list = read();
    if (!list.length) { el.innerHTML = '<span class="empty">' + esc(opts.empty || 'Nothing yet. The shelf is waiting.') + '</span>'; return; }
    var show = opts.limit ? list.slice(-opts.limit) : list;
    el.innerHTML = show.map(function (p) {
      return '<span class="it ' + esc(p.tier) + '" title="' + esc(p.n + (p.g ? ' · won at ' + p.g : '')) + '">' + esc(p.e) + '</span>';
    }).join('');
  }

  window.MMPrizes = {CAT: CAT, read: read, pick: pick, add: add, tokens: tokens, addToken: addToken, useToken: useToken, render: render};
})();
