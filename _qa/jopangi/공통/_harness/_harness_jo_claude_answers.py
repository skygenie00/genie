# -*- coding: utf-8 -*-
"""조판기 1차객 「Claude 답」 칸 — _task_jo_claude_answers §J(J1~J22 · J20 은 _harness_jo_gaek_mb 따로).

  NEW  = genie 작업트리 jo/index.html (고친 판 · CRLF)
  BASE = `f8cec7a` 의 같은 파일(904,215 B · md5 945242dd…) — 헛잣대 · J19 에서는 「옛 판 기기」
  데이터 = genie jo/data(실물) · 기록 = studyplandata jopangi/기록.json(J19 원격 시작값)
  Claude 답 = **이 하네스 안에서만** 가짜 파일(G-픽스처 T901·S901) — 저장소에 안 올린다
  ★ 2026-09-27 uid 판(_task_jo_gaek_uid) — 픽스처·잣대의 지문 열쇠를 새 uid 로 옮김(같은 지문 · uid_alias.json map):
    T0138603→TR01053 · T0138599→TR01051 · T0138512→TR01054 · S0239711→SR02011 · S0239712→SR02012 · T0946093P7→T0946093r
    (옛 uid 로 적힌 답이 새 카드에 붙는지는 _harness_jo_gaek_uid.py 관문 CL 이 잰다)
  엔진 = playwright webkit · chromium — has_touch · is_mobile · 아이패드 1024×768
  누름 = touchscreen.tap(진짜 터치) · 끌기 = chromium CDP 터치(끝에서 멈춤) / webkit 신뢰 마우스(도구 한계)
  網 = 같은 출처만 · GitHub 는 SEED 가 대답(claude.json = 픽스처·404·500 · 기록.json = 메모리 원격 GET·PUT)

쓰기 : python _harness_jo_claude_answers.py
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
SPD = _roots.spd()
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = r'N:\개인\claude\jopangi'
WORK = os.path.join(tempfile.gettempdir(), 'h_jo_claude')
REL = 'jo/index.html'
JOD = os.path.join(GENIE, 'jo')
BASE_REV = 'f8cec7a'
BASE_MD5 = '945242dd1ed1d26881500df58ff518c8'
TESTS = io.open(os.path.join(HERE, '_harness_jo_claude_answers_tests.js'), encoding='utf-8').read()
IPAD_UA = ('Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 '
           '(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
FIXTURE = {
    'v': 1, 'updatedAt': '2026-09-22', 'note': '하네스 픽스처 — 저장소에 안 올린다',
    'answers': {
        'T901': {'law': '특허', 'uid': 'TR01053', 'd': '2026-09-22', 'unit': '특허 8.7.4 권리자침해입증완화규정',
                 'title': '전용실시권 침해에도 과실 추정이 되나',
                 'core': '제130조는 특허권과 전용실시권을 나란히 적는다 — 전용실시권 침해자도 과실이 추정된다.',
                 'md': ('**Q.** 전용실시권을 침해한 자도 과실이 추정되나? (하네스 픽스처 · 답 번호 T901 은 지문 열쇠가 아니다)\n\n'
                        '### A.\n| 권리 | 과실 추정 | 근거 |\n|---|---|---|\n| 특허권 침해 | O | 제130조 |\n| 전용실시권 침해 | O | 제130조 |\n'
                        '| 통상실시권 침해 | X | 조문에 없음 |\n\n'
                        '- 손해배상 청구는 특허권자가 실시하지 않아도 된다 → TR01051\n- 수입도 실시다 → TR01054\n\n'
                        '### 근거\n- 특허법 제130조 · 제128조')},
        'S901': {'law': '상표', 'uid': 'SR02011', 'd': '2026-09-22', 'unit': '상표 하네스 단원',
                 'title': '상표 하네스 답', 'core': '상표 지문 하나 — 특허 화면에서는 안 센다.',
                 'md': '**Q.** 상표 하네스 질문\n\n- 상표 하네스 답 → SR02012'}}}
SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__ALERTS=[];window.alert=function(m){__ALERTS.push(String(m));};
window.confirm=function(){return true;};window.prompt=function(){return null;};
window.__TOASTS=[];try{new MutationObserver(function(ms){ms.forEach(function(m){m.addedNodes.forEach(function(n){if(n.nodeType===1&&n.classList&&n.classList.contains('toast'))window.__TOASTS.push(String(n.textContent));});});}).observe(document.documentElement,{childList:true,subtree:true});}catch(e){}
(function(){var Q=new URLSearchParams(location.search);window.__CLMODE=Q.get('cl')||'file';window.__CLGETS=0;
var nf=window.fetch.bind(window);
window.fetch=function(u,o){o=o||{};var s=String((u&&u.url)||u);
 if(/\/contents\/jopangi\/claude\.json/.test(s)){window.__CLGETS++;
  if(window.__CLMODE==='404')return Promise.resolve(new Response('{"message":"Not Found"}',{status:404}));
  if(window.__CLMODE==='500')return Promise.resolve(new Response('{"message":"harness 500"}',{status:500}));
  return nf('/claude_fixture.json',{cache:'no-store'});}
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
try{localStorage.clear();}catch(e){}
if(Q.get('tok')!=='0'){try{localStorage.setItem('tt.cfg',JSON.stringify({token:'harness-token',person:'하네스'}));}catch(e){}}
})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
</script>"""
READY = "typeof render==='function'&&typeof popShell==='function'&&typeof linkGo==='function'&&!!window.__HZT"


def git(*a, repo=GENIE):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def J(s):
    try:
        return json.loads(s) if isinstance(s, str) else s
    except Exception:
        return {'__raw': str(s)[:300]}


def serve(tag, src):
    OUT = os.path.join(WORK, 'srv_' + tag); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    src = src.replace('\r\n', '\n')
    b = src.index('<body'); bb = src.index('>', b) + 1
    html = src[:bb] + SEED + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + TESTS + '\n</script>\n' + html[e:]
    io.open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)
    io.open(os.path.join(OUT, 'claude_fixture.json'), 'w', encoding='utf-8', newline='\n').write(json.dumps(FIXTURE, ensure_ascii=False))

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=OUT, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            if p.startswith('/data/'):
                return os.path.join(JOD, 'data', p[6:].replace('/', os.sep))
            if p in ('/index.html', '/claude_fixture.json', '/'):
                return super().translate_path(path)
            f = os.path.join(JOD, p.lstrip('/').replace('/', os.sep))
            return f if os.path.exists(f) else super().translate_path(path)

        def log_message(self, *a, **k):
            pass
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


def route_filter(route):
    return route.continue_() if route.request.url.startswith('http://127.0.0.1') else route.abort()


