# -*- coding: utf-8 -*-
r"""_task_jagwa_bundles_1013 §3 관문 [클라우드] — 자과: 물리 목차 서랍 「묶음 [N]」 · 왜 묶나 작은 창 · 문제 창 제목 길게 눌러 고치기(물리 · 지학 · 생물)

  python _harness_jagwa_bundles.py [--new <앱>] [--base <판 = 2a0bbf3>] [--eng chromium,webkit] [--only B1,T2,…] [--spd <studyplandata>] [--notes <notes>] [--vendor <cdnjs 사본>] [--res <결과>]

  NEW = genie 작업트리 jagwa/index.html · BASE = 바탕 main 2a0bbf3(앱 LF md5 18323cd8 = 69126e7 판 · 헛잣대 — B1 · B2 · B3 · T1~T7 바탕 FAIL · B4 · T8 · T9 바탕도 PASS)
  엔진 = Chromium · WebKit · PC 1100×800 마우스 · 폰 384×740 hasTouch(Chromium = CDP 손가락 · WebKit = touchscreen.tap · 길게 = 합성 touch 포인터 WK_LONG) · 원격 = 가짜(공용 JG.Remote · PUT 밖으로 0)
  세 과목 = 공용 Pg_PP subj(phys · earth · bio = 앱 localStorage subj · 지시서 「?subj=」 와 같은 과목 고르기)
  시험 글 = 지어낸 것(제목 「쿼즐…」 · 근거 · 글자 고치기 글) 또는 앱에 이미 있는 묶음 표 · 단원 이름 · 기록 = 빈 기록(문항 · 시각 · 근거 글 0) — 앱 제목 · 문항 글은 출력에 안 옮김(같음 · md5 앞 8 자 · D11)
  길게 = 600ms · 짧게 = 150ms(지시서 값 · 공용 long_press 는 900ms 아래로 못 내려 이 하네스가 손수 누름) · 길게 뒤 click 셈 = 문서 거품 단계 click 수(앱이 잡기 단계에서 먹으면 0 · WebKit 은 합성 click 하나를 보내 먹는지 잼)
  칸:
    B1 물리 서랍 단원 머리 63 다 .ndbd · 1.11 「등속 원운동」 = [5] · 앱 안에서 BUNDLES 를 DATA 로 다시 셈 = 24 묶음 · 63 단원 · 577 문항 · 빠짐 0 · 겹침 0 · 묶음 단원 이름 = 서랍 단원 이름
    B2 [N] 누름(마우스 · 손가락) = #bdPop · 머리 「[N] 이름 a+e=n」 · 왜 묶나 · 단원 줄 수 = 묶음 단원 수 · 지금 단원 .cur · 줄마다 a = PA 수 · e = 나머지(DATA 로 셈) · 「기출」 「PEM」 0 · 화면 안
    B3 같은 [N] 다시 = 닫힘 · 바깥 누름 = 닫힘 · g3Pop ↔ bdPop 서로 닫음(누름 · 함수) · [N] 누름이 서랍 접기 · 첫 화면 스크롤 · 문항 열기 0(대조 = 머리 이름 누름은 스크롤 됨)
    B4 지학 · 생물 서랍 .ndbd 0
    T1 물리 #vT1 길게 600ms(마우스 · 손가락) = .vtt.ied .iedin · 값 = titleOf · 폰 줄 오른쪽 끝(말줄임 · 제목 글자 밖)도 · 짧게 150ms = 안 열림
    T2 지어낸 제목 Enter → TFIX['P###'].nm · 머리 .vtt.fx · 서랍 .ndtt.fx · 정리 창 .pnm · 첫 화면 목록 .item .sub.pnfx · 다시 열기 · 새로고침 · Esc · 바깥 = 안 바뀜 · 비우고 저장 = 원래 · fx 없음
    T3 서랍 줄 제목 길게 → 저장 → 머리 제목 같은 글
    T4 폰 잘린 제목 짧게 = #g3Tip → 이어 길게 = 칸 · #g3Tip 없음 · click 안 샘 · 칸 안 누름 = 칸 그대로
    T5 지학 기출 G… · 확인문제 · 생물: 머리 원래 = 소단원 이름 · 길게 = 칸 · 저장 TFIX[uid].nm · 파랑 · 서랍 꼬리 .ndtt.fx · 서랍 파랑 제목 길게 = 칸 · 비우면 옛 꼴(+ 지학 폰 손가락)
    T6 카드 층: 위 검색(문제)에 고친 제목 낱말 → 그 문항 · tfixAny 거짓 · 글자 고치기(문제 칸 길게 → tfixSheet) 표시 = 바탕 · 「이 글을 쓴 문항」 창 제목 누름 → 비교 창 제목 = 고친 제목
    T7 동기화(공용 원격 흉내 · 기기 둘) — 고침 · 비움이 B 로 감(물리 · 지학)
    T8 다른 길게 누름 무변 — 정리 창 이름 .pnm · 공식 칸 .frcell 길게 = 고치기 칸 · 짧게 = 안 열림(= 바탕)
    T9 위 화면 페이지 오류 0 · 가로 넘침 0 · 폰 ✓ 보임 · 입력 칸 높이 ≤ 26 · 새로 뜬 창(#bdPop · #g3Tip) 높이 ≤ innerHeight/3
  모드 — gate = 바탕 띄움 · regress · smoke = 새 판만(smoke = B1 · B2 PC 크롬)
"""
import os as _os_r, sys as _sys_r   # env_lanes — _roots.py 를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402,F401 — --mode · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음
import _qa_jagwa_common as JG   # noqa: E402
import hashlib, json, os, sys, tempfile, time, traceback   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEWF = ARG('--new', _roots.genie('jagwa', 'index.html'))
BASE = ARG('--base', '2a0bbf3')
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
TMPD = os.path.join(tempfile.gettempdir(), 'h_jagwa_bundles')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_jagwa_bundles_result.txt'))
SPD = ARG('--spd', _roots.spd())
NOTES = ARG('--notes', os.path.join(os.path.dirname(_roots.spd()), 'notes'))
VENDOR = ARG('--vendor', os.path.join(TMPD, 'vendor'))
JG.conf(VENDOR_PP=VENDOR, SPD_PP=SPD, NOTES=NOTES, SHOTS=os.path.join(TMPD, 'shots'))
GATE = QC.GATE
if GATE:
    QC.sub('git:show-app')
SRC = {'NEW': JG.app_src(NEWF)}
if GATE:
    SRC['BASE'] = JG.app_src(BASE)
PC, PH = (1100, 800), (384, 740)
LONG, SHORT = 600, 150
RES = []
SMOKE_CELLS = {'B1', 'B2'}
# 지어낸 글(시험용 · 앱 · 기록에 없는 낱말 「쿼즐」)
NEWT = '쿼즐 제목 시험가'
NEWT3 = '쿼즐 서랍 제목나'
NEWTE = '쿼즐뭉 카드 제목'
WORD = '쿼즐뭉제목'
NEWTW = WORD + ' 찾기'
TXTQ = '쿼즐 문제 글 고침 시험'
TRIG = '쿼즐뭉 트리거 시험 근거'
NEWT7 = '쿼즐 동기화 제목'
TMPT = '쿼즐 취소될 글'


def want(c):
    return (not ONLY or c.upper() in ONLY) and (not QC.SMOKE or c in SMOKE_CELLS)


