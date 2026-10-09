/* ★ 시안 gg3 (사용자 10/8 13:14) — 물리 근거 세 칸(1 트리거 · 2 사용된 공식/개념 · 3 이 문제 주의점)
   저장 꼴 = 옛 GG[uid] 그대로 + 항목마다 f('t'|'c'|'w') · 2 칸은 ref('T:절#블록 차례' = 이론(물리 목차) 블록) — f 없는 옛 항목 = 트리거 칸
   서랍 = O△X 왼쪽 유형 · O△X(유형) 누름 = 세 근거 작은 창 · 🔍 오른쪽 상/중/하(첫 화면 난이도 FL.lv 하나를 같이 씀) */
(function(){
if(typeof SHELL==='undefined'||!SHELL||HASBOOK)return;
var G3F=[['t','트리거'],['c','공식·개념'],['w','이 문제 주의점']];
var G3L={t:'트리거',c:'공식·개념',w:'주의점'};
var g3f=function(g){return (g&&(g.f==='c'||g.f==='w'))?g.f:'t'};
var g3norm=function(t){return String(t||'').replace(/<[^>]+>/g,'').replace(/\s+/g,' ').trim().toLowerCase()};
/* 수식은 HTML 을 지을 때 바로 굽는다(나중 kx 로 바꾸면 근거 칸 높이가 한 번 더 바뀌어 쪽 다시 그림이 되풀이 · 10/8 잼) */
function g3K(h){if(!window.katex)return h;return String(h).replace(/\$([^$]+)\$/g,function(m,t){try{return katex.renderToString(t.replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>'),{throwOnError:false,output:'html',strict:'ignore'})}catch(e){return m}})}
var g3T=function(x){return g3K(thTxt(x))};
var g3plain=function(t){return String(t||'').replace(/<[^>]+>/g,'')};
/* 볼트 개별 물리 파일(UNITS · 「개념」 창 오른쪽) 블록 = br 사이 이어진 줄(볼트 블록 규칙 95) · ^id 가 있으면 열쇠 = 그 id(CB 짝)
   (물리 목차 THEORY 는 br 이 절마다 하나뿐 = 한 절이 30~50 줄 한 덩이라 블록으로 못 고름 · 10/8 잼) */
var TB=null;
function g3Blocks(){
  if(TB)return TB; TB=[];
  ((typeof UNITS!=='undefined'&&UNITS.sec)||[]).forEach(function(s){
    var cur=[],n=0;
    var flush=function(){if(cur.length){var a=(cur.find(function(x){return x.a})||{}).a||'';
      var cbk=a?(Object.keys(CB).find(function(q){return CB[q].i===a})||''):'';
      TB.push({key:a?('U:^'+a):('U:'+s.id+'#'+n),a:a,cbk:cbk,sec:String(s.id),st:String(s.t||''),lines:cur.slice(),
      text:cur.map(function(x){return g3plain(x.x)}).join('\n')});n++;cur=[]}};
    (s.b||[]).forEach(function(b){
      if(b.t==='br'){flush();return}
      if(b.t==='tb'){flush();cur=(b.rows||[]).map(function(rw){return {t:'p',i:0,x:rw.join(' | ')}});flush();return}
      if(b.t==='p'&&String(b.x||'').trim())cur.push(b)});
    flush()});
  return TB}
var g3Blk=function(ref){return g3Blocks().find(function(b){return b.key===ref})||null};
function g3SecName(id){var S=[];try{S.push(THEORY)}catch(e){}try{S.push(UNITS)}catch(e){}for(var q=0;q<S.length;q++){try{var x=S[q].sec.find(function(z){return String(z.id)===String(id)});if(x)return x.id+'. '+x.t}catch(e){}}return String(id||'')}
function g3BlkFind(q){
  var ws=g3norm(q).split(' ').filter(Boolean); if(!ws.length)return [];
  var out=[];
  for(var b of g3Blocks()){
    var hay=(b.sec+' '+b.st+' '+b.text).toLowerCase();
    if(ws.every(function(w){return hay.indexOf(w)>=0}))out.push(b);
    if(out.length>=8)break}
  return out}
/* 쓰임 — 같은 칸에 같은 것(2 칸 = 같은 블록 · 1·3 칸 = 같은 글)을 둔 문항 */
var g3Key=function(g){return (g3f(g)==='c'&&g.ref)?g.ref:g3norm(ggFlat(g))};
function g3Users(f,key){
  var set=[];
  for(var u in GG){(GG[u]||[]).forEach(function(g){if(!g||g3f(g)!==f)return;if(g3Key(g)===key&&set.indexOf(u)<0)set.push(u)})}
  /* 2 칸 — 그 블록이 개념(CB)이면 이미 이어 둔 문항(교재 CL · 개념 잇기 CX = CQ)도 같은 목록 */
  if(f==='c'){var b=g3Blk(key);if(b&&b.cbk)(CQ[b.cbk]||[]).forEach(function(no){var r=rec(no),u=r?GGU(r):'';if(u&&set.indexOf(u)<0)set.push(u)})}
  return set}
function g3UseHTML(f,uid,g){
  var n=g3Users(f,g3Key(g)).length; if(n<1)return '';   /* 댓글 v49(사용자 02:00 「하나만 연결됐어도 1부터 뜨게 해」) — 옛 = 2 넘어야 보임 */
  return '<i class="gguse g3use'+(n>=5?' hot':'')+'" data-g3use="'+ea(f+'|'+uid+'|'+g.k)+'" title="이 칸을 쓰는 문항 '+n+'">'+n+'</i>'}
function g3BlkLines(b,max){
  return b.lines.slice(0,max||99).map(function(x){return '<div class="thl i'+(x.i||0)+'">'+g3T(x.x)+'</div>'}).join('')}
/* 댓글 v12(사용자 16:18 「트리거·주의점은 한 줄씩 차지하고 내용이 보이게 · 공식은 볼트 블록이면 블록 전부 보이게」) — 칩 대신 항목마다 한 줄: 번호 · 글(공식·개념 = 블록 줄 전부 · 굵게) · 쓰인 수
   누름: 트리거·주의점 줄 = 고치기·댓글 판 펴기(옛 번호 칩과 같음) · 공식·개념 줄 = 그 블록 + 쓰인 문항 창 */
/* 댓글 v37(사용자 22:21 · 66 근거 줄 항목 「여기 부분 다 작은 창에서 보이던 것처럼 · 길게 누르면 고치기 · 삭제는 오른쪽 x · 왼쪽 ! 는 그대로」) —
   항목 줄 = 작은 창 꼴(번호·상자·「1.2.6 2차원 운동」 머리 없음 · 칸 사이 얇은 선 · 공식 = 블록 첫 줄 600) · 왼쪽 ! = 중요 표시(누르면 켜고 끔 · 옛 ggbang) · 오른쪽 쓰인 수 · x = 지우기(옛 지우기 창) · 길게 누름 = 그 자리 고치기(✓) · 누름 = 옛 그대로(공식 = 쓰인 문항 창 · 트리거·주의점 = 댓글·칸 옮기기 판) */
function g3ChipHTML(uid,g,f,n){
  var bang='<span class="ggbang g3bg'+(g.bang?' on':'')+'" data-ggbang="'+ea(uid+'|'+g.k)+'" data-gbnum="'+ea(uid+'|'+g.k)+'" title="중요 표시">!</span>';
  /* 댓글 v41(사용자 23:06 「x 왼쪽에 『댓』 글자 하나 · 누르면 댓글 쓰게 · 트리거·주의점 누르면 나오는 하얀 창 없애」) — 「댓」 = 그 줄 밑에 댓글 목록 + 적는 칸(앱 댓글 손 그대로) · 글 누름 판(ggtog) 걷음 */
  var cn=(Array.isArray(g.cs)?g.cs.length:0),sc='qp-'+f,ck=uid+'|'+g.k+'|'+sc,open=G3CMOPEN===ck;
  var cm='<button type="button" class="g3cm'+(cn?' has':'')+(open?' on':'')+'" data-g3cm="'+ea(ck)+'" title="댓글'+(cn?' '+cn:'')+'">댓</button>';
  var del='<button type="button" class="g3del" data-ggdel="'+ea(ck)+'" title="지우기" aria-label="지우기">✕</button>';
  var box=open?'<div class="g3cmb"><div data-ggcs="'+ea(ck)+'">'+ggCsHTML(g.cs,g.k,uid,sc)+'</div><div class="cin"><textarea rows="1" data-ggcin="'+ea(ck)+'"></textarea><button class="lk" data-ggreply="'+ea(ck)+'">달기</button></div></div>':'';
  if(f==='c'){
    var b=g.ref?g3Blk(g.ref):null;
    var body='<span class="g3tx">'+(b?g3T(b.lines[0].x):ggMath(ggFlat(g)))+'</span>';
    return '<div class="g3it g3r g3cc" data-f="c" data-g3c="'+ea(uid+'|'+g.k)+'" data-g3k="'+ea(uid+'|'+g.k+'|c')+'">'+bang+body+g3UseHTML(f,uid,g)+cm+del+'</div>'+box}
  return '<div class="g3it g3r" data-f="'+f+'" data-g3k="'+ea(uid+'|'+g.k+'|'+f)+'">'+bang+'<span class="g3tx">'+ggMath(ggFlat(g))+'</span>'+g3UseHTML(f,uid,g)+cm+del+'</div>'+box}
var G3CMOPEN=null;
/* 댓글 v47(사용자 00:56 「이것도 공식·개념인데 왜 여기엔 댓 · x 표시 안 돼」) — 이은 개념 줄에도 「댓」 · x
   이은 개념은 전부 교재가 이어 둔 것(CL 343 · 개념 잇기 CX 0 · 잼)이라 근거 항목(GG)이 아님 → 문항마다 「뺀 개념」 · 「개념 댓글」 을 기기 저장소 kv 'cqx' 에 따로 둠
   (교재 이음 CL 은 안 건드림 · 지시서 때 동기화 열쇠에 넣을 것) */
var G3CQX={hide:{},cs:{}};
(async function(){try{var v=await get('kv','cqx');if(v&&typeof v==='object'){G3CQX={hide:v.hide||{},cs:v.cs||{}}}}catch(e){}})();
async function g3CqxSave(){try{await put('kv','cqx',G3CQX)}catch(e){console.warn('cqx 저장',e)}}
function g3PanelHTML(uid,g,f){
  var h=ggPanelHTML(uid,g,'qp-'+f);
  var mv=G3F.filter(function(x){return x[0]!==f}).map(function(x){
    return '<button class="lk g3mv" data-g3mv="'+ea(uid+'|'+g.k+'|'+x[0])+'">→ '+G3L[x[0]]+'</button>'}).join('');
  var at='<button class="lk" data-gged=';
  return h.replace(at,mv+at)}
/* 댓글 v2(사용자 14:13 「세 줄을 토글 셋으로 한 줄 · 물리는 ㄱ·(1) 없애도」) — 한 줄 = 근거 · 🔗 · [트리거|공식·개념|주의점] 토글 · 고른 칸 칩 · 적는 칸 · ＋ · 🔍
   토글 = 어느 칸을 보고 적나(기기 안 한 값 · 문항 바뀌어도 그대로) · 토글 옆 수 = 그 칸 항목 수 · 라벨 칸(ㄱ·(1))은 물리에서 숨김(CSS) */
var G3SEL='t', G3SAVED=0, G3LASTQ=null;
/* 댓글 v23(사용자 18:57 「공식·개념 다 들어 있는 문제인데 왜 근거 없음이야」 · PA1501 59번) — 공식·개념 칸 = 근거에 넣은 블록 + 이미 이어 둔 개념(교재 CL · 개념 잇기 CX = conceptsOf) 같이 · 이은 개념 줄 누름 = 앱 개념 창(conceptSheet) */
function g3Cq(uid){try{var r=rowByUid(uid);if(!r||typeof conceptsOf!=='function')return [];var have={};ggOf(uid).forEach(function(g){if(g&&g3f(g)==='c'&&g.ref){have[String(g.ref).replace(/^U:\^/,'')]=1}});
  var hid=(G3CQX.hide||{})[qk(r[F.NO])]||[];return conceptsOf(r).filter(function(c){return !(c.i&&have[c.i])&&hid.indexOf(c.k)<0})}catch(e){return []}}   /* 댓글 v26(사용자 19:28 「왜 같은 게 두 개야」) — 근거에 넣은 블록과 같은 블록(^id)인 이은 개념은 한 번만 */
/* 댓글 v24(사용자 19:24 「그 개념이 그대로 보여야지」) — 이은 개념 = 볼트 물리 목차 그 블록 그대로(이론 THEORY 의 ^id 블록 · 줄 · 들여쓰기 · 수식 · 그림) */
function g3TheoryNode(id){var S=[];try{S.push(UNITS)}catch(e){}try{S.push(THEORY)}catch(e){}for(var q=0;q<S.length;q++){try{var sec=S[q].sec;for(var i=0;i<sec.length;i++){var b=sec[i].b||[];for(var j=0;j<b.length;j++)if(b[j].a===id)return b[j]}}catch(e){}}return null}   /* 볼트 개별 물리 파일(UNITS) 먼저 · 물리 목차(THEORY) */
function g3CqBody(c){var nd=g3TheoryNode(c.i),t=String(c.t||''),x=String(c.x||''),h='';
  if(x)h=x.split('\n').map(function(l,j){var m=(l.match(/^\t*/)||[''])[0].length;return '<div class="g3cql'+(j===0?' h':'')+'" style="padding-left:'+(m*12)+'px">'+g3T(l.replace(/^\t+/,''))+'</div>'}).join('');
  else if(t&&t!==c.i)h='<div class="g3cql h">'+g3T(t)+'</div>';
  if(nd&&nd.g)h+='<img class="g3cqimg" draggable="false" src="img/'+nd.g+'.jpg" alt="">';
  return h}
function g3CqHTML(uid,c,n){var nq=g3QUsers(c,c.k);if(nq.indexOf(uid)<0)nq.push(uid);
  var key=uid+'|'+c.k,cs=(G3CQX.cs||{})[key]||[],open=G3CMOPEN==='q|'+key;
  var cm='<button type="button" class="g3cm'+(cs.length?' has':'')+(open?' on':'')+'" data-g3cqcm="'+ea(key)+'" title="댓글'+(cs.length?' '+cs.length:'')+'">댓</button>';
  var del='<button type="button" class="g3del" data-g3cqdel="'+ea(key)+'" title="이 문항에서 빼기" aria-label="빼기">✕</button>';
  var box=open?'<div class="g3cmb"><div>'+(cs.length?cs.map(function(x){return '<div class="ggcs"><span class="d">'+ggMD(x.ts)+'</span><span class="t">'+esc(x.t)+'</span><button class="lk red" data-g3cqcd="'+ea(key+'|'+x.k)+'">지우기</button></div>'}).join(''):'<div class="ggcs-0">댓글 없음</div>')+'</div><div class="cin"><textarea rows="1" data-g3cqin="'+ea(key)+'"></textarea><button class="lk" data-g3cqreply="'+ea(key)+'">달기</button></div></div>':'';
  return '<div class="g3it g3r g3cc g3cq" data-f="c" data-g3cq="'+ea(key)+'" title="이어 둔 개념 — 누르면 쓰인 문항"><span class="g3bg0"></span><div class="g3bkl">'+g3CqBody(c)+'</div>'+(nq.length>=1?'<i class="gguse g3use g3pn0" data-g3useq="'+ea(key)+'" title="이 개념을 쓴 문항 '+nq.length+'">'+nq.length+'</i>':'')+cm+del+'</div>'+box}
function g3TyHTML(uid){var r=rowByUid(uid);if(!r||typeof TYPES==='undefined')return '';var no=r[F.NO],cur=typeOf(no),fx=typeFixed(no);
  return '<span class="g3ty">'+TYPES.map(function(t){var on=cur.indexOf(t)>=0;return '<button type="button" class="'+(on?'on':'')+(on&&!fx?' dr':'')+'" data-g3ty="'+ea(uid+'|'+t)+'">'+esc(t)+'</button>'}).join('')+'</span>'}
function g3LineHTML(uid,sc){
  var list=ggOf(uid), f=G3SEL, cq=g3Cq(uid);
  var by={t:[],c:[],w:[]}; list.forEach(function(g){if(g)by[g3f(g)].push(g)});
  var row=ggRowHTML('').replace('<textarea rows="1" class="txt">','<textarea rows="1" class="txt" placeholder="'+(f==='c'?'블록 찾기':G3L[f])+'">');
  var pans=G3F.map(function(x){return by[x[0]].map(function(g){return g3PanelHTML(uid,g,x[0])}).join('')}).join('');
  return '<div class="ggbox g3box" id="'+sc+'gg-box-'+ea(uid)+'" data-ggbox="'+ea(uid+'|'+sc)+'">'
    /* 댓글 v27(사용자 19:36 「이 줄(유형 작은 창) 없애고 공식·계산·함정·개념 작게 글자로만 『근거』 글자 크기로 · 그 아랫줄에 트리거·공식개념·주의점 · 입력창은 원래 트리거 칩 있던 줄로 · 오른쪽 병렬·검색 칩 없애」)
       1 줄 = 근거 · 유형 글자 넷(누르면 켜고 끔 · 바로 저장) · 🔗 / 2 줄 = 토글 셋 / 3 줄 = 적는 칸(＋ · 🔍 걷음) / 그 아래 = 항목 줄 */
    /* 댓글 v29(사용자 20:03 「근거 누르면 유형 창 뜬 거에서 하라고」 · v27 을 잘못 읽음) — 줄 = 「근거」(누르면 작은 창: 유형 글자 넷 / 토글 셋) + 적는 칸(옛 토글 자리 · ＋·🔍 없음) · 그 아래 항목 줄 */
    +'<div class="ggline g3f" data-g3f="'+f+'"><span class="lb g3lb">근거'+ggUseHTML(uid,'↩',uid)+'</span>'
    +'<span class="refchips">'+ggRefChipsHTML(uid,sc)+'</span>'
    /* 댓글 v7(사용자 15:41 「토글에 맞는 것만 뜨지 말고 · 트리거 초록 · 공식 파랑 · 주의점 주황 바탕 · 입력한 것은 토글 상관없이 다 뜨게」) — 칩은 세 칸 다(트리거 → 공식·개념 → 주의점 차례 · 칸마다 번호) · 색 = 칸 · 토글은 적을 칸만 고름 */
    +((list.length||cq.length)?'<div class="chips g3list">'+G3F.map(function(x){return by[x[0]].map(function(g,i){return g3ChipHTML(uid,g,x[0],i+1)}).join('')+(x[0]==='c'?cq.map(function(c,i){return g3CqHTML(uid,c,by.c.length+i+1)}).join(''):'')}).filter(function(h){return h}).map(function(h){return '<div class="g3grp">'+h+'</div>'}).join('')+'</div>':'')
    +'<span class="ggrows" data-ggrows="'+ea(uid+'|qp-'+f)+'">'+row+'</span>'
    +'<button class="pl save hide" data-ggsave="'+ea(uid+'|qp-'+f)+'">저장</button>'
    +'<div class="g3sug hide"></div></div>'
    +'<div class="ggpans">'+pans+'</div>'
    +'<div class="ggrb" data-ggrb="'+ea(uid+'|'+sc)+'">'+ggRefBoxHTML(uid,sc)+'</div>'
    +'<div class="ggfind hide" data-ggfindbox="'+ea(uid+'|'+sc)+'">'
    +'<input placeholder="근거·댓글에서 찾기"><div class="res"></div></div>'
    +'</div>'}
function g3Sel(uid,f){
  var t=document.querySelector('[data-ggbox="'+CSS.escape(uid+'|qp-')+'"] .g3f .ggrows .txt'), v=t?t.value:'';
  G3SEL=f; ggRepaint(uid);
  var n=document.querySelector('[data-ggbox="'+CSS.escape(uid+'|qp-')+'"] .g3f .ggrows .txt');
  if(n){n.value=v;try{ggFit(n)}catch(e){};n.focus();if(v)g3Sug(n)}}
window.g3Sel=g3Sel;
/* 댓글 v11(사용자 16:17 「펜 알약 왼쪽에 아래 화살표 단추 · 그 아래 근거 · + · 찾기 줄이 보였다 안 보였다」) — ▾ 하나 · 접힘 = 기기 하나 값(localStorage · 문항 바꿔도 그대로) · PC·폰 같음 */
/* 댓글 v21(사용자 18:24 「접힌 상태가 기본」) — 기본 = 접힘 · 편 것만 기기에 남김(새 열쇠 · 옛 「1」 기억 안 읽음) · G3FOLDMEM = 시안 화면 하나만의 값(저장 안 함) */
/* 댓글 v24(사용자 19:24 「처음에 접힌 게 기본이라 했는데 왜 안 접혀서 나와」) — 문항을 열 때마다 접힘(옛 판은 한 번 펴면 기기에 남아 다음 문항도 펴짐) · 그 문항 보는 동안만 편 상태 유지 */
var G3FOLDCUR=true,G3FOLDNO=null;
function g3FoldOn(){if(typeof window.G3FOLDMEM==='boolean')return window.G3FOLDMEM;if(typeof VNO!=='undefined'&&VNO!==G3FOLDNO){G3FOLDNO=VNO;G3FOLDCUR=true}return G3FOLDCUR}
function g3Fold(){
  var vt=document.querySelector('#view .vtop'), pill=document.getElementById('inkPill'), v=document.getElementById('view');
  if(!vt||!v)return;
  var b=document.getElementById('g3Fold');
  if(!b){b=document.createElement('button');b.type='button';b.id='g3Fold';b.textContent='▾';
    b.onclick=function(e){e.stopPropagation();var on=!v.classList.contains('g3off');v.classList.toggle('g3off',on);
      if(typeof window.G3FOLDMEM==='boolean')window.G3FOLDMEM=on;else G3FOLDCUR=on;b.title=on?'근거 줄 펴기':'근거 줄 접기'}}
  var br=document.getElementById('g3FoldBr');if(!br){br=document.createElement('i');br.id='g3FoldBr'}   /* 좁은 창(폰) = 줄바꿈 칸 · ▾ 와 펜 알약이 같은 둘째 줄(▾ 왼쪽 · 알약 오른쪽) */
  if(pill&&pill.parentNode===vt){if(b.nextSibling!==pill)vt.insertBefore(b,pill);if(br.nextSibling!==b)vt.insertBefore(br,b)}else if(b.parentNode!==vt){vt.appendChild(br);vt.appendChild(b)}
  v.classList.toggle('g3off',g3FoldOn()); b.title=g3FoldOn()?'근거 줄 펴기':'근거 줄 접기'}
window.g3Fold=g3Fold;
function g3After(){
  try{g3Fold()}catch(e){}
  document.querySelectorAll('.g3box').forEach(function(b){
    b.querySelectorAll('.ggrows[data-ggrows]').forEach(function(r){try{ggRowsSync(r)}catch(e){}});
    })}
window.g3LineHTML=g3LineHTML; window.g3After=g3After;
/* 저장 — 칸(f)을 달아 넣는다 · 번호 i 는 옛 꼴 그대로(문항 안 한 줄 차례) */
async function g3Push(uid,f,o){
  /* 댓글 v6(사용자 14:48 「이건 왜 3 개나」) — 같은 칸에 같은 블록·같은 글은 두 번 안 넣음(이미 있으면 그대로) */
  var dup=ggOf(uid).find(function(x){return x&&g3f(x)===f&&(f==='c'&&o.ref?x.ref===o.ref:g3norm(ggFlat(x))===g3norm(o.t))});
  if(dup){G3SAVED=Date.now();ggRepaint(uid);return dup}
  var list=ggOf(uid).slice(); list.forEach(function(x,n){if(x&&x.i!==n+1)x.i=n+1});
  var g={k:ggNewKey('g_'),i:list.length+1,t:o.t,ok:ggMarkNow(rowByUid(uid)[F.NO]),ts:Date.now(),cs:[],f:f};
  if(o.parts)g.parts=o.parts; if(o.ref)g.ref=o.ref;
  list.push(g); G3SAVED=Date.now(); await ggSaveList(uid,list); ggRepaint(uid); return g}
var _add0=ggAdd0;
ggAdd0=async function(uid,sc,keepFocus,box){
  var m=/^qp-([tcw])$/.exec(sc); if(!m)return _add0.apply(this,arguments);
  var f=m[1], rows=ggRowsOf(box).filter(function(x){return x.t}); if(!rows.length)return 0;
  var flat=rows.map(function(x){return (x.l?x.l+' ':'')+x.t}).join('\n');
  if(!ggLimitOk(box.querySelector('.txt'),flat,GG_TMAX))return 0;
  G3LASTQ=String((box.querySelector('.txt')||{}).value||'').trim();
  await g3Push(uid,f,{t:flat,parts:(rows.length>1||rows[0].l)?rows.map(function(x){return {l:x.l,t:x.t}}):null});
  if(keepFocus){var t=document.querySelector('[data-ggrows="'+CSS.escape(uid+'|'+sc)+'"] .txt');if(t)t.focus()}
  return 1};
/* 찾기 — 칸에 치면 바로 아래 목록(2 칸 = 이론 블록 · 1·3 칸 = 다른 문항이 그 칸에 쓴 글) */
function g3SugList(uid,f,q){
  if(f==='c')return g3BlkFind(q).map(function(b){return {ref:b.key,b:b,n:g3Users('c',b.key).length}});
  var ws=g3norm(q).split(' ').filter(Boolean), m={};
  /* 댓글 v38(사용자 22:23 「트리거랑 주의점은 검색 범위 같게 · 주의점에 쓴 것도 트리거에서 · 트리거에 쓴 것도 주의점에서」) — 1·3 칸은 두 칸 글을 같이 찾음 · 이 문항 같은 칸에 이미 있는 글만 뺌 */
  for(var u in GG){(GG[u]||[]).forEach(function(g){if(!g)return;var gf=g3f(g);if(gf==='c')return;var k=g3norm(ggFlat(g));if(!k)return;
    if(!ws.every(function(w){return k.indexOf(w)>=0}))return;
    (m[k]=m[k]||{t:ggFlat(g),us:[],mine:false});if(m[k].us.indexOf(u)<0)m[k].us.push(u);if(String(u)===String(uid)&&gf===f)m[k].mine=true})}
  return Object.keys(m).map(function(k){return {t:m[k].t,n:m[k].us.length,mine:m[k].mine}})
    .filter(function(x){return !x.mine}).sort(function(a,b){return b.n-a.n}).slice(0,8)}
function g3Sug(t){
  var line=t.closest('.g3f'); if(!line)return;
  var f=line.dataset.g3f, sug=line.querySelector('.g3sug'), q=String(t.value||'').trim();
  var uid=String(t.closest('.ggrows').getAttribute('data-ggrows')).split('|')[0];
  if(!q){sug.classList.add('hide');sug.innerHTML='';sug.__l=[];return}
  var L=g3SugList(uid,f,q); sug.__l=L; sug.__uid=uid; sug.__f=f;
  sug.innerHTML=L.length?L.map(function(x,i){
    if(f==='c')return '<div class="g3s'+(i===0?' on':'')+'" data-i="'+i+'"><div class="sec">'+esc(x.b.sec+'. '+x.b.st)
      +(x.n?' <i class="g3n">'+x.n+'</i>':'')+'</div><div class="bt">'+g3BlkLines(x.b,3)+'</div></div>';
    return '<div class="g3s" data-i="'+i+'"><span class="bt1">'+esc(x.t)+'</span> <i class="g3n">'+x.n+'</i></div>'}).join('')
    :'<div class="g3none">'+(f==='c'?'맞는 블록 없음':'다른 문항에 같은 글 없음 · Enter = 새로 적기')+'</div>';
  sug.classList.remove('hide');}
async function g3Pick(sug,i){
  var x=(sug.__l||[])[i]; if(!x)return;
  var uid=sug.__uid,f=sug.__f;
  var q0=sug.closest('.g3f')&&sug.closest('.g3f').querySelector('.ggrows .txt');G3LASTQ=q0?String(q0.value).trim():null;
  if(f==='c')await g3Push(uid,'c',{t:x.b.text,ref:x.ref}); else await g3Push(uid,f,{t:x.t});
  var t=document.querySelector('[data-ggrows="'+CSS.escape(uid+'|qp-'+f)+'"] .txt'); if(t)t.focus()}
document.addEventListener('input',function(e){var t=e.target;if(t&&t.matches&&t.matches('.g3f .ggrows[data-ggrows] .txt'))g3Sug(t)},true);
/* 시안 거울 탓 막기 — 적은 직후 다시 그린 칸에 떨어져 나간 옛 칸의 change 가 옛 글을 되붙이지 않게(앱에선 떨어진 칸이라 일 없음) */
document.addEventListener('change',function(e){var t=e.target;if(t&&t.matches&&t.matches('.g3f .ggrows[data-ggrows] .txt')&&Date.now()-G3SAVED<2000&&G3LASTQ!==null&&String(t.value).trim()===G3LASTQ){t.value='';var s=t.closest('.g3f').querySelector('.g3sug');if(s)s.classList.add('hide')}},true);
/* 2 칸은 칸을 떠날 때 저절로 적지 않는다(찾던 낱말이 근거로 들어가지 않게) · 목록 닫기 */
window.addEventListener('focusout',function(e){var t=e.target;
  if(!t||!t.matches||!t.matches('.g3f .ggrows[data-ggrows] .txt'))return;
  var line=t.closest('.g3f'),to=e.relatedTarget;if(line&&to&&!line.contains(to)){var s0=line.querySelector('.g3sug');if(s0)s0.classList.add('hide')}
  if(line&&line.dataset.g3f==='c')e.stopPropagation()},true);
window.addEventListener('keydown',function(e){var t=e.target;
  if(!t||!t.matches||!t.matches('.g3f .ggrows[data-ggrows] .txt'))return;
  var sug=t.closest('.g3f').querySelector('.g3sug'); if(!sug||sug.classList.contains('hide')||!(sug.__l||[]).length)return;
  var on=sug.querySelector('.g3s.on'), i=on?+on.dataset.i:0, n=sug.__l.length;
  /* 댓글 v52 — 트리거·주의점 목록은 처음에 고른 줄 없음(옛 = 첫 줄이 고른 것처럼 칠해져 있는데 Enter 는 친 글을 새로 적음 · 헷갈림) · ↓↑ 로 고른 줄이 있으면 Enter = 그 줄 */
  if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();e.stopPropagation();i=on?(i+(e.key==='ArrowDown'?1:n-1))%n:(e.key==='ArrowDown'?0:n-1);
    sug.querySelectorAll('.g3s').forEach(function(x){x.classList.toggle('on',+x.dataset.i===i)});return}
  if(e.key==='Escape'){sug.classList.add('hide');e.stopPropagation();return}
  if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing&&(sug.__f==='c'||on)){e.preventDefault();e.stopPropagation();g3Pick(sug,i)}},true);
document.addEventListener('pointerdown',function(e){if(e.target.closest&&e.target.closest('.g3s'))e.preventDefault()},true);
document.addEventListener('mousedown',function(e){if(e.target.closest&&e.target.closest('.g3s'))e.preventDefault()},true);
/* 목록 밖을 누르면 닫음(창 밖으로 초점이 나가는 것만으로는 안 닫음) */
document.addEventListener('pointerdown',function(e){var f=e.target.closest&&e.target.closest('.g3f');document.querySelectorAll('.g3sug:not(.hide)').forEach(function(s){if(!f||!f.contains(s))s.classList.add('hide')})},true);
/* 쓰인 문항 창 — ggUseWin 꼴 그대로(같은 창틀 · 같은 줄) */
function g3UseWin(f,uid,k,o){
  var g=ggItem(uid,k); if(!g)return;
  var key=g3Key(g), owners=ggUseSort(g3Users(f,key)), b0=(f==='c'&&g.ref)?g3Blk(g.ref):null;
  var head='<div class="gguh">'+(b0?'<div class="ln"><span class="cd">'+esc(b0.sec)+'</span><span class="un">'+esc(b0.st)+'</span></div>'
      /* 댓글 v14(사용자 16:20 「블록 내용은 필요 없어 · 앞에서 이미 보임」) — 창 머리 = 절 번호 · 절 이름만 */
      :'<div class="ln"><span class="cd">'+G3L[f]+'</span></div><div class="gg">'+ggMath(ggFlat(g))+'</div>')+'</div>';
  g3UseWinOpen(uid,head,'이 '+(f==='c'?'블록':'글')+'을 '+G3L[f]+' 칸에 쓴 문항 '+owners.length,owners,
    function(){return ''},   /* 댓글 v51(사용자 10:59 「걷어」 · 스레드 63575dc9) — 지금 문항 줄 「고치기·댓글」(옛 하얀 판 길 · 칸 옮기기 같이 없어짐 = 사용자 알고 고름) 걷음 */b0?b0.sec:'',(g.ref?String(g.ref).replace(/^U:\^/,''):''),!!(o&&o.list))}
/* 댓글 v32(사용자 21:32 「『공식·개념』 이라는 건 같은데 왜 하나는 첫 번째(쓰인 문항 창) · 하나는 두 번째(개념 창)가 떠」) — 이은 개념 줄 누름도 근거 블록과 같은 창:
   머리 = 절 번호 · 절 이름 · 「이 블록을 공식·개념 칸에 쓴 문항 N」(근거로 쓴 문항 + 교재·개념 잇기로 이은 문항) · 지금 문항 줄 = 「개념 연결 고치기」 · 밀기 같음 */
function g3UseWinQ(uid,ck,o){var c=(typeof CB!=='undefined')&&CB[ck];if(!c)return;
  var m=String(c.n||'').match(/^\s*([\d.]+?)\.?\s+(.*)$/),cd=m?m[1]:String(c.n||''),un=m?m[2]:'';
  var set=g3QUsers(c,ck);if(set.indexOf(uid)<0)set.push(uid);var owners=ggUseSort(set);
  var head='<div class="gguh"><div class="ln"><span class="cd">'+esc(cd)+'</span><span class="un">'+esc(un)+'</span></div></div>';
  g3UseWinOpen(uid,head,'이 블록을 공식·개념 칸에 쓴 문항 '+owners.length,owners,
    function(){return ''},cd,c.i||'',!!(o&&o.list))}   /* 댓글 v34 — 지금 문항 줄 「개념 연결 고치기」 걷음 */
window.g3UseWinQ=g3UseWinQ;
function g3QUsers(c,ck){var set=c&&c.i?g3Users('c','U:^'+c.i).slice():[];(CQ[ck]||[]).forEach(function(no){var r=rec(no),u=r?GGU(r):'';if(u&&set.indexOf(u)<0)set.push(u)});return set}
function g3UseWinOpen(uid,head,sepTxt,owners,meBtn,secId,markId,listMode){
  var old=document.getElementById('gguw');if(old)old.remove();
  var sep='<div class="gsep">'+sepTxt+'</div>';
  var rows=owners.map(function(u){var r=rowByUid(u);
    if(!r)return '<div class="gguR none">'+esc(String(u))+' — 지금 데이터에 없음</div>';
    var isMe=String(u)===String(uid);
    /* 댓글 v42(사용자 23:08 「여기도 제목 누르면 이 문제 팝업 창 뜨게 · 첫 화면 큰 목록처럼 문제 간략하게 · 그림 있으면 그림도」) — 제목 누름 = ↗ 와 같음(그 문제 = 본창 옆 창) · 아래 = 첫 화면 목록 글(pvText · 세 줄) + 발문 그림(pvFigHTML) */
    return '<div class="gguR'+(isMe?' me':'')+'"><div class="ln">'
      /* 댓글 v48(사용자 01:42 「제목 클릭하면 이 문제 팝업창 떠야지 왜 안 떠」 · 닻 폰 71 「0회 10번」 = 지금 문항 줄 · 옛 = 지금 문항 줄만 누름 없음) — 지금 문항 줄 제목도 누름 */
      +'<span class="g3ttl" data-gguugo="'+ea(String(u))+'" title="그 문제 보기"><span class="cd">'+esc(codeShow(r))+'</span><span class="un">'+esc(ggWhere(r))+'</span></span>'
      +(isMe?'<span class="now">지금 보는 문항</span>':'')+'<span class="sp"></span>'
      +(isMe?meBtn():'')   /* 댓글 v44(사용자 23:11 「제목 눌러서 팝업 뜨게 했으니 이 아이콘 필요 없잖아」) — ↗ 걷음 */
      +'</div><div class="g3qq">'+esc((typeof pvText==='function')?pvText(r):String(txtOf(u,'q')||''))+'</div>'+((typeof pvFigHTML==='function')?pvFigHTML(r):'')+'</div>'}).join('');
  var b=document.createElement('div');b.className='sheet shfloat';b.id='gguw';   /* 댓글 v55(사용자 13:25 「이미 앱에는 그렇게 적용돼 있었는데 네가 퇴화시킨 거라고?」) — 옛 = 화면 전체를 덮는 모달 판(.sheet · 앱 옛 ggUseWin 틀) → 떠 있는 동안 본창·서랍을 못 누름(누른 창 맨 위 규칙이 안 먹은 까닭) · 이제 개념 창처럼 떠 있는 창(.shfloat · 판만 누름) */
  /* 댓글 v13(사용자 16:20 「이 줄 없애」 · 창 머리 「공식·개념 · 쓰인 문항 N」 줄) — 머리 줄 걷음 · ✕ 는 창 오른쪽 위 · 끌기 손잡이 = 블록 머리(gguh) */
  /* 댓글 v36(사용자 22:16 「이 오른쪽 덮개(절 이론)를 메인으로 · 쓰인 공식·개념 부분에 점선 테두리 · 『이 블록을 공식·개념 칸에 쓴 문항』 을 오른쪽 덮개로」) —
     본문 = 그 절 이론(물리 목차) · 그 블록 = 점선 테두리(그 자리로 굴림) · 쓰인 문항 목록 = 왼쪽으로 밀면 나오는 오른쪽 덮개 · 오른쪽으로 밀면 목차(누르면 본문이 그 절) */
  /* 댓글 v49(사용자 01:59 「근거에 쓰인 숫자 클릭했는데 왜 이상한 창이 떠 · 이 근거를 쓰는 문제들이 떠야 할 거 아냐」 · 닻 66 트리거 줄 숫자) — 트리거·주의점(볼트 블록 아님 · 절 없음)은 본문이 비고 목록이 밀어야 나오는 덮개에만 있었음
     → 절 없는 창 = 본문이 바로 그 글을 쓴 문항 목록(밀기 없음) · 공식·개념(절 있음)은 v36 그대로 */
  var LIST=!secId||!!listMode;   /* v50 — 쓰인 수(숫자) 누름 = 공식·개념도 목록 창 */
  var mk=LIST?rows:g3SecMark(secId,markId);
  /* 댓글 v40(사용자 22:32 「얇게 · 1.2.6. 2차원 운동 이 글씨 크기 정도만 · 큰 테두리 줄이 계속 따라다닐 필요 없잖아」) — 머리 = 작은 글 한 줄(바탕·테두리 없음) · 본문과 같이 굴러감 */
  /* 댓글 v41(사용자 23:44 「장난하냐」 — v40 머리가 굴러 올라가면 창을 못 끌었음) — 끌기 손잡이 = 창 맨 위 얇은 띠(굴리지 않음 · 늘 그 자리) */
  /* 댓글 v46(사용자 00:55 「이럴 거면 『1.2.6. 2차원 운동』 글자 줄이 계속 따라오게 하면 되잖아 · 왜 빈 줄이 따라오게 만들어」) — 빈 끌기 띠 걷음 · 머리 글 줄(작은 글 · 얇게)이 맨 위에 늘 있고 그 줄이 끌기 손잡이 */
  b.innerHTML='<div class="panel g3uw"><button id="gguwX" class="g3x" title="닫기">✕</button><div id="gguwBody">'+head+'<div id="gguwSec"><div id="gguwMk"'+(LIST?' class="g3uwList"':'')+'>'+mk+'</div></div></div></div>';
  document.body.appendChild(b);g3DrDown();
  b.querySelector('#gguwX').onclick=function(){b.remove()};

  if(!WIN.gguse){var sv=null;try{sv=JSON.parse(localStorage.getItem('jagwa.win.gguse')||'null')}catch(e){}
    if(!sv){var w=Math.min(560,Math.round(window.innerWidth*0.92)),h=Math.min(640,Math.round(window.innerHeight*0.8));
      WIN.gguse={w:w,h:h,l:Math.round((window.innerWidth-w)/2),t:Math.round((window.innerHeight-h)/2)}}}
  makeFloat(b,b.querySelector('.gguh'),'gguse','jagwa.win.gguse');
  /* 얇은 띠라 끄는 동안 손가락·마우스가 띠 밖으로 나가도 계속 끌리게(포인터 잡기를 못 받는 자리 대비 · 같은 좌표를 띠로 넘김) */
  (function(h){if(!h)return;var on=false;h.addEventListener('pointerdown',function(e){if(e.isTrusted||e.pointerId!==999)on=true},true);
    var mv=function(e){if(!on||e.target===h)return;h.dispatchEvent(new PointerEvent('pointermove',{clientX:e.clientX,clientY:e.clientY,pointerId:e.pointerId,bubbles:false,buttons:1}))};
    var upf=function(e){if(!on)return;on=false;if(e.target!==h)h.dispatchEvent(new PointerEvent('pointerup',{clientX:e.clientX,clientY:e.clientY,pointerId:e.pointerId,bubbles:false}))};
    document.addEventListener('pointermove',mv,true);document.addEventListener('pointerup',upf,true);document.addEventListener('pointercancel',upf,true);
    var mo=new MutationObserver(function(){if(!b.isConnected){document.removeEventListener('pointermove',mv,true);document.removeEventListener('pointerup',upf,true);document.removeEventListener('pointercancel',upf,true);mo.disconnect()}});mo.observe(document.body,{childList:true})})(b.querySelector('.gguh'));
  pwTop(b);
  /* 댓글 v31(사용자 21:27 「작은 창에서 <> 눌렀을 때 나오는 개념 창인데 왜 여긴 스와이프 안 돼」) — 쓰인 문항 창도 개념 창과 같은 밀기: 오른쪽 = 목차 · 왼쪽 = 그 블록 절 이론 */
  try{kx(b.querySelector('#gguwMk'))}catch(e){}
  [80,400,900].forEach(function(ms){setTimeout(function(){if(b.__userScr)return;var sc=b.querySelector('#gguwSec'),m=b.querySelector('#gguwSec .g3mk');if(sc&&m)sc.scrollTop=Math.max(0,m.offsetTop-8)},ms)});   /* 글꼴·수식 그린 뒤 높이가 바뀌어도 그 블록이 보이게 */
  b.addEventListener('wheel',function(){b.__userScr=1},{passive:true});b.addEventListener('touchmove',function(){b.__userScr=1},{passive:true});
  if(LIST){try{if(typeof pvWatch==='function')pvWatch(b.querySelector('#gguwMk'))}catch(e){}return}
  try{if(typeof THEORY!=='undefined'&&THEORY.sec){b.classList.add('g3cw');g3CwDecor(b,rowByUid(uid),null,secId||'',{rHTML:function(){return rows},   /* 댓글 v43(사용자 23:10 「이 줄 없애」) — 「이 블록을 … 쓴 문항 N」 줄 걷음 */after:function(R){try{if(typeof pvWatch==='function')pvWatch(R)}catch(e){}},
    onSec:function(sec){var w=b.querySelector('#gguwSec'),wm=b.querySelector('#gguwMk');if(!w||!wm)return;wm.innerHTML=g3SecMark(sec.id,String(sec.id)===String(secId)?markId:'');kx(wm);var c=b.querySelector('.gguh .cd'),u=b.querySelector('.gguh .un');if(c)c.textContent=sec.id;if(u)u.textContent=sec.t;var m=w.querySelector('.g3mk');w.scrollTop=m?Math.max(0,m.offsetTop-8):0}})}}catch(e){console.warn('gguw 밀기',e)}}
/* 그 절 이론(물리 목차 THEORY)을 그리고 블록(^id · 볼트 개별 파일 UNITS 에 있음)을 점선으로 — 목차 노트엔 ^id 가 없어 같은 글(★·빈칸·\\ 무시)·같은 그림으로 찾음 · 못 찾으면 개별 파일 절을 그려 그 블록 */
function g3SecMark(secId,id){var ts=(typeof secById==='function')?secById(String(secId)):null,us=null;try{us=UNITS.sec.find(function(x){return String(x.id)===String(secId)})}catch(e){}
  var norm=function(x){return String(x||'').replace(/★/g,'').replace(/\\\\/g,'\\').replace(/\s+/g,'')};
  var grp=[];if(id&&us){var k=us.b.findIndex(function(n){return n.a===id});if(k>=0){var a0=k,a1=k;while(a0>0&&us.b[a0-1].t!=='br')a0--;while(a1<us.b.length-1&&us.b[a1+1].t!=='br')a1++;grp=us.b.slice(a0,a1+1)}}
  var render=function(sec,hit){var d=document.createElement('div');d.innerHTML=secHTML(sec);var box=d.firstElementChild;if(!box)return d.innerHTML;if(!hit.length)return d.innerHTML;
    var kids=[].slice.call(box.children).slice(1),els=[],c=0;sec.b.forEach(function(n,i){var cnt=(n.t==='br'||n.t==='tb')?1:((String(n.x||'')+((n.r||[]).length?'r':'')).trim()?1:0)+(n.g?1:0);var mine=kids.slice(c,c+cnt);c+=cnt;if(hit.indexOf(i)>=0)els=els.concat(mine)});
    if(!els.length)return d.innerHTML;var w=document.createElement('div');w.className='g3mk';els[0].parentNode.insertBefore(w,els[0]);els.forEach(function(e){w.appendChild(e)});return d.innerHTML};
  if(ts&&grp.length){var hit=[];grp.forEach(function(gn){var t=norm(gn.x);ts.b.forEach(function(n,i){if(hit.indexOf(i)>=0)return;if((t&&norm(n.x)===t)||(!t&&gn.g&&n.g===gn.g))hit.push(i)})});
    if(hit.length){hit.sort(function(a,b){return a-b});var all=[];for(var i=hit[0];i<=hit[hit.length-1];i++)all.push(i);return render(ts,all)}}
  if(us&&grp.length){var k2=us.b.indexOf(grp[0]),all2=[];for(var j=k2;j<k2+grp.length;j++)all2.push(j);return render(us,all2)}
  return ts?secHTML(ts):''}
window.g3UseWin=g3UseWin;
document.addEventListener('click',async function(e){
  var t=e.target; if(!t||!t.closest)return; var el;
  if(el=t.closest('[data-g3cqcm]')){e.stopPropagation();var k1=el.getAttribute('data-g3cqcm');G3CMOPEN=(G3CMOPEN==='q|'+k1)?null:'q|'+k1;ggRepaint(k1.split('|')[0]);if(G3CMOPEN){var t1=document.querySelector('[data-g3cqin="'+CSS.escape(k1)+'"]');if(t1)t1.focus()}return}
  if(el=t.closest('[data-g3cqreply]')){e.stopPropagation();var k2=el.getAttribute('data-g3cqreply'),in2=document.querySelector('[data-g3cqin="'+CSS.escape(k2)+'"]'),v2=in2?String(in2.value||'').trim():'';if(!v2)return;(G3CQX.cs[k2]=G3CQX.cs[k2]||[]).push({k:'c_'+Date.now().toString(36),t:v2,ts:Date.now()});await g3CqxSave();ggRepaint(k2.split('|')[0]);var t2=document.querySelector('[data-g3cqin="'+CSS.escape(k2)+'"]');if(t2)t2.focus();return}
  if(el=t.closest('[data-g3cqcd]')){e.stopPropagation();var a3=el.getAttribute('data-g3cqcd').split('|'),k3=a3[0]+'|'+a3[1];G3CQX.cs[k3]=(G3CQX.cs[k3]||[]).filter(function(x){return x.k!==a3[2]});if(!G3CQX.cs[k3].length)delete G3CQX.cs[k3];await g3CqxSave();ggRepaint(a3[0]);return}
  if(el=t.closest('[data-g3cqdel]')){e.stopPropagation();g3CqDelAsk(el.getAttribute('data-g3cqdel'));return}
  if(el=t.closest('[data-g3cm]')){e.stopPropagation();var ck0=el.getAttribute('data-g3cm');G3CMOPEN=(G3CMOPEN===ck0)?null:ck0;ggRepaint(ck0.split('|')[0]);if(G3CMOPEN){var ta0=document.querySelector('[data-ggcin="'+CSS.escape(ck0)+'"]');if(ta0)ta0.focus()}return}
  if(t.closest('.g3r .g3bg,.g3r .g3del,.g3r .g3ed,.g3cmb'))return;   /* 댓글 v37 — ! · x · 고치기 칸은 줄 누름(쓰인 문항 창) 아님 */
  if(el=t.closest('.g3s')){e.stopPropagation();var sug=el.closest('.g3sug');await g3Pick(sug,+el.dataset.i);return}
  if(el=t.closest('[data-g3sel]')){e.stopPropagation();var v0=el.getAttribute('data-g3sel').split('|');g3Sel(v0[0],v0[1]);return}
  if(el=t.closest('[data-g3ty]')){e.stopPropagation();var ty=el.getAttribute('data-g3ty').split('|'),r0=rowByUid(ty[0]);if(!r0)return;var no0=r0[F.NO],cur0=new Set(typeOf(no0));cur0.has(ty[1])?cur0.delete(ty[1]):cur0.add(ty[1]);
    QT[qk(no0)]=TYPES.filter(function(y){return cur0.has(y)});await saveQT();try{syncTypeBtn()}catch(_){}try{if(typeof ndSync==='function')ndSync()}catch(_){}try{ggRepaint(ty[0])}catch(_){try{ggPhysPaint()}catch(__){}}try{navBuild()}catch(_){}return}
  /* 댓글 v50(사용자 01:59 「근거에 쓰인 숫자 클릭했는데 왜 이상한 창 · 이 근거를 쓰는 문제들이 떠야」) — 숫자를 줄 누름(공식·개념 = 절 이론 창)보다 먼저 봄 · 숫자 = 그 근거를 쓴 문항 목록 창 */
  if(el=t.closest('[data-g3use]')){e.stopPropagation();var vu=el.getAttribute('data-g3use').split('|');g3UseWin(vu[0],vu[1],vu[2],{list:true});return}
  if(el=t.closest('[data-g3useq]')){e.stopPropagation();var qu=el.getAttribute('data-g3useq').split('|');g3UseWinQ(qu[0],qu.slice(1).join('|'),{list:true});return}
  if(el=t.closest('[data-g3cq]')){e.stopPropagation();var q=el.getAttribute('data-g3cq').split('|');g3UseWinQ(q[0],q.slice(1).join('|'));return}
  if(el=t.closest('[data-g3cpick]')){e.stopPropagation();var rp=rowByUid(el.getAttribute('data-g3cpick'));var w0=document.getElementById('gguw');if(w0)w0.remove();if(rp)conceptPick(rp);return}
  if(el=t.closest('[data-g3c]')){e.stopPropagation();var v=el.getAttribute('data-g3c').split('|');g3UseWin('c',v[0],v[1]);return}
  if(el=t.closest('[data-g3use]')){e.stopPropagation();var v2=el.getAttribute('data-g3use').split('|');g3UseWin(v2[0],v2[1],v2[2]);return}
  if(el=t.closest('[data-g3pan]')){e.stopPropagation();var v3=el.getAttribute('data-g3pan').split('|');
    var w=document.getElementById('gguw');if(w)w.remove();
    var p=document.getElementById('qp-'+v3[2]+'gg-pan-'+v3[0]+'-'+v3[1]);if(p)p.classList.remove('hide');return}
  if(el=t.closest('[data-g3mv]')){e.stopPropagation();var v4=el.getAttribute('data-g3mv').split('|');
    var list=ggOf(v4[0]).slice(),g=list.find(function(x){return x&&x.k===v4[1]});if(!g)return;
    g.f=v4[2]; if(v4[2]!=='c')delete g.ref; await ggSaveList(v4[0],list); ggRepaint(v4[0]); return}
},true);
/* ── 서랍 — O△X 왼쪽 유형 · 누르면 세 근거 작은 창 ── */
var _tail=ndTail;
ndTail=function(no){
  var base=_tail(no), ty=(typeof typeOf==='function'?typeOf(no):[])||[];
  var a=base.indexOf('<b class="ndm'), c=base.indexOf('<b class="ndc');
  var end=c>=0?c:base.length, st=a>=0?a:end;
  var marks=base.slice(st,end);
  if(!ty.length&&!marks)return base;
  /* 댓글 v39(사용자 22:27 「근거 있는 곳에만 아래 점선 밑줄」) — 근거(세 칸 항목 · 이은 개념)가 있는 문항만 O△X 점선 밑줄 */
  var hasG=false;try{var r0=rec(no),u0=r0?GGU(r0):'';hasG=!!u0&&(ggOf(u0).filter(Boolean).length>0||g3Cq(u0).length>0)}catch(e){}
  return base.slice(0,st)+'<span class="ndox'+(hasG?' g3has':'')+'" data-ox="'+no+'">'+(ty.length?'<i class="ndty">'+esc(ty.join('·'))+'</i>':'')
    +marks+'</span>'+base.slice(end)};
var G3P=null;
function g3PopClose(){var p=document.getElementById('g3Pop');if(p)p.remove();
  document.querySelectorAll('#ndList .ndox.on').forEach(function(x){x.classList.remove('on')});G3P=null;
  document.removeEventListener('pointerdown',g3PopOut,true)}
function g3PopOut(e){var p=document.getElementById('g3Pop');if(p&&!p.contains(e.target)&&!(e.target.closest&&e.target.closest('.ndox')))g3PopClose()}
function g3PopToggle(no,ox){
  if(G3P===no){g3PopClose();return}
  g3PopClose(); try{ndPopClose()}catch(e){} G3P=no; ox.classList.add('on');
  var r=rec(no), uid=GGU(r), list=ggOf(uid), by={t:[],c:[],w:[]}, cq=g3Cq(uid);
  list.forEach(function(g){if(g)by[g3f(g)].push(g)});
  cq.forEach(function(c){by.c.push({__cq:c})});
  var p=document.createElement('div');p.id='g3Pop';
  /* 댓글 v29(사용자 19:59 「서랍에서 몇 번인지 다 보이니까 이 줄 없애」) — 머리 줄 「코드 · N번」 걷음 */
  p.innerHTML=''
    /* 댓글 v3(사용자 14:18 「팝업에서 트리거·공식개념 같은 글자 없이」) — 칸 이름 없이 칸 차례(트리거 → 공식·개념 → 주의점)로 · 빈 칸은 안 세움 · 칸 사이 얇은 선 */
    +((list.length||cq.length)?G3F.filter(function(x){return by[x[0]].length}).map(function(x){var f=x[0];
      return '<div class="g3pf" data-f="'+f+'">'+by[f].map(function(g){
          /* 댓글 v29(사용자 19:59 · 20:01 「공식·개념 그 자체 누르면 속한 목차를 작게 호버처럼 · 오른쪽 위 <> 누르면 문제 창에서 공식·개념 누르면 나오는 창처럼」 · 「1.2.6 숫자는 지워」) — 절 번호 걷음 · 누름 = 목차 말풍선 */
          /* 댓글 v35(사용자 21:58 「오른쪽에 근거 창에서처럼 작게 이 개념 쓰인 문항 숫자」) — 근거 줄과 같은 셈 · 같은 규칙(2 넘어야 보임) */
          if(g.__cq){var nq=g3QUsers(g.__cq,g.__cq.k);if(nq.indexOf(uid)<0)nq.push(uid);return '<div class="it g3cqp g3pc" data-g3pc="'+ea('q|'+uid+'|'+g.__cq.k)+'" data-sec="'+ea(g.__cq.n||'')+'">'+g3CqBody(g.__cq)+(nq.length>=1?'<i class="g3pn" title="이 개념을 쓴 문항 '+nq.length+'">'+nq.length+'</i>':'')+'</div>'}
          if(f==='c'&&g.ref){var b=g3Blk(g.ref);if(b){var nc=g3Users('c',g3Key(g)).length;return '<div class="it g3pc" data-g3pc="'+ea('c|'+uid+'|'+g.k)+'" data-sec="'+ea(g3SecName(b.sec))+'">'+g3T(b.lines[0].x)+(nc>=1?'<i class="g3pn" title="이 칸을 쓰는 문항 '+nc+'">'+nc+'</i>':'')+'</div>'}}
          return '<div class="it">'+ggMath(ggFlat(g))+'</div>'}).join('')+'</div>'}).join(''):'<div class="g3pf"><span class="none">근거 없음</span></div>')
    ;   /* 댓글 v5(사용자 14:42 「문제는 서랍에서 누르면 됨 · 열기 없애」) — 「열기」 걷음 */
  p.onclick=function(e){e.stopPropagation();var go=e.target.closest('.g3pgo');if(go){var a=go.getAttribute('data-g3pc').split('|');g3PopClose();
      if(a[0]==='q')g3UseWinQ(a[1],a.slice(2).join('|'));else g3UseWin('c',a[1],a.slice(2).join('|'));return}
    var pn=e.target.closest('.g3pn');if(pn){var it0=pn.closest('.g3pc');if(it0){var a2=it0.getAttribute('data-g3pc').split('|');g3PopClose();   /* v50 — 작은 창 쓰인 수 누름 = 근거 줄 숫자와 같은 문항 목록 창 */
      if(a2[0]==='q')g3UseWinQ(a2[1],a2.slice(2).join('|'),{list:true});else g3UseWin('c',a2[1],a2.slice(2).join('|'),{list:true});return}}
    var it=e.target.closest('.g3pc'),old=p.querySelector('.g3ptip');if(old){var same=old.__it===it;old.remove();if(same)return}if(!it)return;
    var tp=document.createElement('div');tp.className='g3ptip';tp.__it=it;tp.innerHTML='<span class="t">'+esc(it.getAttribute('data-sec')||'')+'</span><button type="button" class="g3pgo" title="창으로" data-g3pc="'+ea(it.getAttribute('data-g3pc'))+'">&lt;&gt;</button>';
    it.appendChild(tp)};
  document.body.appendChild(p);
  var rr=ox.getBoundingClientRect(), dr=document.getElementById('navdr').getBoundingClientRect(), w=p.offsetWidth;
  p.style.left=Math.max(8,Math.min(dr.right+6,window.innerWidth-w-8))+'px';
  var top=(dr.right+6+w>window.innerWidth-8)?rr.bottom+4:rr.top-6;
  p.style.top=Math.max(8,Math.min(top,window.innerHeight-p.offsetHeight-8))+'px';
  setTimeout(function(){document.addEventListener('pointerdown',g3PopOut,true)},0)}
window.g3PopToggle=g3PopToggle;
/* O△X 누름은 창(window) 잡기 단계에서 먼저 받는다 — 폰은 서랍 줄 누름이면 서랍을 접는 문서 잡기 손이 있어(앱) 그 앞에서 멈춤 */
window.addEventListener('click',function(e){var ox=e.target&&e.target.closest&&e.target.closest('#ndList .ndox');if(!ox)return;
  e.stopPropagation();e.preventDefault();g3PopToggle(+ox.dataset.ox,ox)},true);
(function(){var L=document.getElementById('ndList');if(!L)return;var old=L.onclick;
  L.onclick=function(e){var ox=e.target.closest('.ndox');if(ox){e.stopPropagation();g3PopToggle(+ox.dataset.ox,ox);return}
    var rw=e.target.closest('.ndrow');if(rw){var rn=+rw.dataset.no,vh=document.getElementById('view').classList.contains('hide');if(vh||rn!==VNO)window.G3CMP=e.target.closest('.ndno')?rn:null}   /* v18 — 서랍 번호 = 비교 · uid(제목 줄) = 새로 풀기 */
    return old?old.call(this,e):undefined}})();
/* ── 서랍 🔍 오른쪽 [상/중/하] 필터 하나 — 첫 화면 난이도(FL.lv) 하나를 같이 씀 · 깔때기 누름 = 작은 고르개(상 · 중 · 하 · 다시 누르면 풀림)
   (서랍 머리 폭 235 에 셋을 늘어놓으면 24px 넘침 = 잰 값 → 단추 하나 · 고른 동안은 그 글자) */
var FUN='<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"><path d="M3 5h18l-7 8v6l-4 2v-8z"/></svg>';
function g3LvSync(){var b=document.getElementById('ndLv');if(!b)return;
  b.classList.toggle('on',!!FL.lv);b.innerHTML=FL.lv?esc(FL.lv):FUN;b.title=FL.lv?('난이도 '+FL.lv+'만 · 누르면 바꾸기'):'난이도 상·중·하';
  document.querySelectorAll('#ndLvPop .ndlv').forEach(function(x){x.classList.toggle('on',FL.lv===x.dataset.lv)})}
function g3LvPopClose(){var p=document.getElementById('ndLvPop');if(p)p.remove();document.removeEventListener('pointerdown',g3LvOut,true)}
function g3LvOut(e){var p=document.getElementById('ndLvPop');if(p&&!p.contains(e.target)&&e.target.id!=='ndLv'&&!(e.target.closest&&e.target.closest('#ndLv')))g3LvPopClose()}
function g3LvPop(btn){
  if(document.getElementById('ndLvPop')){g3LvPopClose();return}
  var p=document.createElement('div');p.id='ndLvPop';
  p.innerHTML=['상','중','하'].map(function(v){var n=DATA.filter(function(r){return !isC(r)&&String(r[F.LV]||'')===v}).length;
    return '<button type="button" class="ndlv" data-lv="'+v+'">'+v+'<i>'+n+'</i></button>'}).join('');
  p.onclick=function(e){e.stopPropagation();var x=e.target.closest('.ndlv');if(!x)return;var v=x.dataset.lv;
    FL.lv=(FL.lv===v?'':v);draw();try{navBuild()}catch(_){};g3LvSync()};
  document.body.appendChild(p);
  var r=btn.getBoundingClientRect();p.style.top=Math.round(r.bottom+4)+'px';
  p.style.left=Math.round(Math.max(8,Math.min(r.left-p.offsetWidth/2+r.width/2,window.innerWidth-p.offsetWidth-8)))+'px';
  g3LvSync(); setTimeout(function(){document.addEventListener('pointerdown',g3LvOut,true)},0)}
function g3Lv(){
  var sb=document.querySelector('#navdr .ndhead .ndsrch'); if(!sb)return false;
  if(document.getElementById('ndLv'))return true;
  var b=document.createElement('button');b.type='button';b.id='ndLv';b.className='ndlvb';
  b.onclick=function(e){e.stopPropagation();g3LvPop(b)};
  sb.after(b); g3LvSync(); return true}
var _draw=draw; draw=function(){var r=_draw.apply(this,arguments);try{g3LvSync()}catch(e){}return r};
var _pw=pwChips; pwChips=function(){var r=_pw.apply(this,arguments);try{g3Lv()}catch(e){}return r};
(function poll(n){if(g3Lv()||n>200)return;setTimeout(function(){poll(n+1)},300)})(0);
window.g3LvPop=g3LvPop;

/* 댓글 v16(사용자 16:42 「제목은 옆이 잘려 있지만 터치하면 전체 제목이 팝업은 아니지만 팝업처럼 글씨가 보이도록」) — 잘린 제목을 누르면 제목 바로 아래 말풍선 글(창 아님 · 단추 없음) · 다시 누르거나 다른 데 누르면 사라짐 */
function g3TipHide(){var t=document.getElementById('g3Tip');if(t)t.remove()}
window.addEventListener('click',function(e){var tt=e.target&&e.target.closest&&e.target.closest('#view .vtop .title');
  if(!tt){if(!(e.target.closest&&e.target.closest('#g3Tip')))g3TipHide();return}
  var t1=document.getElementById('vT1');if(!t1)return;
  if(document.getElementById('g3Tip')){g3TipHide();return}
  if(t1.scrollWidth<=t1.clientWidth+1)return;   /* 안 잘렸으면 그대로 */
  var b=t1.getBoundingClientRect(),d=document.createElement('div');d.id='g3Tip';d.textContent=t1.textContent;document.body.appendChild(d);
  var W=Math.min(innerWidth-16,Math.max(b.width,240));d.style.maxWidth=W+'px';
  var x=Math.max(8,Math.min(b.left,innerWidth-8-d.offsetWidth));d.style.left=x+'px';d.style.top=(b.bottom+4)+'px'},true);
window.addEventListener('pointerdown',function(e){if(!(e.target.closest&&(e.target.closest('#g3Tip')||e.target.closest('#view .vtop .title'))))g3TipHide()},true);

/* 댓글 v17(사용자 17:13 「연결 링크 만들고 그 창 눌렀는데 이 창 크기가 정상이냐 · 어떤 불편함 있을지 고려 안 해?」) — 나란히 띄운 멈춘 문항 창(.vpin)
   잼(PC 1100 · 서랍 펴짐): 창 432×784 = 화면 세로 통째 · 그림 = 쪽 통째(1536×2171)를 폭 432 로 줄여 문제 글이 위 1/3 에 작게 · 아래는 빈칸·QR·꼬리말 · 「답 ②」 가 가리개 없이 보임 · 폰은 위 칸 370 중 문제 글 ≈150
   고침: ① 그림 = 쪽에서 문제 덩어리만 오려 냄(쪽 맨 위 글 ~ 가장 큰 빈 틈 앞 · 좌우 여백 걷음 · 필기도 같이) → 같은 폭에서 글자 ≈1.5 배 ② 창 높이 = 머리 + 오린 그림 높이(칸 높이 넘으면 칸 높이) ③ 가리개가 켜져 있으면 그 자리를 그림에서도 가림
   ④ 위아래로 쌓인 칸(폰)은 줄어든 만큼 큰 창을 위로 늘림 */
window.g3Crop=function(cv){try{var W=cv.width,H=cv.height;if(!W||!H)return cv;var sw=Math.min(400,W),sh=Math.round(H*sw/W);
  var s=document.createElement('canvas');s.width=sw;s.height=sh;var g=s.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,sw,sh);g.drawImage(cv,0,0,sw,sh);
  var d=g.getImageData(0,0,sw,sh).data,dk=function(i){return d[i]+d[i+1]+d[i+2]<600},x,y,i;
  var seg=[],y0=-1;for(y=0;y<sh;y++){var c=0;for(x=0;x<sw;x++)if(dk((y*sw+x)*4)){c++;break}if(c){if(y0<0)y0=y}else if(y0>=0){seg.push([y0,y-1]);y0=-1}}if(y0>=0)seg.push([y0,sh-1]);
  if(seg.length<2)return cv;var bi=-1,bg=0;for(i=1;i<seg.length;i++){var gp=seg[i][0]-seg[i-1][1];if(gp>bg){bg=gp;bi=i}}
  if(bg<sh*0.1)return cv;var top=seg[0][0],bot=seg[bi-1][1],xl=sw,xr=-1;
  for(y=top;y<=bot;y++)for(x=0;x<sw;x++)if(dk((y*sw+x)*4)){if(x<xl)xl=x;if(x>xr)xr=x}
  if(xr<0)return cv;var pad=Math.round(sw*0.03);xl=Math.max(0,xl-pad);xr=Math.min(sw-1,xr+pad);top=Math.max(0,top-pad);bot=Math.min(sh-1,bot+pad);
  var k=W/sw,cx=Math.floor(xl*k),cy=Math.floor(top*k),cw=Math.min(W-cx,Math.ceil((xr-xl+1)*k)),ch=Math.min(H-cy,Math.ceil((bot-top+1)*k));
  var o=document.createElement('canvas');o.width=cw;o.height=ch;var og=o.getContext('2d');og.drawImage(cv,cx,cy,cw,ch,0,0,cw,ch);return o}catch(e){return cv}};
window.g3MaskSnap=function(cv){try{var m=document.getElementById('mask'),pc=document.getElementById('pdfc');if(!m||!pc||m.classList.contains('hide'))return;
  var pr=pc.getBoundingClientRect(),mr=m.getBoundingClientRect();if(!pr.width||!mr.width)return;var sx=cv.width/pr.width,sy=cv.height/pr.height,g=cv.getContext('2d');
  g.fillStyle='#fff';g.fillRect((mr.left-pr.left)*sx,(mr.top-pr.top)*sy,mr.width*sx,mr.height*sy)}catch(e){}};
window.g3PinFit=function(b){try{if(b.dataset.fit!=='1')return;var p=b.querySelector('.panel'),im=b.querySelector('.vpb img'),hd=b.querySelector('.vph'),vb=b.querySelector('.vpb');if(!p||!im||!im.naturalWidth||!vb)return;
  var r=p.getBoundingClientRect(),h0=r.height,want=Math.max(200,Math.min(Math.max(200,Math.floor(innerHeight/3)),Math.ceil((hd?hd.offsetHeight:30)+(vb.clientWidth||r.width)*im.naturalHeight/im.naturalWidth+2)));   /* 하한 200 = 문항 창 하한(vPlace) — 눌러 살아 있는 창이 돼도 크기 같음 */
  if(want<h0-4){b._g3h0=h0;p.style.height=want+'px';var k=b.dataset.k;if(typeof WIN!=='undefined'&&WIN[k])WIN[k].h=want}
}catch(e){}};
/* 큰 창으로 되돌릴 때(vSwap) 줄어든 높이를 물려받지 않게 — 자리는 멈춘 창 그대로 · 높이는 줄이기 전 칸 높이 */
window.g3PinSt=function(b){try{var w=(typeof WIN!=='undefined')&&WIN[b.dataset.k];if(!w)return null;return {l:w.l,t:w.t,w:w.w,h:w.h}}catch(e){return null}};
/* 좁은 세로 화면(폰 · vCells 가 한 줄로 쌓는 때) — 멈춘 창들을 위에서부터 붙여 쌓고 큰 창은 그 아래 끝까지 */
window.g3Relayout=function(){try{var c=vCells(1)[0];if(!(c.w<c.h&&c.w<600))return;
  var ps=[].slice.call(document.querySelectorAll('.vpin')).sort(function(a,b){return a.querySelector('.panel').getBoundingClientRect().top-b.querySelector('.panel').getBoundingClientRect().top}),y=c.t;
  ps.forEach(function(b){var p=b.querySelector('.panel'),h=Math.round(p.getBoundingClientRect().height);p.style.left=c.l+'px';p.style.top=y+'px';p.style.width=c.w+'px';
    if(typeof WIN!=='undefined')WIN[b.dataset.k]={l:c.l,t:y,w:c.w,h:h};y+=h});
  var v=document.getElementById('view');if(ps.length&&v&&!v.classList.contains('hide')&&v.classList.contains('win')){var vr=v.getBoundingClientRect();vPlace({l:c.l,t:y,w:c.w,h:Math.min(Math.round(vr.height),c.t+c.h-y)})}}catch(e){}};

/* 댓글 v18(사용자 17:42 「목록 카드 · 서랍 uid 누름만 새로 풀기 = 자동 다음 회독 · 필기 안 보임 / 연결 · 번호 누름 = 비교 = 바로 전 회독 필기 보임 / 멈춘 창 눌러 큰 창 = 필기 · 근거 · 다른 회독 필기 다 됨」)
   G3CMP = 비교로 연 문항 번호(그 열람 동안만 · 다른 문항으로 새 열람이면 지움 — showProblem 패치) · 비교로 여는 길: 서랍 .ndno(vSwapOpen · 창 없으면 openView) · 🔗 연결 창 이은 문항(vSwapOpen) · 근거 「그 문제 보기」 ↗(창 떠 있으면 나란히) */
window.G3CMP=null;
window.addEventListener('click',function(e){var t=e.target;if(!t||!t.closest)return;
  if(t.closest('#list')){window.G3CMP=null;return}
  var g=t.closest('[data-gguugo]');if(!g)return;var r=rowByUid(g.getAttribute('data-gguugo'));if(!r)return;var no=r[F.NO];
  var v=document.getElementById('view');
  if(v&&!v.classList.contains('hide')&&VNO===no){e.stopPropagation();e.preventDefault();try{pwTop(v)}catch(_){}return}   /* v48 — 본창이 이미 그 문항이면 새 열람(회독) 안 만들고 본창을 맨 위로 */
  if(v&&!v.classList.contains('hide')&&VNO&&VNO!==no){e.stopPropagation();e.preventDefault();vSwapOpen(no);return}   /* v20 — 그 문항을 본창 옆에 · 댓글 v53(사용자 12:28 「열려 있게 해 줘」) — 쓰인 문항 창은 닫지 않음(비슷한 문제 여럿 이어 보기 · 옛 v20 = 닫음) */
  window.G3CMP=no},true);

/* 댓글 v20(사용자 17:55 「PA0604 로 본창 열고 숫자로 63 창 열었는데 왜 갑자기 창 크기가 뒤바뀌어? · 본창 열 때 크기 좀 줄여 · 작은 상태로」)
   잼(옛 v19 · PC 1100 · 서랍 펴짐): 본창 66 = 792×688 가운데 → 숫자 63 누름(vSwapOpen) → 화면을 칸 둘로 다시 나눠 66 = 왼 칸 멈춘 창(432×203) · 63 = 오른 칸 본창(432×800) — 본창이 새 문항으로 갈리고 크기·자리도 바뀜
   고침: ① 숫자 · 연결 · ↗ 로 여는 비교 문항 = 본창을 건드리지 않고 그 문항 쪽을 따로 그려(쪽 + 바로 전 회독 필기 + 답 가리개 · 문제 덩어리만) 본창 옆 빈 자리(넓은 쪽 · 폭 ≤480)에 작은 창으로
   ② 작은 창을 누르면 = 본창 자리·크기 그대로 내용만 바뀜(그 문항 = 비교 열람 · 옛 본창 내용 = 작은 창 자리) ③ PC 본창 첫 크기 = 폭 46 %(≤600) · 높이 86 % · 서랍 바로 오른쪽 · 기억 열쇠 jagwa.win.view2(옛 큰 크기 기억은 안 읽음) */
function g3TitleOf(no){var r=rec(no);if(!r)return no+'번';return (r[F.VLT]?'V'+r[F.VLT]+' ':'')+no+' '+r[F.CODE]+r[F.LV]+' · '+((typeof pnFix==='function'&&pnFix(r))||titleOf(r))}
async function g3Render(no){try{
  var r=rec(no),loc=locate(r),cv=document.createElement('canvas'),R=null,g;
  if(loc.id==='IMG'){var im=await new Promise(function(ok){var x=new Image();x.onload=function(){ok(x)};x.onerror=function(){ok(null)};x.src='img/'+loc.img+'.jpg'});if(!im)return '';
    cv.width=im.naturalWidth;cv.height=im.naturalHeight;g=cv.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,cv.width,cv.height);g.drawImage(im,0,0);R={W:cv.width,H:cv.height,rot:0,scale:1}}
  else{var buf=await get('pdf',loc.id);if(!buf)return '';var d=await pdfjsLib.getDocument({data:buf.slice(0)}).promise;var page=await d.getPage(Math.min(loc.page,d.numPages));
    var rot=(SET.rot&&SET.rot[loc.id])||0,base=page.getViewport({scale:1,rotation:rot}),sc=1400/base.width,vp=page.getViewport({scale:sc,rotation:rot});
    cv.width=Math.round(vp.width);cv.height=Math.round(vp.height);g=cv.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,cv.width,cv.height);
    await pdfRender(page,{canvasContext:g,viewport:vp});R={W:cv.width,H:cv.height,rot:rot,scale:sc};
    if(SET.mask){try{var own=MPOS[qk(no)],M=own||await detectAnswer(page);if(M){var f=own?1:(SET.maskH||1),a=g3Px(R,M.u,M.v),c=g3Px(R,M.u+M.w,M.v+M.h*f);
      g.fillStyle='#fff';g.fillRect(Math.min(a[0],c[0]),Math.min(a[1],c[1]),Math.max(20,Math.abs(c[0]-a[0])),Math.max(20,Math.abs(c[1]-a[1])))}}catch(e){}}}
  var ink=await get('ink',inkK(no));if(ink){var li=-1;Object.keys(ink).forEach(function(k){if((ink[k]||[]).length&&+k>li)li=+k});
    if(li>=0)(ink[li]||[]).forEach(function(s){if(!s.p||s.p.length<2)return;g.save();g.globalAlpha=s.hl?0.32:1;g.strokeStyle=s.c;g.lineWidth=(s.hl?9:s.w)*R.scale/2;g.lineCap=s.hl?'butt':'round';g.lineJoin='round';g.beginPath();
      for(var i=0;i<s.p.length;i+=2){var q=g3Px(R,s.p[i],s.p[i+1]);i?g.lineTo(q[0],q[1]):g.moveTo(q[0],q[1])}g.stroke();g.restore()})}
  return g3Crop(cv).toDataURL('image/jpeg',0.82)}catch(e){console.warn('g3Render',e);return ''}}
function g3Px(R,u,v){var W=R.W,H=R.H;if(R.rot===90)return[(1-v)*W,u*H];if(R.rot===180)return[(1-u)*W,(1-v)*H];if(R.rot===270)return[v*W,(1-u)*H];return[u*W,v*H]}
window.g3CmpOpen=async function(no){no=+no;
  /* 댓글 v22(사용자 18:51 「비교창을 누른다고 본창이랑 위치가 뒤바뀌는 게 짜증 · 본창 보고 있을 때는 비교창은 그림으로 놔두면 되잖아」)
     창은 제자리·제 크기 그대로 — 누른 창이 그 자리에서 살아 있는 창(필기 · 근거 · 회독 · O△X)이 되고 나머지는 그 자리에서 그림 · 살아 있는 앱은 늘 하나(같은 기록을 둘이 따로 저장하는 일 없음) */
  var ex=[].slice.call(document.querySelectorAll('.vpin')).filter(function(x){return +x.dataset.no===no})[0];if(ex){try{pwTop(ex)}catch(e){}return}
  var v=document.getElementById('view');
  if(!v||v.classList.contains('hide')||!VNO){window.G3CMP=no;return openView(no,navList())}
  if(no===VNO)return;
  if(!v.classList.contains('win')){window.G3CMP=no;VNO=no;return showProblem()}
  var url=await g3Render(no);if(!url)return;
  var m=vRect(),c=vCells(1)[0],L=c.l,Rr=c.l+c.w,lw=m.l-L,rw=Rr-(m.l+m.w),H3=Math.max(160,Math.floor(innerHeight/3)),rect;
  if(c.w<c.h&&c.w<600)rect={l:L,t:c.t,w:c.w,h:H3};
  else if(Math.max(lw,rw)>=280){if(rw>=lw)rect={l:m.l+m.w,t:m.t,w:Math.min(480,rw),h:H3};else{var w0=Math.min(480,lw);rect={l:m.l-w0,t:m.t,w:w0,h:H3}}}
  else{var w1=Math.min(420,Math.round(c.w*0.45));rect={l:Rr-w1,t:m.t,w:w1,h:H3}}
  /* 댓글 v52(사용자 11:30 「진짜 앱 쓰는 데 불편할 점」 · 채팅 잼) — 비교 창을 여럿 열면 모두 같은 자리(본창 옆 위)에 겹쳐 앞 창이 통째로 가려짐 → 머리 줄만큼(30px) 아래로 비껴 쌓음(제목은 다 보임 · 누르면 그 창이 맨 위) */
  var occ=[].slice.call(document.querySelectorAll('.vpin .panel')).map(function(p){return p.getBoundingClientRect()}),kk=0;
  while(kk<8&&occ.some(function(q){return Math.abs(q.left-rect.l)<24&&Math.abs(q.top-rect.t)<24})){rect.t+=30;kk++}
  if(rect.t+120>innerHeight)rect.t=Math.max(c.t,innerHeight-rect.h);
  window.G3PINURL=url;window.G3PINTTL=g3TitleOf(no);window.G3PINFIT=1;
  var b=vPinAt(no,rect);window.G3PINFIT=0;if(b){b.dataset.cmp='1';b.dataset.seen='0';b.dataset.ratio='0';try{pwTop(b)}catch(e){}}
  if(c.w<c.h&&c.w<600){var vr=vRect();if(vr.t<rect.t+rect.h)vPlace({l:vr.l,t:rect.t+rect.h,w:vr.w,h:vr.h})}};

/* 사용자 18:07 「어떤 팝업창이든 처음 뜰 때 화면의 1/3 이상 길이 차지하지 않게 · 반드시 · 길게 뜨면 일일이 창 조절해야」 — 떠 있는 창(makeFloat · 패치) · 문항 창(openView · 아래) · 멈춘 창(g3PinFit) · 모달 판(CSS) 다 */
window.g3CapView=function(){var v=document.getElementById('view');if(!v||!v.classList.contains('win'))return;var H=Math.max(200,Math.floor(innerHeight/2)),   /* 사용자 18:24 「본창은 화면 1/2」 */r=v.getBoundingClientRect();
  if(r.height>H+1)vPlace({l:Math.round(r.left),t:Math.round(r.top),w:Math.round(r.width),h:H})};
window.G3={blocks:g3Blocks,find:g3BlkFind,push:g3Push,users:g3Users};
/* 댓글 v28(사용자 20:01 개념 창 「이론 단추 왼쪽 밀기 개념 덮개 모습으로 · 여기선 그 개념이 메인 · 오른쪽 밀기 = 목차 목록 · 왼쪽 밀기 = 이론 단추 메인이던 창」) —
   개념 창(conceptSheet · 곁창 'concept') = 이론 창(thcDecor)의 역할을 바꾼 꼴: 본문 = 이 문항에 이은 개념 카드(볼트 블록 그대로 · 쓰인 문제 번호 · 옵시디언 · 개념 연결 고치기) ·
   오른쪽 밀기 = 왼쪽 목차 덮개(누르면 그 절 이론을 오른쪽 덮개로) · 왼쪽 밀기 = 오른쪽 이론 덮개(이론 창 본문 = secsFor 첫 절) · 반대 밀기·바깥 = 닫힘 · 옛 탭 줄(블록 번호 「b5f68d」) 걷음 */
function g3ConSheet(startKey,r){try{if(typeof THEORY==='undefined'||!THEORY.sec||typeof conceptsOf!=='function')return false}catch(e){return false}
  var list=conceptsOf(r);if(!list.length){conceptPick(r);return true}
  var b=document.createElement('div');b.className='sheet thsheet thc g3cw';
  b.innerHTML='<div class="panel"><h2>개념 · '+esc(String(r[F.CODE]||''))+'</h2>'+list.map(function(cb){var qs=(CQ[cb.k]||[]).slice().sort(function(a,z){return a-z});
      return '<div class="thcCon'+(cb.k===startKey?' on':'')+'" data-k="'+ea(cb.k)+'">'+(cb.n?'<div class="thcCn">'+esc(cb.n)+'</div>':'')+'<div class="g3cwb">'+g3CqBody(cb)+'</div>'
        +'<div class="thcQs">'+qs.map(function(no){return '<span class="thcQ'+(no===VNO?' me':'')+'" data-no="'+no+'">'+no+'</span>'}).join('')
        +'<span class="thcObs g3obs" data-i="'+ea(cb.i||'')+'" title="옵시디언에서 이 개념 열기" aria-label="옵시디언에서 이 개념 열기">◆</span></div></div>'}).join('')
    +'</div>';   /* 댓글 v34(사용자 21:54 「개념 연결 고치기 없애」) */
  document.body.appendChild(b);kx(b);g3DrDown();
  g3CwDecor(b,r,startKey);return true}
function g3CwDecor(s,r,startKey,secId,opt){var p=s.querySelector('.panel');if(!p)return;opt=opt||{};
  var secs=r?secsFor(r):[],cur=(secId&&secById(String(secId)))||(secs[0]||THEORY.sec[0]),side=null;
  var scrim=document.createElement('div');scrim.className='thcScrim';
  var L=document.createElement('div');L.className='thcSide thcL';
  var R=document.createElement('div');R.className='thcSide thcR g3cwR';
  s.appendChild(scrim);s.appendChild(L);s.appendChild(R);if(opt.rHTML){R.innerHTML=opt.rHTML();if(opt.after)opt.after(R)}
  var place=function(){var bb=p.getBoundingClientRect(),w=Math.round(Math.min(bb.width*0.86,340));
    scrim.style.cssText='left:'+bb.left+'px;top:'+bb.top+'px;width:'+bb.width+'px;height:'+bb.height+'px';
    L.style.left=bb.left+'px';R.style.left=(bb.right-w)+'px';[L,R].forEach(function(x){x.style.top=bb.top+'px';x.style.height=bb.height+'px';x.style.width=w+'px'})};
  var close=function(){side=null;s.classList.remove('thcOnL','thcOnR')};
  var fillL=function(){var groups={};THEORY.sec.forEach(function(x){var g=x.id.split('.')[0];(groups[g]=groups[g]||[]).push(x)});var me=cur?cur.id:'';
    L.innerHTML=Object.keys(groups).sort().map(function(g){var big=(typeof TH_BIG!=='undefined'&&TH_BIG[g])||g;
      return ((groups[g].length===1&&String(groups[g][0].t).replace(/\s/g,'')===String(big).replace(/\s/g,''))?'':'<div class="grouphd">'+esc(big)+'</div>')
        +groups[g].map(function(x){return '<div class="thcRow'+(x.id===me?' on':'')+'" data-sec="'+ea(x.id)+'">'+esc(x.id)+'. '+esc(x.t)+'</div>'}).join('')}).join('');
    kx(L);var on=L.querySelector('.thcRow.on');if(on)on.scrollIntoView({block:'center'})};
  var fillR=function(){R.innerHTML=opt.rHTML?opt.rHTML():(cur?secHTML(cur):'');kx(R);R.scrollTop=0;if(opt.after)opt.after(R)};
  var open=function(k){place();if(k==='L')fillL();else fillR();side=k;s.classList.toggle('thcOnL',k==='L');s.classList.toggle('thcOnR',k==='R')};
  s.__g3cwOpen=open;
  L.onclick=function(e){var x=e.target.closest('.thcRow');if(!x)return;var sec=secById(x.dataset.sec);if(!sec)return;cur=sec;close();if(opt.onSec)opt.onSec(sec);else open('R')};
  var qClick=function(e){var q=e.target.closest('.thcQ');if(q){var no=+q.dataset.no;close();if(no!==VNO)vSwapOpen(no);return true}
    var o=e.target.closest('.thcObs');if(o){location.href=obsFind('^'+o.dataset.i);return true}
    if(e.target.closest('.thcEdit')){s.remove();conceptPick(r);return true}return false};
  p.addEventListener('click',function(e){qClick(e)});
  scrim.onclick=close;
  var sx=0,sy=0,on=false;
  var down=function(e){if(e.button>0)return;sx=e.clientX;sy=e.clientY;on=true};
  var up=function(e){if(!on)return;on=false;var dx=e.clientX-sx,dy=e.clientY-sy;if(Math.hypot(dx,dy)>=10)s.__swiped=Date.now();if(Math.abs(dx)<60||Math.abs(dx)<2*Math.abs(dy))return;
    if(side==='L'){if(dx<0)close();return}if(side==='R'){if(dx>0)close();return}open(dx>0?'L':'R')};
  s.addEventListener('click',function(e){if(Date.now()-(s.__swiped||0)<400){e.stopPropagation();e.preventDefault()}},true);
  s.addEventListener('dragstart',function(e){e.preventDefault()},true);   /* 댓글 v32 — 그림 위에서 밀면 그림 끌기가 시작돼 밀기가 안 됨(마우스) */
  [p,L,R,scrim].forEach(function(el){el.addEventListener('pointerdown',down,true);el.addEventListener('pointerup',up,true);el.addEventListener('pointercancel',function(){on=false},true)});
  if(startKey){var c=p.querySelector('.thcCon.on'),h2=p.querySelector('h2');if(c&&c!==p.querySelector('.thcCon'))setTimeout(function(){p.scrollTop=Math.max(0,c.offsetTop-(h2?h2.offsetHeight:0)-4)},60)}}

function g3TgHTML(uid){var list=ggOf(uid),cq=g3Cq(uid),by={t:[],c:[],w:[]};list.forEach(function(g){if(g)by[g3f(g)].push(g)});
  return '<span class="g3tg">'+G3F.map(function(x){var n=by[x[0]].length+(x[0]==='c'?cq.length:0);
    return '<button type="button" class="'+(x[0]===G3SEL?'on':'')+'" data-g3f="'+x[0]+'" data-g3sel="'+ea(uid+'|'+x[0])+'">'+G3L[x[0]]+(n?'<i>'+n+'</i>':'')+'</button>'}).join('')+'</span>'}
/* 댓글 v29 — 「근거」 누름 = 작은 창(옛 유형 창 자리 · 머리 줄 「N번 유형 ✕」 없음): 1 줄 유형 글자 넷(「근거」 글자 크기 · 누르면 켜고 끔 · 바로 저장) / 2 줄 트리거 · 공식·개념 · 주의점(적는 칸이 쓸 칸) · 바깥 누름 = 닫힘 */
function g3GgPop(no,anc){var o=document.getElementById('tyPop');if(o){if(o.__close)o.__close();else o.remove();return}
  var r=rec(no);if(!r)return;var uid=GGU(r);
  var b=document.createElement('div');b.id='tyPop';b.className='g3ggp';
  var build=function(){if(!b.isConnected&&b.__built)return;b.__built=1;b.innerHTML='<div class="g3ggr">'+g3TyHTML(uid)+'</div><div class="g3ggr">'+g3TgHTML(uid)+'</div>'};
  var out=function(e){if(!b.contains(e.target)&&!(e.target.closest&&e.target.closest('#view .ggline .lb')))close()};
  var close=function(){b.remove();document.removeEventListener('pointerdown',out,true)};b.__close=close;
  b.addEventListener('click',function(){setTimeout(build,80);setTimeout(build,600)});
  build();document.body.appendChild(b);
  var rr=anc?anc.getBoundingClientRect():{left:8,bottom:8,top:8},w=b.offsetWidth,h=b.offsetHeight;
  var l=Math.max(8,Math.min(window.innerWidth-w-8,Math.round(rr.left))),tp=Math.round(rr.bottom+4);if(tp+h>window.innerHeight-8)tp=Math.max(8,Math.round(rr.top-h-4));
  b.style.left=l+'px';b.style.top=tp+'px';setTimeout(function(){document.addEventListener('pointerdown',out,true)},0)}
window.g3GgPop=g3GgPop;window.g3TgHTML=g3TgHTML;

/* 댓글 v30(사용자 21:16 「답 골랐을 때 따로 정답 창 안 떠도 돼 · 정답 정정은 정답 단추 길게 눌렀을 때만 정정 창 · 작게」) —
   OMR 단추 길게 누름(0.55 초 · 10px 안 움직임) = 그 단추 옆 작은 정정 창(머리 줄 없음 · 1 줄 「정답 ③ · 교재 ③」 · 2 줄 ①~⑤ · 고친 것 있으면 「교재 값으로」) · 길게 누른 뒤 따라오는 누름은 채점 안 함 */
var G3LP=0;
function g3AfClose(){var o=document.getElementById('g3Af');if(o){o.remove();document.removeEventListener('pointerdown',g3AfOut,true)}}
function g3AfOut(e){var o=document.getElementById('g3Af');if(o&&!o.contains(e.target))g3AfClose()}
async function g3AfPop(no,btn){g3AfClose();try{await loadAfix()}catch(e){}
  var cur=ansOf(no),raw=String(rawAns(no)||'').trim(),fx=(AFIX||{})[qk(no)];
  var b=document.createElement('div');b.id='g3Af';
  b.innerHTML='<div class="afh">정답 '+(esc(cur.join(','))||'없음')+' · 교재 '+(esc(raw)||'없음')+'</div><div class="afc">'+CIRC5.split('').map(function(c){return '<button type="button" class="'+(cur.indexOf(c)>=0?'on':'')+'" data-af="'+c+'">'+c+'</button>'}).join('')+'</div>'
    +(fx?'<span class="afx" data-afx="1">교재 값으로</span>':'');
  b.addEventListener('click',async function(e){var x=e.target.closest('[data-af]');e.stopPropagation();
    if(x){AFIX[qk(no)]=x.dataset.af;await put('kv','ansfix',AFIX);toast(no+'번 정답을 '+x.dataset.af+' 로 고쳤습니다');g3AfClose();syncOmr();return}
    if(e.target.closest('[data-afx]')){delete AFIX[qk(no)];await put('kv','ansfix',AFIX);toast('교재 값으로 되돌렸습니다');g3AfClose();syncOmr()}});
  document.body.appendChild(b);
  var r=btn.getBoundingClientRect(),w=b.offsetWidth,h=b.offsetHeight;
  var l=Math.max(8,Math.min(window.innerWidth-w-8,Math.round(r.left+r.width/2-w/2))),t=Math.round(r.bottom+6);if(t+h>window.innerHeight-8)t=Math.max(8,Math.round(r.top-h-6));
  b.style.left=l+'px';b.style.top=t+'px';setTimeout(function(){document.addEventListener('pointerdown',g3AfOut,true)},0)}
window.g3AfPop=g3AfPop;window.g3AfClose=g3AfClose;
(function(){var p=document.getElementById('omrPad');if(!p)return;var tm=0,st=null;
  var stop=function(){if(tm){clearTimeout(tm);tm=0}st=null};
  p.addEventListener('pointerdown',function(e){stop();if(e.button>0)return;var bs=[].slice.call(p.querySelectorAll('button[data-omr]'));
    var tb=e.target.closest&&e.target.closest('button[data-omr]');if(!tb)tb=bs.find(function(b){var r=b.getBoundingClientRect();return e.clientX>=r.left&&e.clientX<=r.right&&e.clientY>=r.top-4&&e.clientY<=r.bottom+4})||null;if(!tb)return;
    st={x:e.clientX,y:e.clientY,b:tb};tm=setTimeout(function(){tm=0;if(!st||!VNO)return;G3LP=Date.now();var b0=st.b;st=null;g3AfPop(VNO,b0)},550)},true);
  p.addEventListener('pointermove',function(e){if(st&&Math.hypot(e.clientX-st.x,e.clientY-st.y)>10)stop()},true);
  p.addEventListener('pointerup',function(){if(tm)stop()},true);p.addEventListener('pointercancel',stop,true);
  p.addEventListener('click',function(e){if(G3LP&&Date.now()-G3LP<1500){G3LP=0;e.preventDefault();e.stopImmediatePropagation()}},true);
  p.addEventListener('contextmenu',function(e){if(e.target.closest('button[data-omr]'))e.preventDefault()})})();

/* 댓글 v37 — 근거 줄 항목 길게 누름(0.55 초 · 10px 안 움직임) = 그 자리 고치기: 글 칸 + ✓(Enter = 저장 · Esc = 그만) · 볼트 블록(공식 · ref)은 고칠 글이 없어 안 열림 */
var G3ELP=0;
(function(){var tm=0,st=null;var stop=function(){if(tm){clearTimeout(tm);tm=0}st=null};
  document.addEventListener('pointerdown',function(e){if(st&&e.pointerId!==st.id)return;stop();if(e.button>0)return;var it=e.target.closest&&e.target.closest('#view .g3list .g3r[data-g3k]');if(!it||e.target.closest('.g3bg,.g3del,.gguse,.g3ed,.g3cm'))return;
    st={x:e.clientX,y:e.clientY,it:it,id:e.pointerId};tm=setTimeout(function(){tm=0;if(!st)return;var it0=st.it;st=null;if(g3EditInline(it0))G3ELP=Date.now()},550)},true);
  document.addEventListener('pointermove',function(e){if(st&&e.pointerId===st.id&&Math.hypot(e.clientX-st.x,e.clientY-st.y)>10)stop()},true);
  document.addEventListener('pointerup',function(e){if(tm&&st&&e.pointerId===st.id)stop()},true);document.addEventListener('pointercancel',stop,true);
  document.addEventListener('click',function(e){if(G3ELP&&Date.now()-G3ELP<1200&&e.target.closest&&e.target.closest('#view .g3list')&&!e.target.closest('.g3ed')){G3ELP=0;e.preventDefault();e.stopImmediatePropagation()}},true);
  document.addEventListener('contextmenu',function(e){if(e.target.closest&&e.target.closest('#view .g3list .g3r'))e.preventDefault()},true)})();
function g3EditInline(it){var a=it.getAttribute('data-g3k').split('|'),uid=a[0],k=a[1],g=ggItem(uid,k);if(!g)return false;if(g3f(g)==='c'&&g.ref)return false;
  var tx=it.querySelector('.g3tx');if(!tx)return false;
  var ed=document.createElement('span');ed.className='g3ed';ed.innerHTML='<textarea rows="1"></textarea><button type="button" class="g3ok" title="저장">✓</button>';
  var ta=ed.querySelector('textarea');ta.value=ggFlat(g);tx.replaceWith(ed);ta.focus();try{ta.setSelectionRange(ta.value.length,ta.value.length)}catch(e){}
  var fit=function(){ta.style.height='auto';ta.style.height=ta.scrollHeight+'px'};fit();ta.addEventListener('input',fit);
  var gi=g.i,gfx=g3f(g);var save=async function(){var v=ta.value.trim();if(!v){ggRepaint(uid);return}var list=ggOf(uid),gg=list.find(function(x){return x&&x.k===k})||list.find(function(x){return x&&x.i===gi&&g3f(x)===gfx});if(gg){gg.t=v;delete gg.parts;await ggSaveList(uid,list)}ggRepaint(uid)};
  ed.addEventListener('click',function(e){e.stopPropagation();if(e.target.closest('.g3ok'))save()});
  ed.addEventListener('pointerdown',function(e){e.stopPropagation()});
  ta.addEventListener('keydown',function(e){if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();save()}else if(e.key==='Escape'){e.preventDefault();ggRepaint(uid)}});
  return true}
window.g3EditInline=g3EditInline;


/* 댓글 v45(사용자 23:12 「폰에서 창이 목차 서랍 창 뒤로 뜬다 · 터치한 창이 제일 위로 오게 하기로 했잖아」) — 서랍을 누르면 앱이 서랍을 80 으로 올리고 「곁창·문항 창」 을 누를 때만 내리는데
   이 판이 더한 창(쓰인 문항 창 · 개념 창 · 작은 창들)은 그 목록에 없어 서랍 뒤에 깔렸음 → 이 창들을 열 때 · 누를 때 서랍을 제자리로(내 창이 위) */
function g3DrDown(){var dr=document.getElementById('navdr');if(dr)dr.style.zIndex=''}
window.g3DrDown=g3DrDown;
document.addEventListener('pointerdown',function(e){var t=e.target;if(t&&t.closest&&t.closest('#gguw,.sheet.g3cw,#g3Pop,#tyPop,#g3Af'))g3DrDown()},{capture:true,passive:true});

/* 이은 개념 빼기 확인(근거 지우기 창 꼴 · 작게) — 이 문항 근거에서만 뺌 · 교재 이음·다른 문항 그대로 */
function g3CqDelAsk(key){var a=key.split('|'),uid=a[0],ck=a.slice(1).join('|'),c=(typeof CB!=='undefined')&&CB[ck];var r=rowByUid(uid);if(!r)return;
  var b=document.createElement('div');b.className='sheet';
  b.innerHTML='<div class="panel"><h2>이은 개념 빼기</h2><p>교재가 이어 둔 개념 — 이 문항 근거에서만 뺍니다(다른 문항 · 개념 창 그대로).</p><p><small>'+(c?(c.n?esc(c.n):''):'')+'</small></p><button class="btn red" id="g3cqDo">빼기</button><button class="btn" id="g3cqNo" style="margin-top:6px">닫기</button></div>';
  b.onclick=function(e){if(e.target===b)b.remove()};
  b.querySelector('#g3cqNo').onclick=function(){b.remove()};
  b.querySelector('#g3cqDo').onclick=async function(){var q=qk(r[F.NO]);var L=(G3CQX.hide[q]=G3CQX.hide[q]||[]);if(L.indexOf(ck)<0)L.push(ck);await g3CqxSave();b.remove();ggRepaint(uid);try{navBuild()}catch(_){}};
  document.body.appendChild(b)}
window.g3CqDelAsk=g3CqDelAsk;window.g3Cq=g3Cq;window.g3CqxGet=function(){return G3CQX};
window.g3ConSheet=g3ConSheet;window.g3CmOpen=function(v){G3CMOPEN=v};window.g3SugList=g3SugList;window.g3SecMark=g3SecMark;window.g3Users=g3Users;window.g3Key=g3Key;
/* 댓글 v52(사용자 11:30 「진짜 앱 쓰는 데 불편할 점」 · 채팅 잼) — 근거를 처음 적거나 다 지워도 서랍 O△X 점선 밑줄(v39)이 서랍을 다시 그릴 때까지 안 바뀌던 것 → 근거 다시 그릴 때(ggRepaint) 그 문항 서랍 줄도 바로 */
(function(){if(typeof ggRepaint!=='function')return;var _rp=ggRepaint;
  window.ggRepaint=ggRepaint=function(uid){var r=_rp.apply(this,arguments);try{var row=rowByUid(uid);if(row){var o=document.querySelector('#ndList .ndrow[data-no="'+row[F.NO]+'"] .ndox');if(o)o.classList.toggle('g3has',ggOf(uid).filter(Boolean).length>0||g3Cq(uid).length>0)}}catch(e){}return r}})();

})();
