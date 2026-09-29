# -*- coding: utf-8 -*-
r"""_task_jo_ms_cvfind §F 관문 — A 목차노트 영역 토글 · B 전체 검색 「📖 정리」 민소 · C 정리 탭 검색 목록 누름 · D 정리 결과 팝업

  NEW  = --new <파일>(없으면 genie 작업트리 jo/index.html) · BASE = --base <파일>(없으면 genie 905169d — 이 판 바로 앞 · md5(LF) 9bc75cae)
  헛잣대 = BASE 에 같은 시나리오를 먼저 돌린다 — 고치는 칸마다 BASE 에서 FAIL 이어야 잣대다(지시서 관문 규칙 3)
  누름 = page.mouse.click(x, y)(PC) · page.touchscreen.tap(x, y)(손가락) · 손가락 끌기 = CDP Input.dispatchTouchEvent
         el.click() · dispatchEvent('click') 은 쓰지 않는다(관문 규칙 1 — 포인터 이벤트를 건너뛰어 C 의 버그를 못 잡는다)
  숨김·보임 = 화면 기준 — display ≠ none 그리고 getBoundingClientRect().height > 0(관문 규칙 2)
  데이터 = genie jo/data(BASE·NEW 같은 데이터 · canvas_meta hash 를 적는다) · 비공개 minbeoppdf 없어도 됨(교재 창은 안 연다)
  엔진 = chromium 책상 1440×900(마우스) · 같은 크기 터치 켠 문맥(touchscreen.tap · CDP 한 손가락 끌기) — 아이패드 실기기는 못 잰다(사용자 확인)

쓰기 : python _harness_jo_cvfind.py [--new 파일] [--base 파일] [--out 폴더] [--only base,desk,touch]
"""
import hashlib, http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
CJH = r'N:\개인\claude\jopangi\공통\_harness'
sys.path.insert(0, CJH)
import _harness_canvas_jari as CJ          # noqa: E402 — SEED(기록·교재 fetch 돌림 · 바깥 網 막음) · VENDOR · route_filter · NOISE
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


HERE = os.path.dirname(os.path.abspath(__file__))
OUT = ARG('--out', HERE)
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
GENIE = CJ.GENIE
JOD = os.path.join(GENIE, 'jo')
DATA = os.path.join(JOD, 'data')
NEWF = ARG('--new', os.path.join(JOD, 'index.html'))
BASEF = ARG('--base', '')
BASE_REV, BASE_MD5 = '905169d', '9bc75caeeb5b145fcf5e895c2dc7e9fc'
WORK = os.path.join(tempfile.gettempdir(), 'h_cvfind')
TESTS = io.open(os.path.join(HERE, '_harness_jo_cvfind_tests.js'), encoding='utf-8').read()
READY = "!!window.__HC&&typeof render==='function'&&typeof viewCanvas==='function'"
PRE5 = ['1.3.1.', '1.3.2.', '1.4.', '2.1.1.', '2.2.1.']   # 손값 넣을 노트(채팅 시안과 같은 다섯)
Q_MS, Q_PT, Q_JO = '임의관할', '생산방법추정', '관할'
SHOTS = os.path.join(OUT, '_cvfind_shots')
SERVERS = {}
RES = []
KEEP = {}   # BASE ↔ NEW 맞대기(이름 줄 x · 다른 법 목록 DOM · 특허 정리 수 · 다른 범위 누름)


def git(*a, repo=GENIE):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, d[:300]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('NOTE | %s · %s | %s' % (grp, name, d[:300]), flush=True)


def near(a, b, tol):
    return a is not None and b is not None and abs(a - b) <= tol


def inside(a, v, tol=1):
    return bool(a) and bool(v) and a['x'] >= v['x'] - tol and a['r'] <= v['r'] + tol and a['y'] >= v['y'] - tol and a['b'] <= v['b'] + tol


def serve(tag, src):
    if tag in SERVERS:
        return SERVERS[tag][1]
    out = os.path.join(WORK, 'srv_' + tag); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    src = src.replace('\r\n', '\n')
    b = src.index('<body'); bb = src.index('>', b) + 1
    html = src[:bb] + CJ.SEED + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + TESTS + '\n</script>\n' + html[e:]
    io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=out, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            if p.startswith('/__vendor/'):
                return os.path.join(CJ.VENDOR, p[len('/__vendor/'):].replace('/', os.sep))
            if p.startswith('/data/'):
                return os.path.join(DATA, p[6:].replace('/', os.sep))
            if p in ('/index.html', '/'):
                return super().translate_path(path)
            f = os.path.join(JOD, p.lstrip('/').replace('/', os.sep))
            return f if os.path.exists(f) else super().translate_path(path)

        def log_message(self, *a, **k):
            pass
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


