# -*- coding: utf-8 -*-
"""잉크 덧층 쌓임 순서 · 기기 펜슬 설정 · 손바닥 거르기 헤드리스 검산
(2026-09-07 · gigu/_task_jagwa_ink_guard_add1.md §3)

_harness_ink.py 의 통(가짜 GitHub · 로컬 studyplandata · 헤드리스 크롬)을 그대로 쓴다.

  ① 잉크가 있는 쪽에서 타일 **위**에 획이 오는지(배율을 바꿔 타일 버킷이 갈릴 때도)
  ② 타일끼리 순서가 유지되는지(지금 배율 층 2 가 옛 층 1 위 · 둘 다 잉크 아래)
  ③ 서브노트(#sover .sink)도 같이 보이는지
  ④ 과목 셋 pencil 값이 엇갈릴 때 false 로 통일되는지
  ⑤ 펜 다운 뒤 touch 접점이 들어와도 스트로크가 안 끊기는지
  ⑥ touch 둘이면 여전히 핀치인지

쌓임 순서는 elementsFromPoint 로 잰다 — 잉크 SVG 와 타일 캔버스에 잠깐 pointer-events:auto 를
주고(쌓임에는 영향 없다) 같은 점에서 누가 위에 오는지 본다. 잰 뒤 원래대로 되돌린다.

    PYTHONIOENCODING=utf-8 python _harness_ink_z.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import http.server, os, socketserver, subprocess, sys, threading, hashlib, shutil, urllib.parse

GENIE = _roots.genie()
SRC = os.path.join(GENIE, 'jagwa', 'index.html')
SPD = os.path.join(_roots.spd(), 'earth')
GIGU = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.environ.get('TEMP', '.'), 'inkzh'); os.makedirs(OUT, exist_ok=True)
APP = os.path.join(OUT, 'app.html')

STUB = """<script>try{localStorage.setItem('subj','earth')}catch(e){}</script>
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
 const __nativeFetch=window.fetch.bind(window);
 window.fetch=async function(url,opt){
  opt=opt||{};const u=String(url);
  const m=/api\.github\.com\/repos\/([^\/]+\/[^\/]+)\/contents\/([^?]+)/.exec(u);
  if(!m){ if(/api\.github\.com\/repos\/zzikkaplan\/notes/.test(u))return {ok:true,status:200,json:async()=>({name:'notes'}),text:async()=>''}; return __nativeFetch(url,opt); }
  const path=decodeURIComponent(m[2]);
  if(m[1]==='zzikkaplan/notes'){const r=await __nativeFetch('/notes/'+encodeURI(path),{cache:'no-store'});return r.ok?r:{ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)}}
  if((opt.method||'GET')==='PUT')return {ok:true,status:200,json:async()=>({content:{sha:'x'}}),text:async()=>''};
  const r=await __nativeFetch('/data/'+encodeURI(path),{cache:'no-store'});
  if(!r.ok)return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
  const acc=(opt.headers||{}).Accept||'';
  if(acc.indexOf('raw')>=0)return r;
  return {ok:true,status:200,json:async()=>({sha:'sha'}),text:async()=>JSON.stringify({sha:'sha'})};
 };
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 setInterval(()=>{try{__nativeFetch('/partial',{method:'POST',body:R.join(String.fromCharCode(10))+String.fromCharCode(10)+'(err) '+JSON.stringify(window.__err||[])})}catch(e){}},3000);

 /* ── 쌓임 순서 재기 — 잠깐만 잡히게 하고 되돌린다 ── */
 let hitCSS=null;
 function hitOn(){ if(hitCSS)return; hitCSS=document.createElement('style');
   hitCSS.textContent='#bkover .bkink,#bkover .bkink *,#sover .sink,#sover .sink *,#bktiles canvas,#bktiles .ztl,#stiles canvas,#stiles .ztl{pointer-events:auto!important}';
   document.head.appendChild(hitCSS); }
 function hitOff(){ if(hitCSS){hitCSS.remove();hitCSS=null} }
 /* 쪽 좌표 → 화면 좌표 (덧층의 쪽 상자를 그대로 쓴다) */
 function ptOf(pel,pw,ph,x,y){const r=pel.getBoundingClientRect();
   return {x:r.left+(x/pw)*r.width, y:r.top+(y/ph)*r.height}; }
 /* 잴 점을 화면 한가운데로 끌어온다 — 화면 밖이면 elementsFromPoint 가 빈 배열을 준다 */
 async function center(Z,pg,x,y){const vp=$(Z.vp),r=vp.getBoundingClientRect();
   Z.X=r.width/2-(pg.x+x)*Z.S; Z.Y=r.height/2-(pg.y+y)*Z.S; if(Z.clamp)Z.clamp(); zApply(Z); await wait(200); }
 /* 타일이 그려질 때까지 기다린다(최대 6초) */
 async function tilesReady(sel){for(let i=0;i<60;i++){if($$(sel+' canvas').length)return true;await wait(100)}return false}
 function stackAt(cx,cy){ hitOn();
   const els=document.elementsFromPoint(cx,cy);   /* 위에 있는 것부터 */
   hitOff();
   const idx=(f)=>{for(let i=0;i<els.length;i++)if(f(els[i]))return i;return -1};
   return {
     ink:  idx(e=>e.closest&&e.closest('.bkink,.sink')),
     tile: idx(e=>e.tagName==='CANVAS'&&e.closest('#bktiles,#stiles')),
     names:els.slice(0,6).map(e=>(e.tagName||'')+'.'+((e.getAttribute&&e.getAttribute('class'))||'')+'#'+(e.id||''))
   }; }

 /* 묶음 하나가 죽어도 나머지는 돈다 — 한 묶음의 예외가 검사 전체를 삼키면 안 된다 */
 const grp=async(name,fn)=>{try{await fn()}catch(e){T(name+' 묶음 예외',false,String(e&&e.stack||e).slice(0,300))}};

 async function run(){
  try{
   localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}));
   for(let __i=0;__i<300&&(typeof db==='undefined'||!db);__i++)await wait(100);   /* ★ 2026-10-08 (_task_jagwa_phys_win) 고정 대기(load+600ms) 대신 IndexedDB(db)가 설 때까지(30 초 한도) — 짐이 크면 600ms 안에 안 열려 「db 없음」 예외(1 단계 셋 다) · 같은 판을 짐 적을 때 돌리면 정상(00:25 진단) */
   await loadEarthData(); draw(); await wait(50);
   T('Z-0 지학 카드 층으로 떴다',CARD_LAYER===true&&db.name==='earth1'&&DATA.length>0,[CARD_LAYER,db.name,DATA.length]);

   /* ═══ ④ 기기 하나에 하나인 pencil ═══ */
   await grp('Z-4', async()=>{
   /* A-6(a) 9/30 — 펜슬 스위치 기계(pencilLoad·pencilSet·pencilOf·pencilUnify·PENCIL_KEY)를 걷었다(moolri/_task_jagwa_pen_touch2 §1 · 수행 결과 §6-4 「부르는 자리가 0이 되어 기계째 32줄 걷었다 ·
      헤드리스에서 셋 다 undefined」 · c62b2b2 · _decisions 2026-09-13) — 필기는 언제나 펜만. 아래 옛 여섯 줄은 그 기계가 있을 때만 잰다(지우지 않는다 · 지금 판에서는 안 돈다) */
   T('Z-4 펜슬 스위치 기계를 걷었다 — pencilUnify·pencilSet·pencilLoad·pencilOf 가 undefined',typeof pencilUnify==='undefined'&&typeof pencilSet==='undefined'&&typeof pencilLoad==='undefined'&&typeof pencilOf==='undefined',[typeof pencilUnify,typeof pencilSet,typeof pencilLoad,typeof pencilOf]);
   if(typeof pencilUnify!=='function')return;
   T('Z-4 pencilUnify: 값이 다 같으면 그 값',typeof pencilUnify==='function'&&pencilUnify([true,true])===true&&pencilUnify([false,false])===false);
   T('Z-4 pencilUnify: 엇갈리면 false(푸는 쪽)',pencilUnify([true,false])===false&&pencilUnify([false,true,true])===false);
   T('Z-4 pencilUnify: 값이 하나도 없으면 false',pencilUnify([])===false&&pencilUnify([undefined,null])===false);
   T('Z-4 시동 뒤 localStorage 에 기기 값이 있고 SET.pencil 과 같다',
     localStorage.getItem('jagwa.pencil')!==null&&(localStorage.getItem('jagwa.pencil')==='1')===!!SET.pencil,
     [localStorage.getItem('jagwa.pencil'),SET.pencil]);
   {const before=!!SET.pencil; await pencilSet(!before);
    T('Z-4 토글하면 localStorage 와 SET 이 같이 바뀐다',(localStorage.getItem('jagwa.pencil')==='1')===!before&&!!SET.pencil===!before,[localStorage.getItem('jagwa.pencil'),SET.pencil]);
    await pencilSet(before);}
   {const keep=!!SET.pencil; localStorage.setItem('jagwa.pencil',keep?'1':'0');
    await importData({text:async()=>JSON.stringify({v:2,set:{pencil:!keep,zoom:1}})});
    T('Z-4 백업 복원은 pencil 을 안 얹는다(기기 값 그대로)',!!SET.pencil===keep&&(localStorage.getItem('jagwa.pencil')==='1')===keep,[keep,SET.pencil]);}
   });
   SET.pencil=false; try{localStorage.setItem('jagwa.pencil','0')}catch(e){}   /* 아래 검사는 손가락으로 긋는다 */

   /* ═══ 교재 모드 ═══ */
   const g=DATA.find(r=>r[F.YEAR]); await openView(g?g[F.NO]:1); await wait(60);
   await bkOpen(208); await wait(1800);
   const p=BK.pgs.find(x=>x.pr===208);
   T('Z-0 교재 208쪽 열림',!!p&&BK.pgs.length>0,[BK.pgs.length,$('#bkmsg')&&$('#bkmsg').textContent,window.__err]);
   if(!p)throw new Error('208쪽 없음');

   await del('ink','bink:208'); BK.ink['bink:208']=undefined; await zInkLoad(BK,p);
   await zInkCommit(BK,{i:p.i,c:'#B03A2E',w:24,hl:false,p:[160,160,360,240,560,300]});
   await wait(60);
   T('Z-0 획 하나 저장됨',(await get('ink','bink:208')).s.length===1);

   /* ① 배율 둘에서 타일 위에 잉크가 오는가 */
   const seen=[];
   for(const S of [1,2.4]){
     zSetZoom(BK,S); await center(BK,p,160,160); await tilesReady('#bktiles'); await wait(800);
     const nCv=$$('#bktiles canvas').length;
     const q=ptOf(p.el,p.w,p.h,160,160);
     const st=stackAt(q.x,q.y);
     seen.push({S,nCv,ink:st.ink,tile:st.tile,names:st.names});
     T('Z-1 배율 '+S+': 잉크가 타일 위에 있다(elementsFromPoint 에서 잉크가 먼저)',
       nCv>0&&st.ink>=0&&st.tile>=0&&st.ink<st.tile,[S,nCv,st.ink,st.tile,st.names]);
   }

   /* ② 타일끼리 순서 — 옛 버킷 층(z 1)을 하나 만들어 지금 층(z 2) 아래인지, 둘 다 잉크 아래인지 */
   {
     await center(BK,p,160,160);
     const L=BK.layers[0];
     T('Z-2 지금 타일 층에 인라인 z-index 2 가 그대로',!!L&&L.el.style.zIndex==='2',L&&L.el.style.zIndex);
     const old=document.createElement('div'); old.className='ztl'; old.dataset.b='test';
     old.style.cssText=L.el.style.cssText; old.style.zIndex='1';
     const cv=document.createElement('canvas'); cv.width=cv.height=8; cv.className='ztile';
     cv.style.cssText=$$('#bktiles canvas')[0].style.cssText;
     old.appendChild(cv); $('#bktiles').insertBefore(old,$('#bktiles').firstChild);
     await wait(60);
     const q=ptOf(p.el,p.w,p.h,160,160);
     hitOn(); const els=document.elementsFromPoint(q.x,q.y); hitOff();
     const iNew=els.findIndex(e=>e.closest&&e.closest('.ztl')&&e.closest('.ztl')!==old);
     const iOld=els.findIndex(e=>e.closest&&e.closest('.ztl')===old);
     const iInk=els.findIndex(e=>e.closest&&e.closest('.bkink'));
     T('Z-2 지금 층(z2)이 옛 층(z1) 위 · 둘 다 잉크 아래',iInk>=0&&iNew>=0&&iInk<iNew&&(iOld<0||iNew<iOld),[iInk,iNew,iOld]);
     old.remove();
   }
   zSetZoom(BK,1); await wait(600);

   /* ⑤⑥ 손바닥 거르기 · 핀치 */
   await grp('Z-5/6', async()=>{
     $('#bktools span[data-tool="pen"]').click();
     const vp=$('#bkvp'),r=vp.getBoundingClientRect();
     const PE=(t,x,y,id,pt)=>vp.dispatchEvent(new PointerEvent(t,{clientX:x,clientY:y,pointerId:id,pointerType:pt,bubbles:true,cancelable:true,isPrimary:id===1}));
     const n0=(await get('ink','bink:208')).s.length;
     const x0=r.left+r.width*0.4,y0=r.top+r.height*0.4;
     PE('pointerdown',x0,y0,1,'pen'); await wait(20);
     PE('pointermove',x0+30,y0+10,1,'pen'); await wait(20);
     PE('pointerdown',x0+180,y0+180,2,'touch'); await wait(20);   /* 손바닥 */
     const liveMid=$$('#bkover .bkink .zlive').some(el=>!!el.getAttribute('d'));   /* 어느 쪽에 그어졌는지 모르니 전부 본다 */
     PE('pointermove',x0+60,y0+24,1,'pen'); await wait(20);
     PE('pointerup',x0+180,y0+180,2,'touch');
     PE('pointerup',x0+60,y0+24,1,'pen'); await wait(120);
     const n1=(await get('ink','bink:208')).s.length;
     T('Z-5 펜 스트로크 도중 손바닥(touch)이 닿아도 획이 안 버려진다',n1===n0+1&&liveMid,[n0,n1,liveMid]);

     const S0=BK.S;
     $('#bktools span[data-tool="view"]').click();
     PE('pointerdown',r.left+300,r.top+300,11,'touch');
     PE('pointerdown',r.left+400,r.top+300,12,'touch'); await wait(20);
     PE('pointermove',r.left+500,r.top+300,12,'touch'); await wait(40);
     PE('pointerup',r.left+500,r.top+300,12,'touch');
     PE('pointerup',r.left+300,r.top+300,11,'touch'); await wait(40);
     T('Z-6 touch 둘이면 여전히 핀치(배율 커짐)',BK.S>S0,[S0,BK.S]);
     zSetZoom(BK,1); await wait(300);
   });

   /* ③ 서브노트도 같은 병이었다 */
   await grp('Z-3', async()=>{
     bkClose(); await wait(80);
     await subOpen('3.4',true); await wait(2500);
     const sp=SUB.pages()[0];
     await del('ink',sp.key); SUB.ink[sp.key]=undefined; await zInkLoad(SUB,sp);
     await zInkCommit(SUB,{i:sp.i,c:'#B03A2E',w:24,hl:false,p:[200,200,400,280]});
     zSetZoom(SUB,0.8); await center(SUB,sp,200,200); await tilesReady('#stiles'); await wait(1200);
     const pel=$('#sover .spgo[data-i="0"]');
     const nCv=$$('#stiles canvas').length;
     const q=ptOf(pel,sp.w,sp.h,200,200);
     const st=stackAt(q.x,q.y);
     T('Z-3 서브노트도 잉크가 타일 위에 있다',nCv>0&&st.ink>=0&&st.tile>=0&&st.ink<st.tile,[nCv,st.ink,st.tile,st.names]);
     $('#sX').click(); await wait(60);
   });

   T('Z-0 콘솔 오류 0',(window.__err||[]).length===0,window.__err);
  }catch(e){T('예외',false,String(e&&e.stack||e)+' · 진단 '+JSON.stringify({err:(window.__err||[]).slice(0,6),db:typeof db==='undefined'?'TDZ/없음':(db?db.name:String(db)),ms:Math.round(performance.now()),rs:document.readyState}))}   /* ★ 2026-10-07 (_task_jagwa_phys_win 회귀) 진단만 · 판정 무변 — 옛 줄: }catch(e){T('예외',false,String(e&&e.stack||e))} */
  try{await __nativeFetch('/result',{method:'POST',body:R.join(String.fromCharCode(10))})}catch(e){}
 }
 if(document.readyState==='complete')setTimeout(run,600);else window.addEventListener('load',()=>setTimeout(run,600));
})();
</script>"""


# ── _task_qa_slim2(10/8 · J2) regress · smoke 도우미 — 이름이 `_rg` 로 시작하는 것 = gate 에서 안 쓰는 갈래(TESTS 상수는 글자 그대로) ──
#   쪽 안 고정 대기(bkOpen 뒤 1800 · 배율마다 800 · subOpen 뒤 2500 …)는 TESTS 상수 그대로(두 벌 안 둠) · db 기다림은 10/8 phys_win 판이 이미 조건으로 바꿈
def _rg_regress_tests(t):
    """regress — 처리안 「뺌」 Z-4 옛 여섯(펜슬 기계 · 9/30 걷음 · 지금 앱에선 return 으로 안 돎)을 그 자리에서 잘라 냄 · 나머지 글자 그대로(못 찾으면 통째)"""
    nl = lambda i: t.find('\n', i) + 1
    r0 = t.find("   if(typeof pencilUnify!=='function')return;")
    r1 = t.find("   });\n   SET.pencil=false;")
    if min(r0, r1) < 0 or not r0 < r1:
        print('NOTE | regress 자르기 자리 못 찾음 — 통째로 돈다')
        return t
    return t[:nl(r0)] + t[r1:]


def _rg_smoke_tests(t):
    """smoke — 앞머리 + Z-0 첫 칸(카드 층 부팅) + 손가락 설정 · 교재 208쪽 열기 · 획 하나 · Z-1 배율 둘(잉크가 타일 위) + Z-0 콘솔 오류 0 · 예외 · 결과 보냄
    (원래 글을 그 자리에서 잘라 씀 · 못 찾으면 통째)"""
    nl = lambda i: t.find('\n', i) + 1
    a = t.find("   T('Z-0 지학 카드 층으로 떴다'")
    b0 = t.find("   SET.pencil=false; try{localStorage.setItem('jagwa.pencil','0')}catch(e){}")
    b1 = t.find("   /* ② 타일끼리 순서")
    j0 = t.find("   T('Z-0 콘솔 오류 0'")
    if min(a, b0, b1, j0) < 0 or not (a < b0 < b1 < j0):
        print('NOTE | smoke 자르기 자리 못 찾음 — 통째로 돈다')
        return t
    return t[:nl(a)] + t[b0:b1] + t[j0:]


def main():
    html = open(SRC, encoding='utf-8', newline='').read()
    html = html.replace('<script defer src="https://cdnjs', '<script defer data-off="https://cdnjs')
    html = html.replace('<link rel="stylesheet" href="https://cdnjs', '<link rel="off" href="https://cdnjs')
    html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js',
                        STUB + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    html = html.replace('</body>', (TESTS if QC.GATE else (_rg_regress_tests(TESTS) if not QC.SMOKE else _rg_smoke_tests(TESTS))) + '</body>', 1)   # regress — 뺌 여섯 잘라 냄 · smoke — smoke 칸만 · 쪽 안 시험 글을 이 자리에서만 잘라 씀
    open(APP, 'w', encoding='utf-8', newline='').write(html)
    shutil.copy(os.path.join(GIGU, '지학_서브노트_빈판_A3.pdf'), os.path.join(OUT, 'blank.pdf'))

    done = threading.Event(); box = {}

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=OUT, **k)
        def log_message(self, *a, **k): pass
        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            if p.startswith('/notes/'):
                f = os.path.join(os.path.expanduser('~'), 'Documents', 'notes', p[7:].replace('/', os.sep))
                if not os.path.isfile(f): self.send_response(404); self.end_headers(); return
                b = open(f, 'rb').read(); self.send_response(200); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b); return
            if p.startswith('/data/'):
                rel = p[6:]
                if not rel.startswith('earth/'): self.send_response(404); self.end_headers(); return
                f = os.path.join(SPD, rel[6:].replace('/', os.sep))
                if not os.path.isfile(f): self.send_response(404); self.end_headers(); return
                b = open(f, 'rb').read()
                self.send_response(200); self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', str(len(b))); self.send_header('X-Sha', hashlib.sha1(b).hexdigest()); self.end_headers()
                self.wfile.write(b); return
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
    QC.launch('new')   # 셈(§B-4) — 새 판 크롬 한 번(바탕은 본디 안 띄운다)
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

    if QC.want('src'):   # smoke — 브라우저 밖 소스 칸(Z-7 셋 · isolation · 타일 순서 코드 · 백틱)은 smoke 칸이 아니다
        s = open(SRC, encoding='utf-8').read()
        T2('Z-7 타일 층이 쌓임 맥락을 만든다 — #bktiles·#stiles 에 isolation:isolate',
           '#bktiles{' in s and '#stiles{' in s
           and 'isolation:isolate' in s[s.index('#bktiles{'):s.index('#bktiles{') + 200]
           and 'isolation:isolate' in s[s.index('#stiles{'):s.index('#stiles{') + 200])
        T2('Z-7 타일끼리 순서 코드는 그대로(l===L?2:1)', "l.el.style.zIndex=l===L?2:1" in s)
        T2('Z-7 백틱 짝', s.count('`') % 2 == 0)
    npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
    for x in lines: print(x)
    print('\n== 쌓임/펜슬/손바닥 %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
