# -*- coding: utf-8 -*-
"""자과 서재 물리 층 — 필터·툴바 손질 하니스 (2026-09-05 · moolri/_task_phys_filter_fix.md B-5 ①~④)

_harness_phys_twin.py 골격(로컬 서버 · 헤드리스 크롬 · POST /result · GitHub 404 · KaTeX 스텁 · pdf.js 진짜 CDN). 빈 기록에서 시작. 원본 무접촉.
 ① 히트맵 = 「변리사 기출」 250 / 「기본」 255 / 둘 다 꺼짐 577 · #specHd 한 줄 · 장 필터 동행
 ② 「안 푼 것」 칩 · #btnRand · #btnFirst · 🔒⟳＋ DOM 0(물리) · SET.rot 비움 · SET.zoom 1 · 핀치/Ctrl+휠 코드 무변(없음)
 ③ 「메모 있음」 = 시트 · 줄 수 = 코멘트 ∪ 손필기 ∪ 볼트 · 코드 → 뷰어 · 🃏 → 카드 창 · 💬 → 코멘트 시트
 ④ 「연결」 A→B 저장(한 방향 · kv link · SYNC 12째) → B 카드 역방향 칩 · 목록 칩 · 새로고침 상당 유지 · 끊기 · 검색 셋
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import http.server, os, socketserver, subprocess, sys, threading, shutil
from pypdf import PdfWriter

SRC = _roots.genie(r"jagwa\index.html")
OUT = os.path.join(os.environ.get('TEMP', '.'), 'physhF'); os.makedirs(OUT, exist_ok=True)
APP = os.path.join(OUT, 'app.html')

STUB = """<script>
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
 window.fetch=async function(url,opt){ if(/api\.github\.com/.test(String(url)))return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)}; return __nativeFetch(url,opt) };
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 const findChip=lab=>[...document.querySelectorAll('#fEtc .chip')].find(x=>x.textContent.trim().startsWith(lab));
 const cnt=lab=>{const c=findChip(lab);return c?+(c.querySelector('small')||{textContent:'-1'}).textContent:null};
 async function run(){
  try{
   renderPage=async()=>{};setupMask=async()=>{};paintInk=()=>{};
   ST={};CMT={};MC={};LK={};TW={};await put('kv','link',{});await put('kv','note',{});
   document.querySelectorAll('.sheet').forEach(x=>x.remove());
   const buf=await (await __nativeFetch('/blank.pdf')).arrayBuffer();await put('pdf','111',buf);await loadHave();
   FL.bigs=[];FL.subs=[];FL.past='';FL.mark='';FL.q='';draw();await wait(30);
   const nY=DATA.filter(r=>r[F.SRC]==='변리사').length,nN=DATA.filter(r=>!r[F.SRC]).length;
   /* ===== ① 히트맵 ===== */
   T('① 시작 = 둘 다 꺼짐 → 히트맵 577 · #specHd 「전체 577」',$$('#spec i').length===DATA.length&&DATA.length===577&&$('#specHd').textContent==='전체 577',[$$('#spec i').length,$('#specHd').textContent]);
   findChip('변리사 기출').click();await wait(40);
   T('① 「변리사 기출」 켜면 히트맵 250 · 범례 안 푼 것 = 250 · 「변리사 기출 250」',FL.past==='y'&&$$('#spec i').length===nY&&nY===250&&$('#c0').textContent==='250'&&$('#specHd').textContent==='변리사 기출 250',[$$('#spec i').length,$('#specHd').textContent,$('#c0').textContent]);
   findChip('변리사 기출').click();await wait(20);findChip('기본').click();await wait(40);
   T('① 「기본」 켜면 255',FL.past==='n'&&$$('#spec i').length===nN&&nN===255&&$('#specHd').textContent==='기본 255',[$$('#spec i').length]);
   const big0=BIGS[0];[...document.querySelectorAll('#fBig .chip')].find(c=>c.textContent.startsWith(bigLabel(big0))).click();await wait(40);
   const nB=DATA.filter(r=>!r[F.SRC]&&r[F.BIG]===big0).length;
   T('① 장 필터 동행(기본 ∩ 역학) · 머리 줄에 장 이름',$$('#spec i').length===nB&&$('#specHd').textContent==='기본 '+nB+' · '+bigLabel(big0),[$$('#spec i').length,nB,$('#specHd').textContent]);
   FL.bigs=[];findChip('기본').click();await wait(40);
   T('① 둘 다 꺼지면 577 · 연도 칩·채점표 칩 규칙 무변(변리사 켜야 연도)',$$('#spec i').length===577&&!findChip('02년')&&(()=>{findChip('변리사 기출').click();const ok=!!findChip('02년');findChip('변리사 기출').click();return ok})(),[$$('#spec i').length]);
   FL.lv='상';draw();await wait(30);T('① 상중하·마크 필터는 히트맵이 무시(577 그대로)',$$('#spec i').length===577);FL.lv='';draw();await wait(20);
   /* ===== ② 제거 · 되돌림 ===== */
   T('② 「안 푼 것」 칩 없음 · 틀린 것·헷갈림·두 번 이상 틀림·⚠ 약점·🌤 덜약점·P 있음',!findChip('안 푼 것')&&['틀린 것','헷갈림','두 번 이상 틀림','⚠ 약점','🌤 덜약점','P'].every(l=>!!findChip(l)));
   T('② #btnRand · #btnFirst DOM 0(물리) · 「공식 보기」「개념으로 훑기」 있음',!$('#btnRand')&&!$('#btnFirst')&&!!$('#btnFormula')&&!!$('#btnConcept'));
   T('② 🔒⟳＋ DOM 0 · 쌍둥이·GPT·코멘트·기록·유형·암기카드 있음',!$('#tLock')&&!$('#tRot')&&!$('#tZoom')&&!!$('#tTwin')&&!!$('#tGpt')&&!!$('#tNote')&&!!$('#tHist')&&!!$('#tType')&&!!$('#tCard'));
   T('② SET.p3reset=1 · SET.rot={} · SET.zoom=1 · kv set 에도',SET.p3reset===1&&JSON.stringify(SET.rot)==='{}'&&SET.zoom===1&&((await get('kv','set'))||{}).zoom===1&&JSON.stringify(((await get('kv','set'))||{}).rot)==='{}',[SET.p3reset,SET.rot,SET.zoom]);
   /* ===== ③ 메모 있음 시트 ===== */
   const q1=DATA.find(r=>r[F.FILE]==='111'),qs=DATA.filter(r=>r[F.FILE]==='111');const a=qs[0][F.NO],b=qs[3][F.NO],c=qs[5][F.NO];
   CMT[a]='코멘트 A';CMT[b]='코멘트 B';await saveNote();MC[c]={w:360,h:240,s:[{c:'#000',w:2,hl:0,p:[10,10,50,50]}]};await saveMC();MC[b]={w:360,h:240,s:[]};await saveMC();draw();await wait(40);
   T('③ 칩 「메모 있음 N」 = 코멘트 ∪ 손필기 = 3(a·b 코멘트 · b·c 카드) · 볼트 카드 0장',cnt('메모 있음')===3&&MCARDS.length===0,[cnt('메모 있음'),MCARDS.length]);
   findChip('메모 있음').click();await wait(60);
   const rows=[...document.querySelectorAll('#memoSheet .memor')];
   T('③ 누르면 시트(필터 아님 · 목록 무변) · 줄 3 · 머리 「메모 있음 3 · 코멘트 2 · 암기카드 2」',!!$('#memoSheet')&&rows.length===3&&FL.mark===''&&filtered().length===577&&/메모 있음 3 · 코멘트 2 · 암기카드 2/.test($('#memoSheet h2').textContent),[rows.length,$('#memoSheet h2').textContent]);
   T('③ 줄 = 코드 · 코멘트 첫 줄 · 💬/🃏 · 코드 순 · 대단원 묶음',rows.map(d=>d.dataset.no).map(Number).sort((x,y)=>x-y).join()===[a,b,c].sort((x,y)=>x-y).join()&&rows.every(d=>d.querySelector('.mcode'))&&$$('#memoSheet .memor[data-no="'+a+'"] [data-cmt]').length===1&&!$('#memoSheet .memor[data-no="'+a+'"] [data-card]')&&$$('#memoSheet .memor[data-no="'+b+'"] [data-cmt]').length===1&&$$('#memoSheet .memor[data-no="'+b+'"] [data-card]').length===1&&!$('#memoSheet .memor[data-no="'+c+'"] [data-cmt]')&&$$('#memoSheet .memor[data-no="'+c+'"] [data-card]').length===1&&$$('#memoSheet h3.frmh').length>=1&&$('#memoSheet .memor[data-no="'+a+'"] .mtxt').textContent==='코멘트 A',rows.map(d=>d.outerHTML.slice(0,80)));
   T('③ 정렬 = 코드 순',(()=>{const codes=rows.map(d=>d.querySelector('.mcode').textContent);const groups={};rows.forEach((d,i)=>{const g=d.closest('.memol');(groups[[...document.querySelectorAll('#memoSheet .memol')].indexOf(g)]=groups[[...document.querySelectorAll('#memoSheet .memol')].indexOf(g)]||[]).push(codes[i])});return Object.values(groups).every(g=>g.join()===g.slice().sort().join())})());
   $('#memoSheet .memor[data-no="'+b+'"] [data-cmt]').click();await wait(40);
   T('③ 💬 → 코멘트 시트(값 = 코멘트 B)',!!$('#ntIn')&&$('#ntIn').value==='코멘트 B');$('#ntNo').click();await wait(10);
   $('#memoSheet .memor[data-no="'+c+'"] [data-card]').click();await wait(60);
   T('③ 🃏 → 손필기 카드 창(.mcwin · 뷰어 #tCard 와 같은 창) · 볼트 단추 없음(0장)',!!$('.mcwin')&&/🃏/.test($('.mcwin h2').textContent)&&!$('#mcwVault'));$('.mcwin #mcX').click();await wait(10);
   $('#memoSheet .memor[data-no="'+a+'"] .mcode').click();await wait(80);
   T('③ 코드 → 그 문항 뷰어 · 시트 닫힘',VNO===a&&!$('#view').classList.contains('hide')&&!$('#memoSheet'));
   /* ===== ④ 연결 ===== */
   T('④ 뷰어 툴바 「연결」(#tLink · 쌍둥이 오른쪽) · 칩 #vLink 숨김(0)',!!$('#tLink')&&$('#tLink').previousElementSibling.id==='tTwin'&&$('#tLink').textContent==='연결'&&getComputedStyle($('#vLink')).display==='none');
   T('④ SYNC_KEYS 12 · 12째 link · SYNC_REF.link · SUBJ.phys 12 무변 · 지학 19 · 생물 20(add1 +bref)',SYNC_KEYS.length===12&&SYNC_KEYS[11]==='link'&&SYNC_REF.link.g()===LK&&SUBJ.phys.SYNC_KEYS.length===12&&SUBJ.earth.SYNC_KEYS.length===19&&SUBJ.bio.SYNC_KEYS.length===20);
   $('#tLink').click();await wait(40);
   T('④ 시트 #linkSheet · 아직 없다 · 검색 칸',!!$('#linkSheet')&&/아직 없다/.test($('#lkList').textContent)&&!!$('#lkq'));
   const rb=rec(b);$('#lkq').value=rb[F.CODE];$('#lkq').dispatchEvent(new Event('input'));await wait(30);
   T('④ 코드 검색 → 후보(＋ 연결)',$$('#lkres .lkhit').length>=1&&$('#lkres .lkhit[data-add="'+b+'"]')&&/＋ 연결/.test($('#lkres .lkhit[data-add="'+b+'"] small').textContent));
   $('#lkres .lkhit[data-add="'+b+'"]').click();await wait(80);
   T('④ 잇기 → LK[a]=[b](한 방향) · LK[b] 없음 · kv link · 목록 줄 「끊기」 · 검색 결과 「이미 넣음」 · #vLink 「🔗 1」',JSON.stringify(LK[a])===JSON.stringify([b])&&!LK[b]&&JSON.stringify(((await get('kv','link'))||{})[a])===JSON.stringify([b])&&!!$('#lkList .lkrow[data-no="'+b+'"] .lkdel')&&/이미 넣음/.test(($('#lkres .lkhit[data-add="'+b+'"] small')||{}).textContent||'')&&$('#vLink').textContent==='🔗 1'&&getComputedStyle($('#vLink')).display!=='none',[LK,$('#vLink').textContent]);
   $('#lkq').value=rb[F.SUB].slice(0,4);$('#lkq').dispatchEvent(new Event('input'));await wait(30);const hitSub=$$('#lkres .lkhit').length;
   $('#lkq').value=String(rec(c)[F.BODY]||'그림').slice(0,6);$('#lkq').dispatchEvent(new Event('input'));await wait(30);const hitBody=$$('#lkres .lkhit').length;
   T('④ 소단원·본문 검색도 잡힌다',hitSub>=1&&hitBody>=1,[hitSub,hitBody]);
   $('#lkX').click();await wait(10);
   await openView(b);await wait(60);
   T('④ B 카드 = 역방향 칩 「🔗 1」 · 시트에 「역방향」(끊기 없음)',$('#vLink').textContent==='🔗 1'&&(()=>{$('#tLink').click();const ok=!!$('#lkList .lkrow[data-no="'+a+'"]')&&!$('#lkList .lkrow[data-no="'+a+'"] .lkdel')&&/역방향/.test($('#lkList .lkrow[data-no="'+a+'"]').textContent);$('#lkX').click();return ok})());
   $('#tLink').click();await wait(20);$('#lkList .lkrow[data-no="'+a+'"] b').click();await wait(1200);
   T('④ 시트 줄 코드 → 문항 팝업(twinPeek · 그림+코멘트)',!!$('.sheet.twin')&&/코멘트 A/.test($('.sheet.twin').textContent),$('.sheet.twin')&&$('.sheet.twin').textContent.slice(0,60));$('#twX').click();await wait(10);$('#lkX').click();
   closeView();await wait(60);
   const rowB=[...document.querySelectorAll('#list .item')].find(d=>d.querySelector('.num').textContent===String(b));
   T('④ 목록 B 줄에 🔗 1 칩(역방향)',!!rowB&&!!rowB.querySelector('.tag.lk')&&rowB.querySelector('.tag.lk').textContent==='🔗 1');
   rowB.querySelector('.tag.lk').click();await wait(30);T('④ 목록 칩 → 연결 시트(B)',!!$('#linkSheet')&&/'+b+'번 연결/.test($('#linkSheet h2').textContent)||(!!$('#linkSheet')&&$('#linkSheet h2').textContent.startsWith(b+'번')));$('#lkX').click();
   /* 새로고침 상당 · 동기화 도장 */
   LK={};LK=(await get('kv','link'))||{};T('④ 새로고침 상당(kv 되읽기) 유지',JSON.stringify(LK[a])===JSON.stringify([b]));
   stampAll();T('④ 동기화 도장 link|a · recPayload 에 link',!!lsObj(U_KEY)['link|'+a]&&!!recPayload().data.link&&JSON.stringify(recPayload().data.link[a])===JSON.stringify([b]),Object.keys(lsObj(U_KEY)).filter(k=>k.startsWith('link')));
   await openView(a);await wait(40);$('#tLink').click();await wait(20);$('#lkList .lkrow[data-no="'+b+'"] .lkdel').click();await wait(60);
   T('④ 끊기 → LK 비움 · kv · #vLink 숨김',!LK[a]&&!((await get('kv','link'))||{})[a]&&getComputedStyle($('#vLink')).display==='none');$('#lkX').click();
   T('④ 쌍둥이 무접촉(twinSheet · TW 비어 있음 · 쌍 칩 없음)',typeof twinSheet==='function'&&Object.keys(TW).length===0&&!$('#list .tag.tw'));
   closeView();
   /* ===== add1 첫 화면 목차 서랍 + 세 층 손잡이 (_task_phys_filter_fix_add1.md B-3) ===== */
   const ptr=(el,type,x,y)=>el.dispatchEvent(new PointerEvent(type,{bubbles:true,cancelable:true,clientX:x,clientY:y,pointerId:1,pointerType:'mouse',isPrimary:true,button:0}));
   const drag=async(el,x0,y0,x1,y1)=>{ptr(el,'pointerdown',x0,y0);await wait(10);ptr(el,'pointermove',(x0+x1)/2,(y0+y1)/2);await wait(10);ptr(el,'pointermove',x1,y1);await wait(10);ptr(el,'pointerup',x1,y1);await wait(40)};
   const tap=async(el,x,y)=>{ptr(el,'pointerdown',x,y);await wait(10);ptr(el,'pointerup',x+1,y+1);await wait(60)};
   FL.bigs=[];FL.subs=[];FL.past='';FL.mark='';FL.q='';draw();await wait(30);
   const tr=$('#tree');
   T('A1 「목차」 칩 보임(게이트 해제) · #tree 있음·숨김 · #trTog 숨김 · 손잡이 #trGrip',getComputedStyle($('#btnTree')).display!=='none'&&!!tr&&tr.classList.contains('hide')&&!!$('#trGrip')&&getComputedStyle($('#trTog')).display==='none');
   $('#btnTree').click();await wait(40);
   const subsN=BIGS.reduce((a,b)=>a+new Set(DATA.filter(r=>r[F.BIG]===b).map(r=>r[F.SUB])).size,0);
   const sumN=()=>[...$$('#trlist .trsec .n')].reduce((a,x)=>a+ +x.textContent,0);
   T('A1 서랍 열림(display flex · z 62) · body.tropen · 줄 = 대단원 6 + 소단원 '+subsN+' · 소단원 수 합 = 577',!tr.classList.contains('hide')&&getComputedStyle(tr).display==='flex'&&+getComputedStyle(tr).zIndex===62&&document.body.classList.contains('tropen')&&$$('#trlist .trch').length===6&&$$('#trlist .trsec').length===subsN&&sumN()===577&&/전체/.test($('#tree .trhead span').textContent),[$$('#trlist .trch').length,$$('#trlist .trsec').length,sumN()]);
   findChip('변리사 기출').click();await wait(60);
   T('A1 「변리사 기출」 켜면 서랍 수 합 250 · 머리 글',sumN()===250&&/변리사 기출/.test($('#tree .trhead span').textContent),[sumN(),$('#tree .trhead span').textContent]);
   findChip('변리사 기출').click();await wait(60);
   const sec=$$('#trlist .trsec')[5];const sb=sec.dataset.b,ss=sec.dataset.s;sec.click();await wait(700);
   const ghd=[...$$('#list .grouphd')].find(x=>x.firstChild&&x.firstChild.textContent===bigLabel(sb)+' · '+ss);
   T('A1 소단원 클릭 → FL.bigs/subs · 목록 = 그 소단원 · 줄 hit · 목록 머리가 화면 안(스크롤) · 서랍은 열린 채(≥900)',FL.bigs.join()===sb&&FL.subs.join()===ss&&filtered().every(r=>r[F.SUB]===ss)&&filtered().length>0&&!!$('#trlist .trsec.hit')&&$('#trlist .trsec.hit').dataset.s===ss&&!!ghd&&ghd.getBoundingClientRect().top>=0&&ghd.getBoundingClientRect().top<innerHeight&&!tr.classList.contains('hide'),[FL.bigs,FL.subs,ghd&&ghd.getBoundingClientRect().top]);
   $$('#trlist .trch')[1].click();await wait(300);
   T('A1 대단원 클릭 → 그 대단원 전체(FL.subs 비움) · 줄 hit',FL.bigs.length===1&&FL.subs.length===0&&$('#trlist .trch.hit')&&filtered().every(r=>r[F.BIG]===FL.bigs[0]));
   FL.bigs=[];FL.subs=[];draw();await wait(30);
   /* 손잡이 */
   const g=$('#trGrip');const gb=g.getBoundingClientRect();
   T('A1 데스크톱 여백 = body padding-left 272 · 서랍 폭 272 · 손잡이 13px 오른쪽(테두리 1px 안쪽 = 271)',getComputedStyle(document.body).paddingLeft==='272px'&&Math.round(tr.getBoundingClientRect().width)===272&&Math.round(gb.width)===13&&Math.abs(gb.right-272)<=1,[getComputedStyle(document.body).paddingLeft,gb.width,gb.right]);
   await tap(g,gb.left+6,gb.top+200);
   T('A1 탭 → 접힘(13px · 손잡이만 · 내용 숨김) · SET.tro=1 · kv · 여백 13 · 손잡이 ›',tr.classList.contains('fold')&&Math.round(tr.getBoundingClientRect().width)===13&&getComputedStyle($('#trlist')).display==='none'&&SET.tro===1&&((await get('kv','set'))||{}).tro===1&&getComputedStyle(document.body).paddingLeft==='13px'&&g.textContent==='›',[SET.tro,tr.getBoundingClientRect().width]);
   await drag(g,6,200,106,200);
   T('A1 접힌 채 끌기 = 무시(폭 13 그대로 · SET.trw 없음)',Math.round(tr.getBoundingClientRect().width)===13&&SET.trw===undefined);
   await tap(g,6,200);
   T('A1 다시 탭 → 펼침 · SET.tro=0 · 여백 272',!tr.classList.contains('fold')&&SET.tro===0&&getComputedStyle(document.body).paddingLeft==='272px');
   await drag(g,gb.left+6,gb.top+200,gb.left+106,gb.top+200);
   T('A1 끌기 +100 → 폭 372 · SET.trw=372 · kv · 여백 372',Math.round(tr.getBoundingClientRect().width)===372&&SET.trw===372&&((await get('kv','set'))||{}).trw===372&&getComputedStyle(document.body).paddingLeft==='372px',[tr.getBoundingClientRect().width,SET.trw]);
   await drag(g,372,200,1300,200);T('A1 상한 420',Math.round(tr.getBoundingClientRect().width)===420&&SET.trw===420);
   await drag(g,420,200,-500,200);T('A1 하한 160',Math.round(tr.getBoundingClientRect().width)===160&&SET.trw===160);
   document.documentElement.style.removeProperty('--trw');T('A1 새로고침 흉내(--trw 지움 → 272)',Math.round(tr.getBoundingClientRect().width)===272);
   trSetW(SET.trw);T('A1 시동 적용(trSetW(SET.trw)) → 160',Math.round(tr.getBoundingClientRect().width)===160);trSetW(300);SET.trw=300;
   T('A1 clamp 160~420',trSetW(50)===160&&trSetW(999)===420);trSetW(300);
   T('A1 #ndGrip 도 공통 gripWire(옛 IIFE 없음) · ndSetW 무변',typeof gripWire==='function'&&ndSetW(50)===160&&ndSetW(999)===420);
   $('#trX').click();await wait(30);
   T('A1 ✕ → 숨김 · body.tropen 해제 · 여백 0',tr.classList.contains('hide')&&!document.body.classList.contains('tropen')&&getComputedStyle(document.body).paddingLeft==='0px');
   T('JS 오류 0',(window.__err||[]).length===0,window.__err);
  }catch(e){R.push('FAIL | 하니스가 터짐 | '+(e&&e.stack||e))}
  report(R.join('\n'));
 }
 function report(txt){try{__nativeFetch('/result',{method:'POST',body:txt})}catch(e){}}
 (function boot(n){
  if(typeof syncRecords==='function'&&typeof db!=='undefined'&&db&&typeof recPaint==='function'&&document.getElementById('recChip').textContent&&typeof pdfjsLib!=='undefined'&&pdfjsLib.getDocument&&typeof SET!=='undefined'&&SET.p3reset)return setTimeout(run,200);
  if(n>600)return report('FAIL | 앱이 시동되지 않음 | '+JSON.stringify(window.__err||[]));
  setTimeout(()=>boot(n+1),25);
 })(0);
})();
</script>
"""

def main():
    html = open(SRC, encoding='utf-8', newline='').read()
    html = html.replace('<script defer src="https://cdnjs', '<script defer data-off="https://cdnjs')
    html = html.replace('<link rel="stylesheet" href="https://cdnjs', '<link rel="off" href="https://cdnjs')
    html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', STUB + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    html = html.replace('</body>', TESTS + '</body>', 1)
    open(APP, 'w', encoding='utf-8', newline='').write(html)
    w = PdfWriter(); w.add_blank_page(width=400, height=600); w.write(open(os.path.join(OUT, 'blank.pdf'), 'wb'))
    done = threading.Event(); box = {}
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=OUT, **k)
        def log_message(self, *a, **k): pass
        def do_POST(self):
            n = int(self.headers.get('Content-Length') or 0); box['txt'] = self.rfile.read(n).decode('utf-8', 'replace')
            self.send_response(204); self.end_headers(); done.set()
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    prof = os.path.join(OUT, 'prof'); shutil.rmtree(prof, ignore_errors=True)
    p = subprocess.Popen([chrome, '--headless=new', '--disable-gpu', '--no-first-run', '--user-data-dir=' + prof, '--window-size=1400,900',
                          'http://127.0.0.1:%d/app.html' % port], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    got = done.wait(240); p.terminate()
    try: p.wait(10)
    except Exception: p.kill()
    srv.shutdown()
    if not got: print('결과 없음 — 240초 안에 검사가 끝나지 않았다'); sys.exit(1)
    lines = [ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()]
    def T2(name, cond, info=''): lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))
    s = open(SRC, encoding='utf-8', newline='').read().replace('\r\n', '\n')
    T2('백틱 짝', s.count('`') % 2 == 0, s.count('`'))
    T2('CRLF 만', open(SRC, 'rb').read().count(b'\r\n') == open(SRC, 'rb').read().count(b'\n'))
    # 판 2 add2(2026-09-07) — 카드 층은 「랜덤으로 풀기」 대신 「암기카드」(#btnMC) 하나를 만든다.
    #   그래서 재는 것을 `$('#btnRand').onclick` 에서 `mb.id='btnMC'` 로 갈았다(고친 자리).
    #   물리 쪽 제거 줄(if(!CARD_LAYER){['btnRand','btnFirst']…})은 그대로라 아래에서 따로 잰다.
    T2('② 🔒⟳＋ HTML·핸들러 0 · 「안 푼 것」 칩 = 층 사본 1곳만(지학·생물 무접촉) · 머리 단추 만드는 자리 = 층 1곳만', 'id="tLock"' not in s and "$('#tLock')" not in s and "$('#tRot')" not in s and "$('#tZoom')" not in s and s.count("chip('안 푼 것'") == 1 and s.count("mb.id='btnMC'") == 1 and s.count("if(!CARD_LAYER){['btnRand','btnFirst']") == 1)
    lay = s[s.index('/*EARTH:js*/'):s.index('/*/EARTH:js*/')]
    T2('지학·생물 층 안에 「안 푼 것」·머리 단추(btnMC)·메모 있음 필터 그대로(무접촉)', "chip('안 푼 것'" in lay and "mb.id='btnMC'" in lay and "$('#btnRand')" in lay and "mchip('메모 있음','note',nNt)" in lay)
    # 판 2 add3(2026-09-08) — 모아보기(지학)에 ctrl+휠 확대가 생겼다. mcardSheet 는 층 **밖**이라
    #   소스 위치만 보면 이 줄이 걸린다. CLAUDE.md 「『물리 무변』은 소스 무접촉이 아니다」에 따라
    #   **가드 안에 있는가**로 갈아 잰다(고친 자리). 물리 뷰어 쪽에는 여전히 wheel 핸들러가 없다.
    _pre = s.split('/*EARTH:js*/')[0]
    _z0 = _pre.find('b.__zsetup=()=>{')
    _z1 = _pre.find(chr(10) + '  };' + chr(10), _z0) if _z0 >= 0 else -1
    T2('핀치·Ctrl+휠은 JG 전용 배선(b.__zsetup) 안에만 있다 — 물리 뷰어엔 wheel 핸들러 없음 그대로',
       _pre.count("addEventListener('wheel'") == 1 and _z0 >= 0 and _z1 > _z0
       and _pre.index("addEventListener('wheel'") > _z0 and _pre.index("addEventListener('wheel'") < _z1
       and "if(JG&&b.__zsetup)b.__zsetup();" in s,
       [_pre.count("addEventListener('wheel'"), _z0, _z1])
    # 판 3 ①(2026-09-08) — crop 이 붙어 지학 16 · 생물 17. 물리 12 는 그대로다(고친 자리).
    T2('SUBJ.phys SYNC_KEYS 12 무변 · earth 19 · bio 20 (add1 +bref · SUBJ 블록)', "SYNC_KEYS:['status','note','qtype','conc','gpt','twin','ansfix','frm','maskpos','omrpos','mcard','link']," in s and s.count("'bpit','bpg','crop','txt','tfix','bref'],") == 1 and "'bpg','snote','crop','txt','tfix','bref']," in s)
    npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
    for x in lines: print(x)
    print('\n== %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)

if __name__ == '__main__':
    main()
