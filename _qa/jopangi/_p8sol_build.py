# -*- coding: utf-8 -*-
r"""_task_jo_p8sol §A-1 — 해례 8판 해설 뽑기(⚙) → 특상디\_p8up\_p8sol.json

  두 PDF(7판 _m · 8판)를 같은 길로 읽는다 — 보이는 줄(흰 덮개 밑 숨은 글 뺌 · p7_visible 규칙) · 같은 높이 조각 한 줄 · 쪽 머리(y<62) ·
  쪽 아래 띠(y≥815) · 워터마크 꼴 줄(「@」 또는 휴대전화 꼴 — 값은 어디에도 안 남김) · 오른쪽 답 칸(「답 I x I」) 버림
  지문 덩어리 = 「N.」 머리(본문 x 보다 15pt 넘게 왼쪽) 또는 「[유제…]」 머리부터 다음 머리 전까지 · 「해설」 줄부터 끝 = 해설(머리 글자 뗌)
  선지 조각 = 해설 안 「①…(O)」·「ㄱ, ㄷ (X)」·「가. (△)」 꼴 표지부터 다음 표지 전까지(표지 = 줄 첫머리 · 원문자/자모/가나다 + 판정 괄호)

  헛잣대(§A-1-2) — 7판을 같은 길로 읽어 앱 sol 이 그대로 나오나(통째 · 조각) · 수를 낸다
    python _p8sol_build.py --probe7          7판 되살림 셈만
    python _p8sol_build.py [--write]         8판까지 · 대조표와 맞대 · 산출 쓰기
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import io, os, re, sys, json, hashlib, collections, difflib
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, u'특상디', u'_toc_fuse', 'code'))
import p7_visible as PV   # noqa: E402

PDF7 = os.path.join(HERE, u'특상디', u'_pdf', u'특허법_해례_기출_객관식_제7판_m.pdf')
PDF8 = os.path.join(HERE, u'특상디', u'_pdf', u'특허법 해례 기출 객관식 제8판.pdf')
MD5_8 = '94f115f0a0e2d4387278e600e12fb753'
OUT = os.path.join(HERE, u'특상디', u'_p8up', '_p8sol.json')
REF = os.path.join(HERE, 'task', '_ref_p8sol.json')
APP = os.environ.get('P8SOL_APP') or _roots.genie(r'jo\data\jimun_7pan.json')
WMX = re.compile(r'@|01[016789][-\s./]?\d{3,4}[-\s./]?\d{4}')
ANSL = re.compile(r'^\s*답\s*[I|lⅠ]')
ANSONLY = re.compile(r'^\s*답\s*[I|lⅠ](?:\s*[^\sI|lⅠ]{1,4}\s*[I|lⅠ])+\s*$')
ANSTAIL = re.compile(r'\s*답\s*[I|lⅠ](?:\s*[^\sI|lⅠ]{1,4}(?:\s*,\s*[^\sI|lⅠ]{1,4})*\s*[I|lⅠ])+\s*$|\s+답\s*[I|lⅠ]\s*\S{1,4}\s*$')   # 빈칸 없이 붙은 「…]답 I O I」 · 「답 I ㄱ,ㄴ,ㅁ I」 도
HEAD = re.compile(r'^\s*(\d{1,3})\.\s*(.*)$')
YUJE = re.compile(r'^\s*\[\s*유제\s*(\d*)\s*\]')
SOLH = re.compile(r'^\s*해\s*설\s*')
CHAPTER = re.compile(r'^\s*(?:제\s*\d+\s*[편장절관]\s|[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+\s)')   # 편·장·절 머리 · 로마 숫자 절 머리(짧은 줄만)
MARK = re.compile(r'(?:(?<=\s)|^)((?:(?:[①-⑩]|[ㄱ-ㅎ]|[가-하])[ \t]*[.,·ㆍ]?[ \t]*(?:및[ \t]*)?)+)\(\s*([OX△])\s*\)')   # 표지는 줄 한가운데에도 온다
BARE_BAD = []   # revfix0929 A-1 — 표지뿐 조각인데 8판 제 조각이 앱 글과 다른 줄(있으면 멈춘다)
RANGE7 = (11, 609)
RANGE8 = (11, 646)


def open_pdf(path):
    PV.PDF = path
    PV._DOC = None
    return PV.doc()


NOTEFONT = ('AppleSDGothicNeo',)   # 사용자 필기 사본(_m)에 덧쓴 메모 글꼴 — 책 글이 아니다(「{47⑤/52①단…}」 등)
SUBHEAD = re.compile(r'^\s*\[\s*\d{1,2}\s*\]\s*\S')


def vis_lines(pno, ytol=2.5):
    """p7_visible.visible_lines 와 같은 규칙(흰 덮개 밑 숨은 조각 · 굵은 글 흉내 겹침 뺌 · 같은 높이 한 줄) + 메모 글꼴 조각 뺌"""
    pg = PV.doc()[pno - 1]
    wb = PV._white_boxes(pg)
    ch = []    # 글자 단위(8판은 글자층 조각 하나가 여러 줄에 걸친다 — 조각 윗변으로 묶으면 줄이 섞인다)
    for sp in pg.get_texttrace():
        if str(sp.get('font') or '').startswith(NOTEFONT):
            continue
        bb, sq = tuple(sp['bbox']), sp.get('seqno', 0)
        if any(sq < s2 and PV._cover(box, bb) > 0.8 for box, s2 in wb):
            continue
        for c in sp['chars']:
            if c[0] <= 0:
                continue
            cb = c[3]
            if any(PV._cover(box, cb) > 0.8 and sq < s2 for box, s2 in wb):
                continue
            ch.append((c[2][1], c[2][0], chr(c[0]), cb[2]))
    ch.sort(key=lambda c: (round(c[0], 1), c[1]))
    lines = []
    for y, x, u, xr in ch:
        L = next((L for L in lines[-3:] if abs(L['y'] - y) <= ytol), None)
        if L is None:
            L = {'y': y, 'c': []}; lines.append(L)
        # 굵은 글 흉내 — 같은 글자를 0.3pt 옆에 한 번 더 찍는다 → 1pt 안 같은 글자는 버린다
        if any(k[2] == u and abs(k[0] - x) < 1.0 for k in L['c'][-4:]) and not u.isspace():
            continue
        L['c'].append((x, xr, u))
    out = []
    lines.sort(key=lambda L: L['y'])
    for L in lines:
        cs = sorted(L['c'])
        t = ''
        for i, (x, xr, u) in enumerate(cs):
            if i and not u.isspace() and not t.endswith(' ') and x - cs[i - 1][1] > 2.5:
                t += ' '     # 글자 사이가 벌어졌는데 빈칸 글자가 없으면(다른 조각) 한 칸
            t += u
        if t.strip():
            out.append((round(L['y'], 1), round(cs[0][0], 1), t))
    return out


def page_lines(pno):
    """보이는 줄 [(y, x, text)] — 머리·아래 띠·워터마크 꼴·답 칸 뺌 · 워터마크 꼴은 버린 줄 수만 센다"""
    out, wm = [], 0
    for y, x, t in vis_lines(pno):
        s = t.rstrip()
        if not s.strip():
            continue
        if WMX.search(s):
            wm += 1
            continue
        if y < 62 or y >= 815:
            continue
        if ANSL.match(s) and (x > 380 or ANSONLY.match(s)):
            continue
        s = ANSTAIL.sub('', s).rstrip()   # 같은 높이로 합쳐진 오른쪽 답 칸 「답 I O I」
        if not s.strip():
            continue
        out.append((y, x, s))
    return out, wm


def blocks(path, rng):
    doc = open_pdf(path)
    B, cur, wm = [], None, 0
    for pno in range(rng[0], rng[1] + 1):
        L, w = page_lines(pno)
        wm += w
        if not L:
            continue
        xs = collections.Counter(round(x) for y, x, t in L)
        bx = xs.most_common(1)[0][0]
        for y, x, t in L:
            m, yj = HEAD.match(t), YUJE.match(t)
            if (m and x < bx - 15) or (yj and abs(x - bx) < 6):
                cur = {'pdf': pno, 'y': y, 'no': m.group(1) if m and x < bx - 15 else u'유제' + (yj.group(1) if yj else ''),
                       'body': [], 'sol': None}
                B.append(cur)
                rest = m.group(2) if (m and x < bx - 15) else t
                if rest.strip():
                    cur['body'].append(rest.strip())
                continue
            if cur is None:
                continue
            if cur['sol'] is None and SOLH.match(t):
                cur['sol'] = [SOLH.sub('', t, count=1)]
                continue
            if (CHAPTER.match(t) or SUBHEAD.match(t)) and len(t.strip()) < 40:
                continue
            (cur['sol'] if cur['sol'] is not None else cur['body']).append(t.strip() if cur['sol'] is None else t)
    for b in B:
        b['body'] = '\n'.join(b['body'])
        b['sol'] = clean('\n'.join(b['sol'])) if b['sol'] is not None else ''
    return B, wm


TAGX = re.compile(r'\[\s*(?:\d{2}(?:[\s·,ㆍ]+\d{2})*\s*(?:변리|사법)|미기출)\s*\]')


def clean(s):
    s = '\n'.join(l.rstrip() for l in s.split('\n'))
    s = TAGX.sub('', s)
    return re.sub(r'\n{3,}', '\n\n', s).strip()


def ws(s):
    return re.sub(r'\s+', '', s or '')


NAMEX = re.compile(r'(?:특허청장|지식재산처장|특허청|지식재산처)(?:은|는|이|가|을|를|에게|에|의|과|와|으로|로)?')


def cat_of(a, b):
    if ws(a) == ws(b):
        return u'같음'
    if NAMEX.sub('', ws(a)) == NAMEX.sub('', ws(b)):   # 빈칸 먼저 뺌 — 「지식재산처장\n에게」 처럼 줄바꿈이 조사를 떼어 놓는다
        return u'명칭만'
    return u'바뀜'


def frags(sol):
    """선지 조각 [(표지 글자 집합, 조각 글)] — 표지부터 다음 표지 전까지"""
    ms = list(MARK.finditer(sol))
    out = []
    for i, m in enumerate(ms):
        e = ms[i + 1].start() if i + 1 < len(ms) else len(sol)
        labs = frozenset(re.findall(u'[①-⑩]|[ㄱ-ㅎ]|[가-하]', m.group(1)))
        out.append((labs, sol[m.start():e].strip()))
    return out


def marks_ws(sol):
    """표지 [(빈칸 뺀 자리, 표지 글자 집합, 판정)] — 빈칸 뺀 글 좌표"""
    return [(len(ws(sol[:m.start()])), frozenset(re.findall(u'[①-⑩]|[ㄱ-ㅎ]|[가-하]', m.group(1))), m.group(2)) for m in MARK.finditer(sol)]


def span_of(bsol, frag):
    """앱 조각이 덩어리 해설 안 「표지 사이」에 놓이나 → (시작 표지 i, 끝 표지 j 또는 None=끝) · 아니면 None"""
    W, w = ws(bsol), ws(frag)
    if not w:
        return None
    mk = marks_ws(bsol)
    starts = [p for p, l, v in mk]
    k = W.find(w)
    while k >= 0:
        e = k + len(w)
        if k in starts and (e == len(W) or e in starts):
            return (starts.index(k), starts.index(e) if e in starts else None)
        k = W.find(w, k + 1)
    return None


def lab_of(frag):
    m = MARK.match(frag or '')
    return frozenset(re.findall(u'[①-⑩]|[ㄱ-ㅎ]|[가-하]', m.group(1))) if m else None


def probe7():
    B7, wm = blocks(PDF7, RANGE7)
    app = json.load(io.open(APP, encoding='utf-8'))['지문']
    by = collections.defaultdict(list)
    for b in B7:
        by[b['pdf']].append(b)
    c = collections.Counter()
    miss = []
    for z in app:
        s = clean(z.get('sol') or '')
        if not s:
            continue
        p = int(z.get('pdf쪽') or 0)
        cands = [b for q in (p - 1, p, p + 1) for b in by.get(q, []) if b['sol']]
        w = ws(s)
        whole = [b for b in cands if ws(b['sol']) == w]
        if whole:
            c['통째'] += 1; continue
        inb = [b for b in cands if w and w in ws(b['sol'])]
        if inb:
            sp = [span_of(b['sol'], s) for b in inb]
            sp = [x for x in sp if x]
            c['조각(표지 사이)' if sp else '조각(듦 · 표지 사이 아님)'] += 1
            if not sp:
                miss.append((z['id'], 'in', s[:40]))
            continue
        c['안 맞음'] += 1
        miss.append((z['id'], 'none', s[:40]))
    print('7판 덩어리 %d · 해설 있는 덩어리 %d · 워터마크 꼴 줄 %d(값 안 남김)' % (len(B7), sum(1 for b in B7 if b['sol']), wm))
    print('앱 sol 되살림', dict(c))
    for m in miss[:40]:
        print('  ', m)
    return B7, c, miss


def sim(a, b):
    a, b = NAMEX.sub('', ws(a)), NAMEX.sub('', ws(b))
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def locate7(z, by7):
    """앱 줄 → (7판 덩어리, 갈래, 표지 자리) — 통째 · 조각(표지 사이) · 잘림(표지부터 · 다음 표지 앞에서 끊김) · 듦 · 없음"""
    s = clean(z.get('sol') or '')
    if not s:
        return None, u'해설없음', None
    p = int(z.get('pdf쪽') or 0)
    cands = [b for q in (p - 1, p, p + 1, p + 2) for b in by7.get(q, []) if b['sol']]
    w = ws(s)
    for b in cands:
        if ws(b['sol']) == w:
            return b, u'통째', None
    for b in cands:
        sp = span_of(b['sol'], s)
        if sp:
            return b, u'조각', sp
    for b in cands:     # 잘림 — 표지에서 시작해 다음 표지 전 어딘가에서 끊긴 앱 조각(책보다 짧다)
        W = ws(b['sol']); mk = marks_ws(b['sol']); st = [q for q, l, v in mk]
        k = W.find(w)
        if k in st:
            i = st.index(k)
            e = st[i + 1] if i + 1 < len(st) else len(W)
            if k + len(w) < e:
                return b, u'잘림', (i, i + 1 if i + 1 < len(st) else None)
    for b in cands:
        if w in ws(b['sol']):
            return b, u'듦', None
    # 닮음 — 표를 앱이 칸마다 따로 뽑아 글 순서만 다른 줄 · 앱 글 글자의 95% 이상이 덩어리 안에 있으면 그 덩어리
    bag = collections.Counter(w)
    sc = sorted(((sum((bag & collections.Counter(ws(b['sol']))).values()) / float(len(w)), -len(b['sol']), k) for k, b in enumerate(cands)), reverse=True)
    if sc and sc[0][0] >= 0.85:
        return cands[sc[0][2]], u'닮음', None
    return None, u'없음', None


def shape(s):
    """앱 줄 해설의 꼴 — 통째 · 조각(표지부터) · 머리+조각(공통 머리 + 빈 줄 + 표지부터)"""
    s = clean(s or '')
    parts = s.split('\n\n')
    if len(parts) >= 2 and MARK.match(parts[-1].strip()):
        return u'머리+조각', lab_of(parts[-1].strip())
    if MARK.match(s):
        return u'조각', lab_of(s)
    return u'통째', None


def map_span(sol7, sol8, frag):
    """7판 덩어리 안 조각(빈칸 뺀 글이 그대로 든다) → 8판 해설의 같은 자리 글 · 두 판 글을 맞춰(difflib) 앞끝·뒤끝을 옮긴다"""
    W7, w = ws(sol7), ws(frag)
    k = W7.find(w)
    if not w or k < 0:
        return None
    e = k + len(w)
    idx8 = [i for i, ch in enumerate(sol8) if not ch.isspace()]
    W8 = ''.join(sol8[i] for i in idx8)
    mb = [m for m in difflib.SequenceMatcher(None, W7, W8, autojunk=False).get_matching_blocks() if m.size]
    # 앞끝이 안 맞은 틈(「특허청장」→「지식재산처장」)에 떨어지면 틈 앞 맞은 칸 끝으로 · 뒤끝은 틈 뒤 맞은 칸 머리로 — 바뀐 글을 틈째 안는다
    a8 = next((m.b + (k - m.a) for m in mb if m.a <= k < m.a + m.size), None)
    if a8 is None:
        a8 = max([m.b + m.size for m in mb if m.a + m.size <= k] or [0])
    b8 = next((m.b + (e - m.a) for m in mb if m.a < e <= m.a + m.size), None)
    if b8 is None:
        b8 = min([m.b for m in mb if m.a >= e] or [len(W8)])
    if a8 is None or b8 is None or b8 <= a8:
        return None
    return sol8[idx8[a8]:idx8[b8 - 1] + 1].strip()


TAILBOX = re.compile(r'\s*\n\s*(?:(?:(?:시행령|시행규칙)\s*)?제\s*\d+\s*조(?:의\s*\d+)?\s*\(|\[\d+\])')


def really_cut(bsol, sp, s):
    """잘림 후보 — 책 조각에서 앱 글 뒤에 남은 꼬리가 조문 상자·곁상자로 새 줄에서 시작하면 잘린 것이 아니다"""
    full = cut8(bsol, sp, bsol) or ''
    n, pos = len(ws(clean(s or ''))), 0
    for pos, ch in enumerate(full):
        if n == 0:
            break
        if not ch.isspace():
            n -= 1
    else:
        pos = len(full)
    return not TAILBOX.match(full[pos:])


def bare_mark(s):
    """앱 조각이 표지뿐인가(「② (O)」)"""
    m = MARK.match(clean(s or ''))
    return bool(m) and not clean(s or '')[m.end():].strip()


def grow(bsol, lab):
    """표지 lab 조각이 덩어리에서 글 없이 바로 다음 표지로 이어지면(공동 해설) 글이 있는 표지 조각까지 이어 붙인 전문 · 아니면 None"""
    fs = frags(bsol)
    i = next((k for k, (l, f) in enumerate(fs) if l == lab), None)
    if i is None or not bare_mark(fs[i][1]) or i + 1 >= len(fs):
        return None
    j = i + 1
    while j < len(fs) - 1 and bare_mark(fs[j][1]):
        j += 1
    ms = list(MARK.finditer(bsol))
    e = ms[j + 1].start() if j + 1 < len(ms) else len(bsol)
    return bsol[ms[i].start():e].strip()


def piece(bsol, shp):
    """덩어리 해설에서 앱 줄 꼴대로 떼어 낸 글 · 못 떼면 None"""
    kind, lab = shp
    if kind == u'통째':
        return bsol
    f = next((fr for l, fr in frags(bsol) if l == lab), None)
    if f is None and lab:
        # 표지 묶음이 판마다 다르다(P7-1209 「ㄹ, ㅁ. (O)」 → 8판 「ㄹ, (O)」) — 앱 표지의 부분집합인 조각이 하나뿐이면 그것
        sub = [fr for l, fr in frags(bsol) if l and l <= lab]
        f = sub[0] if len(sub) == 1 else None
    if f is None:
        return None
    if kind == u'조각':
        return f
    m = MARK.search(bsol)
    return bsol[:m.start()].strip() + '\n\n' + f


def cut8(sol7, sp, sol8):
    """7판 표지 자리(i, j) → 8판 해설에서 같은 표지 글자 집합 사이 · 못 찾으면 None"""
    m7, m8 = marks_ws(sol7), list(MARK.finditer(sol8))
    L8 = [frozenset(re.findall(u'[①-⑩]|[ㄱ-ㅎ]|[가-하]', m.group(1))) for m in m8]
    i, j = sp
    li = m7[i][1]
    lj = m7[j][1] if j is not None else None
    if li not in L8:
        return None
    a = L8.index(li)
    if lj is None:
        e = len(sol8)
    else:
        nxt = [k for k in range(a + 1, len(L8)) if L8[k] == lj]
        if not nxt:
            return None
        e = m8[nxt[0]].start()
    return sol8[m8[a].start():e].strip()


def build():
    import pymupdf
    if hashlib.md5(open(PDF8, 'rb').read()).hexdigest() != MD5_8:
        sys.exit('NG 8판 PDF md5 다름')
    B7, wm7 = blocks(PDF7, RANGE7)
    B8, wm8 = blocks(PDF8, RANGE8)
    by7, by8 = collections.defaultdict(list), collections.defaultdict(list)
    for b in B7:
        by7[b['pdf']].append(b)
    for i, b in enumerate(B8):
        b['i'] = i
        by8[b['pdf']].append(b)
    ref = json.load(io.open(REF, encoding='utf-8'))
    R = {r['id']: r for r in ref['rows']}
    appj = json.load(io.open(APP, encoding='utf-8'))
    app = {z['id']: z for z in appj['지문']}
    pair = {}      # id(7판 덩어리) → 8판 덩어리

    def match8(b7, pdf8):
        for win in (1, 3, 8):     # 표 쪽 ±1 → 닮음 0.8 미만이면 ±3 → ±8(7판 쪽 +10 어림일 때)
            cands = [b for q in range(pdf8 - win, pdf8 + win + 1) for b in by8.get(q, [])] if pdf8 else []
            if not cands:
                continue
            sc = sorted(((sim(b7['body'], b['body']), b['i']) for b in cands), reverse=True)
            if sc[0][0] >= 0.8 or win == 8:
                return B8[sc[0][1]], sc[0][0]
        return None, 0.0

    rows, cnt, diffs = {}, collections.Counter(), []
    del BARE_BAD[:]
    qb7, qsol8 = {}, {}
    base = lambda i: '-'.join(i.split('-')[:2])
    for zid, z in app.items():      # 같은 문항 줄끼리 덩어리를 나눠 쓴다(선지 줄은 쪽이 넘어가 제 쪽에서 못 찾는다)
        if not zid.startswith('P8-'):
            b, h, _ = locate7(z, by7)
            if b is not None and base(zid) not in qb7:
                qb7[base(zid)] = b
    for zid, z in app.items():
        if zid.startswith('P8-'):
            continue
        b7, how, sp = locate7(z, by7)
        if b7 is None and how == u'없음' and base(zid) in qb7:
            b7, how, sp = locate7(z, {int(z.get('pdf쪽') or 0): [qb7[base(zid)]]})
        r = R.get(zid) or {}
        rec = {'how7': how}
        if b7 is None:
            rec['cat'] = u'짝없음' if how != u'해설없음' else u'해설없음'
            rows[zid] = rec; cnt[rec['cat']] += 1
            continue
        k7 = (b7['pdf'], b7['y'])
        if k7 not in pair:
            pair[k7] = match8(b7, int(r.get('pdf8') or 0) or (b7['pdf'] + 10))
        b8, s = pair[k7]
        rec.update({'pdf7': b7['pdf'], 'pdf8': b8 and b8['pdf'], 'sim': round(s, 3)})
        if b8 is None or s < 0.5 or (r.get('문항해설') == u'짝없음' and zid != 'P7-0283'):
            # 8판에 없음 · 연도별 기출에만(해설 없음) — 7판 해설 그대로(지시서 ⑲) · P7-0283 은 본문으로 짝(채팅 「확인」)
            rec['cat'] = u'짝없음'; rows[zid] = rec; cnt[u'짝없음'] += 1
            continue
        sol8 = b8['sol']
        if not sol8:   # 8판에서 [유제]가 됨 — 앞뒤 세 덩어리 중 해설이 가장 닮은 것(채팅 규칙)
            nb = [B8[k] for k in range(max(0, b8['i'] - 3), min(len(B8), b8['i'] + 4)) if B8[k]['sol']]
            if nb:
                bb = max(nb, key=lambda x: sim(b7['sol'], x['sol']))
                sol8, rec['yuje8'] = bb['sol'], True
        if not sol8:
            rec['cat'] = u'짝없음'; rows[zid] = rec; cnt[u'짝없음'] += 1
            continue
        qcat = cat_of(b7['sol'], sol8)      # 문항 해설 갈래(PDF 끼리 · 보고용 · 표와 맞댐)
        if rec.get('yuje8') and ws(b7['sol']) == ws(sol8):
            qcat = u'같음'                   # [유제]가 된 줄 — 8판 본 문항 해설이 7판 해설과 글자 같음(「같은 5 = 그대로」 · 8판이 덧붙였으면 바뀜 = 그 해설로 대신 · 지시서 ⑲)
        rec['qcat'] = qcat
        # 줄의 8판 글 — 통째 · 표지 사이 조각 · 잘린 조각(책 조각 전문)
        f7 = None
        if how == u'통째':
            t8, rec['cut'] = sol8, u'통째'
        elif how in (u'듦', u'닮음'):
            # 앱 줄 꼴(머리+조각 · 조각)대로 두 판에서 똑같이 떼어 PDF 끼리 맞댄다 — 앱 글은 표 칸 순서가 달라 직접 못 맞댄다
            shp = shape(z.get('sol'))
            t8, f7 = piece(sol8, shp), piece(b7['sol'], shp)
            if how == u'듦' and (shp[0] == u'통째' or t8 is None or f7 is None):
                # 앱 조각이 덩어리 한가운데(표지 경계 아님) — 두 판 글을 맞춰 같은 자리를 옮겨 뗀다
                m8 = map_span(b7['sol'], sol8, z.get('sol'))
                if m8:
                    t8, f7, shp = m8, clean(z.get('sol') or ''), (u'맞춤 자리', None)
            if t8 is None or f7 is None:
                t8, f7, rec['cut'] = sol8, b7['sol'], u'통째(꼴 못 뗌)'
            else:
                rec['cut'] = shp[0]
        elif how == u'잘림' and not really_cut(b7['sol'], sp, z.get('sol')):
            # 앱 조각은 온전하다 — 책 조각 뒤에 붙은 조문 상자(「제N조(…)」)·곁상자(「[1] …」)를 7판 원장이 뺀 것 · 같은 자리만 옮겨 뗀다
            how = rec['how7'] = u'듦(뒤 상자 뺌)'
            t8 = map_span(b7['sol'], sol8, z.get('sol')) or sol8
            f7, rec['cut'] = clean(z.get('sol') or ''), u'맞춤 자리'
        elif how == u'조각' and bare_mark(z.get('sol')) and grow(b7['sol'], lab_of(clean(z.get('sol') or ''))):
            # ★ revfix0929 A-1 — 표지만 남은 앱 조각(「③ (X)」·「ㄱ. ㄷ. ㅁ. (O)」) 뒤 책 글이 **다른 표지로 시작하면** 그 글은 다음 선지의 해설이다.
            #   제 조각 = 표지뿐 — 되살리지 않는다(옛 §A-2-5 「공동 해설 전문」 규칙이 16 줄에 다른 선지 해설을 붙였다 · 채팅 검수 9/29).
            #   8판 제 조각이 앱 글과 글자가 다르면 멈춘다(16 줄 모두 옛 sol 이 8판 글자층에 그대로 있다 · 지시서 A-1-2).
            lab = lab_of(clean(z.get('sol') or ''))
            t8, f7 = piece(sol8, (u'조각', lab)), clean(z.get('sol') or '')
            rec['cut'] = u'조각(표지뿐)'
            if t8 is None or ws(t8) != ws(f7):
                BARE_BAD.append((zid, f7, t8))
                t8 = t8 or sol8
        else:
            f = cut8(b7['sol'], sp, sol8)
            t8, rec['cut'] = (f, u'조각') if f else (sol8, u'통째(조각 못 자름)')
            if how == u'잘림':
                rec['truncated'] = True
                f7 = cut8(b7['sol'], sp, b7['sol'])     # 7판 책 조각 전문 — 8판 조각과 맞대 「개정」인지 「잘림 되살림」인지 가른다
        # 줄 갈래 = 지금 앱 sol ↔ 그 줄의 8판 글(7판 _m 사본은 추록 덧씌움이 있어 PDF 글이 앱 글과 다를 수 있다)
        if ws(clean(z.get('sol') or '')) == ws(t8):
            cat = u'같음'                    # 앱 글이 8판 글과 같다(7판 책 글만 달랐다 · P7-0716-5)
        elif how == u'잘림':
            c = cat_of(f7, t8) if f7 else u'바뀜'
            cat = u'잘림' if c == u'같음' else c   # 같음 = 책 조각 전문으로 되살림(§A-2-5 · 「7판 해설」 상자 없음)
        elif qcat == u'같음':
            cat = u'같음'
        elif f7 is not None:
            cat = cat_of(f7, t8)
        else:
            cat = cat_of(clean(z.get('sol') or ''), t8)
        rec['cat'] = cat
        rec['sol8'] = t8 if cat != u'같음' else None
        qsol8[base(zid)] = sol8
        cnt[cat] += 1
        ch = r.get('문항해설')
        if ch and ch != qcat:
            diffs.append((zid, ch, qcat))
        rows[zid] = rec
    # 한 줄이라도 꼴을 못 뗀 문항(표로 된 해설 · P7-1784) — 조각을 믿을 수 없으니 바뀐 줄은 모두 8판 문항 해설 통째
    for q in sorted({base(k) for k, v in rows.items() if v.get('cut') == u'통째(꼴 못 뗌)'}):
        for k, v in rows.items():
            if base(k) == q and v['cat'] in (u'명칭만', u'바뀜') and v.get('cut') != u'통째(꼴 못 뗌)':
                cnt[v['cat']] -= 1
                v['sol8'], v['cut'] = qsol8[q], u'통째(문항 안 다른 줄 꼴 못 뗌)'
                v['cat'] = cat_of(clean(app[k].get('sol') or ''), v['sol8'])
                cnt[v['cat']] += 1
    for k, v in rows.items():      # 얹을 때 원장 sol 이 이 글과 같은지 맞댈 도장(다르면 [6e] 가 멈춘다)
        if v.get('sol8'):
            v['s7md5'] = hashlib.md5((app[k].get('sol') or '').encode('utf-8')).hexdigest()[:8]
    # 새 카드 — 8판 덩어리(본문 닮음) 해설 · [유제] 는 빈칸
    new = {}
    for nz in ref['new']:
        z = app.get(nz['id'])
        cands = [b for q in (nz['pdf8'] - 1, nz['pdf8'], nz['pdf8'] + 1) for b in by8.get(q, [])]
        best = max(cands, key=lambda b: sim(z['t'] if z else '', b['body'])) if cands else None
        new[nz['id']] = {'pdf8': best and best['pdf'], 'sim': round(sim(z['t'] if z else '', best['body']), 3) if best else 0,
                         'sol8': (best['sol'] if best and not nz.get('유제') else ''), '유제': bool(nz.get('유제'))}
    out = {'_about': u'해례 8판 해설 판올림 재료(⚙ jopangi\\_p8sol_build.py · 두 PDF 글자층 · 워터마크 꼴 줄 버림 · 값 없음) — rows = 7판 지문 id → {cat, how7, cut, sol8?} · new = 새 카드 해설',
           'pdf8md5': MD5_8, 'rows': rows, 'new': new,
           '셈': {'7판 덩어리': len(B7), '8판 덩어리': len(B8), '갈래': dict(cnt), '표와 다른 문항해설 갈래': len(diffs)}}
    return out, diffs, (wm7, wm8)


if __name__ == '__main__':
    if '--probe7' in sys.argv:
        probe7()
    else:
        out, diffs, wm = build()
        if BARE_BAD:
            for b in BARE_BAD:
                print('  표지뿐≠8판', b[0], repr(b[1]), repr((b[2] or '')[:60]))
            sys.exit('NG 표지뿐 조각 %d 줄이 8판 제 조각과 다르다 — 멈춤(revfix0929 A-1-2)' % len(BARE_BAD))
        print(json.dumps(out['셈'], ensure_ascii=False), '워터마크 꼴 줄(값 안 남김)', wm)
        for d in diffs:
            print('  표≠', d)
        data = json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True).encode('utf-8')
        if WMX.search(data.decode('utf-8')):
            sys.exit('NG 산출에 워터마크 꼴(@·휴대전화) 글자')
        if '--write' in sys.argv:
            os.makedirs(os.path.dirname(OUT), exist_ok=True)
            old = open(OUT, 'rb').read() if os.path.exists(OUT) else None
            if old != data:
                open(OUT, 'wb').write(data)
            print('[쓰기]', OUT, len(data), 'B · md5', hashlib.md5(data).hexdigest()[:8], '· 바뀜' if old != data else '· 무변')
