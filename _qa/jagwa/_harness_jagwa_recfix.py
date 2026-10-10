# -*- coding: utf-8 -*-
r"""_task_jagwa_recfix_1010 §B 관문 [클라우드] — 자과 물리 회독 기록: 지운 기록 되살아남 · 남는 「N회독」 줄 · OMR 뒤 마크 둘 · 창 머리 번호 · 시계 끌기

  python _harness_jagwa_recfix.py [--new <앱>] [--base <판 = df8402a | 6a1580d>] [--eng chromium,webkit] [--only R1,R2,R3,R4,R5,S]
                                  [--spd <studyplandata>] [--notes <notes>] [--vendor <cdnjs 사본>] [--res <결과>]

  NEW = genie 작업트리 jagwa/index.html · BASE = 바탕 main df8402a(헛잣대 — 새 칸은 바탕 FAIL · 「옛 그대로」 칸은 바탕도 같음)
        · --base 6a1580d(_task_jagwa_nospace_1011 헛잣대 = 물리 스페이스를 되살린 판) = 새 칸은 R5e 하나 · 나머지는 그 판에 이미 있어 「바탕도 같음」
  엔진 = Chromium · WebKit(새 판 · 바탕 둘 다) · PC 1100×800 마우스 · 폰 384×844 hasTouch(Chromium = CDP 손가락 · WebKit = 시계에 합성 touch 포인터 — 손가락 포인터는 그 요소에 붙잡힘)
  데이터 = studyplandata 현행 route 사본(JG) · 원격 = 가짜 GitHub(메모리 · PUT 밖으로 안 나감) · 시험 기록 = 기록 없는 물리 문항에 지어낸 회독(개인 기록 값은 출력에 안 옮김 · D11)
  관문:
    R1 기록 창 머리 = 「번 회독」 글자 0 · 「지난 필기 같이」 · ✕ 있음
    R2 지움 이김 — 기록 3 을 동기화(원격 = 같은 3 · 도장 = 셋째 시각) → 기록 창에서 R2a 셋째 ✕ · R2b 가운데 ✕ · R2c 마크 X→O → 동기화 → 앱 · 보낸 data = 바뀐 것 · 보낸 도장 > 셋째 시각
       → 원격을 옛 3 으로 되돌리고 다시 동기화해도 그대로 · R2d 다 지움 = 묘비(옛 그대로 · 바탕도 같음)
    R3 빈 층 — 기록 2 · 층 0~2(층 1 · 2 빈) → 둘째 ✕ → 창 다시 열기 = 빈 「N회독」 줄 0 · #tLayer 빈 층 0(지금 층 빼고) · R3b 층 1 에 획이 있으면 그 줄 남음 · 획 그대로
    R4 OMR 뒤 마크 — 물리 문항 OMR 고름 → △ = 기록 +1 만(마지막 = Q · 고른 답 그대로) → 다시 열어 △ = +1 · R4b 카드 층(지학) 자동 마크 → 마크 = 하나(옛 그대로)
    R5 시계 — R5a PC 마우스 가던 시계 누른 채 40px 밖으로 끌어 밖에서 뗌(0.3 초) · R5b 1 초 → 0:00 아님 · 가던 채 · 다음 시계 톡(마우스 click) = 멈춤 · 또 톡 = 계속
            R5c 폰 손가락 같은 몸짓(0.3 초 · 1 초 · 톡 = 손가락 톡) · R5d 제자리 길게 0.8 초 = 0:00(ansz 그대로 · 바탕도 같음)
            R5e 물리 문항 창 스페이스 = 시계 그대로(가던 · 멈춘 둘 다 · 포커스 뗀 뒤 = 앱 단축키 길) — 사용자 9/20 「문항 화면 단축키는 일부러 죽임」(_task_jagwa_nospace_1011)
            R5x 참고(판정 밖) — 시계를 마우스로 누른 뒤(그 단추에 포커스) 스페이스 = 브라우저 기본 단추 누름이 멈춤/계속을 바꾸나
    S 겉 무변 — 기록 있는 문항(1번)의 기록 창(문항 창 밖에서 엶) 줄 수 · 마크 · 시간 글 = 바탕(실제 기록이라 줄 수 + md5 지문만 적음 · D11)
  모드 — gate = 바탕 띄움 · regress · smoke = 새 판만(S = 기준 스냅샷 · smoke = R5)
"""
import os as _os_r, sys as _sys_r   # env_lanes — _roots.py 를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402,F401 — --mode · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음
import _qa_jagwa_common as JG   # noqa: E402
import hashlib, json, os, sys, tempfile, time, traceback   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEWF = ARG('--new', _roots.genie('jagwa', 'index.html'))
BASE = ARG('--base', 'df8402a')
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
TMPD = os.path.join(tempfile.gettempdir(), 'h_jagwa_recfix')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_jagwa_recfix_result.txt'))
SPD = ARG('--spd', _roots.spd())
NOTES = ARG('--notes', os.path.join(os.path.dirname(_roots.spd()), 'notes'))
VENDOR = ARG('--vendor', os.path.join(TMPD, 'vendor'))
JG.conf(VENDOR_PP=VENDOR, SPD_PP=SPD, NOTES=NOTES, SHOTS=os.path.join(TMPD, 'shots'))
GATE = QC.GATE
if GATE:
    QC.sub('git:show-app')
