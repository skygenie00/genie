# -*- coding: utf-8 -*-
r"""_task_jagwa_claude_e004 관문 「CE4」 — 지학 G06-43-02(no 111) Claude 풀이 · 북극성·평행 광선 모션(canvas 셋)
(2026-10-01 · 같은 길 = _task_jagwa_claude_e001(+add1·add2) CE1 · 물리 짝 = _harness_jagwa_claude_p002.py(CP2) 꼴)

  python _harness_jagwa_claude_e004.py [--eng chromium] [--res <결과>] [--base <genie 커밋>] [--seed <studyplandata 커밋>] [--no 111|119]

  --no = 번호(기본 111 — 옛 줄 글자 · 잣대 그대로) · 10/4 _task_jagwa_claude_e008 §B 「CE4 하네스를 번호 인자로」:
         119 = 지학 G06-43-10 일주 운동 그림(svg 한 장 · 움직임 없음) — 모션 잣대가 canvas 셋 · 「▶ 공전」 · 프리셋 대신 svg#fig 1 · 지평선 ellipse 6 ·
         다른 모션 번호(149 · 84 · 111) 단추 · GP 무변 · 결과 파일 = _harness_jagwa_claude_e004_119_result.txt

  NEW  = genie 작업트리 jagwa/motion/*(earth_111.html · index.json 의 earth 끝에 111)
         + 지학 기록 = studyplandata 작업트리 earth/기록.json — gpt["111"] = 재료면 「적재 뒤 실물」 · 아니면 HEAD 기록에 두 칸을 더한 사본(「합성」)
  BASE(헛잣대) = genie 바탕 커밋의 motion/*(111 없음 · claude_p002 뒤 판) + 기록에서 gpt 111 칸과 그 도장만 뺀 것
         바탕 커밋 = --base · 안 주면 「earth_111.html 을 처음 더한 커밋」의 바로 앞(커밋 전이면 HEAD) — 커밋·병합 뒤 다시 돌려도 헛잣대가 거저 PASS 가 안 된다
  이 판 커밋 — genie = earth_111.html 을 처음 더한 커밋 · studyplandata = 「gpt|111」 을 처음 넣은 커밋(--seed 로 박을 수 있다)을 git 이력에서 찾아
         그 커밋 단위로 잰다(아직 커밋 전이면 HEAD → 작업트리).
  앱 = genie HEAD jagwa/index.html(작업트리와 바이트 같음 · 이 판 커밋이 앱을 안 건드림) · 기록은 route 사본 · PUT 은 가로채 밖으로 안 나감(HU INIT)
  규칙 (57) — 앱 코드 무변 → WebKit 안 돎(기본 chromium) · 회귀 = 모션·Claude 칸 하네스만
  ⚠ 자과앱 픽셀 IDENTICAL 게이트 없음(CLAUDE.md). 「▶ 공전 (1년) 뒤 1초 안에 캔버스 ① 픽셀이 바뀜」은 같은 판 안의 「바뀌었나」다
    — 모션 쪽 canvas 의 getImageData 해시를 누르기 앞(0.5초 정지 대조)·뒤로 잰다(앱 화면 픽셀 대조가 아니다).
  ⚠ 값을 박지 않는다 — 목록 태그는 「그 기록의 gpt 칸 번호」, 모션 번호는 「바탕 + 111 로 시작」과 맞댄다. 이 판이 남긴 index.json 은 커밋 blob 으로 꼭 맞댄다.
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
ENGS = [x for x in (ARG('--eng', 'chromium') or '').split(',') if x]
NO = ARG('--no', '111')   # 10/4 _task_jagwa_claude_e008 「CE4 하네스를 번호 인자로」 — 기본 111(옛 줄 글자 그대로)
SPEC = {   # 번호마다 다른 것 — 문제 번호 · 창 머리 · 읽기 판 셈 · 이웃(단추 0) · 다른 모션 번호(단추 · GP 그대로) · 모션 꼴
    '111': dict(code='G06-43-02', head='G06-43-02 · 43회 2번', want={'h3': 6, 'h3t': '①②③④⑤⑥', 'li': 17, 'ol': 0, 'tb': 1, 'th': 3, 'tr': 4, 'b': 7},
                neigh=(110, 112), others=(149, 84), kind='canvas'),
    '119': dict(code='G06-43-10', head='G06-43-10 · 43회 10번', want={'h3': 6, 'h3t': '①②③④⑤⑥', 'li': 12, 'ol': 0, 'tb': 1, 'th': 3, 'tr': 4, 'b': 6},
                neigh=(118, 120), others=(149, 84, 111), kind='svg', ell=6),   # e008 §0-4 재료 셈 · §B-2 · §B-3
}[NO]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_claude_e004_result.txt' if NO == '111' else '_harness_jagwa_claude_e004_%s_result.txt' % NO))
MAT = _roots.n('jagwa', 'gigu', 'claude_motion')   # N: 에만 있는 재료 — _qa 사본으로 돌려도 N: 에서 읽는다(env_lanes_fix A-2)
SUBJ, RP = 'earth', 'earth/기록.json'
CODE, HEADP = SPEC['code'], SPEC['head']
MOTF = 'jagwa/motion/earth_%s.html' % NO
WANT = SPEC['want']
NEIGH = SPEC['neigh']
OTHERS = SPEC['others']
NSURI = ('http://www.w3.org/2000/svg', 'http://www.w3.org/1999/xlink')   # svg 이름공간 글자(불러오기 아님) — 119 그림 재료에 있다
PRIME = '″'   # 「″」(재료·지시서 둘 다 U+2033)
OLDNUM = re.compile(r'G\d\d-\d\d-\d(?!\d)|(?<![A-Za-z0-9])C\d-\d{3}')   # 옛 꼴 번호(CE1 add2 와 같은 꼴)
ROWS = []
from playwright.sync_api import sync_playwright   # noqa: E402


def R(eng, name, okn, okb, val):
    ROWS.append((eng, name, okn, okb, val))
    print('%s | 바탕 %s | %s · %s | %s' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[okn], {True: 'PASS', False: 'FAIL', None: '—'}[okb], eng, name,
          (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str))[:420]), flush=True)


def mat(f):
    return io.open(os.path.join(MAT, f), encoding='utf-8', newline='').read().replace('\r\n', '\n')


MD = mat('earth_%s.md' % NO)

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

UID = N2U[NO]
MOTK = UID if UIDK else NO                                      # 모션 열쇠(§D-1)
MOTF_NOW = 'jagwa/motion/earth_%s.html' % MOTK                   # 지금 모션 파일 · 옛 이름 MOTF 는 이 판 커밋 이력 조회용으로 둔다
MD_NEW = mat_uid(UID) if UIDK else None                          # D-2 새 재료(없으면 None)
TITLE = gpt_title(_ITEMS[int(NO) - 1])                           # 새 꼴 창 제목 기대(§C-1 표와 같은 규칙 · 문항.json 에서)


def _nob(v):
    """status 칸 값에서 회독 항목의 b 만 뺀 사본 — 문항을 처음 열 때 지난 회독의 〈보기〉 O△X(bogi 칸)가 그 문항 마지막 회독 항목의 b 로 옮겨 붙는다(§G-3-2 · 지학 bogi 24 칸 가운데 84 · 111 · 149 가 든다 · 값은 안 지움)"""
    v = json.loads(json.dumps(v)) if v is not None else None
    if isinstance(v, dict):
        for h_ in (v.get('h') or []):
            if isinstance(h_, dict):
                h_.pop('b', None)
    return v


def big_ok(big):
    """「크게 보기」 링크 = [href, target] — target 은 _blank · href 는 이 모션 파일 이름(옛 번호 이름 · uid 이름 어느 쪽이든 — 파일 이름만 바꾸고 안 글자는 그대로 둔 판은 옛 이름) · 그 링크가 가리키는 파일이 있나는 별도 칸이 잰다(§D-1)"""
    return bool(big) and big[1] == '_blank' and big[0] in ('earth_%s.html' % NO, 'earth_%s.html' % MOTK)


def dumps(d):
    return json.dumps(d, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


def git1(repo, *a):
    return HU.git(repo, *a).decode('utf-8', 'replace').strip()


def seed_rev():
    s = ARG('--seed', '')
    if s:
        return s
    L = git1(SPD, 'log', '--reverse', '--format=%h', '-S', '"gpt|%s"' % NO, '--', RP).split()
    return L[0] if L else ''


def lane_rev():
    L = git1(GENIE, 'log', '--reverse', '--diff-filter=A', '--format=%h', '--', MOTF).split()
    return L[0] if L else ''


LANE = lane_rev()
BASE_REV = ARG('--base', '') or (git1(GENIE, 'rev-parse', '--short', LANE + '~1') if LANE else git1(GENIE, 'rev-parse', '--short', 'HEAD'))


def recs():
    head = HU.git(SPD, 'show', 'HEAD:' + RP)
    wt = open(os.path.join(SPD, 'earth', '기록.json'), 'rb').read()
    dw = json.loads(wt.decode('utf-8'))
    if UIDK:   # ★ uid_unify §A-2 · §D-2 — 번호 칸(옛 글) 또는 uid 칸(새 글)이 재료면 「적재 뒤 실물」 · 바탕은 두 칸(+도장·묘비)을 다 뺀다
        g_ = dw['data'].get('gpt') or {}
        if g_.get(NO) == MD or (MD_NEW is not None and g_.get(UID) == MD_NEW):
            b = json.loads(wt.decode('utf-8'))
            for kk in (NO, UID):
                b['data'].setdefault('gpt', {}).pop(kk, None); b['u'].pop('gpt|' + kk, None); b.get('gone', {}).pop('gpt|' + kk, None)
            return wt, dumps(b), '적재 뒤 실물'
        d = json.loads(head.decode('utf-8'))
        d['data'].setdefault('gpt', {})[UID] = MD_NEW if MD_NEW is not None else MD; d['u']['gpt|' + UID] = int(time.time() * 1000)
        return dumps(d), head, '합성(적재 전)'
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


CJS = r"""
window.__C={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 async open(no){try{closeView()}catch(e){}await new Promise(r=>setTimeout(r,150));await openView(no);await new Promise(r=>setTimeout(r,1200));
   const b=document.getElementById('tGpt');const row=b&&b.parentElement;const vis=[...(row?row.children:[])].filter(x=>x.offsetParent!==null&&getComputedStyle(x).display!=='none');
   return {btn:__C.tx(b),last:vis.length?vis[vis.length-1]===b:false,vis:!!b&&b.offsetParent!==null&&b.getBoundingClientRect().width>0}},
 sheet(){const s=[...document.querySelectorAll('.sheet')].pop();if(!s)return null;const rd=s.querySelector('.gpread');
   return {h2:__C.tx(s.querySelector('.panel > h2')),p:__C.tx(s.querySelector('.panel > p')),read:!!rd,edit:!!s.querySelector('#gpIn'),
     h3:rd?rd.querySelectorAll('h3.gph').length:0,h3t:rd?[...rd.querySelectorAll('h3.gph')].map(x=>__C.tx(x).charAt(0)).join(''):'',
     li:rd?rd.querySelectorAll('ul.gpul li').length:0,ol:rd?rd.querySelectorAll('ol.gpol li').length:0,
     tb:rd?rd.querySelectorAll('table.gptb').length:0,th:rd?rd.querySelectorAll('table.gptb th').length:0,tr:rd?rd.querySelectorAll('table.gptb tbody tr').length:0,
     b:rd?rd.querySelectorAll('b').length:0,script:rd?rd.querySelectorAll('script').length:0,
     p1:rd?((rd.querySelector('p.gpp')||{}).innerText||''):'',text:rd?rd.textContent:'',
     /* 옛: mot:(()=>{const m=s.querySelector('#gpMotBar');return !!m&&m.style.display!=='none'})(),motTx:__C.tx(s.querySelector('#gpMot'))}}, — ★ uid_unify §C-2 카드 층 창은 #gpMotBar 줄이 없고 둘째 줄(#gpSub) 오른쪽에 「▶ 모션」(#gpMot) */
     sub:!!s.querySelector('.panel > #gpSub'),qa:__C.tx(s.querySelector('#gpQa')),
     mot:(()=>{const m=s.querySelector('#gpMotBar');return (!!m&&m.style.display!=='none')||!!s.querySelector('#gpSub #gpMot')})(),motTx:__C.tx(s.querySelector('#gpMot'))}},
 closeSheets(){document.querySelectorAll('.sheet').forEach(x=>x.remove())},
 async frame(){const f=document.getElementById('gpMotFrame');if(!f)return null;
   for(let i=0;i<60;i++){try{const d=f.contentDocument;if(d&&d.readyState==='complete'&&d.body&&d.body.children.length)break}catch(e){}await new Promise(r=>setTimeout(r,150))}
   await new Promise(r=>setTimeout(r,400));
   let d=null;try{d=f.contentDocument}catch(e){return {src:f.getAttribute('src'),same:false}}
   if(!d)return {src:f.getAttribute('src'),same:false};
   const st=await fetch(f.getAttribute('src'),{cache:'no-store'}).then(r=>r.status).catch(()=>0);
   const big=[...d.querySelectorAll('a')].find(x=>/크게 보기/.test(x.textContent));
   const r=f.getBoundingClientRect();
   return {src:f.getAttribute('src'),status:st,same:new URL(f.src,location.href).origin===location.origin,h:Math.round(r.height),
     canvas:d.querySelectorAll('canvas').length,cw:[...d.querySelectorAll('canvas')].map(c=>c.width),card:d.querySelectorAll('svg.card').length,svg:d.querySelectorAll('svg#fig').length,ell:d.querySelectorAll('svg#fig ellipse').length,
     big:big?[big.getAttribute('href'),big.getAttribute('target')]:null,p1:__C.tx(d.getElementById('p1')),m11:__C.tx(d.getElementById('m11')),
     text:d.body?d.body.textContent:''}},
 fdoc(){return document.getElementById('gpMotFrame').contentDocument},
 pix(id){const c=__C.fdoc().getElementById(id);if(!c)return null;const w=c.width,h=c.height;if(!w||!h)return 'empty';
   const a=c.getContext('2d').getImageData(0,0,w,h).data;let x=2166136261>>>0;
   for(let i=0;i<a.length;i+=4){x^=(a[i]|(a[i+1]<<8)|(a[i+2]<<16));x=Math.imul(x,16777619)>>>0}return w+'x'+h+':'+x.toString(16)},
 async waitPix(id,h0,ms){const t0=performance.now();while(performance.now()-t0<ms){const h=__C.pix(id);if(h!==h0)return {ms:Math.round(performance.now()-t0),h};
   await new Promise(r=>setTimeout(r,25))}return {ms:-1,h:__C.pix(id)}},
 m11(){return __C.tx(__C.fdoc().getElementById('m11'))},
 /* 옛: gpNos(){return Object.keys(GP).map(Number).sort((a,b)=>a-b)}, — ★ uid_unify §A-1 열쇠가 uid 글자면 글자로 정렬 */
 gpNos(){const k=Object.keys(GP);return k.every(x=>/^\d+$/.test(x))?k.map(Number).sort((a,b)=>a-b):k.sort()},
 async mot(){try{await motLoad()}catch(e){}return (typeof MOT==='undefined')?'없음':MOT},
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
        out['list'] = dv.ev("()=>__C.listTags()")
        out['gp'] = dv.ev("()=>__C.gpNos()")
        o = {'btn': dv.ev("n=>__C.open(n)", int(NO))}
        o['clicked'] = click(dv, '#tGpt'); dv.pg.wait_for_timeout(900)
        o['sheet'] = dv.ev("()=>__C.sheet()")
        if o['sheet'] and o['sheet']['mot']:
            click(dv, '#gpMot'); dv.pg.wait_for_timeout(1800)
            o['frame'] = dv.ev("()=>__C.frame()")
            fr = o['frame'] or {}
            if fr.get('same') and fr.get('canvas') and SPEC['kind'] == 'canvas':   # 「▶ 공전」 · 프리셋은 111 canvas 그림만(119 = svg 한 장 · 움직임 없음)
                try:
                    fl = dv.pg.frame_locator('#gpMotFrame')
                    h0 = dv.ev("()=>__C.pix('c1')"); dv.pg.wait_for_timeout(500); h0b = dv.ev("()=>__C.pix('c1')")   # 정지 대조 — 누르기 앞 0.5초 동안 안 바뀐다
                    fl.locator('#p1').click(timeout=15000)   # 「▶ 공전 (1년)」 진짜 누름
                    ch = dv.ev("a=>__C.waitPix('c1',a,1000)", h0)
                    fr['pix'] = {'앞': h0, '0.5초 뒤(누르기 앞)': h0b, '뒤': ch.get('h'), '바뀐 ms': ch.get('ms'), 'p1 글자': dv.ev("()=>__C.tx(__C.fdoc().getElementById('p1'))")}
                    m0 = dv.ev("()=>__C.m11()")
                    fl.locator('#d1p button[data-v="1000"]').click(timeout=15000)   # 프리셋 「실제 (약 430광년)」 진짜 누름
                    dv.pg.wait_for_timeout(500)
                    fr['m11'] = {'앞': m0, '뒤': dv.ev("()=>__C.m11()"), '단추': dv.ev("()=>__C.tx(__C.fdoc().querySelector('#d1p button[data-v=\"1000\"]'))")}
                except Exception as e:
                    fr['err'] = repr(e)[:200]
        dv.ev("()=>__C.closeSheets()")
        out[NO] = o
        mb = {}
        for n in NEIGH + OTHERS:   # 이웃 번호 — 모션 단추 0 · 다른 모션 번호(149·84 · 119 판은 111 도)는 단추 그대로
            dv.ev("n=>__C.open(n)", n); click(dv, '#tGpt'); dv.pg.wait_for_timeout(900)
            s = dv.ev("()=>__C.sheet()"); mb[n] = {'sheet': bool(s), 'mot': bool(s and s['mot'])}; dv.ev("()=>__C.closeSheets()")
        out['nb'] = mb
        out['gpText'] = dv.ev("()=>Object.fromEntries(Object.entries(GP))")
        out['keys'] = dv.ev("()=>SYNC_KEYS.filter(k=>k!=='gpt')")
        out['stores'] = dv.ev("k=>__J.stores(k)", out['keys'])   # 빈 기기 — gpt 말고 나머지 칸(새 판·바탕이 같아야)
        out['body'] = dv.ev("p=>__J.lastPut(p)", RP)
        out['errs'] = dv.errs[:5]
        out['cerr'] = list(dv.cerr)[:10]
    finally:
        dv.close()
    return out


def phys_side(br, eng, app, stat):
    """물리 72·97 — 모션 단추·iframe 이 바탕(같은 기록 · motion 만 다름)과 같은가"""
    dv = dv_open(br, eng, app, 'phys', None, stat)
    o = {}
    try:
        o['mot'] = dv.ev("()=>__C.mot()")
        for no in (72, 97):
            dv.ev("n=>__C.open(n)", no); click(dv, '#tGpt'); dv.pg.wait_for_timeout(900)
            s = dv.ev("()=>__C.sheet()") or {}
            f = {}
            if s.get('mot'):
                click(dv, '#gpMot'); dv.pg.wait_for_timeout(1500)
                f = dv.ev("()=>__C.frame()") or {}
            o[no] = {'read': s.get('read'), 'mot': s.get('mot'), 'src': f.get('src'), 'status': f.get('status'), 'same': f.get('same'), 'canvas': f.get('canvas')}
            dv.ev("()=>__C.closeSheets()")
        o['gp'] = dv.ev("()=>({a:GP[72]||'',b:GP[97]||''})")
    finally:
        dv.close()
    return o


def main():
    rn, rb, how = recs()
    sn, sb = statics()
    sb_raw = sb   # 옛 번호 이름 그대로(라벨 · 옛 값 표시용 — 판이 달라도 같은 줄 이름) — 아래 sb 는 uid 열쇠판 앱에 먹이려고 이름·목록을 uid 로 옮긴 것(§D-1)
    if UIDK:
        sb = uidify(sb)
    app = HU.git(GENIE, 'show', 'HEAD:jagwa/index.html')
    wt = open(os.path.join(GENIE, 'jagwa', 'index.html'), 'rb').read().replace(b'\r\n', b'\n')
    jn, jb = json.loads(rn.decode('utf-8')), json.loads(rb.decode('utf-8'))
    MDX = gpx(jn, NO)   # ★ uid_unify — 이 기록을 받은 기기의 이 칸 글(번호 칸 · uid 칸이면 도장 늦은 쪽 · 옛 판이면 MD 그대로)
    if MDX is None:
        MDX = MD
    QA_EXP = gp_qa_split(MDX)[0] if UIDK else ''   # §C-2 — 둘째 줄 왼쪽 = 풀이 글 첫 줄이 QA 꼴이면 그 줄 · 아니면 빈칸
    K5 = gkey('5')
    GPK = UID if UIDK else int(NO)   # N['gp'](GP 칸 열쇠 목록)에 이 판이 더하는 열쇠
    SEED = seed_rev()
    print('기록 = %s · 앱 = genie HEAD jagwa/index.html(작업트리와 %s) · 바탕 genie %s · 이 판 genie 커밋 %s · 적재 커밋 %s' % (
        how, '같음' if wt == app else '다름', BASE_REV, LANE or '(커밋 전)', SEED or '(커밋 전)'))
    t0 = time.time()
    base_fail = {}
    with sync_playwright() as pw:
        for eng in ENGS:
            br = getattr(pw, eng).launch()
            try:
                N = run_side(br, eng, 'NEW', app, rn, sn)
                B = run_side(br, eng, 'BASE', app, rb, sb)
                n, b = N[NO], B[NO]
                s, sbs = n['sheet'] or {}, b['sheet'] or {}
                p = s.get('p', '')
                ok1 = n['btn']['btn'] == 'Claude ✓' and n['btn']['last'] and n['btn']['vis'] and n['clicked'] and s.get('read') and not s.get('edit') \
                    and p == HEADP and 'undefined' not in p and ' ·  ' not in p and not p.endswith('·') and s.get('h2', '').startswith('%s번 Claude 풀이' % NO)
                if UIDK:   # ★ uid_unify 옛 잣대 고침 §C-1(제목 = uid Claude · 정답 … · 번호 글자 0) · §C-2(둘째 줄 = 왼쪽 QA 줄 · 오른쪽 「▶ 모션」) · §0-6(닻) — 옛 두 조건(머리 = 「G06-43-02 · 43회 2번」 · 제목 = 「N번 Claude 풀이」)만 갈았다
                    ok1 = (n['btn']['btn'] == 'Claude ✓' and n['btn']['last'] and n['btn']['vis'] and n['clicked'] and s.get('read') and not s.get('edit')
                           and UID == CODE and (s.get('h2') or '').rstrip('✕ ') == TITLE and '번' not in (s.get('h2') or '') and bool(s.get('sub')) and s.get('qa') == QA_EXP
                           and 'undefined' not in p and ' ·  ' not in p and not p.endswith('·'))
                    R(eng, 'B-1 uid 열쇠판 실측(참고) — 새 꼴 제목 · 둘째 줄 왼쪽 · 닻', None, None,
                      {'제목': s.get('h2'), '기대 제목': TITLE, '둘째 줄 왼쪽(QA)': s.get('qa'), '기대': QA_EXP, '둘째 줄 전체': p, '닻 uid · SPEC code': [UID, CODE]})
                okb1 = b['btn']['btn'] == 'Claude ✓' and bool(sbs.get('read'))
                R(eng, 'B-1 %s — 아랫줄 맨 오른쪽 「Claude ✓」 · 창 머리 둘째 줄 「%s」(undefined·빈 「 · 」 0) · 읽기 판이 먼저' % (NO, HEADP), ok1, okb1,
                  {'단추': n['btn'], '제목': s.get('h2'), '머리': p, '바탕 단추': b['btn']['btn'], '바탕 읽기 판': sbs.get('read')})
                head = [x.strip() for x in MD.split('\n\n')[0].replace('**', '').split('\n')]
                WANTX = WANT
                if UIDK:   # ★ uid_unify §C-3 — 읽기 판은 QA 첫 줄(과 바로 뒤 빈 줄)을 뺀 나머지 · 개수는 그 글에서 센다(옛 재료면 옛 SPEC 값과 같다 — 오프라인 대조 · 새 재료는 §D-2 표와 같다)
                    rest_x = gp_qa_split(MDX)[1]
                    WANTX = {k_: v_ for k_, v_ in gp_counts(rest_x).items() if k_ in WANT}
                    head = [x.strip() for x in rest_x.split('\n\n')[0].replace('**', '').split('\n')]
                p1 = [x.strip() for x in (s.get('p1') or '').split('\n')]
                # 옛 줄: ok2 = all(s.get(k) == v for k, v in WANT.items()) and s.get('script') == 0 and p1 == head
                ok2 = all(s.get(k) == v for k, v in WANTX.items()) and s.get('script') == 0 and p1 == head
                R(eng, 'B-2 읽기 판 — h3.gph %d(①~⑥) · ul.gpul li %d · ol.gpol li %d · table.gptb %d(th %d · tbody tr %d) · <b> %d · script 0 · 원문 첫 문단 %d줄 = 첫 p' % (
                    WANT['h3'], WANT['li'], WANT['ol'], WANT['tb'], WANT['th'], WANT['tr'], WANT['b'], len(head)),
                  ok2, all(sbs.get(k) == v for k, v in WANT.items()), dict({k: s.get(k) for k in list(WANT) + ['script']}, 첫문단=p1 == head, 첫문단줄=len(p1)))
                f = n.get('frame') or {}
                old = OLDNUM.findall(s.get('text', '') + ' ' + f.get('text', ''))
                R(eng, 'B-2 읽기 판·모션 글자에 옛 꼴 번호(G\\d\\d-\\d\\d-\\d(?!\\d) · C\\d-\\d{3}) 0', not old and bool(s.get('text')) and bool(f.get('text')), None, old[:5])
                if SPEC['kind'] == 'canvas':
                    # 옛 줄: ok3 = s.get('mot') and s.get('motTx') == '▶ 모션' and f.get('src') == 'motion/earth_111.html' and f.get('status') == 200 and f.get('same') \
                    # 옛 줄: and abs((f.get('h') or 0) - 480) <= 2 and f.get('canvas') == 3 and all((x or 0) > 0 for x in (f.get('cw') or [0])) and f.get('big') == ['earth_111.html', '_blank']
                    ok3 = s.get('mot') and s.get('motTx') == '▶ 모션' and f.get('src') == 'motion/earth_%s.html' % MOTK and f.get('status') == 200 and f.get('same') \
                        and abs((f.get('h') or 0) - 480) <= 2 and f.get('canvas') == 3 and all((x or 0) > 0 for x in (f.get('cw') or [0])) and big_ok(f.get('big'))   # ★ uid_unify §D-1 — src = motion/earth_<uid>.html · 「크게 보기」 href 는 옛 이름 · uid 이름 어느 쪽이든(파일 안 글자 — 그 링크가 가리키는 파일이 있나는 아래 새 칸이 잰다)
                    R(eng, 'B-3 111 모션 — 「▶ 모션」 · iframe motion/earth_111.html 200 · 같은 출처 · 480px · iframe 안 canvas 3(폭 잡음) · 「크게 보기」 earth_111.html _blank', ok3,
                      bool(sbs.get('mot')), {k: f.get(k) for k in ('src', 'status', 'same', 'h', 'canvas', 'cw', 'big')})
                    px = f.get('pix') or {}
                    okp = bool(px.get('앞')) and px.get('앞') not in ('empty',) and px.get('앞') == px.get('0.5초 뒤(누르기 앞)') and px.get('뒤') != px.get('앞') \
                        and isinstance(px.get('바뀐 ms'), int) and 0 <= px['바뀐 ms'] <= 1000
                    R(eng, 'B-3 「▶ 공전 (1년)」 진짜 누름 → 1초 안에 캔버스 ① 픽셀이 바뀜(누르기 앞 0.5초는 그대로 = 정지 대조)', okp, None, dict(px, err=f.get('err')))
                    m11 = f.get('m11') or {}
                    okm = PRIME in (m11.get('뒤') or '') and PRIME not in (m11.get('앞') or '') and m11.get('단추') == '실제 (약 430광년)'
                    R(eng, 'B-3 프리셋 「실제 (약 430광년)」 진짜 누름 → #m11 글자에 「″」(누르기 앞에는 없음)', okm, None, m11)
                else:   # svg 그림(119 · 움직임 없음) — e008 §B-3
                    # 옛 줄: ok3 = s.get('mot') and s.get('motTx') == '▶ 모션' and f.get('src') == 'motion/earth_%s.html' % NO and f.get('status') == 200 and f.get('same') \
                    # 옛 줄: and abs((f.get('h') or 0) - 480) <= 2 and f.get('svg') == 1 and f.get('ell') == SPEC['ell'] and f.get('canvas') == 0 and f.get('big') == ['earth_%s.html' % NO, '_blank']
                    ok3 = s.get('mot') and s.get('motTx') == '▶ 모션' and f.get('src') == 'motion/earth_%s.html' % MOTK and f.get('status') == 200 and f.get('same') \
                        and abs((f.get('h') or 0) - 480) <= 2 and f.get('svg') == 1 and f.get('ell') == SPEC['ell'] and f.get('canvas') == 0 and big_ok(f.get('big'))   # ★ uid_unify §D-1 — 위와 같다
                    R(eng, 'B-3 %s 모션 — 「▶ 모션」 · iframe motion/earth_%s.html 200 · 같은 출처 · 480px · iframe 안 svg#fig 1 · 그 안 ellipse(지평선) %d · canvas 0 · 「크게 보기」 earth_%s.html _blank' % (
                        NO, NO, SPEC['ell'], NO), ok3, bool(sbs.get('mot')), {k: f.get(k) for k in ('src', 'status', 'same', 'h', 'svg', 'ell', 'canvas', 'big')})
                bh_ = (f.get('big') or [None])[0]   # ★ uid_unify §D-1(새 칸 · 결함 후보) — 파일 이름만 바꾸고 안 글자는 그대로(바이트 무변)라 「크게 보기 ↗」 href 가 옛 이름을 가리킨다 → 새 탭에서 404 인지 잰다
                tgt_ = posixpath.normpath(posixpath.join(posixpath.dirname(f.get('src') or ''), bh_)) if bh_ else None
                R(eng, 'B-3 「크게 보기」 링크가 가리키는 motion 파일이 있다(파일 이름을 바꿔도 404 가 아니다)', bool(tgt_) and tgt_ in sn, None,
                  {'href': bh_, '가리키는 파일': tgt_, '있나': bool(tgt_) and tgt_ in sn, 'iframe src': f.get('src')})
                merr = [x for x in (N['cerr'] or []) if 'motion/' in x]
                R(eng, 'B-3 모션 iframe 쪽 콘솔 오류 0 · 페이지 오류(pageerror) 0', not merr and not N['errs'], None, {'모션': merr, 'pageerror': N['errs'], '앱 콘솔(참고)': N['cerr'][:4]})
                mp = (N['mot'] or {}).get('earth') if isinstance(N['mot'], dict) else None
                mbb = (B['mot'] or {}).get('earth') if isinstance(B['mot'], dict) else None
                j0 = json.loads(sb['motion/index.json'])
                want_me = (j0.get('earth') or []) + [int(NO)]
                if UIDK:   # ★ uid_unify §D-1 — motion/index.json 의 earth = uid 문자열(바탕 목록도 번호 → uid 로 옮겨 맞댄다)
                    want_me = (j0.get('earth') or []) + [UID]
                j0r = json.loads(sb_raw['motion/index.json'])   # 옛 번호 그대로 — 라벨용(판이 달라도 같은 줄 이름)
                mp_l = [int(U2N[x_]) if x_ in U2N else x_ for x_ in mp] if (UIDK and isinstance(mp, list)) else mp
                # 옛 줄: R(eng, 'B-3 지학 모션 번호(MOT.earth) = 바탕 %s + %s 로 시작 — 지금 %s' % (j0.get('earth'), NO, mp), (mp or [])[:len(want_me)] == want_me,
                # 옛 줄: (mbb or [])[:len(want_me)] == want_me, {'NEW': mp, 'BASE': mbb})
                R(eng, 'B-3 지학 모션 번호(MOT.earth) = 바탕 %s + %s 로 시작 — 지금 %s' % (j0r.get('earth'), NO, mp_l), (mp or [])[:len(want_me)] == want_me,
                  (mbb or [])[:len(want_me)] == want_me, {'NEW': mp, 'BASE': mbb})
                nb = N['nb']
                R(eng, 'B-3 이웃 %s — 모션 단추 0(창은 뜸) · %s — 모션 단추 그대로' % ('·'.join(map(str, NEIGH)), '·'.join(map(str, OTHERS))),
                  all(nb[k]['sheet'] and not nb[k]['mot'] for k in NEIGH) and all(nb[k]['mot'] for k in OTHERS),
                  None, nb)
                Pn, Pb = phys_side(br, eng, app, sn), phys_side(br, eng, app, sb)
                okph = {k: Pn[k] for k in (72, 97)} == {k: Pb[k] for k in (72, 97)} and Pn[72]['mot'] and Pn[72]['src'] == 'motion/phys_72.html' and Pn['gp'] == Pb['gp']
                R(eng, 'B-3 물리 72·97 — 모션 단추·iframe·GP = 바탕(무변)', okph, None, {'NEW': {k: Pn[k] for k in (72, 97)}, 'GP 같음': Pn['gp'] == Pb['gp']})
                # ── B-4 데이터 ──
                gk = [k for k in N['keys'] if N['stores'].get(k) != B['stores'].get(k)]
                # 옛 줄: g149, g84 = (jn['data'].get('gpt') or {}).get('149'), (jn['data'].get('gpt') or {}).get('84')
                g149, g84 = gpx(jn, '149'), gpx(jn, '84')   # ★ uid_unify §A-2 · §D-2 — 번호 칸 · uid 칸이면 도장 늦은 쪽의 글
                # 옛 줄: gO = {k: (jn['data'].get('gpt') or {}).get(str(k)) for k in OTHERS}   # 다른 Claude 칸(이 판이 안 건드림 · 119 판은 111 도)
                gO = {k: gpx(jn, str(k)) for k in OTHERS}   # 다른 Claude 칸(이 판이 안 건드림 · 119 판은 111 도) — ★ uid_unify: 도장 늦은 칸의 글
                body = json.loads(N['body']) if N['body'] else None
                bgp = (body or {}).get('data', {}).get('gpt') or {}
                # ★ 합치기 10/1(하위 에이전트 C) — revfix0929 A-1-3(2bc1719) 원격 옛 열쇠 묘비 → 새 열쇠 비춤(같은 칸 · 같은 시각)은 늘어난 묘비가 아니다
                _jg = jn.get('gone') or {}
                _o2n = {r_['옛uid']: r_['uid'] for r_ in json.loads(open(os.path.join(SPD, 'earth', '문항.json'), 'rb').read().decode('utf-8')) if r_.get('옛uid')}
                _mir = lambda k_, t_: any(j.split('|', 1)[0] == k_.split('|', 1)[0] and _o2n.get(j.split('|', 1)[1]) == k_.split('|', 1)[1] and _jg[j] == t_ for j in _jg if '|' in j)
                def _numtomb(k_, t_):   # ★ uid_unify §A-2 — 옮김이 더한 묘비 = 옮긴 칸의 옛 열쇠 「통|번호」(지금 시각 · 옛 판 기기용) · 이미 있던 번호 묘비를 uid 칸에 비춘 「통|uid」(같은 시각)
                    if not UIDK or '|' not in k_:
                        return False
                    k_k, c_ = k_.split('|', 1)
                    pre_ = 'card:' if (k_k == 'txt' and c_.startswith('card:')) else ''
                    c_ = c_[len(pre_):]
                    if k_k not in UID_STORES:
                        return False
                    if re.fullmatch(r'[1-9]\d*', c_) and c_ in N2U:
                        return True
                    return c_ in U2N and _jg.get(k_k + '|' + pre_ + U2N[c_]) == t_
                # 옛 줄: okb_ = body is None or (bgp.get(NO) == MD and all(bgp.get(str(k)) == gO[k] for k in OTHERS)
                #                         and all(k_ in _jg or _mir(k_, t_) for k_, t_ in (body.get('gone') or {}).items()))
                okb_ = body is None or (bgp.get(gkey(NO)) == MDX and all(bgp.get(gkey(str(k))) == gO[k] for k in OTHERS)
                                        and not (UIDK and [c_ for c_ in bgp if re.fullmatch(r'[1-9]\d*', c_)])   # §A-1 — 올린 몸통 gpt 에 번호 열쇠 0
                                        and all(k_ in _jg or _mir(k_, t_) or _numtomb(k_, t_) for k_, t_ in (body.get('gone') or {}).items()))
                # 옛 줄: ok6 = N['gpText'].get(NO) == MD and all(N['gpText'].get(str(k)) == gO[k] == mat('earth_%d.md' % k) and B['gpText'].get(str(k)) == gO[k] for k in OTHERS)
                ok6 = N['gpText'].get(gkey(NO)) == MDX and all(N['gpText'].get(gkey(str(k))) == gO[k] and known_mat(k, gO[k]) and B['gpText'].get(gkey(str(k))) == gO[k] for k in OTHERS)
                # 옛 줄: R(eng, 'B-4 빈 기기 — 동기화 뒤 GP[%s] = 재료 글자 전수(%d자) · %s = 기록 값 무변' % (NO, len(MD), '·'.join('GP[%d]' % k for k in OTHERS)), ok6, B['gpText'].get(NO) == MD,
                # 옛 줄: dict({'%s 길이' % NO: len(N['gpText'].get(NO) or '')}, **{'%d 같음' % k: N['gpText'].get(str(k)) == gO[k] for k in OTHERS}))
                R(eng, 'B-4 빈 기기 — 동기화 뒤 GP[%s] = 재료 글자 전수(%d자) · %s = 기록 값 무변' % (NO, len(MD), '·'.join('GP[%d]' % k for k in OTHERS)), ok6, B['gpText'].get(gkey(NO)) == MDX,
                  dict({'%s 길이' % NO: len(N['gpText'].get(gkey(NO)) or '')}, **{'%d 같음' % k: N['gpText'].get(gkey(str(k))) == gO[k] for k in OTHERS}))
                # 옛 줄: st111 = ((N['stores'].get('status') or {}).get(NO))
                st111 = ((N['stores'].get('status') or {}).get(gkey(NO)))   # ★ uid_unify §A-1 — status 열쇠 = uid
                R(eng, 'B-4 빈 기기 — gpt 말고 동기화 칸 %d 가 바탕과 같다(status.%s = Q 그대로) · GP 칸 = 바탕 + %s(지워진 칸 0) · 올린 몸통 gpt %s · 묘비 늘지 않음' % (
                    len(N['keys']), NO, NO, {3: '셋', 4: '넷'}.get(len(OTHERS) + 1, len(OTHERS) + 1)),
                  # 옛 줄: not gk and N['keys'] == B['keys'] and set(N['gp']) == set(B['gp']) | {int(NO)} and okb_ and st111 == (jn['data'].get('status') or {}).get(NO), None,
                  # 옛 줄: {'다른 칸': gk, 'GP': [N['gp'], B['gp']], 'status.%s' % NO: st111, '올린 몸통': 'PUT 없음' if body is None else 'gpt %s' % sorted(bgp, key=int)})
                  not gk and N['keys'] == B['keys'] and set(N['gp']) == set(B['gp']) | {GPK} and okb_ and ((_nob(st111) == _nob(rec_get(jn['data'].get('status'), NO))) if UIDK else (st111 == rec_get(jn['data'].get('status'), NO))), None,
                  {'다른 칸': gk, 'GP': [N['gp'], B['gp']], 'status.%s' % NO: st111, '올린 몸통': 'PUT 없음' if body is None else 'gpt %s' % sorted(bgp, key=lambda z_: (0, int(z_), '') if z_.isdigit() else (1, 0, z_))})
                # 기록 있는 기기 — 111 없는 기록으로 먼저 열고 5번 △(카드 안 [data-vmark=Q])를 진짜로 눌러(내 칸이 더 새것) 둔 뒤 적재 뒤 원격을 받는다
                dv = dv_open(br, eng, app, SUBJ, rb, sn)
                try:
                    keys = dv.ev("()=>SYNC_KEYS.filter(k=>k!=='gpt')")
                    # 옛 줄: dv.ev("n=>__C.open(n)", 5); h0 = dv.ev("()=>((ST[5]||{}).h||[]).length")
                    dv.ev("n=>__C.open(n)", 5); h0 = dv.ev("k=>((ST[k]||{}).h||[]).length", K5)   # ★ uid_unify §A-1 — ST 열쇠 = uid
                    # 옛 줄: cq = click(dv, '#card [data-vmark="Q"]'); dv.pg.wait_for_timeout(500); h1 = dv.ev("()=>((ST[5]||{}).h||[]).length")
                    cq = click(dv, '#card [data-vmark="Q"]'); dv.pg.wait_for_timeout(500); h1 = dv.ev("k=>((ST[k]||{}).h||[]).length", K5)
                    dv.ev("()=>{try{closeView()}catch(e){}}"); dv.ev("()=>__J.sync()")
                    before = dv.ev("k=>__J.stores(k)", keys)
                    load(dv, app, SUBJ, rn, sn)
                    after = dv.ev("k=>__J.stores(k)", keys)
                    gp = dv.ev("()=>Object.fromEntries(Object.entries(GP))")
                    body = json.loads(dv.ev("p=>__J.lastPut(p)", RP) or '{}')
                    bd = body.get('data', {})
                    same = {k: before.get(k) == after.get(k) for k in keys}
                    # 옛 줄: ok = cq and h1 == h0 + 1 and gp.get(NO) == MD and all(gp.get(str(k)) == gO[k] for k in OTHERS) and all(same.values()) \
                    # 옛 줄: and len(((after.get('status') or {}).get('5') or {}).get('h') or []) == h1 \
                    # 옛 줄: and (bd.get('gpt') or {}).get(NO) == MD and len(((bd.get('status') or {}).get('5') or {}).get('h') or []) == h1
                    ok = cq and h1 == h0 + 1 and gp.get(gkey(NO)) == MDX and all(gp.get(gkey(str(k))) == gO[k] for k in OTHERS) and all(same.values()) \
                        and len(((after.get('status') or {}).get(K5) or {}).get('h') or []) == h1 \
                        and (bd.get('gpt') or {}).get(gkey(NO)) == MDX and len(((bd.get('status') or {}).get(K5) or {}).get('h') or []) == h1
                    R(eng, 'B-4 기록 있는 기기 — 동기화 뒤 GP[%s] = 재료 · GP[%s] 무변 · 다른 칸 %d 무변 · 내 새 칸(5번 △ 진짜 누름) 안 덮임 · 올린 몸통에 %s·5번 둘 다' % (
                        NO, ']·['.join(map(str, OTHERS)), len(keys), NO),
                      # 옛 줄: ok, None, {'다른 칸': [k for k in keys if not same[k]], 'GP%s' % NO: len(gp.get(NO) or ''), '5번 회독': [h0, h1], '누름': cq})
                      ok, None, {'다른 칸': [k for k in keys if not same[k]], 'GP%s' % NO: len(gp.get(gkey(NO)) or ''), '5번 회독': [h0, h1], '누름': cq})
                finally:
                    dv.close()
                # 내 것이 더 새것 — 111 없는 기록 기기에서 111 Claude 창에 써서 저장(진짜 누름 · 원격 도장보다 뒤) → 적재 뒤 원격을 받아도 안 덮인다
                dv = dv_open(br, eng, app, SUBJ, rb, sn)
                try:
                    MY = '내가 먼저 쓴 %s번(검산)' % NO
                    dv.ev("n=>__C.open(n)", int(NO)); click(dv, '#tGpt'); dv.pg.wait_for_timeout(700)
                    dv.pg.locator('#gpIn').fill(MY); click(dv, '#gpSave'); dv.pg.wait_for_timeout(700)
                    dv.ev("()=>__C.closeSheets()"); dv.ev("()=>{try{closeView()}catch(e){}}"); dv.ev("()=>__J.sync()")
                    load(dv, app, SUBJ, rn, sn)
                    # 옛 줄: g = dv.ev("([n,os])=>({a:GP[n]||'',b:GP[149]||'',c:GP[84]||'',o:Object.fromEntries(os.map(k=>[k,GP[k]||'']))})", [int(NO), list(OTHERS)])
                    g = dv.ev("([n,os])=>({a:GP[n]||'',b:GP[149]||'',c:GP[84]||'',o:Object.fromEntries(os.map(k=>[k,GP[k]||'']))})", [(gkey(NO) if UIDK else int(NO)), [(gkey(str(k)) if UIDK else k) for k in OTHERS]])   # ★ uid_unify §A-1 — GP 열쇠 = uid
                    body = json.loads(dv.ev("p=>__J.lastPut(p)", RP) or '{}')
                    bg = body.get('data', {}).get('gpt') or {}
                    # 옛 줄: ok = g['a'] == MY and all(g['o'].get(str(k)) == gO[k] for k in OTHERS) and bg.get(NO) == MY and bg.get('149') == g149
                    ok = g['a'] == MY and all(g['o'].get(gkey(str(k))) == gO[k] for k in OTHERS) and bg.get(gkey(NO)) == MY and bg.get(gkey('149')) == g149
                    R(eng, 'B-4 내 것이 더 새것 — 원격 도장 뒤에 고친 GP[%s] 은 원격이 못 덮는다(claude_slot CL-6 ⓒ 잣대) · GP[%s] 그대로 · 올린 몸통도 내 것' % (NO, ']·['.join(map(str, OTHERS))), ok, None,
                      # 옛 줄: {NO: g['a'][:24], '·'.join(map(str, OTHERS)) + ' 같음': all(g['o'].get(str(k)) == gO[k] for k in OTHERS), '올린 %s' % NO: (bg.get(NO) or '')[:24]})
                      {NO: g['a'][:24], '·'.join(map(str, OTHERS)) + ' 같음': all(g['o'].get(gkey(str(k))) == gO[k] for k in OTHERS), '올린 %s' % NO: (bg.get(gkey(NO)) or '')[:24]})
                finally:
                    dv.close()
                # ── B-5 목록 ──
                # 옛 줄: want = sorted(int(k) for k in (jn['data'].get('gpt') or {}))
                want = sorted({int(k_) if k_.isdigit() else int(U2N[k_]) for k_ in (jn['data'].get('gpt') or {}) if k_.isdigit() or k_ in U2N})   # ★ uid_unify — 번호 칸 · uid 칸(D-2) 둘 다 그 문항의 화면 번호로
                okl = N['list']['tags'] == want and int(NO) in want and set(OTHERS) <= set(want) and N['list']['txt'] == ['Claude']
                R(eng, 'B-5 목록 — .tag.gp 「Claude」 줄 = 기록 gpt 칸 번호 %s(%s) · 다른 줄 0' % (want, '·'.join([NO] + [str(k) for k in OTHERS])), okl, B['list']['tags'] == want,
                  {'NEW': N['list'], 'BASE 태그': B['list']['tags']})
                base_fail[eng] = {'B-1': not okb1, 'B-3': not bool(sbs.get('mot')) and (mbb or [])[:len(want_me)] != want_me, 'B-5': B['list']['tags'] != want}
            finally:
                br.close()
    # ── 헛잣대 · 정적 ──
    for eng, bf in base_fail.items():
        R(eng, 'B-7 헛잣대 — 바탕(이 판 앞 motion · %s 없는 기록)에서 B-1·B-3·B-5 가 FAIL' % NO, all(bf.values()), None, bf)
    if LANE:
        lf = git1(GENIE, 'diff', '--name-only', LANE + '~1', LANE).split()
        jx = json.loads(HU.git(GENIE, 'show', LANE + ':jagwa/motion/index.json').decode('utf-8'))
        j1 = json.loads(HU.git(GENIE, 'show', LANE + '~1:jagwa/motion/index.json').decode('utf-8'))
        where = 'genie 커밋 %s' % LANE
    else:
        lf = [x[3:] for x in HU.git(GENIE, 'status', '--porcelain', '--untracked-files=all', '--', 'jagwa').decode('utf-8', 'replace').split('\n') if x.strip()]   # strip 하면 첫 줄 앞 공백이 빠져 한 글자 더 잘린다(10/1 첫 실행)
        jx, j1 = json.loads(sn['motion/index.json']), json.loads(HU.git(GENIE, 'show', 'HEAD:jagwa/motion/index.json').decode('utf-8'))
        where = 'genie 작업트리(커밋 전)'
    R('-', 'B-6 jagwa/index.html 바이트 무변 — 작업트리 = HEAD · %s 가 바꾼 파일 = motion 둘뿐 %s' % (where, lf),
      wt == app and sorted(lf) == sorted(['jagwa/motion/index.json', MOTF]), None, hashlib.md5(wt).hexdigest()[:8])
    R('-', 'A-2 이 판이 남긴 motion/index.json(%s) = 앞 판 값의 earth 끝에 %s 만 더함 — earth %s → %s · phys %s 무변 · 키 무변' % (where, NO, j1.get('earth'), jx.get('earth'), j1.get('phys')),
      jx.get('earth') == (j1.get('earth') or []) + [int(NO)] and jx.get('phys') == j1.get('phys') and set(jx) == set(j1), None, json.dumps(jx))
    j, j0 = json.loads(sn['motion/index.json']), json.loads(sb['motion/index.json'])
    # 옛 줄: R('-', 'A-2 지금 motion/index.json — earth 가 바탕 %s + [%s] 로 시작 · phys 가 바탕 %s 로 시작(값·차례 무변 · 뒤 판이 끝에 더한 것만 허용) · 바탕 키 다 있음' % (j0.get('earth'), NO, j0.get('phys')),
    # 옛 줄: (j.get('earth') or [])[:len(j0.get('earth') or []) + 1] == (j0.get('earth') or []) + [int(NO)] and (j.get('phys') or [])[:len(j0.get('phys') or [])] == (j0.get('phys') or [])
    # 옛 줄: and set(j0) <= set(j), False, sn['motion/index.json'].decode().strip())
    j0r = json.loads(sb_raw['motion/index.json'])   # 옛 번호 그대로 — 라벨용
    R('-', 'A-2 지금 motion/index.json — earth 가 바탕 %s + [%s] 로 시작 · phys 가 바탕 %s 로 시작(값·차례 무변 · 뒤 판이 끝에 더한 것만 허용) · 바탕 키 다 있음' % (j0r.get('earth'), NO, j0r.get('phys')),
      (j.get('earth') or [])[:len(j0.get('earth') or []) + 1] == (j0.get('earth') or []) + [UID if UIDK else int(NO)] and (j.get('phys') or [])[:len(j0.get('phys') or [])] == (j0.get('phys') or [])
      and set(j0) <= set(j), False, sn['motion/index.json'].decode().strip())   # ★ uid_unify §D-1 — earth = uid 문자열(바탕 번호 목록은 uid 로 옮겨 맞댐)
    SEED = seed_rev()
    if SEED:
        fs = git1(SPD, 'diff', '--name-only', SEED + '~1', SEED).split()
        old, new = HU.git(SPD, 'show', SEED + '~1:' + RP), HU.git(SPD, 'show', SEED + ':' + RP)
        where = 'studyplandata 커밋 %s' % SEED
    else:
        fs = [x[3:] for x in HU.git(SPD, 'status', '--porcelain').decode('utf-8', 'replace').split('\n') if x.strip()]
        old, new = HU.git(SPD, 'show', 'HEAD:' + RP), open(os.path.join(SPD, 'earth', '기록.json'), 'rb').read()
        where = 'studyplandata HEAD → 작업트리(커밋 전)'
    do, dn = json.loads(old.decode('utf-8')), json.loads(new.decode('utf-8'))
    if NO in (dn['data'].get('gpt') or {}) and NO not in (do['data'].get('gpt') or {}):
        x = json.loads(json.dumps(dn)); x['data']['gpt'].pop(NO); x['u'].pop('gpt|' + NO, None)
        y = json.loads(json.dumps(do))
        for z in (x, y):
            z.pop('savedAt', None)
        R('-', 'A-3 적재(%s) — 바꾼 파일 = earth/기록.json 하나 · data.gpt["%s"] = 재료 · u["gpt|%s"] 둘(+savedAt)만 더함 · status.%s 등 다른 칸·gone 무변(물리·생물 기록 무변)' % (where, NO, NO, NO),
          x == y and dn['data']['gpt'][NO] == MD and isinstance(dn['u'].get('gpt|' + NO), int) and fs == [RP], None,
          {'파일': fs, '도장': dn['u'].get('gpt|' + NO), 'savedAt': [do.get('savedAt'), dn.get('savedAt')], 'status.%s' % NO: (dn['data'].get('status') or {}).get(NO)})
    else:
        R('-', 'A-3 적재(%s) — 아직 적재 전(합성 기록으로 잼)' % where, None, None, '')
    P = json.loads(open(os.path.join(SPD, 'phys', '기록.json'), 'rb').read().decode('utf-8'))
    pg = P['data'].get('gpt') or {}
    Bi = json.loads(open(os.path.join(SPD, 'bio', '기록.json'), 'rb').read().decode('utf-8'))
    R('-', 'B-6 물리 gpt["97"] = 재료 phys_97.md 글자 그대로 · gpt["72"] 있음(무변) · 생물 gpt = %s' % json.dumps(Bi['data'].get('gpt')),
      pg.get('97') == mat('phys_97.md') and bool(pg.get('72')), None, {'물리 gpt': sorted(pg, key=int)})
    # 옛 줄: f = 'motion/earth_%s.html' % NO
    fl = 'motion/earth_%s.html' % NO   # 라벨용(옛 이름 · 판이 달라도 같은 줄 이름)
    f = 'motion/earth_%s.html' % MOTK   # ★ uid_unify §D-1 — 카드 층 모션 파일 = earth_<uid>.html(바이트 무변 · 재료 = 옛 이름 파일)
    src = open(os.path.join(MAT, 'earth_%s.html' % NO), 'rb').read()
    # 옛 줄: R('-', 'A-1 %s = 재료 바이트(줄끝만 뺀 대조 · 재료 %d B · md5 %s)' % (f, len(src), hashlib.md5(src).hexdigest()[:8]),
    R('-', 'A-1 %s = 재료 바이트(줄끝만 뺀 대조 · 재료 %d B · md5 %s)' % (fl, len(src), hashlib.md5(src).hexdigest()[:8]),
      (sn.get(f) or b'').replace(b'\r\n', b'\n') == src.replace(b'\r\n', b'\n'), None, len(sn.get(f) or b''))
    # 옛 줄: ix = git1(GENIE, 'ls-files', '-s', '--', MOTF).split()
    ix = git1(GENIE, 'ls-files', '-s', '--', MOTF_NOW).split()   # ★ uid_unify §D-1 — 지금 파일 이름
    if ix:
        blob = HU.git(GENIE, 'cat-file', '-p', ix[1])
        # 옛 줄: R('-', 'A-1 %s git blob = 재료 바이트 그대로(md5 %s)' % (f, hashlib.md5(blob).hexdigest()[:8]), blob == src, None, len(blob))
        R('-', 'A-1 %s git blob = 재료 바이트 그대로(md5 %s)' % (fl, hashlib.md5(blob).hexdigest()[:8]), blob == src, None, len(blob))
    else:
        # 옛 줄: R('-', 'A-1 %s — 아직 git 에 안 올림(blob 대조는 스테이징 뒤)' % f, None, None, '')
        R('-', 'A-1 %s — 아직 git 에 안 올림(blob 대조는 스테이징 뒤)' % fl, None, None, '')
    tx = (sn.get(f) or b'').decode('utf-8', 'replace')
    if SPEC['kind'] == 'canvas':
        # 옛 줄: R('-', '%s — 바깥 스크립트·글꼴·주소 0(<script src · <link · @import · http) · canvas 3 · .pdf 0(공개 genie · D11)' % f,
        R('-', '%s — 바깥 스크립트·글꼴·주소 0(<script src · <link · @import · http) · canvas 3 · .pdf 0(공개 genie · D11)' % fl,
          not re.search(r'<script[^>]*\bsrc\s*=', tx) and not re.search(r'<link\b', tx) and '@import' not in tx and not re.findall(r'https?://', tx)
          and tx.count('<canvas') == 3 and '.pdf' not in tx.lower(), None, re.findall(r'https?://[^\s"\'<>]+', tx)[:3])
    else:   # svg 그림 — 「http」 는 svg 이름공간 글자뿐이어야(불러오기 아님)
        urls = [u for u in re.findall(r'https?://[^\s"\'<>]+', tx) if u not in NSURI]
        # 옛 줄: R('-', '%s — 바깥 스크립트·글꼴·주소 0(<script src · <link · @import · http — svg 이름공간 글자만 허용) · svg#fig 1 · canvas 0 · .pdf 0(공개 genie · D11)' % f,
        R('-', '%s — 바깥 스크립트·글꼴·주소 0(<script src · <link · @import · http — svg 이름공간 글자만 허용) · svg#fig 1 · canvas 0 · .pdf 0(공개 genie · D11)' % fl,
          not re.search(r'<script[^>]*\bsrc\s*=', tx) and not re.search(r'<link\b', tx) and '@import' not in tx and not urls
          and len(re.findall(r'<svg[^>]*\bid=["\']fig["\']', tx)) == 1 and tx.count('<canvas') == 0 and '.pdf' not in tx.lower(), None,
          {'주소(이름공간 뺌)': urls[:3], '이름공간': [u for u in re.findall(r'https?://[^\s"\'<>]+', tx) if u in NSURI][:2]})
    R('-', 'motion 폴더에 .pdf 0', not [k for k in sn if k.lower().endswith('.pdf')], None, sorted(sn))
    npass = sum(1 for r in ROWS if r[2] is True); nfail = sum(1 for r in ROWS if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초 · 기록 %s' % (npass, nfail, time.time() - t0, how))
    with io.open(OUTF, 'a', encoding='utf-8') as fo:
        fo.write('\n==== %s · claude_e004 CE4%s · 기록 %s · genie HEAD %s · 바탕 %s · 이 판 커밋 %s · studyplandata HEAD %s · 적재 %s · 엔진 %s ====\n' % (
            time.strftime('%Y-%m-%d %H:%M'), '' if NO == '111' else ' · 번호 %s' % NO, how, git1(GENIE, 'rev-parse', '--short', 'HEAD'), BASE_REV, LANE or '-',
            git1(SPD, 'rev-parse', '--short', 'HEAD'), SEED or '-', ','.join(ENGS)))
        for eng, nm, okn, okb, v in ROWS:
            fo.write('%s | 바탕 %s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[okn], {True: 'PASS', False: 'FAIL', None: '—'}[okb], eng, nm,
                     (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str))[:1200]))
        fo.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
