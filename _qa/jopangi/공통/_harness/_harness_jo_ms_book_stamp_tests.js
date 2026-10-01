/* _harness_jo_ms_book_stamp_tests.js — _task_jo_ms_book_stamp 하네스가 페이지에 넣는 도구(__HB).
   BASE(6b03bf1)·NEW 둘 다에 같은 것을 넣는다 — 없는 것(도장 상자 · 📘 · 「교재 자리」 창 …)은 빈 값으로 돌려준다.
   재는 것 = DOM 실물(있는가 · 몇 개 · 글자 · 자리 · 계산 스타일) · elementFromPoint(누를 수 있는가) · 창(POPS) · 저장소 값 · 교재 요청 길(minbeoppdf). */
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
/* 교재(비공개 저장소) 요청 길 — SEED 가 /__book/ 으로 돌리기 전 주소를 적는다(pdf.js 의 fetch 도 여기로 온다) */
const REQ=[];{const f0=window.fetch;window.fetch=function(u,o){const s=String((u&&u.url)||u);const k=s.indexOf('minbeoppdf/contents/');
  if(k>=0)REQ.push(decodeURIComponent(s.slice(k+'minbeoppdf/contents/'.length).split('?')[0]));return f0.apply(this,arguments);};}
function idb(){return new Promise((res,rej)=>{const rq=indexedDB.open('ox_master_db',1);rq.onupgradeneeded=()=>{const db=rq.result;if(!db.objectStoreNames.contains('rows'))db.createObjectStore('rows');};rq.onsuccess=()=>res(rq.result);rq.onerror=()=>rej(rq.error);});}
async function idbPut(k,v){const db=await idb();return new Promise(res=>{const tx=db.transaction('rows','readwrite');tx.objectStore('rows').put(v,k);tx.oncomplete=()=>{db.close();res(true);};tx.onerror=()=>{db.close();res(false);};});}
async function idbGet(k){const db=await idb();return new Promise(res=>{const rq=db.transaction('rows','readonly').objectStore('rows').get(k);rq.onsuccess=()=>{db.close();res(rq.result);};rq.onerror=()=>{db.close();res(null);};});}
function bookInfo(w){if(!w)return null;const nav=w.querySelector('.cv-booknav'),pg=w.querySelector('.cv-bookpg'),cv=pg&&pg.querySelector('canvas'),band=w.querySelector('.cv-srcband');
  const inp=nav&&nav.querySelector('#cvBookP');const pdf=(txt(nav).match(/PDF (\d+)/)||[])[1]||null;
  return {pk:w._pk,title:txt(w.querySelector('.ph .pt')),nav:txt(nav),page:inp?inp.value:pdf,big:txt(nav&&nav.querySelector('span b')),cvsW:cv?cv.width:0,cvsH:cv?cv.height:0,
    loading:/받는 중/.test(txt(w)),err:/받지 못했다/.test(txt(w))?txt(w).slice(0,200):null,
    stamps:[...w.querySelectorAll('.cv-stamp')].map(d=>{const g=d.querySelector('.tg');return {st:d.dataset.st,i:+d.dataset.i,tag:txt(g),l:+parseFloat(d.style.left).toFixed(3),t:+parseFloat(d.style.top).toFixed(3),
      w:+parseFloat(d.style.width).toFixed(3),h:+parseFloat(d.style.height).toFixed(3),bw:cs(d,'borderTopWidth'),bc:cs(d,'borderTopColor'),bg:cs(d,'backgroundColor'),z:cs(d,'zIndex'),
      tg:g?{c:cs(g,'color'),bg:cs(g,'backgroundColor'),fs:cs(g,'fontSize'),fw:cs(g,'fontWeight')}:null,title:d.title};}),
    band:band?{l:parseFloat(band.style.left),t:parseFloat(band.style.top),w:parseFloat(band.style.width),h:parseFloat(band.style.height)}:null,
    hl:!!w.querySelector('.cv-bookhl'),okBtn:txt(nav&&nav.querySelector('[data-ok]')),pkBtn:!!(nav&&nav.querySelector('[data-pk]')),rect:R(w),z:+w.style.zIndex||0};}
