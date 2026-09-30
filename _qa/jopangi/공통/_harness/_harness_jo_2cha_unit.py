# -*- coding: utf-8 -*-
"""조판기 2차 「단원별」(민소 기출) · ✎ 단원 재매칭 · 줄 꼴 — _task_jo_2cha_unit §D 관문 하네스.

  NEW  = genie 작업트리 jo/index.html · 데이터 = genie jo/data(⚙ 산출 2cha_단원_민소.json 이 옮겨진 것)
  BASE = `d3dd927` 의 같은 파일(바탕 · 팝업 글자·셀 수 기준이자 헛잣대 · D-7 에서는 「옛 판 기기」)
  엔진 = playwright chromium · webkit — 책상 1440×900(마우스) · 폭 1024·768(줄 넘침 · 캡처) · 아이패드 768×1024 · 1024×768(진짜 터치 · DSF 2)
  끌기 = chromium CDP 터치(끝에서 멈춤) / webkit 신뢰 마우스(playwright webkit 은 톡만 진짜 터치 — 도구 한계)
  網 = 같은 출처만 · GitHub 기록.json 은 SEED 가 창마다 메모리로 대답(두 기기 = 원격 글을 하네스가 넘겨준다 · J19 꼴)
  ?keep=1 = 새로고침해도 저장소를 안 비운다 · ?alt=1 = 2cha_단원_민소.json 대신 자동값을 바꾼 사본(D-6)

쓰기 : python _harness_jo_2cha_unit.py [--out 폴더] [--only desk|sync|pad|wide|build]
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
_NR = _roots.need_n('민소 2차 단원 매핑 json · ⚙ cha2_unit')   # env_lanes_fix(9/29) — N: 작업 폴더 · 없으면(클라우드) 「N: 필요 — 클라우드 불가(…)」 종료 코드 3
import copy, hashlib, http.server, importlib, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

GENIE = _roots.genie()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else HERE
ONLY = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else ''
SHOTS = os.path.join(OUT, '_2cha_unit_shots')
WORK = os.path.join(tempfile.gettempdir(), 'h_jo_2cha_unit')
J = os.path.join(_NR, 'jopangi')
REL = 'jo/index.html'
JOD = os.path.join(GENIE, 'jo')
BASE_REV = 'd3dd927'
BASE_MD5_LF = 'd8f33f906eee303a306d662949a7b686'
UNIT_FILE = '2cha_단원_민소.json'
TESTS = io.open(os.path.join(HERE, '_harness_jo_2cha_unit_tests.js'), encoding='utf-8').read()
IPAD_UA = ('Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 '
           '(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
# §0 표(지시서) — 주단원 분포(번호 → 문제 수 · 합 76)
TABLE0 = {'1.3.1': 2, '1.4': 1, '2.1': 2, '2.1.1': 2, '2.2.1': 2, '2.3': 3, '2.4': 4, '3.1': 1, '3.2': 1, '3.3': 3, '3.4': 1, '3.4.1': 1,
          '3.6.1': 2, '4.1.1': 3, '4.1.2': 4, '4.1.3': 1, '4.2.2': 3, '4.3.1': 2, '4.3.2': 2, '4.4': 2, '5.3': 3, '5.4': 4, '6.1.2': 1,
          '6.3': 1, '6.6': 1, '6.6.1': 1, '6.6.2': 1, '6.6.3': 1, '6.6.4': 1, '7.1': 4, '7.2': 1, '7.3': 2, '7.5': 1, '7.5.1': 1, '7.5.2': 1,
          '7.6': 1, '7.7.1': 1, '8.1': 5, '8.2': 2, '9': 1}
HEADS3 = ['4.1.1. 처분권주의(203조)', '6.6.4.{기시차}기판력 시범,차단효', '9.==재심(451조)== 대기리당사보']
U664 = '6.6.4.{기시차}기판력 시범,차단효'
U411 = '4.1.1. 처분권주의(203조)'
U782 = '7.8.2.{승계}(후발)소송승계-참(81조)인(82조)'
U23 = '2.3. 소송상대리인-법대_임대_무대'
CK251 = 'card|기출|민기출 25-62-1'
POPS3 = ['card|기출|민기출 26-63-1', 'card|기출|민기출 09-46-1-소송상형성권행사-신체상해손배청,상계항변과중복소-기시차,전소변종전발생형성권 변종후행사가부', CK251]
SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.alert=function(){};window.confirm=function(){return true;};window.prompt=function(){return null;};
(function(){var Q=new URLSearchParams(location.search);var nf=window.fetch.bind(window);
window.fetch=function(u,o){o=o||{};var s=String((u&&u.url)||u);
 if(Q.get('alt')==='1'&&/data\/2cha_단원_민소\.json$/.test(s))return nf(s.replace('2cha_단원_민소.json','2cha_단원_민소.alt.json'),o);
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
</script>"""
READY = "!!window.__HU&&typeof render==='function'&&typeof popCard4==='function'"


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
            if p == '/data/2cha_단원_민소.alt.json':
                return os.path.join(WORK, '2cha_단원_민소.alt.json')
            if p.startswith('/data/'):
                return os.path.join(JOD, 'data', p[6:].replace('/', os.sep))
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
    def __init__(self, br, eng, tag, src, W, H, pad=False, q='tok=1', who='꼬까'):
        self.eng, self.tag, self.pad, self.q, self.who = eng, tag, pad, q, who
        self.port = serve(tag, src)
        if pad:
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=IPAD_UA)
        else:
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1)
        self.ctx.route('**/*', route_filter)
        self.pg = self.ctx.new_page()
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' else None)
        self.cdp = self.ctx.new_cdp_session(self.pg) if (eng == 'chromium' and pad) else None
        self.load(q)

    def load(self, q):
        self.pg.goto('http://127.0.0.1:%d/index.html?%s&who=%s' % (self.port, q, urllib.parse.quote(self.who)), wait_until='load', timeout=120000)
        self.pg.wait_for_function(READY, timeout=120000)
        self.pg.wait_for_timeout(1500)

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

    def drag(self, x0, y0, x1, y1, n=12):
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

    def type(self, text):
        self.pg.keyboard.type(text, delay=30); self.pg.wait_for_timeout(250)

    def board(self, law, kind, ord=None):
        self.ev("([l,k,o])=>__HU.board(l,k,o)", [law, kind, ord])
        self.pg.wait_for_timeout(250)

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


def ground():
    """재료 JSON 으로 센 잣대 — 걸침(주단원 밖에서 짚은 문제 수) · 주단원 분포"""
    M = json.load(open(os.path.join(J, '민소', '_민소2차_단원매핑', '_민소2차_단원매핑.json'), encoding='utf-8'))
    U = M['units']
    over, main = Counter(), Counter()
    for p in M['문제']:
        main[p['주단원(제안)']] += 1
        for t in {u['단원'] for s in p['설문'] for u in s['단원']}:
            if t != p['주단원(제안)']:
                over[U[t]] += 1
    return {'over': dict(over), 'main': dict(main), 'units': U}


