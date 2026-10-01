# -*- coding: utf-8 -*-
"""교재쪽 고정이 자동값을 이긴다 · 뷰어 「서재」 단추 자리 — 헤드리스 검산
(2026-09-07 · gigu/_task_jagwa_pan2_add1.md §3)

  P  지학 — 고정 없는 문항 전건 무변 · 고정한 문항은 고정한 쪽에만 · 여러 쪽 · 빈 ps · #bkQn ↔ 팝업
  B  생물 — BOOK_ROWS==='bpage' 갈래가 먼저 잡혀 결과 무변
  Y  물리 — BPG 를 비운 채로도 억지로 채운 채로도 결과가 같다(데이터로 보장)
  V  .vtop — pointer:coarse 에서 #vBack 이 56px 이상 오른쪽 · pointer:fine 에서 한 픽셀도 안 움직임
  S  원본 대조(파이썬) — 새 코드가 if(CARD_LAYER) 안에만 있는가

⚠ 픽셀 IDENTICAL 게이트는 쓰지 않는다(CLAUDE.md 「자과앱에는 픽셀 게이트를 걸지 않는다」).
   지시서 §3 의 픽셀 두 줄은 이 파일의 V 묶음(하네스 측정)으로 갈아 수행한다.

⚠ pointer:coarse 는 창 크기로 못 만든다. 헤드리스 창은 500px 아래로 안 줄고, 좁혀 봐야
   pointer 는 fine 이다. 크롬 실행 깃발 --blink-settings=primaryPointerType=2,... 로 만든다(실측).

    PYTHONIOENCODING=utf-8 python _harness_bookrows_pin.py            # 전부
    PYTHONIOENCODING=utf-8 python _harness_bookrows_pin.py vtop       # 묶음 하나만
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import http.server, os, socketserver, subprocess, sys, threading, hashlib, shutil, urllib.parse, json, time

GENIE = _roots.genie()
SRC = os.path.join(GENIE, 'jagwa', 'index.html')
SPDROOT = _roots.spd()
GIGU = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.environ.get('TEMP', '.'), 'brpin'); os.makedirs(OUT, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# 손가락 기기 흉내 — 1=none 2=coarse 4=fine (Blink PointerType) · 1=none 2=hover (HoverType)
COARSE = ['--blink-settings=primaryPointerType=2,availablePointerTypes=2,primaryHoverType=1,availableHoverTypes=1']

STUB = """<script>try{localStorage.setItem('subj','__SUBJ__')}catch(e){}</script>
<script>
window.katex={render:function(){},renderToString:function(s){return s}};window.renderMathInElement=function(){};
window.__err=[];
window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+(e.filename||'').split('/').pop()+':'+e.lineno)});
window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
</script>
"""

HEAD = r"""<script>
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
 async function run(){
  try{
   localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}));
