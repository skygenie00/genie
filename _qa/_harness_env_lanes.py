# -*- coding: utf-8 -*-
r"""_task_env_lanes §B 관문 — 줄(lane) 정비: GENIE_ROOT · _qa/ · ⚙ 자동 푸시 · g_push · 나란히 시연

  python _harness_env_lanes.py --orig <원본 보관 폴더> --census <el_census.json>
                               [--b1 <앞 로그 r29> <뒤 로그 r29> <앞 로그 shell> <뒤 로그 shell>] [--b6 <시연 기록.json>]
                               [--only b1,b2,b3,b4,b5,b6] [--res <결과>]
  헛잣대 = 착수 때 상태 — 원본 보관본(바꾸기 전 파일)으로 같은 잣대를 대어 FAIL 이어야 한다(B-7).
  ⚠ push 는 하지 않는다 — ⚙ 는 워크트리(줄)에서만 실제로 돌리고 원격(ls-remote)이 무변인지 잰다 · g_push 는 N 으로 취소(stage → reset).
"""
import io, json, os, re, shutil, subprocess, sys, tempfile, time, importlib.util
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _roots   # noqa: E402
NR = _roots.need_n('N: 도구 · ⚙ jopangi · g_push.cmd · 원본 보관본')   # env_lanes_fix(9/29) — N: 작업 폴더 · 없으면(클라우드) 「N: 필요 — 클라우드 불가(…)」 종료 코드 3


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


ORIG = ARG('--orig')
CENSUS = ARG('--census')
B6 = ARG('--b6')
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_env_lanes_result.txt'))
G0 = _roots.DEFAULT['GENIE_ROOT']
RES = []
NAMES = r'(genie|studyplandata|minbeoppdf)(?![\w-])'
RX_FIXED = re.compile(r"Documents[\\/]{1,2}" + NAMES + r"|['\"]Documents['\"]\s*,\s*['\"]" + NAMES + r"|C:[\\/]{1,2}Users[\\/]{1,2}[^\\/'\"]+[\\/]{1,2}Documents[\\/]{1,2}" + NAMES, re.I)
ALLOW = re.compile(r"^\s*if not defined (GENIE_ROOT|SPD_ROOT|MBPDF_ROOT) set ", re.I)


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:500]), flush=True)


def git(repo, *a):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True, text=True, encoding='utf-8', errors='replace')


def env_with(**kw):
    e = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
    for k in ('GENIE_ROOT', 'SPD_ROOT', 'MBPDF_ROOT'):
        e.pop(k, None)
    e.update({k: v for k, v in kw.items() if v is not None})
    return e


def fixed_lines(base_dir, files):
    """파일마다 고정 자리 줄 수(허용: _roots.py · .cmd 의 if not defined *_ROOT set 줄)"""
    out = {}
    for rel in files:
        p = os.path.join(base_dir, rel)
        if not os.path.isfile(p):
            continue
        t = open(p, 'rb').read().decode('utf-8', 'replace')
        n = sum(1 for ln in t.split('\n') if RX_FIXED.search(ln) and not ALLOW.search(ln))
        if n:
            out[rel] = n
    return out


# ══════════ B-1 자리 전수 · 옛 하네스 결과 같음 ══════════
def fails(p):
    t = io.open(p, encoding='utf-8', errors='replace').read()
    return sorted(re.sub(r'\d+(\.\d+)?(ms|s|초)\b', '#', l.strip())[:200] for l in t.split('\n') if l.strip().startswith('FAIL'))


def summ(p):
    t = io.open(p, encoding='utf-8', errors='replace').read()
    m = re.findall(r'== PASS (\d+) · FAIL (\d+)', t)
    if m:
        return [int(x) for x in m[-1]]
    return [len(re.findall(r'^PASS', t, re.M)), len(re.findall(r'^FAIL', t, re.M))]


