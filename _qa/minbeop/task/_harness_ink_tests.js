window.onload=null;
(function(){
const P=__P__;
const R=[];
const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+((i!==undefined&&!c)?' | '+String(i).replace(/\n/g,'⏎').slice(0,500):''));
const say=s=>R.push('INFO | '+String(s).replace(/\n/g,'⏎'));
const V=(k,v)=>R.push('VAL | '+k+' | '+JSON.stringify(v));
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
/* IndexedDB 는 가상 시계를 안 따른다 — 고정 대기 대신 조건을 기다린다 */
const until=async(f,n)=>{ for(let i=0;i<(n||100);i++){ try{ if(f()) return true; }catch(e){} await wait(30); } try{ return !!f(); }catch(e){ return false; } };
const CH='1. 총칙 > 1.1 민법의 법원';
const NEW=typeof qiAfterRender==='function';
const UNIT=P.quiz.filter(q=>!q.examNo&&q.subChapter==='1.1 민법의 법원').map(q=>q.id);
const ptr=(el,type,x,y,pt,id)=>{ const ev=new PointerEvent(type,{pointerType:pt,pointerId:id,isPrimary:true,bubbles:true,cancelable:true,composed:true,clientX:x,clientY:y,button:0,buttons:type==='pointerup'?0:1}); el.dispatchEvent(ev); return ev; };
const center=el=>{ const r=el.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; };
const textRect=p=>{ const rg=document.createRange(); rg.selectNodeContents(p); return rg.getClientRects(); };
const penMode=async on=>{ if(!NEW) return; if((!cardMarksOn)!==on){ qiToggle(); await wait(150); } };
const inkOf=async u=>{ try{ return await dbGet('ink:q:'+u); }catch(e){ return 'err:'+e.message; } };
const clearInk=async us=>{ if(!NEW) return; for(const u of us){ try{ await dbDel('ink:q:'+u); }catch(e){} } };
const paths=u=>{ const s=document.getElementById('ink-'+u); return s?s.querySelectorAll('path[data-j]').length:-1; };
say('판 = '+(NEW?'NEW(qiAfterRender 있음)':'HEAD')+(P.phase?' · '+P.phase:''));

/* G1 폭 — #qcards 900 · 좁으면 scale · 같은 문항 지문 줄바꿈이 폭과 상관없이 같은 자리 */
async function G1(){
  if(!NEW){ T('G1 #qcards 있음',false,'HEAD'); return; }
  resetLS({}); closeAllWins(); openQuiz(UNIT,'민법총칙',CH); await wait(150);
  const host=document.getElementById('quiz-container'), c=document.getElementById('qcards');
  T('G1 #qcards 레이아웃 폭 900 · transform-origin 왼쪽 위', !!c&&c.offsetWidth===900&&/^0px 0px/.test(getComputedStyle(c).transformOrigin), c?c.offsetWidth+' · '+getComputedStyle(c).transformOrigin:'없음');
  say('G1 하네스 창(1280) — 묶음 바깥(#quiz-container) 폭 '+host.clientWidth+'px · 배율 '+(c.getBoundingClientRect().width/900).toFixed(4)+' · 오른쪽 끝 '+c.getBoundingClientRect().right.toFixed(1)+' ≤ 바깥 오른쪽 '+host.getBoundingClientRect().right.toFixed(1));
  T('G1 PC 창에서 카드 묶음 오른쪽 끝이 바깥 틀 안(잘림 0)', c.getBoundingClientRect().right<=host.getBoundingClientRect().right+0.5, c.getBoundingClientRect().right+' / '+host.getBoundingClientRect().right);
  const p=document.querySelector('#q-box-Q9801 [data-mark="q-Q9801"]');
  host.style.width='600px'; qcardsFit(); await wait(30);
  const k6=c.getBoundingClientRect().width/900;
  T('G1 묶음 바깥 폭 600 이면 scale 0.667 · 아래 빈자리 줄임(margin-bottom 음수)', Math.abs(k6-0.6667)<0.003&&/^scale\(0\.66/.test(c.style.transform)&&parseFloat(c.style.marginBottom)<0, k6+' · '+c.style.transform+' · '+c.style.marginBottom);
  host.style.width='1100px'; qcardsFit(); await wait(30);
  const n1100=textRect(p).length, h1100=p.offsetHeight, k1100=c.getBoundingClientRect().width/900;
  host.style.width='820px'; qcardsFit(); await wait(30);
  const n820=textRect(p).length, h820=p.offsetHeight, k820=c.getBoundingClientRect().width/900;
  host.style.width=''; qcardsFit(); await wait(30);
  T('G1 같은 문항 지문 줄 수·높이가 폭 1100(PC)·820(아이패드)에서 같다', n1100===n820&&n1100>=3&&h1100===h820, J({n1100,n820,h1100,h820,k1100:+k1100.toFixed(4),k820:+k820.toFixed(4)}));
  say('G1 지문 줄 rect 수 1100:'+n1100+' · 820:'+n820+' · 높이 '+h1100+'/'+h820+'px · 배율 1100:'+k1100.toFixed(4)+' · 820:'+k820.toFixed(4));
  const svs=document.querySelectorAll('#qcards .question-box > svg.qink');
  T('G1 카드마다 덮개 svg.qink 하나(이 쪽 20)', svs.length===20&&document.querySelectorAll('#qcards .question-box').length===20, svs.length);
  showHome();
}

/* G2 토글 */
async function G2(){
  if(!NEW){ T('G2 qiToggle 있음',false,'HEAD'); return; }
  resetLS({ox_q_marks:{'q-Q9801':[[0,3,'y']]}}); closeAllWins(); openQuiz(UNIT,'민법총칙',CH);
  currentSessionMarks={Q9802:true}; renderQuizPage(); await wait(150);
  const tb=document.getElementById('ink-tools'), tg=document.getElementById('ink-toggle');
  T('G2 켜짐(기본) — 지문 data-mark · 형광펜 span · 도구 묶음 숨김 · 덮개 display:none · ✏️', !!document.querySelector('#q-box-Q9801 [data-mark="q-Q9801"] span[style]')&&tb.classList.contains('hide')&&getComputedStyle(document.getElementById('ink-Q9801')).display==='none'&&tg.textContent==='✏️'&&!document.getElementById('qcards').classList.contains('penon'));
  const tr=tg.getBoundingClientRect(), omr=[...document.querySelectorAll('#quiz-screen button')].find(b=>b.textContent.trim()==='📝 OMR'), orr=omr?omr.getBoundingClientRect():null;
  T('G2 토글 자리 = 머리줄 「📝 OMR」 왼쪽 · 같은 줄', !!orr&&tr.right<=orr.left+0.5&&Math.abs((tr.top+tr.height/2)-(orr.top+orr.height/2))<6, J({t:[tr.left,tr.right,tr.top],o:orr&&[orr.left,orr.top]}));
  togglePeekExp('Q9804');
  const gin=document.getElementById('gg-in-Q9806'); if(gin){ gin.value='토글 전 쓰던 근거'; gin.focus(); }
  const focused=!!gin&&document.activeElement===gin;
  await penMode(true);
  T('G2 끔 → 지문·해설 data-mark 0 · #qcards.penon · 도구 다섯 보임 · ✍', document.querySelectorAll('#qcards [data-mark]').length===0&&document.getElementById('qcards').classList.contains('penon')&&!tb.classList.contains('hide')&&tb.querySelectorAll('button').length===5&&tg.textContent==='✍', J({mark:document.querySelectorAll('#qcards [data-mark]').length,tools:tb.className,t:tg.textContent}));
  T('G2 채점 전에 펴 둔 「정답·해설」(Q9804)은 토글 뒤에도 펴져 있다(정답 글자까지)', !document.getElementById('exp-Q9804').classList.contains('hide')&&!document.getElementById('peek-ans-Q9804').classList.contains('hide'), document.getElementById('exp-Q9804').className);
  T('G2 근거 칸(Q9806)에 쓰던 글자는 토글이 다시 그리기 전에 저장된다(onblur)', focused&&(lsO('ox_q_geunge').Q9806||[]).some(g=>g&&g.t==='토글 전 쓰던 근거'), J({focused,gg:lsO('ox_q_geunge').Q9806}));
  const p=document.querySelector('#q-box-Q9801 p');
  try{ const rg=document.createRange(); rg.setStart(p.firstChild,0); rg.setEnd(p.firstChild,3); const sel=getSelection(); sel.removeAllRanges(); sel.addRange(rg); onSelectMaybe(); sel.removeAllRanges(); }catch(e){ T('G2 글자 고르기 조작 오류',false,e.message); }
  T('G2 필기모드에서 지문 글자를 골라도 #mark-bar 안 뜸', document.getElementById('mark-bar').classList.contains('hide'));
  const r2=[...document.querySelectorAll('input[name="answer_Q9802"]')];
  T('G2 채점된 카드(Q9802) — 라디오 disabled · ✓ 결과 그대로', r2.length===2&&r2.every(x=>x.disabled)&&/정답/.test((document.querySelector('#exp-Q9802 .result-badge')||{}).textContent||'')&&!document.getElementById('exp-Q9802').classList.contains('hide')&&(document.getElementById('ox-res-Q9802')||{}).textContent==='✓ 맞음', J({dis:r2.map(x=>x.disabled),badge:(document.querySelector('#exp-Q9802 .result-badge')||{}).textContent,res:(document.getElementById('ox-res-Q9802')||{}).textContent}));
  const cs=getComputedStyle(document.getElementById('ink-Q9801'));
  T('G2 덮개 보임(display block · pointer-events auto)', cs.display==='block'&&cs.pointerEvents==='auto', cs.display+' / '+cs.pointerEvents);
  await penMode(false);
  T('G2 다시 켬 → 형광펜 돌아옴 · 도구 묶음 사라짐 · 덮개 display:none', !!document.querySelector('#q-box-Q9801 [data-mark="q-Q9801"] span[style]')&&tb.classList.contains('hide')&&getComputedStyle(document.getElementById('ink-Q9801')).display==='none'&&!document.getElementById('qcards').classList.contains('penon'));
  showHome();
}

/* G3 긋기 */
async function G3(){
  if(!NEW){ T('G3 qiWire 있음',false,'HEAD'); return; }
  resetLS({}); closeAllWins(); await clearInk(['Q9801']); QI={};
  openQuiz(UNIT,'민법총칙',CH); await wait(150); await penMode(true);
  window.scrollTo(0,0); await wait(30);
  const sv=document.getElementById('ink-Q9801'), p=document.querySelector('#q-box-Q9801 p'), pr=p.getBoundingClientRect();
  const x0=pr.left+30, y0=pr.top+Math.min(40,pr.height/2);
  const top=document.elementFromPoint(x0,y0);
  T('G3 필기모드에서 지문 위 맨 위 요소 = 덮개 svg', top===sv, top?(top.tagName+'#'+top.id):'없음');
  ptr(sv,'pointerdown',x0,y0,'pen',71);
  for(let i=1;i<=20;i++) ptr(sv,'pointermove',x0+i*6,y0+(i%2),'pen',71);
  ptr(sv,'pointerup',x0+120,y0,'pen',71);
  await wait(450);
  const st=await inkOf('Q9801'), s0=st&&st.s&&st.s[0];
  T('G3 펜 down/move×20/up → ink:q:Q9801 에 획 1 · p 짝수 길이 · 0~1 정규화', !!s0&&st.s.length===1&&s0.p.length%2===0&&s0.p.length>=4&&s0.p.every(v=>v>=0&&v<=1), J(st&&{n:st.s&&st.s.length,len:s0&&s0.p.length,p:s0&&s0.p.slice(0,4)}));
  say('G3 획 점 '+(s0?s0.p.length/2:0)+'개 · 첫 점 '+(s0?s0.p.slice(0,2).join(','):''));
  const p1=sv.querySelector('path[data-j="0"]'), d1=p1?p1.getAttribute('d'):'';
  QI={}; renderQuizPage();
  await until(()=>paths('Q9801')===1);
  const pa=document.getElementById('ink-Q9801').querySelector('path[data-j="0"]'), d2=pa?pa.getAttribute('d'):'';
  T('G3 메모리 비우고 다시 그리면(IndexedDB 에서) 같은 path(d 글자 같음)', !!d1&&d1===d2, J([d1.slice(0,60),d2.slice(0,60)]));
  const sv2=document.getElementById('ink-Q9801');
  const f0=document.elementFromPoint(x0,y0+20);
  ptr(f0,'pointerdown',x0,y0+20,'touch',72); for(let i=1;i<=5;i++) ptr(f0,'pointermove',x0+i*8,y0+20,'touch',72); ptr(f0,'pointerup',x0+40,y0+20,'touch',72);
  ptr(sv2,'pointerdown',x0,y0+24,'mouse',1); for(let i=1;i<=5;i++) ptr(sv2,'pointermove',x0+i*8,y0+24,'mouse',1); ptr(sv2,'pointerup',x0+40,y0+24,'mouse',1);
  await wait(450);
  const st2=await inkOf('Q9801');
  T('G3 손가락·마우스 down/move/up → 획 0(펜만 긋는다)', ((QI.Q9801&&QI.Q9801.s.length)||0)===1&&!!st2&&!!st2.s&&st2.s.length===1&&paths('Q9801')===1, J({mem:QI.Q9801&&QI.Q9801.s.length,db:st2&&st2.s&&st2.s.length,dom:paths('Q9801')}));
  await penMode(false); showHome();
}

/* G4 손바닥 */
async function G4(){
  if(!NEW){ T('G4 qiGuard 있음',false,'HEAD'); return; }
  resetLS({}); closeAllWins(); await clearInk(['Q9803']); QI={};
  openQuiz(UNIT,'민법총칙',CH); await wait(150); await penMode(true);
  const SE=document.scrollingElement;
  SE.scrollTop=0; await wait(30);
  const sv=document.getElementById('ink-Q9803'), p=document.querySelector('#q-box-Q9803 p'), pr=p.getBoundingClientRect();
  const x=pr.left+40, y=pr.top+Math.min(40,pr.height/2);
  ptr(sv,'pointerdown',x,y,'pen',81);
  ptr(sv,'pointerdown',x+300,y+10,'touch',82);
  for(let i=1;i<=6;i++) ptr(sv,'pointermove',x+300,y+10-i*30,'touch',82);
  const s1=SE.scrollTop;
  ptr(sv,'pointerup',x+300,y-170,'touch',82);
  ptr(sv,'pointerup',x,y,'pen',81);
  T('G4 펜이 닿은 뒤 닿은 손가락은 스크롤 0(손바닥)', s1===0, s1);
  await wait(400);
  const q3=(QI.Q9803&&QI.Q9803.s)||[];
  T('G4 손바닥이 덮개 위에서 움직여도 펜 획에 안 섞인다(점 획 1 · 값 4개)', q3.length===1&&q3[0].p.length===4, J(q3));
  SE.scrollTop=0; await wait(30);
  const pr2=p.getBoundingClientRect(), x2=pr2.left+40, y2=pr2.top+Math.min(40,pr2.height/2);
  ptr(sv,'pointerdown',x2,y2,'touch',83);
  for(let i=1;i<=6;i++) ptr(sv,'pointermove',x2,y2-i*30,'touch',83);
  const s2=SE.scrollTop;
  ptr(sv,'pointerup',x2,y2-180,'touch',83);
  T('G4 펜 떼고 손가락만이면 스크롤 됨(손가락으로 굴림 · 굴리는 통 = document.scrollingElement)', s2>=100&&SE===document.documentElement, s2+' · '+(SE&&SE.tagName));
  SE.scrollTop=0; await wait(30);
  const tb=document.getElementById('tag-fake-Q9803'), [bx,by]=center(tb), top=document.elementFromPoint(bx,by);
  ptr(top,'pointerdown',bx,by,'touch',84); ptr(top,'pointerup',bx,by,'touch',84);
  await wait(60);
  T('G4 단추(⚠️ 태그) 위에서 시작한 손가락은 그대로 눌림(덮개 밑 · 스크롤 0)', !!(lsO('ox_q_tags').Q9803||{}).fake&&SE.scrollTop===0&&!!top&&top.tagName.toLowerCase()==='svg', J({tag:lsO('ox_q_tags').Q9803,top:top&&top.tagName,st:SE.scrollTop}));
  await penMode(false); showHome();
}

/* G5 덮개 뚫기(펜) · §0 카드 안 눌리는 것 census */
async function G5(){
  if(!NEW){ T('G5 qiPierce 있음',false,'HEAD'); return; }
  const gI=(k,i,t)=>({k:k,i:i,t:t,ok:null,ts:1789000000000,cs:[]});
  resetLS({ox_q_geunge:{Q9805:[gI('g_Q9805_a',1,'근거 하나')],Q9806:[gI('g_Q9806_a',1,'연결될 근거')]},ox_q_reflinks:{Q9805:{geunge:['Q9806']}},ox_q_links:{Q9805:['Q9806'],Q9807:['Q9805']}});
  closeAllWins(); await clearInk(['Q9805']); QI={};
  openQuiz(UNIT,'민법총칙',CH); await wait(150); await penMode(true);
  await until(()=>QI.Q9805&&Array.isArray(QI.Q9805.s));
  document.getElementById('q-box-Q9805').scrollIntoView({block:'center'}); await wait(60);
  const tap=(el,id)=>{ const [x,y]=center(el); const t=document.elementFromPoint(x,y); ptr(t,'pointerdown',x,y,'pen',id); ptr(t,'pointerup',x,y,'pen',id); return t; };
  const t1=tap(document.getElementById('ox-O-Q9805'),91); await wait(40);
  T('G5 펜으로 O 단추 자리 톡 → 라디오 checked · 획 0 · 맨 위는 덮개', (document.querySelector('input[name="answer_Q9805"][value="O"]')||{}).checked===true&&((QI.Q9805&&QI.Q9805.s.length)||0)===0&&!!t1&&t1.tagName.toLowerCase()==='svg', J({t:t1&&t1.tagName,n:QI.Q9805&&QI.Q9805.s.length}));
  tap(document.getElementById('peek-btn-Q9805'),92); await wait(40);
  T('G5 「정답·해설 ▸」 펴짐', !document.getElementById('exp-Q9805').classList.contains('hide'));
  tap(document.getElementById('tag-concept-Q9805'),93); await wait(40);
  T('G5 태그(💡) 토글', !!(lsO('ox_q_tags').Q9805||{}).concept, J(lsO('ox_q_tags').Q9805));
  const chip=document.querySelector('[id^="gg-chip-Q9805-"]'); if(chip) tap(chip,94); await wait(40);
  const pan=document.querySelector('[id^="gg-pan-Q9805-"]');
  T('G5 근거 칩 펼침', !!chip&&!!pan&&!pan.classList.contains('hide'), pan?pan.className:'없음');
  const gin=document.getElementById('gg-in-Q9805'); tap(gin,95); await wait(40);
  T('G5 근거 입력칸에 포커스', document.activeElement===gin, document.activeElement?document.activeElement.id||document.activeElement.tagName:'없음');
  if(document.activeElement===gin) gin.blur();
  const p=document.querySelector('#q-box-Q9805 p'), pr=p.getBoundingClientRect(), x=pr.left+50, y=pr.top+Math.min(40,pr.height/2);
  const t2=document.elementFromPoint(x,y); ptr(t2,'pointerdown',x,y,'pen',96); ptr(t2,'pointerup',x,y,'pen',96);
  await wait(450);
  const st=await inkOf('Q9805');
  T('G5 빈 자리(지문 글자 위) 톡 → 점 획 1', !!st&&!!st.s&&st.s.length===1&&st.s[0].p.length===4, J(st));
  /* §0 — 이 쪽 카드 안에서 눌리는 것 전부(Q9805 는 기록 줄·메모 칸·근거 찾기·연결 근거를 펴서 숨은 것까지) */
  try{ recStripToggle('Q9805'); toggleMemoPanel('Q9805'); ggSearchToggle('Q9805'); }catch(e){ say('§0 펴기 오류 '+e.message); }
  const rc=document.querySelector('[id^="gg-refchip-Q9805-"]'); if(rc) rc.click();
  await wait(60);
  const FIELD='textarea,select,input:not([type="radio"]):not([type="checkbox"]):not([type="button"]):not([type="submit"]):not([type="file"])';
  const TAGS=['button','a','label','input','select','textarea','summary'];
  const kinds={}, miss=[]; let nAll=0;
  document.querySelectorAll('#qcards .question-box').forEach(b=>b.querySelectorAll('*').forEach(el=>{
    if(el.closest('svg')) return;
    const tag=el.tagName.toLowerCase();
    const own=TAGS.indexOf(tag)>=0||el.hasAttribute('onclick')||el.getAttribute('role')==='button';
    const ptrOnly=!own&&getComputedStyle(el).cursor==='pointer'&&!(el.parentElement&&getComputedStyle(el.parentElement).cursor==='pointer');
    if(!own&&!ptrOnly) return;
    nAll++;
    const id=(el.id||'').replace(/Q\d{4}.*$/,'*');
    const k=tag+(el.hasAttribute('onclick')?'[onclick]':'')+(el.type&&tag==='input'?'['+el.type+']':'')+(id?'#'+id:'')+(ptrOnly?'(cursor:pointer만)':'');
    const cov=el.closest(FIELD)?'글자칸':el.closest(QI_HIT)?'누름':null;
    if(!kinds[k]) kinds[k]={n:0,cov:cov}; kinds[k].n++;
    if(!cov) miss.push(k);
  }));
  say('§0 카드 안 눌리는 것 '+nAll+'개 · '+Object.keys(kinds).sort().map(k=>k+' ×'+kinds[k].n+'→'+(kinds[k].cov||'빠짐')).join(' · '));
  T('G5 §0 카드 안 눌리는 것 전부가 QI_HIT(누름)·글자칸에 걸린다(빠짐 0)', nAll>100&&miss.length===0, J([...new Set(miss)])+' · '+nAll);
  await penMode(false); showHome();
}

/* G6 펜 톡 위임 */
async function G6(){
  if(!NEW){ T('G6 펜 톡 위임 있음',false,'HEAD'); return; }
  resetLS({}); closeAllWins(); openQuiz(UNIT,'민법총칙',CH); await wait(150);
  const b=document.getElementById('peek-btn-Q9807'); let nc=0; const on=()=>nc++; b.addEventListener('click',on);
  b.scrollIntoView({block:'center'}); await wait(30);
  const [x,y]=center(b);
  ptr(b,'pointerdown',x,y,'pen',101); ptr(b,'pointerup',x,y,'pen',101);
  const c0=nc; await wait(150); const c1=nc;
  T('G6 click 이 안 온 펜 톡(pointerdown/up 만) → 60ms 뒤 click 합성 한 번', c0===0&&c1===1, J({c0,c1}));
  await wait(400);
  nc=0; ptr(b,'pointerdown',x,y,'pen',102); ptr(b,'pointerup',x,y,'pen',102); b.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,view:window}));
  await wait(450);
  T('G6 진짜 click 이 온 뒤 350ms 안에는 합성 0(click 1번)', nc===1, nc);
  nc=0; ptr(b,'pointerdown',x,y,'mouse',1); ptr(b,'pointerup',x,y,'mouse',1); await wait(150);
  T('G6 마우스는 합성 0', nc===0, nc);
  nc=0; ptr(b,'pointerdown',x,y,'touch',103); ptr(b,'pointerup',x,y,'touch',103); await wait(150);
  T('G6 손가락은 합성 0(민법은 펜만 · 손가락 click 은 브라우저가 낸다)', nc===0, nc);
  nc=0; ptr(b,'pointerdown',x,y,'pen',104); ptr(b,'pointerup',x+12,y,'pen',104); await wait(150);
  T('G6 8px 넘게 끈 펜은 합성 0', nc===0, nc);
  b.removeEventListener('click',on);
  showHome(); renderDashboard(); await wait(60);
  const hb=[...document.querySelectorAll('#home-screen button')].find(z=>z.offsetParent);
  let nh=0; const onh=e=>{ nh++; e.stopPropagation(); e.preventDefault(); };
  if(hb){ hb.addEventListener('click',onh,true); const [hx,hy]=center(hb); ptr(hb,'pointerdown',hx,hy,'pen',105); ptr(hb,'pointerup',hx,hy,'pen',105); await wait(150); hb.removeEventListener('click',onh,true); }
  T('G6 문제풀이 화면·떠 있는 창 밖(첫 화면)은 합성 0', !!hb&&nh===0, J({hb:hb&&hb.textContent.trim().slice(0,20),nh}));
}

