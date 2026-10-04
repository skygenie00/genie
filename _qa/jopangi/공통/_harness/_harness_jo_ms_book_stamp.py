# -*- coding: utf-8 -*-
r"""_task_jo_ms_book_stamp §E 관문 — A 교재 주석본 · B 도장 → 출처 팝업 · C 목차노트 📘 「교재 자리」 · D 폰 손질 둘.

  NEW  = --new <파일>(없으면 genie 작업트리 jo/index.html) · BASE = genie 6b03bf1(md5 12be5019 · 이 판의 바탕 = 교재 창 막대 고침 인도 판)
  데이터 = genie jo/data(이 판의 새 데이터 — omr/민소/note_canvas.json · canvas_match/cand C-0) · BASE·NEW 같은 데이터(헛잣대 규칙 ⑩)
  교재 = 비공개 저장소(zzikkaplan/minbeoppdf) 요청을 페이지 fetch 에서 같은 출처 /__book/ 으로 돌려 로컬 파일을 준다(토큰 없이)
         words·stamp = 클론 <MBPDF_ROOT> · PDF = jopangi\민소\_pdf\ · pdf.js 3.11.174 = %TEMP%\h_gichul\vendor
         datamode 'oldbook' = 책메타만 minbeoppdf HEAD~1(주석본 전 · 9ee99fdc) 것 → 옛 PDF(도장 없음) · 도장 층 pdfMd5 가드
  엔진 = chromium · webkit · 책상 1440×900(마우스) · 아이패드 768×1024(진짜 터치 · DSF 2) · 폰 390×844(진짜 터치) · PC 1890×907 · 1024×768(마우스)
         끌기 = chromium CDP 터치 / webkit 신뢰 마우스(playwright webkit 은 톡만 진짜 터치 — 도구 한계) · 가로 밀기 webkit = 휠(가로)
  잣대 = DOM 실물 · elementFromPoint(누를 수 있는가) · 창(POPS) · 저장소 값 · 교재 요청 길 · 쪽 캔버스 격자 밝기(A — 같은 앱 · 옛 책/새 책)

쓰기 : python _harness_jo_ms_book_stamp.py [--new 파일] [--out 폴더] [--only a|b|c|pad|d] [--eng chromium|webkit] [--report]
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402 — _task_qa_slim(10/4) 실행 모드: --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같다) · regress = NEW 만(바탕 6b03bf1 안 풀고 안 띄움 · 헛잣대 칸 끔 · 바탕 값 칸은 기준 스냅샷 --snap-in/--snap-out) · smoke = 기본 점검 칸만(chromium) · 새 갈래는 모두 `if QJ.REGRESS:` / `if QJ.GATE:` 안
_NR = _roots.need_n('민소 교재 PDF · annot 초안 json(공통/_재료)')   # env_lanes_fix(9/29) — N: 작업 폴더 · 없으면(클라우드) 「N: 필요 — 클라우드 불가(…)」 종료 코드 3
import copy, hashlib, http.server, io, json, os, random, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
CJH = os.path.dirname(os.path.abspath(__file__))   # env_lanes_fix(9/29) — 같은 폴더(N: · genie _qa 같은 모양 · 옛: N: 고정 자리)
sys.path.insert(0, CJH)
import _harness_canvas_jari as CJ          # noqa: E402 — SEED(교재·기록 fetch 돌림) · VENDOR · NOISE · __HJ 도구
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


HERE = os.path.dirname(os.path.abspath(__file__))
OUT = ARG('--out', HERE)
ONLY = ARG('--only', '')
GENIE = CJ.GENIE
JOD = os.path.join(GENIE, 'jo')
NEWF = ARG('--new', os.path.join(JOD, 'index.html'))
BASE_REV, BASE_MD5 = '6b03bf1', '12be5019dd0b473a90b8e21c4a179c51'
WORK = os.path.join(tempfile.gettempdir(), 'h_book_stamp')
MB = _roots.mbpdf()
PDFD = os.path.join(_NR, 'jopangi', '민소', '_pdf')
DRAFT = os.path.join(_NR, 'jopangi', '공통', '_이전', '_annot_add1', 'annot_links_draft.json')
NCEVAL = os.path.join(tempfile.gettempdir(), 'claude', 'N-----claude', 'c33a3f5c-4556-464c-81b5-f1d0315d2cb5', 'scratchpad', 'bs', 'nc_final.json')
TESTS = io.open(os.path.join(HERE, '_harness_jo_ms_book_stamp_tests.js'), encoding='utf-8').read()
IPAD_UA = CJ.IPAD_UA
PHONE_UA = ('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
READY = "!!window.__HB&&!!window.__HJ&&typeof render==='function'&&typeof viewCanvas==='function'"
N131 = '1.3.1.{법정}직사토(보독관)'
N96 = '9.6.{결}정정심판(136)_특무내정정청구(133-2)'
CK = '특기출 24-61-3'
E = {'clientX': 160, 'clientY': 140}
SERVERS = {}


def git(*a, repo=GENIE):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def serve(tag, src, datamode='new'):
    """tag·datamode 마다 서버 하나 — index.html(SEED + __HJ + __HB) · /data/ = genie jo/data · /__book/(words·stamp·pdf) · /__vendor/"""
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
    oldmeta = {}
    if datamode == 'oldbook':
        QJ.sub('git:show-data', 2)   # 옛 책메타 둘(minbeoppdf 9ee99fdc) — 옛 책 장면(A)의 픽스처 · 바탕 앱이 아니다(regress 에서도 읽는다)
        for d in ('minso_hs', 'minso_yg'):
            f = os.path.join(out, 'oldmeta_' + d + '.json')
            open(f, 'wb').write(git('show', '9ee99fdc:words/%s/책메타.json' % d, repo=MB))   # A-6(d) 9/30 — 옛 책메타 = 인도 때 minbeoppdf HEAD~1(주석본 전 · pdfMd5 0ea571a8) · 옛: 'HEAD~1'(9/28 커밋 둘 뒤 726d41e0 = 새 책과 같은 책메타)
            oldmeta[d] = f

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=out, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            if p.startswith('/__vendor/'):
                return os.path.join(CJ.VENDOR, p[len('/__vendor/'):].replace('/', os.sep))
            if p.startswith('/__book/words/'):
                rest = p[len('/__book/words/'):]
                for d, f in oldmeta.items():
                    if rest == d + '/책메타.json':
                        return f
                return os.path.join(MB, 'words', rest.replace('/', os.sep))
            if p.startswith('/__book/stamp/'):
                return os.path.join(MB, 'stamp', p[len('/__book/stamp/'):].replace('/', os.sep))
            if p.startswith('/__book/pdf/'):
                return os.path.join(PDFD, p[len('/__book/pdf/'):])
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
    def __init__(self, br, eng, tag, src, W, H, mode='desk', q='tok=1', datamode='new'):
        self.eng, self.tag, self.mode, self.q = eng, tag, mode, q
        self.pad = mode in ('pad', 'phone')
        QJ.launch('base' if tag == 'BASE' else 'new')   # 셈(§B-4) — 바탕(BASE) 판을 띄운 수 · NEW 를 띄운 수(옛 책 · 캐시 장면도 NEW 앱)
        self.port = serve(tag, src, datamode)
        if mode == 'pad':
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=IPAD_UA)
        elif mode == 'phone':
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=PHONE_UA)
        else:
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1)
        self.ctx.route('**/*', CJ.route_filter)
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(180000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' else None)
        self.cdp = self.ctx.new_cdp_session(self.pg) if (eng == 'chromium' and self.pad) else None
        self.load(q)

    def load(self, q):
        self.q = q
        self.pg.goto('http://127.0.0.1:%d/index.html?%s&who=%s' % (self.port, q, urllib.parse.quote('꼬까')), wait_until='load', timeout=180000)
        self.pg.wait_for_function(READY, timeout=180000)
        self.pg.wait_for_timeout(1200)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def click(self, at, wait=600):
        if not at or not at.get('on'):
            return False
        if self.pad:
            self.pg.touchscreen.tap(at['cx'], at['cy'])
        else:
            self.pg.mouse.click(at['cx'], at['cy'])
        self.pg.wait_for_timeout(wait)
        return True

    def drag(self, x0, y0, x1, y1, n=14):
        if self.cdp:
            def t(ty, x, y):
                self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': ([] if ty == 'touchEnd' else [{'x': x, 'y': y, 'id': 1}])})
            t('touchStart', x0, y0)
            for i in range(1, n + 1):
                t('touchMove', x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.pg.wait_for_timeout(16)
            for _ in range(5):
                t('touchMove', x1, y1); self.pg.wait_for_timeout(30)
            t('touchEnd', x1, y1)
            return 'cdp-touch'
        m = self.pg.mouse
        m.move(x0, y0); m.down()
        for i in range(1, n + 1):
            m.move(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.pg.wait_for_timeout(16)
        m.up()
        return 'mouse(trusted)'

    def shot(self, name):
        if QJ.REGRESS:   # regress — 눈으로 볼 스크린샷은 안 찍는다(판정 칸 아님 · 찍고 0.5초씩 되읽기)
            return 'regress — 안 찍음'
        os.makedirs(os.path.join(OUT, '_book_stamp_shots'), exist_ok=True)
        f = os.path.join(OUT, '_book_stamp_shots', name + '.png')
        try:
            self.pg.screenshot(path=os.path.join(WORK, name + '.png'))
            b = open(os.path.join(WORK, name + '.png'), 'rb').read()
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


# ══════════ 데이터 잣대 ══════════
def ground():
    G = {}
    for d in ('minso_hs', 'minso_yg'):
        S = json.load(open(os.path.join(MB, 'stamp', d + '.json'), encoding='utf-8'))
        by = {}
        for r in S['rows']:
            by.setdefault(r['p'], []).append(r)
        G['st_' + d] = by
        G['md5_' + d] = S['pdfMd5']
        G['meta_' + d] = json.load(open(os.path.join(MB, 'words', d, '책메타.json'), encoding='utf-8'))
        QJ.sub('git:show-data')   # 옛 책메타(minbeoppdf 9ee99fdc) — 캐시 장면이 심는 옛 pdfMd5 · 책메타 대조
        G['old_' + d] = json.loads(git('show', '9ee99fdc:words/%s/책메타.json' % d, repo=MB))   # A-6(d) 9/30 — 옛 책메타 = 인도 때 minbeoppdf HEAD~1(주석본 전 · pdfMd5 0ea571a8) · 옛: 'HEAD~1'(9/28 커밋 둘 뒤 726d41e0 = 새 책과 같은 책메타) · 캐시 장면이 심는 옛 pdfMd5
    hs = G['st_minso_hs']
    G['P61'] = hs[61]
    G['AMB'] = next(p for p in sorted(hs) if any(r['st'] == 'ambig' and len(r.get('cands') or []) >= 2 for r in hs[p]))
    # 초안(add1)에서 unmatched·noocr 만 있고 발행 줄이 없는 핵심 쪽
    Dr = json.load(open(DRAFT, encoding='utf-8'))
    um = {}
    for r in Dr:                                   # 초안 줄 = {book 핵심|윤곽, page(글자), status ok|ambig|unmatched|noocr, …}
        if r.get('book') == '핵심':
            um.setdefault(int(r['page']), []).append(r.get('status'))
    G['UNM'] = next((p for p in sorted(x for x in um if x) if p not in hs and all(s in ('unmatched', 'noocr') for s in um[p])), None)
    G['UNM_n'] = len(um.get(G['UNM'], []))
    G['draft_keys'] = sorted(Dr[0].keys()) if Dr else []
    # 노트·짝
    N = json.load(open(os.path.join(JOD, 'data', 'note_민소.json'), encoding='utf-8'))
    NC = json.load(open(os.path.join(JOD, 'data', 'omr', '민소', 'note_canvas.json'), encoding='utf-8'))
    M = json.load(open(os.path.join(JOD, 'data', 'omr', '민소', 'canvas_match.json'), encoding='utf-8'))
    meta = json.load(open(os.path.join(JOD, 'data', 'omr', '민소', 'canvas_meta.json'), encoding='utf-8'))
    G['NC'], G['M'], G['N'] = NC, M, N
    G['cv_hash'] = meta.get('hash')
    P = NC['p']
    G['e8'] = P[N131]['8']; G['e10'] = P[N131]['10']
    # 칩 줄 기대 — ^id 행 전부 + ^id 없는 문단 끝 중 짝 있는 것
    def expect(f):
        rows = N[f]['행']; pf = P.get(f, {})
        ids = sorted(i for i, r in enumerate(rows) if r.get('id'))
        new = sorted(int(k) for k, v in pf.items() if v['b'] and not rows[int(k)].get('id'))
        return ids, new
    G['expect'] = expect
    rnd = random.Random(20260924)
    pool = sorted(f for f in P if '타임라인' not in f)
    G['NOTES6'] = [N131] + rnd.sample([f for f in pool if f != N131], 5)
    # 층 표본 — 칩이 있는 문단 먼저(^id 거나 짝) · 없으면 아무 문단(창을 바로 연다)
    def chip_ok(f, k):
        return bool(N[f]['행'][int(k)].get('id') or P[f][k]['b'])
    L = {}
    items = [(f, k, v) for f in pool for k, v in sorted(P[f].items(), key=lambda x: int(x[0]))]
    def first(pred):
        a = [x for x in items if pred(x[2]) and chip_ok(x[0], x[1])]
        b = [x for x in items if pred(x[2])]
        x = (a or b or [None])[0]
        return None if x is None else {'f': x[0], 'end': int(x[1]), 'L': x[2]['L'], 'chip': chip_ok(x[0], x[1]), 'c': x[2]['c'], 'b': x[2]['b']}
    top = lambda v, h: any((v['c'].get(bk) or [{}])[0].get('h') == h for bk in ('핵심', '윤곽'))
    L['자동 hi'] = first(lambda v: v['L'] == 'm' and top(v, 'mh'))
    L['자동 lo'] = first(lambda v: v['L'] == 'm' and top(v, 'ml') and not top(v, 'mh'))
    L['후보'] = first(lambda v: v['L'] == 'c')
    L['목차 축'] = first(lambda v: v['L'] == 'toc')
    L['없음'] = first(lambda v: v['L'] == '')
    G['LAYERS'] = L
    # 합치기 픽스처 — 1L46 을 형제 1L42 에 합친다(1L42 가 1L46 줄을 품는다 · 1L46 은 지워진다)
    G['MERGE_INTO'] = '1L42'
    # 표본 30(C-1 표)
    G['S30'] = rnd.sample(items, 30)
    return G


# ══════════ 장면 ══════════
def boot_ms(p, tab='jo'):
    return p.ev("([l,t])=>__HB.law(l,t)", ['민사소송법', tab])


def open_book(p, book, page):
    p.ev("([b,pg,e])=>{viewCanvas.book({book:b,page:pg},e);return true;}", [book, page, E])


def scen_A(br, eng):
    """A — 같은 NEW 앱 · 옛 책(oldbook) / 새 책 · 쪽 61 도장 자리 격자 · 캐시가 옛 pdfMd5 면 새로 받음"""
    R = {'eng': eng}
    G = GR
    rects = [r['rect'] for r in G['P61']] + [[60.0, 40.0, 460.0, 58.0]]   # 마지막 = 대조 칸(도장 없음 · 쪽 아래 여백)
    for dm in ('oldbook', 'new'):
        p = P(br, eng, 'NEW', SRC['NEW'], 1440, 900, 'desk', datamode=dm)
        try:
            boot_ms(p); p.ev("__HB.reqClear()")
            open_book(p, '핵심', 61)
            b = p.ev("([pk,n])=>__HB.bookWait(pk,n,90000)", ['cv|book|minso_hs', 2 if dm == 'new' else None])   # A-6(d) 9/30 — 새 책은 도장 둘이 그려질 때까지 기다림(판 무관 흔들림 · 옛: None = 쪽만 그려지면 잼 · B 장면은 이미 n=2)
            p.pg.wait_for_timeout(1200)
            x = {'book': b, 'painted': p.ev("pk=>__HB.painted(pk,60000)", 'cv|book|minso_hs'), 'req': p.ev("__HB.req()"),
                 'grid': [p.ev("([pk,d,pg,r])=>__HB.grid(pk,d,pg,r,24,4)", ['cv|book|minso_hs', 'minso_hs', 61, r]) for r in rects],
                 'stat': p.ev("d=>__HB.stat(d)", 'minso_hs'), 'errs': [e for e in p.ev("__HB.errs()") + p.errs if not NOISE(e)]}
            if dm == 'new':
                x['shot'] = p.shot('A_%s_hs61' % eng)
            R[dm] = x
        except Exception as e:
            R[dm] = {'exc': repr(e)[:400]}
        finally:
            p.close()
    # 캐시 — 옛 책메타·옛 pdfMd5 가 기기에 있는 채로 연다 → 새로 받음 · 새로 받은 것을 재운 뒤 다시 열면 캐시
    p = P(br, eng, 'NEW', SRC['NEW'], 1440, 900, 'desk')
    try:
        boot_ms(p)
        R['cache0'] = {'meta': p.ev("([d,m])=>__HB.idbSeedMeta(d,m)", ['minso_hs', G['old_minso_hs']]),
                       'pdf': p.ev("([d,m])=>__HB.idbSeedPdf(d,m,4096)", ['minso_hs', G['old_minso_hs']['pdfMd5']])}
        p.load('tok=1&keep=1'); boot_ms(p); p.ev("__HB.reqClear()")
        open_book(p, '핵심', 61)
        b = p.ev("([pk,n])=>__HB.bookWait(pk,n,90000)", ['cv|book|minso_hs', 2])
        R['cache1'] = {'book': {'page': b.get('page'), 'n': len(b.get('stamps') or []), 'err': b.get('err')}, 'stat': p.ev("d=>__HB.stat(d)", 'minso_hs'), 'req': p.ev("__HB.req()")}
        got = None
        for _ in range(120):
            got = p.ev("d=>__HB.idbPdfMd5(d)", 'minso_hs')
            if got and got.get('md5') == G['md5_minso_hs']:
                break
            p.pg.wait_for_timeout(500)
        R['cache1']['idb'] = got
        R['cache1']['stampIdb'] = p.ev("d=>__HB.idbStamp(d)", 'minso_hs')
        p.load('tok=1&keep=1'); boot_ms(p); p.ev("__HB.reqClear()")
        open_book(p, '핵심', 61)
        b = p.ev("([pk,n])=>__HB.bookWait(pk,n,90000)", ['cv|book|minso_hs', 2])
        R['cache2'] = {'book': {'page': b.get('page'), 'n': len(b.get('stamps') or []), 'err': b.get('err')}, 'stat': p.ev("d=>__HB.stat(d)", 'minso_hs'), 'req': p.ev("__HB.req()")}
        R['errs'] = [e for e in p.ev("__HB.errs()") + p.errs if not NOISE(e)]
    except Exception as e:
        R['cexc'] = repr(e)[:400]
    finally:
        p.close()
    return R


def stamp_idx(b, tag):
    for s in (b or {}).get('stamps') or []:
        if s['tag'] == tag:
            return s['i']
    return None


def scen_B(br, eng, tag, mode='desk', W=1440, H=900):
    R = {'eng': eng, 'tag': tag, 'mode': mode}
    G = GR
    p = P(br, eng, tag, SRC[tag], W, H, mode)
    BK = 'cv|book|minso_hs'
    try:
        boot_ms(p)
        open_book(p, '핵심', 61)
        R['b61'] = b = p.ev("([pk,n])=>__HB.bookWait(pk,n,90000)", [BK, 2 if tag == 'NEW' else None])
        R['pops0'] = p.ev("__HB.pops()")
        if QJ.SMOKE:   # smoke — 핵심 61 도장 둘 · 콘솔 오류 0 까지만(누름 · 출처 창 · ambig · 판례탭은 안 잰다)
            R['errs'] = [e for e in p.ev("__HB.errs()") + p.errs if not NOISE(e)]
            return R
        # 76 누름 → 출처 새 팝업
        i76 = stamp_idx(b, '↗ 핵심 p.76')
        at = p.ev("([pk,i])=>__HB.stampAt(pk,i)", [BK, i76]) if i76 is not None else None
        R['at76'] = at
        R['tap76'] = p.click(at, 900)
        SRC76 = 'cv|src|minso_hs|76'
        R['src76'] = p.ev("([pk,n])=>__HB.bookWait(pk,n,60000)", [SRC76, None]) if R['tap76'] else None
        R['pops1'] = p.ev("__HB.pops()")
        R['b61_after'] = p.ev("pk=>__HB.book(pk)", BK)
        R['H76'] = p.ev("([d,pg])=>__HB.pageView(d,pg)", ['minso_hs', 76]) if tag == 'NEW' else None
        if R['src76'] and mode == 'desk':
            R['shot76'] = p.shot('B_%s_%s_src76' % (tag, eng))
        # 출처 창의 도장도 같은 규칙으로 누른다(76 = ambig 쪽 → 후보 목록)
        if R['src76'] and tag == 'NEW' and (R['src76'].get('stamps') or []):
            before = p.ev("__HB.pops()")
            at = p.ev("([pk,i])=>__HB.stampAt(pk,i)", [SRC76, 0]); R['s76at'] = at; R['s76tap'] = p.click(at, 900)
            R['s76pops'] = [x for x in p.ev("__HB.pops()") if x not in before]
            for pk in R['s76pops']:
                p.ev("pk=>__HB.close(pk)", pk)
        # 출처 창 ▶ — 다음 쪽 · 그 쪽 도장도
        if R['src76']:
            at = p.ev("([pk,w])=>__HB.navAt(pk,w)", [SRC76, 'nx']); R['nxAt'] = at; p.click(at, 900)
            R['src77'] = p.ev("([pk,n])=>__HB.bookWait(pk,n,60000)", [SRC76, None])
            at = p.ev("([pk,w])=>__HB.navAt(pk,w)", [SRC76, 'pv']); p.click(at, 900)
            R['src76b'] = p.ev("([pk,n])=>__HB.bookWait(pk,n,60000)", [SRC76, None])
        # 같은 도장 다시 → 출처 팝업 닫힘
        at = p.ev("([pk,i])=>__HB.stampAt(pk,i)", [BK, i76]) if i76 is not None else None
        R['tap76b'] = p.click(at, 700)
        R['pops2'] = p.ev("__HB.pops()")
        # 다른 책 — 윤곽 p.47
        i47 = stamp_idx(b, '↗ 윤곽 p.47')
        at = p.ev("([pk,i])=>__HB.stampAt(pk,i)", [BK, i47]) if i47 is not None else None
        R['tap47'] = p.click(at, 900)
        SRC47 = 'cv|src|minso_yg|47'
        R['src47'] = p.ev("([pk,n])=>__HB.bookWait(pk,n,60000)", [SRC47, None]) if R['tap47'] else None
        R['H47'] = p.ev("([d,pg])=>__HB.pageView(d,pg)", ['minso_yg', 47]) if (tag == 'NEW' and R['src47']) else None
        p.ev("pk=>__HB.close(pk)", SRC47)
        # ambig — 같은 교재 창을 그 쪽으로(교재마다 하나 · 새 자리로 돌린다)
        open_book(p, '핵심', G['AMB'])
        R['bamb'] = b2 = p.ev("([pk,n])=>__HB.bookWait(pk,n,60000)", [BK, 1 if tag == 'NEW' else None])
        ia = next((s['i'] for s in (b2 or {}).get('stamps') or [] if s['st'] == 'ambig'), None)
        R['ia'] = ia
        at = p.ev("([pk,i])=>__HB.stampAt(pk,i)", [BK, ia]) if ia is not None else None
        R['tapAmb'] = p.click(at, 800)
        CPK = 'cv|cand|minso_hs|%d|%s' % (G['AMB'], ia)
        R['cand'] = p.ev("pk=>__HB.candRows(pk)", CPK)
        if R['cand']:
            at = p.ev("([pk,i])=>__HB.candAt(pk,i)", [CPK, 0]); R['candTap'] = p.click(at, 900)
            c0 = R['cand'][0]
            d0 = 'minso_hs' if c0['book'] == '핵심' else 'minso_yg'
            R['candSrc'] = p.ev("([pk,n])=>__HB.bookWait(pk,n,60000)", ['cv|src|%s|%d' % (d0, c0['p']), None])
        R['popsAmb'] = p.ev("__HB.pops()")
        p.ev("__HB.closeAll()")
        # unmatched 쪽 — 테두리 0
        if G['UNM']:
            open_book(p, '핵심', G['UNM'])
            R['bunm'] = p.ev("([pk,n])=>__HB.bookWait(pk,n,60000)", [BK, None])
        p.ev("__HB.closeAll()")
        # 판례탭 책 칩 창
        p.ev("()=>{S.law='민사소송법';S.tab='prec';S.prec='66마322';render();return true;}")
        p.pg.wait_for_timeout(1500)
        at = p.ev("t=>__HB.bkgoAt(t)", '핵심 p.61'); R['bkAt'] = at
        R['bkTap'] = p.click(at, 900)
        R['bprec'] = p.ev("([pk,n])=>__HB.bookWait(pk,n,90000)", [BK, 2 if tag == 'NEW' else None]) if R['bkTap'] else None
        if R['bprec'] and tag == 'NEW':
            i76 = stamp_idx(R['bprec'], '↗ 핵심 p.76')
            at = p.ev("([pk,i])=>__HB.stampAt(pk,i)", [BK, i76]) if i76 is not None else None
            R['prec76'] = p.click(at, 900)
            R['prec76w'] = p.ev("([pk,n])=>__HB.bookWait(pk,n,60000)", [SRC76, None]) if R['prec76'] else None
        R['errs'] = [e for e in p.ev("__HB.errs()") + p.errs if not NOISE(e)]
    except Exception as e:
        R['exc'] = repr(e)[:500]
    finally:
        p.close()
    return R


def scen_C(br, eng, tag, mode='desk', W=1440, H=900):
    R = {'eng': eng, 'tag': tag, 'mode': mode}
    G = GR
    p = P(br, eng, tag, SRC[tag], W, H, mode)
    try:
        boot_ms(p)
        R['note'] = p.ev("f=>__HB.note(f)", N131)
        R['grey'] = p.ev("__HB.greyRef()")
        if QJ.SMOKE:   # smoke — 1.3.1 칩 줄 · 📘 한 칸까지만(창 · 교재 · 합치기는 안 잰다)
            return R
        at = p.ev("([f,r,t])=>__HB.chipAt(f,r,t)", [N131, 8, '📘']); R['chip8'] = at
        R['tap8'] = p.click(at, 900)
        R['w8'] = p.ev("([f,e])=>__HB.ncbWait(f,e,90000)", [N131, 8]) if R['tap8'] else None
        if R['w8'] and mode == 'desk':
            R['shot8'] = p.shot('C_%s_%s_w8' % (tag, eng))
        if R['w8']:
            # 「후보 N」 펴기
            at = p.ev("([f,e,w,i])=>__HB.ncbAt(f,e,w,i)", [N131, 8, 'more', 0]); R['moreTap'] = p.click(at, 500)
            R['w8b'] = p.ev("([f,e])=>__HB.ncb(f,e)", [N131, 8])
            # 교재 줄 누름 → 교재 쪽 창 강조 · 블록 ctx(✓ 이 자리 · 📍 찍기)
            at = p.ev("([f,e,w,i])=>__HB.ncbAt(f,e,w,i)", [N131, 8, 'row', 0]); R['rowAt'] = at
            R['rowTap'] = p.click(at, 900)
            R['book'] = p.ev("([pk,n])=>__HB.bookWait(pk,n,90000)", ['cv|book|minso_hs', None])
            p.ev("pk=>__HB.close(pk)", 'cv|book|minso_hs')
            # 캔버스 줄 누름 → 정리 탭 그 블록
            at = p.ev("([f,e,w,i])=>__HB.ncbAt(f,e,w,i)", [N131, 8, 'bid', '1L46']); R['cvAt'] = at
            R['cvTap'] = p.click(at, 900)
            R['canvas'] = p.ev("([b,ms])=>__HB.canvasWait(b,ms)", ['1L46', 40000])
            if mode == 'desk':
                R['shotCv'] = p.shot('C_%s_%s_canvas' % (tag, eng))
        # 같은 📘 두 번 = 닫힘
        boot_ms(p); p.ev("f=>__HB.note(f)", N131)
        at = p.ev("([f,r,t])=>__HB.chipAt(f,r,t)", [N131, 10, '📘']); t1 = p.click(at, 900)
        w1 = p.ev("([f,e])=>__HB.ncbWait(f,e,60000)", [N131, 10]) if t1 else None
        at = p.ev("([f,r,t])=>__HB.chipAt(f,r,t)", [N131, 10, '📘']); t2 = p.click(at, 700)
        R['toggle'] = {'t1': t1, 'w1': bool(w1 and w1.get('open')), 't2': t2, 'after': p.ev("([f,e])=>__HB.ncb(f,e)", [N131, 10])}
        if tag == 'NEW' and mode == 'desk':
            # 특허 노트 — 📍 그대로
            p.ev("([l,t])=>__HB.law(l,t)", ['특허법', 'jo'])
            R['n96'] = p.ev("f=>__HB.note(f)", N96)
            boot_ms(p)
            # 층 표본 다섯
            R['layers'] = {}
            for nm, s in G['LAYERS'].items():
                if not s:
                    R['layers'][nm] = None
                    continue
                p.ev("__HB.closeAll()")
                how = 'chip'
                if s['chip']:
                    p.ev("f=>__HB.note(f)", s['f'])
                    at = p.ev("([f,r,t])=>__HB.chipAt(f,r,t)", [s['f'], s['end'], '📘'])
                    if not p.click(at, 900):
                        how = 'direct'
                        p.ev("([f,e])=>__HB.ncbOpen(f,e)", [s['f'], s['end']])
                else:
                    how = 'direct'
                    p.ev("([f,e])=>__HB.ncbOpen(f,e)", [s['f'], s['end']])
                w = p.ev("([f,e])=>__HB.ncbWait(f,e,60000)", [s['f'], s['end']])
                R['layers'][nm] = {'s': {k: s[k] for k in ('f', 'end', 'L', 'chip')}, 'how': how, 'w': w}
            # 짝 없는 문단 칩 줄 — 노트 여섯
            R['notes6'] = {}
            for f in G['NOTES6']:
                ni = p.ev("f=>__HB.note(f)", f)
                R['notes6'][f] = [x['i'] for x in (ni or {}).get('tbl') or []]
            # 손값 픽스처 → 그 자리 하나 + 그림 + 되돌리기
            p.ev("__HB.closeAll()")
            HV = {'1L46': {'by': 'hand', 'b': '핵심', 'p': 62, 'r': [0.12, 0.30, 0.88, 0.36], 't': 1790000000001, 'who': '꼬까PC'}}
            p.ev("([k,v])=>__HB.lsSet(k,v)", ['jopangi.canvasjari', HV])
            p.ev("f=>__HB.note(f)", N131)
            at = p.ev("([f,r,t])=>__HB.chipAt(f,r,t)", [N131, 8, '📘']); p.click(at, 900)
            R['hand'] = p.ev("([f,e])=>__HB.ncbWait(f,e,60000)", [N131, 8])
            R['handPic'] = p.ev("([f,e])=>__HB.picWait(f,e,60000)", [N131, 8])
            R['shotHand'] = p.shot('C_%s_%s_hand' % (tag, eng))
            rv = next((i for i, t in enumerate((R['hand'] or {}).get('more') or []) if t == '자동으로 되돌리기'), None)
            at = p.ev("([f,e,w,i])=>__HB.ncbAt(f,e,w,i)", [N131, 8, 'more', rv]) if rv is not None else None
            R['rvTap'] = p.click(at, 1200)
            R['afterRv'] = {'kv': (p.ev("k=>__HB.ls(k)", 'jopangi.canvasjari') or {}).get('1L46'), 'w': p.ev("([f,e])=>__HB.ncbWait(f,e,30000)", [N131, 8]),
                            'state': p.ev("k=>__HB.jstate(k)", '1L46')}
        R['errs'] = [e for e in p.ev("__HB.errs()") + p.errs if not NOISE(e)]
    except Exception as e:
        R['exc'] = repr(e)[:500]
    finally:
        p.close()
    if tag == 'NEW' and mode == 'desk':
        # 합치기 편집 로그 — 1L46 을 1L42 에 합친 채 연다
        p = P(br, eng, tag, SRC[tag], W, H, mode)
        try:
            op = {'t': 'merge', 'bid': G['MERGE_INTO'], 'sib': '1L46', 'ts': 1790000000000}
            p.ev("([k,v])=>__HB.lsSet(k,v)", ['jopangi.canvas', {'민소': {'hash': G['cv_hash'], 'ops': [op]}}])
            p.load('tok=1&keep=1'); boot_ms(p)
            p.ev("f=>__HB.note(f)", N131)
            at = p.ev("([f,r,t])=>__HB.chipAt(f,r,t)", [N131, 8, '📘']); p.click(at, 900)
            R['merge'] = p.ev("([f,e])=>__HB.ncbWait(f,e,90000)", [N131, 8])
            R['mergeErrs'] = [e for e in p.ev("__HB.errs()") + p.errs if not NOISE(e)]
        except Exception as e:
            R['mexc'] = repr(e)[:400]
        finally:
            p.close()
    return R


def scen_pad(br, eng, tag):
    """아이패드 진짜 터치 — B(도장 톡 → 출처 · 다시 톡 → 닫힘) · C(📘 톡 → 창 · 줄 톡 → 교재 · 캔버스 줄 톡 → 정리 탭)"""
    R = {'eng': eng, 'tag': tag}
    p = P(br, eng, tag, SRC[tag], 768, 1024, 'pad')
    BK = 'cv|book|minso_hs'
    try:
        boot_ms(p)
        open_book(p, '핵심', 61)
        b = p.ev("([pk,n])=>__HB.bookWait(pk,n,90000)", [BK, 2 if tag == 'NEW' else None]); R['b61'] = {'n': len(b.get('stamps') or []), 'page': b.get('page')}
        i76 = stamp_idx(b, '↗ 핵심 p.76')
        at = p.ev("([pk,i])=>__HB.stampAt(pk,i)", [BK, i76]) if i76 is not None else None
        R['at76'] = at; R['tap76'] = p.click(at, 900)
        w = p.ev("([pk,n])=>__HB.bookWait(pk,n,60000)", ['cv|src|minso_hs|76', None]) if R['tap76'] else None
        R['src76'] = {'page': w.get('page'), 'band': w.get('band')} if w else None
        at = p.ev("([pk,i])=>__HB.stampAt(pk,i)", [BK, i76]) if i76 is not None else None
        R['tap76b'] = p.click(at, 700); R['pops2'] = p.ev("__HB.pops()")
        p.ev("__HB.closeAll()")
        p.ev("f=>__HB.note(f)", N131)
        at = p.ev("([f,r,t])=>__HB.chipAt(f,r,t)", [N131, 8, '📘']); R['chip8'] = at; R['tap8'] = p.click(at, 900)
        w8 = p.ev("([f,e])=>__HB.ncbWait(f,e,90000)", [N131, 8]) if R['tap8'] else None
        R['w8'] = {'rows': (w8 or {}).get('rows'), 'rect': (w8 or {}).get('rect')} if w8 else None
        if w8:
            at = p.ev("([f,e,w,i])=>__HB.ncbAt(f,e,w,i)", [N131, 8, 'row', 0]); R['rowTap'] = p.click(at, 900)
            bb = p.ev("([pk,n])=>__HB.bookWait(pk,n,90000)", [BK, None]); R['book'] = {'page': bb.get('page'), 'hl': bb.get('hl'), 'ok': bb.get('okBtn'), 'pk': bb.get('pkBtn')} if bb else None
            p.ev("pk=>__HB.close(pk)", BK)
            at = p.ev("([f,e,w,i])=>__HB.ncbAt(f,e,w,i)", [N131, 8, 'bid', '1L46']); R['cvTap'] = p.click(at, 900)
            R['canvas'] = p.ev("([b,ms])=>__HB.canvasWait(b,ms)", ['1L46', 40000])
        R['errs'] = [e for e in p.ev("__HB.errs()") + p.errs if not NOISE(e)]
    except Exception as e:
        R['exc'] = repr(e)[:500]
    finally:
        p.close()
    return R


def scen_D(br, eng, tag, br_sb=None):
    """폰 390×844 — #hrail 스크롤 줄 · 가로 밀기 · 기억 없는 카드 손잡이 +150 · 기억 크기로 다시 열기 / PC 1890×907 · 1024×768 — 바탕과 같음"""
    R = {'eng': eng, 'tag': tag}
    p = P(br, eng, tag, SRC[tag], 390, 844, 'phone')
    try:
        p.ev("([l,t])=>__HB.law(l,t)", ['특허법', 'cha2'])
        R['rail0'] = p.ev("__HB.rail()")
        r = R['rail0'] or {}
        if r.get('rect'):
            y = r['rect']['cy']; x0 = r['rect']['x'] + r['rect']['w'] * 0.8; x1 = r['rect']['x'] + r['rect']['w'] * 0.2
            if p.cdp:
                R['swipe'] = p.drag(x0, y, x1, y, 10)
            else:
                R['swipe'] = None   # 모바일 WebKit — 휠·끌기 불가(도구 한계) · 아래 모바일 아닌 390 창의 가로 휠로 잰다
            p.pg.wait_for_timeout(600)
        R['rail1'] = p.ev("__HB.rail()")
        # 기억 없는 카드 — 손잡이 +150
        R['card0'] = p.ev("([c,x,y])=>__HB.card(c,x,y)", [CK, 30, 90])
        at = p.ev("pk=>__HB.rszAt(pk)", (R['card0'] or {}).get('pk')); R['rszAt'] = at
        if at and at.get('on'):
            R['rszHow'] = p.drag(at['cx'], at['cy'], at['cx'], at['cy'] + 150, 12)
            p.pg.wait_for_timeout(500)
        R['card1'] = p.ev("pk=>__HB.popInfo(pk)", (R['card0'] or {}).get('pk'))
        R['cfg'] = p.ev("k=>__HB.cfg(k)", 'list')
        R['vv'] = p.ev("__HB.vv()")
        # 기억 크기로 다시 열기 — 60vh(506) 보다 큰 기억 656 을 심고 연다(바탕은 끌어도 506 이라 끈 기억으로는 갈리지 않는다)
        R['cfgSeed'] = {'w': 374, 'h': 656, 'x': 8, 'y': 104}
        p.ev("([k,v])=>__HB.cfgSet(k,v)", ['list', R['cfgSeed']])
        R['card2'] = p.ev("([c,x,y])=>__HB.card(c,x,y)", [CK, 30, 90])
        # 「교재 자리」 창이 폰 화면 안
        boot_ms(p); p.ev("f=>__HB.note(f)", N131)
        at = p.ev("([f,r,t])=>__HB.chipAt(f,r,t)", [N131, 8, '📘']); R['chip8'] = at
        if p.click(at, 900):
            w = p.ev("([f,e])=>__HB.ncbWait(f,e,90000)", [N131, 8]); R['w8'] = {'rect': (w or {}).get('rect'), 'rows': len((w or {}).get('rows') or [])} if w else None
            if tag == 'NEW':
                R['shot'] = p.shot('D_%s_%s_phone_w8' % (tag, eng))
        R['errs'] = [e for e in p.ev("__HB.errs()") + p.errs if not NOISE(e)]
    except Exception as e:
        R['exc'] = repr(e)[:500]
    finally:
        p.close()
    # 모바일 아닌 390×844 창(자리 차지 스크롤바) — #hrail 스크롤바 두께(크로미움 = --hide-scrollbars 를 뺀 브라우저)
    p = P(br_sb or br, eng, tag, SRC[tag], 390, 844, 'desk')
    try:
        p.ev("([l,t])=>__HB.law(l,t)", ['특허법', 'cha2'])
        R['raild'] = rd = p.ev("__HB.rail()")
        if rd and rd.get('rect'):
            p.pg.mouse.move(rd['rect']['cx'], rd['rect']['cy']); p.pg.mouse.wheel(260, 0); p.pg.wait_for_timeout(600)
        R['raild1'] = p.ev("__HB.rail()")
    except Exception as e:
        R['raild'] = {'exc': repr(e)[:300]}
    finally:
        p.close()
    for W, H in ((1890, 907), (1024, 768)):
        p = P(br, eng, tag, SRC[tag], W, H, 'desk')
        k = 'pc%d' % W
        try:
            p.ev("([l,t])=>__HB.law(l,t)", ['특허법', 'cha2'])
            x = {'card0': p.ev("([c,x,y])=>__HB.card(c,x,y)", [CK, 200, 150])}
            at = p.ev("pk=>__HB.rszAt(pk)", (x['card0'] or {}).get('pk'))
            if at and at.get('on'):
                p.drag(at['cx'], at['cy'], at['cx'], at['cy'] + 150, 12); p.pg.wait_for_timeout(400)
            x['card1'] = p.ev("pk=>__HB.popInfo(pk)", (x['card0'] or {}).get('pk'))
            x['card2'] = p.ev("([c,x,y])=>__HB.card(c,x,y)", [CK, 200, 150])
            x['rail'] = p.ev("__HB.rail()")
            boot_ms(p)
            x['note'] = (p.ev("f=>__HB.note(f)", N131) or {}).get('rect')
            x['errs'] = [e for e in p.ev("__HB.errs()") + p.errs if not NOISE(e)]
            R[k] = x
        except Exception as e:
            R[k] = {'exc': repr(e)[:400]}
        finally:
            p.close()
    return R


