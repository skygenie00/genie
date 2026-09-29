/* _harness_jo_revfix0928_tests.js — jo_revfix0928(9/28) 하네스 도구(__RV). __HM · __UZ · __CF · __JS · __WM 뒤에 붙는다.
   NEW·BASE 같은 것을 넣는다 — 없는 함수·자리는 빈 값(헛잣대). 누름은 여기서 안 한다(자리만 · 파이썬이 page.mouse · CDP 터치 r22 · CDP 펜 · WebKit touchscreen).
   보임 = computed display ≠ none · 높이 > 0 · 「보인다」 = 가운데 점이 화면 안이고 elementFromPoint 가 그 요소(창 안이면 창 위·아래 안). */
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
const has = n => { try{ return typeof eval(n) !== 'undefined'; }catch(e){ return false; } };
const cs = (e, ks) => { if (!e) return null; const s = getComputedStyle(e), o = {}; ks.forEach(k => { o[k] = s[k]; }); const r = e.getBoundingClientRect(); o.h = Math.round(r.height * 10) / 10; o.w = Math.round(r.width * 10) / 10; return o; };
const VB = () => { const v = window.visualViewport; return (v && v.width > 0) ? { x: v.offsetLeft || 0, y: v.offsetTop || 0, w: v.width, h: v.height } : { x: 0, y: 0, w: innerWidth, h: innerHeight }; };
const inside = (a, W) => a.x >= W.x - 0.5 && a.r <= W.r + 0.5 && a.y >= W.y - 0.5 && a.b <= W.b + 0.5;
/* 보인다 — 가운데 점이 화면 안 · elementFromPoint = 그 요소 · (창이 있으면) 가운데 점이 창 위·아래 안 */
function seen(e, win){ if (!e || !vis(e)) return false; const r = R(e);
  if (!(r.cy > 0 && r.cy < innerHeight && r.cx > 0 && r.cx < innerWidth)) return false;
  const at = document.elementFromPoint(r.cx, r.cy); if (!(at && (at === e || e.contains(at)))) return false;
  if (win){ const W = R(win); if (!(r.cy >= W.y && r.cy <= W.b)) return false; }
  return true; }
