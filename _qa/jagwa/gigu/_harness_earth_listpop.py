# -*- coding: utf-8 -*-
"""자과앱 지학 목록판 — 헤드리스 검산
(2026-09-20 · gigu/_task_jagwa_earth_listpop.md §I)

  C  §A 코드 표시 G02-39-2 · 검색 두 꼴
  M  §B 회차별 │ 단원별
  S  §B 히트맵 차례·빈 칸
  I  §C 「그림」 칩 삭제
  K  §D 머리 「📖 교재」 → 떠 있는 창 · ⤢ 왕복
  V  §E 문항 = 떠 있는 창 (필기 좌표 ±1/1000 · 뒤 목록이 산다)
  P  §F 「교재 자리 목록」 창 (네 꼴 · 쪽 고정 · 오리기 · CROPFOR)
  H  폰(390px iframe) — ≤480px 은 늘 꽉 참
  B  생물 무변 — DOM 글자 대조(HEAD 사본과)
  Y  물리 무변 — DOM 글자 대조(HEAD 사본과)
  0  헛잣대 — HEAD 에서 C·M·V·P 가 FAIL 해야 한다
  Z  원본 대조(파이썬)

⚠ 픽셀 IDENTICAL 게이트는 쓰지 않는다(CLAUDE.md 「자과앱에는 픽셀 게이트를 걸지 않는다」).
   가림·쌓임은 elementsFromPoint · 그려졌는가는 DOM 개수·getBoundingClientRect 로 잰다.
   §I-7 의 「네 꼴 캡처」도 픽셀이 아니라 **DOM 캡처(.html)** 다 — 사람이 열어 보는 것이고 게이트가 아니다.

    PYTHONIOENCODING=utf-8 python _harness_earth_listpop.py
    PYTHONIOENCODING=utf-8 python _harness_earth_listpop.py earth
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import hashlib
import http.server
import io
import json
import os
import shutil
import socketserver
import subprocess
import sys
import threading
import time
import urllib.parse

GENIE = _roots.genie()
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(GENIE, 'jagwa', 'index.html')
BASE_MD5 = '2f896bfeb0857c6ed8991b731f322996'   # 고침 전 md5(LF)
BASE = os.path.join(HERE, '_jagwa_index_before_listpop.html')   # 공개 저장소에 두지 않는다(D11)


def _ensure_base():
    """사본이 없으면 git 에서 꾺낸다 — 큰 파일을 드라이브마다 끌고 다니지 않게."""
    import subprocess
    if os.path.exists(BASE):
        b = open(BASE, 'rb').read()
        if hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest() == BASE_MD5:
            return BASE
    alt = SRC + '.before_listpop'
    if os.path.exists(alt):
        b = open(alt, 'rb').read()
        if hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest() == BASE_MD5:
            return alt
    for rev in ('a9f9fd4~1', '57ebb08', 'HEAD~1'):
        try:
            b = subprocess.run(['git', '-C', GENIE, 'show', rev + ':jagwa/index.html'],
                               capture_output=True).stdout
        except Exception:
            continue
        if b and hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest() == BASE_MD5:
            open(BASE, 'wb').write(b.replace(b'\n', b'\r\n') if b'\r\n' not in b else b)
            print('[base] git %s 에서 꺼냈다' % rev)
            return BASE
    raise SystemExit('NG  고침 전 사본(md5 %s)을 못 찾았다' % BASE_MD5)


BASE = _ensure_base()
SPDROOT = _roots.spd()
OUT = os.path.join(os.environ.get('TEMP', '.'), 'hlistpop')
os.makedirs(OUT, exist_ok=True)
CAP = os.environ.get('LISTPOP_CAP') or os.path.join(HERE, '_cap_listpop')
os.makedirs(CAP, exist_ok=True)
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
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
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

TAIL = r"""
   T('콘솔 오류 0',(window.__err||[]).length===0,window.__err);
  }catch(e){T('예외',false,String(e&&e.stack||e))}
  try{await __nativeFetch('/result',{method:'POST',body:R.join(String.fromCharCode(10))})}catch(e){}
 }
 if(document.readyState==='complete')setTimeout(run,700);else window.addEventListener('load',()=>setTimeout(run,700));
})();
</script>"""

# ══════════════════════════════════════════════════════════════════════════
BODY_EARTH = r"""
   /* ───── 밑준비 ───── */
   await loadEarthData();                      /* ★ 토큰은 위에서 방금 넣었다 — 부팅 때 토큰이 없어 못 받은 것을 여기서 받는다 */
   await until(()=>DATA.length===704,30000);
   ['jagwa.earth.order','jagwa.view.win','jagwa.win.view','jagwa.win.book','jagwa.win.bplist']
     .forEach(k=>{try{localStorage.removeItem(k)}catch(e){}});
   FL.past='y';FL.q='';FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';
   draw(); await wait(250);
   N('밑준비',{subj:SUBJ_ID,ISEA:(typeof ISEA==='undefined')?'(없음)':ISEA,DATA:DATA.length,
              기출:DATA.filter(r=>!isC(r)).length,확인:DATA.filter(isC).length});
   T('E-0 지학 카드 층 · 데이터 적재',SUBJ_ID==='earth'&&CARD_LAYER===true&&DATA.length===704,
     [SUBJ_ID,CARD_LAYER,DATA.length]);

   /* ══════════ C. §A 코드 표시 (게이트 1) ══════════ */
   await grp('C', async()=>{
     const L=nums();
     T('C-1 기출 목록이 319줄이다',L.length===319,L.length);
     const bad=L.filter(x=>!/^G\d{2}-\d{1,2}-\d{1,2}$/.test(x));
     T('C-1 319건 모두 G<연도2>-<회차>-<문번> 꼴이다',bad.length===0,bad.slice(0,6));
     const want=DATA.filter(r=>!isC(r)).reduce((m,r)=>{m[r[F.CODE]]='G'+String((+r[F.ROUND])+1963).slice(2)+'-'+r[F.ROUND]+'-'+String(+r[F.LNO]).padStart(2,'0');return m},{});   /* ★ 2026-09-30 A-6 — jagwa_uid §A-2 순번 두 자리(지학 순번 = 문번 · 319 어긋남 0) */
     const wrong=Object.keys(want).filter(u=>codeShow(rowByUid(u))!==want[u]);
     T('C-1 codeShow 가 319건 모두 규칙대로다',wrong.length===0,wrong.slice(0,5));
     T('C-1 화면 글자가 그 규칙 그대로다(319건 집합 동일)',
       JSON.stringify(L.slice().sort())===JSON.stringify(Object.values(want).sort()));
     T('C-1 G39-02 → G02-39-02',codeShow(rowByUid('G39-02'))==='G02-39-02'&&L.indexOf('G02-39-02')>=0,codeShow(rowByUid('G39-02')));
     T('C-1 G62-09 → G25-62-09',codeShow(rowByUid('G62-09'))==='G25-62-09'&&L.indexOf('G25-62-09')>=0,codeShow(rowByUid('G62-09')));
     T('C-1 G63-01 → G26-63-01',codeShow(rowByUid('G63-01'))==='G26-63-01',codeShow(rowByUid('G63-01')));
     T('C-1 ★uid(F.CODE)는 새 번호다 — 옛 번호로 불러도 그 행(jagwa_uid)',
       rowByUid('G39-02')[F.CODE]==='G02-39-02'&&rowByUid('G62-09')[F.CODE]==='G25-62-09');
     FL.past='p';draw();await wait(200);
     const C=nums();
     T('C-2 확인문제 목록 385줄',C.length===385,C.length);
     T('C-2 확인문제 .num 은 종전 그대로 uid 다',C.every(x=>/^G\d-\d{3}C$/.test(x)),C.slice(0,3));
     FL.past='y';draw();await wait(200);
     /* ★ 2026-09-30 A-6 — jagwa_search(9/29 eb1113e) A-1: 검색칸은 목록을 안 거르고 결과 상자(#esres)·「N건」(#qCnt) ·
        첫 줄 4 · A-3-2: 번호는 보이는 ID(= 새 uid · jagwa_uid)로만 찾는다 — 옛 번호 G39-02 · 옛 보이는 꼴 G02-39-2 는 안 걸린다 */
     $('#q').value='G39-02';esSearch();await wait(160);
     const n1=ES_NOS.length+'|'+txt($('#qCnt'));
     $('#q').value='G02-39-2';esSearch();await wait(160);
     const n2=ES_NOS.length+'|'+txt($('#qCnt'));
     $('#q').value='';esSearch();FL.q='';draw();await wait(160);
     T('C-3 검색 「G39-02」 0건',n1==='0|0건',n1);
     T('C-3 검색 「G02-39-2」 0건',n2==='0|0건',n2);
   });

   /* ══════════ M. §B 차례 모드 (게이트 2) ══════════ */
   await grp('M', async()=>{
     T('M-0 기본은 단원별이다(저장값이 없을 때)',ordMode()==='unit',ordMode());
     T('M-0 「N문제」(모드 글자 없음 — add1 §A)',/^319문제$/.test(txt($('#cnt'))),txt($('#cnt')));
     const seg=document.getElementById('ordSeg');
     T('M-0 개수 줄 #cnt 바로 뒤에 모드 단추가 있다',!!seg&&$('#cnt').nextElementSibling===seg,!!seg);
     T('M-0 「회차별 │ 단원별」 두 칸 · 지금은 단원별이 켜짐',
       !!seg&&[...seg.querySelectorAll('button')].map(b=>txt(b)).join('|')==='회차별|단원별'
       &&seg.querySelector('[data-o="unit"]').classList.contains('on'),
       seg?[...seg.querySelectorAll('button')].map(b=>txt(b)+(b.classList.contains('on')?'*':'')):null);
     const L1=nums(), byU=[];
     {let cur=null;
      [...$('#list').children].forEach(el=>{
        if(el.classList.contains('grouphd')&&el.classList.contains('u')){cur=[];byU.push(cur)}
        else if(el.classList.contains('item')&&cur)cur.push(+txt(el.querySelector('.num')).split('-')[1])});}
     const notDesc=byU.filter(g=>g.some((v,i)=>i&&v>g[i-1]));
     T('M-1 단원 안 차례가 회차 내림이다',notDesc.length===0,notDesc.slice(0,3));
     T('M-1 절 머리·소단원 머리가 그대로 있다',$$$('#list .grouphd:not(.u)').length>0&&$$$('#list .grouphd.u').length>0,
       [$$$('#list .grouphd:not(.u)').length,$$$('#list .grouphd.u').length]);
     seg.querySelector('[data-o="round"]').click(); await wait(260);
     T('M-2 회차별로 바뀌었다',ordMode()==='round'&&/^319문제$/.test(txt($('#cnt'))),[ordMode(),txt($('#cnt'))]);
     const hd=$('#list .grouphd[data-rhd]');   /* ★ 2026-09-30 A-6 — add1 §B: 회차 머리 = 편 꼴(.grouphd.ch · data-rhd · ▾ 다음 .lb) */
     T('M-2 첫 머리가 「63회 · 2026년」이다',!!hd&&txt(hd.querySelector('.lb'))==='63회 · 2026년',hd?txt(hd.querySelector('.lb')):null);
     T('M-2 그 머리에 「10문항」 칸이 있다',!!hd&&txt(hd.querySelector('.p'))==='10문항',hd?txt(hd.querySelector('.p')):null);
     T('M-2 절 머리(.grouphd:not([data-rhd]))가 없다',$$$('#list .grouphd:not([data-rhd])').length===0,$$$('#list .grouphd:not([data-rhd])').length);
     T('M-2 빈 단원 줄(.gh-empty)이 없다',$$$('#list .gh-empty').length===0);
     const L2=nums();
     T('M-2 첫 칸이 G26-63-01 이다',L2[0]==='G26-63-01',L2[0]);
     T('M-2 두 모드의 문항 수 합이 같다(319)',L1.length===319&&L2.length===319,[L1.length,L2.length]);
     T('M-2 두 모드가 **같은 319건**이다(집합 동일)',
       JSON.stringify(L1.slice().sort())===JSON.stringify(L2.slice().sort()));
     const rd=L2.map(x=>+x.split('-')[1]);
     T('M-2 회차 내림 · 같은 회차 안 문번 오름',
       rd.every((v,i)=>!i||v<=rd[i-1])
       && L2.every((x,i)=>!i||(+x.split('-')[1])!==(+L2[i-1].split('-')[1])||(+x.split('-')[2])>(+L2[i-1].split('-')[2])));
     FL.round='62';draw();await wait(160);
     const n62=$$$('#list .item').length;
     T('M-3 회차별에서도 거르개(회차 62)가 먹는다',n62===DATA.filter(r=>!isC(r)&&String(r[F.ROUND])==='62').length&&n62>0,n62);
     FL.round='';FL.bigs=[BIGS[0]];draw();await wait(160);
     const nb=$$$('#list .item').length;
     T('M-3 회차별에서도 장 거르개가 먹는다',nb>0&&nb<319,nb);
     FL.bigs=[];draw();await wait(160);
     T('M-4 모드가 기기 값에 적힌다',localStorage.getItem('jagwa.earth.order')==='round');
     T('M-4 SYNC_KEYS 에 안 넣었다',SYNC_KEYS.indexOf('order')<0&&SUBJ.earth.SYNC_KEYS.indexOf('order')<0);
     FL.past='p';draw();await wait(220);
     T('M-5 확인문제에서 모드 단추가 숨는다',getComputedStyle(document.getElementById('ordSeg')).display==='none',
       getComputedStyle(document.getElementById('ordSeg')).display);
     T('M-5 확인문제는 단원순 고정 · 385건',ordMode()==='unit'&&$$$('#list .item').length===385&&/^385문제$/.test(txt($('#cnt'))),
       [ordMode(),$$$('#list .item').length,txt($('#cnt'))]);
     T('M-5 저장값은 안 건드렸다',localStorage.getItem('jagwa.earth.order')==='round');
     FL.past='y';draw();await wait(220);
     T('M-5 기출로 돌아오면 저장 모드(회차별)다',ordMode()==='round'&&nums()[0]==='G26-63-01',[ordMode(),nums()[0]]);
     treeGo('1.1.2'); await wait(400);
     T('M-6 목차 글자를 누르면 단원별로 바뀐다',ordMode()==='unit'&&localStorage.getItem('jagwa.earth.order')==='unit',
       [ordMode(),localStorage.getItem('jagwa.earth.order')]);
     T('M-6 도착할 단원 머리가 목록에 있다',!!$('#list [data-uhd="1.1.2"]'));
   });

   /* ══════════ S. §B 히트맵 (게이트 3) ══════════ */
   await grp('S', async()=>{
     const legend=()=>['c0','cO','cQ','cX','cP','cWk','cW'].map(i=>txt(document.getElementById(i))).join('/');
     ordSet('unit');draw();await wait(220);
     const lgU=legend();
     const cellsU=$$$('#spec i:not(.gap)'), gapU=$$$('#spec i.gap');
     T('S-1 단원별 · 색 칸 319(빈 칸 제외)',cellsU.length===319,cellsU.length);
     T('S-1 단원별 · 칸 차례가 목록 .num 과 1:1',
       JSON.stringify(cellsU.map(i=>i.title.split(' ')[0]))===JSON.stringify(nums()),
       [cellsU.slice(0,3).map(i=>i.title.split(' ')[0]),nums().slice(0,3)]);
     T('S-1 단원별 · 빈 칸 없음(add1 §A — 묶음 경계 빈 칸 걷음)',gapU.length===0,gapU.length);
     T('S-1 빈 칸은 안 눌린다',gapU.every(g=>!g.onclick)&&gapU.every(g=>getComputedStyle(g).pointerEvents==='none'));
     ordSet('round');draw();await wait(220);
     const lgR=legend();
     const cellsR=$$$('#spec i:not(.gap)'), gapR=$$$('#spec i.gap');
     T('S-2 회차별 · 색 칸 319',cellsR.length===319,cellsR.length);
     T('S-2 회차별 · 칸 차례가 목록 .num 과 1:1',
       JSON.stringify(cellsR.map(i=>i.title.split(' ')[0]))===JSON.stringify(nums()));
     T('S-2 회차별 · 빈 칸 없음(add1 §A — 묶음 경계 빈 칸 걷음)',gapR.length===0,gapR.length);
     T('S-3 범례 수가 두 모드에서 같다',lgU===lgR,[lgU,lgR]);
     ordSet('unit');draw();await wait(220);
     const c7=$$$('#spec i:not(.gap)')[7], want=nums()[7];
     c7.onclick(); await until(()=>VNO!==null,6000); await wait(400);
     T('S-4 칸을 누르면 그 문항이 열린다',VNO!==null&&codeShow(rec(VNO))===want,[VNO&&codeShow(rec(VNO)),want]);
     closeView(); await wait(220);
   });

   /* ══════════ I. §C 「그림」 칩 (게이트 4) ══════════ */
   await grp('I', async()=>{
     draw();await wait(160);
     const g=$$$('#list .item .tag').filter(x=>txt(x)==='그림');
     T('I-1 지학 목록에 「그림」 칩이 0개다',g.length===0,g.length);
     T('I-1 그림이 있는 기출은 그대로 76건이다(F.FILE 무접촉)',
       DATA.filter(r=>!isC(r)&&r[F.FILE]==='IMG').length===76,
       DATA.filter(r=>!isC(r)&&r[F.FILE]==='IMG').length);
   });

   /* ══════════ K. §D 교재 단추 → 떠 있는 창 (게이트 5) ══════════ */
   await grp('K', async()=>{
     T('K-0 실측 — #bpWin 은 DOM 에 없다(그래서 ⤢ 를 새로 단다)',!document.getElementById('bpWin'));
     T('K-0 실측 — #bpBig 은 옆 칸(#bookpane) 안이라 창 머리줄에 없다',
       !!document.getElementById('bpBig')&&!document.querySelector('#book .bkbar #bpBig')
       &&document.getElementById('bpBig').closest('#bookpane')!==null);
     $('#btnBook').click(); await until(()=>BK.pgs&&BK.pgs.length>0,40000); await wait(700);
     const b=$('#book'), p=$('#book>.panel');
     T('K-1 머리 단추를 누르면 **창**으로 뜬다 — #book.win · .panel.float',
       !b.classList.contains('hide')&&b.classList.contains('win')&&p.classList.contains('float'),
       [b.className,p.className]);
     const r0=p.getBoundingClientRect();
     T('K-1 창이 화면을 다 덮지 않는다',r0.width<window.innerWidth-8&&r0.height<window.innerHeight-8,[r0.width,r0.height]);
     T('K-1 손잡이는 교재 머리줄(.bkbar)이다',!!$('#book .bkbar.twhandle'));
     T('K-1 모서리 손잡이가 하나다',$$$('#book .twgrip').length===1,$$$('#book .twgrip').length);
     const bar=$('#book .bkbar');
     await drag(bar,r0.left+150,r0.top+8,r0.left+90,r0.top+58,'mouse'); await wait(200);
     const r1=p.getBoundingClientRect();
     T('K-2 머리줄을 끌면 창이 움직인다',Math.abs(r1.left-(r0.left-60))<3&&Math.abs(r1.top-(r0.top+50))<3,
       [r0.left,r0.top,r1.left,r1.top]);
     const g=$('#book .twgrip'), gr=g.getBoundingClientRect();
     await drag(g,gr.left+4,gr.top+4,gr.left+4+120,gr.top+4+70,'mouse'); await wait(240);
     const r2=p.getBoundingClientRect();
     T('K-2 모서리를 끌면 커진다',Math.abs(r2.width-(r1.width+120))<3&&Math.abs(r2.height-(r1.height+70))<3,
       [r1.width,r1.height,r2.width,r2.height]);
     const sv=JSON.parse(localStorage.getItem('jagwa.win.book')||'null');
     T('K-2 크기가 기기 값에 적힌다',!!sv&&Math.abs(sv.w-r2.width)<2&&Math.abs(sv.h-r2.height)<2,sv);
     const w2=r2.width,h2=r2.height;
     bkClose(); await wait(200); delete WIN.book; $('#book').__float=0;
     $$$('#book .twgrip').forEach(x=>x.remove());
     $('#btnBook').click(); await until(()=>!$('#book').classList.contains('hide'),10000); await wait(600);
     const r3=$('#book>.panel').getBoundingClientRect();
     T('K-3 새로 세워도(기기 값에서) 크기가 그대로다',Math.abs(r3.width-w2)<3&&Math.abs(r3.height-h2)<3,[w2,h2,r3.width,r3.height]);
     const tg=document.getElementById('bkWinTg');
     T('K-4 창 머리줄에 ⤢ 가 있다',!!tg&&tg.closest('.bkbar')!==null&&txt(tg)==='⤢');
     tg.click(); await wait(260);
     T('K-4 ⤢ 누르면 전체 화면(#book.win 이 빠진다)',!$('#book').classList.contains('win'),$('#book').className);
     const rf=$('#book>.panel').getBoundingClientRect();
     const CW=document.documentElement.clientWidth, CH=document.documentElement.clientHeight;
     T('K-4 전체 화면은 화면을 다 덮는다',rf.width>=CW-2&&rf.height>=CH-2,[rf.width,rf.height,CW,CH]);
     tg.click(); await wait(260);
     T('K-4 다시 누르면 창으로 돌아온다',$('#book').classList.contains('win')
       &&$('#book>.panel').getBoundingClientRect().width<window.innerWidth-8);
     T('K-4 ⤢ 를 눌러도 창이 안 끌린다(단추는 끌기에서 빠진다)',
       Math.abs($('#book>.panel').getBoundingClientRect().left-r3.left)<3,
       [$('#book>.panel').getBoundingClientRect().left,r3.left]);
     bkClose(); await wait(240);
   });

   /* ══════════ V. §E 문항 = 떠 있는 창 (게이트 6) ══════════ */
   await grp('V', async()=>{
     ordSet('unit');FL.q='';draw();await wait(220);
     const row0=$$$('#list .item')[3], want0=txt(row0.querySelector('.num'));
     row0.querySelector('.prev').click(); await until(()=>VNO!==null,8000); await wait(600);
     const v=$('#view');
     T('V-1 문제를 누르면 **창**으로 뜬다 — #view.win.float',
       !v.classList.contains('hide')&&v.classList.contains('win')&&v.classList.contains('float'),v.className);
     T('V-1 그 문항이다',codeShow(rec(VNO))===want0,[codeShow(rec(VNO)),want0]);
     const vr=v.getBoundingClientRect();
     T('V-1 창이 화면을 다 덮지 않는다',vr.width<window.innerWidth-8&&vr.height<window.innerHeight-8,[vr.width,vr.height]);
     T('V-1 머리줄(.vtop)이 손잡이다',!!$('#view .vtop.twhandle'));
     T('V-1 모서리 손잡이가 하나다',$$$('#view .twgrip').length===1,$$$('#view .twgrip').length);
     T('V-1 문항 창 머리에 새 코드가 보인다',txt($('#vT1')).indexOf(want0)===0,txt($('#vT1')));
     T('V-1 ◀▶ 목록이 화면 목록 차례다',JSON.stringify(VLIST)===JSON.stringify(LISTNOS),
       [VLIST.slice(0,4),LISTNOS.slice(0,4)]);
     const VH=document.documentElement.clientHeight;
     /* 창은 가운데 72vw 라 줄 **통째**가 창 밖일 수는 없다 — 줄의 **왼쪽 끝 또는 오른쪽 끝 한 점**이 창 밖이면 된다
        (★ 2026-09-30 A-6 — add1 §A 서재 폭 56rem · add9 §A 상주 서랍(body.ndon 왼쪽 여백)으로 목록이 오른쪽으로 밀려 왼쪽 끝은 창 안에 든다) */
     let rowB=null,pxB=0,pyB=0;
     $$$('#list .item').some(el=>{const r=el.getBoundingClientRect();
       if(!(r.width>0&&r.height>0&&r.top>=4&&r.bottom<=VH-4))return false;
       const y=r.top+r.height/2;
       for(const x of [r.left+6,r.right-6])
         if(x<vr.left-4||x>vr.right+4||y<vr.top-4||y>vr.bottom+4){rowB=el;pxB=x;pyB=y;return true}
       return false});
     T('V-2 창 밖에 목록 줄의 한 점이 남아 있다',!!rowB,[vr.left,vr.right,vr.top,vr.bottom]);
     if(rowB){
       const st=stackAt(pxB,pyB);
       const top=document.elementsFromPoint(pxB,pyB)[0];
       T('V-2 ★그 점이 elementsFromPoint 로 목록에 잡힌다(맨 위가 #view 가 아니다)',
         !!top&&top.closest('#list')!==null&&st.indexOf('view')<0,[st.slice(0,4),pxB,pyB]);
       const wantB=txt(rowB.querySelector('.num')), vno0=VNO;
       rowB.querySelector('.prev').click(); await until(()=>VNO!==vno0,7000); await wait(500);
       T('V-2 ★다른 줄을 누르면 같은 창에서 문제만 바뀐다(VNO 만 바뀜)',
         codeShow(rec(VNO))===wantB&&$('#view').classList.contains('win')&&$$$('#view').length===1
         &&$$$('#view .twgrip').length===1,
         [codeShow(rec(VNO)),wantB,$$$('#view .twgrip').length]);}
     const vt=$('#view .vtop'), a0=v.getBoundingClientRect();
     await drag(vt,a0.left+200,a0.top+10,a0.left+150,a0.top+60,'mouse'); await wait(200);
     const a1=v.getBoundingClientRect();
     T('V-3 머리줄을 끌면 창이 움직인다',Math.abs(a1.left-(a0.left-50))<3&&Math.abs(a1.top-(a0.top+50))<3,[a0.left,a0.top,a1.left,a1.top]);
     const g=$('#view .twgrip'), gr=g.getBoundingClientRect();
     await drag(g,gr.left+4,gr.top+4,gr.left+4+100,gr.top+4+60,'mouse'); await wait(260);
     const a2=v.getBoundingClientRect();
     T('V-3 모서리를 끌면 커진다',Math.abs(a2.width-(a1.width+100))<3&&Math.abs(a2.height-(a1.height+60))<3,[a1.width,a1.height,a2.width,a2.height]);
     const sv=JSON.parse(localStorage.getItem('jagwa.win.view')||'null');
     T('V-3 크기가 기기 값에 적힌다',!!sv&&Math.abs(sv.w-a2.width)<2&&Math.abs(sv.h-a2.height)<2,sv);
     const w2=a2.width,h2=a2.height;
     closeView(); await wait(240);
     T('V-3 닫으면 숨는다(win 은 남는다)',$('#view').classList.contains('hide')&&$('#view').classList.contains('win'));
     delete WIN.view; $('#view').__float=0; $$$('#view .twgrip').forEach(x=>x.remove());
     await openView(rowByUid('G62-09')[F.NO]); await wait(600);
     const a3=$('#view').getBoundingClientRect();
     T('V-3 다시 열면(기기 값에서) 크기가 그대로다',Math.abs(a3.width-w2)<3&&Math.abs(a3.height-h2)<3,[w2,h2,a3.width,a3.height]);
     const tg=document.getElementById('vWinTg');
     T('V-4 머리줄에 ⤢ 가 있다',!!tg&&tg.closest('.vtop')!==null);
     tg.click(); await wait(300);
     T('V-4 ⤢ 누르면 전체 화면',!$('#view').classList.contains('win')
       &&$('#view').getBoundingClientRect().width>=document.documentElement.clientWidth-2,
       [$('#view').className,$('#view').getBoundingClientRect().width,document.documentElement.clientWidth]);
     T('V-4 기기 값에 적힌다',localStorage.getItem('jagwa.view.win')==='0');
     /* ── 필기 좌표 — 창 크기가 바뀌어도 저장 좌표가 같아야 한다 ──
        ⚠ 획을 그을 자리는 `underInk`(1401줄)로 **비어 있는 곳**을 골라야 한다.
          밑에 눌릴 것이 있으면 `inkPierce`(1420줄)가 capture 단계에서 stopPropagation 해서
          획이 아예 안 시작된다 — 그것은 앱이 일부러 그렇게 만든 기능이다(짧게 톡 = 선택지).
          자리를 안 고르고 찍으면 하네스가 **앱이 멀쩡한데 FAIL** 을 낸다(2026-09-20 실측). */
     const uidK='G62-09';
     const freeAt=(sv,u,v)=>{const r=sv.getBoundingClientRect();
       const x=r.left+u*r.width, y=r.top+v*r.width;
       if(x<4||y<4||x>document.documentElement.clientWidth-4||y>document.documentElement.clientHeight-4)return false;
       try{return !underInk(x,y,sv)}catch(e){return false}};
     const CAND=[];for(let v=0.03;v<=0.42;v+=0.03)for(let u=0.03;u<=0.48;u+=0.03)CAND.push([+u.toFixed(2),+v.toFixed(2)]);
     const freeSet=sv=>CAND.filter(([u,v])=>freeAt(sv,u,v)&&freeAt(sv,u+0.18,v+0.07)&&freeAt(sv,u+0.36,v+0.14))
                          .map(([u,v])=>u+','+v);
     /* 지금은 전체 화면(V-4 에서 ⤢ 를 눌렀다) */
     await del('ink','qink:'+uidK); await qLoad(uidK); await wait(220);
     setTool('pen'); qWire(); await wait(160);
     const rf0=$('#card #qink').getBoundingClientRect(), AF=freeSet($('#card #qink'));
     /* 카드가 **실제로 줄어드는** 폭으로 창을 좁힌다 — 안 그러면 두 판이 같은 760px 라 잣대가 헛돈다 */
     tg.click(); await wait(300);
     WIN.view={w:620,h:780,l:24,t:24}; vwApply(true); await wait(500);
     T('V-5 창으로 돌아왔다',$('#view').classList.contains('win'));
     qFit();qPaint();qWire(); await wait(200);
     const rw0=$('#card #qink').getBoundingClientRect(), AW=freeSet($('#card #qink'));
     T('V-5 창과 전체 화면의 카드 폭이 실제로 다르다(그래야 잣대가 산다)',
       Math.abs(rw0.width-rf0.width)>20,[rf0.width,rw0.width]);
     const BOTH=AF.filter(x=>AW.indexOf(x)>=0);
     T('V-5 두 판에서 다 비어 있는 자리를 찾았다',BOTH.length>0,[AF.length,AW.length,BOTH.length]);
     const pu=BOTH.length?+BOTH[0].split(',')[0]:0.03, pv=BOTH.length?+BOTH[0].split(',')[1]:0.03;
     const pts=sv=>{const r=sv.getBoundingClientRect();
       return [r.width*pu,r.width*pv,r.width*(pu+0.18),r.width*(pv+0.07),r.width*(pu+0.36),r.width*(pv+0.14)]};
     N('V-5 고른 자리',[pu,pv,BOTH.length]);
     /* 창에서 한 획 */
     await del('ink','qink:'+uidK); await qLoad(uidK); await wait(200); qWire(); await wait(100);
     const svgW=$('#card #qink');
     const trW=await draw1(svgW,pts(svgW));
     const win=(QINK.s||[]).slice(-1)[0];
     T('V-5 창에서 획이 저장됐다',!!win&&win.p.length>=6,[trW,win&&win.p]);
     /* 전체 화면에서 **같은 상대 자리**에 한 획 */
     await del('ink','qink:'+uidK); await qLoad(uidK); await wait(200);
     tg.click(); await wait(450);
     T('V-5 전체 화면으로 갔다',!$('#view').classList.contains('win'));
     qFit();qPaint();qWire(); await wait(200);
     const svgF=$('#card #qink');
     const trF=await draw1(svgF,pts(svgF));
     const full=(QINK.s||[]).slice(-1)[0];
     T('V-5 전체 화면에서 획이 저장됐다',!!full&&full.p.length>=6,[trF,full&&full.p]);
     if(full&&win){
       const n=Math.min(full.p.length,win.p.length);
       const d=[];for(let i=0;i<n;i++)d.push(Math.abs(full.p[i]-win.p[i]));
       T('V-5 ★창 크기를 바꿔 그은 획의 저장 좌표가 전체 화면과 ±1/1000 안이다',
         full.p.length===win.p.length&&d.length>0&&d.every(x=>x<=0.001),
         [d.length?Math.max.apply(null,d):null,full.p,win.p]);}
     T('V-5 필기 통은 그대로 qink:<uid> 다',!!(await get('ink','qink:'+uidK)));
     T('V-5 SYNC_KEYS 에 qink 를 안 넣었다',SYNC_KEYS.indexOf('qink')<0);
     tg.click(); await wait(400);            /* 창으로 되돌린다(기본값) */
     T('V-5 창으로 되돌아왔다',$('#view').classList.contains('win'));
     await mark('O'); await wait(400);
     T('V-6 O 가 기록에 남는다',lastM(rowByUid(uidK)[F.NO])==='O',lastM(rowByUid(uidK)[F.NO]));
     closeView(); await wait(500);          /* 히트맵은 종전대로 draw() 가 다시 그린다(mark 는 안 부른다 — 무변) */
     const idx=nums().indexOf(codeShow(rec(rowByUid(uidK)[F.NO])));
     const cell=$$$('#spec i:not(.gap)')[idx];
     T('V-6 O 를 찍으면 히트맵 칸이 색을 얻는다',idx>=0&&!!cell&&/(^|\s)O(\s|$)/.test(cell.className),[idx,cell&&cell.className]);
     T('V-6 타이머·O△XP·단축키 자리가 그대로다',!!document.getElementById('tm')&&typeof mark==='function');
   });

   /* ══════════ P. §F 교재 자리 목록 창 (게이트 7) ══════════ */
   await grp('P', async()=>{
     /* ★ 2026-09-30 A-6 — jagwa_uid(9/29 5e18424): 기록 열쇠 = 새 번호(G62-09 → G25-62-09) · 옛 열쇠는 앱이 옮긴다(jgMigrate) — 새 열쇠로 넣고 옛 열쇠도 지운다 */
     BPG['G25-62-09']={ps:[5],last:5};
     BPG['G25-62-02']={ps:[5,9,191],last:9};
     delete BPG['G26-63-01'];delete BPG['G62-09'];delete BPG['G62-02'];delete BPG['G63-01'];
     await saveBPG();
     delete CROP['G62-09'];delete CROP['G62-02'];delete CROP['G63-01'];
     delete CROP['G25-62-09'];delete CROP['G25-62-02'];delete CROP['G26-63-01'];await saveCROP();
     ordSet('unit');FL.q='';draw();await wait(260);
     const noA=rowByUid('G62-09')[F.NO], noB=rowByUid('G62-02')[F.NO], noC=rowByUid('G63-01')[F.NO];
     N('P 밑준비',{JOGAK:Object.keys(JOGAK).length,'62-9':!!jogakOf(rowByUid('G62-09')),'63-1':!!jogakOf(rowByUid('G63-01'))});

     /* ── 꼴 ① 고정 한 쪽 ── */
     bplOpen(noA); await wait(250);
     let w=document.getElementById('bpl');
     T('P-1 목록 창이 뜬다',!!w&&!!w.querySelector('.panel'));
     T('P-1 머리줄 한 줄 = 새 코드 + 닫기',txt(w.querySelector('.bplh span'))==='G25-62-09'&&!!w.querySelector('#bplX'),
       txt(w.querySelector('.bplh')));
     let rows=[...w.querySelectorAll('#bplBody .bplrow')];
     T('P-1 고정 한 쪽 → 교재 줄 한 개 + 정리OMR 줄 한 개',rows.length===2,rows.length);
     T('P-1 교재 줄 = 「하이엔드 11판」 11px · 「5쪽」 14px 800 · 「PDF 16」 10px',
       txt(rows[0].querySelector('.bk'))==='하이엔드 11판'&&txt(rows[0].querySelector('.pr'))==='5쪽'
       &&txt(rows[0].querySelector('.pf'))==='PDF 16'
       &&getComputedStyle(rows[0].querySelector('.bk')).fontSize==='11px'
       &&getComputedStyle(rows[0].querySelector('.pr')).fontSize==='14px'
       &&getComputedStyle(rows[0].querySelector('.pr')).fontWeight==='800'
       &&getComputedStyle(rows[0].querySelector('.pf')).fontSize==='10px',
       [txt(rows[0].querySelector('.bk')),txt(rows[0].querySelector('.pr')),txt(rows[0].querySelector('.pf')),
        getComputedStyle(rows[0].querySelector('.pr')).fontSize,getComputedStyle(rows[0].querySelector('.pr')).fontWeight]);
     /* ★ bookwin(2026-09-24) — 지학은 쪽만 고정한 줄 = 「고정한 쪽」(옛 「찍어 둔 자리」 는 📍 찍기와 헷갈렸다) — 둘 다 받는다 */
     T('P-1 딱지 「찍어 둔 자리」(bookwin 뒤 = 「고정한 쪽」)',['찍어 둔 자리','고정한 쪽'].indexOf(txt(rows[0].querySelector('.tg')))>=0,txt(rows[0].querySelector('.tg')));
     T('P-1 미리보기 = 그 쪽이 속한 소단원',/^1\.1\.\d/.test(txt(rows[0].querySelector('.sn'))),txt(rows[0].querySelector('.sn')));
     T('P-1 「후보」 글자가 0이다',w.innerHTML.indexOf('후보')<0);
     T('P-1 정리OMR 줄 = 「정리OMR · 1쪽」',txt(rows[1].querySelector('.bk'))==='정리OMR'&&txt(rows[1].querySelector('.pr'))==='1쪽',
       [txt(rows[1].querySelector('.bk')),txt(rows[1].querySelector('.pr'))]);
     T('P-1 격차·점수·순위를 안 적었다',!/[0-9.]+%|점수|순위/.test(txt(w)));
     await cap('P1_고정1쪽',w.querySelector('.panel').outerHTML);
     bplOpen(noA); await wait(200);
     T('P-1 같은 칩을 다시 누르면 닫힌다',!document.getElementById('bpl'));

     /* ── 꼴 ② 고정 여러 쪽 ── */
     bplOpen(noB); await wait(250);
     w=document.getElementById('bpl');rows=[...w.querySelectorAll('#bplBody .bplrow')];
     T('P-2 고정 세 쪽 → 교재 줄 셋 + 정리OMR 한 개',rows.length===4,rows.length);
     T('P-2 last(9쪽) 인 줄이 위다',txt(rows[0].querySelector('.pr'))==='9쪽',rows.slice(0,3).map(r=>txt(r.querySelector('.pr'))));
     T('P-2 셋 다 딱지가 「찍어 둔 자리」다(bookwin 뒤 = 「고정한 쪽」)',rows.slice(0,3).every(r=>['찍어 둔 자리','고정한 쪽'].indexOf(txt(r.querySelector('.tg')))>=0),rows.slice(0,3).map(r=>txt(r.querySelector('.tg'))));
     T('P-2 PDF 번호 = 인쇄쪽 + 11',rows.slice(0,3).map(r=>txt(r.querySelector('.pf'))).join('|')==='PDF 20|PDF 16|PDF 202',
       rows.slice(0,3).map(r=>txt(r.querySelector('.pf'))));
     T('P-2 「후보」·「자동으로 되돌리기」를 안 그렸다',w.innerHTML.indexOf('후보')<0&&w.innerHTML.indexOf('자동으로 되돌리기')<0);
     await cap('P2_고정여러쪽',w.querySelector('.panel').outerHTML);

     /* ── 꼴 ③ 고정 없음 · 조각 없음 ── */
     bplOpen(noC); await wait(250);
     w=document.getElementById('bpl');rows=[...w.querySelectorAll('#bplBody .bplrow')];
     {const auto=+rowByUid('G63-01')[F.BPAGE]||0;   /* 자동 쪽은 데이터에서 읽는다 — 값을 하네스에 박지 않는다 */
      T('P-3 고정이 없으면 자동 쪽(데이터 값) 한 줄뿐이다',
        rows.length===1&&txt(rows[0].querySelector('.pr'))===auto+'쪽'&&!rows[0].querySelector('.tg'),
        [rows.length,rows[0]&&txt(rows[0].querySelector('.pr')),auto]);}
     T('P-3 「후보」 글자 0',w.innerHTML.indexOf('후보')<0);
     T('P-3 조각이 없으면 「정리OMR 자리가 없다」',txt(w.querySelector('.bplnone'))==='정리OMR 자리가 없다',txt(w.querySelector('.bplnone')));
     await cap('P3_고정없음_조각없음',w.querySelector('.panel').outerHTML);

     /* ── 줄을 누르면 교재 창 그 쪽 · 목록 창은 남는다 ── */
     bplOpen(noA,1); await wait(250);
     w=document.getElementById('bpl');
     w.querySelector('#bplBody .bplrow').click();
     await until(()=>BK.pgs&&BK.pgs.length>0&&bkCurPage(),40000); await wait(1200);
     T('P-4 줄을 누르면 교재 **창**이 그 쪽으로 열린다',
       $('#book').classList.contains('win')&&!!bkCurPage()&&bkCurPage().pr===5,
       [$('#book').className,bkCurPage()&&bkCurPage().pr]);
     T('P-4 목록 창은 그대로 남는다',!!document.getElementById('bpl'));
     /* ★ bookwin §B(2026-09-24) — 창 무리가 있으면 「마지막에 연 창이 맨 앞」 = 나중에 연 교재 창 > 목록 창 · 없으면 옛 CSS 차례 */
     T('P-4 겹침 차례 — 목록 창(76) > 교재 창(70) · 창 무리(bookwin §B)면 나중에 연 교재 창이 위',
       window.wzRaise?+getComputedStyle($('#book')).zIndex>+getComputedStyle(document.getElementById('bpl')).zIndex
         :+getComputedStyle(document.getElementById('bpl')).zIndex>+getComputedStyle($('#book')).zIndex,
       [getComputedStyle(document.getElementById('bpl')).zIndex,getComputedStyle($('#book')).zIndex]);
     T('P-4 교재 창 머리줄에 「붙는 문항 G25-62-09」 칸이 보인다',
       !!document.getElementById('bkFor')&&txt(document.getElementById('bkFor'))==='붙는 문항 G25-62-09',
       txt(document.getElementById('bkFor')));

     /* ── 목록 칩 = 목록 창만(문항을 안 연다) ── */
     bkClose(); {const wx=document.getElementById('bpl'); if(wx)wx.remove();} BPLNO=null; cropFor(null);
     VNO=null; $('#view').classList.add('hide'); draw(); await wait(300);
     const rowA=$$$('#list .item').find(el=>txt(el.querySelector('.num'))==='G25-62-09');
     T('P-5 목록에 그 줄이 있다',!!rowA);
     const chip=rowA.querySelector('[data-page]');
     T('P-5 목록 칩이 「📖 p5」 다',!!chip&&txt(chip)==='📖 p5',txt(chip));
     chip.click(); await wait(500);
     T('P-5 ★목록 칩은 목록 창만 연다 — 문항을 안 연다',
       !!document.getElementById('bpl')&&VNO===null&&$('#view').classList.contains('hide'),
       [!!document.getElementById('bpl'),VNO,$('#view').className]);
     T('P-5 붙는 문항이 그 문항으로 섰다',CROPFOR===noA,[CROPFOR,noA]);
     rowA.querySelector('.prev').click(); await until(()=>VNO!==null,8000); await wait(500);
     T('P-5 카드 본문을 누르면 **문항 창**이 뜬다',VNO===noA&&$('#view').classList.contains('win'),[VNO,$('#view').className]);
     T('P-5 문항을 열면 붙는 문항이 비워진다',CROPFOR===null,CROPFOR);
     closeView(); await wait(260);

     /* ── 문항을 안 연 채 「◻ 오리기」 · 「✎ 쪽 고정」 ── */
     {const wnd=document.getElementById('bpl'); if(wnd)wnd.remove();} BPLNO=null;
     bplOpen(noA); await wait(250);
     w=document.getElementById('bpl');
     /* ★ bookwin §E(2026-09-24) — 목록 창 아랫줄(#bplFoot · ◻ 오리기 · ✎ 쪽 고정)을 걷었다(오리기 = 교재 도구줄 · 쪽 고정 = 카드 ✎).
        아랫줄이 없으면 사람이 하는 길로 — 목록 창 교재 줄을 눌러 교재 창을 열고 도구줄 ◻ 오리기를 켠다(붙는 문항 = 목록 창 문항 그대로) */
     if(w.querySelector('#bplCrop'))w.querySelector('#bplCrop').click();
     else{N('P-6 길','목록 창 아랫줄 없음(bookwin §E) → 교재 줄 → 도구줄 ◻ 오리기');
       w.querySelector('#bplBody .bplrow').click();await until(()=>BK.pgs&&BK.pgs.length>0&&bkCurPage(),40000);await wait(600);
       const tb=$('#bktools [data-tool="crop"]');if(tb&&!tb.classList.contains('on'))tb.click();}
     await until(()=>BK.pgs&&BK.pgs.length>0&&bkCurPage(),40000); await wait(1200);
     T('P-6 「◻ 오리기」가 교재 창을 열고 도구를 켠다',
       $('#book').classList.contains('win')&&!!$('#bktools [data-tool="crop"].on'),
       [$('#book').className,!!$('#bktools [data-tool="crop"].on')]);
     T('P-6 붙는 문항 칸이 그 코드다',txt(document.getElementById('bkFor'))==='붙는 문항 G25-62-09',
       txt(document.getElementById('bkFor')));
     await bkGoto(7); await wait(900);
     N('P-7 교재 창이 보는 쪽',bkCurPage()?bkCurPage().pr:null);
     bpgSheet(noA); await until(()=>!!document.getElementById('bpgSheet'),8000); await wait(400);
     const sh=document.getElementById('bpgSheet'), hb=sh.querySelector('#bpgHere');
     T('P-7 ★「지금 보는 쪽 담기」가 교재 **창**의 쪽을 읽는다',!!hb&&/\(p7\)/.test(txt(hb)),txt(hb));
     hb.click(); await wait(900);
     T('P-7 그 쪽이 담겼다',((BPG['G25-62-09']||{}).ps||[]).indexOf(7)>=0,BPG['G25-62-09']);
     T('P-7 ★문항을 안 연 채로도 목록 칩이 그 자리에서 바뀐다',
       VNO===null&&(()=>{const el=$$$('#list .item').find(x=>txt(x.querySelector('.num'))==='G25-62-09');
         return !!el&&/\+1/.test(txt(el.querySelector('[data-page]')))})(),
       (()=>{const el=$$$('#list .item').find(x=>txt(x.querySelector('.num'))==='G25-62-09');
         return el?txt(el.querySelector('[data-page]')):null})());
     T('P-7 목록 창 줄도 그 자리에서 늘었다',
       !!document.getElementById('bpl')&&$$$('#bplBody .bplrow').length===3,
       $$$('#bplBody .bplrow').map(r=>txt(r.querySelector('.pr'))));
     if(document.getElementById('bpl'))await cap('P4_조각있음_고정둘',document.getElementById('bpl').querySelector('.panel').outerHTML);

     /* ── 문항을 안 연 채 오리기 ── */
     const n0=((CROP['G25-62-09']||{}).q||[]).length;
     T('P-8 오리기 전 조각 0',n0===0,n0);
     cropOffer({p:7,r:[20,30,120,90]},()=>{},null); await wait(250);
     let menu=document.getElementById('crmenu');
     T('P-8 오리기 메뉴가 뜬다(문항을 안 열었는데도 막지 않는다)',!!menu);
     if(menu){menu.querySelector('[data-s="q"]').click(); await wait(1000);}
     T('P-8 ★CROP[G62-09].q 가 +1 이다',((CROP['G25-62-09']||{}).q||[]).length===n0+1,(CROP['G25-62-09']||{}).q);
     T('P-8 그 문항을 안 열었다',VNO===null,VNO);
     draw(); await wait(300);
     const rowA2=$$$('#list .item').find(el=>txt(el.querySelector('.num'))==='G25-62-09');
     rowA2.querySelector('.prev').click(); await until(()=>VNO!==null,8000); await wait(1200);
     T('P-9 ★열면 카드에 조각이 보인다',VNO===noA&&$$$('#card .crbox, #card .cropbox, #card .cropimg, #card canvas').length>0,
       [$$$('#card canvas').length,$('#card .q')?$('#card .q').className:null]);
     T('P-9 문제 칸 글자가 조각에 가려졌다(crophid)',!!$('#card .q.crophid'),$('#card .q')?$('#card .q').className:null);
     await openView(noB); await wait(800);
     T('P-10 다른 문항을 열면 붙는 문항이 비워진다',CROPFOR===null,CROPFOR);
     const b0=((CROP['G25-62-02']||{}).q||[]).length;
     cropOffer({p:9,r:[10,20,90,70]},()=>{},null); await wait(250);
     {const m2=document.getElementById('crmenu'); if(m2)m2.querySelector('[data-s="q"]').click();}
     await wait(900);
     T('P-10 ★조각이 지금 연 문항 B 에 붙는다',((CROP['G25-62-02']||{}).q||[]).length===b0+1
       &&((CROP['G25-62-09']||{}).q||[]).length===n0+1,
       [(CROP['G25-62-02']||{}).q,(CROP['G25-62-09']||{}).q]);
     closeView(); await wait(240);
     /* ── 창 끌기·크기·유지 ── */
     {const w9=document.getElementById('bpl'); if(w9)w9.remove();} BPLNO=null;
     delete WIN.bplist; try{localStorage.removeItem('jagwa.win.bplist')}catch(e){}
     bplOpen(noA); await wait(280);
     const pw=document.getElementById('bpl').querySelector('.panel'), q0=pw.getBoundingClientRect();
     T('P-11 첫 폭이 360px 다',Math.abs(q0.width-360)<2,q0.width);
     T('P-11 배경이 안 막는다(투명 · pointer-events:none)',
       getComputedStyle(document.getElementById('bpl')).pointerEvents==='none'
       &&getComputedStyle(document.getElementById('bpl')).backgroundColor==='rgba(0, 0, 0, 0)',
       [getComputedStyle(document.getElementById('bpl')).pointerEvents,getComputedStyle(document.getElementById('bpl')).backgroundColor]);
     const hh=pw.querySelector('.bplh');
     await drag(hh,q0.left+100,q0.top+8,q0.left+60,q0.top+48,'mouse'); await wait(200);
     const q1=pw.getBoundingClientRect();
     T('P-11 머리줄을 끌면 움직인다',Math.abs(q1.left-(q0.left-40))<3&&Math.abs(q1.top-(q0.top+40))<3,[q0.left,q0.top,q1.left,q1.top]);
     const gg=pw.querySelector('.twgrip'), gq=gg.getBoundingClientRect();
     await drag(gg,gq.left+4,gq.top+4,gq.left+4+80,gq.top+4+50,'mouse'); await wait(260);
     const q2=pw.getBoundingClientRect();
     T('P-11 모서리를 끌면 커진다',Math.abs(q2.width-(q1.width+80))<3&&Math.abs(q2.height-(q1.height+50))<3,[q1.width,q1.height,q2.width,q2.height]);
     const sv2=JSON.parse(localStorage.getItem('jagwa.win.bplist')||'null');
     T('P-11 크기가 기기 값에 적힌다',!!sv2&&Math.abs(sv2.w-q2.width)<2,sv2);
     document.getElementById('bplX').click(); await wait(200);
     T('P-11 닫기 단추로 닫힌다',!document.getElementById('bpl')&&CROPFOR===null);
   });

   /* ══════════ H. 폰(390px iframe) ══════════ */
   await grp('H', async()=>{
     const f=document.createElement('iframe');
     f.style.cssText='position:fixed;left:0;bottom:0;width:390px;height:780px;border:0;z-index:999';
     f.src='/phone.html'; document.body.appendChild(f);
     const ok=await until(()=>{try{return f.contentWindow&&f.contentWindow.__phready===1}catch(e){return false}},90000);
     let err=null;try{err=f.contentWindow.__pherr||null}catch(e){}
     T('H-0 폰 폭(390px) 틀에서 앱이 떴다',ok,[ok,err]);
     if(!ok){f.remove();return}
     const W=f.contentWindow, D=W.document;
     const CW=D.documentElement.clientWidth, CH=D.documentElement.clientHeight;
     T('H-0 틀 안 화면 폭이 480px 아래다',W.innerWidth===390,[W.innerWidth,CW]);
     const v=D.getElementById('view'), vr=v.getBoundingClientRect();
     /* ★ 2026-09-30 A-6 — phone_win(9/28 fb89ad2) §A-1: 폰 문제 창 = 떠 있는 창(폭 화면−16 · 높이 86% · 가운데 · 크기 기억은 makeFloat 그대로 · 꽉 채우기는 ⤢) */
     T('H-1 ★폰에서 문항 창은 떠 있는 창이다(폭 화면−16 · 좌 8 — phone_win §A-1)',v.classList.contains('win')
       &&Math.abs(vr.width-(W.innerWidth-16))<2&&Math.abs(vr.left-8)<2&&vr.top>=6&&vr.bottom<=CH-6,
       [v.className,vr.width,vr.height,vr.left,vr.top,CW,CH]);
     const bp=D.querySelector('#book>.panel');
     T('H-2 폰에서 교재 창도 꽉 찬다',D.getElementById('book').classList.contains('win')
       &&Math.abs(bp.getBoundingClientRect().width-CW)<2,
       [bp.getBoundingClientRect().width,CW]);
     f.remove();
   });

   /* ══════════ 남는 것 ══════════ */
   T('Q-0 SYNC_KEYS 가 그대로 23개다',SYNC_KEYS.length===23&&SUBJ.earth.SYNC_KEYS.length===23,   /* ★ 2026-09-30 A-6 — add1 §G: gg·ggref·pick·link 넷 → 23 */
     [SYNC_KEYS.length,SUBJ.earth.SYNC_KEYS.length]);
   T('Q-0 uid 열쇠 = 새 번호(jagwa_uid) — rowByUid·unitOf 가 F.CODE 로 돈다',
     rowByUid('G39-02')[F.CODE]==='G02-39-02'&&typeof unitOf(rowByUid('G39-02')[F.NO])==='string');