def _s(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


def h8(s):
    return hashlib.md5(' '.join(str(s or '').split()).encode('utf-8')).hexdigest()[:8]


def _h6(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()[:6]


def R(g, name, new, base=None, d='', yard=True):
    RES.append(dict(g=g, name=name, new=new, base=base, yard=yard, d=d))
    tag = 'INFO' if new is None else ('PASS' if new else 'FAIL')
    yb = '' if base is None else (' · 바탕 ' + (('PASS(바탕도 같음)' if not yard else 'PASS') if base else ('FAIL' if yard else 'FAIL(바탕도 같아야 할 칸)')))
    print('%s | %s · %s%s | %s' % (tag, g, name, yb, _s(d)[:900]), flush=True)


def safe(o, k, fn):
    try:
        o[k] = fn()
    except Exception:
        o[k] = {'하네스 오류': traceback.format_exc()[-600:]}


SYNCED_JS = "()=>typeof recBusy!=='undefined'&&!recBusy&&(((lsObj(SMETA_KEY).lastSync||0)>=performance.timeOrigin)||!!recErr)"   # physphone _RG_SYNCED 꼴 — 부팅 첫 syncRecords 끝


def _pg(br, eng, tag, ver, subj, dev, touch, who='하네스', remote=None):
    p = JG.Pg_PP(br, eng, '%s-%s-%s' % (tag, eng, _h6(SRC[ver])), SRC[ver], subj, dev, touch=touch, who=who, remote=remote or JG.Remote())
    QC.until(p.pg, SYNCED_JS, 15000, '부팅 첫 syncRecords 끝(recBusy 거짓 · lastSync ≥ 쪽 열림 또는 recErr) — 끝난 뒤 서랍 · 목록을 다시 그려 누를 자리가 바뀜')
    p.wait(400)
    return p


# ══ JS ════════════════════════════════════════════════════════════════════════════════
OPEN_JS = r"""async (no)=>{try{await openView(no)}catch(e){return 'ERR '+e}for(let i=0;i<40;i++){await new Promise(r=>setTimeout(r,100));if(VNO===no&&(!HASBOOK||String(QUID)===String(qk(no))))break}
  try{setTool('view')}catch(e){}await new Promise(r=>setTimeout(r,500));return VNO}"""
# 작은 창 닫기 = 몸통 pointerdown 하나(앱 bdPopOut · g3PopOut 이 받음 — bdPopClose · g3PopClose 는 gg3 덩어리 안 함수라 밖에서 못 부름)
BODYPD = "document.body.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,cancelable:true,composed:true}));"
CLEAN_JS = r"""async ()=>{try{if(IED)IED.done(false)}catch(e){}document.querySelectorAll('#gguw,#jnw,#pwl,#tfxSheet,.vpin,#g3Tip').forEach(x=>x.remove());""" + BODYPD + r"""
  await new Promise(r=>setTimeout(r,200));return 1}"""
CLOSEV_JS = r"""async ()=>{try{if(IED)IED.done(false)}catch(e){}try{closeView()}catch(e){}document.querySelectorAll('#gguw,#jnw,#pwl,#tfxSheet,.vpin,#g3Tip').forEach(x=>x.remove());""" + BODYPD + r"""
  await new Promise(r=>setTimeout(r,400));return document.getElementById('view').classList.contains('hide')}"""
# 첫 화면 목록에 그려진 물리 문항(기록 · 고친 글 없음 · 제목 2~40 자)
PICKP_JS = r"""(n)=>{const out=[];for(const it of document.querySelectorAll('#list .item[data-pv]')){const u=it.dataset.pv,r=rowByUid(u);if(!r)continue;const no=r[F.NO];
  if(hist(no).length||TFIX[u]||out.indexOf(no)>=0)continue;const t=String(titleOf(r)||'');if(t.length<2||t.length>40)continue;out.push(no);if(out.length>=n)break}return out}"""
# 카드 층 문항 — 기출(ynUid) · 확인(isC) · 그 밖 · 기록 · 고친 글 · 근거 없음
PICKC_JS = r"""()=>{const g=[],c=[],o=[];for(const r of DATA){const no=r[F.NO],u=GGU(r);if(hist(no).length||TFIX[u]||(typeof ggOf==='function'&&ggOf(u).filter(Boolean).length))continue;if(!unitOf(no))continue;
  if(isC(r)){if(c.length<2)c.push(no)}else if(ynUid(r)){if(g.length<3)g.push(no)}else if(o.length<3)o.push(no)}return {g,c,o}}"""
B1_JS = r"""()=>{const S=[...document.querySelectorAll('#ndList .ndsec')],NM=h=>String(unitName(h.dataset.sec)||'');
  const heads=S.length,withBd=S.filter(h=>h.querySelector('.ndbd')).length,h111=S.find(h=>NM(h)==='등속 원운동');
  const o={heads,withBd,bd111:h111&&h111.querySelector('.ndbd')?h111.querySelector('.ndbd').textContent:null,sec111:h111?h111.dataset.sec:null,data:DATA.length};
  const B=window.BUNDLES;if(!Array.isArray(B)){o.B=null;return o}
  const units=[].concat(...B.map(b=>b.u.map(x=>x[1]))),cnt={};units.forEach(n=>cnt[n]=(cnt[n]||0)+1);
  const set=new Set(units);let q=0,miss=0,pa=0;DATA.forEach(r=>{if(set.has(r[F.SUB])){q++;if(/^PA/.test(String(r[F.CODE])))pa++}else miss++});
  const dn=new Set(S.map(NM)),by={};B.forEach(b=>b.u.forEach(x=>{by[x[1]]=b.n}));
  const wrong=S.filter(h=>{const e=h.querySelector('.ndbd');return !e||+e.dataset.bd!==by[NM(h)]||e.textContent!=='['+by[NM(h)]+']'}).map(h=>h.dataset.sec);
  return Object.assign(o,{B:B.length,ns:B.map(b=>b.n).join(',')===B.map((b,i)=>i+1).join(','),units:units.length,q,pa,miss,dup:Object.keys(cnt).filter(n=>cnt[n]>1).length,
    nameMiss:units.filter(n=>!dn.has(n)).length,wrong:wrong.length,wrongAt:wrong.slice(0,4)})}"""
BIG_JS = r"""()=>{const B=window.BUNDLES||[];let b=null;B.forEach(x=>{if(!b||x.u.length>b.u.length)b=x});return b?{n:b.n,nm:b.u[0][1],k:b.u.length}:null}"""
# 단원 머리 — 그 이름 머리를 서랍 안에서 가운데로 · [N] · 이름 · ▾ 누를 자리
#   머리 .ndsec 는 position:sticky(top 0) — 지나간 머리는 맨 위에 겹쳐 붙어 scrollIntoView 가 안 움직임(뒤 머리가 덮음) → 서랍 맨 위로 돌린 뒤 가운데로
HEAD_JS = r"""(nm)=>{const h=[...document.querySelectorAll('#ndList .ndsec')].find(x=>String(unitName(x.dataset.sec)||'')===nm);if(!h)return null;
  const L=document.getElementById('ndList');if(L)L.scrollTop=0;try{h.scrollIntoView({block:'center'})}catch(e){}const b=h.querySelector('.ndbd'),n=h.querySelector('.nm');
  return {sec:h.dataset.sec,bd:b?__H.at(b):null,nm:n?__H.at(n):null,n:b?+b.dataset.bd:null}}"""
BDAT_JS = r"""(sec)=>{const b=document.querySelector('#ndList .ndsec[data-sec="'+sec+'"] .ndbd');return b?__H.at(b):null}"""
BDPOP_JS = r"""(sec)=>{const P=document.getElementById('bdPop'),on=!!document.querySelector('#ndList .ndsec[data-sec="'+sec+'"] .ndbd.on');if(!P)return {pop:false,on};
  const W=s=>String(s==null?'':s).replace(/\s+/g,' ').trim(),T=e=>e?W(e.textContent):'';
  const nm=String(unitName(sec)||''),B=window.BUNDLES||[],b=B.find(x=>x.u.some(u=>u[1]===nm));
  const C=ns=>{let a=0,e=0;DATA.forEach(r=>{if(ns.indexOf(r[F.SUB])<0)return;if(/^PA/.test(String(r[F.CODE])))a++;else e++});return a+'+'+e+'='+(a+e)};
  const h=P.querySelector('.bdh'),rows=[...P.querySelectorAll('.bdu .bdr')];
  const want=b?b.u.map(u=>({no:u[0],nm:u[1],rg:C([u[1]])})):[];
  const got=rows.map(x=>({no:T(x.querySelector('b')),tx:T(x),rg:T(x.querySelector('.rg')),cur:x.classList.contains('cur')}));
  const curs=got.map((g,i)=>g.cur?i:-1).filter(i=>i>=0),r=P.getBoundingClientRect(),all=b?C(b.u.map(u=>u[1])):null;
  return {pop:true,on,n:b?b.n:null,
    headOk:!!b&&T(h&&h.querySelector('b'))==='['+b.n+']'&&T(h)===W('['+b.n+'] '+b.nm+' '+all)&&T(h&&h.querySelector('.bdc'))===all,
    whyOk:!!b&&T(P.querySelector('.bdw'))===W(b.why),
    rowsOk:!!b&&got.length===want.length&&got.every((g,i)=>g.no===want[i].no&&g.tx===W(want[i].no+' '+want[i].nm+' '+want[i].rg)&&g.rg===want[i].rg),
    curOk:curs.length===1&&!!want[curs[0]]&&want[curs[0]].nm===nm,nRows:got.length,nWant:want.length,head:all,rg:got.map(g=>g.rg),
    noWord:!/기출|PEM/.test(P.textContent),
    rect:{l:Math.round(r.left),t:Math.round(r.top),r:Math.round(r.right),b:Math.round(r.bottom),h:Math.round(r.height)},iw:innerWidth,ih:innerHeight,
    inScreen:r.left>=0&&r.top>=0&&r.right<=innerWidth+0.5&&r.bottom<=innerHeight+0.5}}"""
# 첫 화면 상태(B3 새는 일 재기) — 목록 자리 · 서랍 접기 · 단원 접기 · 본창 · 지금 문항
FS_JS = r"""(sec)=>{const L=document.getElementById('list'),h=document.querySelector('#ndList .ndsec[data-sec="'+sec+'"]'),v=document.getElementById('view');
  let off='';try{off=[...ndSecSet()].sort().join(',')}catch(e){}let scr=Math.round(scrollY);for(let e=L&&L.parentElement;e;e=e.parentElement)scr+=Math.round(e.scrollTop||0);
  return {scr,top:L?Math.round(L.getBoundingClientRect().top):null,sy:Math.round(scrollY),fold:document.getElementById('navdr').classList.contains('fold'),
    off:h?h.classList.contains('off'):null,offSet:off,view:!!v&&!v.classList.contains('hide'),vno:VNO||0,ndoff:document.querySelectorAll('#ndList .ndrow.ndoff').length}}"""
POPS_JS = r"""()=>({bd:!!document.getElementById('bdPop'),g3:!!document.getElementById('g3Pop'),bdOn:document.querySelectorAll('#ndList .ndbd.on').length})"""
# 바깥 누름 자리 — 누를 것 · 창 · 서랍 · 제목 줄 밖(앱이 아무 일 안 하는 글 · 빈 자리) · 둘레 ±10px 안에도 누를 것 없음
#   (크롬 손가락 = 닿은 둘레 안 누를 것으로 자리 맞춤 — 폰 첫 화면 머리 줄 빈 자리를 누르면 옆 과목 탭(#subjTabs)이 눌려 지학으로 바뀐 것을 잼)
NEUTRAL_JS = r"""(ex)=>{const bad='button,a,input,textarea,select,label,[data-go],.item,.chchip,.ndrow,.ndsec,.ndbd,.ndox,#bdPop,#g3Pop,#g3Tip,#navdr,#navTg,#vT1,.ied,[onclick],[data-esq],.jgo,.pnm,.frcell,canvas,svg,img,.sheet,.twhandle,#ndGrip,.vtop,#subjTabs,#recChip,#examChip,[role=button],[tabindex]';
  const BAD=t=>{if(!t||t===document.documentElement||t===document.body)return true;if(t.closest(bad)||(ex&&t.closest(ex)))return true;for(let e=t;e&&e!==document.body;e=e.parentElement){if(getComputedStyle(e).cursor==='pointer')return true}return false};
  const xs=[0.95,0.9,0.85,0.8,0.75,0.7,0.66,0.6,0.55,0.5],ys=[0.03,0.05,0.07,0.09,0.12,0.14,0.17,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95];
  for(const fy of ys)for(const fx of xs){const x=Math.round(innerWidth*fx),y=Math.round(innerHeight*fy);let ok=true;
    for(const dx of [-10,-5,0,5,10]){for(const dy of [-10,-5,0,5,10]){if(BAD(document.elementFromPoint(x+dx,y+dy))){ok=false;break}}if(!ok)break}
    if(!ok)continue;const t=document.elementFromPoint(x,y);
    return {cx:x,cy:y,on:true,top:(t.id?'#'+t.id:t.tagName.toLowerCase()+'.'+String(t.className||'').slice(0,24))}}
  return null}"""
SEED_JS = r"""async (marks)=>{const t0=Date.now()-3600000;for(const [no,m] of marks)ST[qk(no)]={h:[{m,t:t0,s:40}]};await saveST();try{navBuild()}catch(e){}
  return marks.map(([no])=>!!document.querySelector('#ndList .ndox[data-ox="'+no+'"]'))}"""
OX_AT = r"""(no)=>{const x=document.querySelector('#ndList .ndox[data-ox="'+no+'"]');if(!x)return null;try{x.scrollIntoView({block:'center'})}catch(e){}return __H.at(x)}"""
G3X_JS = r"""([no,n,sec])=>{const ox=document.querySelector('#ndList .ndox[data-ox="'+no+'"]'),bd=document.querySelector('#ndList .ndsec[data-sec="'+sec+'"] .ndbd');if(!ox||!bd)return null;
  """ + BODYPD + r"""
  bdPopToggle(n,bd);const a={bd:!!document.getElementById('bdPop'),g3:!!document.getElementById('g3Pop')};
  g3PopToggle(no,ox);const b={bd:!!document.getElementById('bdPop'),g3:!!document.getElementById('g3Pop')};
  bdPopToggle(n,bd);const c={bd:!!document.getElementById('bdPop'),g3:!!document.getElementById('g3Pop')};
  """ + BODYPD + r"""return {a,b,c}}"""
# 문제 창 제목 줄
VT_JS = r"""(no)=>{const t=document.getElementById('vT1'),v=t&&t.querySelector('.vtt'),r=rec(no);
  const inp=t&&t.querySelector('.vtt.ied .iedin'),ok=t&&t.querySelector('.vtt.ied .iedok');
  let okHit=null,okIn=null,okR=null;if(ok){const q=ok.getBoundingClientRect(),e=document.elementFromPoint(q.left+q.width/2,q.top+q.height/2);okHit=!!e&&(e===ok||ok.contains(e));
    okIn=q.left>=0&&q.right<=innerWidth+0.5&&q.top>=0&&q.bottom<=innerHeight+0.5;okR=[Math.round(q.width),Math.round(q.height)]}
  const orig=r?(HASBOOK?(unitOf(no)?String(unitName(unitOf(no))||''):String(titleOf(r)||'')):String(titleOf(r)||'')):null;
  return {vtt:!!v,ied:!!(v&&v.classList.contains('ied')),fx:!!(v&&v.classList.contains('fx')),tx:v&&!v.classList.contains('ied')?v.textContent:null,
    val:inp?inp.value:null,inpH:inp?Math.round(inp.getBoundingClientRect().height):null,okR,okHit,okIn,focus:!!inp&&document.activeElement===inp,orig,
    tip:!!document.getElementById('g3Tip'),trunc:t?t.scrollWidth>t.clientWidth+1:null,vno:VNO||0,sheets:document.querySelectorAll('.sheet').length,
    anyIed:document.querySelectorAll('.ied').length,vcls:(document.getElementById('view')||{}).className||''}}"""
# 제목 줄 누를 자리 — 제목(.vtt 보이는 쪽) · 줄 가운데 · 줄 오른쪽 끝(말줄임 = 제목 글자 밖)
VTAT_JS = r"""()=>{const t=document.getElementById('vT1');if(!t)return null;const r=t.getBoundingClientRect(),v=t.querySelector('.vtt'),H=e=>e?(e.id?'#'+e.id:String(e.className||e.tagName)):null;
  const lx=r.left+5,el=document.elementFromPoint(lx,r.top+r.height/2);
  let tp=null;if(v){const q=v.getBoundingClientRect(),L=Math.max(q.left,r.left),R=Math.min(q.right,r.right);if(R-L>=6){const x=(L+R)/2,y=q.top+q.height/2,e=document.elementFromPoint(x,y);tp={cx:x,cy:y,on:!!e&&(e===v||v.contains(e)),hit:H(e)}}}
  const cx=r.left+r.width/2,cy=r.top+r.height/2,ec=document.elementFromPoint(cx,cy),rx=r.right-3,er=document.elementFromPoint(rx,cy);
  return {title:tp,row:{cx,cy,on:!!ec&&(ec===t||t.contains(ec)),hit:H(ec)},right:{cx:rx,cy,on:!!er&&(er===t||t.contains(er)),hit:H(er),inVtt:!!er&&!!v&&(er===v||v.contains(er))},
    left:{cx:lx,cy,on:!!el&&(el===t||t.contains(el)),hit:H(el),inVtt:!!el&&!!v&&(el===v||v.contains(el))}}}"""
INP_AT = r"""()=>{const i=document.querySelector('.ied .iedin');if(!i)return null;const q=i.getBoundingClientRect();return {cx:q.left+Math.min(20,q.width/2),cy:q.top+q.height/2,on:true}}"""
SEL_JS = r"""()=>{const i=document.querySelector('.ied .iedin');if(!i)return false;i.focus();try{i.select()}catch(e){}return document.activeElement===i}"""
CLK_JS = r"""()=>{window.__clk=0;if(!window.__clkL){window.__clkL=1;document.addEventListener('click',()=>{window.__clk++})}return 1}"""
WK_CLICK = r"""([x,y])=>{const t=document.elementFromPoint(x,y);if(!t)return null;t.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,composed:true,clientX:x,clientY:y,button:0}));return t.tagName}"""
TF_JS = r"""(k)=>{const o=TFIX[k];return (o&&typeof o==='object')?JSON.parse(JSON.stringify(o)):null}"""
KEY_JS = r"""(no)=>GGU(rec(no))"""
NDTT_AT = r"""(no)=>{const e=document.querySelector('#navdr .ndtt[data-pn="'+no+'"]');if(!e)return null;try{e.scrollIntoView({block:'center'})}catch(_){}
  return Object.assign(__H.at(e),{fx:e.classList.contains('fx'),tx:e.textContent,ied:e.classList.contains('ied')})}"""
NDTT_IED = r"""()=>{const i=document.querySelector('#navdr .ndtt.ied .iedin'),k=document.querySelector('#navdr .ndtt.ied .iedok');return i?{val:i.value,h:Math.round(i.getBoundingClientRect().height),okH:k?Math.round(k.getBoundingClientRect().height):null}:null}"""
NDROW_JS = r"""(no)=>{const w=document.querySelector('#ndList .ndrow[data-no="'+no+'"]');if(!w)return null;const t=w.querySelector('.ndt'),s=t&&t.querySelector('.ndtt'),r=rec(no);
  return {tx:t?t.textContent:null,span:!!s,fx:!!(s&&s.classList.contains('fx')),stx:s?s.textContent:null,code:String(r[F.CODE])+String(r[F.LV]||''),tt:String(titleOf(r)||''),yn:!!ynUid(r)}}"""
LIST_JS = r"""(no)=>{const r=rec(no),u=GGU(r),it=document.querySelector('#list .item[data-pv="'+u+'"]');if(!it)return null;const s=it.querySelector('.sub');return s?{tx:s.textContent,fx:s.classList.contains('pnfx')}:null}"""
PNM_JS = r"""(no)=>{document.querySelectorAll('#jnw').forEach(x=>x.remove());try{jnOpen(unitOf(no))}catch(e){return 'ERR '+e}const e=document.querySelector('#jnw .jnrow[data-no="'+no+'"] .pnm');if(!e)return null;
  try{e.scrollIntoView({block:'center'})}catch(_){}const r=rec(no);return Object.assign(__H.at(e),{tx:e.textContent,fx:e.classList.contains('fx'),ied:e.classList.contains('ied'),want:String(pnFix(r)||pnAuto(r))})}"""
PNM_IED = r"""(no)=>{const e=document.querySelector('#jnw .jnrow[data-no="'+no+'"] .pnm');if(!e)return null;const i=e.querySelector('.iedin');return {ied:e.classList.contains('ied'),val:i?i.value:null,h:i?Math.round(i.getBoundingClientRect().height):null,jnw:!!document.getElementById('jnw'),vno:VNO||0}}"""
FR_JS = r"""async ()=>{document.querySelectorAll('#pwl').forEach(x=>x.remove());try{pwList('f')}catch(e){return 'ERR '+e}await new Promise(r=>setTimeout(r,500));const g=document.querySelector('#pwl .pfg');if(g)g.click();
  await new Promise(r=>setTimeout(r,500));const e=document.querySelector('#pwl .frcell');if(!e)return null;try{e.scrollIntoView({block:'center'})}catch(_){}
  return Object.assign(__H.at(e),{k:e.dataset.fk,s:e.dataset.fs,want:String(frFix(e.dataset.fk,e.dataset.fs)||frOrig(e.dataset.fk,e.dataset.fs))})}"""
PNM_AT = r"""(no)=>{const e=document.querySelector('#jnw .jnrow[data-no="'+no+'"] .pnm');if(!e)return null;try{e.scrollIntoView({block:'center'})}catch(_){}return __H.at(e)}"""
FR_AT = r"""([k,s])=>{const e=[...document.querySelectorAll('#pwl .frcell')].find(x=>x.dataset.fk===k&&x.dataset.fs===s);if(!e)return null;try{e.scrollIntoView({block:'center'})}catch(_){}return __H.at(e)}"""
FR_IED = r"""([k,s])=>{const e=[...document.querySelectorAll('#pwl .frcell')].find(x=>x.dataset.fk===k&&x.dataset.fs===s);if(!e)return null;const i=e.querySelector('.iedin');return {ied:e.classList.contains('ied'),val:i?i.value:null,pwl:!!document.getElementById('pwl')}}"""
TIP_JS = r"""()=>{const t=document.getElementById('g3Tip');if(!t)return null;const r=t.getBoundingClientRect();return {h:Math.round(r.height),ih:innerHeight,same:t.textContent===document.getElementById('vT1').textContent}}"""
OVERFLOW_JS = r"""()=>({sw:document.documentElement.scrollWidth,iw:innerWidth,ok:document.documentElement.scrollWidth<=innerWidth+1})"""
ERRS_JS = r"""()=>(window.__err||[]).slice(0,12)"""
SYNC_JS = r"""async ()=>{try{stampAll();await syncRecords(true)}catch(e){return 'ERR '+e}await new Promise(r=>setTimeout(r,300));return (typeof recErr!=='undefined'&&recErr)?String(recErr):'ok'}"""
PAST_JS = r"""(v)=>{const o=FL.past;FL.past=v;try{draw()}catch(e){}try{navBuild()}catch(e){}return o}"""
# 카드 층 위 검색 — 문제 모드 · 낱말 → 줄 문항 번호
SMODE_JS = r"""()=>{const b=document.querySelector('.seg2 [data-sm="q"]');if(b&&typeof GGMODE!=='undefined'&&GGMODE==='g')b.click();const q=document.getElementById('q');if(!q)return null;try{q.scrollIntoView({block:'nearest'})}catch(e){}
  q.value='';q.dispatchEvent(new Event('input',{bubbles:true}));return Object.assign(__H.at(q),{mode:typeof GGMODE!=='undefined'?GGMODE:null})}"""
SRES_JS = r"""()=>{const b=document.getElementById('esres');if(!b||b.classList.contains('hide'))return {box:false,nos:[]};return {box:true,nos:[...b.querySelectorAll('.ggres[data-esq]')].map(x=>+x.dataset.esq)}}"""
TFQ_AT = r"""()=>{const e=document.querySelector('#view [data-tfx="q"]');if(!e)return null;try{e.scrollIntoView({block:'center'})}catch(_){}const a=__H.at(e);return Object.assign(a,{tx8:null})}"""
TFQ_TX = r"""()=>{const e=document.querySelector('#view [data-tfx="q"]');return e?e.innerText.replace(/\s+/g,' ').trim():null}"""
TFX_SHEET = r"""(t)=>{const s=document.getElementById('tfxSheet');if(!s)return null;const ta=s.querySelector('#tfxIn');ta.value=t;const ok=s.querySelector('#tfxOk');try{ok.scrollIntoView({block:'center'})}catch(e){}
  return __H.at(ok)}"""
TFQ_UNDO = r"""async (u)=>{await tfixSet(u,'q','');try{showProblem()}catch(e){}await new Promise(r=>setTimeout(r,400));return tfixRaw(u,'q')}"""
# 근거(트리거 칸) 지어낸 글을 두 문항에 — theorybar SEEDC_JS 꼴(g3Push 는 gg3 덩어리 안 함수라 못 부름)
SEEDT_JS = r"""async ([nos,t])=>{const out=[];for(const no of nos){const r=rec(no),u=GGU(r),list=ggOf(u).slice();list.forEach((x,n)=>{if(x&&x.i!==n+1)x.i=n+1});
  const g={k:ggNewKey('g_'),i:list.length+1,t:t,ok:ggMarkNow(no),ts:Date.now(),cs:[],f:'t'};list.push(g);await ggSaveList(u,list);try{ggRepaint(u)}catch(e){}out.push({u,k:g.k})}return out}"""
UNFOLD_JS = r"""()=>{const v=document.getElementById('view');if(v&&v.classList.contains('g3off')){const b=document.getElementById('g3Fold');if(b)b.click()}return !!v&&!v.classList.contains('g3off')}"""
FOLDB_AT = r"""()=>{const b=document.querySelector('#card .g3f[data-g3f="t"] .g3fb')||document.querySelector('#card .g3fb');if(!b)return null;try{b.scrollIntoView({block:'center'})}catch(_){}return __H.at(b)}"""
USE_AT = r"""(f)=>{const e=document.querySelector('#view i.g3use[data-g3use^="'+f+'"]');if(!e)return null;try{e.scrollIntoView({block:'center'})}catch(_){}return __H.at(e)}"""
GGUW_JS = r"""(ua)=>{const w=document.getElementById('gguw');if(!w)return {win:false};const e=w.querySelector('.g3ttl[data-gguugo="'+ua+'"]');if(!e)return {win:true,row:false,n:w.querySelectorAll('.gguR').length};
  try{e.scrollIntoView({block:'center'})}catch(_){}return {win:true,row:true,n:w.querySelectorAll('.gguR').length,hd:!!w.querySelector('.gguh'),at:__H.at(e)}}"""
VPIN_JS = r"""(no)=>{const p=[...document.querySelectorAll('.vpin')].find(x=>+x.dataset.no===+no);const t=document.getElementById('vT1');
  return {pin:!!p,vpt:p?(p.querySelector('.vpt')||{}).textContent||'':null,vno:VNO||0,vt1:t?t.textContent:null}}"""


def hold(p, x, y, ms, how):
    """누르고 ms 뒤 뗌 — mouse(PC) · cdp(Chromium 손가락) · wk(WebKit 합성 touch 포인터 = 공용 WK_LONG)"""
    if how == 'mouse':
        p.pg.mouse.move(x, y); p.pg.mouse.down(); p.wait(ms); p.pg.mouse.up()
    elif how == 'cdp':
        c = p._cdp()
        c.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'radiusX': 6, 'radiusY': 6, 'id': 1}]})
        p.wait(ms)
        c.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    else:
        p.pg.evaluate(JG.WK_LONG, [x, y, 'pointerdown']); p.wait(ms); p.pg.evaluate(JG.WK_LONG, [x, y, 'pointerup'])


