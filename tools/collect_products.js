/* ============================================================
   MYSTICAL SPIRAL · COLLECT PRODUCTS  (v2)
   ------------------------------------------------------------
   HOW TO RUN
   1. Go to https://www.themysticalspiralstore.com  (any page)
   2. F12 -> Console. Type:  allow pasting   then Enter
   3. Paste this whole file, press Enter
   4. Wait. products.js AND products.json both download at the end.

   Runs ON the store, so there is no CORS problem. It only reads
   the same public pages a shopper sees.

   CHANGES FROM v1 (all three were verified against the live site)
   - Each tile has TWO /product-page/ links: a "Quick View" one and
     the real name one. v1 always took the first, so every name fell
     back to the slug. v2 gathers all links per slug and keeps the
     best name.
   - The root shop page lists everything, so walking it first made
     `cat` come back "Shop" for nearly every product. It now runs
     last and only catches leftovers.
   - Images are lazy-loaded, so img.src is often a placeholder in a
     fetched document. v2 checks srcset/data-src and falls back to
     scanning the tile markup for a wixstatic media id.
   - `img` is now the bare Wix media id, matching the IMG() helper
     the seven vault pages already use.
   ============================================================ */
(async () => {
  'use strict';

  // Order = specificity, most specific first. /crystals is a PARENT of the
  // eight crystal-* pages and re-lists all of their products, and the root
  // shop page lists literally everything, so both must rank last or they
  // swallow every label. A product is recorded under every category it
  // appears in and then assigned the most specific one, so this ordering
  // decides the label but no longer decides coverage.
  const CATEGORIES = [
    ['/crystal-skulls',           'Skulls'],
    ['/crystal-towers',           'Towers'],
    ['/crystal-wands',            'Wands'],
    ['/crystal-palmstones',       'Palmstones'],
    ['/crystal-free-forms',       'Free Forms'],
    ['/crystal-clusters',         'Clusters'],
    ['/crystal-specimens',        'Specimens'],
    ['/crystal-balls',            'Balls & Bracelets'],
    ['/copper-tensor-bracelets',  'Bracelets'],
    ['/harmonizer',               'Harmonizers'],
    ['/tensors',                  'Tensors'],
    ['/pendants-amulets',         'Pendants & Amulets'],
    ['/crystals',                 'Crystals'],   // parent listing
    ['',                          'Shop'],       // catch-all, must stay last
  ];

  const MAX_PAGES = 30;          // 20 products/page, so ~600 per category
  const PAUSE = 500;
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const money = s => {
    const m = /([\d,]+\.\d{2})/.exec(s || '');
    return m ? parseFloat(m[1].replace(/,/g, '')) : null;
  };

  // Strip price / badge / chrome text off a candidate product name.
  const cleanName = t => (t || '')
    .replace(/\s+/g, ' ')
    .replace(/(Regular |Sale )?Price\s*\$[\d,]+\.\d{2}/gi, '')
    .replace(/Out of stock/gi, '')
    .replace(/Quick View/gi, '')
    .replace(/Sold out/gi, '')
    .trim();

  // Lazy-loaded galleries hide the real URL in srcset/data-src, and a
  // fetched document never runs the JS that would populate img.src.
  function pickMediaId(tile) {
    const imgs = tile.querySelectorAll('img');
    for (const img of imgs) {
      const srcset = img.getAttribute('srcset') || '';
      const cands = [
        img.getAttribute('src'),
        img.getAttribute('data-src'),
        img.getAttribute('data-image-src'),
        srcset.split(',').pop().trim().split(/\s+/)[0]
      ];
      for (const c of cands) {
        const m = c && /static\.wixstatic\.com\/media\/([^/?"']+)/.exec(c);
        if (m && !/^nsplsh_/.test(m[1])) return m[1];   // skip stock banners
      }
    }
    // last resort: any media id anywhere in the tile markup
    const m = /static\.wixstatic\.com\/media\/([A-Za-z0-9_~%.-]+\.(?:jpg|jpeg|png|webp|avif))/i
      .exec(tile.innerHTML || '');
    return (m && !/^nsplsh_/.test(m[1])) ? m[1] : '';
  }

  function parse(doc, category) {
    // Group every /product-page/ link by slug first, so the "Quick View"
    // link and the real name link are considered together.
    const groups = new Map();
    doc.querySelectorAll('a[href*="/product-page/"]').forEach(a => {
      const href = (a.href || a.getAttribute('href') || '').split('?')[0];
      const slug = href.split('/product-page/')[1];
      if (!slug) return;
      if (!groups.has(slug)) groups.set(slug, { href, anchors: [] });
      groups.get(slug).anchors.push(a);
    });

    const out = [];
    groups.forEach((g, slug) => {
      // climb from the first anchor to the tile holding image + price
      let tile = g.anchors[0];
      for (let i = 0; i < 7 && tile.parentElement; i++) {
        tile = tile.parentElement;
        if (tile.querySelector('img') && /Price|Out of stock/i.test(tile.textContent)) break;
      }
      const text = (tile.textContent || '').replace(/\s+/g, ' ').trim();
      if (!/Price|Out of stock/i.test(text)) return;

      // best name = longest anchor text once price/badge chrome is stripped
      let name = '';
      g.anchors.forEach(a => {
        const c = cleanName(a.textContent);
        if (c.length > name.length) name = c;
      });
      let named = true;
      if (name.length < 3) {                      // nothing usable in the links
        name = slug.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
        named = false;
      }

      // Wix runs the name straight into the price when the name has no
      // trailing space ("...XL 4ozPrice$37.99"), so `plain` must not
      // require a non-letter before "Price". It is only consulted when
      // neither "Sale Price" nor "Regular Price" matched, so it cannot
      // pick up the pre-discount figure by mistake.
      const sale  = /Sale Price\s*\$([\d,]+\.\d{2})/i.exec(text);
      const reg   = /Regular Price\s*\$([\d,]+\.\d{2})/i.exec(text);
      const plain = /Price\s*\$([\d,]+\.\d{2})/i.exec(text);

      out.push({
        slug: slug,
        name: name,
        img: pickMediaId(tile),                   // bare Wix media id
        price: sale ? money(sale[0]) : (reg ? money(reg[0]) : money(plain && plain[0])),
        was: sale ? money(reg && reg[0]) : null,
        soldOut: /Out of stock|Sold out/i.test(text),
        cat: category,
        _named: named
      });
    });
    return out;
  }

  const all = new Map();

  for (const [path, label] of CATEGORIES) {
    let prevSig = '';
    for (let page = 1; page <= MAX_PAGES; page++) {
      const url = location.origin + path + (page > 1 ? '?page=' + page : '');
      let doc;
      try {
        const res = await fetch(url, { credentials: 'include' });
        if (!res.ok) break;
        doc = new DOMParser().parseFromString(await res.text(), 'text/html');
      } catch (e) { console.warn('[shop] failed', url, e); break; }

      const found = parse(doc, label);
      if (!found.length) break;                   // real end of pagination

      // A page of all-duplicates is normal deep in the catch-all shop
      // listing, so we must NOT stop on it. Stop only when the page is
      // identical to the previous one, i.e. Wix clamped past the last page.
      const sig = found.map(p => p.slug).join('|');
      if (sig === prevSig) break;
      prevSig = sig;

      let added = 0;
      found.forEach(p => {
        const existing = all.get(p.slug);
        if (existing) {
          existing._cats.add(p.cat);      // seen again in another category
        } else {
          p._cats = new Set([p.cat]);
          all.set(p.slug, p);
          added++;
        }
      });
      console.log(`[shop] ${label} p${page} · ${found.length} tiles · ${added} new · total ${all.size}`);

      await sleep(PAUSE);
    }
  }

  const items = [...all.values()];

  // Resolve each product to its most specific category, and keep the full
  // membership list so the page can filter on it (a skull can be a skull
  // AND a specimen).
  const RANK = CATEGORIES.map(c => c[1]);
  items.forEach(p => {
    p.cats = RANK.filter(r => p._cats.has(r));
    p.cat = p.cats[0] || 'Shop';
  });

  // ---- diagnostics: check these numbers before trusting the file ----
  const noName = items.filter(p => !p._named).length;
  const noImg  = items.filter(p => !p.img).length;
  const noPx   = items.filter(p => p.price == null && !p.soldOut).length;
  const onSale = items.filter(p => p.was).length;
  const gone   = items.filter(p => p.soldOut).length;

  console.log(`%c[shop] DONE — ${items.length} products`, 'color:#7bf1e4;font-weight:bold');
  console.log(`  ${onSale} on sale · ${gone} sold out`);
  console.log(`  fell back to slug for name: ${noName}   (want 0)`);
  console.log(`  no image found:            ${noImg}    (want 0)`);
  console.log(`  no price, not sold out:    ${noPx}     (want 0)`);
  console.table(items.slice(0, 8).map(p => ({ name: p.name, price: p.price, was: p.was, cat: p.cat, img: p.img })));

  const byCat = {};
  items.forEach(p => { byCat[p.cat] = (byCat[p.cat] || 0) + 1; });
  console.log('[shop] by category:', byCat);

  items.forEach(p => { delete p._named; delete p._cats; });
  const collected = new Date().toISOString().slice(0, 10);

  // ---- download both shapes -----------------------------------------
  const save = (text, filename, type) => {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([text], { type }));
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 4000);
  };

  save(JSON.stringify({ collected, count: items.length, items }),
       'products.json', 'application/json');

  // products.js is what the page actually loads — plain <script src>,
  // same pattern as pools.js, no fetch() and no local-preview CORS.
  save(
    `/* THE MYSTICAL SPIRAL — product snapshot. Generated by tools/collect_products.js.\n` +
    `   Collected ${collected}. Do not edit by hand. */\n` +
    `const PRODUCTS_COLLECTED = ${JSON.stringify(collected)};\n` +
    `const PRODUCTS = ${JSON.stringify(items)};\n`,
    'products.js', 'application/javascript');

  window.__products = items;
})();
