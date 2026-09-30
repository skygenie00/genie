# -*- coding: utf-8 -*-
"""민법OX 기출뷰 = 시험지 — _task_ox_exview_paper §G(G0~G11).

  NEW  = --app 파일(패치 결과 · 기본 = genie 작업트리 minbeop/index.html)
  BASE = genie HEAD 의 같은 파일이 아니라 **지시서 바탕 blob**(md5 e5ca92e8) — 헛잣대(G11 · G3~G9 가 FAIL 이어야)
  데이터 = 새 마스터(ed1cd1d7)로 구운 문항 JSON·기출키·딱지(--data 폴더) · 기록 = studyplandata origin/main 기록.json ·
           시험지 = genie gichul/pdf 19장 · 엑셀 = 마스터 사본(G1 의 앱 「엑셀 적용」 길)
  엔진 = playwright chromium — 책상(마우스 · 1280×900) · 아이패드(1024×768 · has_touch · CDP 터치 반지름 22)
  누름 = 진짜 포인터만(page.mouse.click / Input.dispatchTouchEvent) · el.click() 없음 · 보임 = computed display + 높이
  網 = 같은 출처 + cdn.tailwindcss.com · GitHub API 는 SEED 가 대답(기출키·딱지·문항 = 파일 · 기록 = 흉내 원격 · PUT 은 받아 적기만)

쓰기 : python _harness_ox_exview_paper.py [--app 파일] [--data 폴더] [--only new|base|ipad]
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
_NR = _roots.need_n('민법 OMR 마스터 엑셀 · minbeop/script')   # env_lanes_fix(9/29) — N: 작업 폴더 · 없으면(클라우드) 「N: 필요 — 클라우드 불가(…)」 종료 코드 3
import hashlib, http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
GENIE = _roots.genie()
SPD = _roots.spd()
MASTER = os.path.join(_NR, 'minbeop', 'OXminbub_OMR_2026111111.xlsx')
SCRIPT = os.path.join(_NR, 'minbeop', 'script')
WORK = os.path.join(tempfile.gettempdir(), 'h_exview')
VENDOR0 = os.path.join(tempfile.gettempdir(), 'h_gichul', 'vendor')
CDN = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/'
BASE_MD5 = 'e5ca92e8024cd8f3c20ab974cdfa5180'
BASE_REV = '33be370'
TESTS = io.open(os.path.join(HERE, '_harness_ox_exview_paper_tests.js'), encoding='utf-8').read()
TESTS += '\n' + io.open(os.path.join(HERE, '_harness_ox_exview_paper_add1_tests.js'), encoding='utf-8').read()   # add1(9/27) __HZA
TESTS += '\n' + io.open(os.path.join(HERE, '_harness_ox_exview_paper_add2_tests.js'), encoding='utf-8').read()   # add2(9/27) __HZB
TESTS += '\n' + io.open(os.path.join(HERE, '_harness_ox_exview_paper_add3_tests.js'), encoding='utf-8').read()   # add3(9/27) __HZC
TESTS += '\n' + io.open(os.path.join(HERE, '_harness_ox_linkwin_tests.js'), encoding='utf-8').read()   # _task_ox_linkwin(9/27) __HZL
RESULT = os.path.join(HERE, '_harness_ox_exview_paper_result.txt')
if '--result' in sys.argv:   # add2(9/27) — 결과를 딴 자리로(본판·add1 결과 파일을 통째로 덮지 않게 · 나중에 이어 붙인다)
    RESULT = sys.argv[sys.argv.index('--result') + 1]
IPAD_UA = ('Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 '
           '(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
ANS26 = ('1:3 2:2 3:2 4:4 5:3 6:4 7:5 8:1 9:2 10:2 11:2 12:1 13:2 14:3 15:3 16:3 17:4 18:3 19:5 20:5 21:4 22:1 23:1 24:2 25:4 '
         '26:5 27:4 28:5 29:3 30:1 31:2 32:5 33:4 34:5 35:4 36:3 37:4 38:1 39:3 40:1')
GOLD26 = {1: 'ㄱ | ㄷ | ㄱ, ㄴ | ㄴ, ㄷ | ㄱ, ㄴ, ㄷ', 7: 'ㄱ, ㄴ | ㄱ, ㄷ | ㄱ, ㄴ, ㄹ | ㄴ, ㄷ, ㄹ | ㄱ, ㄴ, ㄷ, ㄹ',
          11: 'ㄱ, ㄴ | ㄴ, ㄷ | ㄷ, ㄹ | ㄱ, ㄷ, ㄹ | ㄴ, ㄷ, ㄹ', 15: 'ㄱ | ㄷ | ㄱ, ㄴ | ㄴ, ㄷ | ㄱ, ㄴ, ㄷ',
          24: 'ㄱ | ㄱ, ㄴ | ㄱ, ㄷ | ㄴ, ㄷ | ㄱ, ㄴ, ㄷ', 34: 'ㄴ | ㄱ, ㄴ | ㄱ, ㄷ | ㄴ, ㄷ | ㄱ, ㄴ, ㄷ',
          36: 'ㄴ | ㄷ | ㄱ, ㄴ | ㄱ, ㄷ | ㄱ, ㄴ, ㄷ'}


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


APP = ARG('--app', os.path.join(GENIE, 'minbeop', 'index.html'))
DATA = ARG('--data')
ONLY = ARG('--only')
OUTL = []
G = []


def say(*a):
    s = ' '.join(str(x) for x in a)
    print(s)
    OUTL.append(s)


def add(g, ok, msg):
    G.append((g, bool(ok), msg))
    say('  %s %-4s %s' % ('PASS' if ok else 'FAIL', g, msg))


def J(s):
    try:
        return json.loads(s) if isinstance(s, str) else s
    except Exception:
        return {'__raw': str(s)[:300]}


def md5b(b):
    return hashlib.md5(b).hexdigest()


def git(*a, repo=GENIE):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


# ══════════════════════════ 섬기기 ══════════════════════════
SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__ALERTS=[];window.alert=function(m){__ALERTS.push(String(m));};
window.confirm=function(){return true;};window.prompt=function(){return null;};
(function(){   /* revfix0928(9/28) — 기기 시계 옮김(__hzday = +ms · Date 만) · 오프라인(__hzoff = navigator.onLine false) · 표지가 없으면 옛 그대로 */
  var OFF=+(sessionStorage.getItem('__hzday')||0)||0;
  if(OFF){var _D=Date;var D2=function(){if(!(this instanceof D2))return new _D(_D.now()+OFF).toString();
      if(!arguments.length)return new _D(_D.now()+OFF);var a=[null];for(var i=0;i<arguments.length;i++)a.push(arguments[i]);return new (Function.prototype.bind.apply(_D,a))();};
    D2.now=function(){return _D.now()+OFF;};D2.parse=_D.parse;D2.UTC=_D.UTC;D2.prototype=_D.prototype;window.Date=D2;}
  if(sessionStorage.getItem('__hzoff')==='1'){try{Object.defineProperty(Navigator.prototype,'onLine',{get:function(){return false;},configurable:true});}catch(e){}}
})();
(function(){
  var real=window.fetch.bind(window);
  var GH=/^https:\/\/api\.github\.com\/repos\/([^/]+)\/([^/]+)\/contents\/([^?]+)/;
  window.__NET=[];window.__PUTS=[];window.__REMOTE_REC=null;window.__GKEY404=false;try{window.__REMOTE_REC=JSON.parse(sessionStorage.getItem('__hzrem')||'null');}catch(e){}var DLY=+(sessionStorage.getItem('__hzdelay')||0)||0;   /* add2(9/27) — 원격 기록 흉내·기록.json GET 늦춤(sessionStorage · 없으면 옛 그대로) */
  var R=function(b,s){return Promise.resolve(new Response(b,{status:s||200,headers:{'Content-Type':'application/json'}}));};
  window.fetch=function(u,o){
    o=o||{};var s=String((u&&u.url)||u||'');var m=GH.exec(s);
    if(m){
      var path=decodeURIComponent(m[3]),meth=String(o.method||'GET').toUpperCase(),h=o.headers||{},acc=String(h.Accept||h.accept||'');
      window.__NET.push(meth+' gh:'+path);
      if(path==='minbeop/기록.json'){
        if(meth==='PUT'){window.__PUTS.push(o.body);return R(JSON.stringify({content:{sha:'H'+(window.__PUTS.length+1)}}));}
        var G=function(){if(sessionStorage.getItem('__hz500')==='1')return R('{"message":"harness 500"}',500);   /* revfix0928(9/28) — 받기 실패 흉내 */
          if(!window.__REMOTE_REC)return R('{"message":"Not Found"}',404);if(/raw/.test(acc))return R(JSON.stringify(window.__REMOTE_REC));return R(JSON.stringify({sha:'H1'}));};
        return DLY>0?new Promise(function(res){setTimeout(function(){res(G());},DLY);}):G();
      }
      if(path==='minbeop/기출키.json')return window.__GKEY404?R('{"message":"Not Found"}',404):real('/data/gkey.json',{cache:'no-store'});
      if(path==='minbeop/문항메타.json')return real('/data/meta.json',{cache:'no-store'});
      if(path==='minbeop/문항마스터.json')return real('/data/master.json',{cache:'no-store'});
      return R('{"message":"Not Found"}',404);
    }
    if(/^https?:\/\//.test(s)&&s.indexOf(location.origin)!==0){window.__NET.push('BLOCK:'+s.slice(0,90));return Promise.reject(new Error('harness blocked'));}
    return real(u,o);
  };
})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
if(!sessionStorage.getItem('__hzkeep'))localStorage.clear();   /* add1 새로고침 흉내 — 표지가 있으면 기록을 안 지운다 */
</script>"""