SRC = {'NEW': JG.app_src(NEWF)}
if GATE:
    SRC['BASE'] = JG.app_src(BASE)
PC, PH = (1100, 800), (384, 844)
RKEY = 'zzikkaplan/studyplandata:phys/기록.json'
RES = []


def want(g):
    return (not ONLY or g in ONLY) and (not QC.SMOKE or g == 'R5')


def _s(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


def R(g, name, new, base=None, d='', yard=True):
    RES.append(dict(g=g, name=name, new=new, base=base, yard=yard, d=d))
    tag = 'INFO' if new is None else ('PASS' if new else 'FAIL')
    yb = '' if base is None else (' · 바탕 ' + (('PASS(바탕도 같음)' if not yard else 'PASS') if base else 'FAIL'))
    print('%s | %s · %s%s | %s' % (tag, g, name, yb, _s(d)[:700]), flush=True)


# ── JS ───────────────────────────────────────────────────────────────────────────────────────
PICK_JS = r"""(n)=>{const out=[];for(const r of DATA){const no=r[F.NO];if(hist(no).length)continue;if(!ansOf(no).length)continue;out.push(no);if(out.length>=n)break}return out}"""
SEED_JS = r"""async ([no,ms])=>{const t0=Date.now()-3600000;const h=ms.map((m,i)=>({m,t:t0+i*60000,s:20+i*5}));ST[qk(no)]={h};await saveST();return {k:qk(no),t:h.map(x=>x.t)}}"""
SYNC_JS = r"""async ()=>{try{await syncRecords(true)}catch(e){return 'ERR '+e}await new Promise(r=>setTimeout(r,300));return recErr||'ok'}"""
HIST_JS = r"""(no)=>hist(no).map(x=>({m:x.m,a:x.a||null,s:x.s||0,auto:!!x.auto}))"""
SHEET_JS = r"""()=>{const b=document.getElementById('hsPop');if(!b)return null;const head=b.querySelector('.erh');
  return {head:head?head.textContent:'',eye:!!b.querySelector('#hsEye'),x:!!b.querySelector('#hsX'),
    rows:[...b.querySelectorAll('.hsr')].map(r=>{const on=r.querySelector('.hsm button.on');return {i:+r.dataset.i,n:(r.querySelector('.hsn')||{}).textContent,rec:!!r.querySelector('.hsm'),
      m:on?on.dataset.m:null,sec:(r.querySelector('.sec')||{}).textContent||'',now:!!r.querySelector('.hsnow')}})}}"""
OPEN_SHEET = r"""(no)=>{const o=document.getElementById('hsPop');if(o&&o.__close)o.__close();histSheet(no);return !!document.getElementById('hsPop')}"""
CLOSE_SHEET = r"""()=>{const o=document.getElementById('hsPop');if(o&&o.__close)o.__close();return !document.getElementById('hsPop')}"""
ROW_BTN = r"""([i,sel])=>{const b=document.getElementById('hsPop');const r=b&&b.querySelector('.hsr[data-i="'+i+'"]');const e=r&&r.querySelector(sel);if(!e)return null;
  e.scrollIntoView({block:'center'});const q=e.getBoundingClientRect();return {on:true,cx:q.left+q.width/2,cy:q.top+q.height/2}}"""
LAYER_JS = r"""()=>({opts:[...document.querySelectorAll('#tLayer option')].map(o=>+o.value),cur:LAYER,n:LAYERS,ink:Object.keys(INK).map(Number).sort((a,b)=>a-b).map(L=>[L,(INK[L]||[]).length])})"""
TM_JS = r"""()=>{const t=document.getElementById('tm'),r=t.getBoundingClientRect();return {txt:t.textContent,run:!!TM.iv,sec:TM.sec,cx:r.left+r.width/2,cy:r.top+r.height/2,w:r.width,h:r.height}}"""
TM_TOUCH = r"""([ty,x,y])=>{const t=document.getElementById('tm');   // 손가락 포인터 = 누른 요소에 붙잡힘(암묵 capture) — 합성 이벤트도 그 요소로
  t.dispatchEvent(new PointerEvent(ty,{bubbles:true,cancelable:true,composed:true,pointerId:9,pointerType:'touch',isPrimary:true,clientX:x,clientY:y,button:0,buttons:ty==='pointerup'?0:1}));return true}"""


TM_PHASE = r"""(()=>{tmStop();tmRun();return TM.sec})()"""   # 가던 시계 1 초 틱 자리를 지금으로 — 초는 그대로(멈춤 → 계속)


def close_all(p):
    p.ev("(()=>{const o=document.getElementById('hsPop');if(o&&o.__close)o.__close();document.querySelectorAll('.sheet:not(.hide)').forEach(s=>{if(s.id!=='book'&&s.id!=='bkq')s.remove()})})()")
    p.wait(150)


def open_q(p, no):
    p.ev("(no)=>openView(no)", no)
    p.wait(1500)


def rrec(rem, k):
    """원격(가짜) 기록 — 그 칸 h 수 · 도장"""
    b = rem.files.get(RKEY)
    if not b:
        return None
    d = json.loads(b.decode('utf-8'))
    k = str(k)   # 물리 qk = 번호(수) — JSON 열쇠는 글자
    st = ((d.get('data') or {}).get('status') or {}).get(k)
    return {'n': len((st or {}).get('h') or []) if st else 0, 'm': [x.get('m') for x in (st or {}).get('h') or []] if st else [],
            'u': (d.get('u') or {}).get('status|' + k), 'gone': (d.get('gone') or {}).get('status|' + k)}


def r2_one(p, rem, no, kind):
    """R2 한 갈래 — kind: last(셋째 ✕) · mid(가운데 ✕) · mark(둘째 X→O) · all(셋 다 ✕)"""
    o = {'kind': kind}
    sd = p.ev(SEED_JS, [no, ['O', 'X', 'Q']])
    k, ts = sd['k'], sd['t']
    o['sync1'] = p.ev(SYNC_JS)
    r1 = rrec(rem, k)
    o['원격 1'] = r1 and {'n': r1['n'], 'u=셋째': r1['u'] == ts[2]}
    snap = rem.files.get(RKEY)
    open_q(p, no)
    p.ev(OPEN_SHEET, no); p.wait(300)
    if kind == 'last':
        p.press(p.ev(ROW_BTN, [2, '.rm']), wait=600)
    elif kind == 'mid':
        p.press(p.ev(ROW_BTN, [1, '.rm']), wait=600)
    elif kind == 'mark':
        p.press(p.ev(ROW_BTN, [1, '.hsm button[data-m="O"]']), wait=600)
    else:
        for _ in range(3):
            p.press(p.ev(ROW_BTN, [0, '.rm']), wait=500)
    o['고친 뒤 앱'] = [x['m'] for x in p.ev(HIST_JS, no)]
    p.ev(CLOSE_SHEET)
    o['sync2'] = p.ev(SYNC_JS)
    o['동기화 뒤 앱'] = [x['m'] for x in p.ev(HIST_JS, no)]
    r2 = rrec(rem, k)
    o['보냄'] = r2 and {'n': r2['n'], 'm': r2['m'], '도장 > 셋째': (r2['u'] or 0) > ts[2], '묘비': bool(r2['gone'])}
    if snap is not None:   # 원격을 옛 3 그대로(다른 기기 · 늦은 원격)로 되돌리고 다시
        with rem.lock:
            rem.files[RKEY] = snap
    o['sync3'] = p.ev(SYNC_JS)
    o['옛 원격 뒤 앱'] = [x['m'] for x in p.ev(HIST_JS, no)]
    return o


def r3_one(p, no, strokes1):
    open_q(p, no)
    p.ev(SEED_JS, [no, ['O', 'X']])
    p.ev("""(s1)=>{const st={c:'#d33',w:2,p:[0.2,0.2,0.3,0.3,0.4,0.35]};INK={0:[st],1:s1?[Object.assign({},st,{p:[0.5,0.5,0.6,0.6]})]:[],2:[]};LAYERS=3;LAYER=2;
      fillLayerSel();paintInk();saveInk();return true}""", strokes1)
    p.wait(500)
    p.ev(OPEN_SHEET, no); p.wait(300)
    before = p.ev(SHEET_JS)
    p.press(p.ev(ROW_BTN, [1, '.rm']), wait=900)
    p.ev(CLOSE_SHEET); p.wait(200)
    p.ev(OPEN_SHEET, no); p.wait(300)
    after = p.ev(SHEET_JS)
    p.ev(CLOSE_SHEET)
    lay = p.ev(LAYER_JS)
    return {'전 줄': [(r['n'], r['rec']) for r in (before or {}).get('rows', [])], '뒤 줄': [(r['n'], r['rec']) for r in (after or {}).get('rows', [])],
            '기록': [x['m'] for x in p.ev(HIST_JS, no)], '층': lay}


def run(br, eng, ver):
    o = {'ver': ver, 'eng': eng}
    src = SRC[ver]
    QC.launch('base' if ver == 'BASE' else 'new')
    rem = JG.Remote()
    p = JG.Pg_PP(br, eng, 'recfix-%s-%s-pc' % (ver, eng), src, 'phys', PC, touch=False, remote=rem)
    try:
        picks = p.ev(PICK_JS, 8)
        o['문항(기록 없음 · 채점 됨)'] = len(picks)
        if want('R1'):
            open_q(p, picks[0])
            p.ev(OPEN_SHEET, picks[0]); p.wait(300)
            o['R1'] = p.ev(SHEET_JS)
            p.ev(CLOSE_SHEET)
        if want('R2'):
            o['R2'] = {kind: r2_one(p, rem, picks[i], kind) for i, kind in enumerate(('last', 'mid', 'mark', 'all'), start=1)}
            close_all(p)
        if want('R3'):
            o['R3'] = {'빈': r3_one(p, picks[5], False), '획': r3_one(p, picks[6], True)}
            close_all(p)
        if want('R4'):
            no = picks[7]
            open_q(p, no)
            ch = p.ev("(no)=>ansOf(no)[0]", no)
            pick = '③' if ch != '③' else '②'   # 틀린 답이든 맞은 답이든 — 고른 답 a 가 남는지
            a = p.ev("(c)=>{const b=document.querySelector('#omrPad [data-omr=\"'+c+'\"]');if(!b)return null;b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return {on:true,cx:r.left+r.width/2,cy:r.top+r.height/2}}", pick)
            if not p.press(a, wait=600):
                p.ev("(c)=>omrPick(c)", pick); p.wait(600)
            h1 = p.ev(HIST_JS, no)
            q = p.ev("(()=>{const b=document.getElementById('mQ');if(!b)return null;b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return {on:true,cx:r.left+r.width/2,cy:r.top+r.height/2}})()")
            if not p.press(q, wait=600):
                p.ev("(()=>mark('Q'))()"); p.wait(600)
            h2 = p.ev(HIST_JS, no)
            p.ev("(()=>{try{closeView()}catch(e){}})()"); p.wait(400)
            open_q(p, no)
            p.ev("(()=>mark('Q'))()"); p.wait(600)
            h3 = p.ev(HIST_JS, no)
            o['R4'] = {'고른 답': pick, 'OMR 뒤': h1, '△ 뒤': h2, '다시 열어 △ 뒤': h3}
            close_all(p)
        if want('R5'):
            o['R5pc'] = clock_pc(p)
        if want('S'):
            p.ev("(()=>{try{closeView()}catch(e){}})()"); p.wait(400)
            p.ev(OPEN_SHEET, 1); p.wait(300)
            sh = p.ev(SHEET_JS)
            p.ev(CLOSE_SHEET)
            rows = [(r['n'], r['m'], r['sec']) for r in (sh or {}).get('rows', [])]
            o['S'] = {'줄': len(rows), 'md5': hashlib.md5(json.dumps(rows, ensure_ascii=False).encode('utf-8')).hexdigest()[:8]} if rows else None   # D11 — 실제 기록 값(마크 · 시간)은 안 옮김 · 줄 수 + 지문만
        o['오류'] = (p.errs or []) + (p.ev('window.__err||[]') or [])
    finally:
        p.close()
    if want('R4'):   # R4b 카드 층(지학) 자동 마크 → 마크 = 하나(옛 그대로)
        e = JG.Pg_PP(br, eng, 'recfix-%s-%s-earth' % (ver, eng), src, 'earth', PC, touch=False, remote=JG.Remote())
        try:
            no = e.ev("(()=>{for(const r of DATA){const no=r[F.NO];if(!hist(no).length&&r[F.ANS])return no}return null})()")
            e.ev("(no)=>openView(no)", no); e.wait(1800)
            e.ev("(()=>{const r=rec(VNO);return pickChoice(String(r[F.ANS]))})()"); e.wait(600)
            h1 = e.ev(HIST_JS, no)
            e.ev("(()=>mark('Q'))()"); e.wait(600)
            o['R4b'] = {'자동 마크 뒤': h1, '△ 뒤': e.ev(HIST_JS, no)}
        except Exception as ex:
            o['R4b'] = {'오류': str(ex)[:200]}
        finally:
            e.close()
    if want('R5'):   # R5c 폰 손가락
        q = JG.Pg_PP(br, eng, 'recfix-%s-%s-ph' % (ver, eng), src, 'phys', PH, touch=True, remote=JG.Remote())
        try:
            o['R5ph'] = clock_ph(q, eng)
        finally:
            q.close()
    return o


def clock_state(p, touch=False):
    """뗀 뒤 상태 → 다음 시계 톡(PC = 마우스 click · 폰 = 손가락 톡) = 멈춤 · 또 톡 = 계속 — nospace(10/11): 스페이스는 일부러 죽인 단축키라 톡으로 잼"""
    s0 = p.ev(TM_JS)
    tap = (lambda: p.tap(s0['cx'], s0['cy'], wait=450)) if touch else (lambda: p.click(s0['cx'], s0['cy'], wait=450))
    tap()
    s1 = p.ev(TM_JS)
    tap()
    s2 = p.ev(TM_JS)
    return {'뗀 뒤': [s0['txt'], s0['run'], s0['sec']], '톡': s1['run'], '또 톡': s2['run']}


def space_state(p):
    """R5e — 포커스 뗀 뒤 스페이스: 가던 시계 · 멈춘 시계(톡으로 멈춤) 둘 다 그대로여야 · R5x 참고 = 시계를 누른 채 포커스 둔 뒤 스페이스"""
    blur = "(()=>{const a=document.activeElement;if(a&&a.blur)a.blur()})()"
    p.ev("(()=>{if(!TM.iv)tmRun()})()"); p.wait(1300)
    p.ev(blur)
    a0 = p.ev(TM_JS); p.pg.keyboard.press('Space'); p.wait(450); a1 = p.ev(TM_JS)
    p.click(a1['cx'], a1['cy'], wait=450)
    p.ev(blur)
    b0 = p.ev(TM_JS); p.pg.keyboard.press('Space'); p.wait(450); b1 = p.ev(TM_JS)
    p.click(b1['cx'], b1['cy'], wait=450)                       # 다시 계속(톡) — 이때 시계 단추에 포커스가 남음(엔진마다)
    x0 = p.ev(TM_JS); f = p.ev("(()=>document.activeElement&&document.activeElement.id||'')()")
    p.pg.keyboard.press('Space'); p.wait(450); x1 = p.ev(TM_JS)
    p.ev(blur)
    p.ev("(()=>{if(!TM.iv)tmRun()})()")
    return {'가던': [a0['run'], a1['run']], '멈춘': [b0['run'], b1['run']], '포커스 뒤(참고)': {'포커스': f, '전': x0['run'], '스페이스 뒤': x1['run']}}


def clock_pc(p):
    out = {}
    open_q(p, 1)
    for hold in (0.3, 1.0):
        p.ev("(()=>{if(!TM.iv)tmRun()})()"); p.wait(2300)
        t0 = p.ev(TM_JS)
        p.pg.mouse.move(t0['cx'], t0['cy']); p.pg.mouse.down()
        for i in range(1, 6):
            p.pg.mouse.move(t0['cx'], t0['cy'] + 8 * i); p.wait(20)
        p.wait(max(0, int(hold * 1000) - 100))
        p.pg.mouse.up(); p.wait(700)
        out['%.1f' % hold] = dict(clock_state(p), 전=[t0['txt'], t0['run'], t0['sec']])
    out['스페이스'] = space_state(p)
    p.ev("(()=>{if(!TM.iv)tmRun()})()"); p.wait(2300)
    p.ev(TM_PHASE); p.wait(1600)   # 1 초 틱 자리를 다시 맞춤 — 누름(0.55 초에 0:00) ~ 읽기(뗀 뒤) 사이에 틱이 끼면 0:01 로 읽힘(앱 무관 · 잼 자리)
    t0 = p.ev(TM_JS)
    p.pg.mouse.move(t0['cx'], t0['cy']); p.pg.mouse.down(); p.wait(800); p.pg.mouse.up(); p.wait(60)
    t1 = p.ev(TM_JS); p.wait(1100); t2 = p.ev(TM_JS)
    out['제자리 0.8'] = {'전': [t0['txt'], t0['run']], '뗀 직후': [t1['txt'], t1['run']], '1.1 초 뒤': [t2['txt'], t2['run']]}
    return out


def clock_ph(q, eng):
    out = {}
    open_q(q, 1)
    for hold in (0.3, 1.0):
        q.ev("(()=>{if(!TM.iv)tmRun()})()"); q.wait(2300)
        t0 = q.ev(TM_JS)
        x, y = t0['cx'], t0['cy']
        if eng != 'webkit':
            c = q._cdp()
            c.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'radiusX': 6, 'radiusY': 6, 'id': 1}]})
            for i in range(1, 6):
                c.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x, 'y': y + 8 * i, 'radiusX': 6, 'radiusY': 6, 'id': 1}]}); q.wait(20)
            q.wait(max(0, int(hold * 1000) - 100))
            c.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        else:
            q.ev(TM_TOUCH, ['pointerdown', x, y])
            for i in range(1, 6):
                q.ev(TM_TOUCH, ['pointermove', x, y + 8 * i]); q.wait(20)
            q.wait(max(0, int(hold * 1000) - 100))
            q.ev(TM_TOUCH, ['pointerup', x, y + 40])
        q.wait(700)
        out['%.1f' % hold] = dict(clock_state(q, touch=True), 전=[t0['txt'], t0['run'], t0['sec']])
    q.ev("(()=>{if(!TM.iv)tmRun()})()"); q.wait(2300)
    q.ev(TM_PHASE); q.wait(1600)
    t0 = q.ev(TM_JS)
    q.long_press(t0['cx'], t0['cy'], ms=800, wait=60)
    t1 = q.ev(TM_JS); q.wait(1100); t2 = q.ev(TM_JS)
    out['제자리 0.8'] = {'전': [t0['txt'], t0['run']], '뗀 직후': [t1['txt'], t1['run']], '1.1 초 뒤': [t2['txt'], t2['run']]}
    return out


