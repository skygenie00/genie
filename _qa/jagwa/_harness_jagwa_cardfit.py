# -*- coding: utf-8 -*-
r"""_task_jagwa_cardfit_1011 §5 관문 [클라우드] — 자과 합친 판: 지학·생물 문항 창 물리 맞춤(A) · 필기 도구 ⋯(B) · 같은 근거(C) · 암기카드 창 1/3(D) · 서랍 안 접힘(E) · add1 근거 들여쓰기(F)

  python _harness_jagwa_cardfit.py [--new <앱>] [--base <판 = 92f0215>] [--pre <합치기 전 앱(패치 72 만) — B 만 더 돌림>]
                                   [--eng chromium,webkit] [--group A,B,C,D,E,F] [--only A1,T4,C3,…] [--spd <studyplandata>] [--notes <notes>] [--vendor <cdnjs 사본>] [--res <결과>]

  NEW = genie 작업트리 jagwa/index.html · BASE = 바탕 main 92f0215(헛잣대 — 새 칸은 바탕 FAIL · 「바탕도 같음」 칸(SAME)은 바탕 값으로 가름)
  엔진 = Chromium · WebKit(새 판 · 바탕 둘 다) · PC 1100×800 마우스(펜 = Chromium CDP pointerType 'pen' · WebKit = 합성 pen 포인터) · 폰 384×740 hasTouch ·
         아이패드 820×1180 hasTouch · 600×900 hasTouch · 원격 = 가짜(메모리 · PUT 밖으로 안 나감)
  시험 글 · 획 · 기록 · 근거 · 연결 = 하네스가 지어 넣음(기록 · 근거 없는 문항만 골라 씀) · 실제 카드 글 · 근거 글은 출력에 안 옮김(셈 · md5 앞 8 자 · D11)
  무리:
    A 지학 · 생물(카드 층) — 시안 v15 점검 칸(A1~A19 · §4 물리 데이터 글 0 = A19)
    B 물리 · 지학 · 생물 — 필기 도구 ⋯ T1~T11 · TC1(카드 층 교재 창 도구 = 바탕) · TR1 · TR2(카드 층 빈 회독 줄 · §3-1) · --pre = 합치기 전(§3-2) 같은 칸
    C 물리 · 지학 · 생물 — 같은 근거 C1~C7
    D 물리 · 지학 · 생물 × PC · 폰 — 🃏 암기카드 창 처음 = 화면 1/3
    E 물리 · 지학 × 폭 384 · 600 · 820 · 1100 — 서랍 줄 · 검색 줄 · O△X 눌러도 서랍 안 접힘 · 손잡이로는 접힘
    F 물리 · 지학 · 생물 — add1 근거 글 들여쓰기 F1~F7(줄 앞 빈칸 · 줄 안 여러 빈칸 · 폰 꺾임 매단 들임) · 헛잣대 = --pre 앱(패치 72 만)
  모드 — gate = 바탕 띄움 · regress · smoke = 새 판만(SAME 칸 = 기준 스냅샷 · smoke = B T1~T3 · A1)
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
BASE = ARG('--base', '92f0215')
PRE = ARG('--pre')
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
GROUPS = [x.strip().upper() for x in (ARG('--group', 'A,B,C,D,E,F') or '').split(',') if x.strip()]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
TMPD = os.path.join(tempfile.gettempdir(), 'h_jagwa_cardfit')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_jagwa_cardfit_result.txt'))
SPD = ARG('--spd', _roots.spd())
NOTES = ARG('--notes', os.path.join(os.path.dirname(_roots.spd()), 'notes'))
VENDOR = ARG('--vendor', os.path.join(TMPD, 'vendor'))
JG.conf(VENDOR_PP=VENDOR, SPD_PP=SPD, NOTES=NOTES, SHOTS=os.path.join(TMPD, 'shots'))
JG.OKHOST = tuple(JG.OKHOST) + ('blob:', 'data:')   # WebKit 은 blob: · data: 그림 요청도 route 를 지난다(Chromium 은 안 지남) — 공용 route_handler 가 막으면 카드 그림이 안 풀려(naturalWidth 0) 카드가 짧아짐(빈 띠 · 굴릴 틈 0) · 바깥 망은 그대로 막음(penfinger P2 OKNET 과 같은 뜻)
GATE = QC.GATE
if GATE:
    QC.sub('git:show-app')
SRC = {'NEW': JG.app_src(NEWF)}
if GATE:
    SRC['BASE'] = JG.app_src(BASE)
if PRE:
    SRC['PRE'] = JG.app_src(PRE)
PC, PH = (1100, 800), (384, 740)
RES = []
SMOKE_CELLS = {'T1', 'T2', 'T3', 'A1'}


def want(c):
    return (not ONLY or c.upper() in ONLY) and (not QC.SMOKE or c in SMOKE_CELLS)


def _s(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


def R(g, name, new, base=None, d='', yard=True):
    RES.append(dict(g=g, name=name, new=new, base=base, yard=yard, d=d))
    tag = 'INFO' if new is None else ('PASS' if new else 'FAIL')
    yb = '' if base is None else (' · 바탕 ' + (('PASS(바탕도 같음)' if not yard else 'PASS') if base else ('FAIL' if yard else 'FAIL(바탕도 같아야 할 칸)')))
    print('%s | %s · %s%s | %s' % (tag, g, name, yb, _s(d)[:700]), flush=True)



# ══ 무리 A ══════════════════════════════════════════════════════════════════════════════
# 관문 A — 지학 · 생물(카드 층) 문항 창 물리 맞춤 · 시안 v15 점검 칸 — _harness_jagwa_cardfit.py 에 들어갈 몫(개발 사본)
import hashlib, json

PICKN_JS = r"""async ([n,skip])=>{const out=[];for(const r of DATA){const no=r[F.NO];if(typeof isC==='function'&&isC(r))continue;if((skip||[]).indexOf(no)>=0)continue;if(hist(no).length)continue;
  const u=String(qk(no));if((typeof ggOf==='function'?ggOf(u):[]).length)continue;if(typeof QT!=='undefined'&&QT[qk(no)])continue;out.push(no);if(out.length>=n)break}return out}"""
# TD(물리 기본 유형 표) 열쇠인 번호 가운데 카드 층 문항이 있고 기록 · 근거 · 그 과목 유형이 없는 것
PICKTD_JS = r"""(skip)=>{if(typeof TD==='undefined')return null;for(const k of Object.keys(TD)){const no=+k;if((skip||[]).indexOf(no)>=0)continue;const r=rec(no);if(!r||(typeof isC==='function'&&isC(r)))continue;
  if(hist(no).length||(typeof QT!=='undefined'&&QT[qk(no)]))continue;if((TD[k]||[]).length)return no}return null}"""
A_OPEN_JS = r"""async (no)=>{await openView(no);for(let i=0;i<60;i++){await new Promise(r=>setTimeout(r,100));if(!HASBOOK||QUID===String(qk(no)))break}
  try{setTool('view')}catch(e){}await new Promise(r=>setTimeout(r,500));return VNO}"""
# 지어낸 기록(O · 40 초) · 연결(카드 층 열쇠 = uid) · 근거(트리거 칸 지어낸 글)
GGPUT = r"""const ggPut=async(no,t)=>{const u=String(qk(no));if(window.G3&&G3.push)return G3.push(u,'t',{t});   /* 바탕 카드 층 = gg3 안 섬 → 근거 목록에 바로(같은 꼴) */
  const list=ggOf(u).slice();list.push({k:(typeof ggNewKey==='function'?ggNewKey('g_'):'g_'+Date.now().toString(36)),i:list.length+1,t,ts:Date.now(),cs:[],f:'t'});await ggSaveList(u,list);try{ggRepaint(u)}catch(e){}};"""
A_SEED_JS = r"""async (o)=>{""" + GGPUT + r"""const t0=Date.now()-3600000;for(const no of o.rec)ST[qk(no)]={h:[{m:'O',t:t0,s:40}]};await saveST();
  for(const [a,b] of o.lk){const ka=HASBOOK?String(qk(a)):a,kb=HASBOOK?String(qk(b)):b;LK[ka]=[kb]}
  for(const [no,t] of o.gg)await ggPut(no,t)
  try{navBuild()}catch(e){}try{draw()}catch(e){}return true}"""
RECT_JS = r"""(q)=>{const e=typeof q==='string'?document.querySelector(q):q;if(!e)return null;const r=e.getBoundingClientRect();const cs=getComputedStyle(e);
  return {l:Math.round(r.left),t:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),b:Math.round(r.bottom),vis:cs.display!=='none'&&cs.visibility!=='hidden'&&r.width>0&&r.height>0,cx:r.left+r.width/2,cy:r.top+r.height/2}}"""
VIEW_JS = r"""()=>{const v=document.getElementById('view');const r=v.getBoundingClientRect();return {l:Math.round(r.left),t:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),ih:innerHeight,iw:innerWidth,VNO}}"""
PINS_JS = r"""()=>[...document.querySelectorAll('.vpin')].filter(b=>b.isConnected).map(b=>{const p=b.querySelector('.panel')||b;const r=p.getBoundingClientRect();const h=b.querySelector('.vpcard');
  return {no:+b.dataset.no,cmp:b.dataset.cmp,l:Math.round(r.left),t:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),card:!!(h&&h.shadowRoot&&h.shadowRoot.querySelector('#card')),img:b.querySelectorAll('.vpb img').length}})"""
A_ROW_JS = r"""([no,sel])=>{const row=document.querySelector('#ndList .ndrow[data-no="'+no+'"]')||document.querySelector('.ndrow[data-no="'+no+'"]');if(!row)return null;try{row.scrollIntoView({block:'center'})}catch(e){}
  const e=sel?row.querySelector(sel):row;if(!e)return {row:true,el:false};const r=e.getBoundingClientRect();const t=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);
  return {row:true,el:true,cx:r.left+r.width/2,cy:r.top+r.height/2,hit:!!(t&&(t===e||e.contains(t))),top:t?(t.id||t.className||t.tagName):null}}"""
CLOSEALL_JS = r"""()=>{document.querySelectorAll('.vpin,.sheet.twin,#gguw,#rlPop,#nsPop,#sh-ans').forEach(x=>{try{x.__close?x.__close():x.remove()}catch(e){x.remove()}});try{g3PopClose()}catch(e){}
  const mc=document.querySelector('.sheet.mcwin');if(mc){const x=mc.querySelector('.shx,.mcx,[data-x]');x?x.click():mc.remove()}return true}"""
HEAD_JS = r"""()=>{const v=document.querySelector('#view .vtop');const t1=document.getElementById('vT1'),t2=document.querySelector('#view .vtop .t2');const vis=e=>!!e&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0;
  const lh=t1?parseFloat(getComputedStyle(t1).lineHeight)||parseFloat(getComputedStyle(t1).fontSize)*1.3:0;
  const fold=document.getElementById('g3Fold');const kids={};if(v)[...v.children].forEach(e=>{if(e.id&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0)kids[e.id]=Math.round(e.getBoundingClientRect().height*10)/10});
  return {vtopH:v?Math.round(v.getBoundingClientRect().height):null,t1H:t1?Math.round(t1.getBoundingClientRect().height):null,t1lines:t1&&lh?Math.round(t1.getBoundingClientRect().height/lh):null,t2:vis(t2),fold:vis(fold),kids}}"""
BOT_JS = r"""()=>{const b=document.querySelector('#view .vbot');if(!b)return null;const vis=e=>getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().width>0;
  const ks=[...b.querySelectorAll('button,.tl')].filter(vis);const ids=ks.map(e=>e.id||'');const sz=['mO','mQ','mX','mP'].map(id=>{const e=document.getElementById(id);if(!e||!vis(e))return null;const r=e.getBoundingClientRect(),cs=getComputedStyle(e);
    return [Math.round(r.width),Math.round(r.height),cs.fontSize,cs.fontWeight]});
  const a=document.getElementById('tAns'),l=document.getElementById('tLink');
  return {first:ids[0]||null,last:ids[ids.length-1]||null,ans:a&&vis(a)?a.textContent.trim():null,link:l&&vis(l)?l.textContent.trim():null,ord:['tAns','mO','mQ','mX','mP'].map(x=>ids.indexOf(x)),linkAt:ids.indexOf('tLink'),n:ids.length,sz,
    vrow:(()=>{const e=document.querySelector('#card .vrow');return !!e&&vis(e)})(),cdet:(()=>{const e=document.querySelector('#card #cDetBtn');return !!e&&vis(e)})()}}"""
GG_JS = r"""()=>{const c=document.getElementById('card');if(!c)return null;const vis=e=>getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0;
  const fb=[...c.querySelectorAll('.g3fb')].filter(e=>getComputedStyle(e).visibility!=='hidden'&&vis(e));const lists=[...c.querySelectorAll('.g3f .g3list')];
  const lab=[...c.querySelectorAll('.g3box .ggrow .lab,.ggrow .lab')].filter(vis).length;const ph=[...c.querySelectorAll('.g3f textarea')].map(t=>t.placeholder||'');
  return {fold:c.classList.contains('g3fold'),fb:fb.map(e=>e.textContent),fbAll:c.querySelectorAll('.g3fb').length,listVis:lists.filter(vis).length,lists:lists.length,items:c.querySelectorAll('.g3f .g3list .g3it').length,lab,ph:ph.filter(Boolean).length,ta:ph.length}}"""
POP_JS = r"""()=>{const P=document.getElementById('g3Pop');if(!P)return null;const r=P.getBoundingClientRect(),f=P.querySelector('.g3lk.f'),b=P.querySelector('.g3lk.b');
  return {h:Math.round(r.height),ih:innerHeight,f:f?f.textContent.trim():null,b:b?b.textContent.trim():null,fat:f?{cx:f.getBoundingClientRect().left+f.getBoundingClientRect().width/2,cy:f.getBoundingClientRect().top+f.getBoundingClientRect().height/2}:null,
    rows:[...P.querySelectorAll('.g3lkr')].map(x=>{const q=x.getBoundingClientRect();return {no:+x.dataset.no,cx:q.left+q.width/2,cy:q.top+q.height/2}}),top:!!P.querySelector('.g3ptop'),txt:P.innerText}}"""
SH_JS = r"""(q)=>{const s=document.querySelector(q);if(!s)return null;const p=s.querySelector('.panel')||s;const r=p.getBoundingClientRect();const cs=getComputedStyle(p);
  return {h:Math.round(r.height),t:Math.round(r.top),b:Math.round(r.bottom),ih:innerHeight,fs:cs.fontSize,h2:(()=>{const h=s.querySelector('h2');return h?getComputedStyle(h).fontSize:null})(),txt:p.innerText}}"""
# §4 — 물리 데이터 글(물리 유형 TD · 절 · 장 이름 · 개념 블록 이름)이 열린 창 글에 있나 — 그 과목 DATA 에도 있는 글은 셈 밖(카드 글에 같은 낱말이 원래 있음)
PHYS_JS = r"""(no)=>{const S=new Set();try{(TD[no]||[]).forEach(t=>S.add(String(t)))}catch(e){}
  try{(UNITS.sec||[]).forEach(s=>{if(s.t)S.add(String(s.t))});Object.values(UNITS.ch||{}).forEach(t=>S.add(String(t)))}catch(e){}
  try{(THEORY.sec||[]).forEach(s=>{if(s.t)S.add(String(s.t))})}catch(e){}
  try{Object.values(CB||{}).forEach(c=>{if(c&&c.n)S.add(String(c.n))})}catch(e){}
  const D=JSON.stringify(DATA);const td=new Set((()=>{try{return TD[no]||[]}catch(e){return []}})().map(String));
  const words=[...S].filter(t=>t.length>=2&&(td.has(t)||!D.includes(t)));
  const parts={view:'#view',drawer:'#navdr',pop:'#g3Pop',use:'#gguw'};const out={};
  for(const k in parts){const e=document.querySelector(parts[k]);const tx=e?e.innerText:'';out[k]={open:!!e,hit:words.filter(w=>tx.includes(w)).length}}
  out.qt=[...document.querySelectorAll('#card .tag.qt')].filter(x=>td.has(x.textContent.trim())).length;
  out.typeOf=(()=>{try{return (typeOf(no)||[]).filter(t=>td.has(String(t))).length}catch(e){return -1}})();out.words=words.length;return out}"""
UL_JS = r"""(no)=>{const row=document.querySelector('.ndrow[data-no="'+no+'"]');if(!row)return null;const ox=row.querySelector('.ndox');const m=row.querySelector('.ndox .ndm[data-s]')||row.querySelector('.ndm[data-s]');if(!m)return {ox:!!ox,g3has:!!(ox&&ox.classList.contains('g3has')),m:false};
  const cs=getComputedStyle(m);const tn=[...m.childNodes].find(n=>n.nodeType===3&&n.textContent.trim());let gap=null,ul=null,tt=null;
  if(tn){const rg=document.createRange();rg.selectNodeContents(tn);const rr=rg.getBoundingClientRect();const cv=document.createElement('canvas').getContext('2d');cv.font=cs.fontWeight+' '+cs.fontSize+' '+cs.fontFamily;
    const mt=cv.measureText(tn.textContent);const desc=mt.fontBoundingBoxDescent||parseFloat(cs.fontSize)*0.2;const base=rr.bottom-desc;
    const off=cs.textUnderlineOffset==='auto'?Math.max(1,parseFloat(cs.fontSize)*0.1):parseFloat(cs.textUnderlineOffset);const th=cs.textDecorationThickness==='auto'||cs.textDecorationThickness==='from-font'?1:parseFloat(cs.textDecorationThickness);
    ul=base+off+th;const mr=m.getBoundingClientRect();tt=mr.bottom-7;gap=+(tt-ul).toFixed(2)}
  return {ox:!!ox,g3has:!!(ox&&ox.classList.contains('g3has')),m:true,deco:cs.textDecorationLine+' '+cs.textDecorationStyle,off:cs.textUnderlineOffset,gap}}"""


def md5(s):
    return hashlib.md5((s or '').encode('utf-8')).hexdigest()[:8]


def click_el(p, q, touch=False, wait=500):
    e = p.ev(RECT_JS, q)
    if not e or not e['vis']:
        return False
    (p.tap if touch else p.click)(e['cx'], e['cy'], wait)
    return True


def press_row(p, no, sel, touch=False, wait=1500):
    """서랍 줄의 그 칸(번호 .ndno · O△X .ndox) — 진짜 누름 · 맨 위가 그 칸이 아니면(폰 = 문항 창이 서랍 위) el.click() 으로 넘기고 그 길을 적음"""
    at = p.ev(A_ROW_JS, [no, sel])
    if not at or not at.get('el'):
        return 'no-row' if not at else 'no-el'
    if at['hit']:
        (p.tap if touch else p.click)(at['cx'], at['cy'], wait)
        return 'real'
    p.ev("([no,sel])=>{const e=document.querySelector('.ndrow[data-no=\"'+no+'\"] '+sel);if(e)e.click();return !!e}", [no, sel]); p.wait(wait)
    return 'click()'


def flow_A(p, eng, subj, ph=None):
    """p = PC 1100×800 마우스 쪽 · ph = 폰 384×740 손가락 쪽(A4) — 둘 다 같은 과목"""
    o = {}
    ns = p.ev(PICKN_JS, [7, []])
    if not ns or len(ns) < 7:
        o['하네스 오류'] = '고를 문항 모자람 %s' % ns
        return o
    X, Y, Z, T, S, W, V = ns
    TDN = p.ev(PICKTD_JS, ns)
    o['문항'] = dict(X=X, Y=Y, Z=Z, T=T, S=S, W=W, V=V, TD=TDN)
    p.ev(A_OPEN_JS, X)
    p.ev(A_SEED_JS, {'rec': [X, TDN] if TDN else [X], 'lk': [[X, T], [S, X]], 'gg': [[X, '시험근거 가나다 첫째'], [W, '시험근거 바다솔 공통말']]})
    p.ev(A_OPEN_JS, X); p.wait(500)
    def safe(f, k):
        try:
            f()
        except Exception as ex:   # 바탕에 그 동작이 없으면 그 칸만 FAIL(흐름은 이어 감)
            o.setdefault('오류 칸', {})[k] = str(ex).split('\n')[0][:160]

    def _s0():
        nonlocal_o = o
        # A11 · A15 머리 · A9 아랫줄 · A16 · A17 근거 줄
        o['머리'] = p.ev(HEAD_JS)
        o['아랫줄'] = p.ev(BOT_JS)
        o['근거 줄'] = p.ev(GG_JS)
    safe(_s0, 'A11')
    def _s1():
        nonlocal_o = o
        # A12 서랍 점선 틈
        o['점선'] = p.ev(UL_JS, X)
    safe(_s1, 'A12')
    def _s2():
        nonlocal_o = o
        # A5 서랍 🔍 — 상/중/하 없음 · 그 과목 낱말 찾힘
        word = '지구' if subj == 'earth' else '세포'
        s0 = click_el(p, '#ndHead .ndsrch') or click_el(p, '.pwchip.ndsrch')
        p.wait(300)
        n5 = None
        if p.ev("!!document.querySelector('#nsPop .rlq')"):
            p.ev("()=>document.querySelector('#nsPop .rlq').focus()")
            p.pg.keyboard.type(word, delay=30); p.wait(700)
            n5 = p.ev("(()=>{const c=document.querySelector('#nsPop .nsc');return {rows:document.querySelectorAll('#nsPop .nsr').length,cnt:c?c.textContent:''}})()")
        o['A5'] = {'칩': s0, '창': p.ev("!!document.getElementById('nsPop')"), '찾음': n5, '상중하': p.ev("!!document.getElementById('ndLv')||!!document.getElementById('ndLvPop')")}
        p.ev(CLOSEALL_JS); p.wait(300)
    safe(_s2, 'A5')
    def _s3():
        nonlocal_o = o
        # A6 서랍 O△X → 근거 창 · 🔗1 ↩1 · 🔗 → 목록 → 줄
        o['A6 누름'] = press_row(p, X, '.ndox', wait=900)
        g6 = p.ev(POP_JS)
        rows, after = None, None
        if g6 and g6.get('fat'):
            p.click(g6['fat']['cx'], g6['fat']['cy'], 500)
            g6b = p.ev(POP_JS) or {}
            rows = [r['no'] for r in g6b.get('rows', [])]
            if g6b.get('rows'):
                r0 = g6b['rows'][0]
                p.click(r0['cx'], r0['cy'], 1500)
                after = {'비교 창': [x['no'] for x in p.ev(PINS_JS)], '팝업': p.ev("[...document.querySelectorAll('.sheet.twin')].filter(x=>x.isConnected).length"), 'g3Pop': p.ev("!!document.getElementById('g3Pop')")}
        o['A6'] = {'창': {k: v for k, v in (g6 or {}).items() if k not in ('txt', 'rows', 'fat')} if g6 else None, '목록': rows, '줄 뒤': after, 'T': T}
        p.ev(CLOSEALL_JS); p.wait(300)
    safe(_s3, 'A6')
    def _s4():
        nonlocal_o = o
        # A7 🔗(아랫줄) → 작은 창
        o['A7'] = {'누름': click_el(p, '#tLink', wait=600), '창': p.ev(RECT_JS, '#rlPop'), 'ih': p.ev("innerHeight")}
        p.ev(CLOSEALL_JS); p.wait(300)
    safe(_s4, 'A7')
    def _s5():
        nonlocal_o = o
        # A10 정답 → 곁창 · 다시 → 닫힘 · 카드로 되돌아감
        a10 = click_el(p, '#tAns', wait=700)
        s10 = p.ev(SH_JS, '#sh-ans')
        if s10:
            s10 = {k: v for k, v in s10.items() if k != 'txt'}
        a10b = click_el(p, '#tAns', wait=600)
        o['A10'] = {'누름': a10, '곁창': s10, '다시': a10b, '닫힘': not p.ev("!!document.getElementById('sh-ans')"), '카드 정답 칸': p.ev("!!document.querySelector('#cDet .sol')")}
    safe(_s5, 'A10')
    def _s6():
        nonlocal_o = o
        # A8 서브노트 처음 1/2 · $ · <span 글자 0
        a8 = click_el(p, '#cSub', wait=1500) or click_el(p, '#tSub', wait=1500)
        s8 = p.ev(r"""()=>{const s=document.querySelector('#sub .panel,#snw .panel');if(!s)return null;const r=s.getBoundingClientRect();const tx=s.innerText||'';
          return {h:Math.round(r.height),ih:innerHeight,dollar:(tx.match(/\$/g)||[]).length,span:(tx.match(/<span/g)||[]).length,md5:''}}""")
        o['A8'] = {'누름': a8, '창': s8}
        p.ev("(()=>{const s=document.querySelector('#sub,#snw');if(s){const x=s.querySelector('.shx,.x,[data-close]');if(x)x.click();else s.classList.add('hide')}return 1})()"); p.wait(400)
        p.ev(CLOSEALL_JS)
    safe(_s6, 'A8')
    def _s7():
        nonlocal_o = o
        # A13 🃏 연 채 근거 칸 누름 · 적고 Enter
        p.ev(A_OPEN_JS, X); p.wait(300)
        n13a = p.ev("(()=>ggOf(String(qk(VNO))).length)()")
        a13 = click_el(p, '#tCard', wait=1200)
        mc = p.ev("!!document.querySelector('.sheet.mcwin')")
        ta = p.ev(r"""()=>{const t=[...document.querySelectorAll('#card .g3f textarea')][0];if(!t)return null;try{t.scrollIntoView({block:'center'})}catch(e){}const r=t.getBoundingClientRect();const e=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);
          return {cx:r.left+r.width/2,cy:r.top+r.height/2,top:e?(e===t?'textarea':(e.className||e.tagName)):null}}""")
        foc = None
        if ta:
            p.click(ta['cx'], ta['cy'], 300)
            foc = p.ev("(()=>{const a=document.activeElement;return a?(a.tagName+'.'+(a.closest&&a.closest('.g3f')?'g3f':'')):null})()")
            if foc and foc.startswith('TEXTAREA'):
                p.pg.keyboard.type('시험근거 하늘결 넷째', delay=20); p.pg.keyboard.press('Enter'); p.wait(700)
        n13b = p.ev("(()=>ggOf(String(qk(VNO))).length)()")
        o['A13'] = {'🃏': a13, '창': mc, '근거 칸 맨 위': (ta or {}).get('top'), '포커스': foc, '근거 수': [n13a, n13b]}
        p.ev(CLOSEALL_JS); p.wait(300)
    safe(_s7, 'A13')
    def _s8():
        nonlocal_o = o
        # A18 근거 찾기 — uid 칩 · 단원명 · 칩 → 비교 창 · 근거로 안 들어감
        p.ev(A_OPEN_JS, V); p.wait(300)
        n18a = p.ev("(()=>ggOf(String(qk(VNO))).length)()")
        ta = p.ev(r"""()=>{const t=[...document.querySelectorAll('#card .g3f textarea')][0];if(!t)return null;try{t.scrollIntoView({block:'center'})}catch(e){}const r=t.getBoundingClientRect();return {cx:r.left+r.width/2,cy:r.top+r.height/2}}""")
        chips, a18 = None, None
        if ta:
            p.click(ta['cx'], ta['cy'], 300)
            p.pg.keyboard.type('바다솔', delay=30); p.wait(900)
            chips = p.ev(r"""()=>[...document.querySelectorAll('.g3s .g3so .g3ttl')].map(c=>{const r=c.getBoundingClientRect();return {u:c.dataset.gguugo,cd:!!c.querySelector('.cd'),un:!!(c.querySelector('.un')&&c.querySelector('.un').textContent.trim()),cx:r.left+r.width/2,cy:r.top+r.height/2,vis:r.width>0}})""")
            if chips:
                c = chips[0]
                p.click(c['cx'], c['cy'], 1500)
                a18 = {'비교 창': [x['no'] for x in p.ev(PINS_JS)], '근거 수 뒤': p.ev("(()=>ggOf(String(qk(VNO))).length)()"), 'VNO': p.ev("VNO")}
        o['A18'] = {'근거 수 전': n18a, '칩': [{k: v for k, v in c.items() if k in ('cd', 'un', 'vis')} for c in (chips or [])], '칩 uid = W': bool(chips) and chips[0]['u'] == p.ev("(no)=>String(qk(no))", W), '누른 뒤': a18, 'W': W}
        p.ev(CLOSEALL_JS); p.wait(300)
    safe(_s8, 'A18')
    def _s9():
        nonlocal_o = o
        # A1 서랍 번호 → 비교 창(X 를 본창으로 다시 엶)
        p.ev(CLOSEALL_JS); p.ev(A_OPEN_JS, X); p.wait(400)
        v0 = p.ev(VIEW_JS)
        o['A1 누름'] = press_row(p, Y, '.ndno')
        p.wait(800)
        v1 = p.ev(VIEW_JS); pins1 = p.ev(PINS_JS)
        o['A1'] = {'본창 전': v0, '본창 뒤': v1, '비교 창': pins1}
    safe(_s9, 'A1')
    def _s10():
        nonlocal_o = o
        # A2 번호 하나 더
        o['A2 누름'] = press_row(p, Z, '.ndno'); p.wait(800)
        o['A2'] = {'비교 창': p.ev(PINS_JS)}
    safe(_s10, 'A2')
    def _s11():
        nonlocal_o = o
        # A3 비교 창(Y) 누름 → 그 자리 산 창
        pin = [x for x in (o['A2']['비교 창'] or []) if x['no'] == Z] or [x for x in (o['A2']['비교 창'] or []) if x['no'] == Y]   # 맨 앞 비교 창(나중에 연 Z · 비껴 쌓여 Y 를 덮음)
        if pin:
            at = p.ev("(no)=>{const b=[...document.querySelectorAll('.vpin')].find(x=>+x.dataset.no===no);if(!b)return null;const r=b.querySelector('.vpb').getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+Math.min(r.height/2,40)}}", pin[0]['no'])
            vb = p.ev(VIEW_JS)
            if at:
                p.click(at['x'], at['y'], 1800)
            o['A3'] = {'누른 창': pin[0], '본창 전': vb, '본창 뒤': p.ev(VIEW_JS), '비교 창 뒤': p.ev(PINS_JS)}
        else:
            o['A3'] = {'누른 창': None}
        p.ev(CLOSEALL_JS); p.wait(300)
        p.ev(A_OPEN_JS, X); p.wait(300)
    safe(_s11, 'A3')
    def _s12():
        nonlocal_o = o
        # A14 · A19 — TD 열쇠 번호(물리 기본 유형이 박힌 번호)의 카드 층 문항: 문항 창 · 서랍 · 근거 창 · 쓰인 문항 창 글
        if TDN:
            p.ev(A_OPEN_JS, TDN); p.wait(400)
            press_row(p, TDN, '.ndox', wait=900)
            try:   # 쓰인 문항 창(#gguw) — 근거 하나 넣고 그 근거의 쓰인 문항 창
                p.ev("async (no)=>{await (window.G3&&G3.push?G3.push(String(qk(no)),'t',{t:'시험근거 들꽃 셋째'}):null);ggUseWin(String(qk(no)),'');return 1}", TDN); p.wait(700)
            except Exception as ex:
                o['gguw 오류'] = str(ex)[:120]
            o['A19'] = p.ev(PHYS_JS, TDN)
            o['A14'] = {'typeOf 물리': (o['A19'] or {}).get('typeOf'), '카드 .tag.qt 물리': (o['A19'] or {}).get('qt'),
                        '서랍 줄 유형 물리': p.ev("(no)=>{const r=document.querySelector('.ndrow[data-no=\"'+no+'\"]');if(!r)return null;const td=new Set((TD[no]||[]).map(String));return [...r.querySelectorAll('.tag,.qt,.ndty')].filter(x=>td.has(x.textContent.trim())).length}", TDN)}
            p.ev(CLOSEALL_JS)
    safe(_s12, 'A14')
    o['오류'] = (p.errs or [])[:4]
    # A4 폰 — 서랍 번호 → 비교 창 위 ≤ 1/3 · 본창 아래 1/2
    if ph is not None:
        try:
            ph.ev(A_OPEN_JS, X); ph.wait(400)
            ph.ev("(()=>{try{ndResFold(false)}catch(e){}return 1})()"); ph.wait(600)
            how = press_row(ph, Y, '.ndno', touch=True, wait=1800)
            o['A4'] = {'누름': how, '본창': ph.ev(VIEW_JS), '비교 창': ph.ev(PINS_JS)}
        except Exception as ex:
            o['A4'] = {'오류': str(ex)[:200]}
    return o


def _A_near(a, b, d=4):
    return a is not None and b is not None and abs(a - b) <= d


def judge_A(o, phys_head=None):
    """o = flow_A 값 · phys_head = 같은 엔진 물리 문항 창 머리 높이(.vtop) — A11 잣대"""
    J = {}
    if not o or o.get('하네스 오류'):
        return {c: (False, (o or {}).get('하네스 오류', '값 없음')) for c in NAMES_A}
    a1 = o.get('A1') or {}
    v0, v1, pins = a1.get('본창 전') or {}, a1.get('본창 뒤') or {}, a1.get('비교 창') or []
    cmp1 = [x for x in pins if x.get('cmp') == '1']
    J['A1'] = (bool(cmp1) and len(pins) == 1 and _A_near(v0.get('t'), v1.get('t'), 2) and _A_near(v0.get('l'), v1.get('l'), 2) and _A_near(v0.get('h'), v1.get('h'), 2)
               and v1.get('h', 9999) <= v1.get('ih', 0) / 2 + 1 and cmp1[0]['h'] <= v1['ih'] / 3 + 1 and cmp1[0]['card'],
               {'누름': o.get('A1 누름'), '본창': [v0.get('l'), v0.get('t'), v0.get('h'), '→', v1.get('l'), v1.get('t'), v1.get('h'), 'ih', v1.get('ih')], '비교 창': [(x['no'], x['cmp'], x['h'], x['card']) for x in pins]})
    p2 = (o.get('A2') or {}).get('비교 창') or []
    J['A2'] = (len(p2) == 2 and _A_near(p2[1]['t'] - p2[0]['t'], 30, 2) and _A_near(p2[1]['l'], p2[0]['l'], 2), {'누름': o.get('A2 누름'), '비교 창': [(x['no'], x['l'], x['t'], x['h']) for x in p2]})
    a3 = o.get('A3') or {}
    pn, vb, va, pa = a3.get('누른 창'), a3.get('본창 전') or {}, a3.get('본창 뒤') or {}, a3.get('비교 창 뒤') or []
    old = [x for x in pa if x['no'] == (o.get('문항') or {}).get('X')]
    J['A3'] = (bool(pn) and va.get('VNO') == pn['no'] and _A_near(va.get('l'), pn['l'], 4) and _A_near(va.get('t'), pn['t'], 4) and bool(old) and _A_near(old[0]['l'], vb.get('l'), 4) and _A_near(old[0]['t'], vb.get('t'), 4),
               {'누른 창': pn and (pn['no'], pn['l'], pn['t']), '본창 뒤': (va.get('VNO'), va.get('l'), va.get('t')), '옛 본창 자리': (vb.get('l'), vb.get('t')), '옛 문항 그림 창': old and (old[0]['l'], old[0]['t'])})
    a4 = o.get('A4') or {}
    vw, p4 = a4.get('본창') or {}, [x for x in (a4.get('비교 창') or []) if x.get('cmp') == '1']
    J['A4'] = (bool(p4) and p4[0]['t'] < vw.get('t', -1) and p4[0]['h'] <= vw.get('ih', 0) / 3 + 1 and vw.get('t', -1) >= p4[0]['t'] + p4[0]['h'] - 1 and vw.get('h', 9999) <= vw.get('ih', 0) / 2 + 1,
               {'누름': a4.get('누름'), '비교 창': p4 and (p4[0]['t'], p4[0]['h']), '본창': (vw.get('t'), vw.get('h'), 'ih', vw.get('ih')), '오류': a4.get('오류')})
    a5 = o.get('A5') or {}
    f5 = a5.get('찾음') or {}
    J['A5'] = (bool(a5.get('창')) and not a5.get('상중하') and (f5.get('rows') or 0) > 0, {'칩': a5.get('칩'), '창': a5.get('창'), '상중하': a5.get('상중하'), '찾은 줄': f5.get('rows'), '건': f5.get('cnt')})
    a6 = o.get('A6') or {}
    w6, af = a6.get('창') or {}, a6.get('줄 뒤') or {}
    J['A6'] = (bool(w6) and w6.get('h', 9999) <= w6.get('ih', 0) / 3 + 1 and w6.get('f') == '🔗1' and w6.get('b') == '↩1' and a6.get('목록') == [a6.get('T')]
               and (a6.get('T') in (af.get('비교 창') or []) or (af.get('팝업') or 0) >= 1),
               {'누름': o.get('A6 누름'), '창 높이': [w6.get('h'), w6.get('ih')], '🔗': w6.get('f'), '↩': w6.get('b'), '목록': a6.get('목록'), '줄 뒤': af})
    a7 = o.get('A7') or {}
    r7 = a7.get('창') or {}
    J['A7'] = (bool(a7.get('누름')) and bool(r7.get('vis')) and r7.get('h', 9999) <= (a7.get('ih') or 0) / 3 + 1, {'누름': a7.get('누름'), '창 높이': [r7.get('h'), a7.get('ih')]})
    a8 = (o.get('A8') or {}).get('창') or {}
    J['A8'] = (bool(a8) and abs(a8.get('h', 0) - a8.get('ih', 0) / 2) <= 3 and a8.get('dollar') == 0 and a8.get('span') == 0, {'누름': (o.get('A8') or {}).get('누름'), '높이': [a8.get('h'), a8.get('ih')], '$': a8.get('dollar'), '<span': a8.get('span')})
    b9 = o.get('아랫줄') or {}
    sz = b9.get('sz') or []
    J['A9'] = (b9.get('first') == 'tAns' and b9.get('ans') == '정답' and b9.get('ord') == [0, 1, 2, 3, 4] and b9.get('last') == 'tLink' and b9.get('link') == '🔗'
               and all(s and s[0] == 24 and s[1] == 21 and s[2] == '12px' and str(s[3]) == '800' for s in sz) and not b9.get('vrow') and not b9.get('cdet'),
               {'처음': b9.get('first'), '끝': b9.get('last'), '정답 O△X P 자리': b9.get('ord'), '크기': sz, '카드 마크 줄': b9.get('vrow'), '카드 정답·해설 ▸': b9.get('cdet')})
    a10 = o.get('A10') or {}
    s10 = a10.get('곁창') or {}
    J['A10'] = (bool(s10) and s10.get('h', 9999) <= s10.get('ih', 0) / 3 + 1 and s10.get('fs') == '12px' and bool(a10.get('닫힘')) and bool(a10.get('카드 정답 칸')),
                {'곁창 높이': [s10.get('h'), s10.get('ih')], '글자': s10.get('fs'), '머리': s10.get('h2'), '다시 누름 닫힘': a10.get('닫힘'), '카드로 되돌아감': a10.get('카드 정답 칸')})
    hd = o.get('머리') or {}
    pk, ek = (phys_head or {}).get('kids') or {}, hd.get('kids') or {}
    common = [k for k in ek if k in pk and k != 'g3Fold']
    diff = {k: [ek[k], pk[k]] for k in common if abs(ek[k] - pk[k]) > 0.5}
    J['A11'] = (hd.get('t1lines') == 1 and not hd.get('t2') and len(common) >= 4 and not diff,
                {'줄': hd.get('t1lines'), '둘째 줄': hd.get('t2'), '같은 칸': len(common), '높이 다른 칸(카드 · 물리)': diff, '머리 높이(카드 · 물리)': [hd.get('vtopH'), (phys_head or {}).get('vtopH')]})
    ul = o.get('점선') or {}
    J['A12'] = (bool(ul.get('m')) and ul.get('gap') is not None and ul['gap'] >= 2, {'점선': ul.get('deco'), 'offset': ul.get('off'), '틈': ul.get('gap'), 'g3has': ul.get('g3has')})
    a13 = o.get('A13') or {}
    nn = a13.get('근거 수') or [None, None]
    J['A13'] = (bool(a13.get('창')) and a13.get('근거 칸 맨 위') == 'textarea' and str(a13.get('포커스') or '').startswith('TEXTAREA') and nn[0] is not None and nn[1] == nn[0] + 1, a13)
    a14 = o.get('A14') or {}
    J['A14'] = (a14.get('typeOf 물리') == 0 and a14.get('카드 .tag.qt 물리') == 0 and not a14.get('서랍 줄 유형 물리'), a14)
    J['A15'] = (not hd.get('fold'), {'#g3Fold': hd.get('fold')})
    gg = o.get('근거 줄') or {}
    J['A16'] = (gg.get('lab') == 0 and gg.get('ph') == 0, {'ㄱ·(1) 칸': gg.get('lab'), '흐린 글자 칸': gg.get('ph'), '적는 칸': gg.get('ta')})
    J['A17'] = (bool(gg.get('fold')) and gg.get('fb') and all(t == '▸' for t in gg['fb']) and gg.get('listVis') == 0 and gg.get('items', 0) >= 1, {'접힘': gg.get('fold'), '▸': gg.get('fb'), '보이는 목록': gg.get('listVis'), '적은 근거': gg.get('items')})
    a18 = o.get('A18') or {}
    pr = a18.get('누른 뒤') or {}
    ch = a18.get('칩') or []
    J['A18'] = (bool(ch) and ch[0].get('cd') and ch[0].get('un') and a18.get('칩 uid = W') and a18.get('W') in (pr.get('비교 창') or []) and pr.get('근거 수 뒤') == a18.get('근거 수 전'),
                {'칩': ch[:2], 'uid = W': a18.get('칩 uid = W'), '비교 창': pr.get('비교 창'), '근거 수': [a18.get('근거 수 전'), pr.get('근거 수 뒤')]})
    a19 = o.get('A19') or {}
    J['A19'] = (bool(a19) and all((a19.get(k) or {}).get('hit', 1) == 0 for k in ('view', 'drawer', 'pop', 'use')) and all((a19.get(k) or {}).get('open') for k in ('view', 'drawer', 'pop', 'use'))
                and a19.get('qt') == 0 and a19.get('typeOf') == 0, a19)
    return J


NAMES_A = {
    'A1': '서랍 번호 → 본창 1/2 그대로 · 비교 창 1(≤ 1/3 · 카드 그림)',
    'A2': '번호 하나 더 → 비교 창 둘 · 30px 비껴 쌓기',
    'A3': '비교 창 누름 → 그 자리 산 창(본창 = 그 자리 · 옛 문항 = 옛 본창 자리 그림)',
    'A4': '폰 384 — 비교 창 위 ≤ 1/3 · 본창 아래 ≤ 1/2',
    'A5': '서랍 🔍 → 상/중/하 없음 · 그 과목 낱말 찾힘',
    'A6': '서랍 O△X → 근거 창 ≤ 1/3 · 🔗1 ↩1 · 🔗 → 목록 → 그 문항',
    'A7': '아랫줄 🔗(✏️ 연결) → 작은 창 ≤ 1/3',
    'A8': '🗒 서브노트 처음 = 화면 1/2 · 날 $ · <span 글자 0',
    'A9': '아랫줄 = 정답 O △ X P … 🔗 · O△X P 24×21 · 12px 800 · 카드 안 마크 줄 · 정답·해설 ▸ 숨김',
    'A10': '정답 → 곁창 ≤ 1/3 · 12px · 다시 누름 = 닫힘 · 카드로 되돌아감',
    'A11': '창 머리 한 줄 · 머리 칸 높이 = 물리 문항 창 머리 칸(#g3Fold 는 카드 층 숨김이라 뺌)',
    'A12': '서랍 근거 점선 아래 ≥ 2px 틈(걸린 시간 글자)',
    'A13': '🃏 연 채 근거 칸 누름 = 근거 칸 · 적고 Enter → 근거 +1',
    'A14': '유형 = 그 과목 기록만(물리 TD 유형 0)',
    'A15': '머리 근거 접기 ▾ 없음',
    'A16': '근거 줄 ㄱ·(1) 칸 · 흐린 글자 없음',
    'A17': '근거 ▸ 처음 접힘(적은 근거 목록 숨김)',
    'A18': '근거 찾기 = uid 칩 · 단원명 · 칩 → 비교 창 · 근거로 안 들어감',
    'A19': '§4 카드 층 화면에 물리 데이터 글 0(문항 창 · 서랍 · 근거 창 · 쓰인 문항 창)',
}



# ══ 무리 B ══════════════════════════════════════════════════════════════════════════════
# 관문 B — 필기 도구 ⋯(물리 · 지학 · 생물) · TC1 · TR1 · TR2 — _harness_jagwa_cardfit.py 에 들어갈 몫(개발 사본)
import json

# ── JS ──
PICK_JS = r"""async (skip)=>{for(const r of DATA){const no=r[F.NO];if(typeof isC==='function'&&isC(r))continue;if((skip||[]).indexOf(no)>=0)continue;if(hist(no).length)continue;
  let ink=null;try{ink=await get('ink',HASBOOK?('qink:'+String(qk(no))):String(qk(no)))}catch(e){}
  const n=HASBOOK?((ink&&ink.s)||[]).length:(ink?Object.values(ink).reduce((a,v)=>a+((v||[]).length||0),0):0);if(n)continue;return no}return null}"""
B_OPEN_JS = r"""async (no)=>{await openView(no);for(let i=0;i<60;i++){await new Promise(r=>setTimeout(r,100));if(!HASBOOK||QUID===String(qk(no)))break}
  try{setTool('view')}catch(e){}await new Promise(r=>setTimeout(r,300));return {VNO,QUID:HASBOOK?QUID:null}}"""
# 획 넣기(지어낸 획) — 물리 = INK 층 L · 카드 층 = QINK.s 획 r
B_SEED_JS = r"""(o)=>{const mk=a=>{const p=[];for(let i=0;i<=8;i++){p.push(+(a.u0+(a.u1-a.u0)*i/8).toFixed(4),+(a.v0+(a.v1-a.v0)*i/8).toFixed(4))}return {c:'#16181B',w:2,p}};
  if(!HASBOOK){INK={};o.s.forEach(a=>{const L=a.L||0;(INK[L]=INK[L]||[]).push(mk(a))});const mx=Math.max(o.cur||0,...Object.keys(INK).map(Number));for(let L=0;L<=mx;L++)INK[L]=INK[L]||[];
    LAYERS=mx+1;LAYER=o.cur||0;try{fillLayerSel()}catch(e){}paintInk();saveInk()}
  else{QINK={s:o.s.map(a=>Object.assign(mk(a),{r:a.r||1}))};QR=o.cur||1;qFillSel();qPaint();qSave()}
  try{if(typeof IU!=='undefined'){IU.length=0;IRD.length=0;itUR()}}catch(e){}try{if(HASBOOK&&typeof QIU!=='undefined'){QIU.length=0;QIRD.length=0;if(typeof qiUR==='function')qiUR()}}catch(e){}return true}"""
# 정규화 점 → 화면 자리
PT_JS = r"""([u,v])=>{if(!HASBOOK){const c=inkc(),r=c.getBoundingClientRect(),q=toPix(u,v);return [r.left+q[0]/RENDER.W*r.width,r.top+q[1]/RENDER.H*r.height]}
  const sv=document.querySelector('#card #qink');const r=sv.getBoundingClientRect(),k=r.width/QCW;return [r.left+u*QCW*k,r.top+v*QCW*k]}"""
# 화면 길이(px) → 정규화 길이
DN_JS = r"""([dx,dy])=>{if(!HASBOOK){const c=inkc(),r=c.getBoundingClientRect();const a=toNorm(0,0),b=toNorm(dx/r.width*RENDER.W,dy/r.height*RENDER.H);return [b[0]-a[0],b[1]-a[1]]}
  const sv=document.querySelector('#card #qink');const r=sv.getBoundingClientRect(),k=r.width/QCW;return [dx/k/QCW,dy/k/QCW]}"""
ST_JS = r"""()=>{const A=HASBOOK?(QINK.s||[]):(INK[LAYER]||[]);const ls=(HASBOOK&&typeof QLS!=='undefined')?QLS:((typeof LS!=='undefined'&&LS)?LS:null);   /* 합치기 전(패치만) 카드 층 = QLS · QIU · QIRD */
  const box=HASBOOK?(()=>{const g=document.querySelector('#card #qink g.qls rect');return !!g&&g.style.display!=='none'})():(()=>{const b=document.querySelector('#lsLayer .lsbox');return !!b&&getComputedStyle(b).display!=='none'})();
  return {n:A.length,all:HASBOOK?(QINK.s||[]).length:Object.values(INK).reduce((a,v)=>a+((v||[]).length||0),0),p:A.map(s=>[s.p[0],s.p[1]]),r:HASBOOK?(QINK.s||[]).map(s=>qRoundOf(s)):null,
    sel:ls&&ls.sel?ls.sel.slice():null,mode:(typeof TOOL!=='undefined')?TOOL.mode:null,IU:(HASBOOK&&typeof QIU!=='undefined')?QIU.length:((typeof IU!=='undefined')?IU.length:null),IRD:(HASBOOK&&typeof QIRD!=='undefined')?QIRD.length:((typeof IRD!=='undefined')?IRD.length:null),box,
    menu:!!document.querySelector('#tlMenu.open'),lsm:[...document.querySelectorAll('#lsMenu button')].map(b=>b.textContent),
    ch:(()=>{const c=document.getElementById('tTools');return c?c.className:null})(),card:(()=>{const c=document.getElementById('card');return c?c.className:null})(),
    cut:!!document.getElementById('cutLayer')}}"""
SAVED_JS = r"""async ()=>{await new Promise(r=>setTimeout(r,500));if(!HASBOOK){const v=await get('ink',String(qk(VNO)));const A=(v&&v[LAYER])||[];return A.map(s=>[s.p[0],s.p[1]])}
  const v=await get('ink','qink:'+QUID);return ((v&&v.s)||[]).map(s=>[s.p[0],s.p[1]])}"""
B_EL_JS = r"""(q)=>{const e=document.querySelector(q);if(!e)return null;const r=e.getBoundingClientRect();const cs=getComputedStyle(e);
  return {cx:r.left+r.width/2,cy:r.top+r.height/2,w:r.width,h:r.height,t:r.top,vis:cs.display!=='none'&&cs.visibility!=='hidden'&&r.height>0,dis:!!e.disabled,on:!!(e.classList&&e.classList.contains('on'))}}"""
PILL_JS = r"""()=>{const P=document.getElementById('inkPill');if(!P)return null;const vis=e=>e&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().width>0;
  const kids=[...P.children].filter(vis);return {pen:kids.filter(e=>e.dataset&&e.dataset.pen).length,hl:kids.filter(e=>e.classList.contains('hl')).length,
    erase:!!P.querySelector('#tErase'),tools:!!P.querySelector('#tTools'),last:(kids.filter(e=>e.tagName==='BUTTON').pop()||{}).id||null,
    undoIn:!!P.querySelector('#tUndo'),cutIn:!!P.querySelector('#tCut'),txt:!!document.getElementById('tTxt'),txtVis:vis(document.getElementById('tTxt'))}}"""
MENU_JS = r"""()=>{const m=document.getElementById('tlMenu');if(!m)return null;const b=[...m.querySelectorAll('button')].filter(x=>getComputedStyle(x).display!=='none');
  return {open:m.classList.contains('open'),chips:b.map(x=>x.id),tops:b.map(x=>Math.round(x.getBoundingClientRect().top)),h:b.map(x=>Math.round(x.getBoundingClientRect().height)),
    dis:b.map(x=>!!x.disabled),undoDis:!!(document.getElementById('tUndo')||{}).disabled}}"""
ERASE_CUR_JS = r"""async ()=>{const b=document.getElementById('tErase');if(TOOL.mode!=='erase'){b.click();await new Promise(r=>setTimeout(r,150))}
  if(!document.getElementById('erPop'))b.click();await new Promise(r=>setTimeout(r,200));const e=document.querySelector('#erPop #eL');if(!e)return 'erPop 없음';e.click();await new Promise(r=>setTimeout(r,700));return 'ok'}"""
# 펜 획(WebKit = 그 자리 요소에 합성 pen 포인터 · 받은 요소에 이어 보냄)
B_PENSYN_JS = r"""(pts)=>{if(!Element.prototype.__spcw){const o=Element.prototype.setPointerCapture;Element.prototype.setPointerCapture=function(id){try{return o.call(this,id)}catch(e){if(e.name!=='NotFoundError')throw e}};Element.prototype.__spcw=1}
  const t=document.elementFromPoint(pts[0][0],pts[0][1]);if(!t)return null;
  const f=(ty,x,y,b)=>{const ev=new PointerEvent(ty,{bubbles:true,cancelable:true,composed:true,pointerId:41,pointerType:'pen',isPrimary:true,clientX:x,clientY:y,button:0,buttons:b,pressure:b?0.5:0});Object.defineProperty(ev,'getCoalescedEvents',{value:()=>[ev]});return t.dispatchEvent(ev)};   /* 합성 이벤트의 getCoalescedEvents = [] → 진짜 이벤트 하나 꼴([자기]) */
  f('pointerdown',pts[0][0],pts[0][1],1);for(let i=1;i<pts.length;i++)f('pointermove',pts[i][0],pts[i][1],1);f('pointerup',pts[pts.length-1][0],pts[pts.length-1][1],0);return t.id||t.tagName}"""
HS_JS = r"""()=>{const b=document.getElementById('hsPop');if(!b)return null;return [...b.querySelectorAll('.hsr')].map(r=>(r.querySelector('.hsn')||{}).textContent+(r.querySelector('.hsm')?'':'·빈'))}"""
SEEDREC_JS = r"""async ([no,ms])=>{const t0=Date.now()-3600000;ST[qk(no)]={h:ms.map((m,i)=>({m,t:t0+i*60000,s:20+i*5}))};await saveST();return true}"""
# 펜이 그을 수 있는 빈 띠(카드 층 = 밑에 진짜 단추(PEN_HIT) 없음 · 화면 안) — 물리 = 시험지 그림 위 아무 데나
FREE_JS = r"""(u0)=>{if(!HASBOOK)return [u0||0.30,0.40];const sv=document.querySelector('#card #qink');if(!sv)return null;const r=sv.getBoundingClientRect(),k=r.width/QCW;
  const keep=sv.style.pointerEvents;sv.style.pointerEvents='none';let out=null;
  try{for(let v=0.06;v<1.6&&!out;v+=0.02){let ok=true;for(let u=(u0||0.30);u<=(u0||0.30)+0.16;u+=0.04){const x=r.left+u*QCW*k,y=r.top+v*QCW*k;
      if(y<60||y>innerHeight-70||x<0||x>innerWidth){ok=false;break}const e=document.elementFromPoint(x,y);if(!e||(e.closest&&e.closest(PEN_HIT+',.vbot,.vtop,#navdr,.sheet,#g3Pop')&&!e.closest('#card #qink'))){ok=false;break}}
    if(ok)out=[u0||0.30,+v.toFixed(2)]}}finally{sv.style.pointerEvents=keep}return out}"""
# 빈 칸(카드 층) — [u0..u1]×[v..v+dv] 격자가 다 #qink 위 · 화면 안 · 그 자리 맨 위가 #qink 거나 밑에 단추·글칸 없음
FREE2_JS = r"""([u0,u1,v0,dv])=>{if(!HASBOOK)return v0;const sv=document.querySelector('#card #qink');if(!sv)return null;const r=sv.getBoundingClientRect(),k=r.width/QCW;
  const okAt=(x,y)=>{if(y<60||y>innerHeight-70||x<4||x>innerWidth-4)return false;const t=document.elementFromPoint(x,y);if(!t)return false;if(!(t===sv||sv.contains(t)))return false;
    const keep=sv.style.pointerEvents;sv.style.pointerEvents='none';const e=document.elementFromPoint(x,y);sv.style.pointerEvents=keep;
    return !(e&&e.closest&&e.closest(UNDER_HIT+',textarea,input,select'))};
  for(let v=v0;v<1.6;v+=0.02){let ok=true;for(let u=u0;u<=u1+1e-9&&ok;u+=0.025)for(let w=v;w<=v+dv+1e-9;w+=0.01){if(!okAt(r.left+u*QCW*k,r.top+w*QCW*k)){ok=false;break}}
    if(ok)return +v.toFixed(2)}return null}"""
IMGW_JS = r"""async ()=>{for(let i=0;i<60;i++){const im=[...document.querySelectorAll('#card img')];if(im.every(x=>x.complete&&x.naturalWidth>0))break;await new Promise(r=>setTimeout(r,100))}await new Promise(r=>setTimeout(r,150));return 1}"""
CANDS_JS = r"""async ([skip,n])=>{const out=[];for(const r of DATA){const no=r[F.NO];if(typeof isC==='function'&&isC(r))continue;if((skip||[]).indexOf(no)>=0)continue;if(hist(no).length)continue;
  let ink=null;try{ink=await get('ink','qink:'+String(qk(no)))}catch(e){}if(((ink&&ink.s)||[]).length)continue;out.push(no);if(out.length>=n)break}return out}"""
# 카드 층 빈 띠 — 펜 덮개(#card.penon)를 잠깐 켜고 잼(맨 위가 #qink · 그 밑에 UNDER_HIT · 글칸 없음 · 화면 안) · 가장 긴 띠 [길이, 시작 v] · room = #cardwrap 굴릴 틈
BAND_JS = r"""([u0,u1])=>{const sv=document.querySelector('#card #qink');if(!sv)return null;const cd=document.getElementById('card'),had=cd.classList.contains('penon');cd.classList.add('penon');
  try{const r=sv.getBoundingClientRect(),k=r.width/QCW;
  const okAt=(x,y)=>{if(y<60||y>innerHeight-70||x<4||x>innerWidth-4)return false;const t=document.elementFromPoint(x,y);if(!t)return false;if(!(t===sv||sv.contains(t)))return false;
    const keep=sv.style.pointerEvents;sv.style.pointerEvents='none';const e=document.elementFromPoint(x,y);sv.style.pointerEvents=keep;return !(e&&e.closest&&e.closest(UNDER_HIT+',textarea,input,select'))};
  let best=[0,0],run=0,st=0;const H=r.height/(QCW*k);for(let v=0;v<=H+1e-9;v+=0.01){let ok=true;for(let u=u0;u<=u1+1e-9;u+=0.025)if(!okAt(r.left+u*QCW*k,r.top+v*QCW*k)){ok=false;break}
    if(ok){if(!run)st=v;run+=0.01;if(run>best[0])best=[+run.toFixed(2),+st.toFixed(2)]}else run=0}
  const cw=document.getElementById('cardwrap');return {band:best,room:cw?cw.scrollHeight-cw.clientHeight:null}}finally{if(!had)cd.classList.remove('penon')}}"""
BK_JS = r"""async ()=>{try{bookOpen(1,true)}catch(e){return 'ERR '+e}await new Promise(r=>setTimeout(r,1500));const t=document.getElementById('bktools');if(!t)return null;
  const out=[...t.querySelectorAll('[data-tool]')].map(x=>x.dataset.tool+(getComputedStyle(x).display==='none'?'-':''));try{bkClose()}catch(e){}return out}"""


def pen(p, eng, pts):
    """펜 긋기 — Chromium = CDP pointerType pen · WebKit = 합성 pen 포인터"""
    if eng == 'webkit':   # WebKit = CDP 없음 → 그 자리 요소에 합성 pen 포인터(물리 필기 = 펜만 · 합성 포인터의 setPointerCapture NotFoundError 는 하네스 쪽에서만 삼킴)
        return p.ev(B_PENSYN_JS, pts)
    c = p._cdp()
    s = lambda ty, x, y, b, bs: c.send('Input.dispatchMouseEvent', {'type': ty, 'x': x, 'y': y, 'button': b, 'buttons': bs, 'clickCount': 1 if ty != 'mouseMoved' else 0, 'pointerType': 'pen', 'force': 0.5})
    s('mouseMoved', pts[0][0], pts[0][1], 'none', 0); s('mousePressed', pts[0][0], pts[0][1], 'left', 1)
    for x, y in pts[1:]:
        s('mouseMoved', x, y, 'left', 1); p.wait(12)
    s('mouseReleased', pts[-1][0], pts[-1][1], 'left', 0)
    return 'cdp'


def mdrag(p, pts, hold=0):
    m = p.pg.mouse
    m.move(*pts[0]); m.down()
    if hold:
        p.wait(hold)
    for x, y in pts[1:]:
        m.move(x, y, steps=2); p.wait(10)
    m.up()


def ring(p, u0, v0, u1, v1, pad=10):
    a = p.ev(PT_JS, [u0, v0]); b = p.ev(PT_JS, [u1, v1])
    x0, y0, x1, y1 = min(a[0], b[0]) - pad, min(a[1], b[1]) - pad, max(a[0], b[0]) + pad, max(a[1], b[1]) + pad
    pts = []
    for t in range(9):
        pts.append((x0 + (x1 - x0) * t / 8, y0))
    for t in range(1, 9):
        pts.append((x1, y0 + (y1 - y0) * t / 8))
    for t in range(1, 9):
        pts.append((x1 - (x1 - x0) * t / 8, y1))
    for t in range(1, 9):
        pts.append((x0, y1 - (y1 - y0) * t / 8))
    return pts


def press(p, q, touch=False, wait=350):
    e = p.ev(B_EL_JS, q)
    if not e or not e['vis']:
        return False
    (p.tap if touch else p.click)(e['cx'], e['cy'], wait)
    return True


def menu_open(p, touch=False):
    if not p.ev("!!document.querySelector('#tlMenu.open')"):
        press(p, '#tTools', touch)
    return p.ev(MENU_JS)


A_ = (0.30, 0.20, 0.40, 0.22)
B_ = (0.60, 0.20, 0.70, 0.22)


def geom(p):
    """A · B 획 자리 — 물리 = 0.20 · 카드 층 = 고른 문항의 빈 띠 맨 위 + 0.03(올가미 테 · 옮긴 자리 · 길게 누를 곳 · 펜 띠가 다 그 안)"""
    b = p.ev(BAND_JS, [0.24, 0.86])
    v = 0.20 if not b or b['band'][0] < 0.2 else round(b['band'][1] + 0.03, 2)
    return (0.30, v, 0.40, v + 0.02), (0.60, v, 0.70, v + 0.02), v


def pick_card(p, skip=(), need=0.15, n=80):
    """카드 층 시험 문항 — 기록 · 획 없는 문항 가운데 #qink 위 빈 띠(u 0.24~0.86 · 펜 덮개 켠 채 · 밑에 단추 · 글칸 없음)가 need 넘는 첫 문항(그림 문항) · 물리 = PICK_JS"""
    if not p.ev("HASBOOK"):
        return p.ev(PICK_JS, list(skip)), None
    for no in p.ev(CANDS_JS, [list(skip), n]):
        p.ev(B_OPEN_JS, no)
        p.ev(IMGW_JS)
        b = p.ev(BAND_JS, [0.24, 0.86])
        if b and b['band'][0] >= need:
            return no, b
    return None, None


