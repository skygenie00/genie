/* _harness_jo_gaek_uid_tests.js — _task_jo_gaek_uid(+add1) 하네스가 페이지에 넣는 도구(__HU).
   BASE(genie HEAD a9d72c1)·NEW 둘 다에 같은 것을 넣는다 — 없는 함수(uidSearchKeys · UIDALIAS …)는 빈 값(헛잣대).
   보임 = computed display ≠ none 그리고 높이 > 0 · 자리 = getBoundingClientRect + elementFromPoint.
   ⚠ 누름은 여기서 안 한다 — 자리만 돌려주고 파이썬이 page.mouse · 키보드로 누른다(관문 규칙 1). */
(function(){
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const txt=e=>e?(e.textContent||'').replace(/\s+/g,' ').trim():'';
const R=e=>{if(!e)return null;const r=e.getBoundingClientRect();
  return {x:+r.left.toFixed(2),y:+r.top.toFixed(2),w:+r.width.toFixed(2),h:+r.height.toFixed(2),cx:+(r.left+r.width/2).toFixed(2),cy:+(r.top+r.height/2).toFixed(2)};};
const vis=e=>!!e&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0;
function hitOn(t){if(!t)return null;try{t.scrollIntoView({block:'center',inline:'nearest'});}catch(e){}
  const r=R(t);const at=document.elementFromPoint(r.cx,r.cy);
  const onScreen=r.cy>0&&r.cy<innerHeight&&r.cx>0&&r.cx<innerWidth&&r.w>0&&r.h>0;
  return Object.assign(r,{on:!!at&&(at===t||t.contains(at))&&onScreen,onScreen,vis:vis(t)});}
async function idle(){for(let i=0;i<400&&(typeof busy!=='undefined'&&busy);i++)await wait(25);}
async function until(f,ms){const t0=Date.now();while(Date.now()-t0<(ms||8000)){try{const v=f();if(v)return v;}catch(e){}await wait(40);}try{return f();}catch(e){return null;}}
const pops=()=>(typeof POPS!=='undefined'?POPS:[]);
const has=n=>{try{return typeof eval(n)!=='undefined';}catch(e){return false;}};
const rowOf=k=>{const w=[...document.querySelectorAll('.mbrecw')].find(x=>x.dataset.rk===k);return w?w.parentElement:null;};
/* A17 — Claude 답을 처음 받은 순간의 색인(별칭표 전이었나 · 그때 열쇠) */
const CLW={first:null};
(function poll(){try{if(typeof CL_STATE!=='undefined'&&CL_STATE==='ok'&&!CLW.first)
  CLW.first={by:Object.keys(CL_BY_UID||{}),ment:Object.keys(CL_MENT||{}),alias:has('UIDALIAS')&&!!UIDALIAS};}catch(e){}
  if(!CLW.first)setTimeout(poll,10);})();
window.__HU={
  wait,
  errs(){return (window.__ERR||[]).filter(e=>!/^ResizeObserver loop/.test(e)).slice(0,20);},
  async home(law){try{closeAllPops();}catch(e){}
    S.law=law||'특허법';S.tab='jimun';S.jimunTab='ox';S.mok='';S.oxQueue='';S.oxQ='';S.oxQMode='q';
    await idle();await render();await idle();
    await until(()=>OXPOOL&&Object.keys(OXPOOL).length>300&&typeof MBSR!=='undefined'&&MBSR&&MBSR.box&&MBSR.box.isConnected,30000);
    await wait(150);return {law:S.law,pool:Object.keys(OXPOOL||{}).length};},
  migReady(){return {alias:has('UIDALIAS')&&!!UIDALIAS,last:has('UIDMIG_LAST')?UIDMIG_LAST:null,puts:(window.__REMOTE||{}).puts||0};},
  srInp(){return (typeof MBSR!=='undefined'&&MBSR&&MBSR.inp)?hitOn(MBSR.inp):null;},
  srVal(){return (typeof MBSR!=='undefined'&&MBSR&&MBSR.inp)?MBSR.inp.value:null;},
  srRows(){if(typeof MBSR==='undefined'||!MBSR||!MBSR.box)return [];return [...MBSR.box.querySelectorAll('.rr')].slice(0,5).map(r=>({t:txt(r).slice(0,90),vis:vis(r)}));},
  pop(k){const p=pops().find(x=>x._pk==='q|📝 지문 '+k);if(!p)return {open:false};
    const id=p.querySelector('.qb.id');return {open:true,vis:vis(p),z:+p.style.zIndex,title:txt(p.querySelector('.pt')).slice(0,80),id:txt(id)};},
  pops(){return pops().map(p=>p._pk);},
  goBtn(k){const p=pops().find(x=>x._pk==='q|📝 지문 '+k);if(!p)return null;const b=p.querySelector('.qgo');return b?hitOn(b):null;},
  closeAll(){try{closeAllPops();}catch(e){}return pops().length;},
  /* 카드 안 지문 줄(리담 줄 = .mbrecw[data-rk]) · 제7판 카드 = #qb-<열쇠> */
  row(k){const r=rowOf(k)||document.getElementById('qb-'+k);if(!r)return null;
    const star=[...r.querySelectorAll('.qtag')].find(b=>b.title==='중요');
    const idc=r.querySelector('.qb.id');
    return {vis:vis(r),star:star?{vis:vis(star),on:star.classList.contains('on')}:null,id:txt(idc),t:txt(r).slice(0,120)};},
  starAt(k){const r=rowOf(k)||document.getElementById('qb-'+k);if(!r)return null;const s=[...r.querySelectorAll('.qtag')].find(b=>b.title==='중요');return s?Object.assign(hitOn(s),{on:s.classList.contains('on')}):null;},
  oxAt(k,v){const r=rowOf(k)||document.getElementById('qb-'+k);if(!r)return null;const b=r.querySelector('button.mboxb.'+v);return b?Object.assign(hitOn(b),{sel:b.classList.contains('sel')}):null;},
  rec(k){return (typeof oxAll==='function'?oxAll()[k]:null)||null;},
  /* ⭐ 셈 — 화면 지문(OXPOOL) 가운데 ⭐ 켜진 열쇠 · 저장소의 죽은 옛 열쇠 · 전체 */
  stars(){const P=OXPOOL||{},A=(typeof oxAll==='function'?oxAll():{})||{};
    const on=Object.keys(P).filter(k=>((A[k]||{}).tg||{}).important);
    const allOn=Object.keys(A).filter(k=>((A[k]||{}).tg||{}).important);
    const dead=has('UIDALIAS')&&UIDALIAS?Object.keys(A).filter(k=>Object.prototype.hasOwnProperty.call(UIDALIAS.map||{},k)):[];
    return {pool:on.length,store:allOn.length,dead:dead.length,deadEx:dead.slice(0,5),keys:Object.keys(A).length};},
  starKeys(){const A=(typeof oxAll==='function'?oxAll():{})||{};return Object.keys(A).filter(k=>((A[k]||{}).tg||{}).important).sort();},
  async sync(){try{await syncRecords(true);}catch(e){return 'err '+e;}await idle();return (window.__REMOTE||{}).puts||0;},
  remote(){return (window.__REMOTE||{}).text||null;},
  setRemote(t){window.__REMOTE=window.__REMOTE||{};window.__REMOTE.text=t;window.__REMOTE.sha='H_seed_'+Date.now();return true;},
  /* 기출뷰 — 그 해 카드 */
  async gi(year){S.law='특허법';S.tab='jimun';S.jimunTab='gichul';S.year=String(year);S.mok='';await idle();await render();await idle();await wait(200);
    return [...document.querySelectorAll('[id^="gi-"]')].length;},
  giCard(k){const c=document.getElementById('gi-'+k);
    if(!c){/* ★ mbsame_add3 §A-2(9/27) — 기출뷰 = 민법 exv 틀(문항 .exv-q[data-exq] · 지문 칸 .uzexb .mbqtx) · 옛 #gi- 카드가 없으면 새 틀에서 같은 것을 잰다 */
      const w=document.querySelector('.exv-q[data-exq="'+String(k).replace(/"/g,'\\"')+'"]');if(!w)return null;
      return {vis:vis(w),n:txt(w.querySelector('.exv-no')),rows:[...w.querySelectorAll('.uzexb .mbqtx')].map(x=>txt(x).slice(0,60)),exv:true};}
    return {vis:vis(c),n:txt(c.querySelector('.qb.n')),rows:[...c.querySelectorAll('.gich .gitx')].map(x=>txt(x).slice(0,60))};},
  /* ★ mbsame_add3 §A-2(9/27) — 새 기출뷰는 한 쪽 5 문항 · 그 문번이 든 쪽으로(uzExvGoto 와 같은 셈 · 옛 판은 한 쪽에 다 있어 무동작) */
  async giShow(k){if(document.getElementById('gi-'+k)||typeof uzExvGoto!=='function')return 0;const m=/^[^:]+:(\d{4}):(\d+)$/.exec(String(k));if(!m)return 0;
    const qs=((VJ&&VJ.qs)||[]).filter(q=>String(q.연도)===m[1]).sort((a,b)=>((+giNo(a))-(+giNo(b)))||((+a.문번)-(+b.문번)));const ix=qs.findIndex(q=>String(giNo(q))===m[2]);
    S.exvPg=S.exvPg||{};S.exvPg[PLAW()+':'+m[1]]=ix>=0?Math.floor(ix/5):0;await render();await idle();await wait(200);return ix;},
  /* 마디로 — 열쇠가 든 마디(MBK2M) 번호 */
  nodeOf(k){const m=(typeof MBK2M!=='undefined'&&MBK2M||{})[k];return m?{label:m.label,sel:m.sel}:null;},
  async goNode(sel){S.mok=sel;S.oxPage=null;S.oxQueue='';await idle();await render();await idle();await wait(200);return S.mok;},
  cardText(k){const c=document.getElementById('qb-'+k);return c?{vis:vis(c),t:txt(c)}:null;},
  /* A17 — Claude 답 색인 · 카드 단추 · 창 */
  cl(ks){if(!has('CL_STATE'))return {state:null};const pick=o=>{const r={};(ks||[]).forEach(k=>{if(o&&o[k])r[k]=o[k];});return r;};
    return {state:CL_STATE,alias:has('UIDALIAS')&&!!UIDALIAS,first:CLW.first,by:pick(CL_BY_UID),ment:pick(CL_MENT),gets:window.__CLGETS||0};},
  async clCard(k){try{closeAllPops();}catch(e){}
    const sel='#slot [data-ggu="'+k+'"]';
    if(!document.querySelector(sel)){try{linkGo(k);}catch(e){return {go:'err '+e};}await until(()=>document.querySelector(sel),15000);await idle();await wait(300);}
    const box=document.querySelector(sel);if(!box)return {box:false,mok:S.mok};
    const b=box.parentElement.querySelector(':scope > .mbbot [data-clbtn]');if(!b)return {box:true,btn:null};
    return Object.assign(hitOn(b),{text:txt(b),hidden:b.hidden,color:getComputedStyle(b).color,kids:[...b.children].map(x=>[txt(x),getComputedStyle(x).color])});},
  clWin(k){const p=pops().find(x=>x._pk==='claude|'+k);return p?{vis:vis(p),t:txt(p).slice(0,160)}:{pops:pops().map(x=>x._pk)};},
  dump(){const m=document.querySelector('#slot .main');return m?txt(m):'';},
};
})();
