window.onload=null;
(function(){
const P=__P__;
const R=[];
const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+((i!==undefined&&!c)?' | '+String(i).replace(/\n/g,'⏎').slice(0,500):''));
const say=s=>R.push('INFO | '+String(s).replace(/\n/g,'⏎'));
const V=(k,v)=>R.push('VAL | '+k+' | '+JSON.stringify(v));
const J=v=>JSON.stringify(v);
const lsO=k=>{try{return JSON.parse(localStorage.getItem(k)||'{}')||{}}catch(e){return {}}};
const BASE={'ox_uid_migrated':'1','ox_gg_okreset':'1','ox_gg_memo_merged':'{"at":1,"moved":0,"links":0}','ox_auto_important_v2':'1'};
const resetLS=o=>{ localStorage.clear(); for(const k in BASE) localStorage.setItem(k,BASE[k]); for(const k in (o||{})) localStorage.setItem(k,typeof o[k]==='string'?o[k]:JSON.stringify(o[k])); try{useIdxDrop()}catch(e){} try{mcInvalidate()}catch(e){} };
const loadQuiz=()=>{ quizData.length=0; P.quiz.forEach(q=>quizData.push(JSON.parse(JSON.stringify(q)))); };
const closeAllWins=()=>document.querySelectorAll('.oxwin').forEach(w=>w.remove());
const showHome=()=>{ document.getElementById('home-screen').classList.remove('hide'); document.getElementById('quiz-screen').classList.add('hide'); };
const openQuiz=(ids,subject,chap)=>{
  loadQuiz();
  currentSubject=subject; currentChapterLabel=chap; isExamMode=false; currentPageIndex=0; currentSessionMarks={}; resumePicks={}; currentSessionScore=0; lastGradeResults=null;
  if(typeof chapterSaved!=='undefined') chapterSaved=null;   /* startQuiz 가 하는 그대로(add1) */
  currentFilteredData=ids.map(id=>quizData.find(q=>q.id===id));
  document.getElementById('home-screen').classList.add('hide'); document.getElementById('quiz-screen').classList.remove('hide');
  document.getElementById('reopen-grade-bar').classList.add('hide'); document.getElementById('controls-container').classList.remove('hide');
  renderQuizPage();
};
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const CH='1. 총칙 > 1.1 민법의 법원';
const NEW=typeof oxPaint==='function';
const UNIT=P.quiz.filter(q=>!q.examNo).map(q=>q.id);
const mc=()=>{ const c=document.getElementById('mark-count'), t=document.getElementById('mark-total'); return c&&t?c.textContent+'/'+t.textContent:'없음'; };
const tagsOf=b=>[...b.querySelectorAll('button[id^="tag-"]')].filter(x=>!/^tag-coord-/.test(x.id));
say('판 = '+(NEW?'NEW(oxPaint 있음)':'HEAD'));

async function G1(){
  resetLS({}); closeAllWins();
  openQuiz(UNIT.slice(0,20),'민법총칙',CH);
  const boxes=[...document.querySelectorAll('#quiz-container .question-box')];
  T('G1 카드 20장', boxes.length===20, boxes.length);
  T('G1 .ox-label 큰 상자 0', document.querySelectorAll('.ox-label').length===0, document.querySelectorAll('.ox-label').length);
  const radiosOk=boxes.every(b=>{ const id=b.id.slice(6), rs=[...document.querySelectorAll(`input[name="answer_${id}"]`)];
    return rs.length===2&&rs[0].value==='O'&&rs[1].value==='X'&&rs.every(r=>r.type==='radio'&&b.contains(r)); });
  T('G1 카드마다 라디오 O·X 둘 그대로(name·value · 카드 안)', radiosOk);
  const info=boxes.map(b=>{ const tb=tagsOf(b); return {n:tb.length, span:tb.filter(x=>x.querySelector('span')).length, notitle:tb.filter(x=>!x.title).length}; });
  T('G1 태그 단추 5 · 글자 span 0 · title 있음', info.every(x=>x.n===5&&x.span===0&&x.notitle===0), J(info[0]));
  const qc=document.getElementById('quiz-container');
  T('G1 「해설 미리보기」 글자 0 · 「정답·해설 ▸」 카드마다 1', qc.textContent.indexOf('해설 미리보기')<0&&boxes.every(b=>[...b.querySelectorAll('button')].filter(x=>x.textContent.trim()==='정답·해설 ▸').length===1));
  const tb=document.getElementById('tag-confuse-'+UNIT[0]), r=tb.getBoundingClientRect();
  T('G1 태그 단추 24×22px(아이콘만)', Math.round(r.width)===24&&Math.round(r.height)===22, r.width+'×'+r.height);
  const lo=document.getElementById('ox-O-'+UNIT[0]), lr=lo?lo.getBoundingClientRect():null, rr=document.querySelector(`input[name="answer_${UNIT[0]}"]`).getBoundingClientRect();
  T('G1 O·X 단추 26×22px · 라디오는 안 보인다(sr-only)', !!lr&&Math.round(lr.width)===26&&Math.round(lr.height)===22&&rr.width<=1&&rr.height<=1, lr?lr.width+'×'+lr.height+' · 라디오 '+rr.width+'×'+rr.height:'없음');
  const bl=lo?lo.parentElement:null;
  T('G1 아랫줄 = 정답·해설 ▸ · O · X · (결과) · 오른쪽 논리·연결', !!bl&&bl.children[0].textContent==='정답·해설 ▸'&&bl.children[1]===lo&&bl.children[2].id==='ox-X-'+UNIT[0]&&/✏️ 논리·연결/.test(bl.lastElementChild.textContent), bl?bl.textContent.replace(/\s+/g,' '):'없음');
  const g3=document.getElementById('logic-btn-'+UNIT[2]), g1b=document.getElementById('logic-btn-'+UNIT[0]);
  T('G1 논리 단추는 있을 때만(Q9803 보임 · Q9801 숨김)', !!g3&&!g3.classList.contains('hide')&&!!g1b&&g1b.classList.contains('hide'));
  resetLS({}); loadQuiz(); showHome();
  startQuiz('변리사 기출','2016년 제53회');
  const eb=[...document.querySelectorAll('#quiz-container .question-box')];
  const en=eb.map(b=>tagsOf(b).length);
  T('G1 기출뷰 태그 단추 4 · 라디오 둘 · 정답·해설 ▸', eb.length>0&&en.every(n=>n===4)&&eb.every(b=>b.querySelectorAll('input[type="radio"]').length===2&&[...b.querySelectorAll('button')].some(x=>x.textContent.trim()==='정답·해설 ▸')), J(en));
  goHome();
}
async function G2(){
  if(!NEW){ T('G2 O·X 단추(oxPaint)가 있다',false,'없음'); return; }
  resetLS({}); closeAllWins();
  openQuiz(UNIT.slice(0,20),'민법총칙',CH);
  const u=UNIT[0], lO=document.getElementById('ox-O-'+u), lX=document.getElementById('ox-X-'+u);
  const rO=document.querySelector(`input[name="answer_${u}"][value="O"]`), rX=document.querySelector(`input[name="answer_${u}"][value="X"]`);
  T('G2 처음 「마킹 0/20」', mc()==='0/20', mc());
  lO.click();
  T('G2 O 단추 누름 → 라디오 checked · 파란 채움 · 「마킹 1/20」', rO.checked&&lO.classList.contains('bg-blue-700')&&lO.classList.contains('text-white')&&mc()==='1/20', lO.className+' · '+mc());
  lX.click();
  T('G2 X 로 바꾸면 빨강만(O 채움 풀림) · 「마킹 1/20」', rX.checked&&!rO.checked&&lX.classList.contains('bg-red-600')&&!lO.classList.contains('bg-blue-700')&&mc()==='1/20', lO.className+' | '+lX.className+' · '+mc());
  openOmrPad();
  const u2=UNIT[1];
  omrMark(u2,'O');
  const l2=document.getElementById('ox-O-'+u2), oc=document.getElementById('omr-count');
  T('G2 OMR 창에서 마킹 → 카드 라디오·색·수 같음', document.querySelector(`input[name="answer_${u2}"][value="O"]`).checked&&l2.classList.contains('bg-blue-700')&&mc()==='2/20'&&!!oc&&oc.textContent.replace(/\s/g,'')==='마킹2/20', l2.className+' · '+mc()+' · '+(oc&&oc.textContent));
  closeOmrPad();
  resumePicks={}; resumePicks[UNIT[3]]='X';
  renderQuizPage();
  const l3=document.getElementById('ox-X-'+UNIT[3]);
  T('G2 복원(resumePicks) 뒤에도 색 맞음 · 「마킹 1/20」', document.querySelector(`input[name="answer_${UNIT[3]}"][value="X"]`).checked&&l3.classList.contains('bg-red-600')&&mc()==='1/20', l3.className+' · '+mc());
  const r4=document.querySelector(`input[name="answer_${UNIT[4]}"][value="O"]`); r4.checked=true; r4.dispatchEvent(new Event('change',{bubbles:true}));
  T('G2 라디오 change(키보드 등) → 색 · 「마킹 2/20」', document.getElementById('ox-O-'+UNIT[4]).classList.contains('bg-blue-700')&&mc()==='2/20', mc());
}
async function G3(){
  resetLS({}); closeAllWins();
  const ids=UNIT.slice(0,5);                                    /* 정답 O X O X O */
  openQuiz(ids,'민법총칙',CH);
  const pick=['O','X','O','O','X'];                             /* 맞음 3 · 틀림 2(4번째 X→O · 5번째 O→X) */
  ids.forEach((id,i)=>{ document.querySelector(`input[name="answer_${id}"][value="${pick[i]}"]`).checked=true; });
  gradeCurrentPage();   /* add1 — 마지막 쪽은 채점과 함께 저장되고 창을 닫으면 목록으로 가므로 여기서 닫지 않는다 */
  const colorCls=b=>b.className.split(/\s+/).filter(c=>/^(border-(green|red|gray)-\d+|bg-(green|red)-50(\/\d+)?)$/.test(c)).sort();
  ids.forEach(id=>{ const b=document.getElementById('q-box-'+id);
    V('G3.badge.'+id, b.querySelector('.result-badge').innerHTML); V('G3.qboxColor.'+id, colorCls(b));
    V('G3.radio.'+id, [...document.querySelectorAll(`input[name="answer_${id}"]`)].map(r=>[r.value,r.checked,r.disabled])); });
  if(!NEW){ T('G3 채점 뒤 O·X 칠하기(oxPaint)',false,'없음'); return; }
  const w=ids[3], wO=document.getElementById('ox-O-'+w), wX=document.getElementById('ox-X-'+w);
  T('G3 틀린 카드 — 정답 칸(X) ring · 내 답 칸(O) 채움+line-through · 「✗ 틀림」', wX.classList.contains('ring-2')&&wX.classList.contains('ring-red-300')&&wX.classList.contains('border-red-600')&&!wX.classList.contains('bg-red-600')&&wO.classList.contains('bg-blue-700')&&wO.classList.contains('line-through')&&document.getElementById('ox-res-'+w).textContent==='✗ 틀림'&&document.getElementById('ox-res-'+w).classList.contains('text-red-600'), wO.className+' | '+wX.className);
  const v=ids[4], vO=document.getElementById('ox-O-'+v), vX=document.getElementById('ox-X-'+v);
  T('G3 틀린 카드(반대) — 정답 O ring-blue-300·border-blue-700 · 내 X 채움+줄', vO.classList.contains('ring-blue-300')&&vO.classList.contains('border-blue-700')&&vX.classList.contains('bg-red-600')&&vX.classList.contains('line-through'), vO.className+' | '+vX.className);
  const c=ids[0], cO=document.getElementById('ox-O-'+c);
  T('G3 맞은 카드 — 「✓ 맞음」(초록) · 고른 정답 칸 채움+ring · 줄 없음', document.getElementById('ox-res-'+c).textContent==='✓ 맞음'&&document.getElementById('ox-res-'+c).classList.contains('text-green-700')&&cO.classList.contains('bg-blue-700')&&cO.classList.contains('ring-2')&&!cO.classList.contains('line-through'), cO.className);
  T('G3 라디오 disabled', ids.every(id=>[...document.querySelectorAll(`input[name="answer_${id}"]`)].every(r=>r.disabled)));
  T('G3 채점 뒤 해설 저절로 펴짐 · 「정답·해설 ▾」', ids.every(id=>!document.getElementById('exp-'+id).classList.contains('hide')&&document.getElementById('peek-btn-'+id).textContent==='정답·해설 ▾'), J(ids.map(id=>document.getElementById('peek-btn-'+id).textContent)));
  renderQuizPage();
  T('G3 다시 그려도(채점 상태 복원) 같은 칠', document.getElementById('ox-O-'+w).classList.contains('line-through')&&document.getElementById('ox-X-'+w).classList.contains('ring-red-300')&&document.getElementById('ox-res-'+w).textContent==='✗ 틀림'&&document.getElementById('ox-res-'+c).textContent==='✓ 맞음');
}
async function G4(){
  if(!NEW){ T('G4 「정답·해설 ▸」 단추',false,'없음'); return; }
  resetLS({}); closeAllWins();
  const ids=UNIT.slice(0,3);
  openQuiz(ids,'민법총칙',CH);
  const u=ids[1], pb=document.getElementById('peek-btn-'+u), ex=document.getElementById('exp-'+u), pa=document.getElementById('peek-ans-'+u);
  pb.click();
  T('G4 채점 전 누르면 peek-ans 에 정답 + 해설 · 「▾」', !ex.classList.contains('hide')&&!pa.classList.contains('hide')&&/정답\s*X/.test(pa.textContent)&&pb.textContent==='정답·해설 ▾', pa.textContent+' · '+pb.textContent);
  pb.click();
  T('G4 다시 누르면 접힘 · 「▸」', ex.classList.contains('hide')&&pb.textContent==='정답·해설 ▸', pb.textContent);
  document.querySelectorAll('#quiz-container input[value="O"]').forEach(r=>r.checked=true);
  gradeCurrentPage();   /* 한 쪽뿐(마지막 쪽) — 창을 닫지 않는다 */
  pb.click();
  T('G4 채점 뒤 누르면 해설 접힘 · 정답 미리보기 줄 없음 · 「▸」', ex.classList.contains('hide')&&pa.classList.contains('hide')&&pb.textContent==='정답·해설 ▸', pb.textContent);
  pb.click();
  T('G4 채점 뒤 다시 누르면 펴짐 · 미리보기 줄은 여전히 없음 · 「▾」', !ex.classList.contains('hide')&&pa.classList.contains('hide')&&pb.textContent==='정답·해설 ▾', pb.textContent);
}
async function G5(){
  resetLS({}); closeAllWins();
  const ids=UNIT.slice(0,20);
  openQuiz(ids,'민법총칙',CH);
  T('G5 #omr-pad 덮개 0', !document.getElementById('omr-pad'));
  openOmrPad();
  const w=document.getElementById('oxwin-omr');
  const sub=document.getElementById('omr-sub');
  T('G5 oxwin-omr 창이 뜬다 · 제목 📝 OMR 마킹 · 부제 = 진행 글자', !!w&&w.querySelector('.oxwin-head').textContent.indexOf('📝 OMR 마킹')>=0&&!!sub&&sub.textContent===document.getElementById('progress-text').textContent.trim(), w?w.querySelector('.oxwin-head').textContent:'없음');
  if(!w) return;
  const h0=w.offsetHeight, wantH=Math.max(160,Math.min(420,innerHeight-120));
  T('G5 처음 높이 = min(420, 창높이-120) · 줄 20', Math.abs(h0-wantH)<=2&&document.querySelectorAll('#omr-rows [id^="omr-row-"]').length===20, h0+' vs '+wantH);
  const gbtn=w.querySelector('button[onclick="omrGrade()"]');
  T('G5 「키보드 O / X」 글자 없음 · 아랫줄 「마킹 N/총」·「채점 ✓」', w.textContent.indexOf('키보드 O / X')<0&&!!gbtn&&gbtn.textContent==='채점 ✓'&&document.getElementById('omr-count').textContent.replace(/\s/g,'')==='마킹0/20');
  const body=w.querySelector('.oxwin-body');
  T('G5 줄이 많으면 창 안에서 스크롤(.oxwin-body overflow auto)', getComputedStyle(body).overflowY==='auto'&&body.scrollHeight>body.clientHeight, getComputedStyle(body).overflowY+' · '+body.scrollHeight+'/'+body.clientHeight);
  const g=w.querySelector('.oxwin-grip'), gr=g.getBoundingClientRect();
  g.dispatchEvent(new MouseEvent('mousedown',{bubbles:true,cancelable:true,clientX:gr.left+5,clientY:gr.top+5}));
  window.dispatchEvent(new MouseEvent('mousemove',{clientX:gr.left+45,clientY:gr.top+65}));
  window.dispatchEvent(new MouseEvent('mouseup',{clientX:gr.left+45,clientY:gr.top+65}));
  const sv=JSON.parse(localStorage.getItem('oxwin.size.omr')||'null');
  T('G5 모서리로 크기 → oxwin.size.omr 저장', !!sv&&sv.w===w.offsetWidth&&sv.h===w.offsetHeight&&Math.abs(sv.h-(h0+60))<=2, J(sv)+' · '+w.offsetWidth+'×'+w.offsetHeight);
  const hd=w.querySelector('.oxwin-head'), hr=hd.getBoundingClientRect(), left0=w.getBoundingClientRect().left;
  hd.dispatchEvent(new MouseEvent('mousedown',{bubbles:true,cancelable:true,clientX:hr.left+40,clientY:hr.top+8}));
  window.dispatchEvent(new MouseEvent('mousemove',{clientX:hr.left+140,clientY:hr.top+48}));
  window.dispatchEvent(new MouseEvent('mouseup',{}));
  T('G5 제목 줄 잡고 끌기', Math.round(w.getBoundingClientRect().left-left0)===100, w.getBoundingClientRect().left-left0);
  closeOmrPad();
  T('G5 닫기 = oxWinClose(omr)', !document.getElementById('oxwin-omr'));
  openOmrPad();
  const w2=document.getElementById('oxwin-omr');
  T('G5 다시 열면 그 크기', !!w2&&!!sv&&w2.offsetWidth===sv.w&&w2.offsetHeight===sv.h, w2?w2.offsetWidth+'×'+w2.offsetHeight:'없음');
  document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'o',bubbles:true,cancelable:true}));
  T('G5 키보드 O → .omr-cur 줄(첫 문항) 마킹 · 카드 라디오 · 카드 색', document.querySelector(`input[name="answer_${ids[0]}"][value="O"]`).checked&&document.getElementById('ox-O-'+ids[0]).classList.contains('bg-blue-700'));
  const oc=document.getElementById('omr-count').textContent.replace(/\s/g,'');
  T('G5 창 「마킹 N/총」 = 오른쪽 아래 알약 수', oc==='마킹'+mc()&&mc()==='1/20', oc+' vs '+mc());
  const qp=document.querySelector('#q-box-'+ids[5]+' [data-mark]'); qp.scrollIntoView({block:'center'});
  const qr=qp.getBoundingClientRect(), wr=w2.getBoundingClientRect();
  let x=qr.left+4, y=qr.top+Math.min(8,qr.height/2);
  if(x>=wr.left&&x<=wr.right&&y>=wr.top&&y<=wr.bottom) x=qr.right-4;
  const top=document.elementFromPoint(x,y);
  T('G5 창 띄운 채 카드 지문이 맨 위(뒤 덮개 없음)', !!top&&(qp===top||qp.contains(top)), (top&&(top.id||top.tagName))+' @'+Math.round(x)+','+Math.round(y));
  ids.forEach(id=>{ if(!document.querySelector(`input[name="answer_${id}"]:checked`)) document.querySelector(`input[name="answer_${id}"][value="X"]`).checked=true; });
  w2.querySelector('button[onclick="omrGrade()"]').click();
  T('G5 「채점 ✓」 = omrGrade(창 닫고 이 쪽 채점)', !document.getElementById('oxwin-omr')&&Object.keys(currentSessionMarks).length===20, Object.keys(currentSessionMarks).length);
  try{ closeGradeModal(); }catch(e){}
}
