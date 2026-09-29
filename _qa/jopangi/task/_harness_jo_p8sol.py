# -*- coding: utf-8 -*-
r"""_task_jo_p8sol §B 관문 하네스 — 해례 8판 해설 판올림(⚙ [6e] 데이터) · 「8판 해설 고침」 단추 · 「7판 해설」 상자

  python _harness_jo_p8sol.py --new <앱> [--data <jo/data>] [--exam <gichul/pdf>] [--res <결과>] [--eng chromium,webkit] [--only d1,a1,a2,a3,a4]

  NEW  = 이 판 앱 + 이 판 데이터(⚙ --dry-run 산출) · BASE = genie HEAD(바로 앞 인도판 = jo_revfix0928pm cc7b3f5) 앱 + 데이터 — 칸마다 헛잣대(바탕에서 FAIL)
  누름 = 진짜 포인터(page.mouse · 손가락 = Chromium CDP 터치 r22 · WebKit touchscreen.tap) · 보임 = display ≠ none · 높이 > 0
  기록 = 하네스 사본(route) · 사용자가 고친 해설은 기억(QFIXREC)에만 넣는다(lsWrite·동기화 안 탐)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import io, json, os, re, sys, time, shutil, collections, hashlib
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
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_p8sol_result.txt'))
_BASE = ARG('--base', 'HEAD')
sys.argv = [sys.argv[0], '--new', _NEW, '--data', _DATA, '--base', _BASE, '--exam', _EXAM]
sys.path.insert(0, HERE)
sys.path.insert(0, JOP)
import _harness_jo_gaek_mbsame as M   # noqa: E402
from playwright.sync_api import sync_playwright   # noqa: E402
M.TESTS = M.TESTS + '\n' + io.open(os.path.join(HERE, '_harness_jo_uidmbs2_tests.js'), encoding='utf-8').read() \
    + '\n' + io.open(os.path.join(HERE, '_harness_jo_revfix0928pm_tests.js'), encoding='utf-8').read() \
    + '\n' + io.open(os.path.join(HERE, '_harness_jo_p8sol_tests.js'), encoding='utf-8').read()
M.WORK = M.WORK + '_ps'
RES = []
ROW_S7 = 'P7-0826'        # 바뀜 · 한 줄 문항(8판이 해설을 法193① 으로 고침 · 쪽 그림 확인)
ROW_S7B = 'P7-1209-ㄴ'    # 바뀜 · 선지 줄(A-2-6 · 「ㄴ, ㅁ (△)」)
ROW_NM = 'P7-0144'        # 명칭만
ROW_CUT = 'P7-0292-ㄱ'    # 잘림(책 조각 전문으로 되살림 · 표시 없음)
ROW_NEW = 'P8-0001'       # 새 카드(sol 8판)
ROW_PH = 'P7-0116'        # 폰 · 지시서 사용자 확인 카드(「2018. 9. 28(월)」)
SAME3 = ('P7-0001', 'P7-0002', 'P7-0004')   # 같음 표본 셋
SHOT_ROWS = ('P7-0116', 'P7-0727', 'P7-1204', 'P7-0808-1', 'P7-0808-2', 'P7-0808-3', 'P7-0808-4', 'P7-0171', 'P7-1209-ㄴ', 'P7-1209-ㄹ', 'P7-1209-ㅁ', 'P7-0719', 'P8-0006')
SHOT_OPEN = ('P7-0116', 'P7-1209-ㄴ')      # 「8판 해설 고침」 눌러 7판 상자까지 찍음
SHOT_PAGES = (39, 237, 371, 256, 53, 372, 373, 235, 353)
SHOTS = ARG('--shots', os.path.join(os.environ.get('TEMP', HERE), 'p8sol_shots'))


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


class Pg(M.Pg):
    def __init__(self, br, eng, tag, src, data, exam, W=1553, H=900, **k):
        self.eng = eng
        ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, has_touch=True)
        super().__init__(br, tag + '_' + eng, src, data, exam, ctx=ctx, **k)

    def tap(self, at, wait=500):
        if not at or not at.get('on'):
            return False
        if self.eng == 'webkit':
            self.pg.touchscreen.tap(at['cx'], at['cy'])
            self.pg.wait_for_timeout(wait)
            return True
        return super().tap(at, wait)

    def press(self, at, how, wait=500):
        return self.tap(at, wait) if how == 'touch' else self.click(at, wait)


def home(p, gk='g'):
    p.ev("l=>__HM.home(l)", '특허법')
    if p.ev("()=>__UZ.has('UZGK')"):
        p.ev("v=>__UZ.gk(v)", gk)


def go_key(p, k):
    home(p)
    gk = p.ev("k=>{try{return uzIsGi(k)?'g':'x'}catch(e){return 'g'}}", k)
    home(p, gk)
    sel = p.ev("k=>__UZ.selOfKey(k)", k)
    if not sel:
        return None
    p.ev("s=>__HM.go(s)", sel)
    pg = p.ev("k=>{const P=(OXPOOL||{})[k];if(!P)return null;const d=P.dom;const c=document.getElementById(d);return c?null:(OXDOMPG||{})[d]}", k)
    if pg:
        p.ev("n=>__HM.page(n)", pg)
    p.pg.wait_for_timeout(300)
    return sel


def mb_pop(p, k):
    home(p)
    g0 = p.ev("k=>{try{return uzIsGi(k)?'g':'x'}catch(e){return 'g'}}", k)
    home(p, g0)
    p.click(p.ev("()=>__HM.at('#slot .mbsr input')"), 200)
    p.pg.keyboard.press('Control+A'); p.pg.keyboard.press('Delete')
    p.pg.keyboard.type(k, delay=10); p.pg.wait_for_timeout(800)
    row = p.ev("()=>{const r=[...document.querySelectorAll('#slot .mbres .rr')].find(x=>typeof x.onclick==='function');if(!r)return null;r.scrollIntoView({block:'center'});"
               "const b=r.getBoundingClientRect(),at=document.elementFromPoint(b.left+b.width/2,b.top+b.height/2);return {cx:b.left+b.width/2,cy:b.top+b.height/2,on:!!at&&r.contains(at)};}")
    p.click(row, 1200)
    return p.ev("()=>__PS.qpop()")


def open_card(p, id_, how='mouse'):
    """카드로 가서 「정답·해설 ▸」 을 진짜 포인터로 연다 → 해설 칸 읽기"""
    home(p)                 # 1차객 원장(VJ.P7map)은 그 탭을 열어야 읽힌다
    k = p.ev("i=>__PS.keyP7(i)", id_)
    c = None
    for _ in range(3):      # 첫 이동은 마디를 새로 그려 카드가 늦게 선다 — 다시 간다
        go_key(p, k)
        for _ in range(10):
            c = p.ev("k=>__PS.card(k)", k)
            if c:
                break
            p.pg.wait_for_timeout(200)
        if c:
            break
    if c and not c.get('expVis'):
        p.press(p.ev("k=>__PS.pkAt(k)", k), how, 400)
        c = p.ev("k=>__PS.card(k)", k)
    return k, c


# ══════════ 데이터 ══════════
def jl(b):
    return json.loads(b.decode('utf-8'))


def d1():
    """⚙ [6e] — 바뀐 칸 = sol · 판8(s7) 뿐 · 줄 목록 = 재료 표 · s7 = 옛 sol · 워터마크 꼴 0 · 한 번 더 = 그대로 · 줄 표본(헛잣대 = 바탕 데이터)"""
    G = 'd1'
    import _p8sol_apply as A
    import _p8sol_build as B
    new = jl(open(os.path.join(_DATA, 'jimun_7pan.json'), 'rb').read())
    old = jl(M.git('show', '%s:jo/data/jimun_7pan.json' % _BASE))
    src = jl(open(A.SRC, 'rb').read())
    bo, bn = {z['id']: z for z in old['지문']}, {z['id']: z for z in new['지문']}
    want = {i for i, v in src['rows'].items() if v['cat'] in ('명칭만', '바뀜', '잘림')} | {i for i, v in src['new'].items() if v['sol8'] and not v['유제']}
    chg, extra, badkey = set(), [], []
    for i in bn:
        a, b = bo.get(i), bn[i]
        if a is None:
            extra.append(i); continue
        ks = {k for k in set(a) | set(b) if a.get(k) != b.get(k)}
        if ks:
            chg.add(i)
            if not ks <= {'sol', '판8'}:
                badkey.append([i, sorted(ks)])
    top = sorted(k for k in set(old) | set(new) if k != '지문' and old.get(k) != new.get(k))
    T(G, '바뀐 줄 = 재료 표(명칭만·바뀜·잘림 + 새 카드 sol) %d · 바뀐 칸 = sol·판8 뿐 · 지문 수 같음 · 머리 칸 = 판8_해설 하나' % len(want),
      chg == want and not badkey and not extra and len(bo) == len(bn) and top == ['판8_해설'],
      {'바뀜': len(chg), '표': len(want), '표 밖': sorted(chg - want)[:8], '빠짐': sorted(want - chg)[:8], '다른 칸': badkey[:5], '머리': top})
    s7 = [i for i in bn if (bn[i].get('판8') or {}).get('s7') is not None]
    s7ok = all(bn[i]['판8']['s7'] == (bo[i].get('sol') or '') for i in s7)
    p8keep = all({k: v for k, v in bn[i]['판8'].items() if k != 's7'} == ((bo[i].get('판8') or {'cat': '해설'}) if bo[i].get('판8') else {'cat': '해설'}) for i in s7)
    nbak = sum(1 for i in s7 if src['rows'][i]['cat'] == '바뀜')
    T(G, '판8.s7 = 바뀜 줄만 %d(= 옛 sol 그대로) · 판8 칸이 있던 줄은 cat 무변 · 없던 줄은 {cat:해설}' % len(s7), s7ok and p8keep and nbak == len(s7) == 112,
      {'s7': len(s7), '바뀜': nbak, 's7=옛 sol': s7ok, 'cat 무변': p8keep})
    wm_old = sum(len(B.WMX.findall(z.get('sol') or '')) for z in old['지문'])
    wm_new = sum(len(B.WMX.findall(z.get('sol') or '')) for z in new['지문'])
    T(G, '워터마크 꼴(「@」·휴대전화) 글자 — 새 sol 에 늘지 않음(바탕 %d · 이 판 %d)' % (wm_old, wm_new), wm_new <= wm_old, [wm_old, wm_new])
    again = jl(open(os.path.join(_DATA, 'jimun_7pan.json'), 'rb').read())
    log, bad = A.apply(again, src)
    T(G, '⚙ _p8sol_apply — 이 판 데이터에 한 번 더 = 그대로(None)', log is None and not bad, {'log': log, 'bad': bad[:3]})
    ox = [i for i in chg if (bo[i].get('ox') != bn[i].get('ox'))]
    T(G, 'ox 무변(P7-1209 ㄴ·ㅁ = X 그대로)', not ox and bn['P7-1209-ㄴ']['ox'] == 'X' and bn['P7-1209-ㅁ']['ox'] == 'X', {'ox 바뀜': ox})
    # 표본 — 이 판 / 바탕(헛잣대)
    def smp(D):
        g = lambda i: (D.get(i) or {}).get('sol') or ''
        return {
            '1209ㄴㅁ': g('P7-1209-ㄴ').startswith('ㄴ, ㅁ (△)') and g('P7-1209-ㅁ') == g('P7-1209-ㄴ') and 'ㄷ.' not in g('P7-1209-ㄴ') and g('P7-1209-ㄴ').rstrip().endswith('생각된다.'),
            '1209ㄹ': g('P7-1209-ㄹ').startswith('ㄹ') and '간접침해가 성립한다' in g('P7-1209-ㄹ') and 'ㄷ.' not in g('P7-1209-ㄹ'),
            '0549-2': g('P7-0549-2').startswith('② (O) ③ (X)') and len(g('P7-0549-2')) > 100,
            '0826': '法193①' in g('P7-0826') and '194①' not in g('P7-0826'),
            '0144': g('P7-0144').startswith('지식재산처장 또는 심판장'),
            '0292ㄱ': g('P7-0292-ㄱ').rstrip().endswith('없\n다.') or g('P7-0292-ㄱ').rstrip().endswith('없다.'),
            'P8-0001': len(g('P8-0001')) > 50 and not g('P8-0002'),
        }
    sn, sb = smp(bn), smp(bo)
    T(G, '줄 표본 — 1209 ㄴ·ㅁ(△ · ㄷ 앞까지) · 1209 ㄹ(8판 ㄹ 조각) · 0549-2(공동 해설 전문) · 0826(8판 法193①) · 0144(명칭) · 0292-ㄱ(잘린 끝 되살림) · 새 카드 sol · [유제] 빈칸', all(sn.values()), sn)
    T(G + '-헛', '헛잣대 바탕 데이터 — 표본이 하나도 안 맞음(새 카드 [유제] 빈칸 칸 빼고)', not any(v for k, v in sb.items()), sb)


# ══════════ 앱 ══════════
def a1(p, b, eng):
    """바뀜 줄 — 해설 칸 머리 「8판 해설 고침」(회색 11px 700 · 해설 글 바로 위 왼쪽) → 누름 → 해설 아래 「7판 해설」 상자 = 옛 sol → 다시 → 접힘"""
    G = 'a1'
    for rid in (ROW_S7, ROW_S7B):
        for how in (('mouse', 'touch') if eng == 'chromium' else ('mouse', 'touch')):
            k, c = open_card(p, rid, how)
            z = p.ev("i=>__PS.z(i)", rid)
            s7 = re.sub(r'\s+', ' ', (z or {}).get('판8', {}).get('s7') or '')[:30]
            T(G, '%s %s %s — 단추 「8판 해설 고침」 · 11px 700 회색 · 해설 글 바로 위(사이 요소 없음 · 0~10px = 해설 글 자체 위 여백) 왼쪽(±2)' % (eng, how, rid),
              bool(c) and c.get('btn') == '8판 해설 고침' and c.get('btnVis') and c.get('font') and c['font'][0] == '11px' and c['font'][1] == '700'
              and c.get('place') and 0 <= c['place']['dy'] <= 10 and abs(c['place']['dx']) <= 2 and not c.get('box'), c)
            p.press(p.ev("k=>__PS.btnAt(k)", k), how, 400)
            c1 = p.ev("k=>__PS.card(k)", k)
            T(G, '%s %s %s — 누름 → 해설 아래 「7판 해설」 상자 = 옛 sol(p7Text)' % (eng, how, rid),
              bool(c1) and c1.get('boxVis') and (c1.get('box') or '').startswith('7판 해설') and s7[:20] in (c1.get('box') or '').replace('  ', ' ')
              and c1['place'] and c1['place']['after'] and '(내가 고친 해설' not in (c1.get('box') or ''), {'box': (c1 or {}).get('box', '')[:120], 'place': (c1 or {}).get('place'), 's7': s7})
            p.press(p.ev("k=>__PS.btnAt(k)", k), how, 400)
            c2 = p.ev("k=>__PS.card(k)", k)
            T(G, '%s %s %s — 한 번 더 → 접힘' % (eng, how, rid), bool(c2) and not c2.get('box') and c2.get('btn') == '8판 해설 고침', {'box': (c2 or {}).get('box')})
        kb, cb = open_card(b, rid)
        T(G + '-헛', '%s %s 헛잣대 바탕 — 단추 없음' % (eng, rid), bool(cb) and not cb.get('btn'), cb)


def a2(p, b, eng):
    """명칭만 · 잘림 · 새 카드 — 표시 없음 · 글은 8판(새 카드 = 해설 있음 · 바탕은 「해설 없음」)"""
    G = 'a2'
    for rid, lab, need in ((ROW_NM, '명칭만', '지식재산처장'), (ROW_CUT, '잘림(되살림)', '받을 수 없'), (ROW_NEW, '새 카드', None)):
        k, c = open_card(p, rid)
        ok = bool(c) and not c.get('all') and c.get('expVis') and (need is None or need in (c.get('sol') or '')) and '해설 없음' not in (c.get('sol') or '')
        T(G, '%s %s %s — 「8판 해설 고침」 없음 · 해설 글 = 8판' % (eng, lab, rid), ok, c)
    kb, cb = open_card(b, ROW_NEW)
    T(G + '-헛', '%s 헛잣대 바탕 — 새 카드 %s 해설 없음' % (eng, ROW_NEW), bool(cb) and '해설 없음' in (cb.get('sol') or ''), cb)
    kb, cb = open_card(b, ROW_NM)
    T(G + '-헛', '%s 헛잣대 바탕 — %s 해설 글 = 7판(특허청장)' % (eng, ROW_NM), bool(cb) and '특허청장' in (cb.get('sol') or ''), cb)


def a3(p, b, eng):
    """사용자가 고친 해설이 있는 줄 — 고친 글이 먼저 · 단추는 그대로 서고 상자에 「(내가 고친 해설이 보이는 중)」"""
    G = 'a3'
    k = p.ev("i=>__PS.keyP7(i)", ROW_S7)
    p.ev("k=>__PS.fixExp(k,'내가 고친 해설 표본')", k)
    try:
        k, c = open_card(p, ROW_S7)
        p.press(p.ev("k=>__PS.btnAt(k)", k), 'mouse', 400)
        c1 = p.ev("k=>__PS.card(k)", k)
        T(G, '%s %s 고친 해설 — 해설 글 = 고친 글 · 단추 선다 · 상자 끝 「(내가 고친 해설이 보이는 중)」' % (eng, ROW_S7),
          bool(c1) and '내가 고친 해설 표본' in (c1.get('sol') or '') and c1.get('btn') == '8판 해설 고침' and (c1.get('box') or '').endswith('(내가 고친 해설이 보이는 중)'), c1)
    finally:
        p.ev("k=>__PS.fixExp(k,null)", k)
        p.ev("()=>render()")


def a4(p, b, eng):
    """다른 해설 자리 — 문제 창(1차객 🔍 → 줄 · 누름) · 기출뷰 지문 상자(DOM) · 헛잣대 = 바탕"""
    G = 'a4'
    k = p.ev("i=>__PS.keyP7(i)", ROW_S7)
    qp = mb_pop(p, k)
    p.ev("()=>__PS.qpOpen()")
    qp = p.ev("()=>__PS.qpop()")
    ok0 = bool(qp) and qp.get('btn') == '8판 해설 고침'
    p.click(p.ev("()=>__PS.qpBtnAt()"), 400)
    qp1 = p.ev("()=>__PS.qpop()")
    T(G, '%s 문제 창 %s — 단추 · 누름 → 「7판 해설」 상자' % (eng, ROW_S7), ok0 and (qp1 or {}).get('boxVis') and (qp1.get('box') or '').startswith('7판 해설'), {'앞': qp, '뒤': qp1 and qp1.get('box', '')[:80]})
    p.ev("()=>__HM.closeAll()")
    kb = b.ev("i=>__PS.keyP7(i)", ROW_S7)
    qb = mb_pop(b, kb)
    T(G + '-헛', '%s 헛잣대 바탕 문제 창 — 단추 없음' % eng, bool(qb) and not qb.get('btn'), qb)
    b.ev("()=>__HM.closeAll()")
    for rid in (ROW_S7B, ROW_S7):
        ex = p.ev("i=>__PS.exvProbe(i)", rid)
        if ex and ex.get('none'):
            N(G, '%s 기출뷰 지문 상자 %s — 그 지문이 든 기출 문항 없음(%s)' % (eng, rid, ex['none']), ex)
            continue
        T(G, '%s 기출뷰 지문 상자 %s(uzExvBox 직접 · DOM) — 단추 「8판 해설 고침」' % (eng, rid), bool(ex) and ex.get('btn') == '8판 해설 고침', ex)
        exb = b.ev("i=>__PS.exvProbe(i)", rid)
        T(G + '-헛', '%s 헛잣대 바탕 기출뷰 %s — 단추 없음' % (eng, rid), bool(exb) and not exb.get('btn') and not exb.get('none'), exb)
        break


def a5(p, b, eng):
    """「같음」 표본 셋 — 해설 DOM 글 = 바탕과 같음 · 단추 없음"""
    G = 'a5'
    for rid in SAME3:
        k, c = open_card(p, rid)
        kb, cb = open_card(b, rid)
        T(G, '%s 같음 %s — 해설 글 = 바탕 · 「8판 해설 고침」 없음' % (eng, rid),
          bool(c) and bool(cb) and c.get('sol') and c.get('sol') == cb.get('sol') and not c.get('all'), {'NEW': (c or {}).get('sol', '')[:60], 'BASE': (cb or {}).get('sol', '')[:60]})


def a6(p, b, eng, br):
    """폰 390×844 손가락 — P7-0116(지시서 사용자 확인 카드) · 단추 → 상자 → 접힘"""
    G = 'a6'
    ns, nd, ne = M.new_env()
    q = Pg(br, eng, 'psP', ns, nd, ne, W=390, H=844)
    try:
        k, c = open_card(q, ROW_PH, 'touch')
        z = q.ev("i=>__PS.z(i)", ROW_PH)
        ok0 = bool(c) and c.get('btn') == '8판 해설 고침' and c.get('btnVis') and '2018. 9. 28' in (c.get('sol') or '')
        q.tap(q.ev("k=>__PS.btnAt(k)", k), 400)
        c1 = q.ev("k=>__PS.card(k)", k)
        s7 = re.sub(r'\s+', ' ', (z or {}).get('판8', {}).get('s7') or '')[:20]
        ok1 = bool(c1) and c1.get('boxVis') and s7 in (c1.get('box') or '')
        q.tap(q.ev("k=>__PS.btnAt(k)", k), 400)
        c2 = q.ev("k=>__PS.card(k)", k)
        T(G, '%s 폰 390×844 손가락 %s — 해설 「2018. 9. 28」 · 단추 → 「7판 해설」 상자 → 접힘' % (eng, ROW_PH), ok0 and ok1 and bool(c2) and not c2.get('box'),
          {'앞': c and {x: c.get(x) for x in ('btn', 'place')}, '상자': (c1 or {}).get('box', '')[:80], '뒤': (c2 or {}).get('box')})
        T('ERR', '%s 폰 — NEW 앱 오류 0' % eng, not q.errs_all(), q.errs_all()[:4])
    finally:
        q.close()


def s1(p, b, eng):
    """표본 화면 사진(카드 요소 · 해설 편 채) — 쪽 그림(8판 · 아래 띠 잘라 냄)은 한 번만 · 글 대조 = 카드 DOM 해설 글 ↔ ⚙ 가 8판 글자층에서 뽑은 글(빈칸 빼고)"""
    G = 's1'
    if eng != 'chromium':
        return
    os.makedirs(SHOTS, exist_ok=True)
    src = json.loads(open(os.path.join(JOP, '특상디', '_p8up', '_p8sol.json'), 'rb').read().decode('utf-8'))
    ws = lambda t: re.sub(r'\s+', '', t or '')
    for rid in SHOT_ROWS:
        k, c = open_card(p, rid)
        if rid in SHOT_OPEN:
            p.press(p.ev("k=>__PS.btnAt(k)", k), 'mouse', 400)
        f = os.path.join(SHOTS, 'card_%s.png' % rid)
        try:
            p.pg.locator('[id="qb-%s"]' % k).screenshot(path=f)
        except Exception as e:
            f = 'ERR ' + repr(e)[:80]
        v = src['rows'].get(rid) or src['new'].get(rid) or {}
        want = v.get('sol8')
        dom = p.ev("k=>{const c=document.getElementById('qb-'+k);const w=c&&c.querySelector('.mbexp');const s=w&&(w.querySelector('.p8sw > :not(.p8sh):not(.p8t7)')||w.querySelector('.sol'));return s?s.textContent:null}", k)
        ok = bool(dom) and (want is None or ws(dom) == ws(want) or (ws(dom).startswith(ws(want)) and ws(dom)[len(ws(want)):].startswith('📗리담해설')))   # 리담과 흡수된 줄은 뒤에 「📗 리담 해설」(바탕 그대로)
        T(G, '%s 표본 %s — 카드 해설 글 = ⚙ 8판 글%s · 사진 %s' % (eng, rid, '' if want else '(같음 줄 = 옛 글 그대로)', os.path.basename(f)), ok,
          {'dom': (dom or '')[:80], 'pdf8': v.get('pdf8'), 'cat': v.get('cat')})
    try:
        import pymupdf, _p8sol_build as B
        d = pymupdf.open(B.PDF8)
        for pno in sorted(set(SHOT_PAGES)):
            pg = d[pno - 1]; r = pg.rect
            pg.get_pixmap(dpi=100, clip=pymupdf.Rect(0, 0, r.width, r.height * 0.93)).save(os.path.join(SHOTS, 'p8_pdf%d.png' % pno))
        N(G, '8판 쪽 그림(아래 띠 잘라 냄 · 값 안 옮김) — %s' % SHOTS, sorted(set(SHOT_PAGES)))
    except Exception as e:
        N(G, '8판 쪽 그림 못 뜸', repr(e)[:200])


BR = {}
PARTS = [('a1', a1), ('a2', a2), ('a3', a3), ('a4', a4), ('a5', a5), ('a6', a6), ('s1', s1)]
DPARTS = [('d1', d1)]


def run_engine(pw, eng):
    br = getattr(pw, eng).launch()
    BR[eng] = br
    ns, nd, ne = M.new_env()
    bs, bd, be = M.base_env()
    try:
        p = Pg(br, eng, 'psN', ns, nd, ne)
        b = Pg(br, eng, 'psB', bs, bd, be)
        try:
            for k, fn in PARTS:
                if ONLY and k not in ONLY:
                    continue
                print('── %s · %s' % (eng, k), flush=True)
                try:
                    fn(p, b, eng, br) if k == 'a6' else fn(p, b, eng)
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
    for k, fn in DPARTS:
        if not ONLY or k in ONLY:
            try:
                fn()
            except Exception as e:
                T('RUN', u'%s 데이터 묶음이 멈춤' % k, False, repr(e)[:600])
    if not ONLY or any(k in ONLY for k, _ in PARTS):
        with sync_playwright() as pw:
            for eng in ENGS:
                RES.append(('ENG', eng, None, ''))
                run_engine(pw, eng)
    npass = sum(1 for r in RES if r[2] is True); nfail = sum(1 for r in RES if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · %s · NEW %s · 데이터 %s · 바탕 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), 'p8sol', os.path.basename(_NEW), _DATA,
                M.git('rev-parse', '--short', _BASE).decode().strip(), ','.join(ENGS)))
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[ok], g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:900]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