def NOISE(x):
    return CJ.NOISE(x)


# ══════════ 판정 ══════════
L, CNT, NULL = [], {'PASS': 0, 'FAIL': 0}, {}


def T(name, ok, info=None, tag='NEW'):
    ok = bool(ok)
    if tag == 'BASE':
        NULL.setdefault(name, []).append(ok)
        return
    CNT['PASS' if ok else 'FAIL'] += 1
    L.append('%s | %s%s' % ('PASS' if ok else 'FAIL', name, '' if ok else ' | ' + json.dumps(info, ensure_ascii=False, default=str)[:700]))


def I(name, v):
    L.append('INFO | %s | %s' % (name, v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)[:900]))


def near(a, b, tol):
    return a is not None and b is not None and abs(a - b) <= tol


def gates_A(R):
    G = GR
    pre = '[A %s] ' % R['eng']
    o, n = R.get('oldbook') or {}, R.get('new') or {}
    if o.get('exc') or n.get('exc'):
        T(pre + '옛 책·새 책 교재 창', False, [o.get('exc'), n.get('exc')])
        return
    T(pre + '새 책 = 주석본 앱판 PDF 를 받는다(요청 길)', any(x.endswith('26핵심민소ABBYY_주석_앱.pdf') for x in n.get('req') or []), n.get('req'))
    T(pre + '옛 책(바탕 데이터) = 옛 PDF 를 받는다(헛잣대 — 요청 길이 갈린다)', any(x.endswith('26핵심민소ABBYY.pdf') for x in o.get('req') or []), o.get('req'))
    T(pre + '옛 책 쪽 61 — 도장 상자 0(stamp pdfMd5 ≠ 옛 책메타 → 그리지 않는다)', len((o.get('book') or {}).get('stamps') or []) == 0, (o.get('book') or {}).get('stamps'))
    T(pre + '새 책 쪽 61 — 도장 상자 2', len((n.get('book') or {}).get('stamps') or []) == 2, (n.get('book') or {}).get('stamps'))
    go, gn = o.get('grid') or [], n.get('grid') or []
    diffs = []
    for k in range(len(gn)):
        a, b = (go[k] or {}).get('g') or [], (gn[k] or {}).get('g') or []
        if len(a) != len(b) or not a:
            diffs.append(None)
            continue
        d = [abs(x - y) for x, y in zip(a, b)]
        diffs.append({'mean': round(sum(d) / len(d), 1), 'cells>12': round(sum(1 for v in d if v > 12) / len(d), 2), 'old': round(sum(a) / len(a)), 'new': round(sum(b) / len(b))})
    I(pre + '쪽 61 격자 밝기(24×4) — 도장 자리 둘 · 대조 칸(쪽 아래 여백) · 옛 책 → 새 책', diffs)
    T(pre + '도장 자리 둘 — 새 책 그림이 옛 책과 다르다(칸 평균 차 ≥ 8 · 12 넘게 바뀐 칸 ≥ 20%)',
      all(x and x['mean'] >= 8 and x['cells>12'] >= 0.2 for x in diffs[:2]), diffs)
    T(pre + '대조 칸(도장 없음) — 옛 책·새 책 같다(칸 평균 차 < 3 · 헛잣대)', diffs[-1] is not None and diffs[-1]['mean'] < 3, diffs[-1])
    c1, c2 = R.get('cache1') or {}, R.get('cache2') or {}
    if R.get('cexc'):
        T(pre + '캐시 장면', False, R.get('cexc'))
        return
    T(pre + '기기 캐시가 옛 pdfMd5 → 새로 받음(from net · 주석본 앱판 요청)', (c1.get('stat') or {}).get('from') == 'net' and any(x.endswith('_주석_앱.pdf') for x in c1.get('req') or []), c1)
    T(pre + '새로 받은 것을 재운다(IDB bookpdf pdfMd5 = 새 책메타)', (c1.get('idb') or {}).get('md5') == G['md5_minso_hs'], c1.get('idb'))
    T(pre + '도장 데이터도 재운다(IDB bookstamp · pdfMd5 = 새 책)', (c1.get('stampIdb') or {}).get('md5') == G['md5_minso_hs'] and (c1.get('stampIdb') or {}).get('n', 0) > 1000, c1.get('stampIdb'))
    T(pre + '다시 열면 캐시(from cache · PDF 요청 0 — 헛잣대 대조)', (c2.get('stat') or {}).get('from') == 'cache' and not any(x.endswith('.pdf') for x in c2.get('req') or []) and (c2.get('book') or {}).get('n') == 2, c2)
    T(pre + '콘솔 오류 0', not (n.get('errs') or o.get('errs') or R.get('errs')), [n.get('errs'), o.get('errs'), R.get('errs')])


