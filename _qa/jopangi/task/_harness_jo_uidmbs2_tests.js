/* _harness_jo_uidmbs2_tests.js — uid_add2 + mbsame_add2 + mbsame_add3(9/27 한 판) 하네스 도구(__UZ).
   mbsame 하네스 도구(__HM) 뒤에 붙는다 · BASE(genie 539131a)·NEW 같은 것을 넣는다 — 없는 함수는 빈 값(헛잣대).
   ⚠ 누름은 여기서 안 한다 — 자리만 돌려주고 파이썬이 page.mouse · CDP 터치 r22 · WebKit touchscreen 으로 누른다. */
(function(){
const wait = ms => new Promise(r => setTimeout(r, ms));
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const has = n => { try{ return typeof eval(n) !== 'undefined'; }catch(e){ return false; } };
const vis = e => !!e && e.isConnected && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden' && e.getBoundingClientRect().height > 0;
const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); return { x: +r.left.toFixed(2), y: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2), cx: +(r.left + r.width / 2).toFixed(2), cy: +(r.top + r.height / 2).toFixed(2) }; };
function hitOn(t){ if (!t) return null; try{ t.scrollIntoView({ block: 'center', inline: 'nearest' }); }catch(e){}
  const r = R(t), at = document.elementFromPoint(r.cx, r.cy);
  const onScreen = r.cy > 0 && r.cy < innerHeight && r.cx > 0 && r.cx < innerWidth && r.w > 0 && r.h > 0;
  return Object.assign(r, { on: !!at && (at === t || t.contains(at)) && onScreen, onScreen, vis: vis(t), t: txt(t).slice(0, 60), tag: at ? at.tagName + '.' + at.className : null }); }
async function idle(){ for (let i = 0; i < 400 && (typeof busy !== 'undefined' && busy); i++) await wait(25); }
async function until(f, ms){ const t0 = Date.now(); while (Date.now() - t0 < (ms || 8000)){ try{ const v = f(); if (v) return v; }catch(e){} await wait(40); } try{ return f(); }catch(e){ return null; } }
const pops = () => (typeof POPS !== 'undefined' ? POPS : []);
const cs = (e, ks) => { if (!e) return null; const s = getComputedStyle(e), r = e.getBoundingClientRect(), o = {};
  (ks || ['fontSize', 'fontWeight', 'color', 'backgroundColor', 'borderTopColor', 'borderTopStyle', 'borderTopWidth', 'paddingTop', 'paddingLeft', 'borderTopLeftRadius']).forEach(k => { o[k] = s[k]; });
  o.h = Math.round(r.height * 10) / 10; return o; };
