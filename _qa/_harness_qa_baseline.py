# -*- coding: utf-8 -*-
"""_task_qa_baseline §B 관문 — 사슬 실행기(_qa_chain.py) · 전수표 · 저장본 · 값으로 맞대기 · 흔들림 · 옛 잣대 표 (2026-09-30)

  python _harness_qa_baseline.py [--only B1,B2,…] [--res <결과>]
        --run1 <조판기 첫 저장본 실행 기록 id> --run2 <A-6 뒤 다시 만든 저장본 실행 기록 id>    (_qa_results\\jo\\_runs\\<id>.json)
        --jrun1 <자과 첫 저장본> --jrun2 <자과 다시 만든 저장본>
        --plant <심은 퇴행 표 json>  --old <옛 절차 결과 표 json>  --stale <옛 잣대 표 md>  --b7 <시간 표 json>
  B-1 전수표 · B-2 되풀이(같은 커밋 두 번) · B-3 심은 퇴행(① 새 FAIL · ② FAIL 값 바뀜 · 헛잣대 = 제목 맞대기) · B-4 열쇠(_qa 만 바꾼 커밋 · 데이터 한 파일)
  · B-5 흔들림(대기 짧게 한 판 → 흔들림 목록) · B-6 옛 잣대 표 · B-7 시간 · B-8 회귀(env_lanes 관문 · _qa_sync check · 옛 절차 결과와 같은 PASS/FAIL)
  모래상자 = %TEMP%\\qa_gate(전수표 · 저장본 · 흔들림 사본) · 버리는 워크트리 <genie>\\.claude\\worktrees\\qa_gate(분리 HEAD · 가지 없음 · 끝나면 지움) · push 0
  N: 저장본 · 전수표 · _qa_flaky.json 은 읽기만 한다.
"""
import os as _os_r, sys as _sys_r   # env_lanes — _roots.py 를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import glob
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
NR = _roots.need_n('N: 저장본 · 전수표 · 옛 잣대 표')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, NR)
import _qa_chain as QC   # noqa: E402

QCP = os.path.join(NR, '_qa_chain.py')
RESD = os.path.join(NR, '_qa_results')
SB = os.path.join(tempfile.gettempdir(), 'qa_gate')
BASE_REV = 'cedc251'                       # 착수 때 main(첫 저장본)


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(NR, '_harness_qa_baseline_result.txt'))
L = []


def T(g, title, ok, val=''):
    s = ('PASS' if ok else 'FAIL') + ' | ' + g + ' · ' + title + (' | ' + (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False))[:1500] if val != '' else '')
    L.append(s)
    print(s, flush=True)
    return ok


def I(g, title, val=''):
    s = 'INFO | ' + g + ' · ' + title + (' | ' + (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False))[:2500] if val != '' else '')
    L.append(s)
    print(s, flush=True)


def want(b):
    return not ONLY or b in ONLY


def qc(args, env=None, timeout=14400):
    e = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
    e.update(env or {})
    t0 = time.time()
    r = subprocess.run([sys.executable, QCP] + args, capture_output=True, env=e, timeout=timeout)
    return r.returncode, r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace'), round(time.time() - t0, 1)


def jl(p, d=None):
    try:
        with open(p, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return d


def man(app, rid):
    return jl(os.path.join(RESD, app, '_runs', rid + '.json'))


def rec(app, row, resd=RESD):
    return jl(os.path.join(resd, app, '%s%s.json' % (row['key'], ('@' + row['label']) if row.get('label') else '')))


def sandbox(census=None):
    """모래상자 자리 · 환경(전수표 · 저장본 · 흔들림 · 하네스 자리)"""
    os.makedirs(SB, exist_ok=True)
    return {'QA_CHAIN_LIST': census or os.path.join(SB, 'census.json'), 'QA_CHAIN_RES': os.path.join(SB, 'res'),
            'QA_CHAIN_FLAKY': os.path.join(SB, 'flaky.json'), 'QA_CHAIN_HHOME': NR}


def git(repo, *a):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True)


def gate_wt():
    """버리는 워크트리(분리 HEAD · 가지 없음) — 있으면 BASE_REV 로 되돌려 다시 쓴다"""
    clone = QC.main_clone()
    wt = os.path.join(clone, '.claude', 'worktrees', 'qa_gate')
    sha = git(clone, 'rev-parse', BASE_REV).stdout.decode().strip()
    if os.path.isdir(wt):
        git(wt, 'checkout', '-q', '--detach', sha)
        git(wt, 'checkout', '--', '.')
        git(wt, 'clean', '-fdq')
    else:
        git(clone, 'worktree', 'add', '--detach', wt, sha)
    return wt


def drop_gate_wt():
    clone = QC.main_clone()
    wt = os.path.join(clone, '.claude', 'worktrees', 'qa_gate')
    if os.path.isdir(wt):
        git(clone, 'worktree', 'remove', '--force', wt)


def edit(path, pairs):
    b = open(path, 'rb').read()
    for a, c in pairs:
        a, c = a.encode('utf-8'), c.encode('utf-8')
        n = b.count(a)
        if n != 1:
            raise SystemExit('심기 앵커 %d 건(1 이어야): %r' % (n, a[:60]))
        b = b.replace(a, c)
    open(path, 'wb').write(b)


def last_compare(resd, app):
    fs = sorted(glob.glob(os.path.join(resd, app, '_runs', '*_compare.json')))
    return jl(fs[-1]) if fs else None


