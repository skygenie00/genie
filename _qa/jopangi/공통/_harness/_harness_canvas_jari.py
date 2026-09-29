# -*- coding: utf-8 -*-
"""정리캔버스 교재 자리(후보 카드 · 확정 · 직접 찍기 · 필터 · 손값 kv) — _task_canvas_jari_cand §E 관문 하네스.

  NEW  = genie 작업트리 jo/index.html · 데이터 = genie jo/data(⚙ 산출 canvas_match.json + canvas_cand.json)
  BASE = `b2f7338`(2cha_unit v4 · 이 판의 바탕) 의 같은 파일 — 옛 앱이 새 데이터 꼴을 먹어도 되는가 · D-6 의 「옛 판 기기」
  엔진 = playwright chromium · webkit — 책상 1440×900(마우스) · 아이패드 768×1024 · 1024×768(진짜 터치 · DSF 2)
  끌기 = chromium CDP 터치(끝에서 멈춤 · 두 손가락 = CDP 두 점) / webkit 신뢰 마우스(playwright webkit 은 톡만 진짜 터치 — 도구 한계)
  網 = 같은 출처만. 교재(비공개 저장소 zzikkaplan/minbeoppdf)는 페이지 fetch 에서 같은 출처 /__book/ 으로 돌려
       로컬 파일(책메타 = <MBPDF_ROOT>\\words · PDF = jopangi\\*.pdf)을 내준다 · pdf.js 3.11.174 는 로컬 vendor 를 미리 넣는다.
  GitHub 기록.json 은 SEED 가 창마다 메모리로 대답(두 기기 = 원격 글을 하네스가 넘겨준다 · J19 꼴)
  ?keep=1 = 새로고침해도 저장소를 안 비운다 · ?alt=1 = canvas_match.json 대신 자동값을 바꾼 사본(E-5)

쓰기 : python _harness_canvas_jari.py [--out 폴더] [--only build|desk|alt|sync|pad|base]
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import copy, hashlib, http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

GENIE = _roots.genie()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else HERE
ONLY = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else ''
SHOTS = os.path.join(OUT, '_canvas_jari_shots')
WORK = os.path.join(tempfile.gettempdir(), 'h_canvas_jari')
J = r'N:\개인\claude\jopangi'
REL = 'jo/index.html'
JOD = os.path.join(GENIE, 'jo')
DATA = os.path.join(JOD, 'data', 'omr', '민소')
BASE_REV = 'b2f7338'
BASE_MD5_LF = '4c5311031168aedf5e3ef4a987013d7a'
VENDOR = os.path.join(tempfile.gettempdir(), 'h_gichul', 'vendor')          # pdf.js 3.11.174(앱이 cdnjs 에서 받는 판과 같다)
MBPDF = _roots.mbpdf(r'words')
TESTS = io.open(os.path.join(HERE, '_harness_canvas_jari_tests.js'), encoding='utf-8').read()
IPAD_UA = ('Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 '
           '(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.alert=function(){};window.confirm=function(){return true;};window.prompt=function(){return null;};
(function(){var Q=new URLSearchParams(location.search);var nf=window.fetch.bind(window);
window.fetch=function(u,o){o=o||{};var s=String((u&&u.url)||u);
 if(Q.get('alt')==='1'&&/canvas_match\.json(\?|$)/.test(s))return nf(s.replace('canvas_match.json','canvas_match.alt.json'),o);
 var bk=s.indexOf('api.github.com/repos/zzikkaplan/minbeoppdf/contents/');
 if(bk>=0){var rest=s.slice(bk+'api.github.com/repos/zzikkaplan/minbeoppdf/contents/'.length).split('?')[0];return nf(location.origin+'/__book/'+rest,{headers:{}});}
 if(/cdnjs\.cloudflare\.com\/ajax\/libs\/pdf\.js\/3\.11\.174\//.test(s))return nf(location.origin+'/__vendor/'+s.split('/pdf.js/3.11.174/')[1],o);
 if(/\/contents\/jopangi\/(%EA%B8%B0%EB%A1%9D|기록)\.json/.test(s)){var R=window.__REMOTE;
  if((o.method||'GET')==='PUT'){var b=JSON.parse(o.body||'{}');if(!R)R=window.__REMOTE={text:null,sha:null,puts:0};
   if(R.sha&&b.sha!==R.sha)return Promise.resolve(new Response('{"message":"conflict"}',{status:409}));
   R.text=decodeURIComponent(escape(atob(b.content)));R.puts=(R.puts||0)+1;R.sha='H'+R.puts+'_'+Date.now();
   return Promise.resolve(new Response(JSON.stringify({content:{sha:R.sha}}),{status:200,headers:{'Content-Type':'application/json'}}));}
  if(!R||R.text==null)return Promise.resolve(new Response('{"message":"Not Found"}',{status:404}));
  var acc=((o.headers||{}).Accept||'');
  if(acc.indexOf('raw')>=0)return Promise.resolve(new Response(R.text,{status:200}));
  return Promise.resolve(new Response(JSON.stringify({sha:R.sha}),{status:200,headers:{'Content-Type':'application/json'}}));}
 if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));
 return nf(u,o);};
if(Q.get('keep')!=='1'){try{localStorage.clear();}catch(e){}
 try{localStorage.setItem('tt.cfg',JSON.stringify({token:'harness-token',person:Q.get('who')||'꼬까'}));}catch(e){}}
})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
</script>
<script src="/__vendor/pdf.min.js"></script>
<script>try{pdfjsLib.GlobalWorkerOptions.workerSrc=location.origin+'/__vendor/pdf.worker.min.js';}catch(e){__ERR.push('pdfjs vendor '+e);}</script>"""
READY = "!!window.__HJ&&typeof render==='function'&&typeof viewCanvas==='function'"
SERVERS = {}


def git(*a, repo=GENIE):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def wr(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'wb').write(data)
    time.sleep(0.5)
    if open(path, 'rb').read() != data:
        raise SystemExit('되읽기 불일치: ' + path)


def serve(tag, src, datamode='new'):
    """tag 마다 서버 하나 — index.html(SEED + 도구) · /data/ = genie jo/data(datamode='old' 면 canvas_match.json 만 옛 판) · /__book/ · /__vendor/"""
    key = tag + '|' + datamode
    if key in SERVERS:
        return SERVERS[key][1]
    out = os.path.join(WORK, 'srv_' + tag + '_' + datamode); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    src = src.replace('\r\n', '\n')
    b = src.index('<body'); bb = src.index('>', b) + 1
    html = src[:bb] + SEED + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + TESTS + '\n</script>\n' + html[e:]
    io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=out, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            if p.startswith('/__vendor/'):
                return os.path.join(VENDOR, p[len('/__vendor/'):].replace('/', os.sep))
            if p.startswith('/__book/words/'):
                return os.path.join(MBPDF, p[len('/__book/words/'):].replace('/', os.sep))
            if p.startswith('/__book/pdf/'):
                return os.path.join(J, '민소', '_pdf', p[len('/__book/pdf/'):])   # 9/23 — 민소 교재 PDF 는 민소\_pdf\
            if p.endswith('/canvas_match.alt.json'):
                return os.path.join(WORK, 'canvas_match.alt.json')
            if p.endswith('/canvas_cand.alt.json'):
                return os.path.join(WORK, 'canvas_cand.alt.json')
            if datamode == 'old' and p.endswith('omr/민소/canvas_match.json'):
                return os.path.join(WORK, 'canvas_match.old.json')
            if datamode == 'old' and p.endswith('omr/민소/canvas_cand.json'):
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


def route_filter(route):
    return route.continue_() if route.request.url.startswith('http://127.0.0.1') else route.abort()


class P:
    def __init__(self, br, eng, tag, src, W, H, pad=False, q='tok=1', who='꼬까', datamode='new'):
        self.eng, self.tag, self.pad, self.q, self.who = eng, tag, pad, q, who
        self.port = serve(tag, src, datamode)
        if pad:
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=IPAD_UA)
        else:
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1)
        self.ctx.route('**/*', route_filter)
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(120000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' else None)
        self.cdp = self.ctx.new_cdp_session(self.pg) if (eng == 'chromium' and pad) else None
        self.load(q)

    def load(self, q):
        self.q = q
        self.pg.goto('http://127.0.0.1:%d/index.html?%s&who=%s' % (self.port, q, urllib.parse.quote(self.who)), wait_until='load', timeout=120000)
        self.pg.wait_for_function(READY, timeout=120000)
        self.pg.wait_for_timeout(1200)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def click(self, at, wait=500):
        if not at or not at.get('on'):
            return False
        if self.pad:
            self.pg.touchscreen.tap(at['cx'], at['cy'])
        else:
            self.pg.mouse.click(at['cx'], at['cy'])
        self.pg.wait_for_timeout(wait)
        return True

    def tap_cdp(self, x, y):
        self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'id': 1}]})
        self.pg.wait_for_timeout(40)
        self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})

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

    def drag2(self, x0, y0, dx, dy, n=10):
        """두 손가락 — CDP 두 점을 같이 옮긴다(chromium 만)."""
        if not self.cdp:
            return None
        def pts(k):
            f = k / n
            return [{'x': x0 + dx * f, 'y': y0 + dy * f, 'id': 1}, {'x': x0 + 60 + dx * f, 'y': y0 + dy * f, 'id': 2}]
        self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': pts(0)})
        for k in range(1, n + 1):
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': pts(k)}); self.pg.wait_for_timeout(20)
        self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        self.pg.wait_for_timeout(300)
        return 'cdp-2touch'

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