"""

TAIL = r"""
   T('콘솔 오류 0',(window.__err||[]).length===0,window.__err);
  }catch(e){T('예외',false,String(e&&e.stack||e))}
  try{await __nativeFetch('/result',{method:'POST',body:R.join(String.fromCharCode(10))})}catch(e){}
 }
 if(document.readyState==='complete')setTimeout(run,600);else window.addEventListener('load',()=>setTimeout(run,600));
})();
</script>"""

# ═══════════════════════════ P. 지학 ═══════════════════════════
BODY_EARTH = r"""
   await loadEarthData(); draw(); await wait(80);
   T('P-0 지학 카드 층 · 데이터 적재',CARD_LAYER===true&&SUBJ_ID==='earth'&&DATA.length>0,[SUBJ_ID,DATA.length]);

   /* 고침 전 규약(판 1 = 네 갈래 합집합)을 그대로 옮겨 적은 것 — 이것과 대조한다 */
   const oldRows=page=>DATA.filter(r=>CUR.BOOK_ROWS==='bpage'?bpgList(r).indexOf(page)>=0:(r[F.BPAGE]===page||(isC(r)&&r[F.PG]===page)||(!isC(r)&&r[F.SOLPG]===page)||bpgList(r).indexOf(page)>=0));
   const num=v=>{const n=+v;return n>0?n:0};
   const PAGES=(()=>{const s=new Set();DATA.forEach(r=>{[num(r[F.BPAGE]),num(r[F.PG]),num(r[F.SOLPG])].forEach(p=>{if(p)s.add(p)})});return [...s].sort((a,b)=>a-b)})();
   const sig=(page,skipNo)=>bookRows(page).map(r=>r[F.NO]).filter(n=>n!==skipNo).join(',');
   const has=(page,r)=>bookRows(page).indexOf(r)>=0;
   const KEEP=JSON.parse(JSON.stringify(BPG));
   const restore=()=>{Object.keys(BPG).forEach(k=>delete BPG[k]);Object.assign(BPG,JSON.parse(JSON.stringify(KEEP)))};

   /* ═══ P-1 고정이 하나도 없으면 종전과 전건 같다 ═══ */
   let BASE={};
   await grp('P-1', async()=>{
     Object.keys(BPG).forEach(k=>delete BPG[k]);
     const bad=PAGES.filter(p=>sig(p)!==oldRows(p).map(r=>r[F.NO]).join(','));
     T('P-1 고정 0건이면 옛 규약과 쪽마다 전건 같다(수도 같다)',bad.length===0,[bad.slice(0,8),PAGES.length]);
     PAGES.forEach(p=>{BASE[p]=sig(p)});
   });

   /* 표본 — 기출(부록쪽 있음) 하나 · 확인(문제쪽 있음) 하나 · 셋 다 서로 다른 쪽 */
   const X=DATA.find(r=>!isC(r)&&num(r[F.BPAGE])>0&&num(r[F.SOLPG])>0&&num(r[F.SOLPG])!==num(r[F.BPAGE]));
   /* ⚠ 지학 확인문제는 교재쪽 = 문제쪽이다(704행 중 확인 385 전건 · 2026-09-07 실측).
      그래서 「PG 만 다른 확인문항」은 데이터에 없다 — 아래 P-2 는 PG(=BPAGE) 쪽에서 빠지는지로 잰다. */
   const C=DATA.find(r=>isC(r)&&num(r[F.BPAGE])>0&&num(r[F.PG])>0);
   const PIN=(()=>{let p=1;while(PAGES.indexOf(p)>=0)p++;return p})();   /* 아무 문항도 안 걸린 쪽 */

   /* ═══ P-2 고정한 문항은 고정한 쪽에만 · 옛 쪽에서 빠진다 ═══ */
   await grp('P-2', async()=>{
     Object.keys(BPG).forEach(k=>delete BPG[k]);
     T('P-2 표본 둘을 골랐다(기출·확인)',!!X&&!!C,[X&&X[F.NO],C&&C[F.NO],PIN]);
     const xb=num(X[F.BPAGE]), xs=num(X[F.SOLPG]);
     T('P-2 고치기 전 — 기출 표본이 교재쪽·부록쪽 둘 다에 있다',has(xb,X)&&has(xs,X),[xb,xs]);
     BPG[X[F.CODE]]={ps:[PIN],last:PIN};
     T('P-2 고정하면 고정한 쪽에 뜬다',has(PIN,X)&&bpgPinned(X)===true,[PIN,bookRows(PIN).length]);
     T('P-2 옛 자동값 쪽(BPAGE)에서 빠진다',!has(xb,X),xb);
     T('P-2 옛 부록쪽(SOLPG)에서 빠진다',!has(xs,X),xs);
     T('P-2 그 쪽 수도 하나 줄었다',bookRows(xb).length===oldRows(xb).length-1||xb===PIN,[bookRows(xb).length,oldRows(xb).length]);
     /* 다른 문항은 한 건도 안 움직인다 */
     const bad=PAGES.filter(p=>sig(p,X[F.NO])!==BASE[p].split(',').filter(n=>+n!==X[F.NO]).join(','));
     T('P-2 고정 없는 문항은 어느 쪽에서도 한 건도 안 움직인다',bad.length===0,bad.slice(0,8));

     const cb=num(C[F.BPAGE]), cp=num(C[F.PG]);
     T('P-2 지학 확인문제는 교재쪽 = 문제쪽이다(데이터 사실 · 전건)',
       DATA.filter(isC).every(r=>num(r[F.BPAGE])===num(r[F.PG])),
       [DATA.filter(isC).length,DATA.filter(r=>isC(r)&&num(r[F.BPAGE])!==num(r[F.PG])).length]);
     T('P-2 고치기 전 — 확인 표본이 교재쪽·문제쪽에 있다',has(cb,C)&&has(cp,C),[cb,cp]);
     BPG[C[F.CODE]]={ps:[PIN],last:PIN};
     T('P-2 확인문제도 옛 문제쪽(PG)에서 빠진다',has(PIN,C)&&!has(cb,C)&&!has(cp,C),[cb,cp,PIN]);
     restore();
   });

   /* ═══ P-3 여러 쪽을 고정하면 ps 의 모든 쪽에서 뜬다 ═══ */
   await grp('P-3', async()=>{
     Object.keys(BPG).forEach(k=>delete BPG[k]);
     const a=PIN, b=PIN+1, c=PIN+2, xb=num(X[F.BPAGE]), xs=num(X[F.SOLPG]);
     BPG[X[F.CODE]]={ps:[a,b,c],last:b};
     T('P-3 ps 의 세 쪽 전부에서 뜬다',has(a,X)&&has(b,X)&&has(c,X),[a,b,c]);
     T('P-3 그래도 옛 자동값·부록쪽에서는 빠진다',!has(xb,X)&&!has(xs,X),[xb,xs]);
     T('P-3 ps 밖의 쪽에서는 안 뜬다',!has(PIN+3,X));
     restore();
   });

   /* ═══ P-4 ps 가 빈 문항 · 옛 꼴 ═══ */
   await grp('P-4', async()=>{
     Object.keys(BPG).forEach(k=>delete BPG[k]);
     const xb=num(X[F.BPAGE]), xs=num(X[F.SOLPG]);
     BPG[X[F.CODE]]={ps:[]};
     T('P-4 ps 가 빈 배열이면 고정으로 안 친다(bpgPinned false)',bpgPinned(X)===false,BPG[X[F.CODE]]);
     T('P-4 그래서 종전과 같은 쪽에 뜬다(자동값으로 흘림)',has(xb,X)&&has(xs,X),[xb,xs]);
     const bad=PAGES.filter(p=>sig(p)!==BASE[p]);
     T('P-4 ps 가 비면 쪽마다 전건 고침 전과 같다',bad.length===0,bad.slice(0,8));
     BPG[X[F.CODE]]={p:12,s:3};
     T('P-4 옛 꼴 {p,s} 도 고정이다 — 12쪽에만',bpgPinned(X)===true&&has(12,X)&&!has(xb,X)&&!has(xs,X),[xb,xs]);
     /* bpgWrite 는 0 을 걸러 내므로 ps:[0] 을 만들 수 없다 — 그 꼴은 앱이 만들지 않는다 */
     delete BPG[X[F.CODE]];
     bpgWrite(X[F.CODE],[0,0],0);
     T('P-4 bpgWrite 는 0 만 든 ps 를 만들지 않는다(키를 지운다)',BPG[X[F.CODE]]===undefined);
     restore();
   });

   /* ═══ P-5 툴바 「문항 N」 과 「이 쪽의 문항」 팝업이 같은 수 ═══
      쪽은 208 로 못 박는다 — _harness_earth.py B-8 이 쓰는 쪽이라 조각 PDF 가 있는 것이 확인됐다. */
   await grp('P-5', async()=>{
     Object.keys(BPG).forEach(k=>delete BPG[k]);
     const xb=208;
     const n0=bookRows(xb).length;
     await bkOpen(xb); await wait(2500);
     let n=0; while(n++<60&&(!bkCurPage()||bkCurPage().pr!==xb))await wait(200);
     await bkGoto(xb); await wait(600);
     T('P-5 교재 모드가 그 쪽에 서 있다',!!bkCurPage()&&bkCurPage().pr===xb,[bkCurPage()&&bkCurPage().pr,xb]);
     T('P-5 툴바 「문항 N」 = bookRows',+$('#bkQn').textContent===n0,[$('#bkQn').textContent,n0]);
     $('#bkQ').click(); await wait(200);
     T('P-5 팝업 건수 = 툴바 수 = bookRows',!$('#bkq').classList.contains('hide')&&$$('#bkqList [data-no]').length===n0&&+$('#bkQn').textContent===n0,[$$('#bkqList [data-no]').length,$('#bkQn').textContent,n0]);
     /* 그 쪽 문항 하나를 딴 데로 고정하면 둘 다 하나 준다 */
     $('#bkqX').click();
     const Y=bookRows(xb)[0];
     BPG[Y[F.CODE]]={ps:[PIN],last:PIN};
     await bkGoto(xb); await wait(500);
     $('#bkQ').click(); await wait(200);
     T('P-5 그 쪽 문항 하나를 딴 쪽에 고정하면 툴바·팝업이 함께 하나 준다',
       +$('#bkQn').textContent===n0-1&&$$('#bkqList [data-no]').length===n0-1&&bookRows(xb).length===n0-1,
       [$('#bkQn').textContent,$$('#bkqList [data-no]').length,n0]);
     T('P-5 옮긴 문항은 옛 쪽 팝업에 없다',[...$$('#bkqList [data-no]')].every(el=>+el.dataset.no!==Y[F.NO]),Y[F.NO]);
     $('#bkqX').click(); bkClose(); restore();
   });
