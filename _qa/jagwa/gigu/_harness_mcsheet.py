# -*- coding: utf-8 -*-
"""암기카드 여는 자리 · 종이 꼴 모아보기 · 팝업 크기 — 헤드리스 검산
(2026-09-07 · gigu/_task_jagwa_pan2_add2.md §3)

  M  지학 — 머리 단추 · 전 문항/절별 · 띠 · 라벨 · 회차별 · unitOf · 크기 · 카드 좌표 무변
  B  생물 — 카드 층이지만 조각이 없다(JG false) → 종전 꼴 그대로 · 안 깨진다
  Y  물리 — 두 단추·모아보기가 add1 실물과 **글자까지 같다**(HEAD 블롭으로 한 번 더 돌려 대조)
  S  원본 대조(파이썬)

⚠ 픽셀 IDENTICAL 게이트는 쓰지 않는다(CLAUDE.md 「자과앱에는 픽셀 게이트를 걸지 않는다」).
   이 판은 화면이 달라지는 것이 목적이다 — 지시서 §3 도 그렇게 적혀 있다.

    PYTHONIOENCODING=utf-8 python _harness_mcsheet.py            # 전부
    PYTHONIOENCODING=utf-8 python _harness_mcsheet.py earth      # 묶음 하나만
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import _qa_jagwa_common as JG   # noqa: E402 — _task_qa_fix1 §A-1(10/9) · 쪽 안 기다림 wait 한 벌(JG.WAIT_JS)만 가져다 씀(이 하네스의 다른 정의는 무변)
import http.server, os, socketserver, subprocess, sys, threading, hashlib, shutil, urllib.parse, json, time

GENIE = _roots.genie()
SRC = os.path.join(GENIE, 'jagwa', 'index.html')
SPDROOT = _roots.spd()
GIGU = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.environ.get('TEMP', '.'), 'mcsh'); os.makedirs(OUT, exist_ok=True)
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
 /* 옛 줄: const wait=ms=>new Promise(r=>setTimeout(r,ms)); — _task_qa_fix1 §A-1(10/9) 새 정의 = JG.WAIT_JS(_qa_jagwa_common.py 한 벌 · 바로 아래 이어 붙임) */
""" + JG.WAIT_JS + r"""
 setInterval(()=>{try{__nativeFetch('/partial',{method:'POST',body:R.join(String.fromCharCode(10))+String.fromCharCode(10)+'(err) '+JSON.stringify(window.__err||[])})}catch(e){}},3000);
 const grp=async(name,fn)=>{try{await fn()}catch(e){T(name+' 묶음 예외',false,String(e&&e.stack||e).slice(0,300))}};
 const $$$=s=>[...document.querySelectorAll(s)];
 const sheetOf=()=>document.querySelector('.sheet .mcpaper')?document.querySelector('.sheet:has(.mcpaper)'):null;
 const closeSheets=()=>{document.querySelectorAll('.sheet').forEach(x=>{if(x.parentElement===document.body&&!x.id)x.remove()})};
 /* 모서리 끌기 — 포인터로 실제로 끈다(펜·손가락 다 잡는지 pointerType 을 갈아 가며) */
 const PE=(t,el,x,y,pt)=>el.dispatchEvent(new PointerEvent(t,{clientX:x,clientY:y,bubbles:true,cancelable:true,pointerId:7,pointerType:pt||'mouse',isPrimary:true}));
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

# ═══════════════════════════ M. 지학 ═══════════════════════════
BODY_EARTH = r"""
   await loadEarthData(); draw(); await wait(120);
   T('M-0 지학 카드 층 · 조각 좌표표 있다(JG)',CARD_LAYER===true&&SUBJ_ID==='earth'&&DATA.length>0&&jogakAny()===true,[SUBJ_ID,DATA.length]);
   /* A-6(a) 9/30 — 목록 머리 「암기카드」(#btnMC → mcardSheet(null,'전 문항'))는 9/20 부터 없다 — 🃏 전체(#mcAll → 🃏 창)가 갈음했다
      (gigu/_task_jagwa_earth_listpop_add1.md §C · cd248a5 if(rd&&!ISEA) → c9faff2 if(rd&&!SHELL) 세 과목). 종이 모아보기 mcardSheet 는 남아 있어
      (§C 「mcardSheet 함수는 남긴다」) 아래 묶음은 그 단추가 부르던 그대로 직접 부른다 — 화면에서 여는 길은 없다(재는 것 = 종이 꼴 · 크기 · 배치 그대로) */
   const MCALL=()=>mcardSheet(null,'전 문항');
   /* ★ uid_unify A-1(10/4 · 근거 gigu/_task_jagwa_uid_unify.md §A 약속 1 「mcard 통 포함 — 열쇠 함수 qk(no) 한 곳」 · 앱 mcardSheet/mcardWin 의 MC[qk(no)]) —
      카드 잉크 MC 의 열쇠 = 카드 층 uid · 옛 판(qk 없음 · 바탕 4754b1d)은 번호 그대로. 번호로 심으면 앱이 못 읽고 stampAll 의 uidGuard 가 uid 칸으로 옮겨 번호 칸이 비어 버린다 */
   const MK=n=>typeof qk==='function'?qk(n):n;

   /* ═══ M-1 목록 머리 단추 ═══ */
   await grp('M-1', async()=>{
     /* ⚠ body.innerHTML 로 세면 안 된다 — 물리에서 두 단추를 떼는 줄의 주석에도 그 글자가 있다(script 도 innerHTML 이다) */
     const head=document.querySelector('.count');
     /* A-6(a) 9/30 — 껍데기가 목록 머리 .count 줄을 통째로 숨긴다(listpop_add1 §A 「걷는 것 … .count 줄」 · cd248a5 지학 → c9faff2 세 과목 body[data-shell] #lib>.count{display:none}).
        #btnRand 는 #btnMC 를 만들 때만 떼던 것이라(if(rd&&!SHELL)) 숨은 줄 안에 남는다 → 「0곳」 = 화면에 보이는 것 0 */
     T('M-1 목록 머리에 「랜덤으로 풀기」·「처음부터 풀기」가 0곳',
       !document.getElementById('btnFirst')&&(b=>!b||b.getClientRects().length===0)(document.getElementById('btnRand'))&&head.textContent.indexOf('처음부터 풀기')<0,head.textContent.trim().slice(0,80));
     const mb=document.getElementById('btnMC');
     /* A-6(a) 9/30 — 목록 머리 「암기카드」(#btnMC)는 🃏 가 갈음했다(listpop_add1 §C · cd248a5 → c9faff2) — 자리 = 약점 줄(#esh .ebar)의 #mcAll 「🃏 전체 N」(누르면 🃏 창 mcwOpen('all')) */
     const ma=document.getElementById('mcAll');
     T('M-1 「🃏 전체」가 1곳 · 그 자리(약점 줄 .ebar)에 있다 — 옛 「암기카드」(#btnMC)는 없다',!mb&&!!ma&&$$$('#mcAll').length===1&&ma.textContent.indexOf('🃏 전체')===0&&!!ma.closest('#esh .ebar'),[!!mb,!!ma,ma&&ma.textContent,ma&&ma.parentElement&&ma.parentElement.id]);
     T('M-1 그 줄의 다른 단추(공식 보기·개념으로 훑기)는 그대로',!!document.getElementById('btnFormula')&&!!document.getElementById('btnConcept'));
   });

   /* ═══ M-2 머리에서 열면 전 문항 ═══ */
   let COLS=0;
   await grp('M-2', async()=>{
     closeSheets(); MCALL(); await wait(400);
     const paper=document.querySelector('.mcpaper');
     T('M-2 누르면 모아보기가 종이 꼴로 열린다',!!paper&&$$$('.mcgrid').length===0,[!!paper,$$$('.mcgrid').length]);
     const cards=$$$('.mcpaper .mcard');
     T('M-2 그린 칸 수 = 대상 문항 수(전 문항)',cards.length===DATA.length,[cards.length,DATA.length]);
     const nos=new Set(cards.map(el=>+el.dataset.no));
     T('M-2 빠진 문항 0 · 겹친 칸 0',nos.size===DATA.length&&DATA.every(r=>nos.has(r[F.NO])),[nos.size,DATA.length]);
     COLS=$$$('.mccol').length;
     T('M-2 열이 둘 이상이다(세로로 채우고 다음 열로)',COLS>1,COLS);
     /* 세로로 채운다 — 한 열 안에서 칸이 위에서 아래로 */
     const c0=$$$('.mccol')[0].querySelectorAll('.mcard');
     let down=true;for(let i=1;i<c0.length;i++)if(c0[i].getBoundingClientRect().top<=c0[i-1].getBoundingClientRect().top)down=false;
     T('M-2 한 열 안에서 칸이 위에서 아래로 쌓인다',c0.length>1&&down,c0.length);
     const r0=$$$('.mccol')[0].getBoundingClientRect(), r1=$$$('.mccol')[1].getBoundingClientRect();
     T('M-2 다음 열은 오른쪽이다',r1.left>r0.left&&Math.abs(r1.top-r0.top)<2,[r0.left,r1.left,r0.top,r1.top]);
   });

   /* ═══ M-3 단원 줄에서 열면 그 절만 ═══ */
   await grp('M-3', async()=>{
     closeSheets(); await wait(60);
     /* A-6(a) 9/30 — 절 머리 「암기카드 N」(ghbtn → mcardSheet(sub,sub))은 🃏 칩이 갈음했다(listpop_add1 §C · 수행 결과 C 「절 머리 「암기카드」 0」 · cd248a5)
        → 절 머리 🃏(data-mc="s:<절>")로 절을 고르고 옛 단추가 부르던 mcardSheet(sub,sub) 를 직접 부른다(sub = 절 코드 + 이름 = 카드 층 F.SUB · refreshUnits) */
     const gh=$$$('#list [data-mc^="s:"]')[0];
     T('M-3 절 머리 「암기카드 N」은 🃏 칩이 갈음했다(🃏 있음 · 「암기카드」 단추 0)',!!gh&&$$$('#list .ghbtn').filter(x=>x.textContent.indexOf('암기카드')===0).length===0,gh&&gh.textContent);
     const sec=gh.dataset.mc.slice(2);
     const want=DATA.filter(r=>r[F.SUB]===(sec+' '+((TOC.sec[sec]||{}).name||''))).length;
     mcardSheet(sec+' '+((TOC.sec[sec]||{}).name||''),sec+' '+((TOC.sec[sec]||{}).name||'')); await wait(400);
     const cards=$$$('.mcpaper .mcard');
     T('M-3 그 절만 그린다 — 그린 칸 수 = 그 절 문항 수',cards.length===want&&want>0&&want<DATA.length,[cards.length,want,sec]);
     T('M-3 그때도 종이 꼴이다',$$$('.mcpaper').length===1);
     closeSheets();
   });

   /* ═══ M-4 미분류 · M-5 분홍 띠 · M-6 보라 띠 · M-7 띠 높이 ═══ */
   await grp('M-4567', async()=>{
     closeSheets(); MCALL(); await wait(400);
     const cols=$$$('.mccol');
     /* 파이썬이 못 세는 값이라 여기서 기대값을 직접 만든다 — 앱이 쓰는 unitOf 를 그대로 쓴다 */
     const secOfRow=r=>{const u=unitOf(r[F.NO])||'';return (u&&u.split('.').length>=2)?secOf(u):''};
     const un=DATA.filter(r=>!secOfRow(r));
     const lastCols=cols.slice(-Math.ceil(un.length/Math.max(1,cols[0].querySelectorAll('.mcard').length)));
     const tailNos=new Set([].concat(...lastCols.map(c=>[...c.querySelectorAll('.mcard')].map(x=>+x.dataset.no))));
     T('M-4 단원 없는 문항이 맨 뒤에 모여 있다(빠진 칸 0)',un.length>0&&un.every(r=>tailNos.has(r[F.NO])),[un.length,tailNos.size]);
     T('M-4 그 열들의 절 띠는 비어 있다(.mcsec.none · 글자 0자)',lastCols.every(c=>{const s=c.querySelector('.mcsec');return s.classList.contains('none')&&s.textContent.trim()===''}));

     /* M-5 분홍 = 장이 바뀌는 열에만 */
     const chSeq=cols.map(c=>{const a=c.querySelector('.mcard');return a?(function(){const r=rec(+a.dataset.no);const u=unitOf(r[F.NO])||'';return u?chOf(u):''})():''});
     let want5=0,prev='@';chSeq.forEach(ch=>{if(ch!==prev){want5++;prev=ch}});
     const on=$$$('.mcch.on');
     T('M-5 분홍 띠가 장이 바뀌는 열에만 있다',on.length===want5,[on.length,want5,chSeq.slice(0,12)]);
     T('M-5 분홍 띠가 없는 열은 글자 0자(흰색)',cols.every(c=>{const e=c.querySelector('.mcch');return e.classList.contains('on')||e.textContent.trim()===''}));
     T('M-5 분홍 띠 글자는 「n. 이름」 꼴 · 미분류도 있다',on.every(e=>/^(\d+\. .+|미분류)$/.test(e.textContent.trim())),on.slice(0,6).map(e=>e.textContent.trim()));

     /* M-6 보라 = 절이 시작하는 열에만 제목 */
     const secSeq=cols.map(c=>{const a=c.querySelector('.mcard');return a?secOfRow(rec(+a.dataset.no)):''});
     let want6=0,prev6='@';secSeq.forEach(s=>{if(s!==prev6){if(s)want6++;prev6=s}});
     const titled=cols.filter(c=>c.querySelector('.mcsec').textContent.trim()!=='');
     T('M-6 보라 제목이 절이 시작하는 열에만 있다',titled.length===want6,[titled.length,want6]);
     T('M-6 이어지는 열은 띠만 있고 글자 0자',cols.every(c=>{const s=c.querySelector('.mcsec');
       return s.textContent.trim()===''||s.textContent.trim()===titled.find(t=>t===c)?.querySelector('.mcsec').textContent.trim()}));
     T('M-6 「(이어짐)」 같은 표시가 0건',document.querySelector('.mcpaper').textContent.indexOf('이어짐')<0);

     /* M-7 띠 높이가 열마다 같다 */
     const tops=cols.map(c=>{const a=c.querySelector('.mcard');return a?Math.round(a.getBoundingClientRect().top-c.getBoundingClientRect().top):-1});
     T('M-7 첫 칸의 자리가 모든 열에서 같다(띠 높이가 같다)',new Set(tops).size===1,[...new Set(tops)].slice(0,5));
   });

   /* ═══ M-8 라벨 ═══ */
   await grp('M-8', async()=>{
     const bs=$$$('.mcpaper .mcard .t b');
     const G=bs.filter(e=>/^\d{2}-\d{2,3}-\d{1,2}$/.test(e.textContent.trim()));
     const gwant=DATA.filter(r=>(+r[F.YEAR]||0)&&(+r[F.ROUND]||0)&&(+r[F.LNO]||0)).length;
     T('M-8 기출 칸 라벨이 25-62-9 꼴 · 수가 맞다',G.length===gwant&&gwant>0,[G.length,gwant,bs.length]);
     T('M-8 「62회 9번」 꼴이 0건',bs.every(e=>!/회\s*\d+\s*번/.test(e.textContent)),bs.filter(e=>/회\s*\d+\s*번/.test(e.textContent)).slice(0,3).map(e=>e.textContent));
     T('M-8 uid 를 라벨에서 뺐다(.mcc 0건)',$$$('.mcpaper .mcc').length===0);
     T('M-8 라벨 = 연도 두 자리-회차-문번(값 대조)',(function(){const el=bs.find(e=>/^\d{2}-\d{2,3}-\d{1,2}$/.test(e.textContent.trim()));
       const no=+el.closest('.mcard').dataset.no,r=rec(no);
       return el.textContent.trim()===String((+r[F.YEAR])%100).padStart(2,'0')+'-'+(+r[F.ROUND])+'-'+(+r[F.LNO])})());
   });

   /* ═══ M-9 회차별 ═══ */
   await grp('M-9', async()=>{
     const rb=document.querySelector('.mcbar [data-m="round"]');
     T('M-9 단원별/회차별 토글이 그대로 있다',!!rb&&!!document.querySelector('.mcbar [data-m="unit"]')&&!!document.getElementById('mcW'));
     rb.click(); await wait(400);
     T('M-9 회차별에서 분홍 장 띠가 0건',$$$('.mcch.on').length===0,$$$('.mcch.on').length);
     const titled=$$$('.mccol .mcsec').filter(s=>s.textContent.trim()!=='');
     T('M-9 띠는 회차 하나만 쓴다 — 「62회 (2025)」 꼴',titled.length>0&&titled.every(s=>/^\d+회( \(\d{4}\))?$|^회차 없음$/.test(s.textContent.trim())),titled.slice(0,4).map(s=>s.textContent.trim()));
     T('M-9 회차별에서도 그린 칸 수 = 전 문항',$$$('.mcpaper .mcard').length===DATA.length,[$$$('.mcpaper .mcard').length,DATA.length]);
     document.querySelector('.mcbar [data-m="unit"]').click(); await wait(400);
     T('M-9 단원별로 돌아온다',$$$('.mcch.on').length>0);
   });

   /* ═══ M-10 unitOf — 손으로 옮긴 값이 이긴다 ═══ */
   await grp('M-10', async()=>{
     const r=DATA.find(x=>(unitOf(x[F.NO])||'').split('.').length>=3);
     const uid=r[F.CODE], keep=UN[uid], was=unitOf(r[F.NO]);
     const to=(function(){for(const c in TOC.unit){if(secOf(c)!==secOf(was))return c}return ''})();
     UN[uid]=to; refreshUnits();
     closeSheets(); MCALL(); await wait(400);
     const el=document.querySelector('.mcpaper .mcard[data-no="'+r[F.NO]+'"]');
     const col=el.closest('.mccol'), idx=$$$('.mccol').indexOf(col);
     /* 그 칸이 속한 열 묶음의 절 제목을 거슬러 올라가 찾는다(이어지는 열은 글자가 없다) */
     let title='';for(let i=idx;i>=0;i--){const t=$$$('.mccol')[i].querySelector('.mcsec').textContent.trim();if(t){title=t;break}}
     T('M-10 손으로 옮긴 단원(UN)이 이겨서 그 절 자리에 그려진다',title.indexOf(secOf(to))===0,[was,to,title]);
     if(keep===undefined)delete UN[uid];else UN[uid]=keep; refreshUnits();
     closeSheets();
   });

   /* ═══ M-11 크기 조절 ═══ */
   await grp('M-11', async()=>{
     try{localStorage.removeItem('jagwa.win.mcsheet')}catch(e){}
     delete WIN['mcsheet'];
     MCALL(); await wait(400);
     const p=document.querySelector('.mcpp');
     T('M-11 모서리 손잡이가 시트에 붙어 있다',!!p.querySelector('.twgrip'));
     const g=p.querySelector('.twgrip'), r0=p.getBoundingClientRect(), gr=g.getBoundingClientRect();
     PE('pointerdown',g,gr.left+5,gr.top+5,'touch');            /* 손가락으로 잡는다 */
     PE('pointermove',g,gr.left+5-120,gr.top+5-90,'touch');
     PE('pointerup',g,gr.left+5-120,gr.top+5-90,'touch');
     await wait(400);
     const r1=document.querySelector('.mcpp').getBoundingClientRect();
     /* 옛 줄: T('M-11 손가락으로 모서리를 끌면 창 크기가 바뀐다',Math.abs(r1.width-(r0.width-120))<3&&Math.abs(r1.height-(r0.height-90))<3,…) */
     /* ★ 2026-10-09 _task_jagwa_gg3 §A-4(makeFloat 첫 높이 ≤ 1/3 · 세 과목) — 첫 높이가 낮아 −90 이 최소 높이 200 에 걸리면 200 을 받음(바탕은 첫 높이가 커서 옛 셈 그대로) */
     T('M-11 손가락으로 모서리를 끌면 창 크기가 바뀐다',Math.abs(r1.width-(r0.width-120))<3&&Math.abs(r1.height-Math.max(r0.height-90,200))<3,[r0.width,r1.width,r0.height,r1.height]);
     const saved=JSON.parse(localStorage.getItem('jagwa.win.mcsheet')||'null');
     T('M-11 크기를 localStorage(jagwa. 접두사)에 적는다 · SET 에는 안 넣는다',
       !!saved&&Math.abs(saved.w-r1.width)<3&&Math.abs(saved.h-r1.height)<3&&(typeof SET!=='object'||SET.mcsheet===undefined),saved);
     /* 펜으로도 잡힌다 */
     const g2=document.querySelector('.mcpp .twgrip'), gr2=g2.getBoundingClientRect(), r2=document.querySelector('.mcpp').getBoundingClientRect();
     PE('pointerdown',g2,gr2.left+5,gr2.top+5,'pen');
     PE('pointermove',g2,gr2.left+5+60,gr2.top+5+40,'pen');
     PE('pointerup',g2,gr2.left+5+60,gr2.top+5+40,'pen');
     await wait(400);
     const r3=document.querySelector('.mcpp').getBoundingClientRect();
     T('M-11 펜으로도 잡힌다',Math.abs(r3.width-(r2.width+60))<3,[r2.width,r3.width]);
     /* 화면 밖으로 못 나간다 */
     delete WIN['mcsheet'];
     try{localStorage.setItem('jagwa.win.mcsheet',JSON.stringify({w:99999,h:99999}))}catch(e){}
     closeSheets(); MCALL(); await wait(400);
     const r4=document.querySelector('.mcpp').getBoundingClientRect();
     T('M-11 화면보다 크게는 안 된다(화면−16 로 가둔다)',r4.width<=innerWidth-15&&r4.height<=innerHeight-15&&r4.left>=-1&&r4.top>=-1,[r4.width,r4.height,innerWidth,innerHeight]);
     T('M-11 최소 크기가 있다',(function(){delete WIN['mcsheet'];try{localStorage.setItem('jagwa.win.mcsheet',JSON.stringify({w:10,h:10}))}catch(e){}
       closeSheets();MCALL();const rr=document.querySelector('.mcpp').getBoundingClientRect();
       return rr.width>=280&&rr.height>=200})());
     /* 다시 열면 그 크기 */
     delete WIN['mcsheet'];
     try{localStorage.setItem('jagwa.win.mcsheet',JSON.stringify({w:900,h:520}))}catch(e){}
     closeSheets(); MCALL(); await wait(400);
     const r5=document.querySelector('.mcpp').getBoundingClientRect();
     T('M-11 닫고 다시 열면 적어 둔 그 크기다',Math.abs(r5.width-900)<2&&Math.abs(r5.height-520)<2,[r5.width,r5.height]);
     T('M-11 열당 칸 수를 새 높이에 맞춰 다시 센다(칸 수는 그대로)',$$$('.mcpaper .mcard').length===DATA.length,[$$$('.mcpaper .mcard').length,DATA.length]);
     closeSheets();
   });

   /* ═══ M-12 카드 좌표 무변 ═══ */
   await grp('M-12', async()=>{
     const no=DATA[0][F.NO];
     /* 옛: MC[no]={s:[{c:'#B03A2E',w:2,hl:0,p:[100,120,300,420,700,880]}]};
     const snap=JSON.stringify(MC[no]); */
     MC[MK(no)]={s:[{c:'#B03A2E',w:2,hl:0,p:[100,120,300,420,700,880]}]};
     const snap=JSON.stringify(MC[MK(no)]);
     delete WIN['mcard'];try{localStorage.removeItem('jagwa.win.mcard')}catch(e){}
     await openView(no); await wait(300); mcardWin(no); await wait(300);
     const p=document.querySelector('.mcwin .panel'), cv0=document.querySelector('.mccv').getBoundingClientRect();
     const ar0=cv0.width/cv0.height;
     const g=p.querySelector('.twgrip'), gr=g.getBoundingClientRect();
     PE('pointerdown',g,gr.left+5,gr.top+5,'touch');PE('pointermove',g,gr.left+165,gr.top+125,'touch');PE('pointerup',g,gr.left+165,gr.top+125,'touch');
     await wait(500);
     const p1=document.querySelector('.mcwin .panel').getBoundingClientRect();
     T('M-12 카드 창도 모서리로 커진다',p1.width>0,[p1.width,p1.height]);
     T('M-12 카드 창 크기도 기기 하나 값으로 적힌다',!!JSON.parse(localStorage.getItem('jagwa.win.mcard')||'null'));
     const cv1=document.querySelector('.mccv').getBoundingClientRect();
     T('M-12 그리는 바닥 비율이 그대로다(같은 식으로 다시 잰다)',Math.abs(cv1.width/cv1.height-ar0)<0.06,[ar0,cv1.width/cv1.height,cv1.width,cv1.height]);
     /* 옛: T('M-12 획의 상대 좌표가 전건 같다(창 크기는 mcard 에 안 들어간다)',JSON.stringify(MC[no])===snap,[JSON.stringify(MC[no]).slice(0,80),snap.slice(0,80)]); */
     /* 판정은 같다(MC[열쇠] 의 글자 == 처음 심은 글자) — 값이 없을 때 .slice 로 예외가 나 아래 정리 줄이 건너뛰어지던 info 만 String() 으로 감쌌다(예외 0 · 뒤 칸이 같이 끊기지 않게) */
     T('M-12 획의 상대 좌표가 전건 같다(창 크기는 mcard 에 안 들어간다)',JSON.stringify(MC[MK(no)])===snap,[String(JSON.stringify(MC[MK(no)])).slice(0,80),snap.slice(0,80)]);
     document.querySelectorAll('.sheet').forEach(x=>{if(x.classList.contains('mcwin'))x.remove()});
     /* 옛: delete MC[no]; closeView(); await wait(80); */
     delete MC[MK(no)]; closeView(); await wait(80);
   });

   /* ═══ M-14 조각 배경 — 눈에 들어온 칸만 그린다(칸·캔버스는 다 만든다) ═══ */
   await grp('M-14', async()=>{
     closeSheets(); MCALL(); await wait(2500);
     const cvs=$$$('.mcpaper canvas.bg');
     const jgWant=DATA.filter(r=>!!jogakOf(r)).length;
     T('M-14 조각이 있는 칸마다 배경 캔버스가 만들어진다(판 2 와 같은 DOM)',cvs.length===jgWant&&jgWant>0,[cvs.length,jgWant]);
     /* ⚠ 캔버스 기본 크기가 300x150 이라 cv.width 로는 「그렸는가」를 못 잰다.
        앱이 그리기 시작할 때만 붙이는 표시(__jgdone)로 센다. */
     const done=cvs.filter(c=>c.__jgdone===1).length;
     T('M-14 보이는 칸은 실제로 그려진다(비트맵이 조각 크기로 바뀐다)',
       done>0&&cvs.some(c=>c.__jgdone===1&&(c.width!==300||c.height!==150)),[done,cvs.length]);
     T('M-14 안 보이는 칸은 아직 안 그린다(한꺼번에 309장을 안 그린다)',done<cvs.length,[done,cvs.length]);
     /* ⚠ 맨 오른쪽 끝은 미매칭(확인문제) 꼬리라 조각이 아예 없다 — 배경이 있는 마지막 열로 민다 */
     cvs[cvs.length-1].closest('.mccol').scrollIntoView({inline:'center',block:'nearest'}); await wait(2500);
     const done2=$$$('.mcpaper canvas.bg').filter(c=>c.__jgdone===1).length;
     T('M-14 옆으로 밀면 그때 그린다',done2>done,[done,done2]);
     closeSheets();
   });

   /* ═══ M-13 누르는 법 · 판 2 그대로 ═══ */
   await grp('M-13', async()=>{
     closeSheets(); MCALL(); await wait(400);
     const el=document.querySelector('.mcpaper .mcard'); const no=+el.dataset.no;
     const r=el.getBoundingClientRect();
     PE('pointerdown',el,r.left+5,r.top+5); await wait(520); PE('pointerup',el,r.left+5,r.top+5); el.click(); await wait(200);
     T('M-13 길게(≥400ms) = 문항 팝업(이동 아님 · VNO 무변)',!!document.getElementById('mcPop')&&VNO!==no,[!!document.getElementById('mcPop'),VNO,no]);
     const pop=document.getElementById('mcPop');if(pop)pop.remove();
     const el2=document.querySelector('.mcpaper .mcard'); const r2=el2.getBoundingClientRect();
     PE('pointerdown',el2,r2.left+5,r2.top+5); PE('pointermove',el2,r2.left+35,r2.top+5); PE('pointerup',el2,r2.left+35,r2.top+5); await wait(120);
     T('M-13 8px 넘게 움직이면 취소(팝업 안 뜬다)',!document.getElementById('mcPop'));
     closeSheets();
   });

   /* ═══════════ 판 2 add3 ═══════════ */
   /* ── N-1 배치 불변 — 창 높이가 어떻든 같은 문항이 같은 (쪽·열·칸) ── */
   const layout=()=>{const m={};
     $$$('.mcpage').forEach((pg,pi)=>[...pg.querySelectorAll('.mccol')].forEach((c,ci)=>
       [...c.querySelectorAll('.mcard')].forEach((el,ii)=>{m[el.dataset.no]=pi+'/'+ci+'/'+ii})));
     return m};
   const openMC=async(ms)=>{closeSheets();MCALL();await wait(ms||500)};
   await grp('N-1', async()=>{
     try{localStorage.removeItem('jagwa.mcn');localStorage.removeItem('jagwa.mcz')}catch(e){}
     delete WIN['mcsheet'];
     await openMC(700);
     T('N-1 기본 열당 12칸 — 종이와 같다',
       Math.max(...$$$('.mccol').map(c=>c.querySelectorAll('.mcard').length))===12&&+document.getElementById('mcW').value===12,
       [Math.max(...$$$('.mccol').map(c=>c.querySelectorAll('.mcard').length)),document.getElementById('mcW').value]);
     const cd=$$$('.mcpaper .mcard')[0].getBoundingClientRect();
     T('N-1 칸 가로세로비 1.732 ± 0.02',Math.abs(cd.width/cd.height-1.732)<=0.02,[cd.width,cd.height,cd.width/cd.height]);
     const L0=layout(), nc0=$$$('.mccol').length, np0=$$$('.mcpage').length;
     const HS=[820,620,460];const bad=[];
     for(const h of HS){
       delete WIN['mcsheet'];
       try{localStorage.setItem('jagwa.win.mcsheet',JSON.stringify({w:1300,h:h}))}catch(e){}
       await openMC(700);
       const L=layout();
       const diff=Object.keys(L0).filter(k=>L[k]!==L0[k]).length;
       if(diff||$$$('.mccol').length!==nc0||$$$('.mcpage').length!==np0)bad.push([h,diff,$$$('.mccol').length,$$$('.mcpage').length]);
     }
     T('N-1 ★창 높이를 셋으로 바꿔도 열 개수·쪽 수·문항마다의 (쪽/열/칸)이 전건 같다',bad.length===0,[bad,nc0,np0]);
     try{localStorage.removeItem('jagwa.win.mcsheet')}catch(e){}delete WIN['mcsheet'];
   });

   /* ── N-2 최소 칸 높이 · 글자 크기 ── */
   await grp('N-2', async()=>{
     delete WIN['mcsheet'];
     try{localStorage.setItem('jagwa.win.mcsheet',JSON.stringify({w:1300,h:230}))}catch(e){}
     await openMC(700);
     const cd=$$$('.mcpaper .mcard')[0].getBoundingClientRect(), paper=document.querySelector('.mcpaper');
     T('N-2 창이 아주 낮아도 칸 높이가 최소값(34) 아래로 안 내려간다',cd.height>=34,[cd.height]);
     T('N-2 그때는 시트가 세로로 스크롤된다',paper.scrollHeight>paper.clientHeight+10,[paper.scrollHeight,paper.clientHeight]);
     const fs=parseFloat(getComputedStyle($$$('.mcpaper .mcard .t')[0]).fontSize);
     T('N-2 라벨 글자가 최소 크기(7px) 아래로 안 줄어든다',fs>=7,[fs]);
     T('N-2 그린 칸 수 = 대상 문항 수(그대로)',$$$('.mcpaper .mcard').length===DATA.length,[$$$('.mcpaper .mcard').length,DATA.length]);
     try{localStorage.removeItem('jagwa.win.mcsheet')}catch(e){}delete WIN['mcsheet'];
   });

   /* ── N-3 손잡이(열당 칸 수) ── */
   await grp('N-3', async()=>{
     await openMC(600);
     const w=document.getElementById('mcW');
     T('N-3 손잡이가 「열당」이고 범위 8~20 · 눈금 1',w.min==='8'&&w.max==='20'&&w.step==='1'&&/열당/.test(w.parentElement.textContent),[w.min,w.max,w.step]);
     for(const v of [8,20,12]){
       w.value=String(v);w.onchange();await wait(500);
       const mx=Math.max(...$$$('.mccol').map(c=>c.querySelectorAll('.mcard').length));
       T('N-3 손잡이 '+v+' → 열당 '+v,mx===v,[mx,v]);
     }
     w.value='9';w.onchange();await wait(500);
     T('N-3 값이 기기 하나 값으로 남는다(jagwa.mcn) · SET 에는 없다',
       localStorage.getItem('jagwa.mcn')==='9'&&(typeof SET!=='object'||SET.mcn===undefined),localStorage.getItem('jagwa.mcn'));
     await openMC(600);
     T('N-3 다시 열어도 그 값이다',Math.max(...$$$('.mccol').map(c=>c.querySelectorAll('.mcard').length))===9);
     try{localStorage.removeItem('jagwa.mcn')}catch(e){}
     await openMC(600);
   });

   /* ── N-4 쪽으로 끊고 아래로 · 절이 바뀌면 새 열 · 종이와 대조 ── */
   await grp('N-4', async()=>{
     const pages=$$$('.mcpage'), cols=$$$('.mccol'), paper=document.querySelector('.mcpaper');
     T('N-4 한 쪽 = 11열(마지막 쪽만 그보다 적을 수 있다)',
       pages.slice(0,-1).every(p=>p.querySelectorAll('.mccol').length===11)&&pages[pages.length-1].querySelectorAll('.mccol').length<=11,
       pages.map(p=>p.querySelectorAll('.mccol').length));
     T('N-4 쪽 수 = 올림(열 개수 ÷ 11)',pages.length===Math.ceil(cols.length/11),[pages.length,cols.length]);
     const r0=pages[0].getBoundingClientRect(), r1=pages[1].getBoundingClientRect();
     T('N-4 다음 쪽은 아래로 온다',r1.top>r0.bottom-2&&Math.abs(r1.left-r0.left)<2,[r0.bottom,r1.top,r0.left,r1.left]);
     T('N-4 쪽 경계에 굵은 선과 「n쪽」',getComputedStyle(pages[1]).borderTopWidth==='3px'&&/^\d+쪽$/.test(pages[0].querySelector('.mcpgn').textContent),
       [getComputedStyle(pages[1]).borderTopWidth,pages[0].querySelector('.mcpgn').textContent]);
     T('N-4 전체가 세로로 스크롤된다 · 기본 배율에서 가로 스크롤은 없다',
       paper.scrollHeight>paper.clientHeight&&paper.scrollWidth<=paper.clientWidth+1,[paper.scrollHeight,paper.clientHeight,paper.scrollWidth,paper.clientWidth]);
     T('N-4 쪽 바로가기 단추·칩 0개 · 확대축소 단추 0개',
       $$$('.mcpp button').filter(x=>/쪽|확대|축소|100%|＋|－/.test(x.textContent)).length===0,
       $$$('.mcpp button').map(x=>x.textContent.trim()).slice(0,12));
     T('N-4 머리줄 단추 수가 add2 보다 안 늘었다(단원별·회차별 둘 + 슬라이더뿐)',
       $$$('.mcbar b[data-m]').length===2&&$$$('.mcbar button').length===0,[$$$('.mcbar b[data-m]').length,$$$('.mcbar button').length]);
     /* 절이 바뀌면 새 열 */
     const secOfRow=r=>{const u=unitOf(r[F.NO])||'';return (u&&u.split('.').length>=2)?secOf(u):''};
     const mixed=cols.filter(c=>new Set([...c.querySelectorAll('.mcard')].map(el=>secOfRow(rec(+el.dataset.no)))).size>1);
     T('N-4 한 열에 두 절이 섞이지 않는다(절이 바뀌면 새 열)',mixed.length===0,mixed.length);
     /* 종이와 칸 단위로 대조 */
     /* ★ A-6(d) 9/30 — 종이가 두 번 새로 나왔다(사용자 단원 매칭): 9/11 108건 반영 · 자리 바뀐 칸 289(_decisions 2026-09-11) → 9/20 114건 · 88칸(_decisions 2026-09-20 20:20 · gigu/omr_build.py).
        옛 표는 9/8 첫 종이(매칭 전 · 9/4 데이터 그대로) 것이라 지금 앱과 278칸이 달랐다 → 지금 종이 gigu/지학_굿노트_단원순_OMR_20260920.pdf 에서
        _add3_paper_truth.py 와 같은 법(pymupdf 라벨 자리 → 쪽·열·칸)으로 다시 뽑았다(319칸 · 지금 데이터로 앱 배치를 파이썬으로 재면 0칸 다름).
        ⚠ 사용자가 단원을 더 옮기면(기록 unit · 문항.json 단원) 종이를 다시 뽑을 때까지 이 줄은 다시 갈린다 */
     const TRUTH=[[1,0,0,"25-62-9"],[1,0,1,"02-39-2"],[1,0,2,"24-61-7"],[1,0,3,"22-59-6"],[1,0,4,"21-58-9"],[1,0,5,"20-57-5"],[1,0,6,"19-56-8"],[1,0,7,"17-54-7"],[1,0,8,"15-52-7"],[1,0,9,"14-51-4"],[1,0,10,"12-49-7"],[1,0,11,"10-47-7"],[1,1,0,"01-38-10"],[1,1,1,"01-38-2"],[1,1,2,"00-37-1"],[1,1,3,"97-34-5"],[1,1,4,"06-43-3"],[1,1,5,"26-63-7"],[1,1,6,"25-62-1"],[1,1,7,"24-61-1"],[1,1,8,"23-60-1"],[1,1,9,"22-59-8"],[1,1,10,"22-59-2"],[1,1,11,"21-58-5"],[1,2,0,"21-58-4"],[1,2,1,"20-57-2"],[1,2,2,"18-55-2"],[1,2,3,"17-54-1"],[1,2,4,"16-53-1"],[1,2,5,"14-51-1"],[1,2,6,"11-48-3"],[1,2,7,"10-47-1"],[1,2,8,"09-46-10"],[1,2,9,"08-45-5"],[1,2,10,"08-45-2"],[1,2,11,"07-44-2"],[1,3,0,"04-41-4"],[1,3,1,"03-40-5"],[1,3,2,"98-35-9"],[1,3,3,"96-33-5"],[1,3,4,"15-52-4"],[1,3,5,"99-36-9"],[1,4,0,"99-36-6"],[1,4,1,"02-39-7"],[1,4,2,"98-35-3"],[1,4,3,"01-38-1"],[1,5,0,"25-62-10"],[1,5,1,"22-59-9"],[1,5,2,"19-56-3"],[1,5,3,"17-54-9"],[1,5,4,"06-43-2"],[1,5,5,"08-45-9"],[1,5,6,"06-43-10"],[1,5,7,"16-53-10"],[1,5,8,"15-52-10"],[1,5,9,"98-35-6"],[1,5,10,"13-50-9"],[1,5,11,"02-39-1"],[1,6,0,"09-46-1"],[1,6,1,"97-34-1"],[1,7,0,"26-63-5"],[1,7,1,"23-60-7"],[1,7,2,"07-44-9"],[1,7,3,"03-40-1"],[1,7,4,"02-39-10"],[1,7,5,"97-34-2"],[1,7,6,"95-32-2"],[1,7,7,"21-58-6"],[1,7,8,"20-57-6"],[1,7,9,"16-53-7"],[1,7,10,"15-52-6"],[1,7,11,"11-48-2"],[1,8,0,"08-45-7"],[1,8,1,"02-39-8"],[1,8,2,"25-62-8"],[1,8,3,"22-59-7"],[1,8,4,"19-56-5"],[1,8,5,"17-54-6"],[1,8,6,"11-48-4"],[1,8,7,"96-33-4"],[1,8,8,"14-51-6"],[1,8,9,"02-39-9"],[1,8,10,"01-38-9"],[1,8,11,"98-35-4"],[1,9,0,"96-33-9"],[1,9,1,"25-62-6"],[1,9,2,"23-60-6"],[1,9,3,"18-55-5"],[1,9,4,"17-54-5"],[1,9,5,"13-50-7"],[1,9,6,"08-45-4"],[1,9,7,"97-34-3"],[1,9,8,"96-33-7"],[1,9,9,"13-50-3"],[1,9,10,"13-50-6"],[1,9,11,"21-58-3"],[1,10,0,"05-42-8"],[1,10,1,"04-41-10"],[1,10,2,"03-40-3"],[1,10,3,"99-36-4"],[1,10,4,"18-55-6"],[1,10,5,"12-49-5"],[1,10,6,"07-44-8"],[1,10,7,"06-43-1"],[1,10,8,"04-41-8"],[1,10,9,"00-37-2"],[1,10,10,"99-36-8"],[1,10,11,"98-35-2"],[2,0,0,"95-32-1"],[2,0,1,"26-63-1"],[2,0,2,"99-36-5"],[2,0,3,"95-32-3"],[2,1,0,"20-57-7"],[2,1,1,"12-49-6"],[2,1,2,"07-44-7"],[2,1,3,"04-41-7"],[2,1,4,"03-40-2"],[2,1,5,"98-35-8"],[2,1,6,"23-60-5"],[2,1,7,"10-47-6"],[2,1,8,"09-46-2"],[2,1,9,"08-45-6"],[2,1,10,"97-34-4"],[2,1,11,"24-61-8"],[2,2,0,"14-51-8"],[2,2,1,"09-46-4"],[2,2,2,"06-43-6"],[2,2,3,"01-38-3"],[2,2,4,"00-37-10"],[2,2,5,"96-33-10"],[2,2,6,"26-63-8"],[2,2,7,"19-56-10"],[2,2,8,"00-37-9"],[2,2,9,"21-58-7"],[2,2,10,"05-42-7"],[2,2,11,"05-42-6"],[2,3,0,"03-40-4"],[2,4,0,"25-62-3"],[2,4,1,"24-61-2"],[2,4,2,"21-58-1"],[2,4,3,"20-57-4"],[2,4,4,"18-55-1"],[2,4,5,"17-54-3"],[2,4,6,"17-54-2"],[2,4,7,"16-53-2"],[2,4,8,"04-41-1"],[2,4,9,"02-39-4"],[2,4,10,"12-49-1"],[2,4,11,"11-48-7"],[2,5,0,"05-42-4"],[2,5,1,"26-63-6"],[2,5,2,"24-61-4"],[2,5,3,"24-61-3"],[2,5,4,"17-54-4"],[2,5,5,"16-53-3"],[2,5,6,"15-52-5"],[2,5,7,"14-51-3"],[2,5,8,"12-49-3"],[2,5,9,"08-45-3"],[2,5,10,"06-43-8"],[2,5,11,"04-41-2"],[2,6,0,"03-40-6"],[2,6,1,"14-51-7"],[2,6,2,"14-51-5"],[2,6,3,"08-45-1"],[2,6,4,"06-43-5"],[2,6,5,"05-42-2"],[2,6,6,"98-35-5"],[2,6,7,"10-47-2"],[2,6,8,"05-42-3"],[2,6,9,"96-33-6"],[2,7,0,"25-62-2"],[2,7,1,"97-34-8"],[2,7,2,"13-50-2"],[2,7,3,"05-42-5"],[2,7,4,"01-38-6"],[2,7,5,"01-38-5"],[2,8,0,"16-53-6"],[2,8,1,"02-39-6"],[2,8,2,"13-50-4"],[2,8,3,"12-49-8"],[2,8,4,"11-48-1"],[2,9,0,"23-60-2"],[2,9,1,"06-43-7"],[2,9,2,"11-48-10"],[2,9,3,"04-41-5"],[2,9,4,"99-36-7"],[2,9,5,"98-35-7"],[2,9,6,"26-63-2"],[2,9,7,"25-62-4"],[2,9,8,"23-60-3"],[2,9,9,"22-59-1"],[2,9,10,"20-57-1"],[2,9,11,"19-56-2"],[2,10,0,"18-55-4"],[2,10,1,"15-52-1"],[2,10,2,"13-50-5"],[2,10,3,"11-48-9"],[2,10,4,"10-47-3"],[2,10,5,"09-46-3"],[2,10,6,"07-44-10"],[2,10,7,"05-42-1"],[2,10,8,"01-38-4"],[2,10,9,"98-35-1"],[2,10,10,"97-34-10"],[2,10,11,"97-34-9"],[3,0,0,"00-37-8"],[3,0,1,"95-32-4"],[3,1,0,"26-63-3"],[3,1,1,"25-62-5"],[3,1,2,"19-56-6"],[3,1,3,"19-56-1"],[3,1,4,"16-53-5"],[3,1,5,"13-50-1"],[3,1,6,"12-49-10"],[3,1,7,"26-63-4"],[3,1,8,"23-60-4"],[3,1,9,"08-45-8"],[3,1,10,"03-40-7"],[3,1,11,"00-37-4"],[3,2,0,"14-51-2"],[3,2,1,"22-59-3"],[3,2,2,"02-39-5"],[3,2,3,"00-37-3"],[3,2,4,"96-33-8"],[3,3,0,"24-61-5"],[3,3,1,"21-58-2"],[3,3,2,"10-47-5"],[3,3,3,"07-44-1"],[3,4,0,"06-43-9"],[3,4,1,"12-49-9"],[3,4,2,"04-41-3"],[3,4,3,"02-39-3"],[3,5,0,"96-33-2"],[3,5,1,"09-46-9"],[3,5,2,"07-44-4"],[3,5,3,"07-44-3"],[3,5,4,"24-61-6"],[3,5,5,"22-59-4"],[3,5,6,"20-57-3"],[3,5,7,"19-56-4"],[3,5,8,"18-55-3"],[3,5,9,"16-53-4"],[3,5,10,"15-52-3"],[3,5,11,"15-52-2"],[3,6,0,"09-46-8"],[3,6,1,"10-47-4"],[3,7,0,"09-46-7"],[3,7,1,"04-41-6"],[3,7,2,"00-37-6"],[3,7,3,"24-61-10"],[3,7,4,"20-57-8"],[3,7,5,"19-56-7"],[3,7,6,"18-55-8"],[3,7,7,"12-49-2"],[3,7,8,"10-47-9"],[3,7,9,"10-47-8"],[3,7,10,"00-37-5"],[3,7,11,"99-36-3"],[3,8,0,"95-32-6"],[3,8,1,"10-47-10"],[3,8,2,"03-40-9"],[3,8,3,"26-63-9"],[3,8,4,"25-62-7"],[3,8,5,"22-59-10"],[3,8,6,"20-57-10"],[3,8,7,"14-51-10"],[3,8,8,"13-50-8"],[3,8,9,"03-40-8"],[3,8,10,"95-32-7"],[3,8,11,"95-32-5"],[3,9,0,"23-60-8"],[3,9,1,"07-44-6"],[3,9,2,"99-36-1"],[3,9,3,"05-42-9"],[3,9,4,"97-34-7"],[3,9,5,"04-41-9"],[3,9,6,"96-33-3"],[3,10,0,"16-53-8"],[3,10,1,"24-61-9"],[3,10,2,"18-55-7"],[3,10,3,"09-46-6"],[3,10,4,"23-60-9"],[3,10,5,"22-59-5"],[3,10,6,"21-58-10"],[3,10,7,"20-57-9"],[3,10,8,"19-56-9"],[3,10,9,"18-55-10"],[3,10,10,"17-54-8"],[3,10,11,"16-53-9"],[4,0,0,"15-52-9"],[4,0,1,"11-48-5"],[4,0,2,"07-44-5"],[4,0,3,"03-40-10"],[4,0,4,"95-32-9"],[4,0,5,"15-52-8"],[4,0,6,"01-38-7"],[4,0,7,"00-37-7"],[4,0,8,"99-36-2"],[4,0,9,"98-35-10"],[4,0,10,"96-33-1"],[4,0,11,"95-32-8"],[4,1,0,"14-51-9"],[4,1,1,"11-48-8"],[4,1,2,"05-42-10"],[4,1,3,"17-54-10"],[4,1,4,"12-49-4"],[4,1,5,"11-48-6"],[4,1,6,"08-45-10"],[4,1,7,"06-43-4"],[4,1,8,"97-34-6"],[4,2,0,"26-63-10"],[4,2,1,"23-60-10"],[4,2,2,"09-46-5"],[4,2,3,"21-58-8"],[4,2,4,"13-50-10"],[4,2,5,"18-55-9"],[4,2,6,"01-38-8"],[4,2,7,"99-36-10"]];
     const L=layout();
     const miss=[],wrong=[];
     TRUTH.forEach(([p,c,i,lab])=>{
       const el=$$$('.mcpaper .mcard .t b').find(b=>b.textContent.trim()===lab);
       if(!el){miss.push(lab);return}
       const got=L[el.closest('.mcard').dataset.no];
       if(got!==((p-1)+'/'+c+'/'+i))wrong.push([lab,(p-1)+'/'+c+'/'+i,got]);
     });
     T('N-4 ★종이(굿노트 OMR) 319칸이 전건 같은 쪽·열·칸에 온다',miss.length===0&&wrong.length===0,
       [TRUTH.length,miss.slice(0,4),wrong.slice(0,6)]);
   });

   /* ── N-5 확대축소 — 손가락만 · 배치 무변 ── */
   await grp('N-5', async()=>{
     const paper=document.querySelector('.mcpaper');
     const L0=layout(), z0=document.querySelector('.mcz').style.transform;
     T('N-5 기본 배율은 100%',/scale\(1\)/.test(z0)||z0===''||/scale\(1(\.0+)?\)/.test(z0),z0);
     const cd0=$$$('.mcpaper .mcard')[0].getBoundingClientRect().width;
     /* 한 손가락으로 끌면 확대가 아니다 */
     PE('pointerdown',paper,400,400,'touch');PE('pointermove',paper,600,400,'touch');PE('pointerup',paper,600,400,'touch');
     await wait(150);
     T('N-5 한 손가락으로 끌면 확대가 안 된다',/scale\(1\)/.test(document.querySelector('.mcz').style.transform),document.querySelector('.mcz').style.transform);
     /* 두 손가락 핀치 */
     const p1={id:11,x:400,y:400},p2={id:12,x:500,y:400};
     paper.dispatchEvent(new PointerEvent('pointerdown',{clientX:p1.x,clientY:p1.y,pointerId:p1.id,pointerType:'touch',bubbles:true,isPrimary:true}));
     paper.dispatchEvent(new PointerEvent('pointerdown',{clientX:p2.x,clientY:p2.y,pointerId:p2.id,pointerType:'touch',bubbles:true,isPrimary:false}));
     paper.dispatchEvent(new PointerEvent('pointermove',{clientX:600,clientY:400,pointerId:p2.id,pointerType:'touch',bubbles:true}));
     paper.dispatchEvent(new PointerEvent('pointerup',{clientX:600,clientY:400,pointerId:p2.id,pointerType:'touch',bubbles:true}));
     paper.dispatchEvent(new PointerEvent('pointerup',{clientX:400,clientY:400,pointerId:p1.id,pointerType:'touch',bubbles:true}));
     await wait(250);
     const t1=document.querySelector('.mcz').style.transform;
     T('N-5 두 손가락 핀치로 커진다(100 → 200px = 배율 2배)',/scale\(2\)/.test(t1)||/scale\(1\.9|scale\(2\./.test(t1),t1);
     T('N-5 확대해도 배치가 한 칸도 안 바뀐다',Object.keys(L0).every(k=>layout()[k]===L0[k]));
     T('N-5 확대해도 칸의 레이아웃 크기는 그대로다(transform 만 쓴다)',
       Math.abs($$$('.mcpaper .mcard')[0].offsetWidth-cd0)<1,[$$$('.mcpaper .mcard')[0].offsetWidth,cd0]);
     T('N-5 배율이 기기 하나 값으로 남는다(jagwa.mcz) · SET 에는 없다',
       +localStorage.getItem('jagwa.mcz')>1.5&&(typeof SET!=='object'||SET.mcz===undefined),localStorage.getItem('jagwa.mcz'));
     /* ctrl+휠 */
     paper.dispatchEvent(new WheelEvent('wheel',{deltaY:200,ctrlKey:true,bubbles:true,cancelable:true}));
     await wait(200);
     T('N-5 ctrl+휠로 줄어든다',parseFloat(/scale\(([\d.]+)\)/.exec(document.querySelector('.mcz').style.transform)[1])<2);
     /* 빈자리 두 번 톡 = 원래 배율 */
     /* ⚠ 톡은 pointerdown+pointerup 짝이다. up 만 쏘면 「손가락이 둘이었나」 표시가 안 풀려 안 잡힌다(실제 손가락과 다르다) */
     const gapEl=document.querySelector('.mcprow')||paper;
     const tap=(el,x,y)=>{PE('pointerdown',el,x,y,'touch');PE('pointerup',el,x,y,'touch')};
     /* 옛 줄: tap(gapEl,5,5);await wait(70);tap(gapEl,5,5);await wait(250); */
     /* ★ _task_qa_fix1 §A-2(10/9) — 두 번 톡 사이 간격을 쪽 안 타이머(wait(70) · 짐이 크면 앱 기준 330ms 를 넘겨 두 번 톡으로 안 봄 = 10/8 흔들림 N-5 셋) 대신
        CDP 진짜 입력으로 — 파이썬이 Input.dispatchTouchEvent 톡 둘을 간격 70ms 명령으로 던진다(/cdp → _cdp_do · 크롬 --remote-debugging-port=0).
        빈자리 = 종이(.mcpaper) 안 · 칸(.mcard) 밖 · 화면 안 점(둘레 ±12px 도 칸 아님) · 앱이 본 간격 = 진짜 손 뗌(pointerup isTrusted) 두 번 사이 Date.now(앱 잣대와 같은 시계)
        · 배율이 안 돌아왔는데 그 간격이 앱 기준(330ms) 이상이면 FAIL 이 아니라 「다시 잼」 한 번(400ms 쉬어 앞 톡 시각을 흘려보낸 뒤) · CDP 를 못 쓰면 옛 합성 톡 그대로(값에 「cdp 못 씀」) */
     const gapAt=()=>{const pr=paper.getBoundingClientRect();
       const free=(x,y)=>{const e=document.elementFromPoint(x,y);return !!e&&paper.contains(e)&&!e.closest('.mcard')};
       for(let y=Math.max(pr.top,0)+16;y<Math.min(pr.bottom,innerHeight)-16;y+=6)for(let x=Math.max(pr.left,0)+16;x<Math.min(pr.right,innerWidth)-16;x+=6)
         if(free(x,y)&&free(x-12,y)&&free(x+12,y)&&free(x,y-12)&&free(x,y+12))return {x:Math.round(x),y:Math.round(y)};
       return null};
     const upT=[];const upL=e=>{if(e.isTrusted&&e.pointerType==='touch')upT.push(Date.now())};
     const tap2=async p=>{upT.length=0;let r;
       try{r=await (await __nativeFetch('/cdp',{method:'POST',body:JSON.stringify({op:'tap2',x:p.x,y:p.y,gap:70,hold:30})})).json()}catch(e){r={ok:false,err:String(e)}}
       await wait(250);return Object.assign({},r,{app:upT.length>=2?upT[1]-upT[0]:null,ups:upT.length})};
     const gp=gapAt(), tr=[];
     window.addEventListener('pointerup',upL,true);
     if(gp)tr.push(await tap2(gp));
     if(gp&&tr[0].ok&&!/scale\(1\)/.test(document.querySelector('.mcz').style.transform)&&tr[0].app!=null&&tr[0].app>=330){await wait(400);tr.push(await tap2(gp))}   /* 다시 잼 */
     window.removeEventListener('pointerup',upL,true);
     if(!gp||!tr[0]||!tr[0].ok){tap(gapEl,5,5);await wait(70);tap(gapEl,5,5);await wait(250);tr.push({old:'cdp 못 씀 — 옛 합성 톡'})}   /* CDP 못 씀 — 옛 길 그대로 */
     const t2=document.querySelector('.mcz').style.transform;
     T('N-5 빈자리를 두 번 톡 → 원래 배율 100%',/scale\(1\)/.test(t2),[t2,gp,tr]);
     T('N-5 그때 칸 크기가 원래 값이다',Math.abs($$$('.mcpaper .mcard')[0].getBoundingClientRect().width-cd0)<1,[$$$('.mcpaper .mcard')[0].getBoundingClientRect().width,cd0]);
     T('N-5 배치는 그때도 그대로',Object.keys(L0).every(k=>layout()[k]===L0[k]));
     /* 칸 위에서는 두 번 톡이 안 잡힌다(짧게 누름과 안 부딪히게) */
     const card=document.querySelector('.mcpaper .mcard');
     const cr=card.getBoundingClientRect();
     tap(card,cr.left+4,cr.top+4);await wait(70);tap(card,cr.left+4,cr.top+4);await wait(200);
     T('N-5 칸 위 톡은 배율을 안 건드린다',/scale\(1\)/.test(document.querySelector('.mcz').style.transform),document.querySelector('.mcz').style.transform);
     /* 다시 열었을 때 배율이 남는다 */
     try{localStorage.setItem('jagwa.mcz','1.4')}catch(e){}
     await openMC(700);
     T('N-5 다시 열면 적어 둔 배율이다',/scale\(1\.4\)/.test(document.querySelector('.mcz').style.transform),document.querySelector('.mcz').style.transform);
     try{localStorage.removeItem('jagwa.mcz')}catch(e){}
   });

   /* ── N-6 늦게 그리기 뒷정리 ── */
   await grp('N-6', async()=>{
     await openMC(600);
     const cvs=()=>$$$('.mcpaper canvas.bg');
     T('N-6 자리표시자로 「아직 안 그린 칸」과 「조각 없는 칸」이 DOM 으로 갈린다',
       $$$('.mcpaper .mcard').filter(el=>el.querySelector('canvas.bg')&&el.querySelector('.mcph')).length>0&&
       $$$('.mcpaper .mcard').filter(el=>!el.querySelector('canvas.bg')&&el.querySelector('.mcph')).length===0,
       [$$$('.mcph').length,cvs().length]);
     let n=0;while(n++<90&&cvs().filter(c=>c.__jgdone===1&&!c.__jgp).length===0)await wait(500);
     const done=cvs().filter(c=>c.__jgdone===1&&!c.__jgp);
     T('N-6 그려진 칸은 자리표시자가 사라진다',done.length>0&&done.every(c=>!c.parentElement.querySelector('.mcph')),
       [done.length,done.filter(c=>c.parentElement.querySelector('.mcph')).length]);
     T('N-6 안 그린 칸에는 자리표시자가 남아 있다',cvs().filter(c=>!c.__jgdone).every(c=>!!c.parentElement.querySelector('.mcph')));
     /* 지나갔다 돌아오면 그대로 */
     const keep=done[0], sig=[keep.width,keep.height].join('x');
     const paper=document.querySelector('.mcpaper');
     paper.scrollTop=paper.scrollHeight;await wait(1200);
     paper.scrollTop=0;await wait(1200);
     T('N-6 지나갔다 돌아온 칸에 배경이 그대로 있다(상한 안에서)',
       keep.isConnected&&[keep.width,keep.height].join('x')===sig&&!keep.parentElement.querySelector('.mcph'),
       [sig,[keep.width,keep.height].join('x')]);
     /* 축소하면 안 그린다 */
     try{localStorage.setItem('jagwa.mcz','0.45')}catch(e){}
     await openMC(1500);await wait(2500);
     T('N-6 문턱(0.6) 아래로 축소하면 배경을 아예 안 그리고 자리표시자만 둔다',
       $$$('.mcpaper canvas.bg').every(c=>!c.__jgdone)&&$$$('.mcph').length===$$$('.mcpaper canvas.bg').length,
       [$$$('.mcpaper canvas.bg').filter(c=>c.__jgdone).length,$$$('.mcph').length,$$$('.mcpaper canvas.bg').length]);
     try{localStorage.removeItem('jagwa.mcz')}catch(e){}
     await openMC(600);
   });

   /* ── N-7 카드 좌표 무변 · 누르는 법 종전대로 ── */
   await grp('N-7', async()=>{
     const no=DATA[0][F.NO];
     /* 옛: MC[no]={s:[{c:'#B03A2E',w:2,hl:0,p:[110,130,310,430,710,890]}]};
     const snap=JSON.stringify(MC[no]); */
     MC[MK(no)]={s:[{c:'#B03A2E',w:2,hl:0,p:[110,130,310,430,710,890]}]};
     const snap=JSON.stringify(MC[MK(no)]);
     const w=document.getElementById('mcW');w.value='8';w.onchange();await wait(500);
     w.value='20';w.onchange();await wait(500);
     /* 옛: T('N-7 칸 크기를 바꿔도 획의 상대 좌표가 전건 같다',JSON.stringify(MC[no])===snap,[JSON.stringify(MC[no]).slice(0,60)]);
     try{localStorage.removeItem('jagwa.mcn')}catch(e){}delete MC[no]; */
     T('N-7 칸 크기를 바꿔도 획의 상대 좌표가 전건 같다',JSON.stringify(MC[MK(no)])===snap,[String(JSON.stringify(MC[MK(no)])).slice(0,60)]);   /* info 만 String() — 위 M-12 와 같은 까닭 */
     try{localStorage.removeItem('jagwa.mcn')}catch(e){}delete MC[MK(no)];
     await openMC(600);
     const el=document.querySelector('.mcpaper .mcard'), r=el.getBoundingClientRect();
     PE('pointerdown',el,r.left+4,r.top+4);await wait(520);PE('pointerup',el,r.left+4,r.top+4);el.click();await wait(250);
     T('N-7 길게(≥400ms) = 문항 팝업 · VNO 무변(add2 그대로)',!!document.getElementById('mcPop'),!!document.getElementById('mcPop'));
     const pop=document.getElementById('mcPop');if(pop)pop.remove();
     const el2=document.querySelector('.mcpaper .mcard'), r2=el2.getBoundingClientRect();
     PE('pointerdown',el2,r2.left+4,r2.top+4);PE('pointermove',el2,r2.left+34,r2.top+4);PE('pointerup',el2,r2.left+34,r2.top+4);await wait(150);
     T('N-7 8px 넘게 움직이면 취소(add2 그대로)',!document.getElementById('mcPop'));
     closeSheets();
   });
"""

# ═══════════════════════════ B. 생물 ═══════════════════════════
BODY_BIO = r"""
   await loadEarthData(); draw(); await wait(120);
   T('B-0 생물 카드 층 · 조각 좌표표 없다(JG false)',CARD_LAYER===true&&SUBJ_ID==='bio'&&DATA.length>0&&(typeof jogakAny!=='function'||jogakAny()===false),[SUBJ_ID,DATA.length,typeof jogakAny]);
   await grp('B-1', async()=>{
     /* A-6(a) 9/30 — 생물 머리 #btnMC 는 #mcAll 「🃏 전체」가 갈음했다(_task_jagwa_shell_bio_phys_add2 수행 결과 §6 census 「머리 #btnMC 하나(→ #mcAll)」 · c9faff2) ·
        #btnRand 는 숨은 .count 줄 안(listpop_add1 §A → body[data-shell]) · 종전 모아보기 mcardSheet 는 남아 있어 옛 단추가 부르던 그대로 직접 부른다 */
     T('B-1 생물도 머리 단추가 「🃏 전체」 하나(#mcAll · 옛 「암기카드」 #btnMC 없음)',!document.getElementById('btnFirst')&&(b=>!b||b.getClientRects().length===0)(document.getElementById('btnRand'))&&!document.getElementById('btnMC')&&$$$('#mcAll').length===1);
     mcardSheet(null,'전 문항'); await wait(500);
     T('B-1 조각이 없으니 종전 꼴(.mcgrid) 그대로 · 종이 꼴 0건',$$$('.mcgrid').length===1&&$$$('.mcpaper').length===0,[$$$('.mcgrid').length,$$$('.mcpaper').length]);
     T('B-1 전 문항이 그려진다(빠진 칸 0)',$$$('.mcgrid .mcard').length===DATA.length,[$$$('.mcgrid .mcard').length,DATA.length]);
     T('B-1 종전 라벨·uid 그대로(「n. 제목」 · .mcc)',$$$('.mcgrid .mcc').length===DATA.length&&/^\d+\. /.test($$$('.mcgrid .mcard .t b')[0].textContent),[$$$('.mcgrid .mcc').length,$$$('.mcgrid .mcard .t b')[0].textContent]);
     /* ★ A-6(a) 9/30 — add16(genie 0bee72b · _decisions 2026-09-21 15:16)이 「보는 시트」를 떠 있는 창으로 태웠다 — mcardSheet 도 세 과목 모두
        (_task_jagwa_shell_bio_phys_add16.md §A-1 · §A-6 세 과목 공통 · 수행 결과 표 「mcardSheet·cardSheet | mcard·card | 물리 ○ 지학 ○ 생물 ○」 · SHWIN → shFloat → makeFloat)
        → 종전 꼴(.mcgrid)은 그대로 · 판에 float 와 모서리 손잡이(.twgrip) 하나가 붙는다 */
     T('B-1 종전 꼴(.mcgrid) 그대로 · 떠 있는 창 손잡이가 하나 붙는다(add16 — 모아보기도 떠 있는 창)',$$$('.mcgrid').length===1&&$$$('.frmpanel.float .twgrip').length===1,[$$$('.mcgrid').length,$$$('.frmpanel .twgrip').length]);
     closeSheets();
   });
   await grp('B-2', async()=>{
     /* A-6(a) 9/30 — 생물 단원 머리 「암기카드」 45 는 🃏 45 가 갈음했다(shell_bio_phys_add2 §6 census · c9faff2) — 🃏 로 절을 고르고 옛 단추가 부르던 mcardSheet(sub,sub) 를 직접 부른다 */
     const gh=$$$('#list [data-mc^="s:"]')[0];
     T('B-2 단원 줄 「암기카드 N」은 🃏 칩이 갈음했다(🃏 있음 · 「암기카드」 단추 0)',!!gh&&$$$('#list .ghbtn').filter(x=>x.textContent.indexOf('암기카드')===0).length===0);
     {const sec=gh.dataset.mc.slice(2), sub=sec+' '+((TOC.sec[sec]||{}).name||''); mcardSheet(sub,sub);} await wait(400);
     T('B-2 그 절만 · 종전 꼴',$$$('.mcgrid').length===1&&$$$('.mcgrid .mcard').length<DATA.length&&$$$('.mcgrid .mcard').length>0,$$$('.mcgrid .mcard').length);
     closeSheets();
   });
"""

# ═══════════════════════════ Y. 물리 — DOM 을 통째로 찍어 파이썬이 대조 ═══════════════════════════
BODY_PHYS = r"""
   await wait(500);
   /* A-6(d) 9/30 — Y-4 두 판(지금 · HEAD 블롭) DOM 글자 대조는 기록 동기화가 끝난 뒤 찍는다 — 한 판만 동기화가 끝나 물리 목록 글자가 372,109 ↔ 379,538 자로 갈렸다
      (같은 판끼리 · gigu/_task_jagwa_earth_bookwin.md 회귀표 「바탕 판끼리 맞댄 값이 … 갈림 = 기록 동기화 시각 탓」 · _decisions 2026-09-25 01:08 · _harness_earth_shell E-1 9/28 과 같은 길) */
   for(let i=0;i<120&&typeof recBusy!=='undefined'&&recBusy;i++)await wait(500);
   try{if(typeof syncRecords==='function')await Promise.race([syncRecords(true),wait(60000)])}catch(e){}
   for(let i=0;i<120&&typeof recBusy!=='undefined'&&recBusy;i++)await wait(500);
   draw(); await wait(300);
   T('Y-0 물리 · 카드 층 아님',SUBJ_ID==='phys'&&CARD_LAYER===false,[SUBJ_ID,CARD_LAYER]);
   const snap={};
   await grp('Y-1', async()=>{
     T('Y-1 물리는 두 단추를 스스로 뗀다(9/5 필터 손질 B-2) · 새 단추도 안 생긴다',
       !document.getElementById('btnRand')&&!document.getElementById('btnFirst')&&!document.getElementById('btnMC'));
     snap.brand=document.querySelector('.brand').innerHTML;
     snap.list=$('#list').innerHTML; snap.cnt=$('#cnt').textContent;
     snap.n=$$$('#list .item').length;
     T('Y-1 목록이 그려졌다',snap.n>0,snap.n);
   });
   await grp('Y-2', async()=>{
     /* A-6(a) 9/30 — 물리 단원 머리 「암기카드」 61 은 껍데기 🃏 칩이 갈음했다(shell_bio_phys_add2 §6 census 「61 → 🃏 data-mc 63」 · add4 ⑥ · c9faff2) —
        🃏 로 단원을 고르고 옛 단추가 부르던 mcardSheet(날 F.SUB, 날 F.SUB) 를 직접 부른다(물리 TOC.sec[].name = 날 F.SUB · buildTocFromData) */
     const gh=$$$('#list [data-mc^="s:"]')[0];
     T('Y-2 단원 줄 「암기카드」는 🃏 칩이 갈음했다(🃏 있음 · 「암기카드」 단추 0)',!!gh&&$$$('#list .ghbtn').filter(x=>x.textContent.indexOf('암기카드')===0).length===0,gh&&gh.textContent);
     {const sub=(TOC.sec[gh.dataset.mc.slice(2)]||{}).name||''; mcardSheet(sub,sub);} await wait(400);
     T('Y-2 종전 꼴(.mcgrid)로 뜬다 · 종이 꼴 0건',$$$('.mcgrid').length===1&&$$$('.mcpaper').length===0);
     const pan=document.querySelector('.mcgrid').closest('.panel');   /* ⚠ 물리에도 다른 .sheet 이 있다 — 모아보기 판을 콕 집는다 */
     snap.sheet=pan.outerHTML; snap.cls=pan.className;
     /* ★ A-6(a) 9/30 — add16(genie 0bee72b · _decisions 2026-09-21 15:16 · 지시서 §0-2 옛 물리 시트 mcardSheet → §A-1 makeFloat · 수행 결과 표 mcardSheet 물리 ○)부터
        물리 모아보기도 떠 있는 창이다 → 판 class 에 float 가 붙고 모서리 손잡이가 하나 붙는다 · 안(.mcgrid · 글자 · 단추)은 종전 그대로 */
     T('Y-2 시트 껍데기가 종전 class(frmpanel) + 떠 있는 창(float · add16)',snap.cls==='panel frmpanel float',snap.cls);
     T('Y-2 떠 있는 창 손잡이가 하나 붙는다(add16 — 물리 모아보기도 떠 있는 창)',pan.querySelectorAll('.twgrip').length===1,pan.querySelectorAll('.twgrip').length);
     closeSheets();
   });
   await grp('Y-3', async()=>{
     /* 물리 카드 창은 크기를 기억하지 않는다 — jagwa.* 키가 안 생긴다 */
     const before=Object.keys(localStorage).filter(k=>k.indexOf('jagwa.win')===0);
     const no=DATA[0][F.NO];   /* ⚠ 물리 .item 에는 data-no 가 없다 */
     await openView(no); await wait(300); mcardWin(no); await wait(300);
     const p=document.querySelector('.mcwin .panel'), g=p.querySelector('.twgrip'), gr=g.getBoundingClientRect();
     PE('pointerdown',g,gr.left+5,gr.top+5);PE('pointermove',g,gr.left+90,gr.top+70);PE('pointerup',g,gr.left+90,gr.top+70);
     await wait(300);
     const after=Object.keys(localStorage).filter(k=>k.indexOf('jagwa.win')===0);
     T('Y-3 물리는 창 크기를 localStorage 에 안 적는다(세션 동안 WIN 만 · 종전 그대로)',after.length===before.length&&after.length===0,[before,after]);
     T('Y-3 그래도 모서리로 커지는 것은 종전대로 된다',!!WIN['mcard']&&WIN['mcard'].w>0,WIN['mcard']);
     document.querySelectorAll('.sheet').forEach(x=>{if(x.classList.contains('mcwin'))x.remove()});
     closeView(); await wait(80);
   });
   try{await __nativeFetch('/snap',{method:'POST',body:JSON.stringify(snap)})}catch(e){}
"""


# ── _task_qa_slim2(10/8 · J2) regress · smoke 도우미 — 이름이 `_rg` 로 시작하는 것 = gate 에서 안 쓰는 갈래(BODY_* 글은 글자 그대로) ──
#   쪽 안 고정 대기(MCALL 뒤 400 · 시트마다 400~2500 …)는 BODY 글 그대로(두 벌 안 둠) — 처리표 정리 거리(결정 거리 · _done.md)
def _rg_smoke_body(t):
    """smoke — 지학 BODY 에서 M-0 첫 칸 + 정의(MCALL · MK) + M-2 묶음 통째(모아보기가 종이 꼴로 열림 · 그린 칸 = 전 문항 — DOM 셈 · 렌더 한 번)만
    (원래 글을 그 자리에서 잘라 씀 · 못 찾으면 통째)"""
    a = t.find("   /* ═══ M-1 목록 머리 단추 ═══ */")
    m0 = t.find("   /* ═══ M-2 머리에서 열면 전 문항 ═══ */")
    m1 = t.find("   /* ═══ M-3 단원 줄에서 열면 그 절만 ═══ */")
    if min(a, m0, m1) < 0 or not (a < m0 < m1):
        print('NOTE | smoke 자르기 자리 못 찾음 — 통째로 돈다')
        return t
    return t[:a] + t[m0:m1]


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


def _cdp_do(prof, box, body):
    """★ _task_qa_fix1 §A-2(10/9) — 쪽이 /cdp 로 부른 진짜 입력 · op 'tap2' = 같은 자리 손가락 톡 둘(누름 hold ms · 사이 간격 gap ms 를 파이썬이 명령으로)
    크롬 = --remote-debugging-port=0 · 자리 = 프로필 DevToolsActivePort · 쪽 = /json/list 의 app.html · 웹소켓 = websocket-client(suppress_origin)
    돌려줌 = {ok, py(파이썬이 잰 두 손 뗌 사이 ms)} 또는 {ok: False, err} — 쪽이 앱이 본 간격(app)을 붙여 「다시 잼」을 가른다"""
    try:
        q = json.loads(body or '{}')
        if q.get('op') != 'tap2':
            return {'ok': False, 'err': 'op %r' % q.get('op')}
        if not box.get('ws'):
            import urllib.request
            import websocket
            port = None
            for _ in range(100):
                try:
                    port = int(open(os.path.join(prof, 'DevToolsActivePort'), encoding='utf-8').read().split()[0]); break
                except Exception:
                    time.sleep(0.1)
            tl = json.loads(urllib.request.urlopen('http://127.0.0.1:%d/json/list' % port, timeout=10).read().decode('utf-8'))
            t = next(x for x in tl if x.get('type') == 'page' and '/app.html' in x.get('url', ''))
            box['ws'] = websocket.create_connection(t['webSocketDebuggerUrl'], timeout=30, suppress_origin=True)
            box['cid'] = 0
        ws = box['ws']

        def cmd(method, params):
            box['cid'] += 1
            i = box['cid']
            ws.send(json.dumps({'id': i, 'method': method, 'params': params}))
            while True:
                m = json.loads(ws.recv())
                if m.get('id') == i:
                    if 'error' in m:
                        raise RuntimeError(json.dumps(m['error'], ensure_ascii=False))
                    return m.get('result')
        x, y = float(q['x']), float(q['y'])
        gap, hold = float(q.get('gap', 70)), float(q.get('hold', 30))
        pt = {'x': x, 'y': y, 'radiusX': 2, 'radiusY': 2, 'force': 1, 'id': 1}
        ts = []
        for k in range(2):
            if k:
                time.sleep(gap / 1000.0)
            cmd('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [pt]})
            time.sleep(hold / 1000.0)
            cmd('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
            ts.append(time.time())
        return {'ok': True, 'py': round((ts[1] - ts[0]) * 1000)}
    except Exception as e:
        return {'ok': False, 'err': repr(e)[:200]}


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
            # 옛 줄: body = self.rfile.read(n).decode('utf-8', 'replace'); self.send_response(204); self.end_headers()
            body = self.rfile.read(n).decode('utf-8', 'replace')
            if self.path.startswith('/cdp'):   # ★ _task_qa_fix1 §A-2(10/9) — 쪽이 부른 진짜 입력(N-5 두 번 톡) · 결과 JSON 을 돌려준다
                out = json.dumps(_cdp_do(prof, box, body), ensure_ascii=False).encode('utf-8')
                self.send_response(200); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(out)))
                self.end_headers(); self.wfile.write(out); return
            self.send_response(204); self.end_headers()
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
    # 옛 줄: p = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--user-data-dir=' + prof,
    # 옛 줄:                       '--window-size=1400,900', 'http://127.0.0.1:%d/app.html' % port],
    # 옛 줄:                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--user-data-dir=' + prof,
                          '--window-size=1400,900', '--remote-debugging-port=0',   # ★ _task_qa_fix1 §A-2(10/9) — N-5 두 번 톡 CDP 진짜 입력(_cdp_do) · 자리 = 프로필 DevToolsActivePort
                          'http://127.0.0.1:%d/app.html' % port],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 옛 줄: got = done.wait(secs); p.terminate()
    got = done.wait(secs)
    try:   # ★ _task_qa_fix1 §A-2 — CDP 웹소켓(있으면) 닫고 크롬을 끈다
        if box.get('ws'): box['ws'].close()
    except Exception: pass
    p.terminate()
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
    T2('S-1 두 단추 마크업·물리 제거 줄 무접촉',
       '<button class="chip" id="btnRand">랜덤으로 풀기</button>' in s
       and '<button class="chip" id="btnFirst">처음부터 풀기</button>' in s
       and "if(!CARD_LAYER){['btnRand','btnFirst'].forEach(id=>{const b=document.getElementById(id);if(b)b.remove()})}" in s)
    T2('S-2 새 단추를 만드는 코드는 카드 층 블록 안이다(9/21 부터 if(SHELL) · c9faff2 §A)',
       blk >= 0 and s.find("mb.id='btnMC'") > blk and s.count("mb.id='btnMC'") == 1)
    T2('S-3 비-JG(물리·생물) 모아보기 본문이 글자까지 그대로',
       '<div class="mcgrid"${JG?` style="grid-template-columns:repeat(auto-fill,minmax(${cw}px,1fr))"`:\'\'}>' in s
       and '<div class="panel frmpanel"><h2>암기카드 — ${esc(label)}</h2><p>${JG?' in s
       and '카드 없음 · 문제에서 「암기카드」' in s)
    T2('S-4 종이 꼴은 JG 갈래에서만 부른다',
       s.count('if(JG)paperFill(qs,bar);') == 1 and s.count('const paperFill=') == 1
       and s.count("if(JG)makeFloat(b,b.querySelector('h2'),'mcsheet','jagwa.win.mcsheet');") == 1)
    T2('S-5 물리 makeFloat 호출 넷은 인자 셋 그대로',
       all(x in s for x in ["makeFloat(b,b.querySelector('h2'),'twin');",
                            "makeFloat($('#sub'),$('#sub .shead'),'sub');",
                            "makeFloat($('#bkq'),$('#bkq .bkqh'),'bklist');",
                            "makeFloat($('#snw'),$('#snw .shead'),'snote');"]))
    T2('S-6 카드 창만 CARD_LAYER 일 때 pkey 를 준다',
       "makeFloat(b,b.querySelector('h2'),'mcard',CARD_LAYER?'jagwa.win.mcard':null);" in s)
    T2('S-7 mcard 저장 꼴·MC_MAX·조각 좌표표 무접촉',
       'const MC_MAX=20000;' in s and "const saveMC=()=>put('kv','mcard',MC);" in s
       and "JOGAK_PATH:'earth/조각.json', OMR_PATH:'earth/omr2.pdf'," in s
       and 'var jogakAR=cell=>{const [x0,y0,x1,y1]=cell.r;return (x1-x0)/(y1-y0)};' in s)
    # add3 — 손잡이의 뜻이 「칸 크기(px)」에서 「열당 칸 수」로 바뀌었다(고친 자리).
    #   같은 값이면 창 크기와 무관하게 배치가 같아지는 것이 이 판의 목적이다.
    T2('S-8 손잡이가 「열당 칸 수」다 — 범위 8~20 · 기본 12(종이 실측)',
       'id="mcW" min="${NPC_MIN}" max="${NPC_MAX}" step="1"' in s
       and 'NPC_DEF=12, NPC_MIN=8, NPC_MAX=20' in s
       and 'if(n>=NPC_MIN&&n<=NPC_MAX)npc=Math.round(n)' in s
       and "let mode=JG?'unit':'no', cw=JG?170:0;" in s)
    T2('S-12 배치·배율·상수가 한자리에 박혀 있다(PAPER_AR·CPP·최소 칸·문턱·상한)',
       'const PAPER_AR=1.732, CPP=11,' in s and 'CARDH_MIN=34, FONT_MIN=7' in s
       and 'ZMIN=0.35, ZMAX=3, ZBG=0.6' in s and 'const BGCAP=260, ROOTM=250;' in s)
    T2('S-13 확대는 transform 만 쓴다 — 칸 크기·좌표를 다시 계산하지 않는다',
       "zbox.style.transform='scale('+zoom+')'" in s and s.count('.mcz') >= 1
       and 'ZOOMRECALC' not in s)
    T2('S-14 쪽 바로가기·확대축소 단추를 안 만들었다',
       'mcPgBtn' not in s and 'mcZoomIn' not in s and 'id="mcZ100"' not in s)
    T2('S-9 SET 에 창 크기를 안 넣는다 — 키는 jagwa. 접두사',
       "'jagwa.win.mcsheet'" in s and "'jagwa.win.mcard'" in s and 'SET.mcsheet' not in s and 'SET.mcwin' not in s)
    T2('S-10 확대 엔진(zWire)을 카드 창에 안 붙였다 — 부르는 자리 넷이 add1 그대로',
       s.count('zWire(') == 4 and 'zWire(MCZ' not in s
       and s[s.find('function mcardWin('):s.find('function mcardSheet(')].find('zWire') < 0
       and s[s.find('function mcardSheet('):s.find('function mcardPop(')].find('zWire') < 0, s.count('zWire('))
    T2('S-11 백틱 짝', s.count('`') % 2 == 0)
    return out


def main():
    want = [a for a in sys.argv[1:] if a in ('earth', 'bio', 'phys')] or ['earth', 'bio', 'phys']
    if QC.SMOKE:   # smoke — 지학 한 판(M-0 · M-2 모아보기 종이 꼴 · 콘솔 오류 0)만 · bio · phys · physbase 건넘
        want = ['earth']
    cur = open(SRC, encoding='utf-8', newline='').read()
    lines = []
    for mode in want:
        secs = int(os.environ.get('HARNESS_WAIT', '420'))
        ls, snap = run(mode, secs, cur)
        lines += ls
        if mode == 'phys' and QC.GATE:   # regress — 바탕(physbase · git show HEAD 블롭) 띄움 0 → 아래 _rg_phys_same(기준 스냅샷)
            QC.sub('git:show-app')
            base = subprocess.run(['git', '-C', GENIE, 'show', 'HEAD:jagwa/index.html'],
                                  capture_output=True).stdout.decode('utf-8')
            ls0, snap0 = run('physbase', secs, base.replace('\n', '\r\n') if '\r\n' not in base else base)
            def T2(name, cond, info=''):
                lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))
            T2('Y-4 고침 전(HEAD 블롭) 판도 끝까지 돌았다', bool(snap and snap0), [bool(snap), bool(snap0)])
            if snap and snap0:
                for k, ko in (('brand', '머리 칩 줄'), ('list', '목록'), ('cnt', '문항 수'), ('sheet', '모아보기 시트')):
                    T2('Y-4 물리 %s 이(가) 고침 전과 글자까지 같다' % ko, snap.get(k) == snap0.get(k),
                       [len(str(snap.get(k))), len(str(snap0.get(k)))])
        if mode == 'phys' and not QC.GATE:   # regress — Y-4 물리 무변 칸 = 기준 스냅샷(QC.base) · 「Y-4 고침 전(HEAD 블롭) 판도 끝까지 돌았다」(관문만 · 바탕 띄움 건강) 끔
            _y4 = _rg_phys_same(snap, 'Y-4', (('brand', '머리 칩 줄'), ('list', '목록'), ('cnt', '문항 수'), ('sheet', '모아보기 시트')))
            if 'window.G3=' in cur:   # ★ 2026-10-09 _task_jagwa_gg3 §A-4(물리 첫 화면 · 항목 줄 · 머리 꼴) — 물리 화면을 바꾼 판이라 「물리 무변」 칸은 값 그대로 INFO(옛 줄: lines += _rg_phys_same(…))
                _y4 = [('INFO' + x[4:] + ' | gg3 갈음(§A-4 물리 화면 꼴 바뀜)') if x.startswith('FAIL') else x for x in _y4]
            lines += _y4
    if QC.want('src'):   # smoke — 브라우저 밖 소스 칸(S-*)은 smoke 칸이 아니다
        lines += static_checks()
    # 옛 줄: npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
    npass = sum(1 for x in lines if x.startswith('PASS')); nfail = sum(1 for x in lines if x.startswith('FAIL'))   # ★ 2026-10-09 gg3 — INFO 줄은 FAIL 로 안 셈
    for x in lines: print(x)
    print('\n== 암기카드/종이 모아보기 %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
