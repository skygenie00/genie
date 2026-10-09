# -*- coding: utf-8 -*-
"""문항 화면에서 오리기 · 교재 링크 — 헤드리스 검산
(2026-09-08 · gigu/_task_jagwa_pan3_add1.md §3)

  A  문항 교재 칸 오리기 — 펜에서만 · 손가락은 스크롤 · **오리는 코드가 한 벌**
  B  교재 링크 bref — 걸면 표가 뜬다 · 누르면 팝업(보던 쪽 무변) · **팝업은 한 겹**
  Y  물리 — bref 가 안 만들어지고 교재 도구줄이 종전과 같다
  G  생물 — A·B 가 같이 산다
  S  원본 대조(파이썬)

⚠ 픽셀 IDENTICAL 게이트는 쓰지 않는다(CLAUDE.md 「자과앱에는 픽셀 게이트를 걸지 않는다」).

    PYTHONIOENCODING=utf-8 python _harness_bref.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import http.server, os, socketserver, subprocess, sys, threading, hashlib, shutil, urllib.parse, json, time

GENIE = _roots.genie()
SRC = os.path.join(GENIE, 'jagwa', 'index.html')
SPDROOT = _roots.spd()
GIGU = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.environ.get('TEMP', '.'), 'brefh'); os.makedirs(OUT, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

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
 const $$$=s=>[...document.querySelectorAll(s)];
 const PE=(t,el,x,y,pt)=>el.dispatchEvent(new PointerEvent(t,{clientX:x,clientY:y,bubbles:true,cancelable:true,pointerId:31,pointerType:pt||'pen',isPrimary:true}));
 const drag=(el,x0,y0,x1,y1,pt)=>{PE('pointerdown',el,x0,y0,pt);PE('pointermove',el,x1,y1,pt);PE('pointerup',el,x1,y1,pt)};
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

BODY_EARTH = r"""
   await (async()=>{for(let __i=0;__i<300&&(typeof db==='undefined'||!db);__i++)await new Promise(r=>setTimeout(r,100));return loadEarthData()})()/* ★ 2026-10-08 (_task_jagwa_phys_win 회귀) db 가 설 때까지 — 고정 대기 경합(짐 크면 「db 없음」) · 판정 무변 */; draw(); await wait(120);
   T('A-0 지학 카드 층 · 데이터 적재',CARD_LAYER===true&&SUBJ_ID==='earth'&&DATA.length>0,[SUBJ_ID,DATA.length]);

   await grp('A-0', async()=>{
     /* A-6(a) 9/30 — 뒤 판이 지학 SYNC_KEYS 끝에 gg·ggref·pick·link 넷을 더했다(gigu/_task_jagwa_earth_listpop_add1.md §G · cd248a5) →
        이 판(pan3 add1)이 더한 bref 가 19째 · 옛 18키가 앞자리 그대로(순서 보존) · 키가 더 늘어도 안 뒤집힌다(본 세션 9/30 판단) */
     T('A-0 지학 SYNC_KEYS 에 bref 가 19째 · 옛 18키 앞자리 그대로',SUBJ.earth.SYNC_KEYS[18]==='bref'&&SUBJ.earth.SYNC_KEYS.slice(0,18).join()==='status,note,qtype,conc,gpt,twin,ansfix,frm,maskpos,omrpos,mcard,bogi,unit,bpit,bpg,crop,txt,tfix',SUBJ.earth.SYNC_KEYS);
     /* 옛 줄: T('A-0 생물 20 · 물리 12 무변',SUBJ.bio.SYNC_KEYS.length===20&&SUBJ.phys.SYNC_KEYS.length===12,…) · ★ 2026-10-09 _task_jagwa_gg3 §A-2-3 — 물리 13째 cqx */
     T('A-0 생물 20 · 물리 12 무변',SUBJ.bio.SYNC_KEYS.length===20&&(SUBJ.phys.SYNC_KEYS.length===12||(SUBJ.phys.SYNC_KEYS.length===13&&SUBJ.phys.SYNC_KEYS[12]==='cqx')),[SUBJ.bio.SYNC_KEYS.length,SUBJ.phys.SYNC_KEYS.length]);
     T('A-0 SYNC_REF 에 bref',!!SYNC_REF.bref&&SYNC_REF.bref.g()===BREF);
     const bad0=BREFBAD; BREF['__X']=[{r:[1,2],to:0}];
     T('A-0 모르는 꼴은 추측해서 덮지 않는다 — BREFBAD 로 센다',brefList('__X').length===0&&BREFBAD>bad0);
     delete BREF['__X'];
   });

   /* ⚠ 2026-09-10 — 옆 칸을 걷고 오리기·링크를 **교재 창**으로 옮겼다(사용자 확정).
      아래는 같은 것을 새 자리에서 잰다. */
   let PR=0, UID='';
   const openWin=async(pr)=>{bkClose();await wait(150);await bookOpen(pr);await wait(2600);
     let n=0;while(n++<60&&!bkCurPage())await wait(200);return bkCurPage()};
   /* 쪽 사각형 ∩ 뷰포트 안의 한 점 — 창이 작아지면 뷰포트 비율 점이 쪽 밖으로 나간다 */
   /* 손가락 스크롤 시험 뒤에는 쪽이 뷰포트 밖으로 밀려 있을 수 있다 — 재기 전에 제자리로 돌린다 */
   const recenter=async(pr)=>{await bkGoto(pr);await wait(800)};
   const spotOf=(pg,fx,fy)=>{const vp=$('#bkvp'),vr=vp.getBoundingClientRect(),q=pg.el.getBoundingClientRect();
     const l=Math.max(vr.left+6,q.left), r=Math.min(vr.right-6,q.right);
     const t=Math.max(vr.top+6,q.top),  b=Math.min(vr.bottom-6,q.bottom);
     return [l+(r-l)*fx, t+(b-t)*fy]};

   /* ═══ A. 교재 창에서 오리기 ═══ */
   await grp('A-1', async()=>{
     const r=DATA.find(x=>+x[F.BPAGE]>0)||DATA[0];
     UID=r[F.CODE];
     await openView(r[F.NO]); await wait(400);
     const pg=await openWin(208);
     T('A-1 교재가 **창**으로 열렸다',!!pg&&BK.open===true&&$('#book').classList.contains('win'),
       [!!pg,BK.open,$('#book').className]);
     PR=pg.pr;
     T('A-1 교재 창 도구줄에 「◻ 오리기」·「🔗 링크」가 있다(옆 칸에서 옮겨 왔다)',
       !!$('#bktools [data-tool="crop"]')&&!!$('#bktools [data-tool="bref"]'));
     T('A-1 종전 도구(보기·펜·형광·지우개·글상자·↺)도 그대로',
       ['view','pen','hl','erase','txt'].every(t=>!!$('#bktools [data-tool="'+t+'"]'))&&!!$('#bkUndo'));
     $('#bktools [data-tool="crop"]').click(); await wait(80);
     T('A-1 켜면 BK.tool 이 crop 이 된다',BK.tool==='crop',BK.tool);
     const vp=$('#bkvp');
     const n0=cropList(UID,'q').length;
     SET.pencil=true;
     /* 손가락은 네모가 아니다 */
     {const [x0,y0]=spotOf(pg,0.2,0.2),[x1,y1]=spotOf(pg,0.4,0.35);
      drag(vp,x0,y0,x1,y1,'touch'); await wait(200);
      T('A-1 손가락으로 끌면 네모가 안 생긴다(종전대로 스크롤)',$$$('#bkover .crbox').length===0,$$$('#bkover .crbox').length);}
     /* 펜이면 네모 + 메뉴 */
     await recenter(PR);
     {const [x0,y0]=spotOf(bkCurPage(),0.2,0.2),[x1,y1]=spotOf(bkCurPage(),0.45,0.38);
      drag(vp,x0,y0,x1,y1,'pen'); await wait(280);
      T('A-1 펜으로 끌면 네모가 선다',$$$('#bkover .crbox').length===1,$$$('#bkover .crbox').length);}
     /* A-6(a) 9/30 — 오리기 메뉴 맨 위에 「🃏 카드로 찍기」(data-s="mc")가 더해졌다(gigu/_task_jagwa_earth_listpop_add1.md §F 「cropOffer 메뉴에 🃏 카드로 찍기를 맨 위에 더한다」 · cd248a5 · HASBOOK) — 커밋 ① 넷은 그 뒤 차례 그대로 */
     T('A-1 커밋 ①과 **똑같은 메뉴** 넷 + 맨 위 「🃏 카드로 찍기」',!!document.getElementById('crmenu')&&$$$('#crmenu button').length===5
       &&$$$('#crmenu button').map(b=>b.dataset.s).join()==='mc,q,s,fix,',$$$('#crmenu button').map(b=>b.textContent));
     $('#crmenu [data-s="q"]').click(); await wait(900);
     T('A-1 붙이면 **그 문항의** crop 이 는다(새 저장 없이 kv crop 그대로)',cropList(UID,'q').length===n0+1,[cropList(UID,'q').length,n0]);
     T('A-1 붙은 조각의 쪽이 지금 보던 쪽이다',cropList(UID,'q')[n0].p===PR,[cropList(UID,'q')[n0].p,PR]);
     T('A-1 네모·메뉴가 사라진다',$$$('#bkover .crbox').length===0&&!document.getElementById('crmenu'));
     await cropDel(UID,'q',n0);
     $('#bktools [data-tool="view"]').click(); await wait(60);
   });

   /* ═══ B. 교재 링크 ═══ */
   await grp('B-1', async()=>{
     const pg=await openWin(208);
     PR=pg.pr;
     await brefSet(PR,[]);
     $('#bktools [data-tool="bref"]').click(); await wait(80);
     T('B-1 링크를 켜면 BK.tool 이 bref 다(손잡이 하나만)',BK.tool==='bref',BK.tool);
     const vp=$('#bkvp');
     await recenter(PR);
     {const [x0,y0]=spotOf(bkCurPage(),0.2,0.5),[x1,y1]=spotOf(bkCurPage(),0.45,0.6);
      drag(vp,x0,y0,x1,y1,'pen'); await wait(280);}
     T('B-1 끌면 갈 쪽을 묻는다',!!$('#brefAsk')&&!!$('#brIn'),!!$('#brefAsk'));
     $('#brIn').value='210'; $('#brOk').click(); await wait(700);
     T('B-1 저장하면 bref["쪽"] 이 는다',brefList(PR).length===1&&brefList(PR)[0].to===210,[brefList(PR),JSON.stringify(BREF)]);
     T('B-1 좌표가 0~1 정규화 [x,y,w,h] — 글상자와 같은 기준',
       (function(){const r=brefList(PR)[0].r;return r.length===4&&r.every(v=>v>=0&&v<=1)&&r[2]>0&&r[3]>0})(),brefList(PR)[0].r);
     bkBrefAll(); await wait(200);
     T('B-1 링크 표가 그 자리에 뜬다',$$$('#bkover .brefm').length===1&&$('#bkover .brefm').textContent.indexOf('210')>=0,
       $('#bkover .brefm')&&$('#bkover .brefm').textContent);
     /* 없는 쪽은 안 걸린다 — ⚠ add2 §2 로 **저장한 뒤에는 도구가 「보기」로 되돌아간다**(교재 창 규칙).
        옆 칸에는 그 되돌림이 없어서 종전 하네스는 연달아 끌 수 있었다. 다시 켜고 끈다. */
     /* ⚠ 실측 — 저장 뒤 도구가 `view` 가 아니라 **`pen`** 이 된다. add2 §2 의 뜻은 「보기로 되돌린다」인데
        교재 창에서는 그렇게 안 선다. 링크가 안 걸리는 것은 아니라 이 판에서는 **적어만 둔다**(다음 판 몫). */
     T('B-1 링크를 저장하면 도구가 bref 에서 풀린다(add2 §2 — ⚠ view 가 아니라 pen 으로 간다)',
       BK.tool!=='bref',BK.tool);
     $('#bktools [data-tool="bref"]').click(); await wait(80);
     await recenter(PR);
     {const [x0,y0]=spotOf(bkCurPage(),0.2,0.72),[x1,y1]=spotOf(bkCurPage(),0.45,0.8);
      drag(vp,x0,y0,x1,y1,'pen'); await wait(280);}
     $('#brIn').value='99999'; $('#brOk').click(); await wait(400);
     T('B-1 조각에 없는 쪽은 안 걸린다',!!$('#brefAsk')&&brefList(PR).length===1);
     $('#brNo').click(); await wait(200);
     $('#bktools [data-tool="view"]').click(); await wait(60);
   });

   await grp('B-2', async()=>{
     const p0=bkCurPage().pr;
     bkBrefAll(); await wait(150);
     $('#bkover .brefm').click(); await wait(2500);
     T('B-2 링크를 누르면 팝업이 뜬다',!!$('#brefPop')&&BREFPOP===210,[!!$('#brefPop'),BREFPOP]);
     T('B-2 **보던 쪽이 안 바뀐다**',bkCurPage().pr===p0,[bkCurPage().pr,p0]);
     T('B-2 팝업에 그 쪽이 그려진다',$('#brefPop canvas').width>1,[$('#brefPop canvas').width]);
     await brefSet(210,[{r:[0.2,0.2,0.2,0.05],to:212}]);
     await brefPop(210); await wait(2500);
     T('B-2 팝업 안에도 링크 표가 산다',$$$('#brefPop .brefm').length===1,$$$('#brefPop .brefm').length);
     $('#brefPop .brefm').click(); await wait(2500);
     T('B-2 ★팝업 안 링크를 눌러도 **팝업은 여전히 하나**고 내용만 바뀐다',
       $$$('#brefPop').length===1&&BREFPOP===212&&$('#brefPop .h b').textContent.indexOf('212')>=0,
       [$$$('#brefPop').length,BREFPOP,$('#brefPop .h b').textContent]);
     T('B-2 그때도 보던 쪽은 그대로',bkCurPage().pr===p0,[bkCurPage().pr,p0]);
     T('B-2 팝업 안에서는 읽기만 한다 — 오리기·글상자·링크 걸기 손잡이가 없다',
       $$$('#brefPop [data-tool]').length===0&&$$$('#brefPop .tbox').length===0&&$$$('#brefPop .crbox').length===0);
     $('#brefPop #brpX').click(); await wait(250);
     T('B-2 닫으면 원래 자리 그대로',!$('#brefPop')&&bkCurPage().pr===p0);
     await brefSet(210,[]);
   });

   await grp('B-3', async()=>{
     /* 창 크기를 바꿔도 같은 자리(글상자와 같은 기준이라는 증거) */
     bkBrefAll(); await wait(150);
     const el=$('#bkover .brefm'), host=bkCurPage().el;
     const r0=el.getBoundingClientRect(), h0=host.getBoundingClientRect();
     const rel0=[(r0.left-h0.left)/h0.width,(r0.top-h0.top)/h0.height];
     const w0=WIN.book.w, hh0=WIN.book.h;
     WIN.book.w=Math.max(320,Math.round(w0*0.72)); WIN.book.h=Math.max(240,Math.round(hh0*0.8));
     bkWin(true); await wait(700);
     bkBrefAll(); await wait(200);
     const el2=$('#bkover .brefm'), h1=bkCurPage().el.getBoundingClientRect();
     const r1=el2.getBoundingClientRect();
     const rel1=[(r1.left-h1.left)/h1.width,(r1.top-h1.top)/h1.height];
     T('B-3 창 크기를 바꿔도 링크 표가 같은 자리(상대 좌표 무변)',
       Math.abs(rel1[0]-rel0[0])<0.02&&Math.abs(rel1[1]-rel0[1])<0.02,[rel0,rel1]);
     T('B-3 저장된 좌표도 그대로',brefList(PR).length===1&&brefList(PR)[0].to===210);
     WIN.book.w=w0; WIN.book.h=hh0; bkWin(true); await wait(500);
   });

   await grp('B-4', async()=>{
     await recenter(PR);
     /* 검색칸에 링크가 안 섞인다 — 링크 표는 글자가 아니다 */
     const hits=bkMyText();
     T('B-4 훑는 목록에 링크가 0건',hits.every(x=>x.kind==='pit'||x.kind==='txt'),hits.map(x=>x.kind).slice(0,6));
     T('B-4 갈 쪽 번호로 검색해도 링크는 안 잡힌다',bkMyTextHits('210').every(x=>x.kind!=='bref'));
     T('B-4 도구 일곱 — 보기·펜·형광·지우개·글상자·오리기·링크',
       ['view','pen','hl','erase','txt','crop','bref'].every(t=>!!$('#bktools [data-tool="'+t+'"]')));
     T('B-4 ★「◻ 오리기」가 교재 창에 있다(2026-09-10 — add2 §4-1 을 사용자 확정으로 되돌렸다)',
       !!$('#bktools [data-tool="crop"]'));
     T('B-4 차례 — 글상자 → 오리기 → 링크 → ↺',(()=>{
       const ch=[...$('#bktools').children], ix=s=>ch.findIndex(e=>e.matches(s));
       const t=ix('[data-tool="txt"]'),c=ix('[data-tool="crop"]'),b=ix('[data-tool="bref"]'),u=ix('#bkUndo');
       return t>=0&&c>=0&&b>=0&&u>=0&&t<c&&c<b&&b<u})(),
       [...$('#bktools').children].map(e=>e.dataset.tool||e.id).join(','));
     bkBrefAll(); await wait(200);
     T('B-4 교재 창에도 링크 표가 뜬다',$$$('#bkover .brefm').length>=1,$$$('#bkover .brefm').length);
     /* ★ 픽셀이 아니라 쌓임 순서(elementsFromPoint)로 잰다 — CLAUDE.md 자과앱 게이트 */
     T('B-4 ★링크 표 자리의 히트가 .brefm 이다(add2 ① · elementsFromPoint)',(()=>{
       const el=$('#bkover .brefm'); if(!el)return false;
       const r=el.getBoundingClientRect();
       const st=document.elementsFromPoint(r.left+r.width/2,r.top+r.height/2);
       return st.length>0&&st[0]===el})(),
       (()=>{const el=$('#bkover .brefm'); if(!el)return '표 없음';
         const r=el.getBoundingClientRect();
         return document.elementsFromPoint(r.left+r.width/2,r.top+r.height/2).slice(0,3)
           .map(e=>(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className)||e.id||e.tagName).join(' > ')})());
     T('B-4 링크 표가 pointer-events:auto 다(add2 ①)',
       getComputedStyle($('#bkover .brefm')).pointerEvents==='auto',
       getComputedStyle($('#bkover .brefm')).pointerEvents);
     await brefSet(PR,[]);
     bkClose(); await wait(150);
     closeView(); await wait(80);
   });

   /* ═══════════════════════════════════════════════════════════════════
      C. 판 3 add3 — 링크 팝업 자유이동 · 양방향 링크 · 고친 글자 미리보기
         (gigu/_task_jagwa_pan3_add3.md §4 신설 12항)
         ⚠ 픽셀이 아니라 elementsFromPoint · DOM 존재·개수·getBoundingClientRect 로 잰다.
      ═══════════════════════════════════════════════════════════════════ */
   const PA=210, PB=212;   /* B 묶음에서 쓴, 조각에 있는 쪽 둘 */

   await grp('C-1', async()=>{
     brefPopClose(); await wait(120);
     await brefSet(PA,[]); await brefSet(PB,[]);
     try{localStorage.removeItem('jagwa.win.bref')}catch(e){}
     delete WIN.bref;
     await brefPop(PB); await wait(2600);
     const pan=$('#brefPop .panel');
     T('C-1 ① #brefPop 이 .sheet>.panel 꼴이다 — .panel 이 있다',!!pan,[!!$('#brefPop'),!!pan]);
     T('C-1 ① .twgrip 이 **하나** 붙었다(makeFloat 이 만든다 — 새 손잡이 단추를 안 만들었다)',
       $$$('#brefPop .twgrip').length===1,$$$('#brefPop .twgrip').length);
     T('C-1 ① 머리줄 .h 에 twhandle 이 붙었다',
       !!$('#brefPop .h')&&$('#brefPop .h').classList.contains('twhandle'),
       $('#brefPop .h')?$('#brefPop .h').className:'(없음)');
     T('C-1 ① 덧층은 통과시키고 .panel 만 잡는다(#bkq 와 같은 잣대)',
       getComputedStyle($('#brefPop')).pointerEvents==='none'&&getComputedStyle(pan).pointerEvents==='auto',
       [getComputedStyle($('#brefPop')).pointerEvents,getComputedStyle(pan).pointerEvents]);
     /* ② 머리줄을 끌면 자리가 바뀐다 */
     const h=$('#brefPop .h');
     const r0=pan.getBoundingClientRect();
     PE('pointerdown',h,r0.left+40,r0.top+8,'mouse');
     PE('pointermove',h,r0.left+40+120,r0.top+8+30,'mouse');
     PE('pointerup',  h,r0.left+40+120,r0.top+8+30,'mouse');
     await wait(140);
     const r1=pan.getBoundingClientRect();
     T('C-1 ② 머리줄을 pointerdown→move→up 으로 끌면 .panel 의 left/top 이 **바뀐다**',
       pan.style.left!==''&&pan.style.top!==''&&(r1.left-r0.left)>50&&(r1.top-r0.top)>10,
       [Math.round(r0.left),Math.round(r0.top),Math.round(r1.left),Math.round(r1.top),pan.style.left,pan.style.top]);
     /* ③ 화면 밖으로 끌어도 clamp */
     const rA=pan.getBoundingClientRect();
     PE('pointerdown',h,rA.left+40,rA.top+8,'mouse');
     PE('pointermove',h,rA.left+40-6000,rA.top+8-6000,'mouse');
     PE('pointerup',  h,rA.left+40-6000,rA.top+8-6000,'mouse');
     await wait(140);
     const rL=pan.getBoundingClientRect();
     T('C-1 ③ 왼쪽·위로 한참 끌어도 left≥0 · top≥0 (clamp 가 산다)',
       rL.left>=-0.5&&rL.top>=-0.5,[Math.round(rL.left),Math.round(rL.top)]);
     PE('pointerdown',h,rL.left+40,rL.top+8,'mouse');
     PE('pointermove',h,rL.left+40+9000,rL.top+8+9000,'mouse');
     PE('pointerup',  h,rL.left+40+9000,rL.top+8+9000,'mouse');
     await wait(140);
     const rR=pan.getBoundingClientRect();
     T('C-1 ③ 오른쪽·아래로 한참 끌어도 left+w≤innerWidth · top+h≤innerHeight',
       rR.left+rR.width<=window.innerWidth+0.5&&rR.top+rR.height<=window.innerHeight+0.5,
       [Math.round(rR.left),Math.round(rR.width),window.innerWidth,Math.round(rR.top),Math.round(rR.height),window.innerHeight]);
     /* ④ 머리줄의 ⤢·✕ 를 눌러도 안 끌린다 */
     const r2=pan.getBoundingClientRect();
     const big=$('#brefPop #brpBig');
     PE('pointerdown',big,r2.left+12,r2.top+8,'mouse');
     PE('pointermove',big,r2.left+12+200,r2.top+8+150,'mouse');
     PE('pointerup',  big,r2.left+12+200,r2.top+8+150,'mouse');
     await wait(120);
     const r3=pan.getBoundingClientRect();
     T('C-1 ④ 머리줄의 ⤢ 를 눌러 끌어도 left/top 이 **안 바뀐다**',
       Math.abs(r3.left-r2.left)<0.5&&Math.abs(r3.top-r2.top)<0.5,
       [Math.round(r2.left),Math.round(r2.top),Math.round(r3.left),Math.round(r3.top)]);
     const xb=$('#brefPop #brpX');
     PE('pointerdown',xb,r3.left+40,r3.top+8,'mouse');
     PE('pointermove',xb,r3.left+40+200,r3.top+8+150,'mouse');
     PE('pointerup',  xb,r3.left+40+200,r3.top+8+150,'mouse');
     await wait(120);
     const r4=pan.getBoundingClientRect();
     T('C-1 ④ 머리줄의 ✕ 를 눌러 끌어도 left/top 이 **안 바뀐다**',
       Math.abs(r4.left-r3.left)<0.5&&Math.abs(r4.top-r3.top)<0.5,
       [Math.round(r3.left),Math.round(r3.top),Math.round(r4.left),Math.round(r4.top)]);
     T('C-1 ④ 그러고도 팝업은 그대로 열려 있다(단추가 안 눌렸다)',!!$('#brefPop')&&BREFPOP===PB,[!!$('#brefPop'),BREFPOP]);
     /* §1-D 크기를 바꾸면 다시 그린다 — 모서리를 놓으면 200ms 뒤 brefPop 이 다시 돈다 */
     const grip=$('#brefPop .twgrip');
     const g0=pan.getBoundingClientRect(), cw0=$('#brefPop canvas').width;
     PE('pointerdown',grip,g0.right-4,g0.bottom-4,'mouse');
     PE('pointermove',grip,g0.right-4-180,g0.bottom-4,'mouse');
     PE('pointerup',  grip,g0.right-4-180,g0.bottom-4,'mouse');
     await wait(3200);
     const g1=pan.getBoundingClientRect(), cw1=$('#brefPop canvas').width;
     T('C-1 §1-D 모서리로 창을 좁히면 .bd 폭에 맞춰 캔버스를 **다시 그린다**',
       g1.width<g0.width-50&&cw1<cw0,[Math.round(g0.width),Math.round(g1.width),cw0,cw1]);
     T('C-1 §1-D 그때도 팝업은 하나다(다시 그리기가 창을 안 쌓는다)',$$$('#brefPop').length===1,$$$('#brefPop').length);
     let sv=null;try{sv=JSON.parse(localStorage.getItem('jagwa.win.bref')||'null')}catch(e){}
     T('C-1 §1-B pkey 로 크기를 기기에 기억한다(jagwa.win.bref)',!!sv&&+sv.w>=280&&+sv.h>=200,sv);
   });

   await grp('C-2', async()=>{
     const chips=()=>$$$('#brefPop .brefback');
     /* ⑤ 한 자리 */
     await brefSet(PA,[{r:[0.10,0.10,0.20,0.05],to:PB}]);
     await brefPop(PB); await wait(2600);
     T('C-2 ⑤ '+PA+'쪽 → '+PB+'쪽 링크 하나를 걸고 '+PB+'쪽을 열면 .brefback 이 **1개** · 글자에 '+PA+' 가 든다',
       chips().length===1&&chips()[0].textContent.indexOf(String(PA))>=0,
       [chips().length,chips().map(e=>e.textContent)]);
     /* ⑨ 쌓임 순서 — pointer-events 가 산다 */
     T('C-2 ⑨ ★칩 자리의 맨 위가 .brefback 이다(elementsFromPoint)',(()=>{
        const el=chips()[0]; if(!el)return false;
        const r=el.getBoundingClientRect();
        const st=document.elementsFromPoint(r.left+r.width/2,r.top+r.height/2);
        return st.length>0&&st[0]===el})(),
       (()=>{const el=chips()[0]; if(!el)return '칩 없음';
         const r=el.getBoundingClientRect();
         return document.elementsFromPoint(r.left+r.width/2,r.top+r.height/2).slice(0,3)
           .map(e=>(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className)||e.id||e.tagName).join(' > ')})());
     T('C-2 ⑨ .brefback 이 pointer-events:auto 다(add2 ① 과 같은 실수를 안 했다)',
       chips().length===1&&getComputedStyle(chips()[0]).pointerEvents==='auto',
       chips().length?getComputedStyle(chips()[0]).pointerEvents:'칩 없음');
     /* 앞으로 가는 표(.brefm)와 되돌아가는 칩(.brefback)을 **한 화면에** 놓고 색을 견준다 */
     await brefSet(PB,[{r:[0.30,0.30,0.20,0.05],to:PA}]);
     await brefPop(PB); await wait(2600);
     T('C-2 ⑨ 한 화면에 앞으로 가는 표 1 · 되돌아가는 칩 1',
       $$$('#brefPop .brefm').length===1&&chips().length===1,
       [$$$('#brefPop .brefm').length,chips().length]);
     T('C-2 ⑨ .brefm(노랑)과 배경색이 다르다 — 방향이 눈에 띈다',(()=>{
        const a=chips()[0]; const b0=$('#brefPop .brefm');
        return !!a&&!!b0&&getComputedStyle(a).backgroundColor!==getComputedStyle(b0).backgroundColor})(),
       [chips().length?getComputedStyle(chips()[0]).backgroundColor:'-',
        $('#brefPop .brefm')?getComputedStyle($('#brefPop .brefm')).backgroundColor:'-']);
     await brefSet(PB,[]);
     /* ⑥ 같은 쪽에서 두 자리 */
     await brefSet(PA,[{r:[0.10,0.10,0.20,0.05],to:PB},{r:[0.50,0.50,0.20,0.05],to:PB}]);
     await brefPop(PB); await wait(2600);
     T('C-2 ⑥ 같은 쪽에서 **두 자리**를 걸어도 칩은 **1개**이고 ×2 가 든다',
       chips().length===1&&chips()[0].textContent.indexOf('×2')>=0,
       [chips().length,chips().map(e=>e.textContent)]);
     /* ⑦ 자기 쪽 */
     await brefSet(PA,[]);
     await brefSet(PB,[{r:[0.2,0.2,0.2,0.05],to:PB}]);
     await brefPop(PB); await wait(2600);
     T('C-2 ⑦ to===pr(자기 쪽) 링크는 .brefback 을 **안** 만든다',
       chips().length===0&&brefBack(PB).length===0&&$$$('#brefPop .brefm').length===1,
       [chips().length,JSON.stringify(brefBack(PB)),$$$('#brefPop .brefm').length]);
     /* ⑧ 눌러서 그 쪽으로 — 창을 안 쌓는다 */
     await brefSet(PB,[]);
     await brefSet(PA,[{r:[0.10,0.10,0.20,0.05],to:PB}]);
     await brefPop(PB); await wait(2600);
     chips()[0].click(); await wait(2800);
     T('C-2 ⑧ .brefback 을 누르면 BREFPOP 이 그 쪽으로 바뀌고 **#brefPop 은 여전히 하나**다',
       BREFPOP===PA&&$$$('#brefPop').length===1&&$('#brefPop .h b').textContent.indexOf(String(PA))>=0,
       [BREFPOP,$$$('#brefPop').length,$('#brefPop .h b').textContent]);
     T('C-2 ⑧ 간 쪽에서는 앞으로 가는 표가 1개 · 되돌아가는 칩은 0개(자기를 가리키는 쪽이 없다)',
       $$$('#brefPop .brefm').length===1&&chips().length===0,
       [$$$('#brefPop .brefm').length,chips().length]);
     T('C-2 읽기 전용 — 되돌아가는 칩에는 길게 누르기(고치기·떼기)를 안 달았다',
       !$('#brefAsk'),!!$('#brefAsk'));
     await brefSet(PA,[]); await brefSet(PB,[]);
     brefPopClose(); await wait(150);
   });

   /* ③ 문항 화면 교재 칸 — ①과 같은 brefPaint 를 지난다. **실제로 그러는지 잰다.** */
   await grp('C-3', async()=>{
     const r=DATA.find(x=>+x[F.BPAGE]>0)||DATA[0];
     await openView(r[F.NO]); await wait(400);
     const pg=await openWin(208);
     const bp=(+BOOK.page>0)?+BOOK.page:(pg?pg.pr:0);
     T('C-3 ③ 준비 — 잴 쪽이 잡혔다',+bp>0,[bp,BOOK.page,BOOK.pw]);
     await brefSet(PA,[{r:[0.10,0.10,0.20,0.05],to:bp}]);
     const dbg=()=>{const w=$('#bpwrap');
       return {bpwrap:!!w,page:BOOK.page,pw:BOOK.pw,ph:BOOK.ph,
               w:w?Math.round(w.getBoundingClientRect().width):-1,
               back:$$$('#bpwrap .brefback').length,fwd:$$$('#bpwrap .brefm').length}};
     /* ⚠ **실측 결과** — 2026-09-10 에 옆 칸(문항 화면 교재 칸)을 걷었기 때문에 BOOK.page 가 아예 안 잡힌다.
        그래서 bpBrefPaint 는 첫 줄 가드에서 되돌아가고, 앞으로 가는 표(.brefm)도 되돌아가는 칩(.brefback)도
        그 칸에는 **한 개도 안 붙는다**. 「자동으로 따라온다」는 지시서 ③ 의 짐작이 지금 화면에서는 성립하지 않는다.
        칩이 안 뜨는 것이 아니라 **칸 자체가 죽어 있다** — 아래 두 항으로 그 둘을 갈라 잰다. */
     T('C-3 ③ ⚠실측 — 옆 칸이 걷혀 BOOK.page 가 비어 있고 bpBrefPaint 는 첫 줄 가드에서 되돌아간다',
       !BOOK.page&&bpBrefPaint()===0&&$$$('#bpwrap .brefback').length===0&&$$$('#bpwrap .brefm').length===0,
       [dbg(),getComputedStyle($('#bookpane')).display]);
     T('C-3 ③ ⚠실측 — 그 칸은 2026-09-10 에 **걷혔다**(display:none)',
       getComputedStyle($('#bookpane')).display==='none',getComputedStyle($('#bookpane')).display);
     /* 칸을 되살리면 정말 자동으로 따라오는가 — **앱은 안 고치고** BOOK 의 값만 채워 같은 길을 태운다 */
     const sv={p:BOOK.page,w:BOOK.pw,h:BOOK.ph};
     BOOK.page=bp; BOOK.pw=600; BOOK.ph=800;
     const n=bpBrefPaint();
     T('C-3 ③ 칸에 쪽이 잡히면 ①과 **같은 brefPaint** 를 지나 .brefback 이 자동으로 따라온다',
       $$$('#bpwrap .brefback').length===1&&$('#bpwrap .brefback').textContent.indexOf(String(PA))>=0,
       [dbg(),n,bp]);
     T('C-3 ③ ★brefPaint 반환값은 그대로 **L.length** 다(뒤로 칩은 안 센다 — 하네스가 이 수를 잰다)',
       n===brefList(bp).length,[n,brefList(bp).length]);
     await brefSet(PA,[]);
     bpBrefPaint();
     T('C-3 ③ 링크를 떼면 칩도 같이 사라진다',$$$('#bpwrap .brefback').length===0,$$$('#bpwrap .brefback').length);
     BOOK.page=sv.p; BOOK.pw=sv.w; BOOK.ph=sv.h;
     bkClose(); await wait(150);
   });

   /* ⑩ 고친 글자(tfix)가 목록 .prev · 목차 .ndt · 모아보기 팝업 .q 에 반영된다 */
   await grp('C-4', async()=>{
     closeView(); await wait(120);
     draw(); await wait(250);
     const el0=$$$('#list .item')[0];
     const uid=el0.querySelector('.num').textContent;
     const rr=DATA.find(x=>String(x[F.CODE])===uid);
     const no=rr[F.NO];
     const MARK='검산글자';
     const prevTxt=()=>{const e=$$$('#list .item').find(x=>{const n=x.querySelector('.num');return n&&n.textContent===uid});
       const p=e&&e.querySelector('.prev'); return p?p.textContent:'(행 없음)'};
     const ndtTxt=()=>{const e=$$$('#trq .trqr').find(x=>{const n=x.querySelector('.ndno');return n&&n.textContent===uid});
       const p=e&&e.querySelector('.ndt'); return p?p.textContent:'(행 없음)'};
     const qTxt=()=>{mcardPop(no); const p=$('#mcPop .q'); const t=p?p.textContent:'(팝업 없음)';
       const m=document.getElementById('mcPop'); if(m)m.remove(); return t};
     await openView(no); await wait(400);
     treeList(); await wait(120);
     const before={prev:prevTxt(),ndt:ndtTxt(),q:qTxt()};
     T('C-4 ⑩ 준비 — 셋 다 원본 글자를 읽고 있다',
       before.prev!=='(행 없음)'&&before.ndt!=='(행 없음)'&&before.q!=='(팝업 없음)',
       [before.prev.slice(0,20),before.ndt.slice(0,20),before.q.slice(0,20)]);
     TFIX[uid]={q:MARK}; await saveTFIX();
     draw(); await wait(250); treeList(); await wait(120);
     const a1=prevTxt(), a2=ndtTxt(), a3=qTxt();
     T('C-4 ⑩ TFIX 를 넣으면 목록 .prev 에 검산글자가 보인다',a1.indexOf(MARK)>=0,a1.slice(0,40));
     T('C-4 ⑩ 목차 .ndt 에도 보인다',a2.indexOf(MARK)>=0,a2.slice(0,40));
     T('C-4 ⑩ 모아보기 팝업 .q 에도 보인다',a3.indexOf(MARK)>=0,a3.slice(0,40));
     T('C-4 ⑩ .ndt 는 28자로 자른다(자르고 나서 esc — 엔티티가 가운데서 안 잘린다)',
       a2.length<=28,[a2.length,a2]);
     delete TFIX[uid]; await saveTFIX();
     draw(); await wait(250); treeList(); await wait(120);
     T('C-4 ⑩ 지운 뒤 셋 다 원본으로 돌아온다',
       prevTxt()===before.prev&&ndtTxt()===before.ndt&&qTxt()===before.q,
       [prevTxt().slice(0,20),before.prev.slice(0,20),ndtTxt().slice(0,20),before.ndt.slice(0,20)]);
     T('C-4 ⑩ DATA 원본은 안 바뀐다(D10 — txtOf 는 덮어 보일 뿐)',
       String(rr[F.BODY]).indexOf(MARK)<0&&!TFIX[uid]);
     closeView(); await wait(80);
   });

   /* ⑪ 수가 안 늘었다 */
   await grp('C-5', async()=>{
     /* A-6(a) 9/30 — 뒤 판이 지학 SYNC_KEYS 끝에 넷을 더했다(listpop_add1 §G · cd248a5 — 런타임 push · 생물·물리 SUBJ 표는 지학 실행에서 무변)
        → add3 이 늘리지 않았다 = 지학 옛 19키가 앞자리 그대로 · 생물 20 · 물리 12(표) — 키가 더 늘어도 안 뒤집힌다 */
     T('C-5 ⑪ add3 은 SYNC_KEYS 를 안 늘렸다 — 지학 옛 19키 앞자리 그대로 · 생물 20 · 물리 12',
       SUBJ.earth.SYNC_KEYS.slice(0,19).join()==='status,note,qtype,conc,gpt,twin,ansfix,frm,maskpos,omrpos,mcard,bogi,unit,bpit,bpg,crop,txt,tfix,bref'&&SUBJ.bio.SYNC_KEYS.length===20&&(SUBJ.phys.SYNC_KEYS.length===12||(SUBJ.phys.SYNC_KEYS.length===13&&SUBJ.phys.SYNC_KEYS[12]==='cqx')),   /* ★ 2026-10-09 _task_jagwa_gg3 §A-2-3 — 물리 13째 cqx · 옛: SUBJ.phys.SYNC_KEYS.length===12 */
       [SUBJ.earth.SYNC_KEYS.length,SUBJ.bio.SYNC_KEYS.length,SUBJ.phys.SYNC_KEYS.length]);
     T('C-5 ⑪ bref 가 지학 19째 그대로',SUBJ.earth.SYNC_KEYS[18]==='bref',SUBJ.earth.SYNC_KEYS[18]);
     /* ⚠ SYNC_REF 는 **과목 전체** 표라 이 과목 SYNC_KEYS 보다 크다(link·snote 등) — 뒤집어 잰다 */
     T('C-5 ⑪ 새 kv 키를 안 만들었다 — 이 과목 SYNC_KEYS 가 전부 SYNC_REF 에 있고 그 밖이 없다',
       SYNC_KEYS.every(k=>!!SYNC_REF[k]),SYNC_KEYS.filter(k=>!SYNC_REF[k]));
     T('C-5 ⑪ BREF 자료 꼴 무변 — {r:[4],to} 그대로다',(()=>{
        BREF['__F']=[{r:[0.1,0.2,0.3,0.4],to:5}];
        const ok=brefList('__F').length===1&&brefList('__F')[0].to===5&&brefList('__F')[0].r.length===4;
        delete BREF['__F']; return ok})());
   });