def gates_B(R, tag):
    G = GR
    pre = '[B %s %s %s] ' % (R['eng'], R['mode'], tag)
    if R.get('exc'):
        T(pre + '장면', False, R.get('exc'), tag)
        return
    b = R.get('b61') or {}
    st = b.get('stamps') or []
    ok = [s for s in st if s['st'] == 'ok']
    T(pre + '핵심 61 — ok 테두리 2 · 꼬리표 「↗ 윤곽 p.47」「↗ 핵심 p.76」', len(ok) == 2 and sorted(s['tag'] for s in ok) == ['↗ 윤곽 p.47', '↗ 핵심 p.76'], st, tag)
    if tag == 'NEW' and ok and QJ.want('B-style'):   # smoke — 테두리 꼴 칸은 안 잰다
        s = ok[0]
        T(pre + '테두리 2px #2563eb · 안 칠 8% · 꼬리표 10.5px 700 흰 글자 파란 바탕',
          s['bw'] == '2px' and s['bc'] == 'rgb(37, 99, 235)' and s['bg'] == 'rgba(37, 99, 235, 0.08)' and (s['tg'] or {}).get('fs') == '10.5px' and (s['tg'] or {}).get('fw') == '700'
          and (s['tg'] or {}).get('c') == 'rgb(255, 255, 255)' and (s['tg'] or {}).get('bg') == 'rgb(37, 99, 235)', s, tag)
        v = [0, 0, 481.89, 680.31]
        exp = {}
        for r in G['P61']:
            x0, y0, x1, y1 = r['rect']
            exp['↗ %s p.%d' % (r['to']['book'], r['to']['p'])] = r['rect']
        I(pre + '도장 자리(%) — 앱 / 데이터 rect', [(s['tag'], s['l'], s['t'], s['w'], s['h'], exp.get(s['tag'])) for s in ok])
    if QJ.SMOKE:   # smoke — 핵심 61 도장 둘 + 콘솔 오류 0 까지만
        T(pre + '콘솔 오류 0', not R.get('errs'), R.get('errs'))
        return
    n0, n1, n2 = len(R.get('pops0') or []), len(R.get('pops1') or []), len(R.get('pops2') or [])
    s76 = R.get('src76') or {}
    T(pre + '76 누름 → 새 팝업 1(POPS +1 · 출처 창 cv|src|minso_hs|76)', R.get('tap76') and n1 == n0 + 1 and 'cv|src|minso_hs|76' in (R.get('pops1') or []), {'at': R.get('at76'), 'p0': R.get('pops0'), 'p1': R.get('pops1')}, tag)
    T(pre + '원래 창 쪽 번호 61 그대로 · 새 창 쪽 76', str((R.get('b61_after') or {}).get('page')) == '61' and str(s76.get('page')) == '76', {'orig': (R.get('b61_after') or {}).get('page'), 'src': s76.get('page')}, tag)
    if tag == 'NEW':
        H76 = R.get('H76') or [0, 0, 0, 1]
        ph = H76[3] - H76[1]
        T(pre + '출처 창 머리 「출처 · 핵심 p.61 도장 「OCR 앞 20자」」', s76.get('title', '').startswith('출처 · 핵심 p.61 도장 「'), s76.get('title'), tag)
        T(pre + '출처 줄 띠 top ≈ 199.6/H(±0.05%) · 폭 84% · 높이 16pt', s76.get('band') and near(s76['band']['t'], 199.6 / ph * 100, 0.05) and near(s76['band']['w'], 84, 0.01) and near(s76['band']['h'], 16 / ph * 100, 0.01),
          {'band': s76.get('band'), 'H': ph, 'want': round(199.6 / ph * 100, 3)}, tag)
        st76 = G['st_minso_hs'].get(76, [])
        s0 = st76[0] if st76 else None
        want = ('cv|cand|minso_hs|76|0' if s0 and s0['st'] == 'ambig' else ('cv|src|%s|%d' % ('minso_hs' if s0['to']['book'] == '핵심' else 'minso_yg', s0['to']['p']) if s0 else None))
        T(pre + '출처 창 76 — 그 쪽 도장 %d(데이터) · 누르면 같은 규칙(%s)' % (len(st76), want), len(s76.get('stamps') or []) == len(st76) and st76 and R.get('s76tap') and R.get('s76pops') == [want],
          {'n': len(s76.get('stamps') or []), 'tap': R.get('s76tap'), 'opened': R.get('s76pops'), 'want': want}, tag)
        s77, s76b = R.get('src77') or {}, R.get('src76b') or {}
        st77 = G['st_minso_hs'].get(77, [])
        T(pre + '출처 창 ▶ → 77쪽 · 그 쪽 도장 수 = 데이터(%d) · ◀ → 76 띠 다시' % len(st77), str(s77.get('page')) == '77' and len(s77.get('stamps') or []) == len(st77) and str(s76b.get('page')) == '76' and s76b.get('band'),
          {'77': [s77.get('page'), len(s77.get('stamps') or [])], '76b': [s76b.get('page'), s76b.get('band')]}, tag)
    T(pre + '같은 도장 다시 → 출처 팝업 닫힘', R.get('tap76b') and 'cv|src|minso_hs|76' not in (R.get('pops2') or []) and n2 == n0, {'p2': R.get('pops2')}, tag)
    s47 = R.get('src47') or {}
    T(pre + '다른 책 도장(윤곽 p.47) → 윤곽 출처 팝업 · 쪽 47', R.get('tap47') and str(s47.get('page')) == '47' and (s47.get('pk') == 'cv|src|minso_yg|47'), {'tap': R.get('tap47'), 'w': {k: s47.get(k) for k in ('pk', 'page', 'title', 'band')}}, tag)
    if tag == 'NEW' and R.get('H47'):
        ph = R['H47'][3] - R['H47'][1]
        T(pre + '윤곽 출처 띠 top ≈ 73.1/H', s47.get('band') and near(s47['band']['t'], 73.1 / ph * 100, 0.05), {'band': s47.get('band'), 'want': round(73.1 / ph * 100, 3)}, tag)
    amb = [r for r in G['st_minso_hs'][G['AMB']] if r['st'] == 'ambig']
    cand = R.get('cand') or []
    exp = amb[0]['cands'] if amb else []
    T(pre + 'ambig 누름(핵심 %d) → 후보 목록(줄 = 데이터 cands %d · 「핵심 p.N」 꼴)' % (G['AMB'], len(exp)),
      R.get('tapAmb') and len(cand) == len(exp) and all(c['t'] == '%s p.%d' % (x['book'], x['p']) for c, x in zip(cand, exp)), {'cand': cand, 'exp': exp, 'tagAmb': [s['tag'] for s in (R.get('bamb') or {}).get('stamps') or [] if s['st'] == 'ambig']}, tag)
    cs = R.get('candSrc') or {}
    T(pre + '후보 줄 누름 → 출처 팝업(그 쪽)', cand and str(cs.get('page')) == str(cand[0]['p']), {'tap': R.get('candTap'), 'page': cs.get('page'), 'pk': cs.get('pk')}, tag)
    if G['UNM']:
        T(pre + 'unmatched 쪽(핵심 %d · 초안 %d줄 · 발행 0) → 테두리 0' % (G['UNM'], G['UNM_n']), R.get('bunm') and len((R.get('bunm') or {}).get('stamps') or []) == 0 and str((R.get('bunm') or {}).get('page')) == str(G['UNM']), (R.get('bunm') or {}).get('stamps'), tag)
    bp = R.get('bprec') or {}
    okp = [s for s in bp.get('stamps') or [] if s['st'] == 'ok']
    T(pre + '판례탭 책 칩(66마322 · 핵심 p.61) 창 — ok 2 · 꼬리표 같음', R.get('bkTap') and sorted(s['tag'] for s in okp) == ['↗ 윤곽 p.47', '↗ 핵심 p.76'], {'at': R.get('bkAt'), 'st': bp.get('stamps')}, tag)
    if tag == 'NEW':
        pw = R.get('prec76w') or {}
        T(pre + '판례탭 창에서도 76 누름 → 출처 팝업 76', R.get('prec76') and str(pw.get('page')) == '76' and pw.get('band'), {'tap': R.get('prec76'), 'page': pw.get('page')}, tag)
        T(pre + '콘솔 오류 0', not R.get('errs'), R.get('errs'))


