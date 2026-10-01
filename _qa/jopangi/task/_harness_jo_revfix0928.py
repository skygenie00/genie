# -*- coding: utf-8 -*-
r"""_task_jo_revfix0928 §B(9/28) 관문 하네스 — 연결 창 · 정오문제 창 처음 크기 · 빈칸 종류 칸 · 기출뷰 = 민법 값 · 조 패널 카드 칩 · 3법 칸 자리 · 서랍 이름.

  python _harness_jo_revfix0928.py --new <앱> --data <jo/data> [--exam <gichul/pdf>] [--only r1,r2,...] [--eng chromium,webkit] [--res <결과 파일>]

  NEW  = 이 판 앱 + 데이터 · BASE = genie HEAD(바로 앞 인도판 = jo_wonmun b880a04) 앱 + HEAD 데이터 — 칸마다 헛잣대(바탕에서 FAIL)
  누름 = 진짜 포인터(page.mouse · 손가락 = Chromium CDP 터치 r22 · WebKit touchscreen.tap · 펜 = CDP pointerType pen) · 보임 = display ≠ none · 높이 > 0 · 자리 = elementFromPoint
  틀 = mbsame 하네스(_harness_jo_gaek_mbsame.py)의 serve·Pg·__HM · uidmbs2 도구(__UZ) · cardfix 도구(__CF) · joscreen 도구(__JS) · wonmun 도구(__WM) · 이 판 도구(__RV).
  민법 값 = 지시서 §0 ④ 표(채팅 실측 · 민법 1553px 2026)를 고정 잣대로 쓴다.
"""
import io, json, os, re, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


_NEW, _DATA, _EXAM = ARG('--new'), ARG('--data'), ARG('--exam')
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_revfix0928_result.txt'))
sys.argv = [sys.argv[0], '--new', _NEW, '--data', _DATA, '--base', 'b880a04'] + (['--exam', _EXAM] if _EXAM else [])   # A-6(d) 9/30 — 바탕 = 인도 때 HEAD b880a04(docstring 「jo_wonmun b880a04」 · 결정로그 9/28 07:40) · HEAD 로 두면 인도 뒤 헛잣대·바탕 대조가 새 판끼리 맞대 거꾸로 FAIL
sys.path.insert(0, HERE)
import _harness_jo_gaek_mbsame as M   # noqa: E402
from playwright.sync_api import sync_playwright   # noqa: E402
M.TESTS = '\n'.join([M.TESTS] + [io.open(os.path.join(HERE, f), encoding='utf-8').read() for f in (
    '_harness_jo_uidmbs2_tests.js', '_harness_jo_cardfix_tests.js', '_harness_jo_joscreen_tests.js', '_harness_jo_wonmun_tests.js', '_harness_jo_revfix0928_tests.js')])
M.WORK = M.WORK + '_rv'
RES = []


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:480]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:480]), flush=True)


class Pg(M.Pg):
    def __init__(self, br, eng, tag, src, data, exam, W=1440, H=900, **k):
        self.eng = eng
        ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, has_touch=True)
        super().__init__(br, tag + '_' + eng, src, data, exam, ctx=ctx, **k)
        self.pg.on('dialog', lambda d: d.dismiss())

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

    def J(self, expr, arg=None):
        v = self.ev(expr, arg)
        try:
            return json.loads(v) if isinstance(v, str) else v
        except Exception:
            return v

    def size(self, W, H):
        self.pg.set_viewport_size({'width': W, 'height': H})
        self.pg.wait_for_timeout(300)

    def hold(self, x, y, ms=600, wait=400):
        """마우스 길게 누르기(진짜 포인터)"""
        self.pg.mouse.move(x, y); self.pg.mouse.down(); self.pg.wait_for_timeout(ms); self.pg.mouse.up(); self.pg.wait_for_timeout(wait)

    def _cdp(self):
        if not self.cdp:
            self.cdp = self.ctx.new_cdp_session(self.pg)
        return self.cdp

    def finger(self, x, y, ms=600, wait=500):
        """손가락 길게 — CDP 터치 r22(크로미움만)"""
        pt = {'x': x, 'y': y, 'radiusX': 22, 'radiusY': 22, 'force': 1, 'id': 1}
        self._cdp().send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [pt]})
        self.pg.wait_for_timeout(ms)
        self._cdp().send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        self.pg.wait_for_timeout(wait)

    def pen(self, x, y, ms=600, wait=400):
        """펜 — CDP 마우스 사건 pointerType pen(크로미움만)"""
        c = self._cdp()
        c.send('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': x, 'y': y, 'pointerType': 'pen'})
        c.send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': x, 'y': y, 'button': 'left', 'buttons': 1, 'clickCount': 1, 'pointerType': 'pen', 'force': 0.5})
        self.pg.wait_for_timeout(ms)
        c.send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': x, 'y': y, 'button': 'left', 'buttons': 0, 'clickCount': 1, 'pointerType': 'pen'})
        self.pg.wait_for_timeout(wait)

    def drag(self, at, dx, dy, how='mouse'):
        """손잡이 끌기 — 마우스(진짜 포인터)"""
        if not at or not at.get('on'):
            return False
        self.pg.mouse.move(at['cx'], at['cy']); self.pg.mouse.down()
        self.pg.mouse.move(at['cx'] + dx / 2, at['cy'] + dy / 2, steps=4); self.pg.mouse.move(at['cx'] + dx, at['cy'] + dy, steps=4)
        self.pg.mouse.up(); self.pg.wait_for_timeout(500)
        return True


def envs():
    return M.new_env(), M.base_env()


def reload_keep(q):
    q.pg.goto('http://127.0.0.1:%d/index.html?tok=1&keep=1' % q.port, wait_until='load', timeout=180000)
    q.pg.wait_for_function(M.READY, timeout=180000); q.pg.wait_for_timeout(700)


def home(q, law='특허법', gk='g'):
    q.ev("l=>__HM.home(l)", law)
    if q.ev("()=>__UZ.has('UZGK')"):
        q.ev("v=>__UZ.gk(v)", gk)


def gkOf(q, k):
    return 'g' if q.ev("k=>{try{return uzGkPass?(UZGK='g',uzGkPass(k)):true}catch(e){return true}}", k) else 'x'


