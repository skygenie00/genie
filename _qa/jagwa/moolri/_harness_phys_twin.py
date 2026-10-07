# -*- coding: utf-8 -*-
"""물리535 — 쌍둥이 미리보기 필기 · 떠 있는 창 · 서랍 손잡이 · 손필기 암기카드 하니스 (2026-09-04 · _task_phys_twin_drawer.md T-1~T-9)

_harness_phys.py 골격(로컬 서버 · 헤드리스 크롬 · POST /result). pdf.js 는 **진짜 CDN**(회전 문항 좌표를 재야 한다) · KaTeX 스텁 · GitHub 404.
빈 PDF 한 장을 IndexedDB pdf/111 에 넣고 그 위에서 미리보기·필기·회전을 잰다. 원본 무접촉.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import http.server, os, socketserver, subprocess, sys, threading, shutil
from pypdf import PdfWriter

SRC = _roots.genie(r"jagwa\index.html")   # 9/5 자과 서재 이사
OUT = os.path.join(os.environ.get('TEMP', '.'), 'physhT'); os.makedirs(OUT, exist_ok=True)
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
 const px=(cv,fx,fy)=>{const d=cv.getContext('2d').getImageData(Math.round(fx*cv.width),Math.round(fy*cv.height),1,1).data;return [d[0],d[1],d[2]]};
 const reddish=p=>p[0]>150&&p[0]-p[1]>40;
 const white=p=>p[0]>245&&p[1]>245&&p[2]>245;
 const ptr=(el,type,x,y,extra)=>el.dispatchEvent(new PointerEvent(type,Object.assign({bubbles:true,cancelable:true,clientX:x,clientY:y,pointerId:1,pointerType:'mouse',isPrimary:true,button:0},extra||{})));
 /* ★ A-6(a) 9/30 — 9/13 펜/손가락 가름(moolri/_task_jagwa_pen_touch2.md §1 「SET.pencil … ⇒ if(pointerType!=='pen') return」 · 수행 결과 §6-5 표 「암기카드 mcardWin — pen 필기 · touch·mouse 조작」 · genie c62b2b2 · 결정로그 2026-09-13):
    카드 캔버스(#mcc)는 펜만 긋는다(앱 4856) — 그 캔버스에 긋는 끌기만 pointerType 'pen' 으로 던진다(창 제목줄·모서리·서랍 손잡이 끌기는 마우스 그대로) */
 const drag=async(el,x0,y0,x1,y1)=>{const X=(el&&el.id==='mcc')?{pointerType:'pen'}:undefined;ptr(el,'pointerdown',x0,y0,X);await wait(10);ptr(el,'pointermove',(x0+x1)/2,(y0+y1)/2,X);await wait(10);ptr(el,'pointermove',x1,y1,X);await wait(10);ptr(el,'pointerup',x1,y1,X);await wait(30)};
 async function run(){
  try{
   renderPage=async()=>{};setupMask=async()=>{};paintInk=()=>{};
   ST={};CMT={};
   document.querySelectorAll('.sheet').forEach(x=>x.remove());
   /* 빈 PDF 한 장을 111 로 등록 */
   const buf=await (await __nativeFetch('/blank.pdf')).arrayBuffer();await put('pdf','111',buf);await loadHave();
   const q1=DATA.find(r=>r[F.FILE]==='111'), q2=DATA.filter(r=>r[F.FILE]==='111')[3];
   const no=q1[F.NO], no2=q2[F.NO];
   const INK0={0:[{c:'#B03A2E',w:2,hl:0,p:[0.1,0.1,0.3,0.1]}],1:[{c:'#B03A2E',w:2,hl:0,p:[0.5,0.55,0.6,0.55]}]};
   await put('ink',String(no),INK0);
   const inkBefore=JSON.stringify(await get('ink',String(no)));
   /* ===== T-1 필기가 그려짐 · 없으면 차 0 ===== */
   twinPeek(no);await wait(1500);
   let cv=$('#twc');
   T('T-1 미리보기 캔버스 렌더(PDF 111)',!!cv&&cv.width>100,cv&&cv.width);
   T('T-1 현재 층 획이 보임 (0.55W,0.55H) 붉음',reddish(px(cv,0.55,0.55)),px(cv,0.55,0.55));
   T('T-1 옛 층 획 자리 (0.2W,0.1H) 흰색 아님',!white(px(cv,0.2,0.1)),px(cv,0.2,0.1));
   T('T-1 빈 자리 (0.8W,0.8H) 흰색',white(px(cv,0.8,0.8)),px(cv,0.8,0.8));
   $('#twX').click();await wait(20);
   twinPeek(no2);await wait(1200);cv=$('#twc');
   T('T-1 필기 없는 문항 = 획 없음(표본 3점 흰색)',white(px(cv,0.55,0.55))&&white(px(cv,0.2,0.1))&&white(px(cv,0.5,0.5)));
   $('#twX').click();await wait(20);
   /* ===== T-2 옛 층 알파 0.30 · HIDEOLD ===== */
   twinPeek(no);await wait(1200);cv=$('#twc');
   const pOld=px(cv,0.2,0.1),pCur=px(cv,0.55,0.55);
   T('T-2 옛 층은 옅고(g>150) 현재 층은 진함(g<110)',pOld[1]>150&&pCur[1]<110,[pOld,pCur]);
   $('#twX').click();await wait(20);
   HIDEOLD=true;twinPeek(no);await wait(1200);cv=$('#twc');
   T('T-2 HIDEOLD 켜면 옛 층 안 그림 · 현재 층은 그림',white(px(cv,0.2,0.1))&&reddish(px(cv,0.55,0.55)),[px(cv,0.2,0.1),px(cv,0.55,0.55)]);
   HIDEOLD=false;$('#twX').click();await wait(20);
   /* ===== T-1 회전 90 ===== */
   SET.rot['111']=90;twinPeek(no);await wait(1500);cv=$('#twc');
   /* toPix(u,v) rot90 = ((1-v)W, uH): 현재 층 (0.55,0.55)→(0.45W,0.55H) · 옛 층 (0.2,0.1)→(0.9W,0.2H) */
   T('T-1 회전 90: 획이 뷰어 규칙 자리에(0.45W,0.55H 붉음 · 0.9W,0.2H 흰색 아님 · 0.55W,0.55H 흰색)',reddish(px(cv,0.45,0.55))&&!white(px(cv,0.9,0.2))&&white(px(cv,0.55,0.55)),[cv.width,cv.height,px(cv,0.45,0.55),px(cv,0.9,0.2),px(cv,0.55,0.55)]);
   T('T-1 회전 캔버스 = 가로가 세로보다 김',cv.width>cv.height);
   SET.rot['111']=0;$('#twX').click();await wait(20);
   T('T-6 ink 저장소 무변(읽기만)',JSON.stringify(await get('ink',String(no)))===inkBefore);
   /* ===== T-3 팝업 끌기 · 크기 · 자리 기억 ===== */
   twinPeek(no);await wait(1000);
   let panel=$('.sheet.twin .panel'),h2=panel.querySelector('h2'),r0=panel.getBoundingClientRect();
   T('T-3 제목줄 = 손잡이(twhandle) · 모서리 그립 있음',h2.classList.contains('twhandle')&&!!panel.querySelector('.twgrip'));
   await drag(h2,r0.left+40,r0.top+10,r0.left+140,r0.top-150);
   let r1=panel.getBoundingClientRect();
   T('T-3 제목줄 끌기 → left/top 바뀜 · float',panel.classList.contains('float')&&Math.abs(r1.left-(r0.left+100))<3&&r1.top<r0.top-100,[r0.left,r1.left,r0.top,r1.top]);
   const grip=panel.querySelector('.twgrip'),g0=grip.getBoundingClientRect();
   await drag(grip,g0.left+10,g0.top+10,g0.left+70,g0.top+50);
   let r2=panel.getBoundingClientRect();
   T('T-3 모서리 끌기 → 크기 바뀜',Math.abs(r2.width-(r1.width+60))<3&&Math.abs(r2.height-(r1.height+40))<3,[r1.width,r2.width,r1.height,r2.height]);
   T('T-3 캔버스는 CSS 로 늘어남(재렌더 없음)',$('#twc').width===cv.width&&getComputedStyle($('#twc')).width===Math.round($('.twbox').clientWidth)+'px');
   $('#twX').click();await wait(20);
   twinPeek(no);await wait(800);panel=$('.sheet.twin .panel');let r3=panel.getBoundingClientRect();
   T('T-3 닫았다 다시 열면 자리·크기 유지',Math.abs(r3.left-r2.left)<2&&Math.abs(r3.width-r2.width)<2,[r2.left,r3.left]);
   $('.sheet.twin').dispatchEvent(new MouseEvent('click',{bubbles:true}));await wait(20);
   T('T-3 배경 클릭 닫힘',!$('.sheet.twin'));
   /* 크기 하한·상한 */
   twinPeek(no);await wait(600);panel=$('.sheet.twin .panel');const gg=panel.querySelector('.twgrip'),gr=gg.getBoundingClientRect();
   await drag(gg,gr.left+5,gr.top+5,gr.left-2000,gr.top-2000);let r4=panel.getBoundingClientRect();
   T('T-3 최소 280×200',Math.round(r4.width)===280&&Math.round(r4.height)===200,[r4.width,r4.height]);
   $('#twX').click();await wait(20);
   /* ===== T-4 다른 시트 무변 ===== */
   /* ★ A-6(a) 9/30 — 셸 add16(0bee72b): 쌍둥이 잇기(twinSheet)는 「보는 시트」라 떠 있는 창(.sheet.shfloat#sh-twin · makeFloat 그립)으로 뜬다 ·
      phone_win A-5(fb89ad2): 그 창 아래 「닫기」(#twNo)는 걷었다(✕ = .shx) · ⚠ 옛 선택자 '.sheet:not(.twin) .panel' 은 앞에 선 #book(.sheet) 을 잡는다 → 창 id 로 */
   twinSheet(no);await wait(20);let p4=$('#sh-twin .panel');
   T('T-4 쌍둥이 잇기 = 떠 있는 창(셸 add16 · float · 그립 있음)',!!p4&&p4.classList.contains('float')&&!!p4.querySelector('.twgrip'));
   $('#sh-twin .shx').click();await wait(10);
   /* ★ A-6(a) 9/30 — 셸 add16(0bee72b): 마크 이력(histSheet)도 「보는 시트」라 떠 있는 창(#sh-hist · makeFloat 그립)으로 뜬다(add16 §A-1 · 수행 결과 68줄 「histSheet 회독 이력 | hist | ○」 · 앱 SHWIN ['histSheet','hist']) —
      옛 선택자 '.sheet .panel' 대신 창 id 로 · 위 쌍둥이 잇기와 같은 새 기대 · 설정 시트는 모달 그대로라(add16 §A-5) 아래 칸 무변 */
   histSheet(no);await wait(20);p4=$('#sh-hist .panel');
   T('T-4 마크 이력 = 떠 있는 창(셸 add16 · float · 그립 있음)',(!!p4&&p4.classList.contains('float')&&!!p4.querySelector('.twgrip'))||(!p4&&!!$('#hsPop')&&!document.getElementById('sh-hist'))/* ★ 2026-10-07 (_task_jagwa_phys_win §A-18·A-19) — 회독 기록 = 단추 옆 작은 창 #hsPop(시트 아님 · SHWIN 에서 뺌) → 새 판은 #hsPop · sh-hist 없음 */);
   ($('#sh-hist .shx')||$('#hsPop #hsX')).click();await wait(10);   /* ★ 2026-10-07 (_task_jagwa_phys_win §A-18) — 새 판은 #hsPop 의 ✕(#hsX)로 닫는다 */   /* ★ A-6(a) 9/30 — phone_win A-5: 떠 있는 창(add16 · histSheet = sh-hist)의 「닫기」(#hClose)도 걷었다 → ✕ 로 닫는다(안 고치면 여기서 다시 터진다 · 위 「마크 이력」 칸 기대는 이 무리 목록 밖이라 그대로) */
   $('#btnSet').click();await wait(20);p4=$('.sheet .panel');
   T('T-4 설정 시트 그대로',!!p4&&getComputedStyle(p4).position==='static'&&!p4.querySelector('.twgrip'));
   $('#bClose').click();await wait(10);
   /* ===== T-5 서랍 손잡이 ===== */
   SET.nav=true;await openView(no);await wait(40);
   const dr=$('#navdr'),grp=$('#ndGrip');
   T('T-5 #ndX 없음 · #ndGrip 있음 · 서랍 보임',!$('#ndX')&&!!grp&&!dr.classList.contains('hide')&&$('#view').classList.contains('ndopen'));
   const w0=dr.getBoundingClientRect().width,gb=grp.getBoundingClientRect();
   await drag(grp,gb.left+6,gb.top+200,gb.left+106,gb.top+200);
   const w1=dr.getBoundingClientRect().width;
   T('T-5 끌기 → 너비 +100 · SET.ndw 저장',Math.abs(w1-(w0+100))<3&&SET.ndw===Math.round(w1)&&((await get('kv','set'))||{}).ndw===SET.ndw,[w0,w1,SET.ndw]);
   await drag(grp,gb.left+6,gb.top+200,gb.left+900,gb.top+200);
   T('T-5 상한 420',Math.round(dr.getBoundingClientRect().width)===420,dr.getBoundingClientRect().width);
   await drag(grp,gb.left+6,gb.top+200,gb.left-900,gb.top+200);
   T('T-5 하한 160',Math.round(dr.getBoundingClientRect().width)===160);
   T('T-5 본문 여백이 따라감(≥900px)',getComputedStyle($('#stage')).paddingLeft==='160px',getComputedStyle($('#stage')).paddingLeft);
   ptr(grp,'pointerdown',gb.left+6,gb.top+200);await wait(10);ptr(grp,'pointermove',gb.left+8,gb.top+201);ptr(grp,'pointerup',gb.left+8,gb.top+201);await wait(30);
   /* ★ A-6(a) 9/30 — 셸 add9 §A-2(68216cf): 서랍은 첫 화면 상주 서랍 — #ndGrip 탭 = 숨기기가 아니라 접기(.fold · 13px · 손잡이 남음) · 접힘은 기기별 localStorage(ND_FOLD_K = jagwa.nd.fold.<과목>)에 · SET.nav 는 안 바뀐다(add9 수행 결과 78줄 · 앱 3718~3722 onTap ndResFold) */
   T('T-5 탭(4px 미만) → 접힘(상주 서랍 · .fold · 손잡이 남음 · 기기별 기억)',dr.classList.contains('fold')&&!dr.classList.contains('hide')&&localStorage.getItem(ND_FOLD_K)==='1',[dr.className,localStorage.getItem(ND_FOLD_K)]);
   $('#navTg').click();await wait(30);
   T('T-5 navTg 로 다시 열림 · 너비 유지',!dr.classList.contains('hide')&&Math.round(dr.getBoundingClientRect().width)===160);
   $('#view').style.removeProperty('--ndw');SET.ndw=300;ndSetW(SET.ndw);
   T('T-5 새로고침 흉내(SET.ndw → ndSetW) 너비 300',Math.round(dr.getBoundingClientRect().width)===300);
   /* ===== T-6 · T-9 SYNC ===== */
   T('T-6 SYNC_KEYS 14(필터 손질 9/5: +link 열두째) · mcard 열한째',/* ★ A-6(a) 9/30 — 셸 본판 §E-7(c9faff2): 물리 SYNC_KEYS 끝에 gg·ggref(열셋째·열넷째 · 앱 8168~8169) *//* ★ 합치기 10/1(하위 에이전트 C) — physphone A-2(97883ef) 물리 SYNC 키 끝에 tfix 하나 */(SYNC_KEYS.length===14||(SYNC_KEYS.length===15&&SYNC_KEYS[14]==='tfix')||(SYNC_KEYS.length===16&&SYNC_KEYS.slice(14).sort().join()==='solx,tfix')/* ★ 2026-10-07 (_task_jagwa_phys_win §A-30 ㉖) — 물리 SYNC 키 끝에 오린 것 solx 하나 더(tfix 와 둘) */)&&SYNC_KEYS[12]==='gg'&&SYNC_KEYS[13]==='ggref'&&SYNC_KEYS[10]==='mcard'&&SYNC_KEYS[11]==='link'&&SYNC_REF.mcard.g()===MC&&SYNC_REF.link.g()===LK);
   /* ===== T-7 카드 쓰기 ===== */
   mcardWin(no);await wait(60);
   const mc=$('#mcc');T('T-7 카드 창 = 문제명 · 코멘트 · 캔버스 · 도구',!!$('.mcwin')&&$('.mcwin h2').textContent.includes(String(no))&&!!$('.mcnote')&&!!mc&&$$('.mct [data-t]').length===3);
   const rc=mc.getBoundingClientRect();
   await drag(mc,rc.left+20,rc.top+20,rc.left+120,rc.top+80);await wait(400);
   T('T-7 획 → MC[no] · 1/1000 정수',!!MC[no]&&MC[no].s.length===1&&MC[no].s[0].p.every(v=>Number.isInteger(v)&&v>=0&&v<=1000)&&MC[no].w>0,MC[no]);
   T('T-7 kv mcard 되읽기',JSON.stringify(((await get('kv','mcard'))||{})[no])===JSON.stringify(MC[no]));
   T('T-7 캔버스에 획 픽셀',(()=>{const d=mc.getContext('2d').getImageData(0,0,mc.width,mc.height).data;let n=0;for(let i=3;i<d.length;i+=4)if(d[i]>0)n++;return n>50})());
   /* 20KB 상한 */
   const big={c:'#16181B',w:2,hl:0,p:[]};for(let i=0;i<3400;i++)big.p.push(i%1000,(i*7)%1000);
   MC[no].s.push(big);await saveMC();const szBefore=JSON.stringify(MC[no]).length;
   await drag(mc,rc.left+30,rc.top+30,rc.left+150,rc.top+90);await wait(200);
   const toasts=[...document.querySelectorAll('.toast')].map(t=>t.textContent);
   T('T-7 20KB 상한 — 저장 안 함 · 토스트',szBefore>15000&&JSON.stringify(MC[no]).length===szBefore&&toasts.some(t=>/20KB/.test(t)),[szBefore,JSON.stringify(MC[no]).length,toasts]);
   MC[no].s.pop();await saveMC();await wait(300);
   T('T-7 문항 필기 ink 무변',JSON.stringify(await get('ink',String(no)))===inkBefore);
   /* 지우개 */
   $('.mct [data-t="erase"]').click();const p0=MC[no].s[0].p;const rc2=mc.getBoundingClientRect();   /* 상태줄이 바뀌며 캔버스가 움직였을 수 있다 */
   await drag(mc,rc2.left+p0[0]/1000*rc2.width,rc2.top+p0[1]/1000*rc2.height,rc2.left+p0[0]/1000*rc2.width+2,rc2.top+p0[1]/1000*rc2.height+2);await wait(400);
   T('T-7 지우개 → 획 지워지고 카드 삭제',!MC[no]&&!((await get('kv','mcard'))||{})[no],[MC[no]&&MC[no].s.map(s=>s.p.slice(0,4)),p0.slice(0,4),rc.width,rc.height,mc.getBoundingClientRect().left-rc.left,mc.getBoundingClientRect().top-rc.top]);
   $('.mct [data-t="pen"]').click();{const r3=mc.getBoundingClientRect();await drag(mc,r3.left+20,r3.top+20,r3.left+120,r3.top+80)}await wait(400);
   T('T-7 다시 씀',!!MC[no]);
   /* 창 끌기 재사용 */
   const mh=$('.mcwin h2'),mr=$('.mcwin .panel').getBoundingClientRect();await drag(mh,mr.left+30,mr.top+10,mr.left+130,mr.top-40);
   T('T-7 카드 창도 끌림(float)',$('.mcwin .panel').classList.contains('float')&&Math.abs($('.mcwin .panel').getBoundingClientRect().left-(mr.left+100))<3);
   /* 문항 넘기면 닫힘 */
   go(1);await wait(60);T('T-7 문항 넘기면 카드 창 닫힘',!$('.mcwin'));
   /* ===== T-8 단원줄 시트 ===== */
   const sub=q1[F.SUB];CMT[no]='카드 코멘트';await saveNote();
   closeView();await wait(30);
   const gh=[...document.querySelectorAll('#list .grouphd .ghbtn')].find(b=>b.textContent.startsWith('암기카드'));
   const nExp=DATA.filter(r=>r[F.SUB]===sub&&MC[r[F.NO]]).length;
   const ghSub=[...document.querySelectorAll('#list .grouphd')].find(h=>h.textContent.includes(sub));
   const ghBtn=ghSub&&[...ghSub.querySelectorAll('.ghbtn')].find(b=>b.textContent.startsWith('암기카드'));
   /* ★ A-6(a) 9/30 — 지학 listpop_add1 §C(44줄 「🃏 가 갈음하는 것 = 절 머리 「암기카드 N」 단추 … mcardSheet 함수는 남긴다」 · cd248a5)가 셸 이식(c9faff2)으로 물리에도 — 절 머리 단추(.ghbtn)는 🃏 칩(.jcard[data-mc] · 누르면 🃏 창)이 갈음했다 ·
      종이 모아보기 mcardSheet 는 남았다 — 그 단추가 부르던 그대로 mcardSheet(sub,sub) 를 직접 부른다(첫 바퀴 mcsheet 선례 · 화면에서 여는 길은 없다 · 아래 시트 잣대 그대로) */
   const ghC=ghSub&&ghSub.querySelector('.jcard[data-mc]');
   T('T-8 단원줄 🃏 칩(옛 「암기카드 N」 · listpop_add1 §C) = 카드 있는 문항 수',!ghBtn&&!!ghC&&ghC.textContent==='🃏 '+nExp&&nExp===1,[!!ghBtn,ghC&&ghC.textContent]);
   mcardSheet(sub,sub);await wait(60);
   const cards=$$('.sheet .mcard');
   T('T-8 시트: 문항마다 카드 · 카드 있는 것 수 = mcard 수',cards.length===DATA.filter(r=>r[F.SUB]===sub).length&&$$('.sheet .mcard:not(.empty)').length===nExp,[cards.length,$$('.sheet .mcard:not(.empty)').length]);
   const my=$('.sheet .mcard[data-no="'+no+'"]');
   T('T-8 카드 = 문제명(마크 배지) · 코멘트 · 필기 순',[...my.children].map(x=>x.className).join(',')==='t,c,k'&&my.querySelector('.t b').textContent.startsWith(no+'.')&&my.querySelector('.c').textContent.includes('카드 코멘트')&&!!my.querySelector('.k canvas'));
   T('T-8 카드 없는 문항 = 「카드 없음」 자리',$$('.sheet .mcard.empty .k').every(k=>/카드 없음/.test(k.textContent)));
   T('T-8 볼트 카드 줄 「볼트 카드 0장」',/볼트 카드 \d+장/.test($('#mcVault').textContent));
   $('#mcSort').click();await wait(20);T('T-8 정렬 토글 마크순',/마크순/.test($('#mcSort').textContent));
   my.click();await wait(30);T('T-8 누르면 크게(읽기)',!!$('#mcb'));$('#mcBX').click();await wait(10);
   ptr($('.sheet .mcard[data-no="'+no+'"]'),'pointerdown',0,0);await wait(550);
   T('T-8 길게 누르면 그 문제로',VNO===no&&!$('#view').classList.contains('hide'),VNO);
   /* ===== T-9 동기화 도장 ===== */
   stampAll();const U=lsObj(U_KEY);
   T('T-9 mcard 가 도장을 탄다(u 키 mcard|no)',!!U['mcard|'+no],Object.keys(U).filter(k=>k.startsWith('mcard')));
   delete MC[no];await saveMC();stampAll();
   T('T-9 지우면 묘비(gone)',!!lsObj(GONE_KEY)['mcard|'+no]);
   T('M-1 과목 phys · IndexedDB phys535 · 저장소 셋(pdf·ink·kv) · SYNC_KEYS 14(9/5 필터 손질 +link · 9/21 셸 +gg·ggref)',SUBJ_ID==='phys'&&db.name==='phys535'&&[...db.objectStoreNames].sort().join()==='ink,kv,pdf'&&/* ★ A-6(a) 9/30 — 셸 본판 §E-7(c9faff2): 물리 SYNC_KEYS 끝에 gg·ggref(앱 8168~8169) *//* ★ 합치기 10/1(하위 에이전트 C) — physphone A-2(97883ef) 물리 SYNC 키 끝에 tfix 하나 */(SYNC_KEYS.length===14||(SYNC_KEYS.length===15&&SYNC_KEYS[14]==='tfix')||(SYNC_KEYS.length===16&&SYNC_KEYS.slice(14).sort().join()==='solx,tfix')/* ★ 2026-10-07 (_task_jagwa_phys_win §A-30 ㉖) — 물리 SYNC 키 끝에 오린 것 solx 하나 더(tfix 와 둘) */)&&SYNC_KEYS[12]==='gg'&&SYNC_KEYS[13]==='ggref'&&document.body.dataset.subj==='phys',[db.name,[...db.objectStoreNames]]);
   const gd=id=>getComputedStyle($(id)).display;
   /* ★ A-6(a) 9/30 — 셸 add9 §A-1(68216cf): 「목차」 단추 #btnTree 는 걷었다(없는 요소에 getComputedStyle → 하니스가 터짐) — 그 조건만 「없다」로(첫 바퀴 earth M-4 와 같은 고침) · 옛 #tree 는 숨은 채(treeOpen 빈 함수) */
   T('M-4 게이트(물리): 지학 조각 숨김(ebody·tBook·sub · bookpane 은 ebody 안) · #tree 는 숨은 채(.hide · 상주 서랍이 갈음) · 「목차」 단추 #btnTree 는 걷음(add9 §A-1)',gd('#ebody')==='none'&&gd('#tree')==='none'&&$('#tree').classList.contains('hide')&&$('#bookpane').offsetParent===null&&!$('#btnTree')&&gd('#tBook')==='none'&&gd('#sub')==='none',[gd('#ebody'),gd('#tree'),$('#bookpane').offsetParent,!!$('#btnTree'),gd('#tBook'),gd('#sub')]);
   T('M-4 게이트(물리): 물리 도구 보임(stage·tTheory·tCard)',gd('#stage')!=='none'&&gd('#tTheory')!=='none'&&gd('#tCard')!=='none',[gd('#stage'),gd('#tTheory'),gd('#tCard')]);
   /* ★ A-6(a) 9/30 — 셸 이식(c9faff2 · 층 문 if(CARD_LAYER) → if(SHELL)): 카드 층 블록이 물리에서도 돌아 loadEarthData(앱 5352)·unitStats(5767)가 물리에도 만들어진다 —
      물리 무변은 「안 만든다」가 아니라 「카드 층 갈래를 안 탄다」(CARD_LAYER·HASBOOK 거짓 · loadEarthData 는 if(CARD_LAYER) 에서만 부름 — 앱 4734)로 선다(첫 바퀴 bref·bookrows_pin Y-1 과 같은 옮김) */
   T('M-4 게이트(물리): 지학 함수는 SHELL 블록이라 있어도 물리는 카드 층 갈래를 안 탄다(CARD_LAYER·HASBOOK 거짓) · buildTree·treePick 물리 것 · .sheet 잔존 0',CARD_LAYER===false&&HASBOOK===false&&typeof buildTree==='function'&&typeof treePick==='function'&&document.querySelectorAll('.sheet').length===0,[typeof loadEarthData,typeof unitStats,typeof buildTree,document.querySelectorAll('.sheet').length]);
   T('머리 = 「자과 서재 · 물리」 · <title> 자과 서재(생물 판 2 add4 · 9/5: 앱 이름 하나 · SUBJ.phys.TITLE 「물리 535 서재」는 그대로) · 탭 셀 현재 = 물리 · 셀 셋 · 생물 살아 있음(앱 판 1 · 9/5) · data-layer=pdf',document.title==='자과 서재'&&$('.brand h1').textContent==='자과 서재 · 물리'&&SUBJ.phys.TITLE==='물리 535 서재'&&$('#subjTabs .on').textContent==='물리'&&$$('#subjTabs button').map(b=>b.textContent).join('│')==='물리│생물│지학'&&!$('#subjTabs [data-subj=bio]').classList.contains('off')&&document.body.dataset.layer==='pdf'&&CARD_LAYER===false);
   /* 생물 앱 판 1(9/5): 생물 셀은 켜졌다 — 클릭은 새로고침이라 reload=false 로만 검산 · 물리로 되돌린다 */
   T('A-2(물리) 생물 켜짐: subjSwitchTo(bio,false) → subj=bio · 되돌리면 phys',subjSwitchTo('bio',false)===true&&localStorage.getItem('subj')==='bio'&&subjSwitchTo('phys',false)===true&&subjResolve(localStorage.getItem('subj'))==='phys',localStorage.getItem('subj'));
   T('JS 오류 0',(window.__err||[]).length===0,window.__err);
  }catch(e){R.push('FAIL | 하니스가 터짐 | '+(e&&e.stack||e))}
  report(R.join('\n'));
 }
 function report(txt){try{__nativeFetch('/result',{method:'POST',body:txt})}catch(e){}}
 (function boot(n){
  if(typeof syncRecords==='function'&&typeof db!=='undefined'&&db&&typeof recPaint==='function'&&document.getElementById('recChip').textContent&&typeof pdfjsLib!=='undefined'&&pdfjsLib.getDocument)return setTimeout(run,200);
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
    T2('#ndX 없음(HTML·JS)', 'id="ndX"' not in s and "$('#ndX')" not in s)
    npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
    for x in lines: print(x)
    print('\n== %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)

if __name__ == '__main__':
    main()