BADW = ['자동 자리', '확신', '점수', '단원 범위', '본문 겹침', '층', 'mh', 'ml', 'toc', ' sc', '1등', '순위']


def win_clean(w):
    t = (w or {}).get('text') or ''
    import re
    return [x for x in BADW if x in t] + re.findall(r'\d\.\d{2,}', t)


def gates_C(R, tag):
    G = GR
    pre = '[C %s %s %s] ' % (R['eng'], R['mode'], tag)
    if R.get('exc'):
        T(pre + '장면', False, R.get('exc'), tag)
        return
    nt = R.get('note') or {}
    tb = {x['i']: x['chips'] for x in nt.get('tbl') or []}
    ids, new = G['expect'](N131)
    T(pre + '1.3.1 행 7~8 · 9~10(^id 없음 · 짝 있음) 끝 줄에 칩 줄 + 📘', [c['t'] for c in tb.get(8, [])] == ['📘'] and [c['t'] for c in tb.get(10, [])] == ['📘'], {8: tb.get(8), 10: tb.get(10)}, tag)
    if QJ.SMOKE:   # smoke — 1.3.1 칩 줄 한 칸만
        return
    idc = {i: [c['t'] for c in tb.get(i, [])] for i in ids}
    T(pre + '^id 문단(%d) — 📍 칩 0 · 📘 1' % len(ids), all(v.count('📘') == 1 and not any(t.startswith('📍') for t in v) for v in idc.values()), idc, tag)
    T(pre + '칩 줄 = ^id 행 ∪ 짝 있는 문단 끝(1.3.1 · 새 줄 %d)' % len(new), sorted(tb) == sorted(set(ids) | set(new)), {'dom': sorted(tb), 'ids': ids, 'new': new}, tag)
    if tag == 'NEW':
        ch = (tb.get(8) or [{}])[0]
        g = R.get('grey') or {}
        T(pre + '📘 = 다른 칩과 같은 칩(c-src 회색 #efece5 · 흐림·숨김 없음) · title 「교재 자리」',
          ch.get('cls') == 'chip c-src' and ch.get('bg') == 'rgb(239, 236, 229)' and ch.get('op') == '1' and ch.get('vis') == 'visible' and ch.get('disp') != 'none' and ch.get('title') == '교재 자리', {'chip': ch, 'prec': g}, tag)
    w = R.get('w8') or {}
    rows = w.get('rows') or []
    bk = {r['book']: r for r in rows if r.get('book')}
    cvr = [r for r in rows if r.get('bid')]
    m46 = {e['book']: e['page'] for e in G['M']['m'].get('1L46') or []}
    T(pre + '📘 누름 → 「교재 자리」 창(민법 창 머리 mbwin · 제목 = 문단 첫 줄)', R.get('tap8') and w.get('open') and w.get('mbwin') and (w.get('title') or '').startswith('X<-관할-{사}-소제기후'), {k: w.get(k) for k in ('open', 'mbwin', 'title')}, tag)
    T(pre + '핵심 61쪽(PDF 61) · 윤곽 31쪽(PDF 47) 줄 = 짝 블록 1L46 캔버스 자리(%s)' % m46,
      (bk.get('핵심') or {}).get('pp') == '61쪽' and 'PDF 61' in (bk.get('핵심') or {}).get('m', []) and (bk.get('윤곽') or {}).get('pp') == '31쪽' and 'PDF 47' in (bk.get('윤곽') or {}).get('m', [])
      and m46.get('핵심') == 61 and m46.get('윤곽') == 47, {'rows': rows[:3], 'm46': m46}, tag)
    e8 = G['e8']
    want_more = ['후보 %d' % (len(e8['c'][b]) - 1) for b in ('핵심', '윤곽') if len(e8['c'].get(b) or []) > 1]
    T(pre + '「후보 N」 접힘(%s) · 펴면 그 수만큼' % want_more, w.get('more') == want_more and all(f['hidden'] and f['n'] == 0 for f in w.get('folded') or [])
      and ((R.get('w8b') or {}).get('folded') or [{}])[0].get('n') == len(e8['c']['핵심']) - 1 and not ((R.get('w8b') or {}).get('folded') or [{}])[0].get('hidden'), {'more': w.get('more'), 'folded': w.get('folded'), 'after': (R.get('w8b') or {}).get('folded')}, tag)
    T(pre + '「정리캔버스 · 정리 1쪽 · 블록 1L46」 줄(짝 블록 %s)' % e8['b'], w.get('sec') == ['정리캔버스'] and [r['bid'] for r in cvr] == e8['b'] and cvr and cvr[0]['k'] == '정리' and cvr[0]['pp'] == '1쪽' and cvr[0]['m'] == ['· 블록 1L46'],
      {'sec': w.get('sec'), 'cv': cvr}, tag)
    T(pre + '창 글에 층 이름·점수·순위 0', w and not win_clean(w), win_clean(w), tag)
    if tag == 'NEW':
        T(pre + '폭 420(책상) · 제목 한 줄(nowrap · ellipsis)', near((w.get('rect') or {}).get('w'), 420, 1) and (w.get('ptOver') or {}).get('ws') == 'nowrap' and (w.get('ptOver') or {}).get('to') == 'ellipsis', {'rect': w.get('rect'), 'pt': w.get('ptOver')}, tag)
        sn = (bk.get('핵심') or {}).get('sn', '')
        I(pre + '1등 줄 「그 자리 글 두 줄」(글자층 y0~y1)', {b: (bk.get(b) or {}).get('sn') for b in ('핵심', '윤곽')})
        T(pre + '1등 줄에 그 자리 글(글자층) 있음', len(sn) >= 8 and sn.endswith('…'), sn, tag)
    b = R.get('book') or {}
    T(pre + '교재 줄 누름 → 교재 쪽 창 61 · 자리 강조 · 블록 ctx(「✓ 이 자리」·「📍 찍기」)', R.get('rowTap') and str(b.get('page')) == '61' and b.get('hl') and b.get('okBtn') == '✓ 이 자리' and b.get('pkBtn'),
      {k: b.get(k) for k in ('page', 'hl', 'okBtn', 'pkBtn', 'err')}, tag)
    c = R.get('canvas') or {}
    T(pre + '캔버스 줄 누름 → 정리OMR 팝업 · 목표 1L46 · 탭 무변', R.get('cvTap') and c.get('tab') == 'jo' and ('cv|omr|para|%s|8' % N131) in (c.get('pops') or []) and c.get('omr') == ['1L46'], c, tag)   # A-6(a) 9/30 — omrpop C-1: 📘 창 정리캔버스 줄 J.go(정리 탭) → 정리OMR 팝업(목표 = 그 블록) · 옛: tab omr · bid 1L46 · 팝업 0
    tg = R.get('toggle') or {}
    T(pre + '같은 📘 두 번 → 창 닫힘(popToggle)', tg.get('t1') and tg.get('w1') and tg.get('t2') and not tg.get('after'), tg, tag)
    if tag != 'NEW' or R['mode'] != 'desk':
        if tag == 'NEW':
            T(pre + '콘솔 오류 0', not R.get('errs'), R.get('errs'))
        return
    n96 = R.get('n96') or {}
    pins = [c2['t'] for x in n96.get('tbl') or [] for c2 in x['chips'] if c2['t'].startswith('📍')]
    T(pre + '특허 노트(9.6) — 📍 칩 그대로 · 📘 0', pins and not any(c2['t'] == '📘' for x in n96.get('tbl') or [] for c2 in x['chips']), {'pins': pins[:4], 'n': len(pins)}, tag)
    for nm, x in (R.get('layers') or {}).items():
        if not x:
            T(pre + '층 표본 「%s」 있음' % nm, False, None, tag)
            continue
        s, w2 = x['s'], x['w'] or {}
        rows2 = w2.get('rows') or []
        info = {'s': s, 'how': x['how'], 'rows': [(r.get('book'), r.get('pp'), r.get('m')) for r in rows2 if r.get('book')], 'none': w2.get('none'), 'more': w2.get('more')}
        I(pre + '층 표본 「%s」 창 글' % nm, info)
        T(pre + '층 표본 「%s」 — 창 글에 층 이름·점수 0' % nm, w2.get('open') and not win_clean(w2), win_clean(w2), tag)
        if nm == '없음':
            T(pre + '층 표본 「없음」 → 「교재 자리를 찾지 못했습니다.」', '교재 자리를 찾지 못했습니다.' in (w2.get('none') or []), w2.get('none'), tag)
        else:
            e = G['NC']['p'][s['f']][str(s['end'])]
            want = {b2: e['c'][b2][0]['p'] for b2 in ('핵심', '윤곽') if e['c'].get(b2)}
            got = {r['book']: r['p'] for r in rows2 if r.get('book')}
            T(pre + '층 표본 「%s」 — 1등 줄 = ⚙ 1등(%s)' % (nm, want), got == want, {'got': got, 'want': want}, tag)
        if nm == '목차 축':
            e = G['NC']['p'][s['f']][str(s['end'])]
            rg = G['M']['toc'].get(s['f']) or {}
            allp = [(b2, y['p']) for b2 in ('핵심', '윤곽') for y in e['c'].get(b2) or []]
            T(pre + '목차 축 후보가 그 노트 toc 구간 안(%s)' % {k: v[:2] for k, v in rg.items()}, allp and all(rg.get(b2) and rg[b2][0] <= pg <= rg[b2][1] for b2, pg in allp), {'c': allp, 'toc': rg}, tag)
    bad = {}
    for f, dom in (R.get('notes6') or {}).items():
        ids, new = G['expect'](f)
        if sorted(dom) != sorted(set(ids) | set(new)):
            bad[f] = {'dom': dom, 'ids': ids, 'new': new}
    T(pre + '노트 여섯 — 짝도 ^id 도 없는 문단에 칩 줄 새로 생김 0(칩 줄 = ^id ∪ 짝 있는 문단 끝)', not bad and len(R.get('notes6') or {}) == 6, bad or list((R.get('notes6') or {}).keys()), tag)
    h = R.get('hand') or {}
    hrows = [r for r in h.get('rows') or [] if r.get('book') == '핵심']
    T(pre + '손값 픽스처(1L46 = 핵심 p.62 직접 찍음) → 핵심은 그 자리 하나 「찍어 둔 자리」 + 그림 + 「자동으로 되돌리기」',
      len(hrows) == 1 and hrows[0]['p'] == 62 and '찍어 둔 자리' in hrows[0]['m'] and (R.get('handPic') or [{}])[0].get('cv') and '자동으로 되돌리기' in (h.get('more') or []),
      {'rows': h.get('rows'), 'pic': R.get('handPic'), 'more': h.get('more')}, tag)
    T(pre + '손값 픽스처 — 윤곽은 자동 그대로(1등 PDF 47 · 「후보 N」)', any(r.get('book') == '윤곽' and r['p'] == 47 for r in h.get('rows') or []) and any(t.startswith('후보 ') for t in h.get('more') or []), h.get('more'), tag)
    a = R.get('afterRv') or {}
    arows = [r for r in (a.get('w') or {}).get('rows') or [] if r.get('book') == '핵심']
    T(pre + '「자동으로 되돌리기」 → 손값 칸 = {auto:true}(캔버스 자리 창과 같은 값) · 창이 자동으로(핵심 PDF 61) · 캔버스 상태 자동',
      R.get('rvTap') and (a.get('kv') or {}).get('auto') is True and set((a.get('kv') or {}).keys()) == {'auto', 't'} and arows and arows[0]['p'] == 61 and (a.get('state') or {}).get('st') in ('hi', 'lo'),
      {'kv': a.get('kv'), 'rows': arows[:1], 'state': a.get('state')}, tag)
    mg = R.get('merge') or {}
    mb = [r['bid'] for r in mg.get('rows') or [] if r.get('bid')]
    T(pre + '편집 로그로 1L46 을 %s 에 합쳐도 짝이 따라감(정리캔버스 줄 %s · 1L46 없음)' % (G['MERGE_INTO'], G['MERGE_INTO']), G['MERGE_INTO'] in mb and '1L46' not in mb, {'bids': mb, 'exc': R.get('mexc')}, tag)
    T(pre + '콘솔 오류 0', not (R.get('errs') or R.get('mergeErrs')), [R.get('errs'), R.get('mergeErrs')])


