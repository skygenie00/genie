# -*- coding: utf-8 -*-
"""조판기 팝업 머리 겹침 · 콜아웃 안내 글 · 민소 2차 기출 Claude · 통합 검색 「Claude」 범위 + ✎ 수정 큐 볼트 반영 — _task_jo_ms_claude_editq §F 관문 하네스.

  NEW  = genie 작업트리 jo/index.html(또는 --new <파일>) · 데이터 = genie jo/data(무접촉)
  BASE = `509c10b` 의 같은 파일(바탕 · 헛잣대 — 새 판이 뜻한 잣대는 BASE 에서 FAIL 이어야 잣대가 산다 · 규칙 ⑩)
  Claude 답 = **이 하네스 안에서만** 가짜 파일(MS901 · T901) — 저장소에 안 올린다(1차객 하네스 G-픽스처와 같은 길: SEED 가 GitHub 을 대답)
  엔진 = playwright chromium · webkit · 책상 1440×900(마우스) · 아이패드 1024×768(터치 톡 — webkit 진짜 터치 · chromium touchscreen)
  E = editq_apply.py 를 볼트 **사본**(TEMP)에서 시험(쓰기 직전 파일이 바뀐 경우 · 임시 파일 · CRLF·BOM · 꼬리 · 끝 줄바꿈)
      실제 반영 뒤 대조는 --only ereal --eres <결과.json> --eprev <mark 전 기록.json 사본> --edata <genie jo/data 바뀐 파일 목록 txt>
      (전체 판에 같은 인자를 주면 A~E 와 함께 돈다 · --only 판은 %TEMP%/h_jo_ms_claude/raw.json 에 합쳐진다 — 마지막에 전체 판으로 한 번 더)
  ⚠ 자과앱이 아니다(조판기) — 픽셀 게이트는 없다.

쓰기 : python _harness_jo_ms_claude.py [--new 파일] [--out 폴더] [--only a|b|c|pad|rx|d|e|ereal] [--eng chromium|webkit] [--tag BASE|NEW]
       python _harness_jo_ms_claude.py --report [--out 폴더]
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import hashlib, http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

GENIE = _roots.genie()
HERE = os.path.dirname(os.path.abspath(__file__))
JOPANGI = os.path.dirname(os.path.dirname(HERE))
ARG = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
OUT = ARG('--out', HERE)
ONLY = ARG('--only', '')
ENGS = [ARG('--eng')] if ARG('--eng') else ['chromium', 'webkit']
TAGS = [ARG('--tag')] if ARG('--tag') else ['BASE', 'NEW']
NEWF = ARG('--new', os.path.join(GENIE, 'jo', 'index.html'))
TOOL = ARG('--tool', os.path.join(JOPANGI, 'editq_apply.py'))
WORK = os.path.join(tempfile.gettempdir(), 'h_jo_ms_claude')
REL = 'jo/index.html'
JOD = os.path.join(GENIE, 'jo')
DATA = os.path.join(JOD, 'data')
BASE_REV = '509c10b'
BASE_MD5_LF = '3aefbb3f08f804a72b2dcc67a958f1bc'
BASE_SIZE = 1031441
TESTS = io.open(os.path.join(HERE, '_harness_jo_ms_claude_tests.js'), encoding='utf-8').read()
IPAD_UA = ('Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
N96 = '9.6.{결}정정심판(136)_특무내정정청구(133-2)'
PREC = '2021후10374'
MS_CODE, MS_NAME = '민기출 24-61-2', '관할{합}전부구별, 반소이송가부'
MS_MENT = '민기출 22-59-1'
MS_NOANS = '민기출 24-61-1'
FIXTURE = {
    'v': 1, 'updatedAt': '2026-09-24', 'note': '하네스 픽스처 — 저장소에 안 올린다',
    'answers': {
        'MS901': {'law': '민소', 'uid': MS_CODE, 'd': '2026-09-24', 'unit': '1.3.1 {법정}직사토', 'title': '하네스 합의관할',
                  'core': '하네스핵심줄 — 전속적 합의인지 부가적 합의인지가 쟁점',
                  'md': ('**Q.** 하네스질문합의관할 — 합의서에 전속·부가를 적지 않았으면?\n\n| 구분 | 효과 |\n|---|---|\n| 전속적 | 그 법원만 |\n| 부가적 | 법정관할에 더해 |\n\n'
                         '- 관련 문제 → ' + MS_MENT + '\n- 답 번호 MS901 · MS001 · T001 은 열쇠가 아니다')},
        'T901': {'law': '특허', 'uid': 'T0138603', 'd': '2026-09-22', 'unit': '특허 8.7.4', 'title': '특허 하네스', 'core': '특허하네스핵심',
                 'md': '**Q.** 특허하네스낱말 질문\n\n- 수입도 실시다 → T0138512'}}}
SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.alert=function(){};window.confirm=function(){return true;};window.prompt=function(){return null;};
(function(){var Q=new URLSearchParams(location.search);window.__CLMODE=Q.get('cl')||'file';
var nf=window.fetch.bind(window);
window.fetch=function(u,o){o=o||{};var s=String((u&&u.url)||u);
 if(/\/contents\/jopangi\/claude\.json/.test(s)){
  if(window.__CLMODE==='hang')return new Promise(function(){});
  if(window.__CLMODE==='500')return Promise.resolve(new Response('{"message":"harness 500"}',{status:500}));
  if(window.__CLMODE==='404')return Promise.resolve(new Response('{"message":"Not Found"}',{status:404}));
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
try{localStorage.setItem('tt.cfg',JSON.stringify({token:'harness-token',person:'하네스'}));}catch(e){}
if(Q.get('skon')==='old'){try{localStorage.setItem('jopangi_skon',JSON.stringify({jo:true,logic:true}));}catch(e){}}
})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
</script>"""
READY = "!!window.__HC&&typeof render==='function'&&typeof popShell==='function'&&!!document.querySelector('#slot')"


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
    io.open(os.path.join(out, 'claude_fixture.json'), 'w', encoding='utf-8', newline='\n').write(json.dumps(FIXTURE, ensure_ascii=False))

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=out, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            if p.startswith('/data/'):
                return os.path.join(DATA, p[6:].replace('/', os.sep))
            if p in ('/index.html', '/', '/claude_fixture.json'):
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
    def __init__(self, br, eng, tag, src, W=1440, H=900, pad=False, q='cl=file'):
        self.eng, self.tag, self.pad = eng, tag, pad
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
        self.pg.goto('http://127.0.0.1:%d/index.html?%s' % (self.port, q), wait_until='load', timeout=120000)
        self.pg.wait_for_function(READY, timeout=120000)
        self.pg.wait_for_timeout(1500)

    def ev(self, expr, arg=None):
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

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


