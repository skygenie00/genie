/* ══════════ ★ 2026-09-26 (_task_ox_exview_paper) 기출뷰 = 시험지 · OMR 오지선다 + 시계 · 첫 화면 회독 칩 · 기록 칸 지우기(묘비) · 정리 창 기출 칩 ══════════
   · 기출키 = studyplandata `minbeop/기출키.json`(mingong/_json_build.py 가 마스터 기출DB 시트에서 굽는다 · 문항 JSON 옆 셋째 파일)
       keys[해][문번] = {ans:[번호…], combo, y:[글자…], neg, stem} · comboText[해][문번] = 선지 다섯 글(OCR 시험지 판독) · pdfNo[해][문번] = 시험지 문번(2011·2018)
       ⚠ 엑셀 경로(importExcelFile)는 같은 셈 gkeyFromSheet() 로 기출DB 를 읽는다 — _json_build.gkey_from_aoa 와 한 글자도 같아야 한다(G1 이 바이트째 맞댄다)
   · 조합 선지 글 = 시험지 PDF 글자층(mbExam.combo · 색인 캐시 gichulidx 에 같이) → 다섯 집합이 온전히 안 나오면 기출키 comboText → 없으면 「정답 못 정함」
   · 고른 답 ox_exam_pick {"해:문번":1~5} · 시험지 회독 ox_exam_rounds {"해":[{date,ok,n,ms,picks}]} — 동기화(SYNC_KEYS) · 시계 ox_exam_timer 는 기기별(동기화 안 함)
   · 쪽 채점 결과(O 맞음 표시)는 세션 값(EXV_RES) · 남는 것은 고른 답과 전체 채점 회독 */
let GKEY = null;                       /* 기출키 {meta, keys, comboText, pdfNo} — IndexedDB 'gkey' */
let EXV_RES = {};                      /* {"해:문번": true 맞음 | false 틀림 | null 못 정함} — 이 세션 채점 */
let EXV_OPEN = {};                     /* 「정답·해설 ▸」 로 연 문항 {"해:문번": true} */
let EXV_DONE = {};                     /* 이 세션에서 전체 채점을 마친 해 {"해": true} */
let EXV_LASTPICK = {};                 /* 전체 채점 순간의 고른 답(고른 답은 비우지만 화면은 그 답으로 칠한다) */
const EXV_COMBO = {};                  /* {"해:문번": {sets:[[글자…]×5], src:'pdf'|'text'} | {miss:true}} */
const EXV_CIR = ['', '①', '②', '③', '④', '⑤'];
const EXV_KO = 'ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ';
const EXV_LIMIT = 70 * 60 * 1000;
const GKEY_SHEET = '기출DB';
const MB_GKEY_PATH = 'minbeop/기출키.json';

/* ---------- 기출키 — 기출DB 시트 → keys (⚠ _json_build.gkey_from_aoa 와 같은 셈) ---------- */
function gkS(v) { if (v === null || v === undefined) return ''; if (typeof v === 'boolean') return v ? 'true' : 'false'; return String(v).trim(); }
function gkInt(t) { const m = /^\s*([+-]?\d+)/.exec(t || ''); return m ? parseInt(m[1], 10) : 0; }
function gkeyFromAoa(aoa) {
    if (!aoa || !aoa.length) return {};
    const head = (aoa[0] || []).map(gkS), col = {};
    head.forEach((h, i) => { if (h && !(h in col)) col[h] = i; });
    for (const k of ['연도', '문번', '지문', '정답선지', '조합형', '부정형', '발문']) if (!(k in col)) return {};
    const g = (r, k) => gkS(r[col[k]]);
    const isKo = l => l.length === 1 && EXV_KO.includes(l);
    const isCir = c => c.length === 1 && '①②③④⑤'.includes(c);
    const by = {};
    for (let i = 1; i < aoa.length; i++) {
        const r = aoa[i] || [], y = g(r, '연도'), n = gkInt(g(r, '문번'));
        if (!y || n <= 0) continue;
        (by[y] = by[y] || {});
        (by[y][n] = by[y][n] || []).push(r);
    }
    const out = {};
    Object.keys(by).sort((a, b) => (gkInt(a) - gkInt(b)) || (a < b ? -1 : a > b ? 1 : 0)).forEach(y => {
        out[y] = {};
        Object.keys(by[y]).map(Number).sort((a, b) => a - b).forEach(n => {
            const rs = by[y][n], labs = rs.map(r => g(r, '지문'));
            const combo = rs.some(r => g(r, '조합형') === 'Y') || labs.some(isKo);
            const cir = rs.map(r => g(r, '정답선지')).filter(isCir);
            const ys = rs.filter(r => g(r, '정답선지') === 'Y').map(r => g(r, '지문'));
            let ans = [], yy = [];
            if (cir.length) ans = [...new Set(cir.map(c => '①②③④⑤'.indexOf(c) + 1))].sort((a, b) => a - b);
            else if (combo) yy = [...new Set(ys.filter(isKo))].sort((a, b) => EXV_KO.indexOf(a) - EXV_KO.indexOf(b));
            else ans = [...new Set(ys.map(gkInt).filter(k => k >= 1 && k <= 5))].sort((a, b) => a - b);
            const stem = rs.map(r => g(r, '발문')).find(s => s) || '';
            out[y][String(n)] = { ans: ans, combo: combo, y: yy, neg: rs.some(r => g(r, '부정형') === 'Y'), stem: stem };
        });
    });
    return out;
}
function gkeyFromSheet(ws) { return gkeyFromAoa(XLSX.utils.sheet_to_json(ws, { header: 1, defval: '', blankrows: true })); }
/* 엑셀 경로 — 기출DB 에서 keys 만 새로, 엑셀에 없는 덧자료(comboText·pdfNo)는 지금 기출키에서 그대로 */
async function gkeyPutFromSheet(keys, fileName) {
    if (!keys || !Object.keys(keys).length) return;
    GKEY = { meta: { source: fileName || '엑셀', fromExcel: true, builtAt: new Date().toISOString(), masterMd5: '',
                     count: Object.values(keys).reduce((a, v) => a + Object.keys(v).length, 0) },
             keys: keys, comboText: (GKEY && GKEY.comboText) || {}, pdfNo: (GKEY && GKEY.pdfNo) || {} };
    try { await dbPut('gkey', GKEY); } catch (e) { }
    exvAfterGkey();
}
/* 서버 — 문항 JSON 을 받는 fetchServerData 옆 · 토큰이 없거나 못 받으면 조용히 null */
async function fetchServerGkey() {
    let j = null;
    try { j = await mbGhGet(MB_GKEY_PATH); } catch (e) { j = null; }
    return (j && j.keys && j.meta) ? j : null;
}
let _gkBusy = false;
/* m = 서버 딱지(문항메타) · 지금 기출키가 그 마스터 판이 아니면 새로 받는다 · force = 문항을 새로 받았을 때 */
async function gkeyRefresh(m, force) {
    if (_gkBusy) return;
    if (!force && GKEY && GKEY.meta && GKEY.meta.masterMd5 && (!m || GKEY.meta.masterMd5 === m.masterMd5)) return;
    _gkBusy = true;
    try {
        const j = await fetchServerGkey();
        if (j) { GKEY = j; try { await dbPut('gkey', j); } catch (e) { } exvAfterGkey(); }
    } finally { _gkBusy = false; }
}
/* 앱 시작 — IndexedDB 의 기출키부터 · 없으면 서버에서(작다 · 문항은 안 건드린다) */
async function gkeyBoot() {
    try { const g = await dbGet('gkey'); if (g && g.keys) { GKEY = g; exvAfterGkey(); } } catch (e) { }
    if (!GKEY) gkeyRefresh(null, true);
}
function exvAfterGkey() {
    try {
        const home = document.getElementById('home-screen');
        if (home && !home.classList.contains('hide')) { renderDashboard(); return; }
        if (exvOn()) exvFill();
    } catch (e) { }
}
/* 시험지 번호 — 저장소 시험지의 문번이 기출DB 와 다른 해(2011·2018)는 대응표로 */
function gkPdfNo(year, no) {
    const m = GKEY && GKEY.pdfNo && GKEY.pdfNo[String(year)];
    const v = m && m[String(no)];
    return v ? +v : +no;
}

