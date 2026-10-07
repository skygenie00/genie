# -*- coding: utf-8 -*-
r"""_task_jagwa_physphone §B 관문 — 자과 물리 폰 화면 손질(누른 창 앞으로 · 정리 창 줄 · 위 공식 · ✕ · 문항 창 머리 · 개념 글) + 화면 훑기 + 회귀

  python _harness_jagwa_physphone.py [--new <앱>] [--base <앱 파일 | genie git 판>] [--vendor <cdnjs 사본 폴더>] [--eng chromium,webkit] [--only B1,B2,B2S,..,B8] [--reg phys,phone_win,..] [--res <결과>] [--yardstick]

  NEW  = 이 판 앱(기본 genie jagwa/index.html) · BASE = 착수 때 main(기본 genie git 판 cedc251)
  --yardstick = BASE 를 NEW 자리에 넣어 B1~B6 · B2S 가 저마다 FAIL 해야 통과(B7 화면 훑기 = 새 판 흠 − 바탕 흠이라 해당 없음 · B8 회귀 = 안 돌림)
  관문: B1 누른 창 앞 · B2 정리 창 줄(글자 · 이름 · 마크 줄 · 길게 눌러 고치기) · B2S 고친 이름 동기화(칸 도장 · 묘비 · 두 기기 병합 · 옛 판 기기 틈을 재서 적음)
        B3 위 공식(탭 · 묶음 · 단위·기초 · 백지 인출 · 칩 19 · 공식 칸 고치기 세 자리 · FR 무변 · 「이론」) · B4 정리 창 ✕ · B5 문항 창 머리(세 과목 · 물리 근거 칸)
        B6 개념·이론 줄 글 · B7 화면 훑기(폰 · 아이패드 · PC · 넘침 · 잘림 · 겹침 · 누름 < 36 → 새로 생긴 것 0) · B8 회귀(저장소 하네스를 새 판 · 바탕 두 번 돌려 칸마다 견줌)
  자리 = _roots(GENIE_ROOT · SPD_ROOT) — 클라우드: GENIE_ROOT=/home/user/genie SPD_ROOT=/home/user/studyplandata · 지학 정리판 = SPD_ROOT 옆 notes(--notes)
  서버 = 스스로(127.0.0.1 빈 포트 · 앱 글만) · 바깥 요청 = Playwright route:
    api.github.com studyplandata · notes contents = 로컬 사본(읽기만) · **기록(<과목>/기록.json)은 가짜 사본**(Remote — PUT 은 여기 담기고 밖으로 안 나간다 · 기기(문맥)끼리 나눠 쓴다)
    cdnjs(pdf.js 3.11.174 · pdf-lib 1.17.1 · KaTeX 0.16.9) = --vendor 폴더(cdnjs 경로 꼴 그대로 · /ajax/libs/ 뒤) · 그 밖 바깥 = 막음
  누름 = 진짜 포인터(page.mouse · 손가락 = Chromium CDP 터치 550ms) · WebKit = 톡은 touchscreen.tap · 길게 누르기·끌기는 같은 자리 합성 touch 포인터(jo_revfix0929b 합치기 길)
    보임 = elementFromPoint(여러 줄로 감긴 글 칸은 글 줄 상자 가운데) · 자리 = getBoundingClientRect
  B8 회귀 — 하네스 파일은 안 고친다. 돌릴 때만 씌움(REG_SHIM): 윈도 크롬 자리가 없으면 Playwright Chromium(--no-sandbox) · cdnjs = --vendor(크롬 = 로컬 https 사본 +
    host-resolver-rules · Playwright = route) · 임시 GENIE_ROOT(jagwa/index.html = 그 판 · git HEAD = 그 하네스의 바탕 판) · 뜻한 변경(EXPECT) = 지시서가 바꾼 칸을 잣대 함수로
    「그것만 바뀜」 확인한 뒤 회귀에서 뺀다 · N: 을 부르는 하네스 = 「N: 필요 — 합칠 때 본 세션」
  ⚠ 자과앱 픽셀 게이트 없음(CLAUDE.md) — 그림은 화면 훑기 참고로만 남긴다
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import base64, hashlib, json, os, re, sys, time, subprocess, tempfile, threading, urllib.parse   # noqa: E402
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEW = ARG('--new', _roots.genie('jagwa', 'index.html'))
BASE = ARG('--base', 'cedc251')
SPD = ARG('--spd', _roots.spd())
NOTES = ARG('--notes', os.path.join(os.path.dirname(_roots.spd()), 'notes'))
VENDOR = ARG('--vendor', os.path.join(tempfile.gettempdir(), 'h_jagwa', 'vendor'))
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_physphone_result.txt'))
SHOTS = ARG('--shots', os.path.join(tempfile.gettempdir(), 'h_jagwa', 'shots'))
YARD = '--yardstick' in sys.argv
PHONE = (390, 844)
PAD = (820, 1180)
PC = (1440, 900)


def git(*a):
    return subprocess.run(['git', '-C', _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def app_src(x):
    """앱 글 — 파일이면 그 파일 · 아니면 genie git 판의 jagwa/index.html"""
    if os.path.isfile(x):
        return open(x, 'rb').read().decode('utf-8')
    b = git('show', x + ':jagwa/index.html')
    if not b:
        raise SystemExit('바탕 앱을 못 읽었다: ' + x)
    return b.decode('utf-8')


# ── 가짜 원격(기록) — 과목마다 한 파일 · 처음 = studyplandata 로컬 사본 · PUT = 여기 담김(밖으로 안 나감) ──
class Remote:
    def __init__(self):
        self.files, self.puts = {}, []
        self.lock = threading.Lock()

    def path_local(self, repo, path):
        root = NOTES if repo.endswith('/notes') else SPD
        return os.path.join(root, *[p for p in path.split('/') if p])

    def get(self, repo, path):
        key = repo + ':' + path
        with self.lock:
            if key in self.files:
                return self.files[key]
        f = self.path_local(repo, path)
        if os.path.isfile(f):
            return open(f, 'rb').read()
        return None

    def put(self, repo, path, body):
        key = repo + ':' + path
        with self.lock:
            self.files[key] = body
            self.puts.append((key, len(body), time.time()))
        return hashlib.sha1(body).hexdigest()

    def rec(self, subj='phys'):
        b = self.get('zzikkaplan/studyplandata', subj + '/기록.json')
        return json.loads(b.decode('utf-8')) if b else None


REMOTE = Remote()
OKHOST = ('http://127.0.0.1',)


def route_handler(remote):
    def h(route):
        req = route.request
        u = req.url
        if u.startswith(OKHOST):
            return route.continue_()
        m = re.match(r'https://api\.github\.com/repos/([^/]+/[^/]+)/contents/([^?]+)', u)
        if m:
            repo, path = m.group(1), urllib.parse.unquote(m.group(2))
            if req.method == 'PUT':
                try:
                    body = json.loads(req.post_data or '{}')
                    data = base64.b64decode(body.get('content', ''))
                except Exception:
                    return route.fulfill(status=422, body='{}', content_type='application/json')
                sha = remote.put(repo, path, data)
                return route.fulfill(status=200, body=json.dumps({'content': {'sha': sha}}), content_type='application/json')
            b = remote.get(repo, path)
            if b is None:
                return route.fulfill(status=404, body='{"message":"Not Found"}', content_type='application/json')
            acc = (req.headers or {}).get('accept', '')
            if 'raw' in acc:
                return route.fulfill(status=200, body=b, content_type='application/octet-stream')
            return route.fulfill(status=200, body=json.dumps({'sha': hashlib.sha1(b).hexdigest(), 'size': len(b)}), content_type='application/json')
        m = re.match(r'https://cdnjs\.cloudflare\.com/ajax/libs/(.+)$', u.split('?')[0])
        if m:
            f = os.path.join(VENDOR, *m.group(1).split('/'))
            if os.path.isfile(f):
                ct = 'text/css' if f.endswith('.css') else ('font/woff2' if f.endswith('.woff2') else 'application/javascript')
                return route.fulfill(status=200, body=open(f, 'rb').read(), content_type=ct)
            return route.continue_()   # 사본에 없으면 진짜 cdnjs(본 PC 는 열려 있다 · 클라우드는 --vendor 로 다 채운다)
        return route.abort()
    return h


SERVERS = {}


def serve(tag, src):
    """판마다 서버 하나 — 앱 글(메모리) · /img/ 는 genie jagwa/img"""
    if tag in SERVERS:
        return SERVERS[tag][1]
    body = src.encode('utf-8')

    class Hd(SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            p = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
            if p in ('/', '/app.html', '/jagwa/', '/jagwa/index.html'):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                self.wfile.write(body)
                return
            return super().do_GET()

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
            for pre in ('/jagwa/', '/'):
                if p.startswith(pre):
                    rest = [x for x in p[len(pre):].split('/') if x]
                    return _roots.genie('jagwa', *rest)
            return _roots.genie('jagwa', '__없음__')

    srv = ThreadingHTTPServer(('127.0.0.1', 0), Hd)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


INIT = r"""
(()=>{
  if(!sessionStorage.getItem('__h')){sessionStorage.setItem('__h','1');
    try{localStorage.setItem('subj','__SUBJ__')}catch(e){}
    try{localStorage.setItem('tt.cfg',JSON.stringify({token:'harness-token',person:'__WHO__'}))}catch(e){}}
  window.__err=[];
  window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+(e.lineno||''))});
  window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
  window.alert=function(){};window.confirm=function(){return true};window.prompt=function(){return null};
})();
"""


class Pg:
    """쪽 하나 = 기기 하나(문맥) — 과목 · 화면 · 손가락 · 누구(tt.cfg person)"""

    def __init__(self, br, eng, tag, src, subj='phys', dev=PHONE, touch=None, who='하네스', remote=None):
        W, H = dev
        self.eng, self.dev = eng, dev
        self.touch = (dev != PC) if touch is None else touch
        kw = dict(viewport={'width': W, 'height': H}, device_scale_factor=2 if self.touch else 1)
        if self.touch:
            kw.update(has_touch=True)
            if eng != 'webkit':
                kw.update(is_mobile=W < 700)
        self.ctx = br.new_context(**kw)
        self.remote = remote or REMOTE
        self.ctx.route('**/*', route_handler(self.remote))
        self.ctx.add_init_script(INIT.replace('__SUBJ__', subj).replace('__WHO__', who))
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(90000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append(str(e)[:240]))
        self.port = serve(tag, src)
        self.load()

    READY = 'typeof DATA!=="undefined"&&DATA.length>0&&typeof draw==="function"'
    PDFS = '(document.body.dataset.layer!=="pdf")||(typeof HAVE!=="undefined"&&["111","222","333","444","555","666"].every(f=>HAVE[f]))'

    def load(self):
        self.pg.goto('http://127.0.0.1:%d/app.html' % self.port, wait_until='load')
        self._ready()

    def reload(self):
        self.pg.reload(wait_until='load')
        self._ready()

    def _ready(self):
        self.pg.wait_for_function(self.READY, timeout=90000)
        try:   # 물리 = 시험지 여섯(route 가 studyplandata 로컬 사본을 준다 · 한 문맥에 한 번 받으면 IndexedDB 에 남는다)
            self.pg.wait_for_function(self.PDFS, timeout=180000)
        except Exception:
            pass
        self.pg.wait_for_timeout(1500)
        self.pg.evaluate(TOOLS)

    def ev(self, js, arg=None):
        return self.pg.evaluate(js, arg)

    def wait(self, ms):
        self.pg.wait_for_timeout(ms)

    def click(self, x, y, wait=400):
        self.pg.mouse.click(x, y)
        self.pg.wait_for_timeout(wait)

    def _cdp(self):
        if not hasattr(self, '_c'):
            self._c = self.ctx.new_cdp_session(self.pg)
        return self._c

    def tap(self, x, y, wait=400, hold=60):
        if self.eng == 'webkit':
            self.pg.touchscreen.tap(x, y)
        else:
            c = self._cdp()
            c.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'radiusX': 6, 'radiusY': 6, 'id': 1}]})
            self.pg.wait_for_timeout(hold)
            c.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        self.pg.wait_for_timeout(wait)

    def long_press(self, x, y, ms=550, wait=400):
        """진짜 터치 길게 누르기(CDP touchStart → ms → touchEnd) · 마우스 문맥은 mouse.down/up"""
        ms = max(ms, 900)   # ★ 2026-10-08 (_task_jagwa_phys_win 회귀) 앱 문턱 500ms 타이머 — 짐이 크면 550ms 떼기와 경합(1 단계 B2 입력 칸 안 섬 · 짐 적으면 섬) → 900ms 로 여유 · 「길게」 뜻 무변
        if not self.touch:
            self.pg.mouse.move(x, y)
            self.pg.mouse.down()
            self.pg.wait_for_timeout(ms)
            self.pg.mouse.up()
        elif self.eng == 'webkit':
            # Playwright WebKit 은 진짜 터치를 붙잡지 못한다(톡만 · CDP 없음) — jo_revfix0929b 합치기(9/30 Code) 길과 같게:
            # 같은 자리에 합성 touch 포인터를 ms 동안 누르고(앱 길게 누르기 = pointerdown 뒤 500ms 타이머) 손 뗄 때처럼 touchend 도 보낸다
            self.pg.evaluate(WK_LONG, [x, y, 'pointerdown'])
            self.pg.wait_for_timeout(ms)
            self.pg.evaluate(WK_LONG, [x, y, 'pointerup'])
        else:
            self.tap(x, y, wait=0, hold=ms)
        self.pg.wait_for_timeout(wait)

    def press(self, at, wait=400):
        if not at or not at.get('on'):
            return False
        (self.tap if self.touch else self.click)(at['cx'], at['cy'], wait)
        return True

    def shot(self, name):
        try:
            os.makedirs(SHOTS, exist_ok=True)
            self.pg.screenshot(path=os.path.join(SHOTS, name + '.png'))
        except Exception:
            pass

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


WK_LONG = r"""([x, y, ty]) => { const t = ty === 'pointerdown' ? document.elementFromPoint(x, y) : (window.__tlT || document.elementFromPoint(x, y));
  if (ty === 'pointerdown') window.__tlT = t;
  t.dispatchEvent(new PointerEvent(ty, {bubbles: true, cancelable: true, composed: true, pointerId: 7, pointerType: 'touch', isPrimary: true,
    clientX: x, clientY: y, button: 0, buttons: ty === 'pointerdown' ? 1 : 0}));
  if (ty === 'pointerup') t.dispatchEvent(new Event('touchend', {bubbles: true, cancelable: true, composed: true}));
  return t.tagName; }"""

TOOLS = r"""
window.__H={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 vis(e){return !!e&&e.isConnected&&getComputedStyle(e).display!=='none'&&getComputedStyle(e).visibility!=='hidden'&&e.getBoundingClientRect().height>0},
 R(e){if(!e)return null;const r=e.getBoundingClientRect();return {x:Math.round(r.left*10)/10,y:Math.round(r.top*10)/10,w:Math.round(r.width*10)/10,h:Math.round(r.height*10)/10,b:Math.round(r.bottom*10)/10,r:Math.round(r.right*10)/10,cx:r.left+r.width/2,cy:r.top+r.height/2}},
 at(e){if(!e)return null;const r=__H.R(e);let a=document.elementFromPoint(r.cx,r.cy);
   /* 여러 줄로 감긴 글 칸(inline)은 상자 가운데가 줄 틈일 수 있다 — 그러면 글 줄 상자(getClientRects) 가운데 중 그 칸에 닿는 첫 자리 */
   if(!(a&&(a===e||e.contains(a))))for(const q of e.getClientRects()){const x=q.left+q.width/2,y=q.top+q.height/2,b=document.elementFromPoint(x,y);if(b&&(b===e||e.contains(b))){r.cx=x;r.cy=y;a=b;break}}
   return Object.assign(r,{on:!!a&&(a===e||e.contains(a))&&r.cy>0&&r.cy<innerHeight&&r.cx>0&&r.cx<innerWidth,top:a?(a.id?'#'+a.id:a.tagName.toLowerCase()+'.'+String(a.className||'').slice(0,30)):null,t:__H.tx(e).slice(0,30)})},
 hit(e){if(!e)return null;try{e.scrollIntoView({block:'center',inline:'nearest'})}catch(_){}return __H.at(e)},
 /* 누름 영역 — 가운데에서 위·아래·왼·오른으로 elementFromPoint 가 그 요소(또는 안)인 데까지 */
 hitBox(e){if(!e)return null;const r=e.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2;
   const on=(x,y)=>{const a=document.elementFromPoint(x,y);return !!a&&(a===e||e.contains(a))};
   if(!on(cx,cy))return {h:0,w:0,on:false};let u=0,d=0,l=0,rt=0;
   while(u<60&&on(cx,cy-u-1))u++;while(d<60&&on(cx,cy+d+1))d++;while(l<120&&on(cx-l-1,cy))l++;while(rt<120&&on(cx+rt+1,cy))rt++;
   return {h:u+d+1,w:l+rt+1,on:true}},
 top(){const c=document.elementFromPoint(innerWidth/2,innerHeight/2);const w=c&&c.closest('#view,.sheet,[id]');return w?(w.id||w.className):null},
 zs(){return ['view','jnw','mcw','pwl'].concat([...document.querySelectorAll('.sheet.shfloat')].map(x=>x.id||x.dataset.shkey||'')).filter(Boolean).map(id=>{const e=document.getElementById(id)||document.querySelector('[data-shkey="'+id+'"]');
   return e?[id,getComputedStyle(e).zIndex,e.style.zIndex,e.classList.contains('hide')]:null}).filter(Boolean)},
 errs(){return (window.__err||[]).slice(0,8)},
 /* 화면 훑기(규칙 60) — 넘침(가로 굴림 · 화면 밖) · 잘림(숨김인데 말줄임 없이 글이 넘침) · 겹침(누를 것끼리) · 작은 누름(손가락만 · 실제 누름 < 36)
    이름표 = 태그#id(없으면 태그.갈래:글 · 수는 #) · 떠 있는 층(fixed · sticky)은 겹침에서 뺀다 · 작은 누름은 요소마다 가운데로 굴려 잰다(굴림 자리와 무관) */
 ACT:'button, a[href], [role=button], input, select, textarea, label, .jgo, [data-go], .pwr, .jjn, [data-mc]',
 sweep(sel,touch){const out=[],tx=__H.tx,vis=__H.vis;
   const sig=e=>{const c=String(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className).split(' ').filter(x=>x&&!/^(on|cur|hide|z|sel|fold|fx|lp|ied|open|act)$/.test(x)).slice(0,2).join('.');
     return e.tagName.toLowerCase()+(e.id?'#'+e.id:(c?'.'+c:'')+':'+tx(e).replace(/\d+/g,'#').slice(0,14))};
   const se=document.scrollingElement;if(se.scrollWidth>innerWidth+1)out.push('page-hscroll');
   const roots=[...document.querySelectorAll(sel)].filter(vis);if(!roots.length)return ['(뿌리 없음) '+sel];
   const all=[];roots.forEach(r=>{all.push(r);r.querySelectorAll('*').forEach(e=>all.push(e))});
   const V=[...new Set(all)].filter(e=>e.getClientRects().length&&vis(e)).slice(0,6000);
   V.forEach(e=>{const cs=getComputedStyle(e),ox=cs.overflowX;
     if((ox==='auto'||ox==='scroll')&&e.scrollWidth>e.clientWidth+1&&e.clientWidth>0&&!e.closest('.katex-display'))out.push('hscroll:'+sig(e));
     if((ox==='hidden'||ox==='clip')&&e.scrollWidth>e.clientWidth+1&&e.clientWidth>0&&cs.textOverflow!=='ellipsis'&&e.children.length===0&&tx(e))out.push('clip:'+sig(e));
     const r=e.getBoundingClientRect();if(r.width>0&&(r.right>innerWidth+1||r.left<-1)&&cs.position!=='fixed'&&getComputedStyle(e.parentElement||e).overflowX==='visible')out.push('offscreen:'+sig(e))});
   const A=V.filter(e=>e.matches(__H.ACT)&&!e.disabled&&getComputedStyle(e).pointerEvents!=='none');
   const fl=e=>{for(let q=e;q&&q!==document.body;q=q.parentElement){const ps=getComputedStyle(q).position;if(ps==='fixed'||ps==='sticky')return !roots.some(r=>r===q||q.contains(r))}return false};
   const AS=A.filter(e=>!fl(e));
   for(let i=0;i<AS.length;i++)for(let j=i+1;j<AS.length;j++){const a=AS[i],b=AS[j];if(a.contains(b)||b.contains(a))continue;
     const p=a.getBoundingClientRect(),q=b.getBoundingClientRect(),ix=Math.min(p.right,q.right)-Math.max(p.left,q.left),iy=Math.min(p.bottom,q.bottom)-Math.max(p.top,q.top);
     if(ix>2&&iy>2)out.push('overlap:'+sig(a)+'|'+sig(b))}
   if(touch)A.slice(0,300).forEach(e=>{if(!fl(e))try{e.scrollIntoView({block:'center',inline:'nearest'})}catch(x){}const h=__H.hitBox(e),r=e.getBoundingClientRect();
     if(h.on&&((Math.round(r.height)<36&&h.h<36)||(Math.round(r.width)<36&&h.w<36)))out.push('small:'+sig(e))});
   return [...new Set(out)]}
};
"""

RES = []


def T(g, name, ok, detail=''):
    RES.append((g, name, bool(ok), detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', g, name, d[:700]), flush=True)
    return ok


def N(g, name, detail=''):
    RES.append((g, name, None, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('INFO | %s · %s | %s' % (g, name, d[:900]), flush=True)


# ════════════════════════ 관문 ════════════════════════
DEVS = (('폰390', PHONE), ('iPad820', PAD))
PA_SAMPLES = (('PA0801', '2008 변리사 1번'), ('PA1109', '2011 변리사 9번'), ('PA2403', '2024 변리사 3번'))
TX_SAMPLES = ('PEM0101', 'PEM0809', 'PEE0204')   # 교재 문항(연도 0) — 바탕 이름 그대로여야(PET0302 꼴 = 연도 있는 PE 코드 72 = 기출 쪽)
NO = "c => { const r = DATA.find(x => x[F.CODE] === c); return r ? r[F.NO] : null; }"


def fresh(br, tag, src, subj='phys', dev=PHONE, eng=None, who='하네스', remote=None):
    return Pg(br, eng or br.browser_type.name, tag, src, subj, dev, who=who, remote=remote)   # 엔진 = 받은 브라우저 종류(WebKit 을 CDP 길로 보내지 않는다)


def open_view(p, no, wait=2200):
    p.ev("async no => { await openView(no); }", no)
    p.wait(wait)


WK_DRAG = r"""([x, y, ty]) => { const t = ty === 'pointerdown' ? document.elementFromPoint(x, y) : (window.__tdT || document.elementFromPoint(x, y)); if (ty === 'pointerdown') window.__tdT = t;
  t.dispatchEvent(new PointerEvent(ty, {bubbles: true, cancelable: true, composed: true, pointerId: 8, pointerType: 'touch', isPrimary: true, clientX: x, clientY: y, button: 0, buttons: ty === 'pointerup' ? 0 : 1})); return t.tagName; }"""


def touch_drag(p, x, y, dx, dy, steps=10):
    if p.eng == 'webkit':   # 합성 touch 포인터(WebKit 은 CDP 가 없다)
        p.ev(WK_DRAG, [x, y, 'pointerdown'])
        for i in range(1, steps + 1):
            p.wait(16)
            p.ev(WK_DRAG, [x + dx * i / steps, y + dy * i / steps, 'pointermove'])
        p.ev(WK_DRAG, [x + dx, y + dy, 'pointerup'])
        p.wait(300)
        return
    c = p._cdp()
    c.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'id': 1}]})
    for i in range(1, steps + 1):
        p.wait(16)
        c.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x + dx * i / steps, 'y': y + dy * i / steps, 'id': 1}]})
    c.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    p.wait(300)


CENTER = r"""() => { const a = document.elementFromPoint(innerWidth / 2, innerHeight / 2); if (!a) return null; const w = a.closest('#view, #jnw, #mcw, #pwl, .sheet'); return w ? (w.id || w.className) : ('other:' + (a.id || a.className)); }"""
ZS = r"""() => ['view', 'jnw', 'mcw', 'pwl'].map(id => { const e = document.getElementById(id); return e && !e.classList.contains('hide') ? [id, +getComputedStyle(e).zIndex || 0] : null; }).filter(Boolean)"""
VISPT = r"""(id) => { const w = document.getElementById(id); if (!w) return null; const p = w.querySelector('.panel') || w; const r = p.getBoundingClientRect();
  for (let y = r.top + 6; y < r.bottom - 4; y += 14) for (let x = r.left + 8; x < r.right - 8; x += 20){ const a = document.elementFromPoint(x, y); if (a && w.contains(a) && !a.closest('button, a, input, textarea, [data-go]')) return {cx: x, cy: y, on: true}; } return null; }"""


def b1(br, src, base_src, tag):
    """A-1 누른 창 앞으로 — 물리 정리 창 번호 → 가운데 = 문항 창 · 뒤 창 누름 → 그 창 맨 앞 · 🃏 창도 · 지학 z 순서 = 바탕"""
    G = 'B1'
    ok = True
    for dn, dev in DEVS:
        p = fresh(br, tag + dn, src, 'phys', dev)
        sec = p.ev("() => Object.keys(TOC.sec)[0]")
        p.ev("s => jnOpen(s)", sec)
        p.wait(500)
        at = p.ev("() => __H.hit(document.querySelector('#jnw .jnrow .jgo'))")
        p.press(at, 2500)
        c1, z1 = p.ev(CENTER), p.ev(ZS)
        g1 = c1 == 'view'
        # 뒤 창(정리 창) 누름 — 폰은 문항 창이 다 덮으므로 문항 창 머리를 손가락으로 끌어 내려 정리 창을 드러낸다
        pt = p.ev(VISPT, 'jnw')
        if not pt:
            t = p.ev("() => __H.R(document.querySelector('#view .vtop .title'))")
            touch_drag(p, t['cx'], t['cy'], 0, 380)
            pt = p.ev(VISPT, 'jnw')
        if pt:
            p.press(pt, 500)
        z2 = p.ev(ZS)
        top2 = max(z2, key=lambda x: x[1])[0] if z2 else None
        g2 = bool(pt) and top2 == 'jnw'
        # 🃏 창
        p.ev("() => { const w = document.getElementById('jnw'); if (w) w.remove(); try{ closeView(); }catch(e){} }")
        p.wait(300)
        p.ev("() => mcwOpen('all')")
        p.wait(800)
        at3 = p.ev("() => __H.hit(document.querySelector('#mcw .jgo'))")
        p.press(at3, 2500)
        c3, z3 = p.ev(CENTER), p.ev(ZS)
        g3 = bool(at3) and c3 == 'view'
        ok = ok and g1 and g2 and g3
        T(G, '%s 물리 정리 창 번호 → 가운데 = 문항 창' % dn, g1, {'가운데': c1, 'z': z1})
        T(G, '%s 뒤 정리 창 누름 → 맨 앞' % dn, g2, {'누른 곳': pt and [round(pt['cx']), round(pt['cy'])], 'z': z2})
        T(G, '%s 🃏 창 「보기」 → 가운데 = 문항 창' % dn, g3, {'가운데': c3, 'z': z3})
        if p.errs:
            ok = False
            T(G, '%s JS 오류' % dn, False, p.errs[:3])
        p.close()
    # 지학 z 순서 = 바탕
    zz = {}
    for which, s in (('new', src), ('base', base_src)):
        p = fresh(br, tag + 'E' + which, s, 'earth', PHONE)
        p.ev("s => jnOpen(s)", p.ev("() => Object.keys(TOC.sec)[0]"))
        p.wait(500)
        p.press(p.ev("() => __H.hit(document.querySelector('#jnw .jnrow .jgo'))"), 2500)
        zz[which] = (p.ev(ZS), p.ev(CENTER))
        p.close()
    g4 = zz['new'] == zz['base']
    ok = ok and g4
    T(G, '지학 폰 정리 창 → 문항 창 z 순서 = 바탕', g4, zz)
    return ok


ROWS = r"""() => [...document.querySelectorAll('#jnw .jnrow')].map(r => { const h = r.querySelector('.h'), g = h.querySelector('.jgo'), n = h.querySelector('.mut'), k = [...h.children].filter(__H.vis).pop();
  /* 옛: return {no: +r.dataset.no, go: __H.tx(g), name: __H.tx(n), gf: getComputedStyle(g).fontSize + ' ' + getComputedStyle(g).fontWeight, nf: getComputedStyle(n).fontSize + ' ' + getComputedStyle(n).fontWeight, */
  /* ★ uid_unify G-1(10/4 · gigu/_task_jagwa_uid_unify.md §G-1) — 새 판 카드 층(지학) 기출 uid 줄은 .mut(이름)을 안 그린다(n = null) → nf 만 빈칸으로(이름 있는 줄 · 물리 줄은 옛 식 값 그대로) */
  return {no: +r.dataset.no, go: __H.tx(g), name: __H.tx(n), gf: getComputedStyle(g).fontSize + ' ' + getComputedStyle(g).fontWeight, nf: n ? getComputedStyle(n).fontSize + ' ' + getComputedStyle(n).fontWeight : '',
    drop: !!k && k !== g && (k.getBoundingClientRect().top - g.getBoundingClientRect().top) > Math.max(8, g.getBoundingClientRect().height * 0.6)}; })"""


def jn_all(p):
    """물리 모든 절의 정리 창 줄 — {no: row}"""
    out = {}
    for sec in p.ev("() => Object.keys(TOC.sec)"):
        p.ev("s => jnOpen(s)", sec)
        p.wait(120)
        for r in p.ev(ROWS):
            out[r['no']] = r
    p.ev("() => { const w = document.getElementById('jnw'); if (w) w.remove(); }")
    return out


PNM = r"""(no) => { const e = document.querySelector('#jnw .jnrow[data-no="' + no + '"] .pnm'); if (!e) return null; e.scrollIntoView({block: 'center'});
  return {t: e.textContent, fx: e.classList.contains('fx'), pen: getComputedStyle(e, '::after').content, ied: e.classList.contains('ied'), at: __H.at(e)}; }"""
LIST = r"""(code) => { const it = [...document.querySelectorAll('#list .item')].find(x => { const n = x.querySelector('.num'); return n && n.textContent.trim() === code; }); if (!it) return null; const s = it.querySelector('.sub'); return {sub: __H.tx(s), fx: s.classList.contains('pnfx')}; }"""


# ★ uid_unify G-1(10/4) — .jnrow .h 안에 임시 .mut 를 넣어 CSS 규칙(줄 머리 이름 글자)만 재는 JS · 이름 있는 줄이 한 줄도 없을 때만 쓴다
MUTPROBE = r"""() => { const h = document.querySelector('#jnw .jnrow .h'); if (!h) return null; const s = document.createElement('span'); s.className = 'mut'; s.textContent = 'x'; h.appendChild(s);
  const c = getComputedStyle(s), v = c.fontSize + ' ' + c.fontWeight; s.remove(); return v; }"""


def earth_ref(pe, re_):
    """지학 정리 창의 (번호 글자, 이름 글자) 기준 — 이름(.mut)이 있는 첫 줄. 옛 판은 모든 줄에 이름이 있어 첫 줄 = 옛 식(re_[0]) 그대로.
    새 판(§G-1)은 기출 uid 줄이 이름을 안 그리므로 이름 있는 줄(확인문제 등)이 나오는 절까지 훑고 · 끝내 없으면 CSS 규칙 값을 임시 .mut 로 잰다."""
    r0 = next((r for r in re_ if r['nf']), None)
    if r0 is None and re_:
        for sec in (pe.ev("() => Object.keys(TOC.sec)") or [])[1:]:
            pe.ev("s => jnOpen(s)", sec)
            pe.wait(120)
            r0 = next((r for r in pe.ev(ROWS) if r['nf']), None)
            if r0:
                break
    if r0:
        return (r0['gf'], r0['nf'])
    nf = pe.ev(MUTPROBE)
    return (re_[0]['gf'], nf) if re_ and nf else None


def b2(br, src, base_src, tag):
    G = 'B2'
    ok = True
    pn, pb, pe = fresh(br, tag + 'n', src), fresh(br, tag + 'b', base_src), fresh(br, tag + 'e', src, 'earth')
    rn, rb = jn_all(pn), jn_all(pb)
    pe.ev("s => jnOpen(s)", pe.ev("() => Object.keys(TOC.sec)[0]"))
    pe.wait(400)
    re_ = pe.ev(ROWS)
    # 옛 줄: ef = (re_[0]['gf'], re_[0]['nf']) if re_ else None
    ef = earth_ref(pe, re_)   # ★ uid_unify G-1 — 이름(.mut) 있는 첫 줄 기준(옛 판 = re_[0] 그대로)
    nf = sorted(set((r['gf'], r['nf']) for r in rn.values()))
    g1 = nf == [ef]
    ok = ok and g1
    T(G, '물리 정리 창 번호·이름 글자 = 지학 값', g1, {'물리': nf, '지학': ef, '바탕 물리': sorted(set((r['gf'], r['nf']) for r in rb.values()))})
    nos = {c: pn.ev(NO, c) for c, _ in PA_SAMPLES}
    g2 = all(rn.get(nos[c], {}).get('name') == want for c, want in PA_SAMPLES)
    ok = ok and g2
    T(G, '기출 표본 셋 = 「연도 변리사 N번」', g2, [(c, rn.get(nos[c], {}).get('name')) for c, _ in PA_SAMPLES])
    tx = {c: pn.ev(NO, c) for c in TX_SAMPLES}
    g3 = all(tx[c] and rn.get(tx[c], {}).get('name') == rb.get(tx[c], {}).get('name') for c in TX_SAMPLES)
    ok = ok and g3
    T(G, '교재 표본 셋 = 바탕 이름', g3, [(c, rn.get(tx[c], {}).get('name'), rb.get(tx[c], {}).get('name')) for c in TX_SAMPLES])
    pe.ev("() => { const w = document.getElementById('jnw'); if (w) w.remove(); }")
    en = 0
    for sec in pe.ev("() => Object.keys(TOC.sec)"):
        pe.ev("s => jnOpen(s)", sec)
        pe.wait(120)
        en += sum(1 for r in pe.ev(ROWS) if r['drop'])
    dn_, db_ = sum(1 for r in rn.values() if r['drop']), sum(1 for r in rb.values() if r['drop'])
    g4 = dn_ == 0 or dn_ <= en
    ok = ok and g4
    T(G, '마크 줄 떨어짐 = 0(또는 지학 수준)', g4, {'새 판 물리': '%d/%d' % (dn_, len(rn)), '바탕 물리': '%d/%d' % (db_, len(rb)), '지학(새 판)': en})
    pb.close()
    pe.close()
    # 길게 누르기 = 그 자리 고치기(진짜 터치 550ms)
    p = pn
    no = nos['PA0801']
    p.ev("s => jnOpen(s)", p.ev("n => unitOf(n)", no))
    p.wait(500)
    a0 = p.ev(PNM, no)
    p.long_press(a0['at']['cx'], a0['at']['cy'], 550, 400)
    ed = p.ev(r"""(no) => { const e = document.querySelector('#jnw .jnrow[data-no="' + no + '"] .pnm'); const i = e.querySelector('input'), ok = e.querySelector('.iedok');
      return {ied: e.classList.contains('ied'), val: i ? i.value : null, focus: document.activeElement === i, ok: ok ? __H.hitBox(ok) : null}; }""", no)
    g5 = ed['ied'] and ed['focus'] and ed['val'] == a0['t'] and ed['ok'] and ed['ok']['h'] >= 36 and ed['ok']['w'] >= 36
    ok = ok and g5
    T(G, '이름 길게 누름 → 입력 칸 + ✓(≥ 36)', g5, ed)
    p.pg.keyboard.press('Control+A')
    p.pg.keyboard.type('역학 기출 첫 문제')
    p.pg.keyboard.press('Enter')
    p.wait(600)
    a1 = p.ev(PNM, no)
    ls = p.ev(LIST, 'PA0801')
    p.ev("async () => { stampAll(); await syncRecords(true); }")
    p.wait(500)
    rem = (p.remote.rec('phys') or {}).get('data', {}).get('tfix', {})
    g6 = a1['t'] == '역학 기출 첫 문제' and a1['fx'] and '✎' in (a1['pen'] or '') and ls and ls['fx'] and ls['sub'].startswith('역학 기출 첫 문제') and rem.get('P%03d' % no, {}).get('nm') == '역학 기출 첫 문제'
    ok = ok and g6
    T(G, '저장 → 이름 바뀜 + ✎ · 첫 화면 줄 같은 이름 · 올린 몸통에 그 칸', g6, {'정리 창': (a1['t'], a1['fx'], a1['pen']), '첫 화면': ls, '올린 tfix': rem})
    p.reload()
    p.ev("s => jnOpen(s)", p.ev("n => unitOf(n)", no))
    p.wait(500)
    a2 = p.ev(PNM, no)
    g7 = a2['t'] == '역학 기출 첫 문제' and a2['fx']
    ok = ok and g7
    T(G, '새로고침 뒤 남음', g7, (a2['t'], a2['fx']))
    p.long_press(a2['at']['cx'], a2['at']['cy'], 550, 400)
    p.pg.keyboard.press('Control+A')
    p.pg.keyboard.press('Backspace')
    p.pg.keyboard.press('Enter')
    p.wait(500)
    a3 = p.ev(PNM, no)
    g8 = a3['t'] == '2008 변리사 1번' and not a3['fx']
    ok = ok and g8
    T(G, '비우고 저장 = 원래 이름', g8, (a3['t'], a3['fx'], p.ev("() => JSON.stringify(TFIX)")))
    p.long_press(a3['at']['cx'], a3['at']['cy'], 550, 400)
    p.pg.keyboard.type('XYZ')
    p.tap(PHONE[0] // 2, 24, 400)
    a4 = p.ev(PNM, no)
    g9 = a4['t'] == '2008 변리사 1번' and not a4['ied'] and not a4['fx']
    ok = ok and g9
    T(G, '바깥 누름 = 취소', g9, (a4['t'], a4['ied']))
    p.tap(a4['at']['cx'], a4['at']['cy'], 500)
    a5 = p.ev(PNM, no)
    vh = p.ev("() => document.getElementById('view').classList.contains('hide')")
    g10 = not a5['ied'] and a5['t'] == '2008 변리사 1번' and vh
    gat = p.ev("(no) => __H.hit(document.querySelector('#jnw .jnrow[data-no=\"' + no + '\"] .jgo'))", no)
    p.tap(gat['cx'], gat['cy'], 1800)
    g10 = g10 and p.ev("() => !document.getElementById('view').classList.contains('hide') && VNO") == no
    ok = ok and g10
    T(G, '짧게 누름 무변(이름 = 그대로 · 번호 = 문항 열기)', g10, {'이름 톡 뒤 편집': a5['ied'], '문항 창': not vh})
    if p.errs:
        ok = False
        T(G, 'JS 오류', False, p.errs[:3])
    p.close()
    return ok


def b3(br, src, base_src, tag):
    G = 'B3'
    ok = True
    p = fresh(br, tag + 'n', src)
    fr0 = p.ev("() => JSON.stringify(FR)")
    p.ev("() => pwList('f')")
    p.wait(500)
    tabs = p.ev("() => [...document.querySelectorAll('#pwl .pftabs button')].map(b => __H.tx(b))")
    sheet = p.ev(r"""() => { const b = document.getElementById('pwlBody'); const heads = [...b.querySelectorAll('.pwh')].map(h => __H.tx(h)); const g = [...b.querySelectorAll('.pfg')].map(x => __H.tx(x));
      const n = g.reduce((a, t) => a + (+((/· (\d+)식$/.exec(t) || [])[1] || 0)), 0); return {heads, groups: g.length, n, none: [...b.querySelectorAll('.pfnone')].length}; }""")
    g1 = (tabs == ['시트', '백지 인출', '단위·기초'] and sheet['groups'] == 15 and sheet['n'] == 85 and sheet['none'] == 5 or tabs == ['공식', '백지 인출', '단위·기초'] and sheet['groups'] == 51 and sheet['n'] == 244 and sheet['none'] == 0) and sheet['heads'][0].startswith('1. 역학')   # ★ 2026-10-07 (_task_jagwa_phys_win §A-22·A-40) — 탭 「시트」→「공식」 · 공식시트 2~6편 36묶음 159식 더함(15→51 묶음 · 85→244 식 · 「공식 아직 없음」 5→0)
    ok = ok and g1
    T(G, '위 공식 탭 셋 · 시트 = 15묶음 85식이 단원 자리에 · 2~6장 「공식 아직 없음」', g1, {'탭': tabs, **sheet})
    p.ev("() => document.querySelector('#pwl [data-pft=u]').click()")
    p.wait(800)
    u = p.ev(r"""() => { const s0 = THEORY.sec.find(x => String(x.id) === '0'); const b = document.getElementById('pwlBody');
      const blocks = b.querySelectorAll('.thsec > .thl, .thsec > .thpicbox, .thsec > .thtbw, .thsec > .thbr').length;
      return {want: s0.b.length, wantImg: s0.b.filter(x => x.g).length, got: blocks, img: b.querySelectorAll('.thpicbox').length, broken: /0\.\s*·\s*1/.test(__H.tx(b)) || /^0\./.test(__H.tx(b))}; }""")
    g2 = u['got'] == u['want'] and u['img'] == u['wantImg'] and not u['broken']
    ok = ok and g2
    T(G, '단위·기초 = THEORY 첫 절 블록 수·그림 수 같음 · 「0. · 1」 0', g2, u)
    p.ev("() => document.querySelector('#pwl [data-pft=b]').click()")
    p.wait(400)
    dots = p.ev("() => document.querySelectorAll('#pwl .frdot').length")
    nfr = p.ev("() => Object.keys(FR).length")
    g3 = dots == nfr == 7
    ok = ok and g3
    T(G, '백지 인출 O/X 기록 7건 보임', g3, {'점': dots, 'FR': nfr})
    chips = p.ev("() => document.querySelectorAll('.jjn[data-frm]').length")
    pb = fresh(br, tag + 'b', base_src)
    chips_b = pb.ev("() => document.querySelectorAll('.jjn[data-frm]').length")
    pb.close()
    # 옛 줄: g4 = chips == chips_b == 19
    g4 = chips == chips_b == 19 or ('function pfDecor(' in src and chips_b == 19 and chips == 62)   # ★ 2026-10-08 (_task_jagwa_phys_win §A-40) 공식시트 2~6편 → 목차 단원 칩 19 → 62(1 단계 잰 값 · 바탕 19 그대로)
    ok = ok and g4
    T(G, '목차 칩 19 그대로', g4, {'새 판': chips, '바탕': chips_b})
    # 공식·조건·함정 길게 눌러 고치기 → 세 자리 같은 글 · FR 무변
    p.ev("() => document.querySelector('#pwl [data-pft=s]').click()")
    p.wait(300)
    p.ev("() => document.querySelector('#pwl .pfg').click()")
    p.wait(600)
    K = p.ev("() => frKey(FRM[0], FRM[0].r[2])")
    NEWT = {'f': '$v=v_0+at$ (고침)', 'c': '가속도 일정할 때만(고침)', 't': '부호를 처음에 정한다(고침)'}
    for sl in ('f', 'c', 't'):
        at = p.ev(r"""([k, sl]) => { const e = [...document.querySelectorAll('#pwl .frcell')].find(x => x.dataset.fk === k && x.dataset.fs === sl); return e ? __H.hit(e) : null; }""", [K, sl])
        p.long_press(at['cx'], at['cy'], 550, 400)
        p.pg.keyboard.press('Control+A')
        p.pg.keyboard.type(NEWT[sl])
        p.pg.keyboard.press('Enter')
        p.wait(400)
    CELLS = r"""([k]) => { const o = {}; [...document.querySelectorAll('.frcell')].filter(x => x.dataset.fk === k).forEach(x => { const w = x.closest('#pwl') ? 'pwl' : (x.closest('.frmpanel') ? 'chip' : '?'); (o[w] = o[w] || {})[x.dataset.fs] = x.textContent.replace(/\s+/g, ' ').trim(); }); return o; }"""
    c1 = p.ev(CELLS, [K])
    p.ev("() => document.querySelector('.jjn[data-frm]').click()")
    p.wait(700)
    c2 = p.ev(CELLS, [K])
    p.ev("() => document.querySelectorAll('.frmpanel').forEach(x => x.closest('.sheet').remove())")
    p.ev("() => document.querySelector('#pwl [data-pft=b]').click()")
    p.wait(400)
    p.ev(r"""([k]) => { const r = [...document.querySelectorAll('#pwl .frmrow.frhide')].find(x => x.dataset.k === k); if (r) r.querySelector('[data-rv]').click(); }""", [K])
    p.wait(400)
    c3 = p.ev(CELLS, [K])
    fx = p.ev("(k) => TFIX['F|' + k]", K)
    same = lambda d: d and all(NEWT[sl] in d.get(sl, '') or (sl == 'f' and '고침' in d.get(sl, '')) for sl in ('f', 'c', 't'))
    g5 = same(c1.get('pwl')) and same(c2.get('chip')) and same(c3.get('pwl')) and p.ev("() => JSON.stringify(FR)") == fr0 and fx == NEWT
    ok = ok and g5
    T(G, '공식·조건·함정 길게 눌러 고침 → 위 공식 · 목차 칩 창 · 백지 인출 같은 글 · FR 무변', g5, {'위 공식': c1.get('pwl'), '칩 창': c2.get('chip'), '백지 인출': c3.get('pwl'), 'TFIX': fx, 'FR 같음': p.ev("() => JSON.stringify(FR)") == fr0})
    th = p.ev("() => __H.tx(document.getElementById('tTheory'))")
    g6 = th == '이론'
    ok = ok and g6
    T(G, '#tTheory 글 「이론」', g6, th)
    if p.errs:
        ok = False
        T(G, 'JS 오류', False, p.errs[:3])
    p.close()
    return ok


def b4(br, src, tag):
    G = 'B4'
    ok = True
    for subj in ('phys', 'earth'):
        p = fresh(br, tag + subj, src, subj, PHONE)
        p.ev("s => jnOpen(s)", p.ev("() => Object.keys(TOC.sec)[0]"))
        p.wait(500)
        x = p.ev(r"""() => { const b = document.getElementById('jnwX'), t = document.querySelector('#jnw .bplh > span'); const cs = getComputedStyle(t);
          return {txt: __H.tx(b), hit: __H.hitBox(b), at: __H.at(b), one: t.getBoundingClientRect().height < parseFloat(cs.lineHeight || '20') * 1.6 && cs.whiteSpace === 'nowrap', ell: cs.textOverflow}; }""")
        p.press(x['at'], 500)
        gone = p.ev("() => !document.getElementById('jnw')")
        g = x['txt'] == '✕' and x['hit']['h'] >= 36 and x['hit']['w'] >= 36 and x['one'] and x['ell'] == 'ellipsis' and gone
        ok = ok and g
        T(G, '%s 정리 창 ✕ 누름 ≥ 36 · 닫힘 · 제목 한 줄' % subj, g, {'✕': x['txt'], '누름': x['hit'], '한 줄': x['one'], '말줄임': x['ell'], '닫힘': gone})
        p.close()
    return ok


HEAD = r"""() => { const v = document.getElementById('view'), vr = v.getBoundingClientRect(), R = e => e.getBoundingClientRect();
  const ids = ['vBack', 'tm', 'vWinTg', 'vPrev', 'vNext'], els = ids.map(i => document.getElementById(i)).filter(__H.vis), t = document.querySelector('#view .vtop .title');
  const tops = els.concat([t]).map(e => Math.round(R(e).top)); const t1 = document.getElementById('vT1'), cs = getComputedStyle(t1);
  const pill = document.getElementById('inkPill'), gg = document.querySelector('#view .ggline'), gb = document.getElementById('ggphys'), wrap = document.getElementById('wrap');
  return {oneLine: Math.max(...tops) - Math.min(...tops) <= 4, tops, backL: Math.round(R(document.getElementById('vBack')).left - vr.left),
    btn: els.map(e => [e.id, __H.hitBox(e).h, __H.hitBox(e).w]), ell: cs.textOverflow === 'ellipsis' && cs.overflow === 'hidden' && cs.whiteSpace === 'nowrap',
    pillB: pill ? Math.round(R(pill).bottom) : null, ggT: gg ? Math.round(R(gg).top) : null, ggInHead: !!(gg && gg.closest('.vtop')), ggInCard: !!(gg && gg.closest('#card')),
    card: gb ? [getComputedStyle(gb.querySelector('.ggtop') || gb).borderTopWidth, !!gb.closest('#stage')] : null, wrapT: wrap ? Math.round(R(wrap).top - vr.top) : null}; }"""
GGACT = r"""async () => { const box = document.querySelector('#view .ggbox'); if (!box) return null; const lab = box.querySelector('.ggrow .lab'), txt = box.querySelector('.ggrow .txt');
  lab.value = 'ㄱ'; lab.dispatchEvent(new Event('input', {bubbles: true})); txt.value = '관문 근거'; txt.dispatchEvent(new Event('input', {bubbles: true}));
  const n0 = box.querySelectorAll('.ggrow').length; box.querySelector('[data-ggplus]').click(); await new Promise(r => setTimeout(r, 200));
  const n1 = box.querySelectorAll('.ggrow').length; const fb = box.querySelector('.ggfind'); const h0 = fb.classList.contains('hide'); box.querySelector('[data-ggfind]').click(); await new Promise(r => setTimeout(r, 200));
  return {rows: [n0, n1], find: [h0, box.querySelector('.ggfind').classList.contains('hide')], save: !box.querySelector('[data-ggsave]').classList.contains('hide')}; }"""


def b5(br, src, base_src, tag):
    G = 'B5'
    ok = True
    heads = {}
    for subj, code in (('phys', 'PA0801'), ('earth', 'G11-48-03'), ('bio', 'B20-57-05')):
        for which, s in (('new', src), ('base', base_src)):
            p = fresh(br, tag + subj + which, s, subj, PHONE)
            no = p.ev(NO, code)
            open_view(p, no, 2600)
            h = p.ev(HEAD)
            act = p.ev(GGACT) if subj == 'phys' else None
            heads[(subj, which)] = (h, act)
            p.close()
        h, hb = heads[(subj, 'new')][0], heads[(subj, 'base')][0]
        g = h['oneLine'] and h['backL'] <= 12 and all(b[1] >= 36 and b[2] >= 36 or b[0] in ('vBack', 'vWinTg', 'vPrev', 'vNext') and b[1] >= 30 and b[2] >= 30 for b in h['btn']) and h['ell']   # ★ 2026-10-07 (_task_jagwa_phys_win §A-04) — 시안 ⑧⑨ ✕ · ⤢ · ◀ · ▶ = 작은 칩 · 손가락 기기 누를 자리 30px(옛 36)
        ok = ok and g
        T(G, '폰 390 %s 머리 한 줄 · 서재 left − 창 left ≤ 12 · 단추 ≥ 36 · 제목 말줄임' % subj, g, {'한 줄': (hb['oneLine'], '→', h['oneLine']), '서재 왼쪽': (hb['backL'], '→', h['backL']), '단추': h['btn'], '말줄임': h['ell']})
        if subj == 'phys':
            a, ab = heads[(subj, 'new')][1], heads[(subj, 'base')][1]
            g2 = h['ggInHead'] and h['ggT'] is not None and h['pillB'] is not None and h['ggT'] > h['pillB'] and h['card'] and h['card'][0] == '0px' and not h['card'][1] and h['wrapT'] < hb['wrapT'] and a == ab
            ok = ok and g2
            T(G, '물리 근거 칸 = 필기 도구 아랫줄 · 따로 카드 0 · PDF 쪽이 바탕보다 위 · 근거 입력·＋·🔍 무변', g2,
              {'근거 top / 도구 bottom': (h['ggT'], h['pillB']), '카드(테두리·stage 안)': h['card'], 'PDF top(창 기준)': (hb['wrapT'], '→', h['wrapT']), '동작': (ab, a)})
        if subj == 'earth':
            g3 = h['ggInCard'] and hb['ggInCard']
            ok = ok and g3
            T(G, '지학 근거 칸 = 카드 안 그대로', g3, {'새 판': h['ggInCard'], '바탕': hb['ggInCard']})
    return ok


TH6 = r"""() => { const u = document.createElement('div'); u.innerHTML = UNITS.sec.map(s => '<div class="thsec">' + (s.b || []).map(pwLineHTML).join('') + '</div>').join('');
  const t = document.createElement('div'); t.innerHTML = THEORY.sec.map(secHTML).join('');
  const f = el => ({span: (el.textContent.match(/<\/?span/g) || []).length, star: [...el.querySelectorAll('.thl')].filter(x => /^\s*[*-] /.test(x.textContent)).length, marks: el.querySelectorAll('mark').length});
  return {units: f(u), theory: f(t)}; }"""


def b6(br, src, tag):
    G = 'B6'
    p = fresh(br, tag, src)
    p.ev("() => pwList('c')")
    p.wait(500)
    p.ev("() => { const r = [...document.querySelectorAll('#pwl .pwr')].find(x => x.dataset.id === '1.1.3'); if (r) return r.click(); const w = document.getElementById('pwl'), bd = w && w.querySelector('#pwlBody'), x = bd && bd.querySelector('.cws[data-sec=\"1.1.3\"]'); if (x && w.__cwOpen) { bd.scrollTop += x.getBoundingClientRect().top - bd.getBoundingClientRect().top; w.__cwOpen('R'); } }")   # ★ 2026-10-07 (_task_jagwa_phys_win §A-39) — 시안 ㊹ 위 「개념」 = cwOpen(물리 목차 통째 · 옛 .pwr 줄 없음) · 1.1.3 개별 단원 파일 = 그 절에서 여는 오른 덮개(.thcR · 같은 pwLineHTML 줄)
    p.wait(600)
    c = p.ev(r"""() => { const bd = ([...document.querySelectorAll('#pwl .pwr')].find(x => x.dataset.id === '1.1.3') || {}).nextElementSibling || document.querySelector('#pwl .thcR .thsec');   /* ★ 2026-10-07 (_task_jagwa_phys_win §A-39) — ㊹ 새 꼴 = 오른 덮개의 1.1.3 줄 */
      return {span: (bd.textContent.match(/<\/?span/g) || []).length, marks: [...bd.querySelectorAll('mark')].map(m => [m.textContent, getComputedStyle(m).backgroundColor]), star: [...bd.querySelectorAll('.thl')].filter(x => /^\s*[*-] /.test(x.textContent)).length}; }""")
    want = [['지면', 'rgb(210, 203, 255)'], ['물체', 'rgba(240, 167, 216, 0.55)']]
    g1 = c['span'] == 0 and c['marks'] == want and c['star'] == 0
    T(G, '개념 1.1.3 — 글자 <span 0 · 형광 2 · 색 = 원래 값 · 「* 」「- 」 줄 0', g1, c)
    a = p.ev(TH6)
    g2 = a['units']['span'] == 0 and a['units']['star'] == 0 and a['theory']['span'] == 0 and a['theory']['star'] == 0 and a['units']['marks'] == 2
    T(G, '전체 UNITS · THEORY 줄 — 글자 태그 0 · 「* 」「- 」 시작 줄 0', g2, a)
    p.close()
    return g1 and g2


# ── A-2-4 동기화(칸 도장 · 묘비 · 두 기기 병합) + 옛 판 기기 틈(새 SYNC 키 tfix — 잰 것을 결과에 적는다) ──
def edit_name(p, no, text):
    """정리 창 이름 길게 누름(진짜 터치 550ms) → 입력 → Enter · text='' = 비우고 저장(= 원래 이름 = 그 칸 지움)"""
    p.ev("s => jnOpen(s)", p.ev("n => unitOf(n)", no))
    p.wait(400)
    a = p.ev(PNM, no)
    if not a:
        return False
    p.long_press(a['at']['cx'], a['at']['cy'], 550, 400)
    if not p.ev("() => !!document.querySelector('#jnw .pnm.ied input')"):
        return False
    p.pg.keyboard.press('Control+A')
    if text:
        p.pg.keyboard.type(text)
    else:
        p.pg.keyboard.press('Backspace')
    p.pg.keyboard.press('Enter')
    p.wait(400)
    p.ev("() => { const w = document.getElementById('jnw'); if (w) w.remove(); }")
    return True


SYNC = "async () => { stampAll(); await syncRecords(true); }"


def b2s(br, src, base_src, tag):
    G = 'B2S'
    ok = True
    rm = Remote()
    A = fresh(br, tag + 'A', src, who='새판A', remote=rm)
    n0, n1 = A.ev(NO, 'PA0801'), A.ev(NO, 'PA1109')
    k0, k1 = 'P%03d' % n0, 'P%03d' % n1
    e1 = edit_name(A, n0, '가 이름')
    A.ev(SYNC)
    A.wait(400)
    r1 = rm.rec('phys') or {}
    d1 = (r1.get('data') or {}).get('tfix') or {}
    g1 = e1 and d1.get(k0, {}).get('nm') == '가 이름' and bool((r1.get('u') or {}).get('tfix|' + k0))
    ok = ok and g1
    T(G, '새 판 A 이름 고침 → 올린 몸통 data.tfix 칸 + 칸 도장 u[tfix|P###]', g1, {'고침': e1, 'data.tfix': d1, 'u': {k: v for k, v in (r1.get('u') or {}).items() if k.startswith('tfix|')}})
    D = fresh(br, tag + 'D', src, who='새판D', remote=rm)
    D.ev("s => jnOpen(s)", D.ev("n => unitOf(n)", n0))
    D.wait(300)
    dshow = (D.ev(PNM, n0) or {}).get('t')
    D.ev("() => { const w = document.getElementById('jnw'); if (w) w.remove(); }")
    g2 = dshow == '가 이름'
    ok = ok and g2
    T(G, '새 기기 D 켬 → 받은 이름이 정리 창에 보임', g2, dshow)
    # 병합 — A 는 둘째 칸을 고치고 D 는 첫 칸을 비운다(묘비) · 서로 다른 칸이라 둘 다 살아야 · 지운 이름은 안 되살아나야
    e2 = edit_name(A, n1, '나 이름')
    e3 = edit_name(D, n0, '')
    D.ev(SYNC)
    D.wait(300)
    A.ev(SYNC)
    A.wait(300)
    D.ev(SYNC)
    D.wait(300)
    r2 = rm.rec('phys') or {}
    ta, td = json.loads(A.ev("() => JSON.stringify(TFIX)")), json.loads(D.ev("() => JSON.stringify(TFIX)"))
    g3 = e2 and e3 and ta == td and ta.get(k1, {}).get('nm') == '나 이름' and k0 not in ta and ('tfix|' + k0) in (r2.get('gone') or {}) and k0 not in ((r2.get('data') or {}).get('tfix') or {})
    ok = ok and g3
    T(G, '두 기기 병합 — A 가 고친 칸 · D 가 지운 칸(묘비) 둘 다 산다 · 지운 이름 안 되살아남', g3,
      {'A': ta, 'D': td, '묘비': {k: v for k, v in (r2.get('gone') or {}).items() if k.startswith('tfix|')}, 'data.tfix': (r2.get('data') or {}).get('tfix')})
    # 옛 판 기기(바탕 앱 · SYNC_KEYS 에 tfix 없음) 틈
    B = fresh(br, tag + 'B', base_src, who='옛판B', remote=rm)
    B.ev(SYNC)
    B.wait(400)
    r3 = rm.rec('phys') or {}
    lost = 'tfix' not in (r3.get('data') or {})
    kept_u = ('tfix|' + k1) in (r3.get('u') or {})
    C = fresh(br, tag + 'C', src, who='새판C', remote=rm)
    c0 = json.loads(C.ev("() => JSON.stringify(TFIX)"))
    A.ev("async () => { await syncRecords(true); }")
    A.wait(400)
    r4 = rm.rec('phys') or {}
    back = ((r4.get('data') or {}).get('tfix') or {}).get(k1, {}).get('nm') == '나 이름'
    chip = A.ev("() => __H.tx(document.getElementById('recChip'))")
    C.ev("async () => { await syncRecords(true); }")
    C.wait(400)
    c1 = json.loads(C.ev("() => JSON.stringify(TFIX)"))
    N(G, '옛 판 기기 틈(잰 것)', {'옛 판 B 올림 뒤 원격 data.tfix': '빠짐' if lost else '남음', '원격 u[tfix|…] 도장': '남음' if kept_u else '빠짐',
                             '그 사이 새로 켠 새 판 C': c0 or '못 받음(빈 TFIX)', '새 판 A 다음 동기화 뒤 원격 data.tfix': '되살아남' if back else '안 돌아옴',
                             'A 칩': chip, 'C 다시 동기화 뒤': c1})
    g4 = kept_u and back and c1.get(k1, {}).get('nm') == '나 이름' and not B.errs and not B.ev("() => __H.errs()")
    ok = ok and g4
    T(G, '옛 판 기기 올림 뒤 — 도장 u 남음 · 새 판 기기 다음 동기화에 data.tfix 되살림 · 새 기기 C 받음 · 옛 판 JS 오류 0', g4,
      {'u 남음': kept_u, '되살림': back, 'C': c1, '옛 판 오류': B.errs[:2]})
    for q in (A, D, B, C):
        if q.errs:
            ok = False
            T(G, 'JS 오류 ' + q.pg.url[-20:], False, q.errs[:3])
        q.close()
    return ok


# ── B-7 화면 훑기 ──
def sweep_screens(br, src, tag, dev):
    """한 기기 — {화면: [흠 이름표]} · 그림 = SHOTS/<tag>_<화면>.png"""
    p = fresh(br, tag, src, 'phys', dev)
    touch = dev != PC
    out = {}
    sw = lambda sel: p.ev("a => __H.sweep(a[0], a[1])", [sel, touch])
    shot = lambda k: p.shot('%s_%s' % (tag, k))
    clear = "() => { ['jnw', 'mcw', 'pwl'].forEach(i => { const w = document.getElementById(i); if (w) w.remove(); }); document.querySelectorAll('.sheet').forEach(s => { if (s.querySelector('.frmpanel')) s.remove(); }); try { closeView(); } catch (e) {} }"
    root = p.ev("() => { const c = [...document.querySelectorAll('.pwchip')].find(__H.vis); if (!c) return null; let e = c.parentElement; while (e && !e.id) e = e.parentElement; return e ? '#' + e.id : null; }")
    out['첫 화면 위'] = sw(root) if root else ['(칩 없음)']
    shot('home')
    p.ev("s => jnOpen(s)", p.ev("() => Object.keys(TOC.sec)[0]"))
    p.wait(500)
    out['정리 창'] = sw('#jnw')
    shot('jnw')
    p.ev(clear)
    p.ev("() => mcwOpen('all')")
    p.wait(900)
    out['🃏 창'] = sw('#mcw')
    shot('mcw')
    p.ev(clear)
    p.ev("() => pwList('f')")
    p.wait(600)
    for k, t in (('s', '위 공식 시트'), ('b', '위 공식 백지 인출'), ('u', '위 공식 단위·기초')):
        p.ev("k => { const b = document.querySelector('#pwl [data-pft=' + k + ']'); if (b) b.click(); }", k)
        p.wait(700)
        if k == 's':
            p.ev("() => { const g = document.querySelector('#pwl .pfg') || document.querySelector('#pwl .pwr'); if (g) g.click(); }")
            p.wait(700)
        out[t] = sw('#pwl')
        shot('pf_' + k)
    p.ev(clear)
    p.ev("() => { const c = document.querySelector('.jjn[data-frm]'); if (c) { c.scrollIntoView({block: 'center'}); c.click(); } }")
    p.wait(800)
    p.ev("() => { const f = document.querySelector('.frmpanel'); if (f) f.closest('.sheet').setAttribute('data-hsw', '1'); }")
    out['목차 공식 창'] = sw('[data-hsw="1"]')
    shot('frmsheet')
    p.ev(clear)
    p.ev("() => pwList('c')")
    p.wait(600)
    p.ev("() => { const r = [...document.querySelectorAll('#pwl .pwr')].find(x => x.dataset.id === '1.1.3'); if (r) r.click(); }")
    p.wait(700)
    out['개념 창'] = sw('#pwl')
    shot('concept')
    p.ev(clear)
    open_view(p, p.ev(NO, 'PA0801'), 2600)
    out['문항 창 머리'] = sw('#view .vtop, #view .ggbox')
    shot('view')
    errs = p.errs[:] + (p.ev("() => __H.errs()") or [])
    p.close()
    return out, errs


_KTX = re.compile(r'^offscreen:(?:mi|mn|mo|ms|mtext|mrow|msup|msub|msubsup|mfrac|msqrt|mroot|mover|munder|munderover|mtable|mtr|mtd|mspace|mpadded|mstyle|semantics|annotation|math|span\.(?:katex|katex-mathml|katex-html|base|mord|mbin|mrel|mopen|mclose|mpunct|minner|mop|vlist|vlist-t|vlist-r|vlist-s|vlist-t2|pstrut|sizing|strut|accent|frac-line|sqrt|svg-align|hide-tail))(?::|$)')


def _b7_ok(scr, sig, newd):   # ★ 2026-10-08 (_task_jagwa_phys_win §A-38 ㊸ · §A-39 ㊹ · §A-40 · §A-13 ㉑㉕) 새 판 표지(newd)일 때만 받는 새 흠 이름표
    if not newd:
        return False
    if scr == '첫 화면 위' and sig == '(칩 없음)':
        return True   # §A-38 ㊸ 칩 = 서랍 머리(첫 화면엔 없음 · 자리 = 관문 jagwa_phys_win #31·#63)
    if scr in ('위 공식 시트', '위 공식 백지 인출', '위 공식 단위·기초', '목차 공식 창', '개념 창') and _KTX.match(sig):
        return True   # §A-40 공식 2~6편 · §A-39 ㊹ 개념 = 물리 목차 통째 — KaTeX 속 MathML(화면 밖으로 잘라 둔 접근성 글) 이름표
    if scr == '개념 창' and sig.startswith('hscroll:div.thtbw:'):
        return True   # §A-39 ㊹ 이론 표 가로 굴림 감싸개(.thtbw)
    if scr == '문항 창 머리' and sig == 'small:button#tCut':
        return True   # §A-13 ㉑㉕ ✂ 오리기(필기 알약 ↺ 오른쪽 · 작은 아이콘)
    return False


def b7(br, src, base_src, tag):
    G = 'B7'
    ok = True
    newd = 'function pfDecor(' in src   # ★ 2026-10-08 (_task_jagwa_phys_win) 새 판 표지
    for dn, dev in (('폰390', PHONE), ('iPad820', PAD), ('PC', PC)):
        n, en = sweep_screens(br, src, tag + 'N' + dn, dev)
        b, eb = sweep_screens(br, base_src, tag + 'B' + dn, dev)
        for scr in n:
            new = sorted(set(n[scr]) - set(b.get(scr, [])))
            gone = sorted(set(b.get(scr, [])) - set(n[scr]))
            acc = [s for s in new if _b7_ok(scr, s, newd)]   # ★ 2026-10-08 (_task_jagwa_phys_win) §A 근거로 받는 새 이름표
            new = [s for s in new if s not in acc]
            good = not new
            ok = ok and good
            T(G, '%s %s 새로 생긴 흠 0' % (dn, scr), good, {'새로': new[:8], '없어짐': gone[:6], '남은(바탕에도 있음)': len(set(n[scr]) & set(b.get(scr, []))),
                                                       **({'받음(§A · 뜻한 차)': acc[:8], '받음 수': len(acc)} if acc else {})})
        if en:
            ok = False
            T(G, '%s JS 오류' % dn, False, en[:3])
    N(G, '그림', SHOTS)
    return ok


# ── B-8 회귀(규칙 57) — 저장소 하네스를 그대로 돌린다(새 판 · 바탕 cedc251 두 번 · 칸마다 견줌) ──
#   클라우드 틈: 하네스들이 윈도 크롬 자리를 박아 두었고 cdnjs 가 막혀 있다 → 돌릴 때만 씌움(REG_SHIM):
#   크롬 자리 → Playwright Chromium(--no-sandbox) · cdnjs → --vendor 사본(크롬 = 로컬 https 사본 + host-resolver-rules · Playwright = route) · 하네스 파일은 안 고친다
#   자리: GENIE_ROOT = 임시 사본(jagwa/index.html = 그 판 · HEAD = 그 하네스의 바탕 판 · 나머지 jagwa/* = genie 로 잇기) · TEMP = 임시 · 결과 파일은 임시로
REGS = (
    ('phys', ('moolri', '_harness_phys.py'), [], None),
    ('phys_P', ('moolri', '_harness_phys_P.py'), [], None),
    ('phys_filter', ('moolri', '_harness_phys_filter.py'), [], None),
    ('phys_twin', ('moolri', '_harness_phys_twin.py'), [], None),
    ('phone_win', ('_harness_jagwa_phone_win.py',), ['--eng', 'chromium', '--res', '{TMP}/phone_win_result.txt'], 'fd911d5'),
    ('penfinger', ('gigu', '_harness_jagwa_penfinger.py'), ['--new', '{APP}', '--base', '{BASEAPP}'], '72a65b3'),
    ('earth listpop', ('gigu', '_harness_earth_listpop.py'), ['earth'], None),
)
#   덧 파일 — 하네스가 제 바탕 사본을 찾는 자리(임시 GENIE_ROOT 안) = genie git 판(얕은 클론이면 그 커밋만 받아 둔다: git fetch --depth=2 origin a9f9fd4fee37…)
REG_EXTRA = {'earth listpop': {('jagwa', 'index.html.before_listpop'): 'a9f9fd4~1'}}
#   뜻한 변경 — 이 지시서가 바꾸라고 한 것을 옛 하네스가 옛 꼴로 잰 칸(칸 이름 앞머리 · 까닭). 회귀가 아니라 「뜻한 변경」으로 따로 적는다(옛 하네스 = N: 정본 사본이라 안 고친다)
#   셋째 = 새 판 로그로 「바뀐 것이 그것뿐」인지 재는 잣대(참이어야 뜻한 변경 · 거짓이면 회귀로 센다)
def _pw7_rect(log):
    """phone_win 7 — 새 창도 옛 목록 창과 같은 자리·크기(좌 8 · 폭 374 · 높이 72% 608)"""
    ln = next((l for l in log.splitlines() if l.startswith('FAIL | 7 · chromium [공식] 목록 창')), '')
    return bool(re.search(r'"rect": \{"x": 8, "y": [\d.]+, "w": 374, "h": 608\}', ln))


def _pf7_move(log):
    """penfinger phys 7 — DOM 해시만 다르고 #stage 손가락 끌기 결과(move)는 바탕(72a65b3)과 같다"""
    mv = {}
    for l in log.splitlines():
        m = re.match(r'NOTE \| (BASE|NEW) phys · 7 .*? \| (\{.*\})\s*$', l)
        if m:
            try:
                mv[m.group(1)] = json.loads(m.group(2)).get('move')
            except Exception:
                pass
    return 'BASE' in mv and mv.get('BASE') == mv.get('NEW') and mv.get('NEW') is not None