/* G7 지우개 · 🗑 */
async function G7(){
  if(!NEW){ T('G7 qiEraseAt 있음',false,'HEAD'); return; }
  resetLS({}); closeAllWins(); QI={};
  await clearInk(['Q9809','Q9810']);
  await dbPut('ink:q:Q9821',{s:[{c:'#16181B',w:2,hl:0,p:[0.1,0.05,0.2,0.05]}]});
  openQuiz(UNIT,'민법총칙',CH); await wait(150); await penMode(true);
  await until(()=>QI.Q9809&&Array.isArray(QI.Q9809.s));
  document.getElementById('q-box-Q9809').scrollIntoView({block:'center'}); await wait(60);
  const sv=document.getElementById('ink-Q9809'), p=document.querySelector('#q-box-Q9809 p'), pr=p.getBoundingClientRect();
  const x0=pr.left+40, y0=pr.top+12;
  const line=(yy,id)=>{ ptr(sv,'pointerdown',x0,yy,'pen',id); for(let i=1;i<=8;i++) ptr(sv,'pointermove',x0+i*10,yy,'pen',id); ptr(sv,'pointerup',x0+80,yy,'pen',id); };
  line(y0,111); line(y0+14,112); line(y0+28,113);
  await wait(450);
  T('G7 획 3', ((QI.Q9809&&QI.Q9809.s.length)||0)===3&&pr.height>=40, J({n:QI.Q9809&&QI.Q9809.s.length,h:pr.height}));
  qiTool('erase');
  T('G7 지우개 도구 켜짐 표시', !!document.querySelector('#ink-tools [data-qi="erase"].on')&&!document.querySelector('#ink-tools [data-qi="pen"].on'));
  ptr(sv,'pointerdown',x0+30,y0+14,'pen',114); ptr(sv,'pointerup',x0+30,y0+14,'pen',114);
  await wait(450);
  const st=await inkOf('Q9809');
  const ys=(st&&st.s||[]).map(s=>s.p[1]);
  T('G7 지우개 톡 → 2(가운데 획이 빠짐) · 저장 반영', ((QI.Q9809&&QI.Q9809.s.length)||0)===2&&!!st&&!!st.s&&st.s.length===2&&ys[1]-ys[0]>0.02, J({mem:QI.Q9809&&QI.Q9809.s.length,db:st&&st.s&&st.s.length,ys}));
  qiTool('pen');
  await dbPut('ink:q:Q9810',{s:[{c:'#16181B',w:2,hl:0,p:[0.1,0.05,0.2,0.05]}]});
  QI={}; renderQuizPage();
  await until(()=>paths('Q9810')===1&&paths('Q9809')===2);
  window.__CONFIRM_ANS=false; const c0=__CONFIRMS.length;
  await qiClearPage();
  const msg=__CONFIRMS[c0]||'', keep=await inkOf('Q9809');
  T('G7 🗑 → 확인창 「이 쪽 20문항 필기를 모두 지웁니다」 · 아니오 → 그대로', msg==='이 쪽 20문항 필기를 모두 지웁니다'&&!!keep&&!!keep.s&&keep.s.length===2&&paths('Q9809')===2, J({msg,keep:keep&&keep.s&&keep.s.length}));
  window.__CONFIRM_ANS=true;
  await qiClearPage(); await wait(50);
  const a=await inkOf('Q9809'), b=await inkOf('Q9810'), o=await inkOf('Q9821');
  T('G7 예 → 이 쪽 문항 전부 0 · 다른 쪽(Q9821) 필기 그대로', !a&&!b&&!!o&&!!o.s&&o.s.length===1&&document.querySelectorAll('#qcards svg.qink path[data-j]').length===0, J({a,b,o:o&&o.s&&o.s.length}));
  await penMode(false); showHome();
}

