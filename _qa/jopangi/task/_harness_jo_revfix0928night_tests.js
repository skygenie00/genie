/* _harness_jo_revfix0928night_tests.js — _task_jo_revfix0928night 관문 도구(__RN).
   book8 도구(__B8) 뒤에 붙는다 · NEW·BASE 에 같은 것 · 누름은 여기서 안 한다(자리만 · 파이썬이 page.mouse · 손가락). */
(function(){
const wait = ms => new Promise(r => setTimeout(r, ms));
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const vis = e => !!e && e.isConnected && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden' && e.getBoundingClientRect().height > 0;
const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); return { x: +r.left.toFixed(2), y: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2), b: +r.bottom.toFixed(2), r: +r.right.toFixed(2), cx: +(r.left + r.width / 2).toFixed(2), cy: +(r.top + r.height / 2).toFixed(2) }; };
const vv = () => { const v = window.visualViewport; return v ? { y: v.offsetTop, h: v.height, w: v.width } : { y: 0, h: innerHeight, w: innerWidth }; };
/* 자리에 있는 단추 — 스크롤하지 않고 지금 자리 그대로 elementFromPoint */
function atNow(t){ if (!t) return null; const r = R(t), at = document.elementFromPoint(r.cx, r.cy);
  return Object.assign(r, { on: !!at && (at === t || t.contains(at)) && r.cy > 0 && r.cy < innerHeight, vis: vis(t), t: txt(t).slice(0, 40) }); }
function scrollerOf(e){ let q = e && e.parentElement; while (q && q !== document.body){ const cs = getComputedStyle(q); if (/(auto|scroll)/.test(cs.overflowY) && q.scrollHeight > q.clientHeight + 1) return q; q = q.parentElement; } return document.scrollingElement; }
const pops = () => (typeof POPS !== 'undefined' ? POPS : []);
const popOf = pre => pops().filter(x => (x._pk || '').indexOf(pre) === 0).pop();
window.__RN = {
  /* 카드 ID 칩을 화면 y 자리에 둔다(굴림 칸을 옮긴다) → 칩 자리 */
  idTo(k, y){ const c = [...document.querySelectorAll('.qb.id')].filter(vis).find(b => txt(b) === k) || [...document.querySelectorAll('.qb.id')].find(b => txt(b) === k);
    if (!c) return null; try{ c.scrollIntoView({ block: 'center' }); }catch(e){}
    for (let i = 0; i < 4; i++){ const r = c.getBoundingClientRect(), d = (r.top + r.height / 2) - y; if (Math.abs(d) < 2) break; const sc = scrollerOf(c); sc.scrollTop += d; window.scrollBy(0, 0); }
    return atNow(c); },
  pinSeed(u, p, r){ const A = JSON.parse(localStorage.getItem('jopangi.canvasjari') || '{}'); A['p8|' + u] = { by: 'hand', b: 'patent_hr8', p: p, r: r, t: Date.now() };
    localStorage.setItem('jopangi.canvasjari', JSON.stringify(A)); try{ recDropCache(); }catch(e){} return true; },
  pinDel(u){ const A = JSON.parse(localStorage.getItem('jopangi.canvasjari') || '{}'); delete A['p8|' + u]; localStorage.setItem('jopangi.canvasjari', JSON.stringify(A)); try{ recDropCache(); }catch(e){} return true; },
  /* 교재 자리 창 — 창 자리 · 보이는 화면 · 단추 둘 지금 자리 · 굴림 */
  boxWin(){ const w = popOf('cell|📚 교재 자리'); if (!w) return null; const h = w.querySelector('.mbb8');
    const bt = re => { const b = h && [...h.querySelectorAll('.ncb-more')].find(x => new RegExp(re).test(txt(x))); return b ? atNow(b) : null; };
    const pb = w.querySelector('.pb') || w;
    return { rect: R(w), vv: vv(), pic: !!(h && h.querySelector('.ncb-pic canvas')), rv: bt('자동으로 되돌리기'), pk: bt('자리 직접 찍기'),
      sh: w.scrollHeight, ch: w.clientHeight, oy: getComputedStyle(w).overflowY, pbsh: pb.scrollHeight, pbch: pb.clientHeight, pboy: getComputedStyle(pb).overflowY,
      head: R(w.querySelector('.ph')), rows: h ? [...h.querySelectorAll('.mbbrow')].map(r => ({ p: txt(r.querySelector('.hd .p')), hd: txt(r.querySelector('.hd')), m: [...r.querySelectorAll('.hd .m')].map(txt) })) : [],
      more: h ? [...h.querySelectorAll('.ncb-more')].map(txt) : [], moreRows: h ? [...h.querySelectorAll('[data-more] .mbbrow')].filter(vis).length : 0 }; },
  /* 창 몸 굴림 칸을 끝까지 → 단추 자리 */
  boxScrollEnd(){ const w = popOf('cell|📚 교재 자리'); if (!w) return null; [w, w.querySelector('.pb'), w.querySelector('.mbb8')].forEach(e => { if (e) e.scrollTop = e.scrollHeight; }); return __RN.boxWin(); },
  bookWin(){ const w = popOf('cv|book|'); if (!w) return null; return { rect: R(w), vv: vv(), title: txt(w.querySelector('.pt')), st: { h: w.style.height, top: w.style.top, w: w.style.width } }; },
  /* 정리캔버스 목차노트 「교재 자리」 창(ncbook) */
  ncWin(){ const w = popOf('ncbook|'); if (!w) return null; const h = w.querySelector('.mbblist');
    const bt = re => { const b = h && [...h.querySelectorAll('.ncb-more')].find(x => new RegExp(re).test(txt(x))); return b ? atNow(b) : null; };
    return { rect: R(w), vv: vv(), pic: !!(h && h.querySelector('.ncb-pic canvas')), rv: bt('자동으로 되돌리기'), rows: h ? [...h.querySelectorAll('.mbbrow .hd')].map(txt) : [] }; },
};
})();
