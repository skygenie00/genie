/* _task_ox_claude_answers 하네스 — 브라우저 안 도우미.
   ★ 누름은 playwright 가 **진짜 터치**로 한다(touchscreen.tap · 크롬 끌기는 CDP 터치). 여기서는 자리를 재고 상태를 읽는다.
   ⚠ BASE(846dc1e)에는 Claude 함수가 없다 — 있는지부터 보고 없으면 null 을 돌려 헛잣대로 쓴다. */
window.onload = null;   /* 앱 초기화(망·동기화)를 끈다 — 시험이 저장소·문항을 직접 싣는다 */
(function () {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const H = window.__HZ = window.__HZ || {};
  const LS = k => localStorage.getItem(k);
  const txt = n => (n ? n.textContent : '').replace(/\s+/g, ' ').trim();
  const cs = el => el ? getComputedStyle(el) : null;
  const HAS = () => typeof clLoad === 'function';
  function at(el, fx, fy) {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    const x = r.left + r.width * (fx == null ? 0.5 : fx), y = r.top + r.height * (fy == null ? 0.5 : fy);
    const on = r.width > 0 && r.height > 0 && x >= 0 && y >= 0 && x < innerWidth && y < innerHeight;
    const top = on ? document.elementFromPoint(x, y) : null;
    return { cx: Math.round(x * 10) / 10, cy: Math.round(y * 10) / 10, w: Math.round(r.width * 10) / 10, h: Math.round(r.height * 10) / 10, on: on,
             hit: !!(top && (top === el || el.contains(top))), top: top ? (top.id ? '#' + top.id : top.tagName) : null };
  }
  function btnInfo(b) {
    if (!b) return null;
    const s = cs(b), kids = [...b.children];
    return { text: txt(b), tag: b.tagName, hidden: b.hidden, color: s.color, fs: s.fontSize, fw: s.fontWeight, bd: s.borderTopWidth + ' ' + s.borderTopStyle,
             bg: s.backgroundColor, title: b.getAttribute('title'), at: at(b),
             kids: kids.map(k => ({ t: txt(k), color: cs(k).color, fs: cs(k).fontSize, fw: cs(k).fontWeight, bg: cs(k).backgroundColor })) };
  }
  window.__HZT = {
    /* ── 준비: 기록.json 저장소 전부 · 문항 5,548 · 토큰 있음/없음 */
    setup: async function (token) {
      const R = {};
      const rec = await (await fetch('/rec.json')).json();
      const D = rec.data || rec;
      H.recText = JSON.stringify(rec);
      localStorage.clear();
      const BASE = { 'ox_uid_migrated': '1', 'ox_gg_okreset': '1', 'ox_auto_important_v2': '1' };
      for (const k in BASE) localStorage.setItem(k, BASE[k]);
      for (const k in D) localStorage.setItem(k, typeof D[k] === 'string' ? D[k] : JSON.stringify(D[k]));
      localStorage.setItem('tt.cfg', JSON.stringify({ person: '하네스', token: token ? 'github_pat_HARNESS' : '' }));
      try { useIdxDrop(); } catch (e) { }
      const M = await (await fetch('/master.json')).json();
      quizData.length = 0; buildQuizData(M.rows).forEach(q => quizData.push(q));
      R.q = quizData.length;
      R.has = HAS();
      R.syncKeys = (typeof SYNC_KEYS !== 'undefined') ? SYNC_KEYS.slice() : null;
      R.fix0 = LS('ox_cl_fix');
      return JSON.stringify(R);
    },
    recText: function () { return H.recText; },
    /* §A-2 받기 — 앱의 clLoad 를 그대로 부른다(SEED 의 fetch 가 claude.json 길만 대답) */
    load: async function () {
      if (!HAS()) return JSON.stringify({ base: true });
      await clLoad();
      return JSON.stringify({ state: CL_STATE, by: CL_BY_UID, ment: CL_MENT, status: txt(document.getElementById('sync-status')),
                              statusCls: (document.getElementById('sync-status') || {}).className || '', err: (window.__ERR || []).slice() });
    },
    status: function () { return JSON.stringify({ text: txt(document.getElementById('sync-status')), state: HAS() ? CL_STATE : null }); },
    clearStatus: function () { const e = document.getElementById('sync-status'); if (e) e.textContent = ''; return true; },
    /* §B 카드 — 그 문항이 있는 쪽으로 가서 카드 아랫줄의 Claude 단추 */
    card: async function (uid) {
      document.querySelectorAll('.oxwin').forEach(w => w.remove());
      jumpFromSearch(uid); await wait(500);
      const box = document.getElementById('q-box-' + uid);
      if (!box) return JSON.stringify({ card: false });
      box.scrollIntoView({ block: 'center' }); await wait(150);
      const b = box.querySelector('[data-clbtn="' + uid + '"]:not([data-clpop])');
      const lnk = [...box.querySelectorAll('button')].find(x => txt(x) === '✏️ 연결');
      return JSON.stringify({ card: true, btn: btnInfo(b), next: b && b.nextElementSibling ? txt(b.nextElementSibling) : null,
                              lnk: lnk ? { at: at(lnk), fs: cs(lnk).fontSize } : null, n: box.querySelectorAll('[data-clbtn]').length });
    },
    /* §B 문항 팝업 — 「✏️ 연결」(qpLinkToggle) 바로 앞 */
    pop: async function (uid) {
      document.querySelectorAll('.oxwin').forEach(w => w.remove());
      openQPopup(uid); await wait(250);
      const w = document.getElementById('oxwin-q-' + uid);
      if (!w) return JSON.stringify({ pop: false });
      const b = w.querySelector('[data-clbtn="' + uid + '"][data-clpop="1"]');
      const lnk = [...w.querySelectorAll('button')].find(x => /qpLinkToggle/.test(x.getAttribute('onclick') || ''));
      return JSON.stringify({ pop: true, btn: btnInfo(b), nextIsLink: !!(b && b.nextElementSibling === lnk), lnk: lnk ? { at: at(lnk), fs: cs(lnk).fontSize } : null });
    },
    /* §B-3 Claude 창 */
    win: function (uid) {
      const w = document.getElementById('oxwin-cl-' + uid);
      if (!w) return JSON.stringify({ win: false });
      const bd = w.querySelector('.oxwin-body'), c = bd && bd.querySelector('[data-clwin]');
      const ans = c ? [...c.querySelectorAll('[data-clans]')] : [];
      const a0 = ans[0];
      const head = a0 ? a0.firstElementChild : null;
      return JSON.stringify({
        win: true, grip: !!w.querySelector('.oxwin-grip'), title: txt(w.querySelector('.oxwin-head')), z: +w.style.zIndex || 0,
        rect: (r => [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)])(w.getBoundingClientRect()),
        note: c ? txt(c.querySelector(':scope > div:not([data-clans])')) : null, answers: ans.map(a => a.getAttribute('data-clans')),
        head: head ? [...head.children].map(x => txt(x)) : null,
        headUidBtn: head ? !!head.querySelector('button.uid') : null,
        h4: a0 ? [...a0.querySelectorAll('h4')].map(txt) : [], tables: a0 ? a0.querySelectorAll('table').length : 0,
        th: a0 ? a0.querySelectorAll('th').length : 0, td: a0 ? a0.querySelectorAll('td').length : 0, li: a0 ? a0.querySelectorAll('li').length : 0,
        ul: a0 ? cs(a0.querySelector('ul') || a0).listStyleType : null,
        uidBtns: a0 ? [...a0.querySelectorAll('[data-clmdbox] button.uid')].map(txt) : [],
        bold: a0 ? a0.querySelectorAll('[data-clmdbox] b').length : 0,
        core: a0 ? txt(a0.querySelector('.clcore')) : null, fixtag: a0 ? txt(a0.querySelector('.clfixtag')) : null,
        fixBtn: a0 ? txt(a0.querySelector('.clfixbar')) : null, ta: !!(a0 && a0.querySelector('[data-clfixta]')),
        msg: a0 ? txt(a0.querySelector('[data-clfixmsg]')) : null,
        rawTags: a0 ? /<(script|img|iframe)/i.test(a0.innerHTML) : null
      });
    },
    winBtn: function (uid, sel, text) {
      const w = document.getElementById('oxwin-cl-' + uid);
      const b = w ? [...w.querySelectorAll(sel)].find(x => !text || txt(x) === text) : null;
      if (b) b.scrollIntoView({ block: 'nearest' });
      return JSON.stringify(at(b));
    },
    winPart: function (uid, part) {
      const w = document.getElementById('oxwin-cl-' + uid);
      const e = w ? (part === 'head' ? w.querySelector('.oxwin-head > div') : w.querySelector('.oxwin-grip')) : null;
      return JSON.stringify(at(e, part === 'grip' ? 0.6 : 0.3, 0.5));
    },
    size: function () { return LS('oxwin.size.claude'); },
    sizeJn: function () { return LS('oxwin.size.jn'); },
    hasWin: function (key) { return !!document.getElementById('oxwin-' + key); },
    setTa: function (uid, mode) {
      const w = document.getElementById('oxwin-cl-' + uid), ta = w && w.querySelector('[data-clfixta]');
      if (!ta) return JSON.stringify(null);
      H.ta0 = ta.value;
      ta.value = mode === 'long' ? 'ㄱ'.repeat(20001) : ta.value + '\n\n- 하네스정정줄 시험';
      return JSON.stringify({ len: ta.value.length, orig: H.ta0.length });
    },
    fix: function () { return LS('ox_cl_fix'); },
    /* §C-1 근거 검색 */
    search: function (term) {
      document.getElementById('search-input').value = term;
      setSearchMode('m');
      const box = document.getElementById('search-results');
      const rows = [...box.querySelectorAll(':scope > button')].map(b => ({
        id: (txt(b.querySelector('span')) || '').replace('ID ', ''),
        badges: [...b.querySelectorAll('.clsrc')].map(txt),
        blue: !!b.querySelector('.bg-blue-50, [style*="#fff5f5"]'),
        cl: !!b.querySelector('[style*="#fff7ed"]'), clText: txt(b.querySelector('[style*="#fff7ed"]'))
      }));
      return JSON.stringify({ count: txt(document.getElementById('search-count')), rows: rows });
    },
    /* §C-2 단원 목록 */
    dist: async function () {
      document.querySelectorAll('.oxwin').forEach(w => w.remove());
      goHome(); await wait(300);                 /* 단원 목록은 첫 화면의 검색 칸 아래에 뜬다 — 문제풀이 화면이면 크기 0 */
      document.getElementById('search-input').value = '';
      setSearchMode('m');
      showFieldDistribution('m');
      const hd = document.querySelector('#search-results [data-ggfield="dist"]');
      if (hd) hd.scrollIntoView({ block: 'center' });
      await wait(150);
      return window.__HZT.distState();
    },
    distState: function () {
      const box = document.getElementById('search-results');
      const hd = box.querySelector('[data-ggfield="dist"]');
      const cb = hd ? hd.querySelector('.ggclhd') : null, bb = hd ? hd.querySelector('.ggbanghd') : null;
      const units = [...box.querySelectorAll(':scope > button')].map(b => ({ k: txt(b.querySelector('span')), chips: [...b.querySelectorAll('span span')].map(txt) }));
      return JSON.stringify({ head: txt(hd), headBg: hd ? cs(hd).backgroundColor : null, headColor: hd ? cs(hd).color : null,
                              cBtn: cb ? { t: txt(cb), off: cb.classList.contains('off'), color: cs(cb).color, bb: cs(cb).borderBottomStyle, at: at(cb) } : null,
                              bangBtn: bb ? { t: txt(bb), at: at(bb) } : null, units: units.length,
                              clUnits: units.filter(u => u.chips.some(c => /^C\d+$/.test(c))).map(u => u.k + ' ' + u.chips.join(',')),
                              first: units.slice(0, 3), flags: [typeof GG_BANG_ONLY !== 'undefined' ? GG_BANG_ONLY : null, typeof GG_CL_ONLY !== 'undefined' ? GG_CL_ONLY : null] });
    },
    toggles: function () {
      const R = {};
      if (typeof ggClOnlyToggle !== 'function') return JSON.stringify({ base: true });
      GG_BANG_ONLY = false; GG_CL_ONLY = false; showFieldDistribution('m');
      ggBangOnlyToggle(); R.afterBang = [GG_BANG_ONLY, GG_CL_ONLY];
      ggClOnlyToggle(); R.afterBangThenC = [GG_BANG_ONLY, GG_CL_ONLY];
      ggBangOnlyToggle(); R.afterCThenBang = [GG_BANG_ONLY, GG_CL_ONLY];
      GG_BANG_ONLY = false; GG_CL_ONLY = false; showFieldDistribution('m');
      setSearchMode('q'); R.q = [GG_BANG_ONLY, GG_CL_ONLY];
      GG_CL_ONLY = true; setSearchMode('q'); R.qOff = [GG_BANG_ONLY, GG_CL_ONLY];
      setSearchMode('m');
      return JSON.stringify(R);
    },
    /* §C-3 문항 목록 */
    list: function (unitKey, clOnly) {
      if (typeof GG_CL_ONLY !== 'undefined') { GG_CL_ONLY = !!clOnly; GG_BANG_ONLY = false; }
      showFieldDistribution('m');
      const gi = _fieldGroups.indexOf(unitKey);
      if (gi < 0) return JSON.stringify({ gi: -1, groups: _fieldGroups.length });
      showFieldList('m', gi);
      const box = document.getElementById('search-results');
      const rows = [...box.querySelectorAll(':scope > button')].filter(b => /ID Q/.test(txt(b)));
      const row = u => rows.find(b => txt(b.querySelector('span')) === 'ID ' + u);
      const r0 = row('Q0480');
      const R = { gi: gi, head: txt(box.querySelector(':scope > div')), rows: rows.length,
                  q0480: r0 ? { blue: !!r0.querySelector('.bg-blue-50'), cl: txt(r0.querySelector('[style*="#fff7ed"]')),
                                clStyle: (b => b ? [cs(b).backgroundColor, cs(b).color, cs(b).borderLeftColor] : null)(r0.querySelector('[style*="#fff7ed"]')) } : null,
                  clBoxes: rows.filter(b => b.querySelector('[style*="#fff7ed"]')).length };
      if (typeof GG_CL_ONLY !== 'undefined') { GG_CL_ONLY = false; }
      return JSON.stringify(R);
    },
    /* §D 정리 창 — 첫 화면 📋 단추(민법총칙 · 4) */
    jnBtn: async function () {
      document.querySelectorAll('.oxwin').forEach(w => w.remove());
      goHome(); await wait(200);
      renderDashboard(); await wait(200);
      const b = [...document.querySelectorAll('button[data-jn]')].find(x => /openJeongni\('민법총칙','4'/.test(x.getAttribute('onclick') || ''));
      if (!b) return JSON.stringify(null);
      b.scrollIntoView({ block: 'center' }); await wait(150);
      return JSON.stringify(at(b));
    },
    jnState: function () {
      const w = [...document.querySelectorAll('.oxwin')].find(x => /^oxwin-jn-/.test(x.id));
      if (!w) return JSON.stringify({ jn: false });
      const rows = [...w.querySelectorAll('[data-jnrow]')];
      const vis = r => [...r.querySelectorAll('[data-clchip]')].filter(c => !c.hidden && c.tagName === 'BUTTON');
      const r0 = rows.find(r => r.getAttribute('data-jnrow') === 'Q0480');
      const ans = r0 ? [...r0.querySelectorAll(':scope > button')].find(b => /정답·해설/.test(txt(b))) : null;
      const chip = r0 ? vis(r0)[0] : null;
      return JSON.stringify({ jn: true, id: w.id, sub: txt(w.querySelector('.oxwin-head')), rows: rows.length,
                              withChip: rows.filter(r => vis(r).length).map(r => r.getAttribute('data-jnrow') + ' ' + vis(r).map(txt).join(',')),
                              placeholders: rows.filter(r => r.querySelector('[data-clchip][hidden]')).length,
                              q0480: r0 ? { chip: chip ? txt(chip) : null, chipAfterAns: !!(chip && ans && chip.previousElementSibling === ans),
                                            chipStyle: chip ? [cs(chip).color, cs(chip).fontSize, cs(chip).fontWeight, cs(chip).borderTopWidth, cs(chip).backgroundColor] : null,
                                            ansHidden: (b => b ? b.classList.contains('hide') : null)(r0.querySelector('[data-jnans]')), ansText: ans ? txt(ans) : null } : null });
    },
    jnPart: function (uid, what) {
      const w = [...document.querySelectorAll('.oxwin')].find(x => /^oxwin-jn-/.test(x.id));
      const r = w && w.querySelector('[data-jnrow="' + uid + '"]');
      if (!r) return JSON.stringify(null);
      const el = what === 'ans' ? [...r.querySelectorAll(':scope > button')].find(b => /정답·해설/.test(txt(b))) : [...r.querySelectorAll('[data-clchip]')].find(c => !c.hidden);
      if (el) el.scrollIntoView({ block: 'center' });
      return JSON.stringify(at(el));
    },
    /* §E G16 — 가짜 원격 기록(SEED 의 __REMOTE) */
    remoteSet: function (text, sha) { window.__REMOTE = { text: text, sha: sha, puts: 0 }; return true; },
    remoteGet: function () { return JSON.stringify(window.__REMOTE || null); },
    fixPut: function (md) { const a = JSON.parse(LS('ox_cl_fix') || '{}'); a.M001 = { md: md, ts: Date.now(), done: false }; lsPut('ox_cl_fix', a); return true; },
    stamp: function () { return stampAll(); },
    sync: async function (force) { await syncRecords(!!force); return JSON.stringify({ tie: typeof recTie !== 'undefined' ? recTie : null, fail: typeof recFail !== 'undefined' ? recFail : null, remote: window.__REMOTE && { sha: window.__REMOTE.sha, puts: window.__REMOTE.puts } }); },
    ls: function (k) { return LS(k); },
    tagToggle: function () { const t = JSON.parse(LS('ox_q_tags') || '{}'); t.Q0706 = Object.assign({}, t.Q0706 || {}, { important: !(t.Q0706 && t.Q0706.important) }); localStorage.setItem('ox_q_tags', JSON.stringify(t)); return true; },
    /* G17 — 이 쪽 스크립트 블록을 하나씩 파서에 넣는다(실행하지 않는다 · node 가 없어 브라우저 파서로 대신) */
    parse: function () {
      const out = [];
      [...document.scripts].forEach((s, i) => {
        if (s.src) return;
        try { new Function(s.textContent); out.push([i, s.textContent.length, 'ok']); } catch (e) { out.push([i, s.textContent.length, String(e && e.message || e)]); }
      });
      return JSON.stringify(out);
    },
    errs: function () { return JSON.stringify(window.__ERR || []); },
    visibleClBtns: function () { return [...document.querySelectorAll('[data-clbtn]')].filter(b => b.tagName === 'BUTTON' && !b.hidden).length; },
    allClBtns: function () { return document.querySelectorAll('[data-clbtn]').length; }
  };
})();