"""

BODY_BIO = r"""
   await loadEarthData();
   await until(()=>DATA.length>600,30000);
   FL.past='y';FL.q='';FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';
   if(CUR.KINDS)FL.types=new Set(['G']);
   draw(); await wait(300);
   T('B-0 생물 카드 층 · 데이터 적재',SUBJ_ID==='bio'&&CARD_LAYER===true&&DATA.length>0,[SUBJ_ID,DATA.length]);
   T('B-1 모드 단추를 안 만든다',!document.getElementById('ordSeg'));
   T('B-1 히트맵에 빈 칸이 없다',$$$('#spec i.gap').length===0,$$$('#spec i.gap').length);
   await openView(DATA[0][F.NO]); await wait(900);
   T('B-2 생물 문항 화면은 **전체 화면**이다(win 없음 · ⤢ 없음 · 모서리 없음)',
     !$('#view').classList.contains('win')&&!$('#view').classList.contains('float')
     &&!document.getElementById('vWinTg')&&$$$('#view .twgrip').length===0,
     [$('#view').className,!!document.getElementById('vWinTg'),$$$('#view .twgrip').length]);
   snap.view=$('#view').className;
   snap.vT1=String($('#vT1').textContent||'');
   snap.cmeta=String((($('#card .cmeta')||{}).textContent)||'').replace(/\s+/g,' ').trim();
   closeView(); await wait(300);
   snap.cnt=String($('#cnt').textContent||'');
   snap.list=$$$('#list .item').slice(0,25).map(el=>String(el.textContent||'').replace(/\s+/g,' ').trim()).join(' || ');
   snap.hd=$$$('#list .grouphd').slice(0,8).map(el=>String(el.textContent||'').replace(/\s+/g,' ').trim()).join(' || ');
   snap.count=String((($('.count')||{}).textContent)||'').replace(/\s+/g,' ').trim();
   snap.spec=$$$('#spec i').length+'/'+$$$('#spec i.gap').length;
   snap.brand=String((($('.brand')||{}).textContent)||'').replace(/\s+/g,' ').trim();
   snap.tools=String(((document.getElementById('bktools')||{}).textContent)||'').replace(/\s+/g,' ').trim();
   snap.book=$('#book')?$('#book').className:'(없음)';
   try{await __nativeFetch('/snap',{method:'POST',body:JSON.stringify(snap)})}catch(e){}
