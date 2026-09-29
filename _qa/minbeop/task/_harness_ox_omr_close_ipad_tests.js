/* _task_ox_omr_close_ipad 하네스 — 브라우저 안 도우미.
   ★ 누름은 전부 playwright 가 **진짜 터치**(touchscreen.tap · 크롬 끌기는 CDP 터치)로 한다. 여기서는 자리를 재고 상태를 읽기만 한다.
   ⚠ 뷰어의 V 는 클로저 안이라 밖에서 못 읽는다 — 눈에 보이는 것(DOM)으로 잰다.
   ⚠ BASE 판의 뷰어 틀에는 id 가 없다 — 두 판을 같은 잣대로 세려고 「#cd-close 를 품은 body 직계 자식」을 뷰어 한 장으로 센다.
      NEW 판은 그와 따로 `#cd-wrap` 개수도 센다(§B-1). */
window.onload = null;   /* 앱 초기화(망·동기화)를 끈다 — 시험이 저장소·문항을 직접 싣는다 */
(function () {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const H = window.__HZ = window.__HZ || {};
  const LS = k => localStorage.getItem(k);
  const CO = () => JSON.parse(LS('ox_q_coords') || '{}');
  const txt = n => (n ? n.textContent : '').replace(/\s+/g, ' ').trim();
  const wraps = () => [...document.body.children].filter(d => d.querySelector && d.querySelector('#cd-close'));
  const topWrap = () => { const w = wraps(); return w.length ? w[w.length - 1] : null; };
  const inWrap = el => wraps().some(w => w.contains(el));
  const layerOf = w => { const c = w && w.querySelector('canvas'); return c ? c.nextElementSibling : null; };
  const stageOf = w => { const c = w && w.querySelector('canvas'); return c ? c.parentElement.parentElement : null; };
  const book = uid => document.getElementById('oxwin-book-' + uid);
  const omrRow = uid => { const b = book(uid); return b ? [...b.querySelectorAll('div[onclick]')].find(d => /^mbOmrGo\(/.test(d.getAttribute('onclick'))) : null; };

  /* 모든 click 을 잡아채는 층에서 적는다 — 어느 요소에 · 신뢰 이벤트인가 · 언제 */
  const CLK = window.__CLK = [];
  document.addEventListener('click', e => {
    const t = e.target;
    CLK.push({ id: (t && t.id) || '', tag: t && t.tagName, tr: e.isTrusted, inWrap: !!(t && t.closest && inWrap(t)),
               row: !!(t && t.closest && t.closest('div[onclick^="mbOmrGo("]')), t: Math.round(performance.now()) });
  }, true);
  const PEN = window.__PEN = [];
  document.addEventListener('pointerup', e => { if (e.pointerType === 'pen') PEN.push(Math.round(performance.now())); }, true);

  /* 요소 한 점 — 화면 안인가 · 그 자리 맨 위가 그 요소(또는 그 안)인가 · 맨 위 요소 이름 */
  function at(el, fx, fy) {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    const x = r.left + r.width * (fx == null ? 0.5 : fx), y = r.top + r.height * (fy == null ? 0.5 : fy);
    const on = r.width > 0 && r.height > 0 && x >= 0 && y >= 0 && x < innerWidth && y < innerHeight;
    const top = on ? document.elementFromPoint(x, y) : null;
    return { cx: Math.round(x * 10) / 10, cy: Math.round(y * 10) / 10, w: Math.round(r.width), h: Math.round(r.height), on: on,
             hit: !!(top && (top === el || el.contains(top))),
             top: top ? ((top.id ? '#' + top.id : top.tagName) + (inWrap(top) ? '@뷰어' : '') + (top.closest && top.closest('.oxwin') ? '@창' : '')) : null };
  }
  function state() {
    const w = topWrap(), R = { wraps: wraps().length, cdWrap: document.querySelectorAll('#cd-wrap').length };
    R.quiz = !!document.getElementById('quiz-screen') && !document.getElementById('quiz-screen').classList.contains('hide');
    if (!w) return R;
    const L = layerOf(w);
    R.foot = [...w.querySelectorAll('button')].map(b => b.id).filter(id => /^cd-/.test(id) && ['cd-close', 'cd-prev', 'cd-next', 'cd-find', 'cd-check', 'cd-forget'].indexOf(id) < 0);
    R.mode = R.foot.indexOf('cd-zoom') >= 0 ? 'view' : (R.foot.indexOf('cd-mark') >= 0 ? 'pick' : '?');
    R.layerPE = L ? L.style.pointerEvents : null;
    R.pick = !!(L && L.querySelector('#cd-pick'));
    const sv = w.querySelector('#cd-save'); R.saveOn = !!(sv && !sv.disabled);
    R.pg = txt(w.querySelector('#cd-pg'));
    R.bar = txt(w.children[1]).slice(0, 60);
    return R;
  }

  window.__HZT = {
    /* ── 준비: 기록.json 저장소 전부 · 문항 5,548 · 가짜 정리OMR 자산(쪽 비움 — 기존 하네스 `_task_ox_omrgo_pick` 그대로) */
    setup: async function () {
      const R = {};
      const rec = await (await fetch('/rec.json')).json();
      const D = rec.data || rec;
      localStorage.clear();
      const BASE = { 'ox_uid_migrated': '1', 'ox_gg_okreset': '1', 'ox_auto_important_v2': '1' };
      for (const k in BASE) localStorage.setItem(k, BASE[k]);
      for (const k in D) localStorage.setItem(k, typeof D[k] === 'string' ? D[k] : JSON.stringify(D[k]));
      /* 토큰은 가짜 — 교재 자리표(jari) 한 길만 시험이 대답한다(SEED 의 fetch). 나머지 GitHub 는 404 */
      localStorage.setItem('tt.cfg', JSON.stringify({ person: '하네스', token: 'github_pat_HARNESS' }));
      try { useIdxDrop(); } catch (e) { }
      const M = await (await fetch('/master.json')).json();
      quizData.length = 0; buildQuizData(M.rows).forEach(q => quizData.push(q));
      R.q = quizData.length;
      await dbPut('omrasset:minbeopOMR', { pages: new Array(60).fill(null) });

      /* 단원 — 20문항 이상 · 첫 쪽 카드에 정리OMR 자리 0곳 문항이 셋 이상(자리 = oxCoord.omrSlots) */
      const a = window.oxCoord, co = a.coords();
      const U = {};
      quizData.forEach(x => {
        const lab = x.subChapter ? (x.chapter + ' > ' + x.subChapter) : x.chapter;
        (U[x.subject + '||' + lab] = U[x.subject + '||' + lab] || []).push(x);
      });
      const keys = Object.keys(U).filter(k => U[k].length >= 20).sort();
      let got = null;
      for (const k of keys) {
        const i = k.indexOf('||');
        startQuiz(k.slice(0, i), k.slice(i + 2));
        await wait(250);
        const ids = [...document.querySelectorAll('#qcards .question-box')].map(b => String(b.id || '').replace('q-box-', ''));
        const zero = ids.filter(u => !a.omrSlots(co, u).length && document.querySelector('button[onclick="mbBookOpen(\'' + u + '\')"]'));
        if (zero.length >= 3) { got = { k: k, ids: ids, zero: zero }; break; }
      }
      if (!got) return JSON.stringify({ q: R.q, err: 'no unit' });
      H.unit = got.k; H.u1 = got.zero[0]; H.u2 = got.zero[1]; H.u3 = got.zero[2];
      R.unit = got.k; R.cards = got.ids.length; R.u1 = H.u1; R.u2 = H.u2; R.u3 = H.u3;
      /* 📎 교재 창에 뜰 자리표 — 교재 한 줄 + 정리OMR 1등·후보 2 (앱이 받는 꼴 그대로) */
      window.__JARI = {};
      [H.u1, H.u2, H.u3].forEach(u => {
        window.__JARI[u] = { rows: [{ doc: '9판', p: 100, snip: '하네스 교재 줄', score: 1, gap: 0.5 }],
                             omr: [{ p: 5, snip: '하네스 정리OMR 줄', rank: 1, x: 0.30, y: 0.40, w: 0.20, h: 0.05 },
                                   { p: 6, snip: '하네스 후보 2', rank: 2, x: 0.10, y: 0.20, w: 0.30, h: 0.05 }] };
      });
      H.co0 = LS('ox_q_coords');
      R.coKeys0 = Object.keys(CO()).length;
      R.slots0 = [H.u1, H.u2, H.u3].map(u => a.omrSlots(co, u).length);
      R.quiz = state().quiz;
      R.syncKeys = (typeof SYNC_KEYS !== 'undefined') ? SYNC_KEYS.slice().sort() : null;
      return JSON.stringify(R);
    },

    /* ID 칩 한 점(가운데로 굴려 둔 뒤) */
    chip: async function (u) {
      const b = document.querySelector('button[onclick="mbBookOpen(\'' + u + '\')"]');
      if (!b) return JSON.stringify(null);
      b.scrollIntoView({ block: 'center' }); await wait(150);
      return JSON.stringify(at(b));
    },
    /* 📍 칩 한 점 */
    pin: async function (u) {
      const b = document.getElementById('tag-coord-' + u);
      if (!b) return JSON.stringify(null);
      b.scrollIntoView({ block: 'center' }); await wait(150);
      return JSON.stringify(at(b));
    },
    /* 교재 창이 떠서 정리OMR 줄이 섰는가 */
    rowReady: function (u) { return !!omrRow(u); },
    row: function (u) { return JSON.stringify(at(omrRow(u), 0.5, 0.35)); },
    bookOff: function (u) { try { oxWinClose('book-' + u); } catch (e) { } return !book(u); },
    /* 뷰어 위 단추 한 점(맨 위 뷰어) */
    btn: function (id) { const w = topWrap(); return JSON.stringify(at(w && w.querySelector('#' + id))); },
    /* 뷰어가 다 그렸는가(쪽 글자 · 아래 단추 · 원하는 모드) */
    ready: function (mode) { const s = state(); return !!(s.wraps && s.pg && s.foot && s.foot.length && (!mode || s.mode === mode)); },
    state: function () { return JSON.stringify(state()); },
    /* 끌기 자리 — 맨 위 뷰어의 **맨몸 레이어**가 맨 위인 점(남의 핀 상자·교재 창 위는 안 된다) */
    dragPlan: function (dx, dy) {
      const w = topWrap(), L = layerOf(w), S = stageOf(w);
      if (!L || !S) return JSON.stringify(null);
      const a = S.getBoundingClientRect(), b = L.getBoundingClientRect();
      const x0 = Math.max(a.left, b.left) + 12, x1 = Math.min(a.right, b.right) - 12 - dx;
      const y0 = Math.max(a.top, b.top) + 12, y1 = Math.min(a.bottom, b.bottom) - 12 - dy;
      /* 둘레 24px 안에 누를 수 있는 것이 없어야 한다 — 크롬은 손가락 터치를 **면적**으로 판정해 가까운 남의 핀 상자를 잡는다
         (0.77px 떨어진 상자가 잡힌 것을 실측 · 그 상자의 onpointerdown 이 stopPropagation 이라 끌기가 아예 안 선다 · BASE·NEW 같음).
         ⇒ 레이어 안 pointer-events 가 살아 있는 자식 · 떠 있는 창(.oxwin)의 사각형을 24px 넓혀 그 밖인 점만 쓴다 */
      const M = 24;
      const blocks = [...L.children].filter(c => getComputedStyle(c).pointerEvents !== 'none').concat([...document.querySelectorAll('.oxwin')])
        .map(c => c.getBoundingClientRect()).map(r => [r.left - M, r.top - M, r.right + M, r.bottom + M]);
      const ok = (x, y) => document.elementFromPoint(x, y) === L && blocks.every(r => x < r[0] || x > r[2] || y < r[1] || y > r[3]);
      for (let fy = 0.55; fy <= 0.95; fy += 0.05) {
        for (let fx = 0.05; fx <= 0.95; fx += 0.05) {
          const x = Math.round(x0 + (x1 - x0) * fx), y = Math.round(y0 + (y1 - y0) * fy);   /* 잰 점 = 던질 점(반올림 뒤에 잰다) */
          if (x1 > x0 && y1 > y0 && ok(x, y) && ok(x + dx, y + dy) && ok(x + dx / 2, y + dy / 2)) {
            return JSON.stringify({ x: Math.round(x), y: Math.round(y), x2: Math.round(x + dx), y2: Math.round(y + dy),
                                    L: [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)] });
          }
        }
      }
      return JSON.stringify({ none: true, S: [a.left, a.top, a.width, a.height], L: [b.left, b.top, b.width, b.height] });
    },
    /* §A-2 저장 뒤 — ① 뷰어 수 ② 닫기 가운데 elementFromPoint ③(톡은 밖에서) · 책 창이 뷰어 위에 떠 있는가 */
    a2: function (u) {
      const w = topWrap(), R = state();
      R.close = at(w && w.querySelector('#cd-close'));
      R.zoomBtn = at(w && w.querySelector('#cd-zoom'));
      const bk = book(u);
      if (bk) {
        R.bookZ = +bk.style.zIndex || 0;
        R.wrapZ = w ? +getComputedStyle(w).zIndex || 0 : null;
        R.bookOverViewer = at(bk, 0.5, 0.5);                 /* 책 창 가운데 맨 위 = 책 창이면 뷰어 위에 떠 있다 */
        R.rowStillOnTop = at(omrRow(u), 0.5, 0.35);          /* 뷰어가 떠 있어도 정리OMR 줄을 다시 누를 수 있는가 */
      }
      CLK.length = 0;
      return JSON.stringify(R);
    },
    /* 닫기 톡 뒤 — ④ 뷰어 수 · 문제풀이 화면 · 가운데 점이 뷰어 안인가 · 그 사이 click 이 어디에 났나 */
    after: function () {
      const R = state();
      R.clicks = CLK.splice(0).map(c => (c.id || c.tag) + (c.tr ? '' : '(합성)') + (c.inWrap ? '@뷰어' : ''));
      const e = document.elementFromPoint(innerWidth / 2, innerHeight * 0.75);
      R.center = e ? ((e.id ? '#' + e.id : e.tagName) + (inWrap(e) ? '@뷰어' : '') + (e.closest && e.closest('#quiz-screen') ? '@문제풀이' : '') + (e.closest && e.closest('.oxwin') ? '@창' : '')) : null;
      R.centerInWrap = !!(e && inWrap(e));
      return JSON.stringify(R);
    },
    /* 남은 뷰어가 먹통인가(BASE 증상 재현용) — 남은 뷰어의 닫기·아래 단추 자리 · 굴릴 수 있는가 */
    leftover: function () {
      const w = topWrap(); if (!w) return JSON.stringify(null);
      const S = stageOf(w), cv = w.querySelector('canvas');
      return JSON.stringify({ close: at(w.querySelector('#cd-close')), foot: [...w.lastElementChild.querySelectorAll('button')].map(b => b.id),
                              canvas: cv ? [cv.width, cv.height] : null,
                              scrollable: !!(S && (S.scrollHeight > S.clientHeight + 2 || S.scrollWidth > S.clientWidth + 2)),
                              pg: txt(w.querySelector('#cd-pg')) });
    },
    stageScroll: function () { const S = stageOf(topWrap()); return S ? [Math.round(S.scrollLeft), Math.round(S.scrollTop)] : null; },
    /* 뒷정리 — 남은 뷰어를 DOM 에서 뗀다(다음 장면이 깨끗이 시작하게 · 앱 함수는 안 부른다) */
    wipe: function () { const n = wraps().length; wraps().forEach(w => w.remove()); document.querySelectorAll('.oxwin').forEach(w => w.remove()); CLK.length = 0; return n; },
    /* §A-3 펜 톡 흉내 — 앱의 펜 합성기가 보는 그대로(pointerType pen · __syn 없음) 누른 자리에 down→up 을 던진다 */
    pen: function (x, y) {
      const t = document.elementFromPoint(x, y);
      if (!t) return JSON.stringify(null);
      const mk = ty => new PointerEvent(ty, { bubbles: true, cancelable: true, composed: true, pointerId: 31, pointerType: 'pen', isPrimary: true, clientX: x, clientY: y, button: 0, buttons: ty === 'pointerdown' ? 1 : 0 });
      CLK.length = 0; PEN.length = 0;
      t.dispatchEvent(mk('pointerdown'));
      t.dispatchEvent(mk('pointerup'));
      return JSON.stringify({ t: t.tagName + (t.id ? '#' + t.id : ''), up: PEN[0] });
    },
    penResult: function () {
      const up = PEN[0];
      return JSON.stringify({ wraps: wraps().length, cdWrap: document.querySelectorAll('#cd-wrap').length,
                              clicks: CLK.map(c => ({ tr: c.tr, row: c.row, dt: up == null ? null : c.t - up })) });
    },
    coords: function () { return JSON.stringify(CO()); },
    co0: function () { return H.co0; },
    errs: function () { return JSON.stringify(window.__ERR || []); }
  };
})();
