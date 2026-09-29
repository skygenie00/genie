# -*- coding: utf-8 -*-
"""_task_jo_p8sol §A-2 — 해례 8판 해설 판올림(원장 jimun_7pan.json 의 sol) · ⚙ 단계 [6e] · 멱등

  ⚙ = jo_build [6e]([6d] 8판 글 판올림 뒤) 가 build(dump, 검산, OUT) 를 부른다 — 이번 산출 jimun_7pan.json 을 고쳐 다시 쓴다.
  재료 = 특상디\\_p8up\\_p8sol.json(Code 9/29 · jopangi\\_p8sol_build.py --write · 두 PDF 글자층에서 뽑은 8판 해설 · 워터마크 값 없음)
       ⚠ 이 스크립트는 PDF 를 읽지 않는다(재료 표만 쓴다)
  바꾸는 것(지문 sol · 판8 칸)
    명칭만 · 바뀜 · 잘림 줄 → sol = 8판 해설(선지 조각이면 제 조각 · 잘린 조각은 책 조각 전문)
    바뀜 줄만 판8.s7 = 옛 sol(「8판 해설 고침」 단추 · 「7판 해설」 상자) · 판8 칸이 없으면 {cat:'해설', s7} · 있으면 cat 은 두고 s7 만
    새 카드(P8-) → sol = 8판 해설 · [유제] 는 빈칸 그대로
    같음 · 짝없음 · 해설없음 → 무변
  줄 대조 — 재료의 s7md5(뽑을 때 앱 sol 의 md5 앞 8자)가 이번 원장 sol 과 다르면 멈춘다(원장이 그 사이 바뀐 것 · 짐작해 얹지 않는다)

    python _p8sol_apply.py [--data <jo/data>] [--out <폴더>] [--write]     (따로 돌리기 — ⚙ 밖에서 클론 데이터에 바로 얹기)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import collections, hashlib, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '특상디', '_p8up', '_p8sol.json')
FILE = 'jimun_7pan.json'
BASIS = '해례 8판 해설 · 94f115f0 · 2026-09-29'
WANT = {'명칭만': 172, '바뀜': 112, '잘림': 5, '새': 15, 's7': 112}   # _p8sol_build 셈(§A-1 · 결과 절) · revfix0929 A-1 — 잘림 21 → 5(표지뿐 16 줄 = 같음)


def dump_b(o):
    return json.dumps(o, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


def jload(p):
    return json.loads(open(p, 'rb').read().decode('utf-8'))


md8 = lambda s: hashlib.md5((s or '').encode('utf-8')).hexdigest()[:8]


def apply(J, src):
    """J = 이번 원장(자리에서 고친다) → (log, bad) · 이미 얹은 원장이면 (None, [])"""
    if J.get('판8_해설'):
        return None, []
    by = {z['id']: z for z in J['지문']}
    cnt, bad = collections.Counter(), []
    for i, v in sorted(src['rows'].items()):
        if v['cat'] not in ('명칭만', '바뀜', '잘림'):
            continue
        z = by.get(i)
        if not z:
            bad.append([i, '원장에 없는 줄']); continue
        if md8(z.get('sol')) != v['s7md5']:
            bad.append([i, '원장 sol 이 뽑을 때와 다르다', md8(z.get('sol')), v['s7md5']]); continue
        s7 = z.get('sol') or ''
        z['sol'] = v['sol8']
        cnt[v['cat']] += 1
        if v['cat'] == '바뀜':
            p8 = z.get('판8')
            if p8 is None:
                z['판8'] = {'cat': '해설', 's7': s7}
            else:
                p8['s7'] = s7
            cnt['s7'] += 1
    for i, v in sorted(src['new'].items()):
        z = by.get(i)
        if not z:
            bad.append([i, '새 카드가 원장에 없다']); continue
        if v['유제'] or not v['sol8']:
            continue
        if z.get('sol'):
            bad.append([i, '새 카드 sol 이 이미 있다']); continue
        z['sol'] = v['sol8']; cnt['새'] += 1
    J['판8_해설'] = BASIS
    return {'셈': dict(cnt)}, bad


def build(dump, 검산, out):
    """⚙ jo_build [6e] — 이번 산출(out) jimun_7pan.json 에 8판 해설을 얹어 dump 로 다시 쓴다 · 어긋나면 멈춘다(예외 → ⚙ NG)"""
    J = jload(os.path.join(out, FILE))
    log, bad = apply(J, jload(SRC))
    if log is None:
        검산.chk('P8S', '해례 8판 해설(p8sol)', 'INFO', '이미 얹은 원장 — 그대로', J.get('판8_해설'))
        return
    if bad:
        raise RuntimeError('p8sol — 재료와 원장이 어긋난다 %d: %s' % (len(bad), json.dumps(bad[:6], ensure_ascii=False)))
    dump(FILE, J)
    c = log['셈']
    검산.gate('P8S', '해례 8판 해설(p8sol)', c == WANT,
              ' '.join('%s %d' % kv for kv in sorted(c.items())),
              ' '.join('%s %d' % kv for kv in sorted(WANT.items())))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    A = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
    data = A('--data', _roots.genie(r'jo\data'))
    out = A('--out', data)
    raw = open(os.path.join(data, FILE), 'rb').read()
    J = json.loads(raw.decode('utf-8'))
    if dump_b(J) != raw:
        sys.exit('NG %s json 왕복이 바이트가 다르다 — 멈춤' % FILE)
    log, bad = apply(J, jload(SRC))
    if log is None:
        print('이미 얹은 원장(%s) — 그대로(멱등)' % J.get('판8_해설'))
        return
    print('셈', json.dumps(log['셈'], ensure_ascii=False), '· 기대', json.dumps(WANT, ensure_ascii=False))
    if bad:
        print('어긋남', json.dumps(bad[:20], ensure_ascii=False))
        sys.exit('NG 어긋남 %d — 안 씀' % len(bad))
    b = dump_b(J)
    print('%s %d → %d B · md5 %s → %s' % (FILE, len(raw), len(b), hashlib.md5(raw).hexdigest()[:8], hashlib.md5(b).hexdigest()[:8]))
    if '--write' in sys.argv:
        os.makedirs(out, exist_ok=True)
        p = os.path.join(out, FILE)
        for _ in range(5):
            open(p, 'wb').write(b); time.sleep(0.5)
            if open(p, 'rb').read() == b:
                break
        else:
            sys.exit('NG %s 되읽기가 다르다' % p)
    else:
        print('(재기만 · --write 로 쓴다)')


if __name__ == '__main__':
    main()