# ── B-1 전수표 ────────────────────────────────────────────────────────────────────────────────
def b1():
    rc, out, _ = qc(['check'])
    per = re.findall(r'^\s+(\S+)\s+하네스\s+(\d+) · 줄\s+(\d+)', out, re.M)
    T('B-1', '_qa_chain.py check — 줄 수 = N: 정본 하네스 수(앱마다) · 무엇 · 태그 · 입력 빈칸 0', rc == 0, out.strip().splitlines()[-1] if out.strip() else rc)
    for a, h, n in per:
        T('B-1', '%s — N: 정본 하네스 %s = 전수표 줄 %s' % (a, h, n), h == n)
    c = QC.census_load()
    miss = [r['file'] for r in c['rows'] if r['app'] in ('jo', 'jagwa') and not r.get('skip') and r.get('inputs_src') != '추적']
    T('B-1', '조판기 · 자과 줄 입력 = 추적 값(짐작 0 · 사슬을 돌려 채움) · 건넌 줄 빼고', not miss, miss[:10])
    sk = [(r['file'], r['skip']) for r in c['rows'] if r.get('skip')]
    I('B-1', '사슬 밖(skip) 줄 — 까닭', sk)
    # 헛잣대 — 한 줄을 뺀 전수표면 check 가 FAIL
    tmp = os.path.join(SB, 'census_minus1.json')
    os.makedirs(SB, exist_ok=True)
    c2 = dict(c)
    c2['rows'] = [r for r in c['rows'] if r['file'] != c['rows'][0]['file']]
    io.open(tmp, 'w', encoding='utf-8').write(json.dumps(c2, ensure_ascii=False))
    rc2, out2, _ = qc(['check'], env={'QA_CHAIN_LIST': tmp})
    T('B-1-헛', '헛잣대 — 줄 하나(%s)를 뺀 전수표면 check FAIL(종료 코드 1)' % c['rows'][0]['file'], rc2 == 1, out2.strip().splitlines()[-1] if out2.strip() else rc2)
    # _qa_sync check 도 전수표를 잰다(A-7-3)
    r3 = subprocess.run([sys.executable, os.path.join(NR, '_qa_sync.py'), 'check'], capture_output=True)
    o3 = r3.stdout.decode('utf-8', 'replace')
    m = re.search(r'전수표 어긋남 (\d+)', o3)
    T('B-1', '_qa_sync check 가 전수표를 잰다 — 전수표 어긋남 0', bool(m) and m.group(1) == '0', (o3.strip().splitlines() or [''])[0][:300])


# ── B-3 심은 퇴행 ─────────────────────────────────────────────────────────────────────────────
def b3(plant):
    P = jl(plant)
    if not P:
        return T('B-3', '심은 퇴행 표(--plant)', False, '없음')
    h, rid = P['harness'], P['run1']
    m1 = man('jo', rid)
    row = next(x for x in m1['rows'] if x['name'] == h)
    env = sandbox()
    if os.path.isdir(env['QA_CHAIN_RES']):
        shutil.rmtree(env['QA_CHAIN_RES'])
    os.makedirs(os.path.join(env['QA_CHAIN_RES'], 'jo'))
    shutil.copy2(os.path.join(NR, '_qa_chain_list.json'), env['QA_CHAIN_LIST'])
    # 바탕 저장본 = 지금 전수표로 잰 바탕 열쇠의 저장본(없으면 첫 저장본 실행의 것) → 모래상자에 그 열쇠 이름으로
    crow = next(r for r in QC.census_load()['rows'] if QC.rname(r) == h)
    bk, _ = QC.key_of(crow, 'jo', QC.Ctx(rev=BASE_REV))
    src = os.path.join(RESD, 'jo', bk + '.json')
    if not os.path.exists(src):
        src = os.path.join(RESD, 'jo', row['key'] + '.json')
    shutil.copy2(src, os.path.join(env['QA_CHAIN_RES'], 'jo', bk + '.json'))
    row = dict(row, key=bk)
    wt = gate_wt()
    edit(os.path.join(wt, 'jo', 'index.html'), P['edits'])
    rc, out, sec = qc(['compare', 'jo', '--only', h, '--root', wt, '--base', BASE_REV, '--no-flaky'], env=env)
    cj = last_compare(env['QA_CHAIN_RES'], 'jo')
    r = next((x for x in (cj or {}).get('rows', []) if x['name'] == h), {})
    ids = r.get('ids') or {}
    I('B-3', '심은 고침 — %s · jo/index.html %d 곳 · compare %s초 · rc %s' % (h, len(P['edits']), sec, rc), [(a[:80], c[:80]) for a, c in P['edits']])
    T('B-3 ①', '지금 PASS 인 항목을 깨는 고침 → 「새 FAIL」로 잡힘 — %s' % P['break'][:120], P['break'] in ids.get('새 FAIL', []), ids.get('새 FAIL', [])[:6])
    T('B-3 ②', '이미 FAIL 인 항목의 값만 바꾸는 고침 → 「FAIL 값 바뀜」으로 잡힘 — %s' % P['change'][:120], P['change'] in ids.get('FAIL 값 바뀜', []), ids.get('FAIL 값 바뀜', [])[:6])
    # 헛잣대 — 착수 때 절차(FAIL 제목 맞대기): 같은 두 결과를 제목 집합으로 맞대면 ② 는 못 잡는다
    base = jl(os.path.join(env['QA_CHAIN_RES'], 'jo', row['key'] + '.json'))
    newk = r.get('nkey')
    new = jl(os.path.join(env['QA_CHAIN_RES'], 'jo', newk + '.json')) if newk else None
    if base and new:
        bt = {x['t'] for x in base['items'] if x['st'] == 'FAIL'}
        nt = {x['t'] for x in new['items'] if x['st'] == 'FAIL'}
        tb = {x['id']: x['t'] for x in new['items']}
        got1 = tb.get(P['break']) in (nt - bt)
        got2 = tb.get(P['change']) in (nt - bt)
        T('B-3-헛', '헛잣대 — 제목 맞대기(착수 때 절차)는 ① 은 잡고 ② 는 못 잡는다(같은 입력)', got1 and not got2, {'①': got1, '②': got2, '새 FAIL 제목 수': len(nt - bt)})
    else:
        T('B-3-헛', '헛잣대 — 두 결과', False, [bool(base), bool(new)])
    git(wt, 'checkout', '--', '.')


