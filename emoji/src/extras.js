/* From the Magick Mica Emoji Universe: Egyptian page, A–Z Letters, saving any combo,
   plus the Bookmark button. Uses shared helpers from app.js. */

/* ---------- Saved combos & text (lives on the Favorites page) ---------- */
let savedText = strList(store.get("sme-saved", []));
const isSaved = t => savedText.includes(t);
function toggleSaved(t){
  if (isSaved(t)){ savedText = savedText.filter(x => x !== t); toast("Removed from Favorites"); }
  else { savedText = [t, ...savedText].slice(0, 300); toast("Saved ♡ " + t + "  (see Favorites)"); }
  store.set("sme-saved", savedText);
  return isSaved(t);
}
/* a copyable text tile with a small ♡ save button in its corner */
function savableTile(t, label){
  const w = el("div", "tw");
  const b = textTile(t); if (label){ b.appendChild(el("small", "lbl", label)); }
  const h = el("button", "sv" + (isSaved(t) ? " on" : ""), isSaved(t) ? "♥" : "♡"); h.type = "button";
  const lab = () => (isSaved(t) ? "Remove from favorites: " : "Save to favorites: ") + t;
  h.setAttribute("aria-label", lab()); h.title = isSaved(t) ? "Saved" : "Save to Favorites";
  h.addEventListener("click", e => { e.stopPropagation(); const on = toggleSaved(t); h.classList.toggle("on", on); h.textContent = on ? "♥" : "♡"; h.setAttribute("aria-label", lab()); h.title = on ? "Saved" : "Save to Favorites"; });
  w.append(b, h); return w;
}
function savableGrid(list, cls){ const g = el("div", "grid " + (cls || "combo")); list.forEach(t => g.appendChild(savableTile(t))); return g; }

/* ---------- Egyptian ---------- */
/* Draw hieroglyphs only once the bundled font is ready; otherwise some browsers keep showing boxes. */
const HIERO_RE = /[\u{13000}-\u{1343F}]/u;
let hieroReady = false;
function withHieroFont(app, draw){
  if (hieroReady || !document.fonts || !document.fonts.load){ draw(); return; }
  const where = location.hash;
  app.appendChild(el("p", "empty", "𓂀 Loading hieroglyphs…"));
  const go = () => { if (hieroReady) return; hieroReady = true; if (location.hash === where){ app.innerHTML = ""; draw(); } };
  document.fonts.load('24px "MM Hieroglyphs"', "\u{13080}").then(go, go);
  setTimeout(go, 2500);
}
function pageEgyptian(app, which){ withHieroFont(app, () => drawEgyptian(app, which)); }
function drawEgyptian(app, which){
  const x = which ? EGYPT_SETS.find(y => y.s === which) : null;
  if (which && !x){ app.appendChild(el("p", "empty", "That Egyptian set isn't here.")); return; }
  if (x){ const back = el("a", "crumb", "← all Egyptian"); back.href = "#/egyptian"; app.appendChild(back); }
  app.appendChild(el("h1", "pagetitle hiero", x ? x.i + " " + x.n : "𓂀 Egyptian"));
  app.appendChild(el("p", "pagesub", x ? x.d + ". Tap to copy, ♡ to save." : "Hieroglyph combos and all 1,071 Egyptian hieroglyphs. Tap to copy, ♡ to save."));
  const bar = setBar([...EGYPT_SETS, {s:"hieroglyphs", n:"All 1,071 hieroglyphs", i:"📜"}], "egyptian", which);
  bar.classList.add("hiero"); app.appendChild(bar);
  if (x){ app.appendChild(savableGrid(x.t, "combo hiero")); return; }
  EGYPT_SETS.forEach(y => app.appendChild(sec(y.i + " " + y.n, y.t.length + " combos · " + y.d, savableGrid(y.t.slice(0, 18), "combo hiero"), "#/egyptian/" + y.s, "All " + y.t.length + " →")));
  const s = sec("📜 All 1,071 hieroglyphs", "every Egyptian hieroglyph in Unicode", null, "#/egyptian/hieroglyphs", "Open →");
  const list = []; for (let c = HIEROGLYPH_FIRST; c < HIEROGLYPH_FIRST + 60; c++) list.push(String.fromCodePoint(c));
  s.appendChild(textGrid(list, "sym hiero")); app.appendChild(s);
  app.appendChild(el("p", "pagesub", "Hieroglyphs show on this page everywhere. Once pasted elsewhere they use your reader's fonts: most newer phones and computers show them, some older ones show boxes."));
}
function pageHieroglyphs(app){ withHieroFont(app, () => drawHieroglyphs(app)); }
function drawHieroglyphs(app){
  const back = el("a", "crumb", "← all Egyptian"); back.href = "#/egyptian"; app.appendChild(back);
  app.appendChild(el("h1", "pagetitle hiero", "📜 All Egyptian hieroglyphs"));
  app.appendChild(el("p", "pagesub", "1,071 symbols. Hover to see each one's code, tap to copy."));
  const g = el("div", "grid sym hiero");
  for (let c = HIEROGLYPH_FIRST; c <= HIEROGLYPH_LAST; c++){
    const t = String.fromCodePoint(c); const b = textTile(t); const code = "U+" + c.toString(16).toUpperCase();
    b.title = "Copy hieroglyph " + code; b.setAttribute("aria-label", "Copy Egyptian hieroglyph " + code); g.appendChild(b);
  }
  app.appendChild(g);
}

