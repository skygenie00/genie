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


DATA = ARG('--data', _roots.genie(r'jo\data'))
WORDS = ARG('--words', _roots.mbpdf(r'words\patent_hr8'))
OUT = ARG('--out', os.path.join(WORDS, '대응.json'))
REF = ARG('--ref', os.path.join(HERE, 'task', '_ref_book8_pos.json'))
DOCID = 'patent_hr8'
KEEP = re.compile(r'[가-힣A-Za-z0-9ㄱ-ㅎ①-⑳]')
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
    s = ''.join(ch for ch in s if KEEP.match(ch))
    return s.replace('지식재산처', '특허청') if name else s


def load_pages():
    pages = {}
    for f in glob.glob(os.path.join(WORDS, 'ox_book_%s_p*.json.gz' % DOCID)):
        o = json.loads(gzip.decompress(open(f, 'rb').read()).decode('utf-8'))
        rows = [l.split('\t') for l in o['words'].split('\n') if l]
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


BODY_END = 606   # 8판 짜임(pdf) — ~606 본문(제1편~제12편 · 비교표) · 607~649 미기출 판례 모아보기 · 650~789 연도별 기출 · 790 정답표 · 791~ 실전모의고사


def best4(cands, want=None):
    """본문 먼저 — 본문 후보(점수 0.8 이상)가 있으면 뒤 묶음(모아보기·연도별 기출·모의고사의 되풀이)보다 앞에 선다 · 확신은 첫 줄과 같은 묶음 후보끼리 잰다
       want = 어림 쪽 (lo, hi) — 제7판 pdf쪽 + 0~40(8판 쪽 차이 실측 0~34) · 8판 새·리담 34 는 판8 pdf 쪽 그대로 · 같은 점수끼리만 가른다(점수를 이기지 않는다)"""
    for c in cands:
        c['_n7'] = int(bool(want) and want[0] <= c['p'] <= want[1])
    key = lambda c: (-c.get('_adj', 0), -c['s'], -c.get('_no', 0), -c['_n7'], c['p'], c['_i'])   # 보기 줄 = 발문 바로 뒤 먼저 · 같은 점수면 번호 바로 뒤 · 어림 쪽 안
    body = sorted([c for c in cands if c['p'] <= BODY_END and c['s'] >= 0.8], key=key)
    rest = sorted([c for c in cands if not (c['p'] <= BODY_END and c['s'] >= 0.8)], key=key)
    out, seen = [], set()
    for c in body + rest:
        k = (c['p'], c['_i'] // 40)
        if k in seen:
            continue
        seen.add(k)
        out.append({'p': c['p'], 'r': c['r'], 's': c['s'], 'how': c['how'], '_n7': c['_n7'], '_adj': c.get('_adj', 0), '_no': c.get('_no', 0)})
        if len(out) == 4:
            break
    if out:
        grp = [c for c in out if (c['p'] <= BODY_END) == (out[0]['p'] <= BODY_END)]
        s = out[0]['s']
        g = s - (grp[1]['s'] if len(grp) > 1 else 0)
        c0 = '높음' if (s >= 0.95 and g >= 0.15) else ('중간' if (s >= 0.8 and g >= 0.05) else '낮음')
        if c0 == '낮음' and s >= 0.95 and len(grp) > 1 and (out[0]['_n7'] > grp[1]['_n7'] or out[0]['_adj'] > grp[1]['_adj'] or out[0]['_no'] > grp[1]['_no']):
            c0 = '중간'   # 같은 글 두 자리 — 어림 쪽 안 · 발문 바로 뒤 · 번호 바로 뒤가 하나뿐이면 중간
        out[0]['c'] = c0
    for c in out:
        c.pop('_n7', None); c.pop('_adj', None); c.pop('_no', None)
    return out


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    t0 = time.time()
    P = load_pages()
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


if __name__ == '__main__':
    main()
