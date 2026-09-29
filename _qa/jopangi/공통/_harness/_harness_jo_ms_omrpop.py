# -*- coding: utf-8 -*-
r"""_task_jo_ms_omrpop §D 관문 — A 목차노트 압정 · B 정리OMR 팝업 · B-4 영역 지정 손값 · C 📘 창 정리캔버스 줄 · 폰.

  NEW  = --new <파일>(없으면 genie 작업트리 jo/index.html) · BASE = --base <파일>(없으면 genie bd8cfdf — c2card 인도 판 · md5 c5210438)
  헛잣대 = BASE 에 같은 책상 시나리오를 먼저 돌린다 — 새 기능 잣대는 거기서 FAIL 이어야 잣대다
  데이터 = genie jo/data(canvas_meta hash 71e49579 · BASE·NEW 같은 데이터) · 교재 창 요청은 같은 출처 /__book/(canvas_jari 하네스 SEED 그대로)
  엔진 = chromium 책상 1440×900(마우스) · 폰 390×844(CDP 진짜 터치 — 한 손가락 · 두 손가락) · webkit 책상 · 폰(톡만 진짜 터치 · 끌기는 신뢰 마우스 — 도구 한계)
  잣대 = DOM 실물 · getBoundingClientRect · elementFromPoint · 창(POPS) · 저장소 값(localStorage jopangi.ncomr · 동기화 도장)
  땅값 = genie 데이터를 파이썬으로 따로 센다(끝 목차 · 노트 블록 = noteOf(bn 먼저 · 없으면 블록 파일 note) · 블록 자리)

쓰기 : python _harness_jo_ms_omrpop.py [--new 파일] [--base 파일] [--out 폴더] [--only desk,wk,phone,wkphone,base]
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
CJH = r'N:\개인\claude\jopangi\공통\_harness'
sys.path.insert(0, CJH)
import _harness_canvas_jari as CJ          # noqa: E402 — SEED(교재·기록 fetch 돌림) · VENDOR · route_filter
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


HERE = os.path.dirname(os.path.abspath(__file__))
OUT = ARG('--out', HERE)
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
SECS = [x for x in (ARG('--sec', '') or '').split(',') if x]   # 책상 묶음 고르기(A·B·P·C) — 없으면 전부
GENIE = CJ.GENIE
JOD = os.path.join(GENIE, 'jo')
DATA = os.path.join(JOD, 'data')
NEWF = ARG('--new', os.path.join(JOD, 'index.html'))
BASEF = ARG('--base', '')
BASE_REV, BASE_MD5 = 'bd8cfdf', 'c5210438b5083ee524135cbb7296420e'
HASH = '71e49579'
WORK = os.path.join(tempfile.gettempdir(), 'h_omrpop')
MB = _roots.mbpdf()
PDFD = r'N:\개인\claude\jopangi\민소\_pdf'
TESTS = io.open(os.path.join(HERE, '_harness_jo_ms_omrpop_tests.js'), encoding='utf-8').read()
PHONE_UA = ('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
READY = "!!window.__HO&&!!window.__HJ&&typeof render==='function'&&typeof viewCanvas==='function'"
N131 = '1.3.1.{법정}직사토(보독관)'
NJS = '9.==재심(451조)== 대기리당사보'
SERVERS = {}
RES = []


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


# ══════════ 땅값 — genie 데이터를 따로 센다 ══════════
def ground():
    O = os.path.join(DATA, 'omr', '민소')
    meta = json.load(open(os.path.join(O, 'canvas_meta.json'), encoding='utf-8'))
    M = json.load(open(os.path.join(O, 'canvas_match.json'), encoding='utf-8'))
    NT = json.load(open(os.path.join(DATA, 'note_민소.json'), encoding='utf-8'))
    bn = M.get('bn') or {}
    names = list(NT)
    num = lambda f: (lambda m: [int(x) for x in m.group(1).split('.') if x] if m else None)(re.match(r'^(\d+(?:\.\d+)*)', f))
    nums = {f: num(f) for f in names}
    leaf = {f for f in names if not nums[f] or not any(g != f and b and len(b) > len(nums[f]) and b[:len(nums[f])] == nums[f] for g, b in nums.items())}
    blk, by, by_bn = {}, {}, {}
    for p in meta['pages']:
        P = json.load(open(os.path.join(O, 'canvas_p%d.json' % p['n']), encoding='utf-8'))
        oy = P.get('oy', p.get('oy', 0))   # 앱 D.pages = 쪽 파일 — 그 oy
        for b in P['blocks']:
            if b.get('del') or b.get('k') == '헤딩':
                continue
            blk[b['bid']] = (p['n'], [b['x'], b['y'] - oy, b['x'] + b['w'], b['y'] - oy + b['h']])
            nm = bn[b['bid']] if b['bid'] in bn else b.get('note')
            if nm:
                by.setdefault(nm, []).append(b['bid'])
            if bn.get(b['bid']):
                by_bn.setdefault(bn[b['bid']], []).append(b['bid'])
    nc = json.load(open(os.path.join(O, 'note_canvas.json'), encoding='utf-8'))
    e35 = ((nc.get('p') or {}).get(N131) or {}).get('35') or {}
    return {'hash': meta.get('hash'), 'names': names, 'leaf': sorted(leaf), 'nonleaf': sorted(set(names) - leaf), 'by': by, 'by_bn': by_bn,
            'gray': sorted(f for f in leaf if not by.get(f)), 'gray_bn': sorted(f for f in leaf if not by_bn.get(f)), 'blk': blk, 'b35': e35.get('b') or [],
            'oyk': 'meta' if 'oy' in meta['pages'][0] else 'page'}


def serve(tag, src):
    if tag in SERVERS:
        return SERVERS[tag][1]
    out = os.path.join(WORK, 'srv_' + tag); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    src = src.replace('\r\n', '\n')
    b = src.index('<body'); bb = src.index('>', b) + 1
    html = src[:bb] + CJ.SEED + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + CJ.TESTS + '\n</script>\n<script>\n' + TESTS + '\n</script>\n' + html[e:]   # __HJ(동기화 도구) + __HO
    io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=out, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            if p.startswith('/__vendor/'):
                return os.path.join(CJ.VENDOR, p[len('/__vendor/'):].replace('/', os.sep))
            if p.startswith('/__book/words/'):
                return os.path.join(MB, 'words', p[len('/__book/words/'):].replace('/', os.sep))
            if p.startswith('/__book/stamp/'):
                return os.path.join(MB, 'stamp', p[len('/__book/stamp/'):].replace('/', os.sep))
            if p.startswith('/__book/pdf/'):
                return os.path.join(PDFD, p[len('/__book/pdf/'):])
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
    def __init__(self, br, eng, tag, src, W, H, phone=False, q='tok=1', who='꼬까'):
        self.eng, self.tag, self.phone, self.who = eng, tag, phone, who
        self.port = serve(tag, src)
        if phone:
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=PHONE_UA)
        else:
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1)
        self.ctx.route('**/*', CJ.route_filter)
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(180000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' else None)
        self.cdp = self.ctx.new_cdp_session(self.pg) if (eng == 'chromium' and phone) else None
        self.load(q)

    def load(self, q):
        self.pg.goto('http://127.0.0.1:%d/index.html?%s&who=%s' % (self.port, q, urllib.parse.quote(self.who)), wait_until='load', timeout=180000)
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
        if not at or not at.get('on'):
            return False
        if self.phone:
            self.pg.touchscreen.tap(at['cx'], at['cy'])
        else:
            self.pg.mouse.click(at['cx'], at['cy'])
        self.pg.wait_for_timeout(wait)
        return True

    def touch(self, frames, dt=16):
        """CDP 진짜 터치 — frames = [[(x,y),…], …] 한 장면마다 손가락 자리(id = 차례)"""
        def send(ty, pts):
            self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': [{'x': x, 'y': y, 'id': i + 1} for i, (x, y) in enumerate(pts)]})
        send('touchStart', frames[0])
        for f in frames[1:]:
            send('touchMove', f); self.pg.wait_for_timeout(dt)
        for _ in range(3):
            send('touchMove', frames[-1]); self.pg.wait_for_timeout(30)
        send('touchEnd', [])
        self.pg.wait_for_timeout(250)

    def drag(self, x0, y0, x1, y1, n=14):
        if self.cdp:
            self.touch([[(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n)] for i in range(n + 1)])
            return 'cdp-touch'
        m = self.pg.mouse
        m.move(x0, y0); m.down()
        for i in range(1, n + 1):
            m.move(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.pg.wait_for_timeout(16)
        m.up(); self.pg.wait_for_timeout(250)
        return 'mouse(trusted)'

    def shot(self, name):
        d = os.path.join(OUT, '_omrpop_shots'); os.makedirs(d, exist_ok=True)
        f = os.path.join(d, name + '.png')
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

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


def near(a, b, tol):
    return a is not None and b is not None and abs(a - b) <= tol


def pin_at(p, note):
    """목록 창 압정 자리 — 다른 팝업에 가려 있으면 목록 창을 앞으로(사람도 목록 창을 눌러 올린다)"""
    at = p.ev("n=>__HO.pinAt(n)", note)
    if at and not at.get('on'):
        p.ev("()=>{const w=document.querySelector('.pop.mkpop');if(w){w.style.zIndex=++POPZ;popAllSync();}}")
        at = p.ev("n=>__HO.pinAt(n)", note)
    return at


def pin_open(p, note, grp):
    """목록에서 그 노트 압정을 눌러 팝업을 연다 — 팝업 상태(없으면 None)"""
    at = pin_at(p, note)
    if not p.click(at, 300):
        return None, at
    k = 'note|' + note
    o = p.until("k=>{const o=__HO.omr(k);return o&&o.cvpg!==undefined&&o.p?o:null}", k, 60000)
    p.pg.wait_for_timeout(300)
    return p.ev("k=>__HO.omr(k)", k), at


# ══════════ 책상(마우스) ══════════
def scen_desk(br, eng, src, tag, G, keepA=None):
    g = '%s %s 책상' % (tag, eng)
    p = Pg(br, eng, tag, src, 1440, 900)
    k = 'note|' + N131

    def sec(name, fn):   # 묶음마다 따로 — 앞 묶음이 깨져도(바탕 판 · 헛잣대) 뒤 묶음을 잰다
        try:
            fn()
        except Exception as ex:
            T(g, name + ' 묶음 예외', False, repr(ex)[:400])

    def secA():
        for n in range(1, 12):
            p.ev("n=>__HO.inkSeed(n)", n)   # 필기 픽스처(쪽마다 획 하나) — D 를 짓기 전에
        p.ev("()=>__HO.boot('jo')")
        L = p.ev("async()=>{await __HO.mokOpen();return await __HO.listPainted(90000)}")
        if keepA is not None:
            keepA[tag + eng] = L
        rows = (L or {}).get('rows') or []
        pins = [r for r in rows if r['pin'] == 'pin']; gaps = [r for r in rows if r['pin'] == 'gap']
        T(g, 'A1 압정 수 = 끝 목차 수 · 빈자리 = 나머지(목록을 그릴 때 센다)', len(rows) == len(G['names']) and len(pins) == len(G['leaf']) and len(gaps) == len(G['nonleaf'])
          and sorted(r['note'] for r in pins) == G['leaf'] and all(r['first'] for r in pins + gaps),
          {'rows': len(rows), 'pins': len(pins), 'gaps': len(gaps), 'leaf': len(G['leaf']), 'nonleaf': len(G['nonleaf'])})
        byn = {r['note']: r for r in rows}
        want_pin = [f for f in G['names'] if f.startswith(('1.3.1.', '2.3. ', '9.==재심'))]
        want_gap = [f for f in G['names'] if f.startswith(('1.3. ', '2.2. ', '1.==소송주체'))]
        T(g, 'A2 1.3.1 · 2.3. · 9.==재심== 에 압정 · 1.3. · 2.2. · 1.==소송주체== 에는 빈자리',
          len(want_pin) == 3 and len(want_gap) == 3 and all((byn.get(f) or {}).get('pin') == 'pin' for f in want_pin) and all((byn.get(f) or {}).get('pin') == 'gap' for f in want_gap),
          {f: (byn.get(f) or {}).get('pin') for f in want_pin + want_gap})
        gapx = [round(r['nr']['x'] - r['pr']['r'], 2) for r in pins if r['pr'] and r['nr']]
        T(g, 'A3 압정 ↔ 이름 가로 틈 3px(±1) — 모든 압정 줄', bool(gapx) and all(near(x, 3, 1) for x in gapx), {'min': min(gapx) if gapx else None, 'max': max(gapx) if gapx else None})
        svg = pins[0] if pins else {}
        blank = [r for r in pins if r['note'] not in G['gray']]
        T(g, 'A4 꼴 — SVG 11×11 · #111 · 테두리만(속 none) · 빈자리 = visibility:hidden 같은 폭',
          bool(pins) and near(svg.get('svgW'), 11, 0.5) and near(svg.get('svgH'), 11, 0.5) and all(r['color'] == 'rgb(17, 17, 17)' and r['fill'] == 'none' for r in blank)
          and bool(gaps) and all(r['vis'] == 'hidden' and near(r['pr']['w'], pins[0]['pr']['w'], 0.1) for r in gaps),
          {'svg': [svg.get('svgW'), svg.get('svgH')], 'color': sorted({r['color'] for r in blank}), 'fill': sorted({r['fill'] for r in blank}), 'gapVis': sorted({r['vis'] for r in gaps})})
        grey = sorted(r['note'] for r in pins if 'mkoff' in (r['cls'] or ''))
        T(g, 'A5 블록 없는 노트 = 옅은 회색 #c4bfb5 (noteOf 로 센 것과 같음)', bool(pins) and grey == G['gray'] and all(byn[f]['color'] == 'rgb(196, 191, 181)' for f in grey),
          {'grey': grey, 'ground': G['gray'], 'ground_bn만': G['gray_bn']})
        tt = (byn.get(N131) or {}).get('title') or ''
        T(g, 'A6 압정 title = 이 노트 블록 N개(noteOf) · role=button', ('블록 %d개' % len(G['by'].get(N131, []))) in tt and (byn.get(N131) or {}).get('role') == 'button', tt)
        at = p.ev("n=>__HO.pinAt(n)", N131)
        if at and at.get('on'):
            p.pg.mouse.move(at['cx'], at['cy']); p.pg.wait_for_timeout(200)
            hc = p.ev("n=>__HO.pinColor(n)", N131); p.pg.mouse.move(5, 5); p.pg.wait_for_timeout(100)
        else:
            hc = None
        T(g, 'A7 마우스를 올리면 청록 #0f766e', hc == 'rgb(15, 118, 110)', hc)

    def secB():
        # ── B ── 1.3.1 압정 → 팝업
        tab0 = p.ev("()=>S.tab")
        o, at = pin_open(p, N131, g)
        k = 'note|' + N131
        bids = G['by'].get(N131, [])
        onp = [b for b in bids if o and G['blk'].get(b, (0,))[0] == o.get('p')]
        pk = p.ev("()=>__HO.pk()")
        T(g, 'B1 1.3.1 압정 → 팝업 1개 · 노랑 상자 수 = 그 쪽 노트 블록 수 · 정리 탭으로 안 넘어감 · 노트 팝업 안 뜸',
          bool(o) and p.ev("()=>__HO.omrKeys().length") == 1 and o['auto'] == len(onp) and len(onp) > 0 and p.ev("()=>S.tab") == tab0
          and not any((x or '').startswith('note|') for x in pk) and sorted(o['boxesK']) == sorted(bids),
          {'auto': o and o['auto'], 'onPage': len(onp), 'p': o and o['p'], 'bids': len(bids), 'tab': [tab0, p.ev("()=>S.tab")], 'pops': pk})
        if not o:
            return
        T(g, 'B1b 머리 「▦ 정리OMR · 노트」 · 배율 글자·−/+·맞춤 단추 없음 · 도구 줄 = 쪽 단추 · ‹ › · ▭ 영역 지정',
          o['title'] == '▦ 정리OMR · ' + N131 and o['zoomUi'] == 0 and o['nav'] == 2 and o['pickTxt'] == '▭ 영역 지정' and o['pgs'] and all(re.match(r'^\d+쪽\*?$', x) for x in o['pgs']),
          {'title': o['title'], 'bar': o['barBtns'], 'pgs': o['pgs']})
        b0 = next((b for b in bids if G['blk'][b][0] == o['p']), None)
        exp = None
        if b0:
            r = G['blk'][b0][1]
            s0 = p.ev("([k,x,y])=>__HO.scr(k,x,y)", [k, r[0] - 1.5, r[1] - 1.5]); s1 = p.ev("([k,x,y])=>__HO.scr(k,x,y)", [k, r[2] + 1.5, r[3] + 1.5])
            exp = [round(s0['x'], 1), round(s0['y'], 1), round(s1['x'] - s0['x'], 1), round(s1['y'] - s0['y'], 1)]
        hit = [a for a in o['autoR'] if exp and near(a['x'], exp[0], 1.5) and near(a['y'], exp[1], 1.5) and near(a['w'], exp[2], 1.5) and near(a['h'], exp[3], 1.5)]
        T(g, 'B1c 노랑 상자 = 블록 자리 ±1.5pt(땅값 블록 좌표로 잰 화면 자리) · 색 rgba(250,204,21,.28) / #eab308',
          bool(hit) and o['autoBg'] == 'rgba(250, 204, 21, 0.28)' and o['autoOl'] == 'rgb(234, 179, 8)', {'exp': exp, 'first': o['autoR'][:1], 'bg': o['autoBg'], 'ol': o['autoOl']})
        T(g, 'B1d 쪽을 따로 지음(쪽 1 · top 0 · 줄 있음) · 필기 획 같이 · 누름 안 받음(pointer-events none · 상자 위 맨 위 = 겹)',
          o['cvpg'] == 1 and o['pgTop'] == '0px' and o['ln'] > 50 and o['ink'] >= 1 and o['pe'] == 'none' and p.ev("k=>__HO.autoTop(k)", k) == 'opov'
          and p.ev("()=>__HO.stage().worldPg") == 0,
          {'cvpg': o['cvpg'], 'top': o['pgTop'], 'ln': o['ln'], 'ink': o['ink'], 'pe': o['pe'], 'top@box': p.ev("k=>__HO.autoTop(k)", k), 'worldPg': p.ev("()=>__HO.stage().worldPg")})
        vr = o['vr']
        inside = all(a['x'] >= vr['x'] - 1 and a['r'] <= vr['r'] + 1 and a['y'] >= vr['y'] - 1 and a['b'] <= vr['b'] + 1 for a in o['autoR'])
        T(g, 'B1e 처음 = 목표 자리가 보이게 맞춤(노랑 상자 모두 보기 칸 안 · 배율 ≤ 1)', inside and o['s'] <= 1, {'s': o['s'], 'vr': vr, 'n': len(o['autoR'])})
        T(g, 'B1f 첫 크기 = 폭 min(640, 화면−24) · 높이 min(화면×0.78, 720) · 화면 안', near(o['rect']['w'], 640, 2) and near(o['rect']['h'], 702, 2)
          and o['rect']['x'] >= 0 and o['rect']['r'] <= 1440 and o['rect']['y'] >= 0 and o['rect']['b'] <= 900, o['rect'])
        # 휠
        v = p.ev("k=>__HO.vpt(k,.5,.5)", k)
        p.pg.mouse.move(v['x'], v['y']); p.pg.wait_for_timeout(100)
        p.pg.mouse.wheel(0, -120); p.pg.wait_for_timeout(400)
        o2 = p.ev("k=>__HO.omr(k)", k); s2 = p.ev("([k,x,y])=>__HO.scr(k,x,y)", [k, v['px'], v['py']])
        T(g, 'B2 휠 한 번(Ctrl 없이) → 배율 바뀜 · 마우스 밑 쪽 좌표가 2px 안에서 그대로', o2['s'] > o['s'] * 1.1 and near(s2['x'], v['x'], 2) and near(s2['y'], v['y'], 2),
          {'s': [round(o['s'], 4), round(o2['s'], 4)], 'at': [v['x'], v['y']], 'after': [round(s2['x'], 2), round(s2['y'], 2)]})
        e = p.ev("k=>__HO.emptyAt(k)", k)
        how = p.drag(e['x'], e['y'], e['x'] - 90, e['y'] - 70) if e else None
        o3 = p.ev("k=>__HO.omr(k)", k)
        T(g, 'B3 끌기 → 스크롤만 바뀜(배율 무변)', bool(e) and o3['s'] == o2['s'] and near(o3['sl'] - o2['sl'], 90, 4) and near(o3['stp'] - o2['stp'], 70, 4),
          {'how': how, 'd': [o3['sl'] - o2['sl'], o3['stp'] - o2['stp']], 's': o3['s']})
        pinch_n = None
        p.shot('%s_%s_desk_popup' % (tag, eng))
        # 같은 압정 또 → 닫힘
        p.click(pin_at(p, N131), 600)
        T(g, 'B4 같은 압정을 또 누르면 닫힌다(조판기 규칙)', p.ev("()=>__HO.omrKeys().length") == 0, p.ev("()=>__HO.omrKeys()"))
        # 뒤 무대 무변 — 정리 탭 위에서
        st0 = p.ev("async()=>await __HO.canvasBoot()")
        p.ev("async()=>await __HO.mokOpen()"); p.ev("async()=>await __HO.listPainted(60000)")
        o, _ = pin_open(p, N131, g)
        tr0 = p.ev("()=>__HO.stage().tr")
        if o:
            v = p.ev("k=>__HO.vpt(k,.5,.5)", k)
            p.pg.mouse.move(v['x'], v['y']); p.pg.mouse.wheel(0, 200); p.pg.wait_for_timeout(300); p.pg.mouse.wheel(0, -300); p.pg.wait_for_timeout(400)
        st1 = p.ev("()=>__HO.stage()")
        T(g, 'B5 팝업 안 휠에 뒤 무대(정리 탭) transform 무변 · 탭 그대로', bool(o) and st0['stage'] and st1['tr'] == tr0 and st1['tab'] == 'omr',
          {'tr': [tr0, st1['tr']], 'tab': st1['tab']})
        p.ev("()=>{try{closeAllPops()}catch(e){}}")

    def secP():
        # ── B-4 영역 지정 ──
        p.ev("()=>__HO.boot('jo')"); p.ev("async()=>await __HO.mokOpen()"); p.ev("async()=>await __HO.listPainted(60000)")
        o, _ = pin_open(p, N131, g)
        p.click(p.ev("k=>__HO.omrAt(k,'pick')", k), 300)
        o = p.ev("k=>__HO.omr(k)", k)
        T(g, 'P0 ▭ 영역 지정 켜짐 — 발 줄 안내 · 확정 단추는 네모가 생긴 뒤에', bool(o) and o['pick'] and o['pickOn'] and not o['ok'] and '쪽 위를 끌어 네모' in o['msg'], o and o['msg'])
        e = p.ev("k=>__HO.emptyAt(k)", k)
        if e:
            p.drag(e['x'], e['y'], e['x'] + 3, e['y'] + 2, 4)
        o = p.ev("k=>__HO.omr(k)", k)
        T(g, 'P6 너무 작은 네모(폭 < 6pt · 높이 < 4pt)는 버림', bool(o) and o['box'] is None and not o['ok'], o and o['box'])
        a = p.ev("k=>__HO.vpt(k,.30,.32)", k); b = p.ev("k=>__HO.vpt(k,.62,.58)", k)
        p.drag(a['x'], a['y'], b['x'], b['y'])
        o = p.ev("k=>__HO.omr(k)", k)
        T(g, 'P1a 끌기 → 네모(청록 점선) · 「이 자리로 확정」·「다시」 보임', bool(o) and o['box'] and o['tmp'] == 1 and o['ok'] and o['cancel'] and o['tmpOl'] == 'dashed',
          {'box': o and o['box'], 'ft': o and o['ftBtns']})
        p.click(p.ev("k=>__HO.omrAt(k,'ok')", k), 500)
        o = p.ev("k=>__HO.omr(k)", k); V = (p.ev("()=>__HO.ls()") or {}).get(k)
        L2 = p.ev("()=>__HO.list()"); r131 = next((r for r in (L2 or {}).get('rows', []) if r['note'] == N131), {})
        ok_shape = bool(V) and set(V) == {'p', 'r', 'h', 't', 'who'} and V['h'] == HASH and len(V['r']) == 4 and V['r'][2] - V['r'][0] >= 6 and V['who'] == '꼬까PC'
        exp_r = [round(a['px'], 1), round(a['py'], 1), round(b['px'], 1), round(b['py'], 1)]
        T(g, 'P1 확정 → jopangi.ncomr 칸 1 = {p, r(쪽 기준 pt), h, t, who} · 목록 압정 속 채움',
          ok_shape and all(near(V['r'][i], exp_r[i], 1.0) for i in range(4)) and len(p.ev("()=>__HO.ls()") or {}) == 1 and 'mkpin' in (r131.get('cls') or '') and r131.get('fill') == 'rgb(17, 17, 17)',
          {'v': V, 'exp_r': exp_r, 'cls': r131.get('cls'), 'fill': r131.get('fill')})
        T(g, 'P1b 팝업 = 주황 손값 상자 1 · 자동 상자 0 · 쪽 단추 「N쪽 📌」 · 발 줄 「📌 손값」 · 되돌리기 보임',
          bool(o) and o['pin'] == 1 and o['auto'] == 0 and any(x.startswith('%d쪽 📌' % V['p']) for x in o['pgs']) and o['msg'].startswith('📌 손값') and o['rv']
          and o['pinBg'] == 'rgba(249, 115, 22, 0.14)' and o['pinOl'] == 'rgb(249, 115, 22)', {'pgs': o and o['pgs'], 'msg': o and o['msg']})
        u = p.ev("()=>__HO.u()")
        T(g, 'P7 동기화 — SYNC_KEYS 에 jopangi.ncomr · 이름 · 도장 u[jopangi.ncomr|note|…]', 'jopangi.ncomr' in (p.ev("()=>__HO.syncKeys()") or [])
          and bool(p.ev("()=>__HO.recName()")) and ('jopangi.ncomr|' + k) in u, {'u': u, 'name': p.ev("()=>__HO.recName()"), 'n': len(p.ev("()=>__HO.syncKeys()") or [])})
        p.shot('%s_%s_desk_pin' % (tag, eng))
        # 새로고침 뒤 그대로
        p.load('tok=1&keep=1'); p.ev("()=>__HO.boot('jo')")
        L3 = p.ev("async()=>{await __HO.mokOpen();return await __HO.listPainted(90000)}")
        r131 = next((r for r in (L3 or {}).get('rows', []) if r['note'] == N131), {})
        o, _ = pin_open(p, N131, g)
        T(g, 'P2 새로고침 뒤 그대로 — 압정 채움 · 팝업 = 손값 쪽 · 주황 상자', 'mkpin' in (r131.get('cls') or '') and bool(o) and o['pin'] == 1 and o['auto'] == 0 and o['p'] == V['p'],
          {'cls': r131.get('cls'), 'pin': o and o['pin'], 'p': o and o['p']})
        p.click(p.ev("k=>__HO.omrAt(k,'rv')", k), 500)
        o = p.ev("k=>__HO.omr(k)", k); V2 = (p.ev("()=>__HO.ls()") or {}).get(k)
        L4 = p.ev("()=>__HO.list()"); r131 = next((r for r in (L4 or {}).get('rows', []) if r['note'] == N131), {})
        T(g, 'P3 「자동으로 되돌리기」 → {auto:true, t}(칸은 남김) · 압정 빈 속 · 팝업 = 자동 상자',
          bool(V2) and V2.get('auto') is True and set(V2) == {'auto', 't'} and 'mkpin' not in (r131.get('cls') or '') and r131.get('fill') == 'none' and bool(o) and o['pin'] == 0 and o['auto'] > 0,
          {'v': V2, 'cls': r131.get('cls'), 'auto': o and o['auto']})
        # 판이 바뀐 손값
        nb = G['by'].get(NJS, [])
        pj = G['blk'][nb[0]][0] if nb else 1
        cur = p.ev("()=>__HO.ls()") or {}
        cur['note|' + NJS] = {'p': pj, 'r': [100, 100, 400, 300], 'h': 'deadbeef', 't': 1, 'who': '헛값'}
        p.ev("v=>__HO.lsSet(v)", cur)
        p.ev("()=>{try{closeAllPops()}catch(e){}}")
        p.ev("async()=>await __HO.mokOpen()"); L5 = p.ev("async()=>await __HO.listPainted(60000)")
        o, _ = pin_open(p, NJS, g)
        T(g, 'P5 h 가 다른 손값 → 네모는 그리되 발 줄 「판이 바뀜 — 다시 찍어 주세요」', bool(o) and o['pin'] == 1 and '판이 바뀜 — 다시 찍어 주세요' in o['msg'], o and o['msg'])
        p.ev("()=>{try{closeAllPops()}catch(e){}}")

    def secC():
        # ── C 📘 창 ──
        p.ev("()=>__HO.boot('jo')")
        p.ev("f=>__HO.note(f)", N131); p.ev("([f,e])=>__HO.ncbOpen(f,e)", [N131, 35])
        c = p.ev("([f,e])=>__HO.ncbWait(f,e,60000)", [N131, 35])
        pairs = [x['bid'] for x in (c or {}).get('pair', [])]
        T(g, 'C0 1.3.1 문단 35 📘 → 정리캔버스 칸 = 짝 블록 셋(1L108·1L112·1L131)', pairs == G['b35'] == ['1L108', '1L112', '1L131'], {'pairs': pairs, 'ground': G['b35']})
        kp = 'para|%s|35' % N131
        tab0 = p.ev("()=>S.tab")
        p.click(p.ev("([f,e,b])=>__HO.ncbAt(f,e,'bid',b)", [N131, 35, '1L112']), 400)
        o = p.until("k=>{const o=__HO.omr(k);return o&&o.p?o:null}", kp, 60000)
        r = G['blk']['1L112'][1]
        exp = None
        if o:
            s0 = p.ev("([k,x,y])=>__HO.scr(k,x,y)", [kp, r[0] - 1.5, r[1] - 1.5]); exp = [round(s0['x'], 1), round(s0['y'], 1)]
        T(g, 'C1 정리캔버스 1L112 줄 → 팝업(노랑 = 1L112 자리) · 📘 창은 그대로 · 정리 탭으로 안 넘어감',
          bool(o) and o['bids'] == ['1L112'] and o['auto'] == 1 and near(o['autoR'][0]['x'], exp[0], 1.5) and near(o['autoR'][0]['y'], exp[1], 1.5)
          and bool(p.ev("([f,e])=>__HO.ncb(f,e)", [N131, 35])) and p.ev("()=>S.tab") == tab0 and o['title'].endswith('· 블록 1L112'),
          {'bids': o and o['bids'], 'auto': o and o['autoR'][:1], 'exp': exp, 'title': o and o['title'], 'tab': p.ev("()=>S.tab")})
        p.shot('%s_%s_desk_ncb' % (tag, eng))
        # 📘 창이 팝업에 가려 있으면 창 머리를 눌러 올린다(사람도 그렇게 한다)
        def ncb_click(what, i=None):
            at = p.ev("([f,e,w,i])=>__HO.ncbAt(f,e,w,i)", [N131, 35, what, i])
            if at and not at.get('on'):
                p.ev("pk=>{const w=POPS.find(x=>x._pk===pk);if(w){w.style.zIndex=++POPZ;popAllSync();}}", 'ncbook|민소|%s|35' % N131)
                at = p.ev("([f,e,w,i])=>__HO.ncbAt(f,e,w,i)", [N131, 35, what, i])
            return p.click(at, 500)
        ncb_click('bid', '1L131')
        o = p.until("k=>{const o=__HO.omr(k);return o&&o.bids&&o.bids[0]==='1L131'?o:null}", kp, 20000)
        n_same = len([x for x in p.ev("()=>__HO.omrKeys()") if x == 'cv|omr|' + kp])
        T(g, 'C2a 1L131 줄 → 같은 창이 그 자리로(창 1 · 목표 1L131 · 제목 바뀜)', bool(o) and n_same == 1 and o['bids'] == ['1L131'] and o['title'].endswith('· 블록 1L131') and o['auto'] == 1,
          {'n': n_same, 'bids': o and o['bids'], 'title': o and o['title']})
        ncb_click('bid', '1L131')
        T(g, 'C2b 1L131 줄 또 → 닫힘', p.ev("k=>!__HO.omr(k)", kp), p.ev("()=>__HO.omrKeys()"))
        # 손값 → 📘 창 칸
        ncb_click('bid', '1L112')
        o = p.until("k=>{const o=__HO.omr(k);return o&&o.p?o:null}", kp, 20000)
        p.click(p.ev("k=>__HO.omrAt(k,'pick')", kp), 300)
        a = p.ev("k=>__HO.vpt(k,.35,.35)", kp); b = p.ev("k=>__HO.vpt(k,.6,.6)", kp)
        p.drag(a['x'], a['y'], b['x'], b['y'])
        p.click(p.ev("k=>__HO.omrAt(k,'ok')", kp), 600)
        c = p.until("([f,e])=>{const c=__HO.ncb(f,e);return c&&c.ncpin&&c.ncpin.length?c:null}", [N131, 35], 20000)
        V = (p.ev("()=>__HO.ls()") or {}).get(kp)
        T(g, 'C3 손값 → 📘 창 칸 = 「정리 N쪽 · 찍어 둔 자리 📌」 한 줄 + 「영역 지정으로 찍은 자리 — 누르면 그 자리」 + 되돌리기 · 짝 줄 숨김',
          bool(c) and bool(V) and c['pair'] == [] and len(c['ncpin']) == 1 and c['ncpin'][0]['k'] == '정리' and c['ncpin'][0]['p'] == '%d쪽' % V['p']
          and c['ncpin'][0]['m'] == '찍어 둔 자리 📌' and c['ncpin'][0]['sn'] == '영역 지정으로 찍은 자리 — 누르면 그 자리' and '자동으로 되돌리기' in c['more']
          and c['ncpin'][0]['mColor'] == 'rgb(180, 83, 9)', {'c': c and {x: c[x] for x in ('pair', 'ncpin', 'more')}, 'v': V})
        p.ev("k=>{const w=POPS.find(x=>x._pk==='cv|omr|'+k);if(w)closeOne(w)}", kp)
        ncb_click('ncpin')
        o = p.until("k=>{const o=__HO.omr(k);return o&&o.p?o:null}", kp, 20000)
        T(g, 'C4 그 줄을 누르면 팝업(목표 = 짝 블록 전부 · 손값 네모)', bool(o) and o['bids'] == ['1L108', '1L112', '1L131'] and o['pin'] == 1 and o['auto'] == 0,
          {'bids': o and o['bids'], 'pin': o and o['pin']})
        p.ev("k=>{const w=POPS.find(x=>x._pk==='cv|omr|'+k);if(w)closeOne(w)}", kp)
        ncb_click('rv')
        c = p.until("([f,e])=>{const c=__HO.ncb(f,e);return c&&c.pair&&c.pair.length?c:null}", [N131, 35], 20000)
        V = (p.ev("()=>__HO.ls()") or {}).get(kp)
        T(g, 'C5 📘 창 「자동으로 되돌리기」 → 짝 줄 셋 돌아옴 · 칸 = {auto:true}', bool(c) and [x['bid'] for x in c['pair']] == ['1L108', '1L112', '1L131'] and not c['ncpin'] and bool(V) and V.get('auto') is True,
          {'pair': c and [x['bid'] for x in c['pair']], 'v': V})

    try:
        for nm, fn in (('A', secA), ('B', secB), ('P', secP), ('C', secC)):
            if not SECS or nm in SECS:
                sec(nm, fn)
        er = [x for x in p.errs + (p.ev("()=>__HO.errs()") or []) if not CJ.NOISE(x)]
        T(g, 'Z 페이지 오류 0(ResizeObserver loop · 자원 못 받음 잡음 빼고)', not er, er[:6])
    finally:
        p.close()


# ══════════ 폰(진짜 터치) ══════════
def scen_phone(br, eng, src, tag, G):
    g = '%s %s 폰 390' % (tag, eng)
    p = Pg(br, eng, tag, src, 390, 844, phone=True)
    try:
        p.ev("()=>__HO.boot('jo')")
        p.ev("async()=>{await __HO.mokOpen();return await __HO.listPainted(90000)}")
        k = 'note|' + N131
        o, at = pin_open(p, N131, g)
        T(g, 'F1 압정 톡 → 팝업 · 화면 안(폭 ≤ 390 · 아래 끝 ≤ 844)', bool(o) and o['rect']['x'] >= 0 and o['rect']['r'] <= 390 and o['rect']['y'] >= 0 and o['rect']['b'] <= 844 and o['ta'] == 'none',
          {'rect': o and o['rect'], 'at': at, 'ta': o and o['ta']})
        if not o:
            return
        p.shot('%s_%s_phone_popup' % (tag, eng))
        e = p.ev("k=>__HO.emptyAt(k)", k)
        # 옮기기 여유를 만들려고 먼저 키운다(휠 대신 앱 함수 — 폰에는 휠이 없다)
        if p.cdp and e:
            p.touch([[(e['x'] - 20 - i * 4, e['y']), (e['x'] + 20 + i * 4, e['y'])] for i in range(16)])
            o2 = p.ev("k=>__HO.omr(k)", k)
            T(g, 'F2 두 손가락 벌림(CDP 핀치) → 배율 커짐', o2['s'] > o['s'] * 1.3, {'s': [round(o['s'], 4), round(o2['s'], 4)]})
        else:
            N(g, 'F2 핀치', 'webkit 은 톡만 진짜 터치(도구 한계) — 두 손가락은 chromium CDP 로만 잰다')
            p.ev("k=>{const w=POPS.find(x=>x._pk==='cv|omr|'+k);const v=w.querySelector('.opv');const r=v.getBoundingClientRect();v.dispatchEvent(new WheelEvent('wheel',{deltaY:-400,clientX:r.left+r.width/2,clientY:r.top+r.height/2,bubbles:true,cancelable:true}))}", k)
            p.pg.wait_for_timeout(300)
            o2 = p.ev("k=>__HO.omr(k)", k)
        e = p.ev("k=>__HO.emptyAt(k)", k)
        how = p.drag(e['x'], e['y'], e['x'] - 60, e['y'] - 80) if e else None
        o3 = p.ev("k=>__HO.omr(k)", k)
        T(g, 'F3 한 손가락 끌기 → 옮김(스크롤만 · 배율 무변)', bool(e) and o3['s'] == o2['s'] and (abs(o3['sl'] - o2['sl']) > 20 or abs(o3['stp'] - o2['stp']) > 20),
          {'how': how, 'd': [o3['sl'] - o2['sl'], o3['stp'] - o2['stp']]})
        p.click(p.ev("k=>__HO.omrAt(k,'pick')", k), 300)
        if p.cdp:
            e = p.ev("k=>__HO.emptyAt(k)", k)
            p.touch([[(e['x'] - 30, e['y'] - 10 + i * 6), (e['x'] + 30, e['y'] - 10 + i * 6)] for i in range(14)])
            o4 = p.ev("k=>__HO.omr(k)", k)
            T(g, 'P4 영역 지정 중 두 손가락 끌기 → 네모 안 생김', bool(o4) and o4['box'] is None and o4['tmp'] == 0 and o4['pick'], {'box': o4 and o4['box']})
        a = p.ev("k=>__HO.vpt(k,.3,.35)", k); b = p.ev("k=>__HO.vpt(k,.7,.6)", k)
        how = p.drag(a['x'], a['y'], b['x'], b['y'])
        o5 = p.ev("k=>__HO.omr(k)", k)
        T(g, 'F4 영역 지정 — 한 손가락 끌기 → 네모 · 확정 단추', bool(o5) and bool(o5['box']) and o5['ok'], {'how': how, 'box': o5 and o5['box']})
        p.click(p.ev("k=>__HO.omrAt(k,'ok')", k), 500)
        V = (p.ev("()=>__HO.ls()") or {}).get(k)
        T(g, 'F5 톡 「이 자리로 확정」 → 손값 칸', bool(V) and V.get('h') == HASH and V.get('who', '').endswith('폰'), V)
        er = [x for x in p.errs + (p.ev("()=>__HO.errs()") or []) if not CJ.NOISE(x)]
        T(g, 'Z 페이지 오류 0(ResizeObserver loop · 자원 못 받음 잡음 빼고)', not er, er[:6])
    except Exception as ex:
        T(g, '묶음 예외', False, repr(ex)[:400])
    finally:
        p.close()


# ══════════ 동기화 — 새 키 jopangi.ncomr · 옛 판 기기 창(메모: 새 SYNC_KEYS 키는 옛 판 기기가 올릴 때 빠진다) ══════════
def scen_sync(br, base, new, G):
    g = 'NEW 동기화'
    k = 'note|' + N131
    A = Pg(br, 'chromium', 'NEW', new, 1440, 900, who='꼬까')
    B = Pg(br, 'chromium', 'NEW', new, 1440, 900, who='햄찌')
    C = Pg(br, 'chromium', 'BASE', base, 1440, 900, who='옛판')
    try:
        for x in (A, B, C):
            x.ev("()=>__HJ.quiet()"); x.ev("f=>__HJ.sync(f)", False); x.ev("()=>__HJ.quiet()")
        # ① A 가 찍고 올린다
        A.ev("()=>__HO.boot('jo')"); A.ev("async()=>{await __HO.mokOpen();return await __HO.listPainted(90000)}")
        o, _ = pin_open(A, N131, g)
        A.click(A.ev("k=>__HO.omrAt(k,'pick')", k), 300)
        a = A.ev("k=>__HO.vpt(k,.3,.3)", k); b = A.ev("k=>__HO.vpt(k,.6,.6)", k)
        A.drag(a['x'], a['y'], b['x'], b['y'])
        A.click(A.ev("k=>__HO.omrAt(k,'ok')", k), 600)
        A.ev("()=>__HJ.quiet()"); A.ev("()=>__HJ.stamp()"); A.ev("([t,h])=>__HJ.remoteSet(t,h)", [None, None])
        s1 = A.ev("f=>__HJ.sync(f)", True)
        P1 = A.ev("()=>__HJ.remoteGet()")['text']
        p1 = json.loads(P1) if P1 else {'data': {}, 'u': {}}
        cell = (p1['data'].get('jopangi.ncomr') or {}).get(k)
        T(g, 'S1 새 판 A 확정 → 원격 data[jopangi.ncomr][note|1.3.1…] · 도장 u', bool(cell) and cell.get('h') == HASH and ('jopangi.ncomr|' + k) in p1.get('u', {}),
          {'sync': s1, 'cell': cell})
        # ② 새 판 B 가 받는다 → 목록 압정 채움
        B.ev("([t,h])=>__HJ.remoteSet(t,h)", [P1, 'S1']); B.ev("f=>__HJ.sync(f)", False); B.ev("()=>__HJ.quiet()")
        B.ev("()=>__HO.boot('jo')"); L = B.ev("async()=>{await __HO.mokOpen();return await __HO.listPainted(90000)}")
        r = next((x for x in (L or {}).get('rows', []) if x['note'] == N131), {})
        T(g, 'S2 새 판 B 가 받으면 칸 그대로 · 목록 압정 속 채움', (B.ev("()=>__HO.ls()") or {}).get(k) == cell and 'mkpin' in (r.get('cls') or ''), {'cls': r.get('cls')})
        # ③ 옛 판 C(bd8cfdf) 가 받아 제 변경(수정 큐)과 함께 올린다 → 창
        C.ev("([t,h])=>__HJ.remoteSet(t,h)", [P1, 'S1'])
        C.ev("()=>{try{lsWrite('jopangi.editq',[{k:'hz1',target:'note',st:'대기',t:Date.now()}],'수정 큐');}catch(e){}return 1}")
        C.ev("()=>__HJ.quiet()"); C.ev("()=>__HJ.stamp()")
        C.ev("f=>__HJ.sync(f)", True)
        P4 = C.ev("()=>__HJ.remoteGet()")['text']
        p4 = json.loads(P4)
        has = 'jopangi.ncomr' in p4['data']
        N(g, 'S3 옛 판 기기가 올린 원격 — 새 키 칸이 빠지는가(창)', {'data에 ncomr': has, 'u 도장 남음': ('jopangi.ncomr|' + k) in p4.get('u', {}),
                                                         'gone 묘비': [x for x in (p4.get('gone') or {}) if x.startswith('jopangi.ncomr|')]})
        # ④ 새 판 A 가 다시 맞춘다 → 되살려 올린다
        A.ev("([t,h])=>__HJ.remoteSet(t,h)", [P4, 'S4']); A.ev("f=>__HJ.sync(f)", False); A.ev("()=>__HJ.quiet()")
        P5 = A.ev("()=>__HJ.remoteGet()")
        p5 = json.loads(P5['text'])
        c5 = (p5['data'].get('jopangi.ncomr') or {}).get(k)
        T(g, 'S4 새 판 A 가 맞추면 원격에 칸이 되살아난다(묘비 0 · A 칸 무변)', c5 == cell and not [x for x in (p5.get('gone') or {}) if x.startswith('jopangi.ncomr|')]
          and (A.ev("()=>__HO.ls()") or {}).get(k) == cell, {'puts': P5.get('puts'), 'cell': c5})
        er = [y for x in (A, B, C) for y in (x.errs + (x.ev("()=>__HO.errs()") or [])) if not CJ.NOISE(y)]
        T(g, 'Z 페이지 오류 0(세 기기)', not er, er[:6])
    except Exception as ex:
        T(g, '묶음 예외', False, repr(ex)[:400])
    finally:
        for x in (A, B, C):
            x.close()


def report(t0, newf, basef, newmd5):
    lines = ['# _harness_jo_ms_omrpop — %s' % time.strftime('%Y-%m-%d %H:%M'),
             'NEW = %s (md5(LF) %s) · BASE = %s · 데이터 = genie jo/data (hash %s)' % (newf, newmd5, basef, HASH), '']
    for grp, name, ok, d in RES:
        dd = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)
        lines.append('%s | %s · %s | %s' % ('NOTE' if ok is None else 'PASS' if ok else 'FAIL', grp, name, dd[:600]))
    new = [x for x in RES if x[2] is not None and not x[0].startswith('BASE')]
    base = [x for x in RES if x[2] is not None and x[0].startswith('BASE')]
    np_, nf = sum(1 for x in new if x[2]), sum(1 for x in new if not x[2])
    bp, bf = sum(1 for x in base if x[2]), sum(1 for x in base if not x[2])
    lines += ['', '헛잣대(BASE) — PASS %d · FAIL %d (새 기능 잣대는 FAIL 이어야 잣대)' % (bp, bf),
              '합계(NEW)  PASS %d · FAIL %d  (%.0f초)' % (np_, nf, time.time() - t0)]
    txt = '\n'.join(lines) + '\n'
    f = os.path.join(OUT, '_harness_jo_ms_omrpop_result.txt')
    for _ in range(3):
        io.open(f, 'w', encoding='utf-8', newline='\n').write(txt); time.sleep(0.5)
        if io.open(f, encoding='utf-8').read() == txt:
            break
    print('\n'.join(lines[-3:]))
    return nf


def main():
    import hashlib
    t0 = time.time()
    os.makedirs(WORK, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    new = io.open(NEWF, encoding='utf-8').read()
    newmd5 = hashlib.md5(new.replace('\r\n', '\n').encode('utf-8')).hexdigest()
    if BASEF:
        base = io.open(BASEF, encoding='utf-8').read()
    else:
        base = git('show', BASE_REV + ':jo/index.html').decode('utf-8')
    bmd5 = hashlib.md5(base.replace('\r\n', '\n').encode('utf-8')).hexdigest()
    G = ground()
    print('땅값', {'hash': G['hash'], 'notes': len(G['names']), 'leaf': len(G['leaf']), 'gray': G['gray'], 'gray_bn만': G['gray_bn'], '1.3.1': len(G['by'].get(N131, [])), 'b35': G['b35']}, flush=True)
    T('땅값', 'G0-3 canvas_meta hash', G['hash'] == HASH, G['hash'])
    T('땅값', 'BASE = c2card 인도 판(bd8cfdf · c5210438)', bmd5 == BASE_MD5, bmd5)
    run = lambda x: not ONLY or x in ONLY
    A = {}
    with sync_playwright() as pw:
        cr = pw.chromium.launch()
        if run('base'):
            scen_desk(cr, 'chromium', base, 'BASE', G, A)
        if run('desk'):
            scen_desk(cr, 'chromium', new, 'NEW', G, A)
        if run('phone'):
            scen_phone(cr, 'chromium', new, 'NEW', G)
        if run('sync'):
            scen_sync(cr, base, new, G)
        cr.close()
        wk = pw.webkit.launch()
        if run('wk'):
            scen_desk(wk, 'webkit', new, 'NEW', G, A)
        if run('wkphone'):
            scen_phone(wk, 'webkit', new, 'NEW', G)
        wk.close()
    # A — 이름 줄 x 가 바탕과 같음(빈자리 덕 · 모든 줄): 줄 안 이름 자리의 차가 모든 줄에서 같은 값
    if 'BASEchromium' in A and 'NEWchromium' in A and A['BASEchromium'] and A['NEWchromium']:
        bb = {r['note']: r['nr']['x'] - r['rr']['x'] for r in A['BASEchromium']['rows']}
        nn = {r['note']: r['nr']['x'] - r['rr']['x'] for r in A['NEWchromium']['rows']}
        d = sorted({round(nn[f] - bb[f], 2) for f in nn if f in bb})
        T('NEW chromium 책상', 'A8 이름 줄 x = 바탕 + 같은 값(빈자리 덕 · 모든 줄 · 압정 줄과 빈자리 줄이 같다)', len(nn) == len(bb) and len(d) == 1,
          {'dx': d, 'rows': len(nn), '뜻': '압정 11 − 5(margin) + 8(gap) = 14px 만큼 모든 줄이 같이 민다 — 줄끼리의 맞춤(들여쓰기)은 바탕 그대로'})
    return report(t0, NEWF, BASEF or BASE_REV, newmd5)


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
