window.onload = null;
(function () {
const P = __P__;
const R = [];
const T = (n, c, i) => R.push((c ? 'PASS' : 'FAIL') + ' | ' + n + ((i !== undefined && !c) ? ' | ' + String(i).replace(/\n/g, '⏎').slice(0, 600) : ''));
const V = (k, v) => R.push('VAL | ' + k + ' | ' + JSON.stringify(v));
const say = s => R.push('INFO | ' + String(s).replace(/\n/g, '⏎').slice(0, 900));
const wait = ms => new Promise(r => setTimeout(r, ms));
const until = async (f, n) => { for (let i = 0; i < (n || 300); i++) { try { if (f()) return true; } catch (e) { } await wait(30); } try { return !!f(); } catch (e) { return false; } };
const NEW = (typeof ggBangToggle === 'function');
const BASE = { 'ox_uid_migrated': '1', 'ox_gg_okreset': '1', 'ox_auto_important_v2': '1',
               'tt.cfg': JSON.stringify({ person: '하네스', token: 'harness-token' }) };
const resetLS = o => {
  localStorage.clear();
  for (const k in BASE) localStorage.setItem(k, BASE[k]);
  for (const k in (o || {})) localStorage.setItem(k, typeof o[k] === 'string' ? o[k] : JSON.stringify(o[k]));
  try { useIdxDrop(); } catch (e) { }
};
const loadQuiz = () => { quizData.length = 0; buildQuizData(P.rows).forEach(q => quizData.push(q)); };
const closeWins = () => document.querySelectorAll('.oxwin').forEach(w => w.remove());
const showHome = () => {
  document.getElementById('home-screen').classList.remove('hide');
  document.getElementById('quiz-screen').classList.add('hide');
};
const openQuiz = ids => {
  currentSubject = ''; currentChapterLabel = ''; isExamMode = false; currentPageIndex = 0;
  currentSessionMarks = {}; resumePicks = {}; currentSessionScore = 0; lastGradeResults = null;
  currentFilteredData = ids.map(id => quizData.find(q => q.id === id));
  document.getElementById('home-screen').classList.add('hide');
  document.getElementById('quiz-screen').classList.remove('hide');
  renderQuizPage();
};
const A = P.a, B = P.b, C = P.c, D = P.d, OWN = P.own;   /* 문항 uid 다섯 — A·OWN·B 는 1단원 · C 는 2단원 · D 는 3단원 */
const GG = () => { try { return JSON.parse(localStorage.getItem('ox_q_geunge') || '{}'); } catch (e) { return {}; } };

/* 근거 셋 — A 에 3개(k1·k2·k3 · ok 를 갈라 둔다) · B 에 2개 · C 에 1개 */
const SEED = () => {
  const g = {};
  g[A] = [{ k: 'ka1', i: 1, t: 'A 근거 하나', ok: null, ts: 1 },
          { k: 'ka2', i: 2, t: 'A 근거 둘 — 틀림', ok: false, ts: 2 },
          { k: 'ka3', i: 3, t: 'A 근거 셋 — 맞음', ok: true, ts: 3 }];
  g[B] = [{ k: 'kb1', i: 1, t: 'B 근거 하나 정관등기', ok: null, ts: 4 },
          { k: 'kb2', i: 2, t: 'B 근거 둘', ok: null, ts: 5 }];
  g[C] = [{ k: 'kc1', i: 1, t: 'C 근거 하나', ok: null, ts: 6 }];
  /* ⚠ D 는 **켜지지 않는 단원**이다 — 이게 없으면 「켜진 단원만」이 줄어드는지 잴 수 없다(2026-09-16) */
  g[D] = [{ k: 'kd1', i: 1, t: 'D 근거 하나 — 켜지 않는다', ok: null, ts: 7 }];
  const rl = {}; rl[OWN] = { geunge: [A] };            /* OWN 이 A 를 🔗 로 걸고 있다 */
  return { ox_q_geunge: g, ox_q_reflinks: rl };
};

async function main() {
  resetLS(SEED());
  loadQuiz();
  say('NEW=' + NEW + ' · rows=' + P.rows.length + ' · uids ' + [A, OWN, B, C, D].join(','));

  /* ══════════ G1 저장 — 칸 하나, 두 번이면 원상 ══════════ */
  try {
    if (!NEW) { T('G1 ggBangToggle 이 있다', false, 'ggBangToggle 없음(옛 판)'); }
    else {
      const before = localStorage.getItem('ox_q_geunge');
      const keysBefore = Object.keys(localStorage).sort().join(',');
      ggBangToggle(A, 'ka2');
      const mid = GG();
      const it = (mid[A] || []).find(x => x.k === 'ka2');
      T('G1 그 항목에만 bang:true', !!(it && it.bang === true), JSON.stringify(it));
      const others = (mid[A] || []).filter(x => x.k !== 'ka2').concat(mid[B] || [], mid[C] || []);
      T('G1 다른 항목엔 bang 이 안 붙는다', others.every(x => !('bang' in x)),
        JSON.stringify(others.filter(x => 'bang' in x)));
      T('G1 다른 칸 무변', it && it.i === 2 && it.t === 'A 근거 둘 — 틀림' && it.ok === false && it.ts === 2,
        JSON.stringify(it));
      ggBangToggle(A, 'ka2');
      T('G1 두 번 누르면 바이트 단위 원상', localStorage.getItem('ox_q_geunge') === before,
        'after=' + localStorage.getItem('ox_q_geunge'));
      T('G1 끄면 칸을 지운다(false 로 두지 않는다)',
        !('bang' in ((GG()[A] || []).find(x => x.k === 'ka2') || {})),
        JSON.stringify((GG()[A] || []).find(x => x.k === 'ka2')));
      T('G1 새 localStorage 키 0', Object.keys(localStorage).sort().join(',') === keysBefore,
        'before=' + keysBefore + ' after=' + Object.keys(localStorage).sort().join(','));
      T('G1 SYNC_KEYS 무변', SYNC_KEYS.join(',') === P.syncKeys, SYNC_KEYS.join(','));
      T('G1 ox_q_reflinks 무변', localStorage.getItem('ox_q_reflinks') === JSON.stringify(SEED().ox_q_reflinks),
        localStorage.getItem('ox_q_reflinks'));
    }
  } catch (e) { T('G1', false, e.message); }

  /* ══════════ G2 세 범위 + 연결 상자 + 검색 ══════════ */
  try {
    resetLS(SEED()); loadQuiz(); closeWins();
    openQuiz([A, OWN]);
    await wait(60);
    openQPopup(A);                        /* qp- 범위 */
    await wait(60);
    onCountClick();                       /* 근거 목록(정리 창) */
    await wait(60);

    const panes = k => [...document.querySelectorAll('[data-gbbox="' + A + '|' + k + '"]')];
    const bangs = k => [...document.querySelectorAll('[data-gb="' + A + '|' + k + '"]')];
    const nums = k => [...document.querySelectorAll('[data-gbnum="' + A + '|' + k + '"]')];
    V('G2.places', { bang: bangs('ka1').length, box: panes('ka1').length, num: nums('ka1').length });
    T('G2 「!」 가 여러 자리에 있다', NEW && bangs('ka1').length >= 2, 'bang ' + bangs('ka1').length);

    /* 펼침을 켜 두고 → 토글 뒤에도 살아 있어야 한다 */
    ggToggle(A, 'ka1');                   /* 카드 범위 판 펼침 */
    const pan0 = document.getElementById('gg-pan-' + A + '-ka1');
    const wasOpen = pan0 && !pan0.classList.contains('hide');
    T('G2 판을 펼쳐 두었다', !!wasOpen, 'open=' + wasOpen);
    const cardBox = document.getElementById('gg-box-' + A);
    const stamp = cardBox ? cardBox.innerHTML.length : -1;

    if (NEW) {
      const src = bangs('ka1')[0];
      src.click();
      await wait(60);
      T('G2 켠 뒤 모든 「!」 가 켜짐', bangs('ka1').every(e => e.classList.contains('on')),
        bangs('ka1').map(e => e.className).join(' | '));
      T('G2 켠 뒤 모든 판이 켜짐', panes('ka1').every(e => e.classList.contains('gg-on') || e.classList.contains('gg-on-dash')),
        panes('ka1').map(e => e.className).join(' | '));
      T('G2 켠 뒤 원문자가 켜짐', nums('ka1').every(e => e.classList.contains('ggnum-on')),
        nums('ka1').map(e => e.className).join(' | '));
      const pan1 = document.getElementById('gg-pan-' + A + '-ka1');
      T('G2 펼침이 살아 있다(카드 통째 다시 그리기 0)', !!(pan1 && !pan1.classList.contains('hide')),
        pan1 ? pan1.className : 'no pan');
      T('G2 같은 판 노드 그대로', pan1 === pan0, 'replaced');
      /* 연결 상자(OWN 의 🔗 A) */
      const refbox = [...document.querySelectorAll('[data-gbrefbox="' + A + '"]')];
      const refchip = [...document.querySelectorAll('[data-gbref="' + A + '"]')];
      T('G2 연결 상자 틀이 붉어진다', refbox.length > 0 && refbox.every(e => e.classList.contains('ggrefbox-on')),
        refbox.map(e => e.className).join(' | ') || 'none');
      T('G2 🔗 칩이 붉어진다', refchip.length > 0 && refchip.every(e => e.classList.contains('ggchip-on')),
        refchip.map(e => e.className).join(' | ') || 'none');
      /* 다른 범위에서 꺼도 전부 꺼진다 */
      const other = bangs('ka1')[bangs('ka1').length - 1];
      other.click();
      await wait(60);
      T('G2 다른 범위에서 끄면 전부 꺼진다', bangs('ka1').every(e => !e.classList.contains('on')),
        bangs('ka1').map(e => e.className).join(' | '));
      T('G2 판도 전부 꺼진다', panes('ka1').every(e => !e.classList.contains('gg-on') && !e.classList.contains('gg-on-dash')), '');
    }

    /* 근거 검색 결과 — 켜진 근거가 걸리면 그 줄도 빨강 */
    if (NEW) {
      ggBangToggle(B, 'kb1');
      setSearchMode('m');
      document.getElementById('search-input').value = '정관등기';
      runSearch();
      await wait(60);
      const html = document.getElementById('search-results').innerHTML;
      T('G2 검색 결과에 켜진 근거 색', html.indexOf('#fff5f5') >= 0, html.slice(0, 260));
      ggBangToggle(B, 'kb1');
      runSearch();
      await wait(40);
      T('G2 끄면 검색 결과도 돌아온다',
        document.getElementById('search-results').innerHTML.indexOf('#fff5f5') < 0, '');
      document.getElementById('search-input').value = '';
      runSearch();
    }
  } catch (e) { T('G2', false, e.message); }

  /* ══════════ G3 원문자 — 틀림 + 켜짐이 둘 다 ══════════ */
  try {
    resetLS(SEED()); loadQuiz(); closeWins(); showHome();
    openQuiz([A]);
    await wait(50);
    if (NEW) ggBangToggle(A, 'ka2');      /* ka2 = ok:false(틀림) */
    await wait(40);
    const c = document.getElementById('gg-chip-' + A + '-ka2');
    V('G3.chipcls', c ? c.className : 'none');
    T('G3 틀림 클래스가 남아 있다', !!(c && /text-red-700/.test(c.className) && /bg-red-50/.test(c.className)),
      c ? c.className : 'none');
    T('G3 켜짐 클래스도 같이', !!(c && c.classList.contains('ggnum-on')), c ? c.className : 'none');
    T('G3 틀림은 흰 바탕으로 덮지 않는다', !!(c && !c.classList.contains('ggnum-on-n')), c ? c.className : 'none');
    if (NEW) ggBangToggle(A, 'ka1');      /* ka1 = ok:null(안 품) */
    await wait(40);
    const c1 = document.getElementById('gg-chip-' + A + '-ka1');
    T('G3 안 품 + 켜짐은 빨간 글자·흰 바탕', !!(c1 && c1.classList.contains('ggnum-on') && c1.classList.contains('ggnum-on-n')),
      c1 ? c1.className : 'none');
  } catch (e) { T('G3', false, e.message); }

  /* ══════════ G4 정리 창 근거 목록 「! N」 ══════════ */
  try {
    resetLS(SEED()); loadQuiz(); closeWins(); showHome();
    if (NEW) { ggBangToggle(A, 'ka1'); ggBangToggle(A, 'ka2'); ggBangToggle(C, 'kc1'); }   /* 켜짐 3 · 두 단원 */
    setSearchMode('m');
    onCountClick();
    await wait(60);
    const box = document.getElementById('search-results');
    const txt = () => box.textContent.replace(/\s+/g, ' ');
    V('G4.headA', txt().slice(0, 160));
    T('G4 머리줄에 「! 3」', txt().indexOf('! 3') >= 0, txt().slice(0, 200));
    const chips = () => [...box.querySelectorAll('.ggcnt')].map(e => e.textContent.trim());
    V('G4.chipsA', chips());
    T('G4 단원 칩 ! 2 · ! 1', chips().sort().join(',') === ['! 1', '! 2'].sort().join(','), chips().join(','));
    const groupsA = box.querySelectorAll('button[onclick^="showFieldList"]').length;
    V('G4.groupsA', groupsA);

    const hd = box.querySelector('.ggbanghd');
    T('G4 「! N」 이 단추다', !!(hd && !hd.classList.contains('off')), hd ? hd.className : 'none');
    if (hd) hd.click();
    await wait(60);
    V('G4.headB', txt().slice(0, 200));
    const groupsB = box.querySelectorAll('button[onclick^="showFieldList"]').length;
    T('G4 눌렀더니 켜진 단원만', groupsA === 3 && groupsB === 2, 'A=' + groupsA + ' B=' + groupsB + ' (바람 A=3 B=2)');
    T('G4 상태 B 머리줄 문구', txt().indexOf('켜진 근거만 보는 중') >= 0, txt().slice(0, 200));
    T('G4 상태 B 는 「N건」 칩이 없다', chips().every(t => t.indexOf('!') === 0) && !/\d건<\/span>/.test(box.innerHTML.replace(/[\s\S]*?개 단원/, '')),
      chips().join(','));

    /* 펴면 켜진 근거만 */
    const gbtn = box.querySelector('button[onclick^="showFieldList"]');
    if (gbtn) gbtn.click();
    await wait(60);
    V('G4.listB', txt().slice(0, 240));
    T('G4 펴면 켜진 근거만', txt().indexOf('A 근거 셋') < 0 && txt().indexOf('A 근거 하나') >= 0, txt().slice(0, 240));
    T('G4 켜진 근거만 표시가 보인다', txt().indexOf('켜진 근거만') >= 0, txt().slice(0, 240));

    showFieldDistribution('m');
    await wait(40);
    const hd2 = box.querySelector('.ggbanghd');
    if (hd2) hd2.click(); else { const s = [...box.querySelectorAll('span')].find(e => /전체 .*건으로/.test(e.textContent)); if (s) s.click(); }
    await wait(60);
    const groupsA2 = box.querySelectorAll('button[onclick^="showFieldList"]').length;
    T('G4 다시 누르면 원상', groupsA2 === groupsA, 'A=' + groupsA + ' A2=' + groupsA2);

    /* 「문제」 모드로 가면 B 해제 */
    const hd3 = box.querySelector('.ggbanghd');
    if (hd3) hd3.click();
    await wait(50);
    setSearchMode('q');
    await wait(30);
    setSearchMode('m');
    onCountClick();
    await wait(60);
    T('G4 「문제」 모드로 가면 B 해제',
      box.querySelectorAll('button[onclick^="showFieldList"]').length === groupsA, txt().slice(0, 160));

    /* 켜진 게 0 이면 회색·못 누름 */
    resetLS(SEED()); loadQuiz();
    setSearchMode('m'); onCountClick();
    await wait(60);
    const hd0 = box.querySelector('.ggbanghd');
    T('G4 켜진 게 0 이면 회색·못 누름', !!(hd0 && hd0.classList.contains('off') && !hd0.getAttribute('onclick')),
      hd0 ? hd0.className + ' / ' + hd0.getAttribute('onclick') : 'none');
    T('G4 켜진 게 0 이면 「! 0」', !!(hd0 && hd0.textContent.trim() === '! 0'), hd0 ? hd0.textContent : 'none');
  } catch (e) { T('G4', false, e.message); }

  /* ══════════ G5 무변 — 옛 길 회귀 ══════════ */
  try {
    resetLS(SEED()); loadQuiz(); closeWins(); showHome();
    openQuiz([A]);
    await wait(50);
    V('G5.limits', [typeof GG_TMAX !== 'undefined' ? GG_TMAX : null,
                    typeof GG_CMAX !== 'undefined' ? GG_CMAX : null,
                    typeof GG_CN !== 'undefined' ? GG_CN : null]);
    T('G5 근거 한도 무변', GG_TMAX === 4000 && GG_CMAX === 2000 && GG_CN === 20,
      [GG_TMAX, GG_CMAX, GG_CN].join(','));
    /* 고치기 */
    ggEdit(A, 'ka1');
    const ein = document.getElementById('gg-ein-' + A + '-ka1');
    if (ein) { ein.value = 'A 근거 하나 고침'; ggEditSave(A, 'ka1'); }
    await wait(40);
    T('G5 ggEditSave 그대로', ((GG()[A] || []).find(x => x.k === 'ka1') || {}).t === 'A 근거 하나 고침',
      JSON.stringify(GG()[A]));
    /* 댓글 */
    const cin = document.getElementById('gg-cin-' + A + '-ka1');
    if (cin) { cin.value = '댓글 하나'; ggReply(A, 'ka1'); }
    await wait(40);
    const g1 = (GG()[A] || []).find(x => x.k === 'ka1') || {};
    T('G5 ggReply 그대로', Array.isArray(g1.cs) && g1.cs.length === 1 && g1.cs[0].t === '댓글 하나',
      JSON.stringify(g1.cs));
    /* 켜 둔 근거를 지워도 나머지가 멀쩡 */
    if (NEW) ggBangToggle(A, 'ka2');
    ggDel(A, 'ka2');
    await wait(40);
    if (typeof ggDelGo === 'function') ggDelGo(A, 'ka2', '');
    await wait(40);
    const left = GG()[A] || [];
    T('G5 ggDel 그대로(번호 다시 매김)', left.length === 2 && left.map(x => x.i).join(',') === '1,2',
      JSON.stringify(left.map(x => [x.k, x.i, !!x.bang])));
    T('G5 지운 항목의 bang 도 같이 사라진다', !left.some(x => x.k === 'ka2'), JSON.stringify(left));
    T('G5 ggRecalcAfterDelete 가 있다', typeof ggRecalcAfterDelete === 'function', typeof ggRecalcAfterDelete);
  } catch (e) { T('G5', false, e.message); }

  /* ══════════ G7 §C-2 받아 둔 것 지우기 ══════════ */
  try {
    resetLS(SEED()); loadQuiz(); closeWins(); showHome();
    const btn = [...document.querySelectorAll('button')].find(b => /받아 둔 교재·시험지 지우기/.test(b.textContent));
    T('G7 단추가 있다', !!btn, 'none');
    if (btn) {
      const row = btn.parentElement;
      T('G7 단추가 「🔄 기록 동기화」 줄 안', /기록 동기화/.test(row.textContent), row.textContent.slice(0, 80));
      T('G7 「📂 저장폴더 지정」 앞', !!(btn.nextElementSibling && btn.nextElementSibling.id === 'pick-folder-btn'),
        btn.nextElementSibling ? btn.nextElementSibling.id : 'none');
    }
    if (NEW && typeof mbForgetPrompt === 'function') {
      /* 비었을 때 */
      window.__CONFIRMS.length = 0;
      await mbForgetPrompt();
      T('G7 비었으면 묻지 않는다', window.__CONFIRMS.length === 0, JSON.stringify(window.__CONFIRMS));
      /* 꾸며 둔다 — 교재 3 · 시험지 2 · 색인 1 */
      const buf = n => new ArrayBuffer(n);
      await dbPut('bookpdf:minbeop7_1', { pdfMd5: 'x', buf: buf(3000000), at: 1 });
      await dbPut('bookpdf:minbeop7_2', { pdfMd5: 'x', buf: buf(2000000), at: 1 });
      await dbPut('bookpdf:minbeop9', { pdfMd5: 'x', buf: buf(1000000), at: 1 });
      await dbPut('gichulpdf:2024-1-minbeop.pdf:aaaaaaaaaaaa', { hash: 'a', buf: buf(500000), at: 1 });
      await dbPut('gichulpdf:2025-1-minbeop.pdf:bbbbbbbbbbbb', { hash: 'b', buf: buf(500000), at: 1 });
      await dbPut('gichulidx:2024-1-minbeop.pdf:aaaaaaaaaaaa', { no: { 1: { p: 1 } }, lines: [1] });
      await dbPut('ink:q:' + A, { keep: 1 });
      const lsBefore = JSON.stringify(Object.keys(localStorage).sort().map(k => [k, localStorage.getItem(k)]));

      /* 취소 */
      window.__CONFIRMS.length = 0; window.__CONFIRM_ANS = false;
      await mbForgetPrompt();
      V('G7.confirm', window.__CONFIRMS[0] || '');
      T('G7 confirm 에 「교재 3권 · 시험지 2장」',
        /교재 3권/.test(window.__CONFIRMS[0] || '') && /시험지 2장/.test(window.__CONFIRMS[0] || ''),
        window.__CONFIRMS[0] || 'none');
      T('G7 confirm 에 대략 MB', /약 [\d.]+ MB/.test(window.__CONFIRMS[0] || ''), window.__CONFIRMS[0] || '');
      const stillB = await dbGet('bookpdf:minbeop9');
      T('G7 취소하면 무변', !!(stillB && stillB.buf && stillB.buf.byteLength === 1000000),
        JSON.stringify(stillB && stillB.buf && stillB.buf.byteLength));

      /* 확인 */
      window.__CONFIRMS.length = 0; window.__CONFIRM_ANS = true;
      await mbForgetPrompt();
      await until(async () => { const v = await dbGet('bookpdf:minbeop9'); return !(v && v.buf); }, 100);
      const gone = [];
      for (const k of ['bookpdf:minbeop7_1', 'bookpdf:minbeop7_2', 'bookpdf:minbeop9',
                       'gichulpdf:2024-1-minbeop.pdf:aaaaaaaaaaaa', 'gichulpdf:2025-1-minbeop.pdf:bbbbbbbbbbbb']) {
        const v = await dbGet(k);
        gone.push(!(v && v.buf && v.buf.byteLength));
      }
      T('G7 다섯이 다 사라졌다', gone.every(Boolean), JSON.stringify(gone));
      const idx = await dbGet('gichulidx:2024-1-minbeop.pdf:aaaaaaaaaaaa');
      T('G7 색인(gichulidx:)은 무변', !!(idx && idx.no), JSON.stringify(idx && Object.keys(idx)));
      const ink = await dbGet('ink:q:' + A);
      T('G7 필기(ink:)는 무변', !!(ink && ink.keep === 1), JSON.stringify(ink));
      T('G7 기록(ox_*)은 무변',
        JSON.stringify(Object.keys(localStorage).sort().map(k => [k, localStorage.getItem(k)])) === lsBefore, '');
    } else {
      T('G7 mbForgetPrompt 가 있다', false, 'mbForgetPrompt 없음(옛 판)');
    }
  } catch (e) { T('G7', false, e.message); }

  try {
    V('SRC.ggBangToggle', typeof ggBangToggle);
    V('SRC.mbForgetPrompt', typeof mbForgetPrompt);
    V('SRC.dbKeys', typeof dbKeys);
    V('ERR', (window.__ERR || []).slice(0, 8));
    T('창에 자바스크립트 오류 0', (window.__ERR || []).length === 0, JSON.stringify((window.__ERR || []).slice(0, 5)));
  } catch (e) { }

  for (const l of R) console.log('HZR|' + encodeURIComponent(l));
  console.log('HZR|' + encodeURIComponent('END'));
}
main();
})();