/* ---------- 기출뷰 판정 · 저장소 ---------- */
function exvYear() { const m = /^(\d{4})년/.exec(currentChapterLabel || ''); return m ? m[1] : ''; }
function exvOn() { return !!isExamMode && currentSubject === '변리사 기출' && !!exvYear(); }
function exvKey(no, y) { return (y || exvYear()) + ':' + no; }
function exvGK(y, no) { return (GKEY && GKEY.keys && GKEY.keys[String(y)] && GKEY.keys[String(y)][String(no)]) || null; }
function exvMeta(it, y) { return (it.examMeta || []).find(m => String(m.year) === String(y)) || null; }
function exvRaw(it, y) { const m = exvMeta(it, y); return (m && m.optRaw) || ''; }
function exvIsKo(s) { return s.length === 1 && EXV_KO.includes(s); }
function exvLS(k) { try { return JSON.parse(localStorage.getItem(k) || '{}') || {}; } catch (e) { return {}; } }
function exvPicks() { return exvLS('ox_exam_pick'); }
function exvPickPut(key, n) {
    const p = exvPicks();
    if (n) p[key] = n; else delete p[key];
    try { localStorage.setItem('ox_exam_pick', JSON.stringify(p)); } catch (e) { }
}
function exvRounds() { return exvLS('ox_exam_rounds'); }
function exvTimers() { return exvLS('ox_exam_timer'); }
function exvSetKey(a) { return a.slice().sort((x, y) => EXV_KO.indexOf(x) - EXV_KO.indexOf(y)).join(','); }
function exvItemsOf(y, no) {
    return (typeof quizData !== 'undefined' ? quizData : []).filter(q => (q.examMeta || []).some(m => String(m.year) === String(y) && +m.no === +no));
}
function exvIsCombo(y, no, items) {
    const g = exvGK(y, no);
    if (g) return !!g.combo;
    return (items || exvItemsOf(y, no)).some(it => exvIsKo(exvRaw(it, y)));
}
/* 정답 — 원문자·일반 = 기출키 ans · 조합형 Y = 조합 선지 중 글자 집합이 Y 와 똑같은 하나 */
function exvCorrect(y, no) {
    const g = exvGK(y, no);
    if (!g) return { ans: [], why: '기출키 없음' };
    if (g.ans && g.ans.length) return { ans: g.ans.slice() };
    if (g.combo && g.y && g.y.length) {
        const c = EXV_COMBO[exvKey(no, y)];
        if (!c || !c.sets) return { ans: [], why: c && c.miss ? '조합 선지 못 읽음' : '읽는 중' };
        const want = exvSetKey(g.y), hit = [];
        c.sets.forEach((s, i) => { if (exvSetKey(s) === want) hit.push(i + 1); });
        return hit.length === 1 ? { ans: hit } : { ans: [], why: '못 정함' };
    }
    return { ans: [], why: '못 정함' };
}
/* 조합 선지 다섯 — 글자가 그 문항 지문 글자 안에 있고, Y 가 있으면 Y 와 같은 선지가 꼭 하나 */
function exvSetsOk(sets, y, no) {
    if (!Array.isArray(sets) || sets.length !== 5 || sets.some(s => !s || !s.length)) return false;
    const have = new Set(exvItemsOf(y, no).map(it => exvRaw(it, y)).filter(exvIsKo));
    if (have.size && sets.some(s => s.some(c => !have.has(c)))) return false;
    const g = exvGK(y, no);
    if (g && g.y && g.y.length) {
        const want = exvSetKey(g.y);
        if (sets.filter(s => exvSetKey(s) === want).length !== 1) return false;
    }
    return true;
}
/* 조합 선지 읽기 — 시험지 글자층 먼저(mbExam.combo) · 안 되면 기출키 comboText · 결과는 이 세션 EXV_COMBO */
async function exvComboLoad(y, nos) {
    const need = nos.filter(no => !(EXV_COMBO[exvKey(no, y)] && EXV_COMBO[exvKey(no, y)].sets));
    if (!need.length) return;
    let rec = null;
    try { if (window.mbExam && mbExam.index) rec = await mbExam.index(mbExam.file(y)); } catch (e) { rec = null; }
    need.forEach(no => {
        let sets = null, src = '';
        if (rec && mbExam.combo) {
            const s = mbExam.combo(rec, gkPdfNo(y, no));
            if (s && exvSetsOk(s, y, no)) { sets = s; src = 'pdf'; }
        }
        if (!sets) {
            const ct = GKEY && GKEY.comboText && GKEY.comboText[y] && GKEY.comboText[y][String(no)];
            if (Array.isArray(ct) && ct.length === 5) {
                const s2 = ct.map(x => [...String(x)].filter(c => EXV_KO.includes(c)));
                if (exvSetsOk(s2, y, no)) { sets = s2; src = 'text'; }
            }
        }
        EXV_COMBO[exvKey(no, y)] = sets ? { sets: sets, src: src } : { miss: true };
    });
}

