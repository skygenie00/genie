# -*- coding: utf-8 -*-
r"""_task_jo_mokchip §B 관문 — 목차노트 창 줄 칩(기출·사례·GS·판례) → 그 노트 블록 전부에서 모은 카드 목록 창(popNoteList 그대로)

  python _harness_jo_mokchip.py [--new <앱>] [--base <앱 파일 | git rev>] [--eng chromium,webkit] [--only b1,b2,...] [--res <결과>]

  NEW = genie 작업트리 jo/index.html · BASE(헛잣대) = 착수 때 HEAD(기본 HEAD — 이 판을 커밋한 뒤에는 --base cedc251)
  데이터 = genie jo/data(실물 · note_backlink · note_<법> 읽기만) · 원격 = 같은 출처만(밖 주소 404 · 기록 쓰기 0)
  도구 = _qa/jopangi/공통/_harness/_harness_jo_mok_popup_phone.py 의 serve(SEED · __HM) · P(책상 1440 마우스 · 아이패드 834 · 폰 390 터치)를 불러 쓴다
  기대 카드 = 데이터에서 파이썬으로 센 것(노트 줄 위에서 블록이 처음 나온 차례 · 줄에 없는 블록은 그 뒤 열쇠 차례 · 같은 값 한 번)
  fix1(_task_jo_mokchip_fix1) = B12 · B13 — 40자 넘는 노트 이름에서 목차 칩 창과 블록 칩 창(…#^id) 키가 같아지던 것(--base 00a93ea 로 헛잣대)
    창 찾기는 새 키(자르지 않음)와 00a93ea 까지의 키(앞 40자)를 둘 다 받는다 — B1~B11 은 어느 바탕에서도 같은 잣대
"""
import os as _os_r, sys as _sys_r
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402  — _task_qa_slim: --mode · --snap-in · --snap-out 을 여기서 뗀다(아래 인자 읽기는 이 판 앞과 같다)
# --mode gate|regress|smoke (_task_qa_slim 2026-10-04 · 인자 없으면 gate = 이 판 앞과 같다 · gate 경로는 원본과 글자까지 같다 — 갈래는 `if QJ.REGRESS:` · `X if QJ.GATE else Y` 로만)
#   regress = NEW 만 띄운다(바탕 풀기 · 바탕 띄우기 · git 0) · B2 는 칩 수 전수(DOM) + 표본 칩 창 · B11 은 바탕 값 대신 기준 스냅샷(QJ.base) · 엔진 × 화면마다 앱 한 번(칸 사이 = reset) · 고정 대기 → 앱 표지
#   smoke = b1(칩 하나 누름) · b7(터치)만 · WebKit 은 터치 칸만
import importlib.util, io, json, os, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = _roots.genie()
HERE = os.path.dirname(os.path.abspath(__file__))
NEWF = ARG('--new', os.path.join(GENIE, 'jo', 'index.html'))
BASEF = ARG('--base', 'HEAD')
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_mokchip_result.txt'))
DATA = os.path.join(GENIE, 'jo', 'data')

# 목차노트 창 도구(serve · P · __HM) — 그 하네스는 들어올 때 sys.argv 를 읽는다
_argv = sys.argv; sys.argv = [sys.argv[0]]
_mp = os.path.join(HERE, '..', '공통', '_harness', '_harness_jo_mok_popup_phone.py')
_spec = importlib.util.spec_from_file_location('_harness_jo_mok_popup_phone', _mp)
MP = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(MP)
sys.argv = _argv

LAWS = [('특허법', '특허'), ('상표법', '상표'), ('민사소송법', '민소'), ('디자인보호법', '디보')]
KINDS = ['기출', '사례', 'GS', '판례']
N1 = '1.3.1.{법정}직사토(보독관)'
# fix1 — 긴 노트 이름(UTF-16 40 · 44자) · 「기출」 블록 칩이 둘 이상인 노트
LONG = [('민사소송법', '7.7.1.{보참}(후발)보조참가(71조)-없어불판사,보피공주다,없어방실', '0f8334', '09b8fb'),
        ('상표법', '5.9.{민사}{침}(107){손}(109)산정(110)법손(111){신}{부}', 'd400ce', '6314a5')]
ROWS = []
APPS = {}
# ── _task_qa_slim — regress(A-1) · 앱 한 번 띄움(A-2) 상수 ──
T_UP = 6000      # 앱 반응(창 뜸 · 닫힘) 기다림 한도(ms) — 반응이 있으면 그 즉시 · 한도까지 가는 것은 반응이 없는(FAIL 갈래) 때뿐
T_LOAD = 30000   # 첫 자료 읽기(머리 탭 수 · 목록 줄) 한도(ms) — 같은 뜻
T_TAIL = 80      # 눌린 뒤 「창이 더 뜨지 않나」 보는 여유(ms)
NOTES = {}       # regress — 관문별 값 끝 말(표본 n/N)
SMOKE_G = ('b1', 'b7')   # smoke 칸 — b1 = 칩 하나 누름(싸고 핵심) · b7 = 터치 칸
TOUCH_G = ('b7',)        # smoke 에서 WebKit 은 터치 칸만(규칙 57)


def R(g, eng, name, okn, okb, val):
    ROWS.append((g, eng, name, okn, okb, val))
    print('%s | 바탕 %s | %s · %s · %s | %s' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, eng, name,
          (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str))[:700]), flush=True)


def git(*a):
    return subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def app_src(x):
    if os.path.isfile(x):
        return open(x, 'rb').read().decode('utf-8').replace('\r\n', '\n')
    QJ.sub('git:show-app')
    return git('show', '%s:jo/index.html' % x).decode('utf-8').replace('\r\n', '\n')


# ── 기대 카드(앱 mokCite 와 같은 규칙을 데이터에서 따로 센다) ──
def cite_all():
    B = json.load(io.open(os.path.join(DATA, 'note_backlink.json'), encoding='utf-8'))
    ids = {}
    for k in B:
        i = k.find('#^')
        if i >= 0:
            ids.setdefault(k[:i], []).append(k[i + 2:])
    out = {}
    for law, sh in LAWS:
        try:
            N = json.load(io.open(os.path.join(DATA, 'note_%s.json' % sh), encoding='utf-8'))
        except Exception:
            N = {}
        m = {}
        for f in N:
            rows = (N.get(f) or {}).get('행') or []
            at = {}
            for j, r in enumerate(rows):
                if isinstance(r, dict) and r.get('id') and r['id'] not in at:
                    at[r['id']] = j
            o = {c: [] for c in KINDS}
            for bid, _ in sorted([(x, at.get(x, len(rows) + j)) for j, x in enumerate(ids.get(f, []))], key=lambda t: t[1]):
                v = B.get(f + '#^' + bid) or {}
                for c in KINDS:
                    for x in v.get(c) or []:
                        if x not in o[c]:
                            o[c].append(x)
            m[f] = o
        out[sh] = m
    return out


EXP = {}


def vis50(v):
    """popNoteList 줄 글(String(v).slice(0,50) · UTF-16 단위) → 화면 글(__MK.tx = 빈칸 덩이 하나 · 앞뒤 빈칸 뺌)과 같은 꼴"""
    u = str(v).encode('utf-16-le')[:100].decode('utf-16-le', 'ignore')
    return ' '.join(u.split())

