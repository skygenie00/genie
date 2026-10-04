# -*- coding: utf-8 -*-
r"""_task_jo_ms_canvas_relayout §D 관문 (+ _add1 B-3) — 데이터 · 눈 확인 · 편집 · ◇ 도형 · 옛 기록 옮기기 · 터치.

  NEW  = --new <파일>(없으면 genie 작업트리 jo/index.html) + genie 작업트리 jo/data(이 판 데이터 — canvas_meta·p1~11·remap·매칭 셋·note_canvas)
  BASE = genie 4be73ca(md5 966aaa9e · 이 판의 바탕 = book_stamp 인도 판) + 그 판 데이터(git show 로 꺼낸 canvas_*·note_canvas — 옛 배치 94d50c76)
  헛잣대(규칙 ⑩) = 같은 편집·도형 관문을 BASE 에 먼저 · 옛 기록 픽스처 = BASE 에서 실제로 만든 기록(머리 블록 3L461·3L703 은 칩이 없어
         메모·링크 창은 앱 함수 openPop 으로 열고 글은 진짜 키로 친다 · 핀은 앱 lsWrite 로 앱과 같은 꼴을 쓴다)
  엔진 = chromium · webkit 책상 1440×900(마우스) · 아이패드 1024×1366(chromium = CDP 진짜 터치 · webkit = 톡만 진짜 터치) · 눈 확인 = chromium 2600×2600
  잣대 = 데이터(viewCanvas._cv().D · LOG) · DOM 실물 · elementFromPoint · 저장소 값 — 픽셀 비교는 안 한다(눈 확인 그림은 사람·Code 가 본다)

쓰기 : python _harness_jo_ms_canvas_relayout.py [--new 파일] [--out 폴더] [--only data,eye,edit,shape,pad,mig] [--eng chromium|webkit] [--report]
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402 — _task_qa_slim(10/4) 실행 모드: --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같다) · regress = NEW 만(바탕 4be73ca 앱 · 옛 산출 안 풀고 안 띄움 · 헛잣대 장면 0 · 눈 확인 그림 · 원본 PDF 재계산 · 고정 커밋 diff 는 gate 만 · 바탕 값 칸은 기준 스냅샷 --snap-in/--snap-out) · smoke = 기본 점검 칸만(chromium) · 새 갈래는 모두 `if QJ.REGRESS:` / `if QJ.GATE:` 안
_NR = _roots.need_n('민소 canvas 재료 · 정리OMR PDF')   # env_lanes_fix(9/29) — N: 작업 폴더 · 없으면(클라우드) 「N: 필요 — 클라우드 불가(…)」 종료 코드 3
import copy, hashlib, http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
CJH = os.path.dirname(os.path.abspath(__file__))   # env_lanes_fix(9/29) — 같은 폴더(N: · genie _qa 같은 모양 · 옛: N: 고정 자리)
sys.path.insert(0, CJH)
import _harness_canvas_jari as CJ          # noqa: E402 — SEED(기록·교재 fetch 돌림 · 저장소 비우기) · route_filter · VENDOR · __HJ
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


HERE = os.path.dirname(os.path.abspath(__file__))
OUT = ARG('--out', HERE)
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
ENGS = [ARG('--eng')] if ARG('--eng') else ['chromium', 'webkit']
if QJ.SMOKE:   # smoke — chromium 만(이 하네스의 smoke 칸은 책상 폭 둘)
    ENGS = [e for e in ENGS if e == 'chromium']
GENIE = CJ.GENIE
JOD = os.path.join(GENIE, 'jo')
NEWF = ARG('--new', os.path.join(JOD, 'index.html'))
BASE_REV, BASE_MD5 = '4be73ca', '966aaa9e4b587df2ed6a3ee73a014937'
CV = os.path.join(_NR, 'jopangi', '민소', 'canvas')
PROTO = os.path.join(CV, '_relayout_proto')
PDF = os.path.join(_NR, 'jopangi', '정리omr', '26민소정리OMR.pdf')
SHOTS = os.path.join(CV, '_relayout_shots')
B3T = os.path.join(CV, '_relayout_b3_table.json')
WORK = os.path.join(tempfile.gettempdir(), 'h_canvas_relayout')
BASED = os.path.join(WORK, 'base_data')
NEWD = os.path.join(JOD, 'data', 'omr', '민소')
TESTS = io.open(os.path.join(HERE, '_harness_jo_ms_canvas_relayout_tests.js'), encoding='utf-8').read()
READY = "!!window.__HR&&typeof render==='function'&&typeof viewCanvas==='function'"
PITCH = 1.35
SERVERS = {}
RES = []

# regress — 바탕 4be73ca(불변 커밋)에서 한 번 잰 값. 옛 산출(git show 15 개) · 바탕 앱으로 옮기기 픽스처 만들기를 regress 가 안 한다(gate 는 그대로 풀고 만든다).
PICKS_FROZEN = ('3L505', '3L386', ('3L366', '3L381'))   # pick_blocks(바탕 canvas_p3 쪽) — 편집 관문 세 대상(지울 블록 · 윗줄 합칠 줄 · 합칠 블록 쌍)
O_FROZEN = {3: {'oy': 2413.7, 'lines': [{'id': '3L20', 'x': 433.3, 'x1': 482.7, 'y': 2523.24, 'h': 2.7, 'r': [{'t': '·'}]}, {'id': '3L356', 'x': 703.4, 'x1': 815.6, 'y': 2833.17, 'h': 2.7, 'r': [{'t': '·'}]}, {'id': '3L461', 'x': 538.0, 'x1': 555.2, 'y': 2921.62, 'h': 2.7, 'r': [{'t': '·'}]}, {'id': '3L462', 'x': 374.0, 'x1': 385.7, 'y': 2923.46, 'h': 2.7, 'r': [{'t': '·'}]}]}}   # 바탕 3쪽의 줄 넷 + oy — 픽스처 카드 · 필기 획 셋에 가장 가까운 옛 줄(nearest 가 고르는 것 · 글은 자리표시)
MIG_FX_FROZEN = json.loads('{"jopangi.canvas":"{\\"민소\\":{\\"hash\\":\\"94d50c76\\",\\"ops\\":[{\\"t\\":\\"card\\",\\"n\\":3,\\"id\\":\\"3Nmupxposizp1\\",\\"x\\":1180,\\"y\\":2883.66,\\"ts\\":1790883360454},{\\"t\\":\\"text\\",\\"id\\":\\"3Nmupxposizp1\\",\\"s\\":\\"C1\\",\\"ts\\":1790883361550},{\\"t\\":\\"eraseshape\\",\\"n\\":3,\\"key\\":\\"l:511.9,2598.2,511.9,2726.7\\",\\"ts\\":1790883368039},{\\"t\\":\\"eraseshape\\",\\"n\\":3,\\"key\\":\\"l:512.2,2594.6,512.2,2725.7\\",\\"ts\\":1790883368044}]}}","jopangi.canvasink":"{\\"민소\\":{\\"p3\\":[{\\"c\\":\\"#111\\",\\"w\\":1.2,\\"k\\":\\"pen\\",\\"p\\":[[540.4,511.8,1],[541.9,511.9,1],[543.5,511.9,1],[545,512,1],[546.6,512,1],[548.2,512.1,1],[549.7,512.1,1],[551.3,512.2,1],[552.9,512.2,1]]},{\\"c\\":\\"#111\\",\\"w\\":1.2,\\"k\\":\\"pen\\",\\"p\\":[[373.6,513.7,1],[375.2,513.7,1],[376.7,513.8,1],[378.3,513.8,1],[379.9,513.9,1],[381.4,513.9,1],[383,514,1],[384.5,514,1],[386.1,514.1,1]]},{\\"c\\":\\"#111\\",\\"w\\":1.2,\\"k\\":\\"pen\\",\\"p\\":[[437.1,113.4,1],[438.6,113.5,1],[440.2,113.5,1],[441.7,113.6,1],[443.3,113.6,1],[444.9,113.7,1],[446.4,113.8,1],[448,113.8,1],[449.6,113.9,1]]}]}}","jopangi.canvasmemo":"{\\"3L461\\":\\"메모461\\",\\"3L703\\":\\"메모703\\",\\"8L42\\":\\"메모8L42\\"}","jopangi.canvaspin":"{\\"3L461\\":{\\"ts\\":1790000000000}}","jopangi.canvaslink":"{\\"3L461\\":[{\\"to\\":{\\"k\\":\\"block\\",\\"key\\":\\"2L1149\\"},\\"why\\":\\"\\",\\"show\\":false,\\"t\\":1790883355933}],\\"8L40\\":[{\\"to\\":{\\"k\\":\\"block\\",\\"key\\":\\"8L42\\"},\\"why\\":\\"\\",\\"show\\":false,\\"t\\":1790883358958}]}","jopangi.canvasjari":null,"_ops":[{"t":"card","n":3,"id":"3Nmupxposizp1","x":1180,"y":2883.66,"ts":1790883360454},{"t":"text","id":"3Nmupxposizp1","s":"C1","ts":1790883361550},{"t":"eraseshape","n":3,"key":"l:511.9,2598.2,511.9,2726.7","ts":1790883368039},{"t":"eraseshape","n":3,"key":"l:512.2,2594.6,512.2,2725.7","ts":1790883368044}],"_ink":[{"c":"#111","w":1.2,"k":"pen","p":[[540.4,511.8,1],[541.9,511.9,1],[543.5,511.9,1],[545,512,1],[546.6,512,1],[548.2,512.1,1],[549.7,512.1,1],[551.3,512.2,1],[552.9,512.2,1]]},{"c":"#111","w":1.2,"k":"pen","p":[[373.6,513.7,1],[375.2,513.7,1],[376.7,513.8,1],[378.3,513.8,1],[379.9,513.9,1],[381.4,513.9,1],[383,514,1],[384.5,514,1],[386.1,514.1,1]]},{"c":"#111","w":1.2,"k":"pen","p":[[437.1,113.4,1],[438.6,113.5,1],[440.2,113.5,1],[441.7,113.6,1],[443.3,113.6,1],[444.9,113.7,1],[446.4,113.8,1],[448,113.8,1],[449.6,113.9,1]]}]}')   # 바탕 앱(4be73ca)이 실제 조작으로 만든 옮기기 픽스처 — 10/2 04:36 gate 실행의 WORK\mig_fixture.json 그대로


def say(ok, name, detail=''):
    RES.append(('PASS' if ok is True else 'FAIL' if ok is False else 'INFO', name, detail))
    print(RES[-1][0], '|', name, '|', str(detail)[:300], flush=True)


def git(*a, repo=GENIE):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def wr_n(path, data):
    """N: 쓰기 — 0.5초 뒤 되읽어 대조(마이박스 이웃 파일 바뀜)"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for _ in range(4):
        open(path, 'wb').write(data); time.sleep(0.5)
        if open(path, 'rb').read() == data:
            return True
    raise SystemExit('되읽기 불일치: ' + path)


def base_data():
    os.makedirs(BASED, exist_ok=True)
    names = ['canvas_meta.json', 'canvas_match.json', 'canvas_cand.json', 'note_canvas.json'] + ['canvas_p%d.json' % n for n in range(1, 12)]
    for f in names:
        b = git('show', BASE_REV + ':jo/data/omr/민소/' + f)
        assert b, f
        open(os.path.join(BASED, f), 'wb').write(b)


def serve(tag, src, datamode):
    key = tag + '|' + datamode
    if key in SERVERS:
        return SERVERS[key][1]
    out = os.path.join(WORK, 'srv_' + tag + '_' + datamode); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    src = src.replace('\r\n', '\n')
    b = src.index('<body'); bb = src.index('>', b) + 1
    html = src[:bb] + CJ.SEED + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + CJ.TESTS + '\n</script>\n<script>\n' + TESTS + '\n</script>\n' + html[e:]
    io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=out, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            if p.startswith('/__vendor/'):
                return os.path.join(CJ.VENDOR, p[len('/__vendor/'):].replace('/', os.sep))
            if datamode == 'base' and p.startswith('/data/omr/민소/'):
                f = os.path.join(BASED, p[len('/data/omr/민소/'):])
                if os.path.exists(f):
                    return f
                if p.endswith('canvas_remap.json'):
                    return os.path.join(WORK, 'nope.json')
            if p.startswith('/data/'):
                return os.path.join(JOD, 'data', p[6:].replace('/', os.sep))
            if p in ('/index.html', '/'):
                return super().translate_path(path)
            f = os.path.join(JOD, p.lstrip('/').replace('/', os.sep))
            return f if os.path.exists(f) else super().translate_path(path)

        def log_message(self, *a, **k):
            pass
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[key] = (srv, srv.server_address[1])
    return srv.server_address[1]


