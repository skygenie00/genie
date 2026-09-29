/* _harness_jo_c2card_tests.js — _task_jo_c2card(+add1) 하네스가 페이지에 넣는 도구(__HC2).
   BASE(06fd454)·NEW 둘 다에 같은 것을 넣는다 — 없는 것(c2ChipsInto · c2HsPanel …)은 빈 값으로 돌려준다.
   재는 것 = DOM 실물 · getBoundingClientRect · elementFromPoint · 계산 스타일 · 저장소 값 · 앱 상태(S · POPS · eqAll). 픽셀은 안 찍는다. */
(function(){
const wait = ms => new Promise(r => setTimeout(r, ms));
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const R = e => { if (!e) return null; const r = e.getBoundingClientRect();
  return { x: +r.left.toFixed(2), y: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2), r: +r.right.toFixed(2), b: +r.bottom.toFixed(2), cx: +(r.left + r.width / 2).toFixed(2), cy: +(r.top + r.height / 2).toFixed(2) }; };
const cs = (e, p) => e ? getComputedStyle(e)[p] : null;
async function until(f, ms){ const t0 = Date.now(); while (Date.now() - t0 < (ms || 8000)){ try { const v = f(); if (v) return v; } catch (e) {} await wait(40); } return null; }
function hitOn(t){ const r = R(t); if (!r) return null; const onScreen = r.cy > 0 && r.cy < innerHeight && r.cx > 0 && r.cx < innerWidth;
  const at = onScreen ? document.elementFromPoint(r.cx, r.cy) : null;
  return Object.assign(r, { on: !!at && (at === t || t.contains(at)) && onScreen, at: at ? String(at.className || at.tagName).slice(0, 40) : null, onScreen }); }
async function scrollHit(t){ if (!t) return null; try { t.scrollIntoView({ block: 'center', inline: 'nearest' }); } catch (e) {} await wait(180); return hitOn(t); }
function clean(){ try { closeAllPops(); } catch (e) {} document.querySelectorAll('.c2menu').forEach(x => x.remove()); const b = document.getElementById('c2mark'); if (b) b.hidden = true; try { getSelection().removeAllRanges(); } catch (e) {} }
const LAWF = { '민소': '민사소송법', '특허': '특허법', '상표': '상표법', '디보': '디자인보호법' };
const cardPop = () => [...POPS].reverse().find(p => (p._pk || '').indexOf('🧾') >= 0) || null;
async function keyOf(kind, subj, code){ const J = await get('2cha_본문_' + kind + '_' + subj + '.json'); return Object.keys(J).find(k => k === code || k.indexOf(code) >= 0) || null; }
function visible(e){ return !!e && e.isConnected && getComputedStyle(e).display !== 'none' && e.getClientRects().length > 0; }
/* 줄 안 문자열 k 번째 글자의 화면 좌표(칩 · 숨김 제외 · 글자 노드 걷기) */
function charRect(host, i){ const w = document.createTreeWalker(host, NodeFilter.SHOW_TEXT); let n, acc = 0;
  while ((n = w.nextNode())){ if (n.parentNode.closest('.c2m,.c2x')) continue; const L = n.nodeValue.length; if (i < acc + L){ const r = document.createRange(); r.setStart(n, i - acc); r.setEnd(n, i - acc + 1); const rs = r.getClientRects(); return rs.length ? rs[0] : null; } acc += L; } return null; }
/* 글 속 문자열 needle 이 보이는 폭(글자 폭 합) — 0 이면 안 보인다 */
function visWidth(root, needle){ const out = []; const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT); const ns = []; let n; while ((n = w.nextNode())) ns.push(n);
  const all = ns.map(x => x.nodeValue).join(''); let i = all.indexOf(needle);
  while (i >= 0){ let acc = 0, wsum = 0; for (const x of ns){ const L = x.nodeValue.length; const a = Math.max(i, acc), b = Math.min(i + needle.length, acc + L);
      if (b > a){ const r = document.createRange(); r.setStart(x, a - acc); r.setEnd(x, b - acc); [...r.getClientRects()].forEach(q => { wsum += q.width; }); } acc += L; }
    out.push(+wsum.toFixed(2)); i = all.indexOf(needle, i + 1); }
  return out; }