window.__HB={
  wait,
  req(){return REQ.slice();},reqClear(){REQ.length=0;return true;},
  async law(l,tab){try{closeAllPops();}catch(e){}S.law=l;S.tab=tab||'jo';await render();await wait(500);return {law:S.law,tab:S.tab};},
  pops(){return pops().map(x=>x._pk);},
  closeAll(){try{closeAllPops();}catch(e){}return true;},
  close(pk){const w=popOf(pk);if(!w)return false;try{closeOne(w);}catch(e){return false;}return true;},
  /* ── A·B 교재 창(도장 층 · 출처 팝업 · 후보 목록) ── */
  bookPks(){return pops().filter(x=>/^cv\|(book|src|cand)\|/.test(x._pk||'')).map(x=>x._pk);},
  book(pk){return bookInfo(popOf(pk));},
  async bookWait(pk,n,ms){const t0=Date.now();while(Date.now()-t0<(ms||60000)){const b=bookInfo(popOf(pk));if(b&&(b.cvsW>0||b.err)&&!b.loading&&(n==null||b.stamps.length>=n)){await wait(350);return bookInfo(popOf(pk));}await wait(60);}return bookInfo(popOf(pk));},
  /* 쪽 그림이 다 그려졌나 — 쪽 캔버스를 작게 떠서 흰 점이 아닌 비율(두 번 같으면 끝) */
  async painted(pk,ms){const t0=Date.now();let last=-1;while(Date.now()-t0<(ms||60000)){const w=popOf(pk);const cv=w&&w.querySelector('.cv-bookpg canvas');
    if(cv&&cv.width){const c=document.createElement('canvas');c.width=120;c.height=Math.max(1,Math.round(120*cv.height/cv.width));const g=c.getContext('2d');g.drawImage(cv,0,0,c.width,c.height);
      const d=g.getImageData(0,0,c.width,c.height).data;let n=0;for(let i=0;i<d.length;i+=4)if(d[i]+d[i+1]+d[i+2]<690)n++;const f=+(n/(d.length/4)).toFixed(4);
      if(f>0.004&&f===last)return f;last=f;}await wait(400);}return last;},
  /* 도장 자리 격자 — 쪽 캔버스에서 rect(pt · 왼쪽 아래 원점) 칸을 gw×gh 로 나눠 칸마다 밝기 평균(0~255) · 비교는 하네스가 한다 */
  async grid(pk,docid,p,rect,gw,gh){const w=popOf(pk);const cv=w&&w.querySelector('.cv-bookpg canvas');if(!cv)return null;
    const doc=await __jocvb.doc(docid);const pg=await doc.getPage(p);const v=pg.view,W=v[2]-v[0],H=v[3]-v[1];
    const X0=(rect[0]-v[0])/W*cv.width,X1=(rect[2]-v[0])/W*cv.width,Y0=(v[3]-rect[3])/H*cv.height,Y1=(v[3]-rect[1])/H*cv.height;
    const x0=Math.max(0,Math.floor(X0)),y0=Math.max(0,Math.floor(Y0)),ww=Math.max(1,Math.min(cv.width-x0,Math.ceil(X1-X0))),hh=Math.max(1,Math.min(cv.height-y0,Math.ceil(Y1-Y0)));
    const d=cv.getContext('2d').getImageData(x0,y0,ww,hh).data;const out=[];
    for(let gy=0;gy<gh;gy++)for(let gx=0;gx<gw;gx++){let s=0,n=0;const xa=Math.floor(gx*ww/gw),xb=Math.floor((gx+1)*ww/gw),ya=Math.floor(gy*hh/gh),yb=Math.floor((gy+1)*hh/gh);
      for(let y=ya;y<yb;y++)for(let x=xa;x<xb;x++){const i=(y*ww+x)*4;s+=(d[i]*0.299+d[i+1]*0.587+d[i+2]*0.114);n++;}out.push(n?Math.round(s/n):255);}
    return {g:out,px:[ww,hh]};},
  stampAt(pk,i){const w=popOf(pk);if(!w)return null;const d=w.querySelectorAll('.cv-stamp')[i];if(!d)return null;try{d.scrollIntoView({block:'center'});}catch(e){}return hitOn(d);},
  candRows(pk){const w=popOf(pk);return w?[...w.querySelectorAll('.cv-candrow')].map(r=>({t:txt(r),book:r.dataset.book,p:+r.dataset.p})):null;},
  candAt(pk,i){const w=popOf(pk);const r=w&&w.querySelectorAll('.cv-candrow')[i];if(!r)return null;try{r.scrollIntoView({block:'nearest'});}catch(e){}return hitOn(r);},
  navAt(pk,what){const w=popOf(pk);const t=w&&w.querySelector('.cv-booknav [data-'+what+']');if(!t)return null;try{t.scrollIntoView({block:'nearest'});}catch(e){}return hitOn(t);},
  async pageView(docid,p){const doc=await __jocvb.doc(docid);const pg=await doc.getPage(p);return pg.view;},
  stat(docid){return (window.__jocvb&&__jocvb.C&&__jocvb.C.stat)?JSON.parse(JSON.stringify(__jocvb.C.stat[docid]||null)):null;},
  async idbSeedPdf(docid,md5,n){return idbPut('bookpdf:'+docid,{pdfMd5:md5,buf:new ArrayBuffer(n||4096),at:1});},
  async idbSeedMeta(docid,meta){return idbPut('bookmeta:'+docid,meta);},
  async idbPdfMd5(docid){const r=await idbGet('bookpdf:'+docid);return r?{md5:r.pdfMd5,n:r.buf?r.buf.byteLength:0}:null;},
  async idbStamp(docid){const r=await idbGet('bookstamp:'+docid);return r?{md5:r.pdfMd5,n:(r.rows||[]).length}:null;},
  /* 판례탭 머리 책 칩(.bkgo) */
  bkgoAt(t){const e=[...document.querySelectorAll('.bkgo')].find(x=>txt(x)===t);if(!e)return null;try{e.scrollIntoView({block:'center'});}catch(x){}return hitOn(e);},
  /* ── C 목차노트 📘 · 「교재 자리」 창 ── */
  async note(file){try{closeAllPops();}catch(e){}await popNote(file,null,{clientX:130,clientY:120},1);
    for(let i=0;i<300;i++){const w=popOf('note|'+PLAW()+'|'+file+'|');if(w&&w.querySelector('.ntbox'))break;await wait(50);}await wait(250);return __HB.noteInfo(file);},
  noteInfo(file){const w=popOf('note|'+PLAW()+'|'+file+'|');if(!w)return null;const rows=[...w.querySelectorAll('.ntbox > .ntrow')];
    return {n:rows.length,tbl:rows.map((r,i)=>{const b=r.querySelector(':scope > .ntbl');return b?{i,chips:[...b.querySelectorAll('.chip')].map(c=>({t:txt(c),cls:c.className,title:c.title,
      bg:cs(c,'backgroundColor'),color:cs(c,'color'),op:cs(c,'opacity'),vis:cs(c,'visibility'),disp:cs(c,'display'),fl:cs(c,'filter')}))}:null;}).filter(Boolean),rect:R(w)};},
  chipAt(file,ri,t){const w=popOf('note|'+PLAW()+'|'+file+'|');const r=w&&w.querySelectorAll('.ntbox > .ntrow')[ri];const c=r&&[...r.querySelectorAll('.ntbl .chip')].find(x=>txt(x)===t);
    if(!c)return null;try{c.scrollIntoView({block:'center'});}catch(e){}return hitOn(c);},
  greyRef(){const c=[...document.querySelectorAll('.ntbl .chip.c-prec')][0];return c?{bg:cs(c,'backgroundColor'),color:cs(c,'color'),fs:cs(c,'fontSize'),h:R(c).h}:null;},
  ncbPk(file,end){return 'ncbook|'+PLAW()+'|'+file+'|'+end;},
  ncb(file,end){const w=popOf(__HB.ncbPk(file,end));if(!w)return null;const h=w.querySelector('.mbblist');if(!h)return {open:true,noHost:true};
    return {open:true,title:txt(w.querySelector('.ph .pt')),mbwin:w.classList.contains('mbwin'),kind:w.className,closeBtn:txt(w.querySelector('.ph > button')),loading:/받는 중/.test(txt(h)),text:txt(h),
      rows:[...h.querySelectorAll(':scope > .mbbrow')].map(r=>({book:r.dataset.book||null,p:r.dataset.p?+r.dataset.p:null,bid:r.dataset.bid||null,k:txt(r.querySelector('.hd .k')),pp:txt(r.querySelector('.hd .p')),
        m:[...r.querySelectorAll('.hd .m')].map(txt),sn:txt(r.querySelector('.sn'))})),
      more:[...h.querySelectorAll(':scope > .ncb-more')].map(txt),folded:[...h.querySelectorAll(':scope > div[data-more]')].map(d=>({bk:d.dataset.more,hidden:d.hidden,n:d.querySelectorAll('.mbbrow').length,
        rows:[...d.querySelectorAll('.mbbrow')].map(r=>({p:+r.dataset.p,m:[...r.querySelectorAll('.hd .m')].map(txt)}))})),
      sec:[...h.querySelectorAll('.ncb-sec')].map(txt),none:[...h.querySelectorAll('.mbbnone')].map(txt),pic:[...h.querySelectorAll('.ncb-pic')].map(p=>({cv:!!p.querySelector('canvas'),cvW:(p.querySelector('canvas')||{}).width||0,t:txt(p)})),
      rect:R(w),ptOver:(()=>{const t=w.querySelector('.ph .pt');return t?{sw:t.scrollWidth,cw:t.clientWidth,ws:cs(t,'whiteSpace'),to:cs(t,'textOverflow')}:null;})()};},
  async ncbWait(file,end,ms){const t0=Date.now();while(Date.now()-t0<(ms||60000)){const x=__HB.ncb(file,end);if(x&&x.rows&&!x.loading&&(x.rows.length||x.none.length)){await wait(500);return __HB.ncb(file,end);}await wait(60);}return __HB.ncb(file,end);},
  ncbAt(file,end,what,i){const w=popOf(__HB.ncbPk(file,end));const h=w&&w.querySelector('.mbblist');if(!h)return null;let t=null;
    if(what==='row')t=h.querySelectorAll(':scope > .mbbrow')[i];else if(what==='bid')t=h.querySelector('.mbbrow[data-bid="'+i+'"]');
    else if(what==='more')t=h.querySelectorAll(':scope > .ncb-more')[i];else if(what==='pic')t=h.querySelector('.ncb-pic');
    else if(what==='fold')t=h.querySelectorAll(':scope > div[data-more] .mbbrow')[i];
    if(!t)return null;try{t.scrollIntoView({block:'nearest'});}catch(e){}return hitOn(t);},
  async ncbOpen(file,end){try{await ncBookOpen(file,end,{clientX:200,clientY:160},2);}catch(e){return String(e);}return true;},
  async picWait(file,end,ms){const t0=Date.now();while(Date.now()-t0<(ms||60000)){const x=__HB.ncb(file,end);if(x&&x.pic&&x.pic.length&&x.pic.every(p=>p.cv||/아직 없/.test(p.t)))return x.pic;await wait(100);}return (__HB.ncb(file,end)||{}).pic;},
  /* 정리캔버스 — 지금 탭 · 고른 블록 */
  canvas(){const e=document.querySelector('#cvWorld .cv-blk.on');let bid=null;
    try{if(e){const C=viewCanvas._cv();const p=C.D.pages[+e.dataset.p-1];const b=p&&p.blocks[+e.dataset.b];bid=b?b.bid:null;}}catch(x){}
    const ow=pops().find(x=>(x._pk||'').indexOf('cv|omr|')===0),ost=ow&&ow._omr;   /* A-6(a) 9/30 — omrpop C-1: 정리OMR 팝업 목표 블록(ctx.bids) */
    return {tab:S.tab,law:S.law,stage:!!document.getElementById('cvStage'),sel:e?e.dataset.p+'|'+e.dataset.b:null,bid,pops:pops().map(x=>x._pk),omr:ost&&ost.ctx?ost.ctx.bids.slice():null};},
  async canvasWait(bid,ms){const t0=Date.now();while(Date.now()-t0<(ms||30000)){const c=__HB.canvas();if((c.stage&&c.bid===bid)||(c.omr&&c.omr.indexOf(bid)>=0)){await wait(300);return __HB.canvas();}await wait(80);}return __HB.canvas();},   /* A-6(a) 9/30 — 정리OMR 팝업 목표도 기다림(바탕 판은 옛 길 그대로) */
  jstate(k){try{return viewCanvas.jari&&viewCanvas.jari.state?viewCanvas.jari.state(k):(window.__jocvj?__jocvj.state(k):null);}catch(e){return 'ERR '+e;}},
  ls(k){try{return JSON.parse(localStorage.getItem(k)||'null');}catch(e){return null;}},
  lsSet(k,v){localStorage.setItem(k,JSON.stringify(v));return true;},
  /* ── D 폰 손질 ── */
  rail(){const r=document.getElementById('hrail');if(!r)return null;return {oh:r.offsetHeight,ch:r.clientHeight,sb:r.offsetHeight-r.clientHeight,sw:r.scrollWidth,cw:r.clientWidth,sl:r.scrollLeft,
    sbw:cs(r,'scrollbarWidth'),ox:cs(r,'overflowX'),rect:R(r),pseudo:(()=>{try{return getComputedStyle(r,'::-webkit-scrollbar').display;}catch(e){return null;}})()};},
  railSet(x){const r=document.getElementById('hrail');if(!r)return null;r.scrollLeft=x;return r.scrollLeft;},
  async card(ck,x,y){try{closeAllPops();}catch(e){}await popCard4('기출',ck,{clientX:x||40,clientY:y||120},1);await wait(700);const w=pops()[pops().length-1];return w?{pk:w._pk,rect:R(w),mh:w.style.maxHeight,h:w.style.height,sized:w.classList.contains('sized')}:null;},
  popInfo(pk){const w=pk?popOf(pk):pops()[pops().length-1];return w?{pk:w._pk,rect:R(w),mh:w.style.maxHeight,h:w.style.height,sized:w.classList.contains('sized'),cmh:cs(w,'maxHeight')}:null;},
  rszAt(pk){const w=pk?popOf(pk):pops()[pops().length-1];const h=w&&w.querySelector(':scope > .prsz');return h?hitOn(h):null;},
  cfg(k){return JSON.parse(JSON.stringify((S.popCfg||{})[k]||null));},
  cfgSet(k,v){S.popCfg=S.popCfg||{};S.popCfg[k]=v;try{uiSave();}catch(e){}return true;},
  vv(){const v=window.visualViewport;return {iw:innerWidth,ih:innerHeight,vw:v?v.width:null,vh:v?v.height:null,vt:v?v.offsetTop:null};},
  errs(){return (window.__ERR||[]).slice();}
};
})();