def gates_pad(R, tag):
    pre = '[pad %s %s] ' % (R['eng'], tag)
    if R.get('exc'):
        T(pre + '장면', False, R.get('exc'), tag)
        return
    T(pre + '도장 톡 → 출처 팝업 76 · 띠', R.get('tap76') and str((R.get('src76') or {}).get('page')) == '76' and (R.get('src76') or {}).get('band'), {'at': R.get('at76'), 'src': R.get('src76'), 'b61': R.get('b61')}, tag)
    T(pre + '같은 도장 다시 톡 → 닫힘', R.get('tap76b') and 'cv|src|minso_hs|76' not in (R.get('pops2') or []), R.get('pops2'), tag)
    rows = (R.get('w8') or {}).get('rows') or []
    T(pre + '📘 톡 → 「교재 자리」 창(핵심 PDF 61 · 윤곽 PDF 47)', R.get('tap8') and any(r.get('book') == '핵심' and r['p'] == 61 for r in rows) and any(r.get('book') == '윤곽' and r['p'] == 47 for r in rows), {'at': R.get('chip8'), 'rows': rows[:2]}, tag)
    b = R.get('book') or {}
    T(pre + '줄 톡 → 교재 쪽 창 61 · 강조 · ✓ 이 자리', R.get('rowTap') and str(b.get('page')) == '61' and b.get('hl') and b.get('ok') == '✓ 이 자리', b, tag)
    c = R.get('canvas') or {}
    T(pre + '캔버스 줄 톡 → 정리OMR 팝업 · 목표 1L46', R.get('cvTap') and ('cv|omr|para|%s|8' % N131) in (c.get('pops') or []) and c.get('omr') == ['1L46'], c, tag)   # A-6(a) 9/30 — omrpop C-1: 📘 창 정리캔버스 줄 J.go(정리 탭) → 정리OMR 팝업(목표 = 그 블록) · 옛: bid 1L46(정리 탭)
    if tag == 'NEW':
        T(pre + '콘솔 오류 0', not R.get('errs'), R.get('errs'))


