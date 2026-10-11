# -*- coding: utf-8 -*-
r"""_task_jagwa_g3ptop_1011 §B 관문 [클라우드] — 자과 물리 서랍 O △ X 근거 작은 창(#g3Pop) 맨 위 = 그 문제 그림 · 연결 🔗N · ↩N(누르면 목록 · 줄 = 그 문항 팝업)

  python _harness_jagwa_g3ptop.py [--new <앱>] [--base <판 = 400b89a>] [--eng chromium,webkit] [--only G1,G2,…,G7]
                                  [--spd <studyplandata>] [--notes <notes>] [--vendor <cdnjs 사본>] [--prev <phys/미리보기.json>] [--res <결과>]

  NEW = genie 작업트리 jagwa/index.html · BASE = 바탕 main 400b89a(헛잣대 — 새 칸은 바탕 FAIL · 「옛 그대로」 칸은 바탕도 같음)
  엔진 = Chromium · WebKit(새 판 · 바탕 둘 다) · PC 1100×800 마우스 · 폰 384×844 hasTouch(Chromium = CDP 손가락 · WebKit = touchscreen.tap)
  데이터 = studyplandata 현행 route 사본(JG) · 원격 = 가짜 GitHub(메모리 · PUT 밖으로 안 나감)
    · 미리보기(phys/미리보기.json · 비공개) = --prev 파일 → 없으면 <spd>/phys/미리보기.json → 없으면 git -C <spd> show origin/main:phys/미리보기.json — 가짜 원격 files 에 넣음(받는 길 ghRaw 그대로)
    · 연결(LK) · 기록 = 하네스가 메모리에 지어 넣음(기록 없음 · 근거 없음 · 연결 없음인 물리 문항만 골라 씀 · 실제 기록 값은 출력에 안 옮김 · D11) · 창 글은 md5 지문만
  관문:
    G1 그림 있고 「이 문제 → 다른 문항 1」 인 물리 문항(A → T): 서랍 O X 누름 → 창 맨 위 .g3ptop · .pvfig img ≥ 1 · .g3lk.f = 「🔗1」 · .g3lk.b 없음 · 근거 칸 .g3pf 가 그 아래
    G2 🔗1 누름 → .g3lkr 1 줄 · 그 문항(T) 코드 글 · 다시 누름 → 목록 닫힘
    G3 목록 줄 누름 → #g3Pop 닫힘 · .sheet.twin 뜸(그 문항 팝업)
    G4 「다른 문항 → 이 문제」 만 있는 문항(S → C4): ↩1 만(🔗 없음) · 목록 = 그 문항(S)
    G5 그림도 연결도 없는 문항: .g3ptop 없음 · 창 글 = 바탕과 같음(지문)
    G6 폰 손가락: G1 · G2 · G3 톡 · 창 높이 ≤ innerHeight/3 — 첫 화면 상주 서랍(좁은 화면 = 접힌 채 시작 → 폄)
       (문항 창을 연 채로는 폰에서 문항 창 그림판 #inkc 가 서랍 위라 서랍 O X 를 못 누름 — 바탕도 같음 · 이 판 밖)
    G7 지학(카드 층) 서랍 줄 O X 누름 = 바탕과 같음 — 작은 창(#g3Pop) · .g3ptop 없음(근거 작은 창 모듈 gg3 은 물리 전용 · HASBOOK 이면 안 섬) · 줄 글 지문 같음
  모드 — gate = 바탕 띄움 · regress · smoke = 새 판만(G5 · G7 = 기준 스냅샷 · smoke = G1)
"""
import os as _os_r, sys as _sys_r   # env_lanes — _roots.py 를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402,F401 — --mode · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음
import _qa_jagwa_common as JG   # noqa: E402
import hashlib, json, os, subprocess, sys, tempfile, time, traceback   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEWF = ARG('--new', _roots.genie('jagwa', 'index.html'))
BASE = ARG('--base', '400b89a')
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
TMPD = os.path.join(tempfile.gettempdir(), 'h_jagwa_g3ptop')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_jagwa_g3ptop_result.txt'))
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
PVKEY = 'zzikkaplan/studyplandata:phys/미리보기.json'
RES = []