MKJS = r"""
window.__MK={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 R(e){if(!e)return null;const r=e.getBoundingClientRect();return {l:+r.left.toFixed(1),t:+r.top.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1),r:+r.right.toFixed(1),b:+r.bottom.toFixed(1)}},
 vv(){const v=window.visualViewport;return v?{x:v.offsetLeft,y:v.offsetTop,w:v.width,h:v.height}:{x:0,y:0,w:innerWidth,h:innerHeight}},
 mk(){return POPS.find(x=>(x._pk||'').indexOf('moknote|')===0)||null},
 row(n){const p=__MK.mk();return p?[...p.querySelectorAll('.mklist .mkr')].find(r=>r.dataset.note===n)||null:null},
 chip(n,k){const r=__MK.row(n);return r?[...r.querySelectorAll('.ck')].find(c=>__MK.tx(c).split(' ')[0]===k)||null:null},
 async at(e){if(!e)return null;try{e.scrollIntoView({block:'center',inline:'nearest'})}catch(_){}await new Promise(r=>setTimeout(r,220));
   const r=e.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2,a=document.elementFromPoint(cx,cy);return {cx,cy,on:!!a&&(a===e||e.contains(a)),r:__MK.R(e)}},
 pops(){return POPS.filter(p=>p.isConnected).map(p=>({k:p._pk,t:__MK.tx(p.querySelector('.pt')),grp:[...p.querySelectorAll('.pb .grp')].map(__MK.tx),
   res:[...p.querySelectorAll('.pb .res')].map(d=>__MK.tx(d.querySelector('b'))),r:__MK.R(p),z:+p.style.zIndex||0}))},
 on(n){const r=__MK.row(n);return !!(r&&r.classList.contains('on'))},
 key:(k,n)=>'cell|🔗 '+k+' — '+String(n),
 keyCut:(k,n)=>'cell|🔗 '+k+' — '+String(n).slice(0,40),   /* 00a93ea 까지 — 창 키도 앞 40자 */
 findList(k,n){return POPS.find(x=>x._pk===__MK.key(k,n))||POPS.find(x=>x._pk===__MK.keyCut(k,n))||null},
 lists(){return POPS.filter(p=>p.isConnected&&String(p._pk||'').indexOf('cell|🔗 ')===0).map(p=>p._pk)},
 raise(p){if(!p)return false;p.style.zIndex=++POPZ;try{popAllSync()}catch(_){}return true},   /* 하네스 준비만 — 누를 창을 맨 위로(폰에서 창끼리 겹침) */
 raiseMk(){return __MK.raise(__MK.mk())},
 raiseNote(n){return __MK.raise(POPS.find(x=>x._pk==='note|'+PLAW()+'|'+n+'|'))},
 closeExceptMk(){POPS.slice().forEach(p=>{if((p._pk||'').indexOf('moknote|')!==0)closeOne(p)});return POPS.length},
 async waitPop(pk,ms){for(let i=0;i<(ms||3000)/50;i++){const p=POPS.find(x=>x._pk===pk);if(p&&p.querySelector('.pb .grp,.pb .cdim'))return true;await new Promise(r=>setTimeout(r,50))}return false},
 /* B-2 — 칩마다 JS 누름 → 창 줄 · 수 · 같은 값 두 번 · 노트 팝업 */
 async sweepChips(limit){const p=__MK.mk();if(!p)return null;const out=[];let n=0;
   for(const r of [...p.querySelectorAll('.mklist .mkr')]){const f=r.dataset.note;
     for(const c of [...r.querySelectorAll('.ck')]){if(limit&&n>=limit)return out;n++;
       const [k,v]=__MK.tx(c).split(' ');c.click();
       let q=null;for(let i=0;i<80;i++){q=__MK.findList(k,f);if(q&&q.querySelector('.pb .grp,.pb .cdim'))break;await new Promise(z=>setTimeout(z,25))}
       const np=POPS.find(x=>(x._pk||'').indexOf('note|')===0);
       out.push({f,k,v:+v,key:!!q,grp:q?__MK.tx(q.querySelector('.pb .grp')):null,res:q?[...q.querySelectorAll('.pb .res')].map(d=>__MK.tx(d.querySelector('b'))):null,note:!!np});
       __MK.closeExceptMk();await new Promise(z=>setTimeout(z,10))}}
   return out},
 /* B-7 — 누름 칸 재기(가로·세로로 elementFromPoint) */
 hit(c){const r=c.getBoundingClientRect(),row=c.closest('.mkr').getBoundingClientRect(),x=r.left+r.width/2,y=r.top+r.height/2;
   const ys=[],xs=[];for(let t=Math.floor(row.top-4);t<=Math.ceil(row.bottom+4);t++){const a=document.elementFromPoint(x,t+0.5);if(a&&(a===c||c.contains(a)))ys.push(t+0.5)}
   for(let s=Math.floor(r.left-8);s<=Math.ceil(r.right+8);s+=0.5){const a=document.elementFromPoint(s+0.25,y);if(a&&(a===c||c.contains(a)))xs.push(s+0.25)}
   return {vis:__MK.R(c),row:__MK.R(c.closest('.mkr')),hy:ys.length?[ys[0],ys[ys.length-1]]:null,hx:xs.length?[xs[0],xs[xs.length-1]]:null,
     h:ys.length,w:xs.length/2}},
 blockChip(n,id,k){const p=POPS.find(x=>x._pk==='note|'+PLAW()+'|'+n+'|');if(!p)return null;
   const bl=[...p.querySelectorAll('.ntbl')].find(b=>(b.parentElement&&__MK.tx(b.parentElement).indexOf(id)>=0));if(!bl)return null;
   return [...bl.querySelectorAll('.chip')].find(c=>__MK.tx(c).split(' ')[0]===k)||null},
 sw(){const vw=innerWidth,vh=innerHeight,de=document.documentElement;
   const pops=POPS.filter(p=>p.isConnected).map(p=>{const r=p.getBoundingClientRect();return {k:String(p._pk||'').slice(0,46),out:r.left<-0.5||r.right>vw+0.5||r.top<-0.5||r.bottom>vh+0.5,ow:Math.max(0,p.scrollWidth-p.clientWidth),box:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]}});
   const mkr=(()=>{const p=__MK.mk();if(!p)return null;return [...p.querySelectorAll('.mklist .mkr')].filter(r=>r.scrollWidth>r.clientWidth+1).length})();
   return {docow:de.scrollWidth-de.clientWidth,pops,mkrOver:mkr}},
 errs(){return (window.__ERR||[]).slice(0,6)}
};
"""

VPS = {'PC': (1440, 900, 'desk'), 'iPad': (834, 1194, 'pad'), '폰': (390, 844, 'phone')}


