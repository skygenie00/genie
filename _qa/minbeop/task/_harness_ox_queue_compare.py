# -*- coding: utf-8 -*-
r"""_task_ox_queue_compare §B 관문 — 민법OX 채점 창 · 회독 비교 창: ⚡ 빠른 실행(약점 등) 「지난 결과」(문항마다 마지막 · 모든 열쇠) · 계속 틀림 · 극복함 · _task_cloud_batch_1010 클라우드 ①

  python _harness_ox_queue_compare.py [--new <앱>] [--base <판 = 7299ec3>] [--only Q1,…] [--spd <studyplandata>] [--rec <기록.json>] [--tw <Tailwind 사본>] [--res <결과>] [--shots <그림>]

  NEW = genie 작업트리 minbeop/index.html · BASE = 바탕 7299ec3(헛잣대 — ⚡ 지난 줄 다 회색 · 계속 틀림 · 극복함 둘 다 「없음」 → FAIL 이어야)
  데이터 = 문항 studyplandata 현행 · 기록 = 칸마다 갈아 끼움(가짜 GitHub · PUT 메모리 · OL = _ox_live.py)
    Q1 · Q4 = 빈 원격 기록 + 쪽 안 짜 맞춘 기록 · Q2 · Q3 · Q5 = studyplandata ddc6ea7(10/10 00:25) minbeop/기록.json 그대로(--rec <파일> 로 갈음)
  기기 = PC 1100×800(마우스) · 폰 390×844(hasTouch · 모바일 · 톡 = CDP Input.dispatchTouchEvent) · 엔진 = Chromium
  ⚠ 문항 · 해설 글은 출력하지 않는다(D11) — 문항 ID · 번호 · 색 · 수만
  관문:
    Q1 짜 맞춘 기록 — 단원 회독(A ✗ · B ✗ · C ○) · ⚡ 약점 지난 회독(다른 문항 E · F) → 첫 화면 「🔥 약점」 진짜 누름 → A ✗ · B ○ · C ✗ · D(처음) O/X 진짜 누름
        → 「채점 ✓」 진짜 누름(마지막 쪽 = 저장 먼저) → 채점 창 지난 결과 A 빨강 · B 빨강 · C 초록 · D 회색 · 계속 틀림 = A · 극복함 = B · 회독 비교 창(⚡ 열쇠) 같은 값
    Q2 실데이터 ⚡ 약점 둘째 회독(10/10 · 17 문항) 채점 창 다시 그림(저장된 회독 = 이번) — 지난 결과 빨강 = 3(2) Q5517 · 5 Q5681 · 158 Q0705 · 83 Q0684 · 나머지 13 초록 ·
        계속 틀림 = 3(2) · 극복함 = 5 · 158 · 83 · 148(Q0695 지난 O → 이번 X) 어느 쪽도 아님 · 회독 비교 창 같은 값 · 하네스가 기록에서 따로 센 값 = 지시서 값
    Q3 단원 회독(⚡ 아님) 실데이터 표본 셋 + 짜 맞춘 단원 하나(옛 식 계속 틀림 A · 극복함 B) — 채점 창 · 회독 비교 창 = 바탕과 글(HTML) · 칩 색 · 두 줄 · 그림(창 안 사진 화소) 같음
    Q4 같은 회독 두 번 안 셈 — Q1 채점 뒤 ⚡ 열쇠 회독 = 2(저장 한 번) · 「이번 (2회독) · ✓ 저장됨」 · 지난 결과에 이번 값 안 섞임(C 초록 · D 회색) · 채점 창 다시 열기 = 같은 값
    Q5 화면 훑기 — 채점 창 · 회독 비교 창(Q2 17 칩 · PC · 폰) 넘침 · 잘림 · 화면 밖 0 · 페이지 오류 0
  결과 = 화면 PASS/FAIL/INFO 줄 · --res(기본 = 임시 폴더 · _qa 에 결과를 쓰지 않는다)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402,F401 — --mode · --snap-in · --snap-out 을 뗀다
import json, os, re, subprocess, sys, tempfile, time, traceback   # noqa: E402
_sys_r.path.append(_os_r.path.dirname(_os_r.path.abspath(__file__)))
import _ox_live as OL   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEWF = ARG('--new', _roots.genie('minbeop', 'index.html'))
BASE = ARG('--base', '7299ec3')
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
TMPD = os.path.join(tempfile.gettempdir(), 'h_ox_queue_compare')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_ox_queue_compare_result.txt'))
OL.conf(spd=ARG('--spd', _roots.spd()), tw=ARG('--tw'), shots=ARG('--shots', os.path.join(TMPD, 'shots')))
GATE = QC.GATE   # gate = 바탕을 띄워 헛잣대 · regress · smoke = 새 판만(바탕 풀기 · 띄우기 0 · 「= 바탕」 칸은 기준 스냅샷)
if GATE:
    QC.sub('git:show-app')
SRC = {'NEW': OL.app_src(NEWF)}
if GATE:
    SRC['BASE'] = OL.app_src(BASE)
VERS = tuple(SRC)
OL.ON_LAUNCH = lambda tag: QC.launch('base' if tag == 'BASE' else 'new')
REC_REV = 'ddc6ea7'
QS = '⚡빠른실행'
QN = '🔥 약점 (틀림+헷갈림)'
QK = QS + '||' + QN + '||all||all'
EMPTY_REC = json.dumps({'v': 1, 'savedAt': '2026-10-01T00:00:00.000Z', 'by': '하네스', 'data': {}, 'u': {}, 'gone': {}}).encode('utf-8')
# 지시서 §B-2 실데이터 기대값(채팅 10/10 00:3x 잼) — 17 문항 중
EXP2 = {'n': 17, 'red': ['Q5517', 'Q5681', 'Q0705', 'Q0684'], 'always': ['Q5517'], 'fixed': ['Q5681', 'Q0705', 'Q0684'], 'neither': 'Q0695'}
RES = []
STEP = {}
T0 = time.time()


def want(c):
    return (not ONLY or c in ONLY) and (not QC.SMOKE or c == 'Q2')   # smoke = Q2 PC 한 칸(실데이터 기대값)


def _s(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


def R(g, name, new, base=None, d='', yard=True):
    RES.append(dict(g=g, name=name, new=new, base=base, yard=yard, d=d))
    tag = 'INFO' if new is None else ('PASS' if new else 'FAIL')
    yb = '' if base is None else (' · 바탕 ' + (('PASS(바탕도 같음)' if yard else 'PASS') if base else 'FAIL'))
    print('%s | %s · %s%s | %s' % (tag, g, name, yb, _s(d)[:1000]), flush=True)


def rec_real():
    f = ARG('--rec')
    if f:
        return open(f, 'rb').read()
    QC.sub('git:show-rec')
    b = subprocess.run(['git', '-C', OL.CONF['spd'], 'show', REC_REV + ':minbeop/기록.json'], capture_output=True).stdout
    if not b:   # 판 못 박음 — SPD_ROOT 클론에 그 판이 없으면 종료 3(_harness_ox_home_tidy 와 같은 꼴)
        print('FAIL | Q0 · 기록 %s 판을 못 읽었다 — --rec <기록.json> 으로 주거나 studyplandata 클론에 그 판이 있어야 한다' % REC_REV, flush=True)
        sys.exit(3)
    return b


def prior_last_py(rec, key, idx):
    """하네스 따로 셈 — 기록의 모든 열쇠 · 모든 회독(key·idx 회독 뺌)을 날짜 차례(같은 날은 쌓인 차례)로 훑어 문항마다 마지막 결과"""
    ch = (rec.get('data') or {}).get('ox_chap_history') or {}
    if isinstance(ch, str):
        ch = json.loads(ch)

    def dn(s):
        n = re.findall(r'\d+', s or '')
        if len(n) < 3:
            return 0
        if len(n[0]) == 4:
            return int(n[0]) * 10000 + int(n[1]) * 100 + int(n[2])
        if len(n[2]) == 4:
            return int(n[2]) * 10000 + int(n[0]) * 100 + int(n[1])
        return 0
    rows = []
    for k, L in ch.items():
        for i, a in enumerate(L if isinstance(L, list) else []):
            if k == key and i == idx:
                continue
            for qid, v in ((a or {}).get('marks') or {}).items():
                if v is True or v is False:
                    rows.append((dn(a.get('date')), qid, v))
    rows.sort(key=lambda r: r[0])   # 안정 정렬 — 같은 날은 쌓인 차례(같은 열쇠 안은 회독 차례)
    last = {}
    for _, qid, v in rows:
        last[qid] = v
    return last, ch


READ_JS = r"""(()=>{const col=e=>/(^|\s)bg-red-100(\s|$)/.test(e.className)?'R':/(^|\s)bg-green-50(\s|$)/.test(e.className)?'G':/(^|\s)bg-gray-50(\s|$)/.test(e.className)?'-':'?';
 const idOf=e=>{const m=/\('([^']+)'\)/.exec(e.getAttribute('onclick')||'');return m?m[1]:null};
 const chips=box=>box?[...box.querySelectorAll('[style*="min-width:1.6rem"]')].map(e=>({id:idOf(e),l:__H.tx(e),c:col(e)})):null;
 const lab=(b,t)=>{const s=[...b.querySelectorAll('span')].find(x=>__H.tx(x)===t);return s?chips(s.nextElementSibling):null};
 const out={};
 const w=document.getElementById('oxwin-grade');
 if(w&&__H.vis(w)){const b=w.querySelector('.oxwin-body');const pl=b.querySelector('[data-prior-last]');
   out.grade={prior:pl?chips(pl):null,always:lab(b,'계속 틀림'),fixed:lab(b,'극복함'),
     heads:[...b.querySelectorAll('div')].filter(d=>/text-\[10px\]/.test(d.className)&&/(회독|지난 결과)/.test(__H.tx(d))&&!d.querySelector('div')).map(d=>__H.tx(d).replace(/\d{4}\. \d+\. \d+\./,'(날짜)')),
     rows:[...b.querySelectorAll('.mb-1\\.5')].map(d=>chips(d).map(c=>c.c).join('')),html:b.innerHTML}}
 const m=document.getElementById('compare-modal');
 if(m&&!m.classList.contains('hide')){const b=document.getElementById('compare-body');
   out.cmp={prior:lab(b,'지난 결과'),always:lab(b,'계속 틀림'),fixed:lab(b,'극복함'),atts:[...b.querySelectorAll(':scope > div.mb-3')].map(d=>chips(d.querySelector('.p-2')||d).map(c=>c.c).join('')),html:b.innerHTML}}
 return out})()"""


def cmap(L):
    return {c['id']: c['c'] for c in (L or [])}


def ids(L):
    return None if L is None else [c['id'] for c in L]


# ---------- Q1 · Q4 — 짜 맞춘 기록 · 진짜 누름 ----------
SEED_JS = r"""([qs,qn,qk])=>{const P=quizData.filter(q=>!q.pending&&(q.a==='O'||q.a==='X'));
 const [A,B,C,D,E,F]=P.slice(0,6),lb=q=>`${q.displayNo??q.probNum}${q.subNum||''}`,L=(...a)=>Object.fromEntries(a.map(q=>[q.id,lb(q)]));
 const UK=String(A.subject||'민법총칙')+'||하네스 단원||all||all',h={};
 h[UK]=[{score:1,total:3,date:'2026. 10. 1.',marks:{[A.id]:false,[B.id]:false,[C.id]:true},labels:L(A,B,C)},
        {score:1,total:1,date:'2026. 10. 3.',marks:{[F.id]:true},labels:L(F)}];
 h[qk]=[{score:1,total:2,date:'2026. 10. 2.',marks:{[E.id]:true,[F.id]:false},labels:L(E,F)}];
 localStorage.setItem('ox_chap_history',JSON.stringify(h));
 localStorage.setItem('ox_q_history',JSON.stringify({[A.id]:false,[B.id]:false,[C.id]:true,[E.id]:true,[F.id]:true}));
 localStorage.setItem('ox_q_tags',JSON.stringify({[C.id]:{confuse:true},[D.id]:{confuse:true}}));
 try{renderDashboard()}catch(e){}
 return {A:[A.id,A.a],B:[B.id,B.a],C:[C.id,C.a],D:[D.id,D.a],E:E.id,F:F.id,weak:weakQueueItems().map(q=>q.id)}}"""


def tap(p, sel):
    at = p.ev("(s)=>__H.hit(document.querySelector(s))", sel)
    if not at or not at.get('on'):
        return at
    p.press(at['cx'], at['cy'])
    return at


def q1(br, v, dev):
    p = OL.Live(br, v, SRC[v], dev, remote=OL.Remote({'minbeop/기록.json': EMPTY_REC}))
    try:
        sd = p.ev(SEED_JS, [QS, QN, QK])
        want_ = {'A': False, 'B': True, 'C': False, 'D': True}   # 이번 채점
        b_at = tap(p, 'button[onclick="startWeakQueue()"]')       # 첫 화면 「🔥 약점」 진짜 누름
        p.wait(900)
        q = p.ev("(()=>({subj:currentSubject,lab:currentChapterLabel,ids:currentFilteredData.map(q=>q.id)}))()")
        picks = {}
        for k in 'ABCD':
            qid, a = sd[k]
            pick = a if want_[k] else ('X' if a == 'O' else 'O')
            at = tap(p, '#ox-%s-%s' % (pick, qid))
            p.wait(150)
            picks[k] = p.ev("([i,v])=>{const r=document.querySelector(`input[name=\"answer_${i}\"][value=\"${v}\"]`);return !!(r&&r.checked)}", [qid, pick]) and bool(at and at.get('on'))
        g_at = tap(p, '#action-btn')                              # 「채점 ✓」 진짜 누름(마지막 쪽 = 채점과 함께 저장)
        p.pg.wait_for_function("()=>{const w=document.getElementById('oxwin-grade');return !!w&&__H.vis(w)}", timeout=30000)
        p.wait(500)
        r1 = p.ev(READ_JS)
        p.shot('q1_grade_%s_%s' % (v, dev['name']))
        hist = p.ev("(k)=>{const a=(JSON.parse(localStorage.getItem('ox_chap_history')||'{}')[k]||[]);return {n:a.length,last:a.length?a[a.length-1].marks:null}}", QK)
        p.ev("(()=>reopenGradeModal())()")                       # 채점 창 다시 열기(같은 회독 · 같은 값이어야)
        p.wait(300)
        r2 = p.ev(READ_JS)
        p.ev("([s,l])=>openCompareModal(s,l)", [QS, QN])          # 회독 비교 창(⚡ 열쇠 — 첫 화면에 들어가는 줄이 없어 함수로 엶)
        p.wait(400)
        r3 = p.ev(READ_JS)
        p.shot('q1_cmp_%s_%s' % (v, dev['name']))
        errs = p.errors()[:3]
    finally:
        p.close()
    A, B, C, D = (sd[k][0] for k in 'ABCD')
    exp_c = {A: 'R', B: 'R', C: 'G', D: '-'}
    g, c = r1.get('grade') or {}, r3.get('cmp') or {}
    d1 = {'약점 큐(누른 뒤)': {'열쇠 맞음': q['subj'] == QS and q['lab'] == QN, '문항 = A B C D': q['ids'] == [A, B, C, D], '「🔥 약점」 누름 자리': bool(b_at and b_at.get('on'))},
          'O/X 누름': picks, '「채점 ✓」 누름 자리': bool(g_at and g_at.get('on')),
          '채점 창': {'지난 결과': {k: cmap(g.get('prior')).get(sd[k][0]) for k in 'ABCD'}, '계속 틀림': ids(g.get('always')), '극복함': ids(g.get('fixed')), '줄 머리': g.get('heads')},
          '회독 비교 창': {'지난 결과': {k: cmap(c.get('prior')).get(sd[k][0]) for k in 'ABCD'}, '계속 틀림': ids(c.get('always')), '극복함': ids(c.get('fixed')), '회독 칩 색': c.get('atts')},
          '기대': {'지난 결과': {'A': 'R', 'B': 'R', 'C': 'G', 'D': '-'}, '계속 틀림': [A], '극복함': [B]}, '오류': errs}
    ok1 = (all(d1['약점 큐(누른 뒤)'].values()) and all(picks.values()) and d1['「채점 ✓」 누름 자리']
           and cmap(g.get('prior')) == exp_c and ids(g.get('always')) == [A] and ids(g.get('fixed')) == [B]
           and cmap(c.get('prior')) == exp_c and ids(c.get('always')) == [A] and ids(c.get('fixed')) == [B] and not errs)
    g2 = r2.get('grade') or {}
    d4 = {'⚡ 열쇠 회독 수': hist['n'], '이번 회독 marks = 누른 값': hist['last'] == {A: False, B: True, C: False, D: True},
          '줄 머리': g.get('heads'), '이번 값 안 섞임(C 초록 · D 회색)': cmap(g.get('prior')).get(C) == 'G' and cmap(g.get('prior')).get(D) == '-',
          '다시 열기 = 같은 값': bool(g) and {k: g2.get(k) for k in ('prior', 'always', 'fixed', 'heads')} == {k: g.get(k) for k in ('prior', 'always', 'fixed', 'heads')}}
    ok4 = (hist['n'] == 2 and d4['이번 회독 marks = 누른 값'] and any(h.startswith('이번 (2회독) · ✓ 저장됨') for h in (g.get('heads') or []))
           and d4['이번 값 안 섞임(C 초록 · D 회색)'] and d4['다시 열기 = 같은 값'])
    return (ok1, d1), (ok4, d4)


# ---------- Q2 · Q5 — 실데이터 ddc6ea7 ----------
RERENDER_JS = r"""([qs,qn,qk])=>{document.getElementById('source-filter').value='all';document.getElementById('review-filter').value='all';
 const L=(JSON.parse(localStorage.getItem('ox_chap_history')||'{}')[qk])||[];const h=L[L.length-1];if(!h)return null;
 const items=Object.keys(h.marks||{}).map(id=>quizData.find(q=>String(q.id)===String(id))).filter(Boolean);
 startVirtualQuiz(qn,items);                                   /* 채점한 그 판 화면(17 문항) 위에 */
 const results=items.map(it=>({item:it,picked:null,isCorrect:h.marks[it.id]===true}));
 chapterSaved=qk;                                              /* 마지막 쪽 채점 = 저장이 먼저 — 저장된 회독이 이번 */
 const sc=results.filter(r=>r.isCorrect).length;lastGradeResults={results,score:sc,total:results.length};showGradeModal(results,sc,results.length);
 return {n:results.length,hist:L.length,ids:items.map(q=>String(q.id))}}"""

SWEEP_JS = r"""(sel)=>{const out=[];const R=document.querySelector(sel);if(!R||!__H.vis(R))return ['(없음) '+sel];
 const rb=R.getBoundingClientRect();if(rb.left<-1||rb.right>innerWidth+1||rb.top<-1)out.push('창 화면 밖 '+[Math.round(rb.left),Math.round(rb.right),Math.round(rb.top)]);
 if(document.scrollingElement.scrollWidth>innerWidth+1)out.push('page-hscroll');
 [R,...R.querySelectorAll('*')].forEach(e=>{if(!__H.vis(e))return;const cs=getComputedStyle(e),b=e.getBoundingClientRect();
   if((cs.overflowX==='auto'||cs.overflowX==='scroll'||cs.overflowX==='hidden')&&e.scrollWidth>e.clientWidth+1&&e.clientWidth>0)out.push('가로 넘침:'+e.tagName+'.'+String(e.className).slice(0,24));
   if(b.width>0&&(b.right>rb.right+1||b.left<rb.left-1))out.push('창 밖:'+e.tagName+'.'+String(e.className).slice(0,24))});
 R.querySelectorAll('[style*="min-width:1.6rem"]').forEach(e=>{const b=e.getBoundingClientRect();if(b.width<10||b.height<8)out.push('칩 찌그러짐 '+__H.tx(e))});
 return [...new Set(out)].slice(0,8)}"""


def q2(br, v, dev, rec_b, exp_py):
    p = OL.Live(br, v, SRC[v], dev, remote=OL.Remote({'minbeop/기록.json': rec_b}))
    sweep = None
    try:
        rr = p.ev(RERENDER_JS, [QS, QN, QK])
        p.wait(600)
        r1 = p.ev(READ_JS)
        p.shot('q2_grade_%s_%s' % (v, dev['name']))
        sw_g = p.ev(SWEEP_JS, '#oxwin-grade')
        p.ev("([s,l])=>{oxWinClose&&document.getElementById('oxwin-grade')&&(document.getElementById('oxwin-grade').style.display='none');openCompareModal(s,l)}", [QS, QN])
        p.wait(500)
        r3 = p.ev(READ_JS)
        p.shot('q2_cmp_%s_%s' % (v, dev['name']))
        sw_c = p.ev(SWEEP_JS, '#compare-modal > div')
        errs = p.errors()[:3]
        sweep = {'채점 창': sw_g, '회독 비교 창': sw_c, '오류': errs}
    finally:
        p.close()
    g, c = r1.get('grade') or {}, r3.get('cmp') or {}
    gi = cmap(g.get('prior'))
    ids17 = (rr or {}).get('ids') or []
    exp_c = {i: ('R' if i in EXP2['red'] else 'G') for i in ids17}
    d = {'다시 그린 문항': (rr or {}).get('n'), '⚡ 열쇠 회독': (rr or {}).get('hist'),
         '채점 창 지난 결과': {'빨강': [i for i in ids17 if gi.get(i) == 'R'], '초록 수': sum(1 for i in ids17 if gi.get(i) == 'G'), '회색 수': sum(1 for i in ids17 if gi.get(i) == '-'),
                       '번호(빨강)': [x['l'] for x in (g.get('prior') or []) if x['c'] == 'R']},
         '계속 틀림': ids(g.get('always')), '극복함': ids(g.get('fixed')), 'Q0695 어느 쪽도 아님': EXP2['neither'] not in (ids(g.get('always')) or []) + (ids(g.get('fixed')) or []),
         '회독 비교 창(칩 = 번호 차례)': {'지난 결과 = 채점 창': cmap(c.get('prior')) == gi and bool(gi), '계속 틀림': ids(c.get('always')), '극복함': ids(c.get('fixed'))},
         '바탕 꼴(지난 줄 칩 색)': None if g.get('prior') is not None else {'줄 머리': g.get('heads'), '줄 칩 색': g.get('rows')},
         '하네스 따로 셈 = 지시서 값': exp_py, '오류': (sweep or {}).get('오류')}
    ok = ((rr or {}).get('n') == EXP2['n'] and gi == exp_c and ids(g.get('always')) == EXP2['always'] and ids(g.get('fixed')) == EXP2['fixed']
          and d['Q0695 어느 쪽도 아님'] and cmap(c.get('prior')) == exp_c and sorted(ids(c.get('always')) or []) == sorted(EXP2['always'])
          and sorted(ids(c.get('fixed')) or []) == sorted(EXP2['fixed'])   # 회독 비교 창 칩 차례 = 번호 차례(그 창 옛 규칙) → 모임으로 맞댐
          and exp_py is True and not d['오류'])
    return (ok, d), sweep


# ---------- Q3 — 단원 회독 표본 셋 = 바탕 ----------
def unit_samples(ch, quiz_ids):
    """단원 회독 표본 셋 — 문항별 기록이 있는 회독 둘 이상 · 마지막 회독 문항이 다 데이터에 있음 ·
    옛 식(지난 회독 다 틀림 · 한 번이라도 틀림)으로 계속 틀림 · 극복함이 있는 단원 먼저 → 마지막 회독 문항 많은 차례 → 열쇠 차례"""
    ks = []
    for k in sorted(ch):
        L = ch[k] if isinstance(ch[k], list) else []
        if k.startswith(QS) or not k.endswith('||all||all'):
            continue
        wm = [a for a in L if (a or {}).get('marks')]
        mk = (L[-1].get('marks') or {}) if L else {}
        if len(wm) >= 2 and mk and all(i in quiz_ids for i in mk):
            pri = wm[:-1]
            al = [i for i in mk if mk[i] is False and all((h.get('marks') or {}).get(i) is False for h in pri)]
            fx = [i for i in mk if mk[i] is True and any((h.get('marks') or {}).get(i) is False for h in pri)]
            ks.append((0 if (al and fx) else 1 if (al or fx) else 2, -len(mk), k))
    return [k for _, _, k in sorted(ks)[:3]]


UNIT_JS = r"""(k)=>{const [s,l]=k.split('||');document.getElementById('source-filter').value='all';document.getElementById('review-filter').value='all';
 const L=(JSON.parse(localStorage.getItem('ox_chap_history')||'{}')[k])||[];const h=L[L.length-1];
 const results=Object.keys(h.marks||{}).map(id=>({item:quizData.find(q=>String(q.id)===String(id)),picked:null,isCorrect:h.marks[id]===true})).filter(r=>r.item);
 currentSubject=s;currentChapterLabel=l;chapterSaved=k;
 const sc=results.filter(r=>r.isCorrect).length;lastGradeResults={results,score:sc,total:results.length};showGradeModal(results,sc,results.length);return results.length}"""


# 표본 넷째 = 짜 맞춘 단원 회독(실데이터 표본에 계속 틀림 · 극복함이 없을 때도 옛 식 두 줄이 차는 단원) — 1회독 A ✗ B ✗ C ○ → 2회독 A ✗ B ○ C ✗ = 계속 틀림 A · 극복함 B(옛 식)
SYN_UNIT_JS = r"""(()=>{const [A,B,C]=quizData.filter(q=>!q.pending).slice(0,3),lb=q=>`${q.displayNo??q.probNum}${q.subNum||''}`,L={[A.id]:lb(A),[B.id]:lb(B),[C.id]:lb(C)};
 const k=String(A.subject||'민법총칙')+'||하네스 단원 회독||all||all',all=JSON.parse(localStorage.getItem('ox_chap_history')||'{}');
 all[k]=[{score:1,total:3,date:'2026. 10. 1.',marks:{[A.id]:false,[B.id]:false,[C.id]:true},labels:L},{score:1,total:3,date:'2026. 10. 5.',marks:{[A.id]:false,[B.id]:true,[C.id]:false},labels:L}];
 localStorage.setItem('ox_chap_history',JSON.stringify(all));return k})()"""


def shot_stable(p, sel):
    last = None
    for _ in range(6):
        b = p.pg.locator(sel).screenshot(animations='disabled')
        if b == last:
            return b
        last = b
        p.wait(200)
    return last


def q3_run(br, v, dev, rec_b, keys):
    p = OL.Live(br, v, SRC[v], dev, remote=OL.Remote({'minbeop/기록.json': rec_b}))
    out = []
    try:
        for i, k in enumerate(list(keys) + [None]):
            if k is None:
                k = p.ev(SYN_UNIT_JS)
            n = p.ev(UNIT_JS, k)
            p.wait(500)
            g = (p.ev(READ_JS).get('grade') or {})
            gp = shot_stable(p, '#oxwin-grade .oxwin-body')   # 창 안(둥근 모서리 밖 뒤 화면 빼고) · 움직임 멈춤 · 두 번 같을 때까지
            p.ev("(()=>{const w=document.getElementById('oxwin-grade');if(w)w.style.display='none'})()")
            p.ev("(k)=>{const [s,l]=k.split('||');openCompareModal(s,l)}", k)
            p.wait(500)
            c = (p.ev(READ_JS).get('cmp') or {})
            cp = shot_stable(p, '#compare-body')
            p.ev("(()=>{closeCompareModal();const w=document.getElementById('oxwin-grade');if(w)w.remove()})()")
            p.wait(200)
            out.append({'n': n, 'g_html': g.get('html'), 'g_md5': OL.md5lf(g.get('html') or ''), 'c_md5': OL.md5lf(c.get('html') or ''), 'g_rows': g.get('rows'), 'g_heads': g.get('heads'), 'g_always': ids(g.get('always')), 'g_fixed': ids(g.get('fixed')),
                        'c_html': c.get('html'), 'c_atts': c.get('atts'), 'c_always': ids(c.get('always')), 'c_fixed': ids(c.get('fixed')), 'g_png': gp, 'c_png': cp})
        errs = p.errors()[:3]
    finally:
        p.close()
    return out, errs


def png_same(a, b):
    if a == b:
        return True
    try:
        from PIL import Image, ImageChops
        import io
        ia, ib = Image.open(io.BytesIO(a)).convert('RGB'), Image.open(io.BytesIO(b)).convert('RGB')
        return ia.size == ib.size and ImageChops.difference(ia, ib).getbbox() is None
    except Exception:
        return False


def main():
    os.makedirs(TMPD, exist_ok=True)
    rec_b = rec_real()
    rec = json.loads(rec_b.decode('utf-8'))
    R('Q0', '판 · 자리', None, None, {'NEW': NEWF, 'md5(LF)': {k: OL.md5lf(v) for k, v in SRC.items()}, 'BASE': BASE, 'SPD': OL.CONF['spd'], '기록': ARG('--rec') or ('studyplandata ' + REC_REV), 'tw': OL.CONF['tw']})
    # 지시서 값 = 하네스가 기록에서 따로 센 값인가(데이터 전제)
    ch0 = (rec.get('data') or {}).get('ox_chap_history') or {}
    ch0 = json.loads(ch0) if isinstance(ch0, str) else ch0
    L = ch0.get(QK) or []
    exp_py = None
    if L:
        last, _ = prior_last_py(rec, QK, len(L) - 1)
        mk = L[-1].get('marks') or {}
        red = [i for i in mk if last.get(i) is False]
        al = [i for i in mk if mk[i] is False and last.get(i) is False]
        fx = [i for i in mk if mk[i] is True and last.get(i) is False]
        exp_py = (len(mk) == EXP2['n'] and red == EXP2['red'] and al == EXP2['always'] and fx == EXP2['fixed']
                  and all(last.get(i) is True for i in mk if i not in EXP2['red']))
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        sweeps = {}
        if want('Q1') or want('Q4'):
            t1 = time.time()
            for dev in (OL.PC, OL.PH):
                res = {}
                for v in VERS:
                    try:
                        res[v] = q1(br, v, dev)
                    except Exception as e:
                        bad = (False, {'하네스 오류': str(e)[:300], 'tb': traceback.format_exc()[-500:]})
                        res[v] = (bad, bad)
                if want('Q1'):
                    R('Q1', '%s 짜 맞춘 기록 — 「🔥 약점」 · O/X · 「채점 ✓」 진짜 누름 → 지난 결과 A 빨강 · B 빨강 · C 초록 · D 회색 · 계속 틀림 A · 극복함 B · 회독 비교 창 같음' % dev['name'],
                      res['NEW'][0][0], res['BASE'][0][0] if 'BASE' in res else None, {k: x[0][1] for k, x in res.items()})
                if want('Q4'):
                    R('Q4', '%s 같은 회독 두 번 안 셈 — 저장 한 번(⚡ 회독 2) · 이번 (2회독) · ✓ 저장됨 · 지난 결과에 이번 값 안 섞임 · 다시 열기 같은 값' % dev['name'],
                      res['NEW'][1][0], res['BASE'][1][0] if 'BASE' in res else None, {k: x[1][1] for k, x in res.items()})
            STEP['Q1·Q4'] = round((time.time() - t1) / 60, 1)
        if want('Q2') or want('Q5'):
            t1 = time.time()
            for dev in ((OL.PC,) if QC.SMOKE else (OL.PC, OL.PH)):
                res = {}
                for v in VERS:
                    try:
                        res[v], sw = q2(br, v, dev, rec_b, exp_py)
                        if v == 'NEW':
                            sweeps[dev['name']] = sw
                    except Exception as e:
                        res[v] = (False, {'하네스 오류': str(e)[:300], 'tb': traceback.format_exc()[-500:]})
                if want('Q2'):
                    R('Q2', '%s 실데이터 %s ⚡ 약점 10/10 회독 채점 창 다시 그림 — 빨강 3(2) · 5 · 158 · 83 · 초록 13 · 계속 틀림 3(2) · 극복함 5 · 158 · 83 · 회독 비교 창 같음' % (dev['name'], REC_REV),
                      res['NEW'][0], res['BASE'][0] if 'BASE' in res else None, {k: x[1] for k, x in res.items()})
            STEP['Q2'] = round((time.time() - t1) / 60, 1)
        if want('Q3'):
            t1 = time.time()
            quiz_ids = None
            for dev in (OL.PC, OL.PH):
                try:
                    if quiz_ids is None:
                        p = OL.Live(br, 'NEW', SRC['NEW'], OL.PC, remote=OL.Remote({'minbeop/기록.json': EMPTY_REC}), wait_sync=False)
                        quiz_ids = set(p.ev("quizData.map(q=>String(q.id))"))
                        p.close()
                    keys = unit_samples(ch0, quiz_ids)
                    a, ea = q3_run(br, 'NEW', dev, rec_b, keys)
                    if GATE:
                        b, eb = q3_run(br, 'BASE', dev, rec_b, keys)
                    else:   # regress — 바탕 안 띄움 · 「= 바탕」 = 기준 스냅샷(앞 인도판에서 잰 글 · 칩 값)
                        b = [dict(x, g_md5=QC.base('Q3.g@%s#%d' % (dev['name'], i), x['g_md5']), c_md5=QC.base('Q3.c@%s#%d' % (dev['name'], i), x['c_md5']))
                             for i, x in enumerate(a)]
                    for i, x in enumerate(a):
                        if GATE:   # 다음 regress 의 기준(스냅샷 · 글 md5 만)
                            QC.base('Q3.g@%s#%d' % (dev['name'], i), x['g_md5'])
                            QC.base('Q3.c@%s#%d' % (dev['name'], i), x['c_md5'])
                    per = []
                    for i, k in enumerate(list(keys) + ['(짜 맞춤)']):
                        x, y = a[i], b[i]
                        for nm in ('g_png', 'c_png'):   # 그림이 다르면 둘 다 남김(--shots)
                            if GATE and OL.CONF['shots'] and not png_same(x[nm], y[nm]):
                                os.makedirs(OL.CONF['shots'], exist_ok=True)
                                for tg, z in (('NEW', x), ('BASE', y)):
                                    open(os.path.join(OL.CONF['shots'], 'q3_diff_%s_%d_%s_%s.png' % (dev['name'], i + 1, nm, tg)), 'wb').write(z[nm])
                        per.append({'표본': i + 1 if i < len(keys) else '짜 맞춘 단원', '문항': x['n'], '회독': len(x['c_atts'] or []), '채점 창 글 같음': x['g_md5'] == y['g_md5'], '채점 창 그림 같음': png_same(x['g_png'], y['g_png']),
                                    '회독 비교 창 글 같음': x['c_md5'] == y['c_md5'], '회독 비교 창 그림 같음': png_same(x['c_png'], y['c_png']),
                                    '칩 색 · 두 줄 같음': (x['g_rows'], x['g_always'], x['g_fixed'], x['c_atts'], x['c_always'], x['c_fixed']) == (y['g_rows'], y['g_always'], y['g_fixed'], y['c_atts'], y['c_always'], y['c_fixed']),
                                    '「지난 결과」 줄 없음': '지난 결과' not in (x['g_html'] or '') and '지난 결과' not in (x['c_html'] or ''),
                                    '계속 틀림 · 극복함 수(채점 창)': [len(x['g_always'] or []), len(x['g_fixed'] or [])]})
                    ok = len(keys) == 3 and per[-1]['계속 틀림 · 극복함 수(채점 창)'] == [1, 1] and all(all(v for k2, v in q.items() if k2 not in ('표본', '문항', '회독', '계속 틀림 · 극복함 수(채점 창)')) for q in per) and not ea
                    d = {'표본': per, '오류': ea}
                except Exception as e:
                    ok, d = False, {'하네스 오류': str(e)[:300], 'tb': traceback.format_exc()[-500:]}
                R('Q3', '%s 단원 회독 표본 셋 — 채점 창 · 회독 비교 창 = 바탕(글 · 그림 · 칩 색 · 두 줄)' % dev['name'], ok, None, d, yard=False)
            STEP['Q3'] = round((time.time() - t1) / 60, 1)
        if want('Q5'):
            for dev in (OL.PC, OL.PH):
                sw = sweeps.get(dev['name'])
                ok = bool(sw) and not sw['채점 창'] and not sw['회독 비교 창'] and not sw['오류']
                R('Q5', '%s 화면 훑기 — 채점 창 · 회독 비교 창(17 칩) 넘침 · 잘림 · 화면 밖 0 · 오류 0' % dev['name'], ok, None, sw, yard=False)
        br.close()
    nf = [r for r in RES if r['new'] is False]
    yard = [r for r in RES if r['yard'] and r['base'] is not None and r['new'] is not None]
    R('합계', '합계', None, None, {'PASS': sum(1 for r in RES if r['new'] is True), 'FAIL': len(nf), 'FAIL 칸': [r['g'] + ' ' + r['name'][:24] for r in nf],
                                  '헛잣대(바탕 FAIL)': '%d/%d' % (sum(1 for r in yard if r['base'] is False), len(yard)), '단계(분)': STEP, '전체(분)': round((time.time() - T0) / 60, 1)})
    try:
        with open(OUTF, 'w', encoding='utf-8') as f:
            for r in RES:
                f.write(json.dumps(r, ensure_ascii=False, default=str) + '\n')
    except Exception:
        pass
    sys.exit(1 if nf else 0)


if __name__ == '__main__':
    main()