EXPECT = {
    'phone_win': (('7 · chromium [공식] 목록 창', 'A-3 위 「공식」 = THEORY 51단원 목록 → 공식 시트(FRM) 세 탭(창 자리·크기는 같음)', _pw7_rect),
                  ('7 · chromium [공식] 1.1.1 ▸', 'A-3 같은 까닭(옛 목록 줄 1.1.1 이 없다 · 새 창은 묶음 줄 .pfg)', None)),
    'penfinger': (('NEW phys · 7 물리 문제 창 DOM', 'A-3-4 #tTheory 「이론」 · A-5 머리 한 줄 · 근거 칸 = 머리 안(DOM 해시·#stage 높이 다름 · 손가락 끌기 결과는 같음)', _pf7_move),),
}
#   하네스가 제 자리(genie 사본 안)에 쓰는 결과 파일 — 돌린 뒤 로그 폴더로 옮기고, 전에 있던 것은 되돌린다(저장소에 안 남긴다)
REG_STRAY = {'penfinger': (('gigu', '_harness_jagwa_penfinger_result.txt'),)}
REG_SHIM = r'''
import os, sys, runpy, subprocess, inspect
H = sys.argv[1]; sys.argv = sys.argv[1:]
WIN = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
CH, VEND, PORT = os.environ.get('H_CHROMIUM', ''), os.environ.get('H_VENDOR', ''), os.environ.get('H_CDN_PORT', '')
_P = subprocess.Popen
class _P2(_P):
    def __init__(self, args, *a, **k):
        if isinstance(args, (list, tuple)) and args and str(args[0]) == WIN and not os.path.exists(WIN) and CH:
            ex = ['--no-sandbox', '--no-proxy-server', '--ignore-certificate-errors']
            if PORT:
                ex.append('--host-resolver-rules=MAP cdnjs.cloudflare.com 127.0.0.1:%s, MAP * ~NOTFOUND, EXCLUDE 127.0.0.1, EXCLUDE localhost' % PORT)
            args = [CH] + ex + list(args[1:])
        super().__init__(args, *a, **k)
subprocess.Popen = _P2
try:
    from playwright.sync_api._generated import BrowserContext, Page
    PRE = 'https://cdnjs.cloudflare.com/ajax/libs/'
    def _wrap(orig):
        def route(self, url, handler, *a, **k):
            n = len(inspect.signature(handler).parameters)
            def h2(rt):
                u = rt.request.url.split('?')[0]
                if VEND and u.startswith(PRE):
                    f = os.path.join(VEND, *u[len(PRE):].split('/'))
                    if os.path.isfile(f):
                        ct = 'text/css' if f.endswith('.css') else ('font/woff2' if f.endswith('.woff2') else 'application/javascript')
                        return rt.fulfill(status=200, body=open(f, 'rb').read(), content_type=ct, headers={'Access-Control-Allow-Origin': '*'})
                return handler(rt) if n < 2 else handler(rt, rt.request)
            return orig(self, url, h2, *a, **k)
        return route
    BrowserContext.route = _wrap(BrowserContext.route)
    Page.route = _wrap(Page.route)
except Exception as e:
    print('[shim] playwright 못 씌움', e, flush=True)
runpy.run_path(H, run_name='__main__')
'''


