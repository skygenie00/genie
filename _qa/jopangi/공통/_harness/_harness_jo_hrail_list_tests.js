/* _harness_jo_hrail_list_tests.js — _task_jo_hrail_list 하네스가 페이지에 넣는 도구(__HR).
   BASE(dde3300)·NEW 둘 다에 같은 것을 넣는다 — 없는 것(#hrail·#ordSeg …)은 null 로 돌려준다.
   재는 것 = DOM 실물(있는가·몇 개·글자·자리 getBoundingClientRect·계산 스타일). */
(function(){
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const txt=e=>e?(e.textContent||'').replace(/\s+/g,' ').trim():'';
const R=e=>{if(!e)return null;const r=e.getBoundingClientRect();
  return {x:+r.left.toFixed(2),y:+r.top.toFixed(2),w:+r.width.toFixed(2),h:+r.height.toFixed(2),r:+r.right.toFixed(2),b:+r.bottom.toFixed(2),
          cx:+(r.left+r.width/2).toFixed(2),cy:+(r.top+r.height/2).toFixed(2)};};
const cs=(e,p)=>e?getComputedStyle(e)[p]:null;
const idle=async()=>{for(let i=0;i<200;i++){if(!busy)return true;await wait(25);}return false;};
async function counts(){for(let i=0;i<160;i++){const ns=[...document.querySelectorAll('[data-n]')];
  if(ns.length&&ns.every(n=>n.textContent!==''))return true;await wait(50);}return false;}
function clean(){try{closeAllPops();}catch(e){}const sk=document.getElementById('sk');if(sk)sk.style.display='none';}
function cellsOf(){return [...document.querySelectorAll('#slot .main .cell[data-ck]')];}
function cellByCk(ck){return cellsOf().find(e=>e.dataset.ck===ck)||null;}
function hitOn(t){const r=R(t);if(!r)return null;const at=document.elementFromPoint(r.cx,r.cy);
  const onScreen=r.cy>0&&r.cy<innerHeight&&r.cx>0&&r.cx<innerWidth;
  return Object.assign(r,{on:!!at&&(at===t||t.contains(at))&&onScreen,at:at?(at.className||at.tagName):null,onScreen});}

window.__HR={
  wait,
  async go(law,tab,o){clean();await idle();S.law=law;S.tab=tab;Object.assign(S,o||{});await render();await idle();
    const ok=await counts();await wait(120);return ok;},
  /* 갈래 칸 census — BASE = #rail · NEW = #hrail (칸 차례 · 글자 · 수 · 켜짐) */
  census(){const host=document.getElementById('hrail')||document.getElementById('rail');if(!host)return null;
    return {host:host.id,items:[...host.querySelectorAll('.rb')].map(b=>{const n=b.querySelector('b');
      return {label:(b.firstChild&&b.firstChild.nodeType===3)?b.firstChild.textContent:'',n:n?n.textContent:null,
              k:n&&n.dataset?n.dataset.n:null,on:b.classList.contains('on'),dis:!!b.disabled,text:b.textContent};})};},
  hdr(){const top=document.querySelector('header.topbar'),row=document.getElementById('hsrow'),ks=document.getElementById('ksearch'),
      hb=document.getElementById('hbadges'),hr=document.getElementById('hrail'),laws=document.getElementById('laws'),
      b2=document.querySelector('.body2'),logo=document.querySelector('.topbar .logo'),app=document.getElementById('app');
    const badges=['lblToggle','inkToggle','recBtn','eqBtn','syncChip','whoChip'].map(id=>{const e=document.getElementById(id);
      return {id,text:txt(e),vis:!!e&&cs(e,'display')!=='none',rect:R(e),parent:e&&e.parentElement?(e.parentElement.id||e.parentElement.className):null};});
    const tabs=hr?[...hr.querySelectorAll('.rb')].map(b=>{const n=b.querySelector('b');return {t:b.textContent,rect:R(b),fs:cs(b,'fontSize'),
      color:cs(b,'color'),bg:cs(b,'backgroundColor'),br:cs(b,'borderRadius'),pad:cs(b,'padding'),
      nfs:cs(n,'fontSize'),nop:cs(n,'opacity'),nml:cs(n,'marginLeft'),on:b.classList.contains('on')};}):[];
    const sw=e=>e?[e.scrollWidth,e.clientWidth]:null;
    return {W:innerWidth,H:innerHeight,top:R(top),topCls:top&&top.className,row:R(row),ks:R(ks),
      ksParent:ks&&ks.parentElement?(ks.parentElement.id||ks.parentElement.className):null,
      ksStyle:ks?[cs(ks,'flexGrow'),cs(ks,'maxWidth'),cs(ks,'height')]:null,
      rowStyle:row?[cs(row,'display'),cs(row,'padding'),cs(row,'backgroundColor'),cs(row,'borderBottomWidth')+' '+cs(row,'borderBottomColor')]:null,
      topBg:cs(top,'backgroundColor'),
      hb:R(hb),hbParent:hb&&hb.parentElement?(hb.parentElement.id||hb.parentElement.tagName.toLowerCase()):null,
      hr:R(hr),hrStyle:hr?{bl:cs(hr,'borderLeftWidth'),blc:cs(hr,'borderLeftColor'),ml:cs(hr,'marginLeft'),pl:cs(hr,'paddingLeft'),gap:cs(hr,'gap')}:null,
      laws:R(laws),lawsT:laws?[...laws.children].map(txt):null,logo:R(logo),logoT:txt(logo),body2:R(b2),badges,tabs,
      sw:{doc:sw(document.documentElement),body:sw(document.body),app:sw(app),top:sw(top),row:sw(row)},
      rail:document.querySelectorAll('#rail,.rail').length,
      children:top?[...top.children].map(e=>e.id||e.className||e.tagName):null,
      b2kids:b2?[...b2.children].map(e=>e.id||e.className||e.tagName):null};},
  /* 첫 줄에 배지까지 다 넣으면 몇 px 가 드나(보고용 · 옮기지 않고 잰다) */
  need(){const top=document.querySelector('header.topbar'),hb=document.getElementById('hbadges');if(!top||!hb)return null;
    const kids=[...top.children].filter(e=>cs(e,'display')!=='none');let w=0;
    /* #hbadges 의 margin-left:auto 는 「남는 자리」라 셈에서 뺀다 */
    kids.forEach(e=>{w+=e.getBoundingClientRect().width+(e===hb?0:parseFloat(cs(e,'marginLeft')))+parseFloat(cs(e,'marginRight'));});
    if(hb.parentElement!==top)w+=hb.getBoundingClientRect().width;
    const gap=parseFloat(cs(top,'columnGap'))||8,n=kids.length+(hb.parentElement!==top?1:0);
    const pad=parseFloat(cs(top,'paddingLeft'))+parseFloat(cs(top,'paddingRight'));
    return {need:Math.round(w+gap*(n-1)+pad),avail:innerWidth,items:n};},
  async ctrlK(){clean();const ev=new KeyboardEvent('keydown',{key:'k',ctrlKey:true,bubbles:true,cancelable:true});
    document.dispatchEvent(ev);await wait(150);const sk=document.getElementById('sk');const r={open:!!sk&&sk.style.display==='block',
      focus:document.activeElement&&document.activeElement.id};clean();return r;},
  skOpen(){const sk=document.getElementById('sk');return !!sk&&sk.style.display==='block';},
  /* 1차객 세 화면 — 첫 화면(.mbh) · 문제풀이(.mbsbar) · 기출 */
  async jim(screen){clean();await idle();S.law='특허법';S.tab='jimun';S.jimunTab='ox';S.mok='';S.oxQueue='';S.jtFold=false;S.jtW=272;
    await render();await idle();await wait(900);
    if(screen==='solve'){const row=[...document.querySelectorAll('.mbur')].find(e=>/총 [1-9]/.test(txt(e)));
      if(!row)return {err:'풀 단원 줄 없음'};row.click();await wait(300);await idle();await wait(1500);}
    if(screen==='gichul'){S.jimunTab='gichul';await render();await idle();await wait(1200);}
    const main=document.querySelector('#slot .main');if(main)main.scrollTop=0;await wait(150);
    const jt=document.getElementById('jtree'),gp=document.getElementById('jtgrip'),b2=document.querySelector('.body2');
    const first=main?[...main.children].find(e=>cs(e,'display')!=='none'&&e.getBoundingClientRect().height>0):null;
    const mbh=document.querySelector('#slot .mbh');
    return {screen,mok:S.mok,jtab:S.jimunTab,main:R(main),mainCW:main?main.clientWidth:null,mainPad:cs(main,'padding'),mainCls:main&&main.className,
      jt:R(jt),jtDisp:jt?jt.style.display:null,grip:R(gp),body2:R(b2),first:first?{cls:first.className,rect:R(first)}:null,
      mbh:mbh?{br:cs(mbh,'borderRadius'),bl:cs(mbh,'borderLeftWidth'),brw:cs(mbh,'borderRightWidth'),bt:cs(mbh,'borderTopWidth'),
               bb:cs(mbh,'borderBottomWidth'),sh:cs(mbh,'boxShadow'),mb:cs(mbh,'marginBottom'),rect:R(mbh)}:null,
      qcards:document.querySelectorAll('#slot .qwrap,#slot .qcard').length};},
  async pads(){const o={};for(const t of ['jo','prec','cha2','omr']){clean();await idle();S.law='특허법';S.tab=t;await render();await idle();await wait(300);
      const m=document.querySelector('#slot .main');o[t]=m?[cs(m,'padding'),m.className]:null;}return o;},
  /* 2차 보드 — 기출·GS = 목록(NEW) / 격자(BASE) · 사례 = 격자 */
  async board(law,kind,o){clean();await idle();S.law=law;S.tab='cha2';S.boardKind=kind;S.series='';S.yearFilter='';S.cha2Sel=null;S.cha2Filter={};
    Object.assign(S,o||{});await render();await idle();await wait(700);return this.boardRead();},
  boardRead(){const main=document.querySelector('#slot .main');const bar=main?main.firstElementChild:null;
    const cells=cellsOf();
    const rows=cells.map(c=>({ck:c.dataset.ck,cls:c.className,code:txt(c.querySelector('.c2code')),t1:txt(c.querySelector('.c2t1')),
      kind:txt(c.querySelector('.chip.c2k')),rn:txt(c.querySelector('.c2rn')),num:txt(c.querySelector('.chip.c2n')),
      score:txt(c.querySelector('.chip.c-score')),title:txt(c.querySelector('.c2t2')||c.querySelector('.ctitle')),
      pdf:[...c.querySelectorAll('a.chip.c-pdf')].map(a=>a.getAttribute('href')),
      kids:c.classList.contains('c2row')?[...c.children].map(e=>e.className):null,
      t1kids:c.querySelector('.c2t1')?[...c.querySelector('.c2t1').children].map(e=>e.className):null}));
    const seg=document.getElementById('ordSeg');
    const pills=bar?[...bar.querySelectorAll(':scope > button.pill')]:[];
    const sak=pills.find(b=>/^사례/.test(txt(b)));
    const badge=main?[...main.children].reverse().find(e=>e.classList&&e.classList.contains('badge')):null;
    const lh=document.querySelector('#slot .c2lh');
    return {n:cells.length,rows,
      bar:bar?[...bar.children].map(e=>({tag:e.tagName,id:e.id,cls:e.className,t:txt(e)})):null,
      seg:seg?{rect:R(seg),bg:cs(seg,'backgroundColor'),br:cs(seg,'borderRadius'),bd:cs(seg,'borderTopWidth')+' '+cs(seg,'borderTopColor'),
        btn:[...seg.querySelectorAll('button')].map(b=>({t:txt(b),o:b.dataset.o,on:b.classList.contains('on'),dis:b.disabled,op:cs(b,'opacity'),
          title:b.title,bg:cs(b,'backgroundColor'),color:cs(b,'color'),fw:cs(b,'fontWeight'),fs:cs(b,'fontSize'),pad:cs(b,'padding'),rect:R(b)}))}:null,
      sak:R(sak),
      unpl:txt(document.querySelector('#slot .main .unpl')),badge:txt(badge),
      prow:[...document.querySelectorAll('#slot .plist .prow')].map(e=>({ck:e.dataset.ck,t:txt(e),sel:e.classList.contains('sel')})),
      tree:txt(document.querySelector('#slot .tree')),
      gh:document.querySelectorAll('#slot .main .gh').length,cellnone:document.querySelectorAll('#slot .main .cellnone').length,
      grid:document.querySelectorAll('#slot .main .grid').length,list:document.querySelectorAll('#slot .main .c2list').length,
      lh:lh?{t:txt(lh),kids:[...lh.children].map(e=>e.tagName+'.'+e.className),opts:[...lh.querySelectorAll('option')].map(o=>o.textContent)}:null,
      ysort:txt(document.querySelector('#slot .main .ysort')),
      fold:txt(bar?bar.querySelector('button[data-fold]'):null),
      empty:txt(document.querySelector('#slot .main .empty,#slot .main .emptybox')),
      S:{sel:S.cha2Sel,ys:S.yearSort,c2ord:S.c2ord||null},
      rowStyle:(()=>{const c=document.querySelector('#slot .c2row');if(!c)return null;const k=c.querySelector('.c2code'),t2=c.querySelector('.c2t2'),t1=c.querySelector('.c2t1'),ch=c.querySelector('.chip.c2k');
        return {disp:cs(c,'display'),cols:cs(c,'gridTemplateColumns'),gap:cs(c,'columnGap'),pad:cs(c,'padding'),mt:cs(c,'marginTop'),bd:cs(c,'borderTopWidth')+' '+cs(c,'borderTopColor'),
          br:cs(c,'borderRadius'),bg:cs(c,'backgroundColor'),codeFont:cs(k,'fontFamily'),codeFs:cs(k,'fontSize'),codeColor:cs(k,'color'),
          t1fs:cs(t1,'fontSize'),t1gap:cs(t1,'columnGap'),t2fs:cs(t2,'fontSize'),t2ws:cs(t2,'whiteSpace'),kBg:cs(ch,'backgroundColor'),kColor:cs(ch,'color')};})()};},
  /* 결론반대·누락(hot) 줄 · 선택(sel) 줄의 테두리 — BASE 는 칸(.cell) · NEW 는 줄(.c2row) */
  hotStyle(){const c=document.querySelector('#slot .main .cell.hot');const s=document.querySelector('#slot .main .cell.sel');
    return {hot:c?{ck:c.dataset.ck,row:c.classList.contains('c2row'),bd:cs(c,'borderTopColor'),bg:cs(c,'backgroundColor')}:null,
            sel:s?{ck:s.dataset.ck,row:s.classList.contains('c2row'),bd:cs(s,'borderTopColor'),sh:cs(s,'boxShadow')}:null,
            nhot:document.querySelectorAll('#slot .main .cell.hot').length};},
  async clickAt(ck,part){const c=cellByCk(ck);if(!c)return null;
    const t=part==='code'?c.querySelector('.c2code'):part==='score'?c.querySelector('.chip.c-score'):(c.classList.contains('c2row')?c.querySelector('.c2t2'):c.querySelector('.ctitle'));
    if(!t)return {miss:part};t.scrollIntoView({block:'center'});await wait(250);return hitOn(t);},
  async popRead(){for(let i=0;i<80;i++){if(document.querySelectorAll('.pop').length)break;await wait(50);}
    let last=null,same=0;for(let i=0;i<80;i++){const t=[...document.querySelectorAll('.pop')].map(x=>x.innerText).join('\n␞\n');
      if(t===last){if(++same>=4)break;}else{same=0;last=t;}await wait(100);}
    const p=document.querySelector('.pop');
    return {n:document.querySelectorAll('.pop').length,text:last,sel:S.cha2Sel,rect:R(p),
      head:p?hitOn(p.querySelector('.ph .pt')||p.querySelector('.ph')):null,tab:txt(p?p.querySelector('.gtabs .tool.on'):null)};},
  popPos(){const p=document.querySelector('.pop');return p?{l:parseFloat(p.style.left)||0,t:parseFloat(p.style.top)||0,rect:R(p)}:null;},
  closePops(){clean();return document.querySelectorAll('.pop').length;},
  async prowAt(ck){const p=[...document.querySelectorAll('#slot .plist .prow')].find(e=>e.dataset.ck===ck);if(!p)return null;
    p.scrollIntoView({block:'center'});await wait(200);return hitOn(p);},
  centered(ck){const main=document.querySelector('#slot .main');const c=cellByCk(ck);if(!main||!c)return null;const mr=R(main),cr=R(c);
    return {dy:+(cr.cy-mr.cy).toFixed(1),top:main.scrollTop,max:main.scrollHeight-main.clientHeight,sel:c.classList.contains('sel'),S:S.cha2Sel,
      prowSel:[...document.querySelectorAll('#slot .plist .prow.sel')].map(e=>e.dataset.ck)};},
  async scrollTo(ck){const main=document.querySelector('#slot .main');const c=cellByCk(ck);if(!main||!c)return null;
    const mr=main.getBoundingClientRect(),cr=c.getBoundingClientRect();main.scrollTop+=Math.round((cr.top+cr.height/2)-(mr.top+mr.height/2));
    await wait(900);return {S:S.cha2Sel,prowSel:[...document.querySelectorAll('#slot .plist .prow.sel')].map(e=>e.dataset.ck),
      rowSel:cellsOf().filter(e=>e.classList.contains('sel')).map(e=>e.dataset.ck)};},
  async ysortAt(){const b=document.querySelector('#slot .main .ysort');if(!b)return null;b.scrollIntoView({block:'center'});await wait(150);return hitOn(b);},
  async setYear(y){const s=document.querySelector('#slot .main select.ysel');if(!s)return null;s.value=String(y);s.dispatchEvent(new Event('change'));
    await wait(100);await idle();await wait(500);return this.boardRead();},
  async segAt(o){const b=document.querySelector('#ordSeg [data-o="'+o+'"]');if(!b)return null;b.scrollIntoView({block:'center'});await wait(200);return hitOn(b);},
  mark(){const m=document.querySelector('#slot .main');if(m)m.__hrMark=1;return !!m;},
  marked(){const m=document.querySelector('#slot .main');return !!(m&&m.__hrMark);},
  tabAt(k){const n=document.querySelector('#hrail [data-n="'+k+'"]');const b=n?n.closest('.rb'):null;return b?hitOn(b):null;},
  ksAt(){const k=document.getElementById('ksearch');return k?hitOn(k):null;},
  state(){return {tab:S.tab,law:S.law,kind:S.boardKind,on:txt(document.querySelector('#hrail .rb.on,#rail .rb.on'))};},
  /* 배지 글자가 줄면(on) 첫 줄로 올라오고 되돌리면(off) 다시 내려가나 — ResizeObserver 길 */
  async badgeShrink(on){['lblToggle','inkToggle','recBtn','eqBtn','syncChip'].forEach(id=>{const e=document.getElementById(id);if(!e)return;
      if(on){e.__hrD=e.style.display;e.style.display='none';}else{e.style.display=e.__hrD||'';}});
    await wait(450);return this.hdr();},
  /* 목록 줄 안 요소가 줄 테두리(안쪽)를 넘지 않나 — 앞 30줄 */
  rowsFit(){const rows=[...document.querySelectorAll('#slot .c2row')].slice(0,30);const bad=[];
    rows.forEach(r=>{const rr=r.getBoundingClientRect();const lim=rr.right-parseFloat(cs(r,'paddingRight'))+0.5;
      r.querySelectorAll('.c2t1>*,.c2code,.c2t2').forEach(e=>{const er=e.getBoundingClientRect();
        if(er.right>lim)bad.push([r.dataset.ck.slice(-24),e.className,Math.round(er.right-lim)]);});});
    return {n:rows.length,nbad:bad.length,bad:bad.slice(0,6),w:rows[0]?Math.round(rows[0].getBoundingClientRect().width):null};},
  errs(){return (window.__ERR||[]).slice();}
};
})();