def base_snap_D(eng, N):
    """regress — gates_D 의 「= 바탕」 칸(PC 1890 · 1024 의 카드 팝업 · #hrail · 민소 노트 팝업)이 쓰는 바탕 값을 저장된 기준 스냅샷으로 대신한다
    (바탕 6b03bf1 을 띄우던 D/BASE 장면 0 · 스냅샷에 없으면 NEW 값 자신 = 첫 기록 · cid = D@<엔진>/<폭>/<자리>)"""
    out = {}
    for W in (1890, 1024):
        k = 'pc%d' % W
        x = (N or {}).get(k) or {}
        if x.get('exc'):
            continue
        c = 'D@%s/%d' % (eng, W)
        out[k] = {q: {'rect': QJ.base('%s/%s' % (c, q), (x.get(q) or {}).get('rect'))} for q in ('card0', 'card1', 'card2')}
        out[k]['rail'] = {'rect': QJ.base(c + '/rail', (x.get('rail') or {}).get('rect')), 'sb': QJ.base(c + '/rail.sb', (x.get('rail') or {}).get('sb'))}
        out[k]['note'] = QJ.base(c + '/note', x.get('note'))
    return out


def gates_D(R, tag, BR=None):
    pre = '[D %s %s] ' % (R['eng'], tag)
    if R.get('exc'):
        T(pre + '폰 장면', False, R.get('exc'), tag)
    else:
        r0, r1 = R.get('rail0') or {}, R.get('rail1') or {}
        T(pre + '폰 390×844 #hrail 스크롤 줄 안 보임 — 두께 0 · ::-webkit-scrollbar display none · scrollbar-width none(엔진이 알면)',
          r0.get('sb') == 0 and r0.get('oh', 0) > 0 and r0.get('pseudo') == 'none' and r0.get('sbw') in ('none', None, ''), r0, tag)
        rd = R.get('raild') or {}
        T(pre + '모바일 아닌 390×844 창 — #hrail 스크롤바 두께 0(자리 차지 스크롤바 · 바탕 크로미움 10px — scrollbar-width:thin 이 ::-webkit-scrollbar 3px 를 이긴다)', rd.get('sb') == 0 and rd.get('oh', 0) > 0 and rd.get('sw', 0) > rd.get('cw', 0), rd, tag)
        if R.get('swipe'):
            T(pre + '#hrail 가로 밀기 됨(폰 · %s · scrollLeft 0 → >0)' % R.get('swipe'), r0.get('sw', 0) > r0.get('cw', 0) and r1.get('sl', 0) > r0.get('sl', 0), {'r0': r0, 'r1': r1}, tag)
        rd, rd1 = R.get('raild') or {}, R.get('raild1') or {}
        T(pre + '#hrail 가로 밀기 됨(모바일 아닌 390 창 · 가로 휠 · scrollLeft 0 → >0)', rd.get('sw', 0) > rd.get('cw', 0) and rd1.get('sl', 0) > rd.get('sl', 0), {'rd': rd, 'rd1': rd1}, tag)
        c0, c1, c2 = R.get('card0') or {}, R.get('card1') or {}, R.get('card2') or {}
        vv = R.get('vv') or {}
        h0, h1 = (c0.get('rect') or {}).get('h', 0), (c1.get('rect') or {}).get('h', 0)
        T(pre + '기억 없는 카드(%s) 손잡이 +150(%s) → 높이 늘어남 · 화면 밖 0' % (CK, R.get('rszHow')), h1 >= h0 + 60 and (c1.get('rect') or {}).get('b', 1e9) <= vv.get('ih', 844) + 0.5,
          {'h0': h0, 'h1': h1, 'b': (c1.get('rect') or {}).get('b'), 'mh': [c0.get('mh'), c1.get('mh')], 'at': R.get('rszAt')}, tag)
        cfg = R.get('cfgSeed') or {}
        T(pre + '기억 크기(h 656 > 60vh 506)로 다시 열기 → 기억 높이 그대로(60vh 에 안 막힘 · 화면 안)', cfg.get('h') and near((c2.get('rect') or {}).get('h'), min(cfg['h'], vv.get('ih', 844) - 8 - cfg['y']), 2) and (c2.get('rect') or {}).get('b', 1e9) <= vv.get('ih', 844) + 0.5,
          {'seed': cfg, 'dragCfg': R.get('cfg'), 'c2': c2}, tag)
        if tag == 'NEW':
            w = R.get('w8') or {}
            rc = w.get('rect') or {}
            T(pre + '폰 「교재 자리」 창 — 화면 안(폭 ≤ 374 · 좌우 8)', rc and rc.get('x', -1) >= 7.5 and rc.get('r', 1e9) <= 390 - 7.5 and w.get('rows', 0) >= 3, w, tag)
            T(pre + '폰 콘솔 오류 0', not R.get('errs'), R.get('errs'))
    for W in (1890, 1024):
        k = 'pc%d' % W
        x = R.get(k) or {}
        if x.get('exc'):
            T(pre + 'PC %d 장면' % W, False, x.get('exc'), tag)
            continue
        if tag == 'NEW' and BR and BR.get(k):
            b = BR[k]
            eq = lambda a, c: a and c and all(near(a.get(q), c.get(q), 0.5) for q in ('x', 'y', 'w', 'h'))
            T(pre + 'PC %d — 카드 팝업 자리·크기 = 바탕(연 때 · 손잡이 +150 뒤 · 다시 열기)' % W,
              eq((x.get('card0') or {}).get('rect'), (b.get('card0') or {}).get('rect')) and eq((x.get('card1') or {}).get('rect'), (b.get('card1') or {}).get('rect')) and eq((x.get('card2') or {}).get('rect'), (b.get('card2') or {}).get('rect')),
              {'new': [(x.get(q) or {}).get('rect') for q in ('card0', 'card1', 'card2')], 'base': [(b.get(q) or {}).get('rect') for q in ('card0', 'card1', 'card2')]})
            # ★ jo_hdrfold(9/28) — 머리 세모 ▴(#hdrFold)가 #laws 와 #hrail 사이에 서서 #hrail 이 x 로 밀린다(▴ 27 + 사이 8 = 35) — y·폭·높이는 같고 x 는 0 또는 35±1
            eqr = lambda a, c: a and c and all(near(a.get(q), c.get(q), 0.5) for q in ('y', 'w', 'h')) and (near(a.get('x'), c.get('x'), 0.5) or near((a.get('x') or 0) - (c.get('x') or 0), 35, 1))
            T(pre + 'PC %d — #hrail 자리·크기 = 바탕(▴ 가 있으면 x +35)' % W, eqr((x.get('rail') or {}).get('rect'), (b.get('rail') or {}).get('rect')), {'new': (x.get('rail') or {}).get('rect'), 'base': (b.get('rail') or {}).get('rect'), 'sbN': (x.get('rail') or {}).get('sb'), 'sbB': (b.get('rail') or {}).get('sb')})
            nr, br_ = x.get('note') or {}, b.get('note') or {}
            T(pre + 'PC %d — 민소 노트 팝업 자리·폭 = 바탕' % W, nr and br_ and all(near(nr.get(q), br_.get(q), 0.5) for q in ('x', 'y', 'w')), {'new': nr, 'base': br_})
            T(pre + 'PC %d 콘솔 오류 0' % W, not x.get('errs'), x.get('errs'))