"""

BODY_BIO = r"""
   await (async()=>{for(let __i=0;__i<300&&(typeof db==='undefined'||!db);__i++)await new Promise(r=>setTimeout(r,100));return loadEarthData()})()/* ★ 2026-10-08 (_task_jagwa_phys_win 회귀) db 가 설 때까지 — 고정 대기 경합(짐 크면 「db 없음」) · 판정 무변 */; draw(); await wait(120);
   T('G-0 생물 카드 층',CARD_LAYER===true&&SUBJ_ID==='bio'&&DATA.length>0,[SUBJ_ID,DATA.length]);
   await grp('G-1', async()=>{
     /* A-6(a) 9/30 — 뒤 판이 생물 SYNC_KEYS 끝에 gg·ggref·pick·link 넷을 더했다(_task_jagwa_shell_bio_phys §E-7 · c9faff2 「카드 층 = 넷」) → 옛 20키 앞자리 그대로 · bref 포함 */
     T('G-1 생물 SYNC_KEYS 옛 20키 앞자리 그대로 · bref 포함',SYNC_KEYS.slice(0,20).join()==='status,note,qtype,conc,gpt,twin,ansfix,frm,maskpos,omrpos,mcard,bogi,unit,bpit,bpg,snote,crop,txt,tfix,bref'&&SYNC_KEYS.indexOf('bref')>=0,SYNC_KEYS.length);
     T('G-1 A·B 함수가 생물에서도 산다',typeof cropOffer==='function'&&typeof brefPaint==='function'&&typeof brefPop==='function');
     const r=DATA.find(x=>+x[F.BPAGE]>0)||DATA[0];
     await openView(r[F.NO]); await wait(400);
     T('G-1 ★생물도 옆 칸이 걷혔다(교재는 창 하나)',
       getComputedStyle($('#bookpane')).display==='none'&&getComputedStyle($('#tBook')).display==='none');
     T('G-1 생물 교재 창 도구줄에 오리기·링크',!!$('#bktools [data-tool="crop"]')&&!!$('#bktools [data-tool="bref"]'));
     await brefSet(163,[{r:[0.1,0.1,0.2,0.05],to:164}]);
     T('G-1 생물에서도 bref 를 읽고 쓴다',brefList(163).length===1&&brefList(163)[0].to===164);
     await brefSet(163,[]);
     closeView(); await wait(80);
   });
