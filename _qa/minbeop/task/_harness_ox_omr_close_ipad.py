# -*- coding: utf-8 -*-
"""민법OX 정리OMR 좌표 뷰어 — 「이 위치 저장」 뒤 아이패드에서 닫기가 안 먹음 · _task_ox_omr_close_ipad §A·§D.

  NEW  = genie 작업트리 minbeop/index.html (고친 판)
  BASE = `007fde4` 의 같은 파일(fix17 판 · 1,062,455 B · md5 b1926c8c…) — 헛잣대
  실데이터 = studyplandata minbeop/기록.json(저장소 전부) · 문항마스터.json(5,548)
  엔진 = playwright webkit · chromium — 둘 다 has_touch · is_mobile · 아이패드 뷰포트 1024×768 · 768×1024
  누름 = touchscreen.tap(**진짜 터치** · 신뢰 이벤트)
  끌기 = chromium 은 CDP 터치(진짜 · 끝에서 150ms 멈췄다 뗀다) · webkit 은 신뢰 마우스 끌기(도구 한계 — playwright 의 webkit 은 톡만 진짜 터치를 낸다)
         ⚠ 크롬은 움직이는 채로 떼면 튕김으로 보고 다음 톡 하나를 삼킨다(click 0 · BASE·NEW 같음) — 사람의 영역 끌기처럼 끝에서 멈춘다
  網 = 같은 출처 + cdn.tailwindcss.com 만 열고 나머지는 끊는다(fetch 는 SEED 가 가로챈다 · 교재 자리표 한 길만 대답)

  ⚠ 픽셀 게이트는 걸지 않는다 — 가림·쌓임은 elementFromPoint, 그려졌는가는 DOM 개수로 잰다(CLAUDE.md 검산 게이트).

쓰기 : python _harness_ox_omr_close_ipad.py                 (두 엔진 · 두 뷰포트 · BASE·NEW)
       python _harness_ox_omr_close_ipad.py webkit          (한 엔진만)
       python _harness_ox_omr_close_ipad.py webkit NEW      (한 판만)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import difflib, hashlib, http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

GENIE = _roots.genie()
SPD = _roots.spd()
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(tempfile.gettempdir(), 'h_omr_close_ipad')
REL = 'minbeop/index.html'
BASE_REV = '007fde4'
BASE_MD5 = 'b1926c8ccb7e7a038a2d042de9a2fe20'
TESTS = io.open(os.path.join(HERE, '_harness_ox_omr_close_ipad_tests.js'), encoding='utf-8').read()
VPS = {'1024x768': (1024, 768), '768x1024': (768, 1024)}
IPAD_UA = ('Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 '
           '(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__ALERTS=[];window.alert=function(m){__ALERTS.push(String(m));};
window.confirm=function(){return true;};window.prompt=function(){return null;};
(function(){var nf=window.fetch.bind(window);window.fetch=function(u,o){var s=String((u&&u.url)||u);
 var m=/api\.github\.com\/repos\/zzikkaplan\/minbeoppdf\/contents\/jari\/[^\/]+\/([^\/?]+)\.json/.exec(s);
 if(m&&window.__JARI&&window.__JARI[m[1]])return Promise.resolve(new Response(JSON.stringify(window.__JARI[m[1]]),{status:200,headers:{'Content-Type':'application/json'}}));
 if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));
 return nf(u,o);};})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
localStorage.clear();
</script>"""
READY = ("typeof buildQuizData==='function'&&typeof startQuiz==='function'&&typeof window.mbOmrGo==='function'"
         "&&typeof window.mbBookOpen==='function'&&!!window.oxCoord&&typeof dbPut==='function'&&!!window.__HZT")


def git(*a):
    return subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def J(s):
    try:
        return json.loads(s) if isinstance(s, str) else s
    except Exception:
        return {'__raw': str(s)[:300]}


def serve(tag, src):
    OUT = os.path.join(WORK, 'srv_' + tag); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    b = src.index('<body'); bb = src.index('>', b) + 1
    html = src[:bb] + SEED + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + TESTS + '\n</script>\n' + html[e:]
    io.open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)
    MAP = {'/rec.json': os.path.join(SPD, 'minbeop', '기록.json'), '/master.json': os.path.join(SPD, 'minbeop', '문항마스터.json')}

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=OUT, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            return MAP.get(p) or super().translate_path(path)

        def log_message(self, *a, **k):
            pass
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


def route_filter(route):
    u = route.request.url
    if u.startswith('http://127.0.0.1') or u.startswith('https://cdn.tailwindcss.com'):
        return route.continue_()
    return route.abort()