window.__HC2 = {
  wait,
  errs(){ return (window.__ERR || []).filter(e => !/^ResizeObserver loop/.test(e)).slice(0, 20); },
  has(){ return { chips: typeof c2ChipsInto === 'function', hs: typeof c2HsPanel === 'function', lk: typeof c2LkEl === 'function', mark: typeof c2MarkPaint === 'function', syncKeys: SYNC_KEYS.length, syncTail: SYNC_KEYS.slice(-4) }; },
  clean(){ clean(); return POPS.length; },
  ls(k){ try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; } },
  lsSet(k, v){ localStorage.setItem(k, JSON.stringify(v)); return true; },
  async go(law, tab, o){ clean(); S.law = law; S.tab = tab; Object.assign(S, o || {}); await render(); await wait(500); return { law: S.law, tab: S.tab }; },
  async open(kind, subj, code){ clean(); S.law = LAWF[subj]; S.tab = 'cha2'; S.boardKind = kind; await render(); await wait(300);
    const k = await keyOf(kind, subj, code); if (!k) return { miss: code };
    await popCard4(kind, k, { clientX: 240, clientY: 60 }, 1, null, null, LAWF[subj]); await wait(900);
    const p = cardPop(); return { k: k, pk: p ? p._pk : null, rect: R(p) }; },
  /* ── A 칩 ── */
  heads(){ const p = cardPop(); if (!p) return null;
    return [...p.querySelectorAll('.rbody.card > .ln.rh')].map((d, i) => { const lv = +((d.className.match(/\brh(\d)\b/) || [])[1] || 0);
      const m = d.querySelector('.c2m'), x = d.querySelector('.c2x'), t = d.querySelector('.c2t') || d;
      const o = { i: i, lv: lv, text: (t.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 60), a: m ? m.dataset.s : null, b: x ? x.dataset.s : null,
        al: m ? m.dataset.l : null, bl: x ? x.dataset.l : null, fs: m ? cs(m, 'fontSize') : null };
      if (m && x){ const rm = m.getBoundingClientRect(), rx = x.getBoundingClientRect();
        /* 번호 마지막 글자 · 글 첫 글자(숨긴 ♥·빈칸 건너뜀) */
        const host = t; let numEnd = null, txt0 = null; const all = []; const w = document.createTreeWalker(host, NodeFilter.SHOW_TEXT); let n;
        while ((n = w.nextNode())){ if (n.parentNode.closest('.c2m,.c2x')) continue; for (let k = 0; k < n.nodeValue.length; k++) all.push([n, k]); }
        const before = [], after = [];
        all.forEach(([nn, k]) => { const pos = m.compareDocumentPosition(nn); const vis = nn.parentNode.closest('.c2hide') ? false : true; if (!vis) return;
          const r = document.createRange(); r.setStart(nn, k); r.setEnd(nn, k + 1); const q = r.getClientRects()[0]; if (!q || !q.width) return;
          if (pos & Node.DOCUMENT_POSITION_PRECEDING) before.push(q); else if (pos & Node.DOCUMENT_POSITION_FOLLOWING){ const px = x.compareDocumentPosition(nn); if (px & Node.DOCUMENT_POSITION_FOLLOWING) after.push(q); } });
        numEnd = before.length ? before[before.length - 1] : null; txt0 = after.length ? after[0] : null;
        o.g1 = numEnd ? +(rm.left - numEnd.right).toFixed(2) : null; o.g2 = +(rx.left - rm.right).toFixed(2); o.g3 = txt0 ? +(txt0.left - rx.right).toFixed(2) : null;
        o.sameLine = numEnd && txt0 ? Math.abs(numEnd.top - rm.top) < 12 && Math.abs(txt0.top - rx.top) < 12 : null; }
      return o; }); },
  async chipHit(i, which){ const p = cardPop(); const d = [...p.querySelectorAll('.rbody.card > .ln.rh')][i]; const c = d && d.querySelector(which === 'x' ? '.c2x' : '.c2m'); return c ? scrollHit(c) : null; },
  menu(){ const m = document.querySelector('.c2menu'); if (!m) return { open: false };
    return { open: true, opts: [...m.querySelectorAll('.c2opt')].map(o => ({ t: txt(o), sel: o.classList.contains('sel'), cls: o.className, r: R(o) })), r: R(m), focus: document.activeElement && document.activeElement.classList.contains('c2opt') ? txt(document.activeElement) : null }; },
  htag(){ return this.ls(REC_PRE + 'c2htag') || {}; },
  embx(){ const p = cardPop(); return [...p.querySelectorAll('.embx')].map(b => ({ cls: b.className.replace(/\s+/g, ' '), bl: cs(b, 'borderLeftColor'), tag: b.textContent.indexOf('#민소/문학판검') >= 0 })); },
  tagVis(sel){ const roots = [...document.querySelectorAll(sel || '.pop')]; const out = { occ: 0, visible: 0, widths: [] };
    roots.forEach(r => { const ws = visWidth(r, '#민소/문학판검'); out.occ += ws.length; ws.forEach(w => { if (w > 0.5) out.visible++; }); out.widths.push(...ws.slice(0, 5)); }); return out; },
  async searchCount(q){ S.law = '민사소송법'; try { openSk(); } catch (e) { return { err: 'openSk' }; } await wait(200);
    Object.keys(SKON).forEach(k => { SKON[k] = true; }); try { skPaint(); } catch (e) {} const inp = document.getElementById('skin'); inp.value = q; inp.dispatchEvent(new Event('input', { bubbles: true }));
    await until(() => document.querySelectorAll('#skres .res, #skres > *').length, 6000); await wait(1200);
    const n = document.querySelectorAll('#skres .res').length; const head = txt(document.getElementById('skres')).slice(0, 120); try { closeSk(); } catch (e) {} return { n: n, head: head }; },
  /* ── B 접기 n ── */
  fold(){ const p = cardPop(); const b = p && p.querySelector('.gtabs .c2fold'); const rows = p ? [...p.querySelectorAll('.rbody.card > .ln')] : [];
    const vis = rows.filter(visible); const lv = d => +((d.className.match(/\brh(\d)\b/) || [])[1] || 0);
    const by = {}; vis.forEach(d => { const k = lv(d) ? 'h' + lv(d) : 'body'; by[k] = (by[k] || 0) + 1; });
    const tg = rows.filter(d => lv(d)).map(d => { const g = d.querySelector(':scope > .htog'); return g ? g.textContent : ''; });
    return { btn: b ? { t: txt(b), hidden: b.hidden, lv: b.dataset.lv, fs: cs(b, 'fontSize'), bw: cs(b, 'borderTopWidth'), color: cs(b, 'color'), fw: cs(b, 'fontWeight'), title: b.title } : null,
      total: rows.length, visible: vis.length, by: by, callouts: p ? [...p.querySelectorAll('.rbody.card > .callout')].filter(visible).length : 0, tg: tg.join('') }; },
  async foldClick(){ const p = cardPop(); const b = p.querySelector('.gtabs .c2fold'); return scrollHit(b); },
  async togHit(i){ const p = cardPop(); const d = [...p.querySelectorAll('.rbody.card > .ln.rh')][i]; const g = d && d.querySelector(':scope > .htog'); return g && visible(g) ? scrollHit(g) : null; },
  cltab(){ const p = cardPop(); const b = p && p.querySelector('.gtabs .cltab'); return b ? { t: txt(b), fs: cs(b, 'fontSize'), bw: cs(b, 'borderTopWidth'), bg: cs(b, 'backgroundColor'), color: cs(b, 'color'), fw: cs(b, 'fontWeight') } : null; },
  tabsOrder(){ const p = cardPop(); return p ? [...p.querySelectorAll('.gtabs > *')].map(b => b.className + ':' + txt(b)) : null; },
  /* ── C 조문 글자 링크 ── */
  fmJo(){ const p = cardPop(); const w = p && p.querySelector('.chips .c2jo'); if (!w) return null;
    return { segs: [...w.querySelectorAll('.c2sg')].map(g => txt(g)), btns: [...w.querySelectorAll('.c2jb')].map(b => ({ t: txt(b), fs: cs(b, 'fontSize'), color: cs(b, 'color'), bw: cs(b, 'borderTopWidth'), bg: cs(b, 'backgroundColor') })),
      bad: [...w.querySelectorAll('.c2jt')].map(txt), sl: [...w.querySelectorAll('.c2sl')].map(s => ({ t: txt(s), fs: cs(s, 'fontSize'), color: cs(s, 'color') })) }; },
  async fmJoHit(n){ const p = cardPop(); const b = [...p.querySelectorAll('.chips .c2jo .c2jb')][n]; return scrollHit(b); },
  joPop(){ const p = [...POPS].reverse().find(x => (x._pk || '').indexOf('jo|') === 0); if (!p) return null; const ph = p.querySelector(':scope > .ph');
    return { pk: p._pk, title: txt(ph.querySelector('.pt')), rect: R(p), head: R(ph), jhl: p.querySelectorAll('.jhl').length, chip: txt(p.querySelector('.ptchip')), hangs: [...p.querySelectorAll('.jhl')].map(d => txt(d).slice(0, 12)) }; },
  async gaekHome(minJo){ clean(); S.law = '특허법'; S.tab = 'jimun'; S.jimunTab = 'ox'; S.mok = ''; S.oxQueue = ''; await render();
    await until(() => typeof OXPOOL !== 'undefined' && OXPOOL && Object.keys(OXPOOL).length > 1000 && typeof LNKIDX !== 'undefined' && LNKIDX && LNKIDX.jo, 30000);
    const L = [].concat(...Object.values(LNKIDX.jo)); const e = L.find(x => x.z && (x.z.jo || []).length >= (minJo || 1) && x.z.uid); if (!e) return { miss: 1 };
    linkGo(e.z.uid); const sel = '#slot [data-ggu="' + e.z.uid + '"]'; await until(() => document.querySelector(sel), 20000); await wait(400);
    return { uid: e.z.uid, jo: e.z.jo, acts: document.querySelectorAll('#slot .mbact').length }; },
  /* 1차객 액션 바 — kind 'jo'(lnkChips 조문 칩) · 'more'(＋N) · 'jos'(해설 JOS) · 'won'(⚖ 원문) — 그 줄을 「정답·해설 ▸」 로 연 뒤 위치 */
  async p7Jos(id){ const P7 = await get('jimun_7pan.json'); const z = (P7.지문 || []).find(x => x.id === id); if (!z) return { miss: id };
    const c = p7Card(z, 1); let box = document.getElementById('hz_p7box'); if (!box){ box = document.createElement('div'); box.id = 'hz_p7box'; document.body.appendChild(box); }
    box.style.cssText = 'position:fixed;left:0;top:70px;width:900px;max-height:760px;overflow:auto;background:#fff;z-index:60'; box.innerHTML = ''; box.appendChild(c);
    const pk = c.querySelector('.mbpeek'); if (pk && pk.textContent.indexOf('▸') >= 0) pk.click(); await wait(300);
    return { id: id, acts: box.querySelectorAll('.mbact').length }; },
  p7Close(){ const b = document.getElementById('hz_p7box'); if (b) b.remove(); return true; },
  async gaekChip(kind, root){ const acts = [...document.querySelectorAll((root || '#slot') + ' .mbact')];
    const pick = a => { const bs = [...a.querySelectorAll('button, a')];
      if (kind === 'won') return bs.find(b => b.classList.contains('jowon'));
      if (kind === 'jo') return bs.find(b => (b.classList.contains('c2jb') || b.classList.contains('c-jo')) && /누르면 조문 원문/.test(b.title || ''));
      if (kind === 'more') return bs.find(b => (b.classList.contains('c2jb') || b.classList.contains('c-jo')) && /^＋\d/.test(txt(b)));
      if (kind === 'jos') return bs.find(b => (b.classList.contains('c2jb') || b.classList.contains('c-jo')) && !b.title && !/^＋/.test(txt(b)));
      if (kind === 'josdead') return bs.find(b => (b.classList.contains('c2jb') || b.classList.contains('c-jo')) && /시행규칙/.test(b.title || ''));
      return null; };
    const a = acts.find(pick); if (!a) return { miss: kind };
    const exp = a.parentElement; if (getComputedStyle(exp).display === 'none'){ const row = exp.parentElement; const pk = row && row.querySelector('.mbpeek'); if (pk) pk.click(); await wait(250); }
    const b = pick(a); const h = await scrollHit(b);
    return Object.assign({ t: txt(b), cls: b.className, fs: cs(b, 'fontSize'), color: cs(b, 'color'), bw: cs(b, 'borderTopWidth'), bg: cs(b, 'backgroundColor'), href: b.getAttribute('href'), op: b.style.opacity || '', cursor: cs(b, 'cursor') }, h || {}); },
  wonDom(root){ return [...document.querySelectorAll((root || '#slot') + ' .jowon')].slice(0, 40).map(a => txt(a) + '|' + (a.getAttribute('href') || '') + '|' + (a.title || '')); },
  async gradeJo(){ const p = cardPop(); const b = [...p.querySelectorAll('.gtabs .tool')].find(x => x.dataset.t === '채점'); if (b) b.click(); await wait(900);
    const j = [...p.querySelectorAll('.c2jb, .chip.c-prec')].find(x => /^(민소|특|상|디|민법)\d|^⚖ 제\d/.test(txt(x)) && (x.classList.contains('c2jb') || /제\d+조/.test(txt(x))));
    if (!j) return { miss: 1 }; const h = await scrollHit(j); return Object.assign({ t: txt(j), cls: j.className, color: cs(j, 'color'), bg: cs(j, 'backgroundColor') }, h || {}); },
  /* ── D 연결 ── */
  lk(){ const p = cardPop(); const s = p && p.querySelector('.chips .c2lk'); return s ? { btns: [...s.querySelectorAll('button')].map(b => ({ t: txt(b), cls: b.className, color: cs(b, 'color') })), idx: [...p.querySelector('.chips').children].indexOf(s) } : null; },
  async lkHit(cls){ const p = cardPop(); const b = p.querySelector('.chips .c2lk .' + cls); return b ? scrollHit(b) : null; },
  lkWin(){ const p = [...POPS].reverse().find(x => /^c2(rel|edit)\|/.test(x._pk || '')); if (!p) return null;
    return { pk: p._pk, title: txt(p.querySelector('.pt')), rows: [...p.querySelectorAll('.c2wb .row')].map(r => ({ t: txt(r).slice(0, 90), cls: r.className, src: txt(r.querySelector('.src')) })), rect: R(p) }; },
  async lkRowHit(i, sub){ const p = [...POPS].reverse().find(x => /^c2(rel|edit)\|/.test(x._pk || '')); const rs = [...p.querySelectorAll('.c2wb .row')]; const r = rs[i]; if (!r) return null; const t = sub ? r.querySelector(sub) : r; return scrollHit(t); },
  async lkSearch(q){ const p = [...POPS].reverse().find(x => /^c2edit\|/.test(x._pk || '')); const inp = p.querySelector('.c2wb input'); inp.value = q; inp.dispatchEvent(new Event('input')); await wait(300);
    return [...p.querySelectorAll('.c2wb > div:last-child .row')].map(r => txt(r).slice(0, 80)); },
  async lkResHit(i){ const p = [...POPS].reverse().find(x => /^c2edit\|/.test(x._pk || '')); const r = [...p.querySelectorAll('.c2wb > div:last-child .row')][i]; return scrollHit(r); },
  eq(){ return (eqAll() || []).map(x => ({ k: x.k, kind: x.kind, part: x.part, quote: x.quote, target: x.target, st: x.st, file: x.file })); },
  eqChip(){ const c = document.querySelector('#eqChip, .eqchip, [data-eq]'); return c ? txt(c) : txt([...document.querySelectorAll('button, span')].find(b => /^✎ 수정 \d+/.test(txt(b)))); },
  pops(){ return POPS.map(p => p._pk); },
  /* ── E 형광펜 ── */
  async callout(which){ const p = cardPop(); const c = p.querySelector('.rbody.card > .callout.co-' + (which === 'note' ? 'note' : 'question')); if (!c) return { miss: which }; c.click(); await wait(600);
    const q = POPS[POPS.length - 1]; return { pk: q._pk, rows: [...q.querySelectorAll('[data-c2mark]')].map(r => ({ key: r.dataset.c2mark, n: (r.dataset.text || '').length, t: (r.dataset.text || '').slice(0, 30) })), sel: cs(q.querySelector('.rbody .ln'), 'userSelect') }; },
  markRowRect(i, a, b){ const q = POPS[POPS.length - 1]; const r = [...q.querySelectorAll('[data-c2mark]')][i]; if (!r) return null; try { r.scrollIntoView({ block: 'center' }); } catch (e) {}
    const s = charRect(r, a), e = charRect(r, b); return s && e ? { x0: s.left + 1, y0: s.top + s.height / 2, x1: e.right - 1, y1: e.top + e.height / 2, key: r.dataset.c2mark } : null; },
  markBar(){ const b = document.getElementById('c2mark'); if (!b || b.hidden) return { shown: false }; const sel = getSelection(); const rr = sel && sel.rangeCount ? sel.getRangeAt(0).getBoundingClientRect() : null;
    return { shown: true, r: R(b), sel: rr ? { t: rr.top, b: rr.bottom } : null, below: rr ? R(b).y >= rr.bottom - 1 : null, btns: [...b.querySelectorAll('button')].map(x => x.dataset.m) }; },
  async markBtnHit(m){ const b = document.getElementById('c2mark'); const x = [...b.querySelectorAll('button')].find(y => y.dataset.m === m); return hitOn(x); },
  marks(){ return this.ls(REC_PRE + 'c2mark') || {}; },
  markSpans(){ const q = POPS[POPS.length - 1]; return [...q.querySelectorAll('[data-c2mark]')].map(r => [...r.querySelectorAll('span.c2mk')].map(s => (s.getAttribute('style') || '').slice(0, 40) + '|' + s.textContent).join(' ')); },
  selectText(i, a, b){ const q = POPS[POPS.length - 1]; const r = [...q.querySelectorAll('[data-c2mark]')][i]; const ns = []; const w = document.createTreeWalker(r, NodeFilter.SHOW_TEXT); let n; while ((n = w.nextNode())) if (!n.parentNode.closest('.c2m,.c2x')) ns.push(n);
    let acc = 0, sN, sO, eN, eO; for (const x of ns){ const L = x.nodeValue.length; if (sN == null && a < acc + L){ sN = x; sO = a - acc; } if (eN == null && b <= acc + L){ eN = x; eO = b - acc; } acc += L; }
    const rg = document.createRange(); rg.setStart(sN, sO); rg.setEnd(eN, eO); const s = getSelection(); s.removeAllRanges(); s.addRange(rg); document.dispatchEvent(new Event('selectionchange')); return true; },
  /* ── F 정렬 이름 ── */
  async sortLabel(kind, law){ clean(); S.law = law || '민사소송법'; S.tab = 'cha2'; S.boardKind = kind; await render(); await wait(400);
    const sel = [...document.querySelectorAll('select')].find(s => [...s.options].some(o => o.value === 'pct')); return sel ? { first: sel.options[0].textContent, vals: [...sel.options].map(o => o.value) } : null; },
  /* ── G 해설 탭 ── */
  async hsTab(){ const p = cardPop(); const b = [...p.querySelectorAll('.gtabs .tool')].find(x => x.dataset.t === '해설'); b.click();
    await until(() => p.querySelector('.c2hs, .c2hsw') || (p.querySelector('.gtabs + div') && !/^…$/.test(txt(p.querySelector('.gtabs + div')))), 20000); await wait(300);
    const pn = p.querySelector('.c2hs'); const cont = p.querySelector('.gtabs + div');
    return { panel: !!pn, warn: txt(p.querySelector('.c2hsw')), bsel: pn ? [...pn.querySelectorAll('.bsel button')].map(b => txt(b) + (b.classList.contains('on') ? '*' : '')) : null,
      tops: pn ? [...pn.querySelectorAll('.grp .top .m')].map(txt) : null, html: cont ? cont.innerHTML.length : 0, text: cont ? txt(cont).slice(0, 400) : '' }; },
  hsContent(){ const p = cardPop(); const cont = p.querySelector('.gtabs + div'); return cont ? cont.innerHTML : null; },
  async hsPick(name){ const p = cardPop(); const b = [...p.querySelectorAll('.c2hs .bsel button')].find(x => txt(x).indexOf(name) >= 0); if (!b) return null; b.click(); await wait(200);
    const g = [...p.querySelectorAll('.c2hs .grp')].find(x => !x.hidden); return { on: txt(p.querySelector('.c2hs .bsel button.on')), rows: [...g.querySelectorAll('.row, .sec, .none')].map(r => r.className.replace(/\s+/g, ' ') + '|' + txt(r).slice(0, 70)) }; },
  async hsRowHit(needle){ const p = cardPop(); const g = [...p.querySelectorAll('.c2hs .grp')].find(x => !x.hidden); const r = [...g.querySelectorAll('.row')].find(x => txt(x.querySelector('.a')).indexOf(needle) >= 0); return r ? Object.assign(await scrollHit(r), { ri: r.dataset.ri, pg: txt(r.querySelector('.pg')), pin: !r.querySelector('.pin').hidden }) : null; },
  hsWin(){ const p = [...POPS].reverse().find(x => x._hs); if (!p) return null; const band = [...p.querySelectorAll('.band')]; const pg = p.querySelector('.pg');
    return { pk: p._pk, title: txt(p.querySelector('.pt')), p: p._hs.st.p, ri: p._hs.st.ri, n: p._hs.st.n, bands: band.map(b => ({ top: b.style.top, h: b.style.height })), foot: txt(p.querySelector('.ft')),
      canvas: !!(pg && pg.querySelector('canvas')), pgR: R(pg), scroll: p.querySelector('.pb').scrollTop, bandR: band[0] ? R(band[0]) : null, bodyR: R(p.querySelector('.pb')), rv: !!p.querySelector('.ft button') }; },
  async hsNav(d){ const p = [...POPS].reverse().find(x => x._hs); const b = p.querySelectorAll('.ph .c2nv')[d > 0 ? 1 : 0]; return hitOn(b); },
  async hsPageAt(fy){ const p = [...POPS].reverse().find(x => x._hs); const pg = p.querySelector('.pg'); const r = pg.getBoundingClientRect(); const y = r.top + r.height * fy;
    const body = p.querySelector('.pb'); body.scrollTop = Math.max(0, pg.offsetTop + pg.offsetHeight * fy - body.clientHeight / 2); await wait(250); const r2 = pg.getBoundingClientRect();
    return { x: r2.left + r2.width / 2, y: r2.top + r2.height * fy, on: document.elementFromPoint(r2.left + r2.width / 2, r2.top + r2.height * fy) === pg.querySelector('canvas') || pg.contains(document.elementFromPoint(r2.left + r2.width / 2, r2.top + r2.height * fy)) }; },
  async hsRevertHit(){ const p = [...POPS].reverse().find(x => x._hs); const b = p.querySelector('.ft button'); return b ? scrollHit(b) : null; },
  hsJari(){ return this.ls(REC_PRE + 'c2hsjari') || {}; },
  async noToken(){ localStorage.removeItem('tt.cfg'); try { if (window.viewCanvas && viewCanvas.hsBook) viewCanvas.hsBook.stat.last = null; } catch (e) {} return !syncToken || !syncToken(); }
};
})();
