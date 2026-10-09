# -*- coding: utf-8 -*-
r"""자과 띄우기 헬퍼 JG — _task_qa_slim2 §A-1-2(2026-10-08) · 자과 하네스가 서로 import 해 쓰던 띄우기 정의를 한 곳에 둔다.

몸 = 제공 하네스의 지금 정의를 글자 그대로(거울 R = N: 정본 · 2026-10-08 03:2x md5 48 같음) — 정의마다 바로 위 줄에 「← 제공 하네스:줄」.
  같은 이름을 제공 하네스끼리 다르게 정의한 것은 합치지 않고 꼬리로 갈랐다(고르지 않음 · 본 세션 결정 거리):
    _ES = jagwa/gigu/_harness_earth_shell      _E  = jagwa/gigu/_harness_earth            _PP = jagwa/moolri/_harness_jagwa_physphone
    _HU = jagwa/_harness_jagwa_uid             _PF = jagwa/gigu/_harness_jagwa_penfinger   _PW = jagwa/_harness_jagwa_phone_win
    _BO = jagwa/saengmul/_harness_bio_ocrfix
  꼬리를 단 정의 안에서 그 이름을 부르던 자리도 같은 표로 바꿨다(그 밖 글자 무변 — 같음 확인 = out/jgh/equiv.csv · 위치 뺀 ast.dump).
  겹침이 없는 이름은 그대로(CHROME · HEAD · TAIL · Remote · REMOTE · route_handler · fresh · app_src · Srv · Dev · SJS · P · P2 · both · APPS …).

왜 _qa_common(QC) 이 아니라 따로 한 파일인가: 사슬은 하네스가 연 파일을 입력으로 추적해 저장본 열쇠에 넣는다 —
  자과 띄우기를 QC 에 넣으면 민법 · 시간표 하네스 열쇠가 자과 고침 때마다 같이 바뀐다(jo 몸을 _qa_jo_common.py 에 바이트 그대로 둔 것과 같은 까닭).

쓰는 법(자과 하네스) — 머리 5 줄과 `import _qa_common as QC` 바로 다음 줄:
    import _qa_jagwa_common as JG
  옛 부름 → 새 부름 = out/jgh/rewire.json · rewire.md(예 E.STUB → JG.STUB_ES · hp.route_handler(hp.REMOTE) → JG.route_handler(JG.REMOTE) · HU.Dev → JG.Dev).
  자리 · 인자 값(옛 제공 하네스가 제 sys.argv 와 제 자리(HERE)로 정하던 것)은 부르는 쪽이 넘긴다: JG.conf(VENDOR_PP=…, SPD_PP=…) — 받는 이름 = CONF.
    기본값 = 옛 식에서 argv 만 뗀 것(argv 를 안 줬을 때의 옛 값과 같다) · 하네스마다 넘길 값 = rewire.json 「conf」.
  잠깐 바꿔 쓰는 글(exam_wrong_mark 의 토큰 없음 갈래가 PP.INIT 을 바꿨다 되돌리던 것)은 JG.INIT_PP 를 같은 꼴로 바꿨다 되돌린다(Pg_PP 가 부를 때 읽는다).

부작용 0: import 때 크롬 · 서버 · 파일 쓰기 · git · sys.argv 읽기 · stdout 바꿈이 없다(머리 5 줄의 sys.path 덧붙임과 객체 만들기 REMOTE = Remote() 뿐).
  단 하나 — 설정 기본값의 tempfile.gettempdir() 가 그 프로세스 첫 부름이면 표준 라이브러리가 TEMP 에 시험 파일을 만들고 바로 지운다(2026-10-08 감사 훅 실측 cold 1 건 · warm 0 건 · 옛 제공 하네스 import 도 같은 부름이 있었다).
  QC 를 import 하지 않는다 — QC 는 import 때 argv 를 떼고 끝에 스냅샷을 적는다(부르는 하네스가 먼저 import 한다).
  옛 제공 하네스 import 가 하던 일(earth_shell _ensure_base 의 git show · TEMP 와 하네스 옆 폴더 makedirs · stdout utf-8 · sys.argv 읽기)은 여기서 하지 않는다 — 그것에 기대던 소비 자리는 rewire 안내에.
정의를 고칠 때: 이 파일 한 곳만(제공 하네스에 같은 정의를 다시 두지 않는다) · 이 파일 바이트가 바뀌면 이 파일을 연 자과 하네스의 저장본 열쇠가 다 바뀐다.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import base64, hashlib, http.server, io, json, os, re, socketserver, subprocess, tempfile, threading, time, urllib.parse   # noqa: E402,F401
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer   # noqa: E402

JG_DIR = os.path.dirname(os.path.abspath(__file__))   # 이 파일 자리(N: 정본 = N_ROOT · genie _qa · 거울 R 의 맨 위) — REFDIR 기본값이 이 자리 기준

# ── 설정 — 옛 제공 하네스가 제 sys.argv · 제 자리로 정하던 값 · JG 는 argv 를 안 읽는다 · 기본값 = 옛 식에서 argv 만 뗀 것 · 다른 값은 conf(…) 로
GENIE = _roots.genie()   # ← phone_win:30 GENIE = _roots.genie()(uid · penfinger · earth_shell · bio_ocrfix 도 같은 식) — git_PW · IMG
SPDROOT = _roots.spd()   # ← penfinger:29 · bio_ocrfix:21 SPDROOT = _roots.spd()(earth_shell:87 도 같은 식) — serve_PF · serve_PW · serve_BO
VENDOR_PP = os.path.join(tempfile.gettempdir(), 'h_jagwa', 'vendor')   # ← physphone:44 VENDOR = ARG('--vendor', 이 식) — route_handler
NOTES = os.path.join(os.path.dirname(_roots.spd()), 'notes')   # ← physphone:43 NOTES = ARG('--notes', 이 식) — Remote
SPD_PP = _roots.spd()   # ← physphone:42 SPD = ARG('--spd', 이 식) — Remote(physprev 는 옛 PP.SPD = … 로 바꿔 썼다)
SHOTS = os.path.join(tempfile.gettempdir(), 'h_jagwa', 'shots')   # ← physphone:48 SHOTS = ARG('--shots', 이 식) — Pg_PP.shot
SPD_HU = _roots.spd()   # ← uid:29 SPD = _roots.spd() — Srv
WORK_PF = os.path.join(tempfile.gettempdir(), 'h_penfinger')   # ← penfinger:34(같은 줄 os.makedirs 는 뺌 — serve_PF · serve_PW 가 제 하위 폴더를 makedirs) — serve_PF · serve_PW
IMG = os.path.join(GENIE, 'jagwa', 'img')   # ← phone_win:32 IMG = ARG('--img', 이 식) — serve_PW
VENDOR_PW = None   # ← phone_win:36 VENDOR = ARG('--vendor')(없으면 None) — Pg_PW
WORK_BO = os.path.join(tempfile.gettempdir(), 'h_bio_ocrfix')   # ← bio_ocrfix:28(같은 줄 os.makedirs 는 뺌 — serve_BO 가 제 하위 폴더를 makedirs) — serve_BO
REFDIR = os.path.join(JG_DIR, 'jagwa', 'saengmul', '_ocrfix', 'ref')   # ← bio_ocrfix:26 os.path.join(HERE, '_ocrfix', 'ref')(HERE = jagwa/saengmul · 같은 모양 사본에서 같은 자리) — serve_BO
CONF = ('GENIE', 'SPDROOT', 'VENDOR_PP', 'NOTES', 'SPD_PP', 'SHOTS', 'SPD_HU', 'WORK_PF', 'IMG', 'VENDOR_PW', 'WORK_BO', 'REFDIR')


def conf(**kw):
    """자리 · 인자 값을 부르는 쪽이 넘긴다(옛 제공 하네스가 제 argv · 제 자리로 정하던 값) — 모르는 이름이면 멈춘다(오타로 옛 값이 조용히 남지 않게) · 넣은 값을 돌려준다"""
    bad = sorted(k for k in kw if k not in CONF)
    if bad:
        raise SystemExit('_qa_jagwa_common.conf: 모르는 이름 %s — 받는 이름: %s' % (', '.join(bad), ', '.join(CONF)))
    globals().update(kw)
    return {k: globals()[k] for k in kw}


# ═════════ earth_shell(_ES) — 크롬 자리 · 스텁 · 쪽 안 HEAD/TAIL(가짜 GitHub · T · wait · until · fire · /result) — claude_slot · claude_slot_add1 · touch_ipad · earth_ocrfix 가 씀 ═════════


# ← jagwa/gigu/_harness_earth_shell.py:92-92 CHROME · 글자 그대로
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


# ← jagwa/gigu/_harness_earth_shell.py:94-101 STUB · 글자 그대로 · 이름 바꿈 STUB→STUB_ES
STUB_ES = """<script>try{localStorage.setItem('subj','__SUBJ__')}catch(e){}</script>
<script>
window.katex={render:function(){},renderToString:function(s){return s}};window.renderMathInElement=function(){};
window.__err=[];
window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+(e.filename||'').split('/').pop()+':'+e.lineno)});
window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
</script>
"""


# ← _task_qa_fix1 §A-1(2026-10-09) 새 정의 · 쪽 안 기다림 wait(ms) 한 벌 — JG.HEAD(earth_shell · claude_slot · claude_slot_add1 이 씀) · earth_shell PHONE · mcsheet HEAD · bref HEAD 가 이 글을 이어 붙여 쓴다(같은 일 두 벌 없음)
#   뜻 = ms 기다린 뒤 + 앱이 쉴 때까지(진행 중 IndexedDB 쓰기 0 · requestAnimationFrame 두 번) · 쉼 기다림 최대 5 초 — 부르는 곳(earth_shell 564 · bref 63 · mcsheet 54 · claude_slot 23)은 안 고침
#   진행 중 쓰기 셈 = 앱의 전역 put · putRaw · del 을 시험 쪽에서 감싸 들어갈 때 +1 · 끝날 때 −1(앱 파일 무변 · 앱의 IndexedDB 쓰기는 readwrite 두 곳 = put · del 뿐 · putRaw = 갈아 끼우기 전 put)
#   감싸기 = 이 글이 놓일 때(앱 스크립트 뒤) 한 번 + wait 마다 다시 봄(아직 없던 · 뒤에 갈아 끼운 함수) · 시계 = performance.now(가짜 Date.now 하네스와 안 부딪힘)
#   5 초 넘게 안 끝난 쓰기는 멎은 것으로 보고 안 기다림 · rAF 가 안 오면(숨은 쪽) 250ms 뒤 넘어감 · 셈 = window.__qaIdle {n 부른 수 · ms 쉼 기다림 합 · cap 5 초 다 쓴 수}
WAIT_JS = r""" const __qaI=window.__qaIdle||(window.__qaIdle={live:new Map(),id:0,n:0,ms:0,cap:0});
 const __qaHook=()=>{['put','putRaw','del'].forEach(k=>{const f=window[k];if(typeof f!=='function'||f.__qaw)return;
   const g=function(){const id=++__qaI.id;__qaI.live.set(id,performance.now());let p;
     try{p=f.apply(this,arguments)}catch(e){__qaI.live.delete(id);throw e}
     Promise.resolve(p).then(()=>{__qaI.live.delete(id)},()=>{__qaI.live.delete(id)});return p};
   g.__qaw=1;try{window[k]=g}catch(e){}})};
 try{__qaHook()}catch(e){}
 const __qaBusy=()=>{const t=performance.now();for(const t0 of __qaI.live.values())if(t-t0<5000)return true;return false};
 const __qaRaf2=()=>new Promise(r=>{let d=0;const f=()=>{if(!d){d=1;r()}};try{requestAnimationFrame(()=>requestAnimationFrame(f))}catch(e){f()}setTimeout(f,250)});
 const wait=async ms=>{await new Promise(r=>setTimeout(r,ms));try{__qaHook()}catch(e){}
   const t0=performance.now();while(__qaBusy()&&performance.now()-t0<5000)await new Promise(r=>setTimeout(r,10));
   await __qaRaf2();const dt=performance.now()-t0;__qaI.n++;__qaI.ms+=dt;if(dt>=5000)__qaI.cap++};"""


# ← jagwa/gigu/_harness_earth_shell.py:103-175 HEAD · 글자 그대로
# ← _task_qa_fix1 §A-1(10/9) — 그 가운데 wait 정의 한 줄만 WAIT_JS 로 갈음(옛 줄은 쪽 안 주석으로 그 자리에 남김)
HEAD = r"""<script>
(function(){
 const R=[]; const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+(c?'':' | '+JSON.stringify(i===undefined?null:i)));
 const N=(n,i)=>R.push('NOTE | '+n+' | '+JSON.stringify(i===undefined?null:i));
 const __nativeFetch=window.fetch.bind(window);
 window.fetch=async function(url,opt){
  opt=opt||{};const u=String(url);
  const m=/api\.github\.com\/repos\/([^\/]+\/[^\/]+)\/contents\/([^?]+)/.exec(u);
  if(!m){ if(/api\.github\.com\/repos\/zzikkaplan\/notes/.test(u))return {ok:true,status:200,json:async()=>({name:'notes'}),text:async()=>''};
          if(/^https?:/i.test(u))return {ok:false,status:599,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
          return __nativeFetch(url,opt); }
  const path=decodeURIComponent(m[2]);
  if(m[1]==='zzikkaplan/notes')return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
  if((opt.method||'GET')==='PUT')return {ok:true,status:200,json:async()=>({content:{sha:'x'}}),text:async()=>''};
  const r=await __nativeFetch('/data/'+encodeURI(path),{cache:'no-store'});
  if(!r.ok)return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
  const acc=(opt.headers||{}).Accept||'';
  if(acc.indexOf('raw')>=0)return r;
  return {ok:true,status:200,json:async()=>({sha:'sha'}),text:async()=>JSON.stringify({sha:'sha'})};
 };
 /* 옛 줄: const wait=ms=>new Promise(r=>setTimeout(r,ms)); — _task_qa_fix1 §A-1(10/9) 새 정의 = 이 파일 WAIT_JS 한 벌(바로 아래 이어 붙임) */
""" + WAIT_JS + r"""
 const until=async(fn,ms)=>{const t0=Date.now();while(Date.now()-t0<(ms||8000)){try{if(fn())return true}catch(e){}await wait(60)}return false};
 setInterval(()=>{try{__nativeFetch('/partial',{method:'POST',body:R.join(String.fromCharCode(10))+String.fromCharCode(10)+'(err) '+JSON.stringify(window.__err||[])})}catch(e){}},3000);
 const grp=async(name,fn)=>{try{await fn()}catch(e){T(name+' 묶음 예외',false,String(e&&e.stack||e).slice(0,300))}};
 const $$$=s=>[...document.querySelectorAll(s)];
 const txt=el=>(el?String(el.textContent||'').replace(/\s+/g,' ').trim():'');
 const nums=()=>$$$('#list .item .num').map(x=>txt(x));
 /* 합성 이벤트 — 앱이 읽는 값(clientX·clientY·pointerType·pointerId·getCoalescedEvents)만 얹은
    평범한 `Event` 를 쓴다. 앱 코드는 한 글자도 안 고친다 — 읽는 것이 같으니 타는 길도 같다.
    (`new PointerEvent` 도 이 크롬에서 멀줦하다 — pointerType 까지 실린다. 둘 중 아무거나 된다.) */
 const mkPE=(t,x,y,pt,id)=>{const e=new Event(t,{bubbles:true,cancelable:true});
   Object.defineProperties(e,{clientX:{get:()=>x},clientY:{get:()=>y},
     pageX:{get:()=>x},pageY:{get:()=>y},
     pointerType:{get:()=>(pt||'pen')},pointerId:{get:()=>(id||31)},
     isPrimary:{get:()=>true},pressure:{get:()=>0.5},button:{get:()=>0},buttons:{get:()=>1},
     getCoalescedEvents:{value:()=>[]}});
   return e};
 /* 던진 것이 **닿았는지 확인한다.** 돌려주는 값 = 던진 횟수(0 = 끝내 못 닿음).
    ⚠ 안 닿는 데에는 까닭이 있다 — `inkPierce`(1420줄)가 그 자리 밑에 눌릴 것이 있으면
      capture 단계에서 `stopPropagation` 해서 pointerdown 이 `#qink` 까지 안 온다(앱이 일부러 그런 것).
      그래서 획을 그을 자리는 `underInk` 로 미리 골라야 한다(V-5 참조). 여기 다시 던지기는 더부살이다. */
 const fire=async(el,t,x,y,pt,id)=>{
   for(let a=1;a<=10;a++){
     let got=0; const probe=()=>{got=1};
     el.addEventListener(t,probe,true);
     el.dispatchEvent(mkPE(t,x,y,pt,id));
     el.removeEventListener(t,probe,true);
     if(got)return a;
     await wait(60);
   }
   return 0};
 const drag=async(el,x0,y0,x1,y1,pt)=>{
   const a=await fire(el,'pointerdown',x0,y0,pt,31);
   const b=await fire(el,'pointermove',x1,y1,pt,31);
   const c=await fire(el,'pointerup',x1,y1,pt,31);
   return [a,b,c]};
 const stackAt=(x,y)=>document.elementsFromPoint(x,y).map(e=>e.id||((e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className)||e.tagName));
 const cap=async(name,html)=>{try{await __nativeFetch('/cap?n='+encodeURIComponent(name),{method:'POST',body:html})}catch(e){}};
 /* 획 하나 — 점마다 도착을 확인한다(가운데 한 점만 삼켜도 획이 통째로 없어진다) */
 const draw1=async(sv,pts,pt)=>{
   const n0=((typeof QINK!=='undefined'&&QINK.s)||[]).length;
   const r=sv.getBoundingClientRect(), tries=[];
   tries.push(await fire(sv,'pointerdown',r.left+pts[0],r.top+pts[1],pt||'pen',21));
   for(let i=2;i<pts.length;i+=2)
     tries.push(await fire(sv,'pointermove',r.left+pts[i],r.top+pts[i+1],pt||'pen',21));
   tries.push(await fire(sv,'pointerup',r.left+pts[pts.length-2],r.top+pts[pts.length-1],pt||'pen',21));
   await wait(320);
   return [tries,((QINK.s||[]).length)===n0+1]};
 async function run(){
  const snap={};
  try{
   localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}));
"""


# ← jagwa/gigu/_harness_earth_shell.py:177-184 TAIL · 글자 그대로
TAIL = r"""
   T('콘솔 오류 0',(window.__err||[]).length===0,window.__err);
  }catch(e){T('예외',false,String(e&&e.stack||e))}
  try{await __nativeFetch('/result',{method:'POST',body:R.join(String.fromCharCode(10))})}catch(e){}
 }
 if(document.readyState==='complete')setTimeout(run,700);else window.addEventListener('load',()=>setTimeout(run,700));
})();
</script>"""


# ═════════ earth(_E) — 스텁(과목 earth 박힘) — bio 가 씀 ═════════


# ← jagwa/gigu/_harness_earth.py:22-29 STUB · 글자 그대로 · 이름 바꿈 STUB→STUB_E
STUB_E = """<script>try{localStorage.setItem('subj','earth')}catch(e){}</script>
<script>
window.katex={render:function(){},renderToString:function(s){return s}};window.renderMathInElement=function(){};
window.__err=[];
window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+(e.filename||'').split('/').pop()+':'+e.lineno)});
window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
</script>
"""


# ═════════ physphone(_PP) — 가짜 원격 Remote · route_handler · 서버 serve_PP · INIT_PP · 기기 틀 Pg_PP · fresh · 앱 글 app_src — exam_wrong_mark · physprev · phys_win 이 씀 ═════════


# ← jagwa/moolri/_harness_jagwa_physphone.py:50-50 PHONE · 글자 그대로
PHONE = (390, 844)


# ← jagwa/moolri/_harness_jagwa_physphone.py:51-51 PAD · 글자 그대로
PAD = (820, 1180)


# ← jagwa/moolri/_harness_jagwa_physphone.py:52-52 PC · 글자 그대로
PC = (1440, 900)


# ← jagwa/moolri/_harness_jagwa_physphone.py:55-56 git · 글자 그대로 · 이름 바꿈 git→git_PP
def git_PP(*a):
    return subprocess.run(['git', '-C', _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


# ← jagwa/moolri/_harness_jagwa_physphone.py:59-66 app_src · 글자 그대로 · 이름 바꿈 git→git_PP
def app_src(x):
    """앱 글 — 파일이면 그 파일 · 아니면 genie git 판의 jagwa/index.html"""
    if os.path.isfile(x):
        return open(x, 'rb').read().decode('utf-8')
    b = git_PP('show', x + ':jagwa/index.html')
    if not b:
        raise SystemExit('바탕 앱을 못 읽었다: ' + x)
    return b.decode('utf-8')


# ← jagwa/moolri/_harness_jagwa_physphone.py:70-98 Remote · 글자 그대로 · 이름 바꿈 SPD→SPD_PP
# ── 가짜 원격(기록) — 과목마다 한 파일 · 처음 = studyplandata 로컬 사본 · PUT = 여기 담김(밖으로 안 나감) ──
class Remote:
    def __init__(self):
        self.files, self.puts = {}, []
        self.lock = threading.Lock()

    def path_local(self, repo, path):
        root = NOTES if repo.endswith('/notes') else SPD_PP
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


# ← jagwa/moolri/_harness_jagwa_physphone.py:101-101 REMOTE · 글자 그대로
REMOTE = Remote()


# ← jagwa/moolri/_harness_jagwa_physphone.py:102-102 OKHOST · 글자 그대로
OKHOST = ('http://127.0.0.1',)


# ← jagwa/moolri/_harness_jagwa_physphone.py:105-137 route_handler · 글자 그대로 · 이름 바꿈 VENDOR→VENDOR_PP
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
            f = os.path.join(VENDOR_PP, *m.group(1).split('/'))
            if os.path.isfile(f):
                ct = 'text/css' if f.endswith('.css') else ('font/woff2' if f.endswith('.woff2') else 'application/javascript')
                return route.fulfill(status=200, body=open(f, 'rb').read(), content_type=ct)
            return route.continue_()   # 사본에 없으면 진짜 cdnjs(본 PC 는 열려 있다 · 클라우드는 --vendor 로 다 채운다)
        return route.abort()
    return h


# ← jagwa/moolri/_harness_jagwa_physphone.py:140-140 SERVERS · 글자 그대로
SERVERS = {}


# ← jagwa/moolri/_harness_jagwa_physphone.py:143-177 serve · 글자 그대로 · 이름 바꿈 serve→serve_PP
def serve_PP(tag, src):
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


# ← jagwa/moolri/_harness_jagwa_physphone.py:180-190 INIT · 글자 그대로 · 이름 바꿈 INIT→INIT_PP
INIT_PP = r"""
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


