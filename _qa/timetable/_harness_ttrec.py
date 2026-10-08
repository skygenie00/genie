# -*- coding: utf-8 -*-
"""zzikkaTT §C 하니스 — 학습기록을 「저장소에서」 읽는 갈래 (2026-09-01)

`_harness_timetable.py` 는 file:// 로 돌지만 이 하니스는 그러지 못한다 —
물러날 길(IndexedDB `phys535`) 을 진짜로 열어 봐야 하는데 IndexedDB 는
file:// 오리진에서 막히기 때문이다. 그래서 짧게 http 서버를 띄우고
결과를 POST 로 돌려받는다(--dump-dom 은 IndexedDB 를 기다려 주지 않는다).

민법OX 집계는 **진짜 `minbeop/기록.json` 의 `ox_chap_history`** 를 넣어 잰다.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
# --mode gate|regress|smoke (_task_qa_slim2 2026-10-08 · 인자 없으면 gate = 이 판 앞과 같음)
#   regress = 칸 91 = 회귀 84 · data 6 · 관문만 1(P1 = 그 판이 민법 앱을 안 고쳤다는 인도 가드) — 띄움 한 번 · 시드(실물 기록) · 검사 글은 gate 와 같다 · 결과는 원래 %TEMP%\ttrech
#   smoke   = 같은 한 번 띄움에서 「P7 민법OX 를 저장소에서 읽는다」(+ 예외 잡이 줄 「하니스가 터짐」 · 「앱이 시동되지 않음」)만 찍는다
#   N:(마이박스) 크롬 프로필을 TEMP 로 옮기는 까닭 — N: 프로필은 띄움마다 느리다: 9/17 tt 회귀(N: 결과 파일 시각) _harness_timetable 76 초 · tt_race 판마다 76~92 초 /
#     10/6 use_count N: 프로필 --dump-dom 180 초 초과 되풀이 → 사용자 「해」로 TEMP(결정로그 10/6 21:36 · 22:0x) / 프로필이 TEMP 인 민법 dump-dom 하네스는 띄움당 9~14 초
#     · 마이박스가 하네스 프로필 폴더 목록을 못 펼쳐 _qa_sync copy 10 분 멈춤 · 실행기 열쇠 셈 멈춤(결정로그 10/2 · 10/4)
import _qa_common as QC   # noqa: E402 — _task_qa_slim2(10/8) A-1 · 실행 모드 --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같음) · import 때 --mode · --snap-in · --snap-out 을 sys.argv 에서 뗀다
import functools, http.server, json, os, shutil, socketserver, subprocess, sys, threading

GENIE = _roots.genie()
TT = os.path.join(GENIE, 'timetable', 'index.html')
PHYS = os.path.join(GENIE, 'jagwa', 'index.html')   # 9/5 자과 서재 이사
MBREC = _roots.spd(r"minbeop\기록.json")
PHYSREC = _roots.spd(r"phys\기록.json")

OUT = os.path.join(os.environ.get('TEMP', '.'), 'ttrech')
APP = os.path.join(OUT, 'timetable', 'app.html')

SEED = """<script>
window.__err=[];
window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+(e.lineno||0))});
window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
localStorage.clear();
localStorage.setItem('tt.cfg',JSON.stringify({person:'\uaf2c\uae4c',token:'',lastSync:0}));
</script>
"""

TESTS_HEAD = """<script>
window.__OXHIST=__OXHIST__;
window.__OXTAGS=__OXTAGS__;
window.__PHYSST=__PHYSST__;
/* 물리앱의 학습로그 만드는 코드를 **원본에서 그대로 떠 온다**.
   tt 가 낸 글자를 이것과 견주는 것이 P3·P4 의 요점이다 — 내가 다시 쓴 기대값이 아니라
   앱이 실제로 내는 글자와 맞춰야 「똑같이」를 잰 것이 된다. */
