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
const loadReal=()=>{ quizData.length=0; buildQuizData(P.rows).forEach(q=>quizData.push(q)); };
const closeAllWins=()=>document.querySelectorAll('.oxwin').forEach(w=>w.remove());
const showHome=()=>{ document.getElementById('home-screen').classList.remove('hide'); document.getElementById('quiz-screen').classList.add('hide'); };
const openQuiz=(ids,subject,chap)=>{
  loadQuiz();
  currentSubject=subject; currentChapterLabel=chap; isExamMode=false; currentPageIndex=0; currentSessionMarks={}; resumePicks={}; currentSessionScore=0; lastGradeResults=null;
  currentFilteredData=ids.map(id=>quizData.find(q=>q.id===id));
  document.getElementById('home-screen').classList.add('hide'); document.getElementById('quiz-screen').classList.remove('hide');
  renderQuizPage();
};
const key=(el,k)=>el.dispatchEvent(new KeyboardEvent('keydown',{key:k,bubbles:true,cancelable:true}));
const btnIn=(root,text)=>root?[...root.querySelectorAll('button')].find(b=>b.textContent.trim()===text):null;
const rowOf=id=>[...document.querySelectorAll('#search-results > button')].find(b=>b.textContent.indexOf('ID '+id)>=0);
const gItem=(k,i,t)=>({k:k,i:i,t:t,ok:null,ts:1789000000000,cs:[]});
const norm=h=>{ const d=document.createElement('div'); d.innerHTML=h; return d.innerHTML; };
const CH='1. 총칙 > 1.1 민법의 법원', CH7='1. 총칙 > 1.1 민법의 법원(7판신설)', CH2='1. 총칙 > 1.2 신의칙';
const NEW=typeof openJeongni==='function';
const trow=l=>[...document.querySelectorAll('[data-trrow]')].find(r=>r.getAttribute('data-trrow')==='민법총칙|||'+l);
const jnWin=()=>document.querySelector('.oxwin[id^="oxwin-jn-"]');
const T300=('삼백 자 근거 가나다라마바사아자차카타파하 ').repeat(20).slice(0,300);
const wait=ms=>new Promise(r=>setTimeout(r,ms));
say('판 = '+(NEW?'NEW(openJeongni 있음)':'HEAD'));