/* ---------- 시험지 꼴(renderQuizPage 안에서 부른다) ---------- */
function exvRevealed(key, items) {
    if (EXV_RES[key] !== undefined || EXV_OPEN[key]) return true;
    const sm = (typeof currentSessionMarks !== 'undefined' && currentSessionMarks) || {};
    return items.some(it => Object.prototype.hasOwnProperty.call(sm, String(it.id)));
}
/* 채점 전 숨김 칸(O·X 줄 · 근거) — 풀기 줄 div 에 붙이는 class 꼬리 */
function exvPostCls(item) {
    const y = exvYear(), key = exvKey(item.examNo, y);
    return ' exv-post' + (exvRevealed(key, [item]) || exvRevealed(key, exvItemsOf(y, item.examNo)) ? '' : ' exv-hide');
}
/* 카드 머리 번호 — 일반 = 고르는 단추(원문자) · 조합형 = 지문 글자(ㄱ.) */
function exvLabelHTML(item) {
    const y = exvYear(), key = exvKey(item.examNo, y), raw = exvRaw(item, y);
    const lab = 'text-blue-700 font-extrabold text-[13px] whitespace-nowrap pt-px';
    if (exvIsCombo(y, item.examNo)) return `<span class="${lab}">${escHtml(exvIsKo(raw) ? raw : (EXV_CIR[item.examOpt] || raw))}.</span>`;
    const k = item.examOpt;
    if (!(k >= 1 && k <= 5)) return `<span class="${lab}">${escHtml(raw || '')}</span>`;
    return `<span class="${lab}"><button type="button" class="exv-num exv-lab" data-exk="${key}" data-exn="${k}" onclick="exvPick(this)" title="이 선지를 답으로 고르기">${EXV_CIR[k]}</button></span>`;
}
function exvSelHTML(key) {
    const c = EXV_COMBO[key];
    if (!c) return '<span class="exv-wait">조합 선지 읽는 중…</span>';
    if (!c.sets) return '<span class="exv-wait">조합 선지를 읽지 못했습니다</span>';
    return c.sets.map((s, i) => `<button type="button" class="exv-opt" data-exk="${key}" data-exn="${i + 1}" onclick="exvPick(this)"><b class="exv-num">${EXV_CIR[i + 1]}</b>${escHtml(s.join(', '))}</button>`).join('');
}
function exvPaperHTML(pageData, H) {
    const y = exvYear(), byNo = new Map();
    pageData.forEach(it => { if (!byNo.has(it.examNo)) byNo.set(it.examNo, []); byNo.get(it.examNo).push(it); });
    let html = '';
    byNo.forEach((items, no) => {
        const key = exvKey(no, y), combo = exvIsCombo(y, no, items), g = exvGK(y, no);
        const stem = (items.find(x => x.stem) || {}).stem || (g && escHtml(g.stem)) || '';
        html += `<div class="exv-q" data-exq="${key}"><div class="exv-head"><span class="exv-no">${no}.</span><span class="exv-stem">${stem}</span><span class="exv-res" data-exres="${key}"></span></div>`;
        if (combo) {
            html += '<div class="exv-bogi">' + items.map(it => H[it.id] || '').join('') + '</div>';
            html += `<div class="exv-sel" data-exsel="${key}">${exvSelHTML(key)}</div>`;
        } else {
            const used = new Set();
            for (let k = 1; k <= 5; k++) {
                const hit = items.filter(it => it.examOpt === k);
                if (hit.length) hit.forEach(it => { html += H[it.id] || ''; used.add(it.id); });
                else html += `<div class="exv-miss">${EXV_CIR[k]} (이 선지는 마스터에 없음)</div>`;
            }
            items.forEach(it => { if (!used.has(it.id)) html += H[it.id] || ''; });
        }
        html += `<div class="exv-ans"><button type="button" class="exv-peek" data-expk="${key}" onclick="exvPeek('${key}')">정답·해설 ▸</button></div></div>`;
    });
    return `<div class="exv-paper">${html}</div>`;
}
/* 렌더 뒤 — 조합 선지를 채우고(비동기) 칠한다 */
function exvFill() {
    const y = exvYear();
    const nos = [...new Set([...document.querySelectorAll('#quiz-container .exv-q')].map(q => +q.dataset.exq.split(':')[1]))];
    const combos = nos.filter(no => exvIsCombo(y, no));
    exvPaint();
    if (!combos.length) return;
    exvComboLoad(y, combos).then(() => {
        if (exvYear() !== y) return;
        combos.forEach(no => { const el = document.querySelector(`[data-exsel="${exvKey(no, y)}"]`); if (el) el.innerHTML = exvSelHTML(exvKey(no, y)); });
        exvPaint();
    });
}
/* 칠하기 — 고른 번호 · 결과 글자 · 정답 테 · 채점 뒤 O·X 줄 보이기 · 마킹 수 */
function exvPaint() {
    const y = exvYear(), picks = exvPicks();
    let marked = 0, total = 0;
    document.querySelectorAll('#quiz-container .exv-q').forEach(q => {
        const key = q.dataset.exq, no = +key.split(':')[1], res = EXV_RES[key];
        const p = picks[key] || (res !== undefined ? EXV_LASTPICK[key] : undefined);
        const cor = res !== undefined ? exvCorrect(y, no) : null;
        total++; if (picks[key]) marked++;
        q.querySelectorAll('[data-exk]').forEach(b => {
            const n = +b.dataset.exn, tgt = b.classList.contains('exv-num') ? b : b.querySelector('.exv-num') || b;
            b.classList.toggle('sel', p === n && res !== false);
            b.classList.toggle('bad', p === n && res === false);
            b.classList.toggle('ok', !!cor && cor.ans.includes(n));
            if (tgt !== b) { tgt.classList.toggle('sel', p === n && res !== false); tgt.classList.toggle('bad', p === n && res === false); tgt.classList.toggle('ok', !!cor && cor.ans.includes(n)); }
        });
        const rs = q.querySelector('.exv-res');
        if (rs) {
            if (res === undefined) rs.innerHTML = '';
            else if (res === null) rs.innerHTML = '<span class="exv-r-na">정답 못 정함</span>';
            else if (res) rs.innerHTML = '<span class="exv-r-ok">O 맞음</span>';
            else rs.innerHTML = '<span class="exv-r-bad">X 틀림 · 정답 ' + cor.ans.map(n => EXV_CIR[n]).join('·') + '</span>';
        }
        const items = [...q.querySelectorAll('.question-box')].map(b => ({ id: b.id.replace('q-box-', '') }));
        const open = exvRevealed(key, items);
        q.querySelectorAll('.exv-post').forEach(e => e.classList.toggle('exv-hide', !open));
        if (picks[key]) q.classList.remove('exv-need');
    });
    const c = document.getElementById('mark-count'), t = document.getElementById('mark-total');
    if (c) c.textContent = marked;
    if (t) t.textContent = total;
    if (document.getElementById('exv-omr-rows')) exvOmrPaint();
}
function exvPick(b) {
    const key = b.dataset.exk, n = +b.dataset.exn;
    if (!key || EXV_RES[key] !== undefined) return;          /* 채점된 문항은 안 바뀐다 */
    exvPickPut(key, n);
    exvPaint();
}
/* 문항 「정답·해설 ▸」 — 그 문항 지문들의 O·X 줄·근거·해설을 편다(채점하지 않는다) */
function exvPeek(key) {
    const q = document.querySelector(`#quiz-container .exv-q[data-exq="${key}"]`);
    if (!q) return;
    const on = !EXV_OPEN[key];
    if (on) EXV_OPEN[key] = true; else delete EXV_OPEN[key];
    q.querySelectorAll('.question-box').forEach(b => {
        const id = b.id.replace('q-box-', ''), ex = document.getElementById('exp-' + id);
        if (!ex) return;
        if (on && ex.classList.contains('hide')) togglePeekExp(id);
        else if (!on && !ex.classList.contains('hide') && !Object.prototype.hasOwnProperty.call(currentSessionMarks || {}, String(id))) togglePeekExp(id);
    });
    const pb = q.querySelector('.exv-peek');
    if (pb) pb.textContent = on ? '정답·해설 ▾' : '정답·해설 ▸';
    exvPaint();
}
function exvPageKeys() { return [...document.querySelectorAll('#quiz-container .exv-q')].map(q => q.dataset.exq); }
/* 쪽 채점(OMR 「채점 ✓」·gradeCurrentPage) — 이 쪽 문항을 기출키로 · 안 고른 문항이 있으면 채점 안 함 */
function exvGradePage() {
    const y = exvYear(), picks = exvPicks(), keys = exvPageKeys();
    const miss = keys.filter(k => !picks[k] && EXV_RES[k] === undefined);
    document.querySelectorAll('#quiz-container .exv-q').forEach(q => q.classList.toggle('exv-need', miss.includes(q.dataset.exq)));
    if (miss.length) { exvToast('답을 안 고른 문제가 있습니다 — ' + miss.map(k => k.split(':')[1] + '번').join(', ')); return; }
    keys.forEach(k => {
        if (EXV_RES[k] !== undefined) return;
        const cor = exvCorrect(y, +k.split(':')[1]);
        EXV_LASTPICK[k] = picks[k];
        EXV_RES[k] = cor.ans.length ? cor.ans.includes(picks[k]) : null;
    });
    exvPaint();
}
/* 전체 채점 — 이 해 문항 전부를 고른 때만 · 회독 하나(ox_exam_rounds) · 시계와 그 해 고른 답은 비운다 */
function exvGradeAll() {
    const y = exvYear(), picks = exvPicks();
    const nos = [...new Set(currentFilteredData.map(x => x.examNo))].sort((a, b) => a - b);
    const miss = nos.filter(n => !picks[exvKey(n, y)]);
    if (miss.length) { exvToast('답을 안 고른 문제 ' + miss.length + '개 — ' + miss.slice(0, 10).join(', ') + (miss.length > 10 ? ' …' : '') + '번'); return; }
    let ok = 0;
    const pk = {};
    nos.forEach(n => {
        const k = exvKey(n, y), cor = exvCorrect(y, n);
        EXV_LASTPICK[k] = picks[k]; pk[n] = picks[k];
        EXV_RES[k] = cor.ans.length ? cor.ans.includes(picks[k]) : null;
        if (EXV_RES[k]) ok++;
    });
    const t = exvTimerGet(), ms = exvElapsed(t);
    const R = exvRounds();
    (R[y] = R[y] || []).push({ date: new Date().toLocaleDateString(), ok: ok, n: nos.length, ms: ms, picks: pk });
    try { localStorage.setItem('ox_exam_rounds', JSON.stringify(R)); } catch (e) { }
    exvTimerPut({ acc: 0, since: 0 });
    const P = exvPicks();
    Object.keys(P).forEach(k => { if (k.indexOf(y + ':') === 0) delete P[k]; });
    try { localStorage.setItem('ox_exam_pick', JSON.stringify(P)); } catch (e) { }
    EXV_DONE[y] = true;
    try { stampAll(); syncRecords(); } catch (e) { }
    exvPaint();
    exvPill();
    exvToast('전체 채점 — ' + ok + ' / ' + nos.length + ' · ' + exvFmt(ms, true));
}
/* 알약 — 기출뷰는 문제(문번) 단위 · 마지막 쪽 「전체 채점 ✓」 · 전체 채점 뒤 지문 기록이 있으면 「회독 저장 ✓」 */
function exvPill() {
    const ab = document.getElementById('action-btn');
    if (!ab) return;
    const y = exvYear(), nos = [...new Set(currentFilteredData.map(x => x.examNo))];
    const rem = nos.length - (currentPageIndex + 1) * EXAM_Q_PER_PAGE;
    ab.style.display = '';
    if (rem > 0) {
        ab.innerText = '다음 ' + Math.min(EXAM_Q_PER_PAGE, rem) + '문제 ▶';
        ab.setAttribute('onclick', 'goNextPageExam()');
        ab.className = BAR_MOVE_CLS;
    } else if (!EXV_DONE[y]) {
        ab.innerText = '전체 채점 ✓';
        ab.setAttribute('onclick', 'gradeAllExam()');
        ab.className = BAR_GRADE_CLS;
    } else if (Object.keys(currentSessionMarks || {}).length) {
        ab.innerText = '회독 저장 ✓';
        ab.setAttribute('onclick', 'finishChapter()');
        ab.className = BAR_GRADE_CLS;
    } else {
        ab.style.display = 'none';
    }
}
/* 지문 O·X — 문항 채점(또는 ▸) 뒤 누르는 순간 그 지문을 채점·기록(약점 큐 = ox_q_history 틀림 + 🌀) */
function exvRecordOne(id, v) {
    const item = quizData.find(x => String(x.id) === String(id));
    if (!item || !item.examNo) return false;
    const y = exvYear(), key = exvKey(item.examNo, y);
    if (!exvRevealed(key, [item]) && EXV_RES[key] === undefined && !EXV_OPEN[key]) return false;
    if (Object.prototype.hasOwnProperty.call(currentSessionMarks, String(id))) return true;
    const isCorrect = (v === item.a);
    const qHistory = JSON.parse(localStorage.getItem('ox_q_history') || '{}');
    qHistory[id] = isCorrect;
    localStorage.setItem('ox_q_history', JSON.stringify(qHistory));
    try { const L = JSON.parse(localStorage.getItem('ox_q_last') || '{}'); L[id] = Date.now(); localStorage.setItem('ox_q_last', JSON.stringify(L)); } catch (e) { }
    try { ggPaintGraded(id, isCorrect); } catch (e) { }
    currentSessionMarks[id] = isCorrect;
    if (isCorrect) currentSessionScore++;
    document.querySelectorAll(`input[name="answer_${id}"]`).forEach(r => r.disabled = true);
    const exp = document.getElementById('exp-' + id);
    if (exp) {
        exp.classList.remove('hide');
        const pk = document.getElementById('peek-ans-' + id); if (pk) pk.classList.add('hide');
        const bd = exp.querySelector('.result-badge');
        if (bd) bd.innerHTML = isCorrect
            ? `<span class="inline-flex items-baseline gap-1 text-[12.5px] font-bold text-green-700">✓ 정답 <b class="${item.a === 'O' ? 'text-blue-600' : 'text-red-600'} font-extrabold">${item.a}</b> · 맞았습니다</span>`
            : `<span class="inline-flex items-baseline gap-1 text-[12.5px] font-bold text-red-600">✕ 오답 · 정답은 <b class="${item.a === 'O' ? 'text-blue-600' : 'text-red-600'} font-extrabold">${item.a}</b></span>`;
    }
    try { oxPaint(id); recStripRefresh(id); } catch (e) { }
    try { saveInProgress(chapKeyOf(currentSubject, currentChapterLabel)); } catch (e) { }
    try { stampAll(); syncRecords(); } catch (e) { }
    try { clearWrongCache(); } catch (e) { }
    exvPill();
    return true;
}

