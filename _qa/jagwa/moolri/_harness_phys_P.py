# -*- coding: utf-8 -*-
"""물리535 서재 — P 마크 · 약점/덜약점 · 코멘트 칩·검색 하니스 (2026-09-04 · 지시서 _task_phys_mark_P.md §4)

_harness_phys.py 의 골격(CDN 스텁 · 로컬 서버 · 헤드리스 크롬 · POST /result)을 그대로 쓴다.
GitHub 은 404 로 막는다 — 기록 동기화는 이 지시서의 대상이 아니다. 원본은 건드리지 않는다.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import http.server, os, socketserver, subprocess, sys, threading

SRC = _roots.genie(r"jagwa\index.html")   # 9/5 자과 서재 이사
OUT = os.path.join(os.environ.get('TEMP', '.'), 'physhP')
os.makedirs(OUT, exist_ok=True)
APP = os.path.join(OUT, 'app.html')

STUB = """<script>
window.pdfjsLib={GlobalWorkerOptions:{},getDocument:function(){return{promise:new Promise(function(){})}}};
window.katex={render:function(){},renderToString:function(s){return s}};
window.renderMathInElement=function(){};
window.__err=[];
window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+(e.filename||'').split('/').pop()+':'+e.lineno)});
window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
</script>
"""

TESTS = r"""<script>
(function(){
 const R=[]; const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+(c?'':' | '+JSON.stringify(i===undefined?null:i)));
 const __nativeFetch=window.fetch.bind(window);
 window.fetch=async()=>({ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)});
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 const seed=(no,ms)=>{ST[no]={h:ms.map((m,i)=>({m,t:Date.now()-((ms.length-i)*1000),s:0}))}};
 const bg=el=>getComputedStyle(el).backgroundColor;
 const INK='rgb(22, 24, 27)', YEL='rgb(243, 227, 154)';
 async function run(){
  try{
   /* 뷰어를 PDF 없이 연다 — pdf.js 스텁은 영원히 안 끝나므로 그리기만 비운다 */
   renderPage=async()=>{}; setupMask=async()=>{}; paintInk=()=>{};
   ST={};CMT={};
   /* 시동 때 떠 있는 시트(첫 실행 안내 등)는 하니스 환경 산물 — 적어 두고 치운다. 키 4 는 시트가 있으면 막힌다(앱 규칙). */
   await wait(700);   /* 물리 시동 400ms 뒤 「PDF 등록」 설정 시트가 뜬다 — 그 뒤에 치워야 검사 중에 안 끼어든다(병합 판에서 시동이 느려져 드러남) */
   const stray=[...document.querySelectorAll('.sheet')].map(x=>((x.querySelector('h2')||x).textContent||'').slice(0,40));
   document.querySelectorAll('.sheet').forEach(x=>x.remove());
   T('시동 시 떠 있던 시트(기록만 · 치움): '+JSON.stringify(stray),true);

   /* ===== W-1 진리표 ===== */
   const TT=[[[],''],[['O'],''],[['X'],'weak'],[['Q'],'weak'],[['X','O'],'less'],[['X','O','O'],''],[['X','O','X'],'weak'],
             [['X','P'],'weak'],[['X','O','P'],'less'],[['X','O','P','O'],''],[['P'],''],[['O','Q','O'],'less']];
   TT.forEach(([h,exp])=>{ST[500]={h:h.map(m=>({m,t:1,s:0}))};
     T('W-1 '+JSON.stringify(h)+' → '+(exp||'없음'),weakState(500)===exp,weakState(500))});
   delete ST[500];

   /* ===== 씨앗 : 1 X · 2 X,O · 3 O · 4 Q · 5 X,X · 6 P · 7 X,O,P · 8 X,O,O · 9 O,Q,O ===== */
   seed(1,['X']);seed(2,['X','O']);seed(3,['O']);seed(4,['Q']);seed(5,['X','X']);seed(6,['P']);seed(7,['X','O','P']);seed(8,['X','O','O']);seed(9,['O','Q','O']);
   CMT[2]='경사면 마찰 방향에서 시간 씀';CMT[4]='최대정지마찰 부등호';CMT[9]='원판 굴림 마찰력 일 안 함';CMT[3]='근의공식';
   await saveST();await saveNote();
   const ST0=JSON.stringify(ST), CMT0=JSON.stringify(CMT);
   draw();
   T('R-1 draw·필터·약점 계산은 status 바이트를 안 바꾼다',JSON.stringify(ST)===ST0);

   /* ===== W-2 · P-2 · N-2 칩 ===== */
   const findChip=lab=>[...document.querySelectorAll('#fEtc .chip')].find(x=>x.textContent.trim().startsWith(lab));
   const cnt=lab=>{const c=findChip(lab);return c?+(c.querySelector('small')||{textContent:'-1'}).textContent:null};
   const expWeak=DATA.filter(r=>weakState(r[F.NO])==='weak').length, expLess=DATA.filter(r=>weakState(r[F.NO])==='less').length;
   T('W-2 칩 「⚠ 약점 n」 = 진리표 집계(3)',cnt('⚠ 약점')===expWeak&&expWeak===3,[cnt('⚠ 약점'),expWeak]);
   T('W-2 칩 「🌤 덜약점 n」(3)',cnt('🌤 덜약점')===expLess&&expLess===3,[cnt('🌤 덜약점'),expLess]);
   T('P-2 칩 「P n」 = lastM P 수(2)',cnt('P')===2,cnt('P'));
   T('N-2 칩 「메모 있음 n」(4)',cnt('메모 있음')===4,cnt('메모 있음'));
   T('기존 칩 셋 그대로 · 「안 푼 것」 은 뺐다(9/5 필터 손질 B-2)',['틀린 것','헷갈림','두 번 이상 틀림'].every(l=>!!findChip(l))&&!findChip('안 푼 것'));

   /* ===== 히트맵 ===== */
   const cell=no=>document.querySelectorAll('#spec i')[no-1];
   T('W-2 덜약점 칸 = W(연노랑) 2·7·9',cell(2).className==='W'&&cell(7).className==='W'&&cell(9).className==='W',[cell(2).className,cell(7).className,cell(9).className]);
   T('W-2 약점 칸 = 마지막 마크 색 그대로 1·4·5',cell(1).className==='X r1'&&cell(4).className==='Q r1'&&cell(5).className==='X r2',[cell(1).className,cell(4).className,cell(5).className]);
   T('P-1 P 칸 검정 6',cell(6).className==='P r1'&&bg(cell(6))===INK,[cell(6).className,bg(cell(6))]);
   const c6=cell(6);const b1=bg(c6);c6.className='P r2';const b2=bg(c6);c6.className='P r3';const b3=bg(c6);c6.className='P r1';
   T('P-1 히트맵 P r1~r3 전부 같은 검정',b1===b2&&b2===b3&&b1===INK,[b1,b2,b3]);
   T('W-2 W 칸 연노랑',bg(cell(2))===YEL,bg(cell(2)));
   T('통계 줄 P 2 · 약점 3 · 덜약점 3',$('#cP').textContent==='2'&&$('#cWk').textContent==='3'&&$('#cW').textContent==='3',[$('#cP').textContent,$('#cWk').textContent,$('#cW').textContent]);
   /* 맞음 = 마지막 마크 O 인 것(2·3·8·9 — 덜약점도 마지막은 O) · 헷갈림 4 · 틀림 1·5 */
   T('통계 줄 맞음 4·헷갈림 1·틀림 2 그대로',$('#cO').textContent==='4'&&$('#cQ').textContent==='1'&&$('#cX').textContent==='2',[$('#cO').textContent,$('#cQ').textContent,$('#cX').textContent]);

   /* ===== 필터 ===== */
   const ids=()=>filtered().map(r=>r[F.NO]);
   FL.mark='X';let L=ids();T('P-2 「틀린 것」에 lastM P 없음(1·5 만)',L.join()==='1,5',L.slice(0,10));
   FL.mark='P';L=ids();T('P-2 「P」 = 6,7',L.join()==='6,7',L);
   FL.mark='weak';L=ids();T('W-2 「약점」 = 1,4,5',L.join()==='1,4,5',L);
   FL.mark='less';L=ids();T('W-2 「덜약점」 = 2,7,9',L.join()==='2,7,9',L);
   FL.mark='';findChip('메모 있음').click();await wait(60);const memoRows=[...document.querySelectorAll('#memoSheet .memor')].map(d=>+d.dataset.no).sort((a,b)=>a-b);
   T('N-2 「메모 있음」 = 시트(9/5 필터 손질 B-3 · 필터 아님) 줄 = 2,3,4,9',!!$('#memoSheet')&&memoRows.join()==='2,3,4,9',memoRows);$('#memoX').click();await wait(10);
   T('「안 푼 것」 필터 없음(9/5 B-2) — FL.mark new 는 빈 목록',(()=>{FL.mark='new';const n=ids().length;FL.mark='';return n===0})());
   FL.mark='again';const again0=ids().join();T('「두 번 이상 틀림」 = 5',again0==='5',again0);
   FL.mark='';
   FL.q='마찰';L=ids();T('N-2 상단 검색 회귀 — 코멘트 낱말로 목록 거름(2·4·9)',L.includes(2)&&L.includes(4)&&L.includes(9),L.slice(0,10));FL.q='';

   /* ===== 목록 이력 줄 · 볼트 표기 ===== */
   draw();
   const item6=[...document.querySelectorAll('#list .item')].find(d=>d.querySelector('.num').textContent==='6');
   T('P-1 목록 이력 줄 P 검정',!!item6&&!!item6.querySelector('.mk .h i.P')&&bg(item6.querySelector('.mk .h i.P'))===INK);
   T('P-1 볼트 표기 P 읽음(XOP)',(function(){const k=Object.keys(SOL)[0];const bak=SOL[k].f;SOL[k].f='PA0001 하-테스트 XOP';const v=vaultMark(1,k);const t=vaultTitle(k);SOL[k].f=bak;return v==='XOP'&&t==='테스트'})());
   T('P-1 볼트 표기 옛 값 그대로(XO)',(function(){const k=Object.keys(SOL)[0];const bak=SOL[k].f;SOL[k].f='PA1508하-PV그래프 XO';const v=vaultMark(1,k);SOL[k].f=bak;return v==='XO'})());
   T('P-1 vmP CSS 검정',(function(){const b=document.createElement('b');b.className='vmP';document.body.appendChild(b);const c=getComputedStyle(b).color;b.remove();return c===INK})());

   /* ===== 뷰어 · 네비 서랍 ===== */
   SET.nav=true;await openView(6);await wait(30);
   T('뷰어 열림 · VNO=6 · 서랍 보임',VNO===6&&!$('#view').classList.contains('hide')&&!$('#navdr').classList.contains('hide'));
   T('P-1 #mP 넷째 버튼 · on',!!$('#mP')&&$('#mP').previousElementSibling.id==='mX'&&$('#mP').classList.contains('on'));
   T('P-1 #mP 검정 바탕 흰 글자',bg($('#mP'))===INK&&getComputedStyle($('#mP')).color==='rgb(255, 255, 255)',[bg($('#mP')),getComputedStyle($('#mP')).color]);
   const nrow=no=>document.querySelector('#ndList .ndrow[data-no="'+no+'"]');
   T('P-1 네비 ndmP',!!nrow(6).querySelector('.ndm.ndmP')&&nrow(6).querySelector('.ndm').textContent==='P');
   T('네비 △ 그대로',nrow(4).querySelector('.ndm.ndmQ').textContent==='△');
   T('W-2 네비 덜약점 점(2 만 · 1·3 없음)',!!nrow(2).querySelector('.ndw')&&!nrow(1).querySelector('.ndw')&&!nrow(3).querySelector('.ndw'));
   T('N-1 코멘트 없는 행 = 칩 0',!nrow(1).querySelector('.ndc')&&!nrow(6).querySelector('.ndc'));
   T('N-1 코멘트 있는 행 = 🗒',!!nrow(2).querySelector('.ndc')&&!!nrow(4).querySelector('.ndc')&&nrow(2).querySelector('.ndc').textContent==='🗒');

   /* ===== N-1 팝오버 ===== */
   nrow(2).querySelector('.ndc').click();await wait(30);
   T('N-1 칩 클릭 = 팝오버(전문) · 이동 아님',!!$('#ndPop')&&$('#ndPop .txt').textContent===CMT[2]&&VNO===6,[$('#ndPop')&&$('#ndPop').textContent,VNO]);
   T('N-1 팝오버가 서랍 오른쪽에 뜬다',(function(){const p=$('#ndPop').getBoundingClientRect(),d=$('#navdr').getBoundingClientRect();return p.left>=d.right&&p.top>=0})(),$('#ndPop').getBoundingClientRect());
   document.body.click();await wait(30);
   T('N-1 바깥 클릭 닫힘',!$('#ndPop'));
   nrow(2).querySelector('.ndc').click();await wait(10);nrow(2).querySelector('.ndc').click();await wait(10);
   T('N-1 같은 칩 다시 클릭 닫힘',!$('#ndPop'));
   nrow(2).querySelector('.ndc').click();await wait(10);nrow(4).querySelector('.ndc').click();await wait(10);
   T('N-1 다른 칩 클릭 = 그 코멘트로 바뀜',!!$('#ndPop')&&$('#ndPop .txt').textContent===CMT[4]);
   $('#ndFix').click();await wait(30);
   T('N-1 고치기 = noteSheet(4)',!$('#ndPop')&&!!$('#ntIn')&&$('#ntIn').value===CMT[4]&&/4번/.test(document.querySelector('.sheet h2').textContent));
   $('#ntDel').click();await wait(80);
   T('N-1 코멘트 지우면 칩 사라짐(navSync)',!CMT[4]&&!nrow(4).querySelector('.ndc')&&!document.querySelector('.sheet'));
   CMT[4]='최대정지마찰 부등호';await saveNote();navSync();
   T('N-1 코멘트 되살리면 칩 돌아옴',!!nrow(4).querySelector('.ndc'));
   nrow(3).click();await wait(60);
   T('N-1 행 클릭 이동은 그대로',VNO===3);

   /* ===== P-1 마크 ===== */
   VNO=6;await showProblem();await wait(20);
   const before=JSON.stringify(ST);
   $('#mP').click();await wait(60);
   T('P-1 #mP 클릭 → h 끝 {m:P}',hist(6).slice(-1)[0].m==='P'&&hist(6).length===2,hist(6));
   T('P-1 버튼 on · 다른 셋 off',$('#mP').classList.contains('on')&&!$('#mO').classList.contains('on')&&!$('#mQ').classList.contains('on')&&!$('#mX').classList.contains('on'));
   T('P-1 라벨 「패스」(토스트)',[...document.querySelectorAll('.toast')].some(t=>/패스/.test(t.textContent)),[...document.querySelectorAll('.toast')].map(t=>t.textContent));
   T('P-1 P 는 {m,t,s} 꼴',(x=>x.m==='P'&&typeof x.t==='number'&&'s' in x)(hist(6).slice(-1)[0]));
   VNO=3;await showProblem();await wait(20);
   document.dispatchEvent(new KeyboardEvent('keydown',{key:'4',bubbles:true}));await wait(60);
   T('P-1 키 4 → P',lastM(3)==='P'&&hist(3).length===2,hist(3));
   T('P-1 네비 ndmP 갱신(3)',nrow(3).querySelector('.ndm').classList.contains('ndmP'));
   T('약점 상태를 안 민다 — 3: 없음 그대로 · 1: 약점 그대로',weakState(3)===''&&weakState(1)==='weak');
   document.dispatchEvent(new KeyboardEvent('keydown',{key:'1',bubbles:true}));await wait(60);
   T('키 1 그대로(O)',lastM(3)==='O');

   /* ===== 이력 편집 시트 ===== */
   histSheet(6);await wait(20);
   const hb=[...document.querySelectorAll('.histrow')[1].querySelectorAll('.sel button')].map(b=>b.textContent);
   T('P-1 이력 편집 시트 넷째 버튼 「패스」',hb.join()==='맞음,헷갈림,틀림,패스',hb);
   const pon=document.querySelectorAll('.histrow')[1].querySelector('.sel button[data-m=P].on');
   T('P-1 이력 시트 P on = 검정',!!pon&&bg(pon)===INK,pon&&bg(pon));
   document.querySelectorAll('.histrow')[1].querySelector('.sel button[data-m=O]').click();await wait(60);
   T('이력 시트에서 P→O 고치기',lastM(6)==='O');
   document.querySelectorAll('.histrow')[1].querySelector('.sel button[data-m=P]').click();await wait(60);
   T('이력 시트에서 O→P 고치기',lastM(6)==='P');
   $('#hClose').click();await wait(10);

   /* ===== R-1 · again ===== */
   FL.mark='again';T('P-2 again 무변(X 만 센다)',ids().join()===again0,ids());FL.mark='';
   const ST1=JSON.parse(JSON.stringify(ST));delete ST1[6];delete ST1[3];const B=JSON.parse(before);delete B[6];delete B[3];
   T('R-1 P 찍은 문항 밖의 기록 바이트 동일',JSON.stringify(ST1)===JSON.stringify(B));
   T('R-1 note JSON 바이트 동일',JSON.stringify(CMT)===CMT0);
   T('R-1 SYNC_KEYS 12(10 + mcard · 2026-09-04 · + link 2026-09-05 필터 손질 B-4) · status·note',SYNC_KEYS.length===12&&SYNC_KEYS[0]==='status'&&SYNC_KEYS[1]==='note'&&SYNC_KEYS[10]==='mcard'&&SYNC_KEYS[11]==='link',SYNC_KEYS);
   T('R-1 exportData 함수 있음',typeof exportData==='function');

   /* ===== N-2 코멘트 시트 검색 ===== */
   VNO=2;await showProblem();await wait(10);
   noteSheet(2);await wait(20);
   const qIn=$('#ntQ');T('N-2 시트 안 검색칸(입력창 아래)',!!qIn&&!!($('#ntIn').compareDocumentPosition(qIn)&Node.DOCUMENT_POSITION_FOLLOWING));
   qIn.value='마찰';qIn.dispatchEvent(new Event('input'));await wait(60);
   T('N-2 150ms 디바운스(60ms 엔 아직 없음)',document.querySelectorAll('#ntRes .ri').length===0);
   await wait(200);
   const exp=Object.keys(CMT).filter(k=>CMT[k].toLowerCase().includes('마찰')).length;
   let ris=[...document.querySelectorAll('#ntRes .ri')];
   T('N-2 「마찰」 결과 n = CMT 전건 grep(3)',ris.length===exp&&exp===3,[ris.length,exp]);
   T('N-2 <mark> 발췌',ris.every(x=>x.querySelector('mark')&&x.querySelector('mark').textContent==='마찰'));
   T('N-2 현재 문제(2) 포함 · 번호 · 소단원',ris.some(x=>x.dataset.no==='2'&&x.querySelector('.rs').textContent===rec(2)[F.SUB]));
   T('N-2 결과에 마지막 마크',ris.find(x=>x.dataset.no==='4').querySelector('.rk.rkQ').textContent==='△'&&ris.find(x=>x.dataset.no==='9').querySelector('.rk.rkO').textContent==='O');
   T('N-2 머리줄 건수',/3건/.test($('#ntRes .rh').textContent),$('#ntRes .rh').textContent);
   qIn.value='마찰 시간';qIn.dispatchEvent(new Event('input'));await wait(250);
   T('N-2 낱말 AND(마찰 시간 → 2 만)',(ris=[...document.querySelectorAll('#ntRes .ri')]).length===1&&ris[0].dataset.no==='2');
   qIn.value='MaChal';qIn.dispatchEvent(new Event('input'));await wait(250);
   T('N-2 없는 낱말 = 0건',document.querySelectorAll('#ntRes .ri').length===0&&/0건/.test($('#ntRes .rh').textContent));
   for(let i=100;i<160;i++)CMT[i]='Test Abc '+i;
   qIn.value='abc';qIn.dispatchEvent(new Event('input'));await wait(250);
   T('N-2 소문자 비교(abc ↔ Abc) · 최대 50 + 더 보기',document.querySelectorAll('#ntRes .ri').length===50&&!!$('#ntMore')&&/60건/.test($('#ntRes .rh').textContent));
   $('#ntMore').click();await wait(20);
   T('N-2 더 보기 → 60',document.querySelectorAll('#ntRes .ri').length===60&&!$('#ntMore'));
   for(let i=100;i<160;i++)delete CMT[i];
   qIn.value='마찰';qIn.dispatchEvent(new Event('input'));await wait(250);
   document.querySelector('#ntRes .ri[data-no="4"]').click();await wait(100);
   const sheets=document.querySelectorAll('.sheet');
   T('N-2 결과 클릭 = 팝업(twinPeek · 그림 상자) · VNO 무변',sheets.length===2&&!!sheets[1].querySelector('.twbox')&&VNO===2,[sheets.length,VNO]);
   T('N-2 팝업 = 그림 + 코멘트 전문 + 마크',!!$('#twNote')&&$('#twNote').textContent.includes(CMT[4])&&!!sheets[1].querySelector('h2 .vmQ'));
   T('N-2 팝업 버튼 = 「이 문제로 가기」 하나 + 닫기',sheets[1].querySelectorAll('.btn').length===2&&$('#twGo').textContent==='이 문제로 가기');
   $('#twX').click();await wait(20);
   T('N-2 팝업 닫기 = 시트는 남고 검색어 그대로',document.querySelectorAll('.sheet').length===1&&$('#ntQ').value==='마찰');
   document.querySelector('#ntRes .ri[data-no="4"]').click();await wait(60);
   $('#twGo').click();await wait(100);
   T('N-2 「이 문제로 가기」 = 이동 · 시트 둘 다 닫힘',VNO===4&&!document.querySelector('.sheet'),[VNO,document.querySelectorAll('.sheet').length]);
   noteSheet(4);await wait(10);
   T('N-2 시트 닫으면 검색어 비움(다시 열면 빈 칸)',$('#ntQ').value===''&&$('#ntRes').innerHTML==='');
   $('#ntQ').value='마찰';$('#ntQ').dispatchEvent(new KeyboardEvent('keydown',{key:'Enter'}));await wait(20);
   T('N-2 검색칸 Enter = 즉시 검색 · 저장 아님',document.querySelectorAll('#ntRes .ri').length===3&&!!document.querySelector('.sheet'));
   $('#ntNo').click();await wait(10);
   T('R-1 검색은 note 를 안 바꾼다',JSON.stringify(CMT)===CMT0);

   /* ===== 쌍둥이 훔쳐보기 회귀 ===== */
   twinPeek(1);await wait(60);
   T('twinPeek 회귀 — 코멘트 없는 문제 = twnote 없음 · 마크 X',!$('#twNote')&&!!document.querySelector('.sheet h2 .vmX'));
   $('#twX').click();await wait(10);

   /* ===== P-2 학습로그 · 개념 통계 ===== */
   closeView();await wait(10);
   const lb=[...document.querySelectorAll('button')].find(b=>b.textContent==='📝 학습로그');lb.click();await wait(40);
   const txt=$('#plg-text').value;
   const nPh=Object.values(ST).reduce((a,v)=>a+v.h.filter(x=>x.m==='P').length,0);
   T('P-2 학습로그 P 열(합계 · P '+nPh+' = 오늘 이력의 P 수)',new RegExp('합계: .*· P '+nPh+'(\s|$)').test(txt),txt.split(String.fromCharCode(10)).slice(-2));
   T('P-2 학습로그 소단원 줄 P',/· P \d+\)/.test(txt),txt.split(String.fromCharCode(10)).slice(1,3));
   $('#plg-close').click();
   const cs=conceptStat(Object.keys(CQ)[0]||'x');
   T('P-2 conceptStat p 열',('p' in cs)&&('o' in cs)&&('n' in cs),cs);

   T('R-1 JS 오류 0',(window.__err||[]).length===0,window.__err);
  }catch(e){R.push('FAIL | 하니스가 터짐 | '+(e&&e.stack||e))}
  report(R.join('\n'));
 }
 function report(txt){
  try{__nativeFetch('/result',{method:'POST',body:txt})}catch(e){}
  const pre=document.createElement('pre');pre.id='RESULT';pre.textContent=txt;document.body.appendChild(pre);
 }
 (function w(n){if(typeof recPaint==='function'&&document.getElementById('recChip').textContent){window.__booted=1;return}
  if(n>400)return;setTimeout(()=>w(n+1),20)})(0);
 (function boot(n){
  if(typeof weakState==='function'&&typeof db!=='undefined'&&db&&window.__booted&&document.querySelectorAll('#spec i').length)return run();
  if(n>400)return report('FAIL | 앱이 시동되지 않음 | '+JSON.stringify(window.__err||[]));
  setTimeout(()=>boot(n+1),25);
 })(0);
})();
</script>
"""


def main():
    html = open(SRC, encoding='utf-8', newline='').read()
    assert '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js' in html
    html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js',
                        STUB + '<script data-off="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    html = html.replace('<script defer src="https://cdnjs', '<script defer data-off="https://cdnjs')
    html = html.replace('<link rel="stylesheet" href="https://cdnjs', '<link rel="off" href="https://cdnjs')
    assert html.rstrip().endswith('</html>')
    html = html.replace('</body>', TESTS + '</body>', 1)
    open(APP, 'w', encoding='utf-8', newline='').write(html)

    done = threading.Event()
    box = {}

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=OUT, **k)
        def log_message(self, *a, **k):
            pass
        def do_POST(self):
            n = int(self.headers.get('Content-Length') or 0)
            box['txt'] = self.rfile.read(n).decode('utf-8', 'replace')
            self.send_response(204); self.end_headers()
            done.set()

    srv = socketserver.TCPServer(('127.0.0.1', 0), H)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    prof = os.path.join(OUT, 'prof')
    url = 'http://127.0.0.1:%d/app.html' % port
    p = subprocess.Popen([chrome, '--headless=new', '--disable-gpu', '--no-first-run',
                          '--user-data-dir=' + prof, '--window-size=1280,900', url],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    got = done.wait(120)
    p.terminate()
    try:
        p.wait(10)
    except Exception:
        p.kill()
    srv.shutdown()

    if not got:
        print('결과 없음 — 120초 안에 검사가 끝나지 않았다')
        sys.exit(1)
    open(os.path.join(OUT, 'result.txt'), 'w', encoding='utf-8').write(box['txt'])
    lines = [ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()]

    # ---- 브라우저 밖 검사 (파일 층 · HEAD 와 대조) ----
    def T2(name, cond, info=''):
        lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))
    s = open(SRC, encoding='utf-8', newline='').read().replace('\r\n', '\n')
    head = subprocess.run(['git', '-C', os.path.dirname(os.path.dirname(SRC)), 'show', 'HEAD:jagwa/index.html'],
                          capture_output=True).stdout.decode('utf-8').replace('\r\n', '\n')
    fn = lambda src, name: src.split(name, 1)[1].split('\n}\n', 1)[0] if name in src else None
    line1 = lambda src, key: src.split(key, 1)[1].split('\n', 1)[0] if key in src else None
    T2('R-1 SYNC_KEYS = 과목별 표(병합) · 물리 12 = 기존 10 + mcard + link(9/5 필터 손질)', line1(s, 'const SYNC_KEYS=').startswith("CARD_LAYER?CUR.SYNC_KEYS") and "phys:{DB:'phys535', PDF_DIR:'phys/pdf/', REC_PATH:'phys/기록.json', SYNC_PREFIX:'phys_sync_'," in s and "SYNC_KEYS:['status','note','qtype','conc','gpt','twin','ansfix','frm','maskpos','omrpos','mcard','link']," in s)
    T2('R-1 exportData 함수 바이트 동일(v2 꼴 무변)', fn(s, 'async function exportData(') == fn(head, 'async function exportData('))
    T2('R-1 syncRecords 함수 바이트 동일', fn(s, 'async function syncRecords(') == fn(head, 'async function syncRecords('))
    T2('상단 검색(pass 의 FL.q 줄) 무변',
       [l for l in s.split('\n') if 'noteOf(r[F.NO]).includes(FL.q)' in l] == [l for l in head.split('\n') if 'noteOf(r[F.NO]).includes(FL.q)' in l])
    T2('기록 꼴 주석 그대로(새 키 없음)', "let ST={};            // no -> {h:[{m:'O'|'X'|'Q', t:ts, s:초}]}" in s)
    T2('조판기·화학 무접촉(이 파일은 phys 뿐)', 'minbeop' not in s and 'chem/' not in s)
    T2('P11 파일 전체 백틱 수가 짝', s.count('`') % 2 == 0, s.count('`'))
    raw = open(SRC, 'rb').read()
    T2('CRLF 만(줄끝 섞임 없음)', raw.count(b'\r\n') == raw.count(b'\n'))

    npass = sum(1 for x in lines if x.startswith('PASS'))
    nfail = len(lines) - npass
    for x in lines:
        print(x)
    print('\n== %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
