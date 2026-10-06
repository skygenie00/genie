
const winBtn=(w,t)=>w?[...w.querySelectorAll('button')].find(b=>b.textContent.trim()===t):null;
const headClose=w=>w?[...w.querySelectorAll('.oxwin-head button')].find(b=>b.textContent.trim()==='닫기'):null;
async function G13(){
  resetLS({}); closeAllWins();
  openQuiz(UNIT,'민법총칙',CH);
  document.querySelectorAll('#quiz-container input[value="O"]').forEach(r=>r.checked=true);
  gradeCurrentPage();
  const w=document.getElementById('oxwin-grade');
  T('G13 중간 쪽 채점 → oxwin-grade 뜸 · #grade-modal 0', !!w&&!document.getElementById('grade-modal'), 'win '+!!w+' · modal '+!!document.getElementById('grade-modal'));
  if(!w){ try{ closeGradeModal(); }catch(e){} showHome(); return; }
  const tx=w.textContent;
  T('G13 점수 한 줄(10 / 20 · 50%) · 「🎉」「이전 회독 기록이 없어」「확인」「회독 저장됨」 0', /10 \/ 20/.test(tx)&&/50%/.test(tx)&&tx.indexOf('🎉')<0&&tx.indexOf('이전 회독 기록이 없어')<0&&tx.indexOf('확인')<0&&tx.indexOf('회독 저장됨')<0, tx.slice(0,160));
  const chip=[...w.querySelectorAll('button')].find(b=>/^openQPopup\(/.test(b.getAttribute('onclick')||''));
  if(chip) chip.click();
  T('G13 번호 칸 누르면 openQPopup(문항 팝업)', !!chip&&!!document.querySelector('.oxwin[id^="oxwin-q-"]'), chip?chip.getAttribute('onclick'):'번호 칸 없음');
  document.querySelectorAll('.oxwin[id^="oxwin-q-"]').forEach(x=>x.remove());
  const nb=winBtn(w,'다음 ▶');
  T('G13 아랫줄 「다음 ▶」 회색 글자(채움 없음) → goNextPage', !!nb&&/goNextPage\(\)/.test(nb.getAttribute('onclick')||'')&&nb.classList.contains('text-gray-600')&&!/\bbg-blue-600\b/.test(nb.className), nb?nb.outerHTML.slice(0,200):'없음');
  headClose(w).click();
  T('G13 ✕(닫기)는 창만 닫힘 — 카드에 남는다 · 아래 막대가 보인다', !document.getElementById('oxwin-grade')&&!document.getElementById('quiz-screen').classList.contains('hide')&&!!document.getElementById('q-box-'+UNIT[0])&&!document.getElementById('reopen-grade-bar').classList.contains('hide'));
  const rbtn=[...document.getElementById('reopen-grade-bar').querySelectorAll('button')];
  T('G13 막대 「📊 채점」(파스텔 파랑 글자) · 「다음」(회색 글자)', rbtn.length===2&&rbtn[0].textContent.trim()==='📊 채점'&&rbtn[0].classList.contains('text-blue-500')&&rbtn[1].textContent.trim()==='다음'&&rbtn[1].classList.contains('text-gray-600')&&!rbtn[1].classList.contains('hide'), rbtn.map(b=>b.textContent.trim()+':'+b.className).join(' | '));
  rbtn[0].click();
  const w2=document.getElementById('oxwin-grade');
  T('G13 「📊 채점」으로 다시 열림', !!w2);
  const nb2=winBtn(w2,'다음 ▶'); if(nb2) nb2.click();
  T('G13 「다음 ▶」 → 다음 쪽 · 창 닫힘', !document.getElementById('oxwin-grade')&&currentPageIndex===1&&!!document.getElementById('q-box-'+UNIT[20]));
  showHome();
}
async function G14(){
  resetLS({}); closeAllWins();
  const ids=UNIT.slice(0,5), ck='민법총칙||'+CH+'||all||all';
  openQuiz(ids,'민법총칙',CH);
  document.querySelectorAll('#quiz-container input[value="O"]').forEach(r=>r.checked=true);
  gradeCurrentPage();
  const h=lsO('ox_chap_history')[ck]||[], e=h[h.length-1]||{};
  T('G14 마지막 쪽 채점 → ox_chap_history[chapKey] 에 1건 바로(cf·labels 포함)', h.length===1&&!!e.cf&&!!e.labels&&J(Object.keys(e.marks||{}).sort())===J(ids.slice().sort()), J(h).slice(0,200));
  const u=lsO('ox_sync_u');
  T('G14 회독 칸 도장 찍힘(ox_sync_u 에 ox_chap_history|chapKey)', typeof u['ox_chap_history|'+ck]==='number', J(Object.keys(u).filter(k=>/^ox_chap_history/.test(k))));
  T('G14 ox_in_progress 에 그 칸 없음', !(ck in lsO('ox_in_progress')));
  const w=document.getElementById('oxwin-grade');
  T('G14 창에 「✓ 회독 저장됨」 · 아랫줄(다음 ▶) 없음', !!w&&w.textContent.indexOf('✓ 회독 저장됨')>=0&&!winBtn(w,'다음 ▶'), w?w.textContent.slice(0,120):'창 없음');
  T('G14 #action-btn 글자에 「🏆」 0 · 아래 막대 「다음」 숨김', document.getElementById('action-btn').textContent.indexOf('🏆')<0&&document.getElementById('reopen-next-btn').classList.contains('hide'), document.getElementById('action-btn').textContent);
  try{ progFlush(); }catch(err){} try{ saveInProgress(ck); }catch(err){}
  document.dispatchEvent(new Event('visibilitychange'));
  T('G14 progFlush·saveInProgress·visibilitychange 를 억지로 돌려도 ox_in_progress 안 생김', !(ck in lsO('ox_in_progress')), J(lsO('ox_in_progress')));
  const x=headClose(w); if(x) x.click();
  T('G14 ✕ → 첫 화면 · 세션 비움', !document.getElementById('home-screen').classList.contains('hide')&&document.getElementById('quiz-screen').classList.contains('hide')&&J(currentSessionMarks)==='{}'&&!(ck in lsO('ox_in_progress')));
  openQuiz(ids,'민법총칙',CH);
  document.querySelectorAll('#quiz-container input[value="X"]').forEach(r=>r.checked=true);
  gradeCurrentPage();
  T('G14 다시 열어 마지막 쪽 채점 → 새 회독 1건(=2회독)', (lsO('ox_chap_history')[ck]||[]).length===2, (lsO('ox_chap_history')[ck]||[]).length);
  goHome();
  T('G14 「🏠 목록」(goHome)도 저장된 회독이면 세션을 비우고 간다 · 진행중 안 생김', !document.getElementById('home-screen').classList.contains('hide')&&J(currentSessionMarks)==='{}'&&!(ck in lsO('ox_in_progress'))&&(lsO('ox_chap_history')[ck]||[]).length===2);
  resetLS({}); loadQuiz(); showHome(); closeAllWins();
  startQuiz('변리사 기출','2016년 제53회');
  currentFilteredData.forEach(it=>{ resumePicks[String(it.id)]='O'; });
  gradeAllExam();
  const ek='변리사 기출||2016년 제53회||all||all', eh=lsO('ox_chap_history')[ek]||[], ew=document.getElementById('oxwin-grade');
  T('G14 기출 전체 채점도 채점과 함께 저장 · 창 「✓ 회독 저장됨」 · 🏆 0', eh.length===1&&!!ew&&ew.textContent.indexOf('✓ 회독 저장됨')>=0&&document.getElementById('action-btn').textContent.indexOf('🏆')<0, 'hist '+eh.length+' · win '+!!ew);
  if(ew) closeGradeModal();
  T('G14 기출 창 닫기 → 첫 화면', !document.getElementById('home-screen').classList.contains('hide'));
}
async function G15(){
  resetLS({}); closeAllWins();
  openQuiz(UNIT,'민법총칙',CH);
  const ab=document.getElementById('action-btn'), sk=document.getElementById('skip-next-btn');
  T('G15 「채점 ✓」 파스텔 파랑 글자 · 「다음 ▶」 회색 글자(둘 다 채움 없음)', ab.classList.contains('text-blue-500')&&sk.classList.contains('text-gray-600')&&!/\bbg-blue-600\b|\bbg-gray-100\b/.test(ab.className+' '+sk.className), ab.className+' | '+sk.className);
  openOmrPad();
  document.querySelectorAll('#quiz-container input[value="O"]').forEach(r=>r.checked=true);
  renderOmrPad();
  const og=document.querySelector('#oxwin-omr button[onclick="omrGrade()"]');
  T('G15 OMR 창 「채점 ✓」 파스텔 파랑 글자', !!og&&og.classList.contains('text-blue-500')&&!/\bbg-blue-600\b/.test(og.className), og?og.className:'없음');
  gradeCurrentPage();
  const zones=['controls-container','reopen-grade-bar','exam-prev-bar','oxwin-omr','oxwin-grade'].map(id=>document.getElementById(id)).filter(Boolean);
  const blue=zones.flatMap(z=>[...z.querySelectorAll('*')].filter(b=>/\bbg-blue-600\b/.test(b.getAttribute('class')||'')));
  T('G15 아래 막대·OMR 창·채점 창에 bg-blue-600 0', zones.length===5&&blue.length===0, zones.map(z=>z.id).join(',')+' · '+blue.map(b=>b.outerHTML.slice(0,90)).join(' | '));
  say('G15 (참고) 그 밖의 bg-blue-600 '+[...document.querySelectorAll('*')].filter(b=>/\bbg-blue-600\b/.test(b.getAttribute('class')||'')).length+'개(그대로 둔 자리)');
  try{ closeGradeModal(); }catch(e){} closeAllWins(); showHome();
}
async function G16(){
  const ck='민법총칙||'+CH+'||all||all', prog={}; prog[ck]={pageIndex:0,score:0,marks:{},picks:{Q9801:'O'},total:25,date:'2026. 9. 15.'};
  resetLS({ox_in_progress:prog}); loadQuiz(); showHome(); closeAllWins();
  renderDashboard();
  const btns=[...document.querySelectorAll('#dashboard-container button[onclick^="startQuiz("]')];
  T('G16 목차 줄 단추 글자 = N회독 / 이어서 뿐(「시작」「풀기」 0)', btns.length>0&&btns.every(b=>/^(\d+회독|이어서)$/.test(b.textContent.trim())), J(btns.map(b=>b.textContent.trim())));
  T('G16 채움(bg-blue-600·bg-amber-500) 0 · title 에 옛 글자', btns.every(b=>!/\bbg-blue-600\b|\bbg-amber-500\b/.test(b.className)&&/회독 시작|이어서 풀기/.test(b.title)), J(btns.map(b=>b.title)));
  const rb=trow(CH)&&trow(CH).querySelector('button[onclick^="startQuiz("]');
  T('G16 진행중 줄 = 주황 글자 「이어서」 · onclick 그대로', !!rb&&rb.textContent.trim()==='이어서'&&rb.classList.contains('text-amber-600')&&rb.getAttribute('onclick')==="startQuiz('민법총칙', '"+CH+"')", rb?rb.outerHTML.slice(0,220):'없음');
  const r2=trow('1. 총칙 > 2.1 기출'), b2=r2&&r2.querySelector('button[onclick^="startQuiz("]');
  T('G16 진행중 아닌 줄 = 파스텔 파랑 「1회독」', !!b2&&b2.textContent.trim()==='1회독'&&b2.classList.contains('text-blue-500'), b2?b2.outerHTML.slice(0,200):'없음');
}
async function G17(){
  resetLS({}); loadQuiz(); showHome(); closeAllWins();
  renderDashboard();
  const h2=()=>[...document.querySelectorAll('#dashboard-container h2')].map(h=>{ const c=h.cloneNode(true); c.querySelectorAll('[data-dfoldbtn]').forEach(e=>e.remove()); return c.textContent.replace(/\s+/g,' ').trim(); });   /* ★ 2026-10-06 (_task_ox_home_tidy §A-5) — 과목 이름 바로 뒤 [N] 접기 단추(h2 안)는 빼고 읽음 */
  T('G17 과목 제목에 📚 0 · 이 하네스 데이터 두 과목 = Ⅰ 민법총칙 · Ⅱ 변리사 기출', J(h2())===J(['Ⅰ 민법총칙','Ⅱ 변리사 기출']), J(h2()));
  quizData.length=0;
  ['민법총칙','물권법','채권총론','채권각론','미분별 문제'].forEach((s,i)=>quizData.push(Object.assign(JSON.parse(J(P.quiz[0])),{id:'QR'+i,subject:s})));
  quizData.push(JSON.parse(J(P.quiz.find(q=>q.examNo))));
  renderDashboard();
  T('G17 미분별 문제만 숫자 없음 · Ⅰ 민법총칙 Ⅱ 물권법 Ⅲ 채권총론 Ⅳ 채권각론 Ⅴ 변리사 기출', J(h2())===J(['미분별 문제','Ⅰ 민법총칙','Ⅱ 물권법','Ⅲ 채권총론','Ⅳ 채권각론','Ⅴ 변리사 기출']), J(h2()));
  const sp=document.querySelector('#dashboard-container h2 span');
  T('G17 로마 숫자는 유니코드 한 글자(U+2160~) · 파랑 굵게', !!sp&&/^[Ⅰ-Ⅻ]$/.test(sp.textContent)&&sp.classList.contains('text-blue-600')&&sp.classList.contains('font-black'), sp?sp.outerHTML:'없음');
  localStorage.setItem('ox_q_tags', J({QR1:{fake:true}}));
  const rf=document.getElementById('review-filter'); rf.value='fake'; renderDashboard();
  T('G17 필터로 한 과목만 남아도 번호는 그대로(Ⅱ 물권법)', J(h2())===J(['Ⅱ 물권법']), J(h2()));
  rf.value='all'; resetLS({}); loadQuiz(); renderDashboard();
}
async function G18(){
  resetLS({}); loadQuiz(); showHome(); closeAllWins();
  const sf=document.getElementById('source-filter'), ds=document.getElementById('dash-sort'), rf=document.getElementById('review-filter');
  const hs=document.getElementById('home-screen');   /* body.textContent 는 이 시험 글(script)까지 담는다 — 첫 화면 안만 본다 */
  T('G18 옛 필터 줄 DOM 없음(첫 화면에 「🎯 기출 출처」「↕ 단원 정렬」 0 · 라벨 달린 select 0)', hs.textContent.indexOf('🎯 기출 출처')<0&&hs.textContent.indexOf('↕ 단원 정렬')<0&&![...hs.querySelectorAll('label')].some(l=>/기출 출처|약점 복습 필터|단원 정렬/.test(l.textContent)), [...hs.querySelectorAll('label')].map(l=>l.textContent.trim()).join(' | ').slice(0,200));
  T('G18 #source-filter·#dash-sort = hide · 값 all/toc · 옵션 하나씩', !!sf&&!!ds&&sf.classList.contains('hide')&&ds.classList.contains('hide')&&sf.value==='all'&&ds.value==='toc'&&sf.options.length===1&&ds.options.length===1, sf?sf.outerHTML.slice(0,120):'없음');
  const q=document.querySelector('button[onclick="startWeakQueue()"]'), qrow=q&&q.parentElement;
  T('G18 #review-filter 는 ⚡ 줄 안 · 옵션 6 · 「필터」 라벨', !!rf&&!!qrow&&qrow.contains(rf)&&J([...rf.options].map(o=>o.value))===J(['all','fake','concept','memo','important','wrong3'])&&/필터/.test(rf.parentElement.textContent), rf?J([...rf.options].map(o=>o.value)):'없음');
  const keys={}; ['all','wrong3','fake'].forEach(v=>{ rf.value=v; keys[v]=chapKeyOf('민법총칙',CH); });
  V('G18.chapKey', keys);
  rf.value='all';
  const hist={}; hist['민법총칙||'+CH+'||all||all']=[{score:1,total:2,date:'2026. 9. 1.',marks:{Q9801:false}}];
  resetLS({ox_chap_history:hist}); renderDashboard();
  T('G18 옛 회독 기록(||all||all)이 목차 줄에 그대로(1회독 칩)', !!trow(CH)&&/1회독/.test(trow(CH).textContent), trow(CH)?trow(CH).textContent.replace(/\s+/g,' ').slice(0,120):'없음');
  const h3={}; h3['민법총칙||'+CH+'||all||all']=[1,2,3].map(n=>({score:0,total:1,date:'2026. 9. '+n+'.',marks:{Q9802:false}}));
  resetLS({ox_chap_history:h3}); clearWrongCache(); rf.value='wrong3'; renderDashboard();
  const rows=[...document.querySelectorAll('[data-trrow]')].map(r=>r.getAttribute('data-trrow'));
  T('G18 wrong3 → 3번 이상 틀린 문항이 있는 단원만', J(rows)===J(['민법총칙|||'+CH]), J(rows));
  rf.value='all'; renderDashboard();
}
async function G19(){
  const ck='민법총칙||'+CH+'||all||all', qk='⚡빠른실행||🔥 약점 (틀림+헷갈림)||all||all';
  const hist={}; hist[ck]=[{score:0,total:1,date:'2026. 9. 1.',marks:{Q9801:false}},{score:0,total:1,date:'2026. 9. 2.',marks:{Q9801:false}}];
  const prog={}; prog[qk]={pageIndex:0,score:0,marks:{Q9801:false},picks:{},total:3,date:'2026. 9. 15.'};
  resetLS({ox_chap_history:hist,ox_in_progress:prog}); loadQuiz(); showHome(); closeAllWins(); clearWrongCache();
  T('G19 회독 틀림 2 + ⚡약점 진행중 틀림 1 → wrongCount = 3', wrongCount('Q9801')===3, wrongCount('Q9801'));
  const rf=document.getElementById('review-filter'); rf.value='wrong3'; renderDashboard();
  const rows=[...document.querySelectorAll('[data-trrow]')].map(r=>r.getAttribute('data-trrow'));
  T('G19 「3번+ 틀림」에 그 문항의 단원이 걸림', rows.indexOf('민법총칙|||'+CH)>=0, J(rows));
  rf.value='all';
  currentSubject='⚡빠른실행'; currentChapterLabel='🔥 약점 (틀림+헷갈림)'; isExamMode=false; currentFilteredData=[quizData.find(q=>q.id==='Q9801')];
  currentSessionMarks={Q9801:false}; currentSessionScore=0; resumePicks={}; currentPageIndex=0;
  if(typeof chapterSaved!=='undefined') chapterSaved=null;
  finishChapter();
  T('G19 그 큐를 끝내 진행중이 회독으로 옮겨가도 3(4 아님)', !(qk in lsO('ox_in_progress'))&&(lsO('ox_chap_history')[qk]||[]).length===1&&wrongCount('Q9801')===3, 'wc '+wrongCount('Q9801')+' · prog '+J(Object.keys(lsO('ox_in_progress'))));
  resetLS({}); clearWrongCache();
  openQuiz(UNIT,'민법총칙',CH);
  T('G19 (준비) 채점 전 Q9802 틀림 0 — 이때 캐시가 만들어진다', wrongCount('Q9802')===0);
  document.querySelectorAll('#quiz-container input[value="O"]').forEach(r=>r.checked=true);
  gradeCurrentPage(); try{ closeGradeModal(); }catch(e){}
  goHome();
  T('G19 쪽 채점 직후 첫 화면으로 나오면 수가 바로 반영(Q9802 틀림 1)', wrongCount('Q9802')===1&&!!(lsO('ox_in_progress')[ck]||{}).marks, wrongCount('Q9802')+' · '+J(Object.keys(lsO('ox_in_progress'))));
}
const LIST=[['G1',G1],['G2',G2],['G3',G3],['G4',G4],['G5',G5],['G6',G6],['G7',G7],['G8',G8],['G13',G13],['G14',G14],['G15',G15],['G16',G16],['G17',G17],['G18',G18],['G19',G19],['G10',G10]].filter(x=>P.skip.indexOf(x[0])<0);
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
  T('G10 헤드리스 페이지 오류 0 · console.error 0', errs.length===0&&cerr.length===0, 'error '+errs.length+' '+errs.slice(0,3).join(' / ')+' · console.error '+cerr.length+' '+cerr.slice(0,3).join(' / '));
  say('alert '+__ALERTS.length+'번 : '+__ALERTS.slice(0,3).join(' / ')+' · confirm '+__CONFIRMS.length+'번');
  R.forEach(x=>console.log('HZR|'+encodeURIComponent(x)));
  console.log('HZR|END');
},1500);
})();