/* ---------- OMR 창 — 문번 × ①~⑤ + 시계(기기별 ox_exam_timer) ---------- */
function exvOmrOpen() {
    const y = exvYear();
    const nos = [...new Set(currentFilteredData.map(x => x.examNo))].sort((a, b) => a - b);
    const ex = document.getElementById('oxwin-omr');
    if (ex && ex.dataset.exvYear !== y) ex.remove();          /* 일반 OMR 창이나 다른 해 창이 남아 있으면 닫고 연다(oxWinOpen 은 있으면 몸통만 갈아 제목·부제가 남는다) */
    const w = oxWinOpen('omr', '📝 OMR 마킹<span id="exv-timer" class="exv-timer"></span>',
        '<span>' + y + ' · 70분</span><span id="exv-over" class="exv-over"></span>',
        '<div id="exv-omr-rows" class="exv-omr-rows"></div>'
        + '<div class="exv-omr-foot"><span id="exv-omr-count"></span>'
        + '<button onclick="omrGrade()" class="text-[11.5px] font-extrabold text-blue-500 hover:text-blue-700 bg-transparent border-0 rounded-full px-2 py-1" style="font-size:11.5px">채점 ✓</button></div>',
        250, { resize: true, sizeKey: 'omr' });
    if (w) w.dataset.exvYear = y;
    const rows = document.getElementById('exv-omr-rows');
    if (!rows) return;
    rows.innerHTML = nos.map(no => '<div class="exv-omr" data-no="' + no + '"><span class="no">' + no + '</span>'
        + [1, 2, 3, 4, 5].map(k => '<button type="button" data-n="' + k + '" onclick="exvOmrPick(this)">' + k + '</button>').join('') + '</div>').join('');
    if (w && !w.style.height) { w.style.height = Math.max(160, Math.min(560, innerHeight - 120)) + 'px'; w.style.maxHeight = 'none'; }
    exvOmrPaint(); exvTimerPaint();
    const cur = rows.querySelector('.exv-omr.cur');
    if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: 'center' });
}
function exvOmrPick(b) {
    const key = exvKey(b.parentNode.dataset.no);
    if (EXV_RES[key] !== undefined) return;
    exvPickPut(key, +b.dataset.n);
    exvPaint();
}
function exvOmrPaint() {
    const y = exvYear(), picks = exvPicks(), page = new Set(exvPageKeys());
    let n = 0;
    const rows = [...document.querySelectorAll('#exv-omr-rows .exv-omr')];
    rows.forEach(r => {
        const key = exvKey(r.dataset.no, y), res = EXV_RES[key];
        const p = picks[key] || (res !== undefined ? EXV_LASTPICK[key] : undefined);
        const cor = res !== undefined ? exvCorrect(y, +r.dataset.no) : null;
        if (picks[key]) n++;
        r.classList.toggle('cur', page.has(key));
        r.querySelectorAll('button').forEach(b => {
            const k = +b.dataset.n;
            b.className = (p === k ? (res === false ? 'bad' : 'on') : '') + (cor && cor.ans.includes(k) ? ' ok' : '');
        });
    });
    const c = document.getElementById('exv-omr-count');
    if (c) c.innerHTML = '마킹 <b>' + n + '</b>/' + rows.length;
}
function exvTimerGet() { return exvTimers()[exvYear()] || { acc: 0, since: 0 }; }
function exvTimerPut(t) { const all = exvTimers(); all[exvYear()] = t; try { localStorage.setItem('ox_exam_timer', JSON.stringify(all)); } catch (e) { } }
function exvElapsed(t) { return (t.acc || 0) + (t.since ? Date.now() - t.since : 0); }
/* 00H00M00S — 단위 글자는 숫자의 0.55배 · 흐림 .7(사용자 「1/10」은 1px 이 돼 안 보여 절반) · plain = 토스트용 글자만 */
function exvFmt(ms, plain) {
    const t = Math.floor(Math.max(0, ms) / 1000), p = n => String(n).padStart(2, '0');
    const u = x => plain ? x : '<span class="exv-u">' + x + '</span>';
    return p(Math.floor(t / 3600)) + u('H') + p(Math.floor(t / 60) % 60) + u('M') + p(t % 60) + u('S');
}
/* ↺ 두 번 — 첫 누름은 4초 동안만 「한 번 더」(빨강) · 상태는 단추가 아니라 여기 둔다(단추는 다시 그려진다) */
let EXV_RESET_ARM = 0;
const exvArmed = () => !!EXV_RESET_ARM && Date.now() - EXV_RESET_ARM < 4000;
function exvTimerToggle() { EXV_RESET_ARM = 0; const t = exvTimerGet(); if (t.since) { t.acc = exvElapsed(t); t.since = 0; } else t.since = Date.now(); exvTimerPut(t); exvTimerPaint(); }
function exvTimerReset() {
    if (!exvArmed()) { EXV_RESET_ARM = Date.now(); exvTimerPaint(); return; }   /* 한 번 = 빨강 */
    EXV_RESET_ARM = 0;
    exvTimerPut({ acc: 0, since: 0 }); exvTimerPaint();
}
/* 단추는 상태(흐름·멈춤·↺·빨강)가 바뀔 때만 다시 그린다 — 1초마다 통째로 그리면 누르는 순간 단추가 갈려 누름을 놓치고 「한 번 더」가 풀린다 · 초마다는 숫자만 */
function exvTimerPaint() {
    const box = document.getElementById('exv-timer');
    if (!box) return;
    const t = exvTimerGet(), el = exvElapsed(t), over = el - EXV_LIMIT;
    if (EXV_RESET_ARM && !exvArmed()) EXV_RESET_ARM = 0;
    const state = (t.since ? 'run' : 'stop') + (el && !t.since ? ':r' : '') + (exvArmed() ? ':a' : '');
    if (box.dataset.state !== state || !box.querySelector('.exv-t-v')) {
        box.dataset.state = state;
        const stop = 'onpointerdown="event.stopPropagation()" onmousedown="event.stopPropagation()" ontouchstart="event.stopPropagation()"';
        box.innerHTML = '<button type="button" class="exv-t-go' + (t.since ? ' run' : '') + '" ' + stop + ' onclick="event.stopPropagation();exvTimerToggle()" title="' + (t.since ? '멈춤' : '시작') + '">' + (t.since ? '❚❚' : '▶') + '</button>'
            + '<span class="exv-t-v"></span>'
            + (el && !t.since ? '<button type="button" id="exv-t-reset" class="exv-t-reset' + (exvArmed() ? ' sure' : '') + '" ' + stop + ' onclick="event.stopPropagation();exvTimerReset()" title="' + (exvArmed() ? '한 번 더 누르면 0으로' : '0으로(두 번)') + '">↺</button>' : '');
    }
    const v = box.querySelector('.exv-t-v'), s = exvFmt(el);
    if (v.dataset.s !== s) { v.dataset.s = s; v.innerHTML = s; }
    v.classList.toggle('over', over > 0);
    const ov = document.getElementById('exv-over');
    if (ov) { const o = over > 0 ? ' · 초과 +' + exvFmt(over) : ''; if (ov.dataset.s !== o) { ov.dataset.s = o; ov.innerHTML = o; } }
}
setInterval(() => { if (document.getElementById('exv-timer') && (exvTimerGet().since || EXV_RESET_ARM)) exvTimerPaint(); }, 1000);   /* 흐를 때와 「한 번 더」가 풀릴 때만 */