def b1():
    rows = json.load(open(CENSUS, encoding='utf-8'))
    files = sorted({r[0] for r in rows if os.path.splitext(r[0])[1].lower() in ('.py', '.cmd')})
    now = fixed_lines(NR, files)
    T('B-1', 'A-1-1 표의 파일 %d 에서 고정 자리 0(허용 = _roots.py · .cmd 의 if not defined *_ROOT set 줄)' % len(files), not now, dict(list(now.items())[:8]))
    before = fixed_lines(ORIG, files)
    T('B-1-헛', '헛잣대 — 착수 때(원본 보관본) 고정 자리 %d 파일 · %d 줄' % (len(before), sum(before.values())), bool(before), dict(list(before.items())[:3]))
    i = sys.argv.index('--b1') if '--b1' in sys.argv else -1
    if i > 0:
        rb, ra, sb, sa = sys.argv[i + 1:i + 5]
        T('B-1', '옛 하네스 _harness_jo_revfix0929.py(GENIE_ROOT 없음) — 착수 때와 같음(PASS/FAIL 수 · FAIL 제목)', summ(rb) == summ(ra) and fails(rb) == fails(ra), {'앞': summ(rb), '뒤': summ(ra)})
        T('B-1', '옛 하네스 _harness_earth_shell.py phys 묶음(GENIE_ROOT 없음) — 착수 때와 같음', summ(sb) == summ(sa) and fails(sb) == fails(sa), {'앞': summ(sb), '뒤': summ(sa)})


# ══════════ B-2 워크트리를 잰다 ══════════
def make_wt(name):
    wt = os.path.join(G0, '.claude', 'worktrees', name)
    if os.path.exists(wt):
        git(G0, 'worktree', 'remove', '--force', wt)
    r = git(G0, 'worktree', 'add', '--detach', wt, 'HEAD')
    if r.returncode:
        raise RuntimeError('worktree add ' + r.stderr[-300:])
    return wt


def drop_wt(wt):
    git(G0, 'worktree', 'remove', '--force', wt)
    git(G0, 'worktree', 'prune')


