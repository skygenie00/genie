/* _harness_jo_gaek_mbsame_tests.js — _task_jo_gaek_mbsame(+add1) 하네스가 페이지에 넣는 도구(__HM).
   BASE(genie HEAD 17094a5 = uid 판)·NEW 둘 다에 같은 것을 넣는다 — 없는 함수(MLN · jxeChips · grndList …)는 빈 값(헛잣대).
   보임 = computed display ≠ none 그리고 높이 > 0(그리고 부모에 안 잘림) · 자리 = getBoundingClientRect + elementFromPoint.
   ⚠ 누름은 여기서 안 한다 — 자리만 돌려주고 파이썬이 page.mouse · CDP 터치로 누른다. */
(function(){
const wait = ms => new Promise(r => setTimeout(r, ms));
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const has = n => { try{ return typeof eval(n) !== 'undefined'; }catch(e){ return false; } };
const vis = e => !!e && e.isConnected && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden' && e.getBoundingClientRect().height > 0;
const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); return { x: +r.left.toFixed(2), y: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2), cx: +(r.left + r.width / 2).toFixed(2), cy: +(r.top + r.height / 2).toFixed(2) }; };
function hitOn(t){ if (!t) return null; try{ t.scrollIntoView({ block: 'center', inline: 'nearest' }); }catch(e){}
  const r = R(t), at = document.elementFromPoint(r.cx, r.cy);
  const onScreen = r.cy > 0 && r.cy < innerHeight && r.cx > 0 && r.cx < innerWidth && r.w > 0 && r.h > 0;
  return Object.assign(r, { on: !!at && (at === t || t.contains(at)) && onScreen, onScreen, vis: vis(t), tag: at ? at.tagName + '.' + at.className : null }); }
