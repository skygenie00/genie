/* _harness_jo_ms_canvas_relayout_tests.js — _task_jo_ms_canvas_relayout 하네스가 페이지에 넣는 도구(__HR).
   BASE(4be73ca · 옛 데이터)·NEW(새 앱 · 새 데이터) 둘 다에 같은 것을 넣는다 — 없는 것(◇ 도형 · MIG …)은 빈 값으로 돌려준다.
   재는 것 = 데이터(viewCanvas._cv().D) · DOM 실물 · 저장소 값(localStorage) · 화면 자리(getBoundingClientRect · elementFromPoint). */
(function(){
const wait = ms => new Promise(r => setTimeout(r, ms));
const SC = 4;
const cv = () => viewCanvas._cv();
const txt = l => (l.r || []).map(r => r.t).join('');
const stageR = () => { const s = document.getElementById('cvStage'); return s ? s.getBoundingClientRect() : null; };
const LS = k => { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; } };
const KEYS = ['jopangi.canvas', 'jopangi.canvasink', 'jopangi.canvasmemo', 'jopangi.canvaspin', 'jopangi.canvaslink', 'jopangi.canvasjari'];
function box(k, o){ if (k === 'bars') return [o.x - 0.5, o.y, o.x + 0.75, o.y + o.h];
  if (k !== 'shapes' || o.k === 'r') return [o.x, o.y, o.x + o.w, o.y + o.h];
  if (o.k === 'l') return [Math.min(o.x, o.x2), Math.min(o.y, o.y2), Math.max(o.x, o.x2), Math.max(o.y, o.y2)];
  const xs = o.p.map(q => q[0]), ys = o.p.map(q => q[1]); return [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)]; }
function geoOf(k, o){ if (k === 'shapes'){ if (o.k === 'l') return [o.x, o.y, o.x2, o.y2]; if (o.k === 'c') return o.p.map(q => [q[0], q[1]]); return [o.x, o.y, o.w, o.h]; }
  if (k === 'bars') return [o.x, o.y, o.h]; return [o.x, o.y, o.w, o.h]; }
