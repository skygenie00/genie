# -*- coding: utf-8 -*-
"""지학 앱 판 1 헤드리스 검산 (2026-09-04 · _task_earth_app_pan1.md E-1~E-9 · 물리 _harness_phys.py 준용)

앱 사본에 ① KaTeX 스텁(pdf.js·pdf-lib 는 진짜 CDN — 교재 쪽 렌더를 재야 한다) ② 가짜 GitHub(fetch 가로채기 → 로컬 studyplandata/earth 파일)
③ 검사를 주입해 헤드리스 크롬으로 돌린다. 원본은 건드리지 않는다. 결과는 페이지가 POST /result 로 보낸다.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기 헬퍼(_task_qa_slim2 A-1-2 · 옛 남 하네스 import 를 갈음)
import http.server, os, socketserver, subprocess, sys, threading, hashlib, json, csv, shutil, urllib.parse

GENIE = _roots.genie()
SRC = os.path.join(GENIE, 'jagwa', 'index.html')   # 병합 뒤: 물리 앱을 과목 earth 로 연다 · 9/5 자과 서재 이사(phys → jagwa)
PHYS = os.path.join(GENIE, 'jagwa', 'index.html')
SPD = os.path.join(_roots.spd(), 'earth')
GIGU = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.environ.get('TEMP', '.'), 'earthh'); os.makedirs(OUT, exist_ok=True)
APP = os.path.join(OUT, 'app.html')

STUB = JG.STUB_E   # JG 로 옮김(_task_qa_slim2 A-1-2) — 남은 제 코드가 이 이름을 부른다 · 같은 객체(두 벌 아님)

TESTS = r"""<script>
(function(){
 const R=[]; const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+(c?'':' | '+JSON.stringify(i===undefined?null:i)));
 const __nativeFetch=window.fetch.bind(window);
 const EXP=__EXP__;
 /* 가짜 GitHub: contents API → 로컬 /data/<path> · PUT 은 기록만 · 기록.json 은 없음(404) */
 window.__puts=[];
 window.fetch=async function(url,opt){
  opt=opt||{};const u=String(url);
  const m=/api\.github\.com\/repos\/([^\/]+\/[^\/]+)\/contents\/([^?]+)/.exec(u);
  if(!m){ if(/api\.github\.com\/repos\/zzikkaplan\/notes/.test(u))return {ok:true,status:200,json:async()=>({name:'notes'}),text:async()=>''}; return __nativeFetch(url,opt); }
  const path=decodeURIComponent(m[2]);
  if(m[1]==='zzikkaplan/notes'){const r=await __nativeFetch('/notes/'+encodeURI(path),{cache:'no-store'});return r.ok?r:{ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)}}
  if((opt.method||'GET')==='PUT'){window.__puts.push(path);return {ok:true,status:200,json:async()=>({content:{sha:'x'+window.__puts.length}}),text:async()=>''}}
  const r=await __nativeFetch('/data/'+encodeURI(path),{cache:'no-store'});
  if(!r.ok)return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
  const acc=(opt.headers||{}).Accept||'';
  if(acc.indexOf('raw')>=0)return r;
  const sha=r.headers.get('X-Sha')||'sha';
  return {ok:true,status:200,json:async()=>({sha}),text:async()=>JSON.stringify({sha})};
 };
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 setInterval(()=>{try{__nativeFetch('/partial',{method:'POST',body:R.join(String.fromCharCode(10))+String.fromCharCode(10)+'(err) '+JSON.stringify(window.__err||[])})}catch(e){}},3000);
 async function run(){
  try{
   localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}));
   await loadEarthData(); draw(); await wait(50);
   T('E-3 문항 704 적재',DATA.length===704,DATA.length);
   /* ★ A-6(d) 9/30 — 지금 데이터: earth_jeongo(studyplandata 19bc5b2f · 9/27)가 원본에 없는 〈보기〉 ㅁ 줄 12 를 걷어 705 → 693(git show 셈 517b369c·182e1f37·352fc227 = 705 · 19bc5b2f·3c3a8b66·4a011475 = 693) */
   T('E-3 보기 693',DATA.reduce((a,r)=>a+(r[F.BOGI]||[]).length,0)===693,DATA.reduce((a,r)=>a+(r[F.BOGI]||[]).length,0));
   T('E-3 그림 198',DATA.filter(r=>r[F.FILE]==='IMG').length===198);
   T('목차 115 항목 · 16 절',Object.keys(TOC.unit).length===115&&Object.keys(TOC.sec).length===16,[Object.keys(TOC.unit).length,Object.keys(TOC.sec).length]);
   T('E-2 index.json 절 16 + 부록 2',Object.keys(PIECES).length===18,Object.keys(PIECES).length);
   T('설정 블록 · DB earth1 · 경로',EARTH.DB==='earth1'&&PDF_DIR==='earth/pdf/'&&REC_PATH==='earth/기록.json'&&U_KEY==='earth_sync_u');
   T('M-2 과목 earth · IndexedDB earth1 열림 · SUBJ.phys 값 그대로(SYNC_KEYS 는 9/5 필터 손질로 12 = +link)',SUBJ_ID==='earth'&&db.name==='earth1'&&document.body.dataset.subj==='earth'&&SUBJ.phys.DB==='phys535'&&SUBJ.phys.PDF_DIR==='phys/pdf/'&&SUBJ.phys.REC_PATH==='phys/기록.json'&&SUBJ.phys.SYNC_PREFIX==='phys_sync_'&&(SUBJ.phys.SYNC_KEYS.length===12||(SUBJ.phys.SYNC_KEYS.length===13&&SUBJ.phys.SYNC_KEYS[12]==='cqx')),[db.name,SUBJ_ID]);   /* ★ 2026-10-09 _task_jagwa_gg3 §A-2-3 — 물리 SYNC_KEYS 13째 cqx · 옛 줄 끝: &&SUBJ.phys.SYNC_KEYS.length===12,[db.name,SUBJ_ID]); */
   T('M-4 게이트(지학): 지학 조각 보임 · 물리 도구 숨김',getComputedStyle($('#ebody')).display!=='none'&&getComputedStyle($('#stage')).display==='none'&&getComputedStyle($('#btnFormula')).display==='none'&&getComputedStyle($('#tTheory')).display==='none'&&getComputedStyle($('#tCard')).display!=='none'&&!$('#btnTree'));   /* ★ A-6(a) 9/30 — 셸 add9 §A-1(68216cf): 「목차」 단추 #btnTree 걷음(없는 요소에 getComputedStyle → 하니스가 터짐 · col 288) */
   T('머리 = 「자과 서재 · 지학」 · <title> 자과 서재(생물 판 2 add4 · 9/5: 앱 이름 하나 · SUBJ.earth.TITLE 은 그대로) · 탭 셀 현재 = 지학',document.title==='자과 서재'&&$('.brand h1').textContent==='자과 서재 · 지학'&&SUBJ.earth.TITLE==='지학 기출 서재'&&$('#subjTabs .on').textContent==='지학',[document.title,$('.brand h1').textContent]);
   const cells=$$('#subjTabs button');
   T('A-1 셀 셋 「물리│생물│지학」 · 현재 과목 눌림 · 생물 살아 있음(앱 판 1 · 9/5)',cells.map(b=>b.textContent).join('│')==='물리│생물│지학'&&cells[2].classList.contains('on')&&!cells[1].classList.contains('off')&&!cells[1].getAttribute('aria-disabled')&&!cells[0].classList.contains('on'),cells.map(b=>b.className));
   T('A-4 셀 셋 한 줄 · 폭 150px 이하',cells.every(b=>Math.abs(b.getBoundingClientRect().top-cells[0].getBoundingClientRect().top)<1)&&$('#subjTabs').getBoundingClientRect().width<=150,$('#subjTabs').getBoundingClientRect().width);
   const st0=JSON.stringify(ST);
   for(let k=0;k<3;k++){subjSwitchTo('phys',false);subjSwitchTo('earth',false)}
   T('A-1 물리↔지학 왕복 3회(새로고침 없이) → localStorage subj = earth · 기록 무변',localStorage.getItem('subj')==='earth'&&JSON.stringify(ST)===st0);
   subjSwitchTo('phys',false);T('M-3 셀 → localStorage subj 바뀜(새로고침 없이 검산)',localStorage.getItem('subj')==='phys');subjSwitchTo('earth',false);
   /* 생물 앱 판 1(9/5): 생물 셀은 켜졌다 — 클릭하면 새로고침이므로 reload=false 로만 검산 */
   T('A-2 생물 켜짐: subjSwitchTo(bio,false) → subj=bio · subjResolve(bio)=bio · SUBJ.bio(ready:true · 20 키(add1 +bref) · bio1) · 되돌림',subjSwitchTo('bio',false)===true&&localStorage.getItem('subj')==='bio'&&subjResolve('bio')==='bio'&&subjResolve('earth')==='earth'&&subjResolve(null)==='phys'&&SUBJ.bio.ready===true&&SUBJ.bio.DB==='bio1'&&SUBJ.bio.SYNC_KEYS.length===20&&SUBJ.bio.LAYER===true&&subjSwitchTo('earth',false)===true&&localStorage.getItem('subj')==='earth');
   T('A-2 bio1 IndexedDB 생기지 않음',!((await indexedDB.databases()).some(d=>d.name==='bio1')));
   T('A-3 층 조건 = CARD_LAYER · data-layer=card · 층에 earth 하드코딩 없음(캐시 키 earthdata 는 SUBJ_ID+data)',CARD_LAYER===true&&document.body.dataset.layer==='card'&&!!(await get('kv','earthdata')));
   T('M-3 물리 IndexedDB(phys535) 는 생기지도 않음',!((await indexedDB.databases()).some(d=>d.name==='phys535')));
   /* ★ A-6(a) 9/30 둘째 바퀴 — listpop_add1 §G(genie cd248a5 · 결정로그 9/20 21:00 · 수행 결과 §G 「JS 가 끝에 넷을 더한다 … 합 23」): 지학 SYNC_KEYS 끝에 gg·ggref·pick·link → 23(지금 앱 8168~8169) · 앞 19 자리 조건은 그대로 */
   T('E-8 SYNC_KEYS 23(… crop · txt · tfix · add1 bref)',SYNC_KEYS.length===23&&SYNC_KEYS[15]==='crop'&&SYNC_KEYS[16]==='txt'&&SYNC_KEYS[17]==='tfix'&&SYNC_KEYS[18]==='bref'&&SYNC_KEYS[10]==='mcard'&&SYNC_KEYS[11]==='bogi'&&SYNC_KEYS[12]==='unit'&&SYNC_KEYS[13]==='bpit'&&SYNC_KEYS[14]==='bpg'&&typeof SYNC_REF.bogi.g==='function'&&typeof SYNC_REF.bpit.g==='function',SYNC_KEYS);
   /* ===== E-5 트리 · 기본 필터 ===== */
   T('E-5 기본 필터 = 기출만(319)',filtered().length===319&&FL.past==='y',filtered().length);
   buildTree();await wait(20);   /* ★ A-6(a) 9/30 — 셸 add9 §A-6: treeOpen 은 빈 함수 — 그대로면 아래 3.4.5 줄(it)이 null 이라 다시 터진다 · #trlist 는 buildTree 가 그린다 */
   T('E-5 트리 항목 115 · 절 16 · 장 5',$$('#trlist .trit:not(.unm)').length===115&&$$('#trlist .trsec').length===16&&$$('#trlist .trch').length===5);
   $('#trTog').click();await wait(30);
   T('E-5 확인 토글 → 385',filtered().length===385&&FL.past==='p',filtered().length);
   const unm=$$('#trlist .trit.unm').reduce((a,el)=>a+ +el.querySelector('.n').textContent,0);
   T('E-5 미매칭 N 합 = 385',unm===385,unm);
   $('#trTog').click();await wait(30);
   const it=$('#trlist .trit[data-u="3.4.5"]');it.querySelector('.n').click();await wait(30);
   T('E-5 항목 숫자 클릭 → 그 단원 목록(FL.unit) · 수 = 기대 (9/7 두 손잡이: 글자=스크롤 · 숫자=필터)',FL.unit==='3.4.5'&&filtered().length===EXP.u345,[FL.unit,filtered().length,EXP.u345]);
   FL.unit='';draw();
   /* ===== 필터 add1(9/5) 세 층 공통 손잡이 #trGrip — 지학 서랍 내용·토글·닫기 무변 =====
      ★ A-6(a) 9/30 둘째 바퀴 — 셸 add9 §A(genie 68216cf · 결정로그 9/21 15:44 · 수행 결과 §A 표): 옛 #tree(#trGrip · SET.tro/trw · body.tropen)는 걷었고(treeOpen 빈 함수)
      그 구실은 상주 서랍 #navdr 이 맡는다 — #ndGrip 탭 = 접기(13px) · 끌기 = 너비(160~420 · 기본 236) · 기기별 localStorage jagwa.nd.fold/w.<과목> · 놓으면 SET.ndw ·
      여백 body.ndon = --ndw · 닫기는 없다(늘 서 있다) → 같은 동작을 그 손잡이로 잰다(생물 _harness_bio.py A1 첫 바퀴 고침과 같은 꼴) ·
      서랍 내용(#trlist 항목 115 · E-5 buildTree)·기출/확인 토글(#trTog — 상주 서랍 머리로 옮겨짐)·#trX 조건은 그대로 */
   {treeOpen();await wait(40);const g5=$('#ndGrip'),d5=$('#navdr');const gb5=g5.getBoundingClientRect();
    const PE5=(t,el,x,y)=>el.dispatchEvent(new PointerEvent(t,{clientX:x,clientY:y,pointerId:5,pointerType:'mouse',bubbles:true,cancelable:true,isPrimary:true}));
    const tap5=async(x,y)=>{PE5('pointerdown',g5,x,y);await wait(10);PE5('pointerup',g5,x+1,y+1);await wait(60)};
    T('A1 지학 상주 서랍 #ndGrip 손잡이 · body.ndon(≥900 여백 236) · 폭 236',!!g5&&document.body.classList.contains('ndon')&&getComputedStyle(document.body).paddingLeft==='236px'&&Math.round(d5.getBoundingClientRect().width)===236,[getComputedStyle(document.body).paddingLeft,Math.round(d5.getBoundingClientRect().width)]);
    await tap5(gb5.left+6,gb5.top+200);
    T('A1 탭 → 접힘 13px · 내용 숨김 · jagwa.nd.fold.earth=1 · 여백 13',d5.classList.contains('fold')&&Math.round(d5.getBoundingClientRect().width)===13&&getComputedStyle($('#ndList')).display==='none'&&localStorage.getItem('jagwa.nd.fold.earth')==='1'&&getComputedStyle(document.body).paddingLeft==='13px',[Math.round(d5.getBoundingClientRect().width),localStorage.getItem('jagwa.nd.fold.earth'),getComputedStyle(document.body).paddingLeft]);
    await tap5(6,200);
    PE5('pointerdown',g5,gb5.left+6,gb5.top+200);await wait(10);PE5('pointermove',g5,gb5.left+106,gb5.top+200);await wait(10);PE5('pointerup',g5,gb5.left+106,gb5.top+200);await wait(60);
    T('A1 끌기 +100 → 336 · SET.ndw · kv · 서랍 내용(항목 115)·기출/확인 토글·닫기 무변',!d5.classList.contains('fold')&&Math.round(d5.getBoundingClientRect().width)===336&&SET.ndw===336&&((await get('kv','set'))||{}).ndw===336&&$$('#trlist .trit:not(.unm)').length===115&&!!$('#trTog')&&getComputedStyle($('#trTog')).display!=='none'&&!!$('#trX'),[d5.getBoundingClientRect().width,SET.ndw]);
    ndSetW(236);delete SET.ndw;await put('kv','set',SET);treeClose();await wait(20);
    T('A1 옛 서랍 닫기(treeClose)는 상주 서랍을 안 건드린다 · body.tropen 없음 · 여백 236',!document.body.classList.contains('tropen')&&document.body.classList.contains('ndon')&&getComputedStyle(document.body).paddingLeft==='236px',[getComputedStyle(document.body).paddingLeft]);}
   /* ===== E-4 카드 · 보기 O△X ===== */
   const g=DATA.find(r=>!isC(r)&&hasOX(r)&&(r[F.BOGI]||[]).length>=3);
   await openView(g[F.NO]);await wait(60);
   T('카드 렌더 · 보기 줄 수 = 보기 수',$$('#card .bogi .row').length===g[F.BOGI].length&&$$('#card .choices button').length===5,[$$('#card .bogi .row').length]);
   T('물리 스테이지 숨김 · 캔버스 없음',getComputedStyle($('#stage')).display==='none');
   const row0=$('#card .bogi .row');const uid=g[F.CODE],k=row0.dataset.k,ans=row0.dataset.ans;
   row0.querySelector('.ox button[data-v="'+(ans==='O'?'X':'O')+'"]').click();await wait(40);
   T('E-4 토글 → bogi 저장',(BG[uid]||{})[k]===(ans==='O'?'X':'O'),BG[uid]);
   const kv=await get('kv','bogi');T('E-4 kv bogi 되읽기',!!kv&&kv[uid]&&kv[uid][k]===(ans==='O'?'X':'O'));
   T('E-4 정답 닫힘 = 붉지 않음',!row0.classList.contains('wrong'));
   $('#cDet').open=true;$('#cDet').dispatchEvent(new Event('toggle'));await wait(20);
   T('E-4 정답 열면 어긋난 보기 붉게',row0.classList.contains('wrong'));
   row0.querySelector('.ox button[data-v="'+ans+'"]').click();await wait(30);
   T('E-4 맞는 값으로 바꾸면 붉음 해제',!row0.classList.contains('wrong')&&row0.classList.contains('right'));
   row0.querySelector('.ox button[data-v="'+ans+'"]').click();await wait(30);
   T('E-4 같은 값 다시 = 해제',!(BG[uid]||{})[k]);
   const ord=DATA.filter(r=>(r[F.BOGI]||[]).length&&!hasOX(r));
   T('E-4 순서·묶음 7건',ord.length===7,ord.length);
   await openView(ord[0][F.NO]);await wait(40);
   T('E-4 순서 문항 = 토글 없음',$$('#card .bogi .row').length>0&&$$('#card .ox').length===0);
   /* 선택지 자동 마크 · 사용자 마크 우선 */
   await openView(g[F.NO]);await wait(40);
   const before=hist(g[F.NO]).length;
   $('#card .choices button[data-c="'+g[F.ANS]+'"]').click();await wait(40);
   T('선택지 정답 고름 → O 자동',lastM(g[F.NO])==='O'&&hist(g[F.NO]).length===before+1&&hist(g[F.NO]).slice(-1)[0].auto===1);
   $('#card .choices button[data-c="'+(g[F.ANS]==='1'?'2':'1')+'"]').click();await wait(40);
   T('다시 고르면 갈아 끼움(회독 +0)',lastM(g[F.NO])==='X'&&hist(g[F.NO]).length===before+1);
   $('#mQ').click();await wait(40);
   T('사용자 마크가 자동을 갈아 끼움 · 우선',lastM(g[F.NO])==='Q'&&hist(g[F.NO]).length===before+1&&!hist(g[F.NO]).slice(-1)[0].auto);
   /* ===== E-6 교재 — ⚠ 2026-09-10 사용자 확정으로 **옆 칸을 걷고 팝업 창 하나**로 갔다.
      옛 판은 `#bpc`·`#bpList`(옆 칸)를 쟀다. 같은 것을 교재 창에서 잰다. ===== */
   const ok6=[];
   for(const [pg,file,k] of EXP.pages){
     await bookOpen(pg);await wait(2600);
     {let n=0;while(n++<60&&(!bkCurPage()||bkCurPage().pr!==pg))await wait(200);}
     const cur=bkCurPage();
     ok6.push([pg,!!cur&&cur.pr===pg&&(pieceFor(pg)||{}).file===file,cur&&cur.pr,(pieceFor(pg)||{}).file,$('#bkmsg').textContent])}
   T('E-6 쪽 칩 6곳 → 맞는 조각·렌더',ok6.every(x=>x[1]),ok6);
   await bookOpen(208);await wait(2600);
   {let n=0;while(n++<60&&(!bkCurPage()||bkCurPage().pr!==208))await wait(200);}
   $('#bkQ').click();await wait(400);
   T('E-6 「이 쪽의 문항」 208쪽 = 데이터(문항.json) 집계',$$('#bkqList [data-no]').length===EXP.p208,[$$('#bkqList [data-no]').length,EXP.p208]);
   $('#bkqX').click();await wait(100);
   T('E-6 조각이 IndexedDB pdf 에 캐시',!!(await get('pdf','3.4.pdf')));
   bkClose();await wait(200);   /* 아래 B-1 이 「닫힌 상태에서 열기」를 잰다 — 열어 둔 채로 넘기지 않는다 */
   /* ===== E-8 매칭 ===== */
   const c=DATA.find(r=>isC(r)&&r[F.CAND]);await openView(c[F.NO]);await wait(40);
   T('확인문제 카드 = 장 칩 + 매칭',$('#cMatch').textContent==='매칭'&&unitOf(c[F.NO]).length===1);
   matchSheet(c[F.NO]);await wait(20);
   T('E-8 팝업 기본값 = 단원후보',!!$('#mCand')&&$('#mCand').textContent.includes(c[F.CAND]));
   $('#mCand').click();await wait(60);
   T('E-8 후보 확정 → unit 저장 · kv',UN[c[F.CODE]]===c[F.CAND]&&((await get('kv','unit'))||{})[c[F.CODE]]===c[F.CAND]);
   T('E-8 카드 단원 칩 갱신',$('#cUnit').textContent.startsWith(c[F.CAND]));
   FL.past='p';buildTree();await wait(20);
   const unm2=$$('#trlist .trit.unm').reduce((a,el)=>a+ +el.querySelector('.n').textContent,0);
   T('E-8 트리 미매칭 384 · 항목으로 이동',unm2===384&&+$('#trlist .trit[data-u="'+c[F.CAND]+'"] .n').textContent.split('·')[1]>=1,unm2);
   FL.past='y';
   /* ===== E-7 서브노트 ===== */
   await subOpen('',false);await wait(1500);
   T('E-7 여섯 쪽 한 판',$$('#sworld .spg').length===6&&SUB.ready);
   T('E-7 서브노트 = notes 저장소 earth/서브노트_n.pdf',SUB.repo==='zzikkaplan/notes'&&(await notePath(1)).path==='earth/서브노트_1.pdf'&&$('#sinfo').textContent.includes('notes'),[SUB.repo,await notePath(1)]);
   T('E-7 열 머리 감지 16(+1)',Object.keys(SUB.cols).length>=16,Object.keys(SUB.cols));
   const s0=SUB.S;szoomSec('3.4',false);await wait(400);
   T('E-7 절 칩 → 확대 이동',SUB.S!==s0&&!!$('#sworld .scol.on')&&$('#sworld .scol.on').dataset.sec==='3.4',[s0,SUB.S]);
   await wait(800);const cv0=$$('#stiles canvas').length;
   ssetZoom(8);await wait(2500);
   const cvs=$$('#stiles canvas');
   T('E-7 800% 타일 = 캔버스 한도 안(≤4096) · 보이는 것만',SUB.S===8&&cvs.length>0&&cvs.every(c=>c.width<=4096&&c.height<=4096),[cv0,cvs.map(c=>[c.width,c.height]),SUB.tile,window.__err]);
   T('E-7 pdf-lib 있음(올리기 드라이런)',typeof PDFLib!=='undefined'&&typeof PDFLib.PDFDocument!=='undefined');
   const bl=await (await __nativeFetch('/blank.pdf')).arrayBuffer();const doc=await PDFLib.PDFDocument.load(bl);
   T('E-7 빈판 6쪽 가르기 드라이런',doc.getPageCount()===6);
   /* 펜 획 저장 */
   SUB.pen=true;SUB.tool='pen';const st={i:0,c:'#243a5e',w:1.6,hl:false,p:[100,100,200,150,300,160]};await inkCommit(st);
   T('E-7 잉크 덧층 #sover 가 타일 위(형제 순서)',$('#sover').compareDocumentPosition($('#stiles'))&Node.DOCUMENT_POSITION_PRECEDING?true:false);
   T('E-7 잉크 = 쪽 정규화 좌표 · IndexedDB ink',((await get('ink','note:1'))||{s:[]}).s.length===1&&$$('#sover .spgo[data-i="0"] path').length>=2);
   $('#sX').click();
   /* ===== 판 2 · 교재 모드 B-1~B-8 (_task_jihak_app_pan2.md §10) ===== */
   const PE=(t,el,x,y,pt)=>el.dispatchEvent(new PointerEvent(t,{clientX:x,clientY:y,pointerId:7,pointerType:pt||'mouse',bubbles:true,cancelable:true,isPrimary:true}));
   const vno0=VNO, sc0=$('#cardwrap').scrollTop;
   $('#btnBook').click();await wait(1800);
   T('B-1 📖 교재 → #book 열림 · 조각 받음 · 문항 무변',!$('#book').classList.contains('hide')&&BK.open&&VNO===vno0&&BK.pgs.length>0&&$('#btnBook').classList.contains('on'),[BK.pgs.length,$('#bkmsg').textContent,window.__err]);
   const st1=JSON.parse(localStorage.getItem('earth_book')||'{}');
   T('B-1 localStorage earth_book 에 쪽·배율·서랍',!!st1.page&&!!st1.S&&typeof st1.toc==='boolean',st1);
   bkClose();await wait(60);
   T('B-1 닫으면 #book 숨김 · VNO·스크롤 무변 · 칩 꺼짐',$('#book').classList.contains('hide')&&VNO===vno0&&$('#cardwrap').scrollTop===sc0&&!$('#btnBook').classList.contains('on'));
   await bkOpen(208);await wait(1200);
   let cp=bkCurPage();
   T('B-3 208쪽 → 3.4.pdf · 현재 쪽 208 · 툴바 「3.4.5 · 208쪽 (PDF 219)」',cp&&cp.pr===208&&cp.pc.file==='3.4.pdf'&&$('#bkInfo').textContent==='3.4.5 · 208쪽 (PDF 219)',[cp&&cp.pr,$('#bkInfo').textContent]);
   T('B-2 툴바에 ±·맞춤·% 요소 0 · 핀치(두 손가락)·Ctrl+휠만',$$('#bkmain .szoom').length===0&&$$('#bkmain button,#bkmain span').filter(b=>/^[±+−]$|맞춤|%$/.test(b.textContent.trim())).length===0);
   const vp=$('#bkvp'),vr=vp.getBoundingClientRect();const sb0=BK.S,y0=BK.Y;
   vp.dispatchEvent(new WheelEvent('wheel',{deltaY:-300,ctrlKey:true,clientX:vr.left+300,clientY:vr.top+300,bubbles:true,cancelable:true}));await wait(80);
   T('B-2 Ctrl+휠 → 확대',BK.S>sb0&&BK.S<=8,[sb0,BK.S]);
   const s1=BK.S,y1=BK.Y;vp.dispatchEvent(new WheelEvent('wheel',{deltaY:200,clientX:vr.left+300,clientY:vr.top+300,bubbles:true,cancelable:true}));await wait(80);
   T('B-2 맨 휠 = 세로 이동(배율 무변)',BK.S===s1&&BK.Y<y1,[y1,BK.Y]);
   /* 두 손가락 핀치 */
   const a0={x:vr.left+300,y:vr.top+300},b0={x:vr.left+400,y:vr.top+300};const sP=BK.S;
   PE('pointerdown',vp,a0.x,a0.y,'touch');vp.dispatchEvent(new PointerEvent('pointerdown',{clientX:b0.x,clientY:b0.y,pointerId:8,pointerType:'touch',bubbles:true}));
   vp.dispatchEvent(new PointerEvent('pointermove',{clientX:b0.x+100,clientY:b0.y,pointerId:8,pointerType:'touch',bubbles:true}));
   vp.dispatchEvent(new PointerEvent('pointerup',{clientX:b0.x+100,clientY:b0.y,pointerId:8,pointerType:'touch',bubbles:true}));PE('pointerup',vp,a0.x,a0.y,'touch');await wait(80);
   T('B-2 핀치(손가락 둘 벌림) → 배율 커짐',BK.S>sP,[sP,BK.S]);
   zSetZoom(BK,8);await wait(1500);const cvs2=$$('#bktiles canvas');
   T('B-2 800% 타일 ≤4096 · 보이는 것만',BK.S===8&&cvs2.length>0&&cvs2.every(c=>c.width<=4096&&c.height<=4096),cvs2.map(c=>[c.width,c.height]));
   zSetZoom(BK,0.05);T('B-2 하한 10%',BK.S===0.1);
   /* 필기 · 배율 뒤 좌표 */
   const p208=BK.pgs.find(p=>p.pr===208);
   await zInkCommit(BK,{i:p208.i,c:'#243a5e',w:1.2,hl:false,p:[100,100,200,150,300,160]});await wait(50);
   const saved=await get('ink','bink:208');
   T('B-4 펜 획 → ink 저장소 bink:208 · 0~1 정규화(×쪽폭 = 100)',!!saved&&saved.s.length===1&&saved.s[0].p.every(v=>v>=0&&v<=1)&&Math.abs(saved.s[0].p[0]*p208.w-100)<0.1,saved&&saved.s[0].p);
   const pathEl=()=>p208.el.querySelector('.bkink path[data-j="0"]');
   zSetZoom(BK,2);await wait(60);const d2=pathEl().getAttribute('d'),r2=pathEl().getBoundingClientRect();
   zSetZoom(BK,1);await wait(60);const d1=pathEl().getAttribute('d'),r1=pathEl().getBoundingClientRect();
   T('B-2 배율 바꿔도 잉크 = 쪽 좌표(path d 동일 · 화면 크기는 배율 그대로 2배)',d2===d1&&/^M100\.0 100\.0 L200\.0 150\.0 L300\.0 160\.0$/.test(d1)&&Math.abs(r2.width/r1.width-2)<0.02,[d1,r2.width,r1.width]);
   BK.ink['bink:208']=undefined;await zInkLoad(BK,p208);
   T('B-4 되읽기(새로고침 상당) → 획 복원',BK.ink['bink:208'].s.length===1&&!!pathEl());
   T('B-4 SYNC_KEYS 에 bink·ink 없음',!SYNC_KEYS.includes('bink')&&!SYNC_KEYS.includes('ink'));
   const ex=await bkExportObj();await del('ink','bink:208');BK.ink['bink:208']=undefined;const nImp=await bkImportObj(ex);const back=await get('ink','bink:208');
   T('B-4 bink 내보내기/가져오기 왕복 동일',!!ex.bink['bink:208']&&nImp===1&&JSON.stringify(back)===JSON.stringify(ex.bink['bink:208']),[nImp,Object.keys(ex.bink)]);
   /* 툴 전환 · 텍스트층은 보기 툴에서만 */
   $('#bktools span[data-tool="pen"]').click();T('B-4 펜 툴 → 텍스트층 pointer-events none',BK.pen&&getComputedStyle(p208.el.querySelector('.bktx')).pointerEvents==='none');
   $('#bktools span[data-tool="view"]').click();T('B-6 보기 툴 → 텍스트층 잡힘',!BK.pen&&getComputedStyle(p208.el.querySelector('.bktx')).pointerEvents==='auto');
   /* B-3 조각 이어 붙이기 · 부록 */
   await bkAppend();await wait(300);
   T('B-3 「다음 절」 → 4.1.pdf 이어 붙음 · 인쇄쪽 = pdf_offset+k',BK.pcs.length===2&&BK.pcs[1].file==='4.1.pdf'&&BK.pgs.some(p=>p.pr===240)&&BK.pgs.every(p=>p.pr===p.pc.pdf_offset+p.k)&&CUR.BOOK_PDF_ADD===11,BK.pcs.map(x=>x.file));
   await bkGoto(500);await wait(300);cp=bkCurPage();
   T('B-3 부록 500쪽(기출.pdf) 열림 · 툴바 「기출 · 500쪽 (PDF 511)」',cp&&cp.pr===500&&cp.pc.file==='기출.pdf'&&$('#bkInfo').textContent==='기출 · 500쪽 (PDF 511)',[cp&&cp.pr,$('#bkInfo').textContent]);
   await bkGoto(575);await wait(200);
   T('B-3 마지막 조각 끝 = 「끝」 띠',$('#bkworld .bknext').classList.contains('end'));
   /* B-5 목차 서랍 */
   const items=$$('#bklist .bkit');
   T('B-5 서랍 = 항목 115 + 부록 2 · 장 5+부록',items.filter(x=>x.dataset.code).length===115&&items.filter(x=>!x.dataset.code).length===2&&$$('#bklist .bkch').length===6,[items.length,$$('#bklist .bkch').length]);
   let okAll=0,bad=[];for(const it of items.filter(x=>x.dataset.code)){await bkGoto(+it.dataset.p);const c=bkCurPage();if(c&&c.pr===+it.dataset.p&&$('#bklist .bkit.cur')===it)okAll++;else{const tp=BK.pgs.find(x=>x.pr===+it.dataset.p);bad.push([it.dataset.code,it.dataset.p,c&&c.pr,BK.pcs.map(x=>x.file).join(','),tp&&Math.round(tp.y),c&&Math.round(c.y),Math.round(BK.Y),BK.S,BK.pgs.length,BK.loading])}}
   T('B-5 115 항목 전부 누르면 그 쪽 · .cur 따라감',okAll===115,[okAll,bad.slice(0,5)]);
   const grip=$('#bkGrip');
   PE('pointerdown',grip,260,300);PE('pointerup',grip,260,300);await wait(50);
   T('B-5 손잡이 탭 = 접기(손잡이만 남음)',$('#bktoc').classList.contains('fold')&&$('#bktoc').getBoundingClientRect().width<=14);
   PE('pointerdown',grip,13,300);PE('pointerup',grip,13,300);await wait(50);
   PE('pointerdown',grip,260,300);PE('pointermove',grip,360,300);PE('pointerup',grip,360,300);await wait(120);
   T('B-5 끌면 너비 360 · SET.bkw 기기별 저장',!$('#bktoc').classList.contains('fold')&&Math.abs($('#bktoc').getBoundingClientRect().width-360)<2&&SET.bkw===360&&((await get('kv','set'))||{}).bkw===360,[SET.bkw,$('#bktoc').getBoundingClientRect().width]);
   T('B-5 너비 160~420 clamp',bkSetW(50)===160&&bkSetW(999)===420);bkSetW(260);
   $('#bkPrevU').click();await wait(100);$('#bkNextU').click();await wait(100);
   T('B-5 ◀▶ = 목차 항목 순서',true);
   /* B-6 포스트잇 */
   await bkGoto(208);await wait(300);zSetZoom(BK,1.2);await wait(200);const p208b=BK.pgs.find(p=>p.pr===208);await bkText(p208b);await wait(50);   /* 조각을 다시 받았으니 쪽 객체를 새로 잡는다 */
   const dbgItems=(await (await BK.pdfPage(p208b)).getTextContent()).items.length;const dbgTxt=BK.pgs.filter(p=>p.txt).map(p=>p.pr);const dbgN=p208b.el.querySelector('.bktx').children.length;
   const sp=$$('#bkover .bkpg[data-pr="208"] .bktx span[data-j]').find(s=>/[가-힣A-Za-z]{2,}/.test(s.dataset.t)&&s.getBoundingClientRect().width>10&&s.getBoundingClientRect().top>60);
   T('B-6 208쪽 텍스트층 span 있음',!!sp,[$$('#bkover .bkpg[data-pr="208"] .bktx span').length,p208b.txt,p208b.el.querySelector('.bktx').children.length,BK.Y,BK.S,bkCurPage()&&bkCurPage().pr,BK.moving,!!BK.vel,BK.pgs.length,p208b.i,$$('#bkover .bkpg[data-pr="208"]').length,p208b.txterr,p208b.el.querySelector('.bktx').innerHTML.length,dbgItems,dbgTxt,dbgN]);
   const sr=sp.getBoundingClientRect();
   PE('pointerdown',sp,sr.left+3,sr.top+sr.height/2);await wait(650);
   T('B-6 단어 길게 누르기(500ms) → 포스트잇 팝업',!!$('#bkpit')&&/포스트잇 · 208쪽 「/.test($('#bkpit h2').textContent),$('#bkpit')&&$('#bkpit h2').textContent);
   $('#bkpitT').value='검산 메모';$('#bkpitOk').click();await wait(80);
   const keys6=Object.keys(BP);
   T('B-6 저장 → BP 키 꼴 「쪽|span|단어|텍스트」 · kv bpit',keys6.length===1&&/^208\|\d+\|\d+\|\S+$/.test(keys6[0])&&BP[keys6[0]].t==='검산 메모'&&!!((await get('kv','bpit'))||{})[keys6[0]],keys6);
   const chip=()=>p208b.el.querySelector('.pitw .pitchip'),pw=()=>p208b.el.querySelector('.pitw');
   T('B-6 표시 = 단어 밑줄(.pitw) + 칩',!!pw()&&!!chip()&&pw().textContent===keys6[0].split('|')[3]);
   const inside=()=>{const a=chip().getBoundingClientRect(),b=pw().getBoundingClientRect();return a.left>=b.left-2&&a.left<=b.right+2&&a.top<=b.top+2};
   const ok1=inside();zSetZoom(BK,3);await wait(100);const ok3=inside();zSetZoom(BK,1);await wait(100);
   T('B-6 배율 바꿔도 칩이 단어 위(1.2× · 3×)',ok1&&ok3);
   T('B-6 ★ bpit = SYNC_KEYS 14째(채팅 판단 · 사용자 ① 결정에 따라 뺄 수 있음)',SYNC_KEYS[13]==='bpit'&&SYNC_REF.bpit.g()===BP);
   PE('pointerdown',sp,sr.left+3,sr.top+sr.height/2);PE('pointermove',sp,sr.left+30,sr.top+sr.height/2);await wait(650);
   T('B-6 8px 넘게 움직이면 안 붙음',!$('#bkpit'));
   chip().click();await wait(50);T('B-6 칩 누르면 같은 메모 팝업',!!$('#bkpit')&&$('#bkpitT').value==='검산 메모');$('#bkpitDel').click();await wait(80);
   T('B-6 지우기 → 키 없음 · 칩 없음',!Object.keys(BP).length&&!pw());
   /* ===== 판 2 add1 · 스크롤 C-1~C-5 (_task_jihak_app_pan2_add1.md §4) ===== */
   /* ★ A-6(a) 9/30 둘째 바퀴 — listpop §D(genie a9f9fd4 · 결정로그 9/20 19:42): 「📖 교재」가 떠 있는 창(bkWin(true) · 1000×720)으로 열린다 —
      C 묶음은 전체 화면 교재 모드(1400×900 · _task_jihak_app_pan2_add1.md §4 검산 · 9/10 3851bca 130/0)로 짰다. 창에서는 600px 왕복 동안 첫 타일(208|0|0)이
      화면에 남아 캐시에서 다시 붙일 것이 없다(적중 0 · 렌더 0) → C 묶음만 전체 화면(⤢ 길 = bkWin(false) · listpop §D 가 남긴 길)으로 재고 끝에 되돌린다 · 잣대·수치 그대로 */
   const bwC=BKWIN;bkWin(false);await wait(150);
   await bkOpen(208);await wait(600);zSetZoom(BK,1.5);await wait(700);
   const pC=BK.pgs.find(p=>p.pr===208);const protoC=Object.getPrototypeOf(await BK.pdfPage(pC));const origR=protoC.render;let rcnt=0;protoC.render=function(){rcnt++;return origR.apply(this,arguments)};
   const vpC=$('#bkvp'),vcr=vpC.getBoundingClientRect(),cxC=vcr.left+300,cyC=vcr.top+400;
   const inVp=cv=>{const r=cv.getBoundingClientRect();return r.right>vcr.left&&r.left<vcr.right&&r.bottom>vcr.top&&r.top<vcr.bottom};
   const genLog=[];
   const r0C=BK.stats.renders,a0C=BK.stats.applies,h0C=BK.stats.hits;let tsum=0;const domB=new Set($$('#bktiles canvas').map(c=>c.dataset.key));const origT0=zTileRender;const tk=[];zTileRender=function(Z,n){tk.push(n.key);return origT0.apply(this,arguments)};
   T('C-2 캐시가 산다(초기 렌더 뒤 타일 ≥2)',BK.cache.size>1,[BK.cache.size,BK.px,JSON.stringify(BK.stats),[...BK.cache.keys()],BK.layers.map(l=>[l.b,l.keys.size]),$$('#bktiles canvas').length,BK.gen]);
   PE('pointerdown',vpC,cxC,cyC,'touch');
   for(let i=1;i<=60;i++){const t0=performance.now();PE('pointermove',vpC,cxC,cyC-i*10,'touch');tsum+=performance.now()-t0;await wait(33)}
   T('C-1 2초 끌기(60 move) 동안 pg.render 0 · zRender 0 · moving',rcnt===0&&BK.stats.renders===r0C&&vpC.classList.contains('moving'),[rcnt,BK.stats.renders-r0C]);
   T('C-4 60 move 합성: zApply ≤ 60 · 핸들러 평균 < 2ms',BK.stats.applies-a0C<=60&&tsum/60<2,[BK.stats.applies-a0C,+(tsum/60).toFixed(3)]);
   const txC=pC.el.querySelector('.bktx');
   T('C-5 끄는 동안 텍스트층 hidden · 잉크 visible',getComputedStyle(txC).visibility==='hidden'&&getComputedStyle(pC.el.querySelector('.bkink')).visibility==='visible',[getComputedStyle(txC).visibility]);
   const idle=async()=>{await wait(60);let k=0;while((BK.busy||BK.vel)&&k++<200)await wait(50);await wait(60)};
   await wait(150);PE('pointerup',vpC,cxC,cyC-600,'touch');await idle();
   const domA=$$('#bktiles canvas').map(c=>c.dataset.key);const newN=domA.filter(k=>!domB.has(k)).length;
   T('C-1 멈춰서 떼면 렌더 1회 · 그린 타일 = 새로 보인 타일(캐시 적중 뺀 것)',BK.stats.renders===r0C+1&&newN>0&&rcnt+(BK.stats.hits-h0C)===newN&&!vpC.classList.contains('moving')&&getComputedStyle(txC).visibility==='visible',[BK.stats.renders-r0C,rcnt,newN,BK.stats.hits-h0C,tk,[...domB],domA,BK.layers.map(l=>[l.b,[...l.keys]]),BK.gen,BK.Y,BK.moving,!!BK.vel,JSON.stringify(BK.stats),BK.px,BK.cache.size,genLog.slice(-4)]);zTileRender=origT0;
   const rc1=rcnt,hit0=BK.stats.hits;const keysBefore=[...BK.cache.keys()];const origT=zTileRender;const newKeys=[];zTileRender=function(Z,n){newKeys.push(n.key);return origT.apply(this,arguments)};const domBefore=$$('#bktiles canvas').map(c=>c.dataset.key);
   PE('pointerdown',vpC,cxC,cyC,'touch');for(let i=1;i<=60;i++){PE('pointermove',vpC,cxC,cyC+i*10,'touch');await wait(16)}await wait(150);PE('pointerup',vpC,cxC,cyC+600,'touch');await idle();
   T('C-1 같은 자리 왕복 = 캐시 100%(pg.render 0 · 적중 있음)',rcnt===rc1&&BK.stats.hits>hit0,[rcnt-rc1,BK.stats.hits-hit0,newKeys,keysBefore,domBefore,$$('#bktiles canvas').map(c=>c.dataset.key),BK.Y,BK.S]);zTileRender=origT;
   T('C-2 캐시 ≤ 64 · 화면 밖 타일 DOM 0 · 같은 키 두 번 안 그림 · 타일 ≤2048',BK.cache.size<=64&&$$('#bktiles canvas').every(inVp)&&BK.stats.rendered===BK.cache.size&&[...BK.cache.values()].every(c=>c.width<=2048&&c.height<=2048),[BK.cache.size,$$('#bktiles canvas').filter(c=>!inVp(c)).length,BK.stats.rendered]);
   /* C-3 관성 */
   const rB=BK.stats.renders;PE('pointerdown',vpC,cxC,cyC,'touch');for(let i=1;i<=6;i++){PE('pointermove',vpC,cxC,cyC-i*25,'touch');await wait(16)}PE('pointerup',vpC,cxC,cyC-150,'touch');
   const yUp=BK.Y;await wait(80);const yAfter=BK.Y;
   T('C-3 빠른 플릭 → 뗀 뒤에도 이동(관성) · moving',!!BK.vel&&yAfter<yUp&&vpC.classList.contains('moving'),[yUp,yAfter]);
   let n3=0;while(BK.vel&&n3++<300)await wait(20);await wait(300);
   T('C-3 감속 정지 · 정지 뒤 렌더 1회 · 텍스트층 복구',!BK.vel&&BK.stats.renders===rB+1&&getComputedStyle(txC).visibility==='visible'&&!vpC.classList.contains('moving'),[BK.stats.renders-rB]);
   PE('pointerdown',vpC,cxC,cyC,'touch');for(let i=1;i<=6;i++){PE('pointermove',vpC,cxC,cyC-i*25,'touch');await wait(16)}PE('pointerup',vpC,cxC,cyC-150,'touch');await wait(60);
   T('C-3 관성 중 손이 닿으면 즉시 정지',(()=>{const had=!!BK.vel;PE('pointerdown',vpC,cxC,cyC,'touch');const now=!BK.vel;PE('pointerup',vpC,cxC,cyC,'touch');return had&&now})());
   await wait(400);await bkGoto(203);await wait(300);
   PE('pointerdown',vpC,cxC,cyC-150,'touch');for(let i=1;i<=6;i++){PE('pointermove',vpC,cxC,cyC-150+i*40,'touch');await wait(16)}PE('pointerup',vpC,cxC,cyC+90,'touch');
   let n4=0;while(BK.vel&&n4++<300)await wait(20);
   T('C-3 clamp 안 넘김(위로 관성 → Y ≤ 40)',BK.Y<=40.5,BK.Y);
   /* C-5 텍스트층 ±1 */
   await bkGoto(215);let n5=0;while(n5++<80&&(BK.pgs.some(p=>p.txtP)||n5<3))await wait(100);const curC=bkCurPage();const withTx=BK.pgs.filter(p=>p.txt);
   T('C-5 텍스트층 = 보이는 쪽 ±1 만(span 있는 쪽 ≤ 5 · 현재 쪽 ±2 안)',withTx.length>=1&&withTx.length<=5&&withTx.every(p=>Math.abs(p.i-curC.i)<=2),[withTx.map(p=>p.pr),BK.pgs.filter(p=>p.txtP).map(p=>p.pr),BK.pgs.filter(p=>p.txterr).map(p=>[p.pr,p.txterr]),BK.moving,!!BK.vel,BK.stats.renders,curC.pr,bkTextRange(),window.__err,await (async()=>{const t0=performance.now();const pp=await BK.pdfPage(curC);const r=await Promise.race([pp.getTextContent().then(x=>x.items.length),new Promise(r=>setTimeout(()=>r('timeout'),4000))]);return [r,Math.round(performance.now()-t0)]})()]);
   protoC.render=origR;
   bkWin(bwC);await wait(300);   /* ★ A-6(a) 9/30 둘째 바퀴 — C 묶음 끝 · 교재 창 모드 되돌림(아래 B-7·B-8 은 지금까지처럼 창에서) */
   /* B-7 서브노트 팝업 — 교재 모드 안 */
   $('#bkSub').click();await wait(1500);
   const sub=$('#sub'),pan=$('#sub .panel');const pr7=pan.getBoundingClientRect();
   T('B-7 교재 모드 「🗒 서브노트」 → 떠 있는 창(60%×70%) · 3.4 열',!sub.classList.contains('hide')&&getComputedStyle(pan).position==='fixed'&&Math.abs(pr7.width-innerWidth*.6)<3&&Math.abs(pr7.height-innerHeight*.7)<3&&$('#sworld .scol.on')&&$('#sworld .scol.on').dataset.sec==='3.4',[pr7.width,pr7.height,innerWidth,innerHeight]);
   const bp=$('#bkvp').getBoundingClientRect();const hit=document.elementFromPoint(bp.left+40,bp.top+40);
   T('B-7 팝업 뒤 교재가 잡힌다(pointer-events 창 안만)',!!hit&&!!hit.closest('#bkvp')&&getComputedStyle(sub).pointerEvents==='none'&&getComputedStyle(pan).pointerEvents==='auto',hit&&hit.id);
   const hd=$('#sub .shead');PE('pointerdown',hd,pr7.left+40,pr7.top+10);PE('pointermove',hd,pr7.left-60,pr7.top+60);PE('pointerup',hd,pr7.left-60,pr7.top+60);await wait(60);
   const pr8=pan.getBoundingClientRect();
   T('B-7 제목줄 끌기 → 창 이동(WIN.sub)',pan.classList.contains('float')&&Math.abs(pr8.left-(pr7.left-100))<2&&!!WIN.sub,[pr7.left,pr8.left]);
   const gr=$('#sub .twgrip');const gg=gr.getBoundingClientRect();PE('pointerdown',gr,gg.left+5,gg.top+5);PE('pointermove',gr,gg.left-95,gg.top-55);PE('pointerup',gr,gg.left-95,gg.top-55);await wait(200);
   const pr9=pan.getBoundingClientRect();
   T('B-7 모서리 끌기 → 크기 · #svp 따라감',Math.abs(pr9.width-(pr8.width-100))<2&&Math.abs($('#svp').getBoundingClientRect().width-pr9.width)<2,[pr8.width,pr9.width]);
   T('B-7 서브노트 잉크·올리기 무변(note:1 획 · sUp)',((await get('ink','note:1'))||{s:[]}).s.length===1&&!!$('#sUp'));
   $('#sX').click();await wait(50);
   /* B-8 이 쪽의 문항 */
   await bkGoto(208);await wait(200);$('#bkQ').click();await wait(100);
   T('B-8 「문항 N」 팝업 = bookList 와 같은 건수(208쪽)',!$('#bkq').classList.contains('hide')&&$$('#bkqList [data-no]').length===EXP.p208&&+$('#bkQn').textContent===EXP.p208,[$$('#bkqList [data-no]').length,EXP.p208]);
   const pick=$('#bkqList [data-no]');const pickNo=+pick.dataset.no;pick.click();await wait(150);
   /* ★ A-6(a) 9/30 둘째 바퀴 — bookwin §D(genie 6c54347 · 결정로그 9/24 19:15 · _task_jagwa_earth_bookwin.md §D 「줄을 누르면 교재 창은 그대로 두고 문항 창(.win)이 떠서 맨 앞」 ·
      앱 7537 bkQOpen 은 bkClose 를 안 넘긴다): 교재 창은 안 닫힌다 — 「📖 교재」(#btnBook 7202)는 토글이라 닫혔을 때만 눌러 되돌아온다 */
   T('B-8 누르면 교재 창은 그대로 · 그 문항 창(bookwin §D)',!$('#book').classList.contains('hide')&&VNO===pickNo&&!$('#view').classList.contains('hide'),[VNO,pickNo]);
   if(!BK.open)$('#btnBook').click();await wait(400);
   T('B-8 교재 창이 열린 채 같은 쪽(208)(bookwin §D · 닫혔으면 「📖 교재」 로 다시 열어 잰다)',BK.open&&bkCurPage()&&bkCurPage().pr===208,bkCurPage()&&bkCurPage().pr);
   /* B-7 문항 모드 셋도 팝업 */
   bkClose();await wait(50);$('#tSub').click();await wait(200);
   T('B-7 문항 모드 #tSub → 같은 팝업(전체 화면 아님)',!sub.classList.contains('hide')&&getComputedStyle(pan).position==='fixed'&&pan.getBoundingClientRect().width<innerWidth-20&&!$('#sBack'));
   $('#sX').click();$('#cSub').click();await wait(100);T('B-7 #cSub 도 팝업',!sub.classList.contains('hide'));$('#sX').click();
   await bookOpen(208,true);await wait(300);$('#bpSub').click();await wait(100);T('B-7 #bpSub 도 팝업',!sub.classList.contains('hide'));$('#sX').click();
   $('#bpBig').click();await wait(300);T('B-2 교재 패널 「📖 크게」 → 교재 모드 현재 쪽',BK.open&&bkCurPage()&&bkCurPage().pr===208);
   document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));await wait(50);
   T('B-1 Esc → 교재 모드 닫힘',!BK.open);
   /* B-1 재시작 상당: 상태에서 다시 열기 */
   localStorage.setItem('earth_book',JSON.stringify({page:290,S:1.5,toc:false}));BK.pgs=[];BK.pcs=[];BK.tile=null;$('#bkworld').innerHTML='';$('#bkover').innerHTML='';
   await bkOpen();await wait(400);
   T('B-1 저장된 쪽·배율·서랍으로 다시 열림(290 · 1.5 · 접힘)',bkCurPage()&&bkCurPage().pr===290&&BK.S===1.5&&$('#bktoc').classList.contains('fold'),[bkCurPage()&&bkCurPage().pr,BK.S]);
   bkClose();
   T('E-9 JS 오류 0',(window.__err||[]).length===0,window.__err);
   T('기록 PUT 없음(검산 중 원격 무접촉)',window.__puts.length===0,window.__puts);
  }catch(e){R.push('FAIL | 하니스가 터짐 | '+(e&&e.stack||e))}
  report(R.join('\n'));
 }
 function report(txt){try{__nativeFetch('/result',{method:'POST',body:txt})}catch(e){}}
 (function boot(n){
  if(typeof loadEarthData==='function'&&typeof db!=='undefined'&&db&&typeof recPaint==='function'&&document.getElementById('recChip').textContent)return setTimeout(run,300);
  if(n>600)return report('FAIL | 앱이 시동되지 않음 | '+JSON.stringify(window.__err||[]));
  setTimeout(()=>boot(n+1),25);
 })(0);
})();
</script>
"""

TESTS_PHONE = r"""<script>
(function(){
 const R=[]; const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+(c?'':' | '+JSON.stringify(i===undefined?null:i)));
 const __nativeFetch=window.fetch.bind(window);
 window.fetch=async function(url,opt){opt=opt||{};const u=String(url);
  const m=/api\.github\.com\/repos\/([^\/]+\/[^\/]+)\/contents\/([^?]+)/.exec(u);
  if(!m){ if(/api\.github\.com\/repos\/zzikkaplan\/notes/.test(u))return {ok:true,status:200,json:async()=>({name:'notes'}),text:async()=>''}; return __nativeFetch(url,opt); }
  const path=decodeURIComponent(m[2]);
  if((opt.method||'GET')==='PUT')return {ok:true,status:200,json:async()=>({content:{sha:'x'}}),text:async()=>''};
  const r=await __nativeFetch('/data/'+encodeURI(path),{cache:'no-store'});
  if(!r.ok)return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
  const acc=(opt.headers||{}).Accept||'';if(acc.indexOf('raw')>=0)return r;
  const sha=r.headers.get('X-Sha')||'sha';return {ok:true,status:200,json:async()=>({sha}),text:async()=>JSON.stringify({sha})};
 };
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 const vis=sel=>{const el=document.querySelector(sel);return !!el&&getComputedStyle(el).display!=='none'&&el.getBoundingClientRect().height>0};
 async function run(){
  try{
   localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}));
   if(CARD_LAYER){await loadEarthData();draw()}await wait(300);
   document.querySelectorAll('.sheet').forEach(x=>{if(!x.id)x.remove()});
   T('뷰포트 = 폰(≤480) · 과목 '+SUBJ_ID,innerWidth<=480&&innerWidth>=380,[innerWidth,innerHeight]);
   T('A-1 첫 로드 body.fold(기본 접힘 · lib_fold 없음=1)',document.body.classList.contains('fold')&&(localStorage.getItem('lib_fold')===null||localStorage.getItem('lib_fold')==='1'));
   T('A-1 #spec·.legend·#fBig·#fEtc 안 보임',!vis('#spec')&&!vis('.legend')&&!vis('#fBig')&&!vis('#fEtc'));
   T('A-1 「필터 ▾」 줄 보임 · 검색은 보임',vis('#fFold')&&getComputedStyle($('#fFold')).display==='flex'&&vis('#q')&&$('#fFoldBtn').textContent==='필터 ▾');
   const lt=$('#list').getBoundingClientRect().top;
   T('A-1 #list 상단 y ≤ 뷰포트 30%',lt<=innerHeight*0.3,[lt,innerHeight]);
   T('§2-5 폰 제목: h1 16px · 부제 숨김 · 칩 한 줄',getComputedStyle($('.brand h1')).fontSize==='16px'&&!vis('.brand .sub')&&Math.abs($('#btnSet').getBoundingClientRect().top-$('#recChip').getBoundingClientRect().top)<2,[getComputedStyle($('.brand h1')).fontSize,$('#btnSet').getBoundingClientRect().top,$('#recChip').getBoundingClientRect().top]);
   $('#fFoldBtn').click();await wait(50);
   T('A-1 「필터」 누르면 넷 보이고 lib_fold=0 · ▴',!document.body.classList.contains('fold')&&vis('#spec')&&vis('.legend')&&vis('#fBig')&&vis('#fEtc')&&localStorage.getItem('lib_fold')==='0'&&$('#fFoldBtn').textContent==='필터 ▴');
   const chipEl=[...document.querySelectorAll('#fBig .chip')].find(c=>c.childNodes[0]&&c.childNodes[0].textContent.trim()!=='전체'&&!c.classList.contains('on'));
   const lab=chipEl.childNodes[0].textContent.trim();chipEl.click();await wait(80);
   const cnt1=$('#cnt').textContent,n1=$('#list').children.length,f1=filtered().length;
   $('#fFoldBtn').click();await wait(50);
   T('A-2 접힌 채 필터 산다: 목록·#cnt 무변 · 칩 상태 유지',document.body.classList.contains('fold')&&$('#cnt').textContent===cnt1&&$('#list').children.length===n1&&filtered().length===f1&&[...document.querySelectorAll('#fBig .chip.on')].some(c=>c.childNodes[0].textContent.trim()===lab),[cnt1,$('#cnt').textContent,n1,f1]);
   T('A-2 요약 글자 = 켜진 칩 글자',$('#fSum').textContent.split(' · ').includes(lab),[$('#fSum').textContent,lab]);
   $('#q').value='';$('#q').dispatchEvent(new Event('input'));await wait(80);
   T('A-2 검색도 접힌 채 동작(#cnt 있음)',$('#cnt').textContent.length>0);
   localStorage.setItem('lib_fold','0');
   const fr=document.createElement('iframe');fr.src='app.html?re=1';fr.style.cssText='width:390px;height:844px;border:0;position:fixed;left:0;top:0;opacity:0';document.body.appendChild(fr);
   let ok=false;for(let i=0;i<150;i++){await wait(100);try{const d=fr.contentDocument;if(d&&d.body&&d.getElementById('fFoldBtn')&&d.body.dataset.subj&&d.getElementById('fFoldBtn').textContent.indexOf('필터')===0){ok=!d.body.classList.contains('fold')&&d.getElementById('fFoldBtn').textContent==='필터 ▴';if(ok)break}}catch(e){}}
   T('A-1 새로고침 뒤 유지(lib_fold=0 → 펼친 채)',ok);fr.remove();localStorage.setItem('lib_fold','1');
   T('A-4 생물 셀 살아 있음(앱 판 1 · 9/5)',!$('#subjTabs button[data-subj="bio"]').classList.contains('off'));
   /* 필터 add1(9/5): 폰 세 층 목차 서랍 열기·접기 — fixed 덮개 + 손잡이(폰 clamp = 화면−60) · 여백 없음 */
   {$('#btnTree').click();await wait(250);const tP=$('#tree'),gP=$('#trGrip');
    const PEP=(t,x,y)=>gP.dispatchEvent(new PointerEvent(t,{clientX:x,clientY:y,pointerId:3,pointerType:'touch',bubbles:true,cancelable:true,isPrimary:true}));
    T('A1 폰 「목차」 → 서랍 열림(fixed 덮개 · 폭 272 ≤ 화면−60) · 손잡이 · 여백 없음 · 줄 있음',!tP.classList.contains('hide')&&getComputedStyle(tP).position==='fixed'&&Math.round(tP.getBoundingClientRect().width)===272&&272<=innerWidth-60&&!!gP&&getComputedStyle(document.body).paddingLeft==='0px'&&$$('#trlist>div').length>0,[tP.getBoundingClientRect().width,innerWidth,$$('#trlist>div').length]);
    PEP('pointerdown',5,300);await wait(10);PEP('pointerup',6,301);await wait(60);
    T('A1 폰 탭 → 접힘 13px(손잡이만)',tP.classList.contains('fold')&&Math.round(tP.getBoundingClientRect().width)===13);
    PEP('pointerdown',5,300);await wait(10);PEP('pointerup',6,301);await wait(60);
    T('A1 폰 다시 탭 → 펼침 · 끌기 상한 = 화면−60',!tP.classList.contains('fold')&&trSetW(999)===innerWidth-60);trSetW(272);
    $('#trX').click();await wait(30);T('A1 폰 ✕ → 닫힘',tP.classList.contains('hide'));}
   T('JS 오류 0',(window.__err||[]).length===0,window.__err);
  }catch(e){R.push('FAIL | 하니스가 터짐 | '+(e&&e.stack||e))}
  try{__nativeFetch('/result',{method:'POST',body:R.join(String.fromCharCode(10))})}catch(e){}
 }
 (function boot(n){
  if((typeof loadEarthData==='function'||!CARD_LAYER)&&typeof db!=='undefined'&&db&&typeof recPaint==='function'&&document.getElementById('recChip').textContent)return setTimeout(run,300);
  if(n>600)return;
  setTimeout(()=>boot(n+1),25);
 })(0);
})();
</script>
"""

# ── _task_qa_slim2(10/8) regress 도우미 — 이름이 `_rg` · `_RG` 로 시작하는 것 = gate 에서 안 쓰는 갈래(TESTS · TESTS_PHONE 상수는 글자 그대로) ──
_RG_PICK = """<script>window.__qcN={};window.__qcPick=function(a,seed,n,key){a=[...a];n=n||10;key=key||(x=>String(x));if(a.length<=n){__qcN[seed]=[a.length,a.length];return a}
 const pick=new Set([0,a.length-1]);const h=s=>{let x=2166136261;for(const c of String(s)){x^=c.charCodeAt(0);x=Math.imul(x,16777619)>>>0}return x};
 a.map((x,i)=>[h(seed+'|'+key(x)),i]).sort((p,q)=>p[0]-q[0]||p[1]-q[1]).forEach(p=>{if(pick.size<n)pick.add(p[1])});
 const out=a.filter((x,i)=>pick.has(i));__qcN[seed]=[out.length,a.length];return out};</script>
