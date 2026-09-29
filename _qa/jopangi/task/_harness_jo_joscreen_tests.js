/* _harness_jo_joscreen_tests.js — _task_jo_joscreen(+add1) 하네스가 페이지에 넣는 도구(__JS).
   BASE(genie 59b8701 = mbsame 인도 판)·NEW 둘 다에 같은 것을 넣는다 — 없는 함수(jsPanelItems · joOtherLaw · jnMenu …)는 빈 값(헛잣대).
   보임 = computed display ≠ none 그리고 높이 > 0 · 자리 = getBoundingClientRect + elementFromPoint.
   ⚠ 누름은 여기서 안 한다 — 자리만 돌려주고 파이썬이 page.mouse · CDP 터치 · CDP 펜으로 누른다.
   ⚠ 패널 차례·연도는 앱 함수(jsYear 등)를 쓰지 않고 여기서 따로 센다(바탕에서도 같은 잣대). */
(function(){
const wait = ms => new Promise(r => setTimeout(r, ms));
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const has = n => { try{ return typeof eval(n) !== 'undefined'; }catch(e){ return false; } };
const vis = e => !!e && e.isConnected && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden' && e.getBoundingClientRect().height > 0;
const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); return { x: +r.left.toFixed(2), y: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2), r: +r.right.toFixed(2), b: +r.bottom.toFixed(2), cx: +(r.left + r.width / 2).toFixed(2), cy: +(r.top + r.height / 2).toFixed(2) }; };
function hitOn(t){ if (!t) return null; try{ t.scrollIntoView({ block: 'center', inline: 'nearest' }); }catch(e){}
  const r = R(t), at = document.elementFromPoint(r.cx, r.cy);
  const onScreen = r.cy > 0 && r.cy < innerHeight && r.cx > 0 && r.cx < innerWidth && r.w > 0 && r.h > 0;
  return Object.assign(r, { on: !!at && (at === t || t.contains(at)) && onScreen, onScreen, vis: vis(t), tag: at ? at.tagName + '.' + at.className : null }); }
async function idle(){ for (let i = 0; i < 400 && (typeof busy !== 'undefined' && busy); i++) await wait(25); }
async function until(f, ms){ const t0 = Date.now(); while (Date.now() - t0 < (ms || 8000)){ try{ const v = f(); if (v) return v; }catch(e){} await wait(40); } try{ return f(); }catch(e){ return null; } }
const pops = () => (typeof POPS !== 'undefined' ? POPS : []);
const cs = e => getComputedStyle(e);
/* ⚠ 앱 render() 는 이미 도는 중이면 새 호출을 버린다(if(busy)return) — 옛 칸에 표를 달고 부른 뒤,
   새로 그려졌고(표 없음) 바라는 상태(good)가 화면에 보일 때까지 다시 부른다 */
async function rnd(good, ms){
  const t0 = Date.now();
  while (Date.now() - t0 < (ms || 20000)){
    await idle();
    document.querySelectorAll('#slot > *').forEach(e => { e.dataset.jsold = '1'; });
    await render(); await idle();
    const ok = await until(() => { const ch = [...document.querySelectorAll('#slot > *')]; return ch.length > 0 && !ch.some(e => e.dataset.jsold) && (!good || good()); }, 3000);
    if (ok) return true;
  }
  return false;
}
/* ★ jo_wonmun(9/27) — 정오문제 = 오른쪽 패널(.jopane) → 떠 있는 창(.pop.wm-jp · 머리 글자 줄 .jpbar 의 .jpgap 뒤 = 쪽 번호) · 두 꼴 다 읽는다 */
const PANE = () => document.querySelector('#slot .jopane') || document.querySelector('.pop.wm-jp');
const pageBtns = () => { const w = document.querySelector('.pop.wm-jp');
  if (w){ const g = w.querySelector('.jpbar .jpgap'); const o = []; if (g) for (let n = g.nextElementSibling; n; n = n.nextElementSibling) o.push(n); return o; }
  const r = [...document.querySelectorAll('#slot .jopane .ctrlbar')].find(x => txt(x.querySelector('.pl')) === '쪽'); return r ? [...r.querySelectorAll('button')] : []; };