class H(http.server.SimpleHTTPRequestHandler):
    MAP = {}

    def log_message(self, *a):
        pass

    def translate_path(self, path):
        p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
        if p in H.MAP:
            return H.MAP[p]
        if p.startswith('/minbeop/h_'):
            return os.path.join(WORK, os.path.basename(p))
        if p.startswith('/vendor/'):
            f = os.path.join(WORK, 'vendor', *p[len('/vendor/'):].split('/'))
            if not os.path.exists(f):
                try:   # cmaps·standard_fonts 는 처음 부를 때 CDN 에서 한 번 받아 둔다(브라우저는 CDN 에 못 나간다)
                    os.makedirs(os.path.dirname(f), exist_ok=True)
                    with urllib.request.urlopen(CDN + p[len('/vendor/'):], timeout=60) as r:
                        open(f, 'wb').write(r.read())
                except Exception:
                    pass
            return f
        if p.startswith('/gichul/'):
            return os.path.join(GENIE, *p.strip('/').split('/'))
        return os.path.join(WORK, '__none__')


def serve():
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


def build(tag, src):
    html = src
    for n in ('pdf.min.js', 'pdf.worker.min.js'):
        html = html.replace(CDN + n, '/vendor/' + n)
    html = html.replace(CDN + 'cmaps/', '/vendor/cmaps/').replace(CDN + 'standard_fonts/', '/vendor/standard_fonts/')
    b = html.index('<body'); bb = html.index('>', b) + 1
    html = html[:bb] + SEED + html[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + TESTS + '\n</script>\n' + html[e:]
    name = 'h_%s.html' % tag
    io.open(os.path.join(WORK, name), 'w', encoding='utf-8', newline='\n').write(html)
    return '/minbeop/' + name


def route_filter(route):
    u = route.request.url
    if u.startswith('http://127.0.0.1') or u.startswith('https://cdn.tailwindcss.com'):
        return route.continue_()
    return route.abort()


class S:
    """한 판 — 누름은 진짜 포인터만. 누르기 전에 그 자리 맨 위가 그 요소인지(hit) 본다."""

    def __init__(self, pg, touch):
        self.pg, self.touch = pg, touch
        self.cdp = pg.context.new_cdp_session(pg) if touch else None
        self.miss = []

    def js(self, expr, arg=None):
        try:
            return J(self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr))
        except Exception as e:   # 바탕 판에는 없는 함수가 있다 — 판을 멈추지 말고 적어 둔다(FAIL 로 끝난다)
            self.miss.append(('js', expr[:60], str(e)[:160]))
            return {'__err': str(e)[:200]}

    def tap(self, x, y):
        tp = {'x': x, 'y': y, 'radiusX': 22, 'radiusY': 22, 'force': 1, 'id': 1}
        self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [tp]})
        self.pg.wait_for_timeout(70)
        self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})

    def press(self, sel, i=0, no_scroll=False, wait=160):
        p = self.js("([s,i,n])=>__HZX.pt(s,i,n)", [sel, i, no_scroll])
        ok = bool(p and p.get('on') and p.get('hit'))
        if ok:
            if self.touch:
                self.tap(p['cx'], p['cy'])
            else:
                self.pg.mouse.click(p['cx'], p['cy'])
            self.pg.wait_for_timeout(wait)
        else:
            self.miss.append((sel, i, p))
        return ok

    def at(self, p, wait=160):
        if not (p and p.get('on') and p.get('hit')):
            self.miss.append(('pt', p))
            return False
        if self.touch:
            self.tap(p['cx'], p['cy'])
        else:
            self.pg.mouse.click(p['cx'], p['cy'])
        self.pg.wait_for_timeout(wait)
        return True


def open_page(br, tag, src, touch):
    url = build(tag, src)
    if touch:
        ctx = br.new_context(viewport={'width': 1024, 'height': 768}, device_scale_factor=1, is_mobile=True, has_touch=True, user_agent=IPAD_UA)
    else:
        ctx = br.new_context(viewport={'width': 1280, 'height': 900}, device_scale_factor=1)
    ctx.route('**/*', route_filter)
    pg = ctx.new_page()
    pg.set_default_timeout(600000)
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
    pg.goto('http://127.0.0.1:%d%s' % (PORT, url), wait_until='load', timeout=180000)
    pg.wait_for_function("typeof buildQuizData==='function'&&!!window.__HZX", timeout=180000)
    return S(pg, touch), ctx, errs


