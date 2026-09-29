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
const snap=()=>{ const o={}; for(let i=0;i<localStorage.length;i++){ const k=localStorage.key(i); o[k]=localStorage.getItem(k); } return o; };
const snapS=()=>{ const o=snap(); return J(Object.keys(o).sort().map(k=>[k,o[k]])); };
const diffKeys=(a,b)=>Object.keys(Object.assign({},a,b)).filter(k=>a[k]!==b[k]).sort();
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
const nl=s=>String(s).replace(/\r\n?/g,'\n');
const CH='1. 총칙 > 1.1 민법의 법원', CH2='1. 총칙 > 1.2 논리 샘플';
const NEW=typeof ggLogicMergeOnce==='function';
const UNIT=P.quiz.filter(q=>!q.examNo&&q.subChapter==='1.1 민법의 법원').map(q=>q.id);
const SAMPLE=P.quiz.filter(q=>q.subChapter==='1.2 논리 샘플').map(q=>q.id);
const S=P.sample, SU=Object.keys(S.logic).sort(), SRCU=S.srcLogicUid;
say('판 = '+(NEW?'NEW(ggLogicMergeOnce 있음)':'HEAD')+' · 샘플 '+SU.join(',')+' · 근거 있음 '+Object.keys(S.geunge).join(',')+' · src:logic 미리 '+SRCU+' · 특수문자·줄바꿈 든 글 '+S.spec.length);
const seedSample=()=>{
  const gg=JSON.parse(J(S.geunge));
  gg[SRCU]=gg[SRCU].concat([{k:'g_'+SRCU+'_pre',i:gg[SRCU].length+1,t:'다른 기기가 이미 옮긴 논리',ok:null,ts:1789000000000,cs:[],src:'logic'}]);
  resetLS({ox_q_logic:S.logic,ox_q_geunge:gg});
  return gg;
};

/* G1 dry — 기록 파일 샘플(논리 5 · 그중 근거 있는 것 2 · src:'logic' 이미 있는 것 1) */
async function G1(){
  if(!NEW){ T('G1 ggLogicMergeOnce 있음',false,'HEAD'); return; }
  seedSample();
  T('G1 샘플 = 논리 5 · 그중 근거 있는 것 2 · src:logic 이미 있는 것 1', SU.length===5&&Object.keys(S.geunge).length===2&&Object.keys(S.geunge).every(u=>SU.indexOf(u)>=0)&&ggOf(SRCU).filter(g=>g.src==='logic').length===1, J({su:SU,gg:Object.keys(S.geunge)}));
  const s0=snap(), s0s=snapS();
  const r=ggLogicMergeOnce(true);
  T('G1 dry → moved 4 · skipped 1(src:logic 있던 문항)', !!r&&r.moved.length===4&&r.skipped.length===1&&r.skipped[0]===SRCU, J(r));
  T('G1 dry → 근거가 이미 있던 문항 1 · 연결 0 · 4000자 초과 0', !!r&&r.had.length===1&&r.links.length===0&&r.over.length===0, J(r&&[r.had,r.links,r.over]));
  T('G1 dry → 아무것도 안 씀(localStorage 전부 그대로 · 표시키 없음)', snapS()===s0s&&!localStorage.getItem('ox_gg_logic_merged'), J(diffKeys(s0,snap())));
  localStorage.setItem('ox_gg_logic_merged','{"at":1}');
  const r2=ggLogicMergeOnce(true);
  T('G1 dry 는 표시키가 켜져 있어도 계획을 돌려준다(쓰기만 막는다)', !!r2&&r2.moved.length===4, J(r2));
  localStorage.removeItem('ox_gg_logic_merged');
}