# ← jagwa/moolri/_harness_jagwa_physphone.py:193-296 Pg · 글자 그대로 · 이름 바꿈 Pg→Pg_PP, INIT→INIT_PP, serve→serve_PP
class Pg_PP:
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
        self.ctx.add_init_script(INIT_PP.replace('__SUBJ__', subj).replace('__WHO__', who))
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(90000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append(str(e)[:240]))
        self.port = serve_PP(tag, src)
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


# ← jagwa/moolri/_harness_jagwa_physphone.py:299-304 WK_LONG · 글자 그대로
WK_LONG = r"""([x, y, ty]) => { const t = ty === 'pointerdown' ? document.elementFromPoint(x, y) : (window.__tlT || document.elementFromPoint(x, y));
  if (ty === 'pointerdown') window.__tlT = t;
  t.dispatchEvent(new PointerEvent(ty, {bubbles: true, cancelable: true, composed: true, pointerId: 7, pointerType: 'touch', isPrimary: true,
    clientX: x, clientY: y, button: 0, buttons: ty === 'pointerdown' ? 1 : 0}));
  if (ty === 'pointerup') t.dispatchEvent(new Event('touchend', {bubbles: true, cancelable: true, composed: true}));
  return t.tagName; }"""


# ← jagwa/moolri/_harness_jagwa_physphone.py:306-350 TOOLS · 글자 그대로
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


