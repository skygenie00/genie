# -*- coding: utf-8 -*-
"""_task_jo_book8 §A-3 — 1차객 지문 → 해례 8판 자리 대응표(비공개 minbeoppdf/words/patent_hr8/대응.json)

  입력 = minbeoppdf/words/patent_hr8/ 쪽 글자층(낱글자 · 0~2000 · 워터마크 꼴 줄 뺀 것 · _book_words_build.py 산출)
       + jo/data jimun_7pan.json(p8up 뒤 · 판8_리담 표) · jimun_특허.json(리담 문항 · 34 의 글)
  ⚠ 8판 PDF 는 열지 않는다 — 구운 글자층만 읽는다. 대응표에는 책 글을 넣지 않는다(쪽 · 자리 · 점수 · 갈래만).
  대상 = 원장 지문 전부(p8up 뒤 2,538 · 7판과 병합된 리담 지문은 같은 uid 라 여기 든다) + 판8_리담 34(리담 카드 · 문항 통째 2026-63-2 = uid 다섯)
  찾기 = 문장(첫 「답 I x I」 앞 · 원장 36 줄은 답 뒤에 딴 글이 붙어 있다) → 앱 p7Text · 출처 태그 뺌 → 빈칸·기호 빼고 · 「지식재산처」 ↔ 「특허청」 같게 맞대어
         ① 글 = 그대로 통째 · ② 명칭 = 이름만 맞춰 통째 · ③ 조각 = 앞·가운데·뒤 닻 → 둘레 창 닮음(0.6 이상)
         보기 줄(P7-xxxx-ㄱ · -1 꼴 · 글 짧음) = 후보 가운데 그 문항 발문(사례) 바로 뒤 자리를 앞세운다(짧은 글이 딴 자리에 걸리지 않게)
  후보 = 넷까지 · 점수 s(0~1) · 줄 = {p(PDF 쪽), r:[x0,y0,x1,y1](0~2000 · 위 기준), s, how('글'·'명칭'·'조각')}
  차례 = 본문(pdf ~606) 후보 먼저(0.8 이상) — 8판은 모아보기(607~649)·연도별 기출(650~789)·모의고사(791~)가 본문 글을 되풀이한다
  확신(첫 줄 c) = 첫 줄과 같은 묶음(본문/뒤) 후보끼리: 높음(s ≥ 0.95 · 1·2등 차 ≥ 0.15 또는 2등 없음) · 중간(s ≥ 0.8 · 차 ≥ 0.05) · 낮음(그 밖)

    python _book8_map.py [--data <jo/data>] [--words <words/patent_hr8>] [--out <대응.json>] [--ref <_ref_book8_pos.json>] [--dry]
    python _book8_map.py --book tm_view5 --law 상표 [--data <jo/data>] [--words <words/tm_view5>] [--out <대응.json>] [--dry]

  책 갈래(_task_jo_sp_book5 §A-3 · 10/3) — 인자 없음 = 특허 해례 8판(위 그대로 · 산출 바이트 무변) · tm_view5 = 상표법 뷰객 5판(main_tm)
    대상 = jimun_상표_뷰객.json 책 줄(지문 + 객관식 칸 문항째 줄 · 판5 「없음」 11 뺌) + jimun_상표.json 리담 선지 가운데 뷰객 짝(뷰객 줄 리담 칸)의 uid 가 다른 것
    찾기 · 후보 넷 · 점수 · 확신 = 위 search · best4 그대로 · 뷰객 5판에서 달리 한 것:
      맞댐 글자 = 원문자 뺌(ABBYY 가 ①~⑤ 를 「@」로도 읽음) · 甲乙丙丁 둠 · 양쪽(지문 글 · 책 글자층)에 fold = sp_view4 SUB_GAP 甲乙丙 오독 표 + 「Z」+토씨 → 乙
      첫 짐작 쪽 = 그 줄 5판 pdf쪽(·다음 쪽) — 거기 0.8 이상 후보가 있으면 점수보다 앞(차례 = 발문 바로 뒤 → 짐작 쪽 → 점수) · 없으면 책 전체 · 책 전체에도 그 쪽에도 없으면 그 쪽 창 닮음(닻 없이)
      묶음 = 해설 안/밖(책 글자층 「해설」 머리(왼쪽 끝 x<300)~「정답」 · 「#」 문항 머리) — 해설 속 되풀이는 8판 뒤 묶음처럼 뒤로(1·2등 차는 같은 묶음끼리)
      보기 줄 · 선지의 「발문 바로 뒤」 = 발문 끝 뒤부터(짧은 선지가 발문 속 같은 낱말에 걸리지 않게)
      표 보기 줄 = census 이름표(상품1: · 상품2: · 결과: · 특이사항:)와 그림 자리표([도형] · (도안 글자))를 빼고 맞댐(sp_view4 보기 줄 꼴)
      같은 uid 줄 여럿(배지 OX ↔ 객관식 선지) = 1등 · 확신은 지문 차례 첫 줄(book8 그대로) · 둘째 줄부터 그 줄 1등 자리를 2등 후보로(같은 지문이라 1·2등 차에서는 뺌)
      리담 짝(uid 다름) = 리담 글로 찾기(book8 판8_리담 그대로) + 짝 줄 1등 자리도 후보(점수 = 리담 글이 그 자리 글에 담긴 몫) · 짐작 쪽 = 짝 첫 줄 pdf쪽
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import collections, difflib, glob, gzip, io, json, os, re, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


BOOK = ARG('--book', 'patent_hr8')   # sp_book5 §A-3(10/3) — 책 갈래 · 인자 없음 = 특허 해례 8판(옛 산출 바이트 무변)
BK = {'patent_hr8': {'law': '특허', 'end': 606, 'keep': r'[가-힣A-Za-z0-9ㄱ-ㅎ①-⑳]', 'tm': False},
      'tm_view5': {'law': '상표', 'end': 549, 'keep': r'[가-힣A-Za-z0-9ㄱ-ㅎ甲乙丙丁]', 'tm': True}}[BOOK]   # end = 본문 끝 pdf쪽 · keep = 맞댐 글자 · tm = 뷰객 5판 갈래(fold · 해설 묶음 · 짐작 쪽 먼저)
if ARG('--law', BK['law']) != BK['law']:
    sys.exit('--law %s 는 책 %s(%s)와 안 맞음' % (ARG('--law'), BOOK, BK['law']))
DATA = ARG('--data', _roots.genie(r'jo\data'))
WORDS = ARG('--words', _roots.mbpdf('words', BOOK))
OUT = ARG('--out', os.path.join(WORDS, '대응.json'))
REF = ARG('--ref', os.path.join(HERE, 'task', '_ref_book8_pos.json') if BOOK == 'patent_hr8' else '')
DOCID = BOOK
KEEP = re.compile(BK['keep'])
FOLD = {'己': '乙', '石': '乙', '江': '乙', '乞': '乙', '內': '丙'}   # sp_view4 sp4_10_merge SUB_GAP(甲乙丙 오독) 그대로 — 5판 글자층 실측 乙 0 · 己 127 · 石 74 · 江 39 · 內 52 · 丙 0
JOSA = set('은는이가을를의에와과도만로')   # sp4 PART_ONE + 으로·에게·에서 첫 글자


def fold(s):   # 상표 — 지문 글 · 책 글자층 양쪽에 같게 · 글자 수 그대로 · 글자층엔 빈칸이 없어 SUB_GAP 앞뒤 조건 대신 표만 · 「Z」+토씨(앞이 라틴 글자 아님) = 乙(5판 글자층 「Z의」 꼴 실측)
    return ''.join(FOLD.get(c) or ('乙' if c == 'Z' and s[i + 1:i + 2] in JOSA and not (i and s[i - 1].isascii() and s[i - 1].isalpha()) else c)
                   for i, c in enumerate(s))
ASC, DESC, CW = 19, 6, 24   # 자리 상자 — 밑줄(origin y) 위 19 · 아래 6 · 끝 글자 폭 24(0~2000 눈금 · 10pt 본문 실측 어림)


def p7text(t):   # 앱 p7Text 그대로
    x = re.sub(r'\[\s*\d{2}(?:[\s·,]+\d{2})*\s*변리\s*\]', '', t or '')
    x = re.sub(r'(^|\n)[ \t]*답[ \t]*[I|][^\n]*', '', x)
    x = re.sub(r'(^|\n)[ \t]*제\d+편[ \t]+[^\n]*$', '', x)
    return re.sub(r'[ \t]{2,}', ' ', re.sub(r'\s*\n\s*', ' ', x)).strip()


TAGRX = re.compile(r'\[\s*\d{2}(?:[\s·,]+\d{2})*\s*[가-힣 ]{1,6}\]|\[\s*미기출\s*\]|\[\s*\d{2}(?:[\s·,]+\d{2})*\s*[가-힣]{1,4}')


def stmt(t):   # 문장 = 첫 「답 I x I」 앞까지(원장 36 줄은 답 뒤에 장 제목·조문 본문이 붙어 있다 — 그건 책의 다른 자리 글)
    return re.split(r'\n?[ \t]*답[ \t]*[I|]', t or '', maxsplit=1)[0]


def strip_tags(t):   # 출처 태그 [21 변리] · [미기출] · [16 사법](닫는 괄호 빠진 것도)만 뺀다 — 책에서는 태그가 줄 끝에 따로 선다 · 본문 [별표 1] 따위는 둔다
    return TAGRX.sub('', t)


def norm(s, name=True):
    s = ''.join(ch for ch in (fold(s) if BK['tm'] else s) if KEEP.match(ch))
    return s.replace('지식재산처', '특허청') if name else s


def load_pages():
    pages = {}
    for f in glob.glob(os.path.join(WORDS, 'ox_book_%s_p*.json.gz' % DOCID)):
        o = json.loads(gzip.decompress(open(f, 'rb').read()).decode('utf-8'))
        rows = [l.split('\t') for l in o['words'].split('\n') if l]
        if BK['tm']:   # 상표 — 甲乙丙 오독 접기(지문 글과 같은 fold · 낱글자 차례 그대로)
            rows = [[c] + r[1:] for c, r in zip(fold(''.join(r[0] for r in rows)), rows)]
        ch = [(r[0], int(r[1]), int(r[2])) for r in rows if KEEP.match(r[0])]
        raw = ''.join(c for c, _, _ in ch)
        # 명칭 맞춤 흐름 — 「지식재산처」 다섯 글자를 「특허청」 셋으로(자리 = 1·3·5 째 글자)
        mc, i = [], 0
        while i < len(ch):
            if raw.startswith('지식재산처', i):
                mc += [('특', ch[i][1], ch[i][2]), ('허', ch[i + 2][1], ch[i + 2][2]), ('청', ch[i + 4][1], ch[i + 4][2])]; i += 5
            else:
                mc.append(ch[i]); i += 1
        pages[o['page']] = {'raw': raw, 'rc': ch, 'm': ''.join(c for c, _, _ in mc), 'mc': mc}
    return pages


def rect(cs):
    xs, ys = [c[1] for c in cs], [c[2] for c in cs]
    return [max(0, min(xs)), max(0, min(ys) - ASC), min(2000, max(xs) + CW), min(2000, max(ys) + DESC)]


def finds(hay, q, lo=0, hi=None):
    out, i = [], hay.find(q, lo, hi if hi is not None else len(hay))
    while i >= 0:
        out.append(i)
        i = hay.find(q, i + 1, hi if hi is not None else len(hay))
    return out


def search(P, text, near=None):
    """text 한 벌 → 후보 줄(점수 차례) · near = (쪽, 흐름 자리) 면 그 쪽 그 자리 뒤 1,500 글자 안에서만(보기 줄)"""
    qr, qm = norm(text, False), norm(text)
    if len(qm) < 2:
        return []
    cands = []
    pages = [near[0]] if near else sorted(P)
    for p in pages:
        pg = P[p]
        lo, hi = (near[1], near[1] + 1500) if near else (0, None)
        hit = False
        for i in finds(pg['raw'], qr, lo, hi):
            cands.append({'p': p, 'r': rect(pg['rc'][i:i + len(qr)]), 's': 1.0, 'how': '글', '_i': i}); hit = True
        if not hit:
            for i in finds(pg['m'], qm, lo, hi):
                cands.append({'p': p, 'r': rect(pg['mc'][i:i + len(qm)]), 's': 1.0, 'how': '명칭', '_i': i})
    if cands or len(qm) < 12:
        return cands
    # ③ 조각 — 닻 셋(앞 · 가운데 · 뒤)으로 자리를 어림하고 둘레 창의 닮음
    k = min(15, len(qm) // 3)
    anchors = [(0, qm[:k]), (len(qm) // 2 - k // 2, qm[len(qm) // 2 - k // 2: len(qm) // 2 - k // 2 + k]), (len(qm) - k, qm[-k:])]
    seen = set()
    for p in pages:
        pg = P[p]
        for off, a in anchors:
            for i in finds(pg['m'], a):
                st = max(0, i - off)
                key = (p, st // 8)
                if key in seen:
                    continue
                seen.add(key)
                win = pg['m'][st: st + len(qm) + 10]
                sm = difflib.SequenceMatcher(None, qm, win, autojunk=False)
                s = sm.ratio() * (len(qm) + len(win)) / (2 * len(qm))   # 창 길이 차 보정(짧은 쪽 = 질의 길이)
                if s >= 0.6:
                    blk = [b for b in sm.get_matching_blocks() if b.size]
                    j0, j1 = st + blk[0].b, st + blk[-1].b + blk[-1].size
                    cands.append({'p': p, 'r': rect(pg['mc'][j0:j1]), 's': round(min(1.0, s), 3), 'how': '조각', '_i': j0})
    # 쪽 경계에 걸친 글 — 앞 쪽 끝 + 뒤 쪽 앞 이어 붙여 통째(자리는 글자가 많은 쪽)
    if not cands and not near:
        for p in sorted(P):
            if p + 1 not in P:
                continue
            a, b = P[p], P[p + 1]
            hay = a['m'][-600:] + b['m'][:600]
            i = hay.find(qm)
            if i >= 0:
                cut = len(a['m'][-600:])
                na = max(0, cut - i)
                if na >= len(qm) - na:
                    s0 = len(a['m']) - na
                    cands.append({'p': p, 'r': rect(a['mc'][s0:]), 's': 0.9, 'how': '조각', '_i': s0})
                else:
                    cands.append({'p': p + 1, 'r': rect(b['mc'][:len(qm) - na]), 's': 0.9, 'how': '조각', '_i': 0})
    for c in cands:   # 지문 번호 바로 뒤에서 시작하는가(「…답IOI 16 」 꼴) — 같은 글이 다른 문항 ①·해설 속에도 있을 때 가른다
        s = P[c['p']]['raw'] if c['how'] == '글' else P[c['p']]['m']
        c['_no'] = int(bool(re.search(r'(\d{1,3}|유제\d?)$', s[max(0, c['_i'] - 8):c['_i']])))
    return cands


BODY_END = BK['end']   # 8판 짜임(pdf) — ~606 본문(제1편~제12편 · 비교표) · 607~649 미기출 판례 모아보기 · 650~789 연도별 기출 · 790 정답표 · 791~ 실전모의고사 · 뷰객 5판 = 549 전부(PART 1~9 · 뒤 되풀이 묶음 없음 · 되풀이는 해설 속 = _hs)


def best4(cands, want=None):
    """본문 먼저 — 본문 후보(점수 0.8 이상)가 있으면 뒤 묶음(모아보기·연도별 기출·모의고사의 되풀이)보다 앞에 선다 · 확신은 첫 줄과 같은 묶음 후보끼리 잰다
       want = 어림 쪽 (lo, hi) — 제7판 pdf쪽 + 0~40(8판 쪽 차이 실측 0~34) · 8판 새·리담 34 는 판8 pdf 쪽 그대로 · 같은 점수끼리만 가른다(점수를 이기지 않는다)"""
    for c in cands:
        c['_n7'] = int(bool(want) and want[0] <= c['p'] <= want[1])
        c['_b'] = int(c['p'] <= BODY_END and not c.get('_hs'))   # 묶음 — 본문 쪽(8판) · 해설 밖(뷰객 5판 · main_tm 이 _hs 를 단다)
    key = lambda c: (-c.get('_adj', 0), -c['s'], -c.get('_no', 0), -c['_n7'], c['p'], c['_i'])   # 보기 줄 = 발문 바로 뒤 먼저 · 같은 점수면 번호 바로 뒤 · 어림 쪽 안
    if BK['tm']:   # 뷰객 5판 — 짐작 쪽(그 줄 5판 pdf쪽)이 점수 앞(지시서 §A-3 「첫 짐작 쪽에서 1등이 안 나오면 책 전체」) · 짐작 쪽 0.8 미만은 아래 rest 로 · 해설 속 되풀이는 점수 앞에서 뒤로
        key = lambda c: (-c.get('_adj', 0), -c['_n7'], int(bool(c.get('_hs'))), -c['s'], -c.get('_no', 0), c['p'], c['_i'])
    body = sorted([c for c in cands if c['_b'] and c['s'] >= 0.8], key=key)
    rest = sorted([c for c in cands if not (c['_b'] and c['s'] >= 0.8)], key=key)
    out, seen = [], set()
    for c in body + rest:
        k = (c['p'], c['_i'] // 40)
        if k in seen:
            continue
        seen.add(k)
        out.append({'p': c['p'], 'r': c['r'], 's': c['s'], 'how': c['how'], '_n7': c['_n7'], '_adj': c.get('_adj', 0), '_no': c.get('_no', 0), '_b': c['_b']})
        if len(out) == 4:
            break
    if out:
        grp = [c for c in out if c['_b'] == out[0]['_b']]
        s = out[0]['s']
        g = s - (grp[1]['s'] if len(grp) > 1 else 0)
        c0 = '높음' if (s >= 0.95 and g >= 0.15) else ('중간' if (s >= 0.8 and g >= 0.05) else '낮음')
        if c0 == '낮음' and s >= 0.95 and len(grp) > 1 and (out[0]['_n7'] > grp[1]['_n7'] or out[0]['_adj'] > grp[1]['_adj'] or out[0]['_no'] > grp[1]['_no']):
            c0 = '중간'   # 같은 글 두 자리 — 어림 쪽 안 · 발문 바로 뒤 · 번호 바로 뒤가 하나뿐이면 중간
        out[0]['c'] = c0
    for c in out:
        c.pop('_n7', None); c.pop('_adj', None); c.pop('_no', None); c.pop('_b', None)
    return out


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    t0 = time.time()
    P = load_pages()
    if BK['tm']:
        return main_tm(P, t0)
    J = json.load(io.open(os.path.join(DATA, 'jimun_7pan.json'), encoding='utf-8'))
    TQ = json.load(io.open(os.path.join(DATA, 'jimun_특허.json'), encoding='utf-8'))
    objs = {o['id']: o for o in J.get('객관식', [])}
    res, src = collections.OrderedDict(), {}
    stems = {}
    for z in J['지문']:
        u = z.get('uid')
        if not u or u in res:
            continue
        cs = search(P, strip_tags(p7text(stmt(z['t']))))
        if cs and z.get('문항') and z.get('사례'):   # 보기 줄 — 발문(사례) 자리 바로 뒤(같은 쪽 1,500 글자 안 · 다음 쪽 앞 600 글자)를 앞세운다
            q = z['문항']
            if q not in stems:
                stems[q] = [c for c in search(P, strip_tags(p7text(z['사례']))) if c['s'] >= 0.8]
            for c in cs:
                c['_adj'] = int(any((s0['p'] == c['p'] and 0 <= c['_i'] - s0['_i'] <= 1500) or (c['p'] == s0['p'] + 1 and c['_i'] < 600) for s0 in stems[q]))
        p7 = int(z.get('pdf쪽') or 0)
        pdf8 = (z.get('판8') or {}).get('pdf8')
        res[u] = best4(cs, (pdf8, pdf8) if (pdf8 and not p7) else ((p7, p7 + 40) if p7 else None))
        if res[u] and (z.get('판8') or {}).get('cat') == '없음':   # p8up 「8판에 없음」 — 닮은 글은 다른 지문 해설 속 문장일 뿐(P7-1861 = 26 변리 해설) · 교재 자리라 하지 않는다
            res[u][0]['c'] = '낮음'
        src[u] = z['id']
    # 판8_리담 34 — 리담 선지 글(문항 통째면 uid 다섯 각각)
    L = J.get('판8_리담') or {}
    zq = {z['uid']: (q, z) for q in TQ['문제'] for z in q['지문'] if z.get('uid')}
    for k, v in L.items():
        for u in (v.get('uids') or [k]) if v.get('문항') else [k]:
            if u in res or u not in zq:
                continue
            q, z = zq[u]
            res[u] = best4(search(P, strip_tags(stmt(z.get('t') or ''))), (v.get('pdf8'), v.get('pdf8')) if v.get('pdf8') else None)
            src[u] = q['id']
    # 셈 · 헛잣대(채팅 표)
    c = collections.Counter()
    for u, rows in res.items():
        c['자리 있음' if rows else '못 찾음'] += 1
        if rows:
            c['확신 ' + rows[0]['c']] += 1
            c['갈래 ' + rows[0]['how']] += 1
    ref = json.load(io.open(REF, encoding='utf-8')) if os.path.exists(REF) else {}
    same, diff = 0, []
    for u, v in ref.items():
        rows = res.get(u)
        if rows and rows[0]['p'] == v['p8pdf']:
            same += 1
        else:
            diff.append([u, v.get('id'), v.get('p8pdf'), rows[0]['p'] if rows else None, rows[0]['how'] if rows else None, rows[0]['s'] if rows else None])
    meta = {'docid': DOCID, 'unit': 2000, 'n': len(res), 'counts': dict(c), 'ref_same': same, 'ref_n': len(ref),
            'rule': '문장 = 첫 「답 I x I」 앞 · 글 = 그대로 통째 · 명칭 = 지식재산처↔특허청 맞춰 통째 · 조각 = 닻 셋 둘레 창 닮음(≥0.6) · 차례 = 본문(pdf ≤606 · 0.8 이상) 먼저 → 보기 줄은 발문 바로 뒤 → 점수 → 번호 바로 뒤 → 어림 쪽(제7판 pdf +0~40 · 8판 새·리담 34 = 판8 쪽) · 후보 넷 · c = 확신(첫 줄 · 같은 묶음 후보끼리)',
            'src': 'jo/data jimun_7pan.json(판 %s · 건수 %s) · jimun_특허.json · words/%s 책메타 pageHash' % (J.get('판'), J.get('건수'), DOCID)}
    out = {'_meta': meta}
    out.update(res)
    b = (json.dumps(out, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')
    print('대상 uid %d · %s · 채팅 표 1등 쪽 같음 %d / %d · %.0f초' % (len(res), json.dumps(dict(c), ensure_ascii=False), same, len(ref), time.time() - t0))
    print('채팅 표와 1등 쪽 다름 %d (uid · id · 채팅 p8pdf · 여기 · 갈래 · 점수) 앞 12: %s' % (len(diff), json.dumps(diff[:12], ensure_ascii=False)))
    if '--dry' not in sys.argv:
        for _ in range(5):
            open(OUT, 'wb').write(b); time.sleep(0.3)
            if open(OUT, 'rb').read() == b:
                break
        print('씀', OUT, len(b), 'B')
    return res, diff


TBL = re.compile(r'\[도형\]|\(도안 글자\)|상품[12]\s*:|결과\s*:|특이사항\s*:')   # 뷰객 표 보기 줄 — census 가 단 이름표 · 그림 자리표(책 글자층에 없음)


def overlap(a, b):
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


def hs_flags(P):
    """쪽 → {'raw': [해설 안?], 'm': [해설 안?]}(흐름 글자마다) — 글자층 차례로 「해설」 머리(왼쪽 끝 · x < 300 · 글 속 「…에 대한 해설과 동일」 · 「의해 설정」 은 x ≥ 300) = 안 ·
       「정답」 · 「#」(문항 머리 · 시험 번호) = 밖 · 쪽을 건너 이어진다(5판 글자층 실측 해설 머리 821 · 글 속 14)"""
    st, F = False, {}
    for p in sorted(P):
        o = json.loads(gzip.decompress(open(os.path.join(WORDS, 'ox_book_%s_p%d.json.gz' % (DOCID, p)), 'rb').read()).decode('utf-8'))
        rows = [l.split('\t') for l in o['words'].split('\n') if l]
        full = fold(''.join(r[0] for r in rows))
        raw = []
        for i, c in enumerate(full):
            if full.startswith('해설', i) and int(rows[i][1]) < 300:
                st = True
            elif full.startswith('정답', i) or c == '#':
                st = False
            if KEEP.match(c):
                raw.append(st)
        assert len(raw) == len(P[p]['raw']), (p, len(raw), len(P[p]['raw']))
        m, i, r = [], 0, P[p]['raw']
        while i < len(r):   # 명칭 흐름(load_pages 와 같은 줄임)
            if r.startswith('지식재산처', i):
                m += [raw[i], raw[i + 2], raw[i + 4]]; i += 5
            else:
                m.append(raw[i]); i += 1
        F[p] = {'raw': raw, 'm': m}
    return F


