# -*- coding: utf-8 -*-
"""차례 단원순 · 목차 두 손잡이 · 부제 삭제 헤드리스 검산
(2026-09-07 · gigu/_task_jagwa_list_order.md §2)

  ① 1.1.10 이 1.1.2 뒤에 오는가(자연 정렬)
  ② 같은 단원 안에서 회차 → 문항 번호인가
  ③ 기출 0 단원 머리가 남는가
  ④ 거르개를 걸어도 정렬이 유지되는가(그때는 빈 단원 머리를 접는다)
  ⑤ 목차 글자 → 스크롤 · 필터 안 걸림
  ⑥ 목차 숫자 → 필터 걸림
  ⑦ 세 과목 머리에 부제가 없는가
  ＋ 게이트: 문항 수 합계 무변(지학 기출 319 · 확인 385 · 단원별 합 = 목차 값)

    PYTHONIOENCODING=utf-8 python _harness_order.py
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
OUT = os.path.join(os.environ.get('TEMP', '.'), 'ordh'); os.makedirs(OUT, exist_ok=True)

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
 const SUBJX='__SUBJ__';
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
 /* 목록에 그려진 차례대로 단원 코드를 뽑는다(머리 + 문항) */
 const listUnits=()=>$$('#list .grouphd.u').map(el=>el.dataset.uhd);
 const listItemUnits=()=>$$('#list > *').filter(el=>el.classList.contains('grouphd')&&el.classList.contains('u')||el.classList.contains('item'))
   .map(el=>el.classList.contains('item')?null:el.dataset.uhd);

 async function run(){
  try{
   localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}));
   for(let __i=0;__i<300&&(typeof db==='undefined'||!db);__i++)await wait(100);   /* ★ 2026-10-08 (_task_jagwa_phys_win) 고정 대기(load+600ms) 대신 IndexedDB(db)가 설 때까지(30 초 한도) — 짐이 크면 600ms 안에 안 열려 「db 없음」 예외(1 단계 셋 다) · 같은 판을 짐 적을 때 돌리면 정상(00:25 진단) */
   await loadEarthData(); draw(); await wait(80);
   T('O-0 카드 층으로 떴다 · 데이터 적재',CARD_LAYER===true&&DATA.length>0&&(TOC.list||[]).length>0,[SUBJ_ID,DATA.length,(TOC.list||[]).length]);

   /* ═══ ① 자연 정렬 ═══ */
   await grp('O-1', async()=>{
     T('O-1 unitCmp: 1.1.10 이 1.1.2 뒤',unitCmp('1.1.2','1.1.10')<0&&unitCmp('1.1.10','1.1.2')>0);
     T('O-1 unitCmp: 2.1.9 < 2.1.11 < 2.2.1 · 같으면 0',unitCmp('2.1.9','2.1.11')<0&&unitCmp('2.1.11','2.2.1')<0&&unitCmp('3.4.6','3.4.6')===0);
     T('O-1 unitCmp: 짧은 쪽이 앞(1.1 < 1.1.1)',unitCmp('1.1','1.1.1')<0);
     const U=unitOrder().map(x=>x.unit);
     const bad=[];for(let i=1;i<U.length;i++)if(unitCmp(U[i-1],U[i])>0)bad.push([U[i-1],U[i]]);
     T('O-1 unitOrder 가 통째로 오름차순',bad.length===0,bad.slice(0,5));
     const seq=U.filter(c=>c.indexOf('1.1.')===0);
     T('O-1 1.1.x 실물 차례에 1.1.10 이 1.1.2 뒤',(()=>{const a=seq.indexOf('1.1.2'),b=seq.indexOf('1.1.10');return a<0||b<0||a<b})(),seq);
   });

   /* ═══ ② 단원 안 회차·번호순 · 목록이 단원순 ═══ */
   await grp('O-2', async()=>{
     const shown=listUnits();
     const bad=[];for(let i=1;i<shown.length;i++)if(unitCmp(shown[i-1],shown[i])>0)bad.push([shown[i-1],shown[i]]);
     T('O-2 그려진 소단원 머리가 단원순',shown.length>0&&bad.length===0,[shown.length,bad.slice(0,4)]);
     T('O-2 소단원 머리가 단원마다 하나씩(중복 0)',new Set(shown).size===shown.length,shown.length-new Set(shown).size);
     const L=listSort(filtered());
     let ok=true,why=null;
     for(let i=1;i<L.length;i++){const a=L[i-1],b=L[i];
       if((unitOf(a[F.NO])||'')!==(unitOf(b[F.NO])||''))continue;
       const qa=+a[F.ROUND]||0,qb=+b[F.ROUND]||0,la=+a[F.LNO]||0,lb=+b[F.LNO]||0;
       /* ★ A-6(a) 9/30 — 회차가 찬 과목(HASROUND · 지학 · 9/21 부터 생물도)은 같은 단원 안 **회차 내림**(최신 회차가 위) → 문번 오름이다
          (gigu/_task_jagwa_earth_listpop.md §B 「같은 단원 안 차례를 회차 내림 → 문번 오름으로」 · genie a9f9fd4 · c9faff2 에서 ISEA → HASROUND · 앱 listSort) */
       if(((typeof HASROUND==='function'&&HASROUND())?qa<qb:qa>qb)||(qa===qb&&la>lb)){ok=false;why=[a[F.CODE],b[F.CODE]];break}}
     T('O-2 같은 단원 안에서 회차 → 문항 번호',ok,why);
     const codes=$$('#list .item .num').map(x=>x.textContent);
     T('O-2 회차순으로 안 늘어선다(G32-01·G32-02·G32-03 이 잇달아 오지 않음)',
       !(codes.indexOf('G32-01')>=0&&codes[codes.indexOf('G32-01')+1]==='G32-02'),codes.slice(0,6));
   });

   /* ═══ ③ 기출 0 단원 머리 ═══ */
   await grp('O-3', async()=>{
     const all=unitOrder().map(x=>x.unit), shown=listUnits();
     T('O-3 거르개 없을 때 목차의 모든 단원이 머리로 나온다',all.length===shown.length&&all.every((u,i)=>u===shown[i]),[all.length,shown.length]);
     const empties=$$('#list .grouphd.u').filter(el=>/(^|\D)0문항/.test(el.textContent));
     const notes=$$('#list .gh-empty').length;
     T('O-3 0문항 머리 뒤에 「기출이 없다」 줄',empties.length>0&&notes===empties.length,[empties.length,notes]);
     T('O-3 머리에 쪽수·문항 수가 붙는다',$$('#list .grouphd.u .p').length>=shown.length,[$$('#list .grouphd.u .p').length,shown.length]);
   });

   /* ═══ 게이트: 문항 수 합계 무변 ═══ */
   await grp('O-G', async()=>{
     const n0=filtered().length, items=$$('#list .item').length;
     T('O-G 그려진 문항 수 = filtered() 수(머리를 넣어도 문항은 안 는다/안 준다)',items===n0,[items,n0]);
     T('O-G #cnt 가 그 수를 말한다',$('#cnt').textContent.indexOf(String(n0))===0,$('#cnt').textContent);
     const T2=DATA.filter(showKind);
     const sum=unitOrder().reduce((a,u)=>a+T2.filter(r=>{const x=unitOf(r[F.NO]);return x===u.unit||x.indexOf(u.unit+'.')===0}).length,0);
     const un=T2.filter(r=>!unitRank()[unitOf(r[F.NO])||'']&&unitRank()[unitOf(r[F.NO])||'']!==0).length;
     T('O-G 단원별 합 + 목차 밖 = 전체',sum+un===T2.length,[sum,un,T2.length]);
   });

   /* ═══ ④ 거르개를 걸어도 정렬 유지 · 빈 머리는 접힘 ═══ */
   await grp('O-4', async()=>{
     const before=listUnits().length;
     FL.round=String(DATA.find(r=>r[F.ROUND])[F.ROUND]); draw(); await wait(40);
     const shown=listUnits();
     const bad=[];for(let i=1;i<shown.length;i++)if(unitCmp(shown[i-1],shown[i])>0)bad.push([shown[i-1],shown[i]]);
     T('O-4 회차 거르개를 걸어도 단원순 유지',bad.length===0&&shown.length>0,[shown.length,bad.slice(0,4)]);
     T('O-4 거르개가 걸리면 빈 단원 머리는 접힌다',shown.length<before&&$$('#list .gh-empty').length===0,[before,shown.length,$$('#list .gh-empty').length]);
     T('O-4 그려진 문항 수 = filtered()',$$('#list .item').length===filtered().length);
     FL.round=''; draw(); await wait(40);
     T('O-4 거르개를 풀면 빈 머리가 돌아온다',listUnits().length===before,[before,listUnits().length]);
   });

   /* ═══ ⑤⑥ 목차 두 손잡이 ═══ */
   await grp('O-5/6', async()=>{
     treeOpen(); await wait(60);
     /* 생물 목차는 2단(항목 = 절 자신)이라 .trit 줄이 0이다 — 그때는 절 줄을 집는다 */
     const rows=$$('#trlist .trit:not(.unm)').concat($$('#trlist .trsec'));
     const target=rows.find(el=>el.dataset.u&&$('#list [data-uhd="'+el.dataset.u+'"]'));
     /* ★ A-6(a) 9/30 — 옛 목차 서랍(#tree · 글자 = 스크롤 · 숫자 = 필터 두 손잡이)은 add9 §A-6 이 걷었다(genie 68216cf · _decisions 2026-09-21 15:44 ·
        수행 결과 §A 「treeOpen() 을 빈 함수 둘로 만들어 안 뜬다」 · 「목차」 단추 #btnTree 도 걷음) → 새 기대 = 옛 서랍 줄 0.
        목차의 「단원으로 가기」는 상주 서랍 단원 머리 줄(#ndList .ndsec · 누르면 첫 화면 목록이 그 절로 · add9 §A-3)이 갈음한다 — 숫자 = 필터 손잡이는 없다.
        옛 두 손잡이를 재던 아래 줄(O-5 둘로 갈림 · 숫자 너비 · 글자 클릭 · .at · O-6)은 옛 줄이 없어 건너뛴다(target 없음) */
     try{navBuild()}catch(e){}
     const nds=$$('#ndList .ndsec').filter(el=>el.dataset.sec&&$('#list [data-uhd="'+el.dataset.sec+'"]'));
     T('O-5 목차에서 목록과 이어지는 줄을 찾았다',rows.length===0&&nds.length>0,[rows.length,$$('#ndList .ndsec').length,nds.length]);
     if(!target)return;
     const code=target.dataset.u;
     T('O-5 목차 줄이 글자·숫자 둘로 갈렸다',!!target.querySelector('.tlab')&&!!target.querySelector('.n'),code);
     const nBox=target.querySelector('.n').getBoundingClientRect();
     T('O-5 숫자 영역 너비 ≥ 44',nBox.width>=44,[nBox.width,nBox.height]);
     const u0=FL.unit,n0=filtered().length;
     target.querySelector('.tlab').click(); await wait(400);
     const hd=$('#list [data-uhd="'+code+'"]');
     T('O-5 글자 클릭 → 필터 안 걸림(FL.unit·수 무변)',FL.unit===u0&&filtered().length===n0,[u0,FL.unit,n0,filtered().length]);
     T('O-5 글자 클릭 → 그 단원 머리로 스크롤(머리가 화면 안 · 머리 위에 .top 이 안 가림)',
       !!hd&&hd.getBoundingClientRect().top>=0&&hd.getBoundingClientRect().top<innerHeight,
       [code,hd&&hd.getBoundingClientRect().top,innerHeight,window.scrollY]);
     T('O-5 목차 그 줄에 지금 자리 표시(.at)',target.classList.contains('at')||!!$('#trlist .at'));
     treeOpen(); await wait(60);
     const t2=$('#trlist [data-u="'+code+'"]');
     t2.querySelector('.n').click(); await wait(80);
     T('O-6 숫자 클릭 → 종전 필터(FL.unit)',FL.unit===code,[FL.unit,code]);
     T('O-6 필터가 걸리면 목록도 그 단원만',filtered().every(r=>{const x=unitOf(r[F.NO]);return x===code||x.indexOf(code+'.')===0}),filtered().length);
     FL.unit=''; draw(); await wait(40);
   });

   /* ═══ ⑦ 부제 ═══ */
   await grp('O-7', async()=>{
     T('O-7 머리에 부제 노드가 없다',$$('.brand .sub').length===0&&$('.brand').textContent.indexOf('기본교재')<0,$('.brand').textContent.trim().slice(0,60));
     T('O-7 머리는 「자과 서재 · 과목」만',$('.brand h1').textContent==='자과 서재 · '+CUR.NAME,$('.brand h1').textContent);
   });

   T('O-0 콘솔 오류 0',(window.__err||[]).length===0,window.__err);
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
                        STUB.replace('__SUBJ__', SUBJ) + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    html = html.replace('</body>', TESTS.replace('__SUBJ__', SUBJ) + '</body>', 1)
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
    got = done.wait(int(os.environ.get('HARNESS_WAIT', '360'))); p.terminate(); print('elapsed %.0fs' % (_t.time() - _t0))
    try: p.wait(10)
    except Exception: p.kill()
    srv.shutdown()
    if not got:
        print('결과 없음 — 시간 안에 검사가 끝나지 않았다 · 마지막 중간 결과:'); print(box.get('partial', '(없음)')); sys.exit(1)
    lines = [ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()]

    def T2(name, cond, info=''):
        lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))

    s = open(SRC, encoding='utf-8').read()
    T2('O-7 부제 문자열이 파일에 없다(세 과목 공통 한 줄이었다)', '알기 쉬운 변리사' not in s)
    T2('O-7 죽은 CSS(.brand .sub) 도 안 남았다', '.brand .sub' not in s)
    # ★ A-6(a) 9/30 — 새 draw 셋째 줄이 두 번 바뀌었다: 두 모드(listpop §B · a9f9fd4 · `const L=_rnd?roundSort(filtered()):listSort(filtered())`)
    #   → 서랍과 같은 재료(add19 §A-1 · 0c19a60 · `const _s=shellL(), _rnd=_s.rnd;`) — 바뀐 셋째 줄은 빼고 머리 두 줄로 잰다(지금 판 1곳 · 층 표지 뒤 — 파이썬으로 셈)
    NEWDRAW = '\ndraw=function(){\n  drawFilters();drawSpectrum();\n'
    # ★ A-6(a) 9/30 — 셸 이식(c9faff2)부터 층 머리 = if(SHELL){ 라 옛 글자가 없어 s.index(BLK) 가 ValueError(242줄) · if(SHELL){ 은 층 앞(서랍 3724줄)에도 있어 층 표지로 잰다
    BLK = '/*EARTH:js*/'          # 카드 층 여는 줄(3340) — 3184 의 인라인 if 와 구분된다
    PHONE = '{const _drawP=draw;draw=function(){_drawP();foldSummary()}}'   # PHONE 절 껍데기(물리가 쓴다)
    T2('O-8 새 draw 는 카드 층 블록 안에 하나뿐(9/21 부터 if(SHELL) · c9faff2 §A)',
       s.count(NEWDRAW) == 1 and s.index(BLK) < s.index(NEWDRAW), [s.count(NEWDRAW)])
    T2('O-8 물리 draw 와 PHONE 껍데기는 그대로(카드 층 밖 · 무변)',
       'function draw(){' in s and PHONE in s and s.index(PHONE) < s.index(BLK))
    T2('O-8 백틱 짝', s.count('`') % 2 == 0)
    npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
    for x in lines: print(x)
    print('\n== 단원순/목차(%s) %d PASS / %d FAIL / %d항 ==' % (SUBJ, npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