def go_key(q, k):
    home(q, gk=gkOf(q, k))
    sel = q.ev("k=>__UZ.selOfKey(k)", k)
    if not sel:
        return None
    q.ev("s=>__HM.go(s)", sel)
    pg = q.ev("k=>{const P=(OXPOOL||{})[k];if(!P)return null;const d=P.dom;const c=[...document.querySelectorAll('.qb.id')].find(b=>b.textContent.trim()===k);return c?null:(OXDOMPG||{})[d]}", k)
    if pg:
        q.ev("n=>__HM.page(n)", pg)
    q.pg.wait_for_timeout(250)
    return sel


def go_jo(q, law, jo):
    q.ev("a=>__WM.go(a[0],a[1])", [law, jo])
    q.pg.wait_for_timeout(300)


def close_all(q):
    q.ev("()=>{try{closeAllPops(true)}catch(e){}return 1}")


# ══════════ §B-1 연결 창(A-1) ══════════
K0 = 'TR06092'
VPS = (('폰', 390, 844, 'touch'), ('PC', 1280, 900, 'mouse'), ('아이패드', 820, 1180, 'touch'))


def cf_flow(q, how):
    q.ev("o=>__CF.seedLk(o)", {K0: ['T2259185']})
    go_key(q, K0)
    q.ev("()=>__CF.winClose()")
    e0 = len(q.errs_all())
    at = q.ev("k=>__CF.lkBtn(k)", K0)
    q.press(at, how, 900)
    w0 = q.ev("()=>__RV.cf()")
    q.press(q.ev("()=>__RV.cfInp()"), how, 300)
    q.pg.keyboard.type(u'조문', delay=40)
    q.pg.wait_for_timeout(700)
    w1 = {}
    for _ in range(25):   # 다른 두 법 데이터가 붙으면 결과가 다시 그려진다(S1855224 = 상표)
        w1 = q.ev("()=>__RV.cf()")
        if 'S1855224' in (w1.get('uids') or []):
            break
        q.pg.wait_for_timeout(300)
    q.pg.wait_for_timeout(500)   # 결과를 그린 뒤 다시 맞춤(ResizeObserver → rAF)
    w1 = q.ev("()=>__RV.cf()")
    reach1 = q.ev("()=>__RV.cfReach()")
    r0 = q.ev("()=>__RV.cfRow0()")
    pressed = q.press(r0, how, 1300)
    w2 = q.ev("()=>__RV.cf()")
    reach2 = q.ev("()=>__RV.cfReach()")
    lk = q.ev("k=>__CF.lk(k)", K0)
    errs = q.errs_all()[e0:e0 + 4]
    q.ev("()=>__CF.winClose()")
    return {'btn': bool(at and at.get('on')), 'w0': w0, 'w1': w1, 'reach1': reach1, 'row0': r0, 'pressed': pressed, 'w2': w2, 'reach2': reach2, 'lk': lk, 'errs': errs}


def cf_ok(r):
    w1, a, w2, b = r['w1'] or {}, r['reach1'] or {}, r['w2'] or {}, r['reach2'] or {}
    row0 = w1.get('row0') or {}
    uid = (r['row0'] or {}).get('uid')
    my = (r['lk'] or {}).get('my') or []
    part = {
        '열림': bool(r['btn'] and (r['w0'] or {}).get('win')),
        '입력 뒤 창 화면 안(8px)': bool(w1.get('inScreen')),
        '결과 첫 줄 보임(굴리지 않고)': bool(row0.get('seen')),
        '걸린 연결 닿음': bool(a.get('cur')),
        '안내 줄 닿음': bool(a.get('ft')),
        '결과 줄 누름 → 연결': bool(r['pressed'] and uid and my == ['T2259185', uid]),
        '누른 뒤 창 화면 안': bool(w2.get('inScreen') and b.get('inScreen')),
        '누른 뒤 걸린 연결 2 닿음': bool(w2.get('curN') == 2 and b.get('cur') and b.get('ft')),
        '오류 0': not r['errs'],
    }
    return all(part.values()), part


def g_r1(p, b, eng):
    G = 'r-1'
    for vp, W, H, how in VPS:
        res = {}
        for who, q in (('NEW', p), ('BASE', b)):
            q.size(W, H)
            if who == 'NEW':   # ★ 9/30 A-6 — revfix0929b A-6: 폰(≤480) 부팅 = 1차객 서랍 접힌 채 · 펼친 폰 서랍 바깥 첫 누름은 접기만(DRAWER_EAT) → PC 로 연 판을 줄였으니 폰은 부팅처럼 접고 PC·아이패드는 인도 때처럼 편다
                q.ev("w=>{S.jtFold=w<=480;return 1}", W)
            res[who] = cf_flow(q, how)
        ok, part = cf_ok(res['NEW'])
        n = res['NEW']
        T(G, u'%s %d×%d(%s) — 카드 ✏️ → 「조문」 → 창 위·아래 끝 화면 안(8px) · 결과 첫 줄 보임 · 걸린 연결·안내 줄 닿음(몸 굴림) · 결과 줄 누름 → 연결 · 창 여전히 화면 안' % (vp, W, H, u'손가락' if how == 'touch' else u'마우스'), ok,
          {'부분': part, '창': (n['w1'] or {}).get('W'), 'max-height': (n['w1'] or {}).get('mh'), '결과': (n['w1'] or {}).get('rowsN'), '첫 줄': (n['w1'] or {}).get('row0'), '누른 뒤 창': (n['w2'] or {}).get('W'), '연결': n['lk'], '오류': n['errs']})
        bok, bpart = cf_ok(res['BASE'])
        bw = res['BASE']['w1'] or {}
        det = {'부분': bpart, '창': bw.get('W'), 'max-height': bw.get('mh'), '계산 max-height': bw.get('cmh'), '첫 줄': bw.get('row0')}
        if vp == u'폰':
            T(G + '-헛', u'헛잣대 바탕 폰 — 창 max-height 120px · 결과 첫 줄이 창 밖', not bok and bw.get('mh') == '120px' and not (bw.get('row0') or {}).get('seen'), det)
        elif vp == 'PC':
            T(G + '-헛', u'헛잣대 바탕 PC — 「조문」 친 뒤 창 아래 끝이 화면(900) 밖', not bok and ((bw.get('W') or {}).get('b') or 0) > H - 8 + 1, det)
        else:
            N(G + '-헛', u'바탕 아이패드(지시서 헛잣대 없음 — 값만)', det)
    p.size(1440, 900); b.size(1440, 900)


