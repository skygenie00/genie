# -*- coding: utf-8 -*-
r"""_task_jo_revfix0928 §B(9/28) 관문 하네스 — 연결 창 · 정오문제 창 처음 크기 · 빈칸 종류 칸 · 기출뷰 = 민법 값 · 조 패널 카드 칩 · 3법 칸 자리 · 서랍 이름.

  python _harness_jo_revfix0928.py --new <앱> --data <jo/data> [--exam <gichul/pdf>] [--only r1,r2,...] [--eng chromium,webkit] [--res <결과 파일>]

  NEW  = 이 판 앱 + 데이터 · BASE = genie HEAD(바로 앞 인도판 = jo_wonmun b880a04) 앱 + HEAD 데이터 — 칸마다 헛잣대(바탕에서 FAIL)
  누름 = 진짜 포인터(page.mouse · 손가락 = Chromium CDP 터치 r22 · WebKit touchscreen.tap · 펜 = CDP pointerType pen) · 보임 = display ≠ none · 높이 > 0 · 자리 = elementFromPoint
  틀 = mbsame 하네스(_harness_jo_gaek_mbsame.py)의 serve·Pg·__HM · uidmbs2 도구(__UZ) · cardfix 도구(__CF) · joscreen 도구(__JS) · wonmun 도구(__WM) · 이 판 도구(__RV).
  민법 값 = 지시서 §0 ④ 표(채팅 실측 · 민법 1553px 2026)를 고정 잣대로 쓴다.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402 — _task_qa_slim(10/4) A-1·A-2·A-3: --mode gate|regress|smoke(인자 없으면 gate = 이 판 앞과 같음) · regress = NEW 한 쪽만 띄움(바탕 b880a04 안 풀고 안 띄움 · r-5 도 그 한 쪽에서) · 조 패널 표본 · 앱 표지 기다림
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


def _settle(q, wait, js=None, what='', arg=None, ms=None):
    """regress 의 기다림(_task_qa_slim A-2) — 앱 표지(js)가 서면 바로(못 서면 ms · 기본 max(2×옛 대기, 3초) 뒤 그대로 잰다) + 브라우저 두 프레임(ResizeObserver · rAF 로 미룬 자리 맞춤이 끝나는 한 박자 —
    시간이 아니라 프레임 · 앱 표지 아님 · 하네스 쪽) · 표지(js)가 없으면 QJ.sleep(옛 대기, 까닭, page) = 고정 대기를 남기고 까닭을 적는다(page 를 넘겨 그동안 route · 요청이 돈다) ·
    환경변수 QA_SLIM_FIXED=W3,W7 (또는 all) 이면 그 자리는 옛 고정 대기 그대로(흔들림 때 그 자리만 되돌리는 길 · what 첫 낱말 = Wn) · gate 는 안 부른다(호출 자리가 `원본 if QJ.GATE else _settle(…)` 꼴)"""
    fixed = [x for x in os.environ.get('QA_SLIM_FIXED', '').split(',') if x]
    if not js or 'all' in fixed or (what or '').split(' ')[0] in fixed:
        QJ.sleep(wait, what or '고정 대기 남김 — 앱 표지 없음', q.pg)
        return
    QJ.until(q.pg, js, ms or max(2 * wait, 3000), what, arg)
    try:
        q.pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
    except Exception:
        pass


def _press(q, at, how, wait, js=None, what='', arg=None, ms=None):
    """regress — q.press 와 같은 누름인데 뒤 기다림을 표지로(_settle)"""
    ok = q.tap(at, 0) if how == 'touch' else q.click(at, 0)
    if ok:
        _settle(q, wait, js, what, arg, ms)
    return ok


def _clk(q, at, wait, js=None, what='', arg=None, ms=None):
    """regress — q.click 과 같은 누름인데 뒤 기다림을 표지로(_settle)"""
    ok = q.click(at, 0)
    if ok:
        _settle(q, wait, js, what, arg, ms)
    return ok


def _hold(q, x, y, ms, wait, js=None, what='', arg=None):
    """regress — q.hold 와 같은 길게 누름(ms = 앱의 길게 누름 문턱 · 고정 대기 아님) · 뒤 기다림을 표지로"""
    q.hold(x, y, ms, 0)
    _settle(q, wait, js, what, arg)


def _finger(q, x, y, ms, wait, js=None, what='', arg=None):
    q.finger(x, y, ms, 0)
    _settle(q, wait, js, what, arg)


def _pen(q, x, y, ms, wait, js=None, what='', arg=None):
    q.pen(x, y, ms, 0)
    _settle(q, wait, js, what, arg)


def _drag(q, at, dx, dy, how='mouse', js=None, what='', arg=None):
    """regress — q.drag 와 같은 손잡이 끌기(마우스) · 끝 기다림(옛 500ms)을 표지로"""
    if not at or not at.get('on'):
        return False
    q.pg.mouse.move(at['cx'], at['cy']); q.pg.mouse.down()
    q.pg.mouse.move(at['cx'] + dx / 2, at['cy'] + dy / 2, steps=4); q.pg.mouse.move(at['cx'] + dx, at['cy'] + dy, steps=4)
    q.pg.mouse.up(); _settle(q, 500, js, what, arg)
    return True


def _size(q, W, H):
    """regress — q.size 와 같은 폭 바꾸기 · 뒤 기다림(옛 300ms)은 프레임만(다음 줄이 새로 그리거나 연다)"""
    q.pg.set_viewport_size({'width': W, 'height': H})
    _settle(q, 300, "()=>true", 'W3 폭을 바꾼 뒤 — 다음 줄이 새로 그리거나 연다(앱 표지 불필요) · 브라우저 두 프레임만')


# ══════════ A-2 앱 표지(JS) — 목록 · 뜻 · 앱 코드 자리 = R\_qa_slim_out\_a2\_harness_jo_revfix0928_표지.md ══════════
JS_IDLE = "()=>typeof busy==='undefined'||!busy"
JS_BOOTED = "()=>typeof busy!=='undefined'&&!busy&&!!document.querySelector('#slot')&&document.querySelector('#slot').children.length>0"
JS_CFWIN = "()=>(typeof POPS!=='undefined'?POPS:[]).some(p=>p.isConnected&&p._cflw)"
JS_CFFOCUS = "()=>{const w=(typeof POPS!=='undefined'?POPS:[]).filter(p=>p.isConnected&&p._cflw).pop();const i=w&&w.querySelector('input');return !!i&&document.activeElement===i}"
JS_CFROWS = "()=>{const w=(typeof POPS!=='undefined'?POPS:[]).filter(p=>p.isConnected&&p._cflw).pop();return !!w&&w.querySelectorAll('.cfrs .cfr').length>0}"
JS_LK2 = "k=>{try{const l=__CF.lk(k);return !!l&&(l.my||[]).length>=2}catch(e){return false}}"
JS_JPWIN = "()=>!!document.querySelector('.pop.wm-jp')"
JS_JW = "()=>{try{const u=JSON.parse(localStorage.getItem('jopangi_ui')||'{}');return u.jww===520}catch(e){return false}}"
JS_BKPOP = r"()=>(typeof POPS!=='undefined'?POPS:[]).some(x=>/빈칸 종류 확정/.test(x._pk||''))"
JS_FMENU = "()=>!!document.querySelector('#slot .mbqr .uzfm')"
JS_FMENU_BK = "()=>!!document.querySelector('#slot .mbqr .uzfm .uzfc')"
JS_FMENU_GONE = "()=>!document.querySelector('#slot .mbqr .uzfm')"
JS_FJO = "()=>S.oxFilter==='jo'&&(typeof busy==='undefined'||!busy)"
JS_FBK = "()=>(S.oxBk||[]).indexOf('내용')>=0&&(typeof busy==='undefined'||!busy)"
JS_GYFOLD = "()=>!!(S.jtCh&&S.jtCh['gy2026'])"
JS_GYOPEN = "()=>!(S.jtCh&&S.jtCh['gy2026'])"
JS_GYYEAR = "y=>{const e=document.querySelector('.exv-paper.uzexv');return !!e&&e.dataset.uzexv===String(y)}"
JS_C3PICK = "()=>!!document.querySelector('#slot .c3pick')"
JS_MLN = "()=>{try{return !!MLN&&!!MLN.ok&&MLN._subj==='특허'}catch(e){return false}}"
JS_C3COLS = "()=>{const w=__JS.c3();return !!(w&&w.cols&&w.cols.length)}"
R5_IDX_JS = "async()=>{const JP=await joPanelIdx();const o={};for(const k of Object.keys(JP||{}).sort()){let r=null;try{r=jsPanelItems(JP[k],k).map(x=>x.sid)}catch(e){continue}o[k]=r}return o}"
R5_SUB_JS = """async (keep) => { const f = window.joPanelIdx;
  window.joPanelIdx = async function(){ const JP = await f.apply(this, arguments); const o = {}; (keep || []).forEach(k => { if (JP && (k in JP)) o[k] = JP[k]; }); return o; };
  try { return await __RV.chipCensus(); } finally { window.joPanelIdx = f; } }"""


def envs():
    if QJ.REGRESS:   # regress(_task_qa_slim A-1) — 바탕 b880a04 앱·데이터를 풀지 않는다(git show · git archive 0 · 바탕 Pg 도 안 띄움)
        return M.new_env(), (None, None, None)
    QJ.sub('git:show-app'); QJ.sub('git:archive')   # 셈(§B-4) — M.base_env 가 부르는 둘(gate 에서도 동작 무변)
    return M.new_env(), M.base_env()


def reload_keep(q):
    q.pg.goto('http://127.0.0.1:%d/index.html?tok=1&keep=1' % q.port, wait_until='load', timeout=180000)
    q.pg.wait_for_function(M.READY, timeout=180000); (q.pg.wait_for_timeout(700) if QJ.GATE else _settle(q, 700, JS_BOOTED, 'W13 첫 render 끝 — busy 가 풀리고 #slot 이 찼다'))


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
    (q.pg.wait_for_timeout(250) if QJ.GATE else _settle(q, 250, "k=>[...document.querySelectorAll('.qb.id')].some(b=>(b.textContent||'').trim()===k)", 'W23 그 카드 칸(.qb.id)이 섰다', k))
    return sel


def go_jo(q, law, jo):
    q.ev("a=>__WM.go(a[0],a[1])", [law, jo])
    (q.pg.wait_for_timeout(300) if QJ.GATE else _settle(q, 300, "()=>true", 'W24 __WM.go 가 render() 를 기다린 뒤라 따로 표지 불필요 · 브라우저 두 프레임만'))


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
    (q.press(at, how, 900) if QJ.GATE else _press(q, at, how, 900, JS_CFWIN, 'W14 연결 창(POPS · p._cflw)이 섰다'))
    w0 = q.ev("()=>__RV.cf()")
    (q.press(q.ev("()=>__RV.cfInp()"), how, 300) if QJ.GATE else _press(q, q.ev("()=>__RV.cfInp()"), how, 300, JS_CFFOCUS, 'W15 창 안 찾기 칸(input)에 초점'))
    q.pg.keyboard.type(u'조문', delay=40)
    (q.pg.wait_for_timeout(700) if QJ.GATE else _settle(q, 700, JS_CFROWS, 'W16 결과 줄(.cfrs .cfr)이 섰다 — 120ms 디바운스 뒤 paintFind'))
    w1 = {}
    for _ in range(25):   # 다른 두 법 데이터가 붙으면 결과가 다시 그려진다(S1855224 = 상표)
        w1 = q.ev("()=>__RV.cf()")
        if 'S1855224' in (w1.get('uids') or []):
            break
        q.pg.wait_for_timeout(300)
    (q.pg.wait_for_timeout(500) if QJ.GATE else _settle(q, 500, "()=>true", 'W18 결과를 그린 뒤 cfFit 다시 맞춤(ResizeObserver → rAF) — 위 S1855224 폴링이 그린 뒤를 보장 · 브라우저 프레임만'))   # 결과를 그린 뒤 다시 맞춤(ResizeObserver → rAF)
    w1 = q.ev("()=>__RV.cf()")
    reach1 = q.ev("()=>__RV.cfReach()")
    r0 = q.ev("()=>__RV.cfRow0()")
    pressed = (q.press(r0, how, 1300) if QJ.GATE else _press(q, r0, how, 1300, JS_LK2, 'W19 연결이 걸렸다(__CF.lk(K0).my ≥ 2) — 뒤 cfFit 은 프레임', K0))
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
    for vp, W, H, how in (VPS[:1] if QJ.SMOKE else VPS):   # smoke — 폰 390×844(손가락)만
        res = {}
        for who, q in (('NEW', p), ('BASE', b)) if QJ.GATE else (('NEW', p),):   # regress — NEW 만
            (q.size(W, H) if QJ.GATE else _size(q, W, H))
            if who == 'NEW':   # ★ 9/30 A-6 — revfix0929b A-6: 폰(≤480) 부팅 = 1차객 서랍 접힌 채 · 펼친 폰 서랍 바깥 첫 누름은 접기만(DRAWER_EAT) → PC 로 연 판을 줄였으니 폰은 부팅처럼 접고 PC·아이패드는 인도 때처럼 편다
                q.ev("w=>{S.jtFold=w<=480;return 1}", W)
            res[who] = cf_flow(q, how)
        ok, part = cf_ok(res['NEW'])
        n = res['NEW']
        T(G, u'%s %d×%d(%s) — 카드 ✏️ → 「조문」 → 창 위·아래 끝 화면 안(8px) · 결과 첫 줄 보임 · 걸린 연결·안내 줄 닿음(몸 굴림) · 결과 줄 누름 → 연결 · 창 여전히 화면 안' % (vp, W, H, u'손가락' if how == 'touch' else u'마우스'), ok,
          {'부분': part, '창': (n['w1'] or {}).get('W'), 'max-height': (n['w1'] or {}).get('mh'), '결과': (n['w1'] or {}).get('rowsN'), '첫 줄': (n['w1'] or {}).get('row0'), '누른 뒤 창': (n['w2'] or {}).get('W'), '연결': n['lk'], '오류': n['errs']})
        if QJ.GATE:   # 헛잣대(처리안 관문만) — regress 에서 끔
            bok, bpart = cf_ok(res['BASE'])
            bw = res['BASE']['w1'] or {}
            det = {'부분': bpart, '창': bw.get('W'), 'max-height': bw.get('mh'), '계산 max-height': bw.get('cmh'), '첫 줄': bw.get('row0')}
            if vp == u'폰':
                T(G + '-헛', u'헛잣대 바탕 폰 — 창 max-height 120px · 결과 첫 줄이 창 밖', not bok and bw.get('mh') == '120px' and not (bw.get('row0') or {}).get('seen'), det)
            elif vp == 'PC':
                T(G + '-헛', u'헛잣대 바탕 PC — 「조문」 친 뒤 창 아래 끝이 화면(900) 밖', not bok and ((bw.get('W') or {}).get('b') or 0) > H - 8 + 1, det)
            else:
                N(G + '-헛', u'바탕 아이패드(지시서 헛잣대 없음 — 값만)', det)
    (p.size(1440, 900) if QJ.GATE else _size(p, 1440, 900))
    if QJ.GATE:
        (b.size(1440, 900) if QJ.GATE else _size(b, 1440, 900))


# ══════════ §B-2 정오문제 창 처음 크기(A-2) ══════════
def open_jp(q):
    close_all(q)
    q.ev("()=>{S.joPanel=false;return 1}")
    go_jo(q, u'특허법', u'제140조')
    (q.press(q.J("()=>__WM.jpChip()"), 'mouse', 1600) if QJ.GATE else _press(q, q.J("()=>__WM.jpChip()"), 'mouse', 1600, JS_JPWIN, 'W25 정오문제 창(.pop.wm-jp)이 섰다'))
    return q.ev("()=>__RV.jp()")


def g_r2(p, b, eng):
    G = 'r-2'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)) if QJ.GATE else (('NEW', p),):   # regress — NEW 만
        (q.size(1280, 900) if QJ.GATE else _size(q, 1280, 900))
        q.ev("o=>__RV.uiSeed(o)", {'jpw': 340, 'jph': 640, 'jww': None, 'jwh': None})
        reload_keep(q)
        res[who] = {'ui0': q.ev("()=>__RV.ui()"), 'jp': open_jp(q)}
    n, bb = res['NEW']['jp'], (res['BASE']['jp'] if QJ.GATE else None)   # regress — 바탕 칸은 헛잣대뿐(관문만)
    T(G, u'옛 판 UI 기록 {jpw:340} 심고 새로고침 → ☑ 정오문제 창 = 470×640', n.get('win') and n.get('w') == 470 and n.get('h') == 640, {'NEW': n, '심은 UI': {k: (res['NEW']['ui0'] or {}).get(k) for k in ('jpw', 'jph', 'jww', 'jwh')}})
    if QJ.GATE:   # 헛잣대(처리안 관문만) — regress 에서 끔
        T(G + '-헛', u'헛잣대 바탕 — 340 폭(옛 패널 키 jpw 를 읽는다)', bb.get('win') and bb.get('w') == 340, bb)
    # 손잡이 +50 → 520 → 새로고침 520(창 오른쪽에 50px 넘는 자리가 있게 폭 1600)
    (p.size(1600, 900) if QJ.GATE else _size(p, 1600, 900))
    open_jp(p)
    g = p.ev("()=>__RV.jpGrip()")
    (p.drag(g, 50, 0) if QJ.GATE else _drag(p, g, 50, 0, 'mouse', JS_JW, 'W20 끈 폭(470+50)이 UI 기록에 저장됐다(jopangi_ui.jww === 520 — 처음 열 때 쓴 옛 값 470 과 구별)'))
    j1 = p.ev("()=>__RV.jp()")
    u1 = p.ev("()=>__RV.ui()") or {}
    reload_keep(p)
    j2 = open_jp(p)
    T(G, u'손잡이 +50 → 520 · UI 기록 jww 520(옛 jpw 칸은 이 저장에서 사라짐) → 새로고침 뒤 520', j1.get('w') == 520 and u1.get('jww') == 520 and u1.get('jpw') is None and j2.get('w') == 520,
      {'끈 뒤': j1, 'UI': {k: u1.get(k) for k in ('jpw', 'jph', 'jww', 'jwh')}, '새로고침 뒤': j2, '손잡이': g})
    # 폰 390 — 374
    for who, q in (('NEW', p), ('BASE', b)) if QJ.GATE else (('NEW', p),):   # regress — NEW 만
        q.ev("o=>__RV.uiSeed(o)", {'jpw': 340, 'jph': 640, 'jww': None, 'jwh': None})
        (q.size(390, 844) if QJ.GATE else _size(q, 390, 844))
        reload_keep(q)
        res[who]['phone'] = open_jp(q)
        (q.size(1440, 900) if QJ.GATE else _size(q, 1440, 900))
    T(G, u'폰 390×844 — 창 폭 374(화면 − 16)', (res['NEW']['phone'] or {}).get('w') == 374, res['NEW']['phone'])
    if QJ.GATE:   # 헛잣대(처리안 관문만) — regress 에서 끔
        T(G + '-헛', u'헛잣대 바탕 폰 — 340', (res['BASE']['phone'] or {}).get('w') == 340, res['BASE']['phone'])
    for q in ((p, b) if QJ.GATE else (p,)):   # regress — 바탕 Pg 없음
        q.ev("o=>__RV.uiSeed(o)", {'jpw': None, 'jph': None, 'jww': None, 'jwh': None})
        q.ev("()=>{S.joPanel=false;S.joPanelW=470;S.joPanelH=640;return 1}")
        close_all(q)


# ══════════ §B-3 빈칸 종류 = 지문 칸마다(A-3) ══════════
Q14 = ['T225914ㄱ', 'T225914ㄴ', 'T225914ㄷ', 'T225914ㄹ', 'T225914ㅁ']


def pick_bk(q, at, v, how):
    (q.press(at, how, 900) if QJ.GATE else _press(q, at, how, 900, JS_BKPOP, 'W21 빈칸 종류 확정 창(POPS · _pk)이 섰다'))
    title = q.ev("()=>__RV.bkPopTitle()")
    (q.press(q.ev("v=>__UZ.bkPopBtn(v)", v), how, 1000) if QJ.GATE else _press(q, q.ev("v=>__UZ.bkPopBtn(v)", v), how, 1000, JS_IDLE, 'W22 칸 누름 = bkPut · paint · render() 가 동기로 시작 → busy 가 풀렸다(창은 열린 채)'))
    close_all(q)
    return title


def g_r3(p, b, eng):
    G = 'r-3'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)) if QJ.GATE else (('NEW', p),):   # regress — NEW 만
        (q.size(1440, 900) if QJ.GATE else _size(q, 1440, 900))
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
    if QJ.GATE:   # 헛잣대(처리안 관문만) — regress 에서 끔
        bb = res['BASE']
        T(G + '-헛', u'헛잣대 바탕 — 다섯 칸 data-bk 모두 T225914ㄱ · 한 칸 누르면 다섯 칸이 다 바뀜', [c.get('bk') for c in bb['c0']] == ['T225914ㄱ'] * 5 and len(set(c.get('t') for c in bb['c1'])) == 1,
          {'data-bk': [c.get('bk') for c in bb['c0']], '뒤': [c.get('t') for c in bb['c1']], '기록': bb['rec']})
    # 1차객 리담 카드 — 지문 열쇠
    want0 = {'TR06154': 'T2461182h', 'T0946022': 'T0946021', 'T2663012': 'T2663011'}
    cards = {}
    for who, q in (('NEW', p), ('BASE', b)) if QJ.GATE else (('NEW', p),):   # regress — NEW 만
        q.ev("()=>__RV.bkClear()")
        cards[who] = {}
        for u in want0:
            go_key(q, u)
            cards[who][u] = q.ev("k=>__RV.cardBk(k)", u)
    T(G, u'1차객 리담 카드 TR06154 · T0946022 · T2663012 — data-bk = 제 지문 uid', all((cards['NEW'][u] or {}).get('bk') == u for u in want0), cards['NEW'])
    if QJ.GATE:   # 헛잣대(처리안 관문만) — regress 에서 끔
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
        for who, q in (('NEW', p), ('BASE', b)) if QJ.GATE else (('NEW', p),):   # regress — NEW 만
            q.ev("()=>__RV.bkClear()")
            s0 = go_key(q, u)
            pick_bk(q, q.ev("k=>__UZ.bkAt(k)", u), u'내용', 'touch')
            home(q, gk=gkOf(q, u))   # 필터 단추는 첫 화면 필터 줄(.mbqr) — 켠 뒤 필터 켜기 전에 잡은 그 단원으로 간다(홈은 필터를 안 건드림)
            (q.press(q.ev("()=>__UZ.fbtn()"), 'mouse', 500) if QJ.GATE else _press(q, q.ev("()=>__UZ.fbtn()"), 'mouse', 500, JS_FMENU, 'W26a 필터 메뉴(.uzfm)가 열렸다'))
            (q.press(q.ev("()=>__UZ.fopt('jo')"), 'mouse', 1200) if QJ.GATE else _press(q, q.ev("()=>__UZ.fopt('jo')"), 'mouse', 1200, JS_FJO, 'W26b 조문형 고름 = S.oxFilter 를 바꾸고 render() 동기 시작 → busy 풀림'))
            (q.press(q.ev("()=>__UZ.fbtn()"), 'mouse', 500) if QJ.GATE else _press(q, q.ev("()=>__UZ.fbtn()"), 'mouse', 500, JS_FMENU_BK, 'W26c 필터 메뉴가 빈칸 종류(.uzfc)까지 열렸다'))
            (q.press(q.ev("()=>__UZ.fbk('내용')"), 'mouse', 1500) if QJ.GATE else _press(q, q.ev("()=>__UZ.fbk('내용')"), 'mouse', 1500, JS_FBK, 'W26d 내용 체크 = onchange 가 S.oxBk 를 바꾸고 render() 동기 시작 → busy 풀림'))
            btn = (q.ev("()=>__UZ.fbtn()") or {}).get('t')
            q.pg.mouse.click(5, 5); (q.pg.wait_for_timeout(300) if QJ.GATE else _settle(q, 300, JS_FMENU_GONE, 'W26e 메뉴 밖 누름(pointerdown off) → 메뉴(.uzfm)가 닫혔다'))
            q.ev("s=>__HM.go(s)", s0)
            flt[who] = {'sel': s0, u: q.ev("k=>__RV.cardShown(k)", u), u0: q.ev("k=>__RV.cardShown(k)", u0), 'rec': q.ev("()=>__RV.bkAll()"), 'btn': btn, 'S': q.ev("()=>({f:S.oxFilter,bk:S.oxBk})")}
            q.ev("()=>{S.oxFilter='all';S.oxBk=[];return 1}")
            q.ev("()=>__RV.bkClear()")
        T(G, u'%s 카드에서 「내용」(손가락) → 바깥 필터 조문형 · 「내용」 → 그 단원에 %s 걸림(보임) · 기록 = %s 하나' % (u, u, u), flt['NEW'][u] and list((flt['NEW']['rec'] or {}).keys()) == [u], flt['NEW'])
        if QJ.GATE:   # 헛잣대(처리안 관문만) — regress 에서 끔
            T(G + '-헛', u'헛잣대 바탕 — 기록이 %s 에 붙어 필터에 %s 가 안 걸림' % (u0, u), not flt['BASE'][u] and list((flt['BASE']['rec'] or {}).keys()) == [u0], flt['BASE'])
    else:
        T(G, u'바깥 필터 표본 — 단원 줄 · 조문형 · 둘째 이후 지문을 못 찾음', False, '')
    home(p)
    if QJ.GATE:
        home(b)


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
    for who, q in (('NEW', p), ('BASE', b)) if QJ.GATE else (('NEW', p),):   # regress — NEW 만
        (q.size(1553, 900) if QJ.GATE else _size(q, 1553, 900))
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
        if QJ.GATE:   # 헛잣대(처리안 관문만) — regress 에서 끔
            bgot = {'next': res['BASE']['a']['next'], 'grade': res['BASE']['z']['grade'], 'prev': res['BASE']['a']['prev'], 'pill': res['BASE']['a']['pill'], 'mk': res['BASE']['a']['mk'], 'mkb': res['BASE']['a']['mkb'],
                    'pg': res['BASE']['a']['pg'], 't2': res['BASE']['a']['t2'], 'qtx': res['BASE']['a']['qtx']}[k]
            T(G + '-헛', u'헛잣대 바탕 %s — 민법 값과 다름' % lab, bgot is not None and bool(css_diff(bgot, MB[k])), {'바탕': bgot})   # 없는 요소(None)는 헛패스 — 있는 것을 맞대야 선다
    pa, hd = n['a']['paper'] or {}, n['a']['head'] or {}
    T(G, u'본문 폭 = 896 가운데(시험지 · 머리 줄 · 좌우 틈 같음 ±1)', abs((pa.get('w') or 0) - 896) <= 1 and abs((pa.get('gapL') or 0) - (pa.get('gapR') or 99)) <= 1 and abs((hd.get('w') or 0) - 896) <= 1 and abs((hd.get('gapL') or 0) - (hd.get('gapR') or 99)) <= 1,
      {'시험지': pa, '머리': hd, '알약 오른쪽 틈': n['a']['barR']})
    if QJ.GATE:   # 헛잣대(처리안 관문만) — regress 에서 끔
        T(G + '-헛', u'헛잣대 바탕 — 본문 전폭', abs(((res['BASE']['a']['paper'] or {}).get('w') or 0) - 896) > 50, res['BASE']['a']['paper'])
    # 단원 풀이 알약 무변
    up = {}
    for who, q in (('NEW', p), ('BASE', b)) if QJ.GATE else (('NEW', p),):   # regress — NEW 만
        q.ev("()=>{S.jtFold=false;return 1}")   # ★ 9/30 A-6 둘째 바퀴 — revfix0929b A-6: r-2 폰 새로고침이 남긴 1차객 서랍 접힘을 편다(바탕 b880a04 는 폰 부팅 접기가 없어 편 채 — 서랍 폭만큼 .mbbar 자리가 갈렸다 · r2 시험지 mainW 새 1540 · 바탕 1281)
        go_key(q, K0)
        up[who] = q.ev("()=>__RV.unitPill()")
    if QJ.REGRESS:   # 처리안 기준(r-4③) — 바탕 알약 = 기준 스냅샷(NEW 의 알약 computed 묶음 · 스냅샷 없으면 첫 기록)
        up['BASE'] = QJ.base('r-4③@%s' % eng, up['NEW'])
    T(G, u'단원 풀이 알약(채점 ✓ · 마킹 · ◀ 이전) computed = 바탕 그대로', up['NEW'] and up['NEW']['pill'] and up['NEW'] == up['BASE'], {'NEW': up['NEW'], '다름': {k: [up['NEW'].get(k), up['BASE'].get(k)] for k in up['NEW'] if up['NEW'].get(k) != up['BASE'].get(k)} if up['NEW'] else None})
    # 서랍 해 머리 · 회차 줄
    dr = {}
    for who, q in (('NEW', p), ('BASE', b)) if QJ.GATE else (('NEW', p),):   # regress — NEW 만
        q.ev("()=>{S.jtFold=false;return 1}")   # ★ 9/30 A-6 — revfix0929b A-6: r-2 폰(390) 새로고침이 폰 부팅 규칙으로 1차객 서랍을 접어 둔 채 돌아온다(r-7 treeHid 푸는 줄과 같은 까닭) — 편 서랍을 잰다
        home(q)
        q.ev("a=>__RV.exvGo(a[0],a[1])", [2026, 1])
        dr[who] = q.ev("()=>__RV.gy()")
    d = dr['NEW']
    if QJ.REGRESS:   # 처리안 기준(r-4④) — 바탕 「해 줄 수」 = 기준 스냅샷(NEW 회차 줄 수 · 스냅샷 없으면 첫 기록) — 바탕 줄은 글만 세는 자리표
        dr['BASE'] = {'base': [{'t': '(기준 스냅샷 — 바탕 안 띄움)', 'cur': False, 'order': []} for _ in range(int(QJ.base('r-4④@%s/nb' % eng, len(d['items'])) or 0))], 'heads': [], 'items': []}
    bd = dr['BASE']
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
    if QJ.GATE:   # 헛잣대(처리안 관문만) — regress 에서 끔
        bcur = [x for x in bd['base'] if x['cur']]
        T(G + '-헛', u'헛잣대 바탕 — 해 머리 줄 없음 · 「지금」 이 수 뒤', not bd['heads'] and bool(bcur) and bcur[0]['order'][-1:] == ['now'], {'바탕 지금 줄': bcur[:1]})
    # 누름 — 해 머리 = 접기/펴기 · 회차 줄 = 그 해
    q = p
    y2 = d['items'][1]['y'] if len(d['items']) > 1 else None
    (q.press(q.ev("y=>__RV.gyHeadAt(y)", '2026'), 'mouse', 900) if QJ.GATE else _press(q, q.ev("y=>__RV.gyHeadAt(y)", '2026'), 'mouse', 900, JS_GYFOLD, 'W27a 해 머리 누름 = S.jtCh.gy2026 접힘(동기 · jtPaint)'))
    f1 = q.ev("()=>__RV.gy()"); s1 = q.ev("()=>__RV.state()")
    (q.press(q.ev("y=>__RV.gyHeadAt(y)", '2026'), 'touch', 900) if QJ.GATE else _press(q, q.ev("y=>__RV.gyHeadAt(y)", '2026'), 'touch', 900, JS_GYOPEN, 'W27b 다시 누름 = S.jtCh.gy2026 지움(펴기)'))
    f2 = q.ev("()=>__RV.gy()")
    (q.press(q.ev("y=>__RV.gyRowAt(y)", y2), 'touch', 1500) if QJ.GATE else _press(q, q.ev("y=>__RV.gyRowAt(y)", y2), 'touch', 1500, JS_GYYEAR, 'W27c 회차 줄 누름 = mbGiGo → 그 해 기출뷰(.exv-paper.uzexv 의 해)', y2))
    s3 = q.ev("()=>__RV.state()"); p3 = q.ev("()=>document.querySelector('.exv-paper.uzexv')?document.querySelector('.exv-paper.uzexv').dataset.uzexv:null")
    ok = len(f1['items']) == len(d['items']) - 1 and not any(x['y'] == '2026' for x in f1['items']) and f1['heads'][0]['t'].startswith(u'▸') and 'gy2026' in (s1.get('jtCh') or '') \
        and len(f2['items']) == len(d['items']) and f2['heads'][0]['t'].startswith(u'▾') and s3.get('year') == y2 and p3 == y2
    T(G, u'해 머리 누름(마우스) = 접기(그 해 회차 줄 숨음 · ▸ · jt_ch 기억) · 다시(손가락) = 펴기 · 회차 줄 누름(손가락) = 그 해 기출뷰(%s)' % y2, ok,
      {'접은 뒤': [len(f1['items']), f1['heads'][0]['t'] if f1['heads'] else None, s1.get('jtCh')], '편 뒤': len(f2['items']), '누른 뒤': [s3, p3]})
    p.ev("()=>{S.jtCh={};return 1}")
    if QJ.GATE:
        b.ev("()=>{S.jtCh={};return 1}")
    for q in ((p, b) if QJ.GATE else (p,)):   # regress — 바탕 Pg 없음
        (q.size(1440, 900) if QJ.GATE else _size(q, 1440, 900)); home(q)


# ══════════ §B-5 조 패널 카드 칩(A-5) ══════════
def r5_pick(idx):
    """regress 표본 조 — 첫 · 끝 · 카드가 가장 많은 셋 · 가지(의N) 조 셋 · 카드 0 조 둘(삭제 · 빈 조) · 이름 붙은 표본 지문(TR0304가 · TH040743 · T2259011r)이 든 조 + 씨앗 고정 무작위 20(QJ.sample)"""
    ks = sorted(idx)
    pick = set(ks[:1] + ks[-1:])
    pick.update(sorted(ks, key=lambda k: (-len(idx[k]), k))[:3])
    pick.update([k for k in ks if u'의' in k][:3])
    pick.update([k for k in ks if not idx[k]][:2])
    for sid in ('TR0304가', 'TH040743', 'T2259011r'):
        pick.update(k for k in ks if sid in idx[k])
    pick.update(QJ.sample(ks, 20, 'revfix0928·r5'))
    return [k for k in ks if k in pick]


def g_r5_regress(br, eng, q):
    """regress — r-5 를 NEW 한 쪽(q = 막 띄운 처음 부팅 상태)에서 · 조 패널 카드 3,000+ 전수 대신 표본 조(r5_pick)만 두 번(1차객 가기 전 · 후) 지어 맞댄다 ·
    카드·조 총수와 3000+ 판정은 렌더 없이 데이터(jsPanelItems)로 전수 · 바탕(BASE) 둘(헛잣대)은 관문만 · 앱은 안 고치고 joPanelIdx 를 표본 키만 내는 걸로 잠깐 바꿔 chipCensus 를 그대로 부른다"""
    G = 'r-5'
    boot = {'tab': q.ev("()=>S.tab"), 'mln': q.ev("()=>__RV.mln()")}
    if boot['mln'].get('ok'):   # 새로 열기 = 1차객을 안 거친 상태(첫 탭이 1차객이면 MLN 을 비워 흉내)
        q.ev("()=>{MLN={ok:false};return 1}")
    go_jo(q, u'특허법', u'제140조')
    (q.press(q.J("()=>__WM.jpChip()"), 'mouse', 2500) if QJ.GATE else _press(q, q.J("()=>__WM.jpChip()"), 'mouse', 2500, JS_MLN, 'W12 정오문제 창을 열면 MLN 이 준비된다(MLN.ok · _subj 특허)'))
    m1 = q.ev("()=>__RV.mln()")
    idx = q.pg.evaluate(R5_IDX_JS)   # 조 → 카드 열쇠들(렌더 없음 · 데이터만) — 총수·표본 조 고르기
    total_n = sum(len(v) for v in idx.values())
    keys = r5_pick(idx)
    n_s = sum(len(idx[k]) for k in keys)
    t0 = time.time()
    A = q.pg.evaluate(R5_SUB_JS, keys)
    ta = time.time() - t0
    # 표본(창에서) — TR0304가 출제연도 칩 하나 · 1차객 가기 전
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
    B = q.pg.evaluate(R5_SUB_JS, keys)
    errs = q.errs_all()[:4]
    sa, sb = (A or {}).get('sig') or {}, (B or {}).get('sig') or {}
    diff = [x for x in sb if sa.get(x) != sb.get(x)]
    ex = [[x, (sa.get(x) or '')[:70], (sb.get(x) or '')[:70]] for x in diff[:3]]
    note = '(표본 %d/%d 조 · 카드 %d/%d)' % (len(keys), len(idx), n_s, total_n)
    T(G, u'새로 열기 → 조문 탭 → ☑ 정오문제(마우스) → MLN 준비(특허) · 특허 전 조 카드 머리 = 1차객 다녀온 뒤 값 · 어긋남 0 (카드 %d · 조 %d)' % (total_n, len(idx)),
      m1.get('ok') and m1.get('subj') == u'특허' and total_n > 3000 and not diff and len(sa) == len(sb),
      _tail({'부팅': boot, '창 연 뒤 MLN': m1, '어긋남': len(diff), '보기': ex, '잰 시간': round(ta, 1), '오류': errs}, note))
    th = next((v for x, v in sa.items() if x.endswith('|TH040743')), None)
    tb = next((v for x, v in sa.items() if x.endswith('|T2259011r')), None)
    T(G, u'표본(1차객 가기 전) — TR0304가 출제연도 칩 하나(창에서) · TH040743 「🔗 판 1」 · T2259011r 「📖 본문」', yc is not None and len(yc) == 1 and th and u'🔗 판 1' in th and tb and u'📖 본문' in tb,
      {'TR0304가': [k, yc], 'TH040743': (th or '')[:90], 'T2259011r': (tb or '')[:90]})


def _tail(detail, note, lim=480):
    """값 끝에 「(표본 n/N)」 — 출력은 lim 자에서 잘리니 앞을 줄여 꼬리를 남긴다(QJ 표본 규칙)"""
    s = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    return s[:max(0, lim - len(note))] + note


def g_r5(br, eng):
    G = 'r-5'
    (ns, nd, ne), (bs, bd, be) = envs()
    res = {}
    for who, (src, data, exam) in (('NEW', (ns, nd, ne)), ('BASE', (bs, bd, be))):
        q = Pg(br, eng, 'r5' + who, src, data, exam, W=1440, H=900)
        QJ.launch('new' if who == 'NEW' else 'base')   # 셈(§B-4) — r-5 가 NEW · BASE 를 따로 띄움(gate 에서도 동작 무변)
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
    for who, q in (('NEW', p), ('BASE', b)) if QJ.GATE else (('NEW', p),):   # regress — NEW 만
        (q.size(1280, 1000) if QJ.GATE else _size(q, 1280, 1000))
        res[who] = {}
        for how in hows:
            q.ev("()=>__JS.jo('특허법','제1조',{panel:false})")
            if not q.ev("()=>{const w=__JS.c3();return !!(w&&w.cols&&w.cols.length)}"):
                (q.click(q.ev("()=>__JS.c3fold()"), 900) if QJ.GATE else _clk(q, q.ev("()=>__JS.c3fold()"), 900, JS_C3COLS, 'W29 3법 접힘 단추 누름 → 열 칸(__JS.c3().cols)이 펴졌다'))
            h = q.ev("()=>__JS.c3headAt('상표')")
            if not h:
                res[who][how] = None
                continue
            if how == 'mouse':
                (q.hold(h['px'], h['py'], 600) if QJ.GATE else _hold(q, h['px'], h['py'], 600, 400, JS_C3PICK, 'W28 길게 누름이 끝나 3법 칸(.c3pick)이 섰다'))
            elif how == 'finger':
                (q.finger(h['px'], h['py'], 600) if QJ.GATE else _finger(q, h['px'], h['py'], 600, 500, JS_C3PICK, 'W28 길게 누름이 끝나 3법 칸(.c3pick)이 섰다'))
            else:
                (q.pen(h['px'], h['py'], 600) if QJ.GATE else _pen(q, h['px'], h['py'], 600, 400, JS_C3PICK, 'W28 길게 누름이 끝나 3법 칸(.c3pick)이 섰다'))
            res[who][how] = q.ev("()=>__RV.c3pick()")
        (q.size(1440, 900) if QJ.GATE else _size(q, 1440, 900))
    ok = all(v and v['vis'] and v['law'] == u'상표법' and v['afterCard'] and not v['inCard'] and v['below'] and v['inp'] for v in res['NEW'].values())
    T(G, u'3법 상표 카드 머리 600ms(%s) → 조·항 칸 = 카드(.thcol) 바로 뒤 제 줄 · 칸 위 끝 ≥ 카드 아래 끝 · 입력 칸' % '·'.join(hows), ok, res['NEW'])
    if QJ.GATE:   # 헛잣대(처리안 관문만) — regress 에서 끔
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
    for who, q in (('NEW', p), ('BASE', b)) if QJ.GATE else (('NEW', p),):   # regress — NEW 만
        (q.size(1440, 1000) if QJ.GATE else _size(q, 1440, 1000))
        q.ev("()=>{S.treeHid=false;S.listHid=false;return 1}")   # r2 폰 새로고침이 서랍을 접은 채로 남긴다(폰 시작값 treeHid) — 편 서랍을 잰다
        res[who] = {}
        for w in ((212,) if QJ.SMOKE else (212, 260, 320)):   # smoke — 212 만
            q.ev("w=>__JS.jo('특허법','제1조',{panel:false,treeW:w})", w)
            res[who][w] = q.ev("()=>__RV.names()")
        q.ev("()=>{S.treeW=212;return 1}")
        (q.size(1440, 900) if QJ.GATE else _size(q, 1440, 900))
    if QJ.GATE:
        n2, b2 = names_stat(res['NEW'][212]), names_stat(res['BASE'][212])
    else:   # regress — 처리안 기준(r-7①): 바탕 줄 수 = 기준 스냅샷(NEW 의 names_stat · 스냅샷 없으면 첫 기록)
        n2 = names_stat(res['NEW'][212])
        b2 = QJ.base('r-7①@%s/stat212' % eng, n2)
    # ★ 9/30 A-6 둘째 바퀴 — joscreen0929 A-1: 줄 끝 jcol3 = [빈칸 점][체크 단추](✏️M·🔗L 걷음 · CSS grid 30px 44px + 틈 4 = 78 · 넓은 서랍 .wide 44px 44px = 92) — 바탕 b880a04 의 세 칸(30·30·26 + 틈 = 94)과 맞대지 않고 새 틀 폭 한 자리로 잰다
    T(G, u'212px 서랍 — 제2조 정의 이름 다 보임(64/64) · 제14조 ≥ 56 · 조 번호까지 가려진 줄 ≤ 5 · 오른쪽 두 칸(빈칸 점 · 체크) 폭 78 한 자리',
      n2['j2'][0] is not None and n2['j2'][0] >= n2['j2'][1] - 1 and (n2['j14'][0] or 0) >= 56 and n2['pClip'] <= 5 and n2['em'] == [78] and n2['n'] == b2['n'],
      {'NEW': n2, '바탕': b2})
    if QJ.GATE:   # 헛잣대(처리안 관문만) — regress 에서 끔
        T(G + '-헛', u'헛잣대 바탕 212 — 제2조 이름 잘림 · 조 번호 가려진 줄 > 5', b2['j2'][0] is not None and b2['j2'][0] < b2['j2'][1] - 1 and b2['pClip'] > 5, b2)
    if not QJ.want('r-7②'):   # smoke — r-7①(212px 서랍)까지만
        return
    for w in (260, 320):
        if QJ.GATE:
            a, c = res['NEW'][w], res['BASE'][w]
        else:   # regress — 처리안 기준(r-7②): 바탕 줄(글 · 이름 칸 폭 · ★ 칸 폭) = 기준 스냅샷(NEW 줄 · 스냅샷 없으면 첫 기록)
            a = res['NEW'][w]
            _bv = QJ.base('r-7②@%s/%d' % (eng, w), [[x['t'], x['cw'], (x['st'] or {}).get('cw')] for x in a['rows']])
            c = {'n': len(_bv), 'rows': [{'t': t_, 'cw': cw_, 'st': ({'cw': sc_} if sc_ is not None else None)} for t_, cw_, sc_ in _bv]}
        # ★ 9/30 A-6 둘째 바퀴 — 뒤 판이 줄 꼴을 바꿈: joscreen0929 A-1 줄 끝 두 칸(폭 78 · 넓은 서랍 92 · 이름 칸 +16) · revfix0928pm A-5 이름 = 번호(.jno) + 이름(.jtt 말줄임) 격자(span.nm 이 안 넘쳐 sw = cw) — 줄마다 이름 칸은 바탕보다 안 좁고 · ★ 개정일 칸 = 바탕 · 오른쪽 칸 = 새 틀 폭 한 자리
        emw = 92 if w >= 300 else 78
        same = [x for x, y in zip(a['rows'], c['rows']) if x['t'] != y['t'] or x['cw'] < y['cw'] - 1 or (x['st'] or {}).get('cw') != (y['st'] or {}).get('cw') or x['em'] != emw]
        T(G, u'%dpx 서랍 — 줄마다 이름 칸 ≥ 바탕 · ★ 개정일 칸 = 바탕 · 오른쪽 두 칸(빈칸 점 · 체크) 폭 %d 한 자리' % (w, emw), a['n'] == c['n'] and not same and names_stat(a)['shr'] == 0, {'줄': a['n'], '다름': same[:3], 'NEW': names_stat(a)})


BR = {}
PARTS = [('r1', g_r1), ('r2', g_r2), ('r3', g_r3), ('r4', g_r4), ('r6', g_r6), ('r7', g_r7)]
SMOKE_PARTS = {'r1': ('chromium', 'webkit'), 'r7': ('chromium',)}   # smoke(_task_qa_slim A-4) — r-1 폰 390×844 손가락(WebKit 도) · r-7① 212px 서랍 · ERR(엔진마다) · 그 밖(r-2 · r-3 · r-4 · r-5 · r-6)은 건넘


def run_engine_regress(pw, eng):
    """regress(_task_qa_slim A-1 · A-2) — NEW 한 쪽만 띄운다: r-5(처음 부팅 상태가 필요) 를 그 한 쪽의 맨 앞에서 먼저 잰 뒤 r1~r7 을 이어 잰다(앱 띄움 4 → 1 · 바탕 풀기 0 · 바탕 띄움 0)"""
    parts = [(k, fn) for k, fn in PARTS if (not ONLY or k in ONLY) and (not QJ.SMOKE or eng in SMOKE_PARTS.get(k, ()))]
    do_r5 = (not ONLY or 'r5' in ONLY) and not QJ.SMOKE
    if not parts and not do_r5:   # smoke — 이 엔진에서 잴 칸이 없으면 브라우저도 안 띄운다
        return
    br = getattr(pw, eng).launch()
    BR[eng] = br
    try:
        ns, nd, ne = M.new_env()
        p = Pg(br, eng, 'rvN', ns, nd, ne)
        QJ.launch('new')
        try:
            N('boot', eng, {'NEW': p.ev("()=>__RV.cfBoot()"), 'BASE': '(regress — 바탕 안 띄움)'})
            if do_r5:
                print('── %s · r5' % eng, flush=True)
                pre_py, pre_js = list(p.errs), p.ev("()=>(window.__ERR||[]).slice()")   # r-5 앞(부팅까지)의 오류 — ERR 칸은 gate 처럼 p 의 부팅 + r1~r7 오류를 센다
                try:
                    with QJ.stage('%s·r5' % eng):
                        g_r5_regress(br, eng, p)
                except Exception as e:
                    T('RUN', u'%s · r5 묶음이 멈춤' % eng, False, repr(e)[:600])
                # r-5 가 쌓은 오류는 r-5 칸 안(오류 항목)에만 — gate 에서 r-5 는 따로 띄운 쪽이라 ERR 에 안 들어갔다 → 부팅까지의 오류로 되돌린다
                p.errs[:] = pre_py
                p.ev("a=>{window.__ERR=a;return 1}", pre_js)
            for k, fn in parts:
                print('── %s · %s' % (eng, k), flush=True)
                try:
                    with QJ.stage('%s·%s' % (eng, k)):
                        fn(p, None, eng)
                except Exception as e:
                    T('RUN', u'%s · %s 묶음이 멈춤' % (eng, k), False, repr(e)[:600])
            T('ERR', u'%s — NEW 앱 오류 0' % eng, not p.errs_all(), p.errs_all()[:6])
        finally:
            p.close()
    finally:
        br.close()


def run_engine(pw, eng):
    if QJ.REGRESS:   # regress · smoke — 위 run_engine_regress(NEW 한 쪽 · 바탕 0)
        return run_engine_regress(pw, eng)
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
        QJ.launch('new')
        b = Pg(br, eng, 'rvB', bs, bd, be)
        QJ.launch('base')
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