class S:
    def __init__(self, pg, eng):
        self.pg, self.eng = pg, eng
        self.cdp = pg.context.new_cdp_session(pg) if eng == 'chromium' else None

    def js(self, expr, arg=None):
        return J(self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr))

    def tap(self, p):
        if not p or not p.get('on'):
            return False
        self.pg.touchscreen.tap(p['cx'], p['cy'])
        return True

    def drag(self, x0, y0, x1, y1, n=10):
        if self.cdp:
            def t(ty, x, y):
                self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': ([] if ty == 'touchEnd' else [{'x': x, 'y': y, 'id': 1}])})
            t('touchStart', x0, y0)
            for i in range(1, n + 1):
                t('touchMove', x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.pg.wait_for_timeout(16)
            for i in range(5):            # 끝에서 150ms 멈췄다 뗀다(크롬 튕김 뒤 톡 삼킴 방지)
                t('touchMove', x1, y1); self.pg.wait_for_timeout(30)
            t('touchEnd', x1, y1)
            return 'cdp-touch'
        m = self.pg.mouse
        m.move(x0, y0); m.down()
        for i in range(1, n + 1):
            m.move(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.pg.wait_for_timeout(16)
        m.up()
        return 'mouse(trusted)'


def open_page(pw_br, eng, tag, src, extra='', query='tok=1&cl=file'):
    srv, port = serve('%s_%s%s' % (tag, eng, extra), src)
    ctx = pw_br.new_context(viewport={'width': 1024, 'height': 768}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=IPAD_UA)
    ctx.route('**/*', route_filter)
    pg = ctx.new_page()
    errs = {'page': [], 'console': []}
    pg.on('pageerror', lambda e: errs['page'].append(str(e)[:240]))
    pg.on('console', lambda m: errs['console'].append(m.text[:240]) if m.type == 'error' else None)
    pg.goto('http://127.0.0.1:%d/index.html?%s' % (port, query), wait_until='load', timeout=120000)
    pg.wait_for_function(READY, timeout=120000)
    return S(pg, eng), srv, ctx, errs


def main_scenario(s, new):
    pg, R = s.pg, {}
    W = pg.wait_for_timeout
    R['boot'] = s.js("__HZT.boot()")
    R['seed'] = s.js("__HZT.seed()")
    plain = (R['boot'] or {}).get('plain')
    R['J4'] = s.js("__HZT.rx()")
    R['J1'] = s.js("u=>__HZT.card(u)", 'TR01053')
    R['J2a'] = s.js("u=>__HZT.card(u)", 'TR01051')
    R['J2b'] = s.js("u=>__HZT.card(u)", 'TR01054')
    R['J3'] = s.js("u=>__HZT.card(u)", plain)
    if new:
        R['J3tap'] = s.tap(((R['J3'] or {}).get('btn') or {}).get('at')); W(350)
        R['J3win'] = s.js("u=>__HZT.win(u)", plain)
        # J1·J5 — 카드 단추 톡 → Claude 창 · 머리 끌기 · 모서리 손잡이
        c = s.js("u=>__HZT.card(u)", 'TR01053')
        R['J1tap'] = s.tap(((c or {}).get('btn') or {}).get('at')); W(400)
        R['J5win'] = s.js("u=>__HZT.win(u)", 'TR01053')
        hp = s.js("([u,p])=>__HZT.winPart(u,p)", ['TR01053', 'head'])
        if hp and hp.get('on'):
            R['J5drag'] = s.drag(hp['cx'], hp['cy'], hp['cx'] - 90, hp['cy'] - 60); W(350)
        R['J5moved'] = s.js("u=>__HZT.win(u)", 'TR01053')
        gp = s.js("([u,p])=>__HZT.winPart(u,p)", ['TR01053', 'grip'])
        R['J5grip'] = gp
        if gp and gp.get('on'):
            R['J5resize'] = s.drag(gp['cx'], gp['cy'], gp['cx'] + 60, gp['cy'] + 40); W(450)
        R['J5sized'] = s.js("u=>__HZT.win(u)", 'TR01053')
        # J6 — 창 본문 TR01051 톡 → 새 지문 팝업
        R['J6tap'] = s.tap(s.js("([u,sl,t])=>__HZT.winBtn(u,sl,t)", ['TR01053', '[data-clmdbox] button.uid', 'TR01051'])); W(400)
        R['J6'] = s.js("k=>__HZT.pop(k)", 'TR01051')
        # J7 — 정답·해설 보기 → 펴짐 · ↪ 이 지문으로 이동 → 팝업 닫고 그 마디
        R['J7ansTap'] = s.tap(s.js("([k,t])=>__HZT.popBtn(k,t)", ['TR01051', '정답·해설'])); W(250)
        R['J7ans'] = s.js("k=>__HZT.pop(k)", 'TR01051')
        R['J7goTap'] = s.tap(s.js("([k,t])=>__HZT.popBtn(k,t)", ['TR01051', '↪ 이'])); W(1600)   # ★ jo_cardfix §A-5 — 「↪ 이동」(글자 단추)도 같은 단추
        R['J7where'] = s.js("k=>__HZT.where(k)", 'TR01051')
        # J8 — 다른 팝업(조문) 머리는 옛 꼴
        R['J8'] = s.js("__HZT.oldPop()")
        # J9 · J11a — 창 다시 · ✎ 정정 → 고치는 중 · 안 고치고 저장 → 정정 없음
        c = s.js("u=>__HZT.card(u)", 'TR01053')
        R['J9open'] = s.tap(((c or {}).get('btn') or {}).get('at')); W(400)
        R['J9tap'] = s.tap(s.js("([u,sl,t])=>__HZT.winBtn(u,sl,t)", ['TR01053', '.clfixbar button', '✎ 정정'])); W(250)
        R['J9'] = s.js("u=>__HZT.win(u)", 'TR01053')
        R['J11aSave'] = s.tap(s.js("([u,sl,t])=>__HZT.winBtn(u,sl,t)", ['TR01053', '.clfixbar button', '저장 (정정으로)'])); W(400)
        R['J11aFix'] = s.js("__HZT.fix()")
        R['J11aWin'] = s.js("u=>__HZT.win(u)", 'TR01053')
        # J10 — 고쳐서 저장
        R['J10edit'] = s.tap(s.js("([u,sl,t])=>__HZT.winBtn(u,sl,t)", ['TR01053', '.clfixbar button', '✎ 정정'])); W(250)
        R['J10ta'] = s.js("([u,m])=>__HZT.setTa(u,m)", ['TR01053', 'add'])
        R['J10save'] = s.tap(s.js("([u,sl,t])=>__HZT.winBtn(u,sl,t)", ['TR01053', '.clfixbar button', '저장 (정정으로)'])); W(600)
        R['J10fix'] = s.js("__HZT.fix()")
        R['J10win'] = s.js("u=>__HZT.win(u)", 'TR01053')
        R['J10card'] = s.js("u=>__HZT.card(u)", 'TR01053')
        R['J10keys'] = s.js("()=>({n:SYNC_KEYS.length,last:SYNC_KEYS[SYNC_KEYS.length-1],u:Object.keys(JSON.parse(localStorage.getItem('jopangi_sync_u')||'{}')).filter(x=>x.indexOf('jopangi.clfix|')===0)})")
        # J11b — 20,001자 → 저장 안 됨 · 취소
        c = s.js("u=>__HZT.card(u)", 'TR01053')
        s.tap(((c or {}).get('btn') or {}).get('at')); W(400)
        R['J11bEdit'] = s.tap(s.js("([u,sl,t])=>__HZT.winBtn(u,sl,t)", ['TR01053', '.clfixbar button', '✎ 정정'])); W(250)
        R['J11bFix0'] = s.js("__HZT.fix()")
        R['J11bTa'] = s.js("([u,m])=>__HZT.setTa(u,m)", ['TR01053', 'long'])
        R['J11bSave'] = s.tap(s.js("([u,sl,t])=>__HZT.winBtn(u,sl,t)", ['TR01053', '.clfixbar button', '저장 (정정으로)'])); W(400)
        R['J11bWin'] = s.js("u=>__HZT.win(u)", 'TR01053')
        R['J11bFix1'] = s.js("__HZT.fix()")
        R['J11bCancel'] = s.tap(s.js("([u,sl,t])=>__HZT.winBtn(u,sl,t)", ['TR01053', '.clfixbar button', '취소'])); W(250)
        R['J11bAfter'] = s.js("u=>__HZT.win(u)", 'TR01053')
    # J12 — 「🔗 근거」 · 빈 칸
    R['J12'] = s.js("q=>__HZT.gmode(q)", '')
    if new:
        R['J12tap'] = s.tap((R['J12'] or {}).get('at')); W(350)
        R['J12dist'] = s.js("__HZT.dist()")
        # J13 — C → 전체 → ! (진짜 터치) · 코드 길(captured onclick) · 「📄 문제」 → 둘 다 꺼짐
        R['J13cTap'] = s.tap(g(R, 'J12dist', 'c', 'at')); W(250)
        R['J13afterC'] = s.js("__HZT.dist()")
        R['J13backTap'] = s.tap(g(R, 'J13afterC', 'back', 'at')); W(250)
        R['J13afterBack'] = s.js("__HZT.dist()")
        R['J13bangTap'] = s.tap(g(R, 'J13afterBack', 'bang', 'at')); W(250)
        R['J13afterBang'] = s.js("__HZT.dist()")
        R['J13code'] = s.js("__HZT.toggles()")
        pg.evaluate("()=>{GG_BANG_ONLY=true;GG_CL_ONLY=false;ggDist()}")
        R['J13mqTap'] = s.tap(s.js("__HZT.mqAt()")); W(700)
        R['J13afterMq'] = s.js("__HZT.flags()")
        # J14 — 단원 → 지문 목록 → 줄 톡 → 새 지문 팝업
        R['J14cnt'] = s.js("q=>__HZT.gmode(q)", '')
        s.tap((R['J14cnt'] or {}).get('at')); W(350)
        gl = '특허법 · ' + ((R['boot'] or {}).get('label') or '')
        ui = s.js("l=>__HZT.unitIdx(l)", gl)
        R['J14unitIdx'] = ui
        R['J14unitTap'] = s.tap(s.js("i=>__HZT.unitAt(i)", ui)) if isinstance(ui, int) and ui >= 0 else False
        W(350)
        R['J14list'] = s.js("__HZT.dist()")
        R['J14rowTap'] = s.tap(s.js("k=>__HZT.listRowAt(k)", 'TR01053')); W(450)
        R['J14pop'] = s.js("k=>__HZT.pop(k)", 'TR01053')
        # 목록 — 「C」 만 보기 · 「!」 만 보기에서 상자
        pg.evaluate("()=>{closeAllPops();GG_BANG_ONLY=false;GG_CL_ONLY=true;ggDist();}")
        R['J14clOnly'] = s.js("__HZT.dist()")
        ui2 = s.js("l=>__HZT.unitIdx(l)", gl)
        if isinstance(ui2, int) and ui2 >= 0:
            s.tap(s.js("i=>__HZT.unitAt(i)", ui2)); W(300)
        R['J14clList'] = s.js("__HZT.dist()")
        pg.evaluate("()=>{GG_BANG_ONLY=true;GG_CL_ONLY=false;ggDist();}")
        gl2 = '특허법 · ' + (g(R, 'boot', 'labels', 'TR01051') or '')
        ui3 = s.js("l=>__HZT.unitIdx(l)", gl2)
        if isinstance(ui3, int) and ui3 >= 0:
            s.tap(s.js("i=>__HZT.unitAt(i)", ui3)); W(300)
        R['J14bangList'] = s.js("__HZT.dist()")
        pg.evaluate("()=>{GG_BANG_ONLY=false;GG_CL_ONLY=false;}")
    # J15 — 검색어 「과실」(근거 0 · 픽스처만)
    R['J15'] = s.js("t=>__HZT.search(t)", '과실')
    R['J15b'] = s.js("t=>__HZT.search(t)", '침해 추정 규정')
    # J16 — 📋 정리 창
    jb = s.js("u=>__HZT.jnBtn(u)", 'TR01053')
    R['J16btn'] = jb
    R['J16tap'] = s.tap(jb); W(900)
    R['J16'] = s.js("__HZT.jnState()")
    if new:
        R['J16ans1'] = s.tap(s.js("([u,w])=>__HZT.jnPart(u,w)", ['TR01053', 'ans'])); W(250)
        R['J16open'] = s.js("u=>__HZT.jnRowState(u)", 'TR01053')
        R['J16ans2'] = s.tap(s.js("([u,w])=>__HZT.jnPart(u,w)", ['TR01053', 'ans'])); W(250)
        R['J16close'] = s.js("u=>__HZT.jnRowState(u)", 'TR01053')
        R['J16chipTap'] = s.tap(s.js("([u,w])=>__HZT.jnPart(u,w)", ['TR01053', 'chip'])); W(400)
        R['J16chipWin'] = s.js("u=>__HZT.win(u)", 'TR01053')
        pg.evaluate("()=>{const p=POPS.find(x=>x._pk==='claude|TR01053');if(p)closeOne(p)}")   # 칩으로 연 Claude 창이 줄을 덮는다
        R['J16noTap'] = s.tap(s.js("([u,w])=>__HZT.jnPart(u,w)", ['TR01053', 'no'])); W(400)
        R['J16noPop'] = s.js("k=>__HZT.pop(k)", 'TR01053')
    # J16 — 언급 지문(TR01051 · 8.7.2)이 든 묶음의 📋 → 그 줄은 「↩」
    jb2 = s.js("u=>__HZT.jnBtn(u)", 'TR01051')
    R['J16mBtn'] = jb2
    R['J16mTap'] = s.tap(jb2); W(900)
    R['J16m'] = s.js("__HZT.jnChips()")
    R['J21'] = s.js("__HZT.parse()")
    R['toasts'] = s.js("__HZT.toasts()")
    R['err'] = s.js("__HZT.errs()")
    R['ro'] = s.js("__HZT.roCount()")
    return R


def g(d, *ks):
    for k in ks:
        if isinstance(d, dict):
            d = d.get(k)
        elif isinstance(d, list) and isinstance(k, int) and -len(d) <= k < len(d):
            d = d[k]
        else:
            return None
    return d


def run_main(eng, tag, src):
    with sync_playwright() as pw:
        br = getattr(pw, eng).launch()
        s, srv, ctx, errs = open_page(br, eng, tag, src)
        try:
            R = main_scenario(s, tag == 'NEW')
        except Exception as e:
            R = {'exc': str(e)[:900]}
        R['pageerror'], R['consoleError'] = errs['page'], errs['console']
        br.close(); srv.shutdown()
    return R


def run_j17_j18(src):
    R = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for name, q in (('J17', 'tok=1&cl=404'), ('J18', 'tok=0&cl=file'), ('J18net', 'tok=1&cl=500')):
            s, srv, ctx, errs = open_page(br, 'chromium', 'NEW', src, '_' + name, q)
            D = {}
            try:
                D['boot'] = s.js("__HZT.boot()")
                D['load'] = s.js("__HZT.load()")
                D['card'] = s.js("u=>__HZT.card(u)", 'TR01053')
                D['cnt'] = s.js("q=>__HZT.gmode(q)", '')
                D['jn'] = None
                jb = s.js("__HZT.jnBtn()")
                if s.tap(jb):
                    s.pg.wait_for_timeout(800); D['jn'] = s.js("__HZT.jnState()")
                D['reload'] = s.js("__HZT.reload()")       # 두 번째 받기 — 안내가 다시 안 뜨는가(한 번만)
                D['err'] = s.js("__HZT.errs()")
            except Exception as e:
                D['exc'] = str(e)[:500]
            D['pageerror'], D['consoleError'] = errs['page'], errs['console']
            R[name] = D
            ctx.close(); srv.shutdown()
        # §A-2 받는 때 — 앱 시작 = recBoot 한 번 + 첫 syncRecords(겹침 → 한 번) · syncRecords 가 돌면 한 번 더
        s, srv, ctx, errs = open_page(br, 'chromium', 'NEW', src, '_A2')
        D = {}
        try:
            D['boot'] = s.js("__HZT.boot()")
            D['gets0'] = s.pg.evaluate("window.__CLGETS")
            D['both'] = s.pg.evaluate("(async()=>{const a=clLoad(), b=clLoad(); await a; await b; return window.__CLGETS})()")
            D['sync'] = s.js("f=>__HZT.sync(f)", False)
            D['gets1'] = s.pg.evaluate("window.__CLGETS")
            D['err'] = s.js("__HZT.errs()")
        except Exception as e:
            D['exc'] = str(e)[:400]
        R['A2'] = D
        ctx.close(); srv.shutdown()
        br.close()
    return R


def run_j19(base, new, rec0):
    """옛 판 기기(BASE)가 jopangi.clfix 가 든 원격 기록을 받아 올릴 때 · 새 판 기기가 다음 동기화에서"""
    R = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        A, sa, ca, ea = open_page(br, 'chromium', 'NEW', new, '_A')
        B, sb, cb, eb = open_page(br, 'chromium', 'BASE', base, '_B')
        C, sc, cc, ec = open_page(br, 'chromium', 'NEW', new, '_C')
        try:
            for x in (A, B, C):
                x.js("__HZT.boot()")
                x.js("f=>__HZT.sync(f)", False)                   # 부트 동기화가 끝나게
                x.pg.evaluate("()=>clearTimeout(recTouchT)")
            # ① 새 판 기기 A — 정정 하나 · 원격(실물 기록)과 맞춰 올린다
            A.pg.evaluate("m=>__HZT.fixPut(m)", 'A 기기 정정본'); A.pg.evaluate("()=>clearTimeout(recTouchT)")
            A.js("__HZT.stamp()")
            A.pg.evaluate("([t,h])=>__HZT.remoteSet(t,h)", [rec0, 'S0'])
            R['A1'] = A.js("f=>__HZT.sync(f)", True)
            P1 = J(A.pg.evaluate("__HZT.remoteGet()"))['text']
            p1 = json.loads(P1)
            R['P1'] = {'data': 'jopangi.clfix' in p1['data'], 'fix': p1['data'].get('jopangi.clfix'), 'u': p1['u'].get('jopangi.clfix|T901'), 'keys': len(p1['data'])}
            # ② 옛 판 기기 B — P1 을 받아 합치고, 제 변경 하나를 올린다(force)
            B.js("__HZT.stamp()")
            B.pg.evaluate("()=>__HZT.tagToggle()"); B.pg.evaluate("()=>clearTimeout(recTouchT)"); B.js("__HZT.stamp()")
            B.pg.evaluate("([t,h])=>__HZT.remoteSet(t,h)", [P1, 'S1'])
            R['B1'] = B.js("f=>__HZT.sync(f)", True)
            P2 = J(B.pg.evaluate("__HZT.remoteGet()"))['text']
            p2 = json.loads(P2)
            R['P2'] = {'data': 'jopangi.clfix' in p2['data'], 'u': p2['u'].get('jopangi.clfix|T901'), 'keys': len(p2['data']),
                       'gone': [x for x in (p2.get('gone') or {}) if x.startswith('jopangi.clfix|')],
                       'tag': ((p2['data'].get('jopangi.ox') or {}).get('TR01053') or {}).get('tg')}
            R['Blocal'] = B.pg.evaluate("k=>__HZT.ls(k)", 'jopangi.clfix')
            # ③ 새 판 기기 A — P2 를 받는다(강제 아님)
            A.pg.evaluate("([t,h])=>__HZT.remoteSet(t,h)", [P2, 'S2'])
            R['A2'] = A.js("f=>__HZT.sync(f)", False)
            P3 = J(A.pg.evaluate("__HZT.remoteGet()"))
            p3 = json.loads(P3['text'])
            R['P3'] = {'puts': P3.get('puts'), 'data': 'jopangi.clfix' in p3['data'], 'fix': p3['data'].get('jopangi.clfix'),
                       'tag': ((p3['data'].get('jopangi.ox') or {}).get('TR01053') or {}).get('tg')}
            R['Alocal'] = A.pg.evaluate("k=>__HZT.ls(k)", 'jopangi.clfix')
            # ④ 새 판 기기 C(정정 없음) — P2 를 먼저 · 그다음 P3
            C.js("__HZT.stamp()")
            C.pg.evaluate("([t,h])=>__HZT.remoteSet(t,h)", [P2, 'S2'])
            R['C1'] = C.js("f=>__HZT.sync(f)", False)
            R['Clocal1'] = C.pg.evaluate("k=>__HZT.ls(k)", 'jopangi.clfix')
            C.pg.evaluate("([t,h])=>__HZT.remoteSet(t,h)", [P3['text'], 'S3'])
            R['C2'] = C.js("f=>__HZT.sync(f)", False)
            R['Clocal2'] = C.pg.evaluate("k=>__HZT.ls(k)", 'jopangi.clfix')
            R['err'] = [A.js("__HZT.errs()"), B.js("__HZT.errs()"), C.js("__HZT.errs()")]
        except Exception as e:
            R['exc'] = str(e)[:900]
        for c in (ca, cb, cc):
            c.close()
        for sv in (sa, sb, sc):
            sv.shutdown()
        br.close()
    return R


def main():
    os.makedirs(WORK, exist_ok=True)
    new = io.open(os.path.join(GENIE, REL), encoding='utf-8', newline='').read()
    base = git('show', BASE_REV + ':' + REL).decode('utf-8')
    rec0 = git('show', 'origin/main:jopangi/기록.json', repo=SPD).decode('utf-8')
    RES = {}
    only = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else ''
    for eng in ('webkit', 'chromium'):
        for tag, src in (('BASE', base), ('NEW', new)):
            k = '%s/%s' % (eng, tag)
            if only and only not in k:
                continue
            t0 = time.time(); print('… ' + k, flush=True)
            RES[k] = run_main(eng, tag, src)
            print('   %.1fs%s' % (time.time() - t0, ('  EXC ' + RES[k]['exc']) if RES[k].get('exc') else ''), flush=True)
    if not only:
        t0 = time.time(); print('… J17·J18·A-2', flush=True); RES['j1718'] = run_j17_j18(new); print('   %.1fs' % (time.time() - t0), flush=True)
        t0 = time.time(); print('… J19', flush=True); RES['j19'] = run_j19(base, new, rec0); print('   %.1fs' % (time.time() - t0), flush=True)
    json.dump(RES, io.open(os.path.join(WORK, 'raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    report(RES, base, new, rec0, only)


def report(RES, base, new, rec0, only=''):
    L = []
    T = lambda n, c, i=None: L.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c or i is None else ' | ' + json.dumps(i, ensure_ascii=False)[:900]))
    I = lambda n, v: L.append('INFO | ' + n + ' | ' + json.dumps(v, ensure_ascii=False)[:1400])
    ORANGE, SUB = 'rgb(180, 83, 9)', 'rgb(107, 103, 95)'
    # ══ 소스 · 파일
    bb = base.encode('utf-8'); nb_raw = open(os.path.join(GENIE, REL), 'rb').read(); nb = nb_raw.replace(b'\r\n', b'\n')
    T('착수 %s = 지시서 G0-1 (904,215 B · md5 945242dd…)' % BASE_REV, len(bb) == 904215 and hashlib.md5(bb).hexdigest() == BASE_MD5, [len(bb), hashlib.md5(bb).hexdigest()])
    T('J21 NEW 작업트리 CRLF 그대로(LF 단독 0 · %d 줄) · U+FFFD 0 · %d B · md5(LF) %s' % (nb_raw.count(b'\r\n'), len(nb_raw), hashlib.md5(nb).hexdigest()),
      nb_raw.count(b'\n') == nb_raw.count(b'\r\n') and '\ufffd' not in new)
    ch = [l for l in git('status', '--porcelain').decode('utf-8').split('\n') if l.strip()]
    T('genie 작업트리 바뀐 파일 = jo/index.html 하나 %s' % ch, ch == [' M ' + REL], ch)
    sk = lambda s: re.findall(r"'([^']+)'", re.search(r'const SYNC_KEYS = \[(.+?)\]', s.replace('\r\n', '\n'), re.S).group(1))
    T('§F SYNC_KEYS = 옛 29키 그대로 + 끝에 clfix (30키)', sk(new) == sk(base) + ['clfix'] and len(sk(new)) == 30, [len(sk(base)), sk(new)[-3:]])
    nl = new.replace('\r\n', '\n')
    T('§A-2 받는 길 — CL_PATH 상수 · ghRaw(같은 저장소·raw·토큰) · recBoot 한 번 · syncRecords 안 한 번 · 저장소(localStorage·IndexedDB)에 안 넣는다',
      "const CL_PATH = 'jopangi/claude.json';" in nl and 'await ghRaw(CL_PATH)' in nl
      and 'recPaint(); stampAll(); clLoad(); syncRecords();' in nl
      and re.search(r"if \(navigator\.onLine === false\)\{ recPaint\(\); return; \}\n  clLoad\(\);", nl) is not None
      and not re.search(r"(setItem|lsWrite|sPut|idbPut)\([^)]*(CL_DATA|claude\.json|CL_PATH)", nl))
    T('§A 앱이 claude.json 을 쓰는 길 0(CL_PATH 는 상수 · ghRaw 두 곳뿐 · ghPutJson 에 안 간다)', nl.count('CL_PATH') == 2 and 'ghPutJson(CL_PATH' not in nl, nl.count('CL_PATH'))
    T('§I 공개 genie 에 claude.json·픽스처가 없다', not os.path.exists(os.path.join(GENIE, 'jo', 'claude.json')) and 'T901' not in nl, 'T901' in nl)
    T('§H jnAnsToggle — 같은 부모의 data-jnans 를 찾는다(다음 형제 아님)', "btn.parentElement.querySelector(':scope > [data-jnans]')" in nl)
    T('§E sidCardEl 은 남는다(패널이 쓴다) · popCard 정의 1', nl.count('function sidCardEl(') == 1 and nl.count('function popCard(') == 1)
    pc = [m.start() for m in re.finditer(r'\bpopCard\(', nl)]
    callers = []
    for p in pc:
        ln = nl.count('\n', 0, p) + 1
        line = nl.split('\n')[ln - 1].strip()
        if line.startswith('function popCard('):
            continue
        callers.append('%d: %s' % (ln, line[:90]))
    I('§E popCard 부르는 곳 전수(새 판 줄 · 새로 더한 곳 포함)', callers)
    # ══ 부트
    for eng in ('webkit', 'chromium'):
        for tag in ('BASE', 'NEW'):
            d = RES.get('%s/%s' % (eng, tag))
            if d is None:
                continue
            errs = (d.get('err') or []) + [e for e in (d.get('pageerror') or []) if not e.startswith('ResizeObserver loop')]
            T('[%s] %s 부트 · 특허 1차객 지문 %s · JS 오류 %d (ResizeObserver 알림 %s — 브라우저 알림 · 따로 셈)' % (eng, tag, g(d, 'boot', 'pool'), len(errs), d.get('ro')), (g(d, 'boot', 'pool') or 0) > 2000 and not d.get('exc') and not errs,
              [d.get('exc'), errs[:4]])
    for eng in ('webkit', 'chromium'):
        n, b = RES.get(eng + '/NEW') or {}, RES.get(eng + '/BASE') or {}
        if not n:
            continue
        p = '[%s] ' % eng
        bt = n.get('boot') or {}
        T(p + '§A 받기 — CL_STATE %s · 직접 %s · 언급 %s' % (bt.get('cl'), bt.get('by'), sorted((bt.get('ment') or {}).keys())),
          bt.get('cl') == 'ok' and bt.get('by') == {'TR01053': ['T901'], 'SR02011': ['S901']} and sorted((bt.get('ment') or {}).keys()) == sorted(['SR02012', 'TR01054', 'TR01051']), bt)
        j4 = n.get('J4') or {}
        T(p + 'J4 정규식 — 잡힌 것 %s · 본문 단추 %s' % (j4.get('match'), j4.get('btns')),
          j4.get('match') == ['TR01053', 'T0946093r', 'SR02011', 'D1234567'] and j4.get('btns') == ['data-sid="TR01053"', 'data-sid="T0946093r"'], j4)
        b1 = g(n, 'J1', 'btn') or {}
        T(p + 'J1 TR01053 카드 — 「✏️ 연결」 바로 앞(%s) 주황 「%s」 · 11px · 테두리·바탕 없음 · 높이 %s ↔ 연결 %s'
          % (g(n, 'J1', 'next'), b1.get('text'), g(b1, 'at', 'h'), g(n, 'J1', 'lnk', 'at', 'h')),
          b1.get('text') == 'Claude1' and b1.get('color') == ORANGE and b1.get('fs') == '11px' and b1.get('fw') == '700' and g(n, 'J1', 'next') == '✏️ 연결'
          and (b1.get('bd') or '').startswith('0px') and b1.get('bg') in ('rgba(0, 0, 0, 0)', 'transparent') and b1.get('title') == 'T901 답'
          and abs((g(b1, 'at', 'h') or 0) - (g(n, 'J1', 'lnk', 'at', 'h') or 99)) <= 1.5 and g(n, 'J1', 'n') == 1, n.get('J1'))
        T(p + 'J1 헛잣대 BASE — 같은 카드에 Claude 단추 없음', g(b, 'J1', 'card') is True and g(b, 'J1', 'btn') is None and g(b, 'J1', 'n') == 0, b.get('J1'))
        for key, nm in (('J2a', 'TR01051'), ('J2b', 'TR01054')):
            b2 = g(n, key, 'btn') or {}
            T(p + 'J2 %s 카드 — 회색 「Claude」 + 주황 「↩」(10px 800) · title 「%s」' % (nm, b2.get('title')),
              b2.get('text') == 'Claude↩' and b2.get('color') == SUB and b2.get('fw') == '500' and g(b2, 'kids', 0, 't') == '↩'
              and g(b2, 'kids', 0, 'color') == ORANGE and g(b2, 'kids', 0, 'fs') == '10px' and g(b2, 'kids', 0, 'fw') == '800' and b2.get('title') == 'T901 답에서 언급', b2)
        b3 = g(n, 'J3', 'btn') or {}
        T(p + 'J3 %s(답·언급 없음) — 회색 「Claude」 · 톡 → 창 안내 「%s」' % (g(n, 'boot', 'plain'), (g(n, 'J3win', 'note') or '')[:30]),
          b3.get('text') == 'Claude' and b3.get('color') == SUB and n.get('J3tap') is True and g(n, 'J3win', 'win') is True
          and g(n, 'J3win', 'note') == '이 지문에 걸린 Claude 답이 아직 없다. 채팅에서 물어보면 적립되고 여기 붙는다.' and g(n, 'J3win', 'answers') == [], [b3, n.get('J3win')])
        w5 = n.get('J5win') or {}
        T(p + 'J1 톡 → Claude 창 · 제목 「%s」' % w5.get('title'), n.get('J1tap') is True and w5.get('win') is True and w5.get('title') == 'Claude · 2001년 5번(3) · TR01053', w5)
        T(p + 'J5 창 틀 — 폭 %s · 머리 %s · 「%s」 %s · ≡ %s · 제목 %s · 테두리/둥근/그림자 %s'
          % (g(w5, 'rect', 2), w5.get('headBg'), w5.get('close'), w5.get('closeStyle'), w5.get('drag'), w5.get('titleStyle'), w5.get('popStyle')),
          g(w5, 'rect', 2) == 480 and w5.get('mbwin') is True and w5.get('headBg') == 'rgb(248, 250, 252)' and w5.get('close') == '닫기'
          and w5.get('closeStyle') == ['12px', '700', 'rgb(107, 114, 128)', '1px', 'rgb(209, 213, 219)', '6px', 'rgb(255, 255, 255)']
          and w5.get('drag') == 'none' and w5.get('titleStyle') == ['13px', '800', 'rgb(17, 24, 39)'] and w5.get('headPad') == '7px 10px'
          and (w5.get('popStyle') or [None])[:3] == ['1px', 'rgb(203, 213, 225)', '12px'] and 'rgba(0, 0, 0, 0.28)' in (g(w5, 'popStyle', 3) or ''), w5)
        T(p + 'J5 글꼴 「%s」 · 본문 %s · 표 %s(칸선 %s · 머리칸 %s) · 지문 열쇠 %s · 핵심 %s'
          % ((w5.get('font') or '')[:40], w5.get('bodyStyle'), w5.get('tdFs'), w5.get('tdLine'), w5.get('thBg'), w5.get('uidStyle'), w5.get('coreStyle')),
          (w5.get('font') or '').replace('"', '').startswith('Malgun Gothic') and (w5.get('bodyStyle') or [None])[:4] == ['12.5px', '21.25px', 'rgb(255, 253, 249)', '12px']
          and g(w5, 'bodyStyle', 4) == '14px' and w5.get('tdFs') == '11.5px' and w5.get('tdLine') == 'rgb(229, 231, 235)' and w5.get('thBg') == 'rgb(250, 250, 249)'
          and w5.get('uidStyle') == ['11.5px', '800', 'rgb(29, 78, 216)', 'dotted', '0px', 'rgba(0, 0, 0, 0)']
          and w5.get('coreStyle') == ['rgb(255, 247, 237)', '6px', '700', 'rgb(124, 45, 18)', '0px'], w5)
        T(p + 'J5 몸통 — 머리 %s · 오른쪽 끝 %s · 소제목 %s · 표 %s(머리칸 %s) · 목록 %s줄 · 본문 단추 %s · 핵심 · ✎ 정정 · 원문 기호 흘림 0'
          % (w5.get('head'), w5.get('headUid'), w5.get('h4'), w5.get('tables'), w5.get('th'), w5.get('li'), w5.get('uidBtns')),
          g(w5, 'head', 0, 0) == 'T901' and g(w5, 'head', 0, 1) == '2026-09-22 · 특허 8.7.4 권리자침해입증완화규정' and g(w5, 'headUid', 0, 0) == 'TR01053'
          and w5.get('h4') == ['A.', '근거'] and w5.get('tables') == 1 and w5.get('th') == 3 and w5.get('li') == 3 and w5.get('uidBtns') == ['TR01051', 'TR01054']
          and (w5.get('core') or '').startswith('핵심 — 제130조는') and w5.get('fixBtn') == '✎ 정정' and w5.get('rawTags') is False and w5.get('bold', 0) >= 1, w5)
        mv0, mv1 = w5.get('rect') or [0, 0], g(n, 'J5moved', 'rect') or [0, 0]
        ws = n.get('J5sized') or {}
        T(p + 'J5 머리 끌기(%s) %s → %s · 손잡이 끌기 %s → %s · S.popCfg.claude = %s'
          % (n.get('J5drag'), mv0[:2], mv1[:2], (n.get('J5moved') or {}).get('rect', [0, 0, 0, 0])[2:], (ws.get('rect') or [0, 0, 0, 0])[2:], ws.get('cfg')),
          abs(mv1[0] - mv0[0]) > 30 and abs(mv1[1] - mv0[1]) > 30 and ws.get('grip') is True and ws.get('sized') is True
          and isinstance(ws.get('cfg'), dict) and abs((ws.get('cfg') or {}).get('w', 0) - (ws.get('rect') or [0, 0, 0])[2]) <= 2
          and (ws.get('rect') or [0, 0, 0])[2] - g(n, 'J5moved', 'rect', 2) >= 40, [mv0, mv1, n.get('J5grip'), ws.get('rect'), ws.get('cfg')])
        j6 = n.get('J6') or {}
        T(p + 'J6 창 속 TR01051 톡 → 새 지문 팝업 · 제목 「%s」 · 칩 %s · 번호 %s · 근거 줄 %s · O/X %s · 아랫줄 %s · Claude %s'
          % (j6.get('title'), [c[0] for c in (j6.get('chips') or [])], j6.get('num'), j6.get('gg'), j6.get('ox'), j6.get('bar'), j6.get('cl')),
          n.get('J6tap') is True and j6.get('pop') is True and j6.get('mbwin') is True and j6.get('width') == 520
          and [c[0] for c in (j6.get('chips') or [])] == ['변리사 01', '특허법 · ' + (g(n, 'boot', 'labels', 'TR01051') or '?'), 'TR01051']
          and j6.get('num') == ['2001년 5번(1)', 'rgb(29, 78, 216)', '800'] and g(j6, 'txStyle', 0) == '13px' and abs(float((g(j6, 'txStyle', 1) or '0px')[:-2]) - 21.45) < 0.01 and j6.get('gg') is True and j6.get('ox') == 0
          and j6.get('ansHidden') is True and j6.get('bar') in (['정답·해설 보기', 'Claude↩', '✏️ 연결', '🃏 암기카드', '', '↪ 이 지문으로 이동'], ['정답·해설 보기', 'Claude↩', '✏️ 연결', '🃏 암기카드', '', '↪ 이동'])   # ★ jo_cardfix §A-5
          and j6.get('cl') == ['Claude↩', SUB, '11.5px'] and j6.get('title') == '2001년 5번(1) · 특허법 · ' + (g(n, 'boot', 'labels', 'TR01051') or '?'), j6)
        T(p + 'J6 칩 꼴 %s' % [c[1:] for c in (j6.get('chips') or [])],
          [c[1:] for c in (j6.get('chips') or [])] == [['rgb(107, 33, 168)', 'rgb(243, 232, 255)', '10px', '1px', '5px'],
                                                       ['rgb(67, 56, 202)', 'rgb(238, 242, 255)', '10px', '1px', '5px'],
                                                       ['rgb(156, 163, 175)', 'rgb(249, 250, 251)', '10px', '1px', '5px']], j6.get('chips'))
        j7 = n.get('J7ans') or {}
        T(p + 'J7 「정답·해설 보기」 톡 → 정답 상자 펴짐(%s · 「%s」 %s) · 단추 「%s」' % (j7.get('ansVisible'), j7.get('ans'), j7.get('ansColor'), (j7.get('bar') or [''])[0]),
          n.get('J7ansTap') is True and j7.get('ansHidden') is False and j7.get('ansVisible') is True and j7.get('ans') == '정답 O'
          and j7.get('ansColor') == 'rgb(37, 99, 235)' and (j7.get('bar') or [''])[0] == '정답·해설 접기', j7)
        w7 = n.get('J7where') or {}
        T(p + 'J7 「↪ 이 지문으로 이동」 톡 → 팝업 닫힘(%s) · 그 마디(%s · 카드 %s)' % (w7.get('pops'), w7.get('mok'), w7.get('card')),
          n.get('J7goTap') is True and not any((x or '').startswith('q|📝 지문') for x in (w7.get('pops') or [])) and w7.get('card') is True
          and (w7.get('mok') or '').startswith('__mg') and w7.get('tab') == 'jimun', w7)
        j8 = n.get('J8') or {}
        T(p + 'J8 조문 팝업(%s) — 머리 옛 꼴(파란 띠 %s · 「%s」 · ≡ %s · mbwin %s)' % (j8.get('title'), j8.get('headBg'), j8.get('btn'), j8.get('drag'), j8.get('mbwin')),
          j8.get('mbwin') is False and j8.get('headBg') == 'rgb(234, 241, 251)' and j8.get('btn') == '✕' and j8.get('drag') != 'none', j8)
        j9 = n.get('J9') or {}
        T(p + 'J9 ✎ 정정 → 글칸(%s) + 핵심 줄 남음(%s) · 딱지 없음(%s) · 단추 %s' % (j9.get('taStyle'), j9.get('coreAfterTa'), j9.get('fixtag'), j9.get('bar')),
          n.get('J9tap') is True and j9.get('ta') is True and j9.get('coreAfterTa') is True and j9.get('fixtag') is None
          and j9.get('bar') == ['저장 (정정으로)', '취소'] and j9.get('taStyle') == ['240px', '12px', 'rgb(254, 215, 170)'], j9)
        T(p + 'J11 안 고치고 저장 → 정정 안 생김(jopangi.clfix = %s) · 읽기 판으로' % n.get('J11aFix'),
          n.get('J11aSave') is True and n.get('J11aFix') is None and g(n, 'J11aWin', 'ta') is False and g(n, 'J11aWin', 'fixtag') is None, [n.get('J11aFix'), n.get('J11aWin')])
        fx = J(n.get('J10fix') or 'null') or {}
        T(p + 'J10 고쳐서 저장 → jopangi.clfix.T901.done === false · md 에 고친 줄 · ts 숫자',
          n.get('J10edit') is True and n.get('J10save') is True and g(fx, 'T901', 'done') is False and '하네스정정줄' in (g(fx, 'T901', 'md') or '')
          and isinstance(g(fx, 'T901', 'ts'), int), [n.get('J10ta'), {k: (v if k != 'md' else len(v)) for k, v in (fx.get('T901') or {}).items()}])
        T(p + 'J10 창 딱지 「%s」 · 본문에 고친 줄 · 카드 단추 「%s」 · SYNC_KEYS %s(끝 %s) · 도장 %s'
          % (g(n, 'J10win', 'fixtag'), g(n, 'J10card', 'btn', 'text'), g(n, 'J10keys', 'n'), g(n, 'J10keys', 'last'), g(n, 'J10keys', 'u')),
          (g(n, 'J10win', 'fixtag') or '').startswith('정정 · 반영 전 · ') and g(n, 'J10card', 'btn', 'text') == 'Claude1정정'
          and g(n, 'J10card', 'btn', 'kids', 1, 'bg') == 'rgb(255, 237, 213)' and g(n, 'J10keys', 'n') == 30 and g(n, 'J10keys', 'last') == 'jopangi.clfix'
          and g(n, 'J10keys', 'u') == ['jopangi.clfix|T901'] and g(n, 'J10win', 'ta') is False, [n.get('J10win'), n.get('J10card'), n.get('J10keys')])
        T(p + 'J11 20,001자 → 저장 안 됨(정정 그대로) · 「%s」 · 취소하면 읽기 판' % g(n, 'J11bWin', 'msg'),
          g(n, 'J11bTa', 'len') == 20001 and g(n, 'J11bWin', 'msg') == '20,000자까지 · 지금 20,001자' and n.get('J11bFix0') == n.get('J11bFix1')
          and g(n, 'J11bWin', 'ta') is True and g(n, 'J11bAfter', 'ta') is False, [n.get('J11bTa'), g(n, 'J11bWin', 'msg')])
        # J12~J15
        c12, c12b = n.get('J12') or {}, b.get('J12') or {}
        T(p + 'J12 「🔗 근거」 빈 칸 → 「%s」(N = 근거 ∪ Claude = %s) · 꼴 %s' % (c12.get('cnt'), c12.get('want'), c12.get('style')),
          c12.get('cnt') == '근거 3개 ▸' and c12.get('want') == 3 and c12.get('lk') is True
          and c12.get('style') == ['rgb(37, 99, 235)', '700', 'underline', '11px'], c12)
        T(p + 'J12 헛잣대 BASE — 같은 자리 「%s」' % c12b.get('cnt'), c12b.get('cnt') == '' and c12b.get('lk') is False, c12b)
        d12 = n.get('J12dist') or {}
        T(p + 'J12 톡 → 단원 목록 · 머리 「%s」 · 「!」 %s · 「C」 %s' % (d12.get('head'), d12.get('bang'), d12.get('c')),
          n.get('J12tap') is True and d12.get('hidden') is False and (d12.get('head') or '').startswith('🔗 근거 3건 · ') and (d12.get('head') or '').endswith('— 단원을 누르면 목록이 나옵니다 · ! 2 · C1')
          and d12.get('headBg') == 'rgb(249, 250, 251)' and d12.get('headFs') == '11px' and d12.get('headFw') == '800'
          and g(d12, 'bang', 'color') == 'rgb(229, 115, 115)' and g(d12, 'bang', 'bb') == 'dashed' and g(d12, 'c', 'color') == ORANGE and g(d12, 'c', 'bb') == 'dashed', d12)
        I(p + 'J12 단원 줄', [(u.get('l'), [x[0] for x in u.get('pills') or []]) for u in (d12.get('units') or [])])
        a13, k13, b13 = n.get('J13afterC') or {}, n.get('J13afterBack') or {}, n.get('J13afterBang') or {}
        T(p + 'J13 「C1」 톡 → Claude 답만(%s · 머리 「%s」 %s) · 「전체」 → %s · 「! 2」 톡 → 켜진 근거만(%s · 머리 %s)'
          % (a13.get('flags'), a13.get('head'), a13.get('headBg'), k13.get('flags'), b13.get('flags'), b13.get('headBg')),
          n.get('J13cTap') is True and a13.get('flags') == [False, True] and (a13.get('head') or '').startswith('🔗 근거 C1건 · 1개 단원 — Claude 답이 있는 것만 보는 중 · 전체 3건으로')
          and a13.get('headBg') == 'rgb(255, 247, 237)' and k13.get('flags') == [False, False] and b13.get('flags') == [True, False]
          and (b13.get('head') or '').startswith('🔗 근거 ! 2건 · ') and b13.get('headBg') == 'rgb(255, 245, 245)', [a13, k13, b13])
        c13 = n.get('J13code') or {}
        T(p + 'J13 코드 길 — C 켠 뒤 「!」 %s · 「!」 켠 뒤 C %s · 「📄 문제」 톡 → %s' % (c13.get('afterCThenBang'), c13.get('afterBangThenC'), n.get('J13afterMq')),
          c13.get('afterC') == [False, True] and c13.get('afterCThenBang') == [True, False] and c13.get('afterBangThenC') == [False, True]
          and n.get('J13mqTap') is True and n.get('J13afterMq') == [False, False, 'q'], [c13, n.get('J13afterMq')])
        l14 = g(n, 'J14list', 'list') or {}
        r603 = next((r for r in (l14.get('rows') or []) if r.get('k') == 'TR01053'), {})
        T(p + 'J14 단원(%s) → 지문 목록 %s · TR01053 줄 상자 %s' % (n.get('J14unitIdx'), l14.get('ut'), [x[:2] for x in (r603.get('boxes') or [])]),
          n.get('J14unitTap') is True and (l14.get('back') == '← 🔗 근거 단원 목록으로') and (l14.get('ut') or '').endswith('건')
          and [x[0] for x in (r603.get('boxes') or [])] == ['gfbx', 'gfbx cl'] and (g(r603, 'boxes', 1, 1) or '').startswith('C1 · 제130조는')
          and g(r603, 'boxes', 1, 2) == 'rgb(255, 247, 237)' and r603.get('id') == 'ID TR01053' and r603.get('no') == '2001년 5번(3)', l14)
        p14 = n.get('J14pop') or {}
        T(p + 'J14 줄 톡 → 새 지문 팝업(%s · O/X %s)' % (p14.get('title'), p14.get('ox')), n.get('J14rowTap') is True and p14.get('pop') is True and p14.get('mbwin') is True and p14.get('ox') == 0, p14)
        cl14, bg14 = g(n, 'J14clList', 'list') or {}, g(n, 'J14bangList', 'list') or {}
        T(p + 'J14 Claude 만 보기 목록 %s(%s) · 「!」 만 보기 목록 %s(%s)' % (cl14.get('ut'), [[x[0], x[1][:14]] for r in (cl14.get('rows') or []) for x in r.get('boxes') or []],
                                                                        bg14.get('ut'), [[x[0], x[1][:14]] for r in (bg14.get('rows') or []) for x in r.get('boxes') or []]),
          (cl14.get('ut') or '').endswith('· 1건 · Claude 답만') and [x[0] for r in (cl14.get('rows') or []) for x in r.get('boxes') or []] == ['gfbx cl']
          and (g(cl14, 'rows', 0, 'boxes', 0, 1) or '').startswith('Claude · 제130조는')
          and (bg14.get('ut') or '').endswith('· 1건 · 켜진 근거만') and [x[0] for r in (bg14.get('rows') or []) for x in r.get('boxes') or []] == ['gfbx bang']
          and g(bg14, 'rows', 0, 'k') == 'TR01051', [cl14, bg14])
        s15, s15b = n.get('J15') or {}, b.get('J15') or {}
        T(p + 'J15 「과실」 → %s · %s · 딱지 %s · 한 줄 「%s」' % (s15.get('count'), g(s15, 'rows', 0, 'name'), g(s15, 'rows', 0, 'badges'), (g(s15, 'rows', 0, 'snip') or '')[:40]),
          s15.get('count') == '1개' and (g(s15, 'rows', 0, 'name') or '').startswith('2001년 5번(3)') and g(s15, 'rows', 0, 'badges') == ['Claude']
          and '과실' in (g(s15, 'rows', 0, 'snip') or '') and '|' not in (g(s15, 'rows', 0, 'snip') or '') and '**' not in (g(s15, 'rows', 0, 'snip') or '')
          and g(s15, 'rows', 0, 'snipStyle') == ['rgb(255, 247, 237)', 'rgb(253, 186, 116)'], s15)
        T(p + 'J15 헛잣대 BASE — 「과실」 %s' % s15b.get('count'), s15b.get('count') == '0개', s15b)
        s15c = n.get('J15b') or {}
        T(p + 'J15 근거로 걸린 줄(「침해 추정 규정」) → %s · 딱지 %s(근거만 · Claude 한 줄 없음)' % (s15c.get('count'), g(s15c, 'rows', 0, 'badges')),
          s15c.get('count') == '1개' and g(s15c, 'rows', 0, 'badges') == ['근거'] and g(s15c, 'rows', 0, 'snip') is None, s15c)
        # J16
        j16, j16b = n.get('J16') or {}, b.get('J16') or {}
        t6 = j16.get('t603') or {}
        T(p + 'J16 📋 정리 창(%s · 부제 「%s」) — 띠 %s · 줄 %s · 「정답·해설 ▸」 %s · O/X %s' % (j16.get('title'), j16.get('sub'), j16.get('bands'), j16.get('rows'), j16.get('pk'), j16.get('ox')),
          n.get('J16tap') is True and j16.get('jn') is True and j16.get('mbwin') is True and len(j16.get('bands') or []) == 2 and j16.get('rows') == 75
          and j16.get('pk') == 75 and j16.get('ox') == 0 and j16.get('sub') == '특허법 · 75지문' and j16.get('close') == '닫기'
          and j16.get('bandStyle') == ['11px', '800', 'rgb(55, 48, 163)', 'rgb(248, 250, 252)'], j16)
        T(p + 'J16 C 칩 선 줄 = %s · 나머지 %s줄 칩 0(숨은 자리표 %s) — 언급 둘(TR01051 · TR01054)은 이 묶음 밖(다른 단원)이다'
          % (j16.get('withChip'), (j16.get('rows') or 0) - len(j16.get('withChip') or []), j16.get('placeholders')),
          j16.get('withChip') == ['TR01053 C1'] and j16.get('placeholders') == (j16.get('rows') or 0) - 1, j16.get('withChip'))
        jm = n.get('J16m') or {}
        T(p + 'J16 언급 지문이 든 묶음(%s · 「%s」) — 줄 %s · 칩 %s · 든 열쇠 %s' % (g(n, 'J16mBtn', 'head'), g(n, 'J16mBtn', 'title'), jm.get('rows'), jm.get('withChip'), jm.get('has')),
          n.get('J16mTap') is True and 'TR01051 ↩' in (jm.get('withChip') or []) and 'TR01053 C1' not in (jm.get('withChip') or [])
          and all((k + ' ↩') in (jm.get('withChip') or []) for k in (jm.get('has') or []) if k != 'TR01053'), jm)
        T(p + 'J16 TR01053 줄 — 「%s」 바로 뒤 「%s」 %s · 근거 상자 「%s」 %s · 형광펜 %s(「%s」) · 글 %s · 기록 「%s」'
          % (t6.get('pk'), t6.get('chip'), t6.get('chipStyle'), (t6.get('gg') or '')[:24], t6.get('ggStyle'), t6.get('mark'), t6.get('markText'), t6.get('qqStyle'), t6.get('rec')),
          t6.get('chip') == 'C1' and t6.get('chipAfterPk') is True and t6.get('chipStyle') == [ORANGE, '11px', '700', '0px', 'rgba(0, 0, 0, 0)', '8px']
          and t6.get('pk') == '정답·해설 ▸' and t6.get('pkStyle') == ['11px', '700', 'rgb(67, 56, 202)', 'rgb(238, 242, 255)', 'rgb(199, 210, 254)']
          and (t6.get('gg') or '').startswith('🔗 1. 제130조') and t6.get('ggStyle') == ['rgb(239, 246, 255)', 'rgb(96, 165, 250)']
          and t6.get('mark') == 1 and t6.get('markText') == '전용실시권을' and t6.get('qqStyle') == ['12.5px', '20.3125px'] and t6.get('ansHidden') is True and t6.get('no') == '2001년 5번(3)', t6)
        T(p + 'J16 「정답·해설 ▸」 톡 → 펴짐(%s · 「%s」) · 다시 톡 → 접힘(%s · 「%s」)'
          % (g(n, 'J16open', 'ansVisible'), g(n, 'J16open', 'pk'), g(n, 'J16close', 'ansHidden'), g(n, 'J16close', 'pk')),
          n.get('J16ans1') is True and g(n, 'J16open', 'ansHidden') is False and g(n, 'J16open', 'ansVisible') is True and g(n, 'J16open', 'pk') == '정답·해설 ▾'
          and g(n, 'J16open', 'ans') == '정답 O' and n.get('J16ans2') is True and g(n, 'J16close', 'ansHidden') is True and g(n, 'J16close', 'pk') == '정답·해설 ▸', [n.get('J16open'), n.get('J16close')])
        T(p + 'J16 C1 칩 톡 → Claude 창(%s) · 번호 톡 → 새 지문 팝업(%s)' % (g(n, 'J16chipWin', 'answers'), g(n, 'J16noPop', 'title')),
          n.get('J16chipTap') is True and g(n, 'J16chipWin', 'win') is True and g(n, 'J16chipWin', 'answers') == ['T901']
          and n.get('J16noTap') is True and g(n, 'J16noPop', 'pop') is True and g(n, 'J16noPop', 'mbwin') is True, [n.get('J16chipWin'), n.get('J16noPop')])
        T(p + 'J16 헛잣대 BASE — 옛 창은 근거 붙은 지문만(%s줄 · TR01053 형광펜 %s) · 「정답·해설」 0' % (j16b.get('oldRows'), g(j16b, 'oldT603', 'mark')),
          j16b.get('jn') is True and j16b.get('rows') == 0 and 0 < (j16b.get('oldRows') or 0) < 75 and g(j16b, 'oldT603', 'mark') == 1, j16b)
        I(p + 'J16 묶음 📋 자리', n.get('J16btn'))
        for tag, d in (('BASE', b), ('NEW', n)):
            bad = [x for x in (d.get('J21') or []) if x[2] != 'ok']
            T(p + 'J21 %s 스크립트 블록 %d개 파서 통과(%s)' % (tag, len(d.get('J21') or []), 'JSC' if eng == 'webkit' else 'V8'), (d.get('J21') or []) and not bad, bad)
        T(p + '「Claude 답을 못 받았다」 안내 0(정상 받기)', not [t for t in (n.get('toasts') or []) if 'Claude' in t], n.get('toasts'))
    if only:
        return finish(L)
    # ══ J17 · J18 · A-2
    G = RES.get('j1718') or {}
    j17, j18, j18n, a2 = G.get('J17') or {}, G.get('J18') or {}, G.get('J18net') or {}, G.get('A2') or {}
    msg = 'Claude 답을 못 받았다'
    T('J17 claude.json 404 → CL_STATE ok(빈 것) · 카드 회색 「%s」 · 「근거 N개」 %s · 정리 창 칩 %s · 안내 0 · JS 오류 0'
      % (g(j17, 'card', 'btn', 'text'), g(j17, 'cnt', 'cnt'), g(j17, 'jn', 'withChip')),
      g(j17, 'load', 'state') == 'ok' and g(j17, 'load', 'by') == {} and g(j17, 'card', 'btn', 'text') == 'Claude' and g(j17, 'card', 'btn', 'color') == SUB
      and not [t for t in (g(j17, 'reload', 'toasts') or []) if msg in t] and g(j17, 'jn', 'withChip') == [] and g(j17, 'jn', 'rows') == 75
      and not j17.get('err') and not j17.get('pageerror'), j17)
    T('J18 토큰 없음 → 단추 안 그림(보이는 %s · 숨은 자리표 %s / 아랫줄 %s) · 「%s」 %d번 · 두 번째 받기에도 한 번 · 앱 정상(정리 창 %s줄)'
      % (g(j18, 'card', 'visBtns'), g(j18, 'card', 'allBtns'), g(j18, 'card', 'mbbots'), msg, len([t for t in (g(j18, 'reload', 'toasts') or []) if msg in t]), g(j18, 'jn', 'rows')),
      g(j18, 'load', 'state') == 'fail' and g(j18, 'card', 'visBtns') == 0 and g(j18, 'card', 'btn', 'tag') == 'SPAN' and g(j18, 'card', 'btn', 'hidden') is True
      and g(j18, 'card', 'allBtns') == g(j18, 'card', 'mbbots') and len([t for t in (g(j18, 'reload', 'toasts') or []) if msg in t]) == 1
      and g(j18, 'jn', 'rows') == 75 and g(j18, 'jn', 'withChip') == [] and not j18.get('err') and not j18.get('pageerror'), j18)
    T('J18 네트워크 실패(HTTP 500)도 같다 — 단추 안 그림 · 안내 한 번', g(j18n, 'load', 'state') == 'fail' and g(j18n, 'card', 'visBtns') == 0
      and len([t for t in (g(j18n, 'reload', 'toasts') or []) if msg in t]) == 1 and not j18n.get('err'), j18n)
    T('§A-2 받는 때 — 앱 시작(recBoot + 첫 syncRecords 겹침) %s번 · 받는 중에 겹쳐 부르면 한 번(%s) · syncRecords 가 돌면 한 번 더(%s)' % (a2.get('gets0'), a2.get('both'), a2.get('gets1')),
      a2.get('gets0') == 1 and a2.get('both') == 2 and a2.get('gets1') == 3 and not a2.get('err'), a2)
    # ══ J19
    G19 = RES.get('j19') or {}
    I('J19 흐름 — ① 새 판 A 가 정정을 올림 ② 옛 판 B(f8cec7a) 가 그 원격을 받아 제 변경과 함께 올림 ③ A 가 다시 맞춤 ④ 정정 없는 새 판 C',
      {k: G19.get(k) for k in ('P1', 'P2', 'Blocal', 'P3', 'A2', 'C1', 'C2', 'exc')})
    T('J19 ① 새 판이 올린 기록에 data["jopangi.clfix"].T901 · u 도장', g(G19, 'P1', 'data') is True and g(G19, 'P1', 'fix', 'T901', 'done') is False and g(G19, 'P1', 'u'), G19.get('P1'))
    T('J19 ② 옛 판 기기는 제 저장소에 jopangi.clfix 를 만들지 않는다(모르는 키 · 병합이 건드리지 않는다)', G19.get('Blocal') is None, G19.get('Blocal'))
    T('J19 ② 옛 판 기기는 정정을 **지우지 않는다** — 묘비(gone) 0 · u 도장은 남는다(합집합)', g(G19, 'P2', 'gone') == [] and bool(g(G19, 'P2', 'u')), G19.get('P2'))
    I('J19 ② 잰 것 — 옛 판(f8cec7a) 기기가 올린 기록: data["jopangi.clfix"] %s · u 도장 %s · data 키 %s개(옛 recPayload 는 제 SYNC_KEYS 29키만 담는다)'
      % ('있음' if g(G19, 'P2', 'data') else '**없음(빠짐)**', '있음' if g(G19, 'P2', 'u') else '없음', g(G19, 'P2', 'keys')), G19.get('P2'))
    T('J19 ② 옛 판 기기가 올린 파일의 data 에도 jopangi.clfix 가 남는가(민법 G16 과 같은 잣대 · 빠지면 보고에 그대로)', g(G19, 'P2', 'data') is True, G19.get('P2'))
    T('J19 ③ 새 판 기기 A 가 다음 맞추기에서 되살려 올린다(올림 %s · 옛 판 기기의 변경도 그대로 %s)' % (g(G19, 'P3', 'puts'), g(G19, 'P3', 'tag')),
      g(G19, 'P3', 'data') is True and g(G19, 'P3', 'fix', 'T901', 'md') == 'A 기기 정정본' and g(G19, 'P3', 'puts') == 1 and g(G19, 'P3', 'tag') == {'important': 1}, G19.get('P3'))
    T('J19 ④ 새 판 기기 C — 빠진 원격에서는 못 받고(%s) 되살린 원격에서 받는다(%s)' % ('T901 없음' if 'T901' not in (G19.get('Clocal1') or '') else 'T901 있음', 'T901' if G19.get('Clocal2') and 'T901' in G19.get('Clocal2') else G19.get('Clocal2')),
      'T901' not in (G19.get('Clocal1') or '') and 'A 기기 정정본' in (G19.get('Clocal2') or ''), [G19.get('Clocal1'), G19.get('Clocal2')])
    T('J19 JS 오류 0(세 기기)', not any(G19.get('err') or [[1]]), G19.get('err'))
    return finish(L)


def finish(L):
    for l in L:
        print('   ' + l)
    p = sum(1 for l in L if l.startswith('PASS')); f = sum(1 for l in L if l.startswith('FAIL'))
    print('\n합계  PASS %d · FAIL %d' % (p, f))
    io.open(os.path.join(HERE, '_harness_jo_claude_answers_result.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n\n합계  PASS %d · FAIL %d\n' % (p, f))
    return f


if __name__ == '__main__':
    main()