# ══════════ §B-2 정오문제 창 처음 크기(A-2) ══════════
def open_jp(q):
    close_all(q)
    q.ev("()=>{S.joPanel=false;return 1}")
    go_jo(q, u'특허법', u'제140조')
    q.press(q.J("()=>__WM.jpChip()"), 'mouse', 1600)
    return q.ev("()=>__RV.jp()")


def g_r2(p, b, eng):
    G = 'r-2'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        q.size(1280, 900)
        q.ev("o=>__RV.uiSeed(o)", {'jpw': 340, 'jph': 640, 'jww': None, 'jwh': None})
        reload_keep(q)
        res[who] = {'ui0': q.ev("()=>__RV.ui()"), 'jp': open_jp(q)}
    n, bb = res['NEW']['jp'], res['BASE']['jp']
    T(G, u'옛 판 UI 기록 {jpw:340} 심고 새로고침 → ☑ 정오문제 창 = 470×640', n.get('win') and n.get('w') == 470 and n.get('h') == 640, {'NEW': n, '심은 UI': {k: (res['NEW']['ui0'] or {}).get(k) for k in ('jpw', 'jph', 'jww', 'jwh')}})
    T(G + '-헛', u'헛잣대 바탕 — 340 폭(옛 패널 키 jpw 를 읽는다)', bb.get('win') and bb.get('w') == 340, bb)
    # 손잡이 +50 → 520 → 새로고침 520(창 오른쪽에 50px 넘는 자리가 있게 폭 1600)
    p.size(1600, 900)
    open_jp(p)
    g = p.ev("()=>__RV.jpGrip()")
    p.drag(g, 50, 0)
    j1 = p.ev("()=>__RV.jp()")
    u1 = p.ev("()=>__RV.ui()") or {}
    reload_keep(p)
    j2 = open_jp(p)
    T(G, u'손잡이 +50 → 520 · UI 기록 jww 520(옛 jpw 칸은 이 저장에서 사라짐) → 새로고침 뒤 520', j1.get('w') == 520 and u1.get('jww') == 520 and u1.get('jpw') is None and j2.get('w') == 520,
      {'끈 뒤': j1, 'UI': {k: u1.get(k) for k in ('jpw', 'jph', 'jww', 'jwh')}, '새로고침 뒤': j2, '손잡이': g})
    # 폰 390 — 374
    for who, q in (('NEW', p), ('BASE', b)):
        q.ev("o=>__RV.uiSeed(o)", {'jpw': 340, 'jph': 640, 'jww': None, 'jwh': None})
        q.size(390, 844)
        reload_keep(q)
        res[who]['phone'] = open_jp(q)
        q.size(1440, 900)
    T(G, u'폰 390×844 — 창 폭 374(화면 − 16)', (res['NEW']['phone'] or {}).get('w') == 374, res['NEW']['phone'])
    T(G + '-헛', u'헛잣대 바탕 폰 — 340', (res['BASE']['phone'] or {}).get('w') == 340, res['BASE']['phone'])
    for q in (p, b):
        q.ev("o=>__RV.uiSeed(o)", {'jpw': None, 'jph': None, 'jww': None, 'jwh': None})
        q.ev("()=>{S.joPanel=false;S.joPanelW=470;S.joPanelH=640;return 1}")
        close_all(q)


# ══════════ §B-3 빈칸 종류 = 지문 칸마다(A-3) ══════════
Q14 = ['T225914ㄱ', 'T225914ㄴ', 'T225914ㄷ', 'T225914ㄹ', 'T225914ㅁ']


def pick_bk(q, at, v, how):
    q.press(at, how, 900)
    title = q.ev("()=>__RV.bkPopTitle()")
    q.press(q.ev("v=>__UZ.bkPopBtn(v)", v), how, 1000)
    close_all(q)
    return title