def tpt(at):
    """제목 줄 누를 자리 — 제목(.vtt 보이는 쪽)에 닿으면 그 자리 · 아니면(폰 = 제목이 거의 다 잘림) 줄 가운데"""
    at = at or {}
    return at['title'] if (at.get('title') or {}).get('on') else at.get('row')


def how_of(p):
    return 'mouse' if not p.touch else ('wk' if p.eng == 'webkit' else 'cdp')


def press(p, at, wait=400):
    """한 번 누름 — PC 마우스 click · 폰 손가락 톡(공용 tap)"""
    if not at or not at.get('on'):
        return False
    (p.tap if p.touch else p.click)(at['cx'], at['cy'], wait)
    return True


def long_at(p, at, ms=LONG, leak=False):
    """길게 — 뗀 뒤 click 셈(leak) · WebKit 합성 길게는 진짜 click 이 안 나 합성 click 하나를 보내 앱이 먹는지 잼"""
    if not at or not at.get('on'):
        return None
    p.ev(CLK_JS)
    how = how_of(p)
    hold(p, at['cx'], at['cy'], ms, how)
    if leak and how == 'wk':
        p.ev(WK_CLICK, [at['cx'], at['cy']])
    p.wait(450)
    return p.ev("()=>window.__clk||0")


def type_ied(p, text, key='Enter'):
    """열린 고치기 칸 — 다 고르고(select) 지어낸 글 · 비우기 = Backspace · Enter/Escape"""
    if not p.ev(SEL_JS):
        return False
    if text:
        p.pg.keyboard.type(text, delay=8)
    else:
        p.pg.keyboard.press('Backspace')
    p.pg.keyboard.press(key)
    p.wait(500)
    return True


