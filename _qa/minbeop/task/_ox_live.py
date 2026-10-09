# -*- coding: utf-8 -*-
r"""민법OX 실데이터 띄우기 헬퍼 OL — _task_cloud_batch_1010 클라우드 ① 관문 하네스 셋(_harness_ox_search_all · _harness_ox_queue_compare · _harness_ox_ggref_phone)이 같이 씀

  앱 = 글(메모리 · 작업트리 파일 또는 genie git 판) · 문항 · 기록 = studyplandata 로컬 사본(가짜 GitHub contents API · PUT 은 메모리 · 밖으로 안 나감)
  Tailwind = --tw 사본 CSS 가 있으면 cdn 대신 <style> 로(클라우드는 cdn 막힘 · 본 PC 는 cdn 그대로) · 토큰 = tt.cfg 'harness-token'(가짜)
  기기 = PC 1100×800(마우스) · 폰 390×844(hasTouch · 모바일 · DPR 2 · 톡 · 밀기 = CDP Input.dispatchTouchEvent)
  ⚠ 개인 문항 · 해설 글을 출력하지 않는다(D11) — 하네스는 ID · 수 · 자리만 적는다
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import base64, hashlib, json, os, re, subprocess, threading, time, urllib.parse   # noqa: E402
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer   # noqa: E402

PC = dict(name='PC', W=1100, H=800, touch=False)
PH = dict(name='폰', W=390, H=844, touch=True)
REPO = 'zzikkaplan/studyplandata'
CONF = {'spd': _roots.spd(), 'tw': None, 'shots': None}


def conf(**kw):
    CONF.update({k: v for k, v in kw.items() if v is not None})


def md5lf(s):
    return hashlib.md5(s.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def app_src(x):
    """앱 글 — 파일이면 그 파일 · 아니면 genie git 판의 minbeop/index.html"""
    if os.path.isfile(x):
        return open(x, 'rb').read().decode('utf-8')
    b = subprocess.run(['git', '-C', _roots.genie(), 'show', x + ':minbeop/index.html'], capture_output=True).stdout
    if not b:
        raise SystemExit('앱을 못 읽었다: ' + x)
    return b.decode('utf-8')


class Remote:
    """가짜 원격 — 처음 = studyplandata 로컬 사본 · over = 갈아 끼운 파일(바이트) · PUT = 메모리"""
    def __init__(self, over=None):
        self.files = dict(over or {})
        self.puts = []
        self.lock = threading.Lock()

    def get(self, path):
        with self.lock:
            if path in self.files:
                return self.files[path]
        f = os.path.join(CONF['spd'], *[p for p in path.split('/') if p])
        return open(f, 'rb').read() if os.path.isfile(f) else None

    def put(self, path, body):
        with self.lock:
            self.files[path] = body
            self.puts.append((path, len(body), time.time()))
        return hashlib.sha1(body).hexdigest()


def route(remote):
    def h(rt):
        req = rt.request
        u = req.url
        if u.startswith('http://127.0.0.1'):
            return rt.continue_()
        m = re.match(r'https://api\.github\.com/repos/([^/]+/[^/]+)/contents/([^?]+)', u)
        if m and m.group(1) == REPO:
            path = urllib.parse.unquote(m.group(2))
            if req.method == 'PUT':
                try:
                    body = json.loads(req.post_data or '{}')
                    data = base64.b64decode(body.get('content', ''))
                except Exception:
                    return rt.fulfill(status=422, body='{}', content_type='application/json')
                return rt.fulfill(status=200, body=json.dumps({'content': {'sha': remote.put(path, data)}}), content_type='application/json')
            b = remote.get(path)
            if b is None:
                return rt.fulfill(status=404, body='{"message":"Not Found"}', content_type='application/json')
            if 'raw' in ((req.headers or {}).get('accept', '')):
                return rt.fulfill(status=200, body=b, content_type='application/octet-stream')
            return rt.fulfill(status=200, body=json.dumps({'sha': hashlib.sha1(b).hexdigest(), 'size': len(b)}), content_type='application/json')
        return rt.abort()   # 그 밖 바깥(cdn · 다른 저장소) = 막음
    return h


def inject(src):
    src = src.replace('\r\n', '\n')
    tw = '<script src="https://cdn.tailwindcss.com"></script>'
    if CONF['tw'] and tw in src:
        src = src.replace(tw, '<style>/* harness: Tailwind v3 사본(--tw) */\n' + open(CONF['tw'], encoding='utf-8').read() + '\n</style>', 1)
    return src


SERVERS = {}
ON_LAUNCH = None   # 하네스가 QC.launch 를 건다 — 앱 띄움 셈('new' · 'base')


def serve(tag, src):
    if tag in SERVERS:
        return SERVERS[tag][1]
    body = inject(src).encode('utf-8')

    class Hd(SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            p = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
            data, code, ct = (body, 200, 'text/html; charset=utf-8') if p in ('/minbeop/', '/minbeop/index.html') else (b'{"message":"Not Found"}', 404, 'application/json')
            self.send_response(code)
            self.send_header('Content-Type', ct)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)

    srv = ThreadingHTTPServer(('127.0.0.1', 0), Hd)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


INIT = r"""
(()=>{
  if(!sessionStorage.getItem('__h')){sessionStorage.setItem('__h','1');
    try{localStorage.setItem('tt.cfg',JSON.stringify({token:'harness-token',person:'하네스'}))}catch(e){}}
  window.__err=[];
  window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+(e.lineno||''))});
  window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
  window.alert=function(){};window.confirm=function(){return true};window.prompt=function(){return null};
})();
"""
H = r"""
window.__H={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 vis(e){return !!e&&e.isConnected&&getComputedStyle(e).display!=='none'&&getComputedStyle(e).visibility!=='hidden'&&e.getBoundingClientRect().height>0},
 at(e){if(!e)return null;const r=e.getBoundingClientRect();let x=r.left+r.width/2,y=r.top+r.height/2,a=document.elementFromPoint(x,y);
   return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),cx:x,cy:y,on:!!a&&(a===e||e.contains(a))&&y>0&&y<innerHeight&&x>0&&x<innerWidth,top:a?(a.id?'#'+a.id:a.tagName.toLowerCase()+'.'+String(a.className||'').slice(0,24)):null}},
 hit(e){if(!e)return null;try{e.scrollIntoView({block:'center',inline:'nearest'})}catch(_){}return __H.at(e)},
 /* 누를 자리 — 가운데에서 위 · 아래 · 왼 · 오른으로 elementFromPoint 가 그 요소(또는 안)인 데까지(::before 로 넓힌 자리도 셈) */
 hitBox(e){if(!e)return null;const r=e.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2;
   const on=(x,y)=>{const a=document.elementFromPoint(x,y);return !!a&&(a===e||e.contains(a))};
   if(!on(cx,cy))return {h:0,w:0,on:false};let u=0,d=0,l=0,rt=0;
   while(u<60&&on(cx,cy-u-1))u++;while(d<60&&on(cx,cy+d+1))d++;while(l<160&&on(cx-l-1,cy))l++;while(rt<160&&on(cx+rt+1,cy))rt++;
   return {h:u+d+1,w:l+rt+1,on:true}},
 errs(){return (window.__err||[]).slice(0,8)}
};
"""


class Live:
    """기기 하나 = 문맥 하나 — 앱 띄우고 문항(서버 JSON) · 기록 맞추기 끝날 때까지"""
    def __init__(self, br, tag, src, dev, remote=None, init='', wait_sync=True):
        self.tag, self.dev = tag, dev
        if ON_LAUNCH:
            ON_LAUNCH(tag)
        kw = dict(viewport={'width': dev['W'], 'height': dev['H']})
        if dev['touch']:
            kw.update(device_scale_factor=2, is_mobile=True, has_touch=True)
        self.ctx = br.new_context(**kw)
        self.remote = remote or Remote()
        self.ctx.route('**/*', route(self.remote))
        self.ctx.add_init_script(INIT + (init or ''))
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(120000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append(str(e)[:240]))
        port = serve(tag, src)
        self.pg.goto('http://127.0.0.1:%d/minbeop/index.html' % port, wait_until='load', timeout=120000)
        self.pg.wait_for_function("() => typeof quizData !== 'undefined' && quizData.length > 1000 && typeof runSearch === 'function'", timeout=120000)
        if wait_sync:
            self.pg.wait_for_function("() => typeof recBusy !== 'undefined' && !recBusy && ((JSON.parse(localStorage.getItem('ox_sync_meta')||'{}').lastSync)||0) > 0", timeout=120000)
        self.pg.wait_for_timeout(500)
        self.pg.evaluate(H)

    def ev(self, js, arg=None):
        return self.pg.evaluate(js, arg)

    def wait(self, ms):
        self.pg.wait_for_timeout(ms)

    def _cdp(self):
        if not hasattr(self, '_c'):
            self._c = self.ctx.new_cdp_session(self.pg)
        return self._c

    def press(self, x, y, hold=80):
        """진짜 누름 — PC = 마우스 · 폰 = CDP 톡"""
        if self.dev['touch']:
            c = self._cdp()
            c.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'id': 1, 'radiusX': 6, 'radiusY': 6}]})
            self.pg.wait_for_timeout(hold)
            c.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        else:
            self.pg.mouse.click(x, y)

    def swipe(self, x0, y0, x1, y1, steps=10, dur=200):
        c = self._cdp()
        pt = lambda x, y: [{'x': x, 'y': y, 'id': 1, 'radiusX': 6, 'radiusY': 6}]
        c.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': pt(x0, y0)})
        for k in range(1, steps + 1):
            self.pg.wait_for_timeout(dur / steps)
            c.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': pt(x0 + (x1 - x0) * k / steps, y0 + (y1 - y0) * k / steps)})
        c.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})

    def scroll_in(self, sel, dy=600):
        """그 굴림 통 안을 진짜로 굴림 — PC = 마우스 휠 · 폰 = 손가락 밀기(위로)"""
        r = self.ev("(s)=>{const e=document.querySelector(s);if(!e)return null;const b=e.getBoundingClientRect();return {x:b.left+b.width/2,y:b.top+b.height/2,h:b.height}}", sel)
        if not r:
            return False
        if self.dev['touch']:
            span = max(60, min(r['h'] * 0.7, 400))
            self.swipe(r['x'], r['y'] + span / 2, r['x'], r['y'] - span / 2, steps=10, dur=160)
        else:
            self.pg.mouse.move(r['x'], r['y'])
            self.pg.mouse.wheel(0, dy)
        return True

    def errors(self):
        try:
            return (self.errs or []) + (self.ev('window.__err||[]') or [])
        except Exception as e:
            return self.errs + ['ev: ' + str(e)[:120]]

    def shot(self, name):
        if not CONF['shots']:
            return None
        try:
            os.makedirs(CONF['shots'], exist_ok=True)
            f = os.path.join(CONF['shots'], name + '.png')
            self.pg.screenshot(path=f)
            return f
        except Exception:
            return None

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass
