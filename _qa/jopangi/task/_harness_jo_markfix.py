# -*- coding: utf-8 -*-
r"""_task_jo_markfix §B 관문 하네스 — 1차객 7판 카드 형광펜 · 막대 하나(선택 아래) · 조문 칠(jopangi.jomark) · 팝업 켠 마크업 · 「다만,」

  python _harness_jo_markfix.py --new <앱> [--data <jo/data>] [--exam <gichul/pdf>] [--res <결과>] [--eng chromium,webkit] [--only b1,...]

  NEW = 이 판 앱 · BASE = genie HEAD(바로 앞 인도판 = jo_revfix0928night dfbb144) 앱 — 데이터는 둘 다 genie jo/data(이 판 데이터 무변)
  기록 = 하네스 사본(route) · PUT 밖으로 안 나감 · 누름·끌기 = 진짜 포인터(page.mouse) · 손가락 = Chromium CDP r22 / WebKit tap
  폰 「길게 눌러 선택」은 브라우저 선택 메뉴 몫이라 헤드리스로 못 낸다 — 폰 막대 자리는 도구가 만든 선택(Range)으로 잰다(보고에 적음)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import io, json, os, re, sys, time, shutil
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
JOP = os.path.dirname(HERE)


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


_NEW = ARG('--new')
_DATA = ARG('--data', _roots.genie(r'jo\data'))
_EXAM = ARG('--exam', _roots.genie(r'gichul\pdf'))
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_markfix_result.txt'))
sys.argv = [sys.argv[0], '--new', _NEW, '--data', _DATA, '--exam', _EXAM, '--eng', ','.join(ENGS)]
sys.path.insert(0, HERE)
sys.path.insert(0, JOP)
import _harness_jo_book8 as B8   # noqa: E402
M = B8.M
M.TESTS = M.TESTS + '\n' + io.open(os.path.join(HERE, '_harness_jo_markfix_tests.js'), encoding='utf-8').read()
M.WORK = M.WORK + '_mf'
from playwright.sync_api import sync_playwright   # noqa: E402
RES = []
JO7 = ('특허법', '제7조')
DMN = [('특허법', '제103조의2'), ('상표법', '제105조'), ('민사소송법', '제101조')]
BLUE = 'rgb(47, 111, 208)'


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def reload(p):
    p.pg.goto('http://127.0.0.1:%d/index.html?tok=1&keep=1' % p.port, wait_until='load', timeout=180000)
    p.pg.wait_for_function(M.READY, timeout=180000); p.pg.wait_for_timeout(900)


def unit(p, mg):
    B8.home(p)
    p.ev("s=>__HM.go(s)", mg)
    p.pg.wait_for_timeout(700)


def jo(p, law, k, extra=''):
    p.ev("a=>{try{closeAllPops()}catch(e){}S.law=a[0];S.tab='jo';S.jo=a[1];%s;return render()}" % (extra or '0'), [law, k])
    p.pg.wait_for_timeout(1200)


def drag(p, d):
    if not d:
        return False
    m = p.pg.mouse
    m.move(d['x0'], d['y0']); m.down()
    for i in range(1, 11):
        m.move(d['x0'] + (d['x1'] - d['x0']) * i / 10, d['y0'] + (d['y1'] - d['y0']) * i / 10); p.pg.wait_for_timeout(15)
    m.up(); p.pg.wait_for_timeout(450)
    return True


def place_ok(bar, sel):
    """막대가 선택 아래(top ≥ 선택 bottom + 8) · 아래 자리가 없으면 위(bottom ≤ 선택 top) · 보이는 화면 안"""
    if not bar or not bar['vis'] or not sel:
        return False
    r, v = bar['rect'], bar['vv'] or {'x': 0, 'y': 0, 'w': 1e9, 'h': 1e9}
    inside = r['x'] >= v['x'] + 7.5 and r['r'] <= v['x'] + v['w'] - 7.5 and r['y'] >= v['y'] + 7.5 and r['b'] <= v['y'] + v['h'] - 7.5
    below = r['y'] >= sel['b'] + 7.5
    above = r['b'] <= sel['y'] + 0.5 and sel['b'] + 10 + r['h'] > v['y'] + v['h'] - 8
    return inside and (below or above)


# ══════════ A-1 · A-2 1차객 ══════════
def b1(p, b, eng):
    G = 'b1'
    out, outb = {}, {}
    for i in range(12):
        unit(p, '__mg%d' % i); out[i] = p.ev("()=>__MF.cards()")
        unit(b, '__mg%d' % i); outb[i] = b.ev("()=>__MF.cards()")
    n = sum(v['n'] for v in out.values()); mk = sum(v['mk'] for v in out.values()); mkb = sum(v['mk'] for v in outb.values())
    T(G, '%s 첫 12 단원 7판 카드 지문 글 %d — data-mk %d(= 카드 수)' % (eng, n, mk), n > 50 and mk == n, {i: [v['n'], v['mk']] for i, v in out.items()})
    T(G + '-헛', '%s 헛잣대 바탕 — data-mk 0' % eng, mkb == 0, mkb)
    # 긋기 — 마우스 끌기 → 막대 → 노랑 → 저장 → 새로고침 뒤 그대로
    unit(p, '__mg0')
    c = p.ev("()=>__MF.firstCardText()")
    d = p.ev("a=>__MF.dragAB(a[0],a[1],a[2])", [c['sel'], 2, 9]) if c else None
    drag(p, d)
    sel, bar = p.ev("()=>__MF.selRect()"), p.ev("()=>__MF.bar('mkc9')")
    p.click(p.ev("a=>__MF.btnAt(a[0],a[1])", ['mkc9', 'y']), 500)
    uid = (c or {}).get('mk', '|').split('|')[0]
    keys = p.ev("u=>__MF.mkKeys('card|1차객|'+u+'¦')", uid) or p.ev("u=>__MF.mkKeys('card|1차객|'+u)", uid)
    marks = p.ev("s=>__MF.marksIn(s)", c['sel']) if c else None
    reload(p); unit(p, '__mg0')
    after = p.ev("u=>[...document.querySelectorAll('#slot .mbqtx')].filter(x=>(x.dataset.mk||'').indexOf(u+'|')===0).map(x=>x.querySelectorAll('mark.mkc').length)", uid)
    T(G, '%s 7판 카드 글 마우스 끌기 → 막대(선택 아래) → 노랑 → jopangi.markup 「card|1차객|」 1 · 칠 · 새로고침 뒤 그대로' % eng,
      bool(c) and bar and bar['vis'] and len(keys) == 1 and marks and len(marks) == 1 and after and after[0] == 1,
      {'카드': c, '막대': bar and bar['rect'], '선택': sel, '열쇠': keys, '칠': marks, '새로고침 뒤': after})
    # ✏️ 표시
    p.ev("()=>{S.mkOff=true;return render()}"); p.pg.wait_for_timeout(500)
    off = p.ev("()=>document.querySelectorAll('#slot mark.mkc').length")
    p.ev("()=>{S.mkOff=false;return render()}"); p.pg.wait_for_timeout(500)
    on = p.ev("()=>document.querySelectorAll('#slot mark.mkc').length")
    T(G, '%s 「✏️ 표시 꺼짐」 → 칠 0 · 켜면 되살아남' % eng, off == 0 and on >= 1, [off, on])
    # 흡수 줄 — 리담 카드와 7판 카드 열쇠 같음(uid) · 문제 창(7판 글 보이기만)에도 칠
    eq = p.ev("()=>{const z=VJ.P7map['P7-0630'];const q=(VJ.qs||[]).find(q=>(q.지문||[]).some(x=>x.uid===z.uid));const lz=q&&q.지문.find(x=>x.uid===z.uid);return z&&lz?[oxKeyP7(z),oxKeyLid(q,lz)]:null}")
    T(G, '%s 흡수 줄 P7-0630 — 7판 카드 열쇠 = 리담 카드 열쇠(%s)' % (eng, eq and eq[0]), bool(eq) and eq[0] == eq[1], eq)


def b2(p, b, eng, br):
    G = 'b2'
    unit(p, '__mg2')
    c = p.ev("()=>__MF.firstCardText()")
    drag(p, p.ev("a=>__MF.dragAB(a[0],a[1],a[2])", [c['sel'], 1, 6]) if c else None)
    b1_ = p.ev("()=>__MF.bar('mkc9')"); sel = p.ev("()=>__MF.selRect()")
    jo(p, *JO7)
    ls = p.ev("()=>__MF.lineSel(0)")
    drag(p, p.ev("a=>__MF.dragAB(a[0],a[1],a[2])", [ls, 3, 9]))
    b2_ = p.ev("()=>__MF.bar('jomk9')")
    b3_ = p.ev("()=>__MF.c2bar()")
    sig = lambda B: [(x['cls'], x['m'], x['t'], x['w'], x['h']) for x in (B or {}).get('btns', []) if x['t'] != '🏷']
    want = [('sw', m) for m in 'ygbrop'] + [('tx', 'u'), ('tx', 'ub'), ('tx', '')]
    ok = sig(b1_) == sig(b2_) == sig(b3_) and [(x[0], x[1]) for x in sig(b1_)] == want and all(x['t'] == 'U' and x['deco'] == 'underline' for x in b1_['btns'] if x['m'] in ('u', 'ub'))
    T(G, '%s 막대 단추 = 형광 6 + 「U」 2(빨강·파랑 밑줄 글자) + 🧽 · 1차객·조문·2차 차례·크기 같음' % eng, ok, {'1차객': sig(b1_), '조문': sig(b2_), '2차': sig(b3_)})
    T(G, '%s PC 1400×900 마우스 선택 — 1차객 막대 top ≥ 선택 bottom + 8 · 화면 안' % eng, place_ok(b1_, sel), {'막대': b1_ and b1_['rect'], '선택': sel})
    # 화면 아래 끝 선택 → 위로
    unit(p, '__mg0')
    p.ev("()=>{const xs=[...document.querySelectorAll('#slot .qwrap .mbqtx[data-mk]')].filter(e=>e.textContent.length>12);if(!xs.length)return false;let q=xs[0].parentElement;while(q&&q!==document.body){const cs=getComputedStyle(q);if(/(auto|scroll)/.test(cs.overflowY)&&q.scrollHeight>q.clientHeight+1)break;q=q.parentElement;}if(!q||q===document.body)q=document.scrollingElement;q.scrollTop=0;for(let k=0;k<200;k++){const x=xs.find(e=>{const r=e.getBoundingClientRect();return r.top>innerHeight-75&&r.top<innerHeight-22;});if(x){x.id='__mfb';return true;}q.scrollTop+=17;}return false}")
    p.pg.wait_for_timeout(300)
    drag(p, p.ev("a=>__MF.dragAB(a[0],a[1],a[2])", ['#__mfb', 1, 5]))
    lo = p.ev("()=>__MF.bar('mkc9')"); sl = p.ev("()=>__MF.selRect()")
    T(G, '%s 선택이 화면 아래 끝 — 막대가 위(bottom ≤ 선택 top) · 화면 안' % eng, place_ok(lo, sl) and lo['rect']['b'] <= sl['y'] + 0.5, {'막대': lo and lo['rect'], '선택': sl})
    # 칠 꼴 · 옛 칠(y·p·u)
    unit(p, '__mg2')
    c = p.ev("()=>__MF.firstCardText()")
    uid = c['mk'].split('|')[0]
    p.ev("a=>__MF.mkSeed(a[0],a[1])", [uid, [[0, 2, 'y'], [3, 5, 'p'], [6, 8, 'u']]])
    unit(p, '__mg2')
    mk = p.ev("u=>{const x=[...document.querySelectorAll('#slot .mbqtx')].find(x=>(x.dataset.mk||'').indexOf(u+'|')===0);x.id='__mfs';return __MF.marksIn('#__mfs')}", uid)
    ok = bool(mk) and all('linear-gradient' in m['bgi'] for m in mk if m['t'] in ('mkc y', 'mkc p')) and all(m['bb'].startswith('2px solid rgb(239, 68, 68)') for m in mk if m['t'] == 'mkc u') and {m['t'] for m in mk} >= {'mkc y', 'mkc p', 'mkc u'}
    T(G, '%s 칠 꼴 = 아래 45%% 칠(linear-gradient) · u = 밑줄 2px 빨강 · 옛 칠(심은 y·p·u) 그대로 보임' % eng, ok, mk)
    # 폰 390×844 · 확대 1.5
    ns, nd, ne = M.new_env()
    q = B8.Pg(br, eng, 'mfP', ns, nd, ne, W=390, H=844)
    try:
        res = {}
        for zoom in (1.0, 1.5):
            unit(q, '__mg2')
            if zoom != 1.0 and eng == 'chromium':
                cdp = q.pg.context.new_cdp_session(q.pg); cdp.send('Emulation.setPageScaleFactor', {'pageScaleFactor': zoom}); q.pg.wait_for_timeout(400)
            elif zoom != 1.0:
                continue
            c = q.ev("()=>__MF.firstCardText()")
            q.ev("a=>__MF.selectAB(a[0],a[1],a[2])", [c['sel'], 1, 6]); q.pg.wait_for_timeout(500)
            res[zoom] = {'막대': q.ev("()=>__MF.bar('mkc9')"), '선택': q.ev("()=>__MF.selRect()")}
        for zoom, r in res.items():
            T(G, '%s 폰 390×844%s — 1차객 막대 선택 아래 · 보이는 화면 안' % (eng, '' if zoom == 1.0 else ' 확대 1.5'), place_ok(r['막대'], r['선택']), {'막대': r['막대'] and [r['막대']['rect'], r['막대']['vv']], '선택': r['선택']})
        if eng != 'chromium':
            N(G, '%s 폰 확대 1.5 — WebKit 은 CDP 확대가 없어 Chromium 만' % eng, '')
    finally:
        q.close()


# ══════════ A-3 조문 칠 ══════════
def b3(p, b, eng):
    G = 'b3'
    jo(p, *JO7)
    L0 = p.ev("()=>__MF.lines()")
    ls = p.ev("()=>__MF.lineSel(0)")
    drag(p, p.ev("a=>__MF.dragAB(a[0],a[1],a[2])", [ls, 3, 9]))
    bar = p.ev("()=>__MF.bar('jomk9')"); bub = p.ev("()=>__MF.bub()"); sel = p.ev("()=>__MF.selRect()")
    p.click(p.ev("a=>__MF.btnAt(a[0],a[1])", ['jomk9', 'ub']), 500)
    jm = p.ev("()=>__MF.jm()"); L1 = p.ev("()=>__MF.lines()")
    geo = all(abs(a['r'][k] - b_['r'][k]) <= 0.5 for a, b_ in zip(L0, L1) for k in ('y', 'h', 'w'))
    ks = [k for k in jm if k.startswith('특허법:제7조|')]
    T(G, '%s 제7조 본문 마우스 끌기 → 막대(도구 아홉 + 🏷 · 선택 아래) · 따로 뜨던 🏷 거품 0 → 밑줄 파랑 → jopangi.jomark 1 칸 · 그 줄 칠' % eng,
      bar and bar['vis'] and len(bar['btns']) == 10 and bar['btns'][-1]['t'] == '🏷' and not bub and place_ok(bar, sel) and len(ks) == 1 and jm[ks[0]][0][2] == 'ub' and L1[0]['jmk'] >= 1,
      {'막대': bar and bar['rect'], '거품': bub, 'jomark': jm, '줄': L1[:1]})
    T(G, '%s 긋기 전후 줄 높이·폭·다음 줄 y 같음(±0.5px)' % eng, geo and len(L0) == len(L1), [[a['r'], b_['r']] for a, b_ in zip(L0, L1)][:3])
    # 필기 있는 조 · 필기 켜고 끄기 · 스티커 편집 · 빈칸 모드
    p.ev("()=>__MF.inkSeed('jo|특허법:제7조')")
    jo(p, *JO7)
    Lp = p.ev("()=>__MF.lines()")
    ls = p.ev("()=>__MF.lineSel(1)")
    drag(p, p.ev("a=>__MF.dragAB(a[0],a[1],a[2])", [ls, 2, 7]))
    p.click(p.ev("a=>__MF.btnAt(a[0],a[1])", ['jomk9', 'y']), 500)
    jm2 = p.ev("()=>__MF.jm()")
    n2 = sum(len(v) for k, v in jm2.items() if k.startswith('특허법:제7조|'))
    T(G, '%s 필기가 있는 조(심은 필기 · 볼트 줄 모드)에서도 긋기 됨(잠금 없음) · 칠 줄 %d' % (eng, sum(1 for l in p.ev("()=>__MF.lines()") if l['jmk'])), n2 >= 2 and not Lp[0]['wm'], {'줄 모드': 'wm' if Lp and Lp[0]['wm'] else '볼트', 'jomark': jm2})
    jo(p, *JO7, extra='S.ink=true'); a1 = sum(l['jmk'] for l in p.ev("()=>__MF.lines()"))
    jo(p, *JO7, extra='S.ink=false'); a2 = sum(l['jmk'] for l in p.ev("()=>__MF.lines()"))
    jo(p, *JO7, extra='S.stick=true'); a3 = sum(l['jmk'] for l in p.ev("()=>__MF.lines()"))
    jo(p, *JO7, extra="S.stick=false")
    T(G, '%s 필기 켜기·끄기 뒤 칠 그대로 · ✎ 편집(S.stick) 켜도 그대로' % eng, a1 > 0 and a1 == a2 == a3, [a1, a2, a3])
    p.ev("()=>{const A=JSON.parse(localStorage.getItem('jopangi.ink')||'{}');delete A['jo|특허법:제7조'];localStorage.setItem('jopangi.ink',JSON.stringify(A));try{recDropCache()}catch(e){}}")
    # 빈칸 모드 — 빈칸 자료가 있는 조에 칠을 심고 빈칸을 켠다
    bk = p.ev("""async()=>{const D=await blankData('특허법');const ks=Object.keys((D&&D.조)||{});return ks.find(k=>(D.조[k].행||[]).some(r=>(r.b||[]).length))||null}""")
    if bk:
        jo(p, '특허법', bk)
        p.ev("k=>{return get('jo_특허법_본문.json').then(B=>{const j=B.조[k];const r=j.행.find(r=>r.k[0]!=='H'&&(r.t||'').length>6);const A=JSON.parse(localStorage.getItem('jopangi.jomark')||'{}');A['특허법:'+k+'|'+rowKey(r)]=[[0,4,'y']];localStorage.setItem('jopangi.jomark',JSON.stringify(A));try{recDropCache()}catch(e){}})}", bk)
        jo(p, '특허법', bk); n0 = p.ev("()=>document.querySelectorAll('#slot span.jmk').length")
        jo(p, '특허법', bk, extra="S.joBlank={내용:true,주체:true,기간:true}"); n1 = p.ev("()=>document.querySelectorAll('#slot span.jmk').length"); on = p.ev("()=>!!document.querySelector('#slot input')")
        jo(p, '특허법', bk, extra="S.joBlank={내용:false,주체:false,기간:false}")
        T(G, '%s 빈칸 모드(%s) — 칠 0(평소 %d)' % (eng, bk, n0), n0 > 0 and n1 == 0 and on, [n0, n1, on])
    # 🏷 → 태그 스티커 창
    ls = p.ev("()=>__MF.lineSel(0)")
    drag(p, p.ev("a=>__MF.dragAB(a[0],a[1],a[2])", [ls, 12, 16]))
    p.click(p.ev("a=>__MF.btnAt(a[0],a[1])", ['jomk9', '🏷']), 700)
    pops = p.ev("()=>__MF.pops()")
    T(G, '%s 막대 「🏷」 → 태그 스티커 창(stkAttachPop · 옛 거품과 같은 창)' % eng, any(('붙이기' in x or '스티커' in x) for x in pops), pops)
    p.ev("()=>{try{closeAllPops()}catch(e){}}")
    # 헛잣대 — 바탕은 거품 · 막대 없음
    jo(b, *JO7)
    ls = b.ev("()=>__MF.lineSel(0)")
    drag(b, b.ev("a=>__MF.dragAB(a[0],a[1],a[2])", [ls, 3, 9]))
    T(G + '-헛', '%s 헛잣대 바탕 — 조문 긁기 = 🏷 거품 · 막대 없음' % eng, b.ev("()=>__MF.bub()") and not (b.ev("()=>__MF.bar('jomk9')") or {}).get('vis'), '')


# ══════════ A-4 팝업 ══════════
def b4(p, b, eng):
    G = 'b4'
    out = {}
    for tag, q in (('NEW', p), ('BASE', b)):
        jo(q, *JO7)
        hd = q.ev("()=>{const s=document.querySelector('#slot .mkn');return s?s.textContent:null}")
        q.ev("()=>{popJo('특허법','제7조',{clientX:700,clientY:300},1)}"); q.pg.wait_for_timeout(1200)
        out[tag] = {'마크업': hd, '팝업': q.ev("()=>__MF.popMarks('jo|특허법|제7조')") or q.ev("()=>{const p=(POPS||[]).filter(x=>/제7조/.test(x._pk||'')).pop();return p?p._pk:null}")}
        q.ev("()=>{try{closeAllPops()}catch(e){}}")
    T(G, '%s 제7조 「✎ 마크업 %s」(켠 기록 없음) — 조문 팝업 볼트 마크업 칠·빨간 글 %s(바탕 %s)' % (eng, out['NEW']['마크업'], (out['NEW']['팝업'] or {}).get('n'), (out['BASE']['팝업'] or {}).get('n')),
      (out['NEW']['팝업'] or {}).get('n') == 0 and ((out['BASE']['팝업'] or {}).get('n') or 0) >= 3, out)
    # 하나 켬 → 팝업에도 그 하나
    jo(p, *JO7)
    it = p.ev("()=>{const X=WMX;const it=X&&X.b.items.find(x=>x.g==='mk');if(!it)return null;mkonSet(X.base,{k:[it.key],s:[],x:[]});return it.key}")
    p.ev("()=>{popJo('특허법','제7조',{clientX:700,clientY:300},1)}"); p.pg.wait_for_timeout(1200)
    one = p.ev("()=>__MF.popMarks('jo|특허법|제7조')")
    T(G, '%s 「✎ 마크업」에서 하나 켬(%s) → 팝업에도 그 하나 · 내 칠(jomark)도 팝업에 보임' % (eng, it), bool(one) and one['n'] >= 1 and one['n'] < ((out['BASE']['팝업'] or {}).get('n') or 99) and one['jmk'] >= 1, one)
    p.ev("()=>{mkonSet('특허법:제7조',{k:[],s:[],x:[]});try{closeAllPops()}catch(e){}}")


# ══════════ A-5 「다만,」 ══════════
def b6(p, b, eng):
    G = 'b6'
    for law, k in DMN:
        jo(p, law, k); d = p.ev("()=>__MF.dmn('#slot .box')"); tn = p.ev("()=>__MF.lineTexts()")
        jo(b, law, k); db = b.ev("()=>__MF.dmn('#slot .box')"); tb = b.ev("()=>__MF.lineTexts()")
        br = (d or {}).get('br', [])
        ok = bool(br) and all(x['prevTop'] is not None and x['top'] > x['prevTop'] + 5 and x['rowX'] is not None and abs(x['left'] - x['rowX']) <= 1 and int(x['fw']) >= 700 and x['color'] == BLUE for x in br)
        T(G, '%s %s %s — 「다만,」 %d 곳: 앞 글보다 한 줄 아래 · 왼쪽 x = 행 글 시작 x(±1) · 굵기 ≥ 700 · 색 %s · 줄 글자 = 바탕' % (eng, law, k, len(br), BLUE), ok and tn == tb, {'NEW': br[:3], '글자 같음': tn == tb})
        T(G + '-헛', '%s %s %s 헛잣대 바탕 — 줄 안 바뀜(.dmn 0)' % (eng, law, k), not (db or {}).get('br'), db)
    # 이미 첫머리 — 새 줄 안 생김
    hd = p.ev("""async()=>{const B=await get('jo_상표법_본문.json');for(const [k,j] of Object.entries(B.조||{})){for(const r of (j.행||[])){if(/^\\s*다만,/.test(r.t||''))return k;}}return null}""")
    if hd:
        jo(p, '상표법', hd, extra='S.stick=true'); d = p.ev("()=>__MF.dmn('#slot .box')"); jo(p, '상표법', hd, extra='S.stick=false')
        T(G, '%s 상표 %s — 행 첫머리 「다만,」 = 굵은 파랑 · 새 줄 없음(빈 줄 0)' % (eng, hd), (d or {}).get('head', 0) >= 1, d)
    # 팝업 · 3법 비교 카드
    jo(p, '특허법', '제103조의2')
    p.ev("()=>{popJo('특허법','제103조의2',{clientX:700,clientY:300},1)}"); p.pg.wait_for_timeout(1200)
    pm = p.ev("()=>__MF.popMarks('jo|특허법|제103조의2')")
    card = p.ev("async()=>{const c=await cmp3Card('상표법','제105조',null,[],'',false,{});c.id='__mfc3';document.body.appendChild(c);return __MF.dmn('#__mfc3')}")
    T(G, '%s 조문 팝업 · 3법 비교 카드 본문에도 「다만,」 새 줄' % eng, bool(pm) and pm['dmnbr'] >= 1 and bool(card) and len(card['br']) >= 1, {'팝업': pm, '카드': card})
    p.ev("()=>{try{closeAllPops()}catch(e){};const c=document.getElementById('__mfc3');if(c)c.remove();}")
    # 칠이 「다만,」에 걸침 — 칠·다만 둘 다
    jo(p, '특허법', '제103조의2')
    info = p.ev("""()=>{const L=[...document.querySelectorAll('#slot .box .ln')].find(l=>l.querySelector('.dmn.dmnbr'));if(!L)return null;const ri=L._wm?L._wm.ri:+L.dataset.ri;return {ri}}""")
    ink = p.ev("""async()=>{const A=JSON.parse(localStorage.getItem('jopangi.ink')||'{}');const ks=Object.keys(A).filter(k=>/^jo\|/.test(k)&&(A[k].s||[]).length);const out={n:ks.length,dm:[]};
      for(const k of ks){const m=/^jo\|([^:]+):(.+)$/.exec(k);if(!m)continue;try{const B=await get('jo_'+m[1]+'_본문.json');const j=(B.조||{})[m[2]];if(j&&(j.행||[]).some(r=>/다만,/.test(r.t||'')&&/\S/.test((r.t||'').split('다만,')[0])))out.dm.push(k);}catch(e){}}return out}""")
    N(G, '%s 기록 사본의 필기 있는 조문 %s — 「다만,」 새 줄이 생기는 조 %d(필기 자리가 어긋날 수 있음 · 옮기기는 이 판 밖)' % (eng, (ink or {}).get('n'), len((ink or {}).get('dm') or [])), ink)


def b5(p, b, eng):
    """무변 — 리담 선지 글(기출뷰 선지 상자 · pitWire) 길게 누르기(선택 없음) → 포스트잇 창 = 바탕과 같음"""
    G = 'b5'
    res = {}
    for tag, q in (('NEW', p), ('BASE', b)):
        res[tag] = b5one(q)
    T(G, '%s 기출뷰 리담 선지 글 마우스 길게 누르기 700ms(선택 없음) — 뜨는 창 = 바탕과 같음 · 칠 막대 안 뜸' % eng, res['NEW'] is not None and res['NEW'][0] == res['BASE'][0] and not res['NEW'][1], res)


def b5one(p):
    B8.home(p)
    p.ev("()=>{try{mbGiGo('2026')}catch(e){}}"); p.pg.wait_for_timeout(1500)
    at = p.ev("()=>{const x=[...document.querySelectorAll('#slot .uzexb .mbqtx')].find(e=>e.textContent.length>12);if(!x)return null;x.scrollIntoView({block:'center'});const r=x.getBoundingClientRect();return {x:r.left+20,y:r.top+r.height/2}}")
    if not at:
        return None
    m = p.pg.mouse; m.move(at['x'], at['y']); m.down(); p.pg.wait_for_timeout(700); m.up(); p.pg.wait_for_timeout(700)
    pops = p.ev("()=>__MF.pops()"); bar = (p.ev("()=>__MF.bar('mkc9')") or {}).get('vis')
    p.ev("()=>{try{closeAllPops()}catch(e){}}")
    return [pops, bar]


BR = {}
PARTS = [('b1', b1), ('b2', b2), ('b3', b3), ('b4', b4), ('b5', b5), ('b6', b6)]
WITH_BR = ('b2',)


def run_engine(pw, eng):
    br = getattr(pw, eng).launch()
    BR[eng] = br
    ns, nd, ne = M.new_env()
    bs, bd, be = M.base_env()
    try:
        p = B8.Pg(br, eng, 'mfN', ns, nd, ne, W=1400, H=900)
        b = B8.Pg(br, eng, 'mfB', bs, bd, be, W=1400, H=900)
        try:
            for k, fn in PARTS:
                if ONLY and k not in ONLY:
                    continue
                print('── %s · %s' % (eng, k), flush=True)
                try:
                    fn(p, b, eng, br) if k in WITH_BR else fn(p, b, eng)
                except Exception as e:
                    T('RUN', u'%s · %s 묶음이 멈춤' % (eng, k), False, repr(e)[:600])
            T('ERR', u'%s — NEW 앱 오류 0' % eng, not p.errs_all(), p.errs_all()[:6])
        finally:
            p.close(); b.close()
    finally:
        br.close()


def main():
    shutil.rmtree(os.path.join(M.WORK, 'head'), ignore_errors=True)
    os.makedirs(M.WORK, exist_ok=True)
    t0 = time.time()
    with sync_playwright() as pw:
        for eng in ENGS:
            RES.append(('ENG', eng, None, ''))
            run_engine(pw, eng)
    npass = sum(1 for r in RES if r[2] is True); nfail = sum(1 for r in RES if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · %s · NEW %s · 데이터 %s · 바탕 HEAD %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), 'markfix', os.path.basename(_NEW), _DATA,
                M.git('rev-parse', '--short', 'HEAD').decode().strip(), ','.join(ENGS)))
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[ok], g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:900]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