def errs(p):
    """페이지 오류(pageerror + window error · unhandledrejection) — ResizeObserver loop 알림은 따로 셈(브라우저 알림 · 앱 오류 아님)"""
    a = list(p.errs or []) + list(p.ev(ERRS_JS) or [])
    ro = [x for x in a if 'ResizeObserver loop' in x]
    return [x[:160] for x in a if 'ResizeObserver loop' not in x], len(ro)


def ov(p):
    return bool((p.ev(OVERFLOW_JS) or {}).get('ok'))


def vt_view(v, orig_key='orig'):
    """제목 상태를 출력용으로(제목 글 = 같음 · 길이만 · D11)"""
    if not v:
        return v
    o = {'vtt': v.get('vtt'), 'ied': v.get('ied'), 'fx': v.get('fx')}
    if v.get('val') is not None:
        o['칸 값 = 원래'] = v['val'] == v.get(orig_key)
    if v.get('tx') is not None:
        o['글 = 원래'] = v['tx'] == v.get('orig')
    return o


# ══ 흐름 ════════════════════════════════════════════════════════════════════════════════
def bd_open(p, nm):
    """그 단원 머리 [N] 누름 → (창 읽음 · 머리)"""
    hd = p.ev(HEAD_JS, nm)
    if not hd or not hd.get('bd'):
        return None, hd
    p.wait(150)
    at = p.ev(BDAT_JS, hd['sec'])
    press(p, at, 450)
    return p.ev(BDPOP_JS, hd['sec']), hd


def flow_b(p, o, T9, phone):
    """B2 · B3(물리 첫 화면) — PC 마우스 · 폰 손가락 같은 길"""
    big = p.ev(BIG_JS)
    hd = p.ev(HEAD_JS, '등속 원운동')
    if not hd or not hd.get('bd'):
        o['B2'] = {'[N] 없음': True, '머리': bool(hd)}
        o['B3'] = {'[N] 없음': True}
        return
    sec = hd['sec']
    p.wait(200)
    f0 = p.ev(FS_JS, sec)
    at = p.ev(BDAT_JS, sec)
    press(p, at, 900)   # 900 = 머리 줄 누름이면 첫 화면이 부드럽게 굴러갈 틈
    pop5 = p.ev(BDPOP_JS, sec)
    f1 = p.ev(FS_JS, sec)
    T9['넘침'].append(('[5] 창', ov(p)))
    if pop5.get('pop'):
        T9['창'].append(('[5]', pop5['rect']['h'], pop5['ih']))
    press(p, p.ev(BDAT_JS, sec), 450)
    same = p.ev(POPS_JS)
    press(p, p.ev(BDAT_JS, sec), 450)
    re1 = p.ev(POPS_JS)
    nt = p.ev(NEUTRAL_JS, None)
    press(p, nt, 450)
    out = p.ev(POPS_JS)
    b3 = {'같은 [N] 다시': same, '다시 열림': re1, '바깥 누름': out, '바깥 자리': (nt or {}).get('top'),
          '새는 일': {'앞': f0, '뒤': f1}}
    if phone:   # 폰 — 바깥 누름 뒤 서랍이 접혔으면 다음 서랍 누름 앞에 다시 폄(톡 막이 0.4 초 넘김 · 첫 잼 = 바깥 자리가 과목 탭 옆이라 과목이 지학으로 바뀌며 접힘 → 둘레 막이 뒤 접힘 0)
        b3['바깥 누름 뒤 서랍 접힘'] = p.ev("()=>document.getElementById('navdr').classList.contains('fold')")
        b3['과목 그대로'] = p.ev("()=>!HASBOOK&&DATA.length===577")
        p.ev("()=>{try{ndResFold(false)}catch(e){}return 1}"); p.wait(700)
    popb = None
    if big:
        popb, hb = bd_open(p, big['nm'])
        if popb and popb.get('pop'):
            T9['창'].append(('[%d] 단원 %d' % (big['n'], big['k']), popb['rect']['h'], popb['ih']))
            T9['넘침'].append(('[%d] 창' % big['n'], ov(p)))
            press(p, p.ev(BDAT_JS, hb['sec']), 400)
    o['B2'] = {'[5]': pop5, '가장 큰 묶음': popb, 'big': big}
    if not phone:
        # g3Pop ↔ bdPop — 누름(마우스) · 함수(앱 서로 닫기 줄)
        def g3x():
            q2 = ((o.get('문항') or []) + [None, None, None])[2]
            sd = p.ev(SEED_JS, [[q2, 'O']]) if q2 else None
            r = {'O X 줄': sd}
            if not (sd and sd[0]):
                return r
            hd2 = p.ev(HEAD_JS, '등속 원운동')
            press(p, p.ev(BDAT_JS, hd2['sec']), 400)
            a = p.ev(POPS_JS)
            press(p, p.ev(OX_AT, q2), 500)
            b = p.ev(POPS_JS)
            p.ev(HEAD_JS, '등속 원운동'); p.wait(150)
            press(p, p.ev(BDAT_JS, hd2['sec']), 450)
            c = p.ev(POPS_JS)
            p.ev(CLEAN_JS)
            r.update({'누름': {'[N]': a, 'O X 누름': b, '다시 [N]': c}, '함수': p.ev(G3X_JS, [q2, hd2['n'], hd2['sec']])})
            return r
        safe(b3, 'g3Pop', g3x)
    # 대조 — 같은 머리의 이름 누름은 첫 화면을 굴림(잣대가 새는 일을 잡는지)
    p.ev(CLEAN_JS)
    hd3 = p.ev(HEAD_JS, '등속 원운동')
    p.wait(200)
    c0 = p.ev(FS_JS, sec)
    press(p, (hd3 or {}).get('nm'), 1100)
    c1 = p.ev(FS_JS, sec)
    b3['대조 이름 누름'] = {'앞': c0.get('scr'), '뒤': c1.get('scr'), '본창': c1.get('view')}
    o['B3'] = b3