class P:
    def __init__(self, br, eng, tag, src, W, H, datamode, mode='desk', q='tok=1'):
        self.eng, self.tag, self.mode = eng, tag, mode
        QJ.launch('base' if tag == 'BASE' else 'new')   # 셈(§B-4) — 바탕(BASE) 판을 띄운 수 · NEW 를 띄운 수
        self.pad = mode == 'pad'
        self.port = serve(tag, src, datamode)
        if self.pad:
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=CJ.IPAD_UA)
        else:
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1)
        self.ctx.route('**/*', CJ.route_filter)
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(180000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
        self.miss = []
        self.pg.on('response', lambda r: self.miss.append(urllib.parse.unquote(r.url.split('/', 3)[-1])) if r.status >= 400 else None)
        self.cdp = self.ctx.new_cdp_session(self.pg) if (eng == 'chromium' and self.pad) else None
        self.load(q)

    def load(self, q):
        self.pg.goto('http://127.0.0.1:%d/index.html?%s&who=%s' % (self.port, q, urllib.parse.quote('꼬까')), wait_until='load', timeout=180000)
        self.pg.wait_for_function(READY, timeout=180000)
        self.pg.wait_for_timeout(1000)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def w(self, ms):
        self.pg.wait_for_timeout(ms)

    def click(self, x, y, wait=450):
        if self.pad:
            self.pg.touchscreen.tap(x, y)
        else:
            self.pg.mouse.click(x, y)
        self.w(wait)

    def mdrag(self, x0, y0, x1, y1, n=10, wait=500):
        m = self.pg.mouse
        m.move(x0, y0); m.down()
        for i in range(1, n + 1):
            m.move(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.w(16)
        m.up(); self.w(wait)

    def tdrag(self, x0, y0, x1, y1, n=12, wait=500):
        def t(ty, pts):
            self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': pts})
        t('touchStart', [{'x': x0, 'y': y0, 'id': 1}])
        for i in range(1, n + 1):
            t('touchMove', [{'x': x0 + (x1 - x0) * i / n, 'y': y0 + (y1 - y0) * i / n, 'id': 1}]); self.w(16)
        for _ in range(3):
            t('touchMove', [{'x': x1, 'y': y1, 'id': 1}]); self.w(30)
        t('touchEnd', []); self.w(wait)

    def t2(self, a0, b0, a1, b1, n=12, wait=500):
        """두 손가락 — a·b 두 점을 a0→a1 · b0→b1 로(chromium CDP)"""
        def t(ty, pts):
            self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': pts})
        t('touchStart', [{'x': a0[0], 'y': a0[1], 'id': 1}]); self.w(30)
        t('touchStart', [{'x': a0[0], 'y': a0[1], 'id': 1}, {'x': b0[0], 'y': b0[1], 'id': 2}]); self.w(30)
        for i in range(1, n + 1):
            f = i / n
            t('touchMove', [{'x': a0[0] + (a1[0] - a0[0]) * f, 'y': a0[1] + (a1[1] - a0[1]) * f, 'id': 1},
                            {'x': b0[0] + (b1[0] - b0[0]) * f, 'y': b0[1] + (b1[1] - b0[1]) * f, 'id': 2}]); self.w(20)
        t('touchEnd', []); self.w(wait)

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


# ══════════ 잣대 도구(파이썬) ══════════
def load_pages(d):
    out = {}
    for n in range(1, 12):
        out[n] = json.load(open(os.path.join(d, 'canvas_p%d.json' % n), encoding='utf-8'))
    return out


def ltxt(l):
    return ''.join(r['t'] for r in l.get('r') or [])


def hov(a, b):
    """가로 겹침(0.5pt 넘게 · 빈 줄도 한 글자 폭 3pt) — a·b = (x, x1)"""
    ax1, bx1 = max(a[1], a[0] + 3), max(b[1], b[0] + 3)
    return a[0] < bx1 - 0.5 and b[0] < ax1 - 0.5


def overlaps_rows(rows):
    """[id, y, x, x1, h, del, t] → 글 상자 겹침 짝 집합(프로토·canvas_relayout.overlaps 와 같은 판정)"""
    L = sorted([(r[2], r[3], r[1], r[1] + r[4], r[0]) for r in rows if not r[5] and r[6].strip()], key=lambda a: a[2])
    out = set()
    for i, a in enumerate(L):
        for b in L[i + 1:]:
            if b[2] >= a[3] - 0.05:
                break
            if a[0] < b[1] - 0.5 and b[0] < a[1] - 0.5:
                out.add(tuple(sorted((a[4], b[4]))))
    return out


def pt_box(x, y, l):
    """점과 줄 상자 거리(pt)"""
    dx = max(0.0, l['x'] - x, x - l['x1']); dy = max(0.0, l['y'] - y, y - (l['y'] + l['h']))
    return (dx * dx + dy * dy) ** 0.5


def nearest(lines, x, y):
    best = None
    for l in lines:
        if l.get('del') or not ltxt(l).strip():
            continue
        d = pt_box(x, y, l)
        if best is None or d < best[1]:
            best = (l['id'], d)
    return best


# ══════════ 데이터 관문 ══════════
def scen_data_regress():
    """regress — 산출 파일만 읽는 자료 칸(_task_qa_slim A-6) · 칸 글은 gate 와 같다.
    안 한다(처리표 「관문만」 · gate 만): 옛 산출(바탕 4be73ca git show) 풀기 · 원본 PDF 재계산(G0-3 · G0-4 · A-2 · A-5) · ⚙ 모듈(canvas_relayout · canvas_note · canvas_ids) 재계산 ·
    목차노트 판정 표(add1 · B-3 · 바탕 canvas_match 와 대조) · 고정 두 커밋의 앱 diff.
    옛 값을 기댓값으로 쓰던 칸(줄 id · 블록 bid · 줄 글 = 바탕)은 지금 산출의 지문(md5)을 저장된 기준 스냅샷과 맞댄다(스냅샷 없으면 첫 기록)."""
    N = load_pages(NEWD)
    meta_n = json.load(open(os.path.join(NEWD, 'canvas_meta.json'), encoding='utf-8'))
    remap = json.load(open(os.path.join(NEWD, 'canvas_remap.json'), encoding='utf-8'))
    r4 = open(os.path.join(CV, 'blocks2_r4.json'), 'rb').read()
    OLD_HASH = '94d50c76'   # 바탕 데이터 hash — gate 의 G0-3 칸이 blocks2_r3 md5 앞 8 과 같다고 단정하는 값(불변)
    say(meta_n['hash'] == hashlib.md5(r4).hexdigest()[:8] == remap['to'] and remap['from'] == OLD_HASH, 'A-1·C-3 새 데이터 hash = blocks2_r4 md5 앞 8 = remap.to · remap.from = 바탕 hash',
        '%s · r4 %s · remap %s→%s' % (meta_n['hash'], hashlib.md5(r4).hexdigest()[:8], remap['from'], remap['to']))
    dg = lambda v: hashlib.md5(json.dumps(v, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()
    idn = {n: [l['id'] for l in N[n]['lines']] for n in N}; bn = {n: [b['bid'] for b in N[n]['blocks']] for n in N}
    say(QJ.same('data-ids', dg(idn)), '줄 id 목록(차례·개수) = 바탕', '줄 %d · 지문 기준 %s' % (sum(map(len, idn.values())), QJ.base_note('data-ids')))
    say(QJ.same('data-bids', dg(bn)), '블록 bid 목록 = 바탕(del·to 달린 것 포함)', '블록 %d · del %d · 지문 기준 %s' % (sum(map(len, bn.values())),
                                                                                      sum(1 for n in N for b in N[n]['blocks'] if b.get('del')), QJ.base_note('data-bids')))
    tails = {l['id']: l.get('to') for n in N for l in N[n]['lines'] if l.get('del')}
    delb = {b['bid']: b.get('to') for n in N for b in N[n]['blocks'] if b.get('del')}
    say(len(tails) == 13 and all(tails.values()), 'B-2 뒤 조각 줄 13 = {del, r:[], to}', sorted(tails.items()))
    say(all(delb.values()), 'B-2 del 블록마다 to', '%d %s' % (len(delb), sorted(delb.items())))
    NT = {l['id']: ltxt(l) for n in N for l in N[n]['lines']}
    say(QJ.same('data-text', dg(NT)), '줄 글 = 바탕(합친 13 · (cid: 2 만 다름)', '줄 글 %d · 지문 기준 %s' % (len(NT), QJ.base_note('data-text')))
    # 겹침 ⊆ overlap_ref 42(합친 뒤 id)
    REFO = json.load(open(os.path.join(PROTO, 'overlap_ref.json'), encoding='utf-8'))
    fl = lambda k: tails.get(k) or k
    refp = {tuple(sorted((fl(x['a']), fl(x['b'])))) for x in REFO}
    newp = set()
    for n in N:
        rows = [[l['id'], l['y'], l['x'], l.get('x1', l['x']), l['h'], 1 if l.get('del') else 0, ltxt(l)] for l in N[n]['lines']]
        newp |= overlaps_rows(rows)
    say(newp <= refp, '전 줄 쌍 글 상자 겹침 ⊆ overlap_ref 42 짝', '새 판 %d 짝 · 참값 %d · 새 짝 %s · 없어진 짝 %s' % (len(newp), len(refp), sorted(newp - refp)[:10], sorted(refp - newp)))
    REF = json.load(open(os.path.join(PROTO, 'origy_ref.json'), encoding='utf-8'))   # 원본 y 참값(gate 는 A-2 가 읽는다)
    # 원본에 없는 빈자리 — 줄마다 위에서 가로로 겹치는 가장 가까운 줄과의 새 간격 − 1.4 × 원본 간격(밀림으로 더 벌어진 몫)
    big, top = [], []
    for n in N:
        L = [l for l in N[n]['lines'] if not l.get('del') and ltxt(l).strip() and l['id'] in REF]
        for l in L:
            w = (l['x'], max(l['x1'], l['x'] + 3))
            up = [q for q in L if q is not l and q['y'] < l['y'] - 0.05 and hov((q['x'], q['x1']), w)]
            if not up:
                continue
            a = max(up, key=lambda q: q['y'])
            do = REF[l['id']] - REF[a['id']]
            if do > 0:
                ex = (l['y'] - a['y']) - 1.4 * do
                top.append((round(ex, 2), l['id'], a['id']))
    top.sort(reverse=True)
    say(not [x for x in top if x[0] > 10], '원본에 없는 빈자리 — 원본 간격 × 1.4 보다 10pt 넘게 더 벌어진 자리 0', '3pt 넘는 자리 %d %s' % (sum(1 for x in top if x[0] > 3), [x for x in top if x[0] > 3]))
    rep_r = json.load(open(os.path.join(CV, '_relayout_report.json'), encoding='utf-8'))['rep']
    dfl = [x[0] for x in rep_r.get('deflate', [])]
    say(sorted(dfl) == sorted(['3L3', '3L15', '5L4', '6L686', '6L687', '8L508']) and all(N[int(i.split('L')[0])]['lines'][int(i.split('L')[1])]['h'] <= 3 for i in dfl),
        'A-3a 부푼 줄 높이 바로잡기(글자 크기의 3배 + 1pt 넘는 줄 → 글자 크기)', rep_r.get('deflate'))
    # 쪽 높이 · cols
    ph = [N[n]['ph'] for n in N]
    say(all(abs(v - 1107.3) < 0.05 for i, v in enumerate(ph) if i != 9) and abs(ph[9] - 1117.9) < 0.05 and all(N[n].get('cols') == [] for n in N)
        and not any('col' in l for n in N for l in N[n]['lines']), 'A-3 쪽 높이 1,107.3(10쪽 1,117.9) · cols [] · 줄 col 없음', ph)
    # A-6 sid · remap sk
    sids_ok = all(o.get('sid') == '%d%s%d' % (n, tag, i) for n in N for key, tag in (('shapes', 'S'), ('imgs', 'I'), ('bars', 'B'), ('hls', 'H')) for i, o in enumerate(N[n].get(key) or []))
    nsh = sum(len(N[n]['shapes']) for n in N)
    say(sids_ok and len(remap['sk']) == nsh == 738, 'A-6 도형 sid = {n}S·I·B·H{i} · remap.sk = 옛 도형 열쇠 738', 'sk %d · 도형 %d' % (len(remap['sk']), nsh))
    say(all(len(x) == 4 and isinstance(x[0], str) and all(isinstance(v, (int, float)) for v in x[1:]) for pg in remap['pages'].values() for x in pg['L'])
        and set(remap) == {'from', 'to', 'pages', 'sk'},
        'C-3 remap 은 좌표·id 만(줄 글 없음 · D11)', '쪽 %d · 줄 %d' % (len(remap['pages']), sum(len(pg['L']) for pg in remap['pages'].values())))


def scen_data():
    import pymupdf
    sys.path.insert(0, CV)
    from canvas_ids import assign_ids
    import canvas_relayout as CR
    O = load_pages(BASED)
    N = load_pages(NEWD)
    meta_o = json.load(open(os.path.join(BASED, 'canvas_meta.json'), encoding='utf-8'))
    meta_n = json.load(open(os.path.join(NEWD, 'canvas_meta.json'), encoding='utf-8'))
    remap = json.load(open(os.path.join(NEWD, 'canvas_remap.json'), encoding='utf-8'))
    r3 = open(os.path.join(CV, 'blocks2_r3.json'), 'rb').read()
    r4 = open(os.path.join(CV, 'blocks2_r4.json'), 'rb').read()
    say(meta_o['hash'] == '94d50c76' == hashlib.md5(r3).hexdigest()[:8], 'G0-3 바탕 데이터 hash = blocks2_r3 md5 앞 8(94d50c76)', meta_o['hash'])
    say(meta_n['hash'] == hashlib.md5(r4).hexdigest()[:8] == remap['to'] and remap['from'] == meta_o['hash'], 'A-1·C-3 새 데이터 hash = blocks2_r4 md5 앞 8 = remap.to · remap.from = 바탕 hash',
        '%s · r4 %s · remap %s→%s' % (meta_n['hash'], hashlib.md5(r4).hexdigest()[:8], remap['from'], remap['to']))
    # A-2 원본 y — 코드로 다시 재서 origy_ref 와 ±0.3
    doc = pymupdf.open(PDF)
    say(len(doc) == 11 and abs(doc[0].rect.width - 1221.7) < 0.2 and abs(doc[0].rect.height - 790.9) < 0.2, 'G0-4 원본 PDF 11쪽 · 1221.7×790.9pt', '%d쪽 %.1f×%.1f' % (len(doc), doc[0].rect.width, doc[0].rect.height))
    D0 = assign_ids(json.loads(r3))
    t0 = time.time()
    OY, st = CR.orig_y(D0, doc)
    REF = json.load(open(os.path.join(PROTO, 'origy_ref.json'), encoding='utf-8'))
    diff = [k for k in REF if k not in OY or abs(OY[k] - REF[k]) > 0.3]
    extra = [k for k in OY if k not in REF]
    say(not diff and not extra and len(OY) == 6882, 'A-2 원본 y = origy_ref(±0.3)', '줄 %d · 다름 %d %s · 참값에 없는 줄 %d · %s · %.0f초' % (len(OY), len(diff), diff[:8], len(extra), dict(st), time.time() - t0))
    # A-5 — 채팅 목록(프로토 relayout_verify 규칙 · 옛 데이터 · origy_ref) ↔ 이 판(canvas_relayout 검산 · 합친 뒤)
    chat, tot = [], 0
    for n in range(1, 12):
        ch = []
        for b in doc[n - 1].get_text('rawdict')['blocks']:
            for li in b.get('lines', []):
                for sp in li['spans']:
                    for c in sp['chars']:
                        if c['c'].strip():
                            ch.append((c['bbox'][1], c['bbox'][0], c['c']))
        chs = sorted(ch, key=lambda c: c[1])
        for l in O[n]['lines']:
            k = l['id']
            runs = [r for r in l['r'] if len(re.sub(r'\s', '', r['t'])) >= 3 and '(cid:' not in r['t']]
            if not runs or k not in REF:
                continue
            r = max(runs, key=lambda r: len(r['t'])); t = re.sub(r'\s', '', r['t'])[:40]
            v = REF[k]; tot += 1
            row = ''.join(c[2] for c in chs if abs(c[0] - v) < 0.8 and r['x'] - 1.5 <= c[1] <= r['x'] + r.get('w', 50) + 200)
            if t not in row:
                chat.append(k)
    rep = json.load(open(os.path.join(CV, '_relayout_report.json'), encoding='utf-8'))['rep']
    ours = [x[0] for x in rep['verify']['list']]
    say(sorted(chat) == sorted(ours) and len(chat) == 10, 'A-5 어긋남 = 채팅 목록(프로토 규칙 재계산)',
        '채팅 규칙 %d줄 중 %d %s · 이 판 %d줄 중 %d' % (tot, len(chat), sorted(chat), rep['verify']['checked'], len(ours)))
    # 줄 id · 블록 bid 집합 · 차례
    ido = {n: [l['id'] for l in O[n]['lines']] for n in O}; idn = {n: [l['id'] for l in N[n]['lines']] for n in N}
    bo = {n: [b['bid'] for b in O[n]['blocks']] for n in O}; bn = {n: [b['bid'] for b in N[n]['blocks']] for n in N}
    say(ido == idn, '줄 id 목록(차례·개수) = 바탕', '줄 %d → %d' % (sum(map(len, ido.values())), sum(map(len, idn.values()))))
    say(bo == bn, '블록 bid 목록 = 바탕(del·to 달린 것 포함)', '블록 %d → %d · del %d' % (sum(map(len, bo.values())), sum(map(len, bn.values())),
                                                                 sum(1 for n in N for b in N[n]['blocks'] if b.get('del'))))
    tails = {l['id']: l.get('to') for n in N for l in N[n]['lines'] if l.get('del')}
    delb = {b['bid']: b.get('to') for n in N for b in N[n]['blocks'] if b.get('del')}
    say(len(tails) == 13 and all(tails.values()), 'B-2 뒤 조각 줄 13 = {del, r:[], to}', sorted(tails.items()))
    say(all(delb.values()), 'B-2 del 블록마다 to', '%d %s' % (len(delb), sorted(delb.items())))
    # 줄 글 = 바탕 — 합친 13(앞 줄 = 옛 앞 + 옛 뒤 · 뒤 = 빈 것)과 (cid: 2 만 다름
    heads = {v: k for k, v in tails.items()}
    OT = {l['id']: ltxt(l) for n in O for l in O[n]['lines']}; NT = {l['id']: ltxt(l) for n in N for l in N[n]['lines']}
    bad, cid = [], []
    for k in OT:
        o, v = OT[k], NT.get(k)
        if k in tails:
            if v != '':
                bad.append((k, '뒤 조각이 비지 않음'))
        elif k in heads:
            if v != o + OT[heads[k]]:
                bad.append((k, '앞 줄 ≠ 옛 앞 + 옛 뒤'))
        elif v != o:
            if '(cid:' in o and v == re.sub(r'\(cid:\d+\)', '', o):
                cid.append(k)
            else:
                bad.append((k, o[:20], (v or '')[:20]))
    say(not bad and sorted(cid) == ['3L15', '3L3'], '줄 글 = 바탕(합친 13 · (cid: 2 만 다름)', '다름 %d %s · (cid: 뺀 줄 %s' % (len(bad), bad[:5], cid))
    # 겹침 ⊆ overlap_ref 42(합친 뒤 id)
    REFO = json.load(open(os.path.join(PROTO, 'overlap_ref.json'), encoding='utf-8'))
    fl = lambda k: tails.get(k) or k
    refp = {tuple(sorted((fl(x['a']), fl(x['b'])))) for x in REFO}
    newp = set()
    for n in N:
        rows = [[l['id'], l['y'], l['x'], l.get('x1', l['x']), l['h'], 1 if l.get('del') else 0, ltxt(l)] for l in N[n]['lines']]
        newp |= overlaps_rows(rows)
    say(newp <= refp, '전 줄 쌍 글 상자 겹침 ⊆ overlap_ref 42 짝', '새 판 %d 짝 · 참값 %d · 새 짝 %s · 없어진 짝 %s' % (len(newp), len(refp), sorted(newp - refp)[:10], sorted(refp - newp)))
    # 원본에 없는 빈자리 — 줄마다 위에서 가로로 겹치는 가장 가까운 줄과의 새 간격 − 1.4 × 원본 간격(밀림으로 더 벌어진 몫)
    big, top = [], []
    for n in N:
        L = [l for l in N[n]['lines'] if not l.get('del') and ltxt(l).strip() and l['id'] in REF]
        for l in L:
            w = (l['x'], max(l['x1'], l['x'] + 3))
            up = [q for q in L if q is not l and q['y'] < l['y'] - 0.05 and hov((q['x'], q['x1']), w)]
            if not up:
                continue
            a = max(up, key=lambda q: q['y'])
            do = REF[l['id']] - REF[a['id']]
            if do > 0:
                ex = (l['y'] - a['y']) - 1.4 * do
                top.append((round(ex, 2), l['id'], a['id']))
    top.sort(reverse=True)
    say(not [x for x in top if x[0] > 10], '원본에 없는 빈자리 — 원본 간격 × 1.4 보다 10pt 넘게 더 벌어진 자리 0', '3pt 넘는 자리 %d %s' % (sum(1 for x in top if x[0] > 3), [x for x in top if x[0] > 3]))
    rep_r = json.load(open(os.path.join(CV, '_relayout_report.json'), encoding='utf-8'))['rep']
    dfl = [x[0] for x in rep_r.get('deflate', [])]
    say(sorted(dfl) == sorted(['3L3', '3L15', '5L4', '6L686', '6L687', '8L508']) and all(N[int(i.split('L')[0])]['lines'][int(i.split('L')[1])]['h'] <= 3 for i in dfl),
        'A-3a 부푼 줄 높이 바로잡기(글자 크기의 3배 + 1pt 넘는 줄 → 글자 크기)', rep_r.get('deflate'))
    # 쪽 높이 · cols
    ph = [N[n]['ph'] for n in N]
    say(all(abs(v - 1107.3) < 0.05 for i, v in enumerate(ph) if i != 9) and abs(ph[9] - 1117.9) < 0.05 and all(N[n].get('cols') == [] for n in N)
        and not any('col' in l for n in N for l in N[n]['lines']), 'A-3 쪽 높이 1,107.3(10쪽 1,117.9) · cols [] · 줄 col 없음', ph)
    # A-6 sid · remap sk
    sids_ok = all(o.get('sid') == '%d%s%d' % (n, tag, i) for n in N for key, tag in (('shapes', 'S'), ('imgs', 'I'), ('bars', 'B'), ('hls', 'H')) for i, o in enumerate(N[n].get(key) or []))
    nsh = sum(len(N[n]['shapes']) for n in N)
    say(sids_ok and len(remap['sk']) == nsh == 738, 'A-6 도형 sid = {n}S·I·B·H{i} · remap.sk = 옛 도형 열쇠 738', 'sk %d · 도형 %d' % (len(remap['sk']), nsh))
    say(all(len(x) == 4 and isinstance(x[0], str) and all(isinstance(v, (int, float)) for v in x[1:]) for pg in remap['pages'].values() for x in pg['L'])
        and set(remap) == {'from', 'to', 'pages', 'sk'},
        'C-3 remap 은 좌표·id 만(줄 글 없음 · D11)', '쪽 %d · 줄 %d' % (len(remap['pages']), sum(len(pg['L']) for pg in remap['pages'].values())))
    scen_b3()
    scen_diff()


def scen_diff():
    """민소 정리 탭 밖 무변 — 바탕 ↔ 새 판 앱 diff 의 모든 바뀐 줄이 정리캔버스 모듈(viewCanvas IIFE) 안이거나 cv- CSS 줄인가"""
    import difflib
    a = git('show', BASE_REV + ':jo/index.html').decode('utf-8').splitlines()
    DIFF_NEW_REV = '06fd454'   # A-6(d) 9/30 — 인도 검산 새 쪽 = canvas_relayout 인도판(md5(LF) 3898dea6 · 인도 결과 머리 NEW) · 옛: NEWF(지금 판 — 그 뒤 판들이 정리 탭 밖을 고쳐 헛돎)
    b = git('show', DIFF_NEW_REV + ':jo/index.html').decode('utf-8').replace('\r\n', '\n').splitlines()
    def rng(L):
        i0 = next(i for i, l in enumerate(L) if l.startswith('const viewCanvas = (() => {'))
        i1 = next(i for i, l in enumerate(L) if i > i0 and l.startswith('/* ══ 정리캔버스(민소) 끝 ══ */'))
        return i0, i1
    ra, rb = rng(a), rng(b)
    out, n = [], 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == 'equal':
            continue
        for k in range(i1, i2):
            n += 1
            if not (ra[0] <= k <= ra[1] or a[k].startswith(('#cv', '.cv-'))):
                out.append(('-', k + 1, a[k][:60]))
        for k in range(j1, j2):
            n += 1
            if not (rb[0] <= k <= rb[1] or b[k].startswith(('#cv', '.cv-'))):
                out.append(('+', k + 1, b[k][:60]))
    say(not out, '민소 정리 탭 밖 무변 — 앱 diff 의 바뀐 줄이 전부 정리캔버스 모듈 안 · cv- CSS', '바뀐 줄 %d · 밖 %d %s' % (n, len(out), out[:4]))


def scen_b3():
    """_add1 B-3 새 게이트 — 바탕(C-0 r3) ↔ 새 판(r4 + 규칙 ③ 새 좌표) 블록 목차노트 표 · ① 바뀜 0 · 10쪽 항고·재심 · 「둘 다 아님」·「새가 나쁨」 0(보고) · toc/c/cf"""
    sys.path.insert(0, CV)
    from canvas_ids import assign_ids
    import canvas_note as CN
    A = json.load(open(os.path.join(BASED, 'canvas_match.json'), encoding='utf-8')); CA = json.load(open(os.path.join(BASED, 'canvas_cand.json'), encoding='utf-8'))['c']
    B = json.load(open(os.path.join(NEWD, 'canvas_match.json'), encoding='utf-8')); CB = json.load(open(os.path.join(NEWD, 'canvas_cand.json'), encoding='utf-8'))['c']
    D3 = assign_ids(json.load(open(os.path.join(CV, 'blocks2_r3.json'), encoding='utf-8')))
    D4 = assign_ids(json.load(open(os.path.join(CV, 'blocks2_r4.json'), encoding='utf-8')))
    N4, H4 = CN.block_notes(D4)

    def texts(D):
        out, where = {}, {}
        for p in D['pages']:
            for b in p['blocks']:
                out[b['bid']] = None if b.get('del') else '\n'.join(ltxt(p['lines'][i]) for i in b['ls'])
                where[b['bid']] = (p['n'], b)
        return out, where
    T3, W3 = texts(D3); T4, W4 = texts(D4)
    merged = {k for k in set(T3) | set(T4) if T3.get(k) != T4.get(k)}
    note_of = lambda M, W, k: (M['bn'][k] if k in M.get('bn', {}) else (W[k][1].get('note') or '')) if k in W else ''
    rows = []
    for k, (n, b) in W4.items():
        if b.get('del') or b.get('k') == '헤딩':
            continue
        o, nn = note_of(A, W3, k) or '', note_of(B, W4, k) or ''
        if o != nn:
            rows.append({'bid': k, 'p': n, 'old': o, 'new': nn, 'how': H4.get(k), 'merged': k in merged})
    J = json.load(open(B3T, encoding='utf-8')) if os.path.exists(B3T) else []
    V = {r['bid']: r for r in J}
    g1 = [r['bid'] for r in rows if r['how'] == '①' and not r['merged']]
    say(not g1, 'add1 ① 블록(합친 것 밖) 목차노트 바뀜 0', g1)
    same = sorted(r['bid'] for r in rows) == sorted(V) and all(V[r['bid']]['old'] == r['old'] and V[r['bid']]['new'] == r['new'] for r in rows)
    from collections import Counter
    cnt = Counter(V[r['bid']]['v'] for r in rows if r['bid'] in V)
    say(same, 'add1 바뀐 블록 표 = 판정 표(_relayout_b3_table.json)', '바뀐 %d · 표 %d · 판정 %s' % (len(rows), len(V), dict(cnt)))
    p10 = [r for r in rows if r['p'] == 10]
    ok10 = [r['bid'] for r in p10 if not (r['new'].startswith('8.4') or r['new'].startswith('9.'))]
    judged10 = [r['bid'] for r in p10 if V.get(r['bid'], {}).get('v') == '새']
    say(not [b for b in ok10 if b in judged10], 'add1 10쪽 항고·재심 글 → 8.4·9 (판정 「새」 블록 전부)', '10쪽 바뀜 %d · 「새」 %d · 8.4/9 아닌 것 %s' % (len(p10), len(judged10), ok10))
    both = sorted(r['bid'] for r in rows if V.get(r['bid'], {}).get('v') == '둘 다 아님')
    worse = sorted(r['bid'] for r in rows if V.get(r['bid'], {}).get('v') == '옛')
    say(not both, 'add1 「둘 다 아님」 0 (남으면 보고 — 멈추지 않음)', '%d %s' % (len(both), both))
    say(not worse, 'add1 「새가 나쁨」 0 (남으면 보고)', '%d %s' % (len(worse), worse))
    mm = [k for k in set(A['m']) | set(B['m']) if k not in merged and A['m'].get(k) != B['m'].get(k)]
    say(not mm, 'B-3 합친 블록 밖 m 바이트 같음', '%d %s' % (len(mm), mm[:8]))
    cc = [k for k in set(CA) | set(CB) if k not in merged and CA.get(k) != CB.get(k)]
    cf = [k for k in set(A.get('cf', {})) | set(B.get('cf', {})) if k not in merged and A['cf'].get(k) != B['cf'].get(k)]
    tc = [k for k in set(A['toc']) | set(B['toc']) if A['toc'].get(k) != B['toc'].get(k)]
    say(None, 'add1 따라 바뀜(표·합친 블록으로 설명 · 채팅 셈 toc 21 · c 141 · cf 5)', 'toc %d · c %d · cf %d' % (len(tc), len(cc), len(cf)))


# ══════════ 눈 확인 — 11쪽 나란히 · 확대 표본 ══════════
def compose(a_png, b_png, out, cap):
    from PIL import Image, ImageDraw
    A = Image.open(io.BytesIO(a_png)).convert('RGB'); B = Image.open(io.BytesIO(b_png)).convert('RGB')
    top = 26
    W = A.width + B.width + 24; H = max(A.height, B.height) + top
    im = Image.new('RGB', (W, H), (238, 236, 230))
    im.paste(A, (0, top)); im.paste(B, (A.width + 24, top))
    d = ImageDraw.Draw(im)
    d.text((6, 6), cap[0], fill=(40, 40, 40)); d.text((A.width + 30, 6), cap[1], fill=(40, 40, 40))
    bio = io.BytesIO(); (im.quantize(colors=96) if im.width > 3000 else im).save(bio, 'PNG', optimize=True)   # 쪽 나란히 그림은 색 96 으로(크기 — 눈 확인용)
    wr_n(out, bio.getvalue())
    return out


def scen_eye_regress(br):
    """regress — 눈 확인(11쪽 원본|앱 나란히 그림 · 확대 표본 19장 · 원본 PDF 렌더 · PIL 합성 · 장마다 N: 쓰고 0.5초 되읽기)은 안 한다(처리표 「관문만」 · 사람이 보는 그림).
    11쪽을 다 그려 보며 페이지 오류 0 만 잰다(smoke 는 1 · 3 · 11쪽)."""
    src = io.open(NEWF, encoding='utf-8').read()
    p = P(br, 'chromium', 'EYE', src, 2600, 2600, 'new')
    try:
        p.ev("__HR.boot()"); p.ev("__HR.eyeCss()")
        for n in ((1, 3, 11) if QJ.SMOKE else range(1, 12)):
            p.ev("async n=>await __HR.fitPage(n, 0.5)", n)
            p.w(700)
        say(not p.errs and not p.ev("__HR.errs()"), '눈 확인 — 페이지 오류 0', p.errs[:3])
    finally:
        p.close()


def scen_eye(br):
    import pymupdf
    doc = pymupdf.open(PDF)
    O = load_pages(BASED); N = load_pages(NEWD)
    REF = json.load(open(os.path.join(PROTO, 'origy_ref.json'), encoding='utf-8'))
    src = io.open(NEWF, encoding='utf-8').read()
    p = P(br, 'chromium', 'EYE', src, 2600, 2600, 'new')
    shots = []
    try:
        p.ev("__HR.boot()"); p.ev("__HR.eyeCss()")
        for n in range(1, 12):
            r = p.ev("async n=>await __HR.fitPage(n, 0.5)", n)
            p.w(700)
            png = p.pg.screenshot(clip={'x': r['x'], 'y': r['y'], 'width': r['w'], 'height': min(r['h'], r['stage']['y'] + r['stage']['h'] - r['y'])})
            z = r['w'] / doc[n - 1].rect.width
            pdfpng = doc[n - 1].get_pixmap(matrix=pymupdf.Matrix(z, z)).tobytes('png')
            f = compose(pdfpng, png, os.path.join(SHOTS, 'p%02d.png' % n), ('PDF p.%d (original)' % n, 'APP p.%d (relayout K1.4 LEAD1.2)' % n))
            shots.append(f)
        say(len(shots) == 11, '눈 확인 11쪽 나란히 그림(원본 | 앱) → _relayout_shots\\pNN.png', shots[0] + ' …')
        # 확대 표본 — 3쪽 {3.4.}·{3.4.1.}·3L3 · 8L185·8L220 · 10L137·10L142 · 10L602·10L606 · 합친 13
        find = lambda n, pre: next((l['id'] for l in N[n]['lines'] if ltxt(l).startswith(pre)), None)
        tails = {l['to']: l['id'] for n in N for l in N[n]['lines'] if l.get('del')}
        samp = [('34', [find(3, '{3.4. ')]), ('341', ['3L461']), ('3L3', ['3L3']), ('8L185', ['8L185', '8L220']), ('10L137', ['10L137', '10L142']),
                ('10L602', ['10L602', '10L606'])] + [('m_' + h, [h]) for h in sorted(tails, key=lambda k: (int(k.split('L')[0]), int(k.split('L')[1])))]
        zs = []
        for name, ids in samp:
            ids = [i for i in ids if i]
            if not ids:
                say(False, '확대 표본 ' + name, '줄을 못 찾음'); continue
            n = int(ids[0].split('L')[0])
            nl = {l['id']: l for l in N[n]['lines']}; ol = {l['id']: l for l in O[n]['lines']}
            ls = [nl[i] for i in ids]
            ids_o = ids + [tails[i] for i in ids if i in tails]
            x0 = min(min(l['x'] for l in ls), min(ol[i]['x'] for i in ids_o)) - 24
            x1 = max(max(l['x1'] for l in ls), max(ol[i]['x1'] for i in ids_o)) + 24
            ny0 = min(l['y'] for l in ls) - 14; ny1 = max(l['y'] + l['h'] for l in ls) + 14
            oy0 = min(REF[i] for i in ids_o) - 10 - 2.7; oy1 = max(REF[i] for i in ids_o) + 10
            r = p.ev("async a=>await __HR.region(a[0],a[1],a[2],a[3],1)", [x0, ny0, x1, ny1])
            png = p.pg.screenshot(clip={'x': r['x'], 'y': r['y'], 'width': r['w'], 'height': r['h']})
            pdfpng = doc[n - 1].get_pixmap(matrix=pymupdf.Matrix(4, 4), clip=pymupdf.Rect(x0, max(0, oy0), x1, oy1)).tobytes('png')
            zs.append(compose(pdfpng, png, os.path.join(SHOTS, 'z_%s.png' % name), ('PDF p.%d %s' % (n, ','.join(ids_o)), 'APP p.%d' % n)))
        say(len(zs) == len(samp), '확대 표본 %d 장(3쪽 {3.4.}·{3.4.1.}·3L3 · 8L185·8L220 · 10L137·10L142 · 10L602·10L606 · 합친 13)' % len(samp), ', '.join(os.path.basename(z) for z in zs))
        say(not p.errs and not p.ev("__HR.errs()"), '눈 확인 — 페이지 오류 0', p.errs[:3])
    finally:
        p.close()


# ══════════ 편집 관문(BASE·NEW 같은 조작) ══════════
def pick_blocks(Pg):
    """편집 대상 — 3쪽: 지울 블록(2~5줄 · 아래 가로 겹침 줄 있음) · 윗줄 합칠 줄(단락 둘째 줄) · 합칠 블록(아래 같은 급 가로 겹침 짝)"""
    L, B = Pg['lines'], Pg['blocks']
    ext = lambda b: (b['x'], b['x'] + b['w'])
    below = lambda b: [l for l in L if not l.get('del') and l['y'] > b['y'] + b['h'] and hov((l['x'], l['x1']), ext(b))]
    rel = lambda y: (y - Pg['oy']) / Pg['ph']
    dl = next(b['bid'] for b in B if b['k'] != '헤딩' and not b.get('del') and 2 <= len(b['ls']) <= 5 and b['d'] >= 1 and 0.45 < rel(b['y']) < 0.7 and len(below(b)) >= 5)
    mu = None
    for b in B:
        if b['k'] == '단락' and not b.get('del') and len(b['ls']) >= 2:
            a, c = L[b['ls'][0]], L[b['ls'][1]]
            if hov((a['x'], a['x1']), (c['x'], c['x1'])) and 0 < c['y'] - a['y'] < 6 and 0.35 < rel(c['y']) < 0.85 and ltxt(c).strip():
                mu = c['id']; break
    mg = None
    for i, b in enumerate(B):
        if b['k'] == '헤딩' or b.get('del') or not (0.35 < rel(b['y']) < 0.9):
            continue
        sib = sorted([c for c in B if c is not b and not c.get('del') and c.get('p') == b.get('p') and c['d'] == b['d'] and c['y'] > b['y'] and hov(ext(c), ext(b))], key=lambda c: c['y'])
        if sib and sib[0]['y'] - (b['y'] + b['h']) < 12:
            mg = (b['bid'], sib[0]['bid']); break
    return dl, mu, mg


def rowsd(rows):
    return {r[0]: r for r in rows}


def gate_shift(L0, L1, src_ids, dy_expect=None):
    """밀기·당기기 공통 — 움직인 줄은 src 아래·사슬(가로 겹침으로 이어짐) · 같은 높이 옆 자리 줄 그대로 · 모두 같은 값 · 새 겹침 0"""
    A, B = rowsd(L0), rowsd(L1)
    src = [A[i] for i in src_ids]
    sy = max(r[1] for r in src)
    moved = [k for k in A if k in B and not A[k][5] and not B[k][5] and abs(A[k][1] - B[k][1]) > 0.005]
    dys = sorted({round(B[k][1] - A[k][1], 2) for k in moved})
    below = all(A[k][1] > sy for k in moved)
    chain_ok, bad = True, []
    anchors = [(r[2], r[3]) for r in src]
    for k in sorted(moved, key=lambda k: A[k][1]):
        w = (A[k][2], A[k][3])
        if not any(hov(w, a) for a in anchors):
            chain_ok = False; bad.append(k)
        anchors.append(w)
    side = [k for k in A if not A[k][5] and k not in src_ids and abs(A[k][1] - sy) < 4 and not any(hov((A[k][2], A[k][3]), (s[2], s[3])) for s in src)]
    side_same = [k for k in side if k in B and abs(A[k][1] - B[k][1]) < 0.005]
    ov0, ov1 = overlaps_rows(L0), overlaps_rows(L1)
    newov = sorted(ov1 - ov0)
    one = bool(dys) and max(dys) - min(dys) <= 0.011 and (dy_expect is None or all(abs(d - dy_expect) <= 0.011 for d in dys))   # 2자리 반올림(3.645 → 3.64/3.65)
    ok = bool(moved) and below and chain_ok and len(side_same) == len(side) and not newov and one
    return ok, '움직인 줄 %d · dy %s · src 아래 %s · 사슬 %s%s · 같은 높이 옆 자리 %d 중 그대로 %d · 새 겹침 %d %s' % (
        len(moved), dys[:4], below, chain_ok, (' 사슬 밖 ' + str(bad[:6])) if bad else '', len(side), len(side_same), len(newov), newov[:4])


def sayer(tag):
    """새 판 = PASS/FAIL · 바탕 판 = INFO([바탕 PASS/FAIL] — 헛잣대: 같은 관문이 바탕에서 어떻게 나오나)"""
    if tag == 'NEW':
        return say
    return lambda ok, name, detail='': say(None, name, '[바탕 %s] %s' % ('PASS' if ok is True else 'FAIL' if ok is False else '-', detail))


def scen_edit(br, eng, tag, src, dm):
    R = {'eng': eng, 'tag': tag}
    Pg = load_pages(BASED if dm == 'base' else NEWD)[3]
    dl, mu, mg = PICKS_FROZEN if QJ.REGRESS else pick_blocks(load_pages(BASED)[3])
    p = P(br, eng, tag, src, 1440, 900, dm)
    pre = '편집 %s %s — ' % (tag, eng)
    S_ = sayer(tag)
    try:
        R['boot'] = p.ev("__HR.boot()")
        L0 = p.ev("n=>__HR.lines(n)", 3)
        n0 = p.ev("__HR.info()")['ops']
        # E-1 3.4.1 뒤 새 줄(Enter)
        l = p.ev("id=>__HR.lineOf(id)", '3L461')
        p.ev("a=>__HR.center(a[0],a[1],1.2)", [l['x'] + 12, l['y'] + l['h'] / 2])
        s = p.ev("id=>__HR.lineAt(id)", '3L461')
        p.pg.mouse.dblclick(s['x'], s['y']); p.w(600)
        R['e1_ed'] = p.ev("__HR.ed()")
        p.pg.keyboard.press('Enter'); p.w(700)
        p.pg.keyboard.press('Escape'); p.w(400)
        L1 = p.ev("n=>__HR.lines(n)", 3)
        R['e1_ops'] = p.ev("__HR.ops(1)")
        newl = [r for r in L1 if r[0] not in rowsd(L0)]
        S_(bool(R['e1_ed']) and len(newl) == 1 and R['e1_ops'] and R['e1_ops'][0]['t'] == 'new' and abs(newl[0][1] - (l['y'] + l['h'] * PITCH)) < 0.02,
            pre + 'E-1 3.4.1(3L461) 두 번 눌러 편집 → Enter = 새 줄 한 줄(op new)', '편집 %s · 새 줄 %s · op %s' % (R['e1_ed'], newl[:1], R['e1_ops']))
        if QJ.SMOKE:   # smoke — E-1 첫 칸(두 번 눌러 편집 → Enter = 새 줄)까지만
            return R
        ok, d = gate_shift(L0, L1, ['3L461'], round(l['h'] * PITCH, 2)); S_(ok, pre + 'E-1 새 줄 → 가로로 겹치는 아래 줄만 내려감 · 같은 높이 옆 자리 줄 그대로 · 새 겹침 0', d)
        R['e1_col'] = 'col' in json.dumps(R['e1_ops'])
        S_(not R['e1_col'] and bool(R['e1_ops']) and R['e1_ops'][0].get('v') == 2, pre + 'C-1 새 op 에 col 칸 없음 · v:2', R['e1_ops'])
        p.pg.keyboard.press('Control+z'); p.w(700)
        Lu = p.ev("n=>__HR.lines(n)", 3)
        S_(Lu == L0 and p.ev("__HR.info()")['ops'] == n0, pre + 'E-6 Ctrl+Z → 새 줄 전과 같음(줄 y·로그)', '같음 %s' % (Lu == L0))
        # E-2 블록 지우기(칩 「지우기」) → 사슬만 당김 · 당긴 뒤 겹침 0
        bx = [b for b in Pg['blocks'] if b['bid'] == dl][0]
        p.ev("a=>__HR.center(a[0],a[1],1.0)", [bx['x'] + bx['w'] / 2, bx['y'] + bx['h'] / 2])
        at = p.ev("b=>__HR.blkPt(b)", dl)
        p.click(at['x'], at['y'], 500)
        R['e2_sel'] = p.ev("__HR.selBlk()")
        c = p.ev("__HR.chipOp('del')")
        if c:
            p.click(c['x'], c['y'], 700)
        L2 = p.ev("n=>__HR.lines(n)", 3)
        gone = [Pg['lines'][i]['id'] for i in bx['ls']]
        S_(R['e2_sel'] and R['e2_sel']['bid'] == dl and all(rowsd(L2)[k][5] for k in gone), pre + 'E-2 블록 %s 고름 → 칩 「지우기」 → 그 줄 del' % dl, '%s · 지운 줄 %s' % (R['e2_sel'], gone))
        ok, d = gate_shift(L0, L2, gone); S_(ok, pre + 'E-2 블록 지우기 → 사슬만 당김 · 옆 자리 그대로 · 당긴 뒤 새 겹침 0', d)
        p.pg.keyboard.press('Control+z'); p.w(700)
        S_(p.ev("n=>__HR.lines(n)", 3) == L0, pre + 'E-6 Ctrl+Z → 블록 지우기 전과 같음', '')
        # E-3 윗줄 합침(맨 앞 ⌫)
        lm = p.ev("id=>__HR.lineOf(id)", mu)
        p.ev("a=>__HR.center(a[0],a[1],1.2)", [lm['x'] + 12, lm['y'] + lm['h'] / 2])
        s = p.ev("id=>__HR.lineAt(id)", mu)
        p.pg.mouse.dblclick(s['x'], s['y']); p.w(600)
        p.pg.keyboard.press('Home'); p.w(150); p.pg.keyboard.press('Backspace'); p.w(700)
        R['e3_ed'] = p.ev("__HR.ed()")
        p.pg.keyboard.press('Escape'); p.w(400)
        L3 = p.ev("n=>__HR.lines(n)", 3)
        A0, A3 = rowsd(L0), rowsd(L3)
        cand = [k for k in A0 if not A0[k][5] and A0[k][1] < A0[mu][1] and hov((A0[k][2], A0[k][3]), (A0[mu][2], A0[mu][3]))]
        prev = max(cand, key=lambda k: A0[k][1]) if cand else None
        ok = prev and A3[mu][5] == 1 and A3[prev][6] == A0[prev][6] + A0[mu][6]
        S_(bool(ok), pre + 'E-3 %s 맨 앞 ⌫ → 윗줄(위에서 가로로 겹치는 가장 가까운 줄 %s)에 붙고 그 줄 del' % (mu, prev),
            '윗줄 글 끝 %r · 편집 중 %s' % ((A3[prev][6][-24:] if prev else None), R['e3_ed']))
        p.pg.keyboard.press('Control+z'); p.w(700)
        S_(p.ev("n=>__HR.lines(n)", 3) == L0, pre + 'E-6 Ctrl+Z → 윗줄 합침 전과 같음', '')
        # E-4 블록 합치기(칩 「⤵ 합치기」) — 짝 = 아래 같은 급 중 가로로 겹치는 가장 가까운 것
        b0 = [b for b in Pg['blocks'] if b['bid'] == mg[0]][0]
        p.ev("a=>__HR.center(a[0],a[1],1.0)", [b0['x'] + b0['w'] / 2, b0['y'] + b0['h'] / 2])
        at = p.ev("b=>__HR.blkPt(b)", mg[0]); p.click(at['x'], at['y'], 500)
        R['e4_sel'] = p.ev("__HR.selBlk()")
        c = p.ev("__HR.chipOp('merge')")
        if c:
            p.click(c['x'], c['y'], 700)
        op = p.ev("__HR.ops(1)")
        BL = {b['bid']: b for b in p.ev("n=>__HR.blocks(n)", 3)}
        ext = lambda b: (b['x'], b['x'] + b['w'])
        sibs = sorted([c for c in Pg['blocks'] if c['bid'] != b0['bid'] and not c.get('del') and c.get('p') == b0.get('p') and c['d'] == b0['d'] and c['y'] > b0['y'] and hov(ext(c), ext(b0))], key=lambda c: c['y'])
        want = sibs[0]['bid'] if sibs else None
        ok = R['e4_sel'] and R['e4_sel']['bid'] == mg[0] and op and op[0]['t'] == 'merge' and op[0]['sib'] == want and BL[want]['del']
        S_(bool(ok), pre + 'E-4 블록 %s → 「⤵ 합치기」 짝 = %s(아래 같은 급 · 가로로 겹치는 가장 가까운 것)' % (mg[0], want), 'op %s' % op)
        p.pg.keyboard.press('Control+z'); p.w(700)
        # E-5 카드(빈 곳 두 번 누름)
        y = Pg['oy'] + 60
        ex = next((x for x in range(1180, 700, -20) if not any(l['y'] - 8 < y < l['y'] + l['h'] + 8 and l['x'] - 8 < x < l['x1'] + 8 for l in Pg['lines'] if not l.get('del'))), None)
        s = p.ev("a=>__HR.center(a[0],a[1],1.0)", [ex, y])
        p.pg.mouse.dblclick(s['x'], s['y']); p.w(600)
        op = p.ev("__HR.ops(1)")
        p.pg.keyboard.press('Escape'); p.w(300)
        ok = op and op[0]['t'] == 'card' and abs(op[0]['x'] - ex) < 0.6 and abs(op[0]['y'] - y) < 0.6
        S_(bool(ok), pre + 'E-5 빈 곳 두 번 누름 → 카드(op card · 자리 = 누른 곳)', 'op %s · 누른 곳 (%s, %.1f)' % (op, ex, y))
        p.pg.keyboard.press('Control+z'); p.w(700)
        Lz = p.ev("n=>__HR.lines(n)", 3)
        S_([r for r in Lz if not r[5]] == [r for r in L0 if not r[5]] and p.ev("__HR.info()")['ops'] == n0, pre + 'E-6 Ctrl+Z 다 한 뒤 = 처음(줄·로그)', 'ops %d' % p.ev("__HR.info()")['ops'])
        S_(not p.errs and not p.ev("__HR.errs()") and not [u for u in p.miss if 'omr/민소/' in u], pre + '페이지 오류 0(정리캔버스 데이터 404 포함)', '%s · 404 %s' % (p.errs[:3], sorted(set(p.miss))[:4]))
    except Exception as e:
        S_(False, pre + '예외', repr(e)[:300])
    finally:
        p.close()
    return R


# ══════════ ◇ 도형 ══════════
def ink_on(p, tool):
    b = p.ev("__HR.inkBtn()")
    if b and '필기 ON' not in b['t']:
        p.click(b['x'], b['y'], 900)
    t = p.ev("t=>__HR.tool(t)", tool)
    if t:
        p.click(t['x'], t['y'], 300)
    return p.ev("t=>__HR.tool(t)", tool)


def scen_shape(br, eng, tag, src, dm):
    R = {'eng': eng, 'tag': tag}
    p = P(br, eng, tag, src, 1440, 900, dm)
    pre = '도형 %s %s — ' % (tag, eng)
    S_ = sayer(tag)
    try:
        R['boot'] = p.ev("__HR.boot()")
        if not R['boot']['shapeBtn']:
            S_(None if tag == 'BASE' else False, pre + '「◇ 도형」 단추', '없음' + (' — 바탕 판에는 없다(헛잣대: 새 판에만 있는 도구)' if tag == 'BASE' else '')); return R
        t = ink_on(p, 'shape')
        S_(bool(t and t['on']), pre + '✍ 필기 켜고 「◇ 도형」 고름', t)
        L0 = p.ev("n=>__HR.lines(n)", 3)
        G0 = p.ev("n=>__HR.geo(n)", 3)
        z = 1.5
        moved = {}
        for kind in ('r', 'l', 'c', 'img', 'bar', 'hl'):
            cs = p.ev("a=>__HR.cands(a[0],a[1],a[2])", [3, kind, 20])
            done = False
            for cd in cs:
                s = p.ev("a=>__HR.center(a[0],a[1],a[2])", [cd['x'], cd['y'], z])
                hit = p.ev("a=>__HR.at(a[0],a[1])", [s['x'], s['y']])
                if not hit or not hit['ink'] or hit['pgN'] != '3쪽':
                    continue
                n0 = p.ev("__HR.info()")['ops']
                p.mdrag(s['x'], s['y'], s['x'] + 40, s['y'] + 24)
                op = p.ev("__HR.ops(1)"); n1 = p.ev("__HR.info()")['ops']
                G1 = p.ev("n=>__HR.geo(n)", 3)
                K = 'imgs' if kind == 'img' else 'bars' if kind == 'bar' else 'hls' if kind == 'hl' else 'shapes'
                a, b = G0[K][cd['i']]['b'], G1[K][cd['i']]['b']
                dx, dy = 40 / (4 * z), 24 / (4 * z)
                ok = (n1 == n0 + 1 and op[0]['t'] == 'shapemove' and op[0]['sid'] == cd['sid'] and op[0].get('v') == 2 and abs(op[0]['dx'] - dx) < 0.3 and abs(op[0]['dy'] - dy) < 0.3
                      and abs(b[0] - a[0] - op[0]['dx']) < 0.02 and abs(b[1] - a[1] - op[0]['dy']) < 0.02)
                dom = p.ev("a=>__HR.domOf(a[0],a[1])", [3, cd['sid']])
                S_(ok and dom['n'] >= 1, pre + '%s 고르기 → 끌기 → op shapemove 1줄(%s)' % (kind, cd['sid']), 'op %s · 상자 %s → %s · DOM %s' % (op, a[:2], b[:2], dom))
                moved[kind] = cd['sid']; G0 = G1; done = True
                break
            if not done:
                S_(False, pre + '%s 고르기' % kind, '누를 수 있는 후보 없음(%d)' % len(cs))
        L1 = p.ev("n=>__HR.lines(n)", 3)
        S_(L1 == L0, pre + '도형 여섯 옮긴 뒤 글줄 y 전부 그대로', '다른 줄 %d' % sum(1 for a, b in zip(L0, L1) if a != b))
        # 🗑 — 옮긴 상자
        def select(kind, sid, idx=None):
            G = p.ev("n=>__HR.geo(n)", 3)
            K = 'imgs' if kind == 'img' else 'bars' if kind == 'bar' else 'hls' if kind == 'hl' else 'shapes'
            cs = [c for c in p.ev("a=>__HR.cands(a[0],a[1],a[2])", [3, kind, 30]) if (sid is None or c['sid'] == sid)]
            for cd in cs:
                s = p.ev("a=>__HR.center(a[0],a[1],a[2])", [cd['x'], cd['y'], z])
                hit = p.ev("a=>__HR.at(a[0],a[1])", [s['x'], s['y']])
                if hit and hit['ink']:
                    p.click(s['x'], s['y'], 400)
                    return cd, s
            return None, None
        cd, s = select('r', moved.get('r'))
        sh = p.ev("__HR.shsel()")
        ok_sel = bool(sh['sh'] and cd and sh['sh']['sid'] == cd['sid'] and sh['sel'] and sh['del'] and sh['delHit'])
        S_(ok_sel, pre + '누름 = 고름(점선 테두리 + 🗑 누를 수 있음)', sh)
        if sh['del']:
            p.click(sh['del']['cx'], sh['del']['cy'], 500)
        op = p.ev("__HR.ops(1)"); dom = p.ev("a=>__HR.domOf(a[0],a[1])", [3, cd['sid']]) if cd else None
        S_(bool(cd) and op[0]['t'] == 'shapedel' and op[0]['sid'] == cd['sid'] and dom['n'] == 0, pre + '🗑 → op shapedel · DOM 에서 빠짐', 'op %s · DOM %s' % (op, dom))
        # Delete 키 — 형광
        cd, s = select('hl', None)
        p.pg.keyboard.press('Delete'); p.w(500)
        op = p.ev("__HR.ops(1)")
        S_(bool(cd) and op[0]['t'] == 'shapedel' and op[0]['sid'] == cd['sid'], pre + 'Delete 키 → op shapedel', op)
        # Esc — 막대
        cd, s = select('bar', None)
        a1 = p.ev("__HR.shsel()")['sh']
        p.pg.keyboard.press('Escape'); p.w(300)
        a2 = p.ev("__HR.shsel()")
        S_(bool(a1) and not a2['sh'] and not a2['sel'], pre + 'Esc → 고름 풀림', '%s → %s' % (a1, a2['sh']))
        # 되돌리기 — 곡선 하나 옮기고 Ctrl+Z
        cs = p.ev("a=>__HR.cands(a[0],a[1],a[2])", [3, 'c', 30])
        cd = next((c for c in cs if c['sid'] != moved.get('c')), None)
        Gb = p.ev("n=>__HR.geo(n)", 3); nb = p.ev("__HR.info()")['ops']
        s = p.ev("a=>__HR.center(a[0],a[1],a[2])", [cd['x'], cd['y'], z])
        p.mdrag(s['x'], s['y'], s['x'] + 30, s['y'] - 20)
        n1 = p.ev("__HR.info()")['ops']
        p.pg.keyboard.press('Control+z'); p.w(600)
        Ga = p.ev("n=>__HR.geo(n)", 3); na = p.ev("__HR.info()")['ops']
        S_(n1 == nb + 1 and na == nb and Ga == Gb, pre + 'Ctrl+Z → 옮긴 곡선 제자리 · 로그도 뺌', 'ops %d → %d → %d · 도형 같음 %s' % (nb, n1, na, Ga == Gb))
        # 지우개 — 상자·그림
        t = ink_on(p, 'erase')
        er = {}
        for kind in ('r', 'img'):
            cs = p.ev("a=>__HR.cands(a[0],a[1],a[2])", [3, kind, 30])
            cd = next((c for c in cs if c['sid'] not in moved.values()), None) or (cs[0] if cs else None)
            if not cd:
                continue
            s = p.ev("a=>__HR.center(a[0],a[1],a[2])", [cd['x'], cd['y'], z])
            n0 = p.ev("__HR.info()")['ops']
            p.mdrag(s['x'], s['y'], s['x'] + 3, s['y'] + 2, n=3)
            ops = p.ev("k=>__HR.ops(k)", max(1, p.ev("__HR.info()")['ops'] - n0))
            er[kind] = (cd['sid'], [(o['t'], o.get('sid')) for o in ops])
        S_(all(any(t == 'shapedel' and s2 == v[0] for t, s2 in v[1]) for v in er.values()) and len(er) == 2, pre + '지우개로 상자·그림 → op shapedel', er)
        Gpre = p.ev("n=>__HR.geo(n)", 3); Lpre = p.ev("n=>__HR.lines(n)", 3); info0 = p.ev("__HR.info()")
        # 새로고침 뒤 재생 같음
        p.load('tok=1&keep=1'); p.ev("__HR.boot()")
        Gpost = p.ev("n=>__HR.geo(n)", 3); info1 = p.ev("__HR.info()")
        S_(Gpost == Gpre and p.ev("n=>__HR.lines(n)", 3) == Lpre and info1['replay']['bad'] == 0 and info1['ops'] == info0['ops'],
            pre + '새로고침 뒤 재생 = 새로고침 전(도형 자리·지움 · 글줄 · 로그)', 'replay %s · ops %d' % (info1['replay'], info1['ops']))
        S_(not p.errs and not p.ev("__HR.errs()") and not [u for u in p.miss if 'omr/민소/' in u], pre + '페이지 오류 0(정리캔버스 데이터 404 포함)', '%s · 404 %s' % (p.errs[:3], sorted(set(p.miss))[:4]))
    except Exception as e:
        S_(False, pre + '예외', repr(e)[:300])
    finally:
        p.close()
    return R


def scen_pad(br, eng, src):
    """아이패드 — 손가락 하나 = 고르기·끌기(chromium CDP) · 톡 = 고르기(webkit) · 두 손가락 = 이동·확대(op 없음)"""
    p = P(br, eng, 'NEW', src, 1024, 1366, 'new', mode='pad')
    pre = '터치 %s — ' % eng
    try:
        p.ev("__HR.boot()")
        t = ink_on(p, 'shape')
        say(bool(t and t['on']), pre + '톡으로 ✍ 필기 · 「◇ 도형」', t)
        cs = p.ev("a=>__HR.cands(a[0],a[1],a[2])", [3, 'img', 5])
        cd = cs[0]
        s = p.ev("a=>__HR.center(a[0],a[1],a[2])", [cd['x'], cd['y'], 1.2])
        if p.cdp:
            n0 = p.ev("__HR.info()")['ops']
            p.tdrag(s['x'], s['y'], s['x'] + 60, s['y'] + 30)
            op = p.ev("__HR.ops(1)"); n1 = p.ev("__HR.info()")['ops']
            say(n1 == n0 + 1 and op[0]['t'] == 'shapemove' and op[0]['sid'] == cd['sid'], pre + '손가락 하나로 그림 고르기·끌기 → shapemove', op)
            # 두 손가락 — 도형 위에서 시작해도 이동 · op 없음
            cs = p.ev("a=>__HR.cands(a[0],a[1],a[2])", [3, 'img', 5]); cd = cs[0]
            s = p.ev("a=>__HR.center(a[0],a[1],a[2])", [cd['x'], cd['y'], 1.2])
            v0 = p.ev("__HR.info()"); n0 = v0['ops']; G0 = p.ev("n=>__HR.geo(n)", 3)
            p.t2((s['x'], s['y']), (s['x'] + 80, s['y']), (s['x'] + 120, s['y'] + 90), (s['x'] + 200, s['y'] + 90))
            v1 = p.ev("__HR.info()")
            v2 = dict(v1)
            p.t2((s['x'] - 40, s['y']), (s['x'] + 40, s['y']), (s['x'] - 140, s['y']), (s['x'] + 140, s['y']))
            v3 = p.ev("__HR.info()")
            G1 = p.ev("n=>__HR.geo(n)", 3)
            # 바탕 — 같은 자리(그림 3I0 의 바탕 좌표)에서 같은 두 손가락(✍ 필기 · 펜)
            if QJ.GATE:
                b = P(p.pg.context.browser, eng, 'BASE', git('show', BASE_REV + ':jo/index.html').decode('utf-8'), 1024, 1366, 'base', mode='pad')
                try:
                    b.ev("__HR.boot()"); ink_on(b, 'pen')
                    im = json.load(open(os.path.join(BASED, 'canvas_p3.json'), encoding='utf-8'))['imgs'][0]
                    sb = b.ev("a=>__HR.center(a[0],a[1],a[2])", [im['x'] + im['w'] / 2, im['y'] + im['h'] / 2, 1.2])
                    w0 = b.ev("__HR.info()")
                    b.t2((sb['x'], sb['y']), (sb['x'] + 80, sb['y']), (sb['x'] + 120, sb['y'] + 90), (sb['x'] + 200, sb['y'] + 90))
                    w1 = b.ev("__HR.info()")
                    b.t2((sb['x'] - 40, sb['y']), (sb['x'] + 40, sb['y']), (sb['x'] - 140, sb['y']), (sb['x'] + 140, sb['y']))
                    w3 = b.ev("__HR.info()")
                finally:
                    b.close()
            else:
                # regress — 바탕(4be73ca) 판을 안 띄운다(바탕 띄움 0) · 바탕 값(두 손가락 끌기 판 움직임 · 벌리기 배율 비) = 기준 스냅샷(NEW 가 같은 손짓에 한 값 · 스냅샷 없으면 첫 기록)
                _bp = QJ.base('pad-pan@%s/dxy' % eng, [v1['vx'] - v0['vx'], v1['vy'] - v0['vy']])
                _bz = QJ.base('pad-zoom@%s/ratio' % eng, v3['vz'] / v2['vz'])
                w0 = {'vx': 0, 'vy': 0}; w1 = {'vx': _bp[0], 'vy': _bp[1], 'vz': 1.0}; w3 = {'vz': _bz}
            dn = (v1['vx'] - v0['vx'], v1['vy'] - v0['vy']); db = (w1['vx'] - w0['vx'], w1['vy'] - w0['vy'])
            say(v1['ops'] == n0 and G1 == G0 and abs(dn[0] - db[0]) <= 3 and abs(dn[1] - db[1]) <= 3,
                pre + '두 손가락 끌기(도형 위에서 시작) = 바탕과 같은 판 움직임 · op 0 · 도형 그대로', '새 판 Δ(%.0f, %.0f) · 바탕 Δ(%.0f, %.0f) · ops %d→%d' % (dn[0], dn[1], db[0], db[1], n0, v1['ops']))
            say(v3['ops'] == n0 and v3['vz'] > v2['vz'] * 1.3 and abs(v3['vz'] / v2['vz'] - w3['vz'] / w1['vz']) < 0.05,
                pre + '두 손가락 벌리기 = 확대(바탕과 같은 배율) · op 0', 'vz ×%.2f · 바탕 ×%.2f' % (v3['vz'] / v2['vz'], w3['vz'] / w1['vz']))
        else:
            p.pg.touchscreen.tap(s['x'], s['y']); p.w(500)
            sh = p.ev("__HR.shsel()")
            say(bool(sh['sh']) and sh['sh']['sid'] == cd['sid'], pre + '톡(진짜 터치)으로 그림 고르기(끌기는 webkit 도구 한계 — chromium CDP 가 잰다)', sh['sh'])
        say(not p.errs and not p.ev("__HR.errs()") and not [u for u in p.miss if 'omr/민소/' in u], pre + '페이지 오류 0(정리캔버스 데이터 404 포함)', '%s · 404 %s' % (p.errs[:3], sorted(set(p.miss))[:4]))
    except Exception as e:
        say(False, pre + '예외', repr(e)[:300])
    finally:
        p.close()


# ══════════ 옛 기록 옮기기 ══════════
def type_pop(p, js_open, sel, text):
    p.ev(js_open)
    p.w(700)
    at = p.ev("s=>{const e=[...document.querySelectorAll(s)].pop();if(!e)return null;const r=e.getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+Math.min(r.height/2,12)}}", sel)
    if not at:
        return False
    p.click(at['x'], at['y'], 300)
    p.pg.keyboard.type(text, delay=20); p.w(800)
    return True


def scen_mig(br):
    O = (load_pages(BASED) if QJ.GATE else O_FROZEN); N = load_pages(NEWD)
    if QJ.GATE:
        base_src = git('show', BASE_REV + ':jo/index.html').decode('utf-8')
    new_src = io.open(NEWF, encoding='utf-8').read()
    FX = {}
    # ① 바탕 판에서 기록 만들기
    if QJ.GATE:
        p = P(br, 'chromium', 'BASE', base_src, 1440, 900, 'base')
        pre = '옮기기 픽스처(바탕 4be73ca) — '
        try:
            p.ev("__HR.boot()")
            opener = "()=>{const c=viewCanvas._cv();const p=c.D.pages[%d];const b=p.blocks.find(x=>x.bid==='%s');c.openPop(p,b,'%s',{clientX:320,clientY:160},[]);}"
            ok1 = type_pop(p, opener % (2, '3L461', 'memo'), '.cv-pop textarea', '메모461')
            p.ev("()=>closeAllPops()"); p.w(300)
            ok2 = type_pop(p, opener % (2, '3L703', 'memo'), '.cv-pop textarea', '메모703')
            p.ev("()=>closeAllPops()"); p.w(300)
            b8 = next(b for b in O[8]['blocks'] if b['bid'] == '8L42')
            ok3 = type_pop(p, opener % (7, '8L42', 'memo'), '.cv-pop textarea', '메모8L42')
            p.ev("()=>closeAllPops()"); p.w(300)
            p.ev("()=>lsWrite(REC_PRE+'canvaspin',Object.assign(lsRead(REC_PRE+'canvaspin'),{'3L461':{ts:1790000000000}}),'★ 정리캔버스 핀')")
            # 링크 — 3L461 → 「일부청구」 블록 하나 · 8L30 옆 블록 → 8L42(to.key)
            def link(page_i, bid, q, want=None):
                ok = type_pop(p, opener % (page_i, bid, 'link'), '.cv-lfind input', q)
                btn = p.ev("w=>{const bs=[...document.querySelectorAll('.cv-lres button')];const rows=[...document.querySelectorAll('.cv-lres .cv-lrow')];let i=0;"
                           "if(w){i=rows.findIndex(r=>r.textContent.indexOf(w)>=0);if(i<0)return null;const b=rows[i].querySelector('button');if(!b)return null;const r=b.getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2};}"
                           "const b=bs[0];if(!b)return null;const r=b.getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}}", want or '')
                if btn:
                    p.click(btn['x'], btn['y'], 500)
                p.ev("()=>closeAllPops()"); p.w(300)
                return bool(btn)
            t42 = ltxt(O[8]['lines'][b8['ls'][0]])[:8]
            ok4 = link(2, '3L461', '일부청구')
            ok5 = link(7, '8L40', t42)
            # 카드 — 3쪽 빈 곳 두 번 누름 → 글 「C1」 → ✓
            Pg = O[3]
            y = Pg['oy'] + 470
            ex = next(x for x in range(1180, 700, -20) if not any(l['y'] - 8 < y < l['y'] + l['h'] + 8 and l['x'] - 8 < x < l['x1'] + 8 for l in Pg['lines'] if not l.get('del')))
            s = p.ev("a=>__HR.center(a[0],a[1],1.0)", [ex, y])
            p.pg.mouse.dblclick(s['x'], s['y']); p.w(600)
            p.pg.keyboard.type('C1', delay=30); p.w(200)
            okb = p.ev("()=>{const b=document.querySelector('.cv-edtip b[data-k=\"ok\"]');if(!b)return null;const r=b.getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}}")
            if okb:
                p.click(okb['x'], okb['y'], 500)
            # 필기 — 3쪽 줄 셋 곁에 펜 획(✍ 켜고 펜)
            ink_on(p, 'pen')
            strokes = []
            for lid in ('3L461', '3L462', '3L20'):
                l = p.ev("id=>__HR.lineOf(id)", lid)
                s = p.ev("a=>__HR.center(a[0],a[1],1.2)", [l['x'] + min(10, (l['x1'] - l['x']) / 2), l['y'] + l['h'] + 1.2])
                p.mdrag(s['x'] - 30, s['y'], s['x'] + 30, s['y'] + 2, n=8, wait=300)
                strokes.append(lid)
            # 옛 지우개 — 3쪽 선(l) 하나(eraseshape)
            ink_on(p, 'erase')
            L = [s for s in Pg['shapes'] if s['k'] == 'l']
            tgt = None
            for s0 in L:
                mx, my = (s0['x'] + s0['x2']) / 2, (s0['y'] + s0['y2']) / 2
                if any(abs(my - (l['y'] + l['h'] + 1.2)) < 6 for l in Pg['lines'] if l['id'] in ('3L461', '3L462', '3L20')):
                    continue
                tgt = s0; break
            s = p.ev("a=>__HR.center(a[0],a[1],1.2)", [(tgt['x'] + tgt['x2']) / 2, (tgt['y'] + tgt['y2']) / 2])
            p.mdrag(s['x'], s['y'], s['x'] + 2, s['y'] + 1, n=2, wait=400)
            FX = p.ev("__HR.ls()")
            FX['_ops'] = p.ev("__HR.ops()")
            FX['_ink'] = (json.loads(FX['jopangi.canvasink'] or '{}').get('민소') or {}).get('p3') or []
            say(ok1 and ok2 and ok3 and ok4 and ok5 and bool(okb), pre + '메모 3L461·3L703·8L42 · 핀 3L461 · 링크 3L461→ · →8L42 · 카드 · 필기 · 지우개 — 바탕 앱에서 만듦',
                'ops %s · 획 %d · 링크 %s' % ([o['t'] for o in FX['_ops']], len(FX['_ink']), FX['jopangi.canvaslink']))
        except Exception as e:
            say(False, pre + '예외', repr(e)[:300])
            p.close(); return
        finally:
            p.close()
        json.dump(FX, open(os.path.join(WORK, 'mig_fixture.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    else:
        FX = MIG_FX_FROZEN   # regress — 바탕 앱(4be73ca)을 안 띄운다(바탕 띄움 0) · 같은 조작으로 만든 불변 픽스처(위 상수)
    memo0 = json.loads(FX['jopangi.canvasmemo']); link0 = json.loads(FX['jopangi.canvaslink'])
    # ② 새 판 — 기록을 넣고(그림자까지 도장) 다시 연다
    p = P(br, 'chromium', 'NEW', new_src, 1440, 900, 'new')
    pre = '옛 기록 옮기기(새 판) — '
    try:
        for k in ('jopangi.canvas', 'jopangi.canvasink', 'jopangi.canvasmemo', 'jopangi.canvaspin', 'jopangi.canvaslink'):
            if FX.get(k):
                p.ev("a=>__HR.lsSet(a[0],a[1])", [k, FX[k]])
        p.ev("()=>stampAll()")
        g0 = p.ev("__HR.gone()")
        p.load('tok=1&keep=1')
        p.ev("__HR.boot()")
        info = p.ev("__HR.info()")
        memo = p.ev("k=>__HR.lsGet(k)", 'jopangi.canvasmemo'); pin = p.ev("k=>__HR.lsGet(k)", 'jopangi.canvaspin'); link = p.ev("k=>__HR.lsGet(k)", 'jopangi.canvaslink')
        LOG = (p.ev("k=>__HR.lsGet(k)", 'jopangi.canvas') or {}).get('민소') or {}
        say(info['mig'] is not None, pre + 'MIG(옮긴 수)', info['mig'])
        exp = memo0['3L461'] + '\n—\n' + memo0['3L703']
        say(memo.get('3L461') == exp and '3L703' not in memo and memo.get('8L30') == memo0['8L42'] and '8L42' not in memo,
            pre + '메모 3L461+3L703 → 3L461 「새\\n—\\n옛」 · 8L42 → 8L30 · 옛 키 0', {k: v for k, v in memo.items()})
        say('3L461' in pin, pre + '핀 3L461 그대로', pin)
        tos = [(f, l['to'].get('key')) for f, arr in link.items() for l in arr]
        say(all(t not in ('3L703', '8L42') for f, t in tos) and any(f == '3L461' for f, t in tos) and any(t == '8L30' for f, t in tos),
            pre + '링크 — 3L461 에서 나가는 것 그대로 · 8L42 를 가리키던 것 → 8L30', tos)
        say(LOG.get('hash') == info['hash'] and all(o.get('v') == 2 for o in LOG.get('ops', [])) and not any(o['t'] == 'eraseshape' for o in LOG.get('ops', []))
            and info['replay']['bad'] == 0 and not info['replay']['stale'] and not info['stale'],
            pre + '편집 로그 hash = 새 판 · op 전부 v:2 · eraseshape 0 · 재생 못 한 것 0 · 「판이 바뀜」 딱지 없음', 'hash %s · ops %s · replay %s · 딱지 %r' % (LOG.get('hash'), [(o['t'], o.get('v')) for o in LOG.get('ops', [])], info['replay'], info['stale']))
        # 카드 · 획 — 같은 글 옆(가장 가까운 줄과의 거리 차 ≤ 1pt)
        o_card = next(o for o in FX['_ops'] if o['t'] == 'card'); n_card = next(o for o in LOG['ops'] if o['t'] == 'card' and o['id'] == o_card['id'])
        OL = O[3]['lines']; NL = {l['id']: l for l in N[3]['lines']}
        near_o = nearest(OL, o_card['x'], o_card['y'])
        d_new = pt_box(n_card['x'], n_card['y'], NL[near_o[0]])
        near_n = nearest(N[3]['lines'], n_card['x'], n_card['y'])
        say(abs(d_new - near_o[1]) <= 1, pre + '카드 op → 새 판에서 같은 글 옆(옛 판 가장 가까운 줄과의 거리 차 ≤ 1pt)',
            '옛 %s %.2fpt → 새 %.2fpt · 새 판 가장 가까운 줄 %s · y %.2f → %.2f' % (near_o[0], near_o[1], d_new, near_n[0], o_card['y'], n_card['y']))
        ink = ((p.ev("k=>__HR.lsGet(k)", 'jopangi.canvasink') or {}).get('민소') or {}).get('p3') or []
        res = []
        for so, sn in zip(FX['_ink'], ink):
            xo, yo = so['p'][0][0], so['p'][0][1] + O[3]['oy']
            xn, yn = sn['p'][0][0], sn['p'][0][1] + N[3]['oy']
            no = nearest(OL, xo, yo); dn = pt_box(xn, yn, NL[no[0]]); nn = nearest(N[3]['lines'], xn, yn)
            res.append((no[0], round(no[1], 2), round(dn, 2), nn[0], sn.get('v')))
        say(len(ink) == len(FX['_ink']) == 3 and all(abs(a[1] - a[2]) <= 1 and a[4] == 2 for a in res), pre + '필기 획 3 → 같은 글 옆(옛 판 가장 가까운 줄과의 거리 차 ≤ 1pt) · 획마다 v:2',
            '(옛 가장 가까운 줄, 옛 거리, 새 거리, 새 판 가장 가까운 줄, v) %s' % res)
        sd = next((o for o in LOG['ops'] if o['t'] == 'shapedel'), None)
        G = p.ev("n=>__HR.geo(n)", 3)
        say(bool(sd) and any(s['sid'] == sd['sid'] and s['del'] for s in G['shapes']), pre + '옛 eraseshape → shapedel(sk) · 지운 도형이 계속 지워져 있음', sd)
        p.w(4600)
        g1 = p.ev("__HR.gone()")
        say('jopangi.canvasmemo|3L703' in g1 and 'jopangi.canvasmemo|3L703' not in g0, pre + '옛 키는 동기화 묘비로 지움(jopangi_sync_gone)', [k for k in g1 if k.startswith('jopangi.canvas')])
        # 두 번째 로드 — 바뀌는 것 0
        s1 = p.ev("__HR.ls()")
        p.load('tok=1&keep=1'); p.ev("__HR.boot()")
        s2 = p.ev("__HR.ls()"); i2 = p.ev("__HR.info()")
        say(s1 == s2 and not any(i2['mig'][k] for k in i2['mig']), pre + '두 번째 로드 — 기록 바뀜 0 · 옮긴 수 0', i2['mig'])
        say(not p.errs and not p.ev("__HR.errs()") and not [u for u in p.miss if 'omr/민소/' in u], pre + '페이지 오류 0(정리캔버스 데이터 404 포함)', '%s · 404 %s' % (p.errs[:3], sorted(set(p.miss))[:4]))
    except Exception as e:
        say(False, pre + '예외', repr(e)[:300])
    finally:
        p.close()
    # ③ v:2 섞인 로그 — 옛 카드(v 없음)만 옮기고 v:2 카드는 그대로
    p = P(br, 'chromium', 'NEW', new_src, 1440, 900, 'new')
    try:
        o_card = next(o for o in FX['_ops'] if o['t'] == 'card')
        v2 = {'t': 'card', 'n': 3, 'id': '3Nv2test', 'x': 1100.0, 'y': round(N[3]['oy'] + 300.0, 2), 'v': 2, 'ts': 1790000000500}
        p.ev("a=>__HR.lsSet(a[0],a[1])", ['jopangi.canvas', {'민소': {'hash': '94d50c76', 'ops': [dict(o_card), v2]}}])
        p.load('tok=1&keep=1'); p.ev("__HR.boot()")
        L = (p.ev("k=>__HR.lsGet(k)", 'jopangi.canvas') or {}).get('민소') or {}
        a, b = L['ops'][0], L['ops'][1]
        say(L.get('hash') != '94d50c76' and a.get('v') == 2 and abs(a['y'] - o_card['y']) > 0.5 and b['y'] == v2['y'] and b['x'] == v2['x'],
            '옛 기록 옮기기 — v:2 섞인 로그: v 없는 op 만 옮김', 'hash %s · 옛 카드 y %.2f → %.2f · v:2 카드 y %.2f(그대로 %s)' % (L.get('hash'), o_card['y'], a['y'], b['y'], b['y'] == v2['y']))
    except Exception as e:
        say(False, '옛 기록 옮기기 — v:2 섞인 로그 예외', repr(e)[:300])
    finally:
        p.close()


# ══════════ 사용자 실제 기록(G0-5) — 바탕 재생 ↔ 새 판 옮기기 ══════════
SPD = _roots.spd(r'jopangi\기록.json')


def scen_real_regress(br):
    """regress — 사용자 실제 기록(G0-5) 옮기기: NEW 만 돈다(바탕 4be73ca 앱으로 옛 배치에서 재생하던 장면 0). 바탕과 맞대던 칸(재생 ok 수 · 카드 옆 글)은 기준 스냅샷과 맞댄다.
    기록 = 인도 때 studyplandata 고정 커밋(git show 읽기 · 'git:show-data')."""
    REC_REV = 'cf358420'   # A-6(d) 9/30 — 실제 기록 = 인도 때 studyplandata(savedAt 2026-09-23T17:53Z · canvas hash 94d50c76 · op 29 · 옛 배치) · 옛: 지금 클론(9/24 13:08 c845a11c 부터 새 배치 71e49579 로 옮겨져 바탕 재생이 헛돎)
    if not os.path.exists(SPD):
        say(None, '실제 기록 옮기기', 'studyplandata 클론 없음'); return
    QJ.sub('git:show-data')
    _rb = git('show', REC_REV + ':jopangi/기록.json', repo=os.path.dirname(os.path.dirname(SPD)))
    R0 = json.loads(_rb) if _rb else json.load(open(SPD, encoding='utf-8')); d = R0.get('data') or {}
    rec = {k: (d[k] if isinstance(d[k], str) else json.dumps(d[k], ensure_ascii=False)) for k in __import__('itertools').chain(['jopangi.canvas', 'jopangi.canvasink', 'jopangi.canvaslink', 'jopangi.canvasmemo', 'jopangi.canvaspin', 'jopangi.canvasjari']) if k in d}
    LOG0 = json.loads(rec.get('jopangi.canvas', '{}')).get('민소') or {}
    from collections import Counter
    say(None, 'G0-5 실제 기록 census(studyplandata %s · savedAt %s)' % ((REC_REV if _rb else git('rev-parse', '--short', 'HEAD', repo=os.path.dirname(os.path.dirname(SPD))).decode().strip()), R0.get('savedAt')),
        'canvas hash %s · op %d %s · 뒤 조각 id 에 걸린 op %d · 필기 쪽 %d · 링크 %d · 메모 %d · 핀 %d · 손값 %d' % (
            LOG0.get('hash'), len(LOG0.get('ops', [])), dict(Counter(o['t'] for o in LOG0.get('ops', []))),
            sum(1 for o in LOG0.get('ops', []) for f in ('id', 'after', 'bid', 'at', 'sib', 'nbid') if o.get(f) in ('3L109', '3L703', '4L10', '4L16', '4L23', '4L36', '4L108', '8L1', '8L26', '8L42', '8L43', '8L55', '8L149')),
            len(json.loads(rec.get('jopangi.canvasink', '{}')).get('민소') or {}), len(json.loads(rec.get('jopangi.canvaslink', '{}'))),
            len(json.loads(rec.get('jopangi.canvasmemo', '{}'))), len(json.loads(rec.get('jopangi.canvaspin', '{}'))), len(json.loads(rec.get('jopangi.canvasjari', '{}')))))
    out = {}
    for tag, src, dm in (('NEW', io.open(NEWF, encoding='utf-8').read(), 'new'),):
        p = P(br, 'chromium', tag, src, 1440, 900, dm)
        try:
            for k, v in rec.items():
                p.ev("a=>__HR.lsSet(a[0],a[1])", [k, v])
            p.load('tok=1&keep=1'); p.ev("__HR.boot()")
            info = p.ev("__HR.info()")
            cards = p.ev("ids=>{const c=viewCanvas._cv();const out={};for(const p of c.D.pages)for(const l of p.lines)if(ids.includes(l.id))out[l.id]=[p.n,l.x,l.y];return out;}",
                         [o['id'] for o in LOG0.get('ops', []) if o['t'] == 'card'])
            lines = {n: p.ev("n=>__HR.lines(n)", n) for n in sorted({v[0] for v in cards.values()})}
            out[tag] = {'info': info, 'cards': cards, 'lines': lines, 'log': (p.ev("k=>__HR.lsGet(k)", 'jopangi.canvas') or {}).get('민소') or {}, 'errs': p.errs[:3] + p.ev("__HR.errs()")}
        finally:
            p.close()
    n = out['NEW']
    _rp = n['info']['replay']
    _ok = QJ.base('real-replay@chromium/ok', _rp['ok'])   # 기준 칸: 바탕 재생 ok 수 = 기준 스냅샷(스냅샷 없으면 NEW 값 = 첫 기록)
    say(_rp['bad'] == 0 and _rp['ok'] == _ok and not _rp['stale'] and not n['info']['stale'],
        '실제 기록 — 바탕 재생 ↔ 새 판(옮긴 뒤) 재생 · 못 한 것 0 · 「판이 바뀜」 없음', '새 판 %s · MIG %s · 바탕 재생 ok %s(%s)' % (_rp, n['info']['mig'], _ok, QJ.base_note('real-replay@chromium/ok')))
    say(n['log'].get('hash') == n['info']['hash'] and all(o.get('v') == 2 for o in n['log'].get('ops', [])) and len(n['log'].get('ops', [])) == len(LOG0.get('ops', [])),
        '실제 기록 — 편집 로그 hash = 새 판 · op %d 전부 v:2' % len(LOG0.get('ops', [])), n['log'].get('hash'))
    Ln = {pn: [{'id': r[0], 'y': r[1], 'x': r[2], 'x1': r[3], 'h': r[4], 'del': r[5], 'r': [{'t': r[6]}]} for r in n['lines'][pn]] for pn in n['lines']}
    res = []
    for cid in sorted(n['cards']):
        pn, nx, ny = n['cards'][cid]
        nn = nearest(Ln[pn], nx, ny)
        res.append((cid, nn[0], round(nn[1], 2)))
    # 기준 칸: 카드마다 새 판에서 가장 가까운 줄(id · 거리) = 기준 스냅샷 — 옛 판 가장 가까운 줄과 맞대던 것(바탕 앱 재생)을 대신한다
    say(QJ.same('real-card@chromium/res', res) and len(res) == sum(1 for o in LOG0.get('ops', []) if o['t'] == 'card'), '실제 기록 — 카드 %d 모두 같은 글 옆(옛 판 가장 가까운 줄과의 거리 차 ≤ 1pt)' % len(res),
        '새 판 카드 → 가장 가까운 줄 · 거리 %s · 기준 %s' % (res[:5], QJ.base_note('real-card@chromium/res')))
    say(not n['errs'], '실제 기록 — 페이지 오류 0', n['errs'])


def scen_real(br):
    REC_REV = 'cf358420'   # A-6(d) 9/30 — 실제 기록 = 인도 때 studyplandata(savedAt 2026-09-23T17:53Z · canvas hash 94d50c76 · op 29 · 옛 배치) · 옛: 지금 클론(9/24 13:08 c845a11c 부터 새 배치 71e49579 로 옮겨져 바탕 재생이 헛돎)
    if not os.path.exists(SPD):
        say(None, '실제 기록 옮기기', 'studyplandata 클론 없음'); return
    _rb = git('show', REC_REV + ':jopangi/기록.json', repo=os.path.dirname(os.path.dirname(SPD)))
    R0 = json.loads(_rb) if _rb else json.load(open(SPD, encoding='utf-8')); d = R0.get('data') or {}
    rec = {k: (d[k] if isinstance(d[k], str) else json.dumps(d[k], ensure_ascii=False)) for k in __import__('itertools').chain(['jopangi.canvas', 'jopangi.canvasink', 'jopangi.canvaslink', 'jopangi.canvasmemo', 'jopangi.canvaspin', 'jopangi.canvasjari']) if k in d}
    LOG0 = json.loads(rec.get('jopangi.canvas', '{}')).get('민소') or {}
    from collections import Counter
    say(None, 'G0-5 실제 기록 census(studyplandata %s · savedAt %s)' % ((REC_REV if _rb else git('rev-parse', '--short', 'HEAD', repo=os.path.dirname(os.path.dirname(SPD))).decode().strip()), R0.get('savedAt')),
        'canvas hash %s · op %d %s · 뒤 조각 id 에 걸린 op %d · 필기 쪽 %d · 링크 %d · 메모 %d · 핀 %d · 손값 %d' % (
            LOG0.get('hash'), len(LOG0.get('ops', [])), dict(Counter(o['t'] for o in LOG0.get('ops', []))),
            sum(1 for o in LOG0.get('ops', []) for f in ('id', 'after', 'bid', 'at', 'sib', 'nbid') if o.get(f) in ('3L109', '3L703', '4L10', '4L16', '4L23', '4L36', '4L108', '8L1', '8L26', '8L42', '8L43', '8L55', '8L149')),
            len(json.loads(rec.get('jopangi.canvasink', '{}')).get('민소') or {}), len(json.loads(rec.get('jopangi.canvaslink', '{}'))),
            len(json.loads(rec.get('jopangi.canvasmemo', '{}'))), len(json.loads(rec.get('jopangi.canvaspin', '{}'))), len(json.loads(rec.get('jopangi.canvasjari', '{}')))))
    out = {}
    for tag, src, dm in (('BASE', git('show', BASE_REV + ':jo/index.html').decode('utf-8'), 'base'), ('NEW', io.open(NEWF, encoding='utf-8').read(), 'new')):
        p = P(br, 'chromium', tag, src, 1440, 900, dm)
        try:
            for k, v in rec.items():
                p.ev("a=>__HR.lsSet(a[0],a[1])", [k, v])
            p.load('tok=1&keep=1'); p.ev("__HR.boot()")
            info = p.ev("__HR.info()")
            cards = p.ev("ids=>{const c=viewCanvas._cv();const out={};for(const p of c.D.pages)for(const l of p.lines)if(ids.includes(l.id))out[l.id]=[p.n,l.x,l.y];return out;}",
                         [o['id'] for o in LOG0.get('ops', []) if o['t'] == 'card'])
            lines = {n: p.ev("n=>__HR.lines(n)", n) for n in sorted({v[0] for v in cards.values()})}
            out[tag] = {'info': info, 'cards': cards, 'lines': lines, 'log': (p.ev("k=>__HR.lsGet(k)", 'jopangi.canvas') or {}).get('민소') or {}, 'errs': p.errs[:3] + p.ev("__HR.errs()")}
        finally:
            p.close()
    b, n = out['BASE'], out['NEW']
    say(b['info']['replay']['bad'] == 0 and n['info']['replay']['bad'] == 0 and n['info']['replay']['ok'] == b['info']['replay']['ok'] and not n['info']['replay']['stale'] and not n['info']['stale'],
        '실제 기록 — 바탕 재생 ↔ 새 판(옮긴 뒤) 재생 · 못 한 것 0 · 「판이 바뀜」 없음', '바탕 %s · 새 판 %s · MIG %s' % (b['info']['replay'], n['info']['replay'], n['info']['mig']))
    say(n['log'].get('hash') == n['info']['hash'] and all(o.get('v') == 2 for o in n['log'].get('ops', [])) and len(n['log'].get('ops', [])) == len(LOG0.get('ops', [])),
        '실제 기록 — 편집 로그 hash = 새 판 · op %d 전부 v:2' % len(LOG0.get('ops', [])), n['log'].get('hash'))
    res = []
    for cid, (pn, x, y) in b['cards'].items():
        if cid not in n['cards']:
            res.append((cid, None)); continue
        Lb = [{'id': r[0], 'y': r[1], 'x': r[2], 'x1': r[3], 'h': r[4], 'del': r[5], 'r': [{'t': r[6]}]} for r in b['lines'][pn]]
        Ln = [{'id': r[0], 'y': r[1], 'x': r[2], 'x1': r[3], 'h': r[4], 'del': r[5], 'r': [{'t': r[6]}]} for r in n['lines'][pn]]
        nb = nearest(Lb, x, y); nx, ny = n['cards'][cid][1], n['cards'][cid][2]
        nl = {l['id']: l for l in Ln}
        dn = pt_box(nx, ny, nl[nb[0]]) if nb[0] in nl else None
        nn = nearest(Ln, nx, ny)
        res.append((cid, nb[0], round(nb[1], 2), None if dn is None else round(dn, 2), nn[0]))
    bad = [r for r in res if r[1] is None or r[3] is None or abs(r[2] - r[3]) > 1]
    same = sum(1 for r in res if r[1] is not None and r[1] == r[4])
    say(not bad and len(res) == sum(1 for o in LOG0.get('ops', []) if o['t'] == 'card'), '실제 기록 — 카드 %d 모두 같은 글 옆(옛 판 가장 가까운 줄과의 거리 차 ≤ 1pt)' % len(res),
        '어긋남 %d %s · 거리 차 최대 %.2f · (참고) 새 판 가장 가까운 줄도 같음 %d/%d' % (len(bad), bad[:5], max([abs(r[2] - r[3]) for r in res if r[3] is not None] or [0]), same, len(res)))
    say(not b['errs'] and not n['errs'], '실제 기록 — 페이지 오류 0', (b['errs'], n['errs']))


# ══════════ 결과 ══════════
def write_result():
    npass = sum(1 for r in RES if r[0] == 'PASS'); nfail = sum(1 for r in RES if r[0] == 'FAIL')
    b = open(NEWF, 'rb').read()
    head = ['# _harness_jo_ms_canvas_relayout — %s' % time.strftime('%m-%d %H:%M'),
            '# NEW %s · %d B · md5(LF) %s' % (NEWF, len(b), hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest()),
            '# BASE genie %s(md5 %s) + 그 판 데이터 · PASS %d · FAIL %d · INFO %d' % (BASE_REV, BASE_MD5[:8], npass, nfail, len(RES) - npass - nfail), '']
    body = ['%s | %s | %s' % (r[0], r[1], r[2]) for r in RES]
    wr_n(os.path.join(OUT, '_harness_jo_ms_canvas_relayout_result.txt'), ('\n'.join(head + body) + '\n').encode('utf-8'))
    json.dump(RES, open(os.path.join(WORK, 'res.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print('PASS', npass, 'FAIL', nfail)


def main():
    os.makedirs(WORK, exist_ok=True)
    open(os.path.join(WORK, 'nope.json'), 'w').write('')
    if '--report' in sys.argv:
        RES.extend(json.load(open(os.path.join(WORK, 'res.json'), encoding='utf-8'))); write_result(); return
    if QJ.GATE:
        base_data()
        b = git('show', BASE_REV + ':jo/index.html')
        assert hashlib.md5(b).hexdigest() == BASE_MD5
        base_src = b.decode('utf-8')
    else:
        base_src = ''   # regress — 바탕 앱 · 바탕 데이터(4be73ca) 풀기 0(git show 안 부름)
    new_src = io.open(NEWF, encoding='utf-8').read()
    want = lambda k: not ONLY or k in ONLY
    if want('data') and not QJ.SMOKE:   # smoke — 자료 칸은 안 잰다
        if QJ.GATE:
            scen_data()
        else:
            scen_data_regress()
    with sync_playwright() as pw:
        brs = {}
        for eng in ENGS:
            brs[eng] = getattr(pw, eng).launch()
        try:
            if want('eye') and 'chromium' in brs:
                if QJ.GATE:
                    scen_eye(brs['chromium'])
                else:
                    with QJ.stage('eye'):
                        scen_eye_regress(brs['chromium'])
            for eng in ENGS:
                if want('edit'):
                    if QJ.GATE:
                        scen_edit(brs[eng], eng, 'BASE', base_src, 'base')
                    with QJ.stage('edit NEW %s' % eng):
                        scen_edit(brs[eng], eng, 'NEW', new_src, 'new')
                if want('shape') and not QJ.SMOKE:
                    if QJ.GATE:
                        scen_shape(brs[eng], eng, 'BASE', base_src, 'base')
                    with QJ.stage('shape NEW %s' % eng):
                        scen_shape(brs[eng], eng, 'NEW', new_src, 'new')
                if want('pad') and not QJ.SMOKE:
                    with QJ.stage('pad %s' % eng):
                        scen_pad(brs[eng], eng, new_src)
            if want('mig') and 'chromium' in brs and not QJ.SMOKE:
                with QJ.stage('mig'):
                    scen_mig(brs['chromium'])
            if want('real') and 'chromium' in brs and not QJ.SMOKE:
                if QJ.GATE:
                    scen_real(brs['chromium'])
                else:
                    with QJ.stage('real'):
                        scen_real_regress(brs['chromium'])
        finally:
            for x in brs.values():
                x.close()
    write_result()


if __name__ == '__main__':
    main()