class S:
    """한 세션(엔진·뷰포트·판) — 누름은 전부 진짜 터치."""

    def __init__(self, pg, eng):
        self.pg, self.eng = pg, eng
        self.cdp = pg.context.new_cdp_session(pg) if eng == 'chromium' else None

    def js(self, expr, arg=None):
        return J(self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr))

    def until(self, expr, arg=None, ms=15000):
        try:
            self.pg.wait_for_function(expr, arg=arg, timeout=ms)
            return True
        except Exception:
            return False

    def tap(self, p):
        if not p or not p.get('on'):
            return False
        self.pg.touchscreen.tap(p['cx'], p['cy'])
        return True

    def drag(self, x0, y0, x1, y1, n=10):
        if self.cdp:
            def t(ty, x, y):
                self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': ([] if ty == 'touchEnd' else [{'x': x, 'y': y, 'id': 1}])})
            t('touchStart', x0, y0)
            for i in range(1, n + 1):
                t('touchMove', x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n)
                self.pg.wait_for_timeout(16)
            for i in range(5):            # 끝에서 150ms 멈췄다 뗀다 — 움직이는 채로 떼면 크롬이 튕김(fling)으로 보고 **다음 톡을 삼킨다**
                t('touchMove', x1, y1)    # (BASE·NEW 같음 · 멈춤 0ms 4/4 저장 톡 삼킴 ↔ 150ms 0/4 — dbg_chromium_save 실측)
                self.pg.wait_for_timeout(30)
            t('touchEnd', x1, y1)
            return 'cdp-touch(끝에서 멈춤)'
        m = self.pg.mouse
        m.move(x0, y0); m.down()
        for i in range(1, n + 1):
            m.move(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n)
            self.pg.wait_for_timeout(16)
        m.up()
        return 'mouse(trusted)'

    def btn(self, bid):
        return self.js("id=>__HZT.btn(id)", bid)

    def state(self):
        return self.js("__HZT.state()")

    def open_book(self, u):
        c = self.js("u=>__HZT.chip(u)", u)
        ok = self.tap(c)
        return {'chip': c, 'tapped': ok, 'row': self.until("u=>__HZT.rowReady(u)", u)}

    def mark_drag_save(self, dx, dy):
        R = {}
        R['mark'] = self.tap(self.btn('cd-mark'))
        R['markOn'] = self.until("()=>JSON.parse(__HZT.state()).layerPE==='auto'", None, 6000)
        plan = self.js("([a,b])=>__HZT.dragPlan(a,b)", [dx, dy])
        R['plan'] = plan
        if plan and not plan.get('none'):
            R['how'] = self.drag(plan['x'], plan['y'], plan['x2'], plan['y2'])
            self.pg.wait_for_timeout(250)
        s = self.state(); R['pick'] = s.get('pick'); R['saveOn'] = s.get('saveOn')
        R['save'] = self.tap(self.btn('cd-save'))
        R['saved'] = self.until("()=>{const s=JSON.parse(__HZT.state());return s.mode==='view'&&/저장했습니다/.test(s.bar||'')}", None, 12000)
        self.pg.wait_for_timeout(300)
        return R

    def close_and_measure(self, u):
        """§A-2 — 저장 뒤 ①뷰어 수 ②닫기 elementFromPoint ③톡 → click ④톡 뒤 뷰어 수·문제풀이"""
        R = {'a2': self.js("u=>__HZT.a2(u)", u)}
        R['tapClose'] = self.tap((R['a2'] or {}).get('close'))
        self.pg.wait_for_timeout(600)
        R['after'] = self.js("__HZT.after()")
        if (R['after'] or {}).get('wraps'):
            R['left'] = self.leftover()
        return R

    def leftover(self):
        """남은 뷰어가 먹통인가 — 그 닫기를 한 번 더 톡 · 아래 단추 톡 · 굴려 본다(BASE 증상 재현)"""
        L = {'before': self.js("__HZT.leftover()")}
        c = (L['before'] or {}).get('close')
        L['tapClose2'] = self.tap(c)
        self.pg.wait_for_timeout(500)
        L['afterClose2'] = self.js("__HZT.after()")
        foot = (L['before'] or {}).get('foot') or []
        if foot:
            b = self.btn(foot[0]); L['footBtn'] = foot[0]; L['tapFoot'] = self.tap(b)
            self.pg.wait_for_timeout(500)
            L['afterFoot'] = self.js("__HZT.after()")
        s0 = self.js("__HZT.stageScroll()")
        if self.cdp:                      # 크롬 — 남은 뷰어 가운데를 손가락으로 쓸어 올린다(진짜 터치)
            w, h = self.pg.viewport_size['width'], self.pg.viewport_size['height']
            self.drag(w * 0.5, h * 0.62, w * 0.5, h * 0.32)
            self.pg.wait_for_timeout(500)
            L['scroll'] = [s0, self.js("__HZT.stageScroll()")]
        else:                             # webkit(모바일)은 휠·끌기 스크롤을 못 낸다 — 굴릴 거리가 있는지만 적는다
            L['scroll'] = [s0, 'webkit: 굴릴 거리 %s' % (L['before'] or {}).get('scrollable')]
        return L

    def wipe(self):
        return self.js("__HZT.wipe()")