/* ---------- 토스트 — 앱에 알림 거품이 없어 기출뷰 몫만 ---------- */
let _exvToastT = null;
function exvToast(msg) {
    let el = document.getElementById('exv-toast');
    if (!el) { el = document.createElement('div'); el.id = 'exv-toast'; document.body.appendChild(el); }
    el.textContent = msg;
    el.classList.add('on');
    clearTimeout(_exvToastT);
    _exvToastT = setTimeout(() => el.classList.remove('on'), 2800);
}

/* ---------- 첫 화면 「변리사 기출」 줄 — 「40문항 · 188지문」 · 회독 상자 두 줄 · 진행중 ---------- */
function exvYearQCount(y) {
    const g = GKEY && GKEY.keys && GKEY.keys[y];
    if (g) return Object.keys(g).length;
    const s = new Set();
    quizData.forEach(q => (q.examMeta || []).forEach(m => { if (String(m.year) === String(y) && m.no) s.add(+m.no); }));
    return s.size;
}
function exvDashCount(chapLabel, n, countStyle) {
    const y = (/^(\d{4})년/.exec(chapLabel) || [])[1] || '';
    return `<span class="text-[11px] ${countStyle} whitespace-nowrap shrink-0" data-exvcount="${y}">${exvYearQCount(y)}문항 <span style="opacity:.55">·</span> ${n}지문</span>`;
}
function exvMin(ms) { return Math.floor(Math.max(0, ms) / 60000) + 'm'; }
/* 오른쪽 — 회독마다 파란 상자 하나(윗줄 시험지 · 아랫줄 지문) · 시험지 진행중(고른 답 또는 시계) = 주황 칩 · 지문 진행중 칩은 안 그린다 */
function exvDashRight(subject, chapLabel, chapHistory) {
    const y = (/^(\d{4})년/.exec(chapLabel) || [])[1] || '';
    const R = exvRounds()[y] || [], T = exvTimers()[y] || { acc: 0, since: 0 };
    const el = exvElapsed(T), pickN = Object.keys(exvPicks()).filter(k => k.indexOf(y + ':') === 0).length;
    const nq = exvYearQCount(y) || 40, esc = escAttr(chapLabel), prog = !!(pickN || el);
    let h = '';
    if (prog) h += `<span class="exv-dprog">▶ ${R.length + 1}회독 진행중 ${pickN}/${nq} · ${exvMin(el)}</span>`;
    const N = Math.max(R.length, chapHistory.length);
    for (let i = 0; i < N; i++) {
        const x = R[i], c = chapHistory[i];
        const top = x ? `<span class="exv-dok">${x.ok}</span>/${x.n} <span class="exv-dx">X${x.n - x.ok}</span> · <span class="${x.ms > EXV_LIMIT ? 'exv-dover' : ''}">${exvMin(x.ms)}</span>` : '';
        let bot = '';
        if (c) {
            const wrongN = c.marks ? Object.values(c.marks).filter(v => v === false).length : (c.total - c.score);
            bot = (typeof c.confuse === 'number' ? '🌀' + c.confuse + ' ' : '') + (typeof c.fake === 'number' ? '⚠' + c.fake + ' ' : '') + `<span class="exv-dx">X${wrongN}</span> /${c.total}`;
        }
        h += `<button type="button" onclick="event.stopPropagation();openCompareModal('${escAttr(subject)}','${esc}')" title="${i + 1}회독${x ? ' · 시험지 ' + escHtml(x.date || '') : ''}${c ? ' · 지문 ' + escHtml(c.date || '') : ''}" class="exv-dround">`
            + `<span>${i + 1}회독</span><span class="exv-dlines">${top ? '<span>' + top + '</span>' : ''}${bot ? '<span class="exv-dbot">' + bot + '</span>' : ''}</span></button>`;
    }
    h += `<button onclick="startQuiz('${escAttr(subject)}', '${esc}')" title="${prog ? '이어서 풀기' : (R.length + 1) + '회독 시작'}" class="text-[11.5px] font-extrabold bg-transparent border-0 px-1.5 py-1 rounded whitespace-nowrap hover:bg-gray-100 ${prog ? 'text-amber-600 hover:text-amber-700' : 'text-blue-500 hover:text-blue-700'}" style="font-size:11.5px">${prog ? '이어서' : (R.length + 1) + '회독'}</button>`;
    return h;
}

