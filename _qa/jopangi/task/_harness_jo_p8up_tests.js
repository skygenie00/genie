/* _harness_jo_p8up_tests.js — _task_jo_p8up 관문 도구(__P8).
   mbsame 도구(__HM) · uidmbs2 도구(__UZ) 뒤에 붙는다 · BASE(genie HEAD = jo_hdrfold 인도판 앱 + 판올림 전 데이터)·NEW 같은 것을 넣는다 — 없는 함수·칸은 빈 값(헛잣대).
   ⚠ 누름은 여기서 안 한다 — 자리만 돌려주고 파이썬이 page.mouse · CDP 터치 r22 · WebKit touchscreen.tap 으로 누른다. */
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
const st = e => { if (!e) return null; const s = getComputedStyle(e);
  return { fs: s.fontSize, fw: s.fontWeight, color: s.color, bg: s.backgroundColor, bw: s.borderTopWidth, bs: s.borderTopStyle, pad: s.padding, lh: s.lineHeight, cur: s.cursor, h: Math.round(e.getBoundingClientRect().height * 10) / 10 }; };
const card = k => document.getElementById('qb-' + k);
/* 열쇠의 ID 칩이 든 칩 줄(단원 카드 · 리담 카드 · 기출뷰 지문 칸) */
const headOf = k => { const c = card(k); if (c){ const h = c.querySelector(':scope > .mbqhd'); if (h) return h; }
  const idc = [...document.querySelectorAll('.qb.id')].find(b => txt(b) === k); return idc ? (idc.closest('.mbqhd') || idc.closest('.qhd')) : null; };
