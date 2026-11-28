/* Substack category: script letters, writing, journals, reading, podcasting, newsletter bits */
const _cp = n => String.fromCodePoint(n);
function _math(U, L, D, ex){ ex = ex || {}; return ch => {
  if (ex[ch]) return ex[ch];
  const c = ch.charCodeAt(0);
  if (c >= 65 && c <= 90 && U != null) return _cp(U + c - 65);
  if (c >= 97 && c <= 122 && L != null) return _cp(L + c - 97);
  if (c >= 48 && c <= 57 && D != null) return _cp(D + c - 48);
  return ch; }; }
const _small = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ";
const _up = base => ch => { const u = ch.toUpperCase().charCodeAt(0); return u >= 65 && u <= 90 ? _cp(base + u - 65) : ch; };
const SCRIPT_STYLES = [
 {n:"Bold Script", f:_math(0x1D4D0,0x1D4EA)},
 {n:"Script", f:_math(0x1D49C,0x1D4B6,null,{B:"ℬ",E:"ℰ",F:"ℱ",H:"ℋ",I:"ℐ",L:"ℒ",M:"ℳ",R:"ℛ",e:"ℯ",g:"ℊ",o:"ℴ"})},
 {n:"Gothic", f:_math(0x1D504,0x1D51E,null,{C:"ℭ",H:"ℌ",I:"ℑ",R:"ℜ",Z:"ℨ"})},
 {n:"Bold Gothic", f:_math(0x1D56C,0x1D586)},
 {n:"Bold", f:_math(0x1D400,0x1D41A,0x1D7CE)},
 {n:"Italic", f:_math(0x1D434,0x1D44E,null,{h:"ℎ"})},
 {n:"Bold Italic", f:_math(0x1D468,0x1D482)},
 {n:"Sans Bold", f:_math(0x1D5D4,0x1D5EE,0x1D7EC)},
 {n:"Sans Italic", f:_math(0x1D608,0x1D622)},
 {n:"Typewriter", f:_math(0x1D670,0x1D68A,0x1D7F6)},
 {n:"Outline", f:_math(0x1D538,0x1D552,0x1D7D8,{C:"ℂ",H:"ℍ",N:"ℕ",P:"ℙ",Q:"ℚ",R:"ℝ",Z:"ℤ"})},
 {n:"Small Caps", f:ch => { const u = ch.toUpperCase().charCodeAt(0); return u >= 65 && u <= 90 ? _small[u-65] : ch; }},
 {n:"Bubble", f:_math(0x24B6,0x24D0)},
 {n:"Dark Bubble", f:_up(0x1F150)},
 {n:"Squares", f:_up(0x1F130)},
 {n:"Wide", f:_math(0xFF21,0xFF41,0xFF10)},
 {n:"Struck", f:ch => /\s/.test(ch) ? ch : ch + "̶"},
 {n:"Underline", f:ch => ch + "̲"},
 {n:"Sparkle", f:ch => /\s/.test(ch) ? " " : ch + "⋆"}
];
const scriptText = (s, st) => Array.from(s).map(st.f).join("");