def seedAB(p, cur=None, A=None, B=None):
    A = A or A_; B = B or B_
    s = [dict(u0=A[0], v0=A[1], u1=A[2], v1=A[3]), dict(u0=B[0], v0=B[1], u1=B[2], v1=B[3])]
    return p.ev(B_SEED_JS, {'s': s, 'cur': cur})


def cen(p, a):
    x0, y0 = p.ev(PT_JS, [a[0], a[1]]); x1, y1 = p.ev(PT_JS, [a[2], a[3]])
    return ((x0 + x1) / 2, (y0 + y1) / 2)


def lasso_on(p, touch=False):
    menu_open(p, touch)
    press(p, '#tLasso', touch)
    p.wait(250)


def flow_B(p, eng, subj, no, no2=None):
    o = {}
    st = lambda: p.ev(ST_JS)
    A_, B_, V = geom(p)
    o['자리'] = V
    seedAB(p, cur=(1 if subj != 'phys' else 0), A=A_, B=B_); p.wait(300)
    # T1 알약
    o['T1'] = p.ev(PILL_JS)
    if not o['T1'] or not o['T1'].get('tools'):
        return o   # 바탕 = ⋯ 없음 → 뒤 칸은 못 잼
    # T2 ⋯ → 칩
    m = menu_open(p); o['T2'] = m
    p.ev("(()=>{try{tlClose()}catch(e){}})()"); p.wait(150)
    # T3 ➰
    lasso_on(p)
    s3 = st(); o['T3'] = {'mode': s3['mode'], 'menu': s3['menu'], 'ch': s3['ch'], 'card': s3['card']}
    # T4 둘러 고름 → 끌기
    mdrag(p, ring(p, *A_)); p.wait(300)
    s4 = st()
    c = cen(p, A_); dx, dy = 40, 30
    mdrag(p, [c] + [(c[0] + dx * t / 6, c[1] + dy * t / 6) for t in range(1, 7)]); p.wait(400)
    s4b = st(); dn = p.ev(DN_JS, [dx, dy]); sv = p.ev(SAVED_JS)
    o['T4'] = {'sel': s4['sel'], 'box': s4['box'], 'p0': s4['p'][0] if s4['p'] else None, 'p1': s4b['p'][0] if s4b['p'] else None, 'dn': dn,
               'saved': (sv[0] if sv else None), 'B 그대로': (s4b['p'][1] == s4['p'][1]) if len(s4b['p']) > 1 and len(s4['p']) > 1 else None}
    # T5 ↺ · ↻
    menu_open(p); press(p, '#tUndo'); p.wait(300); s5a = st()
    press(p, '#tRedo'); p.wait(300); s5b = st()
    o['T5'] = {'↺ 뒤': s5a['p'][0] if s5a['p'] else None, '↺ 뒤 메뉴': s5a['menu'], '↻ 뒤': s5b['p'][0] if s5b['p'] else None, '원래': o['T4']['p0'], '옮긴': o['T4']['p1']}
    p.ev("(()=>{try{tlClose()}catch(e){}})()"); p.wait(150)
    if p.ev("TOOL.mode") != 'lasso':
        lasso_on(p)
    # T6 톡 → 복사 · 빈 곳 길게 → 붙여넣기 · 잘라내기 · 다음 문항 붙여넣기
    moved = (A_[0] + dn[0], A_[1] + dn[1], A_[2] + dn[0], A_[3] + dn[1])
    mdrag(p, ring(p, *moved)); p.wait(300)
    sel6 = st()['sel']
    c = cen(p, moved); p.click(c[0], c[1], 400); m1 = st()['lsm']
    clicked = p.ev("(t)=>{const b=[...document.querySelectorAll('#lsMenu button')].find(x=>x.textContent===t);if(!b)return false;b.click();return true}", '복사'); p.wait(300)
    n0 = st()['n']
    e0 = p.ev(PT_JS, [0.74, V + 0.12]); mdrag(p, [e0], hold=800); p.wait(300); m2 = st()['lsm']
    p.ev("(t)=>{const b=[...document.querySelectorAll('#lsMenu button')].find(x=>x.textContent===t);if(b)b.click();return !!b}", '붙여넣기'); p.wait(500)
    s6a = st()
    sel = s6a['sel'] or []
    cut_n = None
    if sel:
        # 상자 가운데 = 붙인 획(정규화 → 화면)
        pp = s6a['p'][sel[0]]
        q = p.ev(PT_JS, [pp[0] + 0.05, pp[1] + 0.01])
        p.click(q[0], q[1], 400)
        p.ev("(t)=>{const b=[...document.querySelectorAll('#lsMenu button')].find(x=>x.textContent===t);if(b)b.click();return !!b}", '잘라내기'); p.wait(500)
        cut_n = st()['n']
    if no2 is None:
        nx = p.ev("(()=>{go(1);return VNO})()"); p.wait(2200)
    else:   # 다른 문항(빈 띠 있는 문항) — 문항 창에서 그 문항으로 옮김
        p.ev(B_OPEN_JS, no2); nx = no2
    if p.ev("TOOL.mode") != 'lasso':
        lasso_on(p)
    n_next0 = st()['n']
    _, _, V2 = geom(p)
    e2 = p.ev(PT_JS, [0.74, V2 + 0.12]); mdrag(p, [e2], hold=800); p.wait(300)
    p.ev("(t)=>{const b=[...document.querySelectorAll('#lsMenu button')].find(x=>x.textContent===t);if(b)b.click();return !!b}", '붙여넣기'); p.wait(500)
    n_next1 = st()['n']
    o['T6'] = {'둘러 고름': sel6, '톡 메뉴': m1, '복사 누름': clicked, '길게 메뉴': m2, '붙인 뒤': [n0, s6a['n']], '잘라낸 뒤': cut_n, '다음 문항': [nx, n_next0, n_next1]}
    # T7 펜 긋기 → 지우개 → ↺ 둘 · ↻ 둘
    p.ev(B_OPEN_JS, no); seedAB(p, cur=(1 if subj != 'phys' else 0), A=A_, B=B_); p.wait(300)
    press(p, '[data-pen="#16181B"]'); p.wait(200)
    fb = [0.30, V + 0.07]
    a = p.ev(PT_JS, [fb[0], fb[1]]); b = p.ev(PT_JS, [fb[0] + 0.15, fb[1] + 0.005])
    hit = pen(p, eng, [(a[0] + (b[0] - a[0]) * t / 10, a[1] + (b[1] - a[1]) * t / 10) for t in range(11)]); p.wait(500)
    n_draw = st()['n']
    press(p, '#tErase'); p.wait(200)
    a2 = p.ev(PT_JS, [fb[0] + 0.075, fb[1] - 0.035]); b2 = p.ev(PT_JS, [fb[0] + 0.075, fb[1] + 0.035])
    pen(p, eng, [(a2[0], a2[1] + (b2[1] - a2[1]) * t / 10) for t in range(11)]); p.wait(500)
    n_er = st()['n']
    seq = []
    menu_open(p)
    for bt in ('#tUndo', '#tUndo', '#tRedo', '#tRedo'):
        press(p, bt); p.wait(300); seq.append(st()['n'])
    p.ev("(()=>{try{tlClose()}catch(e){}})()")
    o['T7'] = {'띠': fb, '받은 요소': hit, '긋기 뒤': n_draw, '지운 뒤': n_er, '↺↺↻↻': seq}
    # T8 빈 곳 지우개 = 기록 그대로 · 지금 회독 지우기 → ↺ = 다 살아남
    iu0 = st()['IU']
    a3 = p.ev(PT_JS, [0.62, V + 0.11]); b3 = p.ev(PT_JS, [0.74, V + 0.115])
    pen(p, eng, [(a3[0] + (b3[0] - a3[0]) * t / 8, a3[1] + (b3[1] - a3[1]) * t / 8) for t in range(9)]); p.wait(500)
    iu1 = st()['IU']; n_b = st()['n']
    er = p.ev(ERASE_CUR_JS); n_c = st()['n']
    menu_open(p); press(p, '#tUndo'); p.wait(400); n_d = st()['n']
    p.ev("(()=>{try{tlClose()}catch(e){}})()")
    o['T8'] = {'빈 곳 지우개 기록': [iu0, iu1], '지금 회독 지우기': [n_b, er, n_c], '↺ 뒤': n_d}
    # T9(물리) 오리기 중 ➰ = 오리기 판 없음 · 펜 = 다 풀림
    if subj == 'phys':
        menu_open(p); press(p, '#tCut'); p.wait(300); c1 = st()['cut']
        lasso_on(p); s9 = st()
        press(p, '[data-pen="#16181B"]'); p.wait(200); s9b = st()
        o['T9'] = {'오리기 판': c1, '➰ 뒤': {'판': s9['cut'], 'mode': s9['mode']}, '펜 뒤': {'mode': s9b['mode'], 'ls': s9b['ch'], 'sel': s9b['sel'], '판': s9b['cut']}}
    # T11 지난 회독 획 안 잡힘
    cur = 1 if subj == 'phys' else 2
    p.ev(B_SEED_JS, {'s': [dict(u0=A_[0], v0=A_[1], u1=A_[2], v1=A_[3], L=0, r=1), dict(u0=B_[0], v0=B_[1], u1=B_[2], v1=B_[3], L=cur, r=cur)], 'cur': cur}); p.wait(300)
    lasso_on(p)
    mdrag(p, ring(p, *A_)); p.wait(300)
    s11 = st()
    o['T11'] = {'sel': s11['sel'], '지금 회독 획': s11['n']}
    p.ev("(()=>{try{setTool('view')}catch(e){}})()")
    return o


