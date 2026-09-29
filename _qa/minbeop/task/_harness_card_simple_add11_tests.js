window.onload=null;
(function(){
/* _task_ox_card_simple_add11 §4 — G1 회독 배지 · G2 검색 결과 → 문항 팝업 · G3 📋 정리칩 묶음(진짜 데이터) · G10 */
const P=__P__;
const R=[];
const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+((i!==undefined&&!c)?' | '+String(i).replace(/\n/g,'⏎').slice(0,500):''));
const say=s=>R.push('INFO | '+String(s).replace(/\n/g,'⏎'));
const J=v=>JSON.stringify(v);
const BASE={'ox_uid_migrated':'1','ox_gg_okreset':'1','ox_gg_memo_merged':'{"at":1,"moved":0,"links":0}','ox_gg_logic_merged':'{"at":1,"moved":0,"links":0}','ox_auto_important_v2':'1'};
const resetLS=o=>{ localStorage.clear(); for(const k in BASE) localStorage.setItem(k,BASE[k]); for(const k in (o||{})) localStorage.setItem(k,typeof o[k]==='string'?o[k]:JSON.stringify(o[k])); try{useIdxDrop()}catch(e){} try{mcInvalidate()}catch(e){} };
const loadQuiz=()=>{ quizData.length=0; P.quiz.forEach(q=>quizData.push(JSON.parse(JSON.stringify(q)))); };
const loadReal=()=>{ quizData.length=0; buildQuizData(P.rows).forEach(q=>quizData.push(q)); };
const closeAllWins=()=>document.querySelectorAll('.oxwin').forEach(w=>w.remove());
const showHome=()=>{ document.getElementById('home-screen').classList.remove('hide'); document.getElementById('quiz-screen').classList.add('hide'); };
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const gI=(k,i,t)=>({k:k,i:i,t:t,ok:null,ts:1789000000000,cs:[]});
const CH='1. 총칙 > 1.1 민법의 법원';
const NEW=typeof qpScrollTo==='function';
const UNIT=P.quiz.filter(q=>!q.examNo&&q.subChapter==='1.1 민법의 법원').map(q=>q.id);
say('판 = '+(NEW?'NEW(qpScrollTo 있음)':'HEAD'));

/* G1 회독 배지 틀린 수도 빨강 */
async function G1(){
  const hist={}; hist['민법총칙||'+CH+'||all||all']=[{score:17,total:20,date:'2026. 9. 16.',marks:Object.fromEntries(UNIT.slice(0,20).map((u,n)=>[u,n>=3]))}];
  resetLS({ox_chap_history:hist}); loadQuiz(); showHome(); closeAllWins(); try{ clearWrongCache(); }catch(e){}
  renderDashboard(); await wait(120);
  const row=document.querySelector('[data-trrow="민법총칙|||'+CH+'"]');
  const badge=row?[...row.querySelectorAll('button')].find(b=>/1회독/.test(b.textContent)):null;
  const red=badge?[...badge.querySelectorAll('span.text-red-600')]:[];
  const txt=badge?badge.textContent.replace(/\s+/g,' ').trim():'없음';
  say('G1 배지 글자 「'+txt+'」 · 빨강 span 글자 '+J(red.map(s=>s.textContent))+' · 끝 HTML '+(badge?badge.innerHTML.replace(/\s+/g,' ').trim().slice(-90):''));
  T('G1 첫 화면 회독 배지 — 빨강 span 안 글자 = X${n}(「X3」) · 뒤에 「 /20」 · font-black · 계산 색 빨강', red.length===1&&red[0].textContent==='X3'&&red[0].classList.contains('font-black')&&getComputedStyle(red[0]).color==='rgb(220, 38, 38)'&&/X3 \/20/.test(txt), J({red:red.map(s=>s.textContent),txt}));
}

/* G2 검색 결과 → 문항 팝업 */
async function G2(){
  resetLS({ox_q_geunge:{Q9812:[gI('g_Q9812_a',1,'공동명의 예금은 준합유라는 근거 글')]}});
  loadQuiz(); showHome(); closeAllWins();
  try{ _oxWinZ=12000; _oxWinN=0; }catch(e){}
  const inp=document.getElementById('search-input');
  const clickFirst=async mode=>{
    setSearchMode(mode); inp.value='공동명의'; runSearch(); await wait(30);
    const b=document.querySelector('#search-results > button');
    const id=b?((b.textContent.match(/ID (Q\d+)/)||[])[1]||null):null;
    if(b) b.click();
    await wait(120);
    return {btn:!!b,id:id,quizOpened:!document.getElementById('quiz-screen').classList.contains('hide'),homeHidden:document.getElementById('home-screen').classList.contains('hide'),wins:[...document.querySelectorAll('.oxwin')].map(w=>w.id)};
  };
  const q=await clickFirst('q');
  const wq=document.getElementById('oxwin-q-'+q.id), bq=wq?wq.querySelector('.oxwin-body'):null;
  T('G2 문제 탭 「공동명의」 첫 결과 누름 → 문제풀이 안 열림 · 문항 팝업(oxwin-q-) 1개 · 몸통 맨 위', q.btn&&q.id==='Q9802'&&!q.quizOpened&&!q.homeHidden&&q.wins.length===1&&q.wins[0]==='oxwin-q-Q9802'&&!!bq&&bq.scrollTop===0, J(Object.assign({},q,{scroll:bq&&bq.scrollTop})));
  let front=false, z='';
  if(wq){ const r=wq.getBoundingClientRect(), el=document.elementFromPoint(r.left+r.width/2, r.top+12); z=getComputedStyle(wq).zIndex; front=+z>12000&&!!el&&wq.contains(el); }
  T('G2 팝업이 맨 앞 — z-index > 12000 · 창 머리 자리의 맨 위 요소가 팝업', front, 'z '+z);
  T('G2 검색 결과 칸은 그대로(닫지 않음)', !document.getElementById('search-results').classList.contains('hide')&&document.querySelectorAll('#search-results > button').length>0);
  closeAllWins();
  const m=await clickFirst('m');
  const wm=document.getElementById('oxwin-q-'+m.id), bm=wm?wm.querySelector('.oxwin-body'):null, gb=document.getElementById('qp-gg-box-'+m.id);
  let vis=false, geo={};
  if(bm&&gb){ const a=bm.getBoundingClientRect(), g=gb.getBoundingClientRect(); geo={bodyTop:Math.round(a.top),bodyBottom:Math.round(a.bottom),ggTop:Math.round(g.top),scroll:bm.scrollTop,scrollH:bm.scrollHeight,clientH:bm.clientHeight}; vis=g.top>=a.top-1&&g.top<=a.bottom-10; }
  T('G2 근거 탭 「공동명의」 첫 결과 누름 → 문제풀이 안 열림 · 팝업 1개 · 그 문항 근거 줄이 몸통 보이는 자리 안(굴려서)', m.btn&&m.id==='Q9812'&&!m.quizOpened&&m.wins.length===1&&vis&&bm.scrollTop>0, J(Object.assign({},m,geo,{vis})));
  closeAllWins(); try{ clearSearch(); }catch(e){}
}

/* G3 📋 — 진짜 데이터 목차 전 과목 */
async function G3(){
  loadReal(); resetLS({}); closeAllWins(); showHome();
  renderDashboard(); await wait(50);
  const SUF=/\((7판신설|미수록|변형)\)$/;
  const keyOf=l=>{ const sub=l.indexOf(' > ')>=0?l.slice(l.indexOf(' > ')+3):l; const m=/^\d+(?:\.\d+)?/.exec(sub); return m?m[0]:l; };
  const rows=[...document.querySelectorAll('[data-trrow]')];
  const bySub={};
  rows.forEach((r,idx)=>{ const v=r.getAttribute('data-trrow'), i=v.indexOf('|||'), s=v.slice(0,i), l=v.slice(i+3);
    const d=(bySub[s]=bySub[s]||{rows:[],btns:[]}); d.rows.push({l:l,idx:idx}); const bt=r.querySelector('button[data-jn]'); if(bt) d.btns.push({l:l,idx:idx,bt:bt}); });
  const suffixBtn=[]; let tot=0; const bad=[], cnt=[], moved=[], onlySuf=[];
  Object.keys(bySub).forEach(s=>{ bySub[s].btns.forEach(x=>{ if(SUF.test(x.l)) suffixBtn.push(s+' '+x.l); }); });
  Object.keys(P.census).forEach(s=>{
    const d=bySub[s]||{rows:[],btns:[]}; tot+=d.btns.length;
    if(d.btns.length!==P.census[s].groups) cnt.push(s+' 📋 '+d.btns.length+' ≠ 새 열쇠 묶음 '+P.census[s].groups);
    const pos={}; d.rows.forEach(x=>pos[x.l]=x.idx);
    const seen={};
    d.btns.forEach(x=>{
      const ls=x.bt.getAttribute('data-jn').split('|||');
      const anchor=ls.find(l=>!SUF.test(l))||ls[0];
      if(ls.indexOf(x.l)<0) bad.push(s+' '+x.l+' — 📋 줄이 제 묶음 목록에 없다');
      if(anchor!==x.l) bad.push(s+' '+x.l+' — 📋 줄 ≠ 묶음 안 꼬리표 없는 첫 줄 '+anchor);
      if(!ls.some(l=>!SUF.test(l))) onlySuf.push(s+' '+ls.join('|'));
      if(ls[0]!==x.l) moved.push(s+' 📋 「'+x.l+'」 · 정렬 첫 줄 「'+ls[0]+'」');
      const ps=ls.map(l=>pos[l]===undefined?-1:pos[l]); if(ps.some((v,k)=>v<0||(k>0&&v<ps[k-1]))) bad.push(s+' '+x.l+' — data-jn 이 목차 차례가 아니거나 없는 줄');
      const ks=new Set(ls.map(l=>keyOf(l))); if(s!=='변리사 기출'&&ks.size!==1) bad.push(s+' '+x.l+' — 열쇠 섞임 '+[...ks].join(','));
      ls.forEach(l=>{ if(seen[l]) bad.push(s+' 겹침 '+l); seen[l]=1; });
    });
    const miss=d.rows.filter(x=>!seen[x.l]); if(miss.length) bad.push(s+' 빠짐 '+miss.length+' '+miss.slice(0,3).map(x=>x.l).join(','));
  });
  say('G3 (진짜 데이터) 📋 이 정렬 첫 줄이 아닌 꼬리표 없는 줄로 옮겨 간 묶음 '+moved.length+(moved.length?' — '+moved.join(' ; '):'')+' · 꼬리표 줄만으로 된 묶음 '+onlySuf.length);
  const spot=[['민법총칙','4. 권리의 객체'],['민법총칙','5. 법률행위'],['민법총칙','9. 법률행위의 부관(조건과 기한)'],['민법총칙','12. 제척기간'],['물권법','3. 소유권'],['채권총론','1. 채권 일반,목적']].map(([s,c])=>{
    const d=bySub[s]||{rows:[],btns:[]}; const rs=d.rows.filter(x=>x.l.indexOf(c+' > ')===0||x.l===c); const bs=d.btns.filter(x=>x.l.indexOf(c+' > ')===0||x.l===c);
    return s+' 「'+c+'」 줄 '+rs.length+' · 📋 '+bs.length+(bs.length?' @'+bs.map(x=>x.l.slice(c.length+3)||x.l).join('|')+' · data-jn '+bs.map(x=>x.bt.getAttribute('data-jn').split('|||').length).join(','):''); });
  say('G3 (진짜 데이터) 목차 줄 '+rows.length+' · 📋 '+tot+' · 꼬리표 줄의 📋 '+suffixBtn.length+(suffixBtn.length?' ('+suffixBtn.slice(0,6).join(' / ')+')':''));
  say('G3 장 보기 — '+spot.join(' ; '));
  T('G3 (진짜 데이터) 목차 전 과목 — 꼬리표 줄(chapLabel 이 (7판신설)|(미수록)|(변형) 으로 끝남)의 📋 = 0', suffixBtn.length===0, suffixBtn.slice(0,8).join(' / '));
  T('G3 (진짜 데이터) 묶음마다 꼬리표 없는 첫 줄에 📋 1(그런 줄이 없으면 정렬 첫 줄) · 과목마다 📋 수 = 새 열쇠 묶음 수(합 '+P.censusTotal+') · data-jn ||| = 그 묶음 줄 전부·목차 차례(빠짐·겹침 0)', tot===P.censusTotal&&cnt.length===0&&bad.length===0, cnt.concat(bad).slice(0,8).join(' / ')||('합 '+tot));
}

/* G10 */
async function G10(){
  resetLS({}); loadQuiz(); showHome(); closeAllWins();
  renderDashboard();
  T('G10 첫 화면이 그려진다', document.getElementById('dashboard-container').children.length>0);
  startQuiz('민법총칙',CH); await wait(120);
  T('G10 문제풀이가 열린다', !document.getElementById('quiz-screen').classList.contains('hide')&&!!document.getElementById('q-box-Q9801'));
  goHome();
  const hit=quizData.find(q=>q.id==='Q9803'); openQPopup('Q9803');
  T('G10 문항 팝업 「↪ 이 문제로 이동」은 그대로 jumpFromSearch(단원으로 이동)', !!document.querySelector('#oxwin-q-Q9803 button[onclick*="jumpFromSearch(\'Q9803\')"]'));
  closeAllWins();
}

const LIST=[['G1',G1],['G2',G2],['G3',G3],['G10',G10]].filter(x=>P.skip.indexOf(x[0])<0);
setTimeout(async function(){
  for(const [n,f] of LIST){
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
