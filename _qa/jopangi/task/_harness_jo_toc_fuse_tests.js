/* _harness_jo_toc_fuse_tests.js — _task_jo_toc_fuse(+ _add1) 하네스가 페이지에 넣는 도구(__HT).
   BASE(genie HEAD f497f05)·NEW 둘 다에 같은 것을 넣는다 — 없는 것(칩 · ▸ · 편 한 줄 …)은 빈 값으로 돌려준다(헛잣대).
   재는 것 = DOM 실물 · 화면 기준 보임(display ≠ none 그리고 높이 > 0) · getBoundingClientRect · elementFromPoint · S 값 · 창(POPS).
   ⚠ 누름은 여기서 안 한다 — 자리만 돌려주고 파이썬이 page.mouse(PC) / CDP 터치(손가락 · 반지름 22)로 누른다(관문 규칙 1). */
(function(){
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const txt=e=>e?(e.textContent||'').replace(/\s+/g,' ').trim():'';
const R=e=>{if(!e)return null;const r=e.getBoundingClientRect();
  return {x:+r.left.toFixed(2),y:+r.top.toFixed(2),w:+r.width.toFixed(2),h:+r.height.toFixed(2),r:+r.right.toFixed(2),b:+r.bottom.toFixed(2),
          cx:+(r.left+r.width/2).toFixed(2),cy:+(r.top+r.height/2).toFixed(2)};};
const vis=e=>!!e&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0;   /* 화면 기준 보임(관문 규칙 2) */
const cs=(e,p)=>e?getComputedStyle(e)[p]:null;
function hitOn(t){if(!t)return null;try{t.scrollIntoView({block:'center',inline:'nearest'});}catch(e){}
  const r=R(t);const at=document.elementFromPoint(r.cx,r.cy);
  const onScreen=r.cy>0&&r.cy<innerHeight&&r.cx>0&&r.cx<innerWidth&&r.w>0&&r.h>0;
  return Object.assign(r,{on:!!at&&(at===t||t.contains(at))&&onScreen,at:at?(String(at.className&&at.className.baseVal!=null?at.className.baseVal:at.className||at.tagName)).slice(0,60):null,onScreen});}
async function idle(){for(let i=0;i<400&&(typeof busy!=='undefined'&&busy);i++)await wait(25);}
async function until(f,ms){const t0=Date.now();while(Date.now()-t0<(ms||8000)){try{const v=f();if(v)return v;}catch(e){}await wait(40);}try{return f();}catch(e){return null;}}
const pops=()=>(typeof POPS!=='undefined'?POPS:[]);
const popBy=k=>pops().find(x=>x._pk===k)||null;
const has=n=>{try{return typeof eval(n)!=='undefined';}catch(e){return false;}};
function Mi(no){return (VJ&&VJ.M||[]).findIndex(n=>String(n.no)===String(no));}
function Mt(t){return (VJ&&VJ.M||[]).findIndex(n=>n.제목===t);}
const k7=z=>z.uid||('P7:'+z.id);
window.__HT={
  wait,R,vis,hitOn,
  errs(){return (window.__ERR||[]).filter(e=>!/^ResizeObserver loop/.test(e)).slice(0,20);},
  async home(){try{closeAllPops();}catch(e){}try{closeSk();}catch(e){}
    S.law='특허법';S.tab='jimun';S.jimunTab='ox';S.mok='';S.oxQueue='';S.oxQ='';S.oxQMode='q';S.jtFold=false;S.jtCh={};
    await idle();await render();await idle();
    await until(()=>OXPOOL&&Object.keys(OXPOOL).length>1000&&typeof MBSR!=='undefined'&&MBSR&&MBSR.box&&MBSR.box.isConnected&&document.getElementById('jtlist'),30000);
    await wait(150);return __HT.state();},
  async rr(){await idle();await render();await idle();await wait(120);return __HT.state();},
  state(){return {tab:S.tab,law:S.law,jt:S.jimunTab,mok:S.mok||'',q:S.oxQ||'',qm:S.oxQMode||'q',sy:Math.round(scrollY),
    main:(()=>{const m=document.querySelector('#slot .main');return m?Math.round(m.scrollTop):null;})()};},
  Mi(no){return Mi(no);},
  node(no){const i=Mi(no);const n=(VJ.M||[])[i];return n?{i,no:n.no,제목:n.제목,조:n.조||null,소제목:n.소제목||null,지문:(n.지문||[]).length,리담:(n.리담||[]).length}:null;},
  /* ── 서랍 ── */
  jtRows(){const L=document.getElementById('jtlist');if(!L)return [];
    return [...L.children].map(r=>{const nm=r.querySelector('.jtnm')||r.querySelector('.tx')||r.querySelector('span');
      return {cls:r.className,nm:nm?[...nm.childNodes].filter(n=>n.nodeType===3).map(n=>n.nodeValue).join('').replace(/^[▾▸]\s*/,'').trim():txt(r),vis:vis(r),chips:[...r.querySelectorAll('.jochips .c2jb')].map(b=>txt(b)),now:!!r.querySelector('.now')};});},
  jtFind(label){const L=document.getElementById('jtlist');if(!L)return [];
    return [...L.children].filter(r=>{const nm=r.querySelector('.jtnm')||r.querySelector('.tx')||r.querySelector(':scope > span');
      const t=nm?[...nm.childNodes].filter(n=>n.nodeType===3).map(n=>n.nodeValue).join('').replace(/^[▾▸]\s*/,'').trim():'';return t===label;});},
  jtCount(label){return __HT.jtFind(label).length;},
  jtChip(label,chip){const r=__HT.jtFind(label)[0];if(!r)return null;const b=[...r.querySelectorAll('.jochips .c2jb')].find(x=>txt(x).startsWith(chip));
    if(!b)return null;return Object.assign(hitOn(b),{text:txt(b),fs:cs(b,'fontSize'),fw:cs(b,'fontWeight')});},
  jtName(label){const r=__HT.jtFind(label)[0];if(!r)return null;const t=r.querySelector('.jtnm')||r.querySelector('.tx')||r.querySelector(':scope > span');return hitOn(t);},
  jtArrow(label){const r=__HT.jtFind(label)[0];if(!r)return null;const a=r.querySelector('.jtar');return a?Object.assign(hitOn(a),{t:txt(a)}):null;},
  jtVis(label){const r=__HT.jtFind(label);return r.map(x=>vis(x));},
  /* ── 첫 화면 ── */
  homeRow(label){const all=[...document.querySelectorAll('.mbdash .mbur')];return all.find(r=>{const n=r.querySelector('.l .nm');return n&&txt(n)===label;})||null;},
  homeRowInfo(label){const r=__HT.homeRow(label);if(!r)return null;const L=r.querySelector('.l');
    return {cls:r.className,kids:[...L.children].map(c=>(c.className||c.tagName)+':'+txt(c).slice(0,40)),tot:txt(r.querySelector('.tot')),
      go:!!r.querySelector('.r .mbgo'),goTxt:txt(r.querySelector('.r .mbgo')),chips:[...r.querySelectorAll('.jochips .c2jb')].map(b=>txt(b)),
      nmFs:cs(r.querySelector('.nm'),'fontSize'),nmFw:cs(r.querySelector('.nm'),'fontWeight'),pad:cs(r,'padding'),bg:cs(r,'backgroundColor'),
      ar:!!r.querySelector('.l .ar'),sbt:!!r.querySelector('.l .mbsbt'),sbtTxt:txt(r.querySelector('.l .mbsbt')),vis:vis(r)};},
  homeChip(label,chip){const r=__HT.homeRow(label);if(!r)return null;const b=[...r.querySelectorAll('.jochips .c2jb')].find(x=>txt(x).startsWith(chip));
    if(!b)return null;return Object.assign(hitOn(b),{text:txt(b),fs:cs(b,'fontSize'),fw:cs(b,'fontWeight')});},
  headChip(label,chip){const h=__HT.homeHeadEl(label);if(!h)return null;const b=[...h.querySelectorAll('.jochips .c2jb')].find(x=>txt(x).startsWith(chip));
    return b?Object.assign(hitOn(b),{text:txt(b),fs:cs(b,'fontSize')}):null;},
  subTg(label){const r=__HT.homeRow(label);const t=r&&r.querySelector('.l .mbsbt');if(!t)return null;
    return Object.assign(hitOn(t),{t:txt(t),fs:cs(t,'fontSize'),fw:cs(t,'fontWeight'),color:cs(t,'color'),w:t.getBoundingClientRect().width});},
  subList(label){const r=__HT.homeRow(label);if(!r)return null;const l=r.nextElementSibling;
    if(!l||!l.classList.contains('mbsubs'))return {list:false};
    return {list:true,vis:vis(l),hidden:l.hidden,rows:[...l.querySelectorAll('.mbsi')].map(x=>({t:txt(x),z:x.classList.contains('z')})),
      ml:cs(l,'marginLeft'),bl:cs(l,'borderLeftWidth')};},
  homeHeadEl(label){return [...document.querySelectorAll('.mbdash .mbch > .hh')].find(h=>{const n=h.querySelector('.nm');return n&&txt(n)===label;})||null;},
  homeHead(label){const h=__HT.homeHeadEl(label);if(!h)return null;const n=h.querySelector('.nm');
    return Object.assign(hitOn(n),{go:h.classList.contains('mbhgo'),title:h.title||'',tot:txt(h.querySelector('.tot'))});},
  homeNames(label){return [...document.querySelectorAll('.mbdash .nm')].filter(n=>txt(n)===label).length;},
  cardHead(label){const hs=[...document.querySelectorAll('.mbdash .mbsj > .hd h2')];const h=hs.find(x=>txt(x).replace(/총 \d+문제$/,'').trim()===label);
    return h?{t:txt(h),vis:vis(h)}:null;},
  solo(){const r=document.querySelector('.mbdash .mbur.mbsolo');if(!r)return null;const n=r.querySelector('.nm');
    return Object.assign(hitOn(n),{text:txt(r.querySelector('.l')),tot:txt(r.querySelector('.tot')),go:!!r.querySelector('.mbgo'),goTxt:txt(r.querySelector('.mbgo')),
      card:!!r.querySelector('.mbchip.card'),fs:cs(n,'fontSize'),fw:cs(n,'fontWeight'),pad:cs(r,'padding'),bg:cs(r,'backgroundColor'),sbt:!!r.querySelector('.mbsbt')});},
  cardTots(){return [...document.querySelectorAll('.mbdash .mbsj')].map(c=>{const h=c.querySelector(':scope > .hd h2');const s=c.querySelector(':scope > .mbur.mbsolo');
    return {h:h?txt(h).replace(/총 \d+문제$/,'').trim():(s?txt(s.querySelector('.nm')):''),tot:h?txt(h.querySelector('.tot')):txt(s&&s.querySelector('.tot'))};});},
  heat(){const hb=document.querySelector('.mbhm');if(!hb)return null;const lg=[...hb.querySelectorAll('.hmlg')].map(x=>txt(x));
    let n=0;lg.forEach(t=>{const m=/(\d[\d,]*)\s*$/.exec(t);if(m)n+=+m[1].replace(/,/g,'');});
    return {lg,sum:n,pool:Object.keys(OXPOOL||{}).length,tops:[...hb.querySelectorAll('.hmsc')].map(b=>txt(b))};},
  /* ── 조문 팝업 ── */
  joPop(k){const p=popBy('jo|특허법|'+k);if(!p)return null;return {vis:vis(p),title:txt(p.querySelector('.pt')),z:+p.style.zIndex};},
  closeAll(){try{closeAllPops();}catch(e){}return pops().length;},
  /* ── 마디 화면 ── */
  async openMok(no){const i=Mi(no);S.mok='__mg'+i;S.oxPage=null;await __HT.rr();return i;},
  cards(){const map={};Object.values(VJ.P7map||{}).forEach(z=>{map['qb-'+k7(z)]=z;});
    return [...document.querySelectorAll('#slot .main .qwrap, #slot .main .jimun, #slot .main [id^="qb-"]')].filter(e=>e.id&&e.id.startsWith('qb-')).map(e=>{
      const z=map[e.id];const seq=e.querySelector('.oxseq')||e.querySelector('.mlnbk');   /* A-6(a) 9/30 — mbsame §B-1: 머리 순번 .oxseq 걷고 지문 앞 책 번호 .mlnbk(「1번 - (1)」) · 옛 앱은 .oxseq 그대로 */return {id:e.id,p7:z?z.id:null,sun:z?z.순:null,seq:seq?txt(seq):null,inCase:!!e.closest('.p7case')};});},
  cases(){return [...document.querySelectorAll('#slot .main .p7case')].map(b=>({h:txt(b.querySelector('.p7cash')),t:txt(b.querySelector('.p7cast')).slice(0,40),n:b.querySelectorAll('[id^="qb-"]').length,vis:vis(b)}));},
  oxBtn(key,v){const c=document.getElementById('qb-'+key);if(!c)return null;const b=c.querySelector('.mboxb.'+v);return b?Object.assign(hitOn(b),{sel:b.classList.contains('sel')}):null;},
  oxRec(key){try{return oxOf(key)||null;}catch(e){return null;}},
  mokIdx(id){try{return MOKIDX&&MOKIDX.p7?MOKIDX.p7[id]:undefined;}catch(e){return undefined;}},
  async mokIndexOf(id){try{const ix=await mokIndex();return ix.p7[id];}catch(e){return 'ERR '+e;}},
  /* ── 🔍 검색(add1) ── */
  srInput(){const i=MBSR&&MBSR.inp;return i?Object.assign(hitOn(i),{v:i.value}):null;},
  srRows(){const b=MBSR&&MBSR.box;if(!b)return null;return {vis:vis(b),cnt:txt(MBSR.cnt),rows:[...b.querySelectorAll('.rr')].map(r=>txt(r).slice(0,60))};},
  srRow(i){const b=MBSR&&MBSR.box;if(!b)return null;const r=b.querySelectorAll('.rr')[i||0];return r?hitOn(r):null;},
  srRowKey(i){/* i 번째 결과 줄의 지문 열쇠 — 결과 차례 = mbSearchRun 의 hit 차례와 같다 */
    const q=String(S.oxQ||'').trim();const P=OXPOOL||{};
    const gmode=(S.oxQMode==='g')&&(typeof ggAll==='function');
    let hit;if(gmode){const hg=Object.keys(ggAll()).filter(k=>P[k]&&(ggAll()[k]||[]).some(g=>(ggFlat(g)+' '+((g.cs||[]).map(c=>c.t||'').join(' '))).includes(q)));
      hit=hg.concat(Object.keys(typeof CL_BY_UID!=='undefined'?CL_BY_UID:{}).filter(k=>P[k]&&hg.indexOf(k)<0&&clHitsOf(k,q.toLowerCase()).length));}
    else hit=Object.keys(P).filter(k=>{const c=P[k]||{};return String(c.t||'').includes(q)||String(c.name||'').includes(q);});
    if(typeof uzPass==='function')hit=hit.filter(k=>uzPass(k));   /* ★ mbsame_add3 §A-6·§A-8(9/27) — 앱 검색 결과도 한 거름(기출/기타 · 유형)을 지난다 · 옛 판 = uzPass 없음 · 무변 */
    return hit[i||0]||null;},
  qPop(k){const p=popBy('q|📝 지문 '+k);if(!p)return null;const t=p.querySelector('.pt');
    return {vis:vis(p),mbqp:p.classList.contains('mbqp'),title:txt(t),z:+p.style.zIndex||0,n:pops().filter(x=>x._pk==='q|📝 지문 '+k).length};},
  qPopScroll(k){const p=popBy('q|📝 지문 '+k);if(!p)return null;const gg=p.querySelector('.ggbox');const bd=p.querySelector('.pb')||p;
    let sc=bd;if(!(sc.scrollHeight>sc.clientHeight+1)){for(let q=bd;q&&q!==document.body;q=q.parentElement){const o=getComputedStyle(q).overflowY;if((o==='auto'||o==='scroll')&&q.scrollHeight>q.clientHeight+1){sc=q;break;}if(q===p)break;}}
    const ph=p.querySelector(':scope > .ph');let top0=sc.getBoundingClientRect().top;
    if(ph&&sc.contains(ph)&&getComputedStyle(ph).position==='sticky')top0=Math.max(top0,ph.getBoundingClientRect().bottom);   /* 몸통 위 = 붙박이 머리 아랫변 */
    const a=gg?gg.getBoundingClientRect():null;
    return {gg:!!gg,off:a?+(a.top-top0).toFixed(1):null,ggh:a?Math.round(a.height):null,st:Math.round(sc.scrollTop),sh:sc.scrollHeight,ch:sc.clientHeight,
      bodyH:Math.round(sc.getBoundingClientRect().bottom-top0),sc:(sc.className||sc.tagName).slice(0,30)};},
  srFirstMg(){/* 결과 줄 중 단원(__mg…)에 붙은 첫 지문 — 「이 지문으로 이동」 관문용(미분류 리담은 옛 판도 「마디를 찾지 못했다」) */
    for(let i=0;i<200;i++){const k=__HT.srRowKey(i);if(!k)return -1;if(((MBK2M[k]||{}).sel||'').indexOf('__mg')===0)return i;}return -1;},
  qPopGo(k){const p=popBy('q|📝 지문 '+k);if(!p)return null;const b=[...p.querySelectorAll('button')].find(x=>txt(x).indexOf('이 지문으로 이동')>=0||/^↪\s*이동$/.test(txt(x)));return b?hitOn(b):null;},   /* ★ jo_cardfix §A-5 — 「↪ 이동」 글자 단추도 같은 단추 */
  maxZ(){return pops().reduce((m,p)=>Math.max(m,+p.style.zIndex||0),0);},
  seedGG(uid,t){const A=ggAll();A[uid]=[{k:'hx_'+Date.now().toString(36),i:1,t:t,ok:null,ts:Date.now(),cs:[]}];GGREC=A;try{lsWrite(GG_KEY,A,'근거');}catch(e){localStorage.setItem(GG_KEY,JSON.stringify(A));}return Object.keys(A).length;},
  longP7(min){/* 글이 긴 제7판 지문(팝업 몸통을 넘게) — OXPOOL 안 */const P=OXPOOL||{};let best=null;
    Object.keys(P).forEach(k=>{const c=P[k];if(c.kind==='P'&&String(c.t||'').length>(min||600)&&(!best||String(c.t).length>String(P[best].t).length))best=k;});return best;},
  /* ── 판례 목록(add1 C5) ── */
  async precBoot(){try{closeAllPops();}catch(e){}S.law='특허법';S.tab='prec';await __HT.rr();return S.tab;},
  precRow(i){const rs=[...document.querySelectorAll('#slot .prow, #slot .plist .r, #slot .plist > div')].filter(e=>vis(e)&&e.onclick);return rs[i||0]?Object.assign(hitOn(rs[i||0]),{t:txt(rs[i||0]).slice(0,40),n:rs.length}):null;},
  popsInfo(){return pops().map(p=>({k:p._pk,vis:vis(p),z:+p.style.zIndex||0}));}
};
})();
