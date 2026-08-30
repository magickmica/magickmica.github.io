/* ============================================================
   MAGICKMICA · COLLECT NOTES
   ------------------------------------------------------------
   HOW TO RUN
   1. In Chrome, go to:  https://substack.com/@magickmica/notes
      (make sure you are LOGGED IN)
   2. Press F12  ->  Console tab
   3. Type the words:  allow pasting     then press Enter
      (Chrome makes you do this once per session)
   4. Paste this whole file, press Enter
   5. Wait. It prints progress. A file called notes_refresh.json
      will download automatically when it finishes.

   It walks backwards through your notes newest-first and stops
   once it reaches CUTOFF. Overlap is fine and safe -- duplicates
   are removed later by note id, so a generous cutoff costs
   nothing but a few extra seconds.
   ============================================================ */
(async () => {
  'use strict';

  const CUTOFF   = '2026-07-15';  // go back at least this far (safe overlap)
  const MAX_PAGE = 400;           // hard stop so it can never spin forever
  const PAUSE_MS = 350;           // be polite to the API

  const sleep = ms => new Promise(r => setTimeout(r, ms));

  // ---- find the logged-in user id -------------------------------
  let uid = null;
  try {
    const me = await fetch('/api/v1/user/me', { credentials: 'include' }).then(r => r.json());
    uid = me?.id || me?.user_id || null;
  } catch (e) { /* fall through */ }
  if (!uid) uid = 89688032;  // magickmica fallback
  console.log('%c[collect] user id: ' + uid, 'color:#ff9be4');

  // ---- page through the profile note feed ------------------------
  const items = [];
  const seen  = new Set();
  let cursor = null, page = 0, oldest = null, done = false;

  while (!done && page < MAX_PAGE) {
    page++;
    let url = `/api/v1/reader/feed/profile/${uid}?types%5B%5D=note&limit=50`;
    if (cursor != null) url += `&cursor=${encodeURIComponent(cursor)}`;

    let data;
    try {
      const res = await fetch(url, { credentials: 'include' });
      if (!res.ok) { console.warn('[collect] HTTP ' + res.status + ' - stopping'); break; }
      data = await res.json();
    } catch (err) {
      console.warn('[collect] fetch failed, stopping:', err);
      break;
    }

    const batch = data.items || data.notes || data.comments || [];
    if (!batch.length) { console.log('[collect] empty page - done'); break; }

    for (const it of batch) {
      const c  = it.comment || it;
      const id = c.id ?? it.entity_key ?? null;
      if (id == null || seen.has(String(id))) continue;
      seen.add(String(id));
      items.push(it);
      const d = (c.date || c.created_at || '').slice(0, 10);
      if (d) {
        if (!oldest || d < oldest) oldest = d;
        if (d < CUTOFF) done = true;
      }
    }

    cursor = data.nextCursor ?? data.next_cursor ?? null;
    console.log(`[collect] page ${page} · ${items.length} notes · back to ${oldest || '?'}`);
    if (cursor == null) { console.log('[collect] no more pages'); break; }
    await sleep(PAUSE_MS);
  }

  // ---- hand back a file -----------------------------------------
  const json = JSON.stringify(items, null, 0);
  console.log(`%c[collect] DONE — ${items.length} notes, oldest ${oldest}`,
              'color:#7bf1e4;font-weight:bold');

  const blob = new Blob([json], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'notes_refresh.json';
  document.body.appendChild(a);
  a.click();
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 4000);

  try {
    await navigator.clipboard.writeText(json);
    console.log('[collect] also copied to clipboard');
  } catch (e) {
    console.log('[collect] clipboard blocked — use the downloaded file');
  }

  window.__notes = items;   // also left here if you want to poke at it
})();
