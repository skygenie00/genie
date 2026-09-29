/* _harness_jo_mok_popup_phone_tests.js — _task_jo_mok_popup_phone 하네스가 페이지에 넣는 도구(__HM).
   BASE(c9d5bc0)·NEW 둘 다에 같은 것을 넣는다 — 없는 것(목차노트 탭 · 「모두 닫기」 …)은 빈 값으로 돌려준다.
   재는 것 = DOM 실물(있는가·몇 개·글자·자리 getBoundingClientRect·elementFromPoint·계산 스타일) · 앱 상태(S · POPS).
   closeAllPops·toast 는 감싸서 센다(하네스가 부른 것은 안 센다). 픽셀은 안 찍는다. */
(function(){
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const txt=e=>e?(e.textContent||'').replace(/\s+/g,' ').trim():'';
const R=e=>{if(!e)return null;const r=e.getBoundingClientRect();
  return {x:+r.left.toFixed(2),y:+r.top.toFixed(2),w:+r.width.toFixed(2),h:+r.height.toFixed(2),r:+r.right.toFixed(2),b:+r.bottom.toFixed(2),
          cx:+(r.left+r.width/2).toFixed(2),cy:+(r.top+r.height/2).toFixed(2)};};
const cs=(e,p)=>e?getComputedStyle(e)[p]:null;
const idle=async()=>{for(let i=0;i<320;i++){if(!busy)return true;await wait(25);}return false;};
const SPY={closeAll:0,toasts:[],mute:0};
(function(){const oc=closeAllPops;closeAllPops=function(){if(!SPY.mute)SPY.closeAll++;return oc.apply(this,arguments);};
  const ot=toast;toast=function(m,b){SPY.toasts.push(String(m));return ot.apply(this,arguments);};})();
function clean(){SPY.mute++;try{closeAllPops();}catch(e){}SPY.mute--;document.querySelectorAll('.pitmenu').forEach(x=>x.remove());try{getSelection().removeAllRanges();}catch(e){}}
function vv(){const v=window.visualViewport;return v?{x:v.offsetLeft,y:v.offsetTop,w:v.width,h:v.height}:{x:0,y:0,w:innerWidth,h:innerHeight};}
function hitOn(t){const r=R(t);if(!r)return null;const V=vv();
  const onScreen=r.cy>V.y&&r.cy<V.y+V.h&&r.cx>V.x&&r.cx<V.x+V.w;
  const at=onScreen?document.elementFromPoint(r.cx,r.cy):null;
  return Object.assign(r,{on:!!at&&(at===t||t.contains(at))&&onScreen,at:at?(String(at.className||at.tagName).slice(0,40)):null,onScreen});}
async function scrollHit(t){if(!t)return null;try{t.scrollIntoView({block:'center',inline:'nearest'});}catch(e){}await wait(220);return hitOn(t);}
const topPop=()=>{let t=null,z=-1e9;POPS.forEach(q=>{const k=+q.style.zIndex||0;if(k>=z){z=k;t=q;}});return t;};
const popBy=pk=>POPS.find(x=>x._pk===pk)||null;
const lastPop=()=>POPS[POPS.length-1]||null;
async function popWait(pred,ms){for(let i=0;i<(ms||3000)/50;i++){const p=POPS.find(pred);if(p)return p;await wait(50);}return null;}
const DEPTHRX=/(^|[^0-9])[0-9]+단( —|$)/;
function badgesOf(root){return [...root.querySelectorAll('.badge,span,div')].filter(e=>!e.children.length&&DEPTHRX.test(txt(e))).map(txt);}
function popInfo(p){const ph=p.querySelector(':scope > .ph');const pt=ph&&ph.querySelector('.pt');const pall=ph?[...ph.querySelectorAll(':scope > button.pall')]:[];
  const xb=ph?ph.querySelector(':scope > button:not(.pall)'):null;
  return {pk:p._pk||null,cls:p.className,title:txt(pt),rect:R(p),z:+p.style.zIndex||0,sized:p.classList.contains('sized'),
    pall:pall.length,pallTxt:pall.map(txt),pallR:pall.length?R(pall[0]):null,xR:R(xb),xTxt:txt(xb),phH:ph?+ph.getBoundingClientRect().height.toFixed(2):null,
    memobtn:p.querySelectorAll(':scope > .pb > .memobtn').length,memoTxt:[...p.querySelectorAll(':scope > .pb > .memobtn')].map(txt),
    cdim:[...p.querySelectorAll(':scope > .pb > .cdim')].map(txt),badges:badgesOf(p),
    style:{w:p.style.width,h:p.style.height,mh:p.style.maxHeight,l:p.style.left,t:p.style.top}};}
/* 줄 한 곳의 단어 가운데 — 길게 누르기 자리 */
/* 줄 글자는 글자마다 따로 된 텍스트 노드다(평문 좌표계) — 줄 전체를 이어 붙여 단어를 찾고, 그 가운데 글자의 노드로 자리를 잰다 */
async function wordIn(ln,minLen){if(!ln)return null;ln.scrollIntoView({block:'center'});await wait(220);
  const w=document.createTreeWalker(ln,NodeFilter.SHOW_TEXT);let n,acc='';const nodes=[];
  while((n=w.nextNode())){const pe=n.parentElement;const bad=!pe||!!pe.closest('.htog,.stkchip,.pitwho,sup.fn,.embed,.embx,.lbl,.badge,.chip,.mdtab,.mdhash,.mdmark,.blockid,.vimg');
    nodes.push([n,acc.length,bad]);acc+=bad?'\u0000'.repeat((n.nodeValue||'').length):(n.nodeValue||'');}
  const rx=/[가-힣A-Za-z0-9]{2,}/g;let m;
  while((m=rx.exec(acc))){if(m[0].length<(minLen||2))continue;const mid=m.index+Math.floor(m[0].length/2);
    const hit=nodes.find(([nn,a])=>mid>=a&&mid<a+(nn.nodeValue||'').length);if(!hit)continue;
    const r=document.createRange();r.setStart(hit[0],mid-hit[1]);r.setEnd(hit[0],mid-hit[1]+1);const b=r.getBoundingClientRect();
    if(!b.width)continue;const cx=b.left+b.width/2,cy=b.top+b.height/2;const at=document.elementFromPoint(cx,cy);
    if(at&&(at===ln||ln.contains(at)))return {cx:+cx.toFixed(2),cy:+cy.toFixed(2),on:true,word:m[0]};}
  return null;}
function offenders(){const cw=document.documentElement.clientWidth;const out=[];
  document.querySelectorAll('body *').forEach(e=>{if(e.closest('.pop,.pitmenu,#toasts,#sk'))return;const cst=getComputedStyle(e);if(cst.position==='fixed'||cst.display==='none')return;
    const r=e.getBoundingClientRect();if(r.width&&r.right>cw+0.5){const par=e.parentElement;const pr=par?par.getBoundingClientRect():null;
      if(!pr||pr.right<=cw+0.5)out.push({tag:e.tagName.toLowerCase(),id:e.id||'',cls:String(e.className||'').slice(0,40),x:+r.left.toFixed(1),r:+r.right.toFixed(1),w:+r.width.toFixed(1)});}});
  return out.slice(0,8);}

window.__HM={
  wait,
  errs(){return (window.__ERR||[]).slice();},
  spy(){return {closeAll:SPY.closeAll,toasts:SPY.toasts.slice()};},
  spyReset(){SPY.closeAll=0;SPY.toasts=[];return true;},
  clean(){clean();return POPS.length;},
  has(){return {vvBox:typeof vvBox==='function',popAllSync:typeof popAllSync==='function',mokCount:typeof mokCount==='function',drawerPlace:typeof drawerPlace==='function'};},
  async go(law,tab,o){clean();await idle();S.law=law;S.tab=tab;
    if(tab==='cha2'){S.boardKind='기출';S.series='';S.yearFilter='';S.cha2Sel=null;S.cha2Filter={};}
    if(tab==='prec'){S.precQ='';S.precFilter={};}
    Object.assign(S,o||{});await render();await idle();await wait(450);return {tab:S.tab,law:S.law};},
  state(){const t=topPop();return {tab:S.tab,law:S.law,pops:POPS.length,top:t?t._pk:null,treeHid:!!S.treeHid,listHid:!!S.listHid};},
  pops(){return POPS.map(popInfo);},
  popInfo(pk){const p=pk?popBy(pk):lastPop();return p?popInfo(p):null;},
  topInfo(){const p=topPop();return p?popInfo(p):null;},
  async popHead(pk){const p=pk?popBy(pk):lastPop();if(!p)return null;const t=p.querySelector('.ph .pt')||p.querySelector('.ph');return hitOn(t);},
  /* 머리에서 화면 안에 보이고 단추가 아닌 자리(끝까지 밀린 팝업을 다시 잡을 곳) — 왼쪽부터 4px 씩 */
  headFree(pk){const p=pk?popBy(pk):lastPop();if(!p)return null;const ph=p.querySelector(':scope > .ph');if(!ph)return null;const r=ph.getBoundingClientRect();const V=vv();
    const y=r.top+r.height/2;if(y<=V.y||y>=V.y+V.h)return {on:false,why:'머리가 화면 위아래 밖',r:R(ph)};
    for(let x=Math.max(r.left,V.x)+3;x<Math.min(r.right,V.x+V.w)-2;x+=4){const at=document.elementFromPoint(x,y);if(at&&ph.contains(at)&&!at.closest('button'))return {cx:+x.toFixed(2),cy:+y.toFixed(2),on:true,at:String(at.className||at.tagName).slice(0,30)};}
    return {on:false,why:'보이는 빈 자리 없음',r:R(ph)};},
  async popBodyAt(pk){const p=pk?popBy(pk):null;if(!p)return null;const b=p.querySelector(':scope > .pb');if(!b)return null;const r=b.getBoundingClientRect();
    /* 몸통 안에서 아무 글자도 누르지 않을 자리(왼쪽 위 안쪽 4px) */
    const x=r.left+4,y=r.top+4;const at=document.elementFromPoint(x,y);return {cx:+x.toFixed(2),cy:+y.toFixed(2),on:!!at&&p.contains(at)&&!at.closest('button,.chip,.res,.mkr,a,.plink,.joLink,.embed'),at:at?String(at.className||at.tagName).slice(0,40):null};},
  async pallAt(){const p=topPop();if(!p)return null;const b=p.querySelector(':scope > .ph > button.pall');return b?hitOn(b):null;},
  /* ── A 가로 탭 ── */
  rail(){const r=document.getElementById('hrail');if(!r)return null;
    const tabs=[...r.children].map(b=>{const n=b.querySelector('b[data-n]');const lab=(b.firstChild&&b.firstChild.nodeType===3?b.firstChild.nodeValue:txt(b)).trim();
      return {id:b.id||'',k:n?n.dataset.n:'',label:lab,n:txt(n),on:b.classList.contains('on'),dis:!!b.disabled,cls:b.className,tag:b.tagName.toLowerCase()};});
    const all=document.querySelectorAll('#mokBtn');
    return {tabs,mokAll:all.length,mokInRail:!!r.querySelector('#mokBtn'),mokInSlot:!!document.querySelector('#slot #mokBtn'),
      mokCls:all.length?all[0].className:null,mokTag:all.length?all[0].tagName.toLowerCase():null,mokTitle:all.length?all[0].title:null,
      hrail:{sw:r.scrollWidth,cw:r.clientWidth,ox:cs(r,'overflowX'),rect:R(r)}};},
  async mokAt(){return scrollHit(document.getElementById('mokBtn'));},
  /* G-5 — 탭 줄을 끝까지 민 뒤 오른쪽 탭을 **스크롤 없이** 그 자리에서 누른다(scrollIntoView 를 쓰면 앱이 지키는지 못 잰다) */
  railScrollEnd(){const r=document.getElementById('hrail');if(!r)return null;r.scrollLeft=r.scrollWidth;return {sl:r.scrollLeft,max:r.scrollWidth-r.clientWidth};},
  railTabAt(k){const n=document.querySelector('#hrail b[data-n="'+k+'"]');return n?hitOn(n.parentElement):null;},
  railState(){const r=document.getElementById('hrail');const on=r&&r.querySelector('.rb.on');return {sl:r?r.scrollLeft:null,on:on?hitOn(on):null,onTxt:txt(on),tab:S.tab};},
  mokRect(){return R(document.getElementById('mokBtn'));},
  mokList(){const p=POPS.find(x=>(x._pk||'').indexOf('moknote|')===0);if(!p)return null;
    return Object.assign(popInfo(p),{n:p.querySelectorAll('.mklist .mkr').length});},
  async mokRowAt(note){const p=POPS.find(x=>(x._pk||'').indexOf('moknote|')===0);if(!p)return null;
    const r=[...p.querySelectorAll('.mklist .mkr')].find(x=>x.dataset.note===note)||p.querySelector('.mklist .mkr');if(!r)return null;
    r.scrollIntoView({block:'center'});await wait(220);const h=hitOn(r.querySelector('.nm')||r);if(h)h.note=r.dataset.note;return h;},
  /* BASE 헛잣대 — 2차 보드 알약 「목차노트 N」 으로 연다(바탕엔 탭이 없다) */
  async mokOpenAny(){const b=document.getElementById('mokBtn');if(!b)return false;b.click();await wait(900);return !!POPS.find(x=>(x._pk||'').indexOf('moknote|')===0);},
  noteInfo(name){const p=POPS.find(x=>(x._pk||'')==='note|'+PLAW()+'|'+name+'|');if(!p)return null;
    return Object.assign(popInfo(p),{rows:p.querySelectorAll('.ntrow').length,chips:p.querySelectorAll('.ntbl .chip').length,chipKinds:[...p.querySelectorAll('.ntbl .chip')].slice(0,200).map(c=>txt(c).split(' ')[0])});},
  async noteWait(name){const p=await popWait(x=>(x._pk||'')==='note|'+PLAW()+'|'+name+'|',5000);return !!p;},
  /* ── D 깊이 사슬 · 자리 확인 ── */
  async chipAtTop(sel,pat){const p=topPop();if(!p)return null;const c=[...p.querySelectorAll(sel)].find(x=>!pat||new RegExp(pat).test(txt(x)));if(!c)return null;return scrollHit(c);},
  async linkAtTop(){const p=topPop();if(!p)return null;
    const c=p.querySelector('.plink:not(.dead)')||p.querySelector('.embed.live')||p.querySelector('.embx .emtools span')||p.querySelector('.joLink:not(.dead)')||p.querySelector('.ntbl .chip.c-prec')||p.querySelector(':scope > .pb .res:not(.plout)');
    if(!c)return null;const h=await scrollHit(c);if(h)h.kind=c.className.split(' ').slice(0,2).join('.');return h;},
  depthBadges(){return POPS.map(p=>({pk:p._pk,b:badgesOf(p)})).filter(x=>x.b.length);},
  /* D 표 자리 하나 — 바탕 깊이(d)로 팝업을 직접 연 뒤, 그 안의 대상을 **눌러** 새 팝업이 한 겹 더 뜨는지.
     kind: 2084(<사건번호> 줄 — 데이터에 0건이라 지은 줄) · 2094(조문 링크) · 6230(⤷ 임베드) · 6240(⤢) · 6306(노트 줄 칩) · 6358·6363·6365(목록 행) · 6935(카드 목록 행) · 7001(판례 창 행) */
  async probe(site,a){clean();await idle();S.tab=a.tab||'cha2';S.law=a.law||'특허법';await render();await idle();await wait(300);
    const tab0=S.tab;let host=null,target=null,note='';
    try{
      if(site==='2084'){const body=popShell('cell','하네스 — <사건번호> 줄(지은 줄)','h|2084');showPop(null);
        const t='하네스 줄 <'+a.id+'> 끝';const i=t.indexOf('<'),j=t.indexOf('>')+1;
        const row={t:t,e:[{k:'P',a:i,b:j,j:a.id}]};const d=el('div','ln');d.appendChild(renderLine(row,{label:false,depth:a.d}));body.appendChild(d);
        host=body.parentNode;target=host.querySelector('.plink:not(.dead)');}
      else if(site==='2094'){await popJo(a.law||'특허법',a.jo,null,a.d);await wait(600);host=popBy('jo|'+(a.law||'특허법')+'|'+a.jo);target=host&&host.querySelector('.joLink:not(.dead)');}
      else if(site==='6230'){/* ⤷ 칩은 임베드 상자로 바뀌고(chip.replaceWith) 칩이 남는 곳은 상자 안 줄(inline:false)뿐인데 데이터에 중첩 임베드가 0 — 상자 안 줄을 지어 부른다 */
        const body=popShell('cell','하네스 — 상자 안 ⤷ 임베드 줄(지은 줄)','h|6230');showPop(null);
        const row={t:'하네스 임베드 줄',e:[{k:'E',a:0,b:0,to:a.to}]};const d=el('div','ln');d.appendChild(renderLine(row,{label:false,depth:a.d,inline:false}));body.appendChild(d);
        host=body.parentNode;target=host.querySelector('.embed.live');}
      else if(site==='6240'){await popNote(a.name,null,null,a.d);await wait(900);host=POPS.find(x=>(x._pk||'')==='note|'+PLAW()+'|'+a.name+'|');
        target=host&&host.querySelector('.embx .emtools span');}
      else if(site==='6306'){await popNote(a.name,null,null,a.d);await wait(700);host=POPS.find(x=>(x._pk||'')==='note|'+PLAW()+'|'+a.name+'|');
        target=host&&[...host.querySelectorAll('.ntbl .chip.c-prec')].find(c=>/^(판례|사례|기출|GS|노트) /.test(txt(c)));}
      else if(site==='6358'||site==='6363'||site==='6365'){await popNoteList(a.label,'하네스',a.items,null,a.d);await wait(700);host=lastPop();target=host&&host.querySelector(':scope > .pb .res');}
      else if(site==='6935'){const P=await get(PF('리스트'));const CC=await get(CHF(a.kind)).catch(()=>null);let p=null;
        for(const q of (P.판례||[])){try{if(c2ItemsFor(q,a.kind,null,CC).length>=1){p=q;break;}}catch(e){}}
        if(!p)return {site,miss:'카드를 이은 판례 없음'};note=p.id;
        await popCardList(p,a.kind,null,{__list:true,clientX:420,clientY:220},a.d);await wait(700);host=lastPop();target=host&&host.querySelector('.res.lkrow:not(.plout)');}
      else if(site==='7001'){const P=await get(PF('리스트'));const CI=await get(PF('인용')).catch(()=>null);if(!CI)return {site,miss:'인용 json 없음'};
        const ids=new Set((P.판례||[]).map(x=>x.id));const id=Object.keys(CI).find(k=>ids.has(k)&&((CI[k]||{}).인용||[]).some(x=>ids.has(x)));if(!id)return {site,miss:'인용 표본 없음'};
        const cur=(P.판례||[]).find(x=>x.id===id);precLinkWin('in',cur,CI[id],P,null,a.d);await wait(600);host=lastPop();target=host&&host.querySelector('.plwl .res:not(.plout)');note=id;}
    }catch(e){return {site,exc:String(e&&e.message||e).slice(0,200)};}
    if(!host||!target)return {site,miss:(host?'대상 없음':'팝업 없음'),pops:POPS.length};
    const before=POPS.length;SPY.closeAll=0;SPY.toasts=[];
    const h=await scrollHit(target);
    return {site,host:host._pk,target:String(target.className||'').slice(0,40)+' | '+txt(target).slice(0,30),hit:h,before,tab0,note};},
  async probeAfter(){await wait(900);await idle();return {pops:POPS.length,tab:S.tab,closeAll:SPY.closeAll,toasts:SPY.toasts.slice(),top:(topPop()||{})._pk||null,
    badges:POPS.map(p=>badgesOf(p)).flat()};},
  /* ── E 모두 닫기 ── */
  async openTwo(){clean();await idle();await popJo('특허법','제129조',{clientX:300,clientY:180},1);await wait(500);
    await popNote(a_N96(),null,{clientX:520,clientY:260},1);await wait(700);return POPS.map(popInfo);},
  pallAll(){return [...document.querySelectorAll('.pop .ph > button.pall')].map(b=>({pk:b.closest('.pop')._pk,txt:txt(b),hit:hitOn(b)}));},
  esc(){document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));window.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));return POPS.length;},
  /* ── F 길게 누르기 ── */
  async lineAt(where,a){let ln=null;
    if(where==='jo')ln=[...document.querySelectorAll('#slot .main .ln')].find(l=>l._pit&&/[가-힣]{2,}/.test(l.textContent));
    else if(where==='prec')ln=[...document.querySelectorAll('#slot .main .ln')].find(l=>l._pit&&/[가-힣]{2,}/.test(l.textContent));
    else if(where==='card'){const p=POPS.find(x=>(x._pk||'').indexOf('🧾 ')>=0)||lastPop();ln=p&&[...p.querySelectorAll('.ln')].find(l=>l._pit&&/[가-힣]{2,}/.test(l.textContent)&&!l.closest('.embx'));}
    else if(where==='note'){const p=lastPop();ln=p&&[...p.querySelectorAll('.ntrow > .ln')].find(l=>l._pit&&/[가-힣]{3,}/.test(l.textContent));}
    if(!ln)return null;const w=await wordIn(ln,2);if(w)w.line=txt(ln).slice(0,40);return w;},
  menu(){const m=document.querySelector('.pitmenu');return m?[...m.querySelectorAll('.mi')].map(txt):null;},
  menuClear(){document.querySelectorAll('.pitmenu').forEach(x=>x.remove());try{getSelection().removeAllRanges();}catch(e){}return true;},
  selLen(){const s=getSelection();return s?String(s).length:0;},
  /* ── G 폰 ── */
  vv(){const d=document.documentElement;return {iw:innerWidth,ih:innerHeight,vv:vv(),sw:d.scrollWidth,cw:d.clientWidth,bsw:document.body.scrollWidth,dpr:devicePixelRatio,phone:matchMedia('(max-width:640px)').matches};},
  offenders,
  popsInVV(){const V=vv();return POPS.map(p=>{const r=R(p);return {pk:p._pk,r,inside:r.x>=V.x-0.5&&r.y>=V.y-0.5&&r.r<=V.x+V.w+0.5&&r.b<=V.y+V.h+0.5};});},
  drawer(){const s=document.getElementById('slot');if(!s)return null;
    const one=sel=>{const d=s.querySelector(':scope > '+sel);if(!d)return null;return {hid:d.classList.contains('hid'),pos:cs(d,'position'),rect:R(d),shadow:cs(d,'boxShadow'),z:cs(d,'zIndex'),left:d.style.left||''};};
    return {tree:one('.tree'),plist:one('.plist'),handles:[...s.querySelectorAll(':scope > .handle')].map(h=>({t:txt(h),rect:R(h)})),main:R(s.querySelector(':scope > .main')),slot:R(s)};},
  async handleAt(i){const s=document.getElementById('slot');const h=s&&s.querySelectorAll(':scope > .handle')[i];return h?scrollHit(h):null;},
  async mainAt(){const s=document.getElementById('slot');const m=s&&s.querySelector(':scope > .main');if(!m)return null;const r=m.getBoundingClientRect();
    const x=r.right-12,y=r.top+Math.min(40,r.height/2);const at=document.elementFromPoint(x,y);return {cx:+x.toFixed(2),cy:+y.toFixed(2),on:!!at&&m.contains(at),at:at?String(at.className||at.tagName).slice(0,30):null};},
  setCfg(kind,c){S.popCfg=S.popCfg||{};if(c==null)delete S.popCfg[kind];else S.popCfg[kind]=c;return true;},
  getCfg(kind){const c=(S.popCfg||{})[kind];return c?JSON.parse(JSON.stringify(c)):null;},
  uiRaw(){try{return JSON.parse(localStorage.getItem('jopangi_ui')||'{}');}catch(e){return {};}},
  async openKinds(){clean();await idle();const out=[];const E={clientX:200,clientY:300};
    const run=async(nm,f)=>{try{clean();await f();await wait(700);const p=lastPop();out.push({nm,info:p?popInfo(p):null,vv:vv()});}catch(e){out.push({nm,exc:String(e&&e.message||e).slice(0,160)});}};
    await run('jo',()=>popJo('특허법','제129조',E,1));
    await run('note',()=>popNote(a_N96(),null,E,1));
    await run('card',()=>popCard4('기출','특기출 25-62-1',E,1));
    await run('prec',()=>popPrec4('2021후10374',E,1));
    await run('list',()=>popNoteList('판례','하네스',['2021후10374'],E,1));
    return out;},
  /* PC 무변 — 한 팝업의 자리·크기·DOM(글자 · 클래스) */
  async pcOne(nm){clean();await idle();const E={clientX:640,clientY:260};
    if(nm==='jo')await popJo('특허법','제129조',E,1);else if(nm==='note')await popNote(a_N96(),null,E,1);else if(nm==='prec')await popPrec4('2021후10374',E,1);else if(nm==='card')await popCard4('기출','특기출 25-62-1',E,1);
    await wait(900);const p=lastPop();if(!p)return null;const c=p.cloneNode(true);
    c.querySelectorAll(':scope > .pb > .memobtn').forEach(x=>{if(/이 노트가 인용/.test(txt(x)))x.remove();});
    return {rect:R(p),z:null,cls:p.className,style:{w:p.style.width,h:p.style.height,mh:p.style.maxHeight,l:p.style.left,t:p.style.top},text:c.textContent.replace(/\s+/g,' ').slice(0,4000),n:c.querySelectorAll('*').length,
      html:c.innerHTML.replace(/ style="[^"]*"/g,'').length};},
  layout(){const q=s=>R(document.querySelector(s));return {top:q('header.topbar'),hs:q('#hsrow'),slot:q('#slot'),main:q('#slot > .main'),tree:q('#slot > .tree'),plist:q('#slot > .plist'),badges:q('#hbadges'),hrail:q('#hrail'),laws:q('#laws')};}
};
const a_N96=()=>'9.6.{결}정정심판(136)_특무내정정청구(133-2)';
})();