def flow_phys_pc(br, eng, ver):
    """물리 PC 1100×800 마우스 — B1 · B2 · B3 · T1 · T2 · T3 · T8 · T9"""
    o, T9 = {}, {'넘침': [], '창': [], '칸': [], '✓': []}
    p = _pg(br, eng, 'bdPC', ver, 'phys', PC, False)
    try:
        qs = p.ev(PICKP_JS, 3) or []   # 먼저 고름(뒤 단계가 목록 · 기록을 바꾸기 전)
        no = qs[0] if qs else None
        o['문항'] = qs
        o['B1'] = p.ev(B1_JS)
        safe(o, '_b', lambda: flow_b(p, o, T9, False))
        p.ev(CLEAN_JS)
        if QC.SMOKE:
            return o, T9, p
        key = p.ev(KEY_JS, no)
        # T1 — 길게 600 · 짧게 150(마우스)
        def t1():
            p.ev(OPEN_JS, no)
            at = p.ev(VTAT_JS) or {}
            r = {'누를 자리': {k: (v or {}).get('hit') for k, v in at.items()}}
            clk = long_at(p, tpt(at), LONG, leak=True)
            v = p.ev(VT_JS, no)
            r['길게'] = vt_view(v); r['길게 뒤 click'] = clk
            if v.get('ied'):
                T9['칸'].append(('PC 제목 칸', v.get('inpH')))
                T9['넘침'].append(('PC 제목 칸', ov(p)))
                p.pg.keyboard.press('Escape'); p.wait(300)
            r['Esc 뒤'] = vt_view(p.ev(VT_JS, no))
            pt = tpt(at)
            hold(p, pt['cx'], pt['cy'], SHORT, 'mouse') if pt else None
            p.wait(350)
            r['짧게'] = vt_view(p.ev(VT_JS, no))
            p.ev("()=>{const t=document.getElementById('g3Tip');if(t)t.remove();return 1}")
            return r
        safe(o, 'T1', t1)
        # T2 — 저장 · 다시 열기 · 새로고침 · Esc · 바깥 · 비움
        def t2():
            r = {}
            at = tpt(p.ev(VTAT_JS))
            long_at(p, at)
            ok = type_ied(p, NEWT)
            if not ok:   # 칸이 안 열림(바탕) — 뒤 단계는 뜻 없음
                return {'저장': {'칸 열림': False}}
            v = p.ev(VT_JS, no); tf = p.ev(TF_JS, key); nd = p.ev(NDTT_AT, no); li = p.ev(LIST_JS, no); pn = p.ev(PNM_JS, no)
            p.ev("()=>{document.querySelectorAll('#jnw').forEach(x=>x.remove());return 1}")
            r['저장'] = {'칸 열림': ok, 'TFIX nm = 글': (tf or {}).get('nm') == NEWT, '머리 .vtt.fx = 글': bool(v.get('fx')) and v.get('tx') == NEWT,
                        '서랍 .ndtt.fx = 글': bool(nd and nd.get('fx') and nd.get('tx') == NEWT), '목록 .sub.pnfx': bool(li and li.get('fx') and str(li.get('tx', '')).startswith(NEWT)),
                        '정리 창 .pnm.fx = 글': bool(isinstance(pn, dict) and pn.get('fx') and pn.get('tx') == NEWT)}
            p.ev(CLOSEV_JS); p.ev(OPEN_JS, no)
            v = p.ev(VT_JS, no)
            r['다시 열기'] = bool(v.get('fx')) and v.get('tx') == NEWT
            p.reload(); p.ev(OPEN_JS, no)
            v = p.ev(VT_JS, no); tf = p.ev(TF_JS, key)
            r['새로고침'] = bool(v.get('fx')) and v.get('tx') == NEWT and (tf or {}).get('nm') == NEWT
            at = tpt(p.ev(VTAT_JS))
            long_at(p, at); e1 = type_ied(p, TMPT, 'Escape')
            v = p.ev(VT_JS, no); tf = p.ev(TF_JS, key)
            r['Esc'] = {'칸': e1, '그대로': v.get('tx') == NEWT and bool(v.get('fx')) and (tf or {}).get('nm') == NEWT and not v.get('ied')}
            at = tpt(p.ev(VTAT_JS))
            long_at(p, at)
            opened = p.ev(SEL_JS)
            if opened:
                p.pg.keyboard.type(TMPT, delay=8)
            nt = p.ev(NEUTRAL_JS, '#view')
            press(p, nt, 500)
            v = p.ev(VT_JS, no); tf = p.ev(TF_JS, key)
            r['바깥'] = {'칸': bool(opened), '자리': (nt or {}).get('top'), '그대로': v.get('tx') == NEWT and bool(v.get('fx')) and (tf or {}).get('nm') == NEWT and not v.get('ied')}
            at = tpt(p.ev(VTAT_JS))
            long_at(p, at); e2 = type_ied(p, '')
            v = p.ev(VT_JS, no); tf = p.ev(TF_JS, key); nd = p.ev(NDTT_AT, no); li = p.ev(LIST_JS, no)
            r['비움'] = {'칸': e2, 'TFIX nm 없음': not (tf or {}).get('nm'), '머리 = 원래 · fx 없음': v.get('tx') == v.get('orig') and not v.get('fx'),
                        '서랍 = 원래 · fx 없음': bool(nd) and nd.get('tx') == v.get('orig') and not nd.get('fx'), '목록 pnfx 없음': bool(li) and not li.get('fx')}
            return r
        safe(o, 'T2', t2)
        # T3 — 서랍 줄 제목 길게 → 머리
        def t3():
            p.ev(CLEAN_JS)
            at = p.ev(NDTT_AT, no)
            r = {'서랍 줄': bool(at and at.get('on'))}
            long_at(p, at)
            ie = p.ev(NDTT_IED)
            r['칸'] = bool(ie)
            if ie:
                r['칸 값 = 원래'] = ie['val'] == (p.ev(VT_JS, no) or {}).get('orig')
                T9['칸'].append(('PC 서랍 칸', ie['h']))
                type_ied(p, NEWT3)
            v = p.ev(VT_JS, no); nd = p.ev(NDTT_AT, no)
            r['머리 = 같은 글 · fx'] = v.get('tx') == NEWT3 and bool(v.get('fx'))
            r['서랍 = 글'] = bool(nd) and nd.get('tx') == NEWT3
            p.ev("async (no)=>{const r=rec(no);await tfixSet(pnUid(r),PN_SLOT,'');try{ndTitlePaint(no)}catch(e){}try{pnPaint(no)}catch(e){}return 1}", no)
            return r
        safe(o, 'T3', t3)
        safe(o, 'T8', lambda: t8(p, (qs + [no])[1]))
        p.ev(CLOSEV_JS)
        T9['넘침'].append(('PC 끝', ov(p)))
    except Exception:
        o['하네스 오류'] = traceback.format_exc()[-700:]
    return o, T9, p


def t8(p, no):
    """정리 창 이름(.pnm) · 공식 칸(.frcell) — 길게 = 고치기 칸(값 = 바탕과 같은 원래) · Esc · 짧게 = 안 열림"""
    r = {}
    p.ev(CLEAN_JS)
    a = p.ev(PNM_JS, no)
    if isinstance(a, dict) and a.get('on'):
        p.wait(700)   # 정리 창 줄 그림(pvWatch)이 보일 때 그려져 줄 자리가 밀림 — 자리 잡힌 뒤 다시 재고 누름
        a2 = p.ev(PNM_AT, no) or a
        long_at(p, a2)
        e = p.ev(PNM_IED, no)
        r['.pnm 길게'] = {'칸': bool(e and e['ied']), '값 = 원래': bool(e) and e['val'] == a['want']}
        if e and e['ied']:
            p.pg.keyboard.press('Escape'); p.wait(300)
        a2 = p.ev(PNM_AT, no)
        hold(p, a2['cx'], a2['cy'], SHORT, how_of(p)) if a2 else None
        p.wait(400)
        e2 = p.ev(PNM_IED, no)
        r['.pnm 짧게'] = {'칸 없음': bool(e2) and not e2['ied'], '정리 창 그대로': bool(e2) and e2['jnw']}
    else:
        r['.pnm'] = {'못 찾음': str(a)[:80]}
    p.ev(CLEAN_JS)
    f = p.ev(FR_JS)
    if isinstance(f, dict) and f.get('on'):
        p.wait(500)
        long_at(p, p.ev(FR_AT, [f['k'], f['s']]) or f)
        e = p.ev(FR_IED, [f['k'], f['s']])
        r['.frcell 길게'] = {'칸': bool(e and e['ied']), '값 = 원래': bool(e) and e['val'] == f['want']}
        if e and e['ied']:
            p.pg.keyboard.press('Escape'); p.wait(300)
        f2 = p.ev(FR_AT, [f['k'], f['s']])
        hold(p, f2['cx'], f2['cy'], SHORT, how_of(p)) if f2 else None
        p.wait(400)
        e2 = p.ev(FR_IED, [f['k'], f['s']])
        r['.frcell 짧게'] = {'칸 없음': bool(e2) and not e2['ied'], '창 그대로': bool(e2) and e2['pwl']}
    else:
        r['.frcell'] = {'못 찾음': str(f)[:80]}
    p.ev(CLEAN_JS)
    return r


def flow_phys_ph(br, eng, ver):
    """물리 폰 384×740 손가락 — B2 · B3 · T1 · T4 · T8 · T9"""
    o, T9 = {}, {'넘침': [], '창': [], '칸': [], '✓': []}
    p = _pg(br, eng, 'bdPH', ver, 'phys', PH, True)
    try:
        qs = p.ev(PICKP_JS, 3) or []   # 먼저 고름
        no = qs[0] if qs else None
        o['문항'] = qs
        p.ev("()=>{try{ndResFold(false)}catch(e){}return 1}"); p.wait(700)   # 좁은 화면 = 접힌 채 시작 → 폄(톡 막이 0.4 초 넘김)
        safe(o, '_b', lambda: flow_b(p, o, T9, True))
        p.ev(CLEAN_JS)
        p.ev("()=>{try{ndResFold(true)}catch(e){}return 1}"); p.wait(600)
        def t1():
            p.ev(OPEN_JS, no)
            at = p.ev(VTAT_JS) or {}
            r = {'누를 자리': {k: (v or {}).get('hit') for k, v in at.items()}, '왼쪽(번호 · 코드) = 제목 글자 밖': (at.get('left') or {}).get('on') and not (at.get('left') or {}).get('inVtt')}
            pt = tpt(at)
            long_at(p, pt)
            v = p.ev(VT_JS, no)
            r['길게(제목 줄)'] = vt_view(v)
            if v.get('ied'):
                T9['칸'].append(('폰 제목 칸', v.get('inpH')))
                T9['✓'].append(('폰 제목 칸 ✓', bool(v.get('okIn')) and bool(v.get('okHit')), v.get('okR')))
                T9['넘침'].append(('폰 제목 칸', ov(p)))
                p.pg.keyboard.press('Escape'); p.wait(300)
            for nm_, k_ in (('길게(오른쪽 끝)', 'right'), ('길게(왼쪽 번호 · 코드)', 'left')):
                long_at(p, at.get(k_))
                v = p.ev(VT_JS, no)
                r[nm_] = vt_view(v)
                if v.get('ied'):
                    p.pg.keyboard.press('Escape'); p.wait(300)
            hold(p, pt['cx'], pt['cy'], SHORT, how_of(p)) if pt else None
            p.wait(350)
            r['짧게'] = vt_view(p.ev(VT_JS, no))
            p.ev("()=>{const t=document.getElementById('g3Tip');if(t)t.remove();return 1}")
            return r
        safe(o, 'T1', t1)
        def t4():
            p.ev("()=>{const t=document.getElementById('g3Tip');if(t)t.remove();return 1}")
            at = p.ev(VTAT_JS) or {}
            pt = at.get('row')
            v0 = p.ev(VT_JS, no)
            r = {'잘림': v0.get('trunc')}
            p.tap(pt['cx'], pt['cy'], 500)
            tip = p.ev(TIP_JS)
            r['짧게 → 말풍선'] = bool(tip)
            if tip:
                T9['창'].append(('말풍선 #g3Tip', tip['h'], tip['ih']))
            s0 = p.ev(VT_JS, no)
            clk = long_at(p, pt, LONG, leak=True)
            p.wait(300)
            v = p.ev(VT_JS, no)
            r['이어 길게'] = {'칸': v.get('ied'), '말풍선 없음': not v.get('tip'), 'click 셈': clk, '문항 그대로': v.get('vno') == s0.get('vno') == no, '창 수 그대로': v.get('sheets') == s0.get('sheets')}
            ia = p.ev(INP_AT)
            if ia:
                p.tap(ia['cx'], ia['cy'], 450)
            v2 = p.ev(VT_JS, no)
            r['칸 안 누름'] = {'칸 그대로': bool(v2.get('ied')), '말풍선 없음': not v2.get('tip')}
            if v2.get('ied'):
                p.pg.keyboard.press('Escape'); p.wait(300)
            return r
        safe(o, 'T4', t4)
        p.ev(CLOSEV_JS)
        safe(o, 'T8', lambda: t8(p, (qs + [no, no])[1]))
        T9['넘침'].append(('폰 끝', ov(p)))
    except Exception:
        o['하네스 오류'] = traceback.format_exc()[-700:]
    return o, T9, p