async function idle(){ for (let i = 0; i < 400 && (typeof busy !== 'undefined' && busy); i++) await wait(25); }
async function until(f, ms){ const t0 = Date.now(); while (Date.now() - t0 < (ms || 8000)){ try{ const v = f(); if (v) return v; }catch(e){} await wait(40); } try{ return f(); }catch(e){ return null; } }
const pops = () => (typeof POPS !== 'undefined' ? POPS : []);
window.__TOASTS = window.__TOASTS || [];
try{ new MutationObserver(ms => ms.forEach(m => m.addedNodes.forEach(n => { if (n.nodeType === 1 && n.classList && n.classList.contains('toast')) window.__TOASTS.push(txt(n)); }))).observe(document.documentElement, { childList: true, subtree: true }); }catch(e){}
const labOf = i => { const M = VJ.M; return ((M[i].no ? M[i].no + (M[i].깊이 === 1 ? '. ' : ' ') : '') + M[i].제목); };
window.__HM = {
  wait,
  errs(){ return (window.__ERR || []).filter(e => !/^ResizeObserver loop/.test(e)).slice(0, 20); },
  toasts(){ return window.__TOASTS.slice(-6); },
  ok(){ return { mln: has('MLN') && !!MLN && !!MLN.ok, jxe: has('jxeChips'), grnd: has('grndList'), rgn: has('rgnStrip'), mdp: has('mdpHead') }; },
  async home(law){ try{ closeAllPops(); }catch(e){}
    S.law = law || '특허법'; S.tab = 'jimun'; S.jimunTab = 'ox'; S.mok = ''; S.oxQueue = ''; S.oxQ = ''; S.oxQMode = 'q'; S.year = '';
    await idle(); await render(); await idle();
    await until(() => (S.law !== '특허법' || (OXPOOL && Object.keys(OXPOOL).length > 300)) && document.querySelector('#slot .mbdash'), 30000);
    await wait(200); return { law: S.law, pool: Object.keys(OXPOOL || {}).length }; },
  async go(sel){ try{ closeAllPops(); }catch(e){} S.jimunTab = 'ox'; S.oxQueue = ''; S.mok = sel; S.oxPage = null; await idle(); await render(); await idle(); await wait(250); return S.mok; },
  async page(p){ S.oxPage = p; await render(); await idle(); await wait(150); },
  nodeIdx(no){ return (VJ.M || []).findIndex(n => String(n.no) === String(no)); },
  nodeByTitle(re){ const rx = new RegExp(re); return (VJ.M || []).findIndex(n => rx.test(n.제목 || '')); },
  /* ── 1 단원 줄 셈(데이터 셈 · 서랍 · 첫 화면 · 히트맵) ── */
  lineCensus(){
    if (!(has('MLN') && MLN.ok)) return { ok: false };
    const M = VJ.M, out = { nodes: 0, b: 0, n: 0, u: 0, v: 0, absorbed: 0, lidPlaced: 0, vAbs: 0, bad: [] };
    const placed = new Set(); M.forEach(n => (n.리담 || []).forEach(x => placed.add(x)));
    (VJ.qs || []).forEach(q => { if (!placed.has(q.id)) return; (q.지문 || []).forEach(z => { out.lidPlaced++; const c = mlnClass(q, z);
      if (c === 'a') out.absorbed++; if (c === 'v' && MLN.p7uid.has(z.uid)) out.vAbs++; }); });
    M.forEach((n, i) => { const d = mlnDirect(M, i, VJ.P7map, VJ.byId); out.nodes++; out.b += d.b.length; out.n += d.n.length; out.u += d.u.length; out.u8 = (out.u8 || 0) + d.u.filter(c => c.kind !== 'Z').length; out.v += d.v.length; });
    /* 리담 선지는 붙은 마디(들)마다 한 번 — 한 문항이 두 마디에 붙으면 두 번 센다 */
    let lidSeen = 0; M.forEach(n => (n.리담 || []).forEach(id => { const q = VJ.byId[id]; if (q) lidSeen += (q.지문 || []).length; }));
    let absSeen = 0; M.forEach(n => (n.리담 || []).forEach(id => { const q = VJ.byId[id]; if (q) (q.지문 || []).forEach(z => { if (mlnClass(q, z) === 'a') absSeen++; }); }));
    out.lidSeen = lidSeen; out.absSeen = absSeen; out.sumOK = (out.u - (out.u8 || 0) + out.v + absSeen) === lidSeen;   /* ★ A-6(a) 9/30 — p8up A-1-9: (미수록) 줄에 선 8판 새 카드(kind ≠ Z · 19)는 리담 선지가 아니다 */
    return out;
  },
  /* add1 머리 셈 쪼개 보기 — 그 마디와 아래 전부의 줄 셈(본편 · 미수록 · 변형) · 붙은 리담 선지 중 흡수(본편 제7판 줄로 감) */
  subCensus(no){
    if (!(has('MLN') && MLN.ok)) return null;
    const M = VJ.M, s = String(no), o = { nodes: 0, b: 0, u: 0, v: 0, lid: 0, abs: 0 };
    M.forEach((n, i) => { const x = String(n.no || ''); if (x !== s && x.indexOf(s + '.') !== 0) return;
      const d = mlnDirect(M, i, VJ.P7map, VJ.byId); o.nodes++; o.b += d.b.length; o.u += d.u.length; o.v += d.v.length;
      (n.리담 || []).forEach(id => { const q = VJ.byId[id]; if (q) (q.지문 || []).forEach(z => { o.lid++; if (mlnClass(q, z) === 'a') o.abs++; }); }); });
    return o;
  },
  firstScreenCounts(){
    const rows = [...document.querySelectorAll('#slot .mbur')], out = {};
    rows.forEach(r => { const nm = txt(r.querySelector('.nm')), m = /총 (\d+)문제/.exec(txt(r)); if (nm && m) out[nm] = +m[1]; });
    const lines = rows.filter(r => /\((미수록|변형|판신설)\)$/.test(txt(r.querySelector('.nm')))).length;
    return { rows: rows.length, lines: lines, map: out };
  },
  drawerCounts(){
    const out = {}; [...document.querySelectorAll('#jtlist .jtit')].forEach(r => { const nm = txt(r.querySelector('.tx')), n = txt(r.querySelector('.n')); if (nm) out[nm] = +n; });
    [...document.querySelectorAll('#jtlist .jtch')].forEach(r => { const nm = txt(r.querySelector('.jtnm')), n = txt(r.querySelector(':scope > .n')); if (nm) out['H:' + nm] = +n; });
    return out;
  },
  heatTotal(){ const P = OXPOOL || {}; return Object.keys(P).length; },
  lineKeysNode(i){ if (!(has('MLN') && MLN.ok)) return null; const d = mlnDirect(VJ.M, i, VJ.P7map, VJ.byId); const o = {}; ['b', 'n', 'u', 'v'].forEach(l => { o[l] = d[l].map(mlnCardKey); }); return o; },
  /* ── 2 한 지문 = 한 카드 ── */
  unitCards(){
    const cards = [...document.querySelectorAll('#slot .main .qwrap, #slot .qwrap')].filter((c, i, a) => a.indexOf(c) === i);
    const qcard = cards.filter(c => /^qb-\d{4}-\d+-/.test(c.id || '') || (c.querySelector(':scope > .qhd .src') && !c.classList.contains('mlnz'))).length;
    return { n: cards.length, qcard: qcard, ids: cards.map(c => c.id), kinds: cards.map(c => c.classList.contains('mlnz') ? 'Z' : c.classList.contains('mlno') ? 'O' : 'P'),
             labs: cards.map(c => txt(c.querySelector('.mlnbk, .oxseq'))), boxes: document.querySelectorAll('#slot .p7case').length };
  },
  sunOrder(){ const ids = [...document.querySelectorAll('#slot .qwrap')].map(c => c.id.replace(/^qb-/, ''));
    const P = {}; Object.values(VJ.P7map).forEach(z => { P[oxKeyP7(z)] = z; });
    const suns = ids.map(k => (P[k] || {}).순).filter(x => x != null); let ok = true; for (let i = 1; i < suns.length; i++) if (suns[i] < suns[i - 1]) ok = false; return { ok, n: suns.length }; },
  absorbedCheck(yr, no, sel){   /* 리담 yr-no 번째 문항의 선지 sel 이 본편에 흡수(따로 카드 없음)인가 */
    const q = (VJ.qs || []).find(x => String(x.연도) === String(yr) && (String(x.시험문번) === String(no) || String(x.문번) === String(no)));
    if (!q) return { q: null };
    const z = (q.지문 || []).find(x => String(x.n) === String(sel)); if (!z) return { q: q.id, z: null };
    const k = oxKeyLid(q, z), p7 = Object.values(VJ.P7map).find(p => p.uid === z.uid);
    return { q: q.id, uid: z.uid, cls: has('mlnClass') ? mlnClass(q, z) : null, p7: p7 ? p7.id : null, p7bk: p7 ? p7.책번호 : null, zcard: !!document.getElementById('qb-' + k) && document.getElementById('qb-' + k).classList.contains('mlnz') };
  },
  /* ── 3·4 카드 번호 · 칩 차례 ── */
  cardInfo(key){
    const c = document.getElementById('qb-' + key); if (!c) return null;
    const head = c.querySelector('.mbqhd') || c.querySelector('.qhd');
    const seq = [];
    head && [...head.querySelectorAll('button, span.mbtype, b.oxseq')].forEach(b => { if (b.closest('.mbtags') || b.closest('div.t')) return;
      const t = txt(b); let k = 'x';
      if (b.classList.contains('oxseq')) k = '순번'; else if (b.classList.contains('mbtype')) k = '유형'; else if (b.classList.contains('jxec')) k = (b.classList.contains('sp') ? '상표칩' : '출제연도');
      else if (b.classList.contains('id')) k = 'ID'; else if (b.classList.contains('qexp')) k = '제7판'; else if (/^🃏/.test(t)) k = '🃏';
      else if (/^📎/.test(t)) k = '📎'; else if (/^📖/.test(t)) k = '📖'; else if (/^🔗/.test(t)) k = '🔗'; else if (/^↩/.test(t)) k = '↩';
      else if (b.classList.contains('v')) k = '출처'; else if (b.closest('.mbtype')) return;
      seq.push([k, t.slice(0, 20)]); });
    const tags = c.querySelector('.mbtags, .mbqhd > div.t');   /* 오른쪽 아이콘 묶음(칩 「qb t」 와 헷갈리지 않게 div) */
    const icons = tags ? [...tags.querySelectorAll('button, span')].filter(x => x.children.length === 0).map(txt).filter(Boolean) : [];
    return { seq: seq, icons: icons, bk: txt(c.querySelector('.mlnbk')), head: txt(head).slice(0, 120), hasSeqHead: !!(head && head.querySelector('b.oxseq')) };
  },
  findP7(pred){ const z = Object.values(VJ.P7map).find(pred); return z ? { id: z.id, key: oxKeyP7(z), bk: z.책번호, pdf: z.pdf쪽, node: has('MLN') && MLN.ok ? MLN.p7node[z.id] : null } : null; },
  p7ByPdf(pdf, re){ const rx = new RegExp(re || '.'); return Object.values(VJ.P7map).filter(z => String(z.pdf쪽) === String(pdf) && rx.test(String(z.책번호 || ''))).map(z => ({ id: z.id, key: oxKeyP7(z), bk: z.책번호, uid: z.uid, 문항: z.문항 || null, 선지: z.선지 || null })); },
  nodeOfKey(key){ const m = (typeof MBK2M !== 'undefined' && MBK2M || {})[key]; return m ? m.sel : null; },
  async goKey(key){ const P = (OXPOOL || {})[key]; if (!P) return { ok: false };
    const sel = (has('MLN') && MLN.ok) ? ((P.kind === 'L' ? (() => { const ix = MLN.lidnode[P.id]; return ix == null ? null : mlnSel(ix, P.ln || 'u'); })() : (() => { const ix = MLN.p7node[P.id]; return ix == null ? null : '__mg' + ix; })())) : null;
    if (!sel) return { ok: false, P };
    await this.go(sel);
    const dom = P.dom; const pg = (OXDOMPG || {})[dom]; if (pg != null && pg !== S.oxPage) await this.page(pg);
    return { ok: !!document.getElementById(dom), sel, dom }; },
  at(sel, i){ const e = document.querySelectorAll(sel)[i || 0]; return e ? hitOn(e) : null; },
  atIn(root, sel){ const r = typeof root === 'string' ? document.querySelector(root) : root; const e = r && r.querySelector(sel); return e ? hitOn(e) : null; },
  chipAt(key, re){ const c = document.getElementById('qb-' + key); if (!c) return null; const rx = new RegExp(re);
    const b = [...c.querySelectorAll('.jxec')].find(x => rx.test(txt(x))); return b ? Object.assign(hitOn(b), { t: txt(b), cls: b.className }) : null; },
  chips(key){ const c = document.getElementById('qb-' + key); return c ? [...c.querySelectorAll('.jxec')].map(b => [txt(b), b.className, vis(b)]) : null; },
  btnIn(key, re){ const c = document.getElementById('qb-' + key); if (!c) return null; const rx = new RegExp(re);
    const b = [...c.querySelectorAll('button')].find(x => rx.test(txt(x))); return b ? Object.assign(hitOn(b), { t: txt(b) }) : null; },
  popKeys(){ return pops().map(p => p._pk); },
  pop(re){ const rx = new RegExp(re); const p = pops().find(x => rx.test(x._pk || '')); if (!p) return null;
    return { pk: p._pk, vis: vis(p), t: txt(p).slice(0, 200), bd: p.querySelectorAll('.jxe-bd').length, bn: p.querySelectorAll('.jxe-bn').length,
             bdVis: [...p.querySelectorAll('.jxe-bd')].some(vis), canvas: p.querySelectorAll('canvas').length, nav: txt(p.querySelector('.jxe-nav')) }; },
  closeAll(){ try{ closeAllPops(); }catch(e){} return pops().length; },
  jxeLast(){ return has('JXE') ? { last: JXE.last || null, idx: JXE.stat.idx, list: JXE.stat.list } : null; },
  async jxeIdx(law, y){ if (!has('jxeIndex')) return null; const key = JXE_LAWF[law], f = jxeFile(law, y); try{ const r = await jxeIndex(key, f); return { found: Object.keys(r.no).length, miss: r.miss, pages: r.pages }; }catch(e){ return { err: String(e.message || e) }; } },
  async jxeLists(){ const o = {}; for (const k of ['teukheo', 'sangpyo', 'dibo']){ try{ const r = await fetch('../gichul/pdf/list_' + k + '.json', { cache: 'no-cache' }); o[k] = r.ok ? ((await r.json()).items || []).length : r.status; }catch(e){ o[k] = 'err'; } } return o; },
  /* ── 8 기출뷰 ── */
  async gi(y){ try{ closeAllPops(); }catch(e){} S.jimunTab = 'gichul'; S.year = String(y); S.mok = ''; S.omr = false; S.giWrong = false; await idle(); await render(); await idle(); await wait(250);
    return { n: document.querySelectorAll('[id^="gi-"]').length }; },
  giFirst(){ const c = document.querySelector('[id^="gi-"]'); return c ? c.id : null; },
  giNumAt(cid, n){ const c = document.getElementById(cid); if (!c) return null; const b = c.querySelectorAll('.gich .ginum')[n - 1]; return b ? hitOn(b) : null; },
  giState(cid){ const c = document.getElementById(cid); if (!c) return null; const rows = [...c.querySelectorAll('.gich')];
    return { sel: rows.map(r => r.classList.contains('sel')), res: txt(c.querySelector('.gires')), resVis: vis(c.querySelector('.gires')), headBadge: [...c.querySelectorAll('.jhd .qb')].map(txt),
             stb: c.querySelectorAll('.gistb').length }; },
  async omrOpen(y){ S.omr = true; await render(); await wait(200); return !!document.querySelector('.omk'); },
  omk(){ const w = document.querySelector('.omk'); return w ? { t: txt(w.querySelector('.t')), over: w.classList.contains('over'), ov: txt(w.querySelector('.ov')), tColor: getComputedStyle(w.querySelector('.t')).color,
    rs: w.querySelector('.rs') ? { hidden: w.querySelector('.rs').hidden, sure: w.querySelector('.rs').classList.contains('sure') } : null } : null; },
  omkBtn(which){ const w = document.querySelector('.omk'); if (!w) return null; const b = which === 'rs' ? w.querySelector('.rs') : w.querySelector('.pl'); return b ? hitOn(b) : null; },
  omkFake(y, ms){ const A = omkAll(); A[giYKey(y)] = { acc: ms, run: 0 }; omkSave(A); const w = document.querySelector('.omk'); if (w && w._paint) w._paint(); return omkMs(y); },
  grnd(y){ return has('grndList') ? grndList(y).map(r => ({ ok: r.ok, n: r.n, ms: r.ms, np: Object.keys(r.picks || {}).length, mig: !!r.mig })) : null; },
  giSubmitAt(){ const b = [...document.querySelectorAll('#slot .modebar button, .omrft button')].find(x => /제출/.test(txt(x))); return b ? hitOn(b) : null; },
  giResetAt(){ const b = [...document.querySelectorAll('#slot .modebar button')].find(x => /다시 풀기/.test(txt(x))); return b ? hitOn(b) : null; },
  stmtBtnAt(cid, zi, v){ const c = document.getElementById(cid); if (!c) return null; const g = c.querySelectorAll('.gistb')[zi]; if (!g) return null;
    const b = [...g.querySelectorAll('button')].find(x => txt(x) === v); return b ? hitOn(b) : null; },
  oxRec(k){ return (typeof oxOf === 'function' ? oxOf(k) : null) || null; },
  oxState(k){ return typeof oxState === 'function' ? oxState(k) : null; },
  weakHas(k){ try{ return oxQueueHas(k, 'weak'); }catch(e){ return null; } },
  giCardKeys(cid){ const q = (VJ.qs || []).find(x => 'gi-' + giKey(x) === cid); return q ? (q.지문 || []).map(z => oxKeyLid(q, z)) : []; },
  /* ── 9 첫 화면 기출 줄 ── */
  giRow(y){ const r = document.querySelector('#slot .mbur[data-giy="' + y + '"]'); if (!r) return null;
    return { t: txt(r), boxes: [...r.querySelectorAll('.grbx')].map(b => ({ t: txt(b), ov: !!b.querySelector('.ov'), ovColor: b.querySelector('.ov') ? getComputedStyle(b.querySelector('.ov')).color : null })),
             run: txt(r.querySelector('.grrun')), go: txt(r.querySelector('.mbgo')), jn: !!r.querySelector('.mbchip.jn'), tot: txt(r.querySelector('.tot')) }; },
  giRowJn(y){ const r = document.querySelector('#slot .mbur[data-giy="' + y + '"]'); const b = r && r.querySelector('.mbchip.jn'); return b ? hitOn(b) : null; },
  /* ★ mbsame_add3 §A-2(9/27) — 새 기출뷰 = 민법 exv 틀(문항 .exv-q[data-exq] · 고르기 [data-exk][data-exn] · 결과 .exv-res · 채점 뒤 지문 O/X .exv-post-ox .mboxb) — 옛 관문이 같은 것을 새 틀에서 잰다 */
  exvOn(){ return !!document.querySelector('.exv-paper.uzexv'); },
  exvKeys(){ return [...document.querySelectorAll('.exv-paper.uzexv .exv-q')].map(q => q.dataset.exq); },
  exvNumAt(key, n){ const q = document.querySelector('.exv-q[data-exq="' + key + '"]'); if (!q) return null; const b = q.querySelector('[data-exk][data-exn="' + n + '"]'); return b ? hitOn(b) : null; },
  exvState(key){ const q = document.querySelector('.exv-q[data-exq="' + key + '"]'); if (!q) return null; const r = q.querySelector('.exv-res');
    return { sel: [...q.querySelectorAll('[data-exk]')].filter(b => b.classList.contains('sel')).map(b => +b.dataset.exn), res: txt(r), resVis: !!r && vis(r) && txt(r).length > 0, headBadge: [...q.querySelectorAll('.exv-head .qb')].map(txt) }; },
  exvPostOx(key, zi, v){ const q = document.querySelector('.exv-q[data-exq="' + key + '"]'); if (!q) return null; const bx = q.querySelectorAll('.uzexb')[zi]; if (!bx) return null;
    const b = [...bx.querySelectorAll('.exv-post-ox .mboxb')].find(x => txt(x) === v); return b ? hitOn(b) : null; },
  exvCardKeys(key){ const q = (VJ.qs || []).find(x => giKey(x) === key); return q ? (q.지문 || []).map(z => oxKeyLid(q, z)) : []; },
  omrSubmitAt(){ const b = [...document.querySelectorAll('.omrft button')].find(x => /제출/.test(txt(x))); return b ? hitOn(b) : null; },
  grndFake(y, recs){ const A = grndAll(); A[giYKey(y)] = recs; GRNDREC = A; lsWrite(GRND_KEY, A, '기출 회독'); return grndList(y).length; },
  /* ── 10 기록 칸 ── */
  rndFake(scope, key, ok, date){ const A = rndAll(); const L = (A[scope] || []).slice();
    L.push({ n: L.length + 1, date: date, ts: date + 'T01:00:00Z', total: 1, done: 1, right: ok ? 1 : 0, wrong: ok ? 0 : 1, confuse: 0, semi: 0, fake: 0,
             wrongK: ok ? [] : [key], confuseK: [], semiK: [], rightK: ok ? [key] : [], allK: [key] });
    A[scope] = L; RNDREC = A; lsWrite(RND_KEY, A, '회독'); try{ MBRIDX = null; }catch(e){} return L.length; },
  rndOf(scope){ return (rndAll()[scope] || []).map(r => ({ n: r.n, all: (r.allK || []).length, wrong: r.wrong, w: (r.wrongK || []).length })); },
  gone(){ return has('rgnAll') ? Object.keys(rgnAll()) : null; },
  syncKeys(){ return typeof SYNC_KEYS !== 'undefined' ? SYNC_KEYS.slice() : null; },
  stripOpen(key){ const c = document.getElementById('qb-' + key); if (!c) return null; const sb = c.querySelector('.mbqhd .qb.v, .qhd .qb.v'); return sb ? hitOn(sb) : null; },
  /* 기록 칸 단추 꼴 — span 칸(.mbrec .c)과 같은가 · extra = 헛잣대로 얹을 규칙 */
  rgbStyle(key, extra){ const c = document.getElementById('qb-' + key); const b = c && c.querySelector('.mbrecw .rgb'); if (!b) return null;
    let st = null; if (extra){ st = document.createElement('style'); st.textContent = extra; document.head.appendChild(st); }
    const s = getComputedStyle(b), r = b.getBoundingClientRect();
    const o = { fw: s.fontWeight, bw: s.borderTopWidth, bs: s.borderTopStyle, bc: s.borderTopColor, fs: s.fontSize, w: Math.round(r.width), h: Math.round(r.height), cls: b.className, t: b.textContent };
    if (st) st.remove(); return o; },
  stripCells(key){ const c = document.getElementById('qb-' + key); const w = c && c.querySelector('.mbrecw'); if (!w) return null;
    return { open: !w.classList.contains('hide'), cells: [...w.querySelectorAll('.c')].map(x => [txt(x), x.tagName, x.className]), info: txt(w.querySelector('.rgi')), infoVis: vis(w.querySelector('.rgi')) }; },
  stripCellAt(key, i){ const c = document.getElementById('qb-' + key); const b = c && c.querySelectorAll('.mbrecw .rgb')[i || 0]; return b ? hitOn(b) : null; },
  stripXAt(key){ const c = document.getElementById('qb-' + key); const b = c && c.querySelector('.mbrecw .rgx'); return b ? Object.assign(hitOn(b), { sure: b.classList.contains('sure') }) : null; },
  sweep(){ return has('rgnSweep') ? rgnSweep() : null; },
  /* ── 13 정리 창 ── */
  rowJnAt(sel){ const r = [...document.querySelectorAll('#slot .mbur')].find(x => { const b = x.querySelector('.mbgo'); return x.querySelector('.mbchip.jn') && x.onclick && (x.__sel === sel); });
    return r ? hitOn(r.querySelector('.mbchip.jn')) : null; },
  rowByName(nm){ const r = [...document.querySelectorAll('#slot .mbur')].find(x => txt(x.querySelector('.nm')) === nm); return r ? hitOn(r) : null; },
  rowJnByName(nm){ const r = [...document.querySelectorAll('#slot .mbur')].find(x => txt(x.querySelector('.nm')) === nm); const b = r && r.querySelector('.mbchip.jn'); return b ? hitOn(b) : null; },
  jnWin(re){ const rx = new RegExp(re); const p = pops().find(x => rx.test(x._pk || '')); if (!p) return null;
    const rows = [...p.querySelectorAll('.jnr')];
    return { vis: vis(p), rows: rows.length, qn: p.querySelectorAll('.jnxq').length, grc: p.querySelectorAll('.jnxq .grc').length, tg: !!p.querySelector('.jnxtg'), off: p.classList.contains('jnxoff'),
             chipAfterNo: rows.slice(0, 3).map(r => { const t = r.querySelector('.jntop'); const kids = t ? [...t.children] : []; const i = kids.findIndex(x => x.classList.contains('jnno')); return kids[i + 1] ? kids[i + 1].className : null; }),
             strip: rows.slice(0, 3).map(r => !!r.querySelector('.mbrec')), jnrec: p.querySelectorAll('.jnrec').length,
             marks: [...p.querySelectorAll('mark.mkc')].slice(0, 3).map(m => { const c = getComputedStyle(m); return (c.backgroundImage && c.backgroundImage !== 'none') ? c.backgroundImage : c.backgroundColor; }) }; },   /* ★ jo_markfix(9/29) — 칠 꼴 = 배경 그림(linear-gradient · 민법·2차 꼴)이라 색만 보면 늘 투명 · 그림이 있으면 그것 */
  jnInWin(re, sel, i){ const rx = new RegExp(re); const p = pops().find(x => rx.test(x._pk || '')); const e = p && p.querySelectorAll(sel)[i || 0]; return e ? Object.assign(hitOn(e), { t: txt(e) }) : null; },
  jnGri(re){ const rx = new RegExp(re); const p = pops().find(x => rx.test(x._pk || '')); const e = p && p.querySelector('.jnxq .gri'); return e ? { t: txt(e), vis: vis(e) && txt(e).length > 0 } : null; },
  jnRowRecInfo(re){ const rx = new RegExp(re); const p = pops().find(x => rx.test(x._pk || '')); const e = p && p.querySelector('.jnr .rgi'); return e ? { t: txt(e), vis: vis(e) } : null; },
  mkPut(key){ try{ const A = mkAll(); A[mkcKey(key, 'q', 0, 4, 'y', '하네스')] = { ts: nowIso() }; MKS = A; lsWrite(MK_KEY, A, '형광펜'); return Object.keys(A).length; }catch(e){ return String(e); } },
  /* ── add1 깊이 ── */
  head(no){ const i = this.nodeIdx(no); const r = document.querySelector('#slot .mbur.mdph[data-mdp="' + i + '"]'); if (!r) return null;
    const nm = r.querySelector('.nm'); return Object.assign(hitOn(r.querySelector('.mdpar') || r), { t: txt(r), i: i, fw: nm ? getComputedStyle(nm).fontWeight : null, fs: nm ? getComputedStyle(nm).fontSize : null, nmx: nm ? nm.getBoundingClientRect().left : null }); },
  headName(no){ const i = this.nodeIdx(no); const r = document.querySelector('#slot .mbur.mdph[data-mdp="' + i + '"] .nm'); return r ? hitOn(r) : null; },
  kidRows(no){ const i = this.nodeIdx(no), M = VJ.M, d = M[i].깊이; const names = [];
    for (let j = i + 1; j < M.length && M[j].깊이 > d; j++) names.push(labOf(j));
    const rows = [...document.querySelectorAll('#slot .mbur')];
    return names.map(nm => { const r = rows.find(x => txt(x.querySelector('.nm')) === nm); return r ? { nm, vis: vis(r), x: r.querySelector('.nm').getBoundingClientRect().left, line: getComputedStyle(r).boxShadow } : { nm, vis: false }; }); },
  mbCh(){ return JSON.stringify(S.mbCh || {}); },
  jtCh(){ return JSON.stringify(S.jtCh || {}); },
  rowFit(re){ const rx = new RegExp(re); const r = [...document.querySelectorAll('#slot .mbur')].find(x => rx.test(txt(x.querySelector('.nm')))); if (!r) return null;
    const nm = r.querySelector('.nm'), cs = getComputedStyle(nm), rr = r.getBoundingClientRect(), nr = nm.getBoundingClientRect();
    const clip = (cs.textOverflow === 'ellipsis' && cs.overflow !== 'visible' && nm.scrollWidth > nm.clientWidth + 1 && nm.clientWidth > 0);
    return { nm: txt(nm), sw: nm.scrollWidth, cw: nm.clientWidth, h: +nr.height.toFixed(1), nmR: +nr.right.toFixed(1), rowR: +rr.right.toFixed(1), ws: cs.whiteSpace, to: cs.textOverflow, clip: clip,
             docSW: document.documentElement.scrollWidth, docCW: document.documentElement.clientWidth }; },
  /* ── §E 동기화 창(새 키 둘) ── */
  async sync(){ try{ await syncRecords(true); }catch(e){ return 'err ' + e; } await idle(); await wait(300); return (window.__REMOTE || {}).puts || 0; },
  remote(){ return (window.__REMOTE || {}).text || null; },
  setRemote(t){ window.__REMOTE = window.__REMOTE || {}; window.__REMOTE.text = t; window.__REMOTE.sha = 'H_set_' + Date.now(); return true; },
  seedNewKeys(){ if (!has('grndPush')) return false; grndPush('2015', { date: '2026-09-25', ts: '2026-09-25T01:00:00Z', ok: 12, n: 20, ms: 1800000, picks: { '1': '3' } });
    const G = rgnAll(); G['T1350065|mok|특허|__mg2~u|2026-9-25'] = Date.now(); RGNREC = G; lsWrite(RGN_KEY, G, '풀이 기록 묘비'); try{ stampAll(); }catch(e){} return true; },
  localNewKeys(){ let g = null, r = null; try{ g = JSON.parse(localStorage.getItem(REC_PRE + 'giround') || 'null'); r = JSON.parse(localStorage.getItem(REC_PRE + 'recgone') || 'null'); }catch(e){}
    return { giround: g ? Object.keys(g).length : 0, recgone: r ? Object.keys(r).length : 0 }; },
  dump(){ const m = document.querySelector('#slot .main') || document.querySelector('#slot'); return m ? String(m.innerText || '').split('\n').map(s => s.replace(/\s+/g, ' ').trim()).filter(Boolean).join('\n') : ''; },   /* 줄 단위(블록마다) — 회귀 대조를 줄로 한다 */
  drawerDump(){ const b = document.getElementById('jtlist'); return b ? txt(b) : ''; },
};
})();
