# -*- coding: utf-8 -*-
r"""1차객 지문 조 연결 — ⚙ 마지막 단계 (2026-09-27 · _task_jo_joscreen + add1 §A).

지문 `jo` = 아래 차례로 처음 걸린 것.
  ① 리담 선지 연결 — 리담 조별 「정오문제」 행(예상문제 뺌)을 우리 지문에 짝짓는다.
       리담 문항 → 우리 문항: 같은 연도 · 발문 글자 닮음 최고 · 0.6 이상.
       리담 행 → 우리 지문: 짝 문항 안 선지 글 닮음 최고 0.6 이상 · 모자라면 같은 해 전체 · 그래도 없으면 「못 짝지음」.
       조 = 이어진 pathSlug 들(「42의2」 → 특-42의2) · 항 자세함은 ② 를 거친 해설 코드에서(조가 같은 것) 그대로.
  ② 해설 뽑기(다른 법 뺌) — 지금 조 코드(원장 `조문` 열) 가운데 해설이 다른 법의 그 조라고 적은 것을 뺀 나머지.
       「제N조」 앞(같은 어절 · 괄호 하나 건너)의 이름이 특허법 시행령·시행규칙 · 실용신안법 시행령 · 상표법 시행령 ·
       헌법 · 형법 · 민법 · … · WTO 이면 다른 법(복합 이름 먼저). 같은 해설에 「<이 법> 제N조」 나 「法N」 가 있으면 남긴다.
       앱 코드 꼴이 아닌 것(`제46조` · 특허 쪽 `상-92` …)은 다른 법에서 온 것 → 뺀다.
  ③ 리담이 같은 문항 안에서 다른 선지만 이었으면 → 없음(리담이 일부러 안 단 선지 · 대표 조로 안 채운다).
  ④ 리담 문항 대표 조 `primaryArticleNumber`(특허만 — 상표·디보는 자료가 없다).
  ⑤ 없음.
사용자 손값(앱 「이 조 아님 ×」 · 기록 키 jopangi.jonot)은 앱이 이 위에 얹는다 — ⚙ 를 다시 돌려도 이긴다.

★ ② 의 판정 `other_law()` 는 앱 `joOtherLaw()`(jo/index.html · 제7판 해설 `p7Jo` 가 쓴다)와 같은 규칙이다(㊜).
  둘 중 하나를 고치면 다른 쪽도 고친다 — 하네스 `_harness_jo_joscreen.py` 관문 8-R 이 둘을 같은 해설로 맞댄다.
★ 입력 = 특상디\_data\lidam_ox_by_article_<patent|trademark>*.json(meta.collectedAt 가장 새것) ·
  lidam_problems_<patent|trademark>*.json(가장 새 파일 — 목록 파일이라 collectedAt 이 없어 파일 시각).
"""
import os, re, json, glob, difflib, collections

LAWS = {u'특허': ('patent', u'특', u'특허법'), u'상표': ('trademark', u'상', u'상표법')}

# ── ② 다른 법 이름(복합 이름 먼저 · 이 법 이름은 맨 끝 — 이 법이면 「다른 법」이 아니다)
OTH = (u'(특허법\\s*시행령|특허법\\s*시행규칙|실용신안법\\s*시행령|상표법\\s*시행령|헌법|형법|민법|민사소송법|형사소송법|'
       u'행정소송법|시행령|시행규칙|규칙|조약|협약|협정|PCT|TRIPs|TRIPS|파리|상표법|디자인보호법|실용신안법|저작권법|'
       u'부정경쟁방지법|발명진흥법|행정심판법|WTO|民法|實用|令|특허법)')
# 행정심판법 = 앱 옛 JO_OTHER 에 있던 이름(제7판 P7-0903 · 빼면 되살아난다) ·
# 民法(민법 · 리담 1992-29-3 해설 「民法 제777조」) · 令(시행령 · 제7판 「令 제N조」) · 實用(실용신안법) = 목록에 있는 법의 한자 꼴
# 「<이름> 제N조」 꼴 가운데 목록 밖 이름을 세는 잣대(보고만)
NAME_RX = re.compile(u'([가-힣A-Za-z·]{1,14}(?:법|령|규칙|조약|협약|협정))\\s*(?:\\([^)]*\\)\\s*)?제\\s*(\\d+)\\s*조(?:\\s*의\\s*(\\d+))?')


def jo_num(code, pfx):
    """'특-42의2-1' → '42의2' · 다른 꼴('제45조' · '상-92' 가 특허에)은 None"""
    c = str(code or '')
    if not c.startswith(pfx + u'-'):
        return None
    n = c.split(u'-')[1]
    return n if re.fullmatch(u'[0-9]+(?:의[0-9]+)?', n) else None


