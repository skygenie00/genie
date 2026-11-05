# -*- coding: utf-8 -*-
r"""_task_env_lanes_fix §B 관문 — _roots 조각 · N: 필요 하네스 · D11 넷째 가드 · 클라우드 하네스 들여오기 · .cmd 줄끝 · N: git 남기기

  python _harness_env_lanes_fix.py --orig <착수 때 원본 보관본 폴더> [--dirty6 <md5 목록>] [--b7 <앞/뒤 로그 셋 쌍>] [--only b1,...] [--res <결과>]
  헛잣대 = 착수 때 상태(원본 보관본의 _roots.py · g_push.cmd · 하네스들)에서 같은 잣대가 FAIL 이어야 한다.
  ⚠ push 는 임시 bare 저장소로만(g_push 길 넷) — 진짜 genie 원격은 안 건드린다.
  ⚠ 가짜 메일·전화·토큰 값은 이 파일에 글자로 두지 않는다(실행 중에 붙여 만든다) — 이 파일이 _qa 로 가도 _d11_scan 에 안 걸리게.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
NR = _roots.need_n('N: 도구 · 원본 보관본 · g_push.cmd')   # env_lanes_fix — 클라우드에서는 「N: 필요」 종료 코드 3
import ast, hashlib, importlib.util, io, json, os, posixpath, re, shutil, subprocess, sys, tempfile, time, types   # noqa: E402
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, NR)
import _d11_scan as D   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


ORIG = ARG('--orig')
DIRTY6 = ARG('--dirty6')
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(NR, '_harness_env_lanes_fix_result.txt'))
G0 = _roots.genie()
RES = []
BS = chr(92)


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:500]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:500]), flush=True)


def git(repo, *a, inp=None, env=None):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True, input=inp, env=env)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def fakes():
    """가짜 값 셋 — 글자로 두지 않고 붙여 만든다"""
    at = chr(64)
    return {'mail': 'elf.check' + at + 'example' + '.org', 'phone': '0' + '10' + '-' + '9876' + '-' + '5432', 'token': 'gh' + 'p_' + 'A1b2C3d4E5f6G7h8I9j0K1l2'}


# ══════════ B-1 _roots 조각(A-1) ══════════
QA32 = [('jo' + BS + 'data', ('jo', 'data'), 'd'), ('timetable' + BS + 'index.html', ('timetable', 'index.html'), 'f'), ('jagwa' + BS + 'index.html', ('jagwa', 'index.html'), 'f')]
SAMPLE_QA = ['jopangi/task/_harness_jo_revfix0929.py', 'timetable/_harness_tt_claudetab.py', 'jagwa/_harness_jagwa_uid.py']


def shim():
    s = types.SimpleNamespace(**{k: getattr(os, k) for k in dir(os) if not k.startswith('__')})
    s.sep = '/'; s.path = posixpath; s.name = 'posix'
    return s


def frags_of(p):
    """그 파일의 _roots.genie/spd/mbpdf(r'…') 조각 — (함수, 조각)"""
    t = open(p, encoding='utf-8', errors='replace').read()
    return [(m.group(1), m.group(3)) for m in re.finditer(r"_roots\.(genie|spd|mbpdf)\(r?(['\"])([^'\"]+)\2\)", t) if BS in m.group(3)]


def b1():
    R = load(os.path.join(NR, '_roots.py'), 'r_new')
    same = {a: R.genie(a) == R.genie(*b) for a, b, _ in QA32}
    same['jo/data'] = R.genie('jo/data') == R.genie('jo', 'data')
    ex = {a: os.path.exists(R.genie(a)) for a, _, _ in QA32}
    T('B-1', '윈도 — genie(r"jo\\data") = genie("jo","data") · "/" 조각도 같음 · 그 자리 있음', all(same.values()) and all(ex.values()), {'같음': same, '있음': ex})
    # 리눅스 흉내(os.sep='/' · posixpath) — _qa 표본 셋 파일의 \ 조각이 가리키는 자리를 임시 뿌리에 만들어 두고 잰다
    tmp = tempfile.mkdtemp(prefix='elf_b1_').replace(BS, '/')
    fr = []
    for rel in SAMPLE_QA:
        fr += [(f, g) for f, g in frags_of(_roots.genie('_qa', *rel.split('/')))]
    fr = list(dict.fromkeys(fr))
    for f, g in fr:
        p = posixpath.join(tmp, f, *g.split(BS))
        if '.' in g.split(BS)[-1]:
            os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w').close()
        else:
            os.makedirs(p, exist_ok=True)
    old_env = {k: os.environ.get(k) for k in ('GENIE_ROOT', 'SPD_ROOT', 'MBPDF_ROOT')}
    try:
        for f in ('genie', 'spd', 'mbpdf'):
            os.environ[{'genie': 'GENIE_ROOT', 'spd': 'SPD_ROOT', 'mbpdf': 'MBPDF_ROOT'}[f]] = posixpath.join(tmp, f)
        L = load(os.path.join(NR, '_roots.py'), 'r_lin'); L.os = shim()
        lin = lambda p: BS not in p and os.path.exists(p)   # 리눅스에서는 \\ 가 구분자가 아니다 — 윈도 파일시스템이 받아 주는 것에 속지 않게 글자로도 본다
        got = {'%s(%s)' % (f, g): lin(getattr(L, f)(g)) for f, g in fr}
        T('B-1', '리눅스 흉내 — _qa 표본 셋(%s)의 \\ 조각 %d 이 가리키는 자리 있음' % (' · '.join(os.path.basename(x) for x in SAMPLE_QA), len(fr)), fr and all(got.values()), got)
        O = load(os.path.join(ORIG, '_roots.py'), 'r_old'); O.os = shim()
        gold = {'%s(%s)' % (f, g): lin(getattr(O, f)(g)) for f, g in fr}
        T('B-1-헛', '헛잣대 — 착수 때 _roots 는 리눅스에서 \\ 조각을 한 이름으로 붙여 못 찾는다', fr and not any(gold.values()), gold)
    finally:
        for k, v in old_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(tmp, ignore_errors=True)


# ══════════ B-2 N: 필요 하네스(A-2) ══════════
NEED3 = ['jopangi/공통/_harness/_harness_jo_ms_omrpop.py', 'minbeop/task/_harness_ox_claude_fig.py', 'timetable/_harness_cha2_report_tt.py']
LIT = re.compile(r"r(['\"])(N:" + re.escape(BS) + "개인" + re.escape(BS) + r"claude(?:" + re.escape(BS) + r"[^'\"]*)?)\1")


def run_py(path, env, timeout):
    p = subprocess.Popen([sys.executable, path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, cwd=os.path.dirname(path))
    try:
        out, _ = p.communicate(timeout=timeout)
        return p.returncode, out.decode('utf-8', 'replace')
    except subprocess.TimeoutExpired:
        subprocess.run(['taskkill', '/F', '/T', '/PID', str(p.pid)], capture_output=True)
        return 'TIMEOUT', ''


def eval_paths(src, fpath):
    """고친 파일에서 N: 자리를 만드는 식(os.path.join(NR|_NR|__file__ …) · _roots.n(…) · NR/_NR 한 이름)의 값 — N_ROOT 기본으로"""
    tree = ast.parse(src)
    envd = {'os': os, '_roots': _roots, 'NR': NR, '_NR': NR, '__file__': fpath, 'ARG': lambda k, d=None: d}
    vals = []
    for node in ast.walk(tree):
        seg = ast.get_source_segment(src, node) or ''
        if isinstance(node, ast.Call) and ('NR' in seg or '__file__' in seg or '_roots.n(' in seg):
            f = ast.get_source_segment(src, node.func) or ''
            if f in ('os.path.join', '_roots.n', 'os.path.dirname', 'os.path.abspath'):   # __file__ 기준 식(같은 폴더 · 위 폴더)도 값으로
                try:
                    vals.append(eval(compile(ast.Expression(node), '<e>', 'eval'), envd))
                except Exception:
                    pass
        elif isinstance(node, ast.Name) and node.id in ('NR', '_NR') and isinstance(node.ctx, ast.Load):
            vals.append(NR)
    return vals


def b2():
    env = dict(os.environ, N_ROOT=os.path.join(tempfile.gettempdir(), 'elf_no_N_%d' % os.getpid()), PYTHONIOENCODING='utf-8')
    res = {}
    for rel in NEED3:
        rc, out = run_py(_roots.genie('_qa', *rel.split('/')), env, 120)
        lines = [l for l in out.split('\n') if l.strip()]
        res[rel] = [rc, lines[:2]]
    ok = all(v[0] == 3 and len(v[1]) == 1 and v[1][0].startswith('N: 필요 — 클라우드 불가(') for v in res.values())
    T('B-2', 'N_ROOT 없음(클라우드 흉내) — _qa 표본 셋 → 종료 코드 3 + 「N: 필요 — 클라우드 불가(…)」 한 줄', ok, res)
    old = {}
    for rel in NEED3:
        rc, out = run_py(os.path.join(ORIG, *rel.split('/')), env, 25)
        old[rel] = rc
    T('B-2-헛', '헛잣대 — 착수 때 판은 N: 없음을 모르고 그냥 돈다(종료 코드 3 아님)', all(v != 3 for v in old.values()), old)
    # 있으면 지금과 같음 — 20 파일: 옛 글자 자리(r'N:\…') 모음 = 새 식 값 모음
    m0 = sorted({r for r in _manifest() if r.endswith('.py') and os.path.isfile(os.path.join(ORIG, r)) and LIT.search(open(os.path.join(ORIG, r), encoding='utf-8').read())})
    bad = {}
    for rel in m0:
        o = open(os.path.join(ORIG, rel), encoding='utf-8').read(); n = open(os.path.join(NR, rel), encoding='utf-8').read()
        ov = sorted({os.path.normcase(os.path.normpath(m.group(2))) for m in LIT.finditer(o)})
        nv = sorted({os.path.normcase(os.path.normpath(v)) for v in eval_paths(n, os.path.join(NR, rel)) if isinstance(v, str)})
        left = LIT.findall(n)
        if left or not set(ov) <= set(nv):
            bad[rel] = {'옛': ov, '새': nv, '남은 글자': len(left)}
    T('B-2', 'N: 있으면 지금과 같음 — 고친 %d 파일의 옛 고정 자리 = 새 식 값(N_ROOT 기본) · 고정 글자 남음 0' % len(m0), m0 and not bad, bad or {'파일': len(m0)})
    # howto 표 = list 산출
    r = subprocess.run([sys.executable, os.path.join(NR, '_qa_sync.py'), 'list'], capture_output=True, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    out = r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n')
    a, b = '<!-- qa-table:start', '<!-- qa-table:end -->'
    hw = open(os.path.join(NR, '_cloud_howto.md'), encoding='utf-8').read().replace('\r\n', '\n')
    t_out = out[out.index(a):out.index(b) + len(b)] if a in out and b in out else ''
    t_hw = hw[hw.index(a):hw.index(b) + len(b)] if a in hw and b in hw else ''
    n_need = len(re.findall(r'^\| `[^`]+` \| (?!일부|\s*\|)', t_out.split('| 클라우드에서 못 도는 하네스')[-1], re.M)) if t_out else 0
    T('B-2', 'howto 표 = `_qa_sync.py list` 산출(글자 같음) · 못 도는 하네스에 까닭', bool(t_out) and t_out == t_hw and n_need > 0, {'표 줄': t_out.count('\n'), 'N: 필요 줄': n_need})


def _manifest():
    p = os.path.join(os.path.dirname(ORIG), 'orig_manifest.json')
    return list(json.load(open(p, encoding='utf-8')).keys()) if os.path.isfile(p) else []


# ══════════ B-3 D11 넷째 가드(A-3) ══════════
def b3():
    F = fakes()
    tmp = tempfile.mkdtemp(prefix='elf_b3_')
    fs = {}
    for k, v in F.items():
        p = os.path.join(tmp, 'fake_%s.txt' % k); open(p, 'w', encoding='utf-8').write('앞 글 %s 뒤 글\n' % v); fs[k] = p
    r = subprocess.run([sys.executable, os.path.join(NR, '_d11_scan.py')] + list(fs.values()), capture_output=True, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    out = r.stdout.decode('utf-8', 'replace')
    kinds = {k: ('메일 꼴' if k == 'mail' else '휴대전화 꼴' if k == 'phone' else '토큰 꼴') in ''.join(l for l in out.split('\n') if os.path.basename(fs[k]) in l) for k in F}
    leak = [k for k, v in F.items() if v in out or v.replace('-', '') in out]
    T('B-3', '가짜 메일·전화·토큰 → _d11_scan 걸림(종료 코드 1) · 꼴 이름만 · 출력에 값 0', r.returncode == 1 and all(kinds.values()) and not leak, {'rc': r.returncode, '꼴': kinds, '값 샘': leak})
    H = [(3, hashlib.md5('가나다'.encode('utf-8')).hexdigest(), 'test-name')]
    hit = D.scan_text('시험 가나다라 끝\n다른 줄\n', H, 'x.txt', [])
    T('B-3', '워터마크 해시 길 — 해시와 맞는 조각이 든 줄만 「워터마크(이름)」(합성 해시로)', hit == [(1, '워터마크(test-name)')], hit)
    shutil.rmtree(tmp, ignore_errors=True)
    # _qa 전부 + N: 도구(맨 위 .py · .cmd) 걸림 0
    q = subprocess.run([sys.executable, os.path.join(NR, '_d11_scan.py'), '--tree', _roots.genie('_qa')], capture_output=True, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    tools = sorted(f for f in os.listdir(NR) if f.lower().endswith(('.py', '.cmd')))
    t2 = subprocess.run([sys.executable, os.path.join(NR, '_d11_scan.py')] + [os.path.join(NR, f) for f in tools], capture_output=True, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    T('B-3', '_qa 전부 · N: 도구(맨 위 .py · .cmd %d) 걸림 0' % len(tools), q.returncode == 0 and t2.returncode == 0,
      {'_qa': q.stdout.decode('utf-8', 'replace').strip().split('\n')[-1], '도구': t2.stdout.decode('utf-8', 'replace').strip().split('\n')[-1]})


# ══════════ B-5 · B-3 g_push 길(임시 bare 저장소) ══════════
def mk_repos():
    root = tempfile.mkdtemp(prefix='elf_gp_')
    bare, clone = os.path.join(root, 'remote.git'), os.path.join(root, 'clone')
    subprocess.run(['git', 'init', '-q', '--bare', '--initial-branch=main', bare], capture_output=True)
    subprocess.run(['git', 'clone', '-q', bare, clone], capture_output=True)
    idn = ['-c', 'user.name=elf', '-c', 'user.email=elf' + chr(64) + 'invalid.test']
    git(clone, 'switch', '-q', '-c', 'main')
    os.makedirs(os.path.join(clone, 'jagwa'))
    open(os.path.join(clone, 'index.html'), 'w').write('<p>elf</p>\n')
    open(os.path.join(clone, 'jagwa', 'a.txt'), 'w').write('a\n')
    git(clone, 'add', '-A'); git(clone, *idn, 'commit', '-q', '-m', 'init'); git(clone, 'push', '-q', '-u', 'origin', 'main')
    git(clone, 'config', 'user.name', 'elf'); git(clone, 'config', 'user.email', 'elf' + chr(64) + 'invalid.test')
    return root, bare, clone


def run_gpush(cmd, clone, answer):
    env = dict(os.environ, GENIE_ROOT=clone, PYTHONIOENCODING='')
    env.pop('PYTHONIOENCODING', None)
    env['PATH'] = os.path.join(os.environ.get('SystemRoot', 'C:' + BS + 'Windows'), 'System32') + os.pathsep + env.get('PATH', '')
    p = subprocess.Popen(['cmd', '/c', cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    try:
        out, _ = p.communicate(input=(answer + '\r\n\r\n').encode('ascii'), timeout=240)
        return out.decode('cp949', 'replace')
    except subprocess.TimeoutExpired:
        subprocess.run(['taskkill', '/F', '/T', '/PID', str(p.pid)], capture_output=True)
        git(clone, 'reset', '-q')
        return 'TIMEOUT'


def head(repo, ref='HEAD'):
    return git(repo, 'rev-parse', ref).stdout.decode().strip()


def b5():
    GP = os.path.join(NR, 'g_push.cmd')
    # .cmd 줄끝 · 글자 무변
    rows = {}
    for f in sorted(x for x in os.listdir(NR) if x.lower().endswith('.cmd')):
        b = open(os.path.join(NR, f), 'rb').read()
        o = os.path.join(ORIG, f)
        ob = open(o, 'rb').read().replace(b'\r\n', b'\n') if os.path.isfile(o) else None
        nb = b.replace(b'\r\n', b'\n')
        if f == 'g_push.cmd' and ob is not None:   # 이 판이 넣은 D11 덩어리는 빼고 대조
            nb = re.sub(rb'rem ---- guard 4 .*?\n\n', b'', nb, flags=re.S).replace(b'rem  Refuses if _d11_scan.py finds personal data or a watermark (guard 4).\n', b'')
        rows[f] = {'CRLF=줄': b.count(b'\r\n') == b.count(b'\n') and b.count(b'\n') > 0, '글자 같음': ob == nb if ob is not None else '원본 없음', 'ASCII': all(c < 128 for c in b)}
    T('B-5', '맨 위 .cmd %d 전부 CRLF 수 = 줄 수 · 글자 무변(CR 뺀 바이트 = 착수 때 · g_push 는 D11 덩어리 빼고) · ASCII' % len(rows),
      all(v['CRLF=줄'] and v['글자 같음'] is True and v['ASCII'] for v in rows.values()), rows)
    oldcrlf = {f: (open(os.path.join(ORIG, f), 'rb').read().count(b'\r\n') > 0) for f in rows if os.path.isfile(os.path.join(ORIG, f))}
    T('B-5-헛', '헛잣대 — 착수 때 LF 뿐인 .cmd 가 있었다', any(not v for v in oldcrlf.values()), {f: ('CRLF' if v else 'LF') for f, v in oldcrlf.items()})
    root, bare, clone = mk_repos()
    try:
        o1 = run_gpush(GP, clone, 'N')
        T('B-5', 'g_push :nostage · 밀 것 0 → 「nothing to push」', 'nothing to push' in o1, [l for l in o1.split('\n') if '[g]' in l][:4])
        open(os.path.join(clone, 'jagwa', 'a.txt'), 'a').write('b\n')
        git(clone, 'add', 'jagwa/a.txt'); git(clone, 'commit', '-q', '-m', 'ahead')
        o2 = run_gpush(GP, clone, 'N')
        T('B-5', 'g_push :nostage → 안 민 커밋 1 → :pushonly(pull --rebase · push) → 임시 bare 에 도착', 'never pushed' in o2 and 'OK - pushed' in o2 and head(bare, 'main') == head(clone),
          [l for l in o2.split('\n') if '[g]' in l][:6])
        open(os.path.join(clone, 'jagwa', 'a.txt'), 'a').write('c\n')
        o3 = run_gpush(GP, clone, 'Y')
        T('B-5', 'g_push 보통 길 — stage · D11 통과 · Y · commit · push → 임시 bare 에 도착', '[d11]' in o3 and 'OK - pushed' in o3 and head(bare, 'main') == head(clone),
          [l for l in o3.split('\n') if '[g]' in l or '[d11]' in l][:8])
        F = fakes()
        open(os.path.join(clone, 'jagwa', 'b.txt'), 'w', encoding='utf-8').write('글 %s 끝\n' % F['mail'])
        h0 = head(bare, 'main')
        o4 = run_gpush(GP, clone, 'Y')
        st = git(clone, 'diff', '--cached', '--name-only').stdout.decode().strip()
        T('B-3', 'g_push — 가짜 메일이 든 파일을 stage → D11 거부 · reset(스테이징 0) · 안 밂 · 출력에 값 0',
          'NG - personal data' in o4 and st == '' and head(bare, 'main') == h0 and F['mail'] not in o4, [l for l in o4.split('\n') if '[g]' in l or '[d11]' in l][:6])
        if os.path.isfile(os.path.join(ORIG, 'g_push.cmd')):
            o5 = run_gpush(os.path.join(ORIG, 'g_push.cmd'), clone, 'N')
            T('B-3-헛', '헛잣대 — 착수 때 g_push 는 같은 파일을 안 막고 묻는 데까지 간다(N 으로 취소)', 'NG - personal data' not in o5 and 'will be pushed' in o5,
              [l for l in o5.split('\n') if '[g]' in l][:5])
    finally:
        shutil.rmtree(root, ignore_errors=True)


# ══════════ B-4 클라우드 하네스 들여오기(A-4) ══════════
def b4():
    Q = os.path.join(NR, '_qa_sync.py')
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    r = subprocess.run([sys.executable, Q, 'import', 'cloud/jo_joscreen0929', '--dry'], capture_output=True, env=env)
    out = r.stdout.decode('utf-8', 'replace')
    route_ok = 'jopangi/task/_harness_jo_joscreen0929.py' in out and '_qa/_harness_jo_joscreen0929.py' in out
    T('B-4', 'import cloud/jo_joscreen0929 --dry — 맨 위 _qa/_harness_jo_joscreen0929.py → N: jopangi/task/ 자리 · 이미 합쳐 N: 에 (손본 판이) 있어 「다르다 · 멈춤」 · 안 씀', route_ok and '멈춤' in out,
      [l for l in out.split('\n') if l.strip()][:6])
    # 합성 가지 — 맨 위 하나 + 자리 있는 하나(규약 꼴) · 진짜 원격엔 없다(로컬 ref 만 · 끝나면 지움)
    body = ('# -*- coding: utf-8 -*-\n"""합성 — env_lanes_fix B-4"""\nprint("elf")\n').encode('utf-8')
    tmpidx = os.path.join(tempfile.gettempdir(), 'elf_idx_%d' % os.getpid())
    e2 = dict(os.environ, GIT_INDEX_FILE=tmpidx)
    try:
        git(G0, 'read-tree', 'main', env=e2)
        blob = git(G0, 'hash-object', '-w', '--stdin', inp=body).stdout.decode().strip()
        for pth in ('_qa/_harness_jo_elf_fake.py', '_qa/jopangi/task/_harness_jo_elf_fake2.py'):
            git(G0, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (blob, pth), env=e2)
        tree = git(G0, 'write-tree', env=e2).stdout.decode().strip()
        cm = git(G0, '-c', 'user.name=elf', '-c', 'user.email=elf' + chr(64) + 'invalid.test', 'commit-tree', tree, '-p', 'main', '-m', 'elf fake', env=e2).stdout.decode().strip()
        git(G0, 'update-ref', 'refs/remotes/origin/cloud/elf_fake', cm)
        r2 = subprocess.run([sys.executable, Q, 'import', 'cloud/elf_fake', '--dry'], capture_output=True, env=env)
        o2 = r2.stdout.decode('utf-8', 'replace')
        ok = ('_qa/_harness_jo_elf_fake.py → N: jopangi/task/_harness_jo_elf_fake.py · N: 로 복사(새 정본) · genie 는 _qa/jopangi/task/_harness_jo_elf_fake.py 로 git mv(합친 뒤)' in o2
              and '_qa/jopangi/task/_harness_jo_elf_fake2.py → N: jopangi/task/_harness_jo_elf_fake2.py · N: 로 복사(새 정본)' in o2 and r2.returncode == 0
              and not os.path.exists(os.path.join(NR, 'jopangi', 'task', '_harness_jo_elf_fake.py')))
        T('B-4', '합성 가지(맨 위 1 · 규약 자리 1) --dry — 들어올 N: 자리 · genie 옮길 자리 표 · N: 에 안 씀', ok, [l for l in o2.split('\n') if l.strip()][:5])
    finally:
        git(G0, 'update-ref', '-d', 'refs/remotes/origin/cloud/elf_fake')
        try:
            os.remove(tmpidx)
        except OSError:
            pass
    old = os.path.join(ORIG, '_qa_sync.py')
    if os.path.isfile(old):
        r3 = subprocess.run([sys.executable, old, 'import', 'cloud/jo_joscreen0929', '--dry'], capture_output=True, env=env)
        o3 = r3.stdout.decode('utf-8', 'replace')
        T('B-4-헛', '헛잣대 — 착수 때 _qa_sync 에는 import 가 없다(모르는 모드 = check 로 떨어짐)', 'import' not in o3.split('\n')[0] and '→ N:' not in o3, [l for l in o3.split('\n') if l.strip()][:2])


# ══════════ B-6 N: git 에 남기기(A-6) ══════════
def b6():
    GIT = ['git', '-c', 'core.excludesFile=N:/개인/claude/gitignore', '-c', 'core.quotepath=false', '--git-dir=N:/개인/claude-git', '--work-tree=N:/개인/claude']
    tracked = set(subprocess.run(GIT + ['ls-files'], capture_output=True).stdout.decode('utf-8').split('\n'))
    want = [l.strip() for l in open(os.path.join(os.path.dirname(ORIG), 'a6_commit_list.txt'), encoding='utf-8') if l.strip()]
    miss = [w for w in want if w not in tracked]
    T('B-6', 'env_lanes 가 바꾼 추적 밖 + _qa 에 실린 추적 밖 %d → N: git 추적' % len(want), want and not miss, miss[:6] or {'추적': len(want)})
    if DIRTY6 and os.path.isfile(DIRTY6):
        rows = [l.split(None, 1) for l in open(DIRTY6, encoding='utf-8') if l.strip()]
        ch = {p.strip(): hashlib.md5(open(os.path.join(NR, p.strip()), 'rb').read()).hexdigest() == h for h, p in rows}
        st = subprocess.run(GIT + ['status', '--porcelain', '--'] + [p.strip() for _, p in rows], capture_output=True).stdout.decode('utf-8')
        T('B-6', '전부터 고침 %d(사용자 몫) — 작업트리 바이트 무변 · 커밋 안 함(여전히 「 M」)' % len(rows), all(ch.values()) and st.count(' M ') == len(rows), {'무변': ch, '상태': st.strip().split('\n')})


# ══════════ B-7 회귀 ══════════
def summ(p):
    t = io.open(p, encoding='utf-8', errors='replace').read()
    m = re.findall(r'== PASS (\d+) · FAIL (\d+)', t)
    if m:
        return [int(x) for x in m[-1]]
    return [len(re.findall(r'^PASS', t, re.M)), len(re.findall(r'^FAIL', t, re.M))]


def fails(p):
    t = io.open(p, encoding='utf-8', errors='replace').read()
    return sorted(re.sub(r'\d+(\.\d+)?(ms|s|초)\b', '#', l.strip())[:200] for l in t.split('\n') if l.strip().startswith('FAIL'))


# 알려진 흔들림 — 앞/뒤 대조에서 빼고 INFO 로 따로 적는다(숨기지 않음) · (하네스 이름, 항목 제목 앞머리, 근거)
FLAKY = [('phone_win', '9 · chromium [개념] 다 펼침 — 그림 68 장 깨짐 0',
          '그림 불러오기 흔들림 — 9/29 17:11 결정로그 「그림 로드 흔들림(바탕도 같음)」 · 9/30 앞 2 번 FAIL(깨진 그림이 매번 다름) · 뒤 3 번 PASS · 옛/새 _roots 가 앱·그림·기록 자리를 글자까지 같게 냄')]


def b7():
    q = subprocess.run([sys.executable, os.path.join(NR, '_qa_sync.py'), 'check'], capture_output=True, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    T('B-7', '_qa_sync check — _qa = N: 바이트 · 스크립트만 · d11 걸림 0', q.returncode == 0, q.stdout.decode('utf-8', 'replace').strip().split('\n')[0])
    i = sys.argv.index('--b7') if '--b7' in sys.argv else -1
    if i > 0:
        args = sys.argv[i + 1:i + 1 + 8]
        for k in range(0, len(args), 2):
            a, b = args[k], args[k + 1]
            nm = os.path.basename(b).replace('_after', '').replace('.log', '')
            fl = [(pre, why) for h, pre, why in FLAKY if h == nm]
            isfl = lambda x: any(x.startswith('FAIL | ' + pre) for pre, _ in fl)
            fa, fb = [x for x in fails(a) if not isfl(x)], [x for x in fails(b) if not isfl(x)]
            na, nb = [x for x in fails(a) if isfl(x)], [x for x in fails(b) if isfl(x)]
            sa, sb = summ(a), summ(b)
            same_n = (sa[0] + sa[1]) == (sb[0] + sb[1]) and sa[1] - len(na) == sb[1] - len(nb)
            T('B-7', '하네스 표본 %s — 고치기 앞과 같음(항목 수 · 흔들림 뺀 FAIL 수 · FAIL 제목)' % nm, same_n and fa == fb, {'앞': sa, '뒤': sb, '흔들림 뺀 FAIL': [len(fa), len(fb)]})
            if na or nb:
                N('B-7', '하네스 표본 %s — 알려진 흔들림(대조에서 뺌 · 숨기지 않음)' % nm, {'앞': [x[:110] for x in na], '뒤': [x[:110] for x in nb], '근거': [w for _, w in fl]})


def main():
    t0 = time.time()
    if not ORIG or not os.path.isdir(ORIG):
        sys.exit('--orig <착수 때 원본 보관본 폴더> 가 필요하다')
    for k, fn in (('b1', b1), ('b2', b2), ('b3', b3), ('b4', b4), ('b5', b5), ('b6', b6), ('b7', b7)):
        if ONLY and k not in ONLY:
            continue
        try:
            fn()
        except Exception:
            import traceback
            T('RUN', '%s 멈춤' % k, False, traceback.format_exc()[-700:])
    npass = sum(1 for r in RES if r[2]); nfail = sum(1 for r in RES if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · env_lanes_fix · genie HEAD %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), git(G0, 'rev-parse', '--short', 'HEAD').stdout.decode().strip()))
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ('INFO' if ok is None else ('PASS' if ok else 'FAIL'), g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:1500]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
