# -*- coding: utf-8 -*-
r"""_task_jagwa_claude_e010 관문 「CE10」 — 지학 G23-60-06 Claude 풀이 · 풀이 창 읽기 판 세 가지($…$ 식 · ↳ 줄 · O/X 색)
(2026-10-06 · 같은 길 = _harness_jagwa_claude_e004.py(CE4) 꼴 · 공용 도우미 = jagwa/_harness_jagwa_uid.py(HU))

  python _harness_jagwa_claude_e010.py [--eng chromium,webkit] [--res <결과>] [--base <genie 커밋>] [--seed <studyplandata 커밋>] [--shots <폴더>]

  NEW 앱  = genie 작업트리 jagwa/index.html(줄끝 LF 로 맞춤) — gpPre · gpPost · showRead 의 kx · CSS 셋(§A-1)
  BASE 앱 = genie 바탕 커밋 jagwa/index.html — --base · 안 주면 「function gpPre( 를 처음 넣은 커밋」의 바로 앞(커밋 전이면 HEAD)
            — 커밋·병합 뒤 다시 돌려도 헛잣대가 거저 PASS 가 안 된다(CE4 와 같은 꼴)
  NEW 기록 = studyplandata 작업트리 earth/기록.json 의 gpt["G23-60-06"] 가 재료면 「적재 뒤 실물」 · 아니면 HEAD 기록에 두 칸(글 · 도장)을 더한 「합성(적재 전)」
  BASE 기록 = NEW 기록에서 그 두 칸(+묘비)만 뺀 것
  바탕 칸 = BASE 앱 + NEW 기록(지시서 §B-7 「783799b 앱 · G23-60-06 넣은 합성 기록」) — B-2(식 · 아랫줄 · O/X · 글자) · B-3 이 FAIL 이어야 헛잣대 PASS
  기록은 route 사본 · PUT 은 가로채 밖으로 안 나감(HU INIT) · 앱 코드가 바뀜 → 크롬 · 웹킷 둘 다(규칙 57)
  ⚠ 자과앱 픽셀 IDENTICAL 게이트 없음(CLAUDE.md) — DOM 개수 · 계산된 색 · 글자 크기 · getBoundingClientRect · Range 글자 상자로 잰다.
    390 폭 그림 한 장(엔진마다 · --shots 기본 %TEMP%/h_e010)은 사용자 눈 확인용 — 게이트 아님 · 잰 뒤에 창 높이 한도를 풀어 한 장에 펼쳐 찍는다(크기 손잡이 숨김).
  ⚠ 식 높이(B-3) — `.katex` 는 inline 이라 rect 가 글꼴 높이(≈16px)뿐이고 위·아래 글자는 상대 위치라 rect 에 안 든다
    → 식 안 글자 상자(Range) · 묶음 괄호 svg 범위로 잰다. 둘째 식(위 글자 「풍속↓」·「위도↑」)은 줄 간격(1.72) 안에 들어가
    CSS 줄 높이(22.36px)보다 낮다(21.0px · 10/6 00:1x 탐침 · 크롬 · 웹킷 같음) → 잣대 = ⓐ 위·아래 글자가 식 본 줄 아래(첫 식 · 묶음 괄호 밑)·위(둘째 식)에 붙음
    ⓑ 식 글자 범위 높이 > 같은 문단 보통 글 한 줄 글자 상자 높이 · CSS 줄 높이 · `.katex` rect 높이는 INFO 로 같이 적는다.
  ⚠ §B-4 폭 넷 — 띄운 뒤 창 크기만 바꾸면 떠 있는 창이 옛 자리에 남는다(10/6 탐침) → 폭마다 새 문맥으로 열어 잰다.
    「겹침 0」 — 글꼴 상자(Range)끼리 겹친 짝만 그 열을 찍어 두 잉크 사이 빈 행이 있나로 가른다(글꼴 상자는 위·아래 여백을 품는다 —
    첫 1회 실행 10/6 00:34 = 첫 식 「지구」 상자가 다음 줄 상자와 크롬 2px · 웹킷 1.3px 겹쳐 FAIL · 3배 탐침으로 잉크 사이 빈 줄 4 · 5.3px).
    헛잣대(390) = 첫 식을 8px 내려(상대 위치) 잉크가 닿게 하면 잡는가.
  ⚠ 값을 박지 않는다 — 기대 개수는 재료 글을 앱 규칙(gpPre → gpRender)대로 세어 내고, 지시서 §B-2 숫자와 맞는지는 A-0 줄이 따로 본다.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT · N_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
_roots.need_n('jagwa/gigu/claude_motion 재료(채팅이 만든 md — N: 에만)')
import io, json, os, re, sys, time, hashlib, subprocess, tempfile   # noqa: E402
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import _harness_jagwa_uid as HU   # noqa: E402  (GENIE_ROOT · SPD_ROOT · Dev · route 사본 · PUT 가로채기)


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = HU.GENIE; SPD = HU.SPD
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_claude_e010_result.txt'))
SHOTS = ARG('--shots', os.path.join(tempfile.gettempdir(), 'h_e010'))   # 그림은 N: 밖에(마이박스 잇단 쓰기 · 사슬 되돌리기) — 보고에 쓸 한 장은 손으로 옮긴다
MAT = _roots.n('jagwa', 'gigu', 'claude_motion')   # N: 에만 있는 재료 — _qa 사본으로 돌려도 N: 에서 읽는다
UID = 'G23-60-06'
SUBJ, RP = 'earth', 'earth/기록.json'
TITLE_TASK = 'G23-60-06 Claude · 정답 ③'          # §B-1 지시서 글자
QA_TASK = '지학QA E010 · 질문일 2026-10-05'        # §B-1 · §0-4
WANT_TASK = dict(h3=3, ul=5, ol=10, sub=6, oxo=1, oxx=7, katex=2)   # §B-2 지시서 숫자(= §0-4 재료 셈)
OTHER_EARTH = ['G09-46-10', 'G03-40-05', 'G06-43-02', 'G06-43-10']   # §0-3 다른 Claude 글 — 지학 넷
OTHER_PHYS = [72, 97]                                                # — 물리 둘
WIDTHS = [(1440, 900), (900, 900), (834, 1112), (390, 844)]          # §B-4 폭 넷(높이는 흔한 기기 꼴)
COL_O, COL_X = 'rgb(29, 78, 216)', 'rgb(198, 40, 40)'               # §B-3 #1D4ED8 · #C62828
GP_QA = re.compile(r'^(지학|생물)QA [EB]\d{3} · 질문일 \d{4}-\d{2}-\d{2}$')
GP_SEC = re.compile(r'^\s*([①-⑩])\s*(.*)$')
GP_UL = re.compile(r'^\s*-\s+')
GP_OL = re.compile(r'^\s*\d+\.\s+')
GP_ANS_CHO = re.compile(r'^[ㄱ-ㅎ㉠-㉽,\s]+$')
CIRC_ = '①②③④⑤⑥⑦⑧'
SOH = chr(1)   # 앱 gpPre 가 ↳ 줄을 붙이는 표지(U+0001)
NL = chr(10)
ROWS = []
from playwright.sync_api import sync_playwright   # noqa: E402
from PIL import Image   # noqa: E402  (B-4 — 글꼴 상자가 겹친 짝의 잉크 행만 센다 · 판 사이 픽셀 대조 아님)


def R(eng, name, okn, okb, val):
    okn = okn if okn is None else bool(okn)
    okb = okb if okb is None else bool(okb)
    ROWS.append((eng, name, okn, okb, val))
    print('%s | 바탕 %s | %s · %s | %s' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[okn], {True: 'PASS', False: 'FAIL', None: '—'}[okb], eng, name,
          (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str))[:420]), flush=True)


def dumps(d):
    return json.dumps(d, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


def git1(repo, *a):
    return HU.git(repo, *a).decode('utf-8', 'replace').strip()


def lf(t):
    """줄끝을 LF 로(CR LF · 홑 CR)"""
    return t.replace(chr(13) + NL, NL).replace(chr(13), NL)


def mat(nm):
    """재료 md — N: 에서는 이름이 소문자로 보여도 윈도는 같은 파일(지시서 머리 · uid_unify D-2)"""
    for x in (nm, nm.lower()):
        f = os.path.join(MAT, x)
        if os.path.isfile(f):
            return lf(io.open(f, encoding='utf-8', newline='').read())
    raise SystemExit('NG 재료 없음: %s' % nm)


MD = mat('earth_%s.md' % UID)
_ITEMS = json.loads(open(os.path.join(SPD, 'earth', '문항.json'), 'rb').read().decode('utf-8'))
U2N = {it['uid']: i + 1 for i, it in enumerate(_ITEMS)}   # uid → 화면 번호(F.NO = 문항.json 차례 + 1)
NO = U2N[UID]
K5 = _ITEMS[4]['uid']                                      # 「기록 있는 기기」에서 누를 5번 문항의 칸 열쇠(uid)


def gpt_title(it):
    """앱 gptTitle 과 같은 규칙(uid_unify §C-1) — uid + ' Claude' + (정답 있으면 ' · 정답 ' + CIRC[정답−1] [+ 자음 선택지 글] [+ ' (옳지 않은 것)'])"""
    s = str(it['uid']) + ' Claude'
    try:
        a = int(str(it.get('정답') or '').strip() or 0)
    except ValueError:
        a = 0
    if 1 <= a <= len(CIRC_):
        s += ' · 정답 ' + CIRC_[a - 1]
        ch = it.get('선택지') or []
        t = str(ch[a - 1] if a - 1 < len(ch) else '').strip()
        if t and GP_ANS_CHO.match(t):
            t = re.sub(r'[㉠-㉽]', lambda m_: 'ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ'[ord(m_.group(0)) - 0x3260] if ord(m_.group(0)) - 0x3260 < 14 else m_.group(0), t)
            s += ' ' + re.sub(r'\s+', '', re.sub(r'\s*,\s*', '·', t))
        if '옳지 않은' in str(it.get('문항') or ''):
            s += ' (옳지 않은 것)'
    return s


def gp_qa_split(src):
    """앱 gpQaSplit 과 같은 규칙 — 첫 줄이 QA 꼴이면 (그 줄, 그 줄과 바로 뒤 빈 줄을 뺀 나머지)"""
    L = lf(str(src or '')).split(NL)
    if not L or not GP_QA.match(L[0].strip()):
        return '', str(src or '')
    rest = L[1:]
    while rest and not rest[0].strip():
        rest.pop(0)
    return L[0].strip(), NL.join(rest)


def gp_pre(src):
    """앱 gpPre 와 같은 규칙 — 번호 줄 바로 아랫줄 「↳ …」 를 그 줄 끝에 SOH 로 붙임"""
    o = []
    for x in str(src).split(NL):
        if re.match(r'^\s*↳', x) and o and GP_OL.match(o[-1]):
            o[-1] += SOH + re.sub(r'^\s*↳\s*', '', x, count=1)
        else:
            o.append(x)
    return NL.join(o)


def expect(src):
    """읽기 판에 서야 할 것 — gpPre → gpRender 문법(빈 줄 · | 표 · ①~⑩ 절 머리 · - 글머리 · 1. 번호 · 문단)대로 센다"""
    L = gp_pre(src).split(NL)
    c = dict(h3=0, h3t='', ul=0, ol=0, ols=[], sub=0)
    i, cur = 0, ''
    while i < len(L):
        x = L[i]
        if not x.strip():
            i += 1
            continue
        if '|' in x:
            while i < len(L) and '|' in L[i]:
                i += 1
            continue
        m = GP_SEC.match(x)
        if m:
            c['h3'] += 1; c['h3t'] += m.group(1); cur = m.group(1); i += 1
            continue
        if GP_UL.match(x):
            while i < len(L) and GP_UL.match(L[i]):
                c['ul'] += 1; i += 1
            continue
        if GP_OL.match(x):
            g = []
            while i < len(L) and GP_OL.match(L[i]):
                c['ol'] += 1; g.append(L[i].count(SOH)); i += 1
            c['ols'].append([cur, g])
            continue
        while i < len(L) and L[i].strip() and '|' not in L[i] and not GP_SEC.match(L[i]) and not GP_UL.match(L[i]) and not GP_OL.match(L[i]):
            i += 1
    c['sub'] = sum(sum(g) for _, g in c['ols'])
    c['subs'] = [re.sub(r'^\s*↳\s*', '', y, count=1) for y in str(src).split(NL) if re.match(r'^\s*↳', y)]
    c['oxo'] = src.count('**O**'); c['oxx'] = src.count('**X**')
    c['katex'] = len(re.findall(r'\$[^$\n]+\$', src))
    return c


QA_EXP, REST = gp_qa_split(MD)
EXP = expect(REST)
TITLE = gpt_title(_ITEMS[NO - 1])


def recs():
    head = HU.git(SPD, 'show', 'HEAD:' + RP)
    wt = open(os.path.join(SPD, 'earth', '기록.json'), 'rb').read()
    dw = json.loads(wt.decode('utf-8'))
    if (dw['data'].get('gpt') or {}).get(UID) == MD:
        b = json.loads(wt.decode('utf-8'))   # 바탕 = 지금 기록에서 이 판의 두 칸(+묘비)만 뺀 것
        b['data']['gpt'].pop(UID, None); b['u'].pop('gpt|' + UID, None); b.get('gone', {}).pop('gpt|' + UID, None)
        return wt, dumps(b), '적재 뒤 실물'
    d = json.loads(head.decode('utf-8'))
    d['data'].setdefault('gpt', {})[UID] = MD; d['u']['gpt|' + UID] = int(time.time() * 1000)
    return dumps(d), head, '합성(적재 전)'


def lane_rev():
    L = git1(GENIE, 'log', '--reverse', '--format=%h', '-S', 'function gpPre(', '--', 'jagwa/index.html').split()
    return L[0] if L else ''


def seed_rev():
    s = ARG('--seed', '')
    if s:
        return s
    L = git1(SPD, 'log', '--reverse', '--format=%h', '-S', '"gpt|%s"' % UID, '--', RP).split()
    return L[0] if L else ''


LANE = lane_rev()
BASE_REV = ARG('--base', '') or (git1(GENIE, 'rev-parse', '--short', LANE + '~1') if LANE else git1(GENIE, 'rev-parse', '--short', 'HEAD'))
APP_N = open(os.path.join(GENIE, 'jagwa', 'index.html'), 'rb').read().replace(bytes([13, 10]), bytes([10]))
APP_B = HU.git(GENIE, 'show', BASE_REV + ':jagwa/index.html')


def statics():
    mdir = os.path.join(GENIE, 'jagwa', 'motion')   # 이 판은 motion 을 안 건드린다 — 두 앱 다 같은 motion
    return {'motion/' + f: open(os.path.join(mdir, f), 'rb').read() for f in os.listdir(mdir) if os.path.isfile(os.path.join(mdir, f))}


CJS = r"""
window.__C={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 async open(no){try{closeView()}catch(e){}await new Promise(r=>setTimeout(r,150));await openView(no);await new Promise(r=>setTimeout(r,1200));
   const b=document.getElementById('tGpt');const row=b&&b.parentElement;const vis=[...(row?row.children:[])].filter(x=>x.offsetParent!==null&&getComputedStyle(x).display!=='none');
   return {btn:__C.tx(b),last:vis.length?vis[vis.length-1]===b:false,vis:!!b&&b.offsetParent!==null&&b.getBoundingClientRect().width>0}},
 last(){return [...document.querySelectorAll('.sheet')].pop()||null},
 closeSheets(){document.querySelectorAll('.sheet').forEach(x=>x.remove())},
 async sheet(){const s=__C.last();if(!s)return null;try{await motLoad()}catch(e){}await new Promise(r=>setTimeout(r,300));
   return {h2:__C.tx(s.querySelector('.panel > h2')),qa:__C.tx(s.querySelector('#gpQa')),sub:!!s.querySelector('.panel > #gpSub'),
     read:!!s.querySelector('.gpread'),edit:!!s.querySelector('#gpIn'),mot:!!s.querySelector('#gpMot'),
     motEarth:(typeof MOT!=='undefined'&&MOT&&MOT.earth)||null,kxReady:typeof renderMathInElement==='function'}},
 html(){const s=__C.last();const rd=s&&s.querySelector('.gpread');return rd?rd.innerHTML:null},
 glyphs(root,skip){const L=[];const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let t;
   while(t=w.nextNode()){if(!t.textContent.trim())continue;if(skip&&skip(t))continue;const g=document.createRange();g.selectNodeContents(t);
     for(const r of g.getClientRects())if(r.width>0&&r.height>0)L.push({t:t.textContent,lab:!!t.parentElement.closest('.text'),l:r.left,r:r.right,top:r.top,b:r.bottom})}return L},
 kgeo(k){const html=k.querySelector('.katex-html');const G=html?__C.glyphs(html):[];const main=G.filter(x=>!x.lab),lab=G.filter(x=>x.lab);
   const sv=[...k.querySelectorAll('svg')].map(e=>e.getBoundingClientRect()).filter(r=>r.height>0);
   const mn=a=>a.length?Math.min(...a):null,mx=a=>a.length?Math.max(...a):null;
   const top=mn(G.map(x=>x.top).concat(sv.map(r=>r.top))),bot=mx(G.map(x=>x.b).concat(sv.map(r=>r.bottom)));
   const p=k.closest('p,li')||k.parentElement;
   const nh=mx(__C.glyphs(p,t=>!!t.parentElement.closest('.katex')).map(x=>x.b-x.top))||0;
   const an=k.querySelector('annotation');
   return {src:an?an.textContent:'',lab:[...new Set(lab.map(x=>x.t))].join(''),labTop:mn(lab.map(x=>x.top)),labBot:mx(lab.map(x=>x.b)),
     mainTop:mn(main.map(x=>x.top)),mainBot:mx(main.map(x=>x.b)),top,bot,h:(top!=null&&bot!=null)?bot-top:null,
     left:mn(G.map(x=>x.l)),right:mx(G.map(x=>x.r)),inlineH:k.getBoundingClientRect().height,lh:parseFloat(getComputedStyle(p).lineHeight),nh,
     nmain:main.length,nlab:lab.length,nsvg:sv.length}},
 async read(){const s=__C.last();const rd=s&&s.querySelector('.gpread');if(!rd)return null;
   try{await document.fonts.ready}catch(e){}await new Promise(r=>setTimeout(r,250));
   const q=sel=>[...rd.querySelectorAll(sel)];
   const ols=q('ol.gpol').map(ol=>{let p=ol.previousElementSibling;while(p&&!p.matches('h3.gph'))p=p.previousElementSibling;
     return [p?__C.tx(p).charAt(0):'',[...ol.children].map(li=>li.querySelectorAll('span.gpsub').length)]});
   const subs=q('span.gpsub'),fs=e=>parseFloat(getComputedStyle(e).fontSize);
   const tx=rd.textContent;
   return {h3:q('h3.gph').length,h3t:q('h3.gph').map(x=>__C.tx(x).charAt(0)).join(''),ul:q('ul.gpul li').length,ol:q('ol.gpol li').length,ols,
     sub:subs.length,subIn:subs.filter(x=>x.parentElement&&x.parentElement.matches('ol.gpol > li')).length,subTx:subs.map(x=>x.textContent),
     subFs:subs.map(x=>[fs(x),fs(x.closest('li')||rd)]),
     oxo:q('b.oxo').length,oxx:q('b.oxx').length,oxoC:q('b.oxo').map(x=>getComputedStyle(x).color),oxxC:q('b.oxx').map(x=>getComputedStyle(x).color),
     bOX:q('b:not(.oxo):not(.oxx)').filter(x=>/^[OX]$/.test(x.textContent)).length,bAll:q('b').length,
     inkC:getComputedStyle(rd).color,
     katex:q('.katex').length,kerr:q('.katex-error').length,dollar:(tx.match(/\$/g)||[]).length,arrow:(tx.match(/↳/g)||[]).length,
     u1:(rd.innerHTML.match(/\u0001/g)||[]).length,script:q('script').length,kgeo:q('.katex').map(__C.kgeo),
     kxReady:typeof renderMathInElement==='function'}},
 async geo(){const s=__C.last();const rd=s&&s.querySelector('.gpread');if(!rd)return null;
   try{await document.fonts.ready}catch(e){}await new Promise(r=>setTimeout(r,250));
   const p=s.querySelector('.panel');const pr=p.getBoundingClientRect(),rr=rd.getBoundingClientRect();const K=[...rd.querySelectorAll('.katex')];
   const fr=[];__C._frn=[];{const w=document.createTreeWalker(rd,NodeFilter.SHOW_TEXT);let t;while(t=w.nextNode()){if(!t.textContent.trim())continue;const k=t.parentElement.closest('.katex');
     if(k&&!t.parentElement.closest('.katex-html'))continue;const g=document.createRange();g.selectNodeContents(t);
     [...g.getClientRects()].forEach((r,ri)=>{if(r.width>0&&r.height>0){fr.push({k:k?K.indexOf(k):-1,t:t.textContent.slice(0,10),l:r.left,r:r.right,top:r.top,b:r.bottom});__C._frn.push([t,ri])}})}}
   const ov=[];for(let i=0;i<fr.length;i++)for(let j=i+1;j<fr.length;j++){const a=fr[i],c=fr[j];if(a.k>=0&&a.k===c.k)continue;
     const ww=Math.min(a.r,c.r)-Math.max(a.l,c.l),hh=Math.min(a.b,c.b)-Math.max(a.top,c.top);if(ww>1&&hh>1)ov.push({i,j,a:a.t,c:c.t,w:Math.round(ww),h:Math.round(hh*10)/10})}
   const kx=K.map(k=>{const g=__C.kgeo(k);return [Math.round(g.left*10)/10,Math.round(g.right*10)/10]});
   return {vw:innerWidth,doc:[document.documentElement.scrollWidth,document.documentElement.clientWidth],rd:[rd.scrollWidth,rd.clientWidth],
     panel:[p.scrollWidth,p.clientWidth],prect:[Math.round(pr.left*10)/10,Math.round(pr.right*10)/10],rrect:[Math.round(rr.left*10)/10,Math.round(rr.right*10)/10],
     kx,katex:K.length,nfr:fr.length,nov:ov.length,ov:ov.slice(0,8)}},
 async pairRect(i,j){const [ta,ra]=__C._frn[i],[tc,rc]=__C._frn[j];ta.parentElement.scrollIntoView({block:'center'});await new Promise(r=>setTimeout(r,300));
   const R=(t,ri)=>{const g=document.createRange();g.selectNodeContents(t);const r=[...g.getClientRects()][ri];return {l:r.left,r:r.right,top:r.top,b:r.bottom}};
   return {a:R(ta,ra),c:R(tc,rc),vh:innerHeight}},
 shift(px){const s=__C.last();const k=s&&s.querySelector('.gpread .katex');if(!k)return false;k.style.position=px?'relative':'';k.style.top=px?px+'px':'';return true},
 unclip(){const s=__C.last();const p=s.querySelector('.panel');s.style.position='absolute';s.style.bottom='auto';
   p.style.position='absolute';p.style.height='auto';p.style.maxHeight='none';p.style.overflow='visible';s.querySelectorAll('.twgrip').forEach(g=>g.style.display='none')},
 gp(){return Object.fromEntries(Object.entries(GP))},
 async mot(){try{await motLoad()}catch(e){}return (typeof MOT==='undefined')?'없음':MOT},
 listTags(){const it=[...document.querySelectorAll('#list .item')],g=it.filter(d=>d.querySelector('.tag.gp'));
   const noOf=d=>{const u=d.dataset.uid;if(u){const r=DATA.find(x=>x[F.CODE]===u);return r?r[F.NO]:'?'+u}return '?'+__C.tx(d.querySelector('.num'))};
   return {n:it.length,rows:DATA.length,tags:g.map(noOf).sort((a,b)=>a-b),txt:[...new Set(g.map(d=>__C.tx(d.querySelector('.tag.gp'))))]}}
};
"""


class DevW(HU.Dev):
    """HU.Dev 와 같고 창 크기만 고른다(§B-4 폭 넷 — 띄운 뒤 창 크기만 바꾸면 떠 있는 창이 옛 자리에 남는다 · 그래서 폭마다 새 문맥)"""
    def __init__(self, br, eng, w, h):
        self.eng = eng; self.S = HU.Srv()
        self.ctx = br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, has_touch=True)
        OK = ('http://127.0.0.1', 'https://cdnjs.cloudflare.com/', 'https://cdn.jsdelivr.net/', 'https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')
        self.ctx.route('**/*', lambda rt: rt.continue_() if rt.request.url.startswith(OK) else rt.abort())
        self.pg = None; self.errs = []


def load(dv, app, subj, rec, stat):
    dv.load(app, SPD, subj, rec={'%s/기록.json' % subj: rec} if rec else None, static=stat)
    dv.cerr = []
    dv.pg.on('console', lambda m: dv.cerr.append('%s @%s' % (m.text[:160], ((m.location or {}).get('url') or '')[-48:])) if m.type == 'error' else None)
    dv.ev(CJS)
    dv.ev("()=>__J.sync()"); dv.pg.wait_for_timeout(800)


def dv_open(br, eng, app, subj, rec, stat, wh=None):
    dv = DevW(br, eng, *wh) if wh else HU.Dev(br, eng)
    load(dv, app, subj, rec, stat)
    return dv


def click(dv, sel):
    r = dv.ev("s=>{const e=document.querySelector(s);if(!e)return null;e.scrollIntoView({block:'nearest'});const b=e.getBoundingClientRect();"
              "if(b.width<=0||b.height<=0)return null;return [b.x+b.width/2,b.y+b.height/2]}", sel)
    if not r:
        return False
    dv.pg.mouse.click(r[0], r[1]); dv.pg.wait_for_timeout(700)
    return True


def open_gpt(dv, no):
    """번호 no 문제 창 → 아랫줄 「Claude」 진짜 누름 → 풀이 창"""
    o = {'btn': dv.ev("n=>__C.open(n)", int(no))}
    o['clicked'] = click(dv, '#tGpt'); dv.pg.wait_for_timeout(900)
    o['sheet'] = dv.ev("()=>__C.sheet()")
    return o


def side(br, eng, app, rec, stat, others=True):
    """지학 기기 하나 — 빈 기기에서 그 기록을 받은 뒤 G23-60-06 풀이 창 · 다른 Claude 글 넷의 읽기 판"""
    out = {}
    dv = dv_open(br, eng, app, SUBJ, rec, stat)
    try:
        out['mot'] = dv.ev("()=>__C.mot()")
        out['list'] = dv.ev("()=>__C.listTags()")
        out['gp'] = dv.ev("()=>__C.gp()")
        out['keys'] = dv.ev("()=>SYNC_KEYS.filter(k=>k!=='gpt')")
        out['stores'] = dv.ev("k=>__J.stores(k)", out['keys'])
        out['body'] = dv.ev("p=>__J.lastPut(p)", RP)
        o = open_gpt(dv, NO)
        o['read'] = dv.ev("()=>__C.read()") if (o['sheet'] or {}).get('read') else None
        dv.ev("()=>__C.closeSheets()")
        out['me'] = o
        out['html'] = {}
        if others:
            for u in OTHER_EARTH:
                x = open_gpt(dv, U2N[u])
                out['html'][u] = dv.ev("()=>__C.html()") if (x['sheet'] or {}).get('read') else None
                dv.ev("()=>__C.closeSheets()")
        out['errs'] = dv.errs[:5]
        out['cerr'] = list(dv.cerr)[:10]
    finally:
        dv.close()
    return out


def phys(br, eng, app, stat):
    """물리 72 · 97 — 읽기 판 innerHTML(물리 기록 = studyplandata 작업트리 그대로)"""
    dv = dv_open(br, eng, app, 'phys', None, stat)
    o = {}
    try:
        for no in OTHER_PHYS:
            x = open_gpt(dv, no)
            o[no] = dv.ev("()=>__C.html()") if (x['sheet'] or {}).get('read') else None
            dv.ev("()=>__C.closeSheets()")
        o['gp'] = dv.ev("()=>({a:GP[72]||'',b:GP[97]||''})")
    finally:
        dv.close()
    return o


def ink_sep(dv, pr):
    """글꼴 상자가 겹친 두 글 조각(pr = {'a','c'} · css px) — 겹친 열만 찍어 행마다 가장 어두운 점을 보고
    「위 글자 잉크와 아래 글자 잉크 사이 빈 행(가장 어두운 점 ≥ 200)이 겹친 띠 안에 있나」 · 위 · 아래 잉크가 둘 다 찍혀야 잰 것으로 친다(헛패스 막음)
    글꼴 상자는 글자 위·아래 여백(ascent · descent)을 품어 잉크보다 크다(10/6 탐침 — 상자 1.3~2px 겹침 · 잉크 사이 빈 줄 4~5.3px)"""
    a, c = pr['a'], pr['c']
    up, lo = (a, c) if a['top'] <= c['top'] else (c, a)
    x0, x1 = max(a['l'], c['l']), min(a['r'], c['r'])
    y0, y1 = up['top'], max(up['b'], lo['b'])
    if x1 - x0 < 1 or y1 - y0 < 1 or y0 < 0 or y1 > pr.get('vh', 10 ** 6):
        return {'갈림': False, '까닭': '찍을 자리가 화면 밖 · 빔', '자리': [x0, y0, x1, y1]}
    png = dv.pg.screenshot(clip={'x': x0, 'y': y0, 'width': x1 - x0, 'height': y1 - y0})
    im = Image.open(io.BytesIO(png)).convert('L')
    W_, H_ = im.size
    px = im.load()
    sc = H_ / (y1 - y0)   # 장치 점 / css px
    rows = [min(px[x, y] for x in range(W_)) for y in range(H_)]
    b0, b1 = max(0, int((lo['top'] - y0) * sc) - 1), min(H_ - 1, int((up['b'] - y0) * sc) + 1)   # 두 상자가 겹친 띠(± 한 행)
    blank = [y for y in range(b0, b1 + 1) if rows[y] >= 200]
    ink_up = any(v < 200 for v in rows[:b0 + 1])
    ink_lo = any(v < 200 for v in rows[b1:])
    return {'갈림': bool(blank) and ink_up and ink_lo, '띠 안 빈 행': len(blank), '띠(점 행)': [b0, b1], '위 잉크': ink_up, '아래 잉크': ink_lo,
            '잉크 행': [y for y, v in enumerate(rows) if v < 200][:1] + [y for y, v in enumerate(rows) if v < 200][-1:]}


def ink_all(dv, geo):
    out = []
    for p in (geo or {}).get('ov') or []:
        pr = dv.ev("([i,j])=>__C.pairRect(i,j)", [p['i'], p['j']])
        out.append(dict(ink_sep(dv, pr), 짝=[p['a'], p['c']], 상자겹침=[p['w'], p['h']]))
    return out


def widths(br, eng, app, rec, stat):
    """§B-4 폭 넷 — 폭마다 새 문맥으로 열고 풀이 창을 띄워 잰다 · 글꼴 상자 겹친 짝은 잉크로 가른다 · 390 은 헛잣대(첫 식 8px 내림)와 그림 한 장"""
    out = {}
    for w, h in WIDTHS:
        dv = dv_open(br, eng, app, SUBJ, rec, stat, wh=(w, h))
        try:
            o = open_gpt(dv, NO)
            o['geo'] = dv.ev("()=>__C.geo()") if (o['sheet'] or {}).get('read') else None
            o['ink'] = ink_all(dv, o['geo']) if o['geo'] else []
            if w <= 480 and o['geo']:
                dv.ev("()=>__C.shift(8)"); dv.pg.wait_for_timeout(200)   # 헛잣대 — 첫 식(아래 글자 「물체」「지구」)을 8px 내려 다음 줄과 잉크가 닿게 한다
                g8 = dv.ev("()=>__C.geo()")
                o['null'] = {'상자 겹침': (g8 or {}).get('nov'), 'ink': ink_all(dv, g8)}
                dv.ev("()=>__C.shift(0)"); dv.pg.wait_for_timeout(200)
            if w <= 480 and o['geo']:
                os.makedirs(SHOTS, exist_ok=True)
                f = os.path.join(SHOTS, 'ce10_%d_%s.png' % (w, eng))
                try:
                    dv.ev("()=>__C.unclip()"); dv.pg.wait_for_timeout(300)
                    dv.pg.locator('.sheet .panel').last.screenshot(path=f)
                    o['shot'] = f
                except Exception as e:
                    o['shot'] = 'ERR ' + repr(e)[:160]
            out[w] = o
        finally:
            dv.close()
    return out


def dev_records(br, eng, app, rb, rn, stat):
    """기록 있는 기기 — 바탕 기록(G23-60-06 없음)으로 먼저 열고 5번 △(카드 안 [data-vmark=Q])를 진짜로 눌러(내 칸이 더 새것) 둔 뒤 NEW 기록을 받는다(CE4 꼴)"""
    dv = dv_open(br, eng, app, SUBJ, rb, stat)
    try:
        keys = dv.ev("()=>SYNC_KEYS.filter(k=>k!=='gpt')")
        dv.ev("n=>__C.open(n)", 5); h0 = dv.ev("k=>((ST[k]||{}).h||[]).length", K5)
        cq = click(dv, '#card [data-vmark="Q"]'); dv.pg.wait_for_timeout(500); h1 = dv.ev("k=>((ST[k]||{}).h||[]).length", K5)
        dv.ev("()=>{try{closeView()}catch(e){}}"); dv.ev("()=>__J.sync()")
        before = dv.ev("k=>__J.stores(k)", keys); gp0 = dv.ev("()=>__C.gp()")
        load(dv, app, SUBJ, rn, stat)
        after = dv.ev("k=>__J.stores(k)", keys); gp1 = dv.ev("()=>__C.gp()")
        body = json.loads(dv.ev("p=>__J.lastPut(p)", RP) or '{}')
        return dict(keys=keys, h=[h0, h1], cq=cq, same={k: before.get(k) == after.get(k) for k in keys}, gp0=gp0, gp1=gp1,
                    stK5=len(((after.get('status') or {}).get(K5) or {}).get('h') or []), body=body)
    finally:
        dv.close()


def patched_base():
    """BASE 앱에 이 판 패치(_patch_jagwa_claude_e010.py)를 얹은 바이트 — NEW 앱과 같아야 「고친 자리 셋 밖 무변」"""
    tmp = os.path.join(tempfile.gettempdir(), 'h_e010'); os.makedirs(tmp, exist_ok=True)
    f = os.path.join(tmp, 'base_patched.html'); open(f, 'wb').write(APP_B)
    r = subprocess.run([sys.executable, os.path.join(HERE, '_patch_jagwa_claude_e010.py'), f], capture_output=True)
    return open(f, 'rb').read(), lf(r.stdout.decode('utf-8', 'replace')).strip()


def fnum(x):
    return round(x, 1) if isinstance(x, (int, float)) else x


def main():
    rn, rb, how = recs()
    stat = statics()
    jn, jb = json.loads(rn.decode('utf-8')), json.loads(rb.decode('utf-8'))
    gpn, gpb = jn['data'].get('gpt') or {}, jb['data'].get('gpt') or {}
    print('기록 = %s · NEW 앱 = genie 작업트리(md5 %s) · BASE 앱 = genie %s(md5 %s) · 이 판 genie 커밋 %s · 적재 커밋 %s · 화면 번호 %d' % (
        how, hashlib.md5(APP_N).hexdigest()[:8], BASE_REV, hashlib.md5(APP_B).hexdigest()[:8], LANE or '(커밋 전)', seed_rev() or '(적재 전)', NO))
    # ── A-0 재료 셈(오프라인) = 지시서 §B-2 · §0-4 숫자 ──
    ex = {k: EXP[k] for k in WANT_TASK}
    R('-', 'A-0 재료 셈(앱 규칙 gpPre → gpRender 로 셈) = 지시서 §B-2 숫자 %s · QA 첫 줄 = 「%s」 · 제목(문항.json) = 「%s」' % (WANT_TASK, QA_TASK, TITLE_TASK),
      ex == WANT_TASK and QA_EXP == QA_TASK and TITLE == TITLE_TASK, None, dict(ex, ols=EXP['ols'], qa=QA_EXP, title=TITLE))
    t0 = time.time()
    base_fail = {}
    with sync_playwright() as pw:
        for eng in ENGS:
            br = getattr(pw, eng).launch()
            try:
                N = side(br, eng, APP_N, rn, stat)                 # NEW 앱 + NEW 기록
                X = side(br, eng, APP_B, rn, stat)                 # BASE 앱 + NEW 기록 — 헛잣대 칸 · B-6 바탕
                B0 = side(br, eng, APP_B, rb, stat, others=False)  # BASE 앱 + BASE 기록 — 목록 · GP · 올린 몸통 바탕
                PN, PB = phys(br, eng, APP_N, stat), phys(br, eng, APP_B, stat)
                W = widths(br, eng, APP_N, rn, stat)
                D = dev_records(br, eng, APP_N, rb, rn, stat)
                n, x = N['me'], X['me']
                s, sx = n['sheet'] or {}, x['sheet'] or {}
                r, rx = n['read'] or {}, x['read'] or {}

                # ── B-1 ──
                def b1(o, sh):
                    return bool(o['btn']['btn'] == 'Claude ✓' and o['btn']['last'] and o['btn']['vis'] and o['clicked'] and sh.get('read') and not sh.get('edit')
                                and (sh.get('h2') or '').rstrip('✕ ') == TITLE == TITLE_TASK and sh.get('sub') and sh.get('qa') == QA_EXP == QA_TASK
                                and not sh.get('mot') and UID not in (sh.get('motEarth') or []))
                R(eng, 'B-1 %s(화면 %d) — 아랫줄 맨 오른쪽 「Claude ✓」 · 창 제목 「%s」 · 둘째 줄 왼쪽 「%s」 · 「▶ 모션」 0 · 읽기 판이 먼저' % (UID, NO, TITLE_TASK, QA_TASK),
                  b1(n, s), b1(x, sx), {'단추': n['btn'], '제목': s.get('h2'), '둘째 줄': s.get('qa'), '모션 단추': s.get('mot'), 'MOT.earth': s.get('motEarth'),
                                        '읽기 판': s.get('read'), '고치기 판': s.get('edit')})

                # ── B-2 셈 ──
                def c_base(rr):
                    return bool(rr) and rr.get('h3') == EXP['h3'] and rr.get('h3t') == EXP['h3t'] and rr.get('ul') == EXP['ul'] and rr.get('ol') == EXP['ol']

                def g_sub(rr):
                    return bool(rr) and rr.get('sub') == EXP['sub'] and rr.get('subIn') == EXP['sub'] and rr.get('ols') == EXP['ols'] and rr.get('subTx') == EXP['subs']

                def g_ox(rr):
                    return bool(rr) and rr.get('oxo') == EXP['oxo'] and rr.get('oxx') == EXP['oxx'] and rr.get('bOX') == 0

                def g_kx(rr):
                    return bool(rr) and rr.get('katex') == EXP['katex'] and rr.get('kerr') == 0

                def g_tx(rr):
                    return bool(rr) and rr.get('dollar') == 0 and rr.get('arrow') == 0 and rr.get('u1') == 0 and rr.get('script') == 0

                R(eng, 'B-2 셈 — h3.gph %d(%s) · ul.gpul li %d · ol.gpol li %d' % (EXP['h3'], EXP['h3t'], EXP['ul'], EXP['ol']), c_base(r), c_base(rx),
                  {k: r.get(k) for k in ('h3', 'h3t', 'ul', 'ol')})
                R(eng, 'B-2 span.gpsub %d — 다 ol.gpol li 안 · 절마다 번호 목록 하나 · 항목마다 아랫줄 수 = %s(③ 2~7 번에 하나씩) · 글 = 재료 「↳」 뒤 글' % (EXP['sub'], EXP['ols']),
                  g_sub(r), g_sub(rx), {'sub': r.get('sub'), '안': r.get('subIn'), 'ols': r.get('ols'), '바탕 ols': rx.get('ols'), '글 같음': r.get('subTx') == EXP['subs']})
                R(eng, 'B-2 b.oxo %d · b.oxx %d · 꾸밈 없는 굵은 O/X 0' % (EXP['oxo'], EXP['oxx']), g_ox(r), g_ox(rx),
                  {k: r.get(k) for k in ('oxo', 'oxx', 'bOX', 'bAll')} | {'바탕': {k: rx.get(k) for k in ('oxo', 'oxx', 'bOX')}})
                R(eng, 'B-2 .katex %d · .katex-error 0' % EXP['katex'], g_kx(r), g_kx(rx),
                  {'katex': r.get('katex'), 'error': r.get('kerr'), 'KaTeX 실림': r.get('kxReady'), '바탕': [rx.get('katex'), rx.get('kerr')]})
                R(eng, 'B-2 읽기 판 글에 「$」 0 · 「↳」 0 · U+0001 0 · <script> 0', g_tx(r), g_tx(rx),
                  {k: r.get(k) for k in ('dollar', 'arrow', 'u1', 'script')} | {'바탕': {k: rx.get(k) for k in ('dollar', 'arrow', 'u1', 'script')}})

                # ── B-3 모양 ──
                def g_col(rr):
                    return bool(rr) and bool(rr.get('oxoC')) and bool(rr.get('oxxC')) and all(c == COL_O for c in rr['oxoC']) and all(c == COL_X for c in rr['oxxC'])

                def g_fs(rr):
                    return bool(rr) and len(rr.get('subFs') or []) == EXP['sub'] and all(abs(a - b * 0.75) <= 0.5 for a, b in rr['subFs'])

                def g_lab(rr):
                    G = (rr or {}).get('kgeo') or []
                    if len(G) != EXP['katex']:
                        return False
                    for g in G:
                        if None in (g.get('labTop'), g.get('labBot'), g.get('mainTop'), g.get('mainBot')):
                            return False
                        if 'underbrace' in g['src']:   # 첫 식 — 묶음 괄호 밑 글자(물체 · 지구)가 본 줄 아래
                            if not (g['labTop'] >= g['mainBot'] - 1 and g['nsvg'] >= 1):
                                return False
                        elif 'overset' in g['src']:    # 둘째 식 — 위 글자(풍속↓ · 위도↑)가 본 줄 위
                            if not (g['labTop'] < g['mainTop'] and (g['labTop'] + g['labBot']) / 2 < (g['mainTop'] + g['mainBot']) / 2):
                                return False
                        else:
                            return False
                    return True

                def g_h(rr):
                    G = (rr or {}).get('kgeo') or []
                    return len(G) == EXP['katex'] and all((g.get('h') or 0) > (g.get('nh') or 999) for g in G)

                R(eng, 'B-3 색 — b.oxo %s · b.oxx %s(계산된 색 · 다 같음)' % (COL_O, COL_X), g_col(r), g_col(rx),
                  {'O': r.get('oxoC'), 'X': sorted(set(r.get('oxxC') or [])), '글 색': r.get('inkC')})
                R(eng, 'B-3 .gpsub 글씨 = 그 li 글씨 × 0.75(±0.5px)', g_fs(r), g_fs(rx), r.get('subFs'))
                kg = [{k: fnum(v) for k, v in g.items() if k in ('lab', 'labTop', 'labBot', 'mainTop', 'mainBot', 'nsvg')} for g in (r.get('kgeo') or [])]
                R(eng, 'B-3 식 — 위·아래 글자가 붙음(첫 식 「물체」「지구」 = 묶음 괄호 밑 · 본 줄 아래 · 둘째 식 「풍속↓」「위도↑」 = 본 줄 위)', g_lab(r), g_lab(rx), kg)
                R(eng, 'B-3 식 높이(식 안 글자 · 괄호 범위) > 같은 문단 보통 글 한 줄 글자 높이', g_h(r), g_h(rx),
                  [{'식': (g.get('src') or '')[:24], '높이': fnum(g.get('h')), '보통 글 한 줄': fnum(g.get('nh'))} for g in (r.get('kgeo') or [])])
                R(eng, 'B-3 (참고) CSS 줄 높이 · .katex rect 높이(inline · 위·아래 글자 안 듦) — 지시서 「.katex 높이 > 한 줄 높이」 글자 그대로의 값', None, None,
                  [{'식 높이': fnum(g.get('h')), 'CSS 줄 높이': fnum(g.get('lh')), '.katex rect': fnum(g.get('inlineH')), '> 줄 높이': (g.get('h') or 0) > (g.get('lh') or 0)}
                   for g in (r.get('kgeo') or [])])
                # ── B-4 폭 넷 ──
                for w, _h in WIDTHS:
                    o = W.get(w) or {}
                    g = o.get('geo') or {}
                    rr_ = g.get('rrect') or [0, 0]
                    ink = o.get('ink') or []
                    okw = bool(g) and g['rd'][0] <= g['rd'][1] and g['panel'][0] <= g['panel'][1] and g['doc'][0] <= g['doc'][1] \
                        and g['prect'][0] >= -0.5 and g['prect'][1] <= g['vw'] + 0.5 and g['katex'] == EXP['katex'] \
                        and all(a >= rr_[0] - 0.5 and b <= rr_[1] + 0.5 for a, b in (g.get('kx') or [])) and g.get('nfr', 0) > 0 \
                        and len(ink) == min(g.get('nov', 0), 8) and all(x['갈림'] for x in ink)
                    R(eng, 'B-4 폭 %d — .gpread 가로 넘침 0(scrollWidth ≤ clientWidth · 식 둘 다 판 안) · 창 · 쪽 넘침 0 · 창이 화면 안 · 글자 겹침 0'
                      '(글꼴 상자가 겹친 짝은 잉크 사이 빈 행으로 가름)' % w, okw, None,
                      {k: g.get(k) for k in ('vw', 'rd', 'panel', 'doc', 'prect', 'rrect', 'kx', 'nfr')} | {'글꼴 상자 겹침': g.get('nov'), '잉크': ink}
                      | ({'그림': o.get('shot')} if o.get('shot') else {}))
                    if o.get('null') is not None:
                        nl_ = o['null']
                        R(eng, 'B-4 헛잣대(폭 %d) — 첫 식을 8px 내리면(상대 위치) 잉크 겹침을 잡는다(빈 행 없는 짝 ≥ 1)' % w,
                          bool(nl_['ink']) and any(not x['갈림'] and x.get('위 잉크') and x.get('아래 잉크') for x in nl_['ink']), None, nl_)
                # ── B-5 데이터 ──
                gk = [k for k in N['keys'] if N['stores'].get(k) != B0['stores'].get(k)]
                body = json.loads(N['body']) if N['body'] else None
                body0 = json.loads(B0['body']) if B0['body'] else None
                bgp = (body or {}).get('data', {}).get('gpt') or {}
                okb_ = (body is None and body0 is None) or (body is not None and bgp == gpn and (body.get('gone') or {}) == ((body0 or {}).get('gone') or {}))
                ok5 = bool(N['gp'].get(UID) == MD and {k: v for k, v in N['gp'].items() if k != UID} == {k: v for k, v in gpn.items() if k != UID} == B0['gp'] == gpb
                           and not gk and N['keys'] == B0['keys'] and okb_)
                R(eng, 'B-5 빈 기기 — 동기화 뒤 GP["%s"] = 재료 글자 전수(%d자) · 다른 gpt 칸 %d = 기록 값 = 바탕 기기 값 · gpt 밖 동기화 칸 %d 바탕과 같음 · 올린 몸통 gpt = 기록 · 묘비 = 바탕 기기' % (
                    UID, len(MD), len(gpb), len(N['keys'])), ok5, None,
                  {'길이': len(N['gp'].get(UID) or ''), 'GP 열쇠': sorted(N['gp']), '바탕 GP 열쇠': sorted(B0['gp']), '다른 칸': gk,
                   '올린 몸통': 'PUT 없음' if body is None else 'gpt %s' % sorted(bgp), '묘비 같음': okb_})
                bd = D['body'].get('data', {})
                okd = bool(D['cq'] and D['h'][1] == D['h'][0] + 1 and D['gp1'].get(UID) == MD and {k: v for k, v in D['gp1'].items() if k != UID} == D['gp0'] == gpb
                           and all(D['same'].values()) and D['stK5'] == D['h'][1] and (bd.get('gpt') or {}).get(UID) == MD
                           and len(((bd.get('status') or {}).get(K5) or {}).get('h') or []) == D['h'][1])
                R(eng, 'B-5 기록 있는 기기 — 동기화 뒤 GP["%s"] = 재료 · 다른 gpt 칸 무변 · 다른 동기화 칸 %d 무변 · 내 새 칸(5번 △ 진짜 누름) 안 덮임 · 올린 몸통에 둘 다' % (UID, len(D['keys'])),
                  okd, None, {'다른 칸': [k for k in D['keys'] if not D['same'][k]], 'GP 길이': len(D['gp1'].get(UID) or ''), '5번 회독': D['h'], '누름': D['cq'], 'GP 열쇠': sorted(D['gp1'])})
                # ── B-6 무변 ──
                he = {u: (N['html'].get(u) is not None and N['html'].get(u) == X['html'].get(u)) for u in OTHER_EARTH}
                R(eng, 'B-6 지학 Claude 글 넷(%s) — 읽기 판 innerHTML = 바탕 앱(같은 기록) 바이트 그대로' % ' · '.join(OTHER_EARTH), all(he.values()), None,
                  {u: [len(N['html'].get(u) or ''), he[u]] for u in OTHER_EARTH})
                hp = {k: (PN.get(k) is not None and PN.get(k) == PB.get(k)) for k in OTHER_PHYS}
                R(eng, 'B-6 물리 Claude 글 둘(72 · 97) — 읽기 판 innerHTML = 바탕 앱 바이트 그대로 · GP 같음', all(hp.values()) and PN['gp'] == PB['gp'], None,
                  {k: [len(PN.get(k) or ''), hp[k]] for k in OTHER_PHYS})
                want = sorted(B0['list']['tags'] + [NO])
                R(eng, 'B-6 목록 .tag.gp 「Claude」 줄 = 바탕 %s + %d(%s) 한 줄 · 다른 글자 0' % (B0['list']['tags'], NO, UID),
                  N['list']['tags'] == want and N['list']['txt'] == ['Claude'], None, {'NEW': N['list']['tags'], '바탕': B0['list']['tags'], '글자': N['list']['txt']})
                errs = N['errs'] + [e for e in N['cerr'] if 'katex' in e.lower() or 'gpPre' in e or 'gpPost' in e]
                R(eng, 'B-6 페이지 오류(pageerror) 0 · 식 · 덧댐 함수 콘솔 오류 0', not errs, None, {'pageerror': N['errs'], '콘솔(참고)': N['cerr'][:4]})
                base_fail[eng] = {'B-2 아랫줄': not g_sub(rx), 'B-2 O/X': not g_ox(rx), 'B-2 식': not g_kx(rx), 'B-2 글자': not g_tx(rx),
                                  'B-3 색': not g_col(rx), 'B-3 아랫줄 글씨': not g_fs(rx), 'B-3 식 붙음': not g_lab(rx), 'B-3 식 높이': not g_h(rx)}
            finally:
                br.close()
    # ── 헛잣대 · 정적 ──
    for eng, bf in base_fail.items():
        R(eng, 'B-7 헛잣대 — 바탕(%s 앱 · G23-60-06 넣은 기록)에서 B-2(식 · span.gpsub · b.oxo/oxx · 글자)·B-3 가 FAIL' % BASE_REV, all(bf.values()), None, bf)
    pb, pout = patched_base()
    R('-', 'A-1 NEW 앱 = 바탕 앱(%s) + 이 판 패치(gpPre · gpPost · showRead 감쌈 · kx 한 줄 · CSS 셋) — 그 밖 바이트 무변 · %s' % (BASE_REV, pout), pb == APP_N, None,
      {'NEW md5': hashlib.md5(APP_N).hexdigest()[:8], '바탕+패치 md5': hashlib.md5(pb).hexdigest()[:8], 'NEW B': len(APP_N)})
    jm = json.loads(stat['motion/index.json'].decode('utf-8'))
    jm0 = json.loads(HU.git(GENIE, 'show', BASE_REV + ':jagwa/motion/index.json').decode('utf-8'))
    R('-', 'A-2 motion/index.json = 바탕 그대로 · %s 모션 없음(이 판은 모션 무변)' % UID, jm == jm0 and UID not in (jm.get('earth') or []), None, json.dumps(jm))
    six = {u: gpn.get(u) or '' for u in OTHER_EARTH}
    P = json.loads(open(os.path.join(SPD, 'phys', '기록.json'), 'rb').read().decode('utf-8'))
    pg = P['data'].get('gpt') or {}
    six.update({'phys %s' % k: pg.get(str(k)) or '' for k in OTHER_PHYS})
    cnt = {k: [v.count('$'), v.count('↳'), v.count('**O**'), v.count('**X**')] for k, v in six.items()}
    R('-', '§0-3 다른 Claude 글 여섯(기록 값) — 「$」 · 「↳」 · 「**O**」 · 「**X**」 다 0 · 비지 않음', all(v and not any(cnt[k]) for k, v in six.items()), None, cnt)
    Bi = json.loads(open(os.path.join(SPD, 'bio', '기록.json'), 'rb').read().decode('utf-8'))
    R('-', '물리 gpt["72"] · ["97"] = 재료 phys_72.md · phys_97.md 글자 그대로 · 생물 gpt = %s' % json.dumps(Bi['data'].get('gpt'), ensure_ascii=False)[:60],
      pg.get('72') == mat('phys_72.md') and pg.get('97') == mat('phys_97.md'), None, {'물리 gpt': sorted(pg)})
    SEED = seed_rev()
    if SEED:
        fs = git1(SPD, 'diff', '--name-only', SEED + '~1', SEED).split()
        old, new = HU.git(SPD, 'show', SEED + '~1:' + RP), HU.git(SPD, 'show', SEED + ':' + RP)
        where = 'studyplandata 커밋 %s' % SEED
    else:
        fs = [x_[3:] for x_ in HU.git(SPD, 'status', '--porcelain').decode('utf-8', 'replace').split(NL) if x_.strip()]
        old, new = HU.git(SPD, 'show', 'HEAD:' + RP), open(os.path.join(SPD, 'earth', '기록.json'), 'rb').read()
        where = 'studyplandata HEAD → 작업트리(커밋 전)'
    do, dn = json.loads(old.decode('utf-8')), json.loads(new.decode('utf-8'))
    if UID in (dn['data'].get('gpt') or {}) and UID not in (do['data'].get('gpt') or {}):
        a_ = json.loads(json.dumps(dn)); a_['data']['gpt'].pop(UID); a_['u'].pop('gpt|' + UID, None)
        b_ = json.loads(json.dumps(do))
        for z in (a_, b_):
            z.pop('savedAt', None)
        R('-', 'A-2 적재(%s) — 바꾼 파일 = earth/기록.json 하나 · data.gpt["%s"] = 재료 글자 전수 · u["gpt|%s"] 둘(+savedAt)만 더함 · 다른 칸 · gone 무변' % (where, UID, UID),
          a_ == b_ and dn['data']['gpt'][UID] == MD and isinstance(dn['u'].get('gpt|' + UID), int) and fs == [RP], None,
          {'파일': fs, '도장': dn['u'].get('gpt|' + UID), 'savedAt': [do.get('savedAt'), dn.get('savedAt')], '크기': [len(old), len(new)]})
    else:
        R('-', 'A-2 적재(%s) — 아직 적재 전(합성 기록으로 잼)' % where, None, None, '')
    npass = sum(1 for r_ in ROWS if r_[2] is True); nfail = sum(1 for r_ in ROWS if r_[2] is False)
    print(NL + '== PASS %d · FAIL %d · %.0f초 · 기록 %s' % (npass, nfail, time.time() - t0, how))
    with io.open(OUTF, 'a', encoding='utf-8', newline=NL) as fo:
        fo.write(NL + '==== %s · claude_e010 CE10 · 기록 %s · genie HEAD %s · 바탕 %s · 이 판 커밋 %s · studyplandata HEAD %s · 적재 %s · 엔진 %s ====' % (
            time.strftime('%Y-%m-%d %H:%M'), how, git1(GENIE, 'rev-parse', '--short', 'HEAD'), BASE_REV, LANE or '-',
            git1(SPD, 'rev-parse', '--short', 'HEAD'), SEED or '-', ','.join(ENGS)) + NL)
        for eng, nm, okn, okb, v in ROWS:
            fo.write('%s | 바탕 %s | %s · %s | %s' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[okn], {True: 'PASS', False: 'FAIL', None: '—'}[okb], eng, nm,
                     (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str))[:1200]) + NL)
        fo.write('== PASS %d · FAIL %d' % (npass, nfail) + NL)
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
