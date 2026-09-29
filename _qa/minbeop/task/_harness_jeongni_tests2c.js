
const textRange=(el)=>{ const tw=document.createTreeWalker(el,NodeFilter.SHOW_TEXT); const ts=[]; let nd; while((nd=tw.nextNode())) ts.push(nd); const rg=document.createRange(); rg.setStart(ts[0],0); rg.setEnd(ts[ts.length-1],ts[ts.length-1].length); return rg; };
const selectRange=rg=>{ const sel=window.getSelection(); sel.removeAllRanges(); sel.addRange(rg); document.dispatchEvent(new MouseEvent('mouseup',{bubbles:true})); };
async function G12(){
  if(!NEW){ T('G12 정리 창(openJeongni)이 있다',false,'없음'); return; }
  resetLS({ox_q_marks:{'q-Q9901':[[2,6,'y']],'e-Q9901':[[0,4,'u']]}});
  closeAllWins();
  openQuiz(['Q9901','Q9902'],'민법총칙',CH);
  jnMarksOn=true;
  openJeongni('민법총칙','1.1');
  const w=jnWin();
  const jq=w&&w.querySelector('[data-mark="q-Q9901"]'), je=w&&w.querySelector('[data-mark="e-Q9901"]');
  const cq=document.querySelector('#q-box-Q9901 [data-mark="q-Q9901"]'), ce=document.querySelector('#q-box-Q9901 [data-mark="e-Q9901"]');
  T('G12 범위 둔 문항 — 정리 창 지문·해설 innerHTML = 카드와 같다(<span style> 조각)', !!jq&&!!je&&!!cq&&!!ce&&jq.innerHTML===cq.innerHTML&&je.innerHTML===ce.innerHTML&&/<span style=/.test(jq.innerHTML)&&/<span style=/.test(je.innerHTML), jq?jq.innerHTML.slice(0,120)+' | '+(cq&&cq.innerHTML.slice(0,120)):'없음');
  if(!jq||!cq) { closeAllWins(); showHome(); return; }
  T('G12 data-text 도 카드와 같다', jq.getAttribute('data-text')===cq.getAttribute('data-text')&&je.getAttribute('data-text')===ce.getAttribute('data-text'));
  const q2=w.querySelector('[data-mark="q-Q9902"]');
  T('G12 범위 없는 문항은 평문(span 없음)', !!q2&&q2.children.length===0&&q2.textContent===quizData.find(x=>x.id==='Q9902').q);
  T('G12 &amp;lt; 0건 · 해설 꺾쇠는 글자로 보인다', w.innerHTML.indexOf('&amp;lt;')<0&&je.textContent.indexOf('<b>꺾쇠</b>')>=0, je.innerHTML.slice(0,160));
  localStorage.setItem('ox_q_marks','{}');
  document.querySelectorAll('[data-mark="q-Q9901"]').forEach(h=>h.innerHTML=renderMarked(h.getAttribute('data-text'),null));
  const bar=document.getElementById('mark-bar'); bar.classList.add('hide');
  const jq1=w.querySelector('[data-mark="q-Q9901"]');
  jq1.scrollIntoView({block:'center'});
  const rg=document.createRange(); rg.setStart(jq1.firstChild,3); rg.setEnd(jq1.firstChild,9); selectRange(rg);
  const shown=!bar.classList.contains('hide');
  const br=bar.getBoundingClientRect(), cx=br.left+br.width/2, cy=br.top+br.height/2;
  const top=document.elementFromPoint(cx,cy);
  const inWin=(()=>{ const r=w.getBoundingClientRect(); return cx>=r.left&&cx<=r.right&&cy>=r.top&&cy<=r.bottom; })();
  T('G12 정리 창 지문에서 글자 선택 → #mark-bar 뜸 · 창 위에 보인다(elementFromPoint = 툴바)', shown&&!!top&&bar.contains(top), 'shown '+shown+' · top '+(top&&(top.id||top.tagName))+' · bar z '+getComputedStyle(bar).zIndex+' · 창 z '+w.style.zIndex+' · 툴바 가운데가 창 안 '+inWin);
  const oldZ=bar.style.zIndex; bar.style.zIndex=''; const top0=document.elementFromPoint(cx,cy); bar.style.zIndex=oldZ;
  say('G12 헛잣대 — 인라인 z-index 를 걷으면(z-[60]) 툴바 가운데 맨 위 = '+(top0?(bar.contains(top0)?'툴바':(top0.closest('.oxwin')?'정리 창(가려짐)':top0.tagName)):'없음')+' · 툴바 가운데가 창 안 '+inWin);
  applyMark('y');
  const m=lsO('ox_q_marks')['q-Q9901']||[];
  T('G12 applyMark(y) → ox_q_marks[q-Q9901] 1건 [3,9,y]', J(m)===J([[3,9,'y']]), J(m));
  const jq2=w.querySelector('[data-mark="q-Q9901"]'), cq2=document.querySelector('#q-box-Q9901 [data-mark="q-Q9901"]');
  T('G12 정리 행에 #fde68a span · 같은 uid 카드도 같이 바뀜', /#fde68a/.test(jq2.innerHTML)&&/#fde68a/.test(cq2.innerHTML)&&jq2.innerHTML===cq2.innerHTML, jq2.innerHTML.slice(0,120)+' | '+cq2.innerHTML.slice(0,120));
  selectRange(textRange(jq2));
  applyMark('');
  T("G12 지우개('') — 저장소에서 빠지고 정리 행·카드 둘 다 평문", !lsO('ox_q_marks')['q-Q9901']&&!/<span/.test(w.querySelector('[data-mark="q-Q9901"]').innerHTML)&&!/<span/.test(document.querySelector('#q-box-Q9901 [data-mark="q-Q9901"]').innerHTML), J(lsO('ox_q_marks')));
  window.getSelection().removeAllRanges();
  closeAllWins(); showHome();
}
async function G13(){
  if(!NEW){ T('G13 정리 창 토글이 있다',false,'없음'); return; }
  resetLS({ox_q_marks:{'q-Q9901':[[2,6,'y']]}});
  closeAllWins();
  openQuiz(['Q9901','Q9902'],'민법총칙',CH);
  jnMarksOn=true;
  openJeongni('민법총칙','1.1');
  const w=jnWin(), tb=w.querySelector('[data-jnmarks]');
  const cardMarks=()=>document.querySelectorAll('#quiz-container [data-mark]').length;
  const c0=cardMarks();
  tb.click();
  const qd=w.querySelector('[data-jnrow="Q9901"]').children[1];
  T('G13 끄면 행에 data-mark 0건 · 평문 · 단추 꺼짐 색', jnMarksOn===false&&w.querySelectorAll('[data-mark]').length===0&&w.querySelectorAll('[data-jnrow]').length===5&&qd.children.length===0&&tb.classList.contains('text-gray-500'), 'data-mark '+w.querySelectorAll('[data-mark]').length+' · '+qd.innerHTML.slice(0,80));
  const bar=document.getElementById('mark-bar'); bar.classList.add('hide');
  const rg=document.createRange(); rg.setStart(qd.firstChild,1); rg.setEnd(qd.firstChild,5); selectRange(rg);
  T('G13 꺼진 창에서 긁어도 #mark-bar 안 뜸', bar.classList.contains('hide'));
  window.getSelection().removeAllRanges();
  T('G13 카드 쪽 data-mark 는 그대로', c0>0&&cardMarks()===c0, c0+' → '+cardMarks());
  tb.click();
  T('G13 다시 켜면 돌아온다(data-mark 10 · span)', jnMarksOn===true&&w.querySelectorAll('[data-mark]').length===10&&/#fde68a/.test(w.querySelector('[data-mark="q-Q9901"]').innerHTML)&&tb.classList.contains('text-amber-800'), w.querySelectorAll('[data-mark]').length);
  T('G13 토글 값은 저장소에 안 남는다(키 이름 대조)', Object.keys(localStorage).every(k=>!/jn|mark.?on|표시/i.test(k)), J(Object.keys(localStorage)));
  closeAllWins(); showHome();
}
async function G14(){
  const ck='민법총칙||'+CH+'||all||all', ck2='민법총칙||'+CH2+'||all||all';
  const hist={}; hist[ck]=[{score:38,total:43,date:'2026. 9. 15.',marks:{Q9901:true}}];
  const prog={}; prog[ck]={pageIndex:0,score:1,marks:{Q9901:true,Q9902:false},picks:{Q9903:'O'},total:4,date:'2026. 9. 15.'};
  prog[ck2]={pageIndex:0,score:0,marks:{Q9904:true},picks:{},total:1,date:'2026. 9. 15.'};
  resetLS({ox_chap_history:hist,ox_in_progress:prog});
  loadQuiz(); showHome(); closeAllWins();
  currentSubject=null; currentChapterLabel=null;
  renderDashboard();
  const sel='[onclick^="event.stopPropagation();discardInProgress("]';
  const xOf=l=>{ const r=trow(l); return r?r.querySelector(sel):null; };
  const x1=xOf(CH);
  T('G14 진행중 배지 바로 뒤에 × · 진행중 없는 단원엔 × 0', !!x1&&x1.textContent==='×'&&!!x1.previousElementSibling&&/회독 진행중/.test(x1.previousElementSibling.textContent)&&!xOf(CH7)&&document.querySelectorAll(sel).length===2, 'x1 '+!!x1+' · 전체 '+document.querySelectorAll(sel).length);
  if(!x1) return;
  window.__CONFIRM_ANS=false; const n0=__CONFIRMS.length;
  const before=[localStorage.getItem('ox_in_progress'),localStorage.getItem('ox_chap_history')];
  x1.click();
  T('G14 확인창 글 — 회독 수(2)·채점 수(3/4)·기록 수(1)', __CONFIRMS.length===n0+1&&__CONFIRMS[n0]===('「'+CH+'」 진행중 2회독(3/4)을 버립니다.\n회독 기록(1건)과 문항 채점은 그대로입니다.'), __CONFIRMS[n0]);
  T('G14 아니오 → 아무것도 안 바뀜', localStorage.getItem('ox_in_progress')===before[0]&&localStorage.getItem('ox_chap_history')===before[1]&&!!xOf(CH));
  stampAll();                                              /* 그림자 = 지금 저장소 */
  window.__CONFIRM_ANS=true;
  currentSubject='민법총칙'; currentChapterLabel=CH; currentSessionMarks={Q9901:true}; currentSessionScore=1; currentPageIndex=2; resumePicks={Q9903:'O'};
  xOf(CH).click();
  const ip=lsO('ox_in_progress');
  T('G14 예 → 그 칸만 사라짐(다른 단원 진행중 그대로) · 회독 기록 그대로', !(ck in ip)&&(ck2 in ip)&&localStorage.getItem('ox_chap_history')===before[1], J(Object.keys(ip)));
  T('G14 배지·× 사라짐', !!trow(CH)&&!xOf(CH)&&!/회독 진행중/.test(trow(CH).textContent), trow(CH)?trow(CH).textContent.replace(/\s+/g,' ').slice(0,120):'행 없음');
  T('G14 그 단원이 세션으로 잡혀 있었으면 세션도 비움', J(currentSessionMarks)==='{}'&&currentSessionScore===0&&currentPageIndex===0&&J(resumePicks)==='{}');
  const t0=Date.now(); stampAll(); const t1=Date.now();
  const GK=(typeof GONE_KEY!=='undefined')?GONE_KEY:'ox_sync_gone', gone=lsO(GK), gk='ox_in_progress|'+ck;
  T('G14 stampAll → ox_sync_gone 에 ox_in_progress|<chapKey> 묘비(지금 시각)', GK==='ox_sync_gone'&&typeof gone[gk]==='number'&&gone[gk]>=t0&&gone[gk]<=t1&&!(('ox_in_progress|'+ck2) in gone), J(gone));
  currentSubject=null; currentChapterLabel=null; currentSessionMarks={}; currentSessionScore=0; resumePicks={};
}
async function G15(){
  resetLS({ox_q_geunge:{Q9901:[gItem('g_Q9901_1',1,'근거 하나'),gItem('g_Q9901_2',2,'근거 둘'),gItem('g_Q9901_3',3,'근거 셋')]},ox_q_reflinks:{Q9902:{geunge:['Q9901']}}});
  closeAllWins();
  openQuiz(['Q9901','Q9902'],'민법총칙',CH);
  openQPopup('Q9901');
  const chipTxt=sc=>{ const b=document.getElementById(sc+'gg-chips-Q9901'); return b?[...b.children].map(x=>x.textContent):null; };
  window.__CONFIRM_ANS=true;
  ggDel('Q9901','g_Q9901_2','qp-');
  const st=ggOf('Q9901');
  T('G15 2를 지우면 저장소 i 1·2 · k 는 남은 둘 그대로', J(st.map(g=>[g.i,g.k]))===J([[1,'g_Q9901_1'],[2,'g_Q9901_3']]), J(st.map(g=>[g.i,g.k])));
  T('G15 칩 글자 1·2 — 카드와 문항 팝업 둘 다', J(chipTxt(''))===J(['1','2'])&&J(chipTxt('qp-'))===J(['1','2']), J([chipTxt(''),chipTxt('qp-')]));
  T('G15 지운 항목의 k 를 가리키는 id 0(두 범위)', !document.querySelector('[id*="g_Q9901_2"]'), [...document.querySelectorAll('[id*="g_Q9901_2"]')].map(x=>x.id).join(','));
  const tv=document.getElementById('gg-t-Q9901-g_Q9901_3'), pv=document.getElementById('qp-gg-t-Q9901-g_Q9901_3');
  T('G15 남은 판 id 는 k 그대로 · 글자 그대로(두 범위)', !!tv&&!!pv&&tv.textContent==='근거 셋'&&pv.textContent==='근거 셋');
  const txt=refTextOf('Q9901','geunge');
  T('G15 refTextOf 「i. 본문」도 1·2', txt==='1. 근거 하나\n2. 근거 셋', txt);
  const rr=document.createElement('div'); rr.innerHTML=ggRefBoxHTML('Q9902');
  const nums=[...rr.querySelectorAll('.flex-none.font-extrabold')].map(x=>x.textContent);
  T('G15 연결한 쪽(ggRefRowHTML)에서도 1. 2. · 지운 k 없음', J(nums)===J(['1.','2.'])&&rr.innerHTML.indexOf('g_Q9901_2')<0, J(nums));
  const ob=document.getElementById('reflink-geunge-Q9902'), onums=ob?[...ob.querySelectorAll('.flex-none.font-extrabold')].map(x=>x.textContent):null;
  T('G15 화면에 떠 있던 연결한 쪽 상자(Q9902 카드)도 1. 2.', J(onums)===J(['1.','2.']), J(onums));
  const inp=document.getElementById('gg-in-Q9901'); inp.value='근거 넷'; key(inp,'Enter');
  const st2=ggOf('Q9901');
  T('G15 다시 더하면 i 3 · 앞 둘 k 그대로', J(st2.map(g=>g.i))===J([1,2,3])&&st2[0].k==='g_Q9901_1'&&st2[1].k==='g_Q9901_3', J(st2.map(g=>[g.i,g.k])));
  T('G15 더한 뒤 카드·팝업 칩 1·2·3', J(chipTxt(''))===J(['1','2','3'])&&J(chipTxt('qp-'))===J(['1','2','3']), J([chipTxt(''),chipTxt('qp-')]));
  resetLS({ox_q_geunge:{Q9902:[gItem('g_Q9902_x',2,'옛 둘')]}});
  closeAllWins();
  openQuiz(['Q9902'],'민법총칙',CH);
  const i2=document.getElementById('gg-in-Q9902'); i2.value='새 근거'; key(i2,'Enter');
  const st3=ggOf('Q9902'), ch3=document.getElementById('gg-chips-Q9902');
  T('G15 「2」만 남은 옛 문항에 더하면 1·2(2·2 아님) · 옛 k 그대로 · 칩도', J(st3.map(g=>g.i))===J([1,2])&&st3[0].k==='g_Q9902_x'&&!!ch3&&J([...ch3.children].map(x=>x.textContent))===J(['1','2']), J(st3.map(g=>[g.i,g.k])));
  closeAllWins(); showHome();
}
const LIST=[['G1',G1],['G2',G2],['G3',G3],['G4',G4],['G5',G5],['G6',G6],['G7',G7],['G8',G8],['G12',G12],['G13',G13],['G14',G14],['G15',G15],['G9',G9]].filter(x=>P.skip.indexOf(x[0])<0);
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
  T('G9 헤드리스 페이지 오류 0 · console.error 0', errs.length===0&&cerr.length===0, 'error '+errs.length+' '+errs.slice(0,3).join(' / ')+' · console.error '+cerr.length+' '+cerr.slice(0,3).join(' / '));
  say('alert '+__ALERTS.length+'번 : '+__ALERTS.slice(0,3).join(' / ')+' · confirm '+__CONFIRMS.length+'번');
  R.forEach(x=>console.log('HZR|'+encodeURIComponent(x)));
  console.log('HZR|END');
},1500);
})();
