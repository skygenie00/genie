# -*- coding: utf-8 -*-
r"""_task_jo_2cha_minso_board §B 관문 — 조판기 2차 기출·GS 보드 시안 v41(본문 펴기 · 메모 창 · 누락 · 설문 연결 · 단원 토글 · 보드 검색 · 해설/Claude)

  python _harness_jo_2cha_minso_board.py [--new <앱 파일 | genie git 판>] [--base <판 = 281c93f>] [--yardstick] [--only B1,B6,..] [--eng chromium[,webkit]] [--res <결과 파일>] [--shots <화면 폴더>]

  NEW  = genie 작업트리 jo/index.html(고친 판) · BASE = 바탕(cloud/jo_sp_book5 끝 281c93f) — 헛잣대(--yardstick)와 B2 바탕 높이·B16 바탕 스크롤바에 쓴다
  데이터 = genie jo/data(실물 · 두 판 같은 것) · 기록 = 합성(B-0 — localStorage 주입 · 실제 기록 0 · studyplandata 기록 쓰기 없음)
  망 = 같은 출처만 · studyplandata contents → 가짜 원격(/__rec/ · 하네스 메모리 · B-S) · minbeoppdf hsul/<법>.json → 로컬 클론 사본(/__mb/ · route 사본) · 그 밖의 바깥 주소 404
  엔진 = playwright chromium(--hide-scrollbars 를 뺌 — B16 스크롤바 폭을 잰다) · PC 1440×900 · 900×900(마우스) · 아이패드 834×1194 · 폰 390×844(터치 · DSF 2 · 손가락 = CDP 터치)
         WebKit 은 터치 칸(B6 · B7 · B11 · B12 · B15 · B17)만 — 이 기계에 없으면 「안 잼」
  관문:
    B0 합성 기록 꼴 · B1 머리 줄 · B2 간격 · B3 단계·번호 · B4 제목·깊이 · B5 두루마리·코드 · B6 메모 창 · B7 고침·댓글·깃발 · B8 카드 창 메모 · B9 누락 ·
    B10 누락 올리기 · B11 설문 연결 · B12 단원 토글·+ · B13 해설·Claude · B14 검색 · B15 창 크기·끌기 · B16 스크롤바·토스트 · B17 폭 · B-S 동기화 · 화면 훑기
  헛잣대(--yardstick) = 바탕 + 같은 합성 기록 → B1 B3 B4 B5 B6 B7 B9 B10 B11 B12 B13 B14 B16 묶음마다 FAIL 이어야 한다(잣대가 산다)
  ★ fix8(10/4 · 로컬 회귀 가름 뒤) — B2 간격 셋 = 바탕 대비 상대 잣대(채팅 10/4 01:0x) · B6 메모 창 폭 = 240 / 좁은 화면 min(230, 창폭−24)(A-7-6 · §B-6) ·
    B6 낱말 누름 = 창에 안 덮인 낱말(폰) · B6 GS 넘침 칸 = 판정 무변 · 넘친 요소를 값(INFO 두 줄)에
  결과 = 화면에 PASS/FAIL 줄 · --res 파일(기본 = 임시 폴더 · _qa 에 결과를 쓰지 않는다)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402 — _task_qa_slim(10/4) 실행 모드: --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같다) · 새 갈래는 모두 `if QJ.REGRESS:` / `if QJ.GATE:` 안
import base64, hashlib, io, json, os, re, subprocess, sys, tempfile, threading, time, traceback, urllib.parse   # noqa: E402
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEW = ARG('--new', _roots.genie('jo', 'index.html'))
BASE = ARG('--base', '281c93f')   # cloud/jo_sp_book5 끝 = 이 판의 바탕
YARD = '--yardstick' in sys.argv and QJ.GATE   # 헛잣대(바탕을 띄움)는 gate 몫
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
if QJ.SMOKE:   # smoke: Chromium PC 만 · 칸 = B0(합성 기록 꼴) · B1(머리 줄) + 페이지 오류 0
    ONLY = ['B0', 'B1']
    ENGS = [x for x in ENGS if x == 'chromium']
TMPD = os.path.join(tempfile.gettempdir(), 'h_jo_c2board')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_jo_2cha_minso_board_result.txt'))
SHOTS = ARG('--shots', os.path.join(TMPD, 'shots'))
DATA = _roots.genie('jo', 'data')
MBH = _roots.mbpdf('hsul')
TESTS = io.open(os.path.join(HERE, '_harness_jo_2cha_minso_board_tests.js'), encoding='utf-8').read()
SEP = '\u001f'
F2461 = '민기출 24-61-2-관할{합}전부구별, 반소이송가부'
F1350 = '민기출 13-50-2-사물관할'
TK2461, TK1350 = 'card|기출|' + F2461, 'card|기출|' + F1350
PK_A = SEP.join([TK2461, '1', '2', '설문(1)'])       # 햄찌 · 「Ⅰ. 설문(1) (10점)」
PK_B = SEP.join([TK2461, '3', '2', '합의관할'])      # 꼬까 · 「2. 합의관할 유효성 검토」
PK_C = SEP.join([TK1350, '1', '2', '설문(1)'])       # 햄찌 · 13-50-2
PREC_ID = '2022후10722'
PK_P = SEP.join(['prec|' + PREC_ID, 'sum/14', '2', '확인대상발명에'])   # 판례 깃발 대조(무변)
PIT0 = {PK_A: {'t': '2번 소문제 논점을 34,35 이송가부로 잡았다(합성)', 'who': '햄찌', 'at': '2026-10-03T00:33:38.221Z', 'ts': '2026-10-03T00:33:38.221Z'},
        PK_B: {'t': '합의관할 요건 1임특특서(합성)', 'who': '꼬까', 'at': '2026-10-02T01:00:00.000Z', 'ts': '2026-10-02T01:00:00.000Z'},
        PK_C: {'t': '사물관할은 1심(합성)', 'who': '햄찌', 'at': '2026-10-01T03:24:40.681Z', 'ts': '2026-10-01T03:24:40.681Z'},
        PK_P: {'t': '판례 깃발 대조(합성)', 'who': '햄찌', 'at': '2026-10-01T00:00:00.000Z', 'ts': '2026-10-01T00:00:00.000Z'}}
IPAD_UA = 'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
IPHONE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
DEV = {'pc': dict(W=1440, H=900, touch=False), 'pc900': dict(W=900, H=900, touch=False),
       'pad': dict(W=834, H=1194, touch=True, ua=IPAD_UA), 'phone': dict(W=390, H=844, touch=True, ua=IPHONE_UA)}

RES = []
T0 = time.time()


def T(g, name, ok, detail=''):
    RES.append((g, name, bool(ok), detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', g, name, d[:600]), flush=True)
    return bool(ok)


def N(g, name, detail=''):
    RES.append((g, name, None, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('INFO | %s · %s | %s' % (g, name, d[:900]), flush=True)


def git(*a):
    return subprocess.run(['git', '-C', _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def app_src(x):
    if os.path.isfile(x):
        return open(x, 'rb').read().decode('utf-8')
    b = git('show', x + ':jo/index.html')
    if not b:
        raise SystemExit('앱을 못 읽었다: ' + x)
    return b.decode('utf-8')


def md5lf(s):
    return hashlib.md5(s.replace('\r\n', '\n').encode('utf-8')).hexdigest()


# ════════════════════════ 가짜 원격 · 서버 ════════════════════════
class Remote:
    def __init__(self):
        self.files, self.lock, self.puts = {}, threading.Lock(), 0

    def clear(self):
        with self.lock:
            self.files = {}
            self.puts = 0

    def json(self, k='jopangi/기록.json'):
        with self.lock:
            b = self.files.get(k)
        return json.loads(b.decode('utf-8')) if b else None


REMOTE = Remote()
SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.alert=function(){};window.confirm=function(){return true;};window.prompt=function(){return null;};
(function(){var Q=new URLSearchParams(location.search);var nf=window.fetch.bind(window);
window.fetch=function(u,o){o=o||{};var s=String((u&&u.url)||u);
 var sp=s.indexOf('api.github.com/repos/zzikkaplan/studyplandata/contents/');
 if(sp>=0){var r2=s.slice(sp+'api.github.com/repos/zzikkaplan/studyplandata/contents/'.length).split('?')[0];
  var h2={};try{var hh=o.headers;var ac=hh&&(typeof hh.get==='function'?hh.get('Accept'):(hh.Accept||hh.accept));if(ac)h2['Accept']=ac;}catch(e){}
  if(o.body)h2['Content-Type']='application/json';
  return nf(location.origin+'/__rec/'+r2,{method:o.method||'GET',headers:h2,body:o.body});}
 var mp=s.indexOf('api.github.com/repos/zzikkaplan/minbeoppdf/contents/');
 if(mp>=0){var r3=s.slice(mp+'api.github.com/repos/zzikkaplan/minbeoppdf/contents/'.length).split('?')[0];return nf(location.origin+'/__mb/'+r3,{method:'GET'});}
 if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));
 return nf(u,o);};
if(Q.get('seed')!=='0'){try{localStorage.clear();}catch(e){}
 var cfg={person:Q.get('who')||'햄찌'};if(Q.get('tok')!=='0')cfg.token='harness-token';
 try{localStorage.setItem('tt.cfg',JSON.stringify(cfg));}catch(e){}
 if(Q.get('rec')!=='0'){try{localStorage.setItem('jopangi.postit',JSON.stringify(window.__PIT0));}catch(e){}}}
})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
</script>"""
SERVERS = {}


def inject(src):
    src = src.replace('\r\n', '\n')
    b = src.index('<body'); bb = src.index('>', b) + 1
    seed = '<script>window.__PIT0=' + json.dumps(PIT0, ensure_ascii=False) + ';</script>' + SEED
    html = src[:bb] + seed + src[bb:]
    e = html.rindex('</body>')
    return html[:e] + '<script>\n' + TESTS + '\n</script>\n' + html[e:]


def serve(tag, src):
    if tag in SERVERS:
        return SERVERS[tag][1]
    body = inject(src).encode('utf-8')

    class Hd(SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, data, ct='application/json'):
            self.send_response(code)
            self.send_header('Content-Type', ct)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            p = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
            if p in ('/jo/', '/jo/index.html'):
                return self._send(200, body, 'text/html; charset=utf-8')
            if p.startswith('/__rec/'):
                k = p[len('/__rec/'):]
                with REMOTE.lock:
                    b = REMOTE.files.get(k)
                if b is None:
                    return self._send(404, b'{"message":"Not Found"}')
                if 'raw' in (self.headers.get('Accept') or ''):
                    return self._send(200, b, 'application/octet-stream')
                return self._send(200, json.dumps({'sha': hashlib.sha1(b).hexdigest(), 'size': len(b)}).encode())
            if p.startswith('/__mb/hsul/'):   # minbeoppdf hsul 사본(route) — 그 밖 minbeoppdf 는 404
                f = os.path.join(MBH, *[x for x in p[len('/__mb/hsul/'):].split('/') if x])
                if os.path.isfile(f):
                    return self._send(200, open(f, 'rb').read())
                return self._send(404, b'{"message":"Not Found"}')
            if p.startswith('/__mb/'):
                return self._send(404, b'{"message":"Not Found"}')
            return super().do_GET()

        def do_PUT(self):
            p = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
            if not p.startswith('/__rec/'):
                return self._send(405, b'{}')
            k = p[len('/__rec/'):]
            n = int(self.headers.get('Content-Length') or 0)
            try:
                j = json.loads(self.rfile.read(n).decode('utf-8') or '{}')
                data = base64.b64decode(j.get('content', ''))
            except Exception:
                return self._send(422, b'{}')
            with REMOTE.lock:
                cur = REMOTE.files.get(k)
                if cur is not None and j.get('sha') and j.get('sha') != hashlib.sha1(cur).hexdigest():
                    return self._send(409, b'{"message":"conflict"}')
                REMOTE.files[k] = data
                REMOTE.puts += 1
            return self._send(200, json.dumps({'content': {'sha': hashlib.sha1(data).hexdigest()}}).encode())

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
            if p.startswith('/jo/data/'):
                return os.path.join(DATA, *[x for x in p[len('/jo/data/'):].split('/') if x])
            return os.path.join(HERE, '__없음__')

    srv = ThreadingHTTPServer(('127.0.0.1', 0), Hd)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


