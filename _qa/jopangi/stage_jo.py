# -*- coding: utf-8 -*-
r"""로컬 _out/ → 클론 genie\jo\ 로 옮긴다 (지시서 v3-A §8).

stage_out.py 규약 그대로 — 파일마다 쓰고 **되읽어 바이트 대조**하고, 어긋나면 재시도한다.
바뀐 것만 옮긴다(목적지와 바이트가 같으면 건드리지 않는다).
검산 csv 4종은 공개 저장소에 넣지 않고 `_pipeline\` 으로 보낸다.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import os, sys, time, shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def out_root():
    la = os.environ.get('LOCALAPPDATA') or os.path.join(
        os.environ.get('USERPROFILE', ''), 'AppData', 'Local')
    return os.environ.get('JOPANGI_OUT') or os.path.join(la, 'jopangi', '_out')


def clone_root():
    return os.environ.get('JOPANGI_CLONE') or _roots.genie()


def pipe_dir():
    return os.path.join(HERE, '공통', '_pipeline')   # 9/23 정리 2차


def put(src, dst):
    """쓰고 되읽어 바이트 대조. 4회까지 재시도."""
    want = open(src, 'rb').read()
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    for _ in range(4):
        with open(dst, 'wb') as f:
            f.write(want)
            f.flush()
            os.fsync(f.fileno())
        if open(dst, 'rb').read() == want:
            return True, len(want)
        time.sleep(0.08)
    return False, len(want)


def same(a, b):
    if not os.path.exists(b):
        return False
    if os.path.getsize(a) != os.path.getsize(b):
        return False
    return open(a, 'rb').read() == open(b, 'rb').read()


def stage(src=None, dst=None, pipe=None, verbose=True):
    """→ {'옮김', '그대로', '실패', '불일치', '옮긴파일', '바이트'}"""
    src = src or out_root()
    dst = dst or os.path.join(clone_root(), 'jo')
    pipe = pipe or pipe_dir()
    data_src = os.path.join(src, 'data')
    data_dst = os.path.join(dst, 'data')
    os.makedirs(data_dst, exist_ok=True)
    os.makedirs(pipe, exist_ok=True)

    # ── 옮길 것을 (원본, 목적지) 쌍으로 먼저 다 모은다 — 재대조가 하나도 빠지면 안 된다.
    pairs = []
    for root, _dirs, files in os.walk(data_src):
        for f in sorted(files):
            if f.endswith('.py') or f.endswith('.bak'):
                continue
            s = os.path.join(root, f)
            pairs.append((s, os.path.join(data_dst, os.path.relpath(s, data_src))))

    # 검산 csv 4종은 클론이 아니라 _pipeline 으로 (§8-3 · 공개 저장소)
    검산옮김 = 0
    for f in sorted(os.listdir(src)):
        if f.startswith('_검산_') and f.endswith('.csv'):
            ok, _n = put(os.path.join(src, f), os.path.join(pipe, f))
            검산옮김 += 1 if ok else 0

    moved, kept, bad, tot = [], 0, [], 0
    for s, d in pairs:
        if same(s, d):
            kept += 1
            continue
        ok, n = put(s, d)
        tot += n
        moved.append(os.path.basename(d))
        if not ok:
            bad.append(d)

    # ⚠ 전수 재대조는 **옮긴 것 전부**가 아니라 **쌍 전부**를 본다.
    #   _out 만 훑고 빠뜨렸다가 인접 파일 덮음 사고를 놓친 적이 있다.
    mism = [d for s, d in pairs if not same(s, d)]
    for s, d in pairs:
        if d in mism:
            put(s, d)
    mism = [d for s, d in pairs if not same(s, d)]

    r = {'옮김': len(moved), '그대로': kept, '실패': len(bad), '불일치': len(mism),
         '옮긴파일': moved, '바이트': tot, '검산csv': 검산옮김,
         '대상': dst, '전체': len(pairs)}
    if verbose:
        print('옮김 %d개 · 그대로 %d개 · %.2fMB · 되읽기 실패 %d · 최종 불일치 %d'
              % (r['옮김'], r['그대로'], tot / 1048576, r['실패'], r['불일치']))
        for x in mism[:10]:
            print('   불일치:', x)
        print('대상 =', dst, '· 검산 csv %d개 →' % 검산옮김, pipe)
    return r


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    r = stage()
    sys.exit(0 if r['불일치'] == 0 and r['실패'] == 0 else 4)
