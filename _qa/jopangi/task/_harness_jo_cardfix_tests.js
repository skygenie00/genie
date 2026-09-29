/* _harness_jo_cardfix_tests.js — jo_cardfix(9/27) 하네스 도구(__CF). mbsame 하네스 도구(__HM) · uidmbs2 도구(__UZ) 뒤에 붙는다.
   NEW·BASE 같은 것을 넣는다 — 없는 함수·자리는 빈 값(헛잣대). 누름은 여기서 안 한다(자리만 · 파이썬이 page.mouse · CDP 터치 r22 · WebKit touchscreen). */
(function(){
const wait = ms => new Promise(r => setTimeout(r, ms));
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const vis = e => !!e && e.isConnected && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden' && e.getBoundingClientRect().height > 0;
const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); return { x: +r.left.toFixed(2), y: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2), r: +r.right.toFixed(2), b: +r.bottom.toFixed(2), cx: +(r.left + r.width / 2).toFixed(2), cy: +(r.top + r.height / 2).toFixed(2) }; };
function hitOn(t, noScroll){ if (!t) return null; if (!noScroll){ try{ t.scrollIntoView({ block: 'center', inline: 'nearest' }); }catch(e){} }
  const r = R(t), at = document.elementFromPoint(r.cx, r.cy);
  const onScreen = r.cy > 0 && r.cy < innerHeight && r.cx > 0 && r.cx < innerWidth && r.w > 0 && r.h > 0;
  return Object.assign(r, { on: !!at && (at === t || t.contains(at)) && onScreen, onScreen, vis: vis(t), t: txt(t).slice(0, 60), tag: at ? at.tagName + '.' + String(at.className).slice(0, 40) : null }); }
async function idle(){ for (let i = 0; i < 400 && (typeof busy !== 'undefined' && busy); i++) await wait(25); }
async function until(f, ms){ const t0 = Date.now(); while (Date.now() - t0 < (ms || 8000)){ try{ const v = f(); if (v) return v; }catch(e){} await wait(40); } try{ return f(); }catch(e){ return null; } }
const pops = () => (typeof POPS !== 'undefined' ? POPS : []);
const cs = (e, ks) => { if (!e) return null; const s = getComputedStyle(e), o = {};
  (ks || ['fontSize', 'fontWeight', 'color', 'backgroundColor', 'borderTopWidth', 'borderTopStyle', 'borderTopColor', 'borderLeftWidth', 'borderLeftColor', 'borderTopLeftRadius', 'marginLeft', 'display', 'opacity']).forEach(k => { o[k] = s[k]; }); return o; };
