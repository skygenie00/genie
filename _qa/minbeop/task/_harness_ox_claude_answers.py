# -*- coding: utf-8 -*-
"""민법OX 「Claude 답」 칸 세 자리 — _task_ox_claude_answers §G(G1~G17).

  NEW  = genie 작업트리 minbeop/index.html (고친 판)
  BASE = `846dc1e` 의 같은 파일(1,063,650 B · md5 94c5ffa1…) — 헛잣대 · G16 에서는 「옛 판 기기」
  실데이터 = studyplandata minbeop/기록.json · 문항마스터.json(5,548) · Claude 답 = 이 폴더 claude.json(M001 → Q0480)
  엔진 = playwright webkit · chromium — has_touch · is_mobile · 아이패드 1024×768
  누름 = touchscreen.tap(진짜 터치) · 끌기 = chromium CDP 터치(끝에서 멈춤) / webkit 신뢰 마우스(도구 한계)
  網 = 같은 출처 + cdn.tailwindcss.com 만 · GitHub 는 SEED 가 대답(claude.json = 파일·404·500 · 기록.json = 메모리 원격 GET·PUT)

쓰기 : python _harness_ox_claude_answers.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
_NR = _roots.need_n('민법 task 재료(claude.json)')   # env_lanes_fix(9/29) — N: 작업 폴더 · 없으면(클라우드) 「N: 필요 — 클라우드 불가(…)」 종료 코드 3
import hashlib, http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

GENIE = _roots.genie()
SPD = _roots.spd()
HERE = os.path.dirname(os.path.abspath(__file__))
TASKDIR = os.path.join(_NR, 'minbeop', 'task')
CLJSON = os.path.join(TASKDIR, 'claude.json')
WORK = os.path.join(tempfile.gettempdir(), 'h_claude_answers')
REL = 'minbeop/index.html'
BASE_REV = '846dc1e'
BASE_MD5 = '94c5ffa172b34575835c1d6848c5f24a'
TESTS = io.open(os.path.join(HERE, '_harness_ox_claude_answers_tests.js'), encoding='utf-8').read()
IPAD_UA = ('Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 '
           '(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__ALERTS=[];window.alert=function(m){__ALERTS.push(String(m));};
window.confirm=function(){return true;};window.prompt=function(){return null;};
(function(){var nf=window.fetch.bind(window);window.__CLMODE='file';window.__CLGETS=0;
window.fetch=function(u,o){o=o||{};var s=String((u&&u.url)||u);
 if(/\/contents\/minbeop\/claude\.json/.test(s)){window.__CLGETS++;
  if(window.__CLMODE==='404')return Promise.resolve(new Response('{"message":"Not Found"}',{status:404}));
  if(window.__CLMODE==='500')return Promise.resolve(new Response('{"message":"harness 500"}',{status:500}));
  return nf('/claude.json',{cache:'no-store'});}
 if(/\/contents\/minbeop\/(%EA%B8%B0%EB%A1%9D|기록)\.json/.test(s)){var R=window.__REMOTE;
  if((o.method||'GET')==='PUT'){var b=JSON.parse(o.body||'{}');if(!R)R=window.__REMOTE={text:null,sha:null,puts:0};
   if(R.sha&&b.sha!==R.sha)return Promise.resolve(new Response('{"message":"conflict"}',{status:409}));
   R.text=decodeURIComponent(escape(atob(b.content)));R.puts=(R.puts||0)+1;R.sha='H'+R.puts+'_'+Date.now();
   return Promise.resolve(new Response(JSON.stringify({content:{sha:R.sha}}),{status:200,headers:{'Content-Type':'application/json'}}));}
  if(!R||R.text==null)return Promise.resolve(new Response('{"message":"Not Found"}',{status:404}));
  var acc=((o.headers||{}).Accept||'');
  if(acc.indexOf('raw')>=0)return Promise.resolve(new Response(R.text,{status:200}));
  return Promise.resolve(new Response(JSON.stringify({sha:R.sha}),{status:200,headers:{'Content-Type':'application/json'}}));}
 if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));
 return nf(u,o);};})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
localStorage.clear();
</script>"""
READY = ("typeof buildQuizData==='function'&&typeof startQuiz==='function'&&typeof openQPopup==='function'"
         "&&typeof dbPut==='function'&&!!window.__HZT")


def git(*a):
    return subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def J(s):
    try:
        return json.loads(s) if isinstance(s, str) else s
    except Exception:
        return {'__raw': str(s)[:300]}


def serve(tag, src):
    OUT = os.path.join(WORK, 'srv_' + tag); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    b = src.index('<body'); bb = src.index('>', b) + 1
    html = src[:bb] + SEED + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + TESTS + '\n</script>\n' + html[e:]
    io.open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)
    MAP = {'/rec.json': os.path.join(SPD, 'minbeop', '기록.json'), '/master.json': os.path.join(SPD, 'minbeop', '문항마스터.json'),
           '/claude.json': CLJSON}

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=OUT, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            return MAP.get(p) or super().translate_path(path)

        def log_message(self, *a, **k):
            pass
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


def route_filter(route):
    u = route.request.url
    if u.startswith('http://127.0.0.1') or u.startswith('https://cdn.tailwindcss.com'):
        return route.continue_()
    return route.abort()


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


def open_page(pw_br, eng, tag, src, extra_tag=''):
    srv, port = serve('%s_%s%s' % (tag, eng, extra_tag), src)
    ctx = pw_br.new_context(viewport={'width': 1024, 'height': 768}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=IPAD_UA)
    ctx.route('**/*', route_filter)
    pg = ctx.new_page()
    errs = {'page': [], 'console': []}
    pg.on('pageerror', lambda e: errs['page'].append(str(e)[:240]))
    pg.on('console', lambda m: errs['console'].append(m.text[:240]) if m.type == 'error' else None)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
    pg.wait_for_function(READY, timeout=120000)
    return S(pg, eng), srv, ctx, errs