/* G2 실행 */
async function G2(){
  if(!NEW){ T('G2 ggLogicMergeOnce 있음',false,'HEAD'); return; }
  const gg0=seedSample();
  const lg0=localStorage.getItem('ox_q_logic');
  const r=ggLogicMergeOnce(false);
  const raw=localStorage.getItem('ox_q_geunge')||'';
  const gg=lsO('ox_q_geunge');
  const moved=r?r.moved:[];
  const bad={last:[],num:[],text:[],shape:[],old:[]};
  moved.forEach(u=>{
    const L=gg[u]||[], last=L[L.length-1]||{};
    if(!(last.src==='logic'&&L.filter(x=>x&&x.src==='logic').length===1)) bad.last.push(u);
    if(!L.every((x,n)=>x&&x.i===n+1)) bad.num.push(u);
    if(last.t!==S.logic[u]||raw.indexOf(J(S.logic[u]))<0) bad.text.push(u);
    if(!(J(Object.keys(last))===J(['k','i','t','ok','ts','cs','src'])&&last.ok===null&&J(last.cs)==='[]'&&typeof last.ts==='number'&&String(last.k).indexOf('g_'+u+'_')===0)) bad.shape.push(u);
    (gg0[u]||[]).forEach((x,n)=>{ const y=L[n]; if(!y||y.k!==x.k||y.t!==x.t||y.ok!==x.ok||y.ts!==x.ts||J(y.cs)!==J(x.cs)) bad.old.push(u); });
  });
  T('G2 옮긴 4문항 모두 근거 목록 맨 뒤에 src:logic 하나', moved.length===4&&!bad.last.length, J(bad.last));
  T('G2 번호 1부터 이어짐', moved.length===4&&!bad.num.length, J(bad.num.map(u=>[u,(gg[u]||[]).map(x=>x.i)])));
  T('G2 글 바이트 같음 — t === ox_q_logic 글 · 저장 JSON 에 그 글의 JSON 문자열 그대로(이스케이프 없음 · 특수문자·줄바꿈 든 글 '+S.spec.length+')', moved.length===4&&!bad.text.length&&S.spec.length>0, J(bad.text));
  T('G2 항목 꼴 {k,i,t,ok:null,ts,cs:[],src} · 열쇠 g_<uid>_', moved.length===4&&!bad.shape.length, J(bad.shape.map(u=>(gg[u]||[]).slice(-1)[0])));
  T('G2 옛 근거 항목은 i 말고 그대로(k·t·ok·ts·cs)', !bad.old.length, J(bad.old));
  T('G2 건너뛴 문항(src:logic 있던) 목록 그대로', J(gg[SRCU])===J(gg0[SRCU]), J(gg[SRCU]));
  const nog=SU.filter(u=>!S.geunge[u]);
  T('G2 근거 없던 3문항은 항목 하나(i=1)', nog.length===3&&nog.every(u=>(gg[u]||[]).length===1&&gg[u][0].i===1), J(nog.map(u=>gg[u])));
  const mk=lsO('ox_gg_logic_merged');
  T('G2 표시키 ox_gg_logic_merged 생김(moved 4 · links 0)', mk.moved===4&&mk.links===0&&typeof mk.at==='number', J(mk));
  T('G2 ox_q_logic 무변', localStorage.getItem('ox_q_logic')===lg0);
  const n1=localStorage.getItem('ox_q_geunge');
  const r2=ggLogicMergeOnce(false);
  T('G2 두 번 돌려도 그대로(표시키 켜짐 → null)', r2===null&&localStorage.getItem('ox_q_geunge')===n1, J(r2));
  localStorage.removeItem('ox_gg_logic_merged');
  const r3=ggLogicMergeOnce(false);
  T('G2 표시키 없는 다른 기기(옮긴 판을 동기화로 받음)에서 돌아도 그대로 — src:logic 멱등 · 건너뜀 5', !!r3&&r3.moved.length===0&&r3.skipped.length===5&&localStorage.getItem('ox_q_geunge')===n1, J(r3));
  resetLS({ox_q_logic:{Q9801:'논리'},ox_q_geunge:'{망가진'});
  let r4; try{ r4=ggLogicMergeOnce(false); }catch(e){ r4='throw:'+e.message; }
  T('G2 근거 저장소가 JSON 이 아니면 던지고 안 덮는다(표시키도 안 켜짐)', typeof r4==='string'&&r4.indexOf('throw:')===0&&localStorage.getItem('ox_q_geunge')==='{망가진'&&!localStorage.getItem('ox_gg_logic_merged'), J(r4));
  T('G2 그때 ggLogicMergeBoot 는 건너뜀(false · 던지지 않음)', ggLogicMergeBoot(true)===false&&localStorage.getItem('ox_q_geunge')==='{망가진');
}