def flow_TR(p, subj, no, rounds):
    """카드 층 빈 회독 줄 — 기록 셋(앞 열람) · rounds 회독에만 획 → 기록 2 ✕"""
    p.ev(SEEDREC_JS, [no, ['O', 'X', 'Q']])
    p.ev(B_OPEN_JS, no); p.wait(300)
    qr = p.ev("QR")
    s = [dict(u0=0.30, v0=0.20 + 0.05 * k, u1=0.40, v1=0.22 + 0.05 * k, r=r) for k, r in enumerate(rounds)]
    p.ev(B_SEED_JS, {'s': s, 'cur': qr}); p.wait(300)
    p.ev("(no)=>{const o=document.getElementById('hsPop');if(o&&o.__close)o.__close();histSheet(no);return !!document.getElementById('hsPop')}", no); p.wait(300)
    before = p.ev(HS_JS)
    ok = p.ev("()=>{const b=document.querySelector('#hsPop .hsr[data-i=\"1\"] .rm');if(!b)return false;b.click();return true}"); p.wait(900)
    after = p.ev(HS_JS)
    rs = p.ev("(QINK.s||[]).map(s=>qRoundOf(s))")
    p.ev("(()=>{const o=document.getElementById('hsPop');if(o&&o.__close)o.__close();return 1})()"); p.wait(200)
    p.ev("(no)=>{histSheet(no);return 1}", no); p.wait(300)
    again = p.ev(HS_JS)
    p.ev("(()=>{const o=document.getElementById('hsPop');if(o&&o.__close)o.__close();return 1})()")
    return {'QR': qr, '줄 전': before, '✕': ok, '줄 뒤': after, '획 r': rs, '다시 연 줄': again, 'QR 뒤': p.ev("QR")}