def _pat(n):
    """조 번호 꼴 — 「42」 는 「제42조의2」 를 안 잡고(의 가드), 「42의2」 는 「…의21」 을 안 잡는다.
    ⚠ 앞자리 숫자 가드는 lookbehind 대신 이름 뒤 글자 칸에서 숫자를 빼는 것으로 한다(앱 JS 와 같은 식 · 옛 사파리)."""
    m = re.match(u'([0-9]+)(?:의([0-9]+))?$', n)
    if m.group(2):
        return m.group(1) + u'\\s*조\\s*의\\s*' + m.group(2) + u'(?![0-9])'
    return m.group(1) + u'\\s*조(?!\\s*의\\s*[0-9])'


def _han(n):
    m = re.match(u'([0-9]+)(?:의([0-9]+))?$', n)
    if m.group(2):
        return u'法\\s*' + m.group(1) + u'\\s*(?:조)?\\s*의\\s*' + m.group(2) + u'(?![0-9])'
    return u'法\\s*' + m.group(1) + u'(?![0-9])(?!\\s*(?:조)?\\s*의\\s*[0-9])'


def prep(sol):
    """PDF 줄바꿈이 낱말을 끊은 자리(「협⏎정 제1조」 — 제7판 P7-0024)는 이어 붙여 본다 · 한글과 한글 사이 줄바꿈만."""
    return re.sub(u'([가-힣])[ \\t]*\\n[ \\t]*(?=[가-힣])', u'\\1', str(sol or ''))


def other_law(n, sol, self_law):
    """해설 sol 이 조 n(「42의2」 꼴)을 다른 법의 조라고 적었는가(그리고 이 법 조라는 표기는 없는가).
    = 앱 joOtherLaw(sol, n, selfLaw) 와 같은 규칙."""
    s = prep(sol)
    pat = _pat(n)
    other = False
    for h in re.finditer(OTH + u'[^\\s.,0-9]{0,6}\\s*(?:\\([^)]*\\)\\s*)?제?\\s*' + pat, s):
        if h.group(1) != self_law:
            other = True
            break
    if not other:
        return False
    if re.search(self_law + u'\\s*제?\\s*' + pat, s):
        return False
    if re.search(_han(n), s):
        return False
    return True


def jo_key(n):
    """'42의2' → '제42조의2' (앱 조 목록 열쇠)"""
    return u'제' + n.replace(u'의', u'조의') if u'의' in n else u'제' + n + u'조'


def keep_code(code, sol, pfx, self_law, keys=None):
    n = jo_num(code, pfx)
    if n is None:
        return False
    if keys is not None and jo_key(n) not in keys:
        return False            # 지금 조 목록에 없는 번호 = 딴 법이거나 삭제 조(앱 p7Jo 의 JOKEY 가드와 같은 규칙)
    return not other_law(n, sol, self_law)


def load_keys(law):
    """⚙ 가 먼저 만든 조 목록(jo_<법>_목록.json · 같은 컴파일의 OUT) — 없으면 None(가드 없이)"""
    try:
        import stage_jo as ST
        p = os.path.join(ST.out_root(), 'data', u'jo_%s_목록.json' % LAWS[law][2])
        return set(x['k'] for x in json.load(open(p, encoding='utf-8'))[u'조'])
    except Exception:
        return None


def _norm(s):
    return re.sub(u'[\\s\\W_]+', u'', s or u'')


def _sim(a, b):
    a, b = _norm(a), _norm(b)
    return difflib.SequenceMatcher(None, a, b).ratio() if a and b else 0


def _slug_key(s):
    return [int(x) for x in re.findall(u'\\d+', s)]


def _pick(files, key):
    files = [f for f in files if os.path.isfile(f)]
    if not files:
        return None
    return sorted(files, key=key)[-1]


def _ox_key(f):
    try:
        return (str(json.load(open(f, encoding='utf-8')).get('meta', {}).get('collectedAt') or ''), os.path.getmtime(f))
    except Exception:
        return ('', 0)


def load_lidam(J, law):
    slug = LAWS[law][0]
    d = os.path.join(J, u'특상디', u'_data')
    fox = _pick(glob.glob(os.path.join(d, u'lidam_ox_by_article_%s*.json' % slug)), _ox_key)
    fpr = _pick(glob.glob(os.path.join(d, u'lidam_problems_%s*.json' % slug)), os.path.getmtime)
    rows, meta, probs = [], {}, {}
    if fox:
        X = json.load(open(fox, encoding='utf-8'))
        meta = X.get('meta', {})
        rows = [r for r in X.get('rows', []) if r.get('origin') != 'expected']
    if fpr:
        for p in json.load(open(fpr, encoding='utf-8')):
            if p.get('origin') == 'expected' or p.get('examRound', 'first') != 'first':
                continue
            probs[p['problemId']] = p
    return {'rows': rows, 'meta': meta, 'probs': probs, 'fox': fox, 'fpr': fpr}


