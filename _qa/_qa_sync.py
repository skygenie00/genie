# -*- coding: utf-8 -*-
"""genie/_qa/ 하네스 사본 맞추기 (_task_env_lanes 2026-09-29 A-2 · _task_env_lanes_fix A-2 · A-3 · A-4) — N: 이 정본 · _qa 는 사본(경로 모양 그대로)

  python _qa_sync.py list            모을 목록 · 크기 · 검사 · 클라우드 표(도는 / N: 필요) → _cloud_howto.md 의 표 칸을 이 산출로 갈아 끼움
  python _qa_sync.py copy            <GENIE_ROOT>/_qa/ 로 복사(바뀐 것만 · 되읽기) · N: 에서 없어진 파일은 _qa 에서도 지움 · 끝에 _d11_scan
  python _qa_sync.py check           _qa 전수 = N: 원본 바이트 · 스크립트(.py · .js) 말고 0 · 끝에 _d11_scan   (rc 1 = 어긋남 · 걸림)
  python _qa_sync.py import <브랜치> [--dry]
                                     클라우드 브랜치(origin/<브랜치>)에만 있는 _qa 새 파일 → N: 같은 상대 자리로 복사(정본)
                                     · _qa/ 맨 위에 놓인 파일은 이름으로 앱 줄 폴더를 정해 옮긴다(_harness_jo_* → jopangi/task/ …)
                                     · genie 가 그 브랜치를 이미 합쳤으면 genie 쪽도 git mv 로 그 자리로
                                     · 이미 N: 에 있고 바이트가 다르면 멈추고 diff 셈을 알린다
  모음 = _harness_*.py(_지울것 · _백업 · _이전 빼고) + 같은 폴더 _harness_*_tests.js + 하네스가 부르는 로컬 모듈(.py · 되풀이)
         + 하네스가 이름으로 여는 같은 폴더 .js + _roots.py
         + 사슬 실행기 셋(_qa_chain.py · _qa_chain_list.json · _qa_trace/sitecustomize.py — _task_qa_baseline A-7-4 · 클라우드에서도 실행기가 돈다)
  check 는 전수표(_qa_chain_list.json)도 잰다 — N: 정본 하네스마다 한 줄 · 없거나 남으면 FAIL(_task_qa_baseline A-7-3 · 새 하네스 판은 줄을 더하고 인도)
  ⚠ 저장본(_qa_results) · 흔들림(_qa_flaky.json) · 옛 잣대 표는 N: 에만 — _qa 에 안 넣는다(값에 사용자 기록이 섞일 수 있다)
  ⚠ 공개 저장소다 — 결과 .txt · 그림 · 기록 사본 · .pdf 는 안 넣는다. 워터마크·개인정보는 _d11_scan 이 copy · check 끝과 g_push 에서 본다.
  인도 차례: 하네스를 고친 판은 인도 때 `python _qa_sync.py copy` → `check` → g_push(PATHS 에 _qa).
  합치기 차례(클라우드 판): `import <브랜치>` → `check` → 회귀 → g_push.
"""
import ast, difflib, hashlib, os, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _roots   # noqa: E402
import _d11_scan   # noqa: E402
ROOT = HERE
SKIP = {'_지울것', '_백업', '_이전', '__pycache__', 'node_modules', '.git', '_qa_slim'}   # _qa_slim = _task_qa_slim 사본 · 결과 폴더(정본 하네스 모음 아님 · 10/4)
RX_MAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
RX_PHONE = re.compile(r"(?<!\d)01[016789][-\s.]?\d{3,4}[-\s.]?\d{4}(?!\d)")
RX_TOKEN = re.compile(r"(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|gho_[A-Za-z0-9]{20,})")
RX_NEED = re.compile(r"_roots\.need_n\(\s*(['\"])(.+?)\1")
RX_NOPT = re.compile(r"_roots\.n\(")
HOWTO = os.path.join(ROOT, '_cloud_howto.md')
TBL_A, TBL_B = '<!-- qa-table:start (python _qa_sync.py list 가 갈아 끼운다 · 손으로 고치지 말 것) -->', '<!-- qa-table:end -->'
# 클라우드가 _qa/ 맨 위에 둔 새 하네스의 N: 자리 — 이름 앞머리로(env_lanes_fix A-4)
ROUTE = [('_harness_jo_', 'jopangi/task/'), ('_harness_prec_', 'jopangi/공통/_harness/'), ('_harness_jagwa_', 'jagwa/'),
         ('_harness_earth_', 'jagwa/gigu/'), ('_harness_bio_', 'jagwa/saengmul/'), ('_harness_phys_', 'jagwa/moolri/'),
         ('_harness_ox_', 'minbeop/task/'), ('_harness_mb_', 'minbeop/task/'), ('_harness_tt_', 'timetable/')]