""" + r"""
   /* ═══ P-6 뷰어 「서재」 — 데스크톱(pointer:fine)에서 한 픽셀도 안 움직인다 ═══ */
   await grp('P-6', async()=>{
     T('P-6 이 판은 pointer:fine 이다',matchMedia('(pointer:fine)').matches&&!matchMedia('(pointer:coarse)').matches);
     $('#view').classList.remove('hide'); await wait(60);
     const b=$('#vBack').getBoundingClientRect();
     T('P-6 fine 에서 .vtop 왼쪽 안여백 10px · #vBack 왼쪽 10',
       getComputedStyle($('.vtop')).paddingLeft==='10px'&&Math.round(b.left)===10,
       [getComputedStyle($('.vtop')).paddingLeft,b.left]);
     $('#view').classList.add('hide');
   });
"""

# ═══════════════════════════ B. 생물 ═══════════════════════════
BODY_BIO = r"""
   await loadEarthData(); draw(); await wait(80);
   T('B-0 생물 카드 층 · 데이터 적재 · BOOK_ROWS==="bpage"',CARD_LAYER===true&&SUBJ_ID==='bio'&&DATA.length>0&&CUR.BOOK_ROWS==='bpage',[SUBJ_ID,DATA.length,CUR.BOOK_ROWS]);
   const oldRows=page=>DATA.filter(r=>CUR.BOOK_ROWS==='bpage'?bpgList(r).indexOf(page)>=0:(r[F.BPAGE]===page||(isC(r)&&r[F.PG]===page)||(!isC(r)&&r[F.SOLPG]===page)||bpgList(r).indexOf(page)>=0));
   const num=v=>{const n=+v;return n>0?n:0};
   const PAGES=(()=>{const s=new Set();DATA.forEach(r=>{[num(r[F.BPAGE]),num(r[F.PG]),num(r[F.SOLPG])].forEach(p=>{if(p)s.add(p)})});return [...s].sort((a,b)=>a-b)})();
   const sig=p=>bookRows(p).map(r=>r[F.NO]).join(',');
   const KEEP=JSON.parse(JSON.stringify(BPG));
   await grp('B-1', async()=>{
     const bad=PAGES.filter(p=>sig(p)!==oldRows(p).map(r=>r[F.NO]).join(','));
     T('B-1 있는 그대로 — 쪽마다 옛 규약과 전건 같다',bad.length===0,[bad.slice(0,8),PAGES.length]);
     /* 고정을 넣어도 첫 갈래가 먼저 잡는다 = 새 갈래에 닿지 않는다 */
     const X=DATA.find(r=>num(r[F.BPAGE])>0&&num(r[F.SOLPG])>0&&num(r[F.SOLPG])!==num(r[F.BPAGE]))||DATA[0];
     const PIN=(()=>{let p=1;while(PAGES.indexOf(p)>=0)p++;return p})();
     BPG[X[F.CODE]]={ps:[PIN],last:PIN};
     const bad2=PAGES.concat([PIN]).filter(p=>sig(p)!==oldRows(p).map(r=>r[F.NO]).join(','));
     T('B-1 고정을 넣어도 옛 규약과 전건 같다(첫 갈래가 먼저 잡는다)',bad2.length===0,bad2.slice(0,8));
     T('B-1 생물에서도 고정한 쪽에 뜬다(종전과 같음 — 첫 갈래가 bpgList 를 본다)',bookRows(PIN).indexOf(X)>=0);
     Object.keys(BPG).forEach(k=>delete BPG[k]);Object.assign(BPG,KEEP);
   });