/* ---------- 풀이 기록 칸 — 누르면 출처 · × 두 번 = 지움 · 묘비(ox_rec_gone) ---------- */
function recTombId(uid, key, dateStr) {
    const t = recStripDay(dateStr);
    return uid + '|' + key + '|' + (t ? t.getFullYear() + '-' + (t.getMonth() + 1) + '-' + t.getDate() : String(dateStr || ''));
}
/* 「지금 결과」 다시 세우기 — 남은 칸 중 가장 나중 값(없으면 ox_q_history·ox_q_last·ox_weak_stage 를 지운다) · 근거 칩 색도.
   회독을 통째로 지울 때 쓰는 ggRecalcAfterDelete 를 그대로 부른다(한 칸 = 그 문항만 든 회독 하나를 지운 것과 같다) */
function recRecalc(uids) {
    uids.forEach(uid => {
        const rest = recCellsOf(uid, true).cells.filter(c => c.ok === true || c.ok === false);
        try { ggRecalcAfterDelete([{ marks: { [uid]: true } }], rest.map(c => ({ marks: { [uid]: c.ok } }))); } catch (e) { }
    });
    try { clearWrongCache(); } catch (e) { }
}
/* 되살아난 칸 쓸기 — 동기화 직후 · 앱 시작 때 · 지운 수를 돌려준다(묘비는 비우지 않는다 · ox_sync_gone 과 같은 원칙).
   ⚠ 지운 **뒤에** 같은 날 그 문항을 다시 풀었으면(ox_q_last 가 묘비 시각보다 나중 · 같은 날) 그 칸은 새 답이다 — 쓸지 않는다
     (「이번」 칸을 지우면 라디오가 풀려 다시 풀 수 있다 · 그 답을 묘비가 먹으면 안 된다) */
