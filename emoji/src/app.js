/* Super Magick Emoji */
const $ = s => document.querySelector(s);
const el = (t, c, x) => { const e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; };
const store = {
  get(k, d){ try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch(e){ return d; } },
  set(k, v){ try { localStorage.setItem(k, JSON.stringify(v)); } catch(e){} }
};

/* ---- data ---- */
const ICON = {smileys_emotion:"😀", people_body:"👋", animals_nature:"🐻", food_drink:"🍔", travel_places:"✈️", activities:"⚽", objects:"💡", symbols:"💟", flags:"🏁"};
const SHORT = {smileys_emotion:"Smileys", people_body:"People", animals_nature:"Animals & Nature", food_drink:"Food & Drink", travel_places:"Travel", activities:"Activities", objects:"Objects", symbols:"Symbols", flags:"Flags"};
const ALL = [];   // {e,name,slug,skin,v,kw,g}
EMOJI_GROUPS.forEach(g => g.e.forEach(x => ALL.push({e:x[0], name:x[1], slug:x[2], skin:!!x[3], v:x[4], kw:x[5], g:g.s, gn:g.n})));
const BYSLUG = {}; ALL.forEach(x => BYSLUG[x.slug] = x);
const bare = s => s.replace(/️/g, "");
const BYCHAR = {}; ALL.forEach(x => BYCHAR[bare(x.e)] = x);
const VERSIONS = [...new Set(ALL.map(x => x.v))].sort((a, b) => parseFloat(b) - parseFloat(a));
const NEWEST = VERSIONS[0];
const YEAR = {"17.0":"2025","16.0":"2024","15.1":"2023","15.0":"2022","14.0":"2021","13.1":"2020","13.0":"2020","12.1":"2019","12.0":"2019","11.0":"2018","5.0":"2017","4.0":"2016","3.0":"2016","2.0":"2015","1.0":"2015","0.7":"2014","0.6":"2010"};
const POPULAR = "😂 ❤️ 🤣 👍 😭 🙏 😘 🥰 😍 😊 🎉 😁 💕 🥺 😅 🔥 ☺️ 🤦 🤷 🙄 😆 🤗 😉 🎂 🤔 👏 🙂 😳 🥳 😎 👌 💜 😔 💪 ✨ 💖 👀 😋 😏 😢 👉 💗 😩 💯 🌹 💞 🎈 💙 😃 😡 💐 😜 🙈 🤞 😄 🤤 🙌 🤪 ❣️ 😀 💋 💀 👇 💔 😌 💓 🤩 🙃 😬 😱 😴 🤭 😐 🌞 😒 😇 🌸 😈 🎶 ✌️ 🎊 🥵 😞 💚 ☀️ 🖤 💰 😚 👑 🎁 💥 🙋 😑 🥴 👈 💩 ✅ 🫶 🥹 🫠 🫡".split(" ").map(c => BYCHAR[bare(c)]).filter(Boolean);

/* ---- skin tone ---- */
const TONES = [["","✋","Default"],["\u{1F3FB}","✋🏻","Light"],["\u{1F3FC}","✋🏼","Medium-light"],["\u{1F3FD}","✋🏽","Medium"],["\u{1F3FE}","✋🏾","Medium-dark"],["\u{1F3FF}","✋🏿","Dark"]];
let tone = store.get("sme-tone", 0); if (!(tone >= 0 && tone < TONES.length)) tone = 0;
function withTone(x, t){ t = t === undefined ? tone : t; const m = TONES[t][0]; if (!m || !x.skin) return x.e; const c = [...x.e]; if (c[1] === "️") c.splice(1, 1); c.splice(1, 0, m); return c.join(""); }

/* ---- copy, recent, favorites ---- */
const strList = v => Array.isArray(v) ? v.filter(x => typeof x === "string") : [];   // ignore malformed saved data
let recent = strList(store.get("sme-recent", [])), favs = strList(store.get("sme-favs", []));
function toast(text, slug){
  $("#toastT").textContent = text; const a = $("#toastA");
  if (slug){ a.hidden = false; a.href = "#/e/" + slug; } else a.hidden = true;
  $("#toast").hidden = false; clearTimeout(toast.t); toast.t = setTimeout(() => $("#toast").hidden = true, 2600);
}
async function copyText(text){
  try { await navigator.clipboard.writeText(text); return true; }
  catch(e){ const ta = el("textarea", "fb"); ta.value = text; document.body.appendChild(ta); ta.select(); let ok = false; try { ok = document.execCommand("copy"); } catch(_){} ta.remove(); return ok; }
}
async function copyEmoji(x, text, node){
  const ok = await copyText(text);
  if (!ok){ toast("Couldn't copy: press and hold the emoji to copy it yourself"); return; }
  if (node){ node.classList.remove("flash"); void node.offsetWidth; node.classList.add("flash"); }
  if (x){ recent = [x.slug, ...recent.filter(s => s !== x.slug)].slice(0, 30); store.set("sme-recent", recent); toast("Copied " + text + "  " + x.name, x.slug); }
  else toast("Copied " + text);
}
function toggleFav(slug){ favs = favs.includes(slug) ? favs.filter(s => s !== slug) : [slug, ...favs]; store.set("sme-favs", favs); }

