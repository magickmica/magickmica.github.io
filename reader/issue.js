/* Transmission Reader 98 · issue pages: picture fallback, deep links to a note, current chapter. */
(function () {
  'use strict';
  var FALLBACK = '<svg viewBox="0 0 8 8" width="28" height="28" aria-hidden="true"><rect x="0" y="1" width="8" height="6" fill="#8a819f"/><rect x="1" y="2" width="6" height="4" fill="#fbfaff"/><rect x="2" y="4" width="2" height="2" fill="#3f9c5a"/><rect x="4" y="3" width="2" height="3" fill="#3f8fc0"/><rect x="5" y="2" width="1" height="1" fill="#ffd76e"/></svg>';

  // pictures that can't be received become an attachment notice
  document.querySelectorAll('img[data-fallback]').forEach(function (im) {
    function swap() {
      var d = document.createElement('div');
      d.className = 'att';
      d.innerHTML = FALLBACK + '<span>' + im.getAttribute('data-fallback') + '</span>';
      im.replaceWith(d);
    }
    if (im.complete && im.naturalWidth === 0) swap();
    else im.addEventListener('error', swap);
  });

  // #n123 opens that transmission; #d2026-06-10 lands on that day
  function follow() {
    var id = location.hash.slice(1);
    if (!id) return;
    var el = document.getElementById(id);
    if (!el) return;
    document.querySelectorAll('.msg.hit').forEach(function (m) { m.classList.remove('hit'); });
    if (el.classList.contains('msg')) { el.open = true; el.classList.add('hit'); }
    el.scrollIntoView({ block: 'start' });
    var sum = el.querySelector('summary');
    (sum || el).focus({ preventScroll: true });
  }
  window.addEventListener('hashchange', follow);
  follow();

  // close the phone contents menu after a choice
  var pick = document.querySelector('.toc-pick');
  if (pick) pick.addEventListener('click', function (e) { if (e.target.closest('a')) pick.open = false; });

  // light up the chapter being read in the contents pane
  var doc = document.getElementById('doc'), links = {};
  document.querySelectorAll('.toc a[href^="#"]').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
  if (!('IntersectionObserver' in window) || !doc) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var a = links[en.target.id];
      if (!a) return;
      document.querySelectorAll('.toc a.on').forEach(function (x) { x.classList.remove('on'); x.removeAttribute('aria-current'); });
      a.classList.add('on');
      a.setAttribute('aria-current', 'location');
    });
  }, { root: getComputedStyle(doc).overflowY === 'auto' ? doc : null, rootMargin: '0px 0px -70% 0px' });
  document.querySelectorAll('.group[id]').forEach(function (g) { io.observe(g); });
})();