# ══════════ _task_qa_slim A-2 — regress: 엔진 × 화면마다 앱을 한 번만 띄우고 칸 사이는 되돌려 잇는다 ══════════
# (gate 는 아래 page() 그대로 — 관문마다 새 컨텍스트 · MP.P 는 안 고친다)
RJS = r"""
window.__RJ={
 /* 두 프레임 + 안전 타이머 — 앱 ResizeObserver → hdrFit(앱 2139) · showPop 다음 틱 vvFit(앱 3218) 이 한 번 돈 뒤 */
 frames(){return new Promise(res=>{let d=false;const f=()=>{if(!d){d=true;res(true)}};try{requestAnimationFrame(()=>requestAnimationFrame(f))}catch(_){f()}setTimeout(f,300)})},
 /* 머리 탭 수가 다 차고(앱 railCounts 2146 — set() 이 #hrail b[data-n] 마다 글자를 채운다) 목차노트 단추가 켜짐(앱 2167 mb.disabled=!n) · render 끝(busy 꺼짐) */
 railDone(){const bs=[...document.querySelectorAll('#hrail b[data-n]')],m=document.getElementById('mokBtn');
   return bs.length>0&&bs.every(b=>String(b.textContent||'').trim()!=='')&&!!m&&!m.disabled&&typeof busy!=='undefined'&&!busy},
 /* __HM.go 와 같은 일(clean → idle → S 바꿈 → render → idle) — 끝의 고정 450ms 만 뺐다(그 몫은 railDone) */
 async goQ(law,tab,o){__HM.clean();for(let i=0;i<320&&busy;i++)await new Promise(r=>setTimeout(r,25));
   S.law=law;S.tab=tab;
   if(tab==='cha2'){S.boardKind='기출';S.series='';S.yearFilter='';S.cha2Sel=null;S.cha2Filter={};}
   if(tab==='prec'){S.precQ='';S.precFilter={};}
   Object.assign(S,o||{});await render();for(let i=0;i<320&&busy;i++)await new Promise(r=>setTimeout(r,25));
   return {tab:S.tab,law:S.law}},
 /* 앱 상태 S 첫 기록(부팅 끝 직후) — reset 이 이 값으로 되돌린다(JSON 으로 못 적는 값은 건드리지 않는다) */
 snap(){const o={};for(const k of Object.keys(S)){let v;try{v=JSON.stringify(S[k])}catch(e){v=undefined}o[k]=(typeof v==='string')?v:null}window.__S0=o;return Object.keys(o).length},
 /* IndexedDB — 있는 DB 만 열어 저장소 내용을 비운다(DB 를 지우지 않는다 · 앱이 열어 둔 DB 를 막지 않게 · 앱 15970 ox_master_db) */
 async idbClear(){try{if(!(window.indexedDB&&indexedDB.databases))return 0;const ds=(await indexedDB.databases())||[];let n=0;
   for(const d of ds){if(!d||!d.name)continue;
     await new Promise(res=>{let done=false;const fin=()=>{if(!done){done=true;res(true)}};setTimeout(fin,600);
       try{const rq=indexedDB.open(d.name);rq.onerror=fin;rq.onblocked=fin;
         rq.onsuccess=()=>{const db=rq.result;try{const ns=[...db.objectStoreNames];if(!ns.length){db.close();return fin()}
           const tx=db.transaction(ns,'readwrite');ns.forEach(x=>tx.objectStore(x).clear());n++;
           tx.oncomplete=()=>{try{db.close()}catch(_){}fin()};tx.onerror=()=>{try{db.close()}catch(_){}fin()};tx.onabort=()=>{try{db.close()}catch(_){}fin()}}
         catch(e){try{db.close()}catch(_){}fin()}}}catch(e){fin()}})}
   return n}catch(e){return -1}},
 /* 칸 사이 되돌림 — 팝업 닫기 · S 첫 값 · 굴림 0 · localStorage(SEED 와 같은 첫 상태) · 오류 목록 · IndexedDB */
 async reset(){
   try{__HM.clean()}catch(e){}
   try{for(let i=0;i<320&&busy;i++)await new Promise(r=>setTimeout(r,25))}catch(e){}
   try{const o=window.__S0;if(o){for(const k of Object.keys(S)){if(!(k in o))delete S[k]}for(const k of Object.keys(o)){if(o[k]!==null){try{S[k]=JSON.parse(o[k])}catch(e){}}}}}catch(e){}
   try{document.querySelectorAll('#slot .main,#slot .tree,#slot .plist,#slot .qlwrap').forEach(n=>{n.scrollTop=0});const h=document.getElementById('hrail');if(h)h.scrollLeft=0;window.scrollTo(0,0)}catch(e){}
   try{localStorage.clear();localStorage.setItem('tt.cfg',JSON.stringify({person:'꼬까'}))}catch(e){}
   try{if(window.__ERR)window.__ERR.length=0}catch(e){}
   try{__HM.spyReset()}catch(e){}
   try{await __RJ.idbClear()}catch(e){}
   return true}
};
/* __MK.at — scrollIntoView 뒤 고정 220ms 대신 두 프레임(이 이름을 부르는 모든 칸이 같이 빨라진다 · 재는 식은 그대로) */
__MK.at=async function(e){if(!e)return null;try{e.scrollIntoView({block:'center',inline:'nearest'})}catch(_){}await __RJ.frames();
  const r=e.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2,a=document.elementFromPoint(cx,cy);return {cx,cy,on:!!a&&(a===e||e.contains(a)),r:__MK.R(e)}};
/* B2 regress — 모든 줄 · 모든 칩의 (노트 · 갈래 · 수) 를 눌러 보지 않고 읽는다 */
__MK.census=function(){const p=__MK.mk();if(!p)return null;const out=[];
  for(const r of [...p.querySelectorAll('.mklist .mkr')]){const f=r.dataset.note;
    for(const c of [...r.querySelectorAll('.ck')]){const t=__MK.tx(c).split(' ');out.push({f:f,k:t[0],v:+t[1]})}}
  return out};
/* B2 regress — sweepChips 와 같은 누름 · 같은 기다림 · 같은 읽기, 고른 (노트 · 갈래) 쌍만 */
__MK.sweepSome=async function(pairs){const p=__MK.mk();if(!p)return null;const want=new Set(pairs.map(x=>x[0]+'\u0001'+x[1]));const out=[];
  for(const r of [...p.querySelectorAll('.mklist .mkr')]){const f=r.dataset.note;
    for(const c of [...r.querySelectorAll('.ck')]){const [k,v]=__MK.tx(c).split(' ');if(!want.has(f+'\u0001'+k))continue;
      c.click();
      let q=null;for(let i=0;i<80;i++){q=__MK.findList(k,f);if(q&&q.querySelector('.pb .grp,.pb .cdim'))break;await new Promise(z=>setTimeout(z,25))}
      const np=POPS.find(x=>(x._pk||'').indexOf('note|')===0);
      out.push({f,k,v:+v,key:!!q,grp:q?__MK.tx(q.querySelector('.pb .grp')):null,res:q?[...q.querySelectorAll('.pb .res')].map(d=>__MK.tx(d.querySelector('b'))):null,note:!!np});
      __MK.closeExceptMk();await new Promise(z=>setTimeout(z,10))}}
  return out};
0;   /* 마지막 값이 함수면 Playwright evaluate 가 그 함수를 불러 버린다(식이 함수면 자동 호출) — 함수 아닌 값으로 끝낸다 */
"""
# 앱이 이미 내놓는 표지(창 키 · 줄 · 칩 클래스) — 표지 목록 = _qa_slim_out/_a2/_harness_jo_mokchip_표지.md
JS_LIST_OPEN = "([n,k])=>{const p=__MK.findList(k,n);return !!p&&!!p.querySelector('.pb .grp,.pb .cdim')}"   # 목록 창 + 줄(.grp · .cdim — 앱 popNoteList 7027 · 7040)이 찼다
JS_LIST_GONE = "([n,k])=>!__MK.findList(k,n)"                                                              # 같은 칩 다시 = 닫힘(앱 popToggle 3197)
JS_NOTE_OPEN = "n=>!!POPS.find(x=>x._pk==='note|'+PLAW()+'|'+n+'|')"                                       # 노트 팝업 키(앱 popNote 6786) — 줄은 만들 때 한 번에 찬다
JS_CARD_OPEN = "()=>!!POPS.find(x=>String(x._pk||'').indexOf('cell|🧾')===0)"                              # 카드 팝업 키(앱 popCard4)
JS_ANY_OPEN = ("()=>{const ps=POPS.filter(p=>p.isConnected&&String(p._pk||'').indexOf('moknote|')!==0);"
               "return ps.length>0&&ps.every(p=>String(p._pk||'').indexOf('cell|🔗 ')!==0||!!p.querySelector('.pb .grp,.pb .cdim'))}")   # 목차노트 목록 밖 창이 하나 이상 · 목록 창은 줄이 참


class RigP(MP.P):
    """regress 전용 — MP.P(뿌리 · 안 고침)와 같은 맥락(서버 · 화면 · route · goto · READY)을 한 번만 만들고 칸 사이는 reset 으로 되돌려 쓴다.
    MP.P 와 다른 점 둘 — ① 끝의 고정 1.5초 → 앱 표지(첫 render 끝 = busy 꺼짐) ② close() = 닫지 않고 되돌림(진짜 닫기는 shut)"""

    def __init__(self, br, eng, tag, src, W, H, mode='desk'):
        self.eng, self.tag, self.W, self.H, self.mode = eng, tag, W, H, mode
        self.touch = mode in ('phone', 'pad')
        self.port = MP.serve(tag, src)
        kw = dict(viewport={'width': W, 'height': H}, locale='ko-KR', timezone_id='Asia/Seoul')
        if mode == 'phone':
            self.ctx = br.new_context(device_scale_factor=3, is_mobile=True, has_touch=True, user_agent=MP.PHONE_UA, **kw)
        elif mode == 'pad':
            self.ctx = br.new_context(device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=MP.IPAD_UA, **kw)
        else:
            self.ctx = br.new_context(device_scale_factor=1, **kw)
        self.ctx.route('**/*', MP.route_filter)
        self.pg = self.ctx.new_page()
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' else None)
        self.cdp = self.ctx.new_cdp_session(self.pg) if (eng == 'chromium' and self.touch) else None
        self.dead = False
        self.pg.goto('http://127.0.0.1:%d/index.html?h=1' % self.port, wait_until='load', timeout=120000)
        self.pg.wait_for_function(MP.READY, timeout=120000)
        QJ.until(self.pg, "()=>typeof busy!=='undefined'&&!busy", T_LOAD, '앱 첫 render 끝(busy 꺼짐 · 앱 16561)')   # MP.P 의 고정 1.5초 자리
        self.ev("()=>new Promise(r=>{let d=false;const f=()=>{if(!d){d=true;r(true)}};try{requestAnimationFrame(()=>requestAnimationFrame(f))}catch(_){f()}setTimeout(f,300)})")

    def tap(self, at):
        """P.click 에서 누르기만(뒤 고정 대기 없음)"""
        if self.touch:
            self.pg.touchscreen.tap(at['cx'], at['cy'])
        else:
            self.pg.mouse.click(at['cx'], at['cy'])

    def close(self):
        """관문 함수들의 finally: q.close() — 닫지 않고 되돌린다"""
        try:
            self.pg.evaluate("()=>__RJ.reset()")
            self.errs[:] = []
        except Exception:
            self.dead = True

    def shut(self):
        MP.P.close(self)


