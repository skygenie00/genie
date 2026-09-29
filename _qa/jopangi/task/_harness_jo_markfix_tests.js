/* _harness_jo_markfix_tests.js — _task_jo_markfix 관문 도구(__MF). NEW·BASE 에 같은 것 · 없는 함수는 빈 값(헛잣대).
   누름·끌기는 여기서 안 한다(자리만) — 파이썬이 page.mouse · 손가락. 폰 선택만 도구가 만든다(길게 눌러 선택 = 브라우저 몫 · 헤드리스로 못 낸다). */
(function(){
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const vis = e => !!e && e.isConnected && !e.hidden && getComputedStyle(e).display !== 'none' && e.getBoundingClientRect().height > 0;
const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); return { x: +r.left.toFixed(2), y: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2), b: +r.bottom.toFixed(2), r: +r.right.toFixed(2) }; };
const has = n => { try{ return typeof eval(n) !== 'undefined'; }catch(e){ return false; } };
const skip = (n, root) => { try{ return plainSkip(n, root); }catch(e){ return false; } };
function textNodes(root){ const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT); const out = []; let n; while ((n = w.nextNode())) if (!skip(n, root)) out.push(n); return out; }
function at(root, c){ let acc = 0; for (const n of textNodes(root)){ const L = n.nodeValue.length; if (c < acc + L) return [n, c - acc]; acc += L; } return null; }
function charRect(root, c){ const p = at(root, c); if (!p) return null; const r = document.createRange(); r.setStart(p[0], p[1]); r.setEnd(p[0], p[1] + 1); const q = r.getClientRects()[0] || r.getBoundingClientRect(); return { x: q.left, y: q.top, w: q.width, h: q.height, b: q.bottom, r: q.right }; }
function plain(root){ return textNodes(root).map(n => n.nodeValue).join(''); }
window.__MF = {
  has(n){ return has(n); },
  /* 단원 카드 — 7판 카드 글(.mbqtx) 수 · data-mk 수 */
  cards(){ const a = [...document.querySelectorAll('#slot .qwrap .mbqtx')].filter(x => { const c = x.closest('.qwrap'); return c && /^qb-/.test(c.id) && !c.classList.contains('mlnz'); });
    return { n: a.length, mk: a.filter(x => x.dataset.mk).length, keys: a.slice(0, 3).map(x => x.dataset.mk || null) }; },
  firstCardText(){ const x = [...document.querySelectorAll('#slot .qwrap .mbqtx[data-mk]')].find(e => { const c = e.closest('.qwrap'); return vis(e) && c && !c.classList.contains('mlnz') && plain(e).length > 12; });
    if (!x) return null; x.id = x.id || '__mfc'; try{ x.scrollIntoView({ block: 'center' }); }catch(e){} return { sel: '#' + x.id, mk: x.dataset.mk }; },
  /* 글 조각 끌 자리(평문 a..b) */
  dragAB(sel, a, b){ const root = document.querySelector(sel); if (!root) return null; const r0 = charRect(root, a), r1 = charRect(root, b - 1); if (!r0 || !r1) return null;
    return { x0: r0.x + 1, y0: r0.y + r0.h / 2, x1: r1.r - 1, y1: r1.y + r1.h / 2 }; },
  selectAB(sel, a, b){ const root = document.querySelector(sel); const p = at(root, a), q = at(root, b - 1); if (!p || !q) return false; const r = document.createRange(); r.setStart(p[0], p[1]); r.setEnd(q[0], q[1] + 1);
    const s = getSelection(); s.removeAllRanges(); s.addRange(r); document.dispatchEvent(new Event('selectionchange')); root.dispatchEvent(new MouseEvent('mouseup', { bubbles: true })); root.dispatchEvent(new TouchEvent('touchend', { bubbles: true })); return true; },
  selRect(){ const s = getSelection(); if (!s || !s.rangeCount || s.isCollapsed) return null; return R(s.getRangeAt(0)); },
  clearSel(){ try{ getSelection().removeAllRanges(); }catch(e){} return true; },
  /* 막대 */
  bar(id){ const b = document.getElementById(id); if (!b) return null; const v = window.visualViewport;
    return { vis: vis(b), rect: R(b), vv: v ? { x: v.offsetLeft, y: v.offsetTop, w: v.width, h: v.height, s: v.scale } : null,
      btns: [...b.querySelectorAll('button')].map(x => { const cs = getComputedStyle(x); return { cls: x.className, m: x.dataset.m == null ? null : x.dataset.m, t: txt(x), w: +x.getBoundingClientRect().width.toFixed(1), h: +x.getBoundingClientRect().height.toFixed(1), bg: x.style.background || cs.backgroundColor, color: cs.color, deco: cs.textDecorationLine }; }) }; },
  btnAt(id, m){ const b = document.getElementById(id); const x = b && [...b.querySelectorAll('button')].find(y => m === '🏷' ? y.dataset.tag : y.dataset.m === m); if (!x) return null; const r = x.getBoundingClientRect(), e = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return { cx: r.left + r.width / 2, cy: r.top + r.height / 2, on: !!e && x.contains(e) }; },
  c2bar(){ try{ const b = c2MarkBar(); b.hidden = false; b.style.left = '10px'; b.style.top = '10px'; const o = __MF.bar('c2mark'); b.hidden = true; return o; }catch(e){ return null; } },
  /* 1차객 칠 */
  mkKeys(pre){ try{ return Object.keys(mkAll()).filter(k => k.indexOf(pre) === 0); }catch(e){ return []; } },
  marksIn(sel){ const root = document.querySelector(sel || '#slot'); return root ? [...root.querySelectorAll('mark.mkc')].map(m => { const cs = getComputedStyle(m); return { t: m.className, bgi: cs.backgroundImage.slice(0, 40), bb: cs.borderBottomWidth + ' ' + cs.borderBottomStyle + ' ' + cs.borderBottomColor, txt: m.textContent }; }) : null; },
  mkSeed(uid, list){ const A = mkAll(); list.forEach(([a, b, t]) => { A[mkcKey(uid, 'q', a, b, t, 'x')] = { ts: new Date().toISOString() }; }); MKS = A; lsWrite(MK_KEY, A, '하네스'); return true; },
  /* 조문 */
  lines(){ return [...document.querySelectorAll('#slot .box .ln')].map(l => ({ r: R(l), t: plain(l), wm: !!l._wm, jmk: l.querySelectorAll('span.jmk').length, dmn: l.querySelectorAll('.dmn').length })); },
  lineSel(i){ const L = [...document.querySelectorAll('#slot .box .ln')][i]; if (!L) return null; L.id = '__mfl' + i; return '#__mfl' + i; },
  jm(){ try{ return JSON.parse(localStorage.getItem('jopangi.jomark') || '{}'); }catch(e){ return {}; } },
  jmSeed(k, v){ const A = __MF.jm(); A[k] = v; localStorage.setItem('jopangi.jomark', JSON.stringify(A)); try{ recDropCache(); }catch(e){} return true; },
  rowKeyOf(i){ try{ const L = [...document.querySelectorAll('#slot .box .ln')][i]; const ri = L._wm ? L._wm.ri : +L.dataset.ri; const j = (window.__MFJ || {}); return j.rows ? rowKey(j.rows[ri]) : null; }catch(e){ return null; } },
  inkSeed(key){ const A = JSON.parse(localStorage.getItem('jopangi.ink') || '{}'); A[key] = { s: [{ c: '#e11d48', w: 2, p: [[0.1, 0.1, 1], [0.3, 0.2, 1]] }], ts: new Date().toISOString() }; localStorage.setItem('jopangi.ink', JSON.stringify(A)); try{ recDropCache(); }catch(e){} return true; },
  bub(){ return !!document.getElementById('stkbub'); },
  pops(){ return (typeof POPS !== 'undefined' ? POPS : []).map(p => p._pk || ''); },
  /* 조문 팝업 — 볼트 마크업 요소(빨간 글·칠·밑줄·굵게·태그) 수 · 내 칠 · 다만 */
  popMarks(pre){ const p = (typeof POPS !== 'undefined' ? POPS : []).filter(x => (x._pk || '').indexOf(pre) === 0).pop(); if (!p) return null; const b = p.querySelector('.pb') || p;
    const q = [...b.querySelectorAll('.ln mark, .ln u, .ln s, .ln strong, .ln span[style*="color"], .ln .badge, .ln .stkw2')].filter(e => !e.closest('.dmn') && !e.classList.contains('dmn') && !e.classList.contains('jmk'));
    return { n: q.length, jmk: b.querySelectorAll('span.jmk').length, dmnbr: b.querySelectorAll('.dmn.dmnbr').length, txt: q.slice(0, 4).map(txt) }; },
  /* 「다만,」 줄 — 자리 · 굵기 · 색 */
  dmn(root){ const R0 = document.querySelector(root || '#slot'); if (!R0) return null; const out = [];
    R0.querySelectorAll('.dmn.dmnbr').forEach(d => { const L = d.closest('.ln') || d.parentElement.closest('div'); const s = plain(L); const i0 = s.search(/\S/);
      const r0 = i0 >= 0 ? charRect(L, i0) : null; let rd = R(d); { const tn = [...d.childNodes].find(x => x.nodeType === 3); if (tn){ const g = document.createRange(); g.selectNodeContents(tn); const q = g.getClientRects(); const z = q[q.length - 1] || g.getBoundingClientRect(); rd = { x: z.left, y: z.top }; } }   /* 「다」 글자 자리(::before 줄바꿈 뺌) */ let prevTop = null;
      { let k = 0; const nodes = textNodes(L); const st = s.indexOf('다만,'); for (let c = st - 1; c >= 0; c--){ if (/\S/.test(s[c])){ const q = charRect(L, c); prevTop = q && q.y; break; } } }
      const cs = getComputedStyle(d); out.push({ top: rd.y, prevTop, left: rd.x, rowX: r0 && r0.x, fw: cs.fontWeight, color: cs.color, ind: d.dataset.ind || '' }); });
    const starts = [...R0.querySelectorAll('.dmn:not(.dmnbr)')].filter(d => d.textContent === '다' ).length;
    return { br: out, head: starts }; },
  lineTexts(root){ return [...document.querySelectorAll((root || '#slot .box') + ' .ln')].map(l => l.textContent); },
};
})();