# ── B-4 열쇠 ──────────────────────────────────────────────────────────────────────────────────
def plan_names(out):
    return [m.group(1) for m in re.finditer(r'^(\S+)\s+바탕 \S+ .*→ 새 판에서 돎', out, re.M)], re.search(r'바탕에서 돌 것 (\d+) · 새 판에서 돌 것 (\d+)', out)


def b4():
    wt = gate_wt()
    rc0, out0, sec0 = qc(['plan', 'jo', '--root', wt, '--base', BASE_REV])          # 안 바꾼 판(같은 자리) — 저장 뒤 입력 표류로 생기는 재실행이 바닥
    names0, m0 = plan_names(out0)
    q = os.path.join(wt, '_qa', '_roots.py')
    open(q, 'ab').write(b'\n# qa_gate B-4 - _qa only change\n')
    rc, out, sec = qc(['plan', 'jo', '--root', wt, '--base', BASE_REV])
    names, m = plan_names(out)
    I('B-4 ①', '바닥 — 안 바꾼 판의 계획(저장 뒤 기록·볼트 입력이 바뀌어 지금 열쇠 저장본이 없는 하네스는 바탕에서 다시 돈다 · _qa 와 무관)', m0.group(0) if m0 else out0[-200:])
    I('B-4 ①', '계획 두 벌(같은 때 잰 것이 아니라 병행 판이 N: 을 고치면 흔들린다 — 아래 T 가 잣대)', {'바꾼 판': m.group(0) if m else None, '안 바꾼 판': m0.group(0) if m0 else None, '더 도는 것': sorted(set(names) - set(names0))})
    git(wt, 'checkout', '--', '.')
    # 결정적 잣대 — genie 밖 입력 해시를 한 번만 재 두 번 다 쓴다
    memo, orig = {}, QC.in_hash
    def _ih(pp, ctx):
        if pp.startswith('genie:'):
            return orig(pp, ctx)
        if pp not in memo:
            memo[pp] = orig(pp, ctx)
        return memo[pp]
    QC.in_hash = _ih
    try:
        rows4 = [r for r in QC.rows_for(QC.census_load(), 'jo') if not r.get('skip')]
        k0 = {QC.rname(r): QC.key_of(r, 'jo', QC.Ctx(root=wt))[0] for r in rows4}
        open(q, 'ab').write(b'\n# qa_gate B-4 - _qa only change\n')
        k1 = {QC.rname(r): QC.key_of(r, 'jo', QC.Ctx(root=wt))[0] for r in rows4}
    finally:
        QC.in_hash = orig
        git(wt, 'checkout', '--', '.')
    more = sorted(n for n in k0 if k0[n] != k1.get(n))
    T('B-4 ①', '_qa 만 바꾼 판 → 열쇠가 바뀌는 하네스 0(조판기 %d · genie 밖 입력은 같은 값으로 두 번 잼)' % len(k0), not more, more)
    # 데이터 한 파일 — 그 파일을 읽는 하네스가 가장 적은(0 넘는) 파일을 고른다(전수표 입력 = 추적 값)
    c = QC.census_load()
    rows = QC.rows_for(c, 'jo')
    tree = QC.Ctx(rev=BASE_REV).tree()
    files = sorted(p for p in tree if p.startswith('jo/data/'))
    best = None
    for f in files:
        rd = sorted(QC.rname(r) for r in rows if not r.get('skip') and any(i == 'genie:' + f or (i.endswith('/**') and ('genie:' + f).startswith(i[:-2])) for i in r.get('inputs') or []))
        if rd and (best is None or len(rd) < len(best[1])):
            best = (f, rd)
    f, expect = best
    fp = os.path.join(wt, *f.split('/'))
    open(fp, 'ab').write(b' ')
    rc, out, sec = qc(['plan', 'jo', '--root', wt, '--base', BASE_REV])
    names, m = plan_names(out)
    T('B-4 ②', 'jo 데이터 한 파일(%s) 해시 바꿈 → 그 파일을 읽는 하네스만 다시 돎(= 전수표 입력)' % f, sorted(names) == expect and 0 < len(names) < len(rows),
      {'다시 돎': sorted(names), '전수표 입력으로 읽는 것': expect, '조판기 사슬': len(rows)})
    T('B-4-헛', '헛잣대 — 커밋 단위 열쇠(착수 때 절차 = 바탕 판 통째)면 %d 하네스가 다시 돈다' % len([r for r in rows if not r.get('skip')]), len(names) < len([r for r in rows if not r.get('skip')]))
    git(wt, 'checkout', '--', '.')
    # ⚙ 자동 푸시 16회(9/16~9/30)가 저장본을 얼마나 묵혔나 — 그 커밋이 바꾼 jo/data 파일을 읽는 하네스 수
    clone = QC.main_clone()
    hs = git(clone, 'log', '--since=2026-09-16 00:00', '--until=2026-09-30 23:59', '--format=%h %ad', '--date=format:%m-%d %H:%M', '--grep=^jo: data', '--', 'jo/data').stdout.decode().split('\n')
    stale = []
    for ln in [x for x in hs if x.strip()]:
        h = ln.split()[0]
        ch = [x for x in git(clone, 'show', '--format=', '--name-only', h, '--', 'jo/data').stdout.decode('utf-8').split('\n') if x]
        rd = {QC.rname(r) for r in rows if not r.get('skip') for cf in ch for i in (r.get('inputs') or []) if i == 'genie:' + cf or (i.endswith('/**') and ('genie:' + cf).startswith(i[:-2]))}
        stale.append((ln, len(ch), len(rd)))
    I('B-4', '⚙ 자동 푸시(jo: data) %d 회 — 커밋 · 바뀐 파일 수 · 다시 돌 하네스 수(조판기 %d 중)' % (len(stale), len(rows)), stale)


