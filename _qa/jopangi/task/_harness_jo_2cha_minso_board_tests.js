/* _harness_jo_2cha_minso_board_tests.js — _task_jo_2cha_minso_board 관문이 페이지에 넣는 도구(__C2).
   NEW·BASE(바탕 281c93f) 둘 다에 같은 것을 넣는다 — 없는 것(.c2sortar · .mpop · .c2miss …)은 null·0 으로 돌려준다(헛잣대가 FAIL 로 읽힌다).
   재는 것 = DOM 실물(있는가 · 몇 개 · 글자 · 자리 getBoundingClientRect · 계산 스타일 · localStorage 기록 값). 누름은 하네스(파이썬)가 진짜 마우스·손가락으로. */
(function(){
const wait = ms => new Promise(r => setTimeout(r, ms));
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); return { x: +r.left.toFixed(1), y: +r.top.toFixed(1), w: +r.width.toFixed(1), h: +r.height.toFixed(1), r: +r.right.toFixed(1), b: +r.bottom.toFixed(1), cx: +(r.left + r.width / 2).toFixed(1), cy: +(r.top + r.height / 2).toFixed(1) }; };
const cs = (e, p) => e ? getComputedStyle(e)[p] : null;
const isBusy = () => { try { return !!busy; } catch (e) { return false; } };
const idle = async () => { for (let i = 0; i < 600; i++){ if (!isBusy()) return true; await wait(25); } return false; };
const pops = () => { try { return POPS.filter(p => p.isConnected); } catch (e) { return []; } };
const main = () => document.querySelector('#slot .main');
const vis = e => !!e && e.isConnected && !e.closest('.c2hid,.mdhid,[hidden]') && e.getClientRects().length > 0 && cs(e, 'visibility') !== 'hidden';
const hit = (e, pad) => { if (!e) return null; const r = e.getBoundingClientRect(); let cx = r.left + r.width / 2, cy = r.top + r.height / 2; let a = document.elementFromPoint(cx, cy);
  const on0 = p => !!p && (p === e || e.contains(p));
  if (!on0(a)) for (const f of [0.15, 0.3, 0.7, 0.85]){ const x = r.left + r.width * f, b = document.elementFromPoint(x, cy); if (on0(b)){ cx = x; a = b; break; } }   /* 가운데가 덮였으면 보이는 쪽(사람이 누르는 자리) */
  return Object.assign(R(e), { cx: +cx.toFixed(1), on: on0(a) && cy > 0 && cy < innerHeight && cx > 0 && cx < innerWidth, at: a ? (a.className && a.className.baseVal == null ? String(a.className) : a.tagName) : null }); };
