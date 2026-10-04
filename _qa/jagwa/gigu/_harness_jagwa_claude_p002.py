# -*- coding: utf-8 -*-
r"""_task_jagwa_claude_p002 관문 「CP2」 — 물리 97(PA1109) Claude 풀이 · 「공 하나 vs 두 물체 충돌」 비교 모션
(2026-10-01 · 같은 길 = _task_jagwa_claude_slot §A-3·A-4(물리 72) · 꼴 = _harness_jagwa_claude_e001.py(CE1))

  python _harness_jagwa_claude_p002.py [--eng chromium,webkit] [--res <결과>] [--base <genie 커밋>] [--seed <studyplandata 커밋>]

  NEW  = genie 작업트리 jagwa/motion/*(phys_97.html · index.json 의 phys 에 97)
         + 물리 기록 = studyplandata 작업트리 phys/기록.json — gpt["97"] = 재료면 「적재 뒤 실물」 · 아니면 HEAD 기록에 두 칸을 더한 사본(「합성」)
  BASE(헛잣대) = genie --base(기본 cedc251 = 이 판 바로 앞 · claude_e001 뒤 판)의 motion/* + 기록에서 gpt 97 칸과 그 도장만 뺀 것
         ⚠ 바탕을 HEAD 에서 읽지 않는다 — 커밋·인도 뒤 다시 돌려도 헛잣대가 거저 PASS 가 안 되게(CE1 9/29 실측)
  이 판 커밋 — genie = phys_97.html 을 처음 더한 커밋 · studyplandata = 「gpt|97」 을 처음 넣은 커밋(--seed 로 박을 수 있다)을 git 이력에서 찾아
         그 커밋 단위로 잰다(아직 커밋 전이면 HEAD → 작업트리). 그래서 뒤 판·병합 뒤에 다시 돌려도 「이 판이 한 일」만 잰다.
  앱 = genie HEAD jagwa/index.html(작업트리와 바이트 같음 · 이 판 커밋이 앱을 안 건드림) · 기록은 route 사본 · PUT 은 가로채 밖으로 안 나감(HU INIT)
  ⚠ 자과앱 픽셀 게이트 없음(CLAUDE.md) — DOM 글자·개수로 잰다(모션 「재생 뒤 식 칸」도 글자다).
  ⚠ 값을 박지 않는다 — 목록 태그는 「그 기록의 gpt 칸 번호」, 모션 번호는 「바탕 + 97 로 시작」과 맞댄다
    (claude_e004 처럼 뒤 판이 번호를 끝에 더해도 거짓 FAIL 을 내지 않게 · 9/29 CL-Z 고침의 교훈). 이 판이 남긴 index.json 은 커밋 blob 으로 따로 꼭 맞댄다.
  ⚠ 물리 gg 의 난수 열쇠 k 는 빼고 맞댄다(HU.nok 와 같은 까닭 — ggRestoreNotes_f6cee06 이 열 때마다 새 k 를 만든다 · 판과 무관).
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT · N_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
_roots.need_n('jagwa/gigu/claude_motion 재료(채팅이 만든 md · html — N: 에만)')
import io, json, os, re, sys, time, hashlib   # noqa: E402
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import _harness_jagwa_uid as HU   # noqa: E402  (GENIE_ROOT · SPD_ROOT · Dev · route 사본 · PUT 가로채기)


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = HU.GENIE; SPD = HU.SPD
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_claude_p002_result.txt'))
MAT = _roots.n('jagwa', 'gigu', 'claude_motion')   # N: 에만 있는 재료 — _qa 사본으로 돌려도 N: 에서 읽는다(env_lanes_fix A-2)
BASE_REV = ARG('--base', 'cedc251')   # genie — 이 판 바로 앞(claude_e001 · env_lanes_fix 뒤 판)
SUBJ, NO, RP = 'phys', '97', 'phys/기록.json'
MOTF = 'jagwa/motion/phys_97.html'
WANT = {'h3': 5, 'h3t': '①②③④⑤', 'li': 17, 'ol': 5, 'b': 3, 'tb': 0}
NEIGH = (96, 98)
MINUS = '−'   # 재료·지시서 둘 다 「−3mv」 의 − 는 U+2212
ROWS = []
from playwright.sync_api import sync_playwright   # noqa: E402


def R(eng, name, okn, okb, val):
    ROWS.append((eng, name, okn, okb, val))
    print('%s | 바탕 %s | %s · %s | %s' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[okn], {True: 'PASS', False: 'FAIL', None: '—'}[okb], eng, name,
          (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str))[:420]), flush=True)


def mat(f):
    return io.open(os.path.join(MAT, f), encoding='utf-8', newline='').read().replace('\r\n', '\n')


MD = mat('phys_97.md')


def _old_mat(k):   # 번호 k 의 옛 재료 글(earth_<번호>.md)
    return mat('earth_%d.md' % k)


# ★ uid_unify 옛 잣대 고침(2026-10-04 · 근거 gigu/_task_jagwa_uid_unify.md §A-1 · §A-2 · §C-1 · §C-2 · §C-3 · §D-1 · §D-2 · §0-6) ───────────────────────────────
#   카드 층(지학) 기록 열쇠 = uid(번호 F.NO 는 화면 자리 번호일 뿐) · Claude 풀이 창 새 꼴(제목 「<uid> Claude · 정답 …」 · 둘째 줄 = 왼쪽 QA 줄 + 오른쪽 「▶ 모션」 글자 ·
#   옛 #gpMotBar 줄 없음 · 읽기 판은 QA 첫 줄을 뺀 나머지) · 모션 파일 motion/earth_<uid>.html · motion/index.json 의 earth = uid 문자열.
#   UIDK(그 앱이 uid 열쇠판인가)가 거짓이면(옛 판 · 바탕) 아래 도우미는 옛 값 그대로 돌려준다 — 옛 줄은 바꾼 자리마다 「# 옛 줄:」 주석으로 남겼다.
#   값을 박지 않는다 — 번호 → uid 는 문항.json 에서 · 하네스가 박아 둔 code 는 닻(§0-6)으로 맞대 본다.
import posixpath   # noqa: E402
UIDK = b'function qk(no)' in HU.git(GENIE, 'show', 'HEAD:jagwa/index.html')   # 앱이 카드 층 기록 열쇠를 uid 로 쓰는 판인가(§A-1 의 qk(no))
_ITEMS = json.loads(open(os.path.join(SPD, 'earth', '문항.json'), 'rb').read().decode('utf-8'))
N2U = {str(i + 1): it['uid'] for i, it in enumerate(_ITEMS)}   # 화면 번호(= 문항.json 차례 + 1) → uid
U2N = {u: n for n, u in N2U.items()}
UID_STORES = ['status', 'note', 'qtype', 'conc', 'gpt', 'twin', 'ansfix', 'frm', 'maskpos', 'omrpos', 'mcard', 'link', 'txt']   # 앱 UID_KEYS(§A-2)
GP_QA = re.compile(r'^(지학|생물)QA [EB]\d{3} · 질문일 \d{4}-\d{2}-\d{2}$')
GP_SEC = re.compile(r'^\s*([①-⑩])\s*(.*)$')
GP_UL = re.compile(r'^\s*-\s+')
GP_OL = re.compile(r'^\s*\d+\.\s+')
GP_BOLD = re.compile(r'\*\*([^*]+)\*\*')
GP_ANS_CHO = re.compile(r'^[ㄱ-ㅎ㉠-㉽,\s]+$')
CIRC_ = '①②③④⑤⑥⑦⑧'


def mat_uid(uid):
    """D-2 새 재료(earth_<uid>.md · QA 첫 줄) — 없으면 None(N: 에서 이름이 소문자로 보여도 윈도는 같은 파일)"""
    for nm in (uid, uid.lower()):
        f = os.path.join(MAT, 'earth_%s.md' % nm)
        if os.path.isfile(f):
            return io.open(f, encoding='utf-8', newline='').read().replace('\r\n', '\n')
    return None


def gkey(no):
    """GP · status … 통의 칸 열쇠 — uid 열쇠판이면 그 번호의 uid · 옛 판이면 번호 글자"""
    return N2U.get(str(no), str(no)) if UIDK else str(no)


def gp_expect(rj, no, uid):
    """그 기록(원격)을 받은 기기의 GP[uid] 글 — 번호 칸 · uid 칸 둘 다면 도장이 늦은 쪽(같으면 uid 칸)이 이긴다(§A-2) · 둘 다 없으면 None"""
    g = (rj.get('data') or {}).get('gpt') or {}
    u = rj.get('u') or {}
    a, b = g.get(str(no)), g.get(uid)
    if a is not None and b is not None:
        return a if (u.get('gpt|%s' % no) or 0) > (u.get('gpt|%s' % uid) or 0) else b
    return b if b is not None else a


def gpx(rj, no):
    """이 번호 칸의 글(그 기록 기준) — 옛 판이면 옛 줄 그대로 번호 칸"""
    return gp_expect(rj, no, N2U[str(no)]) if UIDK else (rj['data'].get('gpt') or {}).get(str(no))


def rec_get(d, no):
    """기록 칸에서 이 번호의 값 — 번호 칸이 없으면(uid 열쇠로 옮겨 올린 기록) 그 번호의 uid 칸"""
    d = d or {}
    return d.get(str(no)) if (str(no) in d or not UIDK) else d.get(N2U.get(str(no)))


def known_mat(k, t):
    """글이 그 번호의 재료다 — 옛 재료(earth_<번호>.md) 또는 D-2 새 재료(earth_<uid>.md)"""
    return t == _old_mat(k) or bool(UIDK and t is not None and t == mat_uid(N2U[str(k)]))


def uidify(st):
    """바탕 판 motion 묶음(옛 번호 이름 · 번호 목록)을 uid 열쇠판 앱이 읽는 꼴로 — earth_<번호>.html → earth_<uid>.html · index.json 의 earth = uid 문자열(§D-1) · 파일 바이트는 그대로"""
    out = {}
    for k, v in st.items():
        m = re.fullmatch(r'motion/earth_(\d+)\.html', k)
        if m and m.group(1) in N2U:
            out['motion/earth_%s.html' % N2U[m.group(1)]] = v
        elif k == 'motion/index.json':
            j = json.loads(v.decode('utf-8'))
            if 'earth' in j:
                j['earth'] = [N2U.get(str(x), x) if isinstance(x, int) else x for x in (j.get('earth') or [])]
            out[k] = json.dumps(j, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        else:
            out[k] = v
    return out


def gp_qa_split(src):
    """앱 gpQaSplit 과 같은 규칙(§C-3) — 풀이 글 첫 줄이 「지학QA E008 · 질문일 2026-10-04」 꼴이면 (그 줄, 그 줄과 바로 뒤 빈 줄을 뺀 나머지) · 아니면 ('', 통째)"""
    t = str(src or '')
    L = t.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    if not L or not GP_QA.match(L[0].strip()):
        return '', t
    rest = L[1:]
    while rest and not rest[0].strip():
        rest.pop(0)
    return L[0].strip(), '\n'.join(rest)


def _gp_sep(r):
    return '-' in r and re.fullmatch(r'[\s|:\-]+', r) is not None


def _gp_cells(r):
    r = re.sub(r'\|$', '', re.sub(r'^\|', '', r.strip()))
    return [x.strip() for x in r.split('|')]


def gp_counts(src):
    """앱 gpRender 문법(빈 줄 · | 표 · ①~⑩ 절 머리 · - 글머리 · 1. 번호 · 그 밖 문단 · **굵게**)으로 읽기 판 DOM 개수를 글에서 센다 — 옛 재료는 옛 하네스가 박아 둔 값과 같다(오프라인 대조)"""
    L = str(src or '').replace('\r\n', '\n').replace('\r', '\n').split('\n')
    c = dict(h3=0, h3t='', li=0, ol=0, tb=0, th=0, tr=0, b=0)
    i = 0
    while i < len(L):
        x = L[i]
        if not x.strip():
            i += 1
            continue
        if '|' in x:
            rows = []
            while i < len(L) and '|' in L[i]:
                rows.append(L[i])
                i += 1
            body = [r for r in rows if not _gp_sep(r)]
            head = body.pop(0) if (len(rows) > 1 and _gp_sep(rows[1]) and body) else None
            c['tb'] += 1
            if head is not None:
                hc = _gp_cells(head)
                c['th'] += len(hc)
                c['b'] += sum(len(GP_BOLD.findall(z)) for z in hc)
            for r in body:
                rc = _gp_cells(r)
                c['tr'] += 1
                c['b'] += sum(len(GP_BOLD.findall(z)) for z in rc)
            continue
        m = GP_SEC.match(x)
        if m:
            c['h3'] += 1
            c['h3t'] += m.group(1)
            c['b'] += len(GP_BOLD.findall(m.group(2)))
            i += 1
            continue
        if GP_UL.match(x):
            while i < len(L) and GP_UL.match(L[i]):
                c['li'] += 1
                c['b'] += len(GP_BOLD.findall(GP_UL.sub('', L[i], count=1)))
                i += 1
            continue
        if GP_OL.match(x):
            while i < len(L) and GP_OL.match(L[i]):
                c['ol'] += 1
                c['b'] += len(GP_BOLD.findall(GP_OL.sub('', L[i], count=1)))
                i += 1
            continue
        while i < len(L) and L[i].strip() and '|' not in L[i] and not GP_SEC.match(L[i]) and not GP_UL.match(L[i]) and not GP_OL.match(L[i]):
            c['b'] += len(GP_BOLD.findall(L[i]))
            i += 1
    return c


def gpt_title(it):
    """§C-1 — 제목 = uid + ' Claude' + (정답 있으면 ' · 정답 ' + CIRC[정답−1] [+ ' ' + 자음 선택지 글(㉠㉡… → ㄱㄴ… · 쉼표+빈칸 → ·)] [+ ' (옳지 않은 것)'])"""
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


def mk(no):
    """지학 모션 열쇠(§D-1) — uid 열쇠판이면 uid · 옛 판이면 번호 글자"""
    return N2U[str(no)] if UIDK else str(no)


def dumps(d):
    return json.dumps(d, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


def git1(repo, *a):
    return HU.git(repo, *a).decode('utf-8', 'replace').strip()


def seed_rev():
    """studyplandata — 「gpt|97」 을 처음 넣은 커밋(없으면 '' = 아직 커밋 전)"""
    s = ARG('--seed', '')
    if s:
        return s
    L = git1(SPD, 'log', '--reverse', '--format=%h', '-S', '"gpt|%s"' % NO, '--', RP).split()
    return L[0] if L else ''


def lane_rev():
    """genie — phys_97.html 을 처음 더한 커밋(없으면 '' = 아직 커밋 전)"""
    L = git1(GENIE, 'log', '--reverse', '--diff-filter=A', '--format=%h', '--', MOTF).split()
    return L[0] if L else ''


def recs():
    head = HU.git(SPD, 'show', 'HEAD:' + RP)
    wt = open(os.path.join(SPD, 'phys', '기록.json'), 'rb').read()
    dw = json.loads(wt.decode('utf-8'))
    if (dw['data'].get('gpt') or {}).get(NO) == MD:
        b = json.loads(wt.decode('utf-8'))   # 바탕 = 지금 기록에서 이 판의 두 칸만 뺀 것(다른 칸은 같게)
        b['data']['gpt'].pop(NO, None); b['u'].pop('gpt|' + NO, None); b.get('gone', {}).pop('gpt|' + NO, None)
        return wt, dumps(b), '적재 뒤 실물'
    d = json.loads(head.decode('utf-8'))
    d['data'].setdefault('gpt', {})[NO] = MD; d['u']['gpt|' + NO] = int(time.time() * 1000)
    return dumps(d), head, '합성(적재 전)'


def statics():
    mdir = os.path.join(GENIE, 'jagwa', 'motion')
    new = {'motion/' + f: open(os.path.join(mdir, f), 'rb').read() for f in os.listdir(mdir) if os.path.isfile(os.path.join(mdir, f))}
    base = {}
    for f in git1(GENIE, 'ls-tree', '--name-only', BASE_REV, 'jagwa/motion/').split():
        base['motion/' + f.split('/')[-1]] = HU.git(GENIE, 'show', BASE_REV + ':' + f)
    assert base, 'NG 바탕 motion 을 못 읽었다(%s)' % BASE_REV
    return new, base


def nk(st):
    """물리 gg 의 난수 열쇠 k 를 뺀 사본(HU.nok 와 같은 까닭)"""
    st = json.loads(json.dumps(st or {}))
    for v in ((st.get('gg') or {}).values() if isinstance(st.get('gg'), dict) else []):
        for g in (v or []):
            if isinstance(g, dict):
                g.pop('k', None)
    return st


CJS = r"""
window.__C={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 async open(no){try{closeView()}catch(e){}await new Promise(r=>setTimeout(r,150));await openView(no);await new Promise(r=>setTimeout(r,1200));
   const b=document.getElementById('tGpt');return {btn:__C.tx(b),vis:!!b&&b.offsetParent!==null&&b.getBoundingClientRect().width>0}},
 sheet(){const s=[...document.querySelectorAll('.sheet')].pop();if(!s)return null;const rd=s.querySelector('.gpread');
   return {h2:__C.tx(s.querySelector('.panel > h2')),p:__C.tx(s.querySelector('.panel > p')),read:!!rd,edit:!!s.querySelector('#gpIn'),
     h3:rd?rd.querySelectorAll('h3.gph').length:0,h3t:rd?[...rd.querySelectorAll('h3.gph')].map(x=>__C.tx(x).charAt(0)).join(''):'',
     li:rd?rd.querySelectorAll('ul.gpul li').length:0,ol:rd?rd.querySelectorAll('ol.gpol li').length:0,
     tb:rd?rd.querySelectorAll('table').length:0,b:rd?rd.querySelectorAll('b').length:0,script:rd?rd.querySelectorAll('script').length:0,
     p1:rd?((rd.querySelector('p.gpp')||{}).innerText||''):'',text:rd?rd.textContent:'',
     /* 옛: mot:(()=>{const m=s.querySelector('#gpMotBar');return !!m&&m.style.display!=='none'})(),motTx:__C.tx(s.querySelector('#gpMot'))}}, — ★ uid_unify §C-2 카드 층(지학) 창은 #gpMotBar 줄이 없고 둘째 줄(#gpSub) 오른쪽에 「▶ 모션」(#gpMot) · 물리 창은 옛 꼴 그대로 */
     mot:(()=>{const m=s.querySelector('#gpMotBar');return (!!m&&m.style.display!=='none')||!!s.querySelector('#gpSub #gpMot')})(),motTx:__C.tx(s.querySelector('#gpMot'))}},
 closeSheets(){document.querySelectorAll('.sheet').forEach(x=>x.remove())},
 async frame(){const f=document.getElementById('gpMotFrame');if(!f)return null;
   for(let i=0;i<60;i++){try{const d=f.contentDocument;if(d&&d.readyState==='complete'&&d.body&&d.body.children.length)break}catch(e){}await new Promise(r=>setTimeout(r,150))}
   await new Promise(r=>setTimeout(r,300));
   let d=null;try{d=f.contentDocument}catch(e){return {src:f.getAttribute('src'),same:false}}
   if(!d)return {src:f.getAttribute('src'),same:false};
   const st=await fetch(f.getAttribute('src'),{cache:'no-store'}).then(r=>r.status).catch(()=>0);
   const big=[...d.querySelectorAll('a')].find(x=>/크게 보기/.test(x.textContent));
   const r=f.getBoundingClientRect();
   return {src:f.getAttribute('src'),status:st,same:new URL(f.src,location.href).origin===location.origin,h:Math.round(r.height),w:Math.round(r.width),
     canvas:d.querySelectorAll('canvas').length,cw:[...d.querySelectorAll('canvas')].map(c=>c.width),card:d.querySelectorAll('svg.card').length,
     big:big?[big.getAttribute('href'),big.getAttribute('target')]:null,cv:!!d.getElementById('cv'),
     e1:__C.tx(d.getElementById('e1')),e2:__C.tx(d.getElementById('e2')),play:__C.tx(d.getElementById('play')),tout:__C.tx(d.getElementById('tout')),
     text:d.body?d.body.textContent:''}},
 frameNow(){const d=document.getElementById('gpMotFrame').contentDocument;
   return {e1:__C.tx(d.getElementById('e1')),e2:__C.tx(d.getElementById('e2')),play:__C.tx(d.getElementById('play')),tout:__C.tx(d.getElementById('tout'))}},
 gpNos(){return Object.keys(GP).map(Number).sort((a,b)=>a-b)},
 async mot(){try{await motLoad()}catch(e){}return (typeof MOT==='undefined')?'없음':MOT},
 resetFL(){try{FL.past='';FL.q='';FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';FL.lv='';FL.star=false;FL.year=''}catch(e){}
   try{closeView()}catch(e){}try{draw()}catch(e){}},
 listTags(){const m={};DATA.forEach(r=>{m[String(typeof codeShow==='function'?codeShow(r):r[F.CODE])]=r[F.NO]});
   const it=[...document.querySelectorAll('#list .item')],g=it.filter(d=>d.querySelector('.tag.gp'));
   const noOf=d=>{const u=d.dataset.uid;if(u){const r=DATA.find(x=>x[F.CODE]===u);return r?r[F.NO]:'?'+u}
     const t=__C.tx(d.querySelector('.num'));return m[t]!=null?m[t]:'?'+t};
   return {n:it.length,rows:DATA.length,tags:g.map(noOf).sort((a,b)=>a-b),txt:[...new Set(g.map(d=>__C.tx(d.querySelector('.tag.gp'))))]}}
};
"""


def load(dv, app, subj, rec, stat):
    dv.load(app, SPD, subj, rec={'%s/기록.json' % subj: rec} if rec else None, static=stat)
    dv.cerr = []
    dv.pg.on('console', lambda m: dv.cerr.append('%s @%s' % (m.text[:160], ((m.location or {}).get('url') or '')[-48:])) if m.type == 'error' else None)
    dv.ev(CJS)
    dv.ev("()=>__J.sync()"); dv.pg.wait_for_timeout(800)


def dv_open(br, eng, app, subj, rec, stat):
    dv = HU.Dev(br, eng)
    load(dv, app, subj, rec, stat)
    return dv


def click(dv, sel):
    r = dv.ev("s=>{const e=document.querySelector(s);if(!e)return null;e.scrollIntoView({block:'nearest'});const b=e.getBoundingClientRect();"
              "if(b.width<=0||b.height<=0)return null;return [b.x+b.width/2,b.y+b.height/2]}", sel)
    if not r:
        return False
    dv.pg.mouse.click(r[0], r[1]); dv.pg.wait_for_timeout(700)
    return True


def run_side(br, eng, who, app, rec, stat):
    out = {}
    dv = dv_open(br, eng, app, SUBJ, rec, stat)
    try:
        out['mot'] = dv.ev("()=>__C.mot()")
        dv.ev("()=>__C.resetFL()"); dv.pg.wait_for_timeout(700)
        out['list'] = dv.ev("()=>__C.listTags()")
        out['gp'] = dv.ev("()=>__C.gpNos()")
        for no in (97, 72):
            o = {'btn': dv.ev("n=>__C.open(n)", no)}
            o['clicked'] = click(dv, '#tGpt'); dv.pg.wait_for_timeout(900)
            o['sheet'] = dv.ev("()=>__C.sheet()")
            if o['sheet'] and o['sheet']['mot']:
                click(dv, '#gpMot'); dv.pg.wait_for_timeout(1500)
                o['frame'] = dv.ev("()=>__C.frame()")
                if no == 97 and o['frame'] and o['frame'].get('same') and o['frame'].get('canvas'):
                    try:   # iframe 안 「▶ 재생」 = 진짜 누름(합성 click() 아님) → t 0 → 4(약 6.7초) 끝까지 기다린다
                        dv.pg.frame_locator('#gpMotFrame').locator('#play').click(timeout=15000)
                        t0 = time.time(); now = {}
                        while time.time() - t0 < 25:
                            dv.pg.wait_for_timeout(500)
                            now = dv.ev("()=>__C.frameNow()")
                            if now.get('tout') == 't = 4.00' and now.get('play') == '▶ 재생':
                                break
                        o['frame']['after'] = now; o['frame']['secs'] = round(time.time() - t0, 1)
                    except Exception as e:
                        o['frame']['after'] = {'err': repr(e)[:200]}
            dv.ev("()=>__C.closeSheets()")
            out[no] = o
        nb = {}
        for n in NEIGH:   # 이웃 번호 — 창은 뜨지만(글 없음 → 고치기 판) 모션 단추는 0
            dv.ev("n=>__C.open(n)", n); click(dv, '#tGpt'); dv.pg.wait_for_timeout(900)
            s = dv.ev("()=>__C.sheet()"); nb[n] = {'sheet': bool(s), 'mot': bool(s and s['mot'])}; dv.ev("()=>__C.closeSheets()")
        out['nb'] = nb
        out['gpText'] = dv.ev("()=>Object.fromEntries(Object.entries(GP))")
        out['keys'] = dv.ev("()=>SYNC_KEYS.filter(k=>k!=='gpt')")
        out['stores'] = nk(dv.ev("k=>__J.stores(k)", out['keys']))   # 빈 기기 — gpt 말고 나머지 칸(새 판·바탕이 같아야)
        out['body'] = dv.ev("p=>__J.lastPut(p)", RP)
        out['errs'] = dv.errs[:5]
        out['cerr'] = list(dv.cerr)[:10]
    finally:
        dv.close()
    return out


def earth_side(br, eng, app, stat):
    """지학 149·84 — 모션 단추·iframe 이 바탕(같은 기록 · motion 만 다름)과 같은가"""
    dv = dv_open(br, eng, app, 'earth', None, stat)
    o = {}
    try:
        o['mot'] = dv.ev("()=>__C.mot()")
        for no in (149, 84):
            dv.ev("n=>__C.open(n)", no); click(dv, '#tGpt'); dv.pg.wait_for_timeout(900)
            s = dv.ev("()=>__C.sheet()") or {}
            f = {}
            if s.get('mot'):
                click(dv, '#gpMot'); dv.pg.wait_for_timeout(1500)
                f = dv.ev("()=>__C.frame()") or {}
            o[no] = {'read': s.get('read'), 'mot': s.get('mot'), 'src': f.get('src'), 'status': f.get('status'), 'same': f.get('same'), 'card': f.get('card')}
            dv.ev("()=>__C.closeSheets()")
    finally:
        dv.close()
    return o


def main():
    rn, rb, how = recs()
    sn, sb = statics()
    sb_raw = sb   # 옛 번호 이름 그대로(라벨 · 옛 값 표시용) — 아래 sb 는 uid 열쇠판 앱에 먹이려고 지학 모션 이름·목록을 uid 로 옮긴 것(§D-1 · 물리 쪽은 그대로)
    if UIDK:
        sb = uidify(sb)
    app = HU.git(GENIE, 'show', 'HEAD:jagwa/index.html')
    wt = open(os.path.join(GENIE, 'jagwa', 'index.html'), 'rb').read().replace(b'\r\n', b'\n')
    jn, jb = json.loads(rn.decode('utf-8')), json.loads(rb.decode('utf-8'))
    SEED, LANE = seed_rev(), lane_rev()
    print('기록 = %s · 앱 = genie HEAD jagwa/index.html(작업트리와 %s) · 이 판 genie 커밋 %s · 적재 커밋 %s' % (
        how, '같음' if wt == app else '다름', LANE or '(커밋 전)', SEED or '(커밋 전)'))
    t0 = time.time()
    base_fail = {}
    with sync_playwright() as pw:
        for eng in ENGS:
            br = getattr(pw, eng).launch()
            try:
                N = run_side(br, eng, 'NEW', app, rn, sn)
                B = run_side(br, eng, 'BASE', app, rb, sb)
                n, b = N[97], B[97]
                s, sbs = n['sheet'] or {}, b['sheet'] or {}
                ok1 = n['btn']['btn'] == 'Claude ✓' and n['btn']['vis'] and n['clicked'] and s.get('h2', '').startswith('97번 Claude 풀이') \
                    and s.get('read') and not s.get('edit') and 'PA1109' in s.get('p', '') and 'undefined' not in s.get('p', '')
                okb1 = b['btn']['btn'] == 'Claude ✓' and bool(sbs.get('read'))
                R(eng, 'B-1 97 — 툴바 「Claude ✓」 · 창 제목 「97번 Claude 풀이」 · 읽기 판이 먼저(고치기 칸 없음)', ok1, okb1,
                  {'단추': n['btn'], '제목': s.get('h2'), '둘째 줄': s.get('p'), '바탕 단추': b['btn']['btn'], '바탕 읽기 판': sbs.get('read')})
                head = [x.strip() for x in MD.split('\n\n')[0].replace('**', '').split('\n')]
                p1 = [x.strip() for x in (s.get('p1') or '').split('\n')]
                ok2 = all(s.get(k) == v for k, v in WANT.items()) and s.get('script') == 0 and p1 == head
                R(eng, 'B-1 97 읽기 판 — h3.gph 5(①~⑤) · ul.gpul li 17 · ol.gpol li 5 · <b> 3 · table 0 · script 0 · 원문 첫 문단 = 첫 p', ok2,
                  all(sbs.get(k) == v for k, v in WANT.items()),
                  dict({k: s.get(k) for k in list(WANT) + ['script']}, 첫문단=p1 == head))
                f = n.get('frame') or {}
                fa = f.get('after') or {}
                ok3 = s.get('mot') and s.get('motTx') == '▶ 모션' and f.get('src') == 'motion/phys_97.html' and f.get('status') == 200 and f.get('same') \
                    and abs((f.get('h') or 0) - 480) <= 2 and f.get('canvas') == 2 and all((x or 0) > 0 for x in (f.get('cw') or [0])) \
                    and f.get('big') == ['phys_97.html', '_blank']
                R(eng, 'B-2 97 모션 — 「▶ 모션」 · iframe motion/phys_97.html 200 · 같은 출처 · 480px · iframe 안 canvas 2(폭 잡음) · 「크게 보기」 phys_97.html _blank', ok3,
                  bool(sbs.get('mot')), {k: f.get(k) for k in ('src', 'status', 'same', 'h', 'canvas', 'cw', 'big')})
                e1a, e2a = fa.get('e1') or '', fa.get('e2') or ''
                ok4 = (MINUS + '3mv') in e1a and '그대로' in e2a and (MINUS + '3mv') not in (f.get('e1') or '') and fa.get('tout') == 't = 4.00'
                R(eng, 'B-2 97 모션 재생(iframe 「▶ 재생」 진짜 누름) — 재생 뒤 #e1 에 「−3mv」 · #e2 에 「그대로」 · 재생 앞 #e1 에는 「−3mv」 없음(스크립트가 돌았다)', ok4, None,
                  {'앞 e1': (f.get('e1') or '')[:60], '뒤 e1': e1a[-60:], '뒤 e2': e2a[-40:], 'tout': fa.get('tout'), '초': f.get('secs'), 'err': fa.get('err')})
                n72, b72 = N[72], B[72]
                f72, fb72 = n72.get('frame') or {}, b72.get('frame') or {}
                k72 = ('src', 'status', 'same', 'cv')
                ok5 = n72['btn']['btn'] == 'Claude ✓' and (n72['sheet'] or {}).get('mot') and f72.get('src') == 'motion/phys_72.html' and f72.get('status') == 200 \
                    and f72.get('cv') and {k: f72.get(k) for k in k72} == {k: fb72.get(k) for k in k72} and N['gpText'].get('72') == B['gpText'].get('72')
                R(eng, 'B-2 72 — 「Claude ✓」 · 모션 단추 · iframe motion/phys_72.html = 바탕(무변) · GP[72] = 바탕', ok5, None,
                  {'NEW': {k: f72.get(k) for k in k72}, 'BASE': {k: fb72.get(k) for k in k72}})
                mp = (N['mot'] or {}).get('phys') if isinstance(N['mot'], dict) else None
                mb = (B['mot'] or {}).get('phys') if isinstance(B['mot'], dict) else None
                j0 = json.loads(sb['motion/index.json'])
                want_mp = (j0.get('phys') or []) + [97]
                R(eng, 'B-2 물리 모션 번호(MOT.phys) = 바탕 %s + 97 로 시작 — 지금 %s' % (j0.get('phys'), mp), (mp or [])[:len(want_mp)] == want_mp,
                  (mb or [])[:len(want_mp)] == want_mp, {'NEW': mp, 'BASE': mb})
                R(eng, 'B-2 물리 96·98 — 모션 단추 0(창은 뜸)', all(v['sheet'] and not v['mot'] for v in N['nb'].values()), None, N['nb'])
                En, Eb = earth_side(br, eng, app, sn), earth_side(br, eng, app, sb)
                # 옛 줄: oke = all(En[k]['mot'] and En[k]['status'] == 200 and En[k]['card'] == 1 and En[k]['src'] == 'motion/earth_%d.html' % k for k in (149, 84)) \
                # 옛 줄: and {k: En[k] for k in (149, 84)} == {k: Eb[k] for k in (149, 84)}
                oke = all(En[k]['mot'] and En[k]['status'] == 200 and En[k]['card'] == 1 and En[k]['src'] == 'motion/earth_%s.html' % mk(k) for k in (149, 84)) \
                    and {k: En[k] for k in (149, 84)} == {k: Eb[k] for k in (149, 84)}   # ★ uid_unify §D-1 — 지학 모션 파일 = earth_<uid>.html · 바탕 motion 도 uid 이름·목록으로 옮겨 맞댄다
                R(eng, 'B-2 지학 149·84 — 모션 단추·iframe(motion/earth_149·84.html 200 · svg.card 1) = 바탕(무변)', oke, None, {'NEW': {k: En[k] for k in (149, 84)}, '같음': oke})
                merr = [x for x in (N['cerr'] or []) if 'motion/' in x]
                R(eng, 'B-2 모션 iframe 쪽 콘솔 오류 0 · 앱 페이지 오류 0', not merr and not N['errs'], None, {'모션': merr, '앱 pageerror': N['errs'], '앱 콘솔(참고)': N['cerr'][:4]})
                # ── B-3 데이터 ──
                gk = [k for k in N['keys'] if N['stores'].get(k) != B['stores'].get(k)]
                g72 = (jn['data'].get('gpt') or {}).get('72')
                body = json.loads(N['body']) if N['body'] else None
                okb_ = body is None or ((body.get('data', {}).get('gpt') or {}).get(NO) == MD and (body.get('data', {}).get('gpt') or {}).get('72') == g72
                                        and set(body.get('gone') or {}) <= set(jn.get('gone') or {}))
                ok6 = N['gpText'].get(NO) == MD and N['gpText'].get('72') == g72 and bool(g72) and B['gpText'].get('72') == g72
                R(eng, 'B-3 빈 기기 — 동기화 뒤 GP[97] = 재료 글자 전수(%d자) · GP[72] = 기록 값 무변(%d자)' % (len(MD), len(g72 or '')), ok6, B['gpText'].get(NO) == MD,
                  {'97 길이': len(N['gpText'].get(NO) or ''), '72 같음': N['gpText'].get('72') == g72})
                R(eng, 'B-3 빈 기기 — gpt 말고 동기화 칸 %d 가 바탕과 같다 · GP 칸 = 바탕 + 97(지워진 칸 0) · 올린 몸통 gpt 97·72 · 묘비 늘지 않음' % len(N['keys']),
                  not gk and N['keys'] == B['keys'] and set(N['gp']) == set(B['gp']) | {97} and okb_, None,
                  {'다른 칸': gk, 'GP': [N['gp'], B['gp']], '올린 몸통': 'PUT 없음' if body is None else 'gpt %s' % sorted((body.get('data', {}).get('gpt') or {}).keys())})
                # 기록 있는 기기 — 97 없는 기록으로 먼저 열고 5번 △(툴바 #mQ)를 진짜로 눌러(내 칸이 더 새것) 둔 뒤 적재 뒤 원격을 받는다
                dv = dv_open(br, eng, app, SUBJ, rb, sn)
                try:
                    keys = dv.ev("()=>SYNC_KEYS.filter(k=>k!=='gpt')")
                    dv.ev("n=>__C.open(n)", 5); h0 = dv.ev("()=>((ST[5]||{}).h||[]).length")
                    cq = click(dv, '#mQ'); dv.pg.wait_for_timeout(600); h1 = dv.ev("()=>((ST[5]||{}).h||[]).length")
                    dv.ev("()=>{try{closeView()}catch(e){}}"); dv.ev("()=>__J.sync()")
                    before = nk(dv.ev("k=>__J.stores(k)", keys))
                    load(dv, app, SUBJ, rn, sn)
                    after = nk(dv.ev("k=>__J.stores(k)", keys))
                    gp = dv.ev("()=>Object.fromEntries(Object.entries(GP))")
                    body = json.loads(dv.ev("p=>__J.lastPut(p)", RP) or '{}')
                    bd = body.get('data', {})
                    same = {k: before.get(k) == after.get(k) for k in keys}
                    ok = cq and h1 == h0 + 1 and gp.get(NO) == MD and gp.get('72') == g72 and all(same.values()) \
                        and len(((after.get('status') or {}).get('5') or {}).get('h') or []) == h1 \
                        and (bd.get('gpt') or {}).get(NO) == MD and len(((bd.get('status') or {}).get('5') or {}).get('h') or []) == h1
                    R(eng, 'B-3 기록 있는 기기 — 동기화 뒤 GP[97] = 재료 · GP[72] 무변 · 다른 칸 %d 무변 · 내 새 칸(5번 △ 진짜 누름) 안 덮임 · 올린 몸통에 97·5번 둘 다' % len(keys), ok, None,
                      {'다른 칸': [k for k in keys if not same[k]], 'GP97': len(gp.get(NO) or ''), '5번 회독': [h0, h1], '누름': cq})
                finally:
                    dv.close()
                # 내 것이 더 새것 — 97 없는 기록 기기에서 97 Claude 창에 써서 저장(진짜 누름 · 원격 도장보다 뒤) → 적재 뒤 원격을 받아도 안 덮인다
                dv = dv_open(br, eng, app, SUBJ, rb, sn)
                try:
                    MY = '내가 먼저 쓴 97번(검산)'
                    dv.ev("n=>__C.open(n)", 97); click(dv, '#tGpt'); dv.pg.wait_for_timeout(700)
                    dv.pg.locator('#gpIn').fill(MY); click(dv, '#gpSave'); dv.pg.wait_for_timeout(700)
                    dv.ev("()=>__C.closeSheets()"); dv.ev("()=>{try{closeView()}catch(e){}}"); dv.ev("()=>__J.sync()")
                    load(dv, app, SUBJ, rn, sn)
                    g = dv.ev("()=>({a:GP[97]||'',b:GP[72]||''})")
                    body = json.loads(dv.ev("p=>__J.lastPut(p)", RP) or '{}')
                    bg = body.get('data', {}).get('gpt') or {}
                    ok = g['a'] == MY and g['b'] == g72 and bg.get(NO) == MY and bg.get('72') == g72
                    R(eng, 'B-3 내 것이 더 새것 — 원격 도장 뒤에 고친 GP[97] 는 원격이 못 덮는다(claude_slot CL-6 ⓒ 잣대) · GP[72] 그대로 · 올린 몸통도 내 것', ok, None,
                      {'97': g['a'][:24], '72 같음': g['b'] == g72, '올린 97': (bg.get(NO) or '')[:24]})
                finally:
                    dv.close()
                # ── B-4 목록 ──
                want = sorted(int(k) for k in (jn['data'].get('gpt') or {}))
                okl = N['list']['tags'] == want and 97 in want and 72 in want and N['list']['txt'] == ['Claude']
                R(eng, 'B-4 목록 — .tag.gp 「Claude」 줄 = 기록 gpt 칸 번호 %s(물리 97·72) · 다른 줄 0' % want, okl, B['list']['tags'] == want,
                  {'NEW': N['list'], 'BASE 태그': B['list']['tags']})
                base_fail[eng] = {'B-1': not okb1, 'B-2': not bool(sbs.get('mot')) and (mb or [])[:len(want_mp)] != want_mp, 'B-4': B['list']['tags'] != want}
            finally:
                br.close()
    # ── 헛잣대 · 정적 ──
    for eng, bf in base_fail.items():
        R(eng, 'B-6 헛잣대 — 바탕(옛 index.json · 97 없는 기록)에서 B-1·B-2·B-4 가 FAIL', all(bf.values()), None, bf)
    # 앱 무변 — 작업트리 = HEAD · 이 판 genie 커밋이 앱을 안 건드림(커밋 전이면 작업트리에서 바뀐 것이 motion 뿐)
    if LANE:
        lf = git1(GENIE, 'diff', '--name-only', LANE + '~1', LANE).split()
        jx = json.loads(HU.git(GENIE, 'show', LANE + ':jagwa/motion/index.json').decode('utf-8'))
        j1 = json.loads(HU.git(GENIE, 'show', LANE + '~1:jagwa/motion/index.json').decode('utf-8'))
        where = 'genie 커밋 %s' % LANE
    else:
        lf = [x[3:] for x in HU.git(GENIE, 'status', '--porcelain', '--untracked-files=all', '--', 'jagwa').decode('utf-8', 'replace').split('\n') if x.strip()]   # strip 하면 첫 줄 앞 공백이 빠져 한 글자 더 잘린다(10/1 첫 실행)
        jx, j1 = json.loads(sn['motion/index.json']), json.loads(HU.git(GENIE, 'show', 'HEAD:jagwa/motion/index.json').decode('utf-8'))
        where = 'genie 작업트리(커밋 전)'
    R('-', 'B-5 jagwa/index.html 바이트 무변 — 작업트리 = HEAD · %s 가 바꾼 파일 = motion 둘뿐 %s' % (where, lf),
      wt == app and sorted(lf) == sorted(['jagwa/motion/index.json', MOTF]), None, hashlib.md5(wt).hexdigest()[:8])
    R('-', 'A-1 이 판이 남긴 motion/index.json(%s) = 앞 판 값에 phys 97 만 더함 — phys %s → %s · earth %s 무변 · 키 무변' % (where, j1.get('phys'), jx.get('phys'), j1.get('earth')),
      jx.get('phys') == (j1.get('phys') or []) + [97] and jx.get('earth') == j1.get('earth') and set(jx) == set(j1), None, json.dumps(jx))
    j, j0 = json.loads(sn['motion/index.json']), json.loads(sb['motion/index.json'])
    # 옛 줄: R('-', 'A-1 지금 motion/index.json — phys 가 바탕 %s + [97] 로 시작 · earth 가 바탕 %s 로 시작(값·차례 무변 · 뒤 판이 끝에 더한 것만 허용) · 바탕 키 다 있음' % (j0.get('phys'), j0.get('earth')),
    j0r = json.loads(sb_raw['motion/index.json'])   # 옛 번호 그대로 — 라벨용(판이 달라도 같은 줄 이름) · 조건의 j0 는 uid 로 옮긴 바탕 목록(§D-1)
    R('-', 'A-1 지금 motion/index.json — phys 가 바탕 %s + [97] 로 시작 · earth 가 바탕 %s 로 시작(값·차례 무변 · 뒤 판이 끝에 더한 것만 허용) · 바탕 키 다 있음' % (j0r.get('phys'), j0r.get('earth')),
      (j.get('phys') or [])[:len(j0.get('phys') or []) + 1] == (j0.get('phys') or []) + [97] and (j.get('earth') or [])[:len(j0.get('earth') or [])] == (j0.get('earth') or [])
      and set(j0) <= set(j), False, sn['motion/index.json'].decode().strip())
    # 적재가 두 칸(+savedAt)만 더했나
    if SEED:
        fs = git1(SPD, 'diff', '--name-only', SEED + '~1', SEED).split()
        old, new = HU.git(SPD, 'show', SEED + '~1:' + RP), HU.git(SPD, 'show', SEED + ':' + RP)
        where = 'studyplandata 커밋 %s' % SEED
    else:
        fs = [x[3:] for x in HU.git(SPD, 'status', '--porcelain').decode('utf-8', 'replace').split('\n') if x.strip()]
        old, new = HU.git(SPD, 'show', 'HEAD:' + RP), open(os.path.join(SPD, 'phys', '기록.json'), 'rb').read()
        where = 'studyplandata HEAD → 작업트리(커밋 전)'
    do, dn = json.loads(old.decode('utf-8')), json.loads(new.decode('utf-8'))
    if NO in (dn['data'].get('gpt') or {}) and NO not in (do['data'].get('gpt') or {}):
        x = json.loads(json.dumps(dn)); x['data']['gpt'].pop(NO); x['u'].pop('gpt|' + NO, None)
        y = json.loads(json.dumps(do))
        for z in (x, y):
            z.pop('savedAt', None)
        R('-', 'B-5 적재(%s) — 바꾼 파일 = phys/기록.json 하나 · data.gpt["97"] = 재료 · u["gpt|97"] 둘(+savedAt)만 더함 · 다른 칸·gone 무변(지학·생물 기록 무변)' % where,
          x == y and dn['data']['gpt'][NO] == MD and isinstance(dn['u'].get('gpt|' + NO), int) and fs == [RP], None,
          {'파일': fs, '도장': dn['u'].get('gpt|' + NO), 'savedAt': [do.get('savedAt'), dn.get('savedAt')]})
    else:
        R('-', 'B-5 적재(%s) — 아직 적재 전(합성 기록으로 잼)' % where, None, None, '')
    # 지학 gpt 149·84 · 생물 gpt
    E = json.loads(open(os.path.join(SPD, 'earth', '기록.json'), 'rb').read().decode('utf-8'))
    eg = E['data'].get('gpt') or {}
    Bi = json.loads(open(os.path.join(SPD, 'bio', '기록.json'), 'rb').read().decode('utf-8'))
    R('-', 'B-5 지학 gpt["149"]·["84"] = 재료 글자 그대로(무변) · 생물 gpt = %s' % json.dumps(Bi['data'].get('gpt')),
      # 옛 줄: eg.get('149') == mat('earth_149.md') and eg.get('84') == mat('earth_84.md'), None, {'지학 gpt': sorted(eg, key=int)})
      eg.get('149') == mat('earth_149.md') and eg.get('84') == mat('earth_84.md'), None, {'지학 gpt': sorted(eg, key=lambda z_: (0, int(z_), '') if z_.isdigit() else (1, 0, z_))})   # ★ uid_unify §D-2 — 원격 gpt 에 uid 열쇠 칸이 더해질 수 있다(번호 칸은 그대로)
    # 모션 파일
    f = 'motion/phys_97.html'
    src = open(os.path.join(MAT, 'phys_97.html'), 'rb').read()
    R('-', 'A-1 %s = 재료 바이트(줄끝만 뺀 대조 · 재료 %d B · md5 %s)' % (f, len(src), hashlib.md5(src).hexdigest()[:8]),
      (sn.get(f) or b'').replace(b'\r\n', b'\n') == src.replace(b'\r\n', b'\n'), None, len(sn.get(f) or b''))
    ix = git1(GENIE, 'ls-files', '-s', '--', MOTF).split()
    if ix:
        blob = HU.git(GENIE, 'cat-file', '-p', ix[1])
        R('-', 'A-1 %s git blob = 재료 바이트 그대로(md5 %s)' % (f, hashlib.md5(blob).hexdigest()[:8]), blob == src, None, len(blob))
    else:
        R('-', 'A-1 %s — 아직 git 에 안 올림(blob 대조는 스테이징 뒤)' % f, None, None, '')
    tx = (sn.get(f) or b'').decode('utf-8', 'replace')
    R('-', '%s — 바깥 스크립트·주소 0 · canvas 2 · .pdf 0(공개 genie · D11)' % f,
      not re.search(r'<script[^>]*\bsrc\s*=', tx) and not re.findall(r'https?://', tx) and tx.count('<canvas') == 2 and '.pdf' not in tx.lower(), None,
      re.findall(r'https?://[^\s"\'<>]+', tx)[:3])
    R('-', 'motion 폴더에 .pdf 0', not [k for k in sn if k.lower().endswith('.pdf')], None, sorted(sn))
    npass = sum(1 for r in ROWS if r[2] is True); nfail = sum(1 for r in ROWS if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초 · 기록 %s' % (npass, nfail, time.time() - t0, how))
    with io.open(OUTF, 'a', encoding='utf-8') as fo:
        fo.write('\n==== %s · claude_p002 CP2 · 기록 %s · genie HEAD %s · 바탕 %s · 이 판 커밋 %s · studyplandata HEAD %s · 적재 %s · 엔진 %s ====\n' % (
            time.strftime('%Y-%m-%d %H:%M'), how, git1(GENIE, 'rev-parse', '--short', 'HEAD'), BASE_REV, LANE or '-',
            git1(SPD, 'rev-parse', '--short', 'HEAD'), SEED or '-', ','.join(ENGS)))
        for eng, nm, okn, okb, v in ROWS:
            fo.write('%s | 바탕 %s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[okn], {True: 'PASS', False: 'FAIL', None: '—'}[okb], eng, nm,
                     (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str))[:1200]))
        fo.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