def flow_T10(q, eng, subj, no):
    if q.ev("HASBOOK"):   # 카드 층 = 폰에서 #cardwrap 이 굴러야(굴릴 틈 ≥ 60) · 손가락 놓을 빈 띠 있는 문항(그림 문항)
        for c in q.ev(CANDS_JS, [[], 80]):
            q.ev(B_OPEN_JS, c); q.ev(IMGW_JS)
            b = q.ev(BAND_JS, [0.24, 0.86])
            if b and (b.get('room') or 0) >= 60 and b['band'][0] >= 0.1:
                no = c
                break
    q.ev(B_OPEN_JS, no); q.ev(IMGW_JS); q.wait(300)
    seedAB(q, cur=(1 if subj != 'phys' else 0)); q.wait(200)
    m = None
    if q.ev("!!document.getElementById('tTools')"):
        press(q, '#tTools', touch=True); q.wait(300)
        m = q.ev(MENU_JS)
        press(q, '#tLasso', touch=True); q.wait(300)
    mode = q.ev("TOOL.mode")
    scr = r"""()=>{let s=0,e=HASBOOK?document.querySelector('#card #qink'):inkc();while(e){s+=e.scrollTop||0;e=e.parentElement}return s+(document.scrollingElement||{}).scrollTop}"""
    s0 = q.ev(scr)
    _, _, V10 = geom(q)
    a = q.ev(PT_JS, [0.5, V10 + 0.04]); ls_after = None   # 손가락 = 빈 띠(카드 층 #qink 위 · 밑에 단추 없음)
    if eng != 'webkit':
        c = q._cdp()
        c.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': a[0], 'y': a[1], 'radiusX': 6, 'radiusY': 6, 'id': 1}]})
        for t in range(1, 9):
            c.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': a[0], 'y': a[1] - 25 * t, 'radiusX': 6, 'radiusY': 6, 'id': 1}]}); q.wait(16)
        c.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); q.wait(500)
    else:
        q.ev(r"""(a)=>{const t=document.elementFromPoint(a[0],a[1]);if(!t)return 0;const f=(ty,y,b)=>{const ev=new PointerEvent(ty,{bubbles:true,cancelable:true,composed:true,pointerId:51,pointerType:'touch',isPrimary:true,clientX:a[0],clientY:y,buttons:b});Object.defineProperty(ev,'getCoalescedEvents',{value:()=>[ev]});return t.dispatchEvent(ev)};
          f('pointerdown',a[1],1);for(let i=1;i<9;i++)f('pointermove',a[1]-25*i,1);f('pointerup',a[1]-200,0);return 1}""", a); q.wait(400)
    ls_after = q.ev("(typeof LS!=='undefined'&&LS)?(LS.path?'path':'sel'):null")
    s1 = q.ev(scr)
    room = q.ev(r"""()=>{let m=0,e=HASBOOK?document.querySelector('#card #qink'):inkc();while(e){const cs=getComputedStyle(e);if(/(auto|scroll)/.test(cs.overflowY))m=Math.max(m,e.scrollHeight-e.clientHeight);e=e.parentElement}
      const d=document.scrollingElement;return Math.max(m,d?d.scrollHeight-d.clientHeight:0)}""")
    q.ev("(()=>{try{setTool('view')}catch(e){}})()")
    return {'문항': no, '메뉴': m, 'mode': mode, '올가미 남음': ls_after, '굴림': [s0, s1], '굴릴 틈': room}


def _eqp(a, b, d=0.002):
    return bool(a) and bool(b) and abs(a[0] - b[0]) <= d and abs(a[1] - b[1]) <= d


def judge_B(subj, o, tc1_base=None):
    """o = {'B': flow_B 값, 'TC1': [...], 'TR1': {...}, 'TR2': {...}, 'T10': {...}} · tc1_base = 바탕 교재 창 도구 줄(TC1 잣대)"""
    J, b = {}, (o or {}).get('B') or {}
    card = subj != 'phys'
    if b.get('ERR'):
        return {c: (False, {'오류': b['ERR'][-300:]}) for c in NAMES_B if c != 'T9' or not card}
    t1 = b.get('T1') or {}
    J['T1'] = (bool(t1) and t1.get('pen', 0) > 0 and t1.get('hl', 0) > 0 and t1.get('erase') and t1.get('tools') and t1.get('last') == 'tTools'
               and not t1.get('undoIn') and not t1.get('cutIn') and (not card or not t1.get('txt')), t1 or '알약 없음')
    t2 = b.get('T2') or {}
    want = ['tLasso', 'tUndo', 'tRedo'] + ([] if card else ['tCut'])
    J['T2'] = (bool(t2) and t2.get('open') and t2.get('chips') == want and len(set(t2.get('tops') or [0, 1])) == 1 and t2.get('undoDis'), t2 or 'ⵈ 없음')
    t3 = b.get('T3') or {}
    J['T3'] = (bool(t3) and t3.get('mode') == 'lasso' and not t3.get('menu') and 'ls' in str(t3.get('ch') or '').split() and (not card or {'lsmode', 'penon'} <= set(str(t3.get('card') or '').split())), t3 or None)
    t4 = b.get('T4') or {}
    dn, p0, p1 = t4.get('dn'), t4.get('p0'), t4.get('p1')
    J['T4'] = (bool(t4) and t4.get('sel') == [0] and t4.get('box') and bool(dn and p0 and p1) and abs(p1[0] - p0[0] - dn[0]) <= 0.01 and abs(p1[1] - p0[1] - dn[1]) <= 0.01
               and _eqp(t4.get('saved'), p1) and t4.get('B 그대로'), t4 or None)
    t5 = b.get('T5') or {}
    J['T5'] = (bool(t5) and _eqp(t5.get('↺ 뒤'), t5.get('원래')) and t5.get('↺ 뒤 메뉴') and _eqp(t5.get('↻ 뒤'), t5.get('옮긴')), t5 or None)
    t6 = b.get('T6') or {}
    pa, nx = t6.get('붙인 뒤') or [None, None], t6.get('다음 문항') or [None, None, None]
    J['T6'] = (bool(t6) and t6.get('둘러 고름') == [0] and t6.get('톡 메뉴') == ['복사', '잘라내기', '지우기'] and t6.get('길게 메뉴') == ['붙여넣기'] and pa[0] is not None and pa[1] == pa[0] + 1
               and t6.get('잘라낸 뒤') == pa[0] and nx[2] is not None and nx[1] is not None and nx[2] == nx[1] + 1, t6 or None)
    t7 = b.get('T7') or {}
    sq = t7.get('↺↺↻↻') or []
    J['T7'] = (bool(t7) and t7.get('지운 뒤') is not None and t7.get('긋기 뒤') == t7['지운 뒤'] + 1 and sq == [t7['긋기 뒤'], t7['지운 뒤'], t7['긋기 뒤'], t7['지운 뒤']], t7 or None)
    t8 = b.get('T8') or {}
    iu, ec = t8.get('빈 곳 지우개 기록') or [None, None], t8.get('지금 회독 지우기') or [None, None, None]
    J['T8'] = (bool(t8) and iu[0] is not None and iu[0] == iu[1] and ec[1] == 'ok' and ec[2] == 0 and t8.get('↺ 뒤') == ec[0] and (ec[0] or 0) > 0, t8 or None)
    if not card:
        t9 = b.get('T9') or {}
        a9, p9 = t9.get('➰ 뒤') or {}, t9.get('펜 뒤') or {}
        J['T9'] = (bool(t9) and t9.get('오리기 판') and not a9.get('판') and a9.get('mode') == 'lasso' and p9.get('mode') == 'pen' and 'ls' not in str(p9.get('ls') or '').split()
                   and not p9.get('sel') and not p9.get('판'), t9 or None)
    t10 = (o or {}).get('T10') or {}
    m10, sc = t10.get('메뉴'), t10.get('굴림') or [0, 0]
    J['T10'] = ((m10 is None or (m10.get('open') and min(m10.get('h') or [0]) >= 28)) and sc[1] > sc[0] and not t10.get('올가미 남음'),
                {'메뉴 칩 높이': (m10 or {}).get('h'), '⋯': m10 is not None, 'mode': t10.get('mode'), '굴림': sc, '올가미 남음': t10.get('올가미 남음')})
    t11 = b.get('T11') or {}
    J['T11'] = (bool(t11) and not t11.get('sel') and t11.get('지금 회독 획') is not None, t11 or None)
    if card:
        tc = (o or {}).get('TC1')
        J['TC1'] = (tc is not None and tc == (tc1_base if tc1_base is not None else tc), {'교재 창 도구': tc, '바탕': tc1_base})
        r1 = (o or {}).get('TR1') or {}
        J['TR1'] = (r1.get('✕') and r1.get('줄 뒤') == ['1회독', '2회독'] and r1.get('획 r') == [1, 2] and r1.get('다시 연 줄') == r1.get('줄 뒤') and r1.get('QR 뒤') == (r1.get('QR') or 0) - 1, r1)
        r2 = (o or {}).get('TR2') or {}
        rec2 = lambda L: [x for x in (L or []) if not x.endswith('·빈')]
        J['TR2'] = (r2.get('✕') and r2.get('획 r') == [2] and rec2(r2.get('줄 뒤')) == ['1회독', '2회독'] and rec2(r2.get('다시 연 줄')) == ['1회독', '2회독'], r2)
    return J


NAMES_B = {
    'T1': '알약 = 펜 · 형광 · 지우개 · ⋯(↺ · ✂ 알약에서 걷음 · 카드 층 T 글상자 없음)',
    'T2': '⋯ → 칩 물리 ➰↺↻✂ / 카드 층 ➰↺↻ · 가로 한 줄 · 되돌리기 흐림',
    'T3': '➰ → 올가미 · 메뉴 닫힘 · 칩 .ls · 카드 #card.lsmode.penon',
    'T4': '마우스로 둘러 그림 → 그 획만 · 점선 상자 · 끌기 = 끈 만큼(±0.01) · 저장(ink / qink)',
    'T5': '↺ → 원래 자리 · ↺ 뒤 메뉴 열린 채 · ↻ → 옮긴 자리',
    'T6': '상자 톡 → 복사 · 잘라내기 · 지우기 · 복사 → 빈 곳 길게 → 붙여넣기 +1 · 잘라내기 −1 · 다른 문항 붙여넣기 +1',
    'T7': '긋기 → 지우개 → ↺ 둘 · ↻ 둘',
    'T8': '빈 곳 지우개 = 되돌리기 기록 그대로 · 지금 회독 지우기 → ↺ = 다 살아남',
    'T9': '물리 오리기 중 ➰ = 오리기 판 닫힘 · 펜 고름 = 올가미 · 고름 다 풀림',
    'T10': '폰 384 손가락 톡 ⋯ 메뉴 · 칩 높이 ≥ 28 · 올가미 중 손가락 끌기 = 굴리기',
    'T11': '지난 회독 획 안 잡힘',
    'TC1': '카드 층 교재 창 도구(◻ 오리기 · 📍 · 🃏 …) = 바탕과 같음',
    'TR1': '기록 셋 · 회독 1 · 3 에만 획 → 기록 2 ✕ → 줄 1 · 2(옛 3) · 옛 3 획 r = 2 · 빈 줄 0 · 다시 열어도 같음 · QR −1',
    'TR2': '기록 셋 · 회독 2 에 획 → 기록 2 ✕ → 획 r 그대로(2) · 기록 줄 1 · 2(✕ 뒤 기록은 당겨짐 = 물리 recfix · 바탕과 같음)',
}



# ══ 무리 C ══════════════════════════════════════════════════════════════════════════════
# 관문 C — 같은 근거(물리 · 지학 · 생물) · C1~C7 — _harness_jagwa_cardfit.py 에 들어갈 몫(개발 사본)
# 흐름: PC 1100×800 마우스 · 기록 · 근거 없는 문항 A · B · C · D · A 에 지어낸 근거 1 줄(앱 데이터 함수) · B 근거 0
#   C1 B 1 칸(트리거)에 A 글 낱말 → 찾은 줄 마우스 누름 → B 1 줄 · src = A uid|k
#   C2 B 줄 길게 눌러 끝에 글 더함 · Enter → B 1 줄 · A 글 = 새 글
#   C3 A 줄 길게 눌러 고침 → ggFlat(B) · B 화면 · B t(메모리 · 저장 통) = 새 글
#   C4 C 에서 같은 낱말 → 한 줄 · 쓴 문항 2
#   C5 A ✕ → 「같이 쓰는 문항 1개」 → 지우기 → A · B 둘 다 없음
#   C6 A 에 다시 넣고 B 가 찾아 넣음 → B ✕ → 「이 문항에서만 뺍니다」 → B 만 빠지고 A 그대로
#   C7 2 칸(공식·개념 · 블록 ref) = 바탕과 같음(물리 = 블록 찾기 → ref 항목 · src 없음 · 카드 층 = 2 칸 고르는 길 · ref 항목 수를 바탕과 맞댐)
# 시험 글은 지어낸 것만 · 돌려주는 값 = 셈 · 참거짓 · md5 앞 8 자 · id(uid · k) — 실제 글은 안 돌려줌
import hashlib
import hashlib as _hl
_C_h6 = lambda s: _hl.md5(s.encode('utf-8')).hexdigest()[:6]   # 판마다 다른 tag(serve_PP 는 tag 로 서버를 붙잡아 둠 — 같은 tag 면 바탕 판이 새 판 앱을 받음)
import traceback
import _qa_jagwa_common as JG

W_ = '쿼즐뭉'                    # 찾을 낱말(지어낸 것 · 실제 근거에 없음을 PRE 로 잼)
T0 = '시험근거C 쿼즐뭉 일곱'      # A 근거 글
A2 = ' 더함둘'                    # C2 에서 B 쪽 끝에 더함
A3 = ' 고침셋'                    # C3 에서 A 쪽 끝에 더함
T6 = '시험근거C 쿼즐뭉 여섯'      # C6 에서 A 에 다시 넣는 글
C7Q = '1'                         # C7 2 칸 블록 찾기 글(지어낸 숫자 하나 · 절 번호에 걸림)


def h8(s):
    return hashlib.md5(' '.join(str(s).split()).encode('utf-8')).hexdigest()[:8]


# ── JS ──
MD5 = r"""(s)=>{const b=new TextEncoder().encode(String(s)),n=b.length,W=new Uint32Array((((n+8)>>>6)+1)*16);for(let i=0;i<n;i++)W[i>>2]|=b[i]<<((i%4)*8);W[n>>2]|=0x80<<((n%4)*8);W[W.length-2]=n*8;
 const S=[7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21],K=[];for(let i=0;i<64;i++)K[i]=Math.floor(Math.abs(Math.sin(i+1))*4294967296)>>>0;
 let a0=0x67452301,b0=0xefcdab89,c0=0x98badcfe,d0=0x10325476;for(let o=0;o<W.length;o+=16){let A=a0,B=b0,C=c0,D=d0;for(let i=0;i<64;i++){let F,g;if(i<16){F=(B&C)|(~B&D);g=i}else if(i<32){F=(D&B)|(~D&C);g=(5*i+1)%16}else if(i<48){F=B^C^D;g=(3*i+5)%16}else{F=C^(B|~D);g=(7*i)%16}
  F=(F+A+K[i]+W[o+g])>>>0;A=D;D=C;C=B;B=(B+((F<<S[i])|(F>>>(32-S[i]))))>>>0}a0=(a0+A)>>>0;b0=(b0+B)>>>0;c0=(c0+C)>>>0;d0=(d0+D)>>>0}
 const h=x=>[0,8,16,24].map(s=>((x>>>s)&255).toString(16).padStart(2,'0')).join('');return h(a0)+h(b0)+h(c0)+h(d0)}"""
# 쪽에 md5 · 낱말 고르기(N) 심기 — 글은 늘 공백 하나로 모아 md5 앞 8 자
HELP_JS = "()=>{const m=" + MD5 + ";window.__cfN=s=>String(s==null?'':s).replace(/\\s+/g,' ').trim();window.__cfH=s=>m(window.__cfN(s)).slice(0,8);return window.__cfH('abc')}"
# 기록 · 근거 · 연결 · 이어 둔 것 없는 문항 n 개
PICKQ_JS = r"""(n)=>{const used=new Set();for(const u in GG)(GG[u]||[]).forEach(x=>{if(x&&x.src)used.add(String(x.src).split('|')[0])});const out=[];
 for(const r of DATA){const no=r[F.NO];if(typeof isC==='function'&&isC(r))continue;if(hist(no).length)continue;const u=GGU(r);if(!u||!rowByUid(u))continue;
  if(ggOf(u).length||ggRefOf(u).length||ggOwners(u).length||used.has(u))continue;out.push(no);if(out.length>=n)break}return out}"""
UIDS_JS = r"""(nos)=>nos.map(no=>GGU(rec(no)))"""
# 찾을 낱말이 실제 근거에 이미 있는지(있으면 칸이 흐려짐) · 근거 문항 수
PRE_JS = r"""(w)=>{let n=0,m=0;for(const u in GG){m++;(GG[u]||[]).forEach(x=>{if(x&&window.__cfN(ggFlat(x)).indexOf(w)>=0)n++})}return {w_hits:n,gg_uids:m}}"""
C_OPEN_JS = r"""async (no)=>{await openView(no);for(let i=0;i<60;i++){await new Promise(r=>setTimeout(r,100));if(!HASBOOK||QUID===String(qk(no)))break}
  try{setTool('view')}catch(e){}await new Promise(r=>setTimeout(r,300));return VNO}"""
# 근거 넣기(앱 데이터 함수 · 지어낸 글 · 1 칸 = 트리거) — g3Push 와 같은 꼴
C_SEED_JS = r"""async ([no,t])=>{const r=rec(no),u=GGU(r);const list=ggOf(u).slice();list.forEach((x,n)=>{if(x&&x.i!==n+1)x.i=n+1});
 const g={k:ggNewKey('g_'),i:list.length+1,t:t,ok:ggMarkNow(no),ts:Date.now(),cs:[],f:'t'};list.push(g);await ggSaveList(u,list);try{ggRepaint(u)}catch(e){}return {uid:u,k:g.k}}"""