# ══════════════════════════ 한 판 돌리기 ══════════════════════════
def run_desktop(br, tag, src):
    s, ctx, errs = open_page(br, tag, src, False)
    R = {'errs': errs}
    W = s.pg.wait_for_timeout
    R['setup'] = s.js("__HZX.setup()")
    U = R['setup'].get('U') or {}
    # G10 — 상태를 바꾸기 전에 단원 풀기 첫 쪽 셋 · 일반 OMR 창
    s.js("__HZX.home()")
    labs = s.js("__HZX.unitLabels()")
    R['unitLabels'] = labs
    R['unit'] = [s.js("([a,b])=>__HZX.unitText(a,b)", [a, b]) for a, b in labs]
    # G1 · G2
    R['g1'] = s.js("__HZX.g1()")
    R['labels'] = s.js("__HZX.labels()")
    R['g2'] = s.js("__HZX.g2()")
    R['g2map'] = s.js("__HZX.g2map()")
    # G8 첫 화면 — 흉내 회독(시험지 32/40 · 72분 · 지문 🌀3 ⚠2 X12) · 진행중
    s.js("__HZX.home()")
    R['g8'] = s.js("__HZX.g8()")
    s.js("([n,t])=>__HZX.progSet(n,t)", [5, 23 * 60 + 20])
    R['g8prog'] = s.js("__HZX.g8()")
    s.js("__HZX.progClear()")
    # G3 — 17년 × 첫 쪽
    R['g3'] = []
    for y in [str(x) for x in range(2010, 2027)]:
        R['g3'].append({'open': s.js("y=>__HZX.open(y)", y), 'm': s.js("y=>__HZX.g3(y)", y)})
    # 기출뷰 진입 — 첫 화면 2026 줄의 시작 단추를 진짜로 누른다
    s.js("__HZX.home()")
    R['enter'] = s.press('[data-trrow*="2026년"] button[onclick^="startQuiz"]')
    s.pg.wait_for_function("document.querySelectorAll('#quiz-container .question-box').length>0", timeout=30000)
    W(400)
    if R['setup'].get('has'):
        s.pg.wait_for_function("!document.querySelector('#quiz-container .exv-wait')", timeout=60000)
    R['g3_26'] = s.js("y=>__HZX.g3(y)", '2026')
    # G4 — 1번 조합 ③ · 2번 ② · 3번 ① (진짜 마우스)
    R['p1'] = s.press('#quiz-container .exv-opt[data-exk="2026:1"][data-exn="3"]')
    R['p2'] = s.press('#quiz-container .exv-lab[data-exk="2026:2"][data-exn="2"]')
    R['p3'] = s.press('#quiz-container .exv-lab[data-exk="2026:3"][data-exn="1"]')
    R['st_a'] = s.js("__HZX.st4()")
    # OMR — 4·5 안 고른 채 채점 → 토스트 · 옅은 빨강 · 채점 안 함
    R['omr1'] = s.press('button[onclick="openOmrPad()"]')
    W(300)
    R['omrA'] = s.js("__HZX.omrState()")
    R['omrG0'] = s.press('#oxwin-omr .exv-omr-foot button')
    W(300)
    R['st_b'] = s.js("__HZX.st4()")
    # 다시 OMR — 4번 ④ · 5번 ② → 채점 ✓
    s.press('button[onclick="openOmrPad()"]')
    W(300)
    R['o4'] = s.press('#exv-omr-rows .exv-omr[data-no="4"] button[data-n="4"]')
    R['o5'] = s.press('#exv-omr-rows .exv-omr[data-no="5"] button[data-n="2"]')
    R['omrB'] = s.js("__HZX.omrState()")
    R['omrG'] = s.press('#oxwin-omr .exv-omr-foot button')
    W(400)
    R['st_c'] = s.js("__HZX.st4()")
    # 채점 뒤 번호 안 바뀜 — 2번 ① 을 눌러 본다
    R['p2b'] = s.press('#quiz-container .exv-lab[data-exk="2026:2"][data-exn="1"]')
    R['st_d'] = s.js("__HZX.st4()")
    # G5 즉시 기록 — 1번 ㄱ O · ㄴ X · ㄷ 🌀
    if U.get('a'):
        R['g5a'] = s.press('#ox-O-%s' % U['a'])
        R['g5b'] = s.press('#ox-X-%s' % U['b'])
        R['g5c'] = s.press('#tag-confuse-%s' % U['c'])
        W(300)
        R['st5'] = s.js("u=>__HZX.st5(u)", U)
    # 알약 — 다음 5문제 ▶ 일곱 번(진짜 클릭) → 마지막 쪽 「전체 채점 ✓」
    s.js("([a,b])=>__HZX.pickFill(a,b)", [6, 35])
    R['pill'] = []
    for i in range(7):
        st = s.js("__HZX.st4()")
        ok = s.press('#action-btn', 0, True, 500)
        s.js("__HZX.settle()")
        R['pill'].append({'before': (st.get('pill') or {}).get('txt'), 'page': st.get('page'), 'ok': ok})
    R['last'] = s.js("__HZX.st4()")
    R['q36'] = s.js("__HZX.q36()")
    # 마지막 쪽 36~40 도 진짜로 고른다(36 = 조합 ③)
    R['p36'] = s.press('#quiz-container .exv-opt[data-exk="2026:36"][data-exn="3"]')
    for no, k in ((37, 4), (38, 1), (39, 3), (40, 2)):
        R['p%d' % no] = s.press('#quiz-container .exv-lab[data-exk="2026:%d"][data-exn="%d"]' % (no, k))
    R['last2'] = s.js("__HZX.st4()")
    R['gradeAll'] = s.press('#action-btn', 0, True, 600)
    R['after'] = s.js("__HZX.st4()")
    # G6 — 카드 기록 칸(ㄴ · 이번 칸) → 누름 → 출처 → × 한 번 → × 두 번
    s.js("()=>{currentPageIndex=0;renderQuizPage();return 1}")
    W(400)
    if U.get('b'):
        R['g6open'] = s.press('#q-box-%s button[onclick^="recStripToggle"]' % U['b'])
        R['g6s0'] = s.js("u=>__HZX.st6(u)", U['b'])
        R['g6cell'] = s.press('#rec-strip-%s .rec-cell[data-kind="cur"]' % U['b'])
        R['g6s1'] = s.js("u=>__HZX.st6(u)", U['b'])
        R['g6x1'] = s.press('#rec-strip-%s .rec-del' % U['b'])
        R['g6s2'] = s.js("u=>__HZX.st6(u)", U['b'])
        R['g6x2'] = s.press('#rec-strip-%s .rec-del' % U['b'])
        W(300)
        R['g6s3'] = s.js("u=>__HZX.st6(u)", U['b'])
        # 지운 뒤 같은 날 다시 풀기 → 동기화 쓸기가 새 답을 먹지 않는다
        R['g6re'] = s.press('#ox-X-%s' % U['b'])
        R['g6re2'] = s.js("u=>__HZX.reanswerSweep(u)", U['b'])
    # G9 · G6 정리 창 — 첫 화면 📋(진짜 클릭)
    s.js("__HZX.home()")
    R['jn1btn'] = s.js("([a,b])=>__HZX.jnBtn(a,b)", ['민법총칙', '1.2'])
    R['jn1'] = s.at(R['jn1btn'], 600)
    R['g9a'] = s.js("y=>__HZX.g9(y)", '')
    s.js("()=>{document.querySelectorAll('.oxwin').forEach(w=>w.remove());return 1}")
    R['jn2btn'] = s.js("([a,b])=>__HZX.jnBtn(a,b)", ['변리사 기출', '2026년'])
    R['jn2'] = s.at(R['jn2btn'], 800)
    R['g9b'] = s.js("y=>__HZX.g9(y)", '2026')
    R['jx'] = s.press('.jx-no[data-jxno="1"] .jx-cell')
    R['jxInfo'] = s.js("__HZX.jxInfo()")
    if U.get('h'):
        R['g6j0'] = s.js("u=>__HZX.st6(u)", U['h'])
        R['g6jc'] = s.press('[data-jnrow="%s"] .rec-cell[data-kind="hist"]' % U['h'])
        R['g6j1'] = s.js("u=>__HZX.st6(u)", U['h'])
        R['g6jx1'] = s.press('[data-jnrec="%s"] .rec-del' % U['h'])
        R['g6jx2'] = s.press('[data-jnrec="%s"] .rec-del' % U['h'])
        W(300)
        R['g6j2'] = s.js("u=>__HZX.st6(u)", U['h'])
        k26 = R['setup'].get('k26')
        R['revive'] = s.js("([u,k,n,t])=>__HZX.revive(u,k,n,t)", [U['h'], k26, 1, True])
        R['revive0'] = s.js("([u,k,n,t])=>__HZX.revive(u,k,n,t)", [U['h'], k26, 1, False])
        s.js("()=>{try{recTombSweep()}catch(e){}return 1}")
    R['ver'] = s.js("__HZX.ver()")
    # G7 시계 — 2026 기출뷰 · 📝 · ▶ 3초 · ❚❚ · ↺ 두 번 · 흉내 12:34 · 73:05 · 닫고 다시
    s.js("y=>__HZX.open(y)", '2026')
    s.press('button[onclick="openOmrPad()"]')
    W(300)
    R['t0'] = s.js("__HZX.st7()")
    R['tgo'] = s.press('#exv-timer .exv-t-go')
    s.js("__HZX.markGo()")
    W(3300)
    R['trun'] = s.js("__HZX.st7()")
    R['tstop'] = s.press('#exv-timer .exv-t-go')
    R['t1'] = s.js("__HZX.st7()")
    R['tr1'] = s.press('#exv-t-reset')
    W(1500)   # 첫 누름 뒤 1.5초 — 초마다 다시 그리던 판은 여기서 「한 번 더」가 풀렸다
    R['t2'] = s.js("__HZX.st7()")
    R['tr2'] = s.press('#exv-t-reset')
    R['t3'] = s.js("__HZX.st7()")
    s.js("n=>__HZX.timerSet(n)", 12 * 60 + 34)
    R['t4'] = s.js("__HZX.st7()")
    s.js("n=>__HZX.timerSet(n)", 73 * 60 + 5)
    R['t5'] = s.js("__HZX.st7()")
    R['tclose'] = s.press('#oxwin-omr .oxwin-head > button')
    W(200)
    R['treopen'] = s.press('button[onclick="openOmrPad()"]')
    W(300)
    R['t6'] = s.js("__HZX.st7()")
    R['err'] = s.js("__HZX.err()")
    R['miss'] = s.miss
    ctx.close()
    return R


def run_ipad(br, tag, src):
    s, ctx, errs = open_page(br, tag, src, True)
    R = {'errs': errs}
    W = s.pg.wait_for_timeout
    R['setup'] = s.js("__HZX.setup()")
    U = R['setup'].get('U') or {}
    s.js("__HZX.home()")
    R['enter'] = s.press('[data-trrow*="2026년"] button[onclick^="startQuiz"]')
    s.pg.wait_for_function("document.querySelectorAll('#quiz-container .question-box').length>0", timeout=30000)
    W(400)
    if R['setup'].get('has'):
        s.pg.wait_for_function("!document.querySelector('#quiz-container .exv-wait')", timeout=60000)
    R['p1'] = s.press('#quiz-container .exv-opt[data-exk="2026:1"][data-exn="3"]')
    R['p2'] = s.press('#quiz-container .exv-lab[data-exk="2026:2"][data-exn="2"]')
    R['p3'] = s.press('#quiz-container .exv-lab[data-exk="2026:3"][data-exn="1"]')
    R['st_a'] = s.js("__HZX.st4()")
    s.press('button[onclick="openOmrPad()"]')
    W(300)
    R['o4'] = s.press('#exv-omr-rows .exv-omr[data-no="4"] button[data-n="4"]')
    R['o5'] = s.press('#exv-omr-rows .exv-omr[data-no="5"] button[data-n="2"]')
    R['tgo'] = s.press('#exv-timer .exv-t-go')
    W(2200)
    R['tstop'] = s.press('#exv-timer .exv-t-go')
    R['t1'] = s.js("__HZX.st7()")
    R['omrG'] = s.press('#oxwin-omr .exv-omr-foot button')
    W(400)
    R['st_c'] = s.js("__HZX.st4()")
    if U.get('a'):
        R['g5a'] = s.press('#ox-O-%s' % U['a'])
        R['g5b'] = s.press('#ox-X-%s' % U['b'])
        R['g5c'] = s.press('#tag-confuse-%s' % U['c'])
        W(300)
        R['st5'] = s.js("u=>__HZX.st5(u)", U)
        R['g6open'] = s.press('#q-box-%s button[onclick^="recStripToggle"]' % U['b'])
        R['g6cell'] = s.press('#rec-strip-%s .rec-cell[data-kind="cur"]' % U['b'])
        R['g6s1'] = s.js("u=>__HZX.st6(u)", U['b'])
        R['g6x1'] = s.press('#rec-strip-%s .rec-del' % U['b'])
        R['g6x2'] = s.press('#rec-strip-%s .rec-del' % U['b'])
        W(300)
        R['g6s3'] = s.js("u=>__HZX.st6(u)", U['b'])
    s.js("([a,b])=>__HZX.pickFill(a,b)", [6, 40])
    st = s.js("__HZX.st4()")
    R['pill0'] = (st.get('pill') or {}).get('txt')
    R['pillTap'] = s.press('#action-btn', 0, True, 600)
    s.js("__HZX.settle()")
    R['pill1'] = s.js("__HZX.st4()")
    R['err'] = s.js("__HZX.err()")
    R['miss'] = s.miss
    ctx.close()
    return R