class Rig(object):
    """regress — (엔진, 화면) 마다 RigP 하나"""

    def __init__(self):
        self.pool = {}

    def lease(self, br, eng, who, dn):
        key = (eng, dn)
        q = self.pool.get(key)
        if q is not None and (q.dead or q.pg.is_closed()):
            self.pool.pop(key, None)
            try:
                q.shut()
            except Exception:
                pass
            q = None
        if q is None:
            W, H, mode = VPS[dn]
            QJ.launch('new')
            q = RigP(br, eng, 'MK_' + who, APPS[who], W, H, mode)
            q.ev(MKJS)
            q.ev(RJS)
            q.ev("()=>__RJ.snap()")
            self.pool[key] = q
        return q

    def shut(self):
        for q in list(self.pool.values()):
            try:
                q.shut()
            except Exception:
                pass
        self.pool.clear()


RIG = Rig()


def _wait(pg, ms, why):
    """regress 의 남는 고정 대기 — QJ.sleep(…, page=pg) = page.wait_for_timeout(그동안 ctx.route 콜백 · 요청이 돈다 — time.sleep 은 Playwright 동기 API 에서 route 를 멈춘다) + QJ 대기 셈"""
    QJ.sleep(ms, why, page=pg)


def rhit(q, at, js, arg, what):
    """regress 누르기 — 누른 뒤 고정 wait 대신 앱 표지(js)가 참이 될 때까지(gate 는 호출 자리의 `q.click(at, wait)` 그대로 — 원본 줄)"""
    if not at or not at.get('on'):
        return False
    q.tap(at)
    QJ.until(q.pg, js, T_UP, what, arg)
    q.ev("()=>__RJ.frames()")
    _wait(q.pg, T_TAIL, '눌린 뒤 창이 더 뜨는지(겹친 누름 칸 · 줄 누름이 칩도 누르는 FAIL 갈래) 보는 여유 — 앱 표지 뒤에 남는 유일한 고정 대기')
    return True


def rnap(q, js, arg, what):
    """regress 기다림 — 앱 표지(js)(gate 는 호출 자리의 `q.pg.wait_for_timeout(ms)` 그대로 — 원본 줄)"""
    QJ.until(q.pg, js, T_UP, what, arg)
    q.ev("()=>__RJ.frames()")


def page(br, eng, who, dn='PC'):
    if QJ.REGRESS:
        return RIG.lease(br, eng, who, dn)   # A-2 — 엔진 × 화면마다 한 번 · 칸 사이는 q.close() 가 되돌린다
    W, H, mode = VPS[dn]
    QJ.launch('new' if who == 'NEW' else 'base')
    q = MP.P(br, eng, 'MK_' + who, APPS[who], W, H, mode)
    q.ev(MKJS)
    return q


def open_mok(q, law):
    if QJ.REGRESS:
        # A-2 — __HM.go 끝의 고정 450ms · mokAt 안 220ms · 누른 뒤 1300ms · 목록 기다림 뒤 300ms → 앱 표지(머리 탭 수 다 참 · 단추 켜짐 · 목록 줄 참)
        q.ev("([l,t])=>__RJ.goQ(l,t)", [law, 'cha2'])
        QJ.until(q.pg, "()=>__RJ.railDone()", T_LOAD, '머리 탭 수 다 참 · 목차노트 단추 켜짐(앱 railCounts 2146 · 2167)')
        q.ev("()=>__RJ.frames()")
        at = q.ev("()=>__MK.at(document.getElementById('mokBtn'))")
        if at and at.get('on'):
            q.tap(at)
            QJ.until(q.pg, "()=>!!__MK.mk()&&__MK.mk().querySelectorAll('.mklist .mkr').length>0", T_LOAD, '목차노트 목록 줄 참(앱 popMokNote 7125)')
            q.ev("()=>__RJ.frames()")
        return
    q.ev("([l,t])=>__HM.go(l,t)", [law, 'cha2'])
    at = q.ev("__HM.mokAt()")
    q.click(at, 1300)
    for _ in range(40):
        if q.ev("()=>!!__MK.mk()&&__MK.mk().querySelectorAll('.mklist .mkr').length>0"):
            break
        q.pg.wait_for_timeout(100)
    q.pg.wait_for_timeout(300)


def press_chip(q, note, kind, wait=1100):
    if QJ.REGRESS:
        was = q.ev("([n,k])=>!!__MK.findList(k,n)", [note, kind])
        at = q.ev("([n,k])=>__MK.at(__MK.chip(n,k))", [note, kind])
        rhit(q, at, JS_LIST_GONE if was else JS_LIST_OPEN, [note, kind], '칩 다시 누름 = 목록 창 닫힘(앱 popToggle 3197)' if was else '칩 누름 = 목록 창 줄 참(앱 popNoteList 7027 · 7040)')
        return at
    at = q.ev("([n,k])=>__MK.at(__MK.chip(n,k))", [note, kind])
    q.click(at, wait)
    return at


def g1(br, eng, who):
    """B1 민소 N1 「기출 3」 누름 → 새 팝업 하나 · 제목 · 「기출 — 3건」 · .res b 차례 · note 팝업 0 · 그 줄 .on"""
    q = page(br, eng, who)
    try:
        open_mok(q, '민사소송법')
        at = press_chip(q, N1, '기출')
        ps = q.ev("()=>__MK.pops()")
        key = 'cell|🔗 기출 — ' + N1[:40]
        lp = [p for p in ps if p['k'] == key]
        notes = [p for p in ps if str(p['k']).startswith('note|')]
        others = [p for p in ps if not str(p['k']).startswith('moknote|')]
        want = [vis50(x) for x in EXP['민소'][N1]['기출']]
        ok = (bool(at and at.get('on')) and len(others) == 1 and len(lp) == 1 and lp[0]['t'] == '🔗 기출 — ' + N1[:40] and lp[0]['grp'] == ['기출 — 3건']
              and lp[0]['res'] == want and not notes and q.ev("n=>__MK.on(n)", N1))
        return ok, {'누른 자리': at, '창': [(p['k'], p['t'], p['grp'], p['res']) for p in others], '기대 차례': want, '줄 .on': q.ev("n=>__MK.on(n)", N1),
                    '오류': q.errs[:2] + q.ev("()=>__MK.errs()")}
    finally:
        q.close()


def g2(br, eng, who):
    """B2 전수 — 네 법 × 줄 × 갈래 넷: 칩마다 건수 = 칩 수 = 기대 · 같은 값 두 번 0 · 차례 = 기대(판례는 수·겹침만)"""
    if QJ.REGRESS:
        return g2r(br, eng, who)
    q = page(br, eng, who)
    tot, bad, per = 0, [], {}
    try:
        for law, sh in LAWS:
            open_mok(q, law)
            res = q.ev("lim=>__MK.sweepChips(lim)", 6 if who == 'BASE' else 0) or []
            per[sh] = len(res)
            for x in res:
                tot += 1
                want = EXP[sh].get(x['f'], {}).get(x['k'], [])
                got = x['res'] or []
                okx = x['key'] and not x['note'] and x['v'] == len(want) == len(got) and len(set(got)) == len(got) and x['grp'] == '%s — %d건' % (x['k'], len(want))
                if x['k'] != '판례':
                    okx = okx and got == [vis50(w) for w in want]
                if not okx:
                    bad.append({'법': sh, '노트': x['f'][:30], '갈래': x['k'], '칩': x['v'], '기대': len(want), '줄': len(got), '창': x['key'], '노트 팝업': x['note'],
                                '다른 줄': [[i, g, vis50(w)] for i, (g, w) in enumerate(zip(got, want)) if g != vis50(w)][:2]})
        want_tot = sum(1 for sh in EXP for f in EXP[sh] for k in KINDS if EXP[sh][f][k])
        ok = not bad and (who == 'BASE' or tot == want_tot)
        return ok, {'누른 칩': tot, '데이터 칩': want_tot, '법마다': per, '틀린 칸': bad[:12], '틀린 수': len(bad)}
    finally:
        q.close()


EDGE = {}