const LS = k => { try{ return JSON.parse(localStorage.getItem(k) || 'null'); }catch(e){ return null; } };
const LSP = (k, v) => localStorage.setItem(k, JSON.stringify(v));
/* 카드 = id qb-<열쇠>(제7판·리담 선지 카드) · 없으면 ID 칩 글이 그 열쇠인 머리의 카드 */
function cardOf(k){
  const c = document.getElementById('qb-' + k); if (c) return c;
  const idc = [...document.querySelectorAll('.qb.id')].find(b => txt(b) === k);
  return idc ? (idc.closest('.qwrap, .oxrow, .uzexb') || idc.parentNode) : null;
}
function headOf(k){ const c = cardOf(k); if (!c) return null; const idc = [...c.querySelectorAll('.qb.id')].find(b => txt(b) === k); return idc ? (idc.closest('.mbqhd') || idc.closest('.qhd')) : c.querySelector('.mbqhd'); }
function lkWin(){ return pops().filter(p => p.isConnected && (p._cflw || /메모 및 유사문제 연결/.test(txt(p.querySelector('.ph'))))).slice(-1)[0] || null; }
function qpWin(k){ return pops().filter(p => p.isConnected && p._pk === 'q|📝 지문 ' + k).slice(-1)[0] || null; }
window.__CF = {
  ls(k){ return LS(k); },
  prep(){ try{ localStorage.removeItem('jopangi.qfix'); }catch(e){} return 1; },
  /* 연결 심기 — {a: [b…]} (옛 v 배열 그대로) */
  seedLk(o){ const K = (typeof LK_KEY !== 'undefined') ? LK_KEY : 'jopangi.link'; const A = {}; Object.keys(o).forEach(a => { A[a] = { v: o[a].slice(), ts: '2026-09-27T01:00:00.000Z' }; });
    LSP(K, A); try{ LKREC = null; }catch(e){} return A; },
  lk(k){ try{ return { my: lkOf(k), back: lkBack(k) }; }catch(e){ return null; } },
  /* §B-1 칩 줄 — 머리 칩 x 차례 · 🔗 판 칩 앞 칩 끝 + gap · 태그 묶음 오른쪽 끝 */
  chipRow(k){
    const hd = headOf(k); if (!hd) return null;
    const all = [...hd.querySelectorAll('button, span.qb, .mbtags, .t')].filter(e => vis(e) && !e.closest('.mbtags') || e.classList.contains('mbtags'));
    const flow = [...hd.children].filter(vis).map(e => ({ t: txt(e).slice(0, 18), cls: String(e.className).slice(0, 30), ml: getComputedStyle(e).marginLeft, ...R(e) }));
    const pan = [...hd.querySelectorAll('.mlnpan')].find(vis), yj = [...hd.querySelectorAll('.mlnyj')].find(vis);
    const prevEnd = e => { if (!e) return null; const sib = [...e.parentNode.children].filter(vis); const i = sib.indexOf(e); const p = i > 0 ? sib[i - 1] : null; return p ? { t: txt(p).slice(0, 14), r: R(p).r, gap: +(R(e).x - R(p).r).toFixed(2), sameRow: Math.abs(R(e).y - R(p).y) < 3 } : null; };
    const tags = hd.querySelector('.mbtags') || [...hd.children].find(e => e.querySelector && e.querySelector('.qtag'));
    return { pan: pan ? { t: txt(pan), ml: getComputedStyle(pan).marginLeft, prev: prevEnd(pan) } : null, yj: yj ? { t: txt(yj), ml: getComputedStyle(yj).marginLeft } : null,
             tags: tags ? { r: R(tags).r, hdR: R(hd).r, ml: getComputedStyle(tags).marginLeft } : null, flow: flow.map(f => f.t + '@' + f.x) };
  },
  /* 연결 단추 자리 — 카드 「✏️ 연결」 */
  lkBtn(k){ const c = cardOf(k); const b = c ? [...c.querySelectorAll('button')].find(x => txt(x) === '✏️ 연결' && vis(x)) : null; return hitOn(b); },
  headLkChip(k){ const hd = headOf(k); const b = hd ? [...hd.querySelectorAll('button')].find(x => /^↩/.test(txt(x))) : null; return b ? Object.assign(hitOn(b), { cs: cs(b), cls: b.className }) : null; },
  lnkLines(k){ const c = cardOf(k); return c ? [...c.querySelectorAll('.lnkline')].map(txt) : null; },
  win(){
    const w = lkWin(); if (!w) return { win: false };
    const ph = w.querySelector('.ph'), inp = w.querySelector('input');
    const rows = [...w.querySelectorAll('.cfrs .cfr, .lnkrow')].filter(vis);
    const cur = [...w.querySelectorAll('.cfcur .cfcr')].filter(vis);
    return { win: true, vis: vis(w), w: Math.round(R(w).w), title: txt(ph).replace(/✕|모두 닫기|닫기/g, '').trim(), chips: [...(ph.querySelectorAll('.cfhc'))].map(txt),
      focus: document.activeElement === inp, inTag: document.activeElement ? document.activeElement.tagName : null,
      rows: rows.map(r => ({ uid: txt(r.querySelector('.cfid')) || txt(r.querySelector('.qb.n')), no: txt(r.querySelector('.cfno')), on: r.classList.contains('on'), op: getComputedStyle(r).opacity, has: /이미 넣음/.test(txt(r)), wh: txt(r.querySelector('.cfwh')) })),
      cur: cur.map(r => ({ uid: txt(r.querySelector('.cfid')), no: txt(r.querySelector('.cfno')), back: !!r.querySelector('.cfbk'), t: txt(r.querySelector('.cftx')).slice(0, 20) })),
      curN: txt(w.querySelector('.cfcl')), foot: txt(w.querySelector('.cfft')), headCs: cs(ph, ['backgroundColor', 'borderBottomColor', 'paddingTop', 'paddingLeft']), winCs: cs(w, ['borderTopColor', 'borderTopLeftRadius', 'backgroundColor', 'borderTopWidth']),
      bodyCs: cs(w.querySelector('.pb'), ['backgroundColor', 'paddingTop', 'paddingLeft']), inpCs: cs(inp, ['borderTopColor', 'backgroundColor', 'fontSize', 'paddingTop', 'borderTopLeftRadius']) };
  },
  winInp(){ const w = lkWin(); const i = w && w.querySelector('input'); return hitOn(i, true); },
  winRowAt(uid, part){ const w = lkWin(); if (!w) return null; const r = [...w.querySelectorAll('.cfrs .cfr')].find(x => txt(x.querySelector('.cfid')) === uid); if (!r) return null;
    const t = part === 'no' ? r.querySelector('.cfno') : (r.querySelector('.cftx') || r); return hitOn(t); },
  winCurX(uid){ const w = lkWin(); if (!w) return null; const r = [...w.querySelectorAll('.cfcur .cfcr')].find(x => txt(x.querySelector('.cfid')) === uid); return r ? hitOn(r.querySelector('.cfxx')) : null; },
  winClose(){ try{ closeAllPops(); }catch(e){} return pops().length; },
  qp(k){ const w = qpWin(k); if (!w) return { win: false }; const go = [...w.querySelectorAll('button')].find(b => /↪/.test(txt(b)));
    return { win: true, vis: vis(w), title: txt(w.querySelector('.ph')).slice(0, 60), go: go ? Object.assign(hitOn(go, true), { cs: cs(go, ['backgroundColor', 'borderTopWidth', 'color', 'fontSize', 'fontWeight']) }) : null }; },
  anyQp(){ return pops().filter(p => p.isConnected && /^q\|📝 지문 /.test(p._pk || '')).map(p => p._pk.slice(6)); },
  /* §B-5 근거 「!」 */
  ggSeed(k, t){ const A = LS('jopangi.gg') || {}; A[k] = [{ k: 'g1', i: 1, t: t || '제29조 신규성', ok: 'o', ts: '2026-09-27T01:00:00.000Z', cs: [] }]; LSP('jopangi.gg', A); try{ GGREC = null; }catch(e){} return A[k]; },
  ggNum(k){ const c = cardOf(k); const n = c ? [...c.querySelectorAll('.ggnum')].find(vis) : null; return n ? Object.assign(hitOn(n), { cs: cs(n, ['borderTopWidth', 'borderTopColor', 'color', 'backgroundColor']) }) : null; },
  ggPan(k){ const c = cardOf(k); const p = c ? c.querySelector('.ggpan') : null; if (!p) return null; const bg = p.querySelector('.hd .bg'); const ta = p.querySelector('.ggcsin textarea');
    return { disp: getComputedStyle(p).display, vis: vis(p), cs: cs(p, ['backgroundColor', 'borderLeftWidth', 'borderLeftColor']), bg: bg ? Object.assign(hitOn(bg, true), { on: bg.classList.contains('on'), cs: cs(bg, ['color', 'fontSize', 'fontWeight', 'borderTopWidth', 'backgroundColor']) }) : null,
             ta: ta ? { v: ta.value, focus: document.activeElement === ta } : null, tColor: getComputedStyle(p.querySelector('.hd .t') || p).color }; },
  ggBang(k){ const c = cardOf(k); const p = c ? c.querySelector('.ggpan') : null; const bg = p ? p.querySelector('.hd .bg') : null; return bg ? hitOn(bg) : null; },
  /* 단원 카드 목록 차례(화면 거름 전 · mokCards) — 열쇠 */
  cardSeq(sel){ const m = /^__mg(\d+)(?:~([nuv]))?$/.exec(sel || ''); if (!m) return null;
    return mokCards(+m[1], m[2] || 'b').map(c => c.kind === 'Z' ? oxKeyLid(c.q, c.z) : oxKeyP7(c.kind === 'O' ? c.o : c.z)); },
  ggTypeCs(k, s){ const c = cardOf(k); const p = c && c.querySelector('.ggpan'); const ta = p && p.querySelector('.ggcsin textarea'); if (!ta) return null; ta.focus(); ta.value = s; return { v: ta.value }; },
  bangOf(k){ const A = LS('jopangi.gg') || {}; return ((A[k] || [])[0] || {}).bang || false; },
  /* §B-6 정정 */
  fixBtn(k){ const c = cardOf(k); const b = c ? [...c.querySelectorAll('button')].filter(x => /^✎ 정정/.test(txt(x)) && vis(x)).find(x => txt(x) === '✎ 정정' || /^✎ 정정 [OX]$/.test(txt(x))) : null; return hitOn(b); },
  fixDone(k, where){ const c = cardOf(k); const bs = c ? [...c.querySelectorAll('button')].filter(x => txt(x) === '✎ 정정됨' && vis(x)) : []; const b = where === 'head' ? bs.find(x => x.closest('.mbqhd')) : bs.find(x => !x.closest('.mbqhd')); return b ? hitOn(b) : null; },
  peek(k){ const c = cardOf(k); const b = c ? [...c.querySelectorAll('.mbpeek')].find(vis) : null; return hitOn(b); },
  expShown(k){ const c = cardOf(k); const e = c ? [...c.querySelectorAll('.mbexp')].pop() : null; return !!e && vis(e); },
  fixPanel(k){ const c = cardOf(k); const p = c ? c.querySelector('.cffix') : null; if (!p) return { on: false };
    const tas = [...p.querySelectorAll('textarea')];
    return { on: vis(p), cs: cs(p, ['backgroundColor', 'borderTopColor']), n: tas.length, q: tas[0] && tas[0].value.slice(0, 30), exp: tas[1] && tas[1].value.slice(0, 40), cas: tas[2] && tas[2].value.slice(0, 20),
             orig: txt(p.querySelector('.cffo')), picked: [...p.querySelectorAll('.cfab')].filter(b => /\b(o|x)\b/.test(b.className)).map(txt) }; },
  fixPick(k, v){ const c = cardOf(k); const b = c ? [...c.querySelectorAll('.cffix .cfab')].find(x => txt(x) === v) : null; return hitOn(b); },
  fixSave(k){ const c = cardOf(k); const b = c ? c.querySelector('.cffix .cfsv') : null; return hitOn(b); },
  fixUnset(k){ const c = cardOf(k); const b = c ? c.querySelector('.cffix .cfun') : null; return hitOn(b); },
  fixExpSet(k, s){ const c = cardOf(k); const tas = c ? [...c.querySelectorAll('.cffix textarea')] : []; if (!tas[1]) return null; tas[1].value = s; return tas[1].value; },
  expText(k){ const c = cardOf(k); const e = c ? [...c.querySelectorAll('.mbexp')].pop() : null; return e ? { vis: vis(e), t: txt(e).slice(0, 160), orig: txt(e.querySelector('.cffo2')).slice(0, 120) } : null; },
  oxBtn(k, v){ const c = cardOf(k); const b = c ? [...c.querySelectorAll('.mbboxb, .mboxb')].find(x => txt(x) === v && vis(x)) : null; return hitOn(b); },
  rec(k){ try{ return oxOf(k); }catch(e){ return null; } },
  fixState(k){ try{ return { ansfix: (fixAll() || {})[k] || null, qfix: (LS('jopangi.qfix') || {})[k] || null, ans: oxAns(k, '') }; }catch(e){ return null; } },
  headFixN(){ const s = [...document.querySelectorAll('#slot .mbhd .dl')].find(x => /✎ 정정/.test(txt(x))); return s ? Object.assign(hitOn(s), { n: +(/(\d+)/.exec(txt(s)) || [0, 0])[1] }) : null; },
  fixListWin(){ const p = pops().filter(x => x.isConnected && /정정 목록/.test(x._pk || '')).pop(); return p ? { vis: vis(p), rows: [...p.querySelectorAll('.cffr .cfid')].map(txt) } : null; },
  /* §B-7 판례 줄 */
  panLine(k){ const c = cardOf(k); const bs = c ? [...c.querySelectorAll('.mbexp button, .mbexp span')].filter(x => /^🏛/.test(txt(x))) : []; const b = bs.find(vis) || bs[0];
    return b ? { t: txt(b), vis: vis(b), cs: cs(b, ['borderTopLeftRadius', 'backgroundColor', 'borderTopWidth', 'color', 'fontSize', 'fontWeight']), same: /같은 지문/.test(txt(c.querySelector('.mbexp'))) } : null; },
  /* §B-8 유제 */
  unitOrder(sel){ return [...document.querySelectorAll('#slot .qwrap .qb.id, #slot .mbq .qb.id')].filter(vis).map(txt); },
  yjChip(){ return [...document.querySelectorAll('#slot .mlnyj')].filter(vis).length; },
  /* §B-9 미분류 */
  unk(){ try{ const JM = { 문제: VJ.qs }; const keys = uzUnkKeys(VJ.qs, VJ.M); const card = new Set();
      if (MLN && MLN.ok) VJ.M.forEach((n, i) => MLN_LNS.forEach(ln => mlnKeys(VJ.M, i, ln, VJ.P7map, VJ.byId).forEach(k => card.add(k))));
      const both = keys.filter(k => card.has(k));
      return { n: keys.length, both: both.length, bothEx: both.slice(0, 5) }; }catch(e){ return { err: String(e).slice(0, 120) }; } },
  unkRaw(){ try{ const placed = new Set(); VJ.M.forEach(n => (n.리담 || []).forEach(x => placed.add(x))); let n = 0, ab = 0; const seen = new Set();
      VJ.qs.filter(q => !placed.has(q.id)).forEach(q => (q.지문 || []).forEach(z => { const k = oxKeyLid(q, z); if (seen.has(k)) return; seen.add(k); n++; if (MLN && MLN.p7uid && z.uid && MLN.p7uid.has(z.uid)) ab++; }));
      return { n: n, absorbed: ab }; }catch(e){ return { err: String(e).slice(0, 120) }; } },
  unkChip(){ const b = [...document.querySelectorAll('#slot .mbhm .hmscs .hmsc')].find(x => /미분류/.test(txt(x))); return b ? { t: txt(b), n: +(txt(b.querySelector('b')).replace(/,/g, '') || -1) } : null; },
  unkDrawer(){ const r = [...document.querySelectorAll('#jtlist .jtit, #jtlist .jtch')].find(x => /미분류/.test(txt(x))); return r ? { t: txt(r).slice(0, 40), n: +(txt(r.querySelector('.n')).replace(/,/g, '') || -1), vis: vis(r) } : null; },
  unkCard(){ const c = [...document.querySelectorAll('#slot .mbdash > .mbsj')].find(x => /미분류/.test(txt(x.querySelector('.hd')))); const m = c ? /총 (\d+)/.exec(txt(c.querySelector('.hd .tot'))) : null; return m ? +m[1] : null; },
  errs(){ return (window.__ERR || []).filter(e => !/^ResizeObserver loop/.test(e)).slice(0, 20); }
};
})();