# ══════════ 데이터 잣대 ══════════
def ground():
    M = json.load(open(os.path.join(DATA, 'canvas_match.json'), encoding='utf-8'))
    Cc = json.load(open(os.path.join(DATA, M['cand']), encoding='utf-8'))['c'] if M.get('cand') else M['c']
    meta = json.load(open(os.path.join(DATA, 'canvas_meta.json'), encoding='utf-8'))
    pos, order, note, kind = {}, [], {}, {}
    for pm in meta['pages']:
        Pj = json.load(open(os.path.join(DATA, 'canvas_p%d.json' % pm['n']), encoding='utf-8'))
        for i, b in enumerate(Pj['blocks']):
            if b['k'] == '헤딩' or b.get('del'):
                continue
            pos[b['bid']] = (pm['n'], i)
            order.append(b['bid'])
            note[b['bid']] = b.get('note') or ''
            kind[b['bid']] = b['k']
    m, cf = M['m'], M.get('cf') or {}

    def state(bid, hand):
        h = hand.get(bid)
        if h and not h.get('auto') and (h.get('none') or (h.get('by') in ('cand', 'hand') and h.get('b') and h.get('p'))):
            return 'none' if h.get('none') else 'hand'
        if m.get(bid):
            return 'hi' if cf.get(bid) == 'hi' else 'lo'
        return 'cand' if Cc.get(bid) else 'nil'
    opn = lambda bid, hand: state(bid, hand) in ('lo', 'cand', 'nil')
    pg3 = [b for b in order if pos[b][0] == 3]
    pick = lambda f, pool=pg3: next(b for b in pool if f(b))
    HI = pick(lambda b: m.get(b) and cf.get(b) == 'hi' and m[b][0]['book'] == '핵심')
    LO = pick(lambda b: m.get(b) and cf.get(b) == 'lo' and m[b][0]['book'] == '핵심')
    LOY = next((b for b in order if m.get(b) and cf.get(b) == 'lo' and m[b][0]['book'] == '윤곽'), None)   # 인쇄 쪽 잣대(윤곽 −16)
    CAND = '3L108' if ('3L108' in pos and not m.get('3L108') and len(Cc.get('3L108') or []) >= 4) else pick(lambda b: not m.get(b) and len(Cc.get(b) or []) >= 4)
    NIL = next((b for b in pg3 if not m.get(b) and not Cc.get(b)), None) or next(b for b in order if not m.get(b) and not Cc.get(b))
    used = {HI, LO, CAND, NIL}
    rest = [b for b in pg3 if b not in used and opn(b, {}) and Cc.get(b) and all(x['b'] == '핵심' or True for x in Cc[b])]
    HC, HH, HN, PICK = rest[0], rest[1], rest[2], rest[3]
    c_hc = Cc[HC][0]
    SEEDV = {HC: {'by': 'cand', 'b': c_hc['b'], 'p': c_hc['p'], 'y0': c_hc.get('y0'), 'y1': c_hc.get('y1'), 'x0': c_hc.get('x0'), 'x1': c_hc.get('x1'),
                  's': c_hc['s'], 'h': c_hc['h'], 'ci': 0, 't': 1790000000000, 'who': '꼬까PC'},
             HH: {'by': 'hand', 'b': '핵심', 'p': 150, 'r': [0.1, 0.2, 0.5, 0.3], 't': 1790000000001, 'who': '꼬까PC'},
             HN: {'none': True, 't': 1790000000002, 'who': '꼬까PC'}}
    return {'M': M, 'C': Cc, 'pos': pos, 'order': order, 'note': note, 'kind': kind, 'state': state, 'open': opn,
            'HI': HI, 'LO': LO, 'LOY': LOY, 'CAND': CAND, 'NIL': NIL, 'HC': HC, 'HH': HH, 'HN': HN, 'PICK': PICK, 'SEEDV': SEEDV}


def next_open(G, bid, hand):
    L = G['order']
    i = L.index(bid)
    for k in range(1, len(L) + 1):
        b = L[(i + k) % len(L)]
        if b != bid and G['open'](b, hand):
            return b
    return None


def expect_chip(G, bid, hand, off):
    st = G['state'](bid, hand)
    pr = lambda book, p: p + (off.get(book, 0) if off.get(book) is not None else 0)
    if st == 'none':
        return '교재 없음 ✓'
    if st == 'hand':
        h = hand[bid]
        return '교재 p.%d ✓' % pr(h['b'], h['p'])
    if st in ('hi', 'lo'):
        e = G['M']['m'][bid][0]
        return '교재 p.%d · %s' % (pr(e['book'], e['page']), '자동' if st == 'hi' else '확신 낮음')
    if st == 'cand':
        return '교재 후보 %d — 골라야 함' % len(G['C'][bid])
    return '교재 –'


# ══════════ E-2 · E-3 · E-4 · B-3 · D — 책상(마우스) ══════════
def pan_to(p, n, i):
    """옛 앱(go 창구 없음) — 캔버스를 끌어 블록을 가운데로(마우스 끌기 = 화면 옮기기 · 블록 위에서 시작해도 움직였으면 고르지 않는다)."""
    at = None
    for _ in range(6):
        at = p.ev("([n,i])=>__HJ.blkAt(n,i)", [n, i])
        if at and at.get('on'):
            return at
        st = p.ev("()=>{const r=document.getElementById('cvStage').getBoundingClientRect();return {cx:r.left+r.width/2,cy:r.top+r.height/2,w:r.width,h:r.height}}")
        if not at:
            return None
        dx = max(-st['w'] * 0.4, min(st['w'] * 0.4, st['cx'] - at['cx'])); dy = max(-st['h'] * 0.4, min(st['h'] * 0.4, st['cy'] - at['cy']))
        m = p.pg.mouse
        m.move(st['cx'], st['cy']); m.down()
        for k in range(1, 9):
            m.move(st['cx'] + dx * k / 8, st['cy'] + dy * k / 8); p.pg.wait_for_timeout(16)
        m.up(); p.pg.wait_for_timeout(350)
    return at


def open_block(p, G, bid):
    n, i = G['pos'][bid]
    at = p.ev("([b,n,i])=>__HJ.go(b,n,i)", [bid, n, i])
    if (not at or not at.get('on')) and not p.pad:
        at = pan_to(p, n, i)
    ok = p.click(at, 450)
    for _ in range(2):                                            # 다른 블록이 골라졌으면 다시 재서 한 번 더(쌓임이 바뀌었을 수 있다)
        if p.ev("__HJ.sel()") == '%d|%d' % (n, i):
            break
        at = p.ev("([n,i])=>__HJ.blkAt(n,i)", [n, i]); ok = p.click(at, 450)
    return ok and p.ev("__HJ.sel()") == '%d|%d' % (n, i)


def open_jari(p, G, bid):
    if not open_block(p, G, bid):
        return False
    at = p.ev("__HJ.chipAt()")
    p.click(at, 900)
    for _ in range(40):
        if p.ev("b=>__HJ.jari(b)", bid):
            return True
        p.pg.wait_for_timeout(100)
    return False