class P:
    """한 쪽(page) — 판(tag) · 기기(dev) · 엔진"""
    def __init__(self, br, eng, tag, src, dev='pc', q='seed=1'):
        self.eng, self.tag, self.dev = eng, tag, dev
        QJ.launch('base' if tag == 'BASE' else 'new')
        d = DEV[dev]
        self.touch = d['touch']
        port = serve(tag, src)
        kw = dict(viewport={'width': d['W'], 'height': d['H']})
        if d['touch']:
            kw.update(device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=d.get('ua'))
        self.ctx = br.new_context(**kw)
        self.ctx.route('**/*', lambda r: r.continue_() if r.request.url.startswith('http://127.0.0.1') else r.abort())
        self.pg = self.ctx.new_page()
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:300]))
        self.cdp = self.ctx.new_cdp_session(self.pg) if (eng == 'chromium' and d['touch']) else None
        self.url = 'http://127.0.0.1:%d/jo/index.html?%s' % (port, q)
        self.pg.goto(self.url, wait_until='load', timeout=120000)
        self.pg.wait_for_function("!!window.__C2&&typeof render==='function'&&typeof popCard4==='function'", timeout=120000)
        self.pg.wait_for_timeout(1200)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def go(self, o=None, keep=False):
        return self.ev("([o,k])=>__C2.go(o,k)", [o or {}, keep])

    def board(self):
        return self.ev("()=>__C2.board()")

    def idle(self, ms=350):
        self.pg.wait_for_timeout(ms)
        self.ev("()=>__C2.idle()")

    def click(self, at, wait=450):
        if not at or not at.get('on'):
            return False
        self.pg.wait_for_timeout(120)   # 도구가 scrollIntoView 로 굴린 스크롤 알림이 누름 뒤에 와서 「바깥 스크롤 = 닫힘」 메뉴를 닫지 않게(사람은 굴림이 멎은 뒤 누른다)
        if self.touch:
            self.tap(at['cx'], at['cy'])
        else:
            self.pg.mouse.click(at['cx'], at['cy'])
        self.idle(wait)
        return True

    def tap(self, x, y):
        if self.cdp:
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'id': 1}]})
            self.pg.wait_for_timeout(40)
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        else:
            self.pg.touchscreen.tap(x, y)

    def long(self, at, ms=700):
        if not at or not at.get('on'):
            return False
        self.pg.wait_for_timeout(120)
        x, y = at['cx'], at['cy']
        if self.cdp:
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'id': 1}]})
            self.pg.wait_for_timeout(ms)
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        else:
            self.pg.mouse.move(x, y); self.pg.mouse.down(); self.pg.wait_for_timeout(ms); self.pg.mouse.up()
        self.idle(400)
        return True

    def drag(self, x0, y0, x1, y1, n=12):
        if self.cdp:
            t = lambda ty, x, y: self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': ([] if ty == 'touchEnd' else [{'x': x, 'y': y, 'id': 1}])})
            t('touchStart', x0, y0)
            for i in range(1, n + 1):
                t('touchMove', x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.pg.wait_for_timeout(16)
            t('touchEnd', x1, y1)
            self.idle(300)
            return 'touch'
        m = self.pg.mouse
        m.move(x0, y0); m.down()
        for i in range(1, n + 1):
            m.move(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.pg.wait_for_timeout(16)
        m.up()
        self.idle(300)
        return 'mouse'

    def key(self, k):
        self.pg.keyboard.press(k); self.idle(300)

    def shot(self, name):
        os.makedirs(SHOTS, exist_ok=True)
        f = os.path.join(SHOTS, '%s_%s_%s.png' % (self.tag, self.dev, name))
        try:
            self.pg.screenshot(path=f)
        except Exception:
            pass
        return f

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


def S_(x):
    return json.dumps(x, ensure_ascii=False, default=str)[:500]


def expand(p, code, want=True):
    """그 줄 본문이 want 가 되게 제목을 누른다(떠 있는 작은 메뉴는 먼저 닫는다 — 사람도 Esc·바깥 누름으로 닫고 누른다)"""
    p.ev("()=>{try{if(typeof c2FlyClose==='function')c2FlyClose();}catch(e){}return 1;}")
    ri = p.ev("c=>__C2.rowInfo(c)", code)
    if not ri:
        return None
    if bool(ri['body']) != want:
        p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", [code, 'title']), 700)
    return p.ev("c=>__C2.rowInfo(c)", code)


# ════════════════════════ 관문 ════════════════════════
def B0(p):
    g = 'B0'
    pit = p.ev("()=>__C2.pit()")
    T(g, '합성 기록 — postit 4칸(24-61-2 설문(1) 햄찌 · 같은 카드 합의관할 꼬까 · 13-50-2 설문(1) 햄찌 · 판례 대조 1) · c2miss · c2qlink 빈 것 · tt.cfg person 햄찌',
      set(pit) == set(PIT0) and not p.ev("()=>__C2.ls('jopangi.c2miss')") and not p.ev("()=>__C2.ls('jopangi.c2qlink')") and p.ev("()=>__C2.ls('tt.cfg').person") == '햄찌',
      {'pit': len(pit), 'who': p.ev("()=>__C2.ls('tt.cfg')")})


def B1(p):
    g = 'B1'
    b = p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'yearSort': 'desc'})
    order = p.ev("()=>__C2.headOrder()") or []
    seq = [x for x in order if x in ('pill', 'ordseg', 'c2sortar', 'c2lv', 'c2srw')]
    T(g, '.ysort·.ysel 0 · .c2lh 0', b['ysort'] == 0 and b['ysel'] == 0 and b['lh'] == 0, {k: b[k] for k in ('ysort', 'ysel', 'lh')})
    T(g, '머리 차례 = pill 셋 → .ordseg → .c2sortar → .uzstep.c2lv → .c2srw', seq == ['pill', 'pill', 'pill', 'ordseg', 'c2sortar', 'c2lv', 'c2srw'], order)
    f0, a0 = b['first'], b['sortar']
    p.click(p.ev("()=>__C2.at('#slot .c2sortar')"))
    b1 = p.board()
    T(g, '화살표 누름 → 차례 뒤집힘(첫 줄 코드 바뀜 · ↓ → ↑)', a0 == '↓' and b1['sortar'] == '↑' and b1['first'] != f0 and b1['S']['ys'] == 'asc', [a0, f0, b1['sortar'], b1['first']])
    p.click(p.ev("()=>__C2.at('#slot .c2sortar')"))
    on = p.ev("()=>__C2.segOn()")
    p.long(on)
    fm = p.ev("()=>__C2.fmenu()")
    b2 = p.board()
    T(g, '켜진 단원별 0.5초 길게 → 메뉴(전체 19 + 19) · 길게 뒤 모드 안 바뀜', bool(fm) and fm['n'] == 20 and fm['items'][0] == '전체 19' and b2['S']['ord'] == 'unit', [fm and fm['items'][:4], fm and fm['n'], b2['S']['ord']])
    p.click(p.ev("t=>__C2.fmenuItem(t)", '15-52'))
    b3 = p.board()
    ont = [s['t'] for s in b3['seg'] if s['on']]
    T(g, '15-52 고름 → 단원별 편 4 · 단원 4 · 줄 4 · 단추 「단원별 · 15-52」', b3['bands'] == 4 and b3['heads'] == 4 and b3['rows'] == 4 and ont == ['단원별 · 15-52'],
      {k: b3[k] for k in ('bands', 'heads', 'rows', 'seg')})
    rb = [s for s in b3['seg'] if s['t'].startswith('회차별')]
    p.click(p.ev("()=>{const b=[...document.querySelectorAll('#ordSeg button')].find(x=>x.textContent.indexOf('회차별')===0);return b?(()=>{const r=b.getBoundingClientRect();return {cx:r.left+r.width/2,cy:r.top+r.height/2,on:true};})():null;}"))
    b4 = p.board()
    T(g, '회차별로 바꿔도 15-52(회차 머리 1 · 줄 4 · 단추 「회차별 · 15-52」)', b4['rheads'] == 1 and b4['rows'] == 4 and [s['t'] for s in b4['seg'] if s['on']] == ['회차별 · 15-52'], {k: b4[k] for k in ('rheads', 'rows', 'seg')})
    p.long(p.ev("()=>__C2.segOn()"))
    p.click(p.ev("t=>__C2.fmenuItem(t)", '전체 19'))
    b5 = p.board()
    T(g, '전체로 되돌림 → 줄 76 · 켜진 단추 title 「길게 누르면 회차 고르기」', b5['rows'] == 76 and any(s['on'] and s['title'] == '길게 누르면 회차 고르기' for s in b5['seg']), {'rows': b5['rows'], 'seg': b5['seg']})


def B2(p, pb):
    g = 'B2'
    # 시안(board.html)은 보드만 있는 판 — 같은 폭으로 재려고 옆 두 칸(.tree · .plist)을 접는다(바탕도 같게) · 편 채로 잰 값은 INFO
    o0 = {'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'c2uv': {}, 'treeHid': False, 'listHid': False}
    p.go(o0)
    n0 = p.ev("c=>__C2.gaps(c)", '24-61-2')
    N(g, 'PC 900 · 옆 두 칸 편 채(목록 폭 %s · 560 미만 = 두 줄 꼴)' % (p.board() or {}).get('listW'), n0 and {k: n0[k] for k in ('total', 'bandGapMax', 'bandH', 'band2head', 'bar2band', 'rowH')})
    o = dict(o0, treeHid=True, listHid=True)
    p.go(o)
    n = p.ev("c=>__C2.gaps(c)", '24-61-2')
    # 옛(fix8 전 · 절대값 = 시안을 그린 기계 글꼴에서 잰 값):
    # T(g, 'PC 900(옆 두 칸 접음 = 시안 폭) — 편 띠 사이 ≤ 6px · 편 띠 높이 ≤ 24px · 24-61-2 줄(단원 칩 가림) ≤ 28px(시안 26)',
    #   n and n['bandGapMax'] is not None and n['bandGapMax'] <= 6.5 and n['bandH'] <= 24.5 and n['rowH'] <= 28.5, dict(n or {}, listW=(p.board() or {}).get('listW')))
    b0 = None   # ★ fix8 — 바탕 판 값을 먼저 잰다(같은 실행 · 같은 폭 · 같은 데이터) — 아래 상대 잣대가 쓴다
    if pb:
        pb.go(o)
        b0 = pb.ev("c=>__C2.gaps(c)", '24-61-2')
    # ★ fix8 — 상대 잣대(채팅 10/4 01:0x 「⑧ B2 편 띠 높이 판정」 · 앱 무변 · 사용자 넘김 10/4 02:55 [Code] 줄): 줄어드는 양 = 지시서 A-1 끝 줄 「시안 잰 값(같은 데이터 · PC 900)」 바탕 → 시안 · §B-2 기준
    #   편 띠 사이 14 → 6(§B-2 ≤ 6) = −8 · 편 띠 높이 28 → 24(§B-2 ≤ 24) = −4 · 24-61-2 줄 46 → §B-2 ≤ 28(시안 26 + 여유 2) = −18 · 셋 다 +0.5(옛 절대값 잣대의 0.5 여유 그대로)
    #   기대식: 새 판 ≤ 바탕 − 줄어든 양 + 0.5 · 바탕 판이 없으면(pb 없음) 옛 절대값(6.5 · 24.5 · 28.5) 그대로
    if b0 and all(b0.get(k) is not None for k in ('bandGapMax', 'bandH', 'rowH')):
        th = {'bandGapMax': round(b0['bandGapMax'] - 8 + 0.5, 1), 'bandH': round(b0['bandH'] - 4 + 0.5, 1), 'rowH': round(b0['rowH'] - 18 + 0.5, 1)}
    else:
        th = {'bandGapMax': 6.5, 'bandH': 24.5, 'rowH': 28.5}
    if QJ.REGRESS:   # regress: 바탕(281c93f)을 안 띄운다 — 기준 = 앞 인도판 같은 폭(PC 900 · 옆 두 칸 접음) 값 + 0.5(글꼴 흔들림 여유) · 처음 기록은 지금 값 · 값은 다른 조건이 거짓이어도 늘 스냅샷에 적는다
        _bz = QJ.base('B2@' + p.eng, {k: (n or {}).get(k) for k in ('total', 'bandGapMax', 'bandH', 'rowH')})
        th = {k: (_bz[k] + 0.5 if isinstance(_bz.get(k), (int, float)) else 1e9) for k in ('bandGapMax', 'bandH', 'rowH')}
    T(g, 'PC 900(옆 두 칸 접음 = 시안 폭) — 편 띠 사이 ≤ 바탕 − 8 · 편 띠 높이 ≤ 바탕 − 4 · 24-61-2 줄(단원 칩 가림) ≤ 바탕 − 18 (±0.5) · 지시서 §B-2 절대값 → 상대(글꼴 무관) · 채팅 10/4 01:0x',
      n and all(n.get(k) is not None for k in ('bandGapMax', 'bandH', 'rowH')) and n['bandGapMax'] <= th['bandGapMax'] and n['bandH'] <= th['bandH'] and n['rowH'] <= th['rowH'],
      dict(n or {}, listW=(p.board() or {}).get('listW'), 바탕=b0 and {k: b0.get(k) for k in ('bandGapMax', 'bandH', 'rowH')}, 기준=th))
    if pb:
        # 옛(fix8 전): pb.go(o) · b0 = pb.ev("c=>__C2.gaps(c)", '24-61-2') 가 여기 있었다 — 위로 옮김(상대 잣대가 먼저 쓴다 · 잰 차례는 그대로 새 판 → 바탕)
        T(g, '보드 전체 높이 바탕보다 줄어듦(같은 데이터 · 같은 폭)', n and b0 and n['total'] < b0['total'],
          {'new': {k: n[k] for k in ('total', 'bandGapMax', 'bandH', 'band2head', 'bar2band', 'rowH')}, 'base': b0 and {k: b0[k] for k in ('total', 'bandGapMax', 'bandH', 'band2head', 'bar2band', 'rowH')}})
    if QJ.REGRESS:   # regress: 「바탕보다 줄어듦」 = 앞 인도판보다 안 늘어남(+0.5)
        T(g, '보드 전체 높이 바탕보다 줄어듦(같은 데이터 · 같은 폭)', bool(n) and n.get('total') is not None and n['total'] <= (_bz['total'] if isinstance(_bz.get('total'), (int, float)) else 1e9) + 0.5,
          {'new': {k: (n or {}).get(k) for k in ('total', 'bandGapMax', 'bandH', 'rowH')}, '기준': QJ.base_note('B2@' + p.eng), 'base': _bz})


def B3(p):
    g = 'B3'
    p.ev("()=>{localStorage.setItem('jopangi.c2unit',JSON.stringify({'민소|08-45-1':{main:'',s:{'(1)':[]},t:Date.now(),by:'햄찌PC'}}));return 1;}")   # 「단원 없음」 묶음 하나(합성 손값)
    b = p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}})
    seq = [(b['lv'], b['bodies'], b['rows'], b['heads'], b['bands'])]
    for _ in range(4):
        p.click(p.ev("()=>__C2.at('#slot .uzstep.c2lv')"), 900)
        x = p.board(); seq.append((x['lv'], x['bodies'], x['rows'], x['heads'], x['bands']))
    nb = p.ev("()=>{let n=0;const B=(BODYKEY===S.boardKind+'_'+PLAW()&&BODY)||{};document.querySelectorAll('#slot .c2row[data-ck]').forEach(r=>{const f=r.dataset.ck.split('|').slice(2).join('|');const rec=B[f];if(rec&&(rec.행||[]).some(x=>x.co!=='question'))n++;});return n;}")
    ok = (seq[0][0] == '펴기' and seq[1][0] == '접기1' and seq[1][1] == nb and nb > 50 and seq[1][2] > 70 and seq[2][2] == 0 and seq[2][3] == 0 and seq[2][4] == 9
          and seq[3][3] > 0 and seq[3][2] == 0 and seq[4][2] > 70 and seq[4][1] == 0 and seq[4][0] == '펴기')
    T(g, '처음 「펴기」(unit 3) → all(본문 펴짐 · 「접기1」 · ⑦ 만인 카드는 보드 본문 없음) → 1(편 띠만) → 2(단원 머리) → 3(줄 · 본문 0)', ok, [seq, nb])
    p.click(p.ev("()=>__C2.at('#slot .uzstep.c2lv')"), 900)   # → all
    p.click(p.ev("()=>__C2.at('#slot .uzstep.c2lv')"), 900)   # → 1
    b1 = p.board()
    no2 = p.ev("([k,l])=>__C2.secNo(k,l)", ['p', '2.'])
    T(g, '접기1 — 편 번호 뒤 › · 「단원 없음」 머리 보임', bool(no2) and no2['shut'] and '›' in (no2['after'] or '') and b1['unone'] == 1 and b1['heads'] == 0, [no2, b1['unone'], b1['heads']])
    p.click(no2)
    v1 = p.ev("()=>__C2.sectionView()")
    b2 = p.board()
    T(g, '「2.」 → 그 편 단원 머리만(줄 0 · 본문 0)', 'B:2. U:2.1' in v1 and b2['rows'] == 0 and b2['bodies'] == 0, v1[:300])
    p.click(p.ev("([k,l])=>__C2.secNo(k,l)", ['u', '2.1']))
    b3 = p.board(); v2 = p.ev("()=>__C2.sectionView()")
    T(g, '「2.1」 → 그 단원 줄만 · 본문 0', b3['rows'] >= 1 and b3['bodies'] == 0 and re.search(r'U:2\.1 r', v2) is not None and b3['rows'] == v2.count(' r'), [b3['rows'], v2[:300]])
    p.click(p.ev("([k,l])=>__C2.secNo(k,l)", ['p', '2.']))
    b4 = p.board(); v3 = p.ev("()=>__C2.sectionView()")
    T(g, '「2.」 한 번 더 → 그 편 단원 머리·줄 0', b4['rows'] == 0 and 'U:2.' not in v3, v3[:200])
    p.click(p.ev("([k,l])=>__C2.secNo(k,l)", ['p', '2.']))
    p.click(p.ev("()=>__C2.at('#slot .uzstep.c2lv')"), 900)   # → 2 · 번호 펼침 풀림
    b5 = p.board(); v4 = p.ev("()=>__C2.sectionView()")
    T(g, '단계 단추 → 번호 펼침 풀림(접기2 = 모든 편 단원 머리 · 줄 0)', b5['rows'] == 0 and b5['heads'] > 30 and p.ev("()=>JSON.stringify(S.c2sec||{})") == '{}', [b5['heads'], b5['rows']])
    rh = p.go({'c2ord': 'round', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}})
    r63 = p.ev("([k,l])=>__C2.secNo(k,l)", ['r', '63회'])
    p.click(r63)
    rh2 = p.board()
    T(g, '회차별 — 「63회」 누름 → 그 회차 줄만 접힘(4) · 번호 뒤 ›', r63 and rh2['rows'] == rh['rows'] - 4 and (p.ev("([k,l])=>__C2.secNo(k,l)", ['r', '63회']) or {}).get('shut'), [rh['rows'], rh2['rows']])
    p.ev("()=>{localStorage.setItem('jopangi.c2unit','{}');return 1;}")
    p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}})