/* G3 연결 */
async function G3(){
  if(!NEW){ T('G3 ggLogicMergeOnce 있음',false,'HEAD'); return; }
  const RL={Q9801:{logic:['Q9802','Q9803'],geunge:['Q9803','Q9804']},Q9805:{memo:['Q9806'],logic:['Q9807']},Q9808:{geunge:['Q9809']}};
  resetLS({ox_q_logic:{Q9801:'논리 A'},ox_q_reflinks:RL});
  const d=ggLogicMergeOnce(true);
  T('G3 dry → 연결 옮길 문항 2(Q9801·Q9805) · 아무것도 안 씀', !!d&&J(d.links)===J(['Q9801','Q9805'])&&J(lsO('ox_q_reflinks'))===J(RL), J(d&&d.links));
  ggLogicMergeOnce(false);
  const rl=lsO('ox_q_reflinks');
  T('G3 논리 갈래 → 근거 갈래 합집합(옛 근거 차례 뒤에 논리 · 겹친 것 한 번)', J(rl.Q9801)===J({geunge:['Q9803','Q9804','Q9802']}), J(rl.Q9801));
  T('G3 메모 갈래는 그대로 · 논리 갈래 빈 배열(refOf)', J(rl.Q9805)===J({memo:['Q9806'],geunge:['Q9807']})&&refOf('Q9801','logic').length===0&&refOf('Q9805','logic').length===0, J(rl.Q9805));
  T('G3 논리 연결 없는 문항 그대로', J(rl.Q9808)===J({geunge:['Q9809']}), J(rl.Q9808));
  T('G3 ox_q_reflinks 꼴 그대로(문항 → {memo?,logic?,geunge?} 문자열 배열 · 빈 배열 안 남김)', Object.keys(rl).every(k=>Object.keys(rl[k]).every(b=>['memo','logic','geunge'].indexOf(b)>=0&&Array.isArray(rl[k][b])&&rl[k][b].length&&rl[k][b].every(x=>typeof x==='string'))), J(rl));
  T('G3 표시키 links 2', lsO('ox_gg_logic_merged').links===2, localStorage.getItem('ox_gg_logic_merged'));
}

