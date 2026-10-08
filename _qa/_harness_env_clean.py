# -*- coding: utf-8 -*-
r"""_task_env_clean §C 관문 — 재료(_env_clean_c\*.json · 본 세션이 실행기 실행 · TEMP 재기에서 뽑음)를 판정해 _env_clean_c\result.txt 에 쓴다(브라우저 없음)
  C-1 %TEMP% 항목 수 · 크기 — 새 실행기로 자과 전체 regress 앞 → 뒤(항목 ±5 · 크기 +100 MB 안) · 헛잣대 = 옛 실행기(B 앞)로 같은 하네스 몇 개를 돌리면 항목이 는다
  C-2 ⓐ 죽은 실행이 남긴 하네스 임시 폴더(흉내 · pid 없음 · 2 시간 전)를 다음 실행 시작 쓸기가 지움 ⓑ 시간 넘김(전수표 사본 3 초)으로 죽인 하네스도 임시 폴더가 안 남음
  C-3 판 push 흉내 뒤 그 판 워크트리 없음 — `git worktree list` 에 남은 것 = 지금 쓰는 것뿐
  C-4 같은 하네스 셋 · 같은 판을 옛 실행기 / 새 실행기로 → 열쇠 · 칸 판정 · 값(정규화) 같음
  python _harness_env_clean.py [--data <재료 = _env_clean_c>] [--res <결과>]"""
import os as _os_r, sys as _sys_r   # env_lanes — _roots.py 를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import json, os, sys   # noqa: E402
sys.stdout.reconfigure(encoding='utf-8')
_roots.need_n('_env_clean_c 재료(본 세션이 PC 에서 잰 TEMP · 실행기 결과)')
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


DATA = ARG('--data', os.path.join(HERE, '_env_clean_c'))
OUTF = ARG('--res', os.path.join(DATA, 'result.txt'))
RES = []


def T(g, name, ok, detail=''):
    RES.append((g, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', g, name, detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)[:500]), flush=True)


def I(g, name, detail=''):
    RES.append((g, name, None, detail))
    print('INFO | %s · %s | %s' % (g, name, detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)[:500]), flush=True)


def jl(n):
    p = os.path.join(DATA, n)
    return json.load(open(p, encoding='utf-8')) if os.path.isfile(p) else None


def c1():
    d = jl('c1.json')
    if not d:
        return T('C-1', '재료 없음(c1.json)', False)
    dn = d['after']['entries'] - d['before']['entries']
    dm = (d['after']['bytes'] - d['before']['bytes']) / 2**20
    T('C-1', '새 실행기 · 자과 전체 regress(%s) 앞 → 뒤 %%TEMP%% 항목 %d → %d(%+d · ±5 안) · 크기 %+.1f MB(+100 MB 안)' % (
        d.get('run'), d['before']['entries'], d['after']['entries'], dn, dm), abs(dn) <= 5 and dm <= 100, d.get('new_entries', [])[:20])
    c4 = jl('c4.json') or {}
    o = c4.get('old') or {}
    if o:
        T('C-1', '헛잣대 — 옛 실행기(env_clean B 앞)로 하네스 %s 를 돌리면 %%TEMP%% 항목이 는다(%d → %d · +%d)' % (
            c4.get('set'), o['temp_before'], o['temp_after'], o['temp_after'] - o['temp_before']), o['temp_after'] > o['temp_before'], o.get('new_entries', [])[:20])
        n = c4.get('new') or {}
        ne = n.get('new_entries', [])
        # 하네스 몫이 아닌 것 — 부르는 쪽이 준 실행기 자리(qa_chain_*) · 다른 앱(WinGet 등 · 그 시각에 나란히 돈 것)
        other = [x for x in ne if x.startswith('qa_chain') or x in ('WinGet',)]
        left = [x for x in ne if x not in other]
        T('C-1', '같은 하네스 셋을 새 실행기로 — %%TEMP%% 항목 %d → %d(%+d) · 그 가운데 하네스가 남긴 것 %d(뺀 것 = 실행기 자리 · 다른 앱 %s)' % (
            n['temp_before'], n['temp_after'], n['temp_after'] - n['temp_before'], len(left), other), not left, left[:20])


def c2():
    d = jl('c2.json')
    if not d:
        return T('C-2', '재료 없음(c2.json)', False)
    T('C-2', 'ⓐ 죽은 실행(흉내 · pid 999999 · 2 시간 전)의 하네스 임시 폴더를 다음 실행 시작 쓸기가 지움', d['fake_gone'], {'앞': d['before'], '뒤': d['after']})
    T('C-2', 'ⓑ 시간 넘김(3 초)으로 죽인 하네스 — 그 실행이 끝난 뒤 그 실행이 만든 pa_qa 실행 폴더 남음 0', not d['left_new'], {'남음': d['left_new'], '뒤': d['after'], '줄': d.get('timeout_line')})


def c3():
    d = jl('c3.json')
    if not d:
        return T('C-3', '재료 없음(c3.json)', False)
    T('C-3', '판 push 흉내 뒤 — 그 판 워크트리 없음 · git worktree list = 지금 쓰는 것뿐(%s)' % d.get('when'), not d['left'], {'list': d['list'], '남은 판 워크트리': d['left']})


def c4():
    d = jl('c4.json')
    if not d:
        return T('C-4', '재료 없음(c4.json)', False)
    # 같은 실행기 · 같은 판에서도 판정이 갈린 칸(흔들림 표 _qa_flaky.json — 같은 하네스 · 같은 칸)은 실행기 탓이 아니므로 따로 센다(§B-6 과 같은 꼴)
    fp = os.path.join(_d_r, '_qa_flaky.json')
    fl = json.load(open(fp, encoding='utf-8')) if os.path.isfile(fp) else []
    fls = set((os.path.basename(x['harness'])[:-3].replace('_harness_', ''), x['item']) for x in fl)
    for r in d['rows']:
        if r.get('missing'):
            T('C-4', '%s — 한쪽 결과 없음(%s)' % (r['name'], r['missing']), False); continue
        fk = [i for i in r['st_diff'] if (r['name'], i) in fls]
        real = [i for i in r['st_diff'] if (r['name'], i) not in fls]
        T('C-4', '%s — 옛 / 새 실행기 열쇠 같음 %s · 칸 판정 다름 %d(흔들림 표에 있는 칸 %d 은 따로) · 값 다름 %d · 한쪽만 %d(칸 %d)' % (
            r['name'], r['key_same'], len(real), len(fk), len(r['v_diff']), len(r['one_side']), r['items']),
          r['key_same'] and not real and not r['v_diff'] and not r['one_side'], {'판정': real[:5], '흔들림': fk[:5], '값': r['v_diff'][:5], '한쪽': r['one_side'][:5]})


def main():
    print('§C 관문 _task_env_clean · 재료 %s' % DATA)
    for f in (c1, c2, c3, c4):
        try:
            f()
        except Exception as e:
            T(f.__name__.upper(), '돌다 멈춤', False, repr(e)[:300])
    np = sum(1 for r in RES if r[2] is True)
    nf = sum(1 for r in RES if r[2] is False)
    with open(OUTF, 'w', encoding='utf-8', newline='\n') as f:
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ('INFO' if ok is None else ('PASS' if ok else 'FAIL'), g, n, d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)))
        f.write('_harness_env_clean — PASS %d · FAIL %d\n' % (np, nf))
    print('_harness_env_clean — PASS %d · FAIL %d · 결과 %s' % (np, nf, OUTF))
    return 1 if nf else 0


if __name__ == '__main__':
    sys.exit(main())