# ← jagwa/moolri/_harness_jagwa_physphone.py:375-376 fresh · 글자 그대로 · 이름 바꿈 Pg→Pg_PP
def fresh(br, tag, src, subj='phys', dev=PHONE, eng=None, who='하네스', remote=None):
    return Pg_PP(br, eng or br.browser_type.name, tag, src, subj, dev, who=who, remote=remote)   # 엔진 = 받은 브라우저 종류(WebKit 을 CDP 길로 보내지 않는다)


# ═════════ jagwa_uid(_HU) — 같은 출처 서버 Srv · 기기 Dev · INIT_HU · __J 도구 JS_HU · git_HU — search · search_claude · revfix0929 · ggmath · uid_unify · claude e001/e004/e010/p002 가 씀 ═════════


# ← jagwa/_harness_jagwa_uid.py:50-51 git · 글자 그대로 · 이름 바꿈 git→git_HU
def git_HU(repo, *a):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


# ← jagwa/_harness_jagwa_uid.py:67-91 INIT · 글자 그대로 · 이름 바꿈 INIT→INIT_HU
INIT_HU = r"""
(()=>{
  try{localStorage.setItem('subj','__SUBJ__')}catch(e){}
  try{localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}))}catch(e){}
  window.__err=[];window.__PUTS=[];
  window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+(e.lineno||''))});
  window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
  const nf=window.fetch.bind(window);
  window.fetch=async function(url,opt){
    opt=opt||{};const u=String(url);
    const m=/api\.github\.com\/repos\/([^\/]+\/[^\/]+)\/contents\/([^?]+)/.exec(u);
    if(!m){ if(/^https?:/i.test(u)&&u.indexOf(location.origin)!==0&&!/cdnjs|jsdelivr|googleapis|gstatic/.test(u))
              return {ok:false,status:599,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
            return nf(url,opt) }
    const path=decodeURIComponent(m[2]);
    if((opt.method||'GET')==='PUT'){try{const b=JSON.parse(opt.body);window.__PUTS.push({path,text:decodeURIComponent(escape(atob(b.content)))})}catch(e){window.__PUTS.push({path,err:String(e)})}
      return {ok:true,status:200,json:async()=>({content:{sha:'x'}}),text:async()=>''}}
    const r=await nf('/data/'+encodeURI(path),{cache:'no-store'});
    if(!r.ok)return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
    const acc=(opt.headers||{}).Accept||'';
    if(acc.indexOf('raw')>=0)return r;
    return {ok:true,status:200,json:async()=>({sha:r.headers.get('X-Sha')||'sha'}),text:async()=>JSON.stringify({sha:r.headers.get('X-Sha')||'sha'})};
  };
})();
"""