def scen_desk(br, eng, src):
    G = GR
    R = {'eng': eng}
    p = P(br, eng, 'NEW', src, 1440, 900)
    try:
        p.ev("([k,v])=>__HJ.lsSet(k,v)", ['jopangi.canvasjari', G['SEEDV']])
        p.load('tok=1&keep=1')
        R['boot'] = p.ev("__HJ.boot()")
        R['syncKeys'] = p.ev("__HJ.syncKeys()")
        R['openN'] = p.ev("()=>__HJ.hj('openN')")
        R['filt'] = p.ev("__HJ.filt()")
        R['recNames'] = p.ev("__HJ.recNames()")
        # E-2 칩 — 교재를 열기 전(인쇄 쪽 = PDF 쪽 · 핵심은 같다)
        R['chips'] = {}
        for nm in ('HI', 'LO', 'CAND', 'NIL', 'HC', 'HH', 'HN'):
            bid = G[nm]
            ok = open_block(p, G, bid)
            R['chips'][nm] = {'bid': bid, 'ok': ok, 'chips': p.ev("__HJ.chips()")}
        # B-3 거르기 — 켜면 미확정만 진하게(보이는 쪽) · 끄면 풀림
        at = p.ev("__HJ.filtAt()"); p.click(at, 700)
        R['keep_on'] = p.ev("__HJ.keep()"); R['filt_on'] = p.ev("__HJ.filt()")
        at = p.ev("__HJ.filtAt()"); p.click(at, 600)
        R['keep_off'] = p.ev("__HJ.keep()")
        # E-3 자리 창 — 후보만 있는 블록
        CAND = G['CAND']
        R['jari_open'] = open_jari(p, G, CAND)
        R['jari0'] = p.ev("b=>__HJ.jari(b)", CAND)
        # 카드 누름 → 교재 창 하나 · 자리 강조 = 후보 좌표
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [CAND, 'card', 0]); p.click(at, 600)
        R['book1'] = p.ev("__HJ.bookReady()")
        at = p.ev("__HJ.bookAt('nx')"); p.click(at, 700)            # ▶ 다음 쪽 — 후보 쪽을 떠나면 교재 창 ✓ 는 없다
        R['book1_next'] = p.ev("__HJ.bookReady()")
        at = p.ev("__HJ.bookAt('x')"); p.click(at, 500)             # 닫고 같은 카드로 다시
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [CAND, 'card', 0]); p.click(at, 600)
        p.ev("__HJ.bookReady()")
        # 같은 카드 또 누름 = 닫힘(popToggle 뜻)
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [CAND, 'card', 0]); p.click(at, 700)
        R['book_toggle'] = p.ev("__HJ.book()")
        # 카드 0 → 카드 1(다른 자리) — 창 하나를 돌려쓴다(두 번 안 뜬다)
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [CAND, 'card', 0]); p.click(at, 500)
        p.ev("__HJ.bookReady()")
        k1 = next((i for i, x in enumerate(G['C'][CAND]) if i > 0 and x['b'] == G['C'][CAND][0]['b']), 1)
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [CAND, 'card', k1]); p.click(at, 800)
        R['book2'] = p.ev("__HJ.bookReady()"); R['book2_k'] = k1
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [CAND, 'card', k1]); p.click(at, 400)   # 한 번 더(같은 자리) → 닫힘
        p.ev("__HJ.closeAll()")
        # ✓ 이 자리 — 핵심 p.333 이 있으면 그것(채팅 시안 · 실제 자리) · 없으면 카드 1
        R['jari_open2'] = open_jari(p, G, CAND)
        kk = next((i for i, x in enumerate(G['C'][CAND]) if x['b'] == '핵심' and x['p'] == 333), 1)
        R['ok_k'] = kk
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [CAND, 'ok', kk]); R['ok_click'] = p.click(at, 800)
        R['after_ok'] = {'ls': (p.ev("k=>__HJ.ls(k)", 'jopangi.canvasjari') or {}).get(CAND), 'jari': p.ev("b=>__HJ.jari(b)", CAND), 'chips': p.ev("__HJ.chips()"),
                         'openN': p.ev("()=>__HJ.hj('openN')"), 'filt': p.ev("__HJ.filt()")}
        # 새로고침 뒤 그대로
        p.load('tok=1&keep=1'); p.ev("__HJ.boot()")
        R['reload_open'] = open_jari(p, G, CAND)
        R['after_reload'] = {'jari': p.ev("b=>__HJ.jari(b)", CAND), 'chips': p.ev("__HJ.chips()")}
        # 자동으로 되돌리기 → {auto:true, t} · 칸 남음
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [CAND, 'rv', 0]); R['rv_click'] = p.click(at, 800)
        R['after_rv'] = {'ls': (p.ev("k=>__HJ.ls(k)", 'jopangi.canvasjari') or {}).get(CAND), 'chips': p.ev("__HJ.chips()"), 'jari': p.ev("b=>__HJ.jari(b)", CAND)}
        # 교재에 없음 → {none:true} · 칩 「교재 없음 ✓」 · 다시 되돌리기
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [CAND, 'none', 0]); p.click(at, 800)
        R['after_none'] = {'ls': (p.ev("k=>__HJ.ls(k)", 'jopangi.canvasjari') or {}).get(CAND), 'chips': p.ev("__HJ.chips()")}
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [CAND, 'rv', 0]); p.click(at, 600)
        p.ev("__HJ.closeAll()")
        # E-4 직접 찍기 — 📍 → 교재 창(찍기 켜짐) → 끌어 상자 → 저장 = {by:'hand', r}
        PK = G['PICK']
        R['pick_open'] = open_jari(p, G, PK)
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [PK, 'pick', 0]); p.click(at, 600)
        R['pick_book'] = p.ev("__HJ.bookReady()")
        pg = p.ev("__HJ.bookAt('pg')")
        R['pick_pg'] = pg
        F = (0.20, 0.30, 0.62, 0.41)
        if pg:
            vis = p.ev("()=>({ih:innerHeight})")
            y0 = pg['y'] + pg['h'] * F[1]; y1 = pg['y'] + pg['h'] * F[3]
            if y1 > vis['ih'] - 5:                             # 쪽 그림이 화면보다 길면 — 끄는 자리가 보이게 창 안에서 내린다
                p.ev("()=>{const w=POPS.find(x=>(x._pk||'').indexOf('cv|book|')===0);const b=w&&w.querySelector('.pb');if(b)b.scrollTop=0;return 1}")
                pg = p.ev("__HJ.bookAt('pg')")
            R['pick_drag_kind'] = p.drag(pg['x'] + pg['w'] * F[0], pg['y'] + pg['h'] * F[1], pg['x'] + pg['w'] * F[2], pg['y'] + pg['h'] * F[3])
            p.pg.wait_for_timeout(400)
            R['pick_box'] = p.ev("__HJ.book()")
            R['pick_pg2'] = p.ev("__HJ.bookAt('pg')")
            # 너무 작은 상자(0.8% 미만)는 버린다 — 앞 상자는 그대로
            pg2 = R['pick_pg2']
            p.drag(pg2['x'] + pg2['w'] * 0.7, pg2['y'] + pg2['h'] * 0.7, pg2['x'] + pg2['w'] * 0.703, pg2['y'] + pg2['h'] * 0.703, n=3)
            p.pg.wait_for_timeout(300)
            R['pick_tiny'] = p.ev("__HJ.book()")
            at = p.ev("__HJ.bookAt('sv')"); R['sv_click'] = p.click(at, 900)
        R['after_pick'] = {'ls': (p.ev("k=>__HJ.ls(k)", 'jopangi.canvasjari') or {}).get(PK), 'book': p.ev("__HJ.book()"), 'chips': p.ev("__HJ.chips()"),
                           'stage': p.ev("__HJ.stageHit()"), 'pops': p.ev("__HJ.pops()")}
        R['F'] = F
        # 교재 창을 닫은 뒤 캔버스가 살아 있다 — 다른 블록 누름이 먹는다
        R['after_pick_sel'] = open_block(p, G, G['HI'])
        p.ev("__HJ.closeAll()")
        # 다음 미확정 ▶
        hand_now = dict(G['SEEDV']); hand_now[PK] = R['after_pick']['ls'] or {}
        X = G['LO']
        R['nx_open'] = open_jari(p, G, X)
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [X, 'nx', 0]); p.click(at, 1200)
        R['nx_pops'] = p.ev("__HJ.pops()"); R['nx_expect'] = next_open(G, X, hand_now); R['nx_sel'] = p.ev("__HJ.sel()")
        p.ev("__HJ.closeAll()")
        # 인쇄 쪽 — 윤곽 교재를 한 번 연 뒤(책메타 printOffset −16) 윤곽 칩은 인쇄 쪽
        if G['LOY']:
            R['loy_open'] = open_jari(p, G, G['LOY'])
            j = p.ev("b=>__HJ.jari(b)", G['LOY'])
            ki = next((i for i, x in enumerate(G['C'][G['LOY']]) if x['b'] == '윤곽'), None)
            if ki is not None:
                at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [G['LOY'], 'card', ki]); p.click(at, 600)
                R['loy_book'] = p.ev("__HJ.bookReady()")
            p.ev("__HJ.closeAll()")
            open_block(p, G, G['LOY'])
            R['loy_chips'] = p.ev("__HJ.chips()"); R['loy_jari0'] = j
        # D-3 고아 — 데이터에 없는 bid 의 손값 → 머리 배지 · 칸은 안 지운다
        A0 = p.ev("k=>__HJ.ls(k)", 'jopangi.canvasjari') or {}
        A0['99L999'] = {'by': 'hand', 'b': '핵심', 'p': 100, 'r': [0.1, 0.1, 0.2, 0.2], 't': 1790000000009, 'who': '꼬까PC'}
        p.ev("([k,v])=>__HJ.lsSet(k,v)", ['jopangi.canvasjari', A0])
        p.load('tok=1&keep=1'); p.ev("__HJ.boot()")
        R['orph'] = p.ev("__HJ.orph()"); R['orph_kept'] = (p.ev("k=>__HJ.ls(k)", 'jopangi.canvasjari') or {}).get('99L999')
        # D-4 ⤓ 기록
        R['rec'] = p.ev("__HJ.recRoundtrip()")
        R['errs'] = [x for x in p.ev("__HJ.errs()") + p.errs if not NOISE(x)]
        if eng == 'chromium':
            try:
                os.makedirs(SHOTS, exist_ok=True)
                open_jari(p, G, G['LO']); p.pg.screenshot(path=os.path.join(WORK, 'shot_1440_lo.png'))
                p.ev("__HJ.closeAll()"); open_jari(p, G, G['CAND']); p.pg.screenshot(path=os.path.join(WORK, 'shot_1440_cand.png'))
                at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [G['CAND'], 'card', 0]); p.click(at, 600); p.ev("__HJ.bookReady()")
                p.pg.screenshot(path=os.path.join(WORK, 'shot_1440_book.png'))
                R['shots'] = ['shot_1440_lo.png', 'shot_1440_cand.png', 'shot_1440_book.png']
            except Exception as e:
                R['shot_exc'] = repr(e)[:200]
    except Exception as e:
        R['exc'] = repr(e)[:800]
    finally:
        p.close()
    return R


# ══════════ E-5 손값 이김 — 자동값을 바꾼 사본을 먹여도 칩·창 = 손값 ══════════
def scen_alt(br, eng, src):
    G = GR
    R = {'eng': eng}
    HC = G['HC']
    M = copy.deepcopy(G['M'])
    Cc = copy.deepcopy(G['C'])
    M['m'][HC] = [{'book': '윤곽', 'page': 400, 'y0': 100.0, 'y1': 120.0, 'score': 0.99, 'how': 'vote', 'x0': 50.0, 'x1': 400.0}]
    M['cf'][HC] = 'hi'
    Cc[HC] = [{'b': '윤곽', 'p': 400, 'y0': 100.0, 'y1': 120.0, 'x0': 50.0, 'x1': 400.0, 's': 0.99, 'h': 'vote', 'ax': 'text', 'g': 0.0, 'in': 0}] + Cc[HC]
    M['cand'] = 'canvas_cand.alt.json'
    wr(os.path.join(WORK, 'canvas_match.alt.json'), json.dumps(M, ensure_ascii=False, separators=(',', ':')).encode('utf-8'))
    wr(os.path.join(WORK, 'canvas_cand.alt.json'), json.dumps({'hash': M['hash'], 'c': Cc}, ensure_ascii=False, separators=(',', ':')).encode('utf-8'))
    p = P(br, eng, 'NEW', src, 1440, 900)
    try:
        p.ev("([k,v])=>__HJ.lsSet(k,v)", ['jopangi.canvasjari', G['SEEDV']])
        p.load('tok=1&keep=1&alt=1'); p.ev("__HJ.boot()")
        open_block(p, G, HC); R['chips'] = p.ev("__HJ.chips()")
        R['jari_open'] = open_jari(p, G, HC); R['jari'] = p.ev("b=>__HJ.jari(b)", HC)
        p.ev("__HJ.closeAll()")
        # 되돌리면 사본 자동값(윤곽 p.400 · hi)
        open_jari(p, G, HC)
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [HC, 'rv', 0]); p.click(at, 800)
        R['after_rv_chips'] = p.ev("__HJ.chips()")
        R['errs'] = [x for x in p.ev("__HJ.errs()") + p.errs if not NOISE(x)]
    except Exception as e:
        R['exc'] = repr(e)[:800]
    finally:
        p.close()
    return R


