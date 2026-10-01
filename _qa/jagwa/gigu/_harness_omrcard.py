# -*- coding: utf-8 -*-
"""정리 OMR 조각 암기카드 · 모아보기 헤드리스 검산
(2026-09-07 · gigu/_task_jagwa_pan2.md §3)

  좌표표 — 309행 · 중복 0 · 쪽 범위 · 표 안 · 회차 되짚기
  배경   — 캔버스 **아래**, 내 필기 **위**(elementsFromPoint) · 「내 필기 전부 지움」 뒤 배경만 남음
  MC     — 조각이 들어가지 않는다(획 수·바이트 무변)
  모아보기 — 짧게/길게 400ms · 8px 취소 · 길게 = 팝업이고 VNO 가 안 바뀐다
  물리·생물 — 배경 층이 아예 안 생긴다

    PYTHONIOENCODING=utf-8 python _harness_omrcard.py
    PYTHONIOENCODING=utf-8 python _harness_omrcard.py bio
    PYTHONIOENCODING=utf-8 python _harness_omrcard.py phys
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import http.server, os, socketserver, subprocess, sys, threading, hashlib, shutil, urllib.parse, json, io

GENIE = _roots.genie()
SRC = os.path.join(GENIE, 'jagwa', 'index.html')
SPDROOT = _roots.spd()
GIGU = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.environ.get('TEMP', '.'), 'omrh'); os.makedirs(OUT, exist_ok=True)

ARG = sys.argv[1:]
SUBJ = 'bio' if 'bio' in ARG else ('phys' if 'phys' in ARG else 'earth')
SPD = os.path.join(SPDROOT, SUBJ)

STUB = """<script>try{localStorage.setItem('subj','__SUBJ__')}catch(e){}</script>
<script>
window.katex={render:function(){},renderToString:function(s){return s}};window.renderMathInElement=function(){};
window.__err=[];
window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+(e.filename||'').split('/').pop()+':'+e.lineno)});
window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
</script>
"""

TESTS = r"""<script>
(function(){
 const R=[]; const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+(c?'':' | '+JSON.stringify(i===undefined?null:i)));
 const CARD=(typeof CARD_LAYER!=='undefined')&&CARD_LAYER;
 const __nativeFetch=window.fetch.bind(window);
 window.fetch=async function(url,opt){
  opt=opt||{};const u=String(url);
  const m=/api\.github\.com\/repos\/([^\/]+\/[^\/]+)\/contents\/([^?]+)/.exec(u);
  if(!m){ if(/api\.github\.com\/repos\/zzikkaplan\/notes/.test(u))return {ok:true,status:200,json:async()=>({name:'notes'}),text:async()=>''}; return __nativeFetch(url,opt); }
  const path=decodeURIComponent(m[2]);
  if(m[1]==='zzikkaplan/notes')return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
  if((opt.method||'GET')==='PUT')return {ok:true,status:200,json:async()=>({content:{sha:'x'}}),text:async()=>''};
  const r=await __nativeFetch('/data/'+encodeURI(path),{cache:'no-store'});
  if(!r.ok)return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
  const acc=(opt.headers||{}).Accept||'';
  if(acc.indexOf('raw')>=0)return r;
  return {ok:true,status:200,json:async()=>({sha:'sha'}),text:async()=>JSON.stringify({sha:'sha'})};
 };
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 setInterval(()=>{try{__nativeFetch('/partial',{method:'POST',body:R.join(String.fromCharCode(10))+String.fromCharCode(10)+'(err) '+JSON.stringify(window.__err||[])})}catch(e){}},3000);
 const grp=async(name,fn)=>{try{await fn()}catch(e){T(name+' 묶음 예외',false,String(e&&e.stack||e).slice(0,300))}};
 let hit=null;
 const hitOn=()=>{if(hit)return;hit=document.createElement('style');
   hit.textContent='.mccv canvas{pointer-events:auto!important}';document.head.appendChild(hit)};
 const hitOff=()=>{if(hit){hit.remove();hit=null}};
 const PE=(el,t,x,y,id)=>el.dispatchEvent(new PointerEvent(t,{clientX:x,clientY:y,pointerId:id||3,pointerType:'mouse',bubbles:true,cancelable:true,isPrimary:true}));

 async function run(){
  try{
   localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}));
   if(CARD){await loadEarthData();}
   draw(); await wait(120);
   T('O-0 떴다 · 데이터',DATA.length>0,[SUBJ_ID,DATA.length,CARD]);

   /* ═══ 물리·생물 — 조각이 아예 없어야 한다 ═══ */
   if(!CARD||!CUR.JOGAK_PATH){
     await grp('O-N', async()=>{
       T('O-N 좌표표 없음(JOGAK 비었거나 함수 자체가 없다)',typeof JOGAK==='undefined'||!jogakAny(),typeof JOGAK==='undefined'?'없음':Object.keys(JOGAK).length);
       const r=DATA[0];
       if(typeof mcardWin==='function'){mcardWin(r[F.NO]);await wait(250);
         T('O-N 카드 창에 배경 층이 안 생긴다',$$('.mccv canvas.bg').length===0,$$('.mccv canvas.bg').length);
         T('O-N 「▣ 조각 보기」 토글이 없다',!$('#mcJg'));
         T('O-N 「전체 지움」 글자 그대로',($('#mcClear')||{}).textContent==='전체 지움',($('#mcClear')||{}).textContent);
         if(MCW){MCW.remove();MCW=null}}
       mcardSheet(r[F.SUB],r[F.SUB]);await wait(250);
       T('O-N 모아보기 머리줄(.mcbar)이 없다 — 종전 그대로',$$('.mcbar').length===0);
       T('O-N 「순서」 칩은 그대로 있다',!!$('#mcSort'));
       document.querySelectorAll('.sheet').forEach(x=>x.remove());
     });
     T('O-0 콘솔 오류 0',(window.__err||[]).length===0,window.__err);
     try{await __nativeFetch('/result',{method:'POST',body:R.join(String.fromCharCode(10))})}catch(e){}
     return;
   }

   /* ═══ 좌표표 ═══ */
   await grp('O-J', async()=>{
     T('O-J 좌표표 309행 적재',Object.keys(JOGAK).length===309,Object.keys(JOGAK).length);
     T('O-J 쪽 1~3 · x0<x1 · y0<y1 전건',Object.values(JOGAK).every(v=>v.p>=1&&v.p<=3&&v.r[0]<v.r[2]&&v.r[1]<v.r[3]));
     T('O-J 표 안(y0 ≥ 25.3 · y1 ≤ 472.3)',Object.values(JOGAK).every(v=>v.r[1]>=25.29&&v.r[3]<=472.3));
     const bad=[];
     for(const k in JOGAK){const [h,n]=k.split('-').map(Number);const y=25.3+41.85*(n-1);
       if(Math.abs(JOGAK[k].r[1]-y)>0.06)bad.push(k)}
     T('O-J 문번 → y0 = 25.3 + 41.85×(문번−1) 전건',!bad.length,bad.slice(0,4));
     T('O-J 32회 9행 · 32-10 없음 · 63회 0행',
       Object.keys(JOGAK).filter(k=>k.startsWith('32-')).length===9&&!JOGAK['32-10']
       &&!Object.keys(JOGAK).some(k=>k.startsWith('63-')));
     const G=DATA.filter(r=>kindOf(r)==='G');
     const have=G.filter(r=>jogakOf(r)).length, miss=G.filter(r=>!jogakOf(r));
     T('O-J 기출 319 중 309가 짝 · 못 찾은 10은 전부 63회',
       G.length===319&&have===309&&miss.length===10&&miss.every(r=>+r[F.ROUND]===63),
       [G.length,have,miss.length,[...new Set(miss.map(r=>r[F.ROUND]))]]);
   });

   /* ═══ 카드 창 배경 ═══ */
   let NO=0;
   await grp('O-C', async()=>{
     const r=DATA.find(x=>jogakOf(x)); NO=r[F.NO];
     await openView(NO); await wait(200);
     await del('kv','mcard'); MC={};
     mcardWin(NO); await wait(400);
     /* omr2 는 9.5MB — 처음 한 번은 받아서 pdf.js 로 여는 데 시간이 걸린다. 캔버스가 실제로 커질 때까지 기다린다 */
     for(let i=0;i<120;i++){const c=$('.mccv canvas.bg');if(c&&(c.width!==300||c.height!==150))break;await wait(250)}
     const bg=$('.mccv canvas.bg'), fg=$('#mcc');
     /* ⚠ 빈 캔버스 기본값이 300×150 이라 크기만 보면 안 그려져도 통과한다 — 조각 비율까지 본다 */
     const AR=jogakAR(jogakOf(r));
     T('O-C 배경 층이 생겼다 · 조각 비율로 그려졌다 · 감춰지지 않았다',
       !!bg&&bg.width>50&&bg.height>30&&Math.abs(bg.width/bg.height-AR)<0.02&&getComputedStyle(bg).display!=='none',
       [bg&&bg.width,bg&&bg.height,bg&&(bg.width/bg.height),AR,$('#mcSt')&&$('#mcSt').textContent]);
     T('O-C 「▣ 조각 보기」 토글이 붙었다 · 켜짐',!!$('#mcJg')&&$('#mcJg').classList.contains('on'));
     T('O-C 「내 필기 전부 지움」 으로 이름이 바뀌었다',$('#mcClear').textContent==='내 필기 전부 지움',$('#mcClear').textContent);
     /* 쌓임 — 배경이 아래, 내 필기가 위 */
     const rc=fg.getBoundingClientRect();
     hitOn(); const els=document.elementsFromPoint(rc.left+rc.width/2,rc.top+rc.height/2); hitOff();
     const iF=els.indexOf(fg), iB=els.indexOf(bg);
     T('O-C 쌓임 — 내 필기가 위, 배경이 아래',iF>=0&&iB>=0&&iF<iB,[iF,iB,els.slice(0,4).map(e=>(e.tagName||'')+'.'+(e.className||''))]);
     T('O-C 캔버스 세로비가 조각 비율에 맞춰졌다',
       Math.abs(($('.mccv').clientWidth/$('.mccv').clientHeight)-jogakAR(jogakOf(r)))<0.35,
       [$('.mccv').clientWidth,$('.mccv').clientHeight,jogakAR(jogakOf(r))]);
     /* 획 하나 그리고 — MC 에 조각이 안 들어가는지 */
     const before=JSON.stringify(MC).length;
     await zzDraw(fg);
     T('O-C 획 하나 = MC 에 1획 · 조각은 안 들어간다(획 좌표는 1/1000 정수뿐)',
       MC[NO]&&MC[NO].s.length===1&&MC[NO].s[0].p.every(v=>Number.isInteger(v)&&v>=0&&v<=1000),
       MC[NO]&&MC[NO].s[0].p.slice(0,6));
     T('O-C MC 바이트가 조각 크기만큼 늘지 않았다(1KB 미만 증가)',JSON.stringify(MC).length-before<1024,JSON.stringify(MC).length-before);
     /* 「내 필기 전부 지움」 — 배경은 남는다 */
     const _c=window.confirm; window.confirm=()=>true;
     $('#mcClear').click(); await wait(300); window.confirm=_c;
     T('O-C 「내 필기 전부 지움」 → MC[no] 만 사라지고 배경은 남는다',
       !MC[NO]&&!!$('.mccv canvas.bg')&&$('.mccv canvas.bg').width>50,[!!MC[NO],!!$('.mccv canvas.bg')]);
     /* 토글 끄면 배경만 감춰진다 */
     $('#mcJg').click(); await wait(150);
     T('O-C 토글 끔 → 배경 감춤 · localStorage 기기 값',getComputedStyle($('.mccv canvas.bg')).display==='none'&&localStorage.getItem('jagwa.jogak')==='0');
     $('#mcJg').click(); await wait(400);
     T('O-C 다시 켬 → 배경 돌아옴',getComputedStyle($('.mccv canvas.bg')).display!=='none'&&localStorage.getItem('jagwa.jogak')==='1');
     if(MCW){MCW.remove();MCW=null}
   });

   /* ═══ 모아보기 ═══ */
   await grp('O-D', async()=>{
     const r=rec(NO);
     mcardSheet(r[F.SUB],r[F.SUB]); await wait(2500);
     T('O-D 머리줄에 단원별/회차별 토글 · 칸 슬라이더 · 내 카드 수',
       $$('.mcbar [data-m]').length===2&&!!$('#mcW')&&/내 카드 \d+장 · 합계/.test($('.mcbar .n').textContent),$('.mcbar .n')&&$('.mcbar .n').textContent);
     T('O-D 칸에 조각 배경이 깔린다',$$('.mcard .k canvas.bg').length>0,$$('.mcard .k canvas.bg').length);
     T('O-D 라벨 = 「25-62-9」(연도-회차-문번 · 판 2 add2 로 「N회 M번」에서 바뀌었다)',/^\d{2}-\d{2,3}-\d{1,2}$/.test($('.mcard .t b').textContent),$('.mcard .t b').textContent);
     /* 회차별 정렬 */
     $('.mcbar [data-m="round"]').click(); await wait(600);
     const lab=$$('.mcard .t b').map(x=>x.textContent);
     const nums=lab.map(t=>{const m=/^\d{2}-(\d{2,3})-(\d{1,2})$/.exec(t);return m?[+m[1],+m[2]]:[0,0]});
     /* 판 2 add2 — 회차별은 회차 **내림차순** → 문번 오름차순(종이 꼴 규약). 종전 판은 회차 오름차순이었다. */
     let ok=true;for(let i=1;i<nums.length;i++)if(nums[i-1][0]<nums[i][0]||(nums[i-1][0]===nums[i][0]&&nums[i-1][1]>nums[i][1]))ok=false;
     T('O-D 회차별 = 회차 내림차순 → 문번 순',ok&&nums.length>1,lab.slice(0,4));
     T('O-D 토글이 기기 값으로 남는다',localStorage.getItem('jagwa.mcmode')==='round');
     $('.mcbar [data-m="unit"]').click(); await wait(600);
     /* 짧게 = 크게 보기 · VNO 무변 */
     /* ⚠ 판 2 add2 로 칸 차례가 최신순으로 바뀌어 첫 칸이 「조각도 필기도 없는 칸」일 수 있다.
        그 칸을 짧게 누르면 판 2 규약대로 문항이 열린다(정상) — 여기서 재려는 것은 「크게 보기」다.
        그래서 **조각이 있는 칸**을 골라 잰다(고친 자리 · add2 §3). */
     const v0=VNO, el=$$('.mcard').find(x=>jogakOf(rec(+x.dataset.no)))||$('.mcard'), rc=el.getBoundingClientRect();
     PE(el,'pointerdown',rc.left+10,rc.top+10); await wait(120);
     PE(el,'pointerup',rc.left+10,rc.top+10); el.click(); await wait(300);
     T('O-D 짧게(≤400ms) = 크게 보기 · VNO 무변 · 팝업 아님',VNO===v0&&!$('#mcPop')&&$$('.mccv.big').length===1,[VNO,v0,!!$('#mcPop')]);
     document.querySelectorAll('.sheet').forEach(x=>x.remove());
     mcardSheet(r[F.SUB],r[F.SUB]); await wait(2000);
     /* 길게 = 팝업 · VNO 무변 */
     const el2=$('.mcard'), rc2=el2.getBoundingClientRect(), v1=VNO;
     PE(el2,'pointerdown',rc2.left+10,rc2.top+10); await wait(600);
     PE(el2,'pointerup',rc2.left+10,rc2.top+10); await wait(200);
     T('O-D 길게(≥400ms) = 문항 팝업이 뜨고 **VNO 가 안 바뀐다**',!!$('#mcPop')&&VNO===v1,[!!$('#mcPop'),VNO,v1]);
     T('O-D 팝업에 「이 문항으로 가기」·「카드 열어 쓰기」',!!$('#mpGo')&&!!$('#mpCard'));
     $('#mpX').click(); await wait(100);
     /* 8px 넘게 움직이면 취소 */
     const el3=$('.mcard'), rc3=el3.getBoundingClientRect(), v2=VNO;
     PE(el3,'pointerdown',rc3.left+10,rc3.top+10); await wait(80);
     PE(el3,'pointermove',rc3.left+40,rc3.top+10); await wait(600);
     PE(el3,'pointerup',rc3.left+40,rc3.top+10); await wait(200);
     T('O-D 누르는 사이 8px 넘게 움직이면 취소 — 팝업도 안 뜨고 VNO 무변',!$('#mcPop')&&VNO===v2,[!!$('#mcPop'),VNO,v2]);
     document.querySelectorAll('.sheet').forEach(x=>x.remove());
   });

   T('O-0 콘솔 오류 0',(window.__err||[]).length===0,window.__err);
  }catch(e){T('예외',false,String(e&&e.stack||e))}
  try{await __nativeFetch('/result',{method:'POST',body:R.join(String.fromCharCode(10))})}catch(e){}
 }
 /* 캔버스에 한 획 긋기 */
 async function zzDraw(cv){
   const rc=cv.getBoundingClientRect();
   /* A-6(a) 9/30 — 카드 필기는 **펜만**이다(moolri/_task_jagwa_pen_touch2 §6-5 갈래 표 「3 암기카드 mcardWin — pen 필기 · mouse 조작」 · c62b2b2 · mcardWin 「if(e.pointerType!=='pen')return」) → 펜으로 긋는다 */
   const P=(t,x,y)=>cv.dispatchEvent(new PointerEvent(t,{clientX:x,clientY:y,pointerId:9,pointerType:'pen',bubbles:true,cancelable:true,isPrimary:true}));
   P('pointerdown',rc.left+rc.width*0.2,rc.top+rc.height*0.3);
   await wait(20);P('pointermove',rc.left+rc.width*0.5,rc.top+rc.height*0.5);
   await wait(20);P('pointermove',rc.left+rc.width*0.7,rc.top+rc.height*0.4);
   await wait(20);P('pointerup',rc.left+rc.width*0.7,rc.top+rc.height*0.4);
   await wait(250);
 }
 if(document.readyState==='complete')setTimeout(run,600);else window.addEventListener('load',()=>setTimeout(run,600));
})();
</script>"""


def main():
    html = open(SRC, encoding='utf-8', newline='').read()
    html = html.replace('<script defer src="https://cdnjs', '<script defer data-off="https://cdnjs')
    html = html.replace('<link rel="stylesheet" href="https://cdnjs', '<link rel="off" href="https://cdnjs')
    html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js',
                        STUB.replace('__SUBJ__', SUBJ) + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    html = html.replace('</body>', TESTS + '</body>', 1)
    open(os.path.join(OUT, 'app.html'), 'w', encoding='utf-8', newline='').write(html)

    done = threading.Event(); box = {}

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=OUT, **k)
        def log_message(self, *a, **k): pass
        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            if p.startswith('/data/'):
                rel, pre = p[6:], SUBJ + '/'
                if not rel.startswith(pre): self.send_response(404); self.end_headers(); return
                f = os.path.join(SPD, rel[len(pre):].replace('/', os.sep))
                if not os.path.isfile(f): self.send_response(404); self.end_headers(); return
                b = open(f, 'rb').read()
                self.send_response(200); self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', str(len(b))); self.send_header('X-Sha', hashlib.sha1(b).hexdigest())
                self.end_headers(); self.wfile.write(b); return
            return super().do_GET()

        def do_POST(self):
            n = int(self.headers.get('Content-Length') or 0)
            body = self.rfile.read(n).decode('utf-8', 'replace'); self.send_response(204); self.end_headers()
            if self.path.startswith('/partial'): box['partial'] = body; return
            box['txt'] = body; done.set()

    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    prof = os.path.join(OUT, 'prof'); shutil.rmtree(prof, ignore_errors=True)
    p = subprocess.Popen([chrome, '--headless=new', '--disable-gpu', '--no-first-run', '--user-data-dir=' + prof,
                          '--window-size=1400,900', 'http://127.0.0.1:%d/app.html' % port],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    import time as _t; _t0 = _t.time()
    got = done.wait(int(os.environ.get('HARNESS_WAIT', '420'))); p.terminate(); print('elapsed %.0fs' % (_t.time() - _t0))
    try: p.wait(10)
    except Exception: p.kill()
    srv.shutdown()
    if not got:
        print('결과 없음 — 시간 안에 검사가 끝나지 않았다 · 마지막 중간 결과:'); print(box.get('partial', '(없음)')); sys.exit(1)
    lines = [ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()]

    def T2(name, cond, info=''):
        lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))

    s = open(SRC, encoding='utf-8').read()
    ix = lambda t: s.find(t)
    # A-6(a) 9/30 — 카드 층 블록 문이 if(CARD_LAYER){ → if(SHELL){ 로 바뀌었다(_task_jagwa_shell_bio_phys §A · c9faff2) — 그 블록(/*EARTH:js*/ 바로 뒤)을 잡는다
    blk = s.find('\nif(SHELL){\n', ix('/*EARTH:js*/'))
    T2('O-P 조각 코드는 전부 카드 층 블록(9/21 부터 if(SHELL)) 안 · 물리 층에서도 보이게 var 식으로 둔다(블록 안 async function 은 전역에 안 올라온다)',
       blk >= 0 and all(ix(k) > blk for k in ['var JOGAK=', 'var loadJogak=async function(', 'var omrDoc=async function(', 'var jogakPaint=async function(']))
    T2('O-P 새 동작은 좌표표가 있을 때만 — typeof 가드까지 걸어 물리에서 함수가 없어도 안 죽는다',
       "const JG=(typeof jogakAny==='function')&&jogakAny();" in s
       and "const _jg=(typeof jogakOf==='function')?jogakOf(r):null;" in s and 'if(_jg){' in s)
    T2('O-P mcard 저장 꼴·상한 무변', 'const MC_MAX=20000;' in s and "const saveMC=()=>put('kv','mcard',MC);" in s)
    T2('O-P 조각을 MC 에 넣는 코드 0', 'MC[no]=card' in s and 'jogak' not in s[ix('const end=async()=>{ if(!live)return;'):ix('const end=async()=>{ if(!live)return;') + 600])
    T2('O-P 백틱 짝', s.count('`') % 2 == 0)
    if SUBJ == 'earth':
        J = json.loads(io.open(os.path.join(SPD, '조각.json'), encoding='utf-8').read())
        T2('O-P 조각.json 309행 · src·md5 적힘', len(J['cells']) == 309 and J.get('src') and J.get('md5'), [len(J['cells']), J.get('md5')])
        pdf = os.path.join(SPD, 'omr2.pdf')
        T2('O-P omr2.pdf 가 비공개 저장소에 있다 · md5 f294dcb24b',
           os.path.isfile(pdf) and hashlib.md5(open(pdf, 'rb').read()).hexdigest()[:10] == 'f294dcb24b')
        T2('O-P 공개 저장소(genie)에는 PDF 가 없다',
           not any(f.lower().endswith('.pdf') for _, _, fs in os.walk(os.path.join(GENIE, 'jagwa')) for f in fs))
    npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
    for x in lines: print(x)
    print('\n== 조각카드(%s) %d PASS / %d FAIL / %d항 ==' % (SUBJ, npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