const SUB_SETS = [
 {s:"script", n:"Script letters", i:"𝒜", d:"fancy letters for titles, names and headers"},
 {s:"writing", n:"Writing", i:"✍️", d:"drafts, posts, pens and ideas", e:"✍️ 🖋️ ✒️ 📝 🖊️ ✏️ 📜 💭 🗒️ 📃 📄 ⌨️ 💻 💡 🪶 📎 🧠 🗯️",
  t:["✍️ new post","🖋️ ⋆ ⋆ ⋆","📝 drafts ✨","✒️ — ⋆ — ✒️","💭 ✍️ 📝","🪶 ⋆˚࿔","⌨️ ☕ ✨","📜 ✒️ ⋆˚","✍︎ ⋆｡°✩","✎﹏ notes","💡 idea:","📝 ⋆ writing in progress ⋆","🖋️ words by me","✍️ 1,000 words today","🗒️ ⋆˚✿˖° first draft","✏️ ⋆ edit ⋆ ✂️","☕ + ✍️ = ✨","💭 thinking out loud"]},
 {s:"journals", n:"Journals", i:"📓", d:"diaries, planners and cute notes", e:"📓 📔 📒 📕 📗 📘 📙 🗓️ 📅 📆 🖍️ ✂️ 📎 📌 🏷️ 🎀 🌸 🧷 🗂️",
  t:["📓 dear diary ⋆˚","📔 🌸 ✍️","🗓️ ⋆ today ⋆","📒 ꒰ა ♡ ໒꒱","✂️ 📎 🎀","☕ 📓 🕯️","⋆˚✿˖° journal °˖✿˚⋆","📌 to-do: ☐ ☐ ☑","☐ ","☑ ","☒ ","✓ done","🎀 ୨୧ 📔 ୨୧ 🎀","🌙 ⋆ night pages ⋆ 📓","🗓️ week in review","📅 ⋆ monthly reset ⋆","🖍️ doodles & notes","🌱 gratitude list:","♡ three good things ♡","📓 mood: 😊"]},
 {s:"reading", n:"Reading", i:"📚", d:"books, book clubs and ratings", e:"📚 📖 🔖 📕 📗 📘 📙 🤓 👓 ☕ 🕯️ 🛋️ 🌙 🏛️ 📰 🗞️",
  t:["📚 currently reading","📖 ☕ 🕯️","🔖 ⋆ chapter one","🤓📚","★★★★★","★★★★☆","★★★☆☆","⭐⭐⭐⭐⭐","📖 ⋆｡°✩ book club ✩°｡⋆","🌙 📖 💤","📚 TBR pile","🔖 ⋆ quote of the day ⋆","❝ ❞","“ … ”","📕 → 📗 → 📘","🛋️ 📖 ☕ cozy read","📚 ⋆ what I read this month ⋆","👓 ⋆˚ reading list"]},
 {s:"podcasting", n:"Podcasting", i:"🎙️", d:"episodes, live shows and listening", e:"🎙️ 🎧 🎤 📻 🔊 🔴 ▶️ ⏯️ ⏸️ ⏭️ 📡 🎚️ 🎛️ 🗣️ 💬 📢 🎵 🎶",
  t:["🎙️ new episode","🔴 LIVE","🎧 ⋆ now playing ⋆","▶︎ •၊၊||၊|။||||။၊|•","🎙️ ⋆ on air ⋆ 📡","🗣️💬","🎧 ● REC","📻 ⋆˚ listen now","🔊 ▂▃▅▆▇","⏮ ⏯ ⏭","🎙️ EP. 01","🎧 ⋆ out now on all platforms ⋆","🔴 going live in 10 min","🗣️ guest episode ✨","🎙️ ⋆｡°✩ the pod ✩°｡⋆","▶ PLAY","ılıll|̲̅̅●̲̅̅|̲̅̅=̲̅̅|̲̅̅●̲̅̅|llılı","🎶 ⋆ intro music ⋆"]},
 {s:"newsletter", n:"Newsletter bits", i:"💌", d:"headers, calls to action and sign-offs", e:"💌 📬 📩 📨 ✉️ 📰 🗞️ 📣 🔗 🆕 🔒 🎁 🔁 ❤️ 💬",
  t:["💌 subscribe","✨ new post ✨","📬 in your inbox","xoxo ♡","— with love, ✍️","P.S. 💭","💬 leave a comment","❤️ like · 🔁 restack","🔁 restack","📣 announcement","🆓 free post","🔒 for paid subscribers","🎁 gift a subscription","🔗 link below ↓","👇 read more","📰 this week:","⋆｡°✩ thank you for reading ✩°｡⋆","🙏 thanks for being here","💌 see you next week","🗓️ ⋆ weekly digest ⋆","🌟 subscriber of the week","📌 pinned"]},
 {s:"dividers", n:"Post dividers", i:"✦", d:"section breaks for your posts",
  t:["⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆","━━━━━━ ⊱✿⊰ ━━━━━━","✦•┈๑⋅⋯ ⋯⋅๑┈•✦","──── ୨୧ ────","✧ ═════ •❁• ═════ ✧","⋆ ˚｡⋆୨୧˚ ˚୨୧⋆｡˚ ⋆","* ⋆ ✧ ⋆ *","⊱ ────── {.⋅ ✯ ⋅.} ────── ⊰","· · ─────── ·𖥸· ─────── · ·","❦ ❦ ❦","§ § §","✻ ✻ ✻","〰️〰️〰️〰️〰️","┈┈┈┈┈┈┈┈┈┈","⁂","~ ✍️ ~","📖 ━━━━ 📖","🎙️ ━━━━ 🎧"]}
];

