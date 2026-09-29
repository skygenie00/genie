/* _harness_jo_p8sol_tests.js — _task_jo_p8sol 하네스가 페이지에 넣는 도구(__PS).
   NEW·BASE 둘 다에 같은 것을 넣는다 — 없는 함수는 빈 값(헛잣대). 누름은 여기서 안 한다(자리만 · 파이썬이 page.mouse · 터치). */
(function(){
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const vis = e => !!e && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden' && e.getBoundingClientRect().height > 0;
const R = e => { const r = e.getBoundingClientRect(); return { x: +r.left.toFixed(2), y: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2) }; };
function hitOn(t){ if (!t) return null; try{ t.scrollIntoView({ block: 'center', inline: 'nearest' }); }catch(e){}
  const r = t.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2, at = document.elementFromPoint(cx, cy);
  return { cx, cy, w: r.width, h: r.height, on: !!at && (at === t || t.contains(at)) && cy > 0 && cy < innerHeight, vis: vis(t), t: txt(t) }; }
/* 해설 칸 하나 읽기 — 단추 · 상자 · 해설 글 · 단추가 해설 글 바로 위 왼쪽인가 */
function solBox(host){
  if (!host) return null;
  const w = host.querySelector('.p8sw'), b = w && w.querySelector(':scope > .p8sh > button.p8c'), bx = w && w.querySelector(':scope > .p8t7');
  const sol = w ? w.querySelector(':scope > :not(.p8sh):not(.p8t7)') : null;
  let place = null;
  if (b && sol && vis(b) && vis(sol)){ const rb = R(b), rs = R(sol); place = { dy: +(rs.y - (rb.y + rb.h)).toFixed(2), dx: +(rb.x - rs.x).toFixed(2), after: !!(bx && (sol.compareDocumentPosition(bx) & 4)) }; }
  const cs = b ? getComputedStyle(b) : null;
  return { btn: b ? txt(b) : null, btnVis: vis(b), font: cs ? [cs.fontSize, cs.fontWeight, cs.color] : null, box: bx ? txt(bx) : null, boxVis: vis(bx), place,
           sol: txt(sol || host.querySelector('.sol,.qpe,.jne,.cdim')).slice(0, 120), all: [...host.querySelectorAll('button.p8c')].map(txt) };
}
window.__PS = {
  keyP7(id){ const z = (VJ && VJ.P7map || {})[id]; return z ? oxKeyP7(z) : null; },
  z(id){ const z = (VJ && VJ.P7map || {})[id]; return z ? { sol: z.sol, ox: z.ox, 판8: z.판8 || null } : null; },
  /* 카드 */
  pkAt(k){ const c = document.getElementById('qb-' + k); const b = c && [...c.querySelectorAll('button')].find(x => /정답·해설/.test(txt(x))); return b ? hitOn(b) : null; },
  card(k){ const c = document.getElementById('qb-' + k); if (!c) return null; const e = c.querySelector('.mbexp'); return Object.assign({ expVis: vis(e) }, solBox(e) || {}); },
  btnAt(k){ const c = document.getElementById('qb-' + k); const b = c && c.querySelector('.p8sw > .p8sh > button.p8c'); return b ? hitOn(b) : null; },
  /* 문제 창(1차객 🔍 → 줄) */
  qpop(){ const p = (typeof POPS !== 'undefined' ? POPS : []).find(x => /^q\|📝 지문 /.test(x._pk || '')); if (!p) return null;
    const pk = p.querySelector('.qpans'); return Object.assign({ pk: p._pk, ansHidden: pk ? pk.hidden : null }, solBox(p) || {}); },
  qpOpen(){ const p = (typeof POPS !== 'undefined' ? POPS : []).find(x => /^q\|📝 지문 /.test(x._pk || '')); const a = p && p.querySelector('.qpans'); if (a) a.hidden = false; return !!a; },
  qpBtnAt(){ const p = (typeof POPS !== 'undefined' ? POPS : []).find(x => /^q\|📝 지문 /.test(x._pk || '')); const b = p && p.querySelector('.p8sw > .p8sh > button.p8c'); return b ? hitOn(b) : null; },
  /* 기출뷰 지문 상자 — 앱 함수로 직접 그려 DOM 만 본다(자리 · 누름은 카드에서 잰다) */
  exvProbe(id){ try{ if (typeof uzExvBox !== 'function') return { none: 'fn' };
      /* 기출뷰 문항의 지문 객체 가운데 판8.s7 을 든 것(7판 원장 객체 그대로 · 시험지·리담 객체는 s7 이 없다) */
      let q = null, i = -1; const pairs = [];
      (VJ.qs || []).forEach(q0 => (q0.지문 || []).forEach((x, j) => { if (x && x.판8 && x.판8.s7) pairs.push([q0, j]); }));
      if (!pairs.length) return { none: 's7 든 기출뷰 지문 0', n: 0 };
      [q, i] = pairs[0];
      const box = uzExvBox(q, q.지문[i], i, null, true, true); const e = box.querySelector('.mbexp'); return solBox(e || box); }catch(e){ return { err: String(e).slice(0, 160) }; } },
  /* 사용자가 고친 해설 — 기억에만(lsWrite 안 함 · 동기화 안 탐) */
  fixExp(k, t){ try{ const A = qfixAll(); if (t == null) delete A[k]; else A[k] = Object.assign({}, A[k] || {}, { exp: t }); QFIXREC = A; return true; }catch(e){ return String(e); } },
  counts(){ const c = { s7: 0, 해설: 0 }; Object.values((VJ && VJ.P7map) || {}).forEach(z => { if (z.판8 && z.판8.s7) c.s7++; if (z.판8 && z.판8.cat === '해설') c.해설++; }); return c; },
};
})();