def g_r3(p, b, eng):
    G = 'r-3'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        q.size(1440, 900)
        q.ev("()=>__RV.bkClear()"); q.ev("()=>__UZ.bkLoad()")
        home(q)
        g = q.ev("a=>__RV.exvGo(a[0],a[1])", [2022, 14])
        c0 = q.ev("n=>__RV.exvCells(n)", '14') or []
        how = 'mouse' if who == 'NEW' else 'mouse'
        title = pick_bk(q, q.ev("a=>__RV.exvBkAt(a[0],a[1])", ['14', 'T225914ㄷ']), u'내용', how)
        q.ev("a=>__RV.exvGo(a[0],a[1])", [2022, 14])
        c1 = q.ev("n=>__RV.exvCells(n)", '14') or []
        res[who] = {'go': g, 'c0': c0, 'c1': c1, 'rec': q.ev("()=>__RV.bkAll()"), 'title': title, 'want': q.ev("k=>__RV.bkTitleOf(k)", 'T225914ㄷ')}
    n = res['NEW']
    c0 = {c['id']: c for c in n['c0']}; c1 = {c['id']: c for c in n['c1']}
    ok0 = [c0.get(u, {}).get('bk') for u in Q14] == Q14 and [c0.get(u, {}).get('t') for u in Q14] == [u'빈칸?', u'주체', u'빈칸?', u'주체', u'빈칸?']
    T(G, u'기출뷰 2022 14번 — 다섯 칸 data-bk = 저마다 지문 uid · ㄴ·ㄹ = OMR 「주체」 · 나머지 「빈칸?」', ok0, n['c0'])
    ok1 = [c1.get(u, {}).get('t') for u in Q14] == [u'빈칸?', u'주체', u'내용', u'주체', u'빈칸?'] and n['rec'] and list(n['rec'].keys()) == ['T225914ㄷ'] and (n['rec']['T225914ㄷ'] or {}).get('v') == [u'내용']
    T(G, u'ㄷ 칸(「빈칸?」) 누름 → 창 제목 = linkDisp(T225914ㄷ) → 「내용」 → ㄷ 칸만 「내용」(나머지 무변) · 기록 {T225914ㄷ:[내용]} 하나', ok1 and n['title'] and n['title'] == n['want'],
      {'뒤': [[c['id'][-1], c['t']] for c in n['c1']], '기록': n['rec'], '창 제목': n['title'], 'ㄷ 제목': n['want']})
    bb = res['BASE']
    T(G + '-헛', u'헛잣대 바탕 — 다섯 칸 data-bk 모두 T225914ㄱ · 한 칸 누르면 다섯 칸이 다 바뀜', [c.get('bk') for c in bb['c0']] == ['T225914ㄱ'] * 5 and len(set(c.get('t') for c in bb['c1'])) == 1,
      {'data-bk': [c.get('bk') for c in bb['c0']], '뒤': [c.get('t') for c in bb['c1']], '기록': bb['rec']})
    # 1차객 리담 카드 — 지문 열쇠
    want0 = {'TR06154': 'T2461182h', 'T0946022': 'T0946021', 'T2663012': 'T2663011'}
    cards = {}
    for who, q in (('NEW', p), ('BASE', b)):
        q.ev("()=>__RV.bkClear()")
        cards[who] = {}
        for u in want0:
            go_key(q, u)
            cards[who][u] = q.ev("k=>__RV.cardBk(k)", u)
    T(G, u'1차객 리담 카드 TR06154 · T0946022 · T2663012 — data-bk = 제 지문 uid', all((cards['NEW'][u] or {}).get('bk') == u for u in want0), cards['NEW'])
    T(G + '-헛', u'헛잣대 바탕 — data-bk = 문항 첫 지문(T2461182h · T0946021 · T2663011)', all((cards['BASE'][u] or {}).get('bk') == want0[u] for u in want0), cards['BASE'])
    # 바깥 필터 「내용」 — 그 칸이 걸린다. 표본 = 단원 줄(한 지문 = 한 카드)에 있고 조문형인 둘째 이후 지문(미분류 문항 카드는 문항째 거른다)
    cand = None
    for u in ('T0946022', 'TR06154', 'T2663012'):
        sel0 = go_key(p, u)
        ty = p.ev("k=>__RV.typeOf(k)", u) or ''
        if sel0 and sel0.startswith('__mg') and ty.startswith(u'조문형'):
            cand = (u, want0[u], sel0)
            break
    flt = {}
    if cand:
        u, u0, sel0 = cand
        for who, q in (('NEW', p), ('BASE', b)):
            q.ev("()=>__RV.bkClear()")
            s0 = go_key(q, u)
            pick_bk(q, q.ev("k=>__UZ.bkAt(k)", u), u'내용', 'touch')
            home(q, gk=gkOf(q, u))   # 필터 단추는 첫 화면 필터 줄(.mbqr) — 켠 뒤 필터 켜기 전에 잡은 그 단원으로 간다(홈은 필터를 안 건드림)
            q.press(q.ev("()=>__UZ.fbtn()"), 'mouse', 500)
            q.press(q.ev("()=>__UZ.fopt('jo')"), 'mouse', 1200)
            q.press(q.ev("()=>__UZ.fbtn()"), 'mouse', 500)
            q.press(q.ev("()=>__UZ.fbk('내용')"), 'mouse', 1500)
            btn = (q.ev("()=>__UZ.fbtn()") or {}).get('t')
            q.pg.mouse.click(5, 5); q.pg.wait_for_timeout(300)
            q.ev("s=>__HM.go(s)", s0)
            flt[who] = {'sel': s0, u: q.ev("k=>__RV.cardShown(k)", u), u0: q.ev("k=>__RV.cardShown(k)", u0), 'rec': q.ev("()=>__RV.bkAll()"), 'btn': btn, 'S': q.ev("()=>({f:S.oxFilter,bk:S.oxBk})")}
            q.ev("()=>{S.oxFilter='all';S.oxBk=[];return 1}")
            q.ev("()=>__RV.bkClear()")
        T(G, u'%s 카드에서 「내용」(손가락) → 바깥 필터 조문형 · 「내용」 → 그 단원에 %s 걸림(보임) · 기록 = %s 하나' % (u, u, u), flt['NEW'][u] and list((flt['NEW']['rec'] or {}).keys()) == [u], flt['NEW'])
        T(G + '-헛', u'헛잣대 바탕 — 기록이 %s 에 붙어 필터에 %s 가 안 걸림' % (u0, u), not flt['BASE'][u] and list((flt['BASE']['rec'] or {}).keys()) == [u0], flt['BASE'])
    else:
        T(G, u'바깥 필터 표본 — 단원 줄 · 조문형 · 둘째 이후 지문을 못 찾음', False, '')
    home(p); home(b)


# ══════════ §B-4 기출뷰 = 민법 값(A-4) ══════════
SH = 'rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.1) 0px 4px 6px -4px'
MB = {   # 지시서 §0 ④ 표 — 민법(출처 줄) computed 값
    'next': {'fontSize': '12px', 'fontWeight': '700', 'color': 'rgb(75, 85, 99)', 'backgroundColor': 'rgba(0, 0, 0, 0)', 'borderTopWidth': '0px', 'borderTopLeftRadius': '9999px', 'paddingTop': '4px', 'paddingLeft': '8px', 'paddingRight': '8px'},
    'grade': {'fontSize': '12px', 'fontWeight': '800', 'color': 'rgb(59, 130, 246)', 'backgroundColor': 'rgba(0, 0, 0, 0)', 'borderTopWidth': '0px', 'borderTopLeftRadius': '9999px', 'paddingTop': '4px', 'paddingLeft': '8px'},
    'prev': {'fontSize': '12px', 'fontWeight': '700', 'color': 'rgb(75, 85, 99)', 'backgroundColor': 'rgb(255, 255, 255)', 'borderTopWidth': '1px', 'borderTopColor': 'rgb(229, 231, 235)', 'borderTopLeftRadius': '9999px', 'paddingTop': '4px', 'paddingLeft': '12px', 'paddingRight': '12px', 'boxShadow': SH},
    'pill': {'backgroundColor': 'rgb(255, 255, 255)', 'borderTopWidth': '1px', 'borderTopColor': 'rgb(229, 231, 235)', 'borderTopLeftRadius': '9999px', 'paddingTop': '4px', 'paddingRight': '6px', 'paddingBottom': '4px', 'paddingLeft': '12px', 'boxShadow': SH},
    'mk': {'fontSize': '11px', 'fontWeight': '700', 'color': 'rgb(107, 114, 128)'},
    'mkb': {'fontWeight': '900', 'color': 'rgb(107, 114, 128)'},
    'pg': {'fontSize': '11px', 'fontWeight': '700', 'color': 'rgb(55, 65, 81)', 'backgroundColor': 'rgb(243, 244, 246)', 'borderTopWidth': '1px', 'borderTopColor': 'rgb(229, 231, 235)', 'borderTopLeftRadius': '4px', 'paddingTop': '2px', 'paddingLeft': '8px'},
    't2': {'fontSize': '11px', 'fontWeight': '600', 'color': 'rgb(37, 99, 235)'},
    'qtx': {'color': 'rgb(31, 41, 55)'},
}


