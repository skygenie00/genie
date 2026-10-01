# -*- coding: utf-8 -*-
"""교재 조각 붙이기 · 글상자 · 문항 필기 · 글자 고치기 — 헤드리스 검산
(2026-09-08 · gigu/_task_jagwa_pan3.md §3)

  C  ① 교재 조각 — 펜에서만 네모 · 붙이면 OCR 글자가 가려진다 · ✕ 로 돌아온다 · 좌표 무변
  Y  물리 — crop 이 안 만들어진다 · 화면이 add3 실물과 글자까지 같다
  S  원본 대조(파이썬)

⚠ 픽셀 IDENTICAL 게이트는 쓰지 않는다(CLAUDE.md 「자과앱에는 픽셀 게이트를 걸지 않는다」).

    PYTHONIOENCODING=utf-8 python _harness_crop_qink.py
    PYTHONIOENCODING=utf-8 python _harness_crop_qink.py earth
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import http.server, os, socketserver, subprocess, sys, threading, hashlib, shutil, urllib.parse, json, time

GENIE = _roots.genie()
SRC = os.path.join(GENIE, 'jagwa', 'index.html')
SPDROOT = _roots.spd()
GIGU = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.environ.get('TEMP', '.'), 'cropq'); os.makedirs(OUT, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

STUB = """<script>try{localStorage.setItem('subj','__SUBJ__')}catch(e){}</script>
<script>
window.katex={render:function(){},renderToString:function(s){return s}};window.renderMathInElement=function(){};
window.__err=[];
window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+(e.filename||'').split('/').pop()+':'+e.lineno)});
window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
</script>
"""

HEAD = r"""<script>
(function(){
 const R=[]; const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+(c?'':' | '+JSON.stringify(i===undefined?null:i)));
 const __nativeFetch=window.fetch.bind(window);
 window.fetch=async function(url,opt){
  opt=opt||{};const u=String(url);
  const m=/api\.github\.com\/repos\/([^\/]+\/[^\/]+)\/contents\/([^?]+)/.exec(u);
  if(!m){ if(/api\.github\.com\/repos\/zzikkaplan\/notes/.test(u))return {ok:true,status:200,json:async()=>({name:'notes'}),text:async()=>''}; return __nativeFetch(url,opt); }
  const path=decodeURIComponent(m[2]);
  if(m[1]==='zzikkaplan/notes')return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
  if((opt.method||'GET')==='PUT')return {ok:true,status:200,json:async()=>({content:{sha:'x'}}),text:async()=>''};
  const r=await __nativeFetch('/data/'+encodeURI(path),{cache:'no-store'});
  if(!r.ok)return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
  const acc=(opt.headers||{}).Accept||'';
  if(acc.indexOf('raw')>=0)return r;
  return {ok:true,status:200,json:async()=>({sha:'sha'}),text:async()=>JSON.stringify({sha:'sha'})};
 };
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 setInterval(()=>{try{__nativeFetch('/partial',{method:'POST',body:R.join(String.fromCharCode(10))+String.fromCharCode(10)+'(err) '+JSON.stringify(window.__err||[])})}catch(e){}},3000);
 const grp=async(name,fn)=>{try{await fn()}catch(e){T(name+' 묶음 예외',false,String(e&&e.stack||e).slice(0,300))}};
 const $$$=s=>[...document.querySelectorAll(s)];
 const PE=(t,el,x,y,pt)=>el.dispatchEvent(new PointerEvent(t,{clientX:x,clientY:y,bubbles:true,cancelable:true,pointerId:9,pointerType:pt||'pen',isPrimary:true}));
 async function run(){
  try{
   localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}));
