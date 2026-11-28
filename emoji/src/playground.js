/* Magick Mica Emoji Playground: UI. Data lives in playground-data.js.
   Uses the site's shared helpers from app.js: el, store, BYCHAR, BYSLUG, bare, withTone, copyText, toast, sec. */

const REDUCED_MOTION = (() => { try { return matchMedia("(prefers-reduced-motion: reduce)").matches; } catch(e){ return false; } })();

/* ---- category pools, resolved against the main dataset ---- */
const SHUFFLE_POOLS = {};
(function buildPools(){
  const resolve = str => [...new Set(str.split(/\s+/).filter(Boolean).map(c => BYCHAR[bare(c)]).filter(Boolean))];
  SHUFFLE_CATEGORIES.forEach(c => { SHUFFLE_POOLS[c.id] = resolve(c.pool || ""); });
  SHUFFLE_CATEGORIES.filter(c => c.includeAll).forEach(c => {
    const all = new Set(SHUFFLE_POOLS[c.id]);
    SHUFFLE_CATEGORIES.forEach(o => SHUFFLE_POOLS[o.id].forEach(x => all.add(x)));
    SHUFFLE_POOLS[c.id] = [...all];
  });
})();

/* ---- shuffler state (saved per visitor; bad saved data is ignored) ---- */
const SHUFFLER_KEY = "sme-shuffler";
function loadShuffler(){
  const fresh = {cat:"everything", count:5, slots:[]};
  const s = store.get(SHUFFLER_KEY, null);
  if (!s || typeof s !== "object") return fresh;
  const cat = SHUFFLE_CATEGORIES.some(c => c.id === s.cat) ? s.cat : fresh.cat;
  const count = SHUFFLE_COUNTS.includes(s.count) ? s.count : fresh.count;
  const slots = Array.isArray(s.slots) ? s.slots.filter(x => x && typeof x.s === "string" && BYSLUG[x.s]).map(x => ({x:BYSLUG[x.s], locked:x.l === true})).slice(0, count) : [];
  return {cat, count, slots};
}
function saveShuffler(st){ store.set(SHUFFLER_KEY, {cat:st.cat, count:st.count, slots:st.slots.map(s => ({s:s.x.slug, l:s.locked}))}); }

/* Fill every unlocked slot with a random emoji from the pool.
   No duplicates while the pool has enough unique emojis; tries not to repeat the previous mix. */
function shuffleSlots(st){
  const pool = SHUFFLE_POOLS[st.cat] || [];
  if (!pool.length) return;
  const prev = st.slots.map(s => s.x && s.x.slug).join(",");
  for (let attempt = 0; attempt < 12; attempt++){
    const used = new Set(st.slots.filter(s => s.locked).map(s => s.x));
    const choices = pool.filter(x => !used.has(x));
    for (let i = choices.length - 1; i > 0; i--){ const j = Math.floor(Math.random() * (i + 1)); [choices[i], choices[j]] = [choices[j], choices[i]]; }
    let k = 0;
    st.slots.forEach(s => {
      if (s.locked) return;
      s.x = k < choices.length ? choices[k++] : pool[Math.floor(Math.random() * pool.length)]; // pool too small: allow repeats
    });
    const now = st.slots.map(s => s.x.slug).join(",");
    if (now !== prev || choices.length <= st.slots.filter(s => !s.locked).length) break;
  }
}
function fitCount(st){
  while (st.slots.length > st.count) st.slots.pop();
  if (st.slots.length < st.count){
    const start = st.slots.length;
    while (st.slots.length < st.count) st.slots.push({x:null, locked:false});
    // fill only the new empty slots
    const keep = st.slots.map(s => s.locked); st.slots.forEach((s, i) => { if (i < start) s.locked = true; });
    shuffleSlots(st); st.slots.forEach((s, i) => s.locked = keep[i]);
  }
}