window.__PHYSLOG=(function(){
__PHYSSRC__
return {secFmt2:secFmt2, buildText:buildText};
})();
</script>
"""

TESTS = r"""<script>
(function(){
 const R=[]; const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+(c?'':' | '+JSON.stringify(i===undefined?null:i)));
 const __nf=window.fetch.bind(window);
 const wait=ms=>new Promise(r=>setTimeout(r,ms));

 /* ---- 가짜 GitHub : contents/ 만 가로채고 나머지(앱 페이지 등)는 그대로 흘린다 ---- */
 const REPO_F={};
 window.fetch=async function(url,opt){
  opt=opt||{};
  const m=/api\.github\.com\/repos\/[^/]+\/[^/]+\/contents\/([^?]+)/.exec(String(url));
  if(!m)return __nf(url,opt);
  const path=decodeURIComponent(m[1]);
  const f=REPO_F[path];
  if(!f)return{ok:false,status:404,json:async()=>({}),text:async()=>''};
  const acc=(opt.headers||{}).Accept||'';
  if(acc.indexOf('raw')>=0)return{ok:true,status:200,text:async()=>f,json:async()=>JSON.parse(f)};
  return{ok:true,status:200,json:async()=>({sha:'s1',content:btoa(unescape(encodeURIComponent(f)))}),text:async()=>f};
 };

 function openModal(){const m=document.getElementById('recImpM');if(m)m.remove();recImportModal();}
 const pvTxt=()=>document.getElementById('recPv').textContent;

 /* ---- 물러날 길 시험용 : phys535 IndexedDB 를 손으로 만든다 ---- */
 function seedPhysIDB(ST){
  return new Promise((ok,no)=>{
   const r=indexedDB.open('phys535',1);
   r.onupgradeneeded=e=>{const d=e.target.result;
    ['pdf','ink','kv'].forEach(s=>{if(!d.objectStoreNames.contains(s))d.createObjectStore(s)})};
   r.onerror=()=>no(new Error('idb open'));
   r.onsuccess=e=>{const db=e.target.result;
    const t=db.transaction('kv','readwrite').objectStore('kv').put(ST,'status');
    t.onsuccess=()=>{db.close();ok()};t.onerror=()=>{db.close();no(new Error('idb put'))}};
  });
 }

 async function run(){
  try{
   /* ================= C-2 : 민법OX 집계 (진짜 데이터) ================= */
   const g=oxGroup(window.__OXHIST,window.__OXTAGS);
   T('C-2 회차마다 한 행이 난다', g.list.length>0, g.list.length);
   T('C-2 x 가 음수로 새지 않는다', g.list.every(r=>r.x>=0));
   T('C-2 n=total · o=score', g.list.every(r=>r.n>=r.o&&r.o>=0));
   T('C-2 min(분)을 넣지 않는다', g.list.every(r=>!('min' in r)));
   T("C-2 src='remote'", g.list.every(r=>r.src==='remote'));
   T('C-2 app/subj = 민법OX/민법', g.list.every(r=>r.app==='민법OX'&&r.subj==='민법'));
   T('C-2 날짜가 ISO 로 풀렸다', g.list.every(r=>/^\d{4}-\d{2}-\d{2}$/.test(r.d)),
     g.list.map(r=>r.d).slice(0,4));
   /* 실물에 있는 값 두 개를 콕 집어 */
   const r830=g.list.find(r=>r.d==='2026-08-30');
   T('C-2 8/30 행위능력 = 102문항·정답 90·오답 12·헷갈림 23',
     !!r830&&r830.n===102&&r830.o===90&&r830.q===23&&r830.x===12,
     r830&&[r830.unit,r830.n,r830.o,r830.q,r830.x]);
   T('C-2 x = n-o — 헷갈림을 빼지 않는다(붙여넣기 OX 행과 같은 뜻)',
     g.list.every(r=>r.x===Math.max(0,r.n-r.o)),
     g.list.map(r=>[r.d,r.n,r.o,r.q,r.x]).slice(0,4));
   T('C-2 q 가 오답보다 많은 칸은 값을 안 건드리고 경고만 남긴다',
     g.warn.some(w=>w.indexOf('2026-08-30')===0)&&r830.x===12, g.warn);
   const rq=g.list.find(r=>r.unit==='약점큐');
   T('C-2 ⚡빠른실행 → 약점큐', !!rq, g.list.map(r=>r.unit));
   T('C-2 같은 칸의 회차 2건이 서로 다른 날로 갈린다',
     g.list.filter(r=>r.unit==='약점큐').length===2,
     g.list.filter(r=>r.unit==='약점큐').map(r=>r.d));
   const r804=g.list.find(r=>r.d==='2026-08-04');
   T('C-2 confuse 가 없는 옛 회차도 읽힌다', !!r804&&r804.n===6&&r804.o===5, r804&&[r804.n,r804.o,r804.q]);
   T('C-2 단원 이름이 붙여넣기 갈래와 같은 모양',
     g.list.some(r=>r.unit==='1. 총칙 > 1.1 민법의 법원'), g.list.map(r=>r.unit));
   T('C-2 (미분별) 같은 꼬리표는 살아 있다',
     g.list.some(r=>r.unit==='1. 총칙 > 1.2 신의칙(미분별)'));
   /* 붙여넣기 갈래와 한 벌인지 */
   {/* 같은 회독을 두 길로 넣어 x·q 가 같은 뜻인지 견준다 */
    const pasted=parseRecLog(['[OX 학습로그] 2026-08-30','- 민법총칙 / 2. 자연인 > 2.3 행위능력 (all) : 102문항, 정답 90 · 오답 12 · 헷갈림 23'].join(String.fromCharCode(10))).blocks[0].items[0];
    T('C-2 붙여넣기 갈래와 x·q 가 똑같다',
      pasted.n===r830.n&&pasted.o===r830.o&&pasted.x===r830.x&&pasted.q===r830.q,
      [[pasted.n,pasted.o,pasted.x,pasted.q],[r830.n,r830.o,r830.x,r830.q]]);}
   T('C-2 oxUnitLabel 한 벌 — 붙여넣기도 같은 함수',
     parseRecLog('[OX 학습로그] 2026-08-25\n- 민법총칙 / 1. 총칙 > 1.1 민법의 법원 (all) : 3문항, 정답 2 · 오답 1 · 헷갈림 0')
       .blocks[0].items[0].unit==='1. 총칙 > 1.1 민법의 법원');

   /* ================= C-3 : physGroup 한 벌 ================= */
   const t1=new Date(2026,7,20,3,30).getTime();
   const ST={'10':{h:[{m:'O',t:t1,s:60}]}};
   const a=physGroup(ST,()=>'A'), b=physGroup(ST,()=>'A','remote');
   T('C-3 physGroup 은 한 벌 — src 만 다르다',
     a[0].src==='origin'&&b[0].src==='remote'&&a[0].n===b[0].n&&a[0].d===b[0].d,
     [a[0].src,b[0].src]);
   T('C-3 새벽 4시 경계를 안 건드렸다', a[0].d==='2026-08-19', a[0].d);

   /* ================= C-4 : 모달 문구 ================= */
   openModal();
   const box=document.querySelector('#recImpM .box');
   const html=box.innerHTML, txt=box.textContent;
   T('C-4-2 민법OX 단추가 생겼다', html.indexOf('📕 민법OX 기록 읽기')>=0);
   T('C-4-2 물리535 단추도 그대로', html.indexOf('🔬 물리535 기록 읽기')>=0);
   T('C-4-2 단추는 REC_APPS 에서 자동 생성',
     (html.match(/recAppRead\(/g)||[]).length===REC_APPS.filter(x=>x.remote||x.origin).length,
     (html.match(/recAppRead\(/g)||[]).length);
   T('C-4-1 옛 거짓말이 사라졌다(같은 기기·같은 주소)', txt.indexOf('같은 기기·같은 주소')<0);
   T('C-4-1 옛 거짓말이 사라졌다(로컬 파일)', txt.indexOf('민법OX(로컬 파일)')<0);
   T('C-4-1 새 설명 = 저장소·기기 상관없음·토큰',
     txt.indexOf('저장소에서 읽어')>=0&&txt.indexOf('기기·브라우저 상관없음')>=0&&txt.indexOf('🔑 토큰 필요')>=0);
   T('C-4-3 ⓐ 붙여넣기는 남아 있다', !!document.getElementById('recTx')&&txt.indexOf('ⓐ 붙여넣기')>=0);
   T('C-4-3 ⓑ 가 ⓐ 보다 먼저 온다', html.indexOf('ⓑ 직접 읽기')<html.indexOf('ⓐ 붙여넣기'),
     [html.indexOf('ⓑ 직접 읽기'),html.indexOf('ⓐ 붙여넣기')]);
   T('C-4-3 「평소에는 이걸 써」가 ⓑ 쪽에 있다', txt.indexOf('평소에는 이걸 써')>=0);
   T('C-4-3 ⓐ 는 대비책으로 적혀 있다', txt.indexOf('대비책')>=0);
   /* P11 — 템플릿 리터럴이 새지 않았다 */
   T('P11 모달 글에 ${ 가 0개', txt.indexOf('${')<0);
   T('P11 모달 글에 백틱이 0개', txt.indexOf('`')<0);
   T('P11 recImportModal 여닫이 백틱 수가 짝',
     (recImportModal.toString().match(/`/g)||[]).length%2===0);

   /* ================= P8 : 토큰이 없으면 조용히 실패하지 않는다 ================= */
   cfg.token='';LS.set('tt.cfg',cfg);
   await recAppRead('민법OX');
   T('P8 토큰 없으면 안내를 띄운다(민법)', pvTxt().indexOf('🔑 토큰이 없습니다')>=0, pvTxt());
   T('P8 토큰 없으면 「가져오기」가 잠긴 채', document.getElementById('recGo').disabled===true);
   /* ⓐ 붙여넣기는 토큰 없이도 된다 */
   document.getElementById('recTx').value='[OX 학습로그] 2026-08-25\n- 민법총칙 / 1. 총칙 > 1.1 민법의 법원 (all) : 3문항, 정답 2 · 오답 1 · 헷갈림 0';
   recParse();
   T('P8 ⓐ 붙여넣기는 토큰 없이도 된다',
     document.getElementById('recGo').disabled===false&&pvTxt().indexOf('민법OX')>=0, pvTxt());

   /* ================= C-1 : 저장소 먼저 ================= */
   REPO_F['minbeop/기록.json']=JSON.stringify({v:1,data:{ox_chap_history:window.__OXHIST,ox_q_tags:window.__OXTAGS}});
   REPO_F['phys/기록.json']=JSON.stringify({v:1,data:{status:{'10':{h:[{m:'O',t:t1,s:60}]}}}});
   cfg.token='github_pat_TEST';LS.set('tt.cfg',cfg);
   openModal();
   await recAppRead('민법OX');
   T('P7 민법OX 를 저장소에서 읽는다', pvTxt().indexOf('저장소')>=0&&pvTxt().indexOf('날짜')>=0, pvTxt());
   T('P7 미리보기에 날짜 수와 문항 수가 뜬다', /날짜 \d+일.*\d+문항/.test(pvTxt()), pvTxt());
   T('P7 「가져오기」가 열렸다', document.getElementById('recGo').disabled===false);
   const mbList=recPrev.list.slice();
   recImportGo();
   let f=recFile('꼬까');
   T('P7 records/꼬까.json 에 저장됐다',
     f.data.items.filter(r=>r.app==='민법OX').length===mbList.length,
     f.data.items.filter(r=>r.app==='민법OX').length);
   T('P7 dirty 로 표시돼 push 로 간다', loadF('records/꼬까.json',{}).dirty===true);

   openModal();
   await recAppRead('물리535');
   T('P7 물리535 도 저장소에서 읽는다', pvTxt().indexOf('저장소')>=0, pvTxt());
   recImportGo();
   f=recFile('꼬까');
   T('P7 두 앱 기록이 한 파일에 함께 앉는다',
     f.data.items.some(r=>r.app==='민법OX')&&f.data.items.some(r=>r.app==='물리535'));
   T('P7 저장된 행에 src=remote 가 남는다',
     f.data.items.filter(r=>r.app==='물리535').every(r=>r.src==='remote'));

   /* ================= C-1 : 저장소 실패 → 이 기기로 물러난다 ================= */
   await seedPhysIDB({'77':{h:[{m:'X',t:t1,s:30}]}});
   delete REPO_F['phys/기록.json'];
   openModal();
   await recAppRead('물리535');
   T('C-1 저장소가 없으면 이 기기로 물러난다', pvTxt().indexOf('이 기기')>=0, pvTxt());
   T('C-1 물러난 이유도 같이 적힌다', pvTxt().indexOf('저장소')>=0, pvTxt());
   T('C-1 물러난 뒤에도 가져올 수 있다',
     document.getElementById('recGo').disabled===false&&recPrev.list.some(r=>r.n===1));
   /* 민법은 물러날 길이 없다 */
   delete REPO_F['minbeop/기록.json'];
   openModal();
   await recAppRead('민법OX');
   T('C-1 민법은 물러날 길이 없어 안내로 끝난다',
     pvTxt().indexOf('아직 없어')>=0&&pvTxt().indexOf('붙여넣기')>=0, pvTxt());

   /* ================= reclog §1~§3 : 학습로그와 똑같이 ================= */
   const unitOf=await physUnitMap('../jagwa/index.html');
   const B=new Date(2026,7,20,10,0,0).getTime();          /* 새벽 4시 경계 뒤 */
   const SEEDN=[['17','X',45,0],['21','Q',135,1],['22','X',200,2],['30','O',60,3],['31','O',0,4]];
   const seedST={};
   SEEDN.forEach(([no,m,s,k])=>{seedST[no]={h:[{m,t:B+k*60000,s}]}});
   const D='2026-08-20';

   /* --- P2 items --- */
   const gl=physGroup(seedST,unitOf,'origin');
   T('P2 물리 행에 items 가 담긴다', gl.every(r=>Array.isArray(r.items)&&r.items.length>0),
     gl.map(r=>[r.unit,(r.items||[]).length]));
   const flat=[];gl.forEach(r=>r.items.forEach(it=>flat.push(it)));
   T('P2 낱개가 5건 다 있다', flat.length===5, flat.length);
   T('P2 items 모양 = {no,m,s} (t 는 안 담는다)',
     flat.every(it=>typeof it.no==='string'&&typeof it.m==='string'&&!('t' in it)), flat[0]);
   T('P2 s=0 이면 s 를 생략한다', flat.some(it=>it.no==='31'&&!('s' in it)),
     flat.find(it=>it.no==='31'));
   T('P2 단원 안 차례가 시각순이다',
     gl.every(r=>{const ord=r.items.map(it=>SEEDN.findIndex(z=>z[0]===it.no));
       return ord.every((v,i)=>i===0||ord[i-1]<v)}), gl.map(r=>r.items.map(it=>it.no)));
   const glr=physGroup(seedST,unitOf,'remote');
   T('P2 저장소 갈래도 items 를 담는다(한 벌)',
     JSON.stringify(glr.map(r=>r.items))===JSON.stringify(gl.map(r=>r.items)));
   T('P2 새벽 4시 경계는 그대로', gl.every(r=>r.d===D), gl.map(r=>r.d));

   /* --- P3·P4 : 물리앱이 내는 글자와 견준다 --- */
   const logItems=SEEDN.map(([no,m,s,k])=>({no,m,sec:s,t:B+k*60000,sub:unitOf(no)||'',big:''}));
   const want=__PHYSLOG.buildText({date:D,items:logItems},'').split(String.fromCharCode(10))
     .map(x=>x.trim()).filter(Boolean);
   /* tt 쪽 — 시드를 records 에 넣고 실제 모달을 그린다 */
   LS.del('tt.f.records/꼬까.json');
   upsertRecs(gl);
   const secHtml=recSecHTML('꼬까',D);
   const box2=document.createElement('div');box2.innerHTML=secHtml;document.body.appendChild(box2);
   const got=[...box2.querySelectorAll('.qsub,.qitems,.qsum,.qslow')].map(e=>e.textContent.trim()).filter(Boolean);
   T('P3 물리 칸이 학습로그와 **줄 단위로 같다**',
     JSON.stringify(got)===JSON.stringify(want.slice(1)),
     {tt:got,app:want.slice(1)});
   T('P3 단원 줄 형식', got[0]===want[1], [got[0],want[1]]);
   T('P3 낱개 줄 형식(초 표기까지)', got[1]===want[2], [got[1],want[2]]);
   T('P3 합계 줄 형식', got.some(x=>x.indexOf('합계:')===0)&&got.find(x=>x.indexOf('합계:')===0)===want.find(x=>x.indexOf('합계:')===0),
     [got.find(x=>x.indexOf('합계:')===0),want.find(x=>x.indexOf('합계:')===0)]);
   T('P4 오래 걸림 줄이 앱과 같다',
     got.find(x=>x.indexOf('오래 걸림')===0)===want.find(x=>x.indexOf('오래 걸림')===0),
     [got.find(x=>x.indexOf('오래 걸림')===0),want.find(x=>x.indexOf('오래 걸림')===0)]);
   T('P4 오래 걸림이 실제로 났다(빈 비교가 아니다)',
     !!want.find(x=>x.indexOf('오래 걸림')===0), want);
   box2.remove();

   /* timed < 3 인 날 — 양쪽 다 줄이 없다 */
   const B2=new Date(2026,7,21,10,0,0).getTime(), D2='2026-08-21';
   const seed2={'17':{h:[{m:'X',t:B2,s:300}]},'21':{h:[{m:'O',t:B2+60000,s:400}]}};
   const gl2=physGroup(seed2,unitOf,'origin');
   upsertRecs(gl2);
   const b3=document.createElement('div');b3.innerHTML=recSecHTML('꼬까',D2);document.body.appendChild(b3);
   const li2=SEEDN.slice(0,0).concat([{no:'17',m:'X',sec:300,t:B2,sub:unitOf('17')||'',big:''},
                                      {no:'21',m:'O',sec:400,t:B2+60000,sub:unitOf('21')||'',big:''}]);
   const want2=__PHYSLOG.buildText({date:D2,items:li2},'');
   T('P4 timed<3 이면 앱에도 줄이 없다', want2.indexOf('오래 걸림')<0);
   T('P4 timed<3 이면 tt 에도 줄이 없다', b3.querySelectorAll('.qslow').length===0);
   b3.remove();

   /* --- P6 : items 없는 옛 행 --- */
   const old=gl.map(r=>{const c=Object.assign({},r);delete c.items;c.d='2026-08-22';return c});
   upsertRecs(old);
   const b4=document.createElement('div');b4.innerHTML=recSecHTML('꼬까','2026-08-22');document.body.appendChild(b4);
   T('P6 옛 행 — 낱개 줄을 안 그린다', b4.querySelectorAll('.qitems').length===0);
   T('P6 옛 행 — 오래 걸림 줄도 없다', b4.querySelectorAll('.qslow').length===0);
   T('P6 옛 행 — 단원 줄과 합계 줄은 나온다',
     b4.querySelectorAll('.qsub').length>0&&b4.querySelectorAll('.qsum').length===1);
   b4.remove();

   /* --- P5 : 민법 칸 --- */
   const oxr=oxGroup(window.__OXHIST,window.__OXTAGS).list.filter(r=>r.d==='2026-08-30');
   upsertRecs(oxr);
   const b5=document.createElement('div');b5.innerHTML=recSecHTML('꼬까','2026-08-30');document.body.appendChild(b5);
   const oxLines=[...b5.querySelectorAll('.qsub,.qsum')].map(e=>e.textContent.trim());
   T('P5 민법 단원 줄 = 로그 형식',
     /^- .+ : \d+문항, 정답 \d+ · 오답 \d+ · 헷갈림 \d+$/.test(oxLines[0]), oxLines[0]);
   T('P5 민법 단원 줄에 과목·출처가 붙는다(ulabel)',
     oxLines[0].indexOf('민법총칙 / ')>=0&&oxLines[0].indexOf('(all)')>=0, oxLines[0]);
   T('P5 민법 합계 줄 = 로그 형식',
     /^합계: \d+문항 · 정답 \d+ · 오답 \d+ · 헷갈림 \d+$/.test(oxLines[oxLines.length-1]),
     oxLines[oxLines.length-1]);
   T('P5 민법 칸에 분이 없다', oxLines.every(l=>l.indexOf('분')<0), oxLines);
   T('P5 민법 칸에 낱개 줄이 없다', b5.querySelectorAll('.qitems').length===0);
   T('P5 민법 칸에 오래 걸림 줄이 없다', b5.querySelectorAll('.qslow').length===0);
   b5.remove();

   /* --- 접기 : 기본 펼침 --- */
   const b6=document.createElement('div');b6.innerHTML=recSecHTML('꼬까',D);document.body.appendChild(b6);
   T('§3 접기가 있고 **기본은 펼침**',
     b6.querySelectorAll('details.qapp').length===1&&b6.querySelector('details.qapp').open===true);
   T('§3 앱 줄이 summary 가 됐다(숫자는 그대로)',
     b6.querySelector('summary.qrow').textContent.indexOf('물리535')>=0
     &&b6.querySelector('summary.qrow').textContent.indexOf('문항')>=0,
     b6.querySelector('summary.qrow').textContent.trim());
   b6.remove();
   T('§3 recLineHTML(어제·오늘·내일 한 줄)은 안 건드렸다',
     recLineHTML.toString().indexOf('qitems')<0&&recLineHTML.toString().indexOf('qsum')<0);
   T('§3 「오래 걸림」 식이 물리앱 사본임을 주석에 못 박았다',
     /2606~2613행의 사본/.test(physSlow.toString())
     ||document.documentElement.innerHTML.indexOf('2606~2613행의 사본')>=0);

   /* --- §4 이월 배지 --- */
   T('§4 carryCls — `+N` 은 빨강 갈래', carryCls('+3')==='carry late2', carryCls('+3'));
   T('§4 carryCls — 「→ 오늘」은 파랑 그대로', carryCls('→ 오늘')==='carry', carryCls('→ 오늘'));
   T('§4 carryCls — 빈 값도 안전', carryCls('')==='carry'&&carryCls(null)==='carry');
   const bl=carryBadge({b:{id:'b1'},u:{id:'u1'},late:true,orig:'2026-08-20'});
   const bd=carryBadge({b:{id:'b1'},u:{id:'u1'},dim:true});
   T('§4 carryBadge 밀림 갈래 = carry late2', /class="carry late2"/.test(bl), bl);
   T('§4 carryBadge → 오늘 갈래 = carry (late2 없음)',
     /class="carry"/.test(bd)&&bd.indexOf('late2')<0, bd);
   T('§4 네 자리가 다 carryCls 를 쓴다(literal class="carry" 0건)',
     document.documentElement.innerHTML.indexOf('class="carry"')<0
     ||true /* 렌더된 DOM 에는 실제 클래스가 찍히므로 소스 검사는 파이썬 쪽에서 */);

   /* --- P7 : 실물 기록으로 크기 재기 --- */
   {const uo=await physUnitMap('../jagwa/index.html');
    const rows=physGroup(window.__PHYSST,uo,'remote');
    const withI=JSON.stringify(rows).length;
    const noI=JSON.stringify(rows.map(r=>{const c=Object.assign({},r);delete c.items;return c})).length;
    const cnt=rows.reduce((a,r)=>a+(r.items||[]).length,0);
    T('P7 실물 물리 이력 '+cnt+'건 · items 로 늘어난 바이트 '+(withI-noI)+'B (행 '+rows.length+')', true);
    T('P7 늘어난 뒤에도 1MB 미만', withI<1000000, withI);
    window.__P7=[cnt,rows.length,noI,withI];}

   /* ===== P10 : 콘솔 오류 0 ===== */
   T('P10 잡히지 않은 오류 0건', (window.__err||[]).length===0, window.__err);

  }catch(e){R.push('FAIL | 하니스가 터짐 | '+(e&&e.stack||e))}
  report(R.join('\n'));
 }
 function report(txt){
  try{__nf('/result',{method:'POST',body:txt})}catch(e){}
  const pre=document.createElement('pre');pre.id='RESULT';pre.textContent=txt;document.body.appendChild(pre);
 }
 (function boot(n){
  if(typeof recAppRead==='function'&&typeof oxGroup==='function'&&document.getElementById('side'))return run();
  if(n>400)return report('FAIL | 앱이 시동되지 않음');
  setTimeout(()=>boot(n+1),25);
 })(0);
})();
</script>
"""


_RG_SMOKE = ('P7 민법OX 를 저장소에서 읽는다', '하니스가 터짐', '앱이 시동되지 않음')   # smoke — 처리표 smoke 칸 + 예외 잡이 줄 둘(제목 그대로)


def _rg_title(ln):
    """결과 줄 「PASS | 제목 | 값」의 제목 — smoke 거름(제목 그대로)"""
    p = ln.split(' | ')
    return p[1] if len(p) > 1 else ln


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(os.path.join(OUT, 'timetable'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'jagwa'), exist_ok=True)
    # 물리앱은 physUnitMap 이 진짜로 읽는다 — 사본을 옆에 둔다(../jagwa/index.html · 9/5 이사)
    shutil.copyfile(PHYS, os.path.join(OUT, 'jagwa', 'index.html'))

    rec = json.load(open(MBREC, encoding='utf-8'))
    physrec = json.load(open(PHYSREC, encoding='utf-8'))['data'].get('status', {})
    ps = open(PHYS, encoding='utf-8', newline='').read()
    i = ps.index('function secFmt2')
    j = ps.index('function openPanel')
    physsrc = ps[i:j]
    assert 'function buildText' in physsrc and physsrc.count('`') == 0, 'phys log slice looks wrong'

    head = (TESTS_HEAD
            .replace('__PHYSSRC__', physsrc)
            .replace('__PHYSST__', json.dumps(physrec, ensure_ascii=False))
            .replace('__OXHIST__', json.dumps(rec['data'].get('ox_chap_history', {}), ensure_ascii=False))
            .replace('__OXTAGS__', json.dumps(rec['data'].get('ox_q_tags', {}), ensure_ascii=False)))

    html = open(TT, encoding='utf-8', newline='').read()
    anchor = "<script>\n/* ============================================================\n   타임테이블 v1"
    assert anchor in html, 'seed anchor not found'
    html = html.replace(anchor, SEED + anchor, 1)
    assert html.rstrip().endswith('</html>')
    html = html.replace('</body>', head + TESTS + '</body>', 1)
    open(APP, 'w', encoding='utf-8', newline='').write(html)


def main():
    build()
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
    QC.launch('new')   # §B-4 셈 — 새 판 앱 띄움 1(바탕 띄움 없음)
    p = subprocess.Popen([chrome, '--headless=new', '--disable-gpu', '--no-first-run',
                          '--user-data-dir=' + os.path.join(OUT, 'prof'),
                          '--window-size=1280,900',
                          'http://127.0.0.1:%d/timetable/app.html' % port],
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

    lines = [ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()]
    # ---- 브라우저 밖 검사 (소스 층) ----
    def T2(name, cond, info=''):
        lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))
    tt = open(TT, encoding='utf-8').read()
    T2('§4 소스에 literal class="carry" 가 0건 (네 자리 다 carryCls)',
       tt.count('class="carry"') == 0, tt.count('class="carry"'))
    T2('§4 carryCls 를 부르는 자리가 넷', tt.count('carryCls(') == 4, tt.count('carryCls('))
    T2('§4 .carry.late2 = #c33 (.lateT 와 같은 빨강)', '.carry.late2{color:#c33}' in tt)
    T2('§3 「한쪽을 고치면 다른 쪽도」 주석이 있다', '한쪽을 고치면 다른 쪽도 고쳐야 한다' in tt)
    T2('§3 「정본은 각 앱, tt 는 사본」 주석이 있다', '정본은 각 앱이고 tt 는 사본이다' in tt)
    T2('P11 파일 전체 백틱 수가 짝', tt.count('`') % 2 == 0, tt.count('`'))
    if QC.GATE:   # regress — P1(그 판이 민법 앱을 안 고쳤다는 인도 가드 · 처리표 관문만)은 gate 만
        T2('P1 minbeop/index.html 무접촉(tt 만 고쳤다)', 'minbeop/index.html' not in tt)

    if QC.SMOKE:   # smoke — 처리표 smoke 칸 + 예외 잡이 줄만 찍는다(같은 한 번 띄움 · 나머지 칸은 건넘)
        lines = [x for x in lines if QC.want(_rg_title(x), smoke=_rg_title(x) in _RG_SMOKE)]
    npass = sum(1 for x in lines if x.startswith('PASS'))
    nfail = len(lines) - npass
    for x in lines:
        print(x)
    print('\n== %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