def scen_a(br, eng, tag, src):
    p = P(br, eng, tag, src)
    R = {'eng': eng, 'tag': tag, 'pops': {}}
    try:
        p.ev("__HC.clReady()")
        for kind, a in (('callout', {'code': MS_CODE, 'ct': '문제-2'}), ('jimun', {'uid': 'T0138603'}), ('note', {'name': N96}),
                        ('prec', {'id': PREC}), ('claude', {'uid': 'T0138603'})):
            o = p.ev("([k,a])=>__HC.openA(k,a)", [kind, a])
            V = {'open': o}
            if o and o.get('pk'):
                V['chk'] = p.ev("([k,h,s])=>__HC.headCheck(k,h,s)", [o['pk'], 140, 70])
            R['pops'][kind] = V
        R['errs'] = p.ev("__HC.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


def scen_b(br, eng, tag, src):
    p = P(br, eng, tag, src)
    R = {'eng': eng, 'tag': tag}
    try:
        pick = p.ev("__HC.pickCallout()"); R['pick'] = pick
        o = p.ev("([k,a])=>__HC.openA(k,a)", ['callout', pick or {'code': MS_CODE, 'ct': '문제-2'}])
        R['open'] = o
        pk = (o or {}).get('pk')
        R['info'] = p.ev("k=>__HC.calloutInfo(k)", pk)
        R['htog'] = p.ev("k=>__HC.htogClick(k)", pk)
        at = p.ev("k=>__HC.lineAt(k)", pk); R['at'] = at
        if at and at.get('on'):
            m = p.pg.mouse; m.move(at['cx'], at['cy']); m.down(); p.pg.wait_for_timeout(760)
            R['menu'] = p.ev("__HC.menu()"); m.up(); p.pg.wait_for_timeout(200)
        R['errs'] = p.ev("__HC.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


def scen_c(br, eng, tag, src, pad=False):
    p = P(br, eng, tag, src, 1024 if pad else 1440, 768 if pad else 900, pad=pad)
    R = {'eng': eng, 'tag': tag, 'pad': pad}
    try:
        R['has'] = p.ev("__HC.has()")
        R['cl'] = p.ev("__HC.clReady()")
        p.ev("([l,t])=>__HC.go(l,t)", ['민사소송법', 'cha2'])
        R['rows'] = p.ev("__HC.boardRows()")
        # 줄 단추 누름 = 창만
        at = p.ev("c=>__HC.rowBtnAt(c)", MS_CODE[4:]); R['rowBtnAt'] = at
        R['rowBtnTap'] = p.click(at, 900)
        R['afterRowBtn'] = {'pops': p.ev("__HC.pops()"), 'win': p.ev("u=>__HC.clWin(u)", MS_CODE)}
        p.ev("__HC.clean()")
        # 카드 팝업(줄 누름) → 탭 「Claude 1」 → 새 창 · 카드 탭 무변
        at = p.ev("c=>__HC.rowAt(c)", MS_CODE[4:]); R['rowTap'] = p.click(at, 1200)
        R['tabs'] = p.ev("c=>__HC.cardTabs(c)", MS_CODE)
        at = p.ev("c=>__HC.cardTabAt(c)", MS_CODE); R['tabAt'] = at
        R['tabTap'] = p.click(at, 900)
        R['afterTab'] = {'pops': p.ev("__HC.pops()"), 'tabs': p.ev("c=>__HC.cardTabs(c)", MS_CODE), 'win': p.ev("u=>__HC.clWin(u)", MS_CODE)}
        if not pad:
            # 답 없는 카드 탭 = 회색 → 누르면 「아직 답 없음」 창
            p.ev("__HC.clean()"); p.ev("c=>__HC.openCard(c)", MS_NOANS)
            R['tabsNo'] = p.ev("c=>__HC.cardTabs(c)", MS_NOANS)
            at = p.ev("c=>__HC.cardTabAt(c)", MS_NOANS); R['tabNoTap'] = p.click(at, 900)
            R['winNo'] = p.ev("u=>__HC.clWin(u)", MS_NOANS)
            # 창 제목 · 머리 코드 단추 → 그 카드 · 본문 코드 단추 → 그 카드 · ✎ 정정
            p.ev("__HC.clean()"); p.ev("u=>clOpen(u,{clientX:500,clientY:150})", MS_CODE); p.pg.wait_for_timeout(1200)
            R['win'] = p.ev("u=>__HC.clWin(u)", MS_CODE)
            at = p.ev("([u,s,w])=>__HC.clUidAt(u,s,w)", [MS_CODE, MS_CODE, 'head']); R['headUidTap'] = p.click(at, 1200)
            R['afterHead'] = p.ev("__HC.pops()")
            at = p.ev("([u,s,w])=>__HC.clUidAt(u,s,w)", [MS_CODE, MS_MENT, 'body']); R['bodyUidTap'] = p.click(at, 1200)
            R['afterBody'] = p.ev("__HC.pops()")
            R['fix'] = p.ev("([u,m,w])=>__HC.clFix(u,m,w)", [MS_CODE, 'MS901', '정정본전용낱말'])
            # 특상디 2차·민소 사례·GS 에 단추 0
            other = {}
            for law, kind in (('특허법', '기출'), ('상표법', '기출'), ('디자인보호법', '기출'), ('민사소송법', '사례'), ('민사소송법', 'GS')):
                p.ev("([l,t,o])=>__HC.go(l,t,o)", [law, 'cha2', {'boardKind': kind}])
                rows = p.ev("__HC.boardRows()") or []
                other[law + '|' + kind] = {'rows': len(rows), 'btn': sum(len(r['btn']) for r in rows)}
            R['other'] = other
            p.ev("([l,t])=>__HC.go(l,t)", ['특허법', 'cha2'])
            rows = p.ev("__HC.boardRows()") or []
            R['tkCard'] = None
            if rows:
                k = p.ev("()=>get('2cha_본문_기출_특허.json').then(C=>Object.keys(C)[0])")
                p.ev("k=>popCard4('기출',k,{clientX:300,clientY:120},1)", k); p.pg.wait_for_timeout(800)
                R['tkCard'] = p.ev("()=>{const p=POPS[POPS.length-1];return p?{pk:p._pk,cltab:p.querySelectorAll('.cltab').length,tabs:[...p.querySelectorAll('.gtabs > *')].map(b=>b.textContent)}:null;}")
        R['errs'] = p.ev("__HC.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


RX_IN = ['MS001', 'MS901', 'T001', MS_CODE, 'T0138603', 'T0946093P7', '민기출 24-61-23', '민기출 24-61-2-관할']


def scen_rx(br, eng, tag, src):
    p = P(br, eng, tag, src)
    R = {'eng': eng, 'tag': tag}
    try:
        R['rx'] = p.ev("l=>__HC.rx(l)", RX_IN)
        R['errs'] = p.ev("__HC.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    return R


LAWS4 = ['특허법', '상표법', '디자인보호법', '민사소송법']


def scen_d(br, eng, tag, src):
    R = {'eng': eng, 'tag': tag}
    p = P(br, eng, tag, src)
    try:
        R['cl'] = p.ev("__HC.clReady()")
        R['scopes'] = p.ev("__HC.scopes()")
        R['nonLogic'] = p.ev("()=>(document.getElementById('skscope').textContent.match(/논리/g)||[]).length")
        R['q1'] = p.ev("([q,s,l])=>__HC.search(q,s,l)", ['하네스질문합의관할', ['claude'], LAWS4])
        R['q1off'] = p.ev("([q,s,l])=>__HC.search(q,s,l)", ['하네스질문합의관할', ['claude'], ['특허법', '상표법', '디자인보호법']])
        R['qT_on'] = p.ev("([q,s,l])=>__HC.search(q,s,l)", ['특허하네스낱말', ['claude'], ['특허법']])
        R['qT_off'] = p.ev("([q,s,l])=>__HC.search(q,s,l)", ['특허하네스낱말', ['claude'], ['상표법', '디자인보호법', '민사소송법']])
        R['qName'] = p.ev("([q,s,l])=>__HC.search(q,s,l)", ['반소이송가부', ['claude'], LAWS4])
        R['q1b'] = p.ev("([q,s,l])=>__HC.search(q,s,l)", ['하네스질문합의관할', ['claude'], LAWS4])
        at = p.ev("i=>__HC.searchRowAt(i)", 0); R['rowTap'] = p.click(at, 1000)
        R['afterTap'] = {'state': p.ev("__HC.state()"), 'win': p.ev("u=>__HC.clWin(u)", MS_CODE)}
        p.ev("__HC.clean()")
        p.ev("u=>clOpen(u,{clientX:500,clientY:150})", MS_CODE); p.pg.wait_for_timeout(1000)
        R['fix'] = p.ev("([u,m,w])=>__HC.clFix(u,m,w)", [MS_CODE, 'MS901', '정정본전용낱말'])
        p.ev("__HC.clean()")
        R['qFix'] = p.ev("([q,s,l])=>__HC.search(q,s,l)", ['정정본전용낱말', ['claude'], LAWS4])
        R['errs'] = p.ev("__HC.errs()") + p.errs
    except Exception as e:
        R['exc'] = repr(e)[:600]
    finally:
        p.close()
    for mode in ('500', 'hang'):
        p = P(br, eng, tag, src, q='cl=' + mode)
        try:
            p.pg.wait_for_timeout(800)
            R['mode_' + mode] = {'cl': p.ev("()=>CL_STATE"), 'q': p.ev("([q,s,l])=>__HC.search(q,s,l)", ['하네스', ['claude'], LAWS4])}
        except Exception as e:
            R['mode_' + mode] = {'exc': repr(e)[:300]}
        finally:
            p.close()
    p = P(br, eng, tag, src, q='cl=file&skon=old')
    try:
        R['old'] = {'skon': p.ev("__HC.skonNow()"), 'ls': p.ev("()=>localStorage.getItem('jopangi_skon')"), 'errs': p.ev("__HC.errs()") + p.errs,
                    'q': p.ev("([q,s,l])=>__HC.search(q,s,l)", ['하네스질문합의관할', ['claude'], LAWS4])}
    except Exception as e:
        R['old'] = {'exc': repr(e)[:300]}
    finally:
        p.close()
    return R


# ══════════ E — editq_apply.py 를 볼트 사본에서 ══════════
def scen_e():
    import importlib.util
    R = {'tool': TOOL, 'cases': {}}
    spec = importlib.util.spec_from_file_location('editq_apply_h', TOOL)
    E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
    d = os.path.join(WORK, 'e_vault'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    BEF = '\tⅰ)(96①1)는 실시목적이 연구/시험일것을 정하고있을뿐,'
    AFT = '\tⅰ)1조의 특허법목적과, 94조의 특허권자보호규정 취지에 비추어볼때\n(96①1)는 실시목적이 연구/시험일것을 정하고있을뿐,\n'
    BODY = '# 제목\n\n★<-머리-\n' + BEF + '\n\tⅱ)다음 줄\n\t ^e5ac55\n\n끝\n'

    def mk(name, text, bom=False, crlf=False):
        t = text.replace('\n', '\r\n') if crlf else text
        b = (b'\xef\xbb\xbf' if bom else b'') + t.encode('utf-8')
        p = os.path.join(d, name); open(p, 'wb').write(b); return p, b

    def snap(p):
        return (E.md5(open(p, 'rb').read()), os.stat(p).st_mtime)

    def case(name, fn):
        try:
            R['cases'][name] = fn()
        except Exception as e:
            R['cases'][name] = {'exc': repr(e)[:300]}
    # E1 그대로 — 반영 · 바뀐 곳 밖 바이트 동일 · 백업 = 원본 · 끝 줄바꿈 1개 뺌
    def e1():
        p, b0 = mk('e1.md', BODY); s = snap(p)
        bef, aft, notes = E.norm(BEF, AFT)
        r = E.apply_one(p, bef, aft, s, backup=os.path.join(d, '_bk', 'e1.md'))
        b1 = open(p, 'rb').read(); i = b0.decode().index(BEF)
        return {'r': r, 'notes': notes, 'expect': b1 == (BODY[:i] + aft + BODY[i + len(BEF):]).encode(), 'blank': '\n\n\tⅱ' in b1.decode(),
                'backup': open(os.path.join(d, '_bk', 'e1.md'), 'rb').read() == b0}
    case('E1', e1)
    # E2 읽은 뒤 파일이 바뀜(다른 줄 덧붙임) · before 는 남음 → 다시 찾아 반영
    def e2():
        p, b0 = mk('e2.md', BODY); s = snap(p); time.sleep(0.05)
        open(p, 'ab').write('덧붙인 줄\n'.encode()); bef, aft, _ = E.norm(BEF, AFT)
        r = E.apply_one(p, bef, aft, s); return {'r': r, 'kept': open(p, 'rb').read().decode().endswith('덧붙인 줄\n')}
    case('E2', e2)
    # E3 읽은 뒤 before 가 사라짐 → 보류(까닭 = 그 사이 바뀜)
    def e3():
        p, b0 = mk('e3.md', BODY); s = snap(p); time.sleep(0.05)
        open(p, 'wb').write(BODY.replace(BEF, '\t다른 글').encode()); b1 = open(p, 'rb').read()
        bef, aft, _ = E.norm(BEF, AFT)
        r = E.apply_one(p, bef, aft, s); return {'r': r, 'same': open(p, 'rb').read() == b1}
    case('E3', e3)
    # E4 before 두 번 → 보류
    def e4():
        p, b0 = mk('e4.md', BODY + BEF + '\n'); s = snap(p); bef, aft, _ = E.norm(BEF, AFT)
        r = E.apply_one(p, bef, aft, s); return {'r': r, 'same': open(p, 'rb').read() == b0}
    case('E4', e4)
    # E5 블록번호 꼬리 — 같으면 반영 · 다르면 보류
    def e5():
        tb = '끝 문장 ^abc123'
        p, b0 = mk('e5.md', '앞\n' + tb + '\n뒤\n'); s = snap(p)
        r_bad = E.apply_one(p, tb, '고친 문장 ^abc124', s)
        s = snap(p); r_ok = E.apply_one(p, tb, '고친 문장 ^abc123', s)
        return {'bad': r_bad, 'ok': r_ok, 'text': open(p, 'rb').read().decode()}
    case('E5', e5)
    # E6 CRLF + BOM — 줄끝·BOM 그대로
    def e6():
        p, b0 = mk('e6.md', BODY, bom=True, crlf=True); s = snap(p); bef, aft, _ = E.norm(BEF, AFT)
        r = E.apply_one(p, bef, aft, s); b1 = open(p, 'rb').read()
        return {'r': r, 'bom': b1.startswith(b'\xef\xbb\xbf'), 'lfOnly': b1.count(b'\n') - b1.count(b'\r\n'), 'crlf': b1.count(b'\r\n')}
    case('E6', e6)
    # E7 원본 콜아웃 안 → 보류
    def e7():
        body = '# 제5조\n> [!note]- 원본\n> 제5조(정의) 원본 글\n\n정리부 글\n'
        p, b0 = mk('e7.md', body); s = snap(p)
        return {'r': E.apply_one(p, '> 제5조(정의) 원본 글', '> 고친 원본', s), 'ok2': E.apply_one(p, '정리부 글', '정리부 고친 글', snap(p))}
    case('E7', e7)
    # E8 mark — 사본 기록.json: 반영 = st·appliedAt 만 · 보류 = st·memo 만 · u 도장 그 두 칸만 · 다른 바이트 무변
    def e8():
        rec = os.path.join(d, 'rec.json')
        Q = [{'k': 'qA', 'at': '2026-09-23T15:06', 'who': '나', 'target': 'note|특허|x', 'part': '47', 'file': '', 'before': 'a', 'after': 'b', 'st': '대기'},
             {'k': 'qB', 'at': '2026-09-23T15:07', 'who': '나', 'target': 'note|특허|y', 'part': '3', 'file': '', 'before': 'c', 'after': 'd', 'st': '대기'},
             {'k': 'qC', 'at': '2026-09-22T01:00', 'who': '나', 'target': 'note|특허|z', 'part': '1', 'file': '', 'before': 'e', 'after': 'f', 'st': '대기'}]
        R0 = {'v': 1, 'savedAt': '2026-09-23T17:00:00.000Z', 'by': 'pc', 'data': {'jopangi.editq': Q, 'jopangi.memo': {'m1': '메모'}},
              'u': {'jopangi.editq|qA': 1, 'jopangi.editq|qB': 2, 'jopangi.editq|qC': 3, 'jopangi.memo|m1': 4}, 'gone': {}}
        raw0 = E.js_dump(R0).encode('utf-8'); open(rec, 'wb').write(raw0)
        resf = os.path.join(d, 'res.json')
        json.dump({'vault': d, 'items': [{'k': 'qA', 'res': '반영', 'notes': ['after 끝 줄바꿈 1개 뺌(빈 줄이 문단을 가르지 않게)']},
                                         {'k': 'qB', 'res': '보류', 'why': 'before 0회(정확히 1회여야 고친다)', 'notes': []}]},
                  open(resf, 'w', encoding='utf-8'), ensure_ascii=False)
        keep = E.REC
        try:
            E.REC = rec; n = E.cmd_mark(resf, now_ms=1790185999000)
        finally:
            E.REC = keep
        raw1 = open(rec, 'rb').read(); R1 = json.loads(raw1.decode('utf-8'))
        q0 = {x['k']: x for x in Q}; q1 = {x['k']: x for x in R1['data']['jopangi.editq']}
        fch = {k: sorted(f for f in set(q0[k]) | set(q1[k]) if q0[k].get(f) != q1[k].get(f)) for k in q0}
        uch = sorted(k for k in set(R0['u']) | set(R1['u']) if R0['u'].get(k) != R1['u'].get(k))
        other = sorted(t for t in set(R0) | set(R1) if t not in ('data', 'u') and R0.get(t) != R1.get(t)) + \
            sorted('data:' + t for t in set(R0['data']) | set(R1['data']) if t != 'jopangi.editq' and R0['data'].get(t) != R1['data'].get(t))
        return {'n': n, 'fields': fch, 'st': {k: q1[k].get('st') for k in q1}, 'memoB': q1['qB'].get('memo'), 'appliedA': q1['qA'].get('appliedAt'),
                'u': uch, 'uval': [R1['u'].get(k) for k in uch], 'other': other, 'compact': E.js_dump(R1).encode('utf-8') == raw1,
                'order': [x['k'] for x in R1['data']['jopangi.editq']]}
    case('E8', e8)
    # 임시 파일이 남지 않는다
    R['tmp_left'] = [f for f in os.listdir(d) if f.startswith('.editq_')]
    # locate — 판례원본 · jimun · 이름 되찾기(사본 볼트)
    vb = os.path.join(d, 'vb'); os.makedirs(os.path.join(vb, '판례', '특허판례원본')); os.makedirs(os.path.join(vb, '노트'))
    open(os.path.join(vb, '판례', '특허판례원본', 'x.md'), 'w').write('a'); open(os.path.join(vb, '노트', '8.3.하네스.md'), 'w').write('a')
    R['locate'] = {'raw': E.locate(vb, {'target': 'prec|특허|x', 'file': '판례\\특허판례원본\\x.md'})[2],
                   'jimun': E.locate(vb, {'target': 'jimun|특허|T1', 'file': ''})[2],
                   'note': E.locate(vb, {'target': 'note|특허|8.3.하네스', 'file': ''})[1],
                   'none': E.locate(vb, {'target': 'note|특허|없는노트', 'file': ''})[2]}
    return R


def scen_ereal():
    """실제 반영 뒤 대조 — 결과 JSON · mark 전 기록.json 사본 · genie jo/data 바뀐 파일 목록"""
    R = {}
    eres, eprev, edata = ARG('--eres'), ARG('--eprev'), ARG('--edata')
    if not eres:
        return {'skip': '--eres 없음'}
    res = json.load(open(eres, encoding='utf-8'))
    R['items'] = res['items']
    base = res['vault']
    chk = []
    for it in res['items']:
        c = {'k': it['k'], 'res': it['res']}
        if it['res'] == '반영':
            p = os.path.join(base, it['file']); b = open(p, 'rb').read()
            c['vault_md5_now'] = hashlib.md5(b).hexdigest(); c['vault_md5_ok'] = c['vault_md5_now'] == it['md5_after']
            bk = os.path.join(JOPANGI, '공통', '_이전', 'vault_edit_' + time.strftime('%Y%m%d'), it['file'])
            c['backup_ok'] = os.path.exists(bk) and hashlib.md5(open(bk, 'rb').read()).hexdigest() == it['md5_before']
        chk.append(c)
    R['chk'] = chk
    if eprev:
        prev = json.loads(open(eprev, 'rb').read().decode('utf-8'))
        now_raw = open(os.path.join(_roots.spd(), 'jopangi', '기록.json'), 'rb').read()
        now = json.loads(now_raw.decode('utf-8'))
        ks = {it['k'] for it in res['items'] if it['res'] in ('반영', '보류')}
        diffs = []
        for top in set(prev) | set(now):
            if top in ('data', 'u'):
                continue
            if prev.get(top) != now.get(top):
                diffs.append('top:' + top)
        pd, nd = prev.get('data') or {}, now.get('data') or {}
        for k in set(pd) | set(nd):
            if k == 'jopangi.editq':
                continue
            if pd.get(k) != nd.get(k):
                diffs.append('data:' + k)
        pq = {x['k']: x for x in pd.get('jopangi.editq') or []}; nq = {x['k']: x for x in nd.get('jopangi.editq') or []}
        changed = [k for k in set(pq) | set(nq) if pq.get(k) != nq.get(k)]
        fields = {k: sorted(f for f in set(pq.get(k) or {}) | set(nq.get(k) or {}) if (pq.get(k) or {}).get(f) != (nq.get(k) or {}).get(f)) for k in changed}
        resk = {it['k']: it['res'] for it in res['items']}
        pu, nu = prev.get('u') or {}, now.get('u') or {}
        uchanged = [k for k in set(pu) | set(nu) if pu.get(k) != nu.get(k)]
        R['remote'] = {'otherDiffs': diffs, 'itemsChanged': sorted(changed), 'uChanged': sorted(uchanged), 'expect': sorted(ks),
                       'st': {k: (nq.get(k) or {}).get('st') for k in ks}, 'fields': fields, 'res': {k: resk.get(k) for k in ks},
                       'u': {k: [pu.get(k), nu.get(k)] for k in uchanged}, 'appliedAt': {k: (nq.get(k) or {}).get('appliedAt') for k in ks}}
    if edata:
        R['data'] = [l.strip() for l in open(edata, encoding='utf-8') if l.strip()]
    return R


def main():
    os.makedirs(WORK, exist_ok=True)
    base_b = git('show', BASE_REV + ':' + REL)
    new_raw = open(NEWF, 'rb').read()
    base, new = base_b.decode('utf-8'), new_raw.decode('utf-8')
    RES = {'src': {'base': [len(base_b), hashlib.md5(base_b).hexdigest()],
                   'new': [len(new_raw), hashlib.md5(new_raw.replace(b'\r\n', b'\n')).hexdigest(), new_raw.count(b'\r\n'), NEWF]}}
    t00 = time.time()
    if not ONLY or ONLY == 'e':
        print('… e', flush=True); RES['e'] = scen_e()
    if ONLY == 'ereal' or (not ONLY and ARG('--eres')):   # 전체 판에 --eres 를 주면 실제 반영 대조도 같이(결과 한 파일)
        RES['ereal'] = scen_ereal()
    if ONLY not in ('e', 'ereal'):
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
                            t0 = time.time(); print('… %s %s' % (key, time.strftime('%H:%M:%S')), flush=True)
                            RES[key] = r = fn(*a, **k)
                            print('   %.1fs %s' % (time.time() - t0, (r or {}).get('exc', '')), flush=True)
                        run('a', 'a/%s/%s' % (eng, tag), scen_a, brs[eng], eng, tag, src)
                        run('b', 'b/%s/%s' % (eng, tag), scen_b, brs[eng], eng, tag, src)
                        run('c', 'c/%s/%s' % (eng, tag), scen_c, brs[eng], eng, tag, src)
                        run('pad', 'pad/%s/%s' % (eng, tag), scen_c, brs[eng], eng, tag, src, True)
                        run('rx', 'rx/%s/%s' % (eng, tag), scen_rx, brs[eng], eng, tag, src)
                        run('d', 'd/%s/%s' % (eng, tag), scen_d, brs[eng], eng, tag, src)
            finally:
                for b in brs.values():
                    b.close()
                for srv, _ in SERVERS.values():
                    srv.shutdown()
    RES['sec'] = round(time.time() - t00, 1)
    raw = os.path.join(WORK, 'raw.json')
    if os.path.exists(raw) and (ONLY or len(ENGS) < 2 or len(TAGS) < 2):
        old = json.load(io.open(raw, encoding='utf-8')); old.update(RES); RES = old
    json.dump(RES, io.open(raw, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    report(RES)


def NOISE(x):
    return 'ResizeObserver loop' in x or 'Failed to load resource' in x or 'net::ERR' in x or 'harness' in x or 'sw blocked' in x


ORANGE = 'rgb(180, 83, 9)'


def report(RES):
    L = []
    CNT = {'PASS': 0, 'FAIL': 0}
    NULL = {}

    def T(n, c, i=None, tag='NEW'):
        if tag == 'BASE':
            NULL.setdefault(n, []).append(bool(c)); return
        CNT['PASS' if c else 'FAIL'] += 1
        L.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c or i is None else ' | ' + json.dumps(i, ensure_ascii=False, default=str)[:900]))

    def I(n, v):
        L.append('INFO | ' + n + ' | ' + (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)[:1800]))
    g = lambda d, *ks: __import__('functools').reduce(lambda a, k: (a[k] if isinstance(a, list) and isinstance(k, int) and -len(a) <= k < len(a)
                                                                    else (a or {}).get(k) if isinstance(a, dict) else None), ks, d)
    cg = lambda q: [x for x in ((q or {}).get('grp') or []) if x.startswith('Claude')]   # 결과 머리 줄(끝의 「↵ 열기 · Esc 닫기」 안내 줄은 뺀다)
    sb, sn = RES['src']['base'], RES['src']['new']
    I('바탕 BASE = %s:%s' % (BASE_REV, REL), '%d B · md5 %s' % tuple(sb))
    T('바탕 md5 = mok_popup_phone 인도 판(1,031,441 B · 3aefbb3f…)', sb[1] == BASE_MD5_LF and sb[0] == BASE_SIZE, sb)
    I('새 판 NEW', '%d B · md5(LF) %s · CRLF %d · %s' % tuple(sn))
    I('시간(초)', RES.get('sec'))
    for eng in ENGS:
        E = '[%s] ' % eng
        for tag in TAGS:
            Tt = lambda n, c, i=None: T(E + n, c, i, tag)
            A = RES.get('a/%s/%s' % (eng, tag))
            if A:
                if A.get('exc'):
                    Tt('A 예외 없음', False, A['exc'])
                for kind, lab in (('callout', '민소 민기출 24-61-2 「⑦ 문제-2」 콜아웃'), ('jimun', '1차객 지문 팝업'), ('note', '노트 팝업'), ('prec', '판례 팝업'), ('claude', 'Claude 창')):
                    V = g(A, 'pops', kind) or {}
                    ch = V.get('chk') or {}
                    Tt('A %s — 높이 140 · scrollTop 70 에서 머리 1/4·가운데·3/4 점의 맨 위 = 머리 안' % lab, bool(ch) and ch.get('oneOk'), {'open': V.get('open'), 'one': ch.get('one'), 'st': ch.get('st')})
                    Tt('A %s — 스크롤 전 구간(10px 마다) 어디서도 글줄이 머리를 안 덮음' % lab, bool(ch) and ch.get('bad') == 0, {'range': ch.get('range'), 'bad': ch.get('bad'), 'scan': ch.get('scan')})
                    if tag == 'NEW':
                        I(E + 'A %s — 머리 z-index · 스크롤 범위' % lab, {'phZ': ch.get('phZ'), 'range': ch.get('range'), 'n': ch.get('scanN')})
                if tag == 'NEW':
                    errs = [x for x in (A.get('errs') or []) if not NOISE(x)]
                    Tt('A 콘솔 오류 0', not errs, errs[:6])
            B = RES.get('b/%s/%s' % (eng, tag))
            if B:
                if B.get('exc'):
                    Tt('B 예외 없음', False, B['exc'])
                inf = B.get('info') or {}
                Tt('B 콜아웃 팝업에 안내 글 0(「제목의 ˅ 를 눌러 접고 편다 …」)', bool(inf) and not any('제목의' in x for x in inf.get('cdim') or []), inf)
                Tt('B 접기 그대로(제목 있는 콜아웃에서 ˅ 누르면 줄이 접히고 다시 누르면 펴진다)', bool((B.get('htog') or {}).get('changed')) and g(B, 'htog', 'hidden2') == g(B, 'htog', 'hidden0'), {'pick': B.get('pick'), 'htog': B.get('htog')})
                Tt('B 길게 누르기 메뉴 그대로(마우스 0.5초 → 🗒 메모 · ✎ 수정)', bool(B.get('menu')) and any('메모' in x for x in B['menu']), {'at': B.get('at'), 'menu': B.get('menu')})
            for mode in ('c', 'pad'):
                C = RES.get('%s/%s/%s' % (mode, eng, tag))
                if not C:
                    continue
                M = '아이패드 터치 ' if mode == 'pad' else ''
                if C.get('exc'):
                    Tt('C %s예외 없음' % M, False, C['exc'])
                rows = C.get('rows') or []
                r1 = [r for r in rows if r['code'] == MS_CODE[4:]]
                r2 = [r for r in rows if r['code'] == MS_MENT[4:]]
                others = [r for r in rows if r['code'] not in (MS_CODE[4:], MS_MENT[4:]) and r['btn']]
                if mode == 'c':
                    Tt('C 보드 %s 줄 「Claude 1」(700 · 주황 · 점수 칩 바로 오른쪽)' % MS_CODE[4:], len(r1) == 1 and len(r1[0]['btn']) == 1 and r1[0]['btn'][0]['t'] == 'Claude1'
                       and r1[0]['btn'][0]['fw'] == '700' and r1[0]['btn'][0]['color'] == ORANGE and r1[0]['afterScore'], r1)
                    Tt('C 보드 %s 줄 「Claude ↩」(언급만 · 회색 「Claude」 + 주황 ↩)' % MS_MENT[4:], len(r2) == 1 and len(r2[0]['btn']) == 1 and r2[0]['btn'][0]['t'] == 'Claude↩' and r2[0]['btn'][0]['fw'] != '700', r2)
                    Tt('C 보드 다른 %d줄 단추 0(자리표만 숨김)' % max(0, len(rows) - 2), len(rows) == 76 and not others, {'rows': len(rows), 'others': others[:3]})
                ab = C.get('afterRowBtn') or {}
                Tt('C %s줄 단추 누름 = 창만(카드 안 열림 · 창 제목 「Claude · %s · %s」)' % (M, MS_CODE, MS_NAME), bool(C.get('rowBtnTap')) and [p['pk'] for p in ab.get('pops') or []] == ['claude|' + MS_CODE]
                   and g(ab, 'win', 'title') == 'Claude · %s · %s' % (MS_CODE, MS_NAME), {'tap': C.get('rowBtnTap'), 'pops': [p['pk'] for p in ab.get('pops') or []], 'title': g(ab, 'win', 'title')})
                tb = C.get('tabs') or {}
                tl = [t['t'] for t in tb.get('tabs') or []]
                cl = [t for t in tb.get('tabs') or [] if 'cltab' in t['cls']]
                Tt('C %s카드 팝업 탭 = 문제·해설·채점·「Claude 1」(주황 · 테두리 #fed7aa)' % M, tl == ['문제', '해설', '채점', 'Claude 1'] and len(cl) == 1 and cl[0]['color'] == ORANGE and cl[0]['bc'] == 'rgb(254, 215, 170)', tb)
                at2 = C.get('afterTab') or {}
                on = [t['t'] for t in g(at2, 'tabs', 'tabs') or [] if t['on']]
                Tt('C %s탭 「Claude 1」 → 새 팝업 창 · 카드 탭 무변(문제 켜짐 그대로)' % M, bool(C.get('tabTap')) and len(at2.get('pops') or []) == 2 and (at2.get('pops') or [{}])[-1].get('pk') == 'claude|' + MS_CODE and on == ['문제'],
                   {'tap': C.get('tabTap'), 'pops': [p['pk'] for p in at2.get('pops') or []], 'on': on})
                if mode == 'c':
                    tn = [t for t in g(C, 'tabsNo', 'tabs') or [] if 'cltab' in t['cls']]
                    Tt('C 답 없는 카드 탭 = 회색 「Claude」 → 「아직 답 없음」 창', len(tn) == 1 and tn[0]['t'] == 'Claude' and tn[0]['color'] != ORANGE and bool(C.get('tabNoTap'))
                       and any('아직 없다' in x for x in g(C, 'winNo', 'note') or []), {'tab': tn, 'win': C.get('winNo')})
                    w = C.get('win') or {}
                    Tt('C 창 — 제목 「Claude · %s · %s」 · 답 MS901 · 머리 오른쪽 끝 %s' % (MS_CODE, MS_NAME, MS_CODE), w.get('title') == 'Claude · %s · %s' % (MS_CODE, MS_NAME)
                       and w.get('answers') == ['MS901'] and g(w, 'head', 0, 2) == MS_CODE, w)
                    ah = [p['pk'] for p in C.get('afterHead') or []]
                    Tt('C 창 머리 코드 단추 → popCard4 기출 카드(%s)' % MS_CODE, bool(C.get('headUidTap')) and any(('🧾 기출 · ' + MS_CODE) in (x or '') for x in ah), ah)
                    abd = [p['pk'] for p in C.get('afterBody') or []]
                    Tt('C 창 본문 %s 단추 → 그 카드' % MS_MENT, bool(C.get('bodyUidTap')) and any(('🧾 기출 · ' + MS_MENT) in (x or '') for x in abd), abd)
                    Tt('C ✎ 정정 → jopangi.clfix.MS901.done === false · 고친 글 · ts 숫자', g(C, 'fix', 'fix', 'done') is False and g(C, 'fix', 'fix', 'hasWord') is True and g(C, 'fix', 'fix', 'ts') == 'number', C.get('fix'))
                    oth = C.get('other') or {}
                    Tt('C 특상디 2차 기출 · 민소 사례·GS 보드에 단추 0', bool(oth) and all(v['btn'] == 0 for v in oth.values()) and all(v['rows'] > 0 for k, v in oth.items() if k.endswith('기출')), oth)
                    tk = C.get('tkCard') or {}
                    Tt('C 특허 기출 카드 팝업에 「Claude」 탭 0', bool(tk) and tk.get('cltab') == 0, tk)
                if tag == 'NEW':
                    errs = [x for x in (C.get('errs') or []) if not NOISE(x)]
                    Tt('C %s콘솔 오류 0' % M, not errs, errs[:6])
            X = RES.get('rx/%s/%s' % (eng, tag))
            if X:
                got = dict(zip(RX_IN, X.get('rx') or []))
                Tt('C-정규식 — MS001·MS901·T001 안 걸림', all(got.get(k) == '' for k in ('MS001', 'MS901', 'T001')), got)
                Tt('C-정규식 — 민기출 24-61-2 · T0138603 · T0946093P7 걸림(글자 그대로)', got.get(MS_CODE) == MS_CODE and got.get('T0138603') == 'T0138603' and got.get('T0946093P7') == 'T0946093P7', got)
                Tt('C-정규식 — 「민기출 24-61-23」 안 걸림 · 카드 열쇠 앞머리 「민기출 24-61-2-…」 는 코드만', got.get('민기출 24-61-23') == '' and got.get('민기출 24-61-2-관할') == MS_CODE, got)
            D = RES.get('d/%s/%s' % (eng, tag))
            if D:
                if D.get('exc'):
                    Tt('D 예외 없음', False, D['exc'])
                sc = D.get('scopes') or []
                Tt('D 범위 단추 차례 = 조문·판례·지문·메모·Claude·정리·두문자 · 「논리」 글자 0', [s['s'] for s in sc] == ['jo', 'prec', 'jimun', 'memo', 'claude', 'omr', 'stk'] and D.get('nonLogic') == 0
                   and any(s['s'] == 'claude' and s['t'].startswith('Claude') and 'C' in (s['before'] or '') for s in sc), {'scopes': sc, 'logic': D.get('nonLogic')})
                q1 = D.get('q1') or {}
                Tt('D 「Claude」 켜고 픽스처 낱말 → 1건(머리 「MS901 · %s」 · 아이콘 주황 800 「C」 · 법 민소)' % MS_CODE, cg(q1) == ['Claude — 1건'] and len(q1.get('rows') or []) == 1
                   and g(q1, 'rows', 0, 'head') == 'MS901 · ' + MS_CODE and g(q1, 'rows', 0, 'icon') == 'C' and g(q1, 'rows', 0, 'iconColor') == ORANGE and g(q1, 'rows', 0, 'iconFw') == '800' and g(q1, 'rows', 0, 'tag') == '민소', q1)
                Tt('D 법 칩 민소만 끄면 0', cg(D.get('q1off')) == ['Claude — 0건'], D.get('q1off'))
                Tt('D 특허 픽스처(T901)는 특허 켤 때만 · 머리 「T901 · T0138603」(1차객 풀 밖이면 열쇠 그대로)', cg(D.get('qT_on')) == ['Claude — 1건'] and cg(D.get('qT_off')) == ['Claude — 0건'] and g(D, 'qT_on', 'rows', 0, 'head') == 'T901 · T0138603', [D.get('qT_on'), D.get('qT_off')])
                Tt('D 붙은 카드 이름으로도 걸림(「반소이송가부」)', cg(D.get('qName')) == ['Claude — 1건'], D.get('qName'))
                at = D.get('afterTap') or {}
                Tt('D 결과 누름 → 검색 닫히고 Claude 창', bool(D.get('rowTap')) and g(at, 'state', 'skOpen') is False and g(at, 'win', 'answers') == ['MS901'], at)
                Tt('D 정정본에만 있는 낱말도 걸림', g(D, 'fix', 'fix', 'hasWord') is True and cg(D.get('qFix')) == ['Claude — 1건'], [D.get('fix'), D.get('qFix')])
                Tt('D CL_STATE fail → 「Claude 답을 못 받았다 — 토큰·네트워크」', g(D, 'mode_500', 'cl') == 'fail' and 'Claude 답을 못 받았다 — 토큰·네트워크' in (g(D, 'mode_500', 'q', 'grp') or []), D.get('mode_500'))
                Tt('D CL_STATE wait → 「Claude 답을 받는 중이다」', g(D, 'mode_hang', 'cl') == 'wait' and 'Claude 답을 받는 중이다' in (g(D, 'mode_hang', 'q', 'grp') or []), D.get('mode_hang'))
                old = D.get('old') or {}
                oe = [x for x in (old.get('errs') or []) if not NOISE(x)]
                Tt('D 옛 jopangi_skon 에 logic:true — 오류 0 · claude 꺼짐으로 시작 · 검색 됨', not oe and g(old, 'skon', 'claude') is False and 'logic' not in (old.get('skon') or {}) and cg(old.get('q')) == ['Claude — 1건'], old)
                if tag == 'NEW':
                    errs = [x for x in (D.get('errs') or []) if not NOISE(x)]
                    Tt('D 콘솔 오류 0', not errs, errs[:6])
    Ee = RES.get('e')
    if Ee:
        c = Ee.get('cases') or {}
        T('E1 도구 — 그대로면 반영 · 끝 줄바꿈 1개 뺌(빈 줄 없음) · 바뀐 곳 밖 동일 · 백업 = 원본', g(c, 'E1', 'r', 'res') == '반영' and g(c, 'E1', 'expect') is True and g(c, 'E1', 'blank') is False and g(c, 'E1', 'backup') is True
          and g(c, 'E1', 'notes') == ['after 끝 줄바꿈 1개 뺌(빈 줄이 문단을 가르지 않게)'], c.get('E1'))
        T('E2 도구 — 읽은 뒤 파일이 바뀌어도 before 가 1회면 다시 찾아 반영(덧붙인 줄 살아 있음)', g(c, 'E2', 'r', 'res') == '반영' and g(c, 'E2', 'r', 'changed_since_plan') is True and g(c, 'E2', 'kept') is True, c.get('E2'))
        T('E3 도구 — 읽은 뒤 before 가 사라지면 보류(까닭 = 그 사이 바뀜) · 파일 무변', g(c, 'E3', 'r', 'res') == '보류' and '그 사이 바뀌어' in (g(c, 'E3', 'r', 'why') or '') and g(c, 'E3', 'same') is True, c.get('E3'))
        T('E4 도구 — before 두 번이면 보류 · 파일 무변', g(c, 'E4', 'r', 'res') == '보류' and '2회' in (g(c, 'E4', 'r', 'why') or '') and g(c, 'E4', 'same') is True, c.get('E4'))
        T('E5 도구 — 블록번호 꼬리 다르면 보류 · 같으면 반영', g(c, 'E5', 'bad', 'res') == '보류' and g(c, 'E5', 'ok', 'res') == '반영' and '고친 문장 ^abc123' in (g(c, 'E5', 'text') or ''), c.get('E5'))
        T('E6 도구 — CRLF·BOM 그대로(LF 단독 0)', g(c, 'E6', 'r', 'res') == '반영' and g(c, 'E6', 'bom') is True and g(c, 'E6', 'lfOnly') == 0, c.get('E6'))
        T('E7 도구 — 조문 원본 콜아웃 안은 보류 · 정리부는 반영', g(c, 'E7', 'r', 'res') == '보류' and '원본 콜아웃' in (g(c, 'E7', 'r', 'why') or '') and g(c, 'E7', 'ok2', 'res') == '반영', c.get('E7'))
        e8 = c.get('E8') or {}
        T('E8 도구 mark — 반영 항목은 st·appliedAt 만 · 보류 항목은 st·memo 만 · 결과에 없는 항목 무변(E-7 「다른 칸 무변」)',
          g(e8, 'fields') == {'qA': ['appliedAt', 'st'], 'qB': ['memo', 'st'], 'qC': []} and g(e8, 'st') == {'qA': '반영됨', 'qB': '보류', 'qC': '대기'}
          and g(e8, 'memoB') == 'before 0회(정확히 1회여야 고친다)' and re.match(r'^\d{4}-\d\d-\d\dT\d\d:\d\d$', g(e8, 'appliedA') or '') is not None, e8)
        T('E8 도구 mark — u 도장은 그 두 열쇠만 = 지금(ms) · 다른 칸·차례 무변 · JSON.stringify 꼴 그대로', g(e8, 'u') == ['jopangi.editq|qA', 'jopangi.editq|qB']
          and g(e8, 'uval') == [1790185999000, 1790185999000] and g(e8, 'other') == [] and g(e8, 'compact') is True and g(e8, 'order') == ['qA', 'qB', 'qC'] and g(e8, 'n') == 2, e8)
        T('E 도구 — 임시 파일(.editq_*) 안 남음', Ee.get('tmp_left') == [], Ee.get('tmp_left'))
        lc = Ee.get('locate') or {}
        T('E 도구 — 자리 되찾기: 판례원본 보류 · jimun 보류 · note 이름 1개면 되찾음 · 0개면 보류', '판례원본' in (lc.get('raw') or '') and '원장' in (lc.get('jimun') or '')
          and (lc.get('note') or '').endswith('8.3.하네스.md') and '0개' in (lc.get('none') or ''), lc)
    Er = RES.get('ereal')
    if Er and not Er.get('skip'):
        I('E 실제 반영 결과', [{k: it.get(k) for k in ('k', 'res', 'file', 'before40', 'after40', 'why', 'notes')} for it in Er.get('items') or []])
        for c in Er.get('chk') or []:
            if c['res'] == '반영':
                T('E 실제 %s — 볼트 되읽기 md5 = 결과 md5_after · 백업 = 원본' % c['k'], c.get('vault_md5_ok') and c.get('backup_ok'), c)
        rm = Er.get('remote') or {}
        if rm:
            T('E 실제 — 원격 기록.json: 바뀐 editq 항목 = 반영·보류 항목 · u 도장도 그 칸만 · 다른 칸 무변', rm.get('itemsChanged') == rm.get('expect') and rm.get('uChanged') == ['jopangi.editq|' + k for k in rm.get('expect')]
              and rm.get('otherDiffs') == [] and all(v in ('반영됨', '보류') for v in (rm.get('st') or {}).values()), rm)
            T('E 실제 — 그 항목 안에서 바뀐 칸: 반영 = st·appliedAt · 보류 = st·memo · u 도장은 전보다 크다',
              all((rm.get('fields') or {}).get(k) == (['appliedAt', 'st'] if (rm.get('res') or {}).get(k) == '반영' else ['memo', 'st']) for k in rm.get('expect') or [])
              and all((v[0] or 0) < (v[1] or 0) for v in (rm.get('u') or {}).values()), rm)
        if Er.get('data') is not None:
            I('E 실제 — genie jo/data 바뀐 파일', Er.get('data'))
    tot = sum(len(v) for v in NULL.values()); fails = sum(1 for v in NULL.values() for x in v if not x)
    L.append('')
    L.append('── 헛잣대(규칙 ⑩) — 같은 잣대를 바탕 %s 에 돌린 결과: %d 중 FAIL %d · PASS %d ──' % (BASE_REV, tot, fails, tot - fails))
    grp = {}
    for n, v in NULL.items():
        key = re.sub(r'^\[[a-z]+\] ', '', n)
        a = grp.setdefault(key, [0, 0]); a[0] += sum(1 for x in v if not x); a[1] += len(v)
    for k in sorted(grp):
        L.append('BASE | %s | FAIL %d / %d' % (k, grp[k][0], grp[k][1]))
    body = '\n'.join(L) + '\n\n합계  PASS %d · FAIL %d  (%s초)\n' % (CNT['PASS'], CNT['FAIL'], RES.get('sec'))
    print(body[-3000:])
    wr(os.path.join(OUT, '_harness_jo_ms_claude_result.txt'), body)


if __name__ == '__main__':
    if '--report' in sys.argv:
        RES = json.load(io.open(os.path.join(WORK, 'raw.json'), encoding='utf-8'))
        report(RES)
    else:
        main()