const rowsOf = () => [...document.querySelectorAll('#slot .c2row')];
const rowBy = ck => rowsOf().find(r => r.dataset.ck === ck) || null;
const rowByCode = code => rowsOf().find(r => !r.classList.contains('c2ov') && (txt(r.querySelector('.c2code')) || '').indexOf(code) === 0) || null;
const memoWins = () => [...document.querySelectorAll('.pop.mpop')];
const LS = k => { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; } };
const clean = () => { try { closeAllPops(true); } catch (e) {} document.querySelectorAll('.c2fly,.c2srp,.pitmenu').forEach(x => x.remove()); };   /* 메모 창은 앱이 다룬다(카드 메모 창 = 카드와 같이 닫힘 · 보드 메모 창 = render 가 다시 지음) */
window.__C2 = {
  wait, idle,
  errs: () => (window.__ERR || []).slice(),
  /* 2차 보드로 — o = S 덧값 */
  async go(o, keep){ if (!keep) clean(); await idle(); Object.assign(S, { law: '민사소송법', tab: 'cha2', boardKind: '기출', series: '', yearFilter: '', cha2Sel: null, cha2Filter: {} }, o || {});
    await render(); await idle(); await wait(500); return this.board(); },
  async rerender(){ await idle(); await render(); await idle(); await wait(400); return true; },
  board(){ const m = main(); const bar = m ? m.firstElementChild : null;
    const kids = bar ? [...bar.children].filter(e => cs(e, 'display') !== 'none') : [];
    const lst = m ? m.querySelector('.c2list') : null;
    return { bar: kids.map(e => ({ tag: e.tagName, cls: String(e.className || ''), t: txt(e) })),
      ysort: document.querySelectorAll('#slot .ysort').length, ysel: document.querySelectorAll('#slot select.ysel').length, lh: document.querySelectorAll('#slot .c2lh').length,
      rows: rowsOf().filter(r => !r.classList.contains('c2ov')).length, ov: rowsOf().filter(r => r.classList.contains('c2ov')).length,
      bands: document.querySelectorAll('#slot .c2band').length, heads: document.querySelectorAll('#slot .c2uh:not(.c2unone)').length, unone: document.querySelectorAll('#slot .c2uh.c2unone').length,
      rheads: document.querySelectorAll('#slot .c2rh').length, bodies: document.querySelectorAll('#slot .c2bw').length,
      first: rowsOf().length ? txt(rowsOf()[0].querySelector('.c2code')) : null,
      seg: [...document.querySelectorAll('#ordSeg button')].map(b => ({ t: txt(b), on: b.classList.contains('on'), title: b.title, dis: b.disabled })),
      lv: txt(document.querySelector('#slot .uzstep.c2lv')), lvTitle: (document.querySelector('#slot .uzstep.c2lv') || {}).title || null,
      sortar: txt(document.querySelector('#slot .c2sortar')), srw: !!document.querySelector('#slot .c2srw'),
      S: { ord: (typeof c2Ord === 'function') ? c2Ord() : null, yf: S.yearFilter, ys: S.yearSort, lv: S.c2lv || null },
      listW: lst ? lst.clientWidth : null, mainSW: m ? [m.scrollWidth, m.clientWidth] : null }; },
  /* 머리 줄 차례 — 보이는 자식 가운데 이 다섯의 차례 */
  headOrder(){ const m = main(); const bar = m ? m.firstElementChild : null; if (!bar) return null;
    return [...bar.children].map(e => e.classList.contains('pill') ? 'pill' : e.classList.contains('ordseg') ? 'ordseg' : e.classList.contains('c2sortar') ? 'c2sortar' : (e.classList.contains('uzstep') && e.classList.contains('c2lv')) ? 'c2lv' : e.classList.contains('c2srw') ? 'c2srw' : (e.tagName === 'SELECT' ? 'select' : (e.tagName === 'SPAN' && !e.className ? 'sp' : String(e.className || e.tagName)))); },
  at(sel, i){ const L = [...document.querySelectorAll(sel)].filter(vis); const e = L[i || 0]; if (!e) return null; try { e.scrollIntoView({ block: 'center', inline: 'nearest' }); } catch (x) {} return hit(e); },
  atIn(rootSel, sel, i){ const r0 = document.querySelector(rootSel); if (!r0) return null; const L = [...r0.querySelectorAll(sel)].filter(vis); const e = L[i || 0]; if (!e) return null; try { e.scrollIntoView({ block: 'nearest' }); } catch (x) {} return hit(e); },
  segOn(){ const b = document.querySelector('#ordSeg button.on'); return b ? hit(b) : null; },
  fmenu(){ const m = document.querySelector('.c2fmenu'); return m ? { n: m.querySelectorAll('.it').length, items: [...m.querySelectorAll('.it')].map(txt), on: txt(m.querySelector('.it.on')), rect: R(m), z: cs(m, 'zIndex') } : null; },
  fmenuItem(t){ const m = document.querySelector('.c2fmenu'); const it = m ? [...m.querySelectorAll('.it')].find(x => txt(x) === t) : null; if (!it) return null; try { it.scrollIntoView({ block: 'nearest' }); } catch (x) {} return hit(it); },
  /* 간격(B2) — 편 띠 사이 · 띠 높이 · 띠→단원 머리 · 도구줄→첫 편 띠 · 줄 높이 */
  gaps(code){ const m = main(); const lst = m && m.querySelector('.c2list'); if (!lst) return null; const kids = [...lst.children].filter(e => e.getClientRects().length);
    const bands = kids.filter(e => e.classList.contains('c2band')); const gapB = [], b2h = [];
    bands.forEach(b => { const i = kids.indexOf(b); if (i > 0){ const p = kids[i - 1]; gapB.push(+(b.getBoundingClientRect().top - p.getBoundingClientRect().bottom).toFixed(1)); }
      const n = kids[i + 1]; if (n && n.classList.contains('c2uh')) b2h.push(+(n.getBoundingClientRect().top - b.getBoundingClientRect().bottom).toFixed(1)); });
    const bar = m.firstElementChild; const r0 = code ? rowByCode(code) : null;
    return { bandGapMax: gapB.length ? Math.max(...gapB) : null, bandGaps: gapB.slice(0, 6), bandH: bands.length ? Math.max(...bands.map(b => +b.getBoundingClientRect().height.toFixed(1))) : null,
      band2head: b2h.length ? Math.max(...b2h) : null, bar2band: bands.length ? +(bands[0].getBoundingClientRect().top - bar.getBoundingClientRect().bottom).toFixed(1) : null,
      rowH: r0 ? +r0.getBoundingClientRect().height.toFixed(1) : null, total: +(lst.getBoundingClientRect().height).toFixed(1), scrollH: m.scrollHeight }; },
  /* 번호(B3) */
  secNo(kind, label){ const sel = kind === 'p' ? '#slot .c2band > .no' : kind === 'u' ? '#slot .c2uh > .no' : '#slot .c2rh > .r'; const e = [...document.querySelectorAll(sel)].find(x => txt(x).replace(/\s*›$/, '') === label);
    if (!e) return null; try { e.scrollIntoView({ block: 'center' }); } catch (x) {} return Object.assign(hit(e), { shut: e.classList.contains('shut'), sec: !!e.classList.contains('c2secno'), after: getComputedStyle(e, '::after').content }); },
  sectionView(){ const L = [...document.querySelectorAll('#slot .c2list > *')]; return L.map(e => e.classList.contains('c2band') ? 'B:' + txt(e.querySelector('.no')) : e.classList.contains('c2uh') ? (e.classList.contains('c2unone') ? 'U:없음' : 'U:' + txt(e.querySelector('.no'))) : e.classList.contains('c2rh') ? 'R:' + txt(e.querySelector('.r')) : e.classList.contains('c2row') ? 'r' : '?').join(' '); },
  /* 줄·본문(B4) */
  rowInfo(code){ const r = rowByCode(code); if (!r) return null; const bw = r.querySelector('.c2bw'); const rb = bw && bw.querySelector('.rbody');
    const lines = bw ? [...bw.querySelectorAll('.rln')] : []; const t1 = r.querySelector('.c2t1');
    return { ck: r.dataset.ck, code: txt(r.querySelector('.c2code')), body: !!bw, vis: lines.filter(n => !n.classList.contains('c2hid') && !n.classList.contains('mdhid')).length, all: lines.length,
      dep: txt(r.querySelector('.c2dep')), depFirst: !!(t1 && t1.firstElementChild && t1.firstElementChild.classList.contains('c2dep')), depTitle: (r.querySelector('.c2dep') || {}).title || null,
      q1: !!r.querySelector('.c2code .c2q1'), q1Title: (r.querySelector('.c2q1') || {}).title || null, coq: bw ? bw.querySelectorAll('.callout.co-question').length : 0,
      callouts: bw ? [...bw.querySelectorAll('.callout')].filter(vis).length : 0, h: +r.getBoundingClientRect().height.toFixed(1),
      t1: t1 ? [...t1.children].map(e => String(e.className || e.tagName)) : null, pb: t1 ? [...t1.querySelectorAll('.c2pb .c2pbtn')].map(txt) : null,
      mbcl: r.querySelectorAll('.mbcl,[data-clbtn]:not([hidden])').length, clword: r.querySelectorAll('[data-clword]').length,
      memoChip: txt(r.querySelector('.c2t1 .chip.c-memo')), memoTitle: (r.querySelector('.c2t1 .chip.c-memo') || {}).title || null,
      mchip: txt(r.querySelector('.c2t1 .c2mchip')), mchipCls: (r.querySelector('.c2t1 .c2mchip') || {}).className || null, rmiss: [...r.classList].filter(c => /^rmiss$|^m-/.test(c)).join(' '),
      shadow: cs(r, 'boxShadow'), ue: txt(r.querySelector('.c2r3 .c2ue')), uchips: [...r.querySelectorAll('.c2r3 .c2uc')].filter(vis).map(e => ({ t: txt(e), added: e.classList.contains('added'), bs: cs(e, 'borderTopStyle') })),
      tabs: r.querySelectorAll('.c2tabs').length, r3: R(r.querySelector('.c2r3')), rect: R(r) }; },
  rowPart(code, part){ const r = rowByCode(code); if (!r) return null; let e = null;
    if (part === 'title') e = r.querySelector('.c2t2'); else if (part === 'dep') e = r.querySelector('.c2dep'); else if (part === 'q1') e = r.querySelector('.c2q1');
    else if (part === 'code') { const c = r.querySelector('.c2code'); if (c){ const t = c.firstChild; if (t && t.nodeType === 3){ const rg = document.createRange(); rg.selectNodeContents(t); const b = rg.getBoundingClientRect(); try { c.scrollIntoView({ block: 'center' }); } catch (x) {} const b2 = rg.getBoundingClientRect(); const a = document.elementFromPoint(b2.left + b2.width / 2, b2.top + b2.height / 2); return { cx: b2.left + b2.width / 2, cy: b2.top + b2.height / 2, on: !!a && (a === c || c.contains(a)), w: b2.width }; } e = c; } }
    else if (part === 'memo') e = r.querySelector('.c2t1 .chip.c-memo'); else if (part === 'hs') e = [...r.querySelectorAll('.c2pbtn')].find(x => txt(x) === '해설');
    else if (part === 'cl') e = r.querySelector('.c2pbtn.cl'); else if (part === 'ue') e = r.querySelector('.c2r3 .c2ue'); else if (part === 'uadd') e = r.querySelector('.c2r3 .c2uadd');
    else if (part === 'score') e = r.querySelector('.chip.c-score');
    if (!e) return null; try { e.scrollIntoView({ block: 'center' }); } catch (x) {} return hit(e); },
  rowRect(code){ const r = rowByCode(code); return r ? R(r) : null; },
  /* 본문 줄 하나(헤딩 글 시작으로) · 그 줄의 누락 단추 · 고리 */
  lineOf(code, start, inCard){ const host = inCard ? this.cardBody(code) : (rowByCode(code) || {}).querySelector && rowByCode(code).querySelector('.c2bw .rbody'); if (!host) return null;
    return [...host.querySelectorAll(':scope > .rln')].find(n => (n.textContent || '').replace(/누락.*$|극복.*$/, '').replace(/\s+/g, ' ').indexOf(start) >= 0) || null; },
  lineInfo(code, start, inCard){ const n = this.lineOf(code, start, inCard); if (!n) return null; const b = n.querySelector(':scope > .c2miss');
    return { cls: n.className, vis: vis(n), shadow: cs(n, 'boxShadow'), title: n.title || '', btn: b ? { t: txt(b), cls: b.className, title: b.title, bg: cs(b, 'backgroundColor'), color: cs(b, 'color') } : null,
      lnk: [...n.querySelectorAll(':scope > .c2lnkw > .c2lnk')].map(x => ({ cls: x.className, n: x.dataset.n || '', after: getComputedStyle(x, '::after').content, title: x.title, color: cs(x, 'color') })) }; },
  missBtn(code, start, inCard){ const n = this.lineOf(code, start, inCard); const b = n && n.querySelector(':scope > .c2miss'); if (!b) return null; try { b.scrollIntoView({ block: 'center' }); } catch (x) {} return hit(b); },
  lnkBtn(code, start, inCard, cls){ const n = this.lineOf(code, start, inCard); const b = n && [...n.querySelectorAll(':scope > .c2lnkw > .c2lnk')].find(x => !cls || x.classList.contains(cls)); if (!b) return null; try { b.scrollIntoView({ block: 'center' }); } catch (x) {} return hit(b); },
  missMenu(){ const m = document.querySelector('.c2missm'); return m ? { head: txt(m.querySelector('.mh')), headCls: m.querySelector('.mh').className, rows: [...m.querySelectorAll('.mi')].map(txt), btns: [...m.querySelectorAll('.mb button')].map(txt), z: cs(m, 'zIndex'), rect: R(m) } : null; },
  missMenuBtn(t){ const m = document.querySelector('.c2missm'); const b = m ? [...m.querySelectorAll('.mb button')].find(x => txt(x) === t) : null; return b ? hit(b) : null; },
  missMenuDel(i){ const m = document.querySelector('.c2missm'); const b = m ? m.querySelectorAll('.mi .mdel')[i] : null; return b ? hit(b) : null; },
  missLS(){ return LS('jopangi.c2miss') || {}; },
  setMiss(o){ try { localStorage.setItem('jopangi.c2miss', JSON.stringify(o)); } catch (e) {} return true; },
  /* 메모 창(B6~B8) */
  memo(){ const m = main(); return memoWins().map(p => { const pt = p.querySelector('.ph .pt'); const ph = p.querySelector(':scope > .ph'); const w = p._word;
    return { wk: p.dataset.wk, mode: p.classList.contains('mb') ? 'b' : 'c', inMain: !!(m && m.contains(p)), pos: cs(p, 'position'), title: txt(pt), headH: ph ? +ph.getBoundingClientRect().height.toFixed(1) : null,
      textFs: cs(p.querySelector('.mtext'), 'fontSize'), w: +p.getBoundingClientRect().width.toFixed(1), rect: R(p), z: cs(p, 'zIndex'), text: txt(p.querySelector('.mmain .mtext')), meta: txt(p.querySelector('.mmain .mmeta')),
      re: [...p.querySelectorAll('.mre .mrc')].map(txt), word: w ? R(w) : null, wordT: w ? txt(w).replace(/[햄찌꼬까]+$/, '') : null, edit: !!p.querySelector('textarea.memoin'), add: !!(p.querySelector('.madd') && !p.querySelector('.madd').hidden) }; }); },
  lines(){ const m = main(); const sv = m && m.querySelector(':scope > svg.c2ml'), sf = document.querySelector('body > svg.c2mlf');
    const pp = s => s ? [...s.querySelectorAll('path')].map(x => x.getAttribute('d')) : [];
    return { b: pp(sv), c: pp(sf), bsz: sv ? [sv.getAttribute('width'), sv.getAttribute('height')] : null, bz: sv ? cs(sv, 'zIndex') : null, cz: sf ? cs(sf, 'zIndex') : null }; },
  memoPart(i, part){ const p = memoWins()[i || 0]; if (!p) return null; const e = part === 'x' ? p.querySelector('.ph .mx') : part === 'head' ? p.querySelector('.ph .pt') : part === 'text' ? p.querySelector('.mmain .mtext') : part === 'cl' ? p.querySelector('.mcl')
      : part === 'grip' ? p.querySelector(':scope > .prsz') : part === 'save' ? [...p.querySelectorAll('.memobtn .tool')].find(x => /저장/.test(txt(x))) : part === 'del' ? [...p.querySelectorAll('.memobtn .tool')].find(x => /삭제/.test(txt(x))) : part === 'ta' ? p.querySelector('.madd textarea')
      : part === 'reText' ? p.querySelector('.mre .mrc .mtext') : part === 'go' ? p.querySelector('.madd .tool') : null;
    return e ? hit(e) : null; },
  memoType(i, v, sel){ const p = memoWins()[i || 0]; const t = p && p.querySelector(sel || 'textarea.memoin'); if (!t) return false; t.focus(); t.value = v; t.dispatchEvent(new Event('input', { bubbles: true })); return true; },
  memoIdx(word, mode){ return memoWins().findIndex(p => (!mode || (mode === 'b' ? p.classList.contains('mb') : p.classList.contains('mc'))) && p._word && txt(p._word).indexOf(word) === 0); },
  wordAt(code, word, inCard){ const host = inCard ? this.cardPop(code) : rowByCode(code); if (!host) return null; const w = [...host.querySelectorAll('.pitw')].find(x => txt(x).indexOf(word) === 0 && vis(x)); if (!w) return null; try { w.scrollIntoView({ block: 'center' }); } catch (x) {} return hit(w); },
  flags(){ return { board: [...document.querySelectorAll('#slot .c2bw .pitflag')].filter(e => cs(e, 'display') !== 'none' && e.getClientRects().length).length, card: [...document.querySelectorAll('.pop.k-cell .pitflag')].filter(e => cs(e, 'display') !== 'none' && e.getClientRects().length).length,
    all: [...document.querySelectorAll('#slot .pitflag')].filter(e => cs(e, 'display') !== 'none' && e.getClientRects().length).length }; },
  pit(){ return LS('jopangi.postit') || {}; },
  setPit(o){ try { localStorage.setItem('jopangi.postit', JSON.stringify(o)); PITREC = null; PITIDX.rec = null; PITCIDX.rec = null; } catch (e) {} return true; },
  pitEditSave(k, v){ const p = k.split('\u001f'); pitEdit(p[0], p[1], +p[2], p[3], null); const ta = [...document.querySelectorAll('.pop textarea.memoin')].pop(); if (!ta) return false; ta.value = v; const ok = [...document.querySelectorAll('.pop .memobtn .tool.on')].pop(); if (!ok) return false; ok.click(); return true; },
  /* 카드 창 */
  cardPop(code){ return pops().find(p => /🧾/.test(txt(p.querySelector('.ph .pt'))) && txt(p.querySelector('.ph .pt')).indexOf(code) >= 0) || null; },
  cardBody(code){ const p = this.cardPop(code); return p ? p.querySelector('.rbody.card') : null; },
  card(code){ const p = this.cardPop(code); if (!p) return null; const hd = p.querySelector(':scope > .ph'); const fb = p.querySelector('.c2fold');
    return { rect: R(p), z: cs(p, 'zIndex'), title: txt(p.querySelector('.ph .pt')), tab: txt(p.querySelector('.gtabs .tool.on')), fold: fb ? txt(fb) : null, head: hd ? hit(hd.querySelector('.pt')) : null,
      ow: p.offsetWidth - p.clientWidth - (parseFloat(cs(p, 'borderLeftWidth')) || 0) - (parseFloat(cs(p, 'borderRightWidth')) || 0), scrollTop: p.scrollTop, marks: p.querySelectorAll('mark.srm').length, miss: p.querySelectorAll('.c2miss').length, lnk: p.querySelectorAll('.c2lnk').length,
      pad: cs(p.querySelector('.rbody.card'), 'paddingLeft') }; },
  cardFold(code){ const p = this.cardPop(code); const b = p && p.querySelector('.c2fold'); return b && !b.hidden ? hit(b) : null; },
  cardTab(code, t){ const p = this.cardPop(code); const b = p && [...p.querySelectorAll('.gtabs .tool')].find(x => txt(x).indexOf(t) === 0); return b ? hit(b) : null; },
  popsInfo(){ return pops().map(p => ({ kind: (String(p.className).match(/k-([\w-]+)/) || [])[1] || '', t: txt(p.querySelector('.ph .pt')), z: +(p.style.zIndex || 0), rect: R(p), sized: p.classList.contains('sized') })); },
  pall(){ const b = document.querySelector('.pop .ph > button.pall'); return b ? hit(b) : null; },
  popGrip(i){ const p = pops()[i]; const g = p && p.querySelector(':scope > .prsz'); return g ? hit(g) : null; },
  popOf(re){ const rx = new RegExp(re); const i = pops().findIndex(p => rx.test(txt(p.querySelector('.ph .pt')))); return i; },
  popRect(i){ const p = pops()[i]; return p ? R(p) : null; },
  popHead(i){ const p = pops()[i]; const h = p && p.querySelector('.ph .pt'); return h ? hit(h) : null; },
  popText(re){ const rx = new RegExp(re); const p = pops().find(q => rx.test(txt(q.querySelector('.ph .pt')))); return p ? txt(p.querySelector('.pb')).slice(0, 2000) : null; },
  topZ(){ let z = 0; pops().forEach(p => { z = Math.max(z, +(p.style.zIndex || 0)); }); return z; },
  closeAll(){ clean(); return true; },
  /* 연결(B11) */
  lkm(){ const m = document.querySelector('.c2lkm'); return m ? { head: txt(m.querySelector('.mh')), secs: [...m.querySelectorAll('.sec')].map(txt), li: [...m.querySelectorAll('.li')].map(txt), ai: [...m.querySelectorAll('.ai')].map(txt), a0: txt(m.querySelector('.a0')),
    focus: !!(document.activeElement && m.contains(document.activeElement)), rect: R(m), z: cs(m, 'zIndex') } : null; },
  lkmType(v){ const i = document.querySelector('.c2lkm .add input'); if (!i) return false; i.focus(); i.value = v; i.dispatchEvent(new Event('input', { bubbles: true })); return true; },
  lkmItem(sel, re, i){ const rx = new RegExp(re); const L = [...document.querySelectorAll('.c2lkm ' + sel)].filter(x => rx.test(txt(x))); const e = L[i || 0]; if (!e) return null; try { e.scrollIntoView({ block: 'nearest' }); } catch (x) {} return hit(e); },
  lkmX(i){ const L = [...document.querySelectorAll('.c2lkm .li .lx')]; const e = L[i || 0]; return e ? hit(e) : null; },
  qlLS(){ return LS('jopangi.c2qlink') || {}; },
  flash(code){ const b = this.cardBody(code); return b ? [...b.querySelectorAll(':scope > .rh1.lkflash')].map(txt) : null; },
  lineTopInCard(code, start){ const p = this.cardPop(code); const n = this.lineOf(code, start, true); if (!p || !n) return null; const hd = p.querySelector(':scope > .ph'); return +(n.getBoundingClientRect().top - (hd ? hd.getBoundingClientRect().bottom : p.getBoundingClientRect().top)).toFixed(1); },
  /* 단원(B12) */
  upick(){ const m = document.querySelector('.c2upick'); return m ? { ub: m.querySelectorAll('.ub').length, ui: [...m.querySelectorAll('.ui')].map(txt).slice(0, 60), on: [...m.querySelectorAll('.ui.on')].map(txt), u0: txt(m.querySelector('.u0')), focus: document.activeElement === m.querySelector('input'), rect: R(m) } : null; },
  upickType(v){ const i = document.querySelector('.c2upick input'); if (!i) return false; i.value = v; i.dispatchEvent(new Event('input', { bubbles: true })); return true; },
  upickItem(re){ const rx = new RegExp(re); const e = [...document.querySelectorAll('.c2upick .ui')].find(x => rx.test(txt(x)) && !x.classList.contains('on')); if (!e) return null; try { e.scrollIntoView({ block: 'nearest' }); } catch (x) {} return hit(e); },
  addedX(code){ const r = rowByCode(code); const x = r && r.querySelector('.c2uc.added .x'); return x ? hit(x) : null; },
  unitLS(){ return LS('jopangi.c2unit') || {}; },
  unitRows(name){ const L = [...document.querySelectorAll('#slot .c2list > *')]; const i = L.findIndex(e => e.classList.contains('c2uh') && (e.dataset.unit || '') === name); if (i < 0) return null; const out = [];
    for (let j = i + 1; j < L.length && L[j].classList.contains('c2row'); j++) out.push(txt(L[j].querySelector('.c2code')) + (L[j].classList.contains('c2ov') ? '(걸침)' : '')); return out; },
  /* 검색(B14) */
  srch(){ const i = document.querySelector('#slot .c2srch'); const w = i && i.closest('.c2srw'); return i ? { ph: i.placeholder, rect: R(i), wrap: R(w), val: i.value, focus: document.activeElement === i } : null; },
  srType(v){ const i = document.querySelector('#slot .c2srch'); if (!i) return false; i.focus(); i.value = v; i.dispatchEvent(new Event('input', { bubbles: true })); return true; },
  async srWait(){ for (let i = 0; i < 60; i++){ await wait(60); const p = document.querySelector('.c2srp'); if (p && p.querySelector('.srh')) { await wait(80); return true; } } return false; },
  srp(){ const p = document.querySelector('.c2srp'); return p ? { k: [...p.querySelectorAll('.srk')].map(txt), on: txt(p.querySelector('.srk.on')), rows: [...p.querySelectorAll('.srr')].map(r => ({ kind: txt(r.querySelector('.qb')), f: txt(r.querySelector('.srf')), s: [...r.querySelectorAll('.srs')].map(txt) })), n: p.querySelectorAll('.srr').length,
    sr0: [...p.querySelectorAll('.sr0')].map(txt), marks: p.querySelectorAll('mark').length, rect: R(p), z: cs(p, 'zIndex') } : null; },
  srKind(t){ const b = [...document.querySelectorAll('.c2srp .srk')].find(x => txt(x).indexOf(t) === 0); return b ? hit(b) : null; },
  srRow(kind, i){ const L = [...document.querySelectorAll('.c2srp .srr')].filter(r => !kind || txt(r.querySelector('.qb')) === kind); const e = L[i || 0]; if (!e) return null; try { e.scrollIntoView({ block: 'nearest' }); } catch (x) {} return Object.assign(hit(e), { f: txt(e.querySelector('.srf')) }); },
  mainTop(){ const m = main(); return m ? m.scrollTop : null; },
  setMainTop(v){ const m = main(); if (m) m.scrollTop = v; return m ? m.scrollTop : null; },
  /* 넘침·화면 밖(B17) · 누름 크기 */
  overflow(){ const m = main(); const de = document.documentElement; const out = [];
    const sel = '#slot .c2row .chip, #slot .c2row button, #slot .c2row .c2dep, #slot .c2row .c2q1, #slot .c2band, #slot .c2uh, #slot .c2rh, #slot .ordseg, #slot .c2sortar, #slot .c2lv, #slot .c2srw, .pop.mpop, .c2missm, .c2lkm, .c2upick, .c2srp, .c2fmenu';
    document.querySelectorAll(sel).forEach(e => { if (!e.getClientRects().length || cs(e, 'display') === 'none') return; const r = e.getBoundingClientRect(); const mr = m ? m.getBoundingClientRect() : { left: 0, right: innerWidth };
      const inMain = m && m.contains(e); const L = inMain ? mr.left : 0, Rr = inMain ? mr.right : innerWidth; if (r.right > Rr + 1 || r.left < L - 1) out.push((String(e.className || e.tagName)).slice(0, 40) + ' ' + Math.round(r.left) + '~' + Math.round(r.right)); });
    return { docW: [de.scrollWidth, de.clientWidth], main: m ? [m.scrollWidth, m.clientWidth] : null, off: out.slice(0, 12), n: out.length }; },
  tapSizes(){ const sel = ['.c2sortar', '.c2lv', '.c2secno', '.c2dep', '.c2q1', '.c2pbtn', '.c2ue', '.c2uadd', '.c2miss', '.c2lnk', '.chip.c-memo', '.pop.mpop .mx', '.pop.mpop .mcl'];
    const o = {}; sel.forEach(s => { const e = [...document.querySelectorAll(s)].find(x => x.getClientRects().length); if (e){ const r = e.getBoundingClientRect(); o[s] = [Math.round(r.width), Math.round(r.height)]; } }); return o; },
  /* 스크롤바(B16) */
  sbar(){ const m = main(); return { main: m ? m.offsetWidth - m.clientWidth : null, c2on: document.body.classList.contains('c2on') }; },
  toastZ(){ const t = document.getElementById('toasts'); return t ? cs(t, 'zIndex') : null; },
  layer(sel){ const e = document.querySelector(sel); return e ? { z: +cs(e, 'zIndex'), pos: cs(e, 'position'), root: e.parentNode === document.body } : null; },
  toastTop(){ const t = [...document.querySelectorAll('#toasts .toast')].pop(); if (!t) return null; const r = t.getBoundingClientRect(); const a = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); return { t: txt(t), on: !!a && (a === t || t.contains(a)), rect: R(t) }; },
  toasts(){ return [...document.querySelectorAll('#toasts .toast')].map(txt); },
  /* 동기화(B-S) */
  syncState(){ return { u: LS('jopangi_sync_u') || {}, gone: LS('jopangi_sync_gone') || {}, keys: (typeof SYNC_KEYS !== 'undefined' ? SYNC_KEYS.slice() : []) }; },
  /* 맞추기 한 판 — 시작 맞추기(recBoot)·4초 뒤 맞추기(recTouch)가 돌고 있으면 syncRecords 가 그냥 돌아온다(recBusy) · 앞뒤로 기다린다.
     걸려 있는 4초 뒤 맞추기(새 기기 c2Migrate 의 lsWrite 등)는 지금 이 판이 같은 일(stampAll + syncRecords)을 하므로 지운다 — 시험 순서 밖에서 올리지 않게 */
  async syncNow(){ const free = async () => { for (let i = 0; i < 600; i++){ let b = false; try { b = !!recBusy; } catch (e) {} if (!b) return true; await wait(25); } return false; };
    await free(); try { clearTimeout(recTouchT); } catch (e) {} try { stampAll(); } catch (e) {} try { await syncRecords(true); } catch (e) { return String(e); } await free();
    return (typeof recLastErr !== 'undefined' ? recLastErr : '') || 'ok'; },
  stamp(){ try { return stampAll(); } catch (e) { return -1; } },
  ls(k){ return LS(k); },
  setLS(k, v){ try { localStorage.setItem(k, JSON.stringify(v)); recDropCache(); PITREC = null; } catch (e) {} return true; },
  /* 판례 깃발 */
  async prec(id){ clean(); await idle(); S.law = '특허법'; S.tab = 'prec'; S.prec = id; S.precTab = '요약'; await render(); await idle(); await wait(600);
    return [...document.querySelectorAll('#slot .pitflag')].filter(e => cs(e, 'display') !== 'none' && e.getClientRects().length).length; },
  async jimun(){ clean(); await idle(); S.law = '특허법'; S.tab = 'jimun'; await render(); await idle(); await wait(600); const m = main(); return { sb: m ? m.offsetWidth - m.clientWidth : null, c2on: document.body.classList.contains('c2on') }; },
  /* 1차객 · 판례 등 다른 탭 */
  hsPop(){ const i = pops().findIndex(p => /📘 해설/.test(txt(p.querySelector('.ph .pt')))); if (i < 0) return null; const p = pops()[i]; return { i: i, t: txt(p.querySelector('.ph .pt')), text: txt(p.querySelector('.pb')).slice(0, 600), w: Math.round(p.getBoundingClientRect().width), mh: cs(p, 'maxHeight'), rect: R(p), hasHs: !!p.querySelector('.c2hs'), why: txt(p.querySelector('.c2hsw')) }; },
  clPop(){ const p = pops().find(q => /^Claude/.test(txt(q.querySelector('.ph .pt')))); return p ? { t: txt(p.querySelector('.ph .pt')), text: txt(p.querySelector('.pb')).slice(0, 300) } : null; },
  qPop(){ const p = pops().find(q => /^⑦/.test(txt(q.querySelector('.ph .pt')))); return p ? { t: txt(p.querySelector('.ph .pt')), rect: R(p) } : null; }
};
})();
