/* ============================================================
   MAGICK MICA · SHOP STRIP
   ------------------------------------------------------------
   Drop two lines into any page, just before </body>:

       <script src="products.js"></script>
       <script src="mm-ads.js" defer></script>

   It injects its own styles and its own section, so no page needs
   markup added. A different random handful of in-stock pieces on
   every load — the same idea as the tray on micamagik, and the same
   CRT-and-watermark treatment as the vitrine on crystals.html.

   Placement, in order of preference:
     1. an element with data-mm-ads (if a page wants to choose)
     2. before .adjacent-nav (the prev/next row on issue pages)
     3. before <footer>
     4. end of <body>

   Reads PRODUCTS from products.js. If that file is missing or
   empty the module does nothing at all — no empty headings, no
   broken layout.
   ============================================================ */
(function () {
	'use strict';

	if (typeof PRODUCTS === 'undefined' || !Array.isArray(PRODUCTS) || !PRODUCTS.length) return;

	var COUNT = 4;                    // one row on most layouts
	var STORE = 'https://www.themysticalspiralstore.com';
	var BASE  = STORE + '/product-page/';

	/* Readings are services, not stones — no product photo worth showing, and
	   a $999 twelve-reading package under "hand sourced, one of a kind" reads
	   wrong next to crystal photography. Keep the strip to physical pieces. */
	var SKIP_CATS = { Readings: 1 };

	var live = PRODUCTS.filter(function (p) {
		if (p.soldOut || p.price == null) return false;
		if (SKIP_CATS[p.cat]) return false;
		return !(p.cats || []).some(function (c) { return SKIP_CATS[c]; });
	});
	if (!live.length) return;

	function esc(s) {
		return String(s).replace(/[&<>"]/g, function (c) {
			return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
		});
	}
	function img(f) {
		return 'https://static.wixstatic.com/media/' + f +
		       '/v1/fill/w_600,h_750,al_c,q_80,enc_auto/file.jpg';
	}
	function cut(p) { return p.was ? (p.was - p.price) / p.was : 0; }

	/* Fisher-Yates. sort(() => Math.random()-0.5) is biased and keeps
	   surfacing the same few pieces, which defeats the point. */
	function pick(list, n) {
		var a = list.slice(), i, j, t;
		for (i = a.length - 1; i > 0; i--) {
			j = Math.floor(Math.random() * (i + 1));
			t = a[i]; a[i] = a[j]; a[j] = t;
		}
		return a.slice(0, n);
	}

	/* ---- styles ------------------------------------------------------
	   Scoped under .mm-ads and using its own custom properties, because
	   these pages each have their own palette and we can't assume theirs
	   exists. Falls back to a neutral dark if a page defines nothing.  */
	var css = [
		'.mm-ads{position:relative;z-index:5;',   /* these pages paint a full-page
		  overlay over normal-flow content; without a stacking context of its
		  own the whole strip renders but the text never paints */
		''+
		'  max-width:1100px;margin:3rem auto 0;padding:1.8rem 1.2rem 0;',
		'  border-top:1px solid rgba(160,140,220,.28);font-family:inherit}',
		'.mm-ads-head{display:flex;align-items:baseline;gap:.8rem;flex-wrap:wrap;margin-bottom:1.1rem}',
		'.mm-ads-head h3{margin:0;font-size:.95rem;letter-spacing:.14em;text-transform:uppercase;',
		'  color:#6ef7ff}',
		'.mm-ads-head .sub{font-size:.66rem;letter-spacing:.18em;text-transform:uppercase;',
		'  color:rgba(220,214,240,.5)}',
		'.mm-ads-head .all{margin-left:auto;font-size:.66rem;letter-spacing:.14em;',
		'  text-transform:uppercase;color:#ff9be4;text-decoration:none;',
		'  border-bottom:1px solid currentColor}',
		'.mm-ads-grid{display:grid;gap:.85rem;grid-template-columns:repeat(4,1fr)}',
		'@media(max-width:900px){.mm-ads-grid{grid-template-columns:repeat(2,1fr)}}',
		'@media(max-width:420px){.mm-ads-grid{grid-template-columns:1fr}}',
		'.mm-ad{display:block;text-decoration:none;color:inherit;border-radius:10px;overflow:hidden;',
		'  background:rgba(255,255,255,.045);border:1px solid rgba(160,140,220,.24);transition:.2s}',
		'.mm-ad:hover{border-color:#6ef7ff;transform:translateY(-3px);',
		'  box-shadow:0 14px 30px rgba(0,0,0,.45)}',
		/* the screen treatment from the crystals vitrine */
		'.mm-ad-pic{display:block;position:relative;aspect-ratio:4/5;overflow:hidden;background:#0a0813}',
		'.mm-ad-pic img{width:100%;height:100%;object-fit:cover;display:block;opacity:0;',
		'  transition:opacity .45s}',
		'.mm-ad-pic img.on{opacity:1}',
		'.mm-ad-pic .scan,.mm-ad-pic .vig,.mm-ad-pic .wm,.mm-ad-cut{display:block;font-style:normal;font-weight:400}',
		'.mm-ad-pic .scan{position:absolute;inset:0;pointer-events:none;z-index:2;',
		'  background:repeating-linear-gradient(0deg,rgba(0,0,0,.26) 0 1px,transparent 1px 3px);',
		'  opacity:.55}',
		'.mm-ad-pic .vig{position:absolute;inset:0;pointer-events:none;z-index:3;',
		'  box-shadow:inset 0 0 46px rgba(0,0,0,.72)}',
		'.mm-ad-pic .wm{position:absolute;right:7px;bottom:6px;z-index:4;pointer-events:none;',
		'  font-size:.56rem;letter-spacing:.15em;text-transform:uppercase;color:rgba(255,255,255,.62);',
		'  text-shadow:0 0 6px rgba(110,239,255,.6),0 1px 2px rgba(0,0,0,.85)}',
		'.mm-ad:hover .wm{color:rgba(255,255,255,.92)}',
		'.mm-ad-cut{position:absolute;left:7px;top:7px;z-index:4;font-size:.55rem;letter-spacing:.1em;',
		'  padding:3px 7px;border-radius:99px;color:#0a0813;background:#6ef7ff;font-weight:700}',
		'.mm-ad-txt{display:block;padding:.65rem .7rem .75rem}',
		'.mm-ad-txt .n{display:block;font-size:.78rem;line-height:1.25;color:#ece9f7}',
		'.mm-ad-txt .p{display:block;margin-top:.4rem;font-size:.86rem;font-weight:700;color:#ece9f7}',
		'.mm-ad-txt .p s{font-weight:400;font-size:.7rem;opacity:.55;margin-left:5px}',
		'.mm-ads-note{margin:.9rem 0 0;font-size:.6rem;letter-spacing:.12em;text-transform:uppercase;',
		'  color:rgba(220,214,240,.42)}',
		'.mm-ads-note a{color:inherit}',
		'.mm-ads-compact{margin:2.2rem auto;padding-top:1.2rem}',
		'.mm-ads-compact .mm-ads-head h3{font-size:.82rem}',
		'@media(prefers-reduced-motion:reduce){.mm-ad,.mm-ad-pic img{transition:none}',
		'  .mm-ad-pic img{opacity:1}}',
	].join('');

	var style = document.createElement('style');
	style.textContent = css;
	document.head.appendChild(style);

	/* ---- markup ----
	   These pages run 16,000px tall with six chapters, so one strip at the
	   very bottom is easy to never reach. Draw from a single shuffled pool
	   so the mid-content strips and the closing one never repeat a piece. */
	var pool = pick(live, live.length);
	var poolAt = 0;
	function take(n) {
		if (poolAt + n > pool.length) poolAt = 0;      // wrap on small catalogues
		return pool.slice(poolAt, poolAt += n);
	}

	function cardsFor(list) { return list.map(function (p) {
		var off = p.was ? '<div class="mm-ad-cut">' + Math.round(cut(p) * 100) + '% OFF</div>' : '';
		return '<a class="mm-ad" href="' + BASE + p.slug + '" target="_blank" rel="noopener">' +
			'<div class="mm-ad-pic">' + off +
				'<img loading="lazy" alt="' + esc(p.name) + '" src="' + img(p.img) + '"' +
				' onload="this.classList.add(\'on\')" onerror="this.style.display=\'none\'">' +
				'<i class="scan"></i><i class="vig"></i>' +
				'<b class="wm">Magick Mica TV</b>' +
			'</div>' +
			'<div class="mm-ad-txt"><div class="n">' + esc(p.name) + '</div>' +
			'<div class="p">$' + p.price.toFixed(2) +
			(p.was ? '<s>$' + p.was.toFixed(2) + '</s>' : '') + '</div></div></a>';
	}).join(''); }

	var stamp = (typeof PRODUCTS_COLLECTED !== 'undefined')
		? 'Prices as of ' + esc(PRODUCTS_COLLECTED) + ' &mdash; <a href="' + STORE +
		  '" target="_blank" rel="noopener">check the store</a> for current.'
		: '<a href="' + STORE + '" target="_blank" rel="noopener">Visit the store</a>';

	function strip(n, opts) {
		opts = opts || {};
		var box = document.createElement('section');
		box.className = 'mm-ads' + (opts.compact ? ' mm-ads-compact' : '');
		box.innerHTML =
			'<div class="mm-ads-head">' +
				'<h3>' + (opts.title || 'From the Signal Shop') + '</h3>' +
				'<span class="sub">&#10022; ' + (opts.sub || 'A different handful every visit') + ' &#10022;</span>' +
				'<a class="all" href="crystals.html">See all &rarr;</a>' +
			'</div>' +
			'<div class="mm-ads-grid">' + cardsFor(take(n)) + '</div>' +
			(opts.compact ? '' : '<p class="mm-ads-note">' + stamp + '</p>');
		return box;
	}

	/* ---- placement ---- */
	function placeClosing(box) {
		var slot = document.querySelector('[data-mm-ads]');
		if (slot) { slot.appendChild(box); return; }
		var adj = document.querySelector('.adjacent-nav');
		if (adj && adj.parentNode) { adj.parentNode.insertBefore(box, adj); return; }
		var foot = document.querySelector('footer');
		if (foot && foot.parentNode) { foot.parentNode.insertBefore(box, foot); return; }
		document.body.appendChild(box);
	}

	function place() {
		/* mid-content: after every second chapter, so a long issue carries
		   two or three strips instead of one nobody scrolls to */
		var chapters = document.querySelectorAll('.chapter');
		if (chapters.length >= 3) {
			for (var i = 1; i < chapters.length - 1; i += 2) {
				var c = chapters[i];
				if (!c.parentNode) continue;
				c.parentNode.insertBefore(
					strip(4, { compact: true, title: 'Meanwhile, in the shop',
					           sub: 'Hand sourced \u00b7 One of a kind' }),
					c.nextSibling);
			}
		}
		placeClosing(strip(COUNT));
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', place);
	} else {
		place();
	}
})();
