# -*- coding: utf-8 -*-
"""조판기 머리 가로 탭 · 1차객 틈 0 · 2차 보드 목록 — _task_jo_hrail_list §D 관문 하네스.

  NEW  = genie 작업트리 jo/index.html (고친 판 · CRLF)
  BASE = `dde3300` 의 같은 파일(959,738 B CRLF · md5(LF) d2fc1e5d…) — 기준(census·셀 수·팝업 글자·padding)이자 헛잣대
  데이터 = genie jo/data(실물) · 網 = 같은 출처만(GitHub 기록.json 은 SEED 가 메모리로 대답 · 나머지 밖 주소 404)
  엔진 = playwright chromium · webkit
     책상 1440×900(마우스 · DSF 1) · 세 폭 768·1024·1440(가로 스크롤 · 캡처) · 아이패드 768×1024 세로 · 1024×768 가로(진짜 터치 · DSF 2)
     끌기 = chromium CDP 터치(끝에서 멈춤) / webkit 신뢰 마우스(playwright webkit 은 톡만 진짜 터치 — 도구 한계)
  픽셀 = 사례 격자 무변 하나만(chromium · 본문 폭·높이를 맞춘 두 창 · 레일 40px·머리 높이 차를 창 크기로 갚는다)

쓰기 : python _harness_jo_hrail_list.py [--out 폴더] [--only desk|wide|pix|pad]
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import hashlib, http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

GENIE = _roots.genie()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else HERE
ONLY = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else ''
SHOTS = os.path.join(OUT, '_hrail_shots')
WORK = os.path.join(tempfile.gettempdir(), 'h_jo_hrail')
REL = 'jo/index.html'
JOD = os.path.join(GENIE, 'jo')
BASE_REV = 'dde3300'
BASE_MD5_LF = 'd2fc1e5d9ce80b62fa78ae30cd50e3c7'
TESTS = io.open(os.path.join(HERE, '_harness_jo_hrail_list_tests.js'), encoding='utf-8').read()
IPAD_UA = ('Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 '
           '(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
LAWS = ['특허법', '상표법', '디자인보호법', '민사소송법']
TABS = ['jo', 'prec', 'jimun', 'cha2', 'omr']
BOARDS = [('특허법', '기출'), ('상표법', '기출'), ('민사소송법', '기출'), ('민사소송법', 'GS'), ('디자인보호법', '기출'), ('상표법', 'GS')]
SAK = [('특허법', '사례'), ('민사소송법', '사례')]
POPS = [('특허법', '기출', 'card|기출|특기출 26-63-1-침해금지(진보성 항변·자백)·손해배상(128조 종합)'),
        ('특허법', '기출', 'card|기출|특기출 03-40-1-미행무,선사용권 지득예외,중용권'),
        ('상표법', '기출', 'card|기출|상기출 18-55-3-판-Discovery'),
        ('민사소송법', 'GS', 'card|GS|곽민실전B-26-1회-1-비법당능,지적의무-대위소{불}-화권결준재심3호상대방주장-'),
        ('디자인보호법', '기출', 'card|기출|디기출 18-55-1'),
        ('민사소송법', '기출', 'card|기출|민기출 26-63-2')]
SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.alert=function(){};window.confirm=function(){return true;};window.prompt=function(){return null;};
(function(){var Q=new URLSearchParams(location.search);var nf=window.fetch.bind(window);
window.fetch=function(u,o){o=o||{};var s=String((u&&u.url)||u);
 if(/\/contents\/jopangi\/(%EA%B8%B0%EB%A1%9D|기록)\.json/.test(s)){var R=window.__REMOTE;
  if((o.method||'GET')==='PUT'){var b=JSON.parse(o.body||'{}');if(!R)R=window.__REMOTE={text:null,sha:null,puts:0};
   if(R.sha&&b.sha!==R.sha)return Promise.resolve(new Response('{"message":"conflict"}',{status:409}));
   R.text=decodeURIComponent(escape(atob(b.content)));R.puts=(R.puts||0)+1;R.sha='H'+R.puts;
   return Promise.resolve(new Response(JSON.stringify({content:{sha:R.sha}}),{status:200,headers:{'Content-Type':'application/json'}}));}
  if(!R||R.text==null)return Promise.resolve(new Response('{"message":"Not Found"}',{status:404}));
  var acc=((o.headers||{}).Accept||'');
  if(acc.indexOf('raw')>=0)return Promise.resolve(new Response(R.text,{status:200}));
  return Promise.resolve(new Response(JSON.stringify({sha:R.sha}),{status:200,headers:{'Content-Type':'application/json'}}));}
 if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));
 return nf(u,o);};
try{localStorage.clear();}catch(e){}
if(Q.get('tok')!=='0'){try{localStorage.setItem('tt.cfg',JSON.stringify({token:'harness-token',person:'꼬까'}));}catch(e){}}
})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
</script>"""
READY = "!!window.__HR&&typeof render==='function'&&typeof popCard4==='function'"


def git(*a, repo=GENIE):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def J(s):
    try:
        return json.loads(s) if isinstance(s, str) else s
    except Exception:
        return {'__raw': str(s)[:300]}


def wr(path, data):
    """N: 는 잇달아 쓰면 이웃 파일 내용이 섞인다 — 한 파일 쓰고 0.5초 뒤 되읽어 대조(memory: mybox-adjacent-file-write)."""
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
    """한 쪽(page) — 엔진·판·창 종류"""
    def __init__(self, br, eng, tag, src, W, H, pad=False, q='tok=1'):
        self.eng, self.tag, self.pad = eng, tag, pad
        port = serve(tag, src)
        if pad:
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=IPAD_UA)
        else:
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1)
        self.ctx.route('**/*', route_filter)
        self.pg = self.ctx.new_page()
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' else None)
        self.pg.goto('http://127.0.0.1:%d/index.html?%s' % (port, q), wait_until='load', timeout=120000)
        self.pg.wait_for_function(READY, timeout=120000)
        self.cdp = self.ctx.new_cdp_session(self.pg) if (eng == 'chromium' and pad) else None
        self.ev("([l,t])=>__HR.go(l,t)", ['특허법', 'jo'])
        self.pg.wait_for_timeout(1500)   # recBoot 첫 동기화가 배지 글자를 한 번 바꾼다

    def ev(self, expr, arg=None):
        # 날값 그대로 — 페이지 도구는 객체·문자열을 바로 돌려준다(J() 로 풀면 평문 'round' 가 {'__raw':…} 가 된다)
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def click(self, at, wait=700):
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

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


def pop_by(p, law, kind, ck, part='title'):
    p.ev("([l,k])=>__HR.board(l,k)", [law, kind])
    at = p.ev("([c,x])=>__HR.clickAt(c,x)", [ck, part])
    clicked = p.click(at, 300)
    if not clicked and p.tag == 'BASE' and part == 'title':
        # 바탕 격자는 보이는 칸만 본문을 그려 칸 높이가 뒤늦게 바뀐다 — 다시 재서 한 번 더
        p.pg.wait_for_timeout(700)
        at = p.ev("([c,x])=>__HR.clickAt(c,x)", [ck, part])
        clicked = p.click(at, 300)
    r = p.ev("__HR.popRead()")
    p.ev("__HR.closePops()")
    return {'at': at, 'clicked': clicked, 'pop': r}