def card_t5(p, no, T9, past=None):
    """카드 층 문항 하나 — 머리 원래 = 소단원 · 길게 = 칸 · 저장 · 서랍 꼬리 · 서랍 파랑 길게 · 비움 = 옛 꼴"""
    r = {}
    p0 = p.ev(PAST_JS, past) if past is not None else None
    key = p.ev(KEY_JS, no)
    p.ev(OPEN_JS, no)
    row0 = p.ev(NDROW_JS, no)
    v0 = p.ev(VT_JS, no)
    r['서랍 줄'] = bool(row0)
    r['머리 원래 = 소단원'] = v0.get('vtt') and v0.get('tx') == v0.get('orig')
    at = tpt(p.ev(VTAT_JS))
    long_at(p, at)
    v = p.ev(VT_JS, no)
    r['길게 칸 값 = 소단원'] = bool(v.get('ied')) and v.get('val') == v.get('orig')
    if v.get('ied'):
        T9['칸'].append(('카드 제목 칸', v.get('inpH')))
    ok = type_ied(p, NEWTE) if v.get('ied') else False
    if not ok:   # 칸이 안 열림(바탕) — 뒤 단계는 뜻 없음
        if past is not None:
            p.ev(PAST_JS, p0)
        r['저장'] = {'칸': False}
        return r
    v = p.ev(VT_JS, no); tf = p.ev(TF_JS, key); row = p.ev(NDROW_JS, no)
    r['저장'] = {'칸': ok, 'TFIX nm = 글': (tf or {}).get('nm') == NEWTE, '머리 .vtt.fx = 글': bool(v.get('fx')) and v.get('tx') == NEWTE,
                '서랍 꼬리 .ndtt.fx = 글': bool(row and row.get('fx') and row.get('stx') == NEWTE), '서랍 줄 = 코드 · 글': bool(row) and row.get('tx') == row.get('code') + ' · ' + NEWTE}
    T9['넘침'].append(('카드 저장 뒤', ov(p)))
    nd = p.ev(NDTT_AT, no)
    long_at(p, nd)
    ie = p.ev(NDTT_IED)
    r['서랍 파랑 길게 = 칸'] = bool(ie) and ie['val'] == NEWTE
    if ie:
        p.pg.keyboard.press('Escape'); p.wait(300)
    at = tpt(p.ev(VTAT_JS))
    long_at(p, at)
    e2 = type_ied(p, '')
    v = p.ev(VT_JS, no); tf = p.ev(TF_JS, key); row = p.ev(NDROW_JS, no)
    r['비움'] = {'칸': e2, 'TFIX nm 없음': not (tf or {}).get('nm'), '머리 = 소단원 · fx 없음': v.get('tx') == v.get('orig') and not v.get('fx'),
                '서랍 줄 = 옛 꼴': bool(row and row0) and row.get('tx') == row0.get('tx') and row.get('span') == row0.get('span') == False}
    r['옛 꼴'] = 'uid 만' if (row0 or {}).get('yn') else '코드 · titleOf'
    if past is not None:
        p.ev(PAST_JS, p0)
    return r


def flow_card_pc(br, eng, ver):
    """지학 · 생물 PC 마우스 — B4 · T5 · T6 · T9"""
    out, T9 = {}, {'넘침': [], '창': [], '칸': [], '✓': []}
    pages = []
    for subj in ('earth', 'bio'):
        o = {}
        p = _pg(br, eng, 'bdC' + subj, ver, subj, PC, False)
        pages.append(p)
        try:
            o['B4'] = p.ev("()=>({secs:document.querySelectorAll('#ndList .ndsec').length,bd:document.querySelectorAll('#ndList .ndbd').length,rows:document.querySelectorAll('#ndList .ndrow').length})")
            pk = p.ev(PICKC_JS)
            o['문항'] = pk
            t5 = {}
            if subj == 'earth':
                if pk['g']:
                    safe(t5, '기출', lambda: card_t5(p, pk['g'][0], T9))
                if pk['c']:
                    safe(t5, '확인문제', lambda: card_t5(p, pk['c'][0], T9, past='p'))
            else:
                safe(t5, '문항', lambda: card_t5(p, (pk['o'] or pk['g'])[0], T9))
            o['T5'] = t5
            A = (pk['g'] if subj == 'earth' else (pk['o'] or pk['g']))[0]
            Bq = (pk['g'] if subj == 'earth' else (pk['o'] or pk['g']))[1]
            def t6():
                r = {}
                p.ev(CLEAN_JS)
                p.ev(OPEN_JS, A)
                ua = p.ev(KEY_JS, A)
                at = tpt(p.ev(VTAT_JS))
                long_at(p, at)
                r['제목 고침'] = type_ied(p, NEWTW)
                p.ev(CLOSEV_JS)
                q = p.ev(SMODE_JS)
                if q and q.get('on'):
                    p.click(q['cx'], q['cy'], 200)
                    p.pg.keyboard.type(WORD, delay=8); p.wait(700)
                sr = p.ev(SRES_JS)
                r['위 검색'] = {'칸': bool(q and q.get('on')), '모드': (q or {}).get('mode'), '그 문항': A in sr['nos'], '줄 수': len(sr['nos'])}
                p.ev("()=>{const q=document.getElementById('q');if(q){q.value='';q.dispatchEvent(new Event('input',{bubbles:true}))}return 1}")
                r['tfixAny 거짓'] = p.ev("(u)=>tfixAny(u)", ua) is False
                if subj != 'earth':
                    return r
                p.ev(OPEN_JS, A)
                fa = p.ev(TFQ_AT)
                sh = None
                if fa and fa.get('on'):
                    hold(p, fa['cx'], fa['cy'], 800, 'mouse'); p.wait(400)
                    sh = p.ev(TFX_SHEET, TXTQ)
                    if sh and sh.get('on'):
                        p.click(sh['cx'], sh['cy'], 800)
                tq = p.ev(TFQ_TX)
                r['글자 고치기'] = {'문제 칸': bool(fa and fa.get('on')), 'tfixSheet': bool(sh), '저장 단추 누름': bool(sh and sh.get('on')), 'TFIX q = 글': p.ev("(u)=>tfixRaw(u,'q')", ua) == TXTQ,
                                 '카드에 보임': bool(tq) and TXTQ in tq, '표시 md5': h8(tq)}
                p.ev(TFQ_UNDO, ua)
                # 「이 글을 쓴 문항」 창 → 제목 누름 → 비교 창 제목
                sd = p.ev(SEEDT_JS, [[A, Bq], TRIG])
                p.ev(CLEAN_JS); p.ev(OPEN_JS, Bq); p.ev(UNFOLD_JS); p.wait(300)
                ub = p.ev(KEY_JS, Bq)
                fb = p.ev(FOLDB_AT)   # 카드 층 적은 근거 목록 = 기본 접힘(#card.g3fold) → 「근거」 왼쪽 ▸ 를 눌러 폄(쓰인 수 칩은 그 목록 줄 안)
                if fb and fb.get('on'):
                    p.click(fb['cx'], fb['cy'], 500)
                ua_ = p.ev(USE_AT, 't|' + ub + '|')
                if ua_ and ua_.get('on'):
                    p.click(ua_['cx'], ua_['cy'], 900)
                else:
                    p.ev("([u,k])=>{try{g3UseWin('t',u,k)}catch(e){}return 1}", [ub, (sd or [{}, {}])[1].get('k')]); p.wait(900)
                gw = p.ev(GGUW_JS, ua)
                vp = None
                if gw.get('row') and gw['at'].get('on'):
                    p.click(gw['at']['cx'], gw['at']['cy'], 600)
                    for _ in range(20):
                        vp = p.ev(VPIN_JS, A)
                        if vp.get('pin'):
                            break
                        p.wait(250)
                if vp and vp.get('pin'):
                    T9['넘침'].append(('비교 창', ov(p)))
                r['쓴 문항 창'] = {'근거 둘': bool(sd and all(x.get('k') for x in sd)), '▸ 폄': bool(fb and fb.get('on')), '쓰인 수 누름': bool(ua_ and ua_.get('on')), '창': gw.get('win'), '그 문항 줄': gw.get('row'),
                               '비교 창': (vp or {}).get('pin'), '비교 창 제목 = 고친 제목': bool(vp and vp.get('vpt') and NEWTW in vp['vpt'])}
                p.ev(CLEAN_JS)
                return r
            safe(o, 'T6', t6)
            p.ev(CLOSEV_JS)
            T9['넘침'].append((subj + ' 끝', ov(p)))
        except Exception:
            o['하네스 오류'] = traceback.format_exc()[-700:]
        out[subj] = o
    return out, T9, pages


def flow_card_ph(br, eng, ver):
    """지학 폰 손가락 — 머리 제목 길게(CDP 손가락 · WebKit 합성 touch) = 칸 · 저장 · 비움"""
    T9 = {'넘침': [], '창': [], '칸': [], '✓': []}
    p = _pg(br, eng, 'bdCph', ver, 'earth', PH, True)
    r = {}
    try:
        pk = p.ev(PICKC_JS)
        no = pk['g'][0]
        key = p.ev(KEY_JS, no)
        p.ev(OPEN_JS, no)
        at = p.ev(VTAT_JS) or {}
        long_at(p, tpt(at))
        v = p.ev(VT_JS, no)
        r['길게 칸 값 = 소단원'] = bool(v.get('ied')) and v.get('val') == v.get('orig')
        if v.get('ied'):
            T9['칸'].append(('지학 폰 제목 칸', v.get('inpH')))
            T9['✓'].append(('지학 폰 제목 칸 ✓', bool(v.get('okIn')) and bool(v.get('okHit')), v.get('okR')))
        ok = type_ied(p, NEWTE) if v.get('ied') else False
        v = p.ev(VT_JS, no); tf = p.ev(TF_JS, key)
        r['저장'] = ok and (tf or {}).get('nm') == NEWTE and bool(v.get('fx')) and v.get('tx') == NEWTE
        at = p.ev(VTAT_JS) or {}
        long_at(p, tpt(at))
        type_ied(p, '')
        v = p.ev(VT_JS, no); tf = p.ev(TF_JS, key)
        r['비움'] = not (tf or {}).get('nm') and v.get('tx') == v.get('orig') and not v.get('fx')
        T9['넘침'].append(('지학 폰', ov(p)))
    except Exception:
        r['하네스 오류'] = traceback.format_exc()[-600:]
    return r, T9, p


