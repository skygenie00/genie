window.onload = null;
(function () {
const P = __P__;
const R = [];
const T = (n, c, i) => R.push((c ? 'PASS' : 'FAIL') + ' | ' + n + ((i !== undefined && !c) ? ' | ' + String(i).replace(/\n/g, '⏎').slice(0, 600) : ''));
const V = (k, v) => R.push('VAL | ' + k + ' | ' + JSON.stringify(v));
const say = s => R.push('INFO | ' + String(s).replace(/\n/g, '⏎').slice(0, 900));
const wait = ms => new Promise(r => setTimeout(r, ms));
const until = async (f, n) => { for (let i = 0; i < (n || 300); i++) { try { if (f()) return true; } catch (e) { } await wait(30); } try { return !!f(); } catch (e) { return false; } };

/* 새 판인가 — 옛 판(HEAD)에서는 아래 게이트가 「없음」으로 갈린다(헛잣대) */
const NEW = !!(window.oxCoord && typeof window.oxCoord.resolveSlot === 'function');
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
const A = P.a, B = P.b, C = P.c;          /* A = 자리 원본 · B = 가져오는 쪽 · C = 여벌 */
const CO = () => { try { return JSON.parse(localStorage.getItem('ox_q_coords') || '{}'); } catch (e) { return {}; } };
const J = o => JSON.stringify(o);
/* mbbListHTML 은 교재 그룹이 비면 일찍 돌아간다 — 정리OMR 절을 재려면 그룹 하나가 있어야 한다 */
const GROUPS = () => [{ vol: 'h', top: { doc: '__harness__', p: 1, snip: '가짜 교재 줄' },
                        rest: [], all: [{ doc: '__harness__', p: 1, snip: '가짜 교재 줄' }] }];

/* 자리 씨앗 — A 에 정리OMR 자리 하나(kA) · 교재 자리 하나(kBook) */
const KA = 'co_' + A + '_seedomr', KBOOK = 'co_' + A + '_seedbook';
const RA = [0.10, 0.20, 0.50, 0.30], RB = [0.12, 0.60, 0.55, 0.72];
const BOOKDOC = P.bookDoc || '';
const seedCoords = () => {
  const o = {};
  o[A] = [{ k: KA, doc: 'minbeopOMR', page: 3, r: RA.slice(), num: '12', fp: 'fpA', pad: null, hash: '', ts: 1, label: 'A 정리OMR 자리' }];
  if (BOOKDOC) o[A].push({ k: KBOOK, doc: BOOKDOC, page: 7, r: RB.slice(), num: '', fp: '', pad: null, hash: '', ts: 2, label: '' });
  localStorage.setItem('ox_q_coords', J(o));
  return o;
};

(async function () {
  try {
    say('판 = ' + (NEW ? 'NEW' : 'HEAD(헛잣대)') + ' · A=' + A + ' B=' + B + ' bookDoc=' + (BOOKDOC || '(없음)'));
    resetLS(); loadQuiz();
    await until(() => window.oxCoord && window.mbBook, 200);

    /* ════════ E-9 새 키 0 · SYNC_KEYS 무변 ════════ */
    V('syncKeys', P.syncKeys);
    T('E-9 SYNC_KEYS 에 ox_q_coords·ox_q_geunge·ox_chap_history 가 그대로 있다',
      ['ox_q_coords', 'ox_q_geunge', 'ox_chap_history'].every(k => P.syncKeys.indexOf(k) >= 0), P.syncKeys);

    /* ════════ E-8 옛 꼴 좌표(객체꼴) 도 읽힌다 ════════ */
    {
      const o = {}; o[C] = { doc: 'minbeopOMR', page: 2, r: [0.2, 0.2, 0.4, 0.4] };   /* 배열 아님 = 옛 꼴 */
      localStorage.setItem('ox_q_coords', J(o));
      const arr = window.oxCoord.coordsOf(C);
      const raw = CO();
      T('E-8 옛 꼴 객체 좌표가 배열로 읽히고, 저장값은 그대로(일괄 변환 0)',
        arr.length === 1 && arr[0].k === ('co_legacy_' + C) && !Array.isArray(raw[C]),
        [arr.length, arr[0] && arr[0].k, Array.isArray(raw[C])]);
      if (NEW) {
        const rs = window.oxCoord.resolveSlot(arr[0]);
        T('E-8 ref 없는 자리는 resolveSlot 이 그대로 돌려준다', rs === arr[0] || J(rs.r) === J(arr[0].r), J(rs && rs.r));
      }
    }

    /* ════════ E-3 ② ref 저장·따라오기·삭제 ════════ */
    seedCoords();
    const mkRef = () => {
      /* refAdopt 가 하는 저장을 같은 꼴로 — 앱 안 함수는 뷰어가 있어야 부를 수 있어 저장 결과를 잰다 */
      const o = CO();
      const src = o[A].find(x => x.k === KA);
      o[B] = [{ k: 'co_' + B + '_ref1', doc: src.doc, page: src.page, r: src.r.slice(),
                num: src.num, fp: src.fp, pad: src.pad, hash: src.hash, ts: 9, label: '',
                ref: { qid: A, k: KA } }];
      localStorage.setItem('ox_q_coords', J(o));
      return o;
    };
    {
      const before = J(CO()[A]);
      mkRef();
      const after = J(CO()[A]);
      T('E-3 ref 를 담아도 원본 문항(A) 배열은 바이트 동일', before === after, [before.slice(0, 80), after.slice(0, 80)]);
      if (NEW) {
        /* A 가 「위치 다시 지정」 → B 가 따라온다 */
        const o = CO();
        const moved = [0.30, 0.31, 0.62, 0.44];
        o[A] = o[A].map(x => x.k === KA ? Object.assign({}, x, { r: moved.slice(), page: 5 }) : x);
        localStorage.setItem('ox_q_coords', J(o));
        const b = window.oxCoord.coordsOf(B)[0];
        const rs = window.oxCoord.resolveSlot(b);
        T('E-3 A 가 자리를 옮기면 B 의 ref 자리도 따라온다(복사값은 옛 r 그대로)',
          J(rs.r) === J(moved) && rs.page === 5 && J(b.r) === J(RA),
          [J(rs.r), rs.page, J(b.r)]);
        /* A 에서 그 자리를 지우면 B 는 복사값으로 */
        const o2 = CO();
        o2[A] = o2[A].filter(x => x.k !== KA);
        localStorage.setItem('ox_q_coords', J(o2));
        const rs2 = window.oxCoord.resolveSlot(window.oxCoord.coordsOf(B)[0]);
        T('E-3 A 에서 원본 자리를 지우면 B 는 복사해 둔 r 로 그린다',
          J(rs2.r) === J(RA) && rs2.page === 3, [J(rs2.r), rs2.page]);
        /* B 에서 지워도 A 무변 */
        const o3 = CO();
        const aBefore = J(o3[A]);
        delete o3[B];
        localStorage.setItem('ox_q_coords', J(o3));
        T('E-3 B 에서 지워도 A 는 무변', J(CO()[A]) === aBefore, [J(CO()[A]).slice(0, 80)]);
      }
    }

    /* ════════ E-5 옛 판이 ref 든 값에서 안 깨진다 ════════ */
    {
      seedCoords(); mkRef();
      let err0 = (window.__ERR || []).length;
      const arr = window.oxCoord.coordsOf(B);
      const ok = Array.isArray(arr) && arr.length === 1 && arr[0].r && arr[0].r.length === 4;
      const flat = (window.oxCoord.coords && window.oxCoord.coords()) || {};
      T('E-5 ref 든 값을 읽어도 좌표 읽기가 깨지지 않는다(옛 판 포함 · 복사값 r 로 그린다)',
        ok && (window.__ERR || []).length === err0 && !!flat[B], [arr.length, (window.__ERR || []).length - err0]);
      V('E-5 ref 자리 r', arr[0] && arr[0].r);
    }

    /* ════════ E-2 ① 「찍어 둔 자리」 줄 아래 그림 ════════ */
    if (NEW && window.mbBook && typeof window.mbBook.listHTML === 'function') {
      seedCoords();
      const html = window.mbBook.listHTML(A, GROUPS(), []);          /* 교재 그룹 없음 → 정리OMR 갈래만 */
      const d = document.createElement('div'); d.innerHTML = html;
      const pics = d.querySelectorAll('[data-mbbpic]');
      T('E-2 정리OMR 「찍어 둔 자리」 줄 아래 그림 칸 1', pics.length === 1, pics.length);
      T('E-2 「후보」 줄·핀 없는 재료엔 그림 칸이 안 붙는다',
        d.innerHTML.indexOf('후보') < 0 || pics.length === 1, pics.length);
      /* 핀이 없으면 그림 칸 0 */
      localStorage.setItem('ox_q_coords', '{}');
      const d2 = document.createElement('div');
      d2.innerHTML = window.mbBook.listHTML(A, GROUPS(), [{ p: 1, snip: '가짜 후보', rank: 1 }]);
      T('E-2 핀이 없으면(후보만) 그림 칸 0', d2.querySelectorAll('[data-mbbpic]').length === 0,
        d2.querySelectorAll('[data-mbbpic]').length);
      /* 그림 채우기 — 자산이 없는 기기라 문구가 떠야 한다.
         ⚠ crop → getAsset → window.dbGet → IndexedDB 인데 **가상 시계는 IDB 콜백을 안 돌린다**.
            재려는 상태가 바로 「자산 없는 기기」라 dbGet 을 null 즉답으로 흉내 낸다(앱 코드 무접촉). */
      const _dbGet = window.dbGet;
      window.dbGet = function () { return Promise.resolve(null); };
      seedCoords();
      const host = document.createElement('div');
      host.innerHTML = window.mbBook.listHTML(A, GROUPS(), []);
      document.body.appendChild(host);
      window.mbBook.picFill(host);
      await until(() => (host.querySelector('.mbbpic-img') || {}).innerHTML &&
                        (host.querySelector('.mbbpic-img').innerHTML.indexOf('여는 중') < 0), 260);
      const inner = (host.querySelector('.mbbpic-img') || {}).innerHTML || '';
      T('E-2 자산이 없는 기기 = 「이 기기에 그림이 아직 없습니다」 한 줄',
        inner.indexOf('이 기기에 그림이 아직 없습니다') >= 0, inner.slice(0, 120));
      /* 저장 무변 */
      T('E-2 그림을 그려도 ox_q_coords 무변', J(CO()) === J(seedCoords()), J(CO()).slice(0, 90));
      T('E-2 암기카드(ox_mem_cards) 무접촉', localStorage.getItem('ox_mem_cards') === null,
        localStorage.getItem('ox_mem_cards'));
      /* ref 면 🔗 칩 */
      mkRef();
      const d3 = document.createElement('div');
      d3.innerHTML = window.mbBook.listHTML(B, GROUPS(), []);
      T('E-2/A-6 ref 자리면 🔗 칩이 붙는다', d3.innerHTML.indexOf('🔗') >= 0 && d3.innerHTML.indexOf('자리</span>') >= 0,
        d3.innerHTML.slice(0, 200));
      /* 자리 둘이면 「자리 1 / 2 ▶」 */
      {
        const o = CO();
        o[A].push({ k: 'co_' + A + '_second', doc: 'minbeopOMR', page: 4, r: [0.3, 0.3, 0.6, 0.5], ts: 3, label: '' });
        localStorage.setItem('ox_q_coords', J(o));
        const d4 = document.createElement('div');
        d4.innerHTML = window.mbBook.listHTML(A, GROUPS(), []);
        T('E-2/A-4 자리가 둘이면 「자리 1 / 2 ▶」 칩', d4.innerHTML.indexOf('자리 1 / 2 ▶') >= 0,
          (d4.querySelector('.mbbpic-chip') || {}).textContent);
      }
      host.remove();
      window.dbGet = _dbGet;
      /* 정리OMR 줄이 좌표를 제대로 넘기는가(9/18 에 고친 자리) */
      seedCoords();
      const d5 = document.createElement('div');
      d5.innerHTML = window.mbBook.listHTML(A, GROUPS(), []);
      const go = (d5.innerHTML.match(/mbOmrGo\(([^)]*)\)/) || [])[1] || '';
      T('E-2(덤) 정리OMR 「찍어 둔 자리」 줄이 x/y/w/h 를 넘긴다(옛 판은 전부 null 이었다)',
        go.split(',').length === 5 && go.indexOf('null') < 0, go);
      V('mbOmrGo 인자', go);
    } else if (!NEW) {
      T('E-2 (헛잣대) 옛 판엔 그림 칸이 없다', !(window.mbBook && window.mbBook.listHTML), 'listHTML 없음');
    }

    /* ════════ E-6 ③④ 댓글 지우기 · 🔗 제거 ════════ */
    {
      /* ⚠ 이름을 글자 그대로 쓰면 **하네스 제 코드**가 걸린다 — 이어 붙여 만든다 */
      const NEEDLE = 'ggCs' + 'Link';
      const src = document.documentElement.innerHTML;
      const hits = src.split(NEEDLE).length - 1;
      T('E-6/C-1 페이지 전체에서 그 함수 이름 0회(하네스 제 글자는 뺀다)',
        hits <= 1, [hits, src.indexOf(NEEDLE)]);
      const gg = {};
      gg[A] = [{ k: 'kg1', i: 1, t: 'A 근거', ok: null, ts: 1,
                 cs: [{ k: 'c1', t: '댓글 하나', ts: 11 }, { k: 'c2', t: '댓글 둘', ts: 12 }, { k: 'c3', t: '댓글 셋', ts: 13 }] }];
      for (const sc of ['', 'qp-', 'jn-']) {
        resetLS({ ox_q_geunge: gg }); loadQuiz();
        const box = document.createElement('div');
        box.innerHTML = ggLineHTML(A, sc);
        document.body.appendChild(box);
        const rows = box.querySelectorAll('[data-ck]');
        T('E-6 [' + (sc || '카드') + '] 댓글 줄마다 data-ck · 지우기 단추 3', rows.length === 3 &&
          box.querySelectorAll('button[onclick="ggCsDel(this)"]').length === 3,
          [rows.length, box.querySelectorAll('button[onclick="ggCsDel(this)"]').length]);
        T('E-6 [' + (sc || '카드') + '] 댓글 줄에 🔗 0',
          (box.innerHTML.match(/🔗/g) || []).length === 0, (box.innerHTML.match(/🔗/g) || []).length);
        ggCsDelGo(A, 'kg1', 'c2', sc);
        const g2 = (JSON.parse(localStorage.getItem('ox_q_geunge') || '{}')[A] || [])[0] || {};
        T('E-6 [' + (sc || '카드') + '] 가운데 댓글 하나만 빠진다 · 나머지 k·t 무변',
          (g2.cs || []).length === 2 && g2.cs[0].k === 'c1' && g2.cs[1].k === 'c3' &&
          g2.cs[0].t === '댓글 하나' && g2.cs[1].t === '댓글 셋' && g2.t === 'A 근거' && g2.k === 'kg1',
          J(g2));
        box.remove(); closeWins();
      }
    }

    /* ════════ E-7 ⑤ 「이번 (N회독)」 ════════ */
    {
      const mk = (n) => {
        const h = {}; const key = '||||||';
        return h;
      };
      /* 픽스처: currentSubject·Label·필터가 chapKey 를 만든다 */
      resetLS(); loadQuiz();
      const ids = P.rows.slice(0, 3).map(r => r.uid);
      const items = ids.map(id => quizData.find(q => q.id === id)).filter(Boolean);
      currentSubject = '민법'; currentChapterLabel = '하네스장';
      document.getElementById('source-filter').value = '';
      document.getElementById('review-filter').value = '';
      const sf = document.getElementById('source-filter').value, rf = document.getElementById('review-filter').value;
      const chapKey = currentSubject + '||' + currentChapterLabel + '||' + sf + '||' + rf;
      const results = items.map((it, i) => ({ item: it, isCorrect: i !== 1 }));
      const marks = {}; items.forEach((it, i) => { marks[it.id] = i !== 1; });

      /* (가) 중간 쪽 — 저장 안 됨 */
      chapterSaved = null;
      localStorage.setItem('ox_chap_history', J({}));
      let html = renderAttemptCompare(results);
      T('E-7 중간 쪽(저장 전) = 「이번 (1회독) · 채점중」',
        html.indexOf('이번 (1회독) · 채점중') >= 0, html.slice(0, 260));

      /* (나) 마지막 쪽 — 지난 회독 0 · 저장이 먼저 돈 뒤 */
      const h1 = {}; h1[chapKey] = [{ score: 2, total: 3, date: '9/18', marks: Object.assign({}, marks) }];
      localStorage.setItem('ox_chap_history', J(h1));
      chapterSaved = chapKey;
      html = renderAttemptCompare(results);
      T('E-7 마지막 쪽(지난 0) = 「이번 (1회독) · ✓ 저장됨」 · 지난 회독 줄 0',
        html.indexOf('이번 (1회독) · ✓ 저장됨') >= 0 && html.indexOf('1회독 · 2/3') < 0,
        html.slice(0, 320));
      T('E-7 ox_chap_history 길이 1(표시만 고쳤다 · 저장 무변)',
        (JSON.parse(localStorage.getItem('ox_chap_history'))[chapKey] || []).length === 1,
        (JSON.parse(localStorage.getItem('ox_chap_history'))[chapKey] || []).length);

      /* (다) 마지막 쪽 — 지난 회독 1 */
      const h2 = {}; h2[chapKey] = [
        { score: 1, total: 3, date: '9/17', marks: Object.assign({}, marks) },
        { score: 2, total: 3, date: '9/18', marks: Object.assign({}, marks) }];
      localStorage.setItem('ox_chap_history', J(h2));
      chapterSaved = chapKey;
      html = renderAttemptCompare(results);
      T('E-7 마지막 쪽(지난 1) = 「1회독 · 1/3」 한 줄 + 「이번 (2회독) · ✓ 저장됨」',
        html.indexOf('1회독 · 1/3') >= 0 && html.indexOf('이번 (2회독) · ✓ 저장됨') >= 0 &&
        html.indexOf('2회독 · 2/3') < 0, html.slice(0, 420));
      const rounds = (html.match(/회독 · \d+\/\d+/g) || []);
      T('E-7 같은 회독이 두 줄로 안 보인다(지난 회독 줄 1)', rounds.length === 1, rounds);

      /* (라) 중간 쪽인데 지난 회독 1 */
      chapterSaved = null;
      localStorage.setItem('ox_chap_history', J({ [chapKey]: [h2[chapKey][0]] }));
      html = renderAttemptCompare(results);
      T('E-7 중간 쪽(지난 1) = 「이번 (2회독) · 채점중」 그대로',
        html.indexOf('이번 (2회독) · 채점중') >= 0, html.slice(0, 260));
      chapterSaved = null;
    }

    V('JS 오류', (window.__ERR || []).slice(0, 6));
    T('오류 0', !(window.__ERR || []).length, (window.__ERR || []).slice(0, 6));
  } catch (e) {
    R.push('FAIL | 하네스가 죽었다 | ' + String(e && e.stack || e).slice(0, 700));
  }
  R.push('END');
  R.forEach(x => console.log('HZR|' + encodeURIComponent(x)));
})();
})();
