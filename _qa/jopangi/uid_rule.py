# -*- coding: utf-8 -*-
r"""jopangi uid 판 — 1차객 지문 uid 새 규칙(_task_jo_gaek_uid · 아티팩트 VA1Zzfp6onPh1oBxfQN38j v10).

  꼴(A-1)
    문번 앎(시험 자리)      법 + 연도2 + 회차2 + 문번2 + 선지(1~5) 또는 보기 글자      T2461185 · T084510ㄱ
    2008 이후 · 글 다름      위 꼴 + h(제7판) / r(리담) · 같은 자리·같은 꼬리 둘째부터 h2·r2
    2007 이전 리담 · 못 찾음  법 + R + 연도2 + 리담 순번2 + 선지·보기 글자                  TR03071 · TR9704가
    2007 이전 제7판 · 2차     TH + 연도2 + P7 번호4 (+ 쪼갠 줄이면 선지)                     TH050004
    사법                     TJ + 연도2 + P7 번호4 (+ 선지)                                  TJ080001
    미기출                   TX + P7 번호4 (+ 선지)                                          TX2058
    객관식 문항째 줄           문항 키 = 법 + 연도2 + 회차2 + 문번2(끝자리 뺀 것) · 못 찾으면 TH/TJ/TX + … + P7 번호4
  조합 선지 줄(「ㄱ, ㄴ」·「1개」)은 uid 없음.
  같은 글(법·정답·정규화 글 같음) = uid 하나 — 남길 차례 문번 앎 > R > H·J·X · 같으면 이른 해(A-5).

  시험지 대조 = 특상디/_uid/exam_text.json(uid_exam.py) · 결과 = 특상디/_uid/exam_match.json(재실행 때 그대로 쓴다 · 멱등).
  판독 덧자료 = 특상디/_uid/exam_fix.json(스캔본 해 그림으로 확인한 글 대조 판정 · 추측 금지 · 사람이 읽은 것만).

  함수 new_uids(rows) → [행마다 {'uid','uid7','how','how7'}] · 원장 쓰기는 uid_apply.py
"""
import io, json, os, re, unicodedata, collections, difflib, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
UDIR = os.path.join(HERE, u'특상디', u'_uid')
EXAM = os.path.join(UDIR, 'exam_text.json')
MATCH = os.path.join(UDIR, 'exam_match.json')
FIX = os.path.join(UDIR, 'exam_fix.json')
READ = os.path.join(UDIR, 'exam_read.json')   # 스캔본 문항을 그림에서 옮겨 적은 판독 글(있으면 OCR 대신)
LAWC = {u'특허': 'T', u'상표': 'S', u'디보': 'D'}
RANGE = {'T': (1, 20), 'S': (21, 30), 'D': (31, 40)}
SCAN = ('2009', '2010', '2020', '2022', '2025')
SYM = {}
for a, b in ((u'㉠㉡㉢㉣㉤㉥㉦', u'ㄱㄴㄷㄹㅁㅂㅅ'), (u'㈀㈁㈂㈃㈄㈅㈆', u'ㄱㄴㄷㄹㅁㅂㅅ'), (u'ㄱㄴㄷㄹㅁㅂㅅ', u'ㄱㄴㄷㄹㅁㅂㅅ'),
             (u'㈎㈏㈐㈑㈒㈓㈔', u'가나다라마바사'), (u'㉮㉯㉰㉱㉲㉳㉴', u'가나다라마바사'), (u'가나다라마바사', u'가나다라마바사')):
    for x, y in zip(a, b):
        SYM[x] = y
CIRCS = u'①②③④⑤⑥⑦⑧⑨⑩' + u''.join(k for k in SYM if k not in u'ㄱㄴㄷㄹㅁㅂㅅ가나다라마바사')
PUN = re.compile(u"[\\s.,·ㆍ‧∙•;:!?'\"‘’“”`´′″‵ᆞ⋅⌜⌟̊(){}\\[\\]<>〈〉《》「」『』【】〔〕\\-‐‑–—―~〜/\\\\|※…・、。＿_=+*＊#]")   # ′″ = 프라임(시험지 「A′」 · 원장 「A'」 · 9/26 판독)