/* G8 다른 문항·다른 쪽 */
async function G8(){
  if(!NEW){ T('G8 필기 저장 있음',false,'HEAD'); return; }
  resetLS({}); closeAllWins(); QI={};
  await clearInk(UNIT);
  openQuiz(UNIT,'민법총칙',CH); await wait(150); await penMode(true);
  await until(()=>QI.Q9811&&Array.isArray(QI.Q9811.s));
  document.getElementById('q-box-Q9811').scrollIntoView({block:'center'}); await wait(60);
  const sv=document.getElementById('ink-Q9811'), p=document.querySelector('#q-box-Q9811 p'), pr=p.getBoundingClientRect(), x0=pr.left+40, y0=pr.top+Math.min(30,pr.height/2);
  ptr(sv,'pointerdown',x0,y0,'pen',121); for(let i=1;i<=6;i++) ptr(sv,'pointermove',x0+i*10,y0,'pen',121); ptr(sv,'pointerup',x0+60,y0,'pen',121);
  await wait(450);
  currentPageIndex=1; renderQuizPage();
  await until(()=>document.querySelectorAll('#qcards svg.qink').length===5&&['Q9821','Q9822','Q9823','Q9824','Q9825'].every(u=>QI[u]&&Array.isArray(QI[u].s)));
  const on2=document.querySelectorAll('#qcards svg.qink path[data-j]').length;
  currentPageIndex=0; renderQuizPage();
  await until(()=>paths('Q9811')===1);
  const n11=paths('Q9811');
  const others=[...document.querySelectorAll('#qcards svg.qink')].filter(s=>s.id!=='ink-Q9811').reduce((t,s)=>t+s.querySelectorAll('path[data-j]').length,0);
  T('G8 쪽을 넘겼다 돌아와도 획이 제 문항(Q9811)에만', n11===1&&others===0&&on2===0, J({n11,others,on2}));
  QI={}; renderQuizPage();
  T('G8 메모리를 비우고 다시 그려도(IndexedDB 에서) 보인다', await until(()=>paths('Q9811')===1));
  const keys=[]; for(let i=0;i<localStorage.length;i++) keys.push(localStorage.key(i));
  T('G8 localStorage 에 필기 키 0(키·값에 ink:q: 없음)', !keys.some(k=>/ink/i.test(k)||(localStorage.getItem(k)||'').indexOf('ink:q:')>=0), J(keys));
  await penMode(false); showHome();
}