def edit_flow(p, R, pre, via_search=None):
    """✎ 25-62-1 — 설문 (2) 에 2.3 더하기 · 주단원 7.8.2 · 저장 (via_search = 찾기 칸에 글자를 쳐서 고르기)"""
    at = p.ev("([c,x])=>__HU.rowAt(c,x)", [CK251, 'edit']); R[pre + 'editAt'] = at
    R[pre + 'editOk'] = p.click(at, 700)
    R[pre + 'win0'] = p.ev("__HU.win()")
    at = p.ev("([k,a])=>__HU.winAt(k,a)", ['add', '(2)']); p.click(at, 400)
    R[pre + 'pick'] = p.ev("__HU.pickItems()")
    if via_search:
        at = p.ev("([k])=>__HU.winAt(k)", ['input']); p.click(at, 200)
        p.type(via_search)
        R[pre + 'searched'] = p.ev("__HU.pickItems()")
        items = [x for x in (R[pre + 'searched'] or []) if x['n'] != U664 and not x.get('have')]
        tgt = items[0]['n'] if items else None
        R[pre + 'pickTarget'] = tgt
        at = p.ev("([k,a])=>__HU.winAt(k,a)", ['it', tgt]) if tgt else None
    else:
        at = p.ev("([k,a])=>__HU.winAt(k,a)", ['it', U23])
    R[pre + 'itemOk'] = p.click(at, 400)
    at = p.ev("([k,a])=>__HU.winAt(k,a)", ['rad', U782]); R[pre + 'radOk'] = p.click(at, 300)
    R[pre + 'win1'] = p.ev("__HU.win()")
    at = p.ev("([k])=>__HU.winAt(k)", ['save']); R[pre + 'saveOk'] = p.click(at, 1200)
    p.ev("__HU.quiet()")


