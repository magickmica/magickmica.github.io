/* ============================================================
   MAGICK MICA TV STORE · COLLECT PRODUCTS
   ------------------------------------------------------------
   HOW TO RUN
   1. Go to https://magickmicatv.store/  and let it finish loading.
   2. F12 -> Console. If Chrome asks, type:  allow pasting   then Enter.
   3. Paste this whole file, press Enter.
   4. Scroll down if it asks you to, then wait. store-products.js
      downloads at the end, and a short report prints in the console.

   Runs ON the store, so there is no CORS problem, and it only reads
   the same public pages a shopper already sees.

   The store draws its tiles in the browser rather than serving them
   in the HTML, so this tries three ways of finding the data and uses
   whichever works. It prints which one it used; if the result looks
   wrong, send me the report and I will fix the picker.
   ============================================================ */

(async function () {
  const OUT = [];
  const log = (...a) => console.log("%c[store]", "color:#F5C044", ...a);
  const abs = (u) => { try { return new URL(u, location.origin).href; } catch (e) { return null; } };

  /* Images are often lazy-loaded, so nudge the page to render them all. */
  async function scrollThrough() {
    let last = -1;
    for (let i = 0; i < 40 && document.body.scrollHeight !== last; i++) {
      last = document.body.scrollHeight;
      window.scrollTo(0, document.body.scrollHeight);
      await new Promise((r) => setTimeout(r, 450));
    }
    window.scrollTo(0, 0);
    await new Promise((r) => setTimeout(r, 400));
  }

  /* Pull the biggest candidate out of a srcset, else the plain src. */
  function bestImage(img) {
    if (!img) return null;
    const ss = img.getAttribute("srcset") || img.getAttribute("data-srcset");
    if (ss) {
      const best = ss.split(",")
        .map((s) => s.trim().split(/\s+/))
        .map(([u, w]) => ({ u, w: parseInt(w) || 0 }))
        .sort((a, b) => b.w - a.w)[0];
      if (best && best.u) return abs(best.u);
    }
    return abs(img.getAttribute("src") || img.getAttribute("data-src") || "");
  }

  /* ---- 1. framework state, where most storefronts keep their data ---- */
  function fromState() {
    const roots = [];
    try { if (window.__NEXT_DATA__) roots.push(window.__NEXT_DATA__); } catch (e) {}
    try { if (window.__NUXT__) roots.push(window.__NUXT__); } catch (e) {}
    for (const s of document.querySelectorAll('script[type="application/json"]')) {
      try { roots.push(JSON.parse(s.textContent)); } catch (e) {}
    }
    const found = [];
    const seen = new Set();
    (function walk(node, depth) {
      if (!node || depth > 12 || typeof node !== "object") return;
      if (Array.isArray(node)) { node.forEach((n) => walk(n, depth + 1)); return; }
      const id = node.id ?? node.productId ?? node.product_id;
      const title = node.title ?? node.name;
      if (id != null && typeof title === "string" && title.trim() && !seen.has(String(id))) {
        const price = node.price ?? node.minPrice ?? node.min_price ?? node.variantPrice;
        const img = node.image ?? node.thumbnail ?? node.imageUrl ?? node.image_url ??
                    (Array.isArray(node.images) ? (node.images[0]?.src ?? node.images[0]) : null);
        if (img || price != null) {
          seen.add(String(id));
          found.push({ id: String(id), name: title.trim(), price: price ?? null,
                       img: typeof img === "string" ? abs(img) : null });
        }
      }
      Object.values(node).forEach((v) => walk(v, depth + 1));
    })({ roots }, 0);
    return found;
  }

  /* ---- 2. JSON-LD, which many stores publish for search engines ---- */
  function fromJsonLd() {
    const out = [];
    for (const s of document.querySelectorAll('script[type="application/ld+json"]')) {
      let d; try { d = JSON.parse(s.textContent); } catch (e) { continue; }
      for (const node of [].concat(d, d["@graph"] || [], d.itemListElement || [])) {
        const n = node?.item || node;
        if (!n || n["@type"] !== "Product") continue;
        const url = n.url || "";
        const m = String(url).match(/\/product\/(\d+)/);
        out.push({
          id: m ? m[1] : (n.sku || n.productID || n.name),
          name: n.name,
          price: n.offers?.price ?? n.offers?.lowPrice ?? null,
          img: typeof n.image === "string" ? abs(n.image)
               : Array.isArray(n.image) ? abs(n.image[0]) : null,
        });
      }
    }
    return out.filter((p) => p.name);
  }

  /* ---- 3. the rendered tiles, as a last resort ---- */
  function fromDom() {
    const byId = new Map();
    for (const a of document.querySelectorAll('a[href*="/product/"]')) {
      const m = a.getAttribute("href").match(/\/product\/(\d+)/);
      if (!m) continue;
      const id = m[1];
      // Walk out to the tile so the name, price and image are all in scope.
      let tile = a;
      for (let i = 0; i < 4 && tile.parentElement; i++) {
        tile = tile.parentElement;
        if (tile.querySelector("img") && /\$\s?\d/.test(tile.textContent)) break;
      }
      const text = (tile.innerText || "").trim();
      const price = (text.match(/\$\s?[\d,]+(?:\.\d{2})?/) || [null])[0];
      // The longest line that is not the price is almost always the name.
      const name = text.split("\n").map((s) => s.trim())
        .filter((s) => s && !/^\$/.test(s) && !/^(quick view|add to cart|shop)$/i.test(s))
        .sort((x, y) => y.length - x.length)[0] || null;
      const img = bestImage(tile.querySelector("img"));
      const prev = byId.get(id);
      if (!prev || (!prev.img && img) || (!prev.name && name)) {
        byId.set(id, { id, name: name || prev?.name || null,
                       price: price || prev?.price || null, img: img || prev?.img || null });
      }
    }
    return [...byId.values()];
  }

  log("scrolling to load every tile…");
  await scrollThrough();

  const tries = [["framework state", fromState], ["JSON-LD", fromJsonLd], ["rendered tiles", fromDom]];
  let used = null, rows = [];
  for (const [label, fn] of tries) {
    let r = [];
    try { r = fn() || []; } catch (e) { log(label, "failed:", e.message); }
    const withImg = r.filter((p) => p.img).length;
    log(`${label}: ${r.length} products, ${withImg} with an image`);
    // Prefer whichever gives the most products that actually have pictures.
    if (withImg > rows.filter((p) => p.img).length) { rows = r; used = label; }
  }
  if (!rows.length) { rows = fromDom(); used = "rendered tiles"; }

  const clean = rows
    .filter((p) => p.name)
    .map((p) => ({
      id: String(p.id),
      name: String(p.name).replace(/\s+/g, " ").trim(),
      price: p.price == null ? null :
             String(p.price).startsWith("$") ? String(p.price) : "$" + p.price,
      img: p.img || null,
      url: /^\d+$/.test(String(p.id)) ? location.origin + "/product/" + p.id : null,
    }))
    .filter((p, i, a) => a.findIndex((x) => x.id === p.id) === i);

  const out = {
    app: "COLLECT STORE", version: 1, store: location.origin,
    collected_at: new Date().toISOString(), method: used,
    count: clean.length, products: clean,
  };

  const body = "/* MAGICK MICA TV STORE — product snapshot.\n" +
    "   Generated by tools/collect_store.js. Collected " +
    out.collected_at.slice(0, 10) + ". Do not edit by hand. */\n" +
    'const STORE_COLLECTED = "' + out.collected_at.slice(0, 10) + '";\n' +
    "const STORE_PRODUCTS = " + JSON.stringify(clean) + ";\n";

  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([body], { type: "text/javascript" }));
  a.download = "store-products.js";
  document.body.appendChild(a); a.click();

  window.__storeProducts = out;
  log("── REPORT ─────────────────────────────");
  log("method used :", used);
  log("products    :", clean.length);
  log("with image  :", clean.filter((p) => p.img).length);
  log("with price  :", clean.filter((p) => p.price).length);
  log("first three :", clean.slice(0, 3));
  log("store-products.js is downloading. Send it back along with this report.");
})();
