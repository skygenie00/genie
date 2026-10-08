# -*- coding: utf-8 -*-
"""지학 3건(글상자 · 아이패드 필기 · 교재 창) — 헤드리스 검산
(2026-09-10 · gigu/_task_20260910_자과앱_지학3건.md)

  G  층 게이트 표 — phys / bio / earth (§1-1 · §5 의 미결을 같이 닫는다)
  W  §3 교재 창 — 「⧉ 창으로」 · makeFloat · 창 안 필기/글상자/링크 · 자리 기억 · 「📖 크게」 무변
  K  §2 필기 — stylusGuard 를 직접 불러 본다(손바닥 섞임 · 긋는 중) · #inkc 스타일
  X  §1 글상자 — 지학 **네 자리** 다(교재 전체 화면 · 문항 화면 교재 칸 · 서브노트 · 암기카드)
  B  생물도 같이 산다
  Y  물리 무변 — DOM 글자 대조(고침 전 사본과)
  S  원본 대조(파이썬)

⚠ 픽셀 IDENTICAL 게이트는 쓰지 않는다(CLAUDE.md 「자과앱에는 픽셀 게이트를 걸지 않는다」).
   가림·쌓임은 elementsFromPoint · 그려졌는가는 DOM 개수·getBoundingClientRect 로 잰다.

    PYTHONIOENCODING=utf-8 python _harness_jagwa_3geon.py
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
BASE = SRC + '.before_3geon'
_RG_SMOKE = ('콘솔 오류 0', 'E-0 지학 카드 층', 'W-1 ★교재를 부르면 창으로 뜬다')   # qa_slim2 smoke 칸(A-0)
SPDROOT = _roots.spd()
GIGU = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.environ.get('TEMP', '.'), 'h3geon'); os.makedirs(OUT, exist_ok=True)
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
 const N=(n,i)=>R.push('NOTE | '+n+' | '+JSON.stringify(i===undefined?null:i));
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
 const topAt=(el)=>{const r=el.getBoundingClientRect();
   const st=document.elementsFromPoint(r.left+r.width/2,r.top+r.height/2);
   return st.map(e=>(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className)||e.id||e.tagName)};
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

GATE = r"""
   /* ══ G. 층 게이트 표 (§1-1 · §5) ══ */
   N('G 게이트 · '+SUBJ_ID,{
     subj:SUBJ_ID, CUR_LAYER:(CUR.LAYER===undefined?'(없음)':CUR.LAYER), CARD_LAYER:CARD_LAYER,
     body_layer:document.body.dataset.layer,
     SYNC_KEYS:SYNC_KEYS.length, txt자리:SYNC_KEYS.indexOf('txt'),
     txtAdd:typeof txtAdd, txtPaint:typeof txtPaint, txtSet:typeof txtSet,
     BK_txt:(typeof BK==='undefined')?'BK없음':(BK.txt===undefined?'(없음)':BK.txt),
     SUB_txt:(typeof SUB==='undefined')?'SUB없음':(SUB.txt===undefined?'(없음)':SUB.txt),
     BOOK_txt:(typeof BOOK==='undefined')?'BOOK없음':(BOOK.txt===undefined?'(없음)':BOOK.txt),
     교재도구줄:!!document.querySelector('#bktools [data-tool="txt"]'),
     서브노트도구줄:!!document.querySelector('#stools [data-tool="txt"]'),
     옆칸단추:!!document.getElementById('bpTxt'),
     창단추:!!document.getElementById('bpWin'),
     book_panel:!!document.querySelector('#book>.panel')
   });
"""

INK = r"""
   /* ══ K. §2 아이패드 필기 ══
      stylusGuard 는 top-level 함수라 **직접 불러** 잰다. 헤드리스에는 touchType 이 없으니
      가짜 접점을 만들어 규칙만 확인한다(브라우저가 아니라 우리 규칙을 재는 것이다). */
   await grp('K', async()=>{
     const c=document.getElementById('inkc');
     T('K-1 #inkc 가 있다',!!c);
     const cs=getComputedStyle(c);
     N('K-1 #inkc 계산 스타일',{cls:c.className,ta:cs.touchAction,us:cs.userSelect,ob:cs.overscrollBehavior});
     T('K-1 끝에서 페이지가 끌려가지 않는다(overscroll-behavior: contain)',cs.overscrollBehavior==='contain',cs.overscrollBehavior);
     T('K-1 그리는 층에서 글자가 안 잡힌다(user-select: none)',cs.userSelect==='none',cs.userSelect);
     T('K-1 ★`.pen` 은 여전히 SET.pencil 에 매여 있다 — 손가락 스크롤을 안 죽였다',
       (function(){const was=SET.pencil;
         SET.pencil=true;c.classList.toggle('pen',true);const a=getComputedStyle(c).touchAction;
         SET.pencil=false;c.classList.toggle('pen',false);const b=getComputedStyle(c).touchAction;
         SET.pencil=was;c.classList.toggle('pen',!!was);
         return a==='auto'&&b==='none'})(),
       [getComputedStyle(c).touchAction]);

     const fire=(touches,pencil,live)=>{
       const was=SET.pencil, wasD=(typeof drawing!=='undefined')?drawing:null;
       SET.pencil=pencil; try{drawing=live?{p:[]}:null}catch(e){}
       let hit=false;
       const ev={touches:touches,changedTouches:touches,preventDefault:()=>{hit=true}};
       stylusGuard(ev);
       SET.pencil=was; try{drawing=wasD}catch(e){}
       return hit};
     const P_=t=>({touchType:t});
     /* A-6(a) 9/30 — 손가락 필기 모드(SET.pencil 거짓)는 9/13 c62b2b2 로 없어졌다(pen_touch2 §1 「!SET.pencil 갈래(손가락 필기)는 죽은 길이니 지운다」 · stylusGuard 의 그 줄 걷음)
        → 스위치와 무관하게 손가락 하나는 안 막는다(펜슬 모드 · 손가락 하나 줄과 같은 값) */
     T('K-2 손가락 필기 모드는 없다 — SET.pencil 이 꺼져도 손가락 하나는 안 막는다(9/13 c62b2b2)',fire([P_('direct')],false,false)===false);
     T('K-2 펜슬 모드 · 펜슬 하나 — 막는다(종전 그대로)',fire([P_('stylus')],true,false)===true);
     T('K-2 펜슬 모드 · 손가락 하나 — 안 막는다(스크롤은 그대로 살아 있다)',fire([P_('direct')],true,false)===false);
     T('K-2 ★손바닥이 먼저 · 펜슬이 나중 — **막는다**(종전에는 touches[0] 만 봐서 새던 자리)',
       fire([P_('direct'),P_('stylus')],true,false)===true);
     T('K-2 ★손가락 둘(핀치)은 그대로 흘려보낸다',fire([P_('direct'),P_('direct')],true,false)===false);
     T('K-2 ★획이 사는 동안에는 무조건 막는다',fire([P_('direct')],true,true)===true);
     T('K-2 접점이 없으면 아무것도 안 한다',fire([],true,false)===false);
     /* 9/7 에 들어간 것 둘이 그대로인가 */
     T('K-3 손바닥 거르기·펜슬 전용이 그대로다(pointerdown 규칙 무변)',
       true);   /* 소스 대조는 S-쪽에서 글자로 잰다 */
   });
"""

BODY_EARTH = GATE + r"""
   await loadEarthData(); draw(); await wait(120);
   T('E-0 지학 카드 층 · 데이터 적재',CARD_LAYER===true&&SUBJ_ID==='earth'&&DATA.length>0,[SUBJ_ID,DATA.length]);
   T('G-1 ★지학 층 게이트는 멀쩡하다 — CARD_LAYER·txt 함수·SYNC 키가 다 산다(지시서 §1 가설과 다름)',
     CARD_LAYER===true&&CUR.LAYER===true&&typeof txtAdd==='function'&&typeof txtPaint==='function'
     &&SYNC_KEYS.indexOf('txt')>=0&&!!SYNC_REF.txt,
     [CARD_LAYER,CUR.LAYER,typeof txtAdd,SYNC_KEYS.indexOf('txt')]);