# ══════════ 책상 1440×900 — D-2·3·4·5·6·8 · C-8 ══════════
def scen_desk(br, eng, tag, src):
    p = P(br, eng, tag, src, 1440, 900)
    R = {'eng': eng, 'tag': tag}
    try:
        p.board('민사소송법', '기출', 'round')
        R['seg'] = p.ev("__HU.seg()")
        if tag == 'BASE':
            R['cells'] = p.ev("()=>[...document.querySelectorAll('#slot .main .cell[data-ck]')].map(e=>e.dataset.ck)")
            R['pops'] = {}
            for ck in POPS3:
                p.board('민사소송법', '기출', 'round')
                at = p.ev("c=>__HU.cellTitleAt(c)", ck); ok = p.click(at, 300)
                if not ok:
                    p.pg.wait_for_timeout(700); at = p.ev("c=>__HU.cellTitleAt(c)", ck); ok = p.click(at, 300)
                R['pops'][ck] = {'ok': ok, 'pop': p.ev("__HU.popRead()")}
                p.ev("__HU.closePops()")
        else:
            R['list'] = p.ev("__HU.listRead()")
            # D-4 칩 누름 → 노트 팝업(카드 팝업 아님) · 줄 누름 → 카드 팝업(바탕과 같은 글자)
            at = p.ev("([c,x])=>__HU.rowAt(c,x)", [POPS3[0], 'chip']); ok = p.click(at, 300)
            R['chipPop'] = {'at': at, 'ok': ok, 'pop': p.ev("__HU.popRead()")}
            p.ev("__HU.closePops()")
            R['pops'] = {}
            for ck in POPS3:
                p.board('민사소송법', '기출', 'round')
                at = p.ev("([c,x])=>__HU.rowAt(c,x)", [ck, 'title']); ok = p.click(at, 300)
                R['pops'][ck] = {'ok': ok, 'pop': p.ev("__HU.popRead()")}
                p.ev("__HU.closePops()")
            # D-2 단원별
            p.board('민사소송법', '기출', 'unit')
            R['seg_unit'] = p.ev("__HU.seg()")
            R['unit'] = p.ev("__HU.unitRead()")
            R['headPops'] = {}
            for u in HEADS3:
                p.board('민사소송법', '기출', 'unit')
                at = p.ev("([u,x])=>__HU.headAt(u,x)", [u, 'nm']); ok = p.click(at, 300)
                R['headPops'][u] = {'ok': ok, 'pop': p.ev("__HU.popRead()")}
                p.ev("__HU.closePops()")
            # D-3 걸침 6.6.4 — 펼침 · 접힘
            p.board('민사소송법', '기출', 'unit')
            at = p.ev("([u,x])=>__HU.headAt(u,x)", [U664, 'ov']); R['ovOpenOk'] = p.click(at, 900)
            R['ovOpen'] = p.ev("__HU.unitRead()")
            R['ovUi'] = p.ev("()=>JSON.parse(localStorage.getItem('jopangi_ui')||'{}').c2uopen||null")
            at = p.ev("([u,x])=>__HU.headAt(u,x)", [U664, 'ov']); R['ovCloseOk'] = p.click(at, 900)
            R['ovClose'] = p.ev("__HU.unitRead()")
            # D-5 재매칭(마우스)
            p.board('민사소송법', '기출', 'unit')
            edit_flow(p, R, 'd5_')
            R['d5_after'] = p.ev("__HU.unitRead()")
            R['d5_hand'] = p.ev("k=>__HU.hand(k)", '민소|25-62-1')
            R['d5_win_closed'] = p.ev("__HU.win()")
            p.load('tok=1&keep=1'); p.board('민사소송법', '기출', 'unit')
            R['d5_reload'] = p.ev("__HU.unitRead()")
            R['d5_reload_hand'] = p.ev("k=>__HU.hand(k)", '민소|25-62-1')
            p.board('민사소송법', '기출', 'round')
            R['d5_round'] = p.ev("__HU.listRead()")
            # 같은 ✎ 두 번 = 닫힘(팝업 틀 규칙)
            p.board('민사소송법', '기출', 'unit')
            at = p.ev("([c,x])=>__HU.rowAt(c,x)", [CK251, 'edit']); p.click(at, 500)
            R['twice1'] = p.ev("()=>document.querySelectorAll('.pop.c2uw').length")
            at = p.ev("([c,x,o,n])=>__HU.rowAt(c,x,o,n)", [CK251, 'edit', False, True]); R['twiceAt'] = at; p.click(at, 500)   # 같은 자리(스크롤 없이) 두 번째
            R['twice2'] = p.ev("()=>document.querySelectorAll('.pop.c2uw').length")
            # C-8 기록 왕복 · SYNC_KEYS
            R['keys'] = p.ev("__HU.syncKeys()")
            R['rec'] = p.ev("__HU.recRoundtrip()")
            # 되돌리기 → 원자리 · 칸 = {auto:true}
            p.board('민사소송법', '기출', 'unit')
            at = p.ev("([c,x])=>__HU.rowAt(c,x)", [CK251, 'edit']); p.click(at, 600)
            R['rev_win'] = p.ev("__HU.win()")
            at = p.ev("([k])=>__HU.winAt(k)", ['rev']); R['revOk'] = p.click(at, 1200); p.ev("__HU.quiet()")
            R['rev_after'] = p.ev("__HU.unitRead()")
            R['rev_hand'] = p.ev("k=>__HU.hand(k)", '민소|25-62-1')
            # 고친 게 없으면 저장해도 손값을 안 만든다
            at = p.ev("([c,x])=>__HU.rowAt(c,x)", ['card|기출|민기출 26-63-1', 'edit']); p.click(at, 600)
            at = p.ev("([k])=>__HU.winAt(k)", ['save']); p.click(at, 800); p.ev("__HU.quiet()")
            R['nochange_hand'] = p.ev("k=>__HU.hand(k)", '민소|26-63-1')
            # D-6 손값이 ⚙ 자동값(바뀐 사본)을 이긴다
            p.board('민사소송법', '기출', 'unit')
            edit_flow(p, R, 'd6_')
            p.load('tok=1&keep=1&alt=1'); p.board('민사소송법', '기출', 'unit')
            R['d6_alt_hand'] = p.ev("__HU.unitRead()")
            R['d6_alt_loaded'] = p.ev("()=>((C2U['민소']||{}).문제||{})['25-62-1']")
            at = p.ev("([c,x])=>__HU.rowAt(c,x)", [CK251, 'edit']); p.click(at, 600)
            at = p.ev("([k])=>__HU.winAt(k)", ['rev']); p.click(at, 1200); p.ev("__HU.quiet()")
            R['d6_alt_auto'] = p.ev("__HU.unitRead()")
            p.load('tok=1&keep=1'); p.board('민사소송법', '기출', 'unit')
            # D-8 흐림 유지
            R['dim'] = {}
            for L0, K0 in [('특허법', '기출'), ('상표법', '기출'), ('디자인보호법', '기출'), ('민사소송법', 'GS')]:
                p.board(L0, K0, 'unit')
                R['dim'][L0 + '|' + K0] = {'seg': p.ev("__HU.seg()"), 'unit': p.ev("()=>document.querySelectorAll('#slot .c2uh').length"),
                                          'chips': p.ev("()=>document.querySelectorAll('#slot .c2r3 .c2uc,#slot .c2r3 .c2ue').length"),
                                          'list': p.ev("__HU.listRead()")}
        R['errs'] = p.ev("__HU.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


# ══════════ D-7 두 기기 동기화 (chromium) · 옛 판 기기 창 ══════════
def scen_sync(br, base, new):
    R = {}
    A = P(br, 'chromium', 'NEW', new, 1440, 900, who='꼬까')
    B = P(br, 'chromium', 'NEW', new, 1440, 900, who='햄찌')
    C = P(br, 'chromium', 'BASE', base, 1440, 900, who='옛판')
    try:
        for x in (A, B, C):
            x.ev("__HU.quiet()"); x.ev("f=>__HU.sync(f)", False); x.ev("__HU.quiet()")
        # ① A 손값 → 올림
        A.board('민사소송법', '기출', 'unit'); edit_flow(A, R, 'A_')
        A.ev("__HU.quiet()"); A.ev("__HU.stamp()")
        A.ev("([t,h])=>__HU.remoteSet(t,h)", [None, None])
        R['A1'] = A.ev("f=>__HU.sync(f)", True)
        P1 = A.ev("__HU.remoteGet()")['text']
        p1 = json.loads(P1)
        R['P1'] = {'has': 'jopangi.c2unit' in p1['data'], 'cell': (p1['data'].get('jopangi.c2unit') or {}).get('민소|25-62-1'), 'u': p1['u'].get('jopangi.c2unit|민소|25-62-1')}
        # ② B 받기 → 화면
        B.ev("([t,h])=>__HU.remoteSet(t,h)", [P1, 'S1'])
        R['B1'] = B.ev("f=>__HU.sync(f)", False); B.ev("__HU.quiet()")
        B.board('민사소송법', '기출', 'unit')
        R['Bunit'] = B.ev("__HU.unitRead()"); R['Bhand'] = B.ev("k=>__HU.hand(k)", '민소|25-62-1')
        A.board('민사소송법', '기출', 'unit'); R['Aunit'] = A.ev("__HU.unitRead()")
        # ③ B 되돌리기 → 올림
        at = B.ev("([c,x])=>__HU.rowAt(c,x)", [CK251, 'edit']); B.click(at, 600)
        at = B.ev("([k])=>__HU.winAt(k)", ['rev']); R['BrevOk'] = B.click(at, 1200); B.ev("__HU.quiet()"); B.ev("__HU.stamp()")
        R['B2'] = B.ev("f=>__HU.sync(f)", True)
        P2 = B.ev("__HU.remoteGet()")['text']
        p2 = json.loads(P2)
        R['P2'] = {'cell': (p2['data'].get('jopangi.c2unit') or {}).get('민소|25-62-1'), 'gone': [k for k in (p2.get('gone') or {}) if k.startswith('jopangi.c2unit|')]}
        # ④ A 받기 → 자동 자리 · 칸 = auto:true(되살아나지 않음)
        A.ev("([t,h])=>__HU.remoteSet(t,h)", [P2, 'S2'])
        R['A2'] = A.ev("f=>__HU.sync(f)", False); A.ev("__HU.quiet()")
        A.board('민사소송법', '기출', 'unit')
        R['Aunit2'] = A.ev("__HU.unitRead()"); R['Ahand2'] = A.ev("k=>__HU.hand(k)", '민소|25-62-1')
        # ⑤ 옛 판 기기 C(d3dd927) — A 가 다시 손값을 올린 원격(P3)을 받아 제 변경과 함께 올린다 → P4 · 새 판 A 가 다시 맞춘다 → P5
        A.board('민사소송법', '기출', 'unit'); edit_flow(A, R, 'A3_'); A.ev("__HU.quiet()"); A.ev("__HU.stamp()")
        R['A3'] = A.ev("f=>__HU.sync(f)", True)
        P3 = A.ev("__HU.remoteGet()")['text']
        C.ev("([t,h])=>__HU.remoteSet(t,h)", [P3, 'S3'])
        C.ev("()=>{try{lsWrite('jopangi.editq',[{k:'hz1',target:'note',st:'대기',t:Date.now()}],'수정 큐');}catch(e){}return 1}"); C.ev("__HU.quiet()"); C.ev("__HU.stamp()")
        R['C1'] = C.ev("f=>__HU.sync(f)", True)
        P4 = C.ev("__HU.remoteGet()")['text']
        p4 = json.loads(P4)
        R['P4'] = {'has': 'jopangi.c2unit' in p4['data'], 'u': p4['u'].get('jopangi.c2unit|민소|25-62-1'),
                   'gone': [k for k in (p4.get('gone') or {}) if k.startswith('jopangi.c2unit|')], 'keys': len(p4['data'])}
        A.ev("([t,h])=>__HU.remoteSet(t,h)", [P4, 'S4'])
        R['A4'] = A.ev("f=>__HU.sync(f)", False); A.ev("__HU.quiet()")
        P5 = A.ev("__HU.remoteGet()")
        p5 = json.loads(P5['text'])
        R['P5'] = {'puts': P5.get('puts'), 'cell': (p5['data'].get('jopangi.c2unit') or {}).get('민소|25-62-1')}
        R['Ahand4'] = A.ev("k=>__HU.hand(k)", '민소|25-62-1')
        R['errs'] = [A.ev("__HU.errs()") + A.errs, B.ev("__HU.errs()") + B.errs, C.ev("__HU.errs()") + C.errs]
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        for x in (A, B, C):
            x.close()
    return R


# ══════════ D-9 아이패드 진짜 터치 ══════════
def scen_pad(br, eng, src, W, H, shots):
    p = P(br, eng, 'NEW', src, W, H, pad=True)
    R = {'eng': eng, 'W': W}
    try:
        p.board('민사소송법', '기출', 'round')
        at = p.ev("o=>{const b=document.querySelector('#ordSeg [data-o=\"'+o+'\"]');if(!b)return null;const r=b.getBoundingClientRect();return {cx:r.left+r.width/2,cy:r.top+r.height/2,on:true}}", 'unit')
        R['segTap'] = p.click(at, 1000)
        R['ord'] = p.ev("()=>c2Ord()")
        R['fitUnit'] = p.ev("__HU.rowsFit()")
        edit_flow(p, R, 'T_', via_search='기판력')
        R['after'] = p.ev("__HU.unitRead()")
        R['hand'] = p.ev("k=>__HU.hand(k)", '민소|25-62-1')
        # 창 끌기
        at = p.ev("([c,x])=>__HU.rowAt(c,x)", [CK251, 'edit']); p.click(at, 700)
        w0 = p.ev("__HU.win()")
        hd = (w0 or {}).get('head') or {}
        if hd.get('on'):
            R['drag'] = p.drag(hd['cx'], hd['cy'], hd['cx'] - 90, hd['cy'] + 60); p.pg.wait_for_timeout(400)
        R['pos'] = [(w0 or {}).get('pos'), (p.ev("__HU.win()") or {}).get('pos')]
        R['winRect'] = (p.ev("__HU.win()") or {}).get('rect')
        if shots and W == 768:
            fn = os.path.join(WORK, 'shot_ipad768_win.png'); p.pg.screenshot(path=fn); R['shot'] = fn
        p.ev("__HU.closePops()")
        p.board('민사소송법', '기출', 'round')
        R['fitRound'] = p.ev("__HU.rowsFit()")
        R['errs'] = p.ev("__HU.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


# ══════════ D-10 폭(1024·768) 줄 넘침 · 캡처 ══════════
def scen_wide(br, eng, src, shots):
    R = {'eng': eng, 'w': {}}
    for W, H in [(1440, 900), (1024, 768), (768, 1024)]:
        p = P(br, eng, 'NEW', src, W, H)
        try:
            for mode in ('round', 'unit'):
                p.board('민사소송법', '기출', mode)
                R['w']['%d|%s' % (W, mode)] = {'fit': p.ev("__HU.rowsFit()")}
                if shots and W == 1440:
                    fn = os.path.join(WORK, 'shot_1440_%s.png' % mode); p.pg.screenshot(path=fn); R['w']['%d|%s' % (W, mode)]['shot'] = fn
                    if mode == 'unit':
                        at = p.ev("([u,x])=>__HU.headAt(u,x)", [U664, 'ov']); p.click(at, 900)
                        fn = os.path.join(WORK, 'shot_1440_unit_over.png'); p.pg.screenshot(path=fn); R['w']['1440|over'] = {'shot': fn}
                        at = p.ev("([u,x])=>__HU.headAt(u,x)", [U664, 'ov']); p.click(at, 900)
            if W == 1440 and shots:
                p.board('민사소송법', 'GS', 'round')
                fn = os.path.join(WORK, 'shot_1440_gs.png'); p.pg.screenshot(path=fn); R['w']['1440|gs'] = {'shot': fn}
            R['errs_%d' % W] = p.ev("__HU.errs()") + p.errs
        except Exception as e:
            R['exc_%d' % W] = repr(e)[:500]
        finally:
            p.close()
    return R


# ══════════ D-1 ⚙ ══════════
def scen_build():
    R = {}
    f = os.path.join(JOD, 'data', UNIT_FILE)
    b = open(f, 'rb').read()
    R['file'] = [len(b), hashlib.md5(b).hexdigest()]
    d = json.loads(b)
    R['n'] = len(d['문제'])
    R['keys'] = sorted(d.keys())
    num = lambda n: re.match(r'^(\d+(?:\.\d+)*)', n).group(1)
    R['dist'] = dict(Counter(num(v['주']) for v in d['문제'].values()))
    R['fields'] = sorted({k for v in d['문제'].values() for k in v} | {k for v in d['문제'].values() for s in v['설문'] for k in s}
                         | {k for v in d['문제'].values() for s in v['설문'] for u in s['단원'] for k in u})
    R['s'] = dict(Counter(u['s'] for v in d['문제'].values() for s in v['설문'] for u in s['단원']))
    # 두 번 돌려 바이트 같음 — 모듈을 따로 두 번(노트 = genie note_민소.json)
    sys.path.insert(0, J)
    import jo_common as JC
    CU = importlib.import_module('cha2_unit')
    outs = []
    for k in (1, 2):
        od = os.path.join(WORK, 'build%d' % k); shutil.rmtree(od, ignore_errors=True); os.makedirs(od)
        shutil.copy(os.path.join(JOD, 'data', 'note_민소.json'), od)

        def dump(name, obj, od=od):
            with open(os.path.join(od, name), 'w', encoding='utf-8') as fh:
                json.dump(obj, fh, ensure_ascii=False, separators=(',', ':'))
        G, W0 = JC.Checks(), []
        CU.build(J, od, dump, G, W0)
        outs.append((open(os.path.join(od, UNIT_FILE), 'rb').read(), [(r['코드'], r['판정'], r['실측']) for r in G.rows], W0))
    R['idem'] = outs[0][0] == outs[1][0]
    R['same_as_staged'] = outs[0][0] == b
    R['gates'] = outs[0][1]
    R['warn'] = outs[0][2]
    # D11 — 논점표 문자열이 산출 파일 글자 안에(노트 이름 칸 포함 전체) 있는가 · 노트 이름 밖
    T = json.load(open(os.path.join(J, '민소', '_민소2차_단원매핑', '_민소2차_논점표.json'), encoding='utf-8'))
    lines = sorted({(s.get('논점') or '').strip() for q in T for s in q.get('설문') or [] if (s.get('논점') or '').strip()})
    names = {v['주'] for v in d['문제'].values()} | {u['n'] for v in d['문제'].values() for s in v['설문'] for u in s['단원']}
    txt_all = b.decode('utf-8')
    R['nj_lines'] = len(lines)
    R['nj_in_file'] = [l for l in lines if l in txt_all]
    R['nj_only_in_names'] = all(any(l in n for n in names) for l in R['nj_in_file'])
    return R


def main():
    os.makedirs(WORK, exist_ok=True)
    new_raw = open(os.path.join(GENIE, REL), 'rb').read()
    new = new_raw.decode('utf-8')
    base_b = git('show', BASE_REV + ':' + REL)
    base = base_b.decode('utf-8')
    # D-6 사본 — 25-62-1 의 자동 주단원·설문을 바꾼다(1.4 이송 하나)
    d = json.load(open(os.path.join(JOD, 'data', UNIT_FILE), encoding='utf-8'))
    alt = copy.deepcopy(d)
    alt['문제']['25-62-1'] = {'주': '1.4. 이송(34①35조)법원소송행위', '설문': [{'no': '(1)', '단원': [{'n': '1.4. 이송(34①35조)법원소송행위', 's': '책'}]}]}
    json.dump(alt, io.open(os.path.join(WORK, '2cha_단원_민소.alt.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    RES = {'src': {'base': [len(base_b), hashlib.md5(base_b).hexdigest()],
                   'new': [len(new_raw), hashlib.md5(new_raw.replace(b'\r\n', b'\n')).hexdigest(), new_raw.count(b'\r\n'), new_raw.count(b'\n')]},
           'ground': ground()}
    t00 = time.time()
    if not ONLY or ONLY == 'build':
        RES['build'] = scen_build()
    with sync_playwright() as pw:
        brs = {e: getattr(pw, e).launch() for e in ('chromium', 'webkit')}
        try:
            for eng in ('chromium', 'webkit'):
                if not ONLY or ONLY == 'desk':
                    for tag, src in (('BASE', base), ('NEW', new)):
                        t0 = time.time(); print('… desk %s/%s' % (eng, tag), flush=True)
                        RES['desk/%s/%s' % (eng, tag)] = scen_desk(brs[eng], eng, tag, src)
                        print('   %.1fs %s' % (time.time() - t0, RES['desk/%s/%s' % (eng, tag)].get('exc', '')), flush=True)
                if not ONLY or ONLY == 'pad':
                    for W, H in [(768, 1024), (1024, 768)]:
                        t0 = time.time(); print('… pad %s %d' % (eng, W), flush=True)
                        RES['pad/%s/%d' % (eng, W)] = scen_pad(brs[eng], eng, new, W, H, shots=(eng == 'webkit'))
                        print('   %.1fs %s' % (time.time() - t0, RES['pad/%s/%d' % (eng, W)].get('exc', '')), flush=True)
                if not ONLY or ONLY == 'wide':
                    t0 = time.time(); print('… wide %s' % eng, flush=True)
                    RES['wide/%s' % eng] = scen_wide(brs[eng], eng, new, shots=(eng == 'chromium'))
                    print('   %.1fs' % (time.time() - t0), flush=True)
            if not ONLY or ONLY == 'sync':
                t0 = time.time(); print('… sync chromium', flush=True)
                RES['sync'] = scen_sync(brs['chromium'], base, new)
                print('   %.1fs %s' % (time.time() - t0, RES['sync'].get('exc', '')), flush=True)
        finally:
            for b in brs.values():
                b.close()
            for srv, _ in SERVERS.values():
                srv.shutdown()
    RES['sec'] = round(time.time() - t00, 1)
    json.dump(RES, io.open(os.path.join(WORK, 'raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    report(RES, base, new)


def NOISE(x):
    return 'ResizeObserver loop' in x or 'Failed to load resource' in x


def report(RES, base, new):
    L = []
    T = lambda n, c, i=None: L.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c or i is None else ' | ' + json.dumps(i, ensure_ascii=False)[:900]))
    I = lambda n, v: L.append('INFO | ' + n + ' | ' + (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)[:1600]))
    g = lambda d, *ks: __import__('functools').reduce(lambda a, k: (a[k] if isinstance(a, list) and isinstance(k, int) and -len(a) <= k < len(a)
                                                                    else (a or {}).get(k) if isinstance(a, dict) else None), ks, d)
    G = RES['ground']
    sb, sn = RES['src']['base'], RES['src']['new']
    T('착수 바탕 %s = 969,250 B(CRLF) 판 · md5(LF) d8f33f90…' % BASE_REV, sb[1] == BASE_MD5_LF, sb)
    T('NEW 작업트리 CRLF 그대로(LF 단독 0 · %d 줄) · %d B · md5(LF) %s' % (sn[2], sn[0], sn[1]), sn[2] == sn[3], sn)
    ch = sorted(l for l in git('status', '--porcelain').decode('utf-8').split('\n') if l.strip())
    T('genie 작업트리 바뀐 것 = jo/index.html + jo/data/%s 둘뿐 %s' % (UNIT_FILE, ch), ch == sorted([' M ' + REL, '?? jo/data/' + UNIT_FILE]) or ch == sorted([' M ' + REL, 'A  jo/data/' + UNIT_FILE])
       or (ch == [' M ' + REL] and git('ls-files', 'jo/data/' + UNIT_FILE).strip() != b''), ch)   # v4 부터 = 데이터는 54ced94 에 이미 올라 갔다
    nl, bl = new.replace('\r\n', '\n'), base.replace('\r\n', '\n')
    skn = re.findall(r"'([^']+)'", re.search(r'const SYNC_KEYS = \[(.+?)\]', nl, re.S).group(1))
    skb = re.findall(r"'([^']+)'", re.search(r'const SYNC_KEYS = \[(.+?)\]', bl, re.S).group(1))
    T('§C-5 SYNC_KEYS = 옛 30키 그대로 + 끝에 c2unit (31키)', skn == skb + ['c2unit'] and len(skn) == 31, [len(skb), skn[-3:]])
    T('§B-1 C2_UNIT_READY 상수 → c2UnitReady() 함수(상수 0)', 'C2_UNIT_READY' not in nl and 'function c2UnitReady()' in nl)
    # ── D-1 ⚙
    B0 = RES.get('build') or {}
    if B0:
        T('D-1 ⚙ — 생성 JSON 76문제 · 칸 = 법·갈래·문제 · 문제 칸 = 주·설문 · 설문 칸 = no·단원 · 단원 칸 = n·s(책 글자 칸 없음)',
          B0['n'] == 76 and B0['keys'] == ['갈래', '문제', '법'] and B0['fields'] == sorted({'주', '설문', 'no', '단원', 'n', 's'}), [B0['n'], B0['keys'], B0['fields']])
        T('D-1 주단원 분포 = §0 표 그대로(40 단원 · 합 76)', B0['dist'] == TABLE0, sorted(set(B0['dist'].items()) ^ set(TABLE0.items())))
        T('D-1 두 번 돌려 바이트 같음 · genie 에 옮긴 파일과 같음 %s' % B0['file'], B0['idem'] and B0['same_as_staged'], [B0['idem'], B0['same_as_staged']])
        T('D-1 A-2 D11 — 논점표 %d줄 중 파일에 든 것은 볼트 노트 이름 속 낱말뿐(노트 이름 밖 0 · U1 %s)' % (B0['nj_lines'], [x[1] for x in B0['gates'] if x[0] == 'U1']),
          B0['nj_only_in_names'] and [x for x in B0['gates'] if x[0] == 'U1' and x[1] == 'OK'], [B0['nj_in_file'], B0['gates']])
        I('D-1 파일에 든 논점표 낱말(모두 볼트 노트 이름 속 — note_민소.json 에 이미 공개)', B0['nj_in_file'])
        I('D-1 출처 분포 · ⚙ 경고', {'s': B0['s'], 'warn': B0['warn']})
    for eng in ('chromium', 'webkit'):
        Bd, N = RES.get('desk/%s/BASE' % eng), RES.get('desk/%s/NEW' % eng)
        if not Bd or not N:
            continue
        E = '[%s] ' % eng
        if Bd.get('exc') or N.get('exc'):
            T(E + '책상 시나리오 예외 0', False, [Bd.get('exc'), N.get('exc')])
        # D-10 줄 꼴 · 회차 머리
        lst = N.get('list') or {}
        rows = lst.get('rows', [])
        T(E + 'D-10 회차별 76줄 — .c2k·.c2rn 0 · 첫 줄 첫 자식 = 제목(.c2t2) · 줄 수 = 바탕 격자 셀',
          len(rows) == 76 and all(r['k'] == 0 and r['rn'] == 0 and r['first'] == 'c2t2' for r in rows) and len(rows) == len(Bd.get('cells') or []),
          [len(rows), len(Bd.get('cells') or []), [r for r in rows if r['k'] or r['rn'] or r['first'] != 'c2t2'][:2]])
        heads = lst.get('heads', [])
        T(E + 'D-10 회차 머리 수 = 회차 수(19) · 머리마다 문제 수 합 76 · 머리 글자 「N회 · YYYY년 · n문제」',
          len(heads) == 19 and sum(h['cnt'] for h in heads) == 76 and all(h['n'] == '%d문제' % h['cnt'] for h in heads)
          and all(re.match(r'^\d+회$', h['r']) and re.match(r'^· \d{4}년$', h['y']) for h in heads),
          [len(heads), sum(h['cnt'] for h in heads), heads[:2]])
        T(E + 'D-10 회차 머리 꼴 — 17px ui-monospace 굵게 · 밑줄 2px · 위 여백 20px · 회차마다 줄 바탕 번갈아',
          heads and all(h['fs'] == '17px' and 'monospace' in (h['ff'] or '') and h['bb'] == '2px' and h['mt'] == '20px' for h in heads)
          and all((r['alt'] == (i % 2 == 1)) for i, h in enumerate(heads) for r in rows if r['round'] == h['round']), heads[:1])
        # D-4 셋째 칸 — 주단원 칩 · ✎ · 칩 누름 = 노트 팝업(카드 팝업 아님) · 줄 누름 = 카드 팝업 글자 = 바탕
        T(E + 'D-4 회차별 76줄 전부 주단원 칩 하나 + ✎ 단원', all(len(r['chips']) == 1 and r['edit'] for r in rows), [r['code'] for r in rows if len(r['chips']) != 1 or not r['edit']][:4])
        cp = N.get('chipPop') or {}
        T(E + 'D-4 주단원 칩 누름 → 노트 팝업 1개(「📄 <노트>」) · 카드 팝업 안 열림', cp.get('ok') and g(cp, 'pop', 'n') == 1
          and all(t.startswith('📄 ') for t in g(cp, 'pop', 'titles') or []) and g(cp, 'pop', 'sel') is None, cp)
        for ck in POPS3:
            pn, pb = g(N, 'pops', ck) or {}, g(Bd, 'pops', ck) or {}
            T(E + 'D-4 줄 클릭 → 카드 팝업 · 글자 = 바탕 .ctitle 클릭 팝업 그대로 — %s' % ck[:30],
              pn.get('ok') and pb.get('ok') and g(pn, 'pop', 'n') == 1 and g(pn, 'pop', 'text') == g(pb, 'pop', 'text') and g(pn, 'pop', 'sel') == ck,
              [pn.get('ok'), pb.get('ok'), (g(pn, 'pop', 'text') or '')[:80], (g(pb, 'pop', 'text') or '')[:80]])
        # D-2 단원별
        U0 = N.get('unit') or {}
        heads_u = [h for h in U0.get('heads', []) if not h['none']]
        cnt = {re.match(r'^(\d+(?:\.\d+)*)', h['unit']).group(1): int(h['n'].replace('문제 ', '')) for h in heads_u}
        T(E + 'D-2 단원 머리 수 = 주단원 쓰인 단원 수(40) · 머리마다 「문제 N」 = §0 표 · 줄 합 76 · 머리 아래 줄 수 = 문제 N',
          len(heads_u) == 40 and cnt == TABLE0 and len(U0.get('rows', [])) == 76 and all(h['rows'] == int(h['n'].replace('문제 ', '')) for h in heads_u),
          [len(heads_u), sorted(set(cnt.items()) ^ set(TABLE0.items()))[:4], len(U0.get('rows', []))])
        cks = [r['ck'] for r in U0.get('rows', [])]
        T(E + 'D-2 각 카드 한 번씩만(중복 0 · 바탕 카드 집합과 같음) · 단원 없음 0', len(cks) == len(set(cks)) == 76 and sorted(cks) == sorted(Bd.get('cells') or []) and U0.get('none') == 0,
          [len(cks), len(set(cks)), U0.get('none')])
        pys = sorted({h['unit'].split('.')[0] for h in heads_u})
        T(E + 'D-2 편 띠 = 문제 있는 편만(%s) · 분홍 띠 꼴(#FBDCE8 · #8A3B62)' % ','.join(pys),
          sorted(b['no'] for b in U0.get('bands', [])) == pys and all(b['bg'] == 'rgb(251, 220, 232)' and b['color'] == 'rgb(138, 59, 98)' for b in U0.get('bands', [])),
          U0.get('bands'))
        T(E + 'D-2 단원 머리 번호 = 파랑 ui-monospace · 차례 = 번호 마디 차례',
          heads_u and all('monospace' in (h['noFont'] or '') and h['noColor'] == 'rgb(47, 111, 208)' for h in heads_u)
          and [h['unit'] for h in heads_u] == sorted([h['unit'] for h in heads_u], key=lambda u: [int(x) for x in re.match(r'^(\d+(?:\.\d+)*)', u).group(1).split('.')]),
          [h['unit'] for h in heads_u][:6])
        for u in HEADS3:
            hp = g(N, 'headPops', u) or {}
            T(E + 'D-2 머리 클릭 → 그 노트 팝업 — %s' % u[:20], hp.get('ok') and g(hp, 'pop', 'n') == 1 and (g(hp, 'pop', 'titles') or [''])[0] == '📄 ' + u
              and '목차 노트에 없다' not in (g(hp, 'pop', 'text') or ''), [hp.get('ok'), g(hp, 'pop', 'titles')])
        # D-3 걸침
        want = G['over'].get(U664)
        h664 = [h for h in (U0.get('heads') or []) if h['unit'] == U664]
        op = [h for h in (g(N, 'ovOpen', 'heads') or []) if h['unit'] == U664]
        cl = [h for h in (g(N, 'ovClose', 'heads') or []) if h['unit'] == U664]
        overs = [r for r in (g(N, 'ovOpen', 'over') or []) if r['head'] == U664]
        T(E + 'D-3 6.6.4 「걸침 N」 = 재료로 센 값(%s) · 펼침 → 흐린 줄 N(opacity .55 · 「걸침 — 주단원 …」) · 접힘 → 0 · c2uopen 기억' % want,
          h664 and h664[0]['ov'] == '걸침 %s ▸' % want and op and op[0]['ov'] == '걸침 %s ▾' % want and len(overs) == want
          and all(r['op'] == '0.55' and r['ovt'].startswith('걸침 — 주단원 ') and r['ck'] is None for r in overs)
          and cl and cl[0]['over'] == 0 and N.get('ovUi') == {'민소|' + U664: 1},
          [h664[:1], op[:1], len(overs), cl[:1], N.get('ovUi')])
        # D-5 재매칭
        a5 = N.get('d5_after') or {}
        where = {r['ck']: r['head'] for r in a5.get('rows', [])}
        c5 = {h['unit']: h['n'] for h in a5.get('heads', [])}
        hv = N.get('d5_hand') or {}
        T(E + 'D-5 ✎ 25-62-1 → 설문 (2) 에 2.3 더하기 · 주단원 7.8.2 · 저장 → 7.8.2 머리 아래 · 4.1.1 「문제 2」(−1) · 창 닫힘',
          N.get('d5_editOk') and N.get('d5_itemOk') and N.get('d5_radOk') and N.get('d5_saveOk') and where.get(CK251) == U782 and c5.get(U411) == '문제 2'
          and c5.get(U782) == '문제 1' and N.get('d5_win_closed') is None,
          [N.get('d5_editOk'), N.get('d5_itemOk'), N.get('d5_radOk'), N.get('d5_saveOk'), where.get(CK251), c5.get(U411), c5.get(U782)])
        T(E + 'D-5 jopangi.c2unit[\'민소|25-62-1\'] = {main 7.8.2 · s 설문 셋(2 에 2.3 더함) · t · by 꼬까}',
          hv.get('main') == U782 and list((hv.get('s') or {}).keys()) == ['(1)', '(2)', '(3)'] and U23 in (hv.get('s') or {}).get('(2)', [])
          and isinstance(hv.get('t'), (int, float)) and str(hv.get('by') or '').startswith('꼬까'), hv)
        T(E + 'D-5 새로고침 뒤 그대로(자리·값)', {r['ck']: r['head'] for r in g(N, 'd5_reload', 'rows') or []}.get(CK251) == U782 and N.get('d5_reload_hand') == hv,
          [N.get('d5_reload_hand')])
        rr = [r for r in g(N, 'd5_round', 'rows') or [] if r['ck'] == CK251]
        T(E + 'D-5 회차별 줄 칩 = 손값 주단원 + ✓손', rr and rr[0]['chips'] == [U782] and rr[0]['hand'], rr[:1])
        T(E + '같은 ✎ 두 번 = 창 닫힘(팝업 틀 규칙)', N.get('twice1') == 1 and N.get('twice2') == 0, [N.get('twice1'), N.get('twice2')])
        ra = N.get('rev_after') or {}
        T(E + 'D-5 되돌리기 → 원자리(4.1.1) · 칸 값 = {auto:true, t}(칸 남음)', {r['ck']: r['head'] for r in ra.get('rows', [])}.get(CK251) == U411
          and (N.get('rev_hand') or {}).get('auto') is True and set((N.get('rev_hand') or {}).keys()) == {'auto', 't'}, [N.get('rev_hand')])
        T(E + '§C-4 고친 게 없으면 저장해도 손값을 안 만든다(26-63-1)', N.get('nochange_hand') is None, N.get('nochange_hand'))
        # D-6
        w6 = {r['ck']: r['head'] for r in g(N, 'd6_alt_hand', 'rows') or []}
        w7 = {r['ck']: r['head'] for r in g(N, 'd6_alt_auto', 'rows') or []}
        T(E + 'D-6 손값 이김 — 자동값을 바꾼 사본(25-62-1 → 1.4)을 먹여도 화면 = 손값(7.8.2) · 되돌리면 사본 자동값(1.4)',
          (N.get('d6_alt_loaded') or {}).get('주', '').startswith('1.4.') and w6.get(CK251) == U782 and (w7.get(CK251) or '').startswith('1.4.'),
          [N.get('d6_alt_loaded'), w6.get(CK251), w7.get(CK251)])
        # D-8
        for k, v in (N.get('dim') or {}).items():
            sg = v.get('seg') or [{}, {}]
            why = 'GS 단원 데이터 없음' if k.endswith('GS') else ('%s 기출 단원 데이터 없음' % {'특허법': '특허', '상표법': '상표', '디자인보호법': '디보', '민사소송법': '민소'}[k.split('|')[0]])
            T(E + 'D-8 %s — 「단원별」 disabled · 툴팁 「%s」 · 회차별 켜짐 · 단원 칩·✎ 0' % (k, why),
              sg[1].get('dis') and sg[1].get('title') == why and sg[0].get('on') and v.get('unit') == 0 and v.get('chips') == 0, sg)
            lr = v.get('list') or {}
            T(E + 'D-10 %s — 줄 꼴(.c2k·.c2rn 0 · 첫 자식 = 제목) · 회차 머리 합 = 줄 수' % k,
              lr.get('rows') and all(r['k'] == 0 and r['rn'] == 0 and r['first'] == 'c2t2' for r in lr['rows']) and sum(h['cnt'] for h in lr.get('heads', [])) == len(lr['rows']),
              [len(lr.get('rows') or []), sum(h['cnt'] for h in lr.get('heads', []))])
        # C-8
        ky, rc = N.get('keys') or {}, N.get('rec') or {}
        T(E + 'C-5 SYNC_KEYS 31 · 끝 = jopangi.c2unit', ky.get('n') == 31 and ky.get('last') == 'jopangi.c2unit', ky)
        T(E + 'C-8 ⤓ 기록 — 내보내기에 c2unit 층 · 지웠다 들여오면 되살아남 · 건수에 듦 · 이름표 「🧩 2차 단원 …」',
          rc.get('inDump') and rc.get('mid') is None and rc.get('after') == rc.get('before') and rc.get('before') and rc.get('stat') and rc['stat'][0] >= 1
          and (rc.get('label') or '').startswith('🧩 2차 단원'), rc)
        en = [x for x in (N.get('errs') or []) if not NOISE(x)]
        T(E + 'JS 오류 0(NEW · ResizeObserver loop·자원 404 줄은 뺌)', not en, en[:4])
    # D-7
    S7 = RES.get('sync') or {}
    if S7:
        if S7.get('exc'):
            T('D-7 예외 0', False, S7.get('exc'))
        wB = {r['ck']: r['head'] for r in g(S7, 'Bunit', 'rows') or []}
        wA = {r['ck']: r['head'] for r in g(S7, 'Aunit', 'rows') or []}
        T('D-7 ① A 손값 → 올림(원격 data 에 c2unit 칸 · u 도장) → ② B 받기 → B 화면 = A 화면(25-62-1 → 7.8.2)',
          g(S7, 'P1', 'has') and g(S7, 'P1', 'cell', 'main') == U782 and g(S7, 'P1', 'u') and wB.get(CK251) == U782 and wA.get(CK251) == U782
          and str((S7.get('Bhand') or {}).get('by') or '').startswith('꼬까'), [S7.get('P1'), wB.get(CK251), S7.get('Bhand')])
        wA2 = {r['ck']: r['head'] for r in g(S7, 'Aunit2', 'rows') or []}
        T('D-7 ③ B 되돌리기 → 올림(칸 = auto:true · 묘비 0) → ④ A 받기 → 자동 자리(4.1.1) · A 칸 = auto:true(되살아나지 않음)',
          S7.get('BrevOk') and (g(S7, 'P2', 'cell') or {}).get('auto') is True and not g(S7, 'P2', 'gone') and wA2.get(CK251) == U411
          and (S7.get('Ahand2') or {}).get('auto') is True, [S7.get('P2'), wA2.get(CK251), S7.get('Ahand2')])
        I('D-7 ⑤ 옛 판 기기(d3dd927)가 손값 든 원격을 받아 올린 기록', S7.get('P4'))
        T('D-7 ⑤ 옛 판 기기는 c2unit 을 지우지 않는다 — 묘비 0 · u 도장은 남는다(합집합)', not g(S7, 'P4', 'gone') and g(S7, 'P4', 'u'), S7.get('P4'))
        T('D-7 ⑤ 새 판 기기 A 가 다음 맞추기에서 되살려 올린다(원격 칸 = 손값 7.8.2)', g(S7, 'P5', 'cell', 'main') == U782 and (S7.get('Ahand4') or {}).get('main') == U782,
          [S7.get('P5'), S7.get('Ahand4')])
        I('D-7 ⑤ 옛 판 기기가 올릴 때 data 에서 c2unit 이 빠지나(민법 G16 · 조판기 J19 와 같은 창)', {'옛 판이 올린 data 에 c2unit': g(S7, 'P4', 'has')})
        ee = [x for es in (S7.get('errs') or []) for x in es if not NOISE(x)]
        T('D-7 JS 오류 0(세 기기)', not ee, ee[:4])
    # D-9
    for eng in ('chromium', 'webkit'):
        for W in (768, 1024):
            D = RES.get('pad/%s/%d' % (eng, W))
            if not D:
                continue
            E = '[%s 아이패드 %d] ' % (eng, W)
            if D.get('exc'):
                T(E + '예외 0', False, D.get('exc'))
            T(E + 'D-9 「단원별」 톡 → 단원별', D.get('segTap') and D.get('ord') == 'unit', [D.get('segTap'), D.get('ord')])
            srch = D.get('T_searched') or []
            T(E + 'D-9 ✎ 톡 → 창 · ＋ 단원 → 찾기 칸 「기판력」 → 목록이 그 글자만 · 고르기 → 저장 → 손값',
              D.get('T_editOk') and D.get('T_win0') and srch and all('기판력' in x['n'] for x in srch) and D.get('T_itemOk') and D.get('T_saveOk')
              and (D.get('hand') or {}).get('main') == U782 and D.get('T_pickTarget') in ((D.get('hand') or {}).get('s') or {}).get('(2)', []),
              [D.get('T_editOk'), len(srch), D.get('T_pickTarget'), D.get('hand')])
            ps = D.get('pos') or [None, None]
            mv = ps[0] and ps[1] and abs((ps[1]['l'] - ps[0]['l']) + 90) < 6 and abs((ps[1]['t'] - ps[0]['t']) - 60) < 6
            T(E + 'D-9 창 끌기(-90, +60) · %s' % D.get('drag'), bool(mv), ps)
            wr_ = D.get('winRect') or {}
            T(E + 'D-9 창이 화면 안(mbWinFit)', wr_ and wr_['x'] >= 0 and wr_['r'] <= W + 0.5, wr_)
            for k2 in ('fitUnit', 'fitRound'):
                f = D.get(k2) or {}
                T(E + 'D-9 %s 줄 안 요소(점수 칩 · 단원 칩 · ✎)가 줄 테두리 안(줄 폭 %s)' % ({'fitUnit': '단원별', 'fitRound': '회차별'}[k2], f.get('w')), f.get('n') and f.get('nbad') == 0, f)
            en = [x for x in (D.get('errs') or []) if not NOISE(x)]
            T(E + 'JS 오류 0', not en, en[:4])
    # D-10 폭
    for eng in ('chromium', 'webkit'):
        W0 = RES.get('wide/%s' % eng) or {}
        if not W0:
            continue
        bad = {k: v['fit'] for k, v in (W0.get('w') or {}).items() if v.get('fit') and (not v['fit']['n'] or v['fit']['nbad'])}
        T('[%s] D-10 1440·1024·768 × 회차별·단원별 — 제목·칩이 줄 밖으로 안 나감' % eng, not bad and len([k for k, v in (W0.get('w') or {}).items() if v.get('fit')]) == 6, bad)
        I('[%s] 줄 폭' % eng, {k: v['fit'].get('w') for k, v in (W0.get('w') or {}).items() if v.get('fit')})
        ew = [x for k2 in ('errs_1440', 'errs_1024', 'errs_768') for x in (W0.get(k2) or []) if not NOISE(x)]
        T('[%s] 폭 JS 오류 0' % eng, not ew, ew[:4])
    p = sum(1 for x in L if x.startswith('PASS')); f = sum(1 for x in L if x.startswith('FAIL'))
    body = '\n'.join(L) + '\n\n합계  PASS %d · FAIL %d  (%.0f초)\n' % (p, f, RES.get('sec', 0))
    print(body)
    wr(os.path.join(OUT, '_harness_jo_2cha_unit_result.txt'), body)
    shots = []
    W0 = RES.get('wide/chromium') or {}
    for k, v in (W0.get('w') or {}).items():
        if v.get('shot'):
            shots.append((v['shot'], os.path.basename(v['shot'])[5:]))
    for eng in ('webkit',):
        D = RES.get('pad/%s/768' % eng) or {}
        if D.get('shot'):
            shots.append((D['shot'], os.path.basename(D['shot'])[5:]))
    for src_, name in shots:
        wr(os.path.join(SHOTS, name), open(src_, 'rb').read())


if __name__ == '__main__':
    main()