def data_gates(RES):
    G = GR
    # A-3 민법앱 교재 무변 — minbeoppdf 커밋이 민소 두 권 파일만 건드렸나
    if QJ.GATE:
        DELIV_MB_REV = '127a7dc9'   # A-6(d) 9/30 — 인도 검산 새 쪽 = ms_book_stamp 인도 커밋(민소 두 권 pdf·책메타·stamp) · 옛: 'HEAD'(지금 70766166 = patent_hr8 대응표 · 9/28)
        names = git('show', '--name-status', '--format=', DELIV_MB_REV, repo=MB).decode('utf-8', 'replace').splitlines()
        touched = [q for x in names if x.strip() for q in x.split('\t')[1:]]   # 이름 바꿈(R) 줄은 옛·새 두 경로
        okp = lambda f: f in ('pdf/26핵심민소ABBYY_주석_앱.pdf', 'pdf/26윤곽민소ABBYY_주석_앱.pdf', 'pdf/26핵심민소ABBYY.pdf', 'pdf/윤곽 민소법 기본서ABBYY.pdf',
                              'words/minso_hs/책메타.json', 'words/minso_yg/책메타.json', 'stamp/minso_hs.json', 'stamp/minso_yg.json')
        I('minbeoppdf 인도 커밋(%s) 바뀐 파일' % DELIV_MB_REV, names)
        T('[A] 민법앱 교재 무변 — minbeoppdf 커밋이 민소 두 권(pdf · 책메타 · stamp)만 · 민법 책 words 0', touched and all(okp(f) for f in touched), touched)
    for d in ('minso_hs', 'minso_yg'):
        n, o = G['meta_' + d], G['old_' + d]
        diff = sorted(k for k in set(n) | set(o) if n.get(k) != o.get(k))
        T('[A] %s 책메타 — 바뀐 칸 = file·pdfMd5·hash류·builtAt 만(pageHash 같음)' % d, set(diff) <= {'file', 'pdfMd5', 'hash', 'hashAppFnv', 'builtAt', 'size', 'bytes'} and n.get('pageHash') == o.get('pageHash'), diff)
    # D11 — genie 에 교재 글·도장 글 0(note_canvas.json 은 쪽·좌표·점수·bid·노트 이름만)
    NC = G['NC']
    keys = set()
    for f, v in NC['p'].items():
        for k, e in v.items():
            keys |= set(e.keys())
            for bk2, L2 in e['c'].items():
                for x in L2:
                    keys |= {'c.' + q for q in x.keys()}
    T('[C] note_canvas.json 칸 = a·b·L·c{p,s,h,y0,y1} 만(교재 글 없음 · D11)', keys <= {'a', 'b', 'L', 'c', 'c.p', 'c.s', 'c.h', 'c.y0', 'c.y1'}, sorted(keys))
    raw = open(os.path.join(JOD, 'data', 'omr', '민소', 'note_canvas.json'), 'rb').read().decode('utf-8')
    oc = [r['o'] for r in G['P61']]
    T('[B] genie 데이터에 도장 OCR 글 0(stamp 는 비공개 저장소에만)', not any(o[:10] in raw for o in oc) and not os.path.exists(os.path.join(JOD, 'data', 'stamp')), oc)
    # C-1 표본 30 표 · C-1b 표(평가 파일)
    L.append('')
    L.append('── C-1 note_canvas.json 표본 30(무작위 · 씨 20260924) — 파일 · 행 a~끝 · 층 · 짝 블록 · 핵심 1등 · 윤곽 1등 ──')
    for f, k, e in G['S30']:
        top = lambda b2: ('%d(%s)' % (e['c'][b2][0]['p'], e['c'][b2][0]['h'])) if e['c'].get(b2) else '–'
        L.append('표본 | %s | %d~%s | %s | %s | 핵심 %s | 윤곽 %s' % (f[:28], e['a'], k, e['L'] or '없음', ','.join(e['b'][:4]) + ('…' if len(e['b']) > 4 else ''), top('핵심'), top('윤곽')))
    if os.path.exists(NCEVAL):
        V = json.load(open(NCEVAL, encoding='utf-8'))
        L.append('')
        L.append('── C-1b 홀드아웃(정답지 = 짝 블록 확신 hi 자리 · 원격 손값 0) — 신호 하나씩 끈 값 · 헛잣대 · 두 책 교차 ──')
        for k, v in V.get('res', {}).items():
            L.append('C-1b | %s | %s' % (k, json.dumps(v, ensure_ascii=False)))
        L.append('C-1b | 두 책 교차 | %s' % json.dumps(V.get('cross'), ensure_ascii=False))
        L.append('C-1b | 층 | %s' % json.dumps(V.get('stat'), ensure_ascii=False))
        for s in V.get('verdict') or []:
            L.append('C-1b 표본 | %s' % json.dumps(s, ensure_ascii=False))
    else:
        L.append('INFO | C-1b 평가 파일 없음 | ' + NCEVAL)


