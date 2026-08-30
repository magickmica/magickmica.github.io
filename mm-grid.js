/* MAGICKMICA - renders the weekly Y3K grid from pools.js.
   Include after pools.js:  <script src="mm-grid.js" defer></script> */
(function () {
  function build() {
    var grid = document.querySelector('.mag-grid');
    if (!grid || typeof WEEK_CARDS === 'undefined') return;
    grid.innerHTML = WEEK_CARDS.map(function (c) {
      var img = c.cover
        ? '<img decoding="async" src="' + c.cover + '" loading="lazy" alt="' +
          c.label + ' weekly issue" ' +
          'onerror="this.parentElement.classList.add(\'no-img\')" />'
        : '';
      return '<a class="mag-card" href="' + c.href + '">' +
             '<div class="mag-card-cover">' + img +
             '<div class="mag-card-overlay"></div>' +
             '<div class="mag-card-count">' + c.count + ' NOTES</div></div>' +
             '<div class="mag-card-label">' + c.label + '</div></a>';
    }).join('');
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else { build(); }
})();