def main_scenario(s, has):
    """G1~G13 · G17 — NEW 는 전부, BASE 는 헛잣대가 되는 것만"""
    pg, R = s.pg, {}
    R['setup'] = s.js("__HZT.setup(true)")
    R['load'] = s.js("__HZT.load()")
    R['G1'] = s.js("u=>__HZT.card(u)", 'Q0480')
    R['G2card'] = s.js("u=>__HZT.card(u)", 'Q5514')
    R['G2pop'] = s.js("u=>__HZT.pop(u)", 'Q2396')
    R['G6'] = s.js("t=>__HZT.search(t)", '2002다21592')
    R['G7'] = s.js("t=>__HZT.search(t)", '정착물')
    R['G8'] = s.js("__HZT.dist()")
    if has:
        cb = (R['G8'] or {}).get('cBtn') or {}
        R['G8tap'] = s.tap(cb.get('at'))
        pg.wait_for_timeout(300)
        R['G8after'] = s.js("__HZT.distState()")
        R['G9'] = s.js("__HZT.toggles()")
        R['G10'] = s.js("([k,o])=>__HZT.list(k,o)", ['민법총칙 · 4. 권리의 객체', False])
        R['G10only'] = s.js("([k,o])=>__HZT.list(k,o)", ['민법총칙 · 4. 권리의 객체', True])
    # G11 정리 창 — 첫 화면 📋 단추를 톡
    jb = s.js("__HZT.jnBtn()")
    R['G11tapJn'] = s.tap(jb)
    pg.wait_for_timeout(600)
    R['G11'] = s.js("__HZT.jnState()")
    R['G11ans1'] = s.tap(s.js("([u,w])=>__HZT.jnPart(u,w)", ['Q0480', 'ans'])); pg.wait_for_timeout(250)
    R['G11open'] = s.js("__HZT.jnState()")
    R['G11ans2'] = s.tap(s.js("([u,w])=>__HZT.jnPart(u,w)", ['Q0480', 'ans'])); pg.wait_for_timeout(250)
    R['G11close'] = s.js("__HZT.jnState()")
    if has:
        R['G11chip'] = s.tap(s.js("([u,w])=>__HZT.jnPart(u,w)", ['Q0480', 'chip'])); pg.wait_for_timeout(300)
        R['G11win'] = s.js("__HZT.win('Q0480')")
        R['G11sizeJn'] = s.js("__HZT.sizeJn()")
        # G3 답 없는 카드 → 톡 → 「아직 답 없음」 창
        R['G3'] = s.js("u=>__HZT.card(u)", 'Q0706')
        R['G3tap'] = s.tap(((R['G3'] or {}).get('btn') or {}).get('at')); pg.wait_for_timeout(300)
        R['G3win'] = s.js("__HZT.win('Q0706')")
        # G4 Q0480 카드 → 톡 → Claude 창 · 끌기 · 크기
        c = s.js("u=>__HZT.card(u)", 'Q0480')
        R['G4tap'] = s.tap(((c or {}).get('btn') or {}).get('at')); pg.wait_for_timeout(300)
        R['G4win'] = s.js("__HZT.win('Q0480')")
        hp = s.js("([u,p])=>__HZT.winPart(u,p)", ['Q0480', 'head'])
        if hp and hp.get('on'):
            R['G4drag'] = s.drag(hp['cx'], hp['cy'], hp['cx'] + 70, hp['cy'] - 60); pg.wait_for_timeout(300)   # 위로 — 아래로 끌면 창 아래가 화면 밖(손잡이·본문 단추를 못 누른다)
        R['G4moved'] = s.js("__HZT.win('Q0480')")
        gp = s.js("([u,p])=>__HZT.winPart(u,p)", ['Q0480', 'grip'])
        R['G4size0'] = s.js("__HZT.size()")
        if gp and gp.get('on'):
            R['G4resize'] = s.drag(gp['cx'], gp['cy'], gp['cx'] + 60, gp['cy'] + 30); pg.wait_for_timeout(400)
        R['G4size'] = s.js("__HZT.size()")
        R['G4after'] = s.js("__HZT.win('Q0480')")
        # G5 창 본문 Q5514 → 문항 팝업
        R['G5tap'] = s.tap(s.js("([u,sl,t])=>__HZT.winBtn(u,sl,t)", ['Q0480', '[data-clmdbox] button.uid', 'Q5514'])); pg.wait_for_timeout(300)
        R['G5'] = s.js("k=>__HZT.hasWin(k)", 'q-Q5514')
        # G12 정정 저장
        R['G12edit'] = s.tap(s.js("([u,sl,t])=>__HZT.winBtn(u,sl,t)", ['Q0480', '.clfixbar button', '✎ 정정'])); pg.wait_for_timeout(200)
        R['G12ta'] = s.js("([u,m])=>__HZT.setTa(u,m)", ['Q0480', 'add'])
        R['G12save'] = s.tap(s.js("([u,sl,t])=>__HZT.winBtn(u,sl,t)", ['Q0480', '.clfixbar button', '저장 (정정으로)'])); pg.wait_for_timeout(500)
        R['G12fix'] = s.js("__HZT.fix()")
        R['G12win'] = s.js("__HZT.win('Q0480')")
        R['G12card'] = s.js("u=>__HZT.card(u)", 'Q0480')
        R['G12search'] = s.js("t=>__HZT.search(t)", '하네스정정줄')
        # G13 20,001자 — 다시 창을 연다(card() 가 창을 닫았다)
        c = s.js("u=>__HZT.card(u)", 'Q0480')
        s.tap(((c or {}).get('btn') or {}).get('at')); pg.wait_for_timeout(300)
        R['G13edit'] = s.tap(s.js("([u,sl,t])=>__HZT.winBtn(u,sl,t)", ['Q0480', '.clfixbar button', '✎ 정정'])); pg.wait_for_timeout(200)
        R['G13fix0'] = s.js("__HZT.fix()")
        R['G13ta'] = s.js("([u,m])=>__HZT.setTa(u,m)", ['Q0480', 'long'])
        R['G13save'] = s.tap(s.js("([u,sl,t])=>__HZT.winBtn(u,sl,t)", ['Q0480', '.clfixbar button', '저장 (정정으로)'])); pg.wait_for_timeout(400)
        R['G13win'] = s.js("__HZT.win('Q0480')")
        R['G13fix1'] = s.js("__HZT.fix()")
        R['G13cancel'] = s.tap(s.js("([u,sl,t])=>__HZT.winBtn(u,sl,t)", ['Q0480', '.clfixbar button', '취소'])); pg.wait_for_timeout(200)
        R['G13after'] = s.js("__HZT.win('Q0480')")
    R['G17'] = s.js("__HZT.parse()")
    R['err'] = s.js("__HZT.errs()")
    return R