/* ---- the Shuffler panel ---- */
function shufflerPanel(){
  const st = loadShuffler();
  if (st.slots.length !== st.count || st.slots.some(s => !s.x)){ fitCount(st); }
  if (!st.slots.length){ fitCount(st); }

  const win = el("section", "pg-win pg-shuffler"); win.id = "shuffler"; win.setAttribute("aria-labelledby", "shuf-title");
  const bar = el("div", "pg-bar"); bar.setAttribute("aria-hidden", "true");
  bar.append(el("span", "pg-bar-t", "✦ emoji_shuffler.exe"), el("span", "pg-dots", "● ● ●"));
  win.appendChild(bar);
  const body = el("div", "pg-body"); win.appendChild(body);
  ["s1","s2","s3","s4"].forEach(c => body.appendChild(el("span", "px-star " + c)));

  const h = el("h2", "pg-title", "✨ EMOJI SHUFFLER ✨"); h.id = "shuf-title"; body.appendChild(h);
  body.appendChild(el("p", "pg-tag", "A little randomness makes life more magical."));

  // category picker
  const catLab = el("div", "pg-label", "Category"); catLab.id = "shuf-cat-l"; body.appendChild(catLab);
  const cats = el("div", "pg-chips"); cats.setAttribute("role", "group"); cats.setAttribute("aria-labelledby", "shuf-cat-l"); body.appendChild(cats);
  // count picker
  const cntLab = el("div", "pg-label", "How many emojis?"); cntLab.id = "shuf-cnt-l"; body.appendChild(cntLab);
  const counts = el("div", "pg-seg"); counts.setAttribute("role", "group"); counts.setAttribute("aria-labelledby", "shuf-cnt-l"); body.appendChild(counts);

  // result
  const res = el("div", "pg-result"); res.setAttribute("role", "group"); res.setAttribute("aria-label", "Your magick mix"); body.appendChild(res);
  body.appendChild(el("p", "pg-hint", "🔒 Tap an emoji to lock or unlock it. Keep the ones you love, shuffle the rest."));
  const status = el("p", "pg-status"); status.setAttribute("role", "status"); status.setAttribute("aria-live", "polite"); body.appendChild(status);

  // actions
  const acts = el("div", "pg-acts");
  const bShuf = el("button", "pg-big", "SHUFFLE THE MAGIC"); bShuf.type = "button";
  const bCopy = el("button", "pg-btn", "📋 Copy mix"); bCopy.type = "button";
  const bReset = el("button", "pg-btn ghost", "↺ Reset"); bReset.type = "button";
  const bSave = el("button", "pg-btn ghost", "♡ Save mix"); bSave.type = "button";
  acts.append(bShuf, bCopy, bSave, bReset); body.appendChild(acts);
  const fallback = el("div", "pg-fallback"); fallback.hidden = true;
  fallback.appendChild(el("p", null, "Your browser didn't let the page copy. Select the emojis below and copy them yourself:"));
  const fbInput = el("input"); fbInput.type = "text"; fbInput.readOnly = true; fbInput.setAttribute("aria-label", "Your mix, ready to copy"); fallback.appendChild(fbInput);
  body.appendChild(fallback);

  const say = msg => { status.textContent = msg; };
  const mixText = () => st.slots.map(s => withTone(s.x)).join(" ");

  function drawCats(){
    cats.innerHTML = "";
    SHUFFLE_CATEGORIES.forEach(c => {
      const b = el("button", "pg-chip" + (c.id === st.cat ? " on" : "")); b.type = "button";
      b.setAttribute("aria-pressed", c.id === st.cat); b.title = c.blurb;
      b.append(el("span", "pg-ci", c.icon), document.createTextNode(c.name));
      b.addEventListener("click", () => { if (st.cat === c.id) return; st.cat = c.id; shuffleSlots(st); saveShuffler(st); drawCats(); drawSlots(true); say(c.icon + " " + c.name + ": " + c.blurb + ". Your magick mix is ready."); });
      cats.appendChild(b);
    });
  }
  function drawCounts(){
    counts.innerHTML = "";
    SHUFFLE_COUNTS.forEach(n => {
      const b = el("button", "pg-segb" + (n === st.count ? " on" : ""), String(n)); b.type = "button";
      b.setAttribute("aria-pressed", n === st.count); b.setAttribute("aria-label", n + " emojis");
      b.addEventListener("click", () => { if (st.count === n) return; st.count = n; fitCount(st); saveShuffler(st); drawCounts(); drawSlots(false); say(n + " emojis. Your magick mix is ready."); });
      counts.appendChild(b);
    });
  }
  function drawSlots(animate){
    res.innerHTML = "";
    res.classList.toggle("ten", st.count === 10);
    st.slots.forEach((s, i) => {
      const b = el("button", "pg-slot" + (s.locked ? " locked" : "")); b.type = "button";
      b.setAttribute("aria-pressed", s.locked);
      b.setAttribute("aria-label", (i + 1) + ": " + s.x.name + (s.locked ? ", locked. Tap to unlock." : ". Tap to lock."));
      b.appendChild(el("span", "pg-emo", withTone(s.x)));
      b.appendChild(el("span", "pg-lock", s.locked ? "🔒 Locked" : "Tap to keep"));
      if (animate && !s.locked && !REDUCED_MOTION){ b.classList.add("spin"); b.style.animationDelay = (i * 45) + "ms"; }
      b.addEventListener("click", () => {
        s.locked = !s.locked; saveShuffler(st); drawSlots(false);
        const again = res.querySelectorAll(".pg-slot")[i]; if (again) again.focus();
        say(s.locked ? "Keep this one! " + withTone(s.x) + " is locked." : withTone(s.x) + " unlocked.");
      });
      res.appendChild(b);
    });
  }

  bShuf.addEventListener("click", () => {
    if (st.slots.every(s => s.locked)){ say("Everything is locked! Unlock an emoji to shuffle again."); return; }
    shuffleSlots(st); saveShuffler(st); drawSlots(true); fallback.hidden = true;
    say(["Your magick mix is ready.", "One more shuffle?", "A tiny surprise from the emoji universe.", "Your next favorite combination might be one click away."][Math.floor(Math.random() * 4)]);
  });
  bCopy.addEventListener("click", async () => {
    const t = mixText();
    const ok = await copyText(t);
    if (ok){ fallback.hidden = true; say("Copied! " + t); bCopy.textContent = "✓ Copied!"; clearTimeout(bCopy._t); bCopy._t = setTimeout(() => bCopy.textContent = "📋 Copy mix", 1600); toast("Copied " + t); }
    else { fbInput.value = t; fallback.hidden = false; fbInput.focus(); fbInput.select(); say("Couldn't copy automatically. Your mix is selected below so you can copy it."); }
  });
  bSave.addEventListener("click", () => {
    const t = mixText();
    if (isSaved(t)){ say("This mix is already in your Favorites ♥"); return; }
    toggleSaved(t); say("Saved to Favorites ♥ " + t);
  });
  bReset.addEventListener("click", () => {
    st.slots.forEach(s => s.locked = false); shuffleSlots(st); saveShuffler(st); drawSlots(true); fallback.hidden = true;
    say("All unlocked. Fresh " + SHUFFLE_CATEGORIES.find(c => c.id === st.cat).name + " mix!");
  });

  drawCats(); drawCounts(); drawSlots(false); saveShuffler(st);
  return win;
}

