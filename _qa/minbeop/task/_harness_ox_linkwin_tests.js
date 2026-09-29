/* _task_ox_linkwin 하네스 — 브라우저 안 도구(__HZL). 누름은 playwright 진짜 마우스 / CDP 터치(r22) / WebKit 톡 · 여기서는 자리·상태만.
   바탕(앞 인도 판)에는 lwOpen 이 없다 — typeof 로 가르고 FAIL 로 끝나게 한다(헛잣대). */
(function () {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const T = n => (n ? n.textContent : '').replace(/\s+/g, ' ').trim();
  const Q = (s, r) => (r || document).querySelector(s);
  const QA = (s, r) => [...(r || document).querySelectorAll(s)];
  function vis(el) { if (!el || !el.isConnected) return false; const s = getComputedStyle(el); if (s.display === 'none' || s.visibility === 'hidden') return false; const r = el.getBoundingClientRect(); return r.height > 0 && r.width > 0; }
  async function until(f, ms) { const t0 = Date.now(); while (Date.now() - t0 < (ms || 8000)) { try { if (f()) return true; } catch (e) { } await wait(50); } return false; }
  function ptOf(el, noScroll) {
    if (!el) return { on: false, hit: false, why: 'none' };
    let r = el.getBoundingClientRect();
    if (!noScroll && (r.top < 70 || r.bottom > innerHeight - 80 || r.left < 0 || r.right > innerWidth)) { el.scrollIntoView({ block: 'center', inline: 'nearest' }); r = el.getBoundingClientRect(); }
    const x = r.left + r.width / 2, y = r.top + r.height / 2;
    const on = r.width > 0 && r.height > 0 && x >= 0 && y >= 0 && x < innerWidth && y < innerHeight;
    const top = on ? document.elementFromPoint(x, y) : null;
    return { cx: Math.round(x * 10) / 10, cy: Math.round(y * 10) / 10, w: Math.round(r.width), h: Math.round(r.height), on: on, hit: !!(top && (top === el || el.contains(top))), top: top ? (top.id ? '#' + top.id : top.tagName + '.' + String(top.className || '').slice(0, 30)) : null, txt: T(el).slice(0, 30) };
  }
  const cs = (e, ks) => { if (!e) return null; const s = getComputedStyle(e), o = {}; (ks || ['backgroundColor', 'borderTopWidth', 'color', 'fontSize', 'fontWeight']).forEach(k => { o[k] = s[k]; }); return o; };
  const links = () => { try { return JSON.parse(localStorage.getItem('ox_q_links') || '{}'); } catch (e) { return {}; } };
  const win = () => document.getElementById('oxwin-lk');
  window.__HZL = {
    has: () => typeof lwOpen === 'function',
    seed(o) { localStorage.setItem('ox_q_links', JSON.stringify(o)); try { useIdxDrop(); } catch (e) { } return JSON.stringify(links()); },
    links(id) { return JSON.stringify(links()[id] || null); },
    /* 그 문항이 든 단원·쪽으로 */
    async goQ(id) {
      document.querySelectorAll('.oxwin').forEach(w => w.remove());
      const q = quizData.find(x => x.id === id); if (!q) return JSON.stringify({ err: 'no q' });
      try { goHome(); } catch (e) { }
      const lab = q.subChapter ? q.chapter + ' > ' + q.subChapter : q.chapter;
      startQuiz(q.subject, lab);
      await until(() => QA('#quiz-container .question-box').length > 0, 20000);
      const ix = (typeof currentFilteredData !== 'undefined' ? currentFilteredData : []).findIndex(x => x.id === id);
      if (ix >= 0 && typeof PAGE_SIZE !== 'undefined') { currentPageIndex = Math.floor(ix / PAGE_SIZE); renderQuizPage(); }
      await until(() => !!document.getElementById('q-box-' + id), 10000);
      await wait(300);
      return JSON.stringify({ ok: !!document.getElementById('q-box-' + id), page: typeof currentPageIndex !== 'undefined' ? currentPageIndex : null });
    },
    lkBtn(id) { const box = document.getElementById('q-box-' + id); const b = box ? QA('button', box).find(x => T(x) === '✏️ 연결' && vis(x)) : null; return JSON.stringify(ptOf(b)); },
    qpLkBtn(id) { const w = document.getElementById('oxwin-q-' + id); const b = w ? QA('button', w).find(x => T(x) === '✏️ 연결') : null; return JSON.stringify(ptOf(b)); },
    state(id) {
      const w = win(), box = document.getElementById('q-box-' + id), mp = document.getElementById('memo-panel-' + id);
      const inp = w ? Q('input.cfq', w) : null;
      const rows = w ? QA('.cfrs .cfr', w).filter(vis).map(r => ({ id: T(Q('.cfid', r)), no: T(Q('.cfno', r)), wh: T(Q('.cfwh', r)), on: r.classList.contains('on'), op: getComputedStyle(r).opacity, has: /이미 넣음/.test(T(r)) })) : [];
      const cur = w ? QA('.cfcur .cfcr', w).map(r => T(Q('.cfid', r))) : [];
      const head = w ? Q('.oxwin-head', w) : null;
      const chips = head ? QA('.cfhc', head).map(T) : [];
      const lk = box ? QA('[data-lkchips] button', box).map(T) : [];
      return JSON.stringify({ win: !!w, vis: vis(w), w: w ? Math.round(w.getBoundingClientRect().width) : 0, z: w ? +w.style.zIndex : 0, chips: chips, focus: !!inp && document.activeElement === inp,
        memoPanel: !!mp, memoVis: vis(mp), rows: rows, cur: cur, curN: w ? T(Q('.cfcl', w)) : '', foot: w ? T(Q('.cfft', w)) : '', lkChips: lk,
        save: QA('button', box || document.body).filter(b => /저장하기/.test(T(b)) && vis(b)).length });
    },
    inp() { const w = win(); const i = w ? Q('input.cfq', w) : null; return JSON.stringify(ptOf(i, true)); },
    rowAt(id, part) { const w = win(); if (!w) return 'null'; const r = QA('.cfrs .cfr', w).find(x => T(Q('.cfid', x)) === 'ID ' + id); if (!r) return 'null';
      const t = part === 'no' ? Q('.cfno', r) : Q('.cftx', r); return JSON.stringify(ptOf(t)); },
    curX(id) { const w = win(); if (!w) return 'null'; const r = QA('.cfcur .cfcr', w).find(x => T(Q('.cfid', x)) === 'ID ' + id); return r ? JSON.stringify(ptOf(Q('.cfxx', r))) : 'null'; },
    qp(id) { const w = document.getElementById('oxwin-q-' + id); if (!w) return JSON.stringify({ win: false });
      const go = QA('button', w).find(b => /↪/.test(T(b)));
      return JSON.stringify({ win: true, vis: vis(w), z: +w.style.zIndex, go: go ? Object.assign(ptOf(go), { t: T(go), cs: cs(go) }) : null }); },
    /* 바탕(옛 판) — 카드 안 패널 · ID 칸 · 찾기 칸 · 결과 */
    oldPanel(id) { const mp = document.getElementById('memo-panel-' + id); const li = document.getElementById('link-input-' + id); const ls = document.getElementById('link-search-' + id);
      return JSON.stringify({ panel: !!mp, vis: vis(mp), input: li ? li.value : null, search: ptOf(ls), results: QA('#link-results-' + id + ' button').length }); },
    oldResAt(id, qid) { const b = QA('#link-results-' + id + ' button').find(x => x.getAttribute('onclick') && x.getAttribute('onclick').indexOf("'" + qid + "'") >= 0); return JSON.stringify(ptOf(b)); },
    boxVis(id) { const b = document.getElementById('q-box-' + id); return JSON.stringify({ on: !!b, vis: vis(b), top: b ? Math.round(b.getBoundingClientRect().top) : null }); },
    closeAll() { document.querySelectorAll('.oxwin').forEach(w => w.remove()); return '1'; },
    errs() { return JSON.stringify((window.__ERR || []).slice(0, 5)); },
    /* ★ revfix0928(9/28) A-1 — ✕ 자리·크기 · 나머지 22 종 계산값(창 테·둥근·그림자 · 머리 · 제목 · 칩 · 몸 · 찾기 라벨·칸 · 결과 줄·칸 넷 · 걸린 연결 넷 · 아래 줄) */
    xAt() { const w = win(); const x = w ? Q('.oxwin-head > button', w) : null; if (!x) return JSON.stringify({ on: false });
      const r = x.getBoundingClientRect(), h = Q('.oxwin-head', w).getBoundingClientRect();
      return JSON.stringify(Object.assign(ptOf(x, true), { cls: x.className, wf: Math.round(r.width * 10) / 10, hf: Math.round(r.height * 10) / 10, rightGap: Math.round((h.right - r.right) * 10) / 10,
        cs: cs(x, ['fontSize', 'fontWeight', 'fontFamily', 'color', 'backgroundColor', 'borderTopWidth', 'cursor', 'paddingTop', 'paddingLeft', 'marginLeft']) })); },
    xcss() { const w = win(); if (!w) return JSON.stringify(null);
      const K = ['fontSize', 'fontWeight', 'color', 'backgroundColor', 'borderTopWidth', 'borderTopColor', 'borderTopLeftRadius', 'paddingTop', 'paddingLeft', 'boxShadow', 'lineHeight'];
      const one = s => { const e = Q(s, w); return e ? cs(e, K) : null; };
      return JSON.stringify({ win: cs(w, K), head: one('.oxwin-head'), tt: one('.cftt'), chip: one('.cfhc'), body: one('.cfbd'), lb: one('.cflb'), q: one('input.cfq'), rs: one('.cfrs'), r: one('.cfrs .cfr'),
        id: one('.cfrs .cfid'), no: one('.cfrs .cfno'), wh: one('.cfrs .cfwh'), tx: one('.cfrs .cftx'), cl: one('.cfcl'), cur: one('.cfcur'), cr: one('.cfcur .cfcr'), crid: one('.cfcur .cfid'),
        crno: one('.cfcur .cfno'), xx: one('.cfxx'), ft: one('.cfft'), obody: one('.oxwin-body'), lk: one('.cflk') }); }
  };
})();