/* ---- tiles ---- */
function tile(x, named){
  const text = withTone(x);
  const b = el("button", "e"); b.title = x.name; b.setAttribute("aria-label", "Copy " + x.name);
  b.appendChild(document.createTextNode(text));
  if (named) b.appendChild(el("small", null, x.name));
  if (x.v === NEWEST) b.appendChild(el("span", "newdot"));
  b.addEventListener("click", () => copyEmoji(x, text, b));
  return b;
}
function grid(list, named){ const g = el("div", "grid" + (named ? " named" : "")); list.forEach(x => g.appendChild(tile(x, named))); return g; }
function sec(title, sub, child, moreHref, moreText){
  const s = el("section"); const h = el("div", "sh"); h.appendChild(el("h2", null, title)); if (sub) h.appendChild(el("span", "sub", sub));
  if (moreHref){ const a = el("a", "more", moreText || "See all →"); a.href = moreHref; h.appendChild(a); }
  s.appendChild(h); if (child) s.appendChild(child); return s;
}

/* ---- search ---- */
function search(q){
  q = q.trim().toLowerCase(); if (!q) return [];
  const direct = BYCHAR[bare(q)];
  const mood = MOODS.find(m => m.s === q || m.n.toLowerCase() === q);
  const words = q.split(/\s+/);
  const scored = [];
  for (const x of ALL){
    const n = x.name.toLowerCase(), hay = n + " " + x.kw + " " + x.gn.toLowerCase();
    if (!words.every(w => hay.includes(w) || (w.length > 3 && w.endsWith("s") && hay.includes(w.slice(0, -1))))) continue;
    let s = 0;
    if (n === q) s += 100;
    if (n.startsWith(q)) s += 40;
    if (new RegExp("\\b" + q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).test(n)) s += 25;
    if (n.includes(q)) s += 15;
    if ((" " + x.kw + " ").includes(" " + q + " ")) s += 12;
    if (POPULAR.includes(x)) s += 6;
    s -= n.length / 50;
    scored.push([s, x]);
  }
  scored.sort((a, b) => b[0] - a[0]);
  const out = scored.map(p => p[1]);
  if (mood){ const rest = out.filter(x => !mood.list.includes(x)); out.length = 0; out.push(...mood.list, ...rest); }
  if (direct && !out.includes(direct)) out.unshift(direct);
  return out;
}

/* ---- shared bits ---- */
function toneBar(onChange){
  const t = el("div", "toolbar"); t.appendChild(el("span", null, "Skin tone:"));
  TONES.forEach((tn, i) => { const b = el("button", "tone" + (i === tone ? " on" : ""), tn[1]); b.title = tn[2]; b.setAttribute("aria-label", tn[2] + " skin tone"); b.setAttribute("aria-pressed", i === tone);
    b.addEventListener("click", () => { tone = i; store.set("sme-tone", i); onChange(); }); t.appendChild(b); });
  return t;
}
function groupBar(active){
  const g = el("nav", "groups"); g.setAttribute("aria-label", "Emoji groups");
  EMOJI_GROUPS.forEach(gr => { const a = el("a", gr.s === active ? "on" : ""); a.href = "#/g/" + gr.s; a.appendChild(el("b", null, ICON[gr.s])); a.appendChild(document.createTextNode(SHORT[gr.s])); g.appendChild(a); });
  return g;
}


