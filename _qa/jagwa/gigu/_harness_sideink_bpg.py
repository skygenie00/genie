# -*- coding: utf-8 -*-
"""교재 잉크 · 교재쪽 다중 고정 헤드리스 검산
(2026-09-07 · gigu/_task_jagwa_pan1.md §3 · **2026-09-10 자리 옮김**)

  ⚠⚠ 2026-09-10 — 사용자 확정으로 **옆 교재 칸(#bookpane)을 걷었다.** 교재는 팝업 창 하나다.
     그래서 A(옆 칸 잉크 **덧층**)는 잴 대상이 없어졌다 — 덧층이 하던 일(교재 모드 획을 다른 자리에서
     읽기 전용으로 보여 주기)을 이제 **교재 창이 본체로** 한다. A 를 그 자리에서 다시 잰다.
     B3(고정 칩 줄)도 담는 자리가 교재 창 머리줄로 옮겨 갔다.

  A 덧층 — 획 수 일치 · 쌓임(캔버스 위) · 쪽 넘김 · 조각 없는 쪽은 빈다 · 읽기 전용
  B 고정 — bpgList 세 갈래 · bpgOf(last 우선) · 쓰기는 새 꼴만 · 고정한 쪽에 뜬다 · 칩 +N
  C 동기화 — 지학 SYNC_KEYS 15 · bpg 포함

    PYTHONIOENCODING=utf-8 python _harness_sideink_bpg.py
    PYTHONIOENCODING=utf-8 python _harness_sideink_bpg.py bio
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import http.server, os, socketserver, subprocess, sys, threading, hashlib, shutil, urllib.parse

GENIE = _roots.genie()
SRC = os.path.join(GENIE, 'jagwa', 'index.html')
SPDROOT = _roots.spd()
GIGU = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.environ.get('TEMP', '.'), 'sinkh'); os.makedirs(OUT, exist_ok=True)

SUBJ = 'bio' if 'bio' in sys.argv[1:] else 'earth'
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
 const paths=()=>$$('#bpink path').length;
 /* 쌓임 재기 — 덧층·캔버스에 잠깐만 pointer-events 를 주고(쌓임에는 영향 없다) 누가 위인지 본다 */
 let hit=null;
 const hitOn=()=>{if(hit)return;hit=document.createElement('style');
   hit.textContent='#bpink,#bpink *{pointer-events:auto!important}#bpc{pointer-events:auto!important}';
   document.head.appendChild(hit)};
 const hitOff=()=>{if(hit){hit.remove();hit=null}};

 async function run(){
  try{
   localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}));
   await loadEarthData(); draw(); await wait(80);
   T('S-0 카드 층 · 데이터 적재',CARD_LAYER===true&&DATA.length>0&&(TOC.list||[]).length>0,[SUBJ_ID,DATA.length]);

   /* ═══ C. SYNC_KEYS ═══ */
   await grp('S-C', async()=>{
     T('S-C 지학 SYNC_KEYS 19개 · … tfix 18 · bref 19',SUBJ.earth.SYNC_KEYS.length===19&&SUBJ.earth.SYNC_KEYS.indexOf('bpg')===14&&SUBJ.earth.SYNC_KEYS.indexOf('crop')===15,SUBJ.earth.SYNC_KEYS);
     T('S-C 생물 SYNC_KEYS 20(add1 +bref) · 물리 12 무변',SUBJ.bio.SYNC_KEYS.length===20&&SUBJ.phys.SYNC_KEYS.length===12,[SUBJ.bio.SYNC_KEYS.length,SUBJ.phys.SYNC_KEYS.length]);
     T('S-C 지금 과목의 SYNC_KEYS 에 bpg · SYNC_REF 에 읽기/쓰기 있다',SYNC_KEYS.indexOf('bpg')>=0&&!!SYNC_REF.bpg&&typeof SYNC_REF.bpg.g==='function',SYNC_KEYS.length);
   });

   /* ═══ B(1) 값 꼴 ═══ */
   await grp('S-B1', async()=>{
     const r=DATA.find(x=>+x[F.BPAGE]>0)||DATA[0], uid=r[F.CODE], auto=+r[F.BPAGE]||0;
     const keep=BPG[uid];
     delete BPG[uid];
     T('S-B1 값 없음 → 자동값(BPAGE) 하나',JSON.stringify(bpgList(r))===JSON.stringify(auto?[auto]:[])&&bpgOf(r)===auto,[bpgList(r),bpgOf(r),auto]);
     BPG[uid]={p:12,s:3};
     T('S-B1 옛 꼴 {p,s} → [12] · 대표 12',JSON.stringify(bpgList(r))==='[12]'&&bpgOf(r)===12,[bpgList(r),bpgOf(r)]);
     BPG[uid]={ps:[12,13,88],last:13};
     T('S-B1 새 꼴 → [12,13,88] · 대표는 last(13)',JSON.stringify(bpgList(r))==='[12,13,88]'&&bpgOf(r)===13,[bpgList(r),bpgOf(r)]);
     BPG[uid]={ps:[12,13,88],last:99};
     T('S-B1 last 가 ps 밖이면 ps[0]',bpgOf(r)===12,bpgOf(r));
     BPG[uid]={ps:[12,13,88]};
     T('S-B1 last 가 없어도 ps[0]',bpgOf(r)===12,bpgOf(r));
     const bad0=BPGBAD; BPG[uid]={뭔가:1};
     T('S-B1 모르는 꼴 → 자동값으로 흘리고 BPGBAD 로 센다(덮지 않는다)',
       JSON.stringify(bpgList(r))===JSON.stringify(auto?[auto]:[])&&BPGBAD>bad0,[bpgList(r),BPGBAD-bad0]);
     /* 쓰기는 새 꼴로만 */
     delete BPG[uid];
     bpgWrite(uid,[88,12,12,0,13],13);
     T('S-B1 bpgWrite = 새 꼴만 · 중복/0 제거 · 오름차순',JSON.stringify(BPG[uid])==='{"ps":[12,13,88],"last":13}',BPG[uid]);
     bpgWrite(uid,[12],99);
     T('S-B1 last 가 ps 밖이면 ps[0] 로 눕힌다',BPG[uid].last===12,BPG[uid]);
     T('S-B1 빈 배열이면 키를 지운다(자동값으로)',bpgWrite(uid,[])===null&&BPG[uid]===undefined);
     if(keep!==undefined)BPG[uid]=keep;else delete BPG[uid];
   });

   /* ═══ B(5) 고정한 쪽에 뜬다 — 판 2 add1(9/7) 로 「수는 늘 수만 있다」 전제를 거두었다 ═══ */
   await grp('S-B5', async()=>{
     const page=208, base=bookRows(page).length;
     const r=DATA.find(x=>bookRows(page).indexOf(x)<0);
     const uid=r[F.CODE], keep=BPG[uid];
     bpgWrite(uid,[page],page);
     const now=bookRows(page).length;
     T('S-B5 안 뜨던 문항을 그 쪽에 고정하면 「이 쪽에서 나온 문항」에 더해진다',now===base+1,[base,now]);
     if(keep!==undefined)BPG[uid]=keep;else delete BPG[uid];
     T('S-B5 되돌리면 원래 수',bookRows(page).length===base,[bookRows(page).length,base]);
   });

   /* ═══ A. 교재 잉크 — **자리가 옮겨 갔다**(2026-09-10) ═══
      옛 A 는 옆 교재 칸(#bpwrap·#bpink·#bpc)의 **읽기 전용 덧층**을 쟀다.
      옆 칸을 걷었으므로 그 덧층은 없다. 덧층이 하던 일(같은 키 bink:<쪽> 의 획을 보여 주기)을
      이제 교재 창이 **본체로** 한다. 그것을 여기서 잰다.
      ⚠ 「창 안에서 새로 긋기」는 `_harness_jagwa_3geon.py` W-2 가 잰다 — 여기서 겹쳐 재지 않는다. */
   await grp('S-A', async()=>{
     const PG=208;
     await del('ink','bink:'+PG);
     await openView((DATA.find(x=>+x[F.BPAGE]>0)||DATA[0])[F.NO]); await wait(300);
     T('S-A ★옆 교재 칸은 걷혔다 — 교재는 창 하나다(2026-09-10 사용자 확정)',
       getComputedStyle($('#bookpane')).display==='none'&&getComputedStyle($('#tBook')).display==='none',
       [getComputedStyle($('#bookpane')).display,getComputedStyle($('#tBook')).display]);
     await bookOpen(PG); await wait(2800);
     {let n=0;while(n++<60&&!bkCurPage())await wait(200);}
     T('S-A 교재가 창으로 열렸다',!!bkCurPage()&&$('#book').classList.contains('win'),
       [bkCurPage()&&bkCurPage().pr,$('#book').className]);
     const svOf=()=>{const pg=bkCurPage();return pg&&pg.el?pg.el.querySelector('.bkink'):null};   /* BK.svgOf 와 같은 셀렉터 */
     const npath=()=>{const sv=svOf();return sv?sv.querySelectorAll('path[d]').length:-1};
     T('S-A 잉크 0인 쪽 → 획이 0',npath()===0,npath());
     /* 획 셋을 심고 다시 연다 — 키는 옛 덧층과 **같은 bink:<쪽>** 이다(통을 안 바꿨다) */
     await put('ink','bink:'+PG,{s:[
       {c:'#B03A2E',w:20,hl:0,p:[0.2,0.2,0.6,0.35]},
       {c:'#2F6FD0',w:20,hl:0,p:[0.3,0.5,0.7,0.6]},
       {c:'#F2C230',w:24,hl:1,p:[0.2,0.75,0.8,0.78]}]});
     bkClose(); await wait(200);
     await bookOpen(PG); await wait(2800);
     {let n=0;while(n++<60&&!bkCurPage())await wait(200);}
     /* 잉크는 타일이 그려질 때 늦게 읽힌다 — 확실히 읽히고 그리게 한 번 몰아 준다 */
     {const pg=bkCurPage(); if(pg){await zInkLoad(BK,pg); zInkPaint(BK,pg);} }
     let n2=0;while(n2++<40&&npath()!==3)await wait(200);
     const K=await get('ink','bink:'+PG);
     T('S-A ★획 수 = inkGet 이 돌려준 수(3) — 같은 키를 그대로 읽는다',npath()===3&&K.s.length===3,[npath(),K.s.length]);
     await del('ink','bink:210');
     await bkGoto(210); await wait(1800);
     T('S-A 다른 쪽으로 가면 그 쪽 획으로 바뀐다(210 = 0획)',npath()===0,[npath(),bkCurPage()&&bkCurPage().pr]);
     await bkGoto(PG); await wait(1800);
     {const pg=bkCurPage(); if(pg){await zInkLoad(BK,pg); zInkPaint(BK,pg);} }
     let n3=0;while(n3++<40&&npath()!==3)await wait(200);
     T('S-A 돌아오면 다시 3획',npath()===3,npath());
     await del('ink','bink:'+PG);
     bkClose(); await wait(150);
   });

   /* ═══ B(3) 칩 · 고정 줄 ═══ */
   await grp('S-B3', async()=>{
     const r=DATA.find(x=>+x[F.BPAGE]>0)||DATA[0], uid=r[F.CODE], keep=BPG[uid];
     bpgWrite(uid,[208],208);
     T('S-B3 한 쪽이면 +N 없다',bookChip(r).indexOf('+')<0&&bookChip(r).indexOf('p208')>=0,bookChip(r));
     bpgWrite(uid,[208,210,240],208);
     T('S-B3 여러 쪽이면 📖 p208 +2',bookChip(r).indexOf('p208 +2')>=0,bookChip(r));
     T('S-B3 작은 칩도 +2',bookChipSm(r).indexOf('p208 +2')>=0,bookChipSm(r));
     T('S-B3 지학에서도 고치기 단추(#cBpg)가 칩에 붙는다',bookChip(r).indexOf('id="cBpg"')>=0,bookChip(r).slice(0,120));
     await openView(r[F.NO]); await wait(400);
     /* 문항을 열기만 해도 칩 줄이 그 문항 것으로 바뀌어야 한다 — bookOpen 이 안 불리는 길도 있다 */
     T('S-B3 ★고정 쪽 칩 셋이 교재 창 머리줄에 있다(2026-09-10 자리 옮김)',$$('#bpgChips .pin').length===3&&!$('#bpgChips').classList.contains('hide'),$$('#bpgChips .pin').length);
     await bookOpen(210); await wait(2600);
     T('S-B3 지금 보는 쪽 칩에 on',!!$('#bpgChips .pin.on')&&$('#bpgChips .pin.on').dataset.p==='210',$('#bpgChips .pin.on')&&$('#bpgChips .pin.on').dataset.p);
     T('S-B3 ps 안의 쪽으로 옮기면 last 가 따라간다',(BPG[uid]||{}).last===210,BPG[uid]);
     await bookOpen(2); await wait(2600);
     T('S-B3 ps 밖 쪽으로 넘겨 본 것은 기억하지 않는다',(BPG[uid]||{}).last===210,BPG[uid]);
     BPG[uid]={p:12,s:3};                      /* 옛 꼴은 last 를 안 붙인다(변환은 사용자가 고칠 때만) */
     await bookOpen(12); await wait(2600);
     T('S-B3 옛 꼴은 자동 변환하지 않는다',JSON.stringify(BPG[uid])==='{"p":12,"s":3}',BPG[uid]);
     if(keep!==undefined)BPG[uid]=keep;else delete BPG[uid];
     await saveBPG();
   });

   T('S-0 콘솔 오류 0',(window.__err||[]).length===0,window.__err);
  }catch(e){T('예외',false,String(e&&e.stack||e))}
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
                        STUB.replace('__SUBJ__', SUBJ) + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    html = html.replace('</body>', TESTS + '</body>', 1)
    open(os.path.join(OUT, 'app.html'), 'w', encoding='utf-8', newline='').write(html)
    shutil.copy(os.path.join(GIGU, '지학_서브노트_빈판_A3.pdf'), os.path.join(OUT, 'blank.pdf'))

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
    ix = lambda t: s.find(t)   # 없으면 -1 — 안 고친 판에서도 예외 없이 FAIL 로 적힌다
    blk = ix('\nif(CARD_LAYER){\n')
    T2('S-P 물리 무접촉 — bookChip/bookChipSm 은 카드 층 안이라 물리는 이 함수를 만들지도 않는다',
       blk >= 0 and ix('var bookChip=') > blk and ix('var bookChipSm=') > blk)
    T2('S-P 물리 갈래 본문은 글자까지 그대로(조건만 CUR.KINDS→CARD_LAYER)',
       'if(!CARD_LAYER)return r[F.BPAGE]?`<span class="tag page" data-page="${r[F.BPAGE]}">교재 ${r[F.BPAGE]}쪽</span>`:\'\';' in s
       and 'if(!CARD_LAYER)return r[F.BPAGE]?`<span class="tag page" data-page="${r[F.BPAGE]}">${r[F.BPAGE]}쪽</span>`:\'\';' in s
       and 'CUR.KINDS)return r[F.BPAGE]' not in s)
    T2('S-P 새 코드는 전부 if(CARD_LAYER) 안 (bpgList·bpgWrite·bpInk·bpgChips)',
       blk >= 0 and all(ix(k) > blk for k in ['function bpgList(', 'function bpgWrite(', 'async function bpInk(', 'function bpgChips(']))
    T2('S-P 잉크는 inkGet 으로만 잡는다 — bpInk 안에 get(\'ink\' 직접 호출 0',
       "await inkGet('bink:'+page,{w,h})" in s
       and (ix('async function bpInk(') < 0 or "get('ink'" not in s[ix('async function bpInk('):ix('function bpgChips(')]))
    T2('S-P 백틱 짝', s.count('`') % 2 == 0)
    npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
    for x in lines: print(x)
    print('\n== 옆칸잉크/교재쪽(%s) %d PASS / %d FAIL / %d항 ==' % (SUBJ, npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
