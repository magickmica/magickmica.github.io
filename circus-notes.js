/* MAGICKMICA · circus-notes.js
   Lines from Magick Mica's own Substack notes, for the Fortune Teller and
   the Photo Booth. Reads search-index.json (rebuilt by the site bot), so new
   notes show up here by themselves.

   MMNotes.load()  -> Promise of [{id, d, text, url}], tidy one-liners only
   MMNotes.pretty(d) -> "June 1, 2026"
*/
(function () {
  'use strict';
  var BAD = /https?:|www\.|@|posted|year ago|subscri|substack|restack|comment|giveaway|sale|discount|\$|\bdm\b|follow|thank|link in|click|politic|trump|inspiration:|available|shop|order|episode|issue|chat|live now|\bpost\b|new note|prompt|claude|chatgpt|#|\*|horoscope|see what|here for you|\bme:|\bx\b|today is|tag|share/i;
  var MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  var cache = null;

  function tidy(t) {
    t = String(t || '').replace(/\s+/g, ' ').trim();
    // drop decorative symbol runs (kaomoji borders, sparkle strings) at either end
    var keep = /[A-Za-z0-9.,!?'’"“”…\-—–:;() ]/;
    var a = 0, b = t.length;
    while (a < b && !/[A-Za-z0-9“"‘']/.test(t[a])) a++;
    while (b > a && !/[A-Za-z0-9.!?…”"’')]/.test(t[b - 1])) b--;
    t = t.slice(a, b).trim();
    // a quote followed by an author name is someone else's line: skip it
    if (/[”"]\s*[-—–~]?\s*[A-Z][a-z]+/.test(t) && /^[“"]/.test(t)) return '';
    if (/\s[-—–]\s?[A-Z][a-z]+( [A-Z][a-z]+)?\.?$/.test(t)) return '';
    // unwrap a line that is one whole quote
    var m = t.match(/^[“"](.+?)[”"]$/);
    if (m && !/[“”"]/.test(m[1])) t = m[1].trim();
    var plain = 0;
    for (var i = 0; i < t.length; i++) if (keep.test(t[i])) plain++;
    if (!t.length || plain !== t.length || /[“”"]/.test(t)) return '';
    return t;
  }

  function load() {
    if (cache) return cache;
    cache = fetch('search-index.json', {cache: 'no-cache'}).then(function (r) { return r.json(); }).then(function (d) {
      var seen = {}, out = [];
      (d.notes || []).forEach(function (n) {
        var raw = n[2] || '';
        if (raw.length < 34 || raw.length > 230 || BAD.test(raw) || /\n/.test(raw)) return;
        var t = tidy(raw);
        if (t.length < 30 || t.length > 170 || t.split(' ').length < 6) return;
        var k = t.toLowerCase().replace(/[^a-z]/g, '');
        if (seen[k]) return; seen[k] = 1;
        out.push({id: n[0], d: n[1], text: t, url: 'https://substack.com/@magickmica/note/c-' + n[0]});
      });
      return out;
    }).catch(function () { cache = null; return []; });
    return cache;
  }

  function pretty(d) {
    var p = String(d || '').split('-');
    return p.length === 3 ? MONTHS[+p[1] - 1] + ' ' + (+p[2]) + ', ' + p[0] : '';
  }

  window.MMNotes = {load: load, tidy: tidy, pretty: pretty};
})();
