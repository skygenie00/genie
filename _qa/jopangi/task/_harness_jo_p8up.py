# -*- coding: utf-8 -*-
r"""_task_jo_p8up §B 관문 하네스 — 해례 8판 원장 판올림(데이터 + 앱).

  python _harness_jo_p8up.py --new <앱> --data <jo/data(8판 얹음)> [--exam <gichul/pdf>] [--res <결과>] [--eng chromium,webkit] [--only d1,a5,...] [--shots <폴더>]

  NEW  = 이 판 앱 + 8판 얹은 데이터 · BASE = genie HEAD(jo_hdrfold 인도판 = 바로 앞 인도판) 앱 + HEAD 데이터 — 칸마다 헛잣대(바탕에서 FAIL)
  누름 = 진짜 포인터(page.mouse · 손가락 = Chromium CDP 터치 r22 · WebKit touchscreen.tap) · 보임 = display ≠ none · 높이 > 0 · 자리 = elementFromPoint
  바탕 틀 = mbsame 하네스(_harness_jo_gaek_mbsame.py)의 serve·Pg·__HM + uidmbs2 도구(__UZ) + 이 판 도구(__P8)
  ⚠ 8판 PDF 는 안 연다(워터마크 든 글자층) — 쪽·번호·글은 원장 판8 칸과 특상디\_p8up\ 표로만 잰다.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import io, json, os, re, sys, time, shutil, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
JOP = os.path.dirname(HERE)


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


_NEW, _DATA, _EXAM = ARG('--new'), ARG('--data'), ARG('--exam')
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_p8up_result.txt'))
SHOTS = ARG('--shots', os.path.join(HERE, '_shots_p8up'))
SPD = ARG('--rec', _roots.spd(r'jopangi\기록.json'))
sys.argv = [sys.argv[0], '--new', _NEW, '--data', _DATA, '--base', 'f58039a'] + (['--exam', _EXAM] if _EXAM else [])   # A-6(d) 9/30 — 바탕 = 인도 때 HEAD f58039a(결과 머리 「바탕 HEAD f58039a」) · HEAD 로 두면 인도 뒤 헛잣대·바탕 대조가 새 판끼리 맞대 거꾸로 FAIL
sys.path.insert(0, HERE)
sys.path.insert(0, JOP)
import _harness_jo_gaek_mbsame as M   # noqa: E402
import _p8up_apply as P8A             # noqa: E402
from playwright.sync_api import sync_playwright   # noqa: E402
M.TESTS = M.TESTS + '\n' + io.open(os.path.join(HERE, '_harness_jo_uidmbs2_tests.js'), encoding='utf-8').read() \
    + '\n' + io.open(os.path.join(HERE, '_harness_jo_p8up_tests.js'), encoding='utf-8').read()
M.WORK = M.WORK + '_p8'
RES = []
GRAY, RED, GREEN = 'rgb(156, 163, 175)', 'rgb(220, 38, 38)', 'rgb(21, 128, 61)'
DEL_ID, DEL_UID = ['P7-1207', 'P7-1599'], ['TJ161207', 'TH111599']


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def jl(p):
    return json.loads(open(p, 'rb').read().decode('utf-8'))


class Pg(M.Pg):
    """엔진 이름을 들고 다닌다 — 손가락 = Chromium CDP r22 · WebKit touchscreen.tap"""
    def __init__(self, br, eng, tag, src, data, exam, W=1440, H=900, **k):
        self.eng = eng
        ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, has_touch=True)
        super().__init__(br, tag + '_' + eng, src, data, exam, ctx=ctx, **k)

    def tap(self, at, wait=500):
        if not at or not at.get('on'):
            return False
        if self.eng == 'webkit':
            self.pg.touchscreen.tap(at['cx'], at['cy'])
            self.pg.wait_for_timeout(wait)
            return True
        return super().tap(at, wait)

    def press(self, at, how, wait=500):
        return self.tap(at, wait) if how == 'touch' else self.click(at, wait)


def home(p, gk='g', law='특허법'):
    p.ev("l=>__HM.home(l)", law)
    if p.ev("()=>__UZ.has('UZGK')"):
        p.ev("v=>__UZ.gk(v)", gk)


def go_key(p, k):
    """열쇠가 든 단원 줄로 가서 그 카드가 선 쪽까지(기출/기타는 열쇠 갈래로 먼저 맞춘다)"""
    home(p)   # 1차객 재료(VJ)가 선 뒤에 갈래를 잰다(없으면 uzIsGi 가 늘 기출)
    gk = p.ev("k=>{try{return uzIsGi(k)?'g':'x'}catch(e){return 'g'}}", k)
    home(p, gk)
    sel = p.ev("k=>__UZ.selOfKey(k)", k)
    if not sel:
        return None
    p.ev("s=>__HM.go(s)", sel)
    pg = p.ev("k=>{const P=(OXPOOL||{})[k];if(!P)return null;const d=P.dom;const c=document.getElementById(d);return c?null:(OXDOMPG||{})[d]}", k)
    if pg:
        p.ev("n=>__HM.page(n)", pg)
    p.pg.wait_for_timeout(300)
    return sel


# ══════════ 데이터 관문 ══════════
def env_data():
    bs, bd, be = M.base_env()
    return _DATA, bd


def d_b1():
    """§B-1 원장 셈 · P7-0069-ㄱ~ㅂ"""
    nd, bd = env_data()
    J, B = json.loads(M.git('show', '775457c:jo/data/jimun_7pan.json').decode('utf-8')), jl(os.path.join(bd, 'jimun_7pan.json'))   # A-6(d) 9/30 — 인도 검산 새 쪽 = p8up 인도 커밋 775457c(이 함수에서 J 를 쓰는 항목은 「원장 셈」·「P7-0069 무변」 둘뿐) · 뒤 판 p8sol(판8 {cat:해설} 82 · P7-0069 판8 칸)·revfix0928pm(P7-1153 문장→자리)이 지금 원장을 바꿈
    c = collections.Counter(z['판8']['cat'] for z in J['지문'] if z.get('판8'))
    T('1', '원장 셈 — 지문 2,521 − 2 + 19 = 2,538 · 판8.cat = 명칭 156 · 기관 7 · 오류 5 · 자리 2 · 문장 24 · 답 3 · 없음 6 · 새 19 · 머리 판 「7+8」 · 판8_기준 · 건수',
      len(J['지문']) == 2538 and dict(c) == {'명칭': 156, '기관': 7, '오류': 5, '자리': 2, '문장': 24, '답': 3, '없음': 6, '새': 19} and J.get('판') == '7+8' and J.get('판8_기준') == P8A.BASIS and J.get('건수') == 2538,   # A-6(d) 인도 때 셈(= 제목 글자) · P8A.WANT 는 revfix0928pm §A-4 가 자리 3·문장 23 으로 옮김
      {'지문': len(J['지문']), 'cat': dict(c), '판': J.get('판'), '판8_기준': J.get('판8_기준'), '건수': J.get('건수')})
    T('1-헛', '헛잣대 바탕 — 2,521 · 판8 칸 0 · 판 칸 없음', len(B['지문']) == 2521 and not any(z.get('판8') for z in B['지문']) and '판' not in B,
      {'지문': len(B['지문']), '판8': sum(1 for z in B['지문'] if z.get('판8'))})
    six = [z for z in J['지문'] if z['id'].startswith('P7-0069-')]
    six0 = {z['id']: z for z in B['지문'] if z['id'].startswith('P7-0069-')}
    T('1', 'P7-0069-ㄱ~ㅂ 6(채팅 대조 밖) — 8판 대조 결과 「같음」 → 원장 무변(판8 칸 없음 · 글·답 = 바탕)',
      len(six) == 6 and all(not z.get('판8') and z == six0.get(z['id']) for z in six), [(z['id'], z['t'], z['ox']) for z in six])
    f = os.path.join(JOP, '특상디', '_p8up', '_p8up_0069.json')
    if os.path.exists(f):
        r = jl(f)
        N('1', 'P7-0069-ㄱ~ㅂ 8판 대조(특상디\\_p8up\\_p8up_0069.json · task\\_p8up_0069.py) — 8판 pdf %s(인쇄 p.%s) 15번 · 발문 맞은 길이 %s/%s · 7판 답 %s · 8판 답 %s'
          % (r['8판 pdf'], r['8판 인쇄쪽'], r['발문 맞은 길이'], r['발문 길이'], r['7판 답'], r['8판 답']), [(x['id'], x['판정']) for x in r['보기']])
    else:
        T('1', 'P7-0069-ㄱ~ㅂ 8판 대조 결과 파일', False, f)


def d_b2():
    """§B-2 지운 둘 — 모든 데이터 파일 · 기록 사본"""
    nd, bd = env_data()
    rx = re.compile('(?<![0-9A-Za-z가-힣ㄱ-ㅎ])(%s)(?![0-9A-Za-z가-힣ㄱ-ㅎ-])' % '|'.join(DEL_ID + DEL_UID))

    def census(d):
        out = {}
        for f in sorted(os.listdir(d)):
            if not f.endswith('.json'):
                continue
            s = open(os.path.join(d, f), 'rb').read().decode('utf-8', 'replace')
            n = collections.Counter(m.group(1) for m in rx.finditer(s))
            if n:
                out[f] = dict(n)
        return out
    cn, cb = census(nd), census(bd)
    T('2', '지운 둘(P7-1207 TJ161207 · P7-1599 TH111599) — 새 데이터 json 전부에 id·uid 0(원장 · 연도색인 · 마디 · 제7판 목차 · 별칭표 · 그 밖)', not cn, cn)
    T('2-헛', '헛잣대 바탕 — 가리키는 곳 있음(지운 참조 목록)', bool(cb), cb)
    if os.path.exists(SPD):
        R = jl(SPD)
        hits = collections.Counter()

        def walk(o, path):
            if isinstance(o, dict):
                for k, v in o.items():
                    if rx.search(k):
                        hits[path + '/' + k] += 1
                    walk(v, path + '/' + k)
            elif isinstance(o, list):
                for v in o:
                    walk(v, path)
            elif isinstance(o, str) and rx.search(o):
                hits[path] += 1
        walk(R, '')
        T('2', '기록 사본(studyplandata jopangi/기록.json · savedAt %s) — 두 uid·id 를 가리키는 칸 0(사용자 「없다」)' % R.get('savedAt'), not hits, dict(hits))
    else:
        T('2', '기록 사본', False, '없음 ' + SPD)


def d_b3():
    """§B-3 글 — 표 197 · 채움 셋"""
    nd, bd = env_data()
    J, B = jl(os.path.join(nd, 'jimun_7pan.json')), jl(os.path.join(bd, 'jimun_7pan.json'))
    ref, fill = jl(P8A.REF), jl(P8A.FILL)
    by, b0 = {z['id']: z for z in J['지문']}, {z['id']: z for z in B['지문']}
    ok, bad, base_ok, n = 0, [], 0, 0
    for i, v in ref['changed'].items():
        z, b = by[i], b0[i]
        c = P8A.CAT[v['cat']]
        t8 = v.get('t8') or (fill['fill'].get(i) or {}).get('t8')
        if c == '자리':
            good = z['t'] == b['t'] and 't7' not in z['판8']
        elif i == 'P7-2052':
            m = re.search(r'답\s*[I|]\s*[OX]\s*[I|]', b['t'])
            good = z['t'] == b['t'][:m.end()] and z['판8'].get('t7') == b['t'] and re.search(r'답\s*[I|]\s*[OX]\s*[I|]$', z['t']) is not None
        else:
            n += 1
            good = P8A.ws(P8A.split_tail(z['t'])[0]) == P8A.ws(t8) and z['판8'].get('t7') == b['t']
            base_ok += P8A.ws(P8A.split_tail(b['t'])[0]) == P8A.ws(t8)
        ok += good
        if not good:
            bad.append(i)
    T('3', '글 — 표 197 줄 전부: t8 있는 %d 줄 = 원장 t 의 문장이 t8 과 같음(빈칸만 무시) · 7판 글 = 판8.t7 · 자리만 옮김 2 = 글 무변 · P7-2052 = 「답 I O I」 뒤 걷음(%d자 → %d자)'
      % (n, len(b0['P7-2052']['t']), len(by['P7-2052']['t'])), ok == len(ref['changed']) and not bad, {'맞음': ok, '표': len(ref['changed']), '어긋남': bad[:8]})
    T('3-헛', '헛잣대 바탕 — 바탕 글이 t8 과 같은 줄은 일부뿐', base_ok < n, {'바탕 = t8': base_ok, 't8 줄': n})
    rows = []
    for i in ('P7-1153', 'P7-1601', 'P7-1879'):
        f = fill['fill'][i]; z = by[i]
        rows.append({'id': i, 'uid': z['uid'], '8판': 'p.%s(pdf %s) %s' % (f['p8'], f['pdf8'], f['no8']), '판8': z['판8'], '글': P8A.p7text(z['t'])[:90]})
    T('3', '채팅이 못 뽑은 셋 P7-1153 · 1601 · 1879 — 채움 표(8판 글자층 · 쪽 그림 대조)의 글 = 원장 문장 · 판8 칸에 8판 쪽·번호', all(P8A.ws(P8A.split_tail(by[r['id']]['t'])[0]) == P8A.ws(fill['fill'][r['id']]['t8']) and by[r['id']]['판8'].get('p8') for r in rows), rows)


def d_b4():
    """§B-4 답 — 바뀐 셋 · 새 19"""
    nd, bd = env_data()
    J, B = jl(os.path.join(nd, 'jimun_7pan.json')), jl(os.path.join(bd, 'jimun_7pan.json'))
    by, b0 = {z['id']: z for z in J['지문']}, {z['id']: z for z in B['지문']}
    want = {'P7-0826': 'X', 'P7-1871': 'X', 'P7-1884': 'O'}
    got = {i: (b0[i]['ox'], by[i]['ox'], by[i]['판8'].get('a7'), by[i]['판8']['cat']) for i in want}
    T('4', '답 바뀜 셋 — P7-0826 = X · 1871 = X · 1884 = O(판8.a7 = 옛 답 · cat 답)', all(got[i][1] == w and got[i][2] == got[i][0] and got[i][3] == '답' for i, w in want.items()), {i: '바탕 %s → 새 %s (a7 %s · %s)' % g for i, g in got.items()})
    T('4-헛', '헛잣대 바탕 — 셋 모두 옛 답(O · O · X)', all(b0[i]['ox'] != w for i, w in want.items()), {i: b0[i]['ox'] for i in want})
    fill = jl(P8A.FILL)
    ans = {(a['p8'], a['no8']): a for a in fill['new19_ans']}
    ref = jl(P8A.REF)
    new = [x for x in ref['new'] if x['할일'] == '새 카드']
    rows, bad = [], []
    for k, x in enumerate(new, 1):
        z = by.get('P8-%04d' % k)
        a = ans.get((x['p8'], x['no8'])) or {}
        rows.append('%s %s 8판 p.%s %s 답 %s(8판 답 줄 pdf %s %s · 쪽 그림 대조 %s)' % (z and z['id'], z and z['uid'], x['p8'], x['no8'], z and z['ox'], (a.get('ans') or [None, None])[1], (a.get('ans') or [None])[0], a.get('same')))
        if not z or z['ox'] != x['a8'] or not a.get('same') or z['판8'] != {'cat': '새', 'p8': x['p8'], 'pdf8': x['pdf8'], 'no8': P8A.no8n(x['no8']), '모아보기': x.get('모아보기') or []}:
            bad.append(x['no8'])
    T('4', '새 19 — 답 = 표 a8 = 8판 쪽 그림(채움 표 same) · 19 전부 · 판8 칸(cat 새 · p8 · pdf8 · no8 · 모아보기)', len(rows) == 19 and not bad, rows)
    T('4-헛', '헛잣대 바탕 — 새 19 줄 없음', not any(z['id'].startswith('P8-') for z in B['지문']), '')


def d_b5():
    """§B-8 멱등 · 다시 만들기 — 바탕 넷에 얹은 것 = 인도 데이터(바이트) · 두 번 얹어도 같음"""
    _rv, M.BASE_REV = M.BASE_REV, 'HEAD'   # A-6(d) 9/30 — 이 칸만 지금 HEAD 데이터에 얹는다(거저 PASS 유지 — 바탕 f58039a 에 얹으면 뒤 판 ⚙ 재료(_ref_p8up.json · revfix0928pm P7-1153)·원장 변화로 인도 데이터와 바이트가 달라 깨짐)
    try:
        nd, bd = env_data()
    finally:
        M.BASE_REV = _rv
    ref, fill = jl(P8A.REF), jl(P8A.FILL)
    outs = []
    for _ in range(2):
        objs = {f: jl(os.path.join(bd, f)) for f in P8A.FILES}
        log, bad = P8A.apply(objs, ref, fill)
        outs.append({f: P8A.dump_b(objs[f]) for f in P8A.FILES})
        again = P8A.apply(objs, ref, fill)
    newb = {f: open(os.path.join(nd, f), 'rb').read() for f in P8A.FILES}
    T('8', '멱등 — 바탕 넷에 두 번 따로 얹어 바이트 같음 · 얹은 것에 한 번 더 = 그대로(None) · 인도 데이터 넷 = 바탕에서 다시 만든 것(바이트)',
      outs[0] == outs[1] and again[0] is None and all(outs[0][f] == newb[f] for f in P8A.FILES), {f: [len(newb[f]), outs[0][f] == newb[f]] for f in P8A.FILES})


def d_b7():
    """§B-7 데이터 — 이미 있는 34 표 · 마디 어긋남"""
    nd, bd = env_data()
    J = jl(os.path.join(nd, 'jimun_7pan.json'))
    MK = jl(os.path.join(nd, 'mokcha_병합.json'))
    TQ = jl(os.path.join(nd, 'jimun_특허.json'))
    L = J.get('판8_리담') or {}
    uid2q = {z['uid']: q['id'] for q in TQ['문제'] for z in q['지문'] if z.get('uid')}
    qids = {q['id'] for q in TQ['문제']}
    new_uids = {z['uid'] for z in J['지문'] if z['id'].startswith('P8-')}
    miss = [k for k, v in L.items() if not ((v.get('문항') and k in qids) or k in uid2q)]
    T('7', '이미 있는 34 — 판8_리담 표 34 칸 · 열쇠 = 앱 리담 uid(문항 통째 2026-63-2 = 문항 id) · 새 카드와 겹침 0',
      len(L) == 34 and not miss and not (set(L) & new_uids), {'칸': len(L), '없는 열쇠': miss, '표본': {k: L.get(k) for k in ('T2663014', 'T2663062', '2026-63-2')}})
    where = collections.defaultdict(list)
    for m in MK['마디']:
        for q in m.get('리담') or []:
            where[q].append(m['id'])
    off = []
    for k, v in L.items():
        q = v.get('q') or uid2q.get(k)
        if v.get('마디id') not in where.get(q, []):
            off.append('%s(%s) 표 %s · 앱 %s' % (k, q, v.get('마디id'), '/'.join(where.get(q, [])) or '마디 없음'))
    N('7', '이미 있는 34 — 표의 마디 ≠ 지금 리담 마디 %d(옮기지 않음 · 목록)' % len(off), off)
    unplaced = sorted({(v.get('q') or uid2q.get(k)) for k, v in L.items() if not where.get(v.get('q') or uid2q.get(k))})
    N('7', '이미 있는 34 — 문항이 마디에 붙어 단원 줄에 선 것 %d 칸 · 마디에 안 붙은 문항(미분류 문항 카드 · 기출뷰) %d 칸 = 문항 %s'
      % (sum(1 for k, v in L.items() if where.get(v.get('q') or uid2q.get(k))), sum(1 for k, v in L.items() if not where.get(v.get('q') or uid2q.get(k))), unplaced), '')


# ══════════ 앱 관문 ══════════
def samples(p):
    J = jl(os.path.join(_DATA, 'jimun_7pan.json'))
    by = {z['id']: z for z in J['지문']}
    return {'고침': by['P7-0118']['uid'], '답': by['P7-0826']['uid'], '없음': by['P7-0595']['uid'], '새': by['P8-0001']['uid']}


def g_a5(p, b, eng):
    """§B-5 표시 — 표본 넷 · 「8판 고침」 누름 → 7판 글 · 옛 풀이 기록 「7판 글」"""
    G = 'a5'
    S = samples(p)
    want = {'고침': ('8판 고침', 'p8c g', 'BUTTON', GRAY), '답': ('8판 고침 · 답 O→X', 'p8c r', 'BUTTON', RED), '없음': ('8판에 없음', 'p8c g', 'SPAN', GRAY), '새': ('8판 새', 'p8c n', 'SPAN', GREEN)}
    heads = {}
    for nm, k in S.items():
        go_key(p, k)
        h = p.ev("k=>__P8.head(k)", k)
        heads[nm] = h
        w = want[nm]
        c = (h or {}).get('p8') or []
        good = bool(h) and len(c) == 1 and c[0]['t'] == w[0] and c[0]['cls'] == w[1] and c[0]['tag'] == w[2] and c[0]['color'] == w[3] \
            and c[0]['fs'] == '11px' and c[0]['fw'] == '700' and c[0]['bg'] == 'rgba(0, 0, 0, 0)' and c[0]['bw'] == '0px' and c[0]['vis'] \
            and h['iMc'] >= 0 and c[0]['idx'] == h['iMc'] + 1 and c[0]['idx'] < h['iTags']
        extra = ''
        if nm == '새':
            good = good and h['book'] == 'H8 p.5 14번' and h['src'] == '미기출' and h['qexp'] == 'H8'
            extra = ' · 책번호 자리 「H8 p.5 14번」 · 출처 칩 「미기출」 · 접기 칩 「H8」'
        T(G, '%s %s(%s) — 「%s」 %s · 11px 700 · 바탕 없음 · 테 0 · 칩 줄 끝(🃏 바로 뒤 · 태그 칸 앞)%s' % (eng, nm, k, w[0], w[3], extra), good, h)
        if SHOTS and eng == 'chromium':
            box = p.ev("k=>__P8.shotBox(k)", k)
            if box:
                os.makedirs(SHOTS, exist_ok=True)
                p.pg.screenshot(path=os.path.join(SHOTS, '%s_%s_%s.png' % (eng, nm, k)), clip={'x': box['x'], 'y': box['y'], 'width': box['w'], 'height': box['h']})
    hb = {}
    for nm, k in S.items():
        sel = go_key(b, k)
        hb[nm] = (b.ev("k=>__P8.head(k)", k) or {}).get('p8') if sel else '카드 없음'
    T(G + '-헛', '%s 헛잣대 바탕 — 표본 넷 모두 8판 글자 없음(새 카드는 카드 없음)' % eng, all(v in ([], None, '카드 없음') for v in hb.values()), hb)
    # 누름 — 마우스 · 손가락(Chromium CDP r22 · WebKit touchscreen.tap)
    k = S['고침']
    J = jl(os.path.join(_DATA, 'jimun_7pan.json'))
    t7 = P8A.p7text(next(z for z in J['지문'] if z['uid'] == k)['판8']['t7'])
    for how in ('mouse', 'touch'):
        go_key(p, k)
        at = p.ev("k=>__P8.p8At(k,'8판 고침')", k)
        p.press(at, how, 600)
        r1 = p.ev("k=>__P8.t7Row(k)", k)
        if SHOTS and eng == 'chromium' and how == 'mouse':
            box = p.ev("k=>__P8.shotBox(k)", k)
            if box:
                p.pg.screenshot(path=os.path.join(SHOTS, '%s_고침_펼침_%s.png' % (eng, k)), clip={'x': box['x'], 'y': box['y'], 'width': box['w'], 'height': box['h']})
        at2 = p.ev("k=>__P8.p8At(k,'8판 고침')", k)
        p.press(at2, how, 600)
        r2 = p.ev("k=>__P8.t7Row(k)", k)
        T(G, '%s 「8판 고침」 %s 누름 → 칩 줄 바로 아래 흐린 줄 「7판 글 …」(7판 글 = 판8.t7) 보임 · 한 번 더 → 접힘' % (eng, '마우스' if how == 'mouse' else '손가락'),
          bool(at and at.get('on') and r1 and r1['vis'] and r1['afterHead'] and r1['lab'] == '7판 글' and P8A.ws(t7)[:60] in P8A.ws(r1['t']) and r1['color'] == GRAY and at2 and r2 is None),
          {'누름 자리': at, '펼침': r1, '다시 누른 뒤': r2})
    # 옛 풀이 기록 「7판 글」 — 심은 기록(인도 시각 앞 · 뒤) · 실제 기록은 데이터 관문 §B-2 가 잰다
    k = S['답']
    res = {}
    for nm, ts in (('앞', '2026-09-01T00:00:00.000Z'), ('뒤', '2026-12-31T00:00:00.000Z'), ('없음', None)):
        p.ev("([k,r])=>__P8.seedOx(k,r)", [k, {'p': 'O', 'ok': False, 'm': 'O', 'ts': ts} if ts else None])
        go_key(p, k)
        res[nm] = [c['t'] for c in ((p.ev("k=>__P8.head(k)", k) or {}).get('p8') or [])]
    T(G, '%s 답 바뀜 카드 옛 풀이 기록 — 인도 시각(P8_AT %s) 앞 풀이 = 「7판 글」 회색 곁 표시 · 뒤 풀이·기록 없음 = 없음' % (eng, p.ev("()=>__P8.p8at()")),
      res['앞'] == ['8판 고침 · 답 O→X', '7판 글'] and res['뒤'] == ['8판 고침 · 답 O→X'] and res['없음'] == ['8판 고침 · 답 O→X'], res)


def g_a6(p, b, eng):
    """§B-6 단원 줄 — 1.2 국제조약 (미수록) +3 · 본편 0 · 편 머리 · 서랍 · 히트맵 한 함수"""
    G = 'a6'
    NEWJ = jl(os.path.join(_DATA, 'jimun_7pan.json'))
    MK = jl(os.path.join(_DATA, 'mokcha_병합.json'))
    pyeon = {}
    for m in MK['마디']:
        for i in m['지문']:
            if i.startswith('P8-'):
                pyeon[i] = str(m['no']).split('.')[0]
    want_x = collections.Counter(pyeon.values())
    want_x['8'] -= 1   # P7-1207 TJ161207 「16 사법」 = 기타 · 8.3.2.5
    want_g = collections.Counter({'9': -1})   # P7-1599 TH111599 「11 변리」 = 기출 · 9.2.2

    def triple(q):
        h = q.ev("()=>__UZ.hm()") or {}
        out = {}
        for c in h.get('chips') or []:
            m = re.match(u'^(\\d+)\\. (.+?) ([\\d,]+)$', c.get('t') or '')
            if not m or c.get('gk'):
                continue
            no = m.group(1)
            dh = q.ev("n=>__UZ.drawerHead(n)", no + '. ' + m.group(2))
            if dh is None:
                dh = q.ev("n=>__UZ.drawerTop(n)", int(no))
            out[no] = [int(m.group(3).replace(',', '')), q.ev("n=>__UZ.cardTot(n)", int(no)), dh]
        return out
    res = {}
    for gk in ('g', 'x'):
        home(p, gk); nf = (p.ev("()=>__HM.firstScreenCounts()") or {}).get('map') or {}; tn = triple(p)
        home(b, gk); bf = (b.ev("()=>__HM.firstScreenCounts()") or {}).get('map') or {}; tb = triple(b)
        res[gk] = {'u12': [bf.get('1.2 국제조약 (미수록)'), nf.get('1.2 국제조약 (미수록)')], 'b12': [bf.get('1.2 국제조약'), nf.get('1.2 국제조약')],
                   'diff': {k: tn[k][1] - tb[k][1] for k in tn if k in tb and tn[k][1] is not None and tb[k][1] is not None and tn[k][1] != tb[k][1]},
                   'bad': {k: v for k, v in tn.items() if not (v[0] == v[1] == v[2])}, 'n편': len(tn)}
    x, g = res['x'], res['g']
    T(G, '%s 기타 — 첫 화면 「1.2 국제조약 (미수록)」 = 바탕 + 3(8판 p.5 14번 · 유제 · 15번) · 본편 「1.2 국제조약」 무변' % eng,
      x['u12'][1] is not None and (x['u12'][1] - (x['u12'][0] or 0)) == 3 and x['b12'][0] == x['b12'][1], x)
    T(G, '%s 기출 — 새 카드 0(8판 새 = [미기출] = 기타) · (미수록) · 본편 무변' % eng, g['u12'][0] == g['u12'][1] and g['b12'][0] == g['b12'][1], g)
    dx = {k: v for k, v in want_x.items() if v}
    T(G, '%s 편 머리(카드 「총 N」) 바뀜 — 기타 = 새 19 − 지운 기타 1(P7-1207 「16 사법」 8편) = +18 %s · 기출 = 지운 기출 1(P7-1599 「11 변리」 9편) = −1 · 칩 = 카드 = 서랍(한 함수) 편 전부'
      % (eng, json.dumps(dx, ensure_ascii=False)), x['diff'] == dx and g['diff'] == dict(want_g) and not x['bad'] and not g['bad'] and x['n편'] > 10,
      {'기타 바뀜': x['diff'], '기출 바뀜': g['diff'], '어긋남': [x['bad'], g['bad']]})
    cn = p.ev("()=>__P8.census()")
    T(G, '%s 줄 셈 — 새 카드는 본편(b) 0 · 깊은 본편 0 · (미수록)(u) 19 · 편 깊이 (미수록) 19' % eng, bool(cn) and cn['b'] == 0 and cn['deepB'] == 0 and cn['u'] == 19 and cn['deepU'] == 19, cn)
    # 누름 — 첫 화면 줄 → 그 줄 카드(8판 차례 · 책번호 자리)
    home(p, 'x')
    at = p.ev("()=>__UZ.rowAt('1.2 국제조약 (미수록)')")
    p.click(at, 1500)
    mok = p.ev("()=>S.mok")
    cs = p.ev("()=>__P8.unitCards()") or []
    top = cs[:3]
    T(G, '%s 「1.2 국제조약 (미수록)」 마우스 누름 → 그 줄(~u) · 앞 셋 = 8판 새 카드(T8N0001~3 · 「H8 p.5 14번」 「H8 p.5 유제」 「H8 p.5 15번」 · 「8판 새」)' % eng,
      bool(at and at.get('on')) and bool(mok) and mok.endswith('~u') and [c['k'] for c in top] == ['T8N0001', 'T8N0002', 'T8N0003']
      and [c['book'] for c in top] == ['H8 p.5 14번', 'H8 p.5 유제', 'H8 p.5 15번'] and all(c['p8'] == ['8판 새'] for c in top), {'누름': at, 'mok': mok, '카드': cs[:6]})
    if SHOTS and eng == 'chromium':
        os.makedirs(SHOTS, exist_ok=True)
        p.pg.evaluate("()=>window.scrollTo(0,0)")
        p.pg.screenshot(path=os.path.join(SHOTS, '%s_1.2_미수록.png' % eng))
    home(b, 'x')
    atb = b.ev("()=>__UZ.rowAt('1.2 국제조약 (미수록)')")
    if atb:
        b.click(atb, 1500)
    csb = b.ev("()=>__P8.unitCards()") or []
    T(G + '-헛', '%s 헛잣대 바탕 — 기타 첫 화면에 「1.2 국제조약 (미수록)」 줄 자체가 없다(있으면 그 줄 카드에 T8N 0)' % eng,
      (atb is None) or (bool(atb.get('on')) and not any(c['k'].startswith('T8N') for c in csb)), {'누름': atb, '카드': csb[:4]})


def g_a7(p, b, eng):
    """§B-7 이미 있는 34 — 표본 셋 「H8 p.N N번」(★ revfix0928pm A-2 — 판 이름 칩 H8 · 옛 「8판 p.N」) · 기출뷰 지문 칸 · 문항 머리 · 단원 리담 카드"""
    G = 'a7'
    L = jl(os.path.join(_DATA, 'jimun_7pan.json')).get('판8_리담') or {}
    lab = lambda v: 'H8 p.%s %s' % (v['p8'], v['no8'] if '유제' in v['no8'] else v['no8'] + '번')
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        home(q)
        q.ev("y=>{S.exvPg={};return __HM.gi(y)}", '2026')
        q.pg.wait_for_timeout(900)
        got = {}
        for pg in range(6):
            for k in ('T2663014', 'T2663062'):
                if k not in got:
                    v = q.ev("k=>__P8.exvBox(k)", k)
                    if v:
                        got[k] = v
            if '2026-63-2' not in got:
                v = q.ev("u=>__P8.exvHead(u)", (L.get('2026-63-2') or {}).get('uids', ['?'])[0])   # 선지 uid 로 그 문항(리담 id 번호 ≠ 시험문번)
                if v:
                    got['2026-63-2'] = v
            if len(got) == 3:
                break
            nb = q.ev("()=>__UZ.exvNext()")
            if not nb:
                break
            q.click(nb, 1200)
        q.ev("()=>{S.jimunTab='ox';S.exvPg={}}")
        unit = {}
        for k in ('T2663014', 'T2663062'):
            if go_key(q, k):
                unit[k] = q.ev("k=>__P8.lid(k)", k)
        res[who] = {'기출뷰': got, '단원': unit}
    n = res['NEW']
    w = {k: lab(L[k]) for k in ('T2663014', 'T2663062', '2026-63-2')}
    ok = all([c['t'] for c in (n['기출뷰'].get(k) or {}).get('p8', [])] == [w[k]] for k in ('T2663014', 'T2663062')) \
        and [c['t'] for c in (n['기출뷰'].get('2026-63-2') or {}).get('p8', [])] == [w['2026-63-2']] and (n['기출뷰'].get('2026-63-2') or {}).get('boxP8') == 0 \
        and all(c['color'] == GRAY and c['vis'] for k in n['기출뷰'] for c in n['기출뷰'][k]['p8']) \
        and all([c['t'] for c in (n['단원'].get(k) or {}).get('p8', [])] == [w[k]] and all(c['afterMc'] and c['color'] == GRAY for c in n['단원'][k]['p8']) for k in ('T2663014', 'T2663062'))
    T(G, '%s 이미 있는 34 표본 셋 — 기출뷰 2026 지문 칸 T2663014 「%s」 · T2663062 「%s」 · 2026-63-2 문항 머리 「%s」(지문 칸엔 없음) · 단원 리담 카드 칩 줄 끝(🃏 뒤) 같은 글 · 회색'
      % (eng, w['T2663014'], w['T2663062'], w['2026-63-2']), ok, n)
    bb = res['BASE']
    T(G + '-헛', '%s 헛잣대 바탕 — 셋 모두 8판 글자 없음' % eng, not any(v.get('p8') for v in bb['기출뷰'].values()) and not any((v or {}).get('p8') for v in bb['단원'].values()) and len(bb['기출뷰']) == 3, bb)


def g_a8(p, b, eng):
    """지시서 밖 — 8판 새 카드에 「제7판」 글이 붙던 자리(접기 칩 · 펼친 출처 줄 · 풀 이름 · 검색 줄 · 정리 창 번호)"""
    G = 'a8'
    k = 'T8N0001'
    go_key(p, k)
    at = p.ev("k=>__P8.qexpAt(k)", k)
    p.click(at, 500)
    h = p.ev("k=>__P8.head(k)", k)
    pool = p.ev("k=>__P8.pool(k)", k)
    jn = p.ev("k=>__P8.jnNo(k)", k)
    wh = p.ev("k=>__P8.cfWhere(k)", k)
    home(p, 'x')
    sr = p.ev("q=>__P8.search(q)", '특허권 속지주의는 특허권 효력 발생지')
    T(G, '%s 8판 새 카드 — 접기 칩 「H8」 · 펼친 출처 줄 「H8 p.5 14번 · 해례 8판에만 있는 지문」 · 풀 이름 「H8 p.5」 · 정리 창 번호 「H8 p.5 14번」 · 1차객 🔍 검색 줄 머리 「H8 p.5 · 1.2 국제조약 (미수록)」(「제7판」 0) · 연결 창 자리 「특허법 · 1.2 국제조약 (미수록)」' % eng,
      bool(h) and h['qexp'] == 'H8' and h['sub'] == 'H8 p.5 14번 · 해례 8판에만 있는 지문' and (pool or {}).get('name') == 'H8 p.5' and jn == 'H8 p.5 14번'
      and bool(sr) and any(x.startswith('H8 p.5 · 1.2 국제조약 (미수록)') for x in sr) and not any('제7판' in x and '속지주의는' in x for x in sr) and wh == '특허법 · 1.2 국제조약 (미수록)',
      {'접기': (h or {}).get('qexp'), '출처 줄': (h or {}).get('sub'), '풀': pool, '정리 번호': jn, '연결 창 자리': wh, '검색': sr})
    home(b, 'x')
    srb = b.ev("q=>__P8.search(q)", '특허권 속지주의는 특허권 효력 발생지')
    T(G + '-헛', '%s 헛잣대 바탕 — 그 글 검색 줄 없음 · 풀에 T8N0001 없음' % eng, not any('속지주의는' in x for x in (srb or [])) and not b.ev("k=>__P8.pool(k)", k), srb)
    # 지운 둘 — 풀·P7map 에 없음(검색·서랍·히트맵 셈은 §B-6 이 잰다)
    gone = p.ev("ids=>ids.map(i=>[i,!!(VJ.P7map||{})[i]])", DEL_ID)
    pool2 = p.ev("us=>us.map(u=>[u,!!(OXPOOL||{})[u]])", DEL_UID)
    home(p, 'x')
    s1 = p.ev("q=>__P8.search(q)", '특허물건의 생산이 국외에서만 일어나는 경우에도')
    home(b, 'x')
    s1b = b.ev("q=>__P8.search(q)", '특허물건의 생산이 국외에서만 일어나는 경우에도')
    gb = b.ev("ids=>ids.map(i=>[i,!!(VJ.P7map||{})[i]])", DEL_ID)
    T(G, '%s 지운 둘 — 앱 원장 표(P7map)·풀 0 · P7-1207 글 검색 「제7판」 줄 0' % eng,
      not any(v for _, v in gone) and not any(v for _, v in pool2) and not any(x.startswith('제7판') for x in (s1 or [])), {'P7map': gone, '풀': pool2, '검색': s1})
    T(G + '-헛', '%s 헛잣대 바탕 — 있음 · 검색 「제7판 16 사법」 줄' % eng, all(v for _, v in gb) and any(x.startswith('제7판') for x in (s1b or [])), {'P7map': gb, '검색': s1b})


BR = {}
PARTS = [('a5', g_a5), ('a6', g_a6), ('a7', g_a7), ('a8', g_a8)]
DPARTS = [('d1', d_b1), ('d2', d_b2), ('d3', d_b3), ('d4', d_b4), ('d5', d_b5), ('d7', d_b7)]


def run_engine(pw, eng):
    br = getattr(pw, eng).launch()
    BR[eng] = br
    ns, nd, ne = M.new_env()
    bs, bd, be = M.base_env()
    try:
        p = Pg(br, eng, 'p8N', ns, nd, ne)
        b = Pg(br, eng, 'p8B', bs, bd, be)
        try:
            for k, fn in PARTS:
                if ONLY and k not in ONLY:
                    continue
                print('── %s · %s' % (eng, k), flush=True)
                try:
                    fn(p, b, eng)
                except Exception as e:
                    T('RUN', u'%s · %s 묶음이 멈춤' % (eng, k), False, repr(e)[:600])
            T('ERR', u'%s — NEW 앱 오류 0' % eng, not p.errs_all(), p.errs_all()[:6])
        finally:
            p.close(); b.close()
    finally:
        br.close()


def main():
    shutil.rmtree(os.path.join(M.WORK, 'head'), ignore_errors=True)   # 바탕 = 지금 HEAD 를 늘 새로 푼다(낡은 캐시 금지)
    os.makedirs(M.WORK, exist_ok=True)
    t0 = time.time()
    for k, fn in DPARTS:
        if not ONLY or k in ONLY:
            try:
                fn()
            except Exception as e:
                T('RUN', u'%s 데이터 묶음이 멈춤' % k, False, repr(e)[:600])
    if not ONLY or any(k in ONLY for k, _ in PARTS):
        with sync_playwright() as pw:
            for eng in ENGS:
                RES.append(('ENG', eng, None, ''))
                run_engine(pw, eng)
    npass = sum(1 for r in RES if r[2] is True); nfail = sum(1 for r in RES if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · %s · NEW %s · 데이터 %s · 바탕 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), 'p8up', os.path.basename(_NEW), _DATA,
                M.git('rev-parse', '--short', M.BASE_REV).decode().strip(), ','.join(ENGS)))   # A-6(d) 적히는 바탕 = 실제 바탕
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[ok], g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:900]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
