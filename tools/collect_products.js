/* ============================================================
   MYSTICAL SPIRAL · COLLECT PRODUCTS
   ------------------------------------------------------------
   HOW TO RUN
   1. Go to https://www.themysticalspiralstore.com  (any page)
   2. F12 -> Console. Type:  allow pasting   then Enter
   3. Paste this whole file, press Enter
   4. Wait. It walks every category and every page of results.
      products.json downloads when it finishes.

   Runs ON the store, so there is no CORS problem. It only reads
   the same public pages a shopper sees.
   ============================================================ */
(async () => {
  'use strict';

  const CATEGORIES = [
    ['',                          'Shop'],
    ['/crystals',                 'Crystals'],
    ['/crystal-balls',            'Balls & Bracelets'],
    ['/crystal-clusters',         'Clusters'],
    ['/crystal-free-forms',       'Free Forms'],
    ['/crystal-palmstones',       'Palmstones'],
    ['/crystal-skulls',           'Skulls'],
    ['/crystal-specimens',        'Specimens'],
    ['/crystal-towers',           'Towers'],
    ['/crystal-wands',            'Wands'],
    ['/tensors',                  'Tensors'],
    ['/pendants-amulets',         'Pendants & Amulets'],
    ['/copper-tensor-bracelets',  'Bracelets'],
    ['/harmonizer',               'Harmonizers'],
  ];

  const MAX_PAGES = 12;
  const PAUSE = 500;
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const money = s => { const m = /([\d,]+\.\d{2})/.exec(s || ''); return m ? parseFloat(m[1].replace(/,/g, '')) : null; };

  function parse(doc, category) {
    const out = [];
    const links = doc.querySelectorAll('a[href*="/product-page/"]');
    const seen = new Set();

    links.forEach(a => {
      const href = a.href.split('?')[0];
      const slug = href.split('/product-page/')[1];
      if (!slug || seen.has(slug)) return;

      // climb to the tile that holds this product's image + price text
      let tile = a;
      for (let i = 0; i < 6 && tile.parentElement; i++) {
        tile = tile.parentElement;
        if (tile.querySelector('img') && /Price|stock/i.test(tile.textContent)) break;
      }
      const text = (tile.textContent || '').replace(/\s+/g, ' ').trim();
      if (!/Price|Out of stock/i.test(text)) return;
      seen.add(slug);

      const img = tile.querySelector('img');
      let src = img ? (img.currentSrc || img.src || '') : '';
      // ask Wix for a clean 600px render instead of the thumbnail
      src = src.replace(/\/v1\/(fill|fit)\/[^/]+\//, '/v1/fill/w_600,h_600,al_c,q_85/');

      const sale = /Sale Price\s*\$([\d,]+\.\d{2})/i.exec(text);
      const reg = /Regular Price\s*\$([\d,]+\.\d{2})/i.exec(text);
      const plain = /(?:^|[^e])Price\s*\$([\d,]+\.\d{2})/i.exec(text);

      let name = (a.textContent || '').replace(/\s+/g, ' ').trim()
        .replace(/(Regular |Sale )?Price.*$/i, '')
        .replace(/Out of stock.*$/i, '')
        .replace(/Quick View.*$/i, '').trim();
      if (!name || name.length < 3) {
        name = slug.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
      }

      out.push({
        slug: slug,
        name: name,
        url: href,
        img: src,
        price: money(sale && sale[0]) || money(plain && plain[0]) || money(reg && reg[0]),
        was: sale ? money(reg && reg[0]) : null,
        soldOut: /Out of stock/i.test(text),
        cat: category
      });
    });
    return out;
  }

  const all = new Map();

  for (const [path, label] of CATEGORIES) {
    for (let page = 1; page <= MAX_PAGES; page++) {
      const url = location.origin + path + (page > 1 ? '?page=' + page : '');
      let doc;
      try {
        const res = await fetch(url, { credentials: 'include' });
        if (!res.ok) break;
        doc = new DOMParser().parseFromString(await res.text(), 'text/html');
      } catch (e) { console.warn('[shop] failed', url, e); break; }

      const found = parse(doc, label);
      if (!found.length) break;

      let added = 0;
      found.forEach(p => { if (!all.has(p.slug)) { all.set(p.slug, p); added++; } });
      console.log(`[shop] ${label} p${page} · ${found.length} tiles · ${added} new · total ${all.size}`);

      if (added === 0 && page > 1) break;
      await sleep(PAUSE);
    }
  }

  const items = [...all.values()];
  const payload = {
    collected: new Date().toISOString().slice(0, 10),
    count: items.length,
    items: items
  };

  console.log(`%c[shop] DONE — ${items.length} products`, 'color:#7bf1e4;font-weight:bold');
  console.table(items.slice(0, 5));

  const blob = new Blob([JSON.stringify(payload)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'products.json';
  document.body.appendChild(a);
  a.click();
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 4000);

  window.__products = items;
})();