/* ---- emotions ---- */
const MOODS = [
 {s:"happy", n:"Happy", i:"😊", d:"smiles, joy and good vibes", e:"😀 😃 😄 😁 😆 😊 ☺️ 🙂 😌 🥰 🤗 😇 🥳 🤩 😸 😺 🌞 ☀️ 🌈 🎉 ✨ 💃 🕺 🙌 👏 🎊 🌻 😹 🫶 💛"},
 {s:"love", n:"Love", i:"🥰", d:"crushes, hugs and hearts", e:"🥰 😍 😘 😗 😙 😚 😻 💋 💌 💘 💝 💖 💗 💓 💞 💕 💟 ❣️ ❤️ 🩷 🧡 💛 💚 💙 🩵 💜 🤎 🖤 🩶 🤍 ❤️‍🔥 💑 💏 👩‍❤️‍👨 🫶 🤟 🌹 💐 🥂"},
 {s:"laughing", n:"Laughing", i:"😂", d:"lol, lmao and dying", e:"😂 🤣 😆 😹 😅 😄 😁 🤭 😜 😝 🙃 💀 ☠️ 🫢"},
 {s:"sad", n:"Sad", i:"😢", d:"tears, heartbreak and blues", e:"😢 😭 😞 😔 😟 🙁 ☹️ 😥 😪 🥺 🥹 😿 💔 ❤️‍🩹 🫤 😓 😩 😫 🌧️ ☔ 💧 🥀"},
 {s:"angry", n:"Angry", i:"😠", d:"mad, annoyed and fuming", e:"😠 😡 🤬 😤 👿 😾 💢 🗯️ 🔥 💥 😒 🙄 🖕 👊 🌋 🤯"},
 {s:"surprised", n:"Surprised", i:"😮", d:"shocked, amazed and wow", e:"😮 😯 😲 😳 🤯 😱 🙀 😧 😦 🫨 🫢 ‼️ ⁉️ ❗ ❓ 😵 🤩 👀"},
 {s:"scared", n:"Scared", i:"😱", d:"nervous, worried and spooked", e:"😱 😨 😰 😧 🫣 🙀 😖 😬 🥶 👻 💀 🫨 😵‍💫 🫠"},
 {s:"silly", n:"Silly", i:"🤪", d:"goofy, cheeky and playful", e:"🤪 😜 😝 😛 🤡 🙃 🥴 🤠 🥸 🤓 😋 🫠 🐵 🙈 🙉 🙊 👅 💩"},
 {s:"cool", n:"Cool & confident", i:"😎", d:"chill, smug and unbothered", e:"😎 🕶️ 😏 😌 🤙 🆒 💅 👑 ✌️ 🫡 🤘 😼 🧊 💯 🔥"},
 {s:"thinking", n:"Thinking", i:"🤔", d:"curious, unsure and pondering", e:"🤔 🧐 🤨 😐 😑 😶 🫤 🤷 🤷‍♀️ 🤷‍♂️ 💭 🫥 🙄 😕 ❓ 💡 🫣"},
 {s:"embarrassed", n:"Embarrassed", i:"😳", d:"blushing, awkward and oops", e:"😳 😅 🫣 😬 🙈 🤦 🤦‍♀️ 🤦‍♂️ 😖 ☺️ 🥲 🫠 😶‍🌫️ 🤭"},
 {s:"tired", n:"Tired", i:"😴", d:"sleepy, bored and done", e:"😴 🥱 😪 😫 😩 💤 🛌 🛏️ 😮‍💨 😑 🫠 ☕ 🌙 🧸"},
 {s:"sick", n:"Sick", i:"🤒", d:"ill, gross and not okay", e:"🤒 🤕 🤢 🤮 🤧 😷 🥵 🥶 🥴 😵 😵‍💫 🤯 💊 🩹 🌡️ 🤰"},
 {s:"grateful", n:"Grateful", i:"🙏", d:"thanks, blessed and kind", e:"🙏 🥹 🤗 😇 💖 🫶 🤝 💐 🌸 ✨ 🌟 💫 👐 🫂"},
 {s:"excited", n:"Excited", i:"🤩", d:"hyped, pumped and can't wait", e:"🤩 🥳 😆 🙌 🎉 🎊 🚀 ⚡ 🔥 💥 🕺 💃 🤸 🏃 ✨ 💯 👏 🤑"},
 {s:"evil", n:"Mischievous", i:"😈", d:"sneaky, naughty and plotting", e:"😈 👿 😏 🤫 🫢 👀 🤭 😼 🐍 🃏 🔮 🦹 🦹‍♀️ 🖤"}
];
MOODS.forEach(m => { m.list = [...new Set(m.e.split(" ").map(c => BYCHAR[bare(c)]).filter(Boolean))]; });