def run_main(eng, tag, src):
    with sync_playwright() as pw:
        br = getattr(pw, eng).launch()
        s, srv, ctx, errs = open_page(br, eng, tag, src)
        try:
            R = main_scenario(s, tag == 'NEW')
        except Exception as e:
            R = {'exc': str(e)[:600]}
        R['pageerror'], R['consoleError'] = errs['page'], errs['console']
        br.close(); srv.shutdown()
    return R


def run_g14_g15(src):
    R = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for name, token, mode in (('G14', True, '404'), ('G15', False, 'file'), ('G15net', True, '500')):
            s, srv, ctx, errs = open_page(br, 'chromium', 'NEW', src, '_' + name)
            D = {}
            try:
                D['setup'] = s.js("t=>__HZT.setup(t)", token)
                s.pg.evaluate("m=>{window.__CLMODE=m}", mode)
                D['load'] = s.js("__HZT.load()")
                D['card'] = s.js("u=>__HZT.card(u)", 'Q0480')
                D['vis'] = s.js("__HZT.visibleClBtns()"); D['all'] = s.js("__HZT.allClBtns()")
                D['pop'] = s.js("u=>__HZT.pop(u)", 'Q0480')
                s.js("__HZT.clearStatus()")
                D['load2'] = s.js("__HZT.load()")          # 두 번째 실패 — 문구가 다시 안 뜨는가(한 번만)
                D['err'] = s.js("__HZT.errs()")
            except Exception as e:
                D['exc'] = str(e)[:400]
            D['pageerror'], D['consoleError'] = errs['page'], errs['console']
            R[name] = D
            ctx.close(); srv.shutdown()
        # §A-2 받는 때 — 받는 중 겹침은 한 번 · syncRecords 가 돌면 한 번 더
        s, srv, ctx, errs = open_page(br, 'chromium', 'NEW', src, '_A2')
        D = {}
        try:
            s.js("t=>__HZT.setup(t)", True)
            D['gets0'] = s.pg.evaluate("window.__CLGETS")
            D['both'] = s.pg.evaluate("(async()=>{const a=clLoad(), b=clLoad(); await a; await b; return window.__CLGETS})()")
            s.pg.evaluate("()=>{window.__REMOTE=null}")      # 원격 기록 없음(404) — 맞추기가 끝까지 돈다
            D['sync'] = s.js("f=>__HZT.sync(f)", False)
            D['gets1'] = s.pg.evaluate("window.__CLGETS")
            D['err'] = s.js("__HZT.errs()")
        except Exception as e:
            D['exc'] = str(e)[:400]
        R['A2'] = D
        ctx.close(); srv.shutdown()
        br.close()
    return R


