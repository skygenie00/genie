# -*- coding: utf-8 -*-
"""조판기 팝업 손질(≡·포스트잇·2차 카드) · 「목차노트」 단추 · 노트 들여쓰기 · ✎ 블록번호 지킴 — _task_jo_pop_moknote §G 관문 하네스.

  NEW  = genie 작업트리 jo/index.html(또는 --new <파일>) · 데이터 = genie jo/data(무접촉)
  BASE = `dd9d89f` 의 같은 파일(바탕 · 헛잣대 — 새 판이 뜻한 줄은 BASE 에서 FAIL 이어야 잣대가 산다)
  엔진 = playwright chromium · webkit — 책상 1440×900(마우스) · 폭 1024·768 · 아이패드 768×1024 · 1024×768(진짜 터치 · DSF 2)
  끌기·길게 누르기 = chromium CDP 터치(끝에서 150ms 멈춤) / webkit 신뢰 마우스(playwright webkit 은 톡만 진짜 터치 — 도구 한계)
  網 = 같은 출처만 · 시간대 = Asia/Seoul(포스트잇 시각 표시)

쓰기 : python _harness_jo_pop_moknote.py [--new 파일] [--out 폴더] [--only pops|pit|cards|mok|note|eq|pad|wide|shots] [--eng chromium|webkit]
       python _harness_jo_pop_moknote.py --report [--out 폴더]   (마지막 raw.json 으로 판정만 다시)
  ⚠ 책상 마우스 길게 누르기는 바탕 판부터 selectionchange 로 취소된다(노트 본문 줄) — 책상에서만 앱 핸들러에 합성 pointerdown 을 던지고 결과에 「합성」 으로 적는다.
     아이패드(chromium CDP 진짜 터치)는 합성 없이 뜬다.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import hashlib, http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

GENIE = _roots.genie()
HERE = os.path.dirname(os.path.abspath(__file__))
ARG = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
OUT = ARG('--out', HERE)
ONLY = ARG('--only', '')
ENGS = [ARG('--eng')] if ARG('--eng') else ['chromium', 'webkit']
NEWF = ARG('--new', os.path.join(GENIE, 'jo', 'index.html'))
SHOTS = os.path.join(OUT, '_pop_moknote_shots')
WORK = os.path.join(tempfile.gettempdir(), 'h_jo_pop_moknote')
REL = 'jo/index.html'
JOD = os.path.join(GENIE, 'jo')
DATA = os.path.join(JOD, 'data')
BASE_REV = 'dd9d89f'
BASE_MD5_LF = 'ce234cd4332a8fd76797e10a3f1c4b35'
TESTS = io.open(os.path.join(HERE, '_harness_jo_pop_moknote_tests.js'), encoding='utf-8').read()
IPAD_UA = ('Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 '
           '(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
SEP = '\u001f'
N96 = '9.6.{결}정정심판(136)_특무내정정청구(133-2)'
N41 = '4.1. 특받자-발명자_승계인_특허권이전,공유_무권리자'
N332 = '3.3.2.{공예주}공지예외주장(30)'
N34 = '3.4.{진}진보성(29②)선공기vs청'
PREC = '2021후10374'
PIT_K = 'prec|' + PREC + SEP + 'sum/0' + SEP + '2' + SEP + '{판시사항}'
PIT_TS = '2026-09-04T13:05:00.000Z'   # = 09.04 22:05 KST
PIT_T = '그후에 침해소송까지 간 사건이라 모든 사람들이 이 사건은 자세히 알고있었으니\n시험에 나올 껀덕지가 쎘다. 근데 진짜나왔대'
JO_K = 'jo|특허법:제129조' + SEP + '본문/0' + SEP + '0' + SEP + '물건을'
CK_SCORE = '특기출 26-63-1-침해금지(진보성 항변·자백)·손해배상(128조 종합)'
CK_2562 = '특기출 25-62-1'
LAWS = [('특허법', '특허'), ('상표법', '상표'), ('민사소송법', '민소'), ('디자인보호법', '디보')]
SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__CONF=[];window.alert=function(){};window.prompt=function(){return null;};
window.confirm=function(m){window.__CONF.push(String(m));return window.__CONFANS===undefined?true:!!window.__CONFANS;};
(function(){var Q=new URLSearchParams(location.search);var nf=window.fetch.bind(window);
window.fetch=function(u,o){var s=String((u&&u.url)||u);
 if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));
 return nf(u,o);};
if(Q.get('keep')!=='1'){try{localStorage.clear();}catch(e){}
 try{localStorage.setItem('tt.cfg',JSON.stringify({person:Q.get('who')||'꼬까'}));}catch(e){}}
})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
</script>"""
READY = "!!window.__HP&&typeof render==='function'&&typeof popShell==='function'&&!!document.querySelector('#slot')"