window.__HR = {
  wait, KEYS,
  async boot(){ try { closeAllPops(); } catch (e) {} S.law = '민사소송법'; S.tab = 'omr'; await render();
    for (let i = 0; i < 800; i++){ if (document.getElementById('cvStage') && document.querySelectorAll('#cvWorld .cv-pg').length) break; await wait(50); }
    await wait(600); const c = cv();
    return { stage: !!document.getElementById('cvStage'), pg: document.querySelectorAll('#cvWorld .cv-pg').length, hash: c.META && c.META.hash, np: c.D && c.D.pages.length,
      shapeBtn: !!document.querySelector('#cvInkbar .t[data-t="shape"]'), hasMig: 'MIG' in c, err: (window.__ERR || []).slice(0, 5) }; },
  info(){ const c = cv(); return { hash: c.META.hash, logHash: c.LOG.hash, ops: c.LOG.ops.length, replay: Object.assign({}, c.REPLAY), mig: c.MIG || null, vz: c.vz, vx: c.vx, vy: c.vy,
    ink: S.ink, tool: c.INK.tool, sh: c.SH || null, stale: (document.getElementById('cvStale') || {}).textContent || '', badge: (document.getElementById('cvEditN') || {}).textContent || '' }; },
  ops(k){ const L = cv().LOG.ops; return (k ? L.slice(-k) : L).map(o => Object.assign({}, o)); },
  lines(n){ const p = cv().D.pages[n - 1]; return p.lines.map(l => [l.id, +l.y.toFixed(2), +l.x.toFixed(2), +l.x1.toFixed(2), l.h, l.del ? 1 : 0, txt(l)]); },
  blocks(n){ const p = cv().D.pages[n - 1]; return p.blocks.map((b, i) => ({ i, bid: b.bid, k: b.k, d: b.d, p: b.p, del: !!b.del, ls: b.ls.slice(), x: b.x, y: b.y, w: b.w, h: b.h, to: b.to || null })); },
  geo(n){ const p = cv().D.pages[n - 1]; const out = {};
    ['shapes', 'imgs', 'bars', 'hls'].forEach(k => { out[k] = (p[k] || []).map((o, i) => ({ i, sid: o.sid || null, k: o.k || k, g: geoOf(k, o), del: !!o.del, b: box(k, o).map(v => +v.toFixed(2)) })); });
    out.ph = p.ph; out.oy = p.oy; return out; },
  ls(){ const o = {}; KEYS.forEach(k => { o[k] = localStorage.getItem(k); }); return o; },
  lsGet: k => LS(k),
  lsSet(k, v){ localStorage.setItem(k, typeof v === 'string' ? v : JSON.stringify(v)); return true; },
  gone(){ return LS('jopangi_sync_gone') || {}; },
  /* 화면 ↔ 쪽 좌표(쪽 절대 y) */
  scr(x, y){ const c = cv(), r = stageR(); return { x: r.left + c.vx + x * SC * c.vz, y: r.top + c.vy + y * SC * c.vz }; },
  at(sx, sy){ const e = document.elementFromPoint(sx, sy); return e ? { tag: e.tagName, cls: String(e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className || ''), sid: e.dataset ? (e.dataset.sid || null) : null,
    ink: !!(e.closest && e.closest('.cv-inksvg')), pgN: (() => { const pg = e.closest && e.closest('.cv-pg'); return pg ? (pg.querySelector('.cv-pn') || {}).textContent : null; })() } : null; },
  /* 쪽 점 (x, y)을 무대 가운데로(배율 z) */
  async center(x, y, z){ const c = cv(), r = stageR(); c.set({ vz: z, vx: r.width / 2 - x * SC * z, vy: r.height / 2 - y * SC * z }); await wait(350); return __HR.scr(x, y); },
  lineOf(id){ const c = cv(); const n = parseInt(id, 10); const p = c.D.pages[n - 1]; const l = p && p.lines.find(q => q.id === id); return l ? { n, x: l.x, x1: l.x1, y: l.y, h: l.h, del: !!l.del, t: txt(l), oy: p.oy } : null; },
  /* 줄 한가운데 화면 자리 — 그 줄 div 가 맨 위인지도 */
  lineAt(id){ const l = __HR.lineOf(id); if (!l) return null; const s = __HR.scr((l.x + Math.min(l.x1, l.x + 30)) / 2, l.y + l.h / 2); return Object.assign(s, { hit: __HR.at(s.x, s.y) }); },
  /* ◇ 도형 — 쪽 n 의 kind(r·l·c 는 shapes 의 k · img·bar·hl) 후보 중 제 자리를 누르면 저를 고르는 것들(앱 shpPick 으로 확인) */
  cands(n, kind, lim){ const c = cv(); const p = c.D.pages[n - 1]; if (!c.shpPick) return [];
    const K = kind === 'img' ? 'imgs' : kind === 'bar' ? 'bars' : kind === 'hl' ? 'hls' : 'shapes'; const out = [];
    (p[K] || []).forEach((o, i) => { if (o.del || !o.sid || (K === 'shapes' && o.k !== kind)) return; const b = box(K, o);
      const pts = []; if (K === 'shapes' && o.k === 'l') pts.push([(o.x + o.x2) / 2, (o.y + o.y2) / 2]);
      else if (K === 'shapes' && o.k === 'c'){ const m = Math.floor(o.p.length / 2); pts.push(o.p[m], o.p[Math.max(0, m - 1)], o.p[0]); }
      else if (K === 'shapes') pts.push([o.x, o.y + o.h / 2], [o.x + o.w / 2, o.y]);
      else if (K === 'bars') pts.push([o.x + 0.1, o.y + o.h / 2]);
      else pts.push([(b[0] + b[2]) / 2, (b[1] + b[3]) / 2]);
      for (const q of pts){ const f = c.shpPick(p, q[0], q[1]); if (f && f.o === o){ out.push({ i, sid: o.sid, x: +q[0], y: +q[1], b }); break; } } });
    return lim ? out.slice(0, lim) : out; },
  pick(n, x, y){ const c = cv(); const f = c.shpPick ? c.shpPick(c.D.pages[n - 1], x, y) : null; return f ? f.o.sid : null; },
  shsel(){ const e = document.querySelector('.cv-shsel'), d = document.querySelector('.cv-shdel'); const r = x => { if (!x) return null; const q = x.getBoundingClientRect(); return { x: q.left, y: q.top, w: q.width, h: q.height, cx: q.left + q.width / 2, cy: q.top + q.height / 2 }; };
    return { sh: cv().SH || null, sel: r(e), del: r(d), delHit: d ? (() => { const q = d.getBoundingClientRect(); const t = document.elementFromPoint(q.left + q.width / 2, q.top + q.height / 2); return !!t && (t === d || d.contains(t)); })() : false }; },
  domOf(n, sid){ const pg = cv().built.get(n); if (!pg) return { pg: false }; const es = [...pg.querySelectorAll('[data-sid="' + sid + '"]')];
    return { pg: true, n: es.length, tags: es.map(e => e.tagName), svgXY: es.filter(e => e instanceof SVGElement).map(e => [e.getAttribute('x') || e.getAttribute('x1'), e.getAttribute('y') || e.getAttribute('y1'), (e.getAttribute('d') || '').slice(0, 24)]),
      css: es.filter(e => !(e instanceof SVGElement)).map(e => [e.style.left, e.style.top]) }; },
  tool(t){ const b = document.querySelector('#cvInkbar .t[data-t="' + t + '"]'); if (!b) return null; const r = b.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2, on: b.classList.contains('on') }; },
  inkBtn(){ const b = document.getElementById('inkToggle'); if (!b) return null; const r = b.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2, t: b.textContent }; },
  /* 편집 — 줄 편집 칸 · 칩 */
  ed(){ const e = document.querySelector('.cv-edln'); return e ? { t: e.textContent, id: (() => { const c = cv(); for (const p of c.D.pages){ const pg = c.built.get(p.n); if (pg && pg.contains(e)) return p.n; } return null; })() } : null; },
  chipOp(op){ const c = document.querySelector('#cvChips .cv-ops .cv-chip[data-op="' + op + '"]'); if (!c) return null; const r = c.getBoundingClientRect(); const t = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    return { x: r.left + r.width / 2, y: r.top + r.height / 2, on: !!t && (t === c || c.contains(t)) }; },
  selBlk(){ const e = document.querySelector('#cvWorld .cv-blk.on'); if (!e) return null; const c = cv(); const p = c.D.pages[+e.dataset.p - 1]; const b = p.blocks[+e.dataset.b]; return { n: p.n, i: +e.dataset.b, bid: b.bid }; },
  /* 블록이 맨 위인 점(겹친 블록) — 둘레 ±2px 까지 */
  blkPt(bid){ const c = cv(); const n = parseInt(bid, 10); const p = c.D.pages[n - 1]; const i = p.blocks.findIndex(b => b.bid === bid && !b.del); if (i < 0) return null;
    const e = document.querySelector('#cvWorld .cv-blk[data-p="' + n + '"][data-b="' + i + '"]'); if (!e) return null; const r = e.getBoundingClientRect();
    const mine = (x, y) => { const t = document.elementFromPoint(x, y); return !!t && t.closest('.cv-blk') === e; };
    for (let a = 1; a < 10; a++) for (let b = 1; b < 10; b++){ const x = Math.round(r.left + r.width * a / 10), y = Math.round(r.top + r.height * b / 10);
      if (mine(x, y) && mine(x - 2, y) && mine(x + 2, y) && mine(x, y - 2) && mine(x, y + 2)) return { x, y, on: true }; }
    return { x: r.left + r.width / 2, y: r.top + r.height / 2, on: false }; },
  /* 눈 확인 — 이름표·옅게 하기를 끄고(배치만 본다) · 쪽 n 을 배율 z 로 왼쪽 위에 */
  eyeCss(){ if (document.getElementById('hrEye')) return; const s = document.createElement('style'); s.id = 'hrEye';
    s.textContent = '#cvLabels{display:none!important}#cvWorld.far .cv-ln,#cvWorld.xfar .cv-ln{opacity:1!important}#cvChips,#cvHits,.cv-shsel,.cv-shdel{display:none!important}'; document.head.appendChild(s); },
  async fitPage(n, z){ const c = cv(); const p = c.D.pages[n - 1]; const r = stageR(); c.set({ vz: z, vx: 30, vy: 20 - p.oy * SC * z }); await wait(500);
    const pg = c.built.get(n); if (!pg) return null; const q = pg.getBoundingClientRect(); return { x: q.left, y: q.top, w: q.width, h: q.height, stage: { x: r.left, y: r.top, w: r.width, h: r.height }, vz: cv().vz }; },
  /* 쪽 영역 [x0,x1]×[y0,y1](절대 y)을 배율 z 로 보이게 → 그 화면 사각형 */
  async region(x0, y0, x1, y1, z){ const c = cv(), r = stageR(); c.set({ vz: z, vx: r.width / 2 - (x0 + x1) / 2 * SC * z, vy: r.height / 2 - (y0 + y1) / 2 * SC * z }); await wait(450);
    const a = __HR.scr(x0, y0), b = __HR.scr(x1, y1); return { x: a.x, y: a.y, w: b.x - a.x, h: b.y - a.y, vz: cv().vz }; },
  errs(){ return (window.__ERR || []).slice(0, 10); }
};
})();