function recTombSweep() {
    const J = k => { try { return JSON.parse(localStorage.getItem(k) || '{}') || {}; } catch (e) { return {}; } };
    const gone = J('ox_rec_gone'), ids = Object.keys(gone);
    if (!ids.length) return 0;
    const hist = J('ox_chap_history'), prog = J(PROGRESS_KEY), qlast = J('ox_q_last'), touched = new Set();
    const ymd = t => t ? t.getFullYear() + '-' + (t.getMonth() + 1) + '-' + t.getDate() : '';
    const hit = (uid, key, ds) => {
        const at = gone[recTombId(uid, key, ds)];
        if (!at) return false;
        const q = +qlast[uid] || 0;
        return !(q > at && ymd(new Date(q)) === ymd(recStripDay(ds)));
    };
    let n = 0;
    Object.keys(hist).forEach(key => (Array.isArray(hist[key]) ? hist[key] : []).forEach(a => {
        if (!a || !a.marks) return;
        Object.keys(a.marks).forEach(uid => { if (hit(uid, key, a.date)) { delete a.marks[uid]; if (a.cf) delete a.cf[uid]; touched.add(uid); n++; } });
    }));
    Object.keys(prog).forEach(key => {
        const a = prog[key]; if (!a || !a.marks) return;
        Object.keys(a.marks).forEach(uid => { if (hit(uid, key, a.date)) { delete a.marks[uid]; touched.add(uid); n++; } });
    });
    if (n) {
        localStorage.setItem('ox_chap_history', JSON.stringify(hist));
        localStorage.setItem(PROGRESS_KEY, JSON.stringify(prog));
        recRecalc([...touched]);
    }
    return n;
}
function recCellTap(b) {
    const box = b.closest('[data-jnrec]') || b.closest('[id^="rec-strip-"]');
    const info = box && box.querySelector('.rec-info');
    if (!info) return;
    box.querySelectorAll('.rec-cell').forEach(x => x.classList.remove('rec-on'));
    if (info.dataset.on === b.dataset.tip && !info.classList.contains('hide')) { info.classList.add('hide'); info.dataset.on = ''; return; }
    b.classList.add('rec-on');
    info.dataset.on = b.dataset.tip;
    info.classList.remove('hide');
    info.innerHTML = '<span>' + escHtml(b.dataset.tip) + '</span><button type="button" class="rec-del" title="이 기록 지우기 — 한 번 더 누르면 지워진다">×</button>';
    info.querySelector('.rec-del').onclick = ev => {
        ev.stopPropagation();
        const d = ev.currentTarget;
        if (!d.dataset.sure) { d.dataset.sure = '1'; d.classList.add('sure'); return; }   /* 한 번 = 빨강 · 한 번 더 = 지움 */
        recCellDelete(b.dataset.uid, b.dataset.kind, b.dataset.key, +b.dataset.n);
    };
}
function recCellDelete(uid, kind, key, n) {
    const J = k => { try { return JSON.parse(localStorage.getItem(k) || '{}') || {}; } catch (e) { return {}; } };
    /* 정리 창의 「진행중」 칸이 지금 풀고 있는 바로 그 단원이면 「이번」 칸이다 — saveInProgress 가 marks 를 세션 값으로 통째로 다시 쓰므로 세션·라디오도 같이 푼다 */
    try {
        if (kind === 'prog' && currentSubject && currentChapterLabel && key === chapKeyOf(currentSubject, currentChapterLabel)
            && currentSessionMarks && Object.prototype.hasOwnProperty.call(currentSessionMarks, uid)) kind = 'cur';
    } catch (e) { }
    {
        const gone = J('ox_rec_gone');
        let ds = '';
        if (kind === 'hist') { const a = (J('ox_chap_history')[key] || [])[n - 1]; ds = a ? a.date : ''; }
        else { const p = J(PROGRESS_KEY)[key]; ds = p ? p.date : new Date().toLocaleDateString(); }
        gone[recTombId(uid, key, ds)] = Date.now();
        localStorage.setItem('ox_rec_gone', JSON.stringify(gone));
    }
    if (kind === 'hist') {
        const hist = J('ox_chap_history'), a = (hist[key] || [])[n - 1];
        if (a && a.marks) { delete a.marks[uid]; if (a.cf) delete a.cf[uid]; localStorage.setItem('ox_chap_history', JSON.stringify(hist)); }
    } else {
        const prog = J(PROGRESS_KEY);
        if (prog[key] && prog[key].marks) { delete prog[key].marks[uid]; localStorage.setItem(PROGRESS_KEY, JSON.stringify(prog)); }
        if (kind === 'cur') {
            if (currentSessionMarks && Object.prototype.hasOwnProperty.call(currentSessionMarks, uid)) {
                if (currentSessionMarks[uid] === true) currentSessionScore = Math.max(0, currentSessionScore - 1);
                delete currentSessionMarks[uid];
            }
            document.querySelectorAll('input[name="answer_' + uid + '"]').forEach(r => { r.disabled = false; r.checked = false; });
            const exp = document.getElementById('exp-' + uid);
            if (exp) { exp.classList.add('hide'); const bd = exp.querySelector('.result-badge'); if (bd) bd.innerHTML = ''; }
            try { oxPaint(uid); } catch (e) { }
        }
    }
    /* 「지금 결과」(ox_q_history · 약점 판정)는 남은 칸 중 가장 최근 것 — 남은 칸이 없으면 지운다 */
    recRecalc([uid]);
    try { stampAll(); syncRecords(); } catch (e) { }
    const box = document.getElementById('rec-strip-' + uid);
    if (box && !box.classList.contains('hide')) box.innerHTML = recStripHTML(uid);
    document.querySelectorAll('[data-jnrec="' + uid + '"]').forEach(x => { const t = document.createElement('div'); t.innerHTML = jnRecHTML(uid); x.replaceWith(t.firstElementChild || t); });
    exvToast('풀이 기록 한 칸을 지웠습니다');
}