# ── B-5 흔들림 ────────────────────────────────────────────────────────────────────────────────
PROBE = r'''# -*- coding: utf-8 -*-
"""qa_gate B-5 흔들림 모사 — 0.3 초 뒤 준비되는 것을 기다려 본다. 앱에 QA_PROBE_SHORT_WAIT 표지가 있으면 첫 판은 대기를 짧게(0.05 초 → FAIL) ·
   다시 돌린 판은 제대로 기다린다(1 초 → PASS) = 시간에 기대는 항목이 흔들리는 꼴(판 수는 모래상자 셈 파일)"""
import os, threading, time
app = open(os.path.join(os.environ['GENIE_ROOT'], 'jo', 'index.html'), 'rb').read()
cf = os.environ['QA_PROBE_COUNTER']
short = b'QA_PROBE_SHORT_WAIT' in app
n = int(open(cf).read()) if os.path.exists(cf) else 0
if short:
    n += 1
    open(cf, 'w').write(str(n))
wait = 0.05 if (short and n % 2 == 1) else 1.0
flag = {}
threading.Timer(0.3, lambda: flag.setdefault('ready', True)).start()
time.sleep(wait)
print('PASS | P1 · 늘 PASS 인 항목 | 1')
print(('PASS' if flag.get('ready') else 'FAIL') + ' | P2 · 0.3초 뒤 준비됨을 기다려 본다 | ' + ('ready' if flag.get('ready') else 'not yet'))
'''


def b5():
    env = sandbox(os.path.join(SB, 'census_probe.json'))
    for p in (env['QA_CHAIN_RES'], os.path.join(SB, 'probe')):
        if os.path.isdir(p):
            shutil.rmtree(p)
    for p in (env['QA_CHAIN_FLAKY'], os.path.join(SB, 'cnt.txt')):
        if os.path.exists(p):
            os.remove(p)
    os.makedirs(os.path.join(SB, 'probe'))
    io.open(os.path.join(SB, 'probe', '_harness_qa_probe.py'), 'w', encoding='utf-8').write(PROBE)
    env['QA_CHAIN_HHOME'] = SB
    c = {'v': 1, 'rows': [{'file': 'probe/_harness_qa_probe.py', 'app': 'jo', 'chains': ['jo'], 'what': '흔들림 모사', 'tags': ['흔들림'], 'eng': [],
                           'inputs': [], 'inputs_src': '정적', 'argv': {'*': []}, 'res': 'stdout', 'timeout': 120,
                           'env': {'QA_PROBE_COUNTER': os.path.join(SB, 'cnt.txt')}}]}
    io.open(env['QA_CHAIN_LIST'], 'w', encoding='utf-8').write(json.dumps(c, ensure_ascii=False))
    rc1, o1, s1 = qc(['run', 'jo', '--rev', BASE_REV], env=env)
    T('B-5', '모사 하네스 바탕 저장본(대기 1 초) = PASS 2', 'PASS 2 · FAIL 0' in o1, o1.strip().splitlines()[-1][:200] if o1.strip() else rc1)
    wt = gate_wt()
    open(os.path.join(wt, 'jo', 'index.html'), 'ab').write(b'\n<!-- QA_PROBE_SHORT_WAIT -->\n')
    rc2, o2, s2 = qc(['compare', 'jo', '--root', wt, '--base', BASE_REV], env=env)
    cj = last_compare(env['QA_CHAIN_RES'], 'jo') or {}
    r = (cj.get('rows') or [{}])[0]
    fl = jl(env['QA_CHAIN_FLAKY'], []) or []
    T('B-5', '대기를 짧게 한 판 → 새 FAIL 이 한 번 더 돌린 판과 달라 「흔들림」으로 갈림(새 FAIL 0)', len(r.get('flaky') or []) == 1 and not (r.get('ids') or {}).get('새 FAIL'),
      {'새 FAIL': (r.get('ids') or {}).get('새 FAIL'), '흔들림': r.get('flaky')})
    T('B-5', '흔들림 목록(_qa_flaky.json 꼴)에 쌓임 — 하네스 · 항목 · 날짜 · 두 값', len(fl) == 1 and set(fl[0]) >= {'harness', 'item', 'date', 'values'} and len(fl[0]['values']) == 2, fl[:1])
    T('B-5', '결과에 흔들림이 따로 보인다(보고 「── 흔들림」 절)', '── 흔들림 1' in o2, re.findall(r'── 흔들림[^\n]*', o2)[:1])
    git(wt, 'checkout', '--', '.')