def session(eng, vpk, tag, src):
    w, h = VPS[vpk]
    srv, port = serve('%s_%s_%s' % (tag, eng, vpk), src)
    D = {'eng': eng, 'vp': vpk, 'tag': tag}
    t0 = time.time()
    with sync_playwright() as pw:
        br = getattr(pw, eng).launch()
        ctx = br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=IPAD_UA)
        ctx.route('**/*', route_filter)
        pg = ctx.new_page()
        perr, cerr = [], []
        pg.on('pageerror', lambda e: perr.append(str(e)[:240]))
        pg.on('console', lambda m: cerr.append(m.text[:240]) if m.type == 'error' else None)
        try:
            pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
            pg.wait_for_function(READY, timeout=120000)
            s = S(pg, eng)
            D['setup'] = s.js("__HZT.setup()")
            st = D['setup'] or {}
            u1, u2, u3 = st.get('u1'), st.get('u2'), st.get('u3')
            if not (u1 and u2 and u3):
                raise RuntimeError('setup: %s' % st)

            # ── S1 = D-1 · §A-2 : 자리 0곳 문항 → ID 칩 → 정리OMR 줄 → ⬚ 영역 지정 → 끌기 → 이 위치 저장 → 닫기
            R = D['S1'] = {}
            R['book'] = s.open_book(u1)
            R['tapRow'] = s.tap(s.js("u=>__HZT.row(u)", u1))
            R['ready'] = s.until("m=>__HZT.ready(m)", 'pick'); pg.wait_for_timeout(500)
            R['open'] = s.state()
            R['mds'] = s.mark_drag_save(160, 90)
            R.update(s.close_and_measure(u1))
            R['slot'] = (s.js("__HZT.coords()") or {}).get(u1)
            R['wipe'] = s.wipe()

            # ── S2 = D-2 : 같은 문항을 다시 연다(자리 있음 → view) → 위치 다시 지정 → 영역 지정 → 끌기 → 저장 → 닫기
            R = D['S2'] = {}
            R['book'] = s.open_book(u1)
            R['tapRow'] = s.tap(s.js("u=>__HZT.row(u)", u1))
            R['ready'] = s.until("m=>__HZT.ready(m)", 'view'); pg.wait_for_timeout(500)
            R['open'] = s.state()
            R['re'] = s.tap(s.btn('cd-re'))
            R['rePick'] = s.until("m=>__HZT.ready(m)", 'pick'); pg.wait_for_timeout(300)
            R['mds'] = s.mark_drag_save(200, 70)
            R.update(s.close_and_measure(u1))
            R['slot'] = (s.js("__HZT.coords()") or {}).get(u1)
            R['wipe'] = s.wipe()

            # ── S3 = D-3 : 정리OMR 줄을 200ms 안에 두 번 톡(책 창이 뷰어 위라 두 번째 톡도 그 줄에 닿는다) → 저장 → 닫기 한 번
            R = D['S3'] = {}
            R['book'] = s.open_book(u3)
            p = s.js("u=>__HZT.row(u)", u3)
            t0t = time.time()
            R['tap1'] = s.tap(p); pg.wait_for_timeout(60); R['tap2'] = s.tap(p)
            R['gapMs'] = round((time.time() - t0t) * 1000)
            R['ready'] = s.until("m=>__HZT.ready(m)", 'pick'); pg.wait_for_timeout(1200)
            R['open'] = s.state()
            R['mds'] = s.mark_drag_save(150, 80)
            R.update(s.close_and_measure(u3))
            R['wipe'] = s.wipe()

            # ── S5 = §A-3 : 펜 톡(pointerType pen · 합성기가 60ms 뒤 click) + 진짜 click 을 70ms 뒤 → 뷰어 수 → 닫기 한 번
            R = D['S5'] = {}
            R['book'] = s.open_book(u3)
            p = s.js("u=>__HZT.row(u)", u3)
            R['pen'] = s.js("([x,y])=>__HZT.pen(x,y)", [p['cx'], p['cy']])
            pg.wait_for_timeout(70)
            R['tap'] = s.tap(p)
            s.until("m=>__HZT.ready(m)", None, 8000); pg.wait_for_timeout(1500)
            R['res'] = s.js("__HZT.penResult()")
            R['open'] = s.state()
            R.update(s.close_and_measure(u3))
            R['wipe'] = s.wipe()

            # ── S5c = 헛잣대 : 펜 톡만(진짜 click 없음 = 사파리가 click 을 취소한 경우) → 합성 click 하나 → 뷰어 한 장
            R = D['S5c'] = {}
            R['book'] = s.open_book(u3)
            p = s.js("u=>__HZT.row(u)", u3)
            R['pen'] = s.js("([x,y])=>__HZT.pen(x,y)", [p['cx'], p['cy']])
            s.until("m=>__HZT.ready(m)", None, 8000); pg.wait_for_timeout(1500)
            R['res'] = s.js("__HZT.penResult()")
            R.update(s.close_and_measure(u3))
            R['wipe'] = s.wipe()

            # ── S4 = D-4 : 📍 칩으로 연 뷰어도 D-1
            R = D['S4'] = {}
            R['pin'] = s.js("u=>__HZT.pin(u)", u2)
            R['tapPin'] = s.tap(R['pin'])
            R['ready'] = s.until("m=>__HZT.ready(m)", 'pick'); pg.wait_for_timeout(500)
            R['open'] = s.state()
            R['mds'] = s.mark_drag_save(140, 100)
            R.update(s.close_and_measure(u2))
            R['slot'] = (s.js("__HZT.coords()") or {}).get(u2)
            R['wipe'] = s.wipe()

            # ── D-5 : ox_q_coords 전후
            D['co0'] = s.js("__HZT.co0()")
            D['co1'] = s.js("__HZT.coords()")
            D['err'] = s.js("__HZT.errs()")
            D['alerts'] = s.js("window.__ALERTS")
        except Exception as e:
            D['exc'] = str(e)[:600]
        D['pageerror'] = perr
        D['consoleError'] = cerr
        try:
            br.close()
        except Exception:
            pass
    srv.shutdown()
    D['secs'] = round(time.time() - t0, 1)
    return D