def norm(t):
    """띄어쓰기·문장부호·원문자·해설 꼬리·책 태그를 뺀 글(규칙 ⑲ 「그 밖 한 글자라도 다르면 꼬리」)."""
    t = u'' if t is None else str(t)
    t = re.sub(u'\\[[^\\]]*(변리|사법|유제|미기출|2차)[^\\]]*\\]', u'', t)
    # 제7판 답 표지 「답 I O I」 — 지문은 첫 답 표지 앞까지(원장 124줄은 그 뒤에 다음 항목 머리·조문·둘째 답이 붙어 있다 · 9/26 실측)
    t = re.split(u'답\\s*[IlⅠ|｜]\\s*[OX○×]', t)[0]
    # 제7판 쪽 머리·꼬리(「제3편 특허요건- 111 -」 · 「제6편 PCT 257」 · 「- 361 -」)만 있는 줄 — 원장 39줄에 딸려 들어가 있다(9/26 판독)
    t = u'\n'.join(l for l in t.split(u'\n') if not re.match(u'^\\s*(?:제\\s*\\d+\\s*편[^\\n]{0,24}|-\\s*\\d{1,3}\\s*-|\\d{1,3})\\s*$', l))
    t = re.sub(u'답\\s*[IlⅠ|｜]?\\s*[OX○×]\\s*[IlⅠ|｜]?\\s*$', u'', t.strip())
    # 보기 표지 가~사 는 낱자 목록으로 — 범위 [가-사] 는 「각」「병」 등 음절 수천 개를 덮는다(9/26 COMBO 와 같은 탈)
    t = re.sub(u'^\\s*(?:[①-⑩]|[ㄱ-ㅅ][.．)]|[가나다라마바사][.．)]|\\((?:[ㄱ-ㅅ]|[가나다라마바사])\\))\\s*', u'', t)
    t = u''.join(c for c in t if c not in CIRCS)
    t = PUN.sub(u'', t)   # NFKC 앞에서도 — 「ㆍ」(U+318D)는 NFKC 가 한글 모음 「ᆞ」(U+119E)로 바꿔 뒤 PUN 을 빠져나간다(9/26 판독)
    t = unicodedata.normalize('NFKC', t)
    return PUN.sub(u'', t)


def ratio(a, b):
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


# 조합 선지 글자 = 자음(ㄱ~ㅎ · NFKC 뒤 ᄀ~ᄒ) · ㈎~㈕ 의 가~하 14 낱자. ⚠ 범위 [가-하] 는 한글 음절 거의 전부라
#   「발명의 명칭」「출원공개제도」 같은 짧은 선지 9줄을 조합으로 잘못 걸렀다(9/26 원장 쓰기 뒤 census 로 찾음)
COMBO = re.compile(u'^(?:[ㄱ-ㅎᄀ-ᄒ가나다라마바사아자차카타파하]{1,7}|\\d개|없음|없다|[1-5]개)$')
PLACEHOLDER = frozenset([u'삭제'])   # 리담 「<삭제>」 줄의 정규화 글 — 같은 글 합치기에서 뺀다


def is_combo_text(t):
    """조합 선지 줄 — 글자·쉼표뿐(「ㄱ, ㄴ」·「㈎, ㈏」) 또는 「1개」 꼴."""
    n = norm(t)
    return bool(n) and len(n) <= 8 and bool(COMBO.match(n))


def tag_parse(tag):
    """「24·05·08 변리」 → ('변리', [2024, 2005, 2008]) · 「08 사법」 · 「미기출」 · 빈칸 = ('2차', [])."""
    tag = (tag or u'').strip()
    if not tag:
        return u'2차', []
    if u'미기출' in tag:
        return u'미기출', []
    # 「18 변리 2차」「2013 2차 변형」 = 변리 2차(9/27 add1 §B — 책 글자층에서 읽은 태그) · 해 = 태그의 해(네 자리도)
    kind = u'사법' if u'사법' in tag else (u'2차' if u'2차' in tag else u'변리')
    ys = [int(x) for x in re.findall(r'(?<!\d)(?:19|20)\d{2}(?!\d)', tag)]
    rest = re.sub(r'(?<!\d)(?:19|20)\d{2}(?!\d)', u' ', tag)
    for x in re.findall(r'(?<!\d)\d{2}(?!\d)', rest):
        v = int(x)
        ys.append(2000 + v if v <= 40 else 1900 + v)
    return kind, ys


def yy(y):
    return '%02d' % (int(y) % 100)


def rr(y):
    return '%02d' % (int(y) - 1963)


class Unit(object):
    __slots__ = ('key', 'ident', 'row', 'side', 'law', 'year', 'text', 'n', 'ans', 'label', 'p7', 'k', 'obj', 'q', 'sun', 'mun',
                 'variant', 'old', 'tagkind', 'tagyears', 'pos', 'eq', 'how', 'base', 'uid', 'grade', 'sim', 'note', 'win',
                 'conf')   # conf = ABBYY 글자층 대조가 옛 판독 덧자료와 어긋난 까닭(add1 §C-1 「두 판 차이」)

    def __init__(self, **kw):
        for s in self.__slots__:
            setattr(self, s, kw.get(s))


