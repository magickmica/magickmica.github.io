/* MAGICKMICA · mm-prizes.js
   One prize shelf for every Cosmic Circus midway game. Saved only in the
   visitor's own browser (localStorage), so nothing is sent anywhere.

   MMPrizes.pick(tier)            -> {e, n, tier}   a random prize of that size
   MMPrizes.add(prize, game)      -> stores it, fires a "mm-prizes" event
   MMPrizes.read()                -> every prize won, oldest first
   MMPrizes.tokens() / addToken() / useToken()   bonus spins for the Prize Wheel
   MMPrizes.tickets() / addTickets(n, game) / spendTickets(n)
                                  circus tickets, earned in every game, spent at the Ticket Booth
   MMPrizes.owned() / collect(item)   collectibles traded for at the Ticket Booth
   MMPrizes.render(el, opts)      -> draws a shelf into el
*/
(function () {
  'use strict';
  var KEY = 'mm_prizes_v1', TOK = 'mm_prize_tokens_v1', OLD = 'mm_clownsplash_v1', MAX = 150,
      TIX = 'mm_tickets_v1', OWN = 'mm_collect_v1', PER = {small: 5, medium: 15, jumbo: 40};

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
    if (PER[prize.tier]) addTickets(PER[prize.tier], game); else fire();
    return prize;
  }

  /* circus tickets: every prize pays some, and games hand out a few for playing */
  function tickets() { return +get(TIX, 0) || 0; }
  function addTickets(n, game) {
    n = Math.max(0, Math.round(n || 0)); if (!n) return tickets();
    set(TIX, Math.min(99999, tickets() + n)); fire(); toast(n);
    return tickets();
  }
  function spendTickets(n) { var t = tickets(); if (n > t) return false; set(TIX, t - n); fire(); return true; }
  function owned() { var o = get(OWN, []); return Array.isArray(o) ? o : []; }
  function collect(item) {
    var o = owned(); if (o.indexOf(item.id) < 0) { o.push(item.id); set(OWN, o); }
    add({e: item.e, n: item.n, tier: 'rare'}, 'Ticket Booth');
  }

  var tEl = null, tTimer = 0, tSum = 0;
  function toast(n) {
    if (!document.body) return;
    try {
      if (!tEl) {
        tEl = document.createElement('div');
        tEl.setAttribute('role', 'status');
        tEl.style.cssText = 'position:fixed;right:14px;bottom:14px;z-index:9999;pointer-events:none;font:12px/1 Silkscreen,monospace;' +
          'letter-spacing:.12em;color:#040509;background:linear-gradient(90deg,#ffd166,#ff4fa3);padding:9px 13px;border-radius:999px;' +
          'box-shadow:0 0 18px rgba(255,209,102,.55);transition:opacity .3s,transform .3s;opacity:0;transform:translateY(8px)';
        document.body.appendChild(tEl);
      }
      tSum = tEl.style.opacity === '1' ? tSum + n : n;
      tEl.textContent = '🎟 +' + tSum + ' TICKET' + (tSum === 1 ? '' : 'S');
      tEl.style.opacity = '1'; tEl.style.transform = 'none';
      clearTimeout(tTimer);
      tTimer = setTimeout(function () { tEl.style.opacity = '0'; tEl.style.transform = 'translateY(8px)'; }, 2200);
    } catch (e) {}
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

  window.MMPrizes = {CAT: CAT, PER: PER, read: read, pick: pick, add: add, tokens: tokens, addToken: addToken, useToken: useToken,
    tickets: tickets, addTickets: addTickets, spendTickets: spendTickets, owned: owned, collect: collect, render: render};
})();