window.__P8 = {
  has(n){ return has(n); },
  /* 카드 머리 — 칩 차례 · 8판 칩 · 책 번호 자리 · 「제7판」/「8판」 접기 칩 · 출처 칩 */
  head(k){ const h = headOf(k); if (!h) return null;
    const kids = [...h.children];
    const iMc = kids.findIndex(x => x.classList.contains('mcchip') || /^🃏/.test(txt(x)));
    const iTags = kids.findIndex(x => x.classList.contains('mbtags'));
    const p8 = [...h.querySelectorAll('.p8c')].map(b => Object.assign({ t: txt(b), cls: b.className, tag: b.tagName, idx: kids.indexOf(b), inL: !kids.includes(b), vis: vis(b) }, st(b)));
    const c = card(k);
    const bk = c ? c.querySelector('.mlnbk') : null, qx = h.querySelector('.qexp'), src = h.querySelector('.qb.v:not(.qexp)');
    const sub = c ? c.querySelector(':scope > .qsub') : null;
    return { p8, iMc, iTags, n: kids.length, book: txt(bk), qexp: txt(qx), src: txt(src), sub: sub ? (sub.textContent || '').trim() : null, t7: !!(c && c.querySelector(':scope > .p8t7')) }; },
  p8At(k, re){ const h = headOf(k); const rx = new RegExp(re || '.'); const b = h ? [...h.querySelectorAll('.p8c')].find(x => rx.test(txt(x))) : null; return b ? hitOn(b) : null; },
  qexpAt(k){ const h = headOf(k); const b = h && h.querySelector('.qexp'); return b ? hitOn(b) : null; },
  t7Row(k){ const c = card(k); const r = c && c.querySelector(':scope > .p8t7'); if (!r) return null;
    const prev = r.previousElementSibling; return Object.assign({ vis: vis(r), t: (r.textContent || '').replace(/\s+/g, ' ').trim(), afterHead: !!(prev && prev.classList.contains('mbqhd')), lab: txt(r.querySelector('b')) }, st(r)); },
  shotBox(k){ const h = headOf(k); if (!h) return null; try{ h.scrollIntoView({ block: 'center' }); }catch(e){} const c = card(k) || h; const r = c.getBoundingClientRect(); return { x: Math.max(0, r.left - 4), y: Math.max(0, r.top - 4), w: Math.min(innerWidth, r.width + 8), h: Math.min(innerHeight - 1, Math.min(r.height, 240) + 8) }; },
  /* 단원 줄 · 본편 셈 — 8판 새 카드(판8.cat 새)가 선 줄 */
  census(){ if (!(has('MLN') && MLN.ok)) return null; const M = VJ.M, isN = c => !!(c && c.kind === 'P' && c.z && c.z.판8 && c.z.판8.cat === '새');
    const o = { b: 0, u: 0, deepB: 0, deepU: 0, byNode: {} };
    M.forEach((n, i) => { const d = mlnDirect(M, i, VJ.P7map, VJ.byId); const b = d.b.filter(isN).length, u = d.u.filter(isN).length; o.b += b; o.u += u; if (u || b) o.byNode[n.no + ' ' + n.제목] = { b, u };
      o.deepB += (typeof mlnCardsDeep === 'function' ? mlnCardsDeep(i, 'b').filter(isN).length : 0); });
    M.forEach((n, i) => { if (n.깊이 === 1) o.deepU += (typeof mlnCardsDeep === 'function' ? mlnCardsDeep(i, 'u').filter(isN).length : 0); });
    return o; },
  nodeOf(no){ return (VJ.M || []).findIndex(n => String(n.no) === String(no)); },
  /* 단원 화면 카드 차례(열쇠 · 책 번호 자리 글) */
  unitCards(){ return [...document.querySelectorAll('#slot .mbq[id^="qb-"], #slot .question-box[id^="qb-"]')].filter(vis).map(c => ({ k: c.id.slice(3), book: txt(c.querySelector('.mlnbk')), p8: [...c.querySelectorAll(':scope > .mbqhd .p8c')].map(txt) })); },
  /* 리담 카드(이미 있는 34) — 열쇠의 칩 줄 8판 글 */
  lid(k){ const h = headOf(k); if (!h) return null; return { p8: [...h.querySelectorAll('.p8c')].map(b => Object.assign({ t: txt(b), vis: vis(b), afterMc: !!(b.previousElementSibling && b.previousElementSibling.classList.contains('mcchip')) }, st(b))) }; },
  exvHead(no){ const b0 = /^T/.test(String(no)) ? document.getElementById('exb-' + no) : null;   /* 선지 uid 로 문항 찾기(리담 문항 id 의 번호 ≠ 시험문번일 수 있다) */
    const q = b0 ? b0.closest('.exv-q') : document.querySelector('#slot .exv-q[data-exno="' + no + '"]'); if (!q) return null; const h = q.querySelector('.exv-head');
    return { stem: txt(h.querySelector('.exv-stem')).slice(0, 40), p8: [...h.querySelectorAll('.p8c')].map(b => Object.assign({ t: txt(b), vis: vis(b) }, st(b))), boxP8: [...q.querySelectorAll('.question-box .p8c')].length }; },
  exvBox(k){ const b = document.getElementById('exb-' + k); if (!b) return null; return { p8: [...b.querySelectorAll('.mbqhd .p8c')].map(x => Object.assign({ t: txt(x), vis: vis(x) }, st(x))) }; },
  exvNos(){ return [...document.querySelectorAll('#slot .exv-q')].map(q => q.dataset.exno); },
  /* 검색 · 풀 이름 · 연결 창 줄 · 정리 창 번호 */
  pool(k){ const P = (typeof OXPOOL !== 'undefined' && OXPOOL) ? OXPOOL[k] : null; return P ? { name: P.name, kind: P.kind, id: P.id } : null; },
  cfWhere(k){ try{ const h = cfHit(k); return h ? cfRow(k, h).where : null; }catch(e){ return 'ERR ' + e.message; } },
  jnNo(k){ try{ return uzJnInfo(k, null).no; }catch(e){ return 'ERR ' + e.message; } },
  async search(q){ const inp = document.querySelector('#slot .mbsr input'); if (!inp) return null; inp.value = q; inp.dispatchEvent(new Event('input', { bubbles: true })); await wait(900);
    return [...document.querySelectorAll('#slot .mbres .rr')].slice(0, 8).map(r => txt(r).slice(0, 90)); },
  /* 기록 심기(옛 풀이 기록 「7판 글」) */
  seedOx(k, rec){ const O = JSON.parse(localStorage.getItem('jopangi.ox') || '{}'); if (rec) O[k] = rec; else delete O[k]; localStorage.setItem('jopangi.ox', JSON.stringify(O));
    try{ OXREC = null; }catch(e){} try{ recDropCache(); }catch(e){} return true; },
  p8at(){ return (typeof P8_AT !== 'undefined') ? P8_AT : null; }
};
})();