const pageRowEl = () => { const bs = pageBtns(); return bs.length ? bs[0].parentNode : null; };
const curPage = () => { const bs = pageBtns(); if (!bs.length) return 0; return bs.findIndex(b => b.classList.contains('on')); };
const nPages = () => { const bs = pageBtns(); return bs.length || 1; };
/* 제7판 태그 연도(여기서 따로 · 여러 해면 가장 새 해) · 리담 = 연도 */
function yr7(tag){ let y = 0; (String(tag || '').match(/[0-9]{4}|[0-9]{2}/g) || []).forEach(s => { let v = +s; if (s.length === 2) v = v >= 80 ? 1900 + v : 2000 + v; if (v > y) y = v; }); return y; }
window.__JS = {
  wait,
  errs(){ return (window.__ERR || []).filter(e => !/^ResizeObserver loop/.test(e)).slice(0, 20); },
  ok(){ return { panelItems: has('jsPanelItems'), other: has('joOtherLaw'), jn: has('jnMenu'), lp: has('jsLongPress') }; },
  async jo(law, k, opt){
    opt = opt || {};
    try{ closeAllPops(); }catch(e){}
    let nLaw = null; try{ nLaw = ((await get('jo_' + law + '_목록.json')).조 || []).length; }catch(e){}
    S.tab = 'jo'; S.law = law; S.jo = k;
    if (opt.panel !== undefined) S.joPanel = !!opt.panel;
    if (opt.f) S.joPanelF = opt.f;
    if (opt.p !== undefined) S.joPanelP = opt.p;
    if (opt.treeW) S.treeW = opt.treeW;
    const good = () => { const t = document.querySelector('#slot .jotitle .no'); const b = document.querySelector('#slot .tree .jtbar button');
      return !!t && txt(t) === k && (nLaw == null || (b && txt(b) === '전체 ' + nLaw)) && (!S.joPanel || !!PANE()); };
    const ok = await rnd(good, 30000);
    await wait(200);
    return { law: S.law, jo: S.jo, title: txt(document.querySelector('#slot .jotitle')), fresh: ok };
  },
  /* ── 1 머리 ── */
  head(){
    const main = document.querySelector('#slot .main'); if (!main) return null;
    const title = main.querySelector('.jotitle');
    const pre = []; for (let n = main.firstElementChild; n && n !== title; n = n.nextElementSibling) pre.push(n.className + ':' + txt(n));
    const conn = main.querySelector('.conn');
    const items = conn ? [...conn.children].map(e => { const c = cs(e); return { t: txt(e), cls: e.className, tag: e.tagName, bg: c.backgroundColor, bw: c.borderTopWidth, br: c.borderTopLeftRadius, fs: c.fontSize, fw: c.fontWeight, color: c.color, op: c.opacity, pad: c.paddingLeft + ' ' + c.paddingRight }; }) : [];
    const all = txt(main);
    return { pre: pre, sihaeng: txt(main.querySelector('.sihaeng')), lawChip: [...main.querySelectorAll('.chip')].filter(e => txt(e) === S.law).length,
      connK: conn ? [...conn.querySelectorAll('.k')].map(txt) : [], items: items,
      c3chip: /⇄ 3법 대응/.test(all), themeChip: /🧩 테마 \d+ ↓/.test(all), cardChip: /🃏 카드 — 준비 중/.test(all), clock: /🕐/.test(all),
      file: (() => { try{ return all.indexOf('특-' + S.jo) >= 0 || /[특상디]-제\d+조/.test(txt(main.querySelector('.sihaeng'))); }catch(e){ return null; } })(),
      conn: conn ? { gap: cs(conn).columnGap } : null };
  },
  bodyText(){ const b = document.querySelector('#slot .main .box'); return b ? txt(b).slice(0, 200) : ''; },
  hasEditLine(){ return /내 편집본/.test(txt(document.querySelector('#slot .main'))); },
  /* ── 2·8·11·12·13 패널 ── */
  chipN(){ const b = [...document.querySelectorAll('#slot .main .conn button')].find(x => /정오문제/.test(txt(x))); const m = b && /정오문제\s*(\d+)/.exec(txt(b)); return m ? +m[1] : null; },
  chipAt(){ const b = [...document.querySelectorAll('#slot .main .conn button')].find(x => /정오문제/.test(txt(x))); return b ? hitOn(b) : null; },
  panelAll(){ const b = [...document.querySelectorAll('#slot .jopane .ctrlbar button, .pop.wm-jp .jpbar .jpt')].find(x => /^전체 \d+/.test(txt(x))); return b ? +/\d+/.exec(txt(b))[0] : null; },
  panelBtn(re){ const rx = new RegExp(re); const b = [...document.querySelectorAll('#slot .jopane button, .pop.wm-jp button')].find(x => rx.test(txt(x))); return b ? hitOn(b) : null; },
  pageRow(){ const bs = pageBtns(); if (!bs.length) return null; const r = document.querySelector('.pop.wm-jp') ? bs[0] : pageRowEl(); return { vis: vis(r), t: bs.map(txt).join(' '), h: R(r).h }; },
  panelCards(){ return [...document.querySelectorAll('#slot .jopane > [id^="jp-"], .pop.wm-jp .jpcards > [id^="jp-"]')].map(c => c.id.slice(3)); },
  /* 패널 차례 — 지금 조 색인(JOPANE)에서 sid → 연도·문번·선지를 여기서 센다(앱 함수 안 씀) */
  panelMeta(){
    const ent = (typeof JOPANE !== 'undefined' && JOPANE || {})[S.jo] || { L: [], P: [] }, m = {};
    (ent.L || []).forEach(x => { const sid = oxKeyLid(x.q, x.z); m[sid] = { kind: 'L', y: +x.q.연도 || 0, no: +(x.q.시험문번 || x.q.문번) || 0, ch: +x.z.n || 0, id: x.q.id, n: x.z.n }; });
    (ent.P || []).forEach(z => { const sid = oxKeyP7(z); if (!m[sid]) m[sid] = { kind: 'P', y: yr7(z.태그), no: 0, ch: 0, id: z.id, tag: z.태그 }; });
    return this.panelCards().map(s => Object.assign({ sid: s }, m[s] || {}));
  },
  async panelAllIds(){   /* 모든 쪽을 넘기며 카드 열쇠를 모은다(쪽마다 그 쪽 단추가 켜진 것을 보고 읽는다) */
    const out = []; const N = nPages();
    for (let p = 0; p < N; p++){
      S.joPanelP = p;
      await rnd(() => !!PANE() && (N === 1 ? true : curPage() === p), 20000);
      this.panelMeta().forEach(x => out.push(x));
    }
    S.joPanelP = 0; await rnd(() => !!PANE(), 20000);
    return out;
  },
  /* 전 조 칩 = 패널 — 렌더해서 잰다(느림 · 크로미움만) */
  async chipVsPanelAll(law){
    const L = await get('jo_' + law + '_목록.json'); const out = { n: 0, diff: [], stale: 0 };
    for (const x of (L.조 || [])){
      S.tab = 'jo'; S.law = law; S.jo = x.k; S.joPanel = true; S.joPanelF = 'all'; S.joPanelP = 0;
      const ok = await rnd(() => { const t = document.querySelector('#slot .jotitle .no'); return !!t && txt(t) === x.k && !!PANE(); }, 20000);
      if (!ok) out.stale++;
      const a = this.chipN(), b = this.panelAll(); out.n++;
      if (a !== b) out.diff.push([x.k, a, b]);
    }
    return out;
  },
  /* 9 카드 꼴 */
  cardShape(sid){ const c = document.getElementById('jp-' + sid); if (!c) return null;
    const hd = c.querySelector('.mbqhd, .qhd');
    const heads = hd ? [...hd.querySelectorAll(':scope > *, :scope > .l > *')].map(e => e.tagName.toLowerCase() + '.' + String(e.className).trim().replace(/\s+/g, '.')) : [];
    return { cls: c.className, hd: hd ? hd.className : null, heads: heads, text: txt(c).slice(0, 160), qbn: c.querySelectorAll('.qb.n').length,
      yearChips: [...c.querySelectorAll('.jxec')].map(txt), lab: txt(c.querySelector('.mbqlab')) }; },
  unitShape(key){ const c = document.getElementById('qb-' + key); if (!c) return null;
    const hd = c.querySelector('.mbqhd, .qhd');
    const heads = hd ? [...hd.querySelectorAll(':scope > *, :scope > .l > *')].map(e => e.tagName.toLowerCase() + '.' + String(e.className).trim().replace(/\s+/g, '.')) : [];
    return { cls: c.className, hd: hd ? hd.className : null, heads: heads }; },
  /* ── 4·5 3법 ── */
  c3(){ const w = document.querySelector('#slot .thwrap.c3') || [...document.querySelectorAll('#slot .thwrap')].find(x => /3법/.test(txt(x.querySelector('.thhd'))));
    if (!w) return null; const hd = w.querySelector(':scope > .thhd');
    const cols = [...w.querySelectorAll('.thcols > .thcol')].map(c => { const h = c.querySelector('.thhd'); return { law: txt(h && h.querySelector('.qb.t')), k: txt(h && h.querySelector('b')), head: txt(h), cls: c.className,
      badges: h ? [...h.querySelectorAll('.badge')].map(txt) : [], dashed: cs(c).borderTopStyle, body: txt(c.querySelector('.bj2')).slice(0, 120), pick: !!c.querySelector('.c3pick'), r: R(c) }; });
    const add = w.querySelector('.thcol.add');
    const row = w.querySelector('.thcols');
    const btns = [...w.querySelectorAll('button')].map(txt);
    return { head: hd ? txt(hd) : '', headB: hd ? txt(hd.querySelector('b')) : '', cdim: hd ? [...hd.querySelectorAll('.cdim')].map(txt) : [], cols: cols, btns: btns,
      cand: w.querySelectorAll('.thcol.cand').length, candBtn: btns.filter(t => /^후보 |✓ 이 조|✕ 대응 없음/.test(t)).length,
      add: add ? Object.assign(hitOn(add), { inRow: (() => { const a = R(add), rr = R(row); return a.x >= rr.x - 1 && a.r <= rr.r + 1; })() }) : null,
      rowWrap: row ? cs(row).flexWrap : null, rowOx: row ? cs(row).overflowX : null, vw: innerWidth };
  },
  c3fold(){ const w = [...document.querySelectorAll('#slot .thwrap')].find(x => /3법/.test(txt(x.querySelector('.thhd')))); if (!w) return null; const b = [...w.querySelectorAll('.thhd button')].find(x => /펴기|접기/.test(txt(x))); return b ? Object.assign(hitOn(b), { t: txt(b) }) : null; },
  c3headAt(law){ const w = [...document.querySelectorAll('#slot .thwrap')].find(x => /3법/.test(txt(x.querySelector('.thhd')))); if (!w) return null;
    const c = [...w.querySelectorAll('.thcols > .thcol')].find(x => txt(x.querySelector('.thhd .qb.t')) === law); if (!c) return null;
    const h = c.querySelector('.thhd'); const r = hitOn(h); const b = h.querySelector('b');
    /* 머리 빈 곳(조 글자 b 밖) — 누름 자리 · 길게 누르기는 머리 어디든 */
    const lab = h.querySelector('.qb.t'); const rl = R(lab);
    return Object.assign(r, { bx: R(b), lab: rl, px: rl.cx, py: rl.cy }); },
  c3pick(){ const p = document.querySelector('#slot .c3pick'); if (!p) return null;
    return { vis: vis(p), law: p.dataset.dst, inp: (p.querySelector('input') || {}).value, opts: [...p.querySelectorAll('select option')].map(o => o.value || '조 전체'), sel: (p.querySelector('select') || {}).value, r: R(p),
      under: (() => { const c = p.closest('.thcol'); const h = c && c.querySelector('.thhd'); if (!!h && h.nextElementSibling === p) return true;
        const pv = p.previousElementSibling; return !!pv && pv.classList.contains('thcol'); })() }; },   /* ★ revfix0928 A-6 — 칸이 카드(.thcol) 바로 뒤 제 줄로 옮겨졌다 · 옛 자리(머리 바로 뒤)·새 자리 둘 다 「카드 바로 아래」 */
  c3pickInput(v){ const p = document.querySelector('#slot .c3pick input'); if (!p) return null; const r = hitOn(p); return r; },
  c3pickBtn(re){ const rx = new RegExp(re); const b = [...document.querySelectorAll('#slot .c3pick button')].find(x => rx.test(txt(x))); return b ? hitOn(b) : null; },
  c3pickSelAt(){ const s = document.querySelector('#slot .c3pick select'); return s ? hitOn(s) : null; },
  c3hangRows(law, k, h){ return get('jo_' + law + '_본문.json').then(B => { const j = (B.조 || {})[k] || {}; return (j.행 || []).filter(r => (r.k || [])[0] === '항' && r.k[1] === h).map(r => r.t); }); },
  themefix(){ try{ return JSON.parse(localStorage.getItem('jopangi.themefix') || '{}'); }catch(e){ return null; } },
  /* ── 6 조문 팝업 ── */
  async popjo(law, k){ try{ closeAllPops(); }catch(e){} await popJo(law, k, { clientX: 300, clientY: 200 }, 1); await until(() => pops().some(p => p._pk === 'jo|' + law + '|' + k && !/불러오는 중/.test(txt(p.querySelector('.pt')))), 8000); await wait(150);
    const p = pops().find(x => x._pk === 'jo|' + law + '|' + k); if (!p) return null;
    const b = [...p.querySelectorAll('button')].find(x => /뷰로 이동/.test(txt(x)));
    if (!b) return { found: false };
    const c = cs(b), ph = p.querySelector('.ph');
    return Object.assign(hitOn(b), { found: true, inHead: !!ph && ph.contains(b), inBody: !!p.querySelector('.pb') && p.querySelector('.pb').contains(b), bg: c.backgroundColor, fs: c.fontSize, fw: c.fontWeight, bw: c.borderTopWidth, color: c.color,
      afterTitle: (() => { const pt = ph && ph.querySelector('.pt'); return !!pt && (pt.nextElementSibling === b.parentNode || pt.nextElementSibling === b); })(), headH: ph ? R(ph).h : null }); },
  popKeys(){ return pops().map(p => p._pk); },
  state(){ return { tab: S.tab, law: S.law, jo: S.jo, pops: pops().length }; },
  /* ── 7 서랍 ── */
  drawer(){
    const rows = [...document.querySelectorAll('#slot .tree .r')].filter(r => !r.classList.contains('jhead') && !r.classList.contains('jsub') && r.querySelector('.nm') && /^제\d/.test(txt(r.querySelector('.nm'))));
    const L = new Set(), E = new Set(), K = new Set(); let bars = 0, nm2 = 0, h1 = new Set();
    rows.forEach(r => { const bm = r.querySelector('.bkm3'); if (bm) L.add(Math.round(R(bm).x));
      const ed = [...r.querySelectorAll('em span')].find(s => /^✏/.test(txt(s))); if (ed) E.add(Math.round(R(ed).x));
      const lk = [...r.querySelectorAll('em span')].find(s => /^🔗/.test(txt(s))); if (lk) K.add(Math.round(R(lk).x));
      bars += r.querySelectorAll('.bars').length; h1.add(Math.round(R(r.querySelector('.nm')).h)); });
    const lg = document.querySelector('#slot .tree .legend');
    const eds = rows.map(r => [...r.querySelectorAll('em span')].map(txt).find(t => /^✏/.test(t))).filter(Boolean);
    return { rows: rows.length, bkLeft: [...L].sort((a, b) => a - b), edLeft: [...E].sort((a, b) => a - b), lkLeft: [...K].sort((a, b) => a - b), bars: bars, legend: txt(lg), edSample: eds.slice(0, 3),
      edEmoji: eds.length ? eds.every(t => t.indexOf('✏️') === 0) : null, nmH: [...h1], treeW: S.treeW, starAfterName: (() => { const s = document.querySelector('#slot .tree .r:not(.jhead):not(.jsub) .jstarc'); return s ? { prev: s.previousElementSibling && (s.previousElementSibling.classList.contains('nm') ? 'nm' : s.previousElementSibling.className), inEm: !!s.closest('em') } : null; })() };   /* ★ revfix0928pm — 이름 칸 클래스가 「nm jnm2」 로 늘었다(자리 무변) · 클래스 목록에 nm 이 있으면 nm */
  },
  dotOf(k){ const rows = [...document.querySelectorAll('#slot .tree .r')].filter(r => txt(r.querySelector('.nm')).indexOf(k + ' ') === 0 || txt(r.querySelector('.nm')) === k);
    const r = rows[0]; if (!r) return null; return [...r.querySelectorAll('.bkm3 .bkmk')].map(i => { const c = cs(i); return { bg: c.backgroundColor, sh: c.boxShadow, t: txt(i) }; }); },
  fakeBlank(k, pk){ const A = (typeof blkAll === 'function') ? blkAll() : {}; A[S.law + ':' + k] = { n: 1, r: '2026-09-27', pct: 70, pk: pk };
    try{ localStorage.setItem('jopangi.blank', JSON.stringify(A)); }catch(e){} try{ if (typeof BLKREC !== 'undefined') BLKREC = null; }catch(e){} return A[S.law + ':' + k]; },
  bkColor(){ return typeof BK_COLOR !== 'undefined' ? BK_COLOR : null; },
  /* ── 14 이 조 아님 ── */
  typeJoAt(sid){ const c = document.getElementById('jp-' + sid); if (!c) return null; const s = c.querySelector('.mbtype .seg.jo') || c.querySelector('.mbtype'); return s ? Object.assign(hitOn(s), { t: txt(s) }) : null; },
  jnMenu(){ const p = pops().find(x => /조 연결/.test(x._pk || '')); if (!p) return null; return { rows: [...p.querySelectorAll('.jnmenu .r')].map(r => [txt(r.querySelector('b')), r.className, [...r.querySelectorAll('button')].map(txt)]) }; },
  jnBtn(k, re){ const p = pops().find(x => /조 연결/.test(x._pk || '')); if (!p) return null; const rx = new RegExp(re);
    const r = [...p.querySelectorAll('.jnmenu .r')].find(x => txt(x.querySelector('b')) === k); const b = r && [...r.querySelectorAll('button')].find(x => rx.test(txt(x))); return b ? hitOn(b) : null; },
  jonot(){ try{ return JSON.parse(localStorage.getItem('jopangi.jonot') || 'null'); }catch(e){ return 'bad'; } },
  syncHas(k){ return typeof SYNC_KEYS !== 'undefined' && SYNC_KEYS.indexOf('jopangi.' + k) >= 0; },
  /* ── 8-R 규칙 대조(앱 쪽) ── */
  ruleJS(pairs){ if (typeof joOtherLaw !== 'function') return null; return pairs.map(p => joOtherLaw(p[0], p[1], p[2])); },
  p7JoAll(){ return get('jimun_7pan.json').then(async P7 => {
    if (!JOKEY){ const JL = await get('jo_특허법_목록.json'); JOKEY = {}; JL.조.forEach(x => { JOKEY[x.k] = x.t || ''; }); }
    const o = {}; (P7.지문 || []).forEach(z => { o[z.id] = p7Jo(z.sol, []).map(x => x.k); }); return o; }); },
  /* ── 도움 ── */
  atText(scope, re){ const rx = new RegExp(re); const b = [...document.querySelectorAll(scope)].find(x => rx.test(txt(x))); return b ? Object.assign(hitOn(b), { t: txt(b) }) : null; },
  c3body(law){ const w = [...document.querySelectorAll('#slot .thwrap')].find(x => /3법/.test(txt(x.querySelector('.thhd')))); if (!w) return null;
    const c = [...w.querySelectorAll('.thcols > .thcol')].find(x => txt(x.querySelector('.thhd .qb.t')) === law); return c ? txt(c.querySelector('.bj2')) : null; },
  uiTh(){ try{ return localStorage.getItem('jopangi_ui_th'); }catch(e){ return null; } },
  async pageOf(sid){ const N = nPages();
    for (let p = 0; p < N; p++){ S.joPanelP = p; await rnd(() => !!PANE() && (N === 1 ? true : curPage() === p), 20000);
      if (document.getElementById('jp-' + sid)) return p; }
    return -1; },
  /* 2003 리담 지문이 걸린 조(특허) — 지금 색인에서 */
  async find2003(){ const JP = await joPanelIdx(); const ks = Object.keys(JP || {}).sort((a, b) => (+(/\d+/.exec(a) || [0])[0]) - (+(/\d+/.exec(b) || [0])[0]));
    const have = new Set(((await get('jo_특허법_목록.json')).조 || []).map(x => x.k));   /* 삭제 조(제26조 등)는 조문 화면이 없다 */
    for (const k of ks){
      if (!have.has(k)) continue; const x = ((JP[k] || {}).L || []).find(y => String(y.q.연도) === '2003' && !y.q.시험문번); if (x) return { k: k, sid: oxKeyLid(x.q, x.z), qid: x.q.id, n: x.z.n }; } return null; },
  /* 두 조에 걸린 리담 지문(「이 조 아님」 → 다른 조 패널에서 되살리기) */
  async pickMulti(){ const JP = await joPanelIdx(); const where = {};
    Object.keys(JP || {}).forEach(k => ((JP[k] || {}).L || []).forEach(x => { const s = oxKeyLid(x.q, x.z); (where[s] = where[s] || new Set()).add(k); }));
    const s = Object.keys(where).sort().find(s2 => where[s2].size >= 2 && /^T/.test(s2));
    if (!s) return null; const ks = [...where[s]].sort(); return { sid: s, a: ks[0], b: ks[1] }; },
  /* 같은 지문을 1차객 단원 빌더(mlnLidCard)로 지은 카드의 머리 꼴(패널 카드와 맞댄다) */
  unitShapeOf(sid){ const ent = (typeof JOPANE !== 'undefined' && JOPANE || {})[S.jo] || { L: [] };
    const x = (ent.L || []).find(y => oxKeyLid(y.q, y.z) === sid); if (!x || typeof mlnLidCard !== 'function') return null;
    const c = mlnLidCard(x.q, x.z, 1, (typeof MLN !== 'undefined' && MLN.ok) ? mlnClass(x.q, x.z) : '', null);
    const hd = c.querySelector('.mbqhd, .qhd');
    return { cls: c.className, heads: hd ? [...hd.querySelectorAll(':scope > *, :scope > .l > *')].map(e => e.tagName.toLowerCase() + '.' + String(e.className).trim().replace(/\s+/g, '.')) : [] }; },
  async gaekHome(law){ try{ closeAllPops(); }catch(e){}
    S.law = law; S.tab = 'jimun'; S.jimunTab = 'ox'; S.mok = ''; S.oxQueue = ''; S.year = '';
    await rnd(() => (law !== '특허법' || (typeof OXPOOL !== 'undefined' && OXPOOL && Object.keys(OXPOOL).length > 300)) && !!document.querySelector('#slot .main, #slot .mbdash'), 40000);
    await wait(300); return Object.keys((typeof OXPOOL !== 'undefined' && OXPOOL) || {}).length; },
  async gaekGo(sel){ try{ closeAllPops(); }catch(e){} S.jimunTab = 'ox'; S.oxQueue = ''; S.mok = sel; S.oxPage = null; await rnd(null, 20000); await wait(300); return S.mok; },
  /* ── 10 회귀 ── */
  dump(){ const m = document.querySelector('#slot'); return m ? (m.innerText || '').split('\n').map(s => s.trim()).filter(Boolean).join('\n') : ''; },
  async tab(t, extra){ try{ closeAllPops(); }catch(e){} S.tab = t; Object.assign(S, extra || {}); await rnd(null, 20000); await wait(900); return S.tab; },
  poolKeys(){ return Object.keys((typeof OXPOOL !== 'undefined' && OXPOOL) || {}); }
};
})();