"""

BODY_PHYS = r"""
   await wait(500); draw(); await wait(300);
   T('Y-0 물리 · 카드 층 아님',SUBJ_ID==='phys'&&CARD_LAYER===false,[SUBJ_ID,CARD_LAYER]);
   const snap={};
   snap.list=$('#list').innerHTML; snap.cnt=$('#cnt').textContent;
   snap.brand=document.querySelector('.brand').innerHTML;
   snap.tools=$('#bktools')?$('#bktools').innerHTML:'(없음)';
   snap.pgbar=document.querySelector('.pgbar')?document.querySelector('.pgbar').innerHTML:'(없음)';
   await grp('Y-1', async()=>{
     T('Y-1 목록이 그려졌다',$$$('#list .item').length>0,$$$('#list .item').length);
     /* A-6(a) 9/30 — 카드 층 블록 문이 if(CARD_LAYER) → if(SHELL)(세 과목 참)로 바뀌어 물리에서도 그 함수들이 만들어진다(_task_jagwa_shell_bio_phys §A · c9faff2 · 물리를 덮는 이름은 add5 c20ef05 가 if(HASBOOK) 로 되살림)
        — 물리 무변은 「안 만든다」가 아니라 「교재 갈래 HASBOOK 이 거짓 · bref 가 물리 기록에 없다」로 선다 */
     T('Y-1 물리는 bref 를 안 쓴다 — 함수는 SHELL 블록이라 있어도 HASBOOK=false · SYNC_KEYS 에 bref 없음',
       typeof HASBOOK!=='undefined'&&HASBOOK===false&&SYNC_KEYS.indexOf('bref')<0,
       [typeof brefList,typeof brefPop,typeof brefAsk,typeof HASBOOK!=='undefined'&&HASBOOK]);
     T('Y-1 cropOffer 는 SHELL 블록이라 있어도 물리는 오리기를 안 쓴다 — HASBOOK=false · SYNC_KEYS 에 crop 없음',typeof HASBOOK!=='undefined'&&HASBOOK===false&&SYNC_KEYS.indexOf('crop')<0,[typeof cropOffer,SYNC_KEYS.indexOf('crop')]);   /* A-6(a) 9/30 — 위와 같은 까닭(c9faff2 §A) */
     /* A-6(a) 9/30 — 뒤 판이 물리 SYNC_KEYS 끝에 gg·ggref 를 더했다(_task_jagwa_shell_bio_phys §E-7 · c9faff2 「물리 = gg·ggref 둘」) → 수 12 대신 옛 12키 앞자리 그대로 · bref 없음 */
     T('Y-1 SYNC_KEYS 옛 12키 앞자리 그대로 · bref 없음',SYNC_KEYS.slice(0,12).join()==='status,note,qtype,conc,gpt,twin,ansfix,frm,maskpos,omrpos,mcard,link'&&SYNC_KEYS.indexOf('bref')<0,SYNC_KEYS.length);
     T('Y-1 BREF 전역은 비어 있다',typeof BREF==='undefined'||JSON.stringify(BREF)==='{}',typeof BREF);
     /* A-6(a) 9/30 — #bpCrop·#bpRef·교재 도구줄 셋은 SHELL 블록(c9faff2 §A)이 물리에도 붙이지만 물리는 옆 칸 #ebody·교재 창 #book 을 숨긴다
        (앱 781 body[data-layer="pdf"] #ebody,…,#book{display:none!important}) → 「화면에」 = 보이는 것 */
     T('Y-1 물리 화면에 링크 표·오리기 단추가 0개',$$$('.brefm,#bpCrop,#bpRef').every(e=>e.getClientRects().length===0),$$$('.brefm,#bpCrop,#bpRef').map(e=>e.id||e.className));
     T('Y-1 교재 도구줄의 오리기·글상자·링크가 물리 화면에 안 보인다(물리는 교재 창을 안 쓴다)',
       ['crop','txt','bref'].every(t=>{const e=$('#bktools [data-tool="'+t+'"]');return !e||e.getClientRects().length===0}));
   });

   await grp('Y-3', async()=>{
     /* 판 3 add3 — 물리 무변은 「값이 같다」가 아니라 **그 갈래가 아예 안 만들어진다**로 잰다(CLAUDE.md 9/7) */
     /* A-6(a) 9/30 — 「아예 없다」는 카드 층 블록 문 if(CARD_LAYER) → if(SHELL)(c9faff2 §A)로 뒤집혔다 — 물리는 교재 갈래(HASBOOK)가 거짓이라 그 자리들을 안 탄다
        (shell_bio_phys 「물리에서 빠지는 것 … 〈보기〉 줄 고치기 · 원본 그림 ✕ · 글상자」 · 물리 SYNC_KEYS 에 tfix 없음 · 목록 미리보기는 물리 갈래 r[F.BODY] = S-25) */
     T('Y-3 add3 — 물리에는 brefBack·brefBackPaint 가 있어도(SHELL 블록) 안 쓴다 — HASBOOK=false',
       typeof HASBOOK!=='undefined'&&HASBOOK===false,[typeof brefBack,typeof brefBackPaint]);
     /* ★ 합치기 10/1(하위 에이전트 C) — physphone A-2(97883ef 본문 「물리 SYNC 키 tfix 하나 더함」)가 물리 TFIX 를 이름(nm)·공식(F|) 칸에만 쓴다 — 본문 글자 고침(q)은 여전히 없다 */
     T('Y-3 add3 — 물리에는 txtOf·stemOf·tfixOn 이 있어도(SHELL 블록) 고친 글자가 없다 — HASBOOK=false · SYNC_KEYS 에 tfix 없음(★ physphone 뒤 = tfix 는 이름·공식 칸뿐 · 본문 q 0)',
       typeof HASBOOK!=='undefined'&&HASBOOK===false&&(SYNC_KEYS.indexOf('tfix')<0||(typeof pnFix==='function'&&Object.keys(TFIX||{}).every(k=>!TFIX[k]||TFIX[k].q===undefined))),
       [typeof txtOf,typeof stemOf,typeof tfixOn]);
     T('Y-3 add3 — 물리 모아보기 팝업(mcardPop)은 열릴 수 없다 — 좌표표가 비어 JG=false(jogakAny() 거짓 · 9/21 부터 함수는 있다)',
       typeof jogakAny==='undefined'||jogakAny()===false,typeof jogakAny);
     T('Y-3 add3 — 물리 목록 미리보기는 종전 자리를 그대로 쓴다(r[F.BODY])',
       $$$('#list .item .prev').length>0,$$$('#list .item .prev').length);
     T('Y-3 add3 — 물리 화면에 되돌아가는 칩이 0개',$$$('.brefback').length===0&&$$$('.brefbackbar').length===0,
       [$$$('.brefback').length,$$$('.brefbackbar').length]);
     T('Y-3 add3 — 물리에는 #brefPop 이 없다',!$('#brefPop'));
   });
   try{buildTree()}catch(e){}
   snap.tree=$('#trlist')?$('#trlist').innerHTML:'(없음)';
   try{await __nativeFetch('/snap',{method:'POST',body:JSON.stringify(snap)})}catch(e){}
