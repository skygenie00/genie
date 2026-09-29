/* _task_ox_exview_paper_add3 하네스 — 브라우저 안 도구(__HZC). 누름은 playwright 진짜 마우스 / CDP 터치(반지름 22) / WebKit 마우스 · 필터는 진짜 select(select_option).
   §C-1 서랍 해 차례 · §C-2 정리 창 거름. 바탕(앞 인도 판)에는 새 함수가 없다 — typeof 로 가르고 FAIL 로 끝나게 한다(헛잣대). */
(function () {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const T = n => (n ? n.textContent : '').replace(/\s+/g, ' ').trim();
  const LSJ = k => { try { return JSON.parse(localStorage.getItem(k) || '{}') || {}; } catch (e) { return {}; } };
  const LSP = (k, v) => localStorage.setItem(k, JSON.stringify(v));
  const Q = (s, r) => (r || document).querySelector(s);
  const QA = (s, r) => [...(r || document).querySelectorAll(s)];
  function vis(el) {
    if (!el || !el.isConnected) return false;
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden') return false;
    const r = el.getBoundingClientRect();
    return r.height > 0 && r.width > 0;
  }
  async function until(f, ms) { const t0 = Date.now(); while (Date.now() - t0 < (ms || 8000)) { try { if (f()) return true; } catch (e) { } await wait(50); } return false; }
  function ptOf(el, noScroll) {
    if (!el) return { on: false, hit: false, why: 'none' };
    let r = el.getBoundingClientRect();
    if (!noScroll && (r.top < 70 || r.bottom > innerHeight - 80 || r.left < 0 || r.right > innerWidth)) { el.scrollIntoView({ block: 'center', inline: 'nearest' }); r = el.getBoundingClientRect(); }
    const x = r.left + r.width / 2, y = r.top + r.height / 2;
    const on = r.width > 0 && r.height > 0 && x >= 0 && y >= 0 && x < innerWidth && y < innerHeight;
    const top = on ? document.elementFromPoint(x, y) : null;
    return { cx: Math.round(x * 10) / 10, cy: Math.round(y * 10) / 10, w: Math.round(r.width), h: Math.round(r.height), on: on,
             hit: !!(top && (top === el || el.contains(top))), top: top ? (top.id ? '#' + top.id : top.tagName + '.' + String(top.className || '').slice(0, 30)) : null, txt: T(el).slice(0, 40) };
  }
  const lab = q => q.subChapter ? q.chapter + ' > ' + q.subChapter : q.chapter;
  /* 1.1 묶음 — 앱과 같은 열쇠(jnKeyOf) · 줄 이름은 quizData 첫 등장 차례 */
  function group(subject, gkey) {
    const out = [];
    quizData.forEach(q => { if (q.subject === subject && jnKeyOf(q.subChapter || q.chapter, lab(q)) === gkey && out.indexOf(lab(q)) < 0) out.push(lab(q)); });
    return out;
  }
  function idsOf(subject, labels) { return quizData.filter(q => q.subject === subject && labels.indexOf(lab(q)) >= 0).map(q => q.id); }
  function jnWin() { return QA('.oxwin').filter(x => x.id.indexOf('oxwin-jn-') === 0).slice(-1)[0] || null; }

  window.__HZC = {
    has: () => JSON.stringify({ sort: typeof exvYearSort === 'function', flt: typeof jnFilter === 'function', sync: typeof jnFilterSync === 'function' }),
    /* ── §C-1 서랍 */
    drawer: function () {
      const head = QA('#trhead button').map(b => ({ t: T(b), on: b.classList.contains('on') }));
      const ch = QA('#trlist .trch').map(T);
      const it = QA('#trlist .trit[data-trk]').map(x => x.getAttribute('data-trk').split('|||').slice(1).join('|||'));
      const f = Q('#trlist .trch'), fi = Q('#trlist .trit[data-trk]');
      return JSON.stringify({ subj: (head.find(h => h.on) || {}).t || null, head: head.map(h => h.t), ch: ch.slice(0, 40), it: it, n: it.length,
        first: f ? { t: T(f), vis: vis(f) } : null, firstIt: fi ? { t: T(fi).slice(0, 30), vis: vis(fi) } : null, onQuiz: !Q('#quiz-screen').classList.contains('hide') });
    },
    dashYears: function () { return JSON.stringify(QA('[data-trrow^="변리사 기출|||"]').map(x => x.getAttribute('data-trrow').split('|||').slice(1).join('|||'))); },
    headBtn: function (name) { const b = QA('#trhead button').find(x => T(x) === name); return JSON.stringify(ptOf(b, true)); },
    /* ── §C-2 정리 창 거름 — 심기: ⚠️ 페이크 셋(1.1 묶음 둘 + 2026 기출 한 지문 · 1.1 밖) · 다른 페이크는 다 끔 · 1.1 묶음 💡 개념도 끔(빈 거름 확인용) */
    seed: function () {
      const G = group('민법총칙', '1.1');
      const ids = idsOf('민법총칙', G);
      const TG = LSJ('ox_q_tags');
      let off = 0;
      Object.keys(TG).forEach(k => { if (TG[k] && TG[k].fake) { TG[k].fake = false; off++; } });
      ids.forEach(k => { if (TG[k] && TG[k].concept) TG[k].concept = false; });
      const a = ids[1], b = ids[ids.length - 2];
      const c = (quizData.find(q => (q.examMeta || []).some(m => String(m.year) === '2026') && ids.indexOf(q.id) < 0) || {}).id;
      [a, b, c].forEach(k => { TG[k] = Object.assign({}, TG[k] || {}, { fake: true }); });
      LSP('ox_q_tags', TG);
      /* 2026 정리 창에 남을 지문 = 심은 셋 가운데 2026 기출인 것(보통 c 하나) · 그 문번 */
      const m26 = id => { const q = quizData.find(x => x.id === id); const m = q && (q.examMeta || []).find(z => String(z.year) === '2026'); return m ? +m.no : null; };
      const y26 = [a, b, c].filter(k => m26(k) !== null);
      try { renderDashboard(); } catch (e) { }
      return JSON.stringify({ labels: G, n: ids.length, per: G.map(l => [l, idsOf('민법총칙', [l]).length]), seeded: [a, b, c], in11: [a, b],
        y26: y26, nos26: [...new Set(y26.map(m26))].sort((x, y) => x - y), fakeOff: off });
    },
    jnBtnKey: function (subject, gkey) {
      const b = QA('button[data-jn]').find(x => (x.getAttribute('onclick') || '').indexOf("openJeongni('" + subject + "','" + gkey + "',this)") >= 0);
      return JSON.stringify(Object.assign(ptOf(b), { jn: b ? b.getAttribute('data-jn') : null }));
    },
    jnBtnYear: function (y) {
      const b = QA('button[data-jn]').find(x => (x.getAttribute('onclick') || '').indexOf("openJeongni('변리사 기출'") >= 0 && (x.getAttribute('data-jn') || '').indexOf(y + '년') === 0);
      return JSON.stringify(Object.assign(ptOf(b), { jn: b ? b.getAttribute('data-jn') : null }));
    },
    win: function () {
      const w = jnWin();
      if (!w) return JSON.stringify({ win: false });
      const head = Q('.oxwin-head > div', w);
      const rows = QA('[data-jnrow]', w).map(r => r.getAttribute('data-jnrow'));
      return JSON.stringify({ win: true, vis: vis(w), id: w.id, title: head ? T(head.children[0]) : null, sub: head && head.children[1] ? T(head.children[1]) : null,
        rows: rows, n: rows.length, heads: QA('[data-jnh]', w).map(T), jx: QA('.jx-no', w).map(x => +x.getAttribute('data-jxno')),
        empty: (() => { const e = Q('[data-jnempty]', w); return e ? { t: T(e), vis: vis(e) } : null; })(), jnf: w.getAttribute('data-jnf'),
        rowsVis: QA('[data-jnrow]', w).slice(0, 3).map(vis) });
    },
    closeWins: function () { QA('.oxwin').forEach(w => w.remove()); return '1'; },
    filterVal: function () { const s = Q('#review-filter'); return JSON.stringify({ v: s.value, t: T(s.options[s.selectedIndex]) }); }
  };
})();
