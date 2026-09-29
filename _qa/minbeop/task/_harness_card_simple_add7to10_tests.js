window.onload=null;
(function(){
const P=__P__;
const R=[];
const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+((i!==undefined&&!c)?' | '+String(i).replace(/\n/g,'⏎').slice(0,500):''));
const say=s=>R.push('INFO | '+String(s).replace(/\n/g,'⏎'));
const J=v=>JSON.stringify(v);
const lsO=k=>{try{return JSON.parse(localStorage.getItem(k)||'{}')||{}}catch(e){return {}}};
const BASE={'ox_uid_migrated':'1','ox_gg_okreset':'1','ox_gg_memo_merged':'{"at":1,"moved":0,"links":0}','ox_gg_logic_merged':'{"at":1,"moved":0,"links":0}','ox_auto_important_v2':'1'};
const resetLS=o=>{ localStorage.clear(); for(const k in BASE) localStorage.setItem(k,BASE[k]); for(const k in (o||{})) localStorage.setItem(k,typeof o[k]==='string'?o[k]:JSON.stringify(o[k])); try{useIdxDrop()}catch(e){} try{mcInvalidate()}catch(e){} };
const snap=()=>{ const o={}; for(let i=0;i<localStorage.length;i++){ const k=localStorage.key(i); o[k]=localStorage.getItem(k); } return o; };
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
const CH='1. 총칙 > 1.1 민법의 법원';
const NEW=typeof linkChipsRepaint==='function';
const V=(k,v)=>R.push('VAL | '+k+' | '+JSON.stringify(v));
const UNIT=P.quiz.filter(q=>!q.examNo&&q.subChapter==='1.1 민법의 법원').map(q=>q.id);
const chips=el=>el?[...el.querySelectorAll('[data-lkchips] button')].map(x=>x.textContent.trim()):null;
const cardChips=u=>chips(document.getElementById('q-box-'+u));
say('판 = '+(NEW?'NEW(linkChipsRepaint 있음)':'HEAD'));

/* G21 — 카드 「관련 문제」 줄 없음 · 머리 칩 「↩링크N」「↩백링크N」 (add7) */
async function G21(){
  resetLS({ox_q_links:{Q9801:['Q9802'],Q9803:['Q9801'],Q9802:['Q9801'],Q9806:['Q9805',''],Q9807:['q9808'],Q9808:['Q9807']}});
  closeAllWins(); openQuiz(UNIT,'민법총칙',CH);
  const qc=document.getElementById('quiz-container');
  T('G21 카드에 linked-badges- 0', !qc.querySelector('[id^="linked-badges-"]'), qc.querySelectorAll('[id^="linked-badges-"]').length);
  T('G21 카드 글자에 「관련 문제」「나를 연결한 문제」 0', qc.textContent.indexOf('관련 문제')<0&&qc.textContent.indexOf('나를 연결한 문제')<0, (qc.textContent.match(/.{0,20}(관련 문제|나를 연결한 문제).{0,10}/)||[''])[0]);
  const want={Q9801:['↩링크1','↩백링크1'],Q9802:['↩링크1'],Q9803:['↩링크1'],Q9804:[],Q9805:['↩백링크1'],Q9806:['↩링크1'],Q9807:['↩링크1'],Q9808:['↩링크1']};
  const got={}; Object.keys(want).forEach(u=>{ got[u]=cardChips(u); });
  T('G21 링크 1·백링크 1 인 문항(Q9801) — 「↩링크1」·「↩백링크1」 둘', J(got.Q9801)===J(want.Q9801), J(got.Q9801));
  T('G21 겹치는 uid 는 백링크에서 뺌(Q9802 · 대소문자 다른 겹침 Q9807·Q9808)', J(got.Q9802)===J(want.Q9802)&&J(got.Q9807)===J(want.Q9807)&&J(got.Q9808)===J(want.Q9808), J([got.Q9802,got.Q9807,got.Q9808]));
  T('G21 둘 다 0 이면 글자 0(Q9804) · 백링크만(Q9805) · 빈 칸은 안 셈(Q9806 링크1)', J(got.Q9804)===J([])&&J(got.Q9805)===J(want.Q9805)&&J(got.Q9806)===J(want.Q9806), J([got.Q9804,got.Q9805,got.Q9806]));
  await wait(150);
  const bs=[...document.getElementById('q-box-Q9801').querySelectorAll('[data-lkchips] button')];
  const lk=bs[0], bk=bs[1];
  const pill=el=>/(^|\s)(rounded(-\S+)?|border)(\s|$)/.test(el.className)||/(^|\s)bg-(?!transparent(\s|$))\S+/.test(el.className);
  T('G21 알약 class(rounded·border·bg-) 없음 · 남색 text-blue-900 · 연두 text-lime-700 · 계산 색', !!lk&&!!bk&&!pill(lk)&&!pill(bk)&&/(^|\s)text-blue-900(\s|$)/.test(lk.className)&&/(^|\s)text-lime-700(\s|$)/.test(bk.className)&&getComputedStyle(lk).color==='rgb(30, 58, 138)'&&getComputedStyle(bk).color==='rgb(77, 124, 15)', lk&&bk?[lk.className,getComputedStyle(lk).color,bk.className,getComputedStyle(bk).color].join(' | '):'없음');
  T('G21 title 「내가 연결한 문제」·「나를 연결한 문제」 · N 을 글자에 붙여 씀', !!lk&&!!bk&&lk.title==='내가 연결한 문제'&&bk.title==='나를 연결한 문제'&&/^↩링크\d+$/.test(lk.textContent)&&/^↩백링크\d+$/.test(bk.textContent), lk&&bk?lk.title+' / '+bk.title:'');
  if(lk) lk.click();
  const w1=document.getElementById('oxwin-rel-mine-Q9801');
  T('G21 「↩링크1」 누르면 「내가 연결한 문제」 창 · 행 Q9802', !!w1&&w1.innerHTML.indexOf("openQPopup('Q9802')")>=0, w1?w1.textContent.slice(0,80):'창 없음');
  if(bk) bk.click();
  const w2=document.getElementById('oxwin-rel-back-Q9801');
  const rows2=w2?[...w2.querySelectorAll('button[onclick^="openQPopup"]')]:[];
  T('G21 「↩백링크1」 누르면 「↩ 백링크 · 나를 연결한 문제」 창 · 안내 글 · 행 Q9803 하나(겹친 Q9802 없음)', !!w2&&w2.textContent.indexOf('↩ 백링크 · 나를 연결한 문제')>=0&&w2.textContent.indexOf('이 문제를 연결해 둔 다른 문제 — 누르면 창으로 열립니다')>=0&&rows2.length===1&&rows2[0].getAttribute('onclick')==="openQPopup('Q9803')", w2?w2.textContent.slice(0,120):'창 없음');
  if(rows2[0]) rows2[0].click();
  T('G21 백링크 창 행 누르면 문항 팝업', !!document.getElementById('oxwin-q-Q9803'));
  closeAllWins();
  if(typeof openJeongni==='function') openJeongni('민법총칙','1.1');
  const jt=chips(document.querySelector('[data-jnrow="Q9801"]'));
  T('G21 정리 창 행도 같은 글자', J(jt)===J(want.Q9801), J(jt));
  closeAllWins();
  openQPopup('Q9801');
  const pw=document.getElementById('oxwin-q-Q9801');
  T('G21 문항 팝업도 같은 글자 · 옛 「↩ 연결」 단추 0', J(chips(pw))===J(want.Q9801)&&!!pw&&pw.textContent.indexOf('↩ 연결')<0, J(chips(pw)));
  closeAllWins(); showHome();
}

/* G22 — 연결 상자 「↪ 그 문제 보기」 → 문항 팝업 · 「✏️ 연결」 칸 (add8) */
async function G22(){
  const gI=(k,i,t)=>({k:k,i:i,t:t,ok:null,ts:1789000000000,cs:[]});
  resetLS({ox_q_geunge:{Q9801:[gI('g_Q9801_a',1,'내 근거')],Q9802:[gI('g_Q9802_a',1,'연결될 근거 하나')]},ox_q_reflinks:{Q9801:{geunge:['Q9802']}}});
  closeAllWins(); openQuiz(UNIT,'민법총칙',CH);
  const rbox=document.getElementById('refgg-box-Q9801-Q9802');
  const go=rbox?[...rbox.querySelectorAll('button')].find(b=>b.textContent.trim()==='↪ 그 문제 보기'):null;
  T('G22 연결 상자에 「↪ 그 문제 보기」 그대로', !!go);
  if(go) go.click();
  const w=document.getElementById('oxwin-q-Q9802');
  T('G22 「↪ 그 문제 보기」 → 문항 팝업(oxwin-q-) · 비교 창(oxwin-cmp-) 0', !!w&&!document.getElementById('oxwin-cmp-Q9802'), 'q '+!!w+' · cmp '+!!document.getElementById('oxwin-cmp-Q9802'));
  if(!w){ closeAllWins(); showHome(); return; }
  const btns=[...w.querySelectorAll('button')].map(b=>b.textContent.trim());
  T('G22 팝업 꼴 — 칩 줄(uid)·지문·qp-gg-box-·「정답·해설 보기」·「✏️ 연결」·「🃏」·「↪ 이 문제로 이동」', w.textContent.indexOf('카드 지문 Q9802')>=0&&w.textContent.indexOf('Q9802')>=0&&!!document.getElementById('qp-gg-box-Q9802')&&btns.indexOf('정답·해설 보기')>=0&&btns.indexOf('✏️ 연결')>=0&&btns.some(t=>t.indexOf('🃏')===0)&&btns.indexOf('↪ 이 문제로 이동')>=0, J(btns));
  T('G22 부제 「… 에서 열었습니다」 없음', w.textContent.indexOf('에서 열었습니다')<0);
  const ans=document.getElementById('qpop-ans-Q9802');
  T('G22 정답 글자는 누르기 전 안 보인다', !!ans&&ans.style.display==='none'&&w.innerText.indexOf('정답 X')<0, ans?ans.style.display:'없음');
  const eb=[...w.querySelectorAll('button')].find(b=>b.textContent.trim()==='✏️ 연결');
  if(eb) eb.click();
  const lb=document.getElementById('qp-link-box-Q9802');
  T('G22 「✏️ 연결」 → 칸 펴짐(qp-link-input- · 🔍 찾아서 넣기 · 논리 칸 없음)', !!lb&&lb.style.display==='block'&&!!document.getElementById('qp-link-input-Q9802')&&!!document.getElementById('qp-link-search-Q9802')&&lb.textContent.indexOf('논리')<0, lb?lb.style.display:'없음');
  const sb=document.getElementById('qp-link-search-Q9802');
  if(sb){ sb.value='Q9804'; sb.dispatchEvent(new Event('input',{bubbles:true})); }
  const rb=document.getElementById('qp-link-results-Q9802');
  const hit=rb?[...rb.querySelectorAll('button')].find(b=>(b.getAttribute('onclick')||'')==="addLinkId('Q9802','Q9804','qp-')"):null;
  T('G22 찾아서 넣기 → 결과 칸에 Q9804(범위 qp-)', !!hit&&!rb.classList.contains('hide'), rb?rb.innerHTML.slice(0,200):'없음');
  if(hit) hit.click();
  T('G22 결과를 누르면 qp-link-input- 에 들어가고 결과 칸 접힘', (document.getElementById('qp-link-input-Q9802')||{}).value==='Q9804'&&!!rb&&rb.classList.contains('hide'), (document.getElementById('qp-link-input-Q9802')||{}).value);
  const before=cardChips('Q9802');
  const s0=snap();
  const sv=lb?[...lb.querySelectorAll('button')].find(b=>b.textContent.trim()==='저장하기'):null;
  if(sv) sv.click();
  const ch=diffKeys(s0,snap());
  T('G22 저장 → ox_q_links[Q9802] = [Q9804] · 쓴 키는 ox_q_links 하나', J(lsO('ox_q_links').Q9802)===J(['Q9804'])&&J(ch)===J(['ox_q_links']), J({l:lsO('ox_q_links'),ch}));
  T('G22 카드 「↩링크N」 수 오름(없음 → ↩링크1) · 넣은 Q9804 카드에 「↩백링크1」', J(before)===J([])&&J(cardChips('Q9802'))===J(['↩링크1'])&&J(cardChips('Q9804'))===J(['↩백링크1']), J([before,cardChips('Q9802'),cardChips('Q9804')]));
  T('G22 저장 뒤 팝업 글자도 「↩링크1」 · 칸 접힘', J(chips(w))===J(['↩링크1'])&&!!lb&&lb.style.display==='none', J(chips(w)));
  T('G22 앱 전체에 cmp- id 0 · GG_SCOPES 에 비교 창 범위 없음', !document.querySelector('[id^="cmp-"]')&&J(GG_SCOPES)===J(['','qp-','jn-']), J(GG_SCOPES));
  closeAllWins(); showHome();
}

/* G23 — 목차 회독 배지 빨간 X · 카드 태그 단추 바탕·테두리 없이 · 꺼진 것만 회색 (add9) */
async function G23(){
  const hist={}; hist['민법총칙||'+CH+'||all||all']=[{score:18,total:20,date:'2026. 9. 15.',marks:Object.fromEntries(UNIT.slice(0,20).map((u,n)=>[u,n>=2]))}];
  resetLS({ox_chap_history:hist,ox_q_tags:{Q9801:{confuse:true,fake:false,concept:true,memo:false,important:false}}});
  loadQuiz(); showHome(); closeAllWins(); clearWrongCache(); renderDashboard();
  await wait(120);
  const row=document.querySelector('[data-trrow="민법총칙|||'+CH+'"]');
  const badge=row?[...row.querySelectorAll('button')].find(b=>/1회독/.test(b.textContent)):null;
  const x=badge?[...badge.querySelectorAll('span')].find(s=>s.textContent==='X'):null;
  const btxt=badge?badge.textContent.replace(/\s+/g,' ').trim():'없음';
  T('G23 목차 회독 배지에 🔴 0 · 빨간 X(text-red-600 font-black) 뒤에 틀린 수', !!badge&&btxt.indexOf('🔴')<0&&!!x&&x.classList.contains('text-red-600')&&x.classList.contains('font-black')&&getComputedStyle(x).color==='rgb(220, 38, 38)'&&/X2 \/20/.test(btxt), btxt+(x?' · '+getComputedStyle(x).color:''));
  openQuiz(UNIT,'민법총칙',CH);
  await wait(250);
  const box=document.getElementById('q-box-Q9801');
  const tg=box?[...box.querySelectorAll('button[id^="tag-"]')]:[];
  const emo=tg.map(b=>b.textContent.replace(/\s+\d+$/,'').trim());
  T('G23 카드 태그 단추 6 · 이모지 그대로(📍🌀⚠️💡🧠⭐)', tg.length===6&&J(emo)===J(['📍','🌀','⚠️','💡','🧠','⭐']), J(emo));
  const badCls=el=>el.className.split(/\s+/).filter(c=>/^rounded/.test(c)||c==='border'||(/^border-/.test(c)&&c!=='border-0')||(/^bg-/.test(c)&&c!=='bg-transparent')||/^shadow/.test(c));
  const bads=tg.map(badCls).filter(a=>a.length);
  T('G23 border·bg-·rounded·shadow class 0(bg-transparent·border-0 만) · 계산 바탕 투명 · 테두리 0', tg.length===6&&!bads.length&&tg.every(b=>{ const cs=getComputedStyle(b); return cs.backgroundColor==='rgba(0, 0, 0, 0)'&&cs.borderTopWidth==='0px'; }), J(bads)+' · '+tg.map(b=>getComputedStyle(b).backgroundColor+'/'+getComputedStyle(b).borderTopWidth).join(','));
  const fl=id=>{ const b=document.getElementById(id); return b?getComputedStyle(b).filter:'없음'; };
  const offIds=['tag-fake-Q9801','tag-memo-Q9801','tag-important-Q9801','tag-coord-Q9801'];
  T('G23 켜진 것(🌀 헷갈림·💡 개념) filter 없음 · 꺼진 것(⚠️·🧠·⭐·📍 자리 없음) grayscale', fl('tag-confuse-Q9801')==='none'&&fl('tag-concept-Q9801')==='none'&&offIds.every(id=>/grayscale\(1\)/.test(fl(id))), J(['tag-confuse-Q9801','tag-concept-Q9801'].concat(offIds).map(fl)));
  const tfb=document.getElementById('tag-fake-Q9801'); if(tfb) tfb.style.transition='none';   /* .tag-btn 의 transition:all 0.2s — 헤드리스 가상 시간에서는 끝나지 않아 끝 상태를 재려고 이 단추만 끈다(앱에서는 0.2s 동안 바뀐다) */
  toggleTag('Q9801','fake');
  const f1=fl('tag-fake-Q9801'), c1=(document.getElementById('tag-fake-Q9801')||{}).className||'';
  toggleTag('Q9801','fake');
  const f2=fl('tag-fake-Q9801');
  T('G23 toggleTag 뒤 바뀜(⚠️ 켬 → filter 없음 · 끔 → grayscale)', f1==='none'&&c1.indexOf('grayscale')<0&&/grayscale\(1\)/.test(f2), J([f1,c1,f2]));
  const fb=document.getElementById('tag-fake-Q9801'), rr=fb?fb.getBoundingClientRect():{width:0,height:0};
  T('G23 태그 단추 22×22 · title 글자(좌표·헷갈림·페이크·개념·암기·중요)', Math.round(rr.width)===22&&Math.round(rr.height)===22&&J(tg.map(b=>b.title.split(' · ')[0]))===J(['좌표','헷갈림','페이크','개념','암기','중요']), rr.width+'×'+rr.height+' · '+J(tg.map(b=>b.title)));
  goHome();
  startQuiz('변리사 기출','2016년 제53회');
  await wait(250);
  const exb=document.getElementById('q-box-Q9901');
  const et=exb?[...exb.querySelectorAll('button[id^="tag-"]')]:[];
  T('G23 기출뷰 태그 단추 5(⭐ 없음) · 같은 규칙', et.length===5&&!et.map(badCls).some(a=>a.length), et.length+' · '+J(et.map(b=>b.textContent.trim())));
  goHome();
}

/* G24 — 「근거에서 찾기」 한 번 파싱 · 근거 있는 문항만 · 입력 모으기 · 결과 글자 무변 (add10) */
async function G24(){
  const gst={}, lcg=(()=>{ let s=7; return ()=>(s=(s*1103515245+12345)%2147483648); })();
  const ns=[]; for(let n=1;n<=120;n++) ns.push(n);
  for(let i=ns.length-1;i>0;i--){ const j=lcg()%(i+1); const t=ns[i]; ns[i]=ns[j]; ns[j]=t; }   /* 넣는 차례를 섞는다 — Object.keys 차례가 quizData 차례와 달라야 차례 복원을 잰다 */
  ns.forEach(n=>{
    const u='Q7'+String(n).padStart(3,'0'), L=[];
    if(n%2===0) L.push({k:'g_'+u+'_a',i:1,t:'공통검색어 '+n+'번 근거',ok:null,ts:1,cs:[]});
    if(n%10===3) L.push({k:'g_'+u+'_b',i:L.length+1,t:'평범한 글 '+n,ok:null,ts:1,cs:[{k:'c1',t:'댓글만 걸림 '+n,ts:1}]});
    if(n%15===0) L.push({k:'g_'+u+'_c',i:L.length+1,t:'',ok:null,ts:1,cs:[]});
    if(n%7===0&&!L.length) L.push({k:'g_'+u+'_d',i:1,t:'',ok:null,ts:1,cs:[]});   /* 글 없는 항목만 — 옛 판도 후보에서 뺀다 */
    if(L.length) gst[u]=L;
  });
  gst.Q9801=[{k:'g_Q9801_a',i:1,t:'공통검색어 주인 문항(자기는 빠진다)',ok:null,ts:1,cs:[]}];
  gst.Q9802=[{k:'g_Q9802_a',i:1,t:'공통검색어 카드 문항',ok:null,ts:1,cs:[]}];
  resetLS({ox_q_geunge:gst, ox_q_memos:{Q7004:'메모 공통검색어',Q9803:'메모 글 둘'}, ox_q_links:{Q9801:['Q7010']}, ox_q_reflinks:{Q9801:{geunge:['Q7020']}}});
  closeAllWins(); openQuiz(UNIT,'민법총칙',CH);
  const inp=document.getElementById('link-search-geunge-Q9801'), box=document.getElementById('link-results-geunge-Q9801');
  T('G24 카드 근거 찾기 칸·결과 칸이 있다', !!inp&&!!box);
  if(!inp||!box){ showHome(); return; }
  for(const term of ['공통검색어','댓글만','Q70']){
    inp.value=term; linkSearch('Q9801','geunge');
    V('G24.geunge.'+term, box.innerHTML);
  }
  inp.value='공통검색어'; linkSearch('Q9801','geunge');
  const rows=[...box.querySelectorAll('button')].map(b=>{ const m=(b.getAttribute('onclick')||'').match(/,'geunge','(Q\d+)'/); return m?m[1]:'?'; });
  const ord=rows.map(u=>P.quiz.findIndex(q=>q.id===u));
  T('G24 「공통검색어」 30건에서 자름 · quizData 차례 · 자기(Q9801) 빠짐', rows.length===30&&ord.every((v,i)=>v>=0&&(i===0||ord[i-1]<v))&&rows.indexOf('Q9801')<0, J(rows.slice(0,6))+' … '+rows.length);
  const oS=window.ggStore, oP=JSON.parse; let nS=0, nP=0, nF=0;
  window.ggStore=function(){ nS++; return oS.apply(this,arguments); };
  JSON.parse=function(){ nP++; return oP.apply(this,arguments); };
  quizData.find=function(){ nF++; return Array.prototype.find.apply(this,arguments); };
  inp.value='공'; linkSearch('Q9801','geunge');
  window.ggStore=oS; JSON.parse=oP; delete quizData.find;
  T('G24 한 글자 찾기 한 번에 ggStore 호출 ≤ 1 · quizData.find 0', nS<=1&&nF===0, J({ggStore:nS,JSONparse:nP,find:nF}));
  say('G24 한 글자 찾기 한 번 — ggStore '+nS+'번 · JSON.parse '+nP+'번 · quizData.find '+nF+'번(문항 '+quizData.length+' · 근거 문항 '+Object.keys(gst).length+')');
  let nL=0; const oL=window.linkSearch;
  window.linkSearch=function(){ nL++; return oL.apply(this,arguments); };
  ['공','공통','공통검','공통검색','공통검색어'].forEach(v=>{ inp.value=v; inp.dispatchEvent(new Event('input',{bubbles:true})); });
  const n0=nL;
  await wait(300);
  const n1=nL;
  inp.dispatchEvent(new FocusEvent('focus'));
  const n2=nL;
  window.linkSearch=oL;
  T('G24 타자 다섯 번 → 바로는 안 찾고 120ms 모아 한 번 · onfocus 는 즉시', n0===0&&n1===1&&n2===2&&box.querySelectorAll('button').length===30, J({바로:n0,모은뒤:n1,포커스뒤:n2,결과:box.querySelectorAll('button').length}));
  const li=document.getElementById('link-search-Q9801'), lb=document.getElementById('link-results-Q9801');
  if(li&&lb){ li.value='Q70'; linkSearch('Q9801'); V('G24.links.Q70', lb.innerHTML); }
  const mi=document.createElement('input'); mi.id='link-search-memo-Q9801'; mi.value='메모'; const mb=document.createElement('div'); mb.id='link-results-memo-Q9801';
  document.body.appendChild(mi); document.body.appendChild(mb);
  linkSearch('Q9801','memo'); V('G24.memo.메모', mb.innerHTML);
  const memoN=mb.querySelectorAll('button').length;
  mi.remove(); mb.remove();
  T('G24 유사문제·메모 갈래도 결과가 나온다(글자 대조는 VAL)', !!lb&&lb.querySelectorAll('button').length>0&&memoN>0, J({links:lb?lb.querySelectorAll('button').length:-1,memo:memoN}));
  const extra=[]; for(let i=1;i<=5400;i++) extra.push({id:'QT'+String(i).padStart(4,'0'),subject:'시간재기',chapter:'x',subChapter:'x',q:'시간 재기 지문 '+i,exp:'',a:'O',displayNo:i,probNum:i,subNum:'',source:''});
  const big={}; for(let i=1;i<=1100;i++) big['QT'+String(i*4).padStart(4,'0')]=[{k:'g'+i,i:1,t:'시간 재기 근거 글 '+i+' 가나다라마바사아자차카타파하 가나다라마바사아자차카타파하',ok:null,ts:1,cs:[]}];
  extra.forEach(q=>quizData.push(q));
  localStorage.setItem('ox_q_geunge', J(Object.assign({}, gst, big)));
  let nP2=0; const oP2=JSON.parse; JSON.parse=function(){ nP2++; return oP2.apply(this,arguments); };
  inp.value='근거'; const t0=performance.now(), d0=Date.now(); linkSearch('Q9801','geunge'); const ms=performance.now()-t0, dms=Date.now()-d0;
  JSON.parse=oP2;
  say('G24 (대조용) 문항 '+quizData.length+' · 근거 문항 '+(Object.keys(gst).length+1100)+' 에서 linkSearch(Q9801,geunge) 한 번 — JSON.parse '+nP2+'번 · performance.now '+ms.toFixed(1)+'ms · Date.now '+dms+'ms(헤드리스 가상 시간은 스크립트 도는 동안 멈춰 0 에 가깝게 찍힐 수 있다 — JSON.parse 횟수가 더 믿을 만한 잣대)');
  quizData.splice(quizData.length-5400, 5400);
  closeAllWins(); showHome();
}

/* G10 — 헤드리스 화면 열림(콘솔 오류는 끝에서) */
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
  if(pin) pin.click();
  let cd=null;
  for(let i=0;i<200&&!(cd=document.getElementById('cd-close'));i++) await wait(50);
  T('G10 정리OMR(좌표기억) 뷰어가 열린다(카드 📍 단추)', !!pin&&!!cd&&__ALERTS.length===a0, 'pin '+!!pin+' · cd-close '+!!cd+' · alert '+__ALERTS.slice(a0).join('/'));
  if(cd) cd.click();
  goHome();
}

const LIST=[['G21',G21],['G22',G22],['G23',G23],['G24',G24],['G10',G10]].filter(x=>P.skip.indexOf(x[0])<0);
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