WIN_CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'


def cdn_https(vendor):
    """cdnjs 로컬 https 사본(자체 서명 · 크롬은 --ignore-certificate-errors) — 포트"""
    import ssl
    d = os.path.join(tempfile.gettempdir(), 'h_jagwa', 'tls')
    os.makedirs(d, exist_ok=True)
    key, crt = os.path.join(d, 'k.pem'), os.path.join(d, 'c.pem')
    if not os.path.isfile(crt):
        subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-keyout', key, '-out', crt, '-days', '3',
                        '-subj', '/CN=cdnjs.cloudflare.com', '-addext', 'subjectAltName=DNS:cdnjs.cloudflare.com'], capture_output=True)

    class Hd(SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
            pre = '/ajax/libs/'
            return os.path.join(vendor, *[x for x in p[len(pre):].split('/') if x]) if p.startswith(pre) else os.path.join(vendor, '__없음__')

    srv = ThreadingHTTPServer(('127.0.0.1', 0), Hd)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(crt, key)
    srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


def reg_root(tag, app_text, head_rev, extra=None):
    """임시 GENIE_ROOT — jagwa/index.html = 이 판(작업 글) · git HEAD = head_rev 판(없으면 바탕) · 나머지 jagwa/* 는 genie 로 잇기 · extra = {조각: git 판}"""
    import shutil
    d = os.path.join(tempfile.gettempdir(), 'h_jagwa', 'reg', tag)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, 'jagwa'))
    for x in os.listdir(_roots.genie('jagwa')):
        if x != 'index.html':
            os.symlink(_roots.genie('jagwa', x), os.path.join(d, 'jagwa', x))
    f = os.path.join(d, 'jagwa', 'index.html')
    open(f, 'wb').write(app_src(head_rev).encode('utf-8'))
    g = ['git', '-C', d, '-c', 'user.name=h', '-c', 'user.email=h@h']
    subprocess.run(g + ['init', '-q'], capture_output=True)
    subprocess.run(g + ['add', 'jagwa/index.html'], capture_output=True)
    subprocess.run(g + ['commit', '-q', '-m', 'head ' + head_rev], capture_output=True)
    open(f, 'wb').write(app_text.encode('utf-8'))
    for parts, rev in (extra or {}).items():
        b = git('show', rev + ':jagwa/index.html')
        if b:
            open(os.path.join(d, *parts), 'wb').write(b)
    return d


