/* _task_ox_exview_paper 하네스 — 브라우저 안 도구(__HZX). 누름은 playwright 진짜 마우스 / CDP 터치(반지름 22) · 여기서는 자리·상태·계산 스타일만.
   ⚠ BASE(e5ca92e8)에는 기출뷰 함수가 없다 — typeof 로 가르고 FAIL 로 끝나게 한다(헛잣대). onload 는 끄고 준비를 직접 한다(앞 판 하네스와 같다). */
window.onload = null;
(function () {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const T = n => (n ? n.textContent : '').replace(/\s+/g, ' ').trim();
  const LSJ = k => { try { return JSON.parse(localStorage.getItem(k) || '{}') || {}; } catch (e) { return {}; } };
  const LSP = (k, v) => localStorage.setItem(k, JSON.stringify(v));
  const HAS = () => typeof exvOn === 'function';
  const Q = (s, r) => (r || document).querySelector(s);
  const QA = (s, r) => [...(r || document).querySelectorAll(s)];
  function vis(el) {
    if (!el || !el.isConnected) return false;
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden') return false;
    const r = el.getBoundingClientRect();
    return r.height > 0 && r.width > 0;
  }
  function dispOf(el) { return el ? getComputedStyle(el).display : null; }
  async function until(f, ms) { const t0 = Date.now(); while (Date.now() - t0 < (ms || 8000)) { try { if (f()) return true; } catch (e) { } await wait(50); } return false; }
  async function settle() { let y = -1, n = 0; for (let i = 0; i < 60 && n < 4; i++) { await wait(40); if (scrollY === y) n++; else { n = 0; y = scrollY; } } }
  /* 누를 자리 — 화면 밖이면 가운데로 굴린 뒤 잰다(화면 밖 elementFromPoint 는 null 이라 「안 가로챈다」가 거저 참이 된다) */
  function ptOf(el, noScroll) {
    if (!el) return { on: false, hit: false, why: 'none' };
    let r = el.getBoundingClientRect();
    if (!noScroll && (r.top < 70 || r.bottom > innerHeight - 80 || r.left < 0 || r.right > innerWidth)) { el.scrollIntoView({ block: 'center', inline: 'nearest' }); r = el.getBoundingClientRect(); }
    const x = r.left + r.width / 2, y = r.top + r.height / 2;
    const on = r.width > 0 && r.height > 0 && x >= 0 && y >= 0 && x < innerWidth && y < innerHeight;
    const top = on ? document.elementFromPoint(x, y) : null;
    return { cx: Math.round(x * 10) / 10, cy: Math.round(y * 10) / 10, w: Math.round(r.width), h: Math.round(r.height), on: on,
             hit: !!(top && (top === el || el.contains(top))), top: top ? (top.id ? '#' + top.id : top.tagName + '.' + String(top.className || '').slice(0, 30)) : null,
             txt: T(el).slice(0, 30) };
  }
  const Y26 = '2026';
  function chapOf(y) { const q = quizData.find(x => (x.examMeta || []).some(m => m.year === y)); const m = q && q.examMeta.find(z => z.year === y); return m ? y + '년 제' + m.round + '회' : ''; }
  function ck(y) { return chapKeyOf('변리사 기출', chapOf(y)); }
  function itemsOf(y, no) { return quizData.filter(q => (q.examMeta || []).some(m => m.year === y && +m.no === +no)); }
  function rawOf(q, y) { const m = (q.examMeta || []).find(z => z.year === y); return m ? (m.optRaw || '') : ''; }
  function uidOf(y, no, lab) { const q = itemsOf(y, no).find(x => rawOf(x, y) === lab); return q ? q.id : null; }
  function toastTxt() { const t = document.getElementById('exv-toast'); return t ? { txt: T(t), on: t.classList.contains('on') } : null; }

  window.__HZX = {
    ver: () => JSON.stringify({ has: HAS(), gkey: typeof GKEY !== 'undefined' && !!GKEY, sync: typeof SYNC_KEYS !== 'undefined' ? SYNC_KEYS.slice() : null }),
    err: () => JSON.stringify({ err: window.__ERR || [], alerts: window.__ALERTS || [], net: (window.__NET || []).slice(-40) }),
    pt: (sel, i, noScroll) => { const el = QA(sel)[i || 0]; return JSON.stringify(ptOf(el, noScroll)); },
    settle: async () => { await settle(); return '1'; },
    /* ── 준비 — 실물 기록(studyplandata origin/main)을 넣고 문항 JSON 을 싣는다 · 시험지 몫 키는 비운다 · 흉내 기록은 여기서 한 번(두 판 같게) */
    setup: async function () {
      const R = {};
      const rec = await (await fetch('/data/rec.json')).json();
      const D = rec.data || rec;
      localStorage.clear();
      const BASE = { 'ox_uid_migrated': '1', 'ox_gg_okreset': '1', 'ox_auto_important_v2': '1' };
      for (const k in BASE) localStorage.setItem(k, BASE[k]);
      for (const k in D) localStorage.setItem(k, typeof D[k] === 'string' ? D[k] : JSON.stringify(D[k]));
      ['ox_exam_pick', 'ox_exam_rounds', 'ox_exam_timer', 'ox_rec_gone'].forEach(k => localStorage.removeItem(k));
      localStorage.setItem('tt.cfg', JSON.stringify({ person: '하네스', token: 'github_pat_HARNESS' }));
      try { useIdxDrop(); } catch (e) { }
      const M = await (await fetch('/data/master.json')).json();
      quizData.length = 0; buildQuizData(M.rows).forEach(q => quizData.push(q));
      R.q = quizData.length;
      /* 기출 진행중은 비운다(startQuiz 가 이어 풀기로 들어가지 않게) */
      const P = LSJ('ox_in_progress'); Object.keys(P).forEach(k => { if (k.indexOf('변리사 기출||') === 0) delete P[k]; }); LSP('ox_in_progress', P);
      /* 시험 대상 지문 — 2026 1번 ㄱ·ㄴ·ㄷ(G5·G6 카드) · 2026 2번 ①(G6 정리 창 · 흉내 회독의 X) — 기록·태그를 깨끗이 */
      const U = { a: uidOf(Y26, 1, 'ㄱ'), b: uidOf(Y26, 1, 'ㄴ'), c: uidOf(Y26, 1, 'ㄷ'), h: uidOf(Y26, 2, '1') };   /* 일반 문항 표지는 숫자(2026:2:1) */
      R.U = U;
      const ids = Object.values(U).filter(Boolean);
      const H = LSJ('ox_chap_history');
      Object.keys(H).forEach(k => (H[k] || []).forEach(a => { if (a && a.marks) ids.forEach(u => { delete a.marks[u]; if (a.cf) delete a.cf[u]; }); }));
      const P2 = LSJ('ox_in_progress'); Object.keys(P2).forEach(k => { const a = P2[k]; if (a && a.marks) ids.forEach(u => delete a.marks[u]); }); LSP('ox_in_progress', P2);
      const QH = LSJ('ox_q_history'), QL = LSJ('ox_q_last'), TG = LSJ('ox_q_tags'), WS = LSJ('ox_weak_stage');
      ids.forEach(u => { delete QH[u]; delete QL[u]; delete WS[u]; if (TG[u]) { TG[u].confuse = false; TG[u].fake = false; } });
      QH[U.h] = false;                                   /* 흉내 회독의 X 가 지금 결과다(약점에 있다) */
      /* G8 흉내 — 2026 회독 하나: 시험지 32/40 · 72분 10초 / 지문 🌀3 ⚠2 X12 /188(1번 ㄱㄴㄷ 은 뺀다 · 2번 ① 은 X 열둘 중 하나) */
      const k26 = ck(Y26), it26 = quizData.filter(q => (q.examYears || []).includes(Y26));
      const marks = {}; let x = 0;
      it26.forEach(q => { if (q.id === U.a || q.id === U.b || q.id === U.c) return; marks[q.id] = true; });
      marks[U.h] = false; x = 1;
      Object.keys(marks).forEach(u => { if (x < 12 && marks[u] === true && u !== U.h) { marks[u] = false; x++; } });
      H[k26] = [{ score: Object.values(marks).filter(v => v).length, total: it26.length, confuse: 3, fake: 2, date: '2026. 9. 20.', marks: marks, cf: {}, labels: {} }];
      LSP('ox_chap_history', H); LSP('ox_q_history', QH); LSP('ox_q_last', QL); LSP('ox_q_tags', TG); LSP('ox_weak_stage', WS);
      R.k26 = k26; R.n26 = it26.length; R.chap26 = chapOf(Y26);
      R.has = HAS();
      if (HAS()) {
        await gkeyRefresh(null, true);                   /* 앱 길 그대로 — 서버(비공개 저장소 · 하네스가 대답) → IndexedDB */
        let idb = null; try { idb = await dbGet('gkey'); } catch (e) { }
        R.gkey = GKEY ? { meta: GKEY.meta, years: Object.keys(GKEY.keys).length, ct: Object.keys(GKEY.comboText || {}), pno: Object.keys(GKEY.pdfNo || {}) } : null;
        R.gkeyIdb = !!(idb && idb.keys);
        /* 흉내 시험지 회독 — 정답대로 32 · 틀림 8(1~8번을 틀린 번호로) · 72분 10초 */
        const P = {};
        for (let n = 1; n <= 40; n++) { const c = exvCorrect(Y26, n); P[n] = c.ans.length ? c.ans[0] : 1; }
        R.ans26raw = Object.assign({}, P);
        for (let n = 1; n <= 8; n++) P[n] = (P[n] % 5) + 1;
        LSP('ox_exam_rounds', { [Y26]: [{ date: '2026. 9. 20.', ok: 32, n: 40, ms: 72 * 60000 + 10000, picks: P }] });
      }
      R.errs = (window.__ERR || []).length;
      return JSON.stringify(R);
    },
    /* ── G1 JS 몫 — 앱의 「엑셀 적용」 길(readWorkbook)이 기출DB 에서 뽑은 기출키 · 파이썬이 바이트째 맞댄다 */
    g1: async function () {
      const buf = await (await fetch('/data/master.xlsx')).arrayBuffer();
      const r = readWorkbook(buf);
      const out = { rows: r.rows ? r.rows.length : null, sheets: r.sheets || null, has: 'gkey' in r };
      out.gk = r.gkey ? JSON.stringify(r.gkey) : null;
      if (HAS() && r.gkey) {
        /* 엑셀 길은 keys 만 새로 · 덧자료(comboText·pdfNo)는 지금 기출키 그대로 */
        const ct0 = JSON.stringify(GKEY.comboText), pn0 = JSON.stringify(GKEY.pdfNo), save = GKEY;
        await gkeyPutFromSheet(r.gkey, 'harness.xlsx');
        out.putKeep = JSON.stringify(GKEY.comboText) === ct0 && JSON.stringify(GKEY.pdfNo) === pn0 && GKEY.meta.fromExcel === true;
        GKEY = save; try { await dbPut('gkey', save); } catch (e) { }
      }
      return JSON.stringify(out);
    },
    /* ── G2 조합 선지 — 해마다 글자층 N · comboText M · 못 읽음 · 정답 하나 · 헛잣대(comboText 뺌) · 2026 골든 · 번호 대응 */
    g2: async function () {
      if (!HAS()) return JSON.stringify({ has: false });
      const out = { years: {}, undecided: [], multiAns: [], golden: {}, ans26: '', a2020_24: null, nullM: 0, nullUndecided: [] };
      const years = Object.keys(GKEY.keys);
      const t0 = Date.now();
      for (const y of years) {
        const combos = Object.keys(GKEY.keys[y]).filter(n => GKEY.keys[y][n].combo).map(Number);
        let rec = null; try { rec = await mbExam.index(mbExam.file(y)); } catch (e) { out.years[y] = { err: String(e && e.message || e) }; }
        let N = 0; const Ml = [], miss = [];
        combos.forEach(no => {
          const s = rec ? mbExam.combo(rec, gkPdfNo(y, no)) : null;
          if (s && exvSetsOk(s, y, no)) { N++; return; }
          const ct = ((GKEY.comboText || {})[y] || {})[String(no)];
          const s2 = Array.isArray(ct) && ct.length === 5 ? ct.map(z => [...String(z)].filter(c => EXV_KO.includes(c))) : null;
          if (s2 && exvSetsOk(s2, y, no)) { Ml.push(no); return; }
          miss.push({ no: no, pdf: s ? s.map(a => a.join('')) : null });
        });
        await exvComboLoad(y, combos);
        const src = combos.map(no => (EXV_COMBO[exvKey(no, y)] || {}).src || 'miss');
        out.years[y] = { combo: combos.length, N: N, M: Ml.length, Ml: Ml, miss: miss, pdfSrc: src.filter(s => s === 'pdf').length, textSrc: src.filter(s => s === 'text').length, pages: rec ? rec.pages : null };
        Object.keys(GKEY.keys[y]).map(Number).forEach(no => {
          const c = exvCorrect(y, no), g = GKEY.keys[y][String(no)];
          if (!c.ans.length) out.undecided.push(y + '-' + no + ' ' + (c.why || ''));
          else if (c.ans.length > 1) out.multiAns.push(y + '-' + no + ':' + c.ans.join('·'));
        });
      }
      out.ms = Date.now() - t0;
      const a = []; for (let n = 1; n <= 40; n++) a.push(n + ':' + exvCorrect('2026', n).ans.join('·'));
      out.ans26 = a.join(' ');
      out.a2020_24 = exvCorrect('2020', 24).ans;
      [1, 7, 11, 15, 24, 34, 36].forEach(no => { const c = EXV_COMBO[exvKey(no, '2026')]; out.golden[no] = c && c.sets ? c.sets.map(s => s.join(', ')).join(' | ') : null; });
      /* 헛잣대 — comboText 를 빼면 M 문항이 「못 정함」이 되는가(조합 결과를 비우고 다시 읽는다) */
      const save = GKEY.comboText;
      Object.keys(EXV_COMBO).forEach(k => delete EXV_COMBO[k]);
      GKEY.comboText = {};
      for (const y of years) {
        const combos = Object.keys(GKEY.keys[y]).filter(n => GKEY.keys[y][n].combo).map(Number);
        await exvComboLoad(y, combos);
        combos.forEach(no => { if (!EXV_COMBO[exvKey(no, y)].sets) { out.nullM++; out.nullUndecided.push(y + '-' + no); } });
      }
      GKEY.comboText = save;
      Object.keys(EXV_COMBO).forEach(k => delete EXV_COMBO[k]);
      for (const y of years) await exvComboLoad(y, Object.keys(GKEY.keys[y]).filter(n => GKEY.keys[y][n].combo).map(Number));
      return JSON.stringify(out);
    },
    /* ── G3 전 해 — 앱이 해·문번마다 싣는 지문 표지(examMeta optRaw · 파이썬이 기출DB 표지와 맞댄다) */
    labels: function () {
      const o = {};
      quizData.forEach(q => (q.examMeta || []).forEach(m => { if (!m.no) return; ((o[m.year] = o[m.year] || {})[m.no] = o[m.year][m.no] || []).push(String(m.optRaw || m.opt || '')); }));
      return JSON.stringify(o);
    },
    /* ── G2 번호 대응(2011·2018) — 옮긴 번호의 시험지 덩이가 그 문항 지문과 더 닮았는가(옮기지 않은 번호 = 헛잣대) · 칩 → 시험지 창 머리 */
    g2map: async function () {
      if (!HAS()) return JSON.stringify({ has: false });
      const out = { moves: 0, win: 0, lose: [], keep: { n: 0, ok: 0 } };
      const ko = s => String(s || '').replace(/[^가-힣]/g, '');
      const big = s => { const m = new Map(); for (let i = 0; i + 1 < s.length; i++) { const b = s.slice(i, i + 2); m.set(b, (m.get(b) || 0) + 1); } return m; };
      const dice = (a, b) => { const A = big(a), B = big(b); let x = 0, na = 0, nb = 0; A.forEach(v => na += v); B.forEach(v => nb += v); A.forEach((v, k) => { if (B.has(k)) x += Math.min(v, B.get(k)); }); return na + nb ? 2 * x / (na + nb) : 0; };
      const blk = (rec, n) => { const h = rec.no[n]; if (!h) return ''; const end = h.nx >= 0 ? h.nx : rec.lines.length; return rec.lines.slice(h.i, end).map(l => l.t).join(' '); };
      for (const y of Object.keys(GKEY.pdfNo || {})) {
        const rec = await mbExam.index(mbExam.file(y));
        for (let no = 1; no <= 40; no++) {
          const body = ko(itemsOf(y, no).map(q => q.q).join(' '));
          if (!body) continue;
          const pn = gkPdfNo(y, no);
          const sMap = dice(body, ko(blk(rec, pn))), sRaw = dice(body, ko(blk(rec, no)));
          if (pn !== no) { out.moves++; if (sMap > sRaw) out.win++; else out.lose.push([y, no, pn, +sMap.toFixed(3), +sRaw.toFixed(3)]); }
          else { out.keep.n++; if (sRaw > 0.35) out.keep.ok++; }
        }
      }
      /* 칩 → 시험지 창 — 2018 1번 지문(시험지 2번) */
      const q = itemsOf('2018', 1)[0];
      if (q) {
        const mi = q.examMeta.findIndex(m => m.year === '2018');
        document.querySelectorAll('.oxwin').forEach(w => w.remove());
        mbExamOpen(q.id, mi);
        await until(() => mbExam.last() && mbExam.last().em && mbExam.last().em.year === '2018', 20000);
        const w = Q('[id^="oxwin-exampg-"]');
        const rec = await mbExam.index(mbExam.file('2018'));
        const L = mbExam.last();
        out.chip = { head: w ? T(Q('.oxwin-head', w)).slice(0, 80) : null, p: L && L.p, want: rec.no[gkPdfNo('2018', 1)] ? rec.no[gkPdfNo('2018', 1)].p : null, pn: gkPdfNo('2018', 1) };
        document.querySelectorAll('.oxwin').forEach(w2 => w2.remove());
      }
      return JSON.stringify(out);
    },
    /* ── 기출뷰 열기(시험 준비 · 누름 없는 진입 — 진입 단추는 G8 에서 진짜로 누른다) */
    open: async function (y) {
      document.querySelectorAll('.oxwin').forEach(w => w.remove());
      try { goHome(); } catch (e) { }
      startQuiz('변리사 기출', chapOf(y));
      await until(() => QA('#quiz-container .question-box').length > 0, 20000);
      if (HAS()) await until(() => !QA('#quiz-container .exv-wait').length, 60000);
      await wait(150);
      return JSON.stringify({ label: currentChapterLabel, on: HAS() ? exvOn() : false, boxes: QA('#quiz-container .question-box').length });
    },
    /* ── G3 시험지 꼴 — 그 쪽 문항 5 · 발문 줄 5 · 보기 상자 = 조합형 수 · 빠진 선지 자리 · 채점 전 O·X 줄 숨김 · 칩 줄 보임 */
    g3: function (y) {
      const qs = QA('#quiz-container .exv-q');
      const combo = HAS() ? qs.filter(q => exvIsCombo(y, +q.dataset.exq.split(':')[1])).length : null;
      const post = QA('#quiz-container .exv-post');
      const oxRows = QA('#quiz-container [id^="ox-O-"]').map(l => l.parentElement);
      const chips = QA('#quiz-container button[data-exam]');
      const boxes = QA('#quiz-container .question-box');
      const chipRowVis = boxes.filter(b => { const c = Q('button[data-exam]', b); return c && vis(c); }).length;
      return JSON.stringify({
        y: y, q: qs.length, heads: QA('#quiz-container .exv-head').length, stems: QA('#quiz-container .exv-stem').filter(s => T(s).length > 3).length,
        bogi: QA('#quiz-container .exv-bogi').length, combo: combo, miss: QA('#quiz-container .exv-miss').length,
        sel: QA('#quiz-container .exv-sel').map(s => QA('.exv-opt', s).length),
        oxRows: oxRows.length, oxVis: oxRows.filter(vis).length, oxDisp: [...new Set(oxRows.map(dispOf))],
        postN: post.length, postVis: post.filter(vis).length,
        boxes: boxes.length, chipRowVis: chipRowVis, chips: chips.length,
        nos: qs.map(q => +q.dataset.exq.split(':')[1]),
        comboChipTxt: y === Y26 ? QA('#quiz-container .exv-bogi button[data-exam]').map(T).slice(0, 3) : null,
        q36: null
      });
    },
    /* 2026 36번(8쪽 = 36~40) — 보기 상자 + 「① ㄴ … ⑤ ㄱ, ㄴ, ㄷ」 · 빈자리 없음 */
    q36: function () {
      const q = Q('#quiz-container .exv-q[data-exq="2026:36"]');
      if (!q) return JSON.stringify(null);
      return JSON.stringify({ bogi: QA('.exv-bogi', q).length, opts: QA('.exv-opt', q).map(T), miss: QA('.exv-miss', q).length, labs: QA('.exv-bogi .question-box', q).length });
    },
    /* ── G4 상태 */
    st4: function () {
      const y = Y26, P = LSJ('ox_exam_pick'), R = LSJ('ox_exam_rounds'), TM = LSJ('ox_exam_timer');
      const res = {};
      QA('#quiz-container .exv-q').forEach(q => { res[q.dataset.exq] = T(Q('.exv-res', q)); });
      const sel = {};
      QA('#quiz-container .exv-q').forEach(q => { sel[q.dataset.exq] = QA('[data-exk]', q).filter(b => b.classList.contains('sel') || b.classList.contains('bad')).map(b => b.classList.contains('bad') ? b.dataset.exn + 'x' : +b.dataset.exn); });
      const ok = {};
      QA('#quiz-container .exv-q').forEach(q => { ok[q.dataset.exq] = QA('[data-exk]', q).filter(b => b.classList.contains('ok')).map(b => +b.dataset.exn); });
      const ab = document.getElementById('action-btn');
      return JSON.stringify({ picks: Object.keys(P).filter(k => k.indexOf(y + ':') === 0).reduce((o, k) => (o[k] = P[k], o), {}), res: res, sel: sel, ok: ok,
        rounds: (R[y] || []).length, lastRound: (R[y] || []).slice(-1)[0] || null, timer: TM[y] || null, pill: ab ? { txt: T(ab), disp: dispOf(ab), vis: vis(ab), onclick: ab.getAttribute('onclick') } : null,
        page: typeof currentPageIndex !== 'undefined' ? currentPageIndex : null, toast: toastTxt(), mark: T(document.getElementById('mark-count')) + '/' + T(document.getElementById('mark-total')),
        need: QA('#quiz-container .exv-q.exv-need').map(q => q.dataset.exq), omr: T(document.getElementById('exv-omr-count')) });
    },
    /* 1~40 가운데 from~to 를 고른 답으로(전체 채점 준비 · 누름 게이트는 1~5 와 알약) */
    pickFill: function (from, to) {
      if (!HAS()) return '0';
      const P = LSJ('ox_exam_pick');
      for (let n = from; n <= to; n++) { const c = exvCorrect(Y26, n); P[Y26 + ':' + n] = n % 7 === 0 ? ((c.ans[0] % 5) + 1) : c.ans[0]; }
      LSP('ox_exam_pick', P);
      exvPaint();
      return JSON.stringify(Object.keys(P).length);
    },
    omrRow: function (no, k) { return JSON.stringify(ptOf(Q('#exv-omr-rows .exv-omr[data-no="' + no + '"] button[data-n="' + k + '"]'))); },
    omrState: function () {
      const rows = QA('#exv-omr-rows .exv-omr');
      return JSON.stringify({ rows: rows.length, cur: rows.filter(r => r.classList.contains('cur')).map(r => +r.dataset.no), count: T(document.getElementById('exv-omr-count')),
        on: rows.map(r => QA('button', r).filter(b => b.classList.contains('on') || b.classList.contains('bad')).map(b => +b.dataset.n)).map((a, i) => a.length ? (i + 1) + ':' + a.join('') : '').filter(Boolean),
        title: T(Q('#oxwin-omr .oxwin-head')).slice(0, 60), btn5: rows[0] ? QA('button', rows[0]).length : 0 });
    },
    /* ── G5 즉시 기록 */
    st5: function (U) {
      const QH = LSJ('ox_q_history'), QL = LSJ('ox_q_last'), TG = LSJ('ox_q_tags'), P = LSJ('ox_in_progress');
      const wq = typeof weakQueueItems === 'function' ? weakQueueItems().map(q => q.id) : [];
      const k = ck(Y26);
      return JSON.stringify({ qh: [U.a, U.b, U.c].map(u => (u in QH) ? QH[u] : null), ql: [U.a, U.b, U.c].map(u => QL[u] || 0), tagC: !!(TG[U.c] && TG[U.c].confuse),
        weak: [U.a, U.b, U.c].map(u => wq.includes(u)), sm: [U.a, U.b, U.c].map(u => (typeof currentSessionMarks !== 'undefined' && u in currentSessionMarks) ? currentSessionMarks[u] : null),
        prog: P[k] ? [U.a, U.b, U.c].map(u => (P[k].marks || {})[u] ?? null) : null,
        badge: [U.a, U.b].map(u => T(Q('#exp-' + u + ' .result-badge'))), expVis: [U.a, U.b].map(u => vis(document.getElementById('exp-' + u))) });
    },
    /* ── G6 기록 칸 */
    st6: function (uid) {
      const QH = LSJ('ox_q_history'), G = LSJ('ox_rec_gone');
      const wq = typeof weakQueueItems === 'function' ? weakQueueItems().map(q => q.id) : [];
      const strip = document.getElementById('rec-strip-' + uid);
      const info = strip ? Q('.rec-info', strip) : null;
      const jn = QA('[data-jnrec="' + uid + '"]');
      const jinfo = jn[0] ? Q('.rec-info', jn[0]) : null;
      return JSON.stringify({ qh: (uid in QH) ? QH[uid] : null, weak: wq.includes(uid), gone: Object.keys(G).filter(k => k.indexOf(uid + '|') === 0), goneAll: Object.keys(G).length,
        cells: strip ? QA('.rec-cell', strip).map(b => b.dataset.kind + ':' + T(b)) : null, stripVis: vis(strip),
        info: info ? { vis: vis(info), txt: T(info), del: !!Q('.rec-del', info), sure: !!Q('.rec-del.sure', info), fs: getComputedStyle(info).fontSize } : null,
        strip: strip ? T(strip) : null,
        jn: jn.map(x => QA('.rec-cell', x).map(b => b.dataset.kind + ':' + T(b)).join(',')), jinfo: jinfo ? { vis: vis(jinfo), txt: T(jinfo), left: (() => { const c = Q('.rec-cell', jn[0]); return c ? jinfo.getBoundingClientRect().right <= c.getBoundingClientRect().left + 1 : null; })() } : null,
        radios: QA('input[name="answer_' + uid + '"]').map(r => (r.disabled ? 'd' : 'e') + (r.checked ? 'c' : '')) });
    },
    /* 되살림 흉내 — 원격(하네스가 대답) 기록에 지운 칸을 되살려 넣고 도장을 더 새것으로 → syncRecords(앱 길) → 쓸기 */
    revive: async function (uid, key, n, keepTomb) {
      const G0 = LSJ('ox_rec_gone');
      if (!keepTomb) { LSP('ox_rec_gone', {}); try { stampAll(); } catch (e) { } }
      const pay = recPayload(null);
      const H = pay.data.ox_chap_history;
      if (!H[key] || !H[key][n - 1]) return JSON.stringify({ err: 'no round' });
      H[key][n - 1].marks[uid] = false;
      pay.u = pay.u || {};
      pay.u[ckey('ox_chap_history', key)] = Date.now() + 5000;
      window.__REMOTE_REC = pay; window.__PUTS = [];
      await syncRecords(true);
      window.__REMOTE_REC = null;
      const L = LSJ('ox_chap_history');
      const back = !!(L[key] && L[key][n - 1] && L[key][n - 1].marks && (uid in L[key][n - 1].marks));
      let putHas = null;
      try { const last = window.__PUTS.slice(-1)[0]; if (last) { const b = JSON.parse(last); const txt = decodeURIComponent(escape(atob(b.content))); const j = JSON.parse(txt); putHas = uid in (((j.data.ox_chap_history[key] || [])[n - 1] || {}).marks || {}); } } catch (e) { putHas = 'err ' + e.message; }
      const QH = LSJ('ox_q_history');
      const out = { back: back, putHas: putHas, puts: window.__PUTS.length, qh: (uid in QH) ? QH[uid] : null };
      if (!keepTomb) { LSP('ox_rec_gone', G0); try { stampAll(); } catch (e) { } }
      return JSON.stringify(out);
    },
    /* 지운 뒤 다시 푼 답 — 같은 날 · ox_q_last > 묘비 시각이면 쓸기가 안 먹는다(묘비만 보는 셈이면 먹었을 칸 수를 같이) */
    reanswerSweep: async function (uid) {
      if (!HAS()) return JSON.stringify({ has: false });
      const G = LSJ('ox_rec_gone'), P = LSJ('ox_in_progress'), k = ck(Y26);
      const naive = Object.keys((P[k] || {}).marks || {}).filter(u => u === uid && G[recTombId(u, k, P[k].date)]).length;
      window.__REMOTE_REC = recPayload(null); window.__PUTS = [];
      await syncRecords(true);
      window.__REMOTE_REC = null;
      const P2 = LSJ('ox_in_progress');
      return JSON.stringify({ naive: naive, kept: !!(((P2[k] || {}).marks || {})[uid] !== undefined), sm: (uid in currentSessionMarks) ? currentSessionMarks[uid] : null });
    },
    /* ── G7 시계 */
    st7: function () {
      const box = document.getElementById('exv-timer'), v = box ? Q('.exv-t-v', box) : null, go = box ? Q('.exv-t-go', box) : null, rs = document.getElementById('exv-t-reset');
      const u = v ? Q('.exv-u', v) : null;
      return JSON.stringify({ has: !!box, v: v ? T(v) : null, over: v ? v.classList.contains('over') : null, color: v ? getComputedStyle(v).color : null,
        go: go ? T(go) : null, goVis: vis(go), goMark: go ? (go.dataset.hz || null) : null, reset: rs ? { vis: vis(rs), sure: rs.classList.contains('sure') } : null,
        sub: T(document.getElementById('exv-over')), ufs: u ? [getComputedStyle(v).fontSize, getComputedStyle(u).fontSize, getComputedStyle(u).opacity] : null,
        store: LSJ('ox_exam_timer')[Y26] || null });
    },
    markGo: function () { const g = Q('#exv-timer .exv-t-go'); if (g) g.dataset.hz = '1'; return JSON.stringify(!!g); },
    timerSet: function (sec) { const all = LSJ('ox_exam_timer'); all[Y26] = { acc: sec * 1000, since: 0 }; LSP('ox_exam_timer', all); if (typeof exvTimerPaint === 'function') exvTimerPaint(); return '1'; },
    /* ── G8 첫 화면 */
    g8: function () {
      const rows = QA('[data-trrow^="변리사 기출|||"]');
      const out = { rows: rows.length, cnt: [], r26: null };
      rows.forEach(r => {
        const lab = r.getAttribute('data-trrow').split('|||')[1];
        const c = Q('[data-exvcount]', r);
        const n = quizData.filter(q => (q.examYears || []).includes(lab.slice(0, 4))).length;
        out.cnt.push({ y: lab.slice(0, 4), txt: c ? T(c) : T(r).slice(0, 40), n: n });
      });
      const r26 = rows.find(r => r.getAttribute('data-trrow').indexOf('2026') >= 0);
      if (r26) {
        const box = QA('.exv-dround', r26);
        const d0 = box[0];
        const lines = d0 ? QA('.exv-dlines > span', d0).map(T) : [];
        const over = d0 ? Q('.exv-dover', d0) : null;
        const pr = Q('.exv-dprog', r26);
        const oldProg = QA('span', r26).filter(s => /진행중/.test(T(s)) && !s.classList.contains('exv-dprog') && !s.closest('.exv-dprog')).length;
        const btns = QA('button', r26).map(T).filter(t => /회독$|이어서/.test(t));
        out.r26 = { boxes: box.length, lines: lines, overTxt: over ? T(over) : null, overColor: over ? getComputedStyle(over).color : null,
          prog: pr ? T(pr) : null, progHasClock: pr ? /⏱/.test(T(pr)) : null, oldProg: oldProg, start: btns, oldChips: QA('button', r26).filter(b => /^\d+회독 /.test(T(b)) && !b.classList.contains('exv-dround')).length };
      }
      return JSON.stringify(out);
    },
    home: async function () { document.querySelectorAll('.oxwin').forEach(w => w.remove()); try { goHome(); } catch (e) { } try { renderDashboard(); } catch (e) { } await wait(200); return '1'; },
    progSet: function (n, sec) {
      const P = LSJ('ox_exam_pick'); Object.keys(P).forEach(k => { if (k.indexOf(Y26 + ':') === 0) delete P[k]; });
      for (let i = 1; i <= n; i++) P[Y26 + ':' + i] = 1;
      LSP('ox_exam_pick', P);
      const all = LSJ('ox_exam_timer'); all[Y26] = { acc: sec * 1000, since: 0 }; LSP('ox_exam_timer', all);
      /* 지문 진행중도 하나 — 옛 판이면 주황 「▶ N회독 진행중」 칩이 선다(새 판은 안 그린다) */
      const PR = LSJ('ox_in_progress'); PR[ck(Y26)] = { pageIndex: 0, score: 0, marks: {}, picks: { x: 'O' }, total: 188, date: '2026. 9. 26.' }; LSP('ox_in_progress', PR);
      renderDashboard();
      return '1';
    },
    progClear: function () {
      const P = LSJ('ox_exam_pick'); Object.keys(P).forEach(k => { if (k.indexOf(Y26 + ':') === 0) delete P[k]; }); LSP('ox_exam_pick', P);
      const all = LSJ('ox_exam_timer'); delete all[Y26]; LSP('ox_exam_timer', all);
      const PR = LSJ('ox_in_progress'); delete PR[ck(Y26)]; LSP('ox_in_progress', PR);
      renderDashboard(); return '1';
    },
    /* ── G9 정리 창 */
    jnBtn: function (subject, needle) {
      const bs = QA('button[data-jn]').filter(b => { const oc = b.getAttribute('onclick') || ''; return oc.indexOf("openJeongni('" + subject + "'") >= 0 && b.getAttribute('data-jn').indexOf(needle) >= 0; });
      return JSON.stringify(Object.assign(ptOf(bs[0]), { n: bs.length, jn: bs[0] ? bs[0].getAttribute('data-jn').slice(0, 80) : null }));
    },
    g9: function (y) {
      const w = QA('.oxwin').filter(x => x.id.indexOf('oxwin-jn-') === 0).slice(-1)[0];
      if (!w) return JSON.stringify({ win: false });
      const rows = QA('[data-jnrow]', w);
      const withMeta = rows.filter(r => { const q = quizData.find(x => x.id === r.getAttribute('data-jnrow')); return q && (q.examMeta || []).length; }).length;
      const withChip = rows.filter(r => Q('.jn-exam', r)).length;
      const out = { win: true, id: w.id, title: T(Q('.oxwin-head', w)).slice(0, 90), rows: rows.length, withMeta: withMeta, withChip: withChip,
        jx: QA('.jx-no', w).length, bogi: QA('.exv-bogi', w).length, res: QA('.exv-res, .exv-r-ok, .exv-r-bad', w).length + (/O 맞음|X 틀림/.test(T(w)) ? 1 : 0),
        cellsPer: [...new Set(QA('.jx-no', w).map(n => QA('.jx-cell', n).length))],
        chipSample: QA('.jn-exam', w).slice(0, 4).map(T), jxStyle: null, order1: null };
      const j1 = Q('.jx-no[data-jxno="1"]', w);
      if (j1) {
        const cs = getComputedStyle(j1);
        out.jxStyle = [cs.fontSize, cs.fontWeight, cs.borderTopWidth, cs.borderTopColor, cs.backgroundColor];
        const lab = [];
        let e = j1.nextElementSibling;
        while (e && !e.classList.contains('jx-no')) { const q = quizData.find(x => x.id === e.getAttribute('data-jnrow')); if (q) lab.push(rawOf(q, y)); e = e.nextElementSibling; }
        out.order1 = lab.join('');
        out.j1txt = T(j1).slice(0, 40);
      }
      return JSON.stringify(out);
    },
    jxInfo: function () { const w = QA('.oxwin').filter(x => x.id.indexOf('oxwin-jn-') === 0).slice(-1)[0]; const i = w ? Q('.jx-no[data-jxno="1"] .jx-info', w) : null; return JSON.stringify(i ? { vis: vis(i), txt: T(i) } : null); },
    /* ── G10 무변 — 단원 풀기 첫 쪽 글자 · 일반 OMR 창 */
    unitLabels: function () {
      const pick = (subj, f) => { const r = QA('[data-trrow^="' + subj + '|||"]').map(x => x.getAttribute('data-trrow').split('|||')[1]); return f ? r.find(f) : r[0]; };
      return JSON.stringify([['민법총칙', pick('민법총칙', l => /1\.2/.test(l)) || pick('민법총칙')], ['물권법', pick('물권법')], ['채권각론', pick('채권각론')]]);
    },
    unitText: async function (subj, lab) {
      document.querySelectorAll('.oxwin').forEach(w => w.remove());
      try { goHome(); } catch (e) { }
      startQuiz(subj, lab);
      await until(() => QA('#quiz-container .question-box').length > 0, 20000);
      /* 📍 좌표 단추는 문서 전체 MutationObserver 가 변화가 60ms 멎은 뒤에 얹는다 — 다 얹힐 때까지 기다린 뒤 읽는다(두 판 같은 조건) */
      const pinsIn = await until(() => QA('#quiz-container [id^="tag-confuse-"]').every(b => b.dataset.coordPin), 10000);
      await wait(250);
      const c = document.getElementById('quiz-container');
      /* ★ _task_ox_linkwin(9/27) — 카드 안 memo-panel(숨은 ID 칸·안내 글·저장하기)은 걷었다 → 두 판 다 그 칸을 빼고 잰다(나머지 글 무변을 본다) */
      const c2 = c.cloneNode(true); c2.querySelectorAll('[id^="memo-panel-"]').forEach(x => x.remove());
      const txt = T(c2);
      const recBtn = QA('#quiz-container .rec-cell').length;
      openOmrPad();
      await wait(200);
      const omr = document.getElementById('oxwin-omr');
      const omrTxt = omr ? T(omr) : null;
      const omrHtml = omr ? omr.innerHTML.replace(/z-index:\d+/g, '').length : 0;
      if (omr) oxWinClose('omr');
      const ab = document.getElementById('action-btn');
      return JSON.stringify({ pinsIn: pinsIn, n: QA('#quiz-container .question-box').length, txt: txt, len: txt.length, recBtn: recBtn, omr: omrTxt, omrLen: omrHtml, pill: ab ? T(ab) + '|' + ab.getAttribute('onclick') : null });
    }
  };
})();