# ══════════ E-6 동기화 — 두 프로필(+ 옛 판 기기) ══════════
def scen_sync(br, base, new):
    G = GR
    R = {}
    CAND = G['CAND']
    kk = next((i for i, x in enumerate(G['C'][CAND]) if x['b'] == '핵심' and x['p'] == 333), 1)
    A = P(br, 'chromium', 'NEW', new, 1440, 900, who='꼬까')
    B = P(br, 'chromium', 'NEW', new, 1440, 900, who='햄찌')
    C = P(br, 'chromium', 'BASE', base, 1440, 900, who='옛판')
    try:
        for x in (A, B, C):
            x.ev("__HJ.quiet()"); x.ev("f=>__HJ.sync(f)", False); x.ev("__HJ.quiet()")
        # ① A 확정 → 올림
        A.ev("__HJ.boot()"); open_jari(A, G, CAND)
        at = A.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [CAND, 'ok', kk]); A.click(at, 800)
        A.ev("__HJ.quiet()"); A.ev("__HJ.stamp()")
        A.ev("([t,h])=>__HJ.remoteSet(t,h)", [None, None])
        R['A1'] = A.ev("f=>__HJ.sync(f)", True)
        P1 = A.ev("__HJ.remoteGet()")['text']
        p1 = json.loads(P1)
        R['P1'] = {'cell': (p1['data'].get('jopangi.canvasjari') or {}).get(CAND), 'u': p1['u'].get('jopangi.canvasjari|' + CAND)}
        # ② B 받기 → 칩 ✓
        B.ev("([t,h])=>__HJ.remoteSet(t,h)", [P1, 'S1'])
        R['B1'] = B.ev("f=>__HJ.sync(f)", False); B.ev("__HJ.quiet()")
        B.ev("__HJ.boot()"); open_block(B, G, CAND)
        R['Bchips'] = B.ev("__HJ.chips()"); R['Bcell'] = (B.ev("k=>__HJ.ls(k)", 'jopangi.canvasjari') or {}).get(CAND)
        # ③ B 되돌리기 → 올림(칸 = auto:true · 묘비 0)
        B.ev("__HJ.closeAll()"); open_jari(B, G, CAND)
        at = B.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [CAND, 'rv', 0]); R['BrvOk'] = B.click(at, 900)
        B.ev("__HJ.quiet()"); B.ev("__HJ.stamp()")
        R['B2'] = B.ev("f=>__HJ.sync(f)", True)
        P2 = B.ev("__HJ.remoteGet()")['text']
        p2 = json.loads(P2)
        R['P2'] = {'cell': (p2['data'].get('jopangi.canvasjari') or {}).get(CAND), 'gone': [k for k in (p2.get('gone') or {}) if k.startswith('jopangi.canvasjari|')]}
        # ④ A 받기 → 자동(되살아나지 않음)
        A.ev("([t,h])=>__HJ.remoteSet(t,h)", [P2, 'S2'])
        R['A2'] = A.ev("f=>__HJ.sync(f)", False); A.ev("__HJ.quiet()")
        A.ev("__HJ.boot()"); open_block(A, G, CAND)
        R['Achips2'] = A.ev("__HJ.chips()"); R['Acell2'] = (A.ev("k=>__HJ.ls(k)", 'jopangi.canvasjari') or {}).get(CAND)
        # ⑤ 옛 판 기기 C(b2f7338) — A 가 다시 확정해 올린 원격(P3)을 받아 제 변경과 함께 올린다 → P4 · 새 판 A 가 다시 맞춘다 → P5
        A.ev("__HJ.closeAll()"); open_jari(A, G, CAND)
        at = A.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [CAND, 'ok', kk]); A.click(at, 800)
        A.ev("__HJ.quiet()"); A.ev("__HJ.stamp()")
        R['A3'] = A.ev("f=>__HJ.sync(f)", True)
        P3 = A.ev("__HJ.remoteGet()")['text']
        C.ev("([t,h])=>__HJ.remoteSet(t,h)", [P3, 'S3'])
        C.ev("()=>{try{lsWrite('jopangi.editq',[{k:'hz1',target:'note',st:'대기',t:Date.now()}],'수정 큐');}catch(e){}return 1}"); C.ev("__HJ.quiet()"); C.ev("__HJ.stamp()")
        R['C1'] = C.ev("f=>__HJ.sync(f)", True)
        P4 = C.ev("__HJ.remoteGet()")['text']
        p4 = json.loads(P4)
        R['P4'] = {'has': 'jopangi.canvasjari' in p4['data'], 'u': p4['u'].get('jopangi.canvasjari|' + CAND),
                   'gone': [k for k in (p4.get('gone') or {}) if k.startswith('jopangi.canvasjari|')], 'keys': len(p4['data'])}
        A.ev("([t,h])=>__HJ.remoteSet(t,h)", [P4, 'S4'])
        R['A4'] = A.ev("f=>__HJ.sync(f)", False); A.ev("__HJ.quiet()")
        P5 = A.ev("__HJ.remoteGet()")
        p5 = json.loads(P5['text'])
        R['P5'] = {'puts': P5.get('puts'), 'cell': (p5['data'].get('jopangi.canvasjari') or {}).get(CAND)}
        R['Acell4'] = (A.ev("k=>__HJ.ls(k)", 'jopangi.canvasjari') or {}).get(CAND)
        R['errs'] = [[y for y in x.ev("__HJ.errs()") + x.errs if not NOISE(y)] for x in (A, B, C)]
    except Exception as e:
        R['exc'] = repr(e)[:800]
    finally:
        for x in (A, B, C):
            x.close()
    return R


