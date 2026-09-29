/* _harness_jo_ms_notecolor_tests.js — _task_jo_ms_notecolor 하네스가 페이지에 넣는 도구(__HN).
   BASE(omrpop 인도 판)·NEW 둘 다에 같은 것을 넣는다 — 없는 것(span.nc · 머리 「정리 색」 · 색 창 …)은 빈 값으로 돌려준다(헛잣대).
   재는 것 = DOM 실물(span.nc 수 · 색 · 규칙 · 자리) · 계산 스타일 · elementFromPoint · 저장소 값(localStorage jopangi.notecolor · jopangi_ui). */
(function(){
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const txt=e=>e?(e.textContent||'').replace(/\s+/g,' ').trim():'';
const R=e=>{if(!e)return null;const r=e.getBoundingClientRect();
  return {x:+r.left.toFixed(2),y:+r.top.toFixed(2),w:+r.width.toFixed(2),h:+r.height.toFixed(2),r:+r.right.toFixed(2),b:+r.bottom.toFixed(2),
          cx:+(r.left+r.width/2).toFixed(2),cy:+(r.top+r.height/2).toFixed(2)};};
const cs=(e,p)=>e?getComputedStyle(e)[p]:null;
function hitOn(t){const r=R(t);if(!r)return null;const at=document.elementFromPoint(r.cx,r.cy);
  const onScreen=r.cy>0&&r.cy<innerHeight&&r.cx>0&&r.cx<innerWidth;
  return Object.assign(r,{on:!!at&&(at===t||t.contains(at))&&onScreen,at:at?String(at.className||at.tagName).slice(0,60):null,onScreen});}
const pops=()=>(typeof POPS!=='undefined'?POPS:[]);
const popOf=pk=>pops().find(x=>x._pk===pk)||null;
const NK='jopangi.notecolor';
const lsj=k=>{try{return JSON.parse(localStorage.getItem(k)||'null');}catch(e){return null;}};
const notePop=f=>popOf('note|'+PLAW()+'|'+f+'|');
const SKIP='.mdtab,.blockid,.htog,.mdhash,.chip,.embed,.embx,.emtools,.stkanc,.pitflag,.pitwho';
/* 보이는 글자(칠하기가 쓰는 것과 같은 규칙으로 따로 잰다) */
const inLn=(n,ln,sel)=>{for(let e=n.parentElement;e&&e!==ln;e=e.parentElement)if(e.matches(sel))return true;return false;};   /* 그 줄 안쪽에서만 가른다(앱과 같은 규칙) */
function vis(ln){const out=[];const w=document.createTreeWalker(ln,NodeFilter.SHOW_TEXT,{acceptNode:n=>inLn(n,ln,SKIP)?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT});
  let n;while((n=w.nextNode()))out.push(n.nodeValue);return out.join('');}
/* 한 줄의 칠 — 같은 [s,e,r] 를 하나로(글자마다 노드라 한 낱말이 여러 span) */
function spansOf(ln){const m=new Map();ln.querySelectorAll('span.nc').forEach(sp=>{if(sp.parentElement.closest('.ln')!==ln)return;const k=sp.dataset.s+'|'+sp.dataset.e+'|'+sp.dataset.r;
    if(!m.has(k))m.set(k,{s:+sp.dataset.s,e:+sp.dataset.e,r:sp.dataset.r,c:sp.dataset.c,color:cs(sp,'color'),deco:cs(sp,'textDecorationLine')+' '+cs(sp,'textDecorationStyle'),n:0});m.get(k).n++;});
  const t=vis(ln);return [...m.values()].sort((a,b)=>a.s-b.s).map(x=>Object.assign(x,{w:t.slice(x.s,x.e)}));}
window.__HN={
  wait,R,hitOn,
  async boot(law){try{closeAllPops();}catch(e){}S.law=law||'민사소송법';S.tab='jo';await render();await wait(400);return {law:S.law,tab:S.tab};},
  async note(file){try{closeAllPops();}catch(e){}await popNote(file,null,{clientX:130,clientY:120},1);
    for(let i=0;i<300;i++){const w=notePop(file);if(w&&w.querySelector('.ntbox'))break;await wait(50);}await wait(150);return !!notePop(file);},
  noteNames(){return noteData().then(({N})=>Object.keys(N||{}));},
  /* 노트 한 장의 칠 — 줄마다 [행, 보이는 글자, 칠] */
  lines(file){const w=notePop(file);if(!w)return null;return [...w.querySelectorAll('.ntbox > .ntrow > .ln')].map((ln,ri)=>({ri,t:vis(ln),sp:spansOf(ln),ncf:ln.dataset.ncf||null,nri:ln.dataset.nri!=null?+ln.dataset.nri:null}));},
  /* 규칙별 칠 수(한 노트) */
  census(file){const L=__HN.lines(file)||[];const c={};let tot=0;L.forEach(l=>l.sp.forEach(x=>{c[x.r]=(c[x.r]||0)+1;tot++;}));return {c,tot,lines:L.length};},
  head(file){const w=notePop(file);if(!w)return null;const h=w.querySelector('.ph .nchead');if(!h)return {none:true};
    const on=h.querySelector('.ncon'),me=h.querySelector('.ncme');return {t:txt(h),on:!!on&&on.classList.contains('on'),onColor:cs(on,'color'),onW:cs(on,'fontWeight'),me:txt(me),fs:cs(on,'fontSize'),icons:h.querySelectorAll('svg,img,i').length};},
  headAt(file,what){const w=notePop(file);const t=w&&w.querySelector('.ph .nchead '+(what==='me'?'.ncme':'.ncon'));if(!t)return null;return hitOn(t);},
  /* 그 줄에서 낱말 w 의 k 번째 자리를 덮는 span.nc — 없으면 그 글자 노드 자리 */
  at(file,ri,w,k){const pw=notePop(file);const ln=pw&&pw.querySelectorAll('.ntbox > .ntrow > .ln')[ri];if(!ln)return null;const t=vis(ln);let i=-1;for(let j=0;j<=(k||0);j++){i=t.indexOf(w,i+1);if(i<0)return null;}
    try{ln.scrollIntoView({block:'center'});}catch(e){}
    const sp=[...ln.querySelectorAll('span.nc')].find(x=>x.parentElement.closest('.ln')===ln&&+x.dataset.s<=i&&+x.dataset.e>i);
    if(sp){const h=hitOn(sp);return Object.assign(h,{s:+sp.dataset.s,e:+sp.dataset.e,r:sp.dataset.r,c:sp.dataset.c,color:cs(sp,'color')});}
    /* 칠이 없는 글자 — 글자 노드 범위 */
    const w2=document.createTreeWalker(ln,NodeFilter.SHOW_TEXT,{acceptNode:n=>inLn(n,ln,SKIP)?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT});
    let n,acc=0,a=null,ao=0,b=null,bo=0;while((n=w2.nextNode())){const L=n.nodeValue.length;if(a===null&&i<acc+L){a=n;ao=i-acc;}if(a!==null&&i+w.length<=acc+L){b=n;bo=i+w.length-acc;break;}acc+=L;}
    if(!a||!b)return null;const rg=document.createRange();rg.setStart(a,ao);rg.setEnd(b,bo);const rr=rg.getBoundingClientRect();
    return {x:rr.left,y:rr.top,w:rr.width,h:rr.height,cx:rr.left+rr.width/2,cy:rr.top+rr.height/2,r:rr.right,b:rr.bottom,on:true,none:true,s:i,e:i+w.length};},
  /* 색 창 */
  pick(){const p=document.querySelector('.ncpop');if(!p||p.hidden)return null;return {t:txt(p.querySelector('.nct')),sw:[...p.querySelectorAll('.ncsw')].map(b=>({c:b.dataset.c,cur:b.classList.contains('cur'),bg:cs(b,'backgroundColor')})),
    rv:!!p.querySelector('.ncrv'),rect:R(p),text:txt(p),z:+cs(p,'zIndex')||0};},
  pickAt(c){const p=document.querySelector('.ncpop');if(!p||p.hidden)return null;const b=c==='rv'?p.querySelector('.ncrv'):p.querySelector('.ncsw[data-c="'+c+'"]');return b?hitOn(b):null;},
  ls(){return lsj(NK);},
  lsSet(v){localStorage.setItem(NK,JSON.stringify(v));return true;},
  ui(){const u=lsj('jopangi_ui')||{};return {note_color:u.note_color};},
  u(){const u=lsj('jopangi_sync_u')||{};return Object.keys(u).filter(k=>k.indexOf(NK+'|')===0);},
  gone(){const g=lsj('jopangi_sync_gone')||{};return Object.keys(g).filter(k=>k.indexOf(NK+'|')===0);},
  syncKeys(){try{return SYNC_KEYS.slice();}catch(e){return null;}},
  recName(){try{return REC_NAMES.notecolor||null;}catch(e){return null;}},
  /* 2차 카드 임베드 상자 — 그 카드의 민소 노트 블록 줄 칠 */
  async card(code){try{closeAllPops();}catch(e){}S.law='민사소송법';S.tab='cha2';S.boardKind='기출';await render();await wait(300);
    const J=await get('2cha_본문_기출_민소.json');const k=Object.keys(J).find(x=>x===code||x.indexOf(code)>=0);if(!k)return {miss:code};
    await popCard4('기출',k,{clientX:240,clientY:60},1,null,null,'민사소송법');
    for(let i=0;i<300;i++){if(document.querySelector('.embx .embody > .ln'))break;await wait(50);}await wait(700);
    const p=[...POPS].reverse().find(q=>(q._pk||'').indexOf('🧾')>=0);return {k,pk:p?p._pk:null,emb:document.querySelectorAll('.embx').length};},
  embLines(){return [...document.querySelectorAll('.embx .embody > .ln')].map(ln=>({ncf:ln.dataset.ncf||null,nri:ln.dataset.nri!=null?+ln.dataset.nri:null,t:vis(ln),sp:spansOf(ln)}));},
  pitOpen(){return !!document.querySelector('.pitmenu');},
  pitClose(){document.querySelectorAll('.pitmenu').forEach(x=>x.remove());return true;},
  errs(){return (window.__ERR||[]).slice(0,20);},
};
})();
