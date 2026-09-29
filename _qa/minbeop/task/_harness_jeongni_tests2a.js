
async function G4(){
  const hist={}; hist['민법총칙||'+CH+'||all||all']=[{score:1,total:4,date:'2026. 9. 1.',marks:{Q9901:false}},{score:1,total:4,date:'2026. 9. 3.',marks:{Q9901:true},cf:{Q9901:true}}];
  const prog={}; prog['민법총칙||'+CH+'||all||all']={marks:{Q9901:false},picks:{},date:'2026. 9. 9.',total:4};
  resetLS({ox_q_tags:{Q9901:{fake:true,important:true,confuse:true},Q9906:{concept:true,memo:true},Q9902:{confuse:true}},
    ox_q_geunge:{Q9901:[gItem('g_Q9901_a',1,'내 근거 첫 줄'),gItem('g_Q9901_b',2,'내 근거 둘째 줄')],Q9903:[gItem('g_Q9903_a',1,'연결될 근거 글')],Q9906:[gItem('g_Q9906_a',1,'Q9906 근거')]},
    ox_q_reflinks:{Q9901:{geunge:['Q9903']},Q9902:{geunge:['Q9903']}}, ox_q_links:{Q9901:['Q9902','Q9903']},
    ox_chap_history:hist, ox_in_progress:prog});
  loadQuiz(); showHome(); closeAllWins();
  currentSubject='민법총칙'; currentChapterLabel=CH; currentSessionMarks={Q9901:true};
  renderDashboard();
  const btn=trow(CH)?trow(CH).querySelector('button[data-jn]'):null;
  if(!btn||!NEW){ T('G4 📋 를 누르면 정리 창이 열린다',false,'단추 '+!!btn+' · openJeongni '+NEW); currentSubject=null; currentChapterLabel=null; return; }
  btn.click();
  const w=jnWin();
  const head=w?w.querySelector('.oxwin-head').textContent:'';
  T('G4 창 — 제목 「📋 정리 · 1.1 민법의 법원」 · 부제 「민법총칙 · 5문항」', !!w&&head.indexOf('📋 정리 · 1.1 민법의 법원')>=0&&head.indexOf('민법총칙 · 5문항')>=0, head);
  if(!w) return;
  const hs=[...w.querySelectorAll('[data-jnh]')].map(x=>x.textContent);
  T('G4 소제목 수 = chapLabel 수(2) · 「이름 · N문항」', J(hs)===J(['1.1 민법의 법원 · 4문항','1.1 민법의 법원(7판신설) · 1문항']), J(hs));
  const rows=[...w.querySelectorAll('[data-jnrow]')].map(x=>x.getAttribute('data-jnrow'));
  const want=[...chapUidsOf('민법총칙',CH),...chapUidsOf('민법총칙',CH7)];
  T('G4 행 수·차례 = chapUidsOf 전부(근거·태그·기록 없어도)', J(rows)===J(want)&&rows.length===5, J(rows)+' vs '+J(want));
  const R_=id=>w.querySelector('[data-jnrow="'+id+'"]');
  const ic=id=>{ const s=R_(id).firstElementChild.querySelector('span.tracking-wide'); return s?s.textContent:''; };
  T('G4 태그 아이콘은 붙은 것만(⚠️⭐ · 💡🧠 · 없음 · 없음)', ic('Q9901')==='⚠️⭐'&&ic('Q9906')==='💡🧠'&&ic('Q9902')===''&&ic('Q9903')==='', J([ic('Q9901'),ic('Q9906'),ic('Q9902'),ic('Q9903')]));
  T('G4 🌀 아이콘 0 · 「마지막」 0', w.textContent.indexOf('🌀')<0&&w.textContent.indexOf('마지막')<0);
  T('G4 연결 근거 본문 0(Q9901 행에 「연결될 근거 글」 없음 · 칩만) · Q9903 행엔 제 근거', R_('Q9901').textContent.indexOf('연결될 근거 글')<0&&R_('Q9903').textContent.indexOf('🔗 1. 연결될 근거 글')>=0&&/🔗 Q9903/.test(R_('Q9901').firstElementChild.textContent));
  const f1=R_('Q9901').firstElementChild;
  const chipQ=[...f1.children].find(s=>/^🔗 Q9903/.test(s.textContent));
  T('G4 연결 근거 칩 = 근거 목록 행 칩과 같은 글자(쓰임 수 2 · onclick 없음)', !!chipQ&&chipQ.outerHTML===norm(fieldRefChipsHTML('Q9901'))&&!chipQ.getAttribute('onclick')&&(chipQ.querySelector('i')||{}).textContent==='2', chipQ&&chipQ.outerHTML);
  const cells=[...R_('Q9901').querySelectorAll('[data-jnrec] > div:first-child > span')];
  const rc=recCellsOf('Q9901',true).cells;
  T('G4 이번 세션 칸 0 · 칸 수 = recCellsOf(진행중 전부) · 진행중 칸 점선·title', cells.length===rc.length&&cells.length===3&&w.querySelectorAll('[title*="· 이번"]').length===0&&/진행중/.test(cells[2].title)&&/border-dashed/.test(cells[2].className), cells.length+' vs '+rc.length+' · '+J(cells.map(c=>c.title)));
  T('G4 칸 18×16px · 윗줄 X O X · 아랫줄 – △ –', cells.length===3&&cells.every(c=>/width:18px;height:16px/.test(c.getAttribute('style')))&&J(cells.map(c=>c.textContent))===J(['X','O','X'])&&J([...R_('Q9901').querySelectorAll('[data-jnrec] > div:last-child > span')].map(c=>c.textContent))===J(['–','△','–']), J(cells.map(c=>c.textContent)));
  T('G4 기록 0 이면 「기록 없음」', /기록 없음/.test(R_('Q9902').firstElementChild.textContent)&&!R_('Q9902').querySelector('[data-jnrec]'));
  const myBox=R_('Q9901').querySelector('.border-l-2');
  T('G4 내 근거 상자 — whitespace-pre-wrap · 글 전부', !!myBox&&myBox.classList.contains('whitespace-pre-wrap')&&myBox.textContent==='🔗 1. 내 근거 첫 줄\n2. 내 근거 둘째 줄', myBox&&myBox.textContent);
  const qd=R_('Q9901').querySelector('[data-mark="q-Q9901"]');
  T('G4 지문 전문 · 12.5px · onclick 없음(add1)', !!qd&&qd.textContent===quizData.find(x=>x.id==='Q9901').q&&getComputedStyle(qd).fontSize==='12.5px'&&!qd.getAttribute('onclick'), qd?getComputedStyle(qd).fontSize:'없음');
  const idc=f1.children[0], noc=f1.children[1];
  T('G4 첫 칩 = bookChipHTML(카드와 같게 · 교재 자리) · 번호 칩 = 문항 팝업 단추(add1)', idc.outerHTML===norm(bookChipHTML(quizData.find(x=>x.id==='Q9901')))&&noc.tagName==='BUTTON'&&noc.title==='문항 팝업'&&/^openQPopup\('Q9901'\)$/.test(noc.getAttribute('onclick')||'')&&noc.textContent==='1번', idc.outerHTML.slice(0,90)+' · '+noc.outerHTML.slice(0,140));
  noc.click();
  T('G4 번호 칩을 누르면 문항 팝업이 뜬다', !!document.getElementById('oxwin-q-Q9901'));
  if(document.getElementById('oxwin-q-Q9901')) document.getElementById('oxwin-q-Q9901').remove();
  const sb=[...f1.querySelectorAll('button')].find(b=>/showRelated\('Q9901','same'\)/.test(b.getAttribute('onclick')||'')), mb=[...f1.querySelectorAll('button')].find(b=>/showRelated\('Q9901','mine'\)/.test(b.getAttribute('onclick')||''));
  T('G4 칩 글자 「🔗 판 1」「↩ 연결 2」', !!sb&&!!mb&&sb.textContent.trim()==='🔗 판 1'&&mb.textContent.trim()==='↩ 연결 2', (sb&&sb.textContent)+' · '+(mb&&mb.textContent));
  if(mb) mb.click();
  T('G4 연결 칩 → 관련 창(rel-mine) · 문항 팝업은 안 뜬다', !!document.getElementById('oxwin-rel-mine-Q9901')&&!document.getElementById('oxwin-q-Q9901'));
  if(document.getElementById('oxwin-rel-mine-Q9901')) document.getElementById('oxwin-rel-mine-Q9901').remove();
  const tb=w.querySelector('.oxwin-head [data-jnmarks]');
  T('G4 제목 줄에 「✏️ 표시」(닫기 왼쪽 · 켜짐 색)', !!tb&&tb.nextElementSibling&&tb.nextElementSibling.textContent.trim()==='닫기'&&tb.textContent==='✏️ 표시'&&tb.classList.contains('text-amber-800'), tb?tb.outerHTML:'없음');
  currentSubject=null; currentChapterLabel=null; currentSessionMarks={};
}
async function G5(){
  const w=jnWin();
  if(!w){ T('G5 정리 창이 떠 있다',false,'없음(G4 에서 연다)'); return; }
  openQuiz(['Q9906','Q9901'],'민법총칙',CH);
  const before=document.getElementById('quiz-container').innerHTML;
  const ans=[...w.querySelectorAll('[data-jnans]')];
  T('G5 처음 전부 hide', ans.length===5&&ans.every(a=>a.classList.contains('hide')), ans.map(a=>a.className).join(' / '));
  const btnOf=id=>w.querySelector('[data-jnrow="'+id+'"] > button');
  btnOf('Q9906').click();
  const open=()=>ans.filter(a=>!a.classList.contains('hide')).map(a=>a.getAttribute('data-jnans'));
  const b6=w.querySelector('[data-jnans="Q9906"] b');
  T('G5 한 행 누르면 그 행만 펴짐 · ▾', J(open())===J(['Q9906'])&&btnOf('Q9906').textContent==='정답·해설 ▾', J(open()));
  T('G5 정답 색 — X 빨강 font-black', !!b6&&b6.textContent==='X'&&b6.classList.contains('text-red-600')&&b6.classList.contains('font-black'), b6&&b6.outerHTML);
  btnOf('Q9901').click();
  const b1=w.querySelector('[data-jnans="Q9901"] b');
  T('G5 정답 색 — O 파랑', !!b1&&b1.textContent==='O'&&b1.classList.contains('text-blue-600'), b1&&b1.outerHTML);
  btnOf('Q9906').click();
  T('G5 다시 누르면 접힘(그 행만)', J(open())===J(['Q9901'])&&btnOf('Q9906').textContent==='정답·해설 ▸', J(open()));
  T('G5 창 밖 문제풀이 카드는 안 건드린다', document.getElementById('quiz-container').innerHTML===before);
  closeAllWins(); showHome();
}
function G6(){
  const realNow=Date.now; Date.now=()=>1789000000000;
  try{
    loadQuiz();
    const hA={}; hA['민법총칙||'+CH+'||all||all']=[{score:1,total:2,date:'2026. 9. 1.',marks:{Q9901:false}},{score:1,total:2,date:'2026. 9. 3.',marks:{Q9901:false}}];
    hA['⚡빠른실행||🔥 약점 다시 풀기 (틀림+헷갈림)||all||all']=[{score:1,total:1,date:'2026. 9. 5.',marks:{Q9901:true},cf:{Q9901:true}}];
    const hB=JSON.parse(J(hA)); hB['민법총칙||'+CH2+'||all||all']=[{score:0,total:1,date:'8/30/2026',marks:{Q9901:true}}];
    const pB={}; pB['민법총칙||'+CH+'||all||all']={marks:{Q9901:true},date:'2026. 9. 9.',total:2}; pB['민법총칙||'+CH2+'||all||all']={marks:{Q9901:false},date:'2026. 9. 8.',total:1};
    const hC={}; hC['민법총칙||'+CH+'||all||all']=[{score:0,total:1,date:'이상한 날짜',marks:{Q9901:false,Q9902:true},cf:{}}];
    const sets=[['A',hA,{},{Q9901:{confuse:false}},{}],['B',hB,pB,{Q9901:{confuse:true}},{Q9901:true}],['C',hC,{},{},{Q9902:false}]];
    for(const [n,h,p,tg,sm] of sets){
      resetLS({ox_chap_history:h,ox_in_progress:p,ox_q_tags:tg});
      currentSubject='민법총칙'; currentChapterLabel=CH; currentSessionMarks=sm;
      ['Q9901','Q9902','Q9904'].forEach(u=>V('G6.rec.'+n+'.'+u, recStripHTML(u)));
    }
    resetLS({ox_q_links:{Q9901:['Q9902','','Q9903']}});
    const it=id=>quizData.find(x=>x.id===id);
    ['Q9901','Q9904'].forEach(u=>{ V('G6.chip.same.'+u, samePanryeChipHTML(it(u))); V('G6.chip.mine.'+u, myLinkChipHTML(it(u))); });
    openQuiz(['Q9901','Q9902'],'민법총칙',CH);
    ['Q9901','Q9902'].forEach(u=>V('G6.card.'+u, document.getElementById('q-box-'+u).outerHTML));
  } catch(e){ T('G6 하네스가 죽었다',false,e.message); }
  finally{ Date.now=realNow; currentSessionMarks={}; currentSubject=null; currentChapterLabel=null; showHome(); }
}