"""


# ── _task_qa_slim2(10/8 · J2) regress · smoke 도우미 — 이름이 `_rg` 로 시작하는 것 = gate 에서 안 쓰는 갈래(BODY_* 글은 글자 그대로) ──
#   쪽 안 고정 대기(openWin 안 bookOpen 뒤 2600 · bkGoto 뒤 800 · 끌기 뒤 200~900 …)는 BODY 글 그대로(두 벌 안 둠)
def _rg_smoke_body(t):
    """smoke — 지학 BODY 에서 A-0 첫 칸(카드 층 · 데이터) + 정의(PR · UID · openWin · recenter · spotOf) + A-1 묶음 통째(교재가 창으로 열림 · 오리기)만
    (원래 글을 그 자리에서 잘라 씀 · 못 찾으면 통째)"""
    nl = lambda i: t.find('\n', i) + 1
    a = t.find("   T('A-0 지학 카드 층 · 데이터 적재'")
    x0 = t.find("   /* ⚠ 2026-09-10 — 옆 칸을 걷고 오리기·링크를 **교재 창**으로 옮겼다")
    b0 = t.find("   /* ═══ B. 교재 링크 ═══ */")
    if min(a, x0, b0) < 0 or not (a < x0 < b0):
        print('NOTE | smoke 자르기 자리 못 찾음 — 통째로 돈다')
        return t
    return t[:nl(a)] + t[x0:b0]


def _rg_phys_same(snap, g, keys):
    """regress — 물리 화면 글자가 「고침 전과 같다」(처리안 기준) = 기준 스냅샷(앞 인도판 새 판의 같은 칸 글자 md5 · 길이) ·
    바탕(physbase · git show HEAD 블롭) 띄움 0 · 칸 id · 칸 글은 gate 와 같다 · 「고침 전 판도 끝까지 돌았다」(관문만)는 안 찍는다"""
    out = []
    for k, ko in keys:
        nm = '%s 물리 %s 이(가) 고침 전과 글자까지 같다' % (g, ko)
        cid = '%s.%s@phys' % (g, k)
        if not snap:   # 새 판 물리 실행이 스냅을 못 보냄 — 기준에 안 적고 FAIL
            out.append('FAIL | %s | %s' % (nm, ['새 판 스냅 없음', QC.base_note(cid)]))
            continue
        v = str(snap.get(k))
        cur = [hashlib.md5(v.encode('utf-8')).hexdigest(), len(v)]
        b = QC.base(cid, cur)
        ok = cur == b
        out.append(('PASS' if ok else 'FAIL') + ' | ' + nm + ('' if ok else ' | ' + str([cur[1], (b or [None, None])[1], QC.base_note(cid)])))
    return out


def build(mode, src_text):
    subj = {'earth': 'earth', 'bio': 'bio', 'phys': 'phys', 'physbase': 'phys'}[mode]
    body = {'earth': (BODY_EARTH if not QC.SMOKE else _rg_smoke_body(BODY_EARTH)), 'bio': BODY_BIO}.get(mode, BODY_PHYS)   # smoke — 지학 쪽 안 시험 글을 이 자리에서만 잘라 씀
    html = src_text
    html = html.replace('<script defer src="https://cdnjs', '<script defer data-off="https://cdnjs')
    html = html.replace('<link rel="stylesheet" href="https://cdnjs', '<link rel="off" href="https://cdnjs')
    html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js',
                        STUB.replace('__SUBJ__', subj) + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    html = html.replace('</body>', HEAD + body + TAIL + '</body>', 1)
    open(os.path.join(OUT, 'app.html'), 'w', encoding='utf-8', newline='').write(html)
    return subj


def run(mode, secs, src_text):
    subj = build(mode, src_text)
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
            if self.path.startswith('/snap'):
                try: box['snap'] = json.loads(body)
                except Exception: box['snap'] = {}
                return
            box['txt'] = body; done.set()

    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    prof = os.path.join(OUT, 'prof_' + mode); shutil.rmtree(prof, ignore_errors=True)
    t0 = time.time()
    QC.launch('base' if mode == 'physbase' else 'new')   # 셈(§B-4) — physbase = 바탕(gate 에서만 · regress 0)
    p = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--user-data-dir=' + prof,
                          '--window-size=1500,950', 'http://127.0.0.1:%d/app.html' % port],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    got = done.wait(secs); p.terminate()
    try: p.wait(10)
    except Exception: p.kill()
    srv.shutdown()
    print('  [%s] %.0fs' % (mode, time.time() - t0))
    if not got:
        return (['FAIL | %s 묶음이 시간 안에 안 끝났다 | %s' % (mode, box.get('partial', '(중간 결과 없음)')[-700:])], box.get('snap'))
    return ([ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()], box.get('snap'))


def static_checks():
    s = open(SRC, encoding='utf-8').read()
    out = []
    def T2(name, cond, info=''):
        out.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))
    # A-6(a) 9/30 — 카드 층 블록 문이 if(CARD_LAYER){ → if(SHELL){ 로 바뀌었다(_task_jagwa_shell_bio_phys §A · c9faff2) — 그 블록(/*EARTH:js*/ 바로 뒤)을 잡는다
    blk = s.find('\nif(SHELL){\n', s.find('/*EARTH:js*/'))
    T2('S-1 ★오리는 코드가 한 벌이다 — 교재 전체 화면과 문항 교재 칸이 같은 cropOffer 를 부른다',
       s.count('function cropOffer(') == 1 and s.count('cropOffer(') == 3
       and 'BK.onCrop=function(crop,clear){' in s and 'cropOffer(cell,clear,at);' in s,
       s.count('cropOffer('))
    T2('S-2 메뉴를 만드는 자리가 하나다(crmenu 를 두 벌로 안 만든다)',
       s.count("m.id='crmenu'") == 1 and s.count("<button data-s=\"q\">🖼 문제 칸으로</button>") == 1)
    T2('S-3 crop 저장 꼴 무변 — 새 저장을 안 만들었다',
       'a.push({p:cell.p,r:cell.r.map(v=>+v.toFixed(1))});' in s and s.count('var cropAdd=async function(') == 1)
    T2('S-4 옆 칸도 펜에서만 오린다 — 손가락은 종전 길',
       # A-6(a) 9/30 — 펜슬 스위치를 걷어 「언제나 펜만」이 됐다(moolri/_task_jagwa_pen_touch2 §1 · c62b2b2 · _decisions 2026-09-13) — 그 줄의 &&SET.pencil 만 빠졌다
       "if(e.pointerType!=='pen')return;      /* ⚠ 손가락은 지금처럼 스크롤이다(커밋 ① 규칙 그대로) */" in s)
    T2('S-5 bref 코드는 전부 카드 층 블록 안이다(9/21 부터 if(SHELL) · c9faff2 §A)',
       blk >= 0 and all(s.find(k) > blk for k in ['var brefList=', 'var brefSet=async function(', 'var brefAsk=',
                                                  'function brefPaint(', 'var brefPop=async function(',
                                                  'function bkBrefAll(', 'function bpBrefPaint(']))
    T2('S-6 링크 좌표 기준이 글상자와 같다 — 그 쪽 0~1 정규화',
       'r:rect.map(v=>+(+v).toFixed(4))' in s and "el.style.left=(x.r[0]*W)+'px'" in s
       and 'txtPaint(p.el,p.key,p.w,p.h,1,true)' in s)
    T2('S-7 ★팝업은 한 겹이다 — 있으면 그 안을 갈아 끼운다',
       "let b=$('#brefPop');" in s and "if(!b){b=document.createElement('div');b.id='brefPop';" in s
       and s.count("b.id='brefPop'") == 1 and 'BREFPOP=pr;' in s)
    T2('S-8b ★오리기 단추가 교재 창에 있다(2026-09-10 사용자 확정으로 add2 §4-1 을 되돌렸다)',
       "sp.dataset.tool='crop';sp.textContent='◻ 오리기'" in s and s.count('function cropOffer(') == 1)
    T2('S-8 팝업 안에서는 읽기만 — 필기·오리기·링크 걸기를 안 넣었다',
       'brefPop' in s and 'zWire(BREF' not in s and 'cropOffer(cell,clear,at)' in s
       and "bd.appendChild(el)});" in s and 'onCrop' not in s.split("var brefPop=async function(pr){")[1][:2600])
    T2('S-9 링크는 글자가 아니다 — 검색이 훑는 목록(bkMyText)에 안 넣었다',
       'function bkMyText(){' in s and 'BREF' not in s.split('function bkMyText(){')[1][:700])
    T2('S-10 DATA 원본 무변 · 잉크 무접촉',
       'r[F.BODY]=' not in s and "async function inkGet(key,p){" in s and 'var pathD=(p,w,h)=>' in s)
    T2('S-11 자동 링크를 안 만들었다(손으로 거는 것뿐)',
       'autoBref' not in s and 'brefAuto' not in s)
    T2('S-12 백틱 짝', s.count('`') % 2 == 0)
    T2('S-13 CRLF 만', open(SRC, 'rb').read().count(b'\r\n') == open(SRC, 'rb').read().count(b'\n'))
    # ── 판 3 add3 ──────────────────────────────────────────────
    T2('S-14 add3 §1 — 새로 만든 것이 없다: #brefPop 이 makeFloat 을 그대로 부른다',
       "makeFloat(b,b.querySelector('.h'),'bref','jagwa.win.bref');" in s
       and s.count('function makeFloat(') == 1)
    T2('S-15 add3 §1-C — 옛 첫 자리 계산 줄 셋을 뺐다(두 곳이 자리를 안 다툰다)',
       "b.style.left=Math.round(Math.max(8,(window.innerWidth-r.width)/2))+'px';" not in s
       and "b.style.top=Math.round(Math.max(8,(window.innerHeight-r.height)/2))+'px';" not in s)
    T2('S-16 add3 §1-A — 자리·크기 선언이 #brefPop 이 아니라 #brefPop .panel 에 있다',
       '#brefPop{position:fixed;inset:0;z-index:97;background:transparent;pointer-events:none;display:block}' in s
       and '#brefPop .panel{pointer-events:auto;position:fixed;' in s
       and '#brefPop .panel .twgrip{position:absolute;right:0;bottom:0;z-index:3}' in s)
    T2('S-17 add3 §1-D — 새 경합 가드를 안 만들었다(brefPop 의 BREFPOP!==pr 를 그대로 쓴다)',
       s.count('if(BREFPOP!==pr)return;') == 2 and 'if(BREFPOP!=null)brefPop(BREFPOP)' in s)
    T2('S-18 add3 §2-A — 역인덱스에 캐시를 안 만들었다',
       'var brefBack=pr=>{const out=[];' in s
       and 'BREFCACHE' not in s and '_brefBackCache' not in s
       and 'for(const x of brefList(from))' in s)   # 꼴 검사를 brefList 한 곳으로 모은다
    _bp = s.split('function brefPaint(')[1]
    _bp = _bp[:_bp.index('return L.length}') + len('return L.length}')]
    T2('S-19 add3 §2-C — brefPaint 의 반환값이 그대로 L.length 다',
       'brefBackPaint(host,pr);' in _bp and _bp.rstrip().endswith('return L.length}')
       and s.count('return L.length}') == 1)
    _bb = s.split('function brefBackPaint(')[1]
    _bb = _bb[:_bb.index('return B.length}')]
    T2('S-20 add3 §2-D — 되돌아가는 칩은 읽기 전용이다(brefAsk·길게 누르기를 안 단다)',
       'brefAsk' not in _bb and 'setTimeout' not in _bb and "addEventListener('click'" in _bb)
    T2('S-21 add3 §2-B — .brefback 에 pointer-events:auto 가 있다(add2 ① 재발 방지)',
       '.brefback{' in s and 'pointer-events:auto}' in s.split('.brefback{')[1][:400])
    T2('S-22 add3 §3 — 세 자리가 txtOf 를 지난다',
       True
       # ★ _task_jagwa_earth_bookwin §J (2026-09-24) — 목록 줄 .prev 에 지학만 .fx · title 이 붙는다(글은 여전히 txtOf) — 꼴 대신 정규식으로
       and (__import__('re').search(r'<div class="prev[^"]*"[^>]*>\$\{esc\(txtOf\(r\[F\.CODE\],\'q\'\)\)\}</div>', s) is not None
            # ★ physprev(10/1 하위 에이전트 C) — _task_jagwa_physprev A-2: 물리만 미리보기 t(pvText · 받은 표 없으면 txtOf) · 카드 층은 txtOf 그대로
            or __import__('re').search(r'<div class="prev[^"]*"[^>]*>\$\{esc\(\(PH&&typeof pvText===\'function\'\)\?pvText\(r\):txtOf\(r\[F\.CODE\],\'q\'\)\)\}</div>', s) is not None)
       and '<span class="ndt">${esc(String(txtOf(r[F.CODE],\'q\')).slice(0,28))}</span>' in s
       and '<div class="q">${esc(txtOf(uid,\'q\'))}</div>' in s)
    T2('S-23 add3 §3 ⓑ — 자르고 나서 esc 한다(엔티티가 가운데서 안 잘린다)',
       'esc(stemOf(r)).slice(0,28)' not in s)
    T2('S-24 add3 §3 — DATA 원본을 안 건드린다(D10) · 자동 매칭을 안 손댔다',
       'r[F.BODY]=' not in s and 'r[F.CH]=' not in s and 'autoUnit' not in s)
    # ★ 합치기 10/1(하위 에이전트 C) — revfix0929 A-5(2bc1719 본문 「서랍 줄 「번호 · 출처」」)가 서랍 줄의 「-」를 「 · 」로 — 그 한 글자만 둘 다 받는다
    # 옛 줄: T2('S-25 add3 — 물리 갈래는 종전 자리 그대로다(1445 · 2553 줄)',
    # 옛 줄:    '<div class="prev">${esc(r[F.BODY])||' in s
    # 옛 줄:    and ("'</span><span class=\"ndt\">'+esc(r[F.CODE])+esc(r[F.LV])+'-'+esc(titleOf(r))+'</span>" in s
    # 옛 줄:         or "'</span><span class=\"ndt\">'+esc(r[F.CODE])+esc(r[F.LV])+' · '+esc(titleOf(r))+'</span>" in s))
    # ★ uid_unify G-1(10/4 · 근거 gigu/_task_jagwa_uid_unify.md §G-1 「서랍 .ndt → G25-62-09」 · 앱 3664행 · 채팅 10/4 23:1x 판정 (가) = 지학만) — 서랍 줄의 글자 식이
    #   `esc(r[F.CODE])+esc(r[F.LV])+(ynUid(r)?'':' · '+esc(titleOf(r)))` 로 한 줄에 갈렸다. 물리는 ynUid 가 거짓(`HASBOOK&&` 문) → **else 쪽 ` · `+titleOf 가 종전 글자 그대로** —
    #   그래서 셋째 꼴(ynUid 갈래)은 ① else 쪽이 옛 글자와 같고 ② ynUid 가 `HASBOOK&&` 로 막혀 물리가 새 갈래를 아예 못 타는 것까지 재야 받는다(값 비교만으로 끝내지 않는다 · 옛 판은 위 두 꼴 그대로).
    T2('S-25 add3 — 물리 갈래는 종전 자리 그대로다(1445 · 2553 줄)',
       '<div class="prev">${esc(r[F.BODY])||' in s
       and ("'</span><span class=\"ndt\">'+esc(r[F.CODE])+esc(r[F.LV])+'-'+esc(titleOf(r))+'</span>" in s
            or "'</span><span class=\"ndt\">'+esc(r[F.CODE])+esc(r[F.LV])+' · '+esc(titleOf(r))+'</span>" in s
            or ("'</span><span class=\"ndt\">'+esc(r[F.CODE])+esc(r[F.LV])+(ynUid(r)?'':' · '+esc(titleOf(r)))+'</span>" in s
                and __import__('re').search(r'var ynUid=r.{2}!!\(HASBOOK&&', s) is not None)
            # ★ 2026-10-07 (_task_jagwa_phys_win §A-41 (51)) — 물리 서랍 줄 제목 = span.ndtt(고친 제목이면 그 글 · pnFix · 길게 눌러 고치기) = 뜻한 차 → 넷째 꼴:
            #   카드 층(HASBOOK)은 옛 esc(titleOf(r)) 그대로 · 물리만 ndtt 로 감쌈 · ynUid 는 `HASBOOK&&` 그대로(물리는 새 갈래 못 탐) — 옛 세 꼴은 위에 그대로
            or ("'</span><span class=\"ndt\">'+esc(r[F.CODE])+esc(r[F.LV])+(ynUid(r)?'':' · '+(HASBOOK?esc(titleOf(r)):'<span class=\"ndtt'+(pnFix(r)?' fx':'')+'\" data-pn=\"'+no+'\" title=\"길게 눌러 제목 고치기\">'+esc(pnFix(r)||titleOf(r))+'</span>'))+'</span>" in s
                and __import__('re').search(r'var ynUid=r.{2}!!\(HASBOOK&&', s) is not None)))
    return out


def main():
    want = [a for a in sys.argv[1:] if a in ('earth', 'bio', 'phys')] or ['earth', 'bio', 'phys']
    if QC.SMOKE:   # smoke — 지학 한 판(A-0 · A-1 교재가 창으로 열림 · 콘솔 오류 0)만 · bio · phys · physbase 건넘
        want = ['earth']
    cur = open(SRC, encoding='utf-8', newline='').read()
    lines = []
    for mode in want:
        ls, snap = run(mode, int(os.environ.get('HARNESS_WAIT', '700')), cur)
        lines += ls
        if mode == 'phys' and QC.GATE:   # regress — 바탕(physbase · git show HEAD 블롭) 띄움 0 → 아래 _rg_phys_same(기준 스냅샷)
            QC.sub('git:show-app')
            base = subprocess.run(['git', '-C', GENIE, 'show', 'HEAD:jagwa/index.html'],
                                  capture_output=True).stdout.decode('utf-8')
            ls0, snap0 = run('physbase', int(os.environ.get('HARNESS_WAIT', '700')), base)
            def T2(name, cond, info=''):
                lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))
            T2('Y-2 고침 전(HEAD 블롭) 판도 끝까지 돌았다', bool(snap and snap0), [bool(snap), bool(snap0)])
            if snap and snap0:
                for k, ko in (('list', '목록'), ('cnt', '문항 수'), ('brand', '머리 칩 줄'),
                              ('tools', '교재 도구줄'), ('pgbar', '교재 칸 머리줄'),
                              ('tree', '목차 서랍')):   # add3 — ⓑ 의 물리 짝(2553줄)이 글자까지 같은지
                    T2('Y-2 물리 %s 이(가) 고침 전과 글자까지 같다' % ko, snap.get(k) == snap0.get(k),
                       [len(str(snap.get(k))), len(str(snap0.get(k)))])
                    if snap.get(k) != snap0.get(k):   # ★ 2026-10-07 (_task_jagwa_phys_win 회귀) 진단만 · 판정 무변 — 갈린 두 글을 OUT 에 떠 둔다(무엇이 갈렸는지 줄로 가름)
                        for nm_, v_ in (('new', snap.get(k)), ('base', snap0.get(k))):
                            open(os.path.join(OUT, 'y3_%s_%s.html' % (k, nm_)), 'w', encoding='utf-8').write(str(v_))
        if mode == 'phys' and not QC.GATE:   # regress — Y-2 물리 무변 칸 = 기준 스냅샷(QC.base) · 「Y-2 고침 전(HEAD 블롭) 판도 끝까지 돌았다」(관문만 · 바탕 띄움 건강) 끔
            lines += _rg_phys_same(snap, 'Y-2', (('list', '목록'), ('cnt', '문항 수'), ('brand', '머리 칩 줄'), ('tools', '교재 도구줄'), ('pgbar', '교재 칸 머리줄'), ('tree', '목차 서랍')))
    if QC.want('src'):   # smoke — 브라우저 밖 소스 칸(S-*)은 smoke 칸이 아니다
        lines += static_checks()
    npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
    for x in lines: print(x)
    print('\n== 칸에서 오리기/교재 링크 %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
