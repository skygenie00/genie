/* _task_jo_wonmun 하네스 — 브라우저 안 도구(__WM). 누름은 playwright 진짜 마우스 / CDP 터치(r22) / WebKit 톡 · 여기서는 자리·상태만.
   바탕(앞 인도 판 = jo_cardfix)에는 wmBuild 가 없다 — 본문은 볼트 행 · 창 대신 오른쪽 패널(헛잣대). */
(function () {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const T = n => (n ? n.textContent : '').replace(/\s+/g, ' ').trim();
  const Q = (s, r) => (r || document).querySelector(s);
  const QA = (s, r) => [...(r || document).querySelectorAll(s)];
  function vis(el) { if (!el || !el.isConnected) return false; const s = getComputedStyle(el); if (s.display === 'none' || s.visibility === 'hidden') return false; const r = el.getBoundingClientRect(); return r.height > 0 && r.width > 0; }
  function ptOf(el, noScroll) {
    if (!el) return { on: false, hit: false, why: 'none' };
    let r = el.getBoundingClientRect();
    if (!noScroll && (r.top < 70 || r.bottom > innerHeight - 60 || r.left < 0 || r.right > innerWidth)) { el.scrollIntoView({ block: 'center', inline: 'nearest' }); r = el.getBoundingClientRect(); }
    const x = r.left + Math.min(r.width / 2, 12), y = r.top + r.height / 2;
    const on = r.width > 0 && r.height > 0 && x >= 0 && y >= 0 && x < innerWidth && y < innerHeight;
    const top = on ? document.elementFromPoint(x, y) : null;
    return { cx: Math.round(x * 10) / 10, cy: Math.round(y * 10) / 10, w: Math.round(r.width), h: Math.round(r.height), on: on, hit: !!(top && (top === el || el.contains(top))), top: top ? (top.id ? '#' + top.id : top.tagName + '.' + String(top.className || '').slice(0, 30)) : null, txt: T(el).slice(0, 30) };
  }
  const SKIP = '.lbl,sup,.anchor,.stkanc,.stkchip,.pitflag,.pitwho,.fdmark,.embed,.embx,.blockid,.cdim,.mdmark,.mdhash,.mdtab,.htog';
  function plain(line) { const c = line.cloneNode(true); c.querySelectorAll(SKIP).forEach(x => x.remove()); return c.textContent; }
  /* 글자마다 꾸밈 도장(링크 꼴은 뺀다 — 원문 링크는 점선 글자로 바뀐 것이 뜻) */
  function styleSig(line) {
    const out = [];
    const w = document.createTreeWalker(line, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = w.nextNode())) {
      let p = n.parentNode, skip = false;
      const f = { bg: '', u: 0, b: 0, s: 0, col: '' };
      while (p && p !== line) {
        if (p.nodeType === 1) {
          if (p.matches && p.matches(SKIP)) { skip = true; break; }
          const tg = p.tagName;
          if (tg === 'MARK' && !f.bg) f.bg = getComputedStyle(p).backgroundColor;
          if (tg === 'U') f.u = 1;
          if (tg === 'STRONG') f.b = 1;
          if (tg === 'S') f.s = 1;
          if (tg === 'SPAN' && p.style && p.style.color && !f.col && !p.classList.contains('wmrev')) f.col = p.style.color;
        }
        p = p.parentNode;
      }
      if (skip) continue;
      for (let i = 0; i < n.nodeValue.length; i++) out.push([f.bg, f.u, f.b, f.s, f.col].join('|'));
    }
    return out;
  }
  const bodyBox = () => QA('#slot .main .box').find(b => !b.classList.contains('fold') && !b.closest('.pop'));
  const lines = () => { const b = bodyBox(); return b ? QA(':scope > .ln', b) : []; };
  const pops = () => (typeof POPS !== 'undefined' ? POPS : []).filter(p => p.isConnected);
  const win = k => pops().find(p => p._wmk === k) || null;
  const has = n => { try { return typeof eval(n) !== 'undefined'; } catch (e) { return false; } };
  function mkState(base) { try { const v = JSON.parse(localStorage.getItem('jopangi.mkon') || '{}'); return base ? (v[base] || null) : v; } catch (e) { return null; } }
  window.__WM = {
    has: () => typeof wmBuild === 'function',
    errs: () => JSON.stringify((window.__ERR || []).slice(0, 6)),
    async go(law, jo) {
      pops().filter(p => !p._wmk).forEach(p => { try { closeOne(p); } catch (e) { p.remove(); } });
      S.tab = 'jo'; S.law = law; S.jo = jo;
      await render(); await wait(150);
      return !!bodyBox();
    },
    async orig(law, jo) { const B = await get('jo_' + law + '_본문.json'); const j = B.조[jo]; return JSON.stringify(j ? (typeof wmOrig === 'function' ? wmOrig(j) : (j.원본 || [])).slice(1) : null); },
    async origRaw(law, jo) { const B = await get('jo_' + law + '_본문.json'); const j = B.조[jo]; return JSON.stringify(j ? (j.원본 || []).slice(1) : null); },
    async rowsOf(law, jo) { const B = await get('jo_' + law + '_본문.json'); const j = B.조[jo]; return JSON.stringify(j ? (j.행 || []).map((r, ri) => ({ ri: ri, k: r.k, t: r.t || '' })) : null); },
    body() {
      return JSON.stringify(lines().map(l => ({ c: l.className, ri: l.dataset.ri == null ? null : +l.dataset.ri, t: plain(l), wm: !!l._wm,
        rev: QA('.wmrev', l).map(T), sup: QA('sup.fn', l).length, lbl: QA('.lbl', l).length,
        col: QA('span', l).filter(s => s.style && s.style.color && !s.classList.contains('wmrev')).length, mark: QA('mark', l).length, u: QA('u', l).length, b: QA('strong', l).length,
        jl: QA('.joLink', l).length, wl: QA('.wmlk', l).length })));
    },
    sig() { return JSON.stringify(lines().map(l => ({ ri: l.dataset.ri == null ? null : +l.dataset.ri, s: styleSig(l) }))); },
    geo() { return JSON.stringify(lines().map(l => { const r = l.getBoundingClientRect(); return { ri: l.dataset.ri == null ? null : +l.dataset.ri, h: Math.round(r.height * 10) / 10, n: plain(l).length }; })); },
    /* 네 법 전 조 — 렌더러(wmLineEl)로 모두 끔 줄 글 = 원본[1:] (창·기록 없이 · 볼트 m 그대로) */
    async allOff(law) {
      if (typeof wmBuild !== 'function') return JSON.stringify({ err: 'no wm' });
      const B = await get('jo_' + law + '_본문.json');
      const bad = []; let n = 0, nl = 0;
      const TT = {}; Object.keys(B.조).forEach(k => { TT[k] = { 제목: B.조[k].제목 }; });
      for (const jo of Object.keys(B.조)) {
        const j = B.조[jo]; n++;
        const j1 = Object.assign({}, j, { 원본: wmOrig(j) });   // 앱과 같은 원본(제목 줄에 붙은 ① 본문은 첫 줄로)
        const want = j1.원본.slice(1);
        const J2 = new Proxy({}, { get: (o, k) => k === jo ? j1 : TT[k] });
        const b = wmBuild(J2, jo); wmKeys(b.items);
        const X = { mode: 'wm', base: law + ':' + jo, law: law, jo: jo, j: j, rows: j.행 || [], b: b, on: {}, need: {}, mk: {} };
        const got = [];
        b.lines.forEach(L => { if (L.cls === 'tail' || L.cls === 'emb' || L.cls === 'fd') return; const d = wmLineEl(L, X); if (d) got.push(plain(d)); });
        nl += got.length;
        if (got.length !== want.length || got.some((t, i) => t !== want[i])) {
          const i = got.findIndex((t, i2) => t !== want[i2]);
          bad.push({ jo: jo, got: got.length, want: want.length, at: i, g: (got[i] || '').slice(0, 40), w: (want[i] || '').slice(0, 40) });
        }
      }
      return JSON.stringify({ n: n, lines: nl, bad: bad.length, ex: bad.slice(0, 5) });
    },
    /* ── 단추·칩 ── */
    mkBtn() { const b = QA('#slot .modebar .mode, #slot .jomt .jomd').find(x => /✎ 마크업/.test(T(x)));   /* 9/30 joscreen0929 합치기 — 모드 줄 글자화로 단추 = .jomt 안 .plgb.jomd(옛 .modebar .mode 도 받음) */ return JSON.stringify(Object.assign(ptOf(b), { t: b ? T(b) : null, n: b && Q('.mkn', b) ? T(Q('.mkn', b)) : null,
      ncs: b && Q('.mkn', b) ? (s => ({ fs: s.fontSize, col: s.color }))(getComputedStyle(Q('.mkn', b))) : null })); },
    jpChip() { const b = QA('#slot .conn .plgb').find(x => /☑ 정오문제/.test(T(x))); return JSON.stringify(Object.assign(ptOf(b), { t: b ? T(b) : null })); },
    ciChip() { const b = QA('#slot .conn .plgb').find(x => /📜 인용하는 조/.test(T(x))); return JSON.stringify(Object.assign(ptOf(b), { t: b ? T(b) : null, cur: b ? getComputedStyle(b).cursor : null })); },
    /* ── 마크업 창 ── */
    mkWin() {
      const p = win('mk'); if (!p) return JSON.stringify({ win: false, pane: !!Q('#slot .jopane') });
      const r = p.getBoundingClientRect(), hd = Q(':scope > .ph', p), bd = Q(':scope > .pb', p);
      const types = QA('.sh', p).map(s => ({ sub: s.dataset.sub, n: T(Q('.n', s)), open: T(Q('.ar', s)) === '▾', lock: s.classList.contains('lock') }));
      const items = QA('.it', p).map(i => ({ key: i.dataset.key, id: i.dataset.id, on: i.classList.contains('on'), lock: i.classList.contains('lock'), h: T(Q('.h', i)), pv: T(Q('.pv', i)), k: T(Q('.k', i)), sub: (i.closest('.its') && i.closest('.its').previousElementSibling) ? i.closest('.its').previousElementSibling.dataset.sub : null }));
      const cs = e => { if (!e) return null; const s = getComputedStyle(e); return { bg: s.backgroundColor, bc: s.borderTopColor, br: s.borderTopLeftRadius, fs: s.fontSize, fw: s.fontWeight, col: s.color }; };
      return JSON.stringify({ win: true, vis: vis(p), x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height), title: T(Q('.pt', p)),
        bar: T(Q('.mkbar', p)), lockMsg: T(Q('.wmlock', p)), foot: T(Q('.wmft', p)), groups: QA('.G', p).map(g => ({ g: g.dataset.g, t: T(Q('.wgh', g)), lock: g.classList.contains('lock') })),
        types: types, items: items, css: { p: cs(p), hd: cs(hd), bd: cs(bd) } });
    },
    mkAt(what, arg) {   // 창 안 누를 자리
      const p = win('mk'); if (!p) return 'null';
      let e = null;
      if (what === 'all') e = QA('.mkbar .tx', p).find(b => T(b) === '모두 켜기');
      else if (what === 'none') e = QA('.mkbar .tx', p).find(b => T(b) === '모두 끄기');
      else if (what === 'edit') e = QA('.mkbar .tx', p).find(b => /✎ 편집/.test(T(b)));
      else if (what === 'typeOn' || what === 'typeOff') { const s = QA('.sh', p).find(x => x.dataset.sub === arg); e = s ? QA('.tx', s).find(b => T(b) === (what === 'typeOn' ? '켜기' : '끄기')) : null; }
      else if (what === 'type') { const s = QA('.sh', p).find(x => x.dataset.sub === arg); e = s ? Q('.sn', s) : null; }
      else if (what === 'item') { e = QA('.it', p).find(i => i.dataset.key === arg) || null; if (e && e.parentNode.style.display === 'none') return JSON.stringify({ on: false, why: 'folded' }); }
      else if (what === 'x') e = Q(':scope > .ph > button.cfx', p);
      return JSON.stringify(Object.assign(ptOf(e), { t: e ? T(e) : null }));
    },
    mkItems(sub, h) { const p = win('mk'); if (!p) return '[]'; return JSON.stringify(QA('.it', p).filter(i => { const s = i.closest('.its') && i.closest('.its').previousElementSibling; return (!sub || (s && s.dataset.sub === sub)) && (h == null || T(Q('.h', i)) === h); }).map(i => ({ key: i.dataset.key, on: i.classList.contains('on'), h: T(Q('.h', i)), pv: T(Q('.pv', i)) }))); },
    mkon(base) { return JSON.stringify(mkState(base)); },
    mkonRaw() { return localStorage.getItem('jopangi.mkon'); },
    /* 줄 안 글자 조각의 꼴 — txt 를 품은 줄에서 그 글자 첫 자리의 조상 태그들 */
    charStyle(txt, occ) {
      const L = lines(); let k = 0;
      for (const l of L) {
        const pt = plain(l); let i = pt.indexOf(txt);
        while (i >= 0) {
          if (k === (occ || 0)) {
            const w = document.createTreeWalker(l, NodeFilter.SHOW_TEXT); let n, acc = 0, hit = null;
            while ((n = w.nextNode())) { let p = n.parentNode, sk = false; while (p && p !== l) { if (p.matches && p.matches(SKIP)) { sk = true; break; } p = p.parentNode; } if (sk) continue;
              if (acc + n.nodeValue.length > i) { hit = n; break; } acc += n.nodeValue.length; }
            const el0 = hit ? hit.parentNode : null; const cs = el0 ? getComputedStyle(el0) : null;
            return JSON.stringify({ line: pt.slice(0, 60), ri: l.dataset.ri == null ? null : +l.dataset.ri, fw: cs ? cs.fontWeight : null, tags: (() => { const o = []; let p = el0; while (p && p !== l) { o.push(p.tagName + (p.className ? '.' + p.className : '')); p = p.parentNode; } return o; })() });
          }
          k++; i = pt.indexOf(txt, i + 1);
        }
      }
      return JSON.stringify(null);
    },
    lineHas(txt) { return JSON.stringify(lines().map(plain).filter(t => t.indexOf(txt) >= 0).map(t => t.slice(0, 80))); },
    /* ── 글자 긁기(새로 칠하기) — 줄 안 txt 의 글자 [s, e) 화면 자리 ── */
    selPts(txt, occ) {
      const L = lines(); let k = 0;
      for (const l of L) {
        const pt = plain(l); let i = pt.indexOf(txt);
        while (i >= 0) {
          if (k === (occ || 0)) {
            const w = document.createTreeWalker(l, NodeFilter.SHOW_TEXT); let n, acc = 0; const nodes = [];
            while ((n = w.nextNode())) { let p = n.parentNode, sk = false; while (p && p !== l) { if (p.matches && p.matches(SKIP)) { sk = true; break; } p = p.parentNode; } if (sk) continue;
              for (let c = 0; c < n.nodeValue.length; c++) nodes.push([n, c]); acc += n.nodeValue.length; }
            const a = nodes[i], b = nodes[i + txt.length - 1];
            if (!a || !b) return 'null';
            a[0].parentNode.scrollIntoView ? l.scrollIntoView({ block: 'center' }) : 0;
            const ra = document.createRange(); ra.setStart(a[0], a[1]); ra.setEnd(a[0], a[1] + 1);
            const rb = document.createRange(); rb.setStart(b[0], b[1]); rb.setEnd(b[0], b[1] + 1);
            const A = ra.getBoundingClientRect(), Bx = rb.getBoundingClientRect();
            return JSON.stringify({ x1: A.left + 1, y1: A.top + A.height / 2, x2: Bx.right - 1, y2: Bx.top + Bx.height / 2, ri: l.dataset.ri == null ? null : +l.dataset.ri, wm: !!l._wm });
          }
          k++; i = pt.indexOf(txt, i + 1);
        }
      }
      return 'null';
    },
    selText() { const s = getSelection(); return s ? String(s) : ''; },
    bub() { const b = document.getElementById('stkbub') || document.querySelector('#jomk9:not([hidden]) [data-tag]'); return JSON.stringify(ptOf(b, true)); },   /* ★ jo_markfix(9/29) A-3 — 거품 🏷 가 막대 끝 단추로 옮겨 감 · 옛 판은 거품 그대로 */
    attPop() { const p = pops().find(x => /선택한 글에 붙이기/.test(x._pk || '')); if (!p) return 'null'; const l2 = QA('span', p).find(s => /다른 마크업/.test(T(s))); return JSON.stringify(Object.assign(ptOf(l2), { ex: T(Q('.cdim', p)) })); },
    newPopBtn(label) { const p = pops().find(x => /새 스티커/.test(x._pk || '')); if (!p) return 'null'; const b = QA('button', p).find(x => T(x) === label) || QA('.stkgrid button', p)[0]; return JSON.stringify(Object.assign(ptOf(b), { t: b ? T(b) : null, all: QA('.stkgrid button', p).map(T) })); },
    mks(base) { try { return JSON.stringify(Object.keys(mkAll()).filter(k => k.split('\u001f')[0] === base).map(k => ({ k: k.split('\u001f').slice(1).join('|'), v: mkAll()[k] }))); } catch (e) { return '[]'; } },
    toasts() { return JSON.stringify(QA('#toasts .toast').map(T)); },
    closePops() { pops().filter(p => !p._wmk).forEach(p => { try { closeOne(p); } catch (e) { p.remove(); } }); return '1'; },
    /* ── 필기 씨 ── */
    inkSeed(key) { const A = inkAll(); A[key] = { s: [{ c: '#e11d48', w: 2, p: [[0.1, 0.1], [0.2, 0.15], [0.3, 0.12]] }], ts: nowIso() }; INK = A; lsWrite(INK_KEY, A, '필기'); return inkHas(key); },
    inkClear(key) { const A = inkAll(); delete A[key]; INK = A; lsWrite(INK_KEY, A, '필기'); return !inkHas(key); },
    stickBar() { const b = Q('#slot .stkbar'); return JSON.stringify({ on: !!b, t: T(b), orphan: b ? T(Q('.badge', b)) : null, stk: QA('#slot .box .stk').length }); },
    stkAt(i) { const s = QA('#slot .box .stk')[i || 0]; return JSON.stringify(Object.assign(ptOf(s), { t: s ? T(s) : null })); },
    stkPop() { const p = pops().find(x => /✎ 스티커/.test(x._pk || '')); return JSON.stringify(p ? { on: true, btns: QA('button', p).map(T).slice(0, 12) } : { on: false }); },
    orphanSeed(base) { const k = [base, '항/①', 3, 9, 'font', '#ff0000', '없는글자없는글'].join('\u001f'); mkPut(k, { op: 'new', t: 'font', v: '#ff0000' }); return Object.keys(mkAll()).length; },
    /* ── 정오문제 창 ── */
    jpWin() {
      const p = win('jp');
      const pane = Q('#slot .jopane'), hdl = QA('#slot > .handle').filter(h => /정오문제/.test(h.title || '')).length;
      const main = Q('#slot > .main'), mr = main ? main.getBoundingClientRect() : null;
      if (!p) return JSON.stringify({ win: false, pane: !!pane, handle: hdl, mainW: mr ? Math.round(mr.width * 10) / 10 : null,
        paneHead: pane ? QA('.ctrlbar', pane).map(T) : null, grade: pane ? QA('button', pane).filter(b => /✅ 채점/.test(T(b))).length : 0 });
      const r = p.getBoundingClientRect();
      const bar = Q('.jpbar', p), nav = Q('.jpnav', p);
      const cs = e => { if (!e) return null; const s = getComputedStyle(e); return { fs: s.fontSize, fw: s.fontWeight, col: s.color, bg: s.backgroundColor, bw: s.borderTopWidth }; };
      return JSON.stringify({ win: true, vis: vis(p), x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height), title: T(Q('.pt', p)),
        pane: !!pane, handle: hdl, mainW: mr ? Math.round(mr.width * 10) / 10 : null,
        bar: bar ? QA('.jpt', bar).map(b => ({ t: T(b), on: b.classList.contains('on'), cs: cs(b) })) : null, barText: T(bar),
        nav: nav ? { t: T(nav), cs: cs(nav), arr: QA('.jpt', nav).map(b => ({ t: T(b), dis: b.classList.contains('dis'), cs: cs(b) })) } : null,
        cards: QA('.jpcards > *', p).map(c => c.id), grade: QA('button', p).filter(b => /✅ 채점|← 이전|다음 →/.test(T(b))).length,
        foot: !!Q('.wmft', p), head: !!QA('*', p).find(e => /☑ 정오문제 \d+건/.test(T(e)) && e.children.length === 0) });
    },
    jpAt(what, arg) {
      const p = win('jp'); if (!p) return 'null';
      let e = null;
      if (what === 'bar') e = QA('.jpbar .jpt', p).find(b => T(b) === arg);
      else if (what === 'next') e = QA('.jpnav .jpt', p).find(b => T(b) === '→');
      else if (what === 'prev') e = QA('.jpnav .jpt', p).find(b => T(b) === '←');
      else if (what === 'ox') { const c = document.getElementById('jp-' + arg.k); e = c ? QA('.mboxb', c).find(b => T(b) === arg.v) : null; }
      else if (what === 'src') { const c = document.getElementById('jp-' + arg); e = c ? Q('.mbqhd .qb.v, .qhd .qb.v', c) : null; }
      else if (what === 'rgb') { const c = document.getElementById('jp-' + arg); e = c ? Q('.mbrecw .rgb', c) : null; }
      else if (what === 'rgx') { const c = document.getElementById('jp-' + arg); e = c ? Q('.mbrecw .rgx', c) : null; }
      return JSON.stringify(Object.assign(ptOf(e), { t: e ? T(e) : null }));
    },
    jpCard(k) {
      const c = document.getElementById('jp-' + k); if (!c) return JSON.stringify(null);
      const exp = Q('.mbexp', c), rs = Q('.mbres2', c);
      return JSON.stringify({ ox: QA('.mboxb', c).map(b => ({ t: T(b), cls: b.className, bc: getComputedStyle(b).borderTopColor, col: getComputedStyle(b).color })), res: T(rs),
        exp: vis(exp), inst: !!Q('.oxinst', c) || c.classList.contains('oxinst'), strip: c.querySelector('.mbrecw') ? T(c.querySelector('.mbrecw')) : null });
    },
    jpKeys() { const p = win('jp'); return JSON.stringify(p ? QA('.jpcards > *', p).map(c => c.id.replace(/^jp-/, '')) : []); },
    rec(k) { return JSON.stringify(oxOf(k) || null); },
    recGone(k) { try { return JSON.stringify(Object.keys(rgnAll()).filter(x => x.indexOf(k + '|') === 0)); } catch (e) { return '[]'; } },
    oxClearAll(keys) { keys.forEach(k => { try { oxClear(k); } catch (e) {} }); return '1'; },
    /* 1차객 화면 카드(qb-<열쇠>) */
    gkCard(k) { const c = document.getElementById('qb-' + k); if (!c) return JSON.stringify(null);
      return JSON.stringify({ ox: QA('.mboxb', c).map(b => ({ t: T(b), cls: b.className })), res: T(Q('.mbres2', c)), inst: !!Q('.oxinst', c) }); },
    gkOx(k, v) { const c = document.getElementById('qb-' + k); const b = c ? QA('.mboxb', c).find(x => T(x) === v) : null; return JSON.stringify(ptOf(b)); },
    /* ── 인용 창 ── */
    ciWin() { const p = win('ci'); if (!p) return JSON.stringify({ win: false });
      const r = p.getBoundingClientRect();
      return JSON.stringify({ win: true, vis: vis(p), w: Math.round(r.width), title: T(Q('.pt', p)), foot: T(Q('.wmft', p)),
        rows: QA('.ci', p).map(c => ({ k: c.dataset.jo, cn: T(Q('.cn', c)), ct: T(Q('.ct', c)), cp: T(Q('.cp', c)), b: T(Q('.cp b', c)), bbg: Q('.cp b', c) ? getComputedStyle(Q('.cp b', c)).backgroundColor : null, bfw: Q('.cp b', c) ? getComputedStyle(Q('.cp b', c)).fontWeight : null })) }); },
    ciAt(k) { const p = win('ci'); const c = p ? QA('.ci', p).find(x => x.dataset.jo === k) : null; return JSON.stringify(ptOf(c)); },
    cur() { return JSON.stringify({ tab: S.tab, law: S.law, jo: S.jo, mkWin: !!S.mkWin, ciWin: S.ciWin || '', joPanel: !!S.joPanel, stick: !!S.stick }); },
    setS(o) { Object.assign(S, o); return '1'; },
    async rr() { await render(); await wait(100); return '1'; },
    syncKeys() { return JSON.stringify(typeof SYNC_KEYS !== 'undefined' ? SYNC_KEYS : null); }
  };
})();
