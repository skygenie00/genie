/* _task_ox_exview_paper_add2 하네스 — 브라우저 안 도구(__HZB). 누름은 playwright 진짜 마우스 / CDP 터치(반지름 22) · 여기서는 심기·상태·자리만.
   ⚠ 바탕(9d367aa · 95066d3b)에는 add2 함수(exvFixKick · exvRoundsUnion · exvSelFit)가 없다 — typeof 로 가르고 FAIL 로 끝나게(헛잣대).
   원격 기록 흉내 = SEED 의 __REMOTE_REC(sessionStorage '__hzrem' 에서 읽음) · 기록.json GET 늦춤 = sessionStorage '__hzdelay'(ms) · PUT = __PUTS */
(function () {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const T = n => (n ? n.textContent : '').replace(/\s+/g, ' ').trim();
  const LSJ = k => { try { return JSON.parse(localStorage.getItem(k) || '{}') || {}; } catch (e) { return {}; } };
  const LSP = (k, v) => localStorage.setItem(k, JSON.stringify(v));
  const Q = (s, r) => (r || document).querySelector(s);
  const QA = (s, r) => [...(r || document).querySelectorAll(s)];
  async function until(f, ms) { const t0 = Date.now(); while (Date.now() - t0 < (ms || 8000)) { try { if (f()) return true; } catch (e) { } await wait(50); } return false; }
  const EMPTY = () => ({});
  /* 정답 번호(1~5) — 앱 exvCorrect(그 해 조합 선지를 읽은 뒤) */
  async function ans(y) {
    const nos = (typeof exvNosOf === 'function') ? exvNosOf(y) : [];
    try { await exvComboLoad(y, nos); } catch (e) { }
    const o = {};
    nos.forEach(n => { const c = exvCorrect(y, n); o[n] = (c && c.ans && c.ans.length) ? c.ans[0] : 0; });
    return o;
  }
  function roundOf(A, date, ms, wrong, ok) {
    const P = {}, nos = Object.keys(A).filter(n => A[n]);
    nos.forEach(n => { P[n] = A[n]; });
    (wrong || []).forEach(n => { if (P[n]) P[n] = (P[n] % 5) + 1; });
    return { date: date, ok: ok == null ? nos.length - (wrong || []).length : ok, n: nos.length, ms: ms, picks: P };
  }
  function puts() {
    return (window.__PUTS || []).map(b => { try { const o = JSON.parse(b); return JSON.parse(decodeURIComponent(escape(atob(o.content)))); } catch (e) { return null; } }).filter(Boolean);
  }
  window.__HZB = {
    has: () => JSON.stringify({ kick: typeof exvFixKick === 'function', union: typeof exvRoundsUnion === 'function', fit: typeof exvSelFit === 'function', sync: typeof EXV_SYNC !== 'undefined' }),
    /* ★ revfix0928(9/28) A-2 — 받기 실패한 날 상태: 이 기기 날짜(Date · 하네스 __hzday 로 옮김) · ox_exv_fixskip · 첫 동기화 · 바로잡기 · 그 해 이 기기 회독 · 원격에 나간 키 */
    rxState: function (y) {
      const d = new Date(), today = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
      const L = (LSJ('ox_exam_rounds')[y] || []).map(r => ({ ok: r.ok, date: r.date, fixedAt: r.fixedAt || null, fv: r.fv || null }));
      const P = puts(), keys = {}; P.forEach(p => Object.keys(p.data || {}).forEach(k => { keys[k] = 1; }));
      return JSON.stringify({ today: today, skip: localStorage.getItem('ox_exv_fixskip'), sync: (typeof EXV_SYNC !== 'undefined') ? EXV_SYNC : null, fix: window.__exvFix || null, local: L, puts: P.length,
        putKeys: Object.keys(keys), skipInPut: !!keys.ox_exv_fixskip, syncKeys: (typeof SYNC_KEYS !== 'undefined') ? SYNC_KEYS.indexOf('ox_exv_fixskip') : null, online: navigator.onLine,
        recFail: (typeof recFail !== 'undefined') ? recFail : null, net: (window.__NET || []).filter(x => /기록/.test(x)).slice(-4) });
    },
    /* 첫 켜기 준비(가벼움) — 토큰 → 문항 → 기출키(서버 길 · 앱이 IndexedDB 에 담는다 → 새로고침 뒤 gkeyBoot 가 거기서 바로 읽는다) */
    prep: async function () {
      localStorage.setItem('tt.cfg', JSON.stringify({ token: 'harness-token', person: '꼬까' }));
      const M = await (await fetch('/data/master.json')).json();
      quizData.length = 0; buildQuizData(M.rows).forEach(q => quizData.push(q));
      try { await gkeyBoot(); } catch (e) { }
      await until(() => typeof GKEY !== 'undefined' && GKEY && GKEY.keys, 20000);
      await wait(300);   /* dbPut('gkey') 가 끝나게 */
      return JSON.stringify({ q: quizData.length, gkey: !!(GKEY && GKEY.keys) });
    },
    /* 새로고침 뒤 = 앱 window.onload 와 같은 차례(본판 하네스가 onload 를 끈다) — 문항(await) → gkeyBoot() → 첫 화면 → recBoot()(첫 동기화) · 둘 다 안 기다림 */
    appBoot: async function () {
      const M = await (await fetch('/data/master.json')).json();
      quizData.length = 0; buildQuizData(M.rows).forEach(q => quizData.push(q));
      window.__hzSyncAt = null;
      if (typeof exvSyncDone === 'function') { const o = exvSyncDone; exvSyncDone = function (ok) { if (window.__hzSyncAt === null) window.__hzSyncAt = Date.now(); return o(ok); }; }   /* 첫 동기화 끝 시각(바로잡기 fixedAt 과 차례 대조) */
      try { gkeyBoot(); } catch (e) { }
      try { applyAutoImportant(); renderDashboard(); } catch (e) { }
      try { refreshModeCounts(); } catch (e) { }
      try { recBoot(); } catch (e) { }
      return JSON.stringify({ q: quizData.length, at: Date.now() });
    },
    answers: async function (y) { return JSON.stringify(await ans(y)); },
    /* ── D-1 준비 — 이 기기 [R1](도장 T2−1h · 그림자 = 같은 값) · 원격 [R1, R2](도장 T2 · R2 = 다른 기기) · 토큰 · 기록.json GET 늦춤 */
    d1seed: async function (y, delay) {
      const A = await ans(y), nos = Object.keys(A).filter(n => A[n]);
      const R1 = roundOf(A, '2026. 9. 25.', 2400000, [], nos.length - 6);          /* 고른 답은 다 맞음 · 저장된 ok 는 6 모자람(옛 셈) */
      const R2 = roundOf(A, '2026. 9. 26.', 2500000, nos.slice(0, 2).map(Number)); /* 다른 기기 회독 · 둘 틀림 */
      const T2 = Date.parse('2026-09-27T01:00:00Z');
      localStorage.setItem('tt.cfg', JSON.stringify({ token: 'harness-token', person: '꼬까' }));
      LSP('ox_exam_rounds', { [y]: [R1] });
      const u = LSJ('ox_sync_u'); u['ox_exam_rounds|' + y] = T2 - 3600000; LSP('ox_sync_u', u);
      const sh = LSJ('ox_sync_shadow'); sh.ox_exam_rounds = { [y]: [R1] }; LSP('ox_sync_shadow', sh);
      sessionStorage.setItem('__hzrem', JSON.stringify({ data: { ox_exam_rounds: { [y]: [R1, R2] } }, u: { ['ox_exam_rounds|' + y]: T2 }, gone: {} }));
      sessionStorage.setItem('__hzdelay', String(delay || 0));
      sessionStorage.setItem('__hzkeep', '1');
      return JSON.stringify({ n: nos.length, r1: R1.ok, r2: R2.ok, want1: nos.length });
    },
    d1state: function (y) {
      const L = (LSJ('ox_exam_rounds')[y] || []).map(r => ({ ok: r.ok, date: r.date, fixedAt: r.fixedAt || null, fv: r.fv || null }));
      const P = puts(), last = P.length ? P[P.length - 1] : null;
      const PR = last ? ((((last.data || {}).ox_exam_rounds || {})[y]) || []).map(r => ({ ok: r.ok, date: r.date, fixedAt: r.fixedAt || null })) : null;
      return JSON.stringify({ local: L, puts: P.length, remote: PR, fix: window.__exvFix || null, sync: (typeof EXV_SYNC !== 'undefined') ? EXV_SYNC : null, syncAt: window.__hzSyncAt || null, recFail: (typeof recFail !== 'undefined') ? recFail : null });
    },
    /* ── D-2 준비 — 2016 회독 셋: R(다 맞음 · ok 40) · Rup(다 맞음 · ok 36 = 옛 셈이 모자람) · Rdn(둘 틀림 · ok 40 = 옛 셈이 넘침) · 원격 = 같은 값(도장 같음) · 토큰 */
    d2seed: async function (y, A0) {
      /* ⚠ 시험지 색인은 IndexedDB 에 담긴다 — 이 창에서 PDF 를 읽으면 404 흉내가 안 먹는다. 정답은 다른 창(저장소가 따로)에서 셈해 넘긴다 */
      const A = A0 || await ans(y), nos = Object.keys(A).filter(n => A[n]);
      const R = roundOf(A, '2026. 9. 20.', 3000000, []);
      const Rup = roundOf(A, '2026. 9. 21.', 3100000, [], nos.length - 4);
      const Rdn = roundOf(A, '2026. 9. 22.', 3200000, nos.slice(-2).map(Number), nos.length);
      const T1 = Date.parse('2026-09-26T01:00:00Z');
      localStorage.setItem('tt.cfg', JSON.stringify({ token: 'harness-token', person: '꼬까' }));
      LSP('ox_exam_rounds', { [y]: [R, Rup, Rdn] });
      const u = LSJ('ox_sync_u'); u['ox_exam_rounds|' + y] = T1; LSP('ox_sync_u', u);
      const sh = LSJ('ox_sync_shadow'); sh.ox_exam_rounds = { [y]: [R, Rup, Rdn] }; LSP('ox_sync_shadow', sh);
      sessionStorage.setItem('__hzrem', JSON.stringify({ data: { ox_exam_rounds: { [y]: [R, Rup, Rdn] } }, u: { ['ox_exam_rounds|' + y]: T1 }, gone: {} }));
      sessionStorage.setItem('__hzdelay', '0');
      sessionStorage.setItem('__hzkeep', '1');
      return JSON.stringify({ n: nos.length, oks: [R.ok, Rup.ok, Rdn.ok], want2: [nos.length, nos.length, Rdn.ok] });
    },
    d2state: function (y) {
      const L = (LSJ('ox_exam_rounds')[y] || []).map(r => ({ ok: r.ok, fixedAt: r.fixedAt || null, fv: r.fv || null }));
      const P = puts(), rem = P.map(p => ((((p.data || {}).ox_exam_rounds || {})[y]) || []).map(r => ({ ok: r.ok, fixedAt: r.fixedAt || null })));
      const combos = (typeof exvNosOf === 'function') ? exvNosOf(y).filter(n => exvIsCombo(y, n)).map(n => [n, exvCorrect(y, n).why || '', (exvCorrect(y, n).ans || []).length]) : [];
      return JSON.stringify({ local: L, puts: rem, fix: window.__exvFix || null, combos: combos });
    },
    /* ── D-3 첫 화면 회독 상자(그 해 줄) */
    dash: function (y) {
      const c = Q('[data-exvcount="' + y + '"]');
      let row = c; for (let i = 0; row && i < 6 && !QA('.exv-dround', row).length; i++) row = row.parentElement;
      const boxes = row ? QA('.exv-dround', row) : [];
      const home = document.getElementById('home-screen');
      return JSON.stringify({ home: !!home && !home.classList.contains('hide'), boxes: boxes.map(b => T(b.querySelector('.exv-dok'))), txt: boxes.map(T) });
    },
    /* ── D-4 채점 기다림 — 마지막 회독의 그 문번 고른 답 · 40번 선지 단추 자리 */
    lastPick: function (y, no) { const R = (LSJ('ox_exam_rounds')[y] || []); const r = R[R.length - 1]; return JSON.stringify({ n: R.length, p: r && r.picks ? +r.picks[no] : null, ok: r ? r.ok : null }); },
    optAt: function (y, no, n) {
      const k = y + ':' + no;
      const b = QA('[data-exk="' + k + '"][data-exn="' + n + '"]').find(e => e.offsetParent !== null);
      if (!b) return JSON.stringify(null);
      b.scrollIntoView({ block: 'center', behavior: 'instant' });
      const r = b.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2, at = document.elementFromPoint(cx, cy);
      return JSON.stringify({ cx: cx, cy: cy, on: true, hit: !!at && (at === b || b.contains(at)), tag: at ? at.tagName + '.' + at.className : null });
    },
    pickOf: function (y, no) { return JSON.stringify(+((typeof exvPicks === 'function') ? exvPicks()[y + ':' + no] : 0) || 0); },
    /* ── D-6 선지 줄 — 그 문번 조합 선지 폭·자리 · 둘째 줄 빈 곳 자리 */
    selInfo: function (key) {
      const s = Q('[data-exsel="' + key + '"]');
      if (!s) return JSON.stringify(null);
      s.scrollIntoView({ block: 'center', behavior: 'instant' });
      const opts = QA('.exv-opt', s).map(o => { const r = o.getBoundingClientRect(); return { x: +r.left.toFixed(2), y: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2), n: +o.dataset.exn }; });
      const rows = [...new Set(opts.map(o => Math.round(o.y)))];
      const sr = s.getBoundingClientRect();
      let empty = null;
      if (rows.length > 1) {   /* 마지막 줄의 마지막 선지 오른쪽 빈 곳(줄 안) */
        const lastRow = opts.filter(o => Math.round(o.y) === rows[rows.length - 1]);
        const L = lastRow[lastRow.length - 1];
        const x = L.x + L.w + Math.max(8, (sr.right - (L.x + L.w)) / 2), y = L.y + L.h / 2;
        if (x < sr.right - 2) { const at = document.elementFromPoint(x, y); empty = { cx: x, cy: y, on: true, hit: true, tag: at ? at.tagName + '.' + at.className : null, onOpt: !!(at && at.closest && at.closest('.exv-opt')) }; }
      }
      return JSON.stringify({ opts: opts, rows: rows.length, cls: s.className, sw: +sr.width.toFixed(2), empty: empty });
    }
  };
})();
