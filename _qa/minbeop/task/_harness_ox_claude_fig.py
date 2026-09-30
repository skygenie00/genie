# -*- coding: utf-8 -*-
"""민법OX Claude 창 「그림」 한 장 — _task_ox_claude_fig §D(D1~D11 · D12 는 _harness_ox_claude_answers 사본으로 따로).

  NEW  = genie 작업트리 minbeop/index.html (고친 판 · LF)
  BASE = `7b9e214` 의 같은 파일(1,087,059 B · md5 a32b4202…) — 헛잣대 · D6 에서는 스냅샷 대조의 기준
  데이터 = studyplandata minbeop/기록.json(origin) · 문항마스터.json · Claude 답 = 이 폴더 claude.json(4,030 B · M002.fig) · 그림 = 이 폴더 M002.html(8,376 B)
  엔진 = playwright webkit · chromium — has_touch · is_mobile · 아이패드 1024×768
  누름 = touchscreen.tap(진짜 터치) · 끌기 = chromium CDP 터치(끝에서 멈춤) / webkit 신뢰 마우스(도구 한계)
  網 = 같은 출처 + cdn.tailwindcss.com 만 · GitHub 는 SEED 가 대답(claude.json = 파일 · 그림 = 파일·404·500·스크립트 심은 가짜) · Google Fonts 는 막힌다

쓰기 : python _harness_ox_claude_fig.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
_NR = _roots.need_n('민법 task 재료(claude.json · M002.html)')   # env_lanes_fix(9/29) — N: 작업 폴더 · 없으면(클라우드) 「N: 필요 — 클라우드 불가(…)」 종료 코드 3
import hashlib, http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

GENIE = _roots.genie()
SPD = _roots.spd()
HERE = os.path.dirname(os.path.abspath(__file__))
TASKDIR = os.path.join(_NR, 'minbeop', 'task')
CLJSON = os.path.join(TASKDIR, 'claude.json')
FIGSRC = os.path.join(TASKDIR, 'M002.html')
WORK = os.path.join(tempfile.gettempdir(), 'h_claude_fig')
REL = 'minbeop/index.html'
BASE_REV, BASE_MD5 = '7b9e214', 'a32b4202635387d0b76321bf1444fcd9'
TESTS = io.open(os.path.join(HERE, '_harness_ox_claude_fig_tests.js'), encoding='utf-8').read()
IPAD_UA = ('Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 '
           '(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
EVIL = ('<!doctype html><meta charset="utf-8"><title>evil</title>'
        '<style>body{margin:0}</style><body onload="parent.__FIGRAN3=1">'
        '<script>parent.__FIGRAN=1;document.title="ran";</script>'
        '<img src="x-none.png" onerror="parent.__FIGRAN2=1">'
        '<div style="height:300px;background:#fee">가짜 그림 — 스크립트가 돌면 parent.__FIGRAN 이 선다</div></body>')
SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__ALERTS=[];window.alert=function(m){__ALERTS.push(String(m));};
window.confirm=function(){return true;};window.prompt=function(){return null;};
(function(){var Q=new URLSearchParams(location.search);var nf=window.fetch.bind(window);window.__FIGMODE=Q.get('fig')||'file';window.__CLGETS=0;window.__FIGGETS=0;window.__FIGURLS=[];
window.fetch=function(u,o){o=o||{};var s=String((u&&u.url)||u);
 if(/\/contents\/minbeop\/claude\.json/.test(s)){window.__CLGETS++;return nf('/claude.json',{cache:'no-store'});}
 var fm=/\/contents\/minbeop\/(claude_fig\/[^?]+)/.exec(s);
 if(fm){window.__FIGGETS++;window.__FIGURLS.push(decodeURIComponent(fm[1]));
  if(window.__FIGMODE==='404')return Promise.resolve(new Response('{"message":"Not Found"}',{status:404}));
  if(window.__FIGMODE==='500')return Promise.resolve(new Response('{"message":"harness 500"}',{status:500}));
  return nf(window.__FIGMODE==='evil'?'/evil.html':'/M002.html',{cache:'no-store'});}
 if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));
 return nf(u,o);};})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
localStorage.clear();
</script>"""
READY = ("typeof buildQuizData==='function'&&typeof openQPopup==='function'&&typeof clLoad==='function'&&!!window.__HZT")


