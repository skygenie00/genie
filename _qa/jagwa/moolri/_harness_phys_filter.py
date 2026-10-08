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
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import http.server, os, socketserver, subprocess, sys, threading, shutil
from pypdf import PdfWriter

SRC = _roots.genie(r"jagwa\index.html")
OUT = os.path.join(os.environ.get('TEMP', '.'), 'physhF'); os.makedirs(OUT, exist_ok=True)
APP = os.path.join(OUT, 'app.html')
_RG_SMOKE = ('① 시작 = 둘 다 꺼짐', 'A1 단원 머리 줄', 'JS 오류 0')   # qa_slim2 smoke 칸(A-0)

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
   const nY=DATA.filter(r=>r[F.SRC]==='변리사').length,nN=DATA.filter(r=>r[F.SRC]!=='변리사').length;   /* ★ A-6(a) 9/30 — 셸 add18 §A-1(0c19a60): 「기본」 = 변리사가 아닌 것 전부(옛 기본 255 + 타기출 72 = 327 · 앱 8376 · phPast) */
   /* ===== ① 히트맵 ===== */
   T('① 시작 = 둘 다 꺼짐 → 히트맵 577 · #specHd 「전체 577」',$$('#spec i').length===DATA.length&&DATA.length===577&&$('#specHd').textContent==='전체 577',[$$('#spec i').length,$('#specHd').textContent]);
   /* ★ A-6(a) 9/30 — 셸 이식(c9faff2) 뒤 물리 필터 칩 줄은 카드 층 것(숨은 줄 · 「변리사 기출」·「기본」 칩 없음 → findChip undefined.click 로 터짐) ·
      분류는 히트맵 머리 칩 #eKind [data-past](add6 §B-1 · add18 §A-1 셋 = 전체·기출·기본) · 편은 #eChs [data-big] — 누르는 자리만 옮긴다(기대 값·제목은 그대로) */
   const kd=v=>$('#eKind [data-past="'+v+'"]');kd('y').click();await wait(40);
   T('① 「변리사 기출」 켜면 히트맵 250 · 범례 안 푼 것 = 250 · 「변리사 기출 250」',FL.past==='y'&&$$('#spec i').length===nY&&nY===250&&$('#c0').textContent==='250'&&$('#specHd').textContent==='변리사 기출 250',[$$('#spec i').length,$('#specHd').textContent,$('#c0').textContent]);
   kd('').click();await wait(20);kd('n').click();await wait(40);
   T('① 「기본」 켜면 327',FL.past==='n'&&$$('#spec i').length===nN&&nN===327&&$('#specHd').textContent==='기본 327',[$$('#spec i').length]);
   const big0=BIGS[0];[...document.querySelectorAll('#eChs [data-big]')].find(c=>c.dataset.big===big0).click();await wait(40);
   const nB=DATA.filter(r=>r[F.SRC]!=='변리사'&&r[F.BIG]===big0).length;   /* ★ A-6(a) 9/30 — 셸 add18 §A-1(0c19a60): 기본 = 변리사가 아닌 것 전부 → 기본 ∩ 역학 = 129(옛 118 + 타기출 11) */
   T('① 장 필터 동행(기본 ∩ 역학) · 머리 줄에 장 이름',$$('#spec i').length===nB&&$('#specHd').textContent==='기본 '+nB+' · '+bigLabel(big0),[$$('#spec i').length,nB,$('#specHd').textContent]);
   FL.bigs=[];kd('').click();await wait(40);
   T('① 둘 다 꺼지면 577 · 연도 칩·채점표 칩 규칙 무변(변리사 켜야 연도)',$$('#spec i').length===577&&!!$('#fYear')&&$('#fYear').disabled&&(()=>{kd('y').click();const s=$('#fYear');const ok=!!s&&!s.disabled&&[...s.options].some(o=>o.textContent.startsWith('02년'));kd('').click();return ok})(),[$$('#spec i').length,!!$('#fYear')&&$('#fYear').disabled]);   /* ★ A-6(a) 9/30 — 셸 add4(c9faff2): 옛 연도 칩 25(02~26년)는 .ebar 「연도 ▾」 고르개(#fYear · 옵션 「02년 10」…)로 — 규칙 그대로 「변리사 기출」이 아니면 잠긴다(disabled · 옛 1836줄 · 앱 8443~8455) */
   FL.lv='상';draw();await wait(30);T('① 상중하·마크 필터는 히트맵이 무시(577 그대로)',$$('#spec i').length===577);FL.lv='';draw();await wait(20);
   /* ===== ② 제거 · 되돌림 ===== */
   T('② 「안 푼 것」 칩 없음 · 틀린 것·헷갈림·두 번 이상 틀림·⚠ 약점·🌤 덜약점·P 있음',!findChip('안 푼 것')&&['틀린 것','헷갈림','두 번 이상 틀림','⚠ 약점','🌤 덜약점','P'].every(l=>!!findChip(l)));
   T('② #btnRand · #btnFirst DOM 0(물리) · 「공식 보기」「개념으로 훑기」 있음',!$('#btnRand')&&!$('#btnFirst')&&!!$('#btnFormula')&&!!$('#btnConcept'));
   T('② 🔒⟳＋ DOM 0 · 쌍둥이·GPT·코멘트·기록·유형·암기카드 있음',!$('#tLock')&&!$('#tRot')&&!$('#tZoom')&&!!$('#tTwin')&&!!$('#tGpt')&&!!$('#tNote')&&!!$('#tHist')&&!!$('#tType')&&!!$('#tCard'));
   T('② SET.p3reset=1 · SET.rot={} · SET.zoom=1 · kv set 에도',SET.p3reset===1&&JSON.stringify(SET.rot)==='{}'&&SET.zoom===1&&((await get('kv','set'))||{}).zoom===1&&JSON.stringify(((await get('kv','set'))||{}).rot)==='{}',[SET.p3reset,SET.rot,SET.zoom]);
   /* ===== ③ 메모 있음 시트 ===== */
   const q1=DATA.find(r=>r[F.FILE]==='111'),qs=DATA.filter(r=>r[F.FILE]==='111');const a=qs[0][F.NO],b=qs[3][F.NO],c=qs[5][F.NO];
   CMT[a]='코멘트 A';CMT[b]='코멘트 B';await saveNote();MC[c]={w:360,h:240,s:[{c:'#000',w:2,hl:0,p:[10,10,50,50]}]};await saveMC();MC[b]={w:360,h:240,s:[]};await saveMC();draw();await wait(40);
   /* ★ A-6(a) 9/30 — 셸 add6 §C-3(216dd4a): 물리 「메모 있음 N」 칩(#fMemo)은 걷었다(갈 곳 = 「🃏 전체」 #mcAll · 옛 코멘트는 근거로) —
      #fEtc 의 「메모 있음」은 셸 이식(c9faff2) 뒤 카드 층 칩(숨은 줄 · 거르개 'note' · 코멘트만 세어 2)이라 세지도 누르지도 않는다(누르면 거르개만 걸리고 #memoSheet 가 없어 71줄에서 터졌다) ·
      memoSheet 는 「들머리만 걷었다」(add6 수행 결과 101줄) — 그 칩이 부르던 그대로 직접 부른다(mcsheet A-6 선례 · 화면에서 여는 길은 없다 · 아래 시트 줄·머리·💬·🃏·코드 잣대는 그대로) */
   T('③ 「메모 있음」 칩 = 물리에서 걷음(셸 add6 §C-3 · 갈 곳 🃏 전체) · memoHas = 코멘트 ∪ 손필기 = 3(a·b 코멘트 · b·c 카드) · 볼트 카드 0장',!$('#fMemo')&&!!$('#mcAll')&&DATA.filter(memoHas).length===3&&MCARDS.length===0,[!!$('#fMemo'),!!$('#mcAll'),DATA.filter(memoHas).length,MCARDS.length]);
   memoSheet();await wait(60);
   const rows=[...document.querySelectorAll('#memoSheet .memor')];
   T('③ 누르면 시트(필터 아님 · 목록 무변) · 줄 3 · 머리 「메모 있음 3 · 코멘트 2 · 암기카드 2」',!!$('#memoSheet')&&rows.length===3&&FL.mark===''&&filtered().length===577&&/메모 있음 3 · 코멘트 2 · 암기카드 2/.test($('#memoSheet h2').textContent),[rows.length,$('#memoSheet h2').textContent]);
   T('③ 줄 = 코드 · 코멘트 첫 줄 · 💬/🃏 · 코드 순 · 대단원 묶음',rows.map(d=>d.dataset.no).map(Number).sort((x,y)=>x-y).join()===[a,b,c].sort((x,y)=>x-y).join()&&rows.every(d=>d.querySelector('.mcode'))&&$$('#memoSheet .memor[data-no="'+a+'"] [data-cmt]').length===1&&!$('#memoSheet .memor[data-no="'+a+'"] [data-card]')&&$$('#memoSheet .memor[data-no="'+b+'"] [data-cmt]').length===1&&$$('#memoSheet .memor[data-no="'+b+'"] [data-card]').length===1&&!$('#memoSheet .memor[data-no="'+c+'"] [data-cmt]')&&$$('#memoSheet .memor[data-no="'+c+'"] [data-card]').length===1&&$$('#memoSheet h3.frmh').length>=1&&$('#memoSheet .memor[data-no="'+a+'"] .mtxt').textContent==='코멘트 A',rows.map(d=>d.outerHTML.slice(0,80)));
   T('③ 정렬 = 코드 순',(()=>{const codes=rows.map(d=>d.querySelector('.mcode').textContent);const groups={};rows.forEach((d,i)=>{const g=d.closest('.memol');(groups[[...document.querySelectorAll('#memoSheet .memol')].indexOf(g)]=groups[[...document.querySelectorAll('#memoSheet .memol')].indexOf(g)]||[]).push(codes[i])});return Object.values(groups).every(g=>g.join()===g.slice().sort().join())})());
   $('#memoSheet .memor[data-no="'+b+'"] [data-cmt]').click();await wait(40);
   T('③ 💬 → 코멘트 시트(값 = 코멘트 B)',!!$('#ntIn')&&$('#ntIn').value==='코멘트 B');$('#ntNo').click();await wait(10);
   $('#memoSheet .memor[data-no="'+c+'"] [data-card]').click();await wait(60);
   T('③ 🃏 → 손필기 카드 창(.mcwin · 뷰어 #tCard 와 같은 창) · 볼트 단추 없음(0장)',!!$('.mcwin')&&/🃏/.test($('.mcwin h2').textContent)&&!$('#mcwVault'));$('.mcwin #mcX').click();await wait(10);
   $('#memoSheet .memor[data-no="'+a+'"] .mcode').click();await wait(80);
   /* ★ A-6(a) 9/30 — 셸 전역 [data-go] 규칙(앱 9384~9400 문서 캡처 · earth_bookwin §A 23줄 「전역 9004 는 안 건드린다(data-go = 문항 번호 규칙 유지)」 · 수행 결과 160줄 전수 — 2925 = 이 시트의 코드):
      코드(b.mcode data-go)는 전역 규칙이 먼저 잡아 그 문항 창을 열고 멈춘다 — 시트 제 누름(닫고 열기)은 안 돈다(시트가 남는다 · 여는 길 0 이라 화면 영향 없음 — add6 §C-3) · 뒷정리로 닫는다 */
   T('③ 코드 → 그 문항 뷰어(셸 전역 data-go 규칙) · 시트는 남는다(시트 제 누름 안 돎)',VNO===a&&!$('#view').classList.contains('hide')&&!!$('#memoSheet'),[VNO,!!$('#memoSheet')]);
   {const mx=$('#memoX');if(mx)mx.click();await wait(10);}
   /* ===== ④ 연결 ===== */
   /* ★ A-6(a) 9/30 — 셸 이식(c9faff2 · physRowBuild 앱 9584~9597): 물리 아랫줄 단추는 #pRow1 로 옮겨져 「… 공식 · 개념 · 쌍둥이 · Claude · 유형 · 연결」 차례다 — 연결 바로 앞 = 유형(#tType) */
   T('④ 뷰어 아랫줄 「연결」(#tLink · #pRow1 · 유형 오른쪽) · 칩 #vLink 숨김(0)',!!$('#tLink')&&$('#tLink').previousElementSibling.id==='tType'&&($('#tLink').textContent==='연결'||$('#tLink').textContent==='🔗')&&getComputedStyle($('#vLink')).display==='none');   /* ★ 2026-10-07 (_task_jagwa_phys_win §A-30) — 시안 ㉟ 물리 아랫줄 「연결」 → 🔗 하나(쌍둥이 합침) */
   /* ★ A-6(a) 9/30 — 셸 본판 §E-7(c9faff2): 물리 SYNC_KEYS 끝에 gg·ggref(앱 8168~8169) — SYNC_KEYS 가 SUBJ.phys.SYNC_KEYS 와 같은 배열이라(앱 4355) 둘 다 14 · SUBJ 소스 글자는 12 그대로(아래 파일 층 잣대) */
   T('④ SYNC_KEYS 14(끝에 gg·ggref) · 12째 link · SYNC_REF.link · SUBJ.phys 도 같은 배열 14 · 지학 19 · 생물 20(add1 +bref)',/* ★ 합치기 10/1(하위 에이전트 C) — physphone A-2(97883ef 본문 「물리 SYNC 키 tfix 하나 더함」) — 14 또는 끝에 tfix 하나 */(SYNC_KEYS.length===14||(SYNC_KEYS.length===15&&SYNC_KEYS[14]==='tfix')||(SYNC_KEYS.length===16&&SYNC_KEYS.slice(14).sort().join()==='solx,tfix'))/* ★ 2026-10-07 (_task_jagwa_phys_win §A-30) — 시안 ㉖ 물리 SYNC_KEYS 끝에 solx(오린 것) 하나 더(tfix 와 함께 끝 둘) */&&SYNC_KEYS[12]==='gg'&&SYNC_KEYS[13]==='ggref'&&SYNC_KEYS[11]==='link'&&SYNC_REF.link.g()===LK&&SUBJ.phys.SYNC_KEYS.length===SYNC_KEYS.length&&SUBJ.earth.SYNC_KEYS.length===19&&SUBJ.bio.SYNC_KEYS.length===20);
   (typeof relPop==='function'?linkSheet(VNO):$('#tLink').click());await wait(40);   /* ★ 2026-10-07 (_task_jagwa_phys_win §A-30) — 시안 ㊵ 물리 🔗 = 단추 옆 작은 창 #rlPop(큰 연결 창 걷음) — 연결 저장·검색·끊기 옛 잣대는 큰 연결 창(linkSheet · 목록 🔗 칩이 아직 여는 창)을 직접 열어 잰다(mcsheet A-6 선례) */
   /* ★ A-6(a) 9/30 — 셸 add16(0bee72b): 연결 시트(linkSheet)는 「보는 시트」라 떠 있는 창 #sh-link(앱 SHWIN ['linkSheet','link'] · shFloat 이 id 를 sh-<key> 로) · 안의 #lkList·#lkq·#lkres 는 그대로 ·
      phone_win A-5(fb89ad2 · pwBtns): 그 창의 「닫기」(#lkX)는 걷었다 → 아래 닫기는 전부 ✕(.shx) */
   T('④ 연결 창 #sh-link(떠 있는 창 · 셸 add16) · 아직 없다 · 검색 칸',!!$('#sh-link')&&/아직 없다/.test($('#lkList').textContent)&&!!$('#lkq'));
   const rb=rec(b);$('#lkq').value=rb[F.CODE];$('#lkq').dispatchEvent(new Event('input'));await wait(30);
   T('④ 코드 검색 → 후보(＋ 연결)',$$('#lkres .lkhit').length>=1&&$('#lkres .lkhit[data-add="'+b+'"]')&&/＋ 연결/.test($('#lkres .lkhit[data-add="'+b+'"] small').textContent));
   $('#lkres .lkhit[data-add="'+b+'"]').click();await wait(80);
   T('④ 잇기 → LK[a]=[b](한 방향) · LK[b] 없음 · kv link · 목록 줄 「끊기」 · 검색 결과 「이미 넣음」 · #vLink 「🔗 1」',JSON.stringify(LK[a])===JSON.stringify([b])&&!LK[b]&&JSON.stringify(((await get('kv','link'))||{})[a])===JSON.stringify([b])&&!!$('#lkList .lkrow[data-no="'+b+'"] .lkdel')&&/이미 넣음/.test(($('#lkres .lkhit[data-add="'+b+'"] small')||{}).textContent||'')&&$('#vLink').textContent==='🔗 1'&&getComputedStyle($('#vLink')).display!=='none',[LK,$('#vLink').textContent]);
   $('#lkq').value=rb[F.SUB].slice(0,4);$('#lkq').dispatchEvent(new Event('input'));await wait(30);const hitSub=$$('#lkres .lkhit').length;
   $('#lkq').value=String(rec(c)[F.BODY]||'그림').slice(0,6);$('#lkq').dispatchEvent(new Event('input'));await wait(30);const hitBody=$$('#lkres .lkhit').length;
   T('④ 소단원·본문 검색도 잡힌다',hitSub>=1&&hitBody>=1,[hitSub,hitBody]);
   $('#sh-link .shx').click();await wait(10);   /* ★ A-6(a) 9/30 — 연결 창 「닫기」(#lkX) 걷음(phone_win A-5) → ✕ */
   await openView(b);await wait(60);
   T('④ B 카드 = 역방향 칩 「🔗 1」 · 시트에 「역방향」(끊기 없음)',$('#vLink').textContent==='🔗 1'&&(()=>{(typeof relPop==='function'?linkSheet(VNO):$('#tLink').click());/* ★ 2026-10-07 (_task_jagwa_phys_win §A-30) — ㊵ 위와 같음 */const ok=!!$('#lkList .lkrow[data-no="'+a+'"]')&&!$('#lkList .lkrow[data-no="'+a+'"] .lkdel')&&/역방향/.test($('#lkList .lkrow[data-no="'+a+'"]').textContent);$('#sh-link .shx').click();return ok})());   /* ★ A-6(a) 9/30 — 연결 창 「닫기」 걷음(phone_win A-5) → ✕ */
   (typeof relPop==='function'?linkSheet(VNO):$('#tLink').click());await wait(20);$('#lkList .lkrow[data-no="'+a+'"] b').click();await wait(1200);   /* ★ 2026-10-07 (_task_jagwa_phys_win §A-30) — ㊵ 위와 같음 */
   /* ★ A-6(a) 9/30 — 셸 전역 [data-go] 규칙(앱 9384~9400 문서 캡처 · earth_bookwin §A 23줄 「data-go = 문항 번호 규칙 유지」 · 수행 결과 160줄 전수 — 2117 = 연결 시트 줄 코드):
      줄 코드(b data-go)는 twinPeek 대신 그 문항 창을 연다 · 문항이 바뀌면 문항에 매인 창(연결 창)은 닫힌다(add16 SHPERQ · 앱 7860·7876~7881) — 닫을 팝업·창이 없다 */
   T('④ 시트 줄 코드 → 그 문항 창(셸 전역 data-go 규칙 · 연결 창 닫힘)',VNO===a&&!$('#view').classList.contains('hide')&&!$('#sh-link')&&!$('.sheet.twin'),[VNO,!!$('#sh-link'),!!$('.sheet.twin')]);
   closeView();await wait(60);
   const rowB=[...document.querySelectorAll('#list .item')].find(d=>d.querySelector('.num').textContent===codeShow(rec(b)));   /* ★ A-6(a) 9/30 — 셸 목록 줄 .num = 코드(codeShow · add11 §0-3 · phys_P P-1 과 같은 까닭) */
   T('④ 목록 B 줄에 🔗 1 칩(역방향)',!!rowB&&!!rowB.querySelector('.tag.lk')&&rowB.querySelector('.tag.lk').textContent==='🔗 1');
   rowB.querySelector('.tag.lk').click();await wait(30);T('④ 목록 칩 → 연결 시트(B)',/* ★ A-6(a) 9/30 — 연결 창 = #sh-link(셸 add16) · 「닫기」 걷음(phone_win A-5) → ✕ */!!$('#sh-link')&&/'+b+'번 연결/.test($('#sh-link h2').textContent)||(!!$('#sh-link')&&$('#sh-link h2').textContent.startsWith(b+'번')));$('#sh-link .shx').click();
   /* 새로고침 상당 · 동기화 도장 */
   LK={};LK=(await get('kv','link'))||{};T('④ 새로고침 상당(kv 되읽기) 유지',JSON.stringify(LK[a])===JSON.stringify([b]));
   stampAll();T('④ 동기화 도장 link|a · recPayload 에 link',!!lsObj(U_KEY)['link|'+a]&&!!recPayload().data.link&&JSON.stringify(recPayload().data.link[a])===JSON.stringify([b]),Object.keys(lsObj(U_KEY)).filter(k=>k.startsWith('link')));
   await openView(a);await wait(40);(typeof relPop==='function'?linkSheet(VNO):$('#tLink').click());await wait(20);$('#lkList .lkrow[data-no="'+b+'"] .lkdel').click();await wait(60);   /* ★ 2026-10-07 (_task_jagwa_phys_win §A-30) — ㊵ 위와 같음 */
   T('④ 끊기 → LK 비움 · kv · #vLink 숨김',!LK[a]&&!((await get('kv','link'))||{})[a]&&getComputedStyle($('#vLink')).display==='none');$('#sh-link .shx').click();   /* ★ A-6(a) 9/30 — 연결 창 「닫기」 걷음(phone_win A-5) → ✕ */
   T('④ 쌍둥이 무접촉(twinSheet · TW 비어 있음 · 쌍 칩 없음)',typeof twinSheet==='function'&&Object.keys(TW).length===0&&!$('#list .tag.tw'));
   closeView();
   /* ===== add1 첫 화면 목차 서랍 + 세 층 손잡이 (_task_phys_filter_fix_add1.md B-3) ===== */
   const ptr=(el,type,x,y)=>el.dispatchEvent(new PointerEvent(type,{bubbles:true,cancelable:true,clientX:x,clientY:y,pointerId:1,pointerType:'mouse',isPrimary:true,button:0}));
   const drag=async(el,x0,y0,x1,y1)=>{ptr(el,'pointerdown',x0,y0);await wait(10);ptr(el,'pointermove',(x0+x1)/2,(y0+y1)/2);await wait(10);ptr(el,'pointermove',x1,y1);await wait(10);ptr(el,'pointerup',x1,y1);await wait(40)};
   const tap=async(el,x,y)=>{ptr(el,'pointerdown',x,y);await wait(10);ptr(el,'pointerup',x+1,y+1);await wait(60)};
   FL.bigs=[];FL.subs=[];FL.past='';FL.mark='';FL.q='';draw();await wait(30);
   const tr=$('#tree');
   /* ★ A-6(a) 9/30 — 셸 add9 §A-1·§A-6(68216cf): 첫 화면 「목차」 단추(#btnTree)와 옛 목차 서랍(#tree · treeOpen 빈 함수 — 앱 3770~3771)은 걷었고 그 구실은 왼쪽 상주 서랍(#navdr · 단원 머리 줄 .ndsec)이 맡는다
      (add9 수행 결과 표 「「목차」 단추 걷음」·「옛 목차 서랍 — 안 뜬다」·「단원 머리 줄 .ndsec = 절 이름 · 마지막 마크 점 · 문항 수 · 누르면 첫 화면 목록이 그 절로 스크롤」·「접힘·너비 = #ndGrip」) — 아래 A1 은 그 서랍으로 잰다 */
   T('A1 「목차」 단추 걷음(셸 add9 §A-1 · 상주 서랍이 갈음) · #tree 있음·숨김 · #trTog 숨김 · 손잡이 #trGrip',!$('#btnTree')&&!!tr&&tr.classList.contains('hide')&&!!$('#trGrip')&&getComputedStyle($('#trTog')).display==='none');
   treeOpen();await wait(40);   /* 옛 여는 길 — 빈 함수라 안 뜬다(아래 칸이 잰다) */
   const subsN=BIGS.reduce((a,b)=>a+new Set(DATA.filter(r=>r[F.BIG]===b).map(r=>r[F.SUB])).size,0);
   const sumN=()=>[...$$('#ndList .ndsec .n')].reduce((a,x)=>a+ +x.textContent,0);   /* ★ A-6(a) 9/30 — 상주 서랍 단원 머리 줄(.ndsec)의 문항 수 합(add9 §A-3 · navBuild 앱 3566~3596) */
   T('A1 옛 목차 서랍은 안 뜬다(treeOpen 빈 함수 · #tree 숨김 · body.tropen 없음) · 상주 서랍 단원 머리 줄 = 소단원 '+subsN+' · 머리 수 합 = 577 · 머리 글 「목록 577문항」',tr.classList.contains('hide')&&!document.body.classList.contains('tropen')&&!$('#navdr').classList.contains('hide')&&$('#navdr').classList.contains('ndres')&&$$('#ndList .ndsec').length===subsN&&sumN()===577&&$('#ndHead').textContent==='목록 577문항',[tr.classList.contains('hide'),$$('#ndList .ndsec').length,sumN(),$('#ndHead').textContent]);
   kd('y').click();await wait(60);   /* ★ A-6(a) 9/30 — 「변리사 기출」 = 히트맵 머리 분류 칩 #eKind(add6 §B-1 · ① 과 같은 누름 · #fEtc 옛 칩은 카드 층 숨은 줄이라 없다) · 상주 서랍은 draw 덮개가 다시 짓는다(앱 3728~3734) */
   T('A1 「변리사 기출」 켜면 상주 서랍 머리 수 합 250 · 머리 글 「목록 250문항」',sumN()===250&&$('#ndHead').textContent==='목록 250문항',[sumN(),$('#ndHead').textContent]);
   kd('').click();await wait(60);
   /* ★ A-6(a) 9/30 — add9 §A-3: 단원 머리 줄(.ndsec)을 누르면 첫 화면 목록이 그 단원 머리(#list [data-uhd])로 스크롤한다 — 거르지 않는다(FL 무변 · 앱 3613~3623) */
   const sec=$$('#ndList .ndsec')[5];const su=sec.dataset.sec;sec.click();await wait(300);{let _p=-1,_n=0;for(let i=0;i<20;i++){const _g=[...$$('#list [data-uhd]')].find(x=>x.dataset.uhd===su);const _t=_g?Math.round(_g.getBoundingClientRect().top):-9;if(_t===_p){if(++_n>=2)break}else{_n=0;_p=_t}await wait(100)}}   /* ★ A-6(d) 9/30 — 앱은 scrollIntoView({block:'center',behavior:'smooth'})(3622) — 577줄 목록에서 부드러운 굴림이 700ms 안에 안 끝남(셋째 실행 top 898.875) → 머리 자리가 두 번 같을 때까지(최대 2.3초) 기다린다 */
   const ghd=[...$$('#list [data-uhd]')].find(x=>x.dataset.uhd===su);
   T('A1 단원 머리 줄(상주 서랍 .ndsec) 누름 → 첫 화면 목록이 그 단원 머리로 스크롤(거르지 않음 · FL 무변) · 서랍은 선 채',!FL.bigs.length&&!FL.subs.length&&!FL.unit&&filtered().length===577&&!!ghd&&ghd.getBoundingClientRect().top>=0&&ghd.getBoundingClientRect().top<innerHeight&&!$('#navdr').classList.contains('hide'),[FL.bigs,FL.subs,su,ghd&&ghd.getBoundingClientRect().top]);
   /* ★ A-6(a) 9/30 — 상주 서랍에는 대단원(편) 줄이 없다(add19 §A-2 「편·절 머리는 서랍에 안 세운다」 · 앱 3562~3565) — 대단원으로 거르기는 히트맵 머리 편 칩 #eChs(add6 §A)가 맡는다 */
   [...$$('#eChs [data-big]')].filter(x=>x.dataset.big)[1].click();await wait(300);
   T('A1 대단원 = 편 칩(#eChs · 상주 서랍엔 대단원 줄 없음) 누름 → 그 대단원 전체(FL.subs 비움) · 칩 on',FL.bigs.length===1&&FL.subs.length===0&&!$('#ndList .trch')&&!!$('#eChs [data-big].on')&&$('#eChs [data-big].on').dataset.big===FL.bigs[0]&&filtered().every(r=>r[F.BIG]===FL.bigs[0]),[FL.bigs,FL.subs]);
   FL.bigs=[];FL.subs=[];draw();await wait(30);
   /* 손잡이 */
   /* ★ A-6(a) 9/30 — 셸 add9 §A-2(68216cf): 옛 #tree 손잡이(#trGrip · SET.tro/trw · body.tropen)는 숨은 서랍 안에 남았을 뿐이고 그 구실은 상주 서랍 #navdr 의 #ndGrip 이 맡는다 —
      탭 = 접기(13px · 손잡이 ›) · 끌기 = 너비(160~420 · 기본 236) · 접힘·너비 = 기기별 localStorage(ND_FOLD_K · ND_W_K) · 놓으면 SET.ndw · 여백 body.ndon = --ndw(add9 수행 결과 74·78줄 · 첫 바퀴 생물 A1 과 같은 옮김) */
   const nd=$('#navdr'),g=$('#ndGrip');const gb=g.getBoundingClientRect();
   T('A1 데스크톱 여백 = body.ndon padding-left 236 · 상주 서랍 폭 236 · 손잡이 #ndGrip 13px 오른쪽(테두리 1px 안쪽 = 235)',getComputedStyle(document.body).paddingLeft==='236px'&&Math.round(nd.getBoundingClientRect().width)===236&&Math.round(gb.width)===13&&Math.abs(gb.right-236)<=1,[getComputedStyle(document.body).paddingLeft,nd.getBoundingClientRect().width,gb.width,gb.right]);
   await tap(g,gb.left+6,gb.top+200);
   T('A1 탭 → 접힘(13px · 손잡이만 · 내용 숨김) · jagwa.nd.fold.phys=1 · 여백 13 · 손잡이 ›',nd.classList.contains('fold')&&Math.round(nd.getBoundingClientRect().width)===13&&getComputedStyle($('#ndList')).display==='none'&&localStorage.getItem(ND_FOLD_K)==='1'&&getComputedStyle(document.body).paddingLeft==='13px'&&g.textContent==='›',[localStorage.getItem(ND_FOLD_K),nd.getBoundingClientRect().width]);
   await drag(g,6,200,106,200);
   T('A1 접힌 채 끌기 = 무시(폭 13 그대로 · SET.ndw 없음)',Math.round(nd.getBoundingClientRect().width)===13&&SET.ndw===undefined,[nd.getBoundingClientRect().width,SET.ndw]);
   await tap(g,6,200);
   T('A1 다시 탭 → 펼침 · jagwa.nd.fold.phys=0 · 여백 236',!nd.classList.contains('fold')&&localStorage.getItem(ND_FOLD_K)==='0'&&getComputedStyle(document.body).paddingLeft==='236px');
   await drag(g,gb.left+6,gb.top+200,gb.left+106,gb.top+200);
   T('A1 끌기 +100 → 폭 336 · SET.ndw=336 · kv · 여백 336',Math.round(nd.getBoundingClientRect().width)===336&&SET.ndw===336&&((await get('kv','set'))||{}).ndw===336&&getComputedStyle(document.body).paddingLeft==='336px',[nd.getBoundingClientRect().width,SET.ndw]);
   await drag(g,372,200,1300,200);T('A1 상한 420',Math.round(nd.getBoundingClientRect().width)===420&&SET.ndw===420);
   await drag(g,420,200,-500,200);T('A1 하한 160',Math.round(nd.getBoundingClientRect().width)===160&&SET.ndw===160);
   document.documentElement.style.removeProperty('--ndw');T('A1 새로고침 흉내(--ndw 지움 → 236)',Math.round(nd.getBoundingClientRect().width)===236);
   ndSetW(SET.ndw);T('A1 시동 적용(ndSetW(SET.ndw)) → 160',Math.round(nd.getBoundingClientRect().width)===160);ndSetW(300);SET.ndw=300;
   T('A1 clamp 160~420',trSetW(50)===160&&trSetW(999)===420);trSetW(300);
   T('A1 #ndGrip 도 공통 gripWire(옛 IIFE 없음) · ndSetW 무변',typeof gripWire==='function'&&ndSetW(50)===160&&ndSetW(999)===420);
   $('#trX').click();await wait(30);
   /* ★ A-6(a) 9/30 — add9 §A-2: 상주 서랍은 ✕ 로 숨지 않는다(늘 선다 · 접기만 — add9 수행 결과 표 「상주 서랍」·「접힘·너비」) — 옛 #trX 는 숨은 #tree 만 닫는다 · 본문 여백 = 서랍 폭(body.ndon) */
   T('A1 ✕(옛 #trX) → 옛 서랍만 숨김 · 상주 서랍은 선 채 · 여백 = 서랍 폭',tr.classList.contains('hide')&&!document.body.classList.contains('tropen')&&!$('#navdr').classList.contains('hide')&&getComputedStyle(document.body).paddingLeft===Math.round($('#navdr').getBoundingClientRect().width)+'px',[getComputedStyle(document.body).paddingLeft,$('#navdr').getBoundingClientRect().width]);
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
    QC.launch('new')   # 셈(§B-4) — 새 판 한 번(바탕 판 없음)
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
    _pre = s.split('/*EARTH:js*/')[0].replace("box.addEventListener('wheel',e=>{if(!e.ctrlKey)return;e.preventDefault();const r=box.getBoundingClientRect();apply(z*(e.deltaY<0?1.12:1/1.12),e.clientX-r.left,e.clientY-r.top)},{passive:false});", '', 1)   # ★ 2026-10-07 (_task_jagwa_phys_win §A-26) — 시안 ㉔ 오린 것 확대·축소(solxZoom)의 Ctrl+휠은 물리 뷰어가 아니라 정답·풀이 창 오린 그림 칸 몫 — 그 한 줄만 빼고 센다(바탕엔 그 줄 없음)
    _z0 = _pre.find('b.__zsetup=()=>{')
    _z1 = _pre.find(chr(10) + '  };' + chr(10), _z0) if _z0 >= 0 else -1
    T2('핀치·Ctrl+휠은 JG 전용 배선(b.__zsetup) 안에만 있다 — 물리 뷰어엔 wheel 핸들러 없음 그대로',
       _pre.count("addEventListener('wheel'") == 1 and _z0 >= 0 and _z1 > _z0
       and _pre.index("addEventListener('wheel'") > _z0 and _pre.index("addEventListener('wheel'") < _z1
       and "if(JG&&b.__zsetup)b.__zsetup();" in s,
       [_pre.count("addEventListener('wheel'"), _z0, _z1])
    # 판 3 ①(2026-09-08) — crop 이 붙어 지학 16 · 생물 17. 물리 12 는 그대로다(고친 자리).
    T2('SUBJ.phys SYNC_KEYS 12 무변 · earth 19 · bio 20 (add1 +bref · SUBJ 블록)', "SYNC_KEYS:['status','note','qtype','conc','gpt','twin','ansfix','frm','maskpos','omrpos','mcard','link']," in s and s.count("'bpit','bpg','crop','txt','tfix','bref'],") == 1 and "'bpg','snote','crop','txt','tfix','bref']," in s)
    if QC.SMOKE:   # smoke — smoke 칸 줄만
        lines = [x for x in lines if any((x.split(' | ') + ['', ''])[1].startswith(k) for k in _RG_SMOKE)]
    npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
    for x in lines: print(x)
    print('\n== %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)

if __name__ == '__main__':
    main()