SRC = {}
GR = None


def main():
    if QJ.GATE:
        base_b = git('show', BASE_REV + ':jo/index.html')
    else:
        base_b = b''   # regress — 바탕 앱 풀기 0(git show 안 부름)
    new_raw = open(NEWF, 'rb').read()
    RES = {'src': {'base': [len(base_b), hashlib.md5(base_b).hexdigest()],
                   'new': [len(new_raw), hashlib.md5(new_raw.replace(b'\r\n', b'\n')).hexdigest(), new_raw.count(b'\r\n'), NEWF]}}
    SRC['BASE'] = base_b.decode('utf-8'); SRC['NEW'] = new_raw.decode('utf-8')
    global GR
    GR = ground()
    RES['G'] = {k: GR[k] for k in ('AMB', 'UNM', 'UNM_n', 'draft_keys', 'NOTES6', 'MERGE_INTO', 'cv_hash')}
    RES['G']['LAYERS'] = {k: ({q: v[q] for q in ('f', 'end', 'L', 'chip')} if v else None) for k, v in GR['LAYERS'].items()}
    os.makedirs(WORK, exist_ok=True)
    t00 = time.time()
    engs = [e for e in ('chromium', 'webkit') if ARG('--eng') in (None, e) and (not QJ.SMOKE or e == 'chromium')]   # smoke — chromium 만(이 하네스의 smoke 칸은 책상 폭 둘)
    with sync_playwright() as pw:
        brs = {e: getattr(pw, e).launch() for e in engs}
        sbb = {'chromium': pw.chromium.launch(ignore_default_args=['--hide-scrollbars'])} if 'chromium' in engs and not QJ.SMOKE else {}
        try:
            for eng in engs:
                br = brs[eng]
                def run(key, fn, *a):
                    t0 = time.time(); print('… %s %s' % (key, time.strftime('%H:%M:%S')), flush=True)
                    with QJ.stage(key):
                        RES[key] = r = fn(*a)
                    print('   %.1fs %s' % (time.time() - t0, (r or {}).get('exc', '') if isinstance(r, dict) else ''), flush=True)
                if ONLY in ('', 'a') and not QJ.SMOKE:   # smoke — A(옛 책 · 캐시)는 안 잰다
                    run('A/%s' % eng, scen_A, br, eng)
                if ONLY in ('', 'b'):
                    for tag in (('BASE', 'NEW') if QJ.GATE else ('NEW',)):   # regress — 바탕(헛잣대) 장면 0
                        run('B/%s/%s' % (eng, tag), scen_B, br, eng, tag)
                if ONLY in ('', 'c'):
                    for tag in (('BASE', 'NEW') if QJ.GATE else ('NEW',)):   # regress — 바탕(헛잣대) 장면 0
                        run('C/%s/%s' % (eng, tag), scen_C, br, eng, tag)
                if ONLY in ('', 'pad') and not QJ.SMOKE:
                    for tag in (('BASE', 'NEW') if QJ.GATE else ('NEW',)):   # regress — 바탕(헛잣대) 장면 0
                        run('PAD/%s/%s' % (eng, tag), scen_pad, br, eng, tag)
                if ONLY in ('', 'd') and not QJ.SMOKE:
                    for tag in (('BASE', 'NEW') if QJ.GATE else ('NEW',)):   # regress — D/BASE 장면 0(바탕 값은 기준 스냅샷 · report 의 base_snap_D)
                        run('D/%s/%s' % (eng, tag), scen_D, br, eng, tag, sbb.get(eng))
        finally:
            for b in list(brs.values()) + list(sbb.values()):
                b.close()
            for srv, _ in SERVERS.values():
                srv.shutdown()
    RES['sec'] = round(time.time() - t00, 1)
    rawp = os.path.join(WORK, 'raw_%s.json' % (ONLY or 'all'))
    old = {}
    if ONLY and os.path.exists(os.path.join(WORK, 'raw_all.json')):
        old = json.load(io.open(os.path.join(WORK, 'raw_all.json'), encoding='utf-8'))
    json.dump(RES, io.open(rawp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    if ONLY:
        old.update(RES)
        json.dump(old, io.open(os.path.join(WORK, 'raw_all.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
        RES = old
    else:
        json.dump(RES, io.open(os.path.join(WORK, 'raw_all.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    report(RES)


def report(RES):
    global GR
    if GR is None:
        GR = ground()
    if QJ.GATE:
        I('바탕 BASE = %s:jo/index.html' % BASE_REV, '%d B · md5 %s' % tuple(RES['src']['base']))
        T('바탕 md5 = %s…(genie 6b03bf1 · 교재 창 막대 고침 인도 판)' % BASE_MD5[:8], RES['src']['base'][1] == BASE_MD5, RES['src']['base'])
    I('새 판 NEW', '%d B · md5(LF) %s · CRLF %d · %s' % tuple(RES['src']['new']))
    I('픽스처', RES.get('G'))
    I('시간(초)', RES.get('sec'))
    for eng in ('chromium', 'webkit'):
        if RES.get('A/%s' % eng):
            gates_A(RES['A/%s' % eng])
        for tag in ('BASE', 'NEW'):
            if RES.get('B/%s/%s' % (eng, tag)):
                gates_B(RES['B/%s/%s' % (eng, tag)], tag)
        for tag in ('BASE', 'NEW'):
            if RES.get('C/%s/%s' % (eng, tag)):
                gates_C(RES['C/%s/%s' % (eng, tag)], tag)
        for tag in ('BASE', 'NEW'):
            if RES.get('PAD/%s/%s' % (eng, tag)):
                gates_pad(RES['PAD/%s/%s' % (eng, tag)], tag)
        b = RES.get('D/%s/BASE' % eng)
        if b:
            gates_D(b, 'BASE')
        if QJ.REGRESS and RES.get('D/%s/NEW' % eng):   # regress — 「= 바탕」 칸(PC 카드 · #hrail · 노트 자리) 기댓값 = 기준 스냅샷
            b = base_snap_D(eng, RES['D/%s/NEW' % eng])
        if RES.get('D/%s/NEW' % eng):
            gates_D(RES['D/%s/NEW' % eng], 'NEW', b)
    if not QJ.SMOKE:
        data_gates(RES)
    if QJ.GATE:
        tot = sum(len(v) for v in NULL.values()); fails = sum(1 for v in NULL.values() for x in v if not x)
        L.append('')
        L.append('── 헛잣대(규칙 ⑩) — 같은 잣대를 바탕 %s 에 돌린 결과: %d 중 FAIL %d · PASS %d ──' % (BASE_REV, tot, fails, tot - fails))
        for n in NULL:
            v = NULL[n]
            L.append('BASE | %s | %s' % (n, 'FAIL' if not all(v) else 'PASS'))
    else:
        L.append('')
        L.append('── 헛잣대(규칙 ⑩) — regress: 바탕 판을 안 띄운다(헛잣대 칸은 gate 에서만 · 처리표 「관문만」) ──')
    body = '\n'.join(L) + '\n\n합계  PASS %d · FAIL %d  (%s초)\n' % (CNT['PASS'], CNT['FAIL'], RES.get('sec'))
    print(body[-6000:])
    p = os.path.join(OUT, '_harness_jo_ms_book_stamp_result.txt')
    b = body.encode('utf-8')
    for _ in range(3):
        open(p, 'wb').write(b); time.sleep(0.5)
        if open(p, 'rb').read() == b:
            break


if __name__ == '__main__':
    if '--report' in sys.argv:
        report(json.load(io.open(os.path.join(WORK, 'raw_all.json'), encoding='utf-8')))
    else:
        main()
