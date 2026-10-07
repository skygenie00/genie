# -*- coding: utf-8 -*-
"""잉크 형식 가드 헤드리스 검산 (2026-09-07 · gigu/_task_jagwa_ink_guard.md §3)

_harness_earth.py 의 통(가짜 GitHub · 로컬 studyplandata · 헤드리스 크롬)을 그대로 쓰되
검사는 §3 의 셋만 본다.
  ① 층 꼴 · 순배열 · 모르는 꼴 기록을 심어 두고 획을 얹었을 때 저장·다시 그리기가 되는가
     (모르는 꼴은 ink_orphan: 이 생겼는가 · 원본은 안 지워졌는가)
  ② 옛 필기가 화면(SVG path)에 되살아나는가
  ③ HAVE 빈 상태에서 카드 층은 필기가 안 막히는가 · 물리 식은 종전 그대로인가

돌리기:  PYTHONIOENCODING=utf-8 python _harness_ink.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import http.server, os, socketserver, subprocess, sys, threading, hashlib, json, shutil, urllib.parse

GENIE = _roots.genie()
SRC = os.path.join(GENIE, 'jagwa', 'index.html')
SPD = os.path.join(_roots.spd(), 'earth')
GIGU = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.environ.get('TEMP', '.'), 'inkh'); os.makedirs(OUT, exist_ok=True)
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
 window.__puts=[];
 window.fetch=async function(url,opt){
  opt=opt||{};const u=String(url);
  const m=/api\.github\.com\/repos\/([^\/]+\/[^\/]+)\/contents\/([^?]+)/.exec(u);
  if(!m){ if(/api\.github\.com\/repos\/zzikkaplan\/notes/.test(u))return {ok:true,status:200,json:async()=>({name:'notes'}),text:async()=>''}; return __nativeFetch(url,opt); }
  const path=decodeURIComponent(m[2]);
  if(m[1]==='zzikkaplan/notes'){const r=await __nativeFetch('/notes/'+encodeURI(path),{cache:'no-store'});return r.ok?r:{ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)}}
  if((opt.method||'GET')==='PUT'){window.__puts.push(path);return {ok:true,status:200,json:async()=>({content:{sha:'x'+window.__puts.length}}),text:async()=>''}}
  const r=await __nativeFetch('/data/'+encodeURI(path),{cache:'no-store'});
  if(!r.ok)return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
  const acc=(opt.headers||{}).Accept||'';
  if(acc.indexOf('raw')>=0)return r;
  const sha=r.headers.get('X-Sha')||'sha';
  return {ok:true,status:200,json:async()=>({sha}),text:async()=>JSON.stringify({sha})};
 };
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 setInterval(()=>{try{__nativeFetch('/partial',{method:'POST',body:R.join(String.fromCharCode(10))+String.fromCharCode(10)+'(err) '+JSON.stringify(window.__err||[])})}catch(e){}},3000);

 const KEY='bink:208';
 const svgN=p=>p.el.querySelectorAll('.bkink path[data-j]').length;
 const norm01=v=>v.every(x=>x>=0&&x<=1);
 /* 한 번 심고 → 다시 읽고(zInkLoad) → 한 획 얹는(zInkCommit) 한 바퀴 */
 async function cycle(p,seed){
   for(const k of await keys('ink'))if(String(k).indexOf('ink_orphan:')===0)await del('ink',k);
   await del('ink',KEY);
   if(seed!==undefined)await put('ink',KEY,seed);
   BK.ink[KEY]=undefined;
   const mv0=INKMV,or0=INKORPH;
   await zInkLoad(BK,p);await wait(30);
   const afterLoad=await get('ink',KEY), drawn=svgN(p);
   await zInkCommit(BK,{i:p.i,c:'#243a5e',w:1.2,hl:false,p:[100,100,200,150,300,160]});await wait(30);
   const afterCommit=await get('ink',KEY);
   const orphKeys=(await keys('ink')).filter(k=>String(k).indexOf('ink_orphan:')===0);
   const orph=orphKeys.length?await get('ink',orphKeys[0]):null;
   return {afterLoad,drawn,afterCommit,orphKeys,orph,mv:INKMV-mv0,or:INKORPH-or0,painted:svgN(p)};
 }

 async function run(){
  try{
   localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}));
   for(let __i=0;__i<300&&(typeof db==='undefined'||!db);__i++)await wait(100);   /* ★ 2026-10-08 (_task_jagwa_phys_win) 고정 대기(load+600ms) 대신 IndexedDB(db)가 설 때까지(30 초 한도) — 짐이 크면 600ms 안에 안 열려 「db 없음」 예외(1 단계 셋 다) · 같은 판을 짐 적을 때 돌리면 정상(00:25 진단) */
   await loadEarthData(); draw(); await wait(50);
   T('G-0 지학 카드 층으로 떴다(CARD_LAYER · earth1)',CARD_LAYER===true&&db.name==='earth1'&&DATA.length>0,[CARD_LAYER,db.name,DATA.length]);
   /* inkGet·inkOrphan 은 async 라 Annex B 로 전역에 안 올라온다 — if(CARD_LAYER) 블록 안에서만 산다(부르는 쪽도 그 안이라 문제 없음). 여기선 inkNorm 만 직접 본다. */
   T('G-0 inkNorm 한 자리가 있다',typeof inkNorm==='function'&&typeof inkNormArr==='function');

   /* 형식만 보는 순수 검사 — 쪽 없이 */
   const P={w:1000,h:2000};
   T('G-0 새 꼴은 그대로 통과(옮김 없음)',(()=>{const v={s:[{c:'#000',w:1,hl:0,p:[0.1,0.2]}]};const r=inkNorm(v,P);return r.val===v&&!r.moved&&!r.orphan})());
   T('G-0 빈값 → {s:[]} · 옮김 없음',(()=>{const r=inkNorm(undefined,P);return r.val.s.length===0&&!r.moved&&!r.orphan})());
   T('G-0 층 꼴 → 획 이어 붙임 · 0~1 밖은 쪽 크기로 나눔',(()=>{
      const r=inkNorm({0:[{c:'#a',w:1,hl:0,p:[500,1000]}],1:[{c:'#b',w:1,hl:0,p:[0.25,0.5]}]},P);
      return r.moved&&!r.orphan&&r.val.s.length===2&&r.val.s[0].p[0]===0.5&&r.val.s[0].p[1]===0.5&&r.val.s[1].p[0]===0.25})());
   T('G-0 순배열 → {s:[…]}',(()=>{const r=inkNorm([{c:'#a',w:1,hl:0,p:[0.1,0.2]}],P);return r.moved&&!r.orphan&&r.val.s.length===1})());
   T('G-0 모르는 꼴 → orphan(옮기지 않는다)',(()=>{const r=inkNorm({canvas:'data:image/png;base64,AAAA'},P);return r.orphan&&!r.moved&&r.val.s.length===0})());
   T('G-0 쪽 크기를 모르는데 0~1 밖 → 추측하지 않고 orphan',(()=>{const r=inkNorm([{c:'#a',w:1,hl:0,p:[500,1000]}],null);return r.orphan&&!r.moved})());

   /* 교재 모드를 연다 */
   const g=DATA.find(r=>r[F.YEAR]);await openView(g?g[F.NO]:1);await wait(60);
   await bkOpen(208);await wait(1500);
   const p=BK.pgs.find(x=>x.pr===208);
   T('G-0 교재 208쪽 열림',!!p&&BK.pgs.length>0,[BK.pgs.length,$('#bkmsg')&&$('#bkmsg').textContent,window.__err]);
   if(!p)throw new Error('208쪽 없음');

   /* ── ① 층 꼴 ─────────────────────────────────────────────── */
   let c=await cycle(p,{0:[{c:'#B03A2E',w:1.2,hl:0,p:[100,100,200,150]}],1:[{c:'#2F6FD0',w:1.2,hl:0,p:[300,300,400,320]}]});
   T('G-1 층 꼴: 읽으면 {s:[2획]} 로 옮겨져 그 자리에서 저장된다',!!c.afterLoad&&Array.isArray(c.afterLoad.s)&&c.afterLoad.s.length===2&&c.mv===1&&c.or===0,[c.afterLoad,c.mv,c.or]);
   T('G-1 층 꼴: 좌표가 0~1 로 정규화(100/쪽폭)',c.afterLoad.s.every(s=>norm01(s.p))&&Math.abs(c.afterLoad.s[0].p[0]*p.w-100)<0.2,c.afterLoad.s.map(s=>s.p));
   T('G-2 층 꼴: 옛 필기가 화면에 되살아난다(SVG path 2)',c.drawn===2,c.drawn);
   T('G-1 층 꼴: 획을 얹으면 저장된다(2→3) · 화면도 3',c.afterCommit.s.length===3&&c.painted===3,[c.afterCommit.s.length,c.painted]);
   T('G-1 층 꼴: orphan 안 생김',c.orphKeys.length===0,c.orphKeys);

   /* ── ① 순배열 ────────────────────────────────────────────── */
   c=await cycle(p,[{c:'#B03A2E',w:1.2,hl:0,p:[0.1,0.1,0.2,0.15]},{c:'#2F6FD0',w:1.2,hl:0,p:[0.3,0.3,0.4,0.32]}]);
   T('G-1 순배열: {s:[2획]} 로 옮겨짐 · 화면 2 · 얹으면 3',!!c.afterLoad&&c.afterLoad.s.length===2&&c.drawn===2&&c.afterCommit.s.length===3&&c.mv===1&&c.or===0,[c.afterLoad,c.drawn,c.afterCommit.s.length]);
   T('G-1 순배열: orphan 안 생김',c.orphKeys.length===0,c.orphKeys);

   /* ── ① 모르는 꼴 ─────────────────────────────────────────── */
   const raw={canvas:'data:image/png;base64,AAAA',v:1};
   c=await cycle(p,raw);
   T('G-1 모르는 꼴: ink_orphan:bink:208 에 원본이 그대로 남는다(버리지도 덮지도 않는다)',c.orphKeys.length===1&&c.orphKeys[0]==='ink_orphan:'+KEY&&JSON.stringify(c.orph)===JSON.stringify(raw),[c.orphKeys,c.orph]);
   T('G-1 모르는 꼴: 그 키는 {s:[]} 로 새로 시작 · 획을 얹으면 저장된다(0→1)',c.afterLoad.s.length===0&&c.afterCommit.s.length===1&&c.painted===1&&c.or===1&&c.mv===0,[c.afterLoad,c.afterCommit.s.length,c.or,c.mv]);

   /* ── 새 꼴은 건드리지 않는다 ──────────────────────────────── */
   c=await cycle(p,{s:[{c:'#B03A2E',w:1.2,hl:0,p:[0.1,0.1,0.2,0.15]}]});
   T('G-1 새 꼴: 옮김 0 · orphan 0 · 획 1→2',c.mv===0&&c.or===0&&c.afterLoad.s.length===1&&c.afterCommit.s.length===2,[c.mv,c.or,c.afterCommit.s.length]);

   /* ── 기록 없음(첫 필기) ──────────────────────────────────── */
   c=await cycle(p,undefined);
   T('G-1 기록 없음: 헛 저장 없이(읽기만으론 키가 안 생김) 첫 획이 남는다',c.mv===0&&c.or===0&&c.afterLoad===undefined&&c.afterCommit.s.length===1&&c.painted===1,[c.mv,c.or,c.afterLoad,c.painted]);

   /* ── 가져오기(bkImportObj) 도 같은 길을 탄다 ─────────────── */
   await del('ink',KEY);for(const k of await keys('ink'))if(String(k).indexOf('ink_orphan:')===0)await del('ink',k);
   BK.ink[KEY]=undefined;
   let nImp=await bkImportObj({v:1,bink:{'bink:208':{0:[{c:'#a',w:1,hl:0,p:[100,100,200,150]}]}}});
   let imp=await get('ink',KEY);
   T('G-1 가져오기: 층 꼴도 {s:[…]} 로 옮겨 담는다',nImp===1&&!!imp&&imp.s.length===1&&norm01(imp.s[0].p),[nImp,imp]);
   await put('ink',KEY,{s:[{c:'#a',w:1,hl:0,p:[0.5,0.5]}]});BK.ink[KEY]=undefined;
   const or1=INKORPH;
   nImp=await bkImportObj({v:1,bink:{'bink:208':{canvas:'x'}}});
   imp=await get('ink',KEY);
   T('G-1 가져오기: 모르는 꼴은 기기 기록을 덮지 않는다(orphan 만 남고 n=0)',nImp===0&&imp.s.length===1&&INKORPH===or1+1,[nImp,imp,INKORPH-or1]);
   await del('ink',KEY);for(const k of await keys('ink'))if(String(k).indexOf('ink_orphan:')===0)await del('ink',k);BK.ink[KEY]=undefined;

   /* ── §2.3 put 이 실패해도 화면은 갱신 · 토스트 ────────────── */
   await zInkLoad(BK,p);await wait(20);
   const n0=svgN(p);const _put=put;let blocked=0;
   put=function(s,k,v){if(s==='ink'){blocked++;return Promise.resolve(0)}return _put(s,k,v)};
   document.querySelectorAll('.toast').forEach(x=>x.remove());
   await zInkCommit(BK,{i:p.i,c:'#243a5e',w:1.2,hl:false,p:[110,110,210,160,310,170]});await wait(40);
   const toasts=[...document.querySelectorAll('.toast')].map(x=>x.textContent);
   put=_put;
   T('G-3 put 실패에도 화면은 갱신된다(조용히 죽지 않음)',svgN(p)===n0+1&&blocked>0,[n0,svgN(p),blocked]);
   T('G-3 실패는 토스트로 알린다',toasts.some(t=>t.indexOf('저장하지 못했습니다')>=0),toasts);
   await del('ink',KEY);BK.ink[KEY]=undefined;await zInkLoad(BK,p);await wait(20);

   /* ── ③ 문항 가드: HAVE 가 비어도 카드 층은 안 막힌다 ─────── */
   bkClose();await wait(60);
   const haveKeys=Object.keys(HAVE);HAVE={};
   INK={0:[]};LAYER=0;
   const _spc=Element.prototype.setPointerCapture;Element.prototype.setPointerCapture=function(){};
   const before=(INK[LAYER]||[]).length;
   const pen0=SET.pencil;SET.pencil=false;
   /* A-6(a) 9/30 — 문항 필기(#inkc)는 **펜만**이다(moolri/_task_jagwa_pen_touch2 §1 「SET.pencil 21곳 → if(pointerType!=='pen') return」 · §6-5 갈래 표 「1 문항 필기 #inkc — pen 필기 · mouse 조작」 · c62b2b2)
      → SET.pencil=false 로 마우스 획을 열던 길이 없어졌다 · 펜으로 누른다(재는 것 = HAVE 가 비어도 카드 층은 안 막힌다 그대로) */
   $('#inkc').dispatchEvent(new PointerEvent('pointerdown',{clientX:20,clientY:20,pointerId:11,pointerType:'pen',bubbles:true,cancelable:true,isPrimary:true}));
   await wait(20);
   const after=(INK[LAYER]||[]).length;
   $('#inkc').dispatchEvent(new PointerEvent('pointerup',{clientX:20,clientY:20,pointerId:11,pointerType:'pen',bubbles:true,cancelable:true,isPrimary:true}));
   SET.pencil=pen0;Element.prototype.setPointerCapture=_spc;HAVE={};haveKeys.forEach(k=>HAVE[k]=1);
   T('G-4 HAVE 빈 상태에서도 카드 층 문항 필기는 안 막힌다(획 하나 시작됨)',after===before+1,[before,after]);

   T('errors 0',(window.__err||[]).length===0,window.__err);
  }catch(e){T('예외',false,String(e&&e.stack||e)+' · 진단 '+JSON.stringify({err:(window.__err||[]).slice(0,6),db:typeof db==='undefined'?'TDZ/없음':(db?db.name:String(db)),ms:Math.round(performance.now()),rs:document.readyState}))}   /* ★ 2026-10-07 (_task_jagwa_phys_win 회귀) 진단만 · 판정 무변 — 옛 줄: }catch(e){T('예외',false,String(e&&e.stack||e))} */
  try{await __nativeFetch('/result',{method:'POST',body:R.join(String.fromCharCode(10))})}catch(e){}
 }
 if(document.readyState==='complete')setTimeout(run,600);else window.addEventListener('load',()=>setTimeout(run,600));
})();
</script>"""