def run_g16(base, new):
    """옛 판 기기(BASE)가 ox_cl_fix 가 든 원격 기록을 받아 올릴 때 · 새 판 기기가 다음 동기화에서"""
    R = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        A, sa, ca, ea = open_page(br, 'chromium', 'NEW', new, '_A')
        B, sb, cb, eb = open_page(br, 'chromium', 'BASE', base, '_B')
        C, sc, cc, ec = open_page(br, 'chromium', 'NEW', new, '_C')
        try:
            for x in (A, B, C):
                x.js("t=>__HZT.setup(t)", True)
            rec0 = A.pg.evaluate("__HZT.recText()")          # 실물 기록.json 글자 그대로
            # ① 새 판 기기 A — 정정 하나 · 원격(실물 기록)과 맞춰 올린다
            A.js("__HZT.load()")
            A.pg.evaluate("m=>__HZT.fixPut(m)", 'A 기기 정정본')
            A.js("__HZT.stamp()")
            A.pg.evaluate("([t,h])=>__HZT.remoteSet(t,h)", [rec0, 'S0'])
            R['A1'] = A.js("f=>__HZT.sync(f)", True)
            P1 = J(A.pg.evaluate("__HZT.remoteGet()"))['text']
            p1 = json.loads(P1)
            R['P1'] = {'data': 'ox_cl_fix' in p1['data'], 'fix': p1['data'].get('ox_cl_fix'), 'u': p1['u'].get('ox_cl_fix|M001')}
            # ② 옛 판 기기 B — P1 을 받아 합치고, 제 변경 하나를 올린다(force)
            B.js("__HZT.stamp()")
            B.pg.evaluate("()=>__HZT.tagToggle()"); B.js("__HZT.stamp()")
            B.pg.evaluate("([t,h])=>__HZT.remoteSet(t,h)", [P1, 'S1'])
            R['B1'] = B.js("f=>__HZT.sync(f)", True)
            P2 = J(B.pg.evaluate("__HZT.remoteGet()"))['text']
            p2 = json.loads(P2)
            R['P2'] = {'data': 'ox_cl_fix' in p2['data'], 'u': p2['u'].get('ox_cl_fix|M001'), 'keys': len(p2['data'])}
            R['Blocal'] = B.pg.evaluate("__HZT.ls('ox_cl_fix')")
            # ③ 새 판 기기 A — P2 를 받는다(강제 아님)
            A.pg.evaluate("([t,h])=>__HZT.remoteSet(t,h)", [P2, 'S2'])
            R['A2'] = A.js("f=>__HZT.sync(f)", False)
            P3 = J(A.pg.evaluate("__HZT.remoteGet()"))
            p3 = json.loads(P3['text'])
            R['P3'] = {'puts': P3.get('puts'), 'data': 'ox_cl_fix' in p3['data'], 'fix': p3['data'].get('ox_cl_fix'), 'tag': (p3['data'].get('ox_q_tags') or {}).get('Q0706')}
            R['Alocal'] = A.pg.evaluate("__HZT.ls('ox_cl_fix')")
            # ④ 새 판 기기 C(정정 없음) — P2 를 먼저 · 그다음 P3
            C.js("__HZT.load()"); C.js("__HZT.stamp()")
            C.pg.evaluate("([t,h])=>__HZT.remoteSet(t,h)", [P2, 'S2'])
            R['C1'] = C.js("f=>__HZT.sync(f)", False)
            R['Clocal1'] = C.pg.evaluate("__HZT.ls('ox_cl_fix')")
            C.pg.evaluate("([t,h])=>__HZT.remoteSet(t,h)", [P3['text'], 'S3'])
            R['C2'] = C.js("f=>__HZT.sync(f)", False)
            R['Clocal2'] = C.pg.evaluate("__HZT.ls('ox_cl_fix')")
            R['err'] = [A.js("__HZT.errs()"), B.js("__HZT.errs()"), C.js("__HZT.errs()")]
        except Exception as e:
            R['exc'] = str(e)[:600]
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
    RES = {}
    for eng in ('webkit', 'chromium'):
        for tag, src in (('BASE', base), ('NEW', new)):
            k = '%s/%s' % (eng, tag)
            t0 = time.time(); print('… ' + k, flush=True)
            RES[k] = run_main(eng, tag, src)
            print('   %.1fs%s' % (time.time() - t0, ('  EXC ' + RES[k]['exc']) if RES[k].get('exc') else ''), flush=True)
    t0 = time.time(); print('… G14·G15·A-2', flush=True); RES['g1415'] = run_g14_g15(new); print('   %.1fs' % (time.time() - t0), flush=True)
    t0 = time.time(); print('… G16', flush=True); RES['g16'] = run_g16(base, new); print('   %.1fs' % (time.time() - t0), flush=True)
    json.dump(RES, io.open(os.path.join(WORK, 'raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    L = []
    T = lambda n, c, i=None: L.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c or i is None else ' | ' + json.dumps(i, ensure_ascii=False)[:700]))
    I = lambda n, v: L.append('INFO | ' + n + ' | ' + json.dumps(v, ensure_ascii=False)[:1400])
    g = lambda d, *ks: __import__('functools').reduce(lambda a, k: (a.get(k) if isinstance(a, dict) else (a[k] if isinstance(a, list) and isinstance(k, int) and -len(a) <= k < len(a) else None)), ks, d)
    ORANGE, GRAY = 'rgb(180, 83, 9)', 'rgb(107, 114, 128)'

    # ══ 소스 · 파일
    bb, nb = base.encode('utf-8'), new.encode('utf-8')
    T('착수 %s = 지시서 G0-1 (1,063,650 B · md5 94c5ffa1…)' % BASE_REV, len(bb) == 1063650 and hashlib.md5(bb).hexdigest() == BASE_MD5, [len(bb), hashlib.md5(bb).hexdigest()])
    T('G17 NEW CRLF 0 · U+FFFD 0 (%d B · md5(LF) %s)' % (len(nb), hashlib.md5(nb).hexdigest()), b'\r\n' not in nb and '\ufffd' not in new)
    ch = [l for l in git('status', '--porcelain').decode('utf-8').split('\n') if l.strip()]
    T('genie 작업트리 바뀐 파일 = minbeop/index.html 하나 %s' % ch, ch == [' M ' + REL], ch)
    sk = lambda s: re.findall(r"'([^']+)'", re.search(r'const SYNC_KEYS = \[(.+?)\];', s, re.S).group(1))
    T('§E-1 SYNC_KEYS = 옛 17키 그대로 + 끝에 ox_cl_fix (18키)', sk(new) == sk(base) + ['ox_cl_fix'] and len(sk(new)) == 18, [len(sk(base)), sk(new)[-3:]])
    T('§A-2 받는 길 — MB_CL_PATH 상수 · ghRaw(같은 저장소·raw·토큰) · recBoot 한 번 · syncRecords 안 한 번 · localStorage·IndexedDB 에 안 넣는다',
      "const MB_CL_PATH = 'minbeop/claude.json';" in new and 'await ghRaw(MB_CL_PATH)' in new
      and re.search(r'function recBoot\(\) \{\n\s+recPaint\(\);\n\s+stampAll\(\);\n\s+clLoad\(\);', new) is not None
      and re.search(r"if \(navigator\.onLine === false\) \{ recPaint\(\); return; \}\n\s+clLoad\(\);", new) is not None
      and not re.search(r"(setItem|lsPut|dbPut)\([^)]*(CL_DATA|claude\.json|MB_CL_PATH)", new))
    T('§F 앱이 claude.json 을 쓰는 길 0(PUT 은 기록.json·settings 뿐 · MB_CL_PATH 를 쓰는 곳은 ghRaw 하나)', new.count('MB_CL_PATH') == 2 and 'ghPutJson(MB_CL_PATH' not in new, new.count('MB_CL_PATH'))
    T('§D jnAnsToggle — 같은 부모의 data-jnans 를 찾는다(nextElementSibling 버림)',
      "btn.parentElement.querySelector(':scope > [data-jnans]')" in new and 'const box = btn && btn.nextElementSibling;' not in new)

    # ══ 세션 부트
    for eng in ('webkit', 'chromium'):
        for tag in ('BASE', 'NEW'):
            d = RES.get('%s/%s' % (eng, tag)) or {}
            errs = (d.get('err') or []) + (d.get('pageerror') or [])
            T('[%s] %s 부트 · 문항 %s · JS 오류 %d' % (eng, tag, g(d, 'setup', 'q'), len(errs)), g(d, 'setup', 'q') == 5548 and not d.get('exc') and (tag == 'BASE' or not errs),
              [d.get('exc'), errs[:4]])
    # ══ G1~G13 (두 엔진)
    for eng in ('webkit', 'chromium'):
        n, b = RES.get(eng + '/NEW') or {}, RES.get(eng + '/BASE') or {}
        p = '[%s] ' % eng
        ld = n.get('load') or {}
        T(p + '§A 받기 — CL_STATE ok · 직접 %s · 언급 %s' % (ld.get('by'), sorted((ld.get('ment') or {}).keys())),
          ld.get('state') == 'ok' and ld.get('by') == {'Q0480': ['M001']} and sorted((ld.get('ment') or {}).keys()) == ['Q0474', 'Q2275', 'Q2396', 'Q4336', 'Q5514'], ld)
        b1 = g(n, 'G1', 'btn') or {}
        T(p + 'G1 Q0480 카드 — 「✏️ 연결」 바로 앞(%s) 주황 「%s」 · 11px · 테두리·바탕 없음 · 높이 %s ↔ 연결 %s'
          % (g(n, 'G1', 'next'), b1.get('text'), g(b1, 'at', 'h'), g(n, 'G1', 'lnk', 'at', 'h')),
          b1.get('text') == 'Claude1' and b1.get('color') == ORANGE and b1.get('fs') == '11px' and g(n, 'G1', 'next') == '✏️ 연결'
          and b1.get('bd', '').startswith('0px') and b1.get('bg') in ('rgba(0, 0, 0, 0)', 'transparent')
          and abs((g(b1, 'at', 'h') or 0) - (g(n, 'G1', 'lnk', 'at', 'h') or 99)) <= 1.5 and g(n, 'G1', 'n') == 1, n.get('G1'))
        T(p + 'G1 헛잣대 BASE — 같은 카드에 Claude 단추 없음', g(b, 'G1', 'card') is True and g(b, 'G1', 'btn') is None and g(b, 'G1', 'n') == 0, b.get('G1'))
        b2 = g(n, 'G2card', 'btn') or {}
        T(p + 'G2 Q5514 카드 — 회색 「Claude」 + 주황 「↩」(10px)', b2.get('text') == 'Claude↩' and b2.get('color') == GRAY
          and g(b2, 'kids', 0, 't') == '↩' and g(b2, 'kids', 0, 'color') == ORANGE and g(b2, 'kids', 0, 'fs') == '10px', b2)
        b2p = g(n, 'G2pop', 'btn') or {}
        T(p + 'G2 Q2396 팝업 — 「✏️ 연결」 바로 앞 · 회색 「Claude」 + 주황 「↩」 · 높이 %s ↔ 연결 %s' % (g(b2p, 'at', 'h'), g(n, 'G2pop', 'lnk', 'at', 'h')),
          b2p.get('text') == 'Claude↩' and b2p.get('color') == GRAY and g(n, 'G2pop', 'nextIsLink') is True and g(b2p, 'kids', 0, 'color') == ORANGE
          and abs((g(b2p, 'at', 'h') or 0) - (g(n, 'G2pop', 'lnk', 'at', 'h') or 99)) <= 1.5, n.get('G2pop'))
        T(p + 'G3 Q0706 카드 — 회색 「Claude」 · 톡 → 「아직 없다」 창', g(n, 'G3', 'btn', 'text') == 'Claude' and g(n, 'G3', 'btn', 'color') == GRAY
          and n.get('G3tap') is True and g(n, 'G3win', 'win') is True and '아직 없다' in (g(n, 'G3win', 'note') or ''), [n.get('G3'), n.get('G3win')])
        w4 = n.get('G4win') or {}
        T(p + 'G4 Q0480 톡 → Claude 창(oxwin · 손잡이 .oxwin-grip) · 제목 「%s」' % w4.get('title'),
          n.get('G4tap') is True and w4.get('win') is True and w4.get('grip') is True and (w4.get('title') or '').startswith('Claude · 6번 · Q0480'), w4)
        T(p + 'G4 몸통 — 머리 %s · 오른쪽 끝 uid 단추 · 소제목 %s · 표 %s(머리칸 %s) · 목록 %s줄 · 핵심 줄 · ✎ 정정 · 원문 태그 흘림 0'
          % (w4.get('head'), w4.get('h4'), w4.get('tables'), w4.get('th'), w4.get('li')),
          (w4.get('head') or [None])[0] == 'M001' and '2026-09-18 · 민총 4. 권리의 객체' in (w4.get('head') or []) and w4.get('headUidBtn') is True
          and w4.get('h4') == ['A.', '근거'] and w4.get('tables') == 2 and w4.get('th') == 6 and w4.get('li') >= 6 and w4.get('ul') == 'disc'
          and (w4.get('core') or '').startswith('핵심 — 지하냐 지상이냐가') and w4.get('fixBtn') == '✎ 정정' and w4.get('rawTags') is False
          and w4.get('uidBtns') == ['Q0474', 'Q4336', 'Q5514', 'Q2396', 'Q2275'] and w4.get('bold', 0) >= 3, w4)
        mv0, mv1 = w4.get('rect') or [0, 0], g(n, 'G4moved', 'rect') or [0, 0]
        sz = J(n.get('G4size') or 'null') or {}
        T(p + 'G4 머리를 끌면 옮겨진다(%s → %s · %s) · 모서리를 끌면 크기가 바뀌고 oxwin.size.claude = %s'
          % (mv0[:2], mv1[:2], n.get('G4drag'), sz),
          abs(mv1[0] - mv0[0]) > 20 and abs(mv1[1] - mv0[1]) > 20 and isinstance(sz, dict) and sz.get('w') and sz.get('h')
          and abs(sz.get('w') - (g(n, 'G4after', 'rect') or [0, 0, 0])[2]) <= 2, [mv0, mv1, n.get('G4size0'), sz, g(n, 'G4after', 'rect')])
        T(p + 'G5 창 본문 Q5514 톡 → openQPopup(\'Q5514\') 창', n.get('G5tap') is True and n.get('G5') is True, [n.get('G5tap'), n.get('G5')])
        fx = J(n.get('G12fix') or 'null') or {}
        T(p + 'G12 ✎ 정정 → textarea(md) → 저장 → ox_cl_fix.M001 done:false · md 에 고친 줄',
          n.get('G12edit') is True and g(n, 'G12ta', 'len') and n.get('G12save') is True and g(fx, 'M001', 'done') is False
          and '하네스정정줄' in (g(fx, 'M001', 'md') or '') and isinstance(g(fx, 'M001', 'ts'), int), [n.get('G12ta'), fx and {k: (v if k != 'md' else len(v)) for k, v in (fx.get('M001') or {}).items()}])
        T(p + 'G12 창 딱지 「%s」 · 카드 단추 「%s」 · SYNC_KEYS %s키 · 검색이 정정본으로(「하네스정정줄」 %s)'
          % (g(n, 'G12win', 'fixtag'), g(n, 'G12card', 'btn', 'text'), len(g(n, 'setup', 'syncKeys') or []), g(n, 'G12search', 'count')),
          (g(n, 'G12win', 'fixtag') or '').startswith('정정 · 반영 전 · ') and g(n, 'G12card', 'btn', 'text') == 'Claude1정정'
          and len(g(n, 'setup', 'syncKeys') or []) == 18 and g(n, 'G12search', 'count') == '1건'
          and 'Claude' in (g(n, 'G12search', 'rows', 0, 'badges') or []), [n.get('G12win'), n.get('G12card'), n.get('G12search')])
        T(p + 'G13 20,001자 → 저장 안 됨(ox_cl_fix 그대로) · 「%s」 · 취소하면 읽기 판' % g(n, 'G13win', 'msg'),
          g(n, 'G13ta', 'len') == 20001 and g(n, 'G13win', 'msg') == '20,000자까지 · 지금 20,001자' and n.get('G13fix0') == n.get('G13fix1')
          and g(n, 'G13win', 'ta') is True and g(n, 'G13after', 'ta') is False, [n.get('G13ta'), g(n, 'G13win', 'msg')])
        # G6 · G7 검색
        s6, s6b = n.get('G6') or {}, b.get('G6') or {}
        T(p + 'G6 「2002다21592」 → %s · Q0480 · 딱지 %s (BASE %s)' % (s6.get('count'), g(s6, 'rows', 0, 'badges'), s6b.get('count')),
          s6.get('count') == '1건' and g(s6, 'rows', 0, 'id') == 'Q0480' and g(s6, 'rows', 0, 'badges') == ['Claude'] and g(s6, 'rows', 0, 'cl') is True
          and g(s6, 'rows', 0, 'blue') is False and s6b.get('count') == '0건', [s6, s6b])
        s7 = n.get('G7') or {}
        T(p + 'G7 「정착물」 → %s · Q0480 · 딱지 %s' % (s7.get('count'), g(s7, 'rows', 0, 'badges')),
          s7.get('count') == '1건' and g(s7, 'rows', 0, 'id') == 'Q0480' and g(s7, 'rows', 0, 'badges') == ['근거', '댓글', 'Claude'], s7)
        I(p + 'G7 헛잣대 BASE(같은 말 · 딱지 없는 옛 줄)', b.get('G7'))
        # G8 · G9 단원 목록
        d8, d8b = n.get('G8') or {}, b.get('G8') or {}
        T(p + 'G8 머리 「%s」 · C 단추 주황·밑점선' % d8.get('head'),
          (d8.get('head') or '').endswith('· ! 8 · C1') and g(d8, 'cBtn', 't') == 'C1' and g(d8, 'cBtn', 'off') is False
          and g(d8, 'cBtn', 'color') == ORANGE and g(d8, 'cBtn', 'bb') == 'dashed', d8)
        T(p + 'G8 헛잣대 BASE — 머리 「%s」(C 없음)' % d8b.get('head'), (d8b.get('head') or '').endswith('· ! 8') and d8b.get('cBtn') is None, d8b)
        a8 = n.get('G8after') or {}
        T(p + 'G8 C1 톡 → 단원 %s개(%s) · 머리 「%s」 · 「!」 꺼짐 %s' % (a8.get('units'), a8.get('clUnits'), a8.get('head'), a8.get('flags')),
          n.get('G8tap') is True and a8.get('units') == 1 and a8.get('clUnits') == ['민법총칙 · 4. 권리의 객체 C1'] and a8.get('flags') == [False, True]
          and (a8.get('head') or '').startswith('🔗 근거 C1건 · 1개 단원 — Claude 답이 있는 것만 보는 중') and a8.get('headBg') == 'rgb(255, 247, 237)', a8)
        t9 = n.get('G9') or {}
        T(p + 'G9 「!」 켠 뒤 C → [! , C] = %s · C 켠 뒤 「!」 → %s · 「문제」 로 가면 둘 다 꺼짐 %s' % (t9.get('afterBangThenC'), t9.get('afterCThenBang'), t9.get('qOff')),
          t9.get('afterBang') == [True, False] and t9.get('afterBangThenC') == [False, True] and t9.get('afterCThenBang') == [True, False] and t9.get('qOff') == [False, False], t9)
        l10, l10o = n.get('G10') or {}, n.get('G10only') or {}
        T(p + 'G10 권리의 객체 목록(%s행) — Q0480 근거 상자 아래 Claude 상자 「%s」' % (l10.get('rows'), (g(l10, 'q0480', 'cl') or '')[:30]),
          g(l10, 'q0480', 'blue') is True and (g(l10, 'q0480', 'cl') or '').startswith('C1 · 지하냐 지상이냐가') and l10.get('clBoxes') == 1
          and g(l10, 'q0480', 'clStyle') == ['rgb(255, 247, 237)', ORANGE, 'rgb(253, 186, 116)'], l10)
        T(p + 'G10 Claude 만 보기 — %s행 · 근거 상자 없이 「%s」 · 머리 「%s」' % (l10o.get('rows'), (g(l10o, 'q0480', 'cl') or '')[:24], l10o.get('head')),
          l10o.get('rows') == 1 and g(l10o, 'q0480', 'blue') is False and (g(l10o, 'q0480', 'cl') or '').startswith('Claude · 지하냐') and (l10o.get('head') or '').endswith('· Claude 답만'), l10o)
        # G11 정리 창
        j, jb = n.get('G11') or {}, b.get('G11') or {}
        T(p + 'G11 정리 창(%s행) — Q0480 「정답·해설 ▸」 바로 뒤 「%s」 · 글자만 주황 11px 굵게' % (j.get('rows'), g(j, 'q0480', 'chip')),
          j.get('jn') is True and g(j, 'q0480', 'chip') == 'C1' and g(j, 'q0480', 'chipAfterAns') is True
          and g(j, 'q0480', 'chipStyle') == [ORANGE, '11px', '700', '0px', 'rgba(0, 0, 0, 0)'], j)
        I(p + 'G11 칩이 선 행(§D 규칙 — 직접 답 C · 언급 ↩) · 나머지는 칩 0 · 숨은 자리표 %s행' % j.get('placeholders'), j.get('withChip'))
        T(p + 'G11 칩 선 행 = Q0480 C1 + M001 이 언급한 같은 단원 문항 ↩(%s) · 그 밖 %s행 칩 0'
          % ([x for x in (j.get('withChip') or []) if x.endswith('↩')], (j.get('rows') or 0) - len(j.get('withChip') or [])),
          sorted(j.get('withChip') or []) == ['Q0474 ↩', 'Q0480 C1', 'Q4336 ↩', 'Q5514 ↩'], j.get('withChip'))
        T(p + 'G11 「정답·해설 ▸」 톡 → 정답 상자 열림(%s) · 다시 톡 → 닫힘(%s)' % (g(n, 'G11open', 'q0480', 'ansHidden'), g(n, 'G11close', 'q0480', 'ansHidden')),
          n.get('G11ans1') is True and g(j, 'q0480', 'ansHidden') is True and g(n, 'G11open', 'q0480', 'ansHidden') is False and g(n, 'G11close', 'q0480', 'ansHidden') is True, [j.get('q0480'), g(n, 'G11open', 'q0480')])
        T(p + 'G11 헛잣대 BASE — 같은 창 %s행 · 칩 0 · 「정답·해설 ▸」 은 옛 판도 열림(%s→%s)' % (jb.get('rows'), g(jb, 'q0480', 'ansHidden'), g(b, 'G11open', 'q0480', 'ansHidden')),
          jb.get('rows') == j.get('rows') and not jb.get('withChip') and g(b, 'G11open', 'q0480', 'ansHidden') is False, [jb, b.get('G11open')])
        T(p + 'G11 C1 칩 톡 → Claude 창(%s) · 크기 기억은 claude 와 jn 따로' % g(n, 'G11win', 'title'),
          n.get('G11chip') is True and g(n, 'G11win', 'win') is True and g(n, 'G11win', 'answers') == ['M001'], [n.get('G11win'), n.get('G11sizeJn')])
        # G17
        for tag, d in (('BASE', b), ('NEW', n)):
            bad = [x for x in (d.get('G17') or []) if x[2] != 'ok']
            T(p + 'G17 %s 스크립트 블록 %d개 파서 통과(%s · node 대신)' % (tag, len(d.get('G17') or []), 'JSC' if eng == 'webkit' else 'V8'),
              (d.get('G17') or []) and not bad, bad)
    # ══ G14 · G15 · A-2
    G = RES.get('g1415') or {}
    g14, g15, g15n, a2 = G.get('G14') or {}, G.get('G15') or {}, G.get('G15net') or {}, G.get('A2') or {}
    T('G14 claude.json 404 → CL_STATE ok(빈 것) · 카드 회색 「Claude」 만 · 오류 문구 없음 · JS 오류 0',
      g(g14, 'load', 'state') == 'ok' and g(g14, 'load', 'by') == {} and g(g14, 'card', 'btn', 'text') == 'Claude' and g(g14, 'card', 'btn', 'color') == GRAY
      and g(g14, 'load', 'status') == '' and not g14.get('err') and not g14.get('pageerror'), g14)
    T('G15 토큰 없음 → 단추 안 그림(보이는 단추 %s · 숨은 자리표 %s) · 「%s」 한 번 · 두 번째 실패엔 문구 없음(「%s」) · 앱 정상'
      % (g15.get('vis'), g15.get('all'), g(g15, 'load', 'status'), g(g15, 'load2', 'status')),
      g(g15, 'load', 'state') == 'fail' and g15.get('vis') == 0 and g(g15, 'card', 'card') is True and g(g15, 'card', 'btn', 'tag') == 'SPAN'
      and g(g15, 'load', 'status') == 'Claude 답을 못 받았습니다' and 'text-red-600' in (g(g15, 'load', 'statusCls') or '') and g(g15, 'load2', 'status') == ''
      and g(g15, 'pop', 'pop') is True and not g15.get('err') and not g15.get('pageerror'), g15)
    T('G15 네트워크 실패(HTTP 500)도 같다 — 단추 안 그림 · 문구 한 번', g(g15n, 'load', 'state') == 'fail' and g15n.get('vis') == 0
      and g(g15n, 'load', 'status') == 'Claude 답을 못 받았습니다' and g(g15n, 'load2', 'status') == '' and not g15n.get('err'), g15n)
    T('§A-2 받는 때 — 받는 중에 겹쳐 부르면 한 번만 받는다(%s → %s) · syncRecords 가 돌면 한 번 더(%s)' % (a2.get('gets0'), a2.get('both'), a2.get('gets1')),
      a2.get('gets0') == 0 and a2.get('both') == 1 and a2.get('gets1') == 2 and not a2.get('err'), a2)
    # ══ G16
    G16 = RES.get('g16') or {}
    I('G16 흐름 — ① 새 판 A 가 정정을 올림 ② 옛 판 B 가 그 원격을 받아 제 변경과 함께 올림 ③ A 가 다시 맞춤 ④ 정정 없는 새 판 C', {k: G16.get(k) for k in ('P1', 'P2', 'Blocal', 'P3', 'A2', 'C1', 'C2')})
    T('G16 ① 새 판이 올린 기록에 data.ox_cl_fix.M001 · u 도장', g(G16, 'P1', 'data') is True and g(G16, 'P1', 'fix', 'M001', 'done') is False and g(G16, 'P1', 'u'), G16.get('P1'))
    T('G16 ② 옛 판 기기는 제 저장소에 ox_cl_fix 를 만들지 않는다(모르는 키 · 병합이 건드리지 않는다)', G16.get('Blocal') is None, G16.get('Blocal'))
    I('G16 ② 잰 것 — 옛 판(846dc1e) 기기가 올린 기록: data.ox_cl_fix %s · u 도장 %s · data 키 %s개(옛 recPayload 는 제 SYNC_KEYS 17키만 담는다)'
      % ('있음' if g(G16, 'P2', 'data') else '**없음(빠짐)**', '있음' if g(G16, 'P2', 'u') else '없음', g(G16, 'P2', 'keys')), G16.get('P2'))
    T('G16 ② 지시서 기대 — 옛 판 기기가 올려도 data.ox_cl_fix 가 남는다(「모르는 키로 두고 지우지 않는다」)',
      g(G16, 'P2', 'data') is True, G16.get('P2'))
    T('G16 ③ 새 판 기기 A 가 다음 맞추기에서 되살려 올린다(올림 %s · 옛 판 기기의 변경도 그대로 %s)' % (g(G16, 'P3', 'puts'), g(G16, 'P3', 'tag')),
      g(G16, 'P3', 'data') is True and g(G16, 'P3', 'fix', 'M001', 'md') == 'A 기기 정정본' and g(G16, 'P3', 'puts') == 1, G16.get('P3'))
    T('G16 ④ 새 판 기기 C — 빠진 원격에서는 못 받고(%s) 되살린 원격에서 받는다(%s)' % ('M001 없음' if 'M001' not in (G16.get('Clocal1') or '') else 'M001 있음', 'M001' if G16.get('Clocal2') and 'M001' in G16.get('Clocal2') else G16.get('Clocal2')),
      'M001' not in (G16.get('Clocal1') or '') and 'A 기기 정정본' in (G16.get('Clocal2') or ''), [G16.get('Clocal1'), G16.get('Clocal2')])
    T('G16 JS 오류 0(세 기기)', not any(G16.get('err') or [[1]]), G16.get('err'))

    for l in L:
        print('   ' + l)
    p = sum(1 for l in L if l.startswith('PASS')); f = sum(1 for l in L if l.startswith('FAIL'))
    print('\n합계  PASS %d · FAIL %d' % (p, f))
    io.open(os.path.join(HERE, '_harness_ox_claude_answers_result.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n\n합계  PASS %d · FAIL %d\n' % (p, f))
    sys.exit(0 if not f else 1)


if __name__ == '__main__':
    main()