""" + INK + r"""

   /* 한 자리에서 글상자를 세우고 글자를 넣고 저장까지 되는지 재는 공통 잣대 */
   const tryTxt=async(tag,host,key,fire)=>{
     const n0=txtList(key).length;
     await fire(); await wait(320);
     const el=host.querySelector('.tbox');
     T(tag+' 찍으면 글상자가 선다',!!el,host.querySelectorAll('.tbox').length);
     if(!el)return false;
     T(tag+' 커서가 그 글상자에 있다',document.activeElement===el,
       document.activeElement&&(document.activeElement.className||document.activeElement.id||document.activeElement.tagName));
     T(tag+' 글자를 받는 상태다(contentEditable · pointer-events · user-select)',
       el.isContentEditable===true&&getComputedStyle(el).pointerEvents!=='none'&&getComputedStyle(el).userSelect!=='none',
       [el.contentEditable,getComputedStyle(el).pointerEvents,getComputedStyle(el).userSelect]);
     /* ★가림·쌓임은 픽셀이 아니라 쌓임 순서로 잰다(CLAUDE.md). 맨 위가 그 글상자거나 **그 안의 손잡이**면 통과 —
        `.tmove`·`.tgrip` 은 글상자가 제 안에 단 것이라 가리는 것이 아니다. */
     T(tag+' ★그 자리의 맨 위가 글상자(또는 그 손잡이)다 — 가림 없음 · elementsFromPoint',
       (function(){const r=el.getBoundingClientRect();
         const st=document.elementsFromPoint(r.left+r.width/2,r.top+r.height/2);
         return st.length>0&&(st[0]===el||el.contains(st[0]))})(),topAt(el).slice(0,3));
     el.textContent=tag+' 시험글자';
     el.dispatchEvent(new Event('blur')); await wait(400);
     const a=txtList(key);
     T(tag+' blur 하면 저장된다',a.length===n0+1&&a[a.length-1].s.indexOf('시험글자')>=0,[a.length,n0]);
     const kv=await get('kv','txt');
     T(tag+' ★IndexedDB(kv/txt)에도 들어갔다 — 새로고침 뒤에도 남는다',
       !!kv&&Array.isArray(kv[key])&&kv[key].length===n0+1&&kv[key][kv[key].length-1].s.indexOf('시험글자')>=0,
       kv&&kv[key]&&kv[key].length);
     return true};

   /* ═══ X-1 교재 전체 화면 ═══ */
   let PR=0;
   await grp('X-1', async()=>{
     const r=DATA.find(x=>+x[F.BPAGE]>0)||DATA[0];
     await openView(r[F.NO]); await wait(400);
     bkWin(false); await bkOpen(208); await wait(2800);
     let n=0;while(n++<60&&!bkCurPage())await wait(200);
     PR=bkCurPage()?bkCurPage().pr:0;
     T('X-1 교재 전체 화면(머리 단추 길)이 열렸다',BK.open===true&&PR>0,[BK.open,PR]);
     $('#bktools [data-tool="txt"]').click(); await wait(80);
     const p=bkCurPage(), vp=$('#bkvp'), vr=vp.getBoundingClientRect();
     await tryTxt('X-1 교재 전체화면',p.el,p.key,async()=>{
       PE('pointerdown',vp,vr.left+vr.width/2,vr.top+vr.height/2,'pen');
       PE('pointerup',vp,vr.left+vr.width/2,vr.top+vr.height/2,'pen')});
     $('#bktools [data-tool="view"]').click();
     N('X-1 교재 쪽 키',p.key);
   });

   /* ═══ X-2 ★교재는 팝업 창 하나 (2026-09-10 사용자 확정) ═══ */
   await grp('X-2', async()=>{
     bkClose(); bkWin(false); await wait(200);
     T('X-2 ★아래 도구줄 「교재」(#tBook)가 안 보인다',
       !!$('#tBook')&&getComputedStyle($('#tBook')).display==='none',
       $('#tBook')&&getComputedStyle($('#tBook')).display);
     T('X-2 ★옆 칸(#bookpane)이 안 보인다',
       !!$('#bookpane')&&getComputedStyle($('#bookpane')).display==='none',
       $('#bookpane')&&getComputedStyle($('#bookpane')).display);
     T('X-2 bookVisible() 이 false 로 굳었다 — 따라오기·resize 가 숨은 칸을 안 그린다',bookVisible()===false);
     T('X-2 ★「⧉ 창으로」(#bpWin)·옆 칸 「T 글상자」(#bpTxt)는 안 만든다',!$('#bpWin')&&!$('#bpTxt'),
       [!!$('#bpWin'),!!$('#bpTxt')]);
     /* 문제 카드 머리줄 칩 하나만 남았는가 — 그리고 누르면 창으로 뜨는가 */
     const chip=[...document.querySelectorAll('#card .cmeta [data-page]')];
     T('X-2 ★문제 윗줄(카드 머리줄)에 교재 칩이 하나 있다',chip.length===1,chip.map(x=>x.textContent));
     /* A-6(a) 9/30 — 머리줄 📖 p 칩은 listpop §F(a9f9fd4)부터 「교재 자리 목록」 창(#bpl)을 연다 · 교재 창은 그 줄(data-bkgo · bookwin §A 6c54347)을 눌러 뜬다.
        목록 창은 닫아 옛 차례와 같게 둔다(떠 있는 창이 뒤 묶음의 elementsFromPoint 를 가리지 않게 · 붙는 문항 CROPFOR 도 비운다).
        ⚠ 칩이 목록 창만 열면 PR 이 X-1 의 208쪽에 머물러 X-6 이 X-1 글상자가 남은 쪽에서 옛 글상자를 집었다(X-6 FAIL 여섯의 뿌리) */
     chip[0].click(); await wait(400);
     {const row=$('#bpl [data-bkgo]'); if(row)row.click()} await wait(2800);
     let n=0;while(n++<60&&!bkCurPage())await wait(200);
     {const x=$('#bplX'); if(x)x.click()} await wait(150);
     const b=$('#book'), p=$('#book>.panel');
     T('X-2 ★칩 → 교재 자리 목록 창 줄을 누르면 **팝업 창**으로 뜬다(전체 화면이 아니다)',
       BK.open===true&&b.classList.contains('win')&&p.classList.contains('float'),
       [BK.open,b.className,p&&p.className]);
     T('X-2 창이 화면보다 작다',
       (function(){const r=p.getBoundingClientRect();return r.width<window.innerWidth-8&&r.height<window.innerHeight-8})(),
       (function(){const r=p.getBoundingClientRect();return [Math.round(r.width),window.innerWidth]})());
     T('X-2 칩이 가리킨 쪽이 열렸다',bkCurPage()&&bkCurPage().pr>0,bkCurPage()&&bkCurPage().pr);
     PR=bkCurPage().pr;
     /* 오리기·링크가 교재 창으로 옮겨 왔는가 */
     T('X-2 ★교재 창 도구줄에 ◻ 오리기가 있다(옆 칸에서 옮겨 왔다)',!!$('#bktools [data-tool="crop"]'),
       [...$('#bktools').children].map(e=>e.dataset.tool||e.id).join(','));
     T('X-2 🔗 링크도 그대로 있다',!!$('#bktools [data-tool="bref"]'));
     T('X-2 도구 일곱 — 보기·펜·형광·지우개·글상자·오리기·링크',
       ['view','pen','hl','erase','txt','crop','bref'].every(t=>!!$('#bktools [data-tool="'+t+'"]')));
     T('X-2 차례 = 글상자 → 오리기 → 링크 → ↺',(()=>{
       const ch=[...$('#bktools').children], ix=s2=>ch.findIndex(e=>e.matches(s2));
       const t=ix('[data-tool="txt"]'),c=ix('[data-tool="crop"]'),r=ix('[data-tool="bref"]'),u=ix('#bkUndo');
       return t>=0&&c>=0&&r>=0&&u>=0&&t<c&&c<r&&r<u})(),
       [...$('#bktools').children].map(e=>e.dataset.tool||e.id).join(','));
     /* 창 안에서 오리기가 실제로 도는가 */
     $('#bktools [data-tool="crop"]').click(); await wait(80);
     T('X-2 오리기를 켜면 BK.tool 이 crop 이 된다',BK.tool==='crop',BK.tool);
     const vp=$('#bkvp'), vr=vp.getBoundingClientRect(), pg=bkCurPage();
     const sp=(fx,fy)=>{const q=pg.el.getBoundingClientRect();
       const l=Math.max(vr.left+6,q.left), r2=Math.min(vr.right-6,q.right);
       const t=Math.max(vr.top+6,q.top),  b=Math.min(vr.bottom-6,q.bottom);
       return [l+(r2-l)*fx, t+(b-t)*fy]};
     const was=SET.pencil; SET.pencil=true;
     const [q0x,q0y]=sp(0.25,0.25), [q1x,q1y]=sp(0.45,0.4);
     drag(vp,q0x,q0y,q1x,q1y,'pen');
     await wait(300);
     SET.pencil=was;
     T('X-2 ★창 안에서 펜으로 끌면 네모가 서고 메뉴가 뜬다',
       !!document.getElementById('crmenu'),!!document.getElementById('crmenu'));
     /* ⚠ 메뉴만 지우면 안 된다 — 네모(crop)가 살아 있으면 그 뒤 **모든 pointerup 이 오리기 갈래로 빠져**
        필기가 영영 안 커밋된다(실측). 메뉴의 「취소」를 눌러 제대로 걷는다. */
     const m=document.getElementById('crmenu');
     const x=m&&m.querySelector('button.x');
     if(x)x.click(); else if(m)m.remove();
     await wait(200);
     T('X-2 취소하면 네모·메뉴가 사라진다',!document.getElementById('crmenu')&&$$$('#bkover .crbox').length===0,
       [!!document.getElementById('crmenu'),$$$('#bkover .crbox').length]);
     $('#bktools [data-tool="view"]').click();
   });

   /* ═══ X-3 서브노트 ═══ */
   await grp('X-3', async()=>{
     await subOpen('',false); await wait(2600);
     const t=$('#stools [data-tool="txt"]');
     T('X-3 서브노트 도구줄에 「T 글상자」',!!t);
     t.click(); await wait(80);
     const p=SUB.pages()[0], host=$('#sover .spgo[data-i="'+p.i+'"]');
     const hr=host.getBoundingClientRect(), vp=$('#svp'), vr=vp.getBoundingClientRect();
     const cx=Math.max(vr.left+4,Math.min(vr.right-4,hr.left+hr.width/2));
     const cy=Math.max(vr.top+4,Math.min(vr.bottom-4,hr.top+hr.height/2));
     await tryTxt('X-3 서브노트',host,p.key,async()=>{
       PE('pointerdown',vp,cx,cy,'pen');PE('pointerup',vp,cx,cy,'pen')});
     delete TXT[p.key]; await saveTXT();
     $('#stools [data-tool="view"]').click();
     $('#sX').click(); await wait(150);
   });

   /* ═══ X-4 암기카드 ═══ */
   await grp('X-4', async()=>{
     const no=VNO||DATA[0][F.NO];
     if(!VNO)await openView(no);
     mcardWin(no); await wait(500);
     const t=$('.mcwin .mct [data-t="txt"]');
     T('X-4 카드 도구줄에 「T 글상자」',!!t);
     t.click(); await wait(60);
     const box=$('.mcwin .mccv'), br=box.getBoundingClientRect(), cv=$('.mcwin #mcc');
     /* ★ uid_unify 옛 잣대 고침(2026-10-04 · 근거 gigu/_task_jagwa_uid_unify.md §A-1 · §A-2 「txt 는 card:<번호> 칸」) — 카드 층(지학)의 암기카드 글상자 칸 = card:<uid>(앱 cardKey='card:'+qk(no)) · 옛 판(바탕 4754b1d · qk 없음)은 card:<번호> */
     const ck='card:'+((typeof qk==='function')?qk(no):no);
     /* 옛: await tryTxt('X-4 암기카드',box,'card:'+no,async()=>{
       PE('pointerdown',cv,br.left+br.width/2,br.top+br.height/2,'pen')}); */
     await tryTxt('X-4 암기카드',box,ck,async()=>{
       PE('pointerdown',cv,br.left+br.width/2,br.top+br.height/2,'pen')});
     /* 옛: delete TXT['card:'+no]; await saveTXT(); */
     delete TXT[ck]; await saveTXT();
     document.querySelectorAll('.sheet.mcwin').forEach(x=>x.remove());
   });

   /* ═══ X-5 동기화·백업에 실린다 ═══ */
   await grp('X-5', async()=>{
     T('X-5 SYNC_KEYS 에 txt · SYNC_REF 가 같은 통을 가리킨다',
       SYNC_KEYS.indexOf('txt')>=0&&!!SYNC_REF.txt&&SYNC_REF.txt.g()===TXT);
     /* 백업은 `exportData(withPdf)` 다. 파일을 내려받지 않게 a.click 을 잠깐 가로채고 Blob 을 읽는다. */
     let dump=null;
     const A=document.createElement;
     document.createElement=function(t){const el=A.call(document,t);
       if(String(t).toLowerCase()==='a'){el.click=function(){};}
       return el};
     const BU=URL.createObjectURL, blobs=[];
     URL.createObjectURL=function(b){blobs.push(b);return 'blob:x'};
     try{await exportData(false);await wait(300);
       if(blobs.length)dump=JSON.parse(await blobs[blobs.length-1].text());}catch(e){N('X-5 예외',String(e))}
     document.createElement=A; URL.createObjectURL=BU;
     T('X-5 백업 파일이 만들어졌다',!!dump,dump&&Object.keys(dump));
     if(dump){
       const c=dump.card||{};
       T('X-5 ★백업에 글상자(txt)가 실린다',!!c.txt,Object.keys(c));
       T('X-5 ★같이 빠져 있던 셋(crop·tfix·bref)도 실린다',
         c.crop!==undefined&&c.tfix!==undefined&&c.bref!==undefined,Object.keys(c));
       T('X-5 종전 여섯도 그대로 실린다',
         ['bogi','unit','bpit','bpg','snote','mcard'].every(k=>c[k]!==undefined),Object.keys(c));
       T('X-5 불러오기가 읽는 칸과 이름이 같다(importData 무접촉)',
         ['crop','txt','tfix','bref'].every(k=>k in c));
     }
   });

   /* ═══ X-6 글상자 넷 — 폭 · 지우기 · 색/크기 · iOS 자판 (2026-09-10 사용자 지적) ═══ */
   await grp('X-6', async()=>{
     bkClose(); bkWin(false); await bkOpen(PR); await wait(2600);
     let n=0;while(n++<60&&!bkCurPage())await wait(200);
     const p=bkCurPage(), vp=$('#bkvp'), vr=vp.getBoundingClientRect();
     for(const k of Object.keys(TXT))delete TXT[k];
     $('#bktools [data-tool="txt"]').click(); await wait(80);
     const pr1=p.el.getBoundingClientRect();
     const mx=Math.max(vr.left+6,Math.min(vr.right-6,pr1.left+pr1.width*0.5));
     const my=Math.max(vr.top+6,Math.min(vr.bottom-6,pr1.top+pr1.height*0.5));
     PE('pointerdown',vp,mx,my,'pen');
     PE('pointerup',vp,mx,my,'pen');
     await wait(340);
     const el=p.el.querySelector('.tbox');
     T('X-6 글상자가 섰다',!!el);
     if(!el)return;
     /* ⓐ 폭 — 늘리지 않아도 쓸 만한 넓이가 있다 */
     const w0=el.getBoundingClientRect().width, h0=el.getBoundingClientRect().height;
     T('X-6 ★빈 글상자에 폭이 있다 — 「옆으로 늘려야 써진다」가 안 난다',w0>=40&&h0>=12,[Math.round(w0),Math.round(h0)]);
     T('X-6 빈 표시(.empty)가 붙어 있다',el.classList.contains('empty'));
     /* ⓑ iOS — 포인터를 안 잡고 있다 · 끝난 탭에서 focus 를 다시 건다 */
     T('X-6 ★확대층이 포인터를 놓았다(끝난 탭이 글상자에 닿는다)',
       !(vp.hasPointerCapture&&vp.hasPointerCapture(31)),vp.hasPointerCapture&&vp.hasPointerCapture(31));
     T('X-6 커서가 글상자에 있다',document.activeElement===el);
     /* ⓒ·ⓓ 손잡이 넷 */
     T('X-6 ★손잡이 넷 — 옮기기·폭·지우기·색크기',
       !!el.querySelector('.tmove')&&!!el.querySelector('.tgrip')&&!!el.querySelector('.tdel')&&!!el.querySelector('.tsty'),
       [...el.children].map(x=>x.className));
     /* 글자를 넣고 저장 — 손잡이 글자가 안 섞여야 한다 */
     const tn=document.createTextNode('시험글자');
     el.insertBefore(tn,el.firstChild);
     el.dispatchEvent(new Event('blur')); await wait(420);
     const a=txtList(p.key);
     T('X-6 ★저장된 글에 손잡이 글자(✕·🎨)가 안 섞인다',
       a.length===1&&a[0].s==='시험글자',a.map(x=>x.s));
     /* ⓓ 색·크기 고르개 */
     const sy=el.querySelector('.tsty');
     PE('pointerdown',sy,0,0,'mouse'); await wait(120);
     const pal=el.querySelector('.tpal');
     T('X-6 ★🎨 를 누르면 고르개가 뜬다',!!pal,!!pal);
     if(pal){
       T('X-6 색 여섯 · 크기 넷',pal.querySelectorAll('i').length===6&&pal.querySelectorAll('b').length===4,
         [pal.querySelectorAll('i').length,pal.querySelectorAll('b').length]);
       const c0=txtList(p.key)[0].c;
       const other=[...pal.querySelectorAll('i')].find(x=>x.style.background&&!x.classList.contains('on'));
       PE('pointerdown',other,0,0,'mouse'); await wait(420);
       const c1=txtList(p.key)[0].c;
       T('X-6 ★색을 고르면 그 글상자에 걸리고 저장된다',c1&&c1!==c0,[c0,c1]);
       PE('pointerdown',el.querySelector('.tsty'),0,0,'mouse'); await wait(120);
       const pal2=el.querySelector('.tpal');
       const big=[...pal2.querySelectorAll('b')].find(x=>!x.classList.contains('on'));
       const f0=txtList(p.key)[0].fs;
       PE('pointerdown',big,0,0,'mouse'); await wait(420);
       const f1=txtList(p.key)[0].fs;
       T('X-6 ★크기를 고르면 그 글상자에 걸리고 저장된다',f1&&f1!==f0,[f0,f1]);
       T('X-6 고른 값이 다음 글상자 기본값이 된다(기기에 남는다)',
         TXT_C===c1&&+TXT_FS===+f1&&!!localStorage.getItem('jagwa.txt.style'),
         [TXT_C,TXT_FS,localStorage.getItem('jagwa.txt.style')]);
     }
     /* ⓒ 지우기 */
     const before=txtList(p.key).length;
     PE('pointerdown',el.querySelector('.tdel'),0,0,'mouse'); await wait(450);
     T('X-6 ★✕ 를 누르면 그 글상자만 지워진다',txtList(p.key).length===before-1&&!el.isConnected,
       [before,txtList(p.key).length,el.isConnected]);
     const kv=await get('kv','txt');
     T('X-6 지운 것이 IndexedDB 에도 반영된다',!kv||!kv[p.key]||kv[p.key].length===before-1,
       kv&&kv[p.key]&&kv[p.key].length);
     $('#bktools [data-tool="view"]').click();
     bkClose(); await wait(150);
   });

   /* ═══ X-7 문항 화면(문제 카드) 글상자 — 사용자 지적 「문항화면에는 글상자 버튼도 아예없고」 ═══ */
   await grp('X-7', async()=>{
     bkClose(); bkWin(false); await wait(200);
     const no=VNO||DATA[0][F.NO];
     if(!VNO)await openView(no);
     await wait(400);
     T('X-7 ★아래 도구줄에 「T 글상자」가 있다',!!$('#tTxt'),$('#tTxt')&&$('#tTxt').textContent);
     T('X-7 지우개 바로 뒤에 있다',!!$('#tTxt')&&$('#tTxt').previousElementSibling.id==='tErase',
       $('#tTxt')&&$('#tTxt').previousElementSibling.id);
     const card=$('#card');
     T('X-7 카드에 글자 층(#qtxt)이 얹혔다',!!card.querySelector('#qtxt'));
     T('X-7 평소에는 포인터를 안 받는다(필기와 안 싸운다)',
       getComputedStyle(card.querySelector('#qtxt')).pointerEvents==='none',
       getComputedStyle(card.querySelector('#qtxt')).pointerEvents);
     $('#tTxt').click(); await wait(80);
     T('X-7 켜면 on 이 붙고 카드가 txton 이 된다',QTXT===true&&$('#tTxt').classList.contains('on')&&card.classList.contains('txton'));
     const h=card.querySelector('#qtxt');
     T('X-7 켜면 글자 층이 포인터를 받는다',getComputedStyle(h).pointerEvents==='auto');
     const key='q:'+QUID;
     delete TXT[key]; await saveTXT();
     const hr=h.getBoundingClientRect();
     PE('pointerdown',h,hr.left+hr.width*0.4,hr.top+60,'pen'); await wait(340);
     const el=h.querySelector('.tbox');
     T('X-7 ★찍으면 문제 위에 글상자가 선다',!!el,h.querySelectorAll('.tbox').length);
     if(el){
       T('X-7 커서가 그 글상자에 있다',document.activeElement===el);
       const tn=document.createTextNode('문항 시험글자');
       el.insertBefore(tn,el.firstChild);
       el.dispatchEvent(new Event('blur')); await wait(420);
       const a=txtList(key);
       T('X-7 ★키가 q:<uid> 꼴이다(교재 bink· 서브노트 note· 카드 card 에 이은 넷째)',
         a.length===1&&a[0].s==='문항 시험글자',[key,a.map(x=>x.s)]);
       T('X-7 좌표가 문항 필기와 같은 기준(카드 폭으로 나눈 0~1)',
         a[0].x>0&&a[0].x<1&&a[0].y>0&&a[0].y<1,a[0]);
       const kv=await get('kv','txt');
       T('X-7 IndexedDB 에 남는다',!!kv&&(kv[key]||[]).some(x=>x.s==='문항 시험글자'));
       T('X-7 ★문항 필기(qink)는 안 늘었다 — 통이 다르다',((QINK&&QINK.s)||[]).length===0,
         ((QINK&&QINK.s)||[]).length);
       T('X-7 손잡이 넷이 여기에도 있다',
         !!el.querySelector('.tmove')&&!!el.querySelector('.tgrip')&&!!el.querySelector('.tdel')&&!!el.querySelector('.tsty'));
       /* 다시 그려도 남는가 */
       qTxtPaint(); await wait(150);
       T('X-7 다시 그려도 그 자리에 남는다',h.querySelectorAll('.tbox').length===1&&
         h.querySelector('.tbox').textContent.indexOf('문항 시험글자')>=0,
         h.querySelectorAll('.tbox').length);
     }
     $('#tTxt').click(); await wait(80);
     T('X-7 끄면 다시 포인터를 안 받는다',QTXT===false&&getComputedStyle(h).pointerEvents==='none');
     delete TXT[key]; await saveTXT();
   });

   /* ═══ W. §3 교재 창 ═══ */
   await grp('W-1', async()=>{
     T('W-1 ★교재를 부르면 창으로 뜬다(bookOpen 한 자리로 모았다)',typeof bookOpen==='function'&&typeof bkWin==='function');
     T('W-1 머리 단추(#btnBook)는 종전대로 전체 화면 길이다',!!$('#btnBook'));
     await bookOpen(PR); await wait(2600);
     let n=0;while(n++<60&&!bkCurPage())await wait(200);
     const b=$('#book'), p=$('#book>.panel');
     T('W-1 ★창으로 열린다 — #book.win · .panel.float',
       b.classList.contains('win')&&!!p&&p.classList.contains('float'),[b.className,p&&p.className]);
     T('W-1 ★전체 화면이 아니다(창이 화면보다 작다)',
       (function(){const r=p.getBoundingClientRect();return r.width<window.innerWidth-8&&r.height<window.innerHeight-8})(),
       (function(){const r=p.getBoundingClientRect();return [Math.round(r.width),window.innerWidth,Math.round(r.height),window.innerHeight]})());
     T('W-1 ★껍데기는 안 잡힌다 — 뒤 문항 화면이 그대로 산다(서브노트 창과 같은 규칙)',
       getComputedStyle(b).pointerEvents==='none'&&getComputedStyle(p).pointerEvents==='auto',
       [getComputedStyle(b).pointerEvents,getComputedStyle(p).pointerEvents]);
     T('W-1 창 밖 한 점의 맨 위가 #book 이 아니다(뒤가 눌린다)',
       (function(){const r=p.getBoundingClientRect();
         const x=Math.max(4,r.left/2), y=Math.max(4,r.top/2);
         const st=document.elementsFromPoint(x,y);
         return st.length>0&&st[0].id!=='book'&&!st.some(e=>e.id==='book')})(),
       (function(){const r=p.getBoundingClientRect();
         return document.elementsFromPoint(Math.max(4,r.left/2),Math.max(4,r.top/2)).slice(0,3).map(e=>e.id||e.className||e.tagName)})());
     T('W-1 자리·크기가 WIN.book 에 남는다',!!WIN.book&&WIN.book.w>=280&&WIN.book.h>=200,WIN.book);
     T('W-1 손잡이는 교재 머리줄(.bkbar)이다',!!$('#book .bkbar.twhandle'),!!$('#book .bkbar'));
     T('W-1 모서리 손잡이(.twgrip)가 하나 생겼다',$$$('#book .twgrip').length===1,$$$('#book .twgrip').length);
   });

   await grp('W-2', async()=>{
     /* 창 안에서도 도구가 다 산다 · 실제로 글상자를 놓아 본다 */
     T('W-2 창 안에도 도구 여섯이 그대로',
       ['view','pen','hl','erase','txt','bref'].every(t=>!!$('#bktools [data-tool="'+t+'"]')));
     const p0=bkCurPage();
     T('W-2 창 안에 교재 쪽이 그려졌다',!!p0&&!!p0.el&&p0.el.getBoundingClientRect().width>10,
       p0&&Math.round(p0.el.getBoundingClientRect().width));
     $('#bktools [data-tool="txt"]').click(); await wait(80);
     const vp=$('#bkvp'), vr=vp.getBoundingClientRect();
     /* ★ 쪽 사각형 ∩ 뷰포트 안에서 찍는다 — 창이 작아지면 뷰포트 비율 점이 쪽 밖으로 나간다 */
     const spot=(fx,fy)=>{const pr0=p0.el.getBoundingClientRect();
       const l=Math.max(vr.left+6,pr0.left), r=Math.min(vr.right-6,pr0.right);
       const t=Math.max(vr.top+6,pr0.top),  b=Math.min(vr.bottom-6,pr0.bottom);
       return [l+(r-l)*fx, t+(b-t)*fy]};
     const [cx0,cy0]=spot(0.5,0.5);
     const k0=txtList(p0.key).length;
     PE('pointerdown',vp,cx0,cy0,'pen');
     PE('pointerup',vp,cx0,cy0,'pen'); await wait(320);
     const el=p0.el.querySelector('.tbox.empty')||p0.el.querySelector('.tbox');
     T('W-2 ★창 안에서도 글상자가 선다(읽기 전용이 아니다)',!!el&&txtList(p0.key).length===k0+1,
       [!!el,txtList(p0.key).length,k0]);
     if(el){el.textContent='창 안 시험글자';el.dispatchEvent(new Event('blur'));await wait(380);
       T('W-2 창 안에서 쓴 글자가 같은 통에 저장된다',txtList(p0.key).some(x=>x.s==='창 안 시험글자'));}
     /* 필기도 산다 — 획 하나를 그어 본다 */
     $('#bktools [data-tool="pen"]').click(); await wait(60);
     /* ★ 획은 **한 쪽 안에서** 그어야 한다 — 두 쪽에 걸치면 pointermove 가 버려져 점 하나로 끝난다.
        그래서 toPage 로 쪽을 집고 그 쪽 사각형 안에서 짧게 긋는다. 잉크 통은 쪽마다 따로다. */
     const allS=()=>Object.keys(BK.ink||{}).reduce((n,k)=>n+((BK.ink[k]&&Array.isArray(BK.ink[k].s))?BK.ink[k].s.length:0),0);
     /* ⚠ 방금 만든 글상자가 그 자리를 덮고 있으면 pointerdown 이 글상자에서 멈춘다(제 pointerdown 이
        stopPropagation 한다 — 글상자 위에는 못 긋는 것이 맞는 동작이다). **글상자에서 떨어진 자리**를 고른다. */
     let sx, sy;
     for(const [fx,fy] of [[0.3,0.78],[0.25,0.7],[0.7,0.8],[0.35,0.2]]){
       const [x,y]=spot(fx,fy);
       const st=document.elementsFromPoint(x,y);
       if(!st.some(e=>e.classList&&e.classList.contains('tbox'))){sx=x;sy=y;break}}
     T('W-2 글상자에 안 걸리는 자리를 골랐다',sx!==undefined,[sx,sy]);
     if(sx===undefined)return;
     const hit=BK.toPage(sx,sy);
     T('W-2 그을 쪽을 집었다',!!hit,hit&&hit.i);
     const tgt=hit?BK.pages().find(x=>x.i===hit.i):null;
     if(tgt&&BK.ink[tgt.key]===undefined)await zInkLoad(BK,tgt);
     const before=allS();
     PE('pointerdown',vp,sx,sy,'pen');
     PE('pointermove',vp,sx+14,sy+6,'pen');
     PE('pointermove',vp,sx+28,sy+12,'pen');
     PE('pointermove',vp,sx+42,sy+18,'pen');
     PE('pointerup',vp,sx+42,sy+18,'pen');
     await wait(700);
     const after=allS();
     N('W-2 필기 진단',{tool:BK.tool,pen:BK.pen,pencil:SET.pencil,key:tgt&&tgt.key,
       inkKeys:Object.keys(BK.ink||{}).slice(0,6),before:before,after:after});
     T('W-2 ★창 안에서도 필기가 된다(획이 는다)',after===before+1,[before,after]);
     const kv=tgt?await get('ink',tgt.key):null;
     T('W-2 창 안에서 그은 획이 IndexedDB 까지 간다',
       !!kv&&Array.isArray(kv.s)&&kv.s.length===((BK.ink[tgt.key]||{s:[]}).s||[]).length,
       [kv&&kv.s&&kv.s.length,tgt&&((BK.ink[tgt.key]||{s:[]}).s||[]).length]);
     $('#bktools [data-tool="view"]').click();
   });

   await grp('W-3', async()=>{
     /* 크기를 바꾸면 기억한다 · 「크게」로 되돌아간다 · 다시 창으로 열면 그 자리 */
     const p=$('#book>.panel');
     WIN.book.w=Math.max(300,Math.round(WIN.book.w*0.8));
     WIN.book.h=Math.max(220,Math.round(WIN.book.h*0.8));
     WIN.book.l=40;WIN.book.t=40;
     bkWin(true); await wait(300);
     const r1=p.getBoundingClientRect();
     T('W-3 자리·크기를 바꾸면 그대로 따라간다',
       Math.abs(r1.left-40)<2&&Math.abs(r1.top-40)<2&&Math.abs(r1.width-WIN.book.w)<2,
       [Math.round(r1.left),Math.round(r1.top),Math.round(r1.width),WIN.book]);
     $('#bpBig')&&null;
     bkClose(); await wait(200);
     await bookOpen(PR); await wait(2600);
     const r2=$('#book>.panel').getBoundingClientRect();
     T('W-3 ★닫았다 다시 열어도 같은 자리·크기',
       Math.abs(r2.left-r1.left)<2&&Math.abs(r2.top-r1.top)<2&&Math.abs(r2.width-r1.width)<2,
       [Math.round(r2.left),Math.round(r2.top),Math.round(r2.width)]);
     T('W-3 모서리 손잡이가 여전히 하나다(창을 다시 열어도 안 늘어난다)',$$$('#book .twgrip').length===1,$$$('#book .twgrip').length);
     /* 「📖 크게」로 되돌아간다 */
     bkClose(); await wait(150);
     bkWin(false); await bkOpen(PR); await wait(2400);
     const b=$('#book'), pp=$('#book>.panel');
     T('W-3 ★「📖 크게」는 종전대로 전체 화면이다(.win 이 떨어진다)',
       !b.classList.contains('win')&&!pp.classList.contains('float')&&!pp.style.left,
       [b.className,pp.className,pp.style.cssText]);
     T('W-3 전체 화면일 때 껍데기가 다시 잡힌다',getComputedStyle(b).pointerEvents!=='none',getComputedStyle(b).pointerEvents);
     bkClose(); await wait(150);
   });

   /* 뒷정리 */
   await grp('cleanup', async()=>{
     for(const k of Object.keys(TXT))if(String(k).indexOf('bink:')===0)delete TXT[k];
     await saveTXT();
   });
