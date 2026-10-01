# -*- coding: utf-8 -*-
r"""_task_jo_gaek_uid_add3 §B 관문 하네스 — 해마다 20문항(시험문번 모름 11 가르기 · 빠진 시험 문번 새 문항)

  python _harness_jo_uid_add3.py --new <앱> [--data <jo/data>] [--exam <gichul/pdf>] [--res <결과>] [--eng chromium,webkit] [--only d1,..,a1,..]

  NEW  = 이 판 앱 + 이 판 데이터 · BASE = genie HEAD(바로 앞 인도판) 앱 + 데이터 — 칸마다 헛잣대(바탕에서 FAIL)
         바탕이 원래 통과하는 칸(무변 등)은 「일부러 깨뜨린 사본」을 헛잣대로 쓴다 · 옮기기 헛잣대 = 바탕 앱 + 새 데이터
  누름 = 진짜 포인터(page.mouse · 손가락 = Chromium CDP 터치 r22 · WebKit touchscreen.tap) · 보임 = display ≠ none · 높이 > 0 · 자리 = elementFromPoint
  원장 = N: 특상디\_1차객_원장.csv(헛잣대 = N: 저장소 HEAD 판)
  ⚠ 지시서 §B 는 「_harness_jo_gaek_uid.py 에 더함」 — 그 하네스는 바탕이 a9d72c1 로 박혀 있고 Chromium 전용이라 두 엔진 · 바로 앞 인도판 바탕으로 따로 세웠다(보고에 적음).
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import io, json, os, re, sys, time, csv, copy, shutil, subprocess, collections
sys.stdout.reconfigure(encoding='utf-8')
csv.field_size_limit(10 ** 9)
HERE = os.path.dirname(os.path.abspath(__file__))
JOP = os.path.dirname(HERE)


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


_NEW = ARG('--new')
_DATA = ARG('--data', _roots.genie(r'jo\data'))
_EXAM = ARG('--exam', _roots.genie(r'gichul\pdf'))
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_uid_add3_result.txt'))
LED = os.path.join(JOP, u'특상디', u'_1차객_원장.csv')
NGIT = ['git', '-c', 'core.quotepath=false', '--git-dir=' + os.path.join(os.path.dirname(os.path.dirname(JOP)), 'claude-git')]
sys.argv = [sys.argv[0], '--new', _NEW, '--data', _DATA, '--base', 'fb89ad2', '--exam', _EXAM]   # A-6(d) 9/30 — 바탕 = 인도 때 HEAD fb89ad2(결과 머리 「바탕 HEAD fb89ad2」) · HEAD 면 인도 뒤 헛잣대가 거꾸로 FAIL
sys.path.insert(0, HERE)
sys.path.insert(0, JOP)
import _harness_jo_gaek_mbsame as M   # noqa: E402
from playwright.sync_api import sync_playwright   # noqa: E402
M.TESTS = M.TESTS + '\n' + io.open(os.path.join(HERE, '_harness_jo_uidmbs2_tests.js'), encoding='utf-8').read() \
    + '\n' + io.open(os.path.join(HERE, '_harness_jo_uid_add3_tests.js'), encoding='utf-8').read()
M.WORK = M.WORK + '_u3'
RES = []
# §A-1 가름(쪽 그림 확인 · _decisions 9/28 14:25) — 문항 id → (연도, 회차, 시험문번)
SEAT = {'2009-46-1': ('2009', '46', '4'), '2009-46-4': ('2009', '46', '14'), '2009-46-11': ('2009', '46', '3'),
        '2010-47-6': ('2010', '47', '4'), '2012-49-16': ('2012', '49', '20'),
        '2011-48-12': ('2013', '50', '3'), '2018-55-1': ('2020', '57', '7'), '2022-59-2': ('2018', '55', '13')}
UNRES = ['2010-47-5', '2010-47-18', '2020-57-20']
UIDRX = re.compile(u'^T\\d{6}[1-5ㄱ-ㅂ]$')


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def jl(p):
    return json.loads(open(p, 'rb').read().decode('utf-8'))


# ══════════ 데이터 관문 ══════════
def base_data():
    _, bd, _ = M.base_env()
    return bd


def seats(J):
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    for q in J['문제']:
        if q.get('시험문번'):
            by[str(q['연도'])][str(q['시험문번'])].append(q['id'])
    miss = {y: [n for n in range(1, 21) if str(n) not in by[str(y)]] for y in range(2008, 2027)}
    dup = {y: {n: v for n, v in by[str(y)].items() if len(v) > 1} for y in range(2008, 2027)}
    return {y: v for y, v in miss.items() if v}, {y: v for y, v in dup.items() if v}


def d1():
    """§B-1 해마다 시험문번 1~20 빠짐없이 한 번씩(2008~2026)"""
    G = 'd1'
    nj = jl(os.path.join(_DATA, 'jimun_특허.json'))
    bj = jl(os.path.join(base_data(), 'jimun_특허.json'))
    m, d = seats(nj)
    T(G, '2008~2026 해마다 시험문번 1~20 이 한 번씩 — 빠짐 0 · 겹침 0', not m and not d, {'빠짐': m, '겹침': d})
    bm, bdp = seats(bj)
    nb = sum(len(v) for v in bm.values())
    T(G + '-헛', '헛잣대 바탕 — 빠짐 36(지시서 §0)', nb == 36, {'빠짐 수': nb, '빠짐': bm})


def d2():
    """§B-1 기존 문항 행 — 시험 자리를 채운 여덟 머리 칸(시험문번 · giOld · 연도·회차) 말고 무변"""
    G = 'd2'
    nj = jl(os.path.join(_DATA, 'jimun_특허.json'))
    bj = jl(os.path.join(base_data(), 'jimun_특허.json'))

    def check(A, B):
        bad, moved = [], {}
        Bi = {q['id']: q for q in B['문제']}
        for q in A['문제']:
            x = Bi.get(q['id'])
            if x is None:
                bad.append((q['id'], '없어짐')); continue
            ks = sorted(k for k in set(q) | set(x) if q.get(k) != x.get(k))
            if not ks:
                continue
            if q['id'] in SEAT and set(ks) <= {'시험문번', 'giOld', '연도', '회차'}:
                moved[q['id']] = ks; continue
            bad.append((q['id'], ks))
        return bad, moved
    nj_d = json.loads(M.git('show', 'e36829b:jo/data/jimun_특허.json').decode('utf-8'))   # A-6(d) 9/30 — 이 항목(인도 검산)만 새 쪽 = uid_add3 인도 커밋 e36829b(뒤 판 revfix0928night A-7 정답 넷 · revfix0929 A-3 정답 둘이 지금 문항 행을 바꿈) · 아래 d2-헛 사본은 지금 데이터(nj) 그대로
    bad, moved = check(bj, nj_d)
    T(G, '바탕 문항 %d 행 — 가른 여덟(%s)만 머리 칸이 바뀌고 나머지 바이트 무변(지문 · uid · id 포함)' % (len(bj['문제']), ' · '.join(sorted(moved))),
      not bad and sorted(moved) == sorted(SEAT), {'바뀐 여덟': moved, '어긋남': bad[:6]})
    brk = copy.deepcopy(nj)
    for q in brk['문제']:
        if q['id'] == '2015-52-3':
            q['지문'][0]['t'] = q['지문'][0]['t'] + ' '
            break
    bad2, _ = check(bj, brk)
    T(G + '-헛', '헛잣대 — 일부러 기존 문항 지문 한 글자를 바꾼 사본이면 잡힌다', bool(bad2), bad2[:2])


def d3():
    """§A-1 가름 — 여덟은 시험지 자리 · 셋은 문번 빈 채(목록) · 옛 기록 열쇠 giOld"""
    G = 'd3'
    nj = jl(os.path.join(_DATA, 'jimun_특허.json'))
    Q = {q['id']: q for q in nj['문제']}
    got = {i: (str(Q[i]['연도']), str(Q[i]['회차']), str(Q[i]['시험문번'])) for i in SEAT if i in Q}
    old = {i: Q[i].get('giOld') for i in SEAT if i in Q}
    want_old = {i: '%s:r%s' % (i.split('-')[0], i.split('-')[2]) for i in SEAT}
    T(G, '가른 여덟 = 시험지 자리(연도·회차·시험문번) · giOld = 옛 열쇠 「<원장 해>:r<순번>」 · 연도가 틀린 셋(2011-48-12→2013 · 2018-55-1→2020 · 2022-59-2→2018)',
      got == SEAT and old == want_old, {'자리': got, 'giOld': old})
    un = {i: (Q[i].get('시험문번'), Q[i].get('giOld')) for i in UNRES if i in Q}
    T(G, '못 가른 셋(2010-47-5 · 2010-47-18 = 어느 해 시험지에도 없음 · 2020-57-20 = 2026 12번과 같은 글) — 문번 빈 채 · giOld 없음',
      len(un) == 3 and all(v == ('', None) for v in un.values()), un)
    bj = jl(os.path.join(base_data(), 'jimun_특허.json'))
    bq = {q['id']: q for q in bj['문제']}
    T(G + '-헛', '헛잣대 바탕 — 여덟 모두 시험문번 빈칸', all(not bq[i].get('시험문번') for i in SEAT), {i: bq[i].get('시험문번') for i in SEAT})


def uids(d):
    s = set()
    for q in jl(os.path.join(d, 'jimun_특허.json'))['문제']:
        for z in q['지문']:
            if z.get('uid'):
                s.add(z['uid'])
    P7 = {}
    for x in jl(os.path.join(d, 'jimun_7pan.json'))['지문']:
        if x.get('uid'):
            s.add(x['uid']); P7.setdefault(x['uid'], []).append(x['id'])
    return s, P7


def d4():
    """§A-2 새 문항 — uid 꼴 · 없어진 uid 0 · 7판 같은 uid 흡수(2017 18번)"""
    G = 'd4'
    nj = jl(os.path.join(_DATA, 'jimun_특허.json'))
    bd = base_data()
    bj = jl(os.path.join(bd, 'jimun_특허.json'))
    bi = set(q['id'] for q in bj['문제'])
    new = [q for q in nj['문제'] if q['id'] not in bi]
    nu = [z.get('uid') for q in new for z in q['지문']]
    bad = [u for u in nu if not (u and UIDRX.match(u))]
    selfdup = [q['id'] for q in new if len(set(z['uid'] for z in q['지문'])) != len(q['지문'])]
    T(G, '새 문항 28 · 지문 %d — uid 꼴 T<해2><회2><번2><선지·보기> 밖 0 · 한 문항 안 겹침 0 · 문항마다 id = <해>-<회>-B<번>' % len(nu),
      len(new) == 28 and len(nu) == 137 and not bad and not selfdup and all(re.match(r'^\d{4}-\d{2}-B\d{1,2}$', q['id']) for q in new),
      {'새 문항': len(new), '지문': len(nu), '꼴 밖': bad[:5], '안 겹침': selfdup})
    ns, P7n = uids(_DATA)
    bs, _ = uids(bd)
    T(G, '바탕 uid 가 새 데이터에서 없어짐 0(문항 JSON + 7판)', not (bs - ns), sorted(bs - ns)[:5])
    q18 = next((q for q in new if q['id'] == '2017-54-B18'), None)
    want = ['T1754181', 'T1754183', 'T1754184', 'T1754185']
    got = [z['uid'] for z in (q18 or {}).get('지문', [])]
    T(G, '흡수 — 2017 18번 선지 uid 에 7판 T1754181·183·184·185 가 그대로(7판 줄마다 하나) · ② 는 새 uid(7판 줄 없음)',
      q18 is not None and all(u in got and len(P7n.get(u, [])) == 1 for u in want) and 'T1754182' in got and 'T1754182' not in P7n,
      {'선지 uid': got, '7판': {u: P7n.get(u) for u in want + ['T1754182']}})
    T(G + '-헛', '헛잣대 바탕 — 2017-54-B18 없음', not any(q['id'] == '2017-54-B18' for q in bj['문제']), '')


def d5():
    """원장 — 새 줄(시험지 소스) · 시험자리 조각 · 정답 = 큐넷 최종정답 · 멱등(데이터 스크립트 드라이런 0)"""
    G = 'd5'
    R = list(csv.DictReader(io.open(LED, encoding='utf-8-sig')))
    add = [r for r in R if u'uid_add3(9/28) 시험지 원문' in (r[u'로그'] or '')]
    ans = {}
    for r in csv.DictReader(io.open(os.path.join(JOP, u'공통', u'_재료', u'_최종정답.csv'), encoding='utf-8-sig')):
        if r[u'법'] == u'특허' and r[u'형'] == 'A':
            ans[(r[u'연도'], r[u'문번'])] = r[u'정답']
    wrong = [(r[u'소스'], r[u'오지선다정답']) for r in add if (r[u'오지선다정답'] or u'모두정답') != ans.get((r[u'기출연도'], r[u'문번']))]
    seat = collections.Counter(re.search(u'시험자리=(\\S+?)\\(', r[u'로그']).group(1) for r in R if u'시험자리=' in (r[u'로그'] or ''))
    T(G, '원장 새 줄 167(OX 137 + 조합 선지 30) · 오지선다정답 = 큐넷 최종정답(모두정답 둘은 빈칸) · 시험자리 조각 = 여덟 문항',
      len(add) == 167 and sum(1 for r in add if r[u'형식'] == 'OX') == 137 and not wrong and len(seat) == 8,
      {'새 줄': len(add), '정답 어긋남': wrong[:5], '시험자리': dict(seat)})
    out = subprocess.run([sys.executable, os.path.join(HERE, '_uid_add3_data.py')], capture_output=True, env=dict(os.environ, PYTHONIOENCODING='utf-8')).stdout.decode('utf-8', 'replace')
    T(G, '멱등 — _uid_add3_data.py 드라이런 = 고칠 칸 0 · 새 줄 0 · 판독 덧자료 0', u'고칠 칸 0' in out and u'새 줄 0' in out and u'더할 줄 0' in out, out[-300:])
    head = subprocess.run(NGIT + ['show', 'HEAD:jopangi/특상디/_1차객_원장.csv'], capture_output=True).stdout.decode('utf-8-sig')
    hb = sum(1 for r in csv.DictReader(io.StringIO(head)) if u'uid_add3(9/28)' in (r[u'로그'] or ''))
    N(G, 'N: 저장소 HEAD 원장의 add3 줄 수(인도 전 = 0 · 인도 뒤 = 이 판)', hb)


# ══════════ 앱 관문 ══════════
class Pg(M.Pg):
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

    def reload(self):
        self.pg.goto('http://127.0.0.1:%d/index.html?tok=1&keep=1' % self.port, wait_until='load', timeout=180000)
        self.pg.wait_for_function(M.READY, timeout=180000)
        self.pg.wait_for_timeout(900)


def home(p, gk='g'):
    p.ev("l=>__HM.home(l)", '특허법')
    if p.ev("()=>__UZ.has('UZGK')"):
        p.ev("v=>__UZ.gk(v)", gk)


def go_key(p, k):
    home(p)
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


def open_card(p, k):
    """그 지문 카드를 화면에 — 단원 줄에 서면 그 줄 · 마디에 안 붙은 지문은 사람처럼 🔍 검색 줄 누름 → 지문 팝업(book8 하네스와 같은 길)"""
    if go_key(p, k) and p.ev("k=>!!document.getElementById('qb-'+k)", k):
        return 'unit'
    home(p)
    p.click(p.ev("()=>__HM.at('#slot .mbsr input')"), 200)
    p.pg.keyboard.type(k); p.pg.wait_for_timeout(800)
    row = p.ev("()=>{const r=[...document.querySelectorAll('#slot .mbres .rr')].find(x=>typeof x.onclick==='function');if(!r)return null;r.scrollIntoView({block:'center'});"
               "const b=r.getBoundingClientRect(),at=document.elementFromPoint(b.left+b.width/2,b.top+b.height/2);return {cx:b.left+b.width/2,cy:b.top+b.height/2,on:!!at&&r.contains(at)};}")
    p.click(row, 1500)
    return 'search' if row else None


def open_year(p, y, how):
    home(p)
    at = p.ev("y=>__U3.yearRow(y)", str(y))
    ok = p.press(at, how, 2500)
    p.until("()=>document.querySelectorAll('#slot .exv-q').length>0", ms=15000)
    return ok


def to_q(p, k, how, most=4):
    for _ in range(most):
        q = p.ev("k=>__U3.exvQ(k)", k)
        if q and q['vis']:
            return q
        nx = p.ev("()=>__U3.next()")
        if not p.press(nx, how, 1200):
            break
    return p.ev("k=>__U3.exvQ(k)", k)


OLDS = [('특허:%s' % ('%s:r%s' % (i.split('-')[0], i.split('-')[2])), '특허:%s:%s' % (v[0], v[2])) for i, v in SEAT.items()]


def a1(p, b, eng, br):
    """§B-2 A-1 기록 옮기기 — 옛 열쇠(심은 기록) → 새 열쇠 · 옛 열쇠 0 · 묘비 · 새 열쇠에 더 새 값이 있으면 그것 · 동기화로 되돌아온 옛 열쇠도 옮김"""
    G = 'a1'
    ns, nd, ne = M.new_env()
    bs, _, _ = M.base_env()
    seed = {o: {'p': '2', 'ts': '2026-09-01T00:00:00.000Z'} for o, k in OLDS}
    seed['특허:2009:r4'] = {'p': '2', 'ts': '2026-09-20T00:00:00.000Z'}      # 옛 값이 더 새것 → 새 열쇠를 덮는다
    seed['특허:2009:14'] = {'p': '1', 'ts': '2026-09-05T00:00:00.000Z'}
    seed['특허:2009:4'] = {'p': '5', 'ts': '2026-09-10T00:00:00.000Z'}       # 새 열쇠 값이 더 새것 → 그대로
    olds = [o for o, _ in OLDS]
    news = [k for _, k in OLDS]
    out = {}
    for tag, q in (('NEW', p), ('헛', Pg(br, eng, 'u3H', bs, nd, ne))):
        try:
            q.ev("o=>__U3.seedGi(o)", seed)
            q.reload()
            q.until("()=>{const G=giAll();return !G['특허:2011:r12']}", ms=6000)
            q.pg.wait_for_timeout(400)
            out[tag] = {'옛': q.ev("k=>__U3.gi(k)", olds), '새': q.ev("k=>__U3.gi(k)", news), '도장': q.ev("k=>__U3.stamps(k)", olds + news),
                        '토스트': q.ev("()=>__HM.toasts()"), 'seat': q.ev("()=>__U3.seat()")}
        finally:
            if q is not p:
                q.close()
    o = out['NEW']
    ok = (not any(o['옛'].values()) and all(o['새'][k] for k in news) and o['새']['특허:2009:4']['p'] == '5' and o['새']['특허:2009:14']['p'] == '2'
          and all(o['새'][k]['p'] == '2' for k in news if k not in ('특허:2009:4', '특허:2009:14'))
          and all(o['도장'][x]['gone'] for x in olds) and all(o['도장'][x]['u'] for x in news) and any(u'새 시험 자리' in t for t in o['토스트']))
    T(G, '%s 옛 열쇠 여덟(심은 기록) → 부팅 뒤 새 열쇠(법:연도:시험문번)로 · 옛 열쇠 0 · 옛 = 묘비(gone) · 새 = 씀(u) · 더 새 값 우선(2009:4 는 새 값 5 그대로 · 2009:14 는 옛 값 2) · 토스트' % eng,
      ok, {'옛': o['옛'], '새': o['새'], '토스트': o['토스트'][-2:], 'GISEAT': o['seat']})
    h = out['헛']
    T(G + '-헛', '%s 헛잣대 바탕 앱 + 새 데이터 — 옛 열쇠 그대로 남음(새 열쇠에서 기록 안 보임)' % eng, all(h['옛'].values()), {'옛': h['옛']})
    # 옛 판 기기가 옛 열쇠를 다시 올린 꼴 — 저장소에 옛 열쇠를 되살리고 동기화(가짜 원격) → 다시 옮긴다
    p.ev("o=>__U3.seedGi(o)", {'특허:2011:r12': {'p': '4', 'ts': '2026-09-28T09:00:00.000Z'}})
    p.ev("async()=>{try{await syncRecords(true);}catch(e){}}")
    p.pg.wait_for_timeout(1200)
    g2 = p.ev("k=>__U3.gi(k)", ['특허:2011:r12', '특허:2013:3'])
    T(G, '%s 동기화 뒤(옛 판 기기가 올린 옛 열쇠) — syncRecords 안에서 다시 옮김 · 새 열쇠 = 더 새 값 4' % eng,
      not g2['특허:2011:r12'] and (g2['특허:2013:3'] or {}).get('p') == '4', g2)


def a2(p, b, eng):
    """§B-3 앱 기출뷰 표본 — 2009 머리 「총 20문제」 · 10번 · 2023 15번 · 2008 4번(쪽 넘김 = 진짜 포인터)"""
    G = 'a2'
    for how in ('mouse', 'touch'):
        r = {}
        for y, n in ((2009, 10), (2023, 15), (2008, 4)):
            open_year(p, y, how)
            e = p.ev("()=>__U3.exv()")
            q = to_q(p, '특허:%d:%d' % (y, n), how)
            r['%d-%d' % (y, n)] = {'머리': e['head'][:60], '칸': q}
        ok = all(v['칸'] and v['칸']['vis'] and v['칸']['boxes'] >= 3 for v in r.values()) and u'총 20문제' in r['2009-10']['머리'] \
            and u'총 20문제' in r['2023-15']['머리'] and u'총 20문제' in r['2008-4']['머리']
        T(G, '%s %s — 첫 화면 해 줄 누름 → 기출뷰 · 2009·2023·2008 머리 「총 20문제」 · 2009 10번 · 2023 15번 · 2008 4번 문항 칸 보임(▶ 다음 쪽 누름)' % (eng, '마우스' if how == 'mouse' else '손가락'), ok, r)
    rb = {}
    for y, n in ((2009, 10), (2023, 15), (2008, 4)):
        open_year(b, y, 'mouse')
        e = b.ev("()=>__U3.exv()")
        q = to_q(b, '특허:%d:%d' % (y, n), 'mouse')
        rb['%d-%d' % (y, n)] = {'머리': e['head'][:60], '칸': q}
    T(G + '-헛', '%s 헛잣대 바탕 — 세 문항 칸 없음 · 2009 머리 「총 11문제」' % eng, all(not v['칸'] for v in rb.values()) and u'총 11문제' in rb['2009-10']['머리'], rb)


def a3(p, b, eng):
    """§B-5 채점 — 2009 전체 채점(「채점」 진짜 포인터 · confirm 스텁) → 분모 = 정답 있는 문항(새 9 모두 듦)"""
    G = 'a3'
    res = {}
    for tag, q in (('NEW', p), ('BASE', b)):
        home(q)
        q.ev("()=>{window.confirm=()=>true;}")
        n_pick = q.ev("()=>__U3.pickAll(2009)")   # 답 안 고른 문항이 있으면 새 기출뷰는 제출을 막는다(「답을 안 고른 문제 N개」)
        open_year(q, 2009, 'mouse')
        n_gr = q.ev("()=>__U3.gradable(2009)")
        for _ in range(5):   # 「전체 채점 ✓」 = 마지막 쪽에만 — 「다음 N문제 ▶」 를 진짜 포인터로 넘긴다
            if q.ev("()=>__U3.grade()"):
                break
            if not q.press(q.ev("()=>__U3.next()"), 'mouse', 1200):
                break
        q.press(q.ev("()=>__U3.grade()"), 'mouse', 1500)
        res[tag] = {'정답 있는 문항': n_gr, '심은 답': n_pick, '기록': q.ev("()=>__U3.yearOf(2009)"), '토스트': q.ev("()=>__HM.toasts()")[-1:]}
    nw = res['NEW']
    last = ((nw['기록'] or {}).get('grnd') or [{}])[-1]
    T(G, '%s 2009 채점 — 분모 %s(= 정답 있는 문항 · 새 9 모두 듦) · 회독 한 줄 n 같음 · 토스트 「2009년 0/%s 맞음」 ⚠ 20 이 아닌 까닭 = 옛 리담 넷(2009-46-1·4·6·11)이 원장 정답 빈칸(2009-46-9 = revfix0928night A-7 큐넷 정답)' % (eng, nw['정답 있는 문항'], nw['정답 있는 문항']),
      nw['정답 있는 문항'] == 16 and last.get('n') == 16 and ((nw['기록'] or {}).get('year') or {}).get('n') == 16, nw)   # A-6(a) 9/30 — _task_jo_revfix0928night.md A-7 103줄 「2009-46-9(2009 2번) 정답 = 큐넷 … → 2009 채점 분모 16」 · 결정로그 9/29 08:33
    bw = res['BASE']
    T(G + '-헛', '%s 헛잣대 바탕 — 2009 분모 6(새 문항 없음)' % eng, bw['정답 있는 문항'] == 6 and (((bw['기록'] or {}).get('grnd') or [{}])[-1]).get('n') == 6, bw)


def a4(p, b, eng):
    """§B-6 출제연도 칩 — 새 문항 지문 카드 칩 누름 → 그 해 시험지 쪽 팝업 · 가른 문항(연도 옮김)도 새 해 칩"""
    G = 'a4'
    for qid, n, rx, f in (('2009-46-B8', 1, '^2009:8:', '2009-1-teukheo'),):
        for how in ('mouse', 'touch'):
            home(p)
            k = p.ev("([i,n])=>__U3.keyOf(i,n)", [qid, n])
            via = open_card(p, k)
            c = p.ev("([k,r])=>__HM.chipAt(k,r)", [k, rx])
            clicked = p.press(c, how, 2500)
            pop = p.until("f=>{const x=__HM.pop('^cv\\\\|exam\\\\|'+f);return x&&x.canvas&&x.bdVis?x:null}", f, ms=25000)
            T(G, '%s %s %s ①(%s) — 출제연도 칩 「%s…」 누름 → %s 시험지 쪽 팝업 보임 · 문번 빨간 테' % (eng, '마우스' if how == 'mouse' else '손가락', qid, k, rx[1:], f),
              bool(k and clicked and pop and pop['vis'] and pop['bd']), {'카드': via, '칩': c and {x: c.get(x) for x in ('t', 'on', 'cls')}, '창': pop})
            p.ev("()=>__HM.closeAll()")
    # 연도를 옮긴 문항(2011-48-12 → 2013 3번)은 단원 줄에 안 붙어 있다 — 새로 선 2013 기출뷰 3번 칸의 칩으로 잰다
    for how in ('mouse', 'touch'):
        open_year(p, 2013, how)
        c = p.ev("([k,r])=>__U3.exvChip(k,r)", ['특허:2013:3', '^2013:3:'])
        clicked = p.press(c, how, 2500)
        pop = p.until("f=>{const x=__HM.pop('^cv\\\\|exam\\\\|'+f);return x&&x.canvas&&x.bdVis?x:null}", '2013-1-teukheo', ms=25000)
        T(G, '%s %s 2011-48-12(연도 옮김) — 2013 기출뷰 3번 칸 출제연도 칩 「2013:3:…」 누름 → 2013-1-teukheo 시험지 쪽 팝업 보임 · 문번 빨간 테' % (eng, '마우스' if how == 'mouse' else '손가락'),
          bool(clicked and pop and pop['vis'] and pop['bd']), {'칩': c, '창': pop})
        p.ev("()=>__HM.closeAll()")
    home(b)
    kb = b.ev("([i,n])=>__U3.keyOf(i,n)", ['2011-48-12', 1])
    go_key(b, kb)
    cb = b.ev("([k,r])=>__HM.chipAt(k,r)", [kb, '^2013:3:'])
    kn = b.ev("([i,n])=>__U3.keyOf(i,n)", ['2009-46-B8', 1])
    T(G + '-헛', '%s 헛잣대 바탕 — 2009-46-B8 없음 · 2011-48-12 카드에 「2013:3:」 칩 없음' % eng, kn is None and not cb, {'2009-46-B8': kn, '2013 칩': cb, 'chips': b.ev("k=>__HM.chips(k)", kb)})


def a5(p, b, eng):
    """§B-4 흡수 — 2017 18번 ①③④⑤ = 7판 T1754181·183·184·185 한 카드(같은 uid 카드 둘 없음) · ② = 따로"""
    G = 'a5'
    home(p)
    ab = {x['n']: x for x in (p.ev("i=>__U3.absorbed(i)", '2017-54-B18') or [])}
    k = p.ev("([i,n])=>__U3.keyOf(i,n)", ['2017-54-B18', 1])
    go_key(p, k)
    cnt = {u: p.ev("u=>__U3.uidCards(u)", u) for u in ('T1754181', 'T1754183', 'T1754184', 'T1754185')}
    ok = len(ab) == 5 and all(ab[s].get('cls') == 'a' and ab[s].get('p7') for s in '1345') and ab['2'].get('cls') != 'a' and not ab['2'].get('p7') \
        and all(v <= 1 for v in cnt.values()) and sum(cnt.values()) >= 1
    T(G, '%s 2017 18번 — ①③④⑤ 흡수(cls a · 7판 줄 있음) · ② 따로(7판 줄 없음) · 그 마디 쪽에 같은 uid 카드 둘 없음' % eng, ok, {'흡수': ab, '같은 uid 카드': cnt})
    home(b)
    bb = b.ev("i=>__U3.absorbed(i)", '2017-54-B18')
    T(G + '-헛', '%s 헛잣대 바탕 — 2017-54-B18 문항 없음' % eng, bb is None, bb)


BR = {}
PARTS = [('a1', a1), ('a2', a2), ('a3', a3), ('a4', a4), ('a5', a5)]
DPARTS = [('d1', d1), ('d2', d2), ('d3', d3), ('d4', d4), ('d5', d5)]


def run_engine(pw, eng):
    br = getattr(pw, eng).launch()
    BR[eng] = br
    ns, nd, ne = M.new_env()
    bs, bd, be = M.base_env()
    try:
        p = Pg(br, eng, 'u3N', ns, nd, ne)
        b = Pg(br, eng, 'u3B', bs, bd, be)
        try:
            for k, fn in PARTS:
                if ONLY and k not in ONLY:
                    continue
                print('── %s · %s' % (eng, k), flush=True)
                try:
                    fn(p, b, eng, br) if k == 'a1' else fn(p, b, eng)
                except Exception as e:
                    T('RUN', u'%s · %s 묶음이 멈춤' % (eng, k), False, repr(e)[:600])
            T('ERR', u'%s — NEW 앱 오류 0' % eng, not p.errs_all(), p.errs_all()[:6])
        finally:
            p.close(); b.close()
    finally:
        br.close()


def main():
    shutil.rmtree(os.path.join(M.WORK, 'head'), ignore_errors=True)
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
        f.write('\n==== %s · %s · NEW %s · 데이터 %s · 바탕 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), 'uid_add3', os.path.basename(_NEW), _DATA,
                M.git('rev-parse', '--short', M.BASE_REV).decode().strip(), ','.join(ENGS)))   # A-6(d) 적히는 바탕 = 실제 바탕
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[ok], g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:900]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