"""

BODY_PHYS = r"""
   await wait(1200);
   T('Y-0 물리 층이다',SUBJ_ID==='phys'&&CARD_LAYER===false,[SUBJ_ID,CARD_LAYER]);
   T('Y-1 카드 층 함수가 아예 없다',typeof ISEA==='undefined'&&typeof codeShow==='undefined'
     &&typeof bplOpen==='undefined'&&typeof ordMode==='undefined'&&typeof cropFor==='undefined'
     &&typeof vwApply==='undefined',
     [typeof ISEA,typeof codeShow,typeof bplOpen,typeof ordMode,typeof cropFor,typeof vwApply]);
   T('Y-1 #view 에 win 이 없고 ⤢ 도 없다',!$('#view').classList.contains('win')&&!document.getElementById('vWinTg'));
   T('Y-1 목록 모드 단추를 안 만든다',!document.getElementById('ordSeg'));
   snap.cnt=String($('#cnt').textContent||'');
   snap.list=$$$('#list .item').slice(0,25).map(el=>String(el.textContent||'').replace(/\s+/g,' ').trim()).join(' || ');
   snap.hd=$$$('#list .grouphd').slice(0,8).map(el=>String(el.textContent||'').replace(/\s+/g,' ').trim()).join(' || ');
   snap.count=String((($('.count')||{}).textContent)||'').replace(/\s+/g,' ').trim();
   snap.spec=$$$('#spec i').length+'/'+$$$('#spec i.gap').length;
   snap.brand=String((($('.brand')||{}).textContent)||'').replace(/\s+/g,' ').trim();
   snap.view=$('#view').className;
   snap.vtop=String((($('#view .vtop')||{}).textContent)||'').replace(/\s+/g,' ').trim();
   snap.book=$('#book')?$('#book').className:'(없음)';
   try{await __nativeFetch('/snap',{method:'POST',body:JSON.stringify(snap)})}catch(e){}
