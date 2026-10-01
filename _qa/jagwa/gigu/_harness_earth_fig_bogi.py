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
BASE_MD5 = 'e6c34eb7baa100345c66a1e83d389c68'   # 고침 전 md5(LF)
BASE = os.path.join(HERE, '_base_fig.html')   # 공개 저장소에 두지 않는다(D11)


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
    for rev in ('cd248a5', 'a9f9fd4~1', '57ebb08', 'HEAD~1'):   # ★ A-6(d) 9/30 — 고침 전 = cd248a5(fig_bogi 인도 d8a7d2e 바로 앞 · md5(LF) e6c34eb7 · git show 셈) — 'HEAD~1' 은 인도 때만 맞았다
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
CAP = os.environ.get('LISTPOP_CAP') or os.path.join(HERE, '_cap_fig')
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
  if(/\/img\//.test(path))window.__imgReq=(window.__imgReq||0)+1;   /* §A — 그림 요청을 센다 */
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
   try{_coll=null}catch(e){}
   FL.past='y';FL.q='';FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';
   TFIX={};await saveTFIX();
   draw(); await wait(300);
   /* ★ A-6(a) 9/30 둘째 바퀴 — jagwa_uid(genie 5e18424 + studyplandata 4a011475 · 결정로그 9/29 15:09 · _task_jagwa_uid.md 234줄 「옛 번호를 박은 하네스 셋을 새 번호로」 —
      이 하네스는 그때 바탕 사본을 못 찾아 못 돌아 빠졌다): 기록 열쇠 = 새 uid(renderCard uid=r[F.CODE] · ✕→tfixSet · O·△·X→BG) — 옛 G52-07 로 TFIX·BG·figHid·tfixAny 를 읽으면
      비고, 바탕 앱(cd248a5 · rowByUid = F.CODE 만)은 옛 번호로 행을 못 찾아 헛잣대 run 이 밑준비에서 통째로 터진다 · ⚠ run() 의 지학 기록 박기(b90a4d52)와 짝 */
   const UF='G15-52-07';                    /* 그림 + 보기 ㄱ~ㄹ (옛 uid G52-07 · 화면 코드 = 새 uid) */
   const NOF=rowByUid(UF)[F.NO];
   N('밑준비',{subj:SUBJ_ID,DATA:DATA.length,UF:UF,코드:codeShow(rowByUid(UF)),
              보기:(rowByUid(UF)[F.BOGI]||[]).map(b=>b.키)});

   /* ══════════ 1. §A 원본 그림 가리기 ══════════ */
   await grp('A', async()=>{
     window.__imgReq=0;
     await openView(NOF); await wait(900);
     T('A-0 그림 칸이 있다',!!$('#card #cFig'));
     T('A-0 ✕ 가 그림 칸 오른쪽 위에 있다',!!$('#card #cFig .cx')&&txt($('#card #cFig .cx'))==='✕');
     {const f=$('#card #cFig').getBoundingClientRect(), x=$('#card #cFig .cx').getBoundingClientRect();
      T('A-0 ✕ 가 오른쪽 위다',x.right<=f.right+1&&x.top<=f.top+10,[f.right,x.right,f.top,x.top])}
     T('A-0 조각을 안 붙여도 ✕ 가 보인다',!((CROP[UF]||{}).q||[]).length&&$('#card #cFig .cx').offsetParent!==null);
     T('A-0 지금은 안 가려졌다',figHid(UF)===false);
     const req0=window.__imgReq;
     $('#card #cFig .cx').click(); await wait(700);
     T('A-1 ★가리면 #cFig 가 없다',!$('#card #cFig'),!!$('#card #cFig'));
     T('A-1 TFIX[uid].fig === "0"',(TFIX[UF]||{}).fig==='0',TFIX[UF]);
     T('A-1 그 자리에 「🖼 원본 그림 보이기」 칩',!!$('#card #cFigShow')
       &&txt($('#card #cFigShow'))==='🖼 원본 그림 보이기',txt($('#card #cFigShow')));
     window.__imgReq=0;
     await openView(NOF); await wait(900);
     T('A-2 ★가린 채로 다시 열어도 그림을 안 받는다',window.__imgReq===0,window.__imgReq);
     T('A-2 가림이 이어진다',figHid(UF)===true&&!$('#card #cFig')&&!!$('#card #cFigShow'));
     /* 저장소 왕복(새로고침·동기화 흉내) */
     {const kept=JSON.parse(JSON.stringify(TFIX));TFIX={};TFIX=(await get('kv','tfix'))||{};
      T('A-2 kv tfix 에 남는다(새로고침 뒤 유지)',(TFIX[UF]||{}).fig==='0',TFIX[UF]);
      T('A-2 동기화가 싣는 꼴 그대로다(SYNC_REF.tfix)',JSON.stringify(SYNC_REF.tfix.g())===JSON.stringify(kept))}
     T('A-3 ★fig 는 「고친 글자 있음」에 안 낀다',tfixAny(UF)===false,[tfixAny(UF),TFIX[UF]]);
     T('A-3 ★fig 는 검색 글에 안 낀다',String(tfixHay(UF)).indexOf('0')<0&&tfixHay(UF)==='',JSON.stringify(tfixHay(UF)));
     T('A-3 TFIX_SLOTS·tfixSlotsOf 에 fig 가 없다',
       TFIX_SLOTS.indexOf('fig')<0&&tfixSlotsOf(UF).indexOf('fig')<0,tfixSlotsOf(UF));
     /* 되돌리기 */
     window.__imgReq=0;
     $('#card #cFigShow').click(); await wait(900);
     T('A-4 ★칩을 누르면 다시 보인다',!!$('#card #cFig')&&!$('#card #cFigShow'));
     T('A-4 칸이 지워진다(TFIX[uid] 자체가 없다)',!TFIX[UF]||(TFIX[UF]||{}).fig===undefined,TFIX[UF]);
     /* ⚠ `imgUrl` 은 IMGURL·pdf 스토어에 캐시한다 — 두 번째엔 網을 안 탄다(그게 맞다).
        그러니 「받았는가」가 아니라 **「다시 그려졌는가」**로 재다. */
     await until(()=>!!$('#card #cFig .figw img'),6000);
     T('A-4 그때는 그림이 다시 그려진다',!!$('#card #cFig .figw img'),
       $('#card #cFig .figw')?$('#card #cFig .figw').innerHTML.slice(0,60):null);
   });

   /* ══════════ 2. 그림 없는 문항 · 다른 과목 ══════════ */
   await grp('F', async()=>{
     const u2='G62-09', n2=rowByUid(u2)[F.NO];
     T('F-0 그 문항엔 그림이 없다',rowByUid(u2)[F.FILE]!=='IMG');
     await openView(n2); await wait(700);
     T('F-1 그림 없는 문항엔 ✕·칩이 0개',!$('#card #cFig')&&!$('#card #cFigShow')&&$$$('#card .fig').length===0);
     await openView(NOF); await wait(800);
   });

   /* ══════════ 3. §B 〈보기〉 줄 글자 고치기 ══════════ */
   await grp('B', async()=>{
     const rows=()=>$$$('#card .bogi .row');
     T('B-0 보기 네 줄이 있다',rows().length===4,rows().length);
     const tOf=k=>rows().find(x=>x.dataset.k===k).querySelector('.t');
     T('B-0 ★.t 에 data-tfx="b<키>" 가 붙었다',
       rows().map(x=>x.querySelector('.t').getAttribute('data-tfx')).join(',')==='bㄱ,bㄴ,bㄷ,bㄹ',
       rows().map(x=>x.querySelector('.t').getAttribute('data-tfx')));
     T('B-0 ㄹ 줄은 OCR 이 깨진 그 줄이다',txt(tOf('ㄹ')).indexOf('에서 기압은')>=0,txt(tOf('ㄹ')));
     T('B-0 아직 ✎ 가 없다',$$$('#card .bogi .tfx').length===0);
     /* 600ms 길게 누르기 */
     const long=async(el,ms)=>{const r=el.getBoundingClientRect();
       el.dispatchEvent(mkPE('pointerdown',r.left+8,r.top+6,'pen',41));
       await wait(ms);
       el.dispatchEvent(mkPE('pointerup',r.left+8,r.top+6,'pen',41));
       await wait(250)};
     await long(tOf('ㄹ'),650);
     const sh=document.getElementById('tfxSheet');
     T('B-1 ★길게 누르면 고치기 시트가 뜬다',!!sh);
     T('B-1 제목이 「✎ 글자 고치기 — 〈보기〉 ㄹ」',!!sh&&txt(sh.querySelector('h2')).indexOf('〈보기〉 ㄹ')>0,
       sh?txt(sh.querySelector('h2')):null);
     T('B-1 원본 글이 옆에 보인다',!!sh&&txt(sh.querySelector('.orig')).indexOf('에서 기압은')>=0,
       sh?txt(sh.querySelector('.orig')).slice(0,40):null);
     {const ta=sh.querySelector('#tfxIn');ta.value='(나)에서 기압은 고도가 높아질수록 낮아진다.';
      sh.querySelector('#tfxOk').click();await wait(700)}
     T('B-2 ★줄 글자가 바뀐다',txt(tOf('ㄹ')).indexOf('(나)에서 기압은')===0,txt(tOf('ㄹ')));
     T('B-2 그 줄에 ✎ 가 붙는다',!!tOf('ㄹ').querySelector('.tfx'));
     T('B-2 TFIX[uid]["bㄹ"] 에 담긴다',(TFIX[UF]||{})['bㄹ']&&(TFIX[UF]||{})['bㄹ'].indexOf('(나)')===0,TFIX[UF]);
     T('B-2 「고친 글자 있음」에 들어간다',tfixAny(UF)===true);
     /* 검색 — 새 글·옛 글 둘 다 */
     const hit=q=>{FL.q=q;const n=DATA.filter(pass).length;FL.q='';return n};
     T('B-3 ★검색에 새 글이 걸린다',hit('고도가 높아질수록 낮아진다')>=1,hit('고도가 높아질수록 낮아진다'));
     T('B-3 ★옛 글도 그대로 걸린다',hit('에서 기압은')>=1,hit('에서 기압은'));
     /* 되돌리기 */
     await long(tOf('ㄹ'),650);
     const sh2=document.getElementById('tfxSheet');
     T('B-4 다시 길게 누르면 그 칸이 채워져 뜬다',!!sh2&&sh2.querySelector('#tfxIn').value.indexOf('(나)')===0,
       sh2?sh2.querySelector('#tfxIn').value.slice(0,20):null);
     sh2.querySelector('#tfxDel').click(); await wait(700);
     T('B-4 ★되돌리기 = 칸 삭제·원본 복귀',
       !((TFIX[UF]||{})['bㄹ'])&&txt(tOf('ㄹ')).indexOf('에서 기압은')>=0&&!tOf('ㄹ').querySelector('.tfx'),
       [(TFIX[UF]||{})['bㄹ'],txt(tOf('ㄹ'))]);
   });

   /* ══════════ 4. O·△·X 와 선택지가 안 다친다 ══════════ */
   await grp('X', async()=>{
     const rows=()=>$$$('#card .bogi .row');
     const row=rows().find(x=>x.dataset.k==='ㄹ');
     const oxB=row.querySelector('.ox button[data-v="O"]');
     T('X-0 그 줄에 O·△·X 가 있다',!!oxB&&row.querySelectorAll('.ox button').length===3);
     const bg0=JSON.stringify(BG[UF]||{});
     /* 길게 누른 **뒤** — O 가 안 눌린 채여야 한다 */
     {const t=row.querySelector('.t'), r=t.getBoundingClientRect();
      t.dispatchEvent(mkPE('pointerdown',r.left+8,r.top+6,'pen',42));
      await wait(650);
      t.dispatchEvent(mkPE('pointerup',r.left+8,r.top+6,'pen',42));
      await wait(300)}
     T('X-1 ★길게 누른 뒤에도 O·△·X 는 안 눌렸다',JSON.stringify(BG[UF]||{})===bg0,[bg0,JSON.stringify(BG[UF]||{})]);
     {const s=document.getElementById('tfxSheet');if(s)s.remove()}
     /* 짧게 O 누름 = 지금처럼 bogi 기록 */
     rows().find(x=>x.dataset.k==='ㄹ').querySelector('.ox button[data-v="O"]').click();
     await wait(600);
     T('X-2 ★짧게 O 를 누르면 bogi 에 기록된다',(BG[UF]||{})['ㄹ']==='O',BG[UF]);
     /* 선택지 — 짧게 누름은 고르기 · 길게 누름은 고치기(무변) */
     {const b=$('#card .choices button');
      if(b){b.click();await wait(400);
        T('X-3 선택지 짧게 누름 = 고르기(무변)',!!$('#card .choices button.pick'),
          [...document.querySelectorAll('#card .choices button')].map(x=>x.className).join('|'))}
      else T('X-3 선택지가 있다',false)}
     {const b=$('#card .choices button'), r=b.getBoundingClientRect();
      b.dispatchEvent(mkPE('pointerdown',r.left+10,r.top+8,'pen',43));
      await wait(650);
      b.dispatchEvent(mkPE('pointerup',r.left+10,r.top+8,'pen',43));
      await wait(300);
      const s=document.getElementById('tfxSheet');
      T('X-3 선택지 길게 누름 = 고치기 시트(무변)',!!s&&txt(s.querySelector('h2')).indexOf('보기 ①')>0,
        s?txt(s.querySelector('h2')):null);
      if(s)s.remove()}
     closeView(); await wait(250);
   });

   /* ══════════ 5. §C 머리줄 칩 크기 ══════════ */
   await grp('C', async()=>{
     const ex=document.getElementById('examChip'), rc=document.getElementById('recChip');
     T('C-0 두 칩이 머리줄 안에 있다',!!ex&&!!rc&&ex.closest('#esh .ehead')!==null&&rc.closest('#esh .ehead')!==null);
     /* 보이게 해서 잰다(D-날은 설정이 없으면 숨어 있다) */
     ex.style.display='';ex.textContent='제64회 변리사 1차 D-153';
     rc.textContent='● 동기화됨 1분 전';
     await wait(150);
     const cs=el=>getComputedStyle(el);
     T('C-1 ★D-날 칩 11px · 800',cs(ex).fontSize==='11px'&&cs(ex).fontWeight==='800',[cs(ex).fontSize,cs(ex).fontWeight]);
     T('C-1 ★D-날 칩 높이 ≤ 22px',ex.getBoundingClientRect().height<=22,ex.getBoundingClientRect().height);
     T('C-2 ★동기화 칩 11px',cs(rc).fontSize==='11px',cs(rc).fontSize);
     T('C-2 ★동기화 칩 테두리 0',parseFloat(cs(rc).borderTopWidth)===0&&cs(rc).borderTopStyle==='none',
       [cs(rc).borderTopWidth,cs(rc).borderTopStyle]);
     T('C-2 동기화 칩 바탕이 없다',cs(rc).backgroundColor==='rgba(0, 0, 0, 0)',cs(rc).backgroundColor);
     T('C-3 오류일 때 빨강은 산다',(()=>{rc.classList.add('err');const c=getComputedStyle(rc).color;
        rc.classList.remove('err');return c!==cs(rc).color})(),null);
     T('C-3 누름(동기화·시험 설정)은 무변',typeof rc.onclick==='function'||!!rc.getAttribute('title'));
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
                if rel == 'earth/기록.json':   # ★ A-6(d) 9/30 둘째 바퀴 — 지학 기록은 인도(d8a7d2e · 9/20 21:36) 바로 앞 기록 커밋 b90a4d52(savedAt 9/20 12:35Z)로 박는다 —
                    #   표본 G52-07 에 사용자가 인도 뒤 남긴 기록(글자 고침 7칸 25a5144b 9/21 00:15 · 〈보기〉 4칸 af848326 9/21 00:21)이 jagwa_uid 옮김(jgMigrate)으로
                    #   표본 새 uid 칸에 들어와 B-0(✎)·A-3(고친 글자 있음) 을 흔든다 · 앞 커밋엔 둘 다 없다(git show 셈)
                    b = subprocess.run(['git', '-C', SPDROOT, 'show', 'b90a4d52:earth/기록.json'], capture_output=True).stdout or b
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
    # ★ A-6(d) 9/30 둘째 바퀴 — Z-1·Z-2·Z-11 은 이 판(fig_bogi 인도 d8a7d2e)의 패치 꼴을 잰다 — 지금 판은 뒤 판(add2·add3 · shell_bio_phys c9faff2 · …)이 바꿨다
    s_fb = subprocess.run(['git', '-C', GENIE, 'show', 'd8a7d2e:jagwa/index.html'], capture_output=True).stdout.replace(b'\r\n', b'\n').decode('utf-8')
    out = []

    def T2(n, c, i=''):
        out.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c else ' | ' + str(i)))

    blk = s_fb.find('\nif(CARD_LAYER){\n')
    end = s_fb.find('\n}\n/*/EARTH:js*/')
    keys = ['var tfixSlotsOf=', 'var figHid=', 'var tfixLabel=', 'var tfixBKey=']
    T2('Z-1 새 갈래가 if(CARD_LAYER) 블록 안이다', blk >= 0 and all(blk < s_fb.find(k) < end for k in keys),
       [(k, s_fb.find(k)) for k in keys if not (blk < s_fb.find(k) < end)])
    T2('Z-2 새 kv·새 SYNC 키를 안 만들었다 — tfix 한 통뿐',
       s_fb.count("SYNC_REF.") == base.count("SYNC_REF.") and "put('kv','tfix',TFIX)" in s_fb
       and s_fb.count("put('kv','") == base.count("put('kv','"))
    T2('Z-3 TFIX_SLOTS 에 fig 를 안 넣었다',
       "TFIX_SLOTS=['q','c1','c2','c3','c4','c5','s'];" in s and "'fig'" not in s.split('var tfixSlotsOf=')[1][:200])
    T2('Z-4 tfixAny·tfixHay 가 tfixSlotsOf 를 쓴다',
       'var tfixAny=uid=>tfixSlotsOf(uid)' in s and 'var tfixHay=uid=>tfixSlotsOf(uid)' in s)
    T2('Z-5 보기 줄이 txtOf 를 지난다', "txtOf(uid,'b'+b.\ud0a4)" in s)
    T2('Z-6 가려 두면 그림을 안 받는다(imgUrl 앞에 문이 있다)',
       "if(r[F.FILE]==='IMG'&&!figHid(uid))imgUrl(uid)" in s)
    T2('Z-7 DATA 원본·bogi·crop 을 안 건드렸다',
       s.count('r[F.CODE]=') == 0 and s.count("put('kv','bogi'") == base.count("put('kv','bogi'")
       and s.count("put('kv','crop'") == base.count("put('kv','crop'"))
    T2('Z-8 단축키 줄은 한 글자도 안 건드렸다(§C-2 — 일부러 죽여 둔 것)',
       "if(document.querySelector('.sheet'))return;" in s
       and s.count("if(e.key==='1')mark('O')") == base.count("if(e.key==='1')mark('O')"))
    T2('Z-9 줄끝이 원본과 같다(CRLF)', b.count(b'\r\n') == b.count(b'\n') and b.count(b'\r\n') > 0)
    T2('Z-10 본판 대비 늘기만 했다', len(s) > len(base))
    T2('Z-11 지운 본판 줄이 손댄 자리뿐이다',
       sum(1 for ln in base.split('\n') if ln.strip() and ln not in s_fb) <= 10,
       sum(1 for ln in base.split('\n') if ln.strip() and ln not in s_fb))
    return out


def main():
    want = [a for a in sys.argv[1:] if a in ('earth', 'bio', 'phys', 'null')] \
           or ['earth', 'bio', 'phys', 'null']
    cur = open(SRC, encoding='utf-8', newline='').read()
    basetxt = open(BASE, encoding='utf-8', newline='').read()
    # ★ A-6(d) 9/30 둘째 바퀴 — 생물·물리 무변(B·Y)은 이 판 인도판(fig_bogi d8a7d2e)을 고침 전 사본(cd248a5)과 맞댄다 — 지금 판은 뒤 판(shell_bio_phys c9faff2 등)이
    #   생물·물리를 일부러 바꿨다(결정로그 9/20 22:5x [사용자] · 9/21 02:10) · 첫 바퀴 earth_listpop 같은 꼴(a9f9fd4)
    fbtxt = subprocess.run(['git', '-C', GENIE, 'show', 'd8a7d2e:jagwa/index.html'], capture_output=True).stdout.decode('utf-8')
    lines = []
    W = int(os.environ.get('HARNESS_WAIT', '1500'))

    def T2(name, cond, info=''):
        lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))

    if 'earth' in want:
        ls, _ = run('earth', W, cur)
        lines += ls
    if 'bio' in want:
        ls, sn = run('bio', W, fbtxt)
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
        ls, sn = run('phys', W, fbtxt)
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
        for pre, ko in (('A', '§A 그림 가리기'), ('B', '§B 보기 고치기')):
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
    print('\n== 지학 목록판 %d PASS / %d FAIL / %d NOTE / %d항 ==' % (npass, nfail, nnote, len(lines)))
    print('캡처: %s' % CAP)
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