/* ---------- 📋 정리 창 — 번호 뒤 출제연도 칩(모든 정리 창) · 기출 해 = 「문제 N」 구분 줄 + 문항 채점 칸 ---------- */
function jnExamChips(q) {
    return (q.examMeta || []).map((m, mi) => {
        const opt = (m.optRaw && exvIsKo(m.optRaw)) ? m.optRaw : (EXV_CIR[m.opt] || (m.opt || ''));
        const hasPaper = (typeof mbExamHasYear === 'function') ? mbExamHasYear(m.year) : true;
        return `<button type="button" data-exam="${escHtml(q.id)}:${mi}" onclick="event.stopPropagation();mbExamOpen('${escAttr(q.id)}',${mi})" title="${m.year}년 시험지 ${m.no || ''}번" class="jn-exam bg-gray-100 text-gray-600 text-[11px] font-bold px-2 py-0.5 rounded-md border border-gray-200 whitespace-nowrap"${hasPaper ? '' : ' style="opacity:.45"'}>${m.year}:${m.no || ''}:${escHtml(opt)}</button>`;
    }).join('');
}
function jnExamYear(subject, label) { return subject === '변리사 기출' ? ((/^(\d{4})년/.exec(String(label || '')) || [])[1] || '') : ''; }
/* 문항 채점 칸 — 시험지 회독(ox_exam_rounds)마다 한 칸 · 누르면 옆에 출처(지우기 없음) */
function jnExamCells(y, no) {
    const R = exvRounds()[y] || [];
    const cor = exvCorrect(y, no);
    const md = d => { const t = recStripDay(d); return t ? (t.getMonth() + 1) + '/' + t.getDate() : String(d || ''); };
    return R.map((r, i) => {
        const p = r.picks ? +r.picks[no] : 0;
        const ok = p && cor.ans.length ? cor.ans.includes(p) : null;
        const tip = md(r.date) + ' · ' + (i + 1) + '회독째 · ' + (p ? '고른 ' + EXV_CIR[p] : '안 고름') + (cor.ans.length ? ' · 정답 ' + cor.ans.map(n => EXV_CIR[n]).join('·') : '');
        return `<button type="button" class="jx-cell ${!p ? 'na' : ok ? 'o' : 'x'}" data-tip="${escHtml(tip)}" onclick="event.stopPropagation();jxCellTap(this)">${!p ? '·' : ok ? 'O' : 'X'}</button>`;
    }).join('');
}
/* 기출 해의 정리 창 몸통 — 문번마다 「문제 N」 구분 줄(+ 문항 채점 칸) · 그 안 행은 선지 차례(ㄱ·ㄴ·ㄷ / ①~⑤) · 시험지 꼴은 안 넣는다(§F-2) */
function jnExamBodyHTML(y, l, ids) {
    const by = new Map();
    ids.forEach(id => {
        const q = quizData.find(x => x.id === id);
        if (!q) return;
        const m = (q.examMeta || []).find(x => String(x.year) === String(y)) || { no: q.examNo, opt: q.examOpt };
        const no = +m.no || 0;
        if (!by.has(no)) by.set(no, []);
        by.get(no).push({ q: q, opt: +m.opt || 0 });
    });
    const nos = [...by.keys()].sort((a, b) => a - b);
    let html = `<div data-jnh="1" class="px-3.5 py-1.5 bg-slate-50 border-b border-gray-100 text-[11px] font-extrabold text-indigo-800">${escHtml(jnNameOf(l))} · ${exvYearQCount(y)}문항 · ${ids.length}지문</div>`;
    nos.forEach(no => {
        html += `<div class="jx-no" data-jxno="${no}"><span>문제 ${no}</span><span class="jx-cells">${jnExamCells(y, no)}</span><span class="jx-info hide"></span></div>`;
        by.get(no).sort((a, b) => a.opt - b.opt).forEach(r => { html += jnRowHTML(r.q); });
    });
    return html;
}
function jxCellTap(b) {
    const row = b.closest('.jx-no'), info = row && row.querySelector('.jx-info');
    if (!info) return;
    row.querySelectorAll('.jx-cell').forEach(x => x.classList.remove('rec-on'));
    if (info.dataset.on === b.dataset.tip && !info.classList.contains('hide')) { info.classList.add('hide'); info.dataset.on = ''; return; }
    b.classList.add('rec-on'); info.dataset.on = b.dataset.tip; info.textContent = b.dataset.tip; info.classList.remove('hide');
}