# ══════════ E-7 아이패드 진짜 터치 ══════════
def scen_pad(br, eng, src, W, H, shots):
    G = GR
    R = {'eng': eng, 'W': W}
    p = P(br, eng, 'NEW', src, W, H, pad=True)
    try:
        p.ev("__HJ.boot()")
        CAND = G['CAND']
        R['jari_open'] = open_jari(p, G, CAND)
        R['jari'] = p.ev("b=>__HJ.jari(b)", CAND)
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [CAND, 'card', 0]); R['card_tap'] = p.click(at, 700)
        R['book'] = p.ev("__HJ.bookReady()")
        kk = next((i for i, x in enumerate(G['C'][CAND]) if x['b'] == '핵심' and x['p'] == 333), 1)
        # 작은 화면에선 교재 창이 자리 창을 덮는다 — 그 후보 카드를 톡해 교재 창을 그 자리로 돌린 뒤 교재 창 머리의 ✓ 를 톡
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [CAND, 'card', kk]); R['card_k_tap'] = p.click(at, 700)
        if not R['card_k_tap']:                                   # 카드가 덮였으면 교재 창을 닫고 다시
            at = p.ev("__HJ.bookAt('x')"); p.click(at, 500)
            at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [CAND, 'card', kk]); R['card_k_tap'] = p.click(at, 700)
        R['book_k'] = p.ev("__HJ.bookReady()")
        at = p.ev("__HJ.bookAt('ok')"); R['ok_tap'] = p.click(at, 900)
        R['ok_ls'] = (p.ev("k=>__HJ.ls(k)", 'jopangi.canvasjari') or {}).get(CAND)
        R['ok_book'] = p.ev("__HJ.book()")
        p.ev("__HJ.closeAll()")
        # 📍 찍기 → 끌기 → 저장
        PK = G['PICK']
        R['pick_open'] = open_jari(p, G, PK)
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [PK, 'pick', 0]); p.click(at, 700)
        R['pick_book'] = p.ev("__HJ.bookReady()")
        pg = p.ev("__HJ.bookAt('pg')")
        vis = p.ev("()=>({ih:innerHeight,iw:innerWidth})")
        F = (0.25, 0.12, 0.70, 0.20)
        if pg:
            # 두 손가락은 끌기가 아니다(chromium CDP 두 점 · 상자 안 생김)
            if p.cdp:
                R['two'] = p.drag2(pg['x'] + pg['w'] * 0.3, pg['y'] + pg['h'] * 0.3, 0, -40)
                R['two_box'] = p.ev("__HJ.book()")
                R['two_scrolled'] = p.ev("()=>{const w=POPS.find(x=>(x._pk||'').indexOf('cv|book|')===0);if(!w)return null;let m=0,q=w.querySelector('.cv-bookpg');while(q&&q!==document.body){if(q.scrollTop>m)m=q.scrollTop;q.scrollTop=0;q=q.parentElement;}return m}")   # 두 손가락 = 쪽 스크롤 · 되돌려 놓고 끈다(머리줄이 위를 덮는다)
                p.pg.wait_for_timeout(200)
                pg = p.ev("__HJ.bookAt('pg')")
            y0 = max(pg['y'] + pg['h'] * F[1], 10)
            # ★ 9/24 — 교재 창 막대가 머리 아래로 내려와 창을 굴린 채면 위 가림 띠(머리+막대)가 머리 높이만큼 늘었다.
            #   시작점이 찍기 덮개 위가 아니면 창을 맨 위로 되돌리고 쪽 자리를 굴리지 않고 다시 잰다(끄는 손가락이 막대를 누르지 않게).
            on = lambda q: p.ev("([x,y])=>{const e=document.elementFromPoint(x,y);return !!e&&!!e.closest('.cv-pickov');}", [q['x'] + q['w'] * F[0], q['y'] + q['h'] * F[1]])
            R['start_on'] = [on(pg)]
            if not R['start_on'][0]:
                pg = p.ev("()=>{const w=POPS.find(x=>(x._pk||'').indexOf('cv|book|')===0);if(!w)return null;w.scrollTop=0;const r=w.querySelector('.cv-bookpg').getBoundingClientRect();return {x:r.left,y:r.top,w:r.width,h:r.height};}")
                p.pg.wait_for_timeout(200)
                R['start_on'].append(on(pg))
            R['drag_kind'] = p.drag(pg['x'] + pg['w'] * F[0], pg['y'] + pg['h'] * F[1], pg['x'] + pg['w'] * F[2], pg['y'] + pg['h'] * F[3])
            p.pg.wait_for_timeout(400)
            R['box'] = p.ev("__HJ.book()"); R['pg'] = p.ev("__HJ.bookAt('pg')")
            at = p.ev("__HJ.bookAt('sv')"); R['sv_tap'] = p.click(at, 900)
        R['F'] = F
        R['pick_ls'] = (p.ev("k=>__HJ.ls(k)", 'jopangi.canvasjari') or {}).get(PK)
        R['book_after'] = p.ev("__HJ.book()")                # 저장하면 교재 창은 닫힌다(자리 창은 남는다 — 작은 화면에선 가운데를 덮으니 닫고 잰다)
        p.ev("__HJ.closeAll()")
        R['stage'] = p.ev("__HJ.stageHit()")
        # 창 끌기(자리 창 머리)
        open_jari(p, G, CAND)
        hd = p.ev("k=>__HJ.popHeadAt(k)", 'cv|jari|' + CAND); r0 = p.ev("k=>__HJ.popRect(k)", 'cv|jari|' + CAND)
        if hd:
            R['win_drag_kind'] = p.drag(hd['cx'], hd['cy'], hd['cx'] - 70, hd['cy'] - 40)
            p.pg.wait_for_timeout(300)
        R['win_move'] = [r0, p.ev("k=>__HJ.popRect(k)", 'cv|jari|' + CAND)]
        R['win_in'] = p.ev("k=>{const r=__HJ.popRect(k);return r?(r.x>=-1&&r.y>=-1&&r.r<=innerWidth+1&&r.b<=innerHeight+1):null}", 'cv|jari|' + CAND)
        if shots:
            try:
                p.pg.screenshot(path=os.path.join(WORK, 'shot_ipad%d_jari.png' % W))
                R['shots'] = ['shot_ipad%d_jari.png' % W]
            except Exception as e:
                R['shot_exc'] = repr(e)[:200]
        R['errs'] = [x for x in p.ev("__HJ.errs()") + p.errs if not NOISE(x)]
    except Exception as e:
        R['exc'] = repr(e)[:800]
    finally:
        p.close()
    return R


# ══════════ 옛 앱(b2f7338)이 새 데이터 꼴을 먹는다 · 옛 데이터와 같은 칩 ══════════
def scen_base(br, eng, base):
    G = GR
    R = {'eng': eng}
    for dm in ('new', 'old'):
        p = P(br, eng, 'BASE', base, 1440, 900, datamode=dm)
        try:
            R[dm] = {'boot': p.ev("__HJ.boot()"), 'chips': {}}
            for nm in ('HI', 'LO', 'CAND', 'NIL'):
                open_block(p, G, G[nm]); R[dm]['chips'][nm] = p.ev("__HJ.chips()")
            R[dm]['jari_open'] = open_jari(p, G, G['HI']); R[dm]['jari'] = p.ev("b=>__HJ.jari(b)", G['HI'])
            R[dm]['errs'] = [x for x in p.ev("__HJ.errs()") + p.errs if not NOISE(x)]
        except Exception as e:
            R[dm] = dict(R.get(dm) or {}, exc=repr(e)[:600])
        finally:
            p.close()
    return R