def B4(p):
    g = 'B4'
    p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}})
    r0 = expand(p, '24-61-2', True)
    seq = [(r0 and r0['vis'], r0 and r0['dep'])]
    for _ in range(5):
        p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'dep']), 600)
        r = p.ev("c=>__C2.rowInfo(c)", '24-61-2'); seq.append((r['vis'], r['dep']))
    T(g, '24-61-2 제목 → 본문 23줄(헤딩만) · 깊이 4 → 5(33) → 1(2) → 2(10) → 3(21) → 4(23)', seq == [(23, '4'), (33, '5'), (2, '1'), (10, '2'), (21, '3'), (23, '4')] and r0['depFirst'], [seq, r0 and r0['depTitle']])
    pops0 = len(p.ev("()=>__C2.popsInfo()"))
    r1 = expand(p, '24-61-2', False)
    T(g, '제목 다시 → 본문 0 · 카드 창 0(줄 누름으로 안 번짐)', r1 and not r1['body'] and pops0 == 0 and len(p.ev("()=>__C2.popsInfo()")) == 0, [r1 and r1['body'], pops0])
    r2 = expand(p, '26-63-2', True)
    T(g, '헤딩 없는 본문 카드(26-63-2 · ⑦ 뺀 📄 하나) 제목 → 전부(📄 상자 보임 · 깊이 1)', r2 and r2['body'] and r2['callouts'] == 1 and r2['dep'] == '1' and r2['coq'] == 0, r2 and {k: r2[k] for k in ('body', 'callouts', 'dep', 'coq')})
    expand(p, '26-63-2', False)


def B5(p):
    g = 'B5'
    p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}})
    r = p.ev("c=>__C2.rowInfo(c)", '24-61-2')
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'q1']))
    q = p.ev("()=>__C2.qPop()")
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'q1']))
    q2 = p.ev("()=>__C2.qPop()")
    T(g, '24-61-2 두루마리 → 문제 창 1(제목 「⑦ …」) · 다시 → 0', bool(r and r['q1']) and bool(q) and q['t'].startswith('⑦') and q2 is None, [r and r['q1Title'], q, q2])
    r8 = p.ev("c=>__C2.rowInfo(c)", '08-45-1')
    T(g, '08-45-1(⑦ 없음) 두루마리 0', r8 is not None and not r8['q1'], r8 and r8['q1'])
    qo = p.ev("""c=>{const r=[...document.querySelectorAll('#slot .c2row')].find(x=>!x.classList.contains('c2ov')&&(((x.querySelector('.c2code')||{}).textContent)||'').trim().indexOf(c)===0);
      const e=r&&r.querySelector('.c2code');return e?{qok:e.classList.contains('c2qok'),title:e.title||'',cursor:getComputedStyle(e).cursor}:null;}""", '24-61-2')
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'code']))
    c1 = p.ev("c=>__C2.card(c)", '24-61-2')
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'code']))
    c2 = p.ev("c=>__C2.card(c)", '24-61-2')
    T(g, '코드 숫자(.c2qok · 손가락 · title 「눌러서 카드 창(문제·해설·채점)」) → 카드 창 1 · 다시 → 0',
      bool(qo) and qo['qok'] and qo['cursor'] == 'pointer' and qo['title'] == '눌러서 카드 창(문제·해설·채점)' and c1 is not None and c2 is None, [qo, c1 and c1['title'], c2])
    r2 = expand(p, '24-61-2', True)
    T(g, '보드 본문에 co-question 0', r2 and r2['coq'] == 0 and r2['body'], r2 and r2['coq'])
    expand(p, '24-61-2', False)


# ★ fix8 — .main 내용 상자 오른쪽 끝(Rc = 안쪽 오른쪽 R − padding-right)을 넘는 요소 · 바깥쪽만(넘친 조상 아래는 안 셈) · dR = 안쪽 오른쪽 R 을 넘은 양 ·
#   svg.c2ml(스크롤 폭을 따라 그리는 점선 판 = 결과)·메모 창(자리 잣대가 따로)은 뺌 · 글 노드 = 상자는 안 넘고 글만 넘는 것 · a = {t: 글 몇 자, k: 몇 개}
OVX_JS = r"""(a)=>{const m=document.querySelector('#slot .main');if(!m)return null;const mr=m.getBoundingClientRect(),cs=getComputedStyle(m);
  const R=mr.left+m.clientLeft+m.clientWidth,Rc=R-(parseFloat(cs.paddingRight)||0),T=(a&&a.t)||16,K=(a&&a.k)||4;
  const desc=e=>{const c=String(e.getAttribute('class')||'').trim().split(/\s+/).filter(Boolean).slice(0,3);return e.tagName.toLowerCase()+(c.length?'.'+c.join('.'):'');};
  const skip=e=>!!e.closest('svg.c2ml,.pop.mpop');
  const ckOf=e=>{const r=e.closest('.c2row');return r?String(r.dataset.ck||r.dataset.ckx||'').split('|').slice(2).join('|').slice(0,24):'';};
  const seen=new Set(),el=[];let n=0;
  for(const e of m.querySelectorAll('*')){if(skip(e))continue;const r=e.getBoundingClientRect();if(!(r.width||r.height)||r.right<=Rc+1)continue;
    let q=e.parentElement,inn=false;while(q&&q!==m){if(seen.has(q)){inn=true;break;}q=q.parentElement;}seen.add(e);if(inn)continue;n++;
    if(el.length<K)el.push({s:desc(e),r:Math.round(r.right),w:Math.round(r.width),dR:Math.round(r.right-R),t:String(e.textContent||'').replace(/\s+/g,' ').trim().slice(0,T),ck:ckOf(e),ws:getComputedStyle(e).whiteSpace});}
  const tw=document.createTreeWalker(m,NodeFilter.SHOW_TEXT),rg=document.createRange(),tx=[];let tn=0,x;
  while((x=tw.nextNode())){if(!x.nodeValue.trim())continue;const pe=x.parentElement;if(!pe||skip(pe))continue;rg.selectNodeContents(x);const b=rg.getBoundingClientRect();if(b.right<=Rc+1)continue;
    let q=pe,inS=false;while(q&&q!==m){if(seen.has(q)){inS=true;break;}q=q.parentElement;}if(inS)continue;tn++;
    if(tx.length<K)tx.push({s:desc(pe),r:Math.round(b.right),w:Math.round(b.width),dR:Math.round(b.right-R),t:x.nodeValue.replace(/\s+/g,' ').trim().slice(0,T),ck:ckOf(pe)});}
  const sv=m.querySelector(':scope > svg.c2ml'),mp=[...m.querySelectorAll(':scope > .pop.mpop')].map(p=>Math.round(p.getBoundingClientRect().right));
  return {sw:m.scrollWidth,cw:m.clientWidth,R:Math.round(R),Rc:Math.round(Rc),n:n,el:el,tn:tn,tx:tx,svg:sv?[sv.getAttribute('width'),sv.getAttribute('height')]:null,mpR:mp.length?Math.max(...mp):null};}"""


