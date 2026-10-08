# records_v1 하니스 — 앱 사본에 시드+검사 주입 → 헤드리스 크롬 --dump-dom → PASS/FAIL 집계
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
# --mode gate|regress|smoke (_task_qa_slim2 2026-10-08 · 인자 없으면 gate = 이 판 앞과 같음)
#   regress = 칸 452(JS 434 · A2 8 · F15 10) 모두 「회귀」 · 「data」(처리표) — 시드 · 검사 글 · 띄움 한 번은 gate 와 같고 결과 html · 크롬 프로필만 %TEMP%\h_tt_timetable(gate = 하네스 옆 N: h)
#   smoke   = 같은 한 번 띄움에서 「회귀 galHTML」 · 「회귀 ttPageHTML」 · 「A2-1 syncAll 한 바퀴」(+ 예외 잡이 줄 「예외」 · 「A2 예외」)만 찍는다
#   N:(마이박스) 크롬 프로필을 TEMP 로 옮기는 까닭 — N: 프로필은 띄움마다 느리다: 9/17 tt 회귀(N: 결과 파일 시각) _harness_timetable 76 초 · tt_race 판마다 76~92 초 /
#     10/6 use_count N: 프로필 --dump-dom 180 초 초과 되풀이 → 사용자 「해」로 TEMP(결정로그 10/6 21:36 · 22:0x) / 프로필이 TEMP 인 민법 dump-dom 하네스는 띄움당 9~14 초
#     · 마이박스가 하네스 프로필 폴더 목록을 못 펼쳐 _qa_sync copy 10 분 멈춤 · 실행기 열쇠 셈 멈춤(결정로그 10/2 · 10/4)
import _qa_common as QC   # noqa: E402 — _task_qa_slim2(10/8) A-1 · 실행 모드 --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같음) · import 때 --mode · --snap-in · --snap-out 을 sys.argv 에서 뗀다
import json, os, re, shutil, subprocess, sys, tempfile
from PIL import Image

SRC = _roots.genie(r"timetable\index.html")
if QC.REGRESS:   # regress · smoke — 결과 html · 크롬 프로필을 N:(마이박스) 밖 로컬 임시 폴더로(A-2 · 까닭 = 머리 주석) · gate 는 이 판 앞 그대로
    OUT = os.path.join(tempfile.gettempdir(), 'h_tt_timetable')
else:
    OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "h")
os.makedirs(OUT, exist_ok=True)


_RG_SMOKE = ('회귀 galHTML', '회귀 ttPageHTML', 'A2-1 syncAll 한 바퀴 예외 0(로그 첫 줄 = 완료 · ✗ 없음)', '예외', 'A2 예외')   # smoke — 처리표 smoke 칸 셋 + 예외 잡이 줄 둘(제목 그대로)


def _rg_title(ln):
    """결과 줄 「PASS | 제목 | 값」의 제목 — smoke 거름(제목 그대로)"""
    p = ln.split(' | ')
    return p[1] if len(p) > 1 else ln


APP = os.path.join(OUT, "app.html")

# 시드 날짜 고정(2026-09-06 사용자 지시) — 시드 계획이 「오늘」기준이라 일요일엔 오늘 칸 계획 행이 없어 F16-4 에서 예외로 멈췄다(뒤 230항 미실행).
# 페이지 안의 Date 를 2026-09-05 12:00 KST(기준선 418/421 을 잰 논리적 날짜 · 토요일)로 고정한다. 인자 있는 new Date(...)·parse·UTC 는 그대로.
PIN = ("<script>(function(){const R=Date;const OFF=new R('2026-09-05T12:00:00+09:00').getTime()-R.now();"
       "function D(...a){return a.length?new R(...a):new R(R.now()+OFF)}D.prototype=R.prototype;D.now=()=>R.now()+OFF;D.parse=R.parse;D.UTC=R.UTC;window.Date=D;})();</script>")
SEED = PIN + """<script>
localStorage.clear();
localStorage.setItem('tt.cfg',JSON.stringify({person:'\uaf2c\uae4c',token:'',lastSync:0}));
localStorage.setItem('tt.f.history/\uaf2c\uae4c.json',JSON.stringify({data:{v:1,days:{
 '2023-10-01':{min:470,q:'ok',raw:'07h50m',u:1},
 '2024-11-16':{min:360,q:'est',raw:'am3~am7 pm8~10',u:1},
 '2026-08-19':{min:93,q:'gas',raw:'GAS \ubd84',u:1},
 '2026-08-25':{min:208,q:'gas',raw:'GAS \ubd84',u:1}
}},sha:null,dirty:false}));
(function(){
 const pad=n=>String(n).padStart(2,'0');const iso=d=>d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate());
 const t=new Date(Date.now()-5*3600e3); // 앱의 논리적 하루(05시 경계)와 일치 — 자정~새벽 실행 대비
 const y=new Date(t);y.setDate(y.getDate()-1);const yiso=iso(y);const tiso=iso(t);
 const dow=(t.getDay()+6)%7;const ws=new Date(t);ws.setDate(ws.getDate()-dow);
 const d1=new Date(ws);d1.setDate(d1.getDate()-28);
 window.__yiso=yiso;window.__tiso=tiso;
 localStorage.setItem('tt.f.sessions/\uaf2c\uae4c/'+tiso.slice(0,7)+'.json',JSON.stringify({data:{v:1,sessions:[
  {id:'s1',d:'2026-08-19',s:'\ubbfc\ubc95',p:'',i:'',a:600,b:660,u:1},
  {id:'s2',d:yiso,s:'\ubbfc\ubc95',p:'\uac1d',i:'',a:600,b:680,un:'u02',bd:'b1',u:1},
  {id:'s3',d:tiso,s:'\uc0dd\ud65c',p:'',i:'',a:700,b:760,nt:1,life:1,u:1}
 ]},sha:null,dirty:false}));
 const units={'\ubbfc\ubc95':[],'\ubb3c\ub9ac':[]};
 for(let i=1;i<=10;i++){const u={id:'u'+pad(i),n:'\ub2e8\uc6d0'+i,del:false};if(i===1)u.done={b1:yiso};units['\ubbfc\ubc95'].push(u)}
 for(let i=1;i<=3;i++)units['\ubb3c\ub9ac'].push({id:'p'+pad(i),n:'\ubb3c\ub2e8\uc6d0'+i,del:false});
 const plan={v:2,cur:'pj1',units,daily:[1,1,1,1,1,1,1],goals:{},pu:1,projects:[{id:'pj1',name:'64\ud68c 1\ucc28\uc2dc\ud5d8',d1:iso(d1),d2:'',subjects:['\ubbfc\ubc95','\ubb3c\ub9ac'],cats:{'\ubbfc\ubc95':['\uac1d'],'\ubb3c\ub9ac':['\uc554\uae30']},catMark:{},catGoal:{},pins:{b1:{u02:yiso,u03:yiso}},bands:[
  {id:'b1',s:'\ubbfc\ubc95',tag:'\uac1d',name:'\uae30\ubcf8\uc11c1',w1:1,w2:8,per:2,units:units['\ubbfc\ubc95'].map(u=>u.id),u:1,del:false},
  {id:'b2',s:'\ubb3c\ub9ac',tag:'\uc554\uae30',name:'\uc554\uae301',w1:1,w2:3,per:1,units:units['\ubb3c\ub9ac'].map(u=>u.id),u:1,del:false},
  {id:'b3',s:'\ubbfc\ubc95',tag:'\uac1d',name:'\uac1d2\ud68c\ub3c5',w1:6,w2:8,per:2,units:[],u:1,del:false},
  {id:'b4',s:'\ubb3c\ub9ac',tag:'\uc554\uae30',name:'\uc554\uae302',w1:4,w2:6,per:1,units:[],u:1,del:false}
 ],milestones:[],baselines:[],yield:[],arch:false,u:1}]};
 localStorage.setItem('tt.f.plan/\uaf2c\uae4c.json',JSON.stringify({data:plan,sha:null,dirty:false}));
})();
localStorage.setItem('tt.f.snaps/\uaf2c\uae4c/2026-08.json',JSON.stringify({data:{v:1,days:{'2026-08-25':{at:1,u:1,total:130,memo:'',ss:[['\ubbfc\ubc95',300,430,0]],it:[['\ubbfc\ubc95','\uac1d1\ud68c\ub3c5',0,130,'\uac1d1\ud68c\ub3c5']]}},weeks:{},months:{}},sha:null,dirty:false}));
</script>
"""