# 보이는 요소 하나 — 자리 · 가운데 맨 위 요소가 그것인가(hit)
C_EL_JS = r"""([q,scroll])=>{const vis=e=>{const r=e.getBoundingClientRect(),cs=getComputedStyle(e);return r.width>0&&r.height>0&&cs.visibility!=='hidden'&&cs.display!=='none'};
 const e=[...document.querySelectorAll(q)].filter(vis)[0];if(!e)return null;if(scroll)try{e.scrollIntoView({block:'center',inline:'nearest'})}catch(_){}
 const r=e.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2,t=document.elementFromPoint(cx,cy);
 return {cx,cy,w:r.width,h:r.height,hit:!!t&&(t===e||e.contains(t)),inv:cx>=0&&cy>=0&&cx<=innerWidth&&cy<=innerHeight}}"""
SCROLL_JS = r"""(q)=>{const e=document.querySelector(q);if(!e)return false;try{e.scrollIntoView({block:'center',inline:'nearest'})}catch(_){}return true}"""
# 찾기 목록(보이는 .g3sug) — 줄 수 · 쓴 문항 수(.g3n) · uid 칩 수 · want 글 줄 자리
ROWS_JS = r"""([w,want])=>{const N=window.__cfN;const sug=[...document.querySelectorAll('.g3sug:not(.hide)')].find(s=>s.getBoundingClientRect().height>0);
 if(!sug)return {sug:false,n:0,idx:null};const L=[...sug.querySelectorAll('.g3s')];let idx=null;
 L.forEach((e,i)=>{const b=e.querySelector('.bt1');if(idx===null&&want!=null&&b&&N(b.textContent)===N(want))idx=i});
 const out={sug:true,n:L.length,idx,g3n:L.map(e=>{const g=e.querySelector('.g3n');return g?+g.textContent:null}),chips:L.map(e=>e.querySelectorAll('.g3so .g3ttl').length),
  wrows:L.filter(e=>N(e.textContent).indexOf(w)>=0).length};
 if(idx!==null){const e=L[idx];try{e.scrollIntoView({block:'nearest'})}catch(_){}const b=e.querySelector('.bt1')||e,r=b.getBoundingClientRect();
  out.cx=r.left+Math.min(r.width/2,30);out.cy=r.top+r.height/2;const t=document.elementFromPoint(out.cx,out.cy);out.hit=!!t&&e.contains(t)}
 return out}"""
# C7 — 2 칸 찾기 목록 첫 줄(블록 줄 = .sec 있음) · 고를 ref · 블록 글 md5
ROWS7_JS = r"""()=>{const H=window.__cfH;const sug=[...document.querySelectorAll('.g3sug:not(.hide)')].find(s=>s.getBoundingClientRect().height>0);if(!sug)return {n:0};
 const L=[...sug.querySelectorAll('.g3s')],l=sug.__l||[],x=l[0];
 const out={n:L.length,kind:L[0]?(L[0].querySelector('.sec')?'blk':'txt'):null,ref5:x&&x.ref?H(String(x.ref)):null,bt5:x&&x.b?H(x.b.text):null,l5:H(l.map(y=>y.ref||'').join(','))};
 if(L[0]){try{L[0].scrollIntoView({block:'nearest'})}catch(_){}const r=L[0].getBoundingClientRect();out.cx=r.left+Math.min(r.width/2,60);out.cy=r.top+Math.min(r.height/2,10);
  const t=document.elementFromPoint(out.cx,out.cy);out.hit=!!t&&L[0].contains(t)}return out}"""
FIELD_VAL_JS = r"""(q)=>{const e=document.querySelector(q);return e?String(e.value):null}"""
FIELD_CLR_JS = r"""(q)=>{const e=document.querySelector(q);if(!e)return null;e.value='';return true}"""
# 길게 누른 뒤 — 고치기 칸 · 초점
ED_JS = r"""()=>{const ta=document.querySelector('.g3ed textarea');return {ed:!!ta,focus:!!ta&&document.activeElement===ta}}"""
ED_TAIL_JS = r"""(a)=>{const ta=document.querySelector('.g3ed textarea');return ta?window.__cfN(ta.value).endsWith(window.__cfN(a)):null}"""
# 지우기 창 — 같은 근거 글 두 가지(앱 글 · 실제 근거 글 아님)
DLG_JS = r"""()=>{const S=[...document.querySelectorAll('.sheet')].filter(s=>s.querySelector('#ggdGo'));const s=S[S.length-1];if(!s)return {dlg:false};const t=window.__cfN(s.textContent);
 const m=/같이 쓰는 문항 (\d+)개/.exec(t);return {dlg:true,share:m?+m[1]:null,share1:t.indexOf('같이 쓰는 문항 1개')>=0,only:t.indexOf('이 문항에서만 뺍니다')>=0}}"""
# 상태 — A 항목 · B 항목(src 가 A 를 가리키나 · t · ggFlat md5) · 저장 통(kv gg) · B 화면 줄
STATE_JS = r"""async ([uA,kA,uB,w])=>{const H=window.__cfH,N=window.__cfN,root=uA+'|'+kA;
 const it=x=>({k:x.k,src:x.src?(x.src===root?'A':'other'):null,t:H(x.t),fl:H(ggFlat(x)),f:x.f||null,ref:!!x.ref,w:N(ggFlat(x)).indexOf(w)>=0||N(x.t).indexOf(w)>=0});
 const a=ggItem(uA,kA);let stB=null,stA=null;
 try{const v=await get('kv','gg');stB=((v&&v[uB])||[]).map(x=>({src:x.src?(x.src===root?'A':'other'):null,t:H(x.t)}));const sa=((v&&v[uA])||[]).find(x=>x&&x.k===kA);stA=sa?H(sa.t):null}catch(e){stB='ERR'}
 const scr=[...document.querySelectorAll('.g3it.g3r[data-g3k^="'+uB+'|"]')].map(r=>{const t=r.querySelector('.g3tx'),b=t?t.getBoundingClientRect():null;return {t:H(t?t.textContent:''),vis:!!b&&b.height>0}});
 return {nA:ggOf(uA).length,A:a?it(a):null,stA,nB:ggOf(uB).length,B:ggOf(uB).map(it),stB,scrB:scr,VNO}}"""
# C7 — 문항 항목(칸 · ref · src · t · ggFlat · 블록 글)
ITEMS_JS = r"""(u)=>{const H=window.__cfH;const blk=r=>{try{if(window.G3&&G3.blocks){const b=G3.blocks().find(b=>b.key===r);return b?H(b.text):null}}catch(e){}return null};
 return ggOf(u).map(x=>({f:x.f||null,ref5:x.ref?H(String(x.ref)):null,src:!!x.src,t5:H(x.t),fl5:H(ggFlat(x)),bt5:x.ref?blk(x.ref):null}))}"""

FIELD = '[data-ggbox="%s|qp-"] .ggrows .txt'


def elq(p, q, scroll=False):
    return p.ev(C_EL_JS, [q, bool(scroll)])


def click_q(p, q, wait=350, scroll=True):
    e = elq(p, q, scroll)
    if not e:
        return None
    p.click(e['cx'], e['cy'], wait)
    return e


def open_q(p, no):
    v = p.ev(C_OPEN_JS, no)
    p.wait(250)
    return v


def line_ready(p, uid):
    """근거 줄 보이게 — 물리 = ▾(#g3Fold · 문항 열 때마다 접힘) · 카드 층 = 줄을 화면 가운데로"""
    if not p.ev("HASBOOK"):
        if p.ev("()=>{const v=document.getElementById('view');return !!v&&v.classList.contains('g3off')}"):
            click_q(p, '#g3Fold', 300, scroll=False)
        return 'phys:' + ('off' if p.ev("document.getElementById('view').classList.contains('g3off')") else 'on')
    p.ev(SCROLL_JS, '[data-ggbox="%s|qp-"]' % uid)
    p.wait(200)
    return 'card'


def unfold_list(p, uid):
    """카드 층 적은 근거 목록 ▸ → ▾(문항 열 때마다 접힘)"""
    if not p.ev("HASBOOK"):
        return None
    if p.ev("()=>{const c=document.getElementById('card');return !!c&&c.classList.contains('g3fold')}"):
        e = click_q(p, '[data-ggbox="%s|qp-"] .g3fb' % uid, 300)
        return 'clicked' if e else 'no-fb'
    return 'open'


def clear_field(p, uid, word):
    """찾던 낱말 지우기(칸을 떠날 때 저절로 적히지 않게) — 뒤로 지움 · 남으면 비움"""
    q = FIELD % uid
    for _ in range(len(word) + 2):
        p.pg.keyboard.press('Backspace')
    p.wait(150)
    v = p.ev(FIELD_VAL_JS, q)
    if v:
        p.ev(FIELD_CLR_JS, q)
        return 'js'
    return 'kb'


def search(p, uid, word, want=None, pick=True):
    """트리거 칸 누름(마우스) → 낱말 침(자판) → 목록 잼 → want 글 줄 누름(마우스) · 안 고르면 칸 비움"""
    r = {'field': False}
    f = elq(p, FIELD % uid, scroll=True)
    if not f:
        return r
    r['field'] = True
    r['fhit'] = f['hit']
    p.click(f['cx'], f['cy'], 250)
    p.pg.keyboard.type(word)
    p.wait(500)
    m = p.ev(ROWS_JS, [word, want])
    r.update({k: m.get(k) for k in ('sug', 'n', 'idx', 'g3n', 'chips', 'wrows', 'hit')})
    if pick and m.get('idx') is not None and m.get('cx') is not None:
        p.click(m['cx'], m['cy'], 700)
        r['clicked'] = True
    else:
        r['clear'] = clear_field(p, uid, word)
        p.wait(200)
    return r


def edit_row(p, uid, k, add):
    """줄 길게 누름(마우스 900ms) → 고치기 칸 · 끝에 글 더함(자판) · Enter"""
    r = {'row': False}
    if not k:
        return r
    e = elq(p, '[data-g3k="%s|%s|t"] .g3tx' % (uid, k), scroll=True)
    if not e:
        return r
    r['row'] = True
    r['hit'] = e['hit']
    p.long_press(e['cx'], e['cy'], ms=900, wait=300)
    st = p.ev(ED_JS)
    r.update(st)
    if st['ed'] and not st['focus']:
        q = elq(p, '.g3ed textarea')
        if q:
            p.click(q['cx'] + q['w'] / 2 - 4, q['cy'], 200)
            r['refocus'] = p.ev(ED_JS)['focus']
    if st['ed']:
        p.pg.keyboard.type(add)
        p.wait(150)
        r['tail'] = p.ev(ED_TAIL_JS, add)
        p.pg.keyboard.press('Enter')
        p.wait(800)
        r['closed'] = not p.ev("!!document.querySelector('.g3ed')")
    return r


def delete_row(p, uid, k):
    """줄 ✕ 누름(마우스) → 지우기 창 글 잼 → 「지우기」 누름(마우스)"""
    r = {'x': False}
    if not k:
        return r
    e = elq(p, '[data-g3k="%s|%s|t"] .g3del' % (uid, k), scroll=True)
    if not e:
        return r
    r['x'] = True
    p.click(e['cx'], e['cy'], 500)
    r.update(p.ev(DLG_JS))
    g = elq(p, '.sheet #ggdGo')
    if g:
        p.click(g['cx'], g['cy'], 900)
        r['go'] = True
    return r


def st_(p, uA, kA, uB):
    return p.ev(STATE_JS, [uA, kA, uB, W_])


def flow_C7(p, noD, uD):
    """2 칸 — 「근거」 글자 누름(마우스) → 칸 고르는 작은 창의 「공식·개념」 누름 → 「1」 침 → 첫 줄 누름 → 항목 잼"""
    o = {}
    open_q(p, noD)
    o['line'] = line_ready(p, uD)
    lb = elq(p, '[data-ggbox="%s|qp-"] .ggline .lb' % uD, scroll=True)
    o['lb'] = bool(lb)
    if lb:
        p.click(lb['cx'], lb['cy'], 450)
    tg = elq(p, '#tyPop [data-g3sel$="|c"]')
    o['tg'] = bool(tg)
    if tg:
        p.click(tg['cx'], tg['cy'], 450)
        o['field'] = p.ev("(u)=>{const e=document.querySelector('[data-ggbox=\"'+u+'|qp-\"] .g3f');return e?e.dataset.g3f:null}", uD)
        f = elq(p, FIELD % uD, scroll=True)
        if f:
            p.click(f['cx'], f['cy'], 250)
            p.pg.keyboard.type(C7Q)
            p.wait(500)
            m = p.ev(ROWS7_JS)
            o.update({k: m.get(k) for k in ('n', 'kind', 'ref5', 'bt5', 'l5', 'hit')})
            if m.get('cx') is not None:
                p.click(m['cx'], m['cy'], 700)
                o['clicked'] = True
            else:
                o['clear'] = clear_field(p, uD, C7Q)
    else:
        o['field'] = p.ev("(u)=>{const e=document.querySelector('[data-ggbox=\"'+u+'|qp-\"] .g3f');return e?e.dataset.g3f:null}", uD)
        p.ev("(()=>{const o=document.getElementById('tyPop');if(o){if(o.__close)o.__close();else o.remove()}return 1})()")
    p.wait(300)
    o['items'] = p.ev(ITEMS_JS, uD)
    return o


def flow_C(br, eng, src, subj):
    """관문 C 한 과목 — 제 쪽(PC 1100×800 마우스)을 열고 잰 값 dict(실제 글 없음)"""
    o = {'subj': subj, 'eng': eng}
    p = None
    try:
        p = JG.Pg_PP(br, eng, 'cfC-%s-%s-%s' % (_C_h6(src), eng, subj), src, subj, (1100, 800), touch=False, remote=JG.Remote())
        p.wait(1500)
        o['help'] = p.ev(HELP_JS) == h8('abc')
        o['HASBOOK'] = p.ev("HASBOOK")
        nos = p.ev(PICKQ_JS, 4)
        o['nos'] = nos
        if not nos or len(nos) < 4:
            o['ERR'] = '문항 4 개 못 고름'
            return o
        noA, noB, noC, noD = nos
        uA, uB, uC, uD = p.ev(UIDS_JS, nos)
        o['uids'] = [uA, uB, uC, uD]
        o['PRE'] = p.ev(PRE_JS, W_)
        sd = p.ev(C_SEED_JS, [noA, T0])
        kA = sd['k']
        o['kA'] = kA
        o['seed'] = st_(p, uA, kA, uB)['A']
    except Exception:
        o['ERR'] = traceback.format_exc()[-700:]
        if p:
            p.close()
        return o

    def cell(name, fn):
        try:
            fn()
        except Exception:
            o.setdefault(name, {})['ERR'] = traceback.format_exc()[-600:]

    kB = [None]

    def c1():
        open_q(p, noB)
        r = {'line': line_ready(p, uB)}
        r['ui'] = search(p, uB, W_, T0)
        s = st_(p, uA, kA, uB)
        kB[0] = s['B'][0]['k'] if s['B'] else None
        r.update({'nB': s['nB'], 'B': [{k: x[k] for k in ('src', 't', 'fl', 'f')} for x in s['B']], 'scrB': len(s['scrB'])})
        o['C1'] = r

    def c2():
        r = {'list': unfold_list(p, uB)}
        r['ui'] = edit_row(p, uB, kB[0], A2)
        s = st_(p, uA, kA, uB)
        r.update({'nB': s['nB'], 'scrB': len(s['scrB']), 'A_t': (s['A'] or {}).get('t'), 'B': [{k: x[k] for k in ('src', 't', 'fl')} for x in s['B']]})
        o['C2'] = r

    def c3():
        open_q(p, noA)
        r = {'line': line_ready(p, uA), 'list': unfold_list(p, uA)}
        r['ui'] = edit_row(p, uA, kA, A3)
        open_q(p, noB)
        line_ready(p, uB)
        unfold_list(p, uB)
        s = st_(p, uA, kA, uB)
        r.update({'A_t': (s['A'] or {}).get('t'), 'stA': s['stA'], 'nB': s['nB'], 'B': [{k: x[k] for k in ('src', 't', 'fl')} for x in s['B']],
                  'scrB': s['scrB'], 'stB': s['stB']})
        o['C3'] = r

    def c4():
        open_q(p, noC)
        r = {'line': line_ready(p, uC)}
        r['ui'] = search(p, uC, W_, None, pick=False)
        p.wait(300)
        r['nC'] = p.ev("(u)=>ggOf(u).length", uC)
        o['C4'] = r

    def c5():
        open_q(p, noA)
        r = {'line': line_ready(p, uA), 'list': unfold_list(p, uA)}
        r['ui'] = delete_row(p, uA, kA)
        s = st_(p, uA, kA, uB)
        r.update({'A_has': s['A'] is not None, 'nA': s['nA'], 'nB': s['nB'], 'B_src': [x['src'] for x in s['B']], 'B_w': sum(1 for x in s['B'] if x['w']),
                  'stB_n': (len(s['stB']) if isinstance(s['stB'], list) else s['stB'])})
        o['C5'] = r

    def c6():
        sd6 = p.ev(C_SEED_JS, [noA, T6])
        k6 = sd6['k']
        open_q(p, noB)
        r = {'k6': k6, 'line': line_ready(p, uB)}
        r['pick'] = search(p, uB, W_, T6)
        s0 = st_(p, uA, k6, uB)
        cand = [x for x in s0['B'] if x['src'] == 'A'] or [x for x in s0['B'] if x['fl'] == h8(T6)]
        kB6 = cand[0]['k'] if cand else None
        r['linked'] = [x['src'] for x in s0['B']]
        r['list'] = unfold_list(p, uB)
        r['ui'] = delete_row(p, uB, kB6)
        s = st_(p, uA, k6, uB)
        r.update({'A_has': s['A'] is not None, 'A_t': (s['A'] or {}).get('t'), 'nA': s['nA'], 'nB': s['nB'],
                  'B_T6': sum(1 for x in s['B'] if x['src'] == 'A' or x['fl'] == h8(T6))})
        o['C6'] = r

    def c7():
        o['C7'] = flow_C7(p, noD, uD)

    for name, fn in (('C1', c1), ('C2', c2), ('C3', c3), ('C4', c4), ('C5', c5), ('C6', c6), ('C7', c7)):
        cell(name, fn)
    try:
        o['errs'] = [e[:160] for e in (p.errs or [])][:4] + [str(e)[:160] for e in (p.ev('window.__err||[]') or [])][:4]
    except Exception:
        pass
    p.close()
    return o


# ── 판정 ──
def _g(o, *ks):
    for k in ks:
        if not isinstance(o, dict):
            return None
        o = o.get(k)
    return o


def _sig7(c7):
    if not isinstance(c7, dict):
        return None
    it = c7.get('items') or []
    return {'tg': c7.get('tg'), 'n': c7.get('n'), 'kind': c7.get('kind'), 'l5': c7.get('l5'), 'ref5': c7.get('ref5'), 'bt5': c7.get('bt5'),
            'items': [(x.get('f'), x.get('ref5'), x.get('src'), x.get('t5')) for x in it]}


def judge_C(o, base_o=None):
    """칸마다 (PASS?, 잰 값) — 같은 함수로 엔진 · 과목 · 새 판 / 바탕 · C7 = 바탕 값과 맞댐(base_o 없으면 절대 잣대)"""
    out = {}
    e1, e2, e3, e6 = h8(T0), h8(T0 + A2), h8(T0 + A2 + A3), h8(T6)
    pre_ok = _g(o, 'PRE', 'w_hits') == 0 and _g(o, 'seed', 't') == e1
    c = o.get('C1') or {}
    B = c.get('B') or []
    ok = pre_ok and c.get('nB') == 1 and c.get('scrB') == 1 and len(B) == 1 and B[0].get('src') == 'A' and B[0].get('fl') == e1
    out['C1'] = (bool(ok), {'nB': c.get('nB'), '화면 줄': c.get('scrB'), 'src=A uid|k': [x.get('src') for x in B], '찾기': _g(c, 'ui', 'n'), '누름': _g(c, 'ui', 'clicked'), 'ERR': c.get('ERR')})
    c = o.get('C2') or {}
    B = c.get('B') or []
    ok = c.get('nB') == 1 and c.get('scrB') == 1 and c.get('A_t') == e2 and len(B) == 1 and B[0].get('fl') == e2
    out['C2'] = (bool(ok), {'nB': c.get('nB'), '화면 줄': c.get('scrB'), 'A 새 글': c.get('A_t') == e2, 'B 새 글': bool(B) and B[0].get('fl') == e2,
                            '고치기 칸': _g(c, 'ui', 'ed'), '끝에 더함': _g(c, 'ui', 'tail'), 'ERR': c.get('ERR')})
    c = o.get('C3') or {}
    B = c.get('B') or []
    scr = c.get('scrB') or []
    stB = c.get('stB') if isinstance(c.get('stB'), list) else []
    ok = (c.get('A_t') == e3 and len(B) == 1 and B[0].get('fl') == e3 and B[0].get('t') == e3 and len(scr) == 1 and scr[0].get('t') == e3 and scr[0].get('vis')
          and len(stB) == 1 and stB[0].get('t') == e3)
    out['C3'] = (bool(ok), {'A': c.get('A_t') == e3, 'ggFlat(B)': bool(B) and B[0].get('fl') == e3, 'B t': bool(B) and B[0].get('t') == e3,
                            'B 화면': bool(scr) and scr[0].get('t') == e3, 'B 저장 t': bool(stB) and stB[0].get('t') == e3, '고치기 칸': _g(c, 'ui', 'ed'), 'ERR': c.get('ERR')})
    c = o.get('C4') or {}
    u = c.get('ui') or {}
    ok = u.get('n') == 1 and (u.get('g3n') or [None])[0] == 2 and c.get('nC') == 0
    out['C4'] = (bool(ok), {'줄': u.get('n'), '쓴 문항': u.get('g3n'), 'uid 칩': u.get('chips'), 'C 근거 수': c.get('nC'), 'ERR': c.get('ERR')})
    c = o.get('C5') or {}
    u = c.get('ui') or {}
    ok = u.get('share1') is True and u.get('go') and c.get('A_has') is False and c.get('B_w') == 0 and 'A' not in (c.get('B_src') or [])
    out['C5'] = (bool(ok), {'✕': u.get('x'), '같이 쓰는 문항 1개': u.get('share1'), '같이 N': u.get('share'), 'A 남음': c.get('A_has'), 'B 남은 같은 근거': c.get('B_w'),
                            'ERR': c.get('ERR')})
    c = o.get('C6') or {}
    u = c.get('ui') or {}
    ok = (u.get('only') is True and u.get('go') and 'A' in (c.get('linked') or []) and c.get('A_has') is True and c.get('A_t') == e6 and c.get('B_T6') == 0)
    out['C6'] = (bool(ok), {'넣음(src=A)': c.get('linked'), '이 문항에서만 뺍니다': u.get('only'), 'A 그대로': c.get('A_has') and c.get('A_t') == e6, 'B 남은 것': c.get('B_T6'),
                            'ERR': c.get('ERR')})
    c = o.get('C7') or {}
    s = _sig7(c)
    it = c.get('items') or []
    no_src = not any(x.get('src') for x in it)
    if base_o is not None:
        bs = _sig7(base_o.get('C7'))
        ok = s is not None and bs is not None and s == bs and no_src and not c.get('ERR')
        how = '바탕 값과 맞댐'
    else:
        refs = [x for x in it if x.get('ref5')]
        if c.get('tg'):   # 2 칸 고르는 길이 있음(물리) — 블록 줄 → ref 항목 하나 · src 없음 · 글 = 블록 글
            ok = c.get('kind') == 'blk' and len(refs) == 1 and refs[0].get('t5') == refs[0].get('bt5') == c.get('bt5') and refs[0].get('fl5') == refs[0].get('t5') and no_src
        else:              # 카드 층 — 2 칸 고르는 길 없음 · ref 항목 0
            ok = len(refs) == 0 and no_src
        ok = ok and not c.get('ERR')
        how = '절대 잣대(바탕 판정)'
    out['C7'] = (bool(ok), {'가름': how, '2칸 고름': c.get('tg'), '목록': c.get('n'), '줄 꼴': c.get('kind'), '항목': [(x.get('f'), bool(x.get('ref5')), x.get('src')) for x in it],
                            'ERR': c.get('ERR')})
    return out