def B6(p, pphone):
    g = 'B6'
    p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'c2mx': {}, 'c2memo': {}})
    expand(p, '24-61-2', True)
    p.idle(500)
    m = p.ev("()=>__C2.memo()")
    ln = p.ev("()=>__C2.lines()")
    T(g, '24-61-2 펴면 메모 창 2(.main 안 absolute) · 점선 2', len(m) == 2 and all(x['mode'] == 'b' and x['inMain'] and x['pos'] == 'absolute' for x in m) and len(ln['b']) == 2,
      [[(x['title'], x['pos'], x['inMain']) for x in m], len(ln['b'])])
    # 옛(fix8 전 · 폭 240 고정 — 웹킷 묶음은 폰으로만 돈다 main()):
    # T(g, '창 머리 높이 ≤ 21px · 글 11px · 폭 PC 240', bool(m) and all(x['headH'] <= 21 and x['textFs'] == '11px' and abs(x['w'] - 240) < 1 for x in m), [(x['headH'], x['textFs'], x['w']) for x in m])
    lw = p.ev("()=>{const l=document.querySelector('#slot .main .c2list');return {lw:l?l.clientWidth:0,iw:innerWidth};}")   # ★ fix8
    W0 = 240 if lw['lw'] > 560 else min(230, lw['iw'] - 24)   # ★ fix8 — 지시서 A-7-6 「폭: 보드 = 넓은 화면(컨테이너 > 560) 240px · 좁은 화면 min(230, innerWidth-24)」 · §B-6 「폭 PC 240 / 폰 230」 · 앱 c2MemoBoard W0 같은 식 · 결정로그 10/3 22:36
    T(g, '창 머리 높이 ≤ 21px · 글 11px · 폭 PC 240 / 폰 230', bool(m) and all(x['headH'] <= 21 and x['textFs'] == '11px' and abs(x['w'] - W0) < 1 for x in m),
      [(x['headH'], x['textFs'], x['w']) for x in m] + [{'기대 폭': W0, '.c2list': lw['lw'], 'innerWidth': lw['iw']}])   # ★ fix8
    rel0 = [(x['rect']['x'] - x['word']['x'], x['rect']['y'] - x['word']['y']) for x in m if x['word']]
    t0 = p.ev("()=>__C2.mainTop()")
    p.ev("v=>__C2.setMainTop(v)", (t0 or 0) + 120); p.idle(300)
    m2 = p.ev("()=>__C2.memo()")
    rel1 = [(x['rect']['x'] - x['word']['x'], x['rect']['y'] - x['word']['y']) for x in m2 if x['word']]
    T(g, '보드 굴림 → 창·점선이 낱말과 같이 움직임(낱말−창 상대 위치 무변)', len(rel0) == 2 and all(abs(a[0] - b[0]) < 1.5 and abs(a[1] - b[1]) < 1.5 for a, b in zip(rel0, rel1)) and m2[0]['rect']['y'] != m[0]['rect']['y'],
      [rel0, rel1])
    p.ev("v=>__C2.setMainTop(v)", t0 or 0); p.idle(200)
    # 카드 창을 먼저 열고 보드를 다시 그려도 메모 창이 카드 창 위로 안 올라옴
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['13-50-2', 'code']))
    p.ev("()=>__C2.rerender()"); p.idle(400)
    z = p.ev("""()=>{const c=[...POPS].find(q=>/13-50-2/.test(q.querySelector('.ph .pt').textContent));const cz=c?+c.style.zIndex:0;const cr=c?c.getBoundingClientRect():null;
      const ws=[...document.querySelectorAll('.pop.mpop.mb')];let over=0,hitCard=0;ws.forEach(w=>{const r=w.getBoundingClientRect();if(!cr)return;const x0=Math.max(r.left,cr.left),x1=Math.min(r.right,cr.right),y0=Math.max(r.top,cr.top),y1=Math.min(r.bottom,cr.bottom);
      if(x1>x0+4&&y1>y0+4){over++;const a=document.elementFromPoint((x0+x1)/2,(y0+y1)/2);if(a&&c.contains(a))hitCard++;}});return {cz,mz:ws.map(w=>+getComputedStyle(w).zIndex),over,hitCard};}""")
    T(g, '창을 다시 지어도 열린 카드 창보다 위로 안 올라옴(메모 z < 카드 z · 겹친 자리 = 카드)', z['cz'] > 0 and all(v < z['cz'] for v in z['mz']) and z['over'] == z['hitCard'], z)
    p.ev("()=>__C2.closeAll()"); p.idle(200)
    ov = p.ev("()=>__C2.overflow()")
    T(g, '가로 넘침 0(보드 · 메모 창 오른쪽 끝 ≤ .main 안쪽 − 8)', ov['main'][0] <= ov['main'][1] and ov['docW'][0] <= ov['docW'][1], ov)
    # 낱말 누름 · ✕ · 본문 접고 펴기
    # 옛(fix8 전): p.click(p.ev("([c,w])=>__C2.wordAt(c,w)", ['24-61-2', '합의관할']))
    wd, wat = '합의관할', None
    for w_ in ('합의관할', '설문(1)'):   # ★ fix8 — 폰(좁은 화면)은 창이 낱말 아래(지시서 A-7-6 ③ y = 낱말 bottom+22 · 겹치면 아래로)라 「설문(1)」 창이 「합의관할」 낱말을 통째로 덮는다(10/4 웹킷 폰 값) → hit().on 이 참인 낱말 · PC 는 지금처럼 「합의관할」 · 결정로그 10/3 22:36
        a_ = p.ev("([c,w])=>__C2.wordAt(c,w)", ['24-61-2', w_])
        if a_ and a_.get('on'):
            wd, wat = w_, a_
            break
    p.click(wat)
    n1 = len(p.ev("()=>__C2.memo()"))
    # 옛(fix8 전): p.click(p.ev("([c,w])=>__C2.wordAt(c,w)", ['24-61-2', '합의관할']))
    p.click(p.ev("([c,w])=>__C2.wordAt(c,w)", ['24-61-2', wd]))   # ★ fix8 — 첫 누름과 같은 낱말
    n2 = len(p.ev("()=>__C2.memo()"))
    p.click(p.ev("([i,x])=>__C2.memoPart(i,x)", [0, 'x']))
    n3 = len(p.ev("()=>__C2.memo()"))
    expand(p, '24-61-2', False); expand(p, '24-61-2', True); p.idle(300)
    n4 = len(p.ev("()=>__C2.memo()"))
    # 옛(fix8 전): T(g, '낱말 누름 → 1 · 다시 → 2 · ✕ → 1 · 본문 접고 펴기 → 2', [n1, n2, n3, n4] == [1, 2, 1, 2], [n1, n2, n3, n4])
    T(g, '낱말 누름 → 1 · 다시 → 2 · ✕ → 1 · 본문 접고 펴기 → 2', [n1, n2, n3, n4] == [1, 2, 1, 2], [n1, n2, n3, n4, wd if wat else '안 덮인 낱말 없음'])   # ★ fix8 — 값 끝 = 누른 낱말
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'memo']))
    k1 = len(p.ev("()=>__C2.memo()"))
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'memo']), 900)
    k2 = len(p.ev("()=>__C2.memo()"))
    expand(p, '24-61-2', False)
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'memo']), 900)
    ri = p.ev("c=>__C2.rowInfo(c)", '24-61-2'); k3 = len(p.ev("()=>__C2.memo()"))
    T(g, '메모 칩 → 0 → 칩 → 2 · 본문 접힌 채 칩 → 본문 펴지고 2', [k1, k2, k3] == [0, 2, 2] and ri['body'], [k1, k2, k3, ri['body'], ri['memoTitle']])
    p.long(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'memo']))
    k4 = len(p.ev("()=>__C2.memo()")); ts = p.ev("()=>__C2.toasts()")
    lists = [x for x in p.ev("()=>__C2.popsInfo()") if x['t'].startswith('🗒 메모')]
    T(g, '칩 길게 → 0 + 토스트 「이 문제 메모 창 2개를 닫음」 · 목록 창 0', k4 == 0 and any('메모 창 2개를 닫음' in t for t in ts) and not lists, [k4, ts[-2:], lists])
    # GS 줄(셋째 칸 빈 줄)에 합성 메모 하나 — 가로 넘침
    p.ev("""()=>{ const P=__C2.pit(); P['card|GS|곽민실전A-26-1회-1-목사-소능중단간과-제소전사망간과판결시효중단효'+'\u001f'+'0'+'\u001f'+'2'+'\u001f'+'설문(1)']={t:'GS 넘침 대조(합성)',who:'햄찌',at:'2026-10-03T01:00:00.000Z',ts:'2026-10-03T01:00:00.000Z'}; return __C2.setPit(P); }""")
    p.go({'boardKind': 'GS', 'c2lv': {'unit': 3, 'round': 'all'}, 'c2sec': {}, 'c2rl': {}, 'c2mx': {}})
    p.idle(800)
    mg = p.ev("()=>__C2.memo()"); ov2 = p.ev("()=>__C2.overflow()")
    gsr = p.ev("()=>{const w=[...document.querySelectorAll('.pop.mpop.mb')][0];const r=w&&w._row;const r3=r&&r.querySelector('.c2r3');return r?{r3:!!(r3&&r3.childNodes.length),rowR:Math.round(r.getBoundingClientRect().right),win:w.getBoundingClientRect().right,main:document.querySelector('#slot .main').getBoundingClientRect().right}:null;}")
    # 옛(fix8 전 · 판정 그대로 · 값만 보탬): T(g, 'GS 줄(셋째 칸 빈 줄) 메모 창 — 가로 넘침 0 · 창 오른쪽 끝 ≤ .main 안쪽 − 8', len(mg) >= 1 and ov2['main'][0] <= ov2['main'][1] and gsr and gsr['win'] <= gsr['main'] - 8 + 1 and not gsr['r3'], [len(mg), ov2['main'], gsr])
    ovx = p.ev(OVX_JS, {'t': 16, 'k': 4}) or {}   # ★ fix8 — 넘친 요소(가름 보고 미상 14 재료 · 판정 무변)
    T(g, 'GS 줄(셋째 칸 빈 줄) 메모 창 — 가로 넘침 0 · 창 오른쪽 끝 ≤ .main 안쪽 − 8', len(mg) >= 1 and ov2['main'][0] <= ov2['main'][1] and gsr and gsr['win'] <= gsr['main'] - 8 + 1 and not gsr['r3'],
      [len(mg), ov2['main'], gsr, {k: ovx.get(k) for k in ('sw', 'cw', 'R', 'Rc', 'n', 'tn', 'mpR', 'svg')}])   # ★ fix8 — 판정 무변 · 값 끝에 넘침 요약
    N(g, 'GS 줄 넘친 요소(.main 안쪽 오른쪽 끝을 넘는 바깥쪽 요소 · 판정 무변)', {'el': ovx.get('el'), 'off': (ov2 or {}).get('off')})   # ★ fix8 — 선택자 · 오른쪽 끝 · 폭 · 넘은 양 dR · 글 16자 · 줄 파일
    N(g, 'GS 줄 넘친 글 노드(상자는 안 넘고 글만 · 판정 무변)', {'tx': ovx.get('tx')})   # ★ fix8
    p.ev("()=>{const P=__C2.pit();Object.keys(P).forEach(k=>{if(k.indexOf('card|GS|')===0)delete P[k];});return __C2.setPit(P);}")
    p.go({'boardKind': '기출', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'c2mx': {}})
    if pphone:
        pphone.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'c2mx': {}, 'c2memo': {}})
        expand(pphone, '24-61-2', True); pphone.idle(500)
        mp = pphone.ev("()=>__C2.memo()"); ovp = pphone.ev("()=>__C2.overflow()")
        T(g, '폰 390 — 메모 창 2 · 폭 230 · 화면 안(가로 넘침 0)', len(mp) == 2 and all(abs(x['w'] - 230) < 1 and x['rect']['x'] >= 0 and x['rect']['r'] <= 390 for x in mp) and ovp['docW'][0] <= ovp['docW'][1],
          [[(x['w'], x['rect']['x'], x['rect']['r']) for x in mp], ovp['docW']])


def B7(p):
    g = 'B7'
    p.ev("o=>__C2.setPit(o)", PIT0)
    p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'c2mx': {}, 'c2memo': {}})
    expand(p, '24-61-2', True); p.idle(400)
    ia = p.ev("([w,m])=>__C2.memoIdx(w,m)", ['설문(1)', 'b'])
    p.long(p.ev("([i,x])=>__C2.memoPart(i,x)", [ia, 'text']))
    ed = p.ev("()=>__C2.memo()")
    T(g, '글 길게 → 그 자리 편집(textarea 1 · ✎ 저장 · 취소 · 🗑 삭제)', ia >= 0 and ed[ia]['edit'], [ia, [x['edit'] for x in ed]])
    p.ev("([i,v])=>__C2.memoType(i,v)", [ia, '고친 글(합성)'])
    p.click(p.ev("([i,x])=>__C2.memoPart(i,x)", [ia, 'save']))
    v = p.ev("()=>__C2.pit()")[PK_A]
    m = p.ev("()=>__C2.memo()")
    ia = p.ev("([w,m])=>__C2.memoIdx(w,m)", ['설문(1)', 'b'])
    T(g, '고쳐 저장 → postit 그 칸 t 바뀜 · at·who 같음 · et 생김 · 「· 고침」', v['t'] == '고친 글(합성)' and v['at'] == PIT0[PK_A]['at'] and v['who'] == '햄찌' and bool(v.get('et')) and '고침' in m[ia]['meta'], [v, m[ia]['meta']])
    ib = p.ev("([w,m])=>__C2.memoIdx(w,m)", ['합의관할', 'b'])
    p.click(p.ev("([i,x])=>__C2.memoPart(i,x)", [ib, 'cl']))
    mb = p.ev("()=>__C2.memo()")
    foc = p.ev("()=>document.activeElement&&document.activeElement.closest('.madd')?1:0")
    p.pg.keyboard.type('테스트'); p.key('Enter')
    vb = p.ev("()=>__C2.pit()")[PK_B]; mb2 = p.ev("()=>__C2.memo()"); ib = p.ev("([w,m])=>__C2.memoIdx(w,m)", ['합의관할', 'b'])
    T(g, '「댓글」 → 칸(포커스) → 「테스트」 Enter → re 1(who 햄찌) · 입력 닫힘 · 댓글만 단 메모엔 「고침」 없음',
      mb[ib]['add'] and foc == 1 and len(vb.get('re') or []) == 1 and vb['re'][0]['who'] == '햄찌' and vb['re'][0]['t'] == '테스트' and not mb2[ib]['add'] and '고침' not in mb2[ib]['meta'] and not vb.get('et'),
      [vb.get('re'), mb2[ib]['meta'], mb2[ib]['re']])
    p.click(p.ev("([i,x])=>__C2.memoPart(i,x)", [ib, 'cl']))
    p.pg.keyboard.type('지울 글'); p.key('Escape')
    mb3 = p.ev("()=>__C2.memo()"); ib = p.ev("([w,m])=>__C2.memoIdx(w,m)", ['합의관할', 'b'])
    T(g, 'Esc → 댓글 칸 비우고 닫힘(댓글 그대로 1)', not mb3[ib]['add'] and len(p.ev("()=>__C2.pit()")[PK_B].get('re') or []) == 1, mb3[ib]['add'])
    # 댓글 단 메모를 pitAsk 「🗒 메모 붙이기」 길(pitEdit)로 고쳐 저장 → re 그대로
    p.ev("([k,v])=>__C2.pitEditSave(k,v)", [PK_B, '메모 붙이기 길로 고침(합성)']); p.idle(600)
    vb2 = p.ev("()=>__C2.pit()")[PK_B]
    T(g, '댓글 단 메모를 pitAsk 「🗒 메모 붙이기」 길(pitEdit)로 고쳐 저장 → re 그대로', vb2['t'] == '메모 붙이기 길로 고침(합성)' and len(vb2.get('re') or []) == 1, vb2)
    expand(p, '24-61-2', False); expand(p, '24-61-2', True); p.idle(400)
    ib = p.ev("([w,m])=>__C2.memoIdx(w,m)", ['합의관할', 'b'])
    p.long(p.ev("([i,x])=>__C2.memoPart(i,x)", [ib, 'reText']))
    p.click(p.ev("([i,x])=>__C2.memoPart(i,x)", [ib, 'del']))
    vb3 = p.ev("()=>__C2.pit()")[PK_B]
    T(g, '댓글 길게 → 🗑 삭제 → re 0(메모는 그대로)', vb3 and len(vb3.get('re') or []) == 0 and vb3['t'] == '메모 붙이기 길로 고침(합성)', vb3)
    fl = p.ev("()=>__C2.flags()")
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'code']), 800)
    fl2 = p.ev("()=>__C2.flags()")
    p.ev("()=>__C2.closeAll()")
    pf = p.ev("id=>__C2.prec(id)", PREC_ID)
    T(g, '깃발(.pitflag) 보이는 수 0(보드 · 카드) · 판례 카드 깃발 그대로 보임', fl['board'] == 0 and fl2['card'] == 0 and pf >= 1, [fl, fl2, pf])