function lkWin(){ return pops().filter(p => p.isConnected && p._cflw).slice(-1)[0] || null; }
const EXCS = ['fontSize', 'fontWeight', 'color', 'backgroundColor', 'borderTopWidth', 'borderTopStyle', 'borderTopColor', 'borderTopLeftRadius', 'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft', 'boxShadow'];
window.__RV = {
  vb(){ return VB(); },
  errs(){ return (window.__ERR || []).filter(e => !/^ResizeObserver loop/.test(e)).slice(0, 20); },
  /* ── A-1 연결 창 ── */
  cf(){ const w = lkWin(); if (!w) return { win: false };
    const W = R(w), B = VB(), bd = w.querySelector(':scope > .pb');
    const rows = [...w.querySelectorAll('.cfrs .cfr')].filter(vis), cur = [...w.querySelectorAll('.cfcur .cfcr')].filter(vis), ft = w.querySelector('.cfft');
    return { win: true, W: W, B: B, mh: w.style.maxHeight, cmh: getComputedStyle(w).maxHeight, cls: String(w.className),
      inScreen: W.y >= B.y + 8 - 1 && W.b <= B.y + B.h - 8 + 1 && W.x >= B.x - 0.5 && W.r <= B.x + B.w + 0.5,
      rowsN: rows.length, uids: rows.map(r => txt(r.querySelector('.cfid'))), row0: rows[0] ? Object.assign(R(rows[0]), { seen: seen(rows[0], w), uid: txt(rows[0].querySelector('.cfid')) }) : null,
      curN: cur.length, curT: txt(w.querySelector('.cfcl')), inp: !!w.querySelector('input') && seen(w.querySelector('input'), w),
      ft: ft ? Object.assign(R(ft), { inWin: inside(R(ft), W), inBody: !!bd && bd.contains(ft) }) : null,
      bd: bd ? { sh: bd.scrollHeight, ch: bd.clientHeight, st: bd.scrollTop, R: R(bd) } : null };
  },
  /* 몸을 굴려 닿는가 — 걸린 연결 마지막 줄 · 안내 줄(몸 안이면 몸 끝까지 굴림) · 몸 굴림만 쓴다(scrollIntoView 는 창 밖 문서까지 굴린다) */
  async cfReach(){ const w = lkWin(); if (!w) return null; const bd = w.querySelector(':scope > .pb');
    const toView = e => { if (!bd || !e || !bd.contains(e)) return; for (let i = 0; i < 4; i++){ const a = R(e), b = R(bd); if (a.b > b.b - 1) bd.scrollTop += a.b - b.b + 4; else if (a.y < b.y + 1) bd.scrollTop -= b.y - a.y + 4; else break; } };
    const cur = [...w.querySelectorAll('.cfcur .cfcr')].filter(vis), last = cur[cur.length - 1], ft = w.querySelector('.cfft');
    const out = { curN: cur.length };
    if (last){ toView(last); await wait(80); out.cur = seen(last, w); out.curR = R(last); } else out.cur = null;
    if (ft){ if (bd && bd.contains(ft)) bd.scrollTop = bd.scrollHeight; await wait(80); out.ft = seen(ft, w); out.ftR = R(ft); }
    out.W = R(w); const B = VB(); out.inScreen = out.W.y >= B.y + 8 - 1 && out.W.b <= B.y + B.h - 8 + 1;
    if (bd) bd.scrollTop = 0; await wait(60);
    return out; },
  cfInp(){ const w = lkWin(); const i = w && w.querySelector('input'); return i ? hitOn(i, true) : null; },
  /* 결과 첫 줄 — 굴리지 않고 그 자리(보이면 on) · 글 부분(번호 누름 = 문제 창이라 피한다) */
  cfRow0(){ const w = lkWin(); if (!w) return null; const r = [...w.querySelectorAll('.cfrs .cfr')].filter(vis).find(x => !x.classList.contains('on')); if (!r) return null;
    const t = r.querySelector('.cftx') || r; return Object.assign(hitOn(t, true), { uid: txt(r.querySelector('.cfid')) }); },
  cfBoot(){ return { vvPhone: typeof vvPhone === 'function' ? vvPhone() : null, cfFit: typeof cfFit === 'function' }; },
  /* ── A-2 정오문제 창 크기 ── */
  jp(){ const w = document.querySelector('.pop.wm-jp'); if (!w) return { win: false }; const r = R(w); return { win: true, vis: vis(w), x: r.x, y: r.y, w: Math.round(r.w), h: Math.round(r.h), W: S.joPanelW, H: S.joPanelH }; },
  jpGrip(){ const w = document.querySelector('.pop.wm-jp'); const g = w && w.querySelector(':scope > .prsz'); return g ? hitOn(g, true) : null; },
  ui(){ try{ return JSON.parse(localStorage.getItem('jopangi_ui') || 'null'); }catch(e){ return 'bad'; } },
  uiSeed(o){ let u = {}; try{ u = JSON.parse(localStorage.getItem('jopangi_ui') || '{}') || {}; }catch(e){} Object.keys(o).forEach(k => { if (o[k] === null) delete u[k]; else u[k] = o[k]; }); localStorage.setItem('jopangi_ui', JSON.stringify(u)); return u; },
  /* ── A-3 빈칸 종류 ── */
  async exvGo(y, no){ try{ closeAllPops(); }catch(e){} S.tab = 'jimun'; S.jimunTab = 'gichul'; S.year = String(y); S.mok = ''; S.omr = false; S.giWrong = false;
    const nq = ((typeof VJ !== 'undefined' && VJ && VJ.qs) || []).filter(q => String(q.연도) === String(y)).length, last = Math.max(0, Math.ceil(nq / 5) - 1);
    S.exvPg = S.exvPg || {}; const pgk = (typeof PLAW === 'function' ? PLAW() : '특허') + ':' + y; S.exvPg[pgk] = no ? Math.min(Math.floor((no - 1) / 5), last) : 0;   /* no 가 크면 마지막 쪽 */
    await idle(); await render(); await idle(); await until(() => document.querySelector('.exv-paper.uzexv, [id^="gi-"]'), 20000); await wait(300);
    return { exv: !!document.querySelector('.exv-paper.uzexv'), nos: [...document.querySelectorAll('.exv-q')].map(q => q.dataset.exno) }; },
  exvCells(no){ const q = document.querySelector('.exv-q[data-exno="' + no + '"]'); if (!q) return null;
    return [...q.querySelectorAll('.uzexb')].map(b => { const s = b.querySelector('.mbtype .seg.bk'); return { k: b.dataset.uzk, id: txt(b.querySelector('.qb.id')), bk: s ? s.dataset.bk : null, t: s ? txt(s) : null, q: s ? s.classList.contains('q') : null }; }); },
  exvBkAt(no, id){ const q = document.querySelector('.exv-q[data-exno="' + no + '"]'); if (!q) return null; const b = [...q.querySelectorAll('.uzexb')].find(x => txt(x.querySelector('.qb.id')) === id);
    const s = b && b.querySelector('.mbtype .seg.bk'); return s ? hitOn(s) : null; },
  cardBk(uid){ const idc = [...document.querySelectorAll('#slot .qb.id')].find(b => txt(b) === uid); const hd = idc && (idc.closest('.mbqhd') || idc.closest('.qhd')); const s = hd && hd.querySelector('.mbtype .seg.bk');
    return s ? { bk: s.dataset.bk, t: txt(s), vis: vis(s) } : (idc ? { bk: null } : null); },
  cardShown(uid){ return [...document.querySelectorAll('#slot .qb.id')].some(b => txt(b) === uid && vis(b)); },
  bkAll(){ try{ return JSON.parse(JSON.stringify(bktAll())); }catch(e){ return null; } },
  bkClear(){ try{ localStorage.setItem('jopangi.bktype', '{}'); }catch(e){} try{ BKTREC = null; }catch(e){} return 1; },
  bkPopTitle(){ const p = pops().filter(x => /빈칸 종류 확정/.test(x._pk || '')).pop(); return p ? txt(p.querySelector('.ph .pt')) : null; },
  bkTitleOf(k){ try{ return '🏷 빈칸 종류 확정 — ' + linkDisp(k); }catch(e){ return null; } },
  typeOf(uid){ const idc = [...document.querySelectorAll('#slot .qb.id')].find(b => txt(b) === uid); const hd = idc && (idc.closest('.mbqhd') || idc.closest('.qhd')); return hd ? txt(hd.querySelector('.mbtype')) : null; },
  /* ── A-4 기출뷰 = 민법 값 ── */
  exvCss(){ const q = s => document.querySelector(s);
    const paper = q('#slot .exv-paper.uzexv') || q('#slot .exv-paper'), main = paper && paper.parentNode, head = q('#slot .mbsbar');
    const pr = paper ? R(paper) : null, mr = main ? R(main) : null, hr = head ? R(head) : null;
    const mcs = main ? getComputedStyle(main) : null, pl = mcs ? parseFloat(mcs.paddingLeft) : 0, prr = mcs ? parseFloat(mcs.paddingRight) : 0;
    return { next: cs(q('#slot [data-uzexnext]'), EXCS), grade: cs(q('#slot [data-uzexgrade]'), EXCS), prev: cs(q('#slot .mbbar.l .mbprev'), EXCS),
      pill: cs(q('#slot .mbbar.r .mbpill'), EXCS), mk: cs(q('#slot .mbbar.r .mbpill .mk'), ['fontSize', 'fontWeight', 'color']), mkb: cs(q('#slot .mbbar.r .mbpill .mk b'), ['fontSize', 'fontWeight', 'color']),
      pg: cs(q('#slot .mbsbar .pg'), EXCS), t2: cs(q('#slot .mbsbar .t2'), ['fontSize', 'fontWeight', 'color']), qtx: cs(q('#slot .exv-paper .mbqtx'), ['color']),
      paper: pr && mr ? { w: pr.w, gapL: +(pr.x - mr.x - pl).toFixed(1), gapR: +(mr.r - prr - pr.r).toFixed(1), mainW: +(mr.w - pl - prr).toFixed(1) } : null,
      head: hr && mr ? { w: hr.w, gapL: +(hr.x - mr.x - pl).toFixed(1), gapR: +(mr.r - prr - hr.r).toFixed(1) } : null,
      barR: q('#slot .mbbar.r') && mr ? { r: +(mr.r - prr - R(q('#slot .mbbar.r')).r).toFixed(1) } : null,
      nextT: txt(q('#slot [data-uzexnext]')), gradeT: txt(q('#slot [data-uzexgrade]')), prevT: txt(q('#slot .mbbar.l .mbprev')), vw: innerWidth }; },
  unitPill(){ const q = s => document.querySelector(s); const pill = q('#slot .mbbar .mbpill'); const pb = pill && pill.querySelector('.mbpb');
    return { pill: cs(pill, EXCS), pb: cs(pb, EXCS), pbT: txt(pb), prev: cs(q('#slot .mbbar .mbprev'), EXCS), mk: cs(pill && pill.querySelector('.mk'), ['fontSize', 'fontWeight', 'color']), bar: q('#slot .mbbar') ? R(q('#slot .mbbar')) : null }; },
  /* 서랍 「변리사 기출」 — NEW = 해 머리 .jtych + 회차 줄 .jtyit · 바탕 = 해 줄 .jtit(「2026년 …」) */
  gy(){ const H = [...document.querySelectorAll('#jtlist .jtych')], I = [...document.querySelectorAll('#jtlist .jtyit')];
    const base = [...document.querySelectorAll('#jtlist .jtit')].filter(r => !r.classList.contains('jtyit') && /^\d{4}년/.test(txt(r.querySelector('.tx'))));
    const rowOf = r => { const l1 = r.querySelector('.l1'); const kids = l1 ? [...l1.children].map(c => c.className) : [];
      return { y: r.dataset.gy || (/^(\d{4})/.exec(txt(r.querySelector('.tx'))) || [])[1], t: txt(r), cur: r.classList.contains('cur'), order: kids, bar: !!r.querySelector('.jdbar'),
        cs: cs(r, ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft', 'backgroundColor', 'borderLeftWidth', 'borderLeftColor']),
        tx: cs(r.querySelector('.tx'), ['fontSize', 'fontWeight', 'color']), n: cs(r.querySelector('.n'), ['fontSize', 'fontWeight', 'color']), nT: txt(r.querySelector('.n')),
        now: cs(r.querySelector('.now'), ['fontSize', 'fontWeight', 'color', 'backgroundColor', 'borderTopLeftRadius', 'paddingLeft', 'paddingRight']) }; };
    return { heads: H.map(h => ({ y: h.dataset.gy, t: txt(h), cur: h.classList.contains('cur'), cs: cs(h, ['fontSize', 'fontWeight', 'color', 'backgroundColor', 'paddingTop', 'paddingLeft', 'marginTop']),
               n: cs(h.querySelector('.n'), ['fontSize', 'fontWeight', 'color']), nT: txt(h.querySelector('.n')) })),
             items: I.map(rowOf), base: base.map(rowOf), gi: txt([...document.querySelectorAll('#jtlist .jtch')].find(x => /변리사 기출/.test(txt(x)))) }; },
  gyHeadAt(y){ const h = document.querySelector('#jtlist .jtych[data-gy="' + y + '"]'); return h ? hitOn(h) : null; },
  gyRowAt(y){ const r = document.querySelector('#jtlist .jtyit[data-gy="' + y + '"]') || [...document.querySelectorAll('#jtlist .jtit')].find(x => txt(x.querySelector('.tx')).indexOf(y + '년') === 0); return r ? hitOn(r) : null; },
  state(){ return { tab: S.tab, jt: S.jimunTab, year: S.year, mok: S.mok, jtCh: JSON.stringify(S.jtCh || {}) }; },
  /* ── A-5 조 패널 카드 칩 — 특허 전 조 · 조 패널 카드 빌더(sidCardEl) 그대로 짓고 머리 글자를 모은다(창에 그리지 않음 · 같은 번호) ── */
  mln(){ return { ok: has('MLN') && !!MLN && !!MLN.ok, subj: has('MLN') && MLN ? (MLN._subj || null) : null, lid: has('MLN') && MLN && MLN.lid ? Object.keys(MLN.lid).length : 0 }; },
  async chipCensus(){ if (typeof joPanelIdx !== 'function' || typeof sidCardEl !== 'function' || typeof jsPanelItems !== 'function') return { err: 'no fn' };
    const JP = await joPanelIdx(); const jo0 = S.jo, out = {}; let n = 0;
    const ks = Object.keys(JP || {}).sort();
    for (const k of ks){
      S.jo = k;
      let items = []; try{ items = jsPanelItems(JP[k], k); }catch(e){ continue; }
      const nos = typeof jsPanelNos === 'function' ? jsPanelNos(items) : items.map((x, i) => i + 1);
      items.forEach((it, ix) => { let c = null; try{ c = sidCardEl(it, it.sid, nos[ix], { instant: true }); }catch(e){ out[k + '|' + it.sid] = 'ERR ' + String(e).slice(0, 60); n++; return; }
        const hd = c && (c.querySelector('.mbqhd') || c.querySelector('.qhd'));
        out[k + '|' + it.sid] = hd ? txt(hd) : ('(머리 없음) ' + txt(c).slice(0, 60)); n++; });
      if (n % 400 < 20) await wait(0);
    }
    S.jo = jo0;
    return { n: n, jo: ks.length, sig: out }; },
  cardYearChips(sid){ const c = document.getElementById('jp-' + sid); return c ? [...c.querySelectorAll('.jxec')].map(txt) : null; },
  cardHead(sid){ const c = document.getElementById('jp-' + sid); const hd = c && (c.querySelector('.mbqhd') || c.querySelector('.qhd')); return hd ? txt(hd) : null; },
  /* ── A-6 3법 칸 자리 ── */
  c3pick(){ const p = document.querySelector('#slot .c3pick'); if (!p) return null; const prev = p.previousElementSibling, col = (prev && prev.classList.contains('thcol')) ? prev : p.closest('.thcol');
    const pr = R(p), cr = col ? R(col) : null;
    return { vis: vis(p), law: p.dataset.dst, inCard: !!p.closest('.thcol'), afterCard: !!(prev && prev.classList.contains('thcol')), top: pr.y, cardB: cr ? cr.b : null, below: cr ? pr.y >= cr.b - 0.5 : null,
      w: pr.w, rowW: p.parentNode ? R(p.parentNode).w : null, inp: !!p.querySelector('input'), sel: !!p.querySelector('select') }; },
  /* ── A-7 서랍 이름 ── */
  /* 조 번호까지 가려졌나 — 조 번호 글자 폭(같은 글꼴 탐침) > 보이는 폭 − 말줄임표 폭(넘칠 때만) · Range 사각형은 WebKit 이 말줄임 뒤 글자를 보이는 자리로 줄여 돌려줘 못 쓴다 */
  names(){ const rows = [...document.querySelectorAll('#slot .tree .r')].filter(r => !r.classList.contains('jhead') && !r.classList.contains('jsub') && r.querySelector('span.nm') && /^제\d/.test(txt(r.querySelector('span.nm'))));
    const pr = document.createElement('span'); pr.style.cssText = 'position:absolute;visibility:hidden;white-space:nowrap;left:-9999px;top:0;padding:0;border:0'; document.body.appendChild(pr);
    const wOf = (s, font) => { pr.style.font = font; pr.textContent = s; return pr.getBoundingClientRect().width; };
    const out = rows.map(r => { const nm = r.querySelector('span.nm'), st = r.querySelector('.jstarn'), em = r.querySelector('em.jcol3'); const t = nm.textContent;
      const m = /^제\d+조(?:의\d+)?/.exec(t), font = getComputedStyle(nm).font, over = nm.scrollWidth > nm.clientWidth + 1;
      const pw = m ? wOf(m[0], font) : 0, ew = wOf('…', font);
      return { k: m ? m[0] : t.slice(0, 8), t: t.slice(0, 40), cw: nm.clientWidth, sw: nm.scrollWidth, st: st ? { cw: st.clientWidth, sw: st.scrollWidth, t: txt(st), cls: st.className } : null, em: em ? Math.round(em.getBoundingClientRect().width) : null,
        pw: Math.round(pw * 10) / 10, pClip: !!m && over && pw > nm.clientWidth - ew + 0.5 }; });
    pr.remove();
    return { n: out.length, treeW: S.treeW, rows: out }; }
};
})();