/* ---------- A–Z Letters ---------- */
const LETTER_STYLES = [...SCRIPT_STYLES.slice(0, 16), {n:"Glitch", f:ch => /\s/.test(ch) ? ch : ch + "̴"}, ...SCRIPT_STYLES.slice(16)];
const AZ_EMOJI = {A:"👽",B:"🦋",C:"🏰",D:"💎",E:"👁️",F:"🔥",G:"👾",H:"🔮",I:"🍦",J:"🪼",K:"🗝️",L:"💡",M:"🌙",N:"🌌",O:"🪐",P:"💊",Q:"👑",R:"🌹",S:"❄️",T:"📺",U:"🦄",V:"📼",W:"🪄",X:"❌",Y:"💛",Z:"⚡"};
let azStyle = store.get("sme-az-style", 0); if (!(Number.isInteger(azStyle) && azStyle >= 0 && azStyle < LETTER_STYLES.length)) azStyle = 0;
let azText = "Magick Mica";
function pageLetters(app){
  app.appendChild(el("h1", "pagetitle", "🔤 A–Z Letters"));
  app.appendChild(el("p", "pagesub", "Fancy letters for names, titles and bios. Best for short bits: screen readers and search may not read them as normal words."));
  const card = el("div", "card");
  card.appendChild(el("div", "lbl2", "✍️ Fancy letter typer"));
  const inp = el("input"); inp.type = "search"; inp.value = azText; inp.style.width = "100%"; inp.setAttribute("aria-label", "Text to turn into fancy letters"); card.appendChild(inp);
  const lab = el("label", "pagesub"); lab.style.display = "flex"; lab.style.gap = "8px"; lab.style.alignItems = "center"; lab.style.marginTop = "10px";
  const cb = el("input"); cb.type = "checkbox"; lab.append(cb, document.createTextNode("Add a sparkle frame ⋆｡°✩ … ✩°｡⋆")); card.appendChild(lab);
  const cg = el("div", "grid combo script"); cg.style.marginTop = "10px"; card.appendChild(cg); app.appendChild(card);
  const drawConv = () => { azText = inp.value; cg.innerHTML = ""; const raw = inp.value || "Magick Mica";
    LETTER_STYLES.forEach(st => { let t = scriptText(raw, st); if (cb.checked) t = "⋆｡°✩ " + t + " ✩°｡⋆"; cg.appendChild(savableTile(t, st.n)); }); };
  inp.addEventListener("input", drawConv); cb.addEventListener("change", drawConv); drawConv();

  const s = el("section"); const sh = el("div", "sh"); sh.appendChild(el("h2", null, "🔠 Alphabet by style")); s.appendChild(sh);
  const nav = el("div", "azstyles"); s.appendChild(nav);
  const row = el("div", "btns"); row.style.marginTop = "10px"; const all = el("button", "btn ghost", "📋 Copy the whole A–Z"); all.type = "button"; row.appendChild(all); s.appendChild(row);
  const g = el("div"); s.appendChild(g);
  const s2 = el("section"); const sh2 = el("div", "sh"); sh2.appendChild(el("h2", null, "🪐 Emoji alphabet")); sh2.appendChild(el("span", "sub", "each letter with a Magick Mica emoji, in the style above")); s2.appendChild(sh2);
  const g2 = el("div"); s2.appendChild(g2);
  app.append(s, s2);
  const draw = () => {
    nav.innerHTML = ""; LETTER_STYLES.forEach((st, i) => { const b = el("button", "kw" + (i === azStyle ? " on" : ""), scriptText(st.n, st)); b.type = "button"; b.setAttribute("aria-label", st.n); b.setAttribute("aria-pressed", i === azStyle);
      b.addEventListener("click", () => { azStyle = i; store.set("sme-az-style", i); draw(); }); nav.appendChild(b); });
    const st = LETTER_STYLES[azStyle]; g.innerHTML = ""; g2.innerHTML = "";
    const up = [..."ABCDEFGHIJKLMNOPQRSTUVWXYZ"].map(st.f), lo = [..."abcdefghijklmnopqrstuvwxyz"].map(st.f);
    g.appendChild(textGrid(up, "sym")); if (lo.join("") !== up.join("")) { const gl = textGrid(lo, "sym"); gl.style.marginTop = "6px"; g.appendChild(gl); }
    const pairs = [..."ABCDEFGHIJKLMNOPQRSTUVWXYZ"].map(L => st.f(L) + " " + AZ_EMOJI[L]);
    g2.appendChild(textGrid(pairs, "combo azemo"));
  };
  all.addEventListener("click", () => copyEmoji(null, [..."ABCDEFGHIJKLMNOPQRSTUVWXYZ"].map(LETTER_STYLES[azStyle].f).join(" ")));
  draw();
}