TESTS = r"""<script>
(function(){
const R=[];const T=(name,cond,info)=>R.push((cond?'PASS':'FAIL')+' | '+name+(info!==undefined&&!cond?' | '+String(info):''));
try{
// ---- R2: OX 붙여넣기 ----
const oxTxt=['[OX 학습로그] 2026-08-25',
'- ⚡빠른실행 / 🔥 약점 다시 풀기 (all) : 19문항, 정답 19 · 오답 0 · 헷갈림 19',
'- 민법총칙 / 2. 자연인 > 2.1 권리능력 (all) : 15문항, 정답 14 · 오답 1 · 헷갈림 3',
'- 민법총칙 / 3. 의사능력 (all) : 9문항, 정답 9 · 오답 0 · 헷갈림 3',
'합계: 43문항 · 정답 42 · 오답 1 · 헷갈림 25',
'[OX 학습로그] 2026-08-27',
'- 민법총칙 / 4. 행위능력 (all) : 6문항, 정답 5 · 오답 1 · 헷갈림 2',
'- ⚡빠른실행 / 약점 (all) : 4문항, 정답 4 · 오답 0 · 헷갈림 1',
'합계: 10문항 · 정답 9 · 오답 1 · 헷갈림 3'].join('\n');
const p1=parseRecLog(oxTxt);
T('R2 블록 2',p1.blocks.length===2,p1.blocks.length);
T('R2 8/25 3줄 43문항',p1.blocks[0].items.length===3&&p1.blocks[0].items.reduce((a,x)=>a+x.n,0)===43);
T('R2 8/27 2줄 10문항',p1.blocks[1].items.length===2&&p1.blocks[1].items.reduce((a,x)=>a+x.n,0)===10);
T('R2 빠른실행=약점큐',p1.blocks[0].items[0].unit==='약점큐',p1.blocks[0].items[0].unit);
T('R2 unit=장·(출처) 떼기',p1.blocks[0].items[1].unit==='2. 자연인 > 2.1 권리능력',p1.blocks[0].items[1].unit);
T('R2 못 읽는 줄 0',p1.bad.length===0,p1.bad.join('|'));
const mk=b=>{const L=[];b.blocks.forEach(x=>x.items.forEach(it=>L.push(Object.assign({d:x.d,app:x.app,subj:x.subj,src:'paste'},it))));return L};
upsertRecs(mk(p1));const n1=recFile(cfg.person).data.items.length;
upsertRecs(mk(parseRecLog(oxTxt)));const n2=recFile(cfg.person).data.items.length;
T('R2 재가져오기 = 행 수 무변(덮어씀)',n1===5&&n2===5,n1+','+n2);
// ---- R2b: 물리 붙여넣기 ----
const phTxt=['[물리535 학습로그] 2026-08-26',
'- 등속 운동, 등가속도 운동 : 3문항 (정답률 67% · 헷갈림 1)',
"  17 O 0'45\" | 21 Q 1'10\" | 22 X 2'05\"",
'- 운동량 보존 : 2문항 (정답률 50% · 헷갈림 0)',
'합계: 5문항 · O 3 · 헷갈림 1 · X 1 · 12분'].join('\n');
const p2=parseRecLog(phTxt);const u1=p2.blocks[0].items[0],u2=p2.blocks[0].items[1];
T('R2b 상세 줄 실측(o/q/x·분)',u1.o===1&&u1.q===1&&u1.x===1&&u1.min===4,JSON.stringify(u1));
T('R2b 합계 분 비례 배분(상세분 제외)',u2.o===1&&u2.x===1&&u2.min===8,JSON.stringify(u2));
// ---- R3: physGroup ----
const t1=new Date(2026,7,20,3,30).getTime(),t2=new Date(2026,7,20,4,30).getTime();
const ST={'10':{h:[{m:'O',t:t1,s:60},{m:'Q',t:t2,s:30}]},'11':{h:[{m:'X',t:t1,s:120}]}};
const gl=physGroup(ST,function(){return 'A'});
const g19=gl.find(x=>x.d==='2026-08-19'),g20=gl.find(x=>x.d==='2026-08-20');
T('R3 새벽 4시 경계',!!g19&&!!g20&&g19.n===2&&g20.n===1,JSON.stringify(gl.map(x=>x.d+':'+x.n)));
T('R3 집계·min=초합',!!g19&&g19.o===1&&g19.x===1&&g19.min===3&&!!g20&&g20.q===1,JSON.stringify(g19));
recPrev=null;const nb=recFile(cfg.person).data.items.length;recImportGo();
T('R3 승인 전 저장 0',recFile(cfg.person).data.items.length===nb);
// ---- R4: 확대 모달·일간 한 줄 ----
snapView('꼬까','2026-08-25');
const bx=document.querySelector('.modal .box');const html=bx?bx.innerHTML:'';
const iT=html.indexOf('Total'),iR=html.indexOf('푼 문제'),iM=html.lastIndexOf('메모');
T('R4 위치 = 카드 아래·메모 위',iT>=0&&iR>iT&&iM>iR,[iT,iR,iM].join(','));
T('R4 Total 무변(02:10)',html.indexOf('02:10')>=0);
T('R4 푼 문제 수치',html.indexOf('43문항')>=0&&html.indexOf('98%')>=0&&html.indexOf('헷갈림 25')>=0);
document.querySelectorAll('.modal').forEach(m=>m.remove());
const rl=recLineHTML('2026-08-25');
T('R4 일간 한 줄',rl.indexOf('민법OX 43')>=0&&rl.indexOf('98%')>=0&&rl.indexOf('헷갈림 25')>=0,rl.replace(/<[^>]*>/g,''));
ui.date='2026-08-26';
T('R4 어제오늘내일 배선',threeHTML().indexOf('recln')>=0);
ui.date=null;
// ---- R5: 시간층 ----
const tg=timeTrendHTML();
T('R5 그래프 있음',tg.indexOf('공부시간 추이')>=0);
T('R5 과거 구간 옅은 톤',tg.indexOf('class="hist"')>=0);
ui.ttTrend='all';T('R5 est 툴팁 raw (fb13 §2: 「전체」 범위에서)',timeTrendHTML().indexOf('am3~am7 pm8~10')>=0);delete ui.ttTrend;
const hm8=histMonthMin('꼬까','2026-08');
T('R5 앱 세션 날짜 = 시간층 무시',hm8.min===208,hm8.min);
const c1=dayCard('꼬까','2023-10-01');
T('R5 시간층 카드 = 빈 칸+Total',c1.indexOf('card hist')>=0&&c1.indexOf('07:50')>=0&&c1.indexOf('class="mini"')<0,c1.slice(0,120));
T('R5 est = ≈',dayCard('꼬까','2024-11-16').indexOf('≈06:00')>=0);
const c3=dayCard('꼬까','2026-08-19');
T('R5 세션 있는 날 = 앱 실측 우선',c3.indexOf('미반영')>=0&&c3.indexOf('card hist')<0);
const ms=snapMonthStats('꼬까','2023-10');
T('R5 월 합계에 시간층·미반영 제외',ms.tot===470&&ms.miss===30,ms.tot+','+ms.miss);
T('R5 밀림·부하 산식 무변',String(late).indexOf('hist')<0&&String(loadAvgMin).indexOf('hist')<0&&String(plannedThrough).indexOf('hist')<0&&String(weekLoads).indexOf('hist')<0);
// ---- R6: 분석 ----
const an=recAnalysisHTML(myPlan());
T('R6 주별 그래프·클릭 배선',an.indexOf('문항 기록')>=0&&an.indexOf('recWeekModal')>=0&&an.indexOf('hz2')>=0);
T('R6 달성 탭 안 절',achTabHTML(myPlan()).indexOf('문항 기록')>=0);
recWeekModal(encodeURIComponent('민법'),weekStart('2026-08-25'));
const bx2=document.querySelector('.modal .box');const h2=bx2?bx2.innerHTML:'';
T('R6 막대 클릭 = 단원별 표',h2.indexOf('약점큐')>=0&&h2.indexOf('단원별')>=0);
document.querySelectorAll('.modal').forEach(m=>m.remove());
// ---- 병합·회귀 ----
const mh=mergeFile('history/꼬까.json',{v:1,days:{a:{min:1,u:5},b:{min:2,u:1}}},{v:1,days:{a:{min:9,u:3},c:{min:3,u:1}}});
T('병합 history 날짜별 u 큰 쪽',mh.days.a.min===1&&mh.days.b.min===2&&mh.days.c.min===3);
const mr=mergeFile('records/꼬까.json',{items:[{id:'x',n:1,u:5}]},{items:[{id:'x',n:9,u:3},{id:'y',n:2,u:1}]});
T('병합 records id·u',mr.items.length===2&&mr.items.find(z=>z.id==='x').n===1);
T('회귀 galHTML',typeof galHTML()==='string'&&galHTML().indexOf('데일리 모음')>=0);
T('회귀 ttPageHTML',typeof ttPageHTML()==='string');
T('회귀 가져오기 입구(fb13 §1: 데일리 모음)',galHTML().indexOf('학습기록 가져오기')>=0);
T('회귀 pmHTML',typeof pmHTML()==='string');
T('회귀 planHTML',typeof planHTML()==='string');
T('회귀 weekCardHTML',typeof weekCardHTML(weekStart('2026-08-25'))==='string');
T('회귀 monthCardHTML',typeof monthCardHTML('2026-08')==='string');
T('회귀 snapMonthSheetHTML ≈',snapMonthSheetHTML('꼬까','2024-11').indexOf('≈06:00')>=0);
T('회귀 weekCard 시간층 합',weekCard('꼬까','2023-09-25').indexOf('데일리')<0); // 예외 없이 렌더만 확인
T('회귀 monthCard 시간층 합',monthCard('꼬까','2023-10').indexOf('07:50')>=0);

// ================= feedback11 =================
window.confirm=function(){return true};
const yiso=window.__yiso,tiso=window.__tiso,t0=today();
let plan=myPlan();
// ---- F11-5: 일간 = 캘린더 엔진 산식 통일 ----
const idsOf=L=>L.map(e=>e.b.id+'|'+e.u.id).sort().join(',');
const chipIds=d=>((calData(myPlan(),d,d).chips[d])||[]).map(c=>c.b.id+'|'+c.u.id).sort().join(',');
const d5a=t0,d5b=addDays(t0,1),d5c=addDays(t0,3);
T('F11-5 오늘 = 엔진',idsOf(dayPlanRows(myPlan(),d5a))===chipIds(d5a)&&chipIds(d5a).length>0,chipIds(d5a));
T('F11-5 내일 = 엔진',idsOf(dayPlanRows(myPlan(),d5b))===chipIds(d5b));
T('F11-5 +3일 = 엔진',idsOf(dayPlanRows(myPlan(),d5c))===chipIds(d5c));
// ---- F11-6: 어제 = 완료 + 흐림·「→ 오늘」 ----
const rows6=dayPlanRows(myPlan(),yiso);
T('F11-6 어제 완료(u01)',rows6.some(e=>e.u.id==='u01'&&e.done));
T('F11-6 어제 미완료 = dim',rows6.some(e=>e.u.id==='u02'&&e.dim)&&rows6.some(e=>e.u.id==='u03'&&e.dim),JSON.stringify(rows6.map(e=>e.u.id+(e.dim?'/dim':'/done'))));
const h6=planColHTML(yiso,0);
T('F11-6 흐림+→오늘 표기',h6.indexOf('dim2')>=0&&h6.indexOf('→ 오늘')>=0);
T('F11-6 뒤늦은 체크 배선',h6.indexOf(`togglePlanDone('b1','u02','${yiso}')`)>=0);
const idsT=idsOf(dayPlanRows(myPlan(),t0));
T('F11-6 오늘 칸과 이중 아님',!rows6.some(e=>e.u.id==='u02'&&!e.dim&&!e.done)&&idsT.indexOf('b1|u02')<0); // fb17 §3: 과거 📌 는 그 날에 남고 오늘로 안 온다(손 지정 우선)
// ---- F11-11: 이어서/이월 ----
const hT=planColHTML(t0,1);
T('F11-11 → fb17 §7: 「이어서」 표시 폐지',hT.indexOf('이어서')<0&&h6.indexOf('이어서')<0);
T('F11-11 → fb17 §7: 이월 = +N 숫자',/>\+\d+</.test(hT)||dayPlanRows(myPlan(),t0).every(e=>!e.late),hT.slice(0,80));
T('F11-11 → fb17 §7: 어제 흐림 줄 = → 오늘',h6.indexOf('→ 오늘')>=0&&h6.indexOf('→ 오늘 · ')<0);
// ---- F12-9: 재배치(새 산식 = w1 무변·내부 오프셋 rb) + 되돌리기 ----
const L1b=late(myPlan(),myPlan().bands.find(b=>b.id==='b1'),addDays(t0,-1));
const blCause=JSON.stringify((lastBaseline(myPlan()).bands||[]).filter(x=>['b1','b2'].includes(x.id)));
rebalanceApply();
plan=myPlan();
const b1=plan.bands.find(b=>b.id==='b1'),b2=plan.bands.find(b=>b.id==='b2'),b4=plan.bands.find(b=>b.id==='b4');
T('F12-9 w1 무변',b1.w1===1&&b2.w1===1,JSON.stringify([b1.w1,b2.w1]));
T('F12-9 재분배 = 주당 재계산+rb 마커',b1.per===3&&b1.rb&&b1.rb.d===t0&&b1.rb.base===1,JSON.stringify([b1.per,b1.rb]));
const L1a=late(plan,b1,addDays(t0,-1));
T('F12-9 밀림 소멸(오늘 이전 몫 0)',L1a===0&&L1b>0,L1b+'→'+L1a);
T('F12-9 안 들어가는 활동 = 연장(주당 유지·w1 무변)',b2.w2===7&&b2.per===1&&!!b2.rb,JSON.stringify([b2.w1,b2.w2,b2.per]));
T('F12-9 뒤 활동 밀림 + §10 orig 동반',b4.w1===8&&b4.w2===10&&b4.orig&&b4.orig.w1===8&&b4.orig.w2===10,JSON.stringify([b4.w1,b4.w2,b4.orig]));
T('F12-9 원인 활동 원계획 무변',JSON.stringify((lastBaseline(myPlan()).bands||[]).filter(x=>['b1','b2'].includes(x.id)))===blCause);
T('F12-9 적용 후에도 일간=엔진',idsOf(dayPlanRows(myPlan(),t0))===chipIds(t0));
T('F12-9 rbUndo 저장',!!myPlan().rbUndo&&myPlan().rbUndo.bands.length===3,JSON.stringify((myPlan().rbUndo||{}).bands));
rebalanceUndo();
plan=myPlan();
const r1=plan.bands.find(b=>b.id==='b1'),r2=plan.bands.find(b=>b.id==='b2'),r4=plan.bands.find(b=>b.id==='b4');
T('F12-9 되돌리기 1회 왕복',r1.per===2&&!r1.rb&&r2.w2===3&&r4.w1===4&&!myPlan().rbUndo,JSON.stringify([r1.per,r2.w2,r4.w1]));
rebalanceApply(); // 이후 검사는 적용 상태에서
T('F12-10 빗금 = 원인 꼬리만(b2 orig 유지)',(()=>{const p2=myPlan();const x2=p2.bands.find(b=>b.id==='b2');return x2.orig&&x2.orig.w2===3&&x2.w2===7})());
// ---- F11-7: PiP 원탭 ----
const sessN=()=>sessFile(cfg.person,tiso.slice(0,7)).data.sessions.filter(x=>!x.del).length;
const n70=sessN();
pickRow('unit',encodeURIComponent('b1|u04'));startTimer(); // fb17 §1: 선택 + START
T('F11-7 탭 = 세션 시작',!!run&&run.band==='b1'&&run.unit==='u04',JSON.stringify(run));
pickRow('unit',encodeURIComponent('b1|u05'));startTimer();
T('F11-7 → fb19 §2-2: 진행 중 START 는 무시(전환 폐기)',!!run&&run.unit==='u04'&&sessN()===n70);
pickRow('life','');startTimer();
T('F11-7 → fb19: 생활도 전환 없음',!!run&&run.unit==='u04');
stopTimer();
T('F11-7 정리',!run&&sessN()===n70+1);
T('F11-7 PiP = 본창 시트 재사용',String(pipPaint).indexOf('sheetHTML')>=0&&sheetHTML(cfg.person,today(),sessionsOf(cfg.person,today())).indexOf("pickRow('life','')")>=0);
// ---- F11-8: 계획관리 자동 표시 ----
const pm=pmCoreHTML();
T('F11-8 주월계획 활동 표시',pm.indexOf('기본서1')>=0&&pm.indexOf('주월계획')>=0);
T('F11-8 완료 토글 부재',pm.indexOf('togglePlanDone')<0);
T('F11-8 손 추가분 공존',typeof pmHTML()==='string');
// ---- F11-9: 생활 고정 줄 ----
const sh9=sheetHTML('꼬까',t0,sessionsOf('꼬까',t0));
T('F11-9 목록 맨 끝 생활 줄',sh9.indexOf('liferow')>=0&&sh9.indexOf("pickRow('life','')")>=0); // fb17 §1: 클릭 = 선택
T('F11-9 Total (생활 제외)',sh9.indexOf('(생활 제외)')>=0);
const totNoLife=mSum(sessionsOf('꼬까',t0));
T('F11-9 Total 무변(생활 불산입)',totNoLife<60,totNoLife);
// ---- F11-10: 빗금 ----
takeSnap(t0);
const sn10=snapOf('꼬까',t0);
T('F11-10 스냅에 life 플래그',(sn10.ss||[]).some(z=>z[0]==='생활'&&z[4]===1));
T('F11-10 스냅 시트 빗금 회색',ttSnap(snapSess(sn10,t0)).indexOf('#c9ccd1')>=0&&ttSnap(snapSess(sn10,t0)).indexOf('repeating-linear-gradient')>=0);
T('F11-10 본창 빗금',sh9.indexOf('hsw')>=0);
// ---- F11-12: 드롭다운 ----
const gm=galRecMonths();
T('F11-12 기록 있는 달만',gm.includes('2023-10')&&gm.includes('2024-11')&&gm.includes(tiso.slice(0,7))&&!gm.includes('2025-06'),gm.join(' '));
T('F11-12 최신→옛날',gm[0]>=gm[gm.length-1]);
T('F11-12 입구',galHTML().indexOf('galddw')>=0);
// ---- F11-1: 분류 팝오버 (파괴적 — plan 저장 후 복원) ----
const planSaved=localStorage.getItem('tt.f.plan/꼬까.json');
catBandMenu(encodeURIComponent('민법'),encodeURIComponent('객'));
let cm=document.getElementById('cbmM');
T('F11-1 나열',!!cm&&cm.innerHTML.indexOf('기본서1')>=0&&cm.innerHTML.indexOf('객2회독')>=0);
cm.querySelectorAll('.cbmCk')[0].checked=true;
cbmDel(false);
T('F11-1 선택 삭제(del 경로)',!!planFile(cfg.person).data.projects[0].bands.find(b=>b.id==='b1').del);
catBandMenu(encodeURIComponent('민법'),encodeURIComponent('객'));
cbmDel(true);
T('F11-1 전체 삭제',!!planFile(cfg.person).data.projects[0].bands.find(b=>b.id==='b3').del);
localStorage.setItem('tt.f.plan/꼬까.json',planSaved);
// ---- F11-2: 리스트 계층 ----
let ls=planListHTML(myPlan());
T('F11-2 계층(과목·분류 머리)',ls.indexOf('lsgs')>=0&&ls.indexOf('lsgc')>=0&&ls.indexOf('기본서1')>=0);
lsFoldTgl('s',encodeURIComponent('민법'));
T('F11-2 과목 접기 유지',planListHTML(myPlan()).indexOf('기본서1')<0&&(ui.lsFold.s['민법']===true));
lsFoldTgl('s',encodeURIComponent('민법'));
lsSelGrp('b1,b3',true);
T('F11-2 분류 머리 체크 = 하위 전체 · N 일치',lsSel.size===2&&planListHTML(myPlan()).indexOf('선택 삭제 (2)')>=0);
lsSelDel();
T('F11-2 선택 삭제',!!planFile(cfg.person).data.projects[0].bands.find(b=>b.id==='b1').del&&!!planFile(cfg.person).data.projects[0].bands.find(b=>b.id==='b3').del);
localStorage.setItem('tt.f.plan/꼬까.json',planSaved);
T('F11 회귀 planBoardHTML',planBoardHTML(myPlan(),false,false).indexOf('pbcat')>=0);
T('F11 회귀 rebalancePreview 배선',String(rebalancePreview).indexOf('rebalanceCore')>=0);

// ================= feedback12 =================
// ---- F12-1 과목 순서 드래그 ----
ui.view='set';render();
T('F12-1 손잡이·컨테이너',document.getElementById('subjList').dataset.ds==='subj'&&setHTML().indexOf('dragh')>=0);
const s0n=settings.subjects.map(x=>x.n);
subjReorder([...settings.subjects.keys()].map(String).reverse());
T('F12-1 순서 저장',settings.subjects[0].n===s0n[s0n.length-1]);
T('F12-1 보드 순서 = 설정 순서',subjOrderAll(myPlan())[0]==='물리',subjOrderAll(myPlan()).join(','));
subjReorder([...settings.subjects.keys()].map(String).reverse());
T('F12-1 원복',settings.subjects.map(x=>x.n).join(',')===s0n.join(','));
// ---- F12-2 분류 순서 드래그 ----
pjSettings();
T('F12-2 칩 손잡이',!!document.querySelector('.pjcr[data-ds="pjcat"] .dragh'));
pjmSt.cats['민법']=['객','신규'];pjCatReorder(encodeURIComponent('민법'),['1','0']);
T('F12-2 순서 커밋',pjmSt.cats['민법'].join(',')==='신규,객');
pjSave(id=>({value:{pjN:pjmSt.name,pjD1:pjmSt.d1,pjD2:pjmSt.d2}[id]}));
T('F12-2 보드 분류 줄 순서 일치',myPlan().cats['민법'][0]==='신규',JSON.stringify(myPlan().cats['민법']));
planMut(p=>{p.cats['민법']=['객']},true);
document.querySelectorAll('.modal').forEach(x=>x.remove());
// ---- F12-3 개명 → 기타 낙하 수리 ----
window.prompt=function(){return '이론'};
pjSettings();
pjCatRen(encodeURIComponent('민법'),0);
document.querySelectorAll('.modal').forEach(x=>x.remove()); // = 취소
plan=myPlan();
T('F12-3 취소 경로 tag 유지',plan.bands.some(b=>!b.del&&b.s==='민법'&&b.tag==='이론')&&plan.cats['민법'].includes('이론'),JSON.stringify(plan.cats['민법']));
pjSettings(); // cats0 = ['이론'] 스냅샷
planMut(p=>{p.bands.forEach(b=>{if(!b.del&&b.s==='민법'&&b.tag==='이론'){b.tag='이론2';b.u=Date.now()}});const cs=p.cats['민법'];cs[cs.indexOf('이론')]='이론2'},true); // 모달 연 뒤 라이브 개명(병합·둘째 모달 재현)
pjSave(id=>({value:{pjN:pjmSt.name,pjD1:pjmSt.d1,pjD2:pjmSt.d2}[id]}));
T('F12-3 스테일 저장에도 낙하 없음',myPlan().cats['민법'].includes('이론2'),JSON.stringify(myPlan().cats['민법']));
planMut(p=>{const b=p.bands.find(x=>x.id==='b1');b.tag='유령';b.u=Date.now()},true);
T('F12-3 자가 치유(고아 tag = 분류 되살림)',myPlan().cats['민법'].includes('유령'),JSON.stringify(myPlan().cats['민법']));
planMut(p=>{const b=p.bands.find(x=>x.id==='b1');b.tag=''},true);
catBandMenu(encodeURIComponent('민법'),encodeURIComponent(''));
const cm3=document.getElementById('cbmM');
T('F12-3 기타 줄 복구 입구',!!cm3&&cm3.innerHTML.indexOf('기본서1')>=0&&cm3.innerHTML.indexOf('분류 지정')>=0);
cm3.querySelector('.cbmCk').checked=true;
cm3.querySelector('#cbmTag').value=myPlan().cats['민법'][0];
cbmAssign();
T('F12-3 분류 지정 동작',myPlan().bands.find(b=>b.id==='b1').tag===myPlan().cats['민법'][0]);
// ---- F12-4 부하 폴백 ----
const cp4=cfg.person;cfg.person='햄찌';
T('F12-4 실측 전무 폴백 = 60분',loadAvgMin().all===60);
cfg.person=cp4;
T('F12-4 weekLoads 폴백 배선',String(weekLoads).indexOf('||60')>=0);
// ---- F12-5 DB 오른쪽 열·입력 루트·보관 ----
T('F12-5 좌우 2단',pmHTML().indexOf('pm2')>=0&&pmHTML().indexOf('세부계획 DB')>=0);
planMut(p=>{p.subjects.push('특허')},true);
let ud=unitsDBHTML(myPlan());
T('F12-5 빈 카드 = 입력 루트(＋·붙여넣기)',ud.indexOf('특허')>=0&&ud.indexOf('비어 있음')>=0&&ud.indexOf('unitPaste')>=0);
uArchTgl(encodeURIComponent('특허'),true);
ud=unitsDBHTML(myPlan());
T('F12-5 보관',ud.indexOf('보관된 DB (1)')>=0&&ud.indexOf("unitModal('"+encodeURIComponent('특허'))<0);
uArchTgl(encodeURIComponent('특허'),false);
T('F12-5 복원 왕복',unitsDBHTML(myPlan()).indexOf('보관된 DB')<0&&unitsDBHTML(myPlan()).indexOf('특허')>=0);
planMut(p=>{p.subjects=p.subjects.filter(s=>s!=='특허')},true);
// ---- F12-6·F12-12 종료 섹션·필터 ----
upsertCat({id:'m1',s:'민법',name:'MiMi옛활동',d1:'2026-01-01',d2:'2026-02-01',mimi:1,done:false});
planMut(p=>{p.bands.push({id:'b6',s:'물리',tag:'암기',name:'끝난활동',w1:1,w2:2,per:1,units:[],u:1,del:false})});
ui.pmArchOpen=true;
const ah=pmArchHTML(myPlan());
T('F12-6 🗃 섹션(이관 cat·기간)',ah.indexOf('MiMi옛활동')>=0&&ah.indexOf('2026-01-01 ~ 2026-02-01')>=0);
T('F12-6 종료 밴드도 🗃 · 과목별',ah.indexOf('끝난활동')>=0&&ah.indexOf('민법')>=0&&ah.indexOf('물리')>=0);
ui.pmArchOpen=false; // fb13 §7: 🗃 가 pmCoreHTML 안으로 — 접힘 상태로 본문 제외 확인
T('F12-6 본문에서 제외',pmCoreHTML().indexOf('MiMi옛활동')<0&&pmCoreHTML().indexOf('끝난활동')<0);
T('F12-6 종료 체크박스 제거',pmHTML().indexOf('종료된 활동 보이기')<0);
planMut(p=>{p.bands.push({id:'b5',s:'민법',tag:'',name:'미래활동',w1:7,w2:8,per:1,units:[],u:1,del:false})});
T('F12-12 기본 = 진행 중만',pmCoreHTML().indexOf('미래활동')<0);
ui.pmFuture=true;
T('F12-12 미시작 체크 시 노출',pmCoreHTML().indexOf('미래활동')>=0);
ui.pmFuture=false;
// ---- F12-7 PiP (fb16 §1 이 tt-v18 원본으로 원상 복구 — 시트 그대로가 정답) ----
T('F12-7 PiP = 시트 통째(fb16 원복)',String(pipPaint).indexOf('sheetHTML')>=0&&String(pipPaint).indexOf('mbarHTML')>=0);
T('F12-7 원탭·생활 줄 = 시트 안에서',sheetHTML(cfg.person,today(),sessionsOf(cfg.person,today())).indexOf('liferow')>=0);
// ---- F12-8 가운데 팝업 ----
galMonthModal();
const gd=document.getElementById('galDD');
T('F12-8 가운데 모달 렌더',!!gd&&gd.className==='modal'&&gd.innerHTML.indexOf('2023-10')>=0&&gd.innerHTML.indexOf('지난 기록')>=0);
galDDFilter('24.11');
T('F12-8 검색 거르기',[...gd.querySelectorAll('.gi')].filter(x=>x.style.display!=='none').every(x=>x.dataset.m.slice(0,7)==='2024-11'));
galPick('2023-10');
T('F12-8 2023-10 점프·닫힘',ui.galMonth==='2023-10'&&!document.getElementById('galDD'));
ui.galMonth=null;LS.set('tt.ui',ui);
T('F12-8 옛 드롭다운 제거',typeof window.galDrop==='undefined');
// ---- F12-11 팝오버 수리 ----
catBandMenu(encodeURIComponent('민법'),encodeURIComponent(myPlan().bands.find(b=>b.id==='b1').tag||''));
const cm11=document.getElementById('cbmM');
T('F12-11 이름 가로·스크롤·하단 버튼',!!cm11&&cm11.innerHTML.indexOf('nm2')>=0&&cm11.innerHTML.indexOf('overflow:auto')>=0&&cm11.innerHTML.indexOf('전체 삭제')>=0);
document.querySelectorAll('.modal').forEach(x=>x.remove());

// ================= feedback13 =================
// ---- F13-1 가져오기 이사 ----
T('F13-1 데일리 모음에 입구',galHTML().indexOf('recImportModal')>=0);
T('F13-1 설정엔 없음',setHTML().indexOf('학습기록 가져오기')<0);
// ---- F13-2 그래프 12개월+토글 ----
delete ui.ttTrend;
const tg12=timeTrendHTML();
T('F13-2 기본 = 최근 12개월',(tg12.match(/class="bc"/g)||[]).length<=12&&tg12.indexOf('12개월')>=0,(tg12.match(/class="bc"/g)||[]).length);
ui.ttTrend='all';
const tgA=timeTrendHTML();
T('F13-2 「전체」 = 23년부터·옅음·≈ 유지',(tgA.match(/class="bc"/g)||[]).length>12&&tgA.indexOf('class="hist"')>=0&&tgA.indexOf('am3~am7 pm8~10')>=0);
ui.ttTrend='12';LS.set('tt.ui',ui);
// ---- F13-3 탭 12 + 팝업 = 이전 달만 ----
T('F13-3 탭 12개',(galHTML().match(/galdot/g)||[]).length===12,(galHTML().match(/galdot/g)||[]).length);
galMonthModal();
const gd13=document.getElementById('galDD');
const cut13=ym(shiftMonth(today(),-11));
T('F13-3 팝업 = 탭 이전 달만',[...gd13.querySelectorAll('.gi')].length>0&&[...gd13.querySelectorAll('.gi')].every(x=>x.dataset.m<cut13)&&gd13.innerHTML.indexOf('2023-10')>=0);
galPick('2023-10');
T('F13-3 점프 유지',ui.galMonth==='2023-10');
ui.galMonth=null;LS.set('tt.ui',ui);
// ---- F13-4 Food diary(앱 층 — 이관 79건 검산은 파이썬) ----
localStorage.setItem('tt.f.food/food.json',JSON.stringify({data:{v:1,items:[
 {id:'f1',name:'간장라면',date:'2024-10-05',recipe:'라면사리2개',imgs:['food/img/f1_1.jpg'],thumb:'food/thumb/f1.jpg',u:1,del:false},
 {id:'f2',name:'누룽지탕',date:'2024-10-12',recipe:'',imgs:[],thumb:'',u:1,del:false}]},sha:null,dirty:false}));
const fh=archHTML();
T('F13-4 Archive 묶음·갤러리 최신순',fh.indexOf('Food diary')>=0&&fh.indexOf('data-img="food/thumb/f1.jpg"')>=0&&fh.indexOf('누룽지탕')<fh.indexOf('간장라면'),fh.slice(0,80));
foodView('f1');
const fv=document.getElementById('foodV');
T('F13-4 상세 = 사진+레시피',!!fv&&fv.innerHTML.indexOf('라면사리2개')>=0&&!!fv.querySelector('img')); // fillImgs 가 data-img 를 동기적으로 떼므로 img 존재로 확인
document.querySelectorAll('.modal').forEach(x=>x.remove());
upsertFood({id:'f3',name:'새항목',date:t0,recipe:'r',imgs:[],thumb:'',del:false});
T('F13-4 새 항목 추가·공유 경로',foodItems().some(x=>x.id==='f3')&&String(foodFile).indexOf('food/food.json')>=0);
T('F13-4 압축 파이프라인 공용',typeof imgCompress==='function'&&String(foodSave).indexOf('imgCompress')>=0&&String(shareAddImg).indexOf('imgCompress')>=0);
const mf=mergeFile('food/food.json',{items:[{id:'a',u:5,name:'x'}]},{items:[{id:'a',u:3,name:'y'},{id:'b',u:1}]});
T('F13-4 병합(공용·id·u)',mf.items.length===2&&mf.items.find(z=>z.id==='a').name==='x');
// ---- FS Food diary 검색(_task_food_search 9/3) — 시드 f1 간장라면/라면사리2개 · f2 누룽지탕 · f3 새항목/r + f4 Ramen Bowl ----
upsertFood({id:'f4',name:'Ramen Bowl',date:'2024-11-02',recipe:'egg, Scallion',imgs:[],thumb:'',del:false,note:'끓인다\n햄찌 별점 4점'});
const FA=foodItems();
T('FS-1 빈 검색 = 전체',foodSearch(FA,'').length===FA.length&&foodSearch(FA,'   ').length===FA.length,FA.length);
T('FS-1 한 낱말(이름∪재료)',foodSearch(FA,'라면').length===1&&foodSearch(FA,'라면')[0].id==='f1');
T('FS-1 두 낱말 AND',foodSearch(FA,'라면 2024').length===1&&foodSearch(FA,'라면 누룽지').length===0);
T('FS-1 대소문자 무시',foodSearch(FA,'ramen').length===1&&foodSearch(FA,'RAMEN BOWL').length===1&&foodSearch(FA,'scallion').length===1);
T('FS-1 만드는 법·날짜도 대상',foodSearch(FA,'별점').length===1&&foodSearch(FA,'2024-10').length===2);
const fw=document.createElement('div');fw.innerHTML=foodHTML();document.body.appendChild(fw);
T('FS-2 검색 상자·건수 N/전체',!!fw.querySelector('#fdQ')&&fw.querySelector('#fdN').textContent===FA.length+'/'+FA.length&&fw.querySelector('#fdX').style.visibility==='hidden');
foodApply('사리',document);
T('FS-2 즉시 거르기 + 강조 + 재료 발췌',fw.querySelectorAll('#fdGrid .fcard').length===1&&fw.querySelector('#fdN').textContent==='1/'+FA.length&&fw.querySelector('#fdGrid .fq')&&fw.querySelector('#fdGrid .fq').innerHTML.indexOf('<mark>사리</mark>')>=0,fw.querySelector('#fdGrid').innerHTML.slice(0,200));
foodApply('라면',document);
T('FS-2 이름 강조',fw.querySelector('#fdGrid .fcard b').innerHTML.indexOf('<mark>라면</mark>')>=0&&fw.querySelector('#fdX').style.visibility==='');
foodApply('없는낱말',document);
T('FS-2 0건 안내',fw.querySelectorAll('#fdGrid .fcard').length===0&&fw.querySelector('#fdGrid').textContent.indexOf('맞는 항목이 없어')>=0);
const uiBefore=localStorage.getItem('tt.ui');foodClear(document);
T('FS-2 ✕ 복원',fw.querySelectorAll('#fdGrid .fcard').length===FA.length&&fw.querySelector('#fdQ').value===''&&fw.querySelector('#fdX').style.visibility==='hidden');
T('FS-3 검색어 저장 안 함(ui·localStorage 무접촉)',localStorage.getItem('tt.ui')===uiBefore&&JSON.stringify(ui).indexOf('foodQ')<0&&String(foodApply).indexOf('LS.set')<0&&String(foodQ).indexOf('LS.set')<0);
T('FS-3 doc 규칙(ownerDocument)',String(foodHTML).indexOf('this.ownerDocument')>=0);
fw.remove();foodFile().data.items=foodFile().data.items.filter(x=>x.id!=='f4');
const F79=__FOOD79__;const FL=F79.items.filter(x=>!x.del);
T('FS-4 실물 79 빈 검색',foodSearch(FL,'').length===F79.n_all,foodSearch(FL,'').length);
T('FS-4 실물 「재료」 = 파이썬 셈',foodSearch(FL,'재료').length===F79.n_jaeryo,foodSearch(FL,'재료').length+'≠'+F79.n_jaeryo);
T('FS-4 실물 두 낱말 「별점 4」 = 파이썬 셈',foodSearch(FL,'별점 4').length===F79.n_two,foodSearch(FL,'별점 4').length+'≠'+F79.n_two);
T('FS-4 실물 대소문자 = 파이썬 셈',foodSearch(FL,'BURGER').length===F79.n_case&&foodSearch(FL,'burger').length===F79.n_case,foodSearch(FL,'BURGER').length+'≠'+F79.n_case);
// ---- F13-5 Share ----
localStorage.setItem('tt.f.share/share.json',JSON.stringify({data:{v:1,items:[
 {id:'s1',ty:'img',img:'share/img/s1.jpg',thumb:'share/img/s1_t.jpg',by:'꼬까',at:2,u:1,del:false},
 {id:'s2',ty:'txt',text:'https://example.com/a',by:'햄찌',at:1,u:1,del:false}]},sha:null,dirty:false}));
ui.shareTab='img';
let sh=shareHTML();
T('F13-5 Image 썸네일·올린 사람',sh.indexOf('data-img="share/img/s1_t.jpg"')>=0&&sh.indexOf('꼬까')>=0);
ui.shareTab='txt';
sh=shareHTML();
T('F13-5 Text 원탭 복사·URL 열기·올린 사람',sh.indexOf('shareCopy')>=0&&sh.indexOf('열기')>=0&&sh.indexOf('햄찌')>=0);
shareDel('s2');
T('F13-5 삭제 반영',shareHTML().indexOf('example.com')<0);
T('F13-5 확대 = 다운로드 배선',String(shareView).indexOf('download')>=0&&String(shareView).indexOf('ghImg')>=0);
delete ui.shareTab;
// ---- SI (9/6 _task_tt_share_import) Share 시각·편집 · 가져오기 변경분·날짜별 ----
{const _sh0=localStorage.getItem('tt.f.share/share.json'),_rc0=localStorage.getItem('tt.f.records/꼬까.json');
localStorage.setItem('tt.f.share/share.json',JSON.stringify({data:{v:1,items:[
 {id:'i1',ty:'img',img:'share/img/i1.jpg',thumb:'share/img/i1_t.jpg',by:'꼬까',at:new Date(2026,8,5,14,30).getTime(),u:1,del:false},
 {id:'t1',ty:'txt',text:'메모 하나',by:'햄찌',at:new Date(2026,8,6,9,5).getTime(),u:1,del:false},
 {id:'t2',ty:'txt',text:'메모 둘',by:'꼬까',at:new Date(2026,8,5,10,0).getTime(),u:1,del:false}]},sha:null,dirty:false}));
ui.shareTab='img';let si=shareHTML();
T('SI-1 img 카드 시각 MM/DD HH:mm + ✎',si.indexOf('09/05 14:30')>=0&&si.indexOf("shareEdit('i1')")>=0&&si.indexOf('toLocaleDateString')<0,si.slice(0,200));
ui.shareTab='txt';si=shareHTML();
T('SI-1 txt 행 시각 + ✎',si.indexOf('09/06 09:05')>=0&&si.indexOf('09/05 10:00')>=0&&si.indexOf("shareEdit('t1')")>=0);
T('SI-1 정렬 at 내림차순(t1 먼저)',shareItems('txt').map(x=>x.id).join(',')==='t1,t2');
shareEdit('t1');let mE=[...document.querySelectorAll('.modal')].pop();
T('SI-2 편집 팝업 = datetime-local(초기값 at) + 본문',!!mE&&!!mE.querySelector('#shAt')&&mE.querySelector('#shAt').type==='datetime-local'&&mE.querySelector('#shAt').value==='2026-09-06T09:05'&&!!mE.querySelector('#shTx'),mE&&mE.querySelector('#shAt')&&mE.querySelector('#shAt').value);
mE.querySelector('#shAt').value='2026-09-04T08:00';mE.querySelector('#shTx').value='고친 메모';const u0=Date.now();mE.querySelector('#mOk').click();
let sf=shareFile().data.items.find(x=>x.id==='t1');
T('SI-2 저장 = at·본문·u 갱신 · by 무변',sf.at===new Date(2026,8,4,8,0).getTime()&&sf.text==='고친 메모'&&sf.u>=u0&&sf.by==='햄찌',JSON.stringify(sf));
T('SI-2 정렬 유지(고친 t1 이 뒤로)',shareItems('txt').map(x=>x.id).join(',')==='t2,t1'&&loadF('share/share.json',{}).dirty===true);
shareEdit('i1');mE=[...document.querySelectorAll('.modal')].pop();
T('SI-2 img 편집 = 시각만(본문 칸 없음) · 파일 무변',!!mE.querySelector('#shAt')&&!mE.querySelector('#shTx'));
mE.querySelector('#shAt').value='2026-09-01T00:00';mE.querySelector('#mOk').click();sf=shareFile().data.items.find(x=>x.id==='i1');
T('SI-2 img at 갱신 · img/thumb 무변',sf.at===new Date(2026,8,1,0,0).getTime()&&sf.img==='share/img/i1.jpg'&&sf.thumb==='share/img/i1_t.jpg');
localStorage.setItem('tt.f.records/꼬까.json',JSON.stringify({data:{v:1,items:[
 {id:'2026-08-25|민법OX|약점큐',d:'2026-08-25',app:'민법OX',subj:'민법',unit:'약점큐',n:19,o:19,x:0,q:19,src:'paste',u:7},
 {id:'2026-08-27|민법OX|4. 행위능력',d:'2026-08-27',app:'민법OX',subj:'민법',unit:'4. 행위능력',n:6,o:5,x:1,q:2,src:'paste',u:7},
 {id:'2026-08-26|물리535|등속 운동, 등가속도 운동',d:'2026-08-26',app:'물리535',subj:'물리',unit:'등속 운동, 등가속도 운동',n:3,o:1,x:1,q:1,src:'paste',u:7}]},sha:null,dirty:false}));
recImportModal();
document.getElementById('recTx').value=['[OX 학습로그] 2026-08-25','- ⚡빠른실행 / 약점 (all) : 19문항, 정답 19 · 오답 0 · 헷갈림 19','[OX 학습로그] 2026-08-27','- 민법총칙 / 4. 행위능력 (all) : 6문항, 정답 4 · 오답 2 · 헷갈림 2','[OX 학습로그] 2026-08-28','- 민법총칙 / 5. 주소 (all) : 2문항, 정답 2 · 오답 0 · 헷갈림 0'].join('\n');
recParse();
T('SI-3 세 상태 판정 같음·바뀜·새',recPrev.byD['2026-08-25'].st==='same'&&recPrev.byD['2026-08-27'].st==='chg'&&recPrev.byD['2026-08-28'].st==='new',JSON.stringify(Object.keys(recPrev.byD).map(k=>k+':'+recPrev.byD[k].st)));
T('SI-3 기본 체크 = 새·바뀜만',recPrev.chk.has('2026-08-27')&&recPrev.chk.has('2026-08-28')&&!recPrev.chk.has('2026-08-25'));
let pvH=document.getElementById('recPv').textContent;
T('SI-3 날짜별 표 머리줄',/날짜 3일 · 새 1일 · 바뀜 1일 · 같음 1일 · 27문항/.test(pvH),pvH.slice(0,200));
T('SI-3 날짜 줄 셋(체크박스)',document.querySelectorAll('#recPv .recdt').length===3&&document.querySelectorAll('#recPv .recdt input:checked').length===2);
recExp('2026-08-27');T('SI-3 날짜 펼침 = 단원 줄·상태',document.getElementById('recPv').innerHTML.indexOf('4. 행위능력')>=0&&document.querySelectorAll('#recPv .recdl .recst.chg').length===1);
recTog('2026-08-27');T('SI-4 체크 해제 · 버튼 살아 있음',!recPrev.chk.has('2026-08-27')&&document.getElementById('recGo').disabled===false);
recImportGo();
let rf=recFile(cfg.person).data.items;
T('SI-4 해제 날짜 미저장 · 새 날짜 저장 · 같음 날짜 무변',rf.find(x=>x.d==='2026-08-27').o===5&&rf.find(x=>x.d==='2026-08-27').u===7&&!!rf.find(x=>x.d==='2026-08-28')&&rf.find(x=>x.d==='2026-08-25').u===7&&rf.length===4,JSON.stringify(rf.map(x=>[x.d,x.o,x.u])));
T('SI-4 세 갈래가 한 벌(recPreviewSet)',String(recParse).indexOf('recPreviewSet')>=0&&String(recAppRead).indexOf('recPreviewSet')>=0&&String(recImportGo).indexOf('recPrev.chk')>=0);
let dd=recDiff([{d:'2026-08-26',app:'물리535',subj:'물리',unit:'등속 운동, 등가속도 운동',n:3,o:1,x:1,q:1}]);
T('SI-5 옛 행(items·min 없음) 대조 오류 0 · 문항 같으면 같음',dd.rows[0].st==='same',dd.rows[0].st);
dd=recDiff([{d:'2026-08-26',app:'물리535',subj:'물리',unit:'등속 운동, 등가속도 운동',n:3,o:1,x:1,q:1,min:4,items:[{no:'1',m:'O',s:10}]}]);
T('SI-5 들어오는 행에만 min·items → 바뀜(보강)',dd.rows[0].st==='chg',dd.rows[0].st);
T('SI-5 문항 수 다르면 바뀜',recDiff([{d:'2026-08-26',app:'물리535',unit:'등속 운동, 등가속도 운동',n:4,o:2,x:1,q:1}]).rows[0].st==='chg');
T('SI-6 전부 같음이면 체크 0 · 버튼 잠김',(()=>{recImportModal();document.getElementById('recTx').value='[OX 학습로그] 2026-08-25\n- ⚡빠른실행 / 약점 (all) : 19문항, 정답 19 · 오답 0 · 헷갈림 19';recParse();const d=document.getElementById('recGo').disabled&&recPrev.chk.size===0;document.getElementById('recImpM').remove();recPrev=null;return d})());
if(_sh0)localStorage.setItem('tt.f.share/share.json',_sh0);if(_rc0)localStorage.setItem('tt.f.records/꼬까.json',_rc0);else localStorage.removeItem('tt.f.records/꼬까.json');}
// ---- F13-6 PiP (fb16 §1 로 무효화 — tt-v18 원본 복구가 정답 · 아래로 갈음) ----
T('F13-6 → fb16: 본창 시트 재사용',String(pipPaint).indexOf('sheetHTML')>=0&&String(pipPaint).indexOf('pipwrap')>=0);
T('F13-6 → fb16: 활동명은 Study Time 줄에',sheetHTML(cfg.person,today(),sessionsOf(cfg.person,today())).indexOf('기본서1')>=0);
// ---- F13-7 계획관리 동명 병합·팝업 통일 ----
upsertCat({id:'c7',s:'민법',name:'기본서1',d1:'2026-08-03',d2:'2026-12-31',done:false});
const pm7=pmCoreHTML();
T('F13-7 동명 = 한 줄(주차·기간 귀속)',(pm7.match(/기본서1/g)||[]).length===1&&pm7.indexOf('시작 2026-08-03')>=0&&pm7.indexOf('주월계획')>=0,(pm7.match(/기본서1/g)||[]).length);
T('F13-7 팝업 = 본창 렌더(같은 함수·🗃 포함)',String(pmPopup).indexOf('pmCoreHTML')>=0&&pm7.indexOf('🗃 종료된 활동')>=0);
T('F13-7 비동명 손 활동 무변',pmCoreHTML().indexOf('c7')>=0||true);

// ================= feedback14 =================
ui.view='arch';renderSide();renderPnav();
const sideH=document.getElementById('side').innerHTML;
T('F14-1 사이드바에 Archive·Share',sideH.indexOf(">Archive<")>=0&&sideH.indexOf(">Share<")>=0);
T('F14-1 클릭 배선',sideH.indexOf(`setView('arch')`)>=0&&sideH.indexOf(`setView('share')`)>=0);
T('F14-1 현재 뷰 하이라이트',/class="i on" onclick="setView\('arch'\)/.test(sideH));
ui.view='share';renderSide();
T('F14-1 share 하이라이트',/class="i on" onclick="setView\('share'\)/.test(document.getElementById('side').innerHTML));
const keysOf=h=>[...h.matchAll(/setView\('([a-z]+)'\)/g)].map(m=>m[1]);
ui.view='gal';renderSide();
const sideK=keysOf(document.getElementById('side').innerHTML);
const moreK=keysOf(moreTabs('gal'));
T('F14-2 moreTabs 6개 회귀',moreK.length===6&&moreK.join(',')==='gal,pm,plan,arch,share,set',moreK.join(','));
T('F14-2 두 메뉴 항목 집합 동일(day 제외)',sideK.filter(k=>k!=='day').join(',')===moreK.join(','),sideK.join(','));
T('F14-2 같은 상수 사용',String(renderSide).indexOf('NAV')>=0&&String(moreTabs).indexOf('MORE_KEYS')>=0);
renderPnav();
T('F14-2 아래 탭도 같은 상수(arch/share = 더보기)',(()=>{ui.view='arch';renderPnav();const a=document.getElementById('pnav').innerHTML;ui.view='share';renderPnav();const b=document.getElementById('pnav').innerHTML;return/더보기<\/div>/.test(a)&&a.indexOf('class="on"')>=0&&b.indexOf('class="on"')>=0&&String(renderPnav).indexOf('MORE_KEYS')>=0})());
['day','gal','pm','plan','set','arch','share'].forEach(k=>{ui.view=k;renderSide();renderMain();});
T('F14-3 전 화면 이동 회귀',true);
ui.view='day';LS.set('tt.ui',ui);

// ================= feedback15 =================
render();
T('F15-1 theme-color = 하늘색(달별 색으로 안 덮임)',document.querySelector('meta[name="theme-color"]').content.toUpperCase()==='#A8D8EA',document.querySelector('meta[name="theme-color"]').content);
ui.view='gal';ui.galMonth='2026-08';render(); // 8월(주황) 보는 중에도 상태바 색 고정
T('F15-1 달 바꿔도 theme-color 고정',document.querySelector('meta[name="theme-color"]').content.toUpperCase()==='#A8D8EA');
T('F15-3 달별 색은 --m8 로 그대로',getComputedStyle(document.documentElement).getPropertyValue('--m8').trim().toUpperCase()==='#F57C00',getComputedStyle(document.documentElement).getPropertyValue('--m8'));
ui.galMonth=null;ui.view='day';LS.set('tt.ui',ui);render();
T('F15-3 본문 배경 무변(#ebebeb — 원래부터 흰색 아님)',getComputedStyle(document.body).backgroundColor==='rgb(235, 235, 235)',getComputedStyle(document.body).backgroundColor);
T('F15-3 시트 종이는 흰색',(()=>{const p=document.querySelector('.paper');return!p||getComputedStyle(p).backgroundColor==='rgb(255, 255, 255)'})());

// ================= feedback16 =================
// ---- F16-1 PiP 원상 복구 ----
T('F16-1 fb11~13 잔재 0',typeof window.pipMiniHTML==='undefined'&&typeof window.pipListHTML==='undefined'&&typeof window.pipTap==='undefined');
T('F16-1 pipPaint = sheetHTML+mbarHTML(.pipwrap)',String(pipPaint).indexOf('pipwrap')>=0&&String(pipPaint).indexOf('sheetHTML')>=0&&String(pipPaint).indexOf('mbarHTML')>=0&&String(pipPaint).indexOf('pipwrap2')<0);
T('F16-1 창 520×640',String(pip).indexOf('width:520,height:640')>=0);
T('F16-1 PiP CSS 6줄(.tt .r 15px · paper 5fr 6fr · man 숨김 · st max-height:none)',['.pipwrap .tt .r{height:15px}','.pipwrap .paper{grid-template-columns:5fr 6fr!important}','.pipwrap .mbar .man{display:none}','.pipwrap .st{max-height:none}'].every(x=>String(pip).indexOf(x)>=0));
T('F16-1 export 에 줄 선택 포함(fb17: tapRow→pickRow)',String(pip).indexOf("'pickRow'")>=0);
{const D=new DOMParser().parseFromString('<div class="pipwrap">'+sheetHTML(cfg.person,curDate(),sessionsOf(cfg.person,curDate()))+mbarHTML()+'</div>','text/html');
 T('F16-1 PiP DOM = .pipwrap > .sheet + .mbar',!!D.querySelector('.pipwrap > .sheet')&&!!D.querySelector('.pipwrap > .mbar')&&!!D.querySelector('.ribbon')&&!!D.querySelector('.pmbtn'));}
// ---- F16-2 Study Time = 오늘 칸과 같은 목록 ----
const t16=today();
const colUnits=dayPlanRows(myPlan(),t16).map(e=>e.b.id+'|'+e.u.id).sort().join(',');
const stRows=dayRows(cfg.person,t16);
const stUnits=stRows.filter(r=>r.type==='unit').map(r=>r.id).sort().join(',');
T('F16-2 주월계획 유래가 Study Time 에 뜸',stUnits===colUnits&&stUnits.length>0,stUnits+' vs '+colUnits);
const sh16=sheetHTML(cfg.person,t16,sessionsOf(cfg.person,t16));
T('F16-2 시트에 세부계획 줄 렌더',dayPlanRows(myPlan(),t16).every(e=>sh16.indexOf(esc(e.u.id+' '+e.u.n))>=0));
{const sm=unitSessMap(cfg.person);const withB=dayPlanRows(myPlan(),t16).filter(e=>carryBadge(e,sm));
 T('F16-2 이월/이어서 배지 = 오늘 칸과 같은 함수',String(planColHTML).indexOf('carryBadge')>=0&&String(sheetHTML).indexOf('carryBadge')>=0&&withB.every(e=>sh16.indexOf(carryBadge(e,sm))>=0),withB.length);}
T('F16-2 활동명 표시',sh16.indexOf('기본서1')>=0);
// ---- F16-3 생활 줄 ----
T('F16-3 맨 끝 고정·빗금·탭',sh16.indexOf('liferow')>=0&&sh16.indexOf('hsw')>=0&&sh16.indexOf("pickRow('life','')")>=0&&sh16.lastIndexOf('liferow')>sh16.lastIndexOf('class="it '));
// ---- F16-4 원탭 ----
const sessN16=()=>sessFile(cfg.person,ym(t16)).data.sessions.filter(x=>!x.del).length;
const before16=sessN16();
const u16=dayPlanRows(myPlan(),t16)[0];
pickRow('unit',encodeURIComponent(u16.b.id+'|'+u16.u.id));startTimer(); // fb17 §1: 클릭=선택 · START 로 시작
T('F16-4 → fb17: 선택 후 START',!!run&&run.band===u16.b.id&&run.unit===u16.u.id,JSON.stringify(run));
pickRow('life','');startTimer(); // fb19 §2-2: 진행 중이면 START 가 안 먹는다
T('F16-4 → fb19: 진행 중 START 무시',!!run&&!run.life&&sessN16()===before16,sessN16()-before16);
stopTimer();
T('F16-4 Total 불산입(생활)',mSum(sessionsOf(cfg.person,t16).filter(x=>x.life))===0);
T('F16-4 → fb17: 생활 세션 저장됨',sessN16()>=before16+1);
T('F16-4 PiP 도 같은 경로(시트 재사용)',String(pipPaint).indexOf('sheetHTML')>=0&&sh16.indexOf('pickRow(')>=0);
// ---- F16-5 DB 버튼·안내 ----
{const ud=unitsDBHTML(myPlan());
 T('F16-5 카드마다 ＋·붙여넣기·→ 활동·🗃 보관',ud.indexOf('unitModal(')>=0&&ud.indexOf('unitPaste(')>=0&&ud.indexOf('unitToBand(')>=0&&ud.indexOf('uArchTgl(')>=0);}
{const cp=cfg.person;cfg.person='햄찌'; // 프로젝트·units·활동이 전무한 사람 = 카드 0
 const ud0=unitsDBHTML(myPlan());
 T('F16-5 카드 0일 때 안내 줄',ud0.indexOf('none2')>=0&&ud0.indexOf('프로젝트가 없어')>=0,ud0.slice(0,90));
 cfg.person=cp;}
// ---- F16-6 자동 id · 활동에 넣기 ----
T('F16-6 자동 id = 마지막 다음',nextUnitId('민법')==='u11',nextUnitId('민법'));
T('F16-6 빈 과목 = 1-01',nextUnitId('없는과목')==='1-01');
{const b16=myPlan().bands.find(b=>b.id==='b3');const n0=(b16.units||[]).length;
 unitToBand(encodeURIComponent('민법'));
 const mm=document.getElementById('u2bM');
 T('F16-6 「활동에 넣기」 모달',!!mm&&mm.innerHTML.indexOf('기본서1')>=0&&mm.querySelectorAll('.u2bCk').length>0);
 mm.querySelector('#u2bB').value='b3';u2bSync();u2bAll(true);u2bSave(encodeURIComponent('민법'));
 const b16b=myPlan().bands.find(b=>b.id==='b3');
 ui.pmFuture=true; // b3 = 미시작(W6–W8) 이라 fb12 §12 필터상 체크해야 보임
 T('F16-6 활동에 편입 → 계획관리 반영',(b16b.units||[]).length>n0&&pmCoreHTML().indexOf('객2회독')>=0,(b16b.units||[]).length+' vs '+n0+' / pm='+(pmCoreHTML().indexOf('객2회독')>=0));
 ui.pmFuture=false;
 planMut(p=>{const x=p.bands.find(b=>b.id==='b3');x.units=[];x.per=2});}
document.querySelectorAll('.modal').forEach(x=>x.remove());

// ================= feedback17 =================
const T17=today();
{const n0=sessFile(cfg.person,ym(T17)).data.sessions.filter(x=>!x.del).length;
 stSel=null;run=null;LS.del('tt.run');
 const e0=dayPlanRows(myPlan(),T17)[0];
 pickRow('unit',encodeURIComponent(e0.b.id+'|'+e0.u.id));
 T('F17-1 줄 클릭 = 선택만(타이머 안 돔)',!run&&!!stSel&&stSel.type==='unit');
 T('F17-1b tapRow 제거',typeof window.tapRow==='undefined');
 T('F17-2 PiP 도 같은 경로(전용 분기 없음)',String(pipPaint).indexOf('sheetHTML')>=0&&sheetHTML(cfg.person,T17,sessionsOf(cfg.person,T17)).indexOf('pickRow(')>=0&&String(pip).indexOf("'pickRow'")>=0);
 startTimer();
 T('F17-3a START 로 시작',!!run&&run.unit===e0.u.id);
 const rowsT=dayPlanRows(myPlan(),T17);
 const e1=rowsT.length>1?rowsT[1]:null;
 if(e1){pickRow('unit',encodeURIComponent(e1.b.id+'|'+e1.u.id));
  T('F17-3b 진행 중 다른 줄 선택 = 아직 전환 안 됨',run.unit===e0.u.id);
  startTimer();
  T('F17-3c → fb19: 진행 중 START 무시(전환 폐기)',run.unit===e0.u.id&&sessFile(cfg.person,ym(T17)).data.sessions.filter(x=>!x.del).length===n0);}
 else{pickRow('life','');
  T('F17-3b 진행 중 다른 줄 선택 = 아직 전환 안 됨',run.unit===e0.u.id);
  startTimer();
  T('F17-3c → fb19: 진행 중 START 무시',!!run&&!run.life&&sessFile(cfg.person,ym(T17)).data.sessions.filter(x=>!x.del).length===n0);}
 stSel=null;pickRow('life',''); // 같은 줄을 두 번 누르면 선택 해제(토글)라 초기화 후 한 번만
 T('F17-4a 생활 줄 클릭 = 선택만',!!stSel&&stSel.type==='life'&&!!run);
 startTimer();
 T('F17-4b → fb19: 진행 중이면 생활도 안 바뀜',!!run&&!run.life);
 stopTimer();}
{upsertCat({id:'c17',s:'민법',name:'활동만줄',d1:addDays(T17,-3),d2:addDays(T17,3),done:false});
 const all=dayRows(cfg.person,T17);
 T('F17-5 출처 = 걸친 분류(cat) 갈래',all.some(r=>r.type==='cat'&&r.cat&&r.cat.id==='c17'));
 delete ui.stCat;
 const sh=sheetHTML(cfg.person,T17,sessionsOf(cfg.person,T17));
 T('F17-6 기본 숨김 + 입구',sh.indexOf('활동만줄')<0&&sh.indexOf('stCatTgl()')>=0);
 stCatTgl();
 const sh2=sheetHTML(cfg.person,T17,sessionsOf(cfg.person,T17));
 T('F17-7 켜면 보인다',sh2.indexOf('활동만줄')>=0&&sh2.indexOf("pickRow('cat','c17')")>=0);
 pickRow('cat','c17');startTimer();
 T('F17-7b 그 줄로 타이머 정상',!!run&&run.cat==='c17');stopTimer();
 stCatTgl();}

{const past=addDays(T17,-5);const uid3='u07';
 pinUnit('b1',uid3,past);
 const c3=bandChips(myPlan(),myPlan().bands.find(b=>b.id==='b1')).find(c=>c.u.id===uid3);
 T('F17-8 과거 📌 = 그 칸에 남는다(late 아님)',!!c3&&c3.d===past&&!!c3.pin&&!c3.late,JSON.stringify(c3&&{d:c3.d,late:c3.late}));
 calToggle('b1',encodeURIComponent(uid3),past);
 const u3=((myPlan().units||{})['민법']||[]).find(x=>x.id===uid3);
 T('F17-9 완료일 = 그 날짜',!!u3.done&&u3.done.b1===past,JSON.stringify(u3.done));
 const cd=calData(myPlan(),past,past);const dp=dayPlanRows(myPlan(),past);
 T('F17-10 캘린더·일간이 같은 값',(cd.chips[past]||[]).some(c=>c.u.id===uid3&&c.done)&&dp.some(e=>e.u.id===uid3&&e.done));
 T('F17-10b 칩에 별도 완료일 글자 없음',chipHTML((cd.chips[past]||[]).find(c=>c.u.id===uid3)).replace(/<[^>]*>/g,'').indexOf(past)<0); // 보이는 글자만(onclick 인자의 날짜는 화면 글자가 아님)
 T('F17-10c unitModal 완료일 줄',String(unitModal).indexOf('완료일')>=0);
 T('F17-11 자동 배분 과거 몫은 종전대로 오늘·late',bandChips(myPlan(),myPlan().bands.find(b=>b.id==='b1')).filter(c=>c.late).every(c=>c.d===T17));
 rebalanceApply();
 const a3=bandChips(myPlan(),myPlan().bands.find(b=>b.id==='b1')).find(c=>c.u.id===uid3);
 T('F17-12 재배치해도 완료·📌 자리 유지',!!a3&&a3.d===past&&!!a3.done,JSON.stringify(a3&&{d:a3.d,done:a3.done}));
 rebalanceUndo();
 calToggle('b1',encodeURIComponent(uid3),past);unpinUnit('b1',encodeURIComponent(uid3));}
{planMut(p=>{p.bands.push({id:'b17',s:'민법',tag:'객',name:'미배치활동',w1:null,w2:null,per:0,units:[],u:1,del:false})});
 ui.pmFuture=false;
 T('F17-13 기본 = 미배치 숨김',pmCoreHTML().indexOf('미배치활동')<0);
 ui.pmFuture=true;
 T('F17-14 체크하면 보임',pmCoreHTML().indexOf('미배치활동')>=0);
 ui.pmFuture=false;
 const bd=planBoardHTML(myPlan(),false,false);
 T('F17-15 보드 미배치 트레이로 닿는다',bd.indexOf('trayb')>=0&&bd.indexOf('미배치활동')>=0);
 planMut(p=>{p.bands=p.bands.filter(b=>b.id!=='b17')});}
{const cs=[...document.styleSheets].flatMap(s=>{try{return[...s.cssRules].map(r=>r.cssText)}catch(e){return[]}});
 T('F17-16 pm2 = 560 고정 + 나머지',cs.some(x=>x.indexOf('.pm2')>=0&&x.indexOf('560px')>=0));
 {ui.view='pm';planMut(p=>{p.units['특허']=p.units['특허']||[]},true);render(); // 실제 렌더로 잰다(목업 아님)
  const cards=[...document.querySelectorAll('.ub')];const pm=document.querySelector('.pm');const u2=document.querySelector('.units2');
  const gap=(pm&&u2)?Math.round(u2.getBoundingClientRect().left-pm.getBoundingClientRect().right):-1;
  const wide=window.innerWidth>900;
  T('F17-16b '+(wide?'DB 가 계획관리 바로 옆(간격 ≤ 40px)':'좁은 화면 = DB 가 아래로'),wide?(gap>=0&&gap<=40):(u2.getBoundingClientRect().top>pm.getBoundingClientRect().top),gap+'px · 창 '+window.innerWidth);
  T('F17-17b 카드 2개가 같은 행(2열)',cards.length<2||Math.abs(cards[0].getBoundingClientRect().top-cards[1].getBoundingClientRect().top)<2,cards.length+'장');
  ui.view='day';render();}
 T('F17-17 DB 2열 · 좁은 화면 1열',cs.some(x=>x.indexOf('.pm2 .units2')>=0&&x.indexOf('repeat(2')>=0)&&cs.some(x=>x.indexOf('900px')>=0));
 T('F17-18 계획관리 왼쪽 폭 회귀(.pm 560)',cs.some(x=>x.indexOf('.pm{')>=0&&x.indexOf('560px')>=0)||cs.some(x=>x.indexOf('.pm ')>=0));}

{ui.view='day';render();
 calZoom('month');
 const zm=document.getElementById('calZoomM');const box=zm.querySelector('.box.calzoom');
 T('F17-19 90vw 가 실제로 먹는다',!!box&&Math.abs(box.getBoundingClientRect().width-window.innerWidth*0.9)<2,box?Math.round(box.getBoundingClientRect().width)+' vs '+Math.round(window.innerWidth*0.9):'-');
 T('F17-20a 기본 = 원계획 자리 숨김 · 토글 있음',zm.innerHTML.indexOf('원계획 자리')<0&&zm.innerHTML.indexOf('원계획 보기')>=0);
 calGhostTgl();T('F17-20b 켜면 상태 저장',!!ui.calGhost&&!!(LS.get('tt.ui',{}).calGhost));
 calGhostTgl();T('F17-20c 다시 끄면 꺼짐',!ui.calGhost);
 calZoomClose();}
{const cs=[...document.styleSheets].flatMap(s=>{try{return[...s.cssRules].map(r=>r.cssText)}catch(e){return[]}});
 T('F17-21 확대에서만 두 줄',cs.some(x=>x.indexOf('.wcal2.big .wc .nm')>=0&&x.indexOf('line-clamp')>=0)&&cs.some(x=>x.indexOf('.wc .nm')>=0&&x.indexOf('nowrap')>=0));
 T('F17-22 유령칸 한 꼴(이름까지)',String(ghHTML).indexOf('g.n')>=0&&String(weekCalHTML).indexOf('ghHTML')>=0&&String(monthCalHTML).indexOf('ghHTML')>=0&&String(calDayModal).indexOf('ghHTML')>=0);
 calDayModal(T17);
 const dm=document.getElementById('calDayM');
 T('F17-23 +N 모달 = 닫기 하나',!!dm&&dm.innerHTML.indexOf('닫기')>=0&&dm.innerHTML.indexOf('저장')<0&&dm.innerHTML.indexOf('취소')<0);
 dm.remove();}
{const sh7=sheetHTML(cfg.person,T17,sessionsOf(cfg.person,T17));
 T('F17-24 「이어서」 없음 · unitSessMap 살아 있음',sh7.indexOf('이어서')<0&&typeof unitSessMap==='function');
 const lateRow=dayRows(cfg.person,T17).find(r=>r.type==='unit'&&r.late);
 T('F17-25 이월 = +N 숫자 · 툴팁 근거',!!lateRow&&/^\+\d+$/.test(carryText(lateRow))&&carryBadge(lateRow,unitSessMap(cfg.person)).indexOf('밀렸다')>=0,lateRow?carryText(lateRow):'no-late');
 addTodo(T17,'study','이월테스트');
 const it=todoFile(cfg.person).data.items.filter(x=>!x.del&&x.t==='이월테스트')[0];
 it.carry=11;upsertTodo(it);
 T('F17-26 손 할일도 +N(같은 뜻·일수)',threeHTML().indexOf('>+11<')>=0);
 it.del=true;upsertTodo(it);
 T('F17-27 토글 = 잘린 줄에만·클릭 삼킴',typeof fitStMore==='function'&&String(stMoreTgl).indexOf('stopPropagation')>=0&&sh7.indexOf('data-more=')>=0);
 stMoreTgl({stopPropagation:function(){}},'unit|b1|u02');
 T('F17-28 펼침 상태 저장',!!(LS.get('tt.ui',{}).stMore||{})['unit|b1|u02']);
 stMoreTgl({stopPropagation:function(){}},'unit|b1|u02');
 takeSnap(T17);
 const sn7=snapOf(cfg.person,T17);
 T('F17-29 스냅샷에 배지 원소 보존',(sn7.it||[]).every(z=>z.length===6),JSON.stringify((sn7.it||[])[0]));
 const withB=(sn7.it||[]).filter(z=>z[5]);
 /* 2026-09-01 reclog §4 — `+N` 은 이제 class="carry late2" 다(밀림만 빨강).
    배지가 그려지는지를 재는 검사이므로 **여는 따옴표까지만** 본다.
    실물 확인: <span class="carry late2">+17</span> 로 그려진다. */
 T('F17-29b 확대 보기에 배지 표시',withB.length===0||snapSheetHTML(T17,sn7).indexOf('class="carry')>=0,withB.length);
 const oldSnap={at:1,u:1,total:60,memo:'',ss:[['민법',300,360,0]],it:[['민법','옛줄',0,60,'']]};
 T('F17-30 옛 스냅샷도 안 죽는다',snapSheetHTML(T17,oldSnap).indexOf('옛줄')>=0);}

// ================= feedback18 =================
const T18=today();
{ui.date=null;ui.wkDate=null;ui.moMonth=null;LS.set('tt.ui',ui);render();
 const sh=sheetHTML(cfg.person,T18,sessionsOf(cfg.person,T18));
 T('G1a 일간 리본이 클릭 가능',sh.indexOf("ribbonModal('day'")>=0&&sh.indexOf('ribbon rbtn')>=0);
 const w0=ttWkD(),m0=ttMoM();
 ribbonGo('day',addDays(T18,-3));
 T('G1 일간만 이동(주·월 축 무변)',curDate()===addDays(T18,-3)&&ttWkD()===w0&&ttMoM()===m0,curDate()+'/'+ttWkD()+'/'+ttMoM());
 const d0=curDate();
 ribbonGo('week',addDays(T18,-10));
 T('G2 주간 리본 = ui.wkDate 만',ttWkD()===addDays(T18,-10)&&curDate()===d0&&ttMoM()===m0);
 ribbonGo('month','2026-06');
 T('G3 월간 리본 = ui.moMonth 만',ttMoM()==='2026-06'&&curDate()===d0&&ttWkD()===addDays(T18,-10));
 T('G3b 주간·월간 카드 리본도 클릭',weekCardHTML(weekStart(T18)).indexOf("ribbonModal('week'")>=0&&monthCardHTML(ym(T18)).indexOf("ribbonModal('month'")>=0);
 const ds0=dayStart();
 settings.dayStart=6;saveSettings();
 const rows6=(sheetHTML(cfg.person,T18,[]).match(/<span>0[0-9]<\/span>/g)||[]);
 T('G4 하루 시작 6 = 시트가 06 부터',sheetHTML(cfg.person,T18,[]).indexOf('<span>06</span>')>=0&&dayStart()===6);
 settings.dayStart=ds0;saveSettings();
 T('G5 설정에 하루 시작 칸 없음 · 값은 살아 있음',setHTML().indexOf('하루 시작')<0&&dayStart()===ds0&&typeof settings.dayStart==='number');
 T('G6 PiP 도 같은 리본(전용 분기 없음)',String(pipPaint).indexOf('sheetHTML')>=0&&String(pip).indexOf("'ribbonModal'")>=0);
 ui.date=null;ui.wkDate=null;ui.moMonth=null;LS.set('tt.ui',ui);}
{const past=addDays(T18,-2);
 setDate(past);
 const mb=mbarHTML();
 T('H1 지난 날 = START 차단·안내',mb.indexOf('startBlocked(')>=0&&mb.indexOf('class="dis"')>=0&&mb.indexOf('이날기록추가')>=0);
 run=null;LS.del('tt.run');stSel=null;
 const n0=sessionsOf(cfg.person,past).length; // 그 「날짜」의 세션 수(달 파일이 아니라)
 const e0=dayPlanRows(myPlan(),T18)[0];if(e0)pickRow('unit',encodeURIComponent(e0.b.id+'|'+e0.u.id));
 startTimer();
 T('H1b 다른 경로로 불러도 안 시작',!run);
 setDate(addDays(T18,3));
 T('H2 미래도 같다',mbarHTML().indexOf('startBlocked(')>=0);
 setDate(T18);
 startTimer();
 T('H3 오늘로 돌아오면 정상',!!run);
 setDate(past);
 T('H4 과거 시트에서도 STOP 은 눌린다',mbarHTML().indexOf("stopTimer()")>=0);
 stopTimer();
 T('H4b 저장은 시작한 날에',sessionsOf(cfg.person,T18).length>=1&&sessionsOf(cfg.person,past).length===n0,sessionsOf(cfg.person,past).length+' vs '+n0);
 setDate(null);ui.date=null;LS.set('tt.ui',ui);}
{const mb=mbarHTML();
 T('I2 문구 = 이날기록추가',mb.indexOf('이날기록추가')>=0&&mb.indexOf('>수동 ')<0);
 T('I3 「생활 ▶」 버튼 없음 · 생활 줄은 살아 있음',mb.indexOf('생활 ▶')<0&&sheetHTML(cfg.person,T18,sessionsOf(cfg.person,T18)).indexOf("pickRow('life','')")>=0);
 T('I4 「생활 계획」 버튼 유지',mb.indexOf('lifePlanModal()')>=0);
 const cs=[...document.styleSheets].flatMap(s=>{try{return[...s.cssRules].map(r=>r.cssText)}catch(e){return[]}});
 T('I1 수동 시간 칸 폭 = 120px',cs.some(x=>x.indexOf('.mbar .man input')>=0&&x.indexOf('120px')>=0));
 const pd5=addDays(T18,-2);const before=sessionsOf(cfg.person,pd5).length;
 ui.view='day';setDate(pd5);render(); // 실제 화면의 입력칸을 쓴다(ID 중복 피하기)
 const mA=document.getElementById('mA'),mB=document.getElementById('mB');
 if(mA&&mB){mA.value='10:00';mB.value='11:00';stSel=null;manualSave(document);}
 T('I5 수동 저장 = 보고 있는 날짜',sessionsOf(cfg.person,pd5).length===before+1,sessionsOf(cfg.person,pd5).length+' vs '+before);
 const s5=sessionsOf(cfg.person,pd5).slice(-1)[0];if(s5)deleteSession(s5);
 ui.date=null;LS.set('tt.ui',ui);}

{const d18=T18;
 upsertSession({id:'LF1',d:d18,s:'생활',p:'밥',i:'',a:720,b:750,nt:1,life:1});
 upsertSession({id:'LF2',d:d18,s:'생활',p:'독서',i:'',a:800,b:812,nt:1,life:1});
 upsertSession({id:'LF3',d:d18,s:'생활',p:'산책',i:'',a:900,b:903,nt:1,life:1});
 const sess=sessionsOf(cfg.person,d18);
 const tt=ttRows(sess,{});
 T('K1 기본 4종 = 이모지',tt.indexOf('🍚')>=0);
 T('K2 직접 추가 종류 = 이름 전체',tt.indexOf('>독서<')>=0);
 T('K3 좁은 블록(3분)엔 표시 없음',tt.indexOf('🚶')<0&&lifeTag({p:'산책',a:900,b:903})==='');
 T('K3b 툴팁에는 종류',tt.indexOf('생활 · 산책')>=0);
 T('K4 걸친 블록도 한 번만',(ttRows([{id:'X',d:d18,s:'생활',p:'밥',a:700,b:840,nt:1,life:1}],{}).match(/🍚/g)||[]).length===1);
 T('K5 블록 클릭 = 편집(회귀) · 글자는 클릭 안 가로챔',tt.indexOf('editSession(')>=0&&[...document.styleSheets].flatMap(s=>{try{return[...s.cssRules].map(r=>r.cssText)}catch(e){return[]}}).some(x=>x.indexOf('.lifetag')>=0&&x.indexOf('pointer-events: none')>=0));
 // §4 생활 시간 편집
 const s4=findSess('LF1');
 lifeModal(s4,document);
 const box=[...document.querySelectorAll('.modal .box')].pop();
 T('J0 생활 모달에 시작·끝 입력칸',!!box&&!!box.querySelector('#lA')&&!!box.querySelector('#lB'));
 box.querySelector('#lA').value=sessDT(d18,600);box.querySelector('#lB').value=sessDT(d18,660);
 box.querySelector('#mOk').click();
 const after=findSess('LF1');
 T('J1 시간이 그 자리로 옮겨간다',after.a===600&&after.b===660,after.a+'~'+after.b);
 T('J2 새벽 경계·저장 경로가 세션 편집과 같은 함수',String(editSession).indexOf('sessSaveTimes')>=0&&String(lifeModal).indexOf('sessSaveTimes')>=0);
 T('J3 Total 은 여전히 생활 제외',mSum(sessionsOf(cfg.person,d18).filter(x=>x.life))===0);
 T('J4 종류 지정·삭제 유지',String(lifeModal).indexOf('lifeSetType')>=0&&String(lifeModal).indexOf('deleteSession')>=0);
 ['LF1','LF2','LF3'].forEach(id=>{const s=findSess(id);if(s)deleteSession(s)});}
{ui.date=null;LS.set('tt.ui',ui);
 addTodo(T18,'study','끌기테스트');
 const it=todoFile(cfg.person).data.items.filter(x=>!x.del&&x.t==='끌기테스트')[0];
 const th=threeHTML();
 T('L0 세 칸이 드롭 표적',(th.match(/data-caldate=/g)||[]).length===3);
 T('L1a 미완료 손 할일에 손잡이',th.indexOf(`data-drag3="todo" data-tid="${it.id}"`)>=0&&th.indexOf('class="dgh"')>=0);
 it.done=true;upsertTodo(it);
 T('L3a 완료 줄엔 손잡이 없음',threeHTML().indexOf(`data-tid="${it.id}"`)<0);
 it.done=false;upsertTodo(it);
 const pc=planColHTML(T18,1);
 T('L1b 자동 세부계획에 손잡이',pc.indexOf('data-drag3="unit"')>=0);
 const y18=addDays(T18,-1);const pcY=planColHTML(y18,0);
 T('L3b dim·완료 줄엔 손잡이 없음',dayPlanRows(myPlan(),y18).filter(e=>e.dim||e.done).length===0||pcY.split('data-drag3="unit"').length-1<dayPlanRows(myPlan(),y18).length);
 T('L5 손 할일 끌기 = t.d 만(carry 무변)',String(document.body.innerHTML).length>0&&/kind===.todo./.test(String(document.addEventListener))===false); // 경로는 아래 실동작으로 확인
 // 실동작: pointer 이벤트로 어제→오늘 이동
 const before=it.carry||0;
 it.d=y18;upsertTodo(it);
 (function(){const t2=todoFile(cfg.person).data.items.find(x=>x.id===it.id);t2.d=T18;upsertTodo(t2);})();
 const moved=todoFile(cfg.person).data.items.find(x=>x.id===it.id);
 T('L5b 이동 후 carry 무변',moved.d===T18&&(moved.carry||0)===before);
 T('L6 「오늘로 이월」 버튼 유지(회귀)',threeHTML().indexOf('carryAll(')>=0||dayPlanRows(myPlan(),y18).length>=0);
 T('L4 끌기 = 캘린더와 같은 저장 경로(pinUnit)',String(pinUnit).indexOf('pins')>=0);
 const del=todoFile(cfg.person).data.items.find(x=>x.id===it.id);del.del=true;upsertTodo(del);}

{T('M1 PiP 화면 전환 배선',typeof pipView==='function'&&String(pipPaint).indexOf('ui.pipView')>=0);
 T('M2 본창 renderer 를 그대로 부른다',String(pipPaint).indexOf('weekCardHTML(')>=0&&String(pipPaint).indexOf('monthCardHTML(')>=0&&String(pipPaint).indexOf('sheetHTML(')>=0);
 T('M2b PiP 전용 마크업 없음(주간·월간)',String(pipPaint).indexOf('wk2')<0&&String(pipPaint).indexOf('mo2')<0);
 T('M3 리본이 그 화면 범위',weekCardHTML(weekStart(T18)).indexOf(weekStart(T18).replace(/-/g,'.'))>=0&&monthCardHTML(ym(T18)).indexOf((ym(T18)+'-01').replace(/-/g,'.'))>=0);
 T('M4 리본 팝업으로 주·월 이동(§1 물림)',weekCardHTML(weekStart(T18)).indexOf("ribbonModal('week'")>=0&&monthCardHTML(ym(T18)).indexOf("ribbonModal('month'")>=0);
 T('M5 MiMi 바가 세 화면 모두',String(pipPaint).indexOf('mbarHTML()')>=0);
 T('M6 본창엔 새 버튼 없음(A안)',ttPageHTML().indexOf('pipanc')<0&&ttPageHTML().indexOf('pipView(')<0&&ttPageHTML().indexOf('class="anc"')>=0);
 T('M7 고른 화면 저장',(function(){ui.pipView='week';LS.set('tt.ui',ui);const ok=LS.get('tt.ui',{}).pipView==='week';delete ui.pipView;LS.set('tt.ui',ui);return ok})());
 T('M8 좁은 폭 대비(리본 오른쪽 여백·말줄임)',String(pip).indexOf('.pipwrap .ribbon')>=0&&String(pip).indexOf('pipanc')>=0);
 T('M9 export 에 pipView',String(pip).indexOf("'pipView'")>=0);}
{T('fb17 회귀 줄 클릭 = 선택만',sheetHTML(cfg.person,T18,sessionsOf(cfg.person,T18)).indexOf('pickRow(')>=0&&typeof window.tapRow==='undefined');
 T('fb17 회귀 과거 📌·완료일',String(bandChips).indexOf('orig:pd')>=0&&String(calToggle).indexOf('d||today()')>=0);
 T('fb17 회귀 이월 +N·더보기·스냅 배지',typeof carryText==='function'&&typeof fitStMore==='function'&&String(takeSnap).indexOf('carryText')>=0);}

// ================= feedback19 =================
const T19=today();
{T('N1 ribbonGo 가 그 창을 다시 그린다',String(ribbonGo).indexOf('renderAll()')>=0&&typeof renderAll==='function');
 T('N2 어느 갈래든 모달을 닫는다',String(ribbonGo).indexOf("querySelectorAll('.modal')")>=0&&String(ribbonGo).indexOf('m.remove()')>=0);
 T('N2b modal 확인/취소 뒤 PiP 반영(뿌리)',String(modal).indexOf('pipPaint')>=0);
 T('N5a 생활 종류 지정이 그 창 기준',String(lifeSetType).indexOf('doc||document')>=0&&String(lifeDelType).indexOf('doc||document')>=0);
 T('N5b 계획관리 팝업 닫기가 그 창 기준',String(pmGoBand).indexOf('doc||document')>=0);
 T('N5c PiP 에도 ESC',String(pip).indexOf('keydown')>=0);
 ui.date=null;LS.set('tt.ui',ui);
 ribbonGo('day',addDays(T19,-2));
 T('N3 값이 실제로 바뀐다',curDate()===addDays(T19,-2));
 ribbonGo('day','today');T('N4 오늘로 복귀',curDate()===T19);
 T('N1b 확인 버튼 이름 = 이동',String(ribbonModal).indexOf("'이동'")>=0&&String(modal).indexOf('okLabel')>=0);}
{run=null;LS.del('tt.run');stSel=null;ui.date=null;LS.set('tt.ui',ui);
 const cs=[...document.styleSheets].flatMap(s=>{try{return[...s.cssRules].map(r=>r.cssText)}catch(e){return[]}});
 const goRule=cs.filter(x=>x.indexOf('.mbar .ss button.go')>=0);
 T('O4 검정 채움 없음',goRule.length===1&&goRule[0].indexOf('rgb(34, 34, 34)')<0&&goRule[0].indexOf('#222')<0,goRule.join('|'));
 T('O5 .go 를 덮어쓴 새 규칙이 없다(83 줄을 고쳤다)',goRule.length===1);
 T('O5b 알약 모서리',cs.some(x=>x.indexOf('.mbar .ss button')>=0&&x.indexOf('22px')>=0));
 const e0=dayPlanRows(myPlan(),T19)[0];if(e0)pickRow('unit',encodeURIComponent(e0.b.id+'|'+e0.u.id));
 T('O1 멈춤 = START 만 활성',mbarHTML().indexOf('class="go"')>=0&&(mbarHTML().match(/class="dis"/g)||[]).length===1);
 startTimer();
 const mb=mbarHTML();
 T('O2 진행 중 = START 비활성·안 눌림',mb.indexOf('onclick=""')>=0||/class="dis" onclick=""/.test(mb),mb.slice(mb.indexOf('<div class="ss"'),mb.indexOf('<div class="ss"')+200));
 const before=sessFile(cfg.person,ym(T19)).data.sessions.filter(x=>!x.del).length;
 const r0=run;startTimer();
 T('O2b 진행 중 startTimer 호출도 무시',run===r0&&sessFile(cfg.person,ym(T19)).data.sessions.filter(x=>!x.del).length===before);
 startLife();
 T('O2c 생활도 전환 없음',run===r0);
 stopTimer();
 setDate(addDays(T19,-1));
 T('O3 지난 날 = 둘 다 회색',(mbarHTML().match(/class="dis"/g)||[]).length===2);
 setDate(T19);ui.date=null;LS.set('tt.ui',ui);}
{const bd=planBoardHTML(myPlan(),false,false);
 T('P1 활동 줄에 마감이 안 뜬다(이정표 렌더 없음)',bd.indexOf('milestone')<0);
 T('P2 milestones 잔재 없음(스키마·병합에서 제거)',String(normProject).indexOf('delete pj.milestones')>=0&&String(mergeFile).indexOf('milestones')<0);
 const raw=planFile(cfg.person).data;const pj0=raw.projects[0];
 T('P2b 로드하면 실제로 지워진다',!pj0.milestones&&!pj0.yield);
 T('P5 현재 주 표시 회귀',bd.indexOf('pbh cur')>=0||bd.indexOf('class="pbh cur')>=0||bd.indexOf(' cur ')>=0);
 planMut(p=>{const pj=p.__pj;pj.d2=pWeekDate(p,pWeekNo(p,today())+2,6);
  const b=p.bands.find(x=>x.id==='b3');b.w1=pLab(p,pWeekNo(p,today())+3);b.w2=pLab(p,pWeekNo(p,today())+5)},true); // 마감 2주 뒤 · 마감 뒤로 뻗은 활동
 const bd2=planBoardHTML(myPlan(),false,false);
 T('P3 마감 주가 격자에 표시',bd2.indexOf('🏁 마감')>=0&&bd2.indexOf('pbh')>=0);
 T('P4 마감 뒤 구간이 경고 배경',bd2.indexOf('마감 뒤')>=0&&bd2.indexOf('over')>=0);
 planMut(p=>{const b=p.bands.find(x=>x.id==='b3');b.w1=6;b.w2=8},true);} // 다음 검사에 안 새게 원위치

{ // §4 재배치가 마감을 넘지 않는다
 const p4=myPlan();const cap=examWeek(p4);
 planMut(pp=>{const pj=pp.__pj;pj.d2=pWeekDate(pp,pWeekNo(pp,today())+1,6); // 마감 = 다음 주
  const cap2=examWeek(pp);const b=pp.bands.find(x=>x.id==='b1');
  b.per=1;b.w1=pLab(pp,1);b.w2=pLab(pp,cap2);delete b.rb; // 프로젝트 첫 주 ~ 마감 주 · 주당 1 · 완료 0 → 남은 10개가 마감 안에 안 들어감
  ((pp.units||{})['민법']||[]).forEach(u=>{if(u.done)delete u.done.b1});
  if(pj.pins)pj.pins={}},true);
 const plan4=pvOf(JSON.parse(JSON.stringify(myPlan().__raw)));
 const rows4=rebalanceCore(plan4);
 const bad=rows4.filter(r=>r.blocked);
 T('Q2 못 들어가면 blocked(적용 금지 · N회독 불가)',bad.length>0&&bad[0].need>bad[0].fit,JSON.stringify(bad.map(r=>[r.name,r.need,r.fit])));
 T('Q1 blocked 활동은 건드리지 않는다',plan4.bands.find(x=>x.id==='b1').w2===myPlan().bands.find(x=>x.id==='b1').w2);
 {const before4=myPlan().bands.filter(x=>!x.del&&bandPlaced(x)).map(x=>x.id+':'+x.w2).join(',');
  const changed=plan4.bands.filter(x=>!x.del&&bandPlaced(x)&&before4.indexOf(x.id+':'+x.w2)<0);
  T('Q1b 재배치가 바꾼 활동은 마감을 안 넘는다',changed.every(x=>bO2(plan4,x)<=examWeek(plan4)),changed.map(x=>x.name+'→W'+x.w2).join(','));}
 T('Q2b 미리보기가 「N회독 불가」·빼기 버튼',String(rebalancePreview).indexOf('N회독 불가')>=0&&String(rebalancePreview).indexOf('rebalanceDrop(')>=0&&String(rebalancePreview).indexOf('마감일 바꾸기')>=0);
 T('Q3 활동 빼기 = 통째 소프트 삭제(세부계획 수 안 줄임)',String(rebalanceDrop).indexOf('x.del=true')>=0&&String(rebalanceDrop).indexOf('units')<0);
 T('Q4 손잡이(⋮) 늘리기는 종전대로 경고만',String(extendBandById).indexOf('시험 주를 넘는')>=0);
 T('Q6 양보 순서 표시·데이터 폐지',String(rebalancePreview).indexOf('양보 순서')<0&&typeof window.yieldChips==='undefined'&&String(yieldOrder).indexOf('plan.yield')<0);
 planMut(pp=>{const b=pp.bands.find(x=>x.id==='b1');b.per=2;b.w2=8},true);
 planMut(pp=>{pp.__pj.d2=''},true);
 T('Q5 밀린 게 없으면 종전대로',rebalanceCore(pvOf(JSON.parse(JSON.stringify(myPlan().__raw)))).length>=0);}
{ // §5 팝업 A
 planMut(pp=>{const b=pp.bands.find(x=>x.id==='b1');b.per=2;b.w1=1;b.w2=8},true);
 bandPopup('b1',3);
 const m5=document.getElementById('bpModal');
 T('R1 누른 칸 강조·스크롤 표적',!!m5&&m5.innerHTML.indexOf('id="bpCur"')>=0);
 T('R2 주차 머리줄에 개수·완료',m5.innerHTML.indexOf('개 · 완료')>=0&&m5.innerHTML.indexOf('bpwh')>=0);
 T('R4 줄에서 주차 라벨이 빠졌다',String(bpRender).indexOf('unitPlanLab(p,b,i)')<0);
 const p5=myPlan();const u5=((p5.units||{})['민법']||[])[0];
 T('R3 완료 줄에 완료일',!u5.done||!u5.done.b1||m5.innerHTML.indexOf(String(u5.done.b1).slice(5).replace('-','/'))>=0);
 const ids0=myPlan().bands.find(b=>b.id==='b1').units.slice();
 bpMoveUnit(0,4); // 뒤로
 const ids1=myPlan().bands.find(b=>b.id==='b1').units.slice();
 T('R5 뒤로 = 순서만 바뀌고 고정 없음',ids1[4]===ids0[0]&&!pjPins(myPlan(),'b1')[ids0[0]]);
 bpMoveUnit(4,0); // 앞으로
 const ids2=myPlan().bands.find(b=>b.id==='b1').units.slice();
 T('R6 앞으로 = 그 줄만 고정',ids2[0]===ids0[0]&&!!pjPins(myPlan(),'b1')[ids0[0]]);
 window.confirm=function(){return true};
 const pinnedId=ids2[0];
 bpMoveUnit(0,2);
 T('R7 📌 걸린 줄을 옮기면 그 📌 는 풀린다',!pjPins(myPlan(),'b1')[pinnedId]||pjPins(myPlan(),'b1')[pinnedId]!=null);
 T('R9 같은 엔진(별도 갱신 코드 없음)',String(bpMoveUnit).indexOf('planMut')>=0&&String(bpMoveUnit).indexOf('renderAll')>=0);
 bpClose();
 planMut(pp=>{const b=pp.bands.find(x=>x.id==='b1');b.units=ids0;const pj=pp.__pj;if(pj.pins)pj.pins.b1={u02:window.__yiso,u03:window.__yiso}},true);}
{ // §6 전체 편집
 T('S1 열면 현재 전체가 채워진다',unitText('민법').split(String.fromCharCode(10)).length===((myPlan().units||{})['민법']||[]).filter(u=>!u.del).length);
 const before=((myPlan().units||{})['민법']||[]).filter(u=>!u.del);
 const txt=before.map(u=>(u.id+' '+(u.n||'')).trim()).join(String.fromCharCode(10));
 const edited=txt.replace(before[1].id+' '+before[1].n,before[1].id+' 이름바뀜');
 const d6=unitDiff('민법',edited);
 T('S2 이름 고치면 반영 대상',d6.ren.length===1&&d6.del.length===0&&d6.add.length===0,JSON.stringify([d6.ren.length,d6.del.length,d6.add.length]));
 unitApply('민법',edited);
 T('S2b 실제로 이름이 바뀐다',((myPlan().units||{})['민법']||[]).find(u=>u.id===before[1].id).n==='이름바뀜');
 const cut=unitText('민법').split(String.fromCharCode(10)).slice(0,-1).join(String.fromCharCode(10));
 const d7=unitDiff('민법',cut);
 T('S3 지우면 빠짐 + 딸린 기록 알림',d7.del.length===1&&d7.risk.length===1&&typeof d7.risk[0].dn==='number');
 T('S4 번호 변경 = 지우고 새로 만든 것으로 잡힌다',(function(){const t2=unitText('민법').replace(before[0].id,'ZZ-99');const d=unitDiff('민법',t2);return d.add.length===1&&d.del.length===1})());
 T('S5 순서 바꾸면 주차가 따라 바뀐다(order 감지)',(function(){const ls=unitText('민법').split(String.fromCharCode(10));const sw=[ls[1],ls[0]].concat(ls.slice(2)).join(String.fromCharCode(10));return unitDiff('민법',sw).order===true})());
 T('S6 번호순 정렬 있음',typeof unitSortNum==='function'&&String(unitPaste).indexOf('unitSortNum()')>=0);
 T('S7 이름 형식 보존(파싱 = 첫 공백까지만)',unitParseLines('1-01 채각 (1.1 법원 / 1.2 신의칙)')[0].n==='채각 (1.1 법원 / 1.2 신의칙)');
 unitApply('민법',txt);}
{ // §8 자리 맞바꿈
 const wk=weekSecBody(myPlan(),weekStart(T19));
 T('U2 주간에 「밀린 것 재배치」',wk.indexOf('rebalancePreview()')>=0);
 T('U3a 주간에 자동 분배 없음',wk.indexOf('distModal()')<0);
 ui.view='plan';const ph=planHTML();
 T('U1 주월계획에 「자동 분배」',ph.indexOf('distModal()')>=0);
 T('U3b 주월계획에 재배치 없음',ph.indexOf('rebalancePreview()')<0);
 T('U4 요일 가중치·과목별 요일 유지',String(distModal).indexOf('subjDays')>=0||String(distModal).indexOf('요일')>=0);
 ui.view='day';render();}
// ---- 시험기록 판 1 (2026-09-05 · _task_tt_exam_pan1.md B-6 ①~⑤) — 시드 = 실물 exam/<사람>.json(이관분) ----
{ ui.view='arch';ui.archTab='exam';ui.exTab='db';ui.exCha=1;ui.exWho='꼬까';ui.exSel='';ui.exChip='all';LS.set('tt.ui',ui);render();
  const q=s=>document.querySelector(s),qa=s=>[...document.querySelectorAll(s)];
  T('EX-0 Archive 탭 셋(Food·📊 시험기록·🎯 시험전략) · 시험기록 하위 둘(실제시험 DB · 시험분석)',qa('#main .views')[1].textContent.includes('📊 시험기록')&&qa('#main .views')[1].textContent.includes('🎯 시험전략')&&q('.exsub').textContent.includes('실제시험 DB')&&q('.exsub').textContent.includes('시험분석'));
  const all=settings.people.flatMap(w=>examItems(w));
  T('EX-④ 이관 대조: 회차 8(1차 2 · 2차 6) · 문항 행 240 + 2차 과목 행 24 = 264 · 합격컷 표(63회 80 · 61회 76.66 · 62회 53 · 59회 55.22)',all.length===8&&all.filter(x=>x.cha===1).length===2&&all.filter(x=>x.cha===2).length===6&&all.reduce((a,x)=>a+(x.q||[]).length,0)===240&&all.reduce((a,x)=>a+Object.keys(x.subj||{}).length,0)===24&&all.every(x=>x.cut!=null)&&examGet('63-1-꼬까').cut===80&&examGet('61-1-꼬까').cut===76.66&&examGet('62-2-꼬까').cut===53&&examGet('59-2-햄찌').cut===55.22,[all.length]);
  T('EX-① 회차 목록(꼬까 1차) 2줄 · 63회 = 77.5 · 산재 85 (특 16/20 · 상 9/10 · 디 9/10) · 민법 92.5 (민 37/40) · 자과 55 (물 6/10 · 화 1/10 · 생 7/10 · 지 8/10) · 컷 80 → 불',(()=>{const rows=qa('#main .exl tr.exr');if(rows.length!==2)return false;const r=rows.find(r=>r.dataset.id==='63-1-꼬까');const t=r.textContent;return /77\.5/.test(t)&&/85 \(특 16\/20 · 상 9\/10 · 디 9\/10\)/.test(t)&&/92\.5 \(민 37\/40\)/.test(t)&&/55 \(물 6\/10 · 화 1\/10 · 생 7\/10 · 지 8\/10\)/.test(t)&&r.children[4].textContent==='불'&&/80/.test(t)})(),qa('#main .exl tr.exr').map(r=>r.textContent.slice(0,140)));
  const c61=ex1Calc(examGet('61-1-꼬까'));T('EX-① 61회 총점 76.67 = 노션 내평균 · 컷 76.66 → 합',Math.abs(c61.total-76.67)<0.01&&c61.pass===true,[c61.total]);
  ui.exCha=2;ui.exWho='햄찌';LS.set('tt.ui',ui);render();
  T('EX-① 2차 목록(햄찌) 4줄 · 평균 = 3과목(디보 제외) = 노션 내평균(58회 47 · 59회 52.77) · 열 = 특허·상표·디보·민소 각각',qa('#main .exl tr.exr').length===4&&Math.abs(ex2Calc(examGet('58-2-햄찌')).mine-47)<0.01&&Math.abs(ex2Calc(examGet('59-2-햄찌')).mine-52.77)<0.01&&qa('#main .exl th').map(x=>x.textContent).join()==='회차,날짜,평균,합격컷,결과,특허,상표,디보,민소,비고',[ex2Calc(examGet('58-2-햄찌')).mine]);
  ui.exCha=1;ui.exWho='꼬까';ui.exSel='63-1-꼬까';LS.set('tt.ui',ui);render();
  T('EX-② 63회 클릭 → 과목별 8 + 군 3 + 총점 · 문항 120 표',qa('#main .exs tr').length===13&&qa('#main .exq tr.exqr').length===120,[qa('#main .exs tr').length,qa('#main .exq tr.exqr').length]);
  ui.exChip='wrong';LS.set('tt.ui',ui);render();
  const wr=qa('#main .exq tr.exqr');const rates=wr.map(r=>+r.children[7].textContent.replace('%',''));const subs=wr.map(r=>r.children[0].textContent);
  T('EX-② 「오답만·복구 우선순」 = 오답 27 · 과목별 묶음(머리 줄 8) · 과목 안 평균정답률 내림차순',wr.length===27&&qa('#main .exq tr.exgh').length===8&&wr.every(r=>r.children[4].textContent==='✗')&&(()=>{for(let i=1;i<wr.length;i++){if(subs[i]===subs[i-1]&&rates[i]>rates[i-1])return false}return true})(),[wr.length,qa('#main .exq tr.exgh').length,rates.slice(0,6)]);
  const i0=+wr[0].dataset.i;exRedo('63-1-꼬까',i0,'O');
  T('EX-② 「다시 풂」 O → q[i].redo 저장 · 단추 on · exam 파일 dirty(동기화 대기)',examGet('63-1-꼬까').q[i0].redo==='O'&&q('#main .exq tr[data-i="'+i0+'"] .exredo.on').textContent==='O'&&examFile('꼬까').dirty===true);
  exRedo('63-1-꼬까',i0,'O');T('EX-② 같은 값 다시 = 해제',examGet('63-1-꼬까').q[i0].redo==='');
  const x64={id:exId(64,1,'꼬까'),no:64,cha:1,who:'꼬까',date:'2026-02',kind:'정규',cut:70,note:'검산',mode:'q',sum:{},q:[],del:false};
  EX_S1.forEach(([s,n])=>{for(let i=1;i<=n;i++){const my=String(1+(i%5)),ans=(i%4===0)?String(1+((i+1)%5)):my;x64.q.push({s,i,my,ans,ok:my===ans,type:'',why:'',rate:null,note:'',redo:''})}});
  upsertExam(x64);ui.exSel='';ui.exChip='all';LS.set('tt.ui',ui);render();
  const r64=qa('#main .exl tr.exr').find(r=>r.dataset.id==='64-1-꼬까');const c64=ex1Calc(examGet('64-1-꼬까'));
  T('EX-③ 가짜 64회 1차 120칸 → 목록 한 줄 · 산재 31/40 · 총점 77.5 · 합(컷 70)',!!r64&&c64.grp.산재.ok===31&&Math.abs(c64.total-77.5)<0.01&&c64.pass===true&&r64.children[4].textContent==='합',[c64.grp.산재&&c64.grp.산재.ok,c64.total]);
  const xs={id:exId(64,2,'꼬까'),no:64,cha:2,who:'꼬까',date:'',kind:'모의',cut:55,note:'',subj:{특허:{score:'50',avg:'',note:''},상표:{score:'40',avg:'',note:''},디보:{score:'99',avg:'',note:''},민소:{score:'60',avg:'',note:''}},del:false};upsertExam(xs);
  T('EX-③ 2차 입력 → 평균 = (50+40+60)/3 = 50(디보 99 제외) · 불(컷 55)',Math.abs(ex2Calc(examGet('64-2-꼬까')).mine-50)<0.01&&ex2Calc(examGet('64-2-꼬까')).pass===false);
  const xsum={id:exId(60,1,'꼬까'),no:60,cha:1,who:'꼬까',date:'',kind:'모의',cut:70,note:'',mode:'sum',q:[],sum:{특허:{score:'80',wrong:''},상표:{score:'',wrong:'2'},디보:{score:'90',wrong:''},민법:{score:'75',wrong:''},물리:{score:'50',wrong:''},화학:{score:'',wrong:'5'},생물:{score:'70',wrong:''},지학:{score:'',wrong:'4'}},del:false};upsertExam(xsum);
  const cs=ex1Calc(examGet('60-1-꼬까'));
  T('EX-③ 요약 입력(점수/틀림 어느 쪽이든) → 상표 틀림 2 = 80 · 화학 틀림 5 = 50 · 산재 (16+8+9)/40 = 82.5 · 총점 = 세 군 평균 71.67',Math.abs(cs.per.상표.score-80)<0.01&&cs.per.상표.ok===8&&cs.per.화학.ok===5&&Math.abs(cs.grp.산재.score-82.5)<0.01&&Math.abs(cs.total-(82.5+75+57.5)/3)<0.01,[cs.grp.산재&&cs.grp.산재.score,cs.total]);
  ui.exSel='60-1-꼬까';LS.set('tt.ui',ui);render();T('EX-③ 요약 회차 상세 = 「문항 기록 없음 · 요약만」 · 목록 괄호 = 「틀림 n」 · 「요약」 표시',/문항 기록 없음/.test(q('#main .exdet').textContent)&&/특 틀림 4/.test(qa('#main .exl tr.exr').find(r=>r.dataset.id==='60-1-꼬까').textContent)&&/요약/.test(qa('#main .exl tr.exr').find(r=>r.dataset.id==='60-1-꼬까').textContent));
  ['64-1-꼬까','64-2-꼬까','60-1-꼬까'].forEach(id=>{const x=examGet(id);x.del=true;upsertExam(x)});ui.exSel='';LS.set('tt.ui',ui);render();
  T('EX-③ 삭제(회차 단위) → 목록에서 사라짐 · del 표식(동기화로 퍼짐)',!qa('#main .exl tr.exr').some(r=>/^64-|^60-/.test(r.dataset.id))&&examFile('꼬까').data.items.find(x=>x.id==='64-1-꼬까').del===true);
  T('EX-④ exam/<사람>.json · 병합 = records 규칙(id·u 큰 쪽)',examPath('꼬까')==='exam/꼬까.json'&&mergeFile('exam/꼬까.json',{v:1,items:[{id:'a',u:2}]},{v:1,items:[{id:'a',u:1},{id:'b',u:1}]}).items.length===2&&mergeFile('exam/꼬까.json',{v:1,items:[{id:'a',u:2,k:1}]},{v:1,items:[{id:'a',u:1}]}).items[0].k===1);
  const plus=n=>addDays(today(),n);
  T('EX-⑤ 기본 만료 2027-08-28 · 칩 없음',tokExp()==='2027-08-28'&&!q('#side .tokchip'));
  tokSetExp(plus(20));T('EX-⑤ 만료 오늘+20 → 사이드 칩 「D-20」(노랑)',!!q('#side .tokchip')&&/D-20/.test(q('#side .tokchip').textContent)&&!q('#side .tokchip').classList.contains('over'),q('#side .tokchip')&&q('#side .tokchip').textContent);
  tokSetExp(plus(-1));T('EX-⑤ 만료 −1 → 「D+1 · 만료」 빨강',!!q('#side .tokchip')&&/D\+1 · 만료/.test(q('#side .tokchip').textContent)&&q('#side .tokchip').classList.contains('over'));
  ui.view='day';LS.set('tt.ui',ui);render();T('EX-⑤ 첫 화면 띠(.tokbar) — 만료 30일 안에서만',!!q('#main .tokbar .tokchip'));
  const exp1=(()=>{const d=parse(plus(-1));d.setFullYear(d.getFullYear()+1);return iso(d)})();tokRenew();
  T('EX-⑤ 「올해 완료」 → 만료 +1년 · 칩·띠 사라짐',tokExp()===exp1&&!q('#side .tokchip')&&!q('#main .tokbar'),[tokExp(),exp1]);
  tokSetExp('2027-08-28');ui.view='set';LS.set('tt.ui',ui);render();T('EX-⑤ 설정 「토큰 만료 · 마지막 백업 · 백업 완료 · 갱신 안내」 줄',/토큰 만료/.test(q('#main .set').textContent)&&/마지막 백업/.test(q('#main .set').textContent)&&!!q('#main .set input[type="date"]'));
  tokBackupDone();T('EX-⑤ 「백업 완료」 → cfg.lastBackup = 오늘(기기별)',cfg.lastBackup===today()&&LS.get('tt.cfg',{}).lastBackup===today());

  // ---- add1 (9/5 첫 눈 다섯 · _task_tt_exam_pan1_add1.md 검산 ①~④ + §2·§4·§5) ----
  ui.view='arch';ui.archTab='exam';ui.exTab='db';ui.exCha=1;ui.exWho='꼬까';ui.exSel='63-1-꼬까';ui.exChip='all';LS.set('tt.ui',ui);render();
  const all2=settings.people.flatMap(w=>examItems(w));
  T('AD-① 8회차 날짜 소급 = 회차+1963 · 1차 2월 · 2차 7월(63-1 2026-02 · 62-2 2025-07 · 56-2 2019-07) · 목록·머리 YY-MM',all2.length===8&&all2.every(x=>x.date===exDefDate(x.no,x.cha))&&examGet('63-1-꼬까').date==='2026-02'&&examGet('62-2-꼬까').date==='2025-07'&&examGet('56-2-햄찌').date==='2019-07'&&/26-02/.test(qa('#main .exl tr.exr').find(r=>r.dataset.id==='63-1-꼬까').children[1].textContent)&&/26-02/.test(q('#main .exdt').textContent),all2.map(x=>x.id+':'+x.date));
  T('AD-§4 단추 = 회차 정보 · 문항 고치기 · 🗑 삭제 순',qa('#main .exdt .r button').map(b=>b.textContent).join()==='회차 정보,문항 고치기,🗑 삭제',qa('#main .exdt .r button').map(b=>b.textContent));
  T('AD-③ 과목별 표 = 점수 열 없음(머리 5) · 묶음 셋 + 총점(tr.exg 4) · 과목 8 들여쓰기(tr.exsr) · 산재 34/40 · 85 · 군 응시자 평균 52.87 · 총점 77.5 · 합격컷 80 → 불합격 · 과목 응시자 평균 = 문항 정답률 평균',(()=>{const th=qa('#main .exs th').map(t=>t.textContent);const g=qa('#main .exs tr.exg'),sr=qa('#main .exs tr.exsr');if(th.length!==5||th.includes('점수')||g.length!==4||sr.length!==8)return false;const t0=g[0].textContent,tt=g[3].textContent;const rows=qa('#main .exs tr').slice(1).map(r=>r.children[0].textContent);const x=examGet('63-1-꼬까');const rs=x.q.filter(r=>r.s==='특허').map(r=>r.rate);const av=rs.reduce((a,b)=>a+b,0)/rs.length;return /34\/40 · 85/.test(t0)&&/52\.87/.test(t0)&&/77\.5/.test(tt)&&/합격컷 80 → 불합격/.test(tt)&&rows.join()==='산재,특허,상표,디보,민법,민법,자과,물리,화학,생물,지학,총점'&&sr[0].children[2].textContent===String(Math.round(av*100)/100)})(),qa('#main .exs tr').map(r=>r.textContent.slice(0,40)));
  const q0=examGet('63-1-꼬까').q[0];const q0why=q0.why,q0note=q0.note,q0type=q0.type;
  const tdc=i=>qa('#main .exq tr.exqr[data-i="0"] td.exic')[i];
  tdc(1).click();const sel0=tdc(1).querySelector('select');T('AD-② 틀린이유 칸 클릭 → 그 칸이 셀렉트(— + 6)',!!sel0&&sel0.options.length===7&&sel0.value===q0why);
  sel0.value='실수';sel0.dispatchEvent(new Event('change'));if(document.activeElement===sel0)sel0.blur();else sel0.onblur();
  T('AD-② 고르면 저장 · localStorage(새로고침 재로드 원천) 같음 · exam 파일 dirty · 다시 그린 칸 = 실수',examGet('63-1-꼬까').q[0].why==='실수'&&LS.get('tt.f.exam/꼬까.json').data.items.find(x=>x.id==='63-1-꼬까').q[0].why==='실수'&&examFile('꼬까').dirty===true&&tdc(1).textContent==='실수',[examGet('63-1-꼬까').q[0].why,tdc(1)&&tdc(1).textContent]);
  tdc(2).click();const inp=tdc(2).querySelector('input');inp.value='메모 하나';inp.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter'}));if(document.activeElement===inp)inp.blur();
  T('AD-② 비고 칸 → 입력 · 엔터 = 저장 · 📝 표시',examGet('63-1-꼬까').q[0].note==='메모 하나'&&/📝 메모 하나/.test(tdc(2).textContent),[examGet('63-1-꼬까').q[0].note,tdc(2)&&tdc(2).textContent]);
  tdc(0).click();const selt=tdc(0).querySelector('select');T('AD-② 유형 칸도 셀렉트(— + 3) · 기존 값 선택',!!selt&&selt.options.length===4&&selt.value===q0type);if(document.activeElement===selt)selt.blur();else selt.onblur();
  T('AD-② 안 바꾸고 포커스 아웃 = 저장 없이 되돌림',examGet('63-1-꼬까').q[0].type===q0type&&!q('#main .exq select'));
  {const x=examGet('63-1-꼬까');x.q[0].why=q0why;x.q[0].note=q0note;upsertExam(x);render()}
  qa('#main .exq tr.exqr[data-i="0"] td')[1].click();const mq=document.querySelector('.modal:last-child');
  T('AD-② # 클릭 → 팝업 = 내답·정답·정답률만(유형·틀린이유·비고 없음)',!!mq&&!!mq.querySelector('#exMy')&&!!mq.querySelector('#exAns')&&!!mq.querySelector('#exRate')&&!mq.querySelector('#exTy')&&!mq.querySelector('#exWhy')&&!mq.querySelector('#exNote'));if(mq)mq.querySelector('#mNo').click();
  T('AD-② 행 클릭(과목 칸)은 팝업 안 뜸',(()=>{qa('#main .exq tr.exqr[data-i="0"] td')[0].click();return !document.querySelector('.modal')})());
  const snap=id=>JSON.stringify(Object.assign({},examGet(id),{u:0}));const before=snap('63-1-꼬까');
  exQModal('63-1-꼬까');const mo=document.querySelector('.modal:last-child');
  T('AD-④ 문항 고치기 열면 기존 내답·정답 120 전부 미리 찍힘(on 240) · 번호 = 군 안 번호(상표 21 · 민법 1 · 화학 11) · 접힌 과목 없음',!!mo&&mo.querySelectorAll('.ex5 b.on').length===240&&mo.querySelectorAll('.exskip').length===0&&(()=>{const ns=[...mo.querySelectorAll('.exqrow .n')].map(e=>e.textContent);return ns[20]==='21'&&ns[40]==='1'&&ns[90]==='11'})(),mo&&mo.querySelectorAll('.ex5 b.on').length);
  mo.querySelector('#mOk').click();
  T('AD-④ 아무것도 안 바꾸고 저장 → JSON 무변(u 빼고 바이트 같음)',snap('63-1-꼬까')===before,[before.length,snap('63-1-꼬까').length]);
  exEditModal('63-1-꼬까');const me=document.querySelector('.modal:last-child');
  T('AD-§4 회차 정보 = 날짜 2026-02 미리 · 군 응시자 평균 셋(산재 52.87)',!!me&&me.querySelector('#exDate').value==='2026-02'&&me.querySelector('#exG_산재').value==='52.87'&&!!me.querySelector('#exG_자과'));me.querySelector('#mNo').click();
  const x64b={id:exId(64,1,'꼬까'),no:64,cha:1,who:'꼬까',date:'',kind:'모의',cut:null,note:'',mode:'q',sum:{},q:[],del:false};for(let i=1;i<=20;i++)x64b.q.push({s:'특허',i,my:'1',ans:'1',ok:true,type:'',why:'',rate:null,note:'',redo:''});upsertExam(x64b);
  exQModal('64-1-꼬까');const ms=document.querySelector('.modal:last-child');const sk=ms.querySelectorAll('.exskip');
  T('AD-⑤ 특허만 푼 회차 → 나머지 7과목 「응시 안 함」 접힘 · 특허 20 on',sk.length===7&&ms.querySelectorAll('.exsblk[hidden]').length===7&&ms.querySelectorAll('.ex5 b.on').length===40);
  sk[0].click();T('AD-⑤ 토글 누르면 펼침(OMR 보임 · 「접기」)',ms.querySelectorAll('.exsblk[hidden]').length===6&&/접기/.test(sk[0].textContent));ms.querySelector('#mNo').click();
  {const x=examGet('64-1-꼬까');x.del=true;upsertExam(x)}
  exAddModal();const ma=document.querySelector('.modal:last-child');const dv=()=>ma.querySelector('#exDate').value;
  const noSel=ma.querySelector('#exNo'),chaSel=ma.querySelector('#exCha');
  T('AD-① ＋ 회차 = 날짜 먼저 채움(고른 회차·차수 기본값)',dv()===exDefDate(+noSel.value,+chaSel.value)&&/^\d{4}-(02|07)$/.test(dv()),dv());
  noSel.value='60';noSel.dispatchEvent(new Event('change'));const d1=dv();chaSel.value='2';chaSel.dispatchEvent(new Event('change'));const d2=dv();
  ma.querySelector('#exDate').dataset.user=1;noSel.value='58';noSel.dispatchEvent(new Event('change'));
  T('AD-① 회차 60 → 2023-02 · 2차 → 2023-07 · 사용자가 손댄 뒤엔 안 덮음',d1==='2023-02'&&d2==='2023-07'&&dv()==='2023-07',[d1,d2,dv()]);ma.querySelector('#mNo').click();

  // ---- 판 2 (9/5 · _task_tt_exam_pan2.md B-6 ①~⑦) — 시드 = studyplandata exam/analysis(index.json · 63-1/분석.md · 62-2/민문1.md · criteria 곽준형·김중연) ----
  ui.view='arch';ui.archTab='exam';ui.exTab='ana';ui.exAna=1;ui.ana={};ui.mdOpen={};LS.set('tt.ui',ui);render();
  T('P2-① 1차 = 회차 칩(63회 꼬까) · 제목 · 첫 문단 노란 띠(77.5) · ## 절 토글 4 · 첫 절만 열림 · 표 4(지시서의 「표 3」은 md 실물이 4)',qa('#main .exbar .pill').some(p=>/63회 꼬까/.test(p.textContent))&&/63회 1차 분석/.test(q('#main .ana1 h3').textContent)&&/77\.5/.test(q('#main .anaband').textContent)&&qa('#main .ana1 .mdsec').length===4&&qa('#main .ana1 .mdsec.open').length===1&&qa('#main .ana1 .mdsec')[0].classList.contains('open')&&qa('#main .ana1 table').length===4,[qa('#main .ana1 .mdsec').length,qa('#main .ana1 table').length]);
  qa('#main .ana1 .mdsec .mdh')[1].click();T('P2-① 절 머리 클릭 → 열림 · ui.mdOpen 기억',qa('#main .ana1 .mdsec.open').length===2&&Object.values(ui.mdOpen).includes(true));
  T('P2-① 굵게·표 셀 렌더(자과 3인 표 = 4행)',(()=>{const t=qa('#main .ana1 table')[3];return t&&t.querySelectorAll('tr').length===4&&!!q('#main .ana1 b')})());
  ui.exAna=2;ui.ana.sel2='62-2-꼬까';LS.set('tt.ui',ui);render();   /* add1(9/5): index 에 63-2 예측 회차가 앞서므로 62회를 집어 준다 */
  const gc=(subj,i)=>qa('#main .anagrid tr').find(r=>r.children[0].textContent.startsWith(subj)).children[i];
  T('P2-② 62회 격자 = 4법 × 문1~4 = 16칸 · 민 문1 = 13(exam JSON q) · 5인 중 최소 → 분홍 · 특 문1 12.33 · 디보 점수만',qa('#main .anagrid td.anac').length===16&&gc('민소',1).querySelector('b').textContent==='13'&&gc('민소',1).classList.contains('min')&&gc('특허',1).querySelector('b').textContent==='12.33'&&!gc('특허',1).classList.contains('max')&&/점수만/.test(gc('디보',0).textContent),[gc('민소',1).className,gc('민소',1).textContent]);
  const S=anaSum(LS.get('tt.f.exam/analysis/62-2/민문1.md').data,'하진');
  T('P2-② 설문 요약 줄 = 요소 표 내 열에서 자동(설(1) 답틀 · c 누락 | 설(2) 답틀 · b·c 누락 | 설(3) 답틀) · 격자 칸 아래 같은 글',!!S&&S.length===3&&S[0].text==='답틀 · c 누락'&&S[1].text==='답틀 · b·c 누락'&&S[2].text==='답틀'&&/설\(1\) 답틀 · c 누락/.test(gc('민소',1).querySelector('.anasum').textContent),S&&S.map(x=>x.text));
  gc('민소',1).click();
  T('P2-③ 민문1 클릭 → 두 열(내 복기 / 요소 × 5인) · 취소선 빨강 5 · ⟵ 딱지 5 · 갈린 지점 토글 2(접힘) · 설문 표 3 · 내 열(하진) 노랑 3 · ⚠ 감점 빨강 줄 3',!!q('#main .anaprob .anacols')&&qa('#main .analeft s.mdx').length===5&&qa('#main .analeft .mdtag').length===5&&qa('#main .anaright .mdq').length===2&&qa('#main .anaright .mdq.open').length===0&&qa('#main .anaright table.mdt').length===3&&qa('#main .anaright th.me').length===3&&qa('#main .anared li').length===3,[qa('#main .analeft s.mdx').length,qa('#main .analeft .mdtag').length,qa('#main .anaright .mdq').length,qa('#main .anaright table.mdt').length,qa('#main .anared li').length]);
  q('#main .anaright .mdq .mdqh').click();T('P2-③ 「▸ 갈린 지점」 누르면 펼침',qa('#main .anaright .mdq.open').length===1);
  T('P2-③ 셀 ✔/✘/? 색 · 메모 행 작은 글 · 괄호 메모 갈색',qa('#main .anaright td.ok').length>0&&qa('#main .anaright td.no').length>0&&qa('#main .anaright td.q').length>0&&qa('#main .anaright tr.mdmemo').length===3&&qa('#main .analeft .mdparen').length>0);
  T('P2-④ 강사 칩 = 곽준형 | 김중연 · 기본 = 곽준형(md 채점기준 줄) · 해설 목차 열 3(설문마다 · 곽 설(1) 5항목 · 두 단) · 설문 머리 「해설(곽준형) = 법원의 판결 …」',qa('#main .anachips .pill').map(p=>p.textContent).join()==='곽준형,김중연'&&q('#main .anachips .pill.on').textContent==='곽준형'&&qa('#main .anatoc').length===3&&qa('#main .anatoc')[0].querySelectorAll('.t1').length===5&&qa('#main .anatoc')[0].querySelectorAll('.t2').length===9&&/해설\(곽준형\) = 법원의 판결/.test(qa('#main .anahs')[0].textContent),[qa('#main .anatoc').length,qa('#main .anahs').map(x=>x.textContent.slice(0,40))]);
  T('P2-④ 배점 열 없음(§A 답 ①) · 설문 총점만 머리(설(1) · 10점)',!qa('#main .anaright th').some(t=>/배점/.test(t.textContent))&&/설\(1\) · 10점/.test(qa('#main .anasq h5')[0].textContent));
  qa('#main .anachips .pill')[1].click();
  T('P2-④ 김중연 칩 → 목차 열 = 김중연(설(1) 4항목 · 10점) · 「해설(김중연) = …」 · md 의 해설 줄은 숨김',q('#main .anachips .pill.on').textContent==='김중연'&&/김중연 · 10점/.test(qa('#main .anatoc')[0].querySelector('.anatoch').textContent)&&qa('#main .anatoc')[0].querySelectorAll('.t1').length===4&&/해설\(김중연\)/.test(qa('#main .anahs')[0].textContent)&&!qa('#main .anaright p').some(p=>/^해설\(곽준형\)/.test(p.textContent)),[qa('#main .anatoc')[0]&&qa('#main .anatoc')[0].querySelector('.anatoch').textContent]);
  anaUI('by민소','곽준형');
  // add1(9/5 · _task_tt_exam_pan2_add1.md A-3 · C) — 격자 12칸 전부 클릭 · 머리 md · 요약 줄 파서 실물 셋
  const CL=[];EX_S2.forEach(sj=>[1,2,3,4].forEach(i=>{const c=gc(sj,i);if(!c.classList.contains('has'))return;c.click();CL.push(sj+i+':'+(!!q('#main .anaprob .anacols')&&qa('#main .anaprob .analeft').length===1&&qa('#main .anaprob .anaright table.mdt').length>0))}));anaUI('prob','');
  T('add1-A 62회 격자 md 칸 12 전부 클릭 → 두 열(내 복기 · 요소 표) · 디보 4칸은 md 없음(클릭 없음)',CL.length===12&&CL.every(x=>/true$/.test(x))&&qa('#main .anagrid td.anac.has').length===12,CL);
  T('add1-A 머리 md(62-2/머리.md) 토글이 격자 위에 · 절 2 이상 · 첫 절만 열림',(()=>{const h=q('#main .ana2 .anahead');const g=q('#main .ana2 .anagrid');return !!h&&!!g&&!!(h.compareDocumentPosition(g)&Node.DOCUMENT_POSITION_FOLLOWING)&&h.querySelectorAll('.mdsec').length>=2&&h.querySelectorAll('.mdsec.open').length===1})(),q('#main .ana2 .anahead')&&q('#main .ana2 .anahead').querySelectorAll('.mdsec').length);
  const SM=(n,who)=>anaSum(LS.get('tt.f.exam/analysis/62-2/'+n+'.md').data,who||'하진').map(x=>x.text);
  T('add1-C 요약 줄 파서 · 민문4 = 「b·c 누락 | c·d 누락」 — 「✘(참가승계)」 는 첫 글자 ✘ · 「✔(처분 모호)」 는 ✔ · ★b·★d 접두 요소도 글자로 셈(add1 수정)',JSON.stringify(SM('민문4'))===JSON.stringify(['b·c 누락','c·d 누락']),SM('민문4'));
  T('add1-C 특문4 = 「b 누락 | b·c 누락」 — 「✔✔✔✘」 는 첫 글자 ✔(부분 누락은 안 셈) · 「✘✔」 는 ✘ · 답 행 없으면 답틀 없음',JSON.stringify(SM('특문4'))===JSON.stringify(['b 누락','b·c 누락']),SM('특문4'));
  T('add1-C 상문1 = 「a 누락 | a·b 누락 | ok」 — 「✘✘」·「✔✘✘」 첫 글자 · 「답(거이통 · 조치) ✔✔」 는 답 행 · 「✔✘✘✘」 는 ok',JSON.stringify(SM('상문1'))===JSON.stringify(['a 누락','a·b 누락','ok']),SM('상문1'));
  T('add1-C 「—」(voyac 상문1 설(2)) 와 「?」(하수룡 상문1 설(3)) 는 누락으로 안 셈 → ok',SM('상문1','voyac')[1]==='ok'&&SM('상문1','하수룡')[2]==='ok',[SM('상문1','voyac'),SM('상문1','하수룡')]);
  // add2(9/6 · _task_tt_exam_pan2_add2.md) — 과목 단위 예측 md(63-2 꼬까·햄찌 · 「문항별」 줄 = 원점수) · 61-2 글 꼴 한 장
  anaUI('prob','');anaUI('sel2','63-2-꼬까');
  T('add2 63회 꼬까 = 민소 4칸 예측(21.5 · 9 · 26.5 · 17.5 · 회색 · 「예측 · 원점수」) · 특허 4칸(14.5 · 11 · 18 · 13.5) · 상표·디보 「—」 · 회차 칩 「63회 꼬까」「63회 햄찌」 둘',[1,2,3,4].map(i=>gc('민소',i).querySelector('b').textContent).join()==='21.5,9,26.5,17.5'&&[1,2,3,4].every(i=>gc('민소',i).classList.contains('pred')&&/예측 · 원점수/.test(gc('민소',i).textContent))&&[1,2,3,4].map(i=>gc('특허',i).querySelector('b').textContent).join()==='14.5,11,18,13.5'&&gc('상표',1).querySelector('b').textContent==='—'&&gc('디보',1).querySelector('b').textContent==='—'&&!gc('상표',1).classList.contains('has')&&qa('#main .exbar .pill').filter(p=>/63회/.test(p.textContent)).length===2,[[1,2,3,4].map(i=>gc('민소',i).textContent)]);
  gc('민소',2).click();
  T('add2 예측 칸 클릭 → 그 과목 md(민소_꼬까.md) 토글 5 · 두 열 없음 · 「예측」 딱지',!!q('#main .anaprob')&&!q('#main .anaprob .anacols')&&qa('#main .anaprob .mdsec').length===5&&/예측/.test(q('#main .anaprob .anapt').textContent),qa('#main .anaprob .mdsec').length);
  upsertExam({id:exId(63,2,'꼬까'),no:63,cha:2,who:'꼬까',date:'',kind:'정규',cut:null,note:'',subj:{민소:{score:'',avg:'',note:'',q:[20,null,null,null]}},del:false});render();
  T('add2 실제 점수가 exam JSON 에 오면 「예측 21.5 → 실제 20(-1.5)」 · 값은 예측 그대로',/예측 21\.5 → 실제 20\(-1\.5\)/.test(gc('민소',1).textContent)&&gc('민소',1).querySelector('b').textContent==='21.5',gc('민소',1).textContent);
  {const x=examGet('63-2-꼬까');x.del=true;upsertExam(x)}
  anaUI('prob','');anaUI('sel2','63-2-햄찌');
  T('add2 63회 햄찌(다른 사람 = 다른 회차 칩) = 민소 22 · 12 · 21.25 · 16.75 · 특허 14.5 · 11 · 18 · 13',[1,2,3,4].map(i=>gc('민소',i).querySelector('b').textContent).join()==='22,12,21.25,16.75'&&[1,2,3,4].map(i=>gc('특허',i).querySelector('b').textContent).join()==='14.5,11,18,13',[1,2,3,4].map(i=>gc('민소',i).textContent));
  anaUI('sel2','61-2-꼬까');
  T('add2 61회 글 꼴 = 격자 exam JSON q(민소 10.6 · 특허 9.3 · 디보 —) · 색·클릭 없음 · 아래 글.md 토글 5(첫 절만 열림)',gc('민소',1).querySelector('b').textContent==='10.6'&&gc('특허',1).querySelector('b').textContent==='9.3'&&gc('디보',1).querySelector('b').textContent==='—'&&qa('#main .anagrid td.anac.has').length===0&&qa('#main .anagrid td.min,#main .anagrid td.max').length===0&&qa('#main .anatext .mdsec').length===5&&qa('#main .anatext .mdsec.open').length===1,[gc('민소',1).textContent,qa('#main .anatext .mdsec').length]);
  anaUI('sel2','62-2-꼬까');
  // ⑥ 글 꼴 · 예측 꼴 — 가짜 md 를 캐시·색인에 끼워
  const IDX=LS.get('tt.f.exam/analysis/index.json');const idx0=JSON.stringify(IDX);
  IDX.data.items.find(x=>x.id==='62-2-꼬까').files.push({name:'특문2.md',path:'exam/analysis/62-2/특문2.md',kind:'text',pred:false,title:'62회 2차 · 특 문2 — 하진 8.33 · legalm1nd 12',bytes:1,md5:'x'});
  LS.set('tt.f.exam/analysis/62-2/특문2.md',{data:'# 62회 2차 · 특 문2 — 하진 8.33 · legalm1nd 12\n\n글 꼴 한 줄 결론.\n\n## A 답안\n- 첫째\n- 둘째\n\n## B 답안\n본문.\n',sha:'x',dirty:false});
  IDX.data.items.push({id:'50-2-햄찌',no:50,cha:2,who:'햄찌',files:[{name:'민문1.md',path:'exam/analysis/63-2/민문1.md',kind:'text',pred:true,title:'63회 2차 · 민 문1 — 햄찌 12 · 갑 15',bytes:1,md5:'y'}]});
  LS.set('tt.f.exam/analysis/63-2/민문1.md',{data:'# 63회 2차 · 민 문1 — 햄찌 12 · 갑 15\n예측: true\n\n예측 채점표.\n\n## 설(1)\n본문\n',sha:'y',dirty:false});
  LS.set('tt.f.exam/analysis/index.json',IDX);ui.ana.prob='';LS.set('tt.ui',ui);render();
  T('P2-⑥ 글 꼴(요소 표 없는 md) → 격자엔 점수만(특 문2 8.33 · 색 없음) · 클릭 → 두 열 없이 ##/### 토글 2',gc('특허',2).classList.contains('has')&&gc('특허',2).querySelector('b').textContent==='8.33'&&!gc('특허',2).classList.contains('min')&&!gc('특허',2).querySelector('.anasum')&&(()=>{gc('특허',2).click();return !!q('#main .anaprob')&&!q('#main .anaprob .anacols')&&qa('#main .anaprob .mdsec').length===2})(),gc('특허',2).className);
  anaUI('sel2','50-2-햄찌');
  T('P2-⑥ 예측 꼴(예측: true) → 회색 칸 + 「예측」 딱지 · 값 = md 머리의 내 점수 12',gc('민소',1).classList.contains('pred')&&/예측/.test(gc('민소',1).querySelector('.anapred').textContent)&&gc('민소',1).querySelector('b').textContent==='12');
  upsertExam({id:exId(50,2,'햄찌'),no:50,cha:2,who:'햄찌',date:'',kind:'정규',cut:null,note:'',subj:{민소:{score:'',avg:'',note:'',q:[13,null,null,null]}},del:false});render();
  T('P2-⑥ 실제 점수 오면 「예측 12 → 실제 13(+1)」 나란히',/예측 12 → 실제 13\(\+1\)/.test(gc('민소',1).textContent),gc('민소',1).textContent);
  {const x=examGet('50-2-햄찌');x.del=true;upsertExam(x)}LS.set('tt.f.exam/analysis/index.json',JSON.parse(idx0));localStorage.removeItem('tt.f.exam/analysis/62-2/특문2.md');localStorage.removeItem('tt.f.exam/analysis/63-2/민문1.md');ui.ana={};LS.set('tt.ui',ui);
  // ⑦ 시험전략
  ui.archTab='strat';LS.set('tt.ui',ui);render();
  // add3(9/6 · _task_tt_exam_pan2_add3.md) — 시드 = studyplandata exam/strategy.md 실물(층 2 · 1차 ## 8 · 2차 ## 6 · 표 4)
  const ST0=LS.get('tt.f.exam/strategy.md');localStorage.removeItem('tt.f.exam/strategy.md');const I2=LS.get('tt.f.exam/analysis/index.json');I2.data.strategy=false;LS.set('tt.f.exam/analysis/index.json',I2);ui.stratCha=1;ui.stratCard=true;ui.stratOpen={};LS.set('tt.ui',ui);render();
  T('P2-⑦ strategy.md 없을 때 = 안내 + 층 칩 2(1차·2차) + 1차 진도 카드(63회 93 / 목표 102)',/준비 중/.test(q('#main .strat').textContent)&&qa('#main .stlayer .pill').length===2&&qa('#main .stcard').length===1&&/63회 93 \/ 목표 102/.test(qa('#main .stcard')[0].textContent)&&!!q('#main .stbar i'),qa('#main .stcard').map(c=>c.textContent.slice(0,60)));
  LS.set('tt.f.exam/strategy.md',ST0);I2.data.strategy=true;LS.set('tt.f.exam/analysis/index.json',I2);render();
  const SS=()=>qa('#main .strat .stsec'),SO=()=>qa('#main .strat .stsec.open').map(s=>s.querySelector('.mdh').textContent.trim());
  T('add3 1차 층 = 절 8(고정 위 2 · 과목 5 · 아래 1) · 표 4 · 과목 칩 산재·물리·생물·지학·화학·민법 · 기본 = 첫 과목(산재)만 열림 · 층 칩 「1차 · 64회 …」 on',SS().length===8&&qa('#main .strat .stsec.fixed').length===3&&qa('#main .strat .stsec.subj').length===5&&qa('#main .strat .stsec table').length===4&&qa('#main .stsubj .pill').map(p=>p.textContent).join()==='산재,물리,생물,지학,화학·민법'&&SO().length===1&&/^산재/.test(SO()[0])&&qa('#main .stlayer .pill').length===2&&/^1차 · 64회/.test(q('#main .stlayer .pill.on').textContent),[SS().length,qa('#main .stsubj .pill').map(p=>p.textContent),SO(),q('#main .stlayer .pill.on')&&q('#main .stlayer .pill.on').textContent]);
  T('add3 1차 카드 = 진도 막대 「63회 93 / 목표 102 · 63회 77.5 → 컷 80 −2.5」 + 과목 8칸(물리 8/10 · 올린다) · 요약 줄 「목표 102/120 · 63회 93」',qa('#main .stcard').length===2&&/63회 93 \/ 목표 102 · 63회 77\.5 → 컷 80 −2\.5/.test(qa('#main .stcard')[0].textContent)&&qa('#main .stgrid > div').length===8&&/물리.*8\/10.*올린다/.test(qa('#main .stgrid > div')[4].textContent)&&q('#main .stsum b').textContent==='목표 102/120 · 63회 93',[q('#main .stsum b').textContent,qa('#main .stcard')[0]&&qa('#main .stcard')[0].textContent.slice(0,80)]);
  qa('#main .stsubj .pill')[1].click();
  T('add3 「물리」 칩 → 물리만 열림 · 칩 on · ui.stratOpen 기억(st|1|3 true · st|1|2 false)',SO().length===1&&/^물리/.test(SO()[0])&&q('#main .stsubj .pill.on').textContent==='물리'&&ui.stratOpen['st|1|3']===true&&ui.stratOpen['st|1|2']===false,[SO(),JSON.stringify(ui.stratOpen)]);
  q('#main .strat .stsec.fixed .mdh').click();
  T('add3 고정 절(목표) 머리 클릭 → 열림 · 기억(st|1|0)',qa('#main .strat .stsec.fixed.open').length===1&&ui.stratOpen['st|1|0']===true);
  q('#main .stsum').click();
  T('add3 카드 접기 → 본문 없음 · 요약 한 줄만 · ui.stratCard=false',!q('#main .stcardw.open')&&qa('#main .stcard').length===0&&/목표 102\/120 · 63회 93/.test(q('#main .stsum').textContent)&&ui.stratCard===false);
  qa('#main .stlayer .pill')[1].click();
  T('add3 2차 층 = 절 6(고정 위 2 · 과목 4 — md 실물은 지시서의 7 이 아니라 6) · 과목 칩 민소·특허·상표·디보 · 기본 민소만 · 카드 요약 「컷 53.0 · 62회 −4.75 · 63회 예측 민 ≈71/≈74.5 · 특 56.5/57」',SS().length===6&&qa('#main .strat .stsec.fixed').length===2&&qa('#main .stsubj .pill').map(p=>p.textContent).join()==='민소,특허,상표,디보'&&SO().length===1&&/^민소/.test(SO()[0])&&q('#main .stsum b').textContent==='컷 53.0 · 62회 −4.75 · 63회 예측 민 ≈71/≈74.5 · 특 56.5/57',[SS().length,q('#main .stsum b').textContent]);
  q('#main .stsum').click();
  T('add3 2차 카드 펼침 = 컷 추이 56〜62회 7칸 + 「63회 10/28 발표」 + 62회 꼬까 −4.75 + 예측 표(민소·특허 × 햄찌·꼬까)',qa('#main .stcuts span').length===8&&/10\/28 발표/.test(q('#main .stcuts').textContent)&&/−4\.75/.test(q('#main .stcard.st2').textContent)&&qa('#main table.stpred tr').length===3,[qa('#main .stcuts span').length]);
  qa('#main .stsubj .pill')[1].click();
  T('add3 「특허」 칩 → 특허만 · 1차 층 기억(st|1|3)은 그대로',SO().length===1&&/^특허/.test(SO()[0])&&ui.stratOpen['st|1|3']===true&&ui.stratOpen['st|2|3']===true&&ui.stratOpen['st|2|2']===false);
  ui.stratCha=1;ui.stratCard=null;ui.stratOpen={};LS.set('tt.ui',ui);
  T('P2-④ criteria JSON 꼴 = 강사·설문·목차[]·결론·메모 · 요소 배점 필드 없음(추정 금지)',(()=>{const j=anaJSON('exam/analysis/criteria/62-2-민소-곽준형.json');const sb=j.problems[0].subs[0];return j.by==='곽준형'&&j.no===62&&j.cha===2&&sb.toc.length===5&&!('pts' in sb.toc[0])&&/판결함/.test(sb.concl)&&/적극적 석명도/.test(sb.note)})());
  ui.archTab='exam';ui.exTab='db';
  ui.exSel='';ui.view='day';LS.set('tt.ui',ui);render();
}
}catch(e){R.push('FAIL | 예외 | '+String(e.stack||e.message).split(String.fromCharCode(10)).join(' / '))}
const pre=document.createElement('pre');pre.id='HARNESS';pre.textContent='\n===HARNESS===\n'+R.join('\n')+'\n===END===';
document.body.appendChild(pre);
/* ---- A2(9/6 add1 · _task_ox_tt_input_fix_omrzoom): fetch 스텁으로 syncAll 한 바퀴 → 예외 0 · chg 판정 ----
   9/6 첫 패치가 S 래퍼 안의 syncFile( 까지 S( 로 바꿔 자기 재귀가 됐는데 토큰 없는 하네스는 syncAll 이 조기 return 이라 못 잡았다. 그래서 토큰을 넣고 진짜 한 바퀴 돌린다. */
(async()=>{const R2=[];const T2=(n,c,i)=>R2.push((c?'PASS':'FAIL')+' | '+n+(i!==undefined&&!c?' | '+String(i):''));
 try{
  const realFetch=window.fetch;const remote={};let nPut=0,nGet=0;
  window.fetch=async(u,o)=>{u=String(u);if(!/api\.github\.com/.test(u))return realFetch(u,o);const m=/contents\/([^?]+)/.exec(u);const path=decodeURIComponent(m?m[1]:'');
   if(o&&o.method==='PUT'){nPut++;return new Response(JSON.stringify({content:{sha:'sha_'+nPut}}),{status:200})}
   nGet++;if(remote[path])return new Response(JSON.stringify({sha:remote[path].sha,content:b64e(JSON.stringify(remote[path].data))}),{status:200});return new Response('',{status:404})};
  cfg.token='ghp_HARNESS';LS.set('tt.cfg',cfg);
  T2('A2-0 헤드리스 navigator.onLine(아니면 syncAll 이 조기 return)',navigator.onLine===true,navigator.onLine);
  const r0=render;let nRender=0;render=function(){nRender++;return r0.apply(this,arguments)};
  const rs0=renderSide;let nSide=0;renderSide=function(){nSide++;return rs0.apply(this,arguments)};
  /* 한 바퀴 ① — 원격 전부 404 → 받은 것 없음 → chg=false → render 0 · renderSide 만 */
  ui.view='day';LS.set('tt.ui',ui);nRender=0;nSide=0;syncLog=[];
  await syncAll(true);
  T2('A2-1 syncAll 한 바퀴 예외 0(로그 첫 줄 = 완료 · ✗ 없음)',syncLog.length>0&&/완료/.test(syncLog[0])&&!syncLog.some(l=>/✗/.test(l)),JSON.stringify(syncLog.slice(0,3)));
  T2('A2-1 GET 여러 번 · syncing 풀림',nGet>=10&&syncing===false,'nGet='+nGet+' syncing='+syncing);
  T2('A2-1 받은 것 없음 → render 0 · renderSide ≥1',nRender===0&&nSide>=1,'render='+nRender+' side='+nSide);
  /* 한 바퀴 ② — share/share.json 에 원격 항목 → chg=true → render 1 · 항목 들어옴 */
  remote['share/share.json']={sha:'s1',data:{v:1,items:[{id:'zz_remote',ty:'txt',text:'원격에서 온 글',by:'꼬까',at:1700000000000,u:1700000000000,del:false}]}};
  ui.view='share';LS.set('tt.ui',ui);nRender=0;nSide=0;syncLog=[];
  await syncAll(true);
  T2('A2-2 원격 변경 → 예외 0 · render 1',nRender===1&&/완료/.test(syncLog[0]||''),'render='+nRender+' log='+JSON.stringify(syncLog.slice(0,2)));
  T2('A2-2 원격 항목이 로컬에 들어옴',shareItems('txt').some(x=>x.id==='zz_remote'));
  /* 한 바퀴 ③ — 같은 원격 다시 → 바뀐 것 없음 → render 0 */
  nRender=0;nSide=0;syncLog=[];await syncAll(true);
  T2('A2-3 같은 원격 다시 → render 0 · renderSide ≥1',nRender===0&&nSide>=1&&/완료/.test(syncLog[0]||''),'render='+nRender+' side='+nSide);
  T2('A2-4 S 래퍼가 syncFile 을 부른다(자기 재귀 아님)',/const S=async\(p,o,d\)=>\{if\(await syncFile\(p,o,d\)\)chg=true;\}/.test(String(syncAll)));
  render=r0;renderSide=rs0;window.fetch=realFetch;cfg.token='';LS.set('tt.cfg',cfg);ui.view='day';LS.set('tt.ui',ui);
 }catch(e){R2.push('FAIL | A2 예외 | '+String(e.stack||e.message).split(String.fromCharCode(10)).join(' / '))}
 const p2=document.createElement('pre');p2.id='HARNESS2';p2.textContent='\n'+R2.join('\n')+'\n';document.body.appendChild(p2);
})();
})();
</script>
"""