# ── 판정 ────────────────────────────────────────────────────────────────────────────────────
def j_clock(x):
    x = x or {}
    s = x.get('뗀 뒤') or [None, None, 0]
    pre = x.get('전') or [None, None, 0]
    # 0:00 으로 안 감 = 뗀 뒤 초 ≥ 끌기 전 초(옛 판은 끄는 동안 0:00 → 읽을 때 1 초 틱이 끼어 0:01 일 수 있어 「0:00 아님」 만으론 못 가름)
    return bool(x) and s[0] != '0:00' and (s[2] or 0) >= (pre[2] if len(pre) > 2 and pre[2] is not None else 0) and s[1] is True and x.get('톡') is False and x.get('또 톡') is True


def judge(o, base_s):
    if not o or '하네스 오류' in o:
        return {}
    r = {}
    if want('R1'):
        h = o.get('R1') or {}
        r['R1'] = (bool(h) and '번 회독' not in h.get('head', '') and '지난 필기 같이' in h.get('head', '') and h.get('eye') and h.get('x'),
                   {'머리': h.get('head', '').replace('지난 필기 같이', '「지난 필기 같이」').strip()[:60], '✕': h.get('x')})
    if want('R2'):
        R2 = o.get('R2') or {}
        want_m = {'last': ['O', 'X'], 'mid': ['O', 'Q'], 'mark': ['O', 'O', 'Q'], 'all': []}
        for kind, c in (('last', 'R2a'), ('mid', 'R2b'), ('mark', 'R2c'), ('all', 'R2d')):
            x = R2.get(kind) or {}
            sent = x.get('보냄') or {}
            ok = (x.get('고친 뒤 앱') == want_m[kind] and x.get('동기화 뒤 앱') == want_m[kind] and x.get('옛 원격 뒤 앱') == want_m[kind]
                  and (x.get('원격 1') or {}).get('n') == 3 and (x.get('원격 1') or {}).get('u=셋째'))
            if kind == 'all':
                ok = ok and sent.get('n') == 0 and sent.get('묘비')
            else:
                ok = ok and sent.get('n') == len(want_m[kind]) and sent.get('m') == want_m[kind] and sent.get('도장 > 셋째')
            r[c] = (ok, {'원격 처음': x.get('원격 1'), '고친 뒤': x.get('고친 뒤 앱'), '동기화 뒤': x.get('동기화 뒤 앱'), '보냄': sent, '옛 원격 다시 뒤': x.get('옛 원격 뒤 앱'),
                         'sync': [x.get('sync1'), x.get('sync2'), x.get('sync3')]})
    if want('R3'):
        R3 = o.get('R3') or {}
        a, b = R3.get('빈') or {}, R3.get('획') or {}
        la, lb = a.get('층') or {}, b.get('층') or {}
        empty_opts = lambda L: [v for v in (L.get('opts') or []) if v != L.get('cur') and dict(L.get('ink') or []).get(v, 0) == 0]
        r['R3'] = (a.get('기록') == ['O'] and a.get('뒤 줄') == [('1회독', True)] and not empty_opts(la) and bool(la),
                   {'지우기 전 줄': a.get('전 줄'), '다시 연 줄': a.get('뒤 줄'), '층(번호 · 획)': la.get('ink'), '고르개': la.get('opts'), '지금 층': la.get('cur')})
        ink_b = dict(lb.get('ink') or [])
        r['R3b'] = (b.get('기록') == ['O'] and b.get('뒤 줄') == [('1회독', True), ('2회독', False)] and ink_b.get(1) == 1 and ink_b.get(0) == 1,
                    {'다시 연 줄': b.get('뒤 줄'), '층(번호 · 획)': lb.get('ink'), '고르개': lb.get('opts')})
    if want('R4'):
        x = o.get('R4') or {}
        h1, h2, h3 = x.get('OMR 뒤') or [], x.get('△ 뒤') or [], x.get('다시 열어 △ 뒤') or []
        r['R4'] = (len(h1) == 1 and h1[0].get('a') == x.get('고른 답') and len(h2) == 1 and h2[0]['m'] == 'Q' and h2[0].get('a') == x.get('고른 답') and len(h3) == 2 and h3[-1]['m'] == 'Q',
                   {'OMR 뒤': [(y['m'], y['a']) for y in h1], '△ 뒤': [(y['m'], y['a']) for y in h2], '다시 열어 △ 뒤': [(y['m'], y['a']) for y in h3]})
        y = o.get('R4b') or {}
        a1, a2 = y.get('자동 마크 뒤') or [], y.get('△ 뒤') or []
        r['R4b'] = (len(a1) == 1 and a1[0].get('auto') and len(a2) == 1 and a2[0]['m'] == 'Q' and not a2[0].get('auto'),
                    {'자동 마크 뒤': [(z['m'], z['auto']) for z in a1], '△ 뒤': [(z['m'], z['auto']) for z in a2], '오류': y.get('오류')})
    if want('R5'):
        pc, ph = o.get('R5pc') or {}, o.get('R5ph') or {}
        r['R5a'] = (j_clock(pc.get('0.3')), pc.get('0.3'))
        r['R5b'] = (j_clock(pc.get('1.0')), pc.get('1.0'))
        r['R5c'] = (j_clock(ph.get('0.3')) and j_clock(ph.get('1.0')), {'0.3': ph.get('0.3'), '1.0': ph.get('1.0')})
        lp = [pc.get('제자리 0.8') or {}, ph.get('제자리 0.8') or {}]
        r['R5d'] = (all(z.get('뗀 직후', [None])[0] == '0:00' and z.get('뗀 직후', [0, 0])[1] is True and (z.get('1.1 초 뒤') or [0, 0])[1] is True for z in lp),
                    {'PC': lp[0], '폰': lp[1]})
        sp = pc.get('스페이스') or {}
        r['R5e'] = (sp.get('가던') == [True, True] and sp.get('멈춘') == [False, False], {'가던(전 · 스페이스 뒤)': sp.get('가던'), '멈춘(전 · 스페이스 뒤)': sp.get('멈춘')})
    if want('S'):
        r['S'] = (bool(o.get('S')) and o.get('S') == base_s, {'새 판': o.get('S'), '바탕': base_s})
    return r


