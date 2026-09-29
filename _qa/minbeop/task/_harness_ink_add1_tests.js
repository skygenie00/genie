window.onload=null;
(function(){
/* _task_ox_ink_add1 §C — main(가상 시계 · 창 1280) · g1(iframe 390·768·1280 안에서 한 폭씩) 두 갈래. 성능(G5·G6)은 _harness_ink_add1_perf.js(실시간). */
const P=__P__;
const R=[];
const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+((i!==undefined&&!c)?' | '+String(i).replace(/\n/g,'⏎').slice(0,500):''));
const say=s=>R.push('INFO | '+String(s).replace(/\n/g,'⏎'));
const V=(k,v)=>R.push('VAL | '+k+' | '+JSON.stringify(v));
const M=(k,v)=>R.push('MEAS | '+k+' | '+JSON.stringify(v));
const J=v=>JSON.stringify(v);
const lsO=k=>{try{return JSON.parse(localStorage.getItem(k)||'{}')||{}}catch(e){return {}}};
const BASE={'ox_uid_migrated':'1','ox_gg_okreset':'1','ox_gg_memo_merged':'{"at":1,"moved":0,"links":0}','ox_gg_logic_merged':'{"at":1,"moved":0,"links":0}','ox_auto_important_v2':'1'};
const resetLS=o=>{ localStorage.clear(); for(const k in BASE) localStorage.setItem(k,BASE[k]); for(const k in (o||{})) localStorage.setItem(k,typeof o[k]==='string'?o[k]:JSON.stringify(o[k])); try{useIdxDrop()}catch(e){} try{mcInvalidate()}catch(e){} };
const loadQuiz=()=>{ quizData.length=0; P.quiz.forEach(q=>quizData.push(JSON.parse(JSON.stringify(q)))); };
const closeAllWins=()=>document.querySelectorAll('.oxwin').forEach(w=>w.remove());
const showHome=()=>{ document.getElementById('home-screen').classList.remove('hide'); document.getElementById('quiz-screen').classList.add('hide'); };
const openQuiz=(ids,subject,chap)=>{
  loadQuiz();
  currentSubject=subject; currentChapterLabel=chap; isExamMode=false; currentPageIndex=0; currentSessionMarks={}; resumePicks={}; currentSessionScore=0; lastGradeResults=null;
  if(typeof chapterSaved!=='undefined') chapterSaved=null;
  currentFilteredData=ids.map(id=>quizData.find(q=>q.id===id));
  document.getElementById('home-screen').classList.add('hide'); document.getElementById('quiz-screen').classList.remove('hide');
  document.getElementById('reopen-grade-bar').classList.add('hide'); document.getElementById('controls-container').classList.remove('hide');
  renderQuizPage();
};
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const until=async(f,n)=>{ for(let i=0;i<(n||100);i++){ try{ if(f()) return true; }catch(e){} await wait(30); } try{ return !!f(); }catch(e){ return false; } };
const CH='1. 총칙 > 1.1 민법의 법원';
const NEW=typeof qpCacheOpen==='function';
const HASINK=typeof qiToggle==='function';
const UNIT=P.quiz.filter(q=>!q.examNo&&q.subChapter==='1.1 민법의 법원').map(q=>q.id);
const ptr=(el,type,x,y,pt,id)=>{ const ev=new PointerEvent(type,{pointerType:pt,pointerId:id,isPrimary:true,bubbles:true,cancelable:true,composed:true,clientX:x,clientY:y,button:0,buttons:type==='pointerup'?0:1}); el.dispatchEvent(ev); return ev; };
const penMode=async on=>{ if(!HASINK) return; if((!cardMarksOn)!==on){ qiToggle(); await wait(150); } };
/* IndexedDB 는 가상 시계를 안 따른다 — 기다리는 동안 걸린 타이머가 없으면 가상 시계가 예산 끝까지 뛰어 크롬이 닫힌다(9/16 main NEW 가 G2 첫 clearInk 에서 멈춘 까닭).
   짧은 타이머를 이어 걸어 진짜 시간이 흐르게 붙잡는다 */
const keep=async p=>{ let done=false, val, err; Promise.resolve(p).then(v=>{done=true;val=v;},e=>{done=true;err=e;}); for(let i=0;i<4000&&!done;i++) await wait(5); if(err) throw err; return val; };
const inkOf=async u=>{ try{ return await keep(dbGet('ink:q:'+u)); }catch(e){ return 'err:'+e.message; } };
const clearInk=async us=>{ if(typeof dbDel!=='function') return; for(const u of us){ try{ await keep(dbDel('ink:q:'+u)); }catch(e){} } };
const paths=u=>{ const s=document.getElementById('ink-'+u); return s?s.querySelectorAll('path[data-j]').length:-1; };
const gI=(k,i,t)=>({k:k,i:i,t:t,ok:null,ts:1789000000000,cs:[]});

/* ── g1 — 이 iframe 폭 하나에서 #qcards 폭·transform ── */
if(P.phase==='g1'){
  const wtag=(location.hash||'#w0').slice(1);
  setTimeout(async function(){
    await wait(2500*(P.order[wtag]||0));
    try{
      resetLS({}); openQuiz(UNIT,'민법총칙',CH); await wait(250);
      const host=document.getElementById('quiz-container'), c=document.getElementById('qcards');
      const hs=getComputedStyle(host), inner=host.clientWidth-(parseFloat(hs.paddingLeft)||0)-(parseFloat(hs.paddingRight)||0);
      const r=c.getBoundingClientRect(), want=Math.min(900,inner);
      M('G1.'+wtag, {vw:innerWidth, inner:+inner.toFixed(2), tf:c.style.transform, w:+r.width.toFixed(2), want:+want.toFixed(2), box:+document.getElementById('q-box-Q9801').getBoundingClientRect().width.toFixed(2)});
      T('G1 '+wtag+' — #qcards style.transform 빈 값 · 보이는 폭 = min(900, 안쪽 폭 '+inner.toFixed(0)+')'+(wtag==='w390'?' ±1px':''), c.style.transform===''&&Math.abs(r.width-want)<=(wtag==='w390'?1:0.5), J({tf:c.style.transform,w:r.width,want}));
    }catch(e){ T('G1 '+wtag+' 시험이 죽었다',false,e.message); }
    R.forEach(x=>console.log('HZR|'+encodeURIComponent(x)));
    console.log('HZR|END:'+wtag);
  },1500);
  return;
}

/* G2 필기 좌표 = px ÷ 그린 폭 · w 저장 · 지금 폭으로 균등 */
const stepLog=(g,n)=>console.log('HZ-STEP '+g+' '+n);
async function G2(){
  if(!NEW){ T('G2 필기 좌표 = 그린 카드 폭(add1)',false,'HEAD'); return; }
  resetLS({}); closeAllWins(); stepLog('G2','clearInk'); await clearInk(['Q9801','Q9802']); QI={};
  stepLog('G2','openQuiz'); openQuiz(UNIT,'민법총칙',CH); await wait(150); stepLog('G2','penMode'); await penMode(true); stepLog('G2','ready');
  const host=document.getElementById('quiz-container');
  const box=document.getElementById('q-box-Q9801'), bw=box.offsetWidth-box.clientWidth;
  document.getElementById('qcards').style.maxWidth='none';          /* 시험만 — 덮개(카드 안쪽) 폭을 900 으로 딱 맞추려고 */
  host.style.width=(900+bw)+'px'; await wait(40); window.scrollTo(0,0); await wait(20);
  const sv=document.getElementById('ink-Q9801'), r=sv.getBoundingClientRect();
  T('G2 준비 — 덮개 폭 900 · viewBox 0 0 1 1000 · slice', Math.abs(r.width-900)<0.01&&sv.getAttribute('viewBox')==='0 0 1 1000'&&sv.getAttribute('preserveAspectRatio')==='xMinYMin slice', r.width+' · '+sv.getAttribute('viewBox'));
  const p=document.querySelector('#q-box-Q9801 p'), pr=p.getBoundingClientRect(), x=pr.left+80, y=pr.top+Math.min(30,pr.height/2);
  stepLog('G2','tap'); ptr(sv,'pointerdown',x,y,'pen',201); ptr(sv,'pointerup',x,y,'pen',201);
  await wait(450); stepLog('G2','inkOf');
  const st=await inkOf('Q9801'), s0=st&&st.s&&st.s[0], eu=(x-r.left)/900, ev=(y-r.top)/900; stepLog('G2','dbPut');
  T('G2 폭 900 에서 펜 톡 → 저장 w:900 · p = (x÷900, y÷900)', !!s0&&st.w===900&&Math.abs(s0.p[0]-eu)<2e-4&&Math.abs(s0.p[1]-ev)<2e-4, J({w:st&&st.w,p:s0&&s0.p,eu,ev}));
  await keep(dbPut('ink:q:Q9801',{w:900,s:[{c:'#16181B',w:2,hl:0,p:[0.5,0.2,0.5,0.2]}]}));
  await keep(dbPut('ink:q:Q9802',{s:[{c:'#16181B',w:2,hl:0,p:[0.5,0.2,0.5,0.2]}]}));
  stepLog('G2','render450'); host.style.width=(450+bw)+'px'; QI={}; renderQuizPage();
  await until(()=>paths('Q9801')===1&&paths('Q9802')===1); stepLog('G2','painted');
  const at=u=>{ const s=document.getElementById('ink-'+u), rr=s.getBoundingClientRect(), pa=s.querySelector('path[data-j="0"]'); if(!pa) return null; const m=pa.getScreenCTM(), pt=s.createSVGPoint(); pt.x=0.5; pt.y=0.2; const q=pt.matrixTransform(m); return {w:+rr.width.toFixed(2),x:+(q.x-rr.left).toFixed(3),y:+(q.y-rr.top).toFixed(3)}; };
  const a1=at('Q9801'), a2=at('Q9802'), s1=await inkOf('Q9801');
  M('G2.at450', {a1,a2,w1:s1&&s1.w,w2mem:QI.Q9802&&QI.Q9802.w});
  T('G2 폭 450 에서 그려지는 자리 = (225,90) · 저장 w:900 그대로', !!a1&&a1.w===450&&Math.abs(a1.x-225)<0.05&&Math.abs(a1.y-90)<0.05&&!!s1&&s1.w===900, J({a1,w:s1&&s1.w}));
  T('G2 옛 값(w 없음)도 같은 자리 (225,90) · 읽을 때 w = 900', !!a2&&a2.w===450&&Math.abs(a2.x-225)<0.05&&Math.abs(a2.y-90)<0.05&&!!QI.Q9802&&QI.Q9802.w===900, J({a2,w:QI.Q9802&&QI.Q9802.w}));
  host.style.width=(700+bw)+'px'; await wait(40);
  const a3=at('Q9801'), pa=document.querySelector('#ink-Q9801 path[data-j="0"]');
  M('G2.at700', a3);
  T('G2 다시 그리지 않고 폭만 700(회전 흉내) → 획이 지금 폭으로 따라간다 (350,140) · 굵기는 non-scaling-stroke', !!a3&&a3.w===700&&Math.abs(a3.x-350)<0.05&&Math.abs(a3.y-140)<0.05&&!!pa&&getComputedStyle(pa).vectorEffect==='non-scaling-stroke', J({a3,ve:pa&&getComputedStyle(pa).vectorEffect}));
  host.style.width=''; await clearInk(['Q9801','Q9802']); QI={};
  await penMode(false); showHome();
}

/* G3 문제풀이 카드 「🔗 판 N」 */
async function G3(){
  resetLS({}); closeAllWins(); openQuiz(UNIT,'민법총칙',CH); await wait(150);
  const qc=document.getElementById('quiz-container'), html=qc.innerHTML;
  const boxes=[...qc.querySelectorAll('.question-box')];
  const want=boxes.filter(b=>samePanrye(quizData.find(q=>q.id===b.id.replace('q-box-',''))).length>0).length;
  const nOld=(html.match(/같은 판례/g)||[]).length, nNew=(html.match(/🔗 판 /g)||[]).length;
  const chips=[...qc.querySelectorAll('button[onclick*="\'same\'"]')].map(b=>b.textContent.trim());
  say('G3 카드 HTML — 「같은 판례」 '+nOld+' · 「🔗 판 」 '+nNew+' · 같은 판례가 있는 문항(이 쪽) '+want+' · 칩 글자 '+J(chips));
  T('G3 문제풀이 카드 HTML 에 「같은 판례」 0 · 「🔗 판 」 = 같은 판례가 있는 문항 수', nOld===0&&nNew===want&&want>0, J({nOld,nNew,want}));
  showHome();
}

/* G4 정리 창 결과 HTML 옛 판과 글자까지(VAL) */
async function G4(){
  resetLS({ox_q_geunge:{Q9801:[gI('g_Q9801_a',1,'첫 근거')],Q9805:[gI('g_Q9805_a',1,'근거 하나')],Q9806:[gI('g_Q9806_a',1,'연결될 근거')]},ox_q_reflinks:{Q9805:{geunge:['Q9806']}},ox_q_links:{Q9805:['Q9806'],Q9807:['Q9805']}});
  loadQuiz(); showHome(); closeAllWins();
  try{ _oxWinZ=12000; _oxWinN=0; }catch(e){}
  openJeongni('민법총칙','1.1');
  const w=document.querySelector('.oxwin[id^="oxwin-jn-"]');
  V('G4.jeongni', w?{head:w.querySelector('.oxwin-head').textContent.replace(/\s+/g,' ').trim(),body:w.querySelector('.oxwin-body').innerHTML}:null);
  T('G4 정리 창이 열린다 · 행 있음(글자 대조는 VAL)', !!w&&w.querySelectorAll('[data-jnrow]').length>0, w?'행 0':'창 없음');
  closeAllWins();
}

/* G5 유제 되짚기 색인 = 옛 yujeBackOf */
async function G5E(){
  loadQuiz();
  if(!NEW){ T('G5 유제 되짚기 색인(렌더 중) = 옛 yujeBackOf',false,'HEAD'); return; }
  const ids=[...new Set(quizData.map(q=>String(q.id)).concat(['q9804',' Q9804 ','Q9999','']))];
  const idx=yujeBackIndex(), bad=[];
  ids.forEach(id=>{ const a=yujeBackOf(id), b=idx.get(String(id).trim().toUpperCase())||[]; if(J(a)!==J(b)) bad.push(id+' '+J(a)+'≠'+J(b)); });
  say('G5 유제 되짚기(렌더 밖 · 옛 코드 길) — Q9804 ← '+J(yujeBackOf('Q9804'))+' · Q9812 ← '+J(yujeBackOf('Q9812'))+' · 같은 id 두 줄(Q9803)은 첫 줄의 유제만');
  T('G5 유제 되짚기 색인 = 옛 yujeBackOf — id '+ids.length+'개 글자 대조(대소문자·자기 자신·겹침·같은 id 두 줄 포함)', bad.length===0&&J(yujeBackOf('Q9804'))===J(['Q9803','Q9810','Q9811','Q9813'])&&J(yujeBackOf('Q9812'))===J(['Q9810']), bad.slice(0,4).join(' / '));
  openQuiz(UNIT,'민법총칙',CH); await wait(100);
  T('G5 렌더가 끝나면 페이지 캐시가 비어 있다(GG_PAGE·LINK_PAGE·REF_PAGE·QTYPE_PAGE·YUJE_PAGE)', GG_PAGE===null&&LINK_PAGE===null&&REF_PAGE===null&&QTYPE_PAGE===null&&YUJE_PAGE===null);
  let thrown=false; const og=window.oxPaint; window.oxPaint=function(){ throw new Error('시험 — 렌더 도중 죽음'); };
  try{ renderQuizPage(); }catch(e){ thrown=true; }
  window.oxPaint=og;
  const leftNow=GG_PAGE!==null; await wait(10);
  T('G5 렌더가 도중에 죽어도 그 일이 끝나면 캐시가 빈다(queueMicrotask)', thrown&&GG_PAGE===null&&LINK_PAGE===null&&YUJE_PAGE===null, J({thrown,leftNow,after:GG_PAGE===null}));
  renderQuizPage(); showHome();
}

/* G7 필기모드 손가락 = 브라우저 몫 · 펜이 닿은 동안만 막음 */
async function G7(){
  if(!NEW){ T('G7 손가락 기본 스크롤(add1)',false,'HEAD'); return; }
  resetLS({}); closeAllWins(); openQuiz(UNIT,'민법총칙',CH); await wait(150); await penMode(true);
  const SE=document.scrollingElement; SE.scrollTop=0; await wait(20);
  const sv=document.getElementById('ink-Q9803'), p=document.querySelector('#q-box-Q9803 p'), pr=p.getBoundingClientRect();
  const x=pr.left+60, y=pr.top+Math.min(30,pr.height/2);
  const e1=ptr(sv,'pointerdown',x,y,'touch',301); const e1m=ptr(sv,'pointermove',x,y-40,'touch',301); ptr(sv,'pointerup',x,y-40,'touch',301);
  T('G7 필기모드 · 펜 없음 — 카드 위 손가락 pointerdown·pointermove defaultPrevented false(브라우저 스크롤)', e1.defaultPrevented===false&&e1m.defaultPrevented===false, J([e1.defaultPrevented,e1m.defaultPrevented]));
  ptr(sv,'pointerdown',x-40,y,'pen',302);
  const e2=ptr(sv,'pointerdown',x+200,y,'touch',303), e2m=ptr(sv,'pointermove',x+200,y-30,'touch',303);
  ptr(sv,'pointerup',x+200,y-30,'touch',303); ptr(sv,'pointerup',x-40,y,'pen',302);
  T('G7 펜이 닿은 동안(penDown) — 손가락 pointerdown·pointermove defaultPrevented true(손바닥)', e2.defaultPrevented===true&&e2m.defaultPrevented===true, J([e2.defaultPrevented,e2m.defaultPrevented]));
  const e3=ptr(sv,'pointerdown',x,y+10,'touch',304); ptr(sv,'pointerup',x,y+10,'touch',304);
  T('G7 펜을 뗀 뒤 손가락은 다시 false', e3.defaultPrevented===false, e3.defaultPrevented);
  SE.scrollTop=0; ptr(sv,'pointerdown',x,y,'touch',305); for(let i=1;i<=6;i++) ptr(sv,'pointermove',x,y-i*30,'touch',305); const st=SE.scrollTop; ptr(sv,'pointerup',x,y-180,'touch',305);
  T('G7 JS 수동 굴림 없음 — 합성 손가락 끌기로 scrollTop 0(굴림은 브라우저 몫이라 합성으로는 안 굴러간다)', st===0, st);
  let tt=null; try{ tt=new Touch({identifier:1,target:sv,clientX:x,clientY:y,touchType:'stylus'}).touchType; }catch(e){ tt='err:'+e.message; }
  if(tt==='stylus'&&typeof TouchEvent==='function'){
    const te=(el,type,kind,id)=>{ const t=new Touch({identifier:id,target:el,clientX:x,clientY:y,touchType:kind}); const ev=new TouchEvent(type,{touches:[t],targetTouches:[t],changedTouches:[t],bubbles:true,cancelable:true}); el.dispatchEvent(ev); return ev.defaultPrevented; };
    const s1=te(sv,'touchstart','stylus',401), s1m=te(sv,'touchmove','stylus',401), f1=te(sv,'touchstart','direct',402);
    ptr(sv,'pointerdown',x-40,y,'pen',403); const f2=te(sv,'touchstart','direct',404); ptr(sv,'pointerup',x-40,y,'pen',403);
    T('G7 (iOS 흉내 TouchEvent) 필기모드 — 펜슬 touchstart·touchmove 막음 · 손가락 안 막음 · 펜이 닿은 동안 손가락 막음', s1&&s1m&&!f1&&f2, J({s1,s1m,f1,f2}));
    await penMode(false);
    const pp=document.querySelector('#q-box-Q9803 p'); const s2=te(pp,'touchstart','stylus',405);
    T('G7 (iOS 흉내) 표시 모드 — 펜슬 touchstart 도 안 막음(막는 손잡이를 뗐다)', s2===false, s2);
  } else say('G7 이 헤드리스의 Touch 생성자가 touchType 을 안 받는다('+tt+') — iOS 터치 막기는 못 쟀다');
  await penMode(false); showHome();
}

/* G8 덮개 touch-action */
async function G8(){
  resetLS({}); closeAllWins(); openQuiz(UNIT,'민법총칙',CH); await wait(150);
  if(!HASINK){ T('G8 필기모드 덮개 touch-action',false,'필기 없음'); showHome(); return; }
  await penMode(true);
  const ta=getComputedStyle(document.getElementById('ink-Q9801')).touchAction, tq=getComputedStyle(document.getElementById('qcards')).touchAction;
  T('G8 필기모드 — svg.qink computed touch-action = pan-y pinch-zoom · #qcards.penon = pan-y', ta==='pan-y pinch-zoom'&&tq==='pan-y', ta+' / '+tq);
  await penMode(false); showHome();
}

/* VAL 카드 글자 — 캐시를 써도 옛 판과 같은가(같은 판례 칩과 필기 덮개 태그만 걷고 대조) */
async function GV(){
  resetLS({ox_q_geunge:{Q9801:[gI('g_Q9801_a',1,'첫 근거')],Q9805:[gI('g_Q9805_a',1,'근거 하나')],Q9806:[gI('g_Q9806_a',1,'연결될 근거')],Q9809:[gI('g_Q9809_a',1,'아홉 근거'),gI('g_Q9809_b',2,'둘째')]},
           ox_q_reflinks:{Q9805:{geunge:['Q9806']},Q9809:{geunge:['Q9801','Q9805']}},ox_q_links:{Q9805:['Q9806'],Q9807:['Q9805'],Q9810:['Q9801','q9805']},
           ox_q_type:{Q9801:'판례형',Q9802:'조문형'},ox_q_tags:{Q9802:{fake:true,concept:false,memo:false,confuse:true,important:false}},ox_q_marks:{'q-Q9801':[[0,3,'y']],'e-Q9802':[[1,4,'u']]}});
  closeAllWins(); openQuiz(UNIT,'민법총칙',CH); await wait(200);
  const norm=h=>h.replace(/<svg class="qink"[\s\S]*?<\/svg>/g,'<svg-qink/>').replace(/<button onclick="(?:event\.stopPropagation\(\);)?showRelated\('(Q\d+)','same'\)"[\s\S]*?<\/button>/g,'<same-$1/>');
  const cards=()=>[...document.querySelectorAll('#quiz-container .question-box')].map(b=>norm(b.outerHTML));
  V('GV.cards.marksOn', cards());
  V('GV.yujeback', [...document.querySelectorAll('#quiz-container [onclick*="yujeback"]')].map(b=>b.outerHTML));
  if(HASINK){ await penMode(true); V('GV.cards.penOn', cards()); await penMode(false); }
  T('GV 카드가 그려진다(글자 대조는 VAL · 같은 판례 칩·필기 덮개 태그만 걷고 비교)', document.querySelectorAll('#quiz-container .question-box').length===20);
  showHome();
}

/* G10 — 화면 열림 · 콘솔 오류는 끝에서 */
async function G10(){
  resetLS({}); loadQuiz(); showHome(); closeAllWins();
  renderDashboard();
  T('G10 첫 화면이 그려진다', document.getElementById('dashboard-container').children.length>0);
  startQuiz('민법총칙',CH); await wait(120);
  T('G10 문제풀이가 열린다', !document.getElementById('quiz-screen').classList.contains('hide')&&!!document.getElementById('q-box-Q9801'));
  goHome();
  startQuiz('변리사 기출','2016년 제53회'); await wait(80);
  T('G10 기출뷰가 열린다', !!document.getElementById('q-box-Q9901'), document.getElementById('quiz-container').textContent.slice(0,120));
  goHome();
  startVirtualQuiz('하네스 큐', quizData.filter(q=>!q.examNo).slice(0,3)); await wait(80);
  T('G10 ⚡큐가 열린다', !document.getElementById('quiz-screen').classList.contains('hide')&&!!document.getElementById('q-box-Q9801'));
  goHome();
  startQuiz('민법총칙',CH); await wait(250);
  const a0=__ALERTS.length, pin=document.getElementById('tag-coord-Q9801');
  if(pin) pin.click();
  let cd=null;
  for(let i=0;i<200&&!(cd=document.getElementById('cd-close'));i++) await wait(50);
  T('G10 정리OMR(좌표기억) 뷰어가 열린다(카드 📍 단추)', !!pin&&!!cd&&__ALERTS.length===a0, 'pin '+!!pin+' · cd-close '+!!cd);
  if(cd) cd.click();
  goHome();
}

const LIST=[['G2',G2],['G3',G3],['G4',G4],['G5E',G5E],['G7',G7],['G8',G8],['GV',GV],['G10',G10]].filter(x=>P.skip.indexOf(x[0])<0);
say('판 = '+(NEW?'NEW(qpCacheOpen 있음)':'HEAD')+' · main');
setTimeout(async function(){
  for(const [n,f] of LIST){
    console.log('HZ-START '+n);
    try{ await f(); }
    catch(e){ T(n+' 하네스가 죽었다',false,e.message+' | '+(e.stack||'').split('\n').slice(1,3).join(' ')); }
  }
  await wait(300);
  const errs=(window.__ERR||[]), cerr=(window.__CERR||[]);
  T('G10 헤드리스 페이지 오류 0 · console.error 0', errs.length===0&&cerr.length===0, 'error '+errs.length+' '+errs.slice(0,3).join(' / ')+' · console.error '+cerr.length+' '+cerr.slice(0,3).join(' / '));
  R.forEach(x=>console.log('HZR|'+encodeURIComponent(x)));
  console.log('HZR|END');
},1500);
})();