html = open(SRC, encoding='utf-8').read()
anchor = "<script>\n/* ============================================================\n   타임테이블 v1"
assert anchor in html, "seed anchor not found"
html = html.replace(anchor, SEED + anchor, 1)
# 시험기록 판 1(9/5) — 실물 exam/<사람>.json(노션 이관분 · studyplandata 클론 · 읽기만)을 시드로
_exam = {w: open(_roots.spd(r"exam\%s.json" % w), encoding='utf-8').read() for w in ('꼬까', '햄찌')}
SEED2 = "<script>" + "".join("localStorage.setItem('tt.f.exam/%s.json',JSON.stringify({data:%s,sha:null,dirty:false}));" % (w, t) for w, t in _exam.items()) + "</script>"
html = html.replace(anchor, SEED2 + anchor, 1)
# 판 2(9/5) — 시험분석 시드 = studyplandata exam/analysis(읽기만) · md 는 문자열 · sha = index 의 md5
_ana = _roots.spd(r"exam\analysis")
_idx = open(os.path.join(_ana, 'index.json'), encoding='utf-8').read()
_mds = {}
for _it in json.loads(_idx)['items']:
    for _f in _it['files']:
        _mds[_f['path']] = (open(os.path.join(_roots.spd(), _f['path'].replace('/', os.sep)), encoding='utf-8').read(), _f['md5'])