NAMES = {'R1': '기록 창 머리 = 「번 회독」 0 · 「지난 필기 같이」 · ✕', 'R2a': '셋째 ✕ → 동기화 = 앱 · 보낸 기록 2 · 도장 > 셋째 시각 · 옛 원격 다시 동기화해도 2',
         'R2b': '가운데 ✕ → 같음', 'R2c': '마크 X→O 바꿈 → 같음(바꾼 마크가 이김)', 'R2d': '다 지움 = 묘비(옛 그대로)',
         'R3': '둘째 ✕(층 1 · 2 빈) → 다시 연 기록 창 = 빈 「N회독」 줄 0 · #tLayer 빈 층 0(지금 층 빼고)', 'R3b': '층 1 에 획 → 그 줄 남음 · 획 그대로',
         'R4': '물리 OMR 고름 → △ = 기록 +1 만(마지막 Q · 고른 답 그대로) → 다시 열어 △ = +1', 'R4b': '카드 층(지학) 자동 마크 → △ = 하나(옛 그대로)',
         'R5a': 'PC 마우스 가던 시계 누른 채 40px 밖으로 끌어 밖에서 뗌 0.3 초 → 0:00 아님 · 가던 채 · 다음 시계 톡 멈춤 · 또 톡 계속',
         'R5b': 'PC 같은 몸짓 1 초 → 같음', 'R5c': '폰 손가락 같은 몸짓(0.3 초 · 1 초 · 손가락 톡) → 같음', 'R5d': '제자리 길게 0.8 초 = 0:00 · 가던 채(PC · 폰 · ansz 그대로)',
         'R5e': '물리 문항 창 스페이스 = 시계 그대로(가던 · 멈춘 둘 다 · 사용자 9/20 단축키 일부러 죽임)',
         'S': '기록 있는 문항(1번)의 기록 창 줄 수 · 마크 · 시간 글 = 바탕'}