# ── 옛 잣대 표(_qa_stale_0930.md) 읽기 — 표 줄 · 이름 바뀜 · 표 밖 고침 · 고친 파일 ─────────────────────────────
ROWS2 = []   # 「고친 뒤 새로 선 FAIL」 절(R 줄) — stale_info 가 채운다


def stale_info(md):
    rows, ren, extra, files = [], {}, set(), {}
    del ROWS2[:]
    sec = ''
    if not md or not os.path.exists(md):
        return rows, ren, extra, files
    for ln in io.open(md, encoding='utf-8').read().splitlines():
        if ln.startswith('## '):
            sec = ln
            continue
        if ln.startswith('| ') and not ln.startswith('| #') and not ln.startswith('|---'):
            cols = [x.strip() for x in ln.strip().strip('|').split(' | ')]
            if len(cols) >= 8 and cols[0].isdigit():
                rows.append({'n': int(cols[0]), 'app': cols[1], 'harness': cols[2], 'id': cols[3].replace('¦', '|'), 'old': cols[4], 'now': cols[5], 'cat': cols[6], 'ev': cols[7],
                             'fix': cols[8] if len(cols) > 8 else '', 'after': cols[9] if len(cols) > 9 else ''})
            elif len(cols) >= 11 and re.match(r'^R\d+$', cols[0]) and sec.startswith('## 고친 뒤 새로 선 FAIL'):
                ROWS2.append({'n': cols[0], 'app': cols[1], 'harness': cols[2], 'id': cols[3].replace('¦', '|'), 'was': cols[4], 'old': cols[5], 'now': cols[6],
                              'cat': cols[7], 'ev': cols[8], 'fix': cols[9], 'after': cols[10]})
            continue
        if ln.startswith('- '):
            if sec.startswith('## 이름 바뀜'):
                m = re.match(r'^- (\S+) · (.+) ⟶ (.+)$', ln)
                if m:
                    ren[(m.group(1), m.group(2).replace('¦', '|'))] = m.group(3).replace('¦', '|')
            elif sec.startswith('## 표 밖'):
                m = re.match(r'^- (\S+) · (.+?) ⟶ 새 이름', ln)
                if m:
                    extra.add((m.group(1), m.group(2)))
            elif sec.startswith('## 고친 파일'):
                m = re.match(r'^- (\S+) · (\w+) → (\w+)', ln)
                if m:
                    files[m.group(1)] = (m.group(2), m.group(3))
    return rows, ren, extra, files


def fixed_set(rows):
    return {(r['harness'], r['id']) for r in rows if r['cat'][:1] in 'ad' and r['fix'].strip('- ')}


def flaky_set():
    return {(os.path.basename(x['harness'])[:-3].replace('_harness_', ''), x['item']) for x in (jl(os.path.join(NR, '_qa_flaky.json'), []) or [])}


def same_inputs(r1, r2):
    i1, i2 = r1['keyparts']['in'], r2['keyparts']['in']
    return r1['keyparts']['h'] == r2['keyparts']['h'] and r1['keyparts'].get('argv') == r2['keyparts'].get('argv') and not any(i1[k] != i2[k] for k in set(i1) & set(i2))


def cmp_items(name, r1, r2, ren):
    """두 실행 항목 맞대기 — 앞 실행 id 는 이름 바뀜을 입혀 맞댄다 · [(갈래, 새 id, 옛 id)]"""
    back = {}
    items1 = []
    for it in r1['items']:
        nid = ren.get((name, it['id']))
        if nid:
            back[nid] = it['id']
        items1.append(dict(it, id=nid or it['id']))
    cl = QC.classify(items1, r2['items'])
    return [(k, (n or b)['id'], back.get((n or b)['id'], (n or b)['id'])) for k, v in cl.items() if k not in ('같음', '원래 FAIL') for b, n in v]


# ── B-2 되풀이 — 같은 커밋 두 번 ─────────────────────────────────────────────────────────────────
def b2(app, rid1, rid2, g='B-2', md=None):
    m1, m2 = man(app, rid1), man(app, rid2)
    if not (m1 and m2):
        return T(g, '실행 기록 둘(%s · %s)' % (rid1, rid2), False, '없음')
    rows, ren, extra, files = stale_info(md)
    fl = flaky_set()
    by2 = {x['name']: x for x in m2['rows']}
    same_n, bad_rows, changed, nfl, reused = 0, [], [], 0, []
    for x in m1['rows']:
        y = by2.get(x['name'])
        if not y or x.get('skip') or y.get('skip'):
            continue
        r1, r2 = rec(app, x), rec(app, y)
        if not (r1 and r2):
            bad_rows.append((x['name'], '저장본 없음'))
            continue
        if not same_inputs(r1, r2):
            changed.append(x['name'])            # A-6 고친 하네스(자기 파일 · 부르는 모듈 · tests.js) — B-6 이 잰다
            continue
        if r1.get('when') == r2.get('when') and r1.get('key') == r2.get('key'):
            reused.append(x['name'])             # 같은 저장본(다시 안 돎) — 되풀이가 아니다
            continue
        d = cmp_items(x['name'], r1, r2, ren)
        d2 = [z for z in d if (x['name'], z[2]) not in fl and (x['name'], z[1]) not in fl]
        nfl += len(d) - len(d2)
        same_n += 1
        if d2:
            bad_rows.append((x['name'], d2[:6]))
        T(g, '%s — 같은 커밋 두 번 = 항목 결과 같음(흔들림 목록 뺌 · %d 항목)' % (x['name'], len(r2['items'])), not d2, d2[:6] if d2 else (('흔들림 %d' % (len(d) - len(d2))) if d != d2 else ''))
    I(g, '고친 하네스(자기 파일 · 부르는 모듈 · tests.js 가 바뀜) — 여기서 안 맞대고 B-6 에서 「바뀐 항목 ⊆ 고친 줄」로 잰다', changed)
    I(g, '같은 저장본(두 번째에 다시 안 돎) — 되풀이로 안 셈 %d' % len(reused), reused)
    if app == 'jo':
        T(g, '%s — 입력이 같은 하네스 %d 전부 두 번 같음(흔들림 %d 뺌)' % (app, same_n, nfl), not bad_rows and same_n > 0, bad_rows[:10])
    else:   # 지시서 §B-2 = 조판기 사슬 두 번 — 자과는 참고로만
        I(g, '%s — 입력이 같은 하네스 %d · 다른 것 %d(흔들림 %d 뺌 · 지시서 §B-2 는 조판기만)' % (app, same_n, len(bad_rows), nfl), bad_rows[:10])


