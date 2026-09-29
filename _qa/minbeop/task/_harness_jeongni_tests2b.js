
async function G7(){
  resetLS({ox_q_links:{Q9901:['Q9902','Q9903'],Q9906:['','Q9901']}});
  loadQuiz(); showHome(); closeAllWins();
  const btns=id=>{ const w=document.getElementById('oxwin-q-'+id); return w?[...w.querySelectorAll('button')]:[]; };
  openQPopup('Q9901');
  const m1=btns('Q9901').find(b=>(b.getAttribute('onclick')||'')==="showRelated('Q9901','mine')");
  const s1=btns('Q9901').find(b=>(b.getAttribute('onclick')||'')==="showRelated('Q9901','same')");
  T('G7 ↩ 연결 N = ox_q_links 수(2)', !!m1&&m1.textContent==='↩ 연결 2', m1&&m1.outerHTML);
  T('G7 같은 판례 단추 글자 「🔗 판 1」', !!s1&&s1.textContent==='🔗 판 1', s1&&s1.textContent);
  T('G7 ↩ 연결 은 판 단추 바로 뒤', !!m1&&!!s1&&s1.nextElementSibling===m1);
  openQPopup('Q9906');
  const m6=btns('Q9906').find(b=>/'mine'\)$/.test(b.getAttribute('onclick')||''));
  T('G7 빈 칸은 안 센다(↩ 연결 1)', !!m6&&m6.textContent==='↩ 연결 1', m6&&m6.textContent);
  openQPopup('Q9904');
  T('G7 연결 0·판 0 이면 두 단추 다 없음', btns('Q9904').length>0&&btns('Q9904').filter(b=>/showRelated/.test(b.getAttribute('onclick')||'')).length===0);
  openQPopup('Q9902');
  T('G7 판 1 · 연결 0 이면 연결 단추 없음', btns('Q9902').some(b=>b.textContent==='🔗 판 1')&&!btns('Q9902').some(b=>/'mine'\)$/.test(b.getAttribute('onclick')||'')));
  if(m1) m1.click();
  T('G7 누르면 「내가 연결한」 창', !!document.getElementById('oxwin-rel-mine-Q9901'));
  closeAllWins();
}
async function G8(){
  resetLS({ox_q_geunge:{Q9903:[gItem('g_Q9903_a',1,'연결될 근거 글')]},ox_q_reflinks:{},ox_q_links:{Q9901:['Q9902']}});
  closeAllWins();
  openQuiz(['Q9901','Q9902'],'민법총칙',CH);
  openQPopup('Q9901');
  showLinkedQuestion('Q9901','Q9902');
  const cw=document.getElementById('oxwin-cmp-Q9901'), cbox=document.getElementById('cp-gg-box-Q9901');
  T('G8 비교 창에 근거 줄(cp-gg-box-) · 지문 <p> 바로 아래', !!cw&&!!cbox&&cw.contains(cbox)&&!!cbox.parentElement.previousElementSibling&&cbox.parentElement.previousElementSibling.tagName==='P', 'cmp '+!!cw+' · box '+!!cbox);
  const first=cw?cw.querySelector('.oxwin-body .flex.items-center.gap-2.mb-2'):null;
  T('G8 첫 줄에 「🔗 판 1」「↩ 연결 1」 칩', !!first&&[...first.querySelectorAll('button')].map(b=>b.textContent.trim()).join('|')==='🔗 판 1|↩ 연결 1', first?first.textContent.replace(/\s+/g,' '):'없음');
  if(!cbox){ closeAllWins(); showHome(); return; }
  const cin=document.getElementById('cp-gg-in-Q9901'); cin.value='비교 창에서 적은 근거'; key(cin,'Enter');
  const list=ggOf('Q9901'), k=(list[0]||{}).k;
  T('G8 비교 창에서 적은 근거 = 저장소 1건', list.length===1&&list[0].t==='비교 창에서 적은 근거', J(list));
  const ids=['gg-chip-Q9901-'+k,'qp-gg-chip-Q9901-'+k,'cp-gg-chip-Q9901-'+k];
  T('G8 세 상자(카드·문항 팝업·비교 창) 모두 새 칩', ids.every(x=>!!document.getElementById(x)), J(ids.map(x=>!!document.getElementById(x))));
  const ins=['gg-in-Q9901','qp-gg-in-Q9901','cp-gg-in-Q9901'].map(x=>document.getElementById(x));
  T('G8 다른 상자 칸은 비어 있다(적은 칸도 비움)', ins.every(x=>!!x&&x.value===''), J(ins.map(x=>x?x.value:null)));
  const cin2=document.getElementById('gg-in-Q9901'); cin2.value='카드에서 적은 둘째'; key(cin2,'Enter');
  const k2=(ggOf('Q9901')[1]||{}).k;
  T('G8 (반대) 카드에서 적으면 비교 창·팝업도 새 칩', !!k2&&!!document.getElementById('cp-gg-chip-Q9901-'+k2)&&!!document.getElementById('qp-gg-chip-Q9901-'+k2));
  T('G8 비교 창 댓글 칸도 GG_CMAX(ggMaxOf cp-)', ggMaxOf({id:'cp-gg-cin-Q9901-x'})===GG_CMAX&&ggMaxOf({id:'cp-refgg-cein-x'})===GG_CMAX&&ggMaxOf({id:'cp-gg-in-Q9901'})===GG_TMAX);
  const sbtn=[...document.querySelectorAll('#cp-gg-box-Q9901 button')].find(b=>b.textContent.trim()==='🔍'); if(sbtn) sbtn.click();
  const sin=document.getElementById('cp-link-search-geunge-Q9901'); if(sin){ sin.value='연결될'; sin.dispatchEvent(new Event('input',{bubbles:true})); }
  const hit=[...document.querySelectorAll('#cp-link-results-geunge-Q9901 button')].find(b=>b.textContent.indexOf('Q9903')>=0); if(hit) hit.click();
  T('G8 비교 창에서 연결 → 저장 1건 · 세 상자 연결 칩', J(refOf('Q9901','geunge'))===J(['Q9903'])&&['gg-refchip-Q9901-Q9903','qp-gg-refchip-Q9901-Q9903','cp-gg-refchip-Q9901-Q9903'].every(x=>!!document.getElementById(x)), J(refOf('Q9901','geunge')));
  closeAllWins(); showHome();
}
async function G9(){
  resetLS({});
  loadQuiz(); showHome(); closeAllWins();
  renderDashboard();
  T('G9 첫 화면이 그려진다', document.getElementById('dashboard-container').children.length>0);
  startQuiz('민법총칙',CH);
  T('G9 문제풀이가 열린다', !document.getElementById('quiz-screen').classList.contains('hide')&&!!document.getElementById('q-box-Q9901'));
  goHome();
  startQuiz('변리사 기출','2016년 제53회');
  T('G9 기출뷰가 열린다', !!document.getElementById('q-box-Q9905'), document.getElementById('quiz-container').textContent.slice(0,120));
  goHome();
  startQuiz('민법총칙',CH);
  await wait(250);
  const a0=__ALERTS.length;
  const pin=document.getElementById('tag-coord-Q9901');
  if(pin) pin.click();
  let cd=null;
  for(let i=0;i<200&&!(cd=document.getElementById('cd-close'));i++) await wait(50);
  T('G9 정리OMR(좌표기억) 뷰어가 열린다(카드 📍 핀 단추)', !!pin&&!!cd&&__ALERTS.length===a0, 'pin '+!!pin+' · cd-close '+!!cd+' · alert '+__ALERTS.slice(a0).join('/'));
  if(cd) cd.click();
  goHome();
}