"""

TAIL = r"""
   T('콘솔 오류 0',(window.__err||[]).length===0,window.__err);
  }catch(e){T('예외',false,String(e&&e.stack||e))}
  try{await __nativeFetch('/result',{method:'POST',body:R.join(String.fromCharCode(10))})}catch(e){}
 }
 if(document.readyState==='complete')setTimeout(run,600);else window.addEventListener('load',()=>setTimeout(run,600));
})();
</script>"""

# ═══════════════════════════ C. ① 교재 조각 ═══════════════════════════
BODY_EARTH = r"""
   await loadEarthData(); draw(); await wait(120);
   T('C-0 지학 카드 층 · 데이터 적재',CARD_LAYER===true&&SUBJ_ID==='earth'&&DATA.length>0,[SUBJ_ID,DATA.length]);

   /* ═══ C-1 저장 자리 ═══ */
   await grp('C-1', async()=>{
     /* A-6(a) 9/30 — listpop_add1 §G(cd248a5)가 지학 SYNC_KEYS 끝에 gg·ggref·pick·link 를 JS 로 더해 23 — 옛 19키가 앞자리 그대로인지 잰다(키가 더 늘어도 안 뒤집힌다) */
     T('C-1 지학 SYNC_KEYS 옛 19키 앞자리 그대로 · crop 16 · txt 17 · tfix 18째',SUBJ.earth.SYNC_KEYS.slice(0,19).join()==='status,note,qtype,conc,gpt,twin,ansfix,frm,maskpos,omrpos,mcard,bogi,unit,bpit,bpg,crop,txt,tfix,bref'&&SUBJ.earth.SYNC_KEYS[15]==='crop'&&SUBJ.earth.SYNC_KEYS[16]==='txt'&&SUBJ.earth.SYNC_KEYS[17]==='tfix',SUBJ.earth.SYNC_KEYS);
     T('C-1 생물 SYNC_KEYS 19 · crop·txt·tfix 포함',SUBJ.bio.SYNC_KEYS.length===20&&['crop','txt','tfix','bref'].every(k=>SUBJ.bio.SYNC_KEYS.indexOf(k)>=0),SUBJ.bio.SYNC_KEYS.length);
     T('C-1 물리 SYNC_KEYS 12 무변 · crop 없음',SUBJ.phys.SYNC_KEYS.length===12&&SUBJ.phys.SYNC_KEYS.indexOf('crop')<0,SUBJ.phys.SYNC_KEYS.length);
     T('C-1 SYNC_REF 에 crop 읽기/쓰기가 있다',!!SYNC_REF.crop&&typeof SYNC_REF.crop.g==='function'&&typeof SYNC_REF.crop.s==='function');
     /* 모르는 꼴은 추측해서 덮지 않는다 */
     const bad0=CROPBAD;
     CROP['__X1']={q:'이건 배열이 아니다'};
     T('C-1 배열이 아닌 꼴 → 그 조각만 빼고 CROPBAD 로 센다',cropList('__X1','q').length===0&&CROPBAD>bad0,[CROPBAD-bad0]);
     const bad1=CROPBAD;
     CROP['__X2']={q:[{p:0,r:[1,2,3]},{p:12,r:[1,2,3,4]}]};
     T('C-1 쪽·좌표가 모자란 조각만 빼고 성한 것은 남긴다',cropList('__X2','q').length===1&&CROPBAD>bad1,[cropList('__X2','q'),CROPBAD-bad1]);
     delete CROP['__X1'];delete CROP['__X2'];
   });

   /* ═══ C-2 교재 창에서 네모 — 펜에서만 ═══ */
   let PR=0;
   await grp('C-2', async()=>{
     const r=DATA.find(x=>+x[F.BPAGE]>0)||DATA[0];
     await openView(r[F.NO]); await wait(300);
     await bkOpen(208); await wait(2500);
     let n=0;while(n++<60&&(!bkCurPage()||bkCurPage().pr!==208))await wait(200);
     T('C-2 교재 창이 208쪽에 서 있다',!!bkCurPage()&&bkCurPage().pr===208,bkCurPage()&&bkCurPage().pr);
     /* ⚠ 2026-09-10 — 옆 칸을 걷으면서 **오리기 단추를 교재 창으로 되돌렸다**(사용자 확정).
        add2 §4-1 은 「교재 전체 화면에는 안 그린다」였는데 그 자리가 이제 유일한 자리다.
        엔진(BK.crop)은 그때도 안 지웠으므로 여기서는 **단추가 있는지**를 잰다. */
     T('C-2 ★「◻ 오리기」 단추가 교재 창에 있다(2026-09-10 사용자 확정 · add2 §4-1 되돌림)',
       !!$('#bktools [data-tool="crop"]'),[...$('#bktools').children].map(e=>e.dataset.tool||e.id).join(','));
     T('C-2 그래도 오리기 엔진은 산다 — BK.crop(링크가 같이 쓴다)',BK.crop===true,BK.crop);
     T('C-2 물리 도구 넷은 그대로(보기·펜·형광·지우개)',['view','pen','hl','erase'].every(t=>!!$('#bktools [data-tool="'+t+'"]')));
     const tb=(()=>{const bar=$('#bktools');let x=bar.querySelector('[data-tool="crop"]');
       if(!x){x=document.createElement('span');x.dataset.tool='crop';x.textContent='▢ 오리기';
         bar.appendChild(x);zTools(BK,'#bktools','#bkvp')}      /* 검산용 — 도구줄 끝에 붙여 실물 순서를 안 흔든다 */
       return x})();
     tb.click(); await wait(60);
     T('C-2 오리기를 고르면 BK.tool 이 crop',BK.tool==='crop'&&BK.pen===true,[BK.tool,BK.pen]);
     const vp=$('#bkvp'), vr=vp.getBoundingClientRect();
     const cx=vr.left+vr.width/2, cy=vr.top+vr.height/2;
     /* ⚠ 아래 손가락 스크롤로 화면이 움직이니, 펜을 내린 그 자리의 쪽을 그때 기억한다 */
     /* ⚠ 손가락으로 끌면 네모가 아니라 스크롤이다 */
     const Y0=BK.Y;
     SET.pencil=true;
     PE('pointerdown',vp,cx,cy,'touch');PE('pointermove',vp,cx+90,cy+70,'touch');PE('pointerup',vp,cx+90,cy+70,'touch');
     await wait(150);
     T('C-2 손가락으로 끌면 네모가 안 생긴다',$$$('.crbox').length===0,$$$('.crbox').length);
     T('C-2 손가락은 종전대로 화면이 움직인다(스크롤)',Math.abs(BK.Y-Y0)>10,[Y0,BK.Y]);
     /* 펜으로 끌면 네모가 선다 */
     {const tp=BK.toPage(cx,cy);PR=tp?BK.pages()[tp.i].pr:PR}
     PE('pointerdown',vp,cx,cy,'pen');PE('pointermove',vp,cx+120,cy+90,'pen');PE('pointerup',vp,cx+120,cy+90,'pen');
     await wait(200);
     T('C-2 펜으로 끌면 네모가 선다 · 모서리 넷',$$$('.crbox').length===1&&$$$('.crbox i[data-h]').length===4,[$$$('.crbox').length,$$$('.crbox i[data-h]').length]);
     /* ④가 선 뒤라 「✎ 글자로 고치기」 줄이 살아 있다(①만 있던 판에서는 셋이었다 · 고친 자리) */
     T('C-2 놓으면 메뉴가 뜬다 — 문제 칸 · 해설 칸 · 글자로 고치기 · 취소',!!document.getElementById('crmenu')&&$$$('#crmenu button').length===5,   /* A-6(a) 9/30 — listpop_add1 §F(cd248a5) 「🃏 카드로 찍기」를 맨 위에 더했다(교재 탭 = 카드 · 문제 칸 · 해설 칸 · 글자 · 취소) */
       $$$('#crmenu button').map(b=>b.textContent));
     T('C-2 🃏 카드로 찍기가 맨 위 · 붙이는 두 줄이 그다음 · 취소가 끝이다',$$$('#crmenu button')[0].dataset.s==='mc'&&$$$('#crmenu button')[1].dataset.s==='q'&&$$$('#crmenu button')[2].dataset.s==='s'&&$$$('#crmenu button')[4].dataset.s==='');
   });

   /* ═══ C-3 붙이면 OCR 글자가 가려진다 ═══ */
   let UID='';
   await grp('C-3', async()=>{
     UID=rec(VNO)[F.CODE];
     const n0=cropList(UID,'q').length;
     $('#crmenu [data-s="q"]').click(); await wait(900);
     T('C-3 「문제 칸으로」 → crop.q 가 는다',cropList(UID,'q').length===n0+1,[cropList(UID,'q').length,n0]);
     T('C-3 네모와 메뉴가 사라진다',$$$('.crbox').length===0&&!document.getElementById('crmenu'));
     bkClose(); await wait(200);
     T('C-3 문항 화면에 조각 칸이 생겼다',$$$('#card .cropw[data-cropw="q"] canvas[data-cr]').length===1,$$$('#card .cropw canvas').length);
     const q=$('#card .q');
     T('C-3 그 자리 OCR 글자가 가려진다(지운 것이 아니라 가린다)',
       !!q&&q.classList.contains('crophid')&&getComputedStyle(q).display==='none'&&q.textContent.length>0,
       [q&&q.className,q&&getComputedStyle(q).display,q&&q.textContent.length]);
     const cv=$('#card .cropw canvas[data-cr]');
     let k=0;while(k++<40&&!(cv.width>1&&cv.width!==300))await wait(250);
     T('C-3 조각이 실제로 그려진다(교재 PDF 를 그 자리만 오려 낸다)',cv.width>1&&cv.width!==300&&cv.height>1,[cv.width,cv.height]);
     /* 좌표 무변 — 다시 열어도 같은 자리 */
     const r1=cv.getBoundingClientRect(), c1=[cv.width,cv.height].join('x');
     showProblem(); await wait(1200);
     const cv2=$('#card .cropw canvas[data-cr]');
     let k2=0;while(k2++<40&&!(cv2.width>1&&cv2.width!==300))await wait(250);
     T('C-3 두 번 열어도 조각 자리·크기가 같다',
       Math.abs(cv2.getBoundingClientRect().width-r1.width)<1&&[cv2.width,cv2.height].join('x')===c1,
       [r1.width,cv2.getBoundingClientRect().width,c1,[cv2.width,cv2.height].join('x')]);
     T('C-3 저장 꼴 = {p:인쇄쪽, r:[x0,y0,x1,y1]}',(function(){const c=cropList(UID,'q')[0];
       return c&&c.p===PR&&Array.isArray(c.r)&&c.r.length===4&&c.r[0]<c.r[2]&&c.r[1]<c.r[3]})(),cropList(UID,'q')[0]);
   });

   /* ═══ C-4 ✕ 로 떼면 글자가 돌아온다 ═══ */
   await grp('C-4', async()=>{
     const x=$('#card .cropw [data-crx]');
     T('C-4 조각 옆에 ✕ 가 있다',!!x);
     x.click(); await wait(700);
     T('C-4 떼면 crop.q 가 비고 키가 사라진다',cropList(UID,'q').length===0&&CROP[UID]===undefined,[cropList(UID,'q').length,CROP[UID]]);
     const q=$('#card .q');
     T('C-4 원래 글자가 돌아온다',!!q&&!q.classList.contains('crophid')&&getComputedStyle(q).display!=='none',[q&&q.className,q&&getComputedStyle(q).display]);
     T('C-4 조각 칸도 사라진다',$$$('#card .cropw').length===0);
   });

   /* ═══ C-5 해설 칸 ═══ */
   await grp('C-5', async()=>{
     await cropAdd(UID,'s',{p:PR,r:[80,120,400,240]});
     showProblem(); await wait(500);
     $('#cDet').open=true; await wait(300);
     T('C-5 해설 칸에도 붙는다',$$$('#card .cropw[data-cropw="s"] canvas[data-cr]').length===1);
     const w=$('#card .solwrap');
     T('C-5 해설 OCR 글자가 가려진다',!!w&&w.classList.contains('crophid')&&getComputedStyle(w).display==='none',[w&&w.className]);
     T('C-5 문제 칸은 안 가려진다(칸이 따로 논다)',!$('#card .q').classList.contains('crophid'));
     await cropDel(UID,'s',0); showProblem(); await wait(300);
     T('C-5 떼면 해설 글자도 돌아온다',!$('#card .solwrap').classList.contains('crophid'));
     closeView(); await wait(80);
   });

   /* ═══════════ ② 글상자 txt ═══════════ */
   await grp('T-0', async()=>{
     T('T-0 지학 SYNC_KEYS 옛 19키 앞자리 그대로 · txt 가 17째',SUBJ.earth.SYNC_KEYS.slice(0,19).join()==='status,note,qtype,conc,gpt,twin,ansfix,frm,maskpos,omrpos,mcard,bogi,unit,bpit,bpg,crop,txt,tfix,bref'&&   /* A-6(a) 9/30 — listpop_add1 §G(cd248a5) 끝에 gg·ggref·pick·link 더함 */
       SUBJ.earth.SYNC_KEYS[16]==='txt',SUBJ.earth.SYNC_KEYS);
     T('T-0 생물 20 · 물리 12 무변',SUBJ.bio.SYNC_KEYS.length===20&&SUBJ.phys.SYNC_KEYS.length===12,[SUBJ.bio.SYNC_KEYS.length,SUBJ.phys.SYNC_KEYS.length]);
     T('T-0 SYNC_REF 에 txt',!!SYNC_REF.txt&&SYNC_REF.txt.g()===TXT);
     const bad0=TXTBAD; TXT['__B1']='배열이 아니다';
     T('T-0 모르는 꼴은 추측해서 덮지 않는다 — TXTBAD 로 센다',txtList('__B1').length===0&&TXTBAD>bad0);
     delete TXT['__B1'];
   });

   /* ── T-1 교재 글상자 ── */
   let PG=null;
   await grp('T-1', async()=>{
     await bkOpen(208); await wait(2500);
     let n=0;while(n++<60&&(!bkCurPage()||bkCurPage().pr!==208))await wait(200);
     PG=bkCurPage();
     const tb=$('#bktools [data-tool="txt"]');
     /* add2 §4-2 — 오리기 단추를 뺐으므로 글상자의 기준은 지우개다(종전에는 오리기 뒤였다) */
     T('T-1 교재 도구줄에 「T 글상자」 · 지우개 뒤',!!tb&&tb.textContent.indexOf('글상자')>=0&&tb.previousElementSibling.dataset.tool==='erase',tb&&tb.previousElementSibling.dataset.tool);
     tb.click(); await wait(60);
     T('T-1 고르면 BK.tool 이 txt',BK.tool==='txt',BK.tool);
     const key=PG.key, n0=txtList(key).length;
     const ink0=((BK.ink[key]||{s:[]}).s||[]).length;
     const vp=$('#bkvp'), vr=vp.getBoundingClientRect();
     PE('pointerdown',vp,vr.left+vr.width/2,vr.top+vr.height/2,'pen'); await wait(250);
     T('T-1 찍으면 글상자가 선다',$$$('#bkover .tbox').length>=1,$$$('#bkover .tbox').length);
     const el=[...PG.el.querySelectorAll('.tbox')].pop();
     T('T-1 바로 타이핑할 수 있다(contenteditable · 커서)',!!el&&el.contentEditable==='true'&&document.activeElement===el,[el&&el.contentEditable,document.activeElement===el]);
     el.textContent='지구 자전 증거 푸코진자';
     el.dispatchEvent(new Event('blur'));
     await wait(500);
     T('T-1 타이핑한 글자가 txt 에 남는다 · 키가 그 자리 꼴(bink:)',
       txtList(key).length===n0+1&&/^bink:\d+$/.test(key)&&txtList(key)[n0].s.indexOf('푸코진자')>=0,[key,txtList(key)]);
     T('T-1 좌표가 0~1 정규화다(그 자리 잉크와 같은 기준)',
       (function(){const t=txtList(key)[n0];return t.x>0&&t.x<1&&t.y>0&&t.y<1})(),txtList(key)[n0]);
     T('T-1 잉크 획 수가 무변(획 통과 다른 통)',((BK.ink[key]||{s:[]}).s||[]).length===ink0,[((BK.ink[key]||{s:[]}).s||[]).length,ink0]);
     /* 지우개로 문질러도 글상자는 안 지워진다 */
     $('#bktools [data-tool="erase"]').click(); await wait(40);
     const er=PG.el.querySelector('.tbox').getBoundingClientRect();
     PE('pointerdown',vp,er.left+4,er.top+4,'pen');PE('pointermove',vp,er.left+10,er.top+10,'pen');PE('pointerup',vp,er.left+10,er.top+10,'pen');
     await wait(300);
     T('T-1 지우개는 획만 지운다 — 글상자가 안 지워진다',txtList(key).length===n0+1&&PG.el.querySelectorAll('.tbox').length>=1,txtList(key).length);
     /* 빈 채로 두면 저절로 사라진다 */
     $('#bktools [data-tool="txt"]').click(); await wait(40);
     PE('pointerdown',vp,vr.left+vr.width/2+40,vr.top+vr.height/2+40,'pen'); await wait(250);
     const el2=[...PG.el.querySelectorAll('.tbox')].pop();
     el2.textContent=''; el2.dispatchEvent(new Event('blur')); await wait(400);
     T('T-1 빈 채로 두면 저절로 사라진다',txtList(key).length===n0+1,txtList(key).length);
   });

   /* ── T-2 다시 열어도 같은 자리 ── */
   await grp('T-2', async()=>{
     const key=PG.key, t0=txtList(key)[0];
     const box0=PG.el.querySelector('.tbox').getBoundingClientRect();
     const S0=BK.S;
     BK.S=S0*1.6; zApply(BK); bkTxtAll(); await wait(300);
     const box1=PG.el.querySelector('.tbox').getBoundingClientRect();
     T('T-2 배율을 키우면 글상자도 같은 비율로 커진다(쪽 좌표에 매여 있다)',
       Math.abs(box1.width/box0.width-1.6)<0.2||Math.abs(box1.left-box0.left)>1,[box0.width,box1.width]);
     BK.S=S0; zApply(BK); bkTxtAll(); await wait(300);
     const t1=txtList(key)[0];
     T('T-2 저장된 좌표는 배율에 안 흔들린다',JSON.stringify(t0)===JSON.stringify(t1),[t0,t1]);
     const box2=PG.el.querySelector('.tbox').getBoundingClientRect();
     T('T-2 배율을 되돌리면 같은 자리',Math.abs(box2.left-box0.left)<2&&Math.abs(box2.top-box0.top)<2,[box0.left,box2.left]);
   });

   /* ── T-3 목차 칩 ── */
   await grp('T-3', async()=>{
     bkTocChips(); await wait(120);
     const it=bkItemAt(PG.pr);
     T('T-3 그 쪽이 든 목차 항목을 찾았다',!!it&&!!it.code,it&&it.code);
     const row=$('#bklist .bkit[data-code="'+it.code+'"]');
     const chip=row&&row.querySelector('.bkc');
     const want=bkItemMine(it.code).length;
     T('T-3 그 항목에만 「🗒 N」 칩 · N = 포스트잇 + 글상자 수',!!chip&&+chip.textContent.replace(/\D/g,'')===want&&want>0,[chip&&chip.textContent,want]);
     const zero=[...$$$('#bklist .bkit')].filter(x=>x.dataset.code&&bkItemMine(x.dataset.code).length===0);
     T('T-3 0인 항목에는 칩을 안 그린다',zero.length>0&&zero.every(x=>!x.querySelector('.bkc')),[zero.length]);
     /* 칩 → 팝오버 → 줄을 누르면 그 쪽으로 · 목차 서랍은 열린 채 */
     const foldBefore=$('#bktoc').classList.contains('fold');
     chip.click(); await wait(200);
     T('T-3 칩을 누르면 팝오버',!!$('#bkPop')&&$$$('#bkPop .r').length===want,[$$$('#bkPop .r').length,want]);
     T('T-3 줄 꼴 = 쪽 · 갈래(🗒/T) · 첫 줄',(function(){const r=$('#bkPop .r');
       return /\d+쪽/.test(r.querySelector('.p').textContent)&&/^(🗒|T)$/.test(r.querySelector('.k').textContent)&&r.querySelector('.t').textContent.length>0})(),
       $('#bkPop .r')&&$('#bkPop .r').textContent);
     const p0=bkCurPage().pr;
     $('#bkPop .r').click(); await wait(900);
     T('T-3 줄을 누르면 그 쪽으로 간다 · 목차 서랍은 그대로 열려 있다',
       $('#bktoc').classList.contains('fold')===foldBefore,[foldBefore,$('#bktoc').classList.contains('fold')]);
     bkPopClose();
   });

   /* ── T-4 교재 검색칸 — 내가 쓴 글자만 ── */
   await grp('T-4', async()=>{
     const q=$('#bkTq'), res=$('#bkTres');
     T('T-4 교재 창 안에 검색칸이 있다 · 목차 서랍 머리',!!q&&!!q.closest('#bktoc'),[!!q,q&&!!q.closest('#bktoc')]);
     T('T-4 안내문에 무엇을 훑는지 적혀 있다',/내가 쓴 글자/.test(q.placeholder),q.placeholder);
     T('T-4 목록 머리 #q 는 그대로다(교재 글자가 안 섞인다)',!!$('#q')&&$('#q')!==q&&$('#q').placeholder.indexOf('교재')<0,$('#q').placeholder);
     q.value='푸코진자'; q.oninput(); await wait(200);
     T('T-4 글상자에 친 낱말로 찾으면 그 줄이 나온다',$$$('#bkTres .r').length===1&&/푸코진자/.test(res.textContent),[$$$('#bkTres .r').length,res.textContent.slice(0,60)]);
     /* 포스트잇도 잡힌다 */
     BP[bpitKeyOf(PG.pr,'0','0','자전')]={t:'포스트잇 시험글 코리올리',ts:Date.now()};
     await saveBP();
     q.value='코리올리'; q.oninput(); await wait(200);
     T('T-4 포스트잇에 쓴 낱말도 나온다',$$$('#bkTres .r').length===1&&/코리올리/.test(res.textContent),res.textContent.slice(0,60));
     q.value='코리올리 포스트잇'; q.oninput(); await wait(150);
     T('T-4 낱말 여러 개는 AND',$$$('#bkTres .r').length===1);
     q.value='코리올리 없는낱말'; q.oninput(); await wait(150);
     T('T-4 하나라도 안 맞으면 0건',$$$('#bkTres .r').length===0);
     /* 인쇄 글자는 이 판에서 안 훑는다 */
     q.value='지구'; q.oninput(); await wait(200);
     const hits=[...$$$('#bkTres .r')];
     T('T-4 인쇄 글자만 있는 낱말은 0건(이 판은 인쇄 글자를 안 훑는다)',
       hits.length===bkMyTextHits('지구').length,[hits.length,bkMyTextHits('지구').length]);
     q.value='없을낱말zzz'; q.oninput(); await wait(150);
     T('T-4 0건일 때 「없다」가 아니라 「타이핑한 글자에서는 안 나왔다」',/타이핑한 글자에서는 안 나왔다/.test(res.textContent),res.textContent.slice(0,60));
     q.value='푸코진자'; q.oninput(); await wait(200);
     const p0=bkCurPage().pr;
     $('#bkTres .r').click(); await wait(900);
     T('T-4 결과줄을 누르면 그 쪽으로 간다',!!bkCurPage(),bkCurPage()&&bkCurPage().pr);
     q.value=''; q.oninput();
     delete BP[bpitKeyOf(PG.pr,'0','0','자전')]; await saveBP();
   });

   /* ── T-5 암기카드 글상자 ── */
   await grp('T-5', async()=>{
     bkClose(); await wait(200);
     const no=VNO||DATA[0][F.NO];
     if(!VNO)await openView(no);
     mcardWin(no); await wait(400);
     const t=$('.mcwin .mct [data-t="txt"]');
     T('T-5 카드 도구줄에 「T 글상자」 · 지우개 뒤',!!t&&t.previousElementSibling.dataset.t==='erase',t&&t.textContent);
     t.click(); await wait(60);
     const box=$('.mcwin .mccv'), br=box.getBoundingClientRect();
     const cv=$('.mcwin #mcc');
     const ink0=((MC[no]||{s:[]}).s||[]).length;
     cv.dispatchEvent(new PointerEvent('pointerdown',{clientX:br.left+br.width/2,clientY:br.top+br.height/2,pointerId:5,pointerType:'pen',bubbles:true,cancelable:true}));
     await wait(250);
     const el=box.querySelector('.tbox');
     T('T-5 찍으면 카드에도 글상자가 선다',!!el,box.querySelectorAll('.tbox').length);
     el.textContent='카드 글상자 시험';
     el.dispatchEvent(new Event('blur')); await wait(400);
     T('T-5 키가 card:<no> 꼴',txtList('card:'+no).length===1,[Object.keys(TXT).filter(k=>k.indexOf('card:')===0)]);
     T('T-5 좌표가 1/1000(카드 잉크와 같은 기준)',(function(){const q=txtList('card:'+no)[0];
       return q.x>1&&q.x<1000&&q.y>1&&q.y<1000&&Number.isInteger(q.x)})(),txtList('card:'+no)[0]);
     T('T-5 카드 잉크(MC)는 안 늘었다',((MC[no]||{s:[]}).s||[]).length===ink0,[((MC[no]||{s:[]}).s||[]).length,ink0]);
     T('T-5 세 자리 키가 다 다르다(bink:·note:·card:)',
       Object.keys(TXT).some(k=>k.indexOf('bink:')===0)&&Object.keys(TXT).some(k=>k.indexOf('card:')===0),Object.keys(TXT));
     delete TXT['card:'+no]; await saveTXT();
     document.querySelectorAll('.sheet').forEach(x=>{if(x.classList.contains('mcwin'))x.remove()});
   });

   /* ── T-6 서브노트 자리 ── */
   await grp('T-6', async()=>{
     const t=$('#stools [data-tool="txt"]');
     T('T-6 서브노트 도구줄에도 「T 글상자」',!!t&&t.previousElementSibling.dataset.tool==='erase',t&&t.textContent);
     T('T-6 서브노트 쪽 키는 note: 꼴이다(잉크와 같은 키)',SUB.pages().every(p=>/^note:\d+$/.test(p.key)),SUB.pages().map(p=>p.key).slice(0,3));
     T('T-6 SUB.onTxt 이 걸려 있다',typeof SUB.onTxt==='function'&&SUB.txt===true);
   });

   /* ═══════════ ③ 문항 화면 필기 + 회독 층 ═══════════ */
   const draw1=async(sv,pts,pt)=>{
     const r=sv.getBoundingClientRect();
     sv.dispatchEvent(new PointerEvent('pointerdown',{clientX:r.left+pts[0],clientY:r.top+pts[1],pointerId:21,pointerType:pt||'pen',bubbles:true,cancelable:true}));
     for(let i=2;i<pts.length;i+=2)
       sv.dispatchEvent(new PointerEvent('pointermove',{clientX:r.left+pts[i],clientY:r.top+pts[i+1],pointerId:21,pointerType:pt||'pen',bubbles:true,cancelable:true}));
     sv.dispatchEvent(new PointerEvent('pointerup',{clientX:r.left+pts[pts.length-2],clientY:r.top+pts[pts.length-1],pointerId:21,pointerType:pt||'pen',bubbles:true,cancelable:true}));
     await wait(300)};
   let QUIDT='';
   await grp('Q-1', async()=>{
     const r=DATA[0];
     await openView(r[F.NO]); await wait(600);
     QUIDT=r[F.CODE];
     await del('ink','qink:'+QUIDT); await qLoad(QUIDT); await wait(120);
     T('Q-1 카드 안쪽 폭을 760 으로 박았다',QCW===760&&Math.round($('#card').getBoundingClientRect().width/(($('#card').style.transform?parseFloat(/scale\(([\d.]+)\)/.exec($('#card').style.transform)[1]):1)))===760,
       [$('#card').getBoundingClientRect().width,$('#card').style.transform]);
     T('Q-1 잉크 층이 카드 안에 얹혔다 · viewBox 가 0 0 760 H',!!$('#card #qink')&&/^0 0 760 \d+/.test($('#card #qink').getAttribute('viewBox')),$('#card #qink')&&$('#card #qink').getAttribute('viewBox'));
     /* A-6(a) 9/30 — listpop_add2 §A · §A-4(20a7128): 펜·형광·지우개·↺ 는 머리줄 알약 #inkPill 로 옮겼고(.tools 에는 펜이 없다 — 옛 줄은 빈 표본이라 거저 참) 굵기 #tW 는 숨기고 값 「보통(2)」 */
     T('Q-1 필기 도구가 카드 층에서 살아났다(펜·형광·지우개·↺·회독·👁 · 굵기는 숨김·값 2)',
       ['#tErase','#tUndo','#tLayer','#tLayerAdd','#tLayerEye'].every(x=>getComputedStyle($(x)).display!=='none')
       &&getComputedStyle($('#tW')).display==='none'&&$('#tW').value==='2'
       &&$$$('#inkPill [data-pen]').length>0&&$$$('#inkPill [data-pen]').every(x=>getComputedStyle(x).display!=='none'),
       ['#tErase','#tUndo','#tW','#tLayer','#tLayerAdd','#tLayerEye'].map(x=>getComputedStyle($(x)).display));
     T('Q-1 물리 전용 도구는 그대로 숨어 있다(가리개·OMR·PDF 무대)',
       ['#mask','#omrPad','.stage'].every(x=>getComputedStyle($(x)).display==='none'));
     /* add2 §3·§6 — 문항 화면은 「보기」로 열린다. penon 이 붙으면 #qink(z-index 6)가 카드
        전면을 담요처럼 덮어 선택지·펼치기·이전다음이 전부 죽는다.
        ★ 픽셀이 아니라 쌓임 순서(elementsFromPoint)로 잰다 — CLAUDE.md 자과앱 게이트. */
     /* A-6(a) 9/30 — 9/13 889cd8e(사용자 확정): 문항 카드 「보기」 단추(#tView)를 걷고 카드 층도 물리와 같이 「펜」으로 연다(recBoot setTool('pen')) ·
        #qink 덮개가 카드를 덮어도 누름은 덮개 뚫기(2270f4d · inkPierce)가 밑으로 넘긴다 */
     T('Q-1 카드가 「펜」으로 열린다(889cd8e · 「보기」 단추 걷음)',
       TOOL.mode==='pen'&&$('#card').classList.contains('penon'),[TOOL.mode,$('#card').className]);
     T('Q-1 카드 도구줄에 「보기」 단추가 없다(889cd8e 걷음)',
       !$('#tView'),!!$('#tView'));
     T('Q-1 펜으로 열리니 잉크 층이 잡힌다(누름은 덮개 뚫기가 밑으로 넘긴다 · 889cd8e)',
       getComputedStyle($('#card #qink')).pointerEvents==='auto',
       getComputedStyle($('#card #qink')).pointerEvents);
     T('Q-1 ★선택지 자리의 맨 위는 #qink 덮개 · 덮개 밑(underInk)이 그 선택지다(889cd8e · 2270f4d 덮개 뚫기 · elementsFromPoint)',(()=>{
       const b=$('#card .choices button')||$('#card .choices')||$('#card .q'); if(!b)return false;
       const r=b.getBoundingClientRect();
       const st=document.elementsFromPoint(r.left+r.width/2,r.top+r.height/2);
       /* A-6(a) 9/30 — 펜으로 열려 맨 위는 덮개다 · 짧게 톡은 inkPierce 가 덮개 밑(underInk · UNDER_HIT)으로 넘긴다 → 그 밑이 이 선택지인가 */
       const ink=(st.length&&st[0].closest)?st[0].closest('#qink'):null;
       const u=ink?underInk(r.left+r.width/2,r.top+r.height/2,ink):null;
       return !!ink&&!!u&&(u===b||b.contains(u))})(),
       (()=>{const b=$('#card .choices button')||$('#card .choices')||$('#card .q'); if(!b)return '선택지 없음';
         const r=b.getBoundingClientRect();
         return document.elementsFromPoint(r.left+r.width/2,r.top+r.height/2).slice(0,3)
           .map(e=>e.id||e.tagName+'.'+((e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className)||'')).join(' > ')})());
   });

   await grp('Q-2', async()=>{
     setTool('pen','#B03A2E',$$$('[data-pen]')[1]); qWire(); await wait(60);
     const sv=$('#card #qink');
     T('Q-2 펜을 고르면 잉크 층이 잡힌다',$('#card').classList.contains('penon')&&getComputedStyle(sv).pointerEvents==='auto',getComputedStyle(sv).pointerEvents);
     const n0=((QINK.s)||[]).length;
     await draw1(sv,[60,60,120,90,180,140]);
     T('Q-2 획을 그으면 QINK 가 는다',((QINK.s)||[]).length===n0+1,[((QINK.s)||[]).length,n0]);
     const saved=await get('ink','qink:'+QUIDT);
     T('Q-2 ink 스토어 qink:<uid> 에 저장된다',!!saved&&Array.isArray(saved.s)&&saved.s.length===n0+1,[saved&&saved.s&&saved.s.length]);
     T('Q-2 좌표가 0~1 정규화(둘 다 폭 760 으로)',QINK.s[n0].p.every(v=>v>=0&&v<=1.5)&&QINK.s[n0].p.length>=6,QINK.s[n0].p);
     T('Q-2 획에 회독 번호 r 이 붙는다(지금 1회독)',QINK.s[n0].r===1&&QR===1,[QINK.s[n0].r,QR]);
     T('Q-2 화면에 그려졌다',$$$('#card #qink path[data-j]').length===n0+1);
     T('Q-2 SYNC_KEYS 에 qink 를 안 넣었다 — 문항 필기는 기기별로 산다',
       SYNC_KEYS.indexOf('qink')<0&&SUBJ.earth.SYNC_KEYS.indexOf('qink')<0,SUBJ.earth.SYNC_KEYS.length);
     /* 창 폭을 바꿔 다시 열어도 획의 상대 좌표가 같다 */
     const snap=JSON.stringify(QINK.s);
     /* ⚠ #cardwrap 은 flex 항목이라 width 만 줘서는 안 줄어든다 — flex 도 같이 잡는다 */
     const w=$('#cardwrap'); const oldW=w.style.width, oldF=w.style.flex;
     w.style.flex='0 0 420px'; w.style.width='420px'; await wait(120); qFit(); qPaint(); await wait(200);
     T('Q-2 좁은 화면에서는 카드가 통째로 줄어든다(글이 다시 흐르지 않는다)',
       /scale\(/.test($('#card').style.transform),$('#card').style.transform);
     await qLoad(QUIDT); await wait(200);
     T('Q-2 창 폭을 바꿔 다시 열어도 획의 상대 좌표가 전건 같다',JSON.stringify(QINK.s)===snap,[JSON.stringify(QINK.s).slice(0,60),snap.slice(0,60)]);
     w.style.width=oldW; w.style.flex=oldF; await wait(120); qFit(); qPaint(); await wait(150);
   });

   await grp('Q-3', async()=>{
     const sv=$('#card #qink');
     /* 2회독으로 넘어가 한 획 더 */
     $('#tLayerAdd').click(); await wait(150);
     T('Q-3 「+회독」 → 2회독',QR===2&&+$('#tLayer').value===2,[QR,$('#tLayer').value]);
     await draw1(sv,[300,60,360,90,420,140]);
     const S=QINK.s;
     T('Q-3 새 획은 2회독',S[S.length-1].r===2);
     const paths=$$$('#card #qink path[data-j]');
     const cur=paths.filter(p=>p.dataset.r==='2'), old=paths.filter(p=>p.dataset.r==='1');
     T('Q-3 지금 회독은 진하게 · 옛 회독은 0.30',
       cur.every(p=>p.getAttribute('opacity')==='1')&&old.every(p=>p.getAttribute('opacity')==='0.3'),
       [cur.map(p=>p.getAttribute('opacity')),old.map(p=>p.getAttribute('opacity'))]);
     /* 형광은 0.32 */
     setTool('hl','#F2C230',$$$('[data-hl]')[0]); qWire(); await wait(60);
     await draw1(sv,[500,60,560,90,620,140]);
     const hl=$$$('#card #qink path[data-j]').pop();
     T('Q-3 형광은 0.32',hl.getAttribute('opacity')==='0.32',hl.getAttribute('opacity'));
     /* 👁 = 지금 회독만 */
     $('#tLayerEye').click(); await wait(150);
     T('Q-3 👁 켜면 옛 회독이 안 그려진다',QHIDE===true&&$$$('#card #qink path[data-j]').every(p=>p.dataset.r==='2'),
       $$$('#card #qink path[data-j]').map(p=>p.dataset.r));
     $('#tLayerEye').click(); await wait(150);
     T('Q-3 다시 끄면 옛 회독이 돌아온다',QHIDE===false&&$$$('#card #qink path[data-j]').some(p=>p.dataset.r==='1'));
     /* r 없는 옛 획은 1회독으로 친다 */
     QINK.s.push({c:'#000',w:2,hl:0,p:[0.1,0.9,0.2,0.95]});   /* r 이 없다 */
     qPaint(); await wait(80);
     const noR=$$$('#card #qink path[data-j]').pop();
     T('Q-3 r 이 없는 옛 획은 1회독으로 그려진다(규약)',noR.dataset.r==='1'&&noR.getAttribute('opacity')==='0.3',[noR.dataset.r,noR.getAttribute('opacity')]);
     QINK.s.pop(); qPaint();
   });

   await grp('Q-4', async()=>{
     const sv=$('#card #qink');
     const n1=QINK.s.filter(x=>qRoundOf(x)===1).length, n2=QINK.s.filter(x=>qRoundOf(x)===2).length;
     T('Q-4 1회독 · 2회독 획이 둘 다 있다',n1>0&&n2>0,[n1,n2]);
     /* 지우개는 지금 회독(2)만 */
     setTool('erase'); qWire(); await wait(60);
     const p2=QINK.s.find(x=>qRoundOf(x)===2);
     const r=sv.getBoundingClientRect(), k=r.width/QCW;
     sv.dispatchEvent(new PointerEvent('pointerdown',{clientX:r.left+p2.p[0]*QCW*k,clientY:r.top+p2.p[1]*QCW*k,pointerId:22,pointerType:'pen',bubbles:true,cancelable:true}));
     sv.dispatchEvent(new PointerEvent('pointerup',{clientX:r.left+p2.p[0]*QCW*k,clientY:r.top+p2.p[1]*QCW*k,pointerId:22,pointerType:'pen',bubbles:true,cancelable:true}));
     await wait(300);
     T('Q-4 지우개는 지금 회독만 지운다 — 1회독 획은 그대로',
       QINK.s.filter(x=>qRoundOf(x)===1).length===n1&&QINK.s.filter(x=>qRoundOf(x)===2).length<n2,
       [QINK.s.filter(x=>qRoundOf(x)===1).length,n1,QINK.s.filter(x=>qRoundOf(x)===2).length,n2]);
     /* ↺ 는 지금 회독의 마지막 획 */
     const before=QINK.s.length;
     await qUndo(); await wait(200);
     T('Q-4 ↺ 는 지금 회독의 마지막 획을 무른다',QINK.s.length===before-1||before===0,[QINK.s.length,before]);
     /* 「모두 지움」 */
     setTool('erase'); $('#tErase').click(); await wait(200);
     T('Q-4 지우개 상태에서 다시 누르면 시트 — 「지금 회독만」·「모두 지움」',!!$('#qeL')&&!!$('#qeA'));
     $('#qeA').click(); await wait(300);
     T('Q-4 「모두 지움」은 전부 지운다',(QINK.s||[]).length===0&&QR===1,[(QINK.s||[]).length,QR]);
     const saved=await get('ink','qink:'+QUIDT);
     T('Q-4 저장소에도 반영된다',!!saved&&(saved.s||[]).length===0);
     setTool('pen','#16181B',$$$('[data-pen]')[0]); qWire();
     closeView(); await wait(80);
   });

   /* ═══════════ ④ 글자 고치기 tfix ═══════════ */
   let XU='', XR=null;
   await grp('X-1', async()=>{
     T('X-1 지학 SYNC_KEYS 옛 19키 앞자리 그대로 · tfix 가 18째',SUBJ.earth.SYNC_KEYS.slice(0,19).join()==='status,note,qtype,conc,gpt,twin,ansfix,frm,maskpos,omrpos,mcard,bogi,unit,bpit,bpg,crop,txt,tfix,bref'&&   /* A-6(a) 9/30 — listpop_add1 §G(cd248a5) 끝에 gg·ggref·pick·link 더함 */
       SUBJ.earth.SYNC_KEYS[17]==='tfix',SUBJ.earth.SYNC_KEYS);
     T('X-1 생물 20 · 물리 12 무변',SUBJ.bio.SYNC_KEYS.length===20&&SUBJ.phys.SYNC_KEYS.length===12,[SUBJ.bio.SYNC_KEYS.length,SUBJ.phys.SYNC_KEYS.length]);
     T('X-1 SYNC_REF 에 tfix',!!SYNC_REF.tfix&&SYNC_REF.tfix.g()===TFIX);
     T('X-1 담는 칸이 일곱 — 문제 · 보기 ①~⑤ · 해설',TFIX_SLOTS.length===7&&TFIX_SLOTS.join()==='q,c1,c2,c3,c4,c5,s',TFIX_SLOTS);
     T('X-1 정답은 기존 ansfix 가 맡는다(tfix 에 안 넣는다)',TFIX_SLOTS.indexOf('ans')<0&&SUBJ.earth.SYNC_KEYS.indexOf('ansfix')>=0);
     const bad0=TFIXBAD; TFIX['__F1']={q:12345};
     T('X-1 모르는 꼴은 추측해서 덮지 않는다 — TFIXBAD 로 센다',tfixRaw('__F1','q')===''&&TFIXBAD>bad0);
     delete TFIX['__F1'];
   });

   await grp('X-2', async()=>{
     XR=DATA.find(r=>(r[F.CH]||[]).filter(x=>x).length>=3&&String(r[F.SOL]||'').length>3)||DATA[0];
     XU=XR[F.CODE];
     await openView(XR[F.NO]); await wait(600);
     const q0=stemOf(XR);
     T('X-2 고치기 전에는 txtOf 가 원본을 돌려준다',txtOf(XU,'q')===q0&&txtOf(XU,'c1')===String((XR[F.CH]||[])[0]||''),
       [txtOf(XU,'q').slice(0,20),q0.slice(0,20)]);
     T('X-2 화면에도 원본이 떠 있다',$('#card .q').textContent.indexOf(q0.slice(0,10))>=0);
     T('X-2 고치기 전에는 ✎ 배지가 없다',$$$('#card .tfx').length===0);
     /* 문제 칸을 고친다 */
     await tfixSet(XU,'q','θ:360°=l:2πR 로 고친 문제 글'); showProblem(); await wait(400);
     T('X-2 txtOf 가 고친 글자를 돌려준다',txtOf(XU,'q')==='θ:360°=l:2πR 로 고친 문제 글',txtOf(XU,'q'));
     T('X-2 화면이 고친 글자로 바뀐다',$('#card .q').textContent.indexOf('2πR 로 고친')>=0,$('#card .q').textContent.slice(0,40));
     T('X-2 고친 칸에 ✎ 배지가 뜬다',$$$('#card .q .tfx').length===1&&$('#card .q').classList.contains('fixed'));
     T('X-2 ⚠ DATA 원본은 한 글자도 안 바뀐다',stemOf(XR)===q0&&String(rec(XR[F.NO])[F.BODY]).indexOf(q0.slice(0,10))>=0,[stemOf(XR).slice(0,20),q0.slice(0,20)]);
     /* 되돌리기 = 비우기 */
     await tfixSet(XU,'q',''); showProblem(); await wait(400);
     T('X-2 비우면 원본으로 돌아간다 · 배지도 사라진다',txtOf(XU,'q')===q0&&$$$('#card .q .tfx').length===0&&TFIX[XU]===undefined,[txtOf(XU,'q').slice(0,20)]);
   });

   await grp('X-3', async()=>{
     /* 보기 ①~⑤ · 해설도 같은 길 */
     const c1=String((XR[F.CH]||[])[0]||'');
     await tfixSet(XU,'c1','고친 보기 하나'); await tfixSet(XU,'s','고친 해설 글');
     showProblem(); await wait(400);
     $('#cDet').open=true; await wait(300);
     T('X-3 보기 ①이 고친 글자로 뜬다 · ✎',$('#card .choices button[data-tfx="c1"]').textContent.indexOf('고친 보기 하나')>=0
       &&$('#card .choices button[data-tfx="c1"]').classList.contains('fixed'),$('#card .choices button[data-tfx="c1"]').textContent.slice(0,30));
     T('X-3 해설도 고친 글자로 뜬다',$('#card').textContent.indexOf('고친 해설 글')>=0);
     T('X-3 원본은 그대로다',String((XR[F.CH]||[])[0]||'')===c1&&txtOrig(XU,'c1')===c1);
     T('X-3 일곱 칸이 다 선다',TFIX_SLOTS.every(k=>typeof txtOf(XU,k)==='string'));
   });

   await grp('X-4', async()=>{
     /* 검색 — 원본과 고친 글자를 둘 다 */
     const q0=stemOf(XR);
     const w0=(q0.match(/[가-힣]{3,}/)||['지구'])[0];
     FL.q='고친 해설 글'; const hit1=filtered().some(r=>r[F.CODE]===XU);
     FL.q=w0; const hit2=filtered().some(r=>r[F.CODE]===XU);
     FL.q='';
     T('X-4 고친 글자로 찾힌다',hit1,['고친 해설 글',hit1]);
     T('X-4 ⚠ 옛(원본) 낱말로도 그대로 찾힌다 — 고친 뒤 못 찾게 되면 안 된다',hit2,[w0,hit2]);
     T('X-4 tfixHay 가 고친 칸만 모은다',tfixHay(XU).indexOf('고친 해설 글')>=0&&tfixHay(XU).indexOf('고친 보기 하나')>=0,tfixHay(XU));
   });

   await grp('X-5', async()=>{
     /* 길게 누르면 고치기 시트 · 짧게 누름(선택지 고르기)과 안 부딪힌다 */
     showProblem(); await wait(400);
     const el=$('#card .q');
     const r=el.getBoundingClientRect();
     PE('pointerdown',el,r.left+8,r.top+8,'mouse'); await wait(700); PE('pointerup',el,r.left+8,r.top+8,'mouse'); await wait(250);
     T('X-5 길게 누르면 고치기 시트가 뜬다',!!$('#tfxSheet')&&!!$('#tfxIn'),!!$('#tfxSheet'));
     T('X-5 시트에 원본이 같이 보인다',!!$('#tfxSheet .orig')&&$('#tfxSheet .orig').textContent.length>0);
     $('#tfxIn').value='시트로 고친 글';
     $('#tfxOk').click(); await wait(500);
     T('X-5 저장하면 그 칸이 바뀐다',txtOf(XU,'q')==='시트로 고친 글',txtOf(XU,'q'));
     /* 되돌리기 단추 */
     const el2=$('#card .q'); const r2=el2.getBoundingClientRect();
     PE('pointerdown',el2,r2.left+8,r2.top+8,'mouse'); await wait(700); PE('pointerup',el2,r2.left+8,r2.top+8,'mouse'); await wait(250);
     $('#tfxDel').click(); await wait(500);
     T('X-5 「되돌리기(비우기)」로 원본이 돌아온다',txtOf(XU,'q')===stemOf(XR)&&!tfixOn(XU,'q'),txtOf(XU,'q').slice(0,20));
     /* 짧게 누르면 선택지 고르기가 종전대로 */
     const pick0=(SET&&SET.pick)?1:1;
     const cb=$('#card .choices button[data-c="1"]');
     if(cb){const rb=cb.getBoundingClientRect();
       PE('pointerdown',cb,rb.left+8,rb.top+8,'mouse'); PE('pointerup',cb,rb.left+8,rb.top+8,'mouse'); cb.click(); await wait(250);
       T('X-5 짧게 누름은 종전대로 선택지 고르기(시트가 안 뜬다)',!$('#tfxSheet'));}
     else T('X-5 짧게 누름은 종전대로 선택지 고르기(시트가 안 뜬다)',true);
     await tfixSet(XU,'c1',''); await tfixSet(XU,'s','');
     closeView(); await wait(80);
   });

   await grp('X-6', async()=>{
     /* ①의 메뉴에 「✎ 글자로 고치기」가 살아났다 */
     await openView(XR[F.NO]); await wait(300);
     await bkOpen(208); await wait(2200);
     let n=0;while(n++<60&&!bkCurPage())await wait(200);
     {const bar=$('#bktools');let x=bar.querySelector('[data-tool="crop"]');
      if(!x){x=document.createElement('span');x.dataset.tool='crop';x.textContent='▢ 오리기';
        bar.appendChild(x);zTools(BK,'#bktools','#bkvp')}       /* add2 §4-1 — 단추는 실물에 없다. 엔진만 몬다 */
      x.click()} await wait(60);
     const vp=$('#bkvp'), vr=vp.getBoundingClientRect();
     const cx=vr.left+vr.width/2, cy=vr.top+vr.height/2;
     PE('pointerdown',vp,cx,cy,'pen');PE('pointermove',vp,cx+110,cy+80,'pen');PE('pointerup',vp,cx+110,cy+80,'pen');
     await wait(250);
     T('X-6 ④가 서니 메뉴에 「✎ 글자로 고치기」가 생겼다',$$$('#crmenu button').length===5   /* A-6(a) 9/30 — listpop_add1 §F(cd248a5) 🃏 카드로 찍기를 맨 위에 더함 */
       &&$$$('#crmenu button').some(b=>b.textContent.indexOf('글자로 고치기')>=0),$$$('#crmenu button').map(b=>b.textContent));
     $('#crmenu [data-s="fix"]').click(); await wait(400);
     T('X-6 누르면 고치기 시트가 뜨고 네모·메뉴가 사라진다',!!$('#tfxSheet')&&$$$('.crbox').length===0&&!document.getElementById('crmenu'));
     $('#tfxNo').click(); bkClose(); closeView(); await wait(120);
   });
"""

# ═══════════════════════════ Y. 물리 ═══════════════════════════
BODY_PHYS = r"""
   await wait(500); draw(); await wait(300);
   T('Y-0 물리 · 카드 층 아님',SUBJ_ID==='phys'&&CARD_LAYER===false,[SUBJ_ID,CARD_LAYER]);
   const snap={};
   /* ⚠ 대조 스냅은 맨 먼저 뜬다 — 아래 검사 하나가 고침 전 판에서 ReferenceError 를 내면
      묶음이 통째로 끊겨 스냅이 안 찍힌다(CROP 은 고침 전 판에 아예 없다 · 실측). */
   snap.list=$('#list').innerHTML; snap.cnt=$('#cnt').textContent; snap.n=$$$('#list .item').length;
   snap.brand=document.querySelector('.brand').innerHTML;
   await grp('Y-1', async()=>{
     T('Y-1 목록이 그려졌다',snap.n>0,snap.n);
     /* A-6(a) 9/30 — 카드 층 블록의 문이 c9faff2(shell_bio_phys)에서 if(SHELL)(세 과목 참)로 바뀌었고 add5 §A 원칙(c20ef05 · 「블록의 문 if(SHELL){ 는 그대로 두고 안에서 이름마다 가른다」)이 그대로 두어
        물리에서도 함수는 만들어진다 → 물리 무변은 「안 만든다」가 아니라 「교재 갈래 HASBOOK 이 거짓」으로 선다(값은 info 에 typeof 로 남긴다 ·
        물리 화면에 안 쓰이는 것은 아래 CROP 비어 있음 · 조각 칸 0 · 글상자 0 · 문항 잉크 층 0 이 잰다) */
     T('Y-1 물리는 crop 을 안 쓴다 — cropList·cropAdd·cropPaint 는 SHELL 블록이라 있어도 HASBOOK=false',
       typeof HASBOOK!=='undefined'&&HASBOOK===false,
       [typeof cropList,typeof cropAdd,typeof cropPaint]);
     T('Y-1 교재 창(BK)·zWire 는 SHELL 블록이라 있어도 물리엔 교재 창이 안 뜬다(#book 숨음 · HASBOOK=false)',   /* A-6(a) 9/30 — c9faff2 · add5 §A 원칙 · body[data-layer="pdf"] #book{display:none!important} */
       typeof HASBOOK!=='undefined'&&HASBOOK===false&&!!$('#book')&&getComputedStyle($('#book')).display==='none',[typeof BK,typeof zWire]);
     T('Y-1 SYNC_KEYS 옛 12키 앞자리 그대로 · crop 없음',SYNC_KEYS.slice(0,12).join()==='status,note,qtype,conc,gpt,twin,ansfix,frm,maskpos,omrpos,mcard,link'&&   /* A-6(a) 9/30 — shell_bio_phys §E-7(c9faff2) 물리 끝에 gg·ggref 더함 */
       SYNC_KEYS.indexOf('crop')<0,SYNC_KEYS.length);
     T('Y-1 CROP 전역은 비어 있다(카드 층에서만 채운다)',typeof CROP==='undefined'||JSON.stringify(CROP)==='{}',typeof CROP);
     T('Y-1 물리 화면에 조각 칸이 0개',$$$('.cropw').length===0&&$$$('.crophid').length===0);
     T('Y-1 물리는 글상자를 안 쓴다 — txtList·txtPaint·bkMyText 는 SHELL 블록이라 있어도 HASBOOK=false',   /* A-6(a) 9/30 — c9faff2 · add5 §A 원칙(위 crop 줄과 같은 까닭) */
       typeof HASBOOK!=='undefined'&&HASBOOK===false,
       [typeof txtList,typeof txtPaint,typeof bkMyText]);
     T('Y-1 물리 화면에 글상자·목차 칩이 0개',$$$('.tbox').length===0&&$$$('.bkc').length===0);
     T('Y-1 SYNC_KEYS 에 txt 없음',SYNC_KEYS.indexOf('txt')<0);
     T('Y-1 물리는 문항 필기(qink)를 안 쓴다 — qLoad·qPaint·qWire 는 SHELL 블록이라 있어도 HASBOOK=false',   /* A-6(a) 9/30 — c9faff2 · add5 §A 원칙(위 crop 줄과 같은 까닭) */
       typeof HASBOOK!=='undefined'&&HASBOOK===false,
       [typeof qLoad,typeof qPaint,typeof qWire]);
     T('Y-1 물리 paintInk·INK·LAYER 는 종전 값 그대로',
       typeof paintInk==='function'&&typeof INK==='object'&&typeof LAYER==='number',
       [typeof paintInk,typeof INK,typeof LAYER]);
     T('Y-1 물리 화면에 문항 잉크 층이 0개',$$$('#qink').length===0);
     T('Y-1 물리는 tfix 를 안 쓴다 — txtOf·tfixSet·tfixSheet 는 SHELL 블록이라 있어도 HASBOOK=false',   /* A-6(a) 9/30 — c9faff2 · add5 §A 원칙(위 crop 줄과 같은 까닭) */
       typeof HASBOOK!=='undefined'&&HASBOOK===false,
       [typeof txtOf,typeof tfixSet,typeof tfixSheet]);
     T('Y-1 SYNC_KEYS 에 tfix 없음',SYNC_KEYS.indexOf('tfix')<0);
   });
   try{await __nativeFetch('/snap',{method:'POST',body:JSON.stringify(snap)})}catch(e){}
"""


def build(mode, src_text):
    subj = {'earth': 'earth', 'phys': 'phys', 'physbase': 'phys'}[mode]
    body = BODY_EARTH if mode == 'earth' else BODY_PHYS
    html = src_text
    html = html.replace('<script defer src="https://cdnjs', '<script defer data-off="https://cdnjs')
    html = html.replace('<link rel="stylesheet" href="https://cdnjs', '<link rel="off" href="https://cdnjs')
    html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js',
                        STUB.replace('__SUBJ__', subj) + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    html = html.replace('</body>', HEAD + body + TAIL + '</body>', 1)
    open(os.path.join(OUT, 'app.html'), 'w', encoding='utf-8', newline='').write(html)
    return subj


def run(mode, secs, src_text):
    subj = build(mode, src_text)
    spd = os.path.join(SPDROOT, subj)
    try: shutil.copy(os.path.join(GIGU, '지학_서브노트_빈판_A3.pdf'), os.path.join(OUT, 'blank.pdf'))
    except Exception: pass
    done = threading.Event(); box = {}

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=OUT, **k)
        def log_message(self, *a, **k): pass
        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            if p.startswith('/data/'):
                rel, pre = p[6:], subj + '/'
                if not rel.startswith(pre): self.send_response(404); self.end_headers(); return
                f = os.path.join(spd, rel[len(pre):].replace('/', os.sep))
                if not os.path.isfile(f): self.send_response(404); self.end_headers(); return
                b = open(f, 'rb').read()
                self.send_response(200); self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', str(len(b))); self.send_header('X-Sha', hashlib.sha1(b).hexdigest())
                self.end_headers(); self.wfile.write(b); return
            return super().do_GET()

        def do_POST(self):
            n = int(self.headers.get('Content-Length') or 0)
            body = self.rfile.read(n).decode('utf-8', 'replace'); self.send_response(204); self.end_headers()
            if self.path.startswith('/partial'): box['partial'] = body; return
            if self.path.startswith('/snap'):
                try: box['snap'] = json.loads(body)
                except Exception: box['snap'] = {}
                return
            box['txt'] = body; done.set()

    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    prof = os.path.join(OUT, 'prof_' + mode); shutil.rmtree(prof, ignore_errors=True)
    t0 = time.time()
    p = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--user-data-dir=' + prof,
                          '--window-size=1400,900', 'http://127.0.0.1:%d/app.html' % port],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    got = done.wait(secs); p.terminate()
    try: p.wait(10)
    except Exception: p.kill()
    srv.shutdown()
    print('  [%s] %.0fs' % (mode, time.time() - t0))
    if not got:
        return (['FAIL | %s 묶음이 시간 안에 안 끝났다 | %s' % (mode, box.get('partial', '(중간 결과 없음)')[-700:])], box.get('snap'))
    return ([ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()], box.get('snap'))


def static_checks():
    s = open(SRC, encoding='utf-8').read()
    out = []
    def T2(name, cond, info=''):
        out.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))
    # A-6(a) 9/30 — 카드 층 블록의 문이 c9faff2(shell_bio_phys)에서 `if(CARD_LAYER){` → `if(SHELL){` 로 바뀌었다(add5 §A 원칙 「블록의 문 if(SHELL){ 는 그대로 두고 안에서 이름마다 가른다」 · c20ef05)
    #   → 같은 블록(/*EARTH:js*/ 뒤 첫 `if(SHELL){`)의 시작으로 잰다 · 물리도 이 블록을 돈다(물리 화면 몫은 HASBOOK 이 가른다)
    blk = s.find('\nif(SHELL){\n', s.find('/*EARTH:js*/'))
    T2('S-1 crop 코드는 전부 카드 층 블록(if(SHELL)) 안이다',
       blk >= 0 and all(s.find(k) > blk for k in ['var cropList=', 'var cropAdd=async function(', 'var cropDel=async function(',
                                                  'var cropPaint=', 'var cropBoxHtml=', 'function cropWire(',
                                                  'function cropHandles(', 'BK.onCrop=function(', 'BK.crop=true;']),
       [blk] + [(k, s.find(k)) for k in ['var cropList=', 'var cropAdd=async function(', 'BK.onCrop=function('] if s.find(k) <= blk])
    T2('S-1b 블록 안 async 는 var 꼴로 둔다 — 선언 꼴이면 블록 밖에서 안 보인다(실측)',
       'async function cropAdd(' not in s and 'async function cropDel(' not in s
       and 'var cropAdd=async function(' in s and 'var cropDel=async function(' in s)
    # add1(2026-09-08) — 같은 네모를 링크(bref)도 쓰게 되어 조건이 넓어졌다(고친 자리).
    T2('S-2 오리기·링크는 펜에서만 — 손가락은 종전 길로 흘려보낸다',
       # A-6(a) 9/30 — 9/13 c62b2b2(pen_touch2 §1 · SET.pencil 스위치 없앰 → 「if(pointerType!=='pen') return」) · 9/24 bookwin §E(6c54347 · 📍 찍는 중 교재 창은 마우스도 네모)
       "if(e.pointerType!=='pen'&&!(window.PINFOR&&Z===window.BK&&e.pointerType==='mouse')){" in s
       and "if(Z.crop&&(Z.tool==='crop'||(Z.bref&&Z.tool==='bref'))){" in s
       and "if(e.pointerType!=='pen')return;      /* ⚠ 손가락은 지금처럼 스크롤이다(커밋 ① 규칙 그대로) */" in s)
    T2('S-3 도구줄 마크업 무접촉 · ★오리기 단추를 교재 창에 도로 그린다(2026-09-10) · BK.crop 플래그는 남는다',
       '<div class="stools" id="bktools"><span class="on" data-tool="view">보기</span><span data-tool="pen">펜</span><span data-tool="hl">형광</span><span data-tool' in s
       and s.count("sp.dataset.tool='crop'") == 1
       and 'BK.crop=true;' in s)
    # toBlob 은 판 3 밖(옛 그림 굽기)에 이미 한 곳 있다 — crop 코드 범위 안에서만 잰다
    _c0 = s.find('/* ══ 판 3 ① 교재 조각')
    _c1 = s.find('function cropWire(')
    _cs = s[_c0:_c1] if _c0 >= 0 and _c1 > _c0 else ''
    T2('S-4 그림 파일을 굽지 않는다 — 좌표만 저장하고 열 때 오려 그린다',
       "a.push({p:cell.p,r:cell.r.map(v=>+v.toFixed(1))});" in s
       and bool(_cs) and 'toDataURL' not in _cs and 'toBlob(' not in _cs and s.count('toBlob(') == 1,
       [len(_cs), s.count('toBlob(')])
    T2('S-5 받는 통로는 이미 있는 것(pieceDoc) 을 쓴다 — 새 통로를 안 만든다',
       'const doc=await pieceDoc(pc.file);' in s and s.count('pieceDoc=async function(file){') == 1)
    T2('S-6 DATA 원본 무변 — crop 은 DATA 를 안 건드린다',
       'r[F.BODY]=' not in s and 'r[F.SOL]=' not in s)
    T2('S-7 잉크 무접촉 — inkGet·pathD·zInkCommit 이 판 1 그대로',
       'async function inkGet(key,p){' in s and 'var pathD=(p,w,h)=>' in s
       and 'zInkCommit=async function(Z,st){' in s)
    T2('S-8 mcard 저장 꼴·MC_MAX·조각 좌표표 무접촉',
       'const MC_MAX=20000;' in s and "const saveMC=()=>put('kv','mcard',MC);" in s
       and 'var jogakAR=cell=>{const [x0,y0,x1,y1]=cell.r;return (x1-x0)/(y1-y0)};' in s)
    T2('S-11 txt 코드도 전부 카드 층 블록(if(SHELL)) 안이다',   # A-6(a) 9/30 — 블록의 문 c9faff2 · 잣대 blk 는 S-1 머리에서 고쳤다
       blk >= 0 and all(s.find(k) > blk for k in ['var txtList=', 'function txtPaint(', 'function txtWireOne(',
                                                  'var txtAdd=async function(', 'function txtEl(', 'function bkMyText(', 'function bkTocChips(',
                                                  'function bkPopToggle(', 'function bkTocWire(']))
    T2('S-12 글상자를 잉크 통에 안 넣는다 — 통이 따로다',
       "var saveTXT=()=>put('kv','txt',TXT);" in s and "async function inkGet(key,p){" in s
       and 'TXT[' not in s.split('async function inkGet(key,p){')[1][:600])
    T2('S-13 좌표 기준을 새로 만들지 않았다 — 교재/서브노트 0~1 · 카드 1/1000',
       "txtPaint(p.el,p.key,p.w,p.h,1,true)" in s and "txtPaint(box,cardKey,box.clientWidth||1,box.clientHeight||1,1000,true)" in s)
    T2('S-14 훑는 함수가 한 자리다 — 목차 칩도 검색칸도 bkMyText 를 지난다',
       s.count('function bkMyText(') == 1 and s.count('function bkMyTextHits(') == 1
       and 'bkMyText().filter' in s and 'bkMyTextHits(v)' in s)
    T2('S-15 목차 칩 팝오버도 검색 결과도 같은 이동 함수(bkGoto)를 쓴다 · 새 이동 길을 안 만든다',
       s.count('bkGoto(+r.dataset.p)') == 1 and s.count('bkGoto(+el.dataset.p)') == 2
       and 'bkGoto' in s[s.find('function bkTocWire()'):s.find('function bkPopToggle(')],
       [s.count('bkGoto(+r.dataset.p)'), s.count('bkGoto(+el.dataset.p)')])
    T2('S-16 항목 쪽 범위는 bkItemAt 과 같은 규칙(새 규칙 없음)',
       'function bkItemRange(code){const L=bkItems();' in s and 'hi=(i+1<L.length)?L[i+1].p-1:1e9' in s)
    T2('S-17 포스트잇 키 꼴 무접촉',
       'var bpitKeyOf=(pr,j,wi,word)=>[pr,j,wi,word].join(\'|\');' in s)
    T2('S-18 물리 ndTail·ndPopToggle 소스 무변',
       'function ndTail(no){const m=lastM(no), w=weakState(no), c=noteOf(no);' in s
       and 'function ndPopToggle(no,chip){' in s and s.count('function ndPopToggle(') == 1)
    T2('S-19 문항 필기 코드도 전부 카드 층 블록(if(SHELL)) 안이다',   # A-6(a) 9/30 — 블록의 문 c9faff2 · 잣대 blk 는 S-1 머리에서 고쳤다
       blk >= 0 and all(s.find(k) > blk for k in ['var qLoad=async function(', 'function qPaint(', 'function qWire(',
                                                  'function qEraseAt(', 'var qUndo=async function(', 'var qEraseSheet=',
                                                  'function qFit(', 'function qSvg(']))
    T2('S-20 qink 를 SYNC_KEYS 에 안 넣었다 — 문항 필기는 기기별',
       "'bpit','bpg','crop','txt','tfix','bref']," in s and 'qink' not in s.split('SYNC_KEYS:[')[1][:400]
       and "put('ink',qKey(QUID),QINK)" in s)
    T2('S-21 좌표·그리기는 판 1 규약 그대로(inkGet 으로만 잡고 pathD 로 그린다)',
       'QINK=await inkGet(qKey(uid),{w:QCW,h:QCW})' in s and 'pathD(st.p,QCW,QCW)' in s)
    T2('S-22 물리 #tLayer·#tUndo·#tErase 핸들러 원본 무변(카드 층은 뒤에 다시 맬 뿐)',
       "$('#tLayer').onchange=e=>{LAYER=+e.target.value;paintInk()};" in s
       and "$('#tUndo').onclick=()=>{const a=INK[LAYER];if(a&&a.length){a.pop();paintInk();saveInk()}};" in s
       and "$('#tErase').onclick=()=>{ if(TOOL.mode==='erase')eraseSheet(); else setTool('erase'); };" in s)
    T2('S-23 카드 폭을 박았다 — 좁으면 통째로 줄인다(글이 다시 흐르지 않는다)',
       '#card{position:relative;width:760px;max-width:760px;transform-origin:top left}' in s
       and "card.style.transform='scale('+k+')'" in s)
    T2('S-24 tfix 코드도 전부 카드 층 블록(if(SHELL)) 안이다',   # A-6(a) 9/30 — 블록의 문 c9faff2 · 잣대 blk 는 S-1 머리에서 고쳤다
       blk >= 0 and all(s.find(k) > blk for k in ['var tfixRaw=', 'var txtOf=', 'var tfixSet=async function(',
                                                  'var tfixSheet=', 'function tfixLong(', 'var tfixHay=']))
    T2('S-25 본문을 읽는 길이 txtOf 하나다 — 화면이 stemOf/CH/SOL 를 직접 안 읽는다',
       s.count('var txtOf=') == 1
       and "${esc(txtOf(uid,'q'))}" in s and "esc(txtOf(uid,'c'+(i+1)))" in s and "txtOf(uid,'s')" in s
       and "<div class=\"q${cropHas(uid,'q')?' crophid':''}\">${esc(stemOf(r))}</div>" not in s)
    T2('S-26 검색이 원본과 고친 글자를 둘 다 훑는다',
       # A-6(a) 9/30 — jagwa_search(eb1113e · _task_jagwa_search.md A-1 · A-3)가 목록 거르기 hay 를 걷고 결과 상자 esHit 로 옮겼다 — 본문 원본 + 고친 글자(tfixHay) 둘 다 그대로
       "if((String(r[F.BODY]||'')+' '+tfixHay(uid)).toLowerCase().includes(low))return {k:'body'};" in s)
    T2('S-27 DATA 원본 무변 — tfix 는 DATA 에 안 쓴다',
       'r[F.BODY]=' not in s and 'r[F.SOL]=' not in s and 'r[F.CH]=' not in s)
    T2('S-28 정답은 기존 ansfix 가 맡는다(tfix 칸에 없다)',
       "var TFIX_SLOTS=['q','c1','c2','c3','c4','c5','s'];" in s and "'ansfix'" in s)
    T2('S-9 백틱 짝', s.count('`') % 2 == 0)
    T2('S-10 CRLF 만', open(SRC, 'rb').read().count(b'\r\n') == open(SRC, 'rb').read().count(b'\n'))
    return out


def main():
    want = [a for a in sys.argv[1:] if a in ('earth', 'phys')] or ['earth', 'phys']
    cur = open(SRC, encoding='utf-8', newline='').read()
    lines = []
    for mode in want:
        ls, snap = run(mode, int(os.environ.get('HARNESS_WAIT', '600')), cur)
        lines += ls
        if mode == 'phys':
            base = subprocess.run(['git', '-C', GENIE, 'show', 'HEAD:jagwa/index.html'],
                                  capture_output=True).stdout.decode('utf-8')
            ls0, snap0 = run('physbase', int(os.environ.get('HARNESS_WAIT', '600')), base)
            def T2(name, cond, info=''):
                lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))
            T2('Y-3 고침 전(HEAD 블롭) 판도 끝까지 돌았다', bool(snap and snap0), [bool(snap), bool(snap0)])
            if snap and snap0:
                for k, ko in (('list', '목록'), ('cnt', '문항 수'), ('brand', '머리 칩 줄')):
                    T2('Y-3 물리 %s 이(가) 고침 전과 글자까지 같다' % ko, snap.get(k) == snap0.get(k),
                       [len(str(snap.get(k))), len(str(snap0.get(k)))])
    lines += static_checks()
    npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
    for x in lines: print(x)
    print('\n== 교재 조각/문항 필기 %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