# ← jagwa/_harness_jagwa_uid.py:93-122 JS · 글자 그대로 · 이름 바꿈 JS→JS_HU
JS_HU = r"""
window.__J={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 vis(e){return !!e&&e.isConnected&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0},
 ready(){return typeof DATA!=='undefined'&&DATA.length>0&&(typeof GG_READY==='undefined'||GG_READY)},
 puts(){return (window.__PUTS||[]).map(p=>({path:p.path,len:(p.text||'').length}))},
 lastPut(path){const L=(window.__PUTS||[]).filter(p=>p.path===path);return L.length?L[L.length-1].text:null},
 async sync(){try{await syncRecords(true)}catch(e){return 'ERR '+e}await new Promise(r=>setTimeout(r,400));return (window.__PUTS||[]).length},
 mig(){return window.__JGMIG||0},
 u(){try{return JSON.parse(localStorage.getItem(U_KEY)||'{}')}catch(e){return {}}},
 gone(){try{return JSON.parse(localStorage.getItem(GONE_KEY)||'{}')}catch(e){return {}}},
 stores(keys){const o={};keys.forEach(k=>{const v=SYNC_REF[k]?SYNC_REF[k].g():undefined;o[k]=v?JSON.parse(JSON.stringify(v)):null});return o},
 rows(){return DATA.map(r=>[r[F.NO],r[F.CODE],r[F.OLDU]||'',typeof codeShow==='function'?codeShow(r):''])},
 list(){return [...document.querySelectorAll('#list .item')].filter(__J.vis).map(d=>({uid:d.dataset.uid||'',num:__J.tx(d.querySelector('.num'))}))},
 heat(){return [...document.querySelectorAll('[title]')].filter(e=>/회독|^\S+ /.test(e.title)&&e.onclick).slice(0,4000).map(e=>e.title.split(' ')[0])},
 async card(no){try{closeView()}catch(e){}await new Promise(r=>setTimeout(r,150));await openView(no);await new Promise(r=>setTimeout(r,1600));
   const c=document.getElementById('card');const h=document.getElementById('vT1');
   const img=c&&c.querySelector('img');
   return {head:__J.tx(h),card:__J.tx(c).replace(/\s+/g,' '),bogi:c?[...c.querySelectorAll('.bogi .row .ox button.on')].map(b=>b.closest('.row').dataset.k+b.dataset.v):[],
     tfix:c?c.querySelectorAll('.fx,.fixed').length:0,gg:__J.tx(c&&c.querySelector('.ggwrap')).length,img:!!img,imgOk:img?img.complete&&img.naturalWidth>0:null}},
 heatNos(){const m={};DATA.forEach(r=>m[String(codeShow(r))]=r[F.NO]);return [...document.querySelectorAll('#spec i')].filter(i=>i.title).map(i=>m[i.title.split(' ')[0]]||('?'+i.title.split(' ')[0]))},
 heatCodes(){return [...document.querySelectorAll('#spec i')].filter(i=>i.title).map(i=>i.title.split(' ')[0])},
 memoNos(){try{memoSheet()}catch(e){return 'ERR '+e}const b=document.getElementById('memoSheet');const a=b?[...b.querySelectorAll('.memor')].map(x=>+x.dataset.no):[];if(b)b.remove();return a},
 yearNos(){const ys=[...new Set(DATA.filter(r=>r[F.SRC]==='변리사').map(r=>r[F.YEAR]))].sort();const out=[];const m={};DATA.forEach(r=>m[r[F.CODE]]=r[F.NO]);
   for(const y of ys.slice(-3)){const n0=document.querySelectorAll('.sheet').length;try{yearSheet(y)}catch(e){return 'ERR '+e}const L=[...document.querySelectorAll('.sheet')];const b=L.length>n0?L[L.length-1]:null;
     out.push(b?[...b.querySelectorAll('.histrow .rn')].map(x=>m[x.textContent.trim()]||('?'+x.textContent.trim())):[]);if(b)b.remove()}return out},
 ggHeads(){return [...document.querySelectorAll('#esres [data-ggres] .cd')].map(e=>e.textContent.trim())},
 err(){return (window.__err||[]).slice(0,8)}
};
"""


# ← jagwa/_harness_jagwa_uid.py:125-158 Srv · 글자 그대로 · 이름 바꿈 SPD→SPD_HU
class Srv:
    """같은 출처에서 앱·데이터 폴더·기록을 갈아 끼운다"""
    def __init__(self):
        self.app = b''; self.spd = SPD_HU; self.rec = {}; self.static = {}
        me = self

        class Hh(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *a, **k):
                pass

            def do_GET(self):
                p = urllib.parse.unquote(self.path.split('?')[0])
                if p in ('/', '/app.html'):
                    b = me.app; ct = 'text/html; charset=utf-8'
                elif p.startswith('/data/'):
                    rel = p[6:]
                    if rel in me.rec:
                        b = me.rec[rel]
                    else:
                        f = os.path.join(me.spd, rel.replace('/', os.sep))
                        if not os.path.isfile(f):
                            self.send_response(404); self.end_headers(); return
                        b = open(f, 'rb').read()
                    ct = 'application/octet-stream'
                elif p.lstrip('/') in me.static:   # 앱 옆 파일(motion/…) — 없으면 404
                    b = me.static[p.lstrip('/')]
                    ct = 'text/html; charset=utf-8' if p.endswith('.html') else 'application/json' if p.endswith('.json') else 'application/octet-stream'
                else:
                    self.send_response(404); self.end_headers(); return
                self.send_response(200); self.send_header('Content-Type', ct); self.send_header('Content-Length', str(len(b)))
                self.send_header('X-Sha', hashlib.sha1(b).hexdigest()); self.send_header('Cache-Control', 'no-store'); self.end_headers(); self.wfile.write(b)
        self.srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), Hh); self.srv.daemon_threads = True
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.port = self.srv.server_address[1]


# ← jagwa/_harness_jagwa_uid.py:161-199 Dev · 글자 그대로 · 이름 바꿈 INIT→INIT_HU, JS→JS_HU
class Dev:
    """기기 하나(문맥 하나) — load(앱, 데이터 폴더, 과목) 로 같은 출처에서 다시 연다"""
    def __init__(self, br, eng, phone=False):
        self.eng = eng; self.S = Srv()
        vp = {'width': 390, 'height': 844} if phone else {'width': 1553, 'height': 900}
        self.ctx = br.new_context(viewport=vp, device_scale_factor=1, has_touch=True)
        OK = ('http://127.0.0.1', 'https://cdnjs.cloudflare.com/', 'https://cdn.jsdelivr.net/', 'https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')
        self.ctx.route('**/*', lambda rt: rt.continue_() if rt.request.url.startswith(OK) else rt.abort())
        self.pg = None; self.errs = []

    def load(self, app, spd, subj, rec=None, static=None):
        self.S.app = app; self.S.spd = spd; self.S.rec = dict(rec or {}); self.S.static = dict(static or {})
        if self.pg:
            self.pg.close()
        self.ctx.clear_cookies()
        self.pg = self.ctx.new_page(); self.pg.set_default_timeout(150000)
        self.pg.add_init_script(INIT_HU.replace('__SUBJ__', subj))
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:200]))
        self.pg.goto('http://127.0.0.1:%d/app.html' % self.S.port, wait_until='load')
        self.pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=120000)
        self.pg.evaluate(JS_HU)
        for _ in range(120):
            if self.ev("()=>__J.ready()"):
                break
            self.pg.wait_for_timeout(250)
        self.pg.wait_for_timeout(2500)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass
        try:
            self.S.srv.shutdown()
        except Exception:
            pass


# ═════════ jagwa_search — __S 도구 SJS — revfix0929 · search_claude 가 씀 ═════════


# ← jagwa/_harness_jagwa_search.py:31-59 SJS · 글자 그대로
SJS = r"""
window.__S={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 cnt(){return __S.tx(document.getElementById('cnt'))},
 st(){const b=document.getElementById('esres'),q=document.getElementById('qCnt');
   const rows=b?[...b.querySelectorAll('[data-esq]')]:[];
   return {cnt:__S.cnt(),qcnt:__S.tx(q),esVis:!!b&&!b.classList.contains('hide')&&getComputedStyle(b).display!=='none',
     n:rows.length,rows:rows.slice(0,120).map(d=>({no:+d.dataset.esq,code:__S.tx(d.querySelector('.cd')),lab:__S.tx(d.querySelector('.gl i')),
       chat:(d.textContent||'').indexOf('💬')>=0,marks:d.querySelectorAll('mark').length})),
     note:b?[...b.querySelectorAll('.bplnone')].map(__S.tx):[],nos:(typeof ES_NOS!=='undefined')?ES_NOS.slice():null}},
 byCode(c){const r=DATA.find(x=>String(codeShow(x))===c||x[F.CODE]===c);return r?r[F.NO]:0},
 body(r){return (String(r[F.BODY]||'')+' '+tfixHay(r[F.CODE])).toLowerCase()},
 fields(r){const bg=Array.isArray(r[F.BOGI])?r[F.BOGI]:[],rf=Array.isArray(r[F.REF])?r[F.REF]:[];
   return [['선택지',(r[F.CH]||[]).join(' ')],['보기',bg.map(b=>(b&&b.내용)||'').join(' ')],['해설',String(r[F.SOL]||'')],['해설2',String(r[F.SOL2]||'')],
     ['보기 설명',bg.map(b=>(b&&b.설명)||'').join(' ')],['참고',rf.map(x=>((x&&x.제목)||'')+' '+((x&&x.글)||'')).join(' ')],['코멘트',String(noteOf(r[F.NO])||'')]]},
 /* 칸 하나에만 있는 말 — 그 행 본문·앞 칸·ID·출처에 없고, 그 칸에 있는 6~8 글자 */
 sample(lab){for(const r of DATA){const f=__S.fields(r),k=f.findIndex(x=>x[0]===lab);const t=String(f[k][1]||'');if(t.length<12)continue;
     const pre=__S.body(r)+' '+f.slice(0,k).map(x=>x[1]).join(' ').toLowerCase();
     for(let i=0;i+7<=t.length;i+=3){const w=t.slice(i,i+7);if(/\s|[()\[\]{}.,·…]/.test(w))continue;
       if(!pre.includes(w.toLowerCase()))return {q:w,no:r[F.NO],code:String(codeShow(r))}}}
   return null},
 unitOnly(q){return DATA.filter(r=>{const u=String(unitOf(r[F.NO])||'');if(!u.includes(q))return false;
   const hay=[__S.body(r),...__S.fields(r).map(x=>x[1]),String(codeShow(r)),String(titleOf(r))].join(' ').toLowerCase();return !hay.includes(q.toLowerCase())}).map(r=>r[F.NO])},
 ggN(){return DATA.filter(r=>!isC(r)&&ggOf(GGU(r)).length>0).length},
 ggUnits(){return new Set(DATA.filter(r=>!isC(r)&&ggOf(GGU(r)).length>0).map(r=>String(unitOf(r[F.NO])||''))).size},
 ggBangN(){return DATA.filter(r=>!isC(r)&&ggBangAny(GGU(r))).length},
 rect(sel){const e=typeof sel==='string'?document.querySelector(sel):sel;if(!e)return null;const b=e.getBoundingClientRect();return {x:b.x,y:b.y,w:b.width,h:b.height,cx:b.x+b.width/2,cy:b.y+Math.min(b.height/2,12)}}
};
"""