def B8(p):
    g = 'B8'
    p.ev("o=>__C2.setPit(o)", PIT0)
    p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'c2mx': {}, 'c2memo': {}})
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'code']), 900)
    c = p.ev("c=>__C2.card(c)", '24-61-2'); m = [x for x in p.ev("()=>__C2.memo()") if x['mode'] == 'c']
    side = all(x['rect']['x'] >= c['rect']['r'] + 8 or abs(x['rect']['r'] - (1440 - 10)) < 2 for x in m) if c else False
    T(g, '코드 → 카드 창 + 메모 창 2(카드 오른쪽 또는 화면 오른쪽 · fixed)', c is not None and len(m) == 2 and side and all(x['pos'] == 'fixed' for x in m), [c and c['rect'], [(x['rect'], x['pos']) for x in m]])
    hd = c['head']
    p.drag(hd['cx'], hd['cy'], hd['cx'] - 160, hd['cy'] + 50)
    c2 = p.ev("c=>__C2.card(c)", '24-61-2'); m2 = [x for x in p.ev("()=>__C2.memo()") if x['mode'] == 'c']
    dx, dy = c2['rect']['x'] - c['rect']['x'], c2['rect']['y'] - c['rect']['y']
    T(g, '카드 머리 끌기 → 메모 창 같은 만큼', abs(dx + 160) < 3 and abs(dy - 50) < 3 and len(m2) == 2 and all(abs((b['rect']['x'] - a['rect']['x']) - dx) < 2 and abs((b['rect']['y'] - a['rect']['y']) - dy) < 2 for a, b in zip(m, m2)),
      [dx, dy, [(round(b['rect']['x'] - a['rect']['x'], 1), round(b['rect']['y'] - a['rect']['y'], 1)) for a, b in zip(m, m2)]])
    fs = []
    for _ in range(4):
        p.click(p.ev("c=>__C2.cardFold(c)", '24-61-2'), 500)
        fs.append(len([x for x in p.ev("()=>__C2.memo()") if x['mode'] == 'c']))
    p.click(p.ev("c=>__C2.cardFold(c)", '24-61-2'), 500)
    f5 = len([x for x in p.ev("()=>__C2.memo()") if x['mode'] == 'c'])
    T(g, '「접기 n」으로 낱말 숨김 → 그 창 0(접기 4 = 「2. 합의관할」 숨음 → 1) · 접기 0 → 2', fs[-1] == 1 and f5 == 2, [fs, f5, p.ev("c=>__C2.card(c)", '24-61-2')['fold']])
    p.click(p.ev("()=>__C2.atIn('.pop.k-cell', '.ph > button:not(.pall)')"))
    T(g, '카드 닫기 → 그 메모 창 0', len([x for x in p.ev("()=>__C2.memo()") if x['mode'] == 'c']) == 0 and p.ev("c=>__C2.card(c)", '24-61-2') is None, p.ev("()=>__C2.popsInfo()"))
    expand(p, '24-61-2', True)
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'code']), 900)
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'q1']), 600)
    n0 = len(p.ev("()=>__C2.memo()"))
    pa = p.ev("()=>__C2.pall()")
    p.click(pa, 600)
    n1 = len(p.ev("()=>__C2.memo()")); pp = p.ev("()=>__C2.popsInfo()")
    p.ev("()=>__C2.rerender()"); p.idle(400)
    n2 = len(p.ev("()=>__C2.memo()"))
    T(g, '「모두 닫기」 → 메모 창 0(보드 · 카드) · 다음 render 에도 0', n0 == 4 and pa is not None and n1 == 0 and not pp and n2 == 0, [n0, bool(pa), n1, len(pp), n2])
    expand(p, '24-61-2', False)
    p.go({'boardKind': '사례'}); p.idle(1500)
    sk = p.ev("()=>({miss:document.querySelectorAll('#slot .c2miss').length,lnk:document.querySelectorAll('#slot .c2lnk').length,bodies:document.querySelectorAll('#slot .rbody').length})")
    p.go({'boardKind': '기출', 'c2ord': 'unit'})
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'q1']), 600)
    qq = p.ev("()=>{const p=[...POPS].find(q=>/^⑦/.test(q.querySelector('.ph .pt').textContent));return p?{miss:p.querySelectorAll('.c2miss').length,lnk:p.querySelectorAll('.c2lnk').length}:null;}")
    T(g, '사례 격자 본문 · 문제 창에 .c2miss·.c2lnk 0', sk['bodies'] > 0 and sk['miss'] == 0 and sk['lnk'] == 0 and qq and qq['miss'] == 0 and qq['lnk'] == 0, [sk, qq])
    p.ev("()=>__C2.closeAll()")


def B9(p):
    g = 'B9'
    p.ev("o=>__C2.setPit(o)", {})
    p.ev("o=>__C2.setMiss(o)", {})
    p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'c2mx': {}})
    expand(p, '24-61-2', True)
    L = '2. 합의관할'
    p.click(p.ev("([c,s])=>__C2.missBtn(c,s)", ['24-61-2', L]))
    p.ev("()=>__C2.stamp()")   # 앱의 10초 도장(setInterval stampAll) 대신 — 그림자에 칸이 있어야 다 지우기 때 묘비가 선다
    a = p.ev("([c,s])=>__C2.lineInfo(c,s)", ['24-61-2', L]); ls = p.ev("()=>__C2.missLS()")
    T(g, '「2. 합의관할…」 누락 → 빨강 단추 「누락 · MM.DD」 · 줄 box-shadow 빨강 · 기록 칸 1',
      a and re.match(r'^누락 · \d\d\.\d\d$', a['btn']['t']) and 'm-r' in a['btn']['cls'] and '220, 38, 38' in (a['shadow'] or '') and len(ls) == 1, [a and a['btn'], a and a['shadow'], ls])
    st = []
    for btn in ('극복', '극복', '+ 누락'):
        p.click(p.ev("([c,s])=>__C2.missBtn(c,s)", ['24-61-2', L]))
        if btn == '극복' and not st:
            mm = p.ev("()=>__C2.missMenu()"); N(g, '메뉴(빨강 상태)', mm)
        p.click(p.ev("t=>__C2.missMenuBtn(t)", btn))
        x = p.ev("([c,s])=>__C2.lineInfo(c,s)", ['24-61-2', L]); st.append((x['btn']['t'], x['btn']['cls']))
    ok = (st[0][0].startswith('극복 ·') and 'm-o' in st[0][1] and st[1][0].startswith('극복 2 ·') and 'm-y' in st[1][1] and st[2][0].startswith('누락 2 ·') and 'm-r' in st[2][1])
    T(g, '메뉴 극복 → 주황 · 극복 → 노랑 「극복 2」 · + 누락 → 빨강 「누락 2」', ok, st)
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'code']), 900)
    cl = p.ev("([c,s,k])=>__C2.lineInfo(c,s,k)", ['24-61-2', L, True])
    T(g, '카드 창에서도 같은 칸 같은 색(빨강 「누락 2」)', cl and cl['btn']['t'] == st[2][0] and 'm-r' in cl['btn']['cls'] and '220, 38, 38' in (cl['shadow'] or ''), cl and [cl['btn'], cl['shadow']])
    p.ev("()=>__C2.closeAll()")
    p.click(p.ev("([c,s])=>__C2.missBtn(c,s)", ['24-61-2', L]))
    mm = p.ev("()=>__C2.missMenu()")
    p.click(p.ev("i=>__C2.missMenuDel(i)", 3))
    y = p.ev("([c,s])=>__C2.lineInfo(c,s)", ['24-61-2', L])
    T(g, '마지막(방금 + 누락) 기록 ✕ → 노랑 「극복 2」', mm and len(mm['rows']) == 4 and y['btn']['t'].startswith('극복 2 ·') and 'm-y' in y['btn']['cls'], [mm and mm['rows'], y['btn']])
    p.click(p.ev("([c,s])=>__C2.missBtn(c,s)", ['24-61-2', L]))
    p.click(p.ev("t=>__C2.missMenuBtn(t)", '다 지우기'))
    z = p.ev("([c,s])=>__C2.lineInfo(c,s)", ['24-61-2', L]); ls2 = p.ev("()=>__C2.missLS()")
    p.ev("()=>__C2.stamp()")
    gone = [k for k in p.ev("()=>__C2.syncState()")['gone'] if k.startswith('jopangi.c2miss|')]
    T(g, '다 지우기 → 칸 지움(묘비 jopangi_sync_gone) · 색 0 · 단추 「누락」', not ls2 and z['btn']['t'] == '누락' and 'missed' not in z['cls'] and len(gone) == 1, [ls2, z['btn'], gone])
    expand(p, '24-61-2', False)


def B10(p):
    g = 'B10'
    p.ev("o=>__C2.setPit(o)", {})
    p.ev("o=>__C2.setMiss(o)", {})
    p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'c2mx': {}})
    expand(p, '24-61-2', True)
    mk = p.ev("""()=>{const r=[...document.querySelectorAll('#slot .c2row')].find(x=>x.dataset.ck&&x.dataset.ck.indexOf('24-61-2')>0);const L=[...r.querySelectorAll('.c2bw .rbody > .rln')];
      const f=s=>{const n=L.find(x=>x.textContent.replace(/\\s+/g,' ').indexOf(s)>=0);return n&&n.querySelector(':scope > .c2miss')?n.querySelector(':scope > .c2miss').dataset.mk:null;};return [f('2. 합의관할'),f('(2) 요건'),f('① 원칙')];}""")
    t = ['2026-10-01T01:00:00.000Z', '2026-10-02T01:00:00.000Z', '2026-10-03T01:00:00.000Z']
    o = {mk[0]: {'h': [{'ts': t[0], 'who': '햄찌', 'r': 'x'}, {'ts': t[1], 'who': '햄찌', 'r': 'o'}, {'ts': t[2], 'who': '햄찌', 'r': 'o'}]},
         mk[1]: {'h': [{'ts': t[0], 'who': '햄찌', 'r': 'x'}]},
         mk[2]: {'h': [{'ts': t[0], 'who': '꼬까', 'r': 'x'}, {'ts': t[1], 'who': '꼬까', 'r': 'o'}]}} if all(mk) else {}
    p.ev("o=>__C2.setMiss(o)", o)
    res = {}

    def cls(s):
        x = p.ev("([c,s])=>__C2.lineInfo(c,s)", ['24-61-2', s])
        if not x or not x['vis']:
            return '-'
        m_ = re.search(r'\bm-([roy])\b', x['cls'])
        return (m_.group(1) if m_ and 'missed' in x['cls'] else '0') + ('A' if ' agg' in x['cls'] or x['cls'].endswith('agg') else '')
    probe = ['Ⅰ. 설문(1)', '2. 합의관할', '(2) 요건', 'Ⅱ. 설문(2)', '2. 제34조', '(2) 사물관할', '① 원칙']
    p.ev("()=>__C2.rerender()")
    for d in ('4', '5', '1', '2', '3'):
        for _ in range(6):
            cur = p.ev("c=>__C2.rowInfo(c)", '24-61-2')['dep']
            if cur == d:
                break
            p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'dep']), 500)
        res[d] = [cls(s) for s in probe]
    T(g, '깊이 4·5 = 세 줄 자기 색만(노랑 2. 합의관할 · 빨강 (2) 요건 · 주황 ① 원칙)', mk and res['4'] == ['0', 'y', 'r', '0', '0', '0', 'o'] and res['5'] == res['4'], [mk, res['4'], res['5']])
    T(g, '깊이 1 → Ⅰ 빨강 · Ⅱ 주황(접힌 아래 쟁점 중 가장 진한 색 · agg)', res['1'][0] == 'rA' and res['1'][3] == 'oA', res['1'])
    T(g, '깊이 2 → 「2. 합의관할」 빨강(agg) · 「2. 제34조」 주황 · 깊이 3 → 「(2) 사물관할」 주황', res['2'][1] == 'rA' and res['2'][4] == 'oA' and res['3'][5] == 'oA' and res['3'][2] == 'r', [res['2'], res['3']])
    expand(p, '24-61-2', False)
    ri = p.ev("c=>__C2.rowInfo(c)", '24-61-2')
    T(g, '본문 접음 → 문제 줄 「누락 3」 빨강 + 왼쪽 4px', ri['mchip'] == '누락 3' and 'm-r' in (ri['mchipCls'] or '') and 'rmiss' in ri['rmiss'] and 'inset' in (ri['shadow'] or '') and '220, 38, 38' in (ri['shadow'] or ''), [ri['mchip'], ri['rmiss'], ri['shadow']])
    expand(p, '24-61-2', True)
    for _ in range(6):
        if p.ev("c=>__C2.rowInfo(c)", '24-61-2')['dep'] == '5':
            break
        p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'dep']), 500)
    ri2 = p.ev("c=>__C2.rowInfo(c)", '24-61-2')
    T(g, '다 보이게 펴면 문제 줄 표시 0', ri2['dep'] == '5' and not ri2['mchip'] and 'rmiss' not in ri2['rmiss'], [ri2['dep'], ri2['mchip'], ri2['rmiss']])
    p.ev("o=>__C2.setMiss(o)", {})
    expand(p, '24-61-2', False)