/* G8R — 크롬을 닫고 같은 프로필로 다시 연 판(진짜 새로고침) */
async function G8R(){
  resetLS({}); closeAllWins(); QI={};
  openQuiz(UNIT,'민법총칙',CH); await wait(150);
  T('G8 새로고침 뒤 「✏️ 표시」는 켜짐(메모리 값) · 덮개 숨김', cardMarksOn===true&&getComputedStyle(document.getElementById('ink-Q9811')).display==='none');
  await penMode(true);
  const ok=await until(()=>paths('Q9811')===1,200);
  const others=[...document.querySelectorAll('#qcards svg.qink')].filter(s=>s.id!=='ink-Q9811').reduce((t,s)=>t+s.querySelectorAll('path[data-j]').length,0);
  T('G8 진짜 새로고침(크롬을 닫고 같은 프로필로 다시 열기) 뒤 Q9811 필기 1획 · 다른 문항 0', ok&&others===0, J({q9811:paths('Q9811'),others}));
  await penMode(false); showHome();
}

/* G10 — 헤드리스 화면 열림 · 마우스만 쓰는 조작은 지금과 같다(형광펜 켠 채) · 콘솔 오류는 끝에서 */
async function G10(){
  resetLS({}); loadQuiz(); showHome(); closeAllWins();
  renderDashboard();
  T('G10 첫 화면이 그려진다', document.getElementById('dashboard-container').children.length>0);
  startQuiz('민법총칙',CH); await wait(120);
  T('G10 문제풀이가 열린다', !document.getElementById('quiz-screen').classList.contains('hide')&&!!document.getElementById('q-box-Q9801'));
  const lb=document.getElementById('ox-O-Q9801'); if(lb) lb.click();
  toggleTag('Q9801','fake');
  const pm=document.querySelector('#q-box-Q9801 [data-mark="q-Q9801"]');
  try{ const rg=document.createRange(); rg.setStart(pm.firstChild,0); rg.setEnd(pm.firstChild,4); const sel=getSelection(); sel.removeAllRanges(); sel.addRange(rg); onSelectMaybe(); applyMark('y'); }catch(e){ T('G10 형광펜 긋기 조작 오류',false,e.message); }
  V('G10.mouse.store', {tags:localStorage.getItem('ox_q_tags'), marks:localStorage.getItem('ox_q_marks'), picked:(document.querySelector('input[name="answer_Q9801"]:checked')||{}).value||null, markHTML:(document.querySelector('#q-box-Q9801 [data-mark="q-Q9801"]')||{}).innerHTML||null});
  T('G10 마우스 조작(O 고르기·태그·형광펜) — 형광펜 켠 채 그대로 · 덮개 안 보임 · 도구 숨김', (document.querySelector('input[name="answer_Q9801"]:checked')||{}).value==='O'&&!!document.querySelector('#q-box-Q9801 [data-mark="q-Q9801"] span[style]')&&(!NEW||(getComputedStyle(document.getElementById('ink-Q9801')).display==='none'&&document.getElementById('ink-tools').classList.contains('hide'))));
  goHome();
  startQuiz('변리사 기출','2016년 제53회'); await wait(80);
  T('G10 기출뷰가 열린다', !!document.getElementById('q-box-Q9901'), document.getElementById('quiz-container').textContent.slice(0,120));
  if(NEW) say('G10 기출뷰 덮개 '+document.querySelectorAll('#qcards svg.qink').length+'개 · #qcards 폭 '+(document.getElementById('qcards')||{}).offsetWidth);
  goHome();
  startVirtualQuiz('하네스 큐', quizData.filter(q=>!q.examNo).slice(0,3)); await wait(80);
  T('G10 ⚡큐가 열린다', !document.getElementById('quiz-screen').classList.contains('hide')&&!!document.getElementById('q-box-Q9801')&&document.getElementById('current-subject-title').textContent==='⚡ 빠른 실행');
  goHome();
  startQuiz('민법총칙',CH);
  await wait(250);
  const a0=__ALERTS.length, pin=document.getElementById('tag-coord-Q9801');
  if(pin) pin.click();
  let cd=null;
  for(let i=0;i<200&&!(cd=document.getElementById('cd-close'));i++) await wait(50);
  T('G10 정리OMR(좌표기억) 뷰어가 열린다(카드 📍 단추)', !!pin&&!!cd&&__ALERTS.length===a0, 'pin '+!!pin+' · cd-close '+!!cd+' · alert '+__ALERTS.slice(a0).join('/'));
  if(cd) cd.click();
  goHome();
}