/* G4 시동 순서 */
async function G4(){
  if(!NEW){ T('G4 ggMergeBoots 있음',false,'HEAD'); return; }
  const log=[];
  const oSync=window.syncRecords, oMem=window.ggMemoMergeBoot, oLog=window.ggLogicMergeBoot, oSI=window.setInterval, oMb=window.mbCheckNew;
  const boot=()=>{ window.setInterval=()=>0; window.mbCheckNew=()=>{}; try{ recBoot(); }catch(e){ log.push('recBoot 오류 '+e.message); } finally{ window.setInterval=oSI; window.mbCheckNew=oMb; } };
  window.syncRecords=function(f){ log.push('sync('+(f===true?'force':'')+')'); return Promise.resolve(); };
  window.ggMemoMergeBoot=function(h){ log.push('memo('+h+')'); return oMem.apply(this,arguments); };
  window.ggLogicMergeBoot=function(h){ log.push('logic('+h+')'); return oLog.apply(this,arguments); };
  try{
    resetLS({ox_q_memos:{Q9801:'메모 글'},ox_q_logic:{Q9802:'논리 글'}}); localStorage.removeItem('ox_gg_memo_merged');
    boot(); await wait(50);
    T('G4 recBoot → 첫 동기화 → ggMemoMergeBoot → ggLogicMergeBoot → force 동기화 한 번', J(log)===J(['sync()','memo(true)','logic(true)','sync(force)']), J(log));
    T('G4 둘 다 옮김(src:memo · src:logic) · 표시키 둘', ggOf('Q9801').some(g=>g.src==='memo')&&ggOf('Q9802').some(g=>g.src==='logic')&&!!localStorage.getItem('ox_gg_memo_merged')&&!!localStorage.getItem('ox_gg_logic_merged'), J(lsO('ox_q_geunge')));
    log.length=0; resetLS({ox_q_logic:{Q9803:'논리 글 둘'}});
    ggMergeBoots(); await wait(10);
    T('G4 논리만 옮김 → force 동기화 한 번', J(log)===J(['memo(true)','logic(true)','sync(force)']), J(log));
    log.length=0; ggMergeBoots(); await wait(10);
    T('G4 옮길 것 없음(표시키 켜짐) → 동기화 안 부름', J(log)===J(['memo(true)','logic(true)']), J(log));
    log.length=0; resetLS({ox_q_logic:{Q9804:'논리 글 셋'}});
    window.syncRecords=function(f){ log.push('sync('+(f===true?'force':'')+')'); return f===true?Promise.resolve():Promise.reject(new Error('오프라인')); };
    boot(); await wait(50);
    T('G4 첫 동기화가 실패해도 흡수 · force 동기화 한 번', J(log)===J(['sync()','memo(true)','logic(true)','sync(force)'])&&ggOf('Q9804').some(g=>g.src==='logic'), J(log));
    window.syncRecords=function(f){ log.push('sync('+(f===true?'force':'')+')'); return Promise.resolve(); };
    log.length=0; resetLS({ox_q_memos:{Q9805:'메모 둘'}}); localStorage.removeItem('ox_gg_memo_merged');
    const rv=window.ggMemoMergeBoot(); await wait(10);
    T('G4 ggMemoMergeBoot 를 인자 없이 부르면 옛 그대로(스스로 force 동기화)', rv===true&&J(log)===J(['memo(undefined)','sync(force)']), J(log));
  } finally { window.syncRecords=oSync; window.ggMemoMergeBoot=oMem; window.ggLogicMergeBoot=oLog; window.setInterval=oSI; window.mbCheckNew=oMb; }
}

