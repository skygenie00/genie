/* _harness_jo_2cha_unit_tests.js — _task_jo_2cha_unit 하네스가 페이지에 넣는 도구(__HU).
   BASE(d3dd927)·NEW 둘 다에 같은 것을 넣는다 — 없는 것(.c2uh·✎ 창 …)은 빈 값으로 돌려준다.
   재는 것 = DOM 실물(있는가·몇 개·글자·자리 getBoundingClientRect·계산 스타일) · 저장소 값(localStorage). */
(function(){
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const txt=e=>e?(e.textContent||'').replace(/\s+/g,' ').trim():'';
const R=e=>{if(!e)return null;const r=e.getBoundingClientRect();
  return {x:+r.left.toFixed(2),y:+r.top.toFixed(2),w:+r.width.toFixed(2),h:+r.height.toFixed(2),r:+r.right.toFixed(2),b:+r.bottom.toFixed(2),
          cx:+(r.left+r.width/2).toFixed(2),cy:+(r.top+r.height/2).toFixed(2)};};
const cs=(e,p)=>e?getComputedStyle(e)[p]:null;
const idle=async()=>{for(let i=0;i<200;i++){if(!busy)return true;await wait(25);}return false;};
function clean(){try{closeAllPops();}catch(e){}}
function hitOn(t){const r=R(t);if(!r)return null;const at=document.elementFromPoint(r.cx,r.cy);
  const onScreen=r.cy>0&&r.cy<innerHeight&&r.cx>0&&r.cx<innerWidth;
  return Object.assign(r,{on:!!at&&(at===t||t.contains(at))&&onScreen,at:at?(at.className||at.tagName):null,onScreen});}
async function scrollHit(t){if(!t)return null;t.scrollIntoView({block:'center',inline:'nearest'});await wait(250);return hitOn(t);}
const mainEl=()=>document.querySelector('#slot .main');
function listKids(){const w=document.querySelector('#slot .main .c2list');return w?[...w.children]:[];}
function rowInfo(r){const t1=r.querySelector('.c2t1');
  return {ck:r.dataset.ck||null,ckx:r.dataset.ckx||null,code:txt(r.querySelector('.c2code')),cls:r.className,
    t1kids:t1?[...t1.children].map(e=>e.className):[],first:t1&&t1.firstElementChild?t1.firstElementChild.className:null,
    title:txt(r.querySelector('.c2t2')),score:txt(r.querySelector('.chip.c-score')),
    chips:[...r.querySelectorAll('.c2r3 .c2uc')].map(c=>c.dataset.unit||''),chipTxt:[...r.querySelectorAll('.c2r3 .c2uc')].map(txt),
    chipCls:[...r.querySelectorAll('.c2r3 .c2uc')].map(c=>c.className),hand:!!r.querySelector('.c2r3 .c2uhand'),edit:!!r.querySelector('.c2r3 .c2ue'),
    k:r.querySelectorAll('.c2k').length,rn:r.querySelectorAll('.c2rn').length,ovt:txt(r.querySelector('.c2ovt')),alt:r.classList.contains('alt'),
    bg:cs(r,'backgroundColor')};}

window.__HU={
  wait,
  async board(law,kind,ord,o){clean();await idle();S.law=law;S.tab='cha2';S.boardKind=kind;S.series='';S.yearFilter='';S.cha2Sel=null;S.cha2Filter={};
    if(ord)S.c2ord=ord;Object.assign(S,o||{});await render();await idle();await wait(600);return true;},
  seg(){const s=document.getElementById('ordSeg');return s?[...s.querySelectorAll('button')].map(b=>({t:txt(b),o:b.dataset.o,on:b.classList.contains('on'),dis:b.disabled,title:b.title})):null;},
  /* 회차별 목록 — 회차 머리와 줄을 DOM 차례대로 */
  listRead(){const out={heads:[],rows:[],order:[]};let cur=null;
    listKids().forEach(e=>{
      if(e.classList.contains('c2rh')){cur={round:e.dataset.round,t:txt(e),r:txt(e.querySelector('.r')),y:txt(e.querySelector('.y')),n:txt(e.querySelector('.n')),
        fs:cs(e.querySelector('.r'),'fontSize'),ff:cs(e.querySelector('.r'),'fontFamily'),bb:cs(e,'borderBottomWidth'),mt:cs(e,'marginTop'),cnt:0};out.heads.push(cur);out.order.push('H');return;}
      if(e.classList.contains('c2row')){const ri=rowInfo(e);ri.round=cur?cur.round:null;if(cur)cur.cnt++;out.rows.push(ri);out.order.push('R');}});
    return out;},
  /* 단원별 보드 — 띠 · 머리 · 줄(주 줄 = data-ck · 걸침 줄 = data-ckx) · 단원 없음 */
  unitRead(){const out={bands:[],heads:[],rows:[],over:[],none:0,order:[]};let cur=null;
    listKids().forEach(e=>{
      if(e.classList.contains('c2band')){out.bands.push({no:e.dataset.pyeon,t:txt(e),bg:cs(e,'backgroundColor'),color:cs(e,'color')});out.order.push('B');return;}
      if(e.classList.contains('c2uh')){cur={unit:e.dataset.unit||'',none:e.classList.contains('c2unone'),no:txt(e.querySelector('.no')),nm:txt(e.querySelector('.nm')),
        n:txt(e.querySelector('.n')),ov:txt(e.querySelector('.ov')),rows:0,over:0,noFont:cs(e.querySelector('.no'),'fontFamily'),noColor:cs(e.querySelector('.no'),'color')};
        out.heads.push(cur);out.order.push(cur.none?'N':'U');return;}
      if(e.classList.contains('c2row')){const ri=rowInfo(e);ri.head=cur?cur.unit:null;ri.op=cs(e,'opacity');
        if(ri.ckx){out.over.push(ri);if(cur)cur.over++;}else{out.rows.push(ri);if(cur){cur.rows++;if(cur.none)out.none++;}}}});
    return out;},
  async headAt(unit,part){const h=[...document.querySelectorAll('#slot .c2uh')].find(e=>e.dataset.unit===unit);if(!h)return null;
    const t=part==='ov'?h.querySelector('.ov'):h.querySelector('.nm');return scrollHit(t);},
  async rowAt(ck,part,over,ns){const rows=[...document.querySelectorAll('#slot .main .c2row')].filter(r=>(over?r.dataset.ckx:r.dataset.ck)===ck);const r=rows[0];if(!r)return null;
    const t=part==='chip'?r.querySelector('.c2r3 .c2uc'):part==='edit'?r.querySelector('.c2r3 .c2ue'):part==='code'?r.querySelector('.c2code'):r.querySelector('.c2t2')||r.querySelector('.ctitle');
    return ns?hitOn(t):scrollHit(t);},
  async cellTitleAt(ck){const c=[...document.querySelectorAll('#slot .main .cell[data-ck]')].find(e=>e.dataset.ck===ck);if(!c)return null;
    return scrollHit(c.querySelector('.c2t2')||c.querySelector('.ctitle'));},
  async popRead(){for(let i=0;i<80;i++){if(document.querySelectorAll('.pop').length)break;await wait(50);}
    let last=null,same=0;for(let i=0;i<80;i++){const t=[...document.querySelectorAll('.pop')].map(x=>x.innerText).join('\n␞\n');
      if(t===last){if(++same>=4)break;}else{same=0;last=t;}await wait(100);}
    const ps=[...document.querySelectorAll('.pop')];
    return {n:ps.length,titles:ps.map(p=>txt(p.querySelector('.ph .pt'))),text:last,kinds:ps.map(p=>p.className),sel:S.cha2Sel};},
  closePops(){clean();return document.querySelectorAll('.pop').length;},
  /* ✎ 창 */
  win(){const p=document.querySelector('.pop.c2uw');if(!p)return null;
    return {code:p.dataset.c2uwin,title:txt(p.querySelector('.ph .pt')),sub:txt(p.querySelector('.c2w-sub')),st:txt(p.querySelector('.c2w-st')),
      main:(p.querySelector('.c2w-rad.on')||{dataset:{}}).dataset.n||'',rads:[...p.querySelectorAll('.c2w-rad')].map(b=>b.dataset.n),
      rows:[...p.querySelectorAll('.c2w-row')].map(r=>({no:r.dataset.no,u:[...r.querySelectorAll('.c2uc')].map(c=>c.dataset.n)})),
      pick:!!p.querySelector('.c2w-pick'),items:[...p.querySelectorAll('.c2w-it')].length,autoItems:[...p.querySelectorAll('.c2w-it.auto')].map(b=>b.dataset.n),
      pyeon:[...p.querySelectorAll('.c2w-py')].length,msg:txt(p.querySelector('.c2w-msg')),rect:R(p),head:hitOn(p.querySelector('.ph .pt')),
      pos:{l:parseFloat(p.style.left)||0,t:parseFloat(p.style.top)||0},revDis:!!(p.querySelector('.c2w-rev')||{}).disabled};},
  async winAt(kind,a,b){const p=document.querySelector('.pop.c2uw');if(!p)return null;let t=null;
    if(kind==='rad')t=[...p.querySelectorAll('.c2w-rad')].find(x=>x.dataset.n===a);
    else if(kind==='add')t=([...p.querySelectorAll('.c2w-row')].find(r=>r.dataset.no===a)||{querySelector:()=>null}).querySelector('.c2w-add');
    else if(kind==='x'){const r=[...p.querySelectorAll('.c2w-row')].find(r=>r.dataset.no===a);const c=r?[...r.querySelectorAll('.c2uc')].find(x=>x.dataset.n===b):null;t=c?c.querySelector('.x'):null;}
    else if(kind==='it')t=[...p.querySelectorAll('.c2w-it')].find(x=>x.dataset.n===a&&(b==null||x.classList.contains(b)));
    else if(kind==='itq')t=[...p.querySelectorAll('.c2w-it')].find(x=>x.textContent.indexOf(a)>=0);
    else if(kind==='save')t=p.querySelector('.c2w-save');else if(kind==='rev')t=p.querySelector('.c2w-rev');else if(kind==='cls')t=p.querySelector('.c2w-cls');
    else if(kind==='input')t=p.querySelector('.c2w-pick input');
    if(!t)return null;t.scrollIntoView({block:'nearest'});await wait(120);return hitOn(t);},
  pickItems(){const p=document.querySelector('.pop.c2uw');return p?[...p.querySelectorAll('.c2w-it')].map(b=>({n:b.dataset.n,auto:b.classList.contains('auto'),have:b.classList.contains('have'),pad:b.style.paddingLeft})):[];},
  /* 저장소 · 동기화 */
  hand(k){const o=JSON.parse(localStorage.getItem('jopangi.c2unit')||'{}');return k?(o[k]===undefined?null:o[k]):o;},
  ls(k){return localStorage.getItem(k);},
  syncKeys(){return {n:SYNC_KEYS.length,last:SYNC_KEYS[SYNC_KEYS.length-1],has:SYNC_KEYS.indexOf('jopangi.c2unit')>=0};},
  recNames(){return {label:(typeof recLabel==='function')?recLabel('jopangi.c2unit'):null,stat:(typeof recStat==='function')?recStat().filter(x=>x.k==='jopangi.c2unit'):null,
    dump:(typeof recDump==='function')?Object.keys(recDump().층||recDump()).filter(k=>k.indexOf('c2unit')>=0):null};},
  /* C-8 — ⤓ 기록 내보내기(recDump) → c2unit 층을 지우고 → 들여오기(recImport) → 되살아나나 · 건수에 드나 */
  async recRoundtrip(){const d=recDump();const before=localStorage.getItem('jopangi.c2unit');
    localStorage.removeItem('jopangi.c2unit');const mid=localStorage.getItem('jopangi.c2unit');
    await new Promise(res=>{try{recImport(new File([JSON.stringify(d)],'rec.json',{type:'application/json'}),res);}catch(e){res();}});
    await wait(200);
    return {inDump:Object.prototype.hasOwnProperty.call(d.층||{},'jopangi.c2unit'),count:d.건수,before:before,mid:mid,after:localStorage.getItem('jopangi.c2unit'),
      stat:recStat().filter(x=>x.k==='jopangi.c2unit').map(x=>x.n),label:recLabel('jopangi.c2unit')};},
  remoteSet(t,sha){window.__REMOTE={text:t,sha:sha,puts:0};return true;},
  remoteGet(){const R0=window.__REMOTE||{};return {text:R0.text,sha:R0.sha,puts:R0.puts};},
  async sync(force){await idle();for(let i=0;i<200&&recBusy;i++)await wait(25);await syncRecords(!!force);for(let i=0;i<400&&recBusy;i++)await wait(25);
    return {err:recLastErr,puts:(window.__REMOTE||{}).puts};},
  stamp(){return stampAll();},
  quiet(){try{clearTimeout(recTouchT);}catch(e){}return true;},
  /* 줄 안 요소가 줄 테두리 안인가 — 셋째 칸(단원 칩 · ✎)까지 */
  rowsFit(){const rows=[...document.querySelectorAll('#slot .c2row')].slice(0,40);const bad=[];
    rows.forEach(r=>{const rr=r.getBoundingClientRect();const lim=rr.right-parseFloat(cs(r,'paddingRight'))+0.5;
      r.querySelectorAll('.c2t1>*,.c2code,.c2r3>*').forEach(e=>{const er=e.getBoundingClientRect();
        if(er.right>lim)bad.push([(r.dataset.ck||r.dataset.ckx||'').slice(-18),e.className,Math.round(er.right-lim)]);});});
    return {n:rows.length,nbad:bad.length,bad:bad.slice(0,6),w:rows[0]?Math.round(rows[0].getBoundingClientRect().width):null};},
  errs(){return (window.__ERR||[]).slice();}
};
})();
