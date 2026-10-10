# -*- coding: utf-8 -*-
"""_task_qa_bigguard_1010 §E 관문 — 큰 판 회귀의 낭비를 실행기가 스스로 막는가(모래상자 · N: 무접촉 · 클라우드에서도 됨 · 2026-10-10)

  python _harness_qa_bigguard.py [--qc <_qa_chain.py>] [--only E1,E2,E3,E4] [--res <결과 파일>] [--yard] [--base-rev 43c09e0] [--keep]
     --qc   = 잴 실행기(기본: 이 폴더 위 _qa_chain.py)
     --yard = 헛잣대도 — 바탕 실행기(genie <--base-rev>:_qa/_qa_chain.py · _roots.py · _qa_trace/sitecustomize.py)를 모래상자에 꺼내 같은 잣대(다 FAIL 이어야 잣대가 산다)
  E1 저장본 있는 판 → 안 돎 · --fresh 만 = 거부(종료 코드 2) · --fresh --why = 돎(까닭이 실행 기록에) · compare 새 판 저장본도 기본으로 씀 ·
     (잼) 새 판 결과 = 다음 판 바탕(바탕 다시 안 돎 — 열쇠가 같음)
  E2 --affected 자체 시험 셋 — genie 실제 이력 · 실제 전수표(사본) · 실제 하네스 소스로 plan 이 고른 하네스:
     4ce28d0..e7fd97b(CSS 세 줄) = jagwa_g3tx · smoke 하나 · 67e423e..783799b(uid 묶음 · 기록 열쇠) = 공용 → 전체 · 1b4a4c2..2340c46(「+회독」) = 공용 → 전체
  E3 가짜 사슬 어림 150 분 → 덩어리 둘 · 첫 덩어리 중간에 죽임 → 같은 명령을 다시 부르면 끝난 하네스 건너고 남은 것만 · 시간 예산(--budget) 멈춤 = 종료 코드 4 → 다시 부르면 나머지
  E4 _eta.txt 가 하네스마다 바뀜(남은 수 줄어듦) · 가짜 last_sec(남은 하네스 어림)를 늘리면 「★ 밀림 +N 분 · 까닭(가장 늦은 하네스 셋)」 · _code_now.md 「회귀」 칸 덮어씀
  모래상자 = 임시 폴더(가짜 genie 저장소 chem/index.html 판 셋 · 가짜 하네스 · 전수표 · 저장본 · 잠금 자리) — 실행기 환경 QA_CHAIN_LIST · HHOME · WORK · RES · FLAKY · PA · NOW
  · E2 만 genie 실제 저장소를 읽는다(쓰지 않음 · 워크트리 안 만듦) · push 0 · N: 무접촉
"""
import os as _os_r, sys as _sys_r   # env_lanes — _roots.py 를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import glob
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
QA = os.path.dirname(HERE)                                   # genie\_qa 또는 N:\개인\claude


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


QC = os.path.abspath(ARG('--qc', os.path.join(QA, '_qa_chain.py')))
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
BASE_REV = ARG('--base-rev', '43c09e0')
GENIE = _roots.root('GENIE_ROOT')
SB = tempfile.mkdtemp(prefix='qa_bigguard_')
OUTF = ARG('--res', os.path.join(tempfile.gettempdir(), '_harness_qa_bigguard_result.txt'))   # 모래상자는 끝에 지운다 — 결과는 밖에
NAMES = ['fk_%02d' % i for i in range(1, 11)]
L = []
SUM = {}


def T(g, title, ok, val='', who='new'):
    v = val if isinstance(val, str) else json.dumps(val, ensure_ascii=False)
    if who == 'new':
        s = ('PASS' if ok else 'FAIL') + ' | ' + g + ' · ' + title + (' | ' + v[:1500] if v else '')
    else:
        s = 'INFO | 헛잣대 ' + g + ' · ' + title + ' | 바탕 실행기 ' + ('PASS' if ok else 'FAIL') + (' — ' + v[:900] if v else '')
    SUM.setdefault(who, {}).setdefault(g.split('-')[0], []).append((g, ok))
    L.append(s)
    print(s, flush=True)
    return ok


def I(title, val=''):
    s = 'INFO | ' + title + (' | ' + (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False))[:2500] if val != '' else '')
    L.append(s)
    print(s, flush=True)