def _edge_all():
    """B2 regress 표본 고르기용 — 노트마다 「칩 수가 블록 합보다 작다(같은 카드 겹침)」 · 「줄에 없는 블록이 있다(열쇠 차례 꼬리)」 갈래를 센다(렌더 없음 · note_backlink · note_<법> 읽기만)"""
    if EDGE:
        return EDGE
    B = json.load(io.open(os.path.join(DATA, 'note_backlink.json'), encoding='utf-8'))
    ids = {}
    for k in B:
        i = k.find('#^')
        if i >= 0:
            ids.setdefault(k[:i], []).append(k[i + 2:])
    for law, sh in LAWS:
        try:
            N = json.load(io.open(os.path.join(DATA, 'note_%s.json' % sh), encoding='utf-8'))
        except Exception:
            N = {}
        m = {}
        for f in N:
            rows = (N.get(f) or {}).get('행') or []
            have = set(r['id'] for r in rows if isinstance(r, dict) and r.get('id'))
            miss = any(b not in have for b in ids.get(f, []))
            dup = []
            for k in KINDS:
                tot = sum(len((B.get(f + '#^' + b) or {}).get(k) or []) for b in ids.get(f, []))
                if tot > len(EXP.get(sh, {}).get(f, {}).get(k, [])):
                    dup.append(k)
            m[f] = {'miss': miss, 'dup': dup}
        EDGE[sh] = m
    return EDGE