# ══════════ A·B·C — 책상 1440×900 (마우스) ══════════
def scen_desk(br, eng, tag, src):
    p = P(br, eng, tag, src, 1440, 900)
    R = {'eng': eng, 'tag': tag}
    try:
        R['census'] = {}
        for L in LAWS:
            for T in TABS:
                ok = p.ev("([l,t])=>__HR.go(l,t)", [L, T])
                R['census'][L + '|' + T] = {'ok': ok, 'c': p.ev("__HR.census()"), 'st': p.ev("__HR.state()")}
        p.ev("([l,t])=>__HR.go(l,t)", ['특허법', 'jo'])
        R['hdr'] = p.ev("__HR.hdr()")
        R['need'] = p.ev("__HR.need()")
        R['ctrlK'] = p.ev("__HR.ctrlK()")
        if tag == 'NEW':
            R['tabclick'] = []
            for k in ['prec', 'jimun', 'cha2', 'omr', 'jo']:
                at = p.ev("k=>__HR.tabAt(k)", k)
                ok = p.click(at, 900)
                R['tabclick'].append({'k': k, 'at': at, 'ok': ok, 'st': p.ev("__HR.state()")})
            at = p.ev("__HR.ksAt()")
            p.click(at, 250)
            R['ksClick'] = {'at': at, 'open': p.ev("__HR.skOpen()")}
            p.ev("__HR.closePops()")
        R['jim'] = {s: p.ev("s=>__HR.jim(s)", s) for s in ['home', 'solve', 'gichul']}
        R['pads'] = p.ev("__HR.pads()")
        R['boards'] = {}
        for L, K in BOARDS + SAK:
            R['boards'][L + '|' + K] = p.ev("([l,k])=>__HR.board(l,k)", [L, K])
        R['year'] = {}
        for L, K, y in [('특허법', '기출', 2014), ('민사소송법', '기출', 2020), ('상표법', '기출', 2012), ('디자인보호법', '기출', 2019)]:
            p.ev("([l,k])=>__HR.board(l,k)", [L, K])
            r = p.ev("y=>__HR.setYear(y)", y)
            R['year']['%s|%s|%d' % (L, K, y)] = {'n': (r or {}).get('n'), 'cks': [x['ck'] for x in (r or {}).get('rows', [])]}
        R['pops'] = {}
        for L, K, ck in POPS:
            R['pops'][ck] = {'title': pop_by(p, L, K, ck, 'title')}
            if tag == 'NEW':
                R['pops'][ck]['code'] = pop_by(p, L, K, ck, 'code')
                # A-6(a) 줄 클릭 글자는 같은 카드를 popCard4 로 바로 연 새 판 글자와 맞댄다(바탕 dde3300 팝업 글자는 뒤 판 pop_moknote·c2card·ms_claude_editq 가 바꿈)
                p.ev("__HR.closePops()")
                p.ev("([k,f])=>{popCard4(k,f,null,1);return 1}", [K, ck.split('|', 2)[2]])
                R['pops'][ck]['direct'] = {'pop': p.ev("__HR.popRead()")}
                p.ev("__HR.closePops()")
        # 점수 칩(채점 4건 × 특허·민소) — 누르면 채점 탭 팝업(옛 칸 머리 칩과 같은 길)
        R['scorepop'] = {}
        for L, ck in [('특허법', 'card|기출|특기출 26-63-4-공지예외(30조)·소권범(자유실시기술)'), ('민사소송법', 'card|기출|민기출 26-63-1')]:
            R['scorepop'][ck] = pop_by(p, L, '기출', ck, 'score')
            if tag == 'NEW':   # A-6(a) 채점 탭 글자 = 같은 카드를 popCard4(…, '채점')(점수 칩 onclick 과 같은 부름)로 바로 연 새 판 글자
                p.ev("__HR.closePops()")
                p.ev("f=>{popCard4('기출',f,null,1,null,'채점');return 1}", ck.split('|', 2)[2])
                R['scorepop'][ck]['direct'] = p.ev("__HR.popRead()")
                p.ev("__HR.closePops()")
        if tag == 'NEW':
            # 연도·회차 단추 = 목록 내림 ↔ 오름
            p.ev("([l,k])=>__HR.board(l,k)", ['특허법', '기출'])
            s0 = p.ev("__HR.boardRead()")
            at = p.ev("__HR.ysortAt()"); p.click(at, 900)
            s1 = p.ev("__HR.boardRead()")
            at2 = p.ev("__HR.ysortAt()"); p.click(at2, 900)
            s2 = p.ev("__HR.boardRead()")
            R['ysort'] = {'s0': [x['code'] for x in s0['rows']], 'b0': s0['ysort'], 's1': [x['code'] for x in s1['rows']], 'b1': s1['ysort'],
                          's2': [x['code'] for x in s2['rows']], 'b2': s2['ysort'], 'at': at}
            # 2단 행 클릭 → 그 줄이 보드 가운데
            rows = s2['rows']; mid = rows[len(rows) // 2]['ck']; low = rows[-6]['ck']
            R['prow'] = {}
            for ck in (mid, low):
                at = p.ev("c=>__HR.prowAt(c)", ck)
                p.click(at, 1300)
                R['prow'][ck] = {'at': at, 'c': p.ev("c=>__HR.centered(c)", ck)}
            # 보드 스크롤 → 2단 선택이 따라온다
            tgt = rows[len(rows) // 3]['ck']
            R['follow'] = {'ck': tgt, 'r': p.ev("c=>__HR.scrollTo(c)", tgt)}
        # 선택·결론반대 줄 꼴 — 민소 기출에 결론반대·누락 논점 1건(민기출 16-53-3) · 그 줄을 눌러 선택
        p.ev("([l,k])=>__HR.board(l,k)", ['민사소송법', '기출'])
        hk = 'card|기출|민기출 16-53-3-조합수동소송조합책임고필공,항소심고필누락하자치유-재소금지,{소}-이행반소본소확인이익흠결X'
        R['hot0'] = p.ev("__HR.hotStyle()")
        at = p.ev("([c,x])=>__HR.clickAt(c,x)", [hk, 'title']); p.click(at, 400); p.ev("__HR.closePops()")
        R['hot'] = p.ev("__HR.hotStyle()")
        if tag == 'NEW':
            # 차례 단추 — 단원별(비활성) 눌러도 아무 일 없음 · 회차별 누르면 그대로 켜짐
            p.ev("([l,k])=>__HR.board(l,k)", ['특허법', '기출'])
            p.ev("__HR.mark()")
            at = p.ev("o=>__HR.segAt(o)", 'unit')
            if at and at.get('onScreen'):
                # disabled 단추는 elementFromPoint 가 부모(.ordseg)를 준다 — 화면 안이면 그 자리를 진짜로 누른다
                p.pg.mouse.click(at['cx'], at['cy']); p.pg.wait_for_timeout(700)
            R['segUnit'] = {'at': at, 'marked': p.ev("__HR.marked()"), 'b': p.ev("__HR.boardRead()")['seg'], 'S': p.ev("()=>S.c2ord||null"),
                            'ui': p.ev("()=>JSON.parse(localStorage.getItem('jopangi_ui')||'{}').c2ord||null")}
            at = p.ev("o=>__HR.segAt(o)", 'round')
            p.click(at, 900)
            R['segRound'] = {'at': at, 'marked': p.ev("__HR.marked()"), 'b': p.ev("__HR.boardRead()")['seg'],
                             'ui': p.ev("()=>JSON.parse(localStorage.getItem('jopangi_ui')||'{}').c2ord||null")}
        if tag == 'NEW':
            # 폭이 바뀌면(resize) · 배지 글자가 줄면(ResizeObserver) 배지 묶음이 오르내린다 — 첫 줄은 늘 한 줄
            p.ev("([l,t])=>__HR.go(l,t)", ['특허법', 'jo'])
            D = {}
            p.pg.set_viewport_size({'width': 1024, 'height': 900}); p.pg.wait_for_timeout(600)
            D['w1024'] = p.ev("__HR.hdr()")
            D['shrink'] = p.ev("on=>__HR.badgeShrink(on)", True)
            D['restore'] = p.ev("on=>__HR.badgeShrink(on)", False)
            p.pg.set_viewport_size({'width': 1440, 'height': 900}); p.pg.wait_for_timeout(600)
            D['w1440'] = p.ev("__HR.hdr()")
            # 법을 바꿔도(탭 수·수 글자가 바뀜) 한 줄 — 1024 에서 민소(탭 넷) ↔ 특허
            p.pg.set_viewport_size({'width': 1024, 'height': 900}); p.pg.wait_for_timeout(400)
            p.ev("([l,t])=>__HR.go(l,t)", ['민사소송법', 'cha2']); D['minso1024'] = p.ev("__HR.hdr()")
            p.ev("([l,t])=>__HR.go(l,t)", ['특허법', 'jimun']); p.pg.wait_for_timeout(600); D['jimun1024'] = p.ev("__HR.hdr()")
            p.pg.set_viewport_size({'width': 1440, 'height': 900}); p.pg.wait_for_timeout(400)
            R['dyn'] = D
        R['errs'] = p.ev("__HR.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:500]
    finally:
        p.close()
    return R


def row1(h):
    """첫 줄이 한 줄인가 — 높이 45 · 배지가 첫 줄에 있으면 로고와 같은 줄 · 탭도 로고와 같은 줄"""
    if not h or not h.get('top'):
        return False
    ok = abs(h['top']['h'] - 45) < 0.6 and all(abs(t['rect']['cy'] - h['logo']['cy']) < 6 for t in h.get('tabs', []))
    if h.get('hbParent') == 'header':
        ok = ok and all(abs(b['rect']['cy'] - h['logo']['cy']) < 6 for b in h.get('badges', []) if b['vis'])
    return ok


# ══════════ 세 폭 × 다섯 탭 — 가로 스크롤 0 · 배지 자리 · 캡처(chromium NEW) ══════════
def scen_wide(br, eng, tag, src, shots):
    R = {'eng': eng, 'tag': tag, 'w': {}}
    for W, H in [(768, 1024), (1024, 768), (1440, 900)]:
        p = P(br, eng, tag, src, W, H)
        try:
            for L in LAWS:
                for T in TABS:
                    p.ev("([l,t])=>__HR.go(l,t)", [L, T])
                    p.pg.wait_for_timeout(250)
                    h = p.ev("__HR.hdr()")
                    R['w']['%d|%s|%s' % (W, L, T)] = {'h': h, 'need': p.ev("__HR.need()")}
                    if T == 'cha2':
                        R['w']['%d|%s|%s' % (W, L, T)]['fit'] = p.ev("__HR.rowsFit()")
                    if shots and L == '특허법':
                        if T == 'jimun':
                            p.pg.wait_for_timeout(900)
                        png = p.pg.screenshot(full_page=False)
                        fn = os.path.join(WORK, 'shot_%d_%s.png' % (W, T)); open(fn, 'wb').write(png)
                        R['w']['%d|%s|%s' % (W, L, T)]['shot'] = fn
            R['errs_%d' % W] = p.ev("__HR.errs()") + p.errs
        except Exception as e:
            R['exc_%d' % W] = repr(e)[:500]
        finally:
            p.close()
    return R


# ══════════ 픽셀 — 사례 격자 무변 · 2차 1단/2단 무변 (chromium) ══════════
def scen_pix(br, base, new):
    from PIL import Image, ImageChops
    R = {}
    pb = P(br, 'chromium', 'BASE', base, 1480, 900)
    b2b = pb.ev("__HR.hdr()")['body2']['y']
    pn = P(br, 'chromium', 'NEW', new, 1440, 900)
    b2n = pn.ev("__HR.hdr()")['body2']['y']
    dh = int(round(b2n - b2b))
    pn.pg.set_viewport_size({'width': 1440, 'height': 900 + dh}); pn.pg.wait_for_timeout(600)
    R['dh'] = [b2b, b2n, dh]
    try:
        for L, K in SAK + [('특허법', '기출'), ('민사소송법', 'GS')]:
            out = {}
            for tag, p in (('BASE', pb), ('NEW', pn)):
                p.ev("([l,k])=>__HR.board(l,k)", [L, K])
                p.pg.wait_for_timeout(2500)
                sel = ['#slot .main', '#slot .tree', '#slot .plist'] if K == '사례' else ['#slot .tree', '#slot .plist']
                for s in sel:
                    loc = p.pg.locator(s).first
                    fn = os.path.join(WORK, 'pix_%s_%s_%s_%s.png' % (tag, SHORTN(L), K, s.split('.')[-1]))
                    loc.screenshot(path=fn)
                    out.setdefault(s, {})[tag] = fn
                out.setdefault('rect', {})[tag] = p.ev("()=>{const m=document.querySelector('#slot .main');const r=m.getBoundingClientRect();return [r.width,r.height]}")
            res = {}
            for s, d in out.items():
                if s == 'rect':
                    res['rect'] = d; continue
                a, b = Image.open(d['BASE']).convert('RGB'), Image.open(d['NEW']).convert('RGB')
                if a.size != b.size:
                    res[s] = {'same': False, 'size': [a.size, b.size]}; continue
                if s == '#slot .plist':   # A-6(a) c2card §F 정렬 이름(「해례·회차 순」→「회차 순」/「사례 순」) — 정렬 select 자리만 칠해 빼고 잰다
                    a.paste((0, 0, 0), (13, 7, 116, 32)); b.paste((0, 0, 0), (13, 7, 116, 32))
                # 맨 윗줄 1px = 머리 아래 테두리가 스며든 줄(본문 위 y 가 .86 이라 잘라 찍을 때 들어온다 · 바탕 --line → 새 #d9d5cb 지시서 값)
                top = ImageChops.difference(a.crop((0, 0, a.size[0], 1)), b.crop((0, 0, b.size[0], 1)))
                d2 = ImageChops.difference(a.crop((0, 1, a.size[0], a.size[1])), b.crop((0, 1, b.size[0], b.size[1])))
                px = list(d2.getdata()); nz = sum(1 for q in px if q != (0, 0, 0)); big = sum(1 for q in px if max(q) > 2); mx = max(max(q) for q in px)
                res[s] = {'size': a.size, 'row0': [a.getpixel((2, 0)), b.getpixel((2, 0))], 'row0diff': top.getbbox() is not None,
                          'nz': nz, 'big': big, 'max': mx, 'bbox': d2.getbbox()}
            R[L + '|' + K] = res
    except Exception as e:
        R['exc'] = repr(e)[:500]
    finally:
        pb.close(); pn.close()
    return R


def FOLD(x):
    """보드 머리의 본문 접힘 알약(「본문 뼈대 ▾」·「본문 제목만 ▾」·「본문 펼침 ▴」)"""
    return x.get('tag') == 'BUTTON' and re.match(r'^본문 (뼈대|제목만|펼침)', x.get('t') or '') is not None


def NOISE(x):
    """바탕에도 같은 자리에서 나는 것 — 1차객 화면 옛 ResizeObserver 알림 · 자원 404(콘솔)"""
    return 'ResizeObserver loop' in x or 'Failed to load resource' in x


def SHORTN(L):
    return {'특허법': '특허', '상표법': '상표', '디자인보호법': '디보', '민사소송법': '민소'}[L]


def JIMUN_N(L):
    """A-6(a) 1차객 탭 수 새 셈 — 앱 railCounts(2150~2154) 규칙: 같은 uid 는 한 번(toc_fuse 9/26 · uid 판 9/27) · 특허는 z.병합 뺌 + jimun_7pan ox O/X"""
    sh = {'특허법': '특허', '상표법': '상표', '디자인보호법': '디보'}.get(L)
    if not sh:
        return None
    j = json.load(io.open(os.path.join(JOD, 'data', 'jimun_' + sh + '.json'), encoding='utf-8'))
    ks, n = set(), 0
    for q in j.get('문제') or []:
        for z in q.get('지문') or []:
            if sh == '특허' and z.get('병합'):
                continue
            u = z.get('uid')
            if not (u and u in ks):
                n += 1
            if u:
                ks.add(u)
    if sh == '특허':
        P = json.load(io.open(os.path.join(JOD, 'data', 'jimun_7pan.json'), encoding='utf-8'))
        for z in P.get('지문') or []:
            if z.get('ox') in ('O', 'X'):
                u = z.get('uid')
                if not (u and u in ks):
                    n += 1
                    if u:
                        ks.add(u)
    return '{:,}'.format(n)


# ══════════ 아이패드 — 진짜 터치(톡) · 팝업 머리 끌기 ══════════
def scen_pad(br, eng, src, W, H):
    p = P(br, eng, 'NEW', src, W, H, pad=True)
    R = {'eng': eng, 'W': W, 'H': H}
    try:
        p.ev("([l,t])=>__HR.go(l,t)", ['특허법', 'jo'])
        R['hdr'] = p.ev("__HR.hdr()"); R['need'] = p.ev("__HR.need()")
        R['tab'] = []
        for k in ['prec', 'cha2', 'jimun', 'jo']:
            at = p.ev("k=>__HR.tabAt(k)", k)
            ok = p.click(at, 1000)
            R['tab'].append({'k': k, 'ok': ok, 'st': p.ev("__HR.state()")})
        at = p.ev("__HR.ksAt()"); p.click(at, 300)
        R['ks'] = p.ev("__HR.skOpen()"); p.ev("__HR.closePops()")
        # 2차 줄 톡 → 팝업 · 머리 끌기
        L, K, ck = POPS[0]
        p.ev("([l,k])=>__HR.board(l,k)", [L, K])
        R['fit'] = p.ev("__HR.rowsFit()")
        at = p.ev("([c,x])=>__HR.clickAt(c,x)", [ck, 'title'])
        R['rowTap'] = {'at': at, 'ok': p.click(at, 400)}
        R['pop'] = p.ev("__HR.popRead()")
        pos0 = p.ev("__HR.popPos()")
        hd = (R['pop'] or {}).get('head') or {}
        if hd.get('on'):
            R['drag'] = p.drag(hd['cx'], hd['cy'], hd['cx'] - 120, hd['cy'] + 70); p.pg.wait_for_timeout(400)
        R['pos'] = [pos0, p.ev("__HR.popPos()")]
        p.ev("__HR.closePops()")
        # 점수 칩 톡 → 채점 탭
        at = p.ev("([c,x])=>__HR.clickAt(c,x)", [ck, 'score'])
        R['scoreTap'] = {'ok': p.click(at, 400), 'pop': p.ev("__HR.popRead()")}
        p.ev("__HR.closePops()")
        # 1차객 틈 0 (아이패드)
        R['jim'] = p.ev("s=>__HR.jim(s)", 'home')
        R['errs'] = p.ev("__HR.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:500]
    finally:
        p.close()
    return R


def main():
    os.makedirs(WORK, exist_ok=True)
    new_raw = open(os.path.join(GENIE, REL), 'rb').read()
    new = new_raw.decode('utf-8')
    base_b = git('show', BASE_REV + ':' + REL)
    base = base_b.decode('utf-8')
    RES = {'src': {'base': [len(base_b), hashlib.md5(base_b).hexdigest()],
                   'new': [len(new_raw), hashlib.md5(new_raw.replace(b'\r\n', b'\n')).hexdigest(), new_raw.count(b'\r\n'), new_raw.count(b'\n')]}}
    t00 = time.time()
    with sync_playwright() as pw:
        brs = {}
        for eng in ('chromium', 'webkit'):
            brs[eng] = getattr(pw, eng).launch()
        try:
            for eng in ('chromium', 'webkit'):
                if not ONLY or ONLY == 'desk':
                    for tag, src in (('BASE', base), ('NEW', new)):
                        t0 = time.time(); print('… desk %s/%s' % (eng, tag), flush=True)
                        RES['desk/%s/%s' % (eng, tag)] = scen_desk(brs[eng], eng, tag, src)
                        print('   %.1fs %s' % (time.time() - t0, RES['desk/%s/%s' % (eng, tag)].get('exc', '')), flush=True)
                if not ONLY or ONLY == 'wide':
                    for tag, src in (('BASE', base), ('NEW', new)):
                        t0 = time.time(); print('… wide %s/%s' % (eng, tag), flush=True)
                        RES['wide/%s/%s' % (eng, tag)] = scen_wide(brs[eng], eng, tag, src, shots=(eng == 'chromium' and tag == 'NEW'))
                        print('   %.1fs' % (time.time() - t0), flush=True)
                if not ONLY or ONLY == 'pad':
                    for W, H in [(768, 1024), (1024, 768)]:
                        t0 = time.time(); print('… pad %s %dx%d' % (eng, W, H), flush=True)
                        RES['pad/%s/%d' % (eng, W)] = scen_pad(brs[eng], eng, new, W, H)
                        print('   %.1fs %s' % (time.time() - t0, RES['pad/%s/%d' % (eng, W)].get('exc', '')), flush=True)
            if not ONLY or ONLY == 'pix':
                t0 = time.time(); print('… pix chromium', flush=True)
                RES['pix'] = scen_pix(brs['chromium'], base, new)
                print('   %.1fs' % (time.time() - t0), flush=True)
        finally:
            for b in brs.values():
                b.close()
            for srv, _ in SERVERS.values():
                srv.shutdown()
    RES['sec'] = round(time.time() - t00, 1)
    json.dump(RES, io.open(os.path.join(WORK, 'raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    report(RES, base, new)


# ══════════ 판정 ══════════
def report(RES, base, new):
    L = []
    T = lambda n, c, i=None: L.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c or i is None else ' | ' + json.dumps(i, ensure_ascii=False)[:900]))
    I = lambda n, v: L.append('INFO | ' + n + ' | ' + (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)[:1600]))
    g = lambda d, *ks: (lambda x: x)(__import__('functools').reduce(lambda a, k: (a or {}).get(k) if isinstance(a, dict) else None, ks, d))
    sb, sn = RES['src']['base'], RES['src']['new']
    T('착수 바탕 %s = 959,738 B(CRLF) 판 · md5(LF) d2fc1e5d…' % BASE_REV, sb[1] == BASE_MD5_LF, sb)
    T('NEW 작업트리 CRLF 그대로(LF 단독 0 · %d 줄) · %d B · md5(LF) %s' % (sn[2], sn[0], sn[1]), sn[2] == sn[3], sn)
    # A-6(d) 인도 검산 = hrail 두 커밋(36234e9·d3dd927 · 부모 33be370)이 바꾼 파일 — 작업트리 git status 는 인도 전에만 선다
    ch = [l for l in git('diff', '--name-status', '33be370', 'd3dd927').decode('utf-8').split('\n') if l.strip()]
    T('genie 작업트리 바뀐 파일 = jo/index.html 하나 %s' % ch, ch == ['M\t' + REL], ch)
    nl = new.replace('\r\n', '\n'); bl = base.replace('\r\n', '\n')
    T('§A-4 소스에 세로 레일이 없다(마크업 id="rail" · CSS .rail · $(\'#rail\') 0)',
      'id="rail"' not in nl and '.rail{' not in nl and '.rail .rb' not in nl and "$('#rail')" not in nl)
    T('§0 8/23 결정 주석은 남고 「8/23 → 9/22 가로 탭으로」 한 줄이 붙었다',
      '8/23 사용자 결정.' in nl and '8/23 → 9/22 가로 탭으로' in nl)
    # A-6(d) 「SYNC_KEYS 무변」 은 hrail 판 성질 — 인도판(d3dd927) 소스로 잰다(뒤 판들이 키를 더함: 54ced94 c2unit … ffafcb0 jocheck · c2ord 두 글자는 지금 판 nl 그대로)
    nl_c1 = git('show', 'd3dd927:' + REL).decode('utf-8').replace('\r\n', '\n')
    T('§C-1 jopangi_ui.c2ord — 읽기(round|unit) · uiSave 에 c2ord · SYNC_KEYS 무변',
      "c2ord:S.c2ord||'round'" in nl and "u4.c2ord==='round'||u4.c2ord==='unit'" in nl
      and re.search(r'const SYNC_KEYS = \[(.+?)\]', nl_c1, re.S).group(1) == re.search(r'const SYNC_KEYS = \[(.+?)\]', bl, re.S).group(1))
    for eng in ('chromium', 'webkit'):
        B, N = RES.get('desk/%s/BASE' % eng), RES.get('desk/%s/NEW' % eng)
        if not B or not N:
            continue
        E = '[%s] ' % eng
        if B.get('exc') or N.get('exc'):
            T(E + '책상 시나리오 예외 0', False, [B.get('exc'), N.get('exc')])
        # ── A census
        bad, rows = [], []
        for k in [l + '|' + t for l in LAWS for t in TABS]:
            cb, cn = g(B, 'census', k, 'c') or {}, g(N, 'census', k, 'c') or {}
            ib = [(x['label'], x['n'], x['on']) for x in cb.get('items', [])]
            inn = [(x['label'], x['n'], x['on']) for x in cn.get('items', [])]
            # A-6(a) 바탕 #rail 에 뒤 판 둘만 입힌 기대 — ① 「2차」 바로 뒤 「목차노트」 칸(mok_popup_phone §A) ② 1차객 수 = 같은 uid 한 번(JIMUN_N)
            ibx = []
            for x in ib:
                ibx.append((x[0], JIMUN_N(k.split('|')[0]), x[2]) if x[0] == '1차객 ' else x)
                if x[0] == '2차 ':
                    ibx += [y for y in inn if y[0] == '목차노트 ' and y[2] is False][:1] or [('목차노트 ', None, False)]
            if ibx != inn or cb.get('host') != 'rail' or cn.get('host') != 'hrail' or not ib:
                bad.append([k, ib, inn])
            rows.append([k, ' · '.join('%s%s%s' % (a.strip(), (' ' + n) if n else '', '●' if o else '') for a, n, o in inn)])
        T(E + '관문 A census — 20 상태(법 넷 × 탭 다섯) #hrail 칸 수·글자·수·켜짐 = 바탕 #rail 글자 + 목차노트 칸 · 1차객 새 셈(같은 uid 한 번)', not bad and len(rows) == 20, bad[:3])
        if eng == 'chromium':
            I(E + 'census 표(NEW #hrail · ● 켜짐)', '\n        ' + '\n        '.join('%s : %s' % (a, b) for a, b in rows))
        hB, hN = B.get('hdr') or {}, N.get('hdr') or {}
        T(E + '#rail 0개(NEW) · 바탕 1개(헛잣대)', hN.get('rail') == 0 and hB.get('rail') == 1, [hN.get('rail'), hB.get('rail')])
        # ★ jo_hdrfold(9/28) — 머리 세모 ▴(#hdrFold)는 #laws 와 #hrail 사이(지시서 §A-1) — 걸러 잰다
        T(E + '#hrail 은 #laws 바로 뒤(▴ #hdrFold 걸러) · 배지 묶음 · 첫 줄 자식 차례', [c for c in (hN.get('children') or []) if c != 'hdrFold'][:4] == ['logo', 'laws', 'hrail', 'hbadges'], hN.get('children'))
        tabs = hN.get('tabs') or []
        T(E + '§A-2 탭 꼴 — 26px · 12.5px · #4b5563 · 모서리 7 · 수 11px · .75 · 왼쪽 5 · 켜짐 = --exc 바탕 흰 글자',
          tabs and all(abs(t['rect']['h'] - 26) < 0.6 and t['fs'] == '12.5px' and t['br'] == '7px' and t['nfs'] == '11px' and t['nop'] == '0.75' and t['nml'] == '5px' for t in tabs)
          and all((t['bg'] == 'rgb(47, 111, 208)' and t['color'] == 'rgb(255, 255, 255)') if t['on'] else (t['color'] == 'rgb(75, 85, 99)' and t['bg'] == 'rgba(0, 0, 0, 0)') for t in tabs),
          tabs)
        hs = hN.get('hrStyle') or {}
        T(E + '구분선 — #hrail 왼쪽 1px #cfcabd · 좌우 10(margin·padding)', hs.get('bl') == '1px' and hs.get('blc') == 'rgb(207, 202, 189)' and hs.get('ml') == '10px' and hs.get('pl') == '10px', hs)
        if eng == 'chromium':
            I(E + '1440 실측 — 법 칩 끝 x · 탭 폭 · 탭 줄 x · 구분선 · 배지 · 검색줄 · 머리 두 줄',
              {'laws_r': g(hN, 'laws', 'r'), 'tabs_w': [round(t['rect']['w'], 1) for t in tabs], 'tabs_x': [g(tabs[0], 'rect', 'x') if tabs else None, g(tabs[-1], 'rect', 'r') if tabs else None],
               'hrail': hN.get('hr'), 'badges_parent': hN.get('hbParent'), 'badges': [g(hN, 'hb', 'x'), g(hN, 'hb', 'r')], 'row1_h': g(hN, 'top', 'h'),
               'search': [g(hN, 'ks', 'x'), g(hN, 'ks', 'r'), g(hN, 'ks', 'h')], 'row2_h': g(hN, 'row', 'h'), 'body2_y': g(hN, 'body2', 'y'),
               'mock': '시안 = 법 칩 끝 ≈269 · 탭 74/74/94/69/62 · 탭 줄 298~687 · 검색 12~1428 h34 · 머리 94'})
        T(E + '검색줄 = 둘째 줄(#hsrow · 첫 줄 아래 · 전폭 x 12~W-12 · flex 1)',
          hN.get('ksParent') == 'hsrow' and g(hN, 'ks', 'y') >= g(hN, 'top', 'b') - 0.5 and abs(g(hN, 'ks', 'x') - 12) < 1 and abs(g(hN, 'ks', 'r') - (hN['W'] - 12)) < 1
          and (hN.get('ksStyle') or [None])[0] == '1',
          [hN.get('ksParent'), hN.get('ks'), hN.get('top'), hN.get('ksStyle')])
        T(E + '검색줄 바탕 = 머리 바탕 · 아래 테두리 1px #d9d5cb · padding 7 12', (hN.get('rowStyle') or [None])[2] == hN.get('topBg')
          and (hN.get('rowStyle') or [None] * 4)[3] == '1px rgb(217, 213, 203)' and (hN.get('rowStyle') or [None, None])[1] == '7px 12px', [hN.get('rowStyle'), hN.get('topBg')])
        T(E + '1440 — 배지 여섯 첫 줄 오른쪽(margin-left:auto · 끝 = W-14) · 첫 줄 한 줄', hN.get('hbParent') == 'header' and abs(g(hN, 'hb', 'r') - (hN['W'] - 14)) < 1
          and all(abs(b['rect']['cy'] - g(hN, 'logo', 'cy')) < 6 for b in hN.get('badges', []) if b['vis']), [hN.get('hbParent'), hN.get('hb')])
        T(E + '양방향 — 머리 로고·법 칩·배지 여섯 글자 = 바탕(동기화 시각 숫자는 뺌)',
          hN.get('logoT') == hB.get('logoT') and hN.get('lawsT') == hB.get('lawsT')
          and [re.sub(r'\d', '#', b['text']) for b in hN.get('badges', [])] == [re.sub(r'\d', '#', b['text']) for b in hB.get('badges', [])]
          and [b['vis'] for b in hN.get('badges', [])] == [b['vis'] for b in hB.get('badges', [])],
          [[b['text'] for b in hN.get('badges', [])], [b['text'] for b in hB.get('badges', [])]])
        T(E + 'Ctrl K → 검색 창 열림(바탕도 열림)', g(N, 'ctrlK', 'open') and g(B, 'ctrlK', 'open'), [N.get('ctrlK'), B.get('ctrlK')])
        tc = N.get('tabclick') or []
        T(E + '탭 클릭(진짜 마우스) → S.tab 바뀜 · 그 칸 켜짐', len(tc) == 5 and all(x['ok'] and x['st']['tab'] == x['k'] and x['st']['on'].startswith({'jo': '조문', 'prec': '판례', 'jimun': '1차객', 'cha2': '2차', 'omr': '정리'}[x['k']]) for x in tc),
          [[x['k'], x['ok'], x['st']] for x in tc])
        T(E + '검색줄 클릭(진짜 마우스) → 검색 창', g(N, 'ksClick', 'open') is True, N.get('ksClick'))
        # ── B
        for s in ('home', 'solve', 'gichul'):
            jn, jb = g(N, 'jim', s) or {}, g(B, 'jim', s) or {}
            f = jn.get('first') or {}
            mn = jn.get('main') or {}
            if s == 'gichul':   # ★ revfix0928 A-4 — 기출뷰 = 민법 값(본문 폭 896 가운데 · max-w-4xl mx-auto) → 첫 요소는 .main 안쪽 폭 가운데 · 틈 0 은 .main 왼쪽으로 잰다
                okx = bool(f and mn) and abs(mn['x'] - jn['jt']['r']) < 0.6 and abs((f['rect']['x'] - mn['x']) - ((jn.get('mainCW') or 0) - f['rect']['w']) / 2) < 1.5
            else:
                okx = bool(f) and abs(f['rect']['x'] - jn['jt']['r']) < 0.6
            T(E + '관문 B %s — 본문 첫 요소(%s) 왼쪽 = 서랍 오른쪽 끝(손잡이 옆)%s · 위 = .body2 위' % (s, f.get('cls'), ' — 기출뷰는 .main 왼쪽 = 서랍 끝 · 첫 요소 = .main 안 가운데(revfix0928 A-4 896)' if s == 'gichul' else ''),
              jn.get('jtDisp') != 'none' and f and okx and abs(f['rect']['y'] - jn['body2']['y']) < 0.6
              and jn.get('mainPad') == '0px 0px 90px' and 'mbflush' in (jn.get('mainCls') or ''),
              {'first': f, 'jt': jn.get('jt'), 'grip': jn.get('grip'), 'body2': jn.get('body2'), 'pad': jn.get('mainPad'), 'err': jn.get('err')})
            fb = jb.get('first') or {}
            I(E + 'B %s 실측 NEW 첫 요소 x %s y %s · 서랍 %s~%s · 손잡이 %s~%s · .body2 y %s │ 바탕 x %s y %s pad %s' % (
                s, g(f, 'rect', 'x'), g(f, 'rect', 'y'), g(jn, 'jt', 'x'), g(jn, 'jt', 'r'), g(jn, 'grip', 'x'), g(jn, 'grip', 'r'), g(jn, 'body2', 'y'),
                g(fb, 'rect', 'x'), g(fb, 'rect', 'y'), jb.get('mainPad')), {'mok': jn.get('mok'), 'jtab': jn.get('jtab'), 'qcards': jn.get('qcards')})
        mh, mb = g(N, 'jim', 'home', 'mbh') or {}, g(B, 'jim', 'home', 'mbh') or {}
        T(E + '§B-1 첫 화면 .mbh — 모서리 0 · 옆·위 테두리 0 · 그림자 없음 · 아래 여백 10(바탕 16px · 그림자 · 14)',
          mh.get('br') == '0px' and mh.get('bl') == '0px' and mh.get('brw') == '0px' and mh.get('bt') == '0px' and mh.get('sh') == 'none' and mh.get('mb') == '10px'
          and mb.get('br') == '16px' and mb.get('sh') != 'none', [mh, mb])
        T(E + '§B-1 문제풀이 화면이 진짜로 떴다(단원 줄 → S.mok · 지문 카드) · 기출 화면(S.jimunTab=gichul)', bool(g(N, 'jim', 'solve', 'mok')) and (g(N, 'jim', 'solve', 'qcards') or 0) > 0
          and g(N, 'jim', 'gichul', 'jtab') == 'gichul', [g(N, 'jim', 'solve', 'mok'), g(N, 'jim', 'solve', 'qcards'), g(N, 'jim', 'gichul', 'jtab')])
        T(E + '관문 B — 조문·판례·2차·정리 탭 .main padding = 바탕 그대로(%s)' % ' · '.join('%s %s' % (k2, (v or [None])[0]) for k2, v in (B.get('pads') or {}).items()),
          N.get('pads') == B.get('pads') and len(N.get('pads') or {}) == 4, [N.get('pads'), B.get('pads')])
        # ── C 보드
        for L0, K0 in BOARDS:
            k = L0 + '|' + K0
            bb, bn = g(B, 'boards', k) or {}, g(N, 'boards', k) or {}
            cb = [x['ck'] for x in bb.get('rows', [])]; cn = [x['ck'] for x in bn.get('rows', [])]
            T(E + '관문 C %s — 줄 수 = 바탕 격자 셀 수(%d) · 같은 카드 집합' % (k, len(cb)), len(cn) == len(cb) and len(cb) > 0 and sorted(cn) == sorted(cb)
              and all('c2row' in x['cls'] for x in bn.get('rows', [])), [len(cn), len(cb), sorted(set(cb) - set(cn))[:3], sorted(set(cn) - set(cb))[:3]])
            # 차례 = 회차 내림 · 문번 오름
            codes = [x['code'] for x in bn.get('rows', [])]
            key = lambda c: [int(v) for v in c.split('-')]
            ok_order = True
            for a, b in zip(bn.get('rows', []), bn.get('rows', [])[1:]):
                ka, kb2 = key(a['code']), key(b['code'])
                ra, rb = ka[:-1], kb2[:-1]
                if ra[-1:] and (ra if len(ra) == 1 else ra) < rb:
                    ok_order = False
                if ra == rb and ka[-1] > kb2[-1]:
                    ok_order = False
            rounds = [key(c)[:-1] for c in codes]
            # 기출 = [YY, 회] → 회 기준 · GS = [YY, 회] 그 자체
            T(E + '관문 C %s — 차례 = 회차 내림 · 문번 오름 · 첫 줄 = 최신 회차 1번(%s)' % (k, codes[0] if codes else '—'),
              codes and ok_order and codes[0].split('-')[-1] == '1' and rounds[0] == max(rounds), codes[:6])
            bt = {x['ck']: (x['title'], x['score'], x['pdf']) for x in bb.get('rows', [])}
            mism = [x['ck'] for x in bn.get('rows', []) if bt.get(x['ck']) != (x['title'], x['score'], x['pdf'])]
            T(E + '양방향 %s — 줄마다 논점·점수 칩·해설 칩 = 바탕 칸의 .ctitle·머리 칩 글자 그대로' % k, not mism, mism[:3])
            # A-6(a) 2cha_unit §B-8 줄 꼴(제목 .c2t2 먼저 · 갈래 칩 c2k·회번 c2rn 뺌 · GS 시리즈 c2ser) · 민소 기출 숨은 Claude 자리표('' · ms_claude_editq C-3 · 답 있으면 mbcl)
            bad_form = [x['ck'] for x in bn.get('rows', []) if x['kids'] != ['c2code', 'c2mid', 'c2r3'] or not x['t1kids'] or x['t1kids'][0] != 'c2t2'
                        or not re.match(r'^\d{2}-\d+-\d+$', x['code']) or x['kind'] != ''
                        or any(c not in ('c2t2', 'c2ser', 'chip c-src c2n', '') and not c.startswith('chip c-score') and c != 'chip c-pdf' and not c.startswith('mbcl') for c in x['t1kids'])]
            T(E + '없던 것이 서 있지 않다 %s — 줄 = 코드 │ 논점 · (시리즈) · (사례번호) · 점수 칩 · (Claude) · (해설) │ 셋째 칸 · 코드 YY-회-N' % k, not bad_form, bad_form[:3])
            T(E + '%s — 격자 전용 것(열 머리 .gh · cellnone · .grid) 0 · 목록 1 · 바탕은 격자' % k, bn.get('gh') == 0 and bn.get('cellnone') == 0 and bn.get('grid') == 0 and bn.get('list') == 1
              and bb.get('grid') == 1, [bn.get('gh'), bn.get('cellnone'), bn.get('grid'), bn.get('list'), bb.get('grid')])
            T(E + '%s — 미배치 상자·하단 배지 = 바탕 · 2단 목록(prow) 글자·1단 필터 글자 = 바탕' % k, bn.get('unpl') == bb.get('unpl') and bn.get('badge') == bb.get('badge')
              and [x['t'] for x in bn.get('prow', [])] == [x['t'] for x in bb.get('prow', [])] and bn.get('tree') == bb.get('tree'),
              [bn.get('unpl')[:60] if bn.get('unpl') else None, bb.get('unpl')[:60] if bb.get('unpl') else None, bn.get('badge'), bb.get('badge')])
            barN = [x for x in (bn.get('bar') or []) if x['id'] != 'ordSeg']
            barB = [x for x in (bb.get('bar') or []) if not FOLD(x)]
            T(E + '%s — 보드 머리 = 바탕 − 「본문 뼈대 ▾」(사용자 9/22) + #ordSeg 하나(「사례」 알약 바로 오른쪽 · 강사 select 앞)' % k,
              [(x['tag'], x['cls'], x['t']) for x in barN] == [(x['tag'], x['cls'], x['t']) for x in barB]
              and len(barB) == len(bb.get('bar') or []) - 1
              and [x['id'] for x in (bn.get('bar') or [])].count('ordSeg') == 1 and (bn.get('bar') or [{}] * 4)[3].get('id') == 'ordSeg',
              [bn.get('bar'), bb.get('bar')])
            sg = bn.get('seg') or {}
            btn = sg.get('btn') or [{}, {}]
            # A-6(a) 2cha_unit §B-1 — 민소 기출만 「단원별」 켬 · 나머지는 흐림 + 툴팁 까닭별(「GS 단원 데이터 없음」/「<법> 기출 단원 데이터 없음」)
            T(E + '%s — #ordSeg 회차별 켜짐(--exc · 흰 · 굵게) · 단원별 %s' % (k, '켬(민소 기출 단원 데이터 · 2cha_unit §B-1)' if k == '민사소송법|기출' else 'disabled · .45 · 툴팁'),
              btn[0].get('t') == '회차별' and btn[0].get('on') and btn[0].get('bg') == 'rgb(47, 111, 208)' and btn[0].get('fw') == '700'
              and btn[1].get('t') == '단원별' and ((not btn[1].get('dis') and btn[1].get('op') == '1') if k == '민사소송법|기출' else (btn[1].get('dis') and btn[1].get('op') == '0.45' and btn[1].get('title') == ('GS 단원 데이터 없음' if K0 == 'GS' else SHORTN(L0) + ' 기출 단원 데이터 없음')))
              and bb.get('seg') is None, btn)
        # 사례 = 격자 그대로 · 단추 없음
        for L0, K0 in SAK:
            k = L0 + '|' + K0
            bb, bn = g(B, 'boards', k) or {}, g(N, 'boards', k) or {}
            T(E + '%s — 격자 그대로(칸 수·차례·글자 = 바탕) · #ordSeg 없음 · 목록 0' % k,
              [x['ck'] for x in bn.get('rows', [])] == [x['ck'] for x in bb.get('rows', [])] and bn.get('n', 0) > 0 and bn.get('seg') is None and bn.get('list') == 0
              and [(x['tag'], x['cls'], x['t']) for x in (bn.get('bar') or [])] == [(x['tag'], x['cls'], x['t']) for x in (bb.get('bar') or [])],
              [bn.get('n'), bb.get('n'), bn.get('bar')])
        sb0 = g(N, 'boards', '특허법|기출') or {}
        sg = sb0.get('seg') or {}
        if eng == 'chromium':
            I(E + '#ordSeg 실측(시안 x 731 · y 109 · 111×22)', {'seg': sg.get('rect'), 'sak_r': g(sb0, 'sak', 'r'), 'gap': round((g(sg, 'rect', 'x') or 0) - (g(sb0, 'sak', 'r') or 0), 2),
                                                                'btn': [[b.get('t'), b.get('pad'), b.get('fs'), b.get('rect', {}).get('w')] for b in sg.get('btn', [])], 'bg': sg.get('bg')})
            I(E + '줄 꼴 실측', sb0.get('rowStyle'))
        T(E + '#ordSeg 자리 — 「사례」 알약 오른쪽 10px · 같은 줄', sg.get('rect') and abs((g(sg, 'rect', 'x') - g(sb0, 'sak', 'r')) - 10) < 1.1 and abs(g(sg, 'rect', 'cy') - g(sb0, 'sak', 'cy')) < 3,
          [sg.get('rect'), sb0.get('sak')])
        sakN, sakB = g(N, 'boards', '특허법|사례') or {}, g(B, 'boards', '특허법|사례') or {}
        T(E + '「본문 뼈대 ▾」 — 기출·GS 목록 머리엔 없음(사용자 9/22 결정 · 바탕엔 있었다) · 사례 머리엔 그대로(글자 = 바탕)',
          not sb0.get('fold') and bool(g(B, 'boards', '특허법|기출', 'fold')) and bool(sakN.get('fold')) and sakN.get('fold') == sakB.get('fold'),
          [sb0.get('fold'), g(B, 'boards', '특허법|기출', 'fold'), sakN.get('fold'), sakB.get('fold')])
        # 회차 거르기
        for k, v in (N.get('year') or {}).items():
            vb = g(B, 'year', k) or {}
            T(E + '회차 select 거르기 %s — 줄 수 = 바탕 칸 수(%s)' % (k, vb.get('n')), v.get('n') == vb.get('n') and (v.get('n') or 0) > 0 and sorted(v['cks']) == sorted(vb.get('cks', [])),
              [v.get('n'), vb.get('n')])
        # 팝업 글자
        for ck, d in (N.get('pops') or {}).items():
            db = g(B, 'pops', ck, 'title') or {}
            pn, pb = g(d, 'title', 'pop') or {}, g(db, 'pop') or {}
            T(E + '줄 클릭(논점 줄 · 진짜 마우스) → .pop 1개 · 글자 = 같은 카드 popCard4 팝업 그대로 — %s' % ck[:40],
              g(d, 'title', 'clicked') and db.get('clicked') and pn.get('n') == 1 and pb.get('n') == 1 and pn.get('text') == g(d, 'direct', 'pop', 'text') and len(pn.get('text') or '') > 40
              and pn.get('sel') == ck,
              {'new': [g(d, 'title', 'clicked'), pn.get('n'), (pn.get('text') or '')[:120], pn.get('sel')], 'base': [db.get('clicked'), pb.get('n'), (pb.get('text') or '')[:120]], 'at': g(d, 'title', 'at')})
            pc = g(d, 'code', 'pop') or {}
            T(E + '줄 어디든 — 코드 칸을 눌러도 같은 팝업 — %s' % ck[:40], g(d, 'code', 'clicked') and pc.get('n') == 1 and pc.get('text') == pn.get('text'),
              [g(d, 'code', 'clicked'), pc.get('n'), (pc.get('text') or '')[:80]])
        for ck, d in (N.get('scorepop') or {}).items():
            db = g(B, 'scorepop', ck) or {}
            T(E + '점수 칩 → 채점 탭 팝업 = 같은 카드 popCard4(채점) 글자 — %s' % ck[:30], d.get('clicked') and db.get('clicked') and g(d, 'pop', 'n') == 1
              and g(d, 'pop', 'text') == g(d, 'direct', 'text') and g(d, 'pop', 'tab') == '채점', [g(d, 'pop', 'tab'), (g(d, 'pop', 'text') or '')[:80], (g(db, 'pop', 'text') or '')[:80]])
        graded = [(x['ck'], x['score']) for kk in ('특허법|기출', '민사소송법|기출') for x in (g(N, 'boards', kk) or {}).get('rows', []) if x['score'] != '미채점']
        graded_b = [(x['ck'], x['score']) for kk in ('특허법|기출', '민사소송법|기출') for x in (g(B, 'boards', kk) or {}).get('rows', []) if x['score'] != '미채점']
        T(E + '채점 칩 전부(특허 4 · 민소 4) 글자 = 바탕 칸 머리 칩', len(graded) == 8 and sorted(graded) == sorted(graded_b), [graded, graded_b])
        I(E + '채점 칩', [s for _, s in graded])
        ys = N.get('ysort') or {}
        T(E + '연도·회차 단추 — 기본 「↓」 회차 내림 → 누르면 「↑」 오름(첫 줄 03-40-1) → 다시 「↓」', (ys.get('b0') or '').endswith('↓') and (ys.get('s0') or [''])[0] == '26-63-1'
          and (ys.get('b1') or '').endswith('↑') and (ys.get('s1') or [''])[0] == '03-40-1' and ys.get('s2') == ys.get('s0'),
          {k2: (v[:4] if isinstance(v, list) else v) for k2, v in ys.items()})
        for ck, d in (N.get('prow') or {}).items():
            c = d.get('c') or {}
            clamp = c.get('top') is not None and (c['top'] <= 1 or c['top'] >= c['max'] - 1)
            T(E + '2단 행 클릭 → 그 줄이 보드 가운데(±24px · 끝이면 끝까지) · 줄·행 선택 — %s' % ck[:36],
              d.get('at', {}).get('on') and c.get('sel') and c.get('S') == ck and (abs(c.get('dy', 999)) <= 24 or clamp) and c.get('prowSel') == [ck], d)
        fo = N.get('follow') or {}
        T(E + '보드 스크롤 → 2단 선택이 따라온다(가운데 줄)', g(fo, 'r', 'S') == fo.get('ck') and g(fo, 'r', 'prowSel') == [fo.get('ck')], fo)
        ho, hb0 = N.get('hot') or {}, B.get('hot') or {}
        T(E + '결론반대·누락 줄(민소 기출 1건 · 바탕 칸도 1건) 테두리 #f0b27a', g(ho, 'hot', 'bd') == 'rgb(240, 178, 122)' and g(ho, 'hot', 'row') is True
          and g(N, 'hot0', 'nhot') == 1 and g(B, 'hot0', 'nhot') == 1, [ho.get('hot'), g(N, 'hot0', 'nhot'), g(B, 'hot0', 'nhot'), hb0.get('hot')])
        T(E + '누른 줄 = 선택 — 옛 .cell.sel 과 같은 꼴(#d4a72c · 2px #fff7d6 · 바탕 칸도 같은 값)', g(ho, 'sel', 'row') is True
          and g(ho, 'sel', 'bd') == g(hb0, 'sel', 'bd') == 'rgb(212, 167, 44)' and g(ho, 'sel', 'sh') == g(hb0, 'sel', 'sh') and 'rgb(255, 247, 214)' in (g(ho, 'sel', 'sh') or ''),
          [ho.get('sel'), hb0.get('sel')])
        su, sr = N.get('segUnit') or {}, N.get('segRound') or {}
        T(E + '「단원별」 눌러도 아무 일 없음(다시 안 그림 · c2ord 무변) · 「회차별」 누르면 켜진 채 · jopangi_ui.c2ord = round',
          su.get('at') and su.get('marked') is True and su.get('S') in (None, 'round') and su.get('ui') in (None, 'round')
          and (su.get('b') or {}).get('btn', [{}])[0].get('on') and sr.get('marked') is False and (sr.get('b') or {}).get('btn', [{}])[0].get('on') and sr.get('ui') == 'round',
          [su, sr])
        D = N.get('dyn') or {}
        seq = [(k2, (D.get(k2) or {}).get('hbParent'), row1(D.get(k2))) for k2 in ('w1024', 'shrink', 'restore', 'w1440', 'minso1024', 'jimun1024')]
        T(E + '배지 묶음 오르내림 — 1024 = 둘째 줄 → 배지 글자 줄이면 첫 줄 → 되돌리면 둘째 줄 → 1440 = 첫 줄 · 1024 민소(탭 넷)·1차객 · 늘 첫 줄 한 줄',
          [x[1] for x in seq[:4]] == ['hsrow', 'header', 'hsrow', 'header'] and all(x[2] for x in seq) and seq[4][1] in ('header', 'hsrow') and seq[5][1] == 'hsrow', seq)
        en, eb = N.get('errs') or [], B.get('errs') or []
        T(E + 'JS 오류 0(NEW · ResizeObserver loop 알림·자원 404 줄은 뺌 — 바탕에도 같은 자리에서 난다)', not [x for x in en if not NOISE(x)], [x for x in en if not NOISE(x)])
        T(E + 'ResizeObserver loop 알림 수 ≤ 바탕(1차객 화면들의 옛 관찰자 · 새 판 %d / 바탕 %d)' % (sum('ResizeObserver' in x for x in en), sum('ResizeObserver' in x for x in eb)),
          sum('ResizeObserver' in x for x in en) <= sum('ResizeObserver' in x for x in eb))
    # ── 세 폭
    for eng in ('chromium', 'webkit'):
        W0 = RES.get('wide/%s/NEW' % eng)
        if not W0:
            continue
        E = '[%s] ' % eng
        badw, where = [], {}
        for k, v in W0['w'].items():
            h = v['h']; sw = h['sw']
            over = [n for n, x in sw.items() if x and x[0] > x[1] + 1]
            off = [b['id'] for b in h['badges'] if b['vis'] and (b['rect']['r'] > h['W'] + 0.5 or b['rect']['x'] < -0.5)]
            offt = [t['t'] for t in h['tabs'] if t['rect']['r'] > h['W'] + 0.5]
            wrapTabs = [t['t'] for t in h['tabs'] if abs(t['rect']['cy'] - h['logo']['cy']) > 6]
            one = row1(h)
            if over or off or offt or wrapTabs or h['rail'] != 0 or not one:
                badw.append([k, over, off, offt, wrapTabs, 'row1' if not one else '', h['top']['h'], h.get('hbParent')])
            where.setdefault(k.split('|')[0], set()).add(h['hbParent'])
        T(E + '관문 A — 768·1024·1440 × 법 넷 × 탭 다섯(60 상태) 가로 스크롤 0 · 배지·탭이 창 밖에 없다 · 첫 줄은 한 줄(h 45 · 배지가 첫 줄이면 로고와 같은 줄)',
          not badw and len(W0['w']) == 60, badw[:4])
        I(E + '배지 묶음 자리(폭별)', {k: sorted(v) for k, v in where.items()})
        fits = {k: v['fit'] for k, v in W0['w'].items() if v.get('fit')}
        T(E + '2차 목록 줄 — 세 폭 × 법 넷(기출 보드) 줄 안 요소가 줄 테두리를 안 넘는다(점수 칩 포함)',
          len(fits) == 12 and all(f['n'] > 0 and f['nbad'] == 0 for f in fits.values()), {k: f for k, f in fits.items() if f['nbad'] or not f['n']})
        I(E + '2차 목록 줄 폭(폭별 · 특허)', {k.split('|')[0]: f.get('w') for k, f in fits.items() if '|특허법|' in k})
        for wv in ('768', '1024', '1440'):
            v = W0['w'].get(wv + '|특허법|jo') or {}
            h = v.get('h') or {}
            I(E + '%s 폭 실측(특허 조문) — 첫 줄에 다 넣으면 필요 %s px / 창 %s · 배지 = %s · 첫 줄 h %s · 둘째 줄 h %s · .body2 y %s · 검색 x %s~%s' % (
                wv, g(v, 'need', 'need'), g(v, 'need', 'avail'), h.get('hbParent'), g(h, 'top', 'h'), g(h, 'row', 'h'), g(h, 'body2', 'y'), g(h, 'ks', 'x'), g(h, 'ks', 'r')),
              {'badges': [g(h, 'hb', 'x'), g(h, 'hb', 'r')], 'tabs_x': [h['tabs'][0]['rect']['x'], h['tabs'][-1]['rect']['r']] if h.get('tabs') else None})
        if eng == 'chromium':
            nshot = sum(1 for v in W0['w'].values() if v.get('shot'))
            T(E + '캡처 세 폭 × 다섯 탭 = 15장', nshot == 15, nshot)
        ew = [x for k2 in ('errs_768', 'errs_1024', 'errs_1440') for x in (W0.get(k2) or []) if not NOISE(x)]
        T(E + '세 폭 JS 오류 0(ResizeObserver loop 알림·자원 404 줄은 뺌)', not ew, ew[:4])
        WB = RES.get('wide/%s/BASE' % eng)
        if WB:
            ob = [k for k, v in WB['w'].items() if any(x and x[0] > x[1] + 1 for x in v['h']['sw'].values())]
            I(E + '바탕 세 폭 가로 넘침 상태 수(참고)', len(ob))
    # ── 픽셀
    PX = RES.get('pix') or {}
    if PX:
        I('픽셀 창 맞춤 — 바탕 1480×900 · 새 판 1440×(900+Δ) · .body2 y [바탕, 새, Δ]', PX.get('dh'))
        if PX.get('exc'):
            T('픽셀 시나리오 예외 0', False, PX.get('exc'))
        for k, v in PX.items():
            if not isinstance(v, dict) or k in ('dh',):
                continue
            for s, r in v.items():
                if s == 'rect':
                    continue
                if s == '#slot .main':
                    T('픽셀 %s 본문(격자) — 바탕 = 새 판 · 같은 크기 · 맨 윗줄(머리 테두리) 아래 다른 픽셀 0' % k, r.get('nz') == 0 and 'size' in r, r)
                else:
                    T('픽셀 %s %s — 맨 윗줄 아래 2단계 넘는 차이 0(select 모서리 앤티에일리어싱 ±1 은 셈만 · %s px)' % (k, s, r.get('nz')), r.get('big') == 0 and 'size' in r, r)
                I('픽셀 %s %s 맨 윗줄 [바탕, 새] = 머리 아래 테두리 색' % (k, s), r.get('row0'))
            I('픽셀 %s 본문 크기 [바탕, 새]' % k, v.get('rect'))
    # ── 아이패드
    for eng in ('chromium', 'webkit'):
        for W in (768, 1024):
            D = RES.get('pad/%s/%d' % (eng, W))
            if not D:
                continue
            E = '[%s 아이패드 %d] ' % (eng, W)
            if D.get('exc'):
                T(E + '예외 0', False, D.get('exc'))
            h = D.get('hdr') or {}
            T(E + '가로 스크롤 0 · 배지 창 안 · 탭 첫 줄', all(not x or x[0] <= x[1] + 1 for x in (h.get('sw') or {}).values())
              and all(b['rect']['r'] <= h['W'] + 0.5 for b in h.get('badges', []) if b['vis'])
              and all(abs(t['rect']['cy'] - h['logo']['cy']) < 6 for t in h.get('tabs', [])) and row1(h), [h.get('sw'), h.get('hbParent'), g(h, 'top', 'h'), g(D, 'need')])
            I(E + '배지 자리 %s · 첫 줄 필요 %s / %s · .body2 y %s' % (h.get('hbParent'), g(D, 'need', 'need'), g(D, 'need', 'avail'), g(h, 'body2', 'y')), '')
            T(E + '탭 톡(진짜 터치) → S.tab 바뀜', all(x['ok'] and x['st']['tab'] == x['k'] for x in D.get('tab', [])), D.get('tab'))
            T(E + '검색줄 톡 → 검색 창', D.get('ks') is True, D.get('ks'))
            pp = D.get('pop') or {}
            T(E + '2차 목록 줄 안 요소가 줄 테두리를 안 넘는다(줄 폭 %s)' % g(D, 'fit', 'w'), g(D, 'fit', 'n') and g(D, 'fit', 'nbad') == 0, D.get('fit'))
            T(E + '2차 줄 톡 → 팝업 1개(그 카드)', g(D, 'rowTap', 'ok') and pp.get('n') == 1 and pp.get('sel') == POPS[0][2], [D.get('rowTap'), pp.get('n'), pp.get('sel')])
            ps = D.get('pos') or [None, None]
            mv = ps[0] and ps[1] and abs((ps[1]['l'] - ps[0]['l']) + 120) < 6 and abs((ps[1]['t'] - ps[0]['t']) - 70) < 6
            T(E + '팝업 손잡이(머리) 끌기 → 옮겨짐(-120, +70) · %s' % D.get('drag'), bool(mv), ps)
            T(E + '점수 칩 톡 → 채점 탭 팝업', g(D, 'scoreTap', 'ok') and g(D, 'scoreTap', 'pop', 'n') == 1 and g(D, 'scoreTap', 'pop', 'tab') == '채점', g(D, 'scoreTap', 'pop', 'tab'))
            jm = D.get('jim') or {}
            T(E + '1차객 첫 화면 틈 0(첫 요소 왼쪽 = 서랍 끝 · 위 = .body2 위)', jm.get('first') and abs(jm['first']['rect']['x'] - jm['jt']['r']) < 0.6 and abs(jm['first']['rect']['y'] - jm['body2']['y']) < 0.6,
              [jm.get('first'), jm.get('jt'), jm.get('body2')])
            T(E + 'JS 오류 0(ResizeObserver loop 알림·자원 404 줄은 뺌)', not [x for x in (D.get('errs') or []) if not NOISE(x)], D.get('errs'))
    p = sum(1 for x in L if x.startswith('PASS')); f = sum(1 for x in L if x.startswith('FAIL'))
    body = '\n'.join(L) + '\n\n합계  PASS %d · FAIL %d  (%.0f초)\n' % (p, f, RES.get('sec', 0))
    print(body)
    wr(os.path.join(OUT, '_harness_jo_hrail_list_result.txt'), body)
    # 캡처 — N: 에는 한 장씩(되읽어 대조)
    for eng in ('chromium',):
        W0 = RES.get('wide/%s/NEW' % eng) or {}
        for k, v in (W0.get('w') or {}).items():
            if v.get('shot'):
                wv, _, t = k.split('|')
                wr(os.path.join(SHOTS, 'w%s_%s.png' % (wv, t)), open(v['shot'], 'rb').read())


if __name__ == '__main__':
    main()