function pageSubstack(app, which){
  const x = which ? SUB_SETS.find(y => y.s === which) : null;
  if (which && !x){ app.appendChild(el("p", "empty", "That Substack set isn't here.")); return; }
  if (x){ const back = el("a", "crumb", "← all Substack"); back.href = "#/substack"; app.appendChild(back); }
  app.appendChild(el("h1", "pagetitle", x ? x.i + " " + x.n : "📰 Substack"));
  app.appendChild(el("p", "pagesub", x ? "For your Substack: " + x.d + ". Tap to copy." : "Emojis, symbols and fancy letters for writers, journalers, readers and podcasters. Tap anything to copy it."));
  app.appendChild(setBar(SUB_SETS, "substack", which));
  const show = y => {
    if (y.s === "script") return scriptBlock(!!x);
    const box = el("div");
    if (y.t) box.appendChild(textGrid(x ? y.t : y.t.slice(0, 12), "combo"));
    if (y.e){ const list = [...new Set(y.e.split(" ").map(c => BYCHAR[bare(c)]).filter(Boolean))]; const g = grid(list, !!x); g.style.marginTop = "8px"; box.appendChild(g); }
    return box;
  };
  if (x){ app.appendChild(show(x)); return; }
  SUB_SETS.forEach(y => app.appendChild(sec(y.i + " " + y.n, y.d, show(y), "#/substack/" + y.s, "Open →")));
}
let scriptInput = "Magick Mica";
function scriptBlock(full){
  const box = el("div", "card");
  box.appendChild(el("div", "pagesub", "Type your title or name, then tap a style to copy it:"));
  const inp = el("input"); inp.type = "search"; inp.value = scriptInput; inp.style.width = "100%"; inp.setAttribute("aria-label", "Text to turn into script letters"); box.appendChild(inp);
  const g = el("div", "grid combo script"); g.style.marginTop = "12px"; box.appendChild(g);
  const alpha = el("div"); box.appendChild(alpha);
  const draw = () => { scriptInput = inp.value; g.innerHTML = ""; const raw = inp.value || "Magick Mica";
    (full ? SCRIPT_STYLES : SCRIPT_STYLES.slice(0, 8)).forEach(st => { const t = scriptText(raw, st); const b = textTile(t); b.title = st.n; b.appendChild(el("small", "lbl", st.n)); g.appendChild(b); }); };
  inp.addEventListener("input", draw); draw();
  if (full){
    alpha.appendChild(el("div", "pagesub", "Script alphabets (tap a letter to copy it):")).style.marginTop = "18px";
    SCRIPT_STYLES.slice(0, 4).forEach(st => { alpha.appendChild(el("div", "lbl2", st.n));
      alpha.appendChild(textGrid([..."ABCDEFGHIJKLMNOPQRSTUVWXYZ"].map(st.f), "sym"));
      alpha.appendChild(textGrid([..."abcdefghijklmnopqrstuvwxyz"].map(st.f), "sym")); });
  }
  return box;
}