/* G5 UI */
async function G5(){
  resetLS({ox_q_logic:{Q9803:'논리 글 하나'},ox_q_links:{Q9803:['Q9805']},ox_q_reflinks:{Q9803:{logic:['Q9804']}}});
  closeAllWins();
  openQuiz(UNIT,'민법총칙',CH);
  const qc=document.getElementById('quiz-container');
  const bad=[...qc.querySelectorAll('[id]')].map(e=>e.id).filter(id=>/^(logic-|logic-btn-|logic-input-|reflogic-|link-search-logic-|reflink-logic-|link-results-logic-)/.test(id));
  T('G5 카드에 logic-·logic-btn-·logic-input-·reflogic-·link-search-logic- id 0', bad.length===0, bad.slice(0,6).join(','));
  T('G5 카드 안 「📐」 글자 0(보이는 글·숨은 패널·속성 전부)', qc.innerHTML.indexOf('📐')<0, (qc.innerHTML.match(/.{40}📐.{20}/)||[''])[0]);
  const box=document.getElementById('q-box-Q9803');
  T('G5 논리 글이 카드에 안 보인다(흡수 뒤 근거 칩으로만)', !!box&&box.textContent.indexOf('논리 글 하나')<0);
  T('G5 「🔗 관련/비교 문제 연결」·link-input-·link-search- 있음', !!box&&box.textContent.indexOf('🔗 관련/비교 문제 연결')>=0&&!!document.getElementById('link-input-Q9803')&&!!document.getElementById('link-search-Q9803'));
  const eb=box?[...box.querySelectorAll('button')].find(b=>/✏️/.test(b.textContent)):null;
  T('G5 아랫줄 단추 글자 「✏️ 연결」', !!eb&&eb.textContent.trim()==='✏️ 연결', eb&&eb.textContent);
  if(eb) eb.click();
  const pan=document.getElementById('memo-panel-Q9803');
  T('G5 패널 제목은 「🔗 관련/비교 문제 연결」만(📐 논리 칸 0)', !!pan&&!pan.classList.contains('hide')&&pan.querySelectorAll('label').length===1&&pan.textContent.indexOf('📐')<0, pan&&[...pan.querySelectorAll('label')].map(l=>l.textContent.trim()).join(' / '));
  document.getElementById('link-input-Q9803').value='Q9806, Q9807';
  const s0=snap();
  const sb=pan?[...pan.querySelectorAll('button')].find(b=>b.textContent.trim()==='저장하기'):null; if(sb) sb.click();
  const ch=diffKeys(s0,snap());
  T('G5 저장 단추가 ox_q_links 만 쓴다', !!sb&&J(ch)===J(['ox_q_links']), J(ch));
  V('G5.card.links', lsO('ox_q_links'));
  showLinkedQuestion('Q9803','Q9801');
  const w=document.getElementById('oxwin-cmp-Q9803');
  T('G5 비교 창 「📐」 0 · cmp-logic- · cmp-lb- 0', !!w&&w.innerHTML.indexOf('📐')<0&&!w.querySelector('[id^="cmp-logic-"],[id^="cmp-lb-"]'), w?(w.innerHTML.match(/.{40}📐.{20}/)||[''])[0]:'창 없음');
  const ceb=document.getElementById('cmp-eb-Q9803');
  T('G5 비교 창 편집 단추 글자 「✏️ 연결」', !!ceb&&ceb.textContent.trim()==='✏️ 연결', ceb&&ceb.textContent);
  if(ceb) ceb.click();
  const ce=document.getElementById('cmp-edit-Q9803');
  T('G5 비교 창 편집 칸 — 논리 textarea·reflogic·논리 찾기 0 · 유사문제 칸 있음', !!ce&&!ce.classList.contains('hide')&&!ce.querySelector('[id^="cmp-logic-input-"],[id^="reflogic-"],[id^="link-search-logic-"]')&&!!document.getElementById('cmp-link-input-Q9803')&&ce.innerHTML.indexOf('📐')<0, ce?ce.innerHTML.slice(0,200):'없음');
  T('G5 비교 창 「✏️ 연결」 누른 뒤에도 글자 그대로', !!ceb&&ceb.textContent.trim()==='✏️ 연결', ceb&&ceb.textContent);
  const cli=document.getElementById('cmp-link-input-Q9803'); if(cli) cli.value='Q9808';
  const c0=snap();
  const csb=ce?[...ce.querySelectorAll('button')].find(b=>b.textContent.trim()==='저장하기'):null; if(csb) csb.click();
  const ch2=diffKeys(c0,snap());
  T('G5 비교 창 저장이 ox_q_links 만 쓴다', !!csb&&J(ch2)===J(['ox_q_links']), J(ch2));
  V('G5.cmp.links', lsO('ox_q_links'));
  if(ceb) ceb.click();
  T('G5 비교 창 「✏️ 연결」 다시 누르면 접힘', !!ce&&ce.classList.contains('hide'));
  closeAllWins(); showHome();
  const bar=document.getElementById('search-input').closest('div').parentElement;
  T('G5 첫 화면 search-mode-l 0 · 검색 줄에 「📐」 0', !document.getElementById('search-mode-l')&&bar.textContent.indexOf('📐')<0, bar.textContent.replace(/\s+/g,' ').slice(0,160));
  const e0=(window.__ERR||[]).length;
  let err=null;
  searchMode='l'; document.getElementById('search-input').value='카드';
  try{ runSearch(); }catch(e){ err=e.message; }
  T('G5 searchMode 가 l 인 채 검색 → 오류 없이 m(근거 단추 켜짐)', !err&&searchMode==='m'&&/bg-blue-600/.test(document.getElementById('search-mode-m').className)&&(window.__ERR||[]).length===e0, J({err,searchMode,cls:document.getElementById('search-mode-m').className}));
  searchMode='l'; document.getElementById('search-input').value=''; err=null;
  try{ onCountClick(); }catch(e){ err=e.message; }
  T('G5 searchMode 가 l 인 채 수 누르기 → 오류 없이 m · 근거 분포', !err&&searchMode==='m'&&!document.getElementById('search-results').classList.contains('hide'), J({err,searchMode}));
  err=null;
  try{ setSearchMode('l'); }catch(e){ err=e.message; }
  T("G5 setSearchMode('l') → 오류 없이 m", !err&&searchMode==='m', J({err,searchMode}));
  document.getElementById('search-input').value=''; setSearchMode('q');
}