"""

BODY_BIO = GATE + r"""
   await loadEarthData(); draw(); await wait(120);
   T('B-0 생물 카드 층',CARD_LAYER===true&&SUBJ_ID==='bio'&&DATA.length>0,[SUBJ_ID,DATA.length]);
   await grp('B-1', async()=>{
     T('B-1 생물도 층 게이트가 산다',CARD_LAYER===true&&typeof txtAdd==='function'&&SYNC_KEYS.indexOf('txt')>=0);
     const r=DATA.find(x=>+x[F.BPAGE]>0)||DATA[0];
     await openView(r[F.NO]); await wait(400);
     $('#tBook').click(); await wait(400);
     T('B-1 ★생물도 옆 칸·아래 도구줄 「교재」가 걷혔다',
       getComputedStyle($('#bookpane')).display==='none'&&getComputedStyle($('#tBook')).display==='none');
     T('B-1 생물 교재 창 도구줄에도 오리기·링크가 있다',!!$('#bktools [data-tool="crop"]')&&!!$('#bktools [data-tool="bref"]'));
     T('B-1 bkWin·bpTxtPaint 가 생물에서도 산다',typeof bkWin==='function'&&typeof bpTxtPaint==='function');
     T('B-1 #book 감싸개가 있다',!!$('#book>.panel'));
   });
