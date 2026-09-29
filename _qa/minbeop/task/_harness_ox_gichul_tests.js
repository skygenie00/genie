window.onload = null;
(function () {
const P = __P__;
const R = [];
const T = (n, c, i) => R.push((c ? 'PASS' : 'FAIL') + ' | ' + n + ((i !== undefined && !c) ? ' | ' + String(i).replace(/\n/g, '⏎').slice(0, 600) : ''));
const say = s => R.push('INFO | ' + String(s).replace(/\n/g, '⏎').slice(0, 900));
const V = (k, v) => R.push('VAL | ' + k + ' | ' + JSON.stringify(v));
const wait = ms => new Promise(r => setTimeout(r, ms));
/* IndexedDB·망은 가상 시계를 안 따른다 — 고정 대기 대신 조건을 기다린다 */
const until = async (f, n) => { for (let i = 0; i < (n || 400); i++) { try { if (f()) return true; } catch (e) { } await wait(30); } try { return !!f(); } catch (e) { return false; } };
const NEW = (typeof mbExam !== 'undefined');
const BASE = { 'ox_uid_migrated': '1', 'ox_gg_okreset': '1', 'ox_auto_important_v2': '1',
               'tt.cfg': JSON.stringify({ person: '하네스', token: 'harness-token' }) };
const resetLS = o => {
  localStorage.clear();
  for (const k in BASE) localStorage.setItem(k, BASE[k]);
  for (const k in (o || {})) localStorage.setItem(k, typeof o[k] === 'string' ? o[k] : JSON.stringify(o[k]));
  try { useIdxDrop(); } catch (e) { }
};
const loadQuiz = rows => { quizData.length = 0; buildQuizData(rows).forEach(q => quizData.push(q)); };
const closeWins = () => document.querySelectorAll('.oxwin').forEach(w => w.remove());

async function main() {
  resetLS();
  say('NEW=' + NEW + ' · rows=' + P.rows.length);

  /* ══════════ G2 — 기출 칩: 문 달림 · 회색 0 ══════════ */
  try {
    loadQuiz(P.rows);
    if (NEW) { await mbExam.list(); }
    const ids = P.chipIds.filter(id => quizData.some(q => q.id === id));
    currentSubject = ''; currentChapterLabel = ''; isExamMode = false; currentPageIndex = 0;
    currentSessionMarks = {}; resumePicks = {}; currentSessionScore = 0; lastGradeResults = null;
    currentFilteredData = ids.map(id => quizData.find(q => q.id === id));
    document.getElementById('home-screen').classList.add('hide');
    document.getElementById('quiz-screen').classList.remove('hide');
    renderQuizPage();
    await wait(60);
    const btns = [...document.querySelectorAll('#quiz-screen button[data-exam]')];
    const spans = [...document.querySelectorAll('#quiz-screen span')].filter(s => /^\d{4}:\d*:/.test(s.textContent || ''));
    T('G2 칩이 button 이다', btns.length > 0, 'button ' + btns.length + ' · 옛 span ' + spans.length);
    const gray = btns.filter(b => /opacity\s*:\s*\.?4?5?/.test(b.getAttribute('style') || ''));
    T('G2 회색 칩 0개', gray.length === 0, '회색 ' + gray.length + ' = ' + gray.slice(0, 6).map(b => b.textContent).join(','));
    V('G2.btns', btns.length); V('G2.gray', gray.length);
    /* 마스터 전 연도가 목록에 있는가 */
    if (NEW) {
      const bad = P.years.filter(y => !mbExamHasYear(y));
      T('G2 마스터 전 연도가 list.json 에 있다', bad.length === 0, '없는 해 ' + JSON.stringify(bad));
    } else {
      T('G2 마스터 전 연도가 list.json 에 있다', false, 'mbExamHasYear 없음(옛 판)');
    }
    /* 칩마다 제 examMeta[idx] */
    const multi = btns.filter(b => (b.getAttribute('data-exam') || '').endsWith(':1'));
    T('G2 칩마다 제 idx', multi.length > 0, '두 번째 칩 ' + multi.length + '개');
  } catch (e) { T('G2 돌아감', false, e.message); }

  /* ══════════ G3·G4 — 문번 색인 ══════════ */
  for (const f of P.files) {
    try {
      if (!NEW) { T('G' + (f === '2024-1-minbeop.pdf' ? '3' : '4') + ' ' + f + ' 색인', false, 'mbExam 없음(옛 판)'); continue; }
      const rec = await mbExam.index(f);
      const g = (f === '2024-1-minbeop.pdf') ? 'G3' : 'G4';
      T(g + ' ' + f + ' 1~40 각 한 번', rec.miss.length === 0, '못 짚음 ' + JSON.stringify(rec.miss));
      V('idx.' + f, { pages: rec.pages, miss: rec.miss, lines: rec.lines.length });
      const pg = {}; for (let n = 1; n <= 40; n++) if (rec.no[n]) pg[n] = rec.no[n].p;
      V('page.' + f, pg);
    } catch (e) { T('G3/G4 ' + f, false, e.message); }
  }

  /* G3 상세 — 2024 35번 ③ */
  try {
    if (NEW) {
      const f = '2024-1-minbeop.pdf';
      const rec = await mbExam.index(f);
      const bx = mbExam.box(rec, 35);
      T('G3 35번 덩이 상자', !!bx, String(bx));
      if (bx) {
        V('G3.35.page', bx.page);
        V('G3.35.box', { x0: +bx.box.x0.toFixed(4), y0: +bx.box.y0.toFixed(4), x1: +bx.box.x1.toFixed(4), y1: +bx.box.y1.toFixed(4) });
        const bn = mbExam.band(bx.body, 3, '③');
        T('G3 ③ 띠를 찾았다', !!bn, 'band=' + JSON.stringify(bn));
        const lines = bx.body.map(L => L.t);
        const i3 = lines.findIndex(t => t.replace(/^\s+/, '').indexOf('③') === 0);
        const txt3 = i3 >= 0 ? lines.slice(i3).join('') : '';
        const key = P.g3key;
        T('G3 ③ 줄에 「' + key + '」', txt3.replace(/\s/g, '').indexOf(key.replace(/\s/g, '')) >= 0,
          '③줄=' + txt3.slice(0, 160));
        V('G3.35.opt3', txt3.slice(0, 200));
        /* 띠가 덩이 안에 든다 */
        if (bn) T('G3 띠가 덩이 안', bn.y0 >= bx.box.y0 - 1e-6 && bn.y1 <= bx.box.y1 + 1e-6,
                  JSON.stringify([bx.box.y0, bn.y0, bn.y1, bx.box.y1]));
      }
    }
  } catch (e) { T('G3 상세', false, e.message); }

  /* ══════════ G5 — 교재 무변: 테두리 계산 결과 ══════════ */
  try {
    resetLS();
    loadQuiz(P.rows);
    for (const s of P.border) {
      let out = 'ERR';
      try {
        const w = await mbBook.words(s.docid, s.p);
        const items = await mbBook.items({ _p: { words: w.words } });
        const bd = mbBook.border(s.uid, items);
        out = bd && bd.ok
          ? [bd.ok, bd.anchor, bd.tall ? 1 : 0, bd.both ? 1 : 0, bd.nq, bd.nh,
             bd.box.x0.toFixed(5), bd.box.y0.toFixed(5), bd.box.x1.toFixed(5), bd.box.y1.toFixed(5),
             (bd.pitch || 0).toFixed(5)].join('/')
          : 'no:' + (bd && bd.why);
      } catch (e) { out = 'ERR:' + e.message; }
      V('G5.border.' + s.uid + '@' + s.docid + 'p' + s.p, out);
    }
    T('G5 표본을 다 쟀다', true, '');
  } catch (e) { T('G5', false, e.message); }

  /* ══════════ G6 — 교재 팝업 쪽 입력 ══════════ */
  try {
    if (!NEW) { T('G6 쪽 이동', false, 'mbExam 없음(옛 판)'); }
    else {
      for (const c of P.nav) {
        let got = null;
        try {
          got = c.kind === 'print' ? await mbExam.findPrint(c.docid, c.v)
                                   : await mbExam.stepDoc(c.docid, c.p, c.dir);
        } catch (e) { got = 'ERR:' + e.message; }
        const g = got ? (got.docid + ':' + got.p) : 'null';
        T('G6 ' + c.name, g === c.want, '얻음 ' + g + ' · 바람 ' + c.want);
        V('G6.' + c.name, g);
      }
      /* 권 차례 */
      V('G6.chain', mbExam.chain('minbeop7_1').join(','));
      T('G6 7판이 두 권으로 이어진다', mbExam.chain('minbeop7_1').length === 2, mbExam.chain('minbeop7_1').join(','));
    }
  } catch (e) { T('G6', false, e.message); }

  /* ══════════ G8 — §E 근거 지울 때 걸린 문항 ══════════ */
  try {
    closeWins();
    const GG = {};
    GG[P.e.owner] = [{ k: 'k_h1', i: 1, t: '근거 첫째 줄\n둘째 줄', ts: 1 },
                     { k: 'k_h2', i: 2, t: '근거 둘째', ts: 2 }];
    GG[P.e.solo] = [{ k: 'k_s1', i: 1, t: '혼자 근거', ts: 1 }];
    const RL = {}; RL[P.e.a] = { geunge: [P.e.owner] }; RL[P.e.b] = { geunge: [P.e.owner] };
    resetLS({ ox_q_geunge: GG, ox_q_reflinks: RL });
    loadQuiz(P.rows);
    const before = localStorage.getItem('ox_q_reflinks');

    /* (1) 걸린 문항 2개 */
    ggDel(P.e.owner, 'k_h2', '');
    await wait(40);
    const w1 = document.getElementById('oxwin-ggdel-' + P.e.owner + '-k_h2');
    T('G8 확인 창이 떴다(confirm 아님)', !!w1, 'win=' + !!w1);
    const txt1 = w1 ? w1.textContent : '';
    T('G8 「걸린 문항 2개」', txt1.indexOf('걸린 문항 2개') >= 0, txt1.slice(0, 200));
    const rows = w1 ? [...w1.querySelectorAll('[data-ggowner]')] : [];
    T('G8 목록에 두 문항', rows.length === 2, rows.map(r => r.getAttribute('data-ggowner')).join(','));
    T('G8 목록이 걸린 문항이다', rows.map(r => r.getAttribute('data-ggowner')).sort().join(',') === [P.e.a, P.e.b].sort().join(','),
      rows.map(r => r.getAttribute('data-ggowner')).join(','));
    T('G8 마지막 근거가 아니면 ⚠ 줄 없음', !document.getElementById('ggdel-last-' + P.e.owner), 'last줄 있음');

    /* 줄을 누르면 그 문항 팝업 */
    let opened = '';
    const realOpen = window.openQPopup;
    window.openQPopup = function (id) { opened = id; return realOpen.apply(this, arguments); };
    if (rows[0]) rows[0].click();
    await wait(40);
    window.openQPopup = realOpen;
    T('G8 줄을 누르면 openQPopup', opened === rows[0].getAttribute('data-ggowner'), 'opened=' + opened);
    T('G8 확인 창은 그대로 있다', !!document.getElementById('oxwin-ggdel-' + P.e.owner + '-k_h2'), '사라짐');
    closeWins();

    /* (2) 마지막 근거 — ⚠ 줄 */
    ggSaveList(P.e.owner, [{ k: 'k_h1', i: 1, t: '근거 하나만', ts: 1 }]);
    ggDel(P.e.owner, 'k_h1', '');
    await wait(40);
    const w2 = document.getElementById('oxwin-ggdel-' + P.e.owner + '-k_h1');
    T('G8 마지막 근거면 ⚠ 줄', !!(w2 && document.getElementById('ggdel-last-' + P.e.owner)),
      w2 ? w2.textContent.slice(0, 200) : 'no win');
    closeWins();

    /* (3) 걸린 문항 0 — 옛 문장 그대로 */
    ggDel(P.e.solo, 'k_s1', '');
    await wait(40);
    const w3 = document.getElementById('oxwin-ggdel-' + P.e.solo + '-k_s1');
    const txt3 = w3 ? w3.textContent : '';
    T('G8 걸린 문항 0 이면 목록 없음', txt3.indexOf('걸린 문항') < 0, txt3.slice(0, 160));
    T('G8 걸린 문항 0 이어도 옛 문장', txt3.indexOf('근거 1 을(를) 지웁니다') >= 0, txt3.slice(0, 160));
    T('G8 본문 첫 줄만', txt3.indexOf('혼자 근거') >= 0, txt3.slice(0, 160));
    closeWins();

    /* (4) 지우기 뒤 — 근거는 줄고 연결은 바이트 무변 */
    ggSaveList(P.e.owner, [{ k: 'k_h1', i: 1, t: 'A', ts: 1 }, { k: 'k_h2', i: 2, t: 'B', ts: 2 }]);
    ggDel(P.e.owner, 'k_h1', '');
    await wait(30);
    ggDelGo(P.e.owner, 'k_h1', '');
    await wait(40);
    const left = ggOf(P.e.owner);
    T('G8 [지우기] 뒤 근거 1개', left.length === 1 && left[0].k === 'k_h2', JSON.stringify(left));
    T('G8 [지우기] 뒤 번호 다시 매김', left.length === 1 && left[0].i === 1, JSON.stringify(left));
    T('G8 ox_q_reflinks 바이트 무변', localStorage.getItem('ox_q_reflinks') === before,
      'before=' + before + ' after=' + localStorage.getItem('ox_q_reflinks'));
    T('G8 [지우기] 뒤 창이 닫힘', !document.getElementById('oxwin-ggdel-' + P.e.owner + '-k_h1'), '남아 있음');

    /* (5) 취소는 아무것도 안 한다 */
    const snap = localStorage.getItem('ox_q_geunge');
    ggDel(P.e.owner, 'k_h2', '');
    await wait(30);
    oxWinClose('ggdel-' + P.e.owner + '-k_h2');
    await wait(20);
    T('G8 취소는 무변', localStorage.getItem('ox_q_geunge') === snap, 'changed');
    closeWins();
  } catch (e) { T('G8', false, e.message); }

  /* ══════════ 소스 잣대 ══════════ */
  try {
    V('SRC.mbExam', typeof mbExam);
    V('SRC.ggDelGo', typeof ggDelGo);
    V('SRC.mbPageBody', typeof window.mbPageStep);
    V('NET.block', (window.__NET || []).filter(x => x.indexOf('BLOCK:') === 0).slice(0, 8));
    V('NET.gh', [...new Set((window.__NET || []).filter(x => x.indexOf('gh:') === 0))].slice(0, 8));
    V('ERR', (window.__ERR || []).slice(0, 8));
    V('CERR', (window.__CERR || []).filter(x => !/favicon|Failed to load resource/.test(x)).slice(0, 8));
    T('창에 자바스크립트 오류 0', (window.__ERR || []).length === 0, JSON.stringify((window.__ERR || []).slice(0, 5)));
  } catch (e) { }

  for (const l of R) console.log('HZR|' + encodeURIComponent(l));
  console.log('HZR|' + encodeURIComponent('END'));
}
main();
})();