"""

# ═══════════════════════════ Y. 물리 ═══════════════════════════
BODY_PHYS = r"""
   await wait(400); draw(); await wait(200);
   T('Y-0 물리 · 카드 층 아님',SUBJ_ID==='phys'&&CARD_LAYER===false,[SUBJ_ID,CARD_LAYER]);
   await grp('Y-1', async()=>{
     /* A-6(a) 9/30 — 카드 층 블록 문이 if(CARD_LAYER) → if(SHELL)(세 과목 참)로 바뀌어 물리에서도 만들어진다(_task_jagwa_shell_bio_phys §A · c9faff2) —
        물리 무변은 「교재 갈래 HASBOOK 이 거짓」(교재 창·📖 p 칩을 안 그린다)과 아래 Y-2(BPG 를 채워도 목록 글자 무변)로 선다 */
     T('Y-1 코드는 SHELL 블록이라 만들어져도 물리는 교재 갈래를 안 탄다 — HASBOOK=false',
       typeof HASBOOK!=='undefined'&&HASBOOK===false,
       [typeof bookRows,typeof bpgPinned,typeof bpgList]);
     T('Y-1 물리 SYNC_KEYS 에 bpg 가 없다 — BPG 가 기기에서 채워지지 않는다(데이터로 보장)',
       /* A-6(a) 9/30 — 뒤 판이 물리 SYNC_KEYS 끝에 gg·ggref 를 더했다(_task_jagwa_shell_bio_phys §E-7 · c9faff2) → 수 12 대신 옛 12키 앞자리 그대로 */
       SYNC_KEYS.indexOf('bpg')<0&&SUBJ.phys.SYNC_KEYS.indexOf('bpg')<0&&SYNC_KEYS.slice(0,12).join()==='status,note,qtype,conc,gpt,twin,ansfix,frm,maskpos,omrpos,mcard,link',[SYNC_KEYS.length,SYNC_KEYS]);
     T('Y-1 부팅 뒤 BPG 는 비어 있다',JSON.stringify(BPG)==='{}',BPG);
   });
   await grp('Y-2', async()=>{
     const before=$('#list').innerHTML, n0=$$('#list .item').length;
     T('Y-2 물리 목록이 그려졌다(DATA·.item·#cnt)',DATA.length>0&&n0>0,[DATA.length,n0,$('#cnt').textContent,before.slice(0,120)]);
     /* 억지로 채운다 — 물리 데이터라면 절대 생기지 않는 상태 */
     let k=0; DATA.forEach(r=>{if(k<50&&r&&r[F.CODE]){BPG[r[F.CODE]]={ps:[9999],last:9999};k++}});
     T('Y-2 BPG 를 억지로 채웠다(50건 시도)',k===50&&Object.keys(BPG).length>0,[k,Object.keys(BPG).length]);
     draw(); await wait(200);
     T('Y-2 채운 채로도 목록이 한 글자도 안 달라진다',$('#list').innerHTML===before&&$$('#list .item').length===n0,[$$('#list .item').length,n0,$('#list').innerHTML.length,before.length]);
     Object.keys(BPG).forEach(x=>delete BPG[x]);
     draw(); await wait(200);
     T('Y-2 다시 비워도 같다',$('#list').innerHTML===before);
   });
