# -*- coding: utf-8 -*-
r"""_task_jagwa_gg3 §B 관문 [클라우드] — 자과 물리 「근거 세 칸」(시안 v57 패치 42 + §A-2 cqx 칸 동기화) · 세 과목 공통(창 크기 · 정답 표시 · 서랍 밀기 · 첫 화면 카드)

  python _harness_jagwa_gg3.py [--new <앱>] [--base <판 = cab7b5a>] [--only G1,G1R,G2,G3,G5,G6,G7] [--yard 1|0]
                               [--spd <studyplandata>] [--notes <notes>] [--vendor <cdnjs 사본>] [--res <결과>] [--shots <그림>]

  NEW  = genie 작업트리 jagwa/index.html · BASE = 바탕 cab7b5a(헛잣대 — 패치 없음 · 바뀐 칸은 바탕에서 FAIL 이어야 · PASS 면 「바탕도 같음」)
  만든 헛잣대(하네스 서버만 내줌 · 앱 파일 무접촉):
    SIAN     = 바탕 + 패치 42(시안 꼴 cqx {hide,cs} = 기기 하나 값 · 동기화 밖)
    SIANSYNC = SIAN + cqx 를 시안 꼴 그대로 SYNC_KEYS · SYNC_REF 에(칸 둘 hide · cs · 늦은 통 가드 없음) — 「시안 꼴이면 한쪽이 짐」 · 「빈 값으로 덮음」 을 보이는 판
    OLDTAP   = NEW 에서 패치 #37 · #38(터치 대체 누르기 겹누름 막이)만 되돌림 — R52 헛잣대(바탕엔 ▾ 단추가 없어 잣대가 못 가름)
  엔진 = Chromium · PC 1100×800(마우스) · 폰 384×740(hasTouch · 모바일 · DPR 2 · 터치 = CDP Input.dispatchTouchEvent) · 아이패드 820×1180(G7) · WebKit 칸(관문 4)은 [로컬]
  데이터 = studyplandata 현행(--spd · 가짜 GitHub = JG.route_handler · PUT 은 메모리 · 밖으로 안 나감) · notes(--notes) · cdnjs = --vendor 사본(클라우드는 cdn 막힘)
  관문:
    G1  시안 시험 109(tests_gg3.json) — 화면 넷(p1 · p2 = PC · m1 · m2 = 폰)마다 새 기기 · setup 그대로(바탕이 G3 없음으로 멈추지 않게 G3 · g3Sel · g3PopToggle 은 있으면 부름)
        · pre 9 초 · click / type = 진짜 누름(PC mouse.click · 폰 CDP 톡) · Enter = 진짜 키 · wait · expect 식 그대로(바탕도 같은 식) · same = 그 요소 보임(INFO)
        · #44 는 §A-2 로 cqx 꼴이 바뀌어 옛 식(X.cs · X.hide)이 깨짐(뜻한 차) → 같은 뜻 새 꼴 식 44n 을 따로 잼
    G1R 시안이 엔진 dispatch 로 잰 칸을 진짜 입력으로 — R48 지금 문항 줄 제목 톡(폰) · R52 터치 겹누름(무거운 click · CDP 톡 150ms · PC 크기 터치) ·
        R56 서랍 손가락 밀기 열기 · 닫기 · 접힌 손잡이 6px 흔들림 톡(폰) · R57 개념 창 덮개 밀기 · 본문 밀기 = 목차 덮개 · 서랍 그대로(폰)
    G2  떠 있는 창 누름 차례 — 쓰인 문항 창 · 개념 창 · 비교 창 · 작은 창이 본창을 덮은 채 본창 보이는 자리 진짜 누름 → 본창 맨 위 · 그 창 → 그 창 맨 위 · 폰 서랍 누름 → 서랍 위
    G3  1/3 — 이 판 창 처음 높이 ≤ innerHeight/3(본창 ≤ 1/2) · 손으로 키운 크기(twgrip 진짜 끌기) 기억 → 다시 불러 다시 열면 그 크기
    G5  지학 · 생물 표본(PC · 폰) — 본창 첫 높이 ≤ 1/2 · 팝업 ≤ 1/3 · 첫 화면 카드 = 제목만 엶 · 서랍 손가락 밀기(폰) · 근거 줄 누름 대상 전수 = 바탕(g3 안 돎) ·
        카드 층 필기 도구 · 정리OMR 무변 · 정답 창 · 초록 테두리 · OMR 길게 누름 = 카드 층에 OMR 단추가 없어(바탕부터 #omrPad display:none) 「해당 없음」 — 잰 값을 적음
    G6  cqx 동기화 — 기기 둘(문맥 둘 · 같은 가짜 원격) 다른 문항에서 빼기 · 댓글(진짜 누름) → 맞춘 뒤 둘 다 남음(헛잣대 SIAN · SIANSYNC) ·
        cqx 읽기 전 동기화(IndexedDB get('cqx') 늦춤) → 원격 cqx 그대로(헛잣대 SIANSYNC = 빈 값으로 덮음) · 받은 cqx = 열린 근거 줄에 바로 ·
        시안 꼴 들이기 → 새 꼴로 옮겨짐(옛 열쇠 hide · cs 그대로) · 필기 동기화(_harness_jagwa_ink_sync.py)는 따로 돌려 대조(이 하네스 밖)
    G7  화면 훑기(규칙 60) — PC · 폰 · 아이패드 × 이 판 창 열일곱 · 오류 0 · 화면 밖 0 · 오른쪽 넘침 · 잘림 0(KaTeX 숨은 MathML 뺌) · 가려진 누름 0 ·
        날 $…$ · <span · ^id 글자 0 · 겹침 · 작은 누름 = INFO · 그림 = --shots(_qa 밖)
  결과 = 화면 PASS/FAIL/INFO 줄 · --res(기본 = 임시 폴더 · _qa 에 결과를 쓰지 않는다)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402,F401 — _task_qa_slim2 A-1(10/8) · --mode · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음
import _qa_jagwa_common as JG   # noqa: E402
import hashlib, json, os, re, sys, tempfile, time, traceback   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEWF = ARG('--new', _roots.genie('jagwa', 'index.html'))
BASE = ARG('--base', 'cab7b5a')   # genie main 81ee89c 의 jagwa/index.html = cab7b5a 판 그대로(LF md5 48330c0f)
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
YARD_ON = (ARG('--yard', '1') or '1') != '0'
TMPD = os.path.join(tempfile.gettempdir(), 'h_jagwa_gg3')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_jagwa_gg3_result.txt'))
SHOTS = ARG('--shots', os.path.join(TMPD, 'shots'))
SPD = ARG('--spd', _roots.spd())
NOTES = ARG('--notes', os.path.join(os.path.dirname(_roots.spd()), 'notes'))
VENDOR = ARG('--vendor', os.path.join(TMPD, 'vendor'))
JG.conf(VENDOR_PP=VENDOR, SPD_PP=SPD, NOTES=NOTES, SHOTS=SHOTS)
GG3 = _roots.genie('_qa', 'jagwa', 'gg3')
TESTS = json.load(open(os.path.join(GG3, 'tests_gg3.json'), encoding='utf-8'))
PATCHES = json.load(open(os.path.join(GG3, 'patches_gg3.json'), encoding='utf-8'))['patches']
SCR = {s['id']: s for r in TESTS['rows'] for s in r['screens']}
VIEWS = {v['key']: v for v in TESTS['views']}
PRE = int(TESTS.get('pre_test_ms', 9000))
PC, PH, PAD = (1100, 800), (384, 740), (820, 1180)
DEVS = {'PC': (PC, False), '폰': (PH, True), '아이패드': (PAD, True)}

RES = []    # dict(g, id, name, new(True/False/None=INFO), base(True/False/None), yard(헛잣대 칸), d)
STEP = {}
T0 = time.time()


def want(g):
    return not ONLY or g.upper() in ONLY


def _s(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


def R(g, cid, name, new, base=None, d='', yard=True):
    """한 칸 — new = 새 판 판정 · base = 같은 잣대 바탕(헛잣대) 판정(None = 안 잼) · yard = 바탕이 FAIL 이어야 하는 칸"""
    RES.append(dict(g=g, id=cid, name=name, new=new, base=base, yard=yard, d=d))
    tag = 'INFO' if new is None else ('PASS' if new else 'FAIL')
    yb = '' if base is None else (' · 바탕 ' + ('PASS' + ('(바탕도 같음)' if yard else '') if base else 'FAIL'))
    print('%s | %s · %s · %s%s | %s' % (tag, g, cid, name, yb, _s(d)[:700]), flush=True)


def md5lf(s):
    return hashlib.md5(s.replace('\r\n', '\n').encode('utf-8')).hexdigest()


# ── 판 — NEW · BASE · 만든 헛잣대 셋 ──
SRC = {'NEW': JG.app_src(NEWF), 'BASE': JG.app_src(BASE)}


def _patched(src, pats, why):
    for i, (o, n) in enumerate(pats):
        c = src.count(o)
        if c != 1:
            raise SystemExit('%s: 패치 #%d 옛 글 %d 회(1 회여야)' % (why, i, c))
        src = src.replace(o, n, 1)
    return src


SRC['SIAN'] = _patched(SRC['BASE'], PATCHES, 'SIAN')
SRC['SIANSYNC'] = _patched(SRC['SIAN'], [
    ("SYNC_KEYS:['status','note','qtype','conc','gpt','twin','ansfix','frm','maskpos','omrpos','mcard','link'],",
     "SYNC_KEYS:['status','note','qtype','conc','gpt','twin','ansfix','frm','maskpos','omrpos','mcard','link','cqx'],"),
    ("  bref   :{g:()=>BREF, s:v=>{BREF=v}}\n};",
     "  bref   :{g:()=>BREF, s:v=>{BREF=v}},\n  cqx:{g:()=>window.g3CqxGet?g3CqxGet():null,s:v=>{}}\n};")], 'SIANSYNC')
SRC['OLDTAP'] = _patched(SRC['NEW'], [(PATCHES[37][1], PATCHES[37][0]), (PATCHES[38][1], PATCHES[38][0])], 'OLDTAP')
MD5 = {k: md5lf(v) for k, v in SRC.items()}


# ── 기기 ──
def dev(br, ver, size, touch, subj='phys', who='하네스', remote=None, init=''):
    """기기 하나 = 문맥 하나(IndexedDB · localStorage 따로) · init = INIT 뒤에 붙일 글(JG.INIT_PP 를 잠깐 바꿨다 되돌림 — JG 머리글 안내 꼴)"""
    old = JG.INIT_PP
    if init:
        JG.INIT_PP = old + init
    try:
        p = JG.Pg_PP(br, 'chromium', 'gg3-' + ver, SRC[ver], subj, size, touch=touch, who=who, remote=remote or JG.Remote())
    finally:
        JG.INIT_PP = old
    p.ver = ver
    return p


def tools(p):
    if not p.ev("typeof __H!=='undefined'"):
        p.ev(JG.TOOLS)


def errs(p):
    try:
        return (p.errs or []) + (p.ev('window.__err||[]') or [])
    except Exception as e:
        return p.errs + ['ev: ' + str(e)[:120]]


def press(p, x, y, touch, hold=80):
    """진짜 누름 — PC = mouse.click · 터치 기기 = CDP touchStart → hold → touchEnd"""
    if touch:
        p.tap(x, y, wait=0, hold=hold)
    else:
        p.click(x, y, wait=0)


def swipe(p, x0, y0, x1, y1, steps=8, dur=180):
    """진짜 손가락 밀기 — CDP Input.dispatchTouchEvent(touchStart · touchMove×steps · touchEnd)"""
    c = p._cdp()
    pt = lambda x, y: [{'x': x, 'y': y, 'id': 1, 'radiusX': 6, 'radiusY': 6}]
    c.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': pt(x0, y0)})
    for k in range(1, steps + 1):
        p.pg.wait_for_timeout(dur / steps)
        c.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': pt(x0 + (x1 - x0) * k / steps, y0 + (y1 - y0) * k / steps)})
    c.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})


def drag_mouse(p, x0, y0, x1, y1, steps=10):
    p.pg.mouse.move(x0, y0)
    p.pg.mouse.down()
    for k in range(1, steps + 1):
        p.pg.mouse.move(x0 + (x1 - x0) * k / steps, y0 + (y1 - y0) * k / steps)
        p.pg.wait_for_timeout(16)
    p.pg.mouse.up()


def tolerant(js):
    """바탕(cab7b5a)에는 G3 · g3Sel · g3PopToggle 이 없다 — setup 이 거기서 멈추면 openView 도 못 가 시험마다 같은 까닭으로 진다 → 있으면 부름(새 판에서는 같은 글)"""
    return (js.replace("G3.blocks()", "(window.G3?G3.blocks():[])")
              .replace("g3Sel(", "(window.g3Sel||function(){})(")
              .replace("g3PopToggle(", "(window.g3PopToggle||function(){})("))


def expwrap(expr):
    return ("(()=>{try{const __v=(" + expr + ");return {v:(__v===null||__v===undefined)?null:"
            "((typeof __v==='object'||typeof __v==='function')?!!__v:__v)}}catch(__e){return {e:String(__e&&__e.message||__e).slice(0,240)}}})()")


def truthy(r):
    if not isinstance(r, dict) or 'e' in r:
        return False
    v = r.get('v')
    if v is True:
        return True
    if v in (None, False, 0, '', 'skip'):
        return False
    return bool(v)


LOC = r"""([sel,nth])=>{if(typeof __H==='undefined')return {notools:1};const L=document.querySelectorAll(sel),e=L[nth||0];if(!e)return {miss:1,n:L.length};
  if(!__H.vis(e))return {hidden:1};let a=__H.at(e);
  if(!a.on){try{e.scrollIntoView({block:'center',inline:'nearest'})}catch(_){}a=__H.at(e)}   /* 손이 하듯 보이는 가운데로 굴려서(가장자리면 서랍 절 머리 .ndsec 가 덮는다) */
  return a}"""
CARET = r"""([sel,nth])=>{const e=document.querySelectorAll(sel)[nth||0];if(!e)return null;if(document.activeElement!==e)e.focus();
  try{const n=(e.value||'').length;e.setSelectionRange(n,n)}catch(_){}return {act:document.activeElement===e,val:String(e.value||'').slice(0,40)}}"""
SAME_JS = r"""(s)=>{const e=document.querySelector(s);return !!e&&typeof __H!=='undefined'&&__H.vis(e)}"""


def act(p, t, touch):
    """시험 한 줄의 누름 — click(+nth) = 그 요소 가운데를 진짜로 · type = 진짜 누름으로 칸 고르고(끝으로 커서) 진짜 키 · enter = 진짜 Enter"""
    note = []
    tools(p)
    W, H = p.dev
    if t.get('type'):
        sel, nth = t['type'], t.get('nth', 0) or 0
        a = p.ev(LOC, [sel, nth])
        if a and a.get('on'):
            press(p, a['cx'], a['cy'], touch)
            p.wait(150)
        else:
            note.append('글칸 누름 못 함:' + _s(a)[:60])
        c = p.ev(CARET, [sel, nth])
        if not c:
            note.append('글칸 없음')
        else:
            p.pg.keyboard.type(t.get('text', ''), delay=15)
            if t.get('enter'):
                p.pg.keyboard.press('Enter')
    elif t.get('click'):
        sel, nth = t['click'], t.get('nth', 0) or 0
        a = p.ev(LOC, [sel, nth])
        if not a or a.get('miss') or a.get('hidden') or a.get('notools'):
            note.append('누를 것 ' + ('없음' if (a or {}).get('miss') else '숨음' if (a or {}).get('hidden') else '?'))
        elif 0 < a['cx'] < W and 0 < a['cy'] < H:
            if not a.get('on'):
                note.append('가려짐→' + str(a.get('top')))
            press(p, a['cx'], a['cy'], touch)
        else:
            note.append('화면 밖')
    p.wait(int(t.get('wait', 800)))
    return note


# §A-2 로 깨지는 시안 식 #44 의 같은 뜻 새 꼴 식(빼기 · 댓글을 g3CqxGet() 칸 꼴로 · 되돌림)
T44N = r"""(()=>{const u='P066';const c=g3Cq(u)[0];if(!c)return false;const box=document.createElement('div');box.innerHTML=g3LineHTML(u,'qp-');const row=box.querySelector('.g3cq');
const ok1=!!row&&!!row.querySelector('[data-g3cqcm]')&&row.querySelector('[data-g3cqcm]').textContent==='댓'&&!!row.querySelector('[data-g3cqdel]');
const X=g3CqxGet();if(!X||X.cs||X.hide)return false;const q=String(qk(66));const had=Object.prototype.hasOwnProperty.call(X,q);const cell=X[q]||(X[q]={h:[],c:{}});
(cell.c[c.k]=cell.c[c.k]||[]).push({k:'c_t',t:'개념 댓글',ts:Date.now()});const box2=document.createElement('div');box2.innerHTML=g3LineHTML(u,'qp-');
const ok2=box2.querySelector('.g3cq [data-g3cqcm]').classList.contains('has');cell.h.push(c.k);const ok3=!g3Cq(u).some(x=>x.k===c.k);
cell.h=cell.h.filter(k=>k!==c.k);cell.c[c.k]=cell.c[c.k].filter(x=>x.k!=='c_t');if(!cell.c[c.k].length)delete cell.c[c.k];if(!had)delete X[q];
return ok1&&ok2&&ok3&&g3Cq(u).some(x=>x.k===c.k)})()"""


def g1(br):
    vers = ['NEW'] + (['BASE'] if YARD_ON else [])
    out = {v: {} for v in vers}
    for v in vers:
        for sid in ('p2', 'p1', 'm1', 'm2'):
            sc = SCR[sid]
            vw = VIEWS[sc['view']]
            touch = bool(vw.get('touch'))
            t1 = time.time()
            p = dev(br, v, (vw['W'], vw['H']), touch)
            try:
                p.ev(tolerant(sc['setup']))
            except Exception as e:
                print('  setup 오류', v, sid, str(e)[:200])
            p.wait(PRE)
            for i, t in enumerate(TESTS['tests']):
                if t['screen'] != sid:
                    continue
                try:
                    note = act(p, t, touch)
                    r = p.ev(expwrap(t['expect']))
                    if i == 44:
                        out[v]['44n'] = dict(ok=truthy(p.ev(expwrap(T44N))), note=[], r=None)
                except Exception as e:
                    note, r = ['하네스: ' + str(e)[:160]], {'e': 'harness'}
                same = None
                if t.get('same'):
                    try:
                        same = p.ev(SAME_JS, t['same'])
                    except Exception:
                        same = False
                out[v][i] = dict(ok=truthy(r), r=r, note=note, same=same)
            out[v]['err_' + sid] = errs(p)
            if v == 'NEW':
                p.shot('g1_%s_%s' % (v, sid))
            p.close()
            print('  G1 %s %s %.0fs' % (v, sid, time.time() - t1), flush=True)
    for i, t in enumerate(TESTS['tests']):
        n = out['NEW'].get(i)
        b = out.get('BASE', {}).get(i)
        d = {'새': n['r'], '누름': n['note']}
        if t.get('same'):
            d['same 보임'] = n['same']
        if b is not None:
            d['바탕'] = b['r']
        nm = '[%s] %s' % (t['screen'], t['name'])
        if i == 44:
            nm += ' — 옛 식(시안 꼴 X.cs · X.hide) · §A-2 꼴 바뀜으로 깨짐 = 뜻한 차 · 같은 뜻 새 꼴 = 44n'
            R('G1', '#44', nm, None, b and b['ok'], d)
            continue
        if (n['r'] or {}).get('v') == 'skip':   # 시안 식이 제 조건이 안 맞아 'skip'(시안 거울은 참으로 셈) — 그 칸은 G1R 진짜 입력이 잼
            nm += ' — 시안 식 skip(제 조건 안 맞음 · 시안 거울은 참으로 셈) → G1R R56 이 진짜 손가락으로 잼'
            R('G1', '#%d' % i, nm, None, None if b is None else b['ok'], d)
            continue
        R('G1', '#%d' % i, nm, n['ok'], None if b is None else b['ok'], d)
    n44 = out['NEW'].get('44n')
    R('G1', '#44n', '[p2] 이은 개념 줄 댓 · ✕ · 댓글 · 빼기(66) — #44 를 §A-2 새 꼴(g3CqxGet()[qk] = {h,c})로', n44 and n44['ok'],
      out.get('BASE', {}).get('44n', {}).get('ok') if YARD_ON else None)
    for v in vers:
        e = {sid: out[v].get('err_' + sid) for sid in ('p2', 'p1', 'm1', 'm2')}
        tot = sum(len(x or []) for x in e.values())
        if v == 'NEW':
            R('G1', '오류', '새 판 화면 넷 페이지 오류 0(pageerror · window error · unhandledrejection)', tot == 0, None, e, yard=False)
        else:
            R('G1', '오류(바탕)', '바탕 화면 넷 페이지 오류 수(INFO — 바탕엔 G3 없음 오류가 난다)', None, None, {k: (v2 or [])[:3] for k, v2 in e.items()})


# ═══ G1R — 시안이 엔진 dispatch 로 잰 칸을 진짜 입력으로 ═══
def r48(br, v):
    p = dev(br, v, PH, True)
    try:
        p.ev(tolerant(SCR['m1']['setup']))
        p.wait(PRE)
        tools(p)
        ok0 = p.ev(r"""(()=>{if(typeof g3UseWinQ!=='function')return 'g3UseWinQ 없음';const r=rec(71);g3UseWinQ(GGU(r),conceptsOf(r)[0].k);const s=document.getElementById('gguw');
          if(!s||!s.__g3cwOpen)return 'gguw 덮개 없음';s.__g3cwOpen('R');return document.getElementById('view').classList.contains('hide')})()""")
        p.wait(900)
        at = p.ev("(()=>{const t=document.querySelector('#gguw .g3cwR .gguR.me .g3ttl');return t?__H.at(t):null})()")
        if ok0 is not True or not at or not at.get('on'):
            return False, {'준비': ok0, '제목': at}
        press(p, at['cx'], at['cy'], True, hold=150)
        p.wait(3000)
        r1 = p.ev("({vis:!document.getElementById('view').classList.contains('hide'),no:VNO,s:VSEEN,cmp:window.G3CMP})")
        at2 = p.ev("(()=>{const t=document.querySelector('#gguw .g3cwR .gguR.me .g3ttl');return t?__H.at(t):null})()")
        front = None
        if at2 and not at2.get('on'):   # 본창이 덮었으면 쓰인 문항 창 머리를 진짜로 눌러 앞으로(누른 창 맨 위) 뒤 제목
            h = p.ev("(()=>{const h=document.querySelector('#gguw .gguh');return h?__H.at(h):null})()")
            if h and h.get('on'):
                press(p, h['cx'], h['cy'], True, hold=150)
                p.wait(700)
                front = h.get('top')
            at2 = p.ev("(()=>{const t=document.querySelector('#gguw .g3cwR .gguR.me .g3ttl');return t?__H.at(t):null})()")
        if not at2 or not at2.get('on'):
            return False, {'준비': ok0, '첫 톡 뒤': r1, '둘째 제목': at2}
        press(p, at2['cx'], at2['cy'], True, hold=150)
        p.wait(2500)
        r2 = p.ev("(()=>{const v=document.getElementById('view'),w=document.getElementById('gguw'),z=x=>x?(+getComputedStyle(x).zIndex||0):-1;return {vis:!v.classList.contains('hide'),no:VNO,s:VSEEN,vz:z(v),wz:z(w)}})()")
        ok = bool(r1['vis'] and r1['no'] == 71 and r2['vis'] and r2['no'] == 71 and r2['s'] == r1['s'] and r2['vz'] >= r2['wz'])
        return ok, {'첫 톡': r1, '둘째 톡': r2, '앞으로': front, '오류': errs(p)[:3]}
    finally:
        p.close()


def r52(br, v):
    p = dev(br, v, PC, True)   # PC 크기 · 터치 화면(시안 v52 = PC 화면 터치 톡)
    try:
        p.ev(tolerant(SCR['p2']['setup']))
        p.wait(PRE)
        tools(p)
        pre = p.ev(r"""(()=>{const b=document.getElementById('g3Fold');if(!b)return null;window.__fc=0;b.addEventListener('click',()=>{window.__fc++});
          window.__heavy=1;b.addEventListener('click',()=>{if(window.__heavy){window.__heavy=0;const t0=Date.now();while(Date.now()-t0<500){}}});   /* 무거운 누름 = 단추 click 뒤(▾ onclick 이 stopPropagation 해 문서 손에는 안 옴 — 단추에 직접) */
          return {off:document.getElementById('view').classList.contains('g3off'),at:__H.hit(b)}})()""")
        if not pre or not pre['at'].get('on'):
            return False, {'준비': pre}
        press(p, pre['at']['cx'], pre['at']['cy'], True, hold=150)
        p.wait(1500)
        post = p.ev("({off:document.getElementById('view').classList.contains('g3off'),fc:window.__fc})")
        return bool(post['off'] != pre['off'] and post['fc'] == 1), {'앞': pre['off'], '뒤': post, '오류': errs(p)[:3]}
    finally:
        p.close()


R56_PREP = r"""(()=>{if(document.getElementById('g3Pop')&&window.g3PopToggle){g3PopToggle(65,document.querySelector('#ndList .ndrow[data-no="65"] .ndox'))}
  const lp=document.getElementById('ndLvPop');if(lp)lp.remove();ndResFold(true);return document.getElementById('navdr').classList.contains('fold')})()"""
R56_START = r"""(()=>{const bad='#view,.sheet,.thcSide,.thcScrim,#pwl,.vpin,#g3Pop,#tyPop,#g3Af,input,textarea,select,canvas,#qink,#inkc,#ndGrip,.stage,#navdr';
  for(const y of [520,480,560,440,600,400,640,360]){for(const x of [60,40,80]){const e=document.elementFromPoint(x,y);if(e&&!e.closest(bad))return {x,y,t:e.tagName+'.'+String(e.className).slice(0,24)}}}return null})()"""


def r56(br, v):
    p = dev(br, v, PH, True)
    try:
        p.ev(tolerant(SCR['m1']['setup']))
        p.wait(PRE)
        tools(p)
        f0 = p.ev(R56_PREP)
        p.wait(900)
        st = p.ev(R56_START)
        if not f0 or not st:
            return False, {'접힘': f0, '밀 자리': st}
        swipe(p, st['x'], st['y'], st['x'] + 130, st['y'] + 10)
        p.wait(900)
        a = p.ev("!document.getElementById('navdr').classList.contains('fold')")
        row = p.ev(r"""(()=>{const d=document.getElementById('navdr').getBoundingClientRect();const L=[...document.querySelectorAll('#ndList .ndrow')].map(r=>r.getBoundingClientRect()).filter(r=>r.top>d.top+80&&r.bottom<innerHeight-40);
          const r=L[Math.floor(L.length/2)];return r?{x:Math.min(d.right-24,r.left+r.width*0.7),y:r.top+r.height/2,dr:d.right}:null})()""")
        b = None
        if a and row:
            swipe(p, row['x'], row['y'], row['x'] - 120, row['y'] + 5)
            p.wait(900)
            b = p.ev("document.getElementById('navdr').classList.contains('fold')")
        p.ev('ndResFold(true)')
        p.wait(900)
        g = p.ev(r"""(()=>{const g=document.getElementById('ndGrip');if(!g)return null;const r=g.getBoundingClientRect();return {x:r.left+r.width/2,y:Math.max(r.top+10,Math.min(r.bottom-10,r.top+300)),w:r.width,top:(document.elementFromPoint(r.left+r.width/2,Math.max(r.top+10,Math.min(r.bottom-10,r.top+300)))||{}).id}})()""")
        c = None
        if g:
            cdp = p._cdp()
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': g['x'], 'y': g['y'], 'id': 1, 'radiusX': 6, 'radiusY': 6}]})
            p.wait(40)
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': g['x'] + 3, 'y': g['y'], 'id': 1, 'radiusX': 6, 'radiusY': 6}]})
            p.wait(40)
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': g['x'] + 6, 'y': g['y'], 'id': 1, 'radiusX': 6, 'radiusY': 6}]})
            p.wait(70)
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
            p.wait(900)
            c = p.ev("!document.getElementById('navdr').classList.contains('fold')")
        return bool(a and b and c), {'밀어 펴짐': a, '밀어 접힘': b, '손잡이 6px 흔들림 톡 = 펴짐': c, '밀 자리': st, '줄': row, '손잡이': g, '오류': errs(p)[:3]}
    finally:
        p.close()


def r57(br, v):
    p = dev(br, v, PH, True)
    try:
        p.ev(tolerant(SCR['m1']['setup']))
        p.wait(PRE)
        tools(p)
        p.ev(R56_PREP)
        p.wait(900)
        ok0 = p.ev(r"""(()=>{const r=rec(71);conceptSheet(conceptsOf(r)[0].k,r);const s=document.getElementById('sh-concept');if(!s)return '개념 창 없음';
          if(!s.__g3cwOpen)return '덮개 없음';s.__g3cwOpen('R');return true})()""")
        p.wait(900)
        if ok0 is not True:
            return False, {'준비': ok0}
        at = p.ev(r"""(()=>{const R=document.querySelector('#sh-concept .thcR');if(!R)return null;const rr=R.getBoundingClientRect();const x=rr.left+10,y=rr.top+rr.height/2;const t=document.elementFromPoint(x,y);
          return {x,y,on:!!t&&R.contains(t),onR:document.getElementById('sh-concept').classList.contains('thcOnR')}})()""")
        if not at or not at['on']:
            return False, {'준비': ok0, '덮개 자리': at}
        swipe(p, at['x'], at['y'], at['x'] + 120, at['y'] + 4)
        p.wait(900)
        a = p.ev("(()=>{const s=document.getElementById('sh-concept');return {closed:!!s&&!s.classList.contains('thcOnR')&&!s.classList.contains('thcOnL'),fold:document.getElementById('navdr').classList.contains('fold')}})()")
        bd = p.ev(r"""(()=>{const s=document.getElementById('sh-concept');const P=s&&s.querySelector('.panel');if(!P)return null;const r=P.getBoundingClientRect();
          for(const fy of [0.55,0.45,0.65,0.35]){const x=r.left+r.width*0.3,y=r.top+r.height*fy,t=document.elementFromPoint(x,y);if(t&&P.contains(t)&&!t.closest('button,a,.thcQ,.thcObs,img'))return {x,y}}return {x:r.left+r.width*0.3,y:r.top+r.height*0.55}})()""")
        b = None
        if bd:
            swipe(p, bd['x'], bd['y'], bd['x'] + 120, bd['y'] + 4)
            p.wait(900)
            b = p.ev("(()=>{const s=document.getElementById('sh-concept');return {toc:!!s&&s.classList.contains('thcOnL'),fold:document.getElementById('navdr').classList.contains('fold')}})()")
        ok = bool(a['closed'] and a['fold'] and b and b['toc'] and b['fold'])
        return ok, {'덮개 오른쪽 밀기': a, '본문 오른쪽 밀기': b, '오류': errs(p)[:3]}
    finally:
        p.close()


def g1r(br):
    plan = [('R48', '폰 v48 지금 문항(71) 줄 제목 진짜 톡 → 열림 · 다시 톡 = 새 열람 안 만듦 · 본창이 쓰인 문항 창 위', r48, ['NEW', 'BASE']),
            ('R52', 'PC 터치 v52 ▾ 진짜 톡(150ms) · 누른 일 무거움(click 뒤 0.5 초) → 한 번만 바뀜 · click 1 번', r52, ['NEW', 'OLDTAP', 'BASE']),
            ('R56', '폰 v56 접힌 서랍 손가락 밀기(오른쪽) = 펴짐 · 펴진 서랍 왼쪽 밀기 = 접힘 · 접힌 손잡이 6px 흔들림 톡 = 펴짐', r56, ['NEW', 'BASE']),
            ('R57', '폰 v57 개념 창 덮개 오른쪽 밀기 = 덮개만 닫힘 · 본문 오른쪽 밀기 = 목차 덮개 · 서랍 접힌 채', r57, ['NEW', 'BASE'])]
    for cid, name, fn, vers in plan:
        res = {}
        for v in (vers if YARD_ON else ['NEW']):
            t1 = time.time()
            try:
                res[v] = fn(br, v)
            except Exception as e:
                res[v] = (False, {'하네스 오류': str(e)[:200]})
            print('  G1R %s %s %.0fs' % (cid, v, time.time() - t1), flush=True)
        yb = [v for v in vers if v != 'NEW' and v in res]
        base_ok = None if not yb else any(res[v][0] for v in yb)
        R('G1R', cid, name, res['NEW'][0], base_ok, {v: res[v][1] for v in res})


# ═══ G2 — 떠 있는 창 누름 차례 ═══
# 씨앗(G2 · G3 · G7 공통 = 시안 setup 꼴) — 65 에 블록 588c90(공식) · 트리거 하나가 없으면 넣음(새 판만 · 바탕엔 G3 없음) · 쪽 안 · 가짜 원격만
G2_SETUP = r"""(async()=>{window.G3FOLDMEM=false;ndResFold(__FOLD__);await new Promise(r=>setTimeout(r,1500));if(window.G3){const b=G3.blocks().find(x=>x.key==='U:^588c90');if(b&&!ggOf('P065').some(g=>g&&g.ref===b.key))await G3.push('P065','c',{t:b.text,ref:b.key});if(!ggOf('P065').some(g=>g&&(g.f||'t')==='t'))await G3.push('P065','t',{t:'관문 트리거'})};await openView(65,navList());await new Promise(r=>setTimeout(r,2500));
  return !document.getElementById('view').classList.contains('hide')})()"""
G2_OPEN = {
    'gguw': ('쓰인 문항 창', r"""(async()=>{const e=document.querySelector('#view .g3cc:not(.g3cq) .g3tx')||document.querySelector('#view .g3cc:not(.g3cq)');if(!e)return '블록 줄 없음';e.click();
             await new Promise(r=>setTimeout(r,1800));return !!document.getElementById('gguw')})()""", '#gguw'),
    'concept': ('개념 창', r"""(async()=>{const r=rec(71);conceptSheet(conceptsOf(r)[0].k,r);await new Promise(r=>setTimeout(r,1500));return !!document.getElementById('sh-concept')})()""", '#sh-concept'),
    'pin': ('비교 창', r"""(async()=>{await vSwapOpen(64);await new Promise(r=>setTimeout(r,3500));return document.querySelectorAll('.vpin').length>0})()""", '.vpin'),
    'pop': ('작은 창(서랍 O△X)', r"""(async()=>{if(!window.g3PopToggle)return 'g3PopToggle 없음';const ox=document.querySelector('#ndList .ndrow[data-no="65"] .ndox');if(!ox)return 'O△X 없음';
             ox.scrollIntoView({block:'center'});g3PopToggle(65,ox);await new Promise(r=>setTimeout(r,900));return !!document.getElementById('g3Pop')})()""", '#g3Pop'),
}
G2_CLOSE = r"""(()=>{try{if(window.g3PopToggle&&document.getElementById('g3Pop'))g3PopToggle(65,document.querySelector('#ndList .ndrow[data-no="65"] .ndox'))}catch(_){}   /* 작은 창은 앱 길로 먼저 닫음(요소만 걷으면 열린 표시 G3P 가 남아 다음 열기가 닫기로 감) */
  ['gguw','sh-concept','g3Pop','tyPop','g3Af','g3Tip'].forEach(id=>{const e=document.getElementById(id);if(e)e.remove()});document.querySelectorAll('.vpin').forEach(e=>e.remove())})()"""
# 창 W 를 본창 V 아래 끝에 반쯤 걸치게 옮기고 세 자리를 고름: O = 겹친 데 · Q = 본창만 보이는 자리(머리 줄 · 누를 것 아님) · P = 창만 보이는 자리(본창 밖 · 누를 것 아님)
G2_GEOM = r"""([sel,move])=>{const ACT='button,a,input,select,textarea,label,[role=button],.jgo,[data-go],canvas,.twgrip,[data-gguugo],.g3pc,.ndox,.ndrow,img,.vpb';   /* .vpb · img = 비교 창 몸(누르면 살아 있는 창이 됨 — 앞으로만 올리는 누름이 아님) */
  const Ws=[...document.querySelectorAll(sel)];const W=Ws[Ws.length-1];if(!W)return {noW:1};
  const pn=W.querySelector(':scope>.panel');const P=(pn&&getComputedStyle(pn).position!=='static')?pn:W;
  const V=document.getElementById('view');if(!V||V.classList.contains('hide'))return {noV:1};const VP=V.querySelector(':scope>.panel')||V;
  const inR=(r,x,y)=>x>=r.left&&x<=r.right&&y>=r.top&&y<=r.bottom;
  /* host 안 · ex(다른 창) 밖 · 누를 것 아닌 첫 자리(first 줄 먼저 · 다음 10px 격자) */
  const pick=(R,ex,host,first)=>{const ys=(first||[]).slice();for(let y=R.top+6;y<R.bottom-6;y+=10)ys.push(y);
    for(const y of ys){for(let x=R.left+8;x<R.right-8;x+=8){if(ex&&inR(ex,x,y))continue;if(x<1||y<1||x>innerWidth-1||y>innerHeight-1)continue;
      const e=document.elementFromPoint(x,y);if(e&&host.contains(e)&&!e.closest(ACT))return {x,y,t:e.tagName+'.'+String(e.className).slice(0,20)}}}return null};
  /* 창을 본창에 반쯤 걸침 — 아래(below) · 오른쪽(right) · 위(above) 차례로 세 자리(O 겹친 데 · Q 본창만 · P 창만)가 다 나오는 첫 자리 */
  const tryAt=mode=>{let vr=VP.getBoundingClientRect(),pr=P.getBoundingClientRect();
    if(mode){let l,t;if(mode==='below'){l=vr.left+vr.width*0.4;t=vr.bottom-pr.height*0.5}else if(mode==='right'){l=vr.right-pr.width*0.5;t=vr.top+20}else{l=vr.left+vr.width*0.4;t=vr.top-pr.height*0.5}
      l=Math.round(Math.max(0,Math.min(innerWidth-pr.width,l)));t=Math.round(Math.max(0,Math.min(innerHeight-pr.height,t)));P.style.left=l+'px';P.style.top=t+'px';pr=P.getBoundingClientRect();vr=VP.getBoundingClientRect()}
    const ix=[Math.max(vr.left,pr.left),Math.max(vr.top,pr.top),Math.min(vr.right,pr.right),Math.min(vr.bottom,pr.bottom)];
    const box={vr:[vr.left,vr.top,vr.right,vr.bottom].map(Math.round),pr:[pr.left,pr.top,pr.right,pr.bottom].map(Math.round)};
    if(ix[2]-ix[0]<8||ix[3]-ix[1]<8)return Object.assign({mode,noOverlap:1},box);
    const O={x:(ix[0]+ix[2])/2,y:(ix[1]+ix[3])/2};
    const vt=V.querySelector('.vtop'),vb=vt?vt.getBoundingClientRect():null;
    return Object.assign({mode,O,Q:pick(vr,pr,V,vb?[vb.top+10,vb.top+vb.height/2]:[]),P:pick(pr,vr,W,[pr.top+8,pr.top+16])},box)};
  if(!move)return tryAt(null);
  let last=null;for(const m of ['below','right','above']){const g=tryAt(m);last=g;if(g.O&&g.Q&&g.P)return g}return last}"""
G2_PLAN = r"""([sel,mode])=>{const Ws=[...document.querySelectorAll(sel)];const W=Ws[Ws.length-1];if(!W)return null;
  const pn=W.querySelector(':scope>.panel');const P=(pn&&getComputedStyle(pn).position!=='static')?pn:W;
  const V=document.getElementById('view');const VP=V.querySelector(':scope>.panel')||V;const vr=VP.getBoundingClientRect(),pr=P.getBoundingClientRect();
  let l,t;if(mode==='below'){l=vr.left+vr.width*0.4;t=vr.bottom-pr.height*0.5}else if(mode==='right'){l=vr.right-pr.width*0.5;t=vr.top+20}else{l=vr.left+vr.width*0.4;t=vr.top-pr.height*0.5}
  l=Math.round(Math.max(0,Math.min(innerWidth-pr.width,l)));t=Math.round(Math.max(0,Math.min(innerHeight-pr.height,t)));
  const H=[...W.querySelectorAll('.twhandle')].find(h=>__H.vis(h));if(!H)return {noHandle:1};const hr=H.getBoundingClientRect();const ACT='button,a,input,select,textarea,label,[role=button],[data-gguugo]';
  for(let y=hr.top+4;y<hr.bottom-2;y+=4)for(let x=hr.left+6;x<hr.right-6;x+=6){const e=document.elementFromPoint(x,y);if(e&&H.contains(e)&&!e.closest(ACT))return {h:{x,y},dl:l-pr.left,dt:t-pr.top}}
  return {noPoint:1}}"""
TOP_AT = r"""([x,y,sel])=>{const e=document.elementFromPoint(x,y);if(!e)return 'none';const Ws=[...document.querySelectorAll(sel)];const W=Ws[Ws.length-1];
  if(W&&W.contains(e))return 'W';if(document.getElementById('view').contains(e))return 'V';const d=document.getElementById('navdr');if(d&&d.contains(e))return 'D';return e.tagName+'.'+String(e.className).slice(0,20)}"""


def g2_one(br, v, devk, wk):
    (size, touch) = DEVS[devk]
    p = dev(br, v, size, touch)
    try:
        tools(p)
        ok0 = p.ev(G2_SETUP.replace('__FOLD__', 'true' if touch else 'false'))
        p.ev(G2_CLOSE)
        name, opn, sel = G2_OPEN[wk]
        o = p.ev(opn)
        p.wait(500)
        if ok0 is not True or o is not True:
            return False, {'본창': ok0, '창 열기': o}
        geo, plans = None, []
        for mode in (() if wk == 'pop' else ('below', 'right', 'above')):   # 창 손잡이를 진짜로 끌어 본창에 반쯤 걸침(아래 · 오른쪽 · 위 차례로 세 자리가 다 나오는 첫 자리)
            plan = p.ev(G2_PLAN, [sel, mode])
            plans.append(plan)
            if plan and plan.get('h') and (abs(plan['dl']) > 2 or abs(plan['dt']) > 2):
                hx, hy = plan['h']['x'], plan['h']['y']
                if touch:
                    swipe(p, hx, hy, hx + plan['dl'], hy + plan['dt'], steps=12, dur=360)
                else:
                    drag_mouse(p, hx, hy, hx + plan['dl'], hy + plan['dt'])
                p.wait(500)
            geo = p.ev(G2_GEOM, [sel, False])
            geo['mode'] = mode
            if geo.get('O') and geo.get('Q') and geo.get('P'):
                break
        if wk == 'pop':   # 작은 창(#g3Pop · 손잡이 없음 · 열 때만 자리 잡음)은 글로 옮겨 본창에 걸침
            geo = p.ev(G2_GEOM, [sel, True])
        if not geo.get('O') or not geo.get('Q'):
            return False, {'자리': geo, '끌기': plans}
        O, Q, P = geo['O'], geo['Q'], geo.get('P')
        w0 = p.ev(TOP_AT, [O['x'], O['y'], sel])
        press(p, Q['x'], Q['y'], touch)
        p.wait(700)
        v1 = p.ev(TOP_AT, [O['x'], O['y'], sel])
        gone = p.ev("(s)=>!document.querySelector(s)", sel)
        v1ok = v1 == 'V' or (gone and wk == 'pop')
        if wk == 'pop' and gone:   # 작은 창 = 바깥 누름에 닫힘 → 다시 열기(진짜 O△X 누름) → 그 창 맨 위
            ox = p.ev("(()=>{const e=document.querySelector('#ndList .ndrow[data-no=\"65\"] .ndox');return e?__H.hit(e):null})()")
            if ox and ox.get('on'):
                press(p, ox['cx'], ox['cy'], touch)
                p.wait(900)
            g = p.ev("(()=>{const e=document.getElementById('g3Pop');if(!e)return null;const r=e.getBoundingClientRect();const t=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return !!t&&e.contains(t)})()")
            return bool(v1ok and g), {'자리': geo, '처음': w0, '본창 누른 뒤': 'W 닫힘(바깥 누름)', 'O△X 다시 누름 → 작은 창 맨 위': g}
        if not P:
            return False, {'자리': geo, '처음': w0, '본창 누른 뒤': v1, '창 자리': None}
        pin_no = p.ev("(()=>{const L=[...document.querySelectorAll('.vpin')];const b=L[L.length-1];return b?+b.dataset.no:null})()") if wk == 'pin' else None
        press(p, P['x'], P['y'], touch)
        p.wait(900)
        w2 = p.ev(TOP_AT, [O['x'], O['y'], sel])
        d = {'자리': geo, '처음': w0, '본창 누른 뒤': v1, '창 누른 뒤': w2}
        # 비교 창(멈춘 그림 창)은 누르면 그 자리 · 크기에서 살아 있는 창이 됨(패치 #18 · 시안 v22) — 누른 문항(pin_no)이 본창이 되어 맨 위면 「그 창 맨 위」
        conv = bool(wk == 'pin' and w2 == 'V' and pin_no and p.ev('VNO') == pin_no)
        if wk == 'pin':
            d['비교 창 누름 = 살아 있는 창(그 문항 %s)' % pin_no] = conv
        ok = bool(v1ok and (w2 == 'W' or conv))
        if conv:
            sel = '#view'   # 서랍 칸은 살아 있는 창(본창)과 서랍 사이 차례를 잼
        if touch:   # 폰 — 서랍 펴고 서랍 누름 → 서랍 위 · 창 누름 → 창 위
            p.ev('ndResFold(false)')
            p.wait(1000)
            dg = p.ev(r"""(sel)=>{const ACT='button,a,input,select,textarea,label,[role=button],.ndox,.ndno,.ndt,.ndrow,#ndGrip,.pwchip';const D=document.getElementById('navdr');const Ws=[...document.querySelectorAll(sel)];const W=Ws[Ws.length-1];
              if(!D||!W)return null;const pn=W.querySelector(':scope>.panel');const P=(pn&&getComputedStyle(pn).position!=='static')?pn:W;const dr=D.getBoundingClientRect(),pr=P.getBoundingClientRect();
              const ix=[Math.max(dr.left,pr.left),Math.max(dr.top,pr.top),Math.min(dr.right,pr.right),Math.min(dr.bottom,pr.bottom)];if(ix[2]-ix[0]<8||ix[3]-ix[1]<8)return {noOverlap:1};
              const O={x:(ix[0]+ix[2])/2,y:(ix[1]+ix[3])/2};let Dp=null,Wp=null;const inR=(r,x,y)=>x>=r.left&&x<=r.right&&y>=r.top&&y<=r.bottom;
              for(let y=dr.top+4;y<dr.bottom-4&&!Dp;y+=8)for(let x=dr.left+4;x<dr.right-4;x+=8){if(inR(pr,x,y))continue;const e=document.elementFromPoint(x,y);if(e&&D.contains(e)&&!e.closest(ACT)){Dp={x,y};break}}
              for(let y=pr.top+4;y<pr.bottom-4&&!Wp;y+=8)for(let x=pr.left+4;x<pr.right-4;x+=8){if(inR(dr,x,y))continue;const e=document.elementFromPoint(x,y);if(e&&W.contains(e)&&!e.closest('button,a,input,textarea,canvas,.twgrip,[data-gguugo],img,.vpb')){Wp={x,y};break}}
              return {O,Dp,Wp}}""", sel)
            if dg and dg.get('Dp') and dg.get('Wp'):
                press(p, dg['Dp']['x'], dg['Dp']['y'], True)
                p.wait(700)
                d3 = p.ev(TOP_AT, [dg['O']['x'], dg['O']['y'], sel])
                press(p, dg['Wp']['x'], dg['Wp']['y'], True)
                p.wait(700)
                d4 = p.ev(TOP_AT, [dg['O']['x'], dg['O']['y'], sel])
                d.update({'서랍 누른 뒤': d3, '다시 창 누른 뒤': d4})
                ok = ok and d3 == 'D' and d4 == 'W'
            else:
                d['서랍 자리'] = dg
                ok = False
        d['오류'] = errs(p)[:3]
        return ok, d
    finally:
        p.close()


def g2(br):
    for devk in ('PC', '폰'):
        for wk in ('gguw', 'concept', 'pin', 'pop'):
            if wk == 'pop' and devk == '폰':
                continue   # 폰의 서랍 O△X 작은 창은 펴진 서랍 위에 뜬다(본창을 덮지 않음) — 서랍 위 차례는 아래 서랍 칸이 잼
            res = {}
            for v in (['NEW', 'BASE'] if YARD_ON else ['NEW']):
                t1 = time.time()
                try:
                    res[v] = g2_one(br, v, devk, wk)
                except Exception as e:
                    res[v] = (False, {'하네스 오류': str(e)[:200]})
                print('  G2 %s %s %s %.0fs' % (devk, wk, v, time.time() - t1), flush=True)
            nm = '%s %s 이 본창을 덮은 채 — 본창 보이는 자리 진짜 누름 → 본창 맨 위 · 그 창 누름 → 그 창 맨 위%s' % (devk, G2_OPEN[wk][0], ' · 서랍 누름 → 서랍 위 · 창 → 창 위' if devk == '폰' else '')
            R('G2', '%s-%s' % (devk, wk), nm, res['NEW'][0], res['BASE'][0] if 'BASE' in res else None, {k: x[1] for k, x in res.items()})


# ═══ G3 — 1/3 · 기억된 크기 ═══
G3_PREP = r"""(async()=>{window.G3FOLDMEM=false;ndResFold(__FOLD__);await new Promise(r=>setTimeout(r,1500));if(window.G3){const b=G3.blocks().find(x=>x.key==='U:^588c90');if(b&&!ggOf('P065').some(g=>g&&g.ref===b.key))await G3.push('P065','c',{t:b.text,ref:b.key});if(!ggOf('P065').some(g=>g&&(g.f||'t')==='t'))await G3.push('P065','t',{t:'관문 트리거'})};await openView(65,navList());await new Promise(r=>setTimeout(r,2500));
  const v=document.getElementById('view');return !v.classList.contains('hide')})()"""
G3_WIN = [
    ('view', '본창(문항 창)', None, '#view', 2),
    ('ty', '근거 작은 창', r"""(async()=>{const e=document.querySelector('#view .g3f .g3lb');if(!e)return '근거 글자 없음';e.click();await new Promise(r=>setTimeout(r,900));return !!document.getElementById('tyPop')})()""", '#tyPop', 3),
    ('block', '블록 창(쓰인 문항 창)', G2_OPEN['gguw'][1], '#gguw', 3),
    ('tnum', '숫자 목록 창(트리거 쓰인 수)', r"""(async()=>{const e=document.querySelector('#view .g3list .g3r[data-f="t"] .g3use');if(!e)return '트리거 수 없음';e.click();await new Promise(r=>setTimeout(r,1500));return !!document.getElementById('gguw')})()""", '#gguw', 3),
    ('cnum', '숫자 목록 창(공식 쓰인 수)', r"""(async()=>{const e=document.querySelector('#view .g3list .g3r.g3cc:not(.g3cq) .g3use');if(!e)return '공식 수 없음';e.click();await new Promise(r=>setTimeout(r,1500));return !!document.getElementById('gguw')})()""", '#gguw', 3),
    ('cq', '이은 개념 창(이은 개념 쓰인 수)', r"""(async()=>{await openView(66,navList());await new Promise(r=>setTimeout(r,2500));const e=document.querySelector('#view .g3cq .g3use[data-g3useq]');if(!e)return '이은 개념 수 없음';e.click();
             await new Promise(r=>setTimeout(r,1500));return !!document.getElementById('gguw')})()""", '#gguw', 3),
    ('concept', '개념 창', G2_OPEN['concept'][1], '#sh-concept', 3),
    ('pin', '비교 창', G2_OPEN['pin'][1], '.vpin', 3),
    ('pop', '서랍 작은 창', G2_OPEN['pop'][1], '#g3Pop', 3),
    ('af', '정답 정정 창', r"""(async()=>{if(!window.g3AfPop)return 'g3AfPop 없음';const b=document.querySelectorAll('#omrPad button[data-omr]')[1];if(!b)return 'OMR 없음';await g3AfPop(VNO,b);await new Promise(r=>setTimeout(r,500));return !!document.getElementById('g3Af')})()""", '#g3Af', 3),
    ('del', '빼기 확인', r"""(async()=>{await openView(66,navList());await new Promise(r=>setTimeout(r,2500));if(!window.g3CqDelAsk)return 'g3CqDelAsk 없음';const c=g3Cq('P066')[0];if(!c)return '이은 개념 없음';g3CqDelAsk('P066|'+c.k);
             await new Promise(r=>setTimeout(r,600));return !![...document.querySelectorAll('.sheet')].find(s=>/이은 개념 빼기/.test(s.textContent))})()""", '.sheet.__del', 3),
    ('mc', '암기카드 창(makeFloat · 세 과목)', r"""(async()=>{mcardWin(65);await new Promise(r=>setTimeout(r,900));return !!document.querySelector('.mcwin')})()""", '.mcwin', 3),
]
G3_H = r"""(sel)=>{let W;if(sel==='.sheet.__del')W=[...document.querySelectorAll('.sheet')].find(s=>/이은 개념 빼기/.test(s.textContent));else{const L=[...document.querySelectorAll(sel)];W=L[L.length-1]}
  if(!W)return null;const pn=W.querySelector(':scope>.panel');const P=pn||W;const r=P.getBoundingClientRect();return {h:Math.round(r.height*10)/10,w:Math.round(r.width),ih:innerHeight,top:Math.round(r.top)}}"""


def g3_dev(br, v, devk):
    (size, touch) = DEVS[devk]
    out = {}
    p = dev(br, v, size, touch)
    try:
        tools(p)
        for k, nm, opn, sel, lim in G3_WIN:
            p.ev(G2_CLOSE)
            try:
                p.ev("(async()=>{if(VNO!==65){await openView(65,navList());await new Promise(r=>setTimeout(r,2000))}})()") if k != 'view' else None
            except Exception:
                pass
            if k == 'view':
                o = p.ev(G3_PREP.replace('__FOLD__', 'true' if touch else 'false'))
            else:
                o = p.ev(opn)
            p.wait(400)
            h = p.ev(G3_H, sel) if o is True else None
            out[k] = (o, h)
            if sel == '.sheet.__del':
                p.ev("(()=>{const s=[...document.querySelectorAll('.sheet')].find(s=>/이은 개념 빼기/.test(s.textContent));if(s)s.remove()})()")
            if k == 'mc':
                p.ev("(()=>{const m=document.querySelector('.mcwin');if(m)m.remove();try{MCW=null}catch(_){}})()")
        out['_err'] = errs(p)[:4]
    finally:
        p.close()
    return out


def g3_mem(br, v, devk):
    """손으로 키운 크기 기억 — twgrip 진짜 끌기(PC 마우스 · 폰 CDP 터치) → 다시 불러(reload) → 다시 열면 그 크기 · 쓰인 문항 창(jagwa.win.gguse) · 본창(jagwa.win.view2)"""
    (size, touch) = DEVS[devk]
    p = dev(br, v, size, touch)
    d = {}
    try:
        tools(p)
        ok0 = p.ev(G3_PREP.replace('__FOLD__', 'true' if touch else 'false'))
        if ok0 is not True:
            return False, {'본창': ok0}
        res = True
        for k, opn, sel, key, dy in (('block', G2_OPEN['gguw'][1], '#gguw', 'jagwa.win.gguse', 150), ('view', None, '#view', 'jagwa.win.view2', 110)):
            p.ev(G2_CLOSE)
            o = p.ev(opn) if opn else True
            p.wait(400)
            g = p.ev(r"""(sel)=>{const L=[...document.querySelectorAll(sel)];const W=L[L.length-1];if(!W)return null;const P=W.querySelector(':scope>.panel')||W;const g=P.querySelector(':scope>.twgrip');
              if(!g)return {nogrip:1};const r=g.getBoundingClientRect(),pr=P.getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2,h:pr.height,ih:innerHeight,on:(document.elementFromPoint(r.left+r.width/2,r.top+r.height/2)===g)}}""", sel)
            if o is not True or not g or not g.get('x') or not g.get('on'):
                d[k] = {'열기': o, '손잡이': g}
                res = False
                continue
            dy2 = min(dy, int(g['ih'] - g['y'] - 12))
            if touch:
                swipe(p, g['x'], g['y'], g['x'], g['y'] + dy2, steps=10, dur=250)
            else:
                drag_mouse(p, g['x'], g['y'], g['x'], g['y'] + dy2)
            p.wait(500)
            h1 = p.ev(G3_H, sel)
            saved = p.ev("(k)=>localStorage.getItem(k)", key)
            p.reload()
            tools(p)
            p.ev(G3_PREP.replace('__FOLD__', 'true' if touch else 'false'))
            p.ev(G2_CLOSE)
            if opn:
                p.ev(opn)
            p.wait(500)
            h2 = p.ev(G3_H, sel)
            ok = bool(h1 and h2 and h1['h'] > g['h'] + 30 and abs(h2['h'] - h1['h']) <= 3)
            d[k] = {'처음': round(g['h'], 1), '키운 뒤': h1 and h1['h'], '다시 불러 연 뒤': h2 and h2['h'], '기억': saved, 'innerHeight': g['ih']}
            res = res and ok
        d['오류'] = errs(p)[:3]
        return res, d
    finally:
        p.close()


def g3(br):
    for devk in ('PC', '폰'):
        res = {}
        for v in (['NEW', 'BASE'] if YARD_ON else ['NEW']):
            t1 = time.time()
            try:
                res[v] = g3_dev(br, v, devk)
            except Exception as e:
                res[v] = {'_harness': str(e)[:200]}
            print('  G3 %s %s %.0fs' % (devk, v, time.time() - t1), flush=True)
        for k, nm, opn, sel, lim in G3_WIN:
            def judge(x):
                if not x or not isinstance(x, tuple):
                    return None, x
                o, h = x
                if o is not True or not h:
                    return False, {'열기': o}
                return h['h'] <= h['ih'] / lim + 1, {'높이': h['h'], '상한': round(h['ih'] / lim, 1), '폭': h['w']}
            n_ok, n_d = judge(res['NEW'].get(k))
            b_ok, b_d = judge(res.get('BASE', {}).get(k)) if 'BASE' in res else (None, None)
            R('G3', '%s-%s' % (devk, k), '%s %s 처음 높이 ≤ 화면 1/%d' % (devk, nm, lim), n_ok, b_ok, {'새': n_d, '바탕': b_d})
        R('G3', '%s-오류' % devk, '%s 창 열고 닫는 동안 페이지 오류 0' % devk, not res['NEW'].get('_err'), None, res['NEW'].get('_err'), yard=False)
        mres = {}
        for v in (['NEW', 'BASE'] if YARD_ON else ['NEW']):
            try:
                mres[v] = g3_mem(br, v, devk)
            except Exception as e:
                mres[v] = (False, {'하네스 오류': str(e)[:200]})
        R('G3', '%s-기억' % devk, '%s 손으로 키운 크기(twgrip 진짜 끌기) → 다시 불러 다시 열면 그 크기(1/3 · 1/2 로 안 줄임) — 쓰인 문항 창 · 본창' % devk,
          mres['NEW'][0], mres['BASE'][0] if 'BASE' in mres else None, {k: x[1] for k, x in mres.items()}, yard=False)


# ═══ G5 — 지학 · 생물 표본 ═══
CARD_PICK = r"""(()=>{const it=[...document.querySelectorAll('#list .item')].find(x=>__H.vis(x)&&x.getBoundingClientRect().top>60&&x.getBoundingClientRect().bottom<innerHeight-10)||document.querySelector('#list .item');
  if(!it)return null;it.scrollIntoView({block:'center'});const ttl=it.querySelector('.sub')||it.querySelector('.num');
  const cand=[...it.querySelectorAll('*')].filter(e=>__H.vis(e)&&e.children.length===0&&__H.tx(e).length>8&&!e.closest('.sub,.num,button,a,.chip,[data-go],.jgo')&&!(ttl&&ttl.contains(e)));
  const body=it.querySelector('.prev')||cand[0]||null;
  return {no:+(it.dataset.no||0),ttl:ttl?__H.at(ttl):null,body:body?__H.at(body):null,bodyCls:body?body.className:null,sub:!!it.querySelector('.sub')}})()"""
GG_SIG = r"""(()=>{const out=[];document.querySelectorAll('#view [data-ggbox]').forEach(b=>{b.querySelectorAll('button,a,[data-gged],[data-ggdel],[data-ggsave],textarea,input,[data-gguse],[data-ggref],[role=button],.lk,.chip').forEach(e=>{
  const at=[...e.attributes].map(a=>a.name).filter(n=>n.startsWith('data-')).sort().join(',');
  const cls=String(e.className||'').split(/\s+/).filter(c=>c&&!/^(on|hide|has|act|open|sel)$/.test(c)).sort().join('.');
  out.push(e.tagName.toLowerCase()+'.'+cls+'['+at+']:'+__H.tx(e).slice(0,16))})});return {n:document.querySelectorAll('#view [data-ggbox]').length,sig:out,g3:typeof G3!=='undefined',g3box:!!document.querySelector('.g3box')}})()"""


def g5_one(br, v, subj, devk):
    (size, touch) = DEVS[devk]
    p = dev(br, v, size, touch, subj=subj)
    d = {}
    try:
        tools(p)
        d['OMR(카드 층)'] = p.ev("(()=>{const o=document.getElementById('omrPad');return {pad:!!o,display:o?getComputedStyle(o).display:null,layer:document.body.dataset.layer}})()")
        c = p.ev(CARD_PICK)
        d['카드'] = c and {k: c[k] for k in ('no', 'sub', 'bodyCls')}
        opened_body = None
        if c and c.get('body') and c['body'].get('on'):
            press(p, c['body']['cx'], c['body']['cy'], touch)
            p.wait(1800)
            opened_body = p.ev("!document.getElementById('view').classList.contains('hide')")
            if opened_body:
                p.ev("(()=>{const x=document.getElementById('vBack');if(x)x.click()})()")
                p.wait(800)
        c = p.ev(CARD_PICK)
        opened_ttl = None
        if c and c.get('ttl') and c['ttl'].get('on'):
            press(p, c['ttl']['cx'], c['ttl']['cy'], touch)
            p.wait(2500)
            opened_ttl = p.ev("!document.getElementById('view').classList.contains('hide')")
        d['본문 누름 → 열림'] = opened_body
        d['제목 누름 → 열림'] = opened_ttl
        vh = p.ev("(()=>{const v=document.getElementById('view');const P=v.querySelector(':scope>.panel')||v;return {h:Math.round(P.getBoundingClientRect().height),ih:innerHeight,res:!!document.querySelector('#omrRes,.omrres')}})()")
        d['본창'] = vh
        d['근거 줄'] = p.ev(GG_SIG)
        d['필기 도구'] = p.ev("[...document.querySelectorAll('#view [data-tool]')].map(e=>e.dataset.tool+':'+__H.vis(e)).join(',')")
        d['정리OMR'] = p.ev("({tab:!!document.getElementById('docTab'),omrTab:typeof omrTab})")
        pops = {}
        for lab, js in (('🃏', "(()=>{const b=[...document.querySelectorAll('#view button,#view .lk,#view span')].find(e=>__H.vis(e)&&/^🃏/.test(__H.tx(e)));return b?__H.at(b):null})()"),
                        ('Claude', "(()=>{const b=[...document.querySelectorAll('#view button,#view .lk,#view span')].find(e=>__H.vis(e)&&__H.tx(e)==='Claude');return b?__H.at(b):null})()")):
            at = p.ev(js)
            if not at or not at.get('on'):
                pops[lab] = {'단추': at and at.get('top')}
                continue
            n0 = p.ev("document.querySelectorAll('.sheet').length")
            press(p, at['cx'], at['cy'], touch)
            p.wait(1500)
            pops[lab] = p.ev(r"""(n0)=>{const S=[...document.querySelectorAll('.sheet')].filter(s=>__H.vis(s)&&s.id!=='view');const s=S[S.length-1];if(!s||document.querySelectorAll('.sheet').length<=n0)return {none:1};
              const P=s.querySelector(':scope>.panel')||s;const r=P.getBoundingClientRect();return {cls:String(s.className).slice(0,40),h:Math.round(r.height),ih:innerHeight}}""", n0)
            p.ev("(()=>{const S=[...document.querySelectorAll('.sheet')].filter(s=>s.id!=='view');const s=S[S.length-1];if(s)s.remove();try{MCW=null}catch(_){}})()")
            p.wait(300)
        d['팝업'] = pops
        if touch:
            p.ev("(()=>{if(!document.getElementById('view').classList.contains('hide')){const x=document.getElementById('vBack');if(x)x.click()}})()")
            p.wait(600)
            f0 = p.ev("(()=>{ndResFold(true);return document.getElementById('navdr').classList.contains('fold')})()")
            p.wait(900)
            st = p.ev(R56_START)
            a = b = None
            if f0 and st:
                swipe(p, st['x'], st['y'], st['x'] + 130, st['y'] + 10)
                p.wait(900)
                a = p.ev("!document.getElementById('navdr').classList.contains('fold')")
                row = p.ev(r"""(()=>{const d=document.getElementById('navdr').getBoundingClientRect();const L=[...document.querySelectorAll('#ndList .ndrow')].map(r=>r.getBoundingClientRect()).filter(r=>r.top>d.top+80&&r.bottom<innerHeight-40);
                  const r=L[Math.floor(L.length/2)];return r?{x:Math.min(d.right-24,r.left+r.width*0.7),y:r.top+r.height/2}:null})()""")
                if a and row:
                    swipe(p, row['x'], row['y'], row['x'] - 120, row['y'] + 5)
                    p.wait(900)
                    b = p.ev("document.getElementById('navdr').classList.contains('fold')")
            d['서랍 밀기'] = {'펴짐': a, '접힘': b, '자리': st}
        d['오류'] = errs(p)[:4]
        return d
    finally:
        p.close()


def g5(br):
    for subj, sn in (('earth', '지학'), ('bio', '생물')):
        for devk in ('PC', '폰'):
            res = {}
            for v in (['NEW', 'BASE'] if YARD_ON else ['NEW']):
                t1 = time.time()
                try:
                    res[v] = g5_one(br, v, subj, devk)
                except Exception as e:
                    res[v] = {'하네스 오류': str(e)[:300], 'tb': traceback.format_exc()[-400:]}
                print('  G5 %s %s %s %.0fs' % (sn, devk, v, time.time() - t1), flush=True)
            n, b = res['NEW'], res.get('BASE')
            pre = '%s %s' % (sn, devk)
            om = n.get('OMR(카드 층)') or {}
            R('G5', pre + '-OMR', pre + ' 정답 창 0 · 오답 초록 테두리 · OMR 길게 누름 정정 창 — 카드 층에 OMR 단추 없음(해당 없음 · 잰 값)', None, None,
              {'새': om, '바탕': (b or {}).get('OMR(카드 층)')})

            def vh_ok(x):
                vv = (x or {}).get('본창') or {}
                return bool(vv.get('h')) and vv['h'] <= vv['ih'] / 2 + 1 if (x or {}).get('제목 누름 → 열림') else False
            R('G5', pre + '-본창', pre + ' 본창 첫 높이 ≤ 화면 1/2', vh_ok(n), vh_ok(b) if b else None, {'새': n.get('본창'), '바탕': (b or {}).get('본창')})

            def pop_ok(x):
                ps = (x or {}).get('팝업') or {}
                hs = [q for q in ps.values() if isinstance(q, dict) and q.get('h')]
                return bool(hs) and all(q['h'] <= q['ih'] / 3 + 1 for q in hs)
            R('G5', pre + '-팝업', pre + ' 팝업(🃏 · Claude) 첫 높이 ≤ 화면 1/3', pop_ok(n), pop_ok(b) if b else None, {'새': n.get('팝업'), '바탕': (b or {}).get('팝업')})

            def card_ok(x):
                return (x or {}).get('본문 누름 → 열림') is False and (x or {}).get('제목 누름 → 열림') is True
            R('G5', pre + '-카드', pre + ' 첫 화면 카드 = 본문 누름 안 엶 · 제목(.sub · 없으면 코드) 누름 엶', card_ok(n), card_ok(b) if b else None,
              {'새': {k: n.get(k) for k in ('카드', '본문 누름 → 열림', '제목 누름 → 열림')}, '바탕': {k: (b or {}).get(k) for k in ('카드', '본문 누름 → 열림', '제목 누름 → 열림')}})
            if devk == '폰':
                def sw_ok(x):
                    s = (x or {}).get('서랍 밀기') or {}
                    return s.get('펴짐') is True and s.get('접힘') is True
                R('G5', pre + '-밀기', pre + ' 서랍 손가락 밀기 = 펴짐 · 접힘', sw_ok(n), sw_ok(b) if b else None, {'새': n.get('서랍 밀기'), '바탕': (b or {}).get('서랍 밀기')})
            gn, gb = n.get('근거 줄') or {}, (b or {}).get('근거 줄') or {}
            same = (not gn.get('g3') and not gn.get('g3box') and gn.get('n', 0) >= 1 and gn.get('sig') == gb.get('sig')) if b else None
            R('G5', pre + '-근거줄', pre + ' 근거 줄 = 원래 그대로(G3 안 돎 · .g3box 0 · 누름 대상 전수 = 바탕)', same, None,
              {'새': {'n': gn.get('n'), 'G3': gn.get('g3'), '대상 수': len(gn.get('sig') or [])}, '다른 대상': sorted(set(gn.get('sig') or []) ^ set(gb.get('sig') or []))[:8]}, yard=False)
            same2 = (n.get('필기 도구') == (b or {}).get('필기 도구') and n.get('정리OMR') == (b or {}).get('정리OMR')) if b else None
            R('G5', pre + '-필기', pre + ' 카드 층 필기 도구 · 정리OMR 탭 = 바탕', same2, None, {'새': [n.get('필기 도구'), n.get('정리OMR')], '바탕': [(b or {}).get('필기 도구'), (b or {}).get('정리OMR')]}, yard=False)
            R('G5', pre + '-오류', pre + ' 페이지 오류 0', not n.get('오류') and '하네스 오류' not in n, None, n.get('오류') or n.get('하네스 오류'), yard=False)


# ═══ G6 — cqx 동기화 ═══
HOLD = r"""
(()=>{window.__cqxHold=true;window.__cqxQ=[];const G=IDBObjectStore.prototype.get;
  IDBObjectStore.prototype.get=function(k){const real=G.call(this,k);if(k!=='cqx'||!window.__cqxHold)return real;
    const fake={result:undefined,error:null,onsuccess:null,onerror:null,readyState:'pending'};
    real.onsuccess=()=>{const fire=()=>{fake.result=real.result;fake.readyState='done';if(fake.onsuccess)fake.onsuccess({target:fake})};if(window.__cqxHold)window.__cqxQ.push(fire);else fire()};
    real.onerror=()=>{if(fake.onerror)fake.onerror({target:fake})};return fake};
  window.__cqxRelease=()=>{window.__cqxHold=false;window.__cqxQ.splice(0).forEach(f=>f())};})();
