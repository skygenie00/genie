/* _harness_jo_cvfind_tests.js — _task_jo_ms_cvfind 하네스가 페이지에 넣는 도구(__HC).
   BASE(HEAD 905169d)·NEW 둘 다에 같은 것을 넣는다 — 없는 것(토글 · 정리 결과 팝업 …)은 빈 값으로 돌려준다(헛잣대).
   재는 것 = DOM 실물 · 화면 기준 보임(display ≠ none 그리고 높이 > 0) · getBoundingClientRect · elementFromPoint · 창(POPS) · 무대 값(vz·vx·vy).
   ⚠ 누름은 여기서 안 한다 — 자리만 돌려주고 파이썬이 page.mouse / touchscreen 으로 누른다(지시서 관문 규칙 1). */
(function(){
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const txt=e=>e?(e.textContent||'').replace(/\s+/g,' ').trim():'';
const R=e=>{if(!e)return null;const r=e.getBoundingClientRect();
  return {x:+r.left.toFixed(2),y:+r.top.toFixed(2),w:+r.width.toFixed(2),h:+r.height.toFixed(2),r:+r.right.toFixed(2),b:+r.bottom.toFixed(2),
          cx:+(r.left+r.width/2).toFixed(2),cy:+(r.top+r.height/2).toFixed(2)};};
const vis=e=>!!e&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0;   /* 화면 기준 보임(지시서 관문 규칙 2) */
const cs=(e,p)=>e?getComputedStyle(e)[p]:null;
function hitOn(t){const r=R(t);if(!r)return null;const at=document.elementFromPoint(r.cx,r.cy);
  const onScreen=r.cy>0&&r.cy<innerHeight&&r.cx>0&&r.cx<innerWidth;
  return Object.assign(r,{on:!!at&&(at===t||t.contains(at))&&onScreen,at:at?(String(at.className&&at.className.baseVal!=null?at.className.baseVal:at.className||at.tagName)).slice(0,60):null,onScreen});}
const pops=()=>(typeof POPS!=='undefined'?POPS:[]);
const popOf=pk=>pops().find(x=>x._pk===pk)||null;
const OK='jopangi.ncomr';
const lsj=k=>{try{return JSON.parse(localStorage.getItem(k)||'null');}catch(e){return null;}};
const mkpop=()=>document.querySelector('.pop.mkpop');
const rowOf=note=>{const p=mkpop();return p?[...p.querySelectorAll('.mklist .mkr')].find(x=>x.dataset.note===note)||null:null;};
const scrollerOf=el=>{for(let q=el&&el.parentElement;q;q=q.parentElement){const o=getComputedStyle(q).overflowY;if((o==='auto'||o==='scroll')&&q.scrollHeight>q.clientHeight)return q;}return null;};
const scaleOf=s=>{const m=/scale\(([-\d.e]+)\)/.exec(s||'');return m?+m[1]:null;};
const trOf=s=>{const m=/translate\(([-\d.e]+)px,\s*([-\d.e]+)px\)/.exec(s||'');return m?[+m[1],+m[2]]:null;};
window.__HC={
  wait,R,vis,hitOn,
  async boot(tab,law){try{closeAllPops();}catch(e){}try{closeSk();}catch(e){}S.law=law||'민사소송법';S.tab=tab||'jo';await render();await wait(500);return __HC.state();},
  state(){return {tab:S.tab,law:S.law,omrPage:S.omrPage==null?null:S.omrPage};},
  laws(){return LAWS.slice();},
  async ensure(){try{await viewCanvas.jari.ensure();}catch(e){return 'ERR '+e;}return true;},
  async noteNames(){const d=await noteData();return Object.keys(d.N||{});},
  hash(){try{return viewCanvas._cv().META.hash;}catch(e){return null;}},
  /* ── A 목차노트 목록 ── */
  /* 손값 넣기 — 각 노트 첫 쪽 자동 블록(noteOf) 위에서부터 3개를 합친 네모 ± 4pt(채팅 시안과 같은 값) */
  seedPins(notes){const C=viewCanvas._cv(),M=viewCanvas.jari.noteBids()||{},A=lsj(OK)||{},out={};
    notes.forEach(f=>{const bx=(M[f]||[]).map(k=>{const o=C.BK.get(k);return o?{n:o.p.n,r:[o.b.x,o.b.y-o.p.oy,o.b.x+o.b.w,o.b.y-o.p.oy+o.b.h]}:null;}).filter(Boolean);
      if(!bx.length)return;const n=Math.min(...bx.map(x=>x.n)),on=bx.filter(x=>x.n===n).sort((a,b)=>a.r[1]-b.r[1]).slice(0,3);
      const r=[Math.min(...on.map(x=>x.r[0]))-4,Math.min(...on.map(x=>x.r[1]))-4,Math.max(...on.map(x=>x.r[2]))+4,Math.max(...on.map(x=>x.r[3]))+4].map(v=>Math.round(v*10)/10);
      A['note|'+f]={p:n,r,h:C.META.hash,t:Date.now(),who:'하네스'};out[f]={p:n,r};});
    localStorage.setItem(OK,JSON.stringify(A));return out;},
  ls(){return lsj(OK);},
  async mokOpen(){try{closeAllPops();}catch(e){}const b=document.getElementById('mokBtn');if(!b)return {err:'no mokBtn'};
    try{b.scrollIntoView({block:'nearest'});}catch(e){}const r=R(b);
    await popMokNote(b,{clientX:r.cx,clientY:r.cy});
    for(let i=0;i<300;i++){const p=mkpop();if(p&&p.querySelectorAll('.mklist .mkr').length)break;await wait(50);}
    await wait(300);return __HC.list();},
  /* 압정 칠하기가 끝날 때까지(title 이 「…개 자리」·「…블록이 없다」) — 압정이 없는 법·판은 곧바로 */
  async listPainted(ms){const t0=Date.now();while(Date.now()-t0<(ms||90000)){const p=mkpop();if(!p)return null;const ps=[...p.querySelectorAll('.mkomr:not(.mkgap)')];
      if(!ps.length||ps.every(b=>/개 자리|블록이 없다/.test(b.title||'')))return __HC.list();await wait(100);}return __HC.list();},
  list(){const p=mkpop();if(!p)return null;
    const rows=[...p.querySelectorAll('.mklist .mkr')].map(r=>{const t=r.querySelector(':scope > .mktg');
      return {note:r.dataset.note,tg:!!t,tgVis:vis(t),tgHidden:t?t.hidden:null,open:t?t.classList.contains('mkopen'):null,aria:t?t.getAttribute('aria-expanded'):null,
        tr:R(t),rr:R(r),nr:R(r.querySelector(':scope > .nm')),pl:r.style.paddingLeft,cw:!!(r.nextElementSibling&&r.nextElementSibling.classList.contains('mkcw'))};});
    return {n:rows.length,rows,all:p.querySelectorAll('.mktg').length,mkcw:p.querySelectorAll('.mkcw').length,title:txt(p.querySelector('.ph .pt'))};},
  listHtml(){const p=mkpop();const L=p&&p.querySelector('.mklist');return L?L.outerHTML:null;},
  tgAt(note){const r=rowOf(note);const t=r&&r.querySelector(':scope > .mktg');if(!t)return null;try{t.scrollIntoView({block:'center'});}catch(e){}return hitOn(t);},
  pinAt(note){const r=rowOf(note);const b=r&&r.querySelector(':scope > .mkomr:not(.mkgap)');if(!b)return null;try{b.scrollIntoView({block:'center'});}catch(e){}return hitOn(b);},
  /* 펼친 그림 — 보기 칸 · 주황 테 · 발 줄 · 배율(transform) · 쪽이 지어졌는가 */
  clip(note){const r=rowOf(note);const w=r&&r.nextElementSibling;if(!w||!w.classList.contains('mkcw'))return null;
    const v=w.querySelector('.mkcv'),bx=w.querySelector('.mkbx'),host=w.querySelector('.oppg'),inn=w.querySelector('.mkin');
    return {v:R(v),bx:R(bx),vis:vis(v),foot:txt(w.querySelector('.mkcf')),old:!!w.querySelector('.mkold'),s:host?scaleOf(host.style.transform):null,t:inn?trOf(inn.style.transform):null,
      pg:w.querySelectorAll('.oppg .cv-pg').length,ln:w.querySelectorAll('.oppg .cv-ln').length,z:v?v.classList.contains('mkz'):null,
      ol:[cs(bx,'outlineStyle'),cs(bx,'outlineWidth'),cs(bx,'outlineColor')],pl:w.style.paddingLeft,rowPl:r.style.paddingLeft,ta:cs(v,'touchAction')};},
  async clipWait(note,ms){const t0=Date.now();while(Date.now()-t0<(ms||60000)){const c=__HC.clip(note);if(c&&c.pg&&c.v&&c.v.h>0){await wait(150);return __HC.clip(note);}await wait(80);}return __HC.clip(note);},
  clipPt(note,fx,fy){const r=rowOf(note);const w=r&&r.nextElementSibling;const v=w&&w.querySelector('.mkcv');if(!v)return null;try{v.scrollIntoView({block:'center'});}catch(e){}
    const b=v.getBoundingClientRect(),x=Math.round(b.left+b.width*fx),y=Math.round(b.top+b.height*fy),at=document.elementFromPoint(x,y);return {x,y,on:!!at&&(at===v||v.contains(at))};},
  clipScroller(note){const r=rowOf(note);const w=r&&r.nextElementSibling;const q=scrollerOf(w&&w.querySelector('.mkcv'));return q?{cls:String(q.className).slice(0,40),st:q.scrollTop,sh:q.scrollHeight,ch:q.clientHeight}:null;},
  /* ── 정리OMR 팝업(있는 것 그대로 — A-4 한 번 누름 · A-5 되돌리기·영역 지정) ── */
  omrKeys(){return pops().filter(x=>(x._pk||'').indexOf('cv|omr|')===0).map(x=>x._pk);},
  omrTitle(k){const w=popOf('cv|omr|'+k);return w?txt(w.querySelector('.ph .pt')):null;},
  omrAt(k,what){const w=popOf('cv|omr|'+k);if(!w)return null;const sel={pick:'[data-pick]',ok:'[data-ok]',rv:'[data-revert]',v:'.opv'}[what]||what;const t=w.querySelector(sel);return t?hitOn(t):null;},
  vpt(k,fx,fy){const w=popOf('cv|omr|'+k);const v=w&&w.querySelector('.opv');if(!v)return null;const r=v.getBoundingClientRect();return {x:Math.round(r.left+r.width*fx),y:Math.round(r.top+r.height*fy)};},
  omrClose(){pops().filter(x=>(x._pk||'').indexOf('cv|omr|')===0).forEach(w=>closeOne(w));return true;},
  frontList(){const w=mkpop();if(w){w.style.zIndex=++POPZ;popAllSync();}return !!w;},
  /* ── B·D 전체 검색 ── */
  skSet(scopes,laws){Object.keys(SKON).forEach(k=>{SKON[k]=scopes.indexOf(k)>=0;});skonSave();try{skPaint();}catch(e){}
    Object.keys(SKLAW).forEach(k=>{delete SKLAW[k];});laws.forEach(l=>{SKLAW[l]=true;});try{skLawPaint();}catch(e){}return {SKON:Object.assign({},SKON),SKLAW:Object.assign({},SKLAW)};},
  sk(){const s=document.getElementById('sk');return {disp:cs(s,'display'),z:cs(s,'zIndex'),q:(document.getElementById('skin')||{}).value};},
  skDone(){const b=document.getElementById('skres');return !!b&&[...b.querySelectorAll(':scope > .grp')].some(g=>/↵ 열기/.test(txt(g)));},
  skGroups(){const box=document.getElementById('skres');const out=[];let cur=null;
    [...box.children].forEach(c=>{if(c.classList.contains('grp')){cur={h:txt(c),rows:[]};out.push(cur);}
      else if(c.classList.contains('res')&&cur)cur.rows.push({head:txt(c.querySelector(':scope > b')),tag:txt(c.querySelector(':scope > .lawtag')),tail:txt(c.querySelector(':scope > .x')),
        ctx:txt(c.querySelector('.skctx')),ctxB:txt(c.querySelector('.skctx b')),icon:txt(c.querySelector('.skic')),hasctx:c.classList.contains('hasctx')});});
    return out;},
  skRowAt(prefix,i){const box=document.getElementById('skres');let on=false,k=-1,t=null;
    for(const c of box.children){if(c.classList.contains('grp')){on=txt(c).indexOf(prefix)===0;continue;}if(on&&c.classList.contains('res')){k++;if(k===i){t=c;break;}}}
    if(!t)return null;try{t.scrollIntoView({block:'nearest'});}catch(e){}return hitOn(t);},
  skTop(){const i=document.getElementById('skin');const r=R(i);if(!r)return null;const at=document.elementFromPoint(r.cx,r.cy);
    return {at:at?String(at.id||at.className).slice(0,40):null,onSk:!!at&&!!at.closest('#sk'),z:cs(document.getElementById('sk'),'zIndex'),popz:typeof POPZ!=='undefined'?POPZ:null};},
  async find(q){try{const H=await viewCanvas.find(q);return H?H.map(h=>({n:h.n,i:h.i,at:h.at,b:h.b,memo:h.memo,head:h.head})):null;}catch(e){return 'ERR '+e;}},
  /* ── C 정리 탭 ── */
  async canvasBoot(){try{closeAllPops();}catch(e){}try{closeSk();}catch(e){}S.law='민사소송법';S.tab='omr';await render();
    for(let i=0;i<600;i++){if(document.getElementById('cvStage')&&document.querySelectorAll('#cvWorld .cv-blk').length)break;await wait(50);}await wait(500);return __HC.cv();},
  cv(){try{const C=viewCanvas._cv();return {vz:+C.vz.toFixed(4),vx:+C.vx.toFixed(2),vy:+C.vy.toFixed(2)};}catch(e){return null;}},
  cvSet(v){viewCanvas._cv().set(v);return __HC.cv();},
  cvQ(){const q=document.getElementById('cvQ'),n=document.getElementById('cvQn');return {q:q?q.value:null,n:txt(n)};},
  hitsInfo(){const H=document.getElementById('cvHits');if(!H)return null;return {rect:R(H),st:H.scrollTop,sh:H.scrollHeight,ch:H.clientHeight,n:H.querySelectorAll('.cv-hit').length,
    cur:[...H.querySelectorAll('.cv-hit.cur')].map(d=>+d.dataset.k)};},
  thAt(i){const t=document.querySelectorAll('#cvHits .cv-th')[i];if(!t)return null;try{t.scrollIntoView({block:'nearest'});}catch(e){}const g=t.closest('.cv-hitgrp');const d=g&&g.querySelector('.cv-hit');
    return Object.assign(hitOn(t)||{},{k0:d?+d.dataset.k:null});},
  hitRowAt(k){const d=document.querySelector('#cvHits .cv-hit[data-k="'+k+'"]');if(!d)return null;try{d.scrollIntoView({block:'nearest'});}catch(e){}return hitOn(d);},
  markCur(){const m=document.querySelector('#cvWorld .cv-mark.cur');if(!m)return null;const r=R(m);const at=document.elementFromPoint(r.cx,r.cy);const H=document.getElementById('cvHits');
    return Object.assign(r,{top:at?String(at.id||at.className).slice(0,40):null,underList:!!at&&!!H&&H.contains(at)});},
  stage(){const s=document.getElementById('cvStage');return s?R(s):null;},
  /* ── D 정리 결과 팝업 ── */
  sf(){const ws=pops().filter(x=>x._pk==='sfind');const w=ws[0];if(!w)return {n:0};const q=s=>w.querySelector(s);const v=q('.opv');const o=w._sf||{};
    return {n:ws.length,title:txt(q('.ph .pt')),sfn:txt(q('.sfn')),where:txt(q('.sfwhere')),msg:txt(q('.opmsg')),go:txt(q('[data-go]')),
      prevDis:!!(q('[data-hn="-1"]')||{}).disabled,nextDis:!!(q('[data-hn="1"]')||{}).disabled,pin:w.querySelectorAll('.opbx.oppin').length,auto:w.querySelectorAll('.opbx.opauto').length,
      pinR:R(q('.opbx.oppin')),vr:R(v),rect:R(w),s:o.s,sl:v?v.scrollLeft:null,st:v?v.scrollTop:null,law:o.law,k:o.k,nh:(o.hits||[]).length,imgs:w.querySelectorAll('.sfpg img').length,
      imgOk:[...w.querySelectorAll('.sfpg img')].filter(i=>i.complete&&i.naturalWidth>0).length,imgSz:[...w.querySelectorAll('.sfpg img')].slice(-1).map(i=>[i.naturalWidth,i.getBoundingClientRect().width/(o.s||1)]),
      cvpg:w.querySelectorAll('.sfpg .cv-pg').length,ln:w.querySelectorAll('.sfpg .cv-ln').length,z:+w.style.zIndex,
      zoomUi:w.querySelectorAll('.opbar input,.opbar .zv,[data-zoom],[data-fit],[data-zin],[data-zout]').length,pinOl:cs(q('.opbx.oppin'),'outlineColor'),autoOl:cs(q('.opbx.opauto'),'outlineColor')};},
  sfAt(what){const w=popOf('sfind');const sel={prev:'[data-hn="-1"]',next:'[data-hn="1"]',go:'[data-go]',v:'.opv'}[what];const t=w&&w.querySelector(sel);return t?hitOn(t):null;},
  sfClose(){const w=popOf('sfind');if(w)closeOne(w);return true;},
  errs(){return (window.__ERR||[]).slice(0,20);},
};
})();