def pick_chips(sh, cen):
    """B2 regress 표본 칩 — 처음 · 끝 · 갈래마다 가장 큰 것 · 이름 40자(UTF-16) 넘는 것 · 카드 겹침 · 줄에 없는 블록 · + 씨앗 고정 20(QJ.sample)"""
    E = _edge_all().get(sh, {})
    allc = [(x['f'], x['k']) for x in cen]
    if not allc:
        return []
    pick = {allc[0], allc[-1]}
    for k in KINDS:
        ck = [(x['f'], x['k'], x['v']) for x in cen if x['k'] == k]
        if ck:
            pick.add(max(ck, key=lambda t: t[2])[:2])
    pick.update([c for c in allc if len(str(c[0]).encode('utf-16-le')) // 2 > 40][:3])
    pick.update([c for c in allc if E.get(c[0], {}).get('miss') or c[1] in E.get(c[0], {}).get('dup', [])][:4])
    pick.update(QJ.sample(allc, 20, 'mokchip-b2-' + sh))
    return [list(c) for c in allc if c in pick]


def g2r(br, eng, who):
    """B2 regress — 칩 수는 모든 줄 · 모든 칩을 DOM 에서 데이터와 맞대고(눌러 보지 않음) · 창 안(건수 = 칩 수 = 데이터 · 같은 값 두 번 0 · 차례 = 노트 줄 차례 · 노트 팝업 0)은 표본 칩만 눌러 본다"""
    q = page(br, eng, who)
    tot, bad, per, cen_n, cen_bad = 0, [], {}, 0, []
    try:
        for law, sh in LAWS:
            open_mok(q, law)
            cen = q.ev("()=>__MK.census()") or []
            cen_n += len(cen)
            gm = {}
            for x in cen:
                gm.setdefault(x['f'], {})[x['k']] = x['v']
            wm = {f: {k: len(EXP[sh][f][k]) for k in KINDS if EXP[sh][f][k]} for f in EXP[sh]}
            for f in sorted(set(wm) | set(gm)):
                if (wm.get(f) or {}) != (gm.get(f) or {}):
                    cen_bad.append({'법': sh, '노트': f[:30], '화면 칩': gm.get(f), '데이터 칩': wm.get(f)})
            res = q.ev("p=>__MK.sweepSome(p)", pick_chips(sh, cen)) or []
            per[sh] = len(res)
            for x in res:
                tot += 1
                want = EXP[sh].get(x['f'], {}).get(x['k'], [])
                got = x['res'] or []
                okx = x['key'] and not x['note'] and x['v'] == len(want) == len(got) and len(set(got)) == len(got) and x['grp'] == '%s — %d건' % (x['k'], len(want))
                if x['k'] != '판례':
                    okx = okx and got == [vis50(w) for w in want]
                if not okx:
                    bad.append({'법': sh, '노트': x['f'][:30], '갈래': x['k'], '칩': x['v'], '기대': len(want), '줄': len(got), '창': x['key'], '노트 팝업': x['note'],
                                '다른 줄': [[i, g, vis50(w)] for i, (g, w) in enumerate(zip(got, want)) if g != vis50(w)][:2]})
        want_tot = sum(1 for sh in EXP for f in EXP[sh] for k in KINDS if EXP[sh][f][k])
        NOTES['b2'] = '(표본 %d/%d)' % (tot, want_tot)
        ok = not bad and not cen_bad and cen_n == want_tot
        return ok, {'누른 칩': tot, '데이터 칩': want_tot, '법마다': per, '틀린 칸': bad[:12], '틀린 수': len(bad),
                    '칩 수 전수(DOM · 눌러 보지 않음)': {'화면 칩': cen_n, '틀린 줄': len(cen_bad), '예': cen_bad[:3]}}
    finally:
        q.close()


def g3(br, eng, who):
    """B3 같은 칩 다시 → 닫힘 · 다른 칩 → 새 창(키 다름)"""
    q = page(br, eng, who)
    try:
        open_mok(q, '민사소송법')
        k1, k2 = 'cell|🔗 기출 — ' + N1[:40], 'cell|🔗 사례 — ' + N1[:40]
        press_chip(q, N1, '기출'); a = [p['k'] for p in q.ev("()=>__MK.pops()")]
        press_chip(q, N1, '기출'); b = [p['k'] for p in q.ev("()=>__MK.pops()")]
        press_chip(q, N1, '기출'); press_chip(q, N1, '사례'); c = [p['k'] for p in q.ev("()=>__MK.pops()")]
        # 글쇠 — 칩에 초점(tabIndex 0) → Enter = 열림 · Space = 닫힘(같은 칩 다시)
        q.ev("()=>__MK.closeExceptMk()")
        foc = q.ev("([n,k])=>{const c=__MK.chip(n,k);if(!c)return false;c.focus();return document.activeElement===c}", [N1, '기출'])
        q.pg.keyboard.press('Enter'); q.pg.wait_for_timeout(1000) if QJ.GATE else rnap(q, JS_LIST_OPEN, [N1, '기출'], 'Enter = 칩 목록 창 열림'); d = [p['k'] for p in q.ev("()=>__MK.pops()")]
        q.pg.keyboard.press(' '); q.pg.wait_for_timeout(1000) if QJ.GATE else rnap(q, JS_LIST_GONE, [N1, '기출'], 'Space = 같은 칩 다시 = 닫힘'); e = [p['k'] for p in q.ev("()=>__MK.pops()")]
        ok = k1 in a and k1 not in b and k1 in c and k2 in c and foc and k1 in d and k1 not in e
        return ok, {'한 번': a, '다시': b, '기출 + 사례': c, '글쇠 초점': foc, 'Enter': d, 'Space': e}
    finally:
        q.close()


def g4(br, eng, who):
    """B4 줄 이름 누름 → 노트 팝업(note|민소|N1|) · 목록 창 0 — 바탕과 같음(자리 값 함께)"""
    q = page(br, eng, who)
    try:
        open_mok(q, '민사소송법')
        at = q.ev("n=>__MK.at(__MK.row(n)&&__MK.row(n).querySelector('.nm'))", N1)
        q.click(at, 1500) if QJ.GATE else rhit(q, at, JS_NOTE_OPEN, N1, '줄 이름 누름 = 노트 팝업 뜸(앱 popNote 6786 · mokOpenNote 7148)')
        ps = q.ev("()=>__MK.pops()")
        nk = 'note|민소|' + N1 + '|'
        note = [p for p in ps if p['k'] == nk]
        lists = [p for p in ps if str(p['k']).startswith('cell|🔗')]
        ok = len(note) == 1 and not lists and q.ev("n=>__MK.on(n)", N1)
        return ok, {'창': [(p['k'], p['r']) for p in ps]}
    finally:
        q.close()


def g5(br, eng, who):
    """B5 목록 창 줄 누름 → 카드(popCard4 기출 13-50-2) = 노트 팝업 블록 칩 길로 연 같은 줄과 같은 카드"""
    q = page(br, eng, who)
    try:
        open_mok(q, '민사소송법')
        press_chip(q, N1, '기출')
        key = 'cell|🔗 기출 — ' + N1[:40]
        at = q.ev("k=>{const p=POPS.find(x=>x._pk===k);return __MK.at(p&&p.querySelector('.pb .res'))}", key)
        q.click(at, 1500) if QJ.GATE else rhit(q, at, JS_CARD_OPEN, None, '목록 창 줄 누름 = 카드 팝업 뜸(앱 popCard4)')
        c1 = [p for p in q.ev("()=>__MK.pops()") if str(p['k']).startswith('cell|🧾')]
        # 같은 카드를 노트 팝업 블록 칩 길로
        q.ev("()=>__MK.closeExceptMk()")
        q.click(q.ev("n=>__MK.at(__MK.row(n)&&__MK.row(n).querySelector('.nm'))", N1), 1500) if QJ.GATE else rhit(q, q.ev("n=>__MK.at(__MK.row(n)&&__MK.row(n).querySelector('.nm'))", N1), JS_NOTE_OPEN, N1, '줄 이름 누름 = 노트 팝업 뜸')
        q.click(q.ev("n=>__MK.at(__MK.blockChip(n,'271d19','기출'))", N1), 1200) if QJ.GATE else rhit(q, q.ev("n=>__MK.at(__MK.blockChip(n,'271d19','기출'))", N1), JS_LIST_OPEN, [N1 + '#^271d19', '기출'], '블록 칩 누름 = 목록 창 줄 참')
        k2 = 'cell|🔗 기출 — ' + (N1 + '#^271d19')[:40]
        q.click(q.ev("k=>{const p=POPS.find(x=>x._pk===k);return __MK.at(p&&p.querySelector('.pb .res'))}", k2), 1500) if QJ.GATE else rhit(q, q.ev("k=>{const p=POPS.find(x=>x._pk===k);return __MK.at(p&&p.querySelector('.pb .res'))}", k2), JS_CARD_OPEN, None, '목록 창 줄 누름 = 카드 팝업 뜸')
        c2 = [p for p in q.ev("()=>__MK.pops()") if str(p['k']).startswith('cell|🧾')]
        ok = len(c1) == 1 and len(c2) == 1 and c1[0]['k'] == c2[0]['k'] and c1[0]['t'] == c2[0]['t'] and '13-50-2' in c1[0]['t']
        return ok, {'칩 길 카드': [(p['k'], p['t']) for p in c1], '블록 칩 길 카드': [(p['k'], p['t']) for p in c2]}
    finally:
        q.close()


def place_ok(dn, lp, np, B, w, h):
    """mokPlace 규칙(노트 팝업과 같은 식)으로 기대 자리 → 잰 자리와 맞대기(±1)"""
    if dn == '폰':
        W, H, g = B['w'] - 16, B['h'] - 16, 8
        lh = round((H - g) * 0.3); nh = H - g - lh; X = round(B['x'] + 8); Y = round(B['y'] + 8)
        e = {'lp': [X, Y, round(W), lh], 'np': [X, Y + lh + g, round(W), nh]}
        ok = (abs(lp['l'] - X) <= 1 and abs(lp['t'] - Y) <= 1 and abs(lp['h'] - lh) <= 1 and abs(np['t'] - (Y + lh + g)) <= 1 and abs(np['h'] - nh) <= 1
              and lp['b'] <= np['t'] + 0.5 and np['b'] <= B['y'] + B['h'] + 0.5 and np['r'] <= B['x'] + B['w'] + 0.5)
        return ok, e
    x = min(lp['r'] + 12, B['x'] + B['w'] - w - 8)
    if x - lp['l'] >= min(200, lp['w'] * 0.45):
        el, et = max(B['x'] + 8, x), max(B['y'] + 8, lp['t'])
    else:
        el, et = np['l'], np['t']   # 규칙 밖(좁은 화면) = showPop 자리 그대로 — 화면 안만 본다
    if et + h > B['y'] + B['h'] - 8:
        et = max(B['y'] + 8, B['y'] + B['h'] - h - 8)
    inside = np['l'] >= B['x'] - 0.5 and np['t'] >= B['y'] - 0.5 and np['r'] <= B['x'] + B['w'] + 0.5 and np['b'] <= B['y'] + B['h'] + 0.5
    return abs(np['l'] - el) <= 1 and abs(np['t'] - et) <= 1 and inside and np['l'] > lp['l'], {'np': [round(el), round(et)]}


def g6(br, eng, who):
    """B6 자리 — PC 1440 · 아이패드 834 = 목록 창 오른쪽(노트 팝업 규칙) · 화면 안 · 폰 390 = 위 30% / 아래 70% · 둘 다 화면 안 · 겹침 0"""
    out = {}; ok = True
    for dn in ('PC', 'iPad', '폰'):
        q = page(br, eng, who, dn)
        try:
            open_mok(q, '민사소송법')
            press_chip(q, N1, '기출', 1400)
            key = 'cell|🔗 기출 — ' + N1[:40]
            ps = {p['k']: p for p in q.ev("()=>__MK.pops()")}
            lp = next((p for k, p in ps.items() if str(k).startswith('moknote|')), None)
            np = ps.get(key)
            B = q.ev("()=>__MK.vv()")
            if not (lp and np):
                ok = False; out[dn] = {'창': list(ps)}; continue
            okd, e = place_ok(dn, lp['r'], np['r'], B, np['r']['w'], np['r']['h'])
            out[dn] = {'목차노트': lp['r'], '목록 창': np['r'], '기대': e, '화면': B}
            if dn == 'PC':   # 기억 자리(popSizable 'list')가 있으면 그것 — 옆 자리 규칙이 덮지 않는다
                q.ev("()=>__MK.closeExceptMk()"); q.ev("()=>__HM.setCfg('list',{x:120,y:140,w:420,h:300})")
                press_chip(q, N1, '기출', 1400)
                mr = (next((p for p in q.ev("()=>__MK.pops()") if p['k'] == key), None) or {}).get('r')
                out[dn]['기억 자리 있을 때'] = mr
                okd = okd and bool(mr) and abs(mr['l'] - 120) <= 1 and abs(mr['t'] - 140) <= 1 and abs(mr['w'] - 420) <= 1
            ok = ok and okd
        finally:
            q.close()
    return ok, out


def g7(br, eng, who):
    """B7 터치(아이패드 834 · 폰 390) — 칩 탭 = 목록 창 · 칩 사이 틈 · 칩 위아래 빈칸 탭 = 칩 또는 줄 하나 · 누름 칸 값 · 겹친 누름 칸 0"""
    out = {}; ok = True
    for dn in ('iPad', '폰'):
        q = page(br, eng, who, dn)
        try:
            open_mok(q, '민사소송법')
            D = {}
            press_chip(q, N1, '기출', 1300)
            D['칩 탭'] = [p['k'] for p in q.ev("()=>__MK.pops()") if not str(p['k']).startswith('moknote|')]
            q.ev("()=>__MK.closeExceptMk()")
            q.ev("n=>__MK.at(__MK.row(n))", N1)
            H = q.ev("n=>[...__MK.row(n).querySelectorAll('.ck')].map(c=>__MK.hit(c))", N1)
            D['누름 칸'] = [{'보이는': [h['vis']['w'], h['vis']['h']], '누름': [h['w'], h['h']], '줄': [h['row']['t'], h['row']['b']], '세로': h['hy']} for h in H]
            gaps = []
            for a, b in zip(H, H[1:]):
                if a['hx'] and b['hx']:
                    gaps.append(round(b['hx'][0] - a['hx'][1], 2))
            D['이웃 누름 칸 사이'] = gaps
            spots = []
            for a, b in zip(H, H[1:]):
                spots.append(('틈', (a['vis']['r'] + b['vis']['l']) / 2, a['vis']['t'] + a['vis']['h'] / 2))
            c0 = H[0]
            spots.append(('위', c0['vis']['l'] + c0['vis']['w'] / 2, c0['row']['t'] + 1.5))
            spots.append(('아래', c0['vis']['l'] + c0['vis']['w'] / 2, c0['row']['b'] - 1.5))
            T = []
            for nm, x, y in spots:
                q.ev("()=>__MK.closeExceptMk()")
                q.click({'cx': x, 'cy': y, 'on': True}, 1300) if QJ.GATE else rhit(q, {'cx': x, 'cy': y, 'on': True}, JS_ANY_OPEN, None, '빈칸 탭 = 목록 창 또는 노트 팝업 뜸(목차노트 목록 밖 창 · 목록 창은 줄이 참)')
                ks = [p['k'] for p in q.ev("()=>__MK.pops()") if not str(p['k']).startswith('moknote|')]
                T.append({'자리': nm, '창': ks})
            D['빈칸 탭'] = T
            okd = (D['칩 탭'] == ['cell|🔗 기출 — ' + N1[:40]] and all(len(t['창']) == 1 for t in T) and all(g >= 0 for g in gaps)
                   and all(h['hy'] and h['hy'][0] >= h['row']['t'] - 0.5 and h['hy'][1] <= h['row']['b'] + 0.5 for h in H))
            out[dn] = D; ok = ok and okd
        finally:
            q.close()
    return ok, out


def g8(br, eng, who):
    """B8 노트 팝업 안 블록 칩 「기출 2」(^271d19) → 지금과 같은 창(제목 끝 #^271d19 · 2건)"""
    q = page(br, eng, who)
    try:
        open_mok(q, '민사소송법')
        q.click(q.ev("n=>__MK.at(__MK.row(n)&&__MK.row(n).querySelector('.nm'))", N1), 1500) if QJ.GATE else rhit(q, q.ev("n=>__MK.at(__MK.row(n)&&__MK.row(n).querySelector('.nm'))", N1), JS_NOTE_OPEN, N1, '줄 이름 누름 = 노트 팝업 뜸')
        at = q.ev("n=>__MK.at(__MK.blockChip(n,'271d19','기출'))", N1)
        q.click(at, 1300) if QJ.GATE else rhit(q, at, JS_LIST_OPEN, [N1 + '#^271d19', '기출'], '블록 칩 누름 = 목록 창 줄 참')
        k = 'cell|🔗 기출 — ' + (N1 + '#^271d19')[:40]
        p = [x for x in q.ev("()=>__MK.pops()") if x['k'] == k]
        ok = len(p) == 1 and p[0]['grp'] == ['기출 — 2건'] and p[0]['t'].endswith('#^271d19'[:max(0, 40 - len(N1) - 0)]) and len(p[0]['res']) == 2
        return ok, {'블록 칩': at, '창': [(x['k'], x['t'], x['grp'], x['res']) for x in p]}
    finally:
        q.close()


def _note_open(q, f):
    q.ev("()=>__MK.raiseMk()")
    q.click(q.ev("n=>__MK.at(__MK.row(n)&&__MK.row(n).querySelector('.nm'))", f), 1500) if QJ.GATE else rhit(q, q.ev("n=>__MK.at(__MK.row(n)&&__MK.row(n).querySelector('.nm'))", f), JS_NOTE_OPEN, f, '줄 이름 누름 = 노트 팝업 뜸')


def _block_press(q, f, bid):
    q.ev("n=>__MK.raiseNote(n)", f)
    at = q.ev("([n,id])=>__MK.at(__MK.blockChip(n,id,'기출'))", [f, bid])
    if QJ.REGRESS:
        nb = f + '#^' + bid
        was = q.ev("([n,k])=>!!__MK.findList(k,n)", [nb, '기출'])
        rhit(q, at, JS_LIST_GONE if was else JS_LIST_OPEN, [nb, '기출'], '블록 칩 다시 누름 = 그 창만 닫힘' if was else '블록 칩 누름 = 목록 창 줄 참')
        return at
    q.click(at, 1300)
    return at


def _toc_press(q, f):
    q.ev("()=>__MK.raiseMk()")
    return press_chip(q, f, '기출', 1300)


def g12(br, eng, who):
    """B12 긴 노트(민소 7.7.1 · 상표 5.9.) × PC 1440 · 폰 390 — 목차 칩 「기출」 창 + 노트 팝업 블록 칩 「기출 N」 창이 같이 뜸(두 차례) · 같은 칩 다시 = 그 창만 닫힘"""
    out = {}; ok = True
    for dn in ('PC', '폰'):
        for law, f, bid, _ in LONG:
            q = page(br, eng, who, dn)
            try:
                open_mok(q, law)
                kA, kB = 'cell|🔗 기출 — ' + f, 'cell|🔗 기출 — ' + f + '#^' + bid
                D = {}
                _toc_press(q, f); _note_open(q, f); D['블록 칩'] = _block_press(q, f, bid)
                D['목차 → 블록'] = q.ev("()=>__MK.lists()")
                _toc_press(q, f); D['목차 칩 다시'] = q.ev("()=>__MK.lists()")
                q.ev("()=>__MK.closeExceptMk()")
                _note_open(q, f); _block_press(q, f, bid); _toc_press(q, f)
                D['블록 → 목차'] = q.ev("()=>__MK.lists()")
                _block_press(q, f, bid); D['블록 칩 다시'] = q.ev("()=>__MK.lists()")
                okd = (sorted(D['목차 → 블록']) == sorted([kA, kB]) and D['목차 칩 다시'] == [kB]
                       and sorted(D['블록 → 목차']) == sorted([kA, kB]) and D['블록 칩 다시'] == [kA])
                out['%s %s' % (dn, f[:6])] = D; ok = ok and okd
            finally:
                q.close()
    return ok, out


def g13(br, eng, who):
    """B13 같은 긴 노트의 블록 칩 둘(다른 ^id) → 창 둘 × PC 1440 · 폰 390"""
    out = {}; ok = True
    for dn in ('PC', '폰'):
        for law, f, b1, b2 in LONG:
            q = page(br, eng, who, dn)
            try:
                open_mok(q, law)
                _note_open(q, f); _block_press(q, f, b1); _block_press(q, f, b2)
                L = q.ev("()=>__MK.lists()")
                want = sorted(['cell|🔗 기출 — ' + f + '#^' + b1, 'cell|🔗 기출 — ' + f + '#^' + b2])
                out['%s %s' % (dn, f[:6])] = L; ok = ok and sorted(L) == want
            finally:
                q.close()
    return ok, out


def g11(br, eng, who):
    """B11 화면 훑기 — 목차노트 창(네 법) · 목록 창 · 노트 팝업 × PC · 아이패드 · 폰 — 쪽 넘침 · 창 화면 밖 · 창 안 가로 넘침 · 줄 넘침"""
    out = {}
    for dn in ('PC', 'iPad', '폰'):
        q = page(br, eng, who, dn)
        try:
            for law, sh in LAWS:
                open_mok(q, law)
                out['%s %s 목차노트' % (dn, sh)] = q.ev("()=>__MK.sw()")
                f = q.ev("()=>{const c=__MK.mk()&&__MK.mk().querySelector('.mklist .ck');return c?[c.closest('.mkr').dataset.note,__MK.tx(c).split(' ')[0]]:null}")
                if f:
                    press_chip(q, f[0], f[1], 1300)
                    out['%s %s 목록 창' % (dn, sh)] = q.ev("()=>__MK.sw()")
                    # 같은 창 바탕 꼴 — popNoteList(새 창 함수 없음 · 본문 꼴 무변)에 같은 카드를 바로 넣어 연 창의 가로 넘침(바탕에도 같은 함수가 있다)
                    q.ev("()=>__MK.closeExceptMk()")
                    out['%s %s 같은 창 직접' % (dn, sh)] = q.ev("""([k,f,it])=>popNoteList(k,f,it,null,2).then(()=>{const p=POPS.find(x=>x._pk==='cell|🔗 '+k+' — '+String(f).slice(0,40));
                      const r=p?{w:p.clientWidth,sw:p.scrollWidth,ow:Math.max(0,p.scrollWidth-p.clientWidth)}:null;__MK.closeExceptMk();return r})""", [f[1], f[0], EXP[sh][f[0]][f[1]]])
                    q.ev("()=>__MK.closeExceptMk()")
                    q.click(q.ev("n=>__MK.at(__MK.row(n)&&__MK.row(n).querySelector('.nm'))", f[0]), 1500) if QJ.GATE else rhit(q, q.ev("n=>__MK.at(__MK.row(n)&&__MK.row(n).querySelector('.nm'))", f[0]), JS_NOTE_OPEN, f[0], '줄 이름 누름 = 노트 팝업 뜸')
                    out['%s %s 노트 팝업' % (dn, sh)] = q.ev("()=>__MK.sw()")
        finally:
            q.close()
    return True, out


def sw_cmp(N, B):
    """B11 새 판 · 바탕 맞대기 — 새로 생긴 쪽 넘침 · 창 화면 밖 · 창 안 가로 넘침 · 목차 줄 넘침(칸마다 · 바탕에 없던 것만)"""
    new = []
    for k, n in N.items():
        if '같은 창 직접' in k:
            continue
        b = B.get(k) or {}
        if n.get('docow', 0) > (b.get('docow') or 0):
            new.append((k, '쪽 넘침', n['docow'], b.get('docow')))
        if (n.get('mkrOver') or 0) > (b.get('mkrOver') or 0):
            new.append((k, '목차 줄 넘침', n['mkrOver'], b.get('mkrOver')))
        bo = {p['k']: p for p in (b.get('pops') or [])}
        for p in n.get('pops') or []:
            if p['out'] and not (bo.get(p['k']) or {}).get('out'):
                new.append((k, '창 화면 밖', p['k'], p['box']))
            if p['ow'] > ((bo.get(p['k']) or {}).get('ow') or 0) + 1 and not str(p['k']).startswith('cell|🔗'):
                new.append((k, '창 안 가로 넘침', p['k'], p['ow']))
            if p['ow'] > 1 and str(p['k']).startswith('cell|🔗'):
                d = (B.get(k.replace('목록 창', '같은 창 직접')) or {})   # 바탕에서 같은 함수 · 같은 카드로 연 창
                if p['ow'] > (d.get('ow') or 0) + 1:
                    new.append((k, '목록 창 가로 넘침', p['k'], p['ow'], '바탕 같은 창 %s' % d.get('ow')))
    return new


GATES = [('b1', 'B1 민소 「1.3.1.{법정}직사토(보독관)」 「기출 3」 → 새 팝업 하나 · 제목 「🔗 기출 — …」 · 「기출 — 3건」 · 13-50-2 → 24-61-2 → 17-54-4 · 노트 팝업 0 · 줄 .on', g1, 'fix'),
         ('b2', 'B2 전수 — 네 법 목차노트 × 줄 × 갈래 넷 · 칩마다 건수 = 칩 수 = 데이터 · 같은 값 두 번 0 · 차례 = 노트 줄 차례(바탕은 앞 6 칩만)', g2, 'fix'),
         ('b3', 'B3 같은 칩 다시 = 닫힘 · 다른 칩 = 새 창(키 다름)', g3, 'fix'),
         ('b4', 'B4 줄 이름 누름 → 노트 팝업(note|민소|<노트>|) · 목록 창 0 = 바탕과 같음', g4, 'keep'),
         ('b5', 'B5 목록 창 줄 누름 → 카드 「🧾 기출 · 민기출 13-50-2-사물관할」 = 노트 팝업 블록 칩 길로 연 같은 카드', g5, 'fix'),
         ('b6', 'B6 자리 — PC 1440 · 아이패드 834 = 목록 창 오른쪽(노트 팝업 규칙 mokPlace) · 화면 안 · 폰 390 = 위 30% / 아래 70% · 겹침 0', g6, 'fix'),
         ('b7', 'B7 터치(아이패드 834 · 폰 390) — 칩 탭 = 목록 창 · 틈·위·아래 탭 = 칩 또는 줄 하나 · 누름 칸 겹침 0 · 줄 밖 0 · 값', g7, 'fix'),
         ('b8', 'B8 노트 팝업 블록 칩 「기출 2」(^271d19) → 같은 창(제목 끝 #^271d19 · 2건) = 바탕과 같음', g8, 'keep'),
         ('b12', 'B12 긴 노트 이름(민소 7.7.1 · 40자 · 상표 5.9. · 44자) × PC 1440 · 폰 390 — 목차 칩 「기출」 창과 노트 팝업 블록 칩 「기출 N」 창이 같이 뜸(목차 → 블록 · 블록 → 목차) · 같은 칩 다시 = 그 창만 닫힘', g12, 'fix'),
         ('b13', 'B13 같은 긴 노트의 블록 칩 둘(다른 ^id) → 창 둘 × PC 1440 · 폰 390', g13, 'fix'),
         ('b11', 'B11 화면 훑기 — 목차노트 창(네 법) · 목록 창 · 노트 팝업 × PC · 아이패드 · 폰 — 새로 생긴 쪽 넘침 · 창 화면 밖 · 창 안 가로 넘침 0', g11, 'keep')]


def main():
    APPS['NEW'] = app_src(NEWF)
    if QJ.GATE:
        APPS['BASE'] = app_src(BASEF)   # regress 는 바탕을 풀지 않는다(git:show-app 0)
    EXP.update(cite_all())
    base_rev = BASEF
    if QJ.GATE:
        try:
            base_rev = git('rev-parse', '--short', BASEF).decode().strip() or BASEF
        except Exception:
            pass
    else:
        base_rev = '(regress — 바탕 안 띄움)'
    t0 = time.time(); TIMES = []
    print('INFO | 기대 칩 수 | %s' % json.dumps({sh: sum(1 for f in EXP[sh] for k in KINDS if EXP[sh][f][k]) for sh in EXP}, ensure_ascii=False), flush=True)
    print('INFO | 기대 N1 기출 | %s' % json.dumps(EXP['민소'][N1]['기출'], ensure_ascii=False), flush=True)
    with sync_playwright() as pw:
        for eng in ENGS:
            br = getattr(pw, eng).launch()
            try:
                for g, name, fn, kind in GATES:
                    if ONLY and g not in ONLY:
                        continue
                    if QJ.SMOKE and not (QJ.want(g, smoke=(g in SMOKE_G)) and (eng != 'webkit' or g in TOUCH_G)):
                        continue
                    ts = time.time(); res = {}
                    for who in (('NEW',) if QJ.REGRESS else ('NEW', 'BASE')):
                        try:
                            if QJ.REGRESS:
                                with QJ.stage('%s·%s' % (g, eng)):
                                    res[who] = fn(br, eng, who)
                            else:
                                res[who] = fn(br, eng, who)
                        except Exception as e:
                            res[who] = (False, 'ERR ' + repr(e)[:400])
                    if QJ.REGRESS:
                        res['BASE'] = (None, '(regress — 바탕 안 띄움)')
                    if g == 'b11' and isinstance(res['NEW'][1], dict) and (QJ.REGRESS or isinstance(res['BASE'][1], dict)):
                        if QJ.REGRESS:   # 기준 — 바탕 판 값 대신 저장된 기준 스냅샷(앞 인도판의 같은 칸 값 · 없으면 지금 값 자신 = 첫 기록) · 아래 원본 줄이 BASE[1] 을 바탕 값으로 읽는다
                            bcid = 'b11@%s' % eng
                            res['BASE'] = (None, QJ.base(bcid, res['NEW'][1]))
                        new = sw_cmp(res['NEW'][1], res['BASE'][1])
                        res['NEW'] = (not new, {'새로 생긴 것': new[:20], '바탕 같은 창(popNoteList 에 같은 카드)': {k: v for k, v in res['BASE'][1].items() if '같은 창 직접' in k},
                                                '표': res['NEW'][1]})
                        res['BASE'] = (True, '기준')
                        if QJ.REGRESS:
                            res['BASE'] = (None, '기준 — ' + QJ.base_note(bcid))
                    if QJ.REGRESS and g in NOTES:
                        res['BASE'] = (None, '%s · 바탕 안 띄움' % NOTES.pop(g))
                    R(g, eng, name + ('  [바탕 = 기준]' if kind == 'keep' else ''), res['NEW'][0], res['BASE'][0], {'NEW': res['NEW'][1], 'BASE': res['BASE'][1]})
                    TIMES.append((g, round(time.time() - ts)))
            finally:
                if QJ.REGRESS:
                    RIG.shut()
                br.close()
    npass = sum(1 for r in ROWS if r[3]); nfail = sum(1 for r in ROWS if not r[3])
    vac = [r for r in ROWS if r[4] is True and '기준' not in r[2]]
    if QJ.GATE:
        print('\n== PASS %d · FAIL %d · 헛잣대(바탕도 PASS · 기준 칸 밖) %d · %.0f초 · 단계 초 %s' % (npass, nfail, len(vac), time.time() - t0, TIMES))
    else:
        print('\n== PASS %d · FAIL %d · regress(바탕 안 띄움 · 헛잣대 안 잼) · %.0f초 · 단계 초 %s' % (npass, nfail, time.time() - t0, TIMES))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · jo_mokchip · NEW %s · 바탕 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), os.path.basename(NEWF), base_rev, ','.join(ENGS)))
        for g, eng, n, okn, okb, v in ROWS:
            f.write('%s | 바탕 %s | %s · %s · %s | %s\n' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, eng, n,
                    (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str))[:20000]))
        if QJ.GATE:
            f.write('== PASS %d · FAIL %d · 헛잣대 %d · 단계 초 %s\n' % (npass, nfail, len(vac), TIMES))
        else:
            f.write('== PASS %d · FAIL %d · regress(헛잣대 안 잼) · 단계 초 %s\n' % (npass, nfail, TIMES))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