def main_tm(P, t0):
    """sp_book5 §A-3 — 상표 1차객 카드 → 뷰객 5판 자리(찾기 · 후보 · 확신 = search · best4 · 머리 설명 「책 갈래」)"""
    J = json.load(io.open(os.path.join(DATA, 'jimun_상표_뷰객.json'), encoding='utf-8'))
    TQ = json.load(io.open(os.path.join(DATA, 'jimun_상표.json'), encoding='utf-8'))
    book = [z for z in J['지문'] + J.get('객관식', []) if z.get('uid') and (z.get('판5') or {}).get('cat') != '없음']
    by = collections.OrderedDict()
    for z in book:
        by.setdefault(z['uid'], []).append(z)
    HS = hs_flags(P)
    stems = {}
    tally = collections.Counter()

    def mark(cs):   # 후보마다 해설 안?(_hs) — best4 묶음
        for c in cs:
            f = HS[c['p']]['raw' if c['how'] == '글' else 'm']
            c['_hs'] = f[c['_i']] if c['_i'] < len(f) else False
        return cs

    def near(text, p0):   # 책 전체 닻 찾기가 짐작 쪽 해설 밖을 못 잡은 줄 — 짐작 쪽 · 다음 쪽 해설 밖만 닻 없이 창 닮음(짧은 글 · 글자층 오독 · 리담 글)
        qm, out = norm(text), []
        if len(qm) < 4:
            return out
        for p in (p0, p0 + 1):
            pg = P.get(p)
            if not pg or not pg['m']:
                continue
            L, best = len(qm), None
            for st in range(0, max(1, len(pg['m']) - L + 1)):
                if HS[p]['m'][st]:
                    continue
                win = pg['m'][st: st + L + 2]
                sm = difflib.SequenceMatcher(None, qm, win, autojunk=False)
                sc = sm.ratio() * (L + len(win)) / (2 * L)
                if best is None or sc > best[0] + 1e-9:
                    best = (sc, st, sm)
            if best and best[0] >= 0.6:
                sc, st, sm = best
                blk = [x for x in sm.get_matching_blocks() if x.size]
                j0, j1 = st + blk[0].b, st + blk[-1].b + blk[-1].size
                out.append({'p': p, 'r': rect(pg['mc'][j0:j1]), 's': round(min(1.0, sc), 3), 'how': '조각', '_i': j0})
        return out

    def cands(z, text, p0, stem=True):   # 한 줄 → 후보(책 전체 search · 해설 안 표시 · 짐작 쪽 창 닮음 · 발문 바로 뒤)
        cs = mark(search(P, text))
        if p0 and not any(p0 <= c['p'] <= p0 + 1 and c['s'] >= 0.8 and not c['_hs'] for c in cs):
            got = [c for c in mark(near(text, p0)) if not any(c['p'] == x['p'] and overlap(c['r'], x['r']) for x in cs)]
            tally['짐작 쪽 창 닮음 ' + ('잡음' if got else '없음')] += 1
            cs += got
        if stem and cs and z.get('문항') and z.get('사례'):   # 보기 줄 · 선지 — 발문(사례) 자리 바로 뒤를 앞세운다(book8 꼴 · 발문 끝 뒤부터 — 짧은 선지 「거절결정」 이 발문 속 같은 낱말에 걸리지 않게)
            q = z['문항']
            if q not in stems:
                sq = strip_tags(p7text(z['사례']))
                stems[q] = [(c, len(norm(sq, c['how'] != '글'))) for c in search(P, sq) if c['s'] >= 0.8]
            for c in cs:
                c['_adj'] = int(any((s0['p'] == c['p'] and n0 <= c['_i'] - s0['_i'] <= 1500 + n0) or (c['p'] == s0['p'] + 1 and c['_i'] < 600) for s0, n0 in stems[q]))
        return cs

    def want(z):   # 첫 짐작 쪽 = 그 줄 5판 pdf쪽(· 다음 쪽 — 쪽을 넘는 선지 · 보기)
        p = int(z.get('pdf쪽') or 0)
        return (p, p + 1) if p else None

    res, src, rowbest = collections.OrderedDict(), {}, {}
    for u, zs in by.items():
        C = [cands(z, strip_tags(p7text(stmt(TBL.sub(' ', z['t'])))), int(z.get('pdf쪽') or 0)) for z in zs]
        B = [best4(cs, want(z)) for z, cs in zip(zs, C)]
        for z, b in zip(zs, B):
            if b:
                rowbest[z['id']] = b[0]
        src[u] = zs[0]['id']
        k0 = next((k for k, b in enumerate(B) if b), None)   # 1등 · 확신 = 지문 차례 첫 줄(못 찾으면 찾은 다음 줄)
        tally['같은 uid 둘째 줄'] += len(zs) - 1
        if k0 is None:
            res[u] = []
            continue
        if k0:
            tally['같은 uid 첫 줄 못 찾음 → 다음 줄이 1등'] += 1
        rows, tw = B[k0], []
        for k in range(k0 + 1, len(zs)):   # 둘째 줄부터 그 줄 1등 — 같은 uid = 같은 지문이라 1·2등 차를 잴 때 빼고 2등 후보로 끼운다
            t = B[k][0] if B[k] else None
            if t is None:
                tally['같은 uid 둘째 줄 못 찾음'] += 1
            elif any(t['p'] == x['p'] and overlap(t['r'], x['r']) for x in rows[:1] + tw):
                tally['같은 uid 둘째 줄 1등 = 앞 자리'] += 1
            else:
                tw.append({kk: t[kk] for kk in ('p', 'r', 's', 'how')})
                tally['같은 uid 둘째 줄 1등 = 2등 후보'] += 1
        if tw:
            rows = best4([c for c in C[k0] if not any(c['p'] == t['p'] and overlap(c['r'], t['r']) for t in tw)], want(zs[k0]))
            assert rows and rows[0]['p'] == B[k0][0]['p'] and rows[0]['r'] == B[k0][0]['r'], u
            rows = rows[:1] + tw + rows[1:]
        res[u] = rows[:4]
    # 리담 선지 가운데 뷰객 짝(뷰객 줄 리담 칸)의 uid 가 다른 것 — 리담 글로 찾고(book8 판8_리담 그대로) · 짝 줄 1등 자리도 후보(점수 = 리담 글과 그 자리 글의 닮음) · 짐작 쪽 = 짝 줄 5판 pdf쪽
    key = {(q.get('연도'), q.get('문번'), s.get('n')): (q, s) for q in TQ['문제'] for s in q['지문']}
    pairs = collections.OrderedDict()
    for z in book:
        r = z.get('리담') or {}
        q, s = key.get((r.get('연도'), r.get('문항'), r.get('선지')), (None, {}))
        u = s.get('uid')
        if u and u not in res:
            pairs.setdefault(u, (q, s, []))[2].append(z)
    for u, (q, s, zs) in pairs.items():
        text = strip_tags(stmt(s.get('t') or ''))
        cs, qm = cands(zs[0], text, int(zs[0].get('pdf쪽') or 0), stem=False), norm(text)
        for z in zs:
            b = rowbest.get(z['id'])
            if not b or not qm:
                continue
            pg = P[b['p']]
            idx = [i for i, (ch, x, y) in enumerate(pg['mc']) if b['r'][0] <= x <= b['r'][2] and b['r'][1] <= y <= b['r'][3]]
            if not idx:
                continue
            sm = difflib.SequenceMatcher(None, qm, ''.join(pg['m'][i] for i in idx), autojunk=False)
            sc = round(min(1.0, sum(x.size for x in sm.get_matching_blocks()) / len(qm)), 3)
            ov = [c for c in cs if c['p'] == b['p'] and overlap(c['r'], b['r'])]
            if ov and max(c['s'] for c in ov) >= sc:
                continue   # 그 자리를 리담 글이 이미 같거나 더 높은 점수로 잡았다
            cs = [c for c in cs if c not in ov] + mark([{'p': b['p'], 'r': b['r'], 's': sc, 'how': '조각', '_i': idx[0]}])
            tally['리담 짝 줄 자리 후보'] += 1
        res[u] = best4(cs, want(zs[0]))
        src[u] = q['id']
    # 셈 · 1등 쪽 = 그 줄 5판 pdf쪽
    c = collections.Counter()
    for u, rows in res.items():
        c['자리 있음' if rows else '못 찾음'] += 1
        if rows:
            c['확신 ' + rows[0]['c']] += 1
            c['갈래 ' + rows[0]['how']] += 1
    same, diff = 0, []
    for u, zs in by.items():
        rows = res.get(u)
        if rows and rows[0]['p'] == int(zs[0].get('pdf쪽') or 0):
            same += 1
        else:
            diff.append([u, zs[0]['id'], zs[0].get('pdf쪽'), rows[0]['p'] if rows else None, rows[0]['how'] if rows else None, rows[0]['s'] if rows else None])
    meta = {'docid': DOCID, 'unit': 2000, 'n': len(res), 'counts': dict(c), 'pdf_same': same, 'pdf_n': len(by),
            'rule': '문장 = 첫 「답 I x I」 앞 · 글 = 그대로 통째 · 명칭 = 지식재산처↔특허청 맞춰 통째 · 조각 = 닻 셋 둘레 창 닮음(≥0.6) · 짐작 쪽 창 닮음(닻 없이 · 그 쪽 해설 밖에 0.8 이상이 없을 때) · 맞댐 글자 = 한글·라틴·숫자·ㄱ~ㅎ·甲乙丙丁(원문자 뺌) · 甲乙丙 오독 접기(己石江乞→乙 · 內→丙 · Z+토씨→乙 · 양쪽) · 표 보기 줄 이름표·그림 자리표 뺌 · 묶음 = 해설 밖 먼저(해설 머리 x<300 ~ 정답 · # · 해설 속 되풀이 뒤로) · 차례 = 보기 줄·선지는 발문 바로 뒤 → 짐작 쪽(그 줄 5판 pdf쪽 · 다음 쪽) → 점수 → 번호 바로 뒤 · 같은 uid 둘째 줄부터 그 줄 1등 = 2등 후보(확신은 그 자리 빼고) · 리담 짝(uid 다름) = 리담 글 + 짝 줄 1등 자리(점수 = 리담 글 닮음) · 짐작 쪽 = 짝 줄 pdf쪽 · 후보 넷 · c = 확신(첫 줄 · 같은 묶음 후보끼리)',
            'src': 'jo/data jimun_상표_뷰객.json(판 %s · 건수 %s) · jimun_상표.json · words/%s 책메타 pageHash' % (J.get('판'), J.get('건수'), DOCID)}
    out = {'_meta': meta}
    out.update(res)
    b = (json.dumps(out, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')
    print('대상 uid %d(책 줄 uid %d · 리담 짝 uid %d) · %s · 1등 쪽 = 첫 줄 5판 pdf쪽 %d / %d · %s · %.0f초'
          % (len(res), len(by), len(pairs), json.dumps(dict(c), ensure_ascii=False), same, len(by), json.dumps(dict(tally), ensure_ascii=False), time.time() - t0))
    print('1등 쪽 ≠ pdf쪽 %d (uid · id · pdf쪽 · 여기 · 갈래 · 점수) 앞 12: %s' % (len(diff), json.dumps(diff[:12], ensure_ascii=False)))
    if '--dry' not in sys.argv:
        for _ in range(5):
            open(OUT, 'wb').write(b); time.sleep(0.3)
            if open(OUT, 'rb').read() == b:
                break
        print('씀', OUT, len(b), 'B')
    return res, diff


if __name__ == '__main__':
    main()