def b2():
    JP = os.path.join(NR, 'jopangi', 'task')
    F = os.path.join(G0, 'jo', 'data', 'jimun_7pan.json')
    raw = open(F, 'rb').read()
    A, B = 'ㄱ. ㄷ. ㅁ. (O)'.encode('utf-8'), 'ㄱ. ㄷ. ㅁ. (X)'.encode('utf-8')
    if raw.count(A) < 1:
        T('B-2', '표본 글자 없음', False, ''); return
    wt = make_wt('el-b2')
    line = '16 줄 sol = 표의 옛 sol(바이트)'
    try:
        open(F, 'wb').write(raw.replace(A, B, 1))   # 본 폴더만 한 글자 바꿈(워크트리는 그대로)
        run = lambda env: subprocess.run([sys.executable, '_harness_jo_revfix0929.py', '--new', os.path.join(env.get('GENIE_ROOT') or G0, 'jo', 'index.html'), '--only', 'd1', '--res', os.path.join(tempfile.gettempdir(), 'el_b2_res.txt')],
                                         cwd=JP, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
        o_wt = run(env_with(GENIE_ROOT=wt))
        o_main = run(env_with())
    finally:
        open(F, 'wb').write(raw)
        drop_wt(wt)
    ok_wt = any(l.startswith('PASS') and line in l for l in o_wt.split('\n'))
    ok_main = any(l.startswith('FAIL') and line in l for l in o_main.split('\n'))
    T('B-2', 'GENIE_ROOT = 임시 워크트리 → 하네스가 워크트리를 잰다(본 폴더에 바꿔 둔 한 글자를 못 봄 · d1 「%s」 PASS)' % line, ok_wt,
      [l[:120] for l in o_wt.split('\n') if line in l])
    T('B-2-헛', '헛잣대 — GENIE_ROOT 없음 = 본 폴더를 잰다(바꿔 둔 글자를 봄 · 같은 줄 FAIL)', ok_main, [l[:120] for l in o_main.split('\n') if line in l])
    T('B-2', '본 폴더 파일 되돌림(바이트)', open(F, 'rb').read() == raw, '')


# ══════════ B-3 _qa 사본 ══════════
def b3():
    Q = os.path.join(G0, '_qa')
    bad, diff, total = [], [], 0
    for dp, dns, fns in os.walk(Q):
        for fn in fns:
            total += 1
            q = os.path.join(dp, fn); rel = os.path.relpath(q, Q)
            if not fn.endswith(('.py', '.js')) or fn.lower().endswith(('.pdf', '.txt', '.png', '.jpg', '.json')):
                bad.append(rel)
            src = os.path.join(NR, rel)
            if not os.path.isfile(src) or open(src, 'rb').read() != open(q, 'rb').read():
                diff.append(rel)
    T('B-3', '_qa/ 사본 %d = N: 원본과 바이트 같음 · 스크립트(.py · .js) 말고 0 · .pdf · .txt · 그림 · 기록 0' % total, total > 0 and not bad and not diff, {'다름': diff[:5], '스크립트 아닌 것': bad[:5]})
    tracked = git(G0, 'ls-files', '_qa').stdout.split('\n')
    pdf = [x for x in tracked if x.lower().endswith('.pdf')]
    T('B-3', '_qa/ 안 .pdf 0(추적 · 작업트리)', not pdf and not any(f.lower().endswith('.pdf') for _, _, fs in os.walk(Q) for f in fs), pdf[:3])


# ══════════ B-4 ⚙ 자동 푸시 ══════════
def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def b4():
    JOP = os.path.join(NR, 'jopangi')
    wt = make_wt('el-b4')
    remote0 = git(G0, 'ls-remote', 'origin', 'refs/heads/main').stdout.split()[:1]
    log0 = git(G0, 'rev-parse', 'origin/main').stdout.strip()
    try:
        git(wt, 'switch', '-c', 'worktree-el-b4')
        # 헛잣대 — 착수 때 clone_root 는 GENIE_ROOT 를 안 본다(본 폴더를 가리킨다)
        old_env = dict(os.environ)
        os.environ['GENIE_ROOT'] = wt
        try:
            new_cr = load_mod(os.path.join(JOP, 'stage_jo.py'), 'stage_jo_new').clone_root()
            old_cr = load_mod(os.path.join(ORIG, 'jopangi', 'stage_jo.py'), 'stage_jo_old').clone_root() if os.path.isfile(os.path.join(ORIG, 'jopangi', 'stage_jo.py')) else None
        finally:
            os.environ.clear(); os.environ.update(old_env)
        nrm = lambda p: os.path.normcase(os.path.normpath(p or ''))
        T('B-4', '⚙ 클론 자리 = GENIE_ROOT(워크트리)', nrm(new_cr) == nrm(wt), new_cr)
        T('B-4-헛', '헛잣대 — 착수 때 clone_root 는 GENIE_ROOT 를 무시하고 본 폴더를 가리킨다', old_cr is not None and nrm(old_cr) == nrm(G0), old_cr)
        # 실제로 ⚙ 를 줄에서 돌린다(잠금은 따로 · push 0 을 잰다)
        lockdir = tempfile.mkdtemp(prefix='el_lock_')
        e = env_with(GENIE_ROOT=wt, MBPDF_ROOT=tempfile.mkdtemp(prefix='el_mbpdf_')); e['LOCALAPPDATA'] = lockdir   # 해설 짝(minbeoppdf)은 「클론 없음」으로 건너뛰게 — 진짜 minbeoppdf 에 커밋 안 함
        t0 = time.time()
        r = subprocess.run([sys.executable, 'jo_pipe.py'], cwd=JOP, env=e, capture_output=True, text=True, encoding='utf-8', errors='replace')
        out = (r.stdout or '') + (r.stderr or '')
        last = [l for l in out.split('\n') if l.strip()][-3:]
        remote1 = git(G0, 'ls-remote', 'origin', 'refs/heads/main').stdout.split()[:1]
        log1 = git(G0, 'rev-parse', 'origin/main').stdout.strip()
        wtlog = git(wt, 'log', '--oneline', '-2').stdout.strip().split('\n')
        pipe_log = open(os.path.join(JOP, '공통', '_pipeline', '_last_run.md'), encoding='utf-8').read()
        lane_line = [l for l in pipe_log.split('\n') if '줄(워크트리' in l]
        T('B-4', '워크트리 브랜치에서 ⚙(jo_pipe · push 옵션 없이) → 줄 판정 · commit 만 · push 0(원격 ls-remote 무변 · origin/main 무변)',
          remote0 == remote1 and log0 == log1 and bool(lane_line) and r.returncode == 0,
          {'끝 줄': last, '줄 로그': lane_line[:2], '워크트리 커밋': wtlog, '원격': [remote0, remote1], '%.0f초' % (time.time() - t0): ''})
        m = load_mod(os.path.join(JOP, 'jo_pipe.py'), 'jo_pipe_main')
        T('B-4', '본 폴더 main 에서는 줄 아님(지금과 같이 commit·pull·push 길)', m.lane_info() == (False, 'main'), m.lane_info())
    finally:
        drop_wt(wt)
        git(G0, 'branch', '-D', 'worktree-el-b4')


# ══════════ B-5 g_push ══════════
def run_gpush(cmd_path, env):
    """g_push 를 N 으로 취소하며 돌린다 — PATH 맨 앞 = System32(Git Bash 의 유닉스 find 가 윈도 find.exe 를 가리면 C: 전체를 훑다 멈춘다)"""
    env = dict(env); sysdir = os.path.join(os.environ.get('SystemRoot', r'C:\Windows'), 'System32')
    env['PATH'] = sysdir + os.pathsep + env.get('PATH', '')
    p = subprocess.Popen(['cmd', '/c', cmd_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    try:
        out, _ = p.communicate(input=b'N\r\n\r\n', timeout=240)
        return out.decode('cp949', 'replace')
    except subprocess.TimeoutExpired:
        subprocess.run(['taskkill', '/F', '/T', '/PID', str(p.pid)], capture_output=True)   # 그 프로세스 나무만
        git(G0, 'reset', '-q')   # 묻는 데서 멈췄으면 stage 만 된 채다 — 비운다
        return 'TIMEOUT'


def b5():
    GP = os.path.join(NR, 'g_push.cmd')
    wt = make_wt('el-b5')
    try:
        git(wt, 'switch', '-c', 'worktree-el-b5')
        o_wt = run_gpush(GP, env_with(GENIE_ROOT=wt))
        o_main = run_gpush(GP, env_with())
        st_after = git(G0, 'diff', '--cached', '--name-only').stdout.strip()
        o_old = run_gpush(os.path.join(ORIG, 'g_push.cmd'), env_with(GENIE_ROOT=wt)) if os.path.isfile(os.path.join(ORIG, 'g_push.cmd')) else ''
        st_old = git(G0, 'diff', '--cached', '--name-only').stdout.strip()
    finally:
        drop_wt(wt)
        git(G0, 'branch', '-D', 'worktree-el-b5')
    T('B-5', 'g_push — GENIE_ROOT = 워크트리 브랜치 → 거부(「not main」 · stage 0)', 'not main' in o_wt and 'staging only' not in o_wt, [l for l in o_wt.split('\n') if '[g]' in l][:3])
    T('B-5', 'g_push — 본 폴더 main → 지금과 같다(stage 목록 · N 으로 취소 · reset · stage 남음 0)', ('staging only' in o_main and 'Cancelled' in o_main) or ('nothing to push' in o_main),
      [l for l in o_main.split('\n') if '[g]' in l][:6])
    T('B-5', 'g_push 뒤 본 폴더 스테이징 0', st_after == '', st_after[:200])
    T('B-5-헛', '헛잣대 — 착수 때 g_push 는 GENIE_ROOT 를 무시하고 본 폴더(main)를 stage 했다', bool(o_old) and 'not main' not in o_old and 'staging only' in o_old and 'repo: ' + G0 in o_old,
      [l for l in o_old.split('\n') if '[g]' in l][:3])
    T('B-5', '헛잣대 실행 뒤에도 스테이징 0(N 취소 · reset)', st_old == '', st_old[:200])


# ══════════ B-6 나란히 시연 기록 ══════════
def b6():
    if not B6 or not os.path.isfile(B6):
        T('B-6', '나란히 시연 기록 없음', False, B6); return
    d = json.load(open(B6, encoding='utf-8'))
    T('B-6', '줄 다른 가짜 판 둘(jo · jagwa)을 워크트리 하위 에이전트 둘로 — 각자 커밋 · 본 세션이 main 에 둘 다 합침 · 부딪힘 0 · push 0 · 로컬 main 되돌림',
      d.get('lanes') == 2 and all(d.get('commits', {}).values()) and d.get('conflicts') == 0 and d.get('merged') == 2 and d.get('pushed') == 0 and d.get('main_reset'),
      d)


def main():
    t0 = time.time()
    for k, fn in (('b1', b1), ('b2', b2), ('b3', b3), ('b4', b4), ('b5', b5), ('b6', b6)):
        if ONLY and k not in ONLY:
            continue
        try:
            fn()
        except Exception as e:
            import traceback
            T('RUN', '%s 멈춤' % k, False, traceback.format_exc()[-600:])
    npass = sum(1 for r in RES if r[2]); nfail = sum(1 for r in RES if not r[2])
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · env_lanes · genie HEAD %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), git(G0, 'rev-parse', '--short', 'HEAD').stdout.strip()))
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ('PASS' if ok else 'FAIL', g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:1500]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