def git(*a, repo=GENIE):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def J(s):
    try:
        return json.loads(s) if isinstance(s, str) else s
    except Exception:
        return {'__raw': str(s)[:300]}


def g(d, *ks):
    for k in ks:
        if isinstance(d, dict):
            d = d.get(k)
        elif isinstance(d, list) and isinstance(k, int) and -len(d) <= k < len(d):
            d = d[k]
        else:
            return None
    return d


def serve(tag, src):
    OUT = os.path.join(WORK, 'srv_' + tag); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    b = src.index('<body'); bb = src.index('>', b) + 1
    html = src[:bb] + SEED + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + TESTS + '\n</script>\n' + html[e:]
    io.open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)
    io.open(os.path.join(OUT, 'evil.html'), 'w', encoding='utf-8', newline='\n').write(EVIL)
    open(os.path.join(OUT, 'rec.json'), 'wb').write(git('show', 'origin/main:minbeop/기록.json', repo=SPD))
    MAP = {'/master.json': os.path.join(SPD, 'minbeop', '문항마스터.json'), '/claude.json': CLJSON, '/M002.html': FIGSRC}

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
            for i in range(5):
                t('touchMove', x1, y1); self.pg.wait_for_timeout(30)
            t('touchEnd', x1, y1)
            return 'cdp-touch'
        m = self.pg.mouse
        m.move(x0, y0); m.down()
        for i in range(1, n + 1):
            m.move(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.pg.wait_for_timeout(16)
        m.up()
        return 'mouse(trusted)'


def open_page(pw_br, eng, tag, src, extra='', fig='file'):
    srv, port = serve('%s_%s%s' % (tag, eng, extra), src)
    ctx = pw_br.new_context(viewport={'width': 1024, 'height': 768}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=IPAD_UA)
    ctx.route('**/*', route_filter)
    pg = ctx.new_page()
    errs = {'page': [], 'console': []}
    pg.on('pageerror', lambda e: errs['page'].append(str(e)[:240]))
    pg.on('console', lambda m: errs['console'].append(m.text[:240]) if m.type == 'error' else None)
    pg.goto('http://127.0.0.1:%d/index.html?fig=%s' % (port, fig), wait_until='load', timeout=120000)
    pg.wait_for_function(READY, timeout=120000)
    return S(pg, eng), srv, ctx, errs


def open_cl(s, uid):
    c = s.js("u=>__HZT.card(u)", uid)
    ok = s.tap((c or {}).get('at'))
    s.pg.wait_for_timeout(350)
    return ok


def main_scenario(s, new):
    pg, R = s.pg, {}
    W = pg.wait_for_timeout
    R['setup'] = s.js("t=>__HZT.setup(t)", True)
    R['load'] = s.js("__HZT.load()")
    R['body0'] = s.js("__HZT.body()")
    # D1 · D10 — Q0035 카드 → Claude 1 → 창(여는 때 받는다)
    R['D1tap'] = open_cl(s, 'Q0035')
    R['D1wait'] = s.pg.evaluate("u=>__HZT.waitFig(u)", 'Q0035') if new else None
    if not new:
        W(1200)
    R['D1gets'] = s.js("__HZT.gets()")   # 그림이 뜬 뒤에 센다(WebKit 은 톡이 누름으로 늦게 바뀐다)
    R['D1'] = s.js("u=>__HZT.win(u)", 'Q0035')
    R['body1'] = s.js("__HZT.body()")
    if new:
        # D2 — 창을 480 → 700 → 480(모서리 손잡이 진짜 끌기) · 높이가 따라 바뀐다
        s.js("k=>__HZT.toTop(k)", 'cl-Q0035'); W(150)
        R['D2a'] = s.js("u=>__HZT.win(u)", 'Q0035')
        gp = s.js("([k,p])=>__HZT.winPart(k,p)", ['cl-Q0035', 'grip'])
        R['D2grip'] = gp
        if gp and gp.get('on'):
            R['D2drag'] = s.drag(gp['cx'], gp['cy'], gp['cx'] + 220, gp['cy'] + 40); W(700)
        R['D2b'] = s.js("u=>__HZT.win(u)", 'Q0035')
        gp2 = s.js("([k,p])=>__HZT.winPart(k,p)", ['cl-Q0035', 'grip'])
        if gp2 and gp2.get('on'):
            s.drag(gp2['cx'], gp2['cy'], gp2['cx'] - 220, gp2['cy']); W(700)
        R['D2c'] = s.js("u=>__HZT.win(u)", 'Q0035')
        # D5 — 「크게 보기」 → 860 창 · 끌기 · 손잡이 · oxwin.size.clfig(Claude 창과 따로)
        R['D5size0'] = s.js("__HZT.sizes()")
        R['D5tap'] = s.tap(s.js("([k,sl,t])=>__HZT.winBtn(k,sl,t)", ['cl-Q0035', '[data-clfig] button', '크게 보기'])); W(500)
        R['D5gets'] = s.js("__HZT.gets()")
        R['D5'] = s.js("m=>__HZT.big(m)", 'M002')
        hp = s.js("([k,p])=>__HZT.winPart(k,p)", ['clfig-M002', 'head'])
        if hp and hp.get('on'):
            R['D5drag'] = s.drag(hp['cx'], hp['cy'], hp['cx'] - 60, hp['cy'] - 30); W(400)
        R['D5moved'] = s.js("m=>__HZT.big(m)", 'M002')
        s.js("k=>__HZT.toTop(k)", 'clfig-M002'); W(150)
        gp3 = s.js("([k,p])=>__HZT.winPart(k,p)", ['clfig-M002', 'grip'])
        R['D5grip'] = gp3
        if gp3 and gp3.get('on'):
            R['D5resize'] = s.drag(gp3['cx'], gp3['cy'], gp3['cx'] - 200, gp3['cy'] - 60); W(700)
        R['D5sized'] = s.js("m=>__HZT.big(m)", 'M002')
        R['D5size1'] = s.js("__HZT.sizes()")
        # D8 — ✎ 정정: 글칸에 그림 코드 0 · 그림은 위에 그대로(같은 iframe) · 저장 뒤 다시 안 받음
        pg.evaluate("()=>{const w=document.getElementById('oxwin-clfig-M002');if(w)w.remove()}")
        R['D8ref'] = s.js("u=>__HZT.frameRef(u)", 'Q0035')
        R['D8edit'] = s.tap(s.js("([k,sl,t])=>__HZT.winBtn(k,sl,t)", ['cl-Q0035', '.clfixbar button', '✎ 정정'])); W(300)
        R['D8same'] = s.js("u=>__HZT.sameFrame(u)", 'Q0035')
        R['D8win'] = s.js("u=>__HZT.win(u)", 'Q0035')
        R['D8ta'] = s.js("([u,m])=>__HZT.setTa(u,m)", ['Q0035', 'add'])
        R['D8save'] = s.tap(s.js("([k,sl,t])=>__HZT.winBtn(k,sl,t)", ['cl-Q0035', '.clfixbar button', '저장 (정정으로)'])); W(900)
        R['D8after'] = s.js("u=>__HZT.win(u)", 'Q0035')
        R['D8gets'] = s.js("__HZT.gets()")
        R['D8fix'] = s.js("__HZT.fix()")
        # D10 — 닫고 두 번째 열기 = 받기 0
        s.js("__HZT.closeWins()")
        R['D10tap'] = open_cl(s, 'Q0035')
        R['D10wait'] = s.pg.evaluate("u=>__HZT.waitFig(u)", 'Q0035')
        R['D10gets'] = s.js("__HZT.gets()")
        R['D10'] = s.js("u=>__HZT.win(u)", 'Q0035')
        # D9 — 언급만인 창(Q0013)에도 M002 그림
        R['D9tap'] = open_cl(s, 'Q0013')
        R['D9wait'] = s.pg.evaluate("u=>__HZT.waitFig(u)", 'Q0013')
        R['D9'] = s.js("u=>__HZT.win(u)", 'Q0013')
        R['D9gets'] = s.js("__HZT.gets()")
    # D6 — Q0480(M001 · fig 없음) 창 본문 = 바탕 판과 글자 대조
    s.js("__HZT.closeWins()")
    R['D6tap'] = open_cl(s, 'Q0480')
    R['D6'] = s.js("u=>__HZT.win(u)", 'Q0480')
    R['D6gets'] = s.js("__HZT.gets()")
    R['D11'] = s.js("__HZT.parse()")
    R['err'] = s.js("__HZT.errs()")
    R['ro'] = s.pg.evaluate("__HZT.ro()")
    return R


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


def run_side(new):
    """D7 그림 404·500 · D3 스크립트 심은 가짜 그림(chromium · webkit 둘 다)"""
    R = {}
    with sync_playwright() as pw:
        for eng in ('chromium', 'webkit'):
            br = getattr(pw, eng).launch()
            for name, fig in (('D7', '404'), ('D7net', '500'), ('D3', 'evil')):
                if eng == 'webkit' and name != 'D3':
                    continue
                s, srv, ctx, errs = open_page(br, eng, 'NEW', new, '_' + name, fig)
                D = {}
                try:
                    D['setup'] = s.js("t=>__HZT.setup(t)", True)
                    D['load'] = s.js("__HZT.load()")
                    D['tap'] = open_cl(s, 'Q0035')
                    if name == 'D3':
                        D['wait'] = s.pg.evaluate("u=>__HZT.waitFig(u)", 'Q0035')
                        s.pg.wait_for_timeout(800)
                    else:
                        s.pg.wait_for_timeout(900)
                    D['win'] = s.js("u=>__HZT.win(u)", 'Q0035')
                    D['gets'] = s.js("__HZT.gets()")
                    D['evil'] = s.js("__HZT.evil()")
                    if name != 'D3':      # 창을 다시 열면 한 번 더 받는다
                        s.js("__HZT.closeWins()")
                        open_cl(s, 'Q0035'); s.pg.wait_for_timeout(900)
                        D['gets2'] = s.js("__HZT.gets()")
                        D['win2'] = s.js("u=>__HZT.win(u)", 'Q0035')
                    D['err'] = s.js("__HZT.errs()")
                except Exception as e:
                    D['exc'] = str(e)[:500]
                D['pageerror'], D['consoleError'] = errs['page'], errs['console']
                R['%s/%s' % (eng, name)] = D
                ctx.close(); srv.shutdown()
            br.close()
    return R


def main():
    os.makedirs(WORK, exist_ok=True)
    new = io.open(os.path.join(GENIE, REL), encoding='utf-8', newline='').read()
    base = git('show', BASE_REV + ':' + REL).decode('utf-8')
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
        t0 = time.time(); print('… D3·D7', flush=True); RES['side'] = run_side(new); print('   %.1fs' % (time.time() - t0), flush=True)
    json.dump(RES, io.open(os.path.join(WORK, 'raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    report(RES, base, new, only)


def report(RES, base, new, only):
    L = []
    T = lambda n, c, i=None: L.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c or i is None else ' | ' + json.dumps(i, ensure_ascii=False)[:900]))
    I = lambda n, v: L.append('INFO | ' + n + ' | ' + json.dumps(v, ensure_ascii=False)[:1400])
    bb, nb = base.encode('utf-8'), new.encode('utf-8')
    T('착수 %s = 지시서 G0-1 (1,087,059 B · md5 a32b4202…)' % BASE_REV, len(bb) == 1087059 and hashlib.md5(bb).hexdigest() == BASE_MD5, [len(bb), hashlib.md5(bb).hexdigest()])
    T('D11 NEW CRLF 0 · U+FFFD 0 (%d B · md5 %s)' % (len(nb), hashlib.md5(nb).hexdigest()), b'\r\n' not in nb and '\ufffd' not in new)
    ch = [l for l in git('status', '--porcelain').decode('utf-8').split('\n') if l.strip()]
    T('genie 작업트리 바뀐 파일 = minbeop/index.html 하나 %s' % ch, ch == [' M ' + REL], ch)
    sk = lambda s: re.findall(r"'([^']+)'", re.search(r'const SYNC_KEYS = \[(.+?)\];', s, re.S).group(1))
    T('§C SYNC_KEYS 무변(새 저장 키 0)', sk(new) == sk(base), [len(sk(base)), len(sk(new))])
    T('§A·§C 그림을 앱이 쓰는 길 0 — CL_FIG 는 메모리 · setItem/lsPut/dbPut 에 그림 없음 · ghPutJson 에 claude_fig 없음',
      not re.search(r"(setItem|lsPut|dbPut|idbPut)\([^)]*(CL_FIG|clfig|claude_fig)", new) and 'ghPutJson(' + "'minbeop/' + f" not in new
      and new.count("ghRaw('minbeop/' + f)") == 1)
    T('§B-2 iframe sandbox = "allow-same-origin" 하나 · sandbox 속성에 allow-scripts 0(주석 속 낱말은 안 센다)',
      new.count('<iframe sandbox="allow-same-origin" title=') == 1 and new.count('sandbox="') == 1 and 'allow-scripts' not in new)
    T('§I 공개 genie 에 그림·claude.json 없음', not os.path.exists(os.path.join(GENIE, 'minbeop', 'claude_fig')) and not os.path.exists(os.path.join(GENIE, 'minbeop', 'claude.json')))
    for eng in ('webkit', 'chromium'):
        for tag in ('BASE', 'NEW'):
            d = RES.get('%s/%s' % (eng, tag))
            if d is None:
                continue
            errs = J(d.get('err') or '[]') + [e for e in (d.get('pageerror') or []) if not e.startswith('ResizeObserver loop')]
            T('[%s] %s 부트 · 문항 %s · JS 오류 %d · ResizeObserver loop 알림 %s(그림 그릇 관찰이 알림을 쌓지 않는다)' % (eng, tag, g(d, 'setup', 'q'), len(errs), d.get('ro')),
              g(d, 'setup', 'q') == 5548 and not d.get('exc') and not errs and d.get('ro') == 0, [d.get('exc'), errs[:4], d.get('ro')])
    for eng in ('webkit', 'chromium'):
        n, b = RES.get(eng + '/NEW') or {}, RES.get(eng + '/BASE') or {}
        if not n:
            continue
        p = '[%s] ' % eng
        ld = n.get('load') or {}
        T(p + 'D10 앱 시작(받기 끝)에는 그림 요청 %s · claude.json 의 fig = %s' % (ld.get('figGets'), ld.get('figs')),
          ld.get('figGets') == 0 and ld.get('state') == 'ok' and ['M002', 'claude_fig/M002.html'] in (ld.get('figs') or []) and ['M001', None] in (ld.get('figs') or []), ld)
        a0 = g(n, 'D1', 'a', 0) or {}
        fr = a0.get('frame') or {}
        T(p + 'D1 Q0035 → 「Claude 1」 톡 → 창 · 차례 %s · 요청 %s(%s)' % (a0.get('order'), g(n, 'D1gets', 'fig'), g(n, 'D1gets', 'figUrls')),
          n.get('D1tap') is True and n.get('D1wait') is True and a0.get('m') == 'M002' and a0.get('order') == ['HEAD', 'FIG', 'MD', 'CORE', 'BAR']
          and g(n, 'D1gets', 'fig') == 1 and g(n, 'D1gets', 'figUrls') == ['claude_fig/M002.html'], [n.get('D1'), n.get('D1gets')])
        T(p + 'D1 그릇 — 그림(svg %s · 제목 「%s」) · 테두리 %s · 둥근 %s · 아래 여백 %s · 「%s」 %s(그릇 오른쪽 위 %s)'
          % (fr.get('svg'), fr.get('title'), fr.get('border'), fr.get('radius'), a0.get('figMb'), g(a0, 'big', 't'), [g(a0, 'big', k) for k in ('fs', 'fw', 'color', 'bd', 'bg')], g(a0, 'big', 'pos')),
          fr.get('svg') == 1 and fr.get('title') == 'M002 신의칙 한 장' and fr.get('border') == '0px' and fr.get('radius') == '8px' and a0.get('figMb') == '8px'
          and g(a0, 'big', 't') == '크게 보기' and [g(a0, 'big', k) for k in ('fs', 'fw', 'color', 'bd')] == ['11px', '700', 'rgb(107, 114, 128)', '0px']
          and g(a0, 'big', 'bg') in ('rgba(0, 0, 0, 0)', 'transparent') and g(a0, 'big', 'pos') is not None and g(a0, 'big', 'pos', 0) <= 8 and g(a0, 'big', 'pos', 1) <= 8, a0)
        T(p + 'D1 헛잣대 BASE — 같은 창에 그림 자리 0 · 요청 %s' % g(b, 'D1gets', 'fig'), g(b, 'D1', 'win') is True and g(b, 'D1', 'a', 0, 'fig') is False and g(b, 'D1gets', 'fig') == 0, b.get('D1'))
        T(p + 'D2 높이 = 그림 문서 높이 — iframe %s ↔ 문서 %s · 안쪽 넘침 세로 %s 가로 %s(스크롤바 0)'
          % (fr.get('h'), fr.get('docH'), fr.get('overflowY'), fr.get('overflowX')),
          abs((fr.get('h') or 0) - (fr.get('docH') or -99)) <= 2 and (fr.get('overflowY') or 0) <= 0 and (fr.get('overflowX') or 0) <= 0 and (fr.get('h') or 0) > 200, fr)
        fa, fb, fc = (g(n, 'D2a', 'a', 0, 'frame') or {}), (g(n, 'D2b', 'a', 0, 'frame') or {}), (g(n, 'D2c', 'a', 0, 'frame') or {})
        T(p + 'D2 창 480 → %s → %s(손잡이 %s) · 그림 높이 %s → %s → %s · 매번 문서 높이와 같다(±2) · 넘침 0'
          % (g(n, 'D2b', 'rect', 2), g(n, 'D2c', 'rect', 2), n.get('D2drag'), fa.get('h'), fb.get('h'), fc.get('h')),
          g(n, 'D2a', 'rect', 2) == 480 and (g(n, 'D2b', 'rect', 2) or 0) >= 690 and (fb.get('h') or 0) - (fa.get('h') or 0) > 100
          and abs((fc.get('h') or 0) - (fa.get('h') or 0)) <= 3 and all(abs((x.get('h') or 0) - (x.get('docH') or -99)) <= 2 and (x.get('overflowY') or 0) <= 0 for x in (fa, fb, fc)),
          [n.get('D2a', {}).get('rect'), fa, n.get('D2b', {}).get('rect'), fb, n.get('D2c', {}).get('rect'), fc, n.get('D2grip')])
        T(p + 'D3 iframe sandbox = 「%s」(allow-scripts 없음)' % fr.get('sandbox'), fr.get('sandbox') == 'allow-same-origin', fr)
        T(p + 'D4 그림을 연 뒤 앱 body 무변 — 여백·글꼴·크기·바탕·줄높이 %s' % (n.get('body0') == n.get('body1')), n.get('body0') == n.get('body1'), [n.get('body0'), n.get('body1')])
        b5 = n.get('D5') or {}
        T(p + 'D5 「크게 보기」 톡 → 창(%s · 폭 %s · 손잡이 %s) · 그림 높이 %s = 문서 %s · 요청 %s(다시 안 받음)'
          % (b5.get('head'), g(b5, 'rect', 2), b5.get('grip'), g(b5, 'frame', 'h'), g(b5, 'frame', 'docH'), g(n, 'D5gets', 'fig')),
          n.get('D5tap') is True and b5.get('win') is True and g(b5, 'rect', 2) == 860 and b5.get('grip') is True and (b5.get('head') or '').startswith('Claude 그림 · M002')
          and '신의칙은 강행규정인데 왜 강행규정에 지나' in (b5.get('head') or '') and abs((g(b5, 'frame', 'h') or 0) - (g(b5, 'frame', 'docH') or -99)) <= 2
          and (g(b5, 'frame', 'h') or 0) > (fa.get('h') or 0) and g(n, 'D5gets', 'fig') == 1, b5)
        s0, s1 = J(g(n, 'D5size0', 'claude') or 'null'), J(g(n, 'D5size1', 'clfig') or 'null')
        T(p + 'D5 머리 끌기(%s) %s → %s · 손잡이(%s) %s → %s · oxwin.size.clfig = %s · Claude 창 크기(oxwin.size.claude) 무변 %s'
          % (n.get('D5drag'), g(b5, 'rect'), g(n, 'D5moved', 'rect'), n.get('D5resize'), g(n, 'D5moved', 'rect'), g(n, 'D5sized', 'rect'), s1, g(n, 'D5size0', 'claude') == g(n, 'D5size1', 'claude')),
          abs((g(n, 'D5moved', 'rect', 0) or 0) - (g(b5, 'rect', 0) or 0)) > 30 and isinstance(s1, dict) and s1.get('w') and abs(s1.get('w') - (g(n, 'D5sized', 'rect', 2) or 0)) <= 2
          and (g(n, 'D5sized', 'rect', 2) or 999) < 860 and g(n, 'D5size0', 'claude') == g(n, 'D5size1', 'claude')
          and abs((g(n, 'D5sized', 'frame', 'h') or 0) - (g(n, 'D5sized', 'frame', 'docH') or -99)) <= 2, [n.get('D5moved'), n.get('D5sized'), n.get('D5size0'), n.get('D5size1')])
        d8 = g(n, 'D8win', 'a', 0) or {}
        T(p + 'D8 ✎ 정정 → 글칸(그림 코드 %s) · 그림은 위에 그대로(같은 iframe %s · 차례 %s)' % (d8.get('taHasFig'), g(n, 'D8same', 'same'), d8.get('order')),
          n.get('D8edit') is True and d8.get('ta') is True and d8.get('taHasFig') is False and g(n, 'D8same', 'same') is True and d8.get('order') == ['HEAD', 'FIG', 'MD', 'CORE', 'BAR']
          and g(n, 'D8ta', 'hasFig') is False, [n.get('D8same'), d8])
        a8 = g(n, 'D8after', 'a', 0) or {}
        fx = J(n.get('D8fix') or 'null') or {}
        T(p + 'D8 저장 → ox_cl_fix.M002 · 창 = %s · 그림 다시 안 받음(요청 %s) · 그림 높이 %s = 문서 %s'
          % (a8.get('order'), g(n, 'D8gets', 'fig'), g(a8, 'frame', 'h'), g(a8, 'frame', 'docH')),
          n.get('D8save') is True and g(fx, 'M002', 'done') is False and a8.get('order') == ['HEAD', 'FIG', 'TAG', 'MD', 'CORE', 'BAR']
          and g(n, 'D8gets', 'fig') == 1 and abs((g(a8, 'frame', 'h') or 0) - (g(a8, 'frame', 'docH') or -99)) <= 2, [a8, n.get('D8gets')])
        T(p + 'D10 닫고 두 번째 열기 → 요청 %s(0 더) · 그림 %s' % (g(n, 'D10gets', 'fig'), g(n, 'D10', 'a', 0, 'frame', 'svg')),
          n.get('D10tap') is True and n.get('D10wait') is True and g(n, 'D10gets', 'fig') == 1 and g(n, 'D10', 'a', 0, 'frame', 'svg') == 1, [n.get('D10gets'), g(n, 'D10', 'a', 0, 'order')])
        d9 = n.get('D9') or {}
        T(p + 'D9 Q0013(언급만) 창 → 답 %s · 그림 %s · 차례 %s · 요청 %s(다시 안 받음)' % (d9.get('answers'), g(d9, 'a', 0, 'frame', 'svg'), g(d9, 'a', 0, 'order'), g(n, 'D9gets', 'fig')),
          n.get('D9tap') is True and n.get('D9wait') is True and 'M002' in (d9.get('answers') or []) and g(d9, 'a', 0, 'frame', 'svg') == 1
          and g(d9, 'a', 0, 'order') == ['HEAD', 'FIG', 'TAG', 'MD', 'CORE', 'BAR'] and g(n, 'D9gets', 'fig') == 1, d9)   # D8 에서 M002 정정을 저장했다 — 딱지가 그림 아래에 선다
        n6, b6 = n.get('D6') or {}, b.get('D6') or {}
        same6 = n6.get('html') is not None and n6.get('html') == b6.get('html')
        diff6 = ''
        if not same6 and n6.get('html') and b6.get('html'):
            x, y = n6['html'], b6['html']
            i = next((i for i in range(min(len(x), len(y))) if x[i] != y[i]), min(len(x), len(y)))
            diff6 = ' · 첫 어긋남 %d자 새「%s」 옛「%s」' % (i, x[i:i + 50], y[i:i + 50])
        T(p + 'D6 Q0480(M001 · fig 없음) 창 본문 = 바탕 판과 글자 하나 안 다름(%d자 ↔ %d자%s) · 그림 요청 %s'
          % (len(n6.get('html') or ''), len(b6.get('html') or ''), diff6, g(n, 'D6gets', 'fig')),
          same6 and g(n6, 'a', 0, 'fig') is False and n6.get('answers') == ['M001'], [n6.get('answers'), diff6])
        for tag, d in (('BASE', b), ('NEW', n)):
            bad = [x for x in (J(d.get('D11') or '[]') or []) if x[2] != 'ok']
            T(p + 'D11 %s 스크립트 블록 %d개 파서 통과(%s)' % (tag, len(J(d.get('D11') or '[]') or []), 'JSC' if eng == 'webkit' else 'V8'), (J(d.get('D11') or '[]') or []) and not bad, bad)
    if only:
        return finish(L)
    SD = RES.get('side') or {}
    for k in ('chromium/D7', 'chromium/D7net'):
        d = SD.get(k) or {}
        a = g(d, 'win', 'a', 0) or {}
        T('D7 그림 %s → 그 자리 한 줄 「%s」 %s · 글 본문 「%s…」 · 차례 %s · JS 오류 0 · 다시 열면 한 번 더 받는다(%s → %s)'
          % ('404' if k.endswith('D7') else '500', a.get('figNote'), a.get('figNoteStyle'), (a.get('md') or '')[:12], a.get('order'), g(d, 'gets', 'fig'), g(d, 'gets2', 'fig')),
          a.get('figNote') == '그림을 못 불러왔다 (M002)' and a.get('figNoteStyle') == ['11px', 'rgb(107, 114, 128)'] and (a.get('md') or '') and a.get('order') == ['HEAD', 'FIG', 'MD', 'CORE', 'BAR']
          and a.get('frame') is None and g(d, 'gets', 'fig') == 1 and g(d, 'gets2', 'fig') == 2 and g(d, 'win2', 'a', 0, 'figNote') == '그림을 못 불러왔다 (M002)'
          and not J(d.get('err') or '[]') and not d.get('pageerror'), d)
    for k in ('chromium/D3', 'webkit/D3'):
        d = SD.get(k) or {}
        fr = g(d, 'win', 'a', 0, 'frame') or {}
        T('D3 [%s] 스크립트를 심은 가짜 그림 — 실행 0(%s) · sandbox 「%s」 · 문서에 <script> %s개는 있다 · 높이 %s = 문서 %s'
          % (k.split('/')[0], d.get('evil'), fr.get('sandbox'), fr.get('scripts'), fr.get('h'), fr.get('docH')),
          d.get('evil') == {'ran': None, 'ran2': None, 'ran3': None} and fr.get('sandbox') == 'allow-same-origin' and fr.get('scripts') == 1
          and abs((fr.get('h') or 0) - (fr.get('docH') or -99)) <= 2 and not J(d.get('err') or '[]'), d)
    return finish(L)


def finish(L):
    for l in L:
        print('   ' + l)
    p = sum(1 for l in L if l.startswith('PASS')); f = sum(1 for l in L if l.startswith('FAIL'))
    print('\n합계  PASS %d · FAIL %d' % (p, f))
    io.open(os.path.join(HERE, '_harness_ox_claude_fig_result.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n\n합계  PASS %d · FAIL %d\n' % (p, f))
    return f


if __name__ == '__main__':
    main()