""" + INK

BODY_PHYS = GATE + r"""
   await wait(500); draw(); await wait(300);
   T('Y-0 물리 · 카드 층 아님',SUBJ_ID==='phys'&&CARD_LAYER===false,[SUBJ_ID,CARD_LAYER]);
   const snap={};
   snap.list=$('#list').innerHTML; snap.cnt=$('#cnt').textContent;
   snap.brand=document.querySelector('.brand').innerHTML;
   snap.tools=$('#bktools')?$('#bktools').innerHTML:'(없음)';
   snap.pgbar=document.querySelector('.pgbar')?document.querySelector('.pgbar').innerHTML:'(없음)';
   snap.book=$('#book')?$('#book').className:'(없음)';
   await grp('Y-1', async()=>{
     T('Y-1 목록이 그려졌다',$$$('#list .item').length>0,$$$('#list .item').length);
     /* A-6(a) 9/30 — 카드 층 블록의 문이 c9faff2 에서 if(SHELL)(세 과목 참)로 바뀌었고 add5 §A 원칙(c20ef05)이 그대로 두어 물리에서도 함수는 만들어진다
        → 물리 무변은 「안 만든다」가 아니라 「교재 갈래 HASBOOK 이 거짓」으로 선다(값은 info 에 typeof 로 남긴다 · 화면에 없는 것은 아래 줄들이 잰다) */
     T('Y-1 물리는 글상자·교재 창을 안 쓴다 — txtAdd·bkWin·bpTxtPaint 는 SHELL 블록이라 있어도 HASBOOK=false',
       typeof HASBOOK!=='undefined'&&HASBOOK===false,
       [typeof txtAdd,typeof bkWin,typeof bpTxtPaint]);
     T('Y-1 물리 화면에 「T 글상자」·「⧉ 창으로」 단추가 없다',!$('#bpTxt')&&!$('#bpWin'));
     /* A-6(a) 9/30 — 글상자 도구는 카드 층 블록(if(SHELL) · c9faff2 · add5 §A)이 #bktools 에 붙인다 — 물리는 #book 이 body[data-layer="pdf"] 규칙으로 숨어 화면에 안 보인다 */
     T('Y-1 교재 도구줄 글상자는 물리 화면에 안 보인다(카드 층 블록 if(SHELL) · #book 숨음)',(t=>!t||t.offsetParent===null)($('#bktools [data-tool="txt"]')));
     T('Y-1 #book 은 숨어 있다',!!$('#book')&&$('#book').classList.contains('hide'));
     /* ★물리는 `#ebody` 통째가 `body[data-layer="pdf"]` 규칙으로 숨는다 — 그 안의 #bookpane 은
        제 display 가 flex 여도 **화면에 없다.** 그래서 보이는가는 offsetParent 로 잰다. */
     T('Y-1 ★물리는 교재 칸이 화면에 없다 — 이 판이 한 글자도 안 바꿨다',
       !!$('#ebody')&&getComputedStyle($('#ebody')).display==='none'
       &&$('#bookpane').offsetParent===null&&$('#tBook').offsetParent===null,
       [getComputedStyle($('#ebody')).display,$('#bookpane').offsetParent===null,$('#tBook').offsetParent===null]);
     T('Y-1 물리에서 bookVisible 은 SHELL 블록이라 있어도 거짓이다 — 옆 칸을 안 그린다(안 새 나갔다)',   /* A-6(a) 9/30 — c9faff2 · add5 §A 원칙 · 블록의 bookVisible=()=>false */
       typeof bookVisible!=='function'||bookVisible()===false,typeof bookVisible);
     T('Y-1 SYNC_KEYS 옛 12키 앞자리 그대로',SYNC_KEYS.slice(0,12).join()==='status,note,qtype,conc,gpt,twin,ansfix,frm,maskpos,omrpos,mcard,link',SYNC_KEYS.length);   /* A-6(a) 9/30 — shell_bio_phys §E-7(c9faff2) 물리 끝에 gg·ggref 더함 */
   });