# ═════════ penfinger(_PF) — INIT_PF · __P 도구 JS_PF · serve_PF · 틀 P — phone_win · penfinger_add1 · add2 가 씀 ═════════


# ← jagwa/gigu/_harness_jagwa_penfinger.py:51-74 INIT · 글자 그대로 · 이름 바꿈 INIT→INIT_PF
INIT_PF = r"""
(()=>{
  try{localStorage.setItem('subj','__SUBJ__')}catch(e){}
  try{localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}))}catch(e){}
  window.__err=[];
  window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+(e.lineno||''))});
  window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
  const nf=window.fetch.bind(window);
  window.fetch=async function(url,opt){
    opt=opt||{};const u=String(url);
    const m=/api\.github\.com\/repos\/([^\/]+\/[^\/]+)\/contents\/([^?]+)/.exec(u);
    if(!m){ if(/^https?:/i.test(u)&&u.indexOf(location.origin)!==0&&!/cdnjs|jsdelivr|googleapis|gstatic/.test(u))
              return {ok:false,status:599,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
            return nf(url,opt) }
    const path=decodeURIComponent(m[2]);
    if((opt.method||'GET')==='PUT')return {ok:true,status:200,json:async()=>({content:{sha:'x'}}),text:async()=>''};
    const r=await nf('/data/'+encodeURI(path),{cache:'no-store'});
    if(!r.ok)return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
    const acc=(opt.headers||{}).Accept||'';
    if(acc.indexOf('raw')>=0)return r;
    return {ok:true,status:200,json:async()=>({sha:r.headers.get('X-Sha')||'sha'}),text:async()=>JSON.stringify({sha:r.headers.get('X-Sha')||'sha'})};
  };
})();
"""


# ← jagwa/gigu/_harness_jagwa_penfinger.py:76-108 JS · 글자 그대로 · 이름 바꿈 JS→JS_PF
JS_PF = r"""
window.__P={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 row:u=>DATA.find(x=>x[F.CODE]===u),
 async open(u){const r=__P.row(u);if(!r)return false;
   try{FL.q=u;FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';if(CUR.KINDS)FL.types=new Set(['G','T','E']);else FL.past=isC(r)?'p':'';draw()}catch(e){}
   await new Promise(res=>setTimeout(res,250));try{await openView(r[F.NO])}catch(e){}await new Promise(res=>setTimeout(res,900));return !!document.getElementById('card')},
 async ans(){const d=document.getElementById('cDet');if(d&&!d.open){d.open=true;await new Promise(res=>setTimeout(res,400))}return !!(d&&d.open)},
 tool(m){try{if(m==='pen')setTool('pen','#16181B',document.querySelector('[data-pen="#16181B"]'));else setTool('view')}catch(e){return 'ERR '+e}
   return {mode:TOOL.mode,penon:document.getElementById('card').classList.contains('penon')}},
 st(){const w=document.getElementById('cardwrap'),c=document.getElementById('card');const sh=document.getElementById('tfxSheet');
   return {top:w?Math.round(w.scrollTop):null,sh:w?w.scrollHeight:null,ch:w?w.clientHeight:null,strokes:(QINK&&QINK.s||[]).length,
     sheet:sh?__P.tx(sh.querySelector('h2')):null,pick:[...c.querySelectorAll('.choices button.pick')].map(b=>+b.dataset.c),
     ox:[...c.querySelectorAll('.bogi .row .ox button.on')].map(b=>b.closest('.row').dataset.k+b.dataset.v),
     vox:[...c.querySelectorAll('.vox.on')].map(b=>b.dataset.vmark),det:!!(document.getElementById('cDet')||{}).open,
     gg:__P.tx(c.querySelector('.ggwrap')).length,mode:TOOL.mode}},
 top(v){const w=document.getElementById('cardwrap');w.scrollTop=v;return Math.round(w.scrollTop)},
 closeSheet(){const s=document.getElementById('tfxSheet');if(s)s.remove();return 1},
 /* 표적 자리 — 그 요소를 창 가운데로 굴린 뒤 안쪽 한 점(fx·fy) · 그 점의 맨 위 요소(덮개면 svg/path)와 덮개를 걷었을 때 밑 요소 */
 at(sel,fx,fy){const c=document.getElementById('card');const e=typeof sel==='string'?c.querySelector(sel):sel;if(!e)return null;
   const w=document.getElementById('cardwrap');e.scrollIntoView({block:'center'});
   const r=e.getBoundingClientRect(),x=Math.round(r.left+Math.min(r.width-4,Math.max(4,r.width*(fx==null?.3:fx)))),y=Math.round(r.top+Math.min(r.height-3,Math.max(3,r.height*(fy==null?.5:fy))));
   const top=document.elementFromPoint(x,y);const ink=c.querySelector('#qink');let under=null;
   if(ink){const k=ink.style.pointerEvents;ink.style.pointerEvents='none';under=document.elementFromPoint(x,y);ink.style.pointerEvents=k}
   const nm=q=>q?(q.id?'#'+q.id:'')+(q.tagName||'').toLowerCase()+'.'+String(q.className&&q.className.baseVal!=null?q.className.baseVal:q.className||'').split(' ').join('.'):null;
   return {x,y,top:nm(top),under:nm(under),inEl:!!under&&(under===e||e.contains(under)),w:Math.round(r.width),h:Math.round(r.height),scroll:Math.round(w.scrollTop)}},
 strokeAt(){const p=[...document.querySelectorAll('#qink path[data-j]')].pop();if(!p)return null;const b=p.getBoundingClientRect();return {x:Math.round(b.left+b.width/2),y:Math.round(b.top+b.height/2)}},
 wrapMid(){const w=document.getElementById('cardwrap').getBoundingClientRect();return {x:Math.round(w.left+w.width*.5),y:Math.round(w.top+w.height*.62)}},
 physDom(){const v=document.getElementById('view');return v?__P.tx(v).replace(/\d+'\d{2}"/g,'').slice(0,4000):''},
 sheets(){return document.querySelectorAll('#tfxSheet').length},
 errs(){return (window.__err||[]).slice(0,10)}
};
"""


# ← jagwa/gigu/_harness_jagwa_penfinger.py:111-143 serve · 글자 그대로 · 이름 바꿈 serve→serve_PF, WORK→WORK_PF
def serve_PF(app_text, subj, tag):
    outdir = os.path.join(WORK_PF, 'srv_' + tag); os.makedirs(outdir, exist_ok=True)
    io.open(os.path.join(outdir, 'app.html'), 'w', encoding='utf-8', newline='').write(app_text)
    spd = os.path.join(SPDROOT, subj)

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=outdir, **k)

        def log_message(self, *a, **k):
            pass

        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            if p.startswith('/data/'):
                rel = p[6:]
                if not rel.startswith(subj + '/'):
                    self.send_response(404); self.end_headers(); return
                f = os.path.join(spd, rel[len(subj) + 1:].replace('/', os.sep))
                if not os.path.isfile(f):
                    self.send_response(404); self.end_headers(); return
                b = open(f, 'rb').read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', str(len(b)))
                self.send_header('X-Sha', hashlib.sha1(b).hexdigest())
                self.end_headers(); self.wfile.write(b); return
            return super().do_GET()

    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