function moodBar(active){
  const g = el("nav", "groups"); g.setAttribute("aria-label", "Emotions");
  MOODS.forEach(m => { const a = el("a", m.s === active ? "on" : ""); a.href = "#/emotions/" + m.s; a.appendChild(el("b", null, m.i)); a.appendChild(document.createTextNode(m.n)); g.appendChild(a); });
  return g;
}
function pageEmotions(app, which){
  const m = which ? MOODS.find(x => x.s === which) : null;
  if (which && !m){ app.appendChild(el("p", "empty", "That emotion isn't here.")); return; }
  if (m){ const back = el("a", "crumb", "← all emotions"); back.href = "#/emotions"; app.appendChild(back); }
  app.appendChild(el("h1", "pagetitle", m ? m.i + " " + m.n + " emojis" : "💭 Emotions"));
  app.appendChild(el("p", "pagesub", m ? "Emojis for feeling " + m.n.toLowerCase() + ": " + m.d + ". Tap to copy." : "Find the right emoji for how you feel. " + MOODS.length + " moods, tap one to see them all."));
  app.appendChild(moodBar(which));
  const tb = el("div"); app.appendChild(tb); const body = el("div"); app.appendChild(body);
  const draw = () => { tb.innerHTML = ""; tb.appendChild(toneBar(draw)); body.innerHTML = "";
    if (m){ body.appendChild(grid(m.list, true)); return; }
    MOODS.forEach(x => body.appendChild(sec(x.i + " " + x.n, x.d, grid(x.list), "#/emotions/" + x.s, "All " + x.list.length + " →"))); };
  draw();
}


/* ---- special symbols & combined emojis ---- */
function textTile(t){
  const b = el("button", "e" + ([...t].length > 2 ? " txt" : ""), t); b.setAttribute("aria-label", "Copy " + t); b.title = "Copy " + t;
  b.addEventListener("click", () => copyEmoji(BYCHAR[bare(t)] || null, t, b));
  return b;
}
function textGrid(list, cls){ const g = el("div", "grid " + (cls || "")); list.forEach(t => g.appendChild(textTile(t))); return g; }
function setBar(sets, base, active){
  const g = el("nav", "groups");
  sets.forEach(x => { const a = el("a", x.s === active ? "on" : ""); a.href = "#/" + base + "/" + x.s; a.appendChild(el("b", null, x.i)); a.appendChild(document.createTextNode(x.n)); g.appendChild(a); });
  return g;
}
const symList = x => [...new Set(x.t.split(" ").filter(Boolean))];
function pageSymbols(app, which){
  const x = which ? SYMBOL_SETS.find(y => y.s === which) : null;
  if (which && !x){ app.appendChild(el("p", "empty", "That symbol set isn't here.")); return; }
  if (x){ const back = el("a", "crumb", "← all symbols"); back.href = "#/symbols"; app.appendChild(back); }
  app.appendChild(el("h1", "pagetitle", x ? x.i + " " + x.n : "✦ Special symbols"));
  app.appendChild(el("p", "pagesub", "Text symbols that work almost anywhere you can type: bios, names, posts and messages. Tap to copy."));
  app.appendChild(setBar(SYMBOL_SETS, "symbols", which));
  if (x){ app.appendChild(textGrid(symList(x), "sym")); return; }
  SYMBOL_SETS.forEach(y => app.appendChild(sec(y.i + " " + y.n, symList(y).length + " symbols", textGrid(symList(y), "sym"), "#/symbols/" + y.s, "Open →")));
}
const ZWJ = ALL.filter(x => x.e.includes("\u200D"));
function pageCombos(app, which){
  const isOfficial = which === "official";
  const x = which && !isOfficial ? COMBO_SETS.find(y => y.s === which) : null;
  if (which && !x && !isOfficial){ app.appendChild(el("p", "empty", "That combo set isn't here.")); return; }
  if (which){ const back = el("a", "crumb", "← all combined emojis"); back.href = "#/combos"; app.appendChild(back); }
  app.appendChild(el("h1", "pagetitle", isOfficial ? "🧬 Official combined emojis" : x ? x.i + " " + x.n + " combos" : "🧩 Combined emojis"));
  app.appendChild(el("p", "pagesub", isOfficial ? "These are single emojis made by joining others together, like 🐻 + ❄️ = 🐻‍❄️. Newer phones show each as one picture; older ones may show the parts side by side." : "Emoji combinations ready to copy: reactions, aesthetics, love, party and more."));
  const bar = setBar([{s:"official", n:"Official combos", i:"🧬"}, ...COMBO_SETS], "combos", which); app.appendChild(bar);
  if (isOfficial){ app.appendChild(grid(ZWJ, true)); return; }
  if (x){ app.appendChild(savableGrid(x.t, "combo")); return; }
  COMBO_SETS.forEach(y => app.appendChild(sec(y.i + " " + y.n, y.t.length + " combos", savableGrid(y.t, "combo"), "#/combos/" + y.s, "Open →")));
  app.appendChild(sec("🧬 Official combined emojis", ZWJ.length + " emojis made of other emojis, like 🐻‍❄️ ❤️‍🔥 🧑‍🚀", grid(ZWJ.slice(0, 40)), "#/combos/official", "All " + ZWJ.length + " →"));
}