""" + INK + r"""
   try{await __nativeFetch('/snap',{method:'POST',body:JSON.stringify(snap)})}catch(e){}
"""


def build(mode, src_text):
    subj = {'earth': 'earth', 'bio': 'bio', 'phys': 'phys', 'physbase': 'phys'}[mode]
    body = {'earth': BODY_EARTH, 'bio': BODY_BIO}.get(mode, BODY_PHYS)
    html = src_text
    html = html.replace('<script defer src="https://cdnjs', '<script defer data-off="https://cdnjs')
    html = html.replace('<link rel="stylesheet" href="https://cdnjs', '<link rel="off" href="https://cdnjs')
    html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js',
                        STUB.replace('__SUBJ__', subj) + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    html = html.replace('</body>', HEAD + body + TAIL + '</body>', 1)
    open(os.path.join(OUT, 'app.html'), 'w', encoding='utf-8', newline='').write(html)
    return subj


def run(mode, secs, src_text):
    QC.launch('base' if mode.endswith('base') else 'new')   # 셈(§B-4)
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
    p = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--user-data-dir=' + prof,
                          '--window-size=1500,950', 'http://127.0.0.1:%d/app.html' % port],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    got = done.wait(secs); p.terminate()
    try: p.wait(10)
    except Exception: p.kill()
    srv.shutdown()
    print('  [%s] %.0fs' % (mode, time.time() - t0))
    if not got:
        return (['FAIL | %s 묶음이 시간 안에 안 끝났다 | %s' % (mode, box.get('partial', '(중간 결과 없음)')[-2500:])], box.get('snap'))
    return ([ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()], box.get('snap'))


def static_checks():
    b = open(SRC, 'rb').read()
    s = b.replace(b'\r\n', b'\n').decode('utf-8')
    out = []
    def T2(name, cond, info=''):
        out.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))
    # A-6(a) 9/30 — 카드 층 블록의 문이 c9faff2(shell_bio_phys)에서 `if(CARD_LAYER){` → `if(SHELL){` 로 바뀌었다(add5 §A 원칙 「블록의 문 if(SHELL){ 는 그대로 두고 안에서 이름마다 가른다」 · c20ef05)
    #   → 같은 블록(/*EARTH:js*/ 뒤 첫 `if(SHELL){`)의 시작으로 잰다 · 물리도 이 블록을 돈다(물리 화면 몫은 HASBOOK 이 가른다)
    blk = s.find('\nif(SHELL){\n', s.find('/*EARTH:js*/'))
    T2('S-1 §1·§3 코드는 전부 카드 층 블록(if(SHELL)) 안이다',
       blk >= 0 and all(s.find(k) > blk for k in
                        ['function bpTxtPaint(', 'function bkWin(', 'var txtFocus=function(', 'var txtBody=function(']),
       [s.find(k) - blk for k in ['function bpTxtPaint(', 'function bkWin(', 'var txtFocus=function(', 'var txtBody=function(']])
    T2('S-1b 옆 칸 단추 둘(bpTxt·bpWin)은 **안 만든다**',
       "mk('bpTxt'" not in s and "mk('bpWin'" not in s)
    T2('S-2 §2 는 층 밖(물리도 쓰는 자리)이다 — 그렇게 적어 두었다',
       'function stylusGuard(e){' in s and s.find('function stylusGuard(e){') < blk
       and '지학 3건 §2' in s)
    T2('S-3 새 저장통을 안 만들었다 — 옆 칸 글상자도 같은 kv txt · 같은 bink: 키',
       s.count("var saveTXT=()=>put('kv','txt',TXT);") == 1
       and s.count("txtPaint(w,'bink:'+BOOK.page") == 1
       and s.count("txtAdd(wrap,'bink:'+BOOK.page") == 1)
    T2('S-4 좌표 기준을 새로 만들지 않았다 — 교재/서브노트/옆 칸 0~1 · 카드 1/1000',
       "txtPaint(p.el,p.key,p.w,p.h,1,true)" in s and "txtPaint(h,p.key,p.w,p.h,1,true)" in s
       and "txtPaint(w,'bink:'+BOOK.page,BOOK.pw*k,BOOK.ph*k,1,true)" in s
       and "txtPaint(box,cardKey,box.clientWidth||1,box.clientHeight||1,1000,true)" in s)
    T2('S-5 잉크 무접촉 — inkGet·pathD·zInkCommit·bpInk 가 그대로',
       'async function inkGet(key,p){' in s and 'var pathD=(p,w,h)=>' in s
       and 'async function bpInk(page,w,h){' in s)
    T2('S-6 ★손바닥 거르기·펜슬 전용(9/7)을 안 깼다',
       "if(drawing&&e.pointerType==='touch')return;" in s
       # A-6(a) 9/30 — 9/13 c62b2b2(pen_touch2 §1): SET.pencil 스위치를 없애 두 줄이 「if(e.pointerType!=='pen')return;」 한 줄이 됐다(손가락 필기 갈래는 죽은 길이라 걷음)
       and "갈래는 죽은 길이라 같이 걷었다. */\n  if(e.pointerType!=='pen')return;" in s)
    T2('S-7 ★`.pen`(손가락 스크롤)을 안 죽였다 — touch-action:auto 그대로',
       '#inkc.pen{touch-action:auto}' in s)
    T2('S-8 stylusGuard 가 접점을 전부 훑고 긋는 중에는 무조건 막는다',
       'if(drawing){e.preventDefault();return}' in s
       and 'const ts=(e.touches&&e.touches.length)?e.touches:e.changedTouches;' in s
       and "if(ts[i]&&ts[i].touchType==='stylus'){e.preventDefault();return}}" in s)
    T2('S-9 ★교재 창은 있는 함수를 부른다 — makeFloat 을 새로 짜지 않았다',
       s.count('function makeFloat(') == 1
       and "makeFloat(b,$('#book .bkbar'),'book','jagwa.win.book');" in s)
    T2('S-10 makeFloat 손잡이 무시 목록만 넓혔다(더하기 · 지금 창 넷은 무변)',
       # A-6(a) 9/30 — add18 §B-5(0c19a60)가 손잡이 무시 목록을 또 넓혔다(a · [data-nodrag] · textarea — iOS 서재·✕ click)
       "if(e.target.closest('button,a,[data-tool],[data-nodrag],#bktools,input,select,textarea'))return;" in s
       and s.count("handle.addEventListener('pointerdown'") == 1)
    T2('S-11 「📖 크게」를 안 없앴다 — 창은 더하는 것이다',
       "$('#bpBig').onclick=()=>{bkWin(false);bkOpen(BOOK.page||undefined)};" in s
       and s.count("mk('bpBig'") == 0)
    T2('S-12 창을 두 번 띄워도 makeFloat 은 한 번만 건다',
       'if(!b.__float){b.__float=1;' in s)
    T2('S-13 DATA 원본 무변', 'r[F.BODY]=' not in s)
    T2('S-14 백틱 짝', s.count('`') % 2 == 0)
    T2('S-15 CRLF 만', b.count(b'\r\n') == b.count(b'\n'))
    T2('S-17 폰(≤480)에서는 창이 전체 화면으로 떨어진다(서브노트 창의 폰 규칙 그대로)',
       '@media (max-width:480px){#book.win>.panel:not(.float){left:0;top:0;right:0;bottom:0;width:auto;height:auto;border-radius:0}' in s
       and '#book.win>.panel.float{left:0!important;top:0!important;width:auto!important;height:auto!important;right:0;bottom:0;border-radius:0}}' in s)
    # 옛 줄: T2('S-18 백업 내보내기에 판 3 넷을 더했다 · 불러오기는 무접촉',
    # 옛 줄: # A-6(a) 9/30 — add5(c20ef05)가 card 묶음을 카드 과목만 싣게 갈랐다(근거 gg·ggref 는 맨 위) — 넷은 그대로
    # 옛 줄: 'if(HASBOOK)out.card={bogi:BG,unit:UN,bpit:BP,bpg:BPG,snote:SN,mcard:MC,crop:CROP,txt:TXT,tfix:TFIX,bref:BREF};' in s
    # 옛 줄: and 'if(c.txt){TXT=c.txt;await put(' in s and s.count('importData=async function(f){') == 1)
    # ★ uid_unify 옛 잣대 고침 §A-2 — 앱이 카드 층 기록 열쇠를 uid 로 쓰는 판(앱 글에 qk(no))은 들이기 뒤에 「옛 백업(번호 열쇠) → uid」 옮김(uidMigrateImport)을 하려고 importData 를 **감싸는** 래퍼 하나를 더 세운다 —
    #   옛 본체(`importData=async function(f){if(!f)return;let txt;…` · `if(c.txt){TXT=c.txt;await put(`)는 한 글자도 안 바뀐다(무접촉) · 새 것은 옛 것을 `_imp2(f)` 로 부를 뿐 → 「정의 글자」가 하나가 아니라 둘이다. 옛 판(바탕)은 옛 식 그대로(하나)
    UIDK = 'function qk(no)' in s
    _n_imp = s.count('importData=async function(f){')
    _imp_ok = (_n_imp == 1) if not UIDK else (_n_imp == 2 and s.count('importData=async function(f){if(!f)return;let txt;') == 1
                                              and 'const _imp2=importData;importData=async function(f){' in s and 'await _imp2(f)' in s)
    T2('S-18 백업 내보내기에 판 3 넷을 더했다 · 불러오기는 무접촉',
       # A-6(a) 9/30 — add5(c20ef05)가 card 묶음을 카드 과목만 싣게 갈랐다(근거 gg·ggref 는 맨 위) — 넷은 그대로
       'if(HASBOOK)out.card={bogi:BG,unit:UN,bpit:BP,bpg:BPG,snote:SN,mcard:MC,crop:CROP,txt:TXT,tfix:TFIX,bref:BREF};' in s
       and 'if(c.txt){TXT=c.txt;await put(' in s and _imp_ok, [_n_imp, UIDK])
    T2('S-19 옆 칸 글상자가 교재 전체 화면과 같은 통을 쓴다 — 새 키 규칙이 없다',
       s.count("'bink:'+BOOK.page") == 2 and 'var txtList=key=>' in s)
    T2('S-20 옆 칸을 카드 층에서만 걷는다 — 물리 규칙은 안 건드렸다',
       # A-6(a) 9/30 — 9/13 ee2e1b7(사용자 확정)이 같은 규칙에 아랫줄 #tSub·#tMatch 를 더했다(카드 층만 · 물리 규칙 무접촉)
       'body[data-layer="card"] #bookpane,body[data-layer="card"] #tBook,\nbody[data-layer="card"] #tSub,body[data-layer="card"] #tMatch{display:none!important}' in s
       and 'body[data-layer="pdf"] #tBook' in s)
    T2('S-21b 옆 칸이 하던 두 가지를 교재 창이 잇는다(bpgTouchLast · bpgChips)',
       'var _bkGoto_plain=bkGoto;' in s and 'await bpgTouchLast(+pr);bpgChips()' in s)
    T2('S-21 교재를 부르는 길이 한 자리다 — bookOpen 만 갈아끼웠다(부르는 쪽 칩 손잡이 하나 · §F 목록 창 갈래만 더함)',
       "bookOpen=async function(pr,show){bkWin(true);const r=await bkOpen(+pr||undefined);" in s
       and 'var _bookOpen_pane=bookOpen;' in s
       # A-6(a) 9/30 — listpop §F(a9f9fd4): 머리줄 📖 p 칩 = 교재 자리 목록 창 갈래(HASBOOK) 한 줄을 더했다 · 나머지는 그대로 bookOpen
       and s.count("c.querySelectorAll('[data-page]').forEach(x=>x.onclick=e=>{e.preventDefault();\n    if(HASBOOK&&x.dataset.bpl){bplOpen(r[F.NO]);return}") == 1
       and "\n    bookOpen(+x.dataset.page,true)});" in s)
    T2('S-22 오리기 엔진을 새로 안 짰다 — 단추만 도로 그린다',
       s.count('function cropOffer(') == 1 and 'BK.onCrop=function(crop,clear){' in s
       and "sp.dataset.tool='crop';sp.textContent='◻ 오리기'" in s)
    T2('S-23 ★손잡이 글자가 내용에 안 섞인다 — 읽는 자리가 txtBody 하나다',
       'var txtBody=function(el){' in s and "t.s=String(txtBody(el)||'')" in s
       and s.count("String(el.textContent||'')") == 0)
    T2('S-24 iOS — 포인터를 놓고 · preventDefault 를 안 걸고 · 끝난 탭에서 focus 를 다시 건다',
       'try{vp.releasePointerCapture(e.pointerId)}catch(_){}' in s
       and "if(tool==='txt'&&cardTxt){const[u,v]=pt(e);" + chr(10) in s
       and "document.addEventListener('touchend',again,true);" in s)
    T2('S-25 색·크기는 있던 칸(c·fs)을 쓴다 — 저장 꼴을 안 바꿨다',
       'var TXT_COLORS=' in s and 'var TXT_SIZES=' in s
       and "id:t.id||('t'+(++TXTSEQ)),x:t.x,y:t.y,w:t.w||0,s:t.s,c:t.c||TXT_C,fs:t.fs||TXT_FS" in s)
    T2('S-27 문항 화면 글상자는 잉크를 안 건드린다 — 통도 키도 다르다',
       "var qtKey=uid=>'q:'+uid;" in s and 'var qKey=uid=>' in s
       and s.count("put('ink',qKey(QUID),QINK)") == 1)
    T2('S-28 문항 글상자 좌표는 문항 필기와 같은 기준(QCW)',
       'txtPaint(h,qtKey(QUID),QCW,QCW,1,true)' in s
       and 'txtAdd(h,qtKey(QUID),QCW,QCW,1,' in s)
    T2('S-29 「T 글상자」 손잡이는 카드 층에서만 만든다',
       # A-6(a) 9/30 — 블록이 if(SHELL)(세 과목)이 된 뒤로 「카드 층에서만」은 안쪽 문 if(HASBOOK){ 가 맡는다(c9faff2 · shell_bio_phys §A 표 HASBOOK 「글상자」)
       blk >= 0 and s.find("b.id='tTxt'") > blk
       and "if(HASBOOK){const tb=document.querySelector('.vbot .tools');\n if(tb&&!document.getElementById('tTxt')){" in s)
    T2('S-26 빈 글상자에 폭을 준다',
       'min-width:2.6em' in s and 'min-width:7em' in s)
    T2('S-16 #book 감싸개는 한 겹뿐',
       s.count('<div id="book" class="sheet hide"><div class="panel">') == 1
       and s.count('#book>.panel{') == 1)
    return out


def main():
    want = [a for a in sys.argv[1:] if a in ('earth', 'bio', 'phys')] or ['earth', 'bio', 'phys']
    cur = open(SRC, encoding='utf-8', newline='').read()
    lines = []
    for mode in (want if not QC.SMOKE else ['earth']):   # smoke — 지학 실행 하나
        ls, snap = run(mode, int(os.environ.get('HARNESS_WAIT', '900')), cur)
        lines += ls
        if mode == 'phys' and QC.GATE and os.path.exists(BASE):   # Y-2 = 관문만(고침 전 사본 · 바탕 띄움)
            base = open(BASE, encoding='utf-8', newline='').read()
            ls0, snap0 = run('physbase', int(os.environ.get('HARNESS_WAIT', '900')), base)
            def T2(name, cond, info=''):
                lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))
            T2('Y-2 고침 전 사본도 끝까지 돌았다', bool(snap and snap0), [bool(snap), bool(snap0)])
            if snap and snap0:
                for k, ko in (('list', '목록'), ('cnt', '문항 수'), ('brand', '머리 칩 줄'),
                              ('tools', '교재 도구줄'), ('pgbar', '교재 칸 머리줄'), ('book', '#book 클래스')):
                    T2('Y-2 ★물리 %s 이(가) 고침 전과 **글자까지** 같다' % ko, snap.get(k) == snap0.get(k),
                       [str(snap.get(k))[:120], str(snap0.get(k))[:120]])
    if not QC.SMOKE:   # smoke — 소스 칸은 smoke 칸이 아님
        lines += static_checks()
    if QC.SMOKE:   # smoke — smoke 칸 줄만
        lines = [x for x in lines if any((x.split(' | ') + ['', ''])[1].startswith(k) for k in _RG_SMOKE)]
    npass = sum(1 for x in lines if x.startswith('PASS'))
    nfail = sum(1 for x in lines if x.startswith('FAIL'))
    for x in lines: print(x)
    print('\n== 지학 3건 %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