def apply(J, law, qs, keys=None):
    """qs = jimun_<법>.json 의 문제 배열(차례 = 연도·문번). 지문 jo 를 제자리에서 바꾼다. 통계·목록을 돌려준다.
    keys = 앱 조 목록 열쇠 집합(없으면 같은 컴파일 OUT 의 jo_<법>_목록.json)."""
    slug, pfx, self_law = LAWS[law]
    if keys is None:
        keys = load_keys(law)
    L = load_lidam(J, law)
    ROWS, PR = L['rows'], L['probs']
    byYear = collections.defaultdict(list)
    yk = lambda v: '?' if v in (None, '', 'None', 0) else str(v)   # ★ uid_add2 §D(9/27) — 연도 모름끼리(우리 '' ↔ 리담 null)
    for q in qs:
        byYear[yk(q.get(u'연도'))].append(q)
    # ① 리담 문항 → 우리 문항
    pq = {}
    for pid, p in PR.items():
        best = (0, None)
        for q in byYear.get(yk(p.get('year')), []):
            s = _sim(p.get('bodyMd'), q.get(u'발문'))
            if s > best[0]:
                best = (s, q)
        if best[0] >= 0.6:
            pq[pid] = best[1]
    pid_of_q = collections.defaultdict(list)
    for pid, q in pq.items():
        pid_of_q[q['id']].append(pid)
    # ① 리담 행 → 우리 지문
    link = collections.defaultdict(set)
    qlinked = set()
    unmatched, matched = [], []
    for r in ROWS:
        q0 = pq.get(r.get('problemId'))
        best = (0, None, None)
        if q0 is not None:
            for z in q0.get(u'지문', []):
                s = _sim(r.get('bodyMd'), z.get('t'))
                if s > best[0]:
                    best = (s, q0, z)
        if best[0] < 0.6:
            best = (0, None, None)
            for q in byYear.get(yk(r.get('year')), []):
                for z in q.get(u'지문', []):
                    s = _sim(r.get('bodyMd'), z.get('t'))
                    if s > best[0]:
                        best = (s, q, z)
        if best[0] < 0.6:
            unmatched.append(r)
            continue
        link[(best[1]['id'], best[2]['n'])].add(str(r['pathSlug']))
        matched.append((r, best[1]['id'], best[2]['n']))
        if q0 is not None and q0['id'] == best[1]['id']:
            qlinked.add(q0['id'])
    ST = collections.OrderedDict((k, 0) for k in (u'①', u'②', u'③', u'④', u'없음'))
    dropped, emptied3, changed, src = [], [], 0, {}
    for q in qs:
        allj = set()
        for z in q.get(u'지문', []):
            old = list(z.get('jo') or [])
            sol = z.get('sol') or u''
            sol2 = [c for c in old if keep_code(c, sol, pfx, self_law, keys)]
            for c in old:
                if c not in sol2:
                    dropped.append((q, z, c))
            key = (q['id'], z['n'])
            if key in link:
                slugs = link[key]
                keep = [c for c in sol2 if jo_num(c, pfx) in slugs]
                have = set(jo_num(c, pfx) for c in keep)
                new = keep + [pfx + u'-' + s for s in sorted(slugs, key=_slug_key) if s not in have]
                st = u'①'
            elif sol2:
                new = sol2
                st = u'②'
            elif q['id'] in qlinked:
                new = []
                st = u'③'
                emptied3.append((q, z))
            else:
                prim = sorted(set(str(PR[p]['primaryArticleNumber']) for p in pid_of_q.get(q['id'], [])
                                  if PR[p].get('primaryArticleNumber')), key=_slug_key)
                new = [pfx + u'-' + s for s in prim]
                st = u'④' if prim else u'없음'
            ST[st] += 1
            src[key] = st
            if new != old:
                changed += 1
            z['jo'] = new
            allj.update(new)
        q[u'조'] = sorted(allj)          # 문항 조 = 지문 조의 합(원장 빌드와 같은 뜻) · 갈래는 원장 뜻 그대로 둔다
    # 짝지은 리담 행의 조가 그 지문 조에 다 있나(관문)
    zby = {}
    for q in qs:
        for z in q.get(u'지문', []):
            zby[(q['id'], z['n'])] = z
    miss = [(r, qid, n) for (r, qid, n) in matched
            if pfx + u'-' + str(r['pathSlug']) not in set(pfx + u'-' + str(jo_num(c, pfx)) for c in zby[(qid, n)]['jo'])]
    # 목록 밖 법 이름(보고) · 그 이름의 조 번호가 지문 조에 남은 것(사용자가 「이 조 아님 ×」로 지울 후보)
    names, flagged = collections.Counter(), []
    for q in qs:
        for z in q.get(u'지문', []):
            for m in NAME_RX.finditer(prep(z.get('sol'))):
                nm = m.group(1)
                if re.search(OTH, nm):
                    continue
                names[nm] += 1
                n = m.group(2) + (u'의' + m.group(3) if m.group(3) else u'')
                f = (q, z, nm, n, src.get((q['id'], z['n'])))
                if any(jo_num(c, pfx) == n for c in z['jo']) and not any(
                        g[0] is q and g[1] is z and g[2:4] == f[2:4] for g in flagged):
                    flagged.append(f)
    return {'stat': ST, 'changed': changed, 'rows': len(ROWS), 'unmatched': unmatched, 'matched': len(matched),
            'pq': len(pq), 'probs': len(PR), 'dropped': dropped, 'emptied3': emptied3, 'miss': miss,
            'names': names, 'flagged': flagged, 'src': src, 'keys': keys is not None,
            'fox': L['fox'], 'fpr': L['fpr'], 'collectedAt': L['meta'].get('collectedAt')}