# ══════════════════════════ 판정 ══════════════════════════
def gates_paper(R, tag, strict=True):
    """G3~G9 — 판(NEW · BASE) 하나의 결과를 게이트별로 가른다. 돌려주는 값 = {게이트: [(ok, 글)]}."""
    out = {}

    def a(g, ok, msg):
        out.setdefault(g, []).append((bool(ok), msg))

    st = R.get('setup') or {}
    # G3
    g3 = R.get('g3') or []
    bad = []
    for x in g3:
        m = x.get('m') or {}
        y = m.get('y')
        ok = (m.get('q') == 5 and m.get('heads') == 5 and m.get('stems') == 5 and m.get('bogi') == m.get('combo')
              and m.get('postN', 0) > 0 and m.get('postVis') == 0 and m.get('oxVis') == 0 and m.get('chipRowVis') == m.get('boxes') and m.get('boxes', 0) > 0
              and all(v == 5 for v in (m.get('sel') or [])))
        if not ok:
            bad.append('%s q%s 발문%s 보기%s/조합%s 풀기줄보임%s/%s 칩줄%s/%s 조합선지%s' % (y, m.get('q'), m.get('stems'), m.get('bogi'), m.get('combo'),
                                                                       m.get('oxVis'), m.get('oxRows'), m.get('chipRowVis'), m.get('boxes'), m.get('sel')))
    a('G3', len(g3) == 17 and not bad, '17년 첫 쪽 — 문항 5 · 발문 줄 5 · 보기 상자 = 조합형 수 · 조합 선지 다섯 · 채점 전 O·X 줄 computed 숨김 · 칩 줄 보임 %s'
      % ('모두 맞음' if not bad else '어긋남 %d: %s' % (len(bad), bad[:4])))
    miss = {(x.get('m') or {}).get('y'): (x.get('m') or {}).get('miss') for x in g3}
    a('G3', True, '빠진 선지 자리(첫 쪽) %s' % {k: v for k, v in miss.items() if v})
    q36 = R.get('q36') or {}
    a('G3', q36.get('bogi') == 1 and q36.get('miss') == 0 and ' | '.join(q36.get('opts') or []) == '①ㄴ | ②ㄷ | ③ㄱ, ㄴ | ④ㄱ, ㄷ | ⑤ㄱ, ㄴ, ㄷ',
      '2026 36번 — 보기 상자 %s · 조합 선지 %s · 빈자리 %s' % (q36.get('bogi'), q36.get('opts'), q36.get('miss')))
    ct = (R.get('g3_26') or {}).get('comboChipTxt') or []
    a('G3', ct[:3] == ['2026:1:ㄱ', '2026:1:ㄴ', '2026:1:ㄷ'], '조합형 칩 글자(기출뷰 안) %s' % ct)
    # G4
    pk = (R.get('st_a') or {}).get('picks') or {}
    a('G4', R.get('p1') and R.get('p2') and R.get('p3') and pk == {'2026:1': 3, '2026:2': 2, '2026:3': 1},
      '진짜 마우스로 1번 조합 ③ · 2번 ② · 3번 ① → 고른 답 %s' % pk)
    sb = R.get('st_b') or {}
    a('G4', (sb.get('toast') or {}).get('txt') == '답을 안 고른 문제가 있습니다 — 4번, 5번' and sb.get('need') == ['2026:4', '2026:5'] and not any((sb.get('res') or {}).values()),
      'OMR 채점(4·5 안 고름) → 토스트 %s · 옅은 빨강 %s · 결과 글자 %s' % ((sb.get('toast') or {}).get('txt'), sb.get('need'), [v for v in (sb.get('res') or {}).values() if v]))
    oa = R.get('omrA') or {}
    a('G4', oa.get('rows') == 40 and oa.get('btn5') == 5 and oa.get('cur') == [1, 2, 3, 4, 5] and oa.get('on') == ['1:3', '2:2', '3:1'],
      'OMR 창 = 문번 %s × %s · 이 쪽 행 %s · 본문 고른 것 = OMR %s · 제목 「%s」' % (oa.get('rows'), oa.get('btn5'), oa.get('cur'), oa.get('on'), oa.get('title')))
    sc = R.get('st_c') or {}
    want = {'2026:1': 'O 맞음', '2026:2': 'O 맞음', '2026:3': 'X 틀림 · 정답 ②', '2026:4': 'O 맞음', '2026:5': 'X 틀림 · 정답 ③'}
    a('G4', R.get('o4') and R.get('o5') and sc.get('res') == want, 'OMR 4번 ④ · 5번 ② → 채점 ✓ → 발문 줄 %s' % sc.get('res'))
    a('G4', sc.get('sel') == {'2026:1': [3], '2026:2': [2], '2026:3': ['1x'], '2026:4': [4], '2026:5': ['2x']} and sc.get('ok') == {'2026:1': [3], '2026:2': [2], '2026:3': [2], '2026:4': [4], '2026:5': [3]},
      '고른 번호 파랑(틀리면 빨강 x) %s · 정답 테 %s' % (sc.get('sel'), sc.get('ok')))
    sd = R.get('st_d') or {}
    a('G4', (sd.get('picks') or {}).get('2026:2') == 2 and (sd.get('sel') or {}).get('2026:2') == [2], '채점 뒤 2번 ① 누름(누름 %s) → 고른 답 그대로 %s' % (R.get('p2b'), (sd.get('picks') or {}).get('2026:2')))
    pl = R.get('pill') or []
    want_p = ['다음 5문제 ▶'] * 7
    a('G4', [x.get('before') for x in pl] == want_p and [x.get('page') for x in pl] == list(range(7)) and all(x.get('ok') for x in pl),
      '알약 「다음 5문제 ▶」 진짜 클릭 7번 %s · 쪽 %s' % ([x.get('before') for x in pl][:2], [x.get('page') for x in pl]))
    la = R.get('last2') or {}
    a('G4', (la.get('pill') or {}).get('txt') == '전체 채점 ✓' and la.get('page') == 7, '마지막 쪽 알약 %s · 쪽 %s' % ((la.get('pill') or {}).get('txt'), la.get('page')))
    af = R.get('after') or {}
    a('G4', R.get('gradeAll') and af.get('rounds') == 2 and not af.get('picks') and (af.get('timer') in (None, {'acc': 0, 'since': 0})) and ((af.get('toast') or {}).get('txt') or '').startswith('전체 채점 — '),
      '「전체 채점 ✓」 진짜 클릭 → 회독 %s(흉내 1 + 이번 1) · 그 해 고른 답 %d · 시계 %s · 토스트 「%s」 · 회독 %s' % (af.get('rounds'), len(af.get('picks') or {}), af.get('timer'), (af.get('toast') or {}).get('txt'),
                                                                                              {k: v for k, v in (af.get('lastRound') or {}).items() if k != 'picks'}))
    # G5
    s5 = R.get('st5') or {}
    a('G5', R.get('g5a') and R.get('g5b') and R.get('g5c') and s5.get('qh') == [True, False, None] and s5.get('tagC') is True and s5.get('weak') == [False, True, True]
      and s5.get('sm') == [True, False, None] and s5.get('prog') == [True, False, None],
      '1번 ㄱ O · ㄴ X · ㄷ 🌀 → ox_q_history %s · 🌀 %s · 약점 큐 %s · 세션 %s · 진행중 %s · 딱지 %s' % (s5.get('qh'), s5.get('tagC'), s5.get('weak'), s5.get('sm'), s5.get('prog'), s5.get('badge')))
    # G6 카드
    s1, s2, s3 = R.get('g6s1') or {}, R.get('g6s2') or {}, R.get('g6s3') or {}
    inf = s1.get('info') or {}
    a('G6', R.get('g6open') and R.get('g6cell') and inf.get('vis') and inf.get('del') and '이번' not in (inf.get('txt') or '') and '이번' not in (s1.get('strip') or '') and inf.get('fs') == '11px',
      '카드 칸 누름 → 출처 computed 보임 「%s」 · × 있음 · 「이번」 없음 · 11px %s' % (inf.get('txt'), inf.get('fs')))
    a('G6', R.get('g6x1') and (s2.get('info') or {}).get('sure') and s2.get('cells') == s1.get('cells') and s2.get('qh') is False,
      '× 한 번 = 빨강 %s · 칸 그대로 %s · 지금 결과 %s' % ((s2.get('info') or {}).get('sure'), s2.get('cells'), s2.get('qh')))
    a('G6', R.get('g6x2') and s3.get('cells') in ([], None) and s3.get('qh') is None and s3.get('weak') is False and len(s3.get('gone') or []) == 1 and s3.get('radios') == ['e', 'e'],
      '× 두 번 = 지움 → 칸 %s · ox_q_history %s · 약점 %s · 묘비 %s · 라디오 %s' % (s3.get('cells'), s3.get('qh'), s3.get('weak'), s3.get('gone'), s3.get('radios')))
    re2 = R.get('g6re2') or {}
    a('G6', R.get('g6re') and re2.get('naive') == 1 and re2.get('kept') is True and re2.get('sm') is False,
      '지운 뒤 같은 날 다시 푼 답 — 동기화 쓸기 뒤에도 남음 %s(묘비만 보면 먹혔을 칸 %s)' % (re2.get('kept'), re2.get('naive')))
    j0, j1, j2 = R.get('g6j0') or {}, R.get('g6j1') or {}, R.get('g6j2') or {}
    ji = j1.get('jinfo') or {}
    a('G6', R.get('g6jc') and ji.get('vis') and ji.get('left') is True and '이번' not in (ji.get('txt') or '') and '마지막' not in (ji.get('txt') or ''),
      '정리 창 칸 누름 → 출처 칸 묶음 왼쪽 %s 「%s」' % (ji.get('left'), ji.get('txt')))
    a('G6', R.get('g6jx1') and R.get('g6jx2') and j0.get('qh') is False and j0.get('weak') is True and j2.get('qh') is None and j2.get('weak') is False and len(j2.get('gone') or []) == 1
      and all('hist' not in c for c in (j2.get('jn') or [''])),
      '정리 창 × 두 번 → 전 %s/약점 %s → 후 %s/약점 %s · 묘비 %s · 그 행 칸 %s' % (j0.get('qh'), j0.get('weak'), j2.get('qh'), j2.get('weak'), j2.get('gone'), j2.get('jn')))
    rv, rv0 = R.get('revive') or {}, R.get('revive0') or {}
    a('G6', rv.get('back') is False and rv.get('putHas') is False and rv.get('puts', 0) >= 1 and rv0.get('back') is True,
      '되살림 흉내(원격이 지운 칸을 더 새 도장으로) → syncRecords 뒤 %s · 올린 것에 %s · 헛잣대(묘비 뺌) 되살아남 %s' % ('다시 지워짐' if rv.get('back') is False else '살아남음', rv.get('putHas'), rv0.get('back')))
    sk = ((R.get('ver') or {}).get('sync')) or []
    a('G6', all(k in sk for k in ('ox_rec_gone', 'ox_exam_rounds', 'ox_exam_pick')) and 'ox_exam_timer' not in sk, 'SYNC_KEYS 새 키 %s · 시계 키 없음 %s' % ([k for k in sk if k.startswith(('ox_rec', 'ox_exam'))], 'ox_exam_timer' not in sk))
    # G7
    t1, t2, t3, t4, t5, t6 = [R.get(k) or {} for k in ('t1', 't2', 't3', 't4', 't5', 't6')]
    tr = R.get('trun') or {}
    a('G7', R.get('tgo') and R.get('tstop') and t1.get('v') in ('00H00M03S', '00H00M04S') and (t1.get('reset') or {}).get('vis') and tr.get('go') == '❚❚' and tr.get('goMark') == '1',
      '▶ 3.3초 → ❚❚ → %s · ↺ 보임 %s · 흐르는 3초 동안 ❚❚ 단추 그대로(다시 안 그림) %s' % (t1.get('v'), (t1.get('reset') or {}).get('vis'), tr.get('goMark')))
    a('G7', R.get('tr1') and (t2.get('reset') or {}).get('sure') and t2.get('v') == t1.get('v') and R.get('tr2') and t3.get('v') == '00H00M00S',
      '↺ 한 번 = %s(1.5초 뒤에도 빨강 %s) · 두 번 = %s' % (t2.get('v'), (t2.get('reset') or {}).get('sure'), t3.get('v')))
    a('G7', t4.get('v') == '00H12M34S' and not t4.get('over') and t5.get('v') == '01H13M05S' and t5.get('over') and t5.get('color') == 'rgb(220, 38, 38)' and t5.get('sub') == '· 초과 +00H03M05S',
      '흉내 12:34 → %s · 73:05 → %s 빨강 %s · 부제 「%s」' % (t4.get('v'), t5.get('v'), t5.get('color'), t5.get('sub')))
    uf = t5.get('ufs') or []
    a('G7', R.get('tclose') and R.get('treopen') and t6.get('v') == '01H13M05S' and len(uf) == 3 and uf[0] == '11px' and abs(float(uf[1][:-2]) - 6.05) < 0.1 and uf[2] == '0.7',
      '창 닫고 다시 → %s · 숫자 %s · 단위 %s · 흐림 %s' % (t6.get('v'), uf[:1], uf[1:2], uf[2:3]))
    # G8
    g8 = R.get('g8') or {}
    cnt = g8.get('cnt') or []
    badc = [c for c in cnt if not re.fullmatch(r'40문항 · %d지문' % c['n'], c['txt'] or '')]
    a('G8', len(cnt) == 17 and not badc, '17년 줄 「40문항 · N지문」 %s' % ('모두' if not badc else badc[:3]))
    r26 = g8.get('r26') or {}
    a('G8', r26.get('boxes') == 1 and r26.get('lines') == ['32/40 X8 · 72m', '🌀3 ⚠2 X12 /%d' % st.get('n26', 188)] and r26.get('overColor') == 'rgb(220, 38, 38)' and r26.get('oldChips') == 0,
      '회독 상자 두 줄 %s · 72m 빨강 %s · 옛 칩 %s' % (r26.get('lines'), r26.get('overColor'), r26.get('oldChips')))
    p8 = (R.get('g8prog') or {}).get('r26') or {}
    a('G8', p8.get('prog') == '▶ 2회독 진행중 5/40 · 23m' and p8.get('progHasClock') is False and p8.get('oldProg') == 0 and '이어서' in (p8.get('start') or []),
      '진행중 %s · ⏱ %s · 지문 진행중 칩 %s · 시작 단추 %s' % (p8.get('prog'), p8.get('progHasClock'), p8.get('oldProg'), p8.get('start')))
    # G9
    g9a, g9b = R.get('g9a') or {}, R.get('g9b') or {}
    a('G9', R.get('jn1') and g9a.get('rows', 0) > 0 and g9a.get('withMeta') == g9a.get('withChip') and g9a.get('withChip', 0) > 0,
      '민법총칙 1.2 정리 창 「%s」 — 행 %s · examMeta 있는 행 %s = 칩 단 행 %s(채팅 실측 60 중 37) · 칩 %s' % (g9a.get('title'), g9a.get('rows'), g9a.get('withMeta'), g9a.get('withChip'), g9a.get('chipSample')))
    rounds = (R.get('after') or {}).get('rounds')
    a('G9', R.get('jn2') and g9b.get('jx') == 40 and g9b.get('rows') == st.get('n26') and g9b.get('bogi') == 0 and g9b.get('res') == 0 and g9b.get('cellsPer') == [rounds] and g9b.get('order1') == 'ㄱㄴㄷ',
      '2026 기출 정리 창 「%s」 — 문제 N %s · 행 %s · 보기 상자 %s · 결과 글자 %s · 문항 칸 %s(회독 %s) · 1번 안 차례 %s' % (g9b.get('title'), g9b.get('jx'), g9b.get('rows'), g9b.get('bogi'), g9b.get('res'), g9b.get('cellsPer'), rounds, g9b.get('order1')))
    js = g9b.get('jxStyle') or []
    jx = R.get('jxInfo') or {}
    a('G9', js[:3] == ['11.5px', '900', '2px'] and R.get('jx') and jx.get('vis') and re.match(r'\d+/\d+ · 1회독째 · 고른 [①-⑤] · 정답 [①-⑤]', jx.get('txt') or ''),
      '「문제 1」 줄 %s · 칸 누름 → 「%s」' % (js, jx.get('txt')))
    return out