/* ---- pages ---- */
function pageHome(app, q){
  const hero = el("div", "hero");
  const h1 = el("h1"); h1.append("Every emoji, ", el("span", null, "one tap"), " away"); hero.appendChild(h1);
  hero.appendChild(el("p", null, "Search all " + ALL.length.toLocaleString() + " emojis by name or keyword. Tap one to copy it, then paste it anywhere."));
  const bs = el("div", "bigsearch"); bs.appendChild(el("span", "mag", "🔍"));
  const inp = el("input"); inp.type = "search"; inp.placeholder = "Search emojis: happy, cat, pizza, heart, party…"; inp.setAttribute("aria-label", "Search emojis"); inp.value = q || "";
  bs.appendChild(inp); hero.appendChild(bs);
  const tl = el("div", "tryline"); tl.append("Try: ");
  ["love", "laugh", "cat", "birthday", "fire", "moon", "flag"].forEach(w => { const b = el("button", null, w); b.addEventListener("click", () => { inp.value = w; draw(); inp.focus(); }); tl.appendChild(b); });
  hero.appendChild(tl);
  app.appendChild(hero);
  app.appendChild(playgroundTeaser());
  const tb = el("div"); app.appendChild(tb);
  app.appendChild(groupBar());
  const body = el("div"); app.appendChild(body);
  function draw(){
    tb.innerHTML = ""; tb.appendChild(toneBar(draw));
    body.innerHTML = ""; const v = inp.value.trim();
    if (v){
      const r = search(v);
      const lv = v.toLowerCase();
      const sets = [...EGYPT_SETS.map(y => ({...y, base:"egyptian"})), ...SUB_SETS.map(y => ({...y, base:"substack"})), ...SYMBOL_SETS.map(y => ({...y, base:"symbols"})), ...COMBO_SETS.map(y => ({...y, base:"combos"}))].filter(y => y.n.toLowerCase().includes(lv) || y.s.includes(lv));
      if (sets.length){ const g = el("nav", "groups"); sets.forEach(y => { const a = el("a"); a.href = "#/" + y.base + "/" + y.s; a.appendChild(el("b", null, y.i)); a.appendChild(document.createTextNode(y.n + (y.base === "symbols" ? " symbols" : y.base === "combos" ? " combos" : y.base === "egyptian" ? " · Egyptian" : " · Substack"))); g.appendChild(a); }); body.appendChild(g); }
      body.appendChild(sec("Results for “" + v + "”", r.length + " emoji" + (r.length === 1 ? "" : "s"), r.length ? grid(r.slice(0, 300), true) : el("p", "empty", "No emoji matches that. Try a simpler word, like “smile” or “dog”.")));
      return;
    }
    if (favs.length) body.appendChild(sec("⭐ Your favorites", null, grid(favs.map(s => BYSLUG[s]).filter(Boolean).slice(0, 40)), "#/favorites"));
    if (recent.length) body.appendChild(sec("🕘 Recently copied", null, grid(recent.map(s => BYSLUG[s]).filter(Boolean))));
    body.appendChild(sec("🔥 Popular", "the emojis people use most", grid(POPULAR)));
    const ms = sec("💭 Emotions", "how are you feeling?", moodBar(), "#/emotions", "All emotions →"); body.appendChild(ms);
    const eg = el("div"); eg.appendChild(setBar([...EGYPT_SETS, {s:"hieroglyphs", n:"All 1,071 hieroglyphs", i:"📜"}], "egyptian"));
    body.appendChild(sec("☥ Egyptian", "hieroglyph combos and every hieroglyph", eg, "#/egyptian", "Open Egyptian →"));
    body.appendChild(sec("🔤 A–Z Letters", "fancy letters for names, titles and bios", null, "#/letters", "Open A–Z →"));
    body.appendChild(sec("📰 Substack", "for writers, journalers, readers and podcasters", setBar(SUB_SETS, "substack"), "#/substack", "Open Substack →"));
    body.appendChild(sec("🧩 Combined emojis", "ready-made combos", setBar([{s:"official", n:"Official combos", i:"🧬"}, ...COMBO_SETS], "combos"), "#/combos", "All combos →"));
    body.appendChild(sec("✦ Special symbols", "stars, hearts, arrows and more", setBar(SYMBOL_SETS, "symbols"), "#/symbols", "All symbols →"));
    const newest = ALL.filter(x => x.v === NEWEST);
    body.appendChild(sec("🆕 Newest emojis", "Emoji " + NEWEST + (YEAR[NEWEST] ? " · " + YEAR[NEWEST] : ""), grid(newest, true), "#/new", "All new emojis →"));
    EMOJI_GROUPS.forEach(gr => { const list = ALL.filter(x => x.g === gr.s);
      body.appendChild(sec(ICON[gr.s] + " " + gr.n, list.length + " emojis", grid(list.slice(0, 48)), "#/g/" + gr.s, "All " + list.length + " →")); });
  }
  let t; inp.addEventListener("input", () => { clearTimeout(t); t = setTimeout(draw, 120); });
  draw(); if (q) inp.focus();
}

