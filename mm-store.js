/* ============================================================
   MAGICKMICA · SHOP STRIP
   ------------------------------------------------------------
   Drop one line into any page, just before </body>:
       <script src="mm-store.js" defer></script>

   Shows four products from magickmicatv.store above the footer,
   picked fresh on every load so the whole catalogue gets shown
   over time rather than the same four forever.

   Self-contained like mm-nav.js: the product snapshot is baked in,
   every class is prefixed .mms- so it cannot collide with a page's
   own styles, and the colours are literal rather than var() because
   these pages do not all share one palette.

   To refresh the products, run tools/collect_store.js on the store
   and paste the new STORE_PRODUCTS array over the one below.
   ============================================================ */
(function () {
  'use strict';

  var STORE = 'https://magickmicatv.store/';
  var COLLECTED = '2026-10-03';
  var SHOW = 4;

  /* ---- the snapshot ------------------------------------------------- */
  var PRODUCTS = [];
  PRODUCTS = [{"name": "Retro Tech Tote — Vintage TVs in Neon Surf Canvas Bag", "price": "$22.22", "img": "https://images-api.printify.com/mockup/6ac056260b38708d65062a0b/103598/93895/retro-tech-tote-vintage-tvs-in-neon-surf-canvas-bag.jpg?camera_label=front&revision=1790990082032", "url": "https://magickmicatv.store/product/32664629"}, {"name": "Cosmic Rainbow Goddess Sherpa Blanket", "price": "$50.00", "img": "https://images-api.printify.com/mockup/6ac02c87507a3b0fcf07c80f/103554/100561/cosmic-rainbow-goddess-sherpa-blanket.jpg?camera_label=front&revision=1790979712703", "url": "https://magickmicatv.store/product/32659153"}, {"name": "Crystal Pixel Sleep Frosted Glass Candle — 11oz Relaxing Scented Candle", "price": "$28.00", "img": "https://images-api.printify.com/mockup/6ac016f08feeaed14a090788/114653/108754/crystal-pixel-sleep-frosted-glass-candle-11oz-relaxing-scented-candle.jpg?camera_label=front&revision=1790973808734", "url": "https://magickmicatv.store/product/32656140"}, {"name": "Crystal Pixel Dream Sleep Black Mug — Cozy Nighttime Fantasy Coffee Cup (11oz/15oz)", "price": "$12.00", "img": "https://images-api.printify.com/mockup/6abff16a783bad9caf003bad/65217/6406/crystal-pixel-dream-sleep-black-mug-cozy-nighttime-fantasy-coffee-cup-11oz15oz.jpg?camera_label=left&revision=1790972685131", "url": "https://magickmicatv.store/product/32650763"}, {"name": "Holographic Goddess Silhouette Heart Keychain — Iridescent Celestial Gift", "price": "$4.44", "img": "https://images-api.printify.com/mockup/6ac05afc4d91596e1c0b54ab/147910/112417/holographic-goddess-silhouette-heart-keychain-iridescent-celestial-gift.jpg?camera_label=front&revision=1790991682460", "url": "https://magickmicatv.store/product/32665532"}, {"name": "Holographic Dreamer Matte Canvas Print — Crystal Pixel Sleeping Prism Art", "price": "$55.00", "img": "https://images-api.printify.com/mockup/6abfdf82113ff806090ad1cc/114705/108077/holographic-dreamer-matte-canvas-print-crystal-pixel-sleeping-prism-art.jpg?camera_label=side&revision=1790959679535", "url": "https://magickmicatv.store/product/32648341"}, {"name": "Cosmic Goddess Desk Mat — Vibrant UFO and Moonlight Gaming/Work Mousepad", "price": "$18.00", "img": "https://images-api.printify.com/mockup/6abfc5e795bafa807107d2d2/65240/6570/cosmic-goddess-desk-mat-vibrant-ufo-and-moonlight-gamingwork-mousepad.jpg?camera_label=front&revision=1790959746443", "url": "https://magickmicatv.store/product/32644273"}, {"name": "Nikki Cosmic Crystal Palace Matte Horizontal Poster — Magick Mica TV Wall Art", "price": "$14.00", "img": "https://images-api.printify.com/mockup/6abfaef215a02de7a6023cf9/101240/94761/nikki-cosmic-crystal-palace-matte-horizontal-poster-magick-mica-tv-wall-art.jpg?camera_label=front-2&revision=1790947388128", "url": "https://magickmicatv.store/product/32640386"}, {"name": "Nikki and Midnight Magick Mica TV Ceramic Mug — Cute Pastel Aesthetic Gift (11oz/15oz)", "price": "$12.00", "img": "https://images-api.printify.com/mockup/6abeeb7b1ad79079b7068aa9/65216/6310/nikki-and-midnight-magick-mica-tv-ceramic-mug-cute-pastel-aesthetic-gift-11oz15oz.jpg?camera_label=front&revision=1790897355111", "url": "https://magickmicatv.store/product/32620031"}, {"name": "Cosmic Goddess Matte Horizontal Poster — Psychedelic Space Art Print", "price": "$14.00", "img": "https://images-api.printify.com/mockup/6abedb29364d4d880e0f483f/101240/94761/cosmic-goddess-matte-horizontal-poster-psychedelic-space-art-print.jpg?camera_label=front-2&revision=1790893309556", "url": "https://magickmicatv.store/product/32617644"}, {"name": "Cosmic Goddess Accessory Pouch — Starry Rainbow Makeup Bag", "price": "$12.12", "img": "https://images-api.printify.com/mockup/6abed0381a95f0b60d0ed8cd/44529/46805/cosmic-goddess-accessory-pouch-starry-rainbow-makeup-bag.jpg?camera_label=front&revision=1790890498114", "url": "https://magickmicatv.store/product/32616198"}, {"name": "Cyber Mona Lisa Matte Canvas Wall Art — Retro Futuristic Pixelated Renaissance Print", "price": "$25.00", "img": "https://images-api.printify.com/mockup/6abeb20685f90b92ca04f706/91656/60281/cyber-mona-lisa-matte-canvas-wall-art-retro-futuristic-pixelated-renaissance-print.jpg?camera_label=side&revision=1790890020055", "url": "https://magickmicatv.store/product/32616007"}, {"name": "Mona Lisa Bling Street Art Canvas Print — 'Fine' Pop Graffiti Wall Art", "price": "$25.00", "img": "https://images-api.printify.com/mockup/6abe82282d7a2d0a0004d1da/91656/60281/mona-lisa-bling-street-art-canvas-print-fine-pop-graffiti-wall-art.jpg?camera_label=side&revision=1790870965634", "url": "https://magickmicatv.store/product/32604604"}, {"name": "Cosmic Cloud Goddess Art Tee — Celestial Woman Graphic T-Shirt", "price": "$16.00", "img": "https://images-api.printify.com/mockup/6abdc49dd035a6f5e804af2a/38608/102044/cosmic-cloud-goddess-art-tee-celestial-woman-graphic-t-shirt.jpg?camera_label=front-2&revision=1790940588964", "url": "https://magickmicatv.store/product/32586359"}, {"name": "Mystic Egyptian Eye Matte Canvas Wall Art — Stretched Spiritual Goddess Decor", "price": "$30.00", "img": "https://images-api.printify.com/mockup/6abdc1e62cba60be0908d9d2/91657/60285/mystic-egyptian-eye-matte-canvas-wall-art-stretched-spiritual-goddess-decor.jpg?camera_label=side&revision=1790821190590", "url": "https://magickmicatv.store/product/32586164"}, {"name": "Glitch Goddess Scented Soy Candle — 9oz Aromatherapy Jar", "price": "$19.00", "img": "https://images-api.printify.com/mockup/6abdbfb136334c8c170a41c1/104680/110078/glitch-goddess-scented-soy-candle-9oz-aromatherapy-jar.jpg?camera_label=front&revision=1790973865136", "url": "https://magickmicatv.store/product/32585923"}, {"name": "Galaxy Goddess Square Pillow — Cosmic Woman Decorative Throw Pillow", "price": "$27.99", "img": "https://images-api.printify.com/mockup/6abd56f6628b113835002f7c/41674/47698/galaxy-goddess-square-pillow-cosmic-woman-decorative-throw-pillow.jpg?camera_label=front&revision=1790793519233", "url": "https://magickmicatv.store/product/32571736"}, {"name": "Retro TVs in Neon Ocean Matte Canvas Print — Surreal Vaporwave Wall Art", "price": "$30.00", "img": "https://images-api.printify.com/mockup/6abd180746eec7fa970e1f0b/91644/60287/retro-tvs-in-neon-ocean-matte-canvas-print-surreal-vaporwave-wall-art.jpg?camera_label=side&revision=1790778250989", "url": "https://magickmicatv.store/product/32564467"}, {"name": "Mona Lisa Bling Desk Mat — Retro Art Mouse Pad with Sunglasses and Diamonds", "price": "$18.00", "img": "https://images-api.printify.com/mockup/6abd14d5a8d215dac00730b2/65240/6570/mona-lisa-bling-desk-mat-retro-art-mouse-pad-with-sunglasses-and-diamonds.jpg?camera_label=front&revision=1790857450765", "url": "https://magickmicatv.store/product/32563862"}, {"name": "Mona Lisa Bling Square Pillowcase", "price": "$18.99", "img": "https://images-api.printify.com/mockup/6abc8bb5ef8d165d570b2b20/41629/88916/mona-lisa-bling-square-pillowcase.jpg?camera_label=front&revision=1790742048552", "url": "https://magickmicatv.store/product/32555155"}, {"name": "Pixel Crystal Bedroom Art - Matte Stretched Canvas", "price": "$19.99", "img": "https://images-api.printify.com/mockup/6abc81fc42390930c90d7ce5/101418/95796/pixel-crystal-bedroom-art-matte-stretched-canvas.jpg?camera_label=side&revision=1790739493219", "url": "https://magickmicatv.store/product/32554094"}, {"name": "Psychedelic Goddess Art Poster — Rainbow Cosmic Female Silhouette in Colored Frame", "price": "$36.87", "img": "https://images-api.printify.com/mockup/6abc7fcd42390930c90d7c1b/253574/127507/psychedelic-goddess-art-poster-rainbow-cosmic-female-silhouette-in-colored-frame.jpg?camera_label=front&revision=1790789215702", "url": "https://magickmicatv.store/product/32553803"}, {"name": "Cosmic Goddess Scented Soy Candle — 13.75 oz", "price": "$25.99", "img": "https://images-api.printify.com/mockup/6abc7e7f226a46ee7e080448/76262/44713/cosmic-goddess-scented-soy-candle-1375-oz.jpg?camera_label=front&revision=1790738113272", "url": "https://magickmicatv.store/product/32553684"}, {"name": "Cosmic Aliens Hardcover Journal — Mystical Galaxy Art Notebook", "price": "$14.00", "img": "https://images-api.printify.com/mockup/6a7611f260c34fd96807a130/65223/7340/cosmic-aliens-hardcover-journal-mystical-galaxy-art-notebook.jpg?camera_label=opened&revision=1790731554165", "url": "https://magickmicatv.store/product/32550792"}, {"name": "Galaxy Spirit Tote Bag — Cosmic Woman All-Over Print", "price": "$21.00", "img": "https://images-api.printify.com/mockup/6abc6102254a19778e0e1d70/103599/100877/galaxy-spirit-tote-bag-cosmic-woman-all-over-print.jpg?camera_label=front&revision=1790730538174", "url": "https://magickmicatv.store/product/32550190"}];

  if (!PRODUCTS.length) return;

  /* ---- styles ------------------------------------------------------- */
  var CSS = [
    '.mms-wrap{--mms-gold:#F5C044;--mms-pink:#FF7AC8;--mms-cyan:#5FE8D0;',
    '  --mms-pearl:#FFF6FB;--mms-void:#0B0417;--mms-line:rgba(245,192,68,.22);',
    '  position:relative;z-index:2;max-width:1100px;margin:3rem auto 1.5rem;',
    '  padding:0 20px;box-sizing:border-box}',
    '.mms-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:.5rem 1rem;',
    '  justify-content:space-between;margin-bottom:1rem}',
    '.mms-title{font-family:"Space Mono",ui-monospace,Menlo,monospace;font-size:.7rem;',
    '  font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--mms-gold);margin:0}',
    '.mms-all{font-family:"Space Mono",ui-monospace,Menlo,monospace;font-size:.64rem;',
    '  letter-spacing:.16em;text-transform:uppercase;color:var(--mms-cyan);',
    '  text-decoration:none;border-bottom:1px dashed rgba(95,232,208,.5);padding-bottom:1px}',
    '.mms-all:hover{color:var(--mms-gold);border-bottom-color:var(--mms-gold)}',
    '.mms-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}',
    '.mms-card{display:flex;flex-direction:column;text-decoration:none;color:inherit;',
    '  background:rgba(11,4,23,.55);border:1px solid var(--mms-line);border-radius:6px;',
    '  overflow:hidden;transition:transform .18s,border-color .18s,box-shadow .18s}',
    '.mms-card:hover{transform:translateY(-3px);border-color:rgba(255,122,200,.55);',
    '  box-shadow:0 14px 34px rgba(0,0,0,.45)}',
    '.mms-shot{position:relative;aspect-ratio:1/1;background:#140a24;overflow:hidden}',
    '.mms-shot img{width:100%;height:100%;object-fit:cover;display:block;',
    '  filter:brightness(.74) saturate(1.04) contrast(1.03);transition:filter .24s}',
    /* Printify shoots on white, which punches four bright holes in a dark
       page. Multiplying a plum wash over it did sink the white, but it
       dirtied the artwork with it. Dimming the whole frame and laying a
       thin violet veil over the top tints it without touching the colour
       relationships inside the product, and both lift on hover so the art
       comes back true when someone is actually looking at it. */
    '.mms-shot::after{content:"";position:absolute;inset:0;pointer-events:none;',
    '  background:linear-gradient(168deg,rgba(183,156,255,.26),rgba(43,18,64,.48));',
    '  box-shadow:inset 0 0 64px 10px rgba(11,4,23,.6);transition:opacity .24s}',
    '.mms-card:hover .mms-shot::after{opacity:.35}',
    '.mms-card:hover .mms-shot img{filter:brightness(1.02) saturate(1.05) contrast(1.02)}',
    '.mms-body{padding:10px 11px 12px;display:flex;flex-direction:column;gap:5px;flex:1}',
    '.mms-name{font-family:Georgia,"Cormorant Garamond",serif;font-size:.92rem;line-height:1.25;',
    '  color:var(--mms-pearl);margin:0;display:-webkit-box;-webkit-line-clamp:2;',
    '  -webkit-box-orient:vertical;overflow:hidden}',
    '.mms-price{font-family:"Space Mono",ui-monospace,Menlo,monospace;font-size:.76rem;',
    '  font-weight:700;color:var(--mms-gold);margin-top:auto}',
    '.mms-note{font-family:"Space Mono",ui-monospace,Menlo,monospace;font-size:.6rem;',
    '  letter-spacing:.1em;color:rgba(255,246,251,.4);margin-top:.9rem;text-align:center}',
    '@media (max-width:760px){.mms-grid{grid-template-columns:repeat(2,minmax(0,1fr))}',
    '  .mms-wrap{margin-top:2.2rem}}',
    '@media (prefers-reduced-motion:reduce){.mms-card{transition:none}',
    '  .mms-card:hover{transform:none}}'
  ].join('');

  /* ---- pick four, without repeating ---------------------------------- */
  function pick(n) {
    var pool = PRODUCTS.filter(function (p) { return p.img && p.name; }).slice();
    for (var i = pool.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = pool[i]; pool[i] = pool[j]; pool[j] = t;
    }
    return pool.slice(0, Math.min(n, pool.length));
  }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function build() {
    var wrap = el('section', 'mms-wrap');
    wrap.setAttribute('aria-label', 'From the Magick Mica TV store');

    var head = el('div', 'mms-head');
    head.appendChild(el('h2', 'mms-title', '✦ Magick Mica TV Store'));
    var all = el('a', 'mms-all', 'See everything →');
    all.href = STORE; all.target = '_blank'; all.rel = 'noopener';
    head.appendChild(all);
    wrap.appendChild(head);

    var grid = el('div', 'mms-grid');
    pick(SHOW).forEach(function (p) {
      var a = el('a', 'mms-card');
      a.href = p.url || STORE; a.target = '_blank'; a.rel = 'noopener';

      var shot = el('div', 'mms-shot');
      var img = el('img');
      img.src = p.img;
      img.alt = p.name;
      img.loading = 'lazy';
      img.decoding = 'async';
      // A dead mockup url should lose the picture, not the whole card.
      img.onerror = function () { shot.removeChild(img); };
      shot.appendChild(img);
      a.appendChild(shot);

      var body = el('div', 'mms-body');
      body.appendChild(el('h3', 'mms-name', p.name));
      if (p.price) body.appendChild(el('div', 'mms-price', p.price));
      a.appendChild(body);

      grid.appendChild(a);
    });
    wrap.appendChild(grid);
    wrap.appendChild(el('div', 'mms-note',
      'Prices as of ' + COLLECTED + ' · magickmicatv.store'));
    return wrap;
  }

  function mount() {
    if (document.querySelector('.mms-wrap')) return;   // never twice
    var style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);

    var strip = build();
    // Above the footer where there is one, otherwise at the end of the page,
    // but always before the nav script's drawer so it cannot sit on top of it.
    var foot = document.querySelector('footer, .site-footer, #footer');
    if (foot && foot.parentNode) foot.parentNode.insertBefore(strip, foot);
    else document.body.appendChild(strip);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
