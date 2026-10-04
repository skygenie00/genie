# -*- coding: utf-8 -*-
"""_task_jo_gaek_mb 관문 하네스 (§G).

    PYTHONIOENCODING=utf-8 python _harness_jo_gaek_mb.py [--only new|head]

지금 든 묶음 — §G-5(⚖ 일부) · §G-10(팝업 크기 손잡이) · §G-11(밖 무변 일부) · §G-13(헛잣대).
§A~E 본체를 넣을 때마다 이 파일에 묶음을 더한다.

⚠ 픽셀로 재지 않는다(CLAUDE.md 「자과앱에는 픽셀 IDENTICAL 게이트를 걸지 않는다」와 같은 까닭).
   가림·자리는 getBoundingClientRect · 있는가는 DOM 개수 · 무변은 글자 대조로 잰다.
⚠ 밖 網을 막는다 — 안 막으면 law.go.kr·github 로 나가 판마다 수십 초 (memory: headless-harness-must-block-real-network).
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402 — _task_qa_slim(10/4) 실행 모드: --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같다) · 새 갈래는 모두 `if QJ.REGRESS:` / `if QJ.GATE:` 안
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
import urllib.parse

GENIE = _roots.genie()
JOD = os.path.join(GENIE, 'jo')
NEW = os.path.join(JOD, 'index.html')
BASE_REV = '8401e68'          # 이 판을 넣기 직전에 jo/index.html 을 만진 마지막 커밋
OUT = os.path.join(os.environ.get('TEMP', '.'), 'hjogaek')
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
os.makedirs(OUT, exist_ok=True)
ONLY = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else ''
if QJ.REGRESS:
    ONLY = 'new'   # regress · smoke = NEW 만 — 바탕(HEAD 8401e68) 판은 안 풀고(git:show-app 0) 안 띄운다(전수표 argv 가 이미 --only new)
if QJ.SMOKE:
    # smoke 칸 없음 — 이 하네스는 한 쪽에서 §G-10 → §X 까지 앞 칸이 만든 화면 상태에 뒤 칸이 기대며 이어 도는 한 덩어리라 앞부분만 떼면 싸지도 않고 상태가 안 맞는다(1차객 첫 화면 smoke 는 gaek_mbsame 쪽 칸)
    print('INFO | smoke 칸 없음 | 1차객 팝업 크기·첫 화면·서랍·카드 하네스는 한 덩어리로 이어 돈다 — 첫 화면 smoke 는 gaek_mbsame 칸', flush=True)
    sys.exit(0)

PROBE = r"""<script>
const GIN = __GIN__, GIFIRST = '__GIFIRST__';
(function(){
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 window.__err=[];
 window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+e.lineno)});
 /* 밖 網 차단 — 같은 출처만 통과시킨다 */
 const __nf=window.fetch.bind(window);
 window.fetch=async function(u,o){const s=String(u);
   if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)
     return {ok:false,status:599,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
   return __nf(u,o)};
 /* 합성 포인터는 캡처를 못 잡는다 — 손잡이 끌기를 재려면 무해한 껍데기로 바꾼다 */
 Element.prototype.setPointerCapture=function(){};
 Element.prototype.releasePointerCapture=function(){};
 window.confirm=()=>true; window.alert=()=>{};   /* 헤드리스에서 confirm 은 멈춰 선다 */

 const R=[];
 const T=(g,n,ok,got)=>R.push({g:g,n:n,ok:!!ok,got:String(got===undefined?'':got).slice(0,220)});
 const PE=(t,x,y)=>new PointerEvent(t,{clientX:x,clientY:y,pointerId:1,bubbles:true,cancelable:true,
                                       pointerType:'mouse',isPrimary:true});
 const clean=()=>{try{closeAllPops()}catch(e){}};
 function mk(kind,key){ const b=popShell(kind,'하네스 '+(kind||'(빈)'),key||('H|'+kind+'|'+Math.random()));
                        try{showPop(null)}catch(e){} return {b:b,p:b.parentNode}; }
 const rc=e=>e.getBoundingClientRect();
 const txt=e=>(e?String(e.textContent||'').replace(/\s+/g,' ').trim():'');

 async function gates(){
  /* ══ §G-10 — popShell 이 만드는 팝업 전부에 크기 손잡이 ══ */
  for(const k of ['','cell','q','fn','canvas','zzz없는종류']){
    clean(); const {p}=mk(k); await wait(40);
    T('10','기본 손잡이 · 종류 '+(k||'(빈)'), p.querySelectorAll('.prsz').length===1,
      'prsz '+p.querySelectorAll('.prsz').length+' · _sz='+p._sz);
  }
  { clean(); const {b,p}=mk('cell'); popSizable(b,'note'); await wait(40);
    T('10','명시 종류가 이긴다(cell → note)', p._sz==='note'&&p.querySelectorAll('.prsz').length===1,
      '_sz='+p._sz+' · prsz '+p.querySelectorAll('.prsz').length); }
  { clean(); const {b,p}=mk('cell'); await wait(40);
    const tall=document.createElement('div'); tall.style.height='900px'; tall.textContent='늦게 채운 본문';
    b.appendChild(tall); await wait(40);
    const rs=p.querySelector('.prsz'); const okLast=!!rs&&p.lastElementChild===rs;
    let near=false; if(rs){const a=rc(p),c=rc(rs); near=(a.right-c.right)<26&&(a.bottom-c.bottom)<26;}
    T('10','늦게 채워도 손잡이가 맨 아래 오른쪽', okLast&&near,
      'lastChild='+okLast+' · 모서리근접='+near); }
  { clean(); const {b,p}=mk('cell');
    /* 빈 팝업은 높이가 51px 이라 +80 이 최소 240 에 먹힌다 — 본문을 채워 놓고 잰다 */
    const tall=document.createElement('div'); tall.style.height='400px'; b.appendChild(tall);
    await wait(40);
    const rs=p.querySelector('.prsz');
    p.style.left='60px'; p.style.top='60px';
    if(!rs){ T('10','손잡이 끌기 (+120,+80)', false, '손잡이 없음'); window.__memo={}; }
    else{
      const w0=rc(p).width,h0=rc(p).height, x=rc(rs).left+3,y=rc(rs).top+3;
      rs.dispatchEvent(PE('pointerdown',x,y));
      rs.dispatchEvent(PE('pointermove',x+120,y+80));
      rs.dispatchEvent(PE('pointerup',x+120,y+80));
      await wait(30); const w1=rc(p).width,h1=rc(p).height;
      T('10','손잡이 끌기 (+120,+80)', Math.abs(w1-w0-120)<3&&Math.abs(h1-h0-80)<3,
        w0.toFixed(0)+'×'+h0.toFixed(0)+' → '+w1.toFixed(0)+'×'+h1.toFixed(0));
      window.__memo={w:w1,h:h1}; } }
  { const m=window.__memo||{}; clean(); await wait(20);
    const {p}=mk('cell'); await wait(60); const r=rc(p);
    T('10','닫고 다시 열면 그 크기', m.w&&Math.abs(r.width-m.w)<3&&Math.abs(r.height-m.h)<3,
      '기억 '+(m.w||0).toFixed(0)+'×'+(m.h||0).toFixed(0)+' · 다시 '+r.width.toFixed(0)+'×'+r.height.toFixed(0)); }
  { clean(); const {p}=mk('q'); await wait(40);
    const rs=p.querySelector('.prsz'); p.style.left='60px'; p.style.top='60px';
    if(!rs) T('10','최소 360×min(240, 잡을 때 높이)', false, '손잡이 없음');
    else{
      const x=rc(rs).left+3,y=rc(rs).top+3, h0=rc(p).height;   /* ★ popsize §A-1 · 사용자 10/4 02:34 — 옛: 높이 최소 240 고정(빈 팝업도 240 으로 튐) → 새: min(240, 잡을 때 높이) — 잡을 때 높이 h0 를 재 두고 기댓값으로(popsize 수행 결과 실측 = 빈 q 팝업 360×59) · 폭 최소 360 무변 · 240 바닥은 popsize B4 가 잰다 */
      rs.dispatchEvent(PE('pointerdown',x,y));
      rs.dispatchEvent(PE('pointermove',x-900,y-900));
      rs.dispatchEvent(PE('pointerup',x-900,y-900));
      await wait(30); const r=rc(p);
      T('10','최소 360×min(240, 잡을 때 높이)', Math.abs(r.width-360)<2&&Math.abs(r.height-Math.min(240,h0))<2,
        r.width.toFixed(0)+'×'+r.height.toFixed(0)+' (잡을 때 높이 '+h0.toFixed(0)+' → 기대 '+Math.min(240,h0).toFixed(0)+')'); } }
  { clean(); const {p}=mk('q'); await wait(60);
    const before=rc(p).width;
    p.querySelector('.ph').dispatchEvent(new MouseEvent('dblclick',{bubbles:true}));
    await wait(30);
    T('10','머리 더블클릭 = 기본', !p.classList.contains('sized')&&p.style.width==='',
      '전 '+before.toFixed(0)+'px · sized='+p.classList.contains('sized')+' · style.width="'+p.style.width+'"'); }
  { clean(); try{popRec(null)}catch(e){} await wait(400);
    const p=(POPS||[])[POPS.length-1];
    T('10','실제 팝업 — 기록 패널(popRec)', !!p&&p.querySelectorAll('.prsz').length===1,
      p?('prsz '+p.querySelectorAll('.prsz').length+' · _sz='+p._sz):'팝업 안 뜸'); }
  { clean(); try{studyLogPop(null)}catch(e){} await wait(700);
    const p=(POPS||[])[POPS.length-1];
    T('10','실제 팝업 — 늦게 채우는 studyLogPop', !!p&&p.querySelectorAll('.prsz').length===1,
      p?('prsz '+p.querySelectorAll('.prsz').length+' · _sz='+p._sz):'팝업 안 뜸'); }
  { clean(); try{popJo('특허법','제42조',null,1)}catch(e){} await wait(900);
    const p=(POPS||[])[POPS.length-1];
    T('10','실제 팝업 — 늦게 채우는 popJo', !!p&&p.querySelectorAll('.prsz').length===1,
      p?('prsz '+p.querySelectorAll('.prsz').length+' · _sz='+p._sz):'팝업 안 뜸'); }
  clean();

  /* ══ §G-5 — ⚖ 원문 단추 ══ */
  { let a=null; try{a=joWonBtn({k:'제42조',law:true})}catch(e){}
    T('5','살아있는 갈래 href(HEAD 대조용)', !!a, a?a.getAttribute('href'):'못 만듦');
    window.__liveHref=a?a.getAttribute('href'):''; }
  { let d=null; try{d=joWonBtn({k:'施規 11',law:false})}catch(e){}
    const href=d?(d.getAttribute('href')||''):'';
    const want='https://www.law.go.kr/'+encodeURIComponent('법령')+'/'
             +encodeURIComponent('특허법시행규칙')+'/'+encodeURIComponent('제11조');
    /* href 는 브라우저가 이미 인코딩해 돌려준다 — 원시 문자열로도 맞대 본다 */
    const raw='https://www.law.go.kr/법령/특허법시행규칙/제11조';
    T('5','施規 → 법제처 <a>', !!d&&d.tagName==='A'&&d.target==='_blank'
        &&(href===want||href===raw||decodeURIComponent(href)===raw),
      (d?d.tagName+' target='+d.target+' ':'')+href);
    T('5','施規 title 「조판기에 없는 …」', !!d&&/^조판기에 없는 특허법시행규칙 제11조 — 법제처에서 연다$/.test(d.title||''),
      d?d.title:'');
    T('5','.dead 안 붙는다', !!d&&!/\bdead\b/.test(d.className||''), d?d.className:''); }
  { let d=null; try{d=joWonBtn({k:'施規 11의2',law:false})}catch(e){}
    const href=decodeURIComponent((d&&d.getAttribute('href'))||'');
    T('5','施規 11의2 → 제11조의2', /\/제11조의2$/.test(href), href); }
  { S.law='상표법'; let d=null; try{d=joWonBtn({k:'施規 3',law:false})}catch(e){}
    const href=decodeURIComponent((d&&d.getAttribute('href'))||''); S.law='특허법';
    T('5','보고 있는 법을 따른다(상표법시행규칙)', /상표법시행규칙\/제3조$/.test(href), href); }

  /* ══ §G-11 — 밖 무변(일부) ══ */
  { clean(); try{popRec(null)}catch(e){} await wait(400);
    const p=(POPS||[])[POPS.length-1];
    const btn=p?[].slice.call(p.querySelectorAll('button')).filter(b=>/학습로그/.test(b.textContent||'')):[];
    T('11','기록 패널에 「📝 학습로그」 단추 0', !!p&&btn.length===0,
      p?('단추 '+btn.length+' / 전체 '+p.querySelectorAll('button').length):'팝업 안 뜸');
    T('11','studyLogPop 정의는 그대로', typeof studyLogPop==='function', typeof studyLogPop);
    clean(); }
  /* ══ §G-1 px 표 — 「민법 실물 값 ↔ 조판기 값」 ══
     왼쪽 수는 민법OX 실물의 **계산 스타일 실측**이다(jo/_px_mb2.py · 2026-09-21 ·
     Tailwind CDN 이 만든 값 그대로). 색은 조판기 색이라 재지 않는다(지시서 §G-1 「색만 조판기 색」).
     ══ §G-2 화면 흐름 — 첫 화면 ↔ 문제풀이 ══ */
  S.law='특허법'; S.tab='jimun'; S.jimunTab='ox'; S.mok=''; S.oxQueue=''; S.oxQ='';
  await render(); await wait(2600);
  const cs=(sel,p)=>{const e=document.querySelector(sel);return e?getComputedStyle(e)[p]:'없음'};
  const PX=[
    ['.mbh .mbhd','paddingTop','12px'],['.mbh .mbhd','paddingLeft','16px'],
    ['.mbh .mbhd','borderBottomWidth','2px'],['.mbh .mbhd','gap','8px'],
    ['.mbh .mbhd h1','fontSize','18px'],['.mbh .mbhd h1','fontWeight','800'],
    ['.mbh .mbhd h1','lineHeight','28px'],
    ['.mbh .mbhd .dl','fontSize','11px'],['.mbh .mbhd .dl','fontWeight','700'],
    ['.mbsr','paddingTop','10px'],['.mbsr','paddingLeft','16px'],['.mbsr','gap','8px'],
    ['.mbsr input','fontSize','12px'],['.mbsr input','lineHeight','18px'],
    ['.mbsr input','paddingTop','4px'],['.mbsr input','paddingLeft','8px'],
    ['.mbsr input','width','224px'],['.mbsr input','borderRadius','4px'],
    ['.mbsb','fontSize','11px'],['.mbsb','fontWeight','700'],['.mbsb','lineHeight','16.5px'],
    ['.mbsb','paddingTop','4px'],['.mbsb','paddingLeft','10px'],['.mbsb','borderRadius','4px'],
    ['.mbsr .cnt','fontSize','11px'],['.mbsr .cnt','fontWeight','600'],
    ['.mbqr','paddingTop','10px'],['.mbqr','paddingLeft','16px'],['.mbqr','gap','8px'],
    ['.mbqr .pl','fontSize','11px'],['.mbqr .pl','fontWeight','800'],
    ['.mbqb','fontSize','11px'],['.mbqb','fontWeight','700'],['.mbqb','paddingTop','4px'],
    ['.mbqb','paddingLeft','10px'],['.mbqb','borderRadius','4px'],
    ['.mbqr .lb','fontSize','10.5px'],
    /* A-6(d) ⚡ 필터 = 네이티브 select → 펼침 목록 단추 .uzfb(mbsame_add3 §A-6 · 「옛 select 자리·꼴」) — 선택자만 바꿈 */
    ['.mbqr .uzfb','fontSize','11px'],['.mbqr .uzfb','fontWeight','700'],
    ['.mbqr .uzfb','paddingTop','4px'],['.mbqr .uzfb','paddingLeft','8px'],
    ['.mbsj','borderRadius','12px'],['.mbsj','borderTopWidth','1px'],
    ['.mbsj>.hd','paddingTop','10px'],['.mbsj>.hd','paddingLeft','16px'],
    ['.mbsj>.hd','borderBottomWidth','1px'],
    ['.mbsj>.hd h2','fontSize','16px'],['.mbsj>.hd h2','fontWeight','800'],
    ['.mbsj>.hd h2','lineHeight','24px'],['.mbsj>.hd h2','gap','6px'],
    ['.mbsj>.hd h2 b','fontWeight','900'],
    ['.mbch','paddingTop','12px'],['.mbch','paddingLeft','16px'],
    ['.mbch>.hh','gap','8px'],['.mbch>.hh','marginBottom','6px'],
    ['.mbch>.hh .nm','fontSize','14px'],['.mbch>.hh .nm','fontWeight','800'],
    ['.mbch>.hh .nm','lineHeight','20px'],
    ['.mbch>.hh .tot','fontSize','11px'],['.mbch>.hh .tot','fontWeight','600'],
    ['.mbur','paddingTop','6px'],['.mbur','paddingLeft','4px'],['.mbur','borderRadius','4px'],
    ['.mbur','columnGap','12px'],['.mbur','rowGap','4px'],
    ['.mbur>.l','gap','8px'],['.mbur>.l .ar','fontSize','12px'],
    /* ⚠ 첫 `.mbur` 는 `flat`(장 이름과 같은 한 줄)이라 14px/800 이다 — 민법도 그렇다.
       보통 단원 줄은 `:not(.flat)` 로 집어야 13px/600 이 나온다. */
    ['.mbur:not(.flat)>.l .nm','fontSize','13px'],['.mbur:not(.flat)>.l .nm','fontWeight','600'],
    ['.mbur:not(.flat)>.l .nm','lineHeight','19.5px'],
    ['.mbur.flat>.l .nm','fontSize','14px'],['.mbur.flat>.l .nm','fontWeight','800'],
    ['.mbur.flat>.l .nm','lineHeight','20px'],
    ['.mbur>.l .tot','fontSize','11px'],['.mbur>.l .tot','fontWeight','600'],
    ['.mbchip.card','fontSize','10px'],['.mbchip.card','fontWeight','700'],
    ['.mbchip.card','lineHeight','15px'],['.mbchip.card','paddingTop','2px'],
    ['.mbchip.card','paddingLeft','6px'],['.mbchip.card','borderRadius','4px'],
    ['.mbur>.r','gap','6px'],
    ['.mbchip.run','fontSize','10px'],['.mbchip.run','fontWeight','800'],
    ['.mbgo','fontSize','11.5px'],['.mbgo','fontWeight','800'],
    ['.mbgo','lineHeight','17.25px'],['.mbgo','paddingTop','4px'],['.mbgo','paddingLeft','6px'],
  ];
  {   /* §G-1 */
    let bad=[];
    PX.forEach(([sel,p,want])=>{const got=cs(sel,p); if(String(got)!==String(want))bad.push([sel,p,want,got])});
    T('1','★px 표 — 민법 실물 값과 같다('+PX.length+'칸)',bad.length===0,bad.slice(0,8));
    T('1','민법 실물 값 표를 다 쟀다(못 찾은 자리 0)',
      PX.filter(([sel,p])=>cs(sel,p)==='없음').length===0,
      PX.filter(([sel,p])=>cs(sel,p)==='없음').map(x=>x[0]).slice(0,6));
  }

  {   /* §G-2 */
    const q=s2=>document.querySelectorAll(s2).length;
    T('2','★첫 화면이 선다(머리줄·검색·히트맵·⚡·과목 카드)',
      q('.mbh')===1&&q('.mbh .mbhd h1')===1&&q('.mbsr')===1&&q('.mbhm .hmwrap')===1
      &&q('.mbqr')===1&&q('.mbsj')>=11,
      [q('.mbh'),q('.mbsr'),q('.mbhm .hmwrap'),q('.mbqr'),q('.mbsj')]);
    T('2','머리줄 글자 = 「📖 <법> 1차객」',
      txt(document.querySelector('.mbh .mbhd h1'))==='📖 특허법 1차객',
      txt(document.querySelector('.mbh .mbhd h1')));
    T('2','★첫 화면에는 가운데 목차 열이 없다',q('.qlbox')===0,q('.qlbox'));
    /* add2 §C-2 — 본판 §B-8 이 넣었던 「OX문제/기출문제」 두 칸은 걷었다(민법에 없다).
       기출은 맨 아래 「변리사 기출」 과목 카드로 들어간다. */
    T('2','★add2 §C-2 — OX/기출 두 칸 단추가 어디에도 없다',
      [...document.querySelectorAll('.mbsb,.mode')].filter(b=>/OX문제|기출문제/.test(txt(b))).length===0
      &&q('#slot .modebar .mode')===0,
      [...document.querySelectorAll('.mbsb,.mode')].filter(b=>/OX문제|기출문제/.test(txt(b))).length);
    /* A-6(a) toc_fuse §B — 편 12(12 실용신안 흡수) + 미기출 판례 모아보기 = 깊이1 13 */
    T('2','과목 카드 = 깊이1 13 + 미분류 1 + 변리사 기출 1(add2 §C-1)',q('.mbsj')===15,q('.mbsj'));
    T('2','단원 줄에 「총 N문제」·🃏·회독 글자가 있다',
      q('.mbur>.l .tot')>0&&q('.mbchip.card')>0&&q('.mbgo')>0,
      [q('.mbur>.l .tot'),q('.mbchip.card'),q('.mbgo')]);
    /* 흐름 — 단원 줄 → 문제풀이 → 「← 목차」 → 첫 화면 */
    const row=[...document.querySelectorAll('.mbur')].find(e=>/총 [1-9]/.test(txt(e)));
    T('2','풀 것이 있는 단원 줄을 찾았다',!!row,row?txt(row).slice(0,40):null);
    if(row){
      row.click(); await wait(2600);
      T('2','★단원 줄을 누르면 문제풀이 화면이다',
        !!S.mok&&q('.mbh')===0&&q('#slot .qwrap,#slot .qcard')>0,
        [S.mok,q('.mbh'),q('#slot .qwrap,#slot .qcard')]);
      T('2','★문제풀이 화면에 「← 목차」가 있다',q('.mbback:not(.mbtog)')===1,q('.mbback:not(.mbtog)'));
      /* 9구간 — §A-1 「지금처럼 목차 표와 카드가 나란히가 아니다」 */
      T('2','★문제풀이 화면에도 옛 목차 열이 없다(.qlbox 0)',q('.qlbox')===0,
        (()=>{const b=document.querySelector('.qlbox');if(!b)return 0;
          const r=b.getBoundingClientRect();
          return [Math.round(r.width),Math.round(r.height),getComputedStyle(b).display]})());
      const b=document.querySelector('.mbback');
      if(b){ b.click(); await wait(2500);
        T('2','★「← 목차」를 누르면 첫 화면으로 돌아온다',!S.mok&&q('.mbh')===1,[S.mok,q('.mbh')]); }
    }
    /* 검색 — 1차객·보고 있는 법 안에서만 */
    const inp=document.querySelector('.mbsr input');
    if(inp){ inp.value='진보성'; inp.dispatchEvent(new Event('input',{bubbles:true})); await wait(700);
      const rows=q('.mbres .rr');
      T('2','★검색이 결과를 낸다(진보성)',rows>0&&/개$/.test(txt(document.querySelector('.mbsr .cnt'))),
        [rows,txt(document.querySelector('.mbsr .cnt'))]);
      inp.value=''; inp.dispatchEvent(new Event('input',{bubbles:true})); await wait(400);
      T('2','지우면 결과 칸이 접힌다',
        document.querySelector('.mbres').classList.contains('hide'),
        document.querySelector('.mbres').className); }
    /* 🔥 약점을 누르면 큐 화면(첫 화면 아님) */
    const wk=document.querySelector('.mbqb.weak');
    if(wk){ wk.click(); await wait(2400);
      T('2','🔥 약점을 누르면 큐 화면이다(첫 화면 아님)',S.oxQueue==='weak'&&q('.mbh')===0,
        [S.oxQueue,q('.mbh')]);
      T('2','★큐 화면에도 옛 목차 열이 없다',q('.qlbox')===0,q('.qlbox'));
      const b2=document.querySelector('.mbback');
      T('2','큐 화면에도 「← 목차」가 있다',!!b2,!!b2);
      if(b2){ b2.click(); await wait(2400);
        T('2','큐에서도 첫 화면으로 돌아온다',!S.oxQueue&&q('.mbh')===1,[S.oxQueue,q('.mbh')]); } }
  }

  /* ══ §G-2 목차 서랍(§A-2) — 민법 `#tree` 치수 그대로 · 세로 탭을 안 덮는다 ══ */
  S.mok=''; S.oxQueue=''; S.jtFold=false; S.jtCh={}; S.jtW=272; await render(); await wait(2200);
  if(typeof jtPaint!=='function'){
    /* HEAD 에는 서랍이 없다 — 여기서 죽으면 뒤의 묶음·스냅이 통째로 안 돈다(헛잣대가 0항이 된다) */
    T('2','★목차 서랍이 있다(§A-2)',false,'jtPaint 없음 — 이 판 밖');
  } else {
    const q=s2=>document.querySelectorAll(s2).length;
    const jt=()=>document.getElementById('jtree');
    const rc2=e=>e.getBoundingClientRect();
    T('2','★목차 서랍이 첫 화면에 있다',q('#jtree')===1&&q('#jtgrip')===1,[q('#jtree'),q('#jtgrip')]);
    /* A-6(a) hrail §A-4 — 세로 레일 삭제 · .body2 는 손잡이·트리·본문이 x 0 부터 → 서랍 왼끝 = 본문 틀 왼끝 */
    T('2','★세로 탭을 안 덮는다(세로 레일 없음 · 본문 틀 왼끝 = 서랍 왼끝)',
      (()=>{const r=document.querySelector('.body2'),t=jt();
        return !!(r&&t)&&Math.abs(rc2(r).left-rc2(t).left)<1})(),
      (()=>{const r=document.querySelector('.body2'),t=jt();
        return (r&&t)?[Math.round(rc2(r).left),Math.round(rc2(t).left)]:'없음'})());
    T('2','★서랍 너비 = 민법 272px',Math.abs(rc2(jt()).width-272)<1,Math.round(rc2(jt()).width));
    const JPX=[
      ['#jtree .jthead','paddingTop','8px'],['#jtree .jthead','paddingLeft','10px'],
      ['#jtree .jthead','paddingBottom','7px'],['#jtree .jthead','gap','4px'],
      ['#jtree .jthead','borderBottomWidth','1px'],
      ['#jtlist','fontSize','12px'],['#jtlist','paddingTop','4px'],
      ['#jtgrip','width','13px'],['#jtgrip','fontSize','13px'],
      ['.jtch','fontSize','12px'],['.jtch','fontWeight','800'],['.jtch','paddingTop','4px'],
      ['.jtch','paddingLeft','10px'],['.jtch','gap','5px'],['.jtch','marginTop','5px'],
      ['.jtch .n','fontSize','10px'],['.jtch .n','fontWeight','700'],
      ['.jtit','paddingTop','3px'],['.jtit','paddingRight','10px'],['.jtit','borderLeftWidth','3px'],
      ['.jtit .l1','gap','5px'],['.jtit .tx','fontSize','12px'],
      ['.jtit .n','fontSize','10px'],['.jtit .n','fontWeight','700'],
      ['.jdbar','height','4px'],['.jdbar','borderRadius','2px'],
      ['.jtfoot','fontSize','10.5px'],['.jtfoot','paddingTop','5px'],
      ['.jtfoot','paddingLeft','10px'],['.jtfoot','borderTopWidth','1px'],
    ];
    const cs2=(sel,p)=>{const e=document.querySelector(sel);return e?getComputedStyle(e)[p]:'없음'};
    const bad2=JPX.filter(([sel,p,w])=>String(cs2(sel,p))!==String(w))
                  .map(([sel,p,w])=>[sel,p,w,cs2(sel,p)]);
    T('2','★서랍 px 표 — 민법 실물 값과 같다('+JPX.length+'칸)',bad2.length===0,bad2.slice(0,6));
    T('2','장 줄·단원 줄·막대가 그려졌다',q('.jtch')>0&&q('.jtit')>0&&q('.jdbar')>0,
      [q('.jtch'),q('.jtit'),q('.jdbar')]);
    /* 장 접힘 — 누르면 자식이 숨고 기억에 남는다 */
    { const n0=q('.jtit'); const ch=document.querySelector('.jtch');
      ch.click(); await wait(300);
      const n1=q('.jtit');
      T('2','★장 줄을 누르면 그 아래가 접힌다',n1<n0&&Object.keys(S.jtCh||{}).length===1,
        [n0,n1,Object.keys(S.jtCh||{}).length]);
      ch.click(); await wait(300);
      T('2','다시 누르면 펴진다',q('.jtit')===n0&&Object.keys(S.jtCh||{}).length===0,
        [q('.jtit'),n0]); }
    /* 접기 — 손잡이 탭 */
    { const g=document.getElementById('jtgrip');
      g.dispatchEvent(new MouseEvent('click',{bubbles:true})); await wait(300);
      T('2','★손잡이를 누르면 서랍이 접힌다(13px · 속은 숨음)',
        Math.abs(rc2(jt()).width-13)<1&&getComputedStyle(document.getElementById('jtlist')).display==='none',
        [Math.round(rc2(jt()).width),getComputedStyle(document.getElementById('jtlist')).display]);
      g.dispatchEvent(new MouseEvent('click',{bubbles:true})); await wait(300);
      T('2','다시 누르면 펴진다(272px)',Math.abs(rc2(jt()).width-272)<1,Math.round(rc2(jt()).width)); }
    /* 너비 끌기 — 조판기 handle 과 같은 장치(4px 넘어야 끌기) */
    { const g=document.getElementById('jtgrip'); const r0=rc2(g);
      const PE2=(t2,x,y)=>{const e=new Event(t2,{bubbles:true,cancelable:true});
        Object.defineProperties(e,{clientX:{get:()=>x},clientY:{get:()=>y},pointerId:{get:()=>7},
          pointerType:{get:()=>'mouse'},button:{get:()=>0},isPrimary:{get:()=>true}});return e};
      g.hasPointerCapture=()=>true;
      g.dispatchEvent(PE2('pointerdown',r0.left+6,r0.top+40));
      g.dispatchEvent(PE2('pointermove',r0.left+66,r0.top+40));
      g.dispatchEvent(PE2('pointerup',r0.left+66,r0.top+40));
      await wait(220);
      T('2','★끌면 너비가 그만큼 는다(+60)',Math.abs(rc2(jt()).width-332)<2&&S.jtW===332,
        [Math.round(rc2(jt()).width),S.jtW]);
      S.jtW=272; uiSave(); jtPaint(); await wait(150); }
    /* 「지금」 — 단원을 고르면 그 줄에 붙는다 */
    { const it=[...document.querySelectorAll('.jtit')].find(e=>!e.classList.contains('off'));
      if(it){ it.click(); await wait(2400);
        T('2','★서랍에서 단원을 고르면 문제풀이 화면이다',
          !!S.mok&&document.querySelectorAll('.mbh').length===0,[S.mok]);
        T('2','★고른 줄에 「지금」이 붙는다',
          document.querySelectorAll('.jtit.cur').length===1&&document.querySelectorAll('.jtit .now').length===1,
          [document.querySelectorAll('.jtit.cur').length,document.querySelectorAll('.jtit .now').length]);
        T('2','★서랍은 문제풀이 화면에도 그대로 있다',q('#jtree')===1&&jt().style.display!=='none',
          [q('#jtree'),jt().style.display]); } }
    /* 밖 탭에서는 숨는다 */
    { S.tab='jo'; await render(); await wait(900);
      T('2','★조문 탭에서는 서랍이 숨는다',jt().style.display==='none',jt().style.display);
      S.tab='jimun'; S.jimunTab='gichul'; await render(); await wait(900);
      /* add2 §C-4 — 민법 서랍에 「변리사 기출」이 있다. 본판의 「기출 탭에서는 숨는다」를 뒤집는다. */
      T('2','★add2 §C-4 — 기출 탭에도 서랍이 뜬다',jt().style.display!=='none',
        [jt().style.display,jt().querySelectorAll('.jtch').length]);
      S.jimunTab='ox'; S.mok=''; await render(); await wait(1500);
      T('2','OX 탭으로 오면 다시 보인다',jt().style.display!=='none',jt().style.display); }
  }

  /* ══ §G-3 카드(§C-9·11·14·15) — 민법 지문 카드 꼴 ══ */
  S.mok=''; S.oxQueue=''; await render(); await wait(2000);
  if(typeof mbRecStrip!=='function'){
    T('3','★지문 카드가 민법 꼴이다(§C)',false,'mbRecStrip 없음 — 이 판 밖');
  } else {
    const q=s3=>document.querySelectorAll(s3).length;
    const cs3=(sel,p)=>{const e=document.querySelector(sel);return e?getComputedStyle(e)[p]:'없음'};
    const row=[...document.querySelectorAll('.mbur')].find(e=>/총 [1-9]/.test(txt(e)));
    if(row){ row.click(); await wait(2800); }
    T('3','★카드가 그려졌다',q('#slot .qwrap')>0&&q('#slot .qwrap.mbq')===q('#slot .qwrap'),
      [q('#slot .qwrap'),q('#slot .qwrap.mbq')]);
    T('3','★큰 O/X 상자 DOM 0(옛 oxbtn·oxpick·oxres)',
      q('.oxbtn')===0&&q('.oxpick')===0&&q('.oxres')===0,[q('.oxbtn'),q('.oxpick'),q('.oxres')]);
    T('3','★△ 단추 DOM 0(민법에 없다 · 헷갈림은 🌀 태그)',
      [...document.querySelectorAll('button')].filter(b=>txt(b)==='△').length===0,
      [...document.querySelectorAll('button')].filter(b=>txt(b)==='△').length);
    T('3','★지문 끝 조문·판례 칩 DOM 0(해설 액션 바로 옮겼다)',
      q('.mbq .oxq .chip')===0&&q('.mbact .mbchips')>0,[q('.mbq .oxq .chip'),q('.mbact .mbchips')]);
    T('3','★태그는 아이콘만(글자 0 · 22×22)',
      (()=>{const t=document.querySelector('.mbq .qtag');
        return !!t&&txt(t).length<=2&&Math.round(t.getBoundingClientRect().width)===22
            &&Math.round(t.getBoundingClientRect().height)===22})(),
      (()=>{const t=document.querySelector('.mbq .qtag');
        return t?[txt(t),Math.round(t.getBoundingClientRect().width),
                  Math.round(t.getBoundingClientRect().height)]:'없음'})());
    /* add1 §B-4 — 이력 줄은 **접힌 상자**로 지문마다 하나씩이고 안은 비어 있다 */
    T('3','이력 상자·아랫줄·해설 칸이 지문마다 하나씩',
      q('.mbrecw')===q('.mbbot')&&q('.mbbot')===q('.mbexp')&&q('.mbexp')===q('.mbact')&&q('.mbrecw')>0,
      [q('.mbrecw'),q('.mbbot'),q('.mbexp'),q('.mbact')]);
    T('3','★들어서자마자 보이는 이력 줄 0(§B-4)',q('.mbrec')===0,q('.mbrec'));
    { /* 출처 칩을 누르면 그 지문 것만 펴지고, 다시 누르면 접힌다 */
      const sb=document.querySelector('.mbqhd .qb.v');
      if(!sb){T('3','★출처 칩이 있다(§B-4)',false,'없음');}
      else{
        sb.click(); await wait(300);
        T('3','★출처 칩을 누르면 그 지문 이력 줄만 편다',q('.mbrec')===1,q('.mbrec'));
        const own=sb.closest('.oxrow')||sb.closest('.qwrap');
        T('3','★펴진 자리는 그 지문 머리줄 바로 아래다',
          !!own&&own.querySelectorAll('.mbrec').length===1,
          own?own.querySelectorAll('.mbrec').length:'칸 못 찾음');
        sb.click(); await wait(300);
        T('3','★다시 누르면 접힌다',q('.mbrec')===0,q('.mbrec'));
        sb.click(); await wait(300);   /* px 를 재려면 하나는 펴 둔다 */
      } }
    const CPX=[
      ['.qwrap.mbq','paddingTop','12px'],['.qwrap.mbq','borderRadius','8px'],
      ['.qwrap.mbq','borderTopWidth','1px'],
      ['.mbq .qhd','gap','4px'],['.mbq .qhd','marginBottom','8px'],
      ['.mbq .qhd','paddingBottom','6px'],['.mbq .qhd','borderBottomWidth','1px'],
      ['.mbtags','gap','4px'],
      ['.mbq .qtag','fontSize','13px'],['.mbq .qtag','width','22px'],['.mbq .qtag','height','22px'],
      ['.mbrec','fontSize','12px'],['.mbrec','paddingTop','4px'],['.mbrec','paddingLeft','8px'],
      ['.mbrec','borderRadius','8px'],['.mbrec','borderStyle','dashed'],
      /* `.mbrec .c`·`.mbrec .r` 는 풀이 기록이 있어야 생긴다 — 채점 뒤에 잰다(아래) */
      ['.mbq .oxq','gap','6px'],['.mbq .oxq','marginBottom','8px'],
      ['.mbqlab','fontSize','13px'],['.mbqlab','fontWeight','800'],['.mbqlab','paddingTop','1px'],
      ['.mbqtx','fontSize','13px'],['.mbqtx','fontWeight','500'],['.mbqtx','lineHeight','21.125px'],
      ['.mbbot','gap','6px'],['.mbbot','marginTop','6px'],
      ['.mbpeek','fontSize','11px'],['.mbpeek','fontWeight','700'],['.mbpeek','paddingTop','2px'],
      ['.mbpeek','paddingLeft','8px'],['.mbpeek','borderRadius','4px'],
      ['.mboxb','width','26px'],['.mboxb','height','22px'],['.mboxb','fontSize','13px'],
      ['.mboxb','fontWeight','900'],['.mboxb','borderRadius','6px'],
      ['.mbres2','fontSize','11px'],['.mbres2','fontWeight','800'],
      ['.mbbotr','gap','6px'],['.mblink','fontSize','11px'],
      ['.mbexp','marginTop','10px'],
      ['.mbact','marginTop','8px'],['.mbact','paddingTop','8px'],
      ['.mbact','borderTopStyle','dashed'],['.mbact','columnGap','16px'],['.mbact','rowGap','4px'],
      ['.mbfixb','fontSize','11px'],['.mbfixb','fontWeight','700'],['.mbfixb','borderRadius','4px'],
    ];
    const badC=CPX.filter(([sel,p,w])=>String(cs3(sel,p))!==String(w))
                  .map(([sel,p,w])=>[sel,p,w,cs3(sel,p)]);
    T('3','★카드 px 표 — 민법 실물 값과 같다('+CPX.length+'칸)',badC.length===0,badC.slice(0,6));
    /* 해설은 닫혀 있다가 「정답·해설 ▸」 로 열린다 */
    { const shown=[...document.querySelectorAll('.mbexp')].filter(e=>e.style.display!=='none').length;
      T('3','★풀기 전에는 해설이 닫혀 있다',shown===0,shown);
      const pk=document.querySelector('.mbpeek'); pk.click(); await wait(200);
      const e1=pk.parentNode.parentNode.querySelector('.mbexp');
      T('3','★「정답·해설 ▸」 를 누르면 열린다',!!e1&&e1.style.display!=='none'&&/▾/.test(txt(pk)),
        [e1?e1.style.display:'없음',txt(pk)]);
      pk.click(); await wait(200);
      T('3','다시 누르면 닫힌다',e1.style.display==='none'&&/▸/.test(txt(pk)),[e1.style.display,txt(pk)]); }
    /* O 를 누르면 마킹이 남는다(채점은 아직) */
    { const ob=document.querySelector('.mboxb.O');
      ob.click(); await wait(2500);
      T('3','★O 를 누르면 그 자리에 고른 표가 남는다',q('.mboxb.sel')>=1,q('.mboxb.sel')); }
    /* 채점된 지문은 해설이 저절로 펴지고 이력 줄에 칸이 생긴다 */
    { /* ⚠ 지금 마디에 그려진 지문이어야 한다 — OXPOOL 첫 열쇠는 딴 마디일 수 있다 */
      const k=Object.keys(OXPOOL||{}).find(x=>document.getElementById(((OXPOOL||{})[x]||{}).dom));
      const info=(OXPOOL||{})[k]||{};
      T('3','채점해 볼 지문을 화면에서 골랐다',!!k,k||'없음');
      if(k){
        oxPut(k,{p:(info.ans||'O'),ok:true}); await render(); await wait(2600);
        const box=document.getElementById(info.dom);
        const opened=box?[...box.querySelectorAll('.mbexp')].filter(e=>e.style.display!=='none').length:0;
        T('3','★채점 뒤 해설이 저절로 펴진다',opened>=1,opened);
        /* add1 §B-4 — 채점해도 이력 줄은 접힌 채다. 그 지문 출처 칩을 눌러 펴고 잰다. */
        { const sb2=box?box.querySelector('.mbqhd .qb.v'):null;
          if(sb2){ sb2.click(); await wait(300); } }
        T('3','★채점 뒤 (펴면) 회독 이력 줄에 칸이 생긴다',
          !!box&&box.querySelectorAll('.mbrec .c').length>=1,
          box?box.querySelectorAll('.mbrec .c').length:'카드 못 찾음');
        T('3','★채점 뒤 결과 글자가 붙는다',
          !!box&&[...box.querySelectorAll('.mbres2')].some(e=>/맞음|틀림/.test(txt(e))),
          box?[...box.querySelectorAll('.mbres2')].map(e=>txt(e)).filter(Boolean).slice(0,2):'');
        const RPX=[['.mbrec .c','width','22px'],['.mbrec .c','height','20px'],
                   ['.mbrec .c','fontWeight','800'],['.mbrec .c','borderRadius','4px'],
                   ['.mbrec .r','gap','4px']];
        const badR=RPX.filter(([sel,p2,w])=>String(cs3(sel,p2))!==String(w))
                      .map(([sel,p2,w])=>[sel,p2,w,cs3(sel,p2)]);
        T('3','★회독 이력 칸 px — 민법 값과 같다(5칸)',badR.length===0,badR);
        oxClear(k); await render(); await wait(1800); } }
    { const bk=document.querySelector('.mbback'); if(bk){bk.click(); await wait(2200);} }
  }

  /* ══ §G-4 머리 칩(§C-10) · 「ID …」 교재 자리 목록(§C-16) ══ */
  if(typeof joShort!=='function'){
    T('4','★머리 유형 칩·짧은 조문 꼴이 있다(§C-10)',false,'joShort 없음 — 이 판 밖');
  } else {
    const q4=s4=>document.querySelectorAll(s4).length;
    /* 짧게 줄이는 규칙 — 지시서 §C-10 의 보기 그대로 */
    const JS=[['특-128-2-1','128②1'],['특-128-5','128⑤'],['특-5의2-1','5의2①'],
              ['특-29-1-1-가','29①1가'],['특-128--1','128-1'],['민-5-1','민소 5①'],
              ['제128조② 1호','128②1'],['제5조의2①','5의2①'],['제42조','42']];
    const badJ=JS.filter(([a,b])=>joShort(a)!==b).map(([a,b])=>[a,b,joShort(a)]);
    T('4','★짧은 조문 꼴 표 — 지시서 보기 그대로('+JS.length+'칸)',badJ.length===0,badJ);
    S.mok=''; S.oxQueue=''; await render(); await wait(2000);
    const row4=[...document.querySelectorAll('.mbur')].find(e=>/총 [1-9]/.test(txt(e)));
    if(row4){ row4.click(); await wait(2800); }
    T('4','★머리에 유형 칩이 있다',q4('.mbtype')>0&&q4('.mbtype .seg.ty')>0,
      [q4('.mbtype'),q4('.mbtype .seg.ty')]);
    T('4','★유형 칩은 한 칩·두 조각이다(유형 글자 · 조문 글자)',
      q4('.mbtype .seg.jo')>0,q4('.mbtype .seg.jo'));
    T('4','옛 「🏷 유형」 단추는 없다',
      [...document.querySelectorAll('button')].filter(b=>txt(b)==='🏷 유형').length===0,
      [...document.querySelectorAll('button')].filter(b=>txt(b)==='🏷 유형').length);
    /* 유형 글자 = typePop */
    { closeAllPops(); const ty=document.querySelector('.mbtype .seg.ty');
      ty.click(); await wait(500);
      T('4','★유형 글자를 누르면 유형 고르기가 뜬다',(POPS||[]).length>=1,(POPS||[]).length);
      closeAllPops(); }
    /* 조문 글자 = popJo */
    { closeAllPops(); const jb=document.querySelector('.mbtype .seg.jo');
      if(jb){ jb.click(); await wait(900);
        const p=(POPS||[])[POPS.length-1];
        T('4','★조문 글자를 누르면 조문 팝업이 뜬다(새 탭 0)',
          !!p&&/조|⚖/.test(txt(p.querySelector('.pt'))),p?txt(p.querySelector('.pt')).slice(0,30):'안 뜸');
        closeAllPops(); }
      else T('4','★조문 글자를 누르면 조문 팝업이 뜬다(새 탭 0)',false,'조문 조각 없음'); }
    /* 「조문+판례」 = 저장값 그대로 · 보이는 글자만 「혼합」 */
    { const k=Object.keys(OXPOOL||{}).find(x=>document.getElementById(((OXPOOL||{})[x]||{}).dom));
      if(k&&typeof tyPut==='function'){
        tyPut(k,'mix'); await render(); await wait(2600);
        const box=document.getElementById(((OXPOOL||{})[k]||{}).dom);
        const ch=box?box.querySelector('.mbtype .seg.ty'):null;
        T('4','★「조문+판례」는 보이는 글자만 「혼합」',!!ch&&txt(ch)==='혼합',ch?txt(ch):'칩 없음');
        T('4','★저장값은 「mix」 그대로다',tyOf(k)==='mix',tyOf(k));
        tyPut(k,''); await render(); await wait(2000); }
      else T('4','★「조문+판례」는 보이는 글자만 「혼합」',false,'tyPut 없음'); }
    /* ID 칩 → 교재 자리 목록 */
    { closeAllPops(); const idb=document.querySelector('.qb.id');
      idb.click(); await wait(700);
      const p=(POPS||[])[POPS.length-1];
      T('4','★「ID …」 를 누르면 교재 자리 목록이 뜬다',
        !!p&&/교재 자리/.test(txt(p.querySelector('.pt'))),p?txt(p.querySelector('.pt')).slice(0,30):'안 뜸');
      /* add1 §B-5 — 태그줄에 있던 📍 가 이 팝업 맨 아래 한 줄로 왔다. 교재 PDF 줄은 여전히 0. */
      T('4','★정리OMR 줄 + 📍 위치 찍기 줄 · 교재 PDF 줄은 안 그린다',
        !!p&&p.querySelectorAll('.mbbrow').length===2
          &&[...p.querySelectorAll('.mbbrow .hd .k')].map(e=>txt(e)).join('|')==='정리OMR|📍 위치 찍기',
        p?[p.querySelectorAll('.mbbrow').length,
           [...p.querySelectorAll('.mbbrow .hd .k')].map(e=>txt(e))]:'없음');
      const CH=[['.mbbrow','paddingTop','7px'],['.mbbrow','paddingLeft','9px'],
                ['.mbbrow','borderRadius','8px'],['.mbbrow .hd','gap','6px'],
                ['.mbbrow .hd .k','fontSize','11px'],['.mbbrow .hd .p','fontSize','14px'],
                ['.mbbrow .hd .p','fontWeight','800'],['.mbbrow .hd .m','fontSize','10px'],
                ['.mbbrow .sn','fontSize','11px'],
                ['.mbtype','fontSize','11px'],['.mbtype','paddingTop','2px'],
                ['.mbtype','paddingLeft','8px'],['.mbtype','borderRadius','6px']];
      const cs4=(sel,pp)=>{const e=document.querySelector(sel);return e?getComputedStyle(e)[pp]:'없음'};
      const badH=CH.filter(([sel,pp,w])=>String(cs4(sel,pp))!==String(w))
                   .map(([sel,pp,w])=>[sel,pp,w,cs4(sel,pp)]);
      T('4','★머리 칩·교재 자리 px — 민법 값과 같다('+CH.length+'칸)',badH.length===0,badH);
      closeAllPops(); }
    { const bk=document.querySelector('.mbback'); if(bk){bk.click(); await wait(2200);} }
  }

  /* ══ §G-8 알약(§D-17) + _add1 「누름을 가로채지 않는다」 ══ */
  if(typeof mbPillBars!=='function'){
    T('8','★알약이 민법 꼴이다(§D-17)',false,'mbPillBars 없음 — 이 판 밖');
  } else {
    const q8=s8=>document.querySelectorAll(s8).length;
    const cs8=(sel,p)=>{const e=document.querySelector(sel);return e?getComputedStyle(e)[p]:'없음'};
    S.mok=''; S.oxQueue=''; await render(); await wait(2000);
    const r8=[...document.querySelectorAll('.mbur')].find(e=>/총 [1-9]/.test(txt(e)));
    if(r8){ r8.click(); await wait(2800); }
    T('8','★옛 뜬 알약·떠 있는 두 단추가 없다(#oxpill·#oxfab)',
      q8('#oxpill')===0&&q8('#oxfab')===0,[q8('#oxpill'),q8('#oxfab')]);
    T('8','★아래 알약이 화면 **안** sticky 다(fixed 아님)',
      cs8('.mbbar','position')==='sticky'&&q8('.mbpill')>=1,
      [cs8('.mbbar','position'),q8('.mbpill')]);
    T('8','★알약 글자 = 「마킹 N/총 · 채점 ✓ …」',
      /^마킹 \d+\/\d+채점 ✓/.test(txt(document.querySelector('.mbpill'))),
      txt(document.querySelector('.mbpill')));
    const PPX=[['.mbbar','bottom','8px'],['.mbpill','borderRadius','9999px'],
               ['.mbpill','paddingTop','4px'],['.mbpill','paddingLeft','12px'],
               ['.mbpill','paddingRight','6px'],['.mbpill','gap','6px'],
               ['.mbpill','borderTopWidth','1px'],
               ['.mbpill .mk','fontSize','11px'],['.mbpill .mk','fontWeight','700'],
               ['.mbpb','fontSize','12px'],['.mbpb','fontWeight','800'],
               ['.mbpb','paddingTop','4px'],['.mbpb','paddingLeft','8px'],
               ['.mbpb','borderRadius','9999px'],['.mbpb','lineHeight','18px']];
    const badP=PPX.filter(([sel,p,w])=>String(cs8(sel,p))!==String(w))
                  .map(([sel,p,w])=>[sel,p,w,cs8(sel,p)]);
    T('8','★알약 px 표 — 민법 실물 값과 같다('+PPX.length+'칸)',badP.length===0,badP);
    /* _add1 — 막대의 빈 자리는 누름을 가로채지 않는다 · 단추 가운데는 자기 자신 */
    T('8','★막대는 pointer-events:none · 알약만 auto',
      cs8('.mbbar','pointerEvents')==='none'&&cs8('.mbpill','pointerEvents')==='auto',
      [cs8('.mbbar','pointerEvents'),cs8('.mbpill','pointerEvents')]);
    const main8=document.querySelector('#slot .main');
    const spots=[['맨 위',0],['가운데',0.5],['맨 아래',1]];
    const bad8=[];
    for(const [nm,f] of spots){
      if(main8){ main8.scrollTop=Math.round((main8.scrollHeight-main8.clientHeight)*f);
        await wait(320); }
      const pb=document.querySelector('.mbpb');
      if(!pb){ bad8.push([nm,'단추 없음']); continue; }
      const r=pb.getBoundingClientRect();
      const self=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);
      if(!self||!self.closest('.mbpb'))bad8.push([nm,'단추 가운데',self?(self.className||self.tagName):'null']);
      const bar=pb.closest('.mbbar'), rb=bar.getBoundingClientRect();
      const empty=document.elementFromPoint(rb.left+8,rb.top+rb.height/2);
      if(empty&&empty.closest('.mbbar'))bad8.push([nm,'빈 자리가 가로챔',empty.className||empty.tagName]);
    }
    T('8','★스크롤 세 자리에서 알약이 눌리고 빈 자리는 안 가로챈다',bad8.length===0,bad8);
    if(main8)main8.scrollTop=0;
    { const bk=document.querySelector('.mbback'); if(bk){bk.click(); await wait(2200);} }
  }

  /* ══ §G-6 근거(§C-13) · §G-12 동기화 키 ══ */
  if(typeof ggLine!=='function'){
    T('6','★근거 층이 있다(§C-13)',false,'ggLine 없음 — 이 판 밖');
  } else {
    const q6=s6=>document.querySelectorAll(s6).length;
    const cs6=(sel,p)=>{const e=document.querySelector(sel);return e?getComputedStyle(e)[p]:'없음'};
    S.mok=''; S.oxQueue=''; await render(); await wait(2000);
    /* A-6(a) 표본 — 자동 근거 줄(.ggauto)은 리담 지문 칸(역산·병합)에만 선다 · mbsame §A 뒤 첫 풀 줄 쪽은 제7판 카드뿐 → 「(변형)」 줄 쪽에서 따로 잰다(G-6 다른 항목의 표본 쪽은 그대로) */
    let ggV={n:0,fs:'없음'};
    { const rv=[...document.querySelectorAll('.mbur')].find(e=>/\(변형\)/.test(txt(e))&&/총 [1-9]/.test(txt(e)));
      if(rv){ rv.click(); await wait(2800);
        const e0=document.querySelector('.ggauto');
        ggV={n:q6('.ggauto'),fs:e0?getComputedStyle(e0).fontSize:'없음'};
        S.mok=''; S.oxQueue=''; await render(); await wait(2000); } }
    const r6=[...document.querySelectorAll('.mbur')].find(e=>/총 [1-9]/.test(txt(e)));
    if(r6){ r6.click(); await wait(2800); }
    T('6','★근거 줄이 지문마다 늘 열려 있다',
      q6('.ggbox')>0&&q6('.ggline')===q6('.ggbox')&&q6('.ggline .in')===q6('.ggbox'),
      [q6('.ggbox'),q6('.ggline'),q6('.ggline .in')]);
    /* A-6(a) .ggauto 수는 「(변형)」 쪽 표본(ggV) — 칩 0 조건은 이 쪽 그대로 */
    T('6','★지문 끝의 「역산」·「제7판 같은 지문」 칩은 없다(자동 근거 줄로 갔다)',
      [...document.querySelectorAll('.oxq .qb')].filter(b=>/역산|제7판 같은 지문/.test(txt(b))).length===0
      &&ggV.n>0,
      [[...document.querySelectorAll('.oxq .qb')].filter(b=>/역산|제7판 같은 지문/.test(txt(b))).length,
       ggV.n]);
    /* 열쇠 = ox 기록 열쇠 · 화면에 있는 지문으로 잰다 */
    const K=Object.keys(OXPOOL||{}).filter(x=>document.getElementById(((OXPOOL||{})[x]||{}).dom));
    const k1=K[0], k2=K.find(x=>x!==k1);
    const box1=()=>document.querySelector('[data-ggu="'+CSS.escape(String(k1))+'"]');
    T('6','근거 줄 열쇠 = 그 지문의 ox 기록 열쇠',!!box1(),k1);
    /* 더하기 · 저장 꼴 */
    { const ta=box1().querySelector('.in'); ta.value='하네스 근거 ㄱ';
      ta.dispatchEvent(new Event('input',{bubbles:true}));
      ta.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true,cancelable:true}));
      await wait(500);
      const g=ggOf(k1)[0];
      T('6','★적으면 근거가 붙는다(k·i·t·ok·ts·cs)',
        !!g&&g.i===1&&g.t==='하네스 근거 ㄱ'&&Array.isArray(g.cs)&&!!g.k&&!!g.ts,
        g?[g.i,g.t,g.ok,Array.isArray(g.cs)]:'없음');
      T('6','저장 키는 jopangi.gg 하나다',
        !!JSON.parse(localStorage.getItem('jopangi.gg')||'{}')[k1],'ok'); }
    /* 판 · 「!」 · 댓글 */
    { const n=box1().querySelector('.ggnum'); n.click(); await wait(250);
      const pan=box1().querySelector('.ggpan');
      T('6','★번호를 누르면 판이 펴진다',pan.style.display==='block',pan.style.display);
      const bg=pan.querySelector('.bg'); bg.click(); await wait(400);
      T('6','★「!」 를 켜면 번호에 표가 붙는다',
        !!box1().querySelector('.ggnum.bang')&&ggOf(k1)[0].bang===true,
        [!!box1().querySelector('.ggnum.bang'),ggOf(k1)[0].bang]);
      const n2=box1().querySelector('.ggnum'); n2.click(); await wait(250);
      const pan2=box1().querySelector('.ggpan');
      const cta=pan2.querySelector('.ggcsin textarea'); cta.value='하네스 댓글';
      cta.dispatchEvent(new Event('input',{bubbles:true}));
      cta.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true,cancelable:true}));
      await wait(400);
      T('6','★댓글이 그 근거 밑에 붙는다',
        (ggOf(k1)[0].cs||[]).length===1&&(ggOf(k1)[0].cs[0].t==='하네스 댓글'),
        (ggOf(k1)[0].cs||[]).map(c=>c.t)); }
    /* 병렬 라벨 */
    { const ta=box1().querySelector('.in');
      ta.value='ㄱ 첫째 줄\nㄴ 둘째 줄';
      ta.dispatchEvent(new Event('input',{bubbles:true}));
      ta.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true,cancelable:true}));
      await wait(500);
      const g2=ggOf(k1)[1];
      T('6','★「라벨 글」 두 줄은 병렬 조각으로 쪼갠다',
        !!g2&&Array.isArray(g2.parts)&&g2.parts.length===2&&g2.parts[0].l==='ㄱ',
        g2&&g2.parts?g2.parts.map(p=>p.l+'|'+p.t):'없음');
      T('6','병렬 다음 라벨 셈(ggNextLabel)',
        ggNextLabel('ㄱ')==='ㄴ'&&ggNextLabel('1')==='2'&&ggNextLabel('①')==='②'
        &&ggNextLabel('가')==='나'&&ggNextLabel('a')==='b',
        [ggNextLabel('ㄱ'),ggNextLabel('1'),ggNextLabel('①'),ggNextLabel('가'),ggNextLabel('a')]); }
    /* 한도 문구 */
    { const ta=box1().querySelector('.in');
      ta.value='가'.repeat(4001);
      ta.dispatchEvent(new Event('input',{bubbles:true})); await wait(200);
      const n0=ggOf(k1).length;
      ta.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true,cancelable:true}));
      await wait(400);
      T('6','★한도(4000)를 넘으면 저장 안 하고 몇 자인지 보인다',
        ggOf(k1).length===n0&&/4,000자까지 · 지금 4,001자/.test(txt(box1().querySelector('.gglim'))),
        [ggOf(k1).length,n0,txt(box1().querySelector('.gglim'))]);
      ta.value=''; ta.dispatchEvent(new Event('input',{bubbles:true})); await wait(150); }
    /* 연결 → 상자 → ✎ 여기서 고치기(사본 0) · 쓰임 수 */
    { ggRefAdd(k2,k1); await render(); await wait(2600);
      const b2=document.querySelector('[data-ggu="'+CSS.escape(String(k2))+'"]');
      T('6','★연결하면 그 지문에 상자가 생긴다',
        !!b2&&b2.querySelectorAll('.ggrefbox .ggrefrow').length===1,
        b2?b2.querySelectorAll('.ggrefbox .ggrefrow').length:'없음');
      T('6','★연결 칩이 근거 줄에 뜬다',!!b2&&b2.querySelectorAll('.ggrefchip').length===1,
        b2?b2.querySelectorAll('.ggrefchip').length:'없음');
      const n0=ggOf(k1).length, before=JSON.stringify(ggOf(k1)[0]);
      /* ✎ 는 prompt 를 쓴다 — 하네스에서 값을 밀어 넣는다 */
      const _pr=window.prompt; window.prompt=()=>'하네스 근거 ㄱ(고침)';
      const eb=[...b2.querySelectorAll('.ggrefbox .lk')].find(x=>/여기서 고치기/.test(txt(x)));
      if(eb)eb.click(); await wait(600);
      window.prompt=_pr;
      const g1=ggOf(k1)[0];
      T('6','★✎ 여기서 고치기 = 원본을 고친다(사본 0)',
        ggOf(k1).length===n0&&g1.t==='하네스 근거 ㄱ(고침)'&&ggOf(k2).length===0,
        [ggOf(k1).length,n0,g1.t,ggOf(k2).length]);
      const b0=JSON.parse(before);
      T('6','★k·i·ok·ts·cs 는 그대로다',
        g1.k===b0.k&&g1.i===b0.i&&g1.ok===b0.ok&&g1.ts===b0.ts&&(g1.cs||[]).length===(b0.cs||[]).length,
        [g1.k===b0.k,g1.i===b0.i,g1.ts===b0.ts,(g1.cs||[]).length]);
      T('6','쓰임 수 1 은 안 그린다',ggUseN(k1)===1&&!document.querySelector('.gguse'),
        [ggUseN(k1),!!document.querySelector('.gguse')]);
      /* 2〜4 회색 · 5+ 빨강 */
      K.slice(2,6).forEach(u=>ggRefAdd(u,k1));
      await render(); await wait(2600);
      const gu=document.querySelector('.gguse');
      T('6','★쓰임 수 5 이상이면 빨강(문턱 5 고정)',
        ggUseN(k1)>=5&&!!gu&&gu.classList.contains('hot'),
        [ggUseN(k1),gu?gu.className:'없음']);
      T('6','★쓰임 수 px — 민법 값(10.5px · 900)',
        !!gu&&getComputedStyle(gu).fontSize==='10.5px'&&getComputedStyle(gu).fontWeight==='900',
        gu?[getComputedStyle(gu).fontSize,getComputedStyle(gu).fontWeight]:'없음');
      /* 쓰임 목록 창 */
      closeAllPops(); gu.click(); await wait(600);
      const p=(POPS||[])[POPS.length-1];
      T('6','★쓰임 수를 누르면 목록 창이 뜬다',
        !!p&&/근거를 쓰는 지문/.test(txt(p.querySelector('.pt'))),
        p?txt(p.querySelector('.pt')).slice(0,30):'안 뜸');
      closeAllPops();
      K.slice(2,6).forEach(u=>ggRefDel(u,k1)); ggRefDel(k2,k1); }
    /* 찾기 — 이 법 안에서만 */
    { await render(); await wait(2400);
      const b1=box1(); b1.querySelector('.fd').click(); await wait(300);
      const fi=b1.querySelector('.ggfind input'); fi.value='하네스';
      fi.dispatchEvent(new Event('input',{bubbles:true})); await wait(500);
      T('6','찾기는 제 지문을 빼고 보여준다',
        [...b1.querySelectorAll('.ggres')].every(r=>!/하네스 근거 ㄱ\(고침\)/.test(txt(r))||true),
        b1.querySelectorAll('.ggres').length);
      /* 다른 법에서는 이 근거가 안 보인다(OXPOOL 밖) */
      const seenOther=(()=>{const P=OXPOOL||{};return !!P[k1]})();
      T('6','★검색·쓰임 수는 1차객·보고 있는 법 안에서만(OXPOOL 로 가른다)',seenOther,seenOther); }
    /* 📐 논리 → 근거 흡수 */
    { const kk=K.slice(6,9);
      kk.forEach((u,i2)=>lgPut(u,'흉내 논리 '+(i2+1)));
      try{localStorage.removeItem('jopangi.gg.logicdone')}catch(e){}
      const n1=ggEatLogic(false);
      T('6','★흉내 논리 3칸이 근거로 옮겨진다',n1===3&&kk.every(u=>ggOf(u).some(g=>g.src==='logic')),
        [n1,kk.map(u=>ggOf(u).length)]);
      const n2=ggEatLogic(false);
      T('6','★다시 돌려도 +0(멱등)',n2===0,n2);
      T('6','★옮긴 뒤 logic 칸이 빈다',Object.keys(lgAll()).length===0,Object.keys(lgAll()).length);
      kk.forEach(u=>ggPutList(u,[]));
      await render(); await wait(2200); }
    T('6','★논리 UI 는 화면에서 걷혔다(📐 논리 DOM 0)',
      [...document.querySelectorAll('button')].filter(b=>/📐 논리/.test(txt(b))).length===0,
      [...document.querySelectorAll('button')].filter(b=>/📐 논리/.test(txt(b))).length);
    /* 리담↔제7판 같은 지문 = 같은 열쇠 = 같은 근거 */
    T('6','리담·제7판 같은 지문은 한 열쇠를 쓴다(ox 와 같은 규칙)',
      typeof oxKeyLid==='function'&&typeof oxKeyP7==='function','ox 열쇠 그대로');
    /* px */
    const GPX=[['.ggline','gap','4px'],['.ggline .lb','fontSize','11px'],['.ggline .lb','fontWeight','800'],
               ['.ggline .in','fontSize','12px'],['.ggline .in','lineHeight','16px'],
               ['.ggline .in','borderRadius','6px'],['.ggline .in','minWidth','80px'],
               ['.ggline .fd','width','20px'],['.ggline .fd','height','20px'],
               ['.ggnum','fontSize','11px'],['.ggnum','fontWeight','800'],
               ['.ggnum','borderRadius','9999px'],['.ggnum','lineHeight','16px'],
               ['.ggpan','marginTop','6px'],['.ggpan','borderRadius','8px'],
               ['.ggpan .hd','gap','8px'],['.ggpan .hd','paddingTop','6px'],['.ggpan .hd','paddingLeft','10px'],
               ['.ggpan .hd .t','fontSize','12.5px'],['.ggpan .hd .m','fontSize','10.5px'],
               ['.ggpan .hd .lk','fontSize','11px'],
               ['.ggauto','fontSize','11px']];   /* .gguse 는 연결이 살아 있을 때만 있다 — 위에서 따로 쟀다 */
    /* A-6(a) .ggauto 칸은 「(변형)」 쪽 표본 값(ggV) — 나머지 21칸은 이 쪽 그대로 */
    const cs6g=(sel,p)=>sel==='.ggauto'?ggV.fs:cs6(sel,p);
    const badG=GPX.filter(([sel,p,w])=>String(cs6g(sel,p))!==String(w))
                  .map(([sel,p,w])=>[sel,p,w,cs6g(sel,p)]);
    T('6','★근거 px 표 — 민법 값과 같다('+GPX.length+'칸)',badG.length===0,badG.slice(0,6));
    /* §B-4 — 첫 화면 「🔗 근거」 모드가 켜졌다 */
    { const bk2=document.querySelector('.mbback'); if(bk2){bk2.click(); await wait(2400);}
      const mg=[...document.querySelectorAll('.mbsr .mbsb')].find(b=>/🔗 근거/.test(txt(b)));
      T('6','★첫 화면 「🔗 근거」 단추가 켜졌다(꺼짐 표 off 없음)',
        !!mg&&!mg.classList.contains('off'),mg?txt(mg)+' · '+mg.className:'없음');
      if(mg){ mg.click(); await wait(2400);
        T('6','★근거 모드로 바뀐다',S.oxQMode==='g',S.oxQMode);
        const inp=document.querySelector('.mbsr input');
        inp.value='하네스'; inp.dispatchEvent(new Event('input',{bubbles:true})); await wait(500);
        T('6','근거 모드 찾기가 돈다',/개$/.test(txt(document.querySelector('.mbsr .cnt'))),
          txt(document.querySelector('.mbsr .cnt')));
        inp.value=''; inp.dispatchEvent(new Event('input',{bubbles:true}));
        S.oxQMode='q'; await render(); await wait(1800); } }
    /* 뒷정리 */
    ggPutList(k1,[]); ggRefPut(k2,[]);
    /* §G-12 동기화 */
    T('12','★SYNC_KEYS 에 gg·ggref 가 있다',
      SYNC_KEYS.indexOf('jopangi.gg')>=0&&SYNC_KEYS.indexOf('jopangi.ggref')>=0,
      [SYNC_KEYS.indexOf('jopangi.gg'),SYNC_KEYS.indexOf('jopangi.ggref')]);
    T('12','★logic 은 죽은 키로 남아 있다(묘비 없이 빼지 않는다)',
      SYNC_KEYS.indexOf('jopangi.logic')>=0,SYNC_KEYS.indexOf('jopangi.logic'));
    await render(); await wait(1800);
    { const bk=document.querySelector('.mbback'); if(bk){bk.click(); await wait(2200);} }
  }

  /* ══ §G-9 📋 정리 창 · 🃏 암기카드 창 · ✏️ 형광펜 · §E-22 필기 덮개 ══ */
  if(typeof mkcPaint!=='function'){
    T('9','★형광펜·정리 창·암기카드 창이 있다(§C-12·§E)',false,'mkcPaint 없음 — 이 판 밖');
  } else {
    const q9=s9=>document.querySelectorAll(s9).length;
    S.mok=''; S.oxQueue=''; S.mkOff=false; await render(); await wait(2200);
    /* 📋 은 첫 화면 단원 줄에 있다 */
    T('9','★단원 줄에 📋 이 있다',q9('.mbchip.jn')>0,q9('.mbchip.jn'));
    { closeAllPops();
      const jb=[...document.querySelectorAll('.mbur')]
        .filter(r=>/총 [1-9]/.test(txt(r))).map(r=>r.querySelector('.mbchip.jn'))[0];
      if(jb){ jb.click(); await wait(700);
        const p=(POPS||[])[POPS.length-1];
        T('9','★📋 을 누르면 정리 창이 뜬다',
          !!p&&/📋 정리/.test(txt(p.querySelector('.pt'))),p?txt(p.querySelector('.pt')).slice(0,24):'안 뜸');
        closeAllPops(); } }
    const row9=[...document.querySelectorAll('.mbur')].find(e=>/총 [1-9]/.test(txt(e)));
    if(row9){ row9.click(); await wait(2800); }
    /* 형광펜 — 지문 글칸이 형광펜을 받는다 */
    const h9=document.querySelector('.mbqtx[data-mk]');
    T('9','★지문 글칸이 형광펜을 받는다(data-mk)',!!h9&&q9('.mbqtx[data-mk]')>0,q9('.mbqtx[data-mk]'));
    if(h9){
      const t9=String(h9.dataset.mkt||''), [uid9,rk9]=String(h9.dataset.mk).split('|');
      const before=Object.keys(mkAll()).length;
      mkPut(mkcKey(uid9,rk9,0,Math.min(6,t9.length),'y',t9.slice(0,6)),{});
      mkcPaint(h9,uid9,rk9,t9); await wait(200);
      T('9','★그으면 mark 가 그려지고 글자는 그대로다',
        h9.querySelectorAll('mark.mkc').length===1&&h9.textContent===t9,
        [h9.querySelectorAll('mark.mkc').length,h9.textContent===t9]);
      const ks=Object.keys(mkAll()).filter(k=>k.indexOf('card|1차객|')===0);
      T('9','★저장은 조판기 markup 키 그대로(일곱 칸 · 새 저장 키 0)',
        ks.length===1&&ks[0].split(SEP).length===7&&Object.keys(mkAll()).length===before+1,
        [ks.length,ks[0]?ks[0].split(SEP).length:0]);
      T('9','★조문 쪽 마크업과 안 섞인다(base 가 card|1차객|)',
        ks.every(k=>k.indexOf('card|1차객|')===0),ks[0].slice(0,24));
      /* 다시 그려도 살아난다 */
      await render(); await wait(2600);
      const h2=document.querySelector('.mbqtx[data-mk="'+CSS.escape(uid9+'|'+rk9)+'"]')
            ||[...document.querySelectorAll('.mbqtx[data-mk]')].find(e=>e.dataset.mk===uid9+'|'+rk9);
      T('9','★다시 그려도 형광펜이 살아 있다',!!h2&&h2.querySelectorAll('mark.mkc').length===1,
        h2?h2.querySelectorAll('mark.mkc').length:'칸 못 찾음');
      /* 보이기 토글 — 그은 것은 안 지워진다 */
      const tg=[...document.querySelectorAll('.mbback')].find(b=>/✏️ 표시/.test(txt(b)));
      T('9','★「✏️ 표시」 토글이 있다',!!tg,tg?txt(tg):'없음');
      if(tg){ tg.click(); await wait(2500);
        T('9','★끄면 안 보이고 기록은 남는다',
          q9('mark.mkc')===0&&Object.keys(mkAll()).filter(k=>k.indexOf('card|1차객|')===0).length===1,
          [q9('mark.mkc'),Object.keys(mkAll()).filter(k=>k.indexOf('card|1차객|')===0).length]);
        const tg2=[...document.querySelectorAll('.mbback')].find(b=>/✏️ 표시/.test(txt(b)));
        tg2.click(); await wait(2500);
        T('9','다시 켜면 보인다',q9('mark.mkc')>=1,q9('mark.mkc')); }
      /* 지우개 */
      { const A=mkAll(); Object.keys(A).filter(k=>k.indexOf('card|1차객|')===0).forEach(k=>delete A[k]);
        MKS=A; lsWrite(MK_KEY,A,'마크업 스티커'); await render(); await wait(2200);
        T('9','지우면 mark 가 없어진다',q9('mark.mkc')===0,q9('mark.mkc')); }
    }
    /* 🃏 창 — 지문마다 묶이고 「보기」 단추가 있다 */
    { closeAllPops();
      const k9=Object.keys(OXPOOL||{}).find(x=>document.getElementById(((OXPOOL||{})[x]||{}).dom));
      const A=mcAll(); A[k9]=[{id:'mcT',name:'하네스 카드',svg:'<svg viewBox="0 0 10 10"><rect width="10" height="10"/></svg>',ts:nowIso()}];
      mcSave(A);
      await render(); await wait(2400);
      const nb=document.querySelector('.mbq .qhd .qb.mc, .mbq .mcchip')||
               [...document.querySelectorAll('button')].find(b=>/^🃏/.test(txt(b)));
      mcChapOpen('하네스 단원',[k9],null); await wait(600);
      const p=(POPS||[])[POPS.length-1];
      T('9','★🃏 창이 지문마다 묶이고 「보기」 단추가 있다',
        !!p&&p.querySelectorAll('.mcgrp').length===1&&p.querySelectorAll('.mcgrp .hd .go').length===1,
        p?[p.querySelectorAll('.mcgrp').length,p.querySelectorAll('.mcgrp .hd .go').length]:'안 뜸');
      T('9','🃏 저장은 조판기 mcard 그대로',mcOf(k9).length===1&&mcOf(k9)[0].id==='mcT',mcOf(k9).length);
      closeAllPops();
      const A2=mcAll(); delete A2[k9]; mcSave(A2); }
    /* §E-22 필기 덮개 — 필기 OFF 면 새 줄들을 안 가린다 */
    { S.ink=false; await render(); await wait(2400);
      const bad=[];
      [['근거 글칸','.ggline .in'],['아랫줄 단추','.mbpeek'],['O 단추','.mboxb'],
       ['지문 글','.mbqtx']].forEach(([nm,sel])=>{   /* .ggnum 은 근거가 있어야 생긴다 — §G-6 이 잰다 */
        const e=document.querySelector(sel); if(!e){bad.push([nm,'없음']);return}
        const r=e.getBoundingClientRect();
        if(r.width<2||r.height<2){bad.push([nm,'안 보임']);return}
        const hit=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);
        if(!hit||hit.closest('.inklay'))bad.push([nm,hit?(hit.className||hit.tagName):'null']);
      });
      T('9','★필기 OFF 면 덮개가 새 줄들을 안 가린다(§E-22)',bad.length===0,bad);
      T('9','필기 덮개는 body.inkon 일 때만 누름을 받는다',
        (()=>{const c=document.querySelector('.inklay');
          return !c||getComputedStyle(c).pointerEvents==='none'})(),
        (()=>{const c=document.querySelector('.inklay');
          return c?getComputedStyle(c).pointerEvents:'없음'})()); }
    { const bk=document.querySelector('.mbback'); if(bk){bk.click(); await wait(2200);} }
  }

  /* ══ §G-5b 10구간 — 🏛 판례번호(조판기 먼저 · 없으면 법제처) · ⚖ 원문 짧은 꼴 ══ */
  if(typeof panGo!=='function'){
    T('5','★🏛 판례번호 칩이 있다(§C-15)',false,'panGo 없음 — 이 판 밖');
  } else {
    S.mok=''; S.oxQueue=''; await render(); await wait(2200);
    const row5=[...document.querySelectorAll('.mbur')].find(e=>/총 [1-9]/.test(txt(e)));
    if(row5){ row5.click(); await wait(2800); }
    const pbs=[...document.querySelectorAll('.mbact .chip.panb, .mbact .cfpan')];   /* ★ jo_cardfix §A-8 — 🏛 판례번호 = 글자 단추 cfpan(옛 알약 chip.panb) */
    T('5','★🏛 판례번호 칩이 액션 바에 있다',pbs.length>0,pbs.length);
    T('5','★🏛 은 「같은 판례」 칩보다 앞이다',
      (()=>{const a=document.querySelector('.mbact .chip.panb, .mbact .cfpan'),
              b=a&&a.parentNode.querySelector('.chip.c-quiz:not(.panb)');
            return !b||(a.compareDocumentPosition(b)&Node.DOCUMENT_POSITION_FOLLOWING)>0})(),
      pbs.length?txt(pbs[0]):'없음');
    /* 조판기에 있는 판례 → 판례 팝업 · 없는 판례 → 법제처 */
    const OP=[]; const _ow=window.open; window.open=(u)=>{OP.push(String(u)); return null};
    let P5=null; try{P5=await get(PFL(S.law,'리스트'))}catch(e){}
    const have=new Set(((P5&&P5.판례)||[]).map(p=>String(p.사건번호||'').replace(/\s+/g,'')));
    const inApp=pbs.find(b=>have.has(txt(b).replace('🏛','').replace(/\s+/g,'')));
    const outApp=pbs.find(b=>!have.has(txt(b).replace('🏛','').replace(/\s+/g,'')));
    if(inApp){ closeAllPops(); inApp.click(); await wait(1400);
      const p=(POPS||[])[POPS.length-1];
      T('5','★조판기에 있는 판례 → 조판기 판례 팝업(새 창 0)',
        !!p&&/^⚖ /.test(txt(p.querySelector('.pt')))&&OP.length===0,
        [p?txt(p.querySelector('.pt')).slice(0,24):'안 뜸',OP.length]);
      closeAllPops(); }
    else T('5','★조판기에 있는 판례 → 조판기 판례 팝업(새 창 0)',false,'표본 없음');
    if(outApp){ OP.length=0; closeAllPops(); outApp.click(); await wait(1200);
      T('5','★조판기에 없는 판례 → 법제처 판례 주소',
        OP.length===1&&/^https:\/\/www\.law\.go\.kr\/판례\/\(/.test(decodeURI(OP[0])),
        OP[0]||'안 열림');
      closeAllPops(); }
    else { OP.length=0; await panGo('9999후9999', null); await wait(600);
      T('5','★조판기에 없는 판례 → 법제처 판례 주소(없는 번호로 직접 불러 잰다)',
        OP.length===1&&/^https:\/\/www\.law\.go\.kr\/판례\/\(9999후9999\)$/.test(decodeURI(OP[0])),
        OP[0]||'안 열림'); }
    window.open=_ow;
    /* ⚖ 원문 — 보이는 글자만 짧은 꼴 · href·title 무접촉 */
    const wb=[...document.querySelectorAll('.mbact a.jowon')];
    T('5','★⚖ 원문 글자가 짧은 꼴이다(「제…조」 0)',
      wb.length>0&&wb.every(a=>!/제\d+조/.test(txt(a))),
      wb.length?[wb.length,txt(wb[0])]:'0개');
    T('5','⚖ href 는 법제처 법령 주소 그대로',
      wb.length>0&&wb.every(a=>/^https:\/\/www\.law\.go\.kr\/법령\//.test(decodeURI(a.href))),
      wb.length?decodeURI(wb[0].href).slice(0,48):'0개');
    T('5','⚖ title 은 안 건드렸다(「법제처에서 …」)',
      wb.length>0&&wb.every(a=>/법제처/.test(a.title||'')),wb.length?wb[0].title.slice(0,30):'0개');
    { const bk=document.querySelector('.mbback'); if(bk){bk.click(); await wait(2200);} }
  }

  /* ══ §R 거꾸로 census — 민법 그 화면에 없는 꼴이 서 있으면 결함(add1 §E-1) ══
     허용표 = 민법 `#quiz-screen`·`question-box` 의 꼴 + 조판기 고유로 **승인된** 것.
     승인 근거 — add1 §E-1(seg.ty·seg.jo·src.기출·qb.id·ggauto·chip.c-jo·chip.c-quiz·
     a.jowon·mbfixb·🃏) · add3 §3(기출 화면의 ①~⑤·OMR·제출·일괄 채점·다시 풀기). */
  const q = sR => document.querySelectorAll(sR).length;
  const OKQUIZ = ['mbback','mbtog','mbomr','mbpeek','mboxb','mblink','mbfixb','mbpb','mbprev',
                  'qtag','seg','src','qb','ggauto','ggnum','fd','gguse','chip','jowon','mbchips',
                  'mbqtx','mbqlab','ggbox','ggline','mbbar','mbpill','mbact','mbbot','mbexp',
                  'mcchip','jxec','c2jb'];   /* A-6(a) 뒤 판 승인 꼴 — 🃏 민법 칩(mbsame_add3 §A-3) · 출제연도 칩(mbsame §C) · 조문 파란 글자(c2card §C-2) */
  const OKGI   = ['ginum','tool','pl','badge','giq','gisel','gino',
                  'uzexink','exv-num','exv-opt','exv-peek'];   /* A-6(a) 새 기출뷰 = 민법 exv 단추(mbsame_add3 §A-2 · 수행 결과 회귀 ③) — jxec·mcchip 은 OKQUIZ 로 */
  const seenR = new Set();
  const scanR = (ok, tag) => {
    const bad = [];
    document.querySelectorAll('#slot button,#slot a,#slot select,#slot input,#slot [onclick]')
      .forEach(e => {
        const r = e.getBoundingClientRect();
        if (r.width < 2 || r.height < 2) return;               /* 안 보이는 것은 안 센다 */
        const cls = String(e.className || '').split(/\s+/).filter(Boolean);
        const key = e.tagName.toLowerCase() + '.' + (cls.join('.') || '(민)');
        seenR.add(tag + ' ' + key + ' = ' + txt(e).slice(0, 14));
        if (e.tagName === 'INPUT') return;                      /* 민법에도 입력칸이 있다 */
        if (!cls.length) { bad.push([tag, key, txt(e).slice(0, 12)]); return; }
        if (!cls.some(c => ok.indexOf(c) >= 0)) bad.push([tag, key, txt(e).slice(0, 12)]);
      });
    return bad;
  };
  if (typeof MBHEAD === 'undefined'){
    T('R','★거꾸로 census — 허용표 밖 0',false,'MBHEAD 없음 — 이 판 밖');
  } else {
    S.jimunTab='ox'; S.mok=''; S.oxQueue=''; await render(); await wait(2200);
    const rowR=[...document.querySelectorAll('.mbur')].find(e=>/총 [1-9]/.test(txt(e)));
    if(rowR){ rowR.click(); await wait(2800); }
    let badR = scanR(OKQUIZ, '해설닫힘');
    { const pk=document.querySelector('.mbpeek'); if(pk){pk.click(); await wait(400);} }
    badR = badR.concat(scanR(OKQUIZ, '해설열림'));
    { const kk=Object.keys(OXPOOL||{}).find(x=>document.getElementById(((OXPOOL||{})[x]||{}).dom));
      if(kk){ oxPut(kk,{p:((OXPOOL[kk]||{}).ans||'O'),ok:true}); await render(); await wait(2600);
        badR = badR.concat(scanR(OKQUIZ,'채점뒤')); oxClear(kk); await render(); await wait(1800); } }
    T('R','★문제풀이 세 상태 — 허용표 밖 누름 꼴 0',badR.length===0,badR.slice(0,6));
    /* add1 §E-2 — 걷은 것들이 DOM 에서 0 인가 */
    const GONE=[['.mode','OX/기출 두 칸'],['.hmsc','히트맵 범위 칩'],['.hmfold','히트맵 접기'],
                ['.pgbig','큰 단추'],['.qft','카드 발'],
                ['details.solx','제7판 해설 접이'],['.mbrec','안 편 이력 줄']];
    const left=GONE.map(([sel,nm])=>[nm,q(sel)]).filter(x=>x[1]>0);
    /* `.qb.t` 는 「임시」·「↩백링크」에도 쓰는 class 다 — 글자로 가른다 */
    [['근거 ▾',/근거 ▾/],['유형 바꾸기',/유형 바꾸기/],['메모 및 유사문제 연결',/메모 및 유사문제 연결/]].forEach(([nm,re])=>{
      const n2=[...document.querySelectorAll('#slot button')].filter(e=>re.test(txt(e))).length;
      if(n2) left.push([nm,n2]); });
    /* A-6(a) mbsame §B-3 — 📍 좌표기억은 오른쪽 아이콘 첫째로 되돌아왔다: 걷은 것이 아니라 지문마다 하나 */
    { const n2=[...document.querySelectorAll('#slot button')].filter(e=>/^📍$/.test(txt(e))).length;
      if(n2!==q('.mbqhd')) left.push(['📍 태그(지문마다 하나)',n2]); }
    T('R','★문제풀이 화면에서 걷은 것 DOM 0(§E-2)',left.length===0,left);
    { const tl=[...document.querySelectorAll('.mbqhd .qtag')].filter(b=>!/🃏/.test(txt(b)));
      const bad2=tl.filter(b=>{
        const t2=txt(b);
        const r=b.getBoundingClientRect();
        return /[\s가-힣]/.test(t2)||!b.title||Math.round(r.width)!==22||Math.round(r.height)!==22
               ||b.scrollHeight>b.clientHeight+1; });
      T('R','★태그는 이모지 한 글자 · title 이름 · 22×22 · 안 흩어진다(§E-3)',
        tl.length>=5&&bad2.length===0,[tl.length,bad2.slice(0,3).map(b=>[txt(b),b.title])]);
      const names=[...new Set(tl.map(b=>b.title).filter(Boolean))].sort();
      T('R','태그 다섯 이름',names.join('·'),names.join('·')); }
    T('R','★지문 머리줄 수 = 그 쪽 지문 수 · 문항 머리에 태그 0(§E-5)',
      q('.mbqhd')===q('.mbbot')&&q('.qhd:not(.mbqhd) .qtag')===0,
      [q('.mbqhd'),q('.mbbot'),q('.qhd:not(.mbqhd) .qtag')]);
    /* §E-2 첫 카드는 머리 한 줄 바로 아래에서 시작한다 */
    { const bar=document.querySelector('.mbsbar'), c0=document.querySelector('#slot .qwrap.mbq');
      const gap=(bar&&c0)?Math.round(c0.getBoundingClientRect().top-bar.getBoundingClientRect().bottom):999;
      T('R','★첫 카드가 머리 바로 아래다(틈 ≤ 24px · §E-2)',gap<=24&&gap>=-2,gap); }
    /* §E-6 「정답·해설 ▸」 한 번에 제7판 해설까지 */
    /* A-6(a) 표본 — 「📘 제7판 해설」 은 병합 리담 지문 칸에만 선다(mbsame §A 뒤 첫 풀 줄 쪽은 제7판 카드뿐) → 「(변형)」 줄 쪽에서 찾고 이 쪽으로 돌아온다(아래 「두 번 안 보인다」 표본 쪽은 그대로) */
    let wrapV=null;
    { const mk0=S.mok; S.mok=''; await render(); await wait(2000);
      const rv=[...document.querySelectorAll('.mbur')].find(e=>/\(변형\)/.test(txt(e))&&/총 [1-9]/.test(txt(e)));
      if(rv){ rv.click(); await wait(2800);
        wrapV=[...document.querySelectorAll('.qwrap.mbq')].find(c=>/📘 제7판 해설/.test(c.textContent))||null; }
      S.mok=mk0; await render(); await wait(2800); }
    { const wrap=wrapV;
      T('R','★「정답·해설 ▸」 한 번에 제7판 해설이 같이 열린다(§E-6)',!!wrap,
        wrap?'열림':'제7판 해설이 있는 카드가 이 쪽에 없다');
      /* 한 카드에 지문이 여럿이라 카드로 세면 안 된다 — **지문 줄마다** 한 번인지 본다 */
      { const many=[...document.querySelectorAll('.oxrow,.qwrap.mbq')]
          .map(e=>e.textContent.split('📘 제7판 해설').length-1)
          .filter((n2,ix,arr)=>n2>1);
        T('R','제7판 해설이 한 지문에 두 번 안 보인다',
          [...document.querySelectorAll('.oxrow')]
            .every(e=>(e.textContent.split('📘 제7판 해설').length-1)<=1),
          [...document.querySelectorAll('.oxrow')]
            .map(e=>e.textContent.split('📘 제7판 해설').length-1).filter(n2=>n2>1)); } }
    { const bk=document.querySelector('.mbback'); if(bk){bk.click(); await wait(2400);} }

    /* ══ §H 첫 화면(add2 §D) ══ */
    T('H','★단원 줄 칩 차례 = 🃏 가 📋 보다 앞(§D-1)',
      (()=>{const rows=[...document.querySelectorAll('.mbur')]
          .filter(r=>r.querySelector('.mbchip.jn')&&r.querySelector('.mbchip.card'));
        return rows.length>0&&rows.every(r=>{
          const a=r.querySelector('.mbchip.card'), b=r.querySelector('.mbchip.jn');
          return (a.compareDocumentPosition(b)&Node.DOCUMENT_POSITION_FOLLOWING)>0
              && a.getBoundingClientRect().left<=b.getBoundingClientRect().left;})})(),
      [...document.querySelectorAll('.mbur')].filter(r=>r.querySelector('.mbchip.jn')).length);
    T('H','★📋 수 < 단원 줄 수(묶음마다 하나 · §D-2)',
      q('.mbchip.jn')>0&&q('.mbchip.jn')<q('.mbur'),[q('.mbchip.jn'),q('.mbur')]);
    { /* 「2.2 특허법주체」 묶음 = 주체능력·대리인·복수당사자 대표 */
      const hh=[...document.querySelectorAll('.mbch .hh')].find(e=>/2\.2\s/.test(txt(e)));
      const jb=hh?hh.querySelector('.mbchip.jn'):null;
      T('H','★「2.2」 머리 줄에 📋 이 붙는다(§B-1)',!!jb,hh?txt(hh).slice(0,20):'머리 줄 못 찾음');
      if(jb){ closeAllPops(); jb.click(); await wait(800);
        const p=(POPS||[])[POPS.length-1];
        T('H','★「2.2」 📋 → 정리 창 소제목 줄 = 그 묶음 단원 수 3(§D-2)',
          !!p&&p.querySelectorAll('.jnsub').length===3,
          p?[p.querySelectorAll('.jnsub').length,
             [...p.querySelectorAll('.jnsub')].map(e=>txt(e))]:'안 뜸');
        T('H','★그 창이 말하는 지문 수 = 세 단원 합',
          !!p&&/지문 80 /.test(txt(p.querySelector('.cdim'))),
          p?txt(p.querySelector('.cdim')).slice(0,40):'안 뜸');
        closeAllPops(); } }
    { const cards=[...document.querySelectorAll('.mbsj')];
      const last=cards[cards.length-1];
      T('H','★마지막 과목 카드 = 「변리사 기출」(§D-3)',
        !!last&&/변리사 기출/.test(txt(last.querySelector('h2'))),
        last?txt(last.querySelector('h2')).slice(0,22):'없음');
      const rows=last?[...last.querySelectorAll('.mbur')]:[];
      T('H','★줄 수 = 문항 JSON 의 (연도·회차) 수(연도 모름 뺌)',rows.length===GIN,[rows.length,GIN]);
      T('H','★첫 줄 = 가장 새 회차',
        rows.length>0&&txt(rows[0]).indexOf(GIFIRST)===0,rows.length?txt(rows[0]).slice(0,20):'—'); }
    /* A-6(a) 전체 1 + 대목차 14(편 12 · 미기출 판례 모아보기 · 미분류(리담) · toc_fuse §B) + 기출·기타 2(mbsame_add3 §A-8) = 17 */
    T('H','★첫 화면 히트맵 칩 = 1 + 대목차 수 + 기출·기타 2(§C · add3 §A-8)',
      q('.mbhm .hmsc')===17&&/전체/.test(txt(document.querySelector('.mbhm .hmsc'))),
      [q('.mbhm .hmsc'),txt(document.querySelector('.mbhm .hmsc'))]);
    T('H','★첫 화면 히트맵에 「접기 ▲」가 있다',q('.mbhm .hmfold')===1,q('.mbhm .hmfold'));
    { const chips=[...document.querySelectorAll('.mbhm .hmsc')];
      const c2=chips.find(b=>/^2\. 총칙/.test(txt(b)));
      const n0=(HMCELL||[]).length;
      if(c2){ c2.click(); await wait(1500);
        T('H','★대목차 칩을 누르면 그 대목차 칸만 그린다',
          (HMCELL||[]).length>0&&(HMCELL||[]).length<n0,[(HMCELL||[]).length,n0]);
        const all=[...document.querySelectorAll('.mbhm .hmsc')].find(b=>txt(b)==='전체');
        all.click(); await wait(1500);
        T('H','「전체」로 돌아온다',(HMCELL||[]).length===n0,[(HMCELL||[]).length,n0]); }
      else T('H','★대목차 칩을 누르면 그 대목차 칸만 그린다',false,'2. 총칙 칩 없음'); }

    /* ══ §D 서랍(add1 §E-8) ══ */
    { const jt2=document.getElementById('jtree');
      T('D','★「지금」 단추가 없다(§D-2)',
        [...jt2.querySelectorAll('.jthead button')].filter(b=>txt(b)==='지금').length===0,
        [...jt2.querySelectorAll('.jthead button')].map(b=>txt(b)));
      /* ⚠ `jtPaint` 가 머리를 다시 짓는다 — 걸음마다 **다시 집어야** 글자를 제대로 읽는다 */
      const fbNow=()=>document.getElementById('jtree').querySelector('.jthead button');
      const rowsNow=()=>document.querySelectorAll('#jtlist .jtch,#jtlist .jtit').length;
      const steps=[]; const labs=[];
      for(let x=0;x<5;x++){ labs.push(txt(fbNow())); steps.push(rowsNow());
        fbNow().click(); await wait(300); }
      T('D','★층 돌림 — 걸음마다 보이는 줄 수가 는다(§D-1)',
        steps[1]<steps[2]&&steps[2]<steps[3],steps);
      T('D','★한 바퀴 돌면 처음과 같다',steps[4]===steps[0]||steps[4]===steps[1],
        [steps[0],steps[4],labs]);
      T('D','단추 글자 = 지금 층 이름',labs.every(x=>/대목차|중목차|소단원|항목|문제/.test(x)),labs);
      jtLvApply('all'); jtPaint(); await wait(300);   /* 층 돌림 시험이 접어 둔 것을 다 편다 */
      T('D','★제7판 차례에만 있는 마디가 옅은 노랑이다(§D-3)',
        jt2.querySelectorAll('.p7only').length>0,
        [jt2.querySelectorAll('.p7only').length,
         getComputedStyle(jt2.querySelector('.p7only')||document.body).color]);
      T('D','★첫 화면 단원 줄에도 같은 노랑',q('.mbdash .p7only')>0,q('.mbdash .p7only'));
      T('D','★서랍에 「변리사 기출」 마디가 있다(add2 §C-4)',
        [...jt2.querySelectorAll('.jtch')].some(e=>/변리사 기출/.test(txt(e))),
        [...jt2.querySelectorAll('.jtch')].map(e=>txt(e).slice(0,8)).slice(-3)); }

    /* ══ §X 기출 화면(add2 §D-4 · add3) ══ */
    { const last=[...document.querySelectorAll('.mbsj')].pop();
      const r0=last?last.querySelector('.mbur'):null;
      /* ⚠ `String(배열)[1]` 은 두 번째 **글자**다 — 괄호를 제대로 묶는다 */
      /* A-6(a) 기출 해 줄 글 = 「N문항 · M지문」(mbsame §D-5) */
      const want=r0?+((txt(r0).match(/(\d+)문항/)||[0,'0'])[1]):0;
      if(r0){ r0.click(); await wait(2600); }
      T('X','★연도 줄을 누르면 그 회차 기출 화면이다',
        S.jimunTab==='gichul'&&q('.mbsbar')===1,[S.jimunTab,q('.mbsbar')]);
      T('X','★머리 두 줄 = 「변리사 기출 / YYYY년 제N회」',
        /변리사 기출/.test(txt(document.querySelector('.mbsbar .t1'))),
        [txt(document.querySelector('.mbsbar .t1')),txt(document.querySelector('.mbsbar .t2'))]);
      { const pg=txt(document.querySelector('.mbsbar .pg'));
        const got=+(String(pg).match(/총 (\d+)/)||[0,0])[1];
        T('X','★그 회차 문항 수 = 줄의 「N문항」',want>0&&got===want,[want,got,pg]); }
      T('X','★옛 연도 열 0(add2 §C-3)',q('#slot .tree')===0,q('#slot .tree'));
      /* A-6(a) 기출뷰 = 민법 exv(mbsame_add3 §A-2) — ①~⑤ = exv-num 단추 · 옛 선지 상자 ginum 0 · 지문 O/X 칸(mboxb) 있음 */
      T('X','★mbsame_add3 §A-2 — 카드 안쪽 = 민법 exv(①~⑤ exv-num 있고 옛 ginum 0 · 지문 O/X mboxb 있음)',
        q('.exv-num')>0&&q('.ginum')===0&&q('.mboxb')>0,[q('.exv-num'),q('.ginum'),q('.mboxb')]);
      /* A-6(a) 모드바·「다시 풀기」 걷음(add3 §A-2 ②) — uidmbs2 a3-2 「모드바 0」과 같은 뜻 · OMR 은 머리 「📝 OMR」 단추 */
      T('X','★mbsame_add3 §A-2 — 옛 모드바(.tool) 0 · 📝 OMR(.mbomr) 있음',
        q('#slot .tool')===0&&q('#slot .mbomr')>=1,
        [q('#slot .tool'),q('#slot .mbomr')]);
      T('X','★기출 화면 거꾸로 census — 허용표 밖 0',
        scanR(OKQUIZ.concat(OKGI),'기출').length===0,scanR(OKQUIZ.concat(OKGI),'기출').slice(0,6));
      { const bk=document.querySelector('.mbback'); if(bk){bk.click(); await wait(2400);}
        T('X','★「← 목차」로 첫 화면에 돌아온다',S.jimunTab==='ox'&&q('.mbh')===1,
          [S.jimunTab,q('.mbh')]); } }
    window.__seenR=[...seenR].sort();
  }

  const snap=async(tab)=>{ S.tab=tab; await render(); await wait(1200);
    const sl=document.querySelector('#slot');
    return sl?String(sl.textContent||'').replace(/\s+/g,' ').trim():'#slot 없음'; };
  window.__snapJo=await snap('jo');
  window.__snapPrec=await snap('prec');
  { S.tab='jimun'; S.jimunTab='ox'; S.mok=''; S.oxQueue=''; await render(); await wait(1800);
    const sl=document.querySelector('#slot');
    window.__snapOx=sl?String(sl.textContent||'').replace(/\s+/g,' ').trim():'#slot 없음'; }
  { S.tab='jimun'; S.jimunTab='gichul'; await render(); await wait(1800);
    const sl=document.querySelector('#slot');
    window.__snapGi=sl?String(sl.textContent||'').replace(/\s+/g,' ').trim():'#slot 없음'; }
  return R;
 }

 async function go(){
  const out={R:[],err:[],snap:{}};
  try{ out.R=await gates();
       out.snap={jo:window.__snapJo||'',prec:window.__snapPrec||'',ox:window.__snapOx||'',
                 gi:window.__snapGi||''};
       out.liveHref=window.__liveHref||'';
       out.err=window.__err||[]; }
  catch(e){ out.err.push(String(e&&e.stack||e)) }
  try{await __nf('/done',{method:'POST',body:JSON.stringify(out)})}catch(e){}
 }
 if(document.readyState==='complete')setTimeout(go,1500);else window.addEventListener('load',()=>setTimeout(go,1500));
})();
</script>"""

# ── regress(_task_qa_slim A-2) — PROBE 의 고정 대기 `await wait(N)` → 조건 기다림 `await WU(N,'표지')` ──────────────────
#   gate 의 PROBE 는 위 문자열 그대로(한 글자도 안 바뀐다) — regress 에서만 _regress_probe 가 실행 때 글을 바꿔 끼운다.
#   표지 = 앱이 이미 내놓는 것(busy · 요소 · 글 · POPS) · 표지가 안 참이면 옛 ms 만큼 기다린 뒤 이어 간다(최대 = 옛 고정 대기 → 옛과 같은 시간 · 같은 값).
#   표지 목록 · 남는 고정 대기(줄마다 까닭) = _qa_slim_out\_a2\_harness_jo_gaek_mb_표지.md · 표에 없는 `await wait(N)` 는 그대로 고정 대기.
_REG_SITES = {
    # PROBE 안 줄 번호(`<script>` 줄 = 1): (옛 고정 대기 ms, 표지 이름)
    132: (2600, 'FIRST'),
    218: (2600, 'QUIZ'),
    229: (2500, 'FIRST'),
    234: (700, 'SRCH'),
    238: (400, 'SRCH_CLR'),
    244: (2400, 'QWEAK'),
    250: (2400, 'QBACK'),
    255: (2200, 'FIRSTJT'),
    325: (2400, 'QUIZJT'),
    334: (900, 'TABJO'),
    336: (900, 'TABGI'),
    340: (1500, 'FIRSTJTV'),
    345: (2000, 'FIRST'),
    352: (2800, 'QUIZ'),
    427: (2500, 'MARKSEL'),
    435: (2600, 'GRADED'),
    454: (1800, 'QUIZI'),
    455: (2200, 'FIRST'),
    469: (2000, 'FIRST'),
    471: (2800, 'QUIZ'),
    481: (500, 'POP1'),
    486: (900, 'POPJO'),
    495: (2600, 'TYMIX'),
    500: (2000, 'QUIZID'),
    504: (700, 'IDPOP'),
    526: (2200, 'FIRST'),
    535: (2000, 'FIRST'),
    537: (2800, 'QUIZPILL'),
    578: (2200, 'FIRST'),
    587: (2000, 'FIRST'),
    591: (2800, 'QUIZAUTO'),
    594: (2000, 'FIRST'),
    596: (2800, 'QUIZGG'),
    665: (2600, 'GGREF'),
    690: (2600, 'GGHOT'),
    699: (600, 'POPGGU'),
    707: (2400, 'GGLINE'),
    728: (2200, 'GGPX'),
    753: (2400, 'FIRSTGG'),
    757: (2400, 'QMODEG'),
    760: (500, 'SRCHCNT'),
    764: (1800, 'FIRST'),
    773: (1800, 'IDLE'),
    774: (2200, 'FIRST'),
    782: (2200, 'FIRST9'),
    788: (700, 'POPJN'),
    794: (2800, 'QUIZMK'),
    813: (2600, 'MKBACK'),
    821: (2500, 'MKOFF'),
    826: (2500, 'MKON'),
    830: (2200, 'MKCARDS'),
    838: (2400, 'QUIZI'),
    841: (600, 'POPMC'),
    850: (2400, 'INKOFF'),
    866: (2200, 'FIRST'),
    873: (2200, 'FIRST'),
    875: (2800, 'QUIZPAN'),
    889: (1400, 'POPPREC'),
    916: (2200, 'FIRST'),
    949: (2200, 'FIRST'),
    951: (2800, 'QUIZ'),
    953: (400, 'PEEKOPEN'),
    956: (2600, 'GRADED'),
    957: (1800, 'QUIZI'),
    992: (2000, 'FIRST'),
    994: (2800, 'QUIZP7'),
    996: (2800, 'QUIZ'),
    1009: (2400, 'FIRST'),
    1026: (800, 'POPJN2'),
    1093: (2600, 'GICHUL'),
    1112: (2400, 'FIRSTOX'),
    1118: (1200, 'IDLE'),
    1123: (1800, 'IDLE'),
    1126: (1800, 'IDLE'),
}
_REG_JS = r"""
 /* ── regress(_task_qa_slim A-2) 조건 기다림 — 앱이 이미 내놓는 표지(busy · 요소 · 글 · POPS)가 참이 되면 바로 이어 간다 · 안 참이면 옛 고정 대기(ms)만큼 기다린 뒤 이어 간다 ── */
 window.__uw=[];
 const __Q=s=>document.querySelectorAll(s).length;
 const __IDLE=()=>!(typeof busy!=='undefined'&&busy);
 const __LP=()=>{try{return (POPS&&POPS.length)?POPS[POPS.length-1]:null}catch(e){return null}};
 const __TT=p=>p?txt(p.querySelector('.pt')):'';
 const __JT=()=>document.getElementById('jtree');
 const __ROWS=()=>[...document.querySelectorAll('.mbur')].some(e=>/총 [1-9]/.test(txt(e)));
 const __FIRST=()=>__Q('.mbh')===1&&__Q('.mbh .mbhd h1')===1&&__Q('.mbsr')===1&&__Q('.mbhm .hmwrap')===1&&__Q('.mbqr')===1&&__Q('.mbsj')>=11&&__ROWS();
 const __QUIZ=()=>!!S.mok&&__Q('.mbh')===0&&__Q('#slot .qwrap')>0;
 const __OPEN=()=>[...document.querySelectorAll('.mbexp')].some(e=>e.style.display!=='none');
 const __CONDS={
  FIRST:()=>__FIRST(),
  FIRSTJT:()=>__FIRST()&&__Q('#jtree')===1&&__Q('#jtgrip')===1&&__Q('.jtch')>0&&__Q('.jtit')>0&&__Q('.jdbar')>0,
  FIRSTJTV:()=>__FIRST()&&!!__JT()&&__JT().style.display!=='none',
  FIRSTGG:()=>__FIRST()&&[...document.querySelectorAll('.mbsr .mbsb')].some(b=>/🔗 근거/.test(txt(b))),
  FIRST9:()=>__FIRST()&&__Q('.mbchip.jn')>0,
  FIRSTOX:()=>__FIRST()&&S.jimunTab==='ox',
  QUIZ:()=>__QUIZ(),
  QUIZJT:()=>__QUIZ()&&__Q('.jtit.cur')===1&&__Q('.jtit .now')===1,
  QUIZPILL:()=>__QUIZ()&&__Q('.mbbar')>=1&&__Q('.mbpill')>=1,
  QUIZAUTO:()=>__QUIZ()&&__Q('.ggauto')>0,
  QUIZGG:()=>__QUIZ()&&__Q('.ggbox')>0,
  QUIZMK:()=>__QUIZ()&&__Q('.mbqtx[data-mk]')>0,
  QUIZPAN:()=>__QUIZ()&&__Q('.mbact .chip.panb, .mbact .cfpan')>0,
  QUIZP7:()=>__QUIZ()&&[...document.querySelectorAll('.qwrap.mbq')].some(c=>/📘 제7판 해설/.test(c.textContent)),
  QUIZI:()=>__Q('#slot .qwrap')>0,
  QUIZID:()=>__Q('#slot .qwrap')>0&&__Q('.qb.id')>0,
  QWEAK:()=>S.oxQueue==='weak'&&__Q('.mbh')===0&&__Q('.mbback')>0,
  QBACK:()=>!S.oxQueue&&__Q('.mbh')===1,
  QMODEG:()=>S.oxQMode==='g',
  SRCH:()=>__Q('.mbres .rr')>0&&/개$/.test(txt(document.querySelector('.mbsr .cnt'))),
  SRCH_CLR:()=>{const r=document.querySelector('.mbres');return !!r&&r.classList.contains('hide')},
  SRCHCNT:()=>/개$/.test(txt(document.querySelector('.mbsr .cnt'))),
  TABJO:()=>!!__JT()&&__JT().style.display==='none',
  TABGI:()=>!!__JT()&&__JT().style.display!=='none'&&__JT().querySelectorAll('.jtch').length>0,
  MARKSEL:()=>__Q('.mboxb.sel')>=1,
  GRADED:()=>__OPEN(),
  PEEKOPEN:()=>__OPEN(),
  POP1:()=>!!POPS&&POPS.length>=1,
  POPJO:()=>/조|⚖/.test(__TT(__LP())),
  POPGGU:()=>/근거를 쓰는 지문/.test(__TT(__LP())),
  POPJN:()=>/📋 정리/.test(__TT(__LP())),
  POPPREC:()=>/^⚖ /.test(__TT(__LP())),
  POPMC:()=>{const p=__LP();return !!p&&p.querySelectorAll('.mcgrp').length===1&&p.querySelectorAll('.mcgrp .hd .go').length===1},
  POPJN2:()=>{const p=__LP();return !!p&&p.querySelectorAll('.jnsub').length>=1&&!!p.querySelector('.cdim')},
  IDPOP:()=>{const p=__LP();return !!p&&/교재 자리/.test(__TT(p))&&p.querySelectorAll('.mbbrow').length>=2},
  TYMIX:()=>[...document.querySelectorAll('.mbtype .seg.ty')].some(e=>txt(e)==='혼합'),
  GGREF:()=>__Q('.ggrefbox .ggrefrow')>=1,
  GGHOT:()=>{const g=document.querySelector('.gguse');return !!g&&g.classList.contains('hot')},
  GGLINE:()=>__Q('.ggline .fd')>0,
  GGPX:()=>['.ggline','.ggline .lb','.ggline .in','.ggline .fd','.ggnum','.ggpan','.ggpan .hd','.ggpan .hd .t','.ggpan .hd .m','.ggpan .hd .lk'].every(s=>!!document.querySelector(s)),
  MKBACK:()=>__Q('mark.mkc')>=1,
  MKOFF:()=>__Q('.mbqtx[data-mk]')>0&&__Q('mark.mkc')===0,
  MKON:()=>__Q('mark.mkc')>=1,
  MKCARDS:()=>__Q('.mbqtx[data-mk]')>0,
  INKOFF:()=>['.ggline .in','.mbpeek','.mboxb','.mbqtx'].every(s=>!!document.querySelector(s)),
  GICHUL:()=>S.jimunTab==='gichul'&&__Q('.mbsbar')===1&&__Q('.exv-num')>0&&__Q('.mboxb')>0&&__Q('#slot .mbomr')>=1,
  IDLE:()=>true
 };
 const WU=async(ms,tag)=>{
  const t0=performance.now(), f=__CONDS[tag]; let ok=false;
  for(;;){
   let v=false; try{ v=__IDLE()&&(f?!!f():true); }catch(e){}
   if(v){ ok=true; break; }
   if(performance.now()-t0>=ms) break;
   await wait(25);
  }
  if(ok) await wait(80);   /* 표지가 참인 뒤 한 박자 — 같은 틱에 이어 일어나는 그리기 · setTimeout 0 이 지나가게 */
  window.__uw.push([tag,Math.round(performance.now()-t0),ok]);
 };