"""

PHONE = r"""<script>
(function(){
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 const until=async(fn,ms)=>{const t0=Date.now();while(Date.now()-t0<(ms||40000)){try{if(fn())return true}catch(e){}await wait(80)}return false};
 const __nf=window.fetch.bind(window);
 window.fetch=async function(url,opt){
  opt=opt||{};const u=String(url);
  const m=/api\.github\.com\/repos\/([^\/]+\/[^\/]+)\/contents\/([^?]+)/.exec(u);
  if(!m){ if(/^https?:/i.test(u))return {ok:false,status:599,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
          return __nf(url,opt); }
  const path=decodeURIComponent(m[2]);
  if(m[1]==='zzikkaplan/notes')return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
  if((opt.method||'GET')==='PUT')return {ok:true,status:200,json:async()=>({content:{sha:'x'}}),text:async()=>''};
  const r=await __nf('/data/'+encodeURI(path),{cache:'no-store'});
  if(!r.ok)return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
  const acc=(opt.headers||{}).Accept||'';
  if(acc.indexOf('raw')>=0)return r;
  return {ok:true,status:200,json:async()=>({sha:'sha'}),text:async()=>JSON.stringify({sha:'sha'})};
 };
 async function go(){
  try{
   localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}));
   await loadEarthData();
   await until(()=>DATA.length===704,50000);
   FL.past='y';draw();await wait(250);
   await openView(DATA[0][F.NO]); await wait(900);
   bkWin(true); $('#book').classList.remove('hide'); await wait(500);
   window.__phready=1;
  }catch(e){window.__pherr=String(e&&e.stack||e)}
 }
 if(document.readyState==='complete')setTimeout(go,800);else window.addEventListener('load',()=>setTimeout(go,800));
})();
</script>"""

CAPHEAD = """<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>교재 자리 목록 — DOM 캡처</title>
<style>
:root{--card:#fff;--paper:#F7F6F2;--line:#E3E1DA;--ink:#16181B;--muted:#767C85;--teal:#2E7D6F}
body{background:#DFE3E7;font:14px/1.5 -apple-system,'Malgun Gothic',sans-serif;color:var(--ink);padding:24px}
.panel{background:var(--card);width:360px;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,.3);overflow:hidden;
  display:flex;flex-direction:column;position:static!important;left:auto!important;top:auto!important;
  width:360px!important;height:auto!important}
.bplh{display:flex;align-items:center;gap:6px;padding:8px 10px;font-size:12.5px;font-weight:700;border-bottom:1px solid var(--line);background:var(--card)}
.bplh button{margin-left:auto;padding:3px 8px;border:1px solid var(--line);border-radius:6px;background:var(--card);font-size:12px}
#bplBody{flex:1;overflow:auto;padding:8px 10px}
#bplFoot{display:flex;gap:6px;padding:8px 10px;border-top:1px solid var(--line);background:var(--card)}
#bplFoot button{padding:4px 9px;border:1px solid var(--line);border-radius:6px;background:var(--card);font:inherit;font-size:12px}
.bplrow{padding:7px 9px;border:1px solid var(--line);border-radius:8px;margin:4px 0;background:var(--card)}
.bplrow .h{display:flex;align-items:baseline;gap:6px;flex-wrap:wrap}
.bplrow .bk{font-size:11px;color:var(--muted)} .bplrow .pr{font-size:14px;font-weight:800;color:var(--ink)}
.bplrow .pf{font-size:10px;color:var(--muted)} .bplrow .tg{font-size:10px;color:var(--muted)}
.bplrow .sn{font-size:11px;color:#4A5661;line-height:1.45;margin-top:2px}
.bplhd{font-size:11px;color:var(--muted);margin:10px 0 2px}
.bplnone{padding:8px 9px;font-size:12px;color:var(--muted)}
.twgrip{display:none}
h1{font-size:13px;color:#4A5661;font-weight:600;margin:0 0 10px}
</style></head><body>
<h1>지학 「교재 자리 목록」 창 — 헤드리스 DOM 캡처(픽셀 게이트 아님 · 사람 눈 확인용)</h1>
"""


def build(mode, src_text):
    subj = {'earth': 'earth', 'earthbase': 'earth', 'bio': 'bio', 'biobase': 'bio',
            'phys': 'phys', 'physbase': 'phys'}[mode]
    body = {'earth': BODY_EARTH, 'earthbase': BODY_EARTH,
            'bio': BODY_BIO, 'biobase': BODY_BIO}.get(mode, BODY_PHYS)
    html = src_text
    html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js',
                        STUB.replace('__SUBJ__', subj) + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    open(os.path.join(OUT, 'app.html'), 'w', encoding='utf-8', newline='').write(
        html.replace('</body>', HEAD + body + TAIL + '</body>', 1))
    open(os.path.join(OUT, 'phone.html'), 'w', encoding='utf-8', newline='').write(
        html.replace('</body>', PHONE + '</body>', 1))
    return subj


def run(mode, secs, src_text):
    subj = build(mode, src_text)
    spd = os.path.join(SPDROOT, subj)
    done = threading.Event()
    box = {}

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=OUT, **k)

        def log_message(self, *a, **k):
            pass

        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            if p.startswith('/data/'):
                rel, pre = p[6:], subj + '/'
                if not rel.startswith(pre):
                    self.send_response(404); self.end_headers(); return
                f = os.path.join(spd, rel[len(pre):].replace('/', os.sep))
                if not os.path.isfile(f):
                    self.send_response(404); self.end_headers(); return
                b = open(f, 'rb').read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', str(len(b)))
                self.send_header('X-Sha', hashlib.sha1(b).hexdigest())
                self.end_headers(); self.wfile.write(b); return
            return super().do_GET()

        def do_POST(self):
            n = int(self.headers.get('Content-Length') or 0)
            body = self.rfile.read(n).decode('utf-8', 'replace')
            self.send_response(204); self.end_headers()
            if self.path.startswith('/partial'):
                box['partial'] = body; return
            if self.path.startswith('/snap'):
                try: box['snap'] = json.loads(body)
                except Exception: box['snap'] = {}
                return
            if self.path.startswith('/cap'):
                q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                nm = (q.get('n') or ['cap'])[0]
                open(os.path.join(CAP, nm + '.html'), 'w', encoding='utf-8', newline='').write(
                    CAPHEAD + body + '</body></html>')
                box.setdefault('caps', []).append(nm)
                return
            box['txt'] = body; done.set()

    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    prof = os.path.join(OUT, 'prof_' + mode)
    shutil.rmtree(prof, ignore_errors=True)
    t0 = time.time()
    p = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
                          '--user-data-dir=' + prof, '--window-size=1500,950',
                          'http://127.0.0.1:%d/app.html' % port],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    got = done.wait(secs)
    p.terminate()
    try: p.wait(10)
    except Exception: p.kill()
    srv.shutdown()
    print('  [%s] %.0fs' % (mode, time.time() - t0))
    if not got:
        return (['FAIL | %s 묶음이 시간 안에 안 끝났다 | %s'
                 % (mode, box.get('partial', '(중간 결과 없음)')[-3000:])], box.get('snap'))
    return ([ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()], box.get('snap'))


def static_checks():
    b = open(SRC, 'rb').read()
    s = b.replace(b'\r\n', b'\n').decode('utf-8')
    base = open(BASE, 'rb').read().replace(b'\r\n', b'\n').decode('utf-8')
    # ★ 2026-09-30 A-6 (d) — Z-1·6·7·10·13 은 이 판(listpop 인도 a9f9fd4)의 패치 꼴을 잰다 — 지금 판은 뒤 판(add1 · shell_bio_phys c9faff2 · add16 · phone_win …)이 바꿨다
    s_lp = subprocess.run(['git', '-C', GENIE, 'show', 'a9f9fd4:jagwa/index.html'], capture_output=True).stdout.replace(b'\r\n', b'\n').decode('utf-8')
    out = []

    def T2(name, cond, info=''):
        out.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))

    # ⚠ 「블록이 열린 뒤」만 보면 안 된다 — 닫는 괄호 **뒤**여도 통과한다(9/20 실측 · Y-1 이 잡았다).
    blk = s_lp.find('\nif(CARD_LAYER){\n')
    end = s_lp.find('\n}\n/*/EARTH:js*/')
    keys = ['var ISEA=', 'var codeShow=', 'function ordBar(', 'var CROPFOR=', 'function cropFor(',
            'function vwApply(', 'function bplOpen(', 'function bplRefresh(']
    T2('Z-1 새 갈래 여덟이 전부 if(CARD_LAYER) **블록 안**이다 — 물리는 만들지도 않는다',
       blk >= 0 and end > blk and all(blk < s_lp.find(k) < end for k in keys),
       [(k, s_lp.find(k), blk, end) for k in keys if not (blk < s_lp.find(k) < end)])
    T2("Z-2 과목 문은 SUBJ_ID==='earth' 다 — CARD_LAYER 로 안 걸었다",
       "var ISEA=SUBJ_ID==='earth';" in s)
    T2('Z-3 uid 를 안 바꿨다 — r[F.CODE] 에 대입하는 자리가 없다',
       s.count('r[F.CODE]=') == 0 and s.count('r[F.CODE] =') == 0)
    SK = ("SYNC_KEYS:['status','note','qtype','conc','gpt','twin','ansfix','frm','maskpos','omrpos',"
          "'mcard','bogi','unit','bpit','bpg','crop','txt','tfix','bref']")
    T2('Z-4 지학 SYNC_KEYS 무변', s.count(SK) == base.count(SK) == 1, [s.count(SK), base.count(SK)])
    T2('Z-5 makeFloat 은 **더하기만** 했다(`.panel` 갈래가 그대로 첫째다)',
       "const p=sheet.querySelector('.panel')||(sheet.classList.contains('selfpanel')?sheet:null);" in s)
    T2('Z-6 makeFloat 을 부르는 자리가 둘 늘었다(문항 창 · 목록 창)',
       s_lp.count('makeFloat(') == base.count('makeFloat(') + 2,
       [s_lp.count('makeFloat('), base.count('makeFloat(')])
    T2('Z-7 「그림」 칩은 지학에서만 안 그린다(줄 자체는 남아 있다)',
       '>그림</span>' in s_lp and "(!ISEA&&r[F.FILE]==='IMG')" in s_lp)
    T2('Z-8 cropOffer 는 CROPFOR||VNO 한 곳에서만 갈린다',
       "const tno=(typeof CROPFOR!=='undefined'&&CROPFOR)||VNO;" in s and s.count('rec(tno)[F.CODE]') == 1)
    T2('Z-9 §F 에서 새로 지은 top-level 함수는 셋이다(bplOpen · bplRefresh · cropFor)',
       s.count('\nfunction bplOpen(') == 1 and s.count('\nfunction bplRefresh(') == 1
       and s.count('\nfunction cropFor(') == 1)
    T2('Z-10 CSS 는 전부 지학 문 안이다(body[data-subj="earth"] · #view.win · #bpl)',
       'body[data-subj="earth"] .ordseg{' in s_lp and '#view.win{' in s_lp and '#bpl{' in s_lp)
    T2('Z-11 줄끝이 CRLF 그대로다', b.count(b'\r\n') == b.count(b'\n'))
    T2('Z-12 원본 대비 늘기만 했다(지운 기능이 없다)', len(s) > len(base))
    T2('Z-13 지운 원본 줄이 없다 — 손댄 자리 밖은 그대로다',
       sum(1 for ln in base.split('\n') if ln.strip() and ln not in s_lp) <= 25,
       sum(1 for ln in base.split('\n') if ln.strip() and ln not in s_lp))
    return out



def data_checks():
    """게이트 8 — §G 데이터 박기.
       옛 본(`_문항_before_bake.json` · git HEAD 에서 떴다)과 지금 본을 맞대고,
       앱 칩 스냅 둘(`_chips_before.json` / `_chips_after.json`)을 글자로 맞댄다."""
    out = []

    def T2(name, cond, info=''):
        out.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))

    old_p = os.path.join(HERE, '_\ubb38\ud56d_before_bake.json')
    # ★ 2026-09-30 A-6 (d) — 옛 본 파일은 N: 에 안 왔고(인도 때 N: 가 떨어져 스크래치패드 · 수행 결과 「미해결」) 지금 문항·기록은 뒤 판(jagwa_uid 4a011475 등)이
    #   바꿨다 ⇒ 박기 커밋에서 읽는다: 옛 = 182e1f3~1 · 새 = 182e1f3 · 기록 = db8ea088(박기가 읽은 savedAt 2026-09-20T09:14:33Z)
    _gs = lambda rev, rel: subprocess.run(['git', '-C', SPDROOT, 'show', rev + ':' + rel], capture_output=True).stdout
    _ob = open(old_p, 'rb').read() if os.path.exists(old_p) else _gs('182e1f3~1', 'earth/\ubb38\ud56d.json')
    if not _ob:
        T2('G-0 옛 본(_문항_before_bake.json)이 있다', False, old_p)
        return out
    old = json.loads(_ob.decode('utf-8'))
    new = json.loads(_gs('182e1f3', 'earth/\ubb38\ud56d.json').decode('utf-8'))
    rec = json.loads(_gs('db8ea088', 'earth/\uae30\ub85d.json').decode('utf-8'))
    UN, BPG = rec['data'].get('unit', {}), rec['data'].get('bpg', {})
    K단원, K쪽, K근거 = '\ub2e8\uc6d0', '\uad50\uc7ac\ucabd', '\ub2e8\uc6d0\uadfc\uac70'

    T2('G-1 행이 704 로 그대로다', len(old) == len(new) == 704, [len(old), len(new)])
    T2('G-1 uid 차례가 그대로다', [x['uid'] for x in old] == [x['uid'] for x in new])
    T2('G-1 열 차례가 그대로다', all(list(a.keys()) == list(b.keys()) for a, b in zip(old, new)))

    cells, rows, badkey = 0, 0, []
    for a, b in zip(old, new):
        ch = [k for k in a if a[k] != b[k]]
        if not ch:
            continue
        rows += 1
        cells += len(ch)
        for k in ch:
            if k not in (K단원, K쪽, K근거):
                badkey.append((a['uid'], k))
    T2('G-2 바뀐 칸은 단원·교재쪽·단원근거 셋뿐이다', not badkey, badkey[:5])
    T2('G-2 바뀐 행 %d · 바뀐 칸 %d (행 × 3 이하)' % (rows, cells), cells <= rows * 3, [rows, cells])
    T2('G-2 바뀐 행이 기록.json 의 손값 건수와 같다', rows == len(set(list(UN) + list(BPG))),
       [rows, len(set(list(UN) + list(BPG)))])

    wrong = []
    for b in new:
        u = b['uid']
        if u in UN and str(b[K단원]) != str(UN[u]):
            wrong.append((u, '\ub2e8\uc6d0', b[K단원], UN[u]))
        if u in BPG:
            o = BPG[u]
            p = (o.get('last') if o.get('last') in (o.get('ps') or []) else (o.get('ps') or [None])[0]) \
                if o.get('ps') else o.get('p')
            if p and int(b[K쪽] or 0) != int(p):
                wrong.append((u, '\uad50\uc7ac\ucabd', b[K쪽], p))
    T2('G-3 손값 114건이 그대로 박혔다', not wrong, wrong[:5])
    T2('G-3 박힌 행은 단원근거가 「사람」이다',
       all(b[K근거] == '\uc0ac\ub78c' for b in new if b['uid'] in UN or b['uid'] in BPG))

    cb = os.path.join(HERE, '_chips_before.json')
    ca = os.path.join(HERE, '_chips_after.json')
    if os.path.exists(cb) and os.path.exists(ca):
        A = json.loads(io.open(cb, encoding='utf-8').read())
        B = json.loads(io.open(ca, encoding='utf-8').read())
        T2('G-4 ★박기 전후 앱 칩 319건 글자가 같다',
           len(A['rows']) == 319 and A['rows'] == B['rows'], [len(A['rows']), len(B['rows'])])
        T2('G-4 개수 줄도 같다', A.get('cnt') == B.get('cnt'), [A.get('cnt'), B.get('cnt')])
        da = {r[0]: r for r in A['data']}
        db = {r[0]: r for r in B['data']}
        T2('G-4 원본 열은 114건이 바뀌었다',
           len([k for k in da if da[k][1:3] != db[k][1:3]]) == 114,
           len([k for k in da if da[k][1:3] != db[k][1:3]]))
        T2('G-4 화면값(unitOf·bpgOf)은 한 건도 안 바뀌었다',
           not [k for k in da if da[k][3:5] != db[k][3:5]],
           [k for k in da if da[k][3:5] != db[k][3:5]][:5])
    else:
        T2('G-4 앱 칩 스냅 둘이 있다', False, [cb, ca])
    return out


def main():
    want = [a for a in sys.argv[1:] if a in ('earth', 'bio', 'phys', 'null')] \
           or ['earth', 'bio', 'phys', 'null']
    cur = open(SRC, encoding='utf-8', newline='').read()
    basetxt = open(BASE, encoding='utf-8', newline='').read()
    # ★ 2026-09-30 A-6 (d) — 생물·물리 무변(B·Y)은 이 판 인도판(a9f9fd4)을 고침 전 사본과 맞댄다 — 지금 판은 뒤 판(shell_bio_phys c9faff2 등)이 생물·물리를 일부러 바꿨다
    lptxt = subprocess.run(['git', '-C', GENIE, 'show', 'a9f9fd4:jagwa/index.html'], capture_output=True).stdout.decode('utf-8')
    lines = []
    W = int(os.environ.get('HARNESS_WAIT', '1500'))

    def T2(name, cond, info=''):
        lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))

    if 'earth' in want:
        ls, _ = run('earth', W, cur)
        lines += ls
    if 'bio' in want:
        ls, sn = run('bio', W, lptxt)
        lines += ls
        ls0, sn0 = run('biobase', W, basetxt)
        T2('B-3 고침 전 사본도 끝까지 돌았다', bool(sn and sn0), [bool(sn), bool(sn0)])
        if sn and sn0:
            for k, ko in (('list', '목록 25줄'), ('cnt', '문항 수'), ('hd', '묶음 머리'),
                          ('count', '개수 줄'), ('spec', '히트맵 칸'), ('brand', '머리 칩 줄'),
                          ('view', '#view 클래스'), ('vT1', '문항 머리'), ('cmeta', '카드 머리줄'),
                          ('tools', '교재 도구줄'), ('book', '#book 클래스')):
                T2('B-3 ★생물 %s 이(가) 고침 전과 **글자까지** 같다' % ko, sn.get(k) == sn0.get(k),
                   [str(sn.get(k))[:140], str(sn0.get(k))[:140]])
    if 'phys' in want:
        ls, sn = run('phys', W, lptxt)
        lines += ls
        ls0, sn0 = run('physbase', W, basetxt)
        T2('Y-3 고침 전 사본도 끝까지 돌았다', bool(sn and sn0), [bool(sn), bool(sn0)])
        if sn and sn0:
            for k, ko in (('list', '목록 25줄'), ('cnt', '문항 수'), ('hd', '묶음 머리'),
                          ('count', '개수 줄'), ('spec', '히트맵 칸'), ('brand', '머리 칩 줄'),
                          ('view', '#view 클래스'), ('vtop', '문항 머리줄'), ('book', '#book 클래스')):
                T2('Y-3 ★물리 %s 이(가) 고침 전과 **글자까지** 같다' % ko, sn.get(k) == sn0.get(k),
                   [str(sn.get(k))[:140], str(sn0.get(k))[:140]])
    if 'null' in want:
        ls0, _ = run('earthbase', W, basetxt)
        fails = [x for x in ls0 if x.startswith('FAIL')]
        for pre, ko in (('C', '§A 코드'), ('M', '§B 모드'), ('V', '§E 문항 창'), ('P', '§F 목록 창')):
            hit = [x for x in fails if x.split(' | ')[1].startswith(pre + '-')
                   or x.split(' | ')[1].startswith(pre + ' 묶음')]
            T2('0-헛잣대 HEAD 에서 %s 묶음이 FAIL 한다' % ko, len(hit) > 0,
               [x.split(' | ')[1][:70] for x in fails][:8])
        T2('0-헛잣대 HEAD 는 통과가 아니다', len(fails) > 0, len(fails))

    lines += static_checks()
    lines += data_checks()
    npass = sum(1 for x in lines if x.startswith('PASS'))
    nfail = sum(1 for x in lines if x.startswith('FAIL'))
    nnote = sum(1 for x in lines if x.startswith('NOTE'))
    for x in lines:
        print(x)
    print('\n== 지학 목록판 %d PASS / %d FAIL / %d NOTE / %d항 ==' % (npass, nfail, nnote, len(lines)))
    print('캡처: %s' % CAP)
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