def reg_parse(txt):
    """PASS/FAIL 줄 → {이름: [판정…]} (이름 = 판정 뒤 첫 ' | ' 앞까지)"""
    out = {}
    for ln in txt.splitlines():
        m = re.match(r'\s*(PASS|FAIL)\s*\|\s*(.+?)(?:\s\|\s|$)', ln)
        if m:
            out.setdefault(m.group(2).strip(), []).append(m.group(1))
    return out


def reg_run(name, parts, args, head_rev, which, app_text, env0, tmp):
    import shutil
    hf = os.path.join(os.path.dirname(HERE), *parts)
    src_h = open(hf, encoding='utf-8').read()
    if 'need_n(' in src_h or '_roots.n(' in src_h:
        return None, 'N: 필요 — 합칠 때 본 세션', ''
    root = reg_root(name.replace(' ', '_') + '_' + which, app_text, head_rev or BASE, REG_EXTRA.get(name))
    t = os.path.join(tmp, name.replace(' ', '_') + '_' + which)
    shutil.rmtree(t, ignore_errors=True)
    os.makedirs(t)
    af = os.path.join(t, 'app.html')
    open(af, 'wb').write(app_text.encode('utf-8'))
    bf = os.path.join(t, 'base.html')
    open(bf, 'wb').write(app_src(head_rev or BASE).encode('utf-8'))
    a = [x.replace('{TMP}', t).replace('{APP}', af).replace('{BASEAPP}', bf) for x in args]
    env = dict(env0, GENIE_ROOT=root, TEMP=t, TMP=t, LISTPOP_CAP=os.path.join(t, 'cap'), PYTHONIOENCODING='utf-8')
    t0 = time.time()
    strays = [os.path.join(os.path.dirname(HERE), *x) for x in REG_STRAY.get(name, ())]
    keep = {f: open(f, 'rb').read() for f in strays if os.path.isfile(f)}
    try:
        cp = subprocess.run([sys.executable, '-c', REG_SHIM, hf] + a, capture_output=True, env=env, timeout=1500, cwd=t)
        out = cp.stdout.decode('utf-8', 'replace') + '\n' + cp.stderr.decode('utf-8', 'replace')
    except subprocess.TimeoutExpired as e:
        out = ((e.stdout or b'').decode('utf-8', 'replace')) + '\n[시간 넘김 1500초]'
    open(os.path.join(tmp, name.replace(' ', '_') + '_' + which + '.log'), 'w', encoding='utf-8').write(out)
    for f in strays:
        if os.path.isfile(f):
            shutil.move(f, os.path.join(t, os.path.basename(f)))
        if f in keep:
            open(f, 'wb').write(keep[f])
    out = out.replace(root, '<GENIE_ROOT>').replace(t, '<TMP>')   # 칸 이름에 임시 자리가 박힌 하네스(phone_win 9 등) — 두 판 이름이 같게
    return reg_parse(out), '%.0f초 · 끝줄: %s' % (time.time() - t0, (out.strip().splitlines() or [''])[-1][:160]), out