function pageGroup(app, slug){
  const gr = EMOJI_GROUPS.find(g => g.s === slug);
  if (!gr){ app.appendChild(el("p", "empty", "That group doesn't exist.")); return; }
  const tb = el("div"); app.append(groupBar(slug));
  app.appendChild(el("h1", "pagetitle", ICON[slug] + " " + gr.n));
  const list = ALL.filter(x => x.g === slug);
  app.appendChild(el("p", "pagesub", list.length + " emojis. Hover to see a name, tap to copy."));
  app.appendChild(tb); const body = el("div"); app.appendChild(body);
  const draw = () => { tb.innerHTML = ""; tb.appendChild(toneBar(draw)); body.innerHTML = ""; body.appendChild(grid(list)); };
  draw();
}

function pageAll(app){
  app.appendChild(el("h1", "pagetitle", "All emojis"));
  app.appendChild(el("p", "pagesub", "Every one of the " + ALL.length.toLocaleString() + " standard emojis, in the official Unicode order."));
  const tb = el("div"); app.appendChild(tb); app.appendChild(groupBar());
  const body = el("div"); app.appendChild(body);
  const draw = () => { tb.innerHTML = ""; tb.appendChild(toneBar(draw)); body.innerHTML = "";
    EMOJI_GROUPS.forEach(gr => { const list = ALL.filter(x => x.g === gr.s); body.appendChild(sec(ICON[gr.s] + " " + gr.n, list.length + " emojis", grid(list))); }); };
  draw();
}

function pageNew(app){
  app.appendChild(el("h1", "pagetitle", "🆕 New emojis"));
  app.appendChild(el("p", "pagesub", "The latest emojis, newest first. Brand-new ones only show up on phones and computers that are up to date: on older ones they may look like an empty box."));
  const tb = el("div"); app.appendChild(tb); const body = el("div"); app.appendChild(body);
  const draw = () => { tb.innerHTML = ""; tb.appendChild(toneBar(draw)); body.innerHTML = "";
    VERSIONS.filter(v => parseFloat(v) >= 13).forEach(v => { const list = ALL.filter(x => x.v === v);
      body.appendChild(sec("Emoji " + v, (YEAR[v] ? YEAR[v] + " · " : "") + list.length + " emojis", grid(list, true))); }); };
  draw();
}