def git(*a, repo=GENIE):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def wr(path, data):
    """N: 는 잇달아 쓰면 이웃 파일 내용이 섞인다 — 한 파일 쓰고 0.5초 뒤 되읽어 대조."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(data, str):
        data = data.encode('utf-8')
    for _ in range(3):
        with open(path, 'wb') as f:
            f.write(data)
        time.sleep(0.5)
        if open(path, 'rb').read() == data:
            return True
    raise RuntimeError('되읽기 불일치: ' + path)


SERVERS = {}


def serve(tag, src):
    if tag in SERVERS:
        return SERVERS[tag][1]
    out = os.path.join(WORK, 'srv_' + tag); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
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
            if p.startswith('/data/'):
                return os.path.join(DATA, p[6:].replace('/', os.sep))
            if p in ('/index.html', '/'):
                return super().translate_path(path)
            f = os.path.join(JOD, p.lstrip('/').replace('/', os.sep))
            return f if os.path.exists(f) else super().translate_path(path)

        def log_message(self, *a, **k):
            pass
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


def route_filter(route):
    return route.continue_() if route.request.url.startswith('http://127.0.0.1') else route.abort()


class P:
    def __init__(self, br, eng, tag, src, W, H, pad=False, q='h=1', who='꼬까'):
        self.eng, self.tag, self.pad, self.W, self.H = eng, tag, pad, W, H
        self.port = serve(tag, src)
        kw = dict(viewport={'width': W, 'height': H}, locale='ko-KR', timezone_id='Asia/Seoul')
        if pad:
            self.ctx = br.new_context(device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=IPAD_UA, **kw)
        else:
            self.ctx = br.new_context(device_scale_factor=1, **kw)
        self.ctx.route('**/*', route_filter)
        self.pg = self.ctx.new_page()
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' else None)
        self.cdp = self.ctx.new_cdp_session(self.pg) if (eng == 'chromium' and pad) else None
        self.pg.goto('http://127.0.0.1:%d/index.html?%s&who=%s' % (self.port, q, urllib.parse.quote(who)), wait_until='load', timeout=120000)
        self.pg.wait_for_function(READY, timeout=120000)
        self.pg.wait_for_timeout(1500)

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

    def cdp_touch(self, ty, x, y):
        self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': ([] if ty == 'touchEnd' else [{'x': x, 'y': y, 'id': 1}])})

    def drag(self, x0, y0, x1, y1, n=12):
        if self.cdp:
            self.cdp_touch('touchStart', x0, y0)
            for i in range(1, n + 1):
                self.cdp_touch('touchMove', x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.pg.wait_for_timeout(16)
            for _ in range(5):
                self.cdp_touch('touchMove', x1, y1); self.pg.wait_for_timeout(30)
            self.cdp_touch('touchEnd', x1, y1)
            self.pg.wait_for_timeout(300)
            return 'cdp-touch'
        m = self.pg.mouse
        m.move(x0, y0); m.down()
        for i in range(1, n + 1):
            m.move(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.pg.wait_for_timeout(16)
        m.up()
        self.pg.wait_for_timeout(300)
        return 'mouse(trusted)'

    def longpress(self, x, y, ms=750):
        if self.cdp:
            self.cdp_touch('touchStart', x, y); self.pg.wait_for_timeout(ms)
            self.cdp_touch('touchEnd', x, y); self.pg.wait_for_timeout(250)
            return 'cdp-touch'
        m = self.pg.mouse
        m.move(x, y); m.down(); self.pg.wait_for_timeout(ms); m.up(); self.pg.wait_for_timeout(250)
        return 'mouse(trusted)'

    def type(self, text):
        self.pg.keyboard.type(text, delay=8); self.pg.wait_for_timeout(250)

    def shot(self, name):
        fn = os.path.join(WORK, 'shot_' + name + '.png'); self.pg.screenshot(path=fn); return fn

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


# ══════════ 잣대 — 데이터에서 센 값 ══════════
def ground():
    G = {}
    rx = re.compile(r'^(\d+(?:\.\d+)*)\.')
    num = lambda f: [int(x) for x in rx.match(f).group(1).split('.')] if rx.match(f) else None

    def key(f):
        n = num(f)
        return (0, n, f) if n is not None else (1, [], f)
    B = json.load(open(os.path.join(DATA, 'note_backlink.json'), encoding='utf-8'))
    for law, sh in LAWS:
        N = json.load(open(os.path.join(DATA, 'note_' + sh + '.json'), encoding='utf-8'))
        names = sorted(N.keys(), key=key)
        cite, tot = {}, Counter()
        for f in names:
            acc = {c: set() for c in ('기출', '사례', 'GS', '판례')}
            for k, v in B.items():
                if k.startswith(f + '#^'):
                    for c in acc:
                        acc[c].update(v.get(c) or [])
            cite[f] = {c: len(acc[c]) for c in acc}
            for c in acc:
                tot[c] += len(acc[c])
        tabby = sorted(names, key=lambda f: -sum(1 for r in N[f]['행'] if (r.get('i') or 0) and not r.get('h')))[:3]   # 탭 줄이 가장 많은 노트 셋(표본)
        G[sh] = {'n': len(N), 'order': names, 'cite': cite, 'tot': dict(tot), 'tabby': tabby,
                 'pad': {f: 10 + ((len(num(f)) if num(f) else 1) - 1) * 16 for f in names},
                 'bold': [f for f in names if '==' in f], 'nonum': [f for f in names if num(f) is None]}
    # 9.6 줄 들여쓰기 잣대(E-2)
    NP = json.load(open(os.path.join(DATA, 'note_특허.json'), encoding='utf-8'))

    def pads(rows):
        out, cur = [], 0
        for r in rows:
            h, i = r.get('h', 0) or 0, r.get('i', 0) or 0
            if h:
                cur = h; out.append((h - 1) * 15)
            else:
                out.append((cur * 15 + 12 if cur else 0) + i * 15)
        return out
    G['pad96'] = pads(NP[N96]['행'])
    G['rows96'] = NP[N96]['행']
    G['bl5b'] = B.get(N96 + '#^5b53b7') or {}
    G['rows41'] = NP[N41]['행']
    G['blk_only'] = {}
    for law, sh in LAWS[:3]:
        N = json.load(open(os.path.join(DATA, 'note_' + sh + '.json'), encoding='utf-8'))
        G['blk_only'][sh] = sum(1 for rec in N.values() for r in rec['행'] if re.match(r'^\s*\^[A-Za-z0-9-]+\s*$', r.get('t', '')))
    # 2차 카드 fm 기출
    G['cards'] = {}
    for kind, sh in (('기출', '특허'), ('기출', '상표'), ('사례', '특허'), ('기출', '디보')):
        d = json.load(open(os.path.join(DATA, '2cha_본문_%s_%s.json' % (kind, sh)), encoding='utf-8'))
        G['cards'][kind + '|' + sh] = [k for k, v in d.items() if isinstance(v, dict) and '기출' in (v.get('fm') or {})]   # 칸이 있는 카드 전수(특허 사례는 78장이 빈 값 — 칩은 원래 안 그려진다)
        G['cards_val'] = G.get('cards_val') or {}
        G['cards_val'][kind + '|' + sh] = sum(1 for v in d.values() if isinstance(v, dict) and (v.get('fm') or {}).get('기출'))
    return G


def at_of(p, js, arg=None):
    return p.ev(js, arg) if arg is not None else p.ev(js)


# ══════════ G-A 팝업 일곱 종 — ≡ · 머리 끌기 · 손잡이 ══════════
def scen_pops(br, eng, tag, src):
    p = P(br, eng, tag, src, 1440, 900)
    R = {'eng': eng, 'tag': tag, 'kinds': {}}
    try:
        p.ev("__HP.board('특허법','기출')")
        kinds = [('pit', {'target': 'prec|' + PREC, 'struct': 'sum/0', 'wi': 2, 'word': '{판시사항}'}),
                 ('card', {'kind': '기출', 'ck': CK_2562}), ('note', {'name': N96}), ('memo', {'id': PREC}),
                 ('jo', {'law': '특허법', 'jo': '제129조'}), ('claude', {'uid': 'T0138603'})]
        for k, a in kinds:
            p.ev("__HP.board('특허법','기출')")
            info = p.ev("([k,a])=>__HP.openKind(k,a)", [k, a])
            hd = p.ev("__HP.popHead()")
            d = None
            if hd and hd.get('on'):
                # 머리 글자(.pt) 한가운데서 (-90,+60) — 닫기 단추와는 멀다
                d = p.drag(hd['cx'], hd['cy'], hd['cx'] - 90, hd['cy'] + 60)
            after = p.ev("__HP.popInfo()")
            R['kinds'][k] = {'info': info, 'head': hd, 'drag': d, 'after': after}
            p.ev("__HP.clean()")
        # 목차노트 목록(NEW 만 — BASE 는 단추가 없다)
        p.ev("__HP.board('특허법','기출')")
        mb = p.ev("__HP.mokBtnAt()")
        if mb and mb.get('on'):
            p.click(mb, 900)
            info = p.ev("__HP.popInfo()")
            hd = p.ev("__HP.popHead()")
            d = p.drag(hd['cx'], hd['cy'], hd['cx'] - 90, hd['cy'] + 60) if hd and hd.get('on') else None
            R['kinds']['mok'] = {'info': info, 'head': hd, 'drag': d, 'after': p.ev("__HP.popInfo()")}
        else:
            R['kinds']['mok'] = {'info': None, 'btn': mb}
        R['pdragDoc'] = p.ev("__HP.pdragAll()")
        R['errs'] = p.ev("__HP.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


# ══════════ G-B · G-B5 포스트잇 창 · 메모 칩 ══════════
def scen_pit(br, eng, tag, src, pad=False, W=1440, H=900, shots=False):
    p = P(br, eng, tag, src, W, H, pad=pad)
    R = {'eng': eng, 'tag': tag, 'W': W, 'pad': pad}
    try:
        p.ev("o=>__HP.seedPits(o,true)", {PIT_K: {'t': PIT_T, 'who': '햄찌', 'at': PIT_TS, 'ts': PIT_TS, 'priv': True}})
        FN = {'w': 471, 'h': 240, 'x': 640, 'y': 432}
        p.ev("c=>__HP.setPopCfg('fn',c)", FN)
        p.ev("([l,i])=>__HP.goPrec(l,i)", ['특허법', PREC])
        at = p.ev("w=>__HP.pitwAt(w,'#slot')", '{판시사항}')
        R['pitwAt'] = at
        p.click(at, 700)
        R['w0'] = p.ev("__HP.pitWin()")
        # 같은 칩 두 번 = 닫힘
        at = p.ev("w=>__HP.pitwAt(w,'#slot')", '{판시사항}'); p.click(at, 600)
        R['toggleClosed'] = p.ev("__HP.pitWin()") is None
        at = p.ev("w=>__HP.pitwAt(w,'#slot')", '{판시사항}'); p.click(at, 700)
        R['w1'] = p.ev("__HP.pitWin()")
        # B-4 — 손끌기 +120 (칸 오른쪽 아래 끌개) → 한 글자 → 10줄 더
        g = p.ev("__HP.pitTaGrip()")
        if g and not pad:
            m = p.pg.mouse; m.move(g['x'], g['y']); m.down()
            for i in range(1, 13):
                m.move(g['x'], g['y'] + 120 * i / 12); p.pg.wait_for_timeout(16)
            m.up(); p.pg.wait_for_timeout(300)
            R['handMode'] = 'mouse(trusted) 손잡이 끌기'
        R['wHand'] = p.ev("__HP.pitWin()")
        if not pad and abs(((R['wHand'] or {}).get('ta') or {}).get('h', 0) - ((R['w1'] or {}).get('ta') or {}).get('h', 0)) < 2:
            R['handMode'] = '스크립트(칸 높이 +120 · mouseup) — 합성 마우스가 네이티브 손잡이를 못 잡음(도구 한계)'
            R['handScript'] = p.ev("d=>__HP.pitTaResize(d)", 120); p.pg.wait_for_timeout(200)
            R['wHand'] = p.ev("__HP.pitWin()")
        tf = p.ev("__HP.pitTaFocus()")
        if pad and tf:
            p.click(tf, 300); p.ev("__HP.pitTaFocus()")
        p.type('가')
        R['wChar'] = p.ev("__HP.pitWin()")
        p.type(''.join('\n%d번째 줄 — 메모 칸이 글 길이만큼 늘어나는지 잰다' % (i + 1) for i in range(10)))
        R['w10'] = p.ev("__HP.pitWin()")
        if shots:
            R['shot'] = p.shot('%s_pit_long_%d' % (eng, W))
        R['cfgAfter'] = p.ev("__HP.getPopCfg('fn')")
        # 저장 — 단추를 눌러서(화면 안 · elementFromPoint)
        sv = (R['w10'] or {}).get('saveHit')
        R['saveTap'] = p.click(sv, 900)
        rec = (p.ev("__HP.pitsRaw()") or {}).get(PIT_K)
        R['saved'] = rec
        R['cfgSaved'] = p.ev("__HP.getPopCfg('fn')")
        # 다른 'fn' 창 — 누구? · 메모 목록 = 기억 그대로(h 240)
        p.ev("()=>{pitAskWho(null,null,true);}"); p.pg.wait_for_timeout(400)
        R['who'] = p.ev("__HP.popInfo()"); p.ev("__HP.clean()")
        if not pad:
            # G-B5 — 판례 3단 머리 · 2단 카드 · 3단 클릭 = 메모 목록
            p.ev("([l,i])=>__HP.goPrec(l,i)", ['특허법', PREC])
            R['chip3'] = p.ev("__HP.memoChips('prec3')")
            R['chip2'] = p.ev("i=>__HP.memoChips('prec2',i)", PREC)
            at = p.ev("__HP.memoChipAt('prec3')"); R['chip3tap'] = p.click(at, 600)
            R['chip3pop'] = p.ev("__HP.popInfo()")
            p.ev("__HP.clean()")
            at = p.ev("i=>__HP.memoChipAt('prec2',i)", PREC); R['chip2tap'] = p.click(at, 600)
            R['chip2pop'] = p.ev("__HP.popInfo()")
            p.ev("__HP.clean()")
            R['memoWin'] = None
            # 조문 3단
            p.ev("o=>__HP.seedPits(o)", {JO_K: {'t': '조문 메모', 'who': '햄찌', 'at': PIT_TS, 'ts': PIT_TS}})
            p.ev("([l,j])=>__HP.goJo(l,j)", ['특허법', '제129조'])
            R['chipJo'] = p.ev("__HP.memoChips('jo3')")
            at = p.ev("__HP.memoChipAt('jo3')"); R['chipJoTap'] = p.click(at, 600)
            R['chipJoPop'] = p.ev("__HP.popInfo()")
            p.ev("__HP.clean()")
        R['errs'] = p.ev("__HP.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


# ══════════ G-C 2차 카드 팝업 전수 ══════════
def scen_cards(br, eng, tag, src, G):
    p = P(br, eng, tag, src, 1440, 900)
    R = {'eng': eng, 'tag': tag, 'scan': {}}
    try:
        for key, cks in G['cards'].items():
            kind, sh = key.split('|')
            law = [l for l, s in LAWS if s == sh][0]
            p.ev("([l,k])=>__HP.board(l,k)", [law, kind])
            R['scan'][key] = p.ev("([k,l])=>__HP.cardScan(k,l)", [kind, cks])
        R['errs'] = p.ev("__HP.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


# ══════════ G-D 목차노트 ══════════
def scen_mok(br, eng, tag, src, W=1440, H=900, pad=False, shots=False):
    p = P(br, eng, tag, src, W, H, pad=pad)
    R = {'eng': eng, 'tag': tag, 'W': W, 'pad': pad, 'law': {}}
    try:
        for law, sh in LAWS:
            p.ev("([l,k])=>__HP.board(l,k)", [law, '기출'])
            L = {'btn': p.ev("__HP.mokBtn()")}
            at = p.ev("__HP.mokBtnAt()")
            L['tap'] = p.click(at, 1200)
            L['list'] = p.ev("__HP.mokList()")
            if sh == '특허' and L['list']:
                at = p.ev("n=>__HP.mokRowAt(n)", N96)
                L['rowTap'] = p.click(at, 1200)
                L['note'] = p.ev("n=>__HP.notePop(n)", N96)
                L['noteRead'] = p.ev("n=>__HP.noteRead(n)", N96)
                L['list2'] = p.ev("__HP.mokList()")
                if shots:
                    L['shot'] = p.shot('%s_mok_%d' % (eng, W))
                # 노트 머리 끌기
                hd = p.ev("k=>__HP.popHead(k)", 'note|특허|' + N96 + '|')
                if hd and hd.get('on'):
                    L['noteDrag'] = p.drag(hd['cx'], hd['cy'], hd['cx'] - 60, hd['cy'] + 40)
                    L['noteAfter'] = p.ev("k=>__HP.popInfo(k)", 'note|특허|' + N96 + '|')
            # 같은 단추 두 번 = 닫힘
            at = p.ev("__HP.mokBtnAt()")
            L['tap2'] = p.click(at, 700)
            L['closed'] = p.ev("()=>!POPS.find(x=>(x._pk||'').indexOf('moknote|')===0)")
            R['law'][sh] = L
            p.ev("__HP.clean()")
        R['errs'] = p.ev("__HP.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


# ══════════ G-E 노트 들여쓰기 · 탭 폭 0 · 접기 표시 · 옛 포스트잇 키 ══════════
def scen_note(br, eng, tag, src, G, oldkey=None):
    p = P(br, eng, tag, src, 1440, 900)
    R = {'eng': eng, 'tag': tag}
    try:
        p.ev("([l,k])=>__HP.board(l,k)", ['특허법', '기출'])
        p.ev("n=>__HP.openKind('note',{name:n})", N96)
        R['n96'] = p.ev("n=>__HP.noteRead(n)", N96)
        # 새 포스트잇을 줄 1 「정정심판{136조}」 에 — 길게 눌러 메뉴 → 메모 붙이기 → 저장
        sc = "document.querySelector('.pop.k-cell:last-of-type')"
        at = p.ev("([n,w])=>{const p=POPS.find(x=>(x._pk||'')==='note|특허|'+n+'|');return __HP.wordAt(p,1,w);}", [N96, '정정심판{136조}'])
        R['lpAt'] = at
        if at and at.get('on'):
            R['lp'] = p.longpress(at['cx'], at['cy'])
            if not p.ev("__HP.menu()"):
                ok = p.ev("([x,y])=>__HP.lpSynth(x,y,'mouse')", [at['cx'], at['cy']])
                R['lp'] = (R['lp'] or '') + ' → 합성 pointerdown' + ('' if ok else '(안 뜸)')
        R['menu'] = p.ev("__HP.menu()")
        if R['menu']:
            p.ev("__HP.menuClick(0)")
            tf = p.ev("__HP.pitTaFocus()")
            p.type('H9-옛키')
            sv = (p.ev("__HP.pitWin()") or {}).get('saveHit')
            R['newSave'] = p.click(sv, 900)
        raw = p.ev("__HP.pitsRaw()") or {}
        R['newKeys'] = [k for k in raw if k.startswith('note|특허|' + N96 + SEP)]
        # 옛 키(BASE 에서 만든 키)를 심고 다시 연다 — 같은 단어에 밑줄·깃발(고아 0)
        if oldkey:
            p.ev("o=>__HP.seedPits(o,true)", {oldkey: {'t': '옛 판에서 붙인 메모', 'who': '햄찌', 'at': PIT_TS, 'ts': PIT_TS}})
            p.ev("__HP.clean()")
            p.ev("n=>__HP.openKind('note',{name:n})", N96)
            R['oldLine'] = p.ev("n=>{const p=POPS.find(x=>(x._pk||'')==='note|특허|'+n+'|');return __HP.pitLine(p,1);}", N96)
        p.ev("__HP.clean()")
        # 요약본(3단 · 판례 2021후10374) — 접기 표시 · 줄 들여쓰기
        p.ev("([l,i])=>__HP.goPrec(l,i)", ['특허법', PREC])
        R['sumHtog'] = p.ev("__HP.htogGap('#slot .main')")
        R['sumPad'] = p.ev("__HP.padTable('#slot .main')")
        # 2차 카드 팝업(25-62-1) — 접기 표시 · 줄 들여쓰기(임베드 상자 포함)
        p.ev("([l,k])=>__HP.board(l,k)", ['특허법', '기출'])
        p.ev("c=>__HP.openKind('card',{kind:'기출',ck:c})", CK_2562)
        p.pg.wait_for_timeout(800)
        R['cardHtog'] = p.ev("()=>__HP.htogGap(__HP.cardPopEl())")
        R['cardPad'] = p.ev("()=>__HP.padTable(__HP.cardPopEl())")
        p.ev("__HP.clean()")
        # 다른 두 법 노트 몇 개 — 줄 글자 = row.t · 탭 줄 첫 글자 = 패딩 시작
        R['others'] = {}
        for law, sh, names in (('상표법', '상표', G['상표']['tabby']), ('민사소송법', '민소', G['민소']['tabby'])):
            p.ev("([l,k])=>__HP.board(l,k)", [law, '기출'])
            for nm in names:
                p.ev("n=>__HP.openKind('note',{name:n})", nm)
                R['others'][sh + '|' + nm] = p.ev("([n,s])=>__HP.noteRead(n,s)", [nm, sh])
                p.ev("__HP.clean()")
        R['errs'] = p.ev("__HP.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


# ══════════ G-F ✎ 블록번호 지킴 ══════════
def eq_open(p, name, ri, word, R, pre):
    """노트 팝업을 열고 ri 줄의 word 를 길게 눌러 메뉴 → ✎ 수정"""
    p.ev("__HP.clean()")
    p.ev("n=>__HP.openKind('note',{name:n})", name)
    at = p.ev("([n,i,w])=>{const p=POPS.find(x=>(x._pk||'')==='note|특허|'+n+'|');return __HP.wordAt(p,i,w);}", [name, ri, word])
    R[pre + 'at'] = at
    if not (at and at.get('on')):
        return False
    R[pre + 'lp'] = p.longpress(at['cx'], at['cy'])
    m = p.ev("__HP.menu()")
    if not m:
        ok = p.ev("([x,y,t])=>__HP.lpSynth(x,y,t)", [at['cx'], at['cy'], 'touch' if p.pad else 'mouse'])
        R[pre + 'lp'] = (R[pre + 'lp'] or '') + ' → 합성 pointerdown' + ('' if ok else '(안 뜸)')
        m = p.ev("__HP.menu()")
    R[pre + 'menu'] = [x['t'] for x in (m or [])]
    if not m:
        return False
    i = [k for k, x in enumerate(m) if x['t'].startswith('✎')]
    if not i:
        return False
    hit = m[i[0]]['hit']
    p.click(hit, 400)
    return True


def scen_eq(br, eng, tag, src, G, pad=False, W=1440, H=900, shots=False):
    p = P(br, eng, tag, src, W, H, pad=pad)
    R = {'eng': eng, 'tag': tag, 'W': W, 'pad': pad}
    rows = G['rows96']
    t8 = rows[8]['t']
    try:
        p.ev("([l,k])=>__HP.board(l,k)", ['특허법', '기출'])
        p.ev("__HP.eqClear()")
        # ① 본문만 고치고 저장 → after 끝 = 「   ^5b53b7」
        R['o1'] = eq_open(p, N96, 8, '명도', R, 'o1_')
        R['box1'] = p.ev("__HP.eqBox()")
        p.ev("v=>__HP.eqSetVal(v)", t8.replace('명도', '명도(고침)'))
        R['save1'] = p.ev("__HP.eqClick('고침 저장')")
        R['q1'] = p.ev("__HP.eqQueue()")
        p.ev("__HP.eqClear()")
        if pad:
            # 아이패드: 번호 지우고 저장 → 막힘 까닭 · 저장 단추 톡
            R['o2'] = eq_open(p, N96, 8, '명도', R, 'o2_')
            p.ev("v=>__HP.eqSetVal(v)", t8.replace('   ^5b53b7', ''))
            at = p.ev("t=>__HP.eqClickAt(t)", '고침 저장'); R['saveTap2'] = p.click(at, 500)
            R['box2'] = p.ev("__HP.eqBox()")
            R['q2'] = p.ev("__HP.eqQueue()")
            if shots:
                R['shot'] = p.shot('%s_eq_block_%d' % (eng, W))
            R['errs'] = p.ev("__HP.errs()") + p.errs
            return R
        # ② 번호 지우고 저장 → 막힘+까닭
        R['o2'] = eq_open(p, N96, 8, '명도', R, 'o2_')
        p.ev("v=>__HP.eqSetVal(v)", t8.replace('   ^5b53b7', ''))
        p.ev("__HP.eqClick('고침 저장')")
        R['box2'] = p.ev("__HP.eqBox()"); R['q2'] = p.ev("__HP.eqQueue()")
        if shots:
            R['shot'] = p.shot('%s_eq_block_%d' % (eng, W))
        # ③ 앞 세 칸 → 탭
        p.ev("v=>__HP.eqSetVal(v)", t8.replace('   ^5b53b7', '\t^5b53b7'))
        p.ev("__HP.eqClick('고침 저장')")
        R['box3'] = p.ev("__HP.eqBox()"); R['q3'] = p.ev("__HP.eqQueue()")
        # ④ 번호 뒤에 줄 더
        p.ev("v=>__HP.eqSetVal(v)", t8.replace('명도', '명도(고침)') + '\n추가한 줄')
        p.ev("__HP.eqClick('고침 저장')")
        R['box4'] = p.ev("__HP.eqBox()"); R['q4'] = p.ev("__HP.eqQueue()")
        # ⑤ 원래 꼬리로 되돌리기 → 칸 글 → 저장됨
        R['fix'] = p.ev("__HP.eqClick('원래 꼬리로')")
        R['box5'] = p.ev("__HP.eqBox()")
        p.ev("__HP.eqClick('고침 저장')")
        R['q5'] = p.ev("__HP.eqQueue()")
        p.ev("__HP.eqClear()")
        # ⑥ 4.1 111줄(탭+띄어쓰기+^78111f) — 본문만 고치면 저장 · 탭 지우면 막힘
        t111 = G['rows41'][111]['t']
        R['o6'] = eq_open(p, N41, 111, '공유특허권', R, 'o6_')
        R['box6'] = p.ev("__HP.eqBox()")
        p.ev("v=>__HP.eqSetVal(v)", t111.replace('\t ^78111f', ' ^78111f'))
        p.ev("__HP.eqClick('고침 저장')")
        R['box6b'] = p.ev("__HP.eqBox()"); R['q6b'] = p.ev("__HP.eqQueue()")
        p.ev("v=>__HP.eqSetVal(v)", t111.replace('필요', '필요함'))
        p.ev("__HP.eqClick('고침 저장')")
        R['q6'] = p.ev("__HP.eqQueue()")
        p.ev("__HP.eqClear()")
        # ⑦ 줄 전체가 ^id — 공백+^id(3.3.2 36줄) · 맨 ^id(3.4 86줄) → 안 열림 + 토스트
        for nm, ri, w, k in ((N332, 36, '^bf52e2', 'o7a'), (N34, 86, '^0c5c53', 'o7b')):
            R[k] = eq_open(p, nm, ri, w, R, k + '_')
            R[k + '_box'] = p.ev("__HP.eqBox()")
            R[k + '_toast'] = p.ev("__HP.toasts()")
            p.ev("__HP.clean()")
        # ⑧ 꼬리 줄 비워 지우기 → 확인 창(수 = backlink) · 취소 → 큐 무변 · 확인 → 삭제 항목
        R['o8'] = eq_open(p, N96, 8, '명도', R, 'o8_')
        p.ev("v=>__HP.confSet(v)", False)
        p.ev("v=>__HP.eqSetVal(v)", '')
        p.ev("__HP.eqClick('고침 저장')"); p.pg.wait_for_timeout(300)
        R['conf8'] = p.ev("__HP.conf()"); R['q8'] = p.ev("__HP.eqQueue()")
        p.ev("v=>__HP.confSet(v)", True)
        p.ev("__HP.eqClick('고침 저장')"); p.pg.wait_for_timeout(300)
        R['conf8b'] = p.ev("__HP.conf()"); R['q8b'] = p.ev("__HP.eqQueue()")
        p.ev("__HP.eqClear()")
        # ⑨ 다시 고치기(existing · ✎ 수정 큐 → ✎ 다시 고치기) — 같은 막힘
        item = {'k': 'q_h_1', 'at': '2026-09-23T13:00', 'who': '나', 'target': 'note|특허|' + N96, 'part': '8', 'file': '',
                'before': t8, 'after': t8.replace('명도', '명도(첫 고침)'), 'st': '대기'}
        p.ev("a=>__HP.eqSeed(a)", [item])
        p.ev("__HP.clean()")
        R['eqPop'] = p.ev("__HP.openEqPop()")
        at = p.ev("k=>__HP.eqRedoAt(k)", '명도(첫 고침)'); R['redoTap'] = p.click(at, 600)
        R['box9'] = p.ev("__HP.eqBox()")
        p.ev("v=>__HP.eqSetVal(v)", t8.replace('명도', '명도(둘째)').replace('   ^5b53b7', ''))
        p.ev("__HP.eqClick('고침')")
        R['box9b'] = p.ev("__HP.eqBox()"); R['q9'] = p.ev("__HP.eqQueue()")
        p.ev("__HP.clean()")
        R['blkDirect'] = p.ev("__HP.blkConfirmDirect()")
        R['errs'] = p.ev("__HP.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


# ══════════ 아이패드(진짜 터치 · DSF 2) ══════════
def scen_pad(br, eng, src, W, H, G, shots=False):
    R = {'eng': eng, 'W': W}
    R['mok'] = scen_mok(br, eng, 'NEW', src, W, H, pad=True, shots=shots)
    R['pit'] = scen_pit(br, eng, 'NEW', src, pad=True, W=W, H=H, shots=shots)
    R['eq'] = scen_eq(br, eng, 'NEW', src, G, pad=True, W=W, H=H, shots=shots)
    # 머리 끌기(노트 팝업) — chromium CDP 터치 · webkit 마우스(도구 한계)
    return R


# ══════════ 폭 1024·768(책상) — 목록 줄바꿈 · 창이 화면 안 ══════════
def scen_wide(br, eng, src):
    R = {}
    for W, H in ((1024, 768), (768, 1024)):
        R[W] = scen_mok(br, eng, 'NEW', src, W, H)
    return R


def scen_shots(br, src, G):
    R = {}
    p = P(br, 'chromium', 'NEW', src, 1440, 900)
    try:
        p.ev("([l,k])=>__HP.board(l,k)", ['특허법', '기출'])
        p.ev("c=>__HP.openKind('card',{kind:'기출',ck:c})", CK_SCORE); p.pg.wait_for_timeout(900)
        R['card'] = p.shot('chromium_card_1440')
    finally:
        p.close()
    return R


def main():
    os.makedirs(WORK, exist_ok=True)
    base_b = git('show', BASE_REV + ':' + REL)
    new_raw = open(NEWF, 'rb').read()
    base, new = base_b.decode('utf-8'), new_raw.decode('utf-8')
    RES = {'src': {'base': [len(base_b), hashlib.md5(base_b).hexdigest()],
                   'new': [len(new_raw), hashlib.md5(new_raw.replace(b'\r\n', b'\n')).hexdigest(), new_raw.count(b'\r\n'), NEWF]}}
    G = ground()
    RES['G'] = {k: v for k, v in G.items() if k not in ('rows96', 'rows41')}
    t00 = time.time()
    with sync_playwright() as pw:
        brs = {e: getattr(pw, e).launch() for e in ENGS}
        try:
            oldkey = None
            for eng in ENGS:
                for tag, src in (('BASE', base), ('NEW', new)):
                    def run(name, fn, *a, **k):
                        if ONLY and ONLY != name:
                            return
                        t0 = time.time(); print('… %s %s/%s' % (name, eng, tag), flush=True)
                        RES['%s/%s/%s' % (name, eng, tag)] = r = fn(*a, **k)
                        print('   %.1fs %s' % (time.time() - t0, (r or {}).get('exc', '')), flush=True)
                    run('pops', scen_pops, brs[eng], eng, tag, src)
                    run('pit', scen_pit, brs[eng], eng, tag, src, shots=(tag == 'NEW' and eng == 'chromium'))
                    run('cards', scen_cards, brs[eng], eng, tag, src, G)
                    run('mok', scen_mok, brs[eng], eng, tag, src, shots=(tag == 'NEW' and eng == 'chromium'))
                    run('note', scen_note, brs[eng], eng, tag, src, G, oldkey=oldkey if tag == 'NEW' else None)
                    if tag == 'BASE' and oldkey is None:
                        nk = (RES.get('note/%s/BASE' % eng) or {}).get('newKeys') or []
                        oldkey = nk[0] if nk else None
                        RES['oldkey'] = oldkey
                    run('eq', scen_eq, brs[eng], eng, tag, src, G, shots=(tag == 'NEW' and eng == 'chromium'))
                if not ONLY or ONLY == 'pad':
                    for W, H in ((768, 1024), (1024, 768)):
                        t0 = time.time(); print('… pad %s %d' % (eng, W), flush=True)
                        RES['pad/%s/%d' % (eng, W)] = scen_pad(brs[eng], eng, new, W, H, G, shots=(eng == 'webkit' and W == 768))
                        print('   %.1fs' % (time.time() - t0), flush=True)
                if not ONLY or ONLY == 'wide':
                    t0 = time.time(); print('… wide %s' % eng, flush=True)
                    RES['wide/%s' % eng] = scen_wide(brs[eng], eng, new)
                    print('   %.1fs' % (time.time() - t0), flush=True)
            if (not ONLY or ONLY == 'shots') and 'chromium' in brs:
                RES['shots'] = scen_shots(brs['chromium'], new, G)
        finally:
            for b in brs.values():
                b.close()
            for srv, _ in SERVERS.values():
                srv.shutdown()
    RES['sec'] = round(time.time() - t00, 1)
    json.dump(RES, io.open(os.path.join(WORK, 'raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    report(RES, G)


def NOISE(x):
    return 'ResizeObserver loop' in x or 'Failed to load resource' in x or 'net::ERR' in x


def report(RES, G):
    L = []
    T = lambda n, c, i=None: L.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c or i is None else ' | ' + json.dumps(i, ensure_ascii=False, default=str)[:900]))
    I = lambda n, v: L.append('INFO | ' + n + ' | ' + (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)[:1600]))
    g = lambda d, *ks: __import__('functools').reduce(lambda a, k: (a[k] if isinstance(a, list) and isinstance(k, int) and -len(a) <= k < len(a)
                                                                    else (a or {}).get(k) if isinstance(a, dict) else None), ks, d)
    near = lambda a, b, t=1: a is not None and b is not None and abs(a - b) <= t
    sb, sn = RES['src']['base'], RES['src']['new']
    I('바탕 BASE = %s:%s' % (BASE_REV, REL), '%d B · md5 %s' % tuple(sb))
    T('바탕 md5 = 지시서(1,000,662 B · ce234cd4…)', sb[1] == BASE_MD5_LF and sb[0] == 1000662, sb)
    I('새 판 NEW', '%d B · md5(LF) %s · CRLF %d · %s' % tuple(sn))
    I('시간(초)', RES.get('sec'))
    GT = RES.get('G') or G
    I('잣대 — 노트 수', {sh: GT[sh]['n'] for _, sh in LAWS})
    I('잣대 — 인용 카드 수 합(갈래마다 서로 다른 값)', {sh: GT[sh]['tot'] for _, sh in LAWS})
    I('잣대 — 번호 없는 노트(맨 아래)', {sh: GT[sh]['nonum'] for _, sh in LAWS})
    I('잣대 — 줄 전체가 ^id(앞뒤 공백만)', GT.get('blk_only'))
    T('잣대 = 지시서 칩 합(특허 269·205·45·637 / 상표 151·5·331·547 / 민소 135·899·600·3)',
      GT['특허']['tot'] == {'기출': 269, '사례': 205, 'GS': 45, '판례': 637} and GT['상표']['tot'] == {'기출': 151, '사례': 5, 'GS': 331, '판례': 547}
      and GT['민소']['tot'] == {'기출': 135, '사례': 899, 'GS': 600, '판례': 3}, [GT[s]['tot'] for s in ('특허', '상표', '민소')])
    T('잣대 = 지시서 9.6(기출 5 · 사례 8 · 판례 24 · GS 0)', GT['특허']['cite'].get(N96) == {'기출': 5, '사례': 8, 'GS': 0, '판례': 24}, GT['특허']['cite'].get(N96))
    T('잣대 = 번호 없는 노트 상표 1 · 민소 0(9/24 볼트 밖으로 뺌) · 디보 1', [len(GT[s]['nonum']) for s in ('상표', '민소', '디보')] == [1, 0, 1], [GT[s]['nonum'] for s in ('상표', '민소', '디보')])   # A-6(d) 9/30 — 옛: 지시서 민소 3 · 9/24 13:1x 사용자가 번호 없는 셋을 볼트 밖으로(⚙ aa8ceae note_민소 84→81)
    T('잣대 = 줄 전체 ^id 특허 80 · 상표 24 · 민소 64(결정 14:0x)', GT.get('blk_only') == {'특허': 80, '상표': 24, '민소': 64}, GT.get('blk_only'))
    T('잣대 = fm 기출 카드 특허 기출 90 · 상표 기출 68 · 특허 사례 79(+ 디보 기출 64)',
      [len(GT['cards'][k]) for k in ('기출|특허', '기출|상표', '사례|특허', '기출|디보')] == [90, 68, 79, 64], [len(v) for v in GT['cards'].values()])
    for eng in ENGS:
        E = '[%s] ' % eng
        # ── G-A ──
        for tag in ('NEW', 'BASE'):
            A = RES.get('pops/%s/%s' % (eng, tag))
            if not A:
                continue
            if A.get('exc'):
                T(E + tag + ' G-A 예외 0', False, A['exc'])
            ks = A.get('kinds') or {}
            if tag == 'NEW':
                for k, v in ks.items():
                    inf, af = v.get('info') or {}, v.get('after') or {}
                    T(E + 'G-A %s — 머리 .pdrag 0 · 머리 글자에 「≡」 0 · 크기 손잡이 그대로' % k, inf and inf.get('pdrag') == 0 and inf.get('eq') is False and inf.get('prsz'),
                      [inf.get('pdrag'), inf.get('eq'), inf.get('prsz'), inf.get('title')])
                    dx = (af.get('pos') or {}).get('l', 0) - (inf.get('pos') or {}).get('l', 0)
                    dy = (af.get('pos') or {}).get('t', 0) - (inf.get('pos') or {}).get('t', 0)
                    T(E + 'G-A %s — 머리 끌기(-90,+60) → 자리 움직임 · %s' % (k, v.get('drag')), near(dx, -90, 3) and near(dy, 60, 3), [dx, dy, v.get('head')])
                T(E + 'G-A 일곱 종 다 열림(포스트잇·2차 카드·노트·목차노트 목록·메모 목록·조문·Claude 창)', len([1 for v in ks.values() if v.get('info')]) == 7, sorted(ks))
                T(E + 'G-A 문서 전체 .pdrag 0', A.get('pdragDoc') == 0, A.get('pdragDoc'))
                en = [x for x in (A.get('errs') or []) if not NOISE(x)]
                T(E + 'G-A JS 오류 0', not en, en[:4])
            else:
                pd = {k: (v.get('info') or {}).get('pdrag') for k, v in ks.items() if v.get('info')}
                T(E + 'G-A 헛잣대 — BASE 는 여섯 종 머리마다 .pdrag 1(잣대가 산다 · 목차노트 목록은 BASE 에 없다)', pd and all(x == 1 for x in pd.values()) and len(pd) == 6
                  and not (ks.get('mok') or {}).get('info'), pd)
        # ── G-B ──
        N_, B_ = RES.get('pit/%s/NEW' % eng), RES.get('pit/%s/BASE' % eng)
        if N_:
            if N_.get('exc'):
                T(E + 'G-B 예외 0', False, N_['exc'])
            w0, w1, wh, wc, w10 = (N_.get(k) or {} for k in ('w0', 'w1', 'wHand', 'wChar', 'w10'))
            HEAD = '🗒 판례 2021후10374 「{판시사항}」 [햄찌] 09.04 22:05'
            T(E + 'G-B 머리 글자 = 「%s」' % HEAD, w0.get('title') == HEAD, w0.get('title'))
            T(E + 'G-B 같은 칩 두 번 = 닫힘(키에 머리 글자 · 새 판에서도)', N_.get('toggleClosed') and bool(w1), [N_.get('toggleClosed'), bool(w1)])
            T(E + 'G-B 회색 줄 = 「햄찌 · 09.04 22:05」 · 「GAS」 0', w0.get('grey') == ['햄찌 · 09.04 22:05'] and w0.get('gas') is False, [w0.get('grey'), w0.get('gas')])
            T(E + 'G-B 단추 = 「✎ 수정 저장」「🗑 삭제」 둘 · 🔒 0', w0.get('btns') == ['✎ 수정 저장', '🗑 삭제'] and w0.get('lock') is False, [w0.get('btns'), w0.get('lock')])
            sv = N_.get('saved')
            T(E + 'G-B 옛 priv:true 레코드를 이 창에서 저장 → 저장된 값에 priv 키 없음 · 사람 햄찌 그대로 · 글 = 친 글', isinstance(sv, dict) and 'priv' not in sv and sv.get('who') == '햄찌'
              and '10번째 줄' in (sv.get('t') or ''), sv and {k: (v if k != 't' else v[-40:]) for k, v in sv.items()})
            h0, h1, h2, h3 = g(w1, 'ta', 'h'), g(wh, 'ta', 'h'), g(wc, 'ta', 'h'), g(w10, 'ta', 'h')
            I(E + 'G-B B-4 칸 높이 — 처음 · 손 +120 · 한 글자 · 10줄 더 (시안 헤드리스 실측 77 · 197 · 197 · 279)', [h0, h1, h2, h3, 'sh', g(w10, 'ta', 'sh')])
            T(E + 'G-B B-4 처음 칸 = 글 높이(scrollHeight+2 · min 74)', near(h0, max(74, (g(w1, 'ta', 'sh') or 0) + 2), 2), [h0, g(w1, 'ta', 'sh')])
            T(E + 'G-B B-4 손끌기 +120 → 칸 +120(±4 · resize:vertical 남음) · %s' % N_.get('handMode'), near((h1 or 0) - (h0 or 0), 120, 4), [h0, h1])
            T(E + 'G-B B-4 한 글자 → 손 높이 그대로(±1)', near(h2, h1, 1), [h1, h2])
            T(E + 'G-B B-4 10줄 더 → 칸이 늘어남 · 칸 = scrollHeight+2(±2)', (h3 or 0) > (h2 or 0) + 60 and near(h3, (g(w10, 'ta', 'sh') or 0) + 2, 2), [h2, h3, g(w10, 'ta', 'sh')])
            T(E + 'G-B B-4 창 아래 ≤ 화면 · 칸 전체가 창 안 · 저장 단추 elementFromPoint 로 눌림', g(w10, 'rect', 'b') is not None and g(w10, 'rect', 'b') <= w10.get('innerH', 0) + 0.5
              and g(w10, 'ta', 'rect', 'b') <= g(w10, 'rect', 'b') + 0.5 and g(w10, 'saveHit', 'on'), [g(w10, 'rect'), g(w10, 'ta', 'rect'), g(w10, 'saveHit')])
            T(E + 'G-B B-4 S.popCfg.fn.h=240 을 심어도 칸이 글을 안 가림(창 높이 = 내용 · 창 안 스크롤 0)', w10.get('style', {}).get('h') == '' and
              (g(w10, 'pscroll', 'sh') or 0) <= (g(w10, 'pscroll', 'ch') or 0) + 1 and near(h3, (g(w10, 'ta', 'sh') or 0) + 2, 2), [w10.get('style'), w10.get('pscroll'), g(w10, 'rect', 'h')])
            T(E + 'G-B 저장 단추 누름 → 저장', N_.get('saveTap') and isinstance(sv, dict), N_.get('saveTap'))
            FN = {'w': 471, 'h': 240, 'x': 640, 'y': 432}
            T(E + 'G-B 누구?·메모 목록(다른 fn 창) 크기 기억 무변 — S.popCfg.fn = 심은 값 · 누구? 창 높이 240', N_.get('cfgAfter') == FN and N_.get('cfgSaved') == FN
              and near(g(N_, 'who', 'rect', 'h'), 240, 1), [N_.get('cfgAfter'), N_.get('cfgSaved'), g(N_, 'who', 'rect', 'h')])
            # G-B5
            def chipok(c):
                cs = (c or {}).get('chips') or []
                return len(cs) == 1 and cs[0]['cls'] == 'chip c-memo' and cs[0]['own'] == '🗒 1' and cs[0]['who'] == ['햄찌']
            T(E + 'G-B5 판례 3단 머리 메모 칩 = 2단 카드와 같은 꼴(chip c-memo · 「🗒 1」 + 햄찌 딱지)', chipok(N_.get('chip3')) and chipok(N_.get('chip2')), [N_.get('chip3'), N_.get('chip2')])
            T(E + 'G-B5 3단 칩 클릭 → 메모 목록(pitlist|특허|2021후10374) · 2단 칩도', g(N_, 'chip3pop', 'pk') == 'pitlist|특허|' + PREC and g(N_, 'chip2pop', 'pk') == 'pitlist|특허|' + PREC,
              [N_.get('chip3tap'), g(N_, 'chip3pop', 'pk'), g(N_, 'chip2pop', 'pk')])
            T(E + 'G-B5 조문 3단(메모 심은 제129조) 같은 꼴 · 클릭 → 조문 메모 목록', chipok(N_.get('chipJo')) and g(N_, 'chipJoPop', 'pk') == 'pitlist|jo|특허법:제129조',
              [N_.get('chipJo'), g(N_, 'chipJoPop', 'pk'), g(N_, 'chipJoPop', 'title')])
            en = [x for x in (N_.get('errs') or []) if not NOISE(x)]
            T(E + 'G-B JS 오류 0', not en, en[:4])
        if B_ and not B_.get('exc'):
            bw0, bw10 = B_.get('w0') or {}, B_.get('w10') or {}
            live = ((bw0.get('title') or '').startswith('🗒 포스트잇 · ') and any('GAS' in x for x in bw0.get('grey') or []) and '🔒 비공개' in (bw0.get('btns') or [])
                    and 'priv' in (B_.get('saved') or {}) and (g(bw10, 'ta', 'sh') or 0) > (g(bw10, 'ta', 'h') or 0) + 20)
            T(E + 'G-B 헛잣대 — BASE 는 머리 「포스트잇 · 」·GAS 줄·🔒·priv 남음·10줄에 칸 안 늘어남(잣대가 산다)', live,
              [bw0.get('title'), bw0.get('grey'), bw0.get('btns'), 'priv' in (B_.get('saved') or {}), g(bw10, 'ta', 'h'), g(bw10, 'ta', 'sh')])
            bc = (B_.get('chip3') or {}).get('chips') or []
            T(E + 'G-B5 헛잣대 — BASE 3단 칩 = 「🗒 메모 1」(c-quiz · 사람 없음)', bc and bc[0]['cls'] == 'chip c-quiz' and bc[0]['text'] == '🗒 메모 1', bc)
        # ── G-C ──
        CN, CB = RES.get('cards/%s/NEW' % eng), RES.get('cards/%s/BASE' % eng)
        if CN and CB:
            for key in GT['cards']:
                sn_ = {x['ck']: x for x in (CN.get('scan') or {}).get(key) or []}
                sb_ = {x['ck']: x for x in (CB.get('scan') or {}).get(key) or []}
                n = len(GT['cards'][key])
                T(E + 'G-C %s %d 전수 — 「2차 레일로」 0 · fm 칩 「기출:」 0 · 빈 top 줄 0' % (key, n),
                  len(sn_) == n and all(not v.get('none') and not v['rail'] and v['gi'] == 0 and v['emptyTop'] == 0 for v in sn_.values()),
                  [(k[:20], v.get('rail'), v.get('gi'), v.get('emptyTop')) for k, v in sn_.items() if v.get('none') or v.get('rail') or v.get('gi') or v.get('emptyTop')][:5])
                bad = [k for k in sn_ if sn_[k].get('fm') != [c for c in (sb_.get(k) or {}).get('fm') or [] if not c.startswith(('기출:', '연결사례:', '조문:'))]]   # A-6(a) 9/30 — c2card D-1: fm 「연결사례:」 칩은 ↩링크·✎ 연결로 · C-3: fm 「조문:」 칩은 설(N) + 조문 글자 링크(span.c2jo)로 바뀜(바탕 칩에서도 뺌)
                T(E + 'G-C %s — 다른 fm 칩(연결판례·비고·중요도·사례번호…) = 바탕에서 「기출:」·「연결사례:」·「조문:」 만 뺀 것' % key, not bad and len(sb_) == n,
                  [(k[:20], sn_[k].get('fm'), (sb_.get(k) or {}).get('fm')) for k in bad[:3]])
                badtop = [k for k in sn_ if [x['kids'] for x in sn_[k].get('top') or []] != [[c for c in x['kids'] if '2차 레일로' not in c] for x in (sb_.get(k) or {}).get('top') or [] if [c for c in x['kids'] if '2차 레일로' not in c]]]
                T(E + 'G-C %s — top 줄 = 바탕 top 줄에서 레일로 단추만 뺀 것(점수·PDF 칩 그대로)' % key, not badtop, [(k[:20], sn_[k].get('top'), (sb_.get(k) or {}).get('top')) for k in badtop[:2]])
                nv = (GT.get('cards_val') or {}).get(key)
                T(E + 'G-C %s 헛잣대 — BASE 는 전수에 「2차 레일로」 · 값 있는 %s장에 「기출:」 칩' % (key, nv), sb_ and all(v['rail'] for v in sb_.values())
                  and sum(1 for v in sb_.values() if v['gi'] >= 1) == nv, [len(sb_), sum(1 for v in sb_.values() if v['gi'] >= 1), nv])
            sc = {x['ck']: x for x in (CN.get('scan') or {}).get('기출|특허') or []}.get(CK_SCORE) or {}
            T(E + 'G-C 점수 있는 카드(특허 26-63-1) — top 줄에 점수 칩 그대로', any('점' in c and 'c-alias' in c for t in sc.get('top') or [] for c in t['kids']), sc.get('top'))
            en = [x for x in (CN.get('errs') or []) if not NOISE(x)]
            T(E + 'G-C JS 오류 0', not en, en[:4])
        # ── G-D ──
        M = RES.get('mok/%s/NEW' % eng)
        if M:
            if M.get('exc'):
                T(E + 'G-D 예외 0', False, M['exc'])
            for law, sh in LAWS:
                Lw = (M.get('law') or {}).get(sh) or {}
                b, lst = Lw.get('btn') or {}, Lw.get('list') or {}
                n = GT[sh]['n']
                T(E + 'G-D %s 단추 = 「목차노트 %d」 · 켜짐 · 자리 = 「2차」 탭 바로 오른쪽' % (sh, n), b.get('text') == '목차노트 %d' % n and not b.get('dis')
                  and (b.get('prev') or '').startswith('2차') and g(b, 'rect', 'x') > g(b, 'prevR', 'r'), b)   # A-6(a) 9/30 — mok_popup_phone A-1·A-2: 「목차노트 N」 = 맨 윗줄 탭(「2차」 바로 오른쪽) · 보드 머리 단추 걷음 · 옛: 「사례 N」 알약 오른쪽
                rows = lst.get('rows') or []
                T(E + 'G-D %s 목록 — 머리 「📑 목차노트 — %s %d」 · 줄 수 = %d' % (sh, sh, n, n), lst.get('title') == '📑 목차노트 — %s %d' % (sh, n) and lst.get('n') == n, [lst.get('title'), lst.get('n')])
                lr_, br_ = lst.get('rect') or {}, b.get('rect') or {}
                T(E + 'G-D %s 목록 창 폭 470 · 자리 = 단추 바로 아래(8px · 기억 자리 없을 때)' % sh, near(lr_.get('w'), 470, 1) and near(lr_.get('y'), (br_.get('b') or 0) + 8, 1.5)
                  and near(lr_.get('x'), min(br_.get('x') or 0, 1440 - 470 - 8), 1.5), [lr_, br_])
                T(E + 'G-D %s 차례 = 번호 마디 오름 · 같으면 이름 · 번호 없는 것 맨 아래(잣대 = 파이썬 재셈)' % sh, [r['note'] for r in rows] == GT[sh]['order'],
                  [(i, r['note'], GT[sh]['order'][i]) for i, r in enumerate(rows) if i < len(GT[sh]['order']) and r['note'] != GT[sh]['order'][i]][:3])
                T(E + 'G-D %s 들여쓰기 10+(마디−1)×16 · 「==」 줄 굵게' % sh, all(near(r['pad'], GT[sh]['pad'][r['note']], 0.5) for r in rows)
                  and sorted(r['note'] for r in rows if int(r['fw'] or 400) >= 700) == sorted(GT[sh]['bold']),
                  [(r['note'], r['pad'], r['fw']) for r in rows if not near(r['pad'], GT[sh]['pad'][r['note']], 0.5)][:3])
                want = {f: ['%s %d' % (k, v) for k, v in GT[sh]['cite'][f].items() if v] for f in GT[sh]['order']}
                got = {r['note']: [c['t'] for c in r['chips']] for r in rows}
                T(E + 'G-D %s 칩 = 인용 카드 수(기출·사례·GS·판례 · 0 은 안 그림) — 줄마다 잣대와 같음 · 합 %s' % (sh, GT[sh]['tot']), got == want,
                  [(f, got.get(f), want[f]) for f in want if got.get(f) != want[f]][:3])
                txt_ = lst.get('text') or ''
                T(E + 'G-D %s 「N줄」·「빈 노트」 글자 0' % sh, not re.search(r'\d+\s*줄(?![가-힣])', txt_) and '빈 노트' not in txt_, re.findall(r'.{6}\d+\s*줄.{3}', txt_)[:3])
                T(E + 'G-D %s 목록 두 번 = 닫힘' % sh, Lw.get('tap2') and Lw.get('closed'), [Lw.get('tap2'), Lw.get('closed')])
            P_ = (M.get('law') or {}).get('특허') or {}
            r96 = [r for r in g(P_, 'list', 'rows') or [] if r['note'] == N96]
            T(E + 'G-D 특허 9.6 칩 = 기출 5 · 사례 8 · 판례 24', r96 and [c['t'] for c in r96[0]['chips']] == ['기출 5', '사례 8', '판례 24'], r96 and r96[0]['chips'])
            cc = {c['t'].split()[0]: (c['bg'], c['fg'], c['fs']) for r in g(P_, 'list', 'rows') or [] for c in r['chips']}
            T(E + 'G-D 칩 색(시안) — 기출 #e8f0fb/#2f5fb3 · 사례 #efeae0/#6b5f45 · GS #f3e8fb/#7a3fb0 · 판례 #f1f1ef/#77736b · 10.5px',
              cc.get('기출') == ('rgb(232, 240, 251)', 'rgb(47, 95, 179)', '10.5px') and cc.get('사례') == ('rgb(239, 234, 224)', 'rgb(107, 95, 69)', '10.5px')
              and cc.get('GS') == ('rgb(243, 232, 251)', 'rgb(122, 63, 176)', '10.5px') and cc.get('판례') == ('rgb(241, 241, 239)', 'rgb(119, 115, 107)', '10.5px'), cc)
            nr = P_.get('noteRead') or {}
            T(E + 'G-D 특허 9.6 줄 누름 → 그 노트 팝업(머리 「📄 9.6…」 · 딱지 0)', P_.get('rowTap') and nr.get('found') and not (nr.get('badge') or [])   # A-6(a) 9/30 — mok_popup_phone C·D: 노트 팝업 머리 줄(「N단」 딱지 포함) 걷음 · 옛: 「2단」 딱지
              and (nr.get('title') or '').startswith('📄 ' + N96), [P_.get('rowTap'), nr.get('title'), nr.get('badge')])
            on = [r for r in g(P_, 'list2', 'rows') or [] if r['on']]
            T(E + 'G-D 누른 줄 = 옅은 파랑(#e8f0fb)으로 남음', len(on) == 1 and on[0]['note'] == N96 and on[0]['bg'] == 'rgb(232, 240, 251)', on)
            lr, nrr = g(P_, 'list', 'rect') or {}, nr.get('rect') or {}
            I(E + 'G-D 1440 목록·노트 자리(노트 = 목록 오른쪽 · 화면 안으로 당김)', {'list': [lr.get('x'), lr.get('y'), lr.get('w'), lr.get('h')], 'note': [nrr.get('x'), nrr.get('y'), nrr.get('w'), nrr.get('h')]})
            T(E + 'G-D 1440 노트 팝업 = 목록보다 오른쪽 · 목록과 같은 높이에서 · 화면 안', nrr.get('x', 0) > lr.get('x', 0) + 150 and nrr.get('r', 9e9) <= 1440 + 0.5 and nrr.get('x', -1) >= 0
              and near(nrr.get('y'), lr.get('y'), 1) and nrr.get('b', 9e9) <= 900 + 0.5, [lr, nrr])
            T(E + 'G-D 디보 = 「목차노트 49」 켜짐(사용자 9/23 14:00 — 지시서는 「—」 disabled) · 칩 0', g(M, 'law', '디보', 'btn', 'text') == '목차노트 49' and not g(M, 'law', '디보', 'btn', 'dis')
              and all(not r['chips'] for r in g(M, 'law', '디보', 'list', 'rows') or [1]), g(M, 'law', '디보', 'btn'))
            en = [x for x in (M.get('errs') or []) if not NOISE(x)]
            T(E + 'G-D JS 오류 0', not en, en[:4])
        MB = RES.get('mok/%s/BASE' % eng)
        if MB:
            T(E + 'G-D 헛잣대 — BASE 에는 「목차노트」 단추가 없다', all(not g(MB, 'law', sh, 'btn') for _, sh in LAWS), [g(MB, 'law', sh, 'btn') for _, sh in LAWS])
        # ── G-E ──
        NN, NB = RES.get('note/%s/NEW' % eng), RES.get('note/%s/BASE' % eng)
        if NN:
            if NN.get('exc'):
                T(E + 'G-E 예외 0', False, NN['exc'])
            rows = g(NN, 'n96', 'rows') or []
            tbl = {1: 15, 5: 0, 6: 27, 7: 42, 13: 15, 14: 42, 15: 57, 17: 72}
            T(E + 'G-E 9.6 잣대 표(줄1 15 · 줄5 0 · 줄6 27 · 줄7 42 · 줄13 15 · 줄14 42 · 줄15 57 · 줄17 72) ±1', rows and all(near(rows[k]['pad'], v, 1) for k, v in tbl.items()),
              {k: rows[k]['pad'] for k in tbl if k < len(rows)})
            T(E + 'G-E 9.6 전 줄(%d) padding = 계단 식(제목 (h−1)×15 · 본문 직전 제목×15+12 + 탭×15)' % len(rows), rows and len(rows) == len(GT['pad96'])
              and all(near(r['pad'], GT['pad96'][i], 0.5) for i, r in enumerate(rows)), [(i, r['pad'], GT['pad96'][i]) for i, r in enumerate(rows) if not near(r['pad'], GT['pad96'][i], 0.5)][:4])
            tabr = [r for r in rows if r['i'] and not r['h'] and r['fx'] is not None]
            T(E + 'G-E 탭 줄(%d) 첫 글자 x = 그 줄 padding 시작(탭 폭 0 · ±1)' % len(tabr), tabr and all(near(r['fx'], r['padStart'], 1) for r in tabr),
              [(r['ri'], r['fx'], r['padStart']) for r in tabr if not near(r['fx'], r['padStart'], 1)][:4])
            T(E + 'G-E 줄마다 .ln 글자(접기 표시·칩 뺀 것) = row.t(글자 수 불변)', rows and all(r['plainEq'] for r in rows), [(r['ri'], r['plainLen'], r['tLen']) for r in rows if not r['plainEq']][:4])
            hr = [r for r in rows if r['h'] and r['htog']]
            T(E + 'G-E 9.6 접기 표시 폭 9 · 여백 2 · 제목 첫 글자와 간격 2±1px(제목 %d줄)' % len(hr), hr and all(near(r['htog']['w'], 9, 0.5) and near(r['htog']['mr'], 2, 0.1)
              and near((r['fx'] or 0) - r['htog']['r'], 2, 1) for r in hr), [(r['ri'], r['htog'], r['fx']) for r in hr][:3])
            T(E + 'G-E 「#」 뒤 한 칸까지 mdhash 안(제목 줄)', hr and all((r['hash'] or '').endswith(' ') for r in hr), [r['hash'] for r in hr][:4])
            mm = {0: (2, 2), 1: (7, 2), 2: (5, 2), 3: (4, 1)}
            T(E + 'G-E 줄 간격 — 본문 2/2 · h1 7/2 · h2 5/2 · h3 4/1', rows and all((r['mt'], r['mb']) == mm[min(r['h'], 3)] for r in rows),
              [(r['ri'], r['h'], r['mt'], r['mb']) for r in rows if (r['mt'], r['mb']) != mm[min(r['h'], 3)]][:4])
            fs = {1: '17px', 2: '15px', 3: '13.5px'}
            T(E + 'G-E 제목 글자 크기 그대로(h1 17 · h2 15 · h3 13.5)', all(r['fs'] == fs[min(r['h'], 3)] for r in rows if r['h']), [(r['ri'], r['h'], r['fs']) for r in rows if r['h']][:4])
            ok_o = True; bad_o = []
            for k, v in (NN.get('others') or {}).items():
                rs = v.get('rows') or []
                cur = 0; exp = []
                for r in rs:
                    if r['h']:
                        cur = r['h']; exp.append((r['h'] - 1) * 15)
                    else:
                        exp.append((cur * 15 + 12 if cur else 0) + r['i'] * 15)
                good = rs and all(r['plainEq'] for r in rs) and all(near(r['pad'], exp[i], 0.5) for i, r in enumerate(rs)) \
                    and all(near(r['fx'], r['padStart'], 1) for r in rs if r['i'] and not r['h'] and r['fx'] is not None)
                if not good:
                    ok_o = False; bad_o.append(k)
            T(E + 'G-E 상표·민소 노트 여섯 — 글자 = row.t · 계단 식 · 탭 폭 0', ok_o and len(NN.get('others') or {}) == 6, bad_o)
            ok_ = RES.get('oldkey')
            T(E + 'G-E ★ 새 판에서 줄1 「정정심판{136조}」 에 붙인 포스트잇 키 = 바탕 판에서 붙인 키(이사 0)', ok_ and (NN.get('newKeys') or [None])[0] == ok_, [ok_, NN.get('newKeys')])
            ol = NN.get('oldLine') or {}
            T(E + 'G-E ★ 옛 키(바탕 판에서 만든 키)를 새 판에 심으면 같은 단어에 밑줄 · 깃발(고아 0)', ol.get('pitw') and len(ol['pitw']) == 1 and ol['pitw'][0]['w'] == '정정심판{136조}'
              and ol.get('flags') and all('orph' not in f['cls'] for f in ol['flags']), ol)
            sh_ = NN.get('sumHtog') or []; ch_ = NN.get('cardHtog') or []
            T(E + 'G-E 요약본(2021후10374) 접기 표시 폭 9 · 여백 2 · 간격 2±1 (%d줄)' % len(sh_), sh_ and all(near(x['w'], 9, 0.5) and near(x['mr'], 2, 0.1) and near(x['gap'], 2, 1) for x in sh_), sh_[:3])
            T(E + 'G-E 2차 카드(25-62-1) 접기 표시 폭 9 · 제목 첫 글자와 간격 2±1 (%d줄 · 제목 줄이 flex 라 여백 −3 + 틈 5)' % len(ch_), ch_ and all(near(x['w'], 9, 0.5) and near(x['gap'], 2, 1) for x in ch_),
              ch_[:3])
            if NB:
                I(E + 'G-E 바탕 접기 표시 간격(요약본 · 2차 카드 · 노트 9.6)', {'sum': sorted({x['gap'] for x in NB.get('sumHtog') or []})[:4], 'card': sorted({x['gap'] for x in NB.get('cardHtog') or []})[:4],
                  'note': sorted({round((r['fx'] or 0) - r['htog']['r'], 1) for r in g(NB, 'n96', 'rows') or [] if r['htog']})[:4]})
            if NB:
                T(E + 'G-E 요약본 줄 들여쓰기 = 바탕과 같음(padding 표 %d줄)' % len(NN.get('sumPad') or []), NN.get('sumPad') == NB.get('sumPad') and NN.get('sumPad'),
                  [x for x in zip(NN.get('sumPad') or [], NB.get('sumPad') or []) if x[0] != x[1]][:3])
                T(E + 'G-E 2차 카드 본문·임베드 상자 줄 들여쓰기 = 바탕과 같음(padding 표 %d줄)' % len(NN.get('cardPad') or []), NN.get('cardPad') == NB.get('cardPad') and NN.get('cardPad'),
                  [x for x in zip(NN.get('cardPad') or [], NB.get('cardPad') or []) if x[0] != x[1]][:3])
                en_, eb_ = g(NN, 'n96', 'emb') or [], g(NB, 'n96', 'emb') or []
                T(E + 'G-E 노트 팝업 안 임베드 상자 줄(%d) — 들여쓰기·줄 간격·탭 = 바탕과 같음(노트 줄만 바뀐다)' % len(en_), en_ and en_ == eb_,
                  [x for x in zip(en_, eb_) if x[0] != x[1]][:3])
            en = [x for x in (NN.get('errs') or []) if not NOISE(x)]
            T(E + 'G-E JS 오류 0', not en, en[:4])
        if NB and not NB.get('exc'):
            rb = g(NB, 'n96', 'rows') or []
            tb = [r for r in rb if r['i'] and not r['h'] and r['fx'] is not None]
            T(E + 'G-E 헛잣대 — BASE 는 탭 줄 첫 글자가 패딩 시작보다 탭만큼 오른쪽 · 접기 표시 12/5 · 계단 식과 다름',
              tb and all(r['fx'] - r['padStart'] > 10 for r in tb) and all(near(r['htog']['w'], 12, 0.5) for r in rb if r['htog'])
              and any(not near(r['pad'], GT['pad96'][i], 0.5) for i, r in enumerate(rb)), [(r['ri'], r['fx'], r['padStart']) for r in tb][:3])
            T(E + 'G-E 헛잣대 — BASE 도 줄 글자 = row.t(글자 수 불변 잣대는 두 판 공통)', rb and all(r['plainEq'] for r in rb), [r['ri'] for r in rb if not r['plainEq']][:4])
        # ── G-F ──
        Q, QB = RES.get('eq/%s/NEW' % eng), RES.get('eq/%s/BASE' % eng)
        rows96 = G['rows96']; t8 = rows96[8]['t']; t111 = G['rows41'][111]['t']
        if Q:
            if Q.get('exc'):
                T(E + 'G-F 예외 0', False, Q['exc'])
            b1 = Q.get('box1') or {}
            T(E + 'G-F ✎ 칸 글 = row.t(꼬리 포함 · 떼지 않음) · 칸 옆 「🔒 ^5b53b7」', b1.get('val') == t8 and g(b1, 'chip', 't') == '🔒 ^5b53b7'
              and g(b1, 'chip', 'title') == '블록번호 — 지우거나 옮기면 저장이 막힌다', [Q.get('o1_menu'), b1])
            q1 = Q.get('q1') or []
            T(E + 'G-F 본문만 고치고 저장 → 큐 after 끝 = 「   ^5b53b7」(세 칸) · before = row.t', len(q1) == 1 and q1[0]['after'].endswith('   ^5b53b7') and '명도(고침)' in q1[0]['after']
              and q1[0]['before'] == t8, q1)
            for k, why, lab in (('2', '없어졌다', '번호 지우고 저장'), ('3', '앞 공백이 바뀌었다', '앞 세 칸을 탭으로'), ('4', '뒤에 글이 더 있다', '번호 뒤에 줄 더 쓰기')):
                bx = Q.get('box' + k) or {}
                T(E + 'G-F %s → 막힘(큐 0) · 칸 아래 빨간 까닭 「%s」 · 「원래 꼬리로 되돌리기」' % (lab, why), Q.get('q' + k) == [] and bx.get('whyShown') and why in (bx.get('why') or '') and bx.get('fix'),
                  [Q.get('q' + k), bx.get('why')])
            b5, q5 = Q.get('box5') or {}, Q.get('q5') or []
            T(E + 'G-F 「원래 꼬리로 되돌리기」 → 꼬리만 원래대로(본문 고친 것·더 쓴 줄은 둔다) → 저장됨', b5.get('val', '').endswith('   ^5b53b7') and '명도(고침)' in b5.get('val', '')
              and '추가한 줄' in b5.get('val', '') and not b5.get('whyShown') and len(q5) == 1 and q5[0]['after'] == b5.get('val'), [b5.get('val'), q5])
            b6, q6 = Q.get('box6') or {}, Q.get('q6') or []
            T(E + 'G-F 4.1 111줄(탭+띄어쓰기+^78111f) — 칸 = row.t · 탭 지우면 막힘 · 본문만 고치면 after 끝 「\\t ^78111f」', b6.get('val') == t111 and Q.get('q6b') == []
              and '앞 공백이 바뀌었다' in (g(Q, 'box6b', 'why') or '') and len(q6) == 1 and q6[0]['after'].endswith('\t ^78111f') and '필요함' in q6[0]['after'],
              [g(Q, 'box6b', 'why'), q6])
            for k, lab in (('o7a', '공백+^id 줄(3.3.2 36줄 「\\t ^bf52e2」)'), ('o7b', '맨 ^id 줄(3.4 86줄 「^0c5c53」)')):
                T(E + 'G-F 줄 전체가 ^id — %s → ✎ 안 열림 · 토스트 「블록번호 줄 — 고치지 않는다」' % lab, Q.get(k + '_menu') and Q.get(k + '_box') is None
                  and any('블록번호 줄 — 고치지 않는다' in t for t in Q.get(k + '_toast') or []), [Q.get(k + '_menu'), Q.get(k + '_box'), Q.get(k + '_toast')])
            bl = GT.get('bl5b') or G.get('bl5b') or {}
            want = ' · '.join('%s %d' % (k, len(bl.get(k) or [])) for k in ('기출', '사례', 'GS', '판례', '노트'))
            c8 = Q.get('conf8') or []
            T(E + 'G-F 꼬리 줄 비우기 → 확인 창(부르는 곳 = backlink 「%s」) · 취소 → 큐 무변' % want, len(c8) == 1 and ('부르는 곳: ' + want) in c8[0] and '^5b53b7' in c8[0]
              and Q.get('q8') == [], [c8, Q.get('q8')])
            q8b = Q.get('q8b') or []
            T(E + 'G-F 확인 → 삭제 항목(after \'\')이 큐에', len(q8b) == 1 and q8b[0]['after'] == '' and q8b[0]['before'] == t8, q8b)
            b9, b9b = Q.get('box9') or {}, Q.get('box9b') or {}
            q9 = Q.get('q9') or []
            T(E + 'G-F 다시 고치기(✎ 수정 큐 → ✎ 다시 고치기) — 칩 · 번호 지우면 같은 막힘 · 큐 무변', Q.get('redoTap') and b9.get('kind') == 'form' and g(b9, 'chip', 't') == '🔒 ^5b53b7'
              and b9b.get('whyShown') and '없어졌다' in (b9b.get('why') or '') and len(q9) == 1 and '첫 고침' in q9[0]['after'], [Q.get('redoTap'), b9, b9b.get('why'), q9])
            bd = Q.get('blkDirect') or {}
            T(E + 'G-F 꼬리 줄 비우기 확인 창 — 노트 밖 줄(판례 요약본·2차 카드)은 수 없이 확인만 · backlink 에 없는 노트 줄은 모두 0 · 취소 = 안 적힘 · 확인 = 적힘(지은 값으로 함수 직접 · 데이터에 노트 밖 꼬리 줄 0)',
              all(len((bd.get(k) or {}).get('conf') or []) == 1 and not bd[k]['ranOnCancel'] and bd[k]['ranOnOk'] for k in ('prec', 'card', 'noteNone'))
              and all('부르는 곳:' not in bd[k]['conf'][0] and '^abc123' in bd[k]['conf'][0] for k in ('prec', 'card'))
              and '부르는 곳: 기출 0 · 사례 0 · GS 0 · 판례 0 · 노트 0' in ((bd.get('noteNone') or {}).get('conf') or [''])[0], bd)
            en = [x for x in (Q.get('errs') or []) if not NOISE(x)]
            T(E + 'G-F JS 오류 0', not en, en[:4])
        if QB and not QB.get('exc'):
            T(E + 'G-F 헛잣대 — BASE 는 번호를 지워도 저장된다 · 칩 없음 · 확인 창 없음', len(QB.get('q2') or []) == 1 and not (QB.get('box1') or {}).get('chip') and not QB.get('conf8'),
              [QB.get('q2'), QB.get('box1'), QB.get('conf8')])
        # ── 아이패드 ──
        for W in (768, 1024):
            D = RES.get('pad/%s/%d' % (eng, W))
            if not D:
                continue
            E2 = '[%s 아이패드 %d] ' % (eng, W)
            M2 = g(D, 'mok', 'law', '특허') or {}
            T(E2 + '목차노트 단추 톡 → 목록 70 · 9.6 톡 → 노트(딱지 0) · 노트 창이 화면 안(좌우·아래)', M2.get('tap') and g(M2, 'list', 'n') == 70 and M2.get('rowTap')
              and not (g(M2, 'noteRead', 'badge') or []) and (g(M2, 'noteRead', 'rect', 'x') or -1) >= 0 and (g(M2, 'noteRead', 'rect', 'r') or 9e9) <= W + 0.5   # A-6(a) 9/30 — mok_popup_phone C·D: 딱지 0(목록 70·톡·화면 안 조건 그대로)
              and (g(M2, 'noteRead', 'rect', 'y') or -1) >= 0 and (g(M2, 'noteRead', 'rect', 'b') or 9e9) <= H_OF[W] + 0.5,
              [M2.get('tap'), g(M2, 'list', 'n'), M2.get('rowTap'), g(M2, 'noteRead', 'rect')])
            a0, a1 = g(M2, 'note', 'pos') or {}, g(M2, 'noteAfter', 'pos') or {}
            T(E2 + '노트 머리 끌기(-60,+40) · %s' % M2.get('noteDrag'), near(a1.get('l', 0) - a0.get('l', 0), -60, 3) and near(a1.get('t', 0) - a0.get('t', 0), 40, 3), [a0, a1])
            nr2 = g(M2, 'noteRead', 'rows') or []
            T(E2 + '노트 9.6 계단 식 · 탭 폭 0', nr2 and all(near(r['pad'], GT['pad96'][i], 0.5) for i, r in enumerate(nr2)) and all(near(r['fx'], r['padStart'], 1) for r in nr2 if r['i'] and not r['h'] and r['fx'] is not None), len(nr2))
            PT = D.get('pit') or {}
            w10 = PT.get('w10') or {}
            T(E2 + '포스트잇 톡 → 10줄 → 칸 = 글 높이 · 창 아래 ≤ 화면 · 저장 단추 보임(elementFromPoint) → 톡 → 저장', near(g(w10, 'ta', 'h'), (g(w10, 'ta', 'sh') or 0) + 2, 2)
              and (g(w10, 'rect', 'b') or 9e9) <= H_OF[W] + 0.5 and g(w10, 'saveHit', 'on') and PT.get('saveTap') and isinstance(PT.get('saved'), dict) and 'priv' not in PT.get('saved'),
              [g(w10, 'ta'), g(w10, 'rect'), g(w10, 'saveHit'), PT.get('saveTap'), PT.get('exc')])
            T(E2 + '포스트잇 창 오른쪽 ≤ 화면 · 삭제 단추도 눌림(책상 기억 자리 x=640·폭 471 을 심은 채 — 좁은 화면이면 왼쪽으로 당김)',
              (g(w10, 'rect', 'r') or 9e9) <= W + 0.5 and (g(w10, 'rect', 'x') or -1) >= 0 and g(w10, 'delHit', 'on'), [g(w10, 'rect'), g(w10, 'delHit')])
            EQ = D.get('eq') or {}
            T(E2 + '✎ 길게 눌러 메뉴 → ✎ 수정 → 번호 지우고 저장 톡 → 막힘 · 까닭 · %s' % EQ.get('o2_lp'), EQ.get('o2') and g(EQ, 'box2', 'whyShown') and '없어졌다' in (g(EQ, 'box2', 'why') or '')
              and EQ.get('q2') == [] and EQ.get('saveTap2'), [EQ.get('o2'), EQ.get('o2_menu'), g(EQ, 'box2'), EQ.get('q2'), EQ.get('exc')])
            en = [x for s in ('mok', 'pit', 'eq') for x in (g(D, s, 'errs') or []) if not NOISE(x)]
            T(E2 + 'JS 오류 0', not en, en[:4])
        # ── 폭 1024·768(책상) ──
        WD = RES.get('wide/%s' % eng) or {}
        for W, D in WD.items():
            M3 = g(D, 'law', '특허') or {}
            rr = g(M3, 'list', 'rect') or {}
            wraps = [r for r in g(M3, 'list', 'rows') or [] if (r.get('nmWrap') or {}).get('to') == 'ellipsis' or (r.get('nmWrap') or {}).get('ws') == 'nowrap']
            HH = {1024: 768, 768: 1024}[int(W)]
            T('[%s 폭 %s] 목록 창이 화면 안 · 이름 줄바꿈(말줄임 0) · 노트 창 화면 안(좌우·아래)' % (eng, W), rr.get('x', -1) >= 0 and rr.get('r', 9e9) <= int(W) + 0.5 and not wraps
              and (g(M3, 'noteRead', 'rect', 'r') or 9e9) <= int(W) + 0.5 and (g(M3, 'noteRead', 'rect', 'b') or 9e9) <= HH + 0.5 and (g(M3, 'noteRead', 'rect', 'y') or -1) >= 0,
              [rr, len(wraps), g(M3, 'noteRead', 'rect')])
            I('[%s 폭 %s] 목록·노트 자리' % (eng, W), {'list': rr, 'note': g(M3, 'noteRead', 'rect')})
    p = sum(1 for x in L if x.startswith('PASS')); f = sum(1 for x in L if x.startswith('FAIL'))
    body = '\n'.join(L) + '\n\n합계  PASS %d · FAIL %d  (%.0f초)\n' % (p, f, RES.get('sec', 0))
    print(body)
    wr(os.path.join(OUT, '_harness_jo_pop_moknote_result.txt'), body)
    shots = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and (k == 'shot' or (k in ('card',) and v.endswith('.png'))):
                    shots.append(v)
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(RES)
    for s in sorted(set(shots)):
        if os.path.exists(s):
            wr(os.path.join(SHOTS, os.path.basename(s)[5:]), open(s, 'rb').read())


H_OF = {768: 1024, 1024: 768}

if __name__ == '__main__':
    if '--report' in sys.argv:
        RES = json.load(io.open(os.path.join(WORK, 'raw.json'), encoding='utf-8'))
        G = ground()
        report(RES, G)
    else:
        main()