def flow_sync(br, eng, ver):
    """T7 — 기기 둘(공용 원격 흉내 하나) · A 고침 → A 맞춤 → B 맞춤 = 같은 제목 · 비움도 → 물리 · 지학"""
    out, pages = {}, []
    for subj in ('phys', 'earth'):
        r = {}
        rm = JG.Remote()
        A = _pg(br, eng, 'bdS' + subj, ver, subj, PC, False, who='기기A', remote=rm)
        B = _pg(br, eng, 'bdS' + subj, ver, subj, PC, False, who='기기B', remote=rm)
        pages += [A, B]
        try:
            no = (A.ev(PICKP_JS, 1) or [None])[0] if subj == 'phys' else A.ev(PICKC_JS)['g'][0]
            key = A.ev(KEY_JS, no)
            A.ev(OPEN_JS, no)
            at = A.ev(VTAT_JS) or {}
            long_at(A, tpt(at))
            r['A 고침'] = type_ied(A, NEWT7) and (A.ev(TF_JS, key) or {}).get('nm') == NEWT7
            r['A 맞춤'] = A.ev(SYNC_JS); r['B 맞춤'] = B.ev(SYNC_JS)
            B.ev(OPEN_JS, no)
            vb = B.ev(VT_JS, no)
            r['B 받음'] = (B.ev(TF_JS, key) or {}).get('nm') == NEWT7 and vb.get('tx') == NEWT7 and bool(vb.get('fx'))
            at = A.ev(VTAT_JS) or {}
            long_at(A, tpt(at))
            r['A 비움'] = type_ied(A, '') and not (A.ev(TF_JS, key) or {}).get('nm')
            A.ev(SYNC_JS); B.ev(SYNC_JS)
            B.ev(CLOSEV_JS); B.ev(OPEN_JS, no)
            vb = B.ev(VT_JS, no)
            r['B 비움 받음'] = not (B.ev(TF_JS, key) or {}).get('nm') and vb.get('tx') == vb.get('orig') and not vb.get('fx')
            r['PUT'] = len(rm.puts)
        except Exception:
            r['하네스 오류'] = traceback.format_exc()[-600:]
        out[subj] = r
    return out, pages


# ══ 판정 ════════════════════════════════════════════════════════════════════════════════
def _all(d):
    """{이름: bool | {…}} 안 bool 다 참"""
    if isinstance(d, bool):
        return d
    if isinstance(d, dict):
        return all(_all(v) for v in d.values())
    return bool(d)


def jpop(x):
    x = x or {}
    return bool(x.get('pop') and x.get('on') and x.get('headOk') and x.get('whyOk') and x.get('rowsOk') and x.get('curOk') and x.get('noWord') and x.get('inScreen'))


def jb3(b, phone):
    b = b or {}
    same, re1, out = b.get('같은 [N] 다시') or {}, b.get('다시 열림') or {}, b.get('바깥 누름') or {}
    f0, f1 = (b.get('새는 일') or {}).get('앞') or {}, (b.get('새는 일') or {}).get('뒤') or {}
    leak0 = bool(f0) and all(f0.get(k) == f1.get(k) for k in ('scr', 'sy', 'fold', 'off', 'offSet', 'view', 'vno', 'ndoff'))   # 굴림 자리(scrollY + #list 위 굴림 칸) — 목록 위 글 줄 높이 바뀜(부팅 뒤 칩 등)은 굴림 아님
    c = b.get('대조 이름 누름') or {}
    ctl = c.get('앞') is not None and c.get('뒤') is not None and c['앞'] != c['뒤']
    ok = (not same.get('bd')) and same.get('bdOn') == 0 and re1.get('bd') and (not out.get('bd')) and leak0 and ctl
    if phone:
        ok = ok and b.get('과목 그대로') is True
    if not phone:
        g = b.get('g3Pop') or {}
        k, f = g.get('누름') or {}, g.get('함수') or {}
        ok = ok and (k.get('[N]') or {}).get('bd') and (k.get('O X 누름') or {}).get('g3') and not (k.get('O X 누름') or {}).get('bd') \
            and (k.get('다시 [N]') or {}).get('bd') and not (k.get('다시 [N]') or {}).get('g3') \
            and (f.get('a') or {}).get('bd') and (f.get('b') or {}).get('g3') and not (f.get('b') or {}).get('bd') and (f.get('c') or {}).get('bd') and not (f.get('c') or {}).get('g3')
    return bool(ok), {'같은 [N] 다시 = 닫힘': (not same.get('bd')) and same.get('bdOn') == 0, '바깥 = 닫힘': bool(re1.get('bd')) and not out.get('bd'), '바깥 자리': b.get('바깥 자리'),
                      '서랍 접기 · 첫 화면 스크롤 · 문항 열기 0': leak0, '대조 이름 누름 = 스크롤': ctl, '과목 그대로': b.get('과목 그대로') if phone else None, '폰 바깥 누름 뒤 서랍 접힘': b.get('바깥 누름 뒤 서랍 접힘') if phone else None, 'g3Pop ↔ bdPop': (None if phone else {k: v for k, v in (b.get('g3Pop') or {}).items() if k != 'O X 줄'})}


def j9(T9s, errl):
    """T9 — 오류 0 · 넘침 0 · 폰 ✓ · 칸 ≤ 26 · 새 창 ≤ ih/3 (잰 것만 — 바탕에 없는 칸 · 창은 안 잼)"""
    ovs = [x for t in T9s for x in t['넘침']]
    hs = [x for t in T9s for x in t['칸'] if x[1] is not None]
    ws = [x for t in T9s for x in t['창']]
    ck = [x for t in T9s for x in t['✓']]
    ok = not any(e for _, e in errl) and all(v for _, v in ovs) and all(h <= 26 for _, h in hs) and all(h <= ih / 3 + 0.5 for _, h, ih in ws) and all(v for _, v, _r in ck)
    d = {'오류': {k: e[:2] for k, e in errl if e}, '넘침 0': '%d/%d' % (sum(1 for _, v in ovs if v), len(ovs)), '넘침 흠': [k for k, v in ovs if not v],
         '칸 높이': {k: h for k, h in hs}, '창 높이(ih)': {k: '%d(%d)' % (h, ih) for k, h, ih in ws}, '폰 ✓': {k: [v, r] for k, v, r in ck}}
    return ok, d


def judge(x, base=None):
    """→ {칸: (ok, 값)} · base = 바탕 흐름 값(T6 표시 · T8 은 바탕과 맞댐)"""
    J = {}
    pc, ph, cd, cph, sy = (x.get(k) or {} for k in ('pc', 'ph', 'cd', 'cph', 'sy'))
    b1 = pc.get('B1') or {}
    J['B1'] = (b1.get('heads') == 63 and b1.get('withBd') == 63 and b1.get('bd111') == '[5]' and b1.get('B') == 24 and b1.get('ns') and b1.get('units') == 63 and b1.get('q') == 577 == b1.get('data')
               and b1.get('miss') == 0 and b1.get('dup') == 0 and b1.get('nameMiss') == 0 and b1.get('wrong') == 0, b1)
    pops = {'PC [5]': (pc.get('B2') or {}).get('[5]'), 'PC 가장 큰': (pc.get('B2') or {}).get('가장 큰 묶음'), '폰 [5]': (ph.get('B2') or {}).get('[5]'), '폰 가장 큰': (ph.get('B2') or {}).get('가장 큰 묶음')}
    if QC.SMOKE:   # smoke = PC 크롬만
        pops = {k: v for k, v in pops.items() if k.startswith('PC')}
    J['B2'] = (all(jpop(v) for v in pops.values()), {k: ({kk: (v or {}).get(kk) for kk in ('pop', 'n', 'head', 'rg', 'headOk', 'whyOk', 'rowsOk', 'curOk', 'noWord', 'inScreen', 'rect')} if v else v) for k, v in pops.items()})
    o3p, d3p = jb3(pc.get('B3'), False)
    o3h, d3h = jb3(ph.get('B3'), True)
    J['B3'] = (o3p and o3h, {'PC 마우스': d3p, '폰 손가락': d3h})
    b4 = {s: ((cd.get(s) or {}).get('B4') or {}) for s in ('earth', 'bio')}
    J['B4'] = (all(v.get('secs', 0) > 0 and v.get('bd') == 0 for v in b4.values()), b4)
    t1p, t1h = pc.get('T1') or {}, ph.get('T1') or {}
    def opened(v):
        return bool(v) and v.get('ied') and v.get('칸 값 = 원래') is True
    ok1 = opened(t1p.get('길게')) and not (t1p.get('짧게') or {}).get('ied', True) and opened(t1h.get('길게(제목 줄)')) and opened(t1h.get('길게(오른쪽 끝)')) \
        and opened(t1h.get('길게(왼쪽 번호 · 코드)')) and t1h.get('왼쪽(번호 · 코드) = 제목 글자 밖') and not (t1h.get('짧게') or {}).get('ied', True)
    J['T1'] = (bool(ok1), {'PC 마우스': t1p, '폰 손가락': t1h})
    t2 = pc.get('T2') or {}
    J['T2'] = (bool(t2) and '하네스 오류' not in t2 and _all({k: v for k, v in t2.items()}), t2)
    t3 = pc.get('T3') or {}
    J['T3'] = (bool(t3) and '하네스 오류' not in t3 and _all(t3), t3)
    t4 = ph.get('T4') or {}
    J['T4'] = (bool(t4) and t4.get('잘림') is True and t4.get('짧게 → 말풍선') is True and _all({k: v for k, v in (t4.get('이어 길게') or {}).items() if k != 'click 셈'})
               and (t4.get('이어 길게') or {}).get('click 셈') == 0 and _all(t4.get('칸 안 누름') or {}), t4)
    t5 = {s: (cd.get(s) or {}).get('T5') or {} for s in ('earth', 'bio')}
    ok5 = all(bool(v) and all(isinstance(q, dict) and '하네스 오류' not in q and _all({k: w for k, w in q.items() if k != '옛 꼴'}) for q in v.values()) for v in t5.values()) \
        and len(t5['earth']) == 2 and len(t5['bio']) == 1 and bool(cph) and '하네스 오류' not in cph and _all({k: v for k, v in cph.items() if k != '_T9'})
    J['T5'] = (ok5, {'PC 마우스': t5, '지학 폰 손가락': {k: v for k, v in cph.items() if k != '_T9'}})
    t6 = {s: (cd.get(s) or {}).get('T6') or {} for s in ('earth', 'bio')}
    e6 = t6['earth']
    bd6 = ((((base or {}).get('cd') or {}).get('earth') or {}).get('T6') or {}).get('글자 고치기') if base else None
    md = (e6.get('글자 고치기') or {}).get('표시 md5')
    bmd = (bd6 or {}).get('표시 md5') if bd6 is not None else QC.base('T6.표시@%s' % x.get('eng'), md)
    def s6(v):
        s = v.get('위 검색') or {}
        return bool(v.get('제목 고침')) and s.get('그 문항') and s.get('줄 수') == 1 and v.get('tfixAny 거짓') is True
    g = e6.get('글자 고치기') or {}
    ok6 = s6(e6) and s6(t6['bio']) and g.get('tfixSheet') and g.get('TFIX q = 글') and g.get('카드에 보임') and md is not None and md == bmd \
        and (e6.get('쓴 문항 창') or {}).get('쓰인 수 누름') and (e6.get('쓴 문항 창') or {}).get('비교 창 제목 = 고친 제목')
    J['T6'] = (bool(ok6), {'지학': e6, '생물': t6['bio'], '바탕 표시 md5': bmd})
    J['T7'] = (all(bool(v) and '하네스 오류' not in v and all(v.get(k) is True for k in ('A 고침', 'B 받음', 'A 비움', 'B 비움 받음')) for v in (sy.get('phys'), sy.get('earth'))), sy)
    t8 = {'PC 마우스': pc.get('T8') or {}, '폰 손가락': ph.get('T8') or {}}
    sig = json.dumps(t8, ensure_ascii=False, sort_keys=True)
    if base:
        bsig = json.dumps({'PC 마우스': ((base.get('pc') or {}).get('T8') or {}), '폰 손가락': ((base.get('ph') or {}).get('T8') or {})}, ensure_ascii=False, sort_keys=True)
    else:
        bsig = QC.base('T8.sig@%s' % x.get('eng'), sig)
    J['T8'] = (all(len(v) == 4 for v in t8.values()) and _all(t8) and sig == bsig, {'잰 것': t8, '바탕과 같음': sig == bsig})
    J['T9'] = j9([pc.get('_T9') or {'넘침': [], '창': [], '칸': [], '✓': []}, ph.get('_T9') or {'넘침': [], '창': [], '칸': [], '✓': []},
                  cd.get('_T9') or {'넘침': [], '창': [], '칸': [], '✓': []}, cph.get('_T9') or {'넘침': [], '창': [], '칸': [], '✓': []}], x.get('_errs') or [])
    return J