/* ---------- Bookmark button ---------- */
function setupBookmark(){
  const btn = document.getElementById("bmBtn"), pop = document.getElementById("bmPop");
  if (!btn || !pop) return;
  const ua = navigator.userAgent || "";
  const isMac = /Mac|iPhone|iPad|iPod/.test(navigator.platform || ua);
  const touch = (navigator.maxTouchPoints || 0) > 0 && /Mobi|Android|iPhone|iPad|iPod/.test(ua);
  const ios = /iPhone|iPad|iPod/.test(ua) || (/Mac/.test(ua) && (navigator.maxTouchPoints || 0) > 1);
  const close = () => { pop.hidden = true; btn.setAttribute("aria-expanded", "false"); };
  function open(){
    pop.innerHTML = "";
    pop.appendChild(el("div", "bm-t", "✨ Keep the magic close ✨"));
    if (touch){
      pop.appendChild(el("p", null, ios ? "Tap the Share button ⬆︎ in Safari, then “Add Bookmark” or “Add to Home Screen”." : "Open your browser menu ⋮, then tap the ☆ star or “Add to Home screen”."));
    } else {
      const k = el("div", "bm-keys"); (isMac ? ["⌘", "D"] : ["Ctrl", "D"]).forEach((x, i) => { if (i) k.appendChild(el("span", "plus", "+")); k.appendChild(el("kbd", null, x)); });
      pop.appendChild(k);
      pop.appendChild(el("p", null, "Press these together to bookmark this page."));
    }
    const row = el("div", "bm-row");
    if (navigator.share){ const s = el("button", "btn", "📤 Share / save link"); s.type = "button"; s.addEventListener("click", () => { navigator.share({title: document.title, url: location.href.split("#")[0]}).catch(() => {}); }); row.appendChild(s); }
    const c = el("button", "btn ghost", "🔗 Copy link"); c.type = "button";
    c.addEventListener("click", async () => { const ok = await copyText(location.href.split("#")[0]); c.textContent = ok ? "✓ Link copied!" : "Couldn't copy"; });
    row.appendChild(c); pop.appendChild(row);
    pop.appendChild(el("p", "bm-note", "Browsers don't let websites add bookmarks for you, so this is the quickest way."));
    pop.hidden = false; btn.setAttribute("aria-expanded", "true");
  }
  btn.addEventListener("click", e => { e.stopPropagation(); pop.hidden ? open() : close(); });
  pop.addEventListener("click", e => e.stopPropagation());
  document.addEventListener("click", close);
  document.addEventListener("keydown", e => { if (e.key === "Escape" && !pop.hidden){ close(); btn.focus(); } });
  window.addEventListener("hashchange", close);
}
setupBookmark();
