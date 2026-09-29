/* _harness_jo_uid_add3_tests.js — _task_jo_gaek_uid_add3 하네스가 페이지에 넣는 도구(__U3).
   NEW·BASE 둘 다에 같은 것을 넣는다 — 없는 함수(giSeatBoot …)는 빈 값(헛잣대).
   ⚠ 누름은 여기서 안 한다 — 자리만 돌려주고 파이썬이 page.mouse · 터치로 누른다. */
(function(){
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const vis = e => !!e && getComputedStyle(e).display !== 'none' && e.getBoundingClientRect().height > 0;
const has = n => { try{ return typeof eval(n) !== 'undefined'; }catch(e){ return false; } };
function hitOn(t){ if (!t) return null; try{ t.scrollIntoView({ block: 'center', inline: 'nearest' }); }catch(e){}
  const r = t.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2, at = document.elementFromPoint(cx, cy);
  return { cx, cy, w: r.width, h: r.height, on: !!at && (at === t || t.contains(at)) && cy > 0 && cy < innerHeight, vis: vis(t) }; }
window.__U3 = {
  has(n){ return has(n); },
  /* 기출뷰 기록 — 심기(옛 열쇠 · 새 열쇠) · 읽기 · 동기화 도장 */
  seedGi(o){ const G = giAll(); Object.keys(o).forEach(k => { if (o[k] === null) delete G[k]; else G[k] = o[k]; }); GIREC = G; lsWrite(GI_KEY, G, '하네스'); return Object.keys(G).length; },
  gi(keys){ const G = giAll(); const o = {}; keys.forEach(k => { o[k] = G[k] || null; }); return o; },
  stamps(keys){ const g = sObj(SG_KEY), u = sObj(SU_KEY); const o = {}; keys.forEach(k => { o[k] = { gone: !!g[ckey(GI_KEY, k)], u: !!u[ckey(GI_KEY, k)] }; }); return o; },
  seat(){ return has('GISEAT') ? (GISEAT ? GISEAT.length : GISEAT) : 'none'; },
  /* 기출뷰 — 첫 화면 해 줄 · 쪽 머리 · 문항 칸 */
  yearRow(y){ const r = document.querySelector('#slot .mbur[data-giy="' + y + '"] .nm'); return r ? hitOn(r) : null; },
  exv(){ const h = document.querySelector('#slot .mbsbar'); return { head: txt(h), qs: [...document.querySelectorAll('#slot .exv-q')].map(q => ({ k: q.dataset.exq, no: q.dataset.exno, vis: vis(q), head: txt(q.querySelector('.exv-head')).slice(0, 50) })) }; },
  exvQ(k){ const q = document.querySelector('#slot .exv-q[data-exq="' + k + '"]'); return q ? { vis: vis(q), no: q.dataset.exno, head: txt(q.querySelector('.exv-head')).slice(0, 60), boxes: q.querySelectorAll('.question-box').length } : null; },
  next(){ const b = document.querySelector('#slot [data-uzexnext]'); return b ? hitOn(b) : null; },
  grade(){ const b = document.querySelector('#slot [data-uzexgrade]'); return b ? hitOn(b) : null; },
  yearOf(y){ return { year: has('giYearOf') ? giYearOf(y) : null, grnd: has('grndList') ? grndList(y).map(r => ({ ok: r.ok, n: r.n })) : null }; },
  gradable(y){ return ((VJ && VJ.qs) || []).filter(q => String(q.연도) === String(y) && giGradable(q)).length; },
  /* 지문 열쇠 · 흡수 · 같은 uid 카드 수 */
  keyOf(qid, n){ const q = ((VJ && VJ.qs) || []).find(x => x.id === qid); if (!q) return null; const z = (q.지문 || []).find(x => String(x.n) === String(n)); return z ? oxKeyLid(q, z) : null; },
  uidCards(uid){ return [...document.querySelectorAll('#slot .qwrap')].filter(c => txt(c.querySelector('.qb.id')) === uid && vis(c)).length; },
  /* 흡수 갈래 — 문항 id 로 곧장(__HM.absorbedCheck 는 「시험문번 또는 문번」으로 찾아 같은 해 리담 순번 18 을 잡는다) */
  absorbed(qid){ const q = ((VJ && VJ.qs) || []).find(x => x.id === qid); if (!q) return null;
    return (q.지문 || []).map(z => { const p7 = Object.values(VJ.P7map || {}).find(p => p.uid === z.uid);
      return { n: String(z.n), uid: z.uid, cls: has('mlnClass') ? mlnClass(q, z) : null, p7: p7 ? p7.id : null }; }); },
  /* 채점 앞 — 그 해 정답 있는 문항에 답을 심는다(누름 관문은 「채점」 단추 하나) */
  pickAll(y){ const G = giAll(); let n = 0; ((VJ && VJ.qs) || []).filter(q => String(q.연도) === String(y) && giGradable(q)).forEach(q => { G[giKey(q)] = Object.assign({}, G[giKey(q)] || {}, { p: '1', ts: new Date().toISOString() }); n++; });
    GIREC = G; lsWrite(GI_KEY, G, '하네스'); return n; },
  exvChip(k, re){ const q = document.querySelector('#slot .exv-q[data-exq="' + k + '"]'); if (!q) return null; const rx = new RegExp(re);
    const b = [...q.querySelectorAll('.jxec')].find(x => rx.test(txt(x))); return b ? Object.assign(hitOn(b), { t: txt(b), cls: b.className }) : { none: true, chips: [...q.querySelectorAll('.jxec')].map(txt) }; },
  qOf(qid){ const q = ((VJ && VJ.qs) || []).find(x => x.id === qid); return q ? { 연도: q.연도, 회차: q.회차, 시험문번: q.시험문번, giOld: q.giOld || null } : null; },
};
})();
