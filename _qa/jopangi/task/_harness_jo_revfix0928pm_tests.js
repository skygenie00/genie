/* _harness_jo_revfix0928pm_tests.js — _task_jo_revfix0928pm 하네스가 페이지에 넣는 도구(__RP).
   NEW·BASE 둘 다에 같은 것을 넣는다 — 없는 함수는 빈 값(헛잣대). 누름은 여기서 안 한다(자리만 · 파이썬이 page.mouse · 터치). */
(function(){
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const vis = e => !!e && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden' && e.getBoundingClientRect().height > 0;
const has = n => { try{ return typeof eval(n) !== 'undefined'; }catch(e){ return false; } };
const R = e => { const r = e.getBoundingClientRect(); return { x: +r.left.toFixed(2), y: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2), r: +r.right.toFixed(2), b: +r.bottom.toFixed(2) }; };
function hitOn(t){ if (!t) return null; try{ t.scrollIntoView({ block: 'center', inline: 'nearest' }); }catch(e){}
  const r = t.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2, at = document.elementFromPoint(cx, cy);
  return { cx, cy, w: r.width, h: r.height, on: !!at && (at === t || t.contains(at)) && cy > 0 && cy < innerHeight, vis: vis(t), t: txt(t) }; }
window.__RP = {
  font(f){ let s = document.getElementById('__rpfont'); if (!s){ s = document.createElement('style'); s.id = '__rpfont'; document.head.appendChild(s); }
    s.textContent = f ? '*{font-family:' + f + ' !important}' : ''; return f; },
  /* 머리 — 요소마다 줄 번호(윗변 묶음 · 4px) · 머리 높이 · 본문 위 끝 · 배지 묶음 자리(머리/검색줄) */
  head(){ try{ if (typeof hdrFit === 'function') hdrFit(); }catch(e){}
    const top = document.querySelector('header.topbar'); if (!top) return null;
    const ids = ['.logo', '#laws', '#hrail', '#hbadges'].map(s => [s, top.querySelector(s) || document.querySelector(s)]);
    const on = ids.filter(([s, e]) => e && vis(e) && e.parentElement === top);
    const tops = []; on.forEach(([s, e]) => { const y = e.getBoundingClientRect().top; if (!tops.some(t => Math.abs(t - y) < 4)) tops.push(y); }); tops.sort((a, b) => a - b);
    const line = {}; on.forEach(([s, e]) => { const y = e.getBoundingClientRect().top; line[s] = tops.findIndex(t => Math.abs(t - y) < 4); });
    const hb = document.getElementById('hbadges'), slot = document.getElementById('slot');
    return { h: +top.getBoundingClientRect().height.toFixed(1), line, hb: hb ? (hb.parentElement === top ? 'top' : hb.parentElement.id || 'x') : null,
             body: slot ? +slot.getBoundingClientRect().top.toFixed(1) : null }; },
  fold(){ const b = document.getElementById('hdrFold'), lw = document.getElementById('laws'); if (!b) return null;
    const r = R(b), l = R(lw); const hr = document.getElementById('hrail');
    return { t: txt(b), r, laws: l, dx: +(r.x - l.r).toFixed(2), dy: +((r.y + r.h / 2) - (l.y + l.h / 2)).toFixed(2), pos: getComputedStyle(b).position,
             hfold: document.getElementById('app').classList.contains('hfold'), hrailVis: vis(hr), hrailTxtX: hr && hr.firstElementChild ? R(hr.firstElementChild).x : null,
             at: hitOn(b) }; },
  /* 카드 */
  keyP7(id){ const z = (VJ && VJ.P7map || {})[id]; return z ? oxKeyP7(z) : null; },
  keyLid(qid, n){ const q = ((VJ && VJ.qs) || []).find(x => x.id === qid); if (!q) return null; const z = (q.지문 || []).find(x => String(x.n) === String(n)); return z ? oxKeyLid(q, z) : null; },
  card(k){ const c = document.getElementById('qb-' + k); if (!c) return null;
    return { vis: vis(c), t: txt(c), qexp: [...c.querySelectorAll('.qexp')].map(txt), qbv: [...c.querySelectorAll('.qb.v')].map(txt), p8: [...c.querySelectorAll('.p8c')].map(txt), r: R(c), hit: c.classList.contains('hmhit') }; },
  qexpAt(k){ const c = document.getElementById('qb-' + k); const b = c && c.querySelector('.qexp'); return b ? hitOn(b) : null; },
  p8keys(){ return Object.values((VJ && VJ.P7map) || {}).filter(z => z.판8 && z.판8.cat === '새').map(z => oxKeyP7(z)); },
  p8cat(id){ const z = (VJ && VJ.P7map || {})[id]; return z ? (z.판8 || null) : null; },
  catCount(){ const c = {}; Object.values((VJ && VJ.P7map) || {}).forEach(z => { if (z.판8 && z.판8.cat) c[z.판8.cat] = (c[z.판8.cat] || 0) + 1; }); return c; },
  firstCat(cat){ const z = Object.values((VJ && VJ.P7map) || {}).find(z => z.판8 && z.판8.cat === cat); return z ? { id: z.id, k: oxKeyP7(z) } : null; },
  /* 지문 팝업 */
  qpop(){ const p = (typeof POPS !== 'undefined' ? POPS : []).find(x => /^q\|📝 지문 /.test(x._pk || '')); if (!p) return null;
    const go = p.querySelector('.qgo'); return { pk: p._pk, qpc1: txt(p.querySelector('.qpc1')), t: txt(p).slice(0, 200), go: go ? hitOn(go) : null }; },
  jpop(){ const p = (typeof POPS !== 'undefined' ? POPS : []).find(x => /^q\|📝 /.test(x._pk || '')); if (!p) return null;
    const g = [...p.querySelectorAll('button.tool')].find(b => /그 지문으로 가기/.test(txt(b))); return { pk: p._pk, go: g ? hitOn(g) : null }; },
  /* 통합 검색(#skin) 줄 */
  skRows(){ return [...document.querySelectorAll('#skres .res')].map(r => ({ head: txt(r.querySelector('b')), tag: txt(r.querySelector('.lawtag')) })); },
  skRowAt(re){ const rx = new RegExp(re); const r = [...document.querySelectorAll('#skres .res')].find(x => rx.test(txt(x.querySelector('b')))); return r ? hitOn(r) : null; },
  skin(){ const i = document.getElementById('skin'); return i ? hitOn(i) : null; },
  /* 서랍 */
  drawer(){ const rows = [...document.querySelectorAll('.tree .r')].filter(r => r.querySelector('span.nm') && vis(r));
    return rows.map(r => { const nm = r.querySelector('span.nm'), no = nm.querySelector('.jno'), tt = nm.querySelector('.jtt'), st = r.querySelector('.jstarn'), sd = st && st.querySelector('.jsd');
      const nr = R(nm);
      let noR = no ? R(no) : null;
      if (!no && nm.firstChild && nm.firstChild.nodeType === 3){   /* 바탕(한 칸) — 조 번호 = 첫 빈칸 앞까지 글자 자리(Range) */
        const s = nm.firstChild.nodeValue, i = s.indexOf(' '); if (i > 0){ const rg = document.createRange(); rg.setStart(nm.firstChild, 0); rg.setEnd(nm.firstChild, i);
          const rr = rg.getBoundingClientRect();
          /* 바탕 ★ 칩 — 한 칸 글(「★ 25.1.21」) · 날짜 첫 글자가 칩 오른쪽 끝에 걸쳐 반쯤 보이나(Range) */
          let half = false; const st = r.querySelector('.jstarn');
          if (st && st.firstChild && st.firstChild.nodeType === 3 && st.firstChild.nodeValue.length > 2){ const sr = st.getBoundingClientRect(), g = document.createRange();
            g.setStart(st.firstChild, 2); g.setEnd(st.firstChild, 3); const d = g.getBoundingClientRect(); half = d.left < sr.right - 0.5 && d.right > sr.right + 0.5; }
          return { t: txt(nm), nmw: nr.w, base: true, no: { t: s.slice(0, i), clip: rr.right > nr.r + 0.5 }, half }; } }
      return { t: txt(nm), nmw: nr.w, nmsw: nm.scrollWidth, nmcw: nm.clientWidth, to: getComputedStyle(nm).textOverflow,
               no: no ? { t: no.textContent, r: noR, clip: noR.r > nr.r + 0.5 || no.scrollWidth > no.clientWidth + 1 } : null,
               tt: tt ? { t: tt.textContent, sw: tt.scrollWidth, cw: tt.clientWidth, to: getComputedStyle(tt).textOverflow } : null,
               st: st ? { t: st.textContent, r: R(st), sd: sd ? R(sd) : null } : null }; }); },
  toasts(){ return (window.__TOASTS || []).slice(-6); },
  toastClear(){ if (window.__TOASTS) window.__TOASTS.length = 0; return 0; },
};
})();
