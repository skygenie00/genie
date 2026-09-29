/* _harness_jo_ms_omrpop_tests.js — _task_jo_ms_omrpop 하네스가 페이지에 넣는 도구(__HO).
   BASE(bd8cfdf)·NEW 둘 다에 같은 것을 넣는다 — 없는 것(압정 · 정리OMR 팝업 · 손값 키 …)은 빈 값으로 돌려준다(헛잣대).
   재는 것 = DOM 실물(있는가 · 몇 개 · 글자 · getBoundingClientRect · 계산 스타일) · elementFromPoint · 저장소 값(localStorage) · 창(POPS). */
(function(){
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const txt=e=>e?(e.textContent||'').replace(/\s+/g,' ').trim():'';
const R=e=>{if(!e)return null;const r=e.getBoundingClientRect();
  return {x:+r.left.toFixed(2),y:+r.top.toFixed(2),w:+r.width.toFixed(2),h:+r.height.toFixed(2),r:+r.right.toFixed(2),b:+r.bottom.toFixed(2),
          cx:+(r.left+r.width/2).toFixed(2),cy:+(r.top+r.height/2).toFixed(2)};};
const cs=(e,p)=>e?getComputedStyle(e)[p]:null;
function hitOn(t){const r=R(t);if(!r)return null;const at=document.elementFromPoint(r.cx,r.cy);
  const onScreen=r.cy>0&&r.cy<innerHeight&&r.cx>0&&r.cx<innerWidth;
  return Object.assign(r,{on:!!at&&(at===t||t.contains(at))&&onScreen,at:at?(String(at.className&&at.className.baseVal!=null?at.className.baseVal:at.className||at.tagName)).slice(0,60):null,onScreen});}
const pops=()=>(typeof POPS!=='undefined'?POPS:[]);
const popOf=pk=>pops().find(x=>x._pk===pk)||null;
const OK='jopangi.ncomr';
const lsj=k=>{try{return JSON.parse(localStorage.getItem(k)||'null');}catch(e){return null;}};
const mkpop=()=>document.querySelector('.pop.mkpop');
const omrW=k=>popOf('cv|omr|'+k);
window.__HO={
  wait,R,hitOn,
  async boot(tab,law){try{closeAllPops();}catch(e){}S.law=law||'민사소송법';S.tab=tab||'jo';await render();await wait(500);
    return {tab:S.tab,law:S.law,mok:!!document.getElementById('mokBtn')};},
  /* ── A 목차노트 목록 ── */
  async mokOpen(){try{closeAllPops();}catch(e){}const b=document.getElementById('mokBtn');if(!b)return {err:'no mokBtn'};
    try{b.scrollIntoView({block:'nearest'});}catch(e){}const r=R(b);
    await popMokNote(b,{clientX:r.cx,clientY:r.cy});
    for(let i=0;i<300;i++){const p=mkpop();if(p&&p.querySelectorAll('.mklist .mkr').length)break;await wait(50);}
    await wait(300);return __HO.list();},
  /* 압정 칠하기가 끝날 때까지(블록 수를 센 뒤 title 이 「…개 자리」·「…블록이 없다」) — 압정이 없는 판(바탕)은 곧바로 */
  async listPainted(ms){const t0=Date.now();while(Date.now()-t0<(ms||90000)){const L=__HO.list();if(!L)return L;const ps=L.rows.filter(r=>r.pin==='pin');
      if(!ps.length||ps.every(r=>/개 자리|블록이 없다/.test(r.title||'')))return L;await wait(100);}return __HO.list();},
  list(){const p=mkpop();if(!p)return null;
    const rows=[...p.querySelectorAll('.mklist .mkr')].map(r=>{const pin=r.querySelector(':scope > .mkomr');const nm=r.querySelector(':scope > .nm');const path=pin&&pin.querySelector('path');const sv=pin&&pin.querySelector('svg');
      return {note:r.dataset.note,pin:pin?(pin.classList.contains('mkgap')?'gap':'pin'):null,cls:pin?pin.className:null,pr:R(pin),nr:R(nm),rr:R(r),pl:cs(r,'paddingLeft'),
        color:cs(pin,'color'),fill:path?cs(path,'fill'):null,stroke:path?cs(path,'stroke'):null,vis:cs(pin,'visibility'),svgW:sv?R(sv).w:null,svgH:sv?R(sv).h:null,
        title:pin?pin.title:null,first:!!pin&&r.firstElementChild===pin,role:pin?pin.getAttribute('role'):null};});
    return {n:rows.length,rows,title:txt(p.querySelector('.ph .pt'))};},
  pinAt(note){const p=mkpop();if(!p)return null;const r=[...p.querySelectorAll('.mklist .mkr')].find(x=>x.dataset.note===note);const b=r&&r.querySelector(':scope > .mkomr:not(.mkgap)');
    if(!b)return null;try{b.scrollIntoView({block:'center'});}catch(e){}return hitOn(b);},
  pinColor(note){const p=mkpop();const r=p&&[...p.querySelectorAll('.mklist .mkr')].find(x=>x.dataset.note===note);const b=r&&r.querySelector(':scope > .mkomr');return b?cs(b,'color'):null;},
  /* ── B 정리OMR 팝업 ── */
  omrKeys(){return pops().filter(x=>(x._pk||'').indexOf('cv|omr|')===0).map(x=>x._pk);},
  pk(){return pops().map(x=>x._pk);},
  omr(k){const w=omrW(k);if(!w)return null;const st=w._omr||{};const q=s=>w.querySelector(s);const v=q('.opv'),inn=q('.opin');
    return {title:txt(q('.ph .pt')),p:st.p,s:st.s,pick:!!st.pick,box:st.box?JSON.parse(JSON.stringify(st.box)):null,bids:st.ctx?st.ctx.bids.slice():null,
      boxesK:(st.boxes||[]).map(o=>o.k),auto:w.querySelectorAll('.opbx.opauto').length,pin:w.querySelectorAll('.opbx.oppin').length,tmp:w.querySelectorAll('.opbx.optmp').length,
      pgs:[...w.querySelectorAll('.oppgs [data-pg]')].map(b=>txt(b)+(b.classList.contains('opon')?'*':'')),nav:w.querySelectorAll('.oppgs [data-nav]').length,
      msg:txt(q('.opmsg')),ok:!!q('[data-ok]')&&!q('[data-ok]').hidden,cancel:!!q('[data-cancel]')&&!q('[data-cancel]').hidden,rv:!!q('[data-revert]')&&!q('[data-revert]').hidden,
      pickOn:!!q('[data-pick].opon'),pickTxt:txt(q('[data-pick]')),zoomUi:w.querySelectorAll('.opbar input,.opbar .zv,[data-zoom],[data-fit],[data-zin],[data-zout]').length,
      barBtns:[...w.querySelectorAll('.opbar button')].map(txt),ftBtns:[...w.querySelectorAll('.opft button')].filter(b=>!b.hidden).map(txt),
      sl:v?v.scrollLeft:null,stp:v?v.scrollTop:null,vr:R(v),inner:R(inn),rect:R(w),z:+w.style.zIndex,topZ:typeof POPZ!=='undefined'?POPZ:null,
      autoR:[...w.querySelectorAll('.opbx.opauto')].map(R),pinR:R(q('.opbx.oppin')),tmpR:R(q('.opbx.optmp')),
      cvpg:w.querySelectorAll('.oppg .cv-pg').length,ln:w.querySelectorAll('.oppg .cv-ln').length,blk:w.querySelectorAll('.oppg .cv-blk').length,ink:w.querySelectorAll('.oppg .cv-inksvg path[data-i]').length,
      pe:cs(q('.oppg'),'pointerEvents'),pgTop:q('.oppg .cv-pg')?q('.oppg .cv-pg').style.top:null,kind:w.className,head:txt(q('.ph')),
      autoBg:cs(q('.opbx.opauto'),'backgroundColor'),autoOl:cs(q('.opbx.opauto'),'outlineColor'),pinBg:cs(q('.opbx.oppin'),'backgroundColor'),pinOl:cs(q('.opbx.oppin'),'outlineColor'),
      tmpOl:cs(q('.opbx.optmp'),'outlineStyle'),ta:cs(v,'touchAction')};},
  omrAt(k,what){const w=omrW(k);if(!w)return null;
    const sel={pick:'[data-pick]',ok:'[data-ok]',cancel:'[data-cancel]',rv:'[data-revert]',x:'.ph > button:not(.pall)',v:'.opv',next:'[data-nav="1"]',prev:'[data-nav="-1"]',head:'.ph .pt'}[what]||(what.indexOf('pg')===0?'[data-pg="'+what.slice(2)+'"]':what);
    const t=w.querySelector(sel);if(!t)return null;return hitOn(t);},
  /* 보기 칸 안 한 점(보기 칸 기준 비율) → 화면 좌표 · 그 점 밑 쪽 좌표(pt) · 그 점 맨 위 요소 */
  vpt(k,fx,fy){const w=omrW(k);const v=w&&w.querySelector('.opv');if(!v)return null;const r=v.getBoundingClientRect();const x=Math.round(r.left+r.width*fx),y=Math.round(r.top+r.height*fy);
    const ir=w.querySelector('.opin').getBoundingClientRect(),st=w._omr||{s:1};const at=document.elementFromPoint(x,y);
    return {x,y,px:(x-ir.left)/(st.s*4),py:(y-ir.top)/(st.s*4),at:at?String(at.className||at.tagName).slice(0,40):null};},
  /* 쪽 좌표(pt) → 지금 화면 좌표 */
  scr(k,px,py){const w=omrW(k);if(!w)return null;const ir=w.querySelector('.opin').getBoundingClientRect(),st=w._omr||{s:1};return {x:ir.left+px*st.s*4,y:ir.top+py*st.s*4};},
  /* 쪽 안에서 겹(.opov) 맨 위인 점 — 가운데 둘레에서 찾는다(자동 상자 · 머리 · 발 줄이 가리지 않는 곳) */
  emptyAt(k){const w=omrW(k);const v=w&&w.querySelector('.opv');if(!v)return null;const r=v.getBoundingClientRect();
    for(const [fx,fy] of [[.5,.5],[.4,.45],[.6,.55],[.3,.6],[.7,.4],[.5,.3],[.5,.7]]){const x=Math.round(r.left+r.width*fx),y=Math.round(r.top+r.height*fy);const t=document.elementFromPoint(x,y);
      if(t&&t.classList&&t.classList.contains('opov'))return {x,y};}return null;},
  /* 자동 상자 한가운데 맨 위 요소(쪽 그림은 누름을 안 받는다 — 겹이나 보기 칸이 받아야) */
  autoTop(k){const w=omrW(k);const b=w&&w.querySelector('.opbx.opauto');if(!b)return null;const r=R(b);const t=document.elementFromPoint(r.cx,r.cy);return t?String(t.className||t.tagName).slice(0,40):null;},
  omrPgCount(){return document.querySelectorAll('.pop .oppg .cv-pg').length;},
  /* ── 정리 탭(무대) ── */
  async canvasBoot(){try{closeAllPops();}catch(e){}S.law='민사소송법';S.tab='omr';await render();
    for(let i=0;i<600;i++){if(document.getElementById('cvStage')&&document.querySelectorAll('#cvWorld .cv-blk').length)break;await wait(50);}await wait(500);return __HO.stage();},
  stage(){const w=document.getElementById('cvWorld');return {tab:S.tab,stage:!!document.getElementById('cvStage'),tr:w?w.style.transform:null,
    worldPg:document.querySelectorAll('#cvWorld .cv-pg').length};},
  /* ── 저장소 ── */
  ls(){return lsj(OK);},
  lsSet(v){localStorage.setItem(OK,JSON.stringify(v));},
  u(){const u=lsj('jopangi_sync_u')||{};return Object.keys(u).filter(k=>k.indexOf(OK+'|')===0).reduce((o,k)=>(o[k]=u[k],o),{});},
  syncKeys(){try{return SYNC_KEYS.slice();}catch(e){return null;}},
  recName(){try{return REC_NAMES.ncomr||null;}catch(e){return null;}},
  jari(){try{return Object.keys(viewCanvas.jari);}catch(e){return null;}},
  noteBids(n){try{const m=viewCanvas.jari.noteBids&&viewCanvas.jari.noteBids();return m?(m[n]||[]):null;}catch(e){return 'ERR '+e;}},
  async ensure(){try{await viewCanvas.jari.ensure();}catch(e){return 'ERR '+e;}return true;},
  /* 블록 자리(쪽 기준 pt) — D(편집 재생본)에서 */
  blk(bid){try{const C=viewCanvas._cv();for(const p of C.D.pages){const b=p.blocks.find(x=>x.bid===bid&&!x.del);if(b)return {n:p.n,r:[b.x,b.y-p.oy,b.x+b.w,b.y-p.oy+b.h]};}}catch(e){return 'ERR '+e;}return null;},
  /* 노트 블록을 noteOf(bn → 블록 파일 note) 로 따로 센다 — 앱 함수와 맞대기 */
  noteCount(){try{const C=viewCanvas._cv();const bn=(C.MATCH&&C.MATCH.bn)||{};const m={},mb={};C.D.pages.forEach(p=>p.blocks.forEach(b=>{if(b.del||b.k==='헤딩')return;
      const nm=Object.prototype.hasOwnProperty.call(bn,b.bid)?bn[b.bid]:b.note;if(nm)(m[nm]=m[nm]||[]).push(b.bid);if(Object.prototype.hasOwnProperty.call(bn,b.bid)&&bn[b.bid])(mb[bn[b.bid]]=mb[bn[b.bid]]||[]).push(b.bid);}));
    return {m,mb};}catch(e){return 'ERR '+e;}},
  meta(){try{return viewCanvas._cv().META.hash;}catch(e){return null;}},
  /* ── C 목차노트 📘 · 「교재 자리」 창 ── */
  async note(file){try{closeAllPops();}catch(e){}await popNote(file,null,{clientX:130,clientY:120},1);
    for(let i=0;i<300;i++){const w=popOf('note|'+PLAW()+'|'+file+'|');if(w&&w.querySelector('.ntbox'))break;await wait(50);}await wait(250);return !!popOf('note|'+PLAW()+'|'+file+'|');},
  ncbPk(file,end){return 'ncbook|'+PLAW()+'|'+file+'|'+end;},
  async ncbOpen(file,end){try{await ncBookOpen(file,end,{clientX:200,clientY:160},2);}catch(e){return String(e);}return true;},
  ncb(file,end){const w=popOf(__HO.ncbPk(file,end));if(!w)return null;const h=w.querySelector('.mbblist');if(!h)return {open:true,noHost:true};
    return {open:true,title:txt(w.querySelector('.ph .pt')),loading:/받는 중/.test(txt(h)),
      sec:[...h.querySelectorAll('.ncb-sec')].map(txt),
      pair:[...h.querySelectorAll(':scope > .mbbrow[data-bid]')].map(r=>({bid:r.dataset.bid,t:txt(r),hidden:r.hidden,disp:cs(r,'display')})),
      ncpin:[...h.querySelectorAll(':scope > .mbbrow.ncpin')].map(r=>({k:txt(r.querySelector('.hd .k')),p:txt(r.querySelector('.hd .p')),m:txt(r.querySelector('.hd .m')),sn:txt(r.querySelector('.sn')),mColor:cs(r.querySelector('.hd .m'),'color')})),
      more:[...h.querySelectorAll(':scope > .ncb-more')].map(txt),rect:R(w)};},
  async ncbWait(file,end,ms){const t0=Date.now();while(Date.now()-t0<(ms||60000)){const x=__HO.ncb(file,end);if(x&&x.sec&&!x.loading&&x.sec.length){await wait(400);return __HO.ncb(file,end);}await wait(60);}return __HO.ncb(file,end);},
  ncbAt(file,end,what,i){const w=popOf(__HO.ncbPk(file,end));const h=w&&w.querySelector('.mbblist');if(!h)return null;let t=null;
    if(what==='bid')t=h.querySelector(':scope > .mbbrow[data-bid="'+i+'"]');else if(what==='ncpin')t=h.querySelector(':scope > .mbbrow.ncpin');
    else if(what==='rv')t=[...h.querySelectorAll(':scope > .ncb-more')].find(b=>/자동으로 되돌리기/.test(txt(b))&&b.classList.contains('ncrv'))||null;
    if(!t)return null;try{t.scrollIntoView({block:'nearest'});}catch(e){}return hitOn(t);},
  /* ── 필기 픽스처(정리캔버스 필기 — D 를 짓기 전에 넣어야 쪽 그림에 보인다) ── */
  inkSeed(n){const A=lsj('jopangi.canvasink')||{};const o=A['민소']||{};o['p'+n]=[{c:'#E0301E',w:1.4,p:[[120,120,1],[320,180,1],[520,140,1]]}];A['민소']=o;localStorage.setItem('jopangi.canvasink',JSON.stringify(A));return true;},
  errs(){return (window.__ERR||[]).slice(0,20);},
};
})();