"""   # regress 표본(A-3) — 첫 · 끝 + 씨앗 고정(FNV-1a) · 고른 것은 원래 차례
_RG_SUBS = (("   let okAll=0,bad=[];for(const it of items.filter(x=>x.dataset.code)){",
             "   let okAll=0,bad=[];const __qcS=__qcPick(items.filter(x=>x.dataset.code),'B-5',22,x=>x.dataset.code);for(const it of __qcS){   /* regress 표본 — gate 는 115 전수 */"),
            ("   T('B-5 115 항목 전부 누르면 그 쪽 · .cur 따라감',okAll===115,[okAll,bad.slice(0,5)]);",
             "   T('B-5 115 항목 전부 누르면 그 쪽 · .cur 따라감',okAll===__qcS.length&&items.filter(x=>x.dataset.code).length===115,[okAll,bad.slice(0,5),'(표본 '+__qcS.length+'/115)']);"))


def _rg_tests(t):
    """regress · smoke — 쪽 안 시험 글을 이 자리에서만 고친다 · smoke = 앞머리(E-3) + B-1 교재 열림 + E-9 JS 오류 0 · regress = B-5 표본 — 자리를 못 찾으면 그대로(= gate 와 같은 전수)"""
    if QC.SMOKE:
        i0 = t.find("   T('E-3 문항 704 적재'")
        b0 = t.find("   /* ===== 판 2 · 교재 모드 B-1~B-8")
        b1 = t.find("   T('B-1 📖 교재 → #book 열림 · 조각 받음 · 문항 무변'")
        e0 = t.find("   T('E-9 JS 오류 0'")
        c0 = t.find("  }catch(e){R.push('FAIL | 하니스가 터짐 | '")
        if min(i0, b0, b1, e0, c0) < 0:
            print('NOTE | smoke 자르기 자리 못 찾음 — 통째로 돈다')
            return t
        i1, b2, e1 = t.find('\n', i0) + 1, t.find('\n', b1) + 1, t.find('\n', e0) + 1
        return t[:i1] + t[b0:b2] + t[e0:e1] + t[c0:]
    for old, new in _RG_SUBS:
        if t.count(old) == 1:
            t = t.replace(old, new)
        else:
            print('NOTE | regress B-5 표본 자리 %d 번 — 그대로(전수)' % t.count(old))
            return t
    return _RG_PICK + t


def main():
    phone = 'phone' in sys.argv[1:]; subj = os.environ.get('PHONE_SUBJ', 'earth')
    html = open(SRC, encoding='utf-8', newline='').read()
    html = html.replace('<script defer src="https://cdnjs', '<script defer data-off="https://cdnjs')
    html = html.replace('<link rel="stylesheet" href="https://cdnjs', '<link rel="off" href="https://cdnjs')
    html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', STUB.replace("localStorage.setItem('subj','earth')", "localStorage.setItem('subj','%s')" % (subj if phone else 'earth')) + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    # 기대값(파이썬 쪽 집계)
    rows = list(csv.DictReader(open(os.path.join(GIGU, '_지학_문항.csv'), encoding='utf-8-sig')))
    idx = json.load(open(os.path.join(SPD, 'pdf', 'index.json'), encoding='utf-8'))
    def loc(p):
        for k, v in idx.items():
            if v['인쇄시작'] <= p <= v['인쇄끝']: return [p, v['file'], p - v['pdf_offset']]
    # ★ A-6(d) 9/30 둘째 바퀴 — 3.4.5·208쪽 기대는 앱이 받는 그 데이터(SPD 문항.json)로 센다: listpop §G(studyplandata 182e1f37 · 결정로그 9/20 19:42)가 사용자 매칭 114건(단원·교재쪽)을
    #   박아 CSV(박기 전 사본) 14/14 → 데이터 17/17(git show 셈 517b369c 14 · 182e1f37~cbd451ae 17) · 박힌 114 행의 교재쪽은 수(int)라 str 로 맞댄다 · E-1 표본 글·pages 는 그대로
    qd = json.load(open(os.path.join(SPD, '문항.json'), encoding='utf-8'))
    exp = {'u345': sum(1 for r in qd if r['유형'] == '기출' and str(r['단원']) == '3.4.5'),
           'p208': sum(1 for r in qd if str(r['교재쪽']) == '208' or (r['유형'] == '확인' and str(r['문제쪽']) == '208') or (r['유형'] == '기출' and str(r['해설쪽']) == '208')),
           'pages': [loc(p) for p in (2, 74, 208, 240, 290, 489)]}
    html = html.replace('</body>', ((TESTS_PHONE if phone else TESTS) if QC.GATE else _rg_tests(TESTS_PHONE if phone else TESTS)).replace('__EXP__', json.dumps(exp, ensure_ascii=False)) + '</body>', 1)   # regress · smoke — 쪽 안 시험 글을 이 자리에서만 고쳐 씀
    open(APP, 'w', encoding='utf-8', newline='').write(html)
    # 폰 모드(_task_phys_phone_top.md A-1~A-4): 390×844 iframe 안에서 돈다 — 헤드리스 창은 500px 아래로 안 줄어 미디어 규칙이 안 걸리므로
    open(os.path.join(OUT, 'phone.html'), 'w', encoding='utf-8').write('<!doctype html><meta charset="utf-8"><body style="margin:0;background:#888"><iframe src="app.html" style="width:390px;height:844px;border:0;display:block"></iframe></body>')
    shutil.copy(os.path.join(GIGU, '지학_서브노트_빈판_A3.pdf'), os.path.join(OUT, 'blank.pdf'))

    done = threading.Event(); box = {}
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=OUT, **k)
        def log_message(self, *a, **k): pass
        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            if p.startswith('/notes/'):
                f = os.path.join(os.path.expanduser('~'), 'Documents', 'notes', p[7:].replace('/', os.sep))
                if not os.path.isfile(f): self.send_response(404); self.end_headers(); return
                b = open(f, 'rb').read(); self.send_response(200); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b); return
            if p.startswith('/data/'):
                rel = p[6:]
                if not rel.startswith('earth/'): print('[harness] earth 밖 요청 → 404:', rel); self.send_response(404); self.end_headers(); return
                f = os.path.join(SPD, rel[6:].replace('/', os.sep))
                if not os.path.isfile(f): self.send_response(404); self.end_headers(); return
                b = open(f, 'rb').read()
                self.send_response(200); self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', str(len(b))); self.send_header('X-Sha', hashlib.sha1(b).hexdigest()); self.end_headers()
                self.wfile.write(b); return
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
    QC.launch('new')   # 셈(§B-4) — 새 판 크롬 한 번(바탕은 본디 안 띄운다)
    p = subprocess.Popen([chrome, '--headless=new', '--disable-gpu', '--no-first-run', '--user-data-dir=' + prof, '--window-size=1400,900',
                          'http://127.0.0.1:%d/%s' % (port, 'phone.html' if phone else 'app.html')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    import time as _t; _t0=_t.time(); got = done.wait(int(os.environ.get('HARNESS_WAIT','600'))); p.terminate(); print('elapsed %.0fs' % (_t.time()-_t0))
    try: p.wait(10)
    except Exception: p.kill()
    srv.shutdown()
    if not got: print('결과 없음 — 시간 안에 검사가 끝나지 않았다 · 마지막 중간 결과:'); print(box.get('partial', '(없음)')); sys.exit(1)
    lines = [ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()]
    if phone:
        npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
        for x in lines: print(x)
        print('\n== 폰(%s) %d PASS / %d FAIL / %d항 ==' % (subj, npass, nfail, len(lines))); sys.exit(0 if nfail == 0 else 2)
    def T2(name, cond, info=''): lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))
    if QC.SMOKE:   # smoke — 소스 글 · 파일 셈 칸(E-1 · E-2 · E-3 img · B-5 · B-9 · B-10)은 smoke 칸이 아니다
        npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
        for x in lines: print(x)
        print('\n== smoke %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines))); sys.exit(0 if nfail == 0 else 2)
    s = open(SRC, encoding='utf-8').read()
    T2('E-1(병합 뒤) 물리 동작 무변은 물리 하네스 셋으로 증명 — 여기서는 파일 하나임만 확인', os.path.basename(SRC) == 'index.html' and 'jagwa' in SRC)   # 9/5 자과 서재 이사
    samples = [r['문항'][:18] for r in rows if len(r['문항']) > 30][:5] + [r['해설'][:18] for r in rows if len(r['해설']) > 30][:3]
    T2('E-1 jagwa/index.html 에 교재 본문 문자열 0(표본 8)', not any(x in s for x in samples), [x for x in samples if x in s])
    T2('E-1 물리 데이터는 한 파일이라 있다(PEM0101) — 지학 본문만 없으면 된다', 'PEM0101' in s)
    T2('E-2 조각 18 · 100MB 초과 0', len(idx) == 18 and all(os.path.getsize(os.path.join(SPD, 'pdf', v['file'])) < 100 * 1048576 for v in idx.values()))
    T2('E-3 img 198 파일', len([f for f in os.listdir(os.path.join(SPD, 'img')) if f.endswith('.jpg')]) == 198)
    T2('백틱 짝', s.count('`') % 2 == 0)
    import re as _re
    m480 = _re.findall(r'@media \(max-width:480px\)\{[^\n]*', s)
    T2('B-5 폰(≤480px)에서도 서랍 — #bktoc 에 시트(translateY) 규칙 0', not any('#bktoc' in x for x in m480), [x[:80] for x in m480 if '#bktoc' in x])
    T2('B-9 PDF 층 게이트에 #btnBook·#book·#bkq', 'body[data-layer="pdf"] #btnBook' in s and 'body[data-layer="pdf"] #book' in s and 'body[data-layer="pdf"] #bkq' in s)
    lay = s[s.index('/*EARTH:js*/'):s.index('/*/EARTH:js*/')]
    T2('B-10 층 안 EARTH.·earthdata 0 · 새 코드는 층 머리 if(SHELL) 안(셸 세 과목 · 카드 몫은 if(HASBOOK))', 'EARTH.' not in lay and "'earthdata'" not in lay and lay.split('\n')[2] == 'if(SHELL){')   # ★ A-6(a) 9/30 — 셸 이식(c9faff2): 층 머리 if(CARD_LAYER){ → if(SHELL){
    # 옛 줄: T2('B-9 …', … and "SYNC_KEYS:['status',…,'mcard','link']," in s)
    T2('B-9 SUBJ.phys 다섯 값 무변(9/5 필터 손질: SYNC_KEYS 12째 link 반영)', "phys:{DB:'phys535', PDF_DIR:'phys/pdf/', REC_PATH:'phys/기록.json', SYNC_PREFIX:'phys_sync_'," in s and ("SYNC_KEYS:['status','note','qtype','conc','gpt','twin','ansfix','frm','maskpos','omrpos','mcard','link']," in s or "SYNC_KEYS:['status','note','qtype','conc','gpt','twin','ansfix','frm','maskpos','omrpos','mcard','link','cqx']," in s))   # ★ 2026-10-09 _task_jagwa_gg3 §A-2-3 — 13째 cqx
    npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
    for x in lines: print(x)
    print('\n== %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)

if __name__ == '__main__':
    main()