# 사슬 실행기(_task_qa_baseline) — _qa 에도 둔다 · _qa 안 스크립트 아닌 파일은 전수표 하나만
QA_TOOLS = ['_qa_chain.py', '_qa_chain_list.json', '_qa_trace/sitecustomize.py']
QA_DATA_OK = {'_qa_chain_list.json'}
CENSUS = os.path.join(ROOT, '_qa_chain_list.json')


def harnesses():
    out = []
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP]
        for fn in fns:
            if fn.startswith('_harness_') and fn.endswith('.py'):
                out.append(os.path.join(dp, fn))
    return sorted(out)


def local_imports(p):
    try:
        t = open(p, 'rb').read().decode('utf-8')
        tree = ast.parse(t)
    except Exception:
        return [], []
    names = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                names.add(a.name.split('.')[0])
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            names.add(n.module.split('.')[0])
    d = os.path.dirname(p)
    dirs = [d, os.path.dirname(d)]
    for m in re.finditer(r"os\.path\.join\(\s*(HERE|JOP|os\.path\.dirname\(HERE\))\s*,\s*((?:['\"][^'\"]+['\"]\s*,?\s*)+)\)", t):
        base = d if m.group(1) == 'HERE' else os.path.dirname(d)
        dirs.append(os.path.join(base, *re.findall(r"['\"]([^'\"]+)['\"]", m.group(2))))
    mods = []
    for nm in sorted(names):
        for dd in dirs:
            f = os.path.join(dd, nm + '.py')
            if os.path.isfile(f):
                mods.append(f); break
    js = [os.path.join(d, m.group(1)) for m in re.finditer(r"['\"]([\w\-가-힣]+\.js)['\"]", t) if os.path.isfile(os.path.join(d, m.group(1)))]
    return mods, js


def collect():
    todo, got = harnesses(), set()
    while todo:
        p = todo.pop()
        if p in got:
            continue
        got.add(p)
        mods, js = local_imports(p)
        todo += [f for f in mods if f not in got and not any(s in f.split(os.sep) for s in SKIP)]
        got.update(js)
        tj = p[:-3] + '_tests.js'
        if os.path.isfile(tj):
            got.add(tj)
    got.add(os.path.join(ROOT, '_roots.py'))
    for t in QA_TOOLS:
        f = os.path.join(ROOT, *t.split('/'))
        if os.path.isfile(f):
            got.add(f)
    return sorted(got)


def census_gap():
    """전수표 ↔ N: 정본 하네스 — 어긋난 줄 목록(빈 목록 = 맞음)"""
    import json
    try:
        with open(CENSUS, encoding='utf-8') as f:
            rows = json.load(f)['rows']
    except Exception as e:
        return ['전수표를 못 읽음(%s): %s' % (os.path.basename(CENSUS), e)]
    have = {r['file'] for r in rows}
    hs = {os.path.relpath(h, ROOT).replace(os.sep, '/') for h in harnesses()}
    return ['전수표에 줄 없음(새 하네스는 _qa_chain_list.json 에 한 줄 더할 것): ' + x for x in sorted(hs - have)] + \
           ['하네스 없는 전수표 줄: ' + x for x in sorted(have - hs)]