/* ---- Playground page ---- */
function pagePlayground(app, tool){
  const head = el("div", "pg-hero");
  head.appendChild(el("h1", "pg-h1", "Magick Mica Emoji Playground"));
  head.appendChild(el("p", "pg-sub", "Collect • Shuffle • Play • Create"));
  app.appendChild(head);
  app.appendChild(shufflerPanel());

  const s = el("section"); const sh = el("div", "sh"); sh.appendChild(el("h2", null, "🎪 Explore the Playground")); sh.appendChild(el("span", "sub", "more toys are on the way"));
  s.appendChild(sh);
  const cards = el("div", "pg-cards");
  PLAYGROUND_TOOLS.forEach(t => {
    const live = t.status === "live";
    const c = el(live ? "a" : "div", "pg-card" + (live ? "" : " soon"));
    if (live){ c.href = "#/playground/" + t.id; }
    c.appendChild(el("div", "pg-card-i", t.icon));
    c.appendChild(el("b", null, t.name));
    c.appendChild(el("span", null, t.blurb));
    c.appendChild(el("em", "pg-badge" + (live ? " live" : ""), live ? "▶ Play now" : "Coming soon"));
    if (!live) c.setAttribute("aria-label", t.name + ", coming soon");
    cards.appendChild(c);
  });
  s.appendChild(cards); app.appendChild(s);

  const back = el("p", "pg-back"); const a = el("a", "btn ghost", "← Back to the emoji directory"); a.href = "#/"; back.appendChild(a); app.appendChild(back);

  if (tool){
    const t = PLAYGROUND_TOOLS.find(x => x.id === tool);
    if (t && t.status === "live"){ const target = document.getElementById(t.id); if (target) setTimeout(() => target.scrollIntoView({block:"start"}), 0); }
    else if (t){ const n = el("p", "pg-status", t.icon + " " + t.name + " is coming soon. Try the Shuffler in the meantime!"); app.insertBefore(n, app.children[1]); }
  }
}

/* small banner used on the home page */
function playgroundTeaser(){
  const a = el("a", "pg-teaser"); a.href = "#/playground";
  a.appendChild(el("span", "pg-teaser-i", "🎲"));
  const t = el("span"); t.appendChild(el("b", null, "New! Emoji Playground")); t.appendChild(el("span", null, "Shuffle a magick mix, lock your favorites, copy it in one tap."));
  a.appendChild(t); a.appendChild(el("span", "pg-teaser-go", "SHUFFLE →"));
  return a;
}
