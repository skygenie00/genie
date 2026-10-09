# -*- coding: utf-8 -*-
r"""_task_search_all §B 관문(민법 몫) — 민법OX 검색 결과를 자르지 않고 다 보이기(runSearch · linkSearch · lwFind · runSearchOmr) · _task_cloud_batch_1010 클라우드 ①

  python _harness_ox_search_all.py [--new <앱>] [--base <판 = 7299ec3>] [--only S1,S2,…] [--spd <studyplandata>] [--tw <Tailwind 사본>] [--res <결과>] [--shots <그림>]

  NEW = genie 작업트리 minbeop/index.html · BASE = 바탕 7299ec3(헛잣대 — 100 · 30 · 60 에서 멈춤 → FAIL 이어야)
  데이터 = studyplandata 현행(문항마스터 · 기록 · 정리OMR 그림 · 가짜 GitHub · PUT 메모리 · OL = _ox_live.py) · 개인 문항 · 해설 글은 출력하지 않음(ID · 수만)
  기기 = PC 1100×800(마우스 휠) · 폰 390×844(hasTouch · 모바일 · 굴림 = CDP 손가락 밀기) · 엔진 = Chromium(WebKit 굴림 칸은 로컬 몫)
  기대 수 = 같은 검색어로 데이터를 하네스가 직접 거른 수(앱 거르기 식과 같은 식 · 쪽 안에서 따로 셈 · 정리OMR 은 파이썬이 쪽 글자를 같은 줄 묶음으로 셈)
  관문:
    S1 검색 칸 「대위」(runSearch · PC · 폰) — 셈 글 = 기대 수 · 처음 100 줄 · 「상위 N건만」 글 0 · 끝까지 굴려 줄 수 = 기대 수 · 겹친 줄 0 · 첫 · 끝 줄 = 기대 차례 · 끝 줄 누름 = 그 문항 팝업
    S2 연결 창(lwOpen 찾기 · lwFind) — 30 넘는 검색어(착수 때 고름) · 셈 보임 · 끝까지 굴려 다 붙음 · 차례
    S3 근거 창(문항 팝업 근거 줄 🔍 · linkSearch geunge) — 100 넘고 300 안쪽 검색어(착수 때 고름) · 셈 보임 · 처음 100 · 끝까지 굴려 다 붙음 · 차례 ·
       칸 다시 누름(같은 검색어 다시 그림) = 보던 줄 수 · 굴린 자리 그대로
    S4 정리OMR 찾기(runSearchOmr · 뷰어 = oxCoord.open) — 쪽 그림 다 받은 뒤 · 100 넘고 300 안쪽 검색어 · 셈 = 기대 수 · 처음 100 · 끝까지 굴려 다 붙음(옛 = 60 건에서 멈춤 · 12 줄 + 「더 보기」)
    S5 검색어 바꾸기(긴 결과를 둘째 100 줄까지 굴리는 중 새 검색어 · PC · 폰) — 옛 줄 0 · 새 결과 첫 100 줄 · 통 맨 위(굴림 0) · 새 결과 끝까지 = 기대(옛 관찰자가 옛 줄을 안 붙임)
    S6 첫 그림 빠르기 — 검색 칸 입력 → 첫 100 줄 배치(layout)까지(세 번 가운데 값) 새 판 ≤ 바탕 × 1.2 · 연결 찾기 · 근거 찾기(끝까지 찾음 · 디바운스 120ms 안) 시간 = INFO
    S7 화면 훑기 — 검색 결과(PC · 폰) · 연결 창 결과 넘침 · 잘림 0 · 페이지 오류 0
  결과 = 화면 PASS/FAIL/INFO 줄 · --res(기본 = 임시 폴더 · _qa 에 결과를 쓰지 않는다)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402,F401 — --mode · --snap-in · --snap-out 을 뗀다
import gzip, json, math, os, statistics, sys, tempfile, time, traceback   # noqa: E402
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
TMPD = os.path.join(tempfile.gettempdir(), 'h_ox_search_all')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_ox_search_all_result.txt'))
OL.conf(spd=ARG('--spd', _roots.spd()), tw=ARG('--tw'), shots=ARG('--shots', os.path.join(TMPD, 'shots')))
GATE = QC.GATE   # gate = 바탕을 띄워 헛잣대 · regress · smoke = 새 판만(바탕 풀기 · 띄우기 0 · 「= 바탕」 칸은 기준 스냅샷)
if GATE:
    QC.sub('git:show-app')
SRC = {'NEW': OL.app_src(NEWF)}
if GATE:
    SRC['BASE'] = OL.app_src(BASE)
VERS = tuple(SRC)
OL.ON_LAUNCH = lambda tag: QC.launch('base' if tag == 'BASE' else 'new')
TERM = '대위'
RES = []
STEP = {}
T0 = time.time()


def want(c):
    return (not ONLY or c in ONLY) and (not QC.SMOKE or c == 'S1')   # smoke = S1 PC 한 칸


def _s(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


def R(g, name, new, base=None, d='', yard=True):
    RES.append(dict(g=g, name=name, new=new, base=base, yard=yard, d=d))
    tag = 'INFO' if new is None else ('PASS' if new else 'FAIL')
    yb = '' if base is None else (' · 바탕 ' + (('PASS(바탕도 같음)' if yard else 'PASS') if base else 'FAIL'))
    print('%s | %s · %s%s | %s' % (tag, g, name, yb, _s(d)[:900]), flush=True)


# 쪽 안 기대 수 — 앱 거르기 식과 같은 식(따로 짬)
EXP_Q = r"""(term)=>{const low=term.toLowerCase(),lowNS=low.replace(/\s+/g,'');return quizData.filter(q=>{
  if(!q.pending&&String(q.q).toLowerCase().includes(low))return true;if(!q.pending&&String(q.exp||'').toLowerCase().includes(low))return true;
  if(lowNS&&String(q.id||'').toLowerCase().includes(lowNS))return true;if(lowNS&&String(q.source||'').toLowerCase().replace(/\s+/g,'').includes(lowNS))return true;return false}).map(q=>q.id)}"""
EXP_LW = r"""([owner,term])=>{const low=String(term).trim().toLowerCase();return quizData.filter(q=>{if(String(q.id)===String(owner))return false;
  const no=`${q.displayNo??q.probNum}${q.subNum||''}`;return [q.id,no,q.q,q.source,q.subject,q.subChapter].map(v=>String(v||'').toLowerCase()).some(h=>h.includes(low))}).map(q=>q.id)}"""
EXP_GG = r"""([owner,term])=>{const low=String(term).trim().toLowerCase(),gst=ggStore();return quizData.filter(q=>{if(String(q.id)===String(owner).replace(/^cmp_/,''))return false;
  const L=Array.isArray(gst[q.id])?gst[q.id]:[];const extra=ggTextOfList(L);if(!String(extra).trim())return false;
  const no=`${q.displayNo??q.probNum}${q.subNum||''}`;return [q.id,no,q.q,q.source,q.subject,q.subChapter,extra].map(v=>String(v||'').toLowerCase()).some(h=>h.includes(low))}).map(q=>q.id)}"""


def scroll_all(p, sel, rowsel, want_n, cap=600):
    """그 통을 진짜로 끝까지 굴림 — 줄 수도 굴린 자리도 세 번 그대로면 멈춤(폰 손가락 밀기는 한 번에 몇백 px)"""
    last, same, k = None, 0, 0
    for k in range(cap):
        st = p.ev("([s,r])=>{const b=document.querySelector(s);return [document.querySelectorAll(r).length,b?Math.round(b.scrollTop):-1]}", [sel, rowsel])
        if st[0] >= want_n and not p.ev("(s)=>!!document.querySelector(s+' [data-res-more]')", sel):
            break
        same = same + 1 if st == last else 0
        if same >= 3:
            break
        last = st
        p.scroll_in(sel, 4000)
        p.wait(200)
    return p.ev("(s)=>document.querySelectorAll(s).length", rowsel), k + 1


def ids_of(p, rowsel, attr_js):
    return p.ev("([s,f])=>[...document.querySelectorAll(s)].map(e=>(new Function('e',f))(e))", [rowsel, attr_js])


def s1(br, v, dev):
    p = OL.Live(br, v, SRC[v], dev)
    try:
        exp = p.ev(EXP_Q, TERM)
        p.ev("(t)=>{setSearchMode('q');const i=document.getElementById('search-input');i.value='';runSearch();}", TERM)
        at = p.ev("(()=>__H.hit(document.getElementById('search-input')))()")
        p.press(at['cx'], at['cy'])
        p.wait(200)
        p.pg.keyboard.type(TERM, delay=30)   # 진짜 타자 → oninput runSearch
        p.wait(700)
        first = p.ev("""(()=>({cnt:document.getElementById('search-count').textContent,rows:document.querySelectorAll('#search-results > button').length,
          note:/상위 \\d+건만/.test(document.getElementById('search-results').textContent)}))()""")
        n, rounds = scroll_all(p, '#search-results', '#search-results > button', len(exp))
        got = ids_of(p, '#search-results > button', "const m=/openQPopup\\('([^']+)'/.exec(e.getAttribute('onclick')||'');return m?m[1]:null")
        dup = len(got) - len(set(got))
        last = p.ev("(()=>{const L=document.querySelectorAll('#search-results > button');const e=L[L.length-1];return e?__H.hit(e):null})()")
        opened = None
        if last and last.get('on'):
            p.press(last['cx'], last['cy'])
            p.wait(800)
            opened = p.ev("(id)=>!!document.getElementById('oxwin-q-'+id)", got[-1] if got else '')
        p.shot('s1_%s_%s' % (v, dev['name']))
        d = {'기대': len(exp), '셈': first['cnt'], '처음 줄': first['rows'], '상위 N건만 글': first['note'], '굴린 뒤 줄': n, '굴림': rounds, '겹친 줄': dup,
             '첫 · 끝 = 기대 차례': bool(got) and got[0] == exp[0] and got[-1] == exp[-1] if exp else None, '끝 줄 누름 → 그 문항 팝업': opened, '오류': p.errors()[:3]}
        ok = (first['cnt'] == '%d건' % len(exp) and first['rows'] == min(100, len(exp)) and not first['note'] and n == len(exp) and dup == 0
              and d['첫 · 끝 = 기대 차례'] and opened is True and not d['오류'])
        return ok, d
    finally:
        p.close()


def pick_term(p, js, owner, cands, lo=31, hi=900):
    for t in cands:
        n = len(p.ev(js, [owner, t]))
        if lo <= n <= hi:
            return t, n
    return None, 0


LW_CANDS = ['대리', '취소', '소멸시효', '채권자', '계약', '무효', '등기', '점유']
GG_CANDS = ['취소', '등기', '변제', '보증', '손해', '효력', '무효', '채권자']


def s2(br, v, dev):
    p = OL.Live(br, v, SRC[v], dev)
    try:
        owner = p.ev("quizData[0].id")
        term, nexp = pick_term(p, EXP_LW, owner, LW_CANDS)
        exp = p.ev(EXP_LW, [owner, term])
        p.ev("(o)=>{lwOpen(o)}", owner)
        p.wait(600)
        at = p.ev("(()=>__H.hit(document.querySelector('#oxwin-lk .cfq')))()")
        p.press(at['cx'], at['cy'])
        p.wait(150)
        p.pg.keyboard.type(term, delay=30)
        p.wait(700)
        first = p.ev("(()=>({cnt:(document.querySelector('#oxwin-lk .cfcnt')||{}).textContent||null,rows:document.querySelectorAll('#oxwin-lk .cfrs > .cfr').length}))()")
        n, rounds = scroll_all(p, '#oxwin-lk .cfrs', '#oxwin-lk .cfrs > .cfr', len(exp))
        got = ids_of(p, '#oxwin-lk .cfrs > .cfr', "const x=e.querySelector('.cfid');return x?x.textContent.replace(/^ID /,''):null")
        p.shot('s2_%s_%s' % (v, dev['name']))
        d = {'검색어': term, '기대': len(exp), '셈': first['cnt'], '처음 줄': first['rows'], '굴린 뒤 줄': n, '굴림': rounds, '겹친 줄': len(got) - len(set(got)),
             '차례 = 기대': got == exp, '오류': p.errors()[:3]}
        ok = first['cnt'] == '%d건' % len(exp) and n == len(exp) and got == exp and not d['오류']
        return ok, d
    finally:
        p.close()


def s3(br, v, dev):
    p = OL.Live(br, v, SRC[v], dev)
    try:
        owner = p.ev("(()=>{const g=ggStore();const q=quizData.find(q=>Array.isArray(g[q.id])&&g[q.id].length);return q?q.id:quizData[0].id})()")
        term, nexp = pick_term(p, EXP_GG, owner, GG_CANDS, lo=101, hi=300)   # 100 넘어 이어 붙음까지 · 폰 손가락 밀기로 끝까지 — 300 건 안쪽
        exp = p.ev(EXP_GG, [owner, term])
        p.ev("(o)=>{openQPopup(o)}", owner)
        p.wait(700)
        p.ev("(o)=>{ggSearchToggle(o,'qp-')}", owner)
        p.wait(400)
        sel_in = '#qp-link-search-geunge-' + owner
        at = p.ev("(s)=>__H.hit(document.querySelector(s))", sel_in)
        if at and at.get('on'):
            p.press(at['cx'], at['cy'])
        else:
            p.ev("(s)=>document.querySelector(s).focus()", sel_in)
        p.wait(150)
        p.pg.keyboard.type(term, delay=30)
        p.wait(900)
        box = '#qp-link-results-geunge-' + owner
        first = p.ev("(b)=>({cnt:(document.querySelector(b+' [data-res-cnt]')||{}).textContent||null,rows:document.querySelectorAll(b+' > button').length})", box)
        n, rounds = scroll_all(p, box, box + ' > button', len(exp))
        got = ids_of(p, box + ' > button', "const m=/,'([^']+)'(?:,'qp-')?\\)/.exec(e.getAttribute('onclick')||'');return m?m[1]:null")
        p.shot('s3_%s_%s' % (v, dev['name']))
        # 같은 검색어 다시 그림(칸을 다시 누름 = onfocus linkSearch) — 보던 줄 수 · 굴린 자리 그대로(새 판 resPage key)
        st0 = p.ev("(b)=>Math.round(document.querySelector(b).scrollTop)", box)
        p.ev("(s)=>document.querySelector(s).blur()", sel_in)
        p.wait(150)
        at2 = p.ev("(s)=>__H.at(document.querySelector(s))", sel_in)
        if at2 and at2.get('on'):
            p.press(at2['cx'], at2['cy'])
        else:
            p.ev("(s)=>document.querySelector(s).focus()", sel_in)
        p.wait(500)
        re_ = p.ev("(b)=>({rows:document.querySelectorAll(b+' > button').length,st:Math.round(document.querySelector(b).scrollTop)})", box)
        d = {'검색어': term, '기대': len(exp), '셈': first['cnt'], '처음 줄': first['rows'], '굴린 뒤 줄': n, '굴림': rounds, '차례 = 기대': got == exp,
             '다시 누름(같은 검색어) 줄 · 자리': [re_['rows'], st0, re_['st']], '오류': p.errors()[:3]}
        ok = (first['cnt'] == '%d건' % len(exp) and first['rows'] == min(100, len(exp)) and n == len(exp) and got == exp and not d['오류']
              and re_['rows'] == n and abs(re_['st'] - st0) <= 2)
        return ok, d
    finally:
        p.close()


def omr_expect(q):
    """정리OMR 쪽 글자(words)를 앱 lineIndex 와 같은 줄 묶음 · 같은 찾기(겹침 포함)로 셈"""
    d = os.path.join(OL.CONF['spd'], 'minbeop', 'omr')
    meta = json.load(open(os.path.join(d, 'omr메타.json'), encoding='utf-8'))
    tot = 0
    for n in range(1, int(meta.get('pages') or 0) + 1):
        f = os.path.join(d, 'ox_omr_minbeopOMR_p%d.json.gz' % n)
        if not os.path.isfile(f):
            return None
        words = (json.loads(gzip.open(f).read()).get('pageData') or {}).get('words') or ''
        rows = {}
        for line in words.split('\n'):
            a = line.split('\t')
            if len(a) < 3:
                continue
            x, y = float(a[1]) / 2000, float(a[2]) / 2000
            rows.setdefault(int(math.floor(y * 400 + 0.5)), []).append((a[0], x))
        for k in sorted(rows):
            txt = ''.join(s for s, _ in sorted(rows[k], key=lambda t: t[1]))
            at = txt.find(q)
            while at >= 0:
                tot += 1
                at = txt.find(q, at + 1)
    return tot


OMR_CANDS = ['대리인', '상대방', '소유권', '채권자', '채무자']


def s4(br, v, dev):
    term, nexp = None, 0
    for t in OMR_CANDS:
        c = omr_expect(t)
        if c and 101 <= c <= 300:
            term, nexp = t, c
            break
    if not term:
        return None, {'까닭': '정리OMR 쪽 글자에서 100 넘고 300 안쪽인 검색어를 못 고름', '후보': OMR_CANDS}
    npg = int(json.load(open(os.path.join(OL.CONF['spd'], 'minbeop', 'omr', 'omr메타.json'), encoding='utf-8')).get('pages') or 0)
    p = OL.Live(br, v, SRC[v], dev)
    try:
        qid = p.ev("quizData[0].id")
        p.ev("(q)=>{oxCoord.open(q,'view')}", qid)   # 정리OMR 뷰어(openViewer = window.oxCoord.open)
        p.pg.wait_for_function("()=>!!document.querySelector('#cd-wrap #cd-q')", timeout=120000)
        t_end, got_pg = time.time() + 300, 0   # 쪽 그림(정리OMR 글자)은 뷰어를 열 때만 받는다(mbSyncOmr) — 다 받을 때까지
        while time.time() < t_end:
            got_pg = p.ev("async()=>{try{const a=await dbGet('omrasset:minbeopOMR');return a&&Array.isArray(a.pages)?a.pages.filter(Boolean).length:0}catch(e){return -1}}")
            if got_pg >= npg and not p.ev("typeof mbOmrBusy!=='undefined'&&mbOmrBusy"):
                break
            p.wait(1000)
        p.wait(1500)
        at = p.ev("(()=>__H.hit(document.querySelector('#cd-q')))()")
        p.press(at['cx'], at['cy'])
        p.wait(150)
        p.pg.keyboard.type(term, delay=30)
        p.pg.keyboard.press('Enter')
        p.pg.wait_for_function("()=>/\\d+건/.test((document.querySelector('#cd-wrap')||{}).textContent||'')&&!/찾는 중/.test(document.querySelector('#cd-wrap').textContent)", timeout=180000)
        p.wait(800)
        lst = '[data-cdhits]' if v == 'NEW' else '#cd-wrap div[style*="max-height:46vh"]'
        first = p.ev("""(l)=>{const w=document.querySelector('#cd-wrap');const m=/(\\d+)건/.exec(w.textContent);return {cnt:m?+m[1]:null,rows:document.querySelectorAll(l+' > [data-hit]').length,
          more:!!document.getElementById('cd-more')}}""", lst)
        n, rounds = scroll_all(p, lst, lst + ' > [data-hit]', nexp)
        imgs = p.ev("(l)=>[...document.querySelectorAll(l+' > [data-hit] img')].length", lst)
        p.shot('s4_%s_%s' % (v, dev['name']))
        d = {'검색어': term, '기대': nexp, '받은 쪽': '%d/%d' % (got_pg, npg), '셈': first['cnt'], '처음 줄': first['rows'], '「더 보기」': first['more'], '굴린 뒤 줄': n, '굴림': rounds,
             '그림 채운 줄(보인 것)': imgs, '오류': p.errors()[:3]}
        ok = first['cnt'] == nexp and first['rows'] == min(100, nexp) and n == nexp and not first['more'] and not d['오류']
        return ok, d
    finally:
        p.close()


def s5(br, v, dev):
    p = OL.Live(br, v, SRC[v], dev)
    try:
        p.ev("(t)=>{setSearchMode('q');const i=document.getElementById('search-input');i.value=t;runSearch();}", TERM)
        p.wait(400)
        for _ in range(60):   # 둘째 100 줄이 붙을 때까지 굴림(굴리는 중 · 바탕은 100 에서 멈춤)
            p.scroll_in('#search-results', 3000)
            p.wait(300)
            if p.ev("document.querySelectorAll('#search-results > button').length") > 100:
                break
        mid = p.ev("document.querySelectorAll('#search-results > button').length")
        t2 = '상계'
        exp2 = p.ev(EXP_Q, t2)
        prev = None   # 손가락 밀기 관성(fling)이 멎은 뒤 누름 — 굴러가는 중 톡은 굴림만 멈추고 누름이 안 됨
        for _ in range(30):
            st = p.ev("Math.round(document.getElementById('search-results').scrollTop)")
            if st == prev:
                break
            prev = st
            p.wait(150)
        for _ in range(3):
            at = p.ev("(()=>__H.hit(document.getElementById('search-input')))()")
            p.press(at['cx'], at['cy'])
            p.wait(200)
            if p.ev("document.activeElement===document.getElementById('search-input')"):
                break
        p.pg.keyboard.press('Control+A')
        p.pg.keyboard.type(t2, delay=30)
        p.wait(800)
        st_new = p.ev("Math.round(document.getElementById('search-results').scrollTop)")
        got = ids_of(p, '#search-results > button', "const m=/openQPopup\\('([^']+)'/.exec(e.getAttribute('onclick')||'');return m?m[1]:null")
        old = [x for x in got if x not in set(exp2)]
        n2, _r = scroll_all(p, '#search-results', '#search-results > button', len(exp2))   # 새 결과 끝까지 — 옛 관찰자가 옛 줄을 붙이지 않는가
        got2 = ids_of(p, '#search-results > button', "const m=/openQPopup\\('([^']+)'/.exec(e.getAttribute('onclick')||'');return m?m[1]:null")
        d = {'옛 검색어 굴린 줄': mid, '새 검색어': t2, '새 기대': len(exp2), '새 줄': len(got), '옛 줄 남음': len(old), '첫 100 = 기대 앞 100': got == exp2[:100],
             '새 결과 끝까지 = 기대(옛 줄 0 · 겹침 0)': got2 == exp2, '끝까지 줄': n2, '새 검색어 굴림 자리(맨 위 = 0)': st_new}
        ok = mid > 100 and not old and len(got) == min(100, len(exp2)) and got == exp2[:100] and got2 == exp2 and st_new == 0
        return ok, d
    finally:
        p.close()


def s6(br):
    out = {}
    for v in VERS:
        p = OL.Live(br, v, SRC[v], OL.PC)
        try:
            ts = []
            for _ in range(3):
                ms = p.ev("""(t)=>{setSearchMode('q');const i=document.getElementById('search-input');i.value='';runSearch();void document.body.offsetHeight;
                  const t0=performance.now();i.value=t;i.dispatchEvent(new Event('input',{bubbles:true}));void document.getElementById('search-results').offsetHeight;return performance.now()-t0}""", TERM)   # 입력 → 거르기 · 첫 100 줄 · 배치(layout)까지
                ts.append(round(ms, 1))
                p.wait(300)
            owner = p.ev("quizData[0].id")
            lw = p.ev("""([o,t])=>{const t0=performance.now();const h=lwFind(o,t);return [performance.now()-t0,h.length]}""", [owner, '대리'])
            go = p.ev("(()=>{const g=ggStore();const q=quizData.find(q=>Array.isArray(g[q.id])&&g[q.id].length);return q?q.id:quizData[0].id})()")
            p.ev("(o)=>{openQPopup(o)}", go)
            p.wait(600)
            p.ev("(o)=>{ggSearchToggle(o,'qp-')}", go)
            p.wait(300)
            gs = [p.ev("""([o,t])=>{const i=document.getElementById('qp-link-search-geunge-'+o),b=document.getElementById('qp-link-results-geunge-'+o);i.value='';linkSearch(o,'geunge','qp-');void b.offsetHeight;
              i.value=t;const t0=performance.now();linkSearch(o,'geunge','qp-');void b.offsetHeight;
              const ms=performance.now()-t0;return [ms,b.querySelectorAll(':scope > button').length]}""", [go, '취소']) for _ in range(3)]   # 찾기 + 첫 줄들 배치까지(두 판 같은 잣대)
            out[v] = {'검색 칸(ms)': ts, '가운데': statistics.median(ts), '연결 찾기 「대리」(ms · 건)': [round(lw[0], 1), lw[1]],
                      '근거 찾기 「취소」(linkSearch → 배치 · 세 번 가운데 ms · 그린 줄)': [round(statistics.median([g[0] for g in gs]), 1), gs[-1][1]]}
        finally:
            p.close()
    ok = (out['NEW']['가운데'] <= out['BASE']['가운데'] * 1.2) if 'BASE' in out else None   # regress = 바탕 안 띄움 → 잰 값만(INFO)
    return ok, out


SWEEP = r"""(sel)=>{const out=[];const roots=[...document.querySelectorAll(sel)].filter(__H.vis);if(!roots.length)return ['(뿌리 없음) '+sel];
  const se=document.scrollingElement;if(se.scrollWidth>innerWidth+1)out.push('page-hscroll');
  roots.forEach(r=>[r,...r.querySelectorAll('*')].forEach(e=>{if(!__H.vis(e))return;const cs=getComputedStyle(e);
    if((cs.overflowX==='auto'||cs.overflowX==='scroll')&&e.scrollWidth>e.clientWidth+1&&e.clientWidth>0)out.push('hscroll:'+e.tagName+'.'+String(e.className).slice(0,20));
    const b=e.getBoundingClientRect();if(b.width>0&&(b.right>innerWidth+1||b.left<-1)&&cs.position!=='fixed')out.push('offscreen:'+e.tagName+'.'+String(e.className).slice(0,20))}));
  return [...new Set(out)].slice(0,8)}"""


def s7(br):
    res = {}
    ok = True
    for dev in (OL.PC, OL.PH):
        p = OL.Live(br, 'NEW', SRC['NEW'], dev)
        try:
            p.ev("(t)=>{setSearchMode('q');const i=document.getElementById('search-input');i.value=t;runSearch();}", TERM)
            p.wait(500)
            a = p.ev(SWEEP, '#search-results')
            owner = p.ev("quizData[0].id")
            p.ev("(o)=>{lwOpen(o);const i=document.querySelector('#oxwin-lk .cfq');i.value='대리';i.dispatchEvent(new Event('input',{bubbles:true}))}", owner)
            p.wait(600)
            b = p.ev(SWEEP, '#oxwin-lk')
            res[dev['name']] = {'검색 결과': a, '연결 창': b, '오류': p.errors()[:3]}
            ok = ok and not a and not b and not res[dev['name']]['오류']
            p.shot('s7_%s' % dev['name'])
        finally:
            p.close()
    return ok, res


def main():
    os.makedirs(TMPD, exist_ok=True)
    R('S0', '판 · 자리', None, None, {'NEW': NEWF, 'md5(LF)': {k: OL.md5lf(v) for k, v in SRC.items()}, 'BASE': BASE, 'SPD': OL.CONF['spd'], 'tw': OL.CONF['tw']})
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        plan = [('S1', '검색 칸 「%s」 — 셈 = 기대 · 처음 100 줄 · 「상위 N건만」 0 · 끝까지 굴려 다 · 겹침 0 · 차례 · 끝 줄 누름 = 그 문항' % TERM, s1, True),
                ('S2', '연결 창 찾기 — 30 넘는 검색어 · 셈 보임 · 끝까지 굴려 다 붙음 · 차례', s2, True),
                ('S3', '근거 창 찾기(문항 팝업 근거 🔍) — 30 넘는 검색어 · 셈 보임 · 끝까지 굴려 다 붙음 · 차례', s3, True),
                ('S4', '정리OMR 찾기 — 60 넘는 검색어 · 셈 = 기대 · 끝까지 굴려 다 붙음(「더 보기」 없음)', s4, True)]
        for cid, name, fn, by_dev in plan:
            if not want(cid):
                continue
            t1 = time.time()
            for dev in ((OL.PC,) if QC.SMOKE else (OL.PC, OL.PH)):
                res = {}
                for v in VERS:
                    try:
                        res[v] = fn(br, v, dev)
                    except Exception as e:
                        res[v] = (False, {'하네스 오류': str(e)[:300], 'tb': traceback.format_exc()[-400:]})
                R(cid, '%s %s' % (dev['name'], name), res['NEW'][0], res['BASE'][0] if 'BASE' in res else None, {k: x[1] for k, x in res.items()})
            STEP[cid] = round((time.time() - t1) / 60, 1)
        if want('S5'):
            t1 = time.time()
            for dev in (OL.PC, OL.PH):
                res = {}
                for v in VERS:
                    try:
                        res[v] = s5(br, v, dev)
                    except Exception as e:
                        res[v] = (False, {'하네스 오류': str(e)[:300]})
                R('S5', '%s 검색어 바꾸기(「%s」 굴리는 중 → 「상계」) — 옛 줄 0 · 새 결과 첫 100 줄 · 맨 위 · 끝까지 = 기대' % (dev['name'], TERM), res['NEW'][0], res['BASE'][0] if 'BASE' in res else None, {k: x[1] for k, x in res.items()})
            STEP['S5'] = round((time.time() - t1) / 60, 1)
        if want('S6'):
            t1 = time.time()
            try:
                ok, d = s6(br)
            except Exception as e:
                ok, d = False, {'하네스 오류': str(e)[:300]}
            R('S6', '첫 그림 빠르기 — 검색 칸 입력 → 첫 100 줄 배치까지(세 번 가운데) 새 판 ≤ 바탕 × 1.2 · 연결 찾기(끝까지) 시간 INFO', ok, None, d, yard=False)
            STEP['S6'] = round((time.time() - t1) / 60, 1)
        if want('S7'):
            t1 = time.time()
            try:
                ok, d = s7(br)
            except Exception as e:
                ok, d = False, {'하네스 오류': str(e)[:300]}
            R('S7', '화면 훑기 — 검색 결과 · 연결 창(PC · 폰) 넘침 · 잘림 · 화면 밖 0 · 페이지 오류 0', ok, None, d, yard=False)
            STEP['S7'] = round((time.time() - t1) / 60, 1)
        br.close()
    nf = [r for r in RES if r['new'] is False]
    yard = [r for r in RES if r['yard'] and r['base'] is not None and r['new'] is not None]
    R('합계', '합계', None, None, {'PASS': sum(1 for r in RES if r['new'] is True), 'FAIL': len(nf), 'FAIL 칸': [r['g'] + ' ' + r['name'][:20] for r in nf],
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