INVAR = {'R2d', 'R4b', 'R5d', 'R5e', 'S'}   # 옛 그대로여야 하는 칸 — 헛잣대 셈 밖(R5c 는 아래에서 바탕 결과로 가름 · R5e = 6a1580d 앞 판은 스페이스가 안 먹음)
NEWC = {'6a1580d': {'R5e'}}   # 바탕마다 「새 칸」(바탕 FAIL 이어야) — nospace(10/11): 6a1580d = 물리 스페이스를 되살린 판 · 그 밖 칸은 그 판에 이미 있음


def is_inv(c, b):
    nc = next((v for k, v in NEWC.items() if BASE.startswith(k)), None)
    if nc is not None:
        return c not in nc
    return c in INVAR or (c == 'R5c' and b is not None and b[0])   # 손가락은 옛 판도 포인터가 붙잡혀 이미 됨 — 바탕도 같으면 「바탕도 같음」


def main():
    os.makedirs(TMPD, exist_ok=True)
    R('B0', '판 · 자리', None, None, {'NEW': NEWF, 'md5(LF)': {k: hashlib.md5(v.replace('\r\n', '\n').encode('utf-8')).hexdigest()[:8] for k, v in SRC.items()},
                                     'BASE': BASE if GATE else '(regress · smoke = 안 띄움)', '엔진': ENGS})
    res, t0 = {}, time.time()
    with sync_playwright() as pw:
        brs = {e: getattr(pw, e).launch() for e in ENGS}
        for ver, eng in [('NEW', e) for e in ENGS] + ([('BASE', e) for e in ENGS] if GATE else []):
            t1 = time.time()
            try:
                res[(ver, eng)] = run(brs[eng], eng, ver)
            except Exception as e:
                res[(ver, eng)] = {'하네스 오류': str(e)[:300], 'tb': traceback.format_exc()[-900:]}
            x = res[(ver, eng)]
            R('B0', '%s %s 돎' % (ver, eng), None, None, '%.1f 분 · %s' % ((time.time() - t1) / 60, (x.get('하네스 오류') + ' · ' + x.get('tb', '')[-500:]) if x.get('하네스 오류') else ('오류 %s' % _s(x.get('오류') or [])[:200])))
        for b in brs.values():
            b.close()
    BS = {}
    for eng in ENGS:
        if GATE:
            BS[eng] = (res.get(('BASE', eng)) or {}).get('S')
            QC.base('S@' + eng, BS[eng])
        else:
            BS[eng] = QC.base('S@' + eng, (res.get(('NEW', eng)) or {}).get('S'))
    for eng in ENGS:
        jn = judge(res.get(('NEW', eng)), BS.get(eng))
        jb = judge(res.get(('BASE', eng)), BS.get(eng)) if GATE else {}
        o = res.get(('NEW', eng)) or {}
        for c in NAMES:
            if not want(c[:2] if c[0] == 'R' else c):
                continue
            n = jn.get(c)
            if n is None:
                continue
            b = jb.get(c) if GATE else None
            inv = is_inv(c, b)
            R('%s[%s]' % (c, eng), NAMES[c], bool(n[0]), None if b is None else bool(b[0]),
              {'새 판': n[1], '바탕': b[1]} if b is not None else n[1], yard=not inv)
        if want('R5'):   # R5x 참고(판정 밖) — 시계 단추에 포커스가 남은 채 스페이스 = 브라우저 기본 단추 누름(앱 단축키 아님)
            gx = lambda v: (((res.get((v, eng)) or {}).get('R5pc') or {}).get('스페이스') or {}).get('포커스 뒤(참고)')
            R('R5x[%s]' % eng, '참고(판정 밖) — 시계를 마우스로 누른 뒤(그 단추 포커스) 스페이스 = 브라우저 기본 단추 누름', None, None,
              {'새 판': gx('NEW'), '바탕': gx('BASE')} if GATE else gx('NEW'))
    newp = [x for x in RES if x['new'] is not None]
    yard = [x for x in RES if x['base'] is not None and x['yard']]
    R('B9', '합 — 새 판 PASS %d · FAIL %d · 헛잣대(새 칸 바탕 FAIL) %d/%d · %.1f 분' % (
        sum(1 for x in newp if x['new']), sum(1 for x in newp if not x['new']), sum(1 for x in yard if not x['base']), len(yard), (time.time() - t0) / 60), None)
    with open(OUTF, 'w', encoding='utf-8') as f:
        for x in RES:
            tag = 'INFO' if x['new'] is None else ('PASS' if x['new'] else 'FAIL')
            yb = '' if x['base'] is None else (' · 바탕 ' + (('PASS(바탕도 같음)' if not x['yard'] else 'PASS') if x['base'] else 'FAIL'))
            f.write('%s | %s · %s%s | %s\n' % (tag, x['g'], x['name'], yb, _s(x['d'])[:700]))
    return 0 if all(x['new'] for x in newp) else 1


if __name__ == '__main__':
    sys.exit(main())
