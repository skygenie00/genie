/* _task_ox_prev_case_ink_fix17 §E 하네스 — 브라우저 안 시험(단계마다 window.__HZT.<이름>() 을 CDP 가 부른다 · 결과는 JSON 글자) */
window.onload = null;   /* 앱 초기화(망·동기화)를 끈다 — 시험이 저장소·문항을 직접 싣는다 */
(function () {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const H = window.__HZ = window.__HZ || {};
  const LS = k => localStorage.getItem(k);
  const vis = id => { const e = document.getElementById(id); return !!e && !e.classList.contains('hide'); };
  const rect = el => { const r = el.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)]; };
  /* 「진짜 누름으로 눌린다」 — 그 자리를 짚었을 때 그 단추가 맨 위인가(9/21 pointer-events 잣대) */
  const hitPrev = () => {
    const b = document.querySelector('#exam-prev-bar button');
    if (!b) return 'no-btn';
    const r = b.getBoundingClientRect();
    if (r.width <= 0 || r.height <= 0) return 'no-size';
    const el = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    if (!el) return 'none';
    return (el === b || b.contains(el)) ? 'btn' : ('other:' + (el.id || el.className || el.tagName));
  };
  const answerAll = () => {                       /* 이 쪽 지문 전부 O 로 고른다(라디오 = gradeCurrentPage 가 보는 것) */
    let n = 0;
    document.querySelectorAll('#quiz-container input[type="radio"][value="O"]').forEach(r => {
      if (!document.querySelector('input[name="' + r.name + '"]:checked')) { r.checked = true; n++; }
    });
    return n;
  };
  const killGrade = () => { try { closeGradeModal(); } catch (e) { } const w = document.getElementById('oxwin-grade'); if (w) w.remove(); };
  const boxInfo = () => [...document.querySelectorAll('#qcards .case-box')].map(b => ({
    key: b.dataset.ckey || null,
    uids: [...b.querySelectorAll('.question-box')].map(x => String(x.id || '').replace('q-box-', '')),
    ink: !!b.querySelector('svg.qink'),
    inkIn: b.querySelector('svg.qink') ? (b.querySelector('svg.qink').parentElement.className || '').split(' ')[0] : null
  }));
  /* 옛 판(HEAD)에는 `.case-box` 가 없다 — 지금 화면의 [종합사례 원문] 상자를 글자로 찾는다(헛잣대가 재는 자리) */
  const caseDivs = () => [...document.querySelectorAll('#qcards div')].filter(d => /\[종합사례 원문\]/.test(d.textContent || '') && d.querySelector('.question-box'));
  const PEN = (sv, t, x, y, id) => {
    const e = new PointerEvent(t, { bubbles: true, cancelable: true, composed: true, pointerId: id || 11, pointerType: 'pen', isPrimary: true, clientX: x, clientY: y });
    sv.dispatchEvent(e); return e;
  };

  /* 3쪽짜리(41~60문항) 단원 · 그 안의 [종합사례] 묶음(같은 번호·단원 · 한 쪽 안에 연달아 셋 이상)을 고른다 */
  function pickUnits() {
    const U = {};
    quizData.forEach(x => {
      const lab = x.subChapter ? (x.chapter + ' > ' + x.subChapter) : x.chapter;
      const k = x.subject + '||' + lab;
      (U[k] = U[k] || []).push(x);
    });
    const three = Object.keys(U).filter(k => U[k].length >= 41 && U[k].length <= 60).sort();
    let caseUnit = null;
    for (const k of three) {
      const rows = U[k];
      for (let p = 0; p * 20 < rows.length; p++) {
        const page = rows.slice(p * 20, p * 20 + 20);
        let i = 0;
        while (i < page.length) {
          const c = String(page[i].caseText || '');
          if (!c.trim()) { i++; continue; }
          let j = i; while (j < page.length && String(page[j].caseText || '') === c) j++;
          const run = page.slice(i, j);
          const same = run.every(x => Number(x.probNum) === Number(run[0].probNum)
            && x.subject === run[0].subject && x.chapter === run[0].chapter && x.subChapter === run[0].subChapter);
          /* 같은 글자를 이 단원 밖에서도 쓰면 이웃 먹이기 수가 흔들린다 — 이 단원 안에서만 쓰는 묶음을 고른다 */
          const onlyHere = quizData.filter(x => String(x.caseText || '') === c).length === run.length;
          if (run.length >= 3 && same && onlyHere && !caseUnit) { caseUnit = { k: k, page: p, uids: run.map(x => x.id), c: c }; }
          i = j;
        }
        if (caseUnit) break;
      }
      if (caseUnit) break;
    }
    const other = three.find(k => !caseUnit || k !== caseUnit.k) || three[0];
    return { three: three.length, prevUnit: other, caseUnit: caseUnit, n: other ? U[other].length : 0 };
  }
  const startU = k => { const i = k.indexOf('||'); startQuiz(k.slice(0, i), k.slice(i + 2)); };

  window.__HZT = {
    /* ── 준비: 동기화 기록 파일의 저장소 전부 · 문항 5,548 ── */
    setup: async function () {
      const R = {};
      const rec = await (await fetch('/rec.json')).json();
      const D = rec.data || rec;
      localStorage.clear();
      const BASE = { 'ox_uid_migrated': '1', 'ox_gg_okreset': '1', 'ox_auto_important_v2': '1', 'tt.cfg': JSON.stringify({ person: '하네스', token: '' }) };
      for (const k in BASE) localStorage.setItem(k, BASE[k]);
      for (const k in D) localStorage.setItem(k, typeof D[k] === 'string' ? D[k] : JSON.stringify(D[k]));
      try { useIdxDrop(); } catch (e) { }
      const M = await (await fetch('/master.json')).json();
      quizData.length = 0; buildQuizData(M.rows).forEach(q => quizData.push(q));
      R.q = quizData.length;
      R.fix0 = Object.keys(JSON.parse(LS('ox_q_fix') || '{}')).length;
      R.syncKeys = (typeof SYNC_KEYS !== 'undefined') ? SYNC_KEYS.slice().sort() : null;
      H.pick = pickUnits();
      R.pick = { three: H.pick.three, prevUnit: H.pick.prevUnit, n: H.pick.n, caseUnit: H.pick.caseUnit && { k: H.pick.caseUnit.k, page: H.pick.caseUnit.page, uids: H.pick.caseUnit.uids, clen: H.pick.caseUnit.c.length } };
      /* 필기 통 열쇠 — 시험 앞뒤로 「새 키 0」을 재는 잣대(§E-6) */
      try { H.keys0 = (await dbKeys()).filter(k => typeof k === 'string').sort(); } catch (e) { H.keys0 = []; }
      R.keys0 = H.keys0.length;
      R.ink0 = H.keys0.filter(k => k.indexOf('ink:q:') === 0).length;
      return JSON.stringify(R);
    },

    /* ══════════ §E-1 일반 모드 — 1쪽 채점 → 2쪽 채점 → 2쪽에 「◀ 이전」 → 1쪽(채점된 모습) → 없음 ══════════ */
    a_prev_normal: async function () {
      const R = { unit: H.pick.prevUnit };
      startU(H.pick.prevUnit); await wait(200);
      R.total = currentFilteredData.length;
      R.pages = Math.ceil(currentFilteredData.length / PAGE_SIZE);
      R.p0_prev_before = vis('exam-prev-bar');                 /* 첫 쪽 — 채점 전에도 없다 */
      R.marked0 = answerAll();
      gradeCurrentPage(); await wait(200); killGrade(); await wait(150);
      R.p0graded = Object.keys(currentSessionMarks).length;
      goNextPage(); await wait(400);
      R.idx1 = currentPageIndex;
      R.p1_prev_ungraded = vis('exam-prev-bar');               /* 채점 전 2쪽 — 옛 판도 보인다 */
      R.marked1 = answerAll();
      gradeCurrentPage(); await wait(200); killGrade(); await wait(150);
      renderQuizPage(); await wait(500);                       /* ★ 채점된 모습으로 다시 그림 = 결함이 나던 자리 */
      R.idx1b = currentPageIndex;
      R.allGraded1 = currentFilteredData.slice(PAGE_SIZE, 2 * PAGE_SIZE).every(it => String(it.id) in currentSessionMarks);
      R.p1_prev_graded = vis('exam-prev-bar');                 /* ← §E-1 의 알맹이 */
      R.p1_hit = hitPrev();
      R.ctrl1 = vis('controls-container');                     /* 오른쪽 알약 규칙은 무접촉 — 옛 판과 같아야 한다 */
      if (R.p1_prev_graded) {
        document.querySelector('#exam-prev-bar button').click(); await wait(600);
        R.idx0 = currentPageIndex;
        R.p0_prev_after = vis('exam-prev-bar');                /* 첫 쪽 = 없음 */
        R.p0_ox = document.querySelectorAll('#qcards .question-box [data-ox-mark], #qcards .ox-graded').length;
        R.p0_checked = document.querySelectorAll('#quiz-container input[type="radio"]:checked').length;
        R.p0_cards = document.querySelectorAll('#qcards .question-box').length;
      }
      return JSON.stringify(R);
    },

    /* §E-1 이어풀기 복귀 — 목록으로 나갔다 다시 들어와도 2쪽에 「◀ 이전」 */
    a_prev_resume: async function () {
      const R = {};
      currentPageIndex = 1; renderQuizPage(); await wait(500);   /* 두 판을 같은 쪽에 세운다 — 앞 단계에서 NEW 만 「◀ 이전」을 눌러 0쪽이었다 */
      R.leaveIdx = currentPageIndex;
      goHome(); await wait(300);
      R.saved = Object.keys(JSON.parse(LS('ox_in_progress') || '{}')).length;
      startU(H.pick.prevUnit); await wait(700);
      R.idx = currentPageIndex;
      R.marks = Object.keys(currentSessionMarks).length;
      R.allGraded = currentFilteredData.slice(currentPageIndex * PAGE_SIZE, (currentPageIndex + 1) * PAGE_SIZE).every(it => String(it.id) in currentSessionMarks);
      R.prev = vis('exam-prev-bar');
      R.hit = hitPrev();
      R.lastGrade = !!lastGradeResults;
      R.ctrl = vis('controls-container');
      goHome(); await wait(200);
      return JSON.stringify(R);
    },

    /* §E-1 기출 모드 — 2쪽에서 전체 채점 → 그 자리에서 「◀ 이전」 */
    a_prev_exam: async function () {
      const R = {};
      const ys = {}; quizData.forEach(x => { if (x.examYear) (ys[x.examYear] = ys[x.examYear] || new Set()).add(x.examNo); });
      const y = Object.keys(ys).filter(k => ys[k].size >= 15).sort()[0];
      R.year = y; if (!y) return JSON.stringify(R);
      startQuiz('변리사 기출', y + '년 제1회'); await wait(700);
      R.total = currentFilteredData.length;
      R.nos = [...new Set(currentFilteredData.map(x => x.examNo))].length;
      goNextPageExam(); await wait(500);
      R.idx = currentPageIndex;
      R.prev_before = vis('exam-prev-bar');
      currentFilteredData.forEach(it => { resumePicks[String(it.id)] = 'O'; });
      gradeAllExam(); await wait(900);                          /* 안에서 renderQuizPage 를 부른다 */
      R.idxAfter = currentPageIndex;
      R.allGraded = currentFilteredData.every(it => String(it.id) in currentSessionMarks);
      R.prev_after = vis('exam-prev-bar');
      R.hit = hitPrev();
      const w = document.getElementById('oxwin-grade'); if (w) w.remove();
      R.alerts = (window.__ALERTS || []).length;
      return JSON.stringify(R);
    },

    /* ══════════ 헛잣대 — 옛 판에서 2(원문 칸)·3(상자 덮개)이 없다 ══════════ */
    probe23: async function () {
      const R = {};
      const cu = H.pick.caseUnit;
      if (!cu) return JSON.stringify(R);
      startU(cu.k); currentPageIndex = cu.page; renderQuizPage(); await wait(900);
      R.caseDivs = caseDivs().length;
      R.boxes = boxInfo().length;                               /* 옛 판 = 0(`.case-box` 없음) */
      R.caseInk = document.querySelectorAll('#qcards svg.qink[id^="ink-case:"]').length;
      const id = cu.uids[1];
      try { openFixPanel(id); } catch (e) { R.exc = String(e); }
      await wait(150);
      R.panel = !!document.getElementById('fixpanel-' + id);
      R.fields = [...document.querySelectorAll('#fixpanel-' + id + ' textarea')].map(t => t.id.replace('-' + id, ''));
      R.hasC = !!document.getElementById('fixc-' + id);
      R.hasPull = /원문 가져오기/.test((document.getElementById('fixpanel-' + id) || {}).textContent || '');
      try { closeFixPanel(id); } catch (e) { }
      return JSON.stringify(R);
    },

    /* ══════════ §E-2 ① 상자 밖 지문 → 「가져오기」 → 저장 → 상자 안으로 ══════════ */
    b_pull: async function () {
      const R = {}; const cu = H.pick.caseUnit;
      H.fixSnap = LS('ox_q_fix');
      const items = cu.uids.map(u => quizData.find(x => x.id === u));
      H.items = items; H.c0 = cu.c;
      items.forEach(x => { delete x.origC; });
      items[0].caseText = '';                                   /* 흉내 — 첫 지문의 `사례` 칸이 비었다(사용자 캡처 Q4167) */
      startU(cu.k); currentPageIndex = cu.page; renderQuizPage(); await wait(900);
      const B0 = boxInfo();
      R.n = cu.uids.length;
      R.orphan = items[0].id;
      R.boxes0 = B0.length;
      R.box0 = B0.find(b => b.uids.indexOf(items[1].id) >= 0) || null;
      R.orphanOutside = !document.querySelector('#qcards .case-box #q-box-' + items[0].id) && !!document.getElementById('q-box-' + items[0].id);
      openFixPanel(items[0].id); await wait(150);
      const ta = document.getElementById('fixc-' + items[0].id);
      R.hasC = !!ta; R.cVal0 = ta ? ta.value : null;
      const pull = [...document.querySelectorAll('#fixpanel-' + items[0].id + ' button')].find(b => /원문 가져오기/.test(b.textContent));
      R.pullLabel = pull ? pull.textContent.trim() : null;
      R.wantLabel = '같은 ' + (items[0].displayNo ?? items[0].probNum) + '번 원문 가져오기';
      if (!pull) return JSON.stringify(R);
      pull.click(); await wait(100);
      R.pulledSame = document.getElementById('fixc-' + items[0].id).value === cu.c;   /* 한 글자도 안 바꾸고 */
      saveFix(items[0].id); await wait(900);
      const F = JSON.parse(LS('ox_q_fix') || '{}');
      R.rec = F[items[0].id] ? { c: F[items[0].id].c === cu.c, c0: F[items[0].id].c0, hasA: !!F[items[0].id].a, hasQ: typeof F[items[0].id].q, hasExp: typeof F[items[0].id].exp, done: F[items[0].id].done } : null;
      R.peersStamped = cu.uids.slice(1).filter(u => F[u]).length;   /* 빈 칸 채우기는 이웃에 안 번진다 */
      const B1 = boxInfo();
      R.boxes1 = B1.length;
      R.box1 = B1.find(b => b.uids.indexOf(items[1].id) >= 0) || null;
      R.orphanInside = !!document.querySelector('#qcards .case-box #q-box-' + items[0].id);
      R.fixedChip = /정정됨/.test((document.getElementById('q-box-' + items[0].id) || {}).textContent || '');
      return JSON.stringify(R);
    },

    /* ══════════ §E-2 ② 원문 글자를 고치면 같은 상자 전부에 · 상자는 여전히 하나 ══════════ */
    b_edit: async function () {
      const R = {}; const cu = H.pick.caseUnit; const items = H.items;
      const target = items[1].id;
      openFixPanel(target); await wait(150);
      const ta = document.getElementById('fixc-' + target);
      R.cVal = ta && ta.value === cu.c;
      const NEWC = cu.c + '【HZ 원문 고침】';
      ta.value = NEWC; H.newc = NEWC;
      saveFix(target); await wait(900);
      const F = JSON.parse(LS('ox_q_fix') || '{}');
      R.stamped = cu.uids.filter(u => F[u] && F[u].c === NEWC).length;      /* 셋 다 */
      R.c0s = cu.uids.map(u => F[u] ? (F[u].c0 === cu.c ? 'orig' : (F[u].c0 === '' ? 'empty' : 'other')) : 'none');
      R.status = (document.getElementById('sync-status') || {}).textContent || null;
      const B = boxInfo();
      R.boxes = B.length;
      R.box = B.find(b => b.uids.indexOf(target) >= 0) || null;
      R.n = cu.uids.length;
      const tb = [...document.querySelectorAll('#qcards .case-box')].find(b => (b.dataset.cuids || '').indexOf(target) >= 0);
      R.textHas = /【HZ 원문 고침】/.test(((tb && tb.querySelector('.case-text')) || {}).textContent || '');
      /* 정정 목록에도 「사례」 딱지·전후 한 줄 */
      showFixList(); await wait(200);
      const m = document.getElementById('fixlist-modal');
      R.listHasTag = m ? (m.textContent.match(/사례/g) || []).length : 0;
      R.listHasLine = m ? /사례.*(고침|채움)/.test(m.textContent) : false;
      if (m) m.remove();
      return JSON.stringify(R);
    },

    /* ══════════ §E-3 원문 상자 필기 ══════════ */
    c_ink: async function () {
      const R = {}; const cu = H.pick.caseUnit;
      /* 정정을 모두 걷고(§E-2 뒷정리) 원래 묶음(셋 중 둘)으로 돌아간다 — 필기는 그 상자에 긋는다 */
      cu.uids.forEach(u => { try { clearFix(u); } catch (e) { } });
      await wait(700);
      H.items.forEach(x => { delete x.origC; });
      H.items[0].caseText = '';                                  /* 다시 상자 밖(§C-2 를 재려면 나중에 들여야 한다) */
      startU(cu.k); currentPageIndex = cu.page; renderQuizPage(); await wait(900);
      R.fixLeft = Object.keys(JSON.parse(LS('ox_q_fix') || '{}')).length;
      if (cardMarksOn) { qiToggle(); await wait(500); }           /* 필기모드 */
      R.penon = document.getElementById('qcards').classList.contains('penon');
      qiTool('red');
      R.tool = JSON.stringify(QI_TOOL);
      const B = boxInfo(); R.boxes = B.length;
      const box = [...document.querySelectorAll('#qcards .case-box')].find(b => (b.dataset.cuids || '').indexOf(H.items[1].id) >= 0);
      R.key = box ? box.dataset.ckey : null;
      R.wantKey = 'case:' + cu.uids.slice(1).slice().sort()[0];
      R.n = cu.uids.length;
      const sv = box && box.querySelector('svg.qink');
      R.sv = !!sv; R.svId = sv ? sv.id : null;
      R.host = sv ? (sv.parentElement.className.split(' ')[0]) : null;
      R.hostPos = sv ? getComputedStyle(sv.parentElement).position : null;
      if (!sv) return JSON.stringify(R);
      /* 카드 덮개를 가로채지 않는가 — 상자 안 지문 카드에도 제 덮개가 살아 있다 */
      R.cardInks = box.querySelectorAll('.question-box > svg.qink').length;
      box.scrollIntoView({ block: 'start' }); window.scrollBy(0, -80); await wait(350);   /* ★ 보이는 자리로 — 화면 밖이면 elementFromPoint 가 늘 null 이라 헛패스가 된다 */
      const cb = box.querySelector('.question-box'); const cr = cb.getBoundingClientRect();
      R.cardRect = rect(cb);
      R.cardOnScreen = cr.top >= 0 && cr.top + 12 < innerHeight && cr.width > 0;
      const topAtCard = document.elementFromPoint(cr.left + cr.width / 2, cr.top + 12);
      R.cardTop = topAtCard ? (topAtCard.id || topAtCard.tagName + '.' + (topAtCard.getAttribute('class') || '')) : null;
      R.cardTopIsOwn = !!topAtCard && topAtCard.closest('.question-box') === cb;
      /* 빨강 한 획 */
      const r = sv.getBoundingClientRect();
      R.svRect = rect(sv);
      R.svOnScreen = r.top >= 0 && r.bottom <= innerHeight && r.width > 0 && r.height > 0;
      const x = r.left + r.width * 0.3, y = r.top + Math.min(20, r.height * 0.4);
      const under = qiUnder(x, y, sv);
      R.under = under ? (under.field ? 'field' : 'el') : null;   /* 없어야 획이 그어진다 */
      PEN(sv, 'pointerdown', x, y);
      PEN(sv, 'pointermove', x + 40, y + 6);
      PEN(sv, 'pointermove', x + 80, y + 2);
      PEN(sv, 'pointerup', x + 80, y + 2);
      await wait(700);                                            /* qiSave 는 300ms 뒤 */
      R.mem = (QI[R.key] && QI[R.key].s.length) || 0;
      R.memColor = (QI[R.key] && QI[R.key].s[0] && QI[R.key].s[0].c) || null;
      R.paths = sv.querySelectorAll('path:not(.qlive)').length;
      const v = await dbGet(qiKey(R.key));
      R.db = v && v.s ? v.s.length : 0;
      R.dbKey = qiKey(R.key);
      H.inkKey = R.key; H.cardInk0 = {};
      [...box.querySelectorAll('.question-box')].forEach(b => { const u = b.id.replace('q-box-', ''); H.cardInk0[u] = (QI[u] && QI[u].s.length) || 0; });
      R.cardInk0 = H.cardInk0;
      return JSON.stringify(R);
    },

    /* §E-3 쪽을 넘겼다 돌아오면 다시 그려진다 */
    c_ink_back: async function () {
      const R = {};
      const cu = H.pick.caseUnit;
      currentPageIndex = (cu.page === 0 ? 1 : 0); renderQuizPage(); await wait(700);
      R.away = document.querySelectorAll('#qcards svg.qink[id^="ink-case:"]').length;
      currentPageIndex = cu.page; renderQuizPage(); await wait(1100);
      const sv = document.getElementById('ink-' + H.inkKey);
      R.sv = !!sv;
      R.paths = sv ? sv.querySelectorAll('path:not(.qlive)').length : 0;
      R.mem = (QI[H.inkKey] && QI[H.inkKey].s.length) || 0;
      return JSON.stringify(R);
    },

    /* §E-3 §B 로 지문 하나를 상자에 들인 뒤에도 그 획이 보인다(열쇠가 바뀌어도) */
    c_ink_merge: async function () {
      const R = {}; const cu = H.pick.caseUnit; const items = H.items;
      R.keyBefore = H.inkKey;
      openFixPanel(items[0].id); await wait(150);
      const pull = [...document.querySelectorAll('#fixpanel-' + items[0].id + ' button')].find(b => /원문 가져오기/.test(b.textContent));
      R.pull = !!pull; if (!pull) return JSON.stringify(R);
      pull.click(); await wait(80);
      saveFix(items[0].id); await wait(1400);
      const box = [...document.querySelectorAll('#qcards .case-box')].find(b => (b.dataset.cuids || '').indexOf(items[1].id) >= 0);
      R.boxUids = box ? box.dataset.cuids : null;
      R.keyAfter = box ? box.dataset.ckey : null;
      R.keyChanged = R.keyAfter !== R.keyBefore;
      const sv = box && box.querySelector('svg.qink');
      R.paths = sv ? sv.querySelectorAll('path:not(.qlive)').length : 0;     /* ← 획이 살아 있다 */
      R.mem = (QI[R.keyAfter] && QI[R.keyAfter].s.length) || 0;
      const v = await dbGet(qiKey(R.keyAfter)); R.dbNew = v && v.s ? v.s.length : 0;
      const o = await dbGet(qiKey(R.keyBefore)); R.dbOld = o && o.s ? o.s.length : (o === undefined ? 'gone' : 0);
      H.inkKey2 = R.keyAfter;
      /* 지문 카드 필기는 무변 */
      R.cardInk1 = {}; Object.keys(H.cardInk0).forEach(u => { R.cardInk1[u] = (QI[u] && QI[u].s.length) || 0; });
      R.cardSame = Object.keys(H.cardInk0).every(u => R.cardInk1[u] === H.cardInk0[u]);
      /* 폭이 바뀌어도 획이 글자에 붙어 있다(§C-4 — 단위 좌표 · viewBox 그대로) */
      if (sv) { R.vb = sv.getAttribute('viewBox'); R.par = sv.getAttribute('preserveAspectRatio'); R.w0 = Math.round(sv.getBoundingClientRect().width); }
      return JSON.stringify(R);
    },

    /* §E-3 🗑 은 상자 필기도 지운다 · §E-6 새 키 0 */
    c_ink_clear: async function () {
      const R = {};
      const key = H.inkKey2 || H.inkKey;                        /* ★ 획을 그은 그 열쇠 — 쪽의 첫 상자를 재면 헛패스 */
      R.key = key;
      R.before = (QI[key] && QI[key].s.length) || 0;
      const bv = await dbGet(qiKey(key)); R.dbBefore = bv && bv.s ? bv.s.length : 0;
      await qiClearPage(); await wait(700);
      R.mem = (QI[key] && QI[key].s.length);
      const v = await dbGet(qiKey(key)); R.db = v ? (v.s || []).length : 'gone';
      /* 뒷정리 — 이 시험이 만든 정정을 걷는다 */
      H.pick.caseUnit.uids.forEach(u => { try { clearFix(u); } catch (e) { } });
      await wait(600);
      if (H.fixSnap == null) localStorage.removeItem('ox_q_fix'); else localStorage.setItem('ox_q_fix', H.fixSnap);
      R.fixRestored = LS('ox_q_fix') === H.fixSnap;
      let keys = []; try { keys = (await dbKeys()).filter(k => typeof k === 'string').sort(); } catch (e) { }
      R.newKeys = keys.filter(k => H.keys0.indexOf(k) < 0);
      R.newKeyShapes = [...new Set(R.newKeys.map(k => k.replace(/[^:]+$/, '*')))];
      R.syncKeys = (typeof SYNC_KEYS !== 'undefined') ? SYNC_KEYS.slice().sort() : null;
      return JSON.stringify(R);
    },

    /* §C-3 「✏️ 표시」 켜짐(형광펜·밑줄)에서 원문 글자에 표시가 되는가 — 재서 보고만(이번 판에서 만들지 않는다) */
    c_mark_probe: async function () {
      const R = {};
      if (!cardMarksOn) { qiToggle(); await wait(500); }
      R.penon = document.getElementById('qcards').classList.contains('penon');
      const box = document.querySelector('#qcards .case-box') || caseDivs()[0];
      if (!box) return JSON.stringify(R);
      const t = box.querySelector('.case-text') || box;
      R.caseMarkAttr = t.querySelectorAll('[data-mark]').length;
      R.cardMarkAttr = box.querySelectorAll('.question-box [data-mark]').length;
      R.caseHasMarkHost = !!t.closest('[data-markhost]') || !!t.querySelector('[data-markhost]');
      return JSON.stringify(R);
    }
  };
})();