function pageFavs(app){ if (HIERO_RE.test(savedText.join(""))) withHieroFont(app, () => drawFavs(app)); else drawFavs(app); }
function drawFavs(app){
  app.appendChild(el("h1", "pagetitle", "⭐ Favorites"));
  app.appendChild(el("p", "pagesub", "Everything you've saved: combos, mixes and letters (♡) and single emojis (☆). It's kept in this browser only."));
  const holder = el("div"); app.appendChild(holder);
  const clearBtn = (label, ask, fn) => { const b = el("button", "btn ghost small", label); b.type = "button";
    b.addEventListener("click", () => { if (confirmClear(b, ask)) { fn(); draw(); } }); return b; };
  function draw(){
    holder.innerHTML = "";
    // saved combos & text
    const s1 = sec("♡ Saved combos & text", savedText.length ? savedText.length + " saved" : null);
    if (!savedText.length) s1.appendChild(el("p", "empty", "Nothing saved yet. Tap ♡ on any combo, Shuffler mix, Egyptian combo or fancy-letter result."));
    else {
      const g = el("div", "grid combo");
      savedText.forEach(t => { const w = el("div", "tw"); const b = textTile(t); const x = el("button", "sv on", "×"); x.type = "button"; x.title = "Remove"; x.setAttribute("aria-label", "Remove from favorites: " + t);
        x.addEventListener("click", e => { e.stopPropagation(); toggleSaved(t); draw(); }); w.append(b, x); g.appendChild(w); });
      s1.appendChild(g);
      const row = el("div", "btns"); row.style.marginTop = "12px";
      const ca = el("button", "btn", "📋 Copy all saved"); ca.type = "button"; ca.addEventListener("click", () => copyEmoji(null, savedText.join("\n")));
      row.append(ca, clearBtn("Clear saved", "Tap again to clear all saved combos", () => { savedText = []; store.set("sme-saved", savedText); }));
      s1.appendChild(row);
    }
    holder.appendChild(s1);
    // favorite single emojis
    const list = favs.map(x => BYSLUG[x]).filter(Boolean);
    const s2 = sec("☆ Favorite emojis", list.length ? list.length + " starred" : null);
    if (!list.length) s2.appendChild(el("p", "empty", "No favorite emojis yet. Tap any emoji, choose “Details”, then press ☆ Favorite."));
    else { s2.appendChild(grid(list, true)); const row = el("div", "btns"); row.style.marginTop = "12px";
      const ca = el("button", "btn", "📋 Copy all"); ca.type = "button"; ca.addEventListener("click", () => copyEmoji(null, list.map(x => withTone(x)).join(" ")));
      row.append(ca, clearBtn("Clear favorites", "Tap again to clear all favorite emojis", () => { favs = []; store.set("sme-favs", favs); })); s2.appendChild(row); }
    holder.appendChild(s2);
    // recently copied
    const rec = recent.map(x => BYSLUG[x]).filter(Boolean);
    if (rec.length){ const s3 = sec("🕘 Recently copied", null, grid(rec, true)); const row = el("div", "btns"); row.style.marginTop = "12px";
      row.appendChild(clearBtn("Clear history", "Tap again to clear your history", () => { recent = []; store.set("sme-recent", recent); })); s3.appendChild(row); holder.appendChild(s3); }
  }
  draw();
}
/* two-tap confirm instead of a popup dialog */
function confirmClear(b, ask){
  if (b.dataset.armed){ return true; }
  b.dataset.armed = "1"; const old = b.textContent; b.textContent = ask; b.classList.add("armed");
  setTimeout(() => { if (b.isConnected){ delete b.dataset.armed; b.textContent = old; b.classList.remove("armed"); } }, 3000);
  return false;
}

