# -*- coding: utf-8 -*-
"""물리535 서재 — 학습기록 동기화 하니스 (2026-09-01)

앱 사본에 ① pdf.js·KaTeX 스텁 ② 가짜 GitHub 저장소(fetch 가로채기) ③ 검사를
주입해 헤드리스 크롬 --dump-dom 으로 돌린다. 원본은 건드리지 않는다.

「다른 기기」는 **사이드카(localStorage)와 전역을 백지로 되돌린 상태**로 흉내낸다 —
이 설계에서 기기를 가르는 것이 정확히 그 둘이기 때문이다. 저장소 파일은 그대로 둔다.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import functools, http.server, os, re, socketserver, subprocess, sys, threading

SRC = _roots.genie(r"jagwa\index.html")   # 9/5 자과 서재 이사(phys → jagwa)
OUT = os.path.join(os.environ.get('TEMP', '.'), 'physh')
os.makedirs(OUT, exist_ok=True)
APP = os.path.join(OUT, 'app.html')

# ── ① CDN 스텁 ─────────────────────────────────────────────────────
# pdfjsLib 은 첫 줄에서 바로 쓰이므로 없으면 스크립트 전체가 죽는다.
STUB = """<script>
window.pdfjsLib={GlobalWorkerOptions:{},getDocument:function(){return{promise:new Promise(function(){})}}};
window.katex={render:function(){},renderToString:function(s){return s}};
window.renderMathInElement=function(){};
window.__err=[];
window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+(e.filename||'').split('/').pop()+':'+e.lineno)});
window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
</script>
"""

# ── ② 가짜 GitHub + 검사 ───────────────────────────────────────────
TESTS = r"""<script>
(function(){
 const R=[]; const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+(c?'':' | '+JSON.stringify(i===undefined?null:i)));

 /* ---- 가짜 저장소 : path -> {text, sha} ---- */
 const __nativeFetch=window.fetch.bind(window);
 const REPO={};
 let nsha=0, putCount=0, rawBytesSeen=0, getCount=0, pdfGot=0;
 const enc=new TextEncoder();
 REPO['settings.json']={text:JSON.stringify({dayStart:5,exams:[{id:'ex1',name:'제64회 변리사 1차',date:'2027-02-20',del:false}]}),sha:'s0'};
 window.fetch=async function(url,opt){
  opt=opt||{};
  const m=/contents\/([^?]+)/.exec(String(url));
  const path=m?decodeURIComponent(m[1]):null;
  const J=(o,st)=>({ok:(st||200)<300,status:st||200,json:async()=>o,text:async()=>JSON.stringify(o)});
  if(!path)return{ok:false,status:404,json:async()=>({}),text:async()=>''};
  if((opt.method||'GET')==='GET'){
   getCount++;
   const f=REPO[path];
   if(!f)return{ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
   const acc=(opt.headers||{}).Accept||'';
   if(acc.indexOf('raw')>=0){rawBytesSeen=f.text.length;if(f.bin)pdfGot++;
    return{ok:true,status:200,text:async()=>f.text,json:async()=>JSON.parse(f.text),
           arrayBuffer:async()=>enc.encode(f.text).buffer}}
   return J({sha:f.sha});
  }
  const body=JSON.parse(opt.body);
  const cur=REPO[path];
  if(cur&&body.sha!==cur.sha)return{ok:false,status:409,json:async()=>({}),text:async()=>''};
  if(!cur&&body.sha)return{ok:false,status:409,json:async()=>({}),text:async()=>''};
  const txt=decodeURIComponent(escape(atob(body.content)));
  REPO[path]={text:txt,sha:'sha'+(++nsha)};putCount++;
  return J({content:{sha:REPO[path].sha}});
 };

 /* ---- 「다른 기기」로 만들기 : 사이드카·전역만 백지 ---- */
 async function becomeFreshDevice(){
  ['phys_sync_u','phys_sync_gone','phys_sync_shadow','phys_sync_meta'].forEach(k=>localStorage.removeItem(k));
  ST={};CMT={};QT={};CX={};GP={};TW={};AFIX={};FR={};MPOS={};OPOS={};
  for(const k of SYNC_KEYS)await put('kv',k,{});
 }
 const mark=(no,m,t,s)=>{ST[no]=ST[no]||{h:[]};ST[no].h.push({m:m,t:t||Date.now(),s:s||0})};
 const wait=ms=>new Promise(r=>setTimeout(r,ms));

 async function run(){
  try{
   recSaveToken('github_pat_TEST');
   await becomeFreshDevice();

   /* ===== P2 : 빈 프로필 + 토큰 → 기록.json 이 생기고 status 가 올라간다 ===== */
   mark(10,'O',Date.parse('2026-08-28T09:00:00'),120);
   await syncRecords(true);
   T('P2 기록.json 이 생겼다', !!REPO['phys/기록.json']);
   let F=JSON.parse((REPO['phys/기록.json']||{text:'{}'}).text);
   T('P2 status[10] 이 올라갔다', !!(F.data&&F.data.status&&F.data.status['10']), Object.keys((F.data||{}).status||{}));
   T('P2 열 개 키가 다 있다', SYNC_KEYS.every(k=>F.data&&F.data[k]), Object.keys(F.data||{}));
   T('P2 오류 없음(칩)', recErr==='', recErr);

   /* ===== P5 : ink 가 한 바이트도 없다 · 파일 20KB 미만 ===== */
   const raw=REPO['phys/기록.json'].text;
   T('P5 ink 키가 없다', !('ink' in (F.data||{})) && raw.indexOf('"ink"')<0);
   T('P5 set(설정) 도 없다', !('set' in (F.data||{})));
   T('P5 파일 20KB 미만', raw.length<20000, raw.length);

   /* ===== P3 : 두 기기 왕복 — 서로 덮지 않는다 ===== */
   await becomeFreshDevice();                    /* 기기 B */
   await syncRecords(true);                      /* B 가 원격을 받는다 */
   T('P3 B 가 A 의 문항10 을 받았다', !!ST['10'], Object.keys(ST));
   mark(20,'X',Date.now(),60);
   await syncRecords(true);
   F=JSON.parse(REPO['phys/기록.json'].text);
   T('P3 원격에 10 과 20 이 함께 있다', !!F.data.status['10']&&!!F.data.status['20'], Object.keys(F.data.status));

   await becomeFreshDevice();                    /* 기기 A 로 되돌아감 */
   await syncRecords(true);
   T('P3 A 에도 10 과 20 이 함께 보인다', !!ST['10']&&!!ST['20'], Object.keys(ST));
   T('P3 문항10 의 회독 시각이 보존됐다',
     ST['10'].h[0].t===Date.parse('2026-08-28T09:00:00'), ST['10'].h[0].t);

   /* ===== P4 : 묘비 — 지운 것이 되살아나지 않는다 ===== */
   CMT[10]='메모 하나';await put('kv','note',CMT);
   await syncRecords(true);
   F=JSON.parse(REPO['phys/기록.json'].text);
   T('P4-0 메모가 올라갔다', F.data.note['10']==='메모 하나', F.data.note);

   await becomeFreshDevice();                    /* 기기 B */
   await syncRecords(true);
   T('P4-1 B 가 메모를 받았다', CMT['10']==='메모 하나', CMT);

   await becomeFreshDevice();                    /* 기기 A */
   await syncRecords(true);
   await wait(5);
   delete CMT['10'];await put('kv','note',CMT);   /* A 에서 지운다 */
   stampAll();
   T('P4-2 묘비가 찍혔다', !!lsObj('phys_sync_gone')['note|10'], lsObj('phys_sync_gone'));
   T('P4-2 그림자에서도 빠졌다', !('10' in (lsObj('phys_sync_shadow').note||{})), lsObj('phys_sync_shadow').note);
   await syncRecords(true);
   F=JSON.parse(REPO['phys/기록.json'].text);
   T('P4-3 원격에서도 메모가 빠졌다', !('10' in F.data.note), F.data.note);
   T('P4-3 원격 묘비가 실렸다', !!F.gone['note|10']);

   await becomeFreshDevice();                     /* 기기 B — 옛 메모를 들고 있다고 가정 */
   CMT['10']='메모 하나';await put('kv','note',CMT);
   /* B 의 도장은 「지운 시각」보다 앞이어야 되살아나는지 볼 수 있다 */
   const uu=lsObj('phys_sync_u');uu['note|10']=1;lsPut('phys_sync_u',uu);
   const sh=lsObj('phys_sync_shadow');sh.note={'10':'메모 하나'};lsPut('phys_sync_shadow',sh);
   await syncRecords(true);
   T('P4-4 B 의 옛 메모가 되살아나지 않는다', !('10' in CMT), CMT);
   stampAll();
   T('P4-5 다음 도장이 되레 되살리지 않는다', !('10' in CMT) && !lsObj('phys_sync_u')['note|10'],
     {CMT:CMT,u:lsObj('phys_sync_u')['note|10']});
   await syncRecords(true);
   F=JSON.parse(REPO['phys/기록.json'].text);
   T('P4-6 왕복 뒤에도 원격이 깨끗하다', !('10' in F.data.note), F.data.note);

   /* ===== A-3 한계 확인 : 같은 문항을 두 기기에서 = 나중 것만 ===== */
   await becomeFreshDevice();
   await syncRecords(true);
   mark(30,'O',Date.parse('2026-08-30T10:00:00'));
   await syncRecords(true);
   await becomeFreshDevice();
   await syncRecords(true);
   const before=ST['30'].h.length;
   mark(30,'X',Date.parse('2026-08-31T10:00:00'));
   await syncRecords(true);
   F=JSON.parse(REPO['phys/기록.json'].text);
   T('A-3 한계 — 같은 문항은 통째 최신승(이력 합쳐지지 않음)',
     F.data.status['30'].h.length===before+1, F.data.status['30'].h.length);

   /* ===== 토큰 없음 ===== */
   const keep=recToken();
   recSaveToken('');
   recPaint();
   T('A-6 토큰 없으면 칩이 「○ 토큰 없음」', document.getElementById('recChip').textContent.indexOf('토큰 없음')>=0,
     document.getElementById('recChip').textContent);
   const n0=putCount;
   await syncRecords(true);
   T('A-6 토큰 없으면 올리지 않는다', putCount===n0);
   recSaveToken(keep);

   /* ===== A-6 D-day 칩 ===== */
   await loadExamSettings();
   const ec=document.getElementById('examChip');
   T('A-6 D-day 칩에 시험 이름과 D- 가 뜬다', /제64회 변리사 1차 D-\d+/.test(ec.textContent), ec.textContent);
   T('A-6 dayStart 를 settings.json 에서 읽었다', RECSET&&RECSET.dayStart===5, RECSET&&RECSET.dayStart);
   RECSET=null;recPaint();
   T('A-6 못 읽으면 칩을 아예 안 그린다', ec.style.display==='none'&&ec.textContent==='', [ec.style.display,ec.textContent]);
   await loadExamSettings();

   /* ===== 칩 상태 문구 넷 ===== */
   await syncRecords(true);
   recPaint();
   T('A-6 칩 = 동기화됨', document.getElementById('recChip').textContent.indexOf('동기화됨')>=0,
     document.getElementById('recChip').textContent);
   mark(40,'Q',Date.now());stampAll();
   const meta=lsObj('phys_sync_meta');meta.lastSync=1;lsPut('phys_sync_meta',meta);
   recPaint();
   T('A-6 칩 = 대기 N건', /대기 \d+건/.test(document.getElementById('recChip').textContent),
     document.getElementById('recChip').textContent);

   /* ===== P6 : 내보내기·불러오기 무변 ===== */
   T('P6 exportData 가 ink 를 그대로 싣는다', /out\.ink\[k\]=inkVals\[i\]/.test(exportData.toString()));
   T('P6 exportData 가 열 키 + set + ink 를 다 싣는다',
     ['status','set','maskpos','omrpos','note','qtype','conc','gpt','twin','ansfix','frm','ink']
       .every(k=>exportData.toString().indexOf(k+':')>=0));
   T('P6 importData 가 예전 그대로 열세 갈래를 읽는다(status…pdf)',
     /* 옛 줄: (_imp0.toString().match(/if\(j\./g)||[]).length===13&&/await _imp0\(/.test(importData.toString()), */
     (_imp0.toString().match(/if\(j\./g)||[]).length===13&&(/await _imp0\(/.test(importData.toString())||(/await _imp2\(f\)/.test(importData.toString())&&/uidMigrateImport\(\)/.test(importData.toString())&&typeof uidMigrateImport==='function'&&/^async function uidMigrateImport\(\)\{\s*if\(!CARD_LAYER\|\|!DATA_V\)return 0;/.test(uidMigrateImport.toString()))),   /* ★ uid_unify §A-2(10/4) — 들이기 뒤 옮김: uid 감쌈(_imp2 · 블록 const)이 층 importData 를 한 겹 더 감싸 끝에 uidMigrateImport — 물리는 그 첫 줄 !CARD_LAYER 로 0 · 열세 갈래는 _imp0 그대로 */
     /* ★ A-6(a) 9/30 — 셸 이식(c9faff2)부터 물리도 층 importData(감쌈 · 근거 gg·ggref = add5 §B-7)를 거쳐 옛 importData(_imp0)로 넘긴다 — 열세 갈래는 _imp0 에 그대로 */
     [(_imp0.toString().match(/if\(j\./g)||[]).length,/await _imp0\(/.test(importData.toString())]);

   /* ===== P11 : 사용법 팝업 템플릿 리터럴 ===== */
   const help=showSyncHelp.toString();
   T('P11 사용법 여닫이 백틱 수가 짝', (help.match(/`/g)||[]).length%2===0, (help.match(/`/g)||[]).length);
   T('P11 사용법에 ${ 가 0개', help.indexOf('${')<0);
   showSyncHelp();
   const sheets=document.querySelectorAll('.sheet');
   const hs=sheets[sheets.length-1];
   T('P11 사용법이 실제로 열린다', !!hs&&hs.textContent.indexOf('동기화 사용법')>=0);
   window.__helpText=hs?hs.textContent:'';
   hs.remove();

   /* ===== 설정 화면의 토큰 칸 ===== */
   document.getElementById('btnSet').click();
   const sb=document.querySelectorAll('.sheet');
   const st=sb[sb.length-1];
   T('A-4 설정에 🔑 토큰 칸이 있다', !!st.querySelector('#ftok'));
   T('A-4 토큰 칸이 password 다', st.querySelector('#ftok').type==='password');
   T('A-4 토큰을 화면에 다시 그리지 않는다',
     st.querySelector('#ftok').value===''&&st.innerHTML.indexOf('github_pat_TEST')<0);
   T('A-4 「지금 동기화」 단추가 있다', !!st.querySelector('#bSync'));
   st.querySelector('#bSync').click();
   for(let i=0;i<80&&!st.querySelector('#tokMsg').textContent;i++)await wait(25);
   T('A-4 「지금 동기화」가 결과를 적는다', st.querySelector('#tokMsg').textContent.length>0,
     st.querySelector('#tokMsg').textContent);
   st.remove();

   /* ===== 형식 ===== */
   F=JSON.parse(REPO['phys/기록.json'].text);
   T('형식 v/savedAt/by/data/u/gone', ['v','savedAt','by','data','u','gone'].every(k=>k in F), Object.keys(F));
   T('형식 by = tt.cfg.person', F.by===(JSON.parse(localStorage['tt.cfg']).person), F.by);
   T('경로가 phys/기록.json', REC_PATH==='phys/기록.json', REC_PATH);
   T('저장소 = zzikkaplan/studyplandata · main', REC_REPO==='zzikkaplan/studyplandata'&&REC_BRANCH==='main');
   T('raw 로 받는다(1MB 초과 대비)', rawBytesSeen>0);

   /* ===== §B 저장소에서 시험지 받기 ===== */
   const fake=id=>'%PDF-1.4 fake '+id;
   ['111','222','333','444','555','666'].forEach((id,k)=>{
    REPO['phys/pdf/'+id+'.pdf']={text:fake(id),sha:'p'+k,bin:1}});
   REPO['phys/pdf/시험지메타.json']={text:JSON.stringify({v:1,files:{
    '111':{md5:'m1'},'222':{md5:'m2'},'333':{md5:'m3'},
    '444':{md5:'m4'},'555':{md5:'m5'},'666':{md5:'m6'}}}),sha:'pm'};
   T('§B Contents API 로 받는다(ghUrl)', /api\.github\.com/.test(ghUrl.toString())&&/ghUrl\(PDF_DIR/.test(tryRemote.toString()));
   T('§B Accept 가 vnd.github.raw', /vnd\.github\.raw/.test(tryRemote.toString()));
   T('§B Bearer 토큰을 붙인다', /Bearer/.test(tryRemote.toString()));
   T('§B %PDF 머리 검사를 그대로 뒀다', /%PDF/.test(tryRemote.toString()));
   T("§B put('pdf',key,buf) 흐름 무변", /put\('pdf',key,buf\)/.test(tryRemote.toString()));
   T('§B 딱지 경로 = phys/pdf/시험지메타.json', PDF_META==='phys/pdf/시험지메타.json', PDF_META);

   for(const k of await keys('pdf'))await del('pdf',k);
   await put('kv','pdfhash',{});await loadHave();
   let n1=getCount;
   await ensureFiles(true);
   await loadHave();
   T('§B 여섯 개를 다 받았다', ['111','222','333','444','555','666'].every(f=>HAVE[f]),
     Object.keys(HAVE));
   T('§B 받은 md5 를 적어 뒀다', ((await get('kv','pdfhash'))||{})['111']==='m1',
     await get('kv','pdfhash'));
   let n2=getCount;
   await ensureFiles(true);
   T('§B 두 번째는 바뀐 것이 없어 한 개도 안 받는다', getCount-n2<=2, getCount-n2);
   T('§B 「모두 최신입니다」를 알린다',
     document.getElementById('dl').textContent.indexOf('모두 최신')>=0,
     document.getElementById('dl').textContent);
   /* 한 개만 바뀌면 그 하나만 */
   REPO['phys/pdf/시험지메타.json'].text=JSON.stringify({v:1,files:{
    '111':{md5:'m1'},'222':{md5:'m2-NEW'},'333':{md5:'m3'},
    '444':{md5:'m4'},'555':{md5:'m5'},'666':{md5:'m6'}}});
   pdfGot=0;
   await ensureFiles(true);
   T('§B 바뀐 한 개만 다시 받는다', pdfGot===1, pdfGot);
   T('§B 새 md5 로 갱신했다', ((await get('kv','pdfhash'))||{})['222']==='m2-NEW');
   /* 토큰이 없으면 안내 */
   const keep2=recToken();recSaveToken('');
   pdfGot=0;
   await ensureFiles(true);
   T('§B 토큰 없으면 받지 않는다', pdfGot===0);
   T('§B 토큰 없으면 안내를 띄운다',
     document.getElementById('dl').textContent.indexOf('토큰이 없습니다')>=0,
     document.getElementById('dl').textContent);
   recSaveToken(keep2);

   /* ===== §D 사용법 문안 대조 — 가리키는 것이 실물에 다 있는가 ===== */
   showSyncHelp();
   const shs=document.querySelectorAll('.sheet');
   const hp=shs[shs.length-1];const hx=hp.textContent;
   hp.remove();
   document.getElementById('btnSet').click();
   const s2=document.querySelectorAll('.sheet');
   const sp=s2[s2.length-1];const sx=sp.textContent;
   [['🔑 토큰 · 기록 동기화','설정 칸 이름'],
    ['토큰 저장하고 동기화','단추'],
    ['필기·진도만 내보내기 (가벼움)','단추'],
    ['PDF까지 전부 내보내기 (무거움)','단추'],
    ['백업 파일 불러오기','단추'],
    ['저장소에서 시험지 받기','단추'],
    ['PDF 등록','칸 이름']].forEach(p=>{
    T('§D 문안이 가리킨 「'+p[0]+'」('+p[1]+')이 실물에 있다',
      hx.indexOf(p[0])>=0&&sx.indexOf(p[0])>=0, [hx.indexOf(p[0]),sx.indexOf(p[0])]);
   });
   sp.remove();
   /* 칩 넷 — 사용법이 적은 글자가 recPaint 가 내는 글자와 같아야 한다 */
   const chipTexts=[];
   recBusy=true;recPaint();chipTexts.push($('#recChip').textContent);recBusy=false;
   recSaveToken('');recPaint();chipTexts.push($('#recChip').textContent);recSaveToken(keep2);
   lsPut(SMETA_KEY,{lastSync:Date.now()});stampAll();recPaint();
   chipTexts.push($('#recChip').textContent);
   mark(99,'O',Date.now());stampAll();lsPut(SMETA_KEY,{lastSync:1});recPaint();
   chipTexts.push($('#recChip').textContent);
   T('§D 칩 넷을 다 적었다(⟳ / ● 동기화됨 / ● 대기 / ○ 토큰 없음)',
     chipTexts.every(t=>hx.indexOf(t.replace(/\d+/,'N'))>=0
                     ||hx.indexOf(t.split(' ')[0]+' '+t.split(' ')[1])>=0),
     chipTexts);
   T('§D 「자동」이라고 적었다', /3분마다/.test(hx)&&/저절로/.test(hx));
   T('§D 「필기는 자동이 아니다」를 적었다', hx.indexOf('필기는 자동이 아닙니다')>=0||hx.indexOf('필기는 이제 자동입니다')>=0);   /* ★ 10/8 jagwa_ink_sync 첫 줄 · §A-3 — 필기도 기록과 같은 고리로 저절로 동기화 → 사용법 글이 「필기는 이제 자동입니다」로 바뀜(옛 글 = 바탕도 PASS · 이름은 저장본 맞대기 때문에 그대로) */
   T('§D A-3 한계를 적었다', hx.indexOf('한 문항을 두 기기에서')>=0);
   T('§D 옛 거짓말 셋이 사라졌다',
     hx.indexOf('자동 동기화는 없습니다')<0
     &&hx.indexOf('「저장소에서 시험지 받기」는 지금 안 됩니다')<0
     &&hx.indexOf('PDF 와 필기가 함께 날아갑니다')<0);
   T('§D 사이트 데이터 삭제 문장이 PDF·필기만 가리킨다',
     /<b>PDF 와 필기가<\/b> 날아갑니다/.test(showSyncHelp.toString()));

   /* ===== P10 : 콘솔 오류 0 ===== */
   T('P10 잡히지 않은 오류 0건', (window.__err||[]).length===0, window.__err);

  }catch(e){R.push('FAIL | 하니스가 터짐 | '+(e&&e.stack||e))}
  report(R.join('\n'));
 }
 /* 결과는 DOM 이 아니라 서버로 보낸다 — --dump-dom 은 IndexedDB 를 기다려 주지 않는다
    (--virtual-time-budget 은 실제 I/O 인 IndexedDB 와 함께 돌지 않는다). */
 function report(txt){
  try{__nativeFetch('/result',{method:'POST',body:txt})}catch(e){}
  const pre=document.createElement('pre');pre.id='RESULT';
  pre.textContent=txt;document.body.appendChild(pre);
 }
 /* 앱 시동이 끝나기를 기다린다 — db 가 열리고 recBoot 이 칩을 한 번 칠한 뒤 */
 (function w(n){if(typeof recPaint==='function'&&document.getElementById('recChip').textContent){window.__booted=1;return}
  if(n>400)return;setTimeout(()=>w(n+1),20)})(0);
 (function boot(n){
  if(typeof syncRecords==='function'&&typeof db!=='undefined'&&db&&window.__booted)return run();
  if(n>400)return report('FAIL | 앱이 시동되지 않음 | '+JSON.stringify(window.__err||[]));
  setTimeout(()=>boot(n+1),25);
 })(0);
})();
</script>
"""


def main():
    html = open(SRC, encoding='utf-8', newline='').read()
    assert '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js' in html
    html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js',
                        STUB + '<script data-off="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    # KaTeX / pdf.js 를 실제로 받지 않게 막는다(오프라인 재현성)
    html = html.replace('<script defer src="https://cdnjs', '<script defer data-off="https://cdnjs')
    html = html.replace('<link rel="stylesheet" href="https://cdnjs', '<link rel="off" href="https://cdnjs')
    assert html.rstrip().endswith('</html>')
    html = html.replace('</body>', TESTS + '</body>', 1)
    open(APP, 'w', encoding='utf-8', newline='').write(html)

    # ⚠ IndexedDB 는 file:// 오리진에서 막힌다 — 이 앱은 IndexedDB 가 뿌리라
    # tt 하니스처럼 file:// 로 열면 시동 자체가 안 된다. 짧게 서버를 띄운다.
    # ⚠ --dump-dom + --virtual-time-budget 도 못 쓴다 — 가상시간은 IndexedDB 의
    #   실제 I/O 를 기다려 주지 않아 검사가 시작되기도 전에 DOM 이 찍힌다.
    #   그래서 페이지가 결과를 POST /result 로 보내고 여기서 그걸 기다린다.
    done = threading.Event()
    box = {}

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=OUT, **k)
        def log_message(self, *a, **k):
            pass
        def do_POST(self):
            n = int(self.headers.get('Content-Length') or 0)
            box['txt'] = self.rfile.read(n).decode('utf-8', 'replace')
            self.send_response(204); self.end_headers()
            done.set()

    srv = socketserver.TCPServer(('127.0.0.1', 0), H)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    prof = os.path.join(OUT, 'prof')
    url = 'http://127.0.0.1:%d/app.html' % port
    p = subprocess.Popen([chrome, '--headless=new', '--disable-gpu', '--no-first-run',
                          '--user-data-dir=' + prof, '--window-size=1280,900', url],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    got = done.wait(120)
    p.terminate()
    try:
        p.wait(10)
    except Exception:
        p.kill()
    srv.shutdown()

    if not got:
        print('결과 없음 — 120초 안에 검사가 끝나지 않았다')
        sys.exit(1)
    open(os.path.join(OUT, 'result.txt'), 'w', encoding='utf-8').write(box['txt'])
    lines = [ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()]

    # ---- 브라우저 밖 검사 (파일 층) ----
    def T2(name, cond, info=''):
        lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))
    s = open(SRC, encoding='utf-8').read()
    T2('P5 소스에 ink 동기화가 없다', "'ink'" not in s.split('SYNC_KEYS=')[1].split(']')[0])
    T2('P1 minbeop 무접촉(이 파일은 phys 뿐)', 'minbeop' not in s.replace('민법앱(`minbeop/index.html`)의 실물을 읽고 옮겼다', '').replace('minbeop .clsrc 97~99 · .ggclhd 94~96', ''))   # ★ 합치기 10/1(하위 에이전트 C) — search_claude(e9de3b8) CSS 주석 「minbeop .clsrc 97~99 · .ggclhd 94~96」(민법 값 출처 표기 · 코드 접촉 아님)도 뺀다   # ★ A-6(a) 9/30 — 지학 listpop_add1(genie cd248a5)이 「민법앱 실물을 읽고 옮겼다」 주석 한 줄을 남김(코드 접촉 아님) — 그 주석만 빼고 잰다
    T2('A-4 토큰을 HTML 에 박지 않았다', 'github_pat_' not in s.replace('github_pat_\u2026', ''))
    T2('A-5 도장 10초·동기화 180초', ',10000)' in s and ',180000)' in s)
    body = s
    T2('P11 파일 전체 백틱 수가 짝', body.count('`') % 2 == 0, body.count('`'))

    npass = sum(1 for x in lines if x.startswith('PASS'))
    nfail = len(lines) - npass
    for x in lines:
        print(x)
    print('\n== %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