# ── B-6 옛 잣대 표 ────────────────────────────────────────────────────────────────────────────
def b6(md, runs):
    rows, ren, extra, files = stale_info(md)
    start = 0
    for app, rid1, rid2 in runs:
        for x in man(app, rid1)['rows']:
            if not x.get('skip'):
                r = rec(app, x)
                start += sum(1 for it in r['items'] if it['st'] == 'FAIL' and not it.get('b'))
    T('B-6', '표 줄 수 = 착수 때 저장본 판정 FAIL 수(조판기 · 자과)', len(rows) == start, {'표': len(rows), '저장본 FAIL': start})
    empty_a = [r['n'] for r in rows if r['cat'].startswith('a') and not r['ev'].strip('- ')]
    T('B-6', '(a) 줄마다 근거 칸 빔 0', not empty_a, empty_a[:10])
    und = [r['n'] for r in rows if r['cat'].startswith('?')]
    T('B-6', '안 가른 줄(?) 0', not und, und[:10])
    cats = {}
    for r in rows:
        cats[r['cat'][:1]] = cats.get(r['cat'][:1], 0) + 1
    I('B-6', '분류별 수', cats)
    fixed = fixed_set(rows)
    fl = flaky_set()
    gone, stray, chg_h, pinned = [], [], set(), set()
    # 고친 뒤 줄이 안 선 (a)(d) 줄(예외 · 실패 때만 찍는 전제 줄) — 지운 항목이 아니다 · 그 하네스는 예외가 풀려 새 줄이 선다
    unset = {(r['harness'], r['id']) for r in rows if r['after'].startswith('PASS(줄 안 섬')}
    unset_h = {h for h, _ in unset}
    r2ids = {(r['harness'], r['id']) for r in ROWS2}
    r2ids |= {(h, ren.get((h, i), i)) for h, i in r2ids}
    short = []
    crash_h = unset_h | {h for h, i in fixed if re.search(r'하니스가 터짐|묶음 예외|예외$|^\(항목 없음\)$|^\(오류\)$', i)}
    info_gone, bdrift = [], 0
    for app, rid1, rid2 in runs:
        by2 = {x['name']: x for x in man(app, rid2)['rows']}
        for x in man(app, rid1)['rows']:
            y = by2.get(x['name'])
            if x.get('skip') or not y or y.get('skip'):
                continue
            r1, r2 = rec(app, x), rec(app, y)
            ids2 = {it['id'] for it in r2['items']}
            for it in r1['items']:
                nid = ren.get((x['name'], it['id']), it['id'])
                if nid not in ids2 and (x['name'], it['id']) not in unset:
                    (gone if it['st'] in ('PASS', 'FAIL') else info_gone).append((x['name'], it['id']))
            if x['name'] in unset_h:
                ng = sum(1 for it in r1['items'] if (x['name'], it['id']) in unset)
                if len(r2['items']) < len(r1['items']) - ng:
                    short.append((x['name'], len(r1['items']), len(r2['items']), ng))
            if r1['keyparts']['h'] != r2['keyparts']['h']:
                chg_h.add(r1['harness'])
            if not same_inputs(r1, r2):
                hfix = any(h == x['name'] for h, _ in fixed)
                st1 = {it['id']: it['st'] for it in r1['items']}
                st2 = {it['id']: it['st'] for it in r2['items']}
                for k, nid, oid in cmp_items(x['name'], r1, r2, ren):
                    if k == '바탕 측정 바뀜' and st1.get(oid) and st1.get(oid) == st2.get(nid):
                        bdrift += 1          # 바탕 측정 줄 값만 바뀜(판정 그대로) — 측정 흔들림
                        continue
                    ok = ((x['name'], oid) in fixed or (x['name'], oid) in extra or (x['name'], nid) in fl or (x['name'], oid) in fl
                          or (k == '바탕 측정 바뀜' and hfix)   # 바탕을 박은 하네스의 바탕 측정 줄은 따라 바뀐다
                          or (x['name'], oid) in r2ids or (x['name'], nid) in r2ids   # 「고친 뒤 새로 선 FAIL」 절에 분류째 있음
                          or (k == '새 항목' and x['name'] in crash_h and st2.get(nid, '') != 'FAIL'))   # 예외·터짐을 고쳐(뒤로 밀린 것 포함) 새로 선 PASS·INFO 줄
                    if not ok:
                        stray.append((x['name'], k, oid[:90]))
    T('B-6', '지운 항목 0(이름 바뀜은 새 id 로 있음 · 예외·전제 줄이 고친 뒤 안 선 것 %d 은 「PASS(줄 안 섬)」)' % len(unset), not gone, gone[:10])
    I('B-6', '첫 실행에 있고 두 번째에 없는 INFO 줄(조건부로 찍히는 알림 · 판정 아님) %d' % len(info_gone), info_gone[:10])
    I('B-6', '바탕 측정 줄 — 판정 그대로 값만 바뀜(측정 흔들림 · 딴 항목으로 안 셈) %d' % bdrift, '')
    T('B-6', '「줄 안 섬」 하네스가 덜 돌지 않았다 — 두 번째 항목 수 ≥ 첫 실행 − 안 선 줄 수(%d 하네스)' % len(unset_h), not short, short[:10])
    und2 = [r['n'] for r in ROWS2 if r['cat'].startswith('?')]
    emp2 = [r['n'] for r in ROWS2 if r['cat'].startswith('a') and not r['ev'].strip('- ')]
    cat2 = {}
    for r in ROWS2:
        cat2[r['cat'][:1]] = cat2.get(r['cat'][:1], 0) + 1
    T('B-6', '「고친 뒤 새로 선 FAIL」 %d 줄 — 안 가른 줄(?) 0 · (a) 근거 빔 0' % len(ROWS2), not und2 and not emp2, {'?': und2[:10], '(a) 근거 빔': emp2[:10], '분류': cat2})
    left2 = [(r['harness'], r['id'][:60], r['cat']) for r in ROWS2 if not r['after'].startswith('PASS')]
    I('B-6', '「고친 뒤 새로 선 FAIL」 — 고쳐 PASS · 남은 FAIL(분류)', {'PASS': len(ROWS2) - len(left2), '남은': len(left2),
                                                              '남은 (a)(d)': [z for z in left2 if z[2][:1] in 'ad'][:20]})
    lf = {f for f in files if f.endswith('.py') and os.path.basename(f).startswith('_harness_')}
    T('B-6', '고친 하네스 파일(표 「고친 파일」 절) = 두 실행 사이 하네스 파일 해시가 바뀐 것(1:1)', lf == chg_h, {'표만': sorted(lf - chg_h), '실행만': sorted(chg_h - lf)})
    T('B-6', '고친 하네스에서 바뀐 항목 ⊆ (a)(d) 고침 줄 · 표 밖 고침 · 흔들림(다른 항목은 무변)', not stray, stray[:12])
    turned = [r for r in rows if (r['harness'], r['id']) in fixed and r['after'].startswith('PASS')]
    I('B-6', '(a)(d) 고쳐 FAIL → PASS 된 수 · 남은 FAIL', {'FAIL→PASS': len(turned), '남은 FAIL': len(rows) - len(turned),
                                                        '남은 (a)(d)': [(r['harness'], r['id'][:60]) for r in rows if (r['harness'], r['id']) in fixed and not r['after'].startswith('PASS')][:20]})