# ← jagwa/gigu/_harness_jagwa_penfinger.py:146-215 P · 글자 그대로 · 이름 바꿈 serve→serve_PF, INIT→INIT_PF, JS→JS_PF
class P:
    """한 판(BASE·NEW) · 한 과목 — 1180×700(아이패드 가로 · 사파리 막대 뺀 높이쯤 — 지학 G48-03 카드가 820 창에선 76px 밖에 안 굴렀다) · 터치 켬"""
    def __init__(self, br, app, subj, tag):
        self.srv, port = serve_PF(app, subj, tag)
        self.ctx = br.new_context(viewport={'width': 1180, 'height': 700}, device_scale_factor=1, has_touch=True)
        OKNET = ('http://127.0.0.1', 'https://cdnjs.cloudflare.com/', 'https://cdn.jsdelivr.net/', 'https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')
        self.ctx.route('**/*', lambda rt: rt.continue_() if rt.request.url.startswith(OKNET) else rt.abort())   # 앱 머리 pdf.js·pdf-lib·KaTeX(CDN)만 연다 · 그 밖 網은 막는다
        self.ctx.add_init_script(INIT_PF.replace('__SUBJ__', subj))
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(120000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:200]))
        self.pg.goto('http://127.0.0.1:%d/app.html' % port, wait_until='load')
        self.pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=90000)
        self.pg.wait_for_timeout(2500)
        self.pg.evaluate(JS_PF)
        self.cdp = self.ctx.new_cdp_session(self.pg)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def wait(self, ms):
        self.pg.wait_for_timeout(ms)

    # ── 손가락(CDP 진짜 터치 · 반지름) ──
    def _t(self, ty, pts, r):
        self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': [{'x': x, 'y': y, 'radiusX': r, 'radiusY': r, 'id': 1} for (x, y) in pts]})

    def fdrag(self, x, y, dx, dy, r=22, n=12):
        self._t('touchStart', [(x, y)], r)
        for i in range(1, n + 1):
            self._t('touchMove', [(x + dx * i / n, y + dy * i / n)], r); self.wait(16)
        for _ in range(3):   # 끝에서 멈춘 뒤 뗀다(움직이며 떼면 크롬이 다음 톡을 삼킨다)
            self._t('touchMove', [(x + dx, y + dy)], r); self.wait(30)
        self._t('touchEnd', [], r); self.wait(250)

    def fhold(self, x, y, ms, r=22):
        self._t('touchStart', [(x, y)], r); self.wait(ms)
        self._t('touchEnd', [], r); self.wait(300)

    # ── 펜(CDP 마우스 이벤트 pointerType pen) ──
    def _p(self, ty, x, y, btn='left', buttons=1):
        self.cdp.send('Input.dispatchMouseEvent', {'type': ty, 'x': x, 'y': y, 'button': btn, 'buttons': buttons, 'clickCount': 1 if ty != 'mouseMoved' else 0,
                                                   'pointerType': 'pen', 'force': 0.5})

    def pdrag(self, x0, y0, x1, y1, n=12):
        self._p('mouseMoved', x0, y0, 'none', 0); self._p('mousePressed', x0, y0)
        for i in range(1, n + 1):
            self._p('mouseMoved', x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.wait(16)
        self._p('mouseReleased', x1, y1, 'left', 0); self.wait(350)

    def phold(self, x, y, ms):
        self._p('mouseMoved', x, y, 'none', 0); self._p('mousePressed', x, y)
        for k in range(int(ms / 50)):   # 2px 안에서 떨린다(사람 손)
            self._p('mouseMoved', x + (1 if k % 2 else 0), y + (1 if k % 3 == 0 else 0)); self.wait(50)
        self._p('mouseReleased', x, y, 'left', 0); self.wait(400)

    def ptap(self, x, y):
        self._p('mouseMoved', x, y, 'none', 0); self._p('mousePressed', x, y); self.wait(40)
        self._p('mouseReleased', x, y, 'left', 0); self.wait(450)

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass
        try:
            self.srv.shutdown()
        except Exception:
            pass


# ═════════ penfinger_add1 — 틀 P2(P 를 이음) · JS2 — penfinger_add2 가 씀 ═════════


# ← jagwa/gigu/_harness_jagwa_penfinger_add1.py:46-82 JS2 · 글자 그대로
JS2 = r"""
Object.assign(window.__P,{
 vis(el){if(!el||!el.isConnected)return false;const s=getComputedStyle(el);if(s.display==='none'||s.visibility==='hidden')return false;
   const r=el.getBoundingClientRect();if(!(r.height>0&&r.width>0))return false;return r.bottom>0&&r.right>0&&r.top<innerHeight&&r.left<innerWidth},
 picks(){const c=document.getElementById('card');return [...c.querySelectorAll('.choices button.pick')].map(b=>({c:+b.dataset.c,vis:__P.vis(b)}))},
 ox(k){const c=document.getElementById('card');const row=[...c.querySelectorAll('.bogi .row')].find(r=>r.dataset.k===k);if(!row)return null;
   return [...row.querySelectorAll('.ox button')].map(b=>({v:b.dataset.v,on:b.classList.contains('on'),vis:__P.vis(b)}))},
 oxRows(){const c=document.getElementById('card');return [...c.querySelectorAll('.bogi .row')].filter(r=>r.querySelector('.ox button')).map(r=>r.dataset.k)},
 sheet(){const s=[...document.querySelectorAll('.sheet')].filter(x=>x.id!=='tfxSheet').pop();return s?{h2:__P.tx(s.querySelector('h2')),vis:__P.vis(s.querySelector('.panel')||s)}:null},
 sheetsAll(){return document.querySelectorAll('.sheet').length},
 closeAll(){document.querySelectorAll('.sheet,#ocrrfz').forEach(x=>x.remove());return 1},
 det(){const d=document.getElementById('cDet');return !!(d&&d.open)},
 detClose(){const d=document.getElementById('cDet');if(d)d.open=false;return 1},
 ink(){const c=document.getElementById('card'),sv=c&&c.querySelector('#qink');if(!sv)return null;const r=sv.getBoundingClientRect();
   return {h:+sv.getAttribute('height'),cardH:c.scrollHeight,bottom:Math.round(r.bottom),penon:c.classList.contains('penon')}},
 lastStroke(){const ps=[...document.querySelectorAll('#qink path[data-j]')];const p=ps.pop();if(!p)return null;const b=p.getBoundingClientRect();
   return {n:ps.length+1,w:Math.round(b.width),h:Math.round(b.height),x:Math.round(b.left),y:Math.round(b.top),on:b.bottom>0&&b.top<innerHeight&&b.right>0&&b.left<innerWidth}},
 /* 참고 그림 — 받아질 때까지 기다린 뒤 창 가운데로 굴리고 가운데 점 */
 async refImg(){const t0=Date.now();let im=null;
   while(Date.now()-t0<15000){im=document.querySelector('#card .rfimg img');if(im&&im.complete&&im.naturalWidth>0)break;await new Promise(r=>setTimeout(r,100))}
   if(!im||!im.naturalWidth)return null;im.scrollIntoView({block:'center'});await new Promise(r=>setTimeout(r,200));
   const r=im.getBoundingClientRect();const x=Math.round(r.left+r.width/2),y=Math.round(r.top+r.height/2);const top=document.elementFromPoint(x,y);
   return {x,y,w:Math.round(r.width),nw:im.naturalWidth,nh:im.naturalHeight,top:top?(top.id||top.tagName.toLowerCase()):null}},
 zoom(){const z=document.getElementById('ocrrfz');if(!z)return null;const im=z.querySelector('img');const r=im.getBoundingClientRect();const s=getComputedStyle(im);
   const nw=im.naturalWidth,nh=im.naturalHeight;let cw=r.width,chh=r.height;
   if(s.objectFit==='contain'&&nw&&nh){const k=Math.min(r.width/nw,r.height/nh);cw=nw*k;chh=nh*k}
   return {vis:__P.vis(z),boxW:Math.round(r.width),boxH:Math.round(r.height),w:Math.round(cw*10)/10,h:Math.round(chh*10)/10,nw,nh,fit:s.objectFit,
     want:Math.round(Math.min(innerWidth*.96,innerHeight*.92*nw/nh)*10)/10,vw:innerWidth,vh:innerHeight}},
 /* 획을 그을 빈 자리 — 그 요소 안에서 밑에 진짜 단추(PEN_HIT)가 없는 점 */
 penSpot(sel){const c=document.getElementById('card');const e=c.querySelector(sel);if(!e)return null;e.scrollIntoView({block:'center'});
   const r=e.getBoundingClientRect(),ink=c.querySelector('#qink');
   for(const fy of [.5,.3,.7])for(const fx of [.2,.35,.5]){const x=Math.round(r.left+r.width*fx),y=Math.round(r.top+r.height*fy);
     if(y<=0||y>=innerHeight-4)continue;const u=ink?underInk(x,y,ink,PEN_HIT):null;if(!u){const t=document.elementFromPoint(x,y);
       return {x,y,top:t?(t.id||t.tagName.toLowerCase()):null,inInk:!!(t&&t.closest&&t.closest('#qink'))}}}
   return null}
});
"""


# ← jagwa/gigu/_harness_jagwa_penfinger_add1.py:85-118 P2 · 글자 그대로 · 이름 바꿈 H.P→P, H.serve→serve_PF, H.INIT→INIT_PF, H.JS→JS_PF
class P2(P):
    """한 판 · 한 과목 · 엔진(chromium · webkit) — 820×1180(아이패드 세로) · 터치 켬"""
    def __init__(self, br, app, subj, tag, engine, vh=1180):
        self.engine = engine
        self.srv, port = serve_PF(app, subj, tag)
        self.ctx = br.new_context(viewport={'width': 820, 'height': vh}, device_scale_factor=1, has_touch=True)
        OKNET = ('http://127.0.0.1', 'https://cdnjs.cloudflare.com/', 'https://cdn.jsdelivr.net/', 'https://fonts.googleapis.com/', 'https://fonts.gstatic.com/',
                 'blob:', 'data:')   # WebKit 은 blob: 그림 요청도 route 를 지난다 — 막으면 참고 그림이 안 뜬다(9/27 첫 판 「그림 못 받음」)
        self.ctx.route('**/*', lambda rt: rt.continue_() if rt.request.url.startswith(OKNET) else rt.abort())
        self.ctx.add_init_script(INIT_PF.replace('__SUBJ__', subj))
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(120000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:200]))
        self.pg.goto('http://127.0.0.1:%d/app.html' % port, wait_until='load')
        self.pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=90000)
        self.pg.wait_for_timeout(2500)
        self.pg.evaluate(JS_PF)
        self.pg.evaluate(JS2)
        self.cdp = self.ctx.new_cdp_session(self.pg) if engine == 'chromium' else None

    def ftap(self, x, y, r=22):
        if self.cdp:
            self._t('touchStart', [(x, y)], r); self.wait(60)
            self._t('touchEnd', [], r)
        else:
            self.pg.touchscreen.tap(x, y)
        self.wait(450)

    def pdown(self, x, y):
        self._p('mouseMoved', x, y, 'none', 0); self._p('mousePressed', x, y)

    def pup(self, x, y):
        self._p('mouseReleased', x, y, 'left', 0)