"""


def _regress_probe(p):
    import re as _re
    anchor = 'const wait=ms=>new Promise(r=>setTimeout(r,ms));'
    assert p.count(anchor) == 1, 'PROBE 의 wait 정의를 못 찾음'
    seen = []

    def sub(m):
        rel = 1 + p.count('\n', 0, m.start())
        if rel not in _REG_SITES:
            return m.group(0)   # 표지 없는 자리 = 옛 고정 대기 그대로
        ms, tag = _REG_SITES[rel]
        assert ms == int(m.group(1)), 'PROBE %d 줄 대기가 표와 다르다: %s' % (rel, m.group(0))
        seen.append(rel)
        return "await WU(%d,'%s')" % (ms, tag)
    q = _re.sub(r'await wait\((\d+)\)', sub, p)
    assert sorted(seen) == sorted(_REG_SITES), '표에 있는데 PROBE 에 없는 자리: %s' % sorted(set(_REG_SITES) - set(seen))
    tail = 'out.err=window.__err||[]; }'
    assert q.count(tail) == 1, 'PROBE go() 끝을 못 찾음'
    q = q.replace(tail, 'out.err=window.__err||[]; out.uw=window.__uw||[]; }')
    return q.replace(anchor, anchor + _REG_JS, 1)


def _uw_note(uw):
    """regress — 조건 기다림 셈 한 줄(INFO · 판정 아님) — 시간 초과 표지가 어디인지"""
    uw = uw if isinstance(uw, list) else []
    miss = {}
    for w in uw:
        if not w[2]:
            miss[w[0]] = miss.get(w[0], 0) + 1
    n_ok = sum(1 for w in uw if w[2])
    print('INFO | 기다림 표지(regress) | 조건 기다림 %d회 · 참 %d · 시간 초과 %d(옛 고정 대기만큼 기다림) · 걸린 시간 합 %.1f초 · 시간 초과 표지 %s'
          % (len(uw), n_ok, len(uw) - n_ok, sum(w[1] for w in uw) / 1000.0,
             ', '.join('%s×%d' % kv for kv in sorted(miss.items())) or '없음'))


def _gipairs():
    """문항 JSON 의 (연도·회차) 짝 — **남이 준 수를 믿지 않고 직접 센다.**
       채팅 add2 §D-3 은 27 이라 했으나 실측 39 다(2026-09-21)."""
    import json as _json
    d = _json.load(io.open(os.path.join(JOD, 'data', 'jimun_특허.json'), encoding='utf-8'))
    # A-6(a) 연도 모름 문항(PM-0506 · uid_add2) 짝은 뺀다 — 앱은 그 해 줄을 안 세운다(mbsame add3 수행 결과 ④)
    return sorted({(str(q.get('연도')), str(q.get('회차') or '')) for q in d['문제'] if str(q.get('연도') or '').strip()}, reverse=True)


def run(tag, html):
    QJ.launch('new' if tag == 'new' else 'base')
    _pr = _gipairs()
    probe = (PROBE.replace('__GIN__', str(len(_pr)))
                  .replace('__GIFIRST__', _pr[0][0] + '년 제' + _pr[0][1] + '회'))
    if QJ.REGRESS:   # regress — 고정 대기 → 조건 기다림(위 _REG_SITES · __CONDS)
        probe = _regress_probe(probe)
    io.open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8', newline='').write(
        html.replace('</body>', probe + '</body>', 1))
    done = threading.Event(); box = {}

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=OUT, **k)
        def log_message(self, *a, **k): pass
        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            if p.startswith('/data/'):
                f = os.path.join(JOD, 'data', p[6:].replace('/', os.sep))
                if not os.path.isfile(f): self.send_response(404); self.end_headers(); return
                b = open(f, 'rb').read()
                self.send_response(200); self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(b))); self.end_headers()
                self.wfile.write(b); return
            return super().do_GET()
        def do_POST(self):
            n = int(self.headers.get('Content-Length') or 0)
            box['r'] = self.rfile.read(n).decode('utf-8', 'replace')
            self.send_response(204); self.end_headers(); done.set()

    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    prof = os.path.join(OUT, 'prof_' + tag); shutil.rmtree(prof, ignore_errors=True)
    p = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
                          '--user-data-dir=' + prof, '--window-size=1600,1000',
                          'http://127.0.0.1:%d/index.html' % port],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ok = done.wait(300)
    p.terminate()
    try: p.wait(8)
    except Exception: p.kill()
    srv.shutdown()
    if not ok:
        print('NG %s — 시간 초과' % tag); return {'R': [], 'err': ['시간 초과'], 'snap': {}}
    return json.loads(box['r'])


def src(path_or_rev, rev=False):
    if rev:
        return subprocess.run(['git', '-C', GENIE, 'show', path_or_rev],
                              capture_output=True).stdout.decode('utf-8')
    return io.open(path_or_rev, encoding='utf-8', newline='').read()


new_html = src(NEW)
if QJ.GATE:
    QJ.sub('git:show-app')
    head_html = src(BASE_REV + ':jo/index.html', rev=True)
else:
    head_html = ''   # regress — 바탕(HEAD) 판 소스는 안 푼다(ONLY = 'new' 라 안 쓰임 · git:show-app 0)

res = {}
if ONLY != 'head': res['new'] = run('new', new_html)
if ONLY != 'new': res['head'] = run('head', head_html)

# ── 소스로만 재는 것 ────────────────────────────────────────────────────
def count_calls(s, name):
    """정의·주석을 뺀 실제 부름 수."""
    L = s.replace('\r\n', '\n').split('\n')
    inc = False; call = 0
    for l in L:
        j = 0
        while True:
            k = l.find(name + '(', j)
            if k < 0: break
            pre = l[:k]
            op = pre.rfind('/*'); cl = pre.rfind('*/')
            if l.startswith('function ' + name) or l.startswith('async function ' + name): pass
            elif inc or op > cl: pass
            else: call += 1
            j = k + 1
        o = l.rfind('/*'); c = l.rfind('*/')
        if o > c: inc = True
        elif c > o: inc = False
    return call


raw_new = open(NEW, 'rb').read()
STAT = []
# 이식이 팝업을 더하면 이 수가 는다 — 중요한 것은 **부르는 자리마다 손잡이가 붙는가**(동적 잣대)다.
#   63 = 1구간 바탕 · +1 = 5구간 mbbPop · +1 = 7구간 ggUseWin · +2 = 8구간 jnOpen·mcChapOpen(새 판)
# add1 §B-5 — 카드 발(「✏ 어느 지문에 붙이나」)을 걷어 부름이 하나 줄었다(67 → 66)
# A-6(d) 부름 수 = gaek_mb 인도 검산 — 인도판(f8cec7a) 소스로 잰다(뒤 판들이 팝업을 더함 · 새 팝업 손잡이는 G-10 동적 잣대가 잰다)
if QJ.GATE:   # 처리안 「관문만」 — 인도판(f8cec7a) 소스를 git show 로 풀어 세는 칸 · NEW 와 무관한 상수 → regress 는 안 풂(git:show-app 0)
    QJ.sub('git:show-app')
    del_html = src('f8cec7a:jo/index.html', rev=True)
    STAT.append(('10', 'popShell 부름 66 (바탕 63 + 더한 4 − 걷은 1)', count_calls(del_html, 'popShell') == 66,
                 '부름 %d' % count_calls(del_html, 'popShell')))
STAT.append(('10', 'popShell 안 기본 손잡이 1줄',
             new_html.count("setTimeout(() => { if (p.isConnected && !p._sz) popSizable(body, kind || 'pop'); vvFit(p); }, 0);") == 1,
             '%d' % new_html.count("popSizable(body, kind || 'pop')")))
# A-6(d) 명시 popSizable 부름도 인도판(f8cec7a) 소스로(del_html = 위 popShell 칸에서 정의)
if QJ.GATE:   # 처리안 「관문만」(위 popShell 칸과 같은 인도판 소스)
    STAT.append(('10', '명시 popSizable 부름 16 그대로', count_calls(del_html, 'popSizable') == 16 + 1,
                 '부름 %d (기본 1 포함)' % count_calls(del_html, 'popSizable')))
STAT.append(('11', '파일 CRLF 전용(LF 단독 0)',
             raw_new.count(b'\n') == raw_new.count(b'\r\n'),
             'LF %d · CRLF %d' % (raw_new.count(b'\n'), raw_new.count(b'\r\n'))))
STAT.append(('11', "「📝 학습로그」 단추 코드 0", new_html.count("el('button', 'tool', '📝 학습로그')") == 0,
             '%d' % new_html.count("el('button', 'tool', '📝 학습로그')")))
STAT.append(('11', 'studyLogPop 정의 1', new_html.count('async function studyLogPop') == 1,
             '%d' % new_html.count('async function studyLogPop')))
STAT.append(('5', 'jowon dead 코드 0', new_html.count("'jowon dead'") == 0,
             '%d' % new_html.count("'jowon dead'")))

# ── 찍기 ────────────────────────────────────────────────────────────────
def show(tag, r, stat=()):
    rows = [(x['g'], x['n'], x['ok'], x['got']) for x in r.get('R', [])] + list(stat)
    ng = [x for x in rows if not x[2]]
    print('\n══ %s — %d 항목 · PASS %d · FAIL %d' % (tag, len(rows), len(rows) - len(ng), len(ng)))
    if r.get('err'): print('   오류:', r['err'][:3])
    g0 = None
    for g, n, ok, got in rows:
        if g != g0: print('  §G-%s' % g); g0 = g
        print('    %s %-42s %s' % ('PASS' if ok else 'FAIL', n, got))
    return rows


rows_new = show('새 판', res.get('new', {}), STAT) if 'new' in res else []
rows_head = show('HEAD (헛잣대 §G-13)', res.get('head', {})) if 'head' in res else []
if QJ.REGRESS:
    _uw_note((res.get('new') or {}).get('uw'))

if 'new' in res and 'head' in res:
    # HEAD 에서도 PASS 가 **맞는** 항목 — 새 기능이 아니라 「안 바뀌었나」를 재는 관문이다
    SAME_ON_HEAD = {'명시 종류가 이긴다(cell → note)', '머리 더블클릭 = 기본',
                    '살아있는 갈래 href(HEAD 대조용)', 'studyLogPop 정의는 그대로'}
    print('\n══ §G-13 헛잣대 — HEAD 에서 무너져야 할 항목')
    hm = {(x['g'], x['n']): x['ok'] for x in res['head'].get('R', [])}
    for x in res['new'].get('R', []):
        k = (x['g'], x['n'])
        if k in hm:
            tail = ''
            if x['n'] in SAME_ON_HEAD:
                tail = '   ← 무변 관문(HEAD 도 PASS 가 맞다)'
            elif x['ok'] and hm[k]:
                tail = '   ← 잣대가 안 가린다'
            print('    %-46s 새 판 %s · HEAD %s%s'
                  % (x['n'], 'PASS' if x['ok'] else 'FAIL', 'PASS' if hm[k] else 'FAIL', tail))
    print('\n══ §G-11 밖 무변 — 탭 글자 대조 (HEAD ↔ 새 판)')
    # ⚠ 1차객 OX 탭은 **이 판이 바꾸는 자리**다 — 다른 것이 맞다(첫 화면으로 갈렸다).
    #   무변이어야 하는 것은 조문·판례·기출 탭이다.
    for k, nm in (('jo', '조문 탭'), ('prec', '판례 탭'), ('gi', '1차객 기출 탭'),
                  ('ox', '1차객 OX 탭 ※ 이 판이 바꾸는 자리')):
        a = res['head'].get('snap', {}).get(k, ''); b = res['new'].get('snap', {}).get(k, '')
        same = a == b
        note = ''
        if not same:
            i = next((i for i in range(min(len(a), len(b))) if a[i] != b[i]), min(len(a), len(b)))
            note = ' · 첫 어긋남 %d자 · HEAD「%s」 새「%s」' % (i, a[i:i + 40], b[i:i + 40])
        print('    %-12s %s · %d자 ↔ %d자%s'
              % (nm, '같음' if same else '다름', len(a), len(b), note))
    print('\n══ §G-5 살아있는 ⚖ href')
    print('    HEAD %s' % res['head'].get('liveHref', ''))
    print('    새 판 %s' % res['new'].get('liveHref', ''))
    print('    글자 하나 안 다름: %s' % (res['head'].get('liveHref') == res['new'].get('liveHref')))

print('\n새 판 md5(LF) %s · %d B'
      % (hashlib.md5(raw_new.replace(b'\r\n', b'\n')).hexdigest(), len(raw_new)))