def units_of(rows):
    """원장 행 → 단위(리담 선지 L · 제7판 줄 P). 합친 행(짝 ID)은 L 과 P 둘."""
    U = []
    for i, r in enumerate(rows):
        src = r[u'소스'] or u''
        if u'|' in src:
            if r[u'형식'] == u'오지선다':
                continue
            f, sun, sel = src.split(u'|')
            law = LAWC.get(r[u'과목'])
            if law is None:
                continue
            if is_combo_text(r[u'문제']):
                continue
            if sel.startswith('b'):
                m = re.search(u'기호=(\\S)', r[u'로그'] or u'')
                lab = SYM.get(m.group(1)) if m else None
                if not lab:
                    lab = u'ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋ'[int(sel[1:]) - 1]   # ★ sp_gichul §C(10/3) — 보기 여덟(2005-42-24 ㄱ~ㅇ · 「ㅇ」 은 SYM 밖) · 일곱까지 무변
            else:
                lab = sel
            mun = int(r[u'문번']) if re.fullmatch(r'\d+', r[u'문번'] or u'') else None
            # ★ uid_add2 §D(9/27) — 기출연도 빈칸(연도 모름 리담 문항) = 0 → ④ 에서 법 + RU + PM 번호
            yr = int(r[u'기출연도']) if re.fullmatch(r'\d{4}', r[u'기출연도'] or u'') else 0
            U.append(Unit(key='L:%d' % i, ident=u'L|' + src, row=i, side='L', law=law, year=yr,
                          text=r[u'문제'], n=norm(r[u'문제']), ans=r[u'정답'], label=lab, q=(law, f, sun), sun=int(sun),
                          mun=mun, variant=(r[u'출처'] == u'기출변형'), old=r['uid']))
        pid = r[u'짝 ID'] or u''
        p7 = src if src.startswith('P7-') else (pid if pid.startswith('P7-') else u'')   # ★ sp_view4 §C(10/3) — 「V4-」 짝(상표 뷰객 책)은 특허 책 단위가 아니다
        if p7:
            m = re.match(u'^(P7-\\d{4})(?:-(\\d|[ㄱ-ㅅ가나다라마바사]))?$', p7)   # mbsame §A-4(9/27) — 조합형은 보기 글자 줄로 쪼갠다
            kind, ys = tag_parse(r[u'태그'])
            t = r[u'본문_7판'] or r[u'문제']
            obj = (r[u'형식'] == u'오지선다') and src.startswith('P7-')
            U.append(Unit(key='P:%d' % i, ident=u'P|' + p7, row=i, side='P', law='T', year=None, text=t, n=norm(t),
                          ans=(r[u'정오_7판'] or r[u'정답']), label=(m.group(2) if m and m.group(2) else None),
                          p7=(m.group(1) if m else p7), k=(m.group(2) if m else None), obj=obj,
                          tagkind=kind, tagyears=ys, old=r['uid']))
    return U


def exam_statements(E, y, law):
    """그 해 그 법 범위의 시험 지문 [(문번, 표지, 정규화 글)] — 조합 선지 줄은 뺀다."""
    out = []
    a, b = RANGE[law]
    Y = E.get(str(y)) or {}
    for n in range(a, b + 1):
        q = Y.get(str(n))
        if not q:
            continue
        for lab, t in (q.get('bogi') or {}).items():
            out.append((n, lab, norm(t)))
        for lab, t in (q.get('opt') or {}).items():
            if not is_combo_text(t):
                out.append((n, str(lab), norm(t)))
    return out


def exam_qtext(q):
    s = norm(q.get('stem'))
    s += u''.join(norm(q['bogi'][k]) for k in sorted(q.get('bogi') or {}))
    s += u''.join(norm(v) for k, v in sorted((q.get('opt') or {}).items()) if not is_combo_text(v))
    return s


def ocr_q(q):
    """스캔본 문항 — OCR 줄을 이은 정규화 글 + 줄마다 [시작, 끝) 자리(판독용 그림 자르기)."""
    s, spans = u'', []
    for i, l in enumerate(q.get('ocr_lines') or []):
        t = l['t']
        if i == 0:
            t = re.sub(u'^\\s*\\d{1,2}\\s*[.．,]', u'', t)
        n = norm(t)
        spans.append((len(s), len(s) + len(n)))
        s += n
    return s, spans


