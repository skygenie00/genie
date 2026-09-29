/* _task_jo_claude_answers §J 하네스 — 쪽 안에서 재는 도구(__HZT). 앱 끝 </body> 앞에 붙는다(앱 본체 스크립트 뒤).
   ⚠ 누르기는 파이썬이 진짜 터치로 한다 — 여기서는 자리(rc)·상태·계산 스타일만 잰다. BASE(f8cec7a)에는 새 함수가 없으므로 typeof 로 가른다. */
(function () {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const rc = e => {
    if (!e) return null;
    const r = e.getBoundingClientRect();
    return { x: r.left, y: r.top, w: r.width, h: r.height, cx: r.left + r.width / 2, cy: r.top + r.height / 2,
      on: r.width > 0 && r.height > 0 && r.top >= 0 && r.left >= 0 && r.bottom <= innerHeight && r.right <= innerWidth };
  };
  const txt = e => e ? String(e.textContent || '').replace(/\s+/g, ' ').trim() : null;
  const cs = (e, p) => e ? getComputedStyle(e)[p] : null;
  const has = n => { try { return typeof eval(n) !== 'undefined'; } catch (e) { return false; } };
  async function idle() { for (let i = 0; i < 400 && busy; i++) await wait(25); }
  async function rr() { await idle(); await render(); await idle(); await wait(80); }   /* render 끝의 setTimeout(scrBack,0) 이 스크롤을 되돌린 뒤에 잰다 */
  async function until(f, ms) { const t0 = Date.now(); while (Date.now() - t0 < (ms || 8000)) { try { if (f()) return true; } catch (e) { } await wait(40); } return false; }
  const popBy = k => (POPS || []).find(x => x._pk === k) || null;
  const T = { K: 'TR01053', M1: 'TR01051', M2: 'TR01054' };
  let OTHER = null, PLAIN = null;

  async function home() {
    closeAllPops();
    S.law = '특허법'; S.tab = 'jimun'; S.jimunTab = 'ox'; S.mok = ''; S.oxQueue = '';
    await rr();
    await until(() => OXPOOL && Object.keys(OXPOOL).length > 1000 && MBK2M && Object.keys(MBK2M).length > 1000 && MBSR && MBSR.box && MBSR.box.isConnected, 20000);
    await wait(80);
  }
  function lab(k) { return (MBK2M[k] || {}).label || ''; }

  window.__HZT = {
    errs() { return (window.__ERR || []).filter(e => !/^ResizeObserver loop/.test(e)).slice(0, 20); },
    roCount() { return (window.__ERR || []).filter(e => /^ResizeObserver loop/.test(e)).length; },
    toasts() { return (window.__TOASTS || []).slice(); },   /* SEED 가 모은 것 전부(토스트는 2.4초 뒤 사라진다) */
    async boot() {
      await home();
      if (has('CL_STATE')) await until(() => CL_STATE !== 'wait' || !syncToken(), 8000);
      const q = (VJ.byId || {})['2001-38-5'];
      const sameQ = q ? (q.지문 || []).map(z => z.uid) : [];
      PLAIN = sameQ.find(u => u && [T.K, T.M1, T.M2].indexOf(u) < 0) || null;
      const L0 = lab(T.K);
      OTHER = Object.keys(OXPOOL).find(k => MBK2M[k] && lab(k) !== L0 && !/^8\./.test(lab(k))) || null;
      const labels = {}; [T.K, T.M1, T.M2].forEach(k => { labels[k] = lab(k); });
      return { labels: labels, pool: Object.keys(OXPOOL).length, k2m: Object.keys(MBK2M).length, cl: has('CL_STATE') ? CL_STATE : '(없음)',
        by: has('CL_BY_UID') ? CL_BY_UID : null, ment: has('CL_MENT') ? CL_MENT : null, syncKeys: SYNC_KEYS.length,
        syncKeyTail: SYNC_KEYS.slice(-3), label: L0, sameQ: sameQ, plain: PLAIN, other: OTHER, otherLabel: lab(OTHER), law: S.law,
        tokenAtBoot: !!syncToken(), toasts: this.toasts() };
    },
    /* 근거 셋(켜짐 둘) · 형광펜 하나 — BASE·NEW 같은 값 */
    seed() {
      const now = Date.now();
      const G = {};
      G[T.K] = [{ k: 'gH1', i: 1, t: '제130조 — 침해 추정 규정 (하네스 근거)', ok: null, ts: now, cs: [] }];
      G[T.M1] = [{ k: 'gH2', i: 1, t: '하네스 근거 — 켜짐', ok: null, ts: now, cs: [], bang: 1 }];
      if (OTHER) G[OTHER] = [{ k: 'gH3', i: 1, t: '하네스 근거 — 다른 단원 켜짐', ok: null, ts: now, cs: [], bang: 1 }];
      localStorage.setItem('jopangi.gg', JSON.stringify(G)); GGREC = null;
      const t = ggText(T.K);
      mkPut(mkcKey(T.K, 'q', 0, 6, 'y', t.slice(0, 6)), {});
      return { gg: Object.keys(G), mark: t.slice(0, 6) };
    },
    async card(uid) {
      closeAllPops();
      const sel = '#slot [data-ggu="' + uid + '"]';
      if (!document.querySelector(sel)) { linkGo(uid); await until(() => document.querySelector(sel), 15000); await idle(); await wait(250); }
      const box = document.querySelector(sel);
      if (!box) return { card: false, mok: S.mok };
      const row = box.parentElement;
      row.scrollIntoView({ block: 'center' }); await wait(200);
      const b = row.querySelector(':scope > .mbbot [data-clbtn]');
      const lnk = row.querySelector(':scope > .mbbot .mblink');
      const btn = b ? { tag: b.tagName, text: txt(b), color: cs(b, 'color'), fs: cs(b, 'fontSize'), fw: cs(b, 'fontWeight'),
        bd: cs(b, 'borderTopWidth') + ' ' + cs(b, 'borderTopStyle'), bg: cs(b, 'backgroundColor'), hidden: b.hidden, title: b.title, at: rc(b),
        kids: [...b.children].map(k => ({ tag: k.tagName, t: txt(k), color: cs(k, 'color'), fs: cs(k, 'fontSize'), fw: cs(k, 'fontWeight'), bg: cs(k, 'backgroundColor') })) } : null;
      return { card: true, mok: S.mok, btn: btn, next: b && b.nextElementSibling ? txt(b.nextElementSibling) : null,
        lnk: lnk ? { t: txt(lnk), at: rc(lnk) } : null, n: row.querySelectorAll('[data-clbtn]').length,
        visBtns: [...document.querySelectorAll('#slot .mbcl')].filter(x => !x.hidden && x.offsetParent).length,
        allBtns: document.querySelectorAll('#slot [data-clbtn]').length, mbbots: document.querySelectorAll('#slot .mbbot').length };
    },
    win(uid) {
      const p = popBy('claude|' + uid);
      if (!p) return { win: false, pops: (POPS || []).map(x => x._pk) };
      const ph = p.querySelector('.ph'), pt = ph && ph.querySelector('.pt'), x = ph && ph.querySelector(':scope > button');
      const w = p.querySelector('[data-clwin]'), r = p.getBoundingClientRect(), tb = w && w.querySelector('table');
      const u0 = w && w.querySelector('[data-clmdbox] button.uid');
      return { win: true, mbwin: p.classList.contains('mbwin'), title: txt(pt), close: txt(x),
        closeStyle: x ? [cs(x, 'fontSize'), cs(x, 'fontWeight'), cs(x, 'color'), cs(x, 'borderTopWidth'), cs(x, 'borderTopColor'), cs(x, 'borderTopLeftRadius'), cs(x, 'backgroundColor')] : null,
        headBg: cs(ph, 'backgroundColor'), headPad: cs(ph, 'padding'), headLine: cs(ph, 'borderBottomWidth') + ' ' + cs(ph, 'borderBottomColor'),
        drag: cs(ph && ph.querySelector('.pdrag'), 'display'), titleStyle: [cs(pt, 'fontSize'), cs(pt, 'fontWeight'), cs(pt, 'color')],
        popStyle: [cs(p, 'borderTopWidth'), cs(p, 'borderTopColor'), cs(p, 'borderTopLeftRadius'), cs(p, 'boxShadow')], font: cs(p, 'fontFamily'),
        rect: [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)], grip: !!p.querySelector('.prsz'), sized: p.classList.contains('sized'),
        bodyStyle: w ? [cs(w, 'fontSize'), cs(w, 'lineHeight'), cs(w, 'backgroundColor'), cs(w, 'paddingTop'), cs(w, 'paddingLeft')] : null,
        note: w ? txt(w.querySelector('.clnote')) : null, answers: w ? [...w.querySelectorAll('[data-clans]')].map(a => a.dataset.clans) : [],
        head: w ? [...w.querySelectorAll('.clhd')].map(h => [...h.children].map(txt)) : [],
        headUid: w ? [...w.querySelectorAll('.clhd button.uid')].map(b => [b.dataset.sid, cs(b, 'marginLeft')]) : [],
        h4: w ? [...w.querySelectorAll('h4')].map(txt) : [], tables: w ? w.querySelectorAll('table').length : 0, th: w ? w.querySelectorAll('th').length : 0,
        tdFs: cs(tb, 'fontSize'), thBg: cs(w && w.querySelector('th'), 'backgroundColor'), tdLine: cs(w && w.querySelector('td'), 'borderTopColor'),
        li: w ? w.querySelectorAll('li').length : 0, bold: w ? w.querySelectorAll('[data-clmdbox] b').length : 0,
        uidBtns: w ? [...w.querySelectorAll('[data-clmdbox] button.uid')].map(b => b.dataset.sid) : [],
        uidStyle: u0 ? [cs(u0, 'fontSize'), cs(u0, 'fontWeight'), cs(u0, 'color'), cs(u0, 'textDecorationStyle'), cs(u0, 'borderTopWidth'), cs(u0, 'backgroundColor')] : null,
        core: txt(w && w.querySelector('.clcore')), coreStyle: (w && w.querySelector('.clcore')) ? [cs(w.querySelector('.clcore'), 'backgroundColor'), cs(w.querySelector('.clcore'), 'borderTopLeftRadius'), cs(w.querySelector('.clcore'), 'fontWeight'), cs(w.querySelector('.clcore'), 'color'), cs(w.querySelector('.clcore'), 'borderLeftWidth')] : null,
        fixBtn: txt(w && w.querySelector('.clfixbar button')), bar: w ? [...w.querySelectorAll('.clfixbar button')].map(txt) : [],
        fixtag: txt(w && w.querySelector('.clfixtag')), ta: !!(w && w.querySelector('[data-clfixta]')),
        taStyle: (w && w.querySelector('[data-clfixta]')) ? [cs(w.querySelector('[data-clfixta]'), 'minHeight'), cs(w.querySelector('[data-clfixta]'), 'fontSize'), cs(w.querySelector('[data-clfixta]'), 'borderTopColor')] : null,
        coreAfterTa: !!(w && w.querySelector('[data-clmdbox] [data-clfixta]') && w.querySelector('[data-clmdbox]').nextElementSibling && w.querySelector('[data-clmdbox]').nextElementSibling.classList.contains('clcore')),
        msg: txt(w && w.querySelector('.clfixmsg')), rawTags: w ? /\*\*|###|\|---/.test(w.textContent) : null,
        cfg: (S.popCfg || {}).claude || null };
    },
    winPart(uid, part) {
      const p = popBy('claude|' + uid); if (!p) return null;
      if (part === 'head') { const pt = p.querySelector('.ph .pt'); const r = rc(pt); return r ? Object.assign(r, { cx: r.x + Math.min(40, r.w / 3) }) : null; }
      if (part === 'grip') { const g = p.querySelector('.prsz'); return rc(g); }
      return null;
    },
    winBtn(uid, sel, t) {
      const p = popBy('claude|' + uid); if (!p) return null;
      const b = [...p.querySelectorAll(sel)].find(x => txt(x) === t || x.dataset.sid === t);
      if (!b) return null;
      b.scrollIntoView({ block: 'center' });
      return rc(b);
    },
    cardBtnAt(uid) { const b = document.querySelector('#slot [data-ggu="' + uid + '"]'); const r = b && b.parentElement.querySelector(':scope > .mbbot [data-clbtn]'); if (r) r.scrollIntoView({ block: 'center' }); return rc(r); },
    setTa(uid, mode) {
      const p = popBy('claude|' + uid), ta = p && p.querySelector('[data-clfixta]');
      if (!ta) return null;
      if (mode === 'add') ta.value = ta.value + '\n\n- 하네스정정줄';
      else if (mode === 'long') ta.value = 'x'.repeat(20001);
      ta.dispatchEvent(new Event('input', { bubbles: true }));
      return { len: ta.value.length };
    },
    fix() { return localStorage.getItem('jopangi.clfix'); },
    /* §E 새 지문 팝업 */
    pop(k) {
      const p = popBy('q|📝 지문 ' + k);
      if (!p) return { pop: false, pops: (POPS || []).map(x => x._pk) };
      const w = p.querySelector('.qp2'), r = p.getBoundingClientRect();
      if (!w) return { pop: true, old: true, ox: p.querySelectorAll('.mboxb').length, title: txt(p.querySelector('.ph .pt')), go: txt(p.querySelector('.pb > .tool')) };
      const b = w.querySelector('.qptx b'), cb = w.querySelector('.qpbar [data-clbtn]'), ans = w.querySelector('.qpans');
      return { pop: true, mbwin: p.classList.contains('mbwin'), width: Math.round(r.width), title: txt(p.querySelector('.ph .pt')), close: txt(p.querySelector('.ph > button')),
        headBg: cs(p.querySelector('.ph'), 'backgroundColor'), font: cs(p, 'fontFamily'),
        chips: [...w.querySelectorAll('.qpchips > span')].map(s => [txt(s), cs(s, 'color'), cs(s, 'backgroundColor'), cs(s, 'fontSize'), cs(s, 'borderTopWidth'), cs(s, 'borderTopLeftRadius')]),
        num: b ? [txt(b), cs(b, 'color'), cs(b, 'fontWeight')] : null, txStyle: [cs(w.querySelector('.qptx'), 'fontSize'), cs(w.querySelector('.qptx'), 'lineHeight')],
        gg: !!w.querySelector('.ggbox[data-ggu="' + k + '"]'), ox: p.querySelectorAll('.mboxb').length,
        ansHidden: ans ? ans.hidden : null, ansVisible: ans ? ans.offsetParent !== null : null, ans: txt(w.querySelector('.qpa')), ansColor: cs(w.querySelector('.qpa b'), 'color'),
        sol: (txt(w.querySelector('.qpe')) || '').slice(0, 40),
        bar: [...w.querySelectorAll('.qpbar > *')].map(e => txt(e)), cl: cb ? [txt(cb), cs(cb, 'color'), cs(cb, 'fontSize')] : null,
        barLine: cs(w.querySelector('.qpbar'), 'borderTopStyle') + ' ' + cs(w.querySelector('.qpbar'), 'borderTopColor') };
    },
    popBtn(k, t) {
      const p = popBy('q|📝 지문 ' + k); if (!p) return null;
      const b = [...p.querySelectorAll('.qpbar > button')].find(x => txt(x).indexOf(t) === 0);
      if (!b) return null;
      b.scrollIntoView({ block: 'center' });
      return rc(b);
    },
    where(k) { return { mok: S.mok, pops: (POPS || []).map(x => x._pk), card: !!document.querySelector('#slot [data-ggu="' + k + '"]'), label: lab(k), tab: S.tab }; },
    oldPop() {
      closeAllPops(); popJo('특허법', '제130조', null, 1);
      const p = POPS[POPS.length - 1]; if (!p) return null;
      const ph = p.querySelector('.ph');
      return { mbwin: p.classList.contains('mbwin'), headBg: cs(ph, 'backgroundColor'), btn: txt(ph.querySelector(':scope > button')), drag: cs(ph.querySelector('.pdrag'), 'display'),
        border: cs(p, 'borderTopWidth') + ' ' + cs(p, 'borderTopColor'), title: txt(ph.querySelector('.pt')) };
    },
    /* §G 근거 단원 목록 */
    async gmode(q) {
      await home();
      S.oxQMode = 'g'; S.oxQ = q || ''; await rr();
      await until(() => MBSR && MBSR.cnt && (q ? MBSR.cnt.textContent : /근거|^$/.test(MBSR.cnt.textContent)), 3000);
      await wait(250);
      return this.cnt();
    },
    cnt() {
      const c = MBSR && MBSR.cnt;
      if (c) c.scrollIntoView({ block: 'center' });
      return { cnt: txt(c), lk: !!(c && c.classList.contains('gglk')), style: [cs(c, 'color'), cs(c, 'fontWeight'), cs(c, 'textDecorationLine'), cs(c, 'fontSize')], at: rc(c),
        want: has('ggFieldKeys') ? ggFieldKeys().length : null };
    },
    dist() {
      const box = MBSR && MBSR.box; if (!box) return null;
      const hd = box.querySelector('.gfhd'), b = hd && hd.querySelector('.ggbanghd'), c = hd && hd.querySelector('.ggclhd'), bk = hd && hd.querySelector('.gfbk');
      return { hidden: box.classList.contains('hide'), head: txt(hd), headBg: cs(hd, 'backgroundColor'), headFs: cs(hd, 'fontSize'), headFw: cs(hd, 'fontWeight'),
        bang: b ? { t: txt(b), color: cs(b, 'color'), bb: cs(b, 'borderBottomStyle'), off: b.classList.contains('off'), at: rc(b) } : null,
        c: c ? { t: txt(c), color: cs(c, 'color'), bb: cs(c, 'borderBottomStyle'), off: c.classList.contains('off'), at: rc(c) } : null,
        back: bk ? { t: txt(bk), at: rc(bk) } : null,
        units: [...box.querySelectorAll('.gfur')].map(r => ({ l: txt(r.querySelector('.gfl')), pills: [...r.querySelectorAll('.gfpill')].map(p => [txt(p), cs(p, 'color')]), at: rc(r) })),
        flags: has('GG_BANG_ONLY') ? [GG_BANG_ONLY, GG_CL_ONLY] : null,
        list: box.querySelector('.gfback') ? { back: txt(box.querySelector('.gfback')), ut: txt(box.querySelector('.gfut')),
          rows: [...box.querySelectorAll('.gfir')].map(r => ({ k: r.dataset.ggk, id: txt(r.querySelector('.gfid')), no: txt(r.querySelector('.gfno')),
            boxes: [...r.querySelectorAll('.gfbx')].map(x => [x.className, txt(x).slice(0, 60), cs(x, 'backgroundColor'), cs(x, 'borderLeftColor')]), at: rc(r) })) } : null };
    },
    unitAt(i) { const r = MBSR.box.querySelectorAll('.gfur')[i]; if (r) r.scrollIntoView({ block: 'center' }); return rc(r); },
    unitIdx(label) { return [...MBSR.box.querySelectorAll('.gfur')].findIndex(r => txt(r.querySelector('.gfl')) === label); },
    listRowAt(k) { const r = MBSR.box.querySelector('.gfir[data-ggk="' + k + '"]'); if (r) r.scrollIntoView({ block: 'center' }); return rc(r); },
    toggles() {
      if (!has('ggDist')) return null;
      GG_BANG_ONLY = false; GG_CL_ONLY = false; ggDist();
      const hd = () => MBSR.box.querySelector('.gfhd');
      const bangSpan = hd().querySelector('.ggbanghd'), cSpan = hd().querySelector('.ggclhd');
      const out = {};
      cSpan.onclick(); out.afterC = [GG_BANG_ONLY, GG_CL_ONLY];
      bangSpan.onclick(); out.afterCThenBang = [GG_BANG_ONLY, GG_CL_ONLY];
      cSpan.onclick(); out.afterBangThenC = [GG_BANG_ONLY, GG_CL_ONLY];
      GG_BANG_ONLY = false; GG_CL_ONLY = false; ggDist();
      return out;
    },
    mqAt() { const b = [...document.querySelectorAll('.mbsr .mbsb')].find(x => txt(x) === '📄 문제'); if (b) b.scrollIntoView({ block: 'center' }); return rc(b); },
    flags() { return has('GG_BANG_ONLY') ? [GG_BANG_ONLY, GG_CL_ONLY, S.oxQMode] : [null, null, S.oxQMode]; },
    async search(term) {
      await home();
      S.oxQMode = 'g'; S.oxQ = ''; await rr(); await wait(100);
      MBSR.inp.value = term; MBSR.inp.dispatchEvent(new Event('input', { bubbles: true }));
      await wait(400);
      return { count: txt(MBSR.cnt), rows: [...MBSR.box.querySelectorAll('.rr')].map(r => ({ name: txt(r.querySelector('.m')), badges: [...r.querySelectorAll('.srcb')].map(txt),
        snip: txt(r.querySelector('.clsnip')), snipStyle: r.querySelector('.clsnip') ? [cs(r.querySelector('.clsnip'), 'backgroundColor'), cs(r.querySelector('.clsnip'), 'borderLeftColor')] : null })) };
    },
    /* §H 정리 창 — TR01053 이 든 묶음의 📋 */
    async jnBtn(uid) {
      await home(); S.oxQMode = 'q'; S.oxQ = ''; await rr();
      const L0 = lab(uid || T.K), rows = [...document.querySelectorAll('#slot .mbur')];
      const i = rows.findIndex(r => txt(r.querySelector('.nm')) === L0);
      if (i < 0) return { found: false, label: L0 };
      let j = i; while (j >= 0 && !rows[j].querySelector('.mbchip.jn')) j--;
      if (j < 0) return { found: false, label: L0, i: i };
      const b = rows[j].querySelector('.mbchip.jn');
      b.scrollIntoView({ block: 'center' }); await wait(200);
      return Object.assign(rc(b), { found: true, label: L0, head: txt(rows[j].querySelector('.nm')), title: b.title });
    },
    jnState() {
      const p = (POPS || []).find(x => /^q\|📋 정리 · /.test(x._pk || ''));
      if (!p) return { jn: false, pops: (POPS || []).map(x => x._pk) };
      const rows = [...p.querySelectorAll('.jnr')], row = p.querySelector('.jnr[data-jnrow="' + T.K + '"]');
      const chipOf = r => r.querySelector(':scope > button[data-clchip]');
      const c = row && chipOf(row), pk = row && row.querySelector(':scope > .jnpk'), ans = row && row.querySelector(':scope > [data-jnans]');
      return { jn: true, mbwin: p.classList.contains('mbwin'), title: txt(p.querySelector('.ph .pt')), sub: txt(p.querySelector('.ph .mbps')), close: txt(p.querySelector('.ph > button')),
        bands: [...p.querySelectorAll('.jnh2')].map(txt), bandStyle: p.querySelector('.jnh2') ? [cs(p.querySelector('.jnh2'), 'fontSize'), cs(p.querySelector('.jnh2'), 'fontWeight'), cs(p.querySelector('.jnh2'), 'color'), cs(p.querySelector('.jnh2'), 'backgroundColor')] : null,
        rows: rows.length, pk: p.querySelectorAll('.jnr > .jnpk').length, oldRows: p.querySelectorAll('.jnrow').length, ox: p.querySelectorAll('.mboxb').length,
        withChip: rows.filter(r => chipOf(r)).map(r => r.dataset.jnrow + ' ' + txt(chipOf(r))),
        placeholders: rows.filter(r => r.querySelector(':scope > span[data-clchip][hidden]')).length,
        t603: row ? { chip: txt(c), chipAfterPk: !!(c && c.previousElementSibling === pk), chipStyle: c ? [cs(c, 'color'), cs(c, 'fontSize'), cs(c, 'fontWeight'), cs(c, 'borderTopWidth'), cs(c, 'backgroundColor'), cs(c, 'marginLeft')] : null,
          pk: txt(pk), pkStyle: pk ? [cs(pk, 'fontSize'), cs(pk, 'fontWeight'), cs(pk, 'color'), cs(pk, 'backgroundColor'), cs(pk, 'borderTopColor')] : null,
          ansHidden: ans ? ans.hidden : null, ansVisible: ans ? ans.offsetParent !== null : null, ans: txt(ans && ans.querySelector('.jna')),
          mark: row.querySelectorAll('.jnqq mark.mkc').length, markText: txt(row.querySelector('.jnqq mark.mkc')), gg: txt(row.querySelector('.jngg')),
          ggStyle: row.querySelector('.jngg') ? [cs(row.querySelector('.jngg'), 'backgroundColor'), cs(row.querySelector('.jngg'), 'borderLeftColor')] : null,
          no: txt(row.querySelector('.jnno')), rec: txt(row.querySelector('.jnrec')), qqStyle: [cs(row.querySelector('.jnqq'), 'fontSize'), cs(row.querySelector('.jnqq'), 'lineHeight')] } : null,
        oldT603: (() => { const o = [...p.querySelectorAll('.jnrow')].find(r => /2001년 5번\(3\)/.test(txt(r.querySelector('.go')) || '')); return o ? { mark: o.querySelectorAll('.qq mark.mkc').length, gl: o.querySelectorAll('.gl').length } : null; })() };
    },
    jnPart(uid, which) {
      const p = (POPS || []).find(x => /^q\|📋 정리 · /.test(x._pk || '')); if (!p) return null;
      const row = p.querySelector('.jnr[data-jnrow="' + uid + '"]'); if (!row) return null;
      const b = which === 'chip' ? row.querySelector(':scope > button[data-clchip]') : which === 'no' ? row.querySelector('.jnno') : row.querySelector(':scope > .jnpk');
      if (!b) return null;
      b.scrollIntoView({ block: 'center' });
      return rc(b);
    },
    jnChips() {
      const p = (POPS || []).find(x => /^q\|📋 정리 · /.test(x._pk || '')); if (!p) return null;
      return { rows: p.querySelectorAll('.jnr').length, bands: [...p.querySelectorAll('.jnh2')].map(txt),
        withChip: [...p.querySelectorAll('.jnr')].filter(r => r.querySelector(':scope > button[data-clchip]')).map(r => r.dataset.jnrow + ' ' + txt(r.querySelector(':scope > button[data-clchip]'))),
        has: [T.K, T.M1, T.M2].filter(k => p.querySelector('.jnr[data-jnrow="' + k + '"]')) };
    },
    jnRowState(uid) {
      const p = (POPS || []).find(x => /^q\|📋 정리 · /.test(x._pk || '')); if (!p) return null;
      const row = p.querySelector('.jnr[data-jnrow="' + uid + '"]'); if (!row) return null;
      const ans = row.querySelector(':scope > [data-jnans]'), pk = row.querySelector(':scope > .jnpk');
      return { ansHidden: ans.hidden, ansVisible: ans.offsetParent !== null, pk: txt(pk), ans: txt(ans.querySelector('.jna')) };
    },
    /* §A-2 · J17 · J18 */
    load() { return { state: has('CL_STATE') ? CL_STATE : null, by: has('CL_BY_UID') ? CL_BY_UID : null, ment: has('CL_MENT') ? CL_MENT : null, toasts: this.toasts(), gets: window.__CLGETS }; },
    async reload() { await clLoad(); await wait(100); return this.load(); },
    rx() {
      if (!has('CL_RX')) return null;
      const s = 'T901 T001 S001 D001 TR01053 T0946093r SR02011 D1234567 T013860 TR010531 xTR01053';
      const html = clMdHTML('T901 참고 · TR01053 · T0946093r');
      return { match: s.match(CL_RX), btns: (html.match(/data-sid="[^"]+"/g) || []) };
    },
    /* J19 — 기록 동기화(메모리 원격) */
    remoteSet(t, sha) { window.__REMOTE = { text: t, sha: sha, puts: 0 }; return true; },
    remoteGet() { const R = window.__REMOTE || {}; return JSON.stringify({ text: R.text, sha: R.sha, puts: R.puts }); },
    async sync(force) { await idle(); for (let i = 0; i < 200 && recBusy; i++) await wait(25); await syncRecords(!!force); for (let i = 0; i < 400 && recBusy; i++) await wait(25); return { err: recLastErr, puts: (window.__REMOTE || {}).puts }; },
    stamp() { return stampAll(); },
    fixPut(md) { lsWrite('jopangi.clfix', { T901: { md: md, ts: Date.now(), done: false } }, 'Claude 답 정정'); return localStorage.getItem('jopangi.clfix'); },
    tagToggle() { oxTagToggle(T.K, 'important'); return JSON.stringify((oxOf(T.K) || {}).tg || {}); },
    ls(k) { return localStorage.getItem(k); },
    /* J21 — 이 쪽에 실린 스크립트 블록을 이 엔진 파서로 */
    async parse() {
      const src = await (await fetch(location.href.split('#')[0].split('?')[0], { cache: 'no-store' })).text();
      const out = []; const rx = /<script>([\s\S]*?)<\/script>/g; let m, i = 0;
      while ((m = rx.exec(src))) { let ok = 'ok'; try { new Function(m[1]); } catch (e) { ok = String(e && e.message || e).slice(0, 120); } out.push([i++, m[1].length, ok]); }
      return out;
    }
  };
})();