def main():
    html = open(SRC, encoding='utf-8', newline='').read()
    html = html.replace('<script defer src="https://cdnjs', '<script defer data-off="https://cdnjs')
    html = html.replace('<link rel="stylesheet" href="https://cdnjs', '<link rel="off" href="https://cdnjs')
    html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js',
                        STUB + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    html = html.replace('</body>', TESTS + '</body>', 1)
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
    p = subprocess.Popen([chrome, '--headless=new', '--disable-gpu', '--no-first-run', '--user-data-dir=' + prof,
                          '--window-size=1400,900', 'http://127.0.0.1:%d/app.html' % port],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    import time as _t; _t0 = _t.time()
    got = done.wait(int(os.environ.get('HARNESS_WAIT', '300'))); p.terminate(); print('elapsed %.0fs' % (_t.time() - _t0))
    try: p.wait(10)
    except Exception: p.kill()
    srv.shutdown()
    if not got:
        print('결과 없음 — 시간 안에 검사가 끝나지 않았다 · 마지막 중간 결과:'); print(box.get('partial', '(없음)')); sys.exit(1)
    lines = [ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()]

    def T2(name, cond, info=''):
        lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))

    s = open(SRC, encoding='utf-8').read()
    T2('G-5 문항 가드는 CARD_LAYER 만 덧붙었다 — 물리 식(lc.id!==IMG && !HAVE[lc.id])은 글자 그대로',
       "if(!CARD_LAYER&&lc.id!=='IMG'&&!HAVE[lc.id])return;" in s and s.count("!HAVE[lc.id])return;") == 1)
    T2('G-5 옛 가드(가드 없는 .s.push · get 직접 호출)는 남아 있지 않다',
       "if(Z.ink[p.key]===undefined)Z.ink[p.key]=(await get('ink',p.key))||{s:[]}" not in s
       and "zInkLoad=async function(Z,p){Z.ink[p.key]=await inkGet(p.key,p);zInkPaint(Z,p)}" in s)
    T2('G-5 inkNorm·inkGet·inkOrphan 은 카드 층(if(CARD_LAYER)) 안에 있다 — 물리엔 안 실린다',
       s.index('if(CARD_LAYER){') < s.index('function inkNorm(') < s.index('/*/EARTH:js*/'))
    T2('G-5 물리 층에서 바뀐 줄은 문항 가드 한 줄뿐(#inkc 밖 물리 코드 무변)',
       "if(!CARD_LAYER&&lc.id!=='IMG'" in s and 'inkGet(' not in s[:s.index('if(CARD_LAYER){')])
    T2('G-5 백틱 짝', s.count('`') % 2 == 0)
    npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
    for x in lines: print(x)
    print('\n== 잉크 가드 %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