def main():
    os.makedirs(WORK, exist_ok=True)
    engines = [a for a in sys.argv[1:] if a in ('webkit', 'chromium')] or ['webkit', 'chromium']
    tags = [a for a in sys.argv[1:] if a in ('BASE', 'NEW')] or ['BASE', 'NEW']
    new = io.open(os.path.join(GENIE, REL), encoding='utf-8', newline='').read()
    base = git('show', BASE_REV + ':' + REL).decode('utf-8')
    SRC = {'BASE': base, 'NEW': new}
    RES = {}
    for eng in engines:
        for vpk in VPS:
            for tag in tags:
                k = '%s/%s/%s' % (eng, vpk, tag)
                print('… %s' % k, flush=True)
                RES[k] = session(eng, vpk, tag, SRC[tag])
                print('   %.1fs%s' % (RES[k]['secs'], ('  EXC ' + RES[k]['exc']) if RES[k].get('exc') else ''), flush=True)
    json.dump(RES, io.open(os.path.join(WORK, 'raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    L = []
    T = lambda n, c, i=None: L.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c or i is None else ' | ' + json.dumps(i, ensure_ascii=False)[:700]))
    I = lambda n, v: L.append('INFO | ' + n + ' | ' + json.dumps(v, ensure_ascii=False)[:1200])
    g = lambda d, *ks: (lambda x: x)(__import__('functools').reduce(lambda a, k: (a or {}).get(k) if isinstance(a, dict) else None, ks, d))

    # ══ 소스 · 파일
    bb, nb = base.encode('utf-8'), new.encode('utf-8')
    T('착수 %s = 지시서 §바탕 (1,062,455 B · md5 b1926c8c…)' % BASE_REV, len(bb) == 1062455 and hashlib.md5(bb).hexdigest() == BASE_MD5,
      [len(bb), hashlib.md5(bb).hexdigest()])
    T('NEW CRLF 0 · U+FFFD 0 (%d B · md5(LF) %s)' % (len(nb), hashlib.md5(nb).hexdigest()), b'\r\n' not in nb and '�' not in new)
    ch = [l for l in git('status', '--porcelain').decode('utf-8').split('\n') if l.strip()]
    T('genie 작업트리 바뀐 파일 = minbeop/index.html 하나 %s' % ch, ch == [' M ' + REL], ch)
    sk = lambda s: re.search(r'const SYNC_KEYS = \[(.+?)\];', s, re.S).group(1)
    T('SYNC_KEYS 줄 무변', sk(new) == sk(base))

    def fn(s, name):
        """함수 본문 — 한 줄짜리면 그 줄, 여러 줄이면 머리에서 들여쓰기 두 칸 `  }` 줄까지"""
        i = s.index(name); ls = s.rfind('\n', 0, i) + 1; le = s.index('\n', i)
        line = s[ls:le]
        if line.rstrip().endswith('}') and line.count('{') == line.count('}'):
            return line
        return s[ls:s.index('\n  }\n', i) + 4]

    def outside(s):
        """openViewer·closeViewer·bindDrag 세 함수를 자리표 한 줄로 바꾼 나머지 줄"""
        L = s.split('\n'); out = []; i = 0
        while i < len(L):
            m = re.match(r'  (?:async )?function (openViewer|closeViewer|bindDrag)\(', L[i])
            if m:
                if not (L[i].rstrip().endswith('}') and L[i].count('{') == L[i].count('}')):
                    while L[i] != '  }':
                        i += 1
                i += 1; out.append('<<' + m.group(1) + '>>'); continue
            out.append(L[i]); i += 1
        return out
    ob, on = outside(base), outside(new)
    ops = [o for o in difflib.SequenceMatcher(None, ob, on, autojunk=False).get_opcodes() if o[0] != 'equal']
    blocks = ['\n'.join(on[o[3]:o[4]]) for o in ops]
    okb = [o[0] == 'insert' and re.match(r'^\s*/\* ★ 2026-09-22 \(_task_ox_omr_close_ipad §B-[12]\).*?\*/\s*(var V_OPENING = false;)?\s*$', t, re.S) is not None
           for o, t in zip(ops, blocks)]
    T('§무접촉 — openViewer·closeViewer·bindDrag 밖에서 바뀐 것 = 이 판 주석 두 덩이 + `var V_OPENING = false;` 한 줄뿐 (덩이 %d · 나머지 %d줄 글자 그대로)'
      % (len(ops), len(ob)), len(ops) == 2 and all(okb), [o[0] for o in ops] + blocks)
    same = [nm for nm in ('async function saveRect(', 'function coords()', 'function saveCoords(', 'function docs()', 'async function mbOmrGo(',
                          'function paint()', 'async function draw()', 'function refAdopt(', 'function assetIds(') if fn(new, nm) == fn(base, nm)]
    T('저장 길 무접촉 — saveRect·coords·saveCoords·docs·mbOmrGo·paint·draw·refAdopt·assetIds 본문이 BASE 와 한 글자도 같다 (%d/9)' % len(same), len(same) == 9, same)
    if 'function closeViewer() {\n' in new:
        ov, cv, bd = fn(new, 'async function openViewer('), fn(new, 'function closeViewer()'), fn(new, 'function bindDrag()')
        T('§B-1 openViewer 가 틀을 만들기 **바로 앞**에서 closeViewer() · 틀에 id `cd-wrap` · closeViewer 는 V 의 틀 + #cd-wrap 전부를 뗀다',
          "    wrap.id = 'cd-wrap';" in ov and ov.index('    closeViewer();') < ov.index("    var wrap = el('div', 'position:fixed;inset:0;z-index:10000")
          and "if (V) { V.wrap.remove(); V = null; }" in cv and "document.querySelectorAll('#cd-wrap').forEach(function (w) { w.remove(); });" in cv
          and new.count("wrap.id = 'cd-wrap'") == 1, [cv])
        seg = ov[ov.index('await assetIds()') + 16: ov.index('document.body.appendChild(wrap)')]
        T('§B-2 잠금 V_OPENING — 여는 중이면 돌아감 · 자산 목록 await 하나만 감싸 finally 에서 푼다 · 그 뒤 틀을 붙일 때까지 await 0개(끼어들 틈 없음)',
          ov.count('V_OPENING') == 3 and 'if (V_OPENING) return;' in ov and 'try { have = await assetIds(); } finally { V_OPENING = false; }' in ov
          and 'await' not in seg and new.count('V_OPENING') == 4, [ov.count('V_OPENING'), 'await' in seg])
        T('§B-3 bindDrag 놓을 때 releasePointerCapture 명시(BASE 0회 → NEW 1회 · try 안) · 값·저장 줄 무변',
          base.count('releasePointerCapture') == 0 and new.count('releasePointerCapture') == 1
          and 'L.onpointerup = L.onpointercancel = function (e) {\n      try { L.releasePointerCapture(e.pointerId); } catch (_) { }' in bd
          and bd.replace('function (e) {\n      try { L.releasePointerCapture(e.pointerId); } catch (_) { }   /* ★ §B-3 — 뗄 때 저절로 풀리는 것에만 기대지 않는다 */\n', 'function () {\n')
          == fn(base, 'function bindDrag()'))
    else:
        T('§B 고침이 아직 없다(바탕 판)', False)

    # ══ 세션마다
    rows = []
    for eng in engines:
        for vpk in VPS:
            n, b = RES.get('%s/%s/NEW' % (eng, vpk)) or {}, RES.get('%s/%s/BASE' % (eng, vpk)) or {}
            pre = '[%s %s] ' % (eng, vpk)
            for tag, d in (('BASE', b), ('NEW', n)):
                if tag not in tags:
                    continue
                st = d.get('setup') or {}
                T(pre + '%s 부트 · 문항 %s · 시험 문항 %s·%s·%s(자리 %s) · %.0fs' % (tag, st.get('q'), st.get('u1'), st.get('u2'), st.get('u3'), st.get('slots0'), d.get('secs') or 0),
                  st.get('q') == 5548 and st.get('slots0') == [0, 0, 0] and not d.get('exc'), [d.get('exc'), st])
            if 'NEW' in tags and 'BASE' in tags:
                T(pre + '두 판이 같은 단원·같은 문항으로 잰다', g(n, 'setup', 'unit') == g(b, 'setup', 'unit') and
                  [g(n, 'setup', k) for k in ('u1', 'u2', 'u3')] == [g(b, 'setup', k) for k in ('u1', 'u2', 'u3')])
            for tag, d in (('BASE', b), ('NEW', n)):
                if tag not in tags:
                    continue
                for sc, how in (('S1', '손가락 톡 1번(줄)'), ('S3', '손가락 톡 2번(줄 · 60ms 사이)'), ('S5', '펜 톡 + 진짜 click 70ms 뒤'),
                                ('S5c', '펜 톡만(합성 click)'), ('S4', '손가락 톡 1번(📍 칩)'), ('S2', '손가락 · 위치 다시 지정')):
                    R = d.get(sc) or {}
                    op = (g(R, 'res', 'wraps') if sc in ('S5', 'S5c') else g(R, 'open', 'wraps'))
                    rows.append({'eng': eng, 'vp': vpk, 'tag': tag, 'sc': sc, 'how': how, 'open': op,
                                 'save': g(R, 'mds', 'saved'), 'wrapsAtClose': g(R, 'a2', 'wraps'),
                                 'efpClose': g(R, 'a2', 'close', 'hit'), 'efpTop': g(R, 'a2', 'close', 'top'),
                                 'clickClose': 'cd-close' in ''.join(g(R, 'after', 'clicks') or []),
                                 'wrapsAfter': g(R, 'after', 'wraps'), 'quiz': g(R, 'after', 'quiz'),
                                 'left': R.get('left')})

            if 'NEW' not in tags:
                continue
            S1, S2, S3, S4, S5, S5c = (n.get(k) or {} for k in ('S1', 'S2', 'S3', 'S4', 'S5', 'S5c'))
            u1, u2, u3 = (g(n, 'setup', k) for k in ('u1', 'u2', 'u3'))
            ok_closed = lambda R: (g(R, 'after', 'wraps') == 0 and g(R, 'after', 'cdWrap') == 0 and g(R, 'after', 'quiz') is True
                                   and g(R, 'after', 'centerInWrap') is False)
            # D-1
            T(pre + 'D-1 ID 칩 톡 → 교재 창에 정리OMR 줄 · 줄 톡 → 뷰어 **한 장**(pick) · id cd-wrap 1',
              g(S1, 'book', 'row') is True and g(S1, 'open', 'wraps') == 1 and g(S1, 'open', 'cdWrap') == 1 and g(S1, 'open', 'mode') == 'pick', [S1.get('book'), S1.get('open')])
            T(pre + 'D-1 ⬚ 영역 지정 톡 → 끌기(%s) → 초록 상자 · 「이 위치 저장」 켜짐 → 톡 → 저장(view)' % g(S1, 'mds', 'how'),
              g(S1, 'mds', 'markOn') is True and g(S1, 'mds', 'pick') is True and g(S1, 'mds', 'saveOn') is True and g(S1, 'mds', 'saved') is True, S1.get('mds'))
            T(pre + 'D-1 저장 뒤 닫기 가운데 맨 위 = 닫기(%s) · 톡 → click 이 닫기에 남(%s)' % (g(S1, 'a2', 'close', 'top'), g(S1, 'after', 'clicks')),
              g(S1, 'a2', 'close', 'hit') is True and 'cd-close' in ''.join(g(S1, 'after', 'clicks') or []), [S1.get('a2'), g(S1, 'after', 'clicks')])
            T(pre + '★D-1 닫기 **한 번**에 뷰어 0 · #cd-wrap 0 · 문제풀이 화면 보임 · 가운데 점이 뷰어 밖(%s)' % g(S1, 'after', 'center'), ok_closed(S1), S1.get('after'))
            # D-2
            T(pre + 'D-2 다시 열면 view(자리 있음) → 위치 다시 지정 → pick → 끌기 → 저장',
              g(S2, 'open', 'mode') == 'view' and g(S2, 'rePick') is True and g(S2, 'mds', 'saved') is True, [S2.get('open'), S2.get('rePick'), S2.get('mds')])
            T(pre + '★D-2 닫기 한 번에 뷰어 0 · 문제풀이 보임', ok_closed(S2) and 'cd-close' in ''.join(g(S2, 'after', 'clicks') or []), S2.get('after'))
            s1, s2 = S1.get('slot') or [], S2.get('slot') or []
            T(pre + 'D-2 위치 다시 지정 = 같은 자리 교체(자리 %d → %d · k 같음 · r 바뀜)' % (len(s1), len(s2)),
              len(s1) == 1 and len(s2) == 1 and s1[0].get('k') == s2[0].get('k') and s1[0].get('r') != s2[0].get('r'), [s1, s2])
            # D-3
            T(pre + '★D-3 줄 두 번 톡(%sms) → 뷰어 **한 장** · #cd-wrap 1' % S3.get('gapMs'),
              g(S3, 'open', 'wraps') == 1 and g(S3, 'open', 'cdWrap') == 1, [S3.get('gapMs'), S3.get('open')])
            T(pre + '★D-3 그 뒤 저장 → 닫기 한 번에 0', g(S3, 'mds', 'saved') is True and ok_closed(S3), [S3.get('mds'), S3.get('after')])
            cl5 = g(S5, 'res', 'clicks') or []
            T(pre + '★D-3 펜 겹침(합성 click + 진짜 click %s) → 뷰어 한 장 · 닫기 한 번에 0' % [(c.get('tr'), c.get('dt')) for c in cl5],
              len([c for c in cl5 if c.get('row')]) >= 2 and g(S5, 'res', 'wraps') == 1 and g(S5, 'res', 'cdWrap') == 1 and ok_closed(S5), [S5.get('res'), S5.get('after')])
            T(pre + 'D-3 펜 톡만 → 합성 click 하나 → 뷰어 한 장 → 닫기 한 번에 0(펜 합성기는 그대로 산다)',
              len([c for c in (g(S5c, 'res', 'clicks') or []) if c.get('row')]) == 1 and g(S5c, 'res', 'wraps') == 1 and ok_closed(S5c), [S5c.get('res'), S5c.get('after')])
            # D-4
            T(pre + '★D-4 📍 칩 톡 → pick → 끌기 → 저장 → 닫기 한 번에 0 · 문제풀이 보임',
              g(S4, 'open', 'wraps') == 1 and g(S4, 'open', 'mode') == 'pick' and g(S4, 'mds', 'saved') is True and ok_closed(S4), [S4.get('open'), S4.get('mds'), S4.get('after')])
            # D-5
            c0, c1 = J(n.get('co0') or '{}') or {}, n.get('co1') or {}
            keys = sorted(set(c0) | set(c1))
            diff = [k for k in keys if json.dumps(c0.get(k), sort_keys=True) != json.dumps(c1.get(k), sort_keys=True)]
            one = all(len(c1.get(k) or []) == 1 and (c1[k][0] or {}).get('doc') == 'minbeopOMR' for k in (u1, u2, u3))
            T(pre + '★D-5 ox_q_coords — 바뀐 문항 = 시험이 넣은 셋뿐(%s) · 저마다 정리OMR 자리 하나 · 나머지 %d문항 글자 그대로' % (diff, len(keys) - len(diff)),
              sorted(diff) == sorted([u1, u2, u3]) and one, diff)
            if 'BASE' in tags:
                pick = lambda d, sc, u: [(x.get('doc'), x.get('page'), x.get('r')) for x in (g(d, sc, 'slot') or [])]
                T(pre + 'D-5 같은 손짓 → BASE·NEW 가 저장한 자리값(doc·쪽·r) 같다(S1 %s)' % pick(n, 'S1', u1),
                  pick(n, 'S1', u1) == pick(b, 'S1', u1) and pick(n, 'S2', u1) == pick(b, 'S2', u1) and pick(n, 'S4', u2) == pick(b, 'S4', u2),
                  [pick(n, 'S1', u1), pick(b, 'S1', u1), pick(n, 'S2', u1), pick(b, 'S2', u1), pick(n, 'S4', u2), pick(b, 'S4', u2)])
            errs = (n.get('err') or []) + (n.get('pageerror') or []) + [e for e in (n.get('consoleError') or [])]
            T(pre + 'NEW JS 오류 0 · alert %s' % n.get('alerts'), not errs, errs)
            if 'BASE' in tags:
                I(pre + 'BASE 오류(참고)', (b.get('err') or []) + (b.get('pageerror') or []) + (b.get('consoleError') or []))
                # 헛잣대 — BASE 에서 같은 손짓이 증상을 내는가
                B3, B5 = b.get('S3') or {}, b.get('S5') or {}
                T(pre + '헛잣대 BASE — 줄 두 번 톡 → 뷰어 **두 장**(%s) · 저장 뒤 닫기 한 번 → 남은 뷰어 %s장'
                  % (g(B3, 'open', 'wraps'), g(B3, 'after', 'wraps')),
                  g(B3, 'open', 'wraps') == 2 and g(B3, 'after', 'wraps') == 1, [B3.get('open'), B3.get('after')])
                lf = B3.get('left') or {}
                T(pre + '헛잣대 BASE — 남은 뷰어는 닫기를 또 눌러도 안 닫힘(%s장 · click 은 남) · 아래 단추 %s 톡에도 그대로(%s장)'
                  % (g(lf, 'afterClose2', 'wraps'), lf.get('footBtn'), g(lf, 'afterFoot', 'wraps')),
                  g(lf, 'afterClose2', 'wraps') == 1 and 'cd-close' in ''.join(g(lf, 'afterClose2', 'clicks') or []), lf)
                I(pre + 'BASE 남은 뷰어 굴리기 — 쪽 그림이 틀보다 커서 굴릴 거리 %s · [쓸기 전, 뒤] 스크롤 %s (webkit 은 휠·끌기 스크롤을 못 낸다 — 거리만 적는다)'
                  % (g(lf, 'before', 'scrollable'), lf.get('scroll')), None)
                T(pre + '헛잣대 BASE — 펜 겹침 → 뷰어 두 장(%s) · 닫기 한 번 뒤 %s장' % (g(B5, 'res', 'wraps'), g(B5, 'after', 'wraps')),
                  g(B5, 'res', 'wraps') == 2 and g(B5, 'after', 'wraps') == 1, [B5.get('res'), B5.get('after')])
                B1 = b.get('S1') or {}
                I(pre + 'BASE 손가락 톡 1번(사용자 길 그대로) — 뷰어 %s장 · 저장 %s · 닫기 맨 위 %s · click %s · 닫은 뒤 %s장'
                  % (g(B1, 'open', 'wraps'), g(B1, 'mds', 'saved'), g(B1, 'a2', 'close', 'top'), g(B1, 'after', 'clicks'), g(B1, 'after', 'wraps')), None)
            I(pre + '책 창(z %s)이 뷰어(z %s) 위에 떠 있다 — 책 창 가운데 맨 위 %s · 정리OMR 줄은 뷰어가 떠 있어도 누를 수 있다 %s'
              % (g(S1, 'a2', 'bookZ'), g(S1, 'a2', 'wrapZ'), g(S1, 'a2', 'bookOverViewer', 'top'), g(S1, 'a2', 'rowStillOnTop', 'hit')), None)

    # §A-4 표
    I('§A-4 표 — 엔진·뷰포트·판·입력 → [줄 누른 뒤 뷰어 수 · 저장 · 저장 뒤 뷰어 수 · 닫기 맨 위 · 닫기 click · 닫은 뒤 뷰어 수 · 문제풀이]',
      [[r['eng'], r['vp'], r['tag'], r['how'], r['open'], r['save'], r['wrapsAtClose'], r['efpClose'], r['clickClose'], r['wrapsAfter'], r['quiz']] for r in rows])
    json.dump(rows, io.open(os.path.join(WORK, 'table.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    for l in L:
        print('   ' + l)
    p = sum(1 for l in L if l.startswith('PASS')); f = sum(1 for l in L if l.startswith('FAIL'))
    print('\n합계  PASS %d · FAIL %d' % (p, f))
    io.open(os.path.join(HERE, '_harness_ox_omr_close_ipad_result.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n\n합계  PASS %d · FAIL %d\n' % (p, f))
    sys.exit(0 if not f else 1)


if __name__ == '__main__':
    main()