def css_diff(got, want):
    out = {}
    for k, v in want.items():
        g = (got or {}).get(k)
        if g != v:
            out[k] = [g, v]
    return out


def g_r4(p, b, eng):
    G = 'r-4'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        q.size(1553, 900)
        home(q)
        q.ev("a=>__RV.exvGo(a[0],a[1])", [2026, 6])
        a = q.ev("()=>__RV.exvCss()")
        q.ev("a=>__RV.exvGo(a[0],a[1])", [2026, 999])   # 마지막 쪽 = 「전체 채점 ✓」
        z = q.ev("()=>__RV.exvCss()")
        res[who] = {'a': a, 'z': z}
    n = res['NEW']
    got = {'next': n['a']['next'], 'grade': n['z']['grade'], 'prev': n['a']['prev'], 'pill': n['a']['pill'], 'mk': n['a']['mk'], 'mkb': n['a']['mkb'], 'pg': n['a']['pg'], 't2': n['a']['t2'], 'qtx': n['a']['qtx']}
    for k, lab in (('next', u'「다음 5문제 ▶」'), ('grade', u'「전체 채점 ✓」'), ('prev', u'「◀ 이전」'), ('pill', u'알약 틀'), ('mk', u'「마킹」'), ('mkb', u'마킹 숫자 b'), ('pg', u'범위 칸'), ('t2', u'해 이름 t2'), ('qtx', u'지문 글 색')):
        d = css_diff(got[k], MB[k])
        T(G, u'%s computed = 민법 값(1553px · 2026)' % lab, got[k] is not None and not d, {'다름': d, 'NEW': got[k]})
        bgot = {'next': res['BASE']['a']['next'], 'grade': res['BASE']['z']['grade'], 'prev': res['BASE']['a']['prev'], 'pill': res['BASE']['a']['pill'], 'mk': res['BASE']['a']['mk'], 'mkb': res['BASE']['a']['mkb'],
                'pg': res['BASE']['a']['pg'], 't2': res['BASE']['a']['t2'], 'qtx': res['BASE']['a']['qtx']}[k]
        T(G + '-헛', u'헛잣대 바탕 %s — 민법 값과 다름' % lab, bgot is not None and bool(css_diff(bgot, MB[k])), {'바탕': bgot})   # 없는 요소(None)는 헛패스 — 있는 것을 맞대야 선다
    pa, hd = n['a']['paper'] or {}, n['a']['head'] or {}
    T(G, u'본문 폭 = 896 가운데(시험지 · 머리 줄 · 좌우 틈 같음 ±1)', abs((pa.get('w') or 0) - 896) <= 1 and abs((pa.get('gapL') or 0) - (pa.get('gapR') or 99)) <= 1 and abs((hd.get('w') or 0) - 896) <= 1 and abs((hd.get('gapL') or 0) - (hd.get('gapR') or 99)) <= 1,
      {'시험지': pa, '머리': hd, '알약 오른쪽 틈': n['a']['barR']})
    T(G + '-헛', u'헛잣대 바탕 — 본문 전폭', abs(((res['BASE']['a']['paper'] or {}).get('w') or 0) - 896) > 50, res['BASE']['a']['paper'])
    # 단원 풀이 알약 무변
    up = {}
    for who, q in (('NEW', p), ('BASE', b)):
        q.ev("()=>{S.jtFold=false;return 1}")   # ★ 9/30 A-6 둘째 바퀴 — revfix0929b A-6: r-2 폰 새로고침이 남긴 1차객 서랍 접힘을 편다(바탕 b880a04 는 폰 부팅 접기가 없어 편 채 — 서랍 폭만큼 .mbbar 자리가 갈렸다 · r2 시험지 mainW 새 1540 · 바탕 1281)
        go_key(q, K0)
        up[who] = q.ev("()=>__RV.unitPill()")
    T(G, u'단원 풀이 알약(채점 ✓ · 마킹 · ◀ 이전) computed = 바탕 그대로', up['NEW'] and up['NEW']['pill'] and up['NEW'] == up['BASE'], {'NEW': up['NEW'], '다름': {k: [up['NEW'].get(k), up['BASE'].get(k)] for k in up['NEW'] if up['NEW'].get(k) != up['BASE'].get(k)} if up['NEW'] else None})
    # 서랍 해 머리 · 회차 줄
    dr = {}
    for who, q in (('NEW', p), ('BASE', b)):
        q.ev("()=>{S.jtFold=false;return 1}")   # ★ 9/30 A-6 — revfix0929b A-6: r-2 폰(390) 새로고침이 폰 부팅 규칙으로 1차객 서랍을 접어 둔 채 돌아온다(r-7 treeHid 푸는 줄과 같은 까닭) — 편 서랍을 잰다
        home(q)
        q.ev("a=>__RV.exvGo(a[0],a[1])", [2026, 1])
        dr[who] = q.ev("()=>__RV.gy()")
    d = dr['NEW']; bd = dr['BASE']
    nb = len(bd['base'])
    cur = [x for x in d['items'] if x['cur']]
    curh = [x for x in d['heads'] if x['cur']]
    T(G, u'서랍 「변리사 기출」 — 해 머리 줄 수 = 회차 줄 수 = 바탕 해 줄 수(%d) · 해 머리 「▾ 2026년 제63회 · 수」' % nb, nb > 0 and len(d['heads']) == len(d['items']) == nb and d['heads'][0]['t'].startswith(u'▾') and u'2026년' in d['heads'][0]['t'],
      {'머리': [h['t'] for h in d['heads'][:3]], '회차': [x['t'] for x in d['items'][:3]], '바탕': [x['t'] for x in bd['base'][:3]]})
    hc = (curh[0] if curh else {}) or {}
    ic = (cur[0] if cur else {}) or {}
    okh = hc and hc['cs']['fontSize'] == '12px' and hc['cs']['fontWeight'] == '800' and hc['cs']['color'] == 'rgb(29, 78, 216)' and hc['cs']['backgroundColor'] == 'rgb(249, 250, 251)' \
        and hc['cs']['paddingTop'] == '4px' and hc['cs']['paddingLeft'] == '10px' and hc['cs']['marginTop'] == '5px' and abs(hc['cs']['h'] - 26) <= 0.6 \
        and (hc['n'] or {}).get('fontSize') == '10px' and (hc['n'] or {}).get('fontWeight') == '700' and (hc['n'] or {}).get('color') == 'rgb(156, 163, 175)'
    T(G, u'해 머리(지금 해) = 민법 .trch — 12px 800 #1d4ed8 · 바탕 #f9fafb · 4/10px · 높이 26 · margin-top 5 · 수 10px 700 #9ca3af', bool(okh), hc)
    oki = ic and ic['order'][:3] == ['now', 'tx', 'n'] and ic['cs']['paddingTop'] == '3px' and ic['cs']['paddingLeft'] == '20px' and ic['cs']['paddingRight'] == '10px' and ic['cs']['backgroundColor'] == 'rgb(239, 246, 255)' \
        and ic['cs']['borderLeftWidth'] == '3px' and ic['cs']['borderLeftColor'] == 'rgb(37, 99, 235)' and abs(ic['cs']['h'] - 30) <= 0.6 \
        and (ic['now'] or {}).get('fontSize') == '9px' and (ic['now'] or {}).get('fontWeight') == '800' and (ic['now'] or {}).get('color') == 'rgb(255, 255, 255)' and (ic['now'] or {}).get('backgroundColor') == 'rgb(37, 99, 235)' \
        and (ic['now'] or {}).get('borderTopLeftRadius') == '3px' and (ic['now'] or {}).get('paddingLeft') == '3px' \
        and (ic['tx'] or {}).get('fontSize') == '12px' and (ic['tx'] or {}).get('color') == 'rgb(55, 65, 81)' and (ic['n'] or {}).get('fontSize') == '10px' and (ic['n'] or {}).get('fontWeight') == '700' and (ic['n'] or {}).get('color') == 'rgb(107, 114, 128)' \
        and re.match(r'^\d+/\d+$', ic.get('nT') or '') and ic['bar']
    T(G, u'회차 줄(지금 해) = 민법 .trit — 차례 「지금」 → 이름 → 「0/n」 · 3/10/3/20px · 바탕 #eff6ff · 왼쪽 테 3px #2563eb · 높이 30 · 지금 9px 800 흰/#2563eb r3 · 이름 12px #374151 · 수 10px 700 #6b7280 · 막대', bool(oki), ic)
    bcur = [x for x in bd['base'] if x['cur']]
    T(G + '-헛', u'헛잣대 바탕 — 해 머리 줄 없음 · 「지금」 이 수 뒤', not bd['heads'] and bool(bcur) and bcur[0]['order'][-1:] == ['now'], {'바탕 지금 줄': bcur[:1]})
    # 누름 — 해 머리 = 접기/펴기 · 회차 줄 = 그 해
    q = p
    y2 = d['items'][1]['y'] if len(d['items']) > 1 else None
    q.press(q.ev("y=>__RV.gyHeadAt(y)", '2026'), 'mouse', 900)
    f1 = q.ev("()=>__RV.gy()"); s1 = q.ev("()=>__RV.state()")
    q.press(q.ev("y=>__RV.gyHeadAt(y)", '2026'), 'touch', 900)
    f2 = q.ev("()=>__RV.gy()")
    q.press(q.ev("y=>__RV.gyRowAt(y)", y2), 'touch', 1500)
    s3 = q.ev("()=>__RV.state()"); p3 = q.ev("()=>document.querySelector('.exv-paper.uzexv')?document.querySelector('.exv-paper.uzexv').dataset.uzexv:null")
    ok = len(f1['items']) == len(d['items']) - 1 and not any(x['y'] == '2026' for x in f1['items']) and f1['heads'][0]['t'].startswith(u'▸') and 'gy2026' in (s1.get('jtCh') or '') \
        and len(f2['items']) == len(d['items']) and f2['heads'][0]['t'].startswith(u'▾') and s3.get('year') == y2 and p3 == y2
    T(G, u'해 머리 누름(마우스) = 접기(그 해 회차 줄 숨음 · ▸ · jt_ch 기억) · 다시(손가락) = 펴기 · 회차 줄 누름(손가락) = 그 해 기출뷰(%s)' % y2, ok,
      {'접은 뒤': [len(f1['items']), f1['heads'][0]['t'] if f1['heads'] else None, s1.get('jtCh')], '편 뒤': len(f2['items']), '누른 뒤': [s3, p3]})
    p.ev("()=>{S.jtCh={};return 1}"); b.ev("()=>{S.jtCh={};return 1}")
    for q in (p, b):
        q.size(1440, 900); home(q)