def need_of(p, memo):
    """그 파일(과 부르는 로컬 모듈)이 N: 을 꼭 요구하는가 → [까닭] · 선택으로만 쓰면 ['(선택)']"""
    if p in memo:
        return memo[p]
    memo[p] = []
    try:
        t = open(p, 'rb').read().decode('utf-8', 'replace')
    except Exception:
        return []
    out = [m.group(2) for m in RX_NEED.finditer(t)]
    if not out and RX_NOPT.search(t):
        out = ['(선택)']
    mods, _ = local_imports(p)
    for f in mods:
        out += [x for x in need_of(f, memo) if x != '(선택)' or not out]
    memo[p] = list(dict.fromkeys(out))
    return memo[p]


def table(files):
    memo = {}
    rows_ok, rows_n = [], []
    for f in files:
        rel = os.path.relpath(f, ROOT)
        if not os.path.basename(f).startswith('_harness_') or not f.endswith('.py'):
            continue
        need = need_of(f, memo)
        hard = [x for x in need if x != '(선택)']
        if hard:
            rows_n.append((rel, ' · '.join(hard)))
        else:
            rows_ok.append((rel, '일부 칸은 N: 없으면 건너뜀' if need else ''))
    L = [TBL_A, '',
         '하네스 %d = 클라우드에서 도는 것 %d · N: 필요(첫머리에서 「N: 필요 — 클라우드 불가(…)」 · 종료 코드 3) %d' % (len(rows_ok) + len(rows_n), len(rows_ok), len(rows_n)),
         '(브라우저 · 저장소 클론 같은 다른 준비는 하네스 머리글을 볼 것)', '',
         '| 클라우드에서 도는 하네스(`_qa/` 아래 자리) | 덧붙임 |', '|---|---|']
    L += ['| `%s` | %s |' % (r.replace(os.sep, '/'), n) for r, n in rows_ok]
    L += ['', '| 클라우드에서 못 도는 하네스 | 까닭(N: 에만 있는 것) |', '|---|---|']
    L += ['| `%s` | %s |' % (r.replace(os.sep, '/'), n) for r, n in rows_n]
    L += ['', TBL_B]
    return '\n'.join(L)


def put_table(tbl):
    t = open(HOWTO, 'rb').read().decode('utf-8')
    nl = '\r\n' if '\r\n' in t else '\n'
    t = t.replace('\r\n', '\n')
    if TBL_A in t and TBL_B in t:
        a = t.index(TBL_A); b = t.index(TBL_B) + len(TBL_B)
        t2 = t[:a] + tbl + t[b:]
    else:
        t2 = t.rstrip('\n') + '\n\n## 6. 클라우드에서 도는 하네스 · 못 도는 하네스\n\n' + tbl + '\n'
    if t2 != t:
        open(HOWTO, 'wb').write(t2.replace('\n', nl).encode('utf-8'))
    return t2 != t


def d11_tree(Q):
    """_qa 전부 _d11_scan — (걸림 수, 줄)"""
    H = _d11_scan.load_hash(); allow = _d11_scan.load_allow()
    if H is None:
        return 1, ['  ⚠ _d11_hash.txt 를 못 읽었다 — 워터마크 검사 못 함(밀지 말 것)']
    hits = []
    for name, t in _d11_scan.texts_from_files(_d11_scan.walk([Q])):
        if t is None:
            hits.append('  ⚠ 못 읽음 %s' % os.path.relpath(name, Q)); continue
        for ln, k in _d11_scan.scan_text(t, H, os.path.relpath(name, Q), allow):
            hits.append('  ⚠ d11 %s:%d · %s' % (os.path.relpath(name, Q), ln, k))
    return len(hits), hits