"""
SYNC_IDLE = "typeof recBusy!=='undefined'&&!recBusy&&((JSON.parse(localStorage.getItem(SMETA_KEY)||'{}').lastSync)||0)>0"
CQ_PICK = r"""(()=>{const out=[];for(const r of DATA){const c=conceptsOf(r);if(c.length>=2)out.push(r[F.NO]);if(out.length>=40)break}return out})()"""


def sync_now(p, touch=False):
    """기록 동기화 — 머리 칩(#recChip) 진짜 누름 · 끝날 때까지"""
    tools(p)
    at = p.ev("(()=>{const c=document.getElementById('recChip');return c?__H.hit(c):null})()")
    t0 = p.ev("Date.now()")
    if at and at.get('on'):
        press(p, at['cx'], at['cy'], touch)
    else:
        p.ev('syncRecords(true)')
    p.pg.wait_for_function("(t0)=>typeof recBusy!=='undefined'&&!recBusy&&((JSON.parse(localStorage.getItem(SMETA_KEY)||'{}').lastSync)||0)>=t0", arg=t0, timeout=60000)
    p.wait(600)
    return bool(at and at.get('on'))


def ui_open(p, no, touch=False):
    """문항 열기(준비 = JS openView) · 근거 줄 펴기(▾ 진짜 누름)"""
    tools(p)
    p.ev("(async()=>{await openView(%d,navList());await new Promise(r=>setTimeout(r,2200))})()" % no)
    off = p.ev("document.getElementById('view').classList.contains('g3off')")
    if off:
        at = p.ev("(()=>{const b=document.getElementById('g3Fold');return b?__H.hit(b):null})()")
        if at and at.get('on'):
            press(p, at['cx'], at['cy'], touch)
            p.wait(700)
    return not p.ev("document.getElementById('view').classList.contains('g3off')")


def ui_hide(p, no, ck, touch=False):
    """이은 개념 줄 ✕ 진짜 누름 → 확인 창 「빼기」 진짜 누름"""
    key = 'P%03d|%s' % (no, ck)
    at = p.ev("(k)=>{const e=document.querySelector('#view .g3cq[data-g3cq=\"'+CSS.escape(k)+'\"] .g3del');return e?__H.hit(e):null}", key)
    if not at or not at.get('on'):
        return {'✕': at}
    press(p, at['cx'], at['cy'], touch)
    p.wait(700)
    b = p.ev("(()=>{const e=document.getElementById('g3cqDo');return e?__H.hit(e):null})()")
    if not b or not b.get('on'):
        return {'빼기 단추': b}
    press(p, b['cx'], b['cy'], touch)
    p.wait(900)
    return True


def ui_comment(p, no, ck, text, touch=False):
    """이은 개념 줄 「댓」 진짜 누름 → 글칸 진짜 누름 · 진짜 키 → 「달기」 진짜 누름"""
    key = 'P%03d|%s' % (no, ck)
    at = p.ev("(k)=>{const e=document.querySelector('#view .g3cq[data-g3cq=\"'+CSS.escape(k)+'\"] .g3cm');return e?__H.hit(e):null}", key)
    if not at or not at.get('on'):
        return {'댓': at}
    press(p, at['cx'], at['cy'], touch)
    p.wait(700)
    ta = p.ev("(k)=>{const e=document.querySelector('[data-g3cqin=\"'+CSS.escape(k)+'\"]');return e?__H.hit(e):null}", key)
    if not ta or not ta.get('on'):
        return {'글칸': ta}
    press(p, ta['cx'], ta['cy'], touch)
    p.wait(200)
    p.pg.keyboard.type(text, delay=15)
    bt = p.ev("(k)=>{const e=document.querySelector('[data-g3cqreply=\"'+CSS.escape(k)+'\"]');return e?__H.hit(e):null}", key)
    if not bt or not bt.get('on'):
        return {'달기': bt}
    press(p, bt['cx'], bt['cy'], touch)
    p.wait(900)
    return True


CQX_STATE = r"""([qa,cka,ckb,qb,ckc,ckd])=>{const X=window.g3CqxGet?g3CqxGet():null;if(!X)return {X:null};
  const has=(q,ck,kind)=>{if(X.hide||X.cs){if(kind==='h')return ((X.hide||{})[q]||[]).indexOf(ck)>=0;return (((X.cs||{})['P'+String(q).padStart(3,'0')+'|'+ck])||[]).length>0}
    const c=X[q];if(!c)return false;return kind==='h'?(c.h||[]).indexOf(ck)>=0:((c.c||{})[ck]||[]).length>0};
  return {aHide:has(qa,cka,'h'),aCm:has(qa,ckb,'c'),bHide:has(qb,ckc,'h'),bCm:has(qb,ckd,'c'),keys:Object.keys(X).slice(0,12)}}"""


def g6_two(br, v):
    """기기 둘(A = PC · B = 폰) 같은 원격 — A 는 qa 에서 빼기 · 댓글 · B 는 qb 에서 빼기 · 댓글 → A 맞춤 → B 맞춤 → A 맞춤 → 둘 다 넷 다 남음"""
    rm = JG.Remote()
    A = dev(br, v, PC, False, who='A', remote=rm)
    B = dev(br, v, PH, True, who='B', remote=rm)
    try:
        for p in (A, B):
            p.pg.wait_for_function(SYNC_IDLE, timeout=60000)
        qs = A.ev(CQ_PICK)
        qa, qb = (59, 71) if 59 in qs and 71 in qs else (qs[0], qs[1])
        ca = A.ev("(n)=>conceptsOf(rec(n)).map(c=>c.k)", qa)
        cb = A.ev("(n)=>conceptsOf(rec(n)).map(c=>c.k)", qb)
        if len(ca) < 2 or len(cb) < 2:
            return False, {'문항': [qa, qb], '개념': [ca, cb]}
        d = {'문항': [qa, qb], '개념 a': ca[:2], '개념 b': cb[:2]}
        d['A 열기'] = ui_open(A, qa)
        d['A 댓글'] = ui_comment(A, qa, ca[1], '기기A 댓글')
        d['A 빼기'] = ui_hide(A, qa, ca[0])
        d['B 열기'] = ui_open(B, qb, True)
        d['B 댓글'] = ui_comment(B, qb, cb[1], '기기B 댓글', True)
        d['B 빼기'] = ui_hide(B, qb, cb[0], True)
        d['맞춤 칩 진짜 누름'] = [sync_now(A), sync_now(B, True), sync_now(A)]
        arg = [qa, ca[0], ca[1], qb, cb[0], cb[1]]
        sa, sb = A.ev(CQX_STATE, arg), B.ev(CQX_STATE, arg)
        d['A'] = sa
        d['B'] = sb
        rmc = rm.rec('phys') or {}
        d['원격 cqx 칸'] = sorted(((rmc.get('data') or {}).get('cqx') or {}).keys())[:12]
        ok = all(sa.get(k) for k in ('aHide', 'aCm', 'bHide', 'bCm')) and all(sb.get(k) for k in ('aHide', 'aCm', 'bHide', 'bCm'))
        ui = A.ev(r"""([qb,ckc,ckd])=>{const k1='P'+String(qb).padStart(3,'0')+'|'+ckc,k2='P'+String(qb).padStart(3,'0')+'|'+ckd;return {hidGone:!document.querySelector('#view .g3cq[data-g3cq="'+CSS.escape(k1)+'"]'),cmHas:!!document.querySelector('#view .g3cq[data-g3cq="'+CSS.escape(k2)+'"] .g3cm.has')}}""", [qb, cb[0], cb[1]])
        if ok:
            ui_open(A, qb)
            ui = A.ev(r"""([qb,ckc,ckd])=>{const k1='P'+String(qb).padStart(3,'0')+'|'+ckc,k2='P'+String(qb).padStart(3,'0')+'|'+ckd;return {hidGone:!document.querySelector('#view .g3cq[data-g3cq="'+CSS.escape(k1)+'"]'),cmHas:!!document.querySelector('#view .g3cq[data-g3cq="'+CSS.escape(k2)+'"] .g3cm.has')}}""", [qb, cb[0], cb[1]])
            ok = ok and ui['hidGone'] and ui['cmHas']
        d['A 화면(qb 근거 줄)'] = ui
        d['오류'] = errs(A)[:3] + errs(B)[:3]
        return bool(ok), d
    finally:
        A.close()
        B.close()


def g6_late(br, v):
    """cqx 읽기 전 동기화 — 원격에 cqx 칸이 있는 채 새 기기(get('cqx') 붙잡음)가 시동 동기화 → 원격 cqx 그대로 · 놓은 뒤 맞추면 받음"""
    rm = JG.Remote()
    A = dev(br, v, PC, False, who='A', remote=rm)
    d = {}
    try:
        A.pg.wait_for_function(SYNC_IDLE, timeout=60000)
        qs = A.ev(CQ_PICK)
        qa = 59 if 59 in qs else qs[0]
        ca = A.ev("(n)=>conceptsOf(rec(n)).map(c=>c.k)", qa)
        ui_open(A, qa)
        d['A 빼기'] = ui_hide(A, qa, ca[0])
        d['A 댓글'] = ui_comment(A, qa, ca[1], '먼저 올린 댓글')
        sync_now(A)
        before = json.dumps(((rm.rec('phys') or {}).get('data') or {}).get('cqx'), ensure_ascii=False, sort_keys=True)
        uq_b = {k: x for k, x in ((rm.rec('phys') or {}).get('u') or {}).items() if k.startswith('cqx|')}
        d['원격 cqx(앞)'] = before[:160]
    finally:
        A.close()
    n0 = len(rm.puts)
    C = dev(br, v, PC, False, who='C', remote=rm, init=HOLD)
    try:
        C.pg.wait_for_function("(n)=>true", arg=0)
        t_end = time.time() + 40
        while time.time() < t_end and len(rm.puts) <= n0:
            C.wait(500)
        C.pg.wait_for_function("typeof recBusy!=='undefined'&&!recBusy", timeout=30000)
        held = C.ev("({hold:!!window.__cqxHold,get:window.g3CqxGet?g3CqxGet():'없음'})")
        after = json.dumps(((rm.rec('phys') or {}).get('data') or {}).get('cqx'), ensure_ascii=False, sort_keys=True)
        uq_a = {k: x for k, x in ((rm.rec('phys') or {}).get('u') or {}).items() if k.startswith('cqx|')}
        d['붙잡은 동안 g3CqxGet()'] = held
        d['시동 동기화 PUT'] = len(rm.puts) - n0
        d['원격 cqx(뒤)'] = after[:160]
        same = after == before and uq_a == uq_b
        d['원격 cqx · 도장 그대로'] = same
        C.ev('window.__cqxRelease()')
        C.wait(800)
        sync_now(C)
        got = C.ev("(q)=>{const X=window.g3CqxGet?g3CqxGet():null;if(!X)return null;return X.hide?{old:1,keys:Object.keys(X)}:{cell:X[q]||null}}", qa)
        d['놓고 맞춘 뒤 C'] = got
        recvd = bool(got and got.get('cell') and (got['cell'].get('h') or []) and (got['cell'].get('c') or {}))
        d['오류'] = errs(C)[:3]
        return bool(same and held.get('get') is None and len(rm.puts) - n0 >= 1 and recvd), d
    finally:
        C.close()


def g6_recv(br, v):
    """받은 cqx = 열린 근거 줄에 바로 — A 가 qb 근거 줄을 연 채 · B 가 qb 에 댓글 · 빼기 · 맞춤 → A 칩 진짜 누름(맞춤)만으로 A 근거 줄에 보임(다시 안 엶)"""
    rm = JG.Remote()
    A = dev(br, v, PC, False, who='A', remote=rm)
    B = dev(br, v, PC, False, who='B', remote=rm)
    try:
        for p in (A, B):
            p.pg.wait_for_function(SYNC_IDLE, timeout=60000)
        qs = A.ev(CQ_PICK)
        qb = 71 if 71 in qs else qs[1]
        cb = A.ev("(n)=>conceptsOf(rec(n)).map(c=>c.k)", qb)
        d = {'문항': qb}
        d['A 열기'] = ui_open(A, qb)
        k1, k2 = 'P%03d|%s' % (qb, cb[0]), 'P%03d|%s' % (qb, cb[1])
        pre = A.ev("([a,b])=>({row:!!document.querySelector('#view .g3cq[data-g3cq=\"'+CSS.escape(a)+'\"]'),has:!!document.querySelector('#view .g3cq[data-g3cq=\"'+CSS.escape(b)+'\"] .g3cm.has')})", [k1, k2])
        ui_open(B, qb)
        d['B 댓글'] = ui_comment(B, qb, cb[1], '받을 댓글')
        d['B 빼기'] = ui_hide(B, qb, cb[0])
        sync_now(B)
        sync_now(A)
        post = A.ev("([a,b])=>({row:!!document.querySelector('#view .g3cq[data-g3cq=\"'+CSS.escape(a)+'\"]'),has:!!document.querySelector('#view .g3cq[data-g3cq=\"'+CSS.escape(b)+'\"] .g3cm.has'),vno:VNO,open:!document.getElementById('view').classList.contains('hide')})", [k1, k2])
        d['A 앞'] = pre
        d['A 맞춘 뒤(다시 안 엶)'] = post
        d['오류'] = errs(A)[:3] + errs(B)[:3]
        return bool(pre['row'] and not pre['has'] and post['open'] and post['vno'] == qb and not post['row'] and post['has']), d
    finally:
        A.close()
        B.close()


def g6_mig(br, v):
    """시안 꼴 cqx 들이기 — kv cqx = {hide:{qa:[ck]}, cs:{'Pqb|ck2':[…]}} 를 넣고 다시 불러 → 새 꼴 칸(qa.h · qb.c) · 옛 열쇠 hide · cs 그대로 · 화면 = qa 에서 그 개념 빠짐"""
    p = dev(br, v, PC, False)
    try:
        p.pg.wait_for_function(SYNC_IDLE, timeout=60000)
        qs = p.ev(CQ_PICK)
        qa, qb = (59, 71) if 59 in qs and 71 in qs else (qs[0], qs[1])
        ca = p.ev("(n)=>conceptsOf(rec(n)).map(c=>c.k)", qa)
        cb = p.ev("(n)=>conceptsOf(rec(n)).map(c=>c.k)", qb)
        old = {'hide': {str(qa): [ca[0]]}, 'cs': {'P%03d|%s' % (qb, cb[1]): [{'k': 'c_old', 't': '옛 꼴 댓글', 'ts': 1760000000000}]}}
        p.ev("(v)=>put('kv','cqx',v)", old)
        p.reload()
        p.wait(1500)
        st = p.ev("([qa,qb])=>{const X=window.g3CqxGet?g3CqxGet():null;return X?{a:X[qa]||null,b:X[qb]||null,hide:!!X.hide,cs:!!X.cs}:null}", [qa, qb])
        kv = p.ev("(async()=>{const v=await get('kv','cqx');return v?{keys:Object.keys(v).sort(),hide:v.hide,cs:v.cs}:null})()")
        ui_open(p, qa)
        gone = p.ev("(k)=>!document.querySelector('#view .g3cq[data-g3cq=\"'+CSS.escape(k)+'\"]')", 'P%03d|%s' % (qa, ca[0]))
        ok = bool(st and st['a'] and ca[0] in (st['a'].get('h') or []) and st['b'] and ((st['b'].get('c') or {}).get(cb[1]) or [{}])[0].get('k') == 'c_old'
                  and kv and kv.get('hide') == old['hide'] and kv.get('cs') == old['cs'] and gone)
        return ok, {'칸': st, 'kv': kv and kv.get('keys'), '옛 열쇠 그대로': bool(kv and kv.get('hide') == old['hide'] and kv.get('cs') == old['cs']), 'qa 화면에서 빠짐': gone, '오류': errs(p)[:3]}
    finally:
        p.close()


def g6(br):
    plan = [('two', '기기 둘 다른 문항에서 빼기 · 댓글(진짜 누름) → 맞춘 뒤 둘 다 남음(칸 단위)', g6_two, ['NEW', 'SIAN', 'SIANSYNC', 'BASE']),
            ('late', 'cqx 읽기 전 동기화(get 늦춤) → 원격 cqx · 도장 그대로(빈 값으로 안 덮음) · 붙잡은 동안 g3CqxGet() = null · 놓고 맞추면 받음', g6_late, ['NEW', 'SIANSYNC']),
            ('recv', '받은 cqx = 열린 근거 줄에 바로(맞춤 칩 진짜 누름 · 다시 안 엶)', g6_recv, ['NEW', 'SIANSYNC']),
            ('mig', '시안 꼴 cqx 들이기 → 새 꼴로 옮겨짐 · 옛 열쇠 hide · cs 그대로(안 지움) · 화면에 반영', g6_mig, ['NEW', 'SIAN'])]
    for cid, name, fn, vers in plan:
        res = {}
        for v in (vers if YARD_ON else ['NEW']):
            t1 = time.time()
            try:
                res[v] = fn(br, v)
            except Exception as e:
                res[v] = (False, {'하네스 오류': str(e)[:300], 'tb': traceback.format_exc()[-300:]})
            print('  G6 %s %s %.0fs' % (cid, v, time.time() - t1), flush=True)
        yb = [v for v in vers if v != 'NEW' and v in res]
        R('G6', cid, name, res['NEW'][0], (any(res[v][0] for v in yb) if yb else None), {v: res[v][1] for v in res})


# ═══ G7 — 화면 훑기 ═══
SWEEP_X = r"""(sel)=>{const roots=[...document.querySelectorAll(sel)].filter(__H.vis);
  if(!roots.length)return {noroot:1};
  const clipR=e=>{let r=e.getBoundingClientRect(),L=r.left,T=r.top,Rr=r.right,B=r.bottom;for(let q=e.parentElement;q&&q!==document.body;q=q.parentElement){const cs=getComputedStyle(q);
    if(cs.overflowX!=='visible'||cs.overflowY!=='visible'){const b=q.getBoundingClientRect();L=Math.max(L,b.left);T=Math.max(T,b.top);Rr=Math.min(Rr,b.right);B=Math.min(B,b.bottom)}}return [L,T,Rr,B]};
  const ACT=__H.ACT,cov=[],raw=[];
  roots.forEach(r=>{[r,...r.querySelectorAll(ACT)].forEach(e=>{if(!e.matches(ACT)||!__H.vis(e)||e.disabled||getComputedStyle(e).pointerEvents==='none'||e.closest('.katex-mathml'))return;
    const c=clipR(e);if(c[2]-c[0]<3||c[3]-c[1]<3)return;const x=(c[0]+c[2])/2,y=(c[1]+c[3])/2;if(x<0||y<0||x>innerWidth||y>innerHeight)return;
    const a=document.elementFromPoint(x,y);const own=e.closest('.vpin');if(own&&a&&a.closest('.vpin')&&a.closest('.vpin')!==own)return;   /* 비껴 쌓인 비교 창 = 아래 창 몸은 덮이는 것이 뜻 */
    if(!a||!(a===e||e.contains(a)))cov.push(e.tagName.toLowerCase()+'.'+String(e.className).slice(0,18)+':'+__H.tx(e).slice(0,10)+'←'+(a?(a.id||a.tagName.toLowerCase()+'.'+String(a.className).slice(0,18)):'없음'))});
    const tw=document.createTreeWalker(r,NodeFilter.SHOW_TEXT,{acceptNode:n=>{const p=n.parentElement;if(!p||p.closest('.katex-mathml,script,style,textarea,annotation'))return NodeFilter.FILTER_REJECT;
      const cs=getComputedStyle(p);return (cs.display==='none'||cs.visibility==='hidden'||!p.getClientRects().length)?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT}});   /* 숨은 조상(.ggpan.hide 등) 안 = 안 보이는 글 */
    let s='';for(let n=tw.nextNode();n;n=tw.nextNode())s+=n.nodeValue+' ';
    const m=[...(s.match(/\$[^$\n]{1,80}\$/g)||[]),...(s.match(/<span/g)||[]),...(s.match(/\^[0-9a-f]{6}\b/g)||[])];if(m.length)raw.push(...m.slice(0,5))});
  const out=roots.map(r=>{const b=r.getBoundingClientRect();return {l:Math.round(b.left),t:Math.round(b.top),r:Math.round(b.right),b:Math.round(b.bottom)}});
  const off=out.filter(b=>b.l<-1||b.t<-1||b.r>innerWidth+1||b.b>innerHeight+1);
  return {cov:[...new Set(cov)].slice(0,8),raw:[...new Set(raw)].slice(0,8),rootOff:off,box:out[0]}}"""
G7_WIN = [
    ('pop', '서랍 작은 창', 'pop', '#g3Pop'),
    ('tip', '말풍선(작은 창 공식 줄)', 'tip', '#g3Pop .g3ptip'),
    ('view', '본창', None, '#view'),
    ('gg', '근거 줄 펴기', None, '#view .g3box'),
    ('ty', '근거 작은 창', 'ty', '#tyPop'),
    ('block', '블록 창', 'block', '#gguw'),
    ('ovL', '덮개(왼쪽 · 쓴 문항/목차)', 'ovL', '#gguw .thcL'),
    ('ovR', '덮개(오른쪽)', 'ovR', '#gguw .thcR'),
    ('tnum', '숫자 목록 창(트리거)', 'tnum', '#gguw'),
    ('cnum', '숫자 목록 창(공식)', 'cnum', '#gguw'),
    ('cq', '이은 개념 창', 'cq', '#gguw'),
    ('concept', '개념 창', 'concept', '#sh-concept'),
    ('pins', '비교 창 셋 쌓임', 'pins', '.vpin'),
    ('af', '정답 정정 창', 'af', '#g3Af'),
    ('cm', '댓 칸', 'cm', '#view .g3cmb'),
    ('del', '빼기 확인', 'del', '#g7del'),
    ('ed', '고치기 칸', 'ed', '#view .g3ed'),
]
G7_OPEN = {
    'pop': G2_OPEN['pop'][1],
    'tip': G2_OPEN['pop'][1],   # 열고 나서 g7() 이 공식 줄(.g3pc)을 진짜로 누름
    'ty': G3_WIN[1][2],
    'block': G2_OPEN['gguw'][1],
    'ovL': r"""(async()=>{const o=await (%s);if(o!==true)return o;const s=document.getElementById('gguw');if(!s.__g3cwOpen)return '덮개 없음';s.__g3cwOpen('L');await new Promise(r=>setTimeout(r,700));return s.classList.contains('thcOnL')})()""" % G2_OPEN['gguw'][1],
    'ovR': r"""(async()=>{const o=await (%s);if(o!==true)return o;const s=document.getElementById('gguw');if(!s.__g3cwOpen)return '덮개 없음';s.__g3cwOpen('R');await new Promise(r=>setTimeout(r,700));return s.classList.contains('thcOnR')})()""" % G2_OPEN['gguw'][1],
    'tnum': G3_WIN[3][2],
    'cnum': G3_WIN[4][2],
    'cq': G3_WIN[5][2],
    'concept': G2_OPEN['concept'][1],
    'pins': r"""(async()=>{for(const n of [64,13,71]){await vSwapOpen(n);await new Promise(r=>setTimeout(r,3000))}return document.querySelectorAll('.vpin').length>=3})()""",
    'af': G3_WIN[9][2],
    'cm': r"""(async()=>{const e=document.querySelector('#view .g3list .g3r[data-f="t"] .g3cm');if(!e)return '댓 없음';e.click();await new Promise(r=>setTimeout(r,700));return !!document.querySelector('#view .g3cmb')})()""",
    'del': G3_WIN[10][2],
    'ed': r"""(async()=>{const r=document.querySelector('#view .g3list .g3r[data-f="t"] .g3tx');if(!r)return '트리거 줄 없음';const b=r.getBoundingClientRect();
            r.dispatchEvent(new PointerEvent('pointerdown',{clientX:b.left+5,clientY:b.top+5,button:0,bubbles:true,pointerId:7}));await new Promise(x=>setTimeout(x,800));
            r.dispatchEvent(new PointerEvent('pointerup',{clientX:b.left+5,clientY:b.top+5,button:0,bubbles:true,pointerId:7}));await new Promise(x=>setTimeout(x,300));return !!document.querySelector('#view .g3ed')})()""",
}


BASE_SAME = {}
STAGE_X = r"""(()=>{const s=document.getElementById('stage');return s?{sw:s.scrollWidth,cw:s.clientWidth}:null})()"""


def g7(br):
    # 본창 #stage 가로 굴림(쪽 그림 판 + 여백 · 세로 굴림막대 폭만큼) — 바탕에서도 같은지 먼저 잼 · 같으면 그 한 줄은 INFO
    for devk in ('PC', '폰', '아이패드'):
        (size, touch) = DEVS[devk]
        q = dev(br, 'BASE', size, touch)
        try:
            tools(q)
            q.ev(G3_PREP.replace('__FOLD__', 'true' if devk == '폰' else 'false'))
            q.wait(1200)
            st = q.ev(STAGE_X)
            if st and st['sw'] > st['cw'] + 1:
                BASE_SAME[devk] = {'hscroll:div#stage': '바탕 cab7b5a 도 #stage %d > %d(+%d)' % (st['sw'], st['cw'], st['sw'] - st['cw'])}
        finally:
            q.close()
    for devk in ('PC', '폰', '아이패드'):
        (size, touch) = DEVS[devk]
        t1 = time.time()
        p = dev(br, 'NEW', size, touch)
        try:
            tools(p)
            fold = 'true' if devk == '폰' else 'false'
            p.ev(G3_PREP.replace('__FOLD__', fold))
            # 근거 한 줄 씨앗(시안 setup 꼴 — 65 · 66 에 블록 588c90 · 트리거 하나)
            p.ev(r"""(async()=>{const b=G3.blocks().find(x=>x.key==='U:^588c90');if(b){await G3.push('P065','c',{t:b.text,ref:b.key})}
              if(!ggOf('P065').some(g=>g&&(g.f||'t')==='t'))await G3.push('P065','t',{t:'훑기 트리거'});await openView(65,navList());await new Promise(r=>setTimeout(r,2000))})()""")
            for k, nm, ok_key, sel in G7_WIN:
                p.ev(G2_CLOSE)
                p.ev("(async()=>{document.querySelectorAll('#view .g3cmb').forEach(x=>x.remove());if(VNO!==65){await openView(65,navList());await new Promise(r=>setTimeout(r,2000))}})()")
                if devk == '폰' and k in ('pop', 'tip'):
                    p.ev('ndResFold(false)')
                    p.wait(900)
                elif devk == '폰':
                    p.ev('ndResFold(true)')
                    p.wait(400)
                o = p.ev(G7_OPEN[ok_key]) if ok_key else True
                if k == 'tip' and o is True:
                    a = p.ev("(()=>{const e=document.querySelector('#g3Pop .g3pc');return e?__H.hit(e):null})()")
                    if a and a.get('on'):
                        press(p, a['cx'], a['cy'], touch)
                        p.wait(800)
                    o = p.ev("!!document.querySelector('#g3Pop .g3ptip')") or {'공식 줄': a}
                if k == 'del' and o is True:
                    p.ev("(()=>{const s=[...document.querySelectorAll('.sheet')].find(s=>/이은 개념 빼기/.test(s.textContent));if(s)s.id='g7del'})()")
                p.wait(500)
                e0 = len(errs(p))
                sw = p.ev("([s,t])=>__H.sweep(s,t)", [sel, touch]) if o is True else None
                x = p.ev(SWEEP_X, sel) if o is True else None
                p.shot('g7_%s_%s' % (devk, k))
                bad = [q for q in (sw or []) if q.startswith(('page-hscroll', 'hscroll', 'clip', 'offscreen'))]
                pre = [q for q in bad if q in BASE_SAME.get(devk, ())]   # 바탕 cab7b5a 도 같은 자리 · 같은 꼴(이 판 탓 아님 · INFO)
                bad = [q for q in bad if q not in pre]
                info = [q for q in (sw or []) if q.startswith(('overlap', 'small'))]
                ok = bool(o is True and x and not x.get('noroot') and not bad and not x['cov'] and not x['raw'] and not x['rootOff'])
                R('G7', '%s-%s' % (devk, k), '%s %s — 넘침 · 잘림 · 화면 밖 · 가려진 누름 · 날 글자 0' % (devk, nm), ok, None,
                  {'열기': o, '넘침/잘림/밖': bad[:6], '가려진 누름': (x or {}).get('cov'), '날 글자': (x or {}).get('raw'), '창 밖': (x or {}).get('rootOff'), '창': (x or {}).get('box'),
                   'INFO 겹침·작은 누름': info[:6], 'INFO 바탕도 같음': pre and {q: BASE_SAME[devk][q] for q in pre}}, yard=False)
                if k == 'del':
                    p.ev("(()=>{const s=document.getElementById('g7del');if(s)s.remove()})()")
                if k == 'ed':
                    p.pg.keyboard.press('Escape')
                    p.wait(300)
            R('G7', '%s-오류' % devk, '%s 창 열일곱 여는 동안 페이지 오류 0' % devk, not errs(p), None, errs(p)[:5], yard=False)
        finally:
            p.close()
        print('  G7 %s %.0fs' % (devk, time.time() - t1), flush=True)


# ═══ 차례 ═══
def main():
    os.makedirs(TMPD, exist_ok=True)
    R('G0', '판', '판 · 자리', None, None, {'NEW': NEWF, 'md5(LF)': MD5, 'BASE': BASE, 'SPD': SPD, 'vendor': VENDOR, 'notes': NOTES,
                                             '시험': len(TESTS['tests']), '패치': len(PATCHES)})
    if MD5['BASE'] != '48330c0f4a4e3e503d1cf1f67de75545':
        print('⚠ 바탕 md5 가 지시서(48330c0f)와 다르다: ' + MD5['BASE'])
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for g, fn in (('G1', g1), ('G1R', g1r), ('G2', g2), ('G3', g3), ('G5', g5), ('G6', g6), ('G7', g7)):
            if not want(g):
                continue
            t1 = time.time()
            try:
                fn(br)
            except Exception as e:
                R(g, '하네스', '관문 하네스 오류', False, None, traceback.format_exc()[-800:], yard=False)
            STEP[g] = round((time.time() - t1) / 60, 1)
            print('── %s %.1f 분' % (g, STEP[g]), flush=True)
        br.close()
    np_ = sum(1 for r in RES if r['new'] is True)
    nf = [r for r in RES if r['new'] is False]
    yard = [r for r in RES if r['yard'] and r['base'] is not None and r['new'] is not None]
    ycut = sum(1 for r in yard if r['base'] is False)
    ysame = [r['g'] + ' ' + r['id'] for r in yard if r['base'] is True]
    summ = {'PASS': np_, 'FAIL': len(nf), 'FAIL 칸': [r['g'] + ' ' + r['id'] for r in nf], '헛잣대(바탕 FAIL)': '%d/%d' % (ycut, len(yard)),
            '바탕도 같음': ysame, '단계(분)': STEP, '전체(분)': round((time.time() - T0) / 60, 1)}
    R('합계', '합계', '합계', None, None, summ)
    try:
        with open(OUTF, 'w', encoding='utf-8') as f:
            for r in RES:
                f.write(json.dumps(r, ensure_ascii=False, default=str) + '\n')
    except Exception:
        pass
    sys.exit(1 if nf else 0)


if __name__ == '__main__':
    main()