# ═════════ phone_win(_PW) — serve_PW · 틀 Pg_PW · __W 도구 JS_PW · both(NEW·BASE 한 벌씩) · APPS · git_PW — chipwrap 이 씀 ═════════


# ← jagwa/_harness_jagwa_phone_win.py:56-57 git · 글자 그대로 · 이름 바꿈 git→git_PW
def git_PW(*a):
    return subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


# ← jagwa/_harness_jagwa_phone_win.py:60-99 JS · 글자 그대로 · 이름 바꿈 JS→JS_PW
JS_PW = r"""
window.__W={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 R(e){if(!e)return null;const r=e.getBoundingClientRect();return {x:Math.round(r.left*10)/10,y:Math.round(r.top*10)/10,w:Math.round(r.width*10)/10,h:Math.round(r.height*10)/10}},
 vis(e){return !!e&&e.isConnected&&getComputedStyle(e).display!=='none'&&getComputedStyle(e).visibility!=='hidden'&&e.getBoundingClientRect().height>0},
 hit(e){if(!e)return null;try{e.scrollIntoView({block:'center',inline:'nearest'})}catch(_){}const r=e.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2,at=document.elementFromPoint(cx,cy);
   return {cx:Math.round(cx),cy:Math.round(cy),on:!!at&&(at===e||e.contains(at))&&cx>0&&cy>0&&cx<innerWidth&&cy<innerHeight,at:at?(at.id||at.tagName+'.'+at.className):null}},
 has(n){try{return typeof eval(n)!=='undefined'}catch(e){return false}},
 async openNo(no){try{closeView()}catch(e){}await new Promise(r=>setTimeout(r,200));await openView(no);await new Promise(r=>setTimeout(r,1800));return !document.getElementById('view').classList.contains('hide')},
 noOf(code){const r=DATA.find(x=>x[F.CODE]===code);return r?r[F.NO]:null},
 view(){const v=document.getElementById('view');return {rect:__W.R(v),win:v.classList.contains('win'),z:+v.style.zIndex||0,hide:v.classList.contains('hide'),docw:document.documentElement.scrollWidth,vw:innerWidth}},
 omr(){const o=document.getElementById('omrPad'),w=document.getElementById('wrap');return o?{rect:__W.R(o),ow:o.offsetWidth,tf:o.style.transform,wrap:w?w.clientWidth:null,show:o.classList.contains('show')}:null},
 head(){const fb=document.getElementById('fFoldBtn'),fs=document.getElementById('fSum'),sr=document.querySelector('#esh .erow.esearch'),m=sr&&sr.querySelector(':scope>span.mut'),q=document.getElementById('q');
   const chips=[...document.querySelectorAll('.pwchip')].filter(__W.vis).map(b=>({t:__W.tx(b),r:__W.R(b)}));
   const kids=sr?[...sr.children].filter(__W.vis):[];const top=kids.length?Math.min(...kids.map(k=>k.getBoundingClientRect().top)):null;
   const qFirst=!!(q&&__W.vis(q)&&top!=null&&q.getBoundingClientRect().top<=top+2&&kids[0]===q);
   return {fold:fb?__W.tx(fb):null,foldR:__W.R(fb),fsum:__W.vis(fs),mag:__W.vis(m),q:__W.R(q),sr:__W.R(sr),qFirst,chips,bodyfold:document.body.classList.contains('fold'),
     rows:[...document.querySelectorAll('#esh > *')].filter(__W.vis).map(e=>(e.id||e.className).slice(0,30))}},
 pcHead(){const e=document.getElementById('esh');if(!e)return null;const c=e.cloneNode(true);c.querySelectorAll('.pwchip').forEach(x=>x.remove());
   c.querySelectorAll('#fFold').forEach(x=>x.remove());   /* 폰 전용 접기 줄(PC display:none) — 그 안 글자는 PC 화면에 없다 */return __W.tx(c).replace(/\d+/g,'#').slice(0,1200)},
 side(id){const b=document.getElementById(id)||document.querySelector('[data-shkey="'+id+'"]');const p=b&&b.querySelector(':scope>.panel');
   return b?{float:!!p&&p.classList.contains('float'),x:!!p&&!!p.querySelector('.shx'),rect:__W.R(p),z:+b.style.zIndex||0,
     btn:p?[...p.querySelectorAll('button.btn')].map(x=>({t:__W.tx(x),fs:getComputedStyle(x).fontSize,shlink:x.classList.contains('shlink'),bw:getComputedStyle(x).borderTopWidth,deco:getComputedStyle(x).textDecorationLine})):[],
     close:p?[...p.querySelectorAll('button')].filter(x=>__W.tx(x)==='닫기').length:0}:null},
 list(){const b=document.getElementById('pwl');if(!b)return null;const p=b.querySelector('.panel');
   return {kind:b.dataset.kind,title:__W.tx(b.querySelector('.bplh span')),rect:__W.R(p),rows:[...b.querySelectorAll('.pwr')].map(r=>({id:r.dataset.id,tri:__W.tx(r.querySelector('.tri')),none:r.classList.contains('none')})),
     heads:[...b.querySelectorAll('.pwh')].map(__W.tx),float:!!p&&p.classList.contains('float'),z:+b.style.zIndex||0}},
 rowAt(id){const r=document.querySelector('#pwl .pwr[data-id="'+id+'"]');return r?__W.hit(r):null},
 rowBody(id){const r=document.querySelector('#pwl .pwr[data-id="'+id+'"]');const b=r&&r.nextElementSibling;
   return b?{open:!b.classList.contains('hide'),tri:__W.tx(r.querySelector('.tri')),lines:b.querySelectorAll('.thl').length,imgs:[...b.querySelectorAll('img')].map(i=>({src:i.getAttribute('src'),ok:i.complete&&i.naturalWidth>0})),
     cnt:[...b.querySelectorAll('.pwc')].map(__W.tx),katex:b.querySelectorAll('.katex').length,indent:Math.round(parseFloat(getComputedStyle(b).paddingLeft))}:null},
 async imgOk(){const im=[...document.querySelectorAll('#pwl img')];const r=await Promise.all(im.map(i=>new Promise(res=>{const x=new Image();x.onload=()=>res([i.getAttribute('src'),x.naturalWidth>0]);x.onerror=()=>res([i.getAttribute('src'),false]);x.src=i.src})));return r},
 cntAt(i){const c=document.querySelectorAll('#pwl .pwc')[i||0];return c?__W.hit(c):null},
 sheets(){return [...document.querySelectorAll('.sheet')].filter(__W.vis).map(x=>({id:x.id||x.dataset.shkey||x.className.slice(0,20),z:+x.style.zIndex||0}))},
 cqiAt(no){const b=[...document.querySelectorAll('.sheet .cqi')].find(x=>__W.tx(x.querySelector('b'))===String(no));return b?__W.hit(b):null},
 chip(t){const b=[...document.querySelectorAll('.pwchip')].filter(__W.vis).find(x=>__W.tx(x)===t);return b?__W.hit(b):null},
 at(sel){const e=document.querySelector(sel);return e?__W.hit(e):null},
 errs(){return (window.__err||[]).slice(0,10)}
};
"""


# ← jagwa/_harness_jagwa_phone_win.py:102-133 serve · 글자 그대로 · 이름 바꿈 serve→serve_PW, H.WORK→WORK_PF, H.SPDROOT→SPDROOT
def serve_PW(app_text, subj, tag):
    out = os.path.join(WORK_PF, 'pw_' + tag); os.makedirs(out, exist_ok=True)
    io.open(os.path.join(out, 'app.html'), 'w', encoding='utf-8', newline='').write(app_text)
    spd = os.path.join(SPDROOT, subj)

    class Hh(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=out, **k)

        def log_message(self, *a, **k):
            pass

        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            f = None
            if p.startswith('/img/'):
                f = os.path.join(IMG, p[5:].replace('/', os.sep)); ct = 'image/jpeg'
            elif p.startswith('/data/'):
                rel = p[6:]
                if rel.startswith(subj + '/'):
                    f = os.path.join(spd, rel[len(subj) + 1:].replace('/', os.sep))
                ct = 'application/octet-stream'
            else:
                return super().do_GET()
            if not f or not os.path.isfile(f):
                self.send_response(404); self.end_headers(); return
            b = open(f, 'rb').read()
            self.send_response(200); self.send_header('Content-Type', ct); self.send_header('Content-Length', str(len(b)))
            self.send_header('X-Sha', hashlib.sha1(b).hexdigest()); self.end_headers(); self.wfile.write(b)
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), Hh); srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


