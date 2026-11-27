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
   MMPrizes.daily()               -> {fresh, streak, tickets, spin}  once-a-day visit prize
   MMPrizes.dupes() / tradeIn(e, n) / tradeValue(p)   swap extra prizes for tickets
   MMPrizes.pick(tier, 'winter')  -> a Winter Carnival holiday prize
   Advent prizes (tier 'advent') come one per door from circus-advent.html and are never traded in.
   Every shelf drawn with render() gets a link to my-prizes.html, the full collection page.
*/
(function () {
  'use strict';
  var KEY = 'mm_prizes_v1', TOK = 'mm_prize_tokens_v1', OLD = 'mm_clownsplash_v1', MAX = 150,
      TIX = 'mm_tickets_v1', OWN = 'mm_collect_v1', DAY = 'mm_daily_v1', PER = {small: 5, medium: 15, jumbo: 40};

  var CAT = {
    small:  [['🛸','UFO keychain'],['⭐','Glow-in-the-dark star'],['💎','Pocket crystal'],['☄️','Comet sticker'],
             ['🍦','Mini cosmic cone'],['🔮','Tiny crystal ball'],['🌙','Moon charm'],['🍬','Stardust candy'],
             ['🎀','Holo hair bow'],['🪀','Glitter yo-yo'],['🍪','Moon cookie'],['🐞','Lucky ladybug'],['🍀','Four-leaf clover pin'],
             ['🫧','Bubble wand'],['🎈','Star balloon'],['🌸','Space blossom'],['🪁','Comet kite'],['🍡','Planet mochi'],
             ['🧩','Puzzle of the stars'],['🐣','Baby star chick'],['🫐','Galaxy berries'],['🔔','Tiny moon bell'],
             ['🍉','Moon melon slice'],['🐌','Glitter snail'],['🌻','Sunflower sticker'],['🍒','Twin-star cherries'],
             ['🐝','Buzzy bee pin'],['🥨','Pretzel of Orion'],['🪸','Coral charm'],['🌺','Hibiscus star clip'],
             ['🍧','Shaved ice of Saturn'],['🥤','Comet soda'],['🍿','Big Top popcorn'],['🧇','Waffle moon'],['🍋','Lemon comet drop'],
             ['🪙','Lucky star coin'],['🌼','Daisy chain charm'],['🐟','Goldfish in a bag'],['🍥','Swirl cake of Jupiter'],['🥏','Flying saucer frisbee'],
             ['🎯','Bullseye badge'],['🌷','Tulip of Mars'],['🦀','Crab of Cancer'],['🍫','Chocolate planet bar'],['🐛','Caterpillar sticker']],
    medium: [['👽','Plush Visitor'],['🪐','Squishy Saturn'],['🦄','Holo unicorn'],['🐙','Space octopus plush'],
             ['🧸','Starlight bear'],['🦋','Moth of many colors'],['🐸','Cosmic frog plush'],['🐱','Moon cat plush'],
             ['🐰','White rabbit plush'],['🦊','Aurora fox'],['🐧','Astronaut penguin'],['🦔','Stardust hedgehog'],
             ['🐼','Pastel panda'],['🦭','Sea-of-stars seal'],['🐨','Koala cosmonaut'],
             ['🐶','Space-helmet pup'],['🐷','Piglet of the planets'],['🦦','Aurora otter'],['🐢','Turtle of time'],['🐹','Hamster astronaut'],
             ['🦝','Raccoon of the rings'],['🐿️','Moon squirrel'],['🦥','Sleepy sloth plush'],['🐑','Cloud sheep plush'],['🐭','Mouse in a teacup'],
             ['🦙','Llama of the Milky Way'],['🐮','Moo-n cow plush'],['🦆','Rubber star duck'],['🐻','Honey bear plush'],['🐒','Space monkey plush']],
    jumbo:  [['🌈','JUMBO rainbow worm'],['🐉','GIANT dream dragon'],['🦩','ENORMOUS flamingo'],
             ['🐳','Whale of a whale'],['🦖','Space dino, extra large'],['🦒','TOWERING giraffe'],
             ['🐘','MIGHTY Big Top elephant'],['🦁','GRAND Ringmaster lion'],['🦕','GIANT brontosaurus'],
             ['🐻‍❄️','ENORMOUS polar bear'],['🦜','GIGANTIC rainbow parrot'],
             ['🦈','HUGE sky shark'],['🐅','ROARING ring tiger'],['🦓','MAJESTIC star zebra'],['🦬','COLOSSAL star bison'],
             ['🦍','GIANT gentle gorilla'],['🦘','BOUNCING kangaroo XL'],['🦛','HUGE hippo hug'],['🐊','ENORMOUS moon gator'],
             ['🐆','GIANT leopard of light'],['🦤','GIANT dodo, extra rare'],['🦏','MIGHTY rhino of Mars']]
  };

  var WINTER = {
    small:  [['❄️','Snowflake charm'],['🧤','Star-knit mittens'],['🍪','Gingerbread comet'],['🔔','Sleigh bell'],['🕯️','Peppermint candle'],
             ['🍬','Candy cane rocket'],['🧦','Fuzzy moon socks'],['☃️','Snow globe sticker'],
             ['⛸️','Starlight skates'],['🎿','Comet skis'],['☕','Cocoa cup charm']],
    medium: [['⛄','Snowman plush'],['🐧','Penguin in a scarf'],['🦌','Starlight reindeer'],['🐻‍❄️','Polar cub plush'],['🧣','Aurora scarf'],['🎄','Tiny cosmic tree'],['🦊','Snow fox plush'],['🧸','Snuggle bear in a hat']],
    jumbo:  [['🦌','GIANT glowing reindeer'],['⛄','ENORMOUS snow friend'],['🐻‍❄️','HUGE polar bear hug'],['🛷','JUMBO comet sleigh'],['🎁','GIANT surprise present']]
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
  function pick(tier, set) {
    var C = set === 'winter' ? WINTER : CAT;
    var l = C[tier] || C.small, p = l[Math.floor(Math.random() * l.length)];
    return {e: p[0], n: p[1], tier: C[tier] ? tier : 'small'};
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

  /* once-a-day visit prize: 10 tickets, +5 for every day in a row (up to 40), and a bonus wheel spin every 7th day */
  function dayKey(d) { return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate(); }
  function daily() {
    var now = new Date(), today = dayKey(now), y = new Date(now); y.setDate(y.getDate() - 1);
    var d = get(DAY, {last: '', streak: 0});
    if (d.last === today) return {fresh: false, streak: d.streak};
    d.streak = d.last === dayKey(y) ? d.streak + 1 : 1; d.last = today; set(DAY, d);
    var n = 10 + Math.min(d.streak - 1, 6) * 5, spin = d.streak % 7 === 0;
    addTickets(n, 'Daily visit'); if (spin) addToken(1);
    return {fresh: true, streak: d.streak, tickets: n, spin: spin};
  }
  function dailyCard() {
    var r = daily(); if (!r.fresh || !document.body) return r;
    try {
      var el = document.createElement('div');
      el.setAttribute('role', 'dialog'); el.setAttribute('aria-label', 'Daily visit prize');
      /* on a game, the bottom of the screen is where you play (the mug, the ramp, the hoop),
         so the card goes to the top there and steps aside as soon as you start playing;
         the lobby pages keep it at the bottom */
      var page = (location.pathname.split('/').pop() || 'index.html').toLowerCase(),
          lobby = /^(index|arcade|my-prizes|ticket-booth|winter-carnival|circus-advent)(\.html)?$/.test(page);
      el.style.cssText = 'position:fixed;left:50%;' + (lobby ? 'bottom:18px;' : 'top:calc(12px + env(safe-area-inset-top,0px));') +
        'transform:translateX(-50%);z-index:10000;width:min(360px,calc(100vw - 32px));' +
        'padding:16px 18px 14px;border-radius:18px;text-align:center;color:#fff;font:14px/1.45 "IBM Plex Mono",monospace;' +
        'background:linear-gradient(160deg,#2f2f70,#131c3f);border:2px solid #ffd166;box-shadow:0 0 0 4px rgba(4,5,9,.6),0 18px 50px rgba(0,0,0,.6),0 0 40px rgba(255,209,102,.3)';
      var dots = '';
      for (var i = 1; i <= 7; i++) dots += '<span style="display:inline-block;width:22px;height:22px;line-height:22px;margin:0 2px;border-radius:50%;font-size:11px;' +
        ((((r.streak - 1) % 7) + 1) >= i ? 'background:#ffd166;color:#040509' : 'background:rgba(255,255,255,.1);color:#d5c2dc') + '">' + (i === 7 ? '🎡' : i) + '</span>';
      el.innerHTML = '<div style="font:11px Silkscreen,monospace;letter-spacing:.2em;color:#5ff3e8">★ DAILY VISIT PRIZE ★</div>' +
        '<div style="font:900 28px Orbitron,sans-serif;margin:6px 0 2px;color:#ffd166;text-shadow:0 0 16px rgba(255,209,102,.6)">🎟 +' + r.tickets + '</div>' +
        '<div style="color:#d5c2dc">' + (r.streak > 1 ? 'Day ' + r.streak + ' in a row! Come back tomorrow for more.' : 'Welcome back to the circus! Visit every day to grow your streak.') +
        (r.spin ? '<br><b style="color:#ff4fa3">7-day streak: a free bonus spin on the Prize Wheel!</b>' : '') + '</div>' +
        '<div style="margin:10px 0 8px">' + dots + '</div>' +
        '<button type="button" style="font:12px Silkscreen,monospace;letter-spacing:.12em;padding:9px 18px;border-radius:999px;border:0;cursor:pointer;color:#040509;background:linear-gradient(90deg,#ffd166,#ff4fa3)">YAY! ✨</button>';
      function close() {
        if (el.parentNode) el.remove();
        document.removeEventListener('pointerdown', onPlay, true);
        document.removeEventListener('keydown', onPlay, true);
      }
      function onPlay(e) { if (!el.contains(e.target)) close(); }
      el.querySelector('button').onclick = close;
      document.body.appendChild(el);
      if (!lobby) {
        document.addEventListener('pointerdown', onPlay, true);
        document.addEventListener('keydown', onPlay, true);
      }
      setTimeout(close, 12000);
    } catch (e) {}
    return r;
  }

  /* trading extra prizes back for tickets */
  var TRADE = {small: 2, medium: 6, jumbo: 15};
  function tradeValue(p) {
    if (p.tier === 'rare') { var c = (window.MMRareCost || {})[p.n]; return Math.max(5, Math.round((c || 40) * .3)); }
    return TRADE[p.tier] || 0;
  }
  function dupes() {
    var groups = {}, order = [];
    read().forEach(function (p) {
      if (p.tier === 'fortune' || p.tier === 'advent') return;
      var k = p.e + '|' + p.n;
      if (!groups[k]) { groups[k] = {e: p.e, n: p.n, tier: p.tier, count: 0}; order.push(k); }
      groups[k].count++;
    });
    return order.map(function (k) { return groups[k]; }).filter(function (g) { return g.count > 1; });
  }
  function tradeIn(e, n) {
    var list = read();
    for (var i = 0; i < list.length; i++) {
      if (list[i].e === e && list[i].n === n) {
        var count = list.filter(function (q) { return q.e === e && q.n === n; }).length;
        if (count < 2) return 0;
        var v = tradeValue(list[i]); list.splice(i, 1); set(KEY, list);
        addTickets(v, 'Trade-in'); return v;
      }
    }
    return 0;
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
    if (!list.length) { el.innerHTML = '<span class="empty">' + esc(opts.empty || 'Nothing yet. The shelf is waiting.') + '</span>'; myLink(el, 0, opts); return; }
    var show = opts.limit ? list.slice(-opts.limit) : list;
    el.innerHTML = show.map(function (p) {
      return '<span class="it ' + esc(p.tier) + '" title="' + esc(p.n + (p.g ? ' · won at ' + p.g : '')) + '">' + esc(p.e) + '</span>';
    }).join('');
    myLink(el, list.length, opts);
  }
  // a "see all my prizes" link under every shelf, so the whole collection is one tap away
  function myLink(el, n, opts) {
    if (opts.noLink || /my-prizes/.test(location.pathname)) return;
    var a = el.nextElementSibling && el.nextElementSibling.classList && el.nextElementSibling.classList.contains('mm-mylink') ? el.nextElementSibling : null;
    if (!a) {
      a = document.createElement('a'); a.className = 'mm-mylink'; a.href = 'my-prizes.html';
      a.style.cssText = 'display:inline-block;margin-top:10px;font:400 .66rem/1 Silkscreen,monospace;letter-spacing:.1em;padding:9px 13px;border-radius:999px;' +
        'text-decoration:none;color:#040509;background:linear-gradient(90deg,#ffd166,#ff7ac8);box-shadow:0 3px 0 #8a2a5c';
      el.parentNode.insertBefore(a, el.nextSibling);
    }
    a.textContent = '🎁 SEE ALL MY PRIZES (' + n + ') →';
  }

  window.MMPrizes = {CAT: CAT, PER: PER, read: read, pick: pick, add: add, tokens: tokens, addToken: addToken, useToken: useToken,
    tickets: tickets, addTickets: addTickets, spendTickets: spendTickets, owned: owned, collect: collect, render: render,
    WINTER: WINTER, daily: daily, dailyCard: dailyCard, dupes: dupes, tradeIn: tradeIn, tradeValue: tradeValue};

  // the daily visit prize pops up on whichever circus or arcade page someone opens first each day
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(dailyCard, 900); });
  else setTimeout(dailyCard, 900);
})();