NAMES_C = {
    'C1': 'B 트리거 칸에 A 낱말 → 찾은 줄 마우스 누름 → B 1 줄 · src = A uid|k',
    'C2': 'B 줄 길게 눌러 끝에 글 더함 · Enter → B 1 줄 · A 글 = 새 글',
    'C3': 'A 쪽에서 고침 → ggFlat(B) · B 화면 · B t(메모리 · 저장) = 새 글',
    'C4': '셋째 문항에서 같은 낱말 → 한 줄 · 쓴 문항 2',
    'C5': 'A ✕ → 「같이 쓰는 문항 1개」 → 지우기 → A · B 둘 다 없음',
    'C6': '다시 넣고 B ✕ → 「이 문항에서만 뺍니다」 → B 만 빠짐 · A 그대로',
    'C7': '2 칸(공식·개념 · 블록 ref) = 바탕과 같음(바탕 값으로 가름)',
}



# ══ 무리 DE ══════════════════════════════════════════════════════════════════════════════
# 관문 D(암기카드 창 처음 1/3) · E(목차 서랍 = 문항을 골라도 안 접힘) — _harness_jagwa_cardfit.py 에 들어갈 몫(개발 사본)
# 칸: D_PC · D_PH(과목마다) · E384 · E600 · E820 · E1100(과목마다)
# 잰 값 = 숫자 · 참거짓 · 요소 꼴(id/class)만 — 카드 글 · 교재 글 · 검색 낱말(코드)은 담지 않음(낱말 = 길이 · md5 앞 8 자)
import hashlib
import hashlib as _hl
_DE_h6 = lambda s: _hl.md5(s.encode('utf-8')).hexdigest()[:6]   # 판마다 다른 tag(serve_PP 는 tag 로 서버를 붙잡아 둠 — 같은 tag 면 바탕 판이 새 판 앱을 받음)
import traceback
import _qa_jagwa_common as JG

DEV_D = {'PC': ((1100, 800), False), 'PH': ((384, 740), True)}
DEV_E = {384: ((384, 740), True), 600: ((600, 900), True), 820: ((820, 1180), True), 1100: ((1100, 800), False)}

# ───────────────────────── JS ─────────────────────────
DE_OPEN_JS = r"""async (no)=>{await openView(no);for(let i=0;i<60;i++){await new Promise(r=>setTimeout(r,100));if(!HASBOOK||QUID===String(qk(no)))break}
  try{setTool('view')}catch(e){}await new Promise(r=>setTimeout(r,300));return {VNO,quid:HASBOOK?QUID===String(qk(no)):null}}"""
# 시험 문항 — 카드 층은 조각(배경)이 있는 문항 먼저(지학) · 없으면 첫 문항
PICK_D_JS = r"""()=>{const ok=r=>!(typeof isC==='function'&&isC(r));let no=null,jg=false;
  if(typeof jogakOf==='function'){for(const r of DATA){if(!ok(r))continue;let j=null;try{j=jogakOf(r)}catch(e){}if(j){no=r[F.NO];jg=true;break}}}
  if(no==null){const r=DATA.find(ok);no=r?r[F.NO]:null}return {no,jg}}"""
# 지어낸 획 하나(1/1000 정수) — 그 문항 카드 통(MC · kv/mcard)에 넣고 저장
SEED_D_JS = r"""async (no)=>{const k=String(qk(no));MC[k]={w:300,h:180,s:[{c:'#16181B',w:2,hl:0,p:[120,210,260,330,410,450,590,520,760,610]}]};await saveMC();return MC[k].s.map(s=>s.p.slice())}"""
MC_JS = r"""async (no)=>{const k=String(qk(no));const m=(typeof MC!=='undefined'&&MC[k])?MC[k].s.map(s=>s.p.slice()):null;let d=null;
  try{const v=await get('kv','mcard');d=(v&&v[k])?v[k].s.map(s=>s.p.slice()):null}catch(e){d='ERR'}return {m,d}}"""
# 🃏 단추 — 화면 안 · 그 자리 맨 위가 단추(아니면 줄 안에서 보이게 굴린 뒤 다시 잼)
BTN_JS = r"""(id)=>{const e=document.getElementById(id);if(!e)return null;let r;
  const ok=()=>{r=e.getBoundingClientRect();const cx=r.left+r.width/2,cy=r.top+r.height/2;if(!(r.width>0&&r.height>0&&cx>=0&&cy>=0&&cx<innerWidth&&cy<innerHeight))return false;
    const h=document.elementFromPoint(cx,cy);return !!h&&(h===e||e.contains(h))};
  let moved=false;if(!ok()){try{e.scrollIntoView({block:'nearest',inline:'center'})}catch(_){}moved=true}
  const fine=ok();return {cx:r.left+r.width/2,cy:r.top+r.height/2,w:+r.width.toFixed(1),h:+r.height.toFixed(1),ok:fine,moved}}"""
# 암기카드 창 잼
MCW_JS = r"""()=>{const b=document.querySelector('.sheet.mcwin');if(!b)return {open:false};const pn=b.querySelector('.panel');
  const R=e=>{if(!e)return null;const r=e.getBoundingClientRect();return {x:+r.left.toFixed(1),y:+r.top.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1),r:+r.right.toFixed(1),b:+r.bottom.toFixed(1)}};
  const scr=[];[pn,...pn.querySelectorAll('*')].forEach(e=>{const cs=getComputedStyle(e);if(/(auto|scroll)/.test(cs.overflowY)&&e.scrollHeight>e.clientHeight+1)scr.push({c:(e.className&&String(e.className).split(' ')[0])||e.tagName,sh:e.scrollHeight,ch:e.clientHeight})});
  const hd=pn.querySelector('.mch'),x=pn.querySelector('#mcX'),g=pn.querySelector('.twgrip'),bx=pn.querySelector('.mccv'),cv=pn.querySelector('#mcc');
  const fs=q=>{const e=pn.querySelector(q);return e?parseFloat(getComputedStyle(e).fontSize):null};
  let ls=null;try{ls=localStorage.getItem('jagwa.win.mcard')}catch(e){}
  return {open:true,iw:innerWidth,ih:innerHeight,pn:R(pn),sh:pn.scrollHeight,ch:pn.clientHeight,ovy:getComputedStyle(pn).overflowY,scr,bx:R(bx),cv:R(cv),hd:R(hd),x:R(x),grip:R(g),
    float:pn.classList.contains('float'),fs:{h:fs('.mch'),n:fs('.mcnote'),t:fs('.mct')},bxs:bx?{w:bx.style.width,h:bx.style.height}:null,
    win:(typeof WIN!=='undefined'&&WIN.mcard)?{w:Math.round(WIN.mcard.w),h:Math.round(WIN.mcard.h)}:null,ls}}"""
# 머리 끌 자리(단추 밖) · 모서리 가운데
HDPT_JS = r"""()=>{const b=document.querySelector('.sheet.mcwin');if(!b)return null;const h=b.querySelector('.mch'),r=h.getBoundingClientRect();
  for(let x=r.left+8;x<r.right-30;x+=6){const y=r.top+r.height/2,t=document.elementFromPoint(x,y);if(t&&h.contains(t)&&!t.closest('button,a,input'))return [x,y]}return null}"""
GRIP_JS = r"""()=>{const g=document.querySelector('.sheet.mcwin .twgrip');if(!g)return null;const r=g.getBoundingClientRect();
  for(const [fx,fy] of [[.5,.5],[.7,.7],[.3,.3],[.7,.3],[.3,.7],[.85,.85]]){const x=r.left+r.width*fx,y=r.top+r.height*fy;if(x<0||y<0||x>=innerWidth||y>=innerHeight)continue;const t=document.elementFromPoint(x,y);if(t&&(t===g||g.contains(t)))return {x,y,hit:true}}
  return {x:r.left+r.width/2,y:r.top+r.height/2,hit:false}}"""
CVPT_JS = r"""([u,v])=>{const c=document.querySelector('.sheet.mcwin #mcc');if(!c)return null;const r=c.getBoundingClientRect();return [r.left+u*r.width,r.top+v*r.height]}"""
# 펜 획(WebKit = 그 자리 요소에 합성 pen 포인터)
DE_PENSYN_JS = r"""(pts)=>{const t=document.elementFromPoint(pts[0][0],pts[0][1]);if(!t)return null;
  const f=(ty,x,y,b)=>t.dispatchEvent(new PointerEvent(ty,{bubbles:true,cancelable:true,composed:true,pointerId:41,pointerType:'pen',isPrimary:true,clientX:x,clientY:y,button:0,buttons:b,pressure:b?0.5:0}));
  f('pointerdown',pts[0][0],pts[0][1],1);for(let i=1;i<pts.length;i++)f('pointermove',pts[i][0],pts[i][1],1);f('pointerup',pts[pts.length-1][0],pts[pts.length-1][1],0);return t.id||t.tagName}"""
# 손가락 끌기(WebKit — Playwright WebKit 은 터치 끌기가 없다 → 그 자리 요소에 합성 touch 포인터 · 받은 요소에 이어 보냄 = 앱의 setPointerCapture 와 같은 꼴)
TDRAGSYN_JS = r"""(pts)=>{const t=document.elementFromPoint(pts[0][0],pts[0][1]);if(!t)return null;
  const f=(ty,x,y,b)=>t.dispatchEvent(new PointerEvent(ty,{bubbles:true,cancelable:true,composed:true,pointerId:57,pointerType:'touch',isPrimary:true,clientX:x,clientY:y,button:0,buttons:b,width:12,height:12,pressure:b?0.5:0}));
  f('pointerdown',pts[0][0],pts[0][1],1);for(let i=1;i<pts.length;i++)f('pointermove',pts[i][0],pts[i][1],1);f('pointerup',pts[pts.length-1][0],pts[pts.length-1][1],0);
  return (t.className&&String(t.className).split(' ')[0])||t.id||t.tagName}"""
# 밀기(WebKit) — 앱의 밀기 = document touchstart/touchend(capture) · e.touches / e.changedTouches 만 읽음 → 같은 꼴 합성 터치 이벤트
SWIPESYN_JS = r"""([x0,y0,x1,y1])=>{const t=document.elementFromPoint(x0,y0);if(!t)return null;
  const mk=(ty,x,y,on)=>{const e=new Event(ty,{bubbles:true,cancelable:true,composed:true});const pt={clientX:x,clientY:y,pageX:x,pageY:y,screenX:x,screenY:y,identifier:3,target:t};
    Object.defineProperty(e,'touches',{value:on?[pt]:[]});Object.defineProperty(e,'targetTouches',{value:on?[pt]:[]});Object.defineProperty(e,'changedTouches',{value:[pt]});return e};
  t.dispatchEvent(mk('touchstart',x0,y0,true));t.dispatchEvent(mk('touchmove',(x0+x1)/2,(y0+y1)/2,true));t.dispatchEvent(mk('touchend',x1,y1,false));
  return (t.className&&String(t.className).split(' ')[0])||t.id||t.tagName}"""

# ── E ──
E_ST_JS = r"""()=>{const D=document.getElementById('navdr');const r=D?D.getBoundingClientRect():null;const v=document.getElementById('view');
  return {dw:r?+r.width.toFixed(1):null,fold:D?D.classList.contains('fold'):null,res:D?D.classList.contains('ndres'):null,dz:D?getComputedStyle(D).zIndex:null,
    vis:v?!v.classList.contains('hide'):null,win:v?v.classList.contains('win'):null,VNO:(typeof VNO!=='undefined')?VNO:null,
    pins:[...document.querySelectorAll('.vpin')].map(x=>+x.dataset.no),g3:!!document.getElementById('g3Pop'),ns:!!document.getElementById('nsPop'),
    rows:document.querySelectorAll('#ndList .ndrow').length,ox:document.querySelectorAll('#ndList .ndox').length,iw:innerWidth,ih:innerHeight}}"""
# 서랍 줄 하나 — part = ndno | ndt | ox · 화면 안 · 그 자리 맨 위가 그 칸(다른 창에 안 가림)
DE_ROW_JS = r"""([part,skip])=>{const L=[...document.querySelectorAll('#ndList .ndrow')];let cov=0;
  for(const x of L){const no=+x.dataset.no;if(!no||(skip||[]).indexOf(no)>=0||x.classList.contains('ndoff'))continue;
    const e=part==='ndno'?x.querySelector('.ndno'):part==='ndt'?x.querySelector('.ndt'):x.querySelector('.ndox');if(!e)continue;
    const r=e.getBoundingClientRect();if(!(r.width>2&&r.height>2))continue;
    const cx=part==='ndt'?r.left+Math.min(14,r.width/3):r.left+r.width/2,cy=r.top+r.height/2;
    if(cx<0||cy<4||cx>=innerWidth||cy>=innerHeight-4)continue;
    const h=document.elementFromPoint(cx,cy);if(!h||!(h===e||e.contains(h))){if(h&&!h.closest('#navdr'))cov++;continue}
    if(part!=='ox'&&h.closest('.ndox,.ndc,.ied,button,input'))continue;
    return {no,cx,cy,cov}}
  return {no:null,cov}}"""
# 누른 뒤 — 서랍 폭 · 접힘 · 열린 창(번호/제목/검색 = #view(VNO) 또는 그 문항 .vpin · O△X = #g3Pop) · 열린 창이 서랍 위인지
AFTER_JS = r"""([kind,no])=>{const D=document.getElementById('navdr'),dr=D.getBoundingClientRect(),v=document.getElementById('view');
  const vis=e=>!!e&&e.isConnected&&getComputedStyle(e).display!=='none'&&getComputedStyle(e).visibility!=='hidden'&&e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0;
  let W=null;
  if(kind==='ox'){const g=document.getElementById('g3Pop');if(vis(g))W=g}
  else{const pin=[...document.querySelectorAll('.vpin')].find(x=>+x.dataset.no===+no&&vis(x));
    if(v&&!v.classList.contains('hide')&&+VNO===+no&&vis(v))W=v;else if(pin)W=pin}
  const R=r=>r?[+r.left.toFixed(1),+r.top.toFixed(1),+r.width.toFixed(1),+r.height.toFixed(1)]:null;
  const out={dw:+dr.width.toFixed(1),fold:D.classList.contains('fold'),dz:getComputedStyle(D).zIndex,dr:R(dr),VNO:+VNO,vis:v?!v.classList.contains('hide'):null,vwin:v?v.classList.contains('win'):null,
    pins:[...document.querySelectorAll('.vpin')].map(x=>+x.dataset.no),opened:!!W,wk:W?(W.id||String(W.className).split(' ')[0]):null};
  if(!W)return out;
  const P=(W.classList&&W.classList.contains('sheet')&&W.querySelector(':scope>.panel'))||W;   /* .vpin = 화면 덮는 틀(누름 통과) 안의 .panel 이 창 */
  const a=P.getBoundingClientRect();out.wr=R(a);
  const top=el=>{while(el&&el.parentElement&&el.parentElement!==document.body)el=el.parentElement;return el};
  const z=el=>{const s=getComputedStyle(el).zIndex;return s==='auto'?0:+s};
  out.zW=z(top(W));out.zD=z(D);
  const x0=Math.max(a.left,dr.left,0),y0=Math.max(a.top,dr.top,0),x1=Math.min(a.right,dr.right,innerWidth),y1=Math.min(a.bottom,dr.bottom,innerHeight);
  let n=0,inW=0,inD=0;const oth={};
  if(x1-x0>4&&y1-y0>4){for(let i=1;i<=3;i++)for(let j=1;j<=3;j++){const x=x0+(x1-x0)*i/4,y=y0+(y1-y0)*j/4,h=document.elementFromPoint(x,y);n++;
    if(h&&P.contains(h))inW++;else if(h&&D.contains(h))inD++;else{const k=h?(h.id||String(h.className).split(' ')[0]||h.tagName):'null';oth[k]=(oth[k]||0)+1}}}
  out.ov=n;out.inW=inW;out.inD=inD;out.oth=oth;
  out.above=n?(inD===0&&inW>0):true;   /* 겹치는 데가 없으면 서랍이 창을 가리지 않음(z 는 잰 값으로만 남김) */
  {const cx=Math.min(innerWidth-2,Math.max(1,a.left+a.width/2)),cy=Math.min(innerHeight-2,Math.max(1,a.top+Math.min(a.height/2,40))),h=document.elementFromPoint(cx,cy);out.ctr=!!h&&P.contains(h)}
  return out}"""
# 검색 낱말 — 물리 = 문항 번호(찾는 식 esPhysHit 「번호 같음」) · 카드 층 = 문항 코드(esHit 'id') · 지금 문항 말고 1~30 건 걸리는 첫 문항
QPICK_JS = r"""()=>{const cur=+VNO;const hit=(r,q)=>{try{return HASBOOK?!!esHit(r,q):!!esPhysHit(r,q)}catch(e){return false}};
  for(const r of DATA){const no=r[F.NO];if(no===cur)continue;if(typeof isC==='function'&&isC(r))continue;
    let q=null;try{q=HASBOOK?String((typeof codeShow==='function'?codeShow(r):r[F.CODE])||''):String(no)}catch(e){q=null}if(!q)continue;
    let n=0,other=0;for(const z of DATA){if(hit(z,q)){n++;if(z[F.NO]!==cur)other++}if(n>30)break}
    if(n>=1&&n<=30&&other>=1)return {q,no,n,kind:HASBOOK?'code':'no'}}
  return null}"""
NSROW_JS = r"""(skip)=>{const P=document.getElementById('nsPop');if(!P)return {pop:false};const L=[...P.querySelectorAll('.nsr')];
  for(const x of L){const no=+x.dataset.no;if((skip||[]).indexOf(no)>=0)continue;const e=x.querySelector('.nst')||x;const r=e.getBoundingClientRect();
    const cx=r.left+Math.min(12,r.width/3),cy=r.top+Math.min(r.height/2,9);if(cx<0||cy<0||cx>=innerWidth||cy>=innerHeight)continue;
    const h=document.elementFromPoint(cx,cy);if(!h||!x.contains(h)||h.closest('.nsn'))continue;return {pop:true,no,cx,cy,n:L.length}}
  return {pop:true,no:null,n:L.length}}"""
SCROLLOX_JS = r"""(skip)=>{const L=document.getElementById('ndList');const xs=[...document.querySelectorAll('#ndList .ndrow')].filter(x=>x.querySelector('.ndox')&&(skip||[]).indexOf(+x.dataset.no)<0&&!x.classList.contains('ndoff'));
  if(!xs.length)return false;const dr=document.getElementById('navdr').getBoundingClientRect();const x=xs[Math.min(2,xs.length-1)];x.scrollIntoView({block:'nearest'});
  const r=x.getBoundingClientRect();if(r.top<dr.top+60||r.bottom>Math.min(dr.bottom,innerHeight)-10)x.scrollIntoView({block:'center'});return true}"""
# 손잡이 띠에서 안 가린 자리(가운데부터 위아래로)
GRIPPT_JS = r"""()=>{const e=document.getElementById('ndGrip');if(!e)return null;const r=e.getBoundingClientRect();const cx=r.left+r.width/2;
  for(const f of [0.5,0.45,0.55,0.4,0.6,0.35,0.65,0.3,0.7,0.25,0.75,0.2,0.8]){const cy=r.top+r.height*f;if(cy<2||cy>innerHeight-2)continue;const h=document.elementFromPoint(cx,cy);
    if(h&&(h===e||e.contains(h)))return {cx,cy,ok:true,w:r.width,h:r.height,f}}
  return {cx,cy:r.top+r.height/2,ok:false,w:r.width,h:r.height}}"""
SWPT_JS = r"""()=>{const D=document.getElementById('navdr');if(!D)return null;const r=D.getBoundingClientRect();
  for(const fy of [0.5,0.4,0.6,0.3,0.7]){const x=r.left+r.width*0.75,y=r.top+r.height*fy,h=document.elementFromPoint(x,y);if(h&&D.contains(h)&&!h.closest('#ndGrip,input,textarea,select,canvas'))return [x,y]}return null}"""


# ───────────────────────── 손 ─────────────────────────
def _press(p, x, y, touch, wait=500):
    (p.tap if touch else p.click)(x, y, wait)


def _tdrag(p, pts, step_ms=16):
    """손가락 끌기 — Chromium = CDP 진짜 터치 · WebKit = 합성 touch 포인터"""
    if p.eng == 'webkit':
        return p.ev(TDRAGSYN_JS, [list(q) for q in pts])
    c = p._cdp()
    tp = lambda x, y: [{'x': x, 'y': y, 'radiusX': 6, 'radiusY': 6, 'id': 1}]
    c.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': tp(*pts[0])}); p.wait(step_ms)
    for x, y in pts[1:]:
        c.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': tp(x, y)}); p.wait(step_ms)
    c.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    return 'cdp'


def _mdrag(p, pts):
    m = p.pg.mouse
    m.move(*pts[0]); m.down()
    for x, y in pts[1:]:
        m.move(x, y, steps=2); p.wait(12)
    m.up()
    return 'mouse'


def _drag(p, touch, a, b, n=10):
    pts = [(a[0] + (b[0] - a[0]) * t / n, a[1] + (b[1] - a[1]) * t / n) for t in range(n + 1)]
    return _tdrag(p, pts) if touch else _mdrag(p, pts)


def _pen(p, pts):
    """펜 긋기 — Chromium = CDP pointerType pen · WebKit = 합성 pen 포인터"""
    if p.eng == 'webkit':
        return p.ev(DE_PENSYN_JS, [list(q) for q in pts])
    c = p._cdp()
    s = lambda ty, x, y, b, bs: c.send('Input.dispatchMouseEvent', {'type': ty, 'x': x, 'y': y, 'button': b, 'buttons': bs, 'clickCount': 1 if ty != 'mouseMoved' else 0, 'pointerType': 'pen', 'force': 0.5})
    s('mouseMoved', pts[0][0], pts[0][1], 'none', 0); s('mousePressed', pts[0][0], pts[0][1], 'left', 1)
    for x, y in pts[1:]:
        s('mouseMoved', x, y, 'left', 1); p.wait(12)
    s('mouseReleased', pts[-1][0], pts[-1][1], 'left', 0)
    return 'cdp'