# ══════════ §B-5 조 패널 카드 칩(A-5) ══════════
def g_r5(br, eng):
    G = 'r-5'
    (ns, nd, ne), (bs, bd, be) = envs()
    res = {}
    for who, (src, data, exam) in (('NEW', (ns, nd, ne)), ('BASE', (bs, bd, be))):
        q = Pg(br, eng, 'r5' + who, src, data, exam, W=1440, H=900)
        try:
            boot = {'tab': q.ev("()=>S.tab"), 'mln': q.ev("()=>__RV.mln()")}
            if boot['mln'].get('ok'):   # 새로 열기 = 1차객을 안 거친 상태(첫 탭이 1차객이면 MLN 을 비워 흉내)
                q.ev("()=>{MLN={ok:false};return 1}")
            go_jo(q, u'특허법', u'제140조')
            q.press(q.J("()=>__WM.jpChip()"), 'mouse', 2500)
            m1 = q.ev("()=>__RV.mln()")
            t0 = time.time()
            A = q.pg.evaluate("()=>__RV.chipCensus()")
            ta = time.time() - t0
            # 표본(창에서) — TR0304가 출제연도 칩 · 1차객 가기 전
            sid = 'TR0304가'
            k = next((x.split('|')[0] for x in (A.get('sig') or {}) if x.endswith('|' + sid)), None)
            yc = None
            if k:
                q.ev("a=>__JS.jo('특허법',a,{panel:true})", k)
                pg_ = q.ev("s=>__JS.pageOf(s)", sid)
                yc = q.ev("s=>__RV.cardYearChips(s)", sid)
            q.ev("l=>__JS.gaekHome(l)", u'특허법')
            m2 = q.ev("()=>__RV.mln()")
            go_jo(q, u'특허법', u'제140조')
            B = q.pg.evaluate("()=>__RV.chipCensus()")
            res[who] = {'boot': boot, 'm1': m1, 'm2': m2, 'A': A, 'B': B, 'k': k, 'yc': yc, 'ta': round(ta, 1), 'errs': q.errs_all()[:4]}
        finally:
            q.close()
    for who in ('NEW', 'BASE'):
        r = res[who]
        sa, sb = (r['A'] or {}).get('sig') or {}, (r['B'] or {}).get('sig') or {}
        diff = [x for x in sb if sa.get(x) != sb.get(x)]
        r['diff'] = diff
        r['ex'] = [[x, (sa.get(x) or '')[:70], (sb.get(x) or '')[:70]] for x in diff[:3]]
    n, bb = res['NEW'], res['BASE']
    T(G, u'새로 열기 → 조문 탭 → ☑ 정오문제(마우스) → MLN 준비(특허) · 특허 전 조 카드 머리 = 1차객 다녀온 뒤 값 · 어긋남 0 (카드 %d · 조 %d)' % ((n['B'] or {}).get('n', 0), (n['B'] or {}).get('jo', 0)),
      n['m1'].get('ok') and n['m1'].get('subj') == u'특허' and (n['B'] or {}).get('n', 0) > 3000 and not n['diff'] and len((n['A'] or {}).get('sig') or {}) == len((n['B'] or {}).get('sig') or {}),
      {'부팅': n['boot'], '창 연 뒤 MLN': n['m1'], '어긋남': len(n['diff']), '보기': n['ex'], '잰 시간': n['ta'], '오류': n['errs']})
    T(G + '-헛', u'헛잣대 바탕 — 어긋남 %d(채팅 478)' % len(bb['diff']), len(bb['diff']) > 100, {'어긋남': len(bb['diff']), '보기': bb['ex'], '창 연 뒤 MLN': bb['m1']})
    sa = (n['A'] or {}).get('sig') or {}
    th = next((v for x, v in sa.items() if x.endswith('|TH040743')), None)
    tb = next((v for x, v in sa.items() if x.endswith('|T2259011r')), None)
    T(G, u'표본(1차객 가기 전) — TR0304가 출제연도 칩 하나(창에서) · TH040743 「🔗 판 1」 · T2259011r 「📖 본문」', n['yc'] is not None and len(n['yc']) == 1 and th and u'🔗 판 1' in th and tb and u'📖 본문' in tb,
      {'TR0304가': [n['k'], n['yc']], 'TH040743': (th or '')[:90], 'T2259011r': (tb or '')[:90]})
    sb0 = (bb['A'] or {}).get('sig') or {}
    bth = next((v for x, v in sb0.items() if x.endswith('|TH040743')), None)
    T(G + '-헛', u'헛잣대 바탕 — TR0304가 칩 둘 · TH040743 「🔗 판」 없음', (bb['yc'] is not None and len(bb['yc']) >= 2) and not (bth and u'🔗 판' in bth), {'TR0304가': bb['yc'], 'TH040743': (bth or '')[:90]})