/* G6 검색 — 옮긴 논리 글이 근거 검색·근거 목록·정리 창·카드 칩에서 */
async function G6(){
  if(!NEW){ T('G6 ggLogicMergeOnce 있음',false,'HEAD'); return; }
  resetLS({ox_q_logic:S.logic,ox_q_geunge:S.geunge});
  loadQuiz(); closeAllWins(); showHome();
  refreshModeCounts();
  const mb0=document.getElementById('search-mode-m').textContent;
  ggLogicMergeOnce(false);
  refreshModeCounts();
  const mb1=document.getElementById('search-mode-m').textContent;
  T('G6 「🔗 근거 (N)」 수가 오른다(2 → 5)', mb0==='🔗 근거 (2)'&&mb1==='🔗 근거 (5)', mb0+' → '+mb1);
  const bad={search:[],list:[],jn:[],chip:[]};
  setSearchMode('m');
  for(const u of SU){
    const t=S.logic[u], m=t.match(/[가-힣A-Za-z0-9]{4,}/), term=m?m[0]:t.slice(0,6);
    document.getElementById('search-input').value=term; runSearch();
    if(![...document.querySelectorAll('#search-results button')].some(b=>(b.getAttribute('onclick')||'').indexOf("'"+u+"'")>=0)) bad.search.push(u+':'+term);
  }
  T('G6 옮긴 논리 글이 「🔗 근거」 검색에서 잡힌다(5문항)', !bad.search.length, J(bad.search));
  document.getElementById('search-input').value=''; setSearchMode('m'); onCountClick();
  const gi=_fieldGroups.indexOf('민법총칙 · 1.2 논리 샘플');
  if(gi>=0) showFieldList('m',gi);
  for(const u of SU){
    const row=[...document.querySelectorAll('#search-results button')].find(b=>(b.getAttribute('onclick')||'')==="openQPopup('"+u+"')");
    if(!row||nl(row.textContent).indexOf(nl(S.logic[u]))<0) bad.list.push(u);
  }
  T('G6 근거 목록 행에 옮긴 글이 보인다(줄바꿈·특수문자 그대로)', gi>=0&&!bad.list.length, J({gi,bad:bad.list}));
  document.getElementById('search-input').value=''; setSearchMode('q');
  openJeongni('민법총칙','1.2');
  for(const u of SU){
    const jr=document.querySelector('[data-jnrow="'+u+'"]');
    if(!jr||nl(jr.textContent).indexOf(nl(S.logic[u]))<0) bad.jn.push(u);
  }
  T('G6 정리 창 행에 옮긴 글이 보인다', !bad.jn.length, J(bad.jn));
  closeAllWins();
  openQuiz(SAMPLE,'민법총칙',CH2);
  for(const u of SU){
    const it=ggOf(u).filter(g=>g.src==='logic').slice(-1)[0];
    const chip=it?document.getElementById('gg-chip-'+u+'-'+it.k):null;
    const tv=it?document.getElementById('gg-t-'+u+'-'+it.k):null;
    if(!chip||!((tv&&nl(tv.textContent)===nl(S.logic[u]))||nl(chip.title)===nl(S.logic[u]))) bad.chip.push(u+':'+!!chip+'/'+!!tv);
  }
  T('G6 카드 근거 줄에 칩(글 = 옮긴 논리) — 고치기·댓글·연결은 근거 칩 그대로', !bad.chip.length, J(bad.chip));
  showHome(); closeAllWins();
}

