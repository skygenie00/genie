# -*- coding: utf-8 -*-
"""_task_jo_gichul_q_uid 관문 (§D) — 빌드 산출 JSON 을 읽어 잰다.

    PYTHONIOENCODING=utf-8 python _harness_gichul_q_uid.py [--before <옛 리스트.json>]

⚠ 앱을 안 띄운다. 재는 것은 **데이터**다 — 「가리키는 문제가 참인가」·「no 가 그 문항의
   시험문번인가」·「원장짝없음 수」·「빠진 것 0」·「멱등」·헛잣대.
재료 = 빌드 산출(`%LOCALAPPDATA%\\jopangi\\_out\\data`) · 원장 CSV · 문항 JSON.
"""
import collections
import csv
import hashlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'jopangi', '_out', 'data')
LEDGER = os.path.join(os.path.dirname(os.path.dirname(HERE)), '특상디', '_1차객_원장.csv')   # 9/23 — 하네스는 공통\_harness\ · 원장은 특상디\
BEFORE = sys.argv[sys.argv.index('--before') + 1] if '--before' in sys.argv else None
GA = {'특허': '특', '상표': '상', '디보': '디', '민소': '민'}

R = []
def T(g, n, ok, got=''):
    R.append((g, n, bool(ok), str(got)[:200]))


def load(law, path=None):
    p = path or os.path.join(OUT, 'prec_%s_리스트.json' % law)
    if not os.path.isfile(p):
        return None
    return json.load(io.open(p, encoding='utf-8'))


def qjson(law):
    p = os.path.join(OUT, 'jimun_%s.json' % law)
    if not os.path.isfile(p):
        return None
    return json.load(io.open(p, encoding='utf-8'))


TOKMAP = {}


def tok_build(law):
    """빌드의 `to_id` 는 **판례 목록으로 지은 토큰 표**를 쓴다 — 연도 자릿수를 손으로 늘리지 않는다.
       하네스가 정규식으로 흉내 내면 `99후628` 을 `1999후628` 로 바꿔 짝을 통째로 놓친다
       (2026-09-21 실측 — 상표 1건이 거짓으로 찍혔다). 목록에서 그대로 지어 쓴다."""
    if law in TOKMAP:
        return TOKMAP[law]
    M = {}
    d = load(law) or {}
    for r in (d.get('판례') or []):
        for t in [r.get('id'), r.get('사건번호')] + list(r.get('별칭') or []):
            if t:
                M[str(t).strip()] = r['id']
    TOKMAP[law] = M
    return M


def to_id(s, law='특허'):
    return tok_build(law).get(str(s).strip(), '')



def truth(law):
    """ⓐ 원장 `판례` 열 uid · ⓑ 지문 `pan` · ⓒ 볼트 코드 (회차, 문번) 로 이은 문항 id."""
    J = qjson(law)
    uid2q, byid = {}, {}
    if J:
        for q in J.get('문제', []):
            qi = {'yr': str(q.get('연도')), 'id': str(q.get('id')), 'rd': str(q.get('회차') or ''),
                  'no': str(q.get('시험문번') or '')}
            byid[qi['id']] = qi
            for z in q.get('지문', []):
                if z.get('uid'):
                    uid2q[str(z['uid'])] = qi
    A, B, ledk = collections.defaultdict(set), collections.defaultdict(set), {}
    if os.path.isfile(LEDGER):
        with io.open(LEDGER, encoding='utf-8-sig', newline='') as fh:
            for row in csv.DictReader(fh):
                if row.get('과목') != law:
                    continue
                u = str(row.get('uid') or '').strip()
                rd = str(row.get('회차') or '').strip()
                if u and rd:
                    ledk.setdefault((rd, str(row.get('문번') or '').strip()), u)
                if not row.get('판례'):
                    continue
                q = uid2q.get(u)
                if not q:
                    continue
                for m in re.finditer(r'\d{2,4}[가-힣]{1,3}\d+', row['판례']):
                    i = to_id(m.group(0), law)
                    if i:
                        A[i].add(q['id'])
    if J:
        for q in J.get('문제', []):
            qid = str(q.get('id'))
            for z in q.get('지문', []):
                for m in re.finditer(r'\d{2,4}[가-힣]{1,3}\d+', str(z.get('pan') or '')):
                    i = to_id(m.group(0), law)
                    if i:
                        B[i].add(qid)
    return uid2q, byid, A, B, ledk


def code_ids(r, law, uid2q, ledk):
    out = set()
    for code in (r.get('기출') or []):
        mc = re.match(r'^1차-([특상디민])-(\d{2})-(\d+)-([0-9A-Za-z가-힣]+)$', str(code))
        if not mc or mc.group(1) != GA.get(law):
            continue
        q = uid2q.get(ledk.get((mc.group(3), mc.group(4))) or '')
        if q and q['yr'][-2:] == mc.group(2):
            out.add(q['id'])
    return out


