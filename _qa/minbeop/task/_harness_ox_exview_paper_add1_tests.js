/* _task_ox_exview_paper_add1 하네스 — 브라우저 안 도구(__HZA). 누름은 playwright 진짜 마우스 / CDP 터치(반지름 22) · 여기서는 준비·상태·계산 스타일만.
   ⚠ 바탕(0d4144c · 526d944d)에는 add1 함수(exvOxCls · exvComboWait · exvRoundsFix)가 없다 — typeof 로 가르고 FAIL 로 끝나게 한다(헛잣대).
   새로고침 = sessionStorage '__hzkeep' 를 세운 뒤 reload(SEED 가 그 표지가 있으면 localStorage 를 안 지운다) → boot2(문항 · 기출키 앱 길) */
(function () {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const T = n => (n ? n.textContent : '').replace(/\s+/g, ' ').trim();
  const LSJ = k => { try { return JSON.parse(localStorage.getItem(k) || '{}') || {}; } catch (e) { return {}; } };
  const LSP = (k, v) => localStorage.setItem(k, JSON.stringify(v));
  const Q = (s, r) => (r || document).querySelector(s);
  const QA = (s, r) => [...(r || document).querySelectorAll(s)];
  const Y = '2020';
  async function until(f, ms) { const t0 = Date.now(); while (Date.now() - t0 < (ms || 8000)) { try { if (f()) return true; } catch (e) { } await wait(50); } return false; }
  /* 보임 = display ≠ none · 높이 > 0 · 화면 안 · 부모 overflow 에 안 잘림 */
  function vis(el) {
    if (!el || !el.isConnected) return false;
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden') return false;
    const r = el.getBoundingClientRect();
    if (!(r.height > 0 && r.width > 0)) return false;
    if (r.right < 0 || r.bottom < 0 || r.left > innerWidth || r.top > innerHeight) return false;
    for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) {
      const ps = getComputedStyle(p);
      if (/(hidden|clip|auto|scroll)/.test(ps.overflow + ps.overflowX + ps.overflowY)) {
        const pr = p.getBoundingClientRect();
        if (r.left < pr.left - 0.5 || r.right > pr.right + 0.5 || r.top < pr.top - 0.5 || r.bottom > pr.bottom + 0.5) return false;
      }
    }
    return true;
  }
  function chapOf(y) { const q = quizData.find(x => (x.examMeta || []).some(m => m.year === y)); const m = q && q.examMeta.find(z => z.year === y); return m ? y + '년 제' + m.round + '회' : ''; }
  function itemsOf(y, no) { return quizData.filter(q => (q.examMeta || []).some(m => m.year === y && +m.no === +no)); }
  function rawOf(q, y) { const m = (q.examMeta || []).find(z => z.year === y); return m ? (m.optRaw || '') : ''; }
  const A1 = () => typeof exvOxCls === 'function';
  window.__HZA = {
    ver: () => JSON.stringify({ a1: A1(), wait: typeof exvComboWait === 'function', fix: typeof exvRoundsFix === 'function', exv: typeof exvOn === 'function' }),
    keep: () => { sessionStorage.setItem('__hzkeep', '1'); return '1'; },
    /* 새 세션 — localStorage 는 그대로 · 문항을 짓고 기출키는 앱 길(gkeyBoot → IndexedDB → exvAfterGkey) */
    boot2: async function () {
      const M = await (await fetch('/data/master.json')).json();
      quizData.length = 0; buildQuizData(M.rows).forEach(q => quizData.push(q));
      try { await gkeyBoot(); } catch (e) { }
      await until(() => typeof GKEY !== 'undefined' && GKEY && GKEY.keys, 20000);
      return JSON.stringify({ q: quizData.length, gkey: !!(GKEY && GKEY.keys), combo: Object.keys(EXV_COMBO).length });
    },
    open: async function (y) {
      document.querySelectorAll('.oxwin').forEach(w => w.remove());
      try { goHome(); } catch (e) { }
      startQuiz('변리사 기출', chapOf(y));
      await until(() => QA('#quiz-container .question-box').length > 0, 20000);
      await until(() => !QA('#quiz-container .exv-wait').length, 60000);
      await wait(200);
      return JSON.stringify({ label: currentChapterLabel, on: exvOn(), page: currentPageIndex });
    },
    /* 그 해 정답(조합 선지를 다 읽고) — 준비용 */
    answers: async function (y) {
      const nos = Object.keys(GKEY.keys[y]).map(Number).sort((a, b) => a - b);
      await exvComboLoad(y, nos);
      const A = {}; nos.forEach(n => { const c = exvCorrect(y, n); A[n] = c.ans.length ? c.ans[0] : 0; });
      return A;
    },
    /* 고른 답 = 정답(from~to) — 준비(누름 게이트가 아니다) */
    pickRight: async function (y, from, to) {
      const A = await this.answers(y), P = LSJ('ox_exam_pick');
      for (let n = from; n <= to; n++) if (A[n]) P[y + ':' + n] = A[n];
      LSP('ox_exam_pick', P);
      try { exvPaint(); } catch (e) { }
      return JSON.stringify(Object.keys(P).filter(k => k.indexOf(y + ':') === 0).length);
    },
    /* 이 세션 조합 선지 결과를 그 해만 비운다(「안 연 쪽은 아직 안 읽음」 흉내 = 새로고침 뒤와 같은 상태) */
    comboForget: function (y) { let n = 0; Object.keys(EXV_COMBO).forEach(k => { if (k.indexOf(y + ':') === 0) { delete EXV_COMBO[k]; n++; } }); return JSON.stringify(n); },
    goPage: async function (p) { currentPageIndex = p; renderQuizPage(); await until(() => !QA('#quiz-container .exv-wait').length, 60000); await wait(250); return JSON.stringify({ page: currentPageIndex, nos: QA('#quiz-container .exv-q').map(q => +q.dataset.exq.split(':')[1]) }); },
    /* ── A1 준비 — 그 문항 지문의 지금 결과(ox_q_history · ox_q_last · ox_weak_stage)를 비운다.
          실물 기록에 이미 키가 있으면 「새 키 0 / 기록 1」 이 양쪽 다 거저 같아진다(첫 판 A1 헛패스 · 9/27) */
    a1clean: function (key) {
      const [y, no] = key.split(':'), ids = itemsOf(y, no).map(q => q.id);
      const QH = LSJ('ox_q_history'), QL = LSJ('ox_q_last'), WS = LSJ('ox_weak_stage');
      ids.forEach(u => { delete QH[u]; delete QL[u]; delete WS[u]; });
      LSP('ox_q_history', QH); LSP('ox_q_last', QL); LSP('ox_weak_stage', WS);
      return JSON.stringify({ ids: ids, left: ids.filter(u => Object.prototype.hasOwnProperty.call(LSJ('ox_q_history'), u)).length });
    },
    /* ── A1 채점 전 기록 — 문항 key 의 지문들 */
    a1: function (key) {
      const q = Q('#quiz-container .exv-q[data-exq="' + key + '"]');
      if (!q) return JSON.stringify(null);
      const ids = QA('.question-box', q).map(b => b.id.replace('q-box-', ''));
      const QH = LSJ('ox_q_history');
      return JSON.stringify({
        ids: ids, res: EXV_RES[key] === undefined ? 'undef' : EXV_RES[key], open: !!EXV_OPEN[key],
        items: ids.map(id => ({ id: id, exp: vis(document.getElementById('exp-' + id)), ox: vis(document.getElementById('ox-O-' + id)),
          pre: vis(Q('#q-box-' + id + ' .exv-pre')) || vis((document.getElementById('q-box-' + id) || document).querySelector('.exv-pre')), qh: Object.prototype.hasOwnProperty.call(QH, id) })),
        qhN: Object.keys(QH).length, peekTxt: T(Q('.exv-peek', q))
      });
    },
    /* ── A2~A5 회독 */
    rounds: function (y) { const R = LSJ('ox_exam_rounds'); return JSON.stringify((R[y] || []).map(r => ({ ok: r.ok, n: r.n, fixedAt: r.fixedAt || null }))); },
    resNull: function (y) { return JSON.stringify(Object.keys(EXV_RES).filter(k => k.indexOf(y + ':') === 0 && EXV_RES[k] === null).map(k => +k.split(':')[1])); },
    toast: function () { const t = document.getElementById('exv-toast'); return JSON.stringify(t ? { txt: T(t), vis: vis(t) && t.classList.contains('on') } : null); },
    pill: function () { const ab = document.getElementById('action-btn'); return JSON.stringify(ab ? { txt: T(ab), vis: vis(ab), onclick: ab.getAttribute('onclick') } : null); },
    /* 읽는 중 흉내 — mbExam.index 를 ms 늦춘다(이 세션만) */
    slowIndex: function (ms) {
      if (!window.mbExam || !mbExam.index) return JSON.stringify(false);
      if (!mbExam.__orig) mbExam.__orig = mbExam.index;
      const o = mbExam.__orig;
      mbExam.index = async function (f) { await wait(ms); return o.apply(this, arguments); };
      return JSON.stringify(true);
    },
    fastIndex: function () { if (window.mbExam && mbExam.__orig) mbExam.index = mbExam.__orig; return '1'; },
    /* 전체 채점을 한 번 더 누를 수 있게(앞 저장 뒤) — 그 해 세션 채점·끝남 표지를 푼다(준비) */
    regradeReady: async function (y) { Object.keys(EXV_RES).forEach(k => { if (k.indexOf(y + ':') === 0) delete EXV_RES[k]; }); delete EXV_DONE[y]; await this.pickRight(y, 1, 40); return '1'; },
    /* 옛 회독 심기 — picks = 정답 40 · ok = 34(조합형 여섯을 셈에서 빠뜨린 옛 값) · fixedAt 없음 */
    seedOld: async function (y, ok) {
      const A = await this.answers(y), P = {};
      Object.keys(A).forEach(n => { if (A[n]) P[n] = A[n]; });
      const R = LSJ('ox_exam_rounds'); R[y] = [{ date: '2026. 9. 26.', ok: ok, n: 40, ms: 3600000, picks: P }];
      LSP('ox_exam_rounds', R);
      return JSON.stringify(R[y].length);
    },
    fixWait: async function () { await until(() => !!window.__exvFix, 30000); return JSON.stringify(window.__exvFix || null); },
    /* ── A4 정리 창 「문제 N」 칸 */
    jxCells: async function (y, nos) {
      await until(() => QA('.jx-no[data-jxno]').length > 0, 10000);
      await until(() => !QA('.jx-cell').some(c => T(c) === '…'), 15000);
      await wait(200);
      const out = {};
      /* 보임은 그 칸을 창 안으로 굴린 뒤 잰다(정리 창 아래쪽 줄은 굴리기 전엔 창 밖 — 9/27 둘째 판 A4 가 일곱 칸 다 「안 보임」) */
      nos.forEach(no => { const r = Q('.jx-no[data-jxno="' + no + '"]'); const cs = r ? QA('.jx-cell', r) : []; const c = cs[cs.length - 1];
        if (c) c.scrollIntoView({ block: 'center', behavior: 'instant' });
        out[no] = c ? { t: T(c), tip: c.dataset.tip || '', vis: vis(c) } : null; });
      return JSON.stringify(out);
    },
    /* 정리 창 N 번 줄의 출처 칸(__HZX.jxInfo 는 1번 줄만 본다 — 첫 판 A4 가 24번을 누르고 1번 줄을 쟀다 · 9/27) */
    jxInfo: function (no) {
      const w = QA('.oxwin').filter(x => x.id.indexOf('oxwin-jn-') === 0).slice(-1)[0];
      const r = w ? Q('.jx-no[data-jxno="' + no + '"]', w) : null, i = r ? Q('.jx-info', r) : null;
      const on = r ? QA('.jx-cell.rec-on', r) : [];
      return JSON.stringify(i ? { vis: vis(i), txt: T(i), onTip: on.length ? (on[0].dataset.tip || '') : null } : null);
    },
    /* ── A6 × 동기화 — 2026 1번 ㄱ(X): 회독 1(9/20) O · 회독 2(9/25) X · 지금 결과 X(ox_q_last = 9/25) · 원격 = 지금 기록(도장 = 9/25) */
    a6prep: function () {
      const y = '2026', X = (itemsOf(y, 1).find(q => rawOf(q, y) === 'ㄱ') || {}).id;
      if (!X) return JSON.stringify({ err: 'no X' });
      const k = chapKeyOf('변리사 기출', chapOf(y));
      const H = LSJ('ox_chap_history');
      H[k] = H[k] || [];
      if (!H[k][0]) H[k][0] = { score: 0, total: 0, confuse: 0, fake: 0, date: '2026. 9. 20.', marks: {}, cf: {}, labels: {} };
      H[k][0].marks[X] = true;
      H[k] = [H[k][0], { score: 0, total: 1, confuse: 0, fake: 0, date: '2026. 9. 25.', marks: { [X]: false }, cf: {}, labels: {} }];
      LSP('ox_chap_history', H);
      const QH = LSJ('ox_q_history'), QL = LSJ('ox_q_last'), G = LSJ('ox_rec_gone');
      QH[X] = false; QL[X] = Date.parse('2026-09-25T09:00:00+09:00');
      Object.keys(G).forEach(g => { if (g.indexOf(X) >= 0) delete G[g]; });
      LSP('ox_q_history', QH); LSP('ox_q_last', QL); LSP('ox_rec_gone', G);
      try { stampAll(); } catch (e) { }
      window.__A6R = JSON.parse(JSON.stringify(recPayload(null)));
      window.__REMOTE_REC = window.__A6R; window.__PUTS = [];
      return JSON.stringify({ X: X, key: k, stamp: (LSJ('ox_sync_u')[ckey('ox_q_history', X)] || null), qh: QH[X] });
    },
    a6state: async function (X) {
      await until(() => (window.__PUTS || []).length > 0 && (typeof recBusy === 'undefined' || !recBusy), 8000);
      await wait(300);
      const QH = LSJ('ox_q_history');
      let put = null;
      try { const last = (window.__PUTS || []).slice(-1)[0]; if (last) { const b = JSON.parse(last); const j = JSON.parse(decodeURIComponent(escape(atob(b.content)))); const qh = j.data && j.data.ox_q_history; put = qh ? (typeof qh === 'string' ? JSON.parse(qh) : qh)[X] : undefined; } } catch (e) { put = 'err ' + e; }
      let weak = null; try { weak = weakQueueItems().some(q => q.id === X); } catch (e) { weak = 'err ' + e; }
      return JSON.stringify({ qh: Object.prototype.hasOwnProperty.call(QH, X) ? QH[X] : null, put: put, puts: (window.__PUTS || []).length, weak: weak, stamp: LSJ('ox_sync_u')[ckey('ox_q_history', X)] || null });
    },
    /* ── A7 시계 — ▶ · 숫자 · ↺ 가 창 제목 줄 안이고 부모에 안 잘림 · 그 자리 맨 위가 그 단추 */
    a7: function () {
      const w = document.getElementById('oxwin-omr'), hd = w && Q('.oxwin-head', w), tm = document.getElementById('exv-timer');
      if (!hd || !tm) return JSON.stringify(null);
      const H = hd.getBoundingClientRect();
      const one = el => { if (!el) return null; const r = el.getBoundingClientRect(); const cx = r.left + r.width / 2, cy = r.top + r.height / 2; const top = document.elementFromPoint(cx, cy);
        return { in: r.left >= H.left - 0.5 && r.right <= H.right + 0.5 && r.top >= H.top - 0.5 && r.bottom <= H.bottom + 0.5, vis: vis(el), hit: !!(top && (top === el || el.contains(top))), w: Math.round(r.width), txt: T(el).slice(0, 12) }; };
      return JSON.stringify({ state: tm.dataset.state || '', go: one(Q('.exv-t-go', tm)), v: one(Q('.exv-t-v', tm)), rs: one(document.getElementById('exv-t-reset')), inTitle: !!tm.closest('.oxwin-head > div'), headW: Math.round(H.width), winW: Math.round(w.getBoundingClientRect().width) });
    },
    timerSet: function (y, sec, run) { const all = LSJ('ox_exam_timer'); all[y] = run ? { acc: 0, since: Date.now() - sec * 1000 } : { acc: sec * 1000, since: 0 }; LSP('ox_exam_timer', all); try { exvTimerPaint(); } catch (e) { } return '1'; },
    /* ── A8 선지 — 문항마다 선지 글 줄 수(번호 원 빼고 글 노드 조각의 top 이 몇 갈래인가) · 옆 선지와 글 겹침 · 선지 줄 밖으로 나간 글 · 자리.
          첫 판은 높이만 쟀다 — 높이는 한 줄인데 글이 칸(58px)을 넘어 옆 선지와 겹친 것(nowrap + 5칸 격자)을 못 잡았다(9/27 탐침) */
    a8: function (keys) {
      const out = {};
      (Array.isArray(keys) ? keys : [keys]).forEach(key => {
        const q = Q('#quiz-container .exv-q[data-exq="' + key + '"]');
        const sel = q ? Q('.exv-sel', q) : null;
        if (!sel) { out[key] = null; return; }
        sel.scrollIntoView({ block: 'center' });
        const S = sel.getBoundingClientRect(), os = QA('.exv-opt', sel);
        const box = os.map(o => o.getBoundingClientRect());
        const txt = os.map(o => { const r = document.createRange(); r.selectNodeContents(o); return r.getBoundingClientRect(); });
        const lines = os.map(o => {
          const tops = [], w = document.createTreeWalker(o, NodeFilter.SHOW_TEXT); let n;
          while ((n = w.nextNode())) { if (n.parentElement.closest('.exv-num')) continue; const r = document.createRange(); r.selectNodeContents(n); [...r.getClientRects()].forEach(x => { if (x.width > 0.5) tops.push(x.top); }); }
          tops.sort((a, b) => a - b); let c = 0, last = -1e9; tops.forEach(t => { if (t - last > 2) { c++; last = t; } }); return c;
        });
        const ov = [];
        for (let i = 0; i < os.length; i++) for (let j = i + 1; j < os.length; j++) {
          const a = txt[i], b = txt[j], va = box[i], vb = box[j];
          if (!(va.bottom <= vb.top + 0.5 || vb.bottom <= va.top + 0.5) && a.right > b.left + 0.5 && b.right > a.left + 0.5) ov.push([i + 1, j + 1]);
        }
        const R1 = v => Math.round(v * 10) / 10;
        out[key] = { n: os.length, txt: os.map(T), lines: lines, ov: ov,
          out: txt.filter(t => t.right > S.right + 0.5 || t.left < S.left - 0.5).length,
          vis: os.map(vis), ws: os.length ? getComputedStyle(os[0]).whiteSpace : null, disp: getComputedStyle(sel).display,
          pos: box.map(b => [R1(b.left - S.left), R1(b.top - S.top), R1(b.width), R1(b.height)]), selW: R1(S.width) };
      });
      out.__doc = { sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth };
      return JSON.stringify(out);
    },
    /* ── A9 기출뷰 밖 카드 — 단원 풀기 첫 카드 「정답·해설 ▸」 → O */
    unitOpen: async function (subj) {
      document.querySelectorAll('.oxwin').forEach(w => w.remove());
      try { goHome(); } catch (e) { }
      const lab = QA('[data-trrow^="' + subj + '|||"]').map(x => x.getAttribute('data-trrow').split('|||')[1])[0];
      if (!lab) return JSON.stringify({ err: 'no unit' });
      startQuiz(subj, lab);
      await until(() => QA('#quiz-container .question-box').length > 0, 20000);
      await wait(300);
      const b = QA('#quiz-container .question-box')[0];
      return JSON.stringify({ id: b ? b.id.replace('q-box-', '') : null, exv: exvOn(), label: currentChapterLabel });
    },
    unitState: function (id) {
      const QH = LSJ('ox_q_history'), r = Q('input[name="answer_' + id + '"][value="O"]');
      return JSON.stringify({ exp: vis(document.getElementById('exp-' + id)), checked: !!(r && r.checked), disabled: !!(r && r.disabled), qh: Object.prototype.hasOwnProperty.call(QH, id) ? QH[id] : null,
        sess: (typeof currentSessionMarks !== 'undefined' && currentSessionMarks && Object.prototype.hasOwnProperty.call(currentSessionMarks, id)) ? currentSessionMarks[id] : null });
    }
  };
})();