# ══════════ §B-6 3법 칸 자리(A-6) ══════════
def g_r6(p, b, eng):
    G = 'r-6'
    res = {}
    hows = ('mouse', 'finger', 'pen') if eng == 'chromium' else ('mouse',)
    for who, q in (('NEW', p), ('BASE', b)):
        q.size(1280, 1000)
        res[who] = {}
        for how in hows:
            q.ev("()=>__JS.jo('특허법','제1조',{panel:false})")
            if not q.ev("()=>{const w=__JS.c3();return !!(w&&w.cols&&w.cols.length)}"):
                q.click(q.ev("()=>__JS.c3fold()"), 900)
            h = q.ev("()=>__JS.c3headAt('상표')")
            if not h:
                res[who][how] = None
                continue
            if how == 'mouse':
                q.hold(h['px'], h['py'], 600)
            elif how == 'finger':
                q.finger(h['px'], h['py'], 600)
            else:
                q.pen(h['px'], h['py'], 600)
            res[who][how] = q.ev("()=>__RV.c3pick()")
        q.size(1440, 900)
    ok = all(v and v['vis'] and v['law'] == u'상표법' and v['afterCard'] and not v['inCard'] and v['below'] and v['inp'] for v in res['NEW'].values())
    T(G, u'3법 상표 카드 머리 600ms(%s) → 조·항 칸 = 카드(.thcol) 바로 뒤 제 줄 · 칸 위 끝 ≥ 카드 아래 끝 · 입력 칸' % '·'.join(hows), ok, res['NEW'])
    T(G + '-헛', u'헛잣대 바탕 — 칸이 카드 안(머리와 본문 사이)', all(v and v['inCard'] and not v['below'] for v in res['BASE'].values()), res['BASE'])
    if eng != 'chromium':
        N(G, u'WebKit — 손가락·펜 길게 누르기는 CDP 가 없어 마우스만(크로미움에서 셋 다 잼)', '')