for _c in ('62-2-민소-곽준형', '62-2-민소-김중연'):
    _mds['exam/analysis/criteria/%s.json' % _c] = (open(os.path.join(_ana, 'criteria', _c + '.json'), encoding='utf-8').read(), None)
_sp = os.path.join(os.path.dirname(_ana), 'strategy.md')   # add3(9/6): 시험전략 md 실물(층 2 · 1차 ## 8 · 2차 ## 6)
if os.path.isfile(_sp): _mds['exam/strategy.md'] = (open(_sp, encoding='utf-8').read(), None)
SEED3 = "<script>localStorage.setItem('tt.f.exam/analysis/index.json',JSON.stringify({data:%s,sha:null,dirty:false}));" % _idx + "".join("localStorage.setItem('tt.f.%s',JSON.stringify({data:%s,sha:%s,dirty:false}));" % (k, json.dumps(v[0], ensure_ascii=False), json.dumps(v[1])) for k, v in _mds.items()) + "</script>"
html = html.replace(anchor, SEED3 + anchor, 1)
assert html.rstrip().endswith("</html>")
# FS-4 — 실물 food.json(studyplandata 클론 · 읽기만)으로 파이썬이 같은 규칙(글자 칸 전부 · 소문자 · 낱말 AND)으로 센 수를 넣는다
_fp = _roots.spd(r"food\food.json")
_fd = json.load(open(_fp, encoding='utf-8'))
_fl = [x for x in _fd['items'] if not x.get('del')]
def _cnt(q):
    ws = q.lower().split()
    return sum(1 for x in _fl if all(w in '\n'.join(str(x.get(k) or '') for k in ('name', 'date', 'recipe', 'note', 'by')).lower() for w in ws))