def report(J, law, res):
    """특상디\\_report\\_조연결_<법>.md — ⚙ 가 실행마다 다시 쓴다."""
    out = os.path.join(J, u'특상디', u'_report', u'_조연결_%s.md' % law)
    L = []
    st = res['stat']
    L.append(u'# 1차객 지문 조 연결 — %s (⚙ jo_link · 실행마다 다시 씀)\n' % law)
    L.append(u'- 입력 = `%s`(collectedAt %s) · `%s`' % (os.path.basename(res['fox'] or u'—'), res['collectedAt'] or u'—',
                                                         os.path.basename(res['fpr'] or u'—')))
    L.append(u'- 리담 행(예상 뺌) %d · 짝지음 %d · 못 짝지음 %d · 리담 문항 짝 %d / %d' % (
        res['rows'], res['matched'], len(res['unmatched']), res['pq'], res['probs']))
    L.append(u'- 갈래 — ① 리담 선지 %d · ② 해설(다른 법 뺌) %d · ③ 리담이 같은 문항 다른 선지만 → 없음 %d · ④ 리담 문항 대표 조 %d · 없음 %d · 바뀐 지문 %d' % (
        st[u'①'], st[u'②'], st[u'③'], st[u'④'], st[u'없음'], res['changed']))
    L.append(u'- 해설 코드에서 뺀 것(다른 법 · 앱 꼴 아님) %d · 짝지은 리담 행인데 지문 조에 그 조가 없는 것 %d\n' % (
        len(res['dropped']), len(res['miss'])))
    L.append(u'## 못 짝지음(연도 · 문번 · 조 · 선지 앞 40자)\n')
    for r in res['unmatched']:
        L.append(u'- %s · %s · 제%s조 · %s' % (r.get('year'), r.get('problemNumber'), r.get('pathSlug'),
                                               re.sub(u'\\s+', u' ', r.get('bodyMd') or u'')[:40]))
    L.append(u'\n## ③ 으로 비운 지문(리담 「연도-회-번 · 선지 · uid」)\n')
    for q, z in res['emptied3']:
        L.append(u'- %s-%s-%s · %s · %s' % (q.get(u'연도'), q.get(u'회차'), q.get(u'시험문번') or q.get(u'문번'),
                                          z.get(u'기호') or z.get('n'), z.get('uid') or u'—'))
    L.append(u'\n## 해설 코드에서 뺀 것(리담 「연도-회-번 · 선지 · uid · 코드」)\n')
    for q, z, c in res['dropped']:
        L.append(u'- %s-%s-%s · %s · %s · `%s`' % (q.get(u'연도'), q.get(u'회차'), q.get(u'시험문번') or q.get(u'문번'),
                                                 z.get(u'기호') or z.get('n'), z.get('uid') or u'—', c))
    L.append(u'\n## 목록 밖 법 이름(해설 「<이름> 제N조」 · 보고만)\n')
    for nm, k in res['names'].most_common():
        L.append(u'- %s × %d' % (nm, k))
    L.append(u'\n### 그 이름의 조 번호가 지문 조에 남은 것(리담 「연도-회-번 · 선지 · uid · 이름 제N조 · 갈래」 · 앱 「이 조 아님 ×」 후보)\n')
    for q, z, nm, n, st in res['flagged']:
        L.append(u'- %s-%s-%s · %s · %s · %s 제%s조 · %s' % (q.get(u'연도'), q.get(u'회차'), q.get(u'시험문번') or q.get(u'문번'),
                                                         z.get(u'기호') or z.get('n'), z.get('uid') or u'—', nm, n, st))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(u'\n'.join(L) + u'\n')
    return out
