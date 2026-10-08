# -*- coding: utf-8 -*-
r"""_task_jagwa_claude_e001 · _add1 · _add2 관문 「CE1」 — 지학 149·84 Claude 풀이 · 모션

  python _harness_jagwa_claude_e001.py [--eng chromium,webkit] [--res <결과>]

  NEW = genie 작업트리(motion/index.json · earth_149.html · earth_84.html 더함 · jagwa/index.html 무변)
        + 지학 기록 = studyplandata 작업트리 earth/기록.json(적재 뒤) — 아직 적재 전이면 같은 두 칸을 더한 사본을 만든다(「합성」이라 적음)
  BASE(헛잣대) = genie 인도 앞 커밋(--base · 2998b9e)의 motion/*(84·149 없음) + 기록에서 gpt 149·84 와 그 도장만 뺀 것
        ⚠ 인도 뒤 다시 돌려도 헛잣대가 거저 PASS 가 안 되게 바탕을 HEAD 에서 읽지 않는다(9/29 실측 — HEAD 로 읽으니 모션 줄 바탕이 PASS)
  적재 커밋(--seed · cbd451ae) = studyplandata 에서 earth/기록.json 하나만 건드렸나
  기록은 route 사본 · PUT 은 가로채 밖으로 안 나감 · 앱 코드 한 벌(무변 확인)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기 헬퍼(_task_qa_slim2 A-1-2 · 옛 남 하네스 import 를 갈음)
import io, json, os, re, sys, time, hashlib, subprocess, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = _roots.genie(); SPD = _roots.spd()
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_claude_e001_result.txt'))
MAT = os.path.join(HERE, 'claude_motion')
if not os.path.isdir(MAT):   # ★ 거울 사본(옛 잣대 고침 사본)에서 돌 때 — 재료는 N: 에만 있다(CE4 · CP2 와 같은 자리 · 의미 무변)
    MAT = _roots.n('jagwa', 'gigu', 'claude_motion') or MAT
BASE_REV = ARG('--base', '2998b9e')   # genie — 이 판 인도(802cb0a) 바로 앞 = env_lanes 인도판
SEED_REV = ARG('--seed', 'cbd451ae')  # studyplandata — _gpt_seed.py earth 149 84 --write 커밋
NOS = {'149': {'code': 'G09-46-10', 'li': 19, 'b': 3}, '84': {'code': 'G03-40-05', 'li': 18, 'b': 6}}
ROWS = []
from playwright.sync_api import sync_playwright   # noqa: E402


def R(eng, name, okn, okb, val):
    ROWS.append((eng, name, okn, okb, val))
    print('%s | 바탕 %s | %s · %s | %s' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], eng, name,
          (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str))[:420]), flush=True)


def md(no):
    return io.open(os.path.join(MAT, 'earth_%s.md' % no), encoding='utf-8', newline='').read().replace('\r\n', '\n')


def _old_mat(k):   # 번호 k 의 옛 재료 글(earth_<번호>.md)
    return md(str(k))


# ★ uid_unify 옛 잣대 고침(2026-10-04 · 근거 gigu/_task_jagwa_uid_unify.md §A-1 · §A-2 · §C-1 · §C-2 · §C-3 · §D-1 · §D-2 · §0-6) ───────────────────────────────
#   카드 층(지학) 기록 열쇠 = uid(번호 F.NO 는 화면 자리 번호일 뿐) · Claude 풀이 창 새 꼴(제목 「<uid> Claude · 정답 …」 · 둘째 줄 = 왼쪽 QA 줄 + 오른쪽 「▶ 모션」 글자 ·
#   옛 #gpMotBar 줄 없음 · 읽기 판은 QA 첫 줄을 뺀 나머지) · 모션 파일 motion/earth_<uid>.html · motion/index.json 의 earth = uid 문자열.
#   UIDK(그 앱이 uid 열쇠판인가)가 거짓이면(옛 판 · 바탕) 아래 도우미는 옛 값 그대로 돌려준다 — 옛 줄은 바꾼 자리마다 「# 옛 줄:」 주석으로 남겼다.
#   값을 박지 않는다 — 번호 → uid 는 문항.json 에서 · 하네스가 박아 둔 code 는 닻(§0-6)으로 맞대 본다.
import posixpath   # noqa: E402
UIDK = b'function qk(no)' in (JG.git_HU(GENIE, 'show', 'HEAD:jagwa/index.html') if QC.GATE else open(os.path.join(GENIE, 'jagwa', 'index.html'), 'rb').read())   # 앱이 카드 층 기록 열쇠를 uid 로 쓰는 판인가(§A-1 의 qk(no)) · regress — 작업트리 파일(사슬 = 새 판 워크트리 · git 0)
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


# ── _task_qa_slim2 A-1·A-2(10/8 · J2) regress 갈래 — 이름이 `_rg` · `_RG` 로 시작하는 것 = gate 에서 안 쓰는 도우미(gate 에서 도는 줄은 글자 그대로) ──
#   regress = NEW 쪽만(run_side NEW · 물리 NEW · 기록 기기 둘) — BASE 쪽(2998b9e motion · 두 칸 뺀 기록) · 바탕 motion 풀기(git ls-tree · show) · 앱 무변(작업트리 = HEAD) · 적재 커밋 = gate 만
#   R 줄의 「바탕」 칸(헛잣대) = — · 「기준」 칸(빈 기기 나머지 칸 · 물리 72) = QC.base 스냅샷(앞 인도판의 새 판 값 · md5) · 앱 = 작업트리 파일(HEAD 판 = 새 판 · git show 0)
#   smoke = chromium 한 판 — 149 · 84 「Claude ✓」 · 페이지 오류 0 · 기록 있는 기기(동기화 한 바퀴)
_RG_KEEP = set(x for x in (os.environ.get('QA_SLIM_KEEP_FIXED') or '').split(',') if x)   # 흔들리는 자리만 고정 대기로 되돌리는 손잡이(자리 이름 쉼표 · * = 전부)
_RG_GPSHEET = "()=>{const s=[...document.querySelectorAll('.sheet')].pop();return !!s&&!!s.querySelector('.panel > h2')&&(!!s.querySelector('.gpread')||!!s.querySelector('#gpIn'))}"   # 표지 = 「Claude」 누름 뒤 풀이 창(gptSheet 이 동기로 짓는 머리 · 읽기 판 또는 고치기 판)
_RG_MOTFRAME = "()=>{const f=document.getElementById('gpMotFrame');try{const d=f&&f.contentDocument;return !!d&&d.readyState==='complete'&&d.URL.indexOf(f.getAttribute('src'))>=0&&!!d.body&&d.body.children.length>0}catch(e){return false}}"   # 표지 = 모션 iframe 이 제 src 쪽을 다 읽음(처음 about:blank 은 URL 로 거름)


def _rg_md5(v):
    return hashlib.md5(('' if v is None else (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, sort_keys=True))).encode('utf-8')).hexdigest()


def _rg_wait(dv, ms, js, what):
    """regress — 고정 대기 대신 앱 표지(상한 = gate 의 ms · 못 만나면 남은 시간을 채워 gate 와 같은 길이) · QA_SLIM_KEEP_FIXED 자리는 고정"""
    if js is None or what in _RG_KEEP or '*' in _RG_KEEP:
        QC.sleep(ms, what, dv.pg)
        return
    t = time.time()
    if not QC.until(dv.pg, js, ms, what):
        left = ms - (time.time() - t) * 1000.0
        if left > 1:
            dv.pg.wait_for_timeout(left)


def mk(no):
    """모션 열쇠(§D-1) — uid 열쇠판이면 uid · 옛 판이면 번호 글자"""
    return N2U[str(no)] if UIDK else str(no)


def recs():
    head = JG.git_HU(SPD, 'show', 'HEAD:earth/기록.json') if QC.GATE else None   # regress — 작업트리 기록이 「적재 뒤 실물」이면 git show 0(아래 · 아니면 그때 읽음)
    wt = open(os.path.join(SPD, 'earth', '기록.json'), 'rb').read()
    dw = json.loads(wt.decode('utf-8'))
    if UIDK:   # ★ uid_unify §A-2 · §D-2 — 번호 칸(옛 글) 또는 uid 칸(새 글)이 재료면 「적재 뒤 실물」 · 바탕은 두 칸(+도장·묘비)을 다 뺀다
        g_ = dw['data'].get('gpt') or {}
        if all(g_.get(n) == md(n) or (mat_uid(N2U[n]) is not None and g_.get(N2U[n]) == mat_uid(N2U[n])) for n in NOS):
            b = json.loads(wt.decode('utf-8'))
            for n in NOS:
                for kk in (n, N2U[n]):
                    b['data'].setdefault('gpt', {}).pop(kk, None); b['u'].pop('gpt|' + kk, None); b.get('gone', {}).pop('gpt|' + kk, None)
            return wt, json.dumps(b, ensure_ascii=False, separators=(',', ':')).encode('utf-8'), '적재 뒤 실물'
        if head is None and QC.REGRESS:   # regress — 아직 적재 전이면 HEAD 기록에 두 칸을 더한 합성(gate 와 같은 길)
            QC.sub('git:show-data')
            head = JG.git_HU(SPD, 'show', 'HEAD:earth/기록.json')
        d = json.loads(head.decode('utf-8'))
        now = int(time.time() * 1000)
        for n in NOS:
            d['data'].setdefault('gpt', {})[N2U[n]] = mat_uid(N2U[n]) if mat_uid(N2U[n]) is not None else md(n); d['u']['gpt|' + N2U[n]] = now
        return json.dumps(d, ensure_ascii=False, separators=(',', ':')).encode('utf-8'), head, '합성(적재 전)'
    if all((dw['data'].get('gpt') or {}).get(n) == md(n) for n in NOS):
        b = json.loads(wt.decode('utf-8'))   # 바탕 = 지금 기록에서 이 판의 두 칸과 도장만 뺀 것(다른 칸은 같게)
        for n in NOS:
            b['data']['gpt'].pop(n, None); b['u'].pop('gpt|' + n, None); b.get('gone', {}).pop('gpt|' + n, None)
        return wt, json.dumps(b, ensure_ascii=False, separators=(',', ':')).encode('utf-8'), '적재 뒤 실물'
    if head is None and QC.REGRESS:
        QC.sub('git:show-data')
        head = JG.git_HU(SPD, 'show', 'HEAD:earth/기록.json')
    d = json.loads(head.decode('utf-8'))
    now = int(time.time() * 1000)
    for n in NOS:
        d['data'].setdefault('gpt', {})[n] = md(n); d['u']['gpt|' + n] = now
    return json.dumps(d, ensure_ascii=False, separators=(',', ':')).encode('utf-8'), head, '합성(적재 전)'


def statics():
    mdir = os.path.join(GENIE, 'jagwa', 'motion')
    new = {'motion/' + f: open(os.path.join(mdir, f), 'rb').read() for f in os.listdir(mdir)}
    base = {}
    if not QC.GATE:   # regress — 바탕 motion 안 풂(git 0 · BASE 쪽 문맥 0)
        return new, None
    QC.sub('git:ls-tree'); QC.sub('git:show-app')
    for f in JG.git_HU(GENIE, 'ls-tree', '--name-only', BASE_REV, 'jagwa/motion/').decode('utf-8').split():
        base['motion/' + f.split('/')[-1]] = JG.git_HU(GENIE, 'show', BASE_REV + ':' + f)
    assert base, 'NG 바탕 motion 을 못 읽었다(%s)' % BASE_REV
    return new, base


CJS = r"""
window.__C={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 async open(no){try{closeView()}catch(e){}await new Promise(r=>setTimeout(r,150));await openView(no);await new Promise(r=>setTimeout(r,1200));
   const b=document.getElementById('tGpt');const row=b&&b.parentElement;const vis=[...(row?row.children:[])].filter(x=>x.offsetParent!==null&&getComputedStyle(x).display!=='none');
   return {btn:__C.tx(b),last:vis.length?vis[vis.length-1]===b:false}},
 sheet(){const s=[...document.querySelectorAll('.sheet')].pop();if(!s)return null;const rd=s.querySelector('.gpread');
   return {p:__C.tx(s.querySelector('.panel > p')),read:!!rd,edit:!!s.querySelector('#gpIn'),h3:rd?rd.querySelectorAll('h3.gph').length:0,
     li:rd?rd.querySelectorAll('ul.gpul li').length:0,tb:rd?rd.querySelectorAll('table.gptb').length:0,th:rd?rd.querySelectorAll('table.gptb th').length:0,
     tr:rd?rd.querySelectorAll('table.gptb tbody tr').length:0,b:rd?rd.querySelectorAll('b').length:0,script:rd?rd.querySelectorAll('script').length:0,
     paras:rd?[...rd.querySelectorAll('p')].slice(0,3).map(__C.tx):[],p1:rd?((rd.querySelector('p.gpp')||{}).innerText||''):'',text:rd?rd.textContent:'',
     /* 옛: mot:(()=>{const m=s.querySelector('#gpMotBar');return !!m&&m.style.display!=='none'})()}}, — ★ uid_unify §C-1 · §C-2 카드 층 창은 제목에 uid · #gpMotBar 줄이 없고 둘째 줄(#gpSub) 오른쪽에 「▶ 모션」(#gpMot) */
     h2:__C.tx(s.querySelector('.panel > h2')),sub:!!s.querySelector('.panel > #gpSub'),qa:__C.tx(s.querySelector('#gpQa')),
     mot:(()=>{const m=s.querySelector('#gpMotBar');return (!!m&&m.style.display!=='none')||!!s.querySelector('#gpSub #gpMot')})()}},
 closeSheets(){document.querySelectorAll('.sheet').forEach(x=>x.remove())},
 async frame(){const f=document.getElementById('gpMotFrame');if(!f)return null;for(let i=0;i<40;i++){try{if(f.contentDocument&&f.contentDocument.readyState==='complete'&&f.contentDocument.body)break}catch(e){}await new Promise(r=>setTimeout(r,150))}
   let d=null;try{d=f.contentDocument}catch(e){return {src:f.getAttribute('src'),same:false}}
   const st=await fetch(f.getAttribute('src'),{cache:'no-store'}).then(r=>r.status).catch(()=>0);
   const hide=d.getElementById('hideBtn');
   const big=[...d.querySelectorAll('a')].find(x=>/크게 보기/.test(x.textContent));
   return {src:f.getAttribute('src'),status:st,same:true,card:d.querySelectorAll('svg.card').length,hideBtn:!!hide&&/가리기/.test(hide.textContent),
     /* 옛: ansT:__C.ansOp(d),big:big?big.getAttribute('target'):null,text:d.body?d.body.textContent:''}}, — ★ uid_unify §D-1 「크게 보기」 href 도 잰다 */
     ansT:__C.ansOp(d),big:big?big.getAttribute('target'):null,bigHref:big?big.getAttribute('href'):null,text:d.body?d.body.textContent:''}},
 ansOp(d){return [...d.querySelectorAll('.ans text')].map(t=>getComputedStyle(t).opacity)},
 frameAfter(){const d=document.getElementById('gpMotFrame').contentDocument;const c=d.getElementById('card');
   return {ansT:__C.ansOp(d),pressed:d.getElementById('hideBtn').getAttribute('aria-pressed'),blank:!!c&&c.classList.contains('blank')}},
 gpNos(){return Object.keys(GP).sort()},
 listTags(){return [...document.querySelectorAll('#list .item')].filter(d=>d.querySelector('.tag.gp')).map(d=>+((DATA.find(r=>r[F.CODE]===d.dataset.uid)||[])[0]||0))}
};
"""


def dv_open(br, eng, app, subj, rec, stat, phone=False):
    QC.launch('new')   # 셈(§B-4) — regress 띄움은 다 새 판 앱(바탕 쪽 run_side · 물리 BASE 는 gate 만)
    dv = JG.Dev(br, eng, phone)
    dv.load(app, SPD, subj, rec={'%s/기록.json' % subj: rec} if rec else None, static=stat)
    dv.ev(CJS)
    dv.ev("()=>__J.sync()"); dv.pg.wait_for_timeout(800)
    return dv


def click(dv, sel):
    r = dv.ev("s=>{const e=document.querySelector(s);if(!e)return null;e.scrollIntoView({block:'nearest'});const b=e.getBoundingClientRect();return [b.x+b.width/2,b.y+b.height/2]}", sel)
    if not r:
        return False
    dv.pg.mouse.click(r[0], r[1]); dv.pg.wait_for_timeout(700)
    return True


OLDNUM = re.compile(r'G\d\d-\d\d-\d(?!\d)|(?<![A-Za-z0-9])C\d-\d{3}')


def run_side(br, eng, who, app, rec, stat):
    out = {}
    dv = dv_open(br, eng, app, 'earth', rec, stat)
    try:
        out['list'] = dv.ev("()=>__C.listTags()")
        out['gp'] = dv.ev("()=>__C.gpNos()")
        for no in NOS:
            o = {'btn': dv.ev("n=>__C.open(n)", int(no))}
            click(dv, '#tGpt'); dv.pg.wait_for_timeout(900) if QC.GATE else _rg_wait(dv, 900, _RG_GPSHEET, 'e001.gpsheet')
            o['sheet'] = dv.ev("()=>__C.sheet()")
            if o['sheet'] and o['sheet']['mot'] and not QC.SMOKE:   # smoke — 모션 건넘
                click(dv, '#gpMot'); dv.pg.wait_for_timeout(1500) if QC.GATE else _rg_wait(dv, 1500, _RG_MOTFRAME, 'e001.motframe')
                o['frame'] = dv.ev("()=>__C.frame()")
                if o['frame'] and o['frame'].get('same'):
                    try:   # iframe 안 「가리기」 = 진짜 누름(합성 click() 아님)
                        dv.pg.frame_locator('#gpMotFrame').locator('#hideBtn').click(timeout=15000); dv.pg.wait_for_timeout(600)
                        o['frame']['after'] = dv.ev("()=>__C.frameAfter()")
                    except Exception as e:
                        o['frame']['after'] = {'err': repr(e)[:160]}
            dv.ev("()=>__C.closeSheets()")
            out[no] = o
        # 이웃 번호 · 모션 단추 0
        nb = {}
        for n in ((148, 150, 83, 85) if not QC.SMOKE else ()):   # smoke — 이웃 건넘
            dv.ev("n=>__C.open(n)", n); click(dv, '#tGpt'); dv.pg.wait_for_timeout(700) if QC.GATE else _rg_wait(dv, 700, _RG_GPSHEET, 'e001.nb')
            s = dv.ev("()=>__C.sheet()"); nb[n] = bool(s and s['mot']); dv.ev("()=>__C.closeSheets()")
        out['nb'] = nb
        out['gpText'] = dv.ev("()=>Object.fromEntries(Object.entries(GP))")
        out['keys'] = dv.ev("()=>SYNC_KEYS.filter(k=>k!=='gpt')")
        out['stores'] = dv.ev("k=>__J.stores(k)", out['keys'])   # 빈 기기 — gpt 말고 나머지 칸(새 판·바탕이 같아야)
        ss = {}
        dv.ev("()=>{try{closeView()}catch(e){}}"); dv.pg.wait_for_timeout(300)
        for q in (('G18-55-02', 'G3-059C', 'G03-40-05') if not QC.SMOKE else ()):   # smoke — 검색 건넘
            try:   # 검색 칸을 눌러 치고 Enter(jagwa_search 하네스 typeq 와 같은 길)
                loc = dv.pg.locator('#q'); loc.click(); loc.fill('')
                dv.pg.keyboard.type(q, delay=5); dv.pg.keyboard.press('Enter'); dv.pg.wait_for_timeout(400)
                ss[q] = dv.ev("()=>typeof ES_NOS!=='undefined'?ES_NOS.map(n=>String(codeShow(DATA[n-1]))):null")
            except Exception as e:
                ss[q] = 'ERR ' + repr(e)[:120]
        try:
            loc = dv.pg.locator('#q'); loc.click(); loc.fill(''); dv.pg.keyboard.press('Enter')
        except Exception:
            pass
        out['search'] = ss
        out['errs'] = dv.errs[:3]
    finally:
        dv.close()
    return out


def main():
    rn, rb, how = recs()
    sn, sb = statics()
    sb_raw = sb   # 옛 번호 이름 그대로(라벨 · 옛 값 표시용) — 아래 sb 는 uid 열쇠판 앱에 먹이려고 이름·목록을 uid 로 옮긴 것(§D-1)
    if UIDK and QC.GATE:   # regress — 바탕 motion 없음(sb = None)
        sb = uidify(sb)
    jn_ = json.loads(rn.decode('utf-8'))   # 이 기록(원격 사본) — 번호 칸 · uid 칸의 글을 도장으로 가리는 기준(§A-2)
    if QC.GATE:
        QC.sub('git:show-app')
        app = JG.git_HU(GENIE, 'show', 'HEAD:jagwa/index.html')
        wt = open(os.path.join(GENIE, 'jagwa', 'index.html'), 'rb').read().replace(b'\r\n', b'\n')
    else:   # regress — 앱 = 작업트리 파일(줄끝 LF · 사슬 = 새 판 워크트리 = HEAD) · git show 0 · 「작업트리 = HEAD」 칸은 관문만
        wt = open(os.path.join(GENIE, 'jagwa', 'index.html'), 'rb').read().replace(b'\r\n', b'\n')
        app = wt
    print('기록 = %s · 앱 = genie HEAD jagwa/index.html(작업트리와 %s)' % (how, '같음' if wt == app else '다름'))
    t0 = time.time()
    with sync_playwright() as pw:
        for eng in (ENGS if not QC.SMOKE else [e for e in ENGS if e == 'chromium'][:1]):   # smoke — chromium 한 판
            br = getattr(pw, eng).launch()
            try:
                N = run_side(br, eng, 'NEW', app, rn, sn)
                B = run_side(br, eng, 'BASE', app, rb, sb) if QC.GATE else None   # regress — 바탕 쪽(헛잣대 재료) 문맥 0 · 「바탕」 칸 = —
                for no, w in NOS.items():
                    n, b = N[no], (B[no] if QC.GATE else {'btn': {}, 'sheet': None})
                    s = n['sheet'] or {}
                    MDn = gpx(jn_, no) if UIDK else md(no)   # ★ uid_unify — 이 기록을 받은 기기의 이 칸 글(번호 칸 · uid 칸이면 도장 늦은 쪽 · 옛 판이면 옛 재료 그대로)
                    if MDn is None:
                        MDn = md(no)
                    ok1 = n['btn']['btn'] == 'Claude ✓' and n['btn']['last'] and s.get('read') and not s.get('edit') and s.get('p', '').startswith(w['code'] + ' · ') \
                        and 'undefined' not in s.get('p', '') and ' ·  ' not in s.get('p', '') and not s.get('p', '').endswith('·')
                    if UIDK:   # ★ uid_unify 옛 잣대 고침 §C-1(제목 = uid Claude · 정답 … · 번호 글자 0) · §C-2(둘째 줄 = 왼쪽 QA 줄) · §0-6(닻) — 옛 조건(머리 둘째 줄 = 「코드 · …」)만 갈았다
                        ok1 = (n['btn']['btn'] == 'Claude ✓' and n['btn']['last'] and s.get('read') and not s.get('edit') and N2U[no] == w['code']
                               and (s.get('h2') or '').rstrip('✕ ') == gpt_title(_ITEMS[int(no) - 1]) and '번' not in (s.get('h2') or '') and bool(s.get('sub')) and s.get('qa') == gp_qa_split(MDn)[0]
                               and 'undefined' not in s.get('p', '') and ' ·  ' not in s.get('p', '') and not s.get('p', '').endswith('·'))
                    okb1 = (b['btn']['btn'] == 'Claude ✓' and bool((b['sheet'] or {}).get('read'))) if QC.GATE else None
                    R(eng, '%s — 「Claude ✓」(아랫줄 맨 오른쪽) · 머리 「%s · …」 · 읽기 판 먼저' % (no, w['code']), ok1, okb1, {'단추': n['btn'], '머리': s.get('p'), '바탕 단추': b['btn']['btn'] if QC.GATE else '—'})
                    if QC.SMOKE:   # smoke — 「Claude ✓」 칸만(읽기 판 · 모션 · 데이터 건넘)
                        continue
                    head = [x.strip() for x in md(no).split('\n\n')[0].replace('**', '').split('\n')]
                    WX = dict(h3=6, li=w['li'], tb=1, th=4, tr=4, b=w['b'])   # 옛 재료의 읽기 판 셈(옛 하네스가 박은 값)
                    if UIDK:   # ★ uid_unify §C-3 — 읽기 판은 QA 첫 줄(과 바로 뒤 빈 줄)을 뺀 나머지 · 개수는 그 글에서 센다(옛 재료면 위 옛 값과 같다 — 오프라인 대조 · 새 재료는 §D-2 표와 같다)
                        rest_x = gp_qa_split(MDn)[1]
                        WX = {k_: v_ for k_, v_ in gp_counts(rest_x).items() if k_ in ('h3', 'li', 'tb', 'th', 'tr', 'b')}
                        head = [x.strip() for x in rest_x.split('\n\n')[0].replace('**', '').split('\n')]
                    p1 = [x.strip() for x in (s.get('p1') or '').split('\n')]
                    # 옛 줄: ok2 = s.get('h3') == 6 and s.get('li') == w['li'] and s.get('tb') == 1 and s.get('th') == 4 and s.get('tr') == 4 and s.get('b') == w['b'] and s.get('script') == 0 and p1 == head
                    ok2 = s.get('h3') == WX['h3'] and s.get('li') == WX['li'] and s.get('tb') == WX['tb'] and s.get('th') == WX['th'] and s.get('tr') == WX['tr'] and s.get('b') == WX['b'] and s.get('script') == 0 and p1 == head
                    R(eng, '%s 읽기 판 — h3.gph 6 · li %d · 표 1(th 4 · tr 4) · <b> %d · script 0 · 원문 첫 %d줄 = 첫 문단(줄마다)' % (no, w['li'], w['b'], len(head)), ok2, None,
                      dict({k: s.get(k) for k in ('h3', 'li', 'tb', 'th', 'tr', 'b', 'script')}, 첫문단=p1 == head, 첫문단줄=len(p1)))
                    f = n.get('frame') or {}
                    fa = f.get('after') or {}
                    a0, a1 = f.get('ansT') or [], fa.get('ansT') or []
                    # 옛 줄: ok3 = s.get('mot') and f.get('src') == 'motion/earth_%s.html' % no and f.get('status') == 200 and f.get('same') and f.get('card') == 1 \
                    # 옛 줄: and f.get('hideBtn') and bool(a0) and all(x == '1' for x in a0) and len(a1) == len(a0) and all(x == '0' for x in a1) \
                    # 옛 줄: and fa.get('pressed') == 'true' and fa.get('blank') and f.get('big') == '_blank'
                    ok3 = s.get('mot') and f.get('src') == 'motion/earth_%s.html' % mk(no) and f.get('status') == 200 and f.get('same') and f.get('card') == 1 \
                        and f.get('hideBtn') and bool(a0) and all(x == '1' for x in a0) and len(a1) == len(a0) and all(x == '0' for x in a1) \
                        and fa.get('pressed') == 'true' and fa.get('blank') and f.get('big') == '_blank'   # ★ uid_unify §D-1 — src = motion/earth_<uid>.html
                    R(eng, '%s 모션 — ▶ 모션 · iframe motion/earth_%s.html 200 · 같은 출처 · svg.card 1 · 「가리기」 진짜 누름 → .ans 글자 opacity 0 · 크게 보기 _blank' % (no, no), ok3,
                      bool((b['sheet'] or {}).get('mot')) if QC.GATE else None, {'src': f.get('src'), 'status': f.get('status'), 'same': f.get('same'), 'card': f.get('card'),
                                                            '.ans 글자': '%d개 %s → %s' % (len(a0), sorted(set(a0)), sorted(set(a1))), 'pressed': fa.get('pressed'),
                                                            'blank': fa.get('blank'), 'big': f.get('big'), 'err': fa.get('err')})
                    bh_ = f.get('bigHref')   # ★ uid_unify §D-1(새 칸 · 결함 후보) — 파일 이름만 바꾸고 안 글자는 그대로(바이트 무변)라 「크게 보기 ↗」 href 가 옛 이름을 가리킨다 → 새 탭에서 404 인지 잰다
                    tgt_ = posixpath.normpath(posixpath.join(posixpath.dirname(f.get('src') or ''), bh_)) if bh_ else None
                    R(eng, '%s 모션 — 「크게 보기」 링크가 가리키는 motion 파일이 있다(파일 이름을 바꿔도 404 가 아니다)' % no, bool(tgt_) and tgt_ in sn, None,
                      {'href': bh_, '가리키는 파일': tgt_, '있나': bool(tgt_) and tgt_ in sn, 'iframe src': f.get('src')})
                    old = OLDNUM.findall(s.get('text', '') + ' ' + f.get('text', ''))
                    R(eng, '%s add2 — 읽기 판·모션 글자에 옛 꼴 번호 0' % no, not old and bool(s.get('text')) and bool(f.get('text')), None, old[:5])
                    # 옛 줄: R(eng, '%s 데이터 — GP[%s] = 재료 글자 전수(%d자)' % (no, no, len(md(no))), N['gpText'].get(no) == md(no), B['gpText'].get(no) == md(no),
                    # 옛 줄: {'길이': len(N['gpText'].get(no) or '')})
                    R(eng, '%s 데이터 — GP[%s] = 재료 글자 전수(%d자)' % (no, no, len(md(no))), N['gpText'].get(gkey(no)) == MDn, (B['gpText'].get(gkey(no)) == MDn) if QC.GATE else None,
                      {'길이': len(N['gpText'].get(gkey(no)) or '')})   # ★ uid_unify §A-1 — GP 열쇠 = uid
                if not QC.SMOKE:   # smoke — 검색 · 이웃 · 목록 건넘
                    R(eng, 'add2 — 새 꼴 번호 셋(G18-55-02 · G3-059C · G03-40-05) 검색 = 그 문항 하나', all(v == [k] for k, v in N['search'].items()), None, N['search'])
                    R(eng, '이웃 148·150·83·85 — 모션 단추 0', not any(N['nb'].values()), None, N['nb'])
                    # ★ 2026-10-01 claude_e004 — 지학 111 을 더해 gpt 칸이 셋이 된다. 「84·149 두 줄」 은 값을 박은 잣대라 뒤 판마다 거짓 FAIL
                    #   → 「.tag.gp 줄 = 그 기록의 gpt 칸 번호 전부 · 84·149 가 든다」 로 갈음(바탕 = 두 칸 뺀 기록 → 84·149 없음 → FAIL 그대로)
                    # 옛 줄: wl = sorted(int(k) for k in (json.loads(rn.decode('utf-8'))['data'].get('gpt') or {}))
                    wl = sorted({int(k_) if k_.isdigit() else int(U2N[k_]) for k_ in (json.loads(rn.decode('utf-8'))['data'].get('gpt') or {}) if k_.isdigit() or k_ in U2N})   # ★ uid_unify — 번호 칸 · uid 칸(D-2) 둘 다 그 문항의 화면 번호로
                    R(eng, '목록 — .tag.gp 줄 = 기록 gpt 칸 번호 전부(84·149 가 든다)', sorted(N['list']) == wl and {84, 149} <= set(wl),
                      (sorted(B['list']) == wl and {84, 149} <= set(B['list'])) if QC.GATE else None, {'NEW': N['list'], 'BASE': B['list'] if QC.GATE else '—', '기록 gpt': wl})
                R(eng, '페이지 오류 0', not N['errs'], None, N['errs'])
                if QC.GATE:   # 바탕 쪽(BASE 문맥) 나머지 칸과 맞댐
                    dk = [k for k in N['keys'] if N['stores'].get(k) != B['stores'].get(k)]
                    R(eng, '빈 기기 — 동기화 뒤 gpt 말고 나머지 칸 %d 가 바탕과 같다(status·bogi·gg·unit·bpg …)' % len(N['keys']), not dk and N['keys'] == B['keys'], None,
                      {'다른 칸': dk, '칸 수': len(N['keys'])})
                else:
                    if not QC.SMOKE:   # regress — 바탕 쪽 값 = 기준 스냅샷(앞 인도판 새 판의 같은 칸 · md5) · smoke 건넘
                        _cur = {'keys': N['keys'], 'stores': {k: _rg_md5(N['stores'].get(k)) for k in N['keys']}}
                        _bv = QC.base('빈 기기@%s' % eng, _cur)
                        dk = [k for k in N['keys'] if _cur['stores'].get(k) != (_bv.get('stores') or {}).get(k)]
                        R(eng, '빈 기기 — 동기화 뒤 gpt 말고 나머지 칸 %d 가 바탕과 같다(status·bogi·gg·unit·bpg …)' % len(N['keys']), not dk and N['keys'] == _bv.get('keys'), None,
                          {'다른 칸': dk, '칸 수': len(N['keys']), '기준': QC.base_note('빈 기기@%s' % eng)})
                # 물리 72 무변
                ph = {}
                for who, st in ((('NEW', sn), ('BASE', sb)) if QC.GATE else ((('NEW', sn),) if not QC.SMOKE else ())):   # regress — NEW 만(바탕 = 기준 스냅샷) · smoke 건넘
                    dv = dv_open(br, eng, app, 'phys', None, st)
                    try:
                        dv.ev("n=>__C.open(n)", 72); click(dv, '#tGpt'); dv.pg.wait_for_timeout(900) if QC.GATE else _rg_wait(dv, 900, _RG_GPSHEET, 'e001.phys.gpsheet')
                        s = dv.ev("()=>__C.sheet()")
                        if s and s['mot']:
                            click(dv, '#gpMot'); dv.pg.wait_for_timeout(1500) if QC.GATE else _rg_wait(dv, 1500, _RG_MOTFRAME, 'e001.phys.motframe')
                        f = dv.ev("()=>__C.frame()") or {}
                        ph[who] = {'gp72': dv.ev("()=>GP[72]||''"), 'mot': bool(s and s['mot']), 'src': f.get('src'), 'card': f.get('card'), 'h3': (s or {}).get('h3')}
                    finally:
                        dv.close()
                if QC.GATE:   # 바탕 쪽(2998b9e motion)과 맞댐
                    R(eng, '물리 72 — GP·모션 단추·iframe = 바탕', ph['NEW'] == ph['BASE'] and ph['NEW']['mot'], None, {'NEW': {k: v for k, v in ph['NEW'].items() if k != 'gp72'}, 'GP 같음': ph['NEW']['gp72'] == ph['BASE']['gp72']})
                else:
                    if not QC.SMOKE:   # regress — 바탕 = 기준 스냅샷(앞 인도판 새 판의 같은 칸 · GP 는 md5) · smoke 건넘
                        _p72 = dict(ph['NEW'], gp72=_rg_md5(ph['NEW']['gp72']))
                        R(eng, '물리 72 — GP·모션 단추·iframe = 바탕', QC.same('물리 72@%s' % eng, _p72) and ph['NEW']['mot'], None,
                          {'NEW': {k: v for k, v in ph['NEW'].items() if k != 'gp72'}, 'GP 같음': QC.base('물리 72@%s' % eng, _p72).get('gp72') == _p72['gp72'], '기준': QC.base_note('물리 72@%s' % eng)})
                # 기록 있는 기기 — 적재 전 기록으로 먼저 열고 5번에 △ 를 진짜로 눌러(내 칸이 더 새것) 둔 뒤 적재 뒤 원격을 받는다
                dv = dv_open(br, eng, app, 'earth', rb, sn)
                try:
                    keys = dv.ev("()=>SYNC_KEYS.filter(k=>k!=='gpt')")   # 동기화 칸 전부(gpt 는 따로 잰다)
                    # 옛 줄: dv.ev("n=>__C.open(n)", 5); h0 = dv.ev("()=>((ST[5]||{}).h||[]).length")
                    dv.ev("n=>__C.open(n)", 5); h0 = dv.ev("k=>((ST[k]||{}).h||[]).length", gkey('5'))   # ★ uid_unify §A-1 — ST 열쇠 = uid
                    # 옛 줄: click(dv, '#card [data-vmark="Q"]'); dv.pg.wait_for_timeout(500); h1 = dv.ev("()=>((ST[5]||{}).h||[]).length")   # 지학 카드 층 = 카드 안 △(아랫줄 #mQ 는 숨음)
                    click(dv, '#card [data-vmark="Q"]'); dv.pg.wait_for_timeout(500); h1 = dv.ev("k=>((ST[k]||{}).h||[]).length", gkey('5'))   # 지학 카드 층 = 카드 안 △(아랫줄 #mQ 는 숨음)
                    dv.ev("()=>{try{closeView()}catch(e){}}"); dv.ev("()=>__J.sync()")
                    before = dv.ev("k=>__J.stores(k)", keys)
                    dv.load(app, SPD, 'earth', rec={'earth/기록.json': rn}, static=sn); dv.ev(CJS)
                    dv.ev("()=>__J.sync()"); dv.pg.wait_for_timeout(800)
                    after = dv.ev("k=>__J.stores(k)", keys)
                    gp = dv.ev("()=>Object.fromEntries(Object.entries(GP))")
                    body = json.loads(dv.ev("p=>__J.lastPut(p)", 'earth/기록.json') or '{}')
                    bd = body.get('data', {})
                    same = {k: before.get(k) == after.get(k) for k in keys}
                    # 옛 줄: ok = h1 == h0 + 1 and all(gp.get(n) == md(n) for n in NOS) and all(same.values()) \
                    # 옛 줄: and len(((after.get('status') or {}).get('5') or {}).get('h') or []) == h1 \
                    # 옛 줄: and all((bd.get('gpt') or {}).get(n) == md(n) for n in NOS) and len(((bd.get('status') or {}).get('5') or {}).get('h') or []) == h1
                    ok = h1 == h0 + 1 and all(gp.get(gkey(n)) == (gpx(jn_, n) if UIDK else md(n)) for n in NOS) and all(same.values()) \
                        and len(((after.get('status') or {}).get(gkey('5')) or {}).get('h') or []) == h1 \
                        and all((bd.get('gpt') or {}).get(gkey(n)) == (gpx(jn_, n) if UIDK else md(n)) for n in NOS) and len(((bd.get('status') or {}).get(gkey('5')) or {}).get('h') or []) == h1
                    R(eng, '기록 있는 기기 — 동기화 뒤 GP[149]·GP[84] = 재료 · 다른 칸 무변 · 내 새 칸(5번 △ 진짜 누름) 안 덮임 · 올린 몸통에 셋 다', ok, None,
                      # 옛 줄: {'다른 칸': [k for k in keys if not same[k]], '칸 수': len(keys), 'GP': {n: len(gp.get(n) or '') for n in NOS}, '5번 회독': [h0, h1]})
                      {'다른 칸': [k for k in keys if not same[k]], '칸 수': len(keys), 'GP': {n: len(gp.get(gkey(n)) or '') for n in NOS}, '5번 회독': [h0, h1]})
                finally:
                    dv.close()
                # 내 것이 더 새것 — 적재 전 기록 기기에서 149 Claude 창에 써서 저장(진짜 누름 · 원격 도장보다 뒤) → 적재 뒤 원격을 받아도 안 덮인다
                dv = dv_open(br, eng, app, 'earth', rb, sn) if not QC.SMOKE else None   # smoke — 「내 것이 더 새것」 건넘
                try:
                  if not QC.SMOKE:
                    MY = '내가 먼저 쓴 149번(검산)'
                    dv.ev("n=>__C.open(n)", 149); click(dv, '#tGpt'); dv.pg.wait_for_timeout(700) if QC.GATE else _rg_wait(dv, 700, _RG_GPSHEET, 'e001.my.gpsheet')
                    dv.pg.locator('#gpIn').fill(MY); click(dv, '#gpSave'); dv.pg.wait_for_timeout(700)
                    dv.ev("()=>__C.closeSheets()"); dv.ev("()=>{try{closeView()}catch(e){}}"); dv.ev("()=>__J.sync()")
                    dv.load(app, SPD, 'earth', rec={'earth/기록.json': rn}, static=sn); dv.ev(CJS)
                    dv.ev("()=>__J.sync()"); dv.pg.wait_for_timeout(800)
                    # 옛 줄: g = dv.ev("()=>({a:GP[149]||'',b:GP[84]||''})")
                    g = dv.ev("([a,b])=>({a:GP[a]||'',b:GP[b]||''})", [gkey('149'), gkey('84')])   # ★ uid_unify §A-1 — GP 열쇠 = uid
                    body = json.loads(dv.ev("p=>__J.lastPut(p)", 'earth/기록.json') or '{}')
                    bg = body.get('data', {}).get('gpt') or {}
                    # 옛 줄: ok = g['a'] == MY and g['b'] == md('84') and bg.get('149') == MY and bg.get('84') == md('84')
                    ok = g['a'] == MY and g['b'] == (gpx(jn_, '84') if UIDK else md('84')) and bg.get(gkey('149')) == MY and bg.get(gkey('84')) == (gpx(jn_, '84') if UIDK else md('84'))
                    R(eng, '내 것이 더 새것 — 원격 도장 뒤에 고친 GP[149] 는 원격이 못 덮는다(본판 §B-6 = claude_slot CL-6 ⓒ 잣대) · GP[84] 는 받는다 · 올린 몸통도 그대로', ok, None,
                      # 옛 줄: {'149': g['a'][:24], '84 길이': len(g['b']), '올린 149': (bg.get('149') or '')[:24], '올린 84 길이': len(bg.get('84') or '')})
                      {'149': g['a'][:24], '84 길이': len(g['b']), '올린 149': (bg.get(gkey('149')) or '')[:24], '올린 84 길이': len(bg.get(gkey('84')) or '')})
                finally:
                  if not QC.SMOKE:
                    dv.close()
            finally:
                br.close()
    # 앱 무변 · 생물 gpt 무변
    if QC.GATE:   # 그 판(모션 · 기록 적재)이 앱을 안 건드렸나 — 그 판에만 뜻 · regress 끔
        R('-', 'jagwa/index.html 바이트 무변(작업트리 = HEAD)', wt == app, None, hashlib.md5(wt).hexdigest()[:8])
    if how.startswith('적재 뒤') and QC.GATE:   # 적재 커밋 diff — 관문만
        fs = JG.git_HU(SPD, 'diff', '--name-only', SEED_REV + '~1', SEED_REV).decode('utf-8').split()
        R('-', '적재 커밋 %s 이 건드린 파일 = earth/기록.json 하나(물리·생물 기록 무변)' % SEED_REV, fs == ['earth/기록.json'], None, fs)
    # ★ 2026-10-01 claude_p002·claude_e004 — 뒤 판이 phys 에 97 · earth 에 111 을 끝에 더한다. 「= {"phys":[72],"earth":[149,84]}」 는 값을 박은 잣대라
    #   → 「earth 가 [149, 84] 로 시작(차례 그대로) · phys 맨 앞 72」 로 갈음(바탕 2998b9e = earth 없음 → FAIL 그대로)
    if not QC.SMOKE:   # smoke — 모션 데이터 칸 건넘
        jx, jy = json.loads(sn['motion/index.json']), (json.loads(sb['motion/index.json']) if QC.GATE else {})   # regress — 바탕 index.json 없음(바탕 판정 —)
        # 옛 줄: R('-', 'motion/index.json — earth 가 [149, 84] 로 시작(차례 그대로) · phys 맨 앞 72', (jx.get('earth') or [])[:2] == [149, 84] and (jx.get('phys') or [])[:1] == [72],
        # 옛 줄: (jy.get('earth') or [])[:2] == [149, 84] and (jy.get('phys') or [])[:1] == [72], sn['motion/index.json'].decode())
        E2 = [N2U['149'], N2U['84']] if UIDK else [149, 84]   # ★ uid_unify §D-1 — earth = uid 문자열(바탕 번호 목록은 uid 로 옮겨 맞댐)
        R('-', 'motion/index.json — earth 가 [149, 84] 로 시작(차례 그대로) · phys 맨 앞 72', (jx.get('earth') or [])[:2] == E2 and (jx.get('phys') or [])[:1] == [72],
          ((jy.get('earth') or [])[:2] == E2 and (jy.get('phys') or [])[:1] == [72]) if QC.GATE else None, sn['motion/index.json'].decode())
        for no in NOS:
            # 옛 줄: f = 'motion/earth_%s.html' % no
            fl = 'motion/earth_%s.html' % no   # 라벨용(옛 이름 · 판이 달라도 같은 줄 이름)
            f = 'motion/earth_%s.html' % mk(no)   # ★ uid_unify §D-1 — 카드 층 모션 파일 = earth_<uid>.html(바이트 무변 · 재료 = 옛 이름 파일)
            src = open(os.path.join(MAT, 'earth_%s.html' % no), 'rb').read()
            # ★ A-6(d) 9/30 _task_qa_baseline — 줄끝만 뺀 바이트로 맞댄다: 새로 만든 작업트리(qa 워크트리 · core.autocrlf)는 CRLF 로 풀려(18,745 = 18,515 + 230) · git blob = 재료(LF) 그대로
            # 옛 줄: R('-', '%s = 재료 바이트(md5 %s)' % (f, hashlib.md5(src).hexdigest()[:8]), (sn.get(f) or b'').replace(b'\r\n', b'\n') == src.replace(b'\r\n', b'\n'), None, len(sn.get(f) or b''))
            R('-', '%s = 재료 바이트(md5 %s)' % (fl, hashlib.md5(src).hexdigest()[:8]), (sn.get(f) or b'').replace(b'\r\n', b'\n') == src.replace(b'\r\n', b'\n'), None, len(sn.get(f) or b''))
            tx = (sn.get(f) or b'').decode('utf-8', 'replace')
            ext = re.findall(r'(?:src|href)\s*=\s*["\'](https?://[^"\']+)', tx)
            # 옛 줄: R('-', '%s — 바깥 스크립트 0 · 바깥 주소 = Google Fonts 뿐 · .pdf 0(공개 genie)' % f,
            R('-', '%s — 바깥 스크립트 0 · 바깥 주소 = Google Fonts 뿐 · .pdf 0(공개 genie)' % fl,
              not re.search(r'<script[^>]*\bsrc\s*=', tx) and all(u.startswith('https://fonts.googleapis.com/') for u in ext) and '.pdf' not in tx.lower(), None, ext)
        R('-', 'motion 폴더에 .pdf 0', not [k for k in sn if k.lower().endswith('.pdf')], None, sorted(sn))
    npass = sum(1 for r in ROWS if r[2]); nfail = sum(1 for r in ROWS if not r[2])
    print('\n== PASS %d · FAIL %d · %.0f초 · 기록 %s' % (npass, nfail, time.time() - t0, how))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · claude_e001(+add1+add2) CE1 · 기록 %s · genie HEAD %s · 바탕 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), how,
                JG.git_HU(GENIE, 'rev-parse', '--short', 'HEAD').decode().strip(), BASE_REV, ','.join(ENGS)))
        for eng, n, okn, okb, v in ROWS:
            f.write('%s | 바탕 %s | %s · %s | %s\n' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], eng, n,
                    (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str))[:1200]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