def B11(p):
    g = 'B11'
    p.ev("o=>__C2.setPit(o)", {}); p.ev("()=>localStorage.setItem('jopangi.c2qlink','{}')")
    p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'c2mx': {}})
    expand(p, '24-61-2', True)
    p.click(p.ev("([c,s,k,x])=>__C2.lnkBtn(c,s,k,x)", ['24-61-2', 'Ⅱ.', False, 'none']))
    m0 = p.ev("()=>__C2.lkm()")
    p.ev("v=>__C2.lkmType(v)", '13-50-2'); p.idle(300)
    m1 = p.ev("()=>__C2.lkm()")
    p.click(p.ev("([s,r,i])=>__C2.lkmItem(s,r,i)", ['.ai', '설문\\(1\\)', 0]))
    a = p.ev("([c,s])=>__C2.lineInfo(c,s)", ['24-61-2', 'Ⅱ.']); ql = p.ev("()=>__C2.qlLS()")
    T(g, '24-61-2 Ⅱ 고리 → 「13-50-2」 → 후보(Ⅰ·Ⅱ) → 고름 → Ⅱ 파랑(나감)', m0 and m0['focus'] and m1 and len(m1['ai']) == 2 and a and a['lnk'] and a['lnk'][0]['cls'] == 'c2lnk out' and len(ql) == 1,
      [m0 and m0['head'], m1 and m1['ai'], a and a['lnk'], list(ql)[:1]])
    p.click(p.ev("([c,s,k,x])=>__C2.lnkBtn(c,s,k,x)", ['24-61-2', 'Ⅱ.', False, 'out']))
    p.ev("v=>__C2.lkmType(v)", '이송'); p.idle(300)
    m2 = p.ev("()=>__C2.lkm()")
    p.click(p.ev("([s,r,i])=>__C2.lkmItem(s,r,i)", ['.ai', '.', 0]))
    a2 = p.ev("([c,s])=>__C2.lineInfo(c,s)", ['24-61-2', 'Ⅱ.'])
    T(g, '「이송」으로 하나 더 → 「2」(::after 수 · 줄 글자 노드 0)', a2 and a2['lnk'] and a2['lnk'][0]['n'] == '2' and '2' in (a2['lnk'][0]['after'] or ''), [m2 and m2['ai'][:3], a2 and a2['lnk']])
    expand(p, '13-50-2', True)
    b = p.ev("([c,s])=>__C2.lineInfo(c,s)", ['13-50-2', 'Ⅰ.'])
    p.click(p.ev("([c,s,k,x])=>__C2.lnkBtn(c,s,k,x)", ['13-50-2', 'Ⅰ.', False, 'in']))
    mb = p.ev("()=>__C2.lkm()")
    T(g, '13-50-2 펴면 Ⅰ 보라 ↩(들어옴) · 누르면 「빽링크 1 · 24-61-2 Ⅱ…」', b and any(x['cls'] == 'c2lnk in' for x in b['lnk']) and mb and mb['secs'] == ['빽링크 1'] and '24-61-2' in mb['li'][0] and 'Ⅱ' in mb['li'][0],
      [b and b['lnk'], mb and (mb['secs'], mb['li'])])
    t0 = p.ev("()=>__C2.mainTop()")
    p.click(p.ev("([s,r,i])=>__C2.lkmItem(s,r,i)", ['.li', '24-61-2', 0]), 300)
    fl = p.ev("c=>__C2.flash(c)", '24-61-2'); p.pg.wait_for_timeout(2600)   # 늦게 들어오는 임베드 뒤 다시 맞춤(2.5초)까지
    c = p.ev("c=>__C2.card(c)", '24-61-2'); top = p.ev("([c,s])=>__C2.lineTopInCard(c,s)", ['24-61-2', 'Ⅱ.'])
    t1 = p.ev("()=>__C2.mainTop()")
    T(g, '줄 누름 → 24-61-2 카드 창 · 그 설문 줄 위 12px · .lkflash · 보드 scrollTop 무변', c is not None and top is not None and abs(top - 12) <= 2 and fl and any('Ⅱ' in x for x in fl) and t0 == t1, [c and c['title'], top, fl, t0, t1])
    p.ev("()=>__C2.closeAll()")
    p.click(p.ev("([c,s,k,x])=>__C2.lnkBtn(c,s,k,x)", ['24-61-2', 'Ⅱ.', False, 'out']))
    xs = p.ev("()=>__C2.lkm()")
    i13 = next((i for i, t in enumerate(xs['li']) if '13-50-2' in t), -1) if xs else -1
    p.click(p.ev("i=>__C2.lkmX(i)", i13))
    p.ev("()=>__C2.closeAll()"); p.idle(200)
    b2 = p.ev("([c,s])=>__C2.lineInfo(c,s)", ['13-50-2', 'Ⅰ.'])
    T(g, '내 쪽 ✕ → 상대 ↩ 0', i13 >= 0 and b2 and not any(x['cls'] == 'c2lnk in' for x in b2['lnk']), [i13, b2 and b2['lnk']])
    p.click(p.ev("([c,s,k,x])=>__C2.lnkBtn(c,s,k,x)", ['24-61-2', 'Ⅰ.', False, None]))
    p.ev("v=>__C2.lkmType(v)", '중복소'); p.idle(300)
    ms = p.ev("()=>__C2.lkm()")
    T(g, '사례 카드 후보 0(「중복소」 후보 = 기출·GS 만)', ms and ms['ai'] and all(x.startswith('기출') or x.startswith('GS') for x in ms['ai']), ms and ms['ai'][:6])
    p.ev("()=>__C2.closeAll()")
    p.ev("()=>localStorage.setItem('jopangi.c2qlink','{}')")
    expand(p, '24-61-2', False); expand(p, '13-50-2', False)


def B12(p):
    g = 'B12'
    p.ev("()=>{localStorage.setItem('jopangi.c2unit','{}');return 1;}")
    p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'c2mx': {}, 'c2uv': {}})
    r = p.ev("c=>__C2.rowInfo(c)", '24-61-2')
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'ue']))
    r2 = p.ev("c=>__C2.rowInfo(c)", '24-61-2')
    T(g, '처음 칩 보임 0 · 「단원 3 ▸」 → 3', r and not r['uchips'] and r['ue'] == '단원 3 ▸' and len(r2['uchips']) == 3 and r2['ue'] == '단원 3 ▾', [r and r['ue'], r2['ue'], [x['t'] for x in r2['uchips']]])
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'uadd']))
    u0 = p.ev("()=>__C2.upick()")
    p.ev("v=>__C2.upickType(v)", '기판력'); p.idle(200)
    u1 = p.ev("()=>__C2.upick()")
    p.click(p.ev("v=>__C2.upickItem(v)", '기판력'))
    hv = p.ev("()=>__C2.unitLS()").get('민소|24-61-2'); r3 = p.ev("c=>__C2.rowInfo(c)", '24-61-2')
    added = [x for x in r3['uchips'] if x['added']]
    T(g, '「+」 → 「기판력」 → 후보 → 고름 → jopangi.c2unit 그 칸 손값((+) 칸) · 칩 4 · 점선 테', u0 and u0['focus'] and u1 and len(u1['ui']) >= 1 and hv and '(+)' in (hv.get('s') or {}) and len(r3['uchips']) == 4 and len(added) == 1 and added[0]['bs'] == 'dashed',
      [u1 and u1['ui'][:3], hv, [x['t'] for x in r3['uchips']]])
    nm = (hv or {}).get('s', {}).get('(+)', [''])[0]
    p.go({'c2ord': 'unit'}, True)
    ovt = p.ev("n=>{const h=[...document.querySelectorAll('#slot .c2uh')].find(x=>x.dataset.unit===n);return h?(h.querySelector('.ov')||{}).textContent||'':null;}", nm)
    rows = p.ev("n=>__C2.unitRows(n)", '1.3.1.{법정}직사토(보독관)') or []
    T(g, '단원별 보드 — 주단원 자리 그대로(1.3.1 아래 24-61-2) · 더한 단원 머리 걸침 셈에 24-61-2', '24-61-2' in ' '.join(rows) and bool(ovt) and '걸침' in ovt, [rows[:6], nm, ovt])
    p.click(p.ev("c=>__C2.addedX(c)", '24-61-2'))
    r4 = p.ev("c=>__C2.rowInfo(c)", '24-61-2'); hv2 = p.ev("()=>__C2.unitLS()").get('민소|24-61-2')
    T(g, '✕ → 3 · 손값 = 자동값과 같아져 {auto:true}', len(r4['uchips']) == 3 and hv2 and hv2.get('auto') is True, [len(r4['uchips']), hv2])
    p.long(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'ue']))
    pw = [x for x in p.ev("()=>__C2.popsInfo()") if x['t'].startswith('✎ ')]
    T(g, '「단원 N ▸」 길게 → ✎ 단원 창', len(pw) == 1, p.ev("()=>__C2.popsInfo()"))
    p.ev("()=>__C2.closeAll()")
    p.ev("()=>{localStorage.setItem('jopangi.c2unit','{}');return 1;}")


def B13(p, pnotok):
    g = 'B13'
    p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}})
    r = p.ev("c=>__C2.rowInfo(c)", '26-63-2')
    T(g, '줄 탭 줄(.c2tabs) 0 · 「해설」「Claude」 글자 단추 · 주황 clBtn 0', r and r['tabs'] == 0 and r['pb'] == ['해설', 'Claude'] and r['mbcl'] == 0, r and [r['pb'], r['mbcl'], r['tabs']])
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['26-63-2', 'hs']), 2500)
    h = None
    for _ in range(20):
        h = p.ev("()=>__C2.hsPop()")
        if h and h['text'] and h['text'] != '…':
            break
        p.pg.wait_for_timeout(300)
    T(g, '「해설」 → 창 1(📘 해설 · 민기출 26-63-2 · 원천 줄 · 폭 ≤ 440 · max-height 75vh)', h and h['t'] == '📘 해설 · 민기출 26-63-2' and h['hasHs'] and h['w'] <= 440 and h['mh'] in ('675px', '75vh'), h)
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['26-63-2', 'hs']))
    T(g, '「해설」 다시 → 0', p.ev("()=>__C2.hsPop()") is None, '')
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['26-63-2', 'cl']), 800)
    c = p.ev("()=>__C2.clPop()")
    T(g, '「Claude」 → Claude 창(답 없음 문구)', c and 'Claude 답이 아직 없다' in c['text'], c)
    p.ev("()=>__C2.closeAll()")
    g2 = p.go({'boardKind': 'GS'})
    gs = p.ev("()=>({cl:document.querySelectorAll('#slot .c2row .c2pbtn.cl').length,hs:document.querySelectorAll('#slot .c2row .c2pbtn').length,rows:document.querySelectorAll('#slot .c2row').length})")
    T(g, 'GS 줄 「Claude」 0(「해설」만)', gs['cl'] == 0 and gs['hs'] == gs['rows'] and gs['rows'] > 0, gs)
    p.go({'boardKind': '기출'})
    if pnotok:
        pnotok.go({'c2ord': 'unit'})
        pnotok.click(pnotok.ev("([c,x])=>__C2.rowPart(c,x)", ['26-63-2', 'hs']), 2500)
        h2 = None
        for _ in range(20):
            h2 = pnotok.ev("()=>__C2.hsPop()")
            if h2 and h2['text'] and h2['text'] != '…':
                break
            pnotok.pg.wait_for_timeout(300)
        T(g, '토큰 없음 — 「해설」 창 = 이유 문구 칸(🔑 토큰) + 채점표 해설 목차', h2 and '토큰' in (h2['why'] or '') and '채점표' in h2['text'], h2)


def B14(p):
    g = 'B14'
    p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'c2q': ''})
    s0 = p.ev("()=>__C2.srch()")
    p.click(p.ev("()=>__C2.at('#slot .c2srch')"))
    p.ev("v=>__C2.srType(v)", '중복소'); p.ev("()=>__C2.srWait()")
    a = p.ev("()=>__C2.srp()")
    T(g, '「중복소」 → 전체 58 · 기출 9 · GS 9 · 사례 40(시안 값 · 색인 = 콜아웃 ⑦·📄 둘 다)', a and a['k'] == ['전체 58', '기출 9', 'GS 9', '사례 40'] and s0 and s0['ph'] == '🔍 민소 기출·GS·사례', [s0 and s0['ph'], a and a['k']])
    p.click(p.ev("t=>__C2.srKind(t)", 'GS'))
    b = p.ev("()=>__C2.srp()")
    T(g, 'GS 거르기 → 9 줄 다 GS', b and b['n'] == 9 and all(x['kind'] == 'GS' for x in b['rows']), b and [b['on'], b['n']])
    p.click(p.ev("t=>__C2.srKind(t)", '전체'))
    p.ev("v=>__C2.srType(v)", '사물관할 반소'); p.ev("()=>__C2.srWait()")
    c = p.ev("()=>__C2.srp()")
    p.ev("v=>__C2.srType(v)", '쀍쀍없는말'); p.ev("()=>__C2.srWait()")
    d = p.ev("()=>__C2.srp()")
    T(g, '「사물관할 반소」 4 · 없는 말 0(「찾은 것 없음」)', c and c['n'] == 4 and d and d['n'] == 0 and '찾은 것 없음' in d['sr0'], [c and c['k'], d and d['sr0']])
    p.ev("v=>__C2.srType(v)", '중복소'); p.ev("()=>__C2.srWait()")
    t0 = p.ev("()=>__C2.mainTop()")
    sr = p.ev("()=>__C2.srp()") or {'rows': []}
    ib = next((i for i, x in enumerate([r for r in sr['rows'] if r['kind'] == '기출']) if any(not re.match(r'^(⑦|📄|⤷)', y) for y in x['s'])), 0)   # 본문 줄에 낱말이 든 첫 기출 결과
    rw = p.ev("([k,i])=>__C2.srRow(k,i)", ['기출', ib])
    p.click(rw, 1800)
    code = (re.search(r'(\d\d-\d\d-\d+)', rw['f']) or [None, ''])[1] if rw else ''
    cc = p.ev("c=>__C2.card(c)", code) if code else None
    t1 = p.ev("()=>__C2.mainTop()")
    T(g, '기출 결과 → 카드 창 + mark.srm ≥ 1 · 패널 닫힘 · 보드 scrollTop 무변', cc and cc['marks'] >= 1 and p.ev("()=>__C2.srp()") is None and t0 == t1, [rw and rw['f'], cc and cc['marks'], t0, t1])
    p.ev("()=>__C2.closeAll()")
    p.click(p.ev("()=>__C2.at('#slot .c2srch')")); p.ev("()=>__C2.srWait()")
    rs = p.ev("([k,i])=>__C2.srRow(k,i)", ['사례', 0])
    p.click(rs, 1200)
    sp = [x for x in p.ev("()=>__C2.popsInfo()") if x['t'].startswith('🧾 사례')]
    T(g, '사례 결과 → 카드 창(🧾 사례 · …)', rs is not None and len(sp) == 1, [rs and rs['f'], [x['t'] for x in sp]])
    p.ev("()=>__C2.closeAll()")
    p.click(p.ev("()=>__C2.at('#slot .c2srch')")); p.ev("()=>__C2.srWait()")
    first = (p.ev("()=>__C2.srp()") or {}).get('rows', [{}])[0].get('f', '')
    p.key('Enter'); p.idle(900)
    pe = p.ev("()=>__C2.popsInfo()")
    T(g, 'Enter = 첫 결과(카드 창)', any(first[:20] in x['t'] for x in pe) and p.ev("()=>__C2.srp()") is None, [first, [x['t'] for x in pe]])
    p.ev("()=>__C2.closeAll()")
    p.click(p.ev("()=>__C2.at('#slot .c2srch')")); p.ev("()=>__C2.srWait()")
    p.key('Escape')
    T(g, 'Esc = 패널 닫힘 · 입력 blur', p.ev("()=>__C2.srp()") is None and not p.ev("()=>__C2.srch()")['focus'], '')
    p.go({'law': '특허법', 'boardKind': '기출', 'c2q': ''})
    p.click(p.ev("()=>__C2.at('#slot .c2srch')"))
    p.ev("v=>__C2.srType(v)", '민기출'); p.ev("()=>__C2.srWait()")
    e = p.ev("()=>__C2.srp()")
    p.ev("v=>__C2.srType(v)", '관할'); p.ev("()=>__C2.srWait()")
    e2 = p.ev("()=>__C2.srp()")
    T(g, '다른 법(특허)에서 민소 카드 0(「민기출」 0 · 「관할」 결과에 민기출 0) · 자리표 「🔍 특허 기출·GS·사례」', e and e['n'] == 0 and e2 is not None and not any('민기출' in x['f'] for x in e2['rows']) and p.ev("()=>__C2.srch()")['ph'] == '🔍 특허 기출·GS·사례',
      [e and e['k'], e2 and e2['k']])
    p.key('Escape')
    p.go({'law': '민사소송법', 'boardKind': '기출', 'c2q': ''})