"""

# ═══════════════════════════ V. .vtop 자리 ═══════════════════════════
BODY_VTOP = r"""
   await wait(200);
   const coarse=matchMedia('(pointer:coarse)').matches, fine=matchMedia('(pointer:fine)').matches;
   T('V-0 __MODE__ 판이 맞다 — coarse=__WANT__',coarse===__WANT__&&fine===!__WANT__,[coarse,fine,innerWidth]);
   $('#view').classList.remove('hide'); await wait(80);
   const bk=$('#vBack'), b=bk.getBoundingClientRect(), pl=getComputedStyle($('.vtop')).paddingLeft;
   T('V-1 #vBack 이 떠 있다(크기 > 0)',b.width>10&&b.height>10,[b.width,b.height]);
   T('V-1 마크업 무변 — id·글자·class',bk.id==='vBack'&&bk.textContent==='서재'&&bk.className==='iconbtn',[bk.textContent,bk.className]);
   /* A-6(a) 9/30 — 뒤 판이 .vtop 에 둘을 더했다 — ⤢ 창↔전체 화면 #vWinTg(gigu/_task_jagwa_earth_listpop.md · a9f9fd4 · 타이머 뒤) · 필기 알약 #inkPill(_task_jagwa_earth_listpop_add2 §A-1
      「.vtop 안 · 제목 오른쪽 · 타이머 왼쪽 · 좁으면 둘째 줄로」 · 20a7128 flex-wrap·row-gap:6px · c9faff2 body[data-shell]) — 옛 여섯의 차례·칸 사이 8px 는 그대로 */
   T('V-1 .vtop 은 여전히 flex · 칸 사이 8px · 옛 단추 차례 그대로(+ 필기 알약·⤢ · 줄 사이 6px)',
     getComputedStyle($('.vtop')).display==='flex'&&getComputedStyle($('.vtop')).columnGap==='8px'&&getComputedStyle($('.vtop')).rowGap==='6px'&&
     [...$('.vtop').children].map(e=>e.id||e.className).join(',')==='vBack,title,vLink,inkPill,tm,vWinTg,vPrev,vNext',
     [getComputedStyle($('.vtop')).display,getComputedStyle($('.vtop')).gap,[...$('.vtop').children].map(e=>e.id||e.className).join(',')]);
   /* 가림 — 그 자리에서 맨 위가 #vBack 인가 */
   const els=document.elementsFromPoint(b.left+b.width/2,b.top+b.height/2);
   T('V-2 그 자리 맨 위가 #vBack 이다(무엇에도 안 가린다)',els[0]===bk,els.slice(0,4).map(e=>(e.tagName||'')+'#'+(e.id||'')));
   /* 눌리면 closeView 가 돈다 */
   /* A-6(a) 9/30 — 전역 closeView 는 뒤 판이 겹으로 갈아 끼웠다(c9faff2 shell_bio_phys §B-2 「#ggphys 걷기」 앱 8075 · 6c54347 bookwin §E 📍 「pinBar·pinPaint」 앱 9753) —
      #vBack.onclick 은 3540줄이 단 원본 closeView 그대로(무접촉 = S-7) · 전역과 같거나 원본 함수면 선다 */
   T('V-2 onclick 이 closeView 그대로',bk.onclick===closeView||/^function closeView\(/.test(String(bk.onclick)),String(bk.onclick).slice(0,40));
   bk.click(); await wait(80);
   T('V-2 누르면 뷰어가 닫힌다(closeView 가 돌았다)',$('#view').classList.contains('hide')&&VNO===null);
   try{await __nativeFetch('/vtop',{method:'POST',body:JSON.stringify({mode:'__MODE__',left:b.left,pl:pl,coarse:coarse,fine:fine,w:innerWidth})})}catch(e){}
"""


def build(mode):
    """모드별 app.html 을 만든다."""
    subj = {'earth': 'earth', 'bio': 'bio', 'phys': 'phys', 'fine': 'earth', 'coarse': 'earth'}[mode]
    body = {'earth': BODY_EARTH, 'bio': BODY_BIO, 'phys': BODY_PHYS}.get(mode)
    if body is None:
        body = BODY_VTOP.replace('__MODE__', mode).replace('__WANT__', 'true' if mode == 'coarse' else 'false')
    html = open(SRC, encoding='utf-8', newline='').read()
    html = html.replace('<script defer src="https://cdnjs', '<script defer data-off="https://cdnjs')
    html = html.replace('<link rel="stylesheet" href="https://cdnjs', '<link rel="off" href="https://cdnjs')
    html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js',
                        STUB.replace('__SUBJ__', subj) + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    html = html.replace('</body>', HEAD + body + TAIL + '</body>', 1)
    open(os.path.join(OUT, 'app.html'), 'w', encoding='utf-8', newline='').write(html)
    return subj


def run(mode, secs):
    """크롬 한 판. (결과줄 리스트, /vtop 로 온 값) 을 돌려준다."""
    subj = build(mode)
    spd = os.path.join(SPDROOT, subj)
    try: shutil.copy(os.path.join(GIGU, '지학_서브노트_빈판_A3.pdf'), os.path.join(OUT, 'blank.pdf'))
    except Exception: pass
    done = threading.Event(); box = {}

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=OUT, **k)
        def log_message(self, *a, **k): pass
        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            if p.startswith('/data/'):
                rel, pre = p[6:], subj + '/'
                if not rel.startswith(pre): self.send_response(404); self.end_headers(); return
                f = os.path.join(spd, rel[len(pre):].replace('/', os.sep))
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
            if self.path.startswith('/vtop'): box['vtop'] = json.loads(body); return
            box['txt'] = body; done.set()

    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    prof = os.path.join(OUT, 'prof_' + mode); shutil.rmtree(prof, ignore_errors=True)
    args = [CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--user-data-dir=' + prof,
            '--window-size=1400,900'] + (COARSE if mode == 'coarse' else []) + \
           ['http://127.0.0.1:%d/app.html' % port]
    t0 = time.time()
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    got = done.wait(secs); p.terminate()
    try: p.wait(10)
    except Exception: p.kill()
    srv.shutdown()
    print('  [%s] %.0fs' % (mode, time.time() - t0))
    if not got:
        return (['FAIL | %s 묶음이 시간 안에 안 끝났다 | %s' % (mode, box.get('partial', '(중간 결과 없음)')[-600:])], box.get('vtop'))
    return ([ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()], box.get('vtop'))


def static_checks():
    """원본 대조 — 없으면 -1 이라 안 고친 판에서도 예외 없이 FAIL 로 적힌다."""
    s = open(SRC, encoding='utf-8').read()
    ix = lambda t: s.find(t)
    out = []
    def T2(name, cond, info=''):
        out.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))
    # A-6(a) 9/30 — 카드 층 블록 문이 if(CARD_LAYER){ → if(SHELL){ 로 바뀌었다(_task_jagwa_shell_bio_phys §A · c9faff2) — 그 블록(/*EARTH:js*/ 바로 뒤)을 잡는다
    blk = s.find('\nif(SHELL){\n', ix('/*EARTH:js*/'))
    T2('S-1 새 갈래는 카드 층 블록 안이다(9/21 부터 if(SHELL) · c9faff2 §A)',
       blk >= 0 and ix('var bookRows=') > blk and ix('var bpgPinned=') > blk and ix('function bpgList(') > blk,
       [blk, ix('var bookRows='), ix('var bpgPinned=')])
    T2('S-2 bookRows 가 세 갈래다 · 고정 갈래에서 BPAGE·PG·SOLPG 를 안 본다',
       "var bookRows=page=>DATA.filter(r=>CUR.BOOK_ROWS==='bpage'?bpgList(r).indexOf(page)>=0:bpgPinned(r)?bpgList(r).indexOf(page)>=0:(r[F.BPAGE]===page||(isC(r)&&r[F.PG]===page)||(!isC(r)&&r[F.SOLPG]===page)));" in s)
    T2('S-3 옛 합집합 꼴(||bpgList) 이 남아 있지 않다', '||bpgList(r).indexOf(page)>=0' not in s)
    T2('S-4 주석의 「수는 늘 수만 있다」를 걷어내고 새 규약을 적었다',
       '수는 늘 수만 있다' not in s and '고정한 문항은 고정한 쪽에만 뜬다' in s)
    T2('S-5 bpgList·bpgOf·bpgWrite·bpgPinned 는 판 1 그대로(읽기만 했다)',
       "var bpgPinned=r=>{const o=BPG[r[F.CODE]];return !!(o&&(Array.isArray(o.ps)?o.ps.length:+o.p>0))};" in s
       and "function bpgList(r){const o=BPG[r[F.CODE]],auto=+r[F.BPAGE]>0?[+r[F.BPAGE]]:[];" in s
       and s.count('var saveBPG=()=>put(\'kv\',\'bpg\',BPG);') == 1)
    T2('S-6 .vtop 규칙은 pointer:coarse 안에만 있다 · 10px 그대로 · 56px 을 더한다',
       '@media (pointer:coarse){.vtop{padding-left:calc(env(safe-area-inset-left) + 66px)}}' in s
       and '.vtop{display:flex;align-items:center;gap:8px;padding:calc(env(safe-area-inset-top) + 7px) 10px 7px;' in s)
    T2('S-7 #vBack 마크업·onclick 무접촉',
       '<button class="iconbtn" id="vBack">서재</button>' in s and "$('#vBack').onclick=closeView;" in s)
    T2('S-8 판 2 자리(mcardWin·mcardSheet) 무접촉', s.count('mcardWin') >= 1 and s.count('mcardSheet') >= 1)
    T2('S-9 백틱 짝', s.count('`') % 2 == 0)
    return out


def main():
    want = [a for a in sys.argv[1:] if a in ('earth', 'bio', 'phys', 'vtop')] or ['earth', 'bio', 'phys', 'vtop']
    lines, vt = [], {}
    for mode in want:
        if mode == 'vtop':
            for m in ('fine', 'coarse'):
                ls, v = run(m, int(os.environ.get('HARNESS_WAIT', '180')))
                lines += ls
                if v: vt[m] = v
            f, c = vt.get('fine'), vt.get('coarse')
            def T2(name, cond, info=''):
                lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))
            T2('V-3 두 판 모두 값을 보냈다', bool(f and c), [f, c])
            if f and c:
                T2('V-3 pointer:coarse 에서 #vBack 이 56px 이상 오른쪽으로 간다',
                   c['left'] - f['left'] >= 56, [f['left'], c['left'], c['left'] - f['left']])
                T2('V-3 pointer:fine 에서는 한 픽셀도 안 움직인다 — 10px 그대로',
                   f['pl'] == '10px' and round(f['left']) == 10, [f['pl'], f['left']])
                T2('V-3 coarse 안여백 = 66px(10 + 56 · 안전영역 0)', c['pl'] == '66px', c['pl'])
                T2('V-3 창 너비는 두 판이 같다 — 자리가 바뀐 것은 폭이 아니라 미디어 규칙 때문',
                   f['w'] == c['w'], [f['w'], c['w']])
        else:
            secs = int(os.environ.get('HARNESS_WAIT', '420')) if mode == 'earth' else int(os.environ.get('HARNESS_WAIT_S', '240'))
            ls, _ = run(mode, secs)
            lines += ls
    lines += static_checks()
    npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
    for x in lines: print(x)
    print('\n== 교재쪽 고정/서재 단추 %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