def _until(p, js, arg=None, ms=4000, step=150):
    t = 0
    while t < ms:
        try:
            if p.ev(js, arg):
                return True
        except Exception:
            pass
        p.wait(step); t += step
    return False


def _safe(p, js, arg=None):
    try:
        return p.ev(js, arg)
    except Exception as e:
        return {'ERR': str(e)[:160]}


# ───────────────────────── D ─────────────────────────
def _card_press(p, touch, o, key):
    b = p.ev(BTN_JS, 'tCard'); o[key] = b
    if not b or not b.get('ok'):
        return False
    _press(p, b['cx'], b['cy'], touch, 900)
    return True


def _flow_D1(p, eng, subj, touch, o):
    pk = p.ev(PICK_D_JS); no = pk['no']; o['no'] = no; o['jg'] = pk['jg']; o['layer'] = p.ev("HASBOOK?'card':'pdf'")
    if no is None:
        o['why'] = '문항 없음'; return
    o['seed'] = p.ev(SEED_D_JS, no)
    p.ev("()=>{try{localStorage.removeItem('jagwa.win.mcard')}catch(e){}return 1}")
    o['open'] = p.ev(DE_OPEN_JS, no); p.wait(400)
    # ① 🃏 처음(기억된 크기 없음) — 진짜 누름
    if not _card_press(p, touch, o, 'btn1'):
        o['why'] = '🃏 못 누름'; return
    p.wait(400)
    m1 = p.ev(MCW_JS); o['m1'] = m1
    if not m1.get('open'):
        o['why'] = '창 안 뜸'; return
    o['mc1'] = p.ev(MC_JS, no)
    # ② 펜 획 하나(1/1000 자리) — 그은 자리 · 저장 값
    a = p.ev(CVPT_JS, [0.25, 0.35]); b = p.ev(CVPT_JS, [0.60, 0.60])
    if a and b:
        pts = [(a[0] + (b[0] - a[0]) * t / 10, a[1] + (b[1] - a[1]) * t / 10) for t in range(11)]
        o['pen_by'] = _pen(p, pts); p.wait(600)
        mc = p.ev(MC_JS, no); o['mc2'] = mc
        o['pen'] = mc['m'][-1] if mc and mc.get('m') and len(mc['m']) > len(o['seed']) else None
    # ③ 머리 끌어 위로(모서리 아래 틈 만들기) → 모서리 끌어 키움 — 진짜 마우스 · 손가락
    hp = p.ev(HDPT_JS); g = p.ev(GRIP_JS)
    o['hd_pt'] = hp; o['grip0'] = g
    if hp and g:   # 모서리를 못 누르는 판(바탕 물리 = 속 굴림 창 · 모서리가 가림)은 끌지 않음 — 엉뚱한 데를 끌어 창이 닫히지 않게
        need = max(0, g['y'] + 140 - m1['ih'])
        if need > 0:
            o['hd_by'] = _drag(p, touch, hp, (hp[0], hp[1] - need)); p.wait(400)
        o['m_mv'] = p.ev(MCW_JS)
        g = p.ev(GRIP_JS); o['grip1'] = g
        if g and g.get('hit'):
            dx = 80 if not touch else max(0, min(24, m1['iw'] - 6 - g['x']))
            o['grip_by'] = _drag(p, touch, (g['x'], g['y']), (g['x'] + dx, g['y'] + 120)); p.wait(600)
    m2 = p.ev(MCW_JS); o['m2'] = m2
    o['mc3'] = p.ev(MC_JS, no)
    # ④ ✕ 닫기 → 🃏 다시 — 진짜 누름
    x = p.ev(BTN_JS, 'mcX'); o['x'] = x
    if x and x.get('ok'):
        _press(p, x['cx'], x['cy'], touch, 600)
    o['closed'] = not p.ev(MCW_JS).get('open')
    if _card_press(p, touch, o, 'btn2'):
        p.wait(400)
    o['m3'] = p.ev(MCW_JS)
    o['mc4'] = p.ev(MC_JS, no)


def flow_D(br, eng, src, subj, devs=('PC', 'PH')):
    """D — 과목 하나 × 기기(PC 1100×800 마우스 · 폰 384×740 터치) · 기기마다 새 쪽"""
    out = {}
    for dv in devs:
        (W, H), touch = DEV_D[dv]
        o = {'dev': [W, H], 'touch': touch}; p = None
        try:
            p = JG.Pg_PP(br, eng, 'cfD-%s-%s-%s-%s' % (_DE_h6(src), eng, subj, dv), src, subj, (W, H), touch=touch, remote=JG.Remote())
            p.wait(1500)
            _flow_D1(p, eng, subj, touch, o)
        except Exception:
            o['ERR'] = traceback.format_exc()[-900:]
        finally:
            if p is not None:
                try:
                    o['perr'] = [e[:120] for e in (p.errs or [])[:3]]
                except Exception:
                    pass
                p.close()
        out[dv] = o
    return out


def _DE_near(a, b, tol=2.0):
    return a is not None and b is not None and abs(a - b) <= tol