def b8(src, base_src):
    """회귀 — 칸마다 바탕(cedc251)에서 PASS 인데 새 판에서 FAIL 인 것 = 회귀 · 둘 다 FAIL 은 클라우드 틈(바탕에도 있음)"""
    G = 'B8'
    ok = True
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        chromium = pw.chromium.executable_path
    srv, port = None, ''
    if not os.path.exists(WIN_CHROME) and os.path.isdir(VENDOR):   # 클라우드(윈도 크롬 없음)만 — 본 PC 는 하네스 그대로 진짜 크롬 · 진짜 cdnjs
        try:
            srv, port = cdn_https(VENDOR)
        except Exception as e:
            N(G, 'cdnjs https 사본 못 띄움', str(e)[:160])
    env0 = dict(os.environ, H_CHROMIUM=chromium, H_VENDOR=VENDOR if os.path.isdir(VENDOR) else '', H_CDN_PORT=str(port))
    tmp = os.path.join(tempfile.gettempdir(), 'h_jagwa', 'reglog')
    os.makedirs(tmp, exist_ok=True)
    for name, parts, args, head_rev in REGS:
        if ONLY8 and name not in ONLY8:
            continue
        rn, why_n, raw_n = reg_run(name, parts, args, head_rev, 'new', src, env0, tmp)
        if rn is None:
            N(G, name, why_n)
            continue
        rb, why_b, _ = reg_run(name, parts, args, head_rev, 'base', base_src, env0, tmp)
        np_ = sum(v.count('PASS') for v in rn.values())
        nf_ = sum(v.count('FAIL') for v in rn.values())
        bp_ = sum(v.count('PASS') for v in rb.values())
        bf_ = sum(v.count('FAIL') for v in rb.values())
        reg0 = sorted(k for k in rn if 'FAIL' in rn[k] and 'FAIL' not in rb.get(k, ['FAIL']) and k in rb)
        reg0 += sorted(k for k in rb if k not in rn and 'PASS' in rb[k] and 'FAIL' not in rb[k])   # 새 판에서 아예 안 나온 칸(도중에 멈춤) = 회귀로 센다
        exp = EXPECT.get(name, ())
        why = lambda k: next(((w, v) for p_, w, v in exp if k.startswith(p_)), None)
        meant = [(k, why(k)[0]) for k in reg0 if why(k) and (why(k)[1] is None or why(k)[1](raw_n))]
        reg = [k for k in reg0 if k not in dict(meant)]
        fixed = sorted(k for k in rb if 'FAIL' in rb[k] and k in rn and 'FAIL' not in rn[k])
        only_new = sorted(k for k in rn if k not in rb)
        if not rn and not rb:
            N(G, name, '안 돔(두 판 다 PASS/FAIL 줄 0) — 새 판 %s · 바탕 %s · 로그 %s' % (why_n, why_b, tmp))
            continue
        g = not reg
        ok = ok and g
        T(G, '%s 회귀 0(바탕 PASS → 새 판 FAIL 인 칸 0)' % name, g,
          {'새 판': '%d PASS / %d FAIL' % (np_, nf_), '바탕': '%d PASS / %d FAIL' % (bp_, bf_), '회귀': reg[:8], '뜻한 변경(지시서가 바꾼 것 · 회귀 아님)': meant, '바탕 FAIL → 새 판 PASS': fixed[:4],
           '새 판에만 있는 칸': only_new[:4], '둘 다 FAIL(클라우드 틈 · 바탕에도)': sorted(k for k in rn if 'FAIL' in rn[k] and 'FAIL' in rb.get(k, []))[:6], '시간': [why_n, why_b]})
    if srv:
        srv.shutdown()
    N(G, '로그', tmp)
    return ok


