/* _harness_jo_pop_moknote_tests.js — _task_jo_pop_moknote 하네스가 페이지에 넣는 도구(__HP).
   BASE(dd9d89f)·NEW 둘 다에 같은 것을 넣는다 — 없는 것(#mokBtn · .eqlock …)은 빈 값으로 돌려준다.
   재는 것 = DOM 실물(있는가·몇 개·글자·자리 getBoundingClientRect·계산 스타일) · 저장소 값(localStorage). 픽셀은 안 찍는다(캡처는 사용자용). */
(function(){
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const txt=e=>e?(e.textContent||'').replace(/\s+/g,' ').trim():'';
const R=e=>{if(!e)return null;const r=e.getBoundingClientRect();
  return {x:+r.left.toFixed(2),y:+r.top.toFixed(2),w:+r.width.toFixed(2),h:+r.height.toFixed(2),r:+r.right.toFixed(2),b:+r.bottom.toFixed(2),
          cx:+(r.left+r.width/2).toFixed(2),cy:+(r.top+r.height/2).toFixed(2)};};
const cs=(e,p)=>e?getComputedStyle(e)[p]:null;
const idle=async()=>{for(let i=0;i<240;i++){if(!busy)return true;await wait(25);}return false;};
function clean(){try{closeAllPops();}catch(e){}document.querySelectorAll('.pitmenu').forEach(x=>x.remove());}
function hitOn(t){const r=R(t);if(!r)return null;const onScreen=r.cy>0&&r.cy<innerHeight&&r.cx>0&&r.cx<innerWidth;
  const at=onScreen?document.elementFromPoint(r.cx,r.cy):null;
  return Object.assign(r,{on:!!at&&(at===t||t.contains(at))&&onScreen,at:at?(String(at.className||at.tagName).slice(0,40)):null,onScreen});}
async function scrollHit(t){if(!t)return null;try{t.scrollIntoView({block:'center',inline:'nearest'});}catch(e){}await wait(200);return hitOn(t);}
/* 줄 글자 — 접기 표시·칩·임베드 상자 등 줄에 덧붙는 것은 뺀다(row.t 와 맞대는 글자) */
const EXC='.htog,.stkchip,.pitwho,sup.fn,.embed,.embx,.lbl,.vimg,.eqpend,.badge,.pitflag,.eqflag,.stkanc';
function plainOf(ln){const c=ln.cloneNode(true);c.querySelectorAll(EXC).forEach(x=>x.remove());return c.textContent;}
/* 첫 「보이는」 것의 왼쪽 — 폭 0 꾸밈(mdtab·mdhash·mdmark) 안 글자는 건너뛴다 · 공백은 건너뛴다.
   그림 줄(.vimg · 자리표 글자는 제 안쪽 여백만큼 들어가 있다)은 그림 상자 왼쪽 · 블록번호(.blockid · margin-left 4)는 그 여백을 뺀 왼쪽 */
function firstGlyph(ln){const w=document.createTreeWalker(ln,NodeFilter.SHOW_TEXT);let n;
  while((n=w.nextNode())){const pe=n.parentElement;if(!pe||pe.closest('.mdtab,.mdhash,.mdmark,.htog,.stkchip,.pitwho,sup.fn,.embx'))continue;
    const v=n.nodeValue||'';const k=v.search(/\S/);if(k<0)continue;
    const vi=pe.closest('.vimg');if(vi){const r=vi.getBoundingClientRect();return {x:+r.left.toFixed(2),ch:'[그림]',kind:'vimg'};}
    const bi=pe.closest('.blockid');if(bi&&bi.firstChild&&(bi.textContent||'').trim()===(ln.textContent||'').trim()){const r=bi.getBoundingClientRect();return {x:+(r.left-parseFloat(getComputedStyle(bi).marginLeft)).toFixed(2),ch:'^',kind:'blockid'};}
    const r=document.createRange();r.setStart(n,k);r.setEnd(n,k+1);const b=r.getBoundingClientRect();return {x:+b.left.toFixed(2),ch:v[k],kind:'text'};}
  return null;}
function popInfo(p){const ph=p.querySelector('.ph');const pt=ph&&ph.querySelector('.pt');
  return {pk:p._pk||null,cls:p.className,title:txt(pt),head:ph?ph.innerText.replace(/\s+/g,' ').trim():'',pdrag:ph?ph.querySelectorAll('.pdrag').length:-1,
    eq:ph?(ph.textContent.indexOf('≡')>=0):null,prsz:!!p.querySelector(':scope > .prsz'),rect:R(p),pos:{l:parseFloat(p.style.left)||0,t:parseFloat(p.style.top)||0},
    z:+p.style.zIndex||0,sized:p.classList.contains('sized')};}
const popBy=pk=>POPS.find(x=>x._pk===pk)||null;
const lastPop=()=>POPS[POPS.length-1]||null;
async function popWait(pred,ms){for(let i=0;i<(ms||3000)/50;i++){const p=POPS.find(pred);if(p)return p;await wait(50);}return null;}
function pitWinEl(){return [...document.querySelectorAll('.pop')].reverse().find(p=>p.querySelector('textarea.memoin')&&(p._pk||'').indexOf('fn|')===0)||null;}

window.__HP={
  wait,
  errs(){return (window.__ERR||[]).slice();},
  quiet(){try{clearTimeout(recTouchT);}catch(e){}return true;},
  clean(){clean();return POPS.length;},
  async board(law,kind,o){clean();await idle();S.law=law;S.tab='cha2';S.boardKind=kind;S.series='';S.yearFilter='';S.cha2Sel=null;S.cha2Filter={};
    Object.assign(S,o||{});await render();await idle();await wait(500);return true;},
  async goPrec(law,id,tab){clean();await idle();S.law=law;S.tab='prec';S.prec=id;S.precTab=tab||'요약';S.precQ='';S.precFilter={};await render();await idle();await wait(500);return !!document.querySelector('#slot');},
  async goJo(law,jo){clean();await idle();S.law=law;S.tab='jo';S.jo=jo;S.joMode='본문';await render();await idle();await wait(500);return true;},
  pops(){return POPS.map(popInfo);},
  popInfo(pk){const p=pk?popBy(pk):lastPop();return p?popInfo(p):null;},
  async popHead(pk){const p=pk?popBy(pk):lastPop();if(!p)return null;const t=p.querySelector('.ph .pt')||p.querySelector('.ph');return hitOn(t);},
  /* 팝업 일곱 종 — 여는 함수를 직접 부른다(여는 길 자체는 다른 관문이 잰다) */
  async openKind(kind,a){clean();await idle();
    if(kind==='card'){await popCard4(a.kind,a.ck,null,1);}
    else if(kind==='note'){await popNote(a.name,null,null,1);}
    else if(kind==='memo'){const P=await get(PF('리스트'));const p=(P.판례||[]).find(x=>x.id===a.id);popPitList(p,null);}
    else if(kind==='jo'){await popJo(a.law,a.jo,null,1);}
    else if(kind==='claude'){clOpen(a.uid,null);}
    else if(kind==='pit'){pitEdit(a.target,a.struct,a.wi,a.word,null);}
    await wait(500);const p=lastPop();return p?popInfo(p):null;},
  /* ── 포스트잇 ── */
  pitsRaw(){try{return JSON.parse(localStorage.getItem('jopangi.postit')||'{}');}catch(e){return {};}},
  seedPits(obj,replace){const A=replace?{}:pitAll();Object.keys(obj).forEach(k=>{A[k]=obj[k];});PITREC=A;lsWrite(PIT_KEY,A,'h');try{PITIDX.rec=null;}catch(e){}return Object.keys(A).length;},
  pitKey(t,s,w,wd){return pitKey(t,s,w,wd);},
  setPopCfg(kind,c){S.popCfg=S.popCfg||{};if(c==null)delete S.popCfg[kind];else S.popCfg[kind]=c;return true;},
  getPopCfg(kind){const c=(S.popCfg||{})[kind];return c?JSON.parse(JSON.stringify(c)):null;},
  async pitwAt(word,scopeSel){const sc=scopeSel?document.querySelector(scopeSel):document;if(!sc)return null;
    const w=[...sc.querySelectorAll('.pitw')].find(x=>(x.firstChild&&x.firstChild.nodeValue||x.textContent||'').indexOf(word)===0||x.textContent.indexOf(word)===0);return scrollHit(w);},
  pitWin(){const p=pitWinEl();if(!p)return null;const ta=p.querySelector('textarea.memoin');const btns=[...p.querySelectorAll('.memobtn button')];
    const save=btns.find(b=>/저장/.test(b.textContent));
    return {pk:p._pk,title:txt(p.querySelector('.ph .pt')),head:p.querySelector('.ph').innerText.replace(/\s+/g,' ').trim(),grey:[...p.querySelectorAll('.pb > .cdim')].map(txt),
      btns:btns.map(txt),gas:(p.textContent||'').indexOf('GAS')>=0,lock:(p.textContent||'').indexOf('🔒')>=0,
      ta:{h:ta.offsetHeight,sh:ta.scrollHeight,ch:ta.clientHeight,val:ta.value,rect:R(ta)},rect:R(p),style:{h:p.style.height,mh:p.style.maxHeight,top:p.style.top},
      pscroll:{sh:p.scrollHeight,ch:p.clientHeight,st:p.scrollTop},saveHit:save?hitOn(save):null,delHit:(()=>{const d=btns.find(b=>/삭제/.test(b.textContent));return d?hitOn(d):null;})(),
      taHit:hitOn(ta),innerH:innerHeight,szKeepH:!!p._szKeepH};},
  async pitTaFocus(){const p=pitWinEl();if(!p)return null;const ta=p.querySelector('textarea.memoin');ta.focus();ta.setSelectionRange(ta.value.length,ta.value.length);await wait(50);return hitOn(ta);},
  /* webkit 대안 — playwright webkit 의 합성 마우스는 네이티브 크기 손잡이(resize:vertical)를 못 잡는다(바탕도 74→74).
     칸 높이를 손으로 바꾼 것처럼 +dy 로 두고 mouseup·pointerup 을 던져 앱의 「손 높이 기억」 길만 탄다 */
  pitTaResize(dy){const p=pitWinEl();if(!p)return null;const ta=p.querySelector('textarea.memoin');const h=ta.offsetHeight;ta.style.height=(h+dy)+'px';
    ta.dispatchEvent(new MouseEvent('mouseup',{bubbles:true}));ta.dispatchEvent(new PointerEvent('pointerup',{bubbles:true}));return {h0:h,h1:ta.offsetHeight};},
  pitTaGrip(){const p=pitWinEl();if(!p)return null;const ta=p.querySelector('textarea.memoin');const r=ta.getBoundingClientRect();return {x:r.right-4,y:r.bottom-4,h:ta.offsetHeight};},
  async pitSaveClick(){const p=pitWinEl();if(!p)return false;const b=[...p.querySelectorAll('.memobtn button')].find(x=>/저장/.test(x.textContent));if(!b)return false;b.click();await wait(400);return true;},
  /* ── 메모 칩 ── */
  memoChips(where,id){let sc=null;
    if(where==='prec2')sc=[...document.querySelectorAll('#slot .plist .prow')].find(r=>(r.textContent||'').indexOf(id)>=0);
    else if(where==='prec3'||where==='jo3')sc=document.querySelector('#slot .main');
    if(!sc)return {found:false};
    const cands=[...sc.querySelectorAll('.chip')].filter(c=>/🗒/.test(c.textContent));
    return {found:true,chips:cands.map(c=>({cls:c.className,text:txt(c),own:(c.firstChild&&c.firstChild.nodeType===3?c.firstChild.nodeValue:'').trim(),who:[...c.querySelectorAll('.chip.who')].map(txt),title:c.title,hit:hitOn(c)}))};},
  async memoChipAt(where,id){let sc=null;
    if(where==='prec2')sc=[...document.querySelectorAll('#slot .plist .prow')].find(r=>(r.textContent||'').indexOf(id)>=0);
    else sc=document.querySelector('#slot .main');
    const c=sc?[...sc.querySelectorAll('.chip')].find(x=>/🗒/.test(x.textContent)):null;return scrollHit(c);},
  /* ── 2차 카드 팝업 ── */
  async cardScan(kind,list){const out=[];for(const ck of list){clean();await popCard4(kind,ck,null,1);await wait(30);
      const p=POPS.find(x=>(x._pk||'').indexOf('🧾 '+kind+' · ')>=0);if(!p){out.push({ck:ck,none:true});continue;}
      const b=p.querySelector('.pb');const kids=[...b.children];const tabs=b.querySelector(':scope > .gtabs');const ti=kids.indexOf(tabs);
      const beforeTabs=ti>0?kids[ti-1]:null;
      const flexDivs=kids.filter(k=>k.tagName==='DIV'&&/display:\s*flex/.test(k.getAttribute('style')||''));
      out.push({ck:ck,rail:(b.textContent||'').indexOf('2차 레일로')>=0,fm:[...b.querySelectorAll(':scope > .chips .chip, :scope > .chips a')].map(txt),
        gi:[...b.querySelectorAll(':scope > .chips .chip')].filter(c=>/^기출:/.test(txt(c))).length,
        top:flexDivs.map(d=>({n:d.children.length,kids:[...d.children].map(c=>c.className+'|'+txt(c).slice(0,24))})),
        emptyTop:flexDivs.filter(d=>d.children.length===0).length,before:beforeTabs?(beforeTabs.className||'div')+':'+beforeTabs.children.length:null});
      clean();}
    return out;},
  /* ── 목차노트 ── */
  mokBtn(){const b=document.getElementById('mokBtn');if(!b)return null;const pv=b.previousElementSibling,nx=b.nextElementSibling;
    return {text:txt(b),dis:b.disabled,title:b.title,cls:b.className,prev:pv?txt(pv):null,prevR:R(pv),next:nx?(nx.id||nx.className||nx.tagName):null,rect:R(b),hit:hitOn(b)};},
  async mokBtnAt(){return scrollHit(document.getElementById('mokBtn'));},
  mokList(){const p=POPS.find(x=>(x._pk||'').indexOf('moknote|')===0);if(!p)return null;
    const rows=[...p.querySelectorAll('.mklist .mkr')];
    return {pk:p._pk,title:txt(p.querySelector('.ph .pt')),rect:R(p),n:rows.length,sub:[...p.querySelectorAll('.pb > .cdim')].map(txt),
      rows:rows.map(r=>({note:r.dataset.note,name:txt(r.querySelector('.nm')),pad:parseFloat(cs(r,'paddingLeft')),fw:cs(r,'fontWeight'),on:r.classList.contains('on'),bg:cs(r,'backgroundColor'),
        chips:[...r.querySelectorAll('.ck')].map(c=>({t:txt(c),bg:cs(c,'backgroundColor'),fg:cs(c,'color'),fs:cs(c,'fontSize'),title:c.title})),
        nmWrap:(()=>{const n=r.querySelector('.nm');return n?{ws:cs(n,'whiteSpace'),to:cs(n,'textOverflow'),h:n.getBoundingClientRect().height}:null;})()})),
      text:p.innerText};},
  async mokRowAt(note){const p=POPS.find(x=>(x._pk||'').indexOf('moknote|')===0);if(!p)return null;
    const r=[...p.querySelectorAll('.mklist .mkr')].find(x=>x.dataset.note===note);if(!r)return null;r.scrollIntoView({block:'center'});await wait(200);return hitOn(r.querySelector('.nm')||r);},
  /* ── 노트 팝업 줄 ── */
  async noteRead(name,law){const N=await get(NF());const rec=N[name];const p=POPS.find(x=>(x._pk||'')==='note|'+(law||PLAW())+'|'+name+'|');if(!p||!rec)return {found:!!p,rec:!!rec};
    const rows=[...p.querySelectorAll('.ntrow')];
    const out=rows.map((w,ri)=>{const ln=w.querySelector(':scope > .ln');const row=rec.행[ri]||{};const r=R(ln);const pad=parseFloat(cs(ln,'paddingLeft'));
      const hg=ln.querySelector(':scope > .htog');const hr=hg?R(hg):null;const fg=firstGlyph(ln);
      return {ri:ri,h:row.h||0,i:row.i||0,pad:pad,mt:parseFloat(cs(ln,'marginTop')),mb:parseFloat(cs(ln,'marginBottom')),fs:cs(ln,'fontSize'),
        plainEq:plainOf(ln)===(row.t||''),plainLen:plainOf(ln).length,tLen:(row.t||'').length,
        padStart:+(r.x+pad).toFixed(2),fx:fg?fg.x:null,fch:fg?fg.ch:null,fkind:fg?fg.kind:null,
        htog:hg?{w:+hr.w.toFixed(2),mr:parseFloat(cs(hg,'marginRight')),r:hr.r,ta:cs(hg,'textAlign')}:null,
        tabs:ln.querySelectorAll('.mdtab').length,hash:(ln.querySelector('.mdhash')||{}).textContent||null};});
    const emb=[...p.querySelectorAll('.embx .ln')].map(ln=>({pad:parseFloat(cs(ln,'paddingLeft')),mt:parseFloat(cs(ln,'marginTop')),mb:parseFloat(cs(ln,'marginBottom')),
      cls:ln.className.replace(/\s*(pitline|blkhl|mdhid)\b/g,''),tabs:ln.querySelectorAll('.mdtab').length}));
    return {found:true,title:txt(p.querySelector('.ph .pt')),badge:[...p.querySelectorAll('.pb > .memobtn .badge')].map(txt),rect:R(p),rows:out,n:rows.length,nrec:rec.행.length,emb:emb};},
  /* 줄 하나의 단어 자리(포스트잇 긁기용) */
  async wordAt(scopeSel,lineIdx,word,lnSel){const sc=typeof scopeSel==='string'?document.querySelector(scopeSel):scopeSel;if(!sc)return null;
    const lns=[...sc.querySelectorAll(lnSel||'.ntrow > .ln')];const ln=lns[lineIdx];if(!ln)return null;ln.scrollIntoView({block:'center'});await wait(200);
    const w=document.createTreeWalker(ln,NodeFilter.SHOW_TEXT);let n,acc='';const nodes=[];while((n=w.nextNode())){nodes.push([n,acc.length]);acc+=n.nodeValue;}
    const k=acc.indexOf(word);if(k<0)return {miss:true,acc:acc.slice(0,80)};
    const mid=k+Math.floor(word.length/2);const hit=nodes.find(([nn,a])=>mid>=a&&mid<a+nn.nodeValue.length);if(!hit)return null;
    const r=document.createRange();r.setStart(hit[0],mid-hit[1]);r.setEnd(hit[0],mid-hit[1]+1);const b=r.getBoundingClientRect();
    return {cx:+(b.left+b.width/2).toFixed(2),cy:+(b.top+b.height/2).toFixed(2),on:true};},
  async notePop(name,law){return popWait(x=>(x._pk||'')==='note|'+(law||PLAW())+'|'+name+'|',4000).then(p=>p?popInfo(p):null);},
  pitLine(scopeSel,lineIdx,lnSel){const sc=typeof scopeSel==='string'?document.querySelector(scopeSel):scopeSel;if(!sc)return null;const ln=[...sc.querySelectorAll(lnSel||'.ntrow > .ln')][lineIdx];if(!ln)return null;
    return {pitw:[...ln.querySelectorAll('.pitw')].map(x=>({t:txt(x),w:(()=>{const c=x.cloneNode(true);c.querySelectorAll('.pitwho,.stkchip').forEach(y=>y.remove());return c.textContent;})()})),flags:[...ln.querySelectorAll('.pitflag')].map(f=>({cls:f.className,title:f.title})),line:plainOf(ln).slice(0,60)};},
  /* 길게 누르기 대안 — 진짜 입력이 selectionchange 로 취소될 때만 쓴다(앱의 pointerdown 핸들러를 그대로 탄다 · 보고에 「합성」 으로 적는다) */
  async lpSynth(x,y,pt){const t=document.elementFromPoint(x,y);if(!t)return false;
    t.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,cancelable:true,clientX:x,clientY:y,pointerType:pt||'mouse',isPrimary:true,button:0}));
    await wait(700);return !!document.querySelector('.pitmenu');},
  menu(){const m=document.querySelector('.pitmenu');return m?[...m.querySelectorAll('.mi')].map(x=>({t:txt(x),hit:hitOn(x)})):null;},
  async menuClick(i){const m=document.querySelector('.pitmenu');if(!m)return false;const it=m.querySelectorAll('.mi')[i];if(!it)return false;it.click();await wait(400);return true;},
  /* 요약본 · 2차 카드 · 임베드 상자 — 줄 들여쓰기 표 · 접기 표시 */
  padTable(scopeSel){const sc=typeof scopeSel==='string'?document.querySelector(scopeSel):scopeSel;if(!sc)return null;
    return [...sc.querySelectorAll('.ln')].map(ln=>({pad:parseFloat(cs(ln,'paddingLeft')),emb:!!ln.closest('.embx'),cls:ln.className.replace(/\s*(pitline|blkhl)\b/g,'')}));},
  htogGap(scopeSel){const sc=typeof scopeSel==='string'?document.querySelector(scopeSel):scopeSel;if(!sc)return null;
    const out=[];[...sc.querySelectorAll('.ln')].forEach(ln=>{const hg=ln.querySelector(':scope > .htog');if(!hg)return;const hr=R(hg);const fg=firstGlyph(ln);
      out.push({w:+hr.w.toFixed(2),mr:parseFloat(cs(hg,'marginRight')),gap:fg?+(fg.x-hr.r).toFixed(2):null,ch:fg?fg.ch:null,hash:(ln.querySelector('.mdhash')||{}).textContent||null});});
    return out;},
  cardPopEl(){return POPS.find(x=>(x._pk||'').indexOf('🧾 ')>=0)||null;},
  /* ── ✎ ── */
  eqBox(){const b=document.querySelector('.eqedit')||(POPS.find(x=>x.querySelector('.eqform'))||{querySelector:()=>null}).querySelector('.eqform');if(!b)return null;
    const ta=b.querySelector('textarea');const why=b.querySelector('.eqwhy');const chip=b.querySelector('.chip.eqlock');
    const btn=t=>[...b.querySelectorAll('button')].find(x=>x.textContent.indexOf(t)>=0)||null;
    return {val:ta?ta.value:null,chip:chip?{t:txt(chip),title:chip.title,hit:hitOn(chip)}:null,why:why&&why.style.display!=='none'?txt(why):'',
      whyShown:!!(why&&why.style.display!=='none'),fix:!!btn('원래 꼬리로'),save:!!(btn('고침 저장')||btn('고침')),kind:b.classList.contains('eqedit')?'line':'form'};},
  eqSetVal(v){const b=document.querySelector('.eqedit')||(POPS.find(x=>x.querySelector('.eqform'))||{querySelector:()=>null}).querySelector('.eqform');if(!b)return false;
    const ta=b.querySelector('textarea');ta.value=v;ta.dispatchEvent(new Event('input',{bubbles:true}));return true;},
  async eqClick(t){const b=document.querySelector('.eqedit')||(POPS.find(x=>x.querySelector('.eqform'))||{querySelector:()=>null}).querySelector('.eqform');if(!b)return false;
    const x=[...b.querySelectorAll('button')].find(y=>y.textContent.indexOf(t)>=0);if(!x)return false;x.click();await wait(500);return true;},
  async eqClickAt(t){const b=document.querySelector('.eqedit')||(POPS.find(x=>x.querySelector('.eqform'))||{querySelector:()=>null}).querySelector('.eqform');if(!b)return null;
    const x=[...b.querySelectorAll('button')].find(y=>y.textContent.indexOf(t)>=0);return scrollHit(x);},
  eqQueue(){return JSON.parse(JSON.stringify(eqAll()));},
  eqClear(){eqSave([]);return true;},
  eqSeed(items){eqSave(items);return eqAll().length;},
  /* F-4 갈래를 지은 값으로 직접 — 데이터에 노트 밖 꼬리 줄이 0이라(판례 요약본·2차 카드) 실화면으로는 못 탄다 */
  async blkConfirmDirect(){if(typeof eqBlkConfirm!=='function')return null;const out={};
    for(const [k,tg] of [['prec','prec|특허|2021후10374'],['card','card|기출|특기출 25-62-1'],['noteNone','note|특허|하네스-없는-노트']]){
      window.__CONF=[];window.__CONFANS=false;let ran=false;eqBlkConfirm(tg,{id:'abc123',sp:' ',tail:' ^abc123'},()=>{ran=true;});await wait(300);
      const c1=(window.__CONF||[]).slice();window.__CONF=[];window.__CONFANS=true;let ran2=false;eqBlkConfirm(tg,{id:'abc123',sp:' ',tail:' ^abc123'},()=>{ran2=true;});await wait(300);
      out[k]={conf:c1,ranOnCancel:ran,ranOnOk:ran2};}
    window.__CONFANS=undefined;window.__CONF=[];return out;},
  conf(){return (window.__CONF||[]).slice();},
  confSet(v){window.__CONFANS=v;window.__CONF=[];return true;},
  toasts(){return [...document.querySelectorAll('#toasts .toast')].map(txt);},
  async openEqPop(){popEq(null);await wait(400);const p=POPS.find(x=>(x._pk||'').indexOf('✎ 수정 큐')>=0);return !!p;},
  async eqRedoAt(k){const p=POPS.find(x=>(x._pk||'').indexOf('✎ 수정 큐')>=0);if(!p)return null;
    const rows=[...p.querySelectorAll('.eqrow')];const r=rows.find(x=>(x.textContent||'').indexOf(k)>=0)||rows[0];if(!r)return null;
    const b=[...r.querySelectorAll('button')].find(x=>x.textContent.indexOf('다시 고치기')>=0);return scrollHit(b);},
  /* 조문 3단 마크업·글자(바탕 대조용) */
  joDom(){const m=document.querySelector('#slot .main');if(!m)return null;const lns=[...m.querySelectorAll('.box .ln, .ln')].slice(0,80);
    return {n:lns.length,text:lns.map(l=>plainOf(l)).join('\n'),marks:m.querySelectorAll('mark').length,stk:m.querySelectorAll('.stk,.stkchip').length,
      html:lns.map(l=>l.innerHTML.replace(/ style="[^"]*"/g,'')).join('\n').length};},
  pdragAll(){return document.querySelectorAll('.pdrag').length;},
  vw(){return {w:innerWidth,h:innerHeight};}
};
})();
