/* _harness_jo_ms_claude_tests.js — _task_jo_ms_claude_editq 하네스가 페이지에 넣는 도구(__HC).
   BASE(509c10b)·NEW 둘 다에 같은 것을 넣는다 — 없는 것(clMsUid · 「Claude」 범위 …)은 빈 값으로 돌려준다.
   재는 것 = DOM 실물·elementFromPoint/elementsFromPoint(쌓임 순서)·계산 스타일·앱 상태(S · POPS · SKON · CL_*). 픽셀은 안 찍는다. */
(function(){
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const txt=e=>e?(e.textContent||'').replace(/\s+/g,' ').trim():'';
const R=e=>{if(!e)return null;const r=e.getBoundingClientRect();
  return {x:+r.left.toFixed(2),y:+r.top.toFixed(2),w:+r.width.toFixed(2),h:+r.height.toFixed(2),r:+r.right.toFixed(2),b:+r.bottom.toFixed(2),cx:+(r.left+r.width/2).toFixed(2),cy:+(r.top+r.height/2).toFixed(2)};};
const cs=(e,p)=>e?getComputedStyle(e)[p]:null;
const idle=async()=>{for(let i=0;i<320;i++){if(!busy)return true;await wait(25);}return false;};
function clean(){try{closeAllPops();}catch(e){}document.querySelectorAll('.pitmenu').forEach(x=>x.remove());}
function hitOn(t){const r=R(t);if(!r)return null;const onScreen=r.cy>0&&r.cy<innerHeight&&r.cx>0&&r.cx<innerWidth;
  const at=onScreen?document.elementFromPoint(r.cx,r.cy):null;
  return Object.assign(r,{on:!!at&&(at===t||t.contains(at))&&onScreen,at:at?(String(at.className||at.tagName).slice(0,40)):null,onScreen});}
async function scrollHit(t){if(!t)return null;try{t.scrollIntoView({block:'center',inline:'nearest'});}catch(e){}await wait(200);return hitOn(t);}
const popBy=pk=>POPS.find(x=>x._pk===pk)||null;
const popLike=s=>POPS.find(x=>(x._pk||'').indexOf(s)>=0)||null;
const lastPop=()=>POPS[POPS.length-1]||null;
async function popWait(pred,ms){for(let i=0;i<(ms||4000)/50;i++){const p=POPS.find(pred);if(p)return p;await wait(50);}return null;}
function popInfo(p){if(!p)return null;const ph=p.querySelector(':scope > .ph');return {pk:p._pk,title:txt(ph&&ph.querySelector('.pt')),rect:R(p),z:+p.style.zIndex||0,phZ:cs(ph,'zIndex')};}
async function msKey(code){const C=await get('2cha_본문_기출_민소.json');return Object.keys(C).find(k=>k===code||k.indexOf(code+'-')===0)||null;}
/* A — 머리 가운데(와 1/4·3/4) 점에서 맨 위 요소가 머리 안인가 · 높이 h · scrollTop st 에서 한 번 + 스크롤 전 구간 10px 마다 훑기 */
function headProbe(p){const ph=p.querySelector(':scope > .ph');const r=ph.getBoundingClientRect();const y=r.top+r.height/2;
  const out=[];[0.25,0.5,0.75].forEach(f=>{const x=r.left+r.width*f;const at=document.elementFromPoint(x,y);
    const st=document.elementsFromPoint(x,y);const ih=st.findIndex(e=>e===ph||ph.contains(e));
    out.push({f,at:at?String(at.className||at.tagName).slice(0,40):null,inHead:!!at&&(at===ph||ph.contains(at)),above:ih>0?st.slice(0,ih).map(e=>String(e.className||e.tagName).slice(0,30)):[]});});
  return out;}
window.__HC={
  wait,
  errs(){return (window.__ERR||[]).slice();},
  clean(){clean();return POPS.length;},
  has(){return {clMsUid:typeof clMsUid==='function',clTabBtn:typeof clTabBtn==='function',clWho:typeof clWho==='function',skonClaude:('claude' in SKON),skonLogic:('logic' in SKON)};},
  state(){return {tab:S.tab,law:S.law,pops:POPS.length,cl:CL_STATE,skOpen:getComputedStyle(document.getElementById('sk')).display!=='none'};},
  async go(law,tab,o){clean();await idle();S.law=law;S.tab=tab;
    if(tab==='cha2'){S.boardKind='기출';S.series='';S.yearFilter='';S.cha2Sel=null;S.cha2Filter={};S.c2ord='round';}
    Object.assign(S,o||{});await render();await idle();await wait(450);return {tab:S.tab,law:S.law};},
  async clReady(ms){for(let i=0;i<(ms||8000)/100;i++){if(CL_STATE!=='wait')return CL_STATE;await wait(100);}return CL_STATE;},
  pops(){return POPS.map(popInfo);},
  /* ── A ── */
  async openA(kind,a){clean();await idle();
    if(kind==='callout'){S.law='민사소송법';S.tab='cha2';S.boardKind='기출';await render();await idle();const k=await msKey(a.code);if(!k)return {miss:'카드 열쇠 없음'};
      await popCard4('기출',k,{clientX:300,clientY:120},1);await wait(700);const cp=popLike('🧾 기출 · '+a.code);if(!cp)return {miss:'카드 팝업 없음'};
      const co=[...cp.querySelectorAll('.callout')].find(x=>txt(x.querySelector('.ct')).indexOf(a.ct)===0);if(!co)return {miss:'콜아웃 없음 '+a.ct,cos:[...cp.querySelectorAll('.callout .ct')].map(txt)};
      co.click();await wait(600);const p=lastPop();return {pk:p&&p._pk,card:cp._pk};}
    if(kind==='jimun'){S.law='특허법';S.tab='jimun';S.jimunTab='ox';S.mok='';S.oxQueue='';await render();await idle();   /* 1차객 지문 풀(OXPOOL)이 찬 뒤에 연다 — claude_answers 하네스 home() 과 같은 길 */
      for(let i=0;i<200&&!(OXPOOL&&Object.keys(OXPOOL).length>1000);i++)await wait(100);
      popCard(a.uid,{clientX:300,clientY:120});await wait(900);return {pk:(lastPop()||{})._pk};}
    if(kind==='note'){await popNote(a.name,null,{clientX:300,clientY:120},1);await wait(900);return {pk:(lastPop()||{})._pk};}
    if(kind==='prec'){S.law='특허법';await popPrec4(a.id,{clientX:300,clientY:120},1);await wait(1200);return {pk:(lastPop()||{})._pk};}
    if(kind==='claude'){S.law='특허법';clOpen(a.uid,{clientX:300,clientY:120});await wait(700);return {pk:(lastPop()||{})._pk};}
    return {miss:'kind'};},
  async headCheck(pk,h,st){const p=popBy(pk);if(!p)return null;p.classList.add('sized');p.style.height=h+'px';p.style.maxHeight=h+'px';await wait(60);
    const range=Math.max(0,p.scrollHeight-p.clientHeight);p.scrollTop=Math.min(st,range);await wait(80);
    const one=headProbe(p);const scan=[];let bad=0;
    for(let s=0;s<=range;s+=10){p.scrollTop=s;const pr=headProbe(p);const b=pr.filter(x=>!x.inHead);if(b.length){bad++;if(scan.length<4)scan.push({s,b:b.map(x=>({f:x.f,at:x.at,above:x.above}))});}}
    p.scrollTop=Math.min(st,range);
    return {pk,range,st:p.scrollTop,one,oneOk:one.every(x=>x.inHead),scanN:Math.floor(range/10)+1,bad,scan,phZ:cs(p.querySelector(':scope > .ph'),'zIndex')};},
  /* ── B ── */
  calloutInfo(pk){const p=popBy(pk)||lastPop();if(!p)return null;return {cdim:[...p.querySelectorAll(':scope > .pb > .cdim')].map(txt),htog:p.querySelectorAll('.htog').length,lns:p.querySelectorAll('.ln').length};},
  async htogClick(pk){const p=popBy(pk)||lastPop();const h=p&&p.querySelector('.htog');if(!h)return null;const hid=()=>[...p.querySelectorAll('.ln')].filter(l=>l.offsetParent===null).length;const hidden0=hid();
    h.click();await wait(250);const hidden1=hid();h.click();await wait(250);return {hidden0,hidden1,hidden2:hid(),changed:hidden0!==hidden1};},
  /* B — 제목 줄(h)이 있는 민소 기출 문제 콜아웃을 데이터에서 고른다(접기 ˅ 가 있는 것) */
  async pickCallout(){const C=await get('2cha_본문_기출_민소.json');for(const k of Object.keys(C).sort()){const rec=C[k];if(!rec||!rec.행)continue;
    for(const r of rec.행){if(r&&r.co&&(r.rows||[]).some(x=>x&&x.h)){const m=/^민기출 \d\d-\d\d-\d/.exec(k);if(m)return {code:m[0],ct:r.t,co:r.co};}}}return null;},   /* 제목 줄 있는 콜아웃은 📄(note) 갈래뿐(민소 기출 16개 실측) — 같은 popCallout 으로 뜬다 */
  async lineAt(pk){const p=popBy(pk)||lastPop();if(!p)return null;const ln=[...p.querySelectorAll('.ln')].find(l=>l._pit&&/[가-힣]{2,}/.test(l.textContent));if(!ln)return null;
    ln.scrollIntoView({block:'center'});await wait(200);const w=document.createTreeWalker(ln,NodeFilter.SHOW_TEXT);let n,acc='';const nodes=[];
    while((n=w.nextNode())){nodes.push([n,acc.length]);acc+=n.nodeValue;}const m=/[가-힣]{2,}/.exec(acc);if(!m)return null;const mid=m.index+1;
    const hit=nodes.find(([nn,a])=>mid>=a&&mid<a+nn.nodeValue.length);const rg=document.createRange();rg.setStart(hit[0],mid-hit[1]);rg.setEnd(hit[0],mid-hit[1]+1);const b=rg.getBoundingClientRect();
    return {cx:+(b.left+b.width/2).toFixed(2),cy:+(b.top+b.height/2).toFixed(2),on:true};},
  menu(){const m=document.querySelector('.pitmenu');return m?[...m.querySelectorAll('.mi')].map(txt):null;},
  bar(){const b=document.querySelector('#c2mark:not([hidden])');return b?[...b.querySelectorAll('.mk9r2 button')].filter(x=>!x.hidden).map(txt):null;},   /* A-6(a) 9/30 — joscreen0929 A-5: 2차 문제 창 칠 막대 둘째 줄 */
  /* ── C ── */
  boardRows(){return [...document.querySelectorAll('#slot .cell.c2row[data-ck]')].map(r=>{const vis=[...r.querySelectorAll('[data-clbtn]')].filter(b=>!b.hidden);
    return {code:txt(r.querySelector('.c2code')),btn:vis.map(b=>({t:txt(b),cls:b.className,fw:cs(b,'fontWeight'),color:cs(b,'color'),fs:cs(b,'fontSize')})),ph:r.querySelectorAll('[data-clbtn][hidden]').length,
      afterScore:(()=>{const s=r.querySelector('.c-score');const b=vis[0];return !!(s&&b&&s.nextElementSibling===b);})()};});},
  async rowBtnAt(code){const r=[...document.querySelectorAll('#slot .cell.c2row[data-ck]')].find(x=>txt(x.querySelector('.c2code'))===code);if(!r)return null;const b=[...r.querySelectorAll('[data-clbtn]')].find(x=>!x.hidden);return b?scrollHit(b):{none:true};},
  async rowAt(code){const r=[...document.querySelectorAll('#slot .cell.c2row[data-ck]')].find(x=>txt(x.querySelector('.c2code'))===code);if(!r)return null;const t=r.querySelector('.c2t2')||r;return scrollHit(t);},
  cardTabs(code){const p=popLike('🧾 기출 · '+code);if(!p)return null;const tabs=p.querySelector('.gtabs');return {pk:p._pk,tabs:[...tabs.children].map(b=>({t:txt(b),cls:b.className,on:b.classList.contains('on'),color:cs(b,'color'),bc:cs(b,'borderTopColor'),bw:cs(b,'borderTopWidth'),fw:cs(b,'fontWeight')}))};},   /* A-6(a) 9/30 — c2card B-2: Claude 탭 테두리 0 을 잰다 */
  async cardTabAt(code){const p=popLike('🧾 기출 · '+code);const b=p&&p.querySelector('.gtabs .cltab');return b?scrollHit(b):null;},
  async openCard(code){const k=await msKey(code);if(!k)return null;await popCard4('기출',k,{clientX:260,clientY:120},1);await wait(700);const p=popLike('🧾 기출 · '+code);return p?popInfo(p):null;},
  clWin(uid){const p=popBy('claude|'+uid);if(!p)return null;const w=p.querySelector('[data-clwin]');
    return {pk:p._pk,title:txt(p.querySelector('.ph .pt')),answers:[...p.querySelectorAll('[data-clans]')].map(x=>x.dataset.clans),head:[...p.querySelectorAll('.clhd')].map(h=>[txt(h.querySelector('.clno')),txt(h.querySelector('.cldt')),txt(h.querySelector('button.uid'))]),
      uids:[...p.querySelectorAll('button.uid[data-sid]')].map(b=>b.dataset.sid),note:[...p.querySelectorAll('.clnote')].map(txt),rect:R(p),depth:w&&w.dataset.cldepth};},
  async clUidAt(uid,sid,which){const p=popBy('claude|'+uid);if(!p)return null;const bs=[...p.querySelectorAll('button.uid[data-sid]')].filter(b=>b.dataset.sid===sid);const b=which==='head'?bs.find(x=>x.closest('.clhd')):bs.find(x=>!x.closest('.clhd'));return b?scrollHit(b):null;},
  async clFix(uid,m,word){const p=popBy('claude|'+uid);if(!p)return null;const box=p.querySelector('[data-clans="'+m+'"]');const fx=[...box.querySelectorAll('.clfixbar button')].find(b=>/정정/.test(b.textContent));if(!fx)return {none:true};fx.click();await wait(200);
    const ta=box.querySelector('[data-clfixta]');ta.value=ta.value+'\n'+word;const sv=[...box.querySelectorAll('.clfixbar button')].find(b=>/저장/.test(b.textContent));sv.click();await wait(300);
    let o={};try{o=JSON.parse(localStorage.getItem('jopangi.clfix')||'{}');}catch(e){}return {fix:o[m]?{done:o[m].done,hasWord:String(o[m].md||'').indexOf(word)>=0,ts:typeof o[m].ts}:null};},
  rx(list){return list.map(s=>{CL_RX.lastIndex=0;return (String(s).match(CL_RX)||[]).join('|');});},
  /* ── D ── */
  scopes(){return [...document.querySelectorAll('#skscope .scope')].map(b=>({s:b.getAttribute('data-s'),t:txt(b),on:b.classList.contains('on'),before:getComputedStyle(b,'::before').content}));},
  skonNow(){return JSON.parse(JSON.stringify(SKON));},
  async search(q,scopes,laws){try{openSk();}catch(e){}await wait(150);Object.keys(SKON).forEach(k=>{SKON[k]=scopes.indexOf(k)>=0;});try{skPaint();}catch(e){}
    Object.keys(SKLAW).forEach(k=>{SKLAW[k]=false;});laws.forEach(l=>{SKLAW[l]=true;});try{skLawPaint();}catch(e){}
    const i=document.getElementById('skin');i.value=q;i.oninput({target:i});await wait(900);
    const box=document.getElementById('skres');return {grp:[...box.querySelectorAll('.grp')].map(txt),rows:[...box.querySelectorAll('.res')].map(r=>({icon:txt(r.querySelector('.skic')),iconColor:cs(r.querySelector('.skic'),'color'),iconFw:cs(r.querySelector('.skic'),'fontWeight'),head:txt(r.querySelector('b')),x:txt(r.querySelector('.x')),tag:txt(r.querySelector('.lawtag'))}))};},
  async searchRowAt(i){const r=document.querySelectorAll('#skres .res')[i||0];return r?hitOn(r):null;},
  skClose(){try{closeSk();}catch(e){}return true;}
};
})();