def want(g):
    return not ONLY or g in ONLY


def git(repo, *a):
    r = subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True)
    return r.returncode, r.stdout.decode('utf-8', 'replace')


def jl(p, d=None):
    try:
        with open(p, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return d


# ── 모래상자 재료 ─────────────────────────────────────────────────────────────────────────────
APP_V = ['''<!doctype html><html><head><meta charset="utf-8"><style>
.fk1 .fk2{color:#123}
</style></head><body><div id="fkBox" class="fk1"><span class="fk2">시험</span></div>
<script>
function fkShared(x){return x+1}
function fkLocal(){return fkShared(1)+fkShared(2)+fkShared(3)}
</script></body></html>
''']
APP_V.append(APP_V[0].replace('color:#123', 'color:#456'))
APP_V.append(APP_V[1].replace('color:#456', 'color:#789'))
FAKE_H = r'''# -*- coding: utf-8 -*-
# 가짜 하네스(_harness_qa_bigguard 모래상자) — 돈 것을 exec.log 에 · FK_ETA 면 지금 끝 어림을 eta.log 에 · FK_INFLATE_AT 이면 남은 하네스 어림(가짜 last_sec)을 늘림
import json, os, sys, time
name = os.path.basename(__file__)[:-3].replace('_harness_', '')
sb = os.environ['FK_SB']
with open(os.path.join(sb, 'exec.log'), 'a', encoding='utf-8') as f:
    f.write('%s %s %d\n' % (os.environ.get('FK_TAG', ''), name, os.getpid()))
eta = os.environ.get('FK_ETA')
if eta:
    t = open(eta, encoding='utf-8').read().strip() if os.path.exists(eta) else '(없음)'
    with open(os.path.join(sb, 'eta.log'), 'a', encoding='utf-8') as f:
        f.write(name + '\t' + t.replace('\n', ' / ') + '\n')
inf = os.environ.get('FK_INFLATE')
if inf and os.environ.get('FK_INFLATE_AT') == name and os.path.exists(inf):
    st = json.load(open(inf, encoding='utf-8'))
    for n in list((st.get('plan') or {})):
        if n != name and n not in (st.get('finished') or {}):
            st['plan'][n] = float(st['plan'][n]) + float(os.environ.get('FK_INFLATE_SEC', '900'))
    with open(inf, 'w', encoding='utf-8') as f:
        f.write(json.dumps(st, ensure_ascii=False, indent=1))
time.sleep(float(os.environ.get('FK_SLEEP', '0.3')))
print('PASS | %s 한 칸 | ok' % name)
'''


def fake_genie():
    """가짜 genie 저장소 — chem/index.html 판 셋(c1 → c2 → c3 · CSS 한 줄씩)"""
    d = os.path.join(SB, 'genie')
    os.makedirs(os.path.join(d, 'chem'))
    git(d, 'init', '-q')
    git(d, 'config', 'user.email', 'qa-sandbox@localhost')
    git(d, 'config', 'user.name', 'qa sandbox')
    git(d, 'config', 'core.autocrlf', 'false')
    revs = []
    for i, t in enumerate(APP_V):
        with open(os.path.join(d, 'chem', 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(t)
        git(d, 'add', '-A')
        git(d, 'commit', '-q', '-m', 'v%d' % (i + 1))
        revs.append(git(d, 'rev-parse', 'HEAD')[1].strip())
    return d, revs


def fake_home():
    hh = os.path.join(SB, 'hh')
    os.makedirs(os.path.join(hh, 'chem'))
    for n in NAMES:
        with open(os.path.join(hh, 'chem', '_harness_%s.py' % n), 'w', encoding='utf-8', newline='\n') as f:
            f.write(FAKE_H + '# %s — 하네스마다 바이트가 달라야 열쇠가 갈린다\n' % n)
    return hh


def census(path, names, sec):
    rows = [{'file': 'chem/_harness_%s.py' % n, 'app': 'chem', 'chains': ['chem'], 'what': '가짜 하네스(모래상자)', 'tags': ['가짜'] + (['smoke'] if n == names[0] else []),
             'eng': [], 'inputs': ['genie:chem/index.html'], 'inputs_src': '추적', 'argv': {'*': []}, 'res': 'stdout', 'timeout': 120, 'last_sec': sec}
            for n in names]
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps({'v': 1, 'about': '모래상자', 'apps': {'chem': '화학'}, 'rows': rows}, ensure_ascii=False, indent=1) + '\n')
    return path


def env_for(g, cen, extra=None):
    d = os.path.join(SB, g)
    os.makedirs(d, exist_ok=True)
    e = {'QA_CHAIN_LIST': cen, 'QA_CHAIN_HHOME': HH, 'QA_CHAIN_WORK': os.path.join(d, 'work'), 'QA_CHAIN_RES': os.path.join(d, 'res'),
         'QA_CHAIN_FLAKY': os.path.join(d, 'flaky.json'), 'QA_CHAIN_PA': os.path.join(d, 'pa'), 'QA_CHAIN_NOW': os.path.join(d, '_code_now.md'),
         'GENIE_ROOT': FG}
    e.update(extra or {})
    return e


def clean_env():
    """사슬 실행기 밑에서 돌 때 — 바깥 추적 장치(QA_TRACE_* · sitecustomize)를 안쪽 실행기에 안 물림"""
    e = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
    for k in list(e):
        if k.startswith('QA_TRACE') or k.startswith('QA_CHAIN_') or k.startswith('FK_'):
            e.pop(k)
    if e.get('PYTHONPATH'):
        e['PYTHONPATH'] = os.pathsep.join(x for x in e['PYTHONPATH'].split(os.pathsep) if '_qa_trace' not in x)
    return e


def qc(qcp, args, env, tag, timeout=900, extra=None):
    e = clean_env()
    e.update(env)
    e.update({'FK_SB': SB, 'FK_TAG': tag})
    e.update(extra or {})
    t0 = time.time()
    r = subprocess.run([sys.executable, qcp] + args, capture_output=True, env=e, timeout=timeout, cwd=SB)
    out = r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')
    return r.returncode, out, round(time.time() - t0, 1)


def ran(tag):
    p = os.path.join(SB, 'exec.log')
    if not os.path.exists(p):
        return []
    return [ln.split()[1] for ln in open(p, encoding='utf-8') if ln.split() and ln.split()[0] == tag]


def last_run_manifest(g, app='chem'):
    fs = sorted(glob.glob(os.path.join(SB, g, 'res', app, '_runs', '*_run*.json')), key=os.path.getmtime)
    return jl(fs[-1]) if fs else None


# ── E1 저장본 있는 판 → 안 돎 · --fresh --why ───────────────────────────────────────────────────
def e1(qcp, who):
    g = 'e1_' + who
    cen = census(os.path.join(SB, g + '_census.json'), NAMES, 5.0)
    env = env_for(g, cen)
    C1, C2, C3 = REVS
    rc, out, sec = qc(qcp, ['run', 'chem', '--rev', C1], env, g + 'a')
    n0 = len(ran(g + 'a'))
    I('E1 %s 준비 — 첫 run(저장본 없음) · 돈 하네스 %d · rc %s · %.0f초' % (who, n0, rc, sec))
    rc, out, sec = qc(qcp, ['run', 'chem', '--rev', C1], env, g + 'b')
    nb = len(ran(g + 'b'))
    T('E1-1', '저장본 있는 판 다시 run(깃발 없음) → 안 돎', nb == 0 and n0 == 10 and out.count('저장본 그대로') >= 10,
      '돈 하네스 %d · 「저장본 그대로」 %d · rc %s' % (nb, out.count('저장본 그대로'), rc), who)
    rc, out, sec = qc(qcp, ['run', 'chem', '--rev', C1, '--fresh'], env, g + 'c')
    nc = len(ran(g + 'c'))
    T('E1-2', 'run --fresh 만(까닭 없음) → 거부 · 종료 코드 2', rc == 2 and nc == 0 and '--why' in out,
      'rc %s · 돈 하네스 %d · %s' % (rc, nc, (out.strip().splitlines() or [''])[-1][:160]), who)
    rc, out, sec = qc(qcp, ['run', 'chem', '--rev', C1, '--fresh', '--why', 'E1 다시 잼'], env, g + 'd')
    nd = len(ran(g + 'd'))
    man = last_run_manifest(g) or {}
    meta = man.get('meta') or {}
    T('E1-3', 'run --fresh --why → 돎 · 까닭이 실행 기록(_runs)에', rc == 0 and nd == 10 and meta.get('why') == 'E1 다시 잼' and meta.get('fresh') is True,
      '돈 하네스 %d · rc %s · 실행 기록 meta.why=%r · fresh=%r' % (nd, rc, meta.get('why'), meta.get('fresh')), who)
    rc, out, sec = qc(qcp, ['compare', 'chem', '--base', C1, '--rev', C2, '--all', '--why', 'E1 전체'], env, g + 'e')
    ne = len(ran(g + 'e'))
    I('E1 %s 준비 — compare c1→c2(바탕 저장본 있음) · 돈 하네스 %d · [바탕] %d · rc %s' % (who, ne, out.count('[바탕]'), rc))
    rc, out, sec = qc(qcp, ['compare', 'chem', '--base', C1, '--rev', C2, '--all', '--why', 'E1 전체'], env, g + 'f')
    nf = len(ran(g + 'f'))
    T('E1-4', '같은 compare 다시(깃발 없음) → 바탕 · 새 판 둘 다 저장본(안 돎)', nf == 0 and ne == 10,
      '돈 하네스 %d(앞 compare %d) · [바탕] %d · [새 판] %d · rc %s' % (nf, ne, out.count('[바탕]'), out.count('[새 판]'), rc), who)
    rc, out, sec = qc(qcp, ['compare', 'chem', '--base', C1, '--rev', C2, '--fresh'], env, g + 'g')
    ng = len(ran(g + 'g'))
    T('E1-5', 'compare --fresh 만 → 거부 · 종료 코드 2', rc == 2 and ng == 0 and '--why' in out, 'rc %s · 돈 하네스 %d' % (rc, ng), who)
    rc, out, sec = qc(qcp, ['compare', 'chem', '--base', C2, '--rev', C3, '--all', '--why', 'E1 다음 판'], env, g + 'h')
    nh = len(ran(g + 'h'))
    T('E1-6(잼)', 'push 한 판(c2)의 새 판 결과 = 다음 판(c2→c3) 바탕 저장본 — 바탕 다시 안 돎', out.count('[바탕]') == 0 and nh == 10,
      '[바탕] %d · 새 판에서 돈 하네스 %d · rc %s' % (out.count('[바탕]'), nh, rc), who)


# ── E2 --affected 자체 시험 셋 ────────────────────────────────────────────────────────────────
SELF = [('E2-1', '4ce28d0..e7fd97b', 'CSS 세 줄 → jagwa_g3tx · smoke 하나만'),
        ('E2-2', '67e423e..783799b', '자과 uid 묶음 · 기록 열쇠 → 공용 → 전체'),
        ('E2-3', '1b4a4c2..2340c46', '「+회독」 · 회독 함수 → 공용 → 전체')]
RX_ROW = re.compile(r'^(\S+)\s+바탕 [0-9a-f]{16} ', re.M)


def e2(qcp, who):
    g = 'e2_' + who
    cen = os.path.join(SB, g + '_census.json')
    shutil.copyfile(os.path.join(QA, '_qa_chain_list.json'), cen)
    c = jl(cen)
    rows = [r for r in c['rows'] if 'jagwa' in (r.get('chains') or [r['app']])]
    tags = {os.path.basename(r['file'])[:-3].replace('_harness_', ''): r.get('tags') or [] for r in rows}
    env = env_for(g, cen, {'QA_CHAIN_HHOME': QA, 'GENIE_ROOT': GENIE})
    for code, rng, what in SELF:
        a, b = rng.split('..')
        if git(GENIE, 'cat-file', '-e', a + '^{commit}')[0] or git(GENIE, 'cat-file', '-e', b + '^{commit}')[0]:
            T(code, what, False, 'genie 에 그 커밋이 없음(%s) — GENIE_ROOT 를 볼 것' % rng, who)
            continue
        rc, out, sec = qc(qcp, ['plan', 'jagwa', '--affected', rng], env, g + code, timeout=600)
        names = RX_ROW.findall(out)
        first = (out.strip().splitlines() or [''])[0]
        if code == 'E2-1':
            sm = [n for n in names if n != 'jagwa_g3tx']
            ok = (rc == 0 and 'jagwa_g3tx' in names and len(names) == 2 and len(sm) == 1 and 'smoke' in tags.get(sm[0], [])
                  and first.startswith('== 고름') and '공용 층 안 건드림' in first)
        else:
            ok = rc == 0 and len(names) == len(rows) and first.startswith('== 고름') and '공용 층 건드림' in first and \
                (code != 'E2-3' or ('qFillSel' in first or 'qPaint' in first))
        T(code, '%s(%s)' % (what, rng), ok, '고른 하네스 %d/%d %s · 첫 줄 「%s」 · %.0f초' % (
            len(names), len(rows), ('= ' + ' · '.join(names)) if len(names) <= 4 else '', first[:300], sec), who)


# ── E3 덩어리 · 죽임 · 이어 돎 · 예산 ─────────────────────────────────────────────────────────
def kill_group(p):
    if os.name == 'nt':
        subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True)
    else:
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        except OSError:
            pass
    try:
        p.wait(timeout=30)
    except Exception:
        pass


def e3(qcp, who):
    g = 'e3_' + who
    cen = census(os.path.join(SB, g + '_census.json'), NAMES, 900.0)   # 10 × 15 분 = 어림 150 분
    env = env_for(g, cen)
    C1 = REVS[0]
    sp = os.path.join(SB, g, 'res', 'chem', '_run_state.json')
    e = clean_env()
    e.update(env)
    e.update({'FK_SB': SB, 'FK_TAG': g + 'a', 'FK_SLEEP': '1.0'})
    kw = {'creationflags': 0x00000200} if os.name == 'nt' else {'start_new_session': True}
    p = subprocess.Popen([sys.executable, qcp, 'run', 'chem', '--rev', C1], env=e, cwd=SB, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kw)
    t0 = time.time()
    while time.time() - t0 < 300 and p.poll() is None and len(ran(g + 'a')) < 3:   # 셋째 하네스가 떴다 = 둘 끝남(첫 덩어리 한가운데)
        time.sleep(0.1)
    kill_group(p)
    st = jl(sp) or {}
    done_a = ran(g + 'a')
    fin = sorted((st.get('finished') or {}))
    T('E3-1', '가짜 사슬 어림 150 분 → 덩어리 둘(≤ 80 분) · _run_state.json', bool(st) and st.get('chunked') and len(st.get('chunks') or []) == 2 and
      all(float(ch.get('est_sec') or 0) <= 80 * 60 for ch in st.get('chunks') or []) and abs(float(st.get('est_total_sec') or 0) - 9000) < 1,
      '상태 %s · 어림 %.0f 분 · 덩어리 %s' % ('있음' if st else '없음', float(st.get('est_total_sec') or 0) / 60,
                                    [(ch.get('i'), len(ch.get('rows') or []), round(float(ch.get('est_sec') or 0) / 60)) for ch in st.get('chunks') or []]), who)
    rc, out, sec = qc(qcp, ['run', 'chem', '--rev', C1], env, g + 'b', extra={'FK_SLEEP': '0.3'})
    done_b = ran(g + 'b')
    left = [n for n in NAMES if n not in fin]
    ok = bool(fin) and len(fin) >= 2 and sorted(done_b) == sorted(left) and not (set(done_b) & set(fin)) and rc == 0 and '이어 돎' in out
    T('E3-2', '첫 덩어리 중간에 죽임 → 같은 명령 다시 = 끝난 하네스 건너고 남은 것만', ok,
      '죽이기 전 끝남 %d(%s) · 죽일 때 뜬 것 %d · 다시 부름에서 돈 것 %d(%s) · 겹침 %d · rc %s · 「이어 돎」 %s' % (
          len(fin), ','.join(fin), len(done_a), len(done_b), ','.join(done_b), len(set(done_b) & set(fin)), rc, '있음' if '이어 돎' in out else '없음')
      + ('' if ok else ' · 끝 줄 「%s」' % ' / '.join(out.strip().splitlines()[-3:])[:400]), who)
    st2 = jl(sp) or {}
    T('E3-3', '이어 돈 뒤 상태 = 끝(done) · 끝난 하네스 10 · 남은 것 0', st2.get('done') is True and len(st2.get('finished') or {}) == 10 and not st2.get('remaining'),
      'done=%r · 끝난 %d · 남은 %s · 부름 %s 번' % (st2.get('done'), len(st2.get('finished') or {}), st2.get('remaining'), (st2.get('resumed') or 0) + 1 if st2 else '-'), who)
    # 예산 — 덩어리 하나(75 분 어림 · 첫 덩어리는 늘 돎)를 돈 뒤 지난 시간 + 다음 덩어리 어림이 예산(60 분)을 넘기면 멈춤 · 종료 코드 4 → 다시 부르면 나머지
    g2 = 'e3b_' + who
    cen2 = census(os.path.join(SB, g2 + '_census.json'), NAMES, 900.0)
    env2 = env_for(g2, cen2)
    rc1, out1, _ = qc(qcp, ['run', 'chem', '--rev', C1, '--budget', '60'], env2, g2 + 'a')
    n1 = ran(g2 + 'a')
    rc2, out2, _ = qc(qcp, ['run', 'chem', '--rev', C1, '--budget', '60'], env2, g2 + 'b')
    n2 = ran(g2 + 'b')
    T('E3-4', '시간 예산(--budget 60) → 덩어리 하나(어림 75 분) 뒤 멈춤(종료 코드 4 · 「같은 명령을 다시」) → 다시 부르면 나머지만', rc1 == 4 and len(n1) == 5 and '같은 명령을 다시' in out1 and
      rc2 == 0 and sorted(n1 + n2) == sorted(NAMES), '첫 부름 rc %s · 돈 %d · 둘째 rc %s · 돈 %d(%s)' % (rc1, len(n1), rc2, len(n2), ','.join(n2)), who)


# ── E4 끝 어림 · 밀림 줄 · 「회귀」 칸 ──────────────────────────────────────────────────────────
def e4(qcp, who):
    g = 'e4_' + who
    names6 = NAMES[:6]
    cen = census(os.path.join(SB, g + '_census.json'), names6, 60.0)   # 6 × 1 분 = 어림 6 분
    env = env_for(g, cen)
    os.makedirs(os.path.join(SB, g), exist_ok=True)
    nowmd = os.path.join(SB, g, '_code_now.md')
    with open(nowmd, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 지금 Code 가 하는 일(모래상자)\n- 회귀: (비어 있음)\n- 다른 칸: 그대로\n')
    eta = os.path.join(SB, g, 'res', 'chem', '_eta.txt')
    sp = os.path.join(SB, g, 'res', 'chem', '_run_state.json')
    if os.path.exists(os.path.join(SB, 'eta.log')):
        os.remove(os.path.join(SB, 'eta.log'))
    rc, out, sec = qc(qcp, ['run', 'chem', '--rev', REVS[0]], env, g, extra={'FK_ETA': eta, 'FK_INFLATE': sp, 'FK_INFLATE_AT': 'fk_03', 'FK_INFLATE_SEC': '900'})
    log = [ln.rstrip('\n').split('\t', 1) for ln in open(os.path.join(SB, 'eta.log'), encoding='utf-8')] if os.path.exists(os.path.join(SB, 'eta.log')) else []
    rem = [int(m.group(1)) if m else -1 for m in (re.search(r'남은 하네스 (\d+)/6', t) for _, t in log)]
    T('E4-1', '_eta.txt 가 하네스마다 바뀜 — 시작 때 첫 어림 · 남은 하네스 6→1 · 「÷ 무리」 · 끝 어림 시각', len(log) == 6 and rem == [6, 5, 4, 3, 2, 1] and
      len(set(t for _, t in log)) == 6 and all('÷ 무리 1' in t and '끝 어림' in t for _, t in log),
      '하네스가 본 어림 %d 줄 · 남은 수 %s · 첫 줄 「%s」' % (len(log), rem, (log[0][1] if log else '')[:220]), who)
    slip = [(n, t) for n, t in log if t.startswith('★ 밀림 +')]
    s4 = dict(log).get('fk_04', '')
    m = re.match(r'★ 밀림 \+(\d+) 분 · 까닭\(([^)]*)\)', s4)
    ok = bool(m) and int(m.group(1)) > 30 and all(x in m.group(2) for x in ('fk_04 +15 분', 'fk_05 +15 분', 'fk_06 +15 분')) and not any(n in ('fk_01', 'fk_02', 'fk_03') for n, _ in slip)
    T('E4-2', '가짜 last_sec 늘림(fk_03 이 남은 셋 어림 +15 분씩) → 다음 어림 머리 「★ 밀림 +N 분 · 까닭(가장 늦은 하네스 셋)」', ok,
      '밀림 줄 %d(%s) · fk_04 가 본 줄 「%s」' % (len(slip), ','.join(n for n, _ in slip), s4[:260]), who)
    t = open(nowmd, encoding='utf-8').read()
    fin = open(eta, encoding='utf-8').read().strip() if os.path.exists(eta) else ''
    T('E4-3', '_code_now.md 「회귀」 칸 덮어씀(다른 칸 그대로) · _eta.txt 끝 줄', ('- 회귀: 회귀 chem run · 끝 ' in t) and '- 다른 칸: 그대로' in t and t.count('회귀:') == 1 and
      fin.startswith('회귀 chem run · 끝 ') and rc == 0, '회귀 칸 「%s」 · _eta.txt 「%s」 · rc %s' % (
          next((ln for ln in t.splitlines() if '회귀:' in ln), '(없음)')[:200], fin[:160], rc), who)


# ── 헛잣대 실행기(바탕) 꺼내기 ─────────────────────────────────────────────────────────────────
def base_runner():
    d = os.path.join(SB, 'base_qa', '_qa')
    os.makedirs(os.path.join(d, '_qa_trace'))
    for rel in ('_qa/_qa_chain.py', '_qa/_roots.py', '_qa/_qa_trace/sitecustomize.py'):
        r = subprocess.run(['git', '-C', GENIE, 'show', '%s:%s' % (BASE_REV, rel)], capture_output=True)
        if r.returncode:
            return None
        with open(os.path.join(SB, 'base_qa', *rel.split('/')), 'wb') as f:
            f.write(r.stdout)
    return os.path.join(d, '_qa_chain.py')


def run_all(qcp, who):
    for g, fn in (('E1', e1), ('E2', e2), ('E3', e3), ('E4', e4)):
        if want(g):
            t0 = time.time()
            try:
                fn(qcp, who)
            except Exception as ex:   # 한 묶음이 죽어도 다음 묶음은 돈다(그 묶음 = FAIL)
                T(g + '-x', '묶음 실행 중 예외', False, '%s: %s' % (type(ex).__name__, str(ex)[:300]), who)
            I('%s %s 묶음 %.0f초' % ('새 실행기' if who == 'new' else '바탕 실행기', g, time.time() - t0))


FG, REVS = fake_genie()
HH = fake_home()
I('모래상자 %s · 잴 실행기 %s · genie(E2) %s' % (SB, QC, GENIE))
t_all = time.time()
run_all(QC, 'new')
if '--yard' in sys.argv:
    bq = base_runner()
    if not bq:
        T('YARD', '바탕 실행기 꺼내기', False, 'genie %s 에서 _qa/_qa_chain.py 를 못 꺼냄' % BASE_REV)
    else:
        I('헛잣대 — 바탕 실행기 %s(genie %s)' % (bq, BASE_REV))
        run_all(bq, 'base')
        fails = {g: sum(1 for c, ok in xs if not ok and '잼' not in c) for g, xs in SUM.get('base', {}).items()}
        tots = {g: sum(1 for c, _ in xs if '잼' not in c) for g, xs in SUM.get('base', {}).items()}
        want_g = [g for g in ('E1', 'E2', 'E3', 'E4') if want(g)]
        T('YARD', '헛잣대 — 바탕 실행기(%s)로 %s 다 FAIL(묶음마다 FAIL 하나 넘게 · 잼 줄 빼고)' % (BASE_REV, '~'.join([want_g[0], want_g[-1]]) if want_g else '-'),
          all(fails.get(g, 0) >= 1 for g in want_g), ' · '.join('%s FAIL %d/%d' % (g, fails.get(g, 0), tots.get(g, 0)) for g in want_g))
n_pass = sum(1 for x in L if x.startswith('PASS'))
n_fail = sum(1 for x in L if x.startswith('FAIL'))
I('합 — PASS %d · FAIL %d · %.0f초' % (n_pass, n_fail, time.time() - t_all))
with open(OUTF, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(L) + '\n')
if '--keep' not in sys.argv:
    for wt in glob.glob(os.path.join(FG, '.claude', 'worktrees', '*')):
        git(FG, 'worktree', 'remove', '--force', wt)
    shutil.rmtree(SB, ignore_errors=True)
sys.exit(1 if n_fail else 0)