# ← jagwa/_harness_jagwa_phone_win.py:136-227 Pg · 글자 그대로 · 이름 바꿈 Pg→Pg_PW, serve→serve_PW, VENDOR→VENDOR_PW, H.INIT→INIT_PF, JS→JS_PW
class Pg_PW:
    def __init__(self, br, eng, app, subj, tag, phone, vp=None):
        """vp(fix1 RF2) = 창 크기를 따로(PC 1440 · iPad 820) — 안 주면 종전(폰 390 · PC 1553) · touch = 폭 1100 이하면 손가락"""
        self.eng, self.phone = eng, phone
        self.touch = phone if vp is None else vp['width'] <= 1100
        self.srv, port = serve_PW(app, subj, tag + '_' + eng + (('_%d' % vp['width']) if vp else ('_ph' if phone else '_pc')))
        vp = vp or ({'width': 390, 'height': 844} if phone else {'width': 1553, 'height': 900})
        self.vpw = vp
        self.ctx = br.new_context(viewport=vp, device_scale_factor=1, has_touch=True, is_mobile=bool(self.touch and eng == 'chromium'))
        OKNET = ('http://127.0.0.1', 'https://cdnjs.cloudflare.com/', 'https://cdn.jsdelivr.net/', 'https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')

        def _rt(rt):
            u = rt.request.url
            m = re.match(r'https://cdnjs\.cloudflare\.com/ajax/libs/(.+)$', u.split('?')[0]) if VENDOR_PW else None
            if m:   # cdnjs 사본(줄 때만)
                f = os.path.join(VENDOR_PW, *m.group(1).split('/'))
                if os.path.isfile(f):
                    return rt.fulfill(path=f, content_type='text/css' if f.endswith('.css') else ('font/woff2' if f.endswith('.woff2') else 'application/javascript'))
                return rt.abort()
            return rt.continue_() if u.startswith(OKNET) else rt.abort()
        self.ctx.route('**/*', _rt)
        self.ctx.add_init_script(INIT_PF.replace('__SUBJ__', subj))
        self.pg = self.ctx.new_page(); self.pg.set_default_timeout(120000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:200]))
        self.pg.goto('http://127.0.0.1:%d/app.html' % port, wait_until='load')
        self.pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=90000)
        self.pg.wait_for_timeout(2500)
        self.pg.evaluate(JS_PW)
        self.cdp = self.ctx.new_cdp_session(self.pg) if eng == 'chromium' else None

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def wait(self, ms):
        self.pg.wait_for_timeout(ms)

    def press(self, at, wait=600):
        """폰 = 손가락(Chromium CDP r22 · WebKit touchscreen.tap) · PC = 마우스"""
        if not at or not at.get('on'):
            return False
        x, y = at['cx'], at['cy']
        if not self.touch:
            self.pg.mouse.click(x, y)
        elif self.cdp:
            pt = {'x': x, 'y': y, 'radiusX': 22, 'radiusY': 22, 'force': 1, 'id': 1}
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [pt]}); self.wait(60)
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        else:
            self.pg.touchscreen.tap(x, y)
        self.wait(wait)
        return True

    def pinch(self, cx, cy, d0, d1, n=10):
        """두 손가락 벌리기(Chromium CDP 만)"""
        if not self.cdp:
            return False
        def pts(d):
            return [{'x': cx - d / 2, 'y': cy, 'radiusX': 22, 'radiusY': 22, 'id': 1}, {'x': cx + d / 2, 'y': cy, 'radiusX': 22, 'radiusY': 22, 'id': 2}]
        self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': pts(d0)})
        for i in range(1, n + 1):
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': pts(d0 + (d1 - d0) * i / n)}); self.wait(20)
        self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); self.wait(800)
        return True

    def drag(self, x0, y0, x1, y1, n=12):
        """≡ 끌기 — 폰 Chromium = CDP 터치 · 그 밖 = 마우스"""
        if self.cdp and self.touch:
            def t(ty, x, y):
                self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': ([] if ty == 'touchEnd' else [{'x': x, 'y': y, 'radiusX': 22, 'radiusY': 22, 'id': 1}])})
            t('touchStart', x0, y0)
            for i in range(1, n + 1):
                t('touchMove', x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.wait(16)
            for _ in range(3):
                t('touchMove', x1, y1); self.wait(30)
            t('touchEnd', x1, y1); self.wait(500)
            return 'cdp-touch'
        m = self.pg.mouse; m.move(x0, y0); m.down()
        for i in range(1, n + 1):
            m.move(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.wait(16)
        m.up(); self.wait(500)
        return 'mouse'

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass
        try:
            self.srv.shutdown()
        except Exception:
            pass


# ← jagwa/_harness_jagwa_phone_win.py:230-241 both · 글자 그대로 · 이름 바꿈 Pg→Pg_PW
def both(br, eng, subj, phone, fn, vp=None, whos=('NEW', 'BASE')):
    """NEW · BASE 한 벌씩(vp · whos = fix1 RF2 — 창 크기 · 앱 고르기)"""
    out = {}
    for who in whos:
        app = APPS[who]
        q = Pg_PW(br, eng, app, subj, who, phone, vp)
        try:
            out[who] = fn(q)
            out[who + '_err'] = q.errs + (q.ev("()=>__W.errs()") or [])
        finally:
            q.close()
    return out


# ← jagwa/_harness_jagwa_phone_win.py:1051-1051 APPS · 글자 그대로
APPS = {}


# ═════════ bio_ocrfix(_BO) — INIT_BO(= INIT_PF 바이트 같음) · __h 도구 JS_HELP · serve_BO — bio_ocrfix_add1 · add2 가 씀 ═════════
INIT_BO = INIT_PF   # ← jagwa/saengmul/_harness_bio_ocrfix.py:48-71 INIT — penfinger INIT 과 바이트 같음(md5 bf8efc01be…) · 두 벌 두지 않고 같은 것을 가리킨다


# ← jagwa/saengmul/_harness_bio_ocrfix.py:114-132 JS_HELP · 글자 그대로
JS_HELP = r"""
window.__h={
 vis:e=>{if(!e)return false;const cs=getComputedStyle(e);const r=e.getBoundingClientRect();return cs.display!=='none'&&cs.visibility!=='hidden'&&r.height>0},
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 row:u=>DATA.find(x=>x[F.CODE]===u),
 show:async u=>{const r=__h.row(u);if(!r)return false;
   try{FL.q=u;FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';if(CUR.KINDS)FL.types=new Set(['G','T','E']);else FL.past=isC(r)?'p':'';draw()}catch(e){}
   await new Promise(res=>setTimeout(res,250));return true},
 open:async u=>{const r=__h.row(u);if(!r)return false;try{await openView(r[F.NO])}catch(e){}await new Promise(res=>setTimeout(res,700));return true},
 card:()=>{const c=document.getElementById('card');const ch=[...c.querySelectorAll('.choices button')].map(b=>__h.tx(b).replace(/^[①②③④⑤⑥⑦⑧]\s*/,'').replace(/✎$/,'').trim());
   const bg={},be={},bv={};c.querySelectorAll('.bogi .row').forEach(el=>{const k=el.dataset.k;const t=el.querySelector('.t');if(!t)return;
     const cl=t.cloneNode(true);cl.querySelectorAll('.tfx,.bexp').forEach(x=>x.remove());bg[k]=__h.tx(cl);
     const e=t.querySelector('.bexp');be[k]=e?__h.tx(e):null;bv[k]=e?__h.vis(e):null});
   return {ch,bg,be,bv}},
 prev:u=>{const it=[...document.querySelectorAll('#list .item')].find(x=>x.dataset.uid===u||__h.tx(x.querySelector('.num'))===u);return it?__h.tx(it.querySelector('.prev')):null},
 sumRect:()=>{const s=document.querySelector('#cDet>summary');if(!s)return null;s.scrollIntoView({block:'center'});const r=s.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]},
 hiddenButVisible:()=>[...document.querySelectorAll('[hidden]')].filter(e=>__h.vis(e)).map(e=>(e.id?'#'+e.id:'')+'.'+String(e.className||'').split(' ').join('.')+' '+__h.tx(e).slice(0,30))
};
"""


# ← jagwa/saengmul/_harness_bio_ocrfix.py:74-111 serve · 글자 그대로 · 이름 바꿈 serve→serve_BO, WORK→WORK_BO
def serve_BO(app_text, qjson, subj, tag):
    outdir = os.path.join(WORK_BO, 'srv_' + tag); os.makedirs(outdir, exist_ok=True)
    io.open(os.path.join(outdir, 'app.html'), 'w', encoding='utf-8', newline='').write(app_text)
    spd = os.path.join(SPDROOT, subj)

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=outdir, **k)

        def log_message(self, *a, **k):
            pass

        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            if p.startswith('/data/'):
                rel = p[6:]
                if not rel.startswith(subj + '/'):
                    self.send_response(404); self.end_headers(); return
                sub = rel[len(subj) + 1:]
                if subj == 'bio' and sub == '문항.json' and qjson:
                    f = qjson
                elif subj == 'bio' and sub.startswith('img/ref') and os.path.isfile(os.path.join(REFDIR, sub[4:])):
                    f = os.path.join(REFDIR, sub[4:])
                else:
                    f = os.path.join(spd, sub.replace('/', os.sep))
                if not os.path.isfile(f):
                    self.send_response(404); self.end_headers(); return
                b = open(f, 'rb').read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', str(len(b)))
                self.send_header('X-Sha', hashlib.sha1(b).hexdigest())
                self.end_headers(); self.wfile.write(b); return
            return super().do_GET()

    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]