def main():
    global PORT
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(os.path.join(WORK, 'vendor'), exist_ok=True)
    for n in ('pdf.min.js', 'pdf.worker.min.js'):
        dst = os.path.join(WORK, 'vendor', n)
        if not os.path.exists(dst):
            src0 = os.path.join(VENDOR0, n)
            if os.path.exists(src0):
                shutil.copy(src0, dst)
            else:
                with urllib.request.urlopen(CDN + n, timeout=120) as r:
                    open(dst, 'wb').write(r.read())
    if not DATA:
        raise SystemExit('--data 폴더(문항마스터.json · 기출키.json · 문항메타.json)를 준다')
    xl = os.path.join(WORK, 'master.xlsx')
    shutil.copy(MASTER, xl)
    rec = os.path.join(WORK, 'rec.json')
    open(rec, 'wb').write(git('show', 'origin/main:minbeop/기록.json', repo=SPD))
    H.MAP = {'/data/master.json': os.path.join(DATA, '문항마스터.json'), '/data/gkey.json': os.path.join(DATA, '기출키.json'),
             '/data/meta.json': os.path.join(DATA, '문항메타.json'), '/data/rec.json': rec, '/data/master.xlsx': xl}
    srv, PORT = serve()

    new = io.open(APP, encoding='utf-8', newline='').read()
    base = git('show', BASE_REV + ':minbeop/index.html').decode('utf-8')   # 앱 파일을 마지막으로 고친 커밋(이 판을 밀면 HEAD 가 바뀐다)
    say('=== _task_ox_exview_paper 하네스 · %s ===' % time.strftime('%Y-%m-%d %H:%M:%S'))
    say('NEW  %s · %d B · md5 %s · CRLF %d' % (APP, len(new.encode('utf-8')), md5b(new.encode('utf-8')), new.count('\r\n')))
    bm = md5b(base.encode('utf-8'))
    say('BASE genie ' + BASE_REV + ' blob · %d B · md5 %s %s' % (len(base.encode('utf-8')), bm, '(= 지시서 바탕)' if bm == BASE_MD5 else '★ 지시서 바탕과 다르다'))
    say('데이터 %s · 기록 origin/main %d B' % (DATA, os.path.getsize(rec)))

    # ── G0 census
    gk = json.load(io.open(os.path.join(DATA, '기출키.json'), encoding='utf-8'))
    nq = sum(len(v) for v in gk['keys'].values())
    pdfs = sorted(f for f in os.listdir(os.path.join(GENIE, 'gichul', 'pdf')) if re.fullmatch(r'\d{4}-1-minbeop\.pdf', f))
    lst = json.load(io.open(os.path.join(GENIE, 'gichul', 'pdf', 'list.json'), encoding='utf-8'))
    add('G0', bm == BASE_MD5, '바탕 판 md5 %s = e5ca92e8' % bm[:8])
    add('G0', nq == 680 and len(gk['keys']) == 17, '기출키 문항 %d(17년 × 40 = 680) · 해 %d' % (nq, len(gk['keys'])))
    add('G0', len(pdfs) == 19 and pdfs[0].startswith('2008') and pdfs[-1].startswith('2026') and len([i for i in lst.get('items', []) if 'minbeop' in i.get('file', '')]) == 19,
        '민법 시험지 %d장 %s~%s · list.json 민법 %d' % (len(pdfs), pdfs[0][:4], pdfs[-1][:4], len([i for i in lst.get('items', []) if 'minbeop' in i.get('file', '')])))

    # ── G1 (파이썬 몫)
    sys.path.insert(0, SCRIPT)
    import openpyxl
    import _json_build as JB
    def aoa_of(p):
        wb = openpyxl.load_workbook(p, read_only=True)
        return [list(r) for r in wb['기출DB'].iter_rows(values_only=True)]
    aoa = aoa_of(MASTER)
    keys = JB.gkey_from_aoa(aoa)
    canon = JB.gkey_canon(keys)
    add('G1', md5b(canon.encode('utf-8')) == gk['meta']['keysMd5'] and json.dumps(gk['keys'], ensure_ascii=False, separators=(',', ':')) == canon,
        '마스터 기출DB → 파이썬 기출키 = 구운 파일 keys(keysMd5 %s)' % gk['meta']['keysMd5'][:8])
    head = [JB.gk_s(h) for h in aoa[0]]
    ci = {h: i for i, h in reversed(list(enumerate(head)))}
    rows = [r for r in aoa[1:] if JB.gk_s(r[ci['연도']]) and JB.gk_int(JB.gk_s(r[ci['문번']])) > 0]
    by = {}
    for r in rows:
        by.setdefault((JB.gk_s(r[ci['연도']]), JB.gk_int(JB.gk_s(r[ci['문번']]))), []).append(r)
    gv = lambda r, k: JB.gk_s(r[ci[k]] if ci[k] < len(r) else None)
    KO = JB.GK_KO
    cat = {'일반Y1': 0, '일반원문자': 0, '조합원문자': 0, '조합Y': 0, '예외': []}
    same = diff = multi = 0
    difl = []
    for (y, n), rs in sorted(by.items()):
        k = keys[y][str(n)]
        cir = [gv(r, '정답선지') for r in rs if gv(r, '정답선지') in list('①②③④⑤')]
        ys = [r for r in rs if gv(r, '정답선지') == 'Y']
        if k['combo']:
            cat['조합원문자' if cir else '조합Y'] += 1
            continue
        if cir:
            cat['일반원문자'] += 1
        elif len(ys) == 1:
            cat['일반Y1'] += 1
        else:
            cat['예외'].append('%s-%d(Y %d)' % (y, n, len(ys)))
        oxs = [(JB.gk_int(gv(r, '지문')), gv(r, '정답').upper()) for r in rs]
        want = 'X' if k['neg'] else 'O'
        lone = [no for no, v in oxs if v == want]
        if len(k['ans']) > 1:
            multi += 1
        elif len(lone) == 1 and k['ans'] == lone:
            same += 1
        else:
            diff += 1
            difl.append('%s-%d 키%s 혼자%s' % (y, n, k['ans'], lone))
    ncombo = cat['조합원문자'] + cat['조합Y']
    add('G1', (cat['일반Y1'], cat['일반원문자'], cat['조합원문자'], cat['조합Y'], len(cat['예외'])) == (556, 33, 7, 82, 2),
        '갈래 = 일반 Y한줄 %d · 일반 원문자 %d · 조합 원문자 %d · 조합 Y %d · 예외 %s (§0-1 표 556·33·7·82·2)' % (cat['일반Y1'], cat['일반원문자'], cat['조합원문자'], cat['조합Y'], cat['예외']))
    add('G1', ncombo == 89 and same == 589 and diff == 0 and multi == 2,
        '독립 대조(조합형 아닌 %d) — 기출키 정답 = 지문 정답 O/X 가운데 혼자 다른 하나: 같음 %d · 다름 %d %s · 복수 정답 %d' % (680 - ncombo, same, diff, difl[:3], multi))
    def judge(aoa_):
        h = [JB.gk_s(x) for x in aoa_[0]]
        c = {x: i for i, x in reversed(list(enumerate(h)))}
        g = lambda r, k: JB.gk_s(r[c[k]] if c[k] < len(r) else None)
        byc, byl, lk, dy = set(), set(), 0, 0
        for r in aoa_[1:]:
            y, n = g(r, '연도'), JB.gk_int(g(r, '문번'))
            if not y or n <= 0:
                continue
            if g(r, '조합형') == 'Y':
                byc.add((y, n))
            if len(g(r, '지문')) == 1 and g(r, '지문') in KO:
                byl.add((y, n))
                if g(r, '조합형') != 'Y':
                    lk += 1
            elif g(r, '조합형') == 'Y' and g(r, '지문').isdigit():
                dy += 1
        return len(byc), len(byl), lk, dy
    bak = ['OXminbub_OMR_2026111111.bak_20260926_181726.xlsx']   # §A-0 고치기 전(못 박음 — 뒤 판 백업을 집지 않게)
    jn, jb = judge(aoa), judge(aoa_of(os.path.join(os.path.dirname(MASTER), bak[-1])))
    add('G1', jn[:2] == (89, 89) and jn[2:] == (0, 0) and jb[0] == 88 and jb[1] == 89 and jb[2:] == (4, 0),
        '조합형 칸 판정 %d = 글자 판정 %d · 글자인데 칸≠Y %d · 숫자인데 칸=Y %d — 헛잣대(고치기 전 %s) 칸 %d · 글자 %d · %d · %d' % (jn + (bak[-1][-20:],) + jb))
    # 셀 diff 사슬 — ① 181726(고치기 전) → 210022(§A-0 + 2020-24 뒤) = _exv_master_fix 계획 · ② 210022 → 본판 = _exv_master_fix2(Q5062 꼴 9행) 계획
    d0 = os.path.dirname(MASTER)
    env = dict(os.environ, EXV_BAK=os.path.join(d0, 'OXminbub_OMR_2026111111.bak_20260926_181726.xlsx'),
               EXV_AFTER=os.path.join(d0, 'OXminbub_OMR_2026111111.bak_20260926_210022.xlsx'))
    for nm, args, e_, note in (('①', [os.path.join(SCRIPT, '_exv_master_fix.py'), '--verify-xl'], env, '§A-0 5칸 + 2020-24 사용자 승인 17칸 · 22열은 Q5062 한 칸'),
                               ('②', [os.path.join(SCRIPT, '_exv_master_fix2.py'), '--verify-xl'], None, 'Q5062 꼴 9행 18~21열 36칸 + 23열 8칸 · 22열 0칸(사용자 승인 21:00)')):
        r = subprocess.run([sys.executable] + args, capture_output=True, timeout=900, env=e_)
        vo = r.stdout.decode('utf-8', 'replace')
        m = re.search(r'다른 칸 (\d+) · 계획 (\d+) · 어긋남 (\d+) · 빠짐 (\d+)', vo)
        add('G1', r.returncode == 0 and '판정 = OK' in vo and m and m.group(3) == '0' and m.group(4) == '0',
            '셀 diff %s(백업 ↔ 뒤 판 전 칸) — 다른 칸 %s = 계획 %s(%s) · 어긋남 %s' % (nm, m and m.group(1), m and m.group(2), note, m and m.group(3)))
    src_new = new
    def fn_body(src, name):
        i = src.find('function ' + name + '(')
        return src[i:i + 4000] if i >= 0 else ''
    add('G1', 'gkeyPutFromSheet(gkey' in fn_body(src_new, 'importExcelFile') and 'gkeyFromSheet(wb.Sheets[GKEY_SHEET])' in fn_body(src_new, 'readWorkbook')
        and 'gkeyRefresh(null, true)' in fn_body(src_new, 'loadServerData') and 'gkeyRefresh(null, true)' in fn_body(src_new, 'bootData') and 'gkeyRefresh(m)' in fn_body(src_new, 'mbCheckNew')
        and '문항 파일·딱지·기출키 <b>셋뿐</b>' in src_new,
        '앱 길 — 엑셀(readWorkbook→importExcelFile) · 서버(loadServerData·bootData) · 새 판 알림(mbCheckNew) · 도움말 「셋뿐」')

    RES = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch(headless=True, args=['--disable-gpu'])
        if ONLY in (None, 'new'):
            t0 = time.time()
            RES['new'] = run_desktop(br, 'new', new)
            say('  [new] %.0f초 · pageerror %d · 누름 못함 %d' % (time.time() - t0, len(RES['new']['errs']), len(RES['new']['miss'])))
        if ONLY in (None, 'ipad'):
            t0 = time.time()
            RES['ipad'] = run_ipad(br, 'ipad', new)
            say('  [ipad] %.0f초 · pageerror %d · 누름 못함 %d' % (time.time() - t0, len(RES['ipad']['errs']), len(RES['ipad']['miss'])))
        if ONLY in (None, 'base'):
            t0 = time.time()
            RES['base'] = run_desktop(br, 'base', base)
            say('  [base] %.0f초 · pageerror %d · 누름 못함 %d' % (time.time() - t0, len(RES['base']['errs']), len(RES['base']['miss'])))
        if ONLY in (None, 'a1'):   # add1(9/27) §F — NEW · BASE2(0d4144c) × 책상 · 아이패드 · 폰
            import _harness_ox_exview_paper_add1 as A1
            base2 = git('show', A1.BASE2_REV + ':minbeop/index.html').decode('utf-8')
            say('BASE2 genie %s blob · %d B · md5 %s' % (A1.BASE2_REV, len(base2.encode('utf-8')), md5b(base2.encode('utf-8'))[:8]))
            RES.update(A1.runs(sys.modules[__name__], br, new, base2, say))
        if ONLY in (None, 'a2'):   # add2(9/27) §E — NEW · BASE3(9d367aa) · Chromium 책상·폰 + WebKit 폰·책상
            import _harness_ox_exview_paper_add2 as A2
            base3 = git('show', A2.BASE3_REV + ':minbeop/index.html').decode('utf-8')
            say('BASE3 genie %s blob · %d B · md5 %s' % (A2.BASE3_REV, len(base3.encode('utf-8')), md5b(base3.encode('utf-8'))[:8]))
            RES.update(A2.runs(sys.modules[__name__], br, new, base3, say))
            RES.update(A2.runs_wk(sys.modules[__name__], pw, new, base3, say))
        if ONLY == 'a3' or (ONLY is None and ARG('--base4')):   # add3(9/27) §C — NEW · BASE4(앞 인도 판 --base4) · Chromium 책상·아이패드 + WebKit 책상 · --base4 없는 전체 판은 옛 그대로(본판·add1·add2)
            import _harness_ox_exview_paper_add3 as A3
            A3.BASE4_REV = ARG('--base4')
            if not A3.BASE4_REV:
                raise SystemExit('--base4 <앞 인도 판 커밋> 을 준다(add3 헛잣대)')
            base4 = git('show', A3.BASE4_REV + ':minbeop/index.html').decode('utf-8')
            say('BASE4 genie %s blob · %d B · md5 %s' % (A3.BASE4_REV, len(base4.encode('utf-8')), md5b(base4.encode('utf-8'))[:8]))
            RES.update(A3.runs(sys.modules[__name__], br, new, base4, say))
            RES.update(A3.runs_wk(sys.modules[__name__], pw, new, base4, say))
        if ONLY == 'lw' or (ONLY is None and ARG('--base5')):   # _task_ox_linkwin(9/27) §B — NEW · BASE5(앞 인도 판 --base5) · Chromium 책상·아이패드 + WebKit 책상
            import _harness_ox_linkwin as LW
            LW.BASE5_REV = ARG('--base5')
            if not LW.BASE5_REV:
                raise SystemExit('--base5 <앞 인도 판 커밋> 을 준다(linkwin 헛잣대)')
            base5 = git('show', LW.BASE5_REV + ':minbeop/index.html').decode('utf-8')
            say('BASE5 genie %s blob · %d B · md5 %s' % (LW.BASE5_REV, len(base5.encode('utf-8')), md5b(base5.encode('utf-8'))[:8]))
            RES.update(LW.runs(sys.modules[__name__], br, new, base5, say))
            RES.update(LW.runs_wk(sys.modules[__name__], pw, new, base5, say))
        if ONLY == 'rx' or (ONLY is None and ARG('--base6')):   # _task_ox_revfix0928(9/28) §B — NEW · BASE6(앞 인도 판 --base6) · ✕ 크기(linkwin 모듈) · 받기 실패한 날(add2 모듈) · Chromium + WebKit
            import _harness_ox_linkwin as LW
            import _harness_ox_exview_paper_add2 as A2
            b6 = ARG('--base6')
            if not b6:
                raise SystemExit('--base6 <앞 인도 판 커밋> 을 준다(revfix0928 헛잣대)')
            base6 = git('show', b6 + ':minbeop/index.html').decode('utf-8')
            say('BASE6 genie %s blob · %d B · md5 %s' % (b6, len(base6.encode('utf-8')), md5b(base6.encode('utf-8'))[:8]))
            RES.update(LW.runs_x(sys.modules[__name__], br, new, base6, say))
            RES.update(A2.runs_skip(sys.modules[__name__], br, new, base6, say))
            wk = pw.webkit.launch()
            try:
                RES.update(LW.runs_x(sys.modules[__name__], wk, new, base6, say, wk=True))
                RES.update(A2.runs_skip(sys.modules[__name__], wk, new, base6, say, wk=True))
            finally:
                wk.close()
        br.close()
    io.open(os.path.join(WORK, 'res.json'), 'w', encoding='utf-8').write(json.dumps(RES, ensure_ascii=False, indent=1, default=str))

    if 'new' in RES:
        R = RES['new']
        st = R.get('setup') or {}
        say('— NEW 준비: 문항 %s · 기출키 %s · IndexedDB %s · U %s · 2026 지문 %s' % (st.get('q'), (st.get('gkey') or {}).get('meta', {}).get('keysMd5', '')[:8], st.get('gkeyIdb'), st.get('U'), st.get('n26')))
        # G1 JS 몫
        g1 = R.get('g1') or {}
        add('G1', g1.get('gk') == canon, '앱 「엑셀 적용」 길 readWorkbook → gkeyFromSheet 기출키 = 파이썬 기출키 바이트 동일(%s B · md5 %s)' % (len((g1.get('gk') or '').encode('utf-8')), md5b((g1.get('gk') or '').encode('utf-8'))[:8]))
        add('G1', g1.get('putKeep') is True and st.get('gkeyIdb') is True and (st.get('gkey') or {}).get('years') == 17,
            '엑셀 길은 keys 만 갈고 comboText·pdfNo 는 그대로 %s · 서버 길로 받은 기출키 IndexedDB 에 %s' % (g1.get('putKeep'), st.get('gkeyIdb')))
        # G2
        g2 = R.get('g2') or {}
        ys = g2.get('years') or {}
        N = sum(v.get('N', 0) for v in ys.values())
        M = sum(v.get('M', 0) for v in ys.values())
        missl = {y: v.get('miss') for y, v in ys.items() if v.get('miss')}
        add('G2', N + M == 89 and not missl, '조합형 89 = 글자층 N %d + comboText M %d · 못 읽음 %s' % (N, M, missl or 0))
        say('       해마다 조합형/N/M(M 문항): ' + ' · '.join('%s %d/%d/%d%s' % (y, v.get('combo'), v.get('N'), v.get('M'), v.get('Ml') or '') for y, v in sorted(ys.items()) if v.get('combo')))
        add('G2', not g2.get('undecided') and g2.get('multiAns') == ['2020-19:1·2·3·4·5', '2021-23:1·3'],
            '680 문항 정답 — 못 정함 %s · 복수 정답 %s' % (g2.get('undecided') or 0, g2.get('multiAns')))
        add('G2', g2.get('nullM') == M and M > 0, '헛잣대 — comboText 를 빼면 못 정함 %d = M %d %s' % (g2.get('nullM'), M, (g2.get('nullUndecided') or [])[:6]))
        gold = g2.get('golden') or {}
        gbad = {k: gold.get(str(k)) for k, v in GOLD26.items() if gold.get(str(k)) != v}
        add('G2', not gbad, '2026 조합 일곱 = §A-2 골든 글자 %s' % ('모두 같음' if not gbad else gbad))
        add('G2', g2.get('ans26') == ANS26, '2026 40문항 정답 = 지시서 대조값 %s' % ('같음' if g2.get('ans26') == ANS26 else g2.get('ans26')))
        add('G2', g2.get('a2020_24') == [3], '2020-24(사용자 승인 고침 뒤) Y {ㄷ, ㄹ} → %s(시험지 ③)' % g2.get('a2020_24'))
        gm = R.get('g2map') or {}
        add('G2', gm.get('moves') == 51 and gm.get('win') == 51 and gm.get('keep', {}).get('ok') == gm.get('keep', {}).get('n'),
            '번호 대응(2011·2018) — 옮긴 %s 모두 시험지 덩이가 제 지문과 더 닮음 %s/%s %s · 안 옮긴 %s/%s 닮음' % (gm.get('moves'), gm.get('win'), gm.get('moves'), gm.get('lose') or '', gm.get('keep', {}).get('ok'), gm.get('keep', {}).get('n')))
        ch = gm.get('chip') or {}
        add('G2', ch.get('p') == ch.get('want') and '(시험지 %s번)' % ch.get('pn') in (ch.get('head') or ''),
            '칩 → 시험지 창 — 2018 1번 칩 머리 「%s」 · 쪽 %s = 시험지 %s번 쪽 %s' % (ch.get('head'), ch.get('p'), ch.get('pn'), ch.get('want')))
        # G3 전 해 — 앱이 싣는 지문 표지 = 기출DB 지문 표지(조합형 보기 상자에 빠지는 지문 · 일반 「마스터에 없음」 자리)
        lab = R.get('labels') or {}
        norm = lambda l: str('①②③④⑤'.index(l) + 1) if l in '①②③④⑤' else l
        lmiss = []
        for (y_, n_), rs in sorted(by.items()):
            want_l = sorted(norm(gv(r, '지문')) for r in rs)
            have_l = sorted(set(norm(x) for x in (lab.get(y_) or {}).get(str(n_), [])))
            mm = [l for l in want_l if l not in have_l]
            if mm:
                lmiss.append('%s-%d%s%s' % (y_, n_, '(조합)' if keys[y_][str(n_)]['combo'] else '', ''.join(mm)))
        add('G3', not lmiss, '전 해 680문항 — 기출DB 지문 표지가 앱에 다 실림 · 빠짐 %d %s' % (len(lmiss), lmiss))
        # G3~G9
        say('— NEW G3~G9')
        for g, lst2 in gates_paper(R, 'new').items():
            for ok, msg in lst2:
                add(g, ok, msg)
        add('G4', R.get('enter'), '첫 화면 2026 줄 「N회독」 단추 진짜 클릭으로 기출뷰 진입 %s' % R.get('enter'))
        add('G4', not R['errs'] and not (R.get('err') or {}).get('err'), 'pageerror %s · window.onerror %s' % (R['errs'][:2], ((R.get('err') or {}).get('err') or [])[:2]))
        say('       누름 못함 %s' % R.get('miss'))
    if 'ipad' in RES:
        P = RES['ipad']
        say('— 아이패드(CDP 터치 반지름 22)')
        sa, sc = P.get('st_a') or {}, P.get('st_c') or {}
        add('G4', P.get('enter') and sa.get('picks') == {'2026:1': 3, '2026:2': 2, '2026:3': 1} and P.get('o4') and P.get('o5')
            and sc.get('res') == {'2026:1': 'O 맞음', '2026:2': 'O 맞음', '2026:3': 'X 틀림 · 정답 ②', '2026:4': 'O 맞음', '2026:5': 'X 틀림 · 정답 ③'},
            '[아이패드] 톡으로 진입 · 1③ 2② 3① · OMR 4④ 5② · 채점 ✓ → %s' % sc.get('res'))
        t1 = P.get('t1') or {}
        add('G7', P.get('tgo') and P.get('tstop') and t1.get('v') in ('00H00M02S', '00H00M03S'), '[아이패드] 시계 ▶ 톡 2.2초 → ❚❚ 톡 → %s' % t1.get('v'))
        s5, s3 = P.get('st5') or {}, P.get('g6s3') or {}
        add('G5', s5.get('qh') == [True, False, None] and s5.get('weak') == [False, True, True], '[아이패드] ㄱ O · ㄴ X · ㄷ 🌀 톡 → %s · 약점 %s' % (s5.get('qh'), s5.get('weak')))
        add('G6', P.get('g6cell') and ((P.get('g6s1') or {}).get('info') or {}).get('vis') and s3.get('qh') is None and len(s3.get('gone') or []) == 1,
            '[아이패드] 기록 칸 톡 → 출처 %s · × 두 번 톡 → 지움 %s · 묘비 %s' % (((P.get('g6s1') or {}).get('info') or {}).get('txt'), s3.get('qh'), s3.get('gone')))
        p1 = P.get('pill1') or {}
        add('G4', P.get('pill0') == '다음 5문제 ▶' and P.get('pillTap') and p1.get('page') == 1, '[아이패드] 알약 「%s」 톡 → 쪽 %s' % (P.get('pill0'), p1.get('page')))
        add('G4', not P['errs'] and not (P.get('err') or {}).get('err'), '[아이패드] pageerror %s · onerror %s' % (P['errs'][:2], ((P.get('err') or {}).get('err') or [])[:2]))
        say('       누름 못함 %s' % P.get('miss'))
    if 'base' in RES:
        B = RES['base']
        say('— BASE(e5ca92e8) 헛잣대 — G3~G9 가 FAIL 이어야')
        gb = gates_paper(B, 'base')
        for g in ('G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'):
            lst2 = gb.get(g, [])
            fails = [m for ok, m in lst2 if not ok]
            add('G11', len(fails) > 0, '%s 바탕 판 FAIL %d/%d — %s' % (g, len(fails), len(lst2), (fails[0][:110] if fails else '')))
        if 'new' in RES:
            # G10 — 단원 풀기 첫 쪽 셋 · 일반 OMR · 알약
            for (a_, b_), un, ub in zip(RES['new'].get('unitLabels') or [], RES['new'].get('unit') or [], B.get('unit') or []):
                add('G10', un.get('txt') == ub.get('txt') and un.get('n') == ub.get('n') and un.get('n', 0) > 0 and un.get('pinsIn') and ub.get('pinsIn'),
                    '단원 풀기 %s %s 첫 쪽 %s장 글자 %d자 바탕과 같음 %s(📍 다 얹힘 %s/%s)' % (a_, b_, un.get('n'), un.get('len', 0), un.get('txt') == ub.get('txt'), un.get('pinsIn'), ub.get('pinsIn')))
                add('G10', un.get('omr') == ub.get('omr') and un.get('pill') == ub.get('pill') and un.get('omrLen') == ub.get('omrLen'),
                    '　└ 일반 OMR 창 글자·몸통 길이 %s/%s · 알약 %s 같음' % (un.get('omrLen'), ub.get('omrLen'), un.get('pill')))
    # G10 — 옛 길 코드 줄(ox_chap_history · ox_in_progress/PROGRESS_KEY 를 쓰는 줄) 무변
    def code_lines(src, keys_):
        out = []
        for l in src.split('\n'):
            t = l.strip()
            if not t or len(t) > 3000 or t.startswith(('*', '/*', '//')):
                continue
            if any(k in l for k in keys_):
                out.append(t)
        return out
    blk = io.open(os.path.join(HERE, '_exv_block.js'), encoding='utf-8').read()
    kk = ('ox_chap_history', 'PROGRESS_KEY', "'ox_in_progress'")
    a0, b0 = code_lines(base, kk), code_lines(new, kk)
    sa = [x for x in a0 if x.startswith('const SYNC_KEYS')]
    sb = [x for x in b0 if x.startswith('const SYNC_KEYS')]
    add('G10', len(sa) == 1 and len(sb) == 1 and sb[0].startswith(sa[0][:-2] + ", 'ox_rec_gone', 'ox_exam_rounds', 'ox_exam_pick'];"),
        'SYNC_KEYS 줄 = 옛 줄 + 새 키 셋(ox_rec_gone · ox_exam_rounds · ox_exam_pick) 뿐')
    a0 = [x for x in a0 if not x.startswith('const SYNC_KEYS')]
    b0 = [x for x in b0 if not x.startswith('const SYNC_KEYS')]
    blkl = set(code_lines(blk, kk))
    extra = [x for x in b0 if x not in a0 and x not in blkl]
    lost = [x for x in a0 if x not in b0]
    add('G10', not lost and not extra, 'ox_chap_history·ox_in_progress 를 쓰는 옛 코드 줄 %d → %d(블록 %d 줄 말고 더한 줄 %d · 잃은 줄 %d)' % (len(a0), len(b0), len(blkl), len(extra), len(lost)))

    if any(k.startswith('a1new') for k in RES):
        import _harness_ox_exview_paper_add1 as A1
        A1.gates(RES, add, say)
    if 'a2new' in RES:
        import _harness_ox_exview_paper_add2 as A2
        A2.gates(RES, add, say)
    if 'a3new' in RES:
        import _harness_ox_exview_paper_add3 as A3
        A3.gates(RES, add, say)
    if 'lwnew' in RES:
        import _harness_ox_linkwin as LW
        LW.gates(RES, add, say)
    if any(k.startswith('rx') for k in RES):   # ★ revfix0928(9/28)
        import _harness_ox_linkwin as LW
        import _harness_ox_exview_paper_add2 as A2
        LW.gates_x(RES, add, say)
        A2.gates_skip(RES, add, say)
    srv.shutdown()
    np_ = sum(1 for g in G if g[1])
    say('\n합계 PASS %d / FAIL %d' % (np_, len(G) - np_))
    for g in sorted(set(x[0] for x in G)):
        xs = [x for x in G if x[0] == g]
        say('  %-4s %d/%d' % (g, sum(1 for x in xs if x[1]), len(xs)))
    io.open(RESULT, 'w', encoding='utf-8', newline='\n').write('\n'.join(OUTL) + '\n')
    say('결과 → %s' % RESULT)


if __name__ == '__main__':
    main()
