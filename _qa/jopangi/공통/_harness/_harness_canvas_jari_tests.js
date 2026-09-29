/* _harness_canvas_jari_tests.js — _task_canvas_jari_cand 하네스가 페이지에 넣는 도구(__HJ).
   BASE(b2f7338)·NEW 둘 다에 같은 것을 넣는다 — 없는 것(자리 창 카드 · 찍기 …)은 빈 값으로 돌려준다.
   재는 것 = DOM 실물(있는가 · 몇 개 · 글자 · 자리 getBoundingClientRect · 계산 스타일) · 저장소 값(localStorage) · 창(POPS). */
(function(){
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const txt=e=>e?(e.textContent||'').replace(/\s+/g,' ').trim():'';
const R=e=>{if(!e)return null;const r=e.getBoundingClientRect();
  return {x:+r.left.toFixed(2),y:+r.top.toFixed(2),w:+r.width.toFixed(2),h:+r.height.toFixed(2),r:+r.right.toFixed(2),b:+r.bottom.toFixed(2),
          cx:+(r.left+r.width/2).toFixed(2),cy:+(r.top+r.height/2).toFixed(2)};};
const cs=(e,p)=>e?getComputedStyle(e)[p]:null;
function hitOn(t){const r=R(t);if(!r)return null;const at=document.elementFromPoint(r.cx,r.cy);
  const onScreen=r.cy>0&&r.cy<innerHeight&&r.cx>0&&r.cx<innerWidth;
  return Object.assign(r,{on:!!at&&(at===t||t.contains(at))&&onScreen,at:at?(String(at.className||at.tagName)).slice(0,60):null,onScreen});}
const pops=()=>(typeof POPS!=='undefined'?POPS:[]);
const popOf=pk=>pops().find(x=>x._pk===pk)||null;
const bookPop=()=>pops().find(x=>(x._pk||'').indexOf('cv|book|')===0)||null;
const blkEl=(n,i)=>document.querySelector('#cvWorld .cv-blk[data-p="'+n+'"][data-b="'+i+'"]');
window.__HJ={
  wait,
  async boot(){try{closeAllPops();}catch(e){}S.law='민사소송법';S.tab='omr';await render();
    for(let i=0;i<600;i++){if(document.getElementById('cvStage')&&document.querySelectorAll('#cvWorld .cv-blk').length)break;await wait(50);}
    await wait(500);return {stage:!!document.getElementById('cvStage'),blk:document.querySelectorAll('#cvWorld .cv-blk').length,hj:!!window.__jocvj};},
  /* 블록으로 — NEW 는 읽기 창구 go(jump 의 화면 옮기기) · BASE 는 쪽 칸에 쪽 번호 */
  async go(bid,n,i){if(window.__jocvj&&__jocvj.go)__jocvj.go(bid);
    else{const inp=document.getElementById('cvPg');if(inp){inp.value=String(n);inp.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true}));inp.dispatchEvent(new Event('change',{bubbles:true}));}}
    await wait(400);for(let k=0;k<60;k++){const e=blkEl(n,i);if(e){const h=__HJ.blkAt(n,i);if(h&&h.on)return h;}await wait(50);}return __HJ.blkAt(n,i);},
  blkAt(n,i){const e=blkEl(n,i);if(!e)return null;const r=e.getBoundingClientRect();
    /* 블록은 겹친다(부모 블록 안에 자식 블록) — 이 블록이 맨 위에 오는 점을 격자로 찾는다(가운데에서 가까운 차례) */
    const pts=[];for(let a=1;a<10;a++)for(let b=1;b<10;b++)pts.push([r.left+r.width*a/10,r.top+r.height*b/10]);
    const cx=r.left+r.width/2,cy=r.top+r.height/2;pts.sort((p,q)=>Math.hypot(p[0]-cx,p[1]-cy)-Math.hypot(q[0]-cx,q[1]-cy));
    /* 점 둘레 ±2px 도 모두 이 블록이어야 — 브라우저가 소수 좌표를 정수로 반올림해 옆 블록 경계(0.4px)를 넘은 일이 있다 */
    const mine=(x,y)=>{const t=document.elementFromPoint(x,y);return !!t&&t.closest('.cv-blk')===e;};
    for(const [x0,y0] of pts){const x=Math.round(x0),y=Math.round(y0);if(x<3||y<3||x>innerWidth-3||y>innerHeight-3)continue;
      if(mine(x,y)&&mine(x-2,y)&&mine(x+2,y)&&mine(x,y-2)&&mine(x,y+2))return Object.assign(R(e),{cx:x,cy:y,on:true,onScreen:true,at:'cv-blk'});}
    return Object.assign(hitOn(e),{on:false});},
  sel(){const e=document.querySelector('#cvWorld .cv-blk.on');return e?e.dataset.p+'|'+e.dataset.b:null;},
  chips(){const c=document.getElementById('cvChips');if(!c||c.hidden)return null;
    return [...c.querySelectorAll('.cv-chip')].map(x=>({t:txt(x),cls:x.className,color:cs(x,'color'),bs:cs(x,'borderTopStyle'),bc:cs(x,'borderTopColor'),bg:cs(x,'backgroundColor')}));},
  chipAt(){const c=[...document.querySelectorAll('#cvChips .cv-chip')].find(x=>/^교재/.test(txt(x)));return c?hitOn(c):null;},
  jari(bid){const w=popOf('cv|jari|'+bid);if(!w)return null;const st=w.querySelector('.cv-jst');
    return {st:st?txt(st.querySelector('.t')):null,stCls:st?st.className:null,
      cards:[...w.querySelectorAll('.cv-jc')].map(c=>({t:txt(c),on:c.classList.contains('on'),ok:txt(c.querySelector('[data-ok]')),in:txt(c.querySelector('.in')),inCls:(c.querySelector('.in')||{}).className||''})),
      pick:txt(w.querySelector('[data-pick]')),none:!!w.querySelector('[data-none]'),rv:!!w.querySelector('[data-rv]'),nx:!!w.querySelector('[data-nx]'),
      old:w.querySelectorAll('.cv-lrow[data-mi]').length,miss:/못 찾았다\(자동\)/.test(txt(w)),rect:R(w)};},
  jariAt(bid,what,i){const w=popOf('cv|jari|'+bid);if(!w)return null;let t=null;const cards=w.querySelectorAll('.cv-jc');
    if(what==='card')t=cards[i]?cards[i].querySelector('.r1 b'):null;else if(what==='ok')t=cards[i]?cards[i].querySelector('[data-ok]'):null;
    else if(what==='head')t=w.querySelector('.hd,.phd,.pop-h,.h')||w.firstElementChild;else t=w.querySelector('[data-'+what+']');
    if(!t)return null;try{t.scrollIntoView({block:'nearest'});}catch(e){}return hitOn(t);},
  book(){const bs=pops().filter(x=>(x._pk||'').indexOf('cv|book|')===0);const w=bs[0];if(!w)return {n:0};
    const pg=w.querySelector('.cv-bookpg'),hl=w.querySelector('.cv-bookhl'),box=w.querySelector('.cv-pickbox'),cvs=w.querySelector('.cv-bookpg canvas'),nav=w.querySelector('.cv-booknav');
    return {n:bs.length,pk:bs.map(x=>x._pk),page:nav&&nav.querySelector('#cvBookP')?nav.querySelector('#cvBookP').value:null,nav:txt(nav),
      hl:hl?{l:parseFloat(hl.style.left),t:parseFloat(hl.style.top),w:parseFloat(hl.style.width),h:parseFloat(hl.style.height)}:null,
      pg:R(pg),box:box?{l:parseFloat(box.style.left),t:parseFloat(box.style.top),w:parseFloat(box.style.width),h:parseFloat(box.style.height),rect:R(box)}:null,
      ov:!!w.querySelector('.cv-pickov'),okBtn:txt(w.querySelector('.cv-booknav [data-ok]')),pkBtn:!!w.querySelector('.cv-booknav [data-pk]'),pkOn:!!w.querySelector('.cv-booknav [data-pk].on'),sv:txt(w.querySelector('.cv-booknav [data-sv]')),
      cvsW:cvs?cvs.width:0,loading:/받는 중/.test(txt(w)),err:/받지 못했다/.test(txt(w))?txt(w).slice(0,200):null,rect:R(w)};},
  bookAt(what){const w=bookPop();if(!w)return null;
    const t=w.querySelector(what==='pk'?'.cv-booknav [data-pk]':what==='sv'?'.cv-booknav [data-sv]':what==='ok'?'.cv-booknav [data-ok]':what==='nx'?'.cv-booknav [data-nx]':what==='x'?'.ph button':'.cv-bookpg');
    if(!t)return null;if(what==='pg'){try{t.scrollIntoView({block:'nearest'});}catch(e){}return R(t);}try{t.scrollIntoView({block:'nearest'});}catch(e){}return hitOn(t);},
  async bookReady(){for(let i=0;i<900;i++){const b=__HJ.book();if(b.n&&(b.cvsW>0||b.err)&&!b.loading){await wait(150);return __HJ.book();}await wait(50);}return __HJ.book();},
  /* 창 머리(끌기 손잡이) — 조판기 팝업 틀의 머리 */
  popHeadAt(pk){const w=popOf(pk)||(pk==='book'?bookPop():null);if(!w)return null;const h=w.querySelector('.ph,.phead,.pop-head,.hd')||w.firstElementChild;const r=R(h);return r?Object.assign(r,{cx:r.x+Math.min(60,r.w/3),hitCls:String((document.elementFromPoint(r.x+Math.min(60,r.w/3),r.cy)||{}).className||'')}):null;},
  popRect(pk){const w=popOf(pk)||(pk==='book'?bookPop():null);return w?R(w):null;},
  ls(k){try{return JSON.parse(localStorage.getItem(k)||'null');}catch(e){return null;}},
  lsSet(k,v){localStorage.setItem(k,JSON.stringify(v));return true;},
  filt(){const f=document.querySelector('.cv-scope.f[data-f="jari"]');return f?{t:txt(f),on:f.classList.contains('on'),n:txt(f.querySelector('b'))}:null;},
  filtAt(){const f=document.querySelector('.cv-scope.f[data-f="jari"]');return f?hitOn(f):null;},
  keep(){const w=document.getElementById('cvWorld');return {flt:w.classList.contains('flt'),keep:[...w.querySelectorAll('.cv-blk.keep')].map(e=>e.dataset.p+'|'+e.dataset.b),
    all:[...w.querySelectorAll('.cv-blk')].map(e=>e.dataset.p+'|'+e.dataset.b)};},
  orph(){const w=document.getElementById('cvJariOrph');return w?{t:txt(w),vis:w.style.display!=='none'}:null;},
  hj(k,a){return window.__jocvj&&__jocvj[k]?__jocvj[k](a):null;},
  pops(){return pops().map(x=>x._pk);},
  closeAll(){try{closeAllPops();}catch(e){}return true;},
  /* 교재 창을 닫은 뒤 — 캔버스 가운데가 캔버스인가(덮개가 남아 가로채지 않는가 · 9/22 민법 증상 역검사) */
  stageHit(){const s=document.getElementById('cvStage');if(!s)return null;const r=R(s);const at=document.elementFromPoint(r.cx,r.cy);
    return {in:!!at&&s.contains(at),at:at?String(at.className||at.tagName).slice(0,60):null,ov:document.querySelectorAll('.cv-pickov').length};},
  syncKeys(){return typeof SYNC_KEYS!=='undefined'?SYNC_KEYS.slice():null;},
  recNames(){return {label:(typeof recLabel==='function')?recLabel('jopangi.canvasjari'):null,stat:(typeof recStat==='function')?recStat().filter(x=>x.k==='jopangi.canvasjari'):null};},
  async recRoundtrip(){const d=recDump();const before=localStorage.getItem('jopangi.canvasjari');
    localStorage.removeItem('jopangi.canvasjari');const mid=localStorage.getItem('jopangi.canvasjari');
    await new Promise(res=>{try{recImport(new File([JSON.stringify(d)],'rec.json',{type:'application/json'}),res);}catch(e){res();}});
    await wait(250);
    return {inDump:Object.prototype.hasOwnProperty.call(d.층||{},'jopangi.canvasjari'),before:before,mid:mid,after:localStorage.getItem('jopangi.canvasjari'),
      stat:recStat().filter(x=>x.k==='jopangi.canvasjari').map(x=>x.n),label:recLabel('jopangi.canvasjari')};},
  remoteSet(t,sha){window.__REMOTE={text:t,sha:sha,puts:0};return true;},
  remoteGet(){const R0=window.__REMOTE||{};return {text:R0.text,sha:R0.sha,puts:R0.puts};},
  async sync(force){for(let i=0;i<200&&recBusy;i++)await wait(25);await syncRecords(!!force);for(let i=0;i<400&&recBusy;i++)await wait(25);
    return {err:recLastErr,puts:(window.__REMOTE||{}).puts};},
  stamp(){return stampAll();},
  quiet(){try{clearTimeout(recTouchT);}catch(e){}return true;},
  errs(){return (window.__ERR||[]).slice();}
};
})();
