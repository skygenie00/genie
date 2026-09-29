window.onload=null;
(function(){
/* _task_ox_ink_add1 §C G5·G6 — 실시간 크롬(가상 시계 없음)에서 페이지를 읽는 동안 동기로 돈다.
   실제 앱 크기를 흉내 낸 결정적 데이터(문항 5,548 · 근거 1,195문항 · 연결·참조·형광펜·유형·태그 저장소)로
   ① 렌더 1회의 localStorage.getItem 횟수(키마다) ② 헬퍼마다 걸린 시간 ③ renderQuizPage·qiToggle 시간을 잰다.
   ⚠ 시간 = 스크립트 + 강제 레이아웃(두 판 모두 렌더 뒤 offsetHeight 를 읽어 같게 맞춘다) · Tailwind CDN 의 뒤처리(MutationObserver)는 스크립트가 끝난 뒤라 안 들어간다 */
const P=__P__;
const R=[];
const out=x=>{ R.push(x); console.log('HZR|'+encodeURIComponent(x)); };   /* 잰 즉시 내보낸다 — 뒤에서 죽어도 앞 줄은 남는다 */
const T=(n,c,i)=>out((c?'PASS':'FAIL')+' | '+n+((i!==undefined&&!c)?' | '+String(i).replace(/\n/g,'⏎').slice(0,500):''));
const say=s=>out('INFO | '+String(s).replace(/\n/g,'⏎'));
const M=(k,v)=>out('MEAS | '+k+' | '+JSON.stringify(v));
const J=v=>JSON.stringify(v);
const now=()=>performance.now();
const t00=now();
const NEW=typeof GG_PAGE!=='undefined';
say('판 = '+(NEW?'NEW(GG_PAGE 있음)':'HEAD')+' · 실시간');
try{
  let seed=20260916; const rnd=()=>(seed=(seed*1103515245+12345)%2147483648)/2147483648;
  const syl='가나다라마바사아자차카타파하거너더러머버서어저처커터퍼허고노도로모보소오조초코토포호';
  const txt=n=>{ let s=''; for(let i=0;i<n;i++){ s+=syl[Math.floor(rnd()*syl.length)]; if(rnd()<0.18) s+=' '; } return s; };
  const N=P.n, id=i=>'Q'+String(10000+i);
  const subs=['1.1 민법의 법원','1.2 신의칙','2.1 권리능력','2.2 행위능력','3.1 법인'];
  quizData.length=0;
  for(let i=0;i<N;i++){
    quizData.push({id:id(i),subject:'민법총칙',chapter:'1. 총칙',subChapter:subs[i%subs.length],subNum:'',q:txt(60+Math.floor(rnd()*60)),exp:txt(120+Math.floor(rnd()*160)),
      a:rnd()<0.5?'O':'X',displayNo:i+1,probNum:i+1,source:'변리사 '+(10+i%15),panrye:rnd()<0.3?(Math.floor(rnd()*600)+'다'+100):'',
      yuje:rnd()<0.05?(id(Math.floor(rnd()*N))+', '+id(Math.floor(rnd()*N))):'',jomun:rnd()<0.3?('제'+(1+Math.floor(rnd()*1000))+'조'):'',examMeta:[],caseText:'',stem:'',status:''});
  }
  localStorage.clear();
  const BASE={'ox_uid_migrated':'1','ox_gg_okreset':'1','ox_gg_memo_merged':'{"at":1,"moved":0,"links":0}','ox_gg_logic_merged':'{"at":1,"moved":0,"links":0}','ox_auto_important_v2':'1'};
  for(const k in BASE) localStorage.setItem(k,BASE[k]);
  const gg={}, links={}, ref={}, marks={}, types={}, tags={}, hist={};
  for(let n=0;n<P.gg;n++){ const u=id(Math.floor(n*N/P.gg)); const L=[]; const m=1+Math.floor(rnd()*3);
    for(let j=0;j<m;j++) L.push({k:'g_'+u+'_'+j,i:j+1,t:txt(P.ggLen+Math.floor(rnd()*P.ggLen)),ok:rnd()<0.5?null:(rnd()<0.5),ts:1789000000000+n,cs:rnd()<0.3?[{k:'c_'+u+'_'+j,t:txt(60),ts:1789000000000}]:[]});
    gg[u]=L; }
  for(let n=0;n<800;n++) links[id(Math.floor(rnd()*N))]=[id(Math.floor(rnd()*N)),id(Math.floor(rnd()*N))];
  for(let n=0;n<150;n++) ref[id(Math.floor(rnd()*N))]={geunge:[id(Math.floor(n*N/P.gg)*0+Math.floor(rnd()*N))]};
  for(let n=0;n<3000;n++) marks['q-'+id(Math.floor(rnd()*N))]=[[0,4,'y']];
  for(let n=0;n<2000;n++) types[id(Math.floor(rnd()*N))]=['조문형','판례형','혼합'][n%3];
  for(let n=0;n<1500;n++) tags[id(Math.floor(rnd()*N))]={fake:rnd()<0.3,concept:rnd()<0.3,memo:false,confuse:rnd()<0.2,important:false};
  for(let n=0;n<3000;n++) hist[id(Math.floor(rnd()*N))]=[{d:'2026-09-01',ok:rnd()<0.6}];
  /* 이 쪽 20카드 중 몇 장에 확실히 달리게 — 근거·연결·참조·형광펜 */
  const pageIds=[]; for(let i=0;i<N&&pageIds.length<20;i++) if(i%subs.length===0) pageIds.push(id(i));
  pageIds.forEach((u,n)=>{ if(n%2===0&&!gg[u]) gg[u]=[{k:'g_'+u+'_p',i:1,t:txt(300),ok:null,ts:1789000000000,cs:[]}]; if(n%3===0) links[u]=[pageIds[(n+1)%20]]; if(n%5===0) ref[u]={geunge:[pageIds[(n+2)%20]]}; if(n%4===0) marks['q-'+u]=[[0,6,'y']]; });
  const setJ=(k,v)=>{ const s=JSON.stringify(v); localStorage.setItem(k,s); return s.length; };
  const sizes={ox_q_geunge:setJ('ox_q_geunge',gg),ox_q_links:setJ('ox_q_links',links),ox_q_reflinks:setJ('ox_q_reflinks',ref),ox_q_marks:setJ('ox_q_marks',marks),ox_q_type:setJ('ox_q_type',types),ox_q_tags:setJ('ox_q_tags',tags),ox_q_history:setJ('ox_q_history',hist)};
  say('데이터 — 문항 '+N+' · 근거 문항 '+Object.keys(gg).length+' · 저장소 글자 수 '+J(sizes)+' · 합 '+Object.values(sizes).reduce((a,b)=>a+b,0));
  try{useIdxDrop()}catch(e){} try{mcInvalidate()}catch(e){}
  currentSubject='민법총칙'; currentChapterLabel='1. 총칙 > 1.1 민법의 법원'; isExamMode=false; currentPageIndex=0; currentSessionMarks={}; resumePicks={}; currentSessionScore=0; lastGradeResults=null;
  if(typeof chapterSaved!=='undefined') chapterSaved=null;
  currentFilteredData=quizData.filter(q=>q.subChapter==='1.1 민법의 법원');
  document.getElementById('home-screen').classList.add('hide'); document.getElementById('quiz-screen').classList.remove('hide');
  const host=document.getElementById('quiz-container'); const lay=()=>void host.offsetHeight;
  let w0=now(); renderQuizPage(); lay(); say('첫 렌더 '+(now()-w0).toFixed(0)+'ms'); w0=now(); renderQuizPage(); lay(); say('둘째 렌더 '+(now()-w0).toFixed(0)+'ms');
  const shown=[...host.querySelectorAll('.question-box')].map(b=>b.id.replace('q-box-',''));
  say('이 쪽 카드 '+shown.length+'장 · 첫 카드 '+shown[0]);
  const count=fn=>{ const og=Storage.prototype.getItem, cnt={}; Storage.prototype.getItem=function(k){ cnt[k]=(cnt[k]||0)+1; return og.call(this,k); }; try{ fn(); } finally{ Storage.prototype.getItem=og; } return cnt; };
  const c1=count(()=>renderQuizPage()); lay();
  M('G5.getItem.marksOn', c1);
  say('G5 렌더 1회 getItem(형광펜 켠 채 · 20카드) '+J(c1)+' · 합 '+Object.values(c1).reduce((a,b)=>a+b,0));
  T('G5 렌더 1회 — 근거 저장소(ox_q_geunge) getItem 1회 · ox_q_links 1회 이하', c1['ox_q_geunge']===1&&(c1['ox_q_links']||0)<=1, J({ox_q_geunge:c1['ox_q_geunge'],ox_q_links:c1['ox_q_links']}));
  const names=['typeChipHTML','bookChipHTML','samePanryeChipHTML','myLinkChipHTML','yujeChipHTML','yujeBackChipHTML','mcChipHTML','ggLineHTML','actionBarHTML','markHTML','qiAfterRender'];
  const acc={}, orig={};
  names.forEach(nm=>{ if(typeof window[nm]!=='function') return; orig[nm]=window[nm]; acc[nm]=0; window[nm]=function(){ const a=now(); try{ return orig[nm].apply(this,arguments); } finally{ acc[nm]+=now()-a; } }; });
  const RN=2; let a0=now(); for(let i=0;i<RN;i++){ renderQuizPage(); lay(); } const tot=(now()-a0)/RN;
  names.forEach(nm=>{ if(orig[nm]) window[nm]=orig[nm]; });
  M('PROF', {render:+tot.toFixed(2), helpers:Object.fromEntries(names.filter(n=>acc[n]!==undefined).map(n=>[n,+(acc[n]/RN).toFixed(2)]))});
  say('프로파일(렌더 '+RN+'회 평균 · 헬퍼를 감싼 채 · ms) 렌더 '+tot.toFixed(1)+' · '+names.filter(n=>acc[n]!==undefined).map(n=>n+' '+(acc[n]/RN).toFixed(1)).join(' · '));
  const rs=[]; for(let i=0;i<3;i++){ const a=now(); renderQuizPage(); lay(); rs.push(now()-a); }
  const tg=[]; for(let i=0;i<4;i++){ const a=now(); qiToggle(); lay(); tg.push(now()-a); }
  const c2=count(()=>{ qiToggle(); }); lay();
  M('G5.getItem.toggle', c2);
  if(!cardMarksOn){ qiToggle(); lay(); }
  const med=a=>a.slice().sort((x,y)=>x-y)[Math.floor(a.length/2)];
  M('G6', {render:rs.map(x=>+x.toFixed(2)), renderMed:+med(rs).toFixed(2), toggle:tg.map(x=>+x.toFixed(2)), toggleSum:+tg.reduce((a,b)=>a+b,0).toFixed(2)});
  say('G6 renderQuizPage 5회 ms '+rs.map(x=>x.toFixed(1)).join(', ')+' (가운데 '+med(rs).toFixed(1)+') · qiToggle 왕복 2회(4번) ms '+tg.map(x=>x.toFixed(1)).join(', ')+' · 합 '+tg.reduce((a,b)=>a+b,0).toFixed(1));
  say('G5 필기모드로 가는 qiToggle 1회 getItem '+J(c2));
}catch(e){ T('G5 성능 시험이 죽었다',false,e.message+' | '+(e.stack||'').split('\n').slice(1,3).join(' ')); }
const errs=(window.__ERR||[]), cerr=(window.__CERR||[]);
T('G10 페이지 오류 0 · console.error 0(실시간 판)', errs.length===0&&cerr.length===0, 'error '+errs.length+' '+errs.slice(0,3).join(' / ')+' · console.error '+cerr.length+' '+cerr.slice(0,3).join(' / '));
say('전체 '+(now()-t00).toFixed(0)+'ms');
console.log('HZR|END');
})();