def git(*a, repo=None):
    return subprocess.run(['git', '-C', repo or _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True)


def route(rel):
    """_qa/ 맨 위 파일 이름 → N: 상대 자리(모르면 None)"""
    base = os.path.basename(rel)
    stem = re.sub(r'_tests\d*[a-z]*\.js$', '.py', base) if base.endswith('.js') else base
    for pre, d in ROUTE:
        if stem.startswith(pre):
            return d + base
    return None


def do_import(branch, dry):
    G = _roots.genie()
    ref = branch if branch.startswith('origin/') else 'origin/' + branch
    git('fetch', '-q', 'origin', '+refs/heads/%s:refs/remotes/%s' % (ref[len('origin/'):], ref))
    tip = git('rev-parse', '--verify', '-q', ref).stdout.decode().strip()
    if not tip:
        print('NG 브랜치 없음:', ref); return 1
    base = git('merge-base', 'main', ref).stdout.decode().strip()
    merged = git('merge-base', '--is-ancestor', ref, 'HEAD').returncode == 0
    if merged:   # 이미 합친 가지 — 갈래점이 가지 끝과 같아져 「바뀐 것 0」이 된다 → 그 가지를 합친 커밋의 첫 부모(합치기 앞 main)와의 갈래점에서 잰다
        mc = [x for x in git('rev-list', '--ancestry-path', '--merges', '--reverse', '%s..main' % ref).stdout.decode().split() if x]
        if mc:
            b2 = git('merge-base', mc[0] + '^1', ref).stdout.decode().strip()
            if b2:
                base = b2
    rows = [l.split('\t') for l in git('diff', '--name-status', '--no-renames', base, ref, '--', '_qa/').stdout.decode('utf-8').split('\n') if l.strip()]
    print('import %s(%s) · 바탕 %s · genie HEAD 에 합쳐짐 %s · _qa 바뀐 파일 %d' % (ref, tip[:7], base[:7], '예' if merged else '아니오', len(rows)))
    plan, stop = [], []
    for st, path in rows:
        if st.startswith('D'):
            print('  지움(브랜치에서) — N: 은 안 건드린다:', path); continue
        rel = path[len('_qa/'):]
        top = '/' not in rel
        dest = route(rel) if top else rel
        if not dest:
            stop.append((path, '맨 위 파일인데 이름으로 자리를 못 정함')); continue
        blob = git('show', '%s:%s' % (ref, path)).stdout
        dn = os.path.join(ROOT, *dest.split('/'))
        if os.path.isfile(dn):
            cur = open(dn, 'rb').read()
            if cur == blob:
                plan.append((path, dest, 'N: 에 같은 바이트 있음(건너뜀)', top)); continue
            a = cur.decode('utf-8', 'replace').replace('\r\n', '\n').split('\n'); b = blob.decode('utf-8', 'replace').replace('\r\n', '\n').split('\n')
            dl = [l for l in difflib.unified_diff(a, b, lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
            stop.append((path, 'N: %s 에 이미 있고 다르다 — 빠진 줄 %d · 더한 줄 %d(멈춤 · 사람이 가른다)' % (dest, sum(1 for l in dl if l[0] == '-'), sum(1 for l in dl if l[0] == '+')))); continue
        plan.append((path, dest, 'N: 로 복사(새 정본)', top))
    for p, d, how, top in plan:
        print('  %s → N: %s · %s%s' % (p, d, how, ' · genie 는 _qa/%s 로 git mv%s' % (d, '' if merged else '(합친 뒤)') if top else ''))
    for p, why in stop:
        print('  ⚠ 멈춤 %s — %s' % (p, why))
    if dry or stop:
        print('마른 연습 — 쓰지 않았다' if dry else 'NG 멈춤 — 쓰지 않았다')
        return 1 if stop else 0
    for p, d, how, top in plan:
        if how.startswith('N: 에 같은'):
            continue
        blob = git('show', '%s:%s' % (ref, p)).stdout
        dn = os.path.join(ROOT, *d.split('/'))
        os.makedirs(os.path.dirname(dn), exist_ok=True)
        open(dn, 'wb').write(blob)
        if open(dn, 'rb').read() != blob:
            sys.exit('NG 되읽기 ' + dn)
        print('  복사 N:', d)
        if top and merged and os.path.isfile(os.path.join(G, *p.split('/'))):
            r = git('mv', p, '_qa/' + d)
            print('  genie git mv %s → _qa/%s rc=%d' % (p, d, r.returncode))
    print('끝 — 다음: python _qa_sync.py check → 회귀 → g_push(맨 위 파일은 _roots 머리 5줄이 있는지 보고, 없으면 넣어 N: 과 _qa 를 같이 고친다)')
    return 0


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'check'
    Q = _roots.genie('_qa')
    if mode == 'import':
        args = [a for a in sys.argv[2:] if not a.startswith('--')]
        if not args:
            sys.exit('쓰는 법: python _qa_sync.py import <브랜치> [--dry]')
        sys.exit(do_import(args[0], '--dry' in sys.argv))
    files = collect()
    rels = [os.path.relpath(f, ROOT) for f in files]
    if mode == 'list':
        warn = 0
        for f, rel in zip(files, rels):
            t = open(f, 'rb').read().decode('utf-8', 'replace')
            k = {'mail': len(RX_MAIL.findall(t)), 'phone': len(RX_PHONE.findall(t)), 'token': len(RX_TOKEN.findall(t))}
            if any(k.values()):
                warn += 1; print('  ⚠', rel, k)
        print('파일 %d · %d KB · 살필 것 %d(메일 · 전화 꼴 · 토큰 꼴 — 눈으로 보고 판단)' % (len(files), sum(os.path.getsize(f) for f in files) // 1024, warn))
        tbl = table(files)
        print(tbl)
        print('_cloud_howto.md 표 %s' % ('갈아 끼움' if put_table(tbl) else '같음(그대로)'))
    elif mode == 'copy':
        n = 0
        for f, rel in zip(files, rels):
            b = open(f, 'rb').read(); dst = os.path.join(Q, rel)
            if os.path.isfile(dst) and open(dst, 'rb').read() == b:
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, 'wb').write(b)
            if open(dst, 'rb').read() != b:
                sys.exit('NG 되읽기 ' + dst)
            n += 1
        gone = 0
        want = set(rels)
        for dp, dns, fns in os.walk(Q):
            for fn in fns:
                rel = os.path.relpath(os.path.join(dp, fn), Q)
                if rel not in want:
                    os.remove(os.path.join(dp, fn)); gone += 1
        nh, hits = d11_tree(Q)
        print('복사 %d · 지움 %d · 모음 %d → %s · d11 걸림 %d' % (n, gone, len(files), Q, nh))
        for x in hits[:20]:
            print(x)
        sys.exit(1 if nh else 0)
    else:
        bad, diff, total = [], [], 0
        want = set(rels)
        for dp, dns, fns in os.walk(Q):
            dns[:] = [d for d in dns if d not in SKIP]   # 10/1 — 하네스가 _qa/_roots.py 를 불러 생긴 __pycache__ 는 사본이 아니다(셈·대조 밖 · 올리지도 않는다)
            for fn in fns:
                total += 1
                q = os.path.join(dp, fn); rel = os.path.relpath(q, Q)
                if not fn.endswith(('.py', '.js')) and rel.replace(os.sep, '/') not in QA_DATA_OK:
                    bad.append(rel)
                src = os.path.join(ROOT, rel)
                if not os.path.isfile(src) or open(src, 'rb').read() != open(q, 'rb').read():
                    diff.append(rel)
        miss = sorted(want - {os.path.relpath(os.path.join(dp, fn), Q) for dp, _, fns in os.walk(Q) if not (set(os.path.relpath(dp, Q).split(os.sep)) & SKIP) for fn in fns})
        nh, hits = d11_tree(Q)
        gap = census_gap()
        print('_qa 파일 %d · 모음 %d · 스크립트 아닌 것 %d · N: 원본과 다른 것 %d · 빠진 것 %d · d11 걸림 %d · 전수표 어긋남 %d' % (
            total, len(files), len(bad), len(diff), len(miss), nh, len(gap)))
        for x in (bad + diff + miss)[:20]:
            print('  ⚠', x)
        for x in hits[:20]:
            print(x)
        for x in gap[:20]:
            print('  ⚠', x)
        sys.exit(1 if (bad or diff or miss or nh or gap) else 0)


if __name__ == '__main__':
    main()
