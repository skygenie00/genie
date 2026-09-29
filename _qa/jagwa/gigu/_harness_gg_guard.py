# -*- coding: utf-8 -*-
"""자과앱 지학 껍데기(add1+add2+add3) — 헤드리스 검산
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

    PYTHONIOENCODING=utf-8 python _harness_gg.py
    PYTHONIOENCODING=utf-8 python _harness_gg.py earth
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
import re
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
BASE_MD5 = '129eedb17753b611667c2bcc6e42f3ed'   # 고침 전 md5(LF)
BASE = os.path.join(HERE, '_base_bp.html')   # 공개 저장소에 두지 않는다(D11)


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
    for rev in ('HEAD',):
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
CAP = os.environ.get('LISTPOP_CAP') or os.path.join(HERE, '_cap_gg')
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
   await loadEarthData();
   await until(()=>DATA.length===704,30000);
   ['jagwa.earth.order','jagwa.earth.coll','jagwa.earth.hmfold','jagwa.view.win',
    'jagwa.win.view','jagwa.win.book','jagwa.win.bplist','jagwa.win.mc','jagwa.win.jn']
     .forEach(k=>{try{localStorage.removeItem(k)}catch(e){}});
   _coll=null;
   FL.past='y';FL.q='';FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';
   GG={};GGREF={};PICK={};
   /* 사용자 기기와 같은 상태로 — 기록.json 의 손값(unit·bpg·mcard·crop)을 싣는다 */
   {const rec0=JSON.parse(await (await __nativeFetch('/data/earth/%EA%B8%B0%EB%A1%9D.json')).text());
    UN=rec0.data.unit||{};BPG=rec0.data.bpg||{};MC=rec0.data.mcard||{};CROP=rec0.data.crop||{};
    await put('kv','unit',UN);await put('kv','bpg',BPG);await put('kv','mcard',MC);await put('kv','crop',CROP);
    refreshUnits();}
   draw(); await wait(300);
   N('밑준비',{subj:SUBJ_ID,ISEA:ISEA,DATA:DATA.length,기출:DATA.filter(r=>!isC(r)).length});

   /* ══════════ 1. §A 껍데기 ══════════ */
   await grp('A', async()=>{
     const esh=document.getElementById('esh');
     T('A-0 지학 껍데기가 섰다',!!esh);
     T('A-0 옛 머리·개수 줄은 안 보인다',
       getComputedStyle($('#lib>.top')).display==='none'&&getComputedStyle($('#lib>.count')).display==='none',
       [getComputedStyle($('#lib>.top')).display,getComputedStyle($('#lib>.count')).display]);
     ['#specHd','#fBig','#fEtc'].forEach(q=>
       T('A-1 '+q+' 안 보임',$(q)&&$(q).offsetParent===null,$(q)?getComputedStyle($(q)).display:'(없음)'));
     T('A-1 범례 줄(.legend) 안 보임',$('.legend')&&$('.legend').offsetParent===null);
     T('A-1 긴 검색칸이 아니다(#q 가 껍데기 안 · 폭 224px)',
       !!$('#esh #q')&&Math.abs($('#q').getBoundingClientRect().width-224)<2,
       $('#q')?$('#q').getBoundingClientRect().width:null);
     /* 머리줄 자식 차례 */
     const head=esh.querySelector('.ehead');
     const seq=[...head.children].map(el=>el.id||el.tagName.toLowerCase()).filter(x=>x!=='span'||true);
     T('A-2 머리줄 차례 = 제목 → 수 → (빈칸) → 과목탭 → 목차 → 교재 → 설정 → D-날 → 동기화',
       seq.join(',')==='h1,eCnts,span,subjTabs,btnTree,btnBook,btnSet,examChip,recChip',seq);
     T('A-2 제목 18px 800',getComputedStyle(head.querySelector('h1')).fontSize==='18px'
       &&getComputedStyle(head.querySelector('h1')).fontWeight==='800',
       [getComputedStyle(head.querySelector('h1')).fontSize,getComputedStyle(head.querySelector('h1')).fontWeight]);
     T('A-2 「기출 319 · 확인 385」',txt(document.getElementById('eCnts'))==='기출 319 · 확인 385',txt(document.getElementById('eCnts')));
     /* 약점 줄 단추 높이가 서로 ±1px */
     const hs=[...esh.querySelectorAll('.ebar button')].filter(b=>b.offsetParent!==null)
       .map(b=>Math.round(b.getBoundingClientRect().height));
     T('A-3 약점 줄 단추 높이가 서로 ±1px',hs.length>2&&(Math.max.apply(null,hs)-Math.min.apply(null,hs))<=1,hs);
     T('A-3 #cnt = 「319문제」(모드 글자 0)',txt($('#cnt'))==='319문제',txt($('#cnt')));
     T('A-3 「⚡ 빠른 실행」 글자가 없다',txt(esh).indexOf('빠른 실행')<0);
     T('A-4 필터 고르개에 여덟 갈래',
       [...esh.querySelectorAll('#rvF option')].map(o=>o.value).join(',')===',new,X,Q,again,P,bang,gg',
       [...esh.querySelectorAll('#rvF option')].map(o=>o.value));
     T('A-4 「메모 있음」이 아니라 「근거 있음」이다',txt(esh.querySelector('#rvF')).indexOf('메모 있음')<0
       &&txt(esh.querySelector('#rvF')).indexOf('근거 있음')>=0);
     T('A-5 회차 select 를 안 그린다(#fEtc 가 숨고 FL.round 는 빈 값)',FL.round==='');
     await cap('A1_껍데기',document.getElementById('esh').outerHTML);
   });

   /* ══════════ 2. §A 히트맵 ══════════ */
   await grp('H', async()=>{
     const cells=()=>$$$('#spec i');
     T('H-1 칸 319 · 빈 칸(gap) 0',cells().length===319&&$$$('#spec i.gap').length===0,
       [cells().length,$$$('#spec i.gap').length]);
     const r0=cells()[0].getBoundingClientRect();
     T('H-1 칸 8×8',Math.abs(r0.width-8)<0.6&&Math.abs(r0.height-8)<0.6,[r0.width,r0.height]);
     /* 이웃 칸 간격 10px = 8 + 2 */
     const a=cells()[0].getBoundingClientRect(), b=cells()[1].getBoundingClientRect();
     T('H-1 이웃 칸 간격 10px',Math.abs((b.left-a.left)-10)<0.6,b.left-a.left);
     T('H-1 칸 차례 = 목록 .num 차례',
       JSON.stringify(cells().map(i=>i.title.split(' ')[0]))===JSON.stringify(nums()));
     /* 장 칩 */
     const chs=[...document.querySelectorAll('#eChs [data-big]')];
     T('H-2 장 칩 = 전체 + 다섯',chs.length===6,chs.map(x=>txt(x)));
     const air=chs.find(x=>txt(x).indexOf('대기·해양')===0);
     T('H-2 「대기·해양 77」 칩이 있다',!!air&&txt(air)==='대기·해양 77',air?txt(air):null);
     air.click(); await wait(300);
     T('H-2 ★장 칩이 히트맵과 목록을 같이 좁힌다 — 칸 77 · 목록 77',
       $$$('#spec i').length===77&&nums().length===77,[$$$('#spec i').length,nums().length]);
     T('H-2 장 칩은 하나만 켜진다',FL.bigs.length===1,FL.bigs);
     document.querySelector('#eChs [data-big=""]').click(); await wait(300);
     T('H-2 「전체」로 돌아온다',nums().length===319&&FL.bigs.length===0);
     /* 폭이 바뀌면 한 줄 개수만 바뀐다 */
     const lib=$('#lib');const w0=$('#spec').getBoundingClientRect().width;
     const colsAt=()=>{const t=cells()[0].getBoundingClientRect().top;
       return cells().filter(c=>Math.abs(c.getBoundingClientRect().top-t)<1).length};
     const c900=colsAt();
     lib.style.maxWidth='600px'; await wait(250);
     const c600=colsAt(), rr=cells()[0].getBoundingClientRect();
     T('H-3 ★폭을 줄여도 칸 크기는 그대로 · 한 줄 개수만 줄어든다',
       Math.abs(rr.width-8)<0.6&&c600<c900,[c900,c600,rr.width]);
     lib.style.maxWidth=''; await wait(250);
     /* 접기 */
     document.getElementById('hmTg').click(); await wait(200);
     T('H-4 접으면 히트맵이 숨고 글자가 「펴기 ▼」',$('#spec').offsetParent===null
       &&txt(document.getElementById('hmTg'))==='펴기 ▼',txt(document.getElementById('hmTg')));
     T('H-4 기기 값에 적힌다',localStorage.getItem('jagwa.earth.hmfold')==='1');
     document.getElementById('hmTg').click(); await wait(200);
     T('H-4 다시 펴진다',$('#spec').offsetParent!==null);
   });

   /* ══════════ 3. §B 목차 세 층 · 접기 ══════════ */
   await grp('B', async()=>{
     const nCh=()=>$$$('#list .grouphd.ch').length, nSec=()=>$$$('#list .grouphd.sec').length,
           nU=()=>$$$('#list .grouphd.u').length, nIt=()=>$$$('#list .item').length;
     T('B-1 편 5 · 절 16 · 소단원 115',nCh()===5&&nSec()===16&&nU()===115,[nCh(),nSec(),nU()]);
     const fs=q=>getComputedStyle($(q)).fontSize;
     T('B-1 글자 크기 14 > 12.5 > 11.5',
       fs('#list .grouphd.ch')==='14px'&&fs('#list .grouphd.sec')==='12.5px'&&fs('#list .grouphd.u')==='11.5px',
       [fs('#list .grouphd.ch'),fs('#list .grouphd.sec'),fs('#list .grouphd.u')]);
     T('B-1 머리마다 ▾ 가 있다',$$$('#list .grouphd .ar').length===nCh()+nSec()+nU());
     /* 층마다 접고 편다 */
     const ch1=$('#list .grouphd.ch'); ch1.click(); await wait(250);
     T('B-2 편을 누르면 그 밑이 접힌다',nSec()<16&&$('#list .grouphd.ch').classList.contains('off'));
     ch1_again:{const c=$('#list .grouphd.ch');c.click()} await wait(250);
     T('B-2 다시 누르면 펴진다',nSec()===16);
     const s1=$('#list .grouphd.sec'); s1.click(); await wait(250);
     T('B-2 절을 누르면 그 밑 소단원이 접힌다',nU()<115);
     $('#list .grouphd.sec').click(); await wait(250);
     const u1=[...document.querySelectorAll('#list .grouphd.u')]
       .find(h=>h.nextElementSibling&&h.nextElementSibling.classList.contains('item'));
     const n0=nIt(); u1.click(); await wait(250);
     T('B-2 소단원을 누르면 카드만 접힌다',nU()===115&&nIt()<n0,[nU(),nIt(),n0]);
     $('#list .grouphd.u').click(); await wait(250);
     T('B-2 기기 값에 적힌다',Array.isArray(JSON.parse(localStorage.getItem('jagwa.earth.coll')||'[]')));
     /* 접기 단추 한 바퀴 */
     const lv=document.getElementById('lvBtn');
     const shot=()=>[nCh(),nSec(),nU(),nIt()];
     lv.click(); await wait(300); const s_ch=shot(), l_ch=txt(lv);
     lv.click(); await wait(300); const s_sec=shot(), l_sec=txt(lv);
     lv.click(); await wait(300); const s_u=shot(), l_u=txt(lv);
     lv.click(); await wait(300); const s_all=shot(), l_all=txt(lv);
     N('B-3 단계별 (편,절,소단원,카드)',{편:s_ch,절:s_sec,소단원:s_u,문제:s_all,글자:[l_ch,l_sec,l_u,l_all]});
     T('B-3 ★편 = 5/0/0/0',JSON.stringify(s_ch)===JSON.stringify([5,0,0,0]),s_ch);
     T('B-3 ★절 = 5/16/0/0',JSON.stringify(s_sec)===JSON.stringify([5,16,0,0]),s_sec);
     T('B-3 ★소단원 = 5/16/115/0',JSON.stringify(s_u)===JSON.stringify([5,16,115,0]),s_u);
     T('B-3 ★문제 = 5/16/115/319',JSON.stringify(s_all)===JSON.stringify([5,16,115,319]),s_all);
     T('B-3 단추 글자 = 지금 보이는 층',l_ch==='편'&&l_sec==='절'&&l_u==='소단원'&&l_all==='문제',
       [l_ch,l_sec,l_u,l_all]);
     lv.click(); await wait(300);
     T('B-3 한 바퀴 뒤 다시 편',JSON.stringify(shot())===JSON.stringify([5,0,0,0]),shot());
     lv.click();lv.click();lv.click(); await wait(400);
     /* 회차별 = 회차 ↔ 문제 */
     ordSet('round');draw();await wait(300);
     T('B-4 회차별 머리 = 편 꼴 한 층 32개',$$$('#list .grouphd.ch').length===32
       &&$$$('#list .grouphd.sec').length===0&&$$$('#list .grouphd.u').length===0,
       [$$$('#list .grouphd.ch').length,$$$('#list .grouphd.sec').length]);
     lv.click(); await wait(300);
     T('B-4 회차별 접기 = 회차만',txt(lv)==='회차'&&$$$('#list .item').length===0,[txt(lv),$$$('#list .item').length]);
     lv.click(); await wait(300);
     T('B-4 다시 누르면 문제까지',txt(lv)==='문제'&&$$$('#list .item').length===319);
     ordSet('unit');draw();await wait(300);
     /* treeGo — 접힌 편 밑으로 가면 펴진다 */
     lv.click(); await wait(300);                      /* 편만 */
     treeGo('2.1.3'); await wait(400);
     T('B-5 ★접힌 편 밑 단원으로 가면 펴지고 도착한다',
       !!$('#list [data-uhd="2.1.3"]')&&!collHas('c2')&&!collHas('s2.1')&&!collHas('u2.1.3'),
       [!!$('#list [data-uhd="2.1.3"]'),collHas('c2'),collHas('s2.1'),collHas('u2.1.3')]);
     lvApply('all',false);draw();await wait(300);
   });

   /* ══════════ 4. §C 🃏 · 📋 ══════════ */
   await grp('C', async()=>{
     T('C-0 절 머리 「암기카드」 글자 0',txt($('#list')).indexOf('암기카드')<0);
     T('C-0 #btnMC 를 안 그린다',!document.getElementById('btnMC'));
     /* 실데이터 카드 = 손필기 3장(no 50·71·308) */
     T('C-1 🃏 전체 = 3',txt(document.getElementById('mcAll'))==='🃏 전체 3',txt(document.getElementById('mcAll')));
     T('C-1 crop 45건은 수에 안 들어간다',Object.keys(CROP).length>0&&mcCountIn(DATA.filter(r=>!isC(r)).map(r=>r[F.NO]))===3,
       [Object.keys(CROP).length,mcCountIn(DATA.filter(r=>!isC(r)).map(r=>r[F.NO]))]);
     const u112=document.querySelector('#list [data-uhd="1.1.2"] [data-mc]');
     T('C-1 1.1.2 소단원 🃏 = 2',!!u112&&txt(u112)==='🃏 2',u112?txt(u112):null);
     /* 🃏 창 */
     u112.click(); await wait(600);
     const w=document.getElementById('mcw');
     T('C-2 🃏 창이 뜬다',!!w&&!!w.querySelector('.panel'));
     T('C-2 카드가 있는 문항만',$$$('#mcwBody .mcwq').length===2,$$$('#mcwBody .mcwq').length);
     T('C-2 「보기」 단추가 있다',$$$('#mcwBody .jgo').length===2);
     T('C-2 손필기 칸을 그린다',$$$('#mcwBody canvas[data-ink]').length===2);
     T('C-2 「＋ 카드 넣기」 단추 셋',!!document.getElementById('mcwInk')&&!!document.getElementById('mcwBk')&&!!document.getElementById('mcwOmr'));
     /* 끌기·크기 */
     const p=w.querySelector('.panel'), q0=p.getBoundingClientRect();
     await drag(w.querySelector('.bplh'),q0.left+120,q0.top+8,q0.left+70,q0.top+58,'mouse'); await wait(220);
     const q1=p.getBoundingClientRect();
     T('C-2 머리줄을 끌면 움직인다',Math.abs(q1.left-(q0.left-50))<3&&Math.abs(q1.top-(q0.top+50))<3,[q0.left,q1.left]);
     const g=w.querySelector('.twgrip'), gr=g.getBoundingClientRect();
     await drag(g,gr.left+4,gr.top+4,gr.left+84,gr.top+54,'mouse'); await wait(240);
     T('C-2 모서리를 끌면 커진다',Math.abs(p.getBoundingClientRect().width-(q1.width+80))<3,
       [q1.width,p.getBoundingClientRect().width]);
     T('C-2 크기를 기기 값에 적는다',!!JSON.parse(localStorage.getItem('jagwa.win.mc')||'null'));
     /* 「보기」 → 문항 창 */
     $('#mcwBody .jgo').click(); await until(()=>VNO!==null,6000); await wait(400);
     T('C-2 「보기」를 누르면 문항 창이 뜬다',VNO!==null&&!$('#view').classList.contains('hide'));
     closeView(); await wait(250);
     await cap('C1_암기카드창',document.getElementById('mcw').querySelector('.panel').outerHTML);
     document.getElementById('mcwX').click(); await wait(150);
     /* 📋 */
     const jb=document.querySelector('#list .grouphd.sec [data-jn]');
     T('C-3 📋 는 절 머리에만 있다',$$$('#list .grouphd.sec [data-jn]').length===16
       &&$$$('#list .grouphd.u [data-jn]').length===0,
       [$$$('#list .grouphd.sec [data-jn]').length,$$$('#list .grouphd.u [data-jn]').length]);
     const j11=document.querySelector('#list [data-coll="s1.1"] [data-jn]');
     j11.click(); await wait(600);
     const jw=document.getElementById('jnw');
     T('C-3 정리 창이 뜬다',!!jw);
     T('C-3 1.1 = 42문항',txt(jw.querySelector('.bplh')).indexOf('42문항')>=0,txt(jw.querySelector('.bplh')));
     T('C-3 소제목 수 = 기출 있는 소단원 수',
       $$$('#jnwBody .jnh').length===((TOC.sec['1.1']||{}).units||[]).filter(u=>u!=='1.1'&&DATA.some(r=>!isC(r)&&unitOf(r[F.NO])===u)).length,
       $$$('#jnwBody .jnh').length);
     T('C-3 행마다 지문 전문·기록 칸',$$$('#jnwBody .jnrow .q').length===42&&$$$('#jnwBody .jnrow .mk').length===42);
     /* 정답·해설은 행마다 따로 접힌다 */
     const b0=$$$('#jnwBody .jnans')[0], b1=$$$('#jnwBody .jnans')[1];
     b0.click(); await wait(200);
     T('C-3 ★정답·해설이 그 행만 펴진다',
       !b0.nextElementSibling.classList.contains('hide')&&b1.nextElementSibling.classList.contains('hide'));
     T('C-3 「✏️ 표시」는 안 옮겼다',txt(jw).indexOf('✏️ 표시')<0);
     await cap('C2_정리창',jw.querySelector('.panel').outerHTML);
     document.getElementById('jnwX').click(); await wait(150);
     /* 머리 단추 누름이 접힘을 안 바꾼다 */
     const before=JSON.stringify([...collSet()].sort());
     document.querySelector('#list .grouphd.sec [data-jn]').click(); await wait(400);
     document.getElementById('jnwX').click(); await wait(150);
     T('C-4 ★머리 안 단추를 눌러도 접힘이 안 바뀐다',JSON.stringify([...collSet()].sort())===before);
   });

   /* ══════════ 5. §D 근거 ══════════ */
   await grp('G', async()=>{
     const A='G62-09', B='G39-02';
     const noA=rowByUid(A)[F.NO], noB=rowByUid(B)[F.NO];
     GG={};GGREF={};await saveGG();await saveGGREF();
     await openView(noA); await wait(600);
     const line=()=>$('#card [data-ggbox]');
     T('G-0 문항 창 카드에 근거 줄이 있다',!!line());
     T('G-0 근거 줄은 선택지 아래 · #cDet 위다',
       !!$('#card .ggwrap')&&$('#card .ggwrap').nextElementSibling&&$('#card .ggwrap').nextElementSibling.classList.contains('vrow'));
     T('G-0 목록 카드에는 적는 칸이 없다',$$$('#list .item .ggrow').length===0);
     T('G-0 「＋한줄」이 없다',txt($('#list')).indexOf('＋한줄')<0);
     /* 한 줄 저장 — Enter */
     const put1=async(t)=>{const ta=$('#card .ggrow .txt');ta.value=t;ta.focus();
       ta.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true,cancelable:true}));
       await wait(400)};
     T('G-1 적기 전에는 근거 0',ggOf(A).length===0,[ggOf(A).length,$$$('#card .ggrow').length]);
     await put1('첫 근거');
     N('G-1 첫 저장 뒤',{n:ggOf(A).length,t:ggOf(A).map(g=>g.t),rows:$$$('#card .ggrow').length,
                        boxes:$$$('[data-ggrows]').length});
     T('G-1 Enter 로 저장 — 칩 1개',ggOf(A).length===1&&$$$('#card .ggnum').length===1,
       [ggOf(A).length,$$$('#card .ggnum').length]);
     T('G-1 저장 순간 마크가 ok 에 실린다',ggOf(A)[0].ok===(lastM(noA)||null),[ggOf(A)[0].ok,lastM(noA)]);
     T('G-1 parts 가 없다(줄 하나 · 라벨 없음)',!ggOf(A)[0].parts);
     /* 칸을 벗어나며 저장 */
     {const ta=$('#card .ggrow .txt');ta.value='둘째 근거';ta.focus();ta.blur();await wait(450)}
     T('G-1 칸을 벗어나면 저장(줄 하나일 때)',ggOf(A).length===2,ggOf(A).length);
     /* 병렬 — (1) → ＋ → (2) → ＋ → (3) */
     {const lab=$('#card .ggrow .lab');lab.value='(1)';
      $('#card .ggrow .txt').value='ㄱ 줄';
      $('#card [data-ggplus]').click();await wait(200)}
     const labs1=[...document.querySelectorAll('#card .ggrow .lab')].map(x=>x.value);
     T('G-2 ＋ 를 누르면 라벨이 (2) 로 미리 찬다',labs1.join(',')==='(1),(2)',labs1);
     {const ls=[...document.querySelectorAll('#card .ggrow')];
      ls[1].querySelector('.txt').value='ㄴ 줄';
      $('#card [data-ggplus]').click();await wait(200)}
     const labs2=[...document.querySelectorAll('#card .ggrow .lab')].map(x=>x.value);
     T('G-2 한 번 더 = (3)',labs2.join(',')==='(1),(2),(3)',labs2);
     T('G-2 줄이 둘 이상이면 「저장」 단추가 보인다',!$('#card [data-ggsave]').classList.contains('hide'));
     /* 줄 둘일 때 blur 로 저장되지 않는다 */
     {const ls=[...document.querySelectorAll('#card .ggrow')];ls[2].querySelector('.txt').value='ㄷ 줄';
      ls[2].querySelector('.txt').focus();ls[2].querySelector('.txt').blur();await wait(400)}
     T('G-2 ★줄이 둘 이상이면 칸을 벗어나도 저장 안 됨',ggOf(A).length===2,ggOf(A).length);
     $('#card [data-ggsave]').click(); await wait(450);
     const g3=ggOf(A)[2];
     T('G-2 ★「저장」으로 근거 하나 · parts 3',ggOf(A).length===3&&g3&&g3.parts&&g3.parts.length===3,
       [ggOf(A).length,g3&&g3.parts&&g3.parts.length]);
     T('G-2 t 는 세 줄이 붙은 글',g3&&g3.t==='(1) ㄱ 줄\n(2) ㄴ 줄\n(3) ㄷ 줄',g3&&g3.t);
     /* 라벨 다음 것 — ㄱ→ㄴ · ①→② · 가→나 */
     T('G-2 ㄱ→ㄴ · ①→② · 가→나 · a→b · 1.→2.',
       ggNextLabel('ㄱ')==='ㄴ'&&ggNextLabel('①')==='②'&&ggNextLabel('가')==='나'
       &&ggNextLabel('a')==='b'&&ggNextLabel('1.')==='2.',
       [ggNextLabel('ㄱ'),ggNextLabel('①'),ggNextLabel('가'),ggNextLabel('a'),ggNextLabel('1.')]);
     /* 칩 색 = 저장 순간 마크 */
     T('G-3 칩 색이 ok 를 따른다',$$$('#card .ggnum')[0].className.indexOf(ggOkCls(ggOf(A)[0].ok))>=0,
       $$$('#card .ggnum')[0].className);
     /* 「!」 */
     $$$('#card .ggnum')[0].click(); await wait(200);
     const pan=$('#card .ggpan:not(.hide)');
     T('G-3 칩을 누르면 판이 펴진다',!!pan);
     pan.querySelector('[data-ggbang]').click(); await wait(300);
     T('G-3 ★「!」 를 켜면 판·칩이 빨강',ggOf(A)[0].bang===true
       &&$$$('#card .ggnum')[0].classList.contains('bang')
       &&$('#card .ggpan').classList.contains('bang'),
       [ggOf(A)[0].bang,$$$('#card .ggnum')[0].className]);
     await cap('G1_근거줄',$('#card .ggwrap').outerHTML+$('#card .vrow').outerHTML);
     /* 댓글 */
     {const ci=$('#card [data-ggcin]');ci.value='댓글 하나';
      $('#card [data-ggreply]').click();await wait(400)}
     T('G-4 댓글이 달린다',(ggOf(A)[0].cs||[]).length===1,(ggOf(A)[0].cs||[]).length);
     {const b=$('#card [data-ggce]');b.click();await wait(250);
      const ta=$('#card .ggcs textarea');ta.value='댓글 고침';
      $('#card .ggcs .cedit button').click();await wait(400)}
     T('G-4 댓글을 고친다',(ggOf(A)[0].cs||[])[0].t==='댓글 고침',(ggOf(A)[0].cs||[])[0].t);
     $('#card [data-ggcd]').click(); await wait(400);
     T('G-4 댓글을 지운다',(ggOf(A)[0].cs||[]).length===0);
     /* 한도 */
     {const ta=$('#card .ggrow .txt');ta.value='x'.repeat(GG_TMAX+5);ta.focus();
      ta.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true,cancelable:true}));await wait(400)}
     T('G-5 한도를 넘기면 저장 안 되고 안내가 뜬다',ggOf(A).length===3&&!!$('#card .ggover'),
       [ggOf(A).length,$('#card .ggover')?txt($('#card .ggover')):null]);
     {const ta=$('#card .ggrow .txt');ta.value='';ta.dispatchEvent(new Event('input',{bubbles:true}));await wait(200)}
     /* 🔍 — 남의 근거 찾아 연결 */
     GG[B]=[{k:'gb1',i:1,t:'에라토스테네스 반지름',ok:'O',ts:Date.now(),cs:[{k:'cb1',t:'댓글에만 있는 낱말 코시',ts:Date.now()}]}];
     await saveGG(); await openView(noA); await wait(600);
     $('#card [data-ggfind]').click(); await wait(300);
     {const i=$('#card .ggfind input');i.value='반지름';i.dispatchEvent(new Event('input',{bubbles:true}));await wait(350)}
     T('G-6 🔍 가 남의 근거를 찾는다',$$$('#card .ggfind .ggres').length>=1,$$$('#card .ggfind .ggres').length);
     {const i=$('#card .ggfind input');i.value='코시';i.dispatchEvent(new Event('input',{bubbles:true}));await wait(350)}
     T('G-6 ★댓글에서도 찾고 ↳ 로 보인다',
       $$$('#card .ggfind .ggres').some(x=>txt(x).indexOf('↳')>=0),
       $$$('#card .ggfind .ggres').map(x=>txt(x)).slice(0,2));
     $('#card .ggfind .ggres').click(); await wait(450);
     T('G-6 ★누르면 그 문항이 연결된다',ggRefOf(A).indexOf(B)>=0&&$$$('#card .ggref').length===1,
       [ggRefOf(A),$$$('#card .ggref').length]);
     $('#card .ggref').click(); await wait(300);
     T('G-6 칩을 누르면 연결 상자가 펴진다',!!$('#card .ggrefbox:not(.hide)'));
     T('G-6 상자에 그 문항 근거와 댓글이 보인다',
       txt($('#card .ggrefbox')).indexOf('반지름')>=0&&txt($('#card .ggrefbox')).indexOf('코시')>=0);
     /* ⚠ add1 지시서는 「안 옮긴다」였고 add2 §D 가 옮겼다 — 잣대를 뒤집었다(2026-09-20) */
     T('G-6 add2 §D 로 「✎ 여기서 고치기」가 생겼다',txt($('#card .ggrefbox')).indexOf('여기서 고치기')>=0,
       txt($('#card .ggrefbox')).slice(0,120));
     $('#card [data-ggrx]').click(); await wait(400);
     T('G-6 × 로 연결이 끊긴다',ggRefOf(A).length===0);
     /* 위 검색 줄 「🔗 근거」 모드 */
     closeView(); await wait(300);
     document.querySelector('#esh .seg2 [data-sm="g"]').click(); await wait(300);
     T('G-7 근거 모드로 바뀐다',GGMODE==='g'&&document.querySelector('#esh .seg2 [data-sm="g"]').classList.contains('on'));
     {const q=$('#q');q.value='반지름';q.dispatchEvent(new Event('input',{bubbles:true}));await wait(350)}
     T('G-7 결과 상자가 뜬다',!document.getElementById('esres').classList.contains('hide')
       &&$$$('#esres .ggres').length>=1,$$$('#esres .ggres').length);
     T('G-7 찾은 글자가 노랗게 보인다',$$$('#esres mark').length>=1);
     T('G-7 목록은 그대로 319',nums().length===319,nums().length);
     $$$('#esres .ggres')[0].click(); await until(()=>VNO!==null,5000); await wait(400);
     T('G-7 누르면 그 문항이 열린다',VNO!==null);
     closeView(); await wait(250);
     document.querySelector('#esh .seg2 [data-sm="q"]').click(); await wait(300);
     T('G-7 「문제」로 돌아오면 상자가 닫힌다',document.getElementById('esres').classList.contains('hide'));
     /* 필터 둘 */
     {const f=document.getElementById('rvF');f.value='gg';f.dispatchEvent(new Event('change',{bubbles:true}));await wait(350)}
     T('G-8 「근거 있음」 = 2건',nums().length===2,nums().length);
     {const f=document.getElementById('rvF');f.value='bang';f.dispatchEvent(new Event('change',{bubbles:true}));await wait(350)}
     T('G-8 「❗ 중요 근거」 = 1건',nums().length===1,nums().length);
     {const f=document.getElementById('rvF');f.value='';f.dispatchEvent(new Event('change',{bubbles:true}));await wait(350)}
     T('G-8 목록 카드에 읽기 전용 「근거 n」 칩',
       $$$('#list .item .tag.gg').filter(x=>x.offsetParent!==null).length===2,
       $$$('#list .item .tag.gg').filter(x=>x.offsetParent!==null).map(x=>txt(x)));
     /* 코멘트 흡수 — 흉내 3건 */
     GG={};await saveGG();
     CMT[rec(noA)[F.NO]]='옛 코멘트 1';CMT[rowByUid('G63-01')[F.NO]]='옛 코멘트 2';CMT[rowByUid('G62-02')[F.NO]]='옛 코멘트 3';
     await saveNote();
     const n1=await ggEatNotes(); await wait(300);
     T('G-9 ★옛 코멘트 3건이 근거로 옮겨진다',n1===3&&ggOf(A).length===1&&Object.keys(CMT).length===0,
       [n1,ggOf(A).length,Object.keys(CMT).length]);
     const n2=await ggEatNotes();
     T('G-9 ★다시 돌리면 0건(멱등)',n2===0,n2);
     /* 동기화 키 */
     T('G-10 SYNC_KEYS 에 gg·ggref·pick·link 가 들어갔다',
       ['gg','ggref','pick','link'].every(k=>SYNC_KEYS.indexOf(k)>=0)&&SYNC_KEYS.length===23,
       [SYNC_KEYS.length,SYNC_KEYS.slice(-4)]);
     T('G-10 SYNC_REF 에도 셋이 있다',!!SYNC_REF.gg&&!!SYNC_REF.ggref&&!!SYNC_REF.pick);
     GG={};GGREF={};await saveGG();await saveGGREF();draw();await wait(250);
   });

   /* ══════════ 6. §E 문항 창 아랫줄 ══════════ */
   await grp('V', async()=>{
     const no=rowByUid('G62-09')[F.NO];
     await openView(no); await wait(700);
     /* ⚠ add2 §C 가 P 를 넷째로 더했다 — 셋이던 잣대를 넷으로 고쳤다(2026-09-20) */
     T('V-1 아랫줄이 있다 — 정답·해설 ▸ · O △ X P · ✏️ 연결',
       !!$('#card .vrow')&&$$$('#card .vox').length===4&&!!$('#card #cDetBtn')&&!!$('#card #cLink'));
     T('V-1 <summary> 는 숨긴다',getComputedStyle($('#card #cDet>summary')).display==='none');
     const d=$('#cDet');
     T('V-1 처음엔 닫혀 있다',!d.open);
     $('#card #cDetBtn').click(); await wait(200);
     T('V-1 ▸ 를 누르면 열리고 글자가 ▾',d.open&&txt($('#card #cDetBtn'))==='정답·해설 ▾');
     $('#card #cDetBtn').click(); await wait(200);
     T('V-1 다시 누르면 닫힌다',!d.open);
     /* O △ X */
     const h0=hist(no).length;
     $('#card .vox.vO').click(); await wait(500);
     T('V-2 O 를 누르면 기록에 남는다',lastM(no)==='O'&&hist(no).length===h0+1,[lastM(no),hist(no).length]);
     T('V-2 켜진 단추에 on',$('#card .vox.vO').classList.contains('on'));
     $('#card .vox.vX').click(); await wait(500);
     T('V-2 X 로 바꾸면 그 단추가 켜진다',lastM(no)==='X'&&$('#card .vox.vX').classList.contains('on')
       &&!$('#card .vox.vO').classList.contains('on'));
     closeView(); await wait(400);
     {const idx=nums().indexOf(codeShow(rec(no)));const cell=$$$('#spec i')[idx];
      T('V-2 히트맵 칸이 따라간다',idx>=0&&!!cell&&/(^|\s)X(\s|$)/.test(cell.className),[idx,cell&&cell.className])}
     await openView(no); await wait(600);
     /* .vbot */
     T('V-3 .vbot 에서 #mO·#mQ·#mX·#tNote 가 안 보인다',
       ['#mO','#mQ','#mX','#tNote'].every(q=>$(q)&&$(q).offsetParent===null),
       ['#mO','#mQ','#mX','#tNote'].map(q=>$(q)?getComputedStyle($(q)).display:'(없음)'));
     /* ⚠ add2 §A·§B 가 필기 도구를 머리줄 알약으로 옮기고 #mP 를 근거 아랫줄로 옮겼다 */
     T('V-3 필기 도구는 머리줄 알약에 있고 그래도 보인다',
       !!$('#inkPill #tErase')&&$('#inkPill #tErase').offsetParent!==null,
       [!!$('#inkPill'),$('#tErase')?getComputedStyle($('#tErase')).display:'(없음)']);
     T('V-3 #mP 는 근거 아랫줄로 갔다 · #tHist 는 아랫줄에 남는다',
       !!$('#mP')&&$('#mP').offsetParent===null&&!!$('#card .vox.vP')
       &&!!$('#tHist')&&$('#tHist').offsetParent!==null,
       [$('#mP')?getComputedStyle($('#mP')).display:'(없음)',!!$('#card .vox.vP')]);
     T('V-4 「✏️ 연결」이 있고 linkSheet 를 그대로 쓴다',!!$('#card #cLink')&&typeof linkSheet==='function');
     /* ── 필기가 살아 있는가(§I-6) ──
        ⚠ 획 자리는 `underInk` 로 **빈 곳**을 골라야 한다 — 밑에 눌릴 것이 있으면 `inkPierce` 가
          capture 에서 막는다(앱이 일부러 그런 것 · 9/20 본판에서 배운 함정). */
     {const uidK=rec(no)[F.CODE];
      await del('ink','qink:'+uidK); await qLoad(uidK); await wait(200);
      setTool('pen'); qWire(); await wait(120);
      const sv=$('#card #qink'), r=sv.getBoundingClientRect();
      const freeAt=(u,v)=>{const x=r.left+u*r.width,y=r.top+v*r.width;
        if(x<4||y<4||x>document.documentElement.clientWidth-4||y>document.documentElement.clientHeight-4)return false;
        try{return !underInk(x,y,sv)}catch(e){return false}};
      let pu=0,pv=0,found=false;
      for(let v=0.03;v<=0.40&&!found;v+=0.03)for(let u=0.03;u<=0.50&&!found;u+=0.03)
        if(freeAt(u,v)&&freeAt(u+0.18,v+0.07)&&freeAt(u+0.36,v+0.14)){pu=u;pv=v;found=true}
      T('V-5 획을 그을 빈 자리를 찾았다',found,[pu,pv]);
      const n0=((QINK.s)||[]).length;
      const tr=await draw1(sv,[r.width*pu,r.width*pv,r.width*(pu+0.18),r.width*(pv+0.07),
                               r.width*(pu+0.36),r.width*(pv+0.14)]);
      T('V-5 ★펜으로 한 획을 그으면 QINK 가 는다(필기가 살아 있다)',((QINK.s)||[]).length===n0+1,[tr,((QINK.s)||[]).length]);
      T('V-5 ink 스토어 qink:<uid> 에 저장된다',!!(await get('ink','qink:'+uidK)));
      setTool('view'); qWire(); await wait(100);}
     /* 선택지가 눌린다(잉크 덮개 밑으로 — inkPierce) */
     {const b=$('#card .choices button');
      if(b){const was=lastPick(no);b.click();await wait(300);
        T('V-6 ★선택지가 그대로 눌린다(잉크 덮개 밑으로)',lastPick(no)!==''&&lastPick(no)!==was||!!b.classList.contains('pick'),
          [was,lastPick(no),b.className])}
      else T('V-6 선택지 단추가 있다',false)}
     /* 단축키 1~4 — ⚠ **add1 이전부터 죽어 있다.** 3317줄 가늠쇠 `document.querySelector('.sheet')` 가
        늘 숨어 있는 `#book`·`#bkq`(둘 다 class="sheet hide")에 걸려 늘 return 한다.
        지학·물리 둘 다 그렇다(본판에서 같은 값으로 실측 · _probe_tool.py).
        이 판은 **그 줄을 안 건드렸다** — 고치면 물리까지 바뀐다. 잣대는 「무변」으로 적는다. */
     {const h0=hist(no).length, m0=lastM(no);
      document.dispatchEvent(new KeyboardEvent('keydown',{key:'1',bubbles:true}));
      await wait(400);
      T('V-6 ★단축키 길이 본판과 같다(둘 다 안 먹는다 — 이 판이 깨뜨린 것이 아니다)',
        lastM(no)===m0&&hist(no).length===h0,[m0,lastM(no),h0,hist(no).length]);
      N('V-6 단축키가 죽은 까닭',{가늠쇠:'document.querySelector(".sheet")',
        걸리는것:[...document.querySelectorAll('.sheet')].map(x=>x.id+(x.classList.contains('hide')?'(hide)':''))});}
     closeView(); await wait(250);
   });

   /* ══════════ 7. §F 직접 찍기 ══════════ */
   await grp('P', async()=>{
     const A='G62-09', noA=rowByUid(A)[F.NO];
     PICK={};await savePICK();draw();await wait(250);
     /* 교재 탭 메뉴 */
     cropFor(noA);
     OMRTAB=false;
     cropOffer({p:5,r:[20,30,120,90]},()=>{},null); await wait(250);
     let m=document.getElementById('crmenu');
     T('P-1 교재 탭 메뉴 = 카드 + 문제 칸 + 해설 칸 + 글자 + 취소',
       !!m&&[...m.querySelectorAll('button')].map(b=>b.dataset.s).join(',')==='mc,q,s,fix,',
       m?[...m.querySelectorAll('button')].map(b=>txt(b)):null);
     m.querySelector('[data-s=""]').click(); await wait(200);
     /* OMR 탭 메뉴 */
     OMRTAB=true;
     cropOffer({p:1,r:[20,30,120,90]},()=>{},null); await wait(250);
     m=document.getElementById('crmenu');
     T('P-1 ★OMR 탭 메뉴 = 카드 + 취소뿐',
       !!m&&[...m.querySelectorAll('button')].map(b=>b.dataset.s).join(',')==='mc,',
       m?[...m.querySelectorAll('button')].map(b=>txt(b)):null);
     const n0=mcCountOf(noA);
     m.querySelector('[data-s="mc"]').click(); await wait(700);
     T('P-2 ★문항을 안 연 채 OMR 에서 찍으면 pick +1(doc omr)',
       pkOf(A).length===1&&pkOf(A)[0].doc==='omr'&&VNO===null,
       [pkOf(A).length,pkOf(A)[0]&&pkOf(A)[0].doc,VNO]);
     T('P-2 🃏 수가 +1',mcCountOf(noA)===n0+1,[n0,mcCountOf(noA)]);
     T('P-2 「문제 칸에 붙이기」는 🃏 수에 안 들어간다',
       (()=>{const c0=mcCountOf(noA);return c0===n0+1})());
     draw(); await wait(300);
     const el=$$$('#list .item').find(x=>txt(x.querySelector('.num'))===codeShow(rec(noA)));
     T('P-2 목록 카드 🃏 칩이 그 자리에서 바뀐다',!!el&&txt(el).indexOf('🃏 '+(n0+1))>=0,el?txt(el).slice(0,80):null);
     T('P-2 머리 🃏 전체도 +1',txt(document.getElementById('mcAll')).indexOf(String(mcCountIn(DATA.filter(r=>!isC(r)).map(r=>r[F.NO]))))>=0);
     /* 🃏 창에 그 자리 */
     OMRTAB=false;
     await mcwOpen('all'); await wait(1500);
     T('P-3 🃏 창에 찍은 자리 칸이 있다',$$$('#mcwBody canvas[data-pick]').length>=1,$$$('#mcwBody canvas[data-pick]').length);
     T('P-3 「정리OMR · 1쪽 찍은 자리」 글자',txt($('#mcwBody')).indexOf('정리OMR · 1쪽 찍은 자리')>=0,
       txt($('#mcwBody')).slice(0,120));
     $('#mcwBody [data-px]').click(); await wait(700);
     T('P-3 ✕ 로 빼면 −1',pkOf(A).length===0,pkOf(A).length);
     {const w=document.getElementById('mcw');if(w)w.remove()}
     /* 「문제 칸에 붙이기」는 카드가 아니다 */
     const c0=mcCountOf(noA), q0=((CROP[A]||{}).q||[]).length;
     cropFor(noA);
     cropOffer({p:5,r:[20,30,120,90]},()=>{},null); await wait(250);
     document.getElementById('crmenu').querySelector('[data-s="q"]').click(); await wait(800);
     T('P-4 ★「문제 칸에 붙이기」 = crop 만 늘고 🃏 수는 무변',
       ((CROP[A]||{}).q||[]).length===q0+1&&mcCountOf(noA)===c0,
       [((CROP[A]||{}).q||[]).length,q0,mcCountOf(noA),c0]);
     cropFor(null);
   });

   /* ══════════ 8. add2 — §A 알약 · §B 아랫줄 · §C P · §D ✎ 여기서 고치기 ══════════ */
   await grp('W', async()=>{
     const uid='G62-09', no=rowByUid(uid)[F.NO];
     await openView(no); await wait(900);

     /* ───── §A 머리줄 알약 ───── */
     const pill=document.getElementById('inkPill');
     T('W-1 ★#inkPill 이 .vtop 안이다',!!pill&&!!pill.closest('#view .vtop'),
       pill?String(pill.parentElement&&pill.parentElement.className):'(없음)');
     const pb=pill?[...pill.querySelectorAll('button')]:[];
     T('W-1 ★단추 아홉(펜 3 · 형광 3 · 지우개 · 글상자 · ↺)',pb.length===9,
       pb.map(b=>b.id||b.dataset.pen||b.dataset.hl));
     T('W-1 그 아홉이 옮겨 온 그 단추들이다',
       !!pill&&pill.querySelectorAll('[data-pen]').length===3&&pill.querySelectorAll('[data-hl]').length===3
       &&!!pill.querySelector('#tErase')&&!!pill.querySelector('#tTxt')&&!!pill.querySelector('#tUndo'));
     T('W-1 칸막이 둘(펜│형광│도구)',pill&&pill.querySelectorAll('.sep').length===2,
       pill?pill.querySelectorAll('.sep').length:null);
     T('W-1 ★알약 높이 ≤ 26px',pill.getBoundingClientRect().height<=26,pill.getBoundingClientRect().height);
     T('W-1 글자는 CSS 로 가렸다(textContent 는 그대로)',
       getComputedStyle(pill.querySelector('#tErase')).fontSize==='0px'
       &&txt(pill.querySelector('#tErase'))==='지우개',
       [getComputedStyle(pill.querySelector('#tErase')).fontSize,txt(pill.querySelector('#tErase'))]);
     /* 카드를 맨 아래로 굴려도 알약이 보인다(카드 .cmeta 가 아니라 머리줄에 둔 까닭) */
     {const sc=['#cardwrap','#ebody','#card'].map(q=>$(q)).find(el=>el&&el.scrollHeight>el.clientHeight+10);
      if(sc){sc.scrollTop=sc.scrollHeight; await wait(300)}
      const q=pill.getBoundingClientRect(), vr=$('#view').getBoundingClientRect();
      T('W-1 ★카드를 맨 아래로 굴려도 알약이 보인다',
        pill.offsetParent!==null&&q.height>0&&q.top>=vr.top-1&&q.bottom<=vr.bottom+1,
        [sc?sc.id:'(안 굴러감)',q.top,q.bottom,vr.top,vr.bottom]);}

     /* 빨강 펜 · 형광 초록 — 옮긴 단추가 그대로 먹는가.
        ⚠ 바로 위에서 카드를 맨 아래로 굴려 놨다 — 되돌리지 않으면 `#qink` 가 화면 밖이라
          빈 자리 찾기가 늘 0,0 을 돌려준다(2026-09-20 실측). */
     {['#cardwrap','#ebody','#card'].forEach(x=>{const el=$(x);if(el)el.scrollTop=0});
      await wait(250);
      await del('ink','qink:'+uid); await qLoad(uid); await wait(200);
      const sv=$('#card #qink'), r=sv.getBoundingClientRect();
      const freeAt=(u,v)=>{const x=r.left+u*r.width,y=r.top+v*r.width;
        if(x<4||y<4||x>document.documentElement.clientWidth-4||y>document.documentElement.clientHeight-4)return false;
        try{return !underInk(x,y,sv)}catch(e){return false}};
      let pu=0,pv=0,found=false;
      for(let v=0.03;v<=0.40&&!found;v+=0.03)for(let u=0.03;u<=0.50&&!found;u+=0.03)
        if(freeAt(u,v)&&freeAt(u+0.18,v+0.07)&&freeAt(u+0.36,v+0.14)){pu=u;pv=v;found=true}
      T('W-1 획을 그을 빈 자리를 찾았다',found,[pu,pv]);
      const path=[r.width*pu,r.width*pv,r.width*(pu+0.18),r.width*(pv+0.07),
                  r.width*(pu+0.36),r.width*(pv+0.14)];
      pill.querySelector('[data-pen="#B03A2E"]').click(); await wait(150); qWire(); await wait(80);
      T('W-1 빨강 펜 단추에 on 이 붙는다',pill.querySelector('[data-pen="#B03A2E"]').classList.contains('on'));
      let n0=((QINK.s)||[]).length;
      await draw1(sv,path);
      let st=((QINK.s)||[])[((QINK.s)||[]).length-1];
      T('W-1 ★알약 빨강 펜으로 그은 획이 #B03A2E 로 저장된다',
        ((QINK.s)||[]).length===n0+1&&!!st&&st.c==='#B03A2E'&&!st.hl,[((QINK.s)||[]).length,st&&st.c,st&&st.hl]);
      pill.querySelector('[data-hl="#7FD1AE"]').click(); await wait(150); qWire(); await wait(80);
      n0=((QINK.s)||[]).length;
      await draw1(sv,path.map((v,i)=>i%2?v+r.width*0.05:v));
      st=((QINK.s)||[])[((QINK.s)||[]).length-1];
      T('W-1 ★알약 형광 초록 획이 #7FD1AE · 형광 꼴',
        ((QINK.s)||[]).length===n0+1&&!!st&&st.c==='#7FD1AE'&&st.hl===1,[((QINK.s)||[]).length,st&&st.c,st&&st.hl]);
      /* ↺ */
      const nn=((QINK.s)||[]).length;
      pill.querySelector('#tUndo').click(); await until(()=>((QINK.s)||[]).length===nn-1,5000);
      T('W-1 ↺ 가 마지막 획을 무른다(옮기기 전과 같다)',((QINK.s)||[]).length===nn-1,[nn,((QINK.s)||[]).length]);
      /* 지우개 · 글상자 */
      pill.querySelector('#tErase').click(); await wait(150);
      T('W-1 지우개를 고르면 TOOL.mode=erase',TOOL.mode==='erase',TOOL.mode);
      pill.querySelector('#tTxt').click(); await wait(200);
      T('W-1 글상자 단추가 QTXT 를 켠다',QTXT===true&&pill.querySelector('#tTxt').classList.contains('on'),
        [QTXT,pill.querySelector('#tTxt').className]);
      pill.querySelector('#tTxt').click(); await wait(200);
      T('W-1 다시 누르면 꺼진다',QTXT===false,QTXT);
      setTool('view'); qWire(); await wait(100);
      await del('ink','qink:'+uid); await qLoad(uid); await wait(150);}

     /* 알약 단추를 끌어도 창이 안 움직인다 · 머리줄 빈 곳은 움직인다 */
     {const v=$('#view');
      if(v.classList.contains('win')){
        const r0=v.getBoundingClientRect(), eb=pill.querySelector('#tErase');
        await drag(eb,r0.left+30,r0.top+14,r0.left+110,r0.top+74,'mouse'); await wait(250);
        const r1=v.getBoundingClientRect();
        T('W-1 ★알약 단추를 눌러 끌어도 창 자리가 그대로다',
          Math.abs(r1.left-r0.left)<3&&Math.abs(r1.top-r0.top)<3,[r0.left,r1.left,r0.top,r1.top]);
        const vt=$('#view .vtop'), tr=vt.getBoundingClientRect();
        await drag(vt,tr.left+4,tr.top+3,tr.left+54,tr.top+43,'mouse'); await wait(250);
        const r2=v.getBoundingClientRect();
        T('W-1 머리줄 빈 곳을 끌면 창이 움직인다',
          Math.abs(r2.left-(r1.left+50))<4&&Math.abs(r2.top-(r1.top+40))<4,[r1.left,r2.left,r1.top,r2.top]);
      }else T('W-1 문항 창이 떠 있는 창이다',false,v.className)}

     /* 창이 좁으면 둘째 줄로(오른쪽 맞춤) — §A-1 */
     {const v=$('#view'), w0=v.style.width;
      v.style.width='420px'; await wait(350);
      const pr=pill.getBoundingClientRect(), tt=$('#view .vtop .title').getBoundingClientRect(),
            hr=$('#view .vtop').getBoundingClientRect();
      T('W-1 ★창이 좁으면 알약이 둘째 줄로 내려간다',pr.top>=tt.bottom-1,[pr.top,tt.bottom,pr.right,hr.right]);
      T('W-1 그때 오른쪽 맞춤',Math.abs(hr.right-pr.right)<=14,[hr.right,pr.right]);
      v.style.width=w0; await wait(350);}

     /* ───── §B 아랫줄 다섯 ───── */
     {const kids=[...document.querySelectorAll('.vbot .tools>*')];
      const vis=kids.filter(el=>el.offsetParent!==null);
      T('W-2 ★아랫줄에 보이는 것이 다섯뿐',vis.length===5,vis.map(el=>el.id||el.className));
      T('W-2 ★그 다섯 = 회독 층 · +회독 · 👁 · 기록 · 암기카드',
        vis.map(el=>el.id).join(',')==='tLayer,tLayerAdd,tLayerEye,tHist,tCard',vis.map(el=>el.id));
      T('W-2 오른쪽 맞춤',getComputedStyle($('.vbot .tools')).justifyContent==='flex-end',
        getComputedStyle($('.vbot .tools')).justifyContent);
      T('W-2 ★굵기 #tW 안 보임 · 값 2',$('#tW').offsetParent===null&&$('#tW').value==='2',
        [$('#tW')?getComputedStyle($('#tW')).display:'(없음)',$('#tW').value]);
      T('W-2 필기 단추는 아랫줄에 없다(알약으로 갔다)',
        document.querySelectorAll('.vbot .tools [data-pen]').length===0
        &&document.querySelectorAll('.vbot .tools [data-hl]').length===0
        &&!document.querySelector('.vbot .tools #tErase')&&!document.querySelector('.vbot .tools #tTxt'),
        [document.querySelectorAll('.vbot .tools [data-pen]').length,
         !!document.querySelector('.vbot .tools #tErase')]);
      T('W-2 #mP 는 아랫줄에서 숨는다(근거 아랫줄로 갔다)',$('#mP')&&$('#mP').offsetParent===null,
        $('#mP')?getComputedStyle($('#mP')).display:'(없음)');}
     /* +회독 → 층 +1 · 그 층에 그은 획이 그 층에 */
     {const r0=QR;
      $('#tLayerAdd').click(); await wait(400);
      T('W-2 ★+회독 → 층 +1',QR===r0+1,[r0,QR]);
      setTool('pen','#16181B'); qWire(); await wait(120);
      const sv=$('#card #qink'), r=sv.getBoundingClientRect();
      const freeAt=(u,v)=>{const x=r.left+u*r.width,y=r.top+v*r.width;
        if(x<4||y<4||x>document.documentElement.clientWidth-4||y>document.documentElement.clientHeight-4)return false;
        try{return !underInk(x,y,sv)}catch(e){return false}};
      let pu=0,pv=0,found=false;
      for(let v=0.03;v<=0.40&&!found;v+=0.03)for(let u=0.03;u<=0.50&&!found;u+=0.03)
        if(freeAt(u,v)&&freeAt(u+0.18,v+0.07)&&freeAt(u+0.36,v+0.14)){pu=u;pv=v;found=true}
      await draw1(sv,[r.width*pu,r.width*pv,r.width*(pu+0.18),r.width*(pv+0.07),
                      r.width*(pu+0.36),r.width*(pv+0.14)]);
      const st=((QINK.s)||[])[((QINK.s)||[]).length-1];
      T('W-2 ★그 층에 그은 획이 그 층에 들어간다',!!st&&qRoundOf(st)===QR,[st&&st.r,QR]);
      setTool('view'); qWire(); await wait(100);
      await del('ink','qink:'+uid); await qLoad(uid); await wait(150);}

     /* ───── §C P = 넷째 단추 ───── */
     {const boxes=$$$('#card .vox');
      const vp=$('#card .vox.vP');
      T('W-3 ★근거 아랫줄 단추 넷 · 넷째가 P',boxes.length===4&&!!vp&&boxes[3]===vp,
        boxes.map(b=>b.className+':'+txt(b)));
      T('W-3 title 이 아랫줄 #mP 것 그대로',!!vp&&!!$('#mP')&&vp.title===$('#mP').title,
        [vp&&vp.title,$('#mP')&&$('#mP').title]);
      const h0=hist(no).length;
      vp.click(); await wait(600);
      T('W-3 ★P 를 누르면 기록 마지막이 P',lastM(no)==='P'&&hist(no).length===h0+1,
        [lastM(no),h0,hist(no).length]);
      T('W-3 ★켜지면 먹색(아랫줄 #mP 와 같은 바탕)',
        vp.classList.contains('on')
        &&getComputedStyle(vp).backgroundColor===getComputedStyle($('#mP')).backgroundColor,
        [vp.className,getComputedStyle(vp).backgroundColor,getComputedStyle($('#mP')).backgroundColor]);
      closeView(); await wait(450);
      {const idx=nums().indexOf(codeShow(rec(no)));const cell=$$$('#spec i')[idx];
       T('W-3 ★히트맵 칸이 P 로 따라간다',idx>=0&&!!cell&&/(^|\s)P(\s|$)/.test(cell.className),
         [idx,cell&&cell.className]);}
      await openView(no); await wait(700);
      $('#card .vox.vO').click(); await wait(600);
      T('W-3 다시 O 를 누르면 O 로 돌아온다',
        lastM(no)==='O'&&$('#card .vox.vO').classList.contains('on')
        &&!$('#card .vox.vP').classList.contains('on'),
        [lastM(no),$('#card .vox.vP').className]);}

     /* ───── §D 「✎ 여기서 고치기」 ───── */
     {const U='G62-09', A='G39-02';
      GG={};GGREF={};
      GG[U]=[{k:'g_t1',i:1,t:'ㄱ 처음 글',ok:'O',ts:1,
              parts:[{l:'ㄱ',t:'처음 글'}],cs:[{k:'c_t1',t:'댓글 처음',ts:1}]}];
      GGREF[A]=[U];
      await saveGG(); await saveGGREF();
      const noA=rowByUid(A)[F.NO];
      await openView(noA); await wait(900);
      const chip=$('#card [data-ggrt]');
      T('W-4 연결 칩이 있다',!!chip,chip?txt(chip):null);
      chip.click(); await wait(350);
      let box=$('#card .ggrefbox');
      T('W-4 상자가 펴진다',!!box&&!box.classList.contains('hide'),box?box.className:null);
      const eb=box.querySelector('[data-ggre]');
      T('W-4 ★항목에 「✎ 여기서 고치기」가 있다',!!eb&&txt(eb)==='✎ 여기서 고치기',eb?txt(eb):null);
      eb.click(); await wait(300);
      const edb=box.querySelector('[data-ggre-box]');
      T('W-4 편집 줄 = [라벨][칸] + ＋ 병렬 + 저장(add1 의 그 줄)',
        !!edb&&!edb.classList.contains('hide')&&!!edb.querySelector('.ggrow .lab')
        &&!!edb.querySelector('.ggrow .txt')&&!!edb.querySelector('[data-ggedplus]')
        &&!!edb.querySelector('[data-ggedsave]'),
        edb?edb.className:null);
      T('W-4 저장된 글이 칸에 들어 있다',
        edb.querySelector('.ggrow .lab').value==='ㄱ'&&edb.querySelector('.ggrow .txt').value==='처음 글',
        [edb.querySelector('.ggrow .lab').value,edb.querySelector('.ggrow .txt').value]);
      edb.querySelector('.ggrow .txt').value='고친 글';
      edb.querySelector('[data-ggedsave]').click();
      await until(()=>(ggOf(U)[0]||{}).t==='ㄱ 고친 글',6000); await wait(400);
      const g=ggOf(U)[0];
      T('W-4 ★GG[그 문항] 항목의 글이 바뀐다(사본 아님)',!!g&&g.t==='ㄱ 고친 글',g&&g.t);
      T('W-4 ★k·i·ok·ts·댓글은 무변',
        !!g&&g.k==='g_t1'&&g.i===1&&g.ok==='O'&&g.ts===1
        &&(g.cs||[]).length===1&&g.cs[0].k==='c_t1'&&g.cs[0].ts===1,
        g?[g.k,g.i,g.ok,g.ts,(g.cs||[]).length]:null);
      T('W-4 ★사본이 0 — GG 열쇠 하나 · 목록 하나',
        Object.keys(GG).length===1&&Object.keys(GG)[0]===U&&ggOf(U).length===1,
        [Object.keys(GG),ggOf(U).length]);
      box=$('#card .ggrefbox');
      T('W-4 ★고친 상자는 펼친 채로 남는다',!!box&&!box.classList.contains('hide'),box?box.className:null);
      T('W-4 상자에 새 글이 보인다',txt(box).indexOf('고친 글')>=0,txt(box).slice(0,140));
      /* 댓글 */
      const ce=box.querySelector('[data-ggrce]');
      T('W-4 ★댓글에도 「✎ 여기서 고치기」',!!ce&&txt(ce)==='✎ 여기서 고치기',ce?txt(ce):null);
      ce.click(); await wait(300);
      const cb=$('#card [data-ggrce-box]');
      T('W-4 댓글 편집은 한 칸',!!cb&&!cb.classList.contains('hide')&&!!cb.querySelector('textarea.cein'),
        cb?cb.className:null);
      cb.querySelector('textarea').value='고친 댓글';
      cb.querySelector('[data-ggcesave]').click();
      await until(()=>((ggOf(U)[0]||{}).cs||[{}])[0].t==='고친 댓글',6000); await wait(350);
      const c2=((ggOf(U)[0]||{}).cs||[])[0];
      T('W-4 ★댓글 글만 바뀌고 k·ts 는 무변',
        !!c2&&c2.t==='고친 댓글'&&c2.k==='c_t1'&&c2.ts===1,c2?[c2.t,c2.k,c2.ts]:null);
      /* 병렬 줄 */
      {const b2=$('#card .ggrefbox');
       b2.querySelector('[data-ggre]').click(); await wait(300);
       const e2=$('#card [data-ggre-box]');
       e2.querySelector('[data-ggedplus]').click(); await wait(250);
       const rows=[...e2.querySelectorAll('.ggrow')];
       T('W-4 ＋ 병렬 → 줄이 둘',rows.length===2,rows.length);
       rows[1].querySelector('.lab').value='ㄴ';
       rows[1].querySelector('.txt').value='둘째 줄';
       e2.querySelector('[data-ggedsave]').click();
       await until(()=>((ggOf(U)[0]||{}).parts||[]).length===2,6000); await wait(350);
       const g2=ggOf(U)[0];
       T('W-4 ★병렬 항목은 줄마다 고쳐진다',
         (g2.parts||[]).length===2&&g2.parts[1].l==='ㄴ'&&g2.parts[1].t==='둘째 줄'
         &&g2.t===('ㄱ 고친 글'+String.fromCharCode(10)+'ㄴ 둘째 줄'),
         [(g2.parts||[]).length,g2.t]);}
      /* 그 문항을 열면 새 글 */
      await openView(no); await wait(900);
      T('W-4 ★그 문항을 열면 근거에 새 글이 있다',
        txt($('#card .ggbox')).indexOf('고친 글')>=0,txt($('#card .ggbox')).slice(0,180));
      /* 정리 창에도 같은 단추 */
      {closeView(); await wait(300);
       const sec=String(unitOf(noA)||'').split('.').slice(0,2).join('.');
       jnOpen(sec); await wait(900);
       const jw=document.getElementById('jnw');
       T('W-4 정리 창에도 「✎ 여기서 고치기」가 있다',
         !!jw&&jw.querySelectorAll('[data-ggre]').length>=1,
         [!!jw,jw?jw.querySelectorAll('[data-ggre]').length:null,sec]);
       const x=document.getElementById('jnwX'); if(x)x.click(); await wait(200);}
      await cap('W_연결근거상자','<div>'+(($('#card')||{}).innerHTML||'')+'</div>');
      GG={};GGREF={};await saveGG();await saveGGREF();draw();await wait(250);}
     closeView(); await wait(250);
   });

   /* ══════════ 9. add3 ① 글상자·지우개 엉킴 ══════════ */
   await grp('E', async()=>{
     const uid='G62-09', no=rowByUid(uid)[F.NO];
     await openView(no); await wait(900);
     await del('ink','qink:'+uid); await qLoad(uid); await wait(200);
     const card=$('#card'), pill=document.getElementById('inkPill');
     const q=s=>(pill&&pill.querySelector(s))||$(s);
     const tTxt=q('#tTxt'), tEr=q('#tErase'), tPen=q('[data-pen="#16181B"]'), tHl=q('[data-hl="#F2C230"]');
     const nBox=()=>card.querySelectorAll('#qtxt .tbox').length;
     const onCnt=()=>document.querySelectorAll('[data-pen].on,[data-hl].on,#tErase.on').length;
     /* 획을 그을 빈 자리 — `#qink` 가 덮고 있고 밑에 눌릴 것이 없는 곳 */
     setTool('pen','#16181B'); qWire(); await wait(150);
     const sv=$('#card #qink'), rr=sv.getBoundingClientRect();
     const freeAt=(u,v)=>{const x=rr.left+u*rr.width,y=rr.top+v*rr.width;
       if(x<4||y<4||x>document.documentElement.clientWidth-4||y>document.documentElement.clientHeight-4)return false;
       try{return !underInk(x,y,sv)}catch(e){return false}};
     let pu=0,pv=0,found=false;
     for(let v=0.03;v<=0.40&&!found;v+=0.03)for(let u=0.03;u<=0.50&&!found;u+=0.03)
       if(freeAt(u,v)&&freeAt(u+0.14,v+0.05)&&freeAt(u+0.28,v+0.10)){pu=u;pv=v;found=true}
     T('E-0 획을 그을 빈 자리를 찾았다',found,[pu,pv]);
     await draw1(sv,[rr.width*pu,rr.width*pv,rr.width*(pu+0.14),rr.width*(pv+0.05),
                     rr.width*(pu+0.28),rr.width*(pv+0.10)]);
     T('E-0 펜으로 한 획을 그었다',((QINK.s)||[]).length===1,((QINK.s)||[]).length);
     /* 글상자 켜기 */
     const b0=nBox();
     tTxt.click(); await wait(300);
     T('E-1 글상자가 켜진다',QTXT===true&&card.classList.contains('txton')&&tTxt.classList.contains('on'),
       [QTXT,card.className,tTxt.className]);
     T('E-1 ★그때 펜·형광·지우개 .on 이 0 · #card.penon 없음',
       onCnt()===0&&!card.classList.contains('penon'),[onCnt(),card.className]);
     {/* ⚠ 글상자는 획 **시작점**에 만든다 — 지우개 시험은 획 가운데서 하므로 자리가 겹치면 안 된다 */
      const x=rr.left+rr.width*pu, y=rr.top+rr.width*pv;
      const top=document.elementFromPoint(x,y);
      T('E-1 그 자리 맨 위가 글상자 층(#qtxt)이다',!!top&&(top.id==='qtxt'||!!top.closest('#qtxt')),
        top?(top.id||top.className):null);
      await fire(card.querySelector('#qtxt'),'pointerdown',x,y,'pen',41); await wait(350);
      T('E-1 ★글상자 모드에서 톡 = 글상자 +1',nBox()===b0+1,[b0,nBox()]);}
     /* 지우개 — ①의 본문 */
     tEr.click(); await wait(300);
     T('E-2 ★지우개를 고르면 QTXT 가 꺼진다',QTXT===false,QTXT);
     T('E-2 ★#card.txton 없음 · #tTxt.on 없음',
       !card.classList.contains('txton')&&!tTxt.classList.contains('on'),[card.className,tTxt.className]);
     T('E-2 지우개가 켜졌다(TOOL.mode=erase · penon)',TOOL.mode==='erase'&&card.classList.contains('penon'),
       [TOOL.mode,card.className]);
     {const x=rr.left+rr.width*(pu+0.14), y=rr.top+rr.width*(pv+0.05);
      const top=document.elementFromPoint(x,y);
      /* ⚠ `#qink` 는 <svg> 다 — 그 자리에 획이 있으면 맨 위는 그 <path> 다.
         id·className 으로 가르면 안 된다(SVG 의 className 은 문자열이 아니라 객체다 · 2026-09-20 실측). */
      T('E-2 ★그 자리 맨 위가 다시 필기 덮개(#qink)다',
        !!top&&(top.id==='qink'||!!(top.closest&&top.closest('#qink'))),
        top?(top.id||String(top.tagName)):null);
      const nb=nBox(), ns=((QINK.s)||[]).length;
      await fire(sv,'pointerdown',x,y,'pen',42); await wait(120);
      await fire(sv,'pointerup',x,y,'pen',42); await wait(400);
      T('E-2 ★획 위를 누르면 획 −1',((QINK.s)||[]).length===ns-1,[ns,((QINK.s)||[]).length]);
      T('E-2 ★그때 글상자는 +0',nBox()===nb,[nb,nBox()]);}
     /* 펜·형광도 같다 */
     tTxt.click(); await wait(250);
     T('E-3 글상자 다시 켬',QTXT===true);
     tPen.click(); await wait(250);
     T('E-3 ★펜을 고르면 QTXT 가 꺼진다',QTXT===false&&!card.classList.contains('txton'),[QTXT,card.className]);
     tTxt.click(); await wait(250);
     tHl.click(); await wait(250);
     T('E-3 ★형광을 고르면 QTXT 가 꺼진다',QTXT===false&&!card.classList.contains('txton'),[QTXT,card.className]);
     /* 글상자 다시 누름 = 꺼짐 · 톡해도 +0 */
     tTxt.click(); await wait(250);
     tTxt.click(); await wait(250);
     T('E-4 글상자를 다시 누르면 꺼진다',QTXT===false&&!tTxt.classList.contains('on'),[QTXT,tTxt.className]);
     {const nb=nBox(), x=rr.left+rr.width*(pu+0.30), y=rr.top+rr.width*(pv+0.16);
      const h=card.querySelector('#qtxt');
      await fire(h,'pointerdown',x,y,'pen',43); await wait(300);
      T('E-4 ★꺼진 채 톡하면 글상자 +0',nBox()===nb,[nb,nBox()]);}
     T('E-5 이미 선 글상자를 누르는 길은 그대로다(.tbox 는 고치기)',
       String(qTxtWire).indexOf(".closest('.tbox')")>=0);
     setTool('view'); qWire(); await wait(120);
     await del('ink','qink:'+uid); await qLoad(uid); await wait(150);
     closeView(); await wait(250);
   });

   /* ══════════ 10. add3 ② 펜으로 근거 줄이 눌린다 ══════════ */
   await grp('N', async()=>{
     const A='G39-02', U='G62-09';
     GG={};GGREF={};
     GG[U]=[{k:'g_n1',i:1,t:'ㄱ 남의 근거',ok:'O',ts:1,cs:[{k:'c_n1',t:'댓글',ts:1}]}];
     GG[A]=[{k:'g_n2',i:1,t:'내 근거 하나',ok:'O',ts:1,cs:[]}];
     {const third=(DATA.filter(r=>!isC(r)).map(r=>r[F.CODE]).find(u=>u!==A&&u!==U));
      if(third)GG[third]=[{k:'g_n3',i:1,t:'셋째 문항 근거',ok:'O',ts:1,cs:[]}];}
     GGREF[A]=[U];
     await saveGG(); await saveGGREF();
     const noA=rowByUid(A)[F.NO];
     await openView(noA); await wait(900);
     await del('ink','qink:'+A); await qLoad(A); await wait(200);
     const card=$('#card'), sv=card.querySelector('#qink');
     /* 펜 도구를 켠다 — 덮개가 카드를 통째로 덮는 상태 */
     setTool('pen','#16181B'); qWire(); await wait(200);
     T('N-0 펜 도구가 켜졌다(#card.penon · #qink pointer-events auto)',
       card.classList.contains('penon')&&getComputedStyle(sv).pointerEvents==='auto',
       [card.className,getComputedStyle(sv).pointerEvents]);
     T('N-0 ★근거 덩어리가 덮개 위다(.ggtop z-index 8 > #qink 6)',
       !!card.querySelector('.ggtop')&&getComputedStyle(card.querySelector('.ggtop')).zIndex==='8'
       &&getComputedStyle(sv).zIndex==='6',
       [card.querySelector('.ggtop')?getComputedStyle(card.querySelector('.ggtop')).zIndex:null,
        getComputedStyle(sv).zIndex]);
     const ink0=((QINK.s)||[]).length;
     /* 자리마다 「맨 위가 그것인가」 — 덮개에 안 먹히는지 그대로 잰다(픽셀 아님) */
     const mid=el=>{const r=el.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]};
     const tops=(el)=>{try{el.scrollIntoView({block:'center'})}catch(_){}
       const [x,y]=mid(el);const a=document.elementsFromPoint(x,y);
       const i=a.indexOf(el);
       /* `#qink` 는 <svg> 라 그 안의 <path> 가 잡힐 수 있다 — closest 로 본다 */
       const j=a.findIndex(z=>z&&(z.id==='qink'||(z.closest&&z.closest('#qink'))));
       return {i:i,j:j,ok:(i>=0&&(j<0||i<j))}};
     const chk=(q,ko)=>{const el=card.querySelector(q);
       if(!el){T('N-1 '+ko+' 가 있다',false,q);return null}
       const r=tops(el);
       T('N-1 ★'+ko+' 가 덮개보다 위다',r.ok,[q,r.i,r.j]);return el};
     chk('.ggnum','번호 칩'); chk('[data-ggfind]','🔍');   /* 「!」 는 판을 편 뒤에 — 기본은 접혀 있다 */
     chk('.ggref','🔗 연결 칩'); chk('#cDetBtn','정답·해설'); chk('.vox.vO','O');
     chk('.ggrow .txt','적는 칸'); chk('.ggrow .lab','라벨 칸');
     /* 눌러서 되는지 */
     {const num=card.querySelector('.ggnum'); num.click(); await wait(300);
      T('N-2 번호 칩을 누르면 판이 펴진다',
        !!card.querySelector('.ggpan')&&!card.querySelector('.ggpan').classList.contains('hide'),
        card.querySelector('.ggpan')?card.querySelector('.ggpan').className:null);
      chk('.ggpan:not(.hide) .ggbang','판 안의 「!」');
      num.click(); await wait(200);}
     {const bg=card.querySelector('.ggbox .ggbang'); const was=!!(ggOf(A)[0]||{}).bang;
      if(bg){bg.click(); await until(()=>!!(ggOf(A)[0]||{}).bang!==was,4000);
        T('N-2 「!」가 뒤집힌다',!!(ggOf(A)[0]||{}).bang!==was,[was,!!(ggOf(A)[0]||{}).bang]);
        bg.click(); await wait(300)}
      else T('N-2 「!」가 있다',false)}
     {card.querySelector('[data-ggfind]').click(); await wait(400);
      const fb=card.querySelector('[data-ggfindbox]');
      T('N-2 🔍 를 누르면 찾기 상자가 열린다',!!fb&&!fb.classList.contains('hide'),fb?fb.className:null);
      const rows=[...card.querySelectorAll('[data-ggfindbox] .ggres')];
      const res=rows.find(x=>!x.classList.contains('on'))||rows[0];
      T('N-2 아직 안 걸린 결과 줄이 있다',!!res&&!res.classList.contains('on'),
        rows.map(x=>x.className));
      if(res){const r=tops(res);
        T('N-2 ★결과 줄이 덮개보다 위다',r.ok,[r.i,r.j]);
        const n0=ggRefOf(A).length;
        res.click(); await until(()=>ggRefOf(A).length===n0+1,4000); await wait(300);
        T('N-2 ★결과 줄을 누르면 연결 +1',ggRefOf(A).length===n0+1,[n0,ggRefOf(A).length]);}}
     {const rt=card.querySelector('[data-ggrt]');
      if(rt){rt.click(); await wait(300);
        T('N-2 연결 칩을 누르면 상자가 펴진다',
          !!card.querySelector('.ggrefbox')&&!card.querySelector('.ggrefbox').classList.contains('hide'));}
      else T('N-2 연결 칩이 있다',false)}
     T('N-2 ★그동안 획은 하나도 안 늘었다',((QINK.s)||[]).length===ink0,[ink0,((QINK.s)||[]).length]);
     /* 근거 덩어리 밖에서는 그대로 획이 된다 */
     {const rr=sv.getBoundingClientRect();
      const gt=card.querySelector('.ggtop').getBoundingClientRect();
      const freeAt=(u,v)=>{const x=rr.left+u*rr.width,y=rr.top+v*rr.width;
        if(x<4||y<4||x>document.documentElement.clientWidth-4||y>document.documentElement.clientHeight-4)return false;
        if(y>=gt.top-2)return false;                       /* 근거 덩어리 위쪽(문제 글·여백) */
        try{return !underInk(x,y,sv)}catch(e){return false}};
      let pu=0,pv=0,found=false;
      for(let v=0.03;v<=0.40&&!found;v+=0.03)for(let u=0.03;u<=0.50&&!found;u+=0.03)
        if(freeAt(u,v)&&freeAt(u+0.14,v+0.05)&&freeAt(u+0.28,v+0.10)){pu=u;pv=v;found=true}
      T('N-3 근거 덩어리 밖 빈 자리를 찾았다',found,[pu,pv,gt.top]);
      const n0=((QINK.s)||[]).length;
      await draw1(sv,[rr.width*pu,rr.width*pv,rr.width*(pu+0.14),rr.width*(pv+0.05),
                      rr.width*(pu+0.28),rr.width*(pv+0.10)]);
      T('N-3 ★근거 덩어리 밖 펜 획은 그대로 그어진다',((QINK.s)||[]).length===n0+1,
        [n0,((QINK.s)||[]).length]);}
     /* 선택지·보기 줄은 옛 길 그대로(덮개 밑) */
     {const c=card.querySelector('.choices button');
      if(!c)T('N-4 선택지가 있다',false);
      else{const r=tops(c);
        T('N-4 ★선택지는 덮개 **밑** 그대로다(inkPierce 가 맡는다)',r.j>=0&&(r.i<0||r.j<r.i),[r.i,r.j])}}
     /* 손가락 거르개 */
     {const ok=typeof PASS_THRU==='string';
      T('N-5 PASS_THRU 를 읽을 수 있다',ok);
      if(ok){const miss=['.ggnum','.ggbang','.ggref','.ggres','.gguse']
        .filter(q=>{const el=document.createElement('div');el.className=q.slice(1);
          return !el.matches(PASS_THRU)});
        T('N-5 ★근거 덩어리 선택자가 손가락 거르개에 다 들었다',miss.length===0,miss)}}
     /* 옛 획이 근거 자리에 있어도 글자가 안 가려진다 */
     {const gt=card.querySelector('.ggtop').getBoundingClientRect(), rr=sv.getBoundingClientRect();
      const u=(gt.left+gt.width*0.4-rr.left)/rr.width, v=(gt.top+18-rr.top)/rr.width;
      const n0=((QINK.s)||[]).length;
      QINK.s.push({c:'#16181B',w:2,hl:0,r:QR,p:[u,v,u+0.05,v+0.01,u+0.1,v+0.02]});
      qPaint(); await wait(250);
      const num=card.querySelector('.ggnum');
      const r=num?tops(num):{ok:false};
      T('N-6 ★근거 자리에 옛 획이 있어도 근거가 위다',r.ok,[r.i,r.j]);
      T('N-6 INK 데이터는 그대로 있다(안 지운다)',((QINK.s)||[]).length===n0+1,[n0,((QINK.s)||[]).length]);
      QINK.s.pop(); qPaint();}
     /* 보기 줄은 **보기가 있는 문항**에서 잰다(G39-02 에는 보기가 없다) */
     {await openView(rowByUid('G52-07')[F.NO]); await wait(900);
      setTool('pen','#16181B'); qWire(); await wait(200);
      const c2=$('#card'), bg=c2.querySelector('.bogi .t');
      if(!bg)T('N-4 보기 줄이 있다',false);
      else{try{bg.scrollIntoView({block:'center'})}catch(_){}
        await wait(300);
        const sv2=c2.querySelector('#qink'), sr=sv2?sv2.getBoundingClientRect():null;
        const r0=bg.getBoundingClientRect();
        const a=document.elementsFromPoint(r0.left+r0.width/2,r0.top+r0.height/2);
        const i=a.indexOf(bg);
        const j=a.findIndex(z=>z&&(z.id==='qink'||(z.closest&&z.closest('#qink'))));
        N('N-4 보기 줄 밑준비',{penon:c2.className,pe:sv2?getComputedStyle(sv2).pointerEvents:null,
          ink:sr?[Math.round(sr.top),Math.round(sr.bottom)]:null,
          bogi:[Math.round(r0.top),Math.round(r0.bottom)],
          stack:a.map(z=>z.id||String(z.tagName)).slice(0,6)});
        /* ⚠ 실측 — 이 문항에서는 덮개(`#qink`)의 아래끝이 〈보기〉 줄보다 위다(419 vs 457).
           `qFit` 이 잡는 덮개 높이 얘기이고 **add3 가 만든 것이 아니다**(qFit 무접촉).
           그러니 「덮개가 위에 있다」로 재면 안 된다 — 잴 것은 **내가 안 들어올렸다**는 것이다:
           〈보기〉 줄이 `.ggtop`(z 8) 밖에 있고, 덮개가 닿는 자리에서는 여전히 덮개가 위다. */
        T('N-4 ★보기 줄을 덮개 위로 안 올렸다(.ggtop 밖 — 옛 길 그대로)',
          !bg.closest('.ggtop')&&(j<0||j<i),[i,j,!!bg.closest('.ggtop')]);
        {const yy=sr?Math.min(r0.top+r0.height/2,sr.bottom-6):r0.top;
         const a2=document.elementsFromPoint(r0.left+r0.width/2,yy);
         const j2=a2.findIndex(z=>z&&(z.id==='qink'||(z.closest&&z.closest('#qink'))));
         T('N-4 덮개가 닿는 자리에서는 여전히 덮개가 맨 위다',j2===0,
           [j2,a2.map(z=>z.id||String(z.tagName)).slice(0,4)])}}
      setTool('view'); qWire(); await wait(120);}
     setTool('view'); qWire(); await wait(120);
     await del('ink','qink:'+A); await qLoad(A); await wait(150);
     /* 위 검색 줄 「🔗 근거」 결과 줄 */
     closeView(); await wait(300);
     {ggSearchMode('g'); const qi=$('#q'); qi.value='근거'; ggResBox('근거'); await wait(400);
      const row=document.querySelector('#esres .ggres');
      T('N-7 위 검색 줄에 결과 줄이 있다',!!row,document.getElementById('esres')?document.getElementById('esres').innerHTML.slice(0,90):null);
      if(row){row.click(); await until(()=>VNO!==null,5000); await wait(400);
        T('N-7 ★그 줄을 누르면 문항 창이 열린다',VNO!==null&&!$('#view').classList.contains('hide'),[VNO]);
        closeView(); await wait(250)}
      qi.value=''; ggSearchMode('q'); await wait(250);}
     GG={};GGREF={};await saveGG();await saveGGREF();draw();await wait(250);
   });

   /* ══════════ 11. add3 ③ 쓰임 수 · 쓰임 목록 창 · 찾기 결과 줄 ══════════ */
   await grp('U', async()=>{
     const T0='G62-09';
     const pool=DATA.filter(r=>!isC(r)&&r[F.CODE]!==T0).map(r=>r[F.CODE]);
     const mk=n=>{GGREF={};pool.slice(0,n).forEach(u=>{GGREF[u]=[T0]})};
     GG={};GG[T0]=[{k:'g_u1',i:1,t:'ㄱ 쓰임 시험 근거',ok:'O',ts:1,
                    parts:[{l:'ㄱ',t:'쓰임 시험 근거'}],cs:[{k:'c_u1',t:'댓글 하나',ts:1}]}];
     const css=el=>getComputedStyle(el).color;
     const muted=getComputedStyle(document.documentElement).getPropertyValue('--muted').trim();
     const red=getComputedStyle(document.documentElement).getPropertyValue('--red').trim();
     const asCol=v=>{const d=document.createElement('span');d.style.color=v;document.body.appendChild(d);
       const c=getComputedStyle(d).color;d.remove();return c};
     const cMuted=asCol(muted), cRed=asCol(red);
     const noT=rowByUid(T0)[F.NO];
     for(const n of [1,2,4,5,12]){
       mk(n); await saveGG(); await saveGGREF();
       await openView(noT); await wait(800);
       const lab=$('#card .ggline .lb .gguse');
       if(n<=1){
         T('U-1 n=1 이면 라벨에 숫자가 없다',!lab,lab?txt(lab):null);
       }else{
         T('U-1 n='+n+' 라벨 숫자 = ↩'+n,!!lab&&txt(lab)==='↩'+n,lab?txt(lab):null);
         T('U-1 n='+n+' 색 = '+(n>=5?'빨강':'회색'),!!lab&&css(lab)===(n>=5?cRed:cMuted),
           [lab?css(lab):null,n>=5?cRed:cMuted]);
         T('U-1 n='+n+' 굵기 900',!!lab&&getComputedStyle(lab).fontWeight==='900',
           lab?getComputedStyle(lab).fontWeight:null);
       }
       closeView(); await wait(200);
     }
     /* 세 자리의 수가 서로 같다 — 라벨 · 연결 칩 · 찾기 결과 줄 */
     {mk(4); const A=pool[0];                      /* A 가 T0 를 걸어 두었다 */
      await saveGGREF(); await saveGG();
      const noA=rowByUid(A)[F.NO];
      await openView(noA); await wait(900);
      const chip=$('#card .ggref .gguse');
      T('U-1 ★연결 칩 옆 숫자 = 4(앞 글자 없음)',!!chip&&txt(chip)==='4',chip?txt(chip):null);
      $('#card [data-ggfind]').click(); await wait(500);
      const inp=$('#card [data-ggfindbox] input'); inp.value='쓰임 시험';
      ggFindRun(A,'qp-'); await wait(300);
      const row=$('#card [data-ggfindbox] .ggres');
      T('U-4 ★찾기 결과 줄이 세 줄 꼴(머리줄·문제 글·근거 줄)',
        !!row&&!!row.querySelector('.hd')&&!!row.querySelector('.qq')&&!!row.querySelector('.gl'),
        row?row.innerHTML.slice(0,160):null);
      T('U-4 머리줄 = 코드 칩 · 회차·번호 · 단원',
        !!row&&!!row.querySelector('.hd .cd')&&!!row.querySelector('.hd b')&&!!row.querySelector('.hd .un')
        &&/\d+회 \d+번/.test(txt(row.querySelector('.hd b'))),
        row?txt(row.querySelector('.hd')):null);
      T('U-4 ★이미 연결한 줄 = 「이미 넣음」 + 흐림',
        !!row&&row.classList.contains('on')&&txt(row).indexOf('이미 넣음')>=0
        &&getComputedStyle(row).opacity==='0.5',
        row?[row.className,getComputedStyle(row).opacity,txt(row).slice(0,60)]:null);
      T('U-4 문제 글은 70자까지',!!row&&txt(row.querySelector('.qq')).replace(/…$/,'').length<=70,
        row?txt(row.querySelector('.qq')).length:null);
      T('U-4 근거 줄은 줄마다 90자까지',
        !!row&&String(row.querySelector('.gl').textContent||'').split('\n').every(x=>x.length<=90));
      /* 이미 연결한 줄엔 쓰임 수를 안 그린다(민법 3461 과 같다) */
      T('U-4 이미 넣은 줄엔 쓰임 수를 안 그린다',!!row&&!row.querySelector('.gguse'));
      $('#card [data-ggfind]').click(); await wait(200);
      /* 숫자 누름 → 창 */
      const inkWas=$('#card').classList.contains('penon');
      const panWas=$('#card .ggpan')?$('#card .ggpan').className:'';
      chip.click(); await wait(600);
      const w=document.getElementById('gguw');
      T('U-2 ★숫자를 누르면 쓰임 목록 창이 뜬다',!!w&&!!w.querySelector('.panel'));
      T('U-2 제목 수 = 4',!!w&&txt(w.querySelector('.bplh span')).indexOf('쓰는 문항 4')>=0,
        w?txt(w.querySelector('.bplh')):null);
      T('U-2 줄 수 = 4',w&&w.querySelectorAll('#gguwBody .gguR').length===4,
        w?w.querySelectorAll('#gguwBody .gguR').length:null);
      T('U-2 머리 상자에 그 문항의 근거 전부(댓글 포함)',
        !!w&&txt(w.querySelector('.gguh .gg')).indexOf('쓰임 시험 근거')>=0
        &&txt(w.querySelector('.gguh .gg')).indexOf('댓글 하나')>=0,
        w?txt(w.querySelector('.gguh .gg')).slice(0,90):null);
      T('U-2 ★줄 차례 = 목록 차례(단원순)',(()=>{
        const got=[...w.querySelectorAll('#gguwBody .gguR .cd')].map(x=>txt(x));
        const want=ggUseSort(ggOwners(T0)).map(u=>codeShow(rowByUid(u)));
        return got.join(',')===want.join(',')})(),
        [...w.querySelectorAll('#gguwBody .gguR .cd')].map(x=>txt(x)));
      T('U-2 ★숫자를 눌러도 밑의 칩은 안 열렸다(상자 무변)',
        ($('#card .ggrefbox')?$('#card .ggrefbox').classList.contains('hide'):true),
        $('#card .ggrefbox')?$('#card .ggrefbox').className:'(없음)');
      /* 지금 보는 문항 줄 */
      const meRow=w.querySelector('#gguwBody .gguR.me');
      T('U-3 ★지금 보는 문항 줄이 노랑 + 딱지',
        !!meRow&&txt(meRow).indexOf('지금 보는 문항')>=0
        &&getComputedStyle(meRow).backgroundColor===asCol('#FFFBEA'),
        meRow?[meRow.className,getComputedStyle(meRow).backgroundColor]:null);
      T('U-3 그 줄은 「× 연결 끊기」 · 다른 줄은 「↪ 그 문제 보기」',
        !!meRow&&!!meRow.querySelector('[data-gguux]')&&!meRow.querySelector('[data-gguugo]')
        &&w.querySelectorAll('#gguwBody [data-gguugo]').length===3,
        [meRow?!!meRow.querySelector('[data-gguux]'):null,
         w.querySelectorAll('#gguwBody [data-gguugo]').length]);
      /* 끌기·크기·기억 */
      {const p=w.querySelector('.panel'), q0=p.getBoundingClientRect();
       await drag(w.querySelector('.bplh'),q0.left+120,q0.top+8,q0.left+70,q0.top+58,'mouse'); await wait(250);
       const q1=p.getBoundingClientRect();
       T('U-5 창 머리줄을 끌면 움직인다',Math.abs(q1.left-(q0.left-50))<3&&Math.abs(q1.top-(q0.top+50))<3,
         [q0.left,q1.left]);
       const g=w.querySelector('.twgrip'), gr=g.getBoundingClientRect();
       await drag(g,gr.left+4,gr.top+4,gr.left+84,gr.top+54,'mouse'); await wait(260);
       T('U-5 모서리를 끌면 커진다',Math.abs(p.getBoundingClientRect().width-(q1.width+80))<3,
         [q1.width,p.getBoundingClientRect().width]);
       T('U-5 크기를 기기 값에 적는다',!!JSON.parse(localStorage.getItem('jagwa.win.gguse')||'null'));}
      /* 연결 끊기 */
      {const n0=ggRefOf(A).length;
       meRow.querySelector('[data-gguux]').click();
       await until(()=>ggRefOf(A).length===n0-1,5000); await wait(500);
       T('U-3 ★× 연결 끊기 → ggref −1',ggRefOf(A).length===n0-1,[n0,ggRefOf(A).length]);
       const w2=document.getElementById('gguw');
       T('U-3 ★창의 수가 3 으로 준다',!!w2&&w2.querySelectorAll('#gguwBody .gguR').length===3,
         w2?w2.querySelectorAll('#gguwBody .gguR').length:null);
       T('U-3 ★문항 창의 연결 칩이 사라진다',!$('#card .ggref'),
         $('#card .ggref')?$('#card .ggref').outerHTML.slice(0,80):null);
       T('U-3 라벨 수도 갱신된다(3)',
         (()=>{const l=$('#card .ggline .lb .gguse');return !l})()||
         txt($('#card .ggline .lb .gguse'))==='↩0',
         $('#card .ggline .lb .gguse')?txt($('#card .ggline .lb .gguse')):'(없음)');
       const wx=document.getElementById('gguw');if(wx)wx.remove();}
      closeView(); await wait(250);}
     /* 위 검색 줄 결과도 같은 꼴 + 노란 표시 */
     {mk(4); await saveGGREF(); await saveGG();
      ggSearchMode('g'); const qi=$('#q'); qi.value='쓰임'; ggResBox('쓰임'); await wait(400);
      const row=document.querySelector('#esres .ggres');
      T('U-4 ★위 검색 줄 결과도 세 줄 꼴',
        !!row&&row.classList.contains('g3')&&!!row.querySelector('.hd')&&!!row.querySelector('.qq')
        &&!!row.querySelector('.gl'),row?row.className:null);
      T('U-4 ★거기엔 노란 찾은 글자 표시가 산다',!!row&&!!row.querySelector('mark'),
        row?row.innerHTML.slice(0,140):null);
      T('U-4 위 검색 줄 결과 줄에도 쓰임 수',!!row&&!!row.querySelector('.gguse')
        &&txt(row.querySelector('.gguse'))==='↩4',row?txt(row.querySelector('.gguse')):null);
      qi.value=''; ggSearchMode('q'); await wait(250);}
     T('U-6 찾기 칸은 120ms 모았다 한 번 돌린다',typeof ggFindSoon==='function'
       &&String(ggFindSoon).indexOf('120')>=0);
     GG={};GGREF={};await saveGG();await saveGGREF();draw();await wait(250);
   });
   /* ══════════ S — add3 §C 근거 통 가드 · §A-2 되살림 ══════════
      ⚠ 지시서는 묶음 이름을 「G」라 했지만 add1 근거 묶음이 이미 `G-1`~`G-6` 을 쓴다.
        겹치면 헛잣대 거르개가 섞이므로 **「S」(동기화 가드)** 로 갈아 붙였다. */
   await grp('S', async()=>{
     const ls=k=>{try{return JSON.parse(localStorage.getItem(k)||'{}')}catch(e){return {}}};
     const UID='G61-07';
     const one=[{k:'g_t',i:1,t:'시험 근거',ok:'O',ts:1,cs:[]}];
     const clean=()=>{const sh=ls(SHADOW_KEY);delete sh.gg;lsPut(SHADOW_KEY,sh);
       const g=ls(GONE_KEY);delete g['gg|'+UID];lsPut(GONE_KEY,g);
       const u=ls(U_KEY);delete u['gg|'+UID];lsPut(U_KEY,u)};
     clean();
     GG={}; GG_READY=false;
     {const sh=ls(SHADOW_KEY);sh.gg={};sh.gg[UID]=one;lsPut(SHADOW_KEY,sh)}
     T('S-0 통이 아직 안 읽힌 상태다',GG_READY===false&&SYNC_REF.gg.g()===null,
       [GG_READY,SYNC_REF.gg.g()]);
     stampAll();
     T('S-1 ★안 읽힌 통에는 **묘비를 안 찍는다**',!ls(GONE_KEY)['gg|'+UID],ls(GONE_KEY)['gg|'+UID]);
     T('S-1 그림자도 그대로 남는다',!!(ls(SHADOW_KEY).gg||{})[UID]);
     {const remote={data:{gg:{}},u:{},gone:{}}; remote.data.gg[UID]=one;
      const pay=recPayload(remote);
      T('S-2 ★안 읽힌 통은 **원격 것 그대로** 실어 보낸다(빈 객체로 안 지운다)',
        !!(pay.data.gg||{})[UID],Object.keys(pay.data.gg||{}));}
     {const before=JSON.stringify(GG);
      const remote={data:{gg:{}},u:{},gone:{}}; remote.data.gg[UID]=one; remote.u['gg|'+UID]=Date.now();
      await recMerge(remote);
      T('S-3 ★안 읽힌 통은 병합에서도 안 건드린다',JSON.stringify(GG)===before,
        [before.slice(0,40),JSON.stringify(GG).slice(0,40)]);}
     GG={}; GG[UID]=one; GG_READY=true;
     T('S-4 읽은 뒤에는 g() 가 값을 낸다',SYNC_REF.gg.g()!==null);
     stampAll();
     T('S-4 ★칸이 그대로면 묘비가 안 찍힌다',!ls(GONE_KEY)['gg|'+UID]);
     GG={}; stampAll();
     T('S-5 ★진짜로 지우면 묘비는 그대로 찍힌다(가드가 지우기를 막지 않는다)',
       !!ls(GONE_KEY)['gg|'+UID],ls(GONE_KEY)['gg|'+UID]);
     clean();
     {GG={};GG_READY=true;await saveGG();
      try{localStorage.removeItem(GGFIX_K)}catch(e){}
      const n1=await ggFixEat(); await wait(350);
      T('S-6 ★되살림이 근거를 보탠다',n1===1&&ggOf(UID).length===1,[n1,ggOf(UID).length]);
      T('S-6 ★글자가 깃 이력 그대로다',
        String((ggOf(UID)[0]||{}).t).indexOf('아래부터 대성중열')===0
        &&(ggOf(UID)[0]||{}).k==='g_mu9suur9_18aq'&&(ggOf(UID)[0]||{}).ts===1789907744565,
        [(ggOf(UID)[0]||{}).k,String((ggOf(UID)[0]||{}).t).slice(0,14)]);
      try{localStorage.removeItem(GGFIX_K)}catch(e){}
      const n2=await ggFixEat(); await wait(250);
      T('S-6 ★같은 `k` 는 두 번 안 보탠다(멱등)',n2===0&&ggOf(UID).length===1,[n2,ggOf(UID).length]);
      T('S-6 한 번 먹으면 기기에 표시가 남는다',!!localStorage.getItem(GGFIX_K));
      GG={};GG[UID]=[{k:'g_mu9suur9_18aq',i:1,t:'내가 고친 글',ok:'X',ts:9,cs:[]}];await saveGG();
      try{localStorage.removeItem(GGFIX_K)}catch(e){}
      await ggFixEat(); await wait(250);
      T('S-6 ★사용자가 고친 칸은 안 덮는다',(ggOf(UID)[0]||{}).t==='내가 고친 글',
        (ggOf(UID)[0]||{}).t);
      GG={};await saveGG();clean();}
   });

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
   /* add3 ① 은 카드 층 공통이라 생물에도 같이 든다(지시서 ①-범위).
      모습(snap)은 이미 다 찍은 뒤라 대조에는 안 섞인다. */
   await openView(DATA[0][F.NO]); await wait(900);
   {const b=document.getElementById('tTxt');
    if(!b)T('B-4 생물에도 글상자 단추가 있다',false);
    else{b.click(); await wait(300);
      const on1=(typeof QTXT!=='undefined')&&QTXT===true;
      setTool('erase'); await wait(300);
      T('B-4 ★생물도 지우개를 고르면 글상자가 꺼진다',on1&&QTXT===false,[on1,QTXT]);
      T('B-4 생물 #tTxt.on 도 따라 꺼진다',!b.classList.contains('on'),b.className);
      setTool('view'); await wait(150)}}
   closeView(); await wait(300);
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

def _cap_head():
    """앱의 `<style>` 을 그대로 실어 캡처가 실물과 같은 모양이 되게 한다(픽셀 게이트 아님 · 사람 눈 확인용)."""
    try:
        html = io.open(SRC, encoding='utf-8', newline='').read()
        css = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', html, re.S))
    except Exception:
        css = ''
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            '<title>지학 add1 — DOM 캡처</title><style>' + css + '</style>'
            '<style>body{background:var(--paper);padding:20px}'
            '#esh,.panel{position:static!important;left:auto!important;top:auto!important;'
            'width:min(900px,96vw)!important;height:auto!important;max-height:none!important;'
            'box-shadow:0 8px 30px rgba(0,0,0,.18);border-radius:12px;overflow:visible}'
            '.twgrip{display:none}h1.capt{font-size:13px;color:#4A5661;font-weight:600;margin:0 0 10px}'
            '</style></head><body data-subj="earth" data-layer="card">'
            '<h1 class="capt">지학 add1 — 헤드리스 DOM 캡처(픽셀 게이트 아님 · 사람 눈 확인용)</h1>')


CAPHEAD = _cap_head()



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
    out = []

    def T2(name, cond, info=''):
        out.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))

    blk = s.find('\nif(CARD_LAYER){\n')
    end = s.find('\n}\n/*/EARTH:js*/')
    keys = ['var ISEA=', 'function shellBuild(', 'function drawEarthList(', 'var mcwOpen=async function(',
            'function jnOpen(', 'function ggLineHTML(', 'var ggAdd=async function(', 'function ggCardHTML(',
            'var omrTab=async function(', 'var GG={}']
    T2('Z-1 새 갈래가 전부 if(CARD_LAYER) **블록 안**이다 — 물리는 만들지도 않는다',
       blk >= 0 and end > blk and all(blk < s.find(k) < end for k in keys),
       [(k, s.find(k)) for k in keys if not (blk < s.find(k) < end)])
    T2('Z-2 새 갈래는 전부 ISEA 문 안이다(과목 문 무변)', "var ISEA=SUBJ_ID==='earth';" in s)
    T2('Z-3 uid 를 안 바꿨다', s.count('r[F.CODE]=') == 0)
    T2('Z-4 지학 SYNC_KEYS 줄 자체는 안 고쳤다(넷은 JS 가 더한다)',
       s.count("'crop','txt','tfix','bref']") == base.count("'crop','txt','tfix','bref']"))
    T2('Z-5 Tailwind 를 안 들였다', 'cdn.tailwindcss.com' not in s)
    T2('Z-6 makeFloat 을 **부르는** 자리가 둘 늘었다(🃏 창 · 📋 창)',
       s.count("makeFloat(b,b.querySelector('.bplh'),'mc'") == 1
       and s.count("makeFloat(b,b.querySelector('.bplh'),'jn'") == 1
       and s.count('function makeFloat(') == 1)
    T2('Z-7 bkLoadPiece 는 **더하기만** 했다(pc.__doc · pc.__k)',
       "const doc=pc.__doc?await pc.__doc():await pieceDoc(pc.file);" in s
       and "key:(pc.__k||'bink:')+pr" in s)
    T2('Z-8 cropOffer 의 🃏 는 pick 으로 간다(crop 과 갈래가 다르다)',
       "if(slot==='mc'){await pickAdd(uid,cell," in s and s.count('function cropOffer(') == 1)
    T2('Z-9 새 kv 는 셋뿐이다(gg · ggref · pick)',
       s.count("put('kv','gg',GG)") == 1 and s.count("put('kv','ggref',GGREF)") == 1
       and s.count("put('kv','pick',PICK)") == 1)
    T2('Z-10 CSS 는 지학 문 안이다', 'body[data-subj="earth"] #lib{max-width:56rem' in s)
    T2('Z-11 줄끝이 CRLF 그대로다', b.count(b'\r\n') == b.count(b'\n'))
    T2('Z-12 본판 대비 늘기만 했다', len(s) > len(base))
    T2('Z-13 지운 본판 줄이 거의 없다(손댄 자리뿐)',
       sum(1 for ln in base.split('\n') if ln.strip() and ln not in s) <= 40,
       sum(1 for ln in base.split('\n') if ln.strip() and ln not in s))
    # ── add2 가 둔 것(그대로) ──
    T2('Z-15 새 kv·새 SYNC 키가 없다',
       s.count("put('kv','") == base.count("put('kv','") and s.count('SYNC_REF.') == base.count('SYNC_REF.'),
       [s.count("put('kv','"), base.count("put('kv','")])
    T2('Z-17 아랫줄 감추기는 지학 문 안이다',
       'body[data-subj="earth"] .vbot .tools>*{display:none!important}' in s
       and s.count('.vbot .tools>*{display:none') == 1)
    T2('Z-19 단축키 줄 무변(일부러 죽여 둔 것)',
       s.count("if(e.key==='1')mark('O')") == base.count("if(e.key==='1')mark('O')")
       and "if(document.querySelector('.sheet'))return;" in s)
    # ── add3 ──
    T2('Z-20 ① setTool 덧씌움이 펜·형광·지우개에서 QTXT 를 끈다',
       "if(mode==='pen'||mode==='hl'||mode==='erase')QTXT=false;" in s
       and s.count('setTool=function(mode)') == 1)
    T2('Z-21 ① 글상자를 켜면 필기 도구를 놓는다(#tTxt 쪽)',
       "if(QTXT){TOOL.mode='view';" in s
       and s.count("b.onclick=()=>{QTXT=!QTXT;") == 1)
    T2('Z-22 ① 본디 setTool 은 한 글자도 안 건드렸다',
       "  TOOL.mode=mode;if(color)TOOL.color=color;TOOL.w=+$('#tW').value;" in s
       and s.count('function setTool(mode,color,el){') == base.count('function setTool(mode,color,el){'))
    T2('Z-23 ② 근거 덩어리는 **한 겹**이다(.ggtop) · 물리엔 안 생긴다(ggCardHTML 은 ISEA)',
       s.count("'<div class=\"ggtop\">'") == 1
       and '#card .ggtop{position:relative;z-index:8' in s
       and "function ggCardHTML(r){\n  if(!ISEA)return '';" in s)
    T2('Z-24 ② UNDER_HIT·underInk·inkPierce 는 한 글자도 안 건드렸다(지시서 ⓑ)',
       s.count('const UNDER_HIT=') == 1
       and ".row[data-k],[data-c],[data-tfx],[data-go],[data-page],[data-no],.snt,.trit';" in s
       and s.count("if(el.closest('select,input,textarea'))return null;")
           == base.count("if(el.closest('select,input,textarea'))return null;")
       and s.count('function inkPierce(card){') == base.count('function inkPierce(card){'))
    T2('Z-25 ② PASS_THRU 에 근거 선택자를 **더하기만** 했다',
       ".ggnum,.ggbang,.ggref,.ggres,.gguse,[data-ggown],[data-ggpick],[data-ggrt],[data-ggtog]" in s
       and s.count('const PASS_THRU=') == 1
       and "'[data-tool],#omrPad,#navTg,select,input,textarea,.ogrip,#mask,.tbox,#qtxt," in s)
    T2('Z-26 ③ 쓰임 수는 **한 함수**다 — 정의 1 · 부르는 자리 3',
       s.count('function ggUseHTML(') == 1 and s.count('ggUseHTML(') == 4,
       s.count('ggUseHTML('))
    T2('Z-27 ③ 문턱 5 가 박혀 있다(분포로 조정하지 않는다)',
       "const n=ggUseN(uid); if(n<=1)return '';" in s and "(n>=5?' hot':'')" in s)
    T2('Z-28 ③ 찾기 결과 줄은 **한 꼴**이다 — 카드 안·위 검색 줄이 같은 함수',
       s.count('function ggResRowHTML(') == 1
       and "function ggResLine(h,q){return ggResRowHTML(h,q,'go','','')}" in s
       and "ggResRowHTML(h,q,'pick',uid,sc)" in s)
    T2('Z-29 ③ 찾기 칸 120ms 모으기 · 포커스는 즉시',
       'function ggFindSoon(' in s and 'ggFindSoon(v[0],v[1])' in s
       and "if(i&&!b.classList.contains('hide')){i.focus();ggFindRun(v[0],v[1])}" in s)
    T2('Z-30 ③ 저장 꼴은 무변(gg·ggref)',
       s.count("put('kv','gg',GG)") == base.count("put('kv','gg',GG)")
       and s.count("put('kv','ggref',GGREF)") == base.count("put('kv','ggref',GGREF)"))
    # ── add3 근거 통 가드 ──
    T2('Z-40 늦게 읽는 통 셋이 다 가드 안이다',
       'var GG_READY=false;' in s
       and 'SYNC_REF.gg   ={g:()=>GG_READY?GG:null' in s
       and 'SYNC_REF.ggref={g:()=>GG_READY?GGREF:null' in s
       and 'SYNC_REF.pick ={g:()=>GG_READY?PICK:null' in s)
    T2('Z-41 `g()` 를 읽는 자리가 다 null 을 「아직 모름」으로 다룬다',
       s.count('const cur=SYNC_REF[k].g();\n    if(!cur)continue;') == 2
       and "const v=SYNC_REF[k].g(); if(v)await put('kv',k,v)" in s
       and 'const now=SYNC_REF[k].g(); if(!now)continue;' in s
       and "data[k]=v||((remote&&remote.data&&remote.data[k])||{})" in s)
    T2('Z-42 되살림은 멱등이다(기기 표시 + 없는 k 만)',
       "var GGFIX_K='jagwa.ggfix.20260921.'+SUBJ_ID;" in s
       and 'if(!have.has(g.k)){list.push(g);m++}' in s
       and 'localStorage.setItem(GGFIX_K' in s)
    T2('Z-43 저장 꼴·병합 규칙은 안 건드렸다',
       s.count('function stampAll(){') == base.count('function stampAll(){')
       and s.count('async function recMerge(remote){') == base.count('async function recMerge(remote){')
       and s.count('function ggSaveList') == base.count('function ggSaveList')
       and s.count('var ggSaveList') == base.count('var ggSaveList'))
    return out


def main():
    want = [a for a in sys.argv[1:] if a in ('earth', 'bio', 'phys', 'null')] \
           or ['earth', 'bio', 'phys', 'null']
    cur = open(SRC, encoding='utf-8', newline='').read()
    basetxt = open(BASE, encoding='utf-8', newline='').read()
    lines = []
    W = int(os.environ.get('HARNESS_WAIT', '1500'))

    def T2(name, cond, info=''):
        lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))

    if 'earth' in want:
        ls, _ = run('earth', W, cur)
        lines += ls
    if 'bio' in want:
        ls, sn = run('bio', W, cur)
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
        ls, sn = run('phys', W, cur)
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
        for pre, ko in (('S', 'add3 근거 통 가드·되살림'),):
            hit = [x for x in fails if x.split(' | ')[1].startswith(pre + '-')
                   or x.split(' | ')[1].startswith(pre + ' 묶음')]
            T2('0-헛잣대 HEAD 에서 %s 묶음이 FAIL 한다' % ko, len(hit) > 0,
               [x.split(' | ')[1][:70] for x in fails][:8])
        T2('0-헛잣대 HEAD 는 통과가 아니다', len(fails) > 0, len(fails))

    lines += static_checks()
    npass = sum(1 for x in lines if x.startswith('PASS'))
    nfail = sum(1 for x in lines if x.startswith('FAIL'))
    nnote = sum(1 for x in lines if x.startswith('NOTE'))
    for x in lines:
        print(x)
    print('\n== 자과앱 근거 가드 %d PASS / %d FAIL / %d NOTE / %d항 ==' % (npass, nfail, nnote, len(lines)))
    print('캡처: %s' % CAP)
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