def best_window(Q, s):
    """Q(문항 글) 안에서 s(지문)와 가장 닮은 구간 — difflib 정렬 블록의 가장 큰 덩이 둘레만 모은다.
       돌려주는 것 = (구간 글, 닮음, (시작, 끝))."""
    if not Q or not s:
        return u'', 0.0, (0, 0)
    sm = difflib.SequenceMatcher(None, Q, s, autojunk=False)
    bl = [b for b in sm.get_matching_blocks() if b.size >= 2]
    if not bl:
        return u'', 0.0, (0, 0)
    big = max(bl, key=lambda b: b.size)
    off = big.a - big.b
    m = len(s)
    near = [b for b in bl if abs((b.a - b.b) - off) <= max(12, m // 5)]
    first, last = near[0], near[-1]
    st = max(0, first.a - first.b)
    en = min(len(Q), last.a + last.size + (m - last.b - last.size))
    w = Q[st:en]
    return w, ratio(w, s), (st, en)


def best_of(target, cands):
    """[(key, 글)] 가운데 target 과 가장 닮은 것 · 둘째 닮음."""
    sc = sorted(((ratio(target, c), k) for k, c in cands), key=lambda t: -t[0])
    if not sc:
        return None, 0.0, 0.0
    return sc[0][1], sc[0][0], (sc[1][0] if len(sc) > 1 else 0.0)


def exam_stmt(q, lab):
    return (q.get('bogi') or {}).get(lab) if lab not in (u'1', u'2', u'3', u'4', u'5') else (q.get('opt') or {}).get(lab)


def seg_cands(q):
    """스캔본 문항을 가른 조각([(표지, 정규화 글)]) — 온전할 때만: 보기 표지가 ㄱ·ㄴ·ㄷ…(또는 가·나·다…) 앞에서부터 차례 ·
       선지는 없거나(조합 선지 문항) 1~5 다섯. 아니면 [] (OCR 이 표지를 틀리게 읽은 문항)."""
    bogi, opt = q.get('bogi') or {}, q.get('opt') or {}
    ks = list(bogi.keys())
    okb = (not ks) or any(u''.join(ks) == al[:len(ks)] for al in (u'ㄱㄴㄷㄹㅁㅂㅅ', u'가나다라마바사'))
    oko = (not opt) or sorted(str(k) for k in opt) == ['1', '2', '3', '4', '5']
    if not (okb and oko) or not (bogi or opt):
        return []
    return [(str(k), norm(t)) for k, t in list(bogi.items()) + list(opt.items()) if not is_combo_text(t)]


def win_aligned(q, span):
    """스캔본 구간이 선지·보기 경계에 맞는가(9/26 add1 — P7-1701 「청구범위의 독립항은…」 이 시험지 「특허청구범위의
       독립항은…」 의 꼬리와 정확히 같아 「같음」으로 속았다). 선지·보기 첫 줄 = 걸친 들여쓰기(40~90px 안쪽 줄)보다
       왼쪽에 선 머리 줄. 시작 = 어느 줄 머리(머리 줄이면 첫 글자가 표지 찌꺼기 「丁」「느」 등일 때 그 바로 뒤도) ·
       끝 = 어느 줄 끝이고 다음 줄이 머리 줄이거나 문항 끝. 표지를 통째로 못 읽어 머리 줄이 들여쓰기 자리에 선
       쪽은 맞지 않다고 나온다 → 판독으로(안전한 쪽)."""
    L = q.get('ocr_lines') or []
    if not L:
        return False
    Qn, spans = ocr_q(q)
    xs = [l['box'][0] for l in L]
    head = lambda i: i > 0 and any(40 <= x - xs[i] <= 90 for j, x in enumerate(xs) if j > 0 and j != i)
    st, en = span
    ok_st = False
    for i, (a, b) in enumerate(spans):
        if i == 0:
            continue
        if st == a:
            ok_st = True
            break
        if head(i):
            t = L[i]['t']
            n0 = len(norm(t)) - len(norm(t[1:]))
            if n0 and st == a + n0:
                ok_st = True
                break
    ok_en = False
    for i, (a, b) in enumerate(spans):
        if i == 0 or en != b or a == b:
            continue
        k = i + 1
        while k < len(spans) and spans[k][0] == spans[k][1]:
            k += 1
        if k >= len(spans) or head(k):
            ok_en = True
            break
    return ok_st and ok_en


def is_scan(q):
    """문항 글이 OCR 줄(ocr_lines)로 실렸는가 — Windows OCR(옛) 또는 ABBYY 글자층(9/26 add1 §C · src=abbyy)."""
    return bool(q.get('ocr_lines')) and not q.get('read')


def judge(u, y, q, ex, fix, win=None):
    """글 대조 — 판독 덧자료(fix)가 있으면 그것 · 스캔본은 OCR 구간과 **정확히** 같을 때만 같음(아니면 보류 = 판독 목록)
       · 글자층은 정규화 글이 같으면 같음.
       ABBYY 글자층(src=abbyy)은 **글자층이 먼저**(add1 §C-5 「그림 판독은 글자층이 안 맞는 줄에만」) — 구간이 정확히 같으면 같음 ·
       다르면 판독 덧자료 · 없으면 보류. 옛 판독이 「다름」인데 글자층이 같으면 u.conf 에 적는다(두 판 차이)."""
    fx = fix.get(u.ident) or {}
    scan = is_scan(q)
    if scan:
        w, s1, span = win if win is not None else best_window(ocr_q(q)[0], u.n)
        u.win = (w, round(s1, 3), tuple(span))
    if scan and q.get('src') == 'abbyy':
        if u.win[0] == u.n and win_aligned(q, u.win[2]):
            u.eq, u.note = True, 'abbyy-same'
            if fx.get('eq') == 'diff':
                u.conf = 'fix-diff-but-abbyy-same'
        elif fx.get('eq') in ('same', 'diff'):
            if u.win[0] == u.n and fx['eq'] == 'diff':
                u.conf = 'abbyy-exact-misaligned-fix-diff'   # 구간은 같지만 경계가 어긋남 — 옛 판독 「다름」이 선다
            u.eq, u.note = (fx['eq'] == 'same'), 'fix'
        else:
            u.eq, u.note = None, 'abbyy-check'
        return
    if fx.get('eq') in ('same', 'diff'):
        u.eq, u.note = (fx['eq'] == 'same'), 'fix'
    elif scan:
        u.eq, u.note = (True, 'ocr-same') if u.win[0] == u.n else (None, 'ocr-check')
    elif ex is None:
        u.eq, u.note = None, 'nolabel'
    else:
        u.eq, u.note = (norm(ex) == u.n), 'text'


RULEVER = 'uid-rule-2026-09-27b'   # 대조(찾기·구간) 코드가 바뀌면 올린다 — 캐시가 저절로 무효


def exam_sig():
    """대조 캐시가 유효한 조건 = 시험지 글(exam_text) · 옮겨 적은 글(exam_read) · 규칙 판이 같다(판독 덧자료는 찾기에 안 쓴다)."""
    h = hashlib.md5(RULEVER.encode('utf-8'))
    for p in (EXAM, READ):
        h.update(open(p, 'rb').read() if os.path.exists(p) else b'-')
    return h.hexdigest()


def run(rows, E=None, fix=None, log=print, cache=None):
    """원장 행 → 단위 · 새 uid. 돌려주는 것 = (units, report).
       cache = 지난 실행의 rep['cache'](exam_match.json 'cache') — 단위 입력 글·해·시험지 md5 가 같으면 찾기·구간 결과를 다시 쓴다
       (지시서 A-9 「시험지 대조 결과를 남겨 재실행 때 쓴다」 · 110초 → 몇 초). 새 캐시는 rep['cache'] 로 돌려준다."""
    sig = exam_sig()
    C0 = cache if (cache and cache.get('sig') == sig) else {}
    C1 = {'sig': sig, 'L': {}, 'O': {}, 'P': {}, 'W': {}}

    def cached(kind, key, fn):
        k = hashlib.md5(u'\x1f'.join(json.dumps(x, ensure_ascii=False, sort_keys=True) for x in key).encode('utf-8')).hexdigest()[:20]
        hit = (C0.get(kind) or {}).get(k)
        v = hit['v'] if hit is not None else fn()
        C1[kind][k] = {'v': v}
        return v
    E = E if E is not None else json.load(io.open(EXAM, encoding='utf-8'))
    E = {y: dict(v) for y, v in E.items()}
    read = json.load(io.open(READ, encoding='utf-8')) if os.path.exists(READ) else {}
    for y, qs in read.items():
        if y.startswith('_'):
            continue
        for n, rq in qs.items():
            base = (E.get(y) or {}).get(n) or {}
            if base.get('src') == 'abbyy':
                continue   # ABBYY 글자층이 들어온 문항은 옛 옮겨 적은 글 대신 글자층으로(add1 §C-5) — 옮겨 적은 글은 기록으로만 남는다
            E.setdefault(y, {})[n] = dict(base, stem=rq.get('stem', u''), opt=rq.get('opt') or {}, bogi=rq.get('bogi') or {}, read=True)
    fix = fix if fix is not None else (json.load(io.open(FIX, encoding='utf-8')) if os.path.exists(FIX) else {})
    U = units_of(rows)
    L = [u for u in U if u.side == 'L']
    P = [u for u in U if u.side == 'P']
    rep = collections.OrderedDict()
    Q = lambda y, n: (E.get(str(y)) or {}).get(str(n)) or {}
    qtext = lambda y, q: ocr_q(q)[0] if is_scan(q) else exam_qtext(q)
    abbyy_y = lambda y: any((q or {}).get('src') == 'abbyy' for q in (E.get(str(y)) or {}).values())
    posconf = []   # ABBYY 글자층으로 찾은 자리 ≠ 옛 판독 덧자료 자리(add1 §C-1 「두 판 차이」)
    # ── ① 리담 문항 자리 — 문번 앎 = 그대로 · 모름 = 문항째 닮음(0.8 · 2등과 0.1) · 판독 덧자료가 자리를 주면 그것
    #    ABBYY 해는 글자층으로 먼저 찾고 못 찾을 때만 판독 덧자료 자리(add1 §C-5)
    byq = collections.OrderedDict()
    for u in L:
        byq.setdefault(u.q, []).append(u)
    qpos, notfoundL = {}, []
    for qk, us in byq.items():
        y = us[0].year
        if y < 2008:
            continue
        mun = [u.mun for u in us if u.mun]
        fxp = [fix[u.ident]['pos'] for u in us if (fix.get(u.ident) or {}).get('pos')]
        if mun:
            qpos[qk] = (y, mun[0], 1.0, 1.0, 'known')
            continue
        if fxp and not abbyy_y(y):
            qpos[qk] = (int(fxp[0][0]), int(fxp[0][1]), 1.0, 0.0, 'fix')
            continue
        law = us[0].law
        a, b = RANGE[law]
        Y = E.get(str(y)) or {}
        stem = rows[us[0].row][u'발문']
        tgt = norm(stem) + u''.join(u.n for u in sorted(us, key=lambda u: u.label))
        nostem = not norm(stem) and not any(is_scan(Y.get(str(n)) or {}) for n in range(a, b + 1))

        def _find_q():
            if nostem:
                # 리담 발문이 빈 문항(디보 2023-r8 · 상표 2012-r6) — 시험 쪽도 발문을 빼고 선지·보기끼리 맞댄다
                cands = [(n, exam_qtext(dict(Y[str(n)], stem=u''))) for n in range(a, b + 1) if str(n) in Y]
            else:
                cands = [(n, qtext(y, Y[str(n)])) for n in range(a, b + 1) if str(n) in Y]
            return list(best_of(tgt, cands))
        n, s1, s2 = cached('L', (tgt, y, law, nostem), _find_q)
        if n is not None and s1 >= 0.8 and s1 - s2 >= 0.1:
            qpos[qk] = (y, n, s1, s2, 'found')
            if fxp and (int(fxp[0][0]), int(fxp[0][1])) != (y, n):
                posconf.append((qk, 'L', (int(fxp[0][0]), int(fxp[0][1])), (y, n), round(s1, 3)))
        elif fxp:
            qpos[qk] = (int(fxp[0][0]), int(fxp[0][1]), 1.0, 0.0, 'fix')
        else:
            notfoundL.append((qk, y, n, round(s1, 3), round(s2, 3)))
    # ── ② 리담 선지 → 자리 · 글 대조
    def win_of(u, y, n, q):
        """스캔본 문항 글 안 u 와 가장 닮은 구간 [글, 닮음, [시작, 끝]] — 캐시(W)."""
        if not is_scan(q):
            return None
        return cached('W', (u.n, y, n), lambda: list(best_window(ocr_q(q)[0], u.n)))
    posans, Lat = {}, collections.defaultdict(list)
    for u in L:
        p = qpos.get(u.q)
        if not p:
            continue
        y, n = p[0], p[1]
        q = Q(y, n)
        u.pos, u.sim = (y, n, u.label), p[2]
        judge(u, y, q, exam_stmt(q, u.label), fix, win_of(u, y, n, q))
        Lat[(y, n)].append(u)
        if u.eq:
            posans[u.pos] = u.ans
    # ── ③ 제7판 줄 — 객관식 문항째 · 쪼갠 줄(문항째 자리 + k) · 보통 줄(지문째 닮음 · 스캔본은 문항 글 안 구간)
    objpos = {}
    for u in P:
        if u.tagkind != u'변리' or not u.obj:
            continue
        ys_o = sorted(set(y for y in u.tagyears if y >= 2008))

        def _find_obj():
            best = None
            for y in ys_o:
                Y = E.get(str(y)) or {}
                cands = [(n, qtext(y, Y[str(n)])) for n in range(1, 21) if str(n) in Y]
                n, s1, s2 = best_of(u.n, cands)
                if n is not None and s1 >= 0.8 and s1 - s2 >= 0.1 and (best is None or s1 > best[2] + 1e-9):
                    best = [y, n, s1, s2]
            return best
        best = cached('O', (u.n, ys_o), _find_obj)
        if best:
            objpos[u.p7] = best
            u.pos, u.sim = (best[0], best[1], None), best[2]
    notfoundP = []
    for u in P:
        if u.tagkind != u'변리' or u.obj:
            continue
        ys8 = sorted(set(y for y in u.tagyears if y >= 2008))
        if not ys8:
            continue
        fx = fix.get(u.ident) or {}
        fxpos = (int(fx['pos'][0]), int(fx['pos'][1])) if fx.get('pos') else None
        if u.k:
            op = objpos.get(u.p7)
            if not op:
                continue
            y, n, lab = op[0], op[1], u.k
        elif fxpos and not abbyy_y(fxpos[0]):
            y, n = fxpos
            lab = fx.get('label')
        else:
            def _find_p():
                best = None
                for y in ys8:
                    if any(is_scan(qq or {}) for qq in (E.get(str(y)) or {}).values()):
                        # 스캔본 — 판독 글 문항은 선지째 · 나머지는 OCR 문항 글 안 가장 닮은 구간
                        Y = E.get(str(y)) or {}
                        sc = []
                        for n in range(1, 21):
                            qq = Y.get(str(n))
                            if not qq:
                                continue
                            if qq.get('read'):
                                for lab2, t2 in list((qq.get('bogi') or {}).items()) + list((qq.get('opt') or {}).items()):
                                    if not is_combo_text(t2):
                                        sc.append((ratio(u.n, norm(t2)), (n, str(lab2))))
                            else:
                                sc.append((best_window(ocr_q(qq)[0], u.n)[1], (n, None)))
                        sc.sort(key=lambda t: -t[0])
                        if not sc:
                            continue
                        k, s1, s2 = sc[0][1], sc[0][0], (sc[1][0] if len(sc) > 1 else 0.0)
                    else:
                        cands = [((n, lab), t) for n, lab, t in exam_statements(E, y, 'T')]
                        k, s1, s2 = best_of(u.n, cands)
                    if k is not None and s1 >= 0.8 and s1 - s2 >= 0.1 and (best is None or s1 > best[2] + 1e-9):
                        best = [y, k[0], s1, s2, k[1]]
                return best
            best = cached('P', (u.n, ys8), _find_p)
            if best and fxpos and fxpos != (best[0], best[1]):
                posconf.append((u.ident, 'P', fxpos, (best[0], best[1]), round(best[2], 3)))
            if not best and fxpos:
                # ABBYY 글자층으로 못 찾음 → 옛 판독 덧자료 자리(그림 판독 = 글자층이 안 맞는 줄에만 · add1 §C-5)
                best = (fxpos[0], fxpos[1], 1.0, 0.0, None)
            if not best:
                notfoundP.append(u.ident)
                continue
            y, n, lab = best[0], best[1], best[4]
            u.sim = best[2]
        q = Q(y, n)
        if lab is None and is_scan(q):
            # 스캔본 — 표지는 같은 자리 리담 선지 구간과 겹치는 것(절반 이상)으로
            w, s1, span = win_of(u, y, n, q)
            bestov = (0.0, None)
            for v in Lat.get((y, n), []):
                if not v.win:
                    continue
                a0, a1 = v.win[2]
                ov = max(0, min(a1, span[1]) - max(a0, span[0])) / float(max(1, span[1] - span[0]))
                if ov > bestov[0]:
                    bestov = (ov, v.label)
            if bestov[0] >= 0.5:
                lab = bestov[1]
                if fx.get('label') and fxpos == (y, n) and str(fx['label']) != str(lab):
                    posconf.append((u.ident, 'P-label', (y, n, fx['label']), (y, n, lab), round(bestov[0], 3)))
            elif fx.get('label') and fxpos == (y, n):
                lab = fx['label']   # 겹치는 리담 구간이 없는 줄 — 옛 판독이 준 표지(그림을 보고 적은 것)
            else:
                # 겹치는 리담 구간도 판독 표지도 없는 줄(그 리담 문항을 시험지에서 못 찾음 등) — 문항을 가른 조각이
                #   온전할 때만(보기 표지 ㄱ·ㄴ·ㄷ… 차례 · 선지 1~5) 선지째 맞대기. ABBYY 가 「ㄴ.」을 「느.」로 읽은
                #   2010-13 처럼 조각이 깨졌으면 쓰지 않는다(보류 → 판독).
                cands = seg_cands(q)
                k2, s1b, s2b = best_of(u.n, cands) if cands else (None, 0.0, 0.0)
                if k2 is not None and s1b >= 0.8 and s1b - s2b >= 0.1:
                    lab = k2
        if lab is None:
            u.pos, u.eq, u.note = (y, n, None), None, 'nolabel'
            wv = win_of(u, y, n, q)
            u.win = (wv[0], wv[1], tuple(wv[2])) if wv else None
            continue
        u.pos = (y, n, lab)
        judge(u, y, q, exam_stmt(q, lab), fix, win_of(u, y, n, q))
    # ── ④ 기본 uid
    for u in U:
        if u.side == 'L':
            if u.pos:
                y, n, lab = u.pos
                u.base = LAW_POS(u.law, y, n, lab) + ('' if u.eq else 'r')
                u.grade, u.how = 0, ('pos' if u.eq else ('pos-r' if u.eq is False else 'pending'))
            elif not u.year:
                # ★ uid_add2 §D-1(9/27) — 연도 모름 리담 문항 = 법 + RU + 리담 PM 번호 네 자리 + 선지·보기(예 TRU0506ㄱ · 출제연도 칩 없음)
                m = re.search(r'(\d{4})', u.q[1] or u'')
                u.base = u.law + 'RU' + (m.group(1) if m else '%04d' % u.sun) + u.label
                u.grade, u.how = 1, 'RU'
            else:
                u.base = u.law + 'R' + yy(u.year) + '%02d' % u.sun + u.label
                u.grade, u.how = 1, ('R' if u.year < 2008 else 'R-notfound')
        else:
            num = u.p7[3:]
            lab = u.k or ''
            if u.obj and u.pos:
                y, n = u.pos[0], u.pos[1]
                u.base, u.grade, u.how = 'T' + yy(y) + rr(y) + '%02d' % n, 0, 'obj-pos'
            elif u.pos and u.pos[2] is not None:
                y, n, l2 = u.pos
                bad_ans = (u.pos in posans and posans[u.pos] in ('O', 'X') and u.ans in ('O', 'X') and posans[u.pos] != u.ans)
                tail = '' if (u.eq and not bad_ans) else 'h'
                u.base, u.grade = LAW_POS('T', y, n, l2) + tail, 0
                u.how = ('pos' if not tail else ('pos-h-ans' if (u.eq and bad_ans) else ('pos-h' if u.eq is False else 'pending')))
            elif u.pos:
                u.base, u.grade, u.how = 'T' + yy(u.pos[0]) + rr(u.pos[0]) + '%02d' % u.pos[1] + '?', 0, 'pending-label'
            else:
                kind, ys = u.tagkind, u.tagyears
                if kind == u'사법':
                    u.base, u.how = 'TJ' + yy(min(ys)) + num + lab, 'J'
                elif kind == u'미기출':
                    u.base, u.how = 'TX' + num + lab, 'X'
                elif kind == u'2차':
                    # 2차 해 = 태그의 해(「18 변리 2차」) · 태그가 비면 책 태그 판독 덧자료(year2 · 9/26 P7-0977·1223·1224)
                    y2 = (min(ys) if ys else None) or (fix.get(u.ident) or {}).get('year2') or (fix.get(u'P|' + u.p7) or {}).get('year2')
                    u.base, u.how = 'TH' + (yy(y2) if y2 else '??') + num + lab, 'H-2cha'
                else:
                    u.base, u.how = 'TH' + yy(min(ys)) + num + lab, ('H' if max(ys) < 2008 else 'H-notfound')
                u.grade = 2
    # ── ⑤ 같은 글 = uid 하나(법·정답·정규화 글)
    grp = collections.defaultdict(list)
    for u in U:
        # 자리표시 글(리담 「<삭제>」 = 법이 바뀌어 지운 선지)은 지문 글이 아니다 — 같은 글로 합치지 않는다
        #   (9/26 디보 2006 2번째 ④ 와 2009-32 ② 가 「삭제」 로 한 uid 가 될 뻔했다)
        if u.obj or u.n in PLACEHOLDER:
            continue
        grp[(u.law, u.ans, u.n)].append(u)
    merged = []

    def order(u):
        y = u.pos[0] if u.pos else ((u.year or 9999) if u.side == 'L' else (min(u.tagyears) if u.tagyears else 9999))   # ★ uid_add2 — 연도 모름은 맨 뒤
        return (u.grade, y, 0 if u.side == 'L' else 1, u.base)
    for k, us in grp.items():
        us.sort(key=order)
        keep = us[0].base if k[2] else None
        for u in us:
            u.uid = keep if keep else u.base
        if keep and len(set(u.base for u in us)) > 1:
            merged.append((keep, sorted(set(u.base for u in us) - {keep}), [u.ident for u in us]))
    for u in U:
        if u.obj or u.n in PLACEHOLDER:
            u.uid = u.base
    # ── ⑥ 같은 자리·같은 꼬리 · 글 다름 → 둘째부터 2·3
    by = collections.defaultdict(list)
    for u in U:
        by[u.uid].append(u)
    coll = []
    for uid, us in by.items():
        texts = []
        for u in sorted(us, key=order):
            if u.n not in texts:
                texts.append(u.n)
        if len(texts) > 1:
            for j, t in enumerate(texts[1:], start=2):
                for u in us:
                    if u.n == t:
                        u.uid = (uid + str(j)) if uid[-1:] in ('h', 'r') else (uid + '~' + str(j))
                coll.append((uid, j, [u.ident for u in us if u.n == t]))
    rep['notfoundL'] = notfoundL
    rep['notfoundP'] = notfoundP
    rep['merged'] = merged
    rep['coll'] = coll
    rep['posans'] = len(posans)
    rep['pending'] = [u.ident for u in U if u.how in ('pending', 'pending-label')]
    rep['posconf'] = posconf
    rep['conf'] = [(u.ident, u.conf) for u in U if u.conf]
    rep['cache'] = C1
    return U, rep


def verify_ledger(rows):
    """⚙ 파이프라인 관문(ledger_build) — 규칙이 짓는 uid(대조 캐시 exam_match.json 'cache' 로 빠르게) = 원장 uid·uid7 인가.
       돌려주는 것 = (어긋난 행 [(소스, 원장 (uid, uid7), 규칙 (uid, uid7))], 캐시 적중 여부). 어긋나면 uid_apply.py --write 로 다시 짓는다."""
    try:
        cache = json.load(io.open(MATCH, encoding='utf-8')).get('cache')
    except Exception:
        cache = None
    hit = bool(cache) and cache.get('sig') == exam_sig()
    U, rep = run(rows, cache=cache, log=lambda *a: None)
    by = collections.defaultdict(dict)
    for u in U:
        by[u.row][u.side] = u
    bad = []
    for i, r in enumerate(rows):
        L, P = by[i].get('L'), by[i].get('P')
        if u'|' in (r[u'소스'] or u''):
            want = ((L.uid if L else u''), (P.uid if (P and L and P.uid != L.uid) else u''))
            if (r.get(u'짝 ID') or u'').startswith(('V4-', 'V5-')):   # ★ sp_view4 §C(10/3) — 상표 뷰객 짝 행 uid7(책 쪽 SV uid)은 view4_build 관문 V4U 가 잰다 · ★ sp_view5 §C(10/3) 「V5-」 도
                want = (want[0], r.get('uid7') or u'')
        else:
            want = ((P.uid if P else (r['uid'] or u'')), u'')
        have = ((r['uid'] or u''), (r.get('uid7') or u''))
        if want != have:
            bad.append((r[u'소스'], have, want))
    return bad, hit


def LAW_POS(law, y, n, lab):
    return law + yy(y) + rr(y) + '%02d' % int(n) + str(lab)
