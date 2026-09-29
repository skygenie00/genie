/* _task_ox_cs_edit_usecount §H 하네스 — 브라우저 안 시험(단계마다 window.__HZT.<이름>() 을 CDP 가 부른다 · 결과는 JSON 글자) */
window.onload = null;   /* 앱 초기화(망·동기화)를 끈다 — 시험이 저장소·문항을 직접 싣는다 */
(function () {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const until = async (f, n) => { for (let i = 0; i < (n || 200); i++) { try { if (f()) return true; } catch (e) { } await wait(30); } try { return !!f(); } catch (e) { return false; } };
  const txt = n => (n ? n.textContent : '').replace(/\s+/g, ' ').trim();
  const H = window.__HZ = window.__HZ || {};
  const NEW = typeof window.ggCsEdit === 'function';
  const LS = k => localStorage.getItem(k);
  const oxwins = () => [...document.querySelectorAll('.oxwin')].map(w => w.id);
  const host = (id, css) => { let h = document.getElementById(id); if (!h) { h = document.createElement('div'); h.id = id; document.body.appendChild(h); } h.style.cssText = 'position:absolute;left:0;top:0;width:760px;background:#fff;z-index:9000;padding:10px;font-family:sans-serif;' + (css || ''); return h; };
  const unhide = (n, stop) => { while (n && n !== stop) { if (n.classList && n.classList.contains('hide')) n.classList.remove('hide'); n = n.parentElement; } };
  const key = (el, k, sh) => el.dispatchEvent(new KeyboardEvent('keydown', { key: k, shiftKey: !!sh, bubbles: true, cancelable: true }));

  window.__HZT = {
    /* ── 준비: 동기화 기록 파일의 저장소 전부 · 문항 5,548 · 가짜 정리OMR 자산(쪽 비움 → 자리표 그림) · 흉내 겹침 자리 둘 */
    setup: async function () {
      const R = { NEW: NEW };
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
      await dbPut('omrasset:minbeopOMR', { pages: new Array(60).fill(null) });
      /* 흉내 겹침 둘 — ⓐ Q5631 첫 자리와 같은 상자에 원본 자리 둘(Q0001·Q0002) ⓑ Q4311 둘째 자리와 같은 상자에 ref 하나(Q0003 → Q4311) */
      const co = JSON.parse(LS('ox_q_coords') || '{}');
      const s1 = (co.Q5631 || [])[0], s2 = (co.Q4311 || [])[1];
      R.seedA = !!s1; R.seedB = !!s2;
      if (s1) ['Q0001', 'Q0002'].forEach((q, i) => { co[q] = (co[q] || []).concat([{ k: 'co_' + q + '_hz' + i, doc: s1.doc, page: s1.page, r: s1.r.slice(), num: '', fp: '', pad: null, hash: '', ts: 1, label: '하네스 겹침' }]); });
      if (s2) co.Q0003 = (co.Q0003 || []).concat([{ k: 'co_Q0003_hzref', doc: s2.doc, page: s2.page, r: s2.r.slice(), num: '', fp: '', pad: null, hash: '', ts: 2, label: '', ref: { qid: 'Q4311', k: s2.k } }]);
      localStorage.setItem('ox_q_coords', JSON.stringify(co));
      H.co0 = LS('ox_q_coords');
      /* 옛 호출(useNumHTML 3인자) 출력 — 근거가 걸린 문항 20의 연결 칩 HTML(판마다 같아야 한다) */
      const owners = Object.keys(JSON.parse(LS('ox_q_reflinks') || '{}')).slice(0, 20);
      R.chips = owners.map(o => { try { return ggRefChipsHTML(o, '') + '§' + fieldRefChipsHTML(o); } catch (e) { return 'ERR ' + e; } }).join('\n');
      R.chipOwners = owners.length;
      return JSON.stringify(R);
    },

    /* ── §A 카드(범위 '') — 고치기 단추 · 편집 칸 · 빈 글 · Esc · Shift+Enter · Enter 저장 */
    a_card: async function () {
      const R = {};
      const st = JSON.parse(LS('ox_q_geunge') || '{}');
      let U = null, G = null;
      for (const u of Object.keys(st)) { for (const g of (st[u] || [])) { if (g && Array.isArray(g.cs) && g.cs.length && useOwners('geunge', u).length) { U = u; G = g; break; } } if (U) break; }
      R.U = U; if (!U) return JSON.stringify(R);
      H.U = U; H.GK = G.k; H.CK = String(G.cs[0].k || 0); H.T0 = G.cs[0].t; H.O = useOwners('geunge', U)[0];
      R.GK = H.GK; R.CK = H.CK; R.T0 = H.T0; R.O = H.O; R.owners = useOwners('geunge', U).length;
      const h = host('hz-card');
      h.innerHTML = ggLineHTML(U);
      const cs = document.getElementById('gg-cs-' + U + '-' + H.GK); R.csBox = !!cs;
      unhide(cs, h);
      const row = cs.querySelector('[data-ck]');
      R.btns = [...row.querySelectorAll(':scope>button')].map(b => b.textContent.trim() + '|' + (b.className.indexOf('ml-auto') >= 0 ? 'ml-auto' : '') + '|' + (b.className.match(/text-(blue|red)-\d+/) || [''])[0]);
      /* 「연결한 근거」 상자(범위 jn-) — 댓글 줄에 고치기 단추가 없어야 한다(A-4) */
      const jn = host('hz-jn', 'top:640px');
      jn.innerHTML = '<div id="jn-reflink-geunge-' + H.O + '">' + ggRefBoxHTML(H.O, 'jn-') + '</div>';
      R.jnHasEditBtn = jn.innerHTML.indexOf('ggCsEdit(') >= 0;
      R.jnHasT0 = jn.textContent.indexOf(H.T0.slice(0, 12)) >= 0;
      R.jnHasRefEdit = jn.innerHTML.indexOf('여기서 고치기') >= 0;
      return JSON.stringify(R);
    },
    a_card_open: async function () {
      const R = {}; const U = H.U;
      const row = document.getElementById('gg-cs-' + U + '-' + H.GK).querySelector('[data-ck]');
      H.before = LS('ox_q_geunge');
      row.querySelector(':scope>button').click();          /* 첫 단추 = 고치기 */
      await wait(60);
      const ta = row.querySelector('textarea');
      R.open = !!ta; R.val = ta && ta.value; R.id = ta && ta.id; R.rows = ta && ta.rows;
      R.cls = ta && ta.className; R.kids = [...row.children].map(x => x.tagName.toLowerCase() + (x.tagName === 'DIV' ? '[' + [...x.children].map(y => y.tagName.toLowerCase() + ':' + txt(y)).join(',') + ']' : ''));
      R.focus = document.activeElement === ta;
      R.maxOf = ta ? ggMaxOf(ta) : null; R.CMAX = typeof GG_CMAX !== 'undefined' ? GG_CMAX : null;
      return JSON.stringify(R);
    },
    a_card_rules: async function () {
      const R = {}; const U = H.U;
      const row = () => document.getElementById('gg-cs-' + U + '-' + H.GK).querySelector('[data-ck]');
      let ta = row().querySelector('textarea');
      /* 빈 글 저장 — 안 됨 · 칸 빨강 · 그대로 */
      ta.value = '   '; row().querySelector('textarea + button').click(); await wait(40);
      ta = row().querySelector('textarea');
      R.emptyKept = !!ta; R.emptyBorder = ta && getComputedStyle(ta).borderTopColor; R.emptyStore = LS('ox_q_geunge') === H.before;
      /* Shift+Enter — 저장 안 함 */
      ta.value = 'HZ 줄바꿈 시험'; key(ta, 'Enter', true); await wait(40);
      R.shiftKept = !!row().querySelector('textarea'); R.shiftStore = LS('ox_q_geunge') === H.before;
      /* Esc — 원문으로 · 저장 없음 */
      key(row().querySelector('textarea'), 'Escape'); await wait(40);
      R.escClosed = !row().querySelector('textarea'); R.escText = txt(row().querySelector('span.whitespace-pre-wrap')); R.escStore = LS('ox_q_geunge') === H.before;
      R.escBtns = [...row().querySelectorAll(':scope>button')].map(b => b.textContent.trim());
      return JSON.stringify(R);
    },
    a_card_save: async function () {
      const R = {}; const U = H.U;
      const row = () => document.getElementById('gg-cs-' + U + '-' + H.GK).querySelector('[data-ck]');
      row().querySelector(':scope>button').click(); await wait(40);
      const ta = row().querySelector('textarea');
      H.T1 = '하네스 고친 글 ' + Date.now();
      ta.value = H.T1; key(ta, 'Enter'); await wait(80);
      const after = LS('ox_q_geunge');
      const b = JSON.parse(H.before), a = JSON.parse(after);
      const gb = b[U].find(x => x.k === H.GK), ga = a[U].find(x => x.k === H.GK);
      const cb = ggCsOf(gb, H.CK), ca = ggCsOf(ga, H.CK);
      R.newT = ca && ca.t; R.tsSame = cb.ts === ca.ts; R.kSame = cb.k === ca.k;
      cb.t = H.T1;   /* 옛 저장소에서 그 t 만 바꾸면 새 저장소와 글자까지 같아야 한다 */
      R.onlyT = JSON.stringify(b) === JSON.stringify(a);
      R.rowText = txt(row().querySelector('span.whitespace-pre-wrap')); R.rowBtns = [...row().querySelectorAll(':scope>button')].map(x => x.textContent.trim());
      R.jnHasT1 = document.getElementById('hz-jn').textContent.indexOf(H.T1.slice(0, 12)) >= 0;
      H.afterCard = after;
      return JSON.stringify(R);
    },

    /* ── §A 문항 팝업(범위 qp-) — 같은 줄 · Esc 가 창을 안 닫는다 · 저장이 카드 줄에도 퍼진다 */
    a_popup: async function () {
      const R = {}; const U = H.U;
      openQPopup(U); await wait(250);
      const win = document.getElementById('oxwin-q-' + U); R.win = !!win;
      const cs = document.getElementById('qp-gg-cs-' + U + '-' + H.GK); R.csBox = !!cs;
      if (!cs) return JSON.stringify(R);
      unhide(cs, win);
      const row = () => document.getElementById('qp-gg-cs-' + U + '-' + H.GK).querySelector('[data-ck]');
      R.btns = [...row().querySelectorAll(':scope>button')].map(b => b.textContent.trim());
      row().querySelector(':scope>button').click(); await wait(40);
      R.open = !!row().querySelector('textarea'); R.idQp = (row().querySelector('textarea') || {}).id;
      key(row().querySelector('textarea'), 'Escape'); await wait(60);
      R.winAfterEsc = !!document.getElementById('oxwin-q-' + U); R.escClosed = !row().querySelector('textarea');
      row().querySelector(':scope>button').click(); await wait(40);
      H.T2 = '하네스 팝업에서 고침 ' + Date.now();
      const ta = row().querySelector('textarea'); ta.value = H.T2; key(ta, 'Enter'); await wait(80);
      const a = JSON.parse(LS('ox_q_geunge')), b = JSON.parse(H.afterCard);
      R.newT = ggCsOf(a[U].find(x => x.k === H.GK), H.CK).t;
      ggCsOf(b[U].find(x => x.k === H.GK), H.CK).t = H.T2;
      R.onlyT = JSON.stringify(a) === JSON.stringify(b);
      R.cardFollows = txt(document.getElementById('gg-cs-' + U + '-' + H.GK)).indexOf(H.T2.slice(0, 14)) >= 0;
      R.jnFollows = document.getElementById('hz-jn').textContent.indexOf(H.T2.slice(0, 14)) >= 0;
      return JSON.stringify(R);
    },

    /* ── §B 근거에서 찾기 — ↩ n · 이미 넣음 줄은 없음 · 누르면 넣기 안 하고 쓰임 창 */
    b_search: async function () {
      const R = {};
      document.querySelectorAll('.oxwin').forEach(w => w.remove());   /* 앞 시험의 팝업 창이 캡처 ② 를 가리지 않게 */
      const T = 'Q4311', term = '법인책임';
      R.count = useCount('geunge', T);
      const ownersT = useOwners('geunge', T);
      const O1 = quizData.find(q => q.id !== T && ownersT.indexOf(q.id) < 0 && !(JSON.parse(LS('ox_q_reflinks') || '{}')[q.id])).id;
      const O2 = ownersT[0];
      R.O1 = O1; R.O2 = O2;
      const run = (O, id) => {
        const h = host(id, 'top:0;left:780px;width:480px');
        h.innerHTML = '<div style="font-size:11.5px;font-weight:700;padding:4px 8px;background:#f9fafb">🔍 근거에서 찾기</div><input id="link-search-geunge-' + O + '" value="' + term + '" style="width:100%"><div id="link-results-geunge-' + O + '"></div>';
        linkSearch(O, 'geunge', '');
        return document.getElementById('link-results-geunge-' + O);
      };
      const box = run(O1, 'hz-search');
      const rows = [...box.querySelectorAll(':scope>button')];
      R.nRows = rows.length;
      const rowT = rows.find(r => r.textContent.indexOf('ID ' + T) >= 0);
      R.hasT = !!rowT;
      if (rowT) {
        const hd = rowT.querySelector('div');
        R.head = [...hd.children].map(x => x.tagName.toLowerCase() + ':' + txt(x));
        const i = hd.querySelector('i');
        R.iTxt = i && txt(i); R.iColor = i && getComputedStyle(i).color; R.iAfterWhere = !!(i && i.previousElementSibling && i.previousElementSibling.className.indexOf('text-indigo-700') >= 0);
        H.iSearch = true;
      }
      /* 누르기 — 넣기(addRefId) 안 함 · 쓰임 창 */
      const refl0 = LS('ox_q_reflinks'), pick0 = JSON.stringify(refPicked(O1, 'geunge')), w0 = oxwins();
      if (rowT && rowT.querySelector('i')) rowT.querySelector('i').click();
      await wait(120);
      R.reflSame = LS('ox_q_reflinks') === refl0; R.pickSame = JSON.stringify(refPicked(O1, 'geunge')) === pick0;
      R.newWins = oxwins().filter(x => w0.indexOf(x) < 0);
      R.newWins.forEach(id => { const w = document.getElementById(id); if (w) w.remove(); });   /* 캡처 ② 를 가리지 않게 */
      /* 이미 넣은 쪽(O2 는 T 를 걸어 둠) — 그 줄은 「이미 넣음」·↩ 없음 */
      const box2 = run(O2, 'hz-search2');
      const r2 = [...box2.querySelectorAll(':scope>button')].find(r => r.textContent.indexOf('ID ' + T) >= 0);
      R.onRow = r2 ? [r2.textContent.indexOf('이미 넣음') >= 0, !!r2.querySelector('i')] : null;
      document.getElementById('hz-search2').remove();
      /* 다른 줄 규칙 — 둘째 검색(다른 문항 O3 · 입력칸 id 가 첫 검색과 안 겹친다) · ↩ 있는 줄·없는 줄이 둘 다 나오는 첫 검색어 */
      const idOf = r => ((r.querySelector('span') || {}).textContent || '').replace(/^ID\s*/, '').trim();
      const refAll = JSON.parse(LS('ox_q_reflinks') || '{}');
      const O3 = quizData.find(q => q.id !== T && q.id !== O1 && !refAll[q.id]).id; R.O3 = O3;
      const box3 = run(O3, 'hz-search3'); let rows3 = [];
      for (const t2 of ['실종', '사망', '대표', '법인', '동의', '부합']) {
        document.getElementById('link-search-geunge-' + O3).value = t2; linkSearch(O3, 'geunge', '');
        rows3 = [...box3.querySelectorAll(':scope>button')]; R.term2 = t2;
        if (rows3.some(r => r.querySelector('i')) && rows3.some(r => !r.querySelector('i'))) break;
      }
      R.term2Rows = rows3.length;
      R.noI = rows3.filter(r => !r.querySelector('i') && r.textContent.indexOf('이미 넣음') < 0).map(r => useCount('geunge', idOf(r)));
      R.withI = rows3.filter(r => r.querySelector('i')).map(r => [idOf(r), useCount('geunge', idOf(r)), txt(r.querySelector('i'))]);
      document.getElementById('hz-search3').remove();
      R.firstIntact = document.getElementById('link-search-geunge-' + O1).value === term && !!document.querySelector('#hz-search i');
      return JSON.stringify(R);
    },

    /* ── §C·§D 영역지정 pick 화면 — 상자 그룹 = slotUsers · 팝업 ↩ n = 딱지 이름 수 · 누르면 refAdopt 없이 목록 창 */
    d_viewer: async function () {
      const R = {};
      document.querySelectorAll('.oxwin').forEach(w => w.remove());
      const co0 = JSON.parse(LS('ox_q_coords') || '{}');
      const VQ = quizData.find(q => !co0[q.id]).id; R.VQ = VQ; H.VQ = VQ;
      await window.oxCoord.open(VQ, 'pick');
      const wrap = [...document.body.children].reverse().find(d => d.style && d.style.zIndex === '10000');
      R.wrap = !!wrap;
      const layer = wrap && wrap.querySelector('canvas') && wrap.querySelector('canvas').nextElementSibling;
      await until(() => layer && [...layer.children].some(b => typeof b.onclick === 'function'), 300);
      const boxes = layer ? [...layer.children].filter(b => typeof b.onclick === 'function') : [];
      R.boxes = boxes.length;
      const seen = new Map(); let bad = [];
      for (const b of boxes) {
        b.click(); await wait(10);
        const pop = document.getElementById('cd-refpop');
        const g = pop && pop._g;
        if (!g) { bad.push('no pop'); continue; }
        const q1 = [...new Set(g.list.map(x => x.qid))].sort().join(',');
        const us = window.oxCoord.slotUsers ? window.oxCoord.slotUsers(VQ, g.list[0].rc) : null;
        const q2 = us ? us.map(x => x.qid).sort().join(',') : 'NA';
        if (q1 !== q2) bad.push(q1 + ' ≠ ' + q2);
        seen.set(q1, (seen.get(q1) || 0) + 1);
      }
      R.groups = [...seen.keys()].length; R.multi = [...seen.keys()].filter(k => k.split(',').length >= 2); R.bad = bad.slice(0, 5);
      /* Q4326 무리 팝업 — ↩ n · 딱지 이름 수 · 누르기 */
      const target = boxes.find(b => { b.click(); const p = document.getElementById('cd-refpop'); return p && p._g && p._g.list.some(x => x.qid === 'Q4326'); });
      const pop = document.getElementById('cd-refpop');
      R.popFor = pop && pop._g ? pop._g.list.map(x => x.qid) : null;
      const i = pop && pop.querySelector('i');
      R.iTxt = i && txt(i); R.iBetween = !!(i && i.previousElementSibling && i.previousElementSibling.id === 'cd-refgo' && i.nextElementSibling && i.nextElementSibling.id === 'cd-refno');
      R.rowAlign = pop && getComputedStyle(pop.querySelector('#cd-refgo').parentElement).alignItems;
      const tag = document.getElementById('cd-reftag'); R.tagNames = tag ? tag.textContent.split(' · ').length : null;
      H.popRect = pop ? pop.getBoundingClientRect().toJSON() : null;
      return JSON.stringify(R);
    },
    d_click: async function () {
      const R = {};
      const pop = document.getElementById('cd-refpop'); const i = pop && pop.querySelector('i');
      const co0 = LS('ox_q_coords'), w0 = oxwins();
      if (i) i.click();
      await wait(150);
      R.coordsSame = LS('ox_q_coords') === co0; R.popStill = !!document.getElementById('cd-refpop');
      R.newWins = oxwins().filter(x => w0.indexOf(x) < 0);
      const w = R.newWins.length ? document.getElementById(R.newWins[0]) : null;
      if (w) {
        R.title = txt(w.querySelector('.oxwin-head'));
        const rows = [...w.querySelectorAll('.oxwin-body > div')];
        R.rows = rows.map(r => [txt(r), r.style.background, r.getAttribute('onclick') ? 1 : 0]);
        H.winId = w.id; H.winRect = w.getBoundingClientRect().toJSON();
      }
      return JSON.stringify(R);
    },
    d_rowclick: async function () {
      const R = {};
      const w = document.getElementById(H.winId);
      const row = [...w.querySelectorAll('.oxwin-body > div')].find(r => r.getAttribute('onclick'));
      const q = row && ((row.querySelector('span') || {}).textContent || '').replace(/^ID\s*/, '').trim();
      const w0 = oxwins();
      if (row) row.click();
      await wait(200);
      R.q = q; R.opened = oxwins().filter(x => w0.indexOf(x) < 0);
      R.meRowClick = [...w.querySelectorAll('.oxwin-body > div')][0].getAttribute('onclick');
      return JSON.stringify(R);
    },
    d_close: async function () {
      document.querySelectorAll('.oxwin').forEach(w => w.remove());
      const b = document.querySelector('#cd-close'); if (b) b.click();
      await wait(80);
      return JSON.stringify({ closed: !document.querySelector('#cd-close') });
    },

    /* ── §E 카드 자리 그림 — 한 자리(칩 없음)는 아랫줄 · 여러 자리는 칩 옆 · 넘기면 따라감 · 누르면 뷰어 안 열림 */
    e_pic: async function () {
      const R = {};
      document.querySelectorAll('.oxwin').forEach(w => w.remove());
      const h = host('hz-pic', 'top:0;left:0;width:460px');
      h.innerHTML = '<div style="font-size:12px;font-weight:700">Q4327 · 정리OMR(한 자리 · 🔗 Q4326 자리)</div>' + window.mbBook.picHTML('Q4327', 'minbeopOMR', 'omr')
        + '<div style="font-size:12px;font-weight:700;margin-top:14px">Q4311 · 정리OMR(자리 둘)</div>' + window.mbBook.picHTML('Q4311', 'minbeopOMR', 'omr')
        + '<div style="font-size:12px;font-weight:700;margin-top:14px">Q5631 · 정리OMR(자리 셋 · 첫 자리에 흉내 겹침 둘)</div>' + window.mbBook.picHTML('Q5631', 'minbeopOMR', 'omr');
      window.mbBook.picFill(h); await wait(80);
      const boxes = [...h.querySelectorAll('[data-mbbpic]')];
      R.n = boxes.length;
      const st = b => { const c = b.querySelector('.mbbpic-chip'), u = b.querySelector('.mbbpic-use'); return [c ? txt(c) : null, u ? txt(u) : null, u && c ? (c.nextElementSibling === u) : null]; };
      R.b0 = st(boxes[0]); R.b1 = st(boxes[1]); R.b2 = st(boxes[2]);
      /* 넘기기 — Q4311 둘째 자리에 흉내 ref(Q0003) 가 있다 → 1쪽 ↩ 없음 · 2쪽 ↩1 */
      const seq = [];
      for (let k = 0; k < 3; k++) { const c = boxes[1].querySelector('.mbbpic-chip'); if (!c) break; c.click(); await wait(40); seq.push(st(boxes[1]).slice(0, 2)); }
      R.flip = seq;
      /* ↩ 누르기 — 뷰어(z 10000 겹) 안 열림 · 목록 창만 */
      const i = h.querySelector('.mbbpic-use i'); R.clickedIn = i ? i.closest('[data-mbbpic]').getAttribute('data-mbbpic') : null;
      const ov0 = [...document.body.children].filter(d => d.style && d.style.zIndex === '10000').length, w0 = oxwins();
      if (i) i.click();
      await wait(150);
      R.ovAfter = [...document.body.children].filter(d => d.style && d.style.zIndex === '10000').length - ov0;
      R.newWins = oxwins().filter(x => w0.indexOf(x) < 0);
      const w = R.newWins.length ? document.getElementById(R.newWins[0]) : null;
      R.winRows = w ? [...w.querySelectorAll('.oxwin-body > div')].map(r => txt(r)) : null;
      H.picWin = w ? w.id : null;
      /* 0 이면 없음 — 겹침 없는 문항 하나 */
      const co = JSON.parse(LS('ox_q_coords') || '{}');
      const lone = Object.keys(co).find(q => q !== 'Q4311' && q !== 'Q5631' && (co[q] || []).length === 1 && co[q][0].doc === 'minbeopOMR' && !co[q][0].ref && window.oxCoord.slotUsers(q, window.oxCoord.resolveSlot(co[q][0])).length === 0);
      const h2 = host('hz-pic0', 'top:0;left:500px;width:300px');
      h2.innerHTML = window.mbBook.picHTML(lone, 'minbeopOMR', 'omr'); window.mbBook.picFill(h2); await wait(40);
      R.lone = lone; R.loneUse = h2.querySelectorAll('.mbbpic-use').length; R.loneNav = h2.querySelectorAll('.mbbpic-nav').length;
      h2.remove();
      H.picRect = h.getBoundingClientRect().toJSON();
      return JSON.stringify(R);
    },

    /* ── 헛잣대(HEAD) — 새 것이 하나도 없는가 */
    head_probe: async function () {
      const R = {};
      const st = JSON.parse(LS('ox_q_geunge') || '{}');
      let U = null, G = null;
      for (const u of Object.keys(st)) { for (const g of (st[u] || [])) { if (g && Array.isArray(g.cs) && g.cs.length) { U = u; G = g; break; } } if (U) break; }
      const h = host('hz-card');
      h.innerHTML = ggLineHTML(U);
      const row = document.getElementById('gg-cs-' + U + '-' + G.k).querySelector('[data-ck]');
      R.btns = [...row.querySelectorAll(':scope>button')].map(b => b.textContent.trim());
      const hs = host('hz-search', 'left:780px;width:480px');
      const O1 = quizData.find(q => q.id !== 'Q4311' && useOwners('geunge', 'Q4311').indexOf(q.id) < 0 && !(JSON.parse(LS('ox_q_reflinks') || '{}')[q.id])).id;
      hs.innerHTML = '<input id="link-search-geunge-' + O1 + '" value="법인책임"><div id="link-results-geunge-' + O1 + '"></div>';
      linkSearch(O1, 'geunge', '');
      R.searchI = document.getElementById('link-results-geunge-' + O1).querySelectorAll('i').length;
      const hp = host('hz-pic', 'top:300px');
      hp.innerHTML = window.mbBook.picHTML('Q4326', 'minbeopOMR', 'omr'); window.mbBook.picFill(hp); await wait(60);
      R.picUse = hp.querySelectorAll('.mbbpic-use').length;
      R.slotUsers = !!(window.oxCoord && window.oxCoord.slotUsers);
      await window.oxCoord.open('Q4311', 'pick');
      const wrap = [...document.body.children].reverse().find(d => d.style && d.style.zIndex === '10000');
      const layer = wrap && wrap.querySelector('canvas') && wrap.querySelector('canvas').nextElementSibling;
      await until(() => layer && [...layer.children].some(b => typeof b.onclick === 'function'), 300);
      const b = layer ? [...layer.children].find(x => typeof x.onclick === 'function') : null;
      if (b) b.click(); await wait(20);
      const pop = document.getElementById('cd-refpop');
      R.popI = pop ? pop.querySelectorAll('i').length : null;
      return JSON.stringify(R);
    },
  };
})();
