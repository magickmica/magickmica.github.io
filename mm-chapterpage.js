/* mm-chapterpage.js · keeps the chapter bar under the site bar and fades the opening in */
(function () {
  var body = document.body;
  function navH() { var b = document.querySelector('.mm-bar'); if (b) body.style.setProperty('--nav-h', b.offsetHeight + 'px'); }
  navH(); window.addEventListener('load', navH); window.addEventListener('resize', navH); setTimeout(navH, 600);
  var here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.cp-nav a').forEach(function (a) {
    if ((a.getAttribute('href') || '').split('#')[0] === here) a.setAttribute('aria-current', 'page');
  });
  var els = document.querySelectorAll('.cp-rv');
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    els.forEach(function (el) { el.classList.add('on'); }); return;
  }
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('on'); io.unobserve(e.target); } }); }, { threshold: .05 });
  els.forEach(function (el) { io.observe(el); });
})();