/* G7 자리 — 기록 파일을 받은 기기 꼴 */
async function G7(){
  const D=P.rec.data||{}, U=P.rec.u||{}, GN=P.rec.gone||{};
  localStorage.clear(); for(const k in BASE) localStorage.setItem(k,BASE[k]);
  const sh={}; SYNC_KEYS.forEach(k=>{ if(k in D){ localStorage.setItem(k,J(D[k])); sh[k]=D[k]; } });
  localStorage.setItem('ox_sync_shadow',J(sh)); localStorage.setItem('ox_sync_u',J(U)); localStorage.setItem('ox_sync_gone',J(GN));
  const size=()=>{ let n=0; for(let i=0;i<localStorage.length;i++){ const k=localStorage.key(i); n+=k.length+(localStorage.getItem(k)||'').length; } return n*2; };
  const ksz=k=>(k.length+(localStorage.getItem(k)||'').length)*2;
  const b0=size(), g0=ksz('ox_q_geunge'), s0=ksz('ox_sync_shadow'), u0=ksz('ox_sync_u');
  say('G7 기록을 받은 기기 꼴(동기화 키 값 + 그림자 + 도장·묘비) — localStorage '+b0+' B(UTF-16 · '+(b0/1e6).toFixed(2)+' MB) · ox_q_geunge '+g0+' B · 그림자 '+s0+' B · 도장 '+u0+' B');
  if(!NEW) return;
  const lg0=localStorage.getItem('ox_q_logic');
  const r=ggLogicMergeOnce(false);
  const b1=size();
  let stErr=null; try{ stampAll(); }catch(e){ stErr=e.message; }
  const b2=size(), g2=ksz('ox_q_geunge'), s2=ksz('ox_sync_shadow'), u2=ksz('ox_sync_u');
  say('G7 흡수 직후 '+b1+' B · stampAll(도장·그림자) 뒤 '+b2+' B('+(b2/1e6).toFixed(2)+' MB · 5MB 의 '+(100*b2/5e6).toFixed(1)+'%) · ox_q_geunge '+g0+' → '+g2+' B · 그림자 '+s0+' → '+s2+' B · 도장 '+u0+' → '+u2+' B');
  const nLogic=Object.keys(D.ox_q_logic||{}).filter(k=>String(D.ox_q_logic[k]||'').trim()).length;
  const gg=lsO('ox_q_geunge'), items=Object.keys(gg).reduce((a,k)=>a+(Array.isArray(gg[k])?gg[k].length:0),0);
  say('G7 옮김 '+(r?r.moved.length:'-')+' · 건너뜀 '+(r?r.skipped.length:'-')+' · 근거가 이미 있던 문항 '+(r?r.had.length:'-')+' · 근거 문항 '+Object.keys(gg).length+' · 항목 '+items);
  T('G7 기록 파일 논리 글 전부 옮김(건너뜀 0)', !!r&&r.moved.length===nLogic&&r.skipped.length===0&&nLogic>1000, J(r&&{m:r.moved.length,s:r.skipped.length,n:nLogic}));
  T('G7 흡수 전/후 5MB 안 · 80%(4,000,000 B) 안', b0<5e6&&b2<=4e6&&!stErr, J({b0,b2,stErr}));
  T('G7 ox_q_logic 무변', localStorage.getItem('ox_q_logic')===lg0);
}