def judge_D1(o):
    d = {}
    if o.get('ERR'):
        return False, {'ERR': o['ERR'][-300:]}
    m1 = o.get('m1') or {}
    if not m1.get('open'):
        return False, {'why': o.get('why', '창 안 뜸'), 'btn1': o.get('btn1')}
    ih, iw, pn = m1['ih'], m1['iw'], m1['pn']
    d['창 높이'] = pn['h']; d['1/3'] = round(ih / 3, 1)
    c1 = pn['h'] <= ih / 3 + 0.5
    d['속 굴림'] = [m1['sh'], m1['ch'], len(m1['scr'])]
    c2 = m1['sh'] <= m1['ch'] and not m1['scr']
    bxh = (m1.get('bx') or {}).get('h') or 0
    d['그리는 칸 높이'] = bxh
    c3 = bxh >= 80
    c4 = pn['x'] >= -0.5 and pn['y'] >= -0.5 and pn['r'] <= iw + 0.5 and pn['b'] <= ih + 0.5
    d['화면 안'] = [pn['x'], pn['y'], pn['r'], pn['b']]
    m2 = o.get('m2') or {}; m3 = o.get('m3') or {}
    p2 = m2.get('pn') if m2.get('open') else None
    p3 = m3.get('pn') if m3.get('open') else None
    d['키운 뒤'] = [p2['w'], p2['h']] if p2 else None
    d['다시 연 뒤'] = [p3['w'], p3['h']] if p3 else None
    c5 = bool(p2 and (abs(p2['h'] - pn['h']) >= 20 or abs(p2['w'] - pn['w']) >= 20))   # 모서리로 정말 바뀜
    c6 = bool(o.get('closed') and p2 and p3 and _DE_near(p2['w'], p3['w']) and _DE_near(p2['h'], p3['h']))
    card = o.get('layer') != 'pdf'   # 「다시 열면 그 크기(카드 층 기억)」 — 크기 기억(jagwa.win.mcard)은 카드 층만 · 물리(PDF 층) = 잰 값만(판정 밖 · 앱 주석 「물리는 종전대로 세션 동안만」 + 처음 1/3 캡)
    seed = o.get('seed')
    fin = o.get('mc4') or {}
    pen = o.get('pen')
    want = (seed or []) + ([pen] if pen else [])
    c7 = bool(seed) and fin.get('m') == want and fin.get('d') == want
    d['획'] = {'지어낸 획 그대로': bool(seed) and (fin.get('m') or [None])[0] == seed[0], '펜 획': (len(pen) // 2) if pen else None,
              '펜 그대로': (pen in (fin.get('m') or [])) if pen else None, '저장 = 화면': fin.get('m') == fin.get('d')}
    d['부분'] = {'≤1/3': c1, '속 굴림 0': c2, '칸≥80': c3, '화면 안': c4, '모서리 바뀜': c5, ('다시 열면 그 크기' if card else '다시 열면 그 크기(물리 · 판정 밖)'): c6, '획 무변': c7}
    return all([c1, c2, c3, c4, c5, c6 if card else True, c7]), dict([('부분', d.pop('부분'))] + list(d.items()))


def judge_D(o, base_o=None):
    """o = flow_D 결과 {PC:{…}, PH:{…}} → {D_PC: (bool, 잰 값), D_PH: …}"""
    out = {}
    for dv in ('PC', 'PH'):
        if dv in o:
            out['D_' + dv] = judge_D1(o[dv])
    return out


# ───────────────────────── E ─────────────────────────
def _row_press(p, touch, part, skip, wait=1600):
    r = p.ev(DE_ROW_JS, [part, list(skip)])
    if (not r or r.get('no') is None) and part == 'ox':   # 차림 — O△X 줄을 서랍 목록 안에서 보이게 굴림(누름은 진짜)
        p.ev(SCROLLOX_JS, list(skip)); p.wait(400)
        r = p.ev(DE_ROW_JS, [part, list(skip)])
        if r is not None:
            r['scrolled'] = True
    if not r or r.get('no') is None:
        return r, False
    _press(p, r['cx'], r['cy'], touch, wait)
    return r, True


def _after(p, kind, no, o, key, dw0):
    if kind != 'ox' and no is not None:
        _until(p, "(n)=>{const v=document.getElementById('view');return (v&&!v.classList.contains('hide')&&+VNO===+n&&(!HASBOOK||QUID===String(qk(n))))||[...document.querySelectorAll('.vpin')].some(x=>+x.dataset.no===+n)}", no, ms=4000)
    elif kind == 'ox':
        _until(p, "()=>!!document.getElementById('g3Pop')", None, ms=2000)
    p.wait(300)
    a = p.ev(AFTER_JS, [kind, no]); a['no'] = no; a['dw0'] = dw0
    o[key] = a
    if a.get('fold'):   # 차림 — 접혔으면(바탕 · 폭 < 700) 다시 펴서 다음 누름을 따로 잼(판정은 이 누름 값 그대로)
        p.ev("()=>{ndResFold(false);return 1}"); p.wait(800)
    return a


def _flow_E1(p, eng, subj, touch, o):
    o['s0'] = s0 = p.ev(E_ST_JS)
    if not s0.get('res'):
        o['why'] = '상주 서랍 없음'; return
    if s0.get('fold'):
        p.ev("()=>{ndResFold(false);return 1}"); p.wait(800)
    o['s1a'] = p.ev(E_ST_JS)
    # ⓐ 손잡이 톡/누름 → 접힘(창을 열기 전 — 폭이 좁은 바탕은 창이 서랍 띠를 다 덮어 손잡이를 못 누름)
    p.ev("()=>{try{if(typeof g3PopClose==='function')g3PopClose()}catch(e){}try{const n=document.getElementById('nsPop');if(n&&n.__close)n.__close()}catch(e){}return 1}"); p.wait(300)   # 차림 — 떠 있는 작은 창(근거 · 검색) 닫음
    g = p.ev(GRIPPT_JS)
    o['grip'] = g
    if g and g.get('ok'):
        _press(p, g['cx'], g['cy'], touch, 800)
    o['F_grip'] = p.ev(E_ST_JS)
    # ⓑ 밀기(터치 기기만) → 접힘
    if touch:
        p.ev("()=>{ndResFold(false);return 1}"); p.wait(900)
        o['F_open'] = p.ev(E_ST_JS)
        sp = p.ev(SWPT_JS); o['sw_pt'] = sp
        if sp:
            x0, y0 = sp
            if eng == 'webkit':
                o['sw_by'] = p.ev(SWIPESYN_JS, [x0, y0, x0 - 140, y0])
            else:
                o['sw_by'] = _tdrag(p, [(x0 - 14 * t, y0) for t in range(11)], step_ms=16)
            p.wait(800)
        o['F_swipe'] = p.ev(E_ST_JS)
    if p.ev("document.getElementById('navdr').classList.contains('fold')"):
        p.ev("()=>{ndResFold(false);return 1}"); p.wait(900)   # 차림 — 다시 펴고 네 누름
    s1 = p.ev(E_ST_JS); o['s1'] = s1; dw0 = s1['dw']
    # ① 줄 제목 — 창 없을 때 → 창 열림
    r, ok = _row_press(p, touch, 'ndt', [s1['VNO']] if s1.get('VNO') else [])
    o['r_title'] = r
    if ok:
        _after(p, 'title', r['no'], o, 'P_title', dw0)
    p.wait(500)
    # ② 서랍 🔍 → 낱말(번호/코드 · 출력 안 함) → 찾은 줄 제목
    q = p.ev(QPICK_JS)
    if q:
        o['q'] = {'kind': q['kind'], 'len': len(q['q']), 'md5': hashlib.md5(q['q'].encode('utf-8')).hexdigest()[:8], 'n': q['n']}
        sb = p.ev(r"""()=>{const e=document.querySelector('#navdr .ndhead .ndsrch');if(!e)return null;const r=e.getBoundingClientRect();const cx=r.left+r.width/2,cy=r.top+r.height/2,h=document.elementFromPoint(cx,cy);return {cx,cy,ok:!!h&&(h===e||e.contains(h)),top:h?(h.id||String(h.className).split(' ')[0]||h.tagName):null}}""")
        o['srch_btn'] = sb
        if sb and sb.get('ok'):
            _press(p, sb['cx'], sb['cy'], touch, 600)
            ip = p.ev(r"""()=>{const e=document.querySelector('#nsPop .rlq');if(!e)return null;const r=e.getBoundingClientRect();return {cx:r.left+Math.min(30,r.width/2),cy:r.top+r.height/2}}""")
            o['srch_inp'] = bool(ip)
            if ip:
                _press(p, ip['cx'], ip['cy'], touch, 300)
                p.pg.keyboard.type(q['q'], delay=30); p.wait(700)
                cur = p.ev("+VNO")
                nr = p.ev(NSROW_JS, [cur]); o['r_srch'] = nr
                if nr and nr.get('no') is not None:
                    _press(p, nr['cx'], nr['cy'], touch, 1600)
                    _after(p, 'srch', nr['no'], o, 'P_srch', dw0)
    else:
        o['q'] = None
    p.wait(500)
    # ③ 줄 번호 — 창 떠 있을 때 → 비교 창(또는 그 문항) · 검색 뒤(폰은 비교 창이 위 1/3 = 서랍 머리 🔍 를 덮음)
    cur = p.ev("+VNO")
    r, ok = _row_press(p, touch, 'ndno', [cur])
    o['r_no'] = r
    if ok:
        _after(p, 'no', r['no'], o, 'P_no', dw0)
    p.wait(500)
    # ④ O△X — 근거 창(#g3Pop) · 누름마다 따로: 앞 누름이 연 창(이제 서랍 위)이 O△X 줄을 덮으면 닫고 잼
    p.ev("()=>{document.querySelectorAll('.vpin,.sheet.twin').forEach(x=>x.remove());try{g3PopClose()}catch(e){}try{closeView()}catch(e){}return 1}"); p.wait(600)
    if p.ev("document.getElementById('navdr').classList.contains('fold')"):
        p.ev("()=>{ndResFold(false);return 1}"); p.wait(900)
    r, ok = _row_press(p, touch, 'ox', [], wait=900)
    o['r_ox'] = r
    if ok:
        _after(p, 'ox', r['no'], o, 'P_ox', dw0)
    p.wait(400)


def flow_E(br, eng, src, subj, width):
    """E — 과목 하나 × 폭 하나(384 · 600 · 820 = 터치 · 1100 = 마우스) · 새 쪽"""
    (W, H), touch = DEV_E[width]
    o = {'dev': [W, H], 'touch': touch}; p = None
    try:
        p = JG.Pg_PP(br, eng, 'cfE-%s-%s-%s-%d' % (_DE_h6(src), eng, subj, width), src, subj, (W, H), touch=touch, remote=JG.Remote())
        p.wait(1500)
        _flow_E1(p, eng, subj, touch, o)
    except Exception:
        o['ERR'] = traceback.format_exc()[-900:]
    finally:
        if p is not None:
            try:
                o['perr'] = [e[:120] for e in (p.errs or [])[:3]]
            except Exception:
                pass
            p.close()
    return o


def judge_E(o, base_o=None):
    """o = flow_E 결과(폭 하나) → {E<폭>: (bool, 잰 값)} · base_o 를 주면 바탕 판정을 잰 값에 곁들임(폭 ≥ 700 = 바탕과 같음)"""
    W = (o.get('dev') or [0])[0]
    name = 'E%d' % W
    if o.get('ERR'):
        return {name: (False, {'ERR': o['ERR'][-300:]})}
    parts = {}; d = {'부분': parts}
    for k, lab in (('P_title', '제목'), ('P_no', '번호'), ('P_srch', '검색 줄'), ('P_ox', 'O△X')):
        a = o.get(k)
        if not a:
            parts[lab] = False
            d[lab] = {'못 누름': o.get({'P_title': 'r_title', 'P_no': 'r_no', 'P_srch': 'r_srch', 'P_ox': 'r_ox'}[k])}
            continue
        keep = (not a['fold']) and _DE_near(a['dw'], a['dw0'], 1.0)
        parts[lab] = bool(keep and a['opened'] and a.get('above'))
        d[lab] = {'서랍 폭': [a['dw0'], a['dw']], '접힘': a['fold'], '창': a.get('wk'), '위': a.get('above'),
                 'z': [a.get('zW'), a.get('zD')], '겹친 점': [a.get('ov'), a.get('inW'), a.get('inD')]}
    fg = o.get('F_grip') or {}
    parts['손잡이 접힘'] = bool(fg.get('fold')) and (fg.get('dw') or 999) <= 20
    d['손잡이'] = [fg.get('fold'), fg.get('dw')]
    if o.get('touch'):
        fo = o.get('F_open') or {}; fs = o.get('F_swipe') or {}
        parts['밀기 접힘'] = bool((not fo.get('fold')) and fs.get('fold') and (fs.get('dw') or 999) <= 20)
        d['밀기'] = [fo.get('fold'), fs.get('fold'), fs.get('dw'), o.get('sw_by')]
    if base_o is not None:
        try:
            d['바탕'] = judge_E(base_o)[name][0]
        except Exception:
            d['바탕'] = None
    return {name: (all(parts.values()), d)}


NAMES_D = {
    'D_PC': '🃏 암기카드 창 · PC 1100×800 마우스 — 처음 ≤ innerHeight/3 · 속 굴림 0 · 그리는 칸 ≥ 80 · 화면 안 · 모서리로 키운 뒤 다시 열면 그 크기(카드 층) · 획 좌표 무변',
    'D_PH': '🃏 암기카드 창 · 폰 384×740 손가락 — 같은 칸',
}
NAMES_E = {
    'E384': '서랍 안 접힘 · 폭 384 손가락 — 제목 · 검색 줄 · 번호 · O△X 누름 = 서랍 폭 그대로 · 창 열림 · 창이 서랍 위 · 손잡이 · 밀기로는 접힘',
    'E600': '서랍 안 접힘 · 폭 600 손가락 — 같은 칸',
    'E820': '서랍 안 접힘 · 폭 820(아이패드) 손가락 — 같은 칸(바탕도 같음)',
    'E1100': '서랍 안 접힘 · 폭 1100 마우스 — 같은 칸(바탕도 같음)',
}
E_SAME = ('E820', 'E1100')



# ══ 무리 F ══════════════════════════════════════════════════════════════════════════════
# 관문 F — add1 근거 글 들여쓰기(줄 앞 빈칸 · 줄 안 여러 빈칸 그대로) · 세 과목 · PC 1100×800 · 폰 384×740 — _harness_jagwa_cardfit.py 에 들어갈 몫
import json

F_T1 = '시험근거들임칠\n1.첫 줄\n    들인 줄(m_1v_1)\n    둘째 들인 줄\n2.다음  두칸  띄움'
F_T2 = '가꺾임시험\n      들인 채로 길게 써서 폰 폭에서 꺾이는 줄 가나다라마바사 아자차카타파하 가나다라마바사 아자차카타파하 가나다라마바사'
F_T3 = '한 줄 근거 시험솔'
F_PICK = r"""()=>{for(const r of DATA){const no=r[F.NO];if(typeof isC==='function'&&isC(r))continue;if(hist(no).length)continue;const u=String(typeof GGU==='function'?GGU(r):qk(no));
  if((typeof ggOf==='function'?ggOf(u):[]).length)continue;let used=false;for(const k in GG)(GG[k]||[]).forEach(x=>{if(x&&x.src&&String(x.src).indexOf(u+'|')===0)used=true});if(used)continue;return no}return null}"""
F_SEED = r"""async ([no,ts,addRec])=>{const u=String(typeof GGU==='function'?GGU(rec(no)):qk(no));for(const t of ts){if(window.G3&&G3.push)await G3.push(u,'t',{t});
    else{const list=ggOf(u).slice();list.push({k:ggNewKey('g_'),i:list.length+1,t,ts:Date.now(),cs:[],f:'t'});await ggSaveList(u,list)}}
  if(addRec){ST[qk(no)]={h:[{m:'O',t:Date.now()-3600000,s:30}]};await saveST()}try{ggRepaint(u)}catch(e){}try{navBuild()}catch(e){}return ggOf(u).length}"""
F_OPEN = r"""async (no)=>{await openView(no);for(let i=0;i<60;i++){await new Promise(r=>setTimeout(r,100));if(!HASBOOK||QUID===String(qk(no)))break}
  await new Promise(r=>setTimeout(r,500));
  const v=document.getElementById('view');if(v&&v.classList.contains('g3off')){const f=document.getElementById('g3Fold');if(f)f.click()}
  const c=document.getElementById('card');if(HASBOOK&&c&&c.classList.contains('g3fold')){const b=c.querySelector('.g3fb:not(.none)');if(b)b.click()}
  await new Promise(r=>setTimeout(r,400));return VNO}"""
# 근거 한 덩이(그 글 표지로 찾음) 잼 — 줄(.ggl) · .ggt 왼쪽 · 다섯째 줄 빈칸 둘 · 화면 폭(빈칸 둘 > 하나) · 꺾인 줄 둘째 줄 왼쪽 · 높이
F_MEAS = r"""([root,sel,mark])=>{const R=root?document.querySelector(root):document;if(!R)return {root:false};
  const el=[...R.querySelectorAll(sel)].find(e=>(e.textContent||'').indexOf(mark)>=0);if(!el)return {root:true,el:false};
  try{el.scrollIntoView({block:'center'})}catch(e){}
  const L=[...el.querySelectorAll('.ggl')];const T=L.map(l=>l.querySelector('.ggt'));
  const lx=T.map(t=>t?Math.round(t.getBoundingClientRect().left*10)/10:null);
  const r=el.getBoundingClientRect(),cs=getComputedStyle(el);
  const o={root:true,el:true,ggl:L.length,lx,elx:Math.round(r.left*10)/10,h:Math.round(r.height*10)/10,ws:cs.whiteSpace,txt5:null,w2:null,w1:null,wrap:null};
  const t5=T[4]||null;
  if(t5){o.txt5=(t5.textContent||'').indexOf('두칸  띄움')>=0;
    const tn=[...t5.childNodes].find(n=>n.nodeType===3&&n.textContent.indexOf('두칸  띄움')>=0);
    if(tn){const i=tn.textContent.indexOf('두칸  띄움'),rg=document.createRange();rg.setStart(tn,i);rg.setEnd(tn,i+6);o.w2=Math.round(rg.getBoundingClientRect().width*10)/10;
      const sp=document.createElement('span');sp.textContent='두칸 띄움';t5.appendChild(sp);o.w1=Math.round(sp.getBoundingClientRect().width*10)/10;sp.remove()}}
  else{   /* 헛잣대(.ggl 없음) — 그 글 안 「두칸  띄움」 화면 폭만 */
    const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let n;while((n=w.nextNode())){const i=n.textContent.indexOf('두칸  띄움');if(i>=0){const rg=document.createRange();rg.setStart(n,i);rg.setEnd(n,i+6);o.w2=Math.round(rg.getBoundingClientRect().width*10)/10;
      const sp=document.createElement('span');sp.textContent='두칸 띄움';n.parentNode.appendChild(sp);o.w1=Math.round(sp.getBoundingClientRect().width*10)/10;sp.remove();o.txt5=true;break}}}
  /* 꺾인 들인 줄(둘째 .ggl) — 줄 상자 수 · 둘째 줄 왼쪽 */
  const tw=T[1]||null;if(tw){const rg=document.createRange();rg.selectNodeContents(tw);const rs=[...rg.getClientRects()].filter(q=>q.width>1);
    const ys=[...new Set(rs.map(q=>Math.round(q.top)))].sort((a,b)=>a-b);const lh=parseFloat(getComputedStyle(tw).lineHeight)||parseFloat(getComputedStyle(tw).fontSize)*1.3;
    const second=rs.filter(q=>Math.round(q.top)===ys[1]);const h1=T[0]?T[0].getBoundingClientRect().height:lh;o.wrap={lines:ys.length,h:Math.round(tw.getBoundingClientRect().height*10)/10,lh:Math.round(h1*10)/10,
      l2:second.length?Math.round(Math.min(...second.map(q=>q.left))*10)/10:null,tl:Math.round(tw.getBoundingClientRect().left*10)/10}}
  return o}"""
F_USE = r"""(m)=>{const it=[...document.querySelectorAll('.g3it')].find(e=>(e.textContent||'').indexOf(m)>=0);if(!it)return {it:false};const u=it.querySelector('[data-g3use]');if(!u)return {it:true,el:false};
  try{u.scrollIntoView({block:'center'})}catch(e){}const r=u.getBoundingClientRect();const t=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return {it:true,el:true,cx:r.left+r.width/2,cy:r.top+r.height/2,hit:!!(t&&(t===u||u.contains(t)))}}"""
F_OVER = r"""()=>{const d=document.scrollingElement||document.documentElement;return {sw:d.scrollWidth,iw:innerWidth,over:d.scrollWidth>innerWidth+1}}"""
F_ROW = r"""(no)=>{const row=document.querySelector('.ndrow[data-no="'+no+'"]');if(!row)return null;try{row.scrollIntoView({block:'center'})}catch(e){}const e=row.querySelector('.ndox');if(!e)return {ox:false};
  const r=e.getBoundingClientRect();const t=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return {ox:true,cx:r.left+r.width/2,cy:r.top+r.height/2,hit:!!(t&&(t===e||e.contains(t)))}}"""


def _fpg(JG, br, eng, tag, src, subj, dev, touch):
    p = JG.Pg_PP(br, eng, tag, src, subj, dev, touch=touch, remote=JG.Remote())
    p.wait(1200)
    return p


def flow_F(JG, br, eng, src, subj, tag='F'):
    o = {}
    p = _fpg(JG, br, eng, 'cf%s-%s-%s-pc' % (tag, eng, subj), src, subj, (1100, 800), False)
    try:
        no = p.ev(F_PICK)
        o['문항'] = no
        if not no:
            o['하네스 오류'] = '고를 문항 없음'
            return o
        p.ev(F_OPEN, no)
        o['근거 수'] = p.ev(F_SEED, [no, [F_T1, F_T2, F_T3], True])
        p.ev(F_OPEN, no)
        sel = '.g3it .g3tx'
        o['줄'] = p.ev(F_MEAS, [None, sel, '시험근거들임칠'])
        o['한 줄'] = p.ev(F_MEAS, [None, sel, '한 줄 근거 시험솔'])
        o['넘침 PC'] = p.ev(F_OVER)
        # F6 서랍 O△X 근거 창
        at = p.ev(F_ROW, no)
        if at and at.get('ox'):
            if at.get('hit'):
                p.click(at['cx'], at['cy'], 900)
            else:
                p.ev("(no)=>{const e=document.querySelector('.ndrow[data-no=\"'+no+'\"] .ndox');if(e)e.click();return !!e}", no); p.wait(900)
        o['서랍 창'] = p.ev(F_MEAS, ['#g3Pop', '.g3pf .it', '시험근거들임칠'])
        o['서랍 누름'] = (at or {}).get('hit')
        p.ev("(()=>{try{g3PopClose()}catch(e){}return 1})()")
        # F6 쓰인 문항 창(물리 = 근거 글 · 카드 층 = 패치 45 「이 글을 쓴 문항 N」 한 줄 = 글 없음)
        p.ev(F_OPEN, no)
        ua = p.ev(F_USE, '시험근거들임칠')   # 그 근거 줄의 쓰인 수(data-g3use) — 진짜 누름(맨 위가 아니면 el.click())
        if ua and ua.get('hit'):
            p.click(ua['cx'], ua['cy'], 900)
        elif ua and ua.get('el'):
            p.ev("(m)=>{const it=[...document.querySelectorAll('.g3it')].find(e=>(e.textContent||'').indexOf(m)>=0);const u=it&&it.querySelector('[data-g3use]');if(u)u.click();return !!u}", '시험근거들임칠'); p.wait(900)
        o['쓰인 누름'] = ua
        o['쓰인 창'] = p.ev(F_MEAS, ['#gguw', '.gg', '시험근거들임칠'])
        o['쓰인 창 있음'] = p.ev("!!document.getElementById('gguw')")
        o['오류 PC'] = (p.errs or [])[:3]
    finally:
        p.close()
    q = _fpg(JG, br, eng, 'cf%s-%s-%s-ph' % (tag, eng, subj), src, subj, (384, 740), True)
    try:
        q.ev(F_OPEN, no)
        q.ev(F_SEED, [no, [F_T1, F_T2, F_T3], False])
        q.ev(F_OPEN, no)
        o['꺾임'] = q.ev(F_MEAS, [None, '.g3it .g3tx', '가꺾임시험'])
        o['넘침 폰'] = q.ev(F_OVER)
        o['오류 폰'] = (q.errs or [])[:3]
    finally:
        q.close()
    return o


def _f12(m):
    """F1 · F2 — .ggl 5 · 셋째 · 넷째 .ggt 왼쪽 > 둘째 + 8 · 셋째 = 넷째(±1) · 다섯째 = 둘째(±1)"""
    m = m or {}
    lx = m.get('lx') or []
    f1 = m.get('ggl') == 5
    f2 = f1 and None not in lx and lx[2] > lx[1] + 8 and abs(lx[2] - lx[3]) <= 1 and abs(lx[4] - lx[1]) <= 1
    return f1, bool(f2)


def judge_F(subj, o, pre=None):
    """pre = 헛잣대 앱(패치 72 만) 값 — F5 줄 높이 잣대"""
    J = {}
    if not o or o.get('하네스 오류'):
        return {c: (False, (o or {}).get('하네스 오류', '값 없음')) for c in NAMES_F}
    m = o.get('줄') or {}
    f1, f2 = _f12(m)
    J['F1'] = (f1, {'.ggl': m.get('ggl'), 'white-space': m.get('ws')})
    J['F2'] = (f2, {'.ggt 왼쪽': m.get('lx')})
    J['F3'] = (bool(m.get('txt5')) and (m.get('w2') or 0) > (m.get('w1') or 1e9), {'빈칸 둘 글자': m.get('txt5'), '폭(빈칸 둘 · 하나)': [m.get('w2'), m.get('w1')]})
    w = (o.get('꺾임') or {}).get('wrap') or {}
    J['F4'] = (bool(w) and (w.get('lines') or 0) >= 2 and (w.get('h') or 0) >= 1.8 * (w.get('lh') or 99) and w.get('l2') is not None
               and abs(w['l2'] - w['tl']) <= 1 and w['tl'] > ((o.get('꺾임') or {}).get('elx') or 0) + 4, {'꺾인 줄': w, '그 근거 왼쪽': (o.get('꺾임') or {}).get('elx')})
    h1 = o.get('한 줄') or {}
    hp = ((pre or {}).get('한 줄') or {}).get('h')
    J['F5'] = (h1.get('ggl') == 0 and h1.get('h') is not None and (hp is None or abs(h1['h'] - hp) <= 1), {'.ggl': h1.get('ggl'), '높이(새 판 · 헛잣대)': [h1.get('h'), hp]})
    a1, a2 = _f12(o.get('서랍 창'))
    card = subj != 'phys'
    u = o.get('쓰인 창') or {}
    b1, b2 = _f12(u)
    J['F6'] = (a1 and a2 and (card or (b1 and b2)), {'서랍 근거 창': [(o.get('서랍 창') or {}).get('ggl'), (o.get('서랍 창') or {}).get('lx')],
                                                 '쓰인 문항 창': [u.get('ggl'), u.get('lx')] if not card else '카드 층 = 근거 글 없음(패치 45 · 「이 글을 쓴 문항 N」 한 줄)'})
    op, oh = o.get('넘침 PC') or {}, o.get('넘침 폰') or {}
    J['F7'] = (not (o.get('오류 PC') or o.get('오류 폰')) and not op.get('over', True) and not oh.get('over', True),
               {'오류': (o.get('오류 PC') or []) + (o.get('오류 폰') or []), '가로 넘침(PC · 폰)': [op.get('sw'), op.get('iw'), oh.get('sw'), oh.get('iw')]})
    return J


NAMES_F = {
    'F1': 'add1 근거 줄 — 여러 줄 근거 .g3tx 안 .ggl 5 줄',
    'F2': '셋째 · 넷째 줄 .ggt 왼쪽 > 둘째 + 8px · 셋째 = 넷째 · 다섯째 = 둘째(±1)',
    'F3': '다섯째 줄 「두칸  띄움」 빈칸 둘 그대로 · 화면 폭 > 한 칸 글',
    'F4': '폰 384 — 꺾인 들인 줄 .ggt 두 줄 넘음 · 둘째 줄 왼쪽 = .ggt 왼쪽(±1 · 맨 왼쪽 아님)',
    'F5': '한 줄 근거 = .ggl 0 · 높이 = 헛잣대 앱(±1)',
    'F6': '서랍 O△X 근거 창 · 쓰인 문항 창(물리)에서도 F1 · F2',
    'F7': '페이지 오류 0 · 가로 넘침 0(PC · 폰)',
}
F_SAME = ('F5', 'F7')



# ══ 돌리기 ════════════════════════════════════════════════════════════════════════════════
def _pg(br, eng, tag, src, subj, dev, touch):
    p = JG.Pg_PP(br, eng, tag, src, subj, dev, touch=touch, remote=JG.Remote())
    p.wait(1000)
    return p


def run_A(br, eng, ver):
    src, out = SRC[ver], {}
    f = _pg(br, eng, 'cfA-%s-%s-phys' % (ver, eng), src, 'phys', PC, False)
    try:
        no = f.ev("(()=>{for(const r of DATA){if(!hist(r[F.NO]).length)return r[F.NO]}})()")
        f.ev(A_OPEN_JS, no)
        out['phys_head'] = f.ev(HEAD_JS)
    finally:
        f.close()
    for subj in ('earth', 'bio'):
        p = _pg(br, eng, 'cfA-%s-%s-%s' % (ver, eng, subj), src, subj, PC, False)
        q = _pg(br, eng, 'cfA4-%s-%s-%s' % (ver, eng, subj), src, subj, PH, True)
        try:
            out[subj] = flow_A(p, eng, subj, q)
        except Exception:
            out[subj] = {'하네스 오류': traceback.format_exc()[-700:]}
        finally:
            p.close(); q.close()
    return out


def run_B(br, eng, ver):
    src, out = SRC[ver], {}
    for subj in ('phys', 'earth', 'bio'):
        o = {}
        p = _pg(br, eng, 'cfB-%s-%s-%s' % (ver, eng, subj), src, subj, PC, False)
        try:
            no, band = pick_card(p)
            no2, _ = pick_card(p, skip=[no])
            o['문항'] = {'no': no, 'no2': no2, '빈 띠': band}
            p.ev(B_OPEN_JS, no)
            try:
                o['B'] = flow_B(p, eng, subj, no, no2)
            except Exception:
                o['B'] = {'ERR': traceback.format_exc()[-700:]}
            if subj != 'phys':
                o['TC1'] = p.ev(BK_JS)
                nA = p.ev(PICK_JS, [no, no2]); nB = p.ev(PICK_JS, [no, no2, nA])
                for k, n_, rs in (('TR1', nA, [1, 3]), ('TR2', nB, [2])):
                    try:
                        o[k] = flow_TR(p, subj, n_, rs)
                    except Exception as ex:
                        o[k] = {'오류': str(ex)[:200]}
            o['오류'] = (p.errs or [])[:3]
        finally:
            p.close()
        q = _pg(br, eng, 'cfB10-%s-%s-%s' % (ver, eng, subj), src, subj, PH, True)
        try:
            o['T10'] = flow_T10(q, eng, subj, o['문항']['no'])
        except Exception as ex:
            o['T10'] = {'오류': str(ex)[:200]}
        finally:
            q.close()
        out[subj] = o
    return out


def run_C(br, eng, ver):
    out = {}
    for subj in ('phys', 'earth', 'bio'):
        try:
            out[subj] = flow_C(br, eng, SRC[ver], subj)
        except Exception:
            out[subj] = {'하네스 오류': traceback.format_exc()[-700:]}
    return out


def run_D(br, eng, ver):
    out = {}
    for subj in ('phys', 'earth', 'bio'):
        try:
            out[subj] = flow_D(br, eng, SRC[ver], subj)
        except Exception:
            out[subj] = {'하네스 오류': traceback.format_exc()[-700:]}
    return out


def run_E(br, eng, ver):
    out = {}
    for subj in ('phys', 'earth'):
        for w in (384, 600, 820, 1100):
            try:
                out['%s@%d' % (subj, w)] = flow_E(br, eng, SRC[ver], subj, w)
            except Exception:
                out['%s@%d' % (subj, w)] = {'하네스 오류': traceback.format_exc()[-700:]}
    return out


def run_F(br, eng, ver):
    out = {}
    for subj in ('phys', 'earth', 'bio'):
        try:
            out[subj] = flow_F(JG, br, eng, SRC[ver], subj, 'F%s' % ver[0])
        except Exception:
            out[subj] = {'하네스 오류': traceback.format_exc()[-700:]}
    return out


RUN = {'A': run_A, 'B': run_B, 'C': run_C, 'D': run_D, 'E': run_E, 'F': run_F}


# ══ 판정 ════════════════════════════════════════════════════════════════════════════════
SAME = {'T10', 'TC1', 'TR2', 'C7'} | set(globals().get('E_SAME', ())) | set(globals().get('F_SAME', ()))   # 지시서 「바탕도 같은 칸」 — 바탕 값으로 가름(바탕도 PASS 여야 맞음)
HALF = {'A12'}
INK_CELLS = {'T%d' % i for i in range(1, 12)}   # 「점선 틈」 일부 바탕도 같음 — 헛잣대 셈 밖(바탕 값은 적음)


def judge_group(g, res, eng, ver):
    """{(칸, 과목 꼴): (ok, 값)}"""
    x = (res.get((ver, eng)) or {}).get(g) or {}
    out = {}
    if g == 'A':
        for subj in ('earth', 'bio'):
            for c, v in judge_A(x.get(subj), x.get('phys_head')).items():
                out[(c, subj)] = v
    elif g == 'B':
        bx = (res.get(('BASE', eng)) or {}).get('B') or {}
        for subj in ('phys', 'earth', 'bio'):
            tcb = QC.base('TC1@%s@%s' % (eng, subj), ((bx.get(subj) or {}).get('TC1')) if GATE else ((x.get(subj) or {}).get('TC1')))
            for c, v in judge_B(subj, x.get(subj), tcb).items():
                out[(c, subj)] = v
    elif g == 'C':
        bx = (res.get(('BASE', eng)) or {}).get('C') or {}
        for subj in ('phys', 'earth', 'bio'):
            for c, v in judge_C(x.get(subj), bx.get(subj) if GATE else None).items():
                out[(c, subj)] = v
    elif g == 'D':
        for subj in ('phys', 'earth', 'bio'):
            for c, v in judge_D(x.get(subj)).items():
                out[(c, subj)] = v
    elif g == 'F':   # add1 — 헛잣대 = 패치 72 만 넣은 앱(PRE) · F5 줄 높이는 그 앱 값으로
        px = (res.get(('PRE', eng)) or {}).get('F') or {}
        for subj in ('phys', 'earth', 'bio'):
            for c, v in judge_F(subj, x.get(subj), px.get(subj)).items():
                out[(c, subj)] = v
    elif g == 'E':
        bx = (res.get(('BASE', eng)) or {}).get('E') or {}
        for k, o in x.items():
            for c, v in judge_E(o, bx.get(k) if GATE else None).items():
                if ver == 'BASE' and c in SAME:   # 바탕 값으로 가름 — 바탕에 아예 없는 칸(지학 서랍 검색 줄 · O△X = 이 판에 카드 층으로 들어옴)은 빼고 견줌
                    d = v[1] if isinstance(v[1], dict) else {}
                    pt = {kk: vv for kk, vv in (d.get('부분') or {}).items() if not (kk in ('검색 줄', 'O△X') and isinstance(d.get(kk), dict) and '못 누름' in d[kk])}
                    v = (all(pt.values()) if pt else v[0], dict(d, **{'바탕 견줌': sorted(pt)}))
                out[(c, k)] = v
    return out


NAMES = {}
for _n in ('NAMES_A', 'NAMES_B', 'NAMES_C', 'NAMES_D', 'NAMES_E', 'NAMES_F'):
    NAMES.update(globals().get(_n) or {})


def main():
    os.makedirs(TMPD, exist_ok=True)
    R('B0', '판 · 자리', None, None, {'NEW': NEWF, 'md5(LF)': {k: hashlib.md5(v.replace('\r\n', '\n').encode('utf-8')).hexdigest()[:8] for k, v in SRC.items()},
                                     'BASE': BASE if GATE else '(regress · smoke = 안 띄움)', 'PRE': PRE, '엔진': ENGS, '무리': GROUPS})
    res, t0 = {}, time.time()
    vers = ['NEW'] + (['BASE'] if GATE else []) + (['PRE'] if PRE else [])
    with sync_playwright() as pw:
        brs = {e: getattr(pw, e).launch() for e in ENGS}
        for ver in vers:
            for eng in ENGS:
                QC.launch('base' if ver == 'BASE' else 'new')
                for g in GROUPS:
                    if (ver == 'PRE' and g not in ('B', 'F')) or (ver == 'BASE' and g == 'F'):
                        continue   # B = §3-2 합치기 전후 · F = add1 헛잣대(패치 72 만) · 바탕(92f0215)은 A~E
                    t1 = time.time()
                    try:
                        res.setdefault((ver, eng), {})[g] = RUN[g](brs[eng], eng, ver)
                    except Exception:
                        res.setdefault((ver, eng), {})[g] = {'하네스 오류': traceback.format_exc()[-900:]}
                    R('B0', '%s %s %s 돎' % (ver, eng, g), None, None, '%.1f 분' % ((time.time() - t1) / 60))
        for b in brs.values():
            b.close()
    for g in GROUPS:
        for eng in ENGS:
            jn = judge_group(g, res, eng, 'NEW')
            if g == 'F':   # add1 헛잣대 = 패치 72 만 넣은 앱(--pre)
                jb, jp = (judge_group(g, res, eng, 'PRE') if PRE else {}), {}
            else:
                jb = judge_group(g, res, eng, 'BASE') if GATE else {}
                jp = judge_group(g, res, eng, 'PRE') if (PRE and g == 'B') else {}
            for (c, k), (ok, d) in sorted(jn.items(), key=lambda t: (list(NAMES).index(t[0][0]) if t[0][0] in NAMES else 99, t[0][1])):
                if not want(c):
                    continue
                b = jb.get((c, k)) if jb else None
                det = {'새 판': d, '바탕': b[1]} if b is not None else d
                if c not in INK_CELLS:
                    jp.pop((c, k), None)   # §3-2 견줌 = 필기 도구 칸(T1~T11)만 · TR = §3-1 새 코드 · TC1 = 교재 창
                if jp.get((c, k)) is not None:
                    det = {'새 판': d, '합치기 전': jp[(c, k)][1], '합치기 전 판정': bool(jp[(c, k)][0])}
                    if b is not None:
                        det['바탕'] = b[1]
                R('%s[%s·%s]' % (c, k, eng), NAMES.get(c, c), bool(ok), None if b is None else bool(b[0]), det, yard=(c not in SAME and c not in HALF))
                if jp.get((c, k)) is not None:
                    R('%s[%s·%s]' % (c, k, eng), '§3-2 합치기 전 = 같은 판정', bool(jp[(c, k)][0]) == bool(ok), None, {'합치기 전': bool(jp[(c, k)][0]), '새 판': bool(ok)})
    newp = [x for x in RES if x['new'] is not None]
    yard = [x for x in RES if x['base'] is not None and x['yard']]
    same = [x for x in RES if x['base'] is not None and not x['yard'] and x['g'].split('[')[0] in SAME]
    R('B9', '합 — 새 판 PASS %d · FAIL %d · 헛잣대(새 칸 바탕 FAIL) %d/%d · 바탕도 같음 칸 바탕 PASS %d/%d · %.1f 분' % (
        sum(1 for x in newp if x['new']), sum(1 for x in newp if not x['new']), sum(1 for x in yard if not x['base']), len(yard),
        sum(1 for x in same if x['base']), len(same), (time.time() - t0) / 60), None)
    os.makedirs(os.path.dirname(os.path.abspath(OUTF)), exist_ok=True)
    with open(OUTF, 'w', encoding='utf-8') as f:
        for x in RES:
            tag = 'INFO' if x['new'] is None else ('PASS' if x['new'] else 'FAIL')
            yb = '' if x['base'] is None else (' · 바탕 ' + (('PASS(바탕도 같음)' if not x['yard'] else 'PASS') if x['base'] else ('FAIL' if x['yard'] else 'FAIL(바탕도 같아야 할 칸)')))
            f.write('%s | %s · %s%s | %s\n' % (tag, x['g'], x['name'], yb, _s(x['d'])[:700]))
    return 0 if newp and all(x['new'] for x in newp) else 1


if __name__ == '__main__':
    sys.exit(main())