async function G1(){
  resetLS({ox_q_geunge:{Q9901:[gItem('g_Q9901_a',1,'첫째 줄 근거'),gItem('g_Q9901_b',2,T300)],Q9902:[gItem('g_Q9902_a',1,'짧은 첫 줄'),gItem('g_Q9902_b',2,'짧은 둘째 줄')],Q9903:[gItem('g_Q9903_a',1,'연결될 근거 글')]},
           ox_q_reflinks:{Q9901:{geunge:['Q9903']},Q9902:{geunge:['Q9903']}},ox_q_links:{Q9901:['Q9902']}});
  loadQuiz(); showHome(); closeAllWins();
  showFieldDistribution('m');
  showFieldList('m',_fieldGroups.indexOf(fieldGroupKey(quizData.find(q=>q.id==='Q9901'))));
  const r1=rowOf('Q9901'), r2=rowOf('Q9902');
  if(!r1||!r2){ T('G1 근거 목록 행이 있다',false,'Q9901 '+!!r1+' · Q9902 '+!!r2); return; }
  const b1=r1.querySelector('.border-l-2'), b2=r2.querySelector('.border-l-2');
  say('G1 tailwind '+(typeof tailwind)+' · 상자 white-space '+getComputedStyle(b1).whiteSpace);
  T('G1 근거 상자에 whitespace-pre-wrap', b1.classList.contains('whitespace-pre-wrap')&&getComputedStyle(b1).whiteSpace==='pre-wrap', b1.className+' · '+getComputedStyle(b1).whiteSpace);
  T('G1 300자 근거가 안 잘린다(글 전부)', b1.textContent==='🔗 1. 첫째 줄 근거\n2. '+T300, b1.textContent.length);
  const one=b2.cloneNode(false); one.textContent='🔗 한 줄'; b2.parentNode.appendChild(one); const h1=one.getBoundingClientRect().height; one.remove();
  const h2=b2.getBoundingClientRect().height, cs=getComputedStyle(b2);
  const pad=parseFloat(cs.paddingTop)+parseFloat(cs.paddingBottom)+parseFloat(cs.borderTopWidth)+parseFloat(cs.borderBottomWidth);
  const lines=(h2-pad)/(h1-pad);                     /* 위아래 여백은 줄 수만큼 늘지 않는다 — 글 높이끼리 나눈다 */
  T('G1 두 줄짜리 근거가 두 줄로 보인다(글 높이 = 한 줄의 2배)', h1>pad&&lines>1.9&&lines<2.1, 'h1 '+h1+' · h2 '+h2+' · 여백 '+pad+' · 줄 '+lines.toFixed(2));
  const chip=[...r1.querySelectorAll('span')].find(s=>/^🔗 Q9903/.test(s.textContent));
  const ni=chip?chip.querySelector('i'):null;
  openQPopup('Q9901');
  const pc=document.getElementById('qp-gg-refchip-Q9901-Q9903'), pi=pc?pc.querySelector('i'):null;
  T('G1 연결칩에 횟수 — 문항 팝업 칩과 같은 수·같은 모양', !!ni&&!!pi&&ni.textContent==='2'&&ni.outerHTML===pi.outerHTML, 'row '+(ni&&ni.outerHTML)+' · popup '+(pi&&pi.outerHTML));
  closeAllWins();
  T('G1 근거 목록 행에는 판·연결 칩이 없다', r1.querySelectorAll('[onclick*="showRelated"]').length===0&&!/판 \d|연결 \d/.test(r1.textContent), r1.textContent.slice(0,120));
  showFieldDistribution('l');
  showFieldList('l',_fieldGroups.indexOf(fieldGroupKey(quizData.find(q=>q.id==='Q9903'))));
  V('G1.l.list', document.getElementById('search-results').innerHTML);
}
async function G2(){
  resetLS({ox_mem_cards:{Q9901:[{kind:'svg',svg:'<svg xmlns="http://www.w3.org/2000/svg"></svg>',name:'카드'}]}});
  loadQuiz(); showHome(); closeAllWins();
  renderDashboard();
  const chk=tag=>{
    const bs=[...document.querySelectorAll('[data-mcchap]')];
    T('G2 🃏 innerHTML 에 「암기노트」 0건 — '+tag, bs.length>0&&bs.every(b=>b.innerHTML.indexOf('암기노트')<0), bs.length+' · '+bs.map(b=>b.innerHTML).join(' / ').slice(0,200));
    const a=bs.find(b=>b.getAttribute('data-mcchap')==='민법총칙|||'+CH), b=bs.find(b=>b.getAttribute('data-mcchap')==='민법총칙|||'+CH2);
    T('G2 🃏 = 아이콘+수(1) · 0이면 아이콘만 — '+tag, !!a&&!!b&&a.innerHTML==='🃏 1'&&b.innerHTML==='🃏', (a&&a.innerHTML)+' · '+(b&&b.innerHTML));
  };
  chk('첫 그림');
  renderDashboardCardCounts();
  chk('renderDashboardCardCounts 뒤');
}
async function G3(){
  resetLS({});
  loadQuiz(); showHome(); closeAllWins();
  renderDashboard();
  const jb=[...document.querySelectorAll('button[data-jn]')];
  const on=l=>{ const r=trow(l); return r?r.querySelector('button[data-jn]'):null; };
  const a=on(CH), b=on(CH7), c=on(CH2);
  T('G3 (작은 판) 📋 = 묶음 수 3(1.1 · 1.2 · 변리사 기출 한 해)', jb.length===3, jb.length);
  T('G3 (작은 판) 1.1 묶음 첫 행에만 · data-jn = 1.1 두 소단원(사이에 1.2 행이 끼어도)', !!a&&!b&&a.getAttribute('data-jn')===CH+'|||'+CH7, (a&&a.getAttribute('data-jn'))+' · 7판신설 행 단추 '+!!b);
  T('G3 (작은 판) 1.2 는 제 행 하나가 한 묶음', !!c&&c.getAttribute('data-jn')===CH2, c&&c.getAttribute('data-jn'));
  T('G3 📋 는 🃏 바로 오른쪽 · 글자 📋 만 · title · teal class', !!a&&!!a.previousElementSibling&&a.previousElementSibling.hasAttribute('data-mcchap')&&a.textContent.trim()==='📋'&&a.title==='이 묶음 정리'&&a.className==='text-[10px] font-bold text-teal-700 bg-teal-50 border border-teal-200 rounded px-1.5 py-0.5 whitespace-nowrap shrink-0 hover:bg-teal-100 transition', a?a.className:'없음');
  T('G3 onclick = event.stopPropagation();openJeongni(과목,열쇠,this)', !!a&&/^event\.stopPropagation\(\);openJeongni\('민법총칙','1\.1',this\)$/.test(a.getAttribute('onclick')||''), a&&a.getAttribute('onclick'));
  loadReal(); resetLS({});
  renderDashboard();
  const rows=[...document.querySelectorAll('[data-trrow]')];
  const bySub={};
  rows.forEach((r,idx)=>{ const v=r.getAttribute('data-trrow'), i=v.indexOf('|||'), s=v.slice(0,i), l=v.slice(i+3);
    const d=(bySub[s]=bySub[s]||{rows:[],btns:[]}); d.rows.push({l:l,idx:idx}); const bt=r.querySelector('button[data-jn]'); if(bt) d.btns.push({l:l,idx:idx,bt:bt}); });
  const keyOfLabel=l=>{ const sub=l.indexOf(' > ')>=0?l.slice(l.indexOf(' > ')+3):l; const m=/^\d+\.\d+/.exec(sub); return m?m[0]:l; };
  let tot=0; const bad=[], cnt=[], cross=[];
  Object.keys(P.census).forEach(s=>{
    const d=bySub[s]||{rows:[],btns:[]}; tot+=d.btns.length;
    if(d.btns.length!==P.census[s].groups) cnt.push(s+' 단추 '+d.btns.length+' ≠ '+P.census[s].groups);
    if(d.rows.length!==P.census[s].rows) cnt.push(s+' 행 '+d.rows.length+' ≠ '+P.census[s].rows);
    const pos={}; d.rows.forEach(x=>pos[x.l]=x.idx);
    const seen={};
    d.btns.forEach(x=>{
      const ls=x.bt.getAttribute('data-jn').split('|||');
      if(ls[0]!==x.l) bad.push(s+' '+x.l+' — data-jn 첫 칸이 제 행이 아니다');
      if(Math.min(...ls.map(l=>pos[l]===undefined?-1:pos[l]))!==x.idx) bad.push(s+' '+x.l+' — 묶음의 첫 행이 아니다');
      const ks=new Set(ls.map(keyOfLabel)); if(ks.size!==1) bad.push(s+' '+x.l+' — 열쇠 섞임 '+[...ks].join(','));
      ls.forEach(l=>{ if(seen[l]) bad.push(s+' 겹침 '+l); seen[l]=1; });
      const chs=new Set(ls.map(l=>l.split(' > ')[0])); if(chs.size>1) cross.push(s+' 「'+[...ks][0]+'」 '+ls.length+'줄 · 장 '+[...chs].join(' / '));
      if(NEW){ const fb=jnLabelsOf(s,[...ks][0]); if(J(fb)!==J(ls)) bad.push(s+' '+x.l+' — jnLabelsOf ≠ data-jn '+J(fb).slice(0,80)); }
    });
    const miss=d.rows.filter(x=>!seen[x.l]); if(miss.length) bad.push(s+' 빠짐 '+miss.length+' '+miss.slice(0,3).map(x=>x.l).join(','));
  });
  T('G3 (진짜 데이터) 과목마다 📋 수 = §0 묶음 수 · 합 '+P.censusTotal, tot===P.censusTotal&&cnt.length===0, '합 '+tot+' · '+cnt.slice(0,6).join(' / '));
  T('G3 (진짜 데이터) 묶음 첫 행에만 · data-jn 합집합 = 그 과목 소단원 전부(빠짐 0·겹침 0) · 묶음 안 열쇠 하나 · jnLabelsOf 와 같다', NEW&&bad.length===0&&tot>0, bad.slice(0,6).join(' / ')||('단추 '+tot));
  say('G3 장을 건너는 묶음 : '+(cross.join(' ; ')||'없음'));
  if(NEW){
    for(const [s,k] of [['민법총칙','1.1'],['채권각론','2.2']]){
      const d=bySub[s], x=d&&d.btns.find(y=>keyOfLabel(y.l)===k);
      if(!x){ T('G4 (진짜 데이터) '+s+' 「'+k+'」 단추',false,'없음'); continue; }
      closeAllWins(); x.bt.click();
      const w=jnWin(), ls=x.bt.getAttribute('data-jn').split('|||');
      const want=ls.reduce((n,l)=>n+chapUidsOf(s,l).length,0);
      T('G4 (진짜 데이터) '+s+' 「'+k+'」 창 — 행 수 = 묶음 문항 '+want+' · 소제목 = 소단원 '+ls.length, !!w&&w.querySelectorAll('[data-jnrow]').length===want&&w.querySelectorAll('[data-jnh]').length===ls.length, w?w.querySelectorAll('[data-jnrow]').length+' / '+w.querySelectorAll('[data-jnh]').length:'창 없음');
    }
    closeAllWins();
  }
  loadQuiz(); resetLS({}); renderDashboard();
}