/* G9 헤드리스 화면·엑셀 내보내기 */
async function G9(){
  resetLS({}); loadQuiz(); showHome(); closeAllWins();
  renderDashboard();
  T('G9 첫 화면이 그려진다', document.getElementById('dashboard-container').children.length>0);
  startQuiz('민법총칙',CH);
  T('G9 문제풀이가 열린다', !document.getElementById('quiz-screen').classList.contains('hide')&&!!document.getElementById('q-box-Q9801'));
  goHome();
  startQuiz('변리사 기출','2016년 제53회');
  T('G9 기출뷰가 열린다', !!document.getElementById('q-box-Q9901'), document.getElementById('quiz-container').textContent.slice(0,120));
  goHome();
  startVirtualQuiz('하네스 큐', quizData.filter(q=>!q.examNo).slice(0,3));
  T('G9 ⚡큐가 열린다', !document.getElementById('quiz-screen').classList.contains('hide')&&!!document.getElementById('q-box-Q9801')&&document.getElementById('current-subject-title').textContent==='⚡ 빠른 실행');
  goHome();
  startQuiz('민법총칙',CH);
  await wait(250);
  const a0=__ALERTS.length, pin=document.getElementById('tag-coord-Q9801');
  if(pin) pin.click();
  let cd=null;
  for(let i=0;i<200&&!(cd=document.getElementById('cd-close'));i++) await wait(50);
  T('G9 정리OMR(좌표기억) 뷰어가 열린다(카드 📍 단추)', !!pin&&!!cd&&__ALERTS.length===a0, 'pin '+!!pin+' · cd-close '+!!cd+' · alert '+__ALERTS.slice(a0).join('/'));
  if(cd) cd.click();
  goHome();
  const LOGIC='논리 내보내기 글 <b>&"\'\n둘째 줄';
  resetLS({ox_q_logic:{Q9801:LOGIC}});
  const oDb=window.dbGet, oAoa=XLSX.utils.aoa_to_sheet, oClick=HTMLAnchorElement.prototype.click;
  let aoa=null, dl=null;
  window.dbGet=async function(k){ return k==='rows'?JSON.parse(J(P.rows)):oDb.apply(this,arguments); };
  XLSX.utils.aoa_to_sheet=function(a){ aoa=a; return oAoa.apply(this,arguments); };
  HTMLAnchorElement.prototype.click=function(){ dl=this.download||''; };
  try{ await exportExcelFile(); }catch(e){ T('G9 엑셀 내보내기 오류',false,e.message); }
  finally{ window.dbGet=oDb; XLSX.utils.aoa_to_sheet=oAoa; HTMLAnchorElement.prototype.click=oClick; }
  const hdr=(aoa&&aoa[0])||[], li=hdr.indexOf('논리'), ui=hdr.indexOf('uid');
  const r1=(aoa||[]).find(x=>x[ui]==='Q9801'), r2=(aoa||[]).find(x=>x[ui]==='Q9802');
  T('G9 엑셀 내보내기가 열린다 · 논리 열 = ox_q_logic 값(없는 문항은 엑셀 원래 값)', !!aoa&&li>=0&&!!r1&&r1[li]===LOGIC&&!!r2&&r2[li]===''&&/^민법OX_문항마스터_/.test(dl||''), J({li,r1:r1&&r1[li],r2:r2&&r2[li],dl}));
  V('G9.excel.aoa', aoa);
}

const LIST=[['G1',G1],['G2',G2],['G3',G3],['G4',G4],['G5',G5],['G6',G6],['G7',G7],['G9',G9]].filter(x=>P.skip.indexOf(x[0])<0);
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