def check(law, tag, data):
    rows = (data or {}).get('판례') or []
    if not rows:
        T('5', '%s — 산출물이 없다(문항 JSON 없는 법은 무변)' % law, True, '건너뜀')
        return None
    uid2q, byid, A, B, ledk = truth(law)
    bad1, bad2, n = [], [], 0
    for r in rows:
        ok_ids = A.get(r['id'], set()) | B.get(r['id'], set()) | code_ids(r, law, uid2q, ledk)
        for q in (r.get('기출문항') or []):
            n += 1
            if q['id'] not in ok_ids:
                bad1.append((r['id'], q['id']))
            want = (byid.get(q['id']) or {}).get('no', None)
            if want is not None and str(q.get('no') or '') != want:
                bad2.append((r['id'], q['id'], q.get('no'), want))
    T('1', '%s%s — 가리키는 문제가 참이다(%d항)' % (law, tag, n), not bad1,
      '거짓 %d %s' % (len(bad1), bad1[:4]))
    T('2', '%s%s — no = 그 id 문항의 시험문번' % (law, tag), not bad2,
      '어긋남 %d %s' % (len(bad2), bad2[:4]))
    why = collections.Counter()
    for r in rows:
        for c, v in (r.get('기출문항없음') or {}).items():
            why[v] += 1
    return {'n': n, 'bad1': len(bad1), 'why': dict(why), 'rows': len(rows)}


new = load('특허')
if new is None:
    raise SystemExit('NG  빌드 산출물이 없다 — jo_build.py 를 먼저 돌려라 (%s)' % OUT)
st = check('특허', '', new)
T('3', '특허 — 원장짝없음 79', st['why'].get('원장짝없음') == 79, st['why'])
T('4', '특허 — 판례 391', st['rows'] == 391, st['rows'])

# 표본 여섯(§D-3) — 볼트 코드 → 그 문항이 어느 판례엔가 붙었는가
uid2q, byid, A, B, ledk = truth('특허')
WANT = {'13-50-7': '2013-50-12', '10-47-14': '2010-47-10', '07-44-r2': '2007-44-2',
        '22-59-16': '2022-59-20', '26-63-7': '2026-63-8', '25-62-13': '2025-62-10'}
allids = set()
for r in new['판례']:
    for q in (r.get('기출문항') or []):
        allids.add(q['id'])
miss = [k for k, v in WANT.items() if v not in allids]
T('3', '표본 여섯 — 채팅 표와 같은 문항 id 가 붙었다', not miss, '못 붙은 것 %s' % miss)
r81 = next((x for x in new['판례'] if x['id'] == '81후64'), None)
T('3', '81후64 → 2021-58-14(시험문번 17)',
  bool(r81) and [(q['id'], q.get('no')) for q in (r81.get('기출문항') or [])] == [('2021-58-14', '17')],
  [(q['id'], q.get('no')) for q in (r81.get('기출문항') or [])] if r81 else '없음')

# 상표·민소 — 같은 잣대
for law in ('상표', '디보', '민소'):
    check(law, '', load(law))

# ── §D-4 빠진 것 0 · §D-6 헛잣대 ────────────────────────────────────────
if BEFORE and os.path.isfile(BEFORE):
    old = load('특허', BEFORE)
    O = {r['id']: r for r in old['판례']}
    N = {r['id']: r for r in new['판례']}
    uid2q, byid, A, B, ledk = truth('특허')
    obad, keep_miss = 0, []
    for i, r in O.items():
        # ⚠ 헛잣대는 **ⓐ∪ⓑ 만**으로 잰다 — 셋째 원천(ⓒ 볼트 코드)은 고치기 전엔 없던 길이다.
        #   ⓒ 를 넣으면 13 이 되살아나 347 이 된다(2026-09-21 실측).
        ok_ids = A.get(i, set()) | B.get(i, set())
        cur = {q['id'] for q in (N.get(i, {}).get('기출문항') or [])}
        for q in (r.get('기출문항') or []):
            if q['id'] not in ok_ids:
                obad += 1
            elif q['id'] not in cur:
                keep_miss.append((i, q['id']))
    # 채팅이 잰 값은 360 이다. 내 셈은 **uid 로 이은 참값**을 잣대로 삼아 그보다 크게 나온다 —
    # 잣대의 구실(고치기 전에는 크게 거짓 · 고친 뒤 0)은 같다. 두 수를 다 적는다.
    T('6', '헛잣대 — 고치기 전에는 크게 거짓(채팅 셈 360)', obad >= 300, '%d (채팅 360)' % obad)
    owhy = collections.Counter()
    for r in O.values():
        for c, v in (r.get('기출문항없음') or {}).items():
            owhy[v] += 1
    T('6', '헛잣대 — 고치기 전 원장짝없음 211', owhy.get('원장짝없음') == 211, dict(owhy))
    T('4', '참이던 항목은 하나도 안 사라진다', not keep_miss,
      '사라짐 %d %s' % (len(keep_miss), keep_miss[:4]))
    same = [k for k in ('기출표시', '기출', '자동중요도') if
            all(O[i].get(k) == N.get(i, {}).get(k) for i in O)]
    T('4', '기출표시·기출·자동중요도 무변', len(same) == 3, same)
else:
    T('6', '헛잣대 — 고치기 전 산출물을 --before 로 준다', False, '안 줌')

# ── §D-7 재실행 멱등 ────────────────────────────────────────────────────
def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()
T('7', '산출물 md5(이 판)', True, md5(os.path.join(OUT, 'prec_특허_리스트.json'))[:16])

ng = [x for x in R if not x[2]]
print('== _task_jo_gichul_q_uid 관문 — %d항 · PASS %d · FAIL %d =='
      % (len(R), len(R) - len(ng), len(ng)))
g0 = None
for g, n, ok, got in R:
    if g != g0:
        print('  §D-%s' % g); g0 = g
    print('    %s %-52s %s' % ('PASS' if ok else 'FAIL', n, got))