# ══════════ §B-7 서랍 이름(A-7) ══════════
def names_stat(r):
    rows = (r or {}).get('rows') or []
    by = {x['k']: x for x in rows}
    return {'n': len(rows), 'avg': round(sum(x['cw'] for x in rows) / max(1, len(rows)), 1), 'ell': sum(1 for x in rows if x['sw'] > x['cw'] + 1),
            'pClip': sum(1 for x in rows if x['pClip']), 'j2': [by.get(u'제2조', {}).get('cw'), by.get(u'제2조', {}).get('sw')], 'j14': [by.get(u'제14조', {}).get('cw'), by.get(u'제14조', {}).get('sw')],
            'em': sorted(set(x['em'] for x in rows if x['em'])), 'shr': sum(1 for x in rows if x['st'] and 'jsshr' in x['st']['cls'])}


def g_r7(p, b, eng):
    G = 'r-7'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        q.size(1440, 1000)
        q.ev("()=>{S.treeHid=false;S.listHid=false;return 1}")   # r2 폰 새로고침이 서랍을 접은 채로 남긴다(폰 시작값 treeHid) — 편 서랍을 잰다
        res[who] = {}
        for w in (212, 260, 320):
            q.ev("w=>__JS.jo('특허법','제1조',{panel:false,treeW:w})", w)
            res[who][w] = q.ev("()=>__RV.names()")
        q.ev("()=>{S.treeW=212;return 1}")
        q.size(1440, 900)
    n2, b2 = names_stat(res['NEW'][212]), names_stat(res['BASE'][212])
    # ★ 9/30 A-6 둘째 바퀴 — joscreen0929 A-1: 줄 끝 jcol3 = [빈칸 점][체크 단추](✏️M·🔗L 걷음 · CSS grid 30px 44px + 틈 4 = 78 · 넓은 서랍 .wide 44px 44px = 92) — 바탕 b880a04 의 세 칸(30·30·26 + 틈 = 94)과 맞대지 않고 새 틀 폭 한 자리로 잰다
    T(G, u'212px 서랍 — 제2조 정의 이름 다 보임(64/64) · 제14조 ≥ 56 · 조 번호까지 가려진 줄 ≤ 5 · 오른쪽 두 칸(빈칸 점 · 체크) 폭 78 한 자리',
      n2['j2'][0] is not None and n2['j2'][0] >= n2['j2'][1] - 1 and (n2['j14'][0] or 0) >= 56 and n2['pClip'] <= 5 and n2['em'] == [78] and n2['n'] == b2['n'],
      {'NEW': n2, '바탕': b2})
    T(G + '-헛', u'헛잣대 바탕 212 — 제2조 이름 잘림 · 조 번호 가려진 줄 > 5', b2['j2'][0] is not None and b2['j2'][0] < b2['j2'][1] - 1 and b2['pClip'] > 5, b2)
    for w in (260, 320):
        a, c = res['NEW'][w], res['BASE'][w]
        # ★ 9/30 A-6 둘째 바퀴 — 뒤 판이 줄 꼴을 바꿈: joscreen0929 A-1 줄 끝 두 칸(폭 78 · 넓은 서랍 92 · 이름 칸 +16) · revfix0928pm A-5 이름 = 번호(.jno) + 이름(.jtt 말줄임) 격자(span.nm 이 안 넘쳐 sw = cw) — 줄마다 이름 칸은 바탕보다 안 좁고 · ★ 개정일 칸 = 바탕 · 오른쪽 칸 = 새 틀 폭 한 자리
        emw = 92 if w >= 300 else 78
        same = [x for x, y in zip(a['rows'], c['rows']) if x['t'] != y['t'] or x['cw'] < y['cw'] - 1 or (x['st'] or {}).get('cw') != (y['st'] or {}).get('cw') or x['em'] != emw]
        T(G, u'%dpx 서랍 — 줄마다 이름 칸 ≥ 바탕 · ★ 개정일 칸 = 바탕 · 오른쪽 두 칸(빈칸 점 · 체크) 폭 %d 한 자리' % (w, emw), a['n'] == c['n'] and not same and names_stat(a)['shr'] == 0, {'줄': a['n'], '다름': same[:3], 'NEW': names_stat(a)})


BR = {}
PARTS = [('r1', g_r1), ('r2', g_r2), ('r3', g_r3), ('r4', g_r4), ('r6', g_r6), ('r7', g_r7)]


def run_engine(pw, eng):
    br = getattr(pw, eng).launch()
    BR[eng] = br
    try:
        if not ONLY or 'r5' in ONLY:
            print('── %s · r5' % eng, flush=True)
            try:
                g_r5(br, eng)
            except Exception as e:
                T('RUN', u'%s · r5 묶음이 멈춤' % eng, False, repr(e)[:600])
        (ns, nd, ne), (bs, bd, be) = envs()
        p = Pg(br, eng, 'rvN', ns, nd, ne)
        b = Pg(br, eng, 'rvB', bs, bd, be)
        try:
            N('boot', eng, {'NEW': p.ev("()=>__RV.cfBoot()"), 'BASE': b.ev("()=>__RV.cfBoot()")})
            for k, fn in PARTS:
                if ONLY and k not in ONLY:
                    continue
                print('── %s · %s' % (eng, k), flush=True)
                try:
                    fn(p, b, eng)
                except Exception as e:
                    T('RUN', u'%s · %s 묶음이 멈춤' % (eng, k), False, repr(e)[:600])
            T('ERR', u'%s — NEW 앱 오류 0' % eng, not p.errs_all(), p.errs_all()[:6])
        finally:
            p.close(); b.close()
    finally:
        br.close()


def main():
    os.makedirs(M.WORK, exist_ok=True)
    t0 = time.time()
    with sync_playwright() as pw:
        for eng in ENGS:
            RES.append(('ENG', eng, None, ''))
            print('INFO | ENG · %s |' % eng, flush=True)
            run_engine(pw, eng)
    npass = sum(1 for r in RES if r[2] is True); nfail = sum(1 for r in RES if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · %s · NEW %s · 데이터 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), 'revfix0928', os.path.basename(_NEW), _DATA, ','.join(ENGS)))
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[ok], g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:700]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
