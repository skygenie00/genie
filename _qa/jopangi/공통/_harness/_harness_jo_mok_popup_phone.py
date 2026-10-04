# -*- coding: utf-8 -*-
"""조판기 목차노트 탭 · 팝업 손질(깊이 제한 풀기 · 모두 닫기 · 줄 걷기) · 마우스 길게 누르기 · 폰 화면 — _task_jo_mok_popup_phone §H 관문 하네스.

  NEW  = genie 작업트리 jo/index.html(또는 --new <파일>) · 데이터 = genie jo/data(무접촉)
  BASE = `c9d5bc0` 의 같은 파일(바탕 · 헛잣대 — 새 판이 뜻한 잣대는 BASE 에서 FAIL 이어야 잣대가 산다 · 규칙 ⑩)
  엔진 = playwright chromium · webkit
  화면 = 책상 1440×900(마우스) · PC 1890×907(무변 대조) · 폰 390×844(DSF 3 · 터치) · 아이패드 768×1024 · 1024×768(DSF 2 · 터치)
  터치 = 톡은 두 엔진 다 진짜 터치(touchscreen.tap) · 끌기·길게 누르기 = chromium CDP 터치(끝에서 멈춤) /
         webkit 은 신뢰 마우스(playwright webkit 은 톡만 진짜 터치 — 도구 한계 · 결과에 적는다)
  網 = 같은 출처만 · 시간대 = Asia/Seoul
  ⚠ 자과앱이 아니다(조판기) — 픽셀 게이트는 없다. 재는 것은 DOM·자리·elementFromPoint·앱 상태뿐이고 캡처는 사용자용이다.

쓰기 : python _harness_jo_mok_popup_phone.py [--new 파일] [--out 폴더] [--only rail|bc|depth|probe|all|lp|phone|pc] [--eng chromium|webkit] [--tag BASE|NEW]
       python _harness_jo_mok_popup_phone.py --report [--out 폴더]   (마지막 raw.json 으로 판정만 다시)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402  — _task_qa_slim: --mode · --snap-in · --snap-out 을 여기서 뗀다(아래 인자 읽기는 이 판 앞과 같다 · mokchip 이 이 파일을 불러올 때는 mokchip 이 먼저 불러 둔 같은 모듈)
# --mode gate|regress|smoke (_task_qa_slim 2026-10-04 · 인자 없으면 gate = 이 판 앞과 같다 · gate 경로는 원본과 글자까지 같다 — 갈래는 `if QJ.REGRESS:` · `X if QJ.GATE else Y` 로만 ·
#   mokchip 이 P · serve · SEED · READY · __HM 을 불러 쓰므로 P · serve · SEED · READY · 상수 · 짝 JS 는 gate · regress 어느 쪽에서도 안 바꾼다 — regress 갈래는 부르는 자리에서 가른다)
#   regress = NEW 만 띄운다(바탕 풀기 · 바탕 띄우기 · git 0 · PC 무변 바탕 둘도 안 띄움) · 바탕 값을 기댓값으로 쓰던 칸(C 칩 수 · G > 640 옆 두 칸 · PC 무변)은 기준 스냅샷(QJ.base) ·
#     엔진 × 화면마다 앱 한 번(시나리오 사이 = p.close() 가 reset) · 머리 탭 수 · 목록 · 노트 팝업은 앱 표지로 기다림 · 캡처 안 찍음
#   smoke = rail 시나리오(특허·조문 · 민소·2차 두 칸 — A-1 · 콘솔 오류 0)만 · Chromium 만
import hashlib, http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

GENIE = _roots.genie()
HERE = os.path.dirname(os.path.abspath(__file__))
ARG = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
OUT = ARG('--out', HERE)
ONLY = ARG('--only', '')
ENGS = [ARG('--eng')] if ARG('--eng') else ['chromium', 'webkit']
TAGS = [ARG('--tag')] if ARG('--tag') else ['BASE', 'NEW']
if QJ.REGRESS:   # regress · smoke — 바탕(BASE)은 안 띄운다
    TAGS = ['NEW']
# ── _task_qa_slim — regress(A-1) · 앱 한 번 띄움(A-2) 상수 ──
T_UP = 6000      # 앱 반응(창 뜸 · 닫힘) 기다림 한도(ms) — 반응이 있으면 그 즉시 · 한도까지 가는 것은 반응이 없는(FAIL 갈래) 때뿐
T_LOAD = 30000   # 첫 자료 읽기(머리 탭 수 · 정리 탭 화면) 한도(ms) — 같은 뜻
T_TAIL = 80      # 눌린 뒤 「팝업이 더 뜨지 않나」 보는 여유(ms)
SMOKE_SCEN = ('rail',)                          # smoke — rail 시나리오만(A-1 · 콘솔 오류 0)
SMOKE_TABS = {('특허', 'jo'), ('민소', 'cha2')}   # smoke 에서 도는 (법 · 탭) — 조문 탭 하나 · 2차 탭 하나
NEWF = ARG('--new', os.path.join(GENIE, 'jo', 'index.html'))
WORK = os.path.join(tempfile.gettempdir(), 'h_jo_mok_popup_phone')
SHOTS = os.path.join(OUT, '_mok_popup_phone_shots')
REL = 'jo/index.html'
JOD = os.path.join(GENIE, 'jo')
DATA = os.path.join(JOD, 'data')
BASE_REV = 'c9d5bc0'
BASE_MD5_LF = 'c541b24092c083cbb1dbd4f7c55ab827'
BASE_SIZE = 1017845
PC_BASE = {'jo': 'd42248d', 'card': 'bd8cfdf'}   # A-6(a) 9/30 — PC 무변 대조의 바뀐 뒤 바탕: jo = 조문 팝업을 마지막으로 바꾼 판(revfix0929b · md5(LF) a5e43ca8) · card = c2card 인도판(c5210438) · note·prec 는 BASE_REV 그대로
TESTS = io.open(os.path.join(HERE, '_harness_jo_mok_popup_phone_tests.js'), encoding='utf-8').read()
IPAD_UA = ('Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
PHONE_UA = ('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
N96 = '9.6.{결}정정심판(136)_특무내정정청구(133-2)'
N101 = '10.1.심결취소소송(186)특법-판결'      # ⤷ 임베드가 있는 노트(줄 29 → 4.1.#^be3984)
REF41 = '4.1. 특받자-발명자_승계인_특허권이전,공유_무권리자#^be3984'
PREC = '2021후10374'
CK_2562 = '특기출 25-62-1'
LAWS = [('특허법', '특허'), ('상표법', '상표'), ('민사소송법', '민소'), ('디자인보호법', '디보')]
TABS = {'특허': ['jo', 'prec', 'jimun', 'cha2', 'omr'], '상표': ['jo', 'prec', 'jimun', 'cha2'],
        '디보': ['jo', 'prec', 'jimun', 'cha2'], '민소': ['jo', 'prec', 'cha2', 'omr']}
ORDER = {'특허': ['jo', 'prec', 'jimun', 'cha2', 'mok', 'omr'], '상표': ['jo', 'prec', 'jimun', 'cha2', 'mok'],
         '디보': ['jo', 'prec', 'jimun', 'cha2', 'mok'], '민소': ['jo', 'prec', 'cha2', 'mok', 'omr']}
SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__CONF=[];window.alert=function(){};window.prompt=function(){return null;};
window.confirm=function(m){window.__CONF.push(String(m));return true;};
(function(){var Q=new URLSearchParams(location.search);var nf=window.fetch.bind(window);
window.fetch=function(u,o){var s=String((u&&u.url)||u);
 if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));
 return nf(u,o);};
if(Q.get('keep')!=='1'){try{localStorage.clear();}catch(e){}
 try{localStorage.setItem('tt.cfg',JSON.stringify({person:'꼬까'}));}catch(e){}}
})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
</script>"""
READY = "!!window.__HM&&typeof render==='function'&&typeof popShell==='function'&&!!document.querySelector('#slot')"


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
    """mode = desk(마우스 · DSF 1) · phone(390 · DSF 3 · 터치) · pad(DSF 2 · 터치)"""
    def __init__(self, br, eng, tag, src, W, H, mode='desk'):
        self.eng, self.tag, self.W, self.H, self.mode = eng, tag, W, H, mode
        self.touch = mode in ('phone', 'pad')
        self.port = serve(tag, src)
        kw = dict(viewport={'width': W, 'height': H}, locale='ko-KR', timezone_id='Asia/Seoul')
        if mode == 'phone':
            self.ctx = br.new_context(device_scale_factor=3, is_mobile=True, has_touch=True, user_agent=PHONE_UA, **kw)
        elif mode == 'pad':
            self.ctx = br.new_context(device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=IPAD_UA, **kw)
        else:
            self.ctx = br.new_context(device_scale_factor=1, **kw)
        self.ctx.route('**/*', route_filter)
        self.pg = self.ctx.new_page()
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' else None)
        self.cdp = self.ctx.new_cdp_session(self.pg) if (eng == 'chromium' and self.touch) else None
        self.pg.goto('http://127.0.0.1:%d/index.html?h=1' % self.port, wait_until='load', timeout=120000)
        self.pg.wait_for_function(READY, timeout=120000)
        self.pg.wait_for_timeout(1500)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def click(self, at, wait=600):
        if not at or not at.get('on'):
            return False
        if self.touch:
            self.pg.touchscreen.tap(at['cx'], at['cy'])
        else:
            self.pg.mouse.click(at['cx'], at['cy'])
        self.pg.wait_for_timeout(wait)
        return True

    def cdp_touch(self, ty, x, y):
        self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': ([] if ty == 'touchEnd' else [{'x': x, 'y': y, 'id': 1}])})

    def drag(self, x0, y0, x1, y1, n=14):
        if self.cdp:
            self.cdp_touch('touchStart', x0, y0)
            for i in range(1, n + 1):
                self.cdp_touch('touchMove', x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.pg.wait_for_timeout(16)
            for _ in range(5):
                self.cdp_touch('touchMove', x1, y1); self.pg.wait_for_timeout(30)
            self.cdp_touch('touchEnd', x1, y1)
            self.pg.wait_for_timeout(350)
            return 'cdp-touch'
        m = self.pg.mouse
        m.move(x0, y0); m.down()
        for i in range(1, n + 1):
            m.move(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.pg.wait_for_timeout(16)
        m.up()
        self.pg.wait_for_timeout(350)
        return 'mouse(trusted)' + (' — webkit 끌기는 진짜 터치가 안 된다(도구 한계)' if self.touch else '')

    def longpress(self, x, y, ms=760, touch=False):
        if touch and self.cdp:
            self.cdp_touch('touchStart', x, y); self.pg.wait_for_timeout(ms)
            self.cdp_touch('touchEnd', x, y); self.pg.wait_for_timeout(200)
            return 'cdp-touch'
        m = self.pg.mouse
        m.move(x, y); m.down(); self.pg.wait_for_timeout(ms)
        menu = self.ev("__HM.menu()")
        self.last_bar = self.ev("__HM.bar()")   # A-6(a) 9/30 — joscreen0929 A-5: 조문 줄 칠 막대 둘째 줄(누르는 동안 · mouseup 전)
        m.up(); self.pg.wait_for_timeout(200)
        return menu

    def shot(self, name):
        fn = os.path.join(WORK, 'shot_' + name + '.png'); self.pg.screenshot(path=fn); return fn

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


# ══════════ _task_qa_slim A-2 — regress: 엔진 × 화면마다 앱을 한 번만 띄우고 시나리오 사이는 되돌려 잇는다 ══════════
# (gate 는 시나리오마다 P(...) 새 컨텍스트 그대로 · P 는 안 고친다: 목차노트 칩 하네스(mokchip)가 P 를 불러 쓴다)
RJS = r"""
window.__RJ={
 /* 두 프레임 + 안전 타이머 — 앱 ResizeObserver → hdrFit(앱 2139) 이 한 번 돈 뒤 */
 frames(){return new Promise(res=>{let d=false;const f=()=>{if(!d){d=true;res(true)}};try{requestAnimationFrame(()=>requestAnimationFrame(f))}catch(_){f()}setTimeout(f,300)})},
 /* 머리 탭 수가 다 차고(앱 railCounts 2146 — set() 이 #hrail b[data-n] 마다 글자를 채운다) 목차노트 단추가 켜짐(앱 2167 mb.disabled=!n) · render 끝(busy 꺼짐) */
 railDone(){const bs=[...document.querySelectorAll('#hrail b[data-n]')],m=document.getElementById('mokBtn');
   return bs.length>0&&bs.every(b=>String(b.textContent||'').trim()!=='')&&!!m&&!m.disabled&&typeof busy!=='undefined'&&!busy},
 async untilRail(ms){const t0=performance.now();while(performance.now()-t0<ms){if(__RJ.railDone())return true;await new Promise(r=>setTimeout(r,25))}return false},
 /* 앱 상태 S 첫 기록(부팅 끝 직후) — reset 이 이 값으로 되돌린다(JSON 으로 못 적는 값은 건드리지 않는다) */
 snap(){const o={};for(const k of Object.keys(S)){let v;try{v=JSON.stringify(S[k])}catch(e){v=undefined}o[k]=(typeof v==='string')?v:null}window.__S0=o;return Object.keys(o).length},
 /* IndexedDB — 있는 DB 만 열어 저장소 내용을 비운다(DB 를 지우지 않는다 · 앱이 열어 둔 DB 를 막지 않게 · 앱 15970 ox_master_db) */
 async idbClear(){try{if(!(window.indexedDB&&indexedDB.databases))return 0;const ds=(await indexedDB.databases())||[];let n=0;
   for(const d of ds){if(!d||!d.name)continue;
     await new Promise(res=>{let done=false;const fin=()=>{if(!done){done=true;res(true)}};setTimeout(fin,600);
       try{const rq=indexedDB.open(d.name);rq.onerror=fin;rq.onblocked=fin;
         rq.onsuccess=()=>{const db=rq.result;try{const ns=[...db.objectStoreNames];if(!ns.length){db.close();return fin()}
           const tx=db.transaction(ns,'readwrite');ns.forEach(x=>tx.objectStore(x).clear());n++;
           tx.oncomplete=()=>{try{db.close()}catch(_){}fin()};tx.onerror=()=>{try{db.close()}catch(_){}fin()};tx.onabort=()=>{try{db.close()}catch(_){}fin()}}
         catch(e){try{db.close()}catch(_){}fin()}}}catch(e){fin()}})}
   return n}catch(e){return -1}},
 /* 시나리오 사이 되돌림 — 팝업 닫기 · S 첫 값(팝업 자리·크기 기억 · 서랍 · 조문·판례 선택 …) · 굴림 0 · localStorage(SEED 와 같은 첫 상태) · 오류 목록 · 세는 것 · IndexedDB */
 async reset(){
   try{__HM.clean()}catch(e){}
   try{for(let i=0;i<320&&busy;i++)await new Promise(r=>setTimeout(r,25))}catch(e){}
   try{const o=window.__S0;if(o){for(const k of Object.keys(S)){if(!(k in o))delete S[k]}for(const k of Object.keys(o)){if(o[k]!==null){try{S[k]=JSON.parse(o[k])}catch(e){}}}}}catch(e){}
   try{document.querySelectorAll('#slot .main,#slot .tree,#slot .plist,#slot .qlwrap').forEach(n=>{n.scrollTop=0});const h=document.getElementById('hrail');if(h)h.scrollLeft=0;window.scrollTo(0,0)}catch(e){}
   try{localStorage.clear();localStorage.setItem('tt.cfg',JSON.stringify({person:'꼬까'}))}catch(e){}
   try{if(window.__ERR)window.__ERR.length=0}catch(e){}
   try{__HM.spyReset()}catch(e){}
   try{await __RJ.idbClear()}catch(e){}
   return true}
};
/* __HM.go — 짝 JS 의 go 와 같은 일(clean → idle → S 바꿈 → render → idle) · 끝의 고정 450ms 만 앱 표지(머리 탭 수 다 참 · 단추 켜짐 · 두 프레임)로 — regress 쪽 페이지에서만 */
__HM.go=async function(law,tab,o){__HM.clean();for(let i=0;i<320&&busy;i++)await new Promise(r=>setTimeout(r,25));
  S.law=law;S.tab=tab;
  if(tab==='cha2'){S.boardKind='기출';S.series='';S.yearFilter='';S.cha2Sel=null;S.cha2Filter={};}
  if(tab==='prec'){S.precQ='';S.precFilter={};}
  Object.assign(S,o||{});await render();for(let i=0;i<320&&busy;i++)await new Promise(r=>setTimeout(r,25));
  await __RJ.untilRail(15000);await __RJ.frames();
  return {tab:S.tab,law:S.law}};
0;   /* 마지막 값이 함수면 Playwright evaluate 가 그 함수를 불러 버린다(식이 함수면 자동 호출) — 함수 아닌 값으로 끝낸다 */
"""
# 앱이 이미 내놓는 표지(팝업 키 · 줄 · 머리 탭 글) — 표지 목록 = _qa_slim_out/_a2/_harness_jo_mok_popup_phone_표지.md
JS_MOK_OPEN = "()=>{const p=POPS.find(x=>(x._pk||'').indexOf('moknote|')===0);return !!p&&p.querySelectorAll('.mklist .mkr').length>0}"   # 목차노트 목록 팝업 + 줄(앱 popMokNote 7125)이 찼다
JS_MOK_GONE = "()=>!POPS.find(x=>(x._pk||'').indexOf('moknote|')===0)"                                                               # 같은 단추 다시 = 닫힘(앱 popToggle 3197)
JS_NOTE_OPEN = "n=>!!POPS.find(x=>x._pk==='note|'+PLAW()+'|'+n+'|')"                                                               # 노트 팝업 키(앱 popNote 6786) — 줄은 만들 때 한 번에 찬다
JS_OMR_DONE = "()=>S.tab==='omr'&&__RJ.railDone()"                                                                                   # 「정리」 탭으로 다시 그림 끝 · 머리 탭 수 다 참(앱 drawRail 2131 의 sl 되돌림 포함)


def _wait(pg, ms, why):
    """regress 의 남는 고정 대기 — QJ.sleep(…, page=pg) = page.wait_for_timeout(그동안 ctx.route 콜백 · 요청이 돈다 — time.sleep 은 Playwright 동기 API 에서 route 를 멈춘다) + QJ 대기 셈"""
    QJ.sleep(ms, why, page=pg)


class RigP(P):
    """regress 전용 — P(뿌리 · 안 고침)와 같은 맥락(서버 · 화면 · route · goto · READY)을 한 번만 만들고 시나리오 사이는 reset 으로 되돌려 쓴다.
    P 와 다른 점 셋 — ① 끝의 고정 1.5초 → 앱 표지(첫 render 끝 = busy 꺼짐) ② click 의 고정 대기 = _wait(까닭 · page.wait_for_timeout) ③ close() = 닫지 않고 되돌림(진짜 닫기는 shut)"""

    def __init__(self, br, eng, tag, src, W, H, mode='desk'):
        self.eng, self.tag, self.W, self.H, self.mode = eng, tag, W, H, mode
        self.touch = mode in ('phone', 'pad')
        self.port = serve(tag, src)
        kw = dict(viewport={'width': W, 'height': H}, locale='ko-KR', timezone_id='Asia/Seoul')
        if mode == 'phone':
            self.ctx = br.new_context(device_scale_factor=3, is_mobile=True, has_touch=True, user_agent=PHONE_UA, **kw)
        elif mode == 'pad':
            self.ctx = br.new_context(device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=IPAD_UA, **kw)
        else:
            self.ctx = br.new_context(device_scale_factor=1, **kw)
        self.ctx.route('**/*', route_filter)
        self.pg = self.ctx.new_page()
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' else None)
        self.cdp = self.ctx.new_cdp_session(self.pg) if (eng == 'chromium' and self.touch) else None
        self.dead = False
        self.pg.goto('http://127.0.0.1:%d/index.html?h=1' % self.port, wait_until='load', timeout=120000)
        self.pg.wait_for_function(READY, timeout=120000)
        QJ.until(self.pg, "()=>typeof busy!=='undefined'&&!busy", T_LOAD, '앱 첫 render 끝(busy 꺼짐 · 앱 16561)')   # P 의 고정 1.5초 자리
        self.ev("()=>new Promise(r=>{let d=false;const f=()=>{if(!d){d=true;r(true)}};try{requestAnimationFrame(()=>requestAnimationFrame(f))}catch(_){f()}setTimeout(f,300)})")

    def tap(self, at):
        """P.click 에서 누르기만(뒤 고정 대기 없음)"""
        if self.touch:
            self.pg.touchscreen.tap(at['cx'], at['cy'])
        else:
            self.pg.mouse.click(at['cx'], at['cy'])

    def click(self, at, wait=600):
        """P.click 과 같은 누르기 · 뒤 고정 대기는 _wait(까닭) — 표지를 단 자리는 hit() 가 대신한다"""
        if not at or not at.get('on'):
            return False
        self.tap(at)
        _wait(self.pg, wait, '누른 뒤 앱 반응 — 완료 표지가 팝업 종류마다 달라 고정(_a2 표지 문서 「남는 고정 대기」)')
        return True

    def close(self):
        """시나리오 함수들의 finally: p.close() — 닫지 않고 되돌린다"""
        try:
            self.pg.evaluate("()=>__RJ.reset()")
            self.errs[:] = []
        except Exception:
            self.dead = True

    def shut(self):
        P.close(self)


class Rig(object):
    """regress — (엔진, 화면) 마다 RigP 하나"""

    def __init__(self):
        self.pool = {}

    def lease(self, br, eng, tag, src, W, H, mode):
        key = (eng, W, H, mode)
        q = self.pool.get(key)
        if q is not None and (q.dead or q.pg.is_closed()):
            self.pool.pop(key, None)
            try:
                q.shut()
            except Exception:
                pass
            q = None
        if q is None:
            QJ.launch('new')
            q = RigP(br, eng, tag, src, W, H, mode)
            q.ev(RJS)
            q.ev("()=>__RJ.snap()")
            self.pool[key] = q
        return q

    def shut(self):
        for q in list(self.pool.values()):
            try:
                q.shut()
            except Exception:
                pass
        self.pool.clear()


RIG = Rig()


def rhit(p, at, js, arg, what):
    """regress 누르기 — 누른 뒤 고정 wait 대신 앱 표지(js)가 참이 될 때까지(gate 는 호출 자리의 `p.click(at, wait)` 그대로 — 원본 줄)"""
    if not at or not at.get('on'):
        return False
    p.tap(at)
    QJ.until(p.pg, js, T_LOAD if js is JS_OMR_DONE else T_UP, what, arg)
    p.ev("()=>__RJ.frames()")
    _wait(p.pg, T_TAIL, '눌린 뒤 팝업이 더 뜨는지(S.tab 무변 · 목록 팝업만 같은 칸) 보는 여유 — 앱 표지 뒤에 남는 유일한 고정 대기')
    return True


# ══════════ 잣대 — 데이터에서 센 값 ══════════
def ground():
    G = {'nf': {}}
    for law, sh in LAWS:
        G['nf'][sh] = len(json.load(open(os.path.join(DATA, 'note_' + sh + '.json'), encoding='utf-8')))
    NP = json.load(open(os.path.join(DATA, 'note_특허.json'), encoding='utf-8'))
    G['emb101'] = sum(1 for r in NP[N101]['행'] for e in (r.get('e') or []) if e.get('k') == 'E' and not e.get('miss'))
    B = json.load(open(os.path.join(DATA, 'note_backlink.json'), encoding='utf-8'))
    G['bl96'] = sum(1 for k in B if k.startswith(N96 + '#^'))
    G['plinkData'] = 0
    for fn in os.listdir(DATA):
        if fn.endswith('.json') and (fn.startswith('note_') or fn.startswith('prec_') or fn.startswith('2cha_본문')):
            G['plinkData'] += open(os.path.join(DATA, fn), encoding='utf-8').read().count('"k":"P"')
    return G


# ══════════ A — 가로 탭 「목차노트 N」(책상 1440×900 · 마우스) ══════════
def scen_rail(br, eng, tag, src, G):
    if QJ.GATE:
        QJ.launch('new' if tag == 'NEW' else 'base')
    p = P(br, eng, tag, src, 1440, 900) if QJ.GATE else RIG.lease(br, eng, tag, src, 1440, 900, 'desk')
    R = {'eng': eng, 'tag': tag, 'has': None, 'v': {}}
    try:
        R['has'] = p.ev("__HM.has()")
        for law, sh in LAWS:
            for tab in TABS[sh]:
                if QJ.SMOKE and (sh, tab) not in SMOKE_TABS:
                    continue
                k = sh + '|' + tab
                p.ev("([l,t])=>__HM.go(l,t)", [law, tab])
                p.pg.wait_for_timeout(250) if QJ.GATE else _wait(p.pg, 250, '탭 화면 레이아웃 안정(머리 줄 hdrFit · 배지 줄) — 앱 표지 없음(go 가 머리 탭 수 · 두 프레임까지는 기다린다)')
                V = {'rail': p.ev("__HM.rail()"), 'st0': p.ev("__HM.state()")}
                at = p.ev("__HM.mokAt()")
                V['at'] = at
                V['tap'] = p.click(at, 1200) if QJ.GATE else rhit(p, at, JS_MOK_OPEN, None, '목차노트 탭 누름 = 목록 팝업 줄 참(앱 popMokNote 7125)')
                V['list'] = p.ev("__HM.mokList()"); V['st1'] = p.ev("__HM.state()"); V['mr'] = p.ev("__HM.mokRect()")
                V['rail1'] = p.ev("__HM.rail()")
                at2 = p.ev("__HM.mokAt()")
                V['tap2'] = p.click(at2, 700) if QJ.GATE else rhit(p, at2, JS_MOK_GONE, None, '목차노트 탭 다시 누름 = 목록 팝업 닫힘(앱 popToggle 3197)')
                V['list2'] = p.ev("__HM.mokList()"); V['st2'] = p.ev("__HM.state()")
                R['v'][k] = V
        R['errs'] = p.ev("__HM.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


# ══════════ B·C — 목록 안내 글 · 노트 머리 줄 · 줄 칩 수 · 깊이 딱지 ══════════
def scen_bc(br, eng, tag, src, G):
    if QJ.GATE:
        QJ.launch('new' if tag == 'NEW' else 'base')
    p = P(br, eng, tag, src, 1440, 900) if QJ.GATE else RIG.lease(br, eng, tag, src, 1440, 900, 'desk')
    R = {'eng': eng, 'tag': tag, 'law': {}}
    try:
        for law, sh in LAWS:
            p.ev("([l,t])=>__HM.go(l,t)", [law, 'cha2'])
            L = {}
            at = p.ev("__HM.mokAt()")
            L['tap'] = p.click(at, 1200) if QJ.GATE else rhit(p, at, JS_MOK_OPEN, None, '목차노트 탭 누름 = 목록 팝업 줄 참(앱 popMokNote 7125)')
            L['list'] = p.ev("__HM.mokList()")
            at = p.ev("n=>__HM.mokRowAt(n)", N96 if sh == '특허' else '')
            L['rowAt'] = at
            L['rowTap'] = p.click(at, 1400) if QJ.GATE else rhit(p, at, JS_NOTE_OPEN, (at or {}).get('note'), '목록 줄 누름 = 노트 팝업 뜸(앱 popNote 6786 · mokOpenNote 7148)')
            nm = (at or {}).get('note')
            if nm:
                p.ev("n=>__HM.noteWait(n)", nm)
                L['note'] = p.ev("n=>__HM.noteInfo(n)", nm)
            L['pops'] = p.ev("__HM.pops()")
            R['law'][sh] = L
            p.ev("__HM.clean()")
        R['errs'] = p.ev("__HM.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


# ══════════ D — 깊이 1→2→3→4→5→6 실제로 눌러 쌓기(책상 · 마우스) ══════════
def scen_depth(br, eng, tag, src, G):
    if QJ.GATE:
        QJ.launch('new' if tag == 'NEW' else 'base')
    p = P(br, eng, tag, src, 1440, 900) if QJ.GATE else RIG.lease(br, eng, tag, src, 1440, 900, 'desk')
    R = {'eng': eng, 'tag': tag, 'steps': []}
    S_ = R['steps']

    def snap(name, at, tapped):
        S_.append({'step': name, 'at': at, 'tap': tapped, 'st': p.ev("__HM.state()"), 'spy': p.ev("__HM.spy()"), 'badges': p.ev("__HM.depthBadges()")})
    try:
        p.ev("([l,t])=>__HM.go(l,t)", ['특허법', 'cha2'])
        p.ev("__HM.spyReset()")
        at = p.ev("__HM.mokAt()"); snap('1 목록(탭)', at, p.click(at, 1200) if QJ.GATE else rhit(p, at, JS_MOK_OPEN, None, '목차노트 탭 누름 = 목록 팝업 줄 참(앱 popMokNote 7125)'))
        at = p.ev("n=>__HM.mokRowAt(n)", N96); snap('2 노트(목록 줄)', at, p.click(at, 1400) if QJ.GATE else rhit(p, at, JS_NOTE_OPEN, N96, '목록 줄 누름 = 노트 팝업 뜸(앱 popNote 6786)'))
        p.ev("n=>__HM.noteWait(n)", N96)
        at = p.ev("([s,t])=>__HM.chipAtTop(s,t)", ['.ntbl .chip.c-prec', '^판례 ']); snap('3 목록(노트 줄 칩 판례)', at, p.click(at, 1200))
        # 4 — 목록의 판례 줄 → 판례 팝업 · 그 안에 누를 링크가 없으면 닫고 다음 줄(최대 8)
        ok4 = False
        for i in range(8):
            at = p.ev("i=>(async()=>{const p=POPS.slice().sort((a,b)=>(+b.style.zIndex||0)-(+a.style.zIndex||0))[0];if(!p)return null;const r=[...p.querySelectorAll(':scope > .pb .res')][i];if(!r)return null;r.scrollIntoView({block:'center'});await new Promise(z=>setTimeout(z,200));const b=r.getBoundingClientRect();const x=b.left+b.width/2,y=b.top+b.height/2;const at=document.elementFromPoint(x,y);return {cx:x,cy:y,on:!!at&&r.contains(at),i:i,t:(r.textContent||'').slice(0,30)};})()", i)
            if not at or not at.get('on'):
                break
            tapped = p.click(at, 1500)
            lk = p.ev("__HM.linkAtTop()")
            st = p.ev("__HM.state()")
            if st['pops'] >= 4 and lk and lk.get('on'):
                snap('4 판례(목록 줄 %d)' % i, at, tapped); ok4 = True
                R['link5'] = lk
                break
            if st['pops'] < 4:
                snap('4 판례(목록 줄 %d)' % i, at, tapped)
                break
            p.ev("()=>{const p=POPS.slice().sort((a,b)=>(+b.style.zIndex||0)-(+a.style.zIndex||0))[0];if(p)closeOne(p);return POPS.length;}")
        def lift(n):
            """PC showPop 은 바탕 규칙 그대로(내용이 차기 전 키로 자리) — 화면 아래에서 연 깊은 팝업은 몸통이 화면 밖일 수 있다.
               사람이 하듯 머리를 끌어 올린 뒤 누른다(dragify · 진짜 마우스) · 끌어 올렸는지는 결과에 남긴다"""
            ti = p.ev("__HM.topInfo()") or {}
            if (ti.get('rect') or {}).get('b', 0) > 900 - 4:
                hd = p.ev("k=>__HM.headFree(k)", ti['pk'])
                if hd and hd.get('on'):
                    R['lift%d' % n] = {'from': ti['rect'], 'how': p.drag(hd['cx'], hd['cy'], hd['cx'], 60)}
        if ok4:
            lift(5); at = p.ev("__HM.linkAtTop()"); snap('5 ' + ((at or {}).get('kind') or '?'), at, p.click(at, 1600))
            lift(6); at = p.ev("__HM.linkAtTop()"); snap('6 ' + ((at or {}).get('kind') or '?'), at, p.click(at, 1600))
        R['pops'] = p.ev("__HM.pops()")
        R['errs'] = p.ev("__HM.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


# ══════════ D — 표 자리마다(바탕 깊이로 연 팝업 안 대상을 눌러 한 겹 더) ══════════
PROBES = [('2084', {'d': 3, 'id': PREC}), ('2094', {'d': 2, 'jo': '제129조'}), ('6230', {'d': 3, 'to': REF41}), ('6240', {'d': 3, 'name': N101}),
          ('6306', {'d': 3, 'name': N96}), ('6358', {'d': 3, 'label': '판례', 'items': [PREC]}), ('6363', {'d': 3, 'label': '노트', 'items': [REF41]}),
          ('6365', {'d': 3, 'label': '기출', 'items': [CK_2562]}), ('6935', {'d': 3, 'kind': '기출'}), ('7001', {'d': 3})]
JO_CANDS = ['제129조', '제133조', '제132조', '제94조', '제128조', '제2조', '제29조', '제42조']


def scen_probe(br, eng, tag, src, G):
    if QJ.GATE:
        QJ.launch('new' if tag == 'NEW' else 'base')
    p = P(br, eng, tag, src, 1440, 900) if QJ.GATE else RIG.lease(br, eng, tag, src, 1440, 900, 'desk')
    R = {'eng': eng, 'tag': tag, 'site': {}}
    try:
        for site, a in PROBES:
            tries = JO_CANDS if site == '2094' else [None]
            for jo in tries:
                if jo:
                    a = dict(a, jo=jo)
                info = p.ev("([s,a])=>__HM.probe(s,a)", [site, a])
                if not (info.get('miss') and site == '2094'):
                    break
            V = {'info': info, 'args': a}
            if info.get('hit') and info['hit'].get('on'):
                V['tap'] = p.click(info['hit'], 400)
                V['after'] = p.ev("__HM.probeAfter()")
            R['site'][site] = V
            p.ev("__HM.clean()")
        R['errs'] = p.ev("__HM.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


# ══════════ E — 「모두 닫기」(책상 마우스 · 아이패드 터치) ══════════
def scen_all(br, eng, tag, src, W=1440, H=900, mode='desk'):
    if QJ.GATE:
        QJ.launch('new' if tag == 'NEW' else 'base')
    p = P(br, eng, tag, src, W, H, mode) if QJ.GATE else RIG.lease(br, eng, tag, src, W, H, mode)
    R = {'eng': eng, 'tag': tag, 'W': W, 'mode': mode}
    try:
        p.ev("([l,t])=>__HM.go(l,t)", ['특허법', 'cha2'])
        p.ev("()=>popJo('특허법','제129조',{clientX:300,clientY:180},1)"); p.pg.wait_for_timeout(700) if QJ.GATE else _wait(p.pg, 700, '조문 팝업 본문(원문 줄)이 팝업 뜬 뒤 비동기로 참 — 표지 없음')
        R['one'] = {'pall': p.ev("__HM.pallAll()"), 'top': p.ev("__HM.topInfo()")}
        R['two'] = p.ev("__HM.openTwo()")
        R['twoPall'] = p.ev("__HM.pallAll()")
        # 아래(조문) 팝업을 눌러 올린다 — 책상 = 몸통 빈 자리 마우스 / 터치 = 머리 잡기(chromium CDP 끌기 · webkit 톡)
        jk = 'jo|특허법|제129조'
        if p.touch and p.cdp:
            hd = p.ev("k=>__HM.popHead(k)", jk)
            R['raiseHow'] = p.drag(hd['cx'], hd['cy'], hd['cx'] + 6, hd['cy'] + 30) if hd and hd.get('on') else 'no head'
        elif p.touch:
            hd = p.ev("k=>__HM.popHead(k)", jk)
            R['raiseHow'] = 'webkit 톡(머리)'; p.click(hd, 600)
        else:
            at = p.ev("k=>__HM.popBodyAt(k)", jk); R['raiseAt'] = at
            R['raiseHow'] = 'mouse 몸통'; p.click(at, 600)
        R['raised'] = {'pall': p.ev("__HM.pallAll()"), 'top': p.ev("__HM.state()")['top']}
        # 머리 높이 — 같은 조문 팝업의 머리: 혼자일 때(단추 없음) = 맨 위로 올라 단추가 붙은 뒤
        R['phH'] = [g1 for g1 in [(R.get('one') or {}).get('top') and R['one']['top'].get('phH'), (p.ev("k=>__HM.popInfo(k)", jk) or {}).get('phH')]]
        at = p.ev("__HM.pallAt()"); R['pallHit'] = at
        R['pallTap'] = p.click(at, 700)
        R['afterAll'] = p.ev("__HM.state()")
        # Esc = 맨 위 하나(closePop 그대로)
        p.ev("__HM.openTwo()")
        p.pg.keyboard.press('Escape'); p.pg.wait_for_timeout(400) if QJ.GATE else _wait(p.pg, 400, 'Esc 뒤 맨 위 팝업 닫힘 · 「모두 닫기」 단추 옮김(popAllSync) 반영 — 표지 없음(닫힘 뒤 남은 팝업 수를 읽는 칸)')
        R['esc'] = p.ev("__HM.state()")
        R['escPall'] = p.ev("__HM.pallAll()")
        R['errs'] = p.ev("__HM.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


# ══════════ F — 마우스 길게 누르기(조문 줄 · 판례 요약 줄 · 2차 카드 줄 · 노트 팝업 줄) · 긁기 · 터치 ══════════
def scen_lp(br, eng, tag, src, W=1440, H=900, mode='desk'):
    if QJ.GATE:
        QJ.launch('new' if tag == 'NEW' else 'base')
    p = P(br, eng, tag, src, W, H, mode) if QJ.GATE else RIG.lease(br, eng, tag, src, W, H, mode)
    R = {'eng': eng, 'tag': tag, 'W': W, 'mode': mode, 'where': {}}
    try:
        def one(name, prep, where, touch=False):
            p.ev(prep); p.pg.wait_for_timeout(900) if QJ.GATE else _wait(p.pg, 900, '화면 · 팝업이 다 그려진 뒤 줄에 길게 누르기 핸들러(앱 pitWire · l._pit)가 붙음 — 표지 없음')
            p.ev("__HM.menuClear()")
            at = p.ev("w=>__HM.lineAt(w)", where)
            V = {'at': at}
            if at and at.get('on'):
                if touch:
                    V['how'] = p.longpress(at['cx'], at['cy'], touch=True)
                    V['menu'] = p.ev("__HM.menu()")
                    V['bar'] = p.ev("__HM.bar()")   # A-6(a) 9/30 — joscreen0929 A-5
                else:
                    V['how'] = 'mouse(trusted) 760ms'
                    V['menu'] = p.longpress(at['cx'], at['cy'])
                    V['bar'] = getattr(p, 'last_bar', None)   # A-6(a) 9/30 — 누르는 동안 읽은 칠 막대 둘째 줄
                V['menuAfterUp'] = p.ev("__HM.menu()")
            R['where'][name] = V
            p.ev("__HM.menuClear()")
        if mode == 'desk':
            one('jo', "(async()=>{await __HM.go('특허법','jo',{jo:'제129조',joMode:'본문'});})()", 'jo')
            one('prec', "(async()=>{await __HM.go('특허법','prec',{prec:'%s',precTab:'요약'});})()" % PREC, 'prec')
            one('card', "(async()=>{await __HM.go('특허법','cha2');await popCard4('기출','%s',null,1);})()" % CK_2562, 'card')
            one('note', "(async()=>{await __HM.go('특허법','cha2');await popNote('%s',null,null,1);})()" % N96, 'note')
            # 긁기 — 누른 채 80px 끌면 메뉴 없이 선택이 남는다
            p.ev("(async()=>{await __HM.go('특허법','jo',{jo:'제129조',joMode:'본문'});})()"); p.pg.wait_for_timeout(900) if QJ.GATE else _wait(p.pg, 900, '조문 화면 줄에 길게 누르기 핸들러(앱 pitWire · l._pit)가 붙음 — 표지 없음')
            at = p.ev("w=>__HM.lineAt(w)", 'jo')
            V = {'at': at}
            if at and at.get('on'):
                m = p.pg.mouse; m.move(at['cx'], at['cy']); m.down()
                for i in range(1, 11):
                    m.move(at['cx'] + 8 * i, at['cy']); p.pg.wait_for_timeout(20)
                p.pg.wait_for_timeout(700) if QJ.GATE else _wait(p.pg, 700, '끌어 긁는 동안 길게 누르기 임계(0.5초)가 지나도록 둠 — 시간 자체가 잣대(그 시간 동안 메뉴가 안 뜨는지 봄)')
                V['menuDuring'] = p.ev("__HM.menu()")
                m.up(); p.pg.wait_for_timeout(200) if QJ.GATE else _wait(p.pg, 200, 'mouseup 뒤 메뉴·선택 반영 — 표지 없음')
                V['menu'] = p.ev("__HM.menu()"); V['sel'] = p.ev("__HM.selLen()")
            R['where']['drag'] = V
        else:
            one('note_touch', "(async()=>{await __HM.go('특허법','cha2');await popNote('%s',null,null,1);})()" % N96, 'note', touch=True)
            one('jo_touch', "(async()=>{await __HM.go('특허법','jo',{jo:'제129조',joMode:'본문'});})()", 'jo', touch=True)
        R['errs'] = p.ev("__HM.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


# ══════════ G — 폰 · 아이패드(보이는 폭 · 팝업 화면 안 · 끌기 60px · 30/70 · 서랍 · 맨 윗줄) ══════════
def scen_phone(br, eng, tag, src, W, H, mode, shots=False):
    if QJ.GATE:
        QJ.launch('new' if tag == 'NEW' else 'base')
    p = P(br, eng, tag, src, W, H, mode) if QJ.GATE else RIG.lease(br, eng, tag, src, W, H, mode)
    R = {'eng': eng, 'tag': tag, 'W': W, 'H': H, 'mode': mode, 'tabs': {}}
    try:
        R['start'] = p.ev("__HM.state()")
        for law, sh in LAWS:
            for tab in TABS[sh]:
                p.ev("([l,t])=>__HM.go(l,t)", [law, tab]); p.pg.wait_for_timeout(300) if QJ.GATE else _wait(p.pg, 300, '탭 화면 가로 넘침(scrollWidth) 재기 전 레이아웃 안정 — 앱 표지 없음(글꼴 · 그림이 늦게 들어올 수 있다)')
                v = p.ev("__HM.vv()")
                if v['sw'] > v['cw']:
                    v['off'] = p.ev("__HM.offenders()")
                v['hrail'] = (p.ev("__HM.rail()") or {}).get('hrail')
                R['tabs'][sh + '|' + tab] = v
        # G-5 — 탭 줄을 끝까지 밀고 맨 오른쪽 「정리」를 그 자리에서 톡 → 다시 그린 뒤에도 켠 탭이 보인다(옆으로 민 자리 지킴)
        p.ev("([l,t])=>__HM.go(l,t)", ['특허법', 'jo'])
        R['railEnd'] = p.ev("__HM.railScrollEnd()")
        at = p.ev("k=>__HM.railTabAt(k)", 'omr'); R['railAt'] = at
        R['railTap'] = p.click(at, 1500) if QJ.GATE else rhit(p, at, JS_OMR_DONE, None, '「정리」 탭 톡 = 정리 탭 그림 끝 · 머리 탭 수 다 참 · 민 자리 되돌림(앱 drawRail 2131)')
        R['railAfter'] = p.ev("__HM.railState()")
        # 목차노트 목록 → 노트(진짜 터치 톡)
        p.ev("([l,t])=>__HM.go(l,t)", ['특허법', 'cha2'])
        at = p.ev("__HM.mokAt()"); R['mokAt'] = at; R['mokTap'] = p.click(at, 1300) if QJ.GATE else rhit(p, at, JS_MOK_OPEN, None, '목차노트 탭 톡 = 목록 팝업 줄 참(앱 popMokNote 7125)')
        R['list'] = p.ev("__HM.mokList()")
        at = p.ev("n=>__HM.mokRowAt(n)", N96); R['rowTap'] = p.click(at, 1500) if QJ.GATE else rhit(p, at, JS_NOTE_OPEN, N96, '목록 줄 톡 = 노트 팝업 뜸 · 위 30 · 아래 70 자리(앱 popNote 6786 · mokPlace 7162)')
        p.ev("n=>__HM.noteWait(n)", N96)
        R['split'] = {'list': p.ev("__HM.mokList()"), 'note': p.ev("n=>__HM.noteInfo(n)", N96), 'vv': p.ev("__HM.vv()"), 'in': p.ev("__HM.popsInVV()")}
        if shots:
            R['shot_split'] = p.shot('%s_%s_%d_split' % (tag, eng, W))
        # 팝업 다섯 종이 화면 안
        R['kinds'] = p.ev("__HM.openKinds()")
        # 머리 끌기 — 노트 팝업 하나 · 왼쪽 끝까지 · 오른쪽 끝까지 · 아래 끝까지(60px 규칙)
        p.ev("__HM.clean()")
        p.ev("n=>popNote(n,null,{clientX:120,clientY:200},1)", N96); p.pg.wait_for_timeout(900) if QJ.GATE else _wait(p.pg, 900, '노트 팝업이 떠 자리 잡은 뒤(showPop · vvFit 다음 틱) 머리 끌기 — 앱 표지 있음(note| 키)이나 끌기 시작 자리를 popInfo 로 읽기 전 안정 여유')
        k = 'note|특허|' + N96 + '|'
        D = {'r0': (p.ev("k=>__HM.popInfo(k)", k) or {}).get('rect')}
        hd = p.ev("k=>__HM.headFree(k)", k); D['hL'] = hd
        if hd and hd.get('on'):
            D['howL'] = p.drag(hd['cx'], hd['cy'], hd['cx'] - W * 1.6, hd['cy'])
            D['rL'] = (p.ev("k=>__HM.popInfo(k)", k) or {}).get('rect')
            hd = p.ev("k=>__HM.headFree(k)", k); D['hR'] = hd
            if hd and hd.get('on'):
                D['howR'] = p.drag(hd['cx'], hd['cy'], hd['cx'] + W * 2.2, hd['cy'])
                D['rR'] = (p.ev("k=>__HM.popInfo(k)", k) or {}).get('rect')
                hd = p.ev("k=>__HM.headFree(k)", k); D['hD'] = hd
                if hd and hd.get('on'):
                    D['howD'] = p.drag(hd['cx'], hd['cy'], hd['cx'] - 40, hd['cy'] + H * 1.5)
                    D['rD'] = (p.ev("k=>__HM.popInfo(k)", k) or {}).get('rect')
        D['cfg'] = p.ev("__HM.getCfg('note')")
        R['drag'] = D
        # 서랍(판례 탭 · 옆 두 칸)
        p.ev("([l,t])=>__HM.go(l,t)", ['특허법', 'prec'])
        DR = {'d0': p.ev("__HM.drawer()"), 'v0': p.ev("__HM.vv()")}
        at = p.ev("i=>__HM.handleAt(i)", 0); DR['h0'] = at; DR['tap0'] = p.click(at, 900)
        DR['d1'] = p.ev("__HM.drawer()"); DR['v1'] = p.ev("__HM.vv()")
        at = p.ev("__HM.mainAt()"); DR['outAt'] = at; DR['tapOut'] = p.click(at, 900)
        DR['d2'] = p.ev("__HM.drawer()")
        at = p.ev("i=>__HM.handleAt(i)", 1); DR['h1'] = at; DR['tap1'] = p.click(at, 900)
        DR['d3'] = p.ev("__HM.drawer()"); DR['v3'] = p.ev("__HM.vv()")
        if shots:
            DR['shot'] = p.shot('%s_%s_%d_drawer' % (tag, eng, W))
        at = p.ev("__HM.mainAt()"); DR['tapOut2'] = p.click(at, 900)
        DR['d4'] = p.ev("__HM.drawer()")
        R['drawer'] = DR
        R['ui'] = p.ev("__HM.uiRaw()")
        R['errs'] = p.ev("__HM.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


# ══════════ PC 무변 — 1890×907 · 팝업 하나의 자리·크기·DOM ══════════
def scen_pc(br, eng, tag, src):
    if QJ.GATE:
        QJ.launch('new' if tag == 'NEW' else 'base')
    p = P(br, eng, tag, src, 1890, 907) if QJ.GATE else RIG.lease(br, eng, tag, src, 1890, 907, 'desk')
    R = {'eng': eng, 'tag': tag, 'one': {}, 'lay': {}}
    try:
        p.ev("([l,t])=>__HM.go(l,t)", ['특허법', 'jo'])
        for nm in ('jo', 'note', 'prec', 'card'):
            R['one'][nm] = p.ev("n=>__HM.pcOne(n)", nm)
        for tab in ('jo', 'prec', 'cha2'):
            p.ev("([l,t])=>__HM.go(l,t)", ['특허법', tab])
            R['lay'][tab] = p.ev("__HM.layout()")
        R['vv'] = p.ev("__HM.vv()")
        R['errs'] = p.ev("__HM.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


def main():
    os.makedirs(WORK, exist_ok=True)
    if QJ.GATE:
        QJ.sub('git:show-app')
        base_b = git('show', BASE_REV + ':' + REL)
    else:
        base_b = b''   # regress — 바탕을 풀지 않는다(git:show-app 0)
    new_raw = open(NEWF, 'rb').read()
    base, new = base_b.decode('utf-8'), new_raw.decode('utf-8')
    RES = {'src': {'base': [len(base_b), hashlib.md5(base_b).hexdigest()],
                   'new': [len(new_raw), hashlib.md5(new_raw.replace(b'\r\n', b'\n')).hexdigest(), new_raw.count(b'\r\n'), NEWF]}}
    G = ground()
    RES['G'] = G
    t00 = time.time()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        brs = {e: getattr(pw, e).launch() for e in ENGS}
        try:
            for eng in ENGS:
                for tag in TAGS:
                    src = base if tag == 'BASE' else new

                    def run(name, key, fn, *a, **k):
                        if ONLY and ONLY != name:
                            return
                        if QJ.SMOKE and (name not in SMOKE_SCEN or eng != 'chromium'):   # smoke — rail · Chromium 만(규칙 57 · rail 에 터치 칸 없음)
                            return
                        t0 = time.time(); print('… %s %s' % (key, time.strftime('%H:%M:%S')), flush=True)
                        if QJ.REGRESS:
                            with QJ.stage(key):
                                RES[key] = r = fn(*a, **k)
                        else:
                            RES[key] = r = fn(*a, **k)
                        print('   %.1fs %s' % (time.time() - t0, (r or {}).get('exc', '')), flush=True)
                    run('rail', 'rail/%s/%s' % (eng, tag), scen_rail, brs[eng], eng, tag, src, G)
                    run('bc', 'bc/%s/%s' % (eng, tag), scen_bc, brs[eng], eng, tag, src, G)
                    run('depth', 'depth/%s/%s' % (eng, tag), scen_depth, brs[eng], eng, tag, src, G)
                    run('probe', 'probe/%s/%s' % (eng, tag), scen_probe, brs[eng], eng, tag, src, G)
                    run('all', 'all/%s/%s/desk' % (eng, tag), scen_all, brs[eng], eng, tag, src)
                    run('all', 'all/%s/%s/pad' % (eng, tag), scen_all, brs[eng], eng, tag, src, 1024, 768, 'pad')
                    run('lp', 'lp/%s/%s/desk' % (eng, tag), scen_lp, brs[eng], eng, tag, src)
                    run('lp', 'lp/%s/%s/pad' % (eng, tag), scen_lp, brs[eng], eng, tag, src, 1024, 768, 'pad')
                    for W, H, mode in ((390, 844, 'phone'), (768, 1024, 'pad'), (1024, 768, 'pad')):
                        run('phone', 'phone/%s/%s/%d' % (eng, tag, W), scen_phone, brs[eng], eng, tag, src, W, H, mode, shots=(W == 390 and QJ.GATE))   # regress — 캡처 안 찍음(사용자용)
                    run('pc', 'pc/%s/%s' % (eng, tag), scen_pc, brs[eng], eng, tag, src)
                    if tag == 'NEW' and QJ.GATE:   # A-6(a) 9/30 — PC 무변 바탕을 팝업마다(PC_BASE) · regress 는 바탕을 안 띄운다(기준 스냅샷)
                        for _nm, _rv in PC_BASE.items():
                            QJ.sub('git:show-app')
                            run('pc', 'pc/%s/B_%s' % (eng, _nm), scen_pc, brs[eng], eng, 'B_' + _nm, git('show', _rv + ':' + REL).decode('utf-8'))
        finally:
            if QJ.REGRESS:
                RIG.shut()
            for b in brs.values():
                b.close()
            for srv, _ in SERVERS.values():
                srv.shutdown()
    RES['sec'] = round(time.time() - t00, 1)
    raw = os.path.join(WORK, 'raw.json' if QJ.GATE else 'raw_regress.json')   # regress 는 따로(gate 의 raw.json · --report 를 안 덮는다)
    if QJ.GATE and os.path.exists(raw) and (ONLY or len(ENGS) < 2 or len(TAGS) < 2):
        old = json.load(io.open(raw, encoding='utf-8'))
        old.update(RES); RES = old
    json.dump(RES, io.open(raw, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    report(RES, G)


def NOISE(x):
    return 'ResizeObserver loop' in x or 'Failed to load resource' in x or 'net::ERR' in x or 'harness' in x or 'sw blocked' in x


def report(RES, G):
    L = []
    CNT = {'PASS': 0, 'FAIL': 0}
    NULL = {}

    def T(n, c, i=None, tag='NEW', eng=''):
        """NEW 줄만 합계에 센다 · BASE 줄은 헛잣대 표(NULL)로만"""
        key = n
        if tag == 'BASE':
            NULL.setdefault(key, []).append(bool(c)); return
        CNT['PASS' if c else 'FAIL'] += 1
        L.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c or i is None else ' | ' + json.dumps(i, ensure_ascii=False, default=str)[:900]))
    if QJ.REGRESS:
        def Tr(n, c, i=None, tag='NEW', eng='', note=''):
            """regress — T 와 같되 값 끝 말(note = 기준 스냅샷 출처)을 붙인다 · 기준 칸만 쓴다"""
            CNT['PASS' if c else 'FAIL'] += 1
            body = '' if c or i is None else json.dumps(i, ensure_ascii=False, default=str)[:900]
            if note:
                body = (body + ' ' + note).strip()
            L.append(('PASS' if c else 'FAIL') + ' | ' + n + (' | ' + body if body else ''))

    def I(n, v):
        L.append('INFO | ' + n + ' | ' + (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)[:1800]))
    g = lambda d, *ks: __import__('functools').reduce(lambda a, k: (a[k] if isinstance(a, list) and isinstance(k, int) and -len(a) <= k < len(a)
                                                                    else (a or {}).get(k) if isinstance(a, dict) else None), ks, d)
    near = lambda a, b, t=1.0: a is not None and b is not None and abs(a - b) <= t
    sb, sn = RES['src']['base'], RES['src']['new']
    if QJ.GATE:
        I('바탕 BASE = %s:%s' % (BASE_REV, REL), '%d B · md5 %s' % tuple(sb))
    else:
        I('바탕 BASE', '(regress — 바탕 안 띄움 · 바탕 md5 칸은 gate 에서만)')
    CNT_T = lambda n, c, i=None: T(n, c, i)
    if QJ.GATE:
        CNT_T('바탕 md5 = 지시서(1,017,845 B · c541b240…)', sb[1] == BASE_MD5_LF and sb[0] == BASE_SIZE, sb)
    I('새 판 NEW', '%d B · md5(LF) %s · CRLF %d · %s' % tuple(sn))
    I('시간(초)', RES.get('sec'))
    GT = RES.get('G') or G
    I('잣대 — 목차노트 수 NF()', GT['nf'])
    if QJ.want('잣대'):   # smoke 는 앱 칸만(데이터 잣대는 gate · regress 에서)
        CNT_T('잣대 = 목차노트 수(특허 70 · 상표 99 · 민소 81 · 디보 49 — 9/24 민소 번호 없는 셋 볼트 밖)', GT['nf'] == {'특허': 70, '상표': 99, '민소': 81, '디보': 49}, GT['nf'])   # A-6(d) 9/30 — 옛: 지시서 민소 84 · 9/24 13:1x 사용자 결정 → ⚙ aa8ceae 84→81
    I('잣대 — 데이터 속 <사건번호> 링크(k:P) 수 · 0 이면 2084 자리는 지은 줄로 잰다', GT.get('plinkData'))
    I('잣대 — 10.1 노트 ⤷ 임베드 수 · 9.6 노트 블록 칩 수', [GT.get('emb101'), GT.get('bl96')])
    for eng in ENGS:
        E = '[%s] ' % eng
        for tag in TAGS:
            Tt = lambda n, c, i=None: T(E + n, c, i, tag)
            if QJ.REGRESS:
                Ttr = lambda n, c, i=None, note='': Tr(E + n, c, i, tag, note=note)
            # ── A ──
            A = RES.get('rail/%s/%s' % (eng, tag))
            if A:
                if A.get('exc'):
                    Tt('A 시나리오 예외 없음', False, A['exc'])
                if tag == 'NEW':
                    I(E + 'A 함수 있음(NEW)', A.get('has'))
                for law, sh in LAWS:
                    for tab in TABS[sh]:
                        if QJ.SMOKE and (sh, tab) not in SMOKE_TABS:
                            continue
                        V = g(A, 'v', sh + '|' + tab) or {}
                        rl = V.get('rail') or {}
                        ks = [t['k'] or t['id'] for t in (rl.get('tabs') or [])]
                        mok = [t for t in (rl.get('tabs') or []) if t['id'] == 'mokBtn']
                        mk = mok[0] if mok else {}
                        Tt('A-1 %s·%s 탭 차례 = %s' % (sh, tab, '·'.join(ORDER[sh])), ks == ORDER[sh], ks)
                        Tt('A-1 %s·%s 목차노트 탭 = button.rb#mokBtn · 수 %d · 켜짐 · .on 없음' % (sh, tab, GT['nf'][sh]),
                           bool(mk) and mk.get('tag') == 'button' and 'rb' in (mk.get('cls') or '').split() and mk.get('n') == str(GT['nf'][sh]) and not mk.get('dis') and not mk.get('on') and mk.get('k') == 'mok', mk or rl.get('mokCls'))
                        Tt('A-1 %s·%s #mokBtn 전체 1개 · 탭 줄 안 · 보드 머리(#slot) 0' % (sh, tab), rl.get('mokAll') == 1 and rl.get('mokInRail') and not rl.get('mokInSlot'), {k: rl.get(k) for k in ('mokAll', 'mokInRail', 'mokInSlot')})
                        st0, st1, lst = V.get('st0') or {}, V.get('st1') or {}, V.get('list') or {}
                        Tt('A-1 %s·%s 누르면 목록 팝업만(S.tab 무변 · .on 없음)' % (sh, tab), bool(V.get('tap')) and bool(lst) and st1.get('tab') == tab == st0.get('tab') and st1.get('pops') == 1
                           and not any(t.get('on') for t in (g(V, 'rail1', 'tabs') or []) if t['id'] == 'mokBtn'), {'tap': V.get('tap'), 'st1': st1, 'list': bool(lst)})
                        mr, lr = V.get('mr') or {}, (lst or {}).get('rect') or {}
                        Tt('A-1 %s·%s 목록 첫 자리 = 탭 바로 아래(위 = 탭 아래 + 8 · 왼쪽 = 탭 왼쪽)' % (sh, tab), bool(lr) and near(lr.get('y'), mr.get('b', -99) + 8, 1.5) and near(lr.get('x'), max(8, min(mr.get('x', -99), 1440 - 470 - 8)), 1.5), {'mok': mr, 'list': lr})
                        Tt('A-1 %s·%s 다시 누르면 닫힘' % (sh, tab), bool(V.get('tap2')) and V.get('list2') is None and (V.get('st2') or {}).get('pops') == 0, {'tap2': V.get('tap2'), 'st2': V.get('st2')})
                if tag == 'NEW':
                    errs = [x for x in (A.get('errs') or []) if not NOISE(x)]
                    Tt('A 콘솔 오류 0', not errs, errs[:6])
            # ── B·C ──
            B = RES.get('bc/%s/%s' % (eng, tag))
            if B:
                if B.get('exc'):
                    Tt('B·C 시나리오 예외 없음', False, B['exc'])
                for law, sh in LAWS:
                    Lw = g(B, 'law', sh) or {}
                    lst, nt = Lw.get('list') or {}, Lw.get('note') or {}
                    Tt('B %s 목록 팝업 안내 글 0(「볼트 목차 차례 · 누르면 노트 팝업」)' % sh, bool(lst) and not any('볼트 목차 차례' in x for x in (lst.get('cdim') or [])) and lst.get('n') == GT['nf'][sh], {'cdim': lst.get('cdim'), 'n': lst.get('n')})
                    Tt('C %s 노트 팝업 머리 아래 줄(.memobtn) 0 · 「이 노트가 인용」 0' % sh, bool(nt) and nt.get('memobtn') == 0 and not any('이 노트가 인용' in x for x in (nt.get('memoTxt') or [])), {'memobtn': nt.get('memobtn'), 'memoTxt': nt.get('memoTxt')})
                    Tt('C %s 깊이 딱지(「N단」) 0 — 노트 팝업(깊이 2)' % sh, bool(nt) and not nt.get('badges'), nt.get('badges'))
                    if tag == 'NEW':
                        if QJ.REGRESS:   # regress — 기준 스냅샷(앞 인도판의 같은 칸 값 · 없으면 지금 값 자신 = 첫 기록)
                            bcid = 'C-chips@%s/%s' % (eng, sh)
                            bb = QJ.base(bcid, {'chips': nt.get('chips'), 'rows': nt.get('rows')})
                            Ttr('C %s 줄 칩 수 = 바탕(%s)' % (sh, bb.get('chips')), bool(nt) and nt.get('chips') == bb.get('chips') and nt.get('rows') == bb.get('rows'), {'new': [nt.get('chips'), nt.get('rows')], 'base': [bb.get('chips'), bb.get('rows')]}, note=QJ.base_note(bcid))
                        else:
                            bb = g(RES, 'bc/%s/BASE' % eng, 'law', sh, 'note') or {}
                            Tt('C %s 줄 칩 수 = 바탕(%s)' % (sh, bb.get('chips')), bool(nt) and nt.get('chips') == bb.get('chips') and nt.get('rows') == bb.get('rows'), {'new': [nt.get('chips'), nt.get('rows')], 'base': [bb.get('chips'), bb.get('rows')]})
            # ── D 사슬 ──
            Dd = RES.get('depth/%s/%s' % (eng, tag))
            if Dd:
                if Dd.get('exc'):
                    Tt('D 사슬 예외 없음', False, Dd['exc'])
                steps = Dd.get('steps') or []
                I(E + tag + ' D 사슬', [(s['step'], s['tap'], (s.get('st') or {}).get('pops'), (s.get('st') or {}).get('tab'), (s.get('spy') or {}).get('closeAll')) for s in steps])
                if Dd.get('lift5') or Dd.get('lift6'):
                    I(E + tag + ' D 사슬 — 화면 아래에 뜬 팝업을 머리 끌어 올린 뒤 누름(PC showPop 바탕 규칙 그대로)', {k: Dd.get(k) for k in ('lift5', 'lift6') if Dd.get(k)})
                for n in range(1, 7):
                    s = [x for x in steps if x['step'].startswith(str(n) + ' ')]
                    s = s[-1] if s else None
                    Tt('D 깊이 %d 까지 눌러 쌓임(팝업 %d개 · 탭 2차 그대로 · closeAllPops 0)' % (n, n), bool(s) and s.get('tap') and (s.get('st') or {}).get('pops') == n and (s.get('st') or {}).get('tab') == 'cha2' and (s.get('spy') or {}).get('closeAll') == 0,
                       s and {'step': s['step'], 'st': s.get('st'), 'spy': s.get('spy'), 'at': s.get('at')})
                last = steps[-1] if steps else {}
                Tt('D 사슬 어디에도 「깊이 3 —」 알림 0 · 「N단」 딱지 0', bool(steps) and not any('깊이 3' in t for s in steps for t in ((s.get('spy') or {}).get('toasts') or [])) and not any(s.get('badges') for s in steps),
                   [(s['step'], (s.get('spy') or {}).get('toasts'), s.get('badges')) for s in steps])
            # ── D 표 자리 ──
            Pp = RES.get('probe/%s/%s' % (eng, tag))
            if Pp:
                if Pp.get('exc'):
                    Tt('D 표 자리 예외 없음', False, Pp['exc'])
                for site, a in PROBES:
                    V = g(Pp, 'site', site) or {}
                    inf, af = V.get('info') or {}, V.get('after') or {}
                    ok = bool(V.get('tap')) and af.get('pops') == inf.get('before', -9) + 1 and af.get('closeAll') == 0 and af.get('tab') == inf.get('tab0') and not any('깊이 3' in t for t in (af.get('toasts') or [])) and not af.get('badges')
                    Tt('D 자리 %s(바탕 깊이 %d) 눌러 → 새 팝업 한 겹 더 · closeAllPops 0 · 탭 무변 · 「깊이 3 —」 0' % (site, a['d']), ok,
                       {'info': {k: inf.get(k) for k in ('host', 'target', 'before', 'tab0', 'miss', 'exc', 'note')}, 'after': af})
            # ── E ──
            for mode in ('desk', 'pad'):
                Ee = RES.get('all/%s/%s/%s' % (eng, tag, mode))
                if not Ee:
                    continue
                M = '%s ' % mode
                if Ee.get('exc'):
                    Tt('E %s예외 없음' % M, False, Ee['exc'])
                one = g(Ee, 'one', 'pall') or []
                Tt('E %s팝업 1개 = 「모두 닫기」 0' % M, g(Ee, 'one', 'top') is not None and len(one) == 0, one)
                two = Ee.get('twoPall') or []
                tops = sorted(Ee.get('two') or [], key=lambda x: -(x.get('z') or 0))
                Tt('E %s팝업 2개 = 맨 위(z 최대)에만 1 · ✕ 바로 왼쪽 · 글자 「모두 닫기」' % M, len(two) == 1 and bool(tops) and two[0]['pk'] == tops[0]['pk'] and two[0]['txt'] == '모두 닫기'
                   and tops[0].get('pallR') and tops[0].get('xR') and near(tops[0]['pallR']['r'] + 6 + 7, tops[0]['xR']['x'], 2.5), {'pall': two, 'top': tops[0] if tops else None})
                rz = Ee.get('raised') or {}
                Tt('E %s아래 팝업을 %s 올리면 단추가 옮김' % (M, '누름(몸통)' if mode == 'desk' else '머리 잡아'), len(rz.get('pall') or []) == 1 and (rz.get('pall') or [{}])[0].get('pk') == 'jo|특허법|제129조' == rz.get('top'), {'how': Ee.get('raiseHow'), 'raised': rz})
                ph = Ee.get('phH') or [None, None]
                Tt('E %s머리 높이 무변 — 조문 팝업 머리: 혼자(단추 없음) = 맨 위로 올라 「모두 닫기」가 붙은 뒤' % M, ph[0] is not None and near(ph[0], ph[1], 0.3), ph)
                Tt('E %s「모두 닫기」 누르면 POPS 0' % M, bool(Ee.get('pallTap')) and (Ee.get('afterAll') or {}).get('pops') == 0, {'hit': Ee.get('pallHit'), 'after': Ee.get('afterAll')})
                Tt('E %sEsc = 맨 위 하나만 닫기(그대로) → 남은 1개엔 단추 0' % M, (Ee.get('esc') or {}).get('pops') == 1 and len(Ee.get('escPall') or []) == 0, {'esc': Ee.get('esc'), 'pall': Ee.get('escPall')})
            # ── F ──
            Fd = RES.get('lp/%s/%s/desk' % (eng, tag))
            if Fd:
                if Fd.get('exc'):
                    Tt('F 예외 없음', False, Fd['exc'])
                for wh, lab in (('jo', '조문 줄'), ('prec', '판례 요약 줄'), ('card', '2차 카드 줄'), ('note', '노트 팝업 줄')):
                    V = g(Fd, 'where', wh) or {}
                    if wh == 'jo':   # A-6(a) 9/30 — joscreen0929 A-5: 조문 줄 = 칠 막대 하나(둘째 줄) · .pitmenu 0 · 판례·2차 카드·노트 줄은 .pitmenu 그대로(A-5-6)
                        Tt('F 마우스 0.5초 누름 → 칠 막대 둘째 줄(🗒 메모 · ✎ 수정 · 🏷 태그) · .pitmenu 0 — %s' % lab, not V.get('menu') and V.get('bar') == ['🗒 메모', '✎ 수정', '🏷 태그'], {'at': V.get('at'), 'menu': V.get('menu'), 'bar': V.get('bar')})
                        continue
                    Tt('F 마우스 0.5초 누름 → 메뉴(🗒 메모 붙이기 / ✎ 수정) — %s' % lab, bool(V.get('menu')) and any('메모 붙이기' in x for x in V['menu']) and any('수정' in x for x in V['menu']), {'at': V.get('at'), 'menu': V.get('menu')})
                V = g(Fd, 'where', 'drag') or {}
                Tt('F 마우스로 끌어 긁으면 메뉴 없음 · 선택 남음', bool(V.get('at')) and not V.get('menuDuring') and not V.get('menu') and (V.get('sel') or 0) > 0, V)
            Fp = RES.get('lp/%s/%s/pad' % (eng, tag))
            if Fp and eng == 'chromium':
                for wh in ('note_touch', 'jo_touch'):
                    V = g(Fp, 'where', wh) or {}
                    if wh == 'jo_touch':   # A-6(a) 9/30 — joscreen0929 A-5(관문 B-5 5a 와 같은 기대)
                        Tt('F 터치 길게 누름(CDP) → 칠 막대 둘째 줄(🗒 메모 · ✎ 수정 · 🏷 태그) · .pitmenu 0 — %s' % wh, not V.get('menu') and V.get('bar') == ['🗒 메모', '✎ 수정', '🏷 태그'], V)
                        continue
                    Tt('F 터치 길게 누름(CDP) → 메뉴 그대로 — %s' % wh, bool(V.get('menu')) and any('메모 붙이기' in x for x in V['menu']), V)
            # ── G ──
            for W, H in ((390, 844), (768, 1024), (1024, 768)):
                Gp = RES.get('phone/%s/%s/%d' % (eng, tag, W))
                if not Gp:
                    continue
                M = '%d×%d ' % (W, H)
                if Gp.get('exc'):
                    Tt('G %s예외 없음' % M, False, Gp['exc'])
                for law, sh in LAWS:
                    for tab in TABS[sh]:
                        v = g(Gp, 'tabs', sh + '|' + tab) or {}
                        Tt('G %s%s·%s scrollWidth = clientWidth(페이지가 옆으로 안 넘침)' % (M, sh, tab), v.get('sw') is not None and v.get('sw') == v.get('cw') and near(v.get('iw'), W, 0.5), {k: v.get(k) for k in ('sw', 'cw', 'iw', 'vv', 'off')})
                sp = Gp.get('split') or {}
                ins = sp.get('in') or []
                Tt('G %s목차노트 목록·노트 팝업이 보이는 화면(visualViewport) 안' % M, len(ins) >= 2 and all(x['inside'] for x in ins), ins)
                ks = Gp.get('kinds') or []
                bad = [(k['nm'], g(k, 'info', 'rect'), k.get('exc')) for k in ks if not k.get('info') or not (lambda r, v: r['x'] >= v['x'] - 0.5 and r['y'] >= v['y'] - 0.5 and r['r'] <= v['x'] + v['w'] + 0.5 and r['b'] <= v['y'] + v['h'] + 0.5)(k['info']['rect'], k['vv'])]
                if W <= 640:
                    Tt('G %s팝업 다섯 종(조문·노트·카드·판례·목록)이 보이는 화면 안' % M, len(ks) == 5 and not bad, bad or ks)
                elif tag == 'NEW':
                    if QJ.REGRESS:   # regress — 정보 줄(판정 없음) · 바탕 대신 기준 스냅샷
                        I(E + 'G %s(> 640 · G-6 그대로) 팝업 다섯 종 — 화면 밖으로 삐져나간 것(내용이 뒤에 와서 늘어난 팝업 · 바탕과 같은지 대조)' % M,
                          {'new': bad, 'base(기준 스냅샷)': QJ.base('G-out@%s/%d' % (eng, W), bad)})
                    else:
                        I(E + 'G %s(> 640 · G-6 그대로) 팝업 다섯 종 — 화면 밖으로 삐져나간 것(내용이 뒤에 와서 늘어난 팝업 · 바탕과 같은지 대조)' % M,
                          {'new': bad, 'base': [(k['nm'], g(k, 'info', 'rect')) for k in (g(RES, 'phone/%s/BASE/%d' % (eng, W), 'kinds') or []) if k.get('info') and not (lambda r, v: r['x'] >= v['x'] - 0.5 and r['y'] >= v['y'] - 0.5 and r['r'] <= v['x'] + v['w'] + 0.5 and r['b'] <= v['y'] + v['h'] + 0.5)(k['info']['rect'], k['vv'])]})
                D = Gp.get('drag') or {}
                rL, rR, rD = D.get('rL') or {}, D.get('rR') or {}, D.get('rD') or {}
                if W <= 640:
                    lst, nt = sp.get('list') or {}, sp.get('note') or {}
                    lr, nr = lst.get('rect') or {}, nt.get('rect') or {}
                    Hh = H - 16; lh = round((Hh - 8) * 0.3); nh = Hh - 8 - lh
                    Tt('G %s목록 = 위 30%%(y 8 · 높이 %d) · 노트 = 아래 70%%(y %d · 높이 %d) · 폭 = 화면 − 16 · 가운데' % (M, lh, 8 + lh + 8, nh),
                       near(lr.get('x'), 8) and near(lr.get('y'), 8) and near(lr.get('w'), W - 16) and near(lr.get('h'), lh, 1.5)
                       and near(nr.get('x'), 8) and near(nr.get('y'), 8 + lh + 8, 1.5) and near(nr.get('w'), W - 16) and near(nr.get('b'), H - 8, 1.5), {'list': lr, 'note': nr})
                    Tt('G %s팝업 다섯 종 폭 = 화면 − 16 · 왼쪽 8' % M, bool(ks) and all(k.get('info') and near(k['info']['rect']['w'], W - 16) and near(k['info']['rect']['x'], 8) for k in ks), [(k['nm'], g(k, 'info', 'rect', 'w'), g(k, 'info', 'rect', 'x')) for k in ks])
                    Tt('G %s머리 끌기 왼쪽 끝 = 머리 60px 남김(오른쪽 끝 x = 60)' % M, near(rL.get('r'), 60, 1.0), {'how': D.get('howL'), 'r0': D.get('r0'), 'rL': rL})
                    Tt('G %s머리 끌기 오른쪽 끝 = 왼쪽 x = 폭 − 60' % M, near(rR.get('x'), W - 60, 1.0), {'how': D.get('howR'), 'rR': rR})
                    Tt('G %s머리 끌기 아래 끝 = 위 y = 높이 − 34' % M, near(rD.get('y'), H - 34, 1.0), {'how': D.get('howD'), 'rD': rD})
                    DR = Gp.get('drawer') or {}
                    d0, d1, d2, d3, d4 = (DR.get(k) or {} for k in ('d0', 'd1', 'd2', 'd3', 'd4'))
                    Tt('G %s서랍 — 기억이 없으면 접힌 채로 시작(판례 탭 .tree·.plist 둘 다 hid)' % M, g(d0, 'tree', 'hid') is True and g(d0, 'plist', 'hid') is True and (Gp.get('start') or {}).get('treeHid') is True, {'d0': d0, 'start': Gp.get('start'), 'ui': Gp.get('ui')})
                    t1 = d1.get('tree') or {}
                    Tt('G %s서랍 — 손잡이 ‹ › 톡 → .tree 가 본문 위에 겹쳐 뜬다(absolute · 그림자 · 폭 ≤ 85%% · 본문 안 밀림 · 페이지 안 넓어짐)' % M,
                       bool(DR.get('tap0')) and t1.get('hid') is False and t1.get('pos') == 'absolute' and (t1.get('shadow') or 'none') != 'none' and t1.get('rect') and t1['rect']['w'] <= 0.85 * W + 0.5
                       and near(g(d1, 'main', 'x'), g(d0, 'main', 'x'), 0.5) and (DR.get('v1') or {}).get('sw') == (DR.get('v1') or {}).get('cw'), {'d1': d1, 'v1': DR.get('v1'), 'd0main': g(d0, 'main')})
                    Tt('G %s서랍 — 바깥(본문)을 누르면 닫힘' % M, bool(DR.get('tapOut')) and g(d2, 'tree', 'hid') is True, {'out': DR.get('outAt'), 'd2': d2})
                    p3 = d3.get('plist') or {}
                    Tt('G %s서랍 — 둘째 손잡이 → .plist 서랍(absolute · 폭 ≤ 85%%) · 바깥 누르면 닫힘' % M, bool(DR.get('tap1')) and p3.get('hid') is False and p3.get('pos') == 'absolute' and p3.get('rect') and p3['rect']['w'] <= 0.85 * W + 0.5
                       and g(d4, 'plist', 'hid') is True, {'d3': d3, 'd4': d4})
                    ra = Gp.get('railAfter') or {}
                    Tt('G %s맨 윗줄 탭 — 끝까지 밀고 「정리」 톡 → 탭이 바뀌고 다시 그린 뒤에도 켠 탭이 화면 안(민 자리 지킴)' % M,
                       bool(Gp.get('railTap')) and ra.get('tab') == 'omr' and (ra.get('sl') or 0) > 0 and bool((ra.get('on') or {}).get('on')), {'end': Gp.get('railEnd'), 'at': Gp.get('railAt'), 'after': ra})
                    hr = g(Gp, 'tabs', '특허|cha2', 'hrail') or {}
                    Tt('G %s맨 윗줄 탭 = 제 줄 안 가로 스크롤(overflow-x auto · 넘치는 탭은 그 안에서)' % M, hr.get('ox') == 'auto' and hr.get('sw', 0) >= hr.get('cw', 1), hr)
                else:
                    Tt('G %s(> 640) 끌기 한계 그대로 — 왼쪽 끝 x = 0 · 오른쪽 끝 x = 폭 − 60 · 아래 끝 y = 높이 − 34' % M, near(rL.get('x'), 0, 1.0) and near(rR.get('x'), W - 60, 1.0) and near(rD.get('y'), H - 34, 1.0), {'rL': rL, 'rR': rR, 'rD': rD})
                    if tag == 'NEW':
                        if QJ.REGRESS:   # regress — 기준 스냅샷(같은 모양 {drawer:{d0:{tree:{pos,hid}}}} 로 감싸 아래 식을 그대로 쓴다)
                            bcid = 'G-tree@%s/%d' % (eng, W)
                            b0 = {'drawer': {'d0': {'tree': QJ.base(bcid, {'pos': g(Gp, 'drawer', 'd0', 'tree', 'pos'), 'hid': g(Gp, 'drawer', 'd0', 'tree', 'hid')})}}}
                            Ttr('G %s(> 640) 옆 두 칸 = 바탕 그대로(서랍 아님 · 시작 상태 같음)' % M, g(Gp, 'drawer', 'd0', 'tree', 'pos') == g(b0, 'drawer', 'd0', 'tree', 'pos') and g(Gp, 'drawer', 'd0', 'tree', 'hid') == g(b0, 'drawer', 'd0', 'tree', 'hid'),
                                {'new': g(Gp, 'drawer', 'd0', 'tree'), 'base': g(b0, 'drawer', 'd0', 'tree')}, note=QJ.base_note(bcid))
                        else:
                            b0 = RES.get('phone/%s/BASE/%d' % (eng, W)) or {}
                            Tt('G %s(> 640) 옆 두 칸 = 바탕 그대로(서랍 아님 · 시작 상태 같음)' % M, g(Gp, 'drawer', 'd0', 'tree', 'pos') == g(b0, 'drawer', 'd0', 'tree', 'pos') and g(Gp, 'drawer', 'd0', 'tree', 'hid') == g(b0, 'drawer', 'd0', 'tree', 'hid'),
                               {'new': g(Gp, 'drawer', 'd0', 'tree'), 'base': g(b0, 'drawer', 'd0', 'tree')})
                if tag == 'NEW':
                    errs = [x for x in (Gp.get('errs') or []) if not NOISE(x)]
                    Tt('G %s콘솔 오류 0' % M, not errs, errs[:6])
            # ── PC 무변 ──
            if tag == 'NEW':
                Pn, Pb = RES.get('pc/%s/NEW' % eng), RES.get('pc/%s/BASE' % eng)
                if Pn and (Pb or QJ.REGRESS):
                    for nm in ('jo', 'note', 'prec', 'card'):
                        a, b = g(Pn, 'one', nm) or {}, g(Pb, 'one', nm) or {}
                        bn = g(RES.get('pc/%s/B_%s' % (eng, nm)), 'one', nm) or {}   # A-6(a) 9/30 — 바뀐 뒤 바탕(PC_BASE): jo = 자리·DOM · card = DOM 만 · note·prec 는 c9d5bc0 그대로 · ★ ⑧ A-8-1 · A-9-4(사용자 10/3 08:22·08:32·09:33) — card DOM 은 ⑧ 꾸밈(.c2miss · .c2lnkw)을 뺀 값으로 센다(_harness_jo_mok_popup_phone_tests.js pcOne · 옛 405 ↔ ⑧ 463 = 405 + 58)
                        bp, tp = (bn, '바뀐 뒤 바탕 ' + PC_BASE[nm]) if nm == 'jo' else (b, '바탕')
                        bd, td = (bn, '바뀐 뒤 바탕 ' + PC_BASE[nm]) if nm in PC_BASE else (b, '바탕')
                        if QJ.REGRESS:   # regress — 바탕 판(c9d5bc0 · 바뀐 뒤 바탕) 대신 앞 인도판의 같은 팝업 값(기준 스냅샷 · 없으면 지금 값 자신 = 첫 기록)
                            bcid = 'PC-%s@%s' % (nm, eng)
                            bp = bd = QJ.base(bcid, {k2: a.get(k2) for k2 in ('rect', 'style', 'cls', 'text', 'n')})
                            Ttr('PC 1890×907 %s 팝업 자리·크기·꼴 = %s' % (nm, tp), bool(a) and a.get('rect') == bp.get('rect') and a.get('style') == bp.get('style') and a.get('cls') == bp.get('cls'), {'new': [a.get('rect'), a.get('style')], 'base': [bp.get('rect'), bp.get('style')]}, note=QJ.base_note(bcid))
                            Ttr('PC 1890×907 %s 팝업 DOM 글자·요소 수 = %s(걷은 줄 제외)' % (nm, td), bool(a) and a.get('text') == bd.get('text') and a.get('n') == bd.get('n'), {'new': [a.get('n'), (a.get('text') or '')[:160]], 'base': [bd.get('n'), (bd.get('text') or '')[:160]]}, note=QJ.base_note(bcid))
                        else:
                            Tt('PC 1890×907 %s 팝업 자리·크기·꼴 = %s' % (nm, tp), bool(a) and a.get('rect') == bp.get('rect') and a.get('style') == bp.get('style') and a.get('cls') == bp.get('cls'), {'new': [a.get('rect'), a.get('style')], 'base': [bp.get('rect'), bp.get('style')]})
                            Tt('PC 1890×907 %s 팝업 DOM 글자·요소 수 = %s(걷은 줄 제외)' % (nm, td), bool(a) and a.get('text') == bd.get('text') and a.get('n') == bd.get('n'), {'new': [a.get('n'), (a.get('text') or '')[:160]], 'base': [bd.get('n'), (bd.get('text') or '')[:160]]})
                    for tab in ('jo', 'prec', 'cha2'):
                        a, b = g(Pn, 'lay', tab) or {}, g(Pb, 'lay', tab) or {}
                        if QJ.REGRESS:   # regress — 기준 스냅샷
                            bcid = 'PC-lay-%s@%s' % (tab, eng)
                            b = QJ.base(bcid, {k2: a.get(k2) for k2 in ('slot', 'tree', 'plist', 'laws', 'top')})
                            same = all(a.get(k) == b.get(k) for k in ('slot', 'tree', 'plist', 'laws', 'top'))
                            Ttr('PC 1890×907 %s 탭 본문 자리(slot·tree·plist·머리 줄) = 바탕' % tab, same, {k: [a.get(k), b.get(k)] for k in ('slot', 'tree', 'plist', 'laws', 'top') if a.get(k) != b.get(k)}, note=QJ.base_note(bcid))
                        else:
                            same = all(a.get(k) == b.get(k) for k in ('slot', 'tree', 'plist', 'laws', 'top'))
                            Tt('PC 1890×907 %s 탭 본문 자리(slot·tree·plist·머리 줄) = 바탕' % tab, same, {k: [a.get(k), b.get(k)] for k in ('slot', 'tree', 'plist', 'laws', 'top') if a.get(k) != b.get(k)})
                    I(E + 'PC 1890×907 탭 줄(#hrail · 목차노트 탭이 더해져 넓어짐 — 뜻한 차이)', {'new': g(Pn, 'lay', 'jo', 'hrail'), 'base': g(Pb, 'lay', 'jo', 'hrail')})
    # ── 헛잣대 표 ──
    tot = sum(len(v) for v in NULL.values()); fails = sum(1 for v in NULL.values() for x in v if not x)
    L.append('')
    if QJ.GATE:   # regress — 헛잣대(바탕에 같은 잣대 돌리기)는 gate 에서만
        L.append('── 헛잣대(규칙 ⑩) — 같은 잣대를 바탕 %s 에 돌린 결과: %d 중 FAIL %d · PASS %d ──' % (BASE_REV, tot, fails, tot - fails))
    grp = {}
    for n, v in NULL.items():
        key = re.sub(r'^\[[a-z]+\] ', '', n)
        key = re.sub(r' (특허|상표|민소|디보)·[a-z0-9]+ ', ' * ', key)
        key = re.sub(r' (특허|상표|민소|디보) ', ' * ', key)
        a = grp.setdefault(key, [0, 0]); a[0] += sum(1 for x in v if not x); a[1] += len(v)
    for k in sorted(grp):
        L.append('BASE | %s | FAIL %d / %d' % (k, grp[k][0], grp[k][1]))
    body = '\n'.join(L) + '\n\n합계  PASS %d · FAIL %d  (%s초)\n' % (CNT['PASS'], CNT['FAIL'], RES.get('sec'))
    print(body[-3000:])
    wr(os.path.join(OUT, '_harness_jo_mok_popup_phone_result.txt'), body)
    shots = [v for k, v in RES.items() if k.startswith('phone/') for v in [RES[k].get('shot_split'), (RES[k].get('drawer') or {}).get('shot')] if v]
    if shots:
        os.makedirs(SHOTS, exist_ok=True)
        for s in shots:
            if os.path.exists(s):
                wr(os.path.join(SHOTS, os.path.basename(s).replace('shot_', '')), open(s, 'rb').read())


if __name__ == '__main__':
    if '--report' in sys.argv:
        RES = json.load(io.open(os.path.join(WORK, 'raw.json'), encoding='utf-8'))
        report(RES, RES.get('G') or ground())
    else:
        main()