function pageEmoji(app, slug){
  const x = BYSLUG[slug];
  if (!x){ app.appendChild(el("p", "empty", "That emoji wasn't found.")); return; }
  const back = el("a", "crumb", "← " + ICON[x.g] + " " + x.gn); back.href = "#/g/" + x.g; app.appendChild(back);
  const d = el("div", "detail");
  const left = el("div"); const big = el("div", "bigemoji", withTone(x)); left.appendChild(big); d.appendChild(left);
  const right = el("div", "card");
  right.appendChild(el("h1", null, x.name));
  const badges = el("div", "badges");
  if (x.v === NEWEST) badges.appendChild(el("span", "badge new", "NEW"));
  badges.appendChild(el("span", "badge", "Emoji " + x.v + (YEAR[x.v] ? " · " + YEAR[x.v] : "")));
  badges.appendChild(el("span", "badge", x.gn));
  if (x.skin) badges.appendChild(el("span", "badge", "Skin tones"));
  right.appendChild(badges);
  const btns = el("div", "btns");
  const cb = el("button", "btn", "Copy " + withTone(x)); cb.addEventListener("click", () => copyEmoji(x, withTone(x), big));
  const fb = el("button", "btn ghost" + (favs.includes(slug) ? " on" : ""), favs.includes(slug) ? "★ Favorited" : "☆ Favorite");
  fb.addEventListener("click", () => { toggleFav(slug); const on = favs.includes(slug); fb.classList.toggle("on", on); fb.textContent = on ? "★ Favorited" : "☆ Favorite"; });
  btns.append(cb, fb); right.appendChild(btns);
  if (x.skin){
    right.appendChild(el("div", "pagesub", "All skin tones (tap to copy):"));
    const tg = el("div", "grid"); tg.style.marginBottom = "16px";
    TONES.forEach((t, i) => { const txt = withTone(x, i); const b = el("button", "e", txt); b.title = x.name + " · " + t[2]; b.setAttribute("aria-label", "Copy " + x.name + ", " + t[2] + " skin tone"); b.addEventListener("click", () => copyEmoji(x, txt, b)); tg.appendChild(b); });
    right.appendChild(tg);
  }
  const tb = el("table", "info");
  const row = (k, v) => { const tr = el("tr"); tr.appendChild(el("th", null, k)); const td = el("td"); if (typeof v === "string") td.textContent = v; else td.appendChild(v); tr.appendChild(td); tb.appendChild(tr); };
  const codes = el("span"); [...withTone(x)].forEach(c => { const cd = el("code", null, "U+" + c.codePointAt(0).toString(16).toUpperCase().padStart(4, "0")); cd.style.marginRight = "6px"; codes.appendChild(cd); });
  row("Codepoints", codes);
  row("Shortcode", ":" + x.slug + ":");
  row("Added", "Emoji " + x.v + (YEAR[x.v] ? " (" + YEAR[x.v] + ")" : ""));
  row("Group", x.gn);
  right.appendChild(tb);
  if (x.kw){
    right.appendChild(el("div", "pagesub", "Keywords")).style.marginTop = "16px";
    const kws = el("div"); [...new Set(x.kw.split(" "))].filter(w => w.length > 1).slice(0, 24).forEach(w => { const b = el("button", "kw", w); b.addEventListener("click", () => location.hash = "#/search/" + encodeURIComponent(w)); kws.appendChild(b); });
    right.appendChild(kws);
  }
  d.appendChild(right); app.appendChild(d);
  const i = ALL.indexOf(x); const near = ALL.filter(y => y.g === x.g && y !== x).sort((a, b) => Math.abs(ALL.indexOf(a) - i) - Math.abs(ALL.indexOf(b) - i)).slice(0, 24);
  app.appendChild(sec("Similar emojis", null, grid(near, true)));
}

/* ---- router ---- */
function route(){
  const h = location.hash.replace(/^#\/?/, ""); const app = $("#app"); app.innerHTML = ""; let key = "home";
  if (h.startsWith("search/")) pageHome(app, decodeURIComponent(h.slice(7)));
  else if (h.startsWith("g/")){ key = "all"; pageGroup(app, h.slice(2)); }
  else if (h.startsWith("e/")){ key = ""; pageEmoji(app, decodeURIComponent(h.slice(2))); }
  else if (h === "emotions" || h.startsWith("emotions/")){ key = "emotions"; pageEmotions(app, h.startsWith("emotions/") ? h.slice(9) : null); }
  else if (h === "egyptian/hieroglyphs"){ key = "egyptian"; pageHieroglyphs(app); }
  else if (h === "egyptian" || h.startsWith("egyptian/")){ key = "egyptian"; pageEgyptian(app, h.startsWith("egyptian/") ? h.slice(9) : null); }
  else if (h === "letters"){ key = "letters"; pageLetters(app); }
  else if (h === "saved"){ key = "favorites"; pageFavs(app); }
  else if (h === "playground" || h.startsWith("playground/")){ key = "playground"; pagePlayground(app, h.startsWith("playground/") ? h.slice(11) : null); }
  else if (h === "substack" || h.startsWith("substack/")){ key = "substack"; pageSubstack(app, h.startsWith("substack/") ? h.slice(9) : null); }
  else if (h === "symbols" || h.startsWith("symbols/")){ key = "symbols"; pageSymbols(app, h.startsWith("symbols/") ? h.slice(8) : null); }
  else if (h === "combos" || h.startsWith("combos/")){ key = "combos"; pageCombos(app, h.startsWith("combos/") ? h.slice(7) : null); }
  else if (h === "new"){ key = "new"; pageNew(app); }
  else if (h === "all"){ key = "all"; pageAll(app); }
  else if (h === "favorites"){ key = "favorites"; pageFavs(app); }
  else pageHome(app);
  document.querySelectorAll("#nav a").forEach(a => a.classList.toggle("on", a.dataset.r === key));
  window.scrollTo(0, 0);
}
$("#miniq").addEventListener("keydown", e => { if (e.key === "Enter"){ const v = e.target.value.trim(); location.hash = v ? "#/search/" + encodeURIComponent(v) : "#/"; e.target.value = ""; e.target.blur(); } });
window.addEventListener("hashchange", route);
/* first render waits until every script (including the Playground) has loaded */
if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", route); else setTimeout(route, 0);