NAMES = {
    'B1': '물리 서랍 단원 머리 63 다 .ndbd · 1.11 등속 원운동 = [5] · BUNDLES 를 DATA 로 다시 셈 = 24 묶음 · 63 단원 · 577 · 빠짐 0 · 겹침 0 · 이름 = 서랍',
    'B2': '[N] 누름(마우스 · 손가락) = #bdPop 머리 「[N] 이름 a+e=n」 · 왜 · 줄 = 단원 수 · .cur · a = PA · e = 나머지(DATA) · 「기출」「PEM」 0 · 화면 안',
    'B3': '같은 [N] = 닫힘 · 바깥 = 닫힘 · g3Pop ↔ bdPop 서로 닫음 · [N] 누름이 서랍 접기 · 첫 화면 스크롤 · 문항 열기 0',
    'B4': '지학 · 생물 서랍 .ndbd 0',
    'T1': '물리 #vT1 길게 600ms(마우스 · 손가락) = .vtt.ied .iedin 값 = titleOf · 폰 줄 오른쪽 끝(제목 글자 밖)도 · 짧게 150ms = 안 열림',
    'T2': '지어낸 제목 Enter → TFIX[P###].nm · 머리 · 서랍 · 정리 창 .pnm · 첫 화면 목록 · 다시 열기 · 새로고침 · Esc · 바깥 = 안 바뀜 · 비움 = 원래',
    'T3': '서랍 줄 제목 길게 → 고쳐 저장 → 머리 제목도 같은 글',
    'T4': '폰 잘린 제목 짧게 = #g3Tip → 이어 길게 = 칸 · 말풍선 없음 · click 안 샘(문항 · 창 그대로) · 칸 안 누름 = 칸 그대로',
    'T5': '지학 기출 · 확인문제 · 생물 — 머리 원래 = 소단원 · 길게 = 칸 · TFIX[uid].nm · 파랑 · 서랍 꼬리 .ndtt.fx · 서랍 파랑 길게 = 칸 · 비움 = 옛 꼴(+ 지학 폰 손가락)',
    'T6': '카드 층 위 검색(문제) 고친 제목 낱말 → 그 문항 · tfixAny 거짓 · 글자 고치기(tfixSheet) 표시 = 바탕 · 「이 글을 쓴 문항」 → 비교 창 제목 = 고친 제목',
    'T7': '동기화 기기 둘(공용 원격 흉내) — A 고침 → B 같은 제목 · 비움도 → 물리 · 지학',
    'T8': '다른 길게 무변 — 정리 창 이름 .pnm · 공식 칸 .frcell 길게 = 고치기 칸 · 짧게 = 안 열림(= 바탕)',
    'T9': '위 화면 페이지 오류 0 · 가로 넘침 0 · 폰 ✓ · 입력 칸 높이 ≤ 26 · 새 창(#bdPop · #g3Tip) 높이 ≤ innerHeight/3',
}
SAME = {'B4', 'T8', 'T9'}   # 지시서 헛잣대 — 바탕도 PASS 여야 맞는 칸


def run_ver(brs, eng, ver):
    x = {'eng': eng}
    errl = []
    def keep(name, p):
        try:
            e, ro = errs(p)
            errl.append((name, e))
            x.setdefault('_ro', 0)
            x['_ro'] += ro
        except Exception:
            errl.append((name, ['(오류 못 읽음)']))
        p.close()
    br = brs[eng]
    try:
        o, T9, p = flow_phys_pc(br, eng, ver)
        o['_T9'] = T9; x['pc'] = o; keep('물리 PC', p)
    except Exception:
        x['pc'] = {'하네스 오류': traceback.format_exc()[-700:]}
    if QC.SMOKE:
        x['_errs'] = errl
        return x
    for k, fn, nm in (('ph', flow_phys_ph, '물리 폰'),):
        try:
            o, T9, p = fn(br, eng, ver)
            o['_T9'] = T9; x[k] = o; keep(nm, p)
        except Exception:
            x[k] = {'하네스 오류': traceback.format_exc()[-700:]}
    try:
        o, T9, pages = flow_card_pc(br, eng, ver)
        o['_T9'] = T9; x['cd'] = o
        for s, p in zip(('지학 PC', '생물 PC'), pages):
            keep(s, p)
    except Exception:
        x['cd'] = {'하네스 오류': traceback.format_exc()[-700:]}
    try:
        o, T9, p = flow_card_ph(br, eng, ver)
        o['_T9'] = T9; x['cph'] = o; keep('지학 폰', p)
    except Exception:
        x['cph'] = {'하네스 오류': traceback.format_exc()[-700:]}
    try:
        o, pages = flow_sync(br, eng, ver)
        x['sy'] = o
        for s, p in zip(('동기 물리 A', '동기 물리 B', '동기 지학 A', '동기 지학 B'), pages):
            keep(s, p)
    except Exception:
        x['sy'] = {'하네스 오류': traceback.format_exc()[-700:]}
    x['_errs'] = errl
    return x


def main():
    os.makedirs(TMPD, exist_ok=True)
    R('B0', '판 · 자리', None, None, {'NEW': NEWF, 'md5(LF)': {k: hashlib.md5(v.replace('\r\n', '\n').encode('utf-8')).hexdigest()[:8] for k, v in SRC.items()},
                                     'BASE': BASE if GATE else '(regress · smoke = 안 띄움)', '엔진': ENGS, '길게 · 짧게 ms': [LONG, SHORT]})
    res, t0 = {}, time.time()
    vers = ['NEW'] + (['BASE'] if GATE else [])
    engs = ENGS if not QC.SMOKE else ['chromium']
    with sync_playwright() as pw:
        brs = {e: getattr(pw, e).launch() for e in engs}
        for eng in engs:
            for ver in vers:
                QC.launch('base' if ver == 'BASE' else 'new')
                t1 = time.time()
                res[(ver, eng)] = run_ver(brs, eng, ver)
                R('B0', '%s %s 돎' % (ver, eng), None, None, {'분': round((time.time() - t1) / 60, 1), 'ResizeObserver loop 알림': res[(ver, eng)].get('_ro', 0)})
        for b in brs.values():
            b.close()
    try:
        with open(os.path.join(TMPD, 'raw.json'), 'w', encoding='utf-8') as f:
            json.dump({'%s|%s' % k: v for k, v in res.items()}, f, ensure_ascii=False, default=str, indent=1)
    except Exception:
        pass
    for eng in engs:
        n = res.get(('NEW', eng)) or {}
        b = res.get(('BASE', eng))
        jb = judge(b, base=b) if b else {}
        jn = judge(n, base=b)
        for c in NAMES:
            if not want(c):
                continue
            ok, d = jn[c]
            bb = jb.get(c) if jb else None
            R('%s[%s]' % (c, eng), NAMES[c], bool(ok), None if bb is None else bool(bb[0]), {'새 판': d, '바탕': bb[1]} if bb is not None else d, yard=(c not in SAME))
    newp = [x for x in RES if x['new'] is not None]
    yard = [x for x in RES if x['base'] is not None and x['yard']]
    same = [x for x in RES if x['base'] is not None and not x['yard']]
    R('B9', '합 — 새 판 PASS %d · FAIL %d · 헛잣대(새 칸 바탕 FAIL) %d/%d · 바탕도 같음 칸 바탕 PASS %d/%d · %.1f 분' % (
        sum(1 for x in newp if x['new']), sum(1 for x in newp if not x['new']), sum(1 for x in yard if not x['base']), len(yard),
        sum(1 for x in same if x['base']), len(same), (time.time() - t0) / 60), None)
    os.makedirs(os.path.dirname(os.path.abspath(OUTF)), exist_ok=True)
    with open(OUTF, 'w', encoding='utf-8') as f:
        for x in RES:
            tag = 'INFO' if x['new'] is None else ('PASS' if x['new'] else 'FAIL')
            yb = '' if x['base'] is None else (' · 바탕 ' + (('PASS(바탕도 같음)' if not x['yard'] else 'PASS') if x['base'] else ('FAIL' if x['yard'] else 'FAIL(바탕도 같아야 할 칸)')))
            f.write('%s | %s · %s%s | %s\n' % (tag, x['g'], x['name'], yb, _s(x['d'])[:2400]))
    return 0 if newp and all(x['new'] for x in newp) else 1


if __name__ == '__main__':
    sys.exit(main())