window.__UZ = {
  has(n){ return has(n); },
  /* 첫 화면 — 기출/기타 · 히트맵 칩 · 편 카드 머리 · 서랍 머리 */
  async gk(v){ if (has('UZGK')) UZGK = v; await idle(); await render(); await idle(); await wait(200); return has('UZGK') ? UZGK : null; },
  hm(){ const sc = document.querySelector('#slot .mbhm .hmscs'); if (!sc) return null;
    return { chips: [...sc.children].map(c => ({ t: txt(c), on: c.classList.contains('on'), gk: c.dataset ? (c.dataset.uzgk || '') : '', tag: c.tagName })),
             legend: [...document.querySelectorAll('#slot .mbhm .hmhd .hmlg')].map(txt), head: txt(document.querySelector('#slot .mbhd .dl')) }; },
  gkAt(v){ const b = document.querySelector('#slot .mbhm .hmscs [data-uzgk="' + v + '"]'); return b ? hitOn(b) : null; },
  sepInRow(){ const sc = document.querySelector('#slot .mbhm .hmscs'), s = sc && sc.querySelector('.uzgksep'), g = sc && sc.querySelector('[data-uzgk="g"]'), last = sc && [...sc.querySelectorAll('.hmsc')].filter(x => !x.dataset.uzgk).pop();
    if (!s || !g || !last) return null; const a = last.getBoundingClientRect(), b = s.getBoundingClientRect(), c = g.getBoundingClientRect();
    return { sameRow: Math.abs(a.top - c.top) < 2 || c.left > b.left, sepColor: getComputedStyle(s).color, sepFs: getComputedStyle(s).fontSize, order: b.left > a.left - 1 && c.left > b.left }; },
  cards(){ return [...document.querySelectorAll('#slot .mbdash > .mbsj')].map(c => { const h = c.querySelector(':scope > .hd h2'); const so = c.querySelector('.mbur.mbsolo');
    return { t: h ? txt(h) : ('[solo] ' + txt(so)), tot: h ? txt(h.querySelector('.tot')) : txt(so && so.querySelector('.tot')), arrow: h ? txt(h.querySelector('.uztar')) : null, rows: c.querySelectorAll('.mbur').length }; }); },
  cardTot(no){ const c = [...document.querySelectorAll('#slot .mbdash > .mbsj')].find(x => { const b = x.querySelector(':scope > .hd h2 b'); return b && txt(b) === String(no); });
    if (!c) { const so = [...document.querySelectorAll('#slot .mbur.mbsolo')].find(r => new RegExp('^' + no + ' ').test(txt(r.querySelector('.nm')))); return so ? (+(/총 (\d+)/.exec(txt(so.querySelector('.tot'))) || [0, -1])[1]) : null; }
    const m = /총 (\d+)/.exec(txt(c.querySelector(':scope > .hd .tot'))); return m ? +m[1] : null; },
  drawerHead(nm){ const r = [...document.querySelectorAll('#jtlist .jtch')].find(x => txt(x.querySelector('.jtnm')) === nm); return r ? +txt(r.querySelector(':scope > .n')) : null; },
  /* 서랍 편 줄 수 — 편 번호로(자식 있는 편 = .jtch · 한 줄 편(12 실용신안) = .jtit 로 그려진다) */
  drawerTop(no){ const rx = new RegExp('^' + no + '\\.?\\s'); const rs = [...document.querySelectorAll('#jtlist .jtch, #jtlist .jtit')].filter(x => rx.test(txt(x.querySelector('.jtnm, .tx'))));
    if (!rs.length) return null;   /* 한 줄 편은 머리 없이 줄(본편 · (미수록) · (변형) …)로만 선다 → 그 편 줄 합 */
    return rs.reduce((s, r) => { const n = r.querySelector(':scope > .n') || r.querySelector('.n'); return s + (n ? +txt(n).replace(/,/g, '') : 0); }, 0); },
  drawerLeaf(nm){ const r = [...document.querySelectorAll('#jtlist .jtit')].find(x => txt(x.querySelector('.tx')) === nm); return r ? { n: txt(r.querySelector('.n')), vis: vis(r) } : null; },
  hmChip(re){ const rx = new RegExp(re); const b = [...document.querySelectorAll('#slot .mbhm .hmscs .hmsc')].find(x => rx.test(txt(x))); return b ? { t: txt(b), n: +(txt(b.querySelector('b')).replace(/,/g, '') || -1) } : null; },
  rowTot(nm){ const r = [...document.querySelectorAll('#slot .mbur')].find(x => txt(x.querySelector('.nm')) === nm); if (!r) return null;
    const m = /총 (\d+)문제/.exec(txt(r)); return { tot: m ? +m[1] : null, none: /문항 없음/.test(txt(r)), jn: !!r.querySelector('.mbchip.jn'), vis: vis(r) }; },
  rowAt(nm, sel){ const r = [...document.querySelectorAll('#slot .mbur')].find(x => txt(x.querySelector('.nm')) === nm); const e = r && (sel ? r.querySelector(sel) : r); return e ? hitOn(e) : null; },
  giCardN(){ return document.querySelectorAll('#slot .mbur[data-giy]').length; },
  unkCard(){ return [...document.querySelectorAll('#slot .mbsj .hd h2')].some(h => /미분류/.test(txt(h))); },
  drawerGi(){ return [...document.querySelectorAll('#jtlist .jtit')].filter(x => /^\d{4}년/.test(txt(x.querySelector('.tx')))).length; },
  /* 필터 — 단추 · 목록 · 빈칸 종류 */
  fbtn(){ const b = document.querySelector('#slot .mbqr .uzfb'); if (b) return Object.assign(hitOn(b), { kind: 'btn' });
    const s = document.querySelector('#slot .mbqr select'); return s ? Object.assign(hitOn(s), { kind: 'select' }) : null; },
  fmenu(){ const m = document.querySelector('#slot .mbqr .uzfm'); if (!m) return null;
    return { vis: vis(m), opts: [...m.querySelectorAll('.uzfo')].map(o => txt(o)), sep: !!m.querySelector('.uzfsep'), bk: [...m.querySelectorAll('.uzfc')].map(c => ({ t: txt(c), vis: vis(c), on: c.querySelector('input').checked, color: getComputedStyle(c.querySelector('span')).color })), note: txt(m.querySelector('.uzfn')) }; },
  fopt(k){ const o = document.querySelector('#slot .mbqr .uzfo[data-uzty="' + k + '"]'); return o ? hitOn(o) : null; },
  fbk(k){ const o = document.querySelector('#slot .mbqr .uzfc[data-uzbk="' + k + '"]'); return o ? hitOn(o) : null; },
  label(){ const l = document.querySelector('#slot .mbqr .lb'); return txt(l); },
  step(){ const s = document.querySelector('#slot .mbqr .uzstep'); if (!s) return null; const c = getComputedStyle(s);
    return Object.assign(hitOn(s), { n: document.querySelectorAll('#slot .mbqr .uzstep').length, bw: c.borderTopWidth, bs: c.borderTopStyle, bg: c.backgroundColor, fs: c.fontSize, fw: c.fontWeight, color: c.color }); },
  topArrow(no){ const c = [...document.querySelectorAll('#slot .mbdash > .mbsj')].find(x => { const b = x.querySelector(':scope > .hd h2 b'); return b && txt(b) === String(no); }); const a = c && c.querySelector(':scope > .hd h2 .uztar'); return a ? hitOn(a) : null; },
  cardBody(no){ const c = [...document.querySelectorAll('#slot .mbdash > .mbsj')].find(x => { const b = x.querySelector(':scope > .hd h2 b'); return b && txt(b) === String(no); });
    return c ? { rows: [...c.querySelectorAll('.mbur')].filter(vis).length, arrow: txt(c.querySelector(':scope > .hd h2 .uztar')) } : null; },
  depthVis(no){ const i = __HM.nodeIdx(no), M = VJ.M, d = M[i].깊이, rows = [...document.querySelectorAll('#slot .mbur, #slot .mbch > .hh')], out = { d2: 0, d3: 0, d4: 0 };
    const nm2d = {}; for (let j = i + 1; j < M.length && M[j].깊이 > d; j++){ const n = M[j]; nm2d[(n.no ? n.no + (n.깊이 === 1 ? '. ' : ' ') : '') + n.제목] = n.깊이; }
    rows.forEach(r => { const nm = txt(r.querySelector('.nm')).replace(/ \((미수록|변형|판신설)\)$/, ''); const dd = nm2d[nm]; if (!dd || !vis(r)) return; if (dd === 2) out.d2++; else if (dd === 3) out.d3++; else out.d4++; });
    return out; },
  nameX(nm){ const r = [...document.querySelectorAll('#slot .mbur, #slot .mbch > .hh')].find(x => txt(x.querySelector('.nm')) === nm); const n = r && r.querySelector('.nm');
    const card = r && r.closest('.mbsj'); return n && card ? Math.round((n.getBoundingClientRect().left - card.getBoundingClientRect().left) * 10) / 10 : null; },
  drawerTopArrow(nm){ const r = [...document.querySelectorAll('#jtlist .jtch')].find(x => txt(x.querySelector('.jtnm')) === nm); return r ? txt(r.querySelector('.jtar')) : null; },
  /* 정리 창 */
  jn(re){ const rx = new RegExp(re || '정리'); const p = pops().filter(x => rx.test(x._pk || '')).pop(); if (!p) return null; const r = p.getBoundingClientRect();
    return { w: Math.round(r.width), h: Math.round(r.height), sub: txt(p.querySelector('.mbps')), heads: [...p.querySelectorAll('.jnh2')].map(txt), rows: p.querySelectorAll('.jnr').length,
             kids: [...p.querySelectorAll('.jn2 > *')].slice(0, 14).map(x => ({ c: x.className, t: txt(x).slice(0, 90), k: x.dataset ? (x.dataset.jnrow || x.dataset.jnstem || '') : '' })),
             empty: txt(p.querySelector('.jn0')), tg: cs(p.querySelector('.jnxtg'), ['fontSize', 'fontWeight', 'color', 'backgroundColor', 'borderTopColor', 'borderTopLeftRadius']) }; },
  jnFirstRow(re){ const rx = new RegExp(re || '정리'); const p = pops().filter(x => rx.test(x._pk || '')).pop(); const r = p && p.querySelector('.jnr'); if (!r) return null; const top = r.querySelector('.jntop');
    const kids = [...top.children].map(x => ({ c: x.className, t: txt(x).slice(0, 30) }));
    const rec = top.querySelector('.jnrecw') || top.querySelector('.mbrec'); const tr = top.getBoundingClientRect(), rr = rec ? rec.getBoundingClientRect() : null;
    return { kids, recRight: rr ? Math.round(tr.right - rr.right) : null, recText: txt(rec), noneStyle: cs(top.querySelector('.jnnone'), ['fontSize', 'color']), id: cs(top.querySelector('.qb.id'), ['fontSize', 'fontWeight', 'color', 'backgroundColor']),
             no: cs(top.querySelector('.jnno'), ['fontSize', 'fontWeight', 'color']), src: cs(top.querySelector('.jnsrc'), ['fontSize', 'fontWeight', 'color']) }; },
  jnStem(re, k){ const rx = new RegExp(re || '정리'); const p = pops().filter(x => rx.test(x._pk || '')).pop(); if (!p) return null;
    const row = p.querySelector('.jnr[data-jnrow="' + k + '"]'); if (!row) return { row: false }; const prev = row.previousElementSibling;
    return { row: true, stem: prev && prev.classList.contains('jnstem') ? txt(prev) : null, vis: prev ? vis(prev) : false, style: prev && prev.classList.contains('jnstem') ? cs(prev, ['fontSize', 'fontWeight', 'color', 'backgroundColor', 'borderTopColor', 'borderTopWidth', 'paddingTop', 'paddingLeft']) : null }; },
  /* 카드 칩 — 열쇠의 ID 칩이 든 칩 줄(단원 카드 · 미분류 문항 카드 · 기출뷰 지문 칸 어디든) */
  chipRow(k){ const idc = [...document.querySelectorAll('.qb.id')].find(b => txt(b) === k); if (!idc) return null; const hd = idc.closest('.mbqhd') || idc.closest('.qhd'); if (!hd) return null;
    const ty = hd.querySelector('.mbtype'), yr = hd.querySelector('.jxec'), mc = hd.querySelector('.mcchip') || [...hd.querySelectorAll('button')].find(b => /^🃏/.test(txt(b))), sr = hd.querySelector('.qb.v');
    return { type: cs(ty), typeT: txt(ty), typeCls: ty ? ty.className : '', bk: ty && ty.querySelector('.seg.bk') ? { t: txt(ty.querySelector('.seg.bk')), cls: ty.querySelector('.seg.bk').className, deco: getComputedStyle(ty.querySelector('.seg.bk')).textDecorationStyle, color: getComputedStyle(ty.querySelector('.seg.bk')).color } : null,
             year: cs(yr), yearT: txt(yr), mc: cs(mc), mcT: txt(mc), src: cs(sr), srcT: txt(sr), id: cs(idc), idT: txt(idc), font: getComputedStyle(idc).fontFamily.slice(0, 30), stars: [...hd.querySelectorAll('.qtag')].filter(b => txt(b) === '⭐').length }; },
  bkAt(k){ const idc = [...document.querySelectorAll('.qb.id')].find(b => txt(b) === k); const hd = idc && (idc.closest('.mbqhd') || idc.closest('.qhd')); const b = hd && hd.querySelector('.mbtype .seg.bk'); return b ? hitOn(b) : null; },
  bkPopBtn(v){ const p = pops().filter(x => /빈칸 종류 확정/.test(x._pk || '')).pop(); const b = p && p.querySelector('[data-bkv="' + v + '"]'); return b ? hitOn(b) : null; },
  bkRec(k){ return has('bktAll') ? (bktAll()[k] || null) : null; },
  bkOmr(){ return has('BKTOMR') ? BKTOMR : null; },
  async bkLoad(){ if (has('bktOmrLoad')) await bktOmrLoad(); return has('BKTOMR') ? Object.keys(BKTOMR || {}).length : null; },
  /* 단원 찾기 — 열쇠가 든 첫 줄(필터·기출/기타 거친 뒤) */
  selOfKey(k){ if (!(has('MLN') && MLN.ok)) return null; const M = VJ.M; for (let i = 0; i < M.length; i++) for (const ln of ['b', 'n', 'u', 'v']){ if (mlnKeys(M, i, ln, VJ.P7map, VJ.byId).indexOf(k) >= 0) return (typeof mlnSel === 'function' ? mlnSel(i, ln) : '__mg' + i); }
    const placed = new Set(); M.forEach(n => (n.리담 || []).forEach(x => placed.add(x)));
    return (VJ.qs || []).some(q => !placed.has(q.id) && (q.지문 || []).some(z => oxKeyLid(q, z) === k)) ? '__미분류' : null; },
  /* 기출뷰 */
  exv(){ const h = document.querySelector('#slot .mbsbar'); const ps = [...document.querySelectorAll('#slot .exv-q')];
    return { head: txt(h), headKids: h ? [...h.querySelectorAll('.t1,.t2,.pg,button')].map(txt) : [], modebar: document.querySelectorAll('#slot .main > .modebar').length,
             qs: ps.map(q => ({ no: q.dataset.exno, head: txt(q.querySelector('.exv-head')).slice(0, 60), boxes: q.querySelectorAll('.question-box').length, sel: txt(q.querySelector('.exv-sel')), stars: [...q.querySelectorAll('.qtag')].filter(b => txt(b) === '⭐').length,
               noStyle: cs(q.querySelector('.exv-no'), ['fontSize', 'fontWeight']), pre: q.querySelectorAll('.exv-pre:not(.exv-hide)').length, oxRows: [...q.querySelectorAll('.exv-post-ox')].filter(vis).length, chipRows: [...q.querySelectorAll('.question-box .mbqhd')].filter(vis).length })),
             pill: [...document.querySelectorAll('#slot .mbbar')].map(txt), oldBoxes: document.querySelectorAll('#slot .gich, #slot .ginum').length, giCards: document.querySelectorAll('[id^="gi-"]').length }; },
  exvNum(no, n){ const q = document.querySelector('#slot .exv-q[data-exno="' + no + '"]'); const b = q && q.querySelector('.exv-num.exv-lab[data-exn="' + n + '"], .exv-opt[data-exn="' + n + '"]'); return b ? hitOn(b) : null; },
  exvNumState(no, n){ const q = document.querySelector('#slot .exv-q[data-exno="' + no + '"]'); const b = q && q.querySelector('.exv-num[data-exn="' + n + '"], .exv-opt[data-exn="' + n + '"] .exv-num'); return b ? { sel: b.classList.contains('sel'), bg: getComputedStyle(b).backgroundColor } : null; },
  exvNext(){ const b = document.querySelector('#slot [data-uzexnext]'); return b ? hitOn(b) : null; },
  exvGradeBtn(){ const b = document.querySelector('#slot [data-uzexgrade]'); return b ? hitOn(b) : null; },
  exvPeek(no){ const q = document.querySelector('#slot .exv-q[data-exno="' + no + '"]'); const b = q && q.querySelector('.exv-peek'); return b ? hitOn(b) : null; },
  exvHeadBtn(re){ const rx = new RegExp(re); const b = [...document.querySelectorAll('#slot .mbsbar button')].find(x => rx.test(txt(x))); return b ? hitOn(b) : null; },
  drawerYears(){ return [...document.querySelectorAll('#jtlist .jtit')].map(r => ({ t: txt(r.querySelector('.tx')), n: txt(r.querySelector('.n')), now: !!r.querySelector('.now'), bar: !!r.querySelector('.jdbar') })).filter(x => /^\d{4}년/.test(x.t)); },
  drawerTree(){ return document.querySelectorAll('#jtlist .jtch').length; },
  /* 기출 해 줄 · 회독 상자 · 비교 창 */
  grBoxAt(y, i){ const r = document.querySelector('#slot .mbur[data-giy="' + y + '"]'); const b = r && r.querySelectorAll('.grbx')[i || 0]; return b ? Object.assign(hitOn(b), { tag: b.tagName }) : null; },
  grRow(y){ const r = document.querySelector('#slot .mbur[data-giy="' + y + '"]'); if (!r) return null; return { boxes: [...r.querySelectorAll('.grbx')].map(b => ({ t: txt(b), tag: b.tagName, l2: [...b.querySelectorAll('.l2 > span')].map(txt) })), go: txt(r.querySelector('.mbgo')), run: txt(r.querySelector('.grrun')) }; },
  cmp(){ const p = pops().filter(x => /회독별 비교/.test(x._pk || '')).pop(); if (!p) return null; return { vis: vis(p), rounds: p.querySelectorAll('.uzgcr').length, chips: p.querySelectorAll('.uzgcc').length, t: txt(p).slice(0, 200) }; },
  giRecs(y){ return { gi: Object.keys((typeof giAll === 'function' ? giAll() : {}) || {}).filter(k => k.indexOf(PLAW() + ':' + y + ':') === 0).length, year: typeof giYearOf === 'function' ? giYearOf(y) : null,
    rounds: typeof grndAll === 'function' ? (grndAll()[giYKey(y)] || null) : null }; },
  seedGi(y, yrec, gis){ const G = giAll(); Object.keys(gis).forEach(k => { G[k] = gis[k]; }); GIREC = G; lsWrite(GI_KEY, G, '하네스'); const Y = giYAll(); Y[giYKey(y)] = yrec; GIYREC = Y; lsWrite(GIY_KEY, Y, '하네스');
    if (typeof grndAll === 'function'){ const A = grndAll(); delete A[giYKey(y)]; GRNDREC = A; lsWrite(GRND_KEY, A, '하네스'); } return true; },
  seedGround(y, recs){ const A = grndAll(); A[giYKey(y)] = recs; GRNDREC = A; lsWrite(GRND_KEY, A, '하네스'); return true; },
  /* 시험지 띠·이어짐(⑩) — 해 색인에서 문번 n 선지 opt 띠 · 이어짐 */
  async band(law, y, n, opt){ if (!has('jxeIndex')) return null; const rec = await jxeIndex(JXE_LAWF[law], jxeFile(law, y)); const bx = jxeBox(rec, n); if (!bx) return { box: null };
    const b = has('uzBand') ? uzBand(bx.body, opt, '') : jxeBand(bx.body, opt, ''); const cut = has('uzCut') ? uzCut(rec, n) : bx.cut;
    const optY = []; bx.body.forEach(l => { const t = l.t.replace(/^\s+/, ''); if (/^[①②③④⑤]/.test(t)) optY.push([t[0], +l.y0.toFixed(3), +l.y1.toFixed(3)]); });
    return { band: b ? { y0: +b.y0.toFixed(3), y1: +b.y1.toFixed(3) } : null, cut: !!cut, opts: optY, page: bx.page }; },
  async cutAll(law, y){ if (!has('jxeIndex')) return null; const rec = await jxeIndex(JXE_LAWF[law], jxeFile(law, y)); const out = {};
    Object.keys(rec.no).forEach(n => { const bx = jxeBox(rec, +n); out[n] = { cut: has('uzCut') ? uzCut(rec, +n) : !!(bx && bx.cut), p: rec.no[n].p, nxp: rec.no[n].nx >= 0 ? rec.lines[rec.no[n].nx].p : null }; }); return out; },
  toasts(){ return (window.__TOASTS || []).slice(-6); },
  toastClear(){ window.__TOASTS = []; return 0; },
  syncKeys(){ return typeof SYNC_KEYS !== 'undefined' ? SYNC_KEYS.slice() : null; },
  ls(k){ try{ return JSON.parse(localStorage.getItem(k) || 'null'); }catch(e){ return null; } },
  lsPut(k, v){ localStorage.setItem(k, JSON.stringify(v)); try{ recDropCache(); }catch(e){} return true; },
  migLast(){ return typeof UIDMIG_LAST !== 'undefined' ? UIDMIG_LAST : null; },
  async migRun(){ if (typeof uidMigrateBoot !== 'function') return null; try{ return await uidMigrateBoot(); }catch(e){ return 'err ' + e; } },
  pitHas(k){ return !!(typeof pitAll === 'function' && pitAll()[k]); },
  pitKeys(pre){ return typeof pitAll === 'function' ? Object.keys(pitAll()).filter(k => k.indexOf(pre) === 0) : null; },
  pitFlag(k){ const idc = [...document.querySelectorAll('.qb.id')].find(b => txt(b) === k); const box = idc && (idc.closest('.oxrow') || idc.closest('.qwrap') || idc.closest('.question-box')); const f = box && box.querySelector('.pitflag'); return f ? Object.assign(hitOn(f), { vis: vis(f) }) : null; },
  star(k){ const idc = [...document.querySelectorAll('.qb.id')].find(b => txt(b) === k); const hd = idc && (idc.closest('.mbqhd') || idc.closest('.qhd')); const b = hd && [...hd.querySelectorAll('.qtag')].find(x => txt(x) === '⭐'); return b ? { on: b.classList.contains('on'), vis: vis(b), filter: getComputedStyle(b).filter } : null; },
  srch(q){ S.oxQ = q; S.oxQMode = 'q'; if (typeof mbSearchRun === 'function') mbSearchRun(); const box = document.querySelector('#slot .mbres'); return box ? [...box.querySelectorAll('.rr')].map(r => ({ t: txt(r).slice(0, 80), badge: [...r.querySelectorAll('.srcb')].map(txt) })) : null; },
  cardP7(id){ const z = VJ.P7map[id]; if (!z) return null; const k = oxKeyP7(z); const c = document.getElementById('qb-' + k); return { key: k, ox: z.ox, 답: z.답 || null, card: !!c, vis: vis(c), t: txt(c).slice(0, 160) }; },
  obj(id){ const o = (has('MLN') && MLN.obj || {})[id]; return o ? { 답: o.답, uid: o.uid } : null; },
  p7(id){ const z = VJ.P7map[id]; return z ? { ox: z.ox, uid: z.uid, 책번호: z.책번호, 문항: z.문항 || null } : null; },
  boxes(){ if (!has('mlnBoxL')) return null; let n = 0, qs = 0; (VJ.qs || []).forEach(q => { qs++; try{ if (mlnBoxL(q)) n++; }catch(e){} }); return { boxy: n, qs: qs }; },
  boxOf(qid){ const q = VJ.byId[qid]; return q && has('mlnBoxL') ? mlnBoxL(q) : null; }
};
})();