ONLY8 = [x.strip() for x in (ARG('--reg', '') or '').split(',') if x.strip()]


def webkit_try(pw):
    try:
        return pw.webkit.launch()
    except Exception as e:
        N('WK', 'WebKit 안 잼', str(e).splitlines()[0][:160])
        return None


ORDER = ('B1', 'B2', 'B2S', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8')


def main():
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    if YARD:
        src = app_src(BASE)
        base_src = src
        print('헛잣대 — 앱 = %s(착수 판) · B-1~B-6 · B2S 가 저마다 FAIL 해야 통과' % BASE)
    else:
        src, base_src = app_src(NEW), app_src(BASE)
        print('관문 _task_jagwa_physphone · 앱 = %s · 바탕 = %s' % (NEW, BASE))
    got = {}
    tm = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        steps = [('B1', lambda: b1(br, src, base_src, 'b1')),
                 ('B2', lambda: b2(br, src, base_src, 'b2')),
                 ('B2S', lambda: b2s(br, src, base_src, 'b2s')),
                 ('B3', lambda: b3(br, src, base_src, 'b3')),
                 ('B4', lambda: b4(br, src, 'b4')),
                 ('B5', lambda: b5(br, src, base_src, 'b5')),
                 ('B6', lambda: b6(br, src, 'b6')),
                 ('B7', lambda: b7(br, src, base_src, 'b7'))]
        for g, fn in steps:
            if ONLY and g not in ONLY:
                continue
            if YARD and g == 'B7':
                N(g, '헛잣대 해당 없음', '화면 훑기 = 새 판 흠 − 바탕 흠 · 바탕끼리 견주면 늘 0(잣대가 아니라 잠금)')
                continue
            print('── %s' % g, flush=True)
            t1 = time.time()
            try:
                got[g] = bool(fn())
            except Exception as e:
                got[g] = False
                T(g, '돌다 멈춤', False, str(e).splitlines()[0][:300])
            tm[g] = time.time() - t1
            print('   (%s %.0f초)' % (g, tm[g]), flush=True)
        br.close()
        if 'webkit' in ENGS and not YARD and (not ONLY or 'WK' in ONLY):
            wk = webkit_try(pw)
            if wk:
                for g, fn in (('B1', lambda: b1(wk, src, base_src, 'wk1')), ('B2', lambda: b2(wk, src, base_src, 'wk2')), ('B3', lambda: b3(wk, src, base_src, 'wk3')),
                              ('B4', lambda: b4(wk, src, 'wk4')), ('B5', lambda: b5(wk, src, base_src, 'wk5'))):
                    try:
                        fn()
                    except Exception as e:
                        T(g + '-wk', 'WebKit 돌다 멈춤', False, str(e).splitlines()[0][:200])
                wk.close()
    if not YARD and (not ONLY or 'B8' in ONLY):
        print('── B8', flush=True)
        t1 = time.time()
        try:
            got['B8'] = bool(b8(src, base_src))
        except Exception as e:
            got['B8'] = False
            T('B8', '돌다 멈춤', False, str(e).splitlines()[0][:300])
        tm['B8'] = time.time() - t1
    if not YARD:
        N('B8', 'qa_baseline 판(_qa_chain compare)', '바탕 cedc251 에 _qa_chain 없음 → 안 함')
    lines = []
    print('\n══ 요약 (%.0f초)%s' % (time.time() - t0, ' — 헛잣대' if YARD else ''))
    for g in [x for x in ORDER if x in got]:
        cells = [r for r in RES if r[0] == g and r[2] is not None]
        nf = sum(1 for r in cells if not r[2])
        verdict = ('FAIL(헛잣대 통과)' if not got[g] else 'PASS(헛잣대 실패)') if YARD else ('PASS' if got[g] else 'FAIL')
        s = '  %-4s %s (%d 칸 중 FAIL %d · %.0f초)' % (g, verdict, len(cells), nf, tm.get(g, 0))
        print(s)
        lines.append(s)
    with open(OUTF, 'w', encoding='utf-8', newline='\n') as f:
        for r in RES:
            d = r[3] if isinstance(r[3], str) else json.dumps(r[3], ensure_ascii=False, default=str)
            f.write('%s | %s · %s | %s\n' % ('INFO' if r[2] is None else ('PASS' if r[2] else 'FAIL'), r[0], r[1], d))
        f.write('\n'.join(lines) + '\n')
    print('결과 → %s' % OUTF)


if __name__ == '__main__':
    main()