def load_prev():
    """미리보기 표(비공개) — 파일에서 읽어 가짜 원격에 넣는다 · 글은 출력에 안 옮김"""
    f = ARG('--prev') or os.path.join(SPD, 'phys', '미리보기.json')
    if os.path.isfile(f):
        return open(f, 'rb').read(), f
    try:
        b = subprocess.run(['git', '-C', SPD, 'show', 'origin/main:phys/미리보기.json'], capture_output=True, timeout=60).stdout
        if b:
            return b, 'git origin/main:phys/미리보기.json'
    except Exception:
        pass
    return None, None


PVB, PVSRC = load_prev()


def want(g):
    return (not ONLY or g in ONLY) and (not QC.SMOKE or g == 'G1')


def _s(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


def R(g, name, new, base=None, d='', yard=True):
    RES.append(dict(g=g, name=name, new=new, base=base, yard=yard, d=d))
    tag = 'INFO' if new is None else ('PASS' if new else 'FAIL')
    yb = '' if base is None else (' · 바탕 ' + (('PASS(바탕도 같음)' if not yard else 'PASS') if base else 'FAIL'))
    print('%s | %s · %s%s | %s' % (tag, g, name, yb, _s(d)[:700]), flush=True)


def remote():
    rem = JG.Remote()
    if PVB:
        rem.files[PVKEY] = PVB
    return rem


# ── JS ───────────────────────────────────────────────────────────────────────────────────────
PV_READY = r"""()=>!!(typeof PV!=='undefined'&&PV)"""
# 기록 · 근거 · 연결(양쪽) 없는 물리 문항 — 그림 있음(시험지 PDF 쪽 그림) / 그림 없음
PICK_JS = r"""()=>{const lk=new Set();for(const k in LK){lk.add(+k);(LK[k]||[]).forEach(x=>lk.add(+x))}
  const fig=[],nof=[];
  for(const r of DATA){const no=r[F.NO];if(typeof isC==='function'&&isC(r))continue;if(hist(no).length||lk.has(no))continue;
    const u=GGU(r);let gg=0;try{gg=(ggOf(u)||[]).filter(Boolean).length+((typeof g3Cq==='function'?g3Cq(u):[])||[]).length}catch(e){}if(gg)continue;
    let can=false;try{can=pvCanFig(r)}catch(e){}const e=(typeof pvOf==='function')?pvOf(r):null;
    if(can&&e&&Array.isArray(e.fig))fig.push(no);else if(!can)nof.push(no)}
  return {fig:fig.slice(0,6),nofig:nof.slice(0,2),nfig:fig.length,nnofig:nof.length,LK:Object.keys(LK).length}}"""
SEED_JS = r"""async (marks)=>{const t0=Date.now()-3600000;for(const [no,m] of marks)ST[qk(no)]={h:[{m,t:t0,s:40}]};await saveST();try{navBuild()}catch(e){}
  return marks.map(([no])=>!!document.querySelector('#ndList .ndox[data-ox="'+no+'"]'))}"""
LK_JS = r"""(pairs)=>{for(const [a,b] of pairs)LK[a]=[b];return Object.keys(LK).length}"""
# 서랍 O X(.ndox) 자리 — 서랍 목록 안에서 보이게 굴린 뒤
OX_AT = r"""(no)=>{const x=document.querySelector('#ndList .ndox[data-ox="'+no+'"]');if(!x)return null;try{x.scrollIntoView({block:'center'})}catch(e){}
  const r=x.getBoundingClientRect(),e=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);
  return {on:!!e&&(e===x||x.contains(e)),cx:r.left+r.width/2,cy:r.top+r.height/2,top:e?(e.id||e.className||e.tagName):null}}"""
POP_JS = r"""()=>{const P=document.getElementById('g3Pop');if(!P)return null;const t=P.querySelector('.g3ptop'),pf=P.querySelector('.g3pf'),f=P.querySelector('.g3lk.f'),b=P.querySelector('.g3lk.b');
  const R=e=>{if(!e)return null;const q=e.getBoundingClientRect();return {t:q.top,b:q.bottom,cx:q.left+q.width/2,cy:q.top+q.height/2}};
  return {top:!!t,img:P.querySelectorAll('.g3ptop .pvfig img').length,fig:!!P.querySelector('.g3ptop .pvfig'),f:f?f.textContent:null,b:b?b.textContent:null,
    first:P.firstElementChild?P.firstElementChild.className:null,pf:!!pf,pfBelow:!!(t&&pf&&pf.getBoundingClientRect().top>=t.getBoundingClientRect().bottom-1),
    h:Math.round(P.getBoundingClientRect().height),ih:innerHeight,fr:R(f),br:R(b),list:!!P.querySelector('.g3lkl'),
    rows:[...P.querySelectorAll('.g3lkr')].map(r=>({no:+r.dataset.no,code:(r.querySelector('b')||{}).textContent||'',cy:r.getBoundingClientRect().top+r.getBoundingClientRect().height/2,cx:r.getBoundingClientRect().left+30})),
    md5txt:P.innerText.replace(/\s+/g,' ').trim()}}"""
CODE_JS = r"""(no)=>{const r=rec(no);return r?codeShow(r):null}"""
TWIN_JS = r"""()=>{const s=[...document.querySelectorAll('.sheet.twin')].filter(x=>x.isConnected&&getComputedStyle(x).display!=='none');return {twin:s.length,pop:!!document.getElementById('g3Pop')}}"""
EROW_JS = r"""(no)=>{const row=document.querySelector('#ndList .ndrow[data-no="'+no+'"]');if(!row)return null;const m=row.querySelector('.ndox')||row.querySelector('.ndtail .ndm');
  if(m){try{m.scrollIntoView({block:'center'})}catch(e){}}const r=m?m.getBoundingClientRect():null,e=r?document.elementFromPoint(r.left+r.width/2,r.top+r.height/2):null;
  return {ndox:!!row.querySelector('.ndox'),html:row.innerHTML,at:r?{cx:r.left+r.width/2,cy:r.top+r.height/2,on:!!e&&(e===m||m.contains(e))}:null}}"""
CLOSE_JS = r"""()=>{try{g3PopClose()}catch(e){const P=document.getElementById('g3Pop');if(P)P.remove()}document.querySelectorAll('.sheet.twin').forEach(s=>s.remove());return true}"""


def md5(s):
    return hashlib.md5(str(s).encode('utf-8')).hexdigest()[:8]


def wait_pv(p):
    for _ in range(60):
        if p.ev(PV_READY):
            return True
        p.wait(250)
    return False


def pop(p, wait_img=False):
    """창 상태 — 그림은 보일 때 그려짐(pvWatch · PDF 쪽) → 그림 칸이 있으면 img 가 설 때까지 기다림(6 초까지)"""
    x = p.ev(POP_JS)
    if wait_img and x and x.get('fig'):
        for _ in range(24):
            if x.get('img'):
                break
            p.wait(250)
            x = p.ev(POP_JS)
    if x:
        x['md5txt'] = md5(x.get('md5txt', ''))   # D11 — 창 글(근거 · 문항 글)은 지문만
    return x


def press_ox(p, no, touch, wait=700):
    at = p.ev(OX_AT, no)
    if not at:
        return None
    (p.tap if touch else p.click)(at['cx'], at['cy'], wait)
    return at


def press_xy(p, xy, touch, wait=500):
    if not xy:
        return False
    (p.tap if touch else p.click)(xy['cx'], xy['cy'], wait)
    return True


def flow123(p, A, T, touch):
    """G1 · G2 · G3(PC 마우스 · 폰 손가락 같은 길)"""
    o = {}
    p.ev(LK_JS, [[A, T]])   # 동기화가 LK 를 갈아 끼웠어도 다시
    at = press_ox(p, A, touch)
    g1 = pop(p, wait_img=True)
    o['G1'] = {'누름': bool(at and at.get('on')), '창': g1}
    if not g1 or not g1.get('fr'):
        return o
    press_xy(p, g1['fr'], touch)
    g2a = pop(p)
    press_xy(p, (pop(p) or {}).get('fr'), touch)
    g2b = pop(p)
    o['G2'] = {'열림': {'줄': [r['no'] for r in (g2a or {}).get('rows', [])], '코드 = T': [r['code'] == p.ev(CODE_JS, T) for r in (g2a or {}).get('rows', [])], '목록': (g2a or {}).get('list')},
               '다시 누름': {'목록': (g2b or {}).get('list'), '줄 수': len((g2b or {}).get('rows', []))}}
    press_xy(p, (pop(p) or {}).get('fr'), touch)
    g3a = pop(p)
    rows = (g3a or {}).get('rows') or []
    if rows:
        (p.tap if touch else p.click)(rows[0]['cx'], rows[0]['cy'], 1500)
    o['G3'] = {'줄 누름': bool(rows), '뒤': p.ev(TWIN_JS)}
    p.ev(CLOSE_JS); p.wait(300)
    return o


def run(br, eng, ver):
    o = {'ver': ver, 'eng': eng}
    src = SRC[ver]
    QC.launch('base' if ver == 'BASE' else 'new')
    p = JG.Pg_PP(br, eng, 'g3ptop-%s-%s-pc' % (ver, eng), src, 'phys', PC, touch=False, remote=remote())
    try:
        o['PV'] = wait_pv(p)
        pk = p.ev(PICK_JS)
        o['고름'] = {'그림 · 빈 문항': pk.get('nfig'), '그림 없음 · 빈 문항': pk.get('nnofig')}
        fig, nof = pk.get('fig') or [], pk.get('nofig') or []
        if len(fig) < 4 or not nof:
            o['하네스 오류'] = '고를 문항 모자람 %s' % _s(o['고름'])
            return o
        A, T, C4, S = fig[:4]
        N = nof[0]
        o['문항'] = {'A': A, 'T': T, 'C4': C4, 'S': S, 'N': N}
        p.ev("(no)=>openView(no)", A); p.wait(1800)
        o['서랍 O X'] = p.ev(SEED_JS, [[A, 'O'], [C4, 'X'], [N, 'O']])
        p.wait(400)
        if want('G1') or want('G2') or want('G3'):
            o.update(flow123(p, A, T, False))
        if want('G4'):
            p.ev(LK_JS, [[S, C4]])
            at = press_ox(p, C4, False)
            g4 = pop(p)
            if g4 and g4.get('br'):
                press_xy(p, g4['br'], False)
            g4b = pop(p)
            o['G4'] = {'누름': bool(at and at.get('on')), '창': g4, '목록': [r['no'] for r in (g4b or {}).get('rows', [])], 'S': S}
            p.ev(CLOSE_JS); p.wait(300)
        if want('G5'):
            at = press_ox(p, N, False)
            o['G5'] = {'누름': bool(at and at.get('on')), '창': pop(p)}
            p.ev(CLOSE_JS); p.wait(300)
        o['오류'] = (p.errs or []) + (p.ev('window.__err||[]') or [])
    finally:
        p.close()
    if want('G6'):   # 폰 손가락 — 첫 화면 상주 서랍(좁은 화면이면 접힌 채 시작) → 펴고(톡 막이 0.4 초 지나) 같은 길
        q = JG.Pg_PP(br, eng, 'g3ptop-%s-%s-ph' % (ver, eng), src, 'phys', PH, touch=True, remote=remote())
        try:
            wait_pv(q)
            A, T = o['문항']['A'], o['문항']['T']
            q.ev(SEED_JS, [[A, 'O']])
            q.ev("(()=>{try{ndResFold(false)}catch(e){}return true})()"); q.wait(700)
            o['G6'] = flow123(q, A, T, True)
        except Exception as ex:
            o['G6'] = {'오류': str(ex)[:200]}
        finally:
            q.close()
    if want('G7'):   # 지학(카드 층) — 서랍 줄 O X 누름 = 바탕과 같음(작은 창 없음 · 줄 글 같음)
        e = JG.Pg_PP(br, eng, 'g3ptop-%s-%s-earth' % (ver, eng), src, 'earth', PC, touch=False, remote=JG.Remote())
        try:
            no = e.ev("(()=>{for(const r of DATA){const no=r[F.NO];if(typeof isC==='function'&&isC(r))continue;if(!hist(no).length)return no}return null})()")
            e.ev("(no)=>openView(no)", no); e.wait(1800)
            e.ev(SEED_JS, [[no, 'O']]); e.wait(400)
            rw = e.ev(EROW_JS, no)
            if rw and rw.get('at'):
                e.click(rw['at']['cx'], rw['at']['cy'], 700)
            o['G7'] = {'누름': bool(rw and rw.get('at') and rw['at'].get('on')), 'ndox': (rw or {}).get('ndox'), '창': e.ev(TWIN_JS).get('pop'),
                       'g3ptop': e.ev("(()=>!!document.querySelector('.g3ptop'))()"), '줄 지문': md5((rw or {}).get('html', '')), '문항': no}
            e.ev(CLOSE_JS)
        except Exception as ex:
            o['G7'] = {'오류': str(ex)[:200]}
        finally:
            e.close()
    return o


# ── 판정 ────────────────────────────────────────────────────────────────────────────────────
def j123(x, T):
    x = x or {}
    g1 = (x.get('G1') or {}).get('창') or {}
    ok1 = bool(g1) and g1.get('top') and g1.get('first') == 'g3ptop' and (g1.get('img') or 0) >= 1 and g1.get('f') == '🔗1' and g1.get('b') is None and g1.get('pf') and g1.get('pfBelow')
    g2 = x.get('G2') or {}
    op, cl = g2.get('열림') or {}, g2.get('다시 누름') or {}
    ok2 = op.get('줄') == [T] and op.get('코드 = T') == [True] and op.get('목록') is True and cl.get('목록') is False and cl.get('줄 수') == 0
    g3 = x.get('G3') or {}
    ok3 = bool(g3.get('줄 누름')) and (g3.get('뒤') or {}).get('pop') is False and ((g3.get('뒤') or {}).get('twin') or 0) >= 1
    return ok1, ok2, ok3, g1


def judge(o, base):
    if not o or '하네스 오류' in o:
        return {}
    r = {}
    T = (o.get('문항') or {}).get('T')
    ok1, ok2, ok3, g1 = j123(o, T)
    if want('G1'):
        r['G1'] = (ok1, {'창': {k: g1.get(k) for k in ('top', 'first', 'img', 'f', 'b', 'pf', 'pfBelow', 'h')} if g1 else None, '누름': (o.get('G1') or {}).get('누름')})
    if want('G2'):
        r['G2'] = (ok2, o.get('G2'))
    if want('G3'):
        r['G3'] = (ok3, o.get('G3'))
    if want('G4'):
        x = o.get('G4') or {}
        w = x.get('창') or {}
        r['G4'] = (bool(w) and w.get('top') and w.get('b') == '↩1' and w.get('f') is None and x.get('목록') == [x.get('S')],
                   {'창': {k: w.get(k) for k in ('top', 'f', 'b', 'img')} if w else None, '목록 = S': x.get('목록') == [x.get('S')], '누름': x.get('누름')})
    if want('G5'):
        w = (o.get('G5') or {}).get('창') or {}
        bw = base.get('G5') if base else None
        r['G5'] = (bool(w) and not w.get('top') and bw is not None and w.get('md5txt') == bw,
                   {'.g3ptop': w.get('top') if w else None, '창 글 지문': w.get('md5txt') if w else None, '바탕 지문': bw})
    if want('G6'):
        x = o.get('G6') or {}
        a1, a2, a3, h1 = j123(x, T)
        hh = (h1 or {}).get('h') or 0
        ih = (h1 or {}).get('ih') or 1
        r['G6'] = (a1 and a2 and a3 and hh <= ih / 3, {'G1': a1, 'G2': a2, 'G3': a3, '창 높이': hh, 'innerHeight/3': round(ih / 3, 1), '그림': (h1 or {}).get('img'), '오류': x.get('오류')})
    if want('G7'):
        x = o.get('G7') or {}
        bw = base.get('G7') if base else None
        r['G7'] = (bool(x.get('누름')) and x.get('창') is False and x.get('g3ptop') is False and bw is not None and x.get('줄 지문') == bw,
                   {'누름': x.get('누름'), '.ndox': x.get('ndox'), '#g3Pop': x.get('창'), '.g3ptop': x.get('g3ptop'), '줄 지문': x.get('줄 지문'), '바탕 지문': bw, '오류': x.get('오류')})
    return r


NAMES = {'G1': '그림 + 「이 문제 → 다른 문항 1」: 서랍 O X 누름 → 맨 위 .g3ptop · .pvfig img ≥ 1 · 🔗1 · ↩ 없음 · 근거 칸 그 아래',
         'G2': '🔗1 누름 → 목록 1 줄 · 그 문항 코드 · 다시 누름 → 닫힘', 'G3': '목록 줄 누름 → #g3Pop 닫힘 · .sheet.twin 뜸',
         'G4': '「다른 문항 → 이 문제」 만: ↩1 만 · 목록 = 그 문항', 'G5': '그림도 연결도 없는 문항: .g3ptop 없음 · 창 글 = 바탕(지문)',
         'G6': '폰 손가락 G1 · G2 · G3 · 창 높이 ≤ innerHeight/3(첫 화면 서랍)', 'G7': '지학(카드 층) 서랍 줄 O X 누름 = 바탕(작은 창 · .g3ptop 없음 · 줄 글 지문 같음)'}
INVAR = {'G5', 'G7'}   # 옛 그대로여야 하는 칸 — 헛잣대 셈 밖


def main():
    os.makedirs(TMPD, exist_ok=True)
    R('B0', '판 · 자리', None, None, {'NEW': NEWF, 'md5(LF)': {k: hashlib.md5(v.replace('\r\n', '\n').encode('utf-8')).hexdigest()[:8] for k, v in SRC.items()},
                                     'BASE': BASE if GATE else '(regress · smoke = 안 띄움)', '엔진': ENGS, '미리보기': [PVSRC, len(PVB or b'')]})
    if not PVB:
        R('B0', '미리보기 없음 — 그림 칸을 잴 수 없음', False, None, PVSRC)
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
            R('B0', '%s %s 돎' % (ver, eng), None, None, '%.1f 분 · 문항 %s · 고름 %s · %s' % (
                (time.time() - t1) / 60, _s(x.get('문항')), _s(x.get('고름')),
                (x.get('하네스 오류') + ' · ' + x.get('tb', '')[-500:]) if x.get('하네스 오류') else ('오류 %s' % _s(x.get('오류') or [])[:200])))
        for b in brs.values():
            b.close()
    BS = {}
    for eng in ENGS:
        bs = {}
        for c in ('G5', 'G7'):
            x = (res.get(('BASE' if GATE else 'NEW', eng)) or {}).get(c) or {}
            v = (x.get('창') or {}).get('md5txt') if c == 'G5' else x.get('줄 지문')
            bs[c] = QC.base('%s@%s' % (c, eng), v)
        BS[eng] = bs
    for eng in ENGS:
        jn = judge(res.get(('NEW', eng)), BS.get(eng))
        jb = judge(res.get(('BASE', eng)), BS.get(eng)) if GATE else {}
        for c in NAMES:
            if not want(c):
                continue
            n = jn.get(c)
            if n is None:
                continue
            b = jb.get(c) if GATE else None
            R('%s[%s]' % (c, eng), NAMES[c], bool(n[0]), None if b is None else bool(b[0]),
              {'새 판': n[1], '바탕': b[1]} if b is not None else n[1], yard=c not in INVAR)
    newp = [x for x in RES if x['new'] is not None]
    yard = [x for x in RES if x['base'] is not None and x['yard']]
    R('B9', '합 — 새 판 PASS %d · FAIL %d · 헛잣대(새 칸 바탕 FAIL) %d/%d · %.1f 분' % (
        sum(1 for x in newp if x['new']), sum(1 for x in newp if not x['new']), sum(1 for x in yard if not x['base']), len(yard), (time.time() - t0) / 60), None)
    os.makedirs(os.path.dirname(os.path.abspath(OUTF)), exist_ok=True)
    with open(OUTF, 'w', encoding='utf-8') as f:
        for x in RES:
            tag = 'INFO' if x['new'] is None else ('PASS' if x['new'] else 'FAIL')
            yb = '' if x['base'] is None else (' · 바탕 ' + (('PASS(바탕도 같음)' if not x['yard'] else 'PASS') if x['base'] else 'FAIL'))
            f.write('%s | %s · %s%s | %s\n' % (tag, x['g'], x['name'], yb, _s(x['d'])[:700]))
    return 0 if newp and all(x['new'] for x in newp) else 1


if __name__ == '__main__':
    sys.exit(main())