class Pg:
    def __init__(self, br, tag, src, W, H, touch=False, q='tok=1', who='꼬까'):
        self.tag, self.touch = tag, touch
        self.port = serve(tag, src)
        self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, has_touch=touch)
        self.ctx.route('**/*', CJ.route_filter)
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(180000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' else None)
        self.cdp = self.ctx.new_cdp_session(self.pg) if touch else None
        self.pg.goto('http://127.0.0.1:%d/index.html?%s&who=%s' % (self.port, q, urllib.parse.quote(who)), wait_until='load', timeout=180000)
        self.pg.wait_for_function(READY, timeout=180000)
        self.pg.wait_for_timeout(1000)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def until(self, expr, arg=None, ms=30000):
        t0 = time.time()
        while time.time() - t0 < ms / 1000:
            v = self.ev(expr, arg)
            if v:
                return v
            self.pg.wait_for_timeout(80)
        return self.ev(expr, arg)

    def click(self, at, wait=500):
        """진짜 포인터 — 책상 = mouse.click · 터치 문맥 = touchscreen.tap · 자리가 가려 있으면(elementFromPoint ≠ 대상) 안 누르고 False"""
        if not at or not at.get('on'):
            return False
        if self.touch:
            self.pg.touchscreen.tap(at['cx'], at['cy'])
        else:
            self.pg.mouse.click(at['cx'], at['cy'])
        self.pg.wait_for_timeout(wait)
        return True

    def fdrag(self, x0, y0, x1, y1, n=12):
        """CDP 진짜 터치 한 손가락 끌기"""
        def send(ty, pts):
            self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': [{'x': x, 'y': y, 'id': 1} for (x, y) in pts]})
        send('touchStart', [(x0, y0)])
        for i in range(1, n + 1):
            send('touchMove', [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n)]); self.pg.wait_for_timeout(16)
        for _ in range(3):   # 끝에서 멈춘 뒤 뗀다(움직이며 떼면 크롬이 다음 톡을 삼킨다)
            send('touchMove', [(x1, y1)]); self.pg.wait_for_timeout(30)
        send('touchEnd', [])
        self.pg.wait_for_timeout(300)

    def pinch(self, cx, cy, d0, d1, n=10):
        """CDP 진짜 터치 두 손가락 — 가로로 d0 → d1 벌리기(좁히기)"""
        def send(ty, d):
            self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': [] if d is None else [{'x': cx - d / 2, 'y': cy, 'id': 1}, {'x': cx + d / 2, 'y': cy, 'id': 2}]})
        send('touchStart', d0)
        for i in range(1, n + 1):
            send('touchMove', d0 + (d1 - d0) * i / n); self.pg.wait_for_timeout(16)
        for _ in range(3):
            send('touchMove', d1); self.pg.wait_for_timeout(30)
        send('touchEnd', None)
        self.pg.wait_for_timeout(300)

    def drag(self, x0, y0, x1, y1, n=14):
        m = self.pg.mouse
        m.move(x0, y0); m.down()
        for i in range(1, n + 1):
            m.move(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.pg.wait_for_timeout(16)
        m.up(); self.pg.wait_for_timeout(300)

    def blur(self):
        self.ev("()=>{try{document.activeElement&&document.activeElement.blur()}catch(e){}return 1}")

    def sk_open(self, scopes, laws, q):
        """Ctrl K(진짜 키) → 범위·법 칩(차림 — 누름 관문 아님) → 검색어 입력(진짜 키 입력) → skRun 이 끝날 때까지"""
        self.blur(); self.pg.keyboard.press('Control+k'); self.pg.wait_for_timeout(250)
        self.ev("([s,l])=>__HC.skSet(s,l)", [scopes, laws])
        self.pg.fill('#skin', ''); self.pg.type('#skin', q, delay=20)
        self.pg.wait_for_timeout(700)
        return self.until("()=>__HC.skDone()", None, 120000)

    def shot(self, name):
        os.makedirs(SHOTS, exist_ok=True)
        f = os.path.join(SHOTS, name + '.png')
        try:
            tmp = os.path.join(WORK, name + '.png')
            self.pg.screenshot(path=tmp)
            b = open(tmp, 'rb').read()
            for _ in range(3):
                open(f, 'wb').write(b); time.sleep(0.5)
                if open(f, 'rb').read() == b:
                    break
            return f
        except Exception as e:
            return 'shot 실패 ' + repr(e)[:120]

    def errs_all(self):
        return [y for y in (self.errs + (self.ev("()=>__HC.errs()") or [])) if not CJ.NOISE(y)]

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


def row(L, note):
    return next((r for r in (L or {}).get('rows', []) if r['note'] == note), {})


def grp_of(G, prefix):
    return next((x for x in (G or []) if x['h'].startswith(prefix)), None)


# ══════════ 책상(마우스) ══════════
def scen_desk(br, src, tag, G):
    g = '%s 책상' % tag
    p = Pg(br, tag, src, 1440, 900)
    NOTES = G['notes5']; N131, N14 = NOTES[0], NOTES[2]
    k131 = 'note|' + N131

    def sec(name, fn):   # 묶음마다 따로 — 앞 묶음이 깨져도(바탕 판 · 헛잣대) 뒤 묶음을 잰다
        try:
            fn()
        except Exception as ex:
            T(g, name + ' 묶음 예외', False, repr(ex)[:400])

    # ── A ──
    def secA():
        p.ev("()=>__HC.boot('jo')"); p.ev("async()=>await __HC.ensure()")
        seeded = p.ev("n=>__HC.seedPins(n)", NOTES)
        KEEP.setdefault('seed', seeded)
        L = p.ev("async()=>{await __HC.mokOpen();return await __HC.listPainted(90000)}")
        rows = (L or {}).get('rows', [])
        vis = sorted(r['note'] for r in rows if r['tgVis'])
        tg = [r for r in rows if r['tg']]
        T(g, 'A1·A2 화면 기준 보이는 토글 = 손값 넣은 5 · 손값 없는 끝 목차 줄 0 · 토글은 끝 목차 줄에만(헛잣대: 바탕 0)',
          vis == sorted(NOTES) and len(tg) == len(G['leaf']) and all(r['note'] in G['leaf'] for r in tg),
          {'보임': len(vis), '토글': len(tg), '끝 목차': len(G['leaf']), '손값 없는데 보임': [r['note'] for r in rows if r['tgVis'] and r['note'] not in NOTES][:3], '넣은 값': {k[:8]: v for k, v in (seeded or {}).items()}})
        KEEP.setdefault('namex', {})[tag] = {r['note']: round(r['nr']['x'] - r['rr']['x'], 2) for r in rows if r.get('nr') and r.get('rr')}
        t131 = row(L, N131)
        T(g, 'A1b 토글 자리 = 줄 들여쓰기 칸(left = paddingLeft − 15px) · 9px 꺾쇠 · aria-expanded=false',
          bool(t131.get('tr')) and near(t131['tr']['x'] - t131['rr']['x'], int(t131['pl'][:-2]) - 15, 0.6) and t131.get('aria') == 'false',
          {'dx': t131.get('tr') and round(t131['tr']['x'] - t131['rr']['x'], 2), 'pl': t131.get('pl'), 'aria': t131.get('aria')})
        if not t131.get('tg'):
            T(g, 'A3~A5 묶음 — 토글이 없다(바탕이면 헛잣대 그대로)', False, t131.get('note')); return
        # A3 — 1.3.1 › 누름
        p.click(p.ev("n=>__HC.tgAt(n)", N131), 300)
        c = p.ev("([n,ms])=>__HC.clipWait(n,ms)", [N131, 60000])
        L = p.ev("()=>__HC.list()"); r = row(L, N131)
        sp = (seeded or {}).get(N131) or {}
        R0 = sp.get('r') or [0, 0, 1, 1]
        ratio = (R0[3] - R0[1]) / max(1e-6, R0[2] - R0[0])
        ok = bool(c) and c['vis'] and near(c['v']['h'], c['bx']['h'], 1) and near(c['v']['x'], c['bx']['x'], 1) and near(c['v']['y'], c['bx']['y'], 1) \
            and near(c['v']['w'], c['bx']['w'], 1) and near(c['bx']['h'], c['bx']['w'] * ratio, 1.5) and c['foot'].startswith('%s쪽 · 영역 지정' % sp.get('p')) \
            and r.get('open') and r.get('aria') == 'true' and L['mkcw'] == 1 and c['ol'] == ['solid', '2px', 'rgb(249, 115, 22)'] and c['pg'] == 1 and c['ln'] > 10
        T(g, 'A3 1.3.1 › mouse.click → 펼침 1 · 보기 칸 높이 = 네모 높이(±1px) · 주황 테(2px #f97316) = 칸과 같은 자리 · 발 「N쪽 · 영역 지정」 · ⌄',
          ok, {'v': c and c['v'], 'bx': c and c['bx'], 'ratio': round(ratio, 3), 'foot': c and c['foot'], 'open': r.get('open'), 'ol': c and c['ol'], 'pg': c and c['pg'], 'ln': c and c['ln']})
        p.shot('%s_A_open' % tag) if tag == 'NEW' else None
        p.click(p.ev("n=>__HC.tgAt(n)", N131), 400)
        L = p.ev("()=>__HC.list()"); r = row(L, N131)
        T(g, 'A3b 다시 누르면 접힘(펼친 칸 0 · › · aria-expanded=false)', bool(L) and L['mkcw'] == 0 and r.get('open') is False and r.get('aria') == 'false', {'mkcw': L and L['mkcw'], 'open': r.get('open')})
        # 긴 네모(1.4) — 잘림 0
        p.click(p.ev("n=>__HC.tgAt(n)", N14), 300)
        c = p.ev("([n,ms])=>__HC.clipWait(n,ms)", [N14, 60000])
        s4 = (seeded or {}).get(N14) or {}
        R4 = s4.get('r') or [0, 0, 1, 1]
        r4 = (R4[3] - R4[1]) / max(1e-6, R4[2] - R4[0])
        T(g, 'A3c 1.4 처럼 긴 네모도 잘림 0 — 보기 칸 높이 = 네모 높이(상한 없음 · ±1px) · 폭에 꽉',
          bool(c) and near(c['v']['h'], c['bx']['h'], 1) and near(c['bx']['h'], c['bx']['w'] * r4, 1.5) and near(c['v']['w'], c['bx']['w'], 1),
          {'v': c and c['v'], 'bx': c and c['bx'], '높이/폭': round(r4, 3)})
        p.click(p.ev("n=>__HC.tgAt(n)", N14), 300)
        # A4 — 확대 · 옮기기 · 두 번 · 한 번 · Ctrl 없는 휠
        p.click(p.ev("n=>__HC.tgAt(n)", N131), 300)
        c0 = p.ev("([n,ms])=>__HC.clipWait(n,ms)", [N131, 60000])
        pt = p.ev("([n,x,y])=>__HC.clipPt(n,x,y)", [N131, .5, .5])
        c0 = p.ev("n=>__HC.clip(n)", N131); s0 = p.ev("n=>__HC.clipScroller(n)", N131)
        if not (c0 and pt and pt['on']):
            T(g, 'A4 묶음 — 펼친 그림이 없다', False, {'c0': c0, 'pt': pt}); return
        p.pg.mouse.move(pt['x'], pt['y']); p.pg.wait_for_timeout(100)
        p.pg.keyboard.down('Control')
        for _ in range(4):
            p.pg.mouse.wheel(0, -100); p.pg.wait_for_timeout(120)
        p.pg.keyboard.up('Control'); p.pg.wait_for_timeout(300)
        c1 = p.ev("n=>__HC.clip(n)", N131); s1 = p.ev("n=>__HC.clipScroller(n)", N131)
        u0 = (pt['x'] - c0['v']['x'] - c0['t'][0]) / c0['s']; u1 = (pt['x'] - c1['v']['x'] - c1['t'][0]) / c1['s']
        w0 = (pt['y'] - c0['v']['y'] - c0['t'][1]) / c0['s']; w1 = (pt['y'] - c1['v']['y'] - c1['t'][1]) / c1['s']
        T(g, 'A4a Ctrl+휠 4번 → 확대(배율 ↑ · 끌기 손 모양) · 마우스 밑 쪽 자리 그대로(±1px) · 목록은 안 굴러감',
          c1['s'] > c0['s'] * 1.3 and c1['z'] and near(u0, u1, 1) and near(w0, w1, 1) and (s0 or {}).get('st') == (s1 or {}).get('st'),
          {'s': [c0['s'], c1['s']], 'z': c1['z'], 'under': [[round(u0, 1), round(w0, 1)], [round(u1, 1), round(w1, 1)]], 'list': [(s0 or {}).get('st'), (s1 or {}).get('st')]})
        if tag == 'NEW':
            p.shot('%s_A_zoom' % tag)
        pt = p.ev("([n,x,y])=>__HC.clipPt(n,x,y)", [N131, .5, .5])
        p.drag(pt['x'], pt['y'], pt['x'] - 60, pt['y'] - 40)
        c2 = p.ev("n=>__HC.clip(n)", N131)
        T(g, 'A4b 마우스 끌기 → 옮김(−60, −40 ±2) · 배율 무변', near(c2['t'][0] - c1['t'][0], -60, 2) and near(c2['t'][1] - c1['t'][1], -40, 2) and c2['s'] == c1['s'],
          {'d': [round(c2['t'][0] - c1['t'][0], 1), round(c2['t'][1] - c1['t'][1], 1)], 's': c2['s']})
        pt = p.ev("([n,x,y])=>__HC.clipPt(n,x,y)", [N131, .5, .5])
        p.pg.mouse.dblclick(pt['x'], pt['y']); p.pg.wait_for_timeout(700)
        c3 = p.ev("n=>__HC.clip(n)", N131)
        T(g, 'A4c 두 번 누름 → 처음 크기 · 자리(팝업은 안 뜸)', near(c3['s'], c0['s'], 1e-6) and near(c3['t'][0], c0['t'][0], 0.5) and near(c3['t'][1], c0['t'][1], 0.5) and not p.ev("()=>__HC.omrKeys()"),
          {'s': [c0['s'], c3['s']], 't': [c0['t'], c3['t']], 'pops': p.ev("()=>__HC.omrKeys()")})
        pt = p.ev("([n,x,y])=>__HC.clipPt(n,x,y)", [N131, .5, .5])
        p.pg.mouse.click(pt['x'], pt['y']); p.until("k=>__HC.omrKeys().indexOf('cv|omr|'+k)>=0", k131, 5000); p.pg.wait_for_timeout(300)
        T(g, 'A4d 한 번 누름 → 「▦ 정리OMR · 1.3.1…」 팝업', p.ev("k=>__HC.omrTitle(k)", k131) == '▦ 정리OMR · ' + N131, {'title': p.ev("k=>__HC.omrTitle(k)", k131), 'pops': p.ev("()=>__HC.omrKeys()")})
        p.ev("()=>__HC.omrClose()"); p.pg.wait_for_timeout(200)
        c4 = p.ev("n=>__HC.clip(n)", N131); pt = p.ev("([n,x,y])=>__HC.clipPt(n,x,y)", [N131, .5, .5]); s4a = p.ev("n=>__HC.clipScroller(n)", N131)
        p.pg.mouse.move(pt['x'], pt['y']); p.pg.wait_for_timeout(80); p.pg.mouse.wheel(0, 200); p.pg.wait_for_timeout(400)
        c5 = p.ev("n=>__HC.clip(n)", N131); s5 = p.ev("n=>__HC.clipScroller(n)", N131)
        T(g, 'A4e Ctrl 없는 휠 = 목록 굴림(목록 창 scrollTop ↑) · 그림 배율·자리 무변', bool(s4a) and bool(s5) and s5['st'] > s4a['st'] + 20 and c5['s'] == c4['s'] and c5['t'] == c4['t'],
          {'list': [s4a and s4a['st'], s5 and s5['st']], 'scroller': s5 and s5['cls'], 's': [c4['s'], c5['s']]})
        # A5 — 정리OMR 팝업에서 되돌리기 → 토글·그림 사라짐 · 새로 찍기 → 토글
        p.ev("()=>__HC.frontList()")
        p.click(p.ev("n=>__HC.pinAt(n)", N131), 300)
        p.until("k=>__HC.omrKeys().indexOf('cv|omr|'+k)>=0", k131, 20000); p.pg.wait_for_timeout(400)
        p.click(p.ev("k=>__HC.omrAt(k,'rv')", k131), 600)
        L = p.ev("()=>__HC.list()"); r = row(L, N131)
        T(g, 'A5a 「자동으로 되돌리기」 → 그 줄 토글 사라짐(화면 기준) · 펼친 그림 사라짐', r.get('tg') and not r.get('tgVis') and not r.get('cw'), {'tgVis': r.get('tgVis'), 'cw': r.get('cw'), 'ls': (p.ev("()=>__HC.ls()") or {}).get(k131)})
        p.click(p.ev("k=>__HC.omrAt(k,'pick')", k131), 300)
        a = p.ev("([k,x,y])=>__HC.vpt(k,x,y)", [k131, .30, .30]); b = p.ev("([k,x,y])=>__HC.vpt(k,x,y)", [k131, .62, .58])
        p.drag(a['x'], a['y'], b['x'], b['y'])
        p.click(p.ev("k=>__HC.omrAt(k,'ok')", k131), 600)
        L = p.ev("()=>__HC.list()"); r = row(L, N131)
        V = (p.ev("()=>__HC.ls()") or {}).get(k131) or {}
        T(g, 'A5b 새로 찍기(▭ 영역 지정 → 확정) → 토글 나타남', r.get('tgVis') is True and bool(V.get('r')), {'tgVis': r.get('tgVis'), 'v': V})
        p.ev("()=>__HC.omrClose()")
        L = p.ev("async()=>{await __HC.mokOpen();return await __HC.listPainted(60000)}")
        c = p.ev("([n,ms])=>__HC.clipWait(n,ms)", [N131, 20000]); r = row(p.ev("()=>__HC.list()"), N131)
        T(g, 'A3d 목록 창을 닫고 다시 열어도 펼친 줄은 펼친 채(이 세션 안 기억 · 저장 안 함)', bool(c) and c['vis'] and r.get('open') is True, {'open': r.get('open'), 'clip': bool(c)})

    # ── A6 · 다른 법 목차노트 목록 DOM ──
    def secA6():
        out = {}
        for law in p.ev("()=>__HC.laws()"):
            if law == '민사소송법':
                continue
            p.ev("l=>__HC.boot('jo',l)", law)
            p.ev("async()=>{await __HC.mokOpen();return await __HC.listPainted(30000)}")
            h = p.ev("()=>__HC.listHtml()")
            out[law] = hashlib.md5((h or '').encode('utf-8')).hexdigest() + ':%d' % len(h or '')
        KEEP.setdefault('lawdom', {})[tag] = out
        N(g, 'A6 다른 법 목차노트 목록 DOM(md5:길이) — 바탕과 맞대기는 끝에', out)

    # ── B ──
    def secB():
        cv = p.ev("async()=>await __HC.canvasBoot()")
        p.pg.fill('#cvQ', ''); p.pg.type('#cvQ', Q_MS, delay=20); p.pg.wait_for_timeout(600)
        nq = p.ev("()=>__HC.cvQ()")
        KEEP.setdefault('cvqn', {})[tag] = nq
        p.ev("()=>__HC.boot('jo')")
        p.sk_open(['omr'], ['민사소송법', '특허법'], Q_MS)
        G2 = p.ev("()=>__HC.skGroups()"); gr = grp_of(G2, '📖 정리')
        ms = [x for x in (gr or {}).get('rows', []) if x['tag'].startswith('민소')]
        n = int(re.search(r'— (\d+)건', gr['h']).group(1)) if gr and re.search(r'— (\d+)건', gr['h']) else None
        T(g, 'B8 민소+특허 · 「%s」 → 「📖 정리 — N건」 = 정리 탭 검색칸 수(#cvQn) · 민소 줄 = min(40, N)(헛잣대: 바탕 0건)' % Q_MS,
          bool(gr) and n is not None and str(n) == nq['n'] and n > 0 and len(ms) == min(40, n), {'머리': gr and gr['h'], 'cvQn': nq['n'], '민소 줄': len(ms)})
        T(g, 'B8b 줄 꼴 — 머리 「N쪽 · 목차노트」 · 꼬리표 「민소 · 정리」(메모면 · 메모) · 문맥 줄에 검색어 굵게 · 아이콘 📖',
          bool(ms) and all(re.match(r'^\d+쪽( · .+)?$', x['head']) and x['tag'] in ('민소 · 정리', '민소 · 정리 · 메모') and x['ctxB'] == Q_MS and x['hasctx'] and x['icon'] == '📖' for x in ms),
          {'첫 줄': ms[:2]})
        p.pg.keyboard.press('Escape'); p.pg.wait_for_timeout(200)
        p.sk_open(['omr'], ['특허법'], Q_PT)
        G3 = p.ev("()=>__HC.skGroups()"); g3 = grp_of(G3, '📖 정리')
        m3 = re.search(r'— (\d+)건', (g3 or {}).get('h', ''))
        KEEP.setdefault('ptn', {})[tag] = {'n': int(m3.group(1)) if m3 else None, 'rows': len((g3 or {}).get('rows', [])), 'first': (g3 or {}).get('rows', [])[:1]}
        N(g, 'B8c 특허만 「%s」 — 수(바탕과 맞대기는 끝에)' % Q_PT, KEEP['ptn'][tag])
        p.pg.keyboard.press('Escape'); p.pg.wait_for_timeout(200)
        # B8d — 정리캔버스를 못 읽으면 0건 침묵 대신 문구(창구를 잠깐 막아 잰다)
        p.ev("()=>{window.__vf=viewCanvas.find;viewCanvas.find=async()=>{throw new Error('하네스 막음')};return 1}")
        p.sk_open(['omr'], ['민사소송법', '특허법'], Q_MS)
        g4 = grp_of(p.ev("()=>__HC.skGroups()"), '📖 정리')
        p.ev("()=>{viewCanvas.find=window.__vf;return 1}")
        T(g, 'B8d 민소 정리를 못 읽으면 머리에 「… 민소 정리를 읽지 못했다」(0건 침묵 금지)', bool(g4) and g4['h'].endswith('민소 정리를 읽지 못했다'), g4 and g4['h'])
        p.pg.keyboard.press('Escape'); p.pg.wait_for_timeout(200)
        # B8e — 상한 40 · 머리 「(앞 40건 · 전부는 정리 탭 검색칸)」 · 수 = 정리 탭 검색칸
        p.ev("async()=>await __HC.canvasBoot()")
        p.pg.fill('#cvQ', ''); p.pg.type('#cvQ', Q_JO, delay=20); p.pg.wait_for_timeout(700)
        nj = p.ev("()=>__HC.cvQ()")['n']
        p.ev("()=>__HC.boot('jo')")
        p.sk_open(['omr'], ['민사소송법'], Q_JO)
        g5 = grp_of(p.ev("()=>__HC.skGroups()"), '📖 정리')
        KEEP.setdefault('capn', {})[tag] = nj
        T(g, 'B8e 「%s」 %s건 → 민소 줄 상한 40 · 머리 「📖 정리 — %s건 (앞 40건 · 전부는 정리 탭 검색칸)」' % (Q_JO, nj, nj),
          bool(g5) and nj.isdigit() and int(nj) > 40 and len(g5['rows']) == 40 and g5['h'] == '📖 정리 — %s건 (앞 40건 · 전부는 정리 탭 검색칸)' % nj, {'머리': g5 and g5['h'], '줄': g5 and len(g5['rows']), 'cvQn': nj})
        p.pg.keyboard.press('Escape'); p.pg.wait_for_timeout(200)

    # ── C ──
    def secC():
        C0 = p.ev("async()=>await __HC.canvasBoot()")
        p.ev("v=>__HC.cvSet(v)", {'vz': 0.35}); p.pg.wait_for_timeout(200)
        p.pg.fill('#cvQ', ''); p.pg.type('#cvQ', Q_MS, delay=20); p.pg.wait_for_timeout(700)
        hi = p.ev("()=>__HC.hitsInfo()"); cv0 = p.ev("()=>__HC.cv()"); st = p.ev("()=>__HC.stage()")
        kk = 5 if hi and hi['n'] > 5 else 0
        if tag == 'NEW':
            p.shot('%s_C_before' % tag)
        at = p.ev("k=>__HC.hitRowAt(k)", kk)
        p.click(at, 450)
        cv1 = p.ev("()=>__HC.cv()"); m = p.ev("()=>__HC.markCur()"); hi2 = p.ev("()=>__HC.hitsInfo()")
        L = max(0, min(st['w'] - 80, hi['rect']['r'] - st['x'] + 16)) if hi and hi['n'] else 0
        tx, ty = st['x'] + L + (st['w'] - L) / 2, st['y'] + st['h'] / 2
        centred = bool(m) and near(m['cx'], tx, 60) and near(m['cy'], ty, 60)
        onscr = bool(m) and m['cx'] > st['x'] + L and m['cx'] < st['r'] and m['cy'] > st['y'] and m['cy'] < st['b'] and not m['underList']
        T(g, 'C9·C10 vz 0.35 · 「%s」 · 목록 %d번째 줄 mouse.click → 0.4초 뒤 vz 2 · 찾은 글자 = (목록 오른쪽 ~ 무대 오른쪽) 가운데 ±60 · 무대 세로 가운데 ±60(무대 끝이면 화면 안·목록에 안 가림) · 그 줄 .cur(헛잣대: 바탕 무변)' % (Q_MS, kk + 1),
          bool(at and at.get('on')) and near(cv1['vz'], 2, 0.01) and (centred or onscr) and (hi2 or {}).get('cur') == [kk],
          {'vz': [cv0['vz'], cv1['vz']], 'vxy': [[cv0['vx'], cv0['vy']], [cv1['vx'], cv1['vy']]], 'mark': m and [m['cx'], m['cy']], 'target': [round(tx), round(ty)], 'centred': centred, 'onscr': onscr, 'cur': (hi2 or {}).get('cur'), 'at': at and at.get('at')})
        if tag == 'NEW':
            p.shot('%s_C_after' % tag)
        p.ev("v=>__HC.cvSet(v)", {'vz': 3}); p.pg.wait_for_timeout(200)
        k2 = 8 if hi and hi['n'] > 8 else 1
        p.click(p.ev("k=>__HC.hitRowAt(k)", k2), 450)
        cv2 = p.ev("()=>__HC.cv()"); hi3 = p.ev("()=>__HC.hitsInfo()")
        T(g, 'C10b vz 3 에서 누르면 3 유지 · 그 줄 .cur', near(cv2['vz'], 3, 0.01) and (hi3 or {}).get('cur') == [k2], {'vz': cv2['vz'], 'cur': (hi3 or {}).get('cur')})
        # C10d — 검색칸 Enter = 다음 결과로 같은 확대
        p.ev("v=>__HC.cvSet(v)", {'vz': 0.35}); p.pg.wait_for_timeout(150)
        p.pg.focus('#cvQ'); p.pg.keyboard.press('Enter'); p.pg.wait_for_timeout(450)
        cv3 = p.ev("()=>__HC.cv()"); hi4 = p.ev("()=>__HC.hitsInfo()")
        T(g, 'C10d 검색칸 Enter → 다음 결과로 같은 확대(vz 2 · 그 줄 .cur)', near(cv3['vz'], 2, 0.01) and (hi4 or {}).get('cur') == [(k2 + 1) % max(1, hi4['n'])],
          {'vz': cv3['vz'], 'cur': (hi4 or {}).get('cur'), 'want': (k2 + 1) % max(1, (hi4 or {}).get('n') or 1)})
        # C10e — 쪽 그림 mouse.click = 그 쪽 첫 결과로 같은 확대
        p.ev("v=>__HC.cvSet(v)", {'vz': 0.35}); p.pg.wait_for_timeout(150)
        th = p.ev("i=>__HC.thAt(i)", 0)
        p.click(th, 450)
        cv5 = p.ev("()=>__HC.cv()"); hi5 = p.ev("()=>__HC.hitsInfo()")
        T(g, 'C10e 쪽 그림 mouse.click → 그 쪽 첫 결과로 같은 확대(vz 2 · .cur)', bool(th and th.get('on')) and near(cv5['vz'], 2, 0.01) and (hi5 or {}).get('cur') == [th.get('k0')],
          {'vz': cv5['vz'], 'cur': (hi5 or {}).get('cur'), 'k0': th and th.get('k0'), 'at': th and th.get('at')})
        # C10c — 목록 위 휠 = 목록 굴림(「임의관할」 15 줄은 한 화면에 들어 긴 목록 「관할」 로 잰다)
        p.pg.fill('#cvQ', ''); p.pg.type('#cvQ', Q_JO, delay=20); p.pg.wait_for_timeout(800)
        h0 = p.ev("()=>__HC.hitsInfo()"); z0 = p.ev("()=>__HC.cv()")
        if h0 and h0['sh'] > h0['ch'] + 10:
            hr = h0['rect']; p.pg.mouse.move(hr['cx'], hr['y'] + min(hr['h'] - 10, 150)); p.pg.wait_for_timeout(80)
            p.pg.mouse.wheel(0, 240); p.pg.wait_for_timeout(400)
            h1 = p.ev("()=>__HC.hitsInfo()"); z1 = p.ev("()=>__HC.cv()")
            T(g, 'C10c 목록(「%s」 %d줄) 위 휠 = 목록 scrollTop 변화 · vz·vx·vy 무변' % (Q_JO, h0['n']), h1['st'] > h0['st'] and z1 == z0, {'st': [h0['st'], h1['st']], 'cv': [z0, z1]})
        else:
            T(g, 'C10c 목록이 짧아 휠을 못 잰다', False, h0)

    # ── D ──
    def secD():
        p.ev("async()=>await __HC.canvasBoot()"); p.ev("v=>__HC.cvSet(v)", {'vz': 0.35})   # 정리 탭 배율을 2 아래로(앞 묶음 C 가 3 에 두었다 — D13a 가 2 를 잰다)
        p.ev("()=>__HC.boot('jo')")
        H = p.ev("q=>__HC.find(q)", Q_MS)
        H = H if isinstance(H, list) else []
        p.sk_open(['omr'], ['민사소송법'], Q_MS)
        at = p.ev("([p,i])=>__HC.skRowAt(p,i)", ['📖 정리', 5])
        if not (at and at.get('on')):
            T(g, 'D11 민소 조문 탭 · Ctrl K 「%s」 · 정리 6번째 줄 — 줄이 없다(바탕이면 헛잣대 그대로)' % Q_MS, False, {'groups': [x['h'] for x in p.ev("()=>__HC.skGroups()")]}); return
        p.click(at, 300)
        s = p.until("()=>{const s=__HC.sf();return s.n&&s.cvpg?s:null}", None, 30000) or p.ev("()=>__HC.sf()")
        stt = p.ev("()=>__HC.state()"); sk = p.ev("()=>__HC.sk()")
        n6 = H[5]['n'] if len(H) > 5 else None
        T(g, 'D11 민소 조문 탭 · Ctrl K 「%s」 · 정리 6번째 줄 mouse.click → 탭 무변 · 검색창 닫힘 · 팝업 1 · 「🔍 정리 · 민소 N쪽」 · 「6 / %d」 · 주황 1 이 보기 칸 안(헛잣대: 바탕엔 민소 줄이 없다)' % (Q_MS, len(H)),
          bool(at and at.get('on')) and stt['tab'] == 'jo' and sk['disp'] == 'none' and s.get('n') == 1 and s.get('title') == '🔍 정리 · 민소 %s쪽' % n6
          and s.get('sfn') == '6 / %d' % len(H) and s.get('pin') == 1 and inside(s.get('pinR'), s.get('vr')) and s.get('zoomUi') == 0,
          {'tab': stt['tab'], 'sk': sk['disp'], 'n': s.get('n'), 'title': s.get('title'), 'sfn': s.get('sfn'), 'pin': s.get('pin'), 'pinR': s.get('pinR'), 'vr': s.get('vr'), 'where': s.get('where'), 'msg': s.get('msg')})
        if not s.get('n'):
            return
        T(g, 'D11a 꼴 — 막대 ◀ ▶ + 목차노트 이름 · 발 「「검색어」 · 휠·두 손가락 = 확대 · 끌기 = 옮기기」 + 「정리 탭 이 자리로 →」 · 첫 크기 폭 min(820, 화면−24) · 높이 min(화면×0.74, 680) · 가운데',
          s['go'] == '정리 탭 이 자리로 →' and s['msg'] == '「%s」 · 휠·두 손가락 = 확대 · 끌기 = 옮기기' % Q_MS and near(s['rect']['w'], 820, 2) and near(s['rect']['h'], 666, 2)
          and near(s['rect']['cx'], 720, 3) and s['where'] == (H[5].get('head') or ''), {'rect': s['rect'], 'where': s['where'], 'go': s['go']})
        pr, vr = s.get('pinR') or {}, s.get('vr') or {}
        T(g, 'D11e 첫 배율 1.6 · 찾은 글자(주황)가 보기 칸 가운데(±10px — 스크롤 막대 몫)', near(s['s'], 1.6, 1e-6) and near(pr.get('cx'), vr.get('cx'), 10) and near(pr.get('cy'), vr.get('cy'), 10),
          {'s': s['s'], 'pin': [pr.get('cx'), pr.get('cy')], 'view': [vr.get('cx'), vr.get('cy')]})
        p.shot('%s_D_minso' % tag)
        # 휠(Ctrl 없이) — 팝업 안에서 확대 · 뒤로 안 샘
        v = s['vr']; p.pg.mouse.move(v['cx'], v['cy']); p.pg.wait_for_timeout(80); p.pg.mouse.wheel(0, -120); p.pg.wait_for_timeout(300)
        s1 = p.ev("()=>__HC.sf()")
        T(g, 'D11d 휠(Ctrl 없이) → 팝업 쪽 확대(배율 ↑)', s1['s'] > s['s'] * 1.1, {'s': [s['s'], s1['s']]})
        p.click(p.ev("()=>__HC.sfAt('next')"), 500)
        s2 = p.ev("()=>__HC.sf()")
        T(g, 'D11b ▶ mouse.click → 「7 / %d」 · 주황 1' % len(H), s2['sfn'] == '7 / %d' % len(H) and s2['pin'] == 1 and inside(s2['pinR'], s2['vr']), {'sfn': s2['sfn'], 'title': s2['title']})
        p.sk_open(['omr'], ['민사소송법'], Q_MS)
        p.click(p.ev("([p,i])=>__HC.skRowAt(p,i)", ['📖 정리', 1]), 600)
        s3 = p.until("()=>{const s=__HC.sf();return s.n&&s.sfn&&s.sfn.indexOf('2 /')===0?s:null}", None, 20000) or p.ev("()=>__HC.sf()")
        T(g, 'D11c 다른 줄(2번째) → 창은 여전히 1 · 「2 / %d」' % len(H), s3['n'] == 1 and s3['sfn'] == '2 / %d' % len(H), {'n': s3['n'], 'sfn': s3['sfn']})
        p.click(p.ev("()=>__HC.sfAt('prev')"), 500)
        s4 = p.ev("()=>__HC.sf()")
        T(g, 'D11g ◀ → 「1 / %d」 · 처음에서 ◀ 비활성 · ▶ 살아 있음' % len(H), s4['sfn'] == '1 / %d' % len(H) and s4['prevDis'] and not s4['nextDis'], {'sfn': s4['sfn'], 'prevDis': s4['prevDis'], 'nextDis': s4['nextDis']})
        v = s4['vr']; sl0, st0 = s4['sl'], s4['st']
        p.drag(v['cx'], v['cy'], v['cx'] - 80, v['cy'] - 50)
        s5 = p.ev("()=>__HC.sf()")
        T(g, 'D11h 팝업 안 마우스 끌기 = 옮기기(스크롤 +80 · +50 ±4) · 배율 무변', near(s5['sl'] - sl0, 80, 4) and near(s5['st'] - st0, 50, 4) and s5['s'] == s4['s'],
          {'d': [s5['sl'] - sl0, s5['st'] - st0], 's': [s4['s'], s5['s']]})
        # D14 — 팝업 띄운 채 Ctrl K
        p.blur(); p.pg.keyboard.press('Control+k'); p.pg.wait_for_timeout(300)
        tp = p.ev("()=>__HC.skTop()")
        T(g, 'D14 팝업 띄운 채 Ctrl K → 검색창이 팝업 위(검색칸 가운데 elementFromPoint = #sk 안)', bool(tp) and tp['onSk'], tp)
        p.pg.keyboard.press('Escape'); p.pg.wait_for_timeout(200)
        # D13a — 민소 「정리 탭 이 자리로 →」
        kcur = p.ev("()=>__HC.sf().k")
        p.click(p.ev("()=>__HC.sfAt('go')"), 300)
        p.until("q=>{const c=__HC.cvQ();return S.tab==='omr'&&c.q===q&&__HC.hitsInfo()&&__HC.hitsInfo().cur.length?1:0}", Q_MS, 60000)
        p.pg.wait_for_timeout(600)
        stt = p.ev("()=>__HC.state()"); q = p.ev("()=>__HC.cvQ()"); hi = p.ev("()=>__HC.hitsInfo()"); cv = p.ev("()=>__HC.cv()"); sf = p.ev("()=>__HC.sf()")
        T(g, 'D13a 민소 「정리 탭 이 자리로 →」 → 정리 탭 · 검색칸 「%s」 · 그 결과 .cur · vz 2 · 팝업 닫힘' % Q_MS,
          stt['tab'] == 'omr' and stt['law'] == '민사소송법' and q['q'] == Q_MS and (hi or {}).get('cur') == [kcur] and near((cv or {}).get('vz'), 2, 0.01) and sf['n'] == 0,
          {'state': stt, 'q': q, 'cur': (hi or {}).get('cur'), 'k': kcur, 'vz': (cv or {}).get('vz'), 'pop': sf['n']})
        # D11f — 목록 상한(40) 밖 결과로도 ▶ 가 넘어간다(전체 수 기준)
        p.ev("()=>__HC.boot('jo')")
        p.sk_open(['omr'], ['민사소송법'], Q_JO)
        p.click(p.ev("([p,i])=>__HC.skRowAt(p,i)", ['📖 정리', 39]), 300)
        s6 = p.until("()=>{const s=__HC.sf();return s.n&&s.sfn&&s.sfn.indexOf('40 /')===0?s:null}", None, 20000) or p.ev("()=>__HC.sf()")
        p.click(p.ev("()=>__HC.sfAt('next')"), 500)
        s7 = p.ev("()=>__HC.sf()")
        nh = s6.get('nh') or 0
        T(g, 'D11f 「%s」 40번째 줄 → 「40 / N」 → ▶ → 「41 / N」(목록 상한 밖 결과도 넘어감)' % Q_JO, nh > 40 and s6.get('sfn') == '40 / %d' % nh and s7.get('sfn') == '41 / %d' % nh and s7.get('pin') == 1,
          {'sfn': [s6.get('sfn'), s7.get('sfn')], 'nh': nh})
        p.ev("()=>__HC.sfClose()")
        # D12 — 특허
        p.ev("()=>__HC.boot('jo')")
        p.sk_open(['omr'], ['특허법'], Q_PT)
        G3 = p.ev("()=>__HC.skGroups()"); g3 = grp_of(G3, '📖 정리')
        p1 = int(re.match(r'^(\d+)쪽', g3['rows'][0]['head']).group(1)) if g3 and g3['rows'] else None
        p.click(p.ev("([p,i])=>__HC.skRowAt(p,i)", ['📖 정리', 0]), 300)
        s = p.until("()=>{const s=__HC.sf();return s.n&&s.imgs&&s.imgOk===s.imgs?s:null}", None, 30000) or p.ev("()=>__HC.sf()")
        tm = G['tiles'].get(str(p1)) or {}
        T(g, 'D12 특허 「%s」 첫 줄 → 「🔍 정리 · 특허 %s쪽」 · 타일 %s장 다 받음 · 끝 칸 타일 제 폭 · 주황 1 보기 칸 안 · 탭 무변' % (Q_PT, p1, tm.get('cols', 0) * tm.get('rows', 0)),
          s.get('n') == 1 and s.get('title') == '🔍 정리 · 특허 %s쪽' % p1 and s.get('imgs') == tm.get('cols', 0) * tm.get('rows', 0) and s.get('imgOk') == s.get('imgs')
          and s.get('pin') == 1 and inside(s.get('pinR'), s.get('vr')) and p.ev("()=>S.tab") == 'jo' and bool(s.get('imgSz')) and near(s['imgSz'][0][0], s['imgSz'][0][1], 1),
          {'title': s.get('title'), 'imgs': [s.get('imgOk'), s.get('imgs')], 'imgSz': s.get('imgSz'), 'pin': s.get('pin'), 'pinR': s.get('pinR'), 'vr': s.get('vr'), 'where': s.get('where')})
        p.shot('%s_D_patent' % tag)
        # D13b — 특허 「정리 탭 이 자리로 →」(민소 탭에서)
        p.click(p.ev("()=>__HC.sfAt('go')"), 300)
        p.until("()=>S.law==='특허법'&&S.tab==='omr'?1:0", None, 20000); p.pg.wait_for_timeout(500)
        stt = p.ev("()=>__HC.state()")
        T(g, 'D13b 특허 「정리 탭 이 자리로 →」(민소 탭에서) → 특허법 · 정리 탭 · 그 쪽(옛 판은 민소 정리로 갔다)',
          stt['law'] == '특허법' and stt['tab'] == 'omr' and stt['omrPage'] == p1 and p.ev("()=>__HC.sf().n") == 0, stt)

    # ── D15 — 다른 범위 결과 누름 = 바탕 ──
    def secD15():
        out = {}
        for sc, ql in (('jo', Q_JO), ('prec', Q_JO)):
            p.ev("()=>__HC.boot('jo')")
            p.sk_open([sc], ['민사소송법'], ql)
            G4 = p.ev("()=>__HC.skGroups()")
            gg = next((x for x in G4 if x['rows'] and not x['h'].startswith('📖 정리')), None)
            at = p.ev("([p,i])=>__HC.skRowAt(p,i)", [gg['h'][:4], 0]) if gg else None
            p.click(at, 1200)
            out[sc] = {'grp': gg and gg['h'], 'first': gg and gg['rows'][0]['head'], 'state': p.ev("()=>__HC.state()"), 'pops': p.ev("()=>POPS.map(x=>x._pk)"), 'sk': p.ev("()=>__HC.sk().disp")}
        KEEP.setdefault('other', {})[tag] = out
        N(g, 'D15 다른 범위(조문·판례) 첫 줄 누름 — 바탕과 맞대기는 끝에', out)

    try:
        for nm, fn in (('A', secA), ('A6', secA6), ('B', secB), ('C', secC), ('D', secD), ('D15', secD15)):
            sec(nm, fn)
        er = p.errs_all()
        T(g, 'Z 페이지 오류 0', not er, er[:6])
    finally:
        p.close()


# ══════════ 터치 문맥(touchscreen.tap · CDP 한 손가락) ══════════
def scen_touch(br, src, tag, G):
    g = '%s 터치' % tag
    p = Pg(br, tag + 'T', src, 1440, 900, touch=True)
    NOTES = G['notes5']; N131 = NOTES[0]
    try:
        # A — 토글 톡 · 한 손가락 세로 끌기 = 목록 굴림
        p.ev("()=>__HC.boot('jo')"); p.ev("async()=>await __HC.ensure()")
        p.ev("n=>__HC.seedPins(n)", NOTES)
        p.ev("async()=>{await __HC.mokOpen();return await __HC.listPainted(90000)}")
        at = p.ev("n=>__HC.tgAt(n)", N131)
        c0 = None
        if at:
            p.click(at, 300); c0 = p.ev("([n,ms])=>__HC.clipWait(n,ms)", [N131, 60000])
        T(g, 'A3t › touchscreen.tap → 펼침', bool(c0) and c0['vis'] and c0['ta'] == 'none', {'v': c0 and c0['v'], 'ta': c0 and c0['ta']})
        if c0:
            pt = p.ev("([n,x,y])=>__HC.clipPt(n,x,y)", [N131, .5, .7]); s0 = p.ev("n=>__HC.clipScroller(n)", N131)
            p.fdrag(pt['x'], pt['y'], pt['x'], pt['y'] - 80)
            c1 = p.ev("n=>__HC.clip(n)", N131); s1 = p.ev("n=>__HC.clipScroller(n)", N131)
            T(g, 'A4t 한 손가락 세로 끌기(확대 전) = 목록 굴림(≈ 80px) · 그림 무변', bool(s0) and bool(s1) and near(s1['st'] - s0['st'], 80, 12) and c1['s'] == c0['s'] and c1['t'] == c0['t'],
              {'list': [s0 and s0['st'], s1 and s1['st']], 'scroller': s1 and s1['cls'], 's': [c0['s'], c1['s']]})
            pt = p.ev("([n,x,y])=>__HC.clipPt(n,x,y)", [N131, .5, .5]); c2 = p.ev("n=>__HC.clip(n)", N131); s2 = p.ev("n=>__HC.clipScroller(n)", N131)
            p.pinch(pt['x'], pt['y'], 60, 180)
            c3 = p.ev("n=>__HC.clip(n)", N131); s3 = p.ev("n=>__HC.clipScroller(n)", N131)
            T(g, 'A4u 두 손가락 벌리기 = 그림 확대(배율 ↑ · 목록 무변)', c3['s'] > c2['s'] * 1.8 and (s2 or {}).get('st') == (s3 or {}).get('st'), {'s': [c2['s'], c3['s']], 'list': [(s2 or {}).get('st'), (s3 or {}).get('st')]})
        # C — 목록 줄 톡
        p.ev("async()=>await __HC.canvasBoot()")
        p.ev("v=>__HC.cvSet(v)", {'vz': 0.35}); p.pg.wait_for_timeout(200)
        p.pg.fill('#cvQ', ''); p.pg.type('#cvQ', Q_MS, delay=20); p.pg.wait_for_timeout(700)
        hi = p.ev("()=>__HC.hitsInfo()"); st = p.ev("()=>__HC.stage()"); cv0 = p.ev("()=>__HC.cv()")
        kk = 5 if hi and hi['n'] > 5 else 0
        at = p.ev("k=>__HC.hitRowAt(k)", kk); p.click(at, 450)
        cv1 = p.ev("()=>__HC.cv()"); m = p.ev("()=>__HC.markCur()"); hi2 = p.ev("()=>__HC.hitsInfo()")
        L = max(0, min(st['w'] - 80, hi['rect']['r'] - st['x'] + 16)) if hi and hi['n'] else 0
        tx, ty = st['x'] + L + (st['w'] - L) / 2, st['y'] + st['h'] / 2
        ok_pos = bool(m) and ((near(m['cx'], tx, 60) and near(m['cy'], ty, 60)) or (m['cx'] > st['x'] + L and m['cx'] < st['r'] and m['cy'] > st['y'] and m['cy'] < st['b'] and not m['underList']))
        T(g, 'C10t 목록 %d번째 줄 touchscreen.tap → vz 2 · 찾은 글자 가운데 · 그 줄 .cur(헛잣대: 바탕 무변)' % (kk + 1),
          bool(at and at.get('on')) and near(cv1['vz'], 2, 0.01) and ok_pos and (hi2 or {}).get('cur') == [kk], {'vz': [cv0['vz'], cv1['vz']], 'mark': m and [m['cx'], m['cy']], 'target': [round(tx), round(ty)], 'cur': (hi2 or {}).get('cur')})
        # Dt — 정리 결과 팝업: 줄 톡 → 팝업 · 두 손가락 벌리기 = 확대
        p.ev("()=>__HC.boot('jo')")
        p.sk_open(['omr'], ['민사소송법'], Q_MS)
        at = p.ev("([p,i])=>__HC.skRowAt(p,i)", ['📖 정리', 5])
        p.click(at, 300)
        s0 = p.until("()=>{const s=__HC.sf();return s.n&&s.cvpg?s:null}", None, 20000) or p.ev("()=>__HC.sf()")
        if s0.get('n'):
            v = s0['vr']; p.pinch(v['cx'], v['cy'], 60, 180)
            s1 = p.ev("()=>__HC.sf()")
            T(g, 'Dt 정리 줄 touchscreen.tap → 팝업 1 · 두 손가락 벌리기 = 쪽 확대(배율 ↑)', s1['n'] == 1 and s1['s'] > s0['s'] * 1.8, {'s': [s0['s'], s1['s']], 'n': s1['n']})
        else:
            T(g, 'Dt 정리 줄 touchscreen.tap → 팝업 — 안 떴다(바탕이면 헛잣대 그대로)', False, {'at': at and at.get('at')})
        er = p.errs_all()
        T(g, 'Z 페이지 오류 0', not er, er[:6])
    except Exception as ex:
        T(g, '묶음 예외', False, repr(ex)[:400])
    finally:
        p.close()


def ground():
    names = list(json.load(open(os.path.join(DATA, 'note_민소.json'), encoding='utf-8')))
    num = lambda f: (lambda m: [int(x) for x in m.group(1).split('.') if x] if m else None)(re.match(r'^(\d+(?:\.\d+)*)', f))
    nums = {f: num(f) for f in names}
    leaf = {f for f in names if not nums[f] or not any(g != f and b and len(b) > len(nums[f]) and b[:len(nums[f])] == nums[f] for g, b in nums.items())}
    notes5 = [next(f for f in names if f.startswith(pre)) for pre in PRE5]
    meta = json.load(open(os.path.join(DATA, 'omr', '민소', 'canvas_meta.json'), encoding='utf-8'))
    om = json.load(open(os.path.join(DATA, 'omr', '특허', 'omr_meta.json'), encoding='utf-8'))
    tiles = {k: v.get('300') for k, v in (om.get('tiles') or {}).items()}
    return {'names': names, 'leaf': sorted(leaf), 'notes5': notes5, 'hash': meta.get('hash'), 'tiles': tiles}


def report(t0, newf, basef, newmd5, bmd5, G):
    lines = ['# _harness_jo_cvfind — %s' % time.strftime('%Y-%m-%d %H:%M'),
             'NEW = %s (md5(LF) %s) · BASE = %s (md5(LF) %s) · 데이터 = genie jo/data (canvas_meta hash %s)' % (newf, newmd5, basef, bmd5, G['hash']),
             '누름 = page.mouse.click · page.touchscreen.tap · CDP 터치 끌기(el.click·dispatchEvent 없음) · 보임 = display ≠ none 그리고 높이 > 0', '']
    for grp, name, ok, d in RES:
        dd = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)
        lines.append('%s | %s · %s | %s' % ('NOTE' if ok is None else 'PASS' if ok else 'FAIL', grp, name, dd[:700]))
    new = [x for x in RES if x[2] is not None and not x[0].startswith('BASE')]
    base = [x for x in RES if x[2] is not None and x[0].startswith('BASE')]
    np_, nf = sum(1 for x in new if x[2]), sum(1 for x in new if not x[2])
    bp, bf = sum(1 for x in base if x[2]), sum(1 for x in base if not x[2])
    lines += ['', '헛잣대(BASE) — PASS %d · FAIL %d (새 기능 잣대는 FAIL 이어야 잣대 — 페이지 오류·손값 없는 줄 같은 무변 잣대는 PASS)' % (bp, bf),
              '합계(NEW)  PASS %d · FAIL %d  (%.0f초)' % (np_, nf, time.time() - t0)]
    txt = '\n'.join(lines) + '\n'
    f = os.path.join(OUT, '_harness_jo_cvfind_result.txt')
    for _ in range(3):
        io.open(f, 'w', encoding='utf-8', newline='\n').write(txt); time.sleep(0.5)
        if io.open(f, encoding='utf-8').read() == txt:
            break
    print('\n'.join(lines[-3:]))
    return nf