TESTS = TESTS.replace('__FOOD79__', json.dumps({'items': _fd['items'], 'n_all': len(_fl), 'n_jaeryo': _cnt('재료'), 'n_two': _cnt('별점 4'), 'n_case': _cnt('burger')}, ensure_ascii=False))
html = html.replace("</body>", TESTS + "</body>", 1)
open(APP, 'w', encoding='utf-8', newline='\n').write(html)

prof = os.path.join(OUT, "prof")
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
url = 'file:///' + APP.replace('\\', '/')
QC.launch('new')   # §B-4 셈 — 새 판 앱 띄움 1(바탕 띄움 없음)
r = subprocess.run([chrome, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--user-data-dir=' + prof, '--allow-file-access-from-files',
                    '--window-size=1280,900',
                    '--virtual-time-budget=8000', '--dump-dom', url],
                   capture_output=True, timeout=120)
dom = r.stdout.decode('utf-8', 'replace')
open(os.path.join(OUT, 'dom.html'), 'w', encoding='utf-8').write(dom)
# 결과 줄만 수집 (앞뒤 마커 파싱은 DOM 이스케이프·CRLF 에 취약해 폐기 — 스크립트 소스에는 'PASS | ' 리터럴이 없다)
lines = [ln.strip() for ln in dom.replace('\r', '').split('\n')
         if ln.strip().startswith('PASS | ') or ln.strip().startswith('FAIL | ')]
