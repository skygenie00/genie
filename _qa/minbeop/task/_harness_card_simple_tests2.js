
const trow=l=>[...document.querySelectorAll('[data-trrow]')].find(r=>r.getAttribute('data-trrow')==='민법총칙|||'+l);
const GC=()=>typeof BAR_GRADE_CLS!=='undefined'?BAR_GRADE_CLS:'없음', MC=()=>typeof BAR_MOVE_CLS!=='undefined'?BAR_MOVE_CLS:'없음';
async function G6(){
  resetLS({}); closeAllWins();
  const ab=()=>document.getElementById('action-btn'), sk=()=>document.getElementById('skip-next-btn');
  const row=()=>({t:ab().textContent.trim(), on:ab().getAttribute('onclick'), cls:ab().className, skip:!sk().classList.contains('hide')});
  const pillOk=()=>{ const c=document.getElementById('controls-container'); const inner=c&&c.firstElementChild; return !!inner&&/sticky/.test(c.className)&&/justify-end/.test(c.className)&&/rounded-full/.test(inner.className)&&!!document.getElementById('mark-count'); };
  openQuiz(UNIT,'민법총칙',CH);
  let a=row(); V('G6.on.unit1-before', a.on);
  T('G6 단원 1쪽 채점 전 — 「채점 ✓」 파스텔 파랑 글자 gradeCurrentPage · 「다음 ▶」 회색 글자 · 알약 하나', a.t==='채점 ✓'&&a.on==='gradeCurrentPage()'&&a.skip&&a.cls===GC()&&sk().classList.contains('text-gray-600')&&!/\bbg-(gray-100|gray-200|blue-600)\b/.test(sk().className+' '+a.cls)&&pillOk(), J(a)+' · '+sk().className);
  document.querySelectorAll('#quiz-container input[value="O"]').forEach(r=>r.checked=true);
  gradeCurrentPage(); try{ closeGradeModal(); }catch(e){}
  a=row();
  T('G6 단원 1쪽 채점 뒤 — 「다음 5문제 ▶」 goNextPage · 회색 글자', a.t==='다음 5문제 ▶'&&a.on==='goNextPage()'&&a.cls===MC(), J(a));
  const rb=document.getElementById('reopen-grade-bar');
  T('G6 채점 뒤 #reopen-grade-bar 알약', !rb.classList.contains('hide')&&!!rb.firstElementChild&&/rounded-full/.test(rb.firstElementChild.className));
  goNextPage();
  a=row(); V('G6.on.unit2-before', a.on);
  const pb=document.getElementById('exam-prev-bar');
  T('G6 단원 마지막 쪽 — 「채점 ✓」 · 「다음 ▶」 숨김 · 「◀ 이전」 흰 알약 회색 글자', a.t==='채점 ✓'&&a.on==='gradeCurrentPage()'&&!a.skip&&!pb.classList.contains('hide')&&/rounded-full/.test(pb.firstElementChild.className)&&pb.firstElementChild.classList.contains('text-gray-600'), J(a)+' · '+pb.firstElementChild.className);
  goHome();
  resetLS({}); loadQuiz(); showHome();
  startQuiz('변리사 기출','2016년 제53회');
  a=row(); V('G6.on.exam1', a.on);
  T('G6 기출 중간 쪽 — 「다음 4문제 ▶」 goNextPageExam · 회색 글자 · 「다음 ▶」 숨김', a.t==='다음 4문제 ▶'&&a.on==='goNextPageExam()'&&!a.skip&&a.cls===MC(), J(a));
  goNextPageExam();
  a=row(); V('G6.on.exam2', a.on);
  T('G6 기출 마지막 쪽 — 「전체 채점 ✓」 gradeAllExam · 파스텔 파랑 글자 · 이전 알약', a.t==='전체 채점 ✓'&&a.on==='gradeAllExam()'&&a.cls===GC()&&!document.getElementById('exam-prev-bar').classList.contains('hide'), J(a));
  goHome();
}
async function G7(){
  const btns=[...document.querySelectorAll('button')].filter(b=>b.textContent.trim()==='📝 학습로그');
  T('G7 「📝 학습로그」 단추 DOM 0', btns.length===0, btns.length);
}
async function G8(){
  const gI=(k,i,t)=>({k:k,i:i,t:t,ok:null,ts:1789000000000,cs:[]});
  resetLS({ox_q_geunge:{Q9801:[gI('g_Q9801_a',1,'내 근거')],Q9802:[gI('g_Q9802_a',1,'연결될 근거 하나'),gI('g_Q9802_b',2,'연결될 근거 둘')]},ox_q_reflinks:{Q9801:{geunge:['Q9802']}}});
  closeAllWins(); loadQuiz();
  V('G8.card.refchips', ggRefChipsHTML('Q9801'));
  V('G8.card.refbox', ggRefBoxHTML('Q9801'));
  if(typeof openJeongni!=='function'){ T('G8 정리 창',false,'openJeongni 없음'); return; }
  openQuiz(['Q9801','Q9802'],'민법총칙',CH);
  openJeongni('민법총칙','1.1');
  const w=document.querySelector('.oxwin[id^="oxwin-jn-"]');
  const chip=document.getElementById('jn-gg-refchip-Q9801-Q9802');
  if(!chip){ T('G8 정리 행에 jn- 연결칩',false,'칩 없음'); closeAllWins(); showHome(); return; }
  T('G8 칩 = 🔗 Q9802 · onclick 안 event.stopPropagation() · 범위 jn-', /^🔗 Q9802/.test(chip.textContent)&&/^event\.stopPropagation\(\);ggRefToggle\('Q9801','Q9802','jn-'\)$/.test(chip.getAttribute('onclick')||''), chip.getAttribute('onclick'));
  const box0=document.getElementById('jn-refgg-box-Q9801-Q9802');
  T('G8 처음엔 접혀 있다 · 내 근거 상자 아래 자리', !!box0&&box0.classList.contains('hide')&&box0.parentElement.id==='jn-reflink-geunge-Q9801'&&w.contains(box0));
  chip.click();
  const box=document.getElementById('jn-refgg-box-Q9801-Q9802');
  T('G8 누르면 jn-refgg-box 펴짐 · 항목 수 = ggOf(Q9802).length', !!box&&!box.classList.contains('hide')&&box.querySelectorAll('.flex-none.font-extrabold').length===ggOf('Q9802').length, box?box.className:'없음');
  const eb=[...box.querySelectorAll('button')].find(b=>b.textContent.trim()==='✎ 여기서 고치기'); if(eb) eb.click();
  const ein=document.getElementById('jn-refgg-ein-Q9801-Q9802-g_Q9802_a'); if(ein) ein.value='정리 창에서 고친 글';
  const ed=document.getElementById('jn-refgg-edit-Q9801-Q9802-g_Q9802_a');
  const sb=ed?[...ed.querySelectorAll('button')].find(b=>b.textContent.trim()==='저장'):null; if(sb) sb.click();
  const chipCard=document.getElementById('gg-chip-Q9802-g_Q9802_a');
  T('G8 ✎ 저장 → ox_q_geunge[Q9802] 바뀜 · 떠 있는 Q9802 카드 칩 title 도', (ggOf('Q9802')[0]||{}).t==='정리 창에서 고친 글'&&!!chipCard&&chipCard.title==='정리 창에서 고친 글', (ggOf('Q9802')[0]||{}).t+' · '+(chipCard&&chipCard.title));
  T('G8 저장 뒤에도 상자는 펴져 있다(ggRefPaint)', !!document.getElementById('jn-refgg-box-Q9801-Q9802')&&!document.getElementById('jn-refgg-box-Q9801-Q9802').classList.contains('hide'));
  const gb=[...document.getElementById('jn-refgg-box-Q9801-Q9802').querySelectorAll('button')].find(b=>b.textContent.trim()==='↪ 그 문제 보기'); if(gb) gb.click();
  T('G8 ↪ 그 문제 보기 → 비교 창', !!document.getElementById('oxwin-cmp-Q9802'));
  const cb=[...document.getElementById('jn-refgg-box-Q9801-Q9802').querySelectorAll('button')].find(b=>b.textContent.trim()==='× 연결 끊기'); if(cb) cb.click();
  T('G8 × 끊기 → ox_q_reflinks 에서 빠지고 칩·상자 사라짐', J(refOf('Q9801','geunge'))==='[]'&&!document.getElementById('jn-gg-refchip-Q9801-Q9802')&&!document.getElementById('jn-refgg-box-Q9801-Q9802'), J(lsO('ox_q_reflinks')));
  T('G8 jn- 댓글 고치기 칸도 GG_CMAX', ggMaxOf({id:'jn-refgg-cein-x'})===GG_CMAX&&ggMaxOf({id:'jn-refgg-ein-x'})===GG_TMAX);
  closeAllWins(); showHome();
}
async function G10(){
  resetLS({}); loadQuiz(); showHome(); closeAllWins();
  renderDashboard();
  T('G10 첫 화면이 그려진다', document.getElementById('dashboard-container').children.length>0);
  startQuiz('민법총칙',CH);
  T('G10 문제풀이가 열린다', !document.getElementById('quiz-screen').classList.contains('hide')&&!!document.getElementById('q-box-Q9801'));
  goHome();
  startQuiz('변리사 기출','2016년 제53회');
  T('G10 기출뷰가 열린다', !!document.getElementById('q-box-Q9901'), document.getElementById('quiz-container').textContent.slice(0,120));
  goHome();
  startVirtualQuiz('하네스 큐', quizData.filter(q=>!q.examNo).slice(0,3));
  T('G10 ⚡큐가 열린다', !document.getElementById('quiz-screen').classList.contains('hide')&&!!document.getElementById('q-box-Q9801')&&document.getElementById('current-subject-title').textContent==='⚡ 빠른 실행');
  goHome();
  startQuiz('민법총칙',CH);
  await wait(250);
  const a0=__ALERTS.length, pin=document.getElementById('tag-coord-Q9801');
  if(pin&&NEW){ const r=pin.getBoundingClientRect(); T('G10 📍 단추 높이 22px(태그 단추와 같게)', Math.round(r.height)===22, r.width+'×'+r.height); }
  if(pin) pin.click();
  let cd=null;
  for(let i=0;i<200&&!(cd=document.getElementById('cd-close'));i++) await wait(50);
  T('G10 정리OMR(좌표기억) 뷰어가 열린다(카드 📍 단추)', !!pin&&!!cd&&__ALERTS.length===a0, 'pin '+!!pin+' · cd-close '+!!cd+' · alert '+__ALERTS.slice(a0).join('/'));
  if(cd) cd.click();
  goHome();
}