def main():
    t0 = time.time()
    os.makedirs(WORK, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    new = io.open(NEWF, encoding='utf-8').read()
    newmd5 = hashlib.md5(new.replace('\r\n', '\n').encode('utf-8')).hexdigest()
    base = io.open(BASEF, encoding='utf-8').read() if BASEF else git('show', BASE_REV + ':jo/index.html').decode('utf-8')
    bmd5 = hashlib.md5(base.replace('\r\n', '\n').encode('utf-8')).hexdigest()
    G = ground()
    print('땅값', {'hash': G['hash'], 'notes': len(G['names']), 'leaf': len(G['leaf']), 'notes5': G['notes5']}, flush=True)
    T('땅값', 'BASE = 이 판 바로 앞(905169d · 9bc75cae)', bmd5 == BASE_MD5, bmd5)
    T('땅값', '손값 넣을 다섯 = 모두 끝 목차', all(f in G['leaf'] for f in G['notes5']), G['notes5'])
    run = lambda x: not ONLY or x in ONLY
    with sync_playwright() as pw:
        cr = pw.chromium.launch()
        if run('base'):
            scen_desk(cr, base, 'BASE', G)
        if run('desk'):
            scen_desk(cr, new, 'NEW', G)
        if run('base'):
            scen_touch(cr, base, 'BASE', G)
        if run('touch'):
            scen_touch(cr, new, 'NEW', G)
        cr.close()
    g = 'NEW 책상'
    nx = KEEP.get('namex', {})
    if 'BASE' in nx and 'NEW' in nx:
        d = sorted({round(nx['NEW'][f] - nx['BASE'][f], 2) for f in nx['NEW'] if f in nx['BASE']})
        T(g, 'A1c 이름 줄 x = 바탕 그대로(모든 줄 · 토글은 절대 자리)', d == [0.0] and len(nx['NEW']) == len(nx['BASE']), {'dx': d, 'rows': len(nx['NEW'])})
    ld = KEEP.get('lawdom', {})
    if 'BASE' in ld and 'NEW' in ld:
        T(g, 'A6 특허·상표·디보 목차노트 목록 DOM = 바탕', ld['NEW'] == ld['BASE'] and len(ld['NEW']) == 3, {'NEW': ld['NEW'], 'BASE': ld['BASE']})
    pt = KEEP.get('ptn', {})
    if 'BASE' in pt and 'NEW' in pt:
        T(g, 'B8c 특허만 「%s」 → 정리 수 = 바탕(지금 규칙 그대로)' % Q_PT, pt['NEW']['n'] == pt['BASE']['n'] and pt['NEW']['n'] is not None and pt['NEW']['rows'] == pt['BASE']['rows'],
          {'NEW': pt['NEW'], 'BASE': pt['BASE']})
    ot = KEEP.get('other', {})
    if 'BASE' in ot and 'NEW' in ot:
        T(g, 'D15 다른 범위(조문·판례) 첫 줄 누름 동작 = 바탕(탭·법·뜬 창·검색창)', ot['NEW'] == ot['BASE'], {'NEW': ot['NEW'], 'BASE': ot['BASE']})
    return report(t0, NEWF, BASEF or BASE_REV, newmd5, bmd5, G)


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