def B15(p, ptouch):
    g = 'B15'
    p.ev("o=>__C2.setPit(o)", PIT0)
    p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'c2mx': {}, 'c2memo': {}})
    expand(p, '24-61-2', True); p.idle(400)
    m = p.ev("()=>__C2.memo()")
    gp = p.ev("([i,x])=>__C2.memoPart(i,x)", [0, 'grip'])
    p.drag(gp['cx'], gp['cy'], gp['cx'] - 40, gp['cy'] - 30) if gp else None
    m1 = p.ev("()=>__C2.memo()")
    T(g, '메모 창 손잡이 −40·−30 → 폭 줄음(최소 160×70)', gp and m1 and m1[0]['w'] < m[0]['w'] - 30 and m1[0]['rect']['h'] >= 69.5, [m and (m[0]['w'], m[0]['rect']['h']), m1 and (m1[0]['w'], m1[0]['rect']['h'])])
    expand(p, '24-61-2', False); expand(p, '24-61-2', True); p.idle(400)
    m2 = p.ev("()=>__C2.memo()")
    T(g, '메모 창 크기 기억(본문 접고 펴도)', m2 and m1 and abs(m2[0]['w'] - m1[0]['w']) < 1.5, [m1 and m1[0]['w'], m2 and m2[0]['w']])
    hp = p.ev("([i,x])=>__C2.memoPart(i,x)", [0, 'head'])
    r0 = m2[0]['rect'] if m2 else None
    p.drag(hp['cx'], hp['cy'], hp['cx'] - 80, hp['cy'] + 60) if hp else None
    m3 = p.ev("()=>__C2.memo()")
    T(g, '메모 창 머리 끌기(PC 마우스) → 옮김', r0 and m3 and abs(m3[0]['rect']['x'] - r0['x'] + 80) < 3 and abs(m3[0]['rect']['y'] - r0['y'] - 60) < 3, [r0, m3 and m3[0]['rect']])
    for nm, open_ in (('카드', "['24-61-2','code']"), ('문제', "['24-61-2','q1']"), ('해설', "['26-63-2','hs']")):
        p.ev("()=>__C2.closeAll()")
        p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", json.loads(open_.replace("'", '"'))), 1500)
        i = len(p.ev("()=>__C2.popsInfo()")) - 1
        a = p.ev("i=>__C2.popRect(i)", i); gg = p.ev("i=>__C2.popGrip(i)", i)
        if gg:
            p.drag(gg['cx'], gg['cy'], gg['cx'] - 40, gg['cy'] - 30)
        b = p.ev("i=>__C2.popRect(i)", i)
        T(g, '%s 창 손잡이 −40·−30 → 크기 줄음' % nm, a and b and gg and (b['w'] < a['w'] - 30 or b['h'] < a['h'] - 20), [a and (a['w'], a['h']), b and (b['w'], b['h'])])
    p.ev("()=>__C2.closeAll()")
    p.ev("()=>{S.c2memo={};uiSave();return 1;}")
    if ptouch:
        ptouch.ev("o=>__C2.setPit(o)", PIT0)
        ptouch.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'c2mx': {}, 'c2memo': {}})
        expand(ptouch, '24-61-2', True); ptouch.idle(400)
        t0 = ptouch.ev("()=>__C2.memo()")
        hh = ptouch.ev("([i,x])=>__C2.memoPart(i,x)", [0, 'head'])
        how = ptouch.drag(hh['cx'], hh['cy'], hh['cx'] - 40, hh['cy'] + 50) if hh else None
        t1 = ptouch.ev("()=>__C2.memo()")
        T(g, '%s 손가락 끌기 → 메모 창 옮김' % ptouch.dev, t0 and t1 and abs(t1[0]['rect']['y'] - t0[0]['rect']['y'] - 50) < 4, [how, t0 and t0[0]['rect'], t1 and t1[0]['rect']])


def B16(p, pb):
    g = 'B16'
    p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}})
    s1 = p.ev("()=>__C2.sbar()")
    p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'code']), 900)
    c1 = p.ev("c=>__C2.card(c)", '24-61-2')
    b1 = None
    if pb:
        pb.go({'c2ord': 'unit'})
        b1 = pb.ev("()=>__C2.sbar()")
        pb.click(pb.ev("([c,x])=>__C2.rowPart(c,x)", ['24-61-2', 'code']), 900)
        bc = pb.ev("c=>__C2.card(c)", '24-61-2')
        b1 = dict(b1, card=bc and bc['ow'])
    T(g, '2차 탭 .main · 카드 창 .pop 스크롤바 폭 0(바탕 > 0 · PC Chromium)', s1['main'] == 0 and c1 and c1['ow'] == 0 and (b1 is None or (b1['main'] > 0 and (b1['card'] or 0) > 0)), [s1, c1 and c1['ow'], b1])
    p.ev("()=>__C2.closeAll()")
    t0 = p.ev("()=>__C2.mainTop()")
    mr = p.ev("()=>{const r=document.querySelector('#slot .main').getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2};}")
    p.pg.mouse.move(mr['x'], mr['y']); p.pg.mouse.wheel(0, 600); p.idle(500)
    t1 = p.ev("()=>__C2.mainTop()")
    T(g, '휠 굴림 됨', t1 > t0, [t0, t1])
    j = p.ev("()=>__C2.jimun()")
    jb = pb.ev("()=>__C2.jimun()") if pb else None
    if QJ.REGRESS:   # 기준: 1차객 탭 .main 스크롤바(j['sb'])가 앞 인도판 같은 값(스냅샷) — 바탕 판은 안 띄운다
        _jsb = QJ.same('B16-1차객sb@' + p.eng, j['sb'])
    T(g, '1차객 탭 .main = 바탕과 같음(c2on 없음)', not j['c2on'] and ((jb is None or j['sb'] == jb['sb']) if QJ.GATE else _jsb), [j, jb])
    p.go({'c2ord': 'unit'})
    expand(p, '24-61-2', True)
    p.click(p.ev("([c,s,k,x])=>__C2.lnkBtn(c,s,k,x)", ['24-61-2', 'Ⅰ.', False, None]))
    lk = p.ev("()=>__C2.lkm()")
    p.ev("()=>{toast('토스트 대조(합성)');return 1;}")
    p.pg.wait_for_timeout(150)
    lt, lm = p.ev("s=>__C2.layer(s)", '#toasts'), p.ev("s=>__C2.layer(s)", '.c2lkm')
    T(g, '토스트가 연결 메뉴 위(둘 다 body 바로 아래 fixed · #toasts z 9700 > 메뉴 9600 · 옛 90)', lk and lt and lm and lt['root'] and lm['root'] and lt['pos'] == 'fixed' and lm['pos'] == 'fixed' and lt['z'] == 9700 and lm['z'] == 9600, [lt, lm])
    p.ev("()=>__C2.closeAll()")
    expand(p, '24-61-2', False)


