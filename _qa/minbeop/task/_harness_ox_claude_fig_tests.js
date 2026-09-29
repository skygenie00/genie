/* _task_ox_claude_fig 하네스 — 브라우저 안 도구(__HZT). 누름은 playwright 진짜 터치 · 여기서는 자리·상태·계산 스타일만.
   ⚠ BASE(7b9e214)에는 그림 함수가 없다 — typeof 로 가른다(헛잣대). 준비는 앞 판 하네스와 같다(onload 끔 · 기록·문항 직접 싣기). */
window.onload = null;
(function () {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const LS = k => localStorage.getItem(k);
  const txt = n => (n ? n.textContent : '').replace(/\s+/g, ' ').trim();
  const cs = el => el ? getComputedStyle(el) : null;
  const HASFIG = () => typeof clFigLoad === 'function';
  function at(el, fx, fy) {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    const x = r.left + r.width * (fx == null ? 0.5 : fx), y = r.top + r.height * (fy == null ? 0.5 : fy);
    const on = r.width > 0 && r.height > 0 && x >= 0 && y >= 0 && x < innerWidth && y < innerHeight;
    const top = on ? document.elementFromPoint(x, y) : null;
    return { cx: Math.round(x * 10) / 10, cy: Math.round(y * 10) / 10, w: Math.round(r.width * 10) / 10, h: Math.round(r.height * 10) / 10, on: on,
             hit: !!(top && (top === el || el.contains(top))), top: top ? (top.id ? '#' + top.id : top.tagName) : null };
  }
  async function until(f, ms) { const t0 = Date.now(); while (Date.now() - t0 < (ms || 6000)) { try { if (f()) return true; } catch (e) { } await wait(40); } return false; }
  function figInfo(fr) {
    if (!fr) return null;
    let doc = null; try { doc = fr.contentDocument; } catch (e) { }
    const de = doc && doc.documentElement;
    const st = cs(fr);
    return { sandbox: fr.getAttribute('sandbox'), h: Math.round(fr.getBoundingClientRect().height * 10) / 10, w: Math.round(fr.getBoundingClientRect().width * 10) / 10,
      docH: de ? de.scrollHeight : null, clientH: fr.clientHeight, clientW: fr.clientWidth, scrollW: de ? de.scrollWidth : null,
      overflowY: de ? de.scrollHeight - fr.clientHeight : null, overflowX: de ? de.scrollWidth - fr.clientWidth : null,
      border: st.borderTopWidth, radius: st.borderTopLeftRadius, disp: st.display, title: doc ? doc.title : null,
      svg: doc ? doc.querySelectorAll('svg').length : null, scripts: doc ? doc.querySelectorAll('script').length : null,
      bodyMargin: doc && doc.body ? cs(doc.body).margin : null };
  }
  window.__HZT = {
    setup: async function (token) {
      const R = {};
      const rec = await (await fetch('/rec.json')).json();
      const D = rec.data || rec;
      localStorage.clear();
      const BASE = { 'ox_uid_migrated': '1', 'ox_gg_okreset': '1', 'ox_auto_important_v2': '1' };
      for (const k in BASE) localStorage.setItem(k, BASE[k]);
      for (const k in D) localStorage.setItem(k, typeof D[k] === 'string' ? D[k] : JSON.stringify(D[k]));
      localStorage.setItem('tt.cfg', JSON.stringify({ person: '하네스', token: token ? 'github_pat_HARNESS' : '' }));
      try { useIdxDrop(); } catch (e) { }
      const M = await (await fetch('/master.json')).json();
      quizData.length = 0; buildQuizData(M.rows).forEach(q => quizData.push(q));
      R.q = quizData.length; R.hasFig = HASFIG();
      R.syncKeys = (typeof SYNC_KEYS !== 'undefined') ? SYNC_KEYS.slice() : null;
      R.lsKeys = Object.keys(localStorage).sort();
      return JSON.stringify(R);
    },
    load: async function () {
      await clLoad();
      return JSON.stringify({ state: CL_STATE, by: CL_BY_UID, ment: CL_MENT, figs: Object.keys(CL_DATA.answers).map(m => [m, CL_DATA.answers[m].fig || null]),
                              figGets: window.__FIGGETS, clGets: window.__CLGETS, cache: HASFIG() ? Object.keys(CL_FIG) : null });
    },
    gets: function () { return JSON.stringify({ fig: window.__FIGGETS, cl: window.__CLGETS, figUrls: window.__FIGURLS || [] }); },
    body: function () { const s = cs(document.body); return JSON.stringify({ margin: s.margin, font: s.fontFamily, fs: s.fontSize, bg: s.backgroundColor, lh: s.lineHeight }); },
    card: async function (uid) {
      document.querySelectorAll('.oxwin').forEach(w => w.remove());
      jumpFromSearch(uid); await wait(500);
      const box = document.getElementById('q-box-' + uid);
      if (!box) return JSON.stringify({ card: false });
      box.scrollIntoView({ block: 'center' }); await wait(150);
      const b = box.querySelector('[data-clbtn="' + uid + '"]:not([data-clpop])');
      return JSON.stringify({ card: true, text: txt(b), at: at(b) });
    },
    closeWins: function () { document.querySelectorAll('.oxwin').forEach(w => w.remove()); return true; },
    waitFig: async function (uid) {
      const w = () => document.getElementById('oxwin-cl-' + uid);
      const ok = await until(() => { const fr = w() && w().querySelector('[data-clfig] iframe'); return fr && fr.getBoundingClientRect().height > 50; }, 8000);
      await wait(300);
      return ok;
    },
    win: function (uid) {
      const w = document.getElementById('oxwin-cl-' + uid);
      if (!w) return JSON.stringify({ win: false });
      const c = w.querySelector('[data-clwin]');
      const ans = c ? [...c.querySelectorAll('[data-clans]')] : [];
      const out = { win: true, rect: (r => [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)])(w.getBoundingClientRect()),
        answers: ans.map(a => a.getAttribute('data-clans')), html: c ? c.innerHTML : null, a: [] };
      ans.forEach(a => {
        const kids = [...a.children].map(k => k.hasAttribute('data-clfig') ? 'FIG' : k.hasAttribute('data-clmdbox') ? 'MD' : k.classList.contains('clcore') ? 'CORE'
          : k.classList.contains('clfixbar') ? 'BAR' : k.classList.contains('clfixtag') ? 'TAG' : (k === a.firstElementChild ? 'HEAD' : k.tagName));
        const fc = a.querySelector(':scope > [data-clfig]'), fr = fc && fc.querySelector('iframe'), big = fc && fc.querySelector('button');
        let bigPos = null;
        if (big && fc) { const rb = big.getBoundingClientRect(), rc2 = fc.getBoundingClientRect(); bigPos = [Math.round(rc2.right - rb.right), Math.round(rb.top - rc2.top)]; }
        out.a.push({ m: a.getAttribute('data-clans'), order: kids, fig: !!fc, figNote: fc && !fr ? txt(fc) : null,
          figNoteStyle: fc && !fr && fc.firstElementChild ? [cs(fc.firstElementChild).fontSize, cs(fc.firstElementChild).color] : null,
          frame: figInfo(fr), big: big ? { t: txt(big), fs: cs(big).fontSize, fw: cs(big).fontWeight, color: cs(big).color, bd: cs(big).borderTopWidth, bg: cs(big).backgroundColor, pos: bigPos, at: at(big) } : null,
          figMb: fc ? cs(fc).marginBottom : null, md: txt(a.querySelector('[data-clmdbox]')).slice(0, 40), ta: !!a.querySelector('[data-clfixta]'),
          taHasFig: (() => { const t = a.querySelector('[data-clfixta]'); return t ? /<svg|<iframe|claude_fig|srcdoc/i.test(t.value) : null; })() });
      });
      return JSON.stringify(out);
    },
    frameRef: function (uid) { const w = document.getElementById('oxwin-cl-' + uid); window.__FRREF = w ? w.querySelector('[data-clfig] iframe') : null; return !!window.__FRREF; },
    sameFrame: function (uid) { const w = document.getElementById('oxwin-cl-' + uid); const fr = w ? w.querySelector('[data-clfig] iframe') : null; return JSON.stringify({ same: !!fr && fr === window.__FRREF, connected: !!(window.__FRREF && window.__FRREF.isConnected) }); },
    winBtn: function (uid, sel, text) {
      const w = document.getElementById('oxwin-' + uid);
      const b = w ? [...w.querySelectorAll(sel)].find(x => !text || txt(x) === text) : null;
      if (b) b.scrollIntoView({ block: 'nearest' });
      return JSON.stringify(at(b));
    },
    winPart: function (key, part) {
      const w = document.getElementById('oxwin-' + key);
      const e = w ? (part === 'head' ? w.querySelector('.oxwin-head > div') : w.querySelector('.oxwin-grip')) : null;
      return JSON.stringify(at(e, part === 'grip' ? 0.6 : 0.3, 0.5));
    },
    toTop: function (key) { const w = document.getElementById('oxwin-' + key); if (w) { w.style.top = '8px'; w.style.left = '20px'; } return !!w; },
    big: function (m) {
      const w = document.getElementById('oxwin-clfig-' + m);
      if (!w) return JSON.stringify({ win: false });
      const fr = w.querySelector('[data-clfigbig] iframe');
      return JSON.stringify({ win: true, rect: (r => [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)])(w.getBoundingClientRect()),
        head: txt(w.querySelector('.oxwin-head')), grip: !!w.querySelector('.oxwin-grip'), frame: figInfo(fr) });
    },
    sizes: function () { return JSON.stringify({ claude: LS('oxwin.size.claude'), clfig: LS('oxwin.size.clfig') }); },
    setTa: function (uid, mode) {
      const w = document.getElementById('oxwin-cl-' + uid), t = w && w.querySelector('[data-clfixta]');
      if (!t) return JSON.stringify(null);
      if (mode === 'add') t.value = t.value + '\n\n- 하네스정정줄';
      return JSON.stringify({ len: t.value.length, hasFig: /<svg|<iframe|claude_fig|srcdoc/i.test(t.value) });
    },
    fix: function () { return LS('ox_cl_fix'); },
    evil: function () { return JSON.stringify({ ran: window.__FIGRAN || null, ran2: window.__FIGRAN2 || null, ran3: window.__FIGRAN3 || null }); },
    parse: function () {
      const out = [];
      [...document.scripts].forEach((s, i) => {
        if (s.src) return;
        try { new Function(s.textContent); out.push([i, s.textContent.length, 'ok']); } catch (e) { out.push([i, s.textContent.length, String(e && e.message || e)]); }
      });
      return JSON.stringify(out);
    },
    errs: function () { return JSON.stringify((window.__ERR || []).filter(e => !/^ResizeObserver loop/.test(e))); },
    ro: function () { return (window.__ERR || []).filter(e => /^ResizeObserver loop/.test(e)).length; }
  };
})();
