# -*- coding: utf-8 -*-
r"""_task_jagwa_ansz_1010 §B 관문 [클라우드] — 자과 물리 답풀 그림 · 시계 0:00 · 서랍 걸린 시간 · 근거 개념 줄 고르기 (26 칸 · 시안 때 잰 식 그대로)

  python _harness_jagwa_ansz.py [--new <앱>] [--base <판 = 6f99850>] [--eng chromium,webkit] [--only A,C,D,G,S]
                                [--spd <studyplandata>] [--notes <notes>] [--vendor <cdnjs 사본>] [--res <결과>]

  NEW = genie 작업트리 jagwa/index.html · BASE = 바탕 main 6f99850(헛잣대 — 새 기능 칸은 바탕 FAIL · 「겉 무변」 칸은 바탕도 같음)
  엔진 = Chromium · WebKit(둘 다 · 바탕은 Chromium) · PC 1100×800 마우스 · 폰 384×844 hasTouch(Chromium = CDP 손가락 · WebKit = touchscreen.tap · 길게 · 두 손가락 = 합성 touch 포인터)
  데이터 = studyplandata 현행 route 사본(JG · 가짜 GitHub · PUT 은 메모리) · 볼트 = notes · cdnjs = --vendor 사본
  ⚠ 개인 기록 · 볼트 글을 출력에 옮기지 않는다(D11) — 출력 = 칸 · 수 · 자리 · 시각 · 판정 글자(「운동량 보존」 · 「탄성충돌」 있음/없음)만
  관문(26):
    A 답풀(13번 · 그림 1)  A1 PC 그림 누름 = 새 창 · 이동 0 · 창 그대로  A2 Ctrl+휠 위 두 번 = 폭 > 1.15 배 · 칸 안 굴림  A3 두 번 누름 = 처음 폭
                           A4 폰 그림 톡 = 이동 0  A5 폰 두 손가락 벌리기 = 그림만 > 1.5 배 · visualViewport.scale = 1
    C 시계  C1 PC 가던 시계 0.8 초 누름 = 0:00 부터 계속  C2 짧게 = 멈춤  C3 멈춘 시계 길게 = 0:00 멈춘 채  C4 누른 채 20px 끌기 = 안 바뀜(바탕도 같음)
            C5 스페이스 = 켜고 끄기 그대로(바탕도 같음)  C6 폰 손가락 0.8 초 = 0:00 부터 계속  C7 폰 톡 = 멈춤
    D 서랍(1번 줄)  D1 .ndm data-s = 기록 h[i].s(m:ss)  D2 ::after content = 그 값  D3 ::after 7px  D4 .ndm 글자 한 자  D5 줄 높이 바탕 + 2px 안
    G 근거(108번 PA2001 · 블록 U:^01ad5c 를 G3.push)  G1 넣은 직후 = 「(1) 탄성충돌」(옛 그대로)  G2 근거 줄 누름 = #gguw.g3sel · 고를 줄 ≥ 3
            G3 블록 둘째 · 셋째 줄 누름 = g.sl 2 · 근거 <br> 1 · 「운동량 보존」 있음 · 「탄성충돌」 없음(서랍 작은 창 g3Pop 도)  G4 다시 누름 = 뺌  G5 다 빼면 옛 그대로  G6 폰 손가락 G1~G5
    S 겉 무변  S1 이론 창(theorySheet) .thl 보이는 글 · 높이 = 바탕(data-bx 만 더해짐)  S2 개념 창(conceptSheet · 13번 · 줄 = .g3cql) 같음  S3 날 $ · <span 글자 0
  모드 — gate = 바탕 띄움 · regress · smoke = 새 판만(D5 · S1 · S2 = 기준 스냅샷)
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
BASE = ARG('--base', '6f99850')
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
TMPD = os.path.join(tempfile.gettempdir(), 'h_jagwa_ansz')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_jagwa_ansz_result.txt'))
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
QA_NO, QG_NO, QG_U, BLK = 13, 108, 'P108', 'U:^01ad5c'
RES = []


def want(g):
    return (not ONLY or g in ONLY) and (not QC.SMOKE or g == 'C')


def _s(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


def R(g, name, new, base=None, d='', yard=True):
    RES.append(dict(g=g, name=name, new=new, base=base, yard=yard, d=d))
    tag = 'INFO' if new is None else ('PASS' if new else 'FAIL')
    yb = '' if base is None else (' · 바탕 ' + (('PASS(바탕도 같음)' if not yard else 'PASS') if base else 'FAIL'))
    s = '%s | %s · %s%s | %s' % (tag, g, name, yb, _s(d)[:700])
    print(s, flush=True)


# ── 잼 JS ─────────────────────────────────────────────────────────────────────────────────────
IMG_JS = r"""(sc)=>{const s=[...document.querySelectorAll('.sheet')].pop(),im=s&&s.querySelector('img.solpic');if(!im)return null;if(sc)im.scrollIntoView({block:'center'});
  const r=im.getBoundingClientRect(),z=im.closest('.solz')||im.parentNode,pn=s.querySelector('.panel')||s;
  return {w:+r.width.toFixed(1),cx:r.left+Math.min(r.width,300)/2,cy:r.top+Math.min(r.height,200)/2,sheets:document.querySelectorAll('.sheet').length,
    url:location.href,a:!!im.closest('a'),boxSt:z.scrollTop,boxSl:z.scrollLeft,pnSt:pn.scrollTop,shSt:s.scrollTop,vv:visualViewport?visualViewport.scale:null}}"""
TM_JS = r"""()=>{const t=document.getElementById('tm'),r=t.getBoundingClientRect();return {txt:t.textContent,run:!!TM.iv,sec:TM.sec,cx:r.left+r.width/2,cy:r.top+r.height/2,w:r.width,h:r.height}}"""
ND_JS = r"""(no)=>{const row=document.querySelector('#ndList .ndrow[data-no="'+no+'"]');if(!row)return null;
  return {h:+row.getBoundingClientRect().height.toFixed(2),hist:hist(no).filter(x=>x&&x.m).map(x=>({m:x.m,s:tmFmt(+x.s||0),s0:+x.s||0})),
    m:[...row.querySelectorAll('.ndm')].map(b=>{const a=getComputedStyle(b,'::after');return {cls:b.className,tx:b.textContent,ds:b.getAttribute('data-s'),ac:a.content,afs:a.fontSize}})}}"""
G_JS = r"""(u)=>{const g=(ggOf(u)||[]).find(x=>x&&x.f==='c'&&x.ref);const it=document.querySelector('#view .g3list .g3it[data-f="c"] .g3tx');
  const W=document.getElementById('gguw'),ls=W?[...W.querySelectorAll('#gguwMk .thl[data-bx]')]:[];
  return {g:g?{sl:Array.isArray(g.sl)?g.sl.length:null,t_eq_blk:null,t_lines:String(g.t||'').split('\n').length}:null,
    html:it?it.innerHTML:null,txt:it?it.textContent:null,br:it?(it.innerHTML.match(/<br>/g)||[]).length:-1,
    w:W?{sel:W.classList.contains('g3sel'),vis:__H.vis(W),n:ls.length,on:ls.filter(e=>e.classList.contains('on')).length}:null}}"""
BLK_JS = r"""(k)=>{const b=G3.blocks().find(x=>x.key===k);return b?{n:b.lines.length,x:b.lines.map(l=>l.x),text:b.text}:null}"""
TH_JS = r"""(q)=>{const s=[...document.querySelectorAll('.sheet:not(.hide)')].pop();if(!s)return null;const ls=[...s.querySelectorAll(q)].filter(e=>__H.vis(e));
  return {n:ls.length,bx:ls.filter(e=>e.hasAttribute('data-bx')).length,rows:ls.map(e=>[__H.tx(e),+e.getBoundingClientRect().height.toFixed(1)]),
    raw:ls.filter(e=>/\$|<span/.test(e.textContent)).length}}"""
PINCH_JS = r"""([x,y,d0,d1,n])=>{const el=document.elementFromPoint(x,y),box=el&&el.closest('.solz');if(!box)return 'no box';
  const fire=(ty,id,px)=>box.dispatchEvent(new PointerEvent(ty,{bubbles:true,cancelable:true,composed:true,pointerId:id,pointerType:'touch',isPrimary:id===11,clientX:px,clientY:y,buttons:ty==='pointerup'?0:1}));
  fire('pointerdown',11,x-d0/2);fire('pointerdown',12,x+d0/2);
  for(let i=1;i<=n;i++){const d=d0+(d1-d0)*i/n;fire('pointermove',11,x-d/2);fire('pointermove',12,x+d/2)}
  fire('pointerup',11,x-d1/2);fire('pointerup',12,x+d1/2);return 'ok'}"""


def close_sheets(p):
    p.ev("(()=>{document.querySelectorAll('.sheet').forEach(s=>s.remove())})()")
    p.wait(200)


def pinch(p, eng, x, y, d0=60, d1=170, n=10):
    if eng != 'webkit':   # Chromium = CDP 두 손가락(진짜 터치 입력)
        c = p._cdp()

        def pts(d):
            return [{'x': x - d / 2, 'y': y, 'radiusX': 8, 'radiusY': 8, 'id': 1}, {'x': x + d / 2, 'y': y, 'radiusX': 8, 'radiusY': 8, 'id': 2}]
        c.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': pts(d0)})
        for i in range(1, n + 1):
            c.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': pts(d0 + (d1 - d0) * i / n)})
            p.wait(25)
        c.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        p.wait(500)
        return 'cdp'
    r = p.ev(PINCH_JS, [x, y, d0, d1, n])   # WebKit = 합성 touch 포인터 둘(Playwright WebKit 은 두 손가락을 못 보냄 — 길게 누름 WK_LONG 과 같은 길)
    p.wait(500)
    return 'synthetic ' + r


def popups(p):
    return len(p.ctx.pages)


# ── 한 판 · 한 엔진 ──────────────────────────────────────────────────────────────────────────
def run(br, eng, ver):
    o = {'ver': ver, 'eng': eng}
    src = SRC[ver]
    QC.launch('base' if ver == 'BASE' else 'new')
    # PC — A1~A3 · C1~C5 · D · G1~G5 · S
    p = JG.Pg_PP(br, eng, 'ansz-%s-%s-pc' % (ver, eng), src, 'phys', PC, touch=False, remote=JG.Remote())
    try:
        if want('A'):
            p.ev("(no)=>openView(no)", QA_NO); p.wait(1500)
            p.ev("(no)=>ansSheet(no)", QA_NO); p.wait(2500)
            a0 = p.ev(IMG_JS, True); n0 = popups(p)
            p.click(a0['cx'], a0['cy'], wait=1200) if a0 else None
            a1 = p.ev(IMG_JS, False)
            o['A1'] = {'전': a0, '뒤': a1, '창 수 전 · 뒤': [n0, popups(p)]}
            for pg in p.ctx.pages[1:]:
                pg.close()
            a1 = p.ev(IMG_JS, False) or a0
            if a1:
                p.pg.mouse.move(a1['cx'], a1['cy'])
                p.pg.keyboard.down('Control')
                for _ in range(2):
                    p.pg.mouse.wheel(0, -120); p.wait(250)
                p.pg.keyboard.up('Control'); p.wait(500)
            a2 = p.ev(IMG_JS, False)
            o['A2'] = {'전': a1, '뒤': a2}
            if a2:
                p.pg.mouse.dblclick(a2['cx'], a2['cy']); p.wait(700)
            o['A3'] = {'뒤': p.ev(IMG_JS, False), '처음 폭': (a0 or {}).get('w')}
            for pg in p.ctx.pages[1:]:
                pg.close()
            close_sheets(p)
        if want('C'):
            p.ev("(no)=>openView(no)", QA_NO); p.wait(1500)
            p.ev("(()=>{if(!TM.iv)tmRun()})()"); p.wait(3300)
            t0 = p.ev(TM_JS)
            p.pg.mouse.move(t0['cx'], t0['cy']); p.pg.mouse.down(); p.wait(800); p.pg.mouse.up(); p.wait(60)
            t1 = p.ev(TM_JS); p.wait(1300); t1b = p.ev(TM_JS)
            o['C1'] = {'전': t0, '뗀 직후': t1, '1.3 초 뒤': t1b}
            p.click(t0['cx'], t0['cy'], wait=400)
            o['C2'] = {'뒤': p.ev(TM_JS)}
            p.wait(1200)
            t3a = p.ev(TM_JS)
            p.pg.mouse.move(t0['cx'], t0['cy']); p.pg.mouse.down(); p.wait(800); p.pg.mouse.up(); p.wait(60)
            t3 = p.ev(TM_JS); p.wait(1200); t3b = p.ev(TM_JS)
            o['C3'] = {'전': t3a, '뗀 직후': t3, '1.2 초 뒤': t3b}
            p.ev("(()=>{if(!TM.iv)tmRun()})()"); p.wait(2300)
            t4a = p.ev(TM_JS)
            p.pg.mouse.move(t0['cx'] - 10, t0['cy']); p.pg.mouse.down()
            for i in range(1, 6):
                p.pg.mouse.move(t0['cx'] - 10 + 4 * i, t0['cy']); p.wait(30)
            p.wait(650); p.pg.mouse.up(); p.wait(100)
            t4 = p.ev(TM_JS)
            o['C4'] = {'전': t4a, '뒤': t4, '끈 길': '시계 안 가로 20px(폭 %.0f)' % t0['w']}
            p.ev("(()=>{const a=document.activeElement;if(a&&a.blur)a.blur()})()")
            c5 = [p.ev(TM_JS)['run']]
            for _ in range(2):
                p.pg.keyboard.press('Space'); p.wait(400); c5.append(p.ev(TM_JS)['run'])
            o['C5'] = {'켜짐 차례(전 · 스페이스 · 스페이스)': c5}
            # C4x(참고 · 판정 밖) — 마우스로 시계 밖까지 세로 20px 끌기: 길게 누름이 풀리나 · 다음 스페이스 한 번
            p.ev("(()=>{if(!TM.iv)tmRun()})()"); p.wait(2300)
            x0 = p.ev(TM_JS)
            p.pg.mouse.move(t0['cx'], t0['cy']); p.pg.mouse.down()
            for i in range(1, 6):
                p.pg.mouse.move(t0['cx'], t0['cy'] + 4 * i); p.wait(30)
            p.wait(650); p.pg.mouse.up(); p.wait(100)
            x1 = p.ev(TM_JS)
            p.pg.keyboard.press('Space'); p.wait(400)
            o['C4x'] = {'전': [x0['txt'], x0['run']], '뒤': [x1['txt'], x1['run']], '다음 스페이스 뒤 켜짐': p.ev(TM_JS)['run']}
            p.ev("(()=>{if(!TM.iv)tmRun()})()")
        if want('D'):
            o['D'] = p.ev(ND_JS, 1)
        if want('G'):
            o['G'] = gflow(p, eng, touch=False)
        if want('S'):
            p.ev("(no)=>openView(no)", QG_NO); p.wait(1500)
            close_sheets(p)
            p.ev("(()=>{const s=secById('1.3.8');theorySheet([s],s.id+'. '+s.t)})()"); p.wait(1800)
            th = p.ev(TH_JS, '.thl')
            close_sheets(p)
            p.ev("(no)=>openView(no)", QA_NO); p.wait(1500)
            close_sheets(p)
            p.ev("(no)=>conceptSheet(null,rec(no))", QA_NO); p.wait(1800)
            co = p.ev(TH_JS, '.thl,.g3cql')   # 개념 창(sh-concept · g3cw) 줄 = .g3cql(secHTML 아님 — data-bx 없음이 맞음)
            close_sheets(p)
            o['S'] = {'이론': th, '개념': co}
        o['오류'] = (p.errs or []) + (p.ev('window.__err||[]') or [])
    finally:
        p.close()
    # 폰 — A4 · A5 · C6 · C7 · G6
    q = JG.Pg_PP(br, eng, 'ansz-%s-%s-ph' % (ver, eng), src, 'phys', PH, touch=True, remote=JG.Remote())
    try:
        if want('A'):
            q.ev("(no)=>openView(no)", QA_NO); q.wait(1500)
            q.ev("(no)=>ansSheet(no)", QA_NO); q.wait(2500)
            b0 = q.ev(IMG_JS, True); n0 = popups(q)
            if b0:
                q.tap(b0['cx'], b0['cy'], wait=1200)
            b1 = q.ev(IMG_JS, False)
            o['A4'] = {'전': b0, '뒤': b1, '창 수 전 · 뒤': [n0, popups(q)]}
            for pg in q.ctx.pages[1:]:
                pg.close()
            b1 = q.ev(IMG_JS, False) or b0
            how = pinch(q, eng, b1['cx'], b1['cy']) if b1 else None
            o['A5'] = {'전': b1, '뒤': q.ev(IMG_JS, False), '손짓': how}
            close_sheets(q)
        if want('C'):
            q.ev("(no)=>openView(no)", QA_NO); q.wait(1500)
            q.ev("(()=>{if(!TM.iv)tmRun()})()"); q.wait(3300)
            u0 = q.ev(TM_JS)
            q.long_press(u0['cx'], u0['cy'], ms=800, wait=60)
            u1 = q.ev(TM_JS); q.wait(1300); u1b = q.ev(TM_JS)
            o['C6'] = {'전': u0, '뗀 직후': u1, '1.3 초 뒤': u1b}
            q.tap(u0['cx'], u0['cy'], wait=400)
            o['C7'] = {'뒤': q.ev(TM_JS)}
        if want('G'):
            o['G6'] = gflow(q, eng, touch=True)
        o['오류 폰'] = (q.errs or []) + (q.ev('window.__err||[]') or [])
    finally:
        q.close()
    return o


def gflow(p, eng, touch):
    """근거 — 108번 · 블록 U:^01ad5c 넣기 → 근거 줄 누름(개념 창) → 블록 둘째 · 셋째 줄 고름 → 셋째 뺌 → 둘째 뺌"""
    out = {}
    p.ev("(no)=>openView(no)", QG_NO); p.wait(1800)
    blk = p.ev(BLK_JS, BLK)
    if not blk:
        return {'블록 없음': BLK}
    p.ev("([u,k])=>{const b=G3.blocks().find(x=>x.key===k);return G3.push(u,'c',{t:b.text,ref:b.key})}", [QG_U, BLK]); p.wait(1200)
    if p.ev("document.getElementById('view').classList.contains('g3off')"):
        a = p.ev("(()=>__H.hit(document.getElementById('g3Fold')))()")
        p.press(a, wait=700)
    g1 = p.ev(G_JS, QG_U)
    out['G1'] = {'근거 글': g1['txt'], 'sl': (g1['g'] or {}).get('sl'), '<br>': g1['br']}
    at = p.ev("""(()=>{const t=document.querySelector('#view .g3list .g3it[data-f="c"] .g3tx');if(!t)return null;t.scrollIntoView({block:'center'});const r=t.getBoundingClientRect();
      return {on:true,cx:r.left+Math.min(24,r.width/2),cy:r.top+r.height/2}})()""")
    p.press(at, wait=1500)
    g2 = p.ev(G_JS, QG_U)
    out['G2'] = {'개념 창': g2['w']}

    def hit_line(x):
        return p.ev("""(x)=>{const W=document.getElementById('gguw');const e=W&&[...W.querySelectorAll('#gguwMk .thl[data-bx]')].find(z=>z.getAttribute('data-bx')===x);
          if(!e)return null;e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect();return {on:true,cx:r.left+Math.min(40,r.width/2),cy:r.top+Math.min(r.height/2,9)}}""", x)
    l2, l3 = blk['x'][1], blk['x'][2]
    ok2 = p.press(hit_line(l2), wait=900)
    ok3 = p.press(hit_line(l3), wait=900)
    g3 = p.ev(G_JS, QG_U)
    # 서랍 작은 창(g3Pop)도 같은 글
    pop = None
    if p.ev("""(no)=>{const x=document.querySelector('#ndList .ndrow[data-no="'+no+'"] .ndox')||document.getElementById('vBack');if(!x)return false;try{x.scrollIntoView({block:'center'})}catch(e){}g3PopToggle(no,x);return true}""", QG_NO):
        p.wait(900)
        pop = p.ev("""()=>{const P=document.getElementById('g3Pop');if(!P||!__H.vis(P))return null;const e=P.querySelector('.g3pf[data-f="c"] .it.g3pc')||[...P.querySelectorAll('.it.g3pc')].pop();
          return e?{br:(e.innerHTML.match(/<br>/g)||[]).length,mo:/운동량 보존/.test(e.textContent),el:/탄성충돌/.test(e.textContent)}:null}""")
        p.ev("(()=>{const P=document.getElementById('g3Pop');if(P&&typeof g3PopClose==='function')g3PopClose();else if(P)P.remove()})()"); p.wait(300)
    out['G3'] = {'누름': [ok2, ok3], 'sl': (g3['g'] or {}).get('sl'), '<br>': g3['br'], '운동량 보존': '운동량 보존' in (g3['txt'] or ''),
                 '탄성충돌': '탄성충돌' in (g3['txt'] or ''), '고른 줄 표시': (g3['w'] or {}).get('on'), '서랍 작은 창': pop}
    p.press(hit_line(l3), wait=900)
    g4 = p.ev(G_JS, QG_U)
    out['G4'] = {'sl': (g4['g'] or {}).get('sl'), '<br>': g4['br'], '고른 줄 표시': (g4['w'] or {}).get('on')}
    p.press(hit_line(l2), wait=900)
    g5 = p.ev(G_JS, QG_U)
    t5 = p.ev("([u,k])=>{const g=(ggOf(u)||[]).find(x=>x&&x.f==='c'&&x.ref===k);const b=G3.blocks().find(x=>x.key===k);return g&&b?String(g.t)===b.text:null}", [QG_U, BLK])
    out['G5'] = {'근거 글': g5['txt'], 'sl': (g5['g'] or {}).get('sl'), 'g.t = 블록 글': t5, '<br>': g5['br']}
    return out


# ── 판정 ────────────────────────────────────────────────────────────────────────────────────
def j_A(o):
    A1, A2, A3, A4, A5 = (o.get(k) or {} for k in ('A1', 'A2', 'A3', 'A4', 'A5'))
    r = {}
    a0, a1 = A1.get('전') or {}, A1.get('뒤') or {}
    r['A1'] = (bool(a0) and bool(a1) and A1.get('창 수 전 · 뒤', [0, 9])[1] == A1.get('창 수 전 · 뒤', [9, 0])[0] and a1.get('url') == a0.get('url')
               and a1.get('sheets') == a0.get('sheets') and not a1.get('a'),
               {'창 수': A1.get('창 수 전 · 뒤'), '링크 안': a0.get('a'), '폭': [a0.get('w'), a1.get('w')], '이동': a1.get('url') != a0.get('url')})
    b0, b1 = A2.get('전') or {}, A2.get('뒤') or {}
    r['A2'] = (bool(b0) and bool(b1) and b1.get('w', 0) > 1.15 * b0.get('w', 1e9) and b1.get('pnSt') == b0.get('pnSt') and b1.get('shSt') == b0.get('shSt'),
               {'폭 전 · 뒤': [b0.get('w'), b1.get('w')], '배': round(b1.get('w', 0) / max(1, b0.get('w', 1)), 2), '창 굴림 전 · 뒤': [b0.get('pnSt'), b1.get('pnSt'), b0.get('shSt'), b1.get('shSt')]})
    c1 = A3.get('뒤') or {}
    r['A3'] = (bool(c1) and A3.get('처음 폭') is not None and abs(c1.get('w', 0) - A3['처음 폭']) <= 1.5 and b1.get('w', 0) > 1.15 * b0.get('w', 1e9),
               {'두 번 누름 뒤 폭': c1.get('w'), '처음 폭': A3.get('처음 폭'), '확대된 폭(전)': b1.get('w')})
    d0, d1 = A4.get('전') or {}, A4.get('뒤') or {}
    r['A4'] = (bool(d0) and bool(d1) and A4.get('창 수 전 · 뒤', [0, 9])[1] == A4.get('창 수 전 · 뒤', [9, 0])[0] and d1.get('url') == d0.get('url') and not d0.get('a'),
               {'창 수': A4.get('창 수 전 · 뒤'), '링크 안': d0.get('a'), '이동': d1.get('url') != d0.get('url')})
    e0, e1 = A5.get('전') or {}, A5.get('뒤') or {}
    r['A5'] = (bool(e0) and bool(e1) and e1.get('w', 0) > 1.5 * e0.get('w', 1e9) and e1.get('vv') == 1,
               {'폭 전 · 뒤': [e0.get('w'), e1.get('w')], '배': round(e1.get('w', 0) / max(1, e0.get('w', 1)), 2), 'visualViewport.scale': e1.get('vv'), '손짓': A5.get('손짓')})
    return r


def j_C(o):
    r = {}
    C1 = o.get('C1') or {}
    t0, t1, t2 = C1.get('전') or {}, C1.get('뗀 직후') or {}, C1.get('1.3 초 뒤') or {}
    r['C1'] = (t0.get('run') and t0.get('sec', 0) >= 2 and t1.get('txt') == '0:00' and t1.get('run') and t2.get('run') and 1 <= t2.get('sec', 0) <= 3,
               {'전': [t0.get('txt'), t0.get('run')], '뗀 직후': [t1.get('txt'), t1.get('run')], '1.3 초 뒤': [t2.get('txt'), t2.get('run')]})
    c2 = (o.get('C2') or {}).get('뒤') or {}
    r['C2'] = (c2.get('run') is False, {'짧게 누른 뒤': [c2.get('txt'), c2.get('run')]})
    C3 = o.get('C3') or {}
    a, b, c = C3.get('전') or {}, C3.get('뗀 직후') or {}, C3.get('1.2 초 뒤') or {}
    r['C3'] = (a.get('run') is False and a.get('sec', 0) >= 1 and b.get('txt') == '0:00' and b.get('run') is False and c.get('txt') == '0:00' and c.get('run') is False,
               {'전': [a.get('txt'), a.get('run')], '뗀 직후': [b.get('txt'), b.get('run')], '1.2 초 뒤': [c.get('txt'), c.get('run')]})
    C4 = o.get('C4') or {}
    a, b = C4.get('전') or {}, C4.get('뒤') or {}
    r['C4'] = (a.get('run') and b.get('txt') != '0:00' and b.get('sec', 0) >= a.get('sec', 0),   # 안 바뀜 = 0:00 으로 안 감(손 뗀 자리가 시계 안이면 짧은 누름 = 멈춤은 옛 그대로)
               {'전': [a.get('txt'), a.get('run')], '뒤': [b.get('txt'), b.get('run')]})
    c5 = (o.get('C5') or {}).get('켜짐 차례(전 · 스페이스 · 스페이스)') or []
    r['C5'] = (len(c5) == 3 and c5[0] != c5[1] and c5[1] != c5[2], {'켜짐 차례': c5})
    C6 = o.get('C6') or {}
    t0, t1, t2 = C6.get('전') or {}, C6.get('뗀 직후') or {}, C6.get('1.3 초 뒤') or {}
    r['C6'] = (t0.get('run') and t0.get('sec', 0) >= 2 and t1.get('txt') == '0:00' and t1.get('run') and t2.get('run') and 1 <= t2.get('sec', 0) <= 3,
               {'전': [t0.get('txt'), t0.get('run')], '뗀 직후': [t1.get('txt'), t1.get('run')], '1.3 초 뒤': [t2.get('txt'), t2.get('run')]})
    c7 = (o.get('C7') or {}).get('뒤') or {}
    r['C7'] = (c7.get('run') is False, {'톡 뒤': [c7.get('txt'), c7.get('run')]})
    return r


def j_D(o, base_h):
    D = o.get('D') or {}
    m, hs = D.get('m') or [], D.get('hist') or []
    want_s = [x['s'] if x['s0'] > 0 else None for x in hs]
    r = {}
    r['D1'] = (bool(m) and len(m) == len(hs) and [x['ds'] for x in m] == want_s and all(x['m'] in x2['cls'] for x, x2 in zip(hs, m)),
               {'마크(칸 · data-s)': [(x['cls'].replace('ndm ', ''), x['ds']) for x in m], '기록 h(m · s)': [(x['m'], x['s']) for x in hs]})
    r['D2'] = (bool(m) and any(x['ds'] for x in m) and all((x['ac'] == '"%s"' % x['ds']) if x['ds'] else x['ac'] in ('none', 'normal', '') for x in m), {'::after content': [x['ac'] for x in m]})
    r['D3'] = (bool(m) and all(x['afs'] == '7px' for x in m if x['ds']) and any(x['ds'] for x in m), {'::after font-size': [x['afs'] for x in m]})
    r['D4'] = (bool(m) and all(len(x['tx']) == 1 for x in m), {'textContent': [x['tx'] for x in m]})
    r['D5'] = (D.get('h') is not None and base_h is not None and D['h'] <= base_h + 2, {'줄 높이 새 판 · 바탕': [D.get('h'), base_h]})
    return r


def j_G(G):
    G = G or {}
    g1, g2, g3, g4, g5 = (G.get(k) or {} for k in ('G1', 'G2', 'G3', 'G4', 'G5'))
    w = g2.get('개념 창') or {}
    pop = g3.get('서랍 작은 창') or {}
    return {
        'G1': (g1.get('근거 글') == '(1) 탄성충돌' and g1.get('sl') is None and g1.get('<br>') == 0, g1),
        'G2': (bool(w) and w.get('sel') is True and w.get('vis') and w.get('n', 0) >= 3, w),
        'G3': (g3.get('sl') == 2 and g3.get('<br>') == 1 and g3.get('운동량 보존') and not g3.get('탄성충돌') and g3.get('고른 줄 표시') == 2
               and pop.get('br') == 1 and pop.get('mo') and not pop.get('el'), g3),
        'G4': (g4.get('sl') == 1 and g4.get('<br>') == 0 and g4.get('고른 줄 표시') == 1, g4),
        'G5': (g4.get('sl') == 1 and g5.get('근거 글') == '(1) 탄성충돌' and g5.get('sl') is None and g5.get('g.t = 블록 글') is True and g5.get('<br>') == 0, g5)}   # G4(하나 남음)를 거쳐 다 뺀 뒤


def j_S(o, base_s):
    S, B = o.get('S') or {}, base_s or {}
    r = {}
    for c, k in (('S1', '이론'), ('S2', '개념')):
        n, b = S.get(k) or {}, B.get(k) or {}
        rows_n, rows_b = n.get('rows') or [], b.get('rows') or []
        same = len(rows_n) == len(rows_b) and all(x[0] == y[0] and abs(x[1] - y[1]) <= 0.5 for x, y in zip(rows_n, rows_b))
        r[c] = (bool(rows_n) and same and (n.get('bx') == n.get('n') if c == 'S1' else True), {'줄': [n.get('n'), b.get('n')], 'data-bx': n.get('bx'), '글 · 높이 같음': same,
                                                                     '다른 줄': [(i, x[1], y[1]) for i, (x, y) in enumerate(zip(rows_n, rows_b)) if x != y][:3]})
    r['S3'] = (bool(S) and (S.get('이론') or {}).get('raw') == 0 and (S.get('개념') or {}).get('raw') == 0,
               {'날 $ · <span 줄(이론 · 개념)': [(S.get('이론') or {}).get('raw'), (S.get('개념') or {}).get('raw')]})
    return r


NAMES = {'A1': 'PC 그림 누름 = 새 창 · 이동 0 · 창 그대로', 'A2': 'PC Ctrl+휠 위 두 번 = 그림 폭 > 1.15 배 · 칸 안 굴림', 'A3': 'PC 두 번 누름 = 처음 폭',
         'A4': '폰 384 그림 톡 = 이동 0', 'A5': '폰 두 손가락 벌리기 = 그림만 > 1.5 배 · visualViewport.scale = 1',
         'C1': 'PC 가던 시계 0.8 초 누름 = 0:00 부터 계속', 'C2': 'PC 짧게 누름 = 멈춤', 'C3': 'PC 멈춘 시계 길게 = 0:00 멈춘 채',
         'C4': 'PC 누른 채 20px 끌기 = 안 바뀜', 'C5': '스페이스 = 켜고 끄기 그대로', 'C6': '폰 손가락 0.8 초 = 0:00 부터 계속', 'C7': '폰 톡 = 멈춤',
         'D1': '서랍 1번 줄 .ndm data-s = 기록 h[i].s(m:ss)', 'D2': '::after content = 그 값', 'D3': '::after 7px', 'D4': '.ndm 글자 한 자(textContent 그대로)',
         'D5': '줄 높이 = 바탕 + 2px 안', 'G1': '근거 넣은 직후 = 「(1) 탄성충돌」(옛 그대로)', 'G2': '근거 줄 누름 = #gguw.g3sel · 고를 줄 ≥ 3',
         'G3': '블록 둘째 · 셋째 줄 누름 = g.sl 2 · <br> 1 · 「운동량 보존」 있음 · 「탄성충돌」 없음 · 서랍 작은 창도', 'G4': '셋째 다시 누름 = 뺌(g.sl 1)',
         'G5': '다 빼면 옛 그대로(g.sl 없음 · g.t = 블록 글)', 'G6': '폰 손가락 G1~G5 같음',
         'S1': '이론 창 .thl 보이는 글 · 높이 = 바탕(data-bx 만)', 'S2': '개념 창(conceptSheet · 13번) 보이는 줄 글 · 높이 = 바탕', 'S3': '날 $ · <span 글자 0'}
INVAR = {'C2', 'C4', 'C5', 'D4', 'D5', 'G1', 'S2', 'S3'}   # 바탕도 같아야 하는 칸(겉 무변 · 옛 동작) — 헛잣대 셈 밖


def main():
    os.makedirs(TMPD, exist_ok=True)
    R('B0', '판 · 자리', None, None, {'NEW': NEWF, 'md5(LF)': {k: hashlib.md5(v.replace('\r\n', '\n').encode('utf-8')).hexdigest()[:8] for k, v in SRC.items()},
                                     'BASE': BASE if GATE else '(regress · smoke = 안 띄움)', '엔진': ENGS})
    res = {}
    t0 = time.time()
    with sync_playwright() as pw:
        brs = {}
        for eng in ENGS:
            brs[eng] = getattr(pw, eng).launch()
        runs = [('NEW', e) for e in ENGS] + ([('BASE', e) for e in ENGS] if GATE else [])
        for ver, eng in runs:
            t1 = time.time()
            try:
                res[(ver, eng)] = run(brs[eng], eng, ver)
            except Exception as e:
                res[(ver, eng)] = {'하네스 오류': str(e)[:300], 'tb': traceback.format_exc()[-800:]}
            R('B0', '%s %s 돎' % (ver, eng), None, None, '%.1f 분 · 오류 %s' % ((time.time() - t1) / 60, _s((res[(ver, eng)].get('오류') or []) + (res[(ver, eng)].get('오류 폰') or []))[:200]
                                                                              if '하네스 오류' not in res[(ver, eng)] else res[(ver, eng)]['하네스 오류']))
        for b in brs.values():
            b.close()
    BH, BS = {}, {}
    for eng in ENGS:   # 바탕 줄 높이 · 이론/개념 창 = 엔진마다(regress = 기준 스냅샷)
        if GATE:
            bo = res.get(('BASE', eng)) or {}
            BH[eng], BS[eng] = (bo.get('D') or {}).get('h'), bo.get('S')
            QC.base('D5@' + eng, BH[eng])
            QC.base('S@' + eng, BS[eng])
        else:
            no = res.get(('NEW', eng)) or {}
            BH[eng] = QC.base('D5@' + eng, (no.get('D') or {}).get('h'))
            BS[eng] = QC.base('S@' + eng, no.get('S'))

    def judge(o, eng):
        base_h, base_s = BH.get(eng), BS.get(eng)
        if not o or '하네스 오류' in o:
            return {}
        r = {}
        if want('A'):
            r.update(j_A(o))
        if want('C'):
            r.update(j_C(o))
        if want('D'):
            r.update(j_D(o, base_h))
        if want('G'):
            r.update(j_G(o.get('G')))
            g6 = j_G(o.get('G6'))
            r['G6'] = (bool(g6) and all(v[0] for v in g6.values()), {k: v[0] for k, v in g6.items()})
        if want('S'):
            r.update(j_S(o, base_s))
        return r
    for eng in ENGS:
        jn = judge(res.get(('NEW', eng)), eng)
        jb = judge(res.get(('BASE', eng)), eng) if GATE else {}
        o = res.get(('NEW', eng)) or {}
        if o.get('C4x'):
            R('C4x[%s]' % eng, '(참고 · 판정 밖) 마우스로 시계 밖까지 세로 20px 끌기 — 포인터가 시계를 떠나면 앱이 움직임을 못 봄', None, None, o['C4x'])
        for c in NAMES:
            if not want(c[0]):
                continue
            n = jn.get(c)
            b = jb.get(c) if GATE else None
            R('%s[%s]' % (c, eng), NAMES[c], bool(n and n[0]), None if b is None else bool(b[0]),
              {'새 판': n[1] if n else o.get('하네스 오류', '잼 없음'), '바탕': b[1] if b else None} if b else (n[1] if n else o.get('하네스 오류', '잼 없음')), yard=c not in INVAR)
    newp = [x for x in RES if x['new'] is not None]
    yard = [x for x in RES if x['base'] is not None and x['yard']]
    R('B9', '합 — 새 판 PASS %d · FAIL %d · 헛잣대(새 기능 칸 바탕 FAIL) %d/%d · %.1f 분' % (
        sum(1 for x in newp if x['new']), sum(1 for x in newp if not x['new']), sum(1 for x in yard if not x['base']), len(yard), (time.time() - t0) / 60), None)
    with open(OUTF, 'w', encoding='utf-8') as f:
        for x in RES:
            tag = 'INFO' if x['new'] is None else ('PASS' if x['new'] else 'FAIL')
            yb = '' if x['base'] is None else (' · 바탕 ' + (('PASS(바탕도 같음)' if not x['yard'] else 'PASS') if x['base'] else 'FAIL'))
            f.write('%s | %s · %s%s | %s\n' % (tag, x['g'], x['name'], yb, _s(x['d'])[:700]))
    return 0 if all(x['new'] for x in newp) else 1


if __name__ == '__main__':
    sys.exit(main())