def B17(pg_list):
    g = 'B17'
    for p in pg_list:
        p.ev("o=>__C2.setPit(o)", PIT0)
        p.go({'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'c2mx': {}, 'c2memo': {}})
        expand(p, '24-61-2', True); p.idle(500)
        ov = p.ev("()=>__C2.overflow()"); m = p.ev("()=>__C2.memo()"); sr = p.ev("()=>__C2.srch()")
        W = DEV[p.dev]['W']
        seg = p.ev("()=>{const s=document.getElementById('ordSeg');return s?s.getBoundingClientRect().bottom:0;}")
        own = (sr['wrap']['y'] >= seg - 1) if p.dev == 'phone' else True
        inside = all(x['rect']['x'] >= -0.5 and x['rect']['r'] <= W + 0.5 for x in m)
        T(g, '%s %d — 가로 넘침 0 · 칩·단추 화면 밖 0 · 메모 창 화면 안%s' % (p.eng, W, ' · 폰 검색 칸 제 줄' if p.dev == 'phone' else ''),
          ov['docW'][0] <= ov['docW'][1] and ov['main'][0] <= ov['main'][1] and ov['n'] == 0 and inside and own and len(m) == 2, [ov, [(x['rect']['x'], x['rect']['r']) for x in m], sr and sr['wrap'], seg])
        N(g, '%s %d 누름 크기(36 미만은 값만)' % (p.eng, W), p.ev("()=>__C2.tapSizes()"))
        p.shot('B17')
        expand(p, '24-61-2', False)


def BS(br, eng, src_new, src_base):
    g = 'B-S'
    REMOTE.clear()
    a = P(br, eng, 'NEW', src_new, 'pc', 'seed=1')
    a.ev("()=>__C2.syncNow()"); a.idle(500)
    a.ev("o=>__C2.setMiss(o)", {TK2461 + '|합의관할 유효성 검토': {'h': [{'ts': '2026-10-03T02:00:00.000Z', 'who': '햄찌', 'r': 'x'}]}})
    a.ev("o=>__C2.setLS('jopangi.c2qlink',o)", {TK2461 + '#1' + '\u001e' + TK1350 + '#0': {'ts': '2026-10-03T02:00:00.000Z', 'who': '햄찌', 'qa': '설문(2)', 'qb': '설문(1)'}})
    pit = a.ev("()=>__C2.pit()"); pit[PK_B] = dict(pit[PK_B], re=[{'t': '댓글 동기화(합성)', 'who': '햄찌', 'ts': '2026-10-03T02:00:00.000Z'}])
    a.ev("o=>__C2.setPit(o)", pit)
    r1 = a.ev("()=>__C2.syncNow()"); a.idle(400)
    rm = REMOTE.json() or {}
    T(g, 'PC(새 판) 올림 → 원격 data 에 c2miss · c2qlink · postit re', r1 == 'ok' and 'jopangi.c2miss' in rm.get('data', {}) and len(rm['data'].get('jopangi.c2qlink') or {}) == 1 and (rm['data'].get('jopangi.postit', {}).get(PK_B, {}).get('re') or [{}])[0].get('t') == '댓글 동기화(합성)',
      [r1, sorted(k for k in rm.get('data', {}) if 'c2' in k)])
    b = P(br, eng, 'NEW', src_new, 'pad', 'seed=1&rec=0&who=꼬까')
    b.ev("()=>__C2.syncNow()"); b.idle(500)
    T(g, '아이패드(새 판 · 빈 기기) 받음 → c2miss · c2qlink · postit re 같은 값', b.ev("()=>__C2.missLS()") == a.ev("()=>__C2.missLS()") and b.ev("()=>__C2.qlLS()") == a.ev("()=>__C2.qlLS()") and (b.ev("()=>__C2.pit()").get(PK_B) or {}).get('re') == pit[PK_B]['re'],
      [b.ev("()=>__C2.missLS()"), len(b.ev("()=>__C2.qlLS()"))])
    b.ev("o=>__C2.setMiss(o)", {})   # 다 지우기 = 칸 지움
    b.ev("()=>__C2.syncNow()"); b.idle(300)
    a.ev("()=>__C2.syncNow()"); a.idle(300)
    T(g, '아이패드에서 다 지움(묘비) → PC 받은 뒤 그 칸 없음(칸 단위 · 묘비 이김)', a.ev("()=>__C2.missLS()") == {} and any(k.startswith('jopangi.c2miss|') for k in (REMOTE.json() or {}).get('gone', {})), a.ev("()=>__C2.missLS()"))
    b.ev("()=>__C2.syncNow()"); b.close()   # 아이패드 몫 끝 — 열어 두면 제 때(4초 뒤 · 3분) 맞추기가 옛 판 순서 사이에 끼어 되살림을 앞당긴다
    if QJ.GATE:   # 옛 판(바탕 281c93f) 기기 몫 — regress 는 바탕을 안 띄운다(처리안 「관문만」)
        a.ev("o=>__C2.setMiss(o)", {TK2461 + '|요건,방식-1임특특서': {'h': [{'ts': '2026-10-03T03:00:00.000Z', 'who': '햄찌', 'r': 'x'}]}})
        a.ev("()=>__C2.syncNow()"); a.idle(300)
        c = P(br, eng, 'BASE', src_base, 'pc900', 'seed=1&rec=0')
        c.ev("()=>__C2.syncNow()"); c.idle(500)
        cp = c.ev("()=>__C2.pit()"); cp[PK_C] = dict(cp.get(PK_C) or PIT0[PK_C])
        cp[PK_C]['t'] = '옛 판 기기에서 고침(합성)'; c.ev("o=>__C2.setPit(o)", cp)
        c.ev("()=>__C2.syncNow()"); c.idle(300)
        rm2 = REMOTE.json() or {}
        lost = 'jopangi.c2miss' not in rm2.get('data', {}) and 'jopangi.c2qlink' not in rm2.get('data', {})
        stamps = [k for k in rm2.get('u', {}) if k.startswith('jopangi.c2miss|') or k.startswith('jopangi.c2qlink|')]
        N(g, '옛 판(바탕) 기기가 올린 원격 — 새 키 data 빠짐 · 도장은 남음(theme 키 선례)', {'data_빠짐': lost, '도장': len(stamps)})
        a.ev("()=>__C2.syncNow()"); a.idle(400)
        rm3 = REMOTE.json() or {}
        T(g, '새 판 기기가 다음 맞추기에서 되살림(원격 data 에 c2miss · c2qlink 다시) · 옛 판의 postit 고침은 받음',
          lost and len(stamps) >= 2 and len(rm3.get('data', {}).get('jopangi.c2miss') or {}) == 1 and len(rm3.get('data', {}).get('jopangi.c2qlink') or {}) == 1 and a.ev("()=>__C2.pit()").get(PK_C, {}).get('t') == '옛 판 기기에서 고침(합성)',
          [lost, len(stamps), sorted((rm3.get('data', {}).get('jopangi.c2miss') or {}).keys()), a.ev("()=>__C2.pit()").get(PK_C, {}).get('t')])
        # 옛 판 기기가 댓글 단 메모를 pitEdit 으로 고치면 re 가 사라지는가(정한 것 7 — 값만 적음)
        c.ev("()=>__C2.syncNow()"); c.idle(300)
        c.ev("([k,v])=>__C2.pitEditSave(k,v)", [PK_B, '옛 판 pitEdit 고침(합성)']); c.idle(500)
        c.ev("()=>__C2.syncNow()"); c.idle(300)
        a.ev("()=>__C2.syncNow()"); a.idle(300)
        va = a.ev("()=>__C2.pit()").get(PK_B) or {}
        N(g, '옛 판 기기에서 댓글 단 메모를 고침 → 새 판이 받은 값(⚠ 정한 것 7 — 모든 기기가 새 판을 받으면 사라지는 한계)', {'t': va.get('t'), 're': va.get('re'), 're_사라짐': not va.get('re')})
    for x in ((a, c) if QJ.GATE else (a,)):
        x.close()
    REMOTE.clear()


def sweep(pg_list):
    """화면 훑기 — 단원별·회차별 · 본문 · 메모 창 · 누락 메뉴 · 연결 메뉴 · 단원 고르개 · 검색 패널 · 해설 창(네 폭 · 넘침·잘림·겹침)"""
    g = '훑기'
    for p in pg_list:
        p.ev("o=>__C2.setPit(o)", PIT0)
        W = DEV[p.dev]['W']
        bad = []
        p.go({'c2ord': 'round', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'c2mx': {}, 'c2memo': {}})
        p.shot('round')
        ov = p.ev("()=>__C2.overflow()"); bad += ov['off']
        p.go({'c2ord': 'unit'})
        p.shot('unit')
        ov = p.ev("()=>__C2.overflow()"); bad += ov['off']
        expand(p, '24-61-2', True); p.idle(500)
        p.shot('body_memo')
        ov = p.ev("()=>__C2.overflow()"); bad += ov['off']
        mm = p.ev("()=>__C2.memo()")
        ovl = [(i, j) for i in range(len(mm)) for j in range(i + 1, len(mm)) if mm[i]['mode'] == mm[j]['mode'] == 'b' and not (mm[i]['rect']['r'] <= mm[j]['rect']['x'] or mm[j]['rect']['r'] <= mm[i]['rect']['x'] or mm[i]['rect']['b'] <= mm[j]['rect']['y'] or mm[j]['rect']['b'] <= mm[i]['rect']['y'])]
        if ovl:
            bad.append('메모 창 겹침 %s' % ovl)
        for nm, js_open, sel in (('miss', "()=>__C2.missBtn('24-61-2','2. 합의관할')", '.c2missm'), ('lkm', "()=>__C2.lnkBtn('24-61-2','Ⅰ.',false,null)", '.c2lkm'),
                                 ('upick', "()=>__C2.rowPart('24-61-2','uadd')", '.c2upick')):
            if nm == 'miss':
                p.ev("o=>__C2.setMiss(o)", {})
            at = p.ev(js_open)
            if nm == 'miss' and at:
                # 첫 누름 = 기록(메뉴 없음) · 둘째 = 메뉴
                p.ev("()=>{document.querySelectorAll('.pop.mpop').forEach(x=>x.remove());return 1;}")
                at = p.ev(js_open); p.click(at); at = p.ev(js_open)
            p.click(at)
            r = p.ev("s=>{const m=document.querySelector(s);if(!m)return null;const r=m.getBoundingClientRect();return {x:r.left,y:r.top,r:r.right,b:r.bottom,sh:m.scrollHeight,ch:m.clientHeight};}", sel)
            p.shot(nm)
            if not r or r['x'] < -0.5 or r['r'] > W + 0.5 or r['y'] < -0.5 or r['b'] > DEV[p.dev]['H'] + 0.5:
                bad.append('%s 화면 밖 %s' % (nm, r))
            p.ev("()=>__C2.closeAll()"); p.idle(200)
        p.ev("o=>__C2.setMiss(o)", {})
        p.click(p.ev("()=>__C2.at('#slot .c2srch')"))
        p.ev("v=>__C2.srType(v)", '중복소'); p.ev("()=>__C2.srWait()")
        r = p.ev("()=>__C2.srp()")
        p.shot('search')
        if not r or r['rect']['x'] < -0.5 or r['rect']['r'] > W + 0.5:
            bad.append('검색 패널 %s' % (r and r['rect']))
        p.key('Escape')
        p.click(p.ev("([c,x])=>__C2.rowPart(c,x)", ['26-63-2', 'hs']), 2500)
        h = p.ev("()=>__C2.hsPop()")
        p.shot('hs')
        if not h or h['rect']['x'] < -0.5 or h['rect']['r'] > W + 0.5:
            bad.append('해설 창 %s' % (h and h['rect']))
        p.ev("()=>__C2.closeAll()")
        expand(p, '24-61-2', False)
        T(g, '%s %d — 넘침·잘림·겹침 0(단원별·회차별 · 본문 · 메모 창 · 누락 메뉴 · 연결 메뉴 · 단원 고르개 · 검색 패널 · 해설 창)' % (p.eng, W), not bad, bad[:8])


# ════════════════════════ 차례 ════════════════════════
def want(k):
    return not ONLY or k in ONLY


def run_suite(br, eng, tag, src, src_base=None, yard=False):
    """한 판 — yard 면 바탕(헛잣대 묶음만)"""
    phase = {}
    t = time.time()
    p = P(br, eng, tag, src, 'pc')
    pb = None
    try:
        if not yard and want('B0'):
            B0(p)
        groups = [('B1', lambda: B1(p)), ('B3', lambda: B3(p)), ('B4', lambda: B4(p)), ('B5', lambda: B5(p)), ('B6', lambda: B6(p, None if yard else ph())),
                  ('B7', lambda: B7(p)), ('B8', lambda: B8(p)), ('B9', lambda: B9(p)), ('B10', lambda: B10(p)), ('B11', lambda: B11(p)), ('B12', lambda: B12(p)),
                  ('B13', lambda: B13(p, None if yard else notok())), ('B14', lambda: B14(p)), ('B15', lambda: B15(p, None if yard else ph())), ('B16', lambda: B16(p, None if yard else base_pc()))]
        cache = {}

        def ph():
            if 'ph' not in cache:
                cache['ph'] = P(br, eng, tag, src, 'phone')
            return cache['ph']

        def notok():
            if 'nt' not in cache:
                cache['nt'] = P(br, eng, tag, src, 'pc', 'seed=1&tok=0')
            return cache['nt']

        def base_pc():
            if 'bp' not in cache and src_base:
                cache['bp'] = P(br, eng, 'BASE', src_base, 'pc')
            return cache.get('bp')
        for k, fn in groups:
            if yard and k in ('B8', 'B15'):
                continue
            if not want(k):
                continue
            t1 = time.time()
            n0 = len(RES)
            try:
                fn()
            except Exception as e:
                T(k, '실행 오류', False, '%s: %s' % (type(e).__name__, str(e)[:300]))
                if not yard:
                    traceback.print_exc()
            phase[k] = round(time.time() - t1, 1)
            if yard:
                fails = [r for r in RES[n0:] if r[2] is False]
                print('YARD | %s — 바탕 FAIL %d / %d' % (k, len(fails), len([r for r in RES[n0:] if r[2] is not None])), flush=True)
        if not yard and want('B2'):
            t1 = time.time()
            p9 = P(br, eng, tag, src, 'pc900')
            b9 = P(br, eng, 'BASE', src_base, 'pc900') if src_base else None
            try:
                B2(p9, b9)
            finally:
                p9.close()
                if b9:
                    b9.close()
            phase['B2'] = round(time.time() - t1, 1)
        if not yard and (want('B17') or want('SWEEP')):
            t1 = time.time()
            L = [p, P(br, eng, tag, src, 'pc900'), P(br, eng, tag, src, 'pad'), cache.get('ph') or P(br, eng, tag, src, 'phone')]
            if want('B17'):
                B17(L)
            if want('SWEEP'):
                sweep(L)
            for x in L[1:]:
                x.close()
            cache.pop('ph', None)
            phase['B17·훑기'] = round(time.time() - t1, 1)
        errs = [e for e in p.errs if 'Failed to load resource' not in e]
        if not yard:
            T('B0', '페이지 오류 0(pageerror)', not errs, errs[:5])
        for v in cache.values():
            if v:
                v.close()
    finally:
        p.close()
    return phase


def main():
    if QJ.GATE:
        QJ.sub('git:show-app')
        src_new, src_base = app_src(NEW), app_src(BASE)
    else:
        src_new, src_base = app_src(NEW), None   # regress · smoke: 바탕 앱을 안 푼다(git show 0) — B2 · B16 · B-S 의 바탕 쪽은 pb=None 길 · 기준(스냅샷)
    print('NEW  = %s · md5(LF) %s · %d B(LF)' % (NEW, md5lf(src_new), len(src_new.replace('\r\n', '\n').encode('utf-8'))))
    if QJ.GATE:
        print('BASE = %s · md5(LF) %s' % (BASE, md5lf(src_base)))
    os.makedirs(TMPD, exist_ok=True)
    phases = {}
    with sync_playwright() as pw:
        for eng in ENGS:
            try:
                br = getattr(pw, eng).launch(ignore_default_args=['--hide-scrollbars']) if eng == 'chromium' else getattr(pw, eng).launch()
            except Exception as e:
                N('엔진', '%s 안 잼(이 기계에 없음)' % eng, str(e).splitlines()[0][:160])
                continue
            try:
                if eng == 'chromium':
                    phases['new'] = run_suite(br, eng, 'NEW', src_new, src_base)
                    if want('BS'):
                        t1 = time.time(); BS(br, eng, src_new, src_base); phases['B-S'] = round(time.time() - t1, 1)
                    if YARD:
                        n0 = len(RES)
                        t1 = time.time()
                        run_suite(br, eng, 'BASE', src_base, None, yard=True)
                        phases['헛잣대'] = round(time.time() - t1, 1)
                        yr = RES[n0:]
                        del RES[n0:]
                        by = {}
                        for gname, nm, ok, d in yr:
                            if ok is None:
                                continue
                            by.setdefault(gname, []).append(ok)
                        for gname, oks in by.items():
                            RES.append(('헛잣대', gname, not all(oks), '바탕 FAIL %d / %d' % (oks.count(False), len(oks))))
                            print('%s | 헛잣대 · %s | 바탕 FAIL %d / %d' % ('PASS' if not all(oks) else 'FAIL', gname, oks.count(False), len(oks)), flush=True)
                else:
                    N('엔진', '%s — 터치 칸만(B6·B7·B11·B12·B15·B17)' % eng, '')
                    p = P(br, eng, 'NEW', src_new, 'phone')
                    try:
                        for k, fn in (('B6', lambda: B6(p, None)), ('B7', lambda: B7(p)), ('B11', lambda: B11(p)), ('B12', lambda: B12(p)), ('B15', lambda: B15(p, None)), ('B17', lambda: B17([p]))):
                            if want(k):
                                try:
                                    fn()
                                except Exception as e:
                                    T(k, '%s 실행 오류' % eng, False, str(e)[:300])
                    finally:
                        p.close()
            finally:
                br.close()
    ok = [r for r in RES if r[2] is True]
    bad = [r for r in RES if r[2] is False]
    tot = round(time.time() - T0, 1)
    lines = ['_harness_jo_2cha_minso_board — PASS %d · FAIL %d · %s초' % (len(ok), len(bad), tot), 'NEW md5(LF) ' + md5lf(src_new) + ' · BASE ' + BASE, '단계별 초 ' + json.dumps(phases, ensure_ascii=False)]
    for g_, nm, o, d in RES:
        lines.append('%s | %s · %s | %s' % ('INFO' if o is None else ('PASS' if o else 'FAIL'), g_, nm, d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str)[:600]))
    os.makedirs(os.path.dirname(OUTF), exist_ok=True)
    io.open(OUTF, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines[:3]))
    print('결과 → ' + OUTF)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