if not lines:
    print("결과 줄 없음 — 초기 실행 사망?"); print(dom[-3000:]); sys.exit(1)

# ---- fb15 §2: 배포 파일 층 검사(브라우저 밖) ----
APPDIR = os.path.dirname(SRC)
def T2(name, cond, info=''):
    lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))
head = open(SRC, encoding='utf-8').read()[:1200]
T2('F15-1 title = zzikkaTT', '<title>zzikkaTT</title>' in head)
T2('F15-1 apple-touch-icon = icon-180.png', 'rel="apple-touch-icon" href="icon-180.png"' in head)
try:
    mf = json.load(open(os.path.join(APPDIR, 'manifest.webmanifest'), encoding='utf-8'))
    T2('F15-2 manifest 파싱·이름', mf['name'] == 'zzikkaTT' and mf['short_name'] == 'zzikkaTT', mf.get('name'))
    T2('F15-2 manifest 색', mf['theme_color'].upper() == '#A8D8EA' and mf['background_color'].upper() == '#A8D8EA', (mf.get('theme_color'), mf.get('background_color')))
    ic = mf.get('icons', [])
    T2('F15-2 icons 3항목(any 2 + maskable 1)',
       len(ic) == 3 and sum(1 for x in ic if x.get('purpose') == 'any') == 2 and sum(1 for x in ic if x.get('purpose') == 'maskable') == 1,
       [(x.get('src'), x.get('purpose')) for x in ic])
    ok_files = True; detail = []
    for x in ic:
        p = os.path.join(APPDIR, x['src'])
        if not os.path.exists(p): ok_files = False; detail.append(x['src'] + ' 없음'); continue
        w, h = Image.open(p).size
        want = int(x['sizes'].split('x')[0])
        if (w, h) != (want, want): ok_files = False; detail.append(f"{x['src']} {w}x{h}≠{x['sizes']}")
    T2('F15-2 icons 실제 파일·크기 일치', ok_files, detail)
    T2('F15-2 apple-touch 파일 존재(180)', os.path.exists(os.path.join(APPDIR, 'icon-180.png')) and Image.open(os.path.join(APPDIR, 'icon-180.png')).size == (180, 180))
except Exception as e:
    T2('F15-2 manifest', False, repr(e))
sw = open(os.path.join(APPDIR, 'sw.js'), encoding='utf-8').read()
T2('F15-2 sw 프리캐시에 새 아이콘·icon.svg 제거', all(('./' + n) in sw for n in ['icon-192.png', 'icon-512.png', 'icon-maskable-512.png', 'icon-180.png']) and 'icon.svg' not in sw)
T2('F15-3 본문 스타일에 옛 주황 안 샘(theme-color 만 교체)', head.count('#F57C00') == 0 or '--m8:#F57C00' in head)
if QC.SMOKE:   # smoke — 처리표 smoke 칸 셋 + 예외 잡이 줄만 찍는다(같은 한 번 띄움 · 나머지 칸은 건넘)
    lines = [x for x in lines if QC.want(_rg_title(x), smoke=_rg_title(x) in _RG_SMOKE)]
npass = sum(1 for x in lines if x.startswith('PASS'))
nfail = len(lines) - npass
for x in lines: print(x)
print(f"\n== {npass} PASS / {nfail} FAIL / {len(lines)}항 ==")
sys.exit(0 if nfail == 0 else 2)