const ALL=P.phase==='reload'?[['G8R',G8R]]:[['G1',G1],['G2',G2],['G3',G3],['G4',G4],['G5',G5],['G6',G6],['G7',G7],['G8',G8],['G10',G10]];
const LIST=ALL.filter(x=>P.skip.indexOf(x[0])<0);
if(P.skip.length) say('건너뜀(진단용) : '+P.skip.join(','));
setTimeout(async function(){
  for(const [n,f] of LIST){
    console.log('HZ-START '+n);
    try{ await f(); }
    catch(e){ T(n+' 하네스가 죽었다',false,e.message+' | '+(e.stack||'').split('\n').slice(1,3).join(' ')); }
    console.log('HZ-END '+n+' · '+R.filter(x=>x.startsWith('FAIL')).length+' FAIL');
  }
  await wait(300);
  const errs=(window.__ERR||[]), cerr=(window.__CERR||[]);
  T('G10 헤드리스 페이지 오류 0 · console.error 0'+(P.phase?' ('+P.phase+')':''), errs.length===0&&cerr.length===0, 'error '+errs.length+' '+errs.slice(0,3).join(' / ')+' · console.error '+cerr.length+' '+cerr.slice(0,3).join(' / '));
  say('alert '+__ALERTS.length+'번 : '+__ALERTS.slice(0,3).join(' / ')+' · confirm '+__CONFIRMS.length+'번');
  R.forEach(x=>console.log('HZR|'+encodeURIComponent(x)));
  console.log('HZR|END');
},1500);
})();