# ══════════ ⚙ — E-1 ══════════
def scen_build():
    R = {}
    tmp = os.path.join(WORK, 'build'); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    cm = os.path.join(J, '민소', 'canvas', 'canvas_match.py')
    outs = []
    for k in (1, 2):
        o = os.path.join(tmp, 'r%d' % k); os.makedirs(o)
        r = subprocess.run([sys.executable, cm, '--out', os.path.join(o, 'canvas_match.json')], capture_output=True, cwd=os.path.join(J, '민소', 'canvas'),
                           env=dict(os.environ, PYTHONIOENCODING='utf-8'))
        R['run%d' % k] = r.stdout.decode('utf-8', 'replace').strip().split('\n')[-1][:600]
        outs.append(o)
    def strip(p):
        d = json.load(open(p, encoding='utf-8')); d.pop('생성', None); return json.dumps(d, ensure_ascii=False, sort_keys=True)
    R['same_main'] = strip(os.path.join(outs[0], 'canvas_match.json')) == strip(os.path.join(outs[1], 'canvas_match.json'))
    R['same_cand'] = open(os.path.join(outs[0], 'canvas_cand.json'), 'rb').read() == open(os.path.join(outs[1], 'canvas_cand.json'), 'rb').read()
    R['same_genie'] = strip(os.path.join(outs[0], 'canvas_match.json')) == strip(os.path.join(DATA, 'canvas_match.json')) and \
        open(os.path.join(outs[0], 'canvas_cand.json'), 'rb').read() == open(os.path.join(DATA, 'canvas_cand.json'), 'rb').read()
    R['bytes'] = [os.path.getsize(os.path.join(DATA, 'canvas_match.json')), os.path.getsize(os.path.join(DATA, 'canvas_cand.json'))]
    old = git('show', BASE_REV + ':jo/data/omr/민소/canvas_match.json')
    R['old_bytes'] = len(old)
    O = json.loads(old.decode('utf-8')); N = json.load(open(os.path.join(DATA, 'canvas_match.json'), encoding='utf-8'))
    R['m_st_same'] = {'m': O['m'] == N['m'], 'st': O['st'] == N['st'], 'hash': O['hash'] == N['hash'], 'books': O['books'] == N['books']}
    ck = os.path.join(tmp, 'check.json')
    r = subprocess.run([sys.executable, os.path.join(J, '민소', 'canvas', 'canvas_jari_check.py'), '--match', os.path.join(DATA, 'canvas_match.json'),
                        '--blocks', os.path.join(J, '민소', 'canvas', 'blocks2_r3.json'), '--old', os.path.join(WORK, 'canvas_match.old.json'), '--out-json', ck],
                       capture_output=True, cwd=os.path.join(J, '민소', 'canvas'), env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    R['check_rc'] = r.returncode
    R['check'] = json.load(open(ck, encoding='utf-8')) if os.path.isfile(ck) else r.stderr.decode('utf-8', 'replace')[-600:]
    return R


GR = None


def main():
    global GR
    os.makedirs(WORK, exist_ok=True)
    if not os.path.isfile(os.path.join(VENDOR, 'pdf.min.js')):
        raise SystemExit('pdf.js vendor 없음: ' + VENDOR)
    new_raw = open(os.path.join(GENIE, REL), 'rb').read()
    new = new_raw.decode('utf-8')
    base_b = git('show', BASE_REV + ':' + REL)
    base = base_b.decode('utf-8')
    wr(os.path.join(WORK, 'canvas_match.old.json'), git('show', BASE_REV + ':jo/data/omr/민소/canvas_match.json'))
    GR = ground()
    RES = {'src': {'base': [len(base_b), hashlib.md5(base_b).hexdigest()],
                   'new': [len(new_raw), hashlib.md5(new_raw.replace(b'\r\n', b'\n')).hexdigest(), new_raw.count(b'\r\n'), new_raw.count(b'\n')]},
           'G': {k: GR[k] for k in ('HI', 'LO', 'LOY', 'CAND', 'NIL', 'HC', 'HH', 'HN', 'PICK')}}
    t00 = time.time()
    if not ONLY or ONLY == 'build':
        t0 = time.time(); print('… build', flush=True)
        RES['build'] = scen_build(); print('   %.1fs' % (time.time() - t0), flush=True)
    with sync_playwright() as pw:
        brs = {e: getattr(pw, e).launch() for e in ('chromium', 'webkit')}
        try:
            for eng in ('chromium', 'webkit'):
                if not ONLY or ONLY == 'desk':
                    t0 = time.time(); print('… desk %s' % eng, flush=True)
                    RES['desk/' + eng] = scen_desk(brs[eng], eng, new); print('   %.1fs %s' % (time.time() - t0, RES['desk/' + eng].get('exc', '')), flush=True)
                if not ONLY or ONLY == 'alt':
                    t0 = time.time(); print('… alt %s' % eng, flush=True)
                    RES['alt/' + eng] = scen_alt(brs[eng], eng, new); print('   %.1fs %s' % (time.time() - t0, RES['alt/' + eng].get('exc', '')), flush=True)
                if not ONLY or ONLY == 'base':
                    t0 = time.time(); print('… base %s' % eng, flush=True)
                    RES['base/' + eng] = scen_base(brs[eng], eng, base); print('   %.1fs' % (time.time() - t0), flush=True)
                if not ONLY or ONLY == 'pad':
                    for W, H in [(768, 1024), (1024, 768)]:
                        t0 = time.time(); print('… pad %s %d' % (eng, W), flush=True)
                        RES['pad/%s/%d' % (eng, W)] = scen_pad(brs[eng], eng, new, W, H, shots=(eng == 'webkit' and W == 768))
                        print('   %.1fs %s' % (time.time() - t0, RES['pad/%s/%d' % (eng, W)].get('exc', '')), flush=True)
            if not ONLY or ONLY == 'sync':
                t0 = time.time(); print('… sync chromium', flush=True)
                RES['sync'] = scen_sync(brs['chromium'], base, new); print('   %.1fs %s' % (time.time() - t0, RES['sync'].get('exc', '')), flush=True)
        finally:
            for b in brs.values():
                b.close()
            for srv, _ in SERVERS.values():
                srv.shutdown()
    RES['sec'] = round(time.time() - t00, 1)
    json.dump(RES, io.open(os.path.join(WORK, 'raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    report(RES)


def NOISE(x):
    return 'ResizeObserver loop' in x or 'Failed to load resource' in x


def near(a, b, tol):
    return a is not None and b is not None and abs(a - b) <= tol


def report(RES):
    G = GR
    L = []
    T = lambda n, c, i=None: L.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c or i is None else ' | ' + json.dumps(i, ensure_ascii=False, default=str)[:900]))
    I = lambda n, v: L.append('INFO | ' + n + ' | ' + (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)[:1600]))
    sb, sn = RES['src']['base'], RES['src']['new']
    T('NEW 작업트리 CRLF 그대로(LF 단독 0 · %d 줄) · %d B · md5(LF) %s' % (sn[2], sn[0], sn[1]), sn[2] == sn[3])
    ch = sorted(l for l in git('status', '--porcelain').decode('utf-8').split('\n') if l.strip())
    want = sorted([' M ' + REL, ' M jo/data/omr/민소/canvas_match.json', '?? jo/data/omr/민소/canvas_cand.json'])
    T('genie 작업트리 바뀐 것 = jo/index.html · canvas_match.json · 새 canvas_cand.json 셋뿐 %s' % ch, ch == want, ch)
    I('표본 bid', RES['G'])
    M = G['M']
    # ── E-1 ⚙
    B = RES.get('build')
    if B:
        C = B['check'] if isinstance(B['check'], dict) else {}
        E = C.get('E1') or {}
        T('E-1 ⚙ 두 번 돌려 바이트 같음(생성 칸 빼고) · genie 에 있는 산출과 같음', B['same_main'] and B['same_cand'] and B['same_genie'], [B['same_main'], B['same_cand'], B['same_genie'], B.get('run1')])
        T('E-1 옛 칸 무변 — m · st · hash · books = 바탕(%s) canvas_match.json' % BASE_REV, all(B['m_st_same'].values()), B['m_st_same'])
        I('E-1 바이트', {'canvas_match.json': B['bytes'][0], 'canvas_cand.json': B['bytes'][1], '옛 canvas_match.json': B['old_bytes'], '떼기': bool(M.get('cand'))})
        T('E-1 A-5 — 합쳐 2 MB 를 넘어 c 를 canvas_cand.json 으로 뗌 · 본 파일에 cn(후보 수) · cand 가리킴', bool(M.get('cand')) and 'c' not in M and isinstance(M.get('cn'), dict), sorted(M.keys()))
        T('E-1 같은 프로세스 다시 재기 = 파일(c · cf · toc)', all((C.get('same_as_file') or {}).values()), C.get('same_as_file'))
        dist = E.get('dist') or {}
        n4 = sum(v for k, v in dist.items() if int(k) >= 4)
        T('E-1 c 가 있는 블록 %s / %s · 넷 이상 %d · 4 미만 까닭 = note 없음·구간 없음·0 hit 로 갈라 셈' % (E.get('with_c'), E.get('blocks'), n4), bool(E.get('with_c')) and bool(E.get('lt4') is not None), {'dist': dist, 'lt4': E.get('lt4')})
        T('E-1 none·short %s 중 후보 생김 %s(목표 ≥ 1,289)' % (E.get('none_short'), E.get('none_short_with_c')), (E.get('none_short_with_c') or 0) >= 1289, E.get('by_st'))
        T('E-1 D11 — 파일의 한글 문자열 = 책 이름·파일 이름·노트 이름·「생성」 밖 0(교재·블록 글자 없음)', (C.get('D11') or {}).get('outside_allowed') == 0 and (C.get('D11') or {}).get('toc_keys_are_block_notes'), C.get('D11'))
        A4 = C.get('A4a') or {}
        T('E-1 A-4 ⓐ 하나 빼고 다시 재기 — 짧은 블록 흉내 구간 안 넷(%s) > 헛잣대 무작위 넷(%s)' % (A4.get('short9_in_range_top4'), A4.get('null_random4_in_range')),
          (A4.get('short9_in_range_top4') or 0) > (A4.get('null_random4_in_range') or 1), A4)
        I('E-1 A-4 ⓐ 전부', A4)
        I('E-1 확신 · m≠c · 미확정', {'cf': E.get('cf'), 'm1_ne_c1': E.get('m1_ne_c1'), 'unconfirmed': E.get('unconfirmed'), 'toc': [E.get('toc_notes'), E.get('toc_books')]})
    # ── 책상
    for eng in ('chromium', 'webkit'):
        D = RES.get('desk/' + eng)
        if not D:
            continue
        E_ = '[%s] ' % eng
        if D.get('exc'):
            T(E_ + '책상 시나리오 예외 없음', False, D['exc'])
        sk = D.get('syncKeys') or []
        T(E_ + 'D-1 SYNC_KEYS 32 · 끝 = jopangi.canvasjari · 기록 이름표 「📘 정리캔버스 교재 자리」', len(sk) == 32 and sk[-1:] == ['jopangi.canvasjari'] and (D.get('recNames') or {}).get('label') == '📘 정리캔버스 교재 자리', [len(sk), sk[-2:], D.get('recNames')])
        hand = G['SEEDV']
        exp_open = sum(1 for b in G['order'] if G['open'](b, hand))
        T(E_ + 'B-3 「교재 미확정 N」 = ⚙ 로 센 값(%d · 손값 셋 뺌)' % exp_open, str(D.get('openN')) == str(exp_open) and (D.get('filt') or {}).get('n') == str(exp_open), [D.get('openN'), D.get('filt')])
        off0 = {}                                            # 교재를 열기 전 — 인쇄 쪽 = PDF 쪽
        for nm in ('HI', 'LO', 'CAND', 'NIL', 'HC', 'HH', 'HN'):
            c = (D.get('chips') or {}).get(nm) or {}
            chip = next((x for x in (c.get('chips') or []) if x['t'].startswith('교재')), None)
            want_t = expect_chip(G, c.get('bid'), hand, off0)
            st = G['state'](c.get('bid'), hand)
            cls_ok = chip is not None and ('jr-' + st) in chip['cls']
            look = True
            if chip and st == 'lo':
                look = chip['color'] == 'rgb(180, 83, 9)'
            if chip and st == 'cand':
                look = chip['bs'] == 'dashed' and chip['color'] == 'rgb(185, 28, 28)'
            if chip and st in ('hand', 'none'):
                look = chip['color'] == 'rgb(29, 122, 62)'
            T(E_ + 'E-2 칩 %s(%s · %s) = 「%s」 · 꼴' % (nm, c.get('bid'), st, want_t), c.get('ok') and chip is not None and chip['t'] == want_t and cls_ok and look, [c.get('ok'), chip])
        ko, kf = D.get('keep_on') or {}, D.get('keep_off') or {}
        inv = {('%d|%d' % v): k for k, v in G['pos'].items()}
        exp_keep = sorted(x for x in ko.get('all', []) if inv.get(x) and G['open'](inv[x], hand))
        T(E_ + 'B-3 거르기 켬 → 보이는 쪽의 진한 블록 = 미확정 블록(%d) · 끔 → 풀림' % len(exp_keep),
          ko.get('flt') and sorted(ko.get('keep', [])) == exp_keep and len(exp_keep) > 0 and not kf.get('flt') and not kf.get('keep'), [len(ko.get('keep', [])), len(exp_keep), kf.get('flt')])
        CAND = G['CAND']; cc = G['C'][CAND]
        j0 = D.get('jari0') or {}
        T(E_ + 'E-3 자리 창(%s · 후보만) — 카드 수 = c 수(%d) · 상태 「골라야 함」 · 「📍 직접 찍기」·「교재에 없음」·「다음 미확정 ▶」 · 옛 목록·「못 찾았다(자동)」 0' % (CAND, len(cc)),
          D.get('jari_open') and len(j0.get('cards', [])) == len(cc) and '골라야 함' in (j0.get('st') or '') and '직접 찍기' in (j0.get('pick') or '') and j0.get('none') and j0.get('nx') and j0.get('old') == 0 and not j0.get('miss'), j0)
        cards_ok = all(('p.%d' % x['p']) in y['t'] and x['b'] in y['t'] for x, y in zip(cc, j0.get('cards', [])))
        T(E_ + 'E-3 카드 글자 = c 차례 그대로(책 · 쪽)', cards_ok, [y['t'][:40] for y in j0.get('cards', [])][:4])
        b1 = D.get('book1') or {}
        x0 = cc[0]
        wh = M['books'][x0['b']]['wh'][x0['p'] - 1]
        exp_hl = None if x0.get('y0') is None else [x0.get('x0', 0) / wh[0] * 100, x0['y0'] / wh[1] * 100, (x0.get('x1', wh[0]) - x0.get('x0', 0)) / wh[0] * 100, (x0['y1'] - x0['y0']) / wh[1] * 100]
        hl = b1.get('hl')
        hl_ok = (exp_hl is None and hl is None) or (hl is not None and exp_hl is not None and all(near(a, b, 0.15) for a, b in zip([hl['l'], hl['t'], hl['w'], hl['h']], exp_hl)))
        T(E_ + 'E-3 카드 누름 → 교재 창 1개 · 쪽 = 후보 쪽(PDF %d) · 강조 = 후보 좌표(쪽 크기로 · ±0.15%%)' % x0['p'],
          b1.get('n') == 1 and str(b1.get('page')) == str(x0['p']) and b1.get('cvsW', 0) > 0 and hl_ok and not b1.get('pkBtn') is False, [b1.get('n'), b1.get('page'), hl, exp_hl, b1.get('err')])
        T(E_ + 'C-1 자리 창에서 연 교재 창 = 「📍 찍기」 있음 · 켜지지는 않음', b1.get('pkBtn') and not b1.get('pkOn'), [b1.get('pkBtn'), b1.get('pkOn')])
        bn = D.get('book1_next') or {}
        T(E_ + '보탬 — 카드에서 연 교재 창 머리 「✓ 이 자리」 = 그 후보 쪽에서만(▶ 로 넘기면 없음)', b1.get('okBtn') == '✓ 이 자리' and str(bn.get('page')) == str(x0['p'] + 1) and not bn.get('okBtn'), [b1.get('okBtn'), bn.get('page'), bn.get('okBtn')])
        T(E_ + 'C-4 같은 카드 또 누름 = 교재 창 닫힘(popToggle 뜻)', (D.get('book_toggle') or {}).get('n') == 0, D.get('book_toggle'))
        b2 = D.get('book2') or {}
        k1 = D.get('book2_k')
        T(E_ + 'C-4 다른 카드 누름 = 창 하나를 새 자리로(두 번 안 뜬다) · 쪽 = 카드 %s 쪽' % k1, b2.get('n') == 1 and str(b2.get('page')) == str(cc[k1]['p']), [b2.get('n'), b2.get('page'), cc[k1]['p'], b2.get('pk')])
        ao = D.get('after_ok') or {}
        kk = D.get('ok_k'); xk = cc[kk]
        v = ao.get('ls') or {}
        T(E_ + 'E-3 「✓ 이 자리」(카드 %d · %s p.%d) → 칸 {by:cand, b, p, 자리, s, h, ci, t, who}' % (kk, xk['b'], xk['p']),
          v.get('by') == 'cand' and v.get('b') == xk['b'] and v.get('p') == xk['p'] and v.get('ci') == kk and v.get('s') == xk['s'] and v.get('h') == xk['h'] and v.get('y0') == xk.get('y0')
          and isinstance(v.get('t'), (int, float)) and str(v.get('who', '')).startswith('꼬까'), v)
        chip = next((x for x in (ao.get('chips') or []) if x['t'].startswith('교재')), None)
        T(E_ + 'E-3 확정 뒤 칩 「교재 p.%d ✓」 · 창 머리 ✓ · 그 카드 on · 미확정 수 −1' % xk['p'],
          chip is not None and chip['t'] == '교재 p.%d ✓' % xk['p'] and (ao.get('jari') or {}).get('st', '').startswith('✓') and ((ao.get('jari') or {}).get('cards') or [{}] * (kk + 1))[kk].get('on')
          and str(ao.get('openN')) == str(exp_open - 1), [chip, (ao.get('jari') or {}).get('st'), ao.get('openN')])
        ar = D.get('after_reload') or {}
        chip = next((x for x in (ar.get('chips') or []) if x['t'].startswith('교재')), None)
        T(E_ + 'E-3 새로고침 뒤 그대로(칩 · 카드 on)', chip is not None and chip['t'] == '교재 p.%d ✓' % xk['p'] and ((ar.get('jari') or {}).get('cards') or [{}] * (kk + 1))[kk].get('on'), [chip])
        rv = D.get('after_rv') or {}
        chip = next((x for x in (rv.get('chips') or []) if x['t'].startswith('교재')), None)
        T(E_ + 'E-3 되돌리기 → 칸 = {auto:true, t}(칸 남음) · 칩 = 자동 글자(「후보 %d — 골라야 함」)' % len(cc),
          (rv.get('ls') or {}).get('auto') is True and 'by' not in (rv.get('ls') or {}) and chip is not None and chip['t'] == '교재 후보 %d — 골라야 함' % len(cc), [rv.get('ls'), chip])
        an = D.get('after_none') or {}
        chip = next((x for x in (an.get('chips') or []) if x['t'].startswith('교재')), None)
        T(E_ + 'B-2 「교재에 없음」 → 칸 {none:true, t, who} · 칩 「교재 없음 ✓」', (an.get('ls') or {}).get('none') is True and chip is not None and chip['t'] == '교재 없음 ✓', [an.get('ls'), chip])
        pb = D.get('pick_book') or {}
        PK = G['PICK']; cp = G['C'].get(PK) or []
        T(E_ + 'C-1 「📍 직접 찍기」 → 교재 창 · 찍기 켜짐 · 덮개 · 시작 쪽 = 1등 후보 쪽(%s)' % (cp[0]['p'] if cp else '—'),
          pb.get('n') == 1 and pb.get('pkOn') and pb.get('ov') and (not cp or str(pb.get('page')) == str(cp[0]['p'])), [pb.get('n'), pb.get('pkOn'), pb.get('ov'), pb.get('page')])
        F = D.get('F'); bx = (D.get('pick_box') or {}).get('box')
        T(E_ + 'C-2 끌기 → 초록 상자 = 끈 자리(±0.5%%) · 「이 자리 저장」 단추', bx is not None and all(near(a, b, 0.5) for a, b in zip([bx['l'], bx['t'], bx['w'], bx['h']], [F[0] * 100, F[1] * 100, (F[2] - F[0]) * 100, (F[3] - F[1]) * 100]))
          and '이 자리 저장' in ((D.get('pick_box') or {}).get('sv') or ''), [bx, F, D.get('pick_drag_kind')])
        tb = (D.get('pick_tiny') or {}).get('box')
        T(E_ + 'C-2 너무 작은 상자(0.3%%)는 버리고 앞 상자 그대로', tb is not None and bx is not None and near(tb['l'], bx['l'], 0.01) and near(tb['w'], bx['w'], 0.01), [tb, bx])
        ap = D.get('after_pick') or {}
        v = ap.get('ls') or {}
        r_ok = v.get('r') and all(near(a, b, 0.005) for a, b in zip(v['r'], F))
        prp = (v.get('p') or 0) - (16 if v.get('b') == '윤곽' else 0)   # 그 교재를 열었으니 책메타가 읽혔다 — 칩은 인쇄 쪽(윤곽 −16 · 핵심 0)
        T(E_ + 'C-3 저장 → 칸 {by:hand, b, p, r(0~1 네 자리 · ±0.5%%), t, who} · 교재 창 닫힘 · 칩 「교재 p.%s ✓」(인쇄 쪽)' % prp,
          v.get('by') == 'hand' and v.get('b') in ('핵심', '윤곽') and r_ok and all(round(x, 4) == x for x in (v.get('r') or [])) and (ap.get('book') or {}).get('n') == 0
          and str(v.get('who', '')).startswith('꼬까') and next((x for x in (ap.get('chips') or []) if x['t'] == '교재 p.%s ✓' % prp), None) is not None, [v, (ap.get('book') or {}).get('n'), ap.get('chips')])
        T(E_ + 'E-4 찍기 뒤 창 닫힘 → 캔버스로 돌아옴(가운데 = 캔버스 · 덮개 0) · 다른 블록 누름이 먹는다', (ap.get('stage') or {}).get('in') and (ap.get('stage') or {}).get('ov') == 0 and D.get('after_pick_sel'), [ap.get('stage'), D.get('after_pick_sel')])
        nxe = D.get('nx_expect')
        T(E_ + 'B-3 「다음 미확정 ▶」 → 다음 블록(%s)의 자리 창 하나 · 그 블록이 골라짐' % nxe,
          nxe is not None and 'cv|jari|' + nxe in (D.get('nx_pops') or []) and len([x for x in (D.get('nx_pops') or []) if x.startswith('cv|jari|')]) == 1
          and D.get('nx_sel') == '%d|%d' % G['pos'][nxe], [D.get('nx_pops'), D.get('nx_sel'), G['pos'].get(nxe)])
        if G['LOY']:
            chip = next((x for x in (D.get('loy_chips') or []) if x['t'].startswith('교재')), None)
            e0 = M['m'][G['LOY']][0]
            T(E_ + 'B-1 인쇄 쪽 — 윤곽 교재를 연 뒤 윤곽 칩 = 인쇄 쪽(PDF %d − 16 = %d)' % (e0['page'], e0['page'] - 16),
              chip is not None and chip['t'] == '교재 p.%d · 확신 낮음' % (e0['page'] - 16), [chip, (D.get('loy_book') or {}).get('nav')])
        T(E_ + 'D-3 고아 — 데이터에 없는 bid 의 손값 → 머리 배지 「교재 확정 1 고아」 · 칸은 남음', (D.get('orph') or {}).get('vis') and (D.get('orph') or {}).get('t') == '교재 확정 1 고아' and D.get('orph_kept'), [D.get('orph'), bool(D.get('orph_kept'))])
        rc = D.get('rec') or {}
        T(E_ + 'D-4 ⤓ 기록 — 내보내기에 canvasjari 층 · 지웠다 들여오면 되살아남 · 건수에 듦', rc.get('inDump') and rc.get('mid') is None and rc.get('after') == rc.get('before') and rc.get('before') and rc.get('stat'), rc)
        T(E_ + 'JS 오류 0', not D.get('errs'), D.get('errs'))
    # ── E-5
    for eng in ('chromium', 'webkit'):
        A = RES.get('alt/' + eng)
        if not A:
            continue
        E_ = '[%s] ' % eng
        hc = G['SEEDV'][G['HC']]
        chip = next((x for x in (A.get('chips') or []) if x['t'].startswith('교재')), None)
        T(E_ + 'E-5 손값 이김 — 자동값을 바꾼 사본(윤곽 p.400 · hi)을 먹여도 칩 = 손값 「교재 p.%d ✓」 · 창 머리 ✓' % hc['p'],
          chip is not None and chip['t'] == '교재 p.%d ✓' % hc['p'] and (A.get('jari') or {}).get('st', '').startswith('✓'), [chip, (A.get('jari') or {}).get('st')])
        chip = next((x for x in (A.get('after_rv_chips') or []) if x['t'].startswith('교재')), None)
        T(E_ + 'E-5 되돌리면 사본의 자동값(「교재 p.384 · 자동」 = 윤곽 400 − 16)', chip is not None and chip['t'] in ('교재 p.384 · 자동', '교재 p.400 · 자동'), chip)
        T(E_ + 'E-5 JS 오류 0', not A.get('errs') and not A.get('exc'), [A.get('errs'), A.get('exc')])
    # ── 옛 앱
    for eng in ('chromium', 'webkit'):
        Bs = RES.get('base/' + eng)
        if not Bs:
            continue
        E_ = '[%s] ' % eng
        cn, co = (Bs.get('new') or {}).get('chips') or {}, (Bs.get('old') or {}).get('chips') or {}
        same = all(json.dumps(cn.get(k)) == json.dumps(co.get(k)) and cn.get(k) for k in ('HI', 'LO', 'CAND', 'NIL'))
        T(E_ + '옛 앱(%s)이 새 데이터를 먹어도 칩 = 옛 데이터와 같다(HI·LO·CAND·NIL) · 자리 창 옛 목록 · JS 오류 0' % BASE_REV,
          same and ((Bs.get('new') or {}).get('jari') or {}).get('old', 0) >= 1 and not (Bs.get('new') or {}).get('errs') and not (Bs.get('old') or {}).get('errs'),
          [cn, co, (Bs.get('new') or {}).get('errs'), (Bs.get('new') or {}).get('exc')])
    # ── E-6
    S = RES.get('sync')
    if S:
        if S.get('exc'):
            T('E-6 동기화 시나리오 예외 없음', False, S['exc'])
        CAND = G['CAND']
        kk = next((i for i, x in enumerate(G['C'][CAND]) if x['b'] == '핵심' and x['p'] == 333), 1)
        xk = G['C'][CAND][kk]
        p1 = S.get('P1') or {}
        chip = next((x for x in (S.get('Bchips') or []) if x['t'].startswith('교재')), None)
        T('E-6 ① A 확정 → 올림(원격 data 에 canvasjari 칸 · u 도장) → ② B 받기 → B 칩 「교재 p.%d ✓」' % xk['p'],
          (p1.get('cell') or {}).get('by') == 'cand' and p1.get('u') and (S.get('Bcell') or {}).get('by') == 'cand' and chip is not None and chip['t'] == '교재 p.%d ✓' % xk['p'], [p1, S.get('Bcell'), chip])
        p2 = S.get('P2') or {}
        chip = next((x for x in (S.get('Achips2') or []) if x['t'].startswith('교재')), None)
        T('E-6 ③ B 되돌리기 → 올림(칸 = auto:true · 묘비 0) → ④ A 받기 → A 칸 auto:true · 칩 자동 글자(되살아나지 않음)',
          S.get('BrvOk') and (p2.get('cell') or {}).get('auto') is True and not p2.get('gone') and (S.get('Acell2') or {}).get('auto') is True and chip is not None and '골라야 함' in chip['t'], [p2, S.get('Acell2'), chip])
        p4 = S.get('P4') or {}
        I('E-6 ⑤ 옛 판 기기(%s)가 확정 든 원격을 받아 올린 기록' % BASE_REV, p4)
        T('E-6 ⑤ 옛 판 기기는 canvasjari 를 지우지 않는다 — 묘비 0 · u 도장은 남는다', not p4.get('gone') and p4.get('u'), p4)
        p5 = S.get('P5') or {}
        T('E-6 ⑤ 새 판 기기 A 가 다음 맞추기에서 되살려 올린다(원격 칸 = 확정)', (p5.get('cell') or {}).get('by') == 'cand', p5)
        I('E-6 ⑤ 옛 판 기기가 올릴 때 data 에서 canvasjari 가 빠지나(조판기 J19 · 2cha c2unit 과 같은 창)', {'옛 판이 올린 data 에 canvasjari': p4.get('has')})
        T('E-6 JS 오류 0(세 기기)', not any(S.get('errs') or [[1]]), S.get('errs'))
    # ── E-7
    for eng in ('chromium', 'webkit'):
        for W in (768, 1024):
            Pd = RES.get('pad/%s/%d' % (eng, W))
            if not Pd:
                continue
            E_ = '[%s 아이패드 %d] ' % (eng, W)
            if Pd.get('exc'):
                T(E_ + '시나리오 예외 없음', False, Pd['exc'])
            CAND = G['CAND']; cc = G['C'][CAND]
            kk = next((i for i, x in enumerate(cc) if x['b'] == '핵심' and x['p'] == 333), 1)
            T(E_ + 'E-7 블록 톡 → 교재 칩 톡 → 자리 창 · 카드 %d장' % len(cc), Pd.get('jari_open') and len((Pd.get('jari') or {}).get('cards', [])) == len(cc), [Pd.get('jari_open'), len((Pd.get('jari') or {}).get('cards', []))])
            T(E_ + 'E-7 카드 톡 → 교재 창 1개(그림 그려짐)', Pd.get('card_tap') and (Pd.get('book') or {}).get('n') == 1 and (Pd.get('book') or {}).get('cvsW', 0) > 0, [Pd.get('card_tap'), (Pd.get('book') or {}).get('n'), (Pd.get('book') or {}).get('err')])
            T(E_ + 'E-7 카드 톡 → 교재 창 머리 「✓ 이 자리」 톡 → 칸 by:cand · %s p.%d · 교재 창 닫힘' % (cc[kk]['b'], cc[kk]['p']),
              (Pd.get('ok_ls') or {}).get('by') == 'cand' and (Pd.get('ok_ls') or {}).get('p') == cc[kk]['p'] and (Pd.get('ok_ls') or {}).get('ci') == kk and (Pd.get('ok_book') or {}).get('n') == 0,
              [Pd.get('card_k_tap'), (Pd.get('book_k') or {}).get('okBtn'), Pd.get('ok_ls'), (Pd.get('ok_book') or {}).get('n')])
            if eng == 'chromium':
                tb = (Pd.get('two_box') or {}).get('box')
                T(E_ + 'C-2 두 손가락 끌기 = 상자 안 생김 · 쪽이 스크롤된다(CDP 두 점)', Pd.get('two') == 'cdp-2touch' and tb is None and (Pd.get('two_scrolled') or 0) > 0, [Pd.get('two'), tb, Pd.get('two_scrolled')])
            F = Pd.get('F'); bx = (Pd.get('box') or {}).get('box'); v = Pd.get('pick_ls') or {}
            T(E_ + 'E-7 📍 찍기 끌기(%s) → 상자 → 저장 톡 → 칸 by:hand · r = 끈 자리(±0.5%%)' % Pd.get('drag_kind'),
              bx is not None and v.get('by') == 'hand' and v.get('r') and all(near(a, b, 0.005) for a, b in zip(v['r'], F)), [bx, v, F])
            T(E_ + 'E-7 저장 → 교재 창 닫힘 · 창을 다 닫으면 가운데 = 캔버스 · 덮개 0', (Pd.get('book_after') or {}).get('n') == 0 and (Pd.get('stage') or {}).get('in') and (Pd.get('stage') or {}).get('ov') == 0, [(Pd.get('book_after') or {}).get('n'), Pd.get('stage')])
            wm = Pd.get('win_move') or [None, None]
            T(E_ + 'E-7 자리 창 끌기(%s) · 창이 화면 안' % Pd.get('win_drag_kind'), wm[0] and wm[1] and (abs(wm[1]['x'] - wm[0]['x']) > 20 or abs(wm[1]['y'] - wm[0]['y']) > 20) and Pd.get('win_in'), [wm, Pd.get('win_in')])
            T(E_ + 'JS 오류 0', not Pd.get('errs'), Pd.get('errs'))
    txt = '\n'.join(L)
    npass = sum(1 for l in L if l.startswith('PASS')); nfail = sum(1 for l in L if l.startswith('FAIL'))
    txt += '\n\n합계  PASS %d · FAIL %d  (%s초)\n' % (npass, nfail, RES.get('sec'))
    print(txt)
    open(os.path.join(OUT, '_harness_canvas_jari_result.txt' if not ONLY else '_harness_canvas_jari_result_%s.txt' % ONLY), 'w', encoding='utf-8', newline='\n').write(txt)
    for sub in ('desk/chromium', 'pad/webkit/768'):
        for name in ((RES.get(sub) or {}).get('shots') or []):
            src_ = os.path.join(WORK, name)
            if os.path.isfile(src_):
                wr(os.path.join(SHOTS, name.replace('shot_', '')), open(src_, 'rb').read())


if __name__ == '__main__':
    main()
