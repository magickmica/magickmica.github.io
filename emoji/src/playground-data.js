/* Magick Mica Emoji Playground: data only (no UI logic here).
   Every emoji here is looked up in the site's main emoji dataset (emoji-data.js),
   so names and accessible labels come from there. Add a category by adding an entry. */

/* Emoji Shuffler categories. "pool" lists emoji characters; "groups" pulls whole
   groups from the main dataset (by group slug), minus anything in "skip". */
const SHUFFLE_CATEGORIES = [
  {id:"everything", name:"Everything", icon:"✨", blurb:"a little bit of all the magic",
   pool:"🌙 🦋 🍓 💎 🌈 🪄 🐈 ✨ 🪐 🍄 💖 🧚 🌸 ☀️ 🦄 🔮 🫧 ⭐ 🍒 🪷 🛸 🧁 🌊 🪻", includeAll:true},
  {id:"cosmic", name:"Cosmic", icon:"🪐", blurb:"moons, planets and stardust",
   pool:"🌙 🪐 ⭐ 🌌 ☄️ 🛸 👽 🌟 🔭 🌞 🌠 💫 🌕 🌖 🌗 🌘 🌑 🌒 🌓 🌔 🌛 🌜 🌝 🚀 🛰️ 👾 ✨ 🌍 🌏 🌎 🌚"},
  {id:"love", name:"Love & Hearts", icon:"💖", blurb:"crushes, kisses and every heart",
   pool:"💖 💕 💗 💘 💝 ❤️ 💞 💓 😘 🌹 🥰 💌 😍 😻 💋 💟 ❣️ 🩷 🧡 💛 💚 🩵 💙 💜 🤍 🫶 🥂 🍫 💐 🧸 💍 👩‍❤️‍👨 💑 ❤️‍🔥"},
  {id:"nature", name:"Nature & Flowers", icon:"🌸", blurb:"blooms, leaves, sea and sky",
   pool:"🌸 🌻 🍄 🌿 🦋 🌈 🌊 🌷 🍓 🌳 🐝 🌼 🌺 🌹 🪷 🪻 💐 🌱 🍀 🍃 🍂 🍁 🌵 🌴 🌲 🪴 🐞 🐌 🐚 🪸 🌾 ☀️ 🌦️ 🪺"},
  {id:"magic", name:"Magic & Fantasy", icon:"🪄", blurb:"wands, fairies and crystal balls",
   pool:"🪄 🔮 🧚 ✨ 🦄 🪷 💎 🫧 🪞 🪽 🧿 🌟 🧙 🧜 🐉 🏰 👑 🗝️ 🕯️ 🍄 🌙 ⭐ 🪬 🃏 🧞 🐲 🦢 🌈 💫 🧝"},
  {id:"cute", name:"Cute & Kawaii", icon:"🎀", blurb:"soft, sweet and squishy",
   pool:"🎀 🧸 🐰 🐱 🐶 🐻 🐼 🐹 🐥 🦊 🍓 🧁 🍡 🍭 🌸 💗 🫧 🩰 🦢 🐣 🍰 🍬 🌷 🐾 🥺 🥹 ☁️ 🐨 🦔"},
  {id:"sweets", name:"Sweets & Treats", icon:"🧁", blurb:"dessert for your posts",
   pool:"🧁 🍰 🎂 🍩 🍪 🍫 🍬 🍭 🍮 🍯 🍦 🍨 🍧 🥧 🍡 🍓 🍒 🍑 🍉 🍇 🫐 🥐 🧇 🥞 ☕ 🧋 🍵 🍹"},
  {id:"y2k", name:"Y2K & Retro", icon:"💿", blurb:"discs, pagers and disco balls",
   pool:"💿 📀 📼 📺 📟 📱 💾 🖥️ 🕹️ 👾 🪩 🦋 💖 ⭐ 🌈 💅 👛 🕶️ 🎧 📸 ☎️ 💽 🛼 🔮 ✨ 💎"},
  {id:"faces", name:"Happy Faces", icon:"😊", blurb:"smiles and good moods",
   pool:"😊 😁 😄 😆 🥰 😍 🤩 😎 🥳 😇 🤗 😋 😌 😺 🙂 ☺️ 😸 🤭 😉 😚 🫶 🙌 👏 🌞"}
];

/* Every other tool in the Playground. status "live" = built and working;
   "soon" = shown as a Coming soon card (never presented as working). */
const PLAYGROUND_TOOLS = [
  {id:"shuffler", name:"Emoji Shuffler", icon:"🎲", blurb:"Shuffle a mix, lock the ones you love, copy it.", status:"live"},
  {id:"mood", name:"Mood Generator", icon:"💭", blurb:"Pick a mood. Find your emojis.", status:"soon"},
  {id:"aesthetic", name:"Aesthetic Generator", icon:"🌈", blurb:"Y2K, fairycore, cosmic and more.", status:"soon"},
  {id:"dice", name:"Emoji Dice", icon:"🎯", blurb:"Roll up to three emoji dice.", status:"soon"},
  {id:"fortune", name:"Fortune Teller", icon:"🔮", blurb:"A tiny surprise from the emoji universe.", status:"soon"},
  {id:"combo", name:"Combo Maker", icon:"🧩", blurb:"Build, reorder and copy your own sequence.", status:"soon"},
  {id:"decorator", name:"Sentence Decorator", icon:"✍️", blurb:"Add the right emojis to your own words.", status:"soon"},
  {id:"story", name:"Story Machine", icon:"📖", blurb:"Emoji sequences that start a story.", status:"soon"}
];

const SHUFFLE_COUNTS = [3, 5, 6, 10];