# ── B-7 시간 ──────────────────────────────────────────────────────────────────────────────────
def b7(tbl):
    t = jl(tbl)
    if not t:
        return T('B-7', '시간 표(--b7)', False, '없음')
    for k, v in t.get('rows', []):
        I('B-7', k, v)
    T('B-7', '같은 판(%s) — 새 절차(compare · 저장본 있음) %s분 < 착수 때 절차(전체 사슬 + 바탕 다시) %s분' % (t['ver'], t['new_min'], t['old_min']), t['new_min'] < t['old_min'], t.get('note', ''))


# ── B-8 회귀 — 새 실행기 결과 = 옛 절차 결과(A-6 고친 항목만 다름) ─────────────────────────────────────
def last_sec(t):
    """결과 파일의 마지막 실행 — 「==== 」 로 시작하는 머리 줄이 여럿이면 마지막 머리부터(옛 결과 파일은 개발 중 실행과 인도 실행이 이어져 있다 · 9/29 search 15:18 FAIL → 16:09 PASS)"""
    idx = [m.start() for m in re.finditer(r'(?m)^==== ', t)]
    return t[idx[-1]:] if idx else t


def b8(old, md=None):
    O = jl(old)
    if not O:
        return T('B-8', '옛 절차 결과 표(--old)', False, '없음')
    rows, ren, extra, files = stale_info(md)
    fixed = fixed_set(rows) | {(r['harness'], r['id']) for r in ROWS2 if r['cat'][:1] in 'ad' and r['fix'].strip('- ')}
    fl = flaky_set()
    r = subprocess.run([sys.executable, os.path.join(NR, '_qa_sync.py'), 'check'], capture_output=True, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    lines = r.stdout.decode('utf-8', 'replace').strip().splitlines() or ['']
    wip = O.get('wip', {})   # 병행 판의 아직 안 합친 N: 하네스 — {경로 조각: 까닭}
    warn = [x.strip()[1:].strip() for x in lines[1:] if x.strip().startswith('⚠')]
    unexp = [x for x in warn if not any(k.replace('/', '\\') in x or k in x for k in wip)]
    for x in warn:
        if x not in unexp:
            I('B-8', '_qa_sync check — 병행 판 칸: %s' % x[:120], next((v for k, v in wip.items() if k.replace('/', '\\') in x or k in x), ''))
    T('B-8', '_qa_sync check 통과(종료 코드 0 · 또는 남은 ⚠ 가 모두 병행 판의 아직 안 합친 하네스)', r.returncode == 0 or (warn and not unexp), {'첫 줄': lines[0][:300], '까닭 없는 ⚠': unexp[:8]})
    if O.get('env_lanes') and O['env_lanes'].get('args'):
        e = O['env_lanes']
        subprocess.run([sys.executable, os.path.join(NR, '_harness_env_lanes_fix.py')] + e['args'], capture_output=True, cwd=NR, timeout=7200)
        res = last_sec(io.open(e['res'], encoding='utf-8').read()) if os.path.exists(e['res']) else ''
        now = [(x['id'], x['st']) for x in QC.parse(res) if x['st'] in ('PASS', 'FAIL')]
        want = [(i, s) for i, s in e['want'] if s in ('PASS', 'FAIL')]
        wd, nd = dict(want), dict(now)
        diff = [(i, wd.get(i), nd.get(i)) for i in sorted(set(wd) | set(nd)) if wd.get(i) != nd.get(i)]
        ex = e.get('explained', {})
        unexp = [d for d in diff if not any(d[0].startswith(k) for k in ex)]
        for d in diff:
            k = next((k for k in ex if d[0].startswith(k)), None)
            I('B-8', 'env_lanes_fix 다른 칸 — %s : 인도 때 %s → 지금 %s' % (d[0][:90], d[1], d[2]), ex.get(k, '(까닭 없음)') if k else '(까닭 없음)')
        T('B-8', 'env_lanes_fix 관문 — 인도 때와 같은 PASS/FAIL(%d 항목) · 다른 칸은 모두 까닭 있음(이 판이 일부러 바꾼 것 · A-6 고침 · 환경)' % len(now), not unexp,
          {'다른 칸': len(diff), '까닭 없는 칸': unexp[:6], '지금 FAIL': [s for _, s in now].count('FAIL'), '인도 때 FAIL': [s for _, s in want].count('FAIL')})
    for app, pairs in O.get('chains', {}).items():
        bad, nitem, nfix, absent = [], 0, 0, []
        m = man(app, O['run'][app])
        for name, p in pairs.items():
            x = next((y for y in m['rows'] if y['name'] == name), None)
            if not x or x.get('skip') or not os.path.exists(p):
                continue
            new = {it['id']: it['st'] for it in rec(app, x)['items']}
            t = last_sec(io.open(p, encoding='utf-8', errors='replace').read().split('\n---stderr---\n')[0])
            oldi = {it['id']: it for it in QC.parse(t) if it['st'] in ('PASS', 'FAIL')}   # 「같은 PASS/FAIL」 — INFO 줄은 안 맞댐
            nitem += len(oldi)
            hfix = any(h == name for h, _ in fixed)
            d = []
            for i, it in oldi.items():
                ni = ren.get((name, i), i)
                if ni not in new:
                    b0 = re.sub(r' #\d+$', '', ni)          # 옛 결과 파일이 두 번 이어 붙어 생긴 「 #k」
                    ni = b0 if (b0 in new and b0 not in oldi) else ni   # 옛 결과 안에 원래 id 가 따로 있으면 「#k」 는 다른 줄
                if ni not in new:
                    absent.append((name, i[:80]))            # 새 결과에 없는 옛 줄(옛 하네스 판의 제목) — 맞댈 수 없다 · INFO
                    continue
                if new.get(ni) != it['st']:
                    if (name, i) in fixed or (name, i) in extra or (name, i) in fl or (name, ni) in fl or (it.get('b') and hfix):
                        nfix += 1
                        continue
                    d.append((i[:80], it['st'], new.get(ni)))
            ex = set(O.get('explained', {}).get(name, []))
            d2 = [z for z in d if z[0] not in ex]
            if d2:
                bad.append((name, len(d2), d2[:3]))
        I('B-8', '%s 사슬 — 새 결과에 없는 옛 PASS/FAIL 줄 %d(옛 결과가 다른 하네스 판에서 나와 제목이 다름 — 맞댈 수 없음)' % (app, len(absent)), absent[:12])
        T('B-8', '%s 사슬 — 새 실행기 결과 = 옛 절차 결과(같은 PASS/FAIL · 다른 것 = A-6 고친 항목 %d · 맞댄 옛 줄 %d)' % (app, nfix, nitem - len(absent)), not bad, bad[:8])


def main():
    t0 = time.time()
    try:
        if want('B1'):
            b1()
        if want('B2'):
            if ARG('--run1') and ARG('--run2'):
                b2('jo', ARG('--run1'), ARG('--run2'), md=ARG('--stale'))
            if ARG('--jrun1') and ARG('--jrun2'):
                b2('jagwa', ARG('--jrun1'), ARG('--jrun2'), 'B-2 자과', md=ARG('--stale'))
        if want('B3'):
            b3(ARG('--plant'))
        if want('B4'):
            b4()
        if want('B5'):
            b5()
        if want('B6') and ARG('--stale'):
            runs = [('jo', ARG('--run1'), ARG('--run2'))] + ([('jagwa', ARG('--jrun1'), ARG('--jrun2'))] if ARG('--jrun1') else [])
            b6(ARG('--stale'), runs)
        if want('B7'):
            b7(ARG('--b7'))
        if want('B8'):
            b8(ARG('--old'), ARG('--stale'))
    finally:
        if '--keep' not in sys.argv:
            drop_gate_wt()
    np_ = sum(1 for x in L if x.startswith('PASS'))
    nf = sum(1 for x in L if x.startswith('FAIL'))
    head = '==== %s · qa_baseline 관문 · N: 실행기 %s · PASS %d · FAIL %d · %d초 ====' % (time.strftime('%Y-%m-%d %H:%M'), QC.fmd5(QCP)[:8], np_, nf, time.time() - t0)
    print(head)
    io.open(OUTF, 'w', encoding='utf-8', newline='\n').write(head + '\n' + '\n'.join(L) + '\n')
    return 1 if nf else 0


if __name__ == '__main__':
    sys.exit(main())
