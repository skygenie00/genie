# -*- coding: utf-8 -*-
r"""⚙ jo_pipe_push 관문 하네스 — 지시서 `_task_jo_pipe_push.md` §B 1~10 + `_add1.md` §B 1~3 (2026-10-04) + 조이기 Y1~Y7(채팅 판정 ① ② ④ · 10/4 22:4x)

  python _harness_jo_pipe_push.py --pipe <jo_pipe.py 자리>  [--expect new|base] [--only B1,B3,…] [--work 폴더] [--keep]
                                  [--src jopangi 폴더] [--wheelhouse 폴더] [--base-pipe 정본 jo_pipe.py] [--json 결과.json] [--bait new|old] [--no-venv]

같은 시험을 `--pipe` 로 받은 jo_pipe.py 에 돌린다.
  --expect new  새 판(사본) — 모든 칸이 PASS 여야 한다(기본)
  --expect base 바탕(= 정본 그대로) — 헛잣대: 헛잣대 칸이 FAIL 로 서면 「헛잣대가 섰다」(종료 0) · 아니면 1
    --bait new(기본)  헛잣대 칸 = 조이기 판 Y1~Y7 — 바탕 = 조이기 전 정본(d0f4c1d4). 옛 칸(B · X · R)은 바탕에서도 전처럼 PASS 여야 한다(참고로 센다)
    --bait old        헛잣대 칸 = 옛 B3 · B4 · B5(B-10) — 바탕 = push 판 전(29ae7c57)
■ 조이기 Y 칸(10/4 22:4x [채팅] 판정): Y1 ① 앱 파일 안 실음(고치다 만 jo/index.html · 새 파일 · jo/data 안 지워진 파일은 같이) · Y2 ② _meta.json 하나뿐이면 올릴 것 없음 · Y3 ① 앱 파일이 섞인 jo: data 커밋은 안 버림 ·
  Y4 ① 멈춘 rebase 를 풀 때 앱 파일 고치다 만 것이 있으면 [NG] · Y5 ④ minbeoppdf 클론이 멈춘 상태(rebase · merge · 분리 HEAD)면 hsul 만 WARN · Y6 ④ 원격 먼저 받기(pull --rebase 0) · Y7 ④ 앞 실행이 못 올린 hsul 커밋을 같이 올림.
  Y5~Y7 은 샌드박스에 minbeoppdf 클론 + 가짜 hsul_build 를 더한다(SB.with_mbp) — 진짜 minbeoppdf 는 안 닿는다.

■ 어디서도 진짜를 안 건드린다
  · 모든 시험은 `--work`(기본 %TEMP%\jopipe_h) 아래 **샌드박스**에서만 돈다 — 샌드박스마다 가짜 USERPROFILE(= `_roots.DEFAULT['GENIE_ROOT']` 의 홈 기준 자리가 그 안 = 「본 클론」)·
    LOCALAPPDATA · APPDATA · 임시 폴더 · 볼트(빈 폴더 꼴) · 로컬 bare 원격(origin.git) · 「다른 PC」 클론(other).
    ⚙(jo_pipe.py)는 샌드박스 안 사본 폴더(jopangi\)에서 돈다 → HERE 가 거기라 `공통\_pipeline\`(_last_run.md · _runs\ · 기준선)도 샌드박스 안이다.
  · GitHub 로는 못 나간다 — 모든 하위 프로세스에 GIT_ALLOW_PROTOCOL=file · GIT_CONFIG_NOSYSTEM=1 · 가짜 HOME(전역 설정 없음) · 돌리기 전에 `git remote -v` 가
    샌드박스 안 로컬 경로인지 확인한다. 해설 짝(minbeoppdf)은 샌드박스에 클론이 없어 「클론 없음 — 건너뜀」.
  · 이 PC 의 진짜 본 genie 클론(`_roots.DEFAULT['GENIE_ROOT']`)에는 git 명령을 안 쓴다 — G() 가 샌드박스 밖을 assert 로 막고 .git/HEAD 한 줄만 읽어 보여 준다.
  · N: 정본(jo_pipe.py · python_setup.cmd) · N: 상태 파일(`공통\_pipeline\`)도 시험 앞뒤 md5 · 목록으로 대조한다.
  · pip 시험은 임시 venv 안에서만(PIP_REQUIRE_VIRTUALENV=1 + JO_PIPE_PIP_ARGS="" — venv 는 --user 를 거부한다) · 전역 파이썬 pip list 전후 대조.
    기본 형태(--user) 시험은 가짜 APPDATA · PYTHONUSERBASE(샌드박스) + PIP_NO_INDEX + 가짜 바퀴(없는 이름) 로만 — 진짜 사용자 자리에는 닿을 길이 없다.

■ 컴파일(jo_build.py)은 가짜(stub)다 — 진짜는 40~60 초 · N: 재료 · 볼트에 닿는다. ⚙ 의 A-1~A-6 은 컴파일 바깥(git · 판정 · 기록)이라 같은 인터페이스(_out\data\*.json ·
  _meta.json · _검산_*.csv)만 만든다. 「볼트 바뀜」 = 가짜 컴파일의 seed 가 바뀜. (진짜 컴파일은 본 세션이 꼬까 본 클론 --dry-run 으로 본다 · R1 은 이 PC 의 진짜 `_out` 을 읽기만 해 그대로 재생한다.)
■ L 묶음(add1 · 라이브러리)은 임시 venv 를 만들어 PyPI 에서 pymupdf · numpy · pdfplumber 를 받는다(인터넷 필요 · 몇 분) — `--no-venv` 로 빼거나 `--wheelhouse 폴더`(pip download 로 받아 둔 바퀴 · 오프라인)로 돌린다.
"""
import os as _os_r, sys as _sys_r   # env_lanes — _roots.py 를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import argparse, ast, hashlib, json, os, re, shutil, stat, subprocess, sys, tempfile, time, zipfile

sys.stdout.reconfigure(encoding='utf-8')
_roots.need_n('jo_pipe_push 하네스 — N: jopangi 의 jo_common · stage_jo · structure 와 P7PDF 가 필요')

TAGS = ('[OK]', '[NG]', '[줄]')
GEN_BASE = 'jo: data '


# ───────────────────────────────────────── 작은 도구
def rm_rf(p):
    def _onerr(f, path, _exc):
        try:
            os.chmod(path, stat.S_IWRITE)
            f(path)
        except OSError:
            pass
    if os.path.isdir(p):
        shutil.rmtree(p, onerror=_onerr)


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest() if os.path.isfile(p) else None


def fwd(p):
    return p.replace('\\', '/')


def wr(p, text, nl='\n'):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'wb') as f:
        f.write(text.replace('\r\n', '\n').replace('\n', nl).encode('utf-8'))


def load_consts(pipe_path):
    """jo_pipe.py 가 exist_gate 에서 보는 상수를 **그 파일에서** 읽는다(ast) — 시험 대상이 바뀌어도 샌드박스가 따라간다"""
    tree = ast.parse(open(pipe_path, 'rb').read().decode('utf-8'))
    want = {'WHITELIST', 'MATERIAL_FILES', 'MATERIAL_DIRS', 'VAULT_DIRS', 'P7PDF', 'BLANKPDFS'}
    out = {}
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in want:
            out[n.targets[0].id] = eval(compile(ast.Expression(n.value), '<const>', 'eval'), {'os': os}, {})
    return out


def vault_need(jo_common_path):
    tree = ast.parse(open(jo_common_path, 'rb').read().decode('utf-8'))
    for n in tree.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'VAULT_NEED':
            return ast.literal_eval(n.value)
    raise SystemExit('jo_common.VAULT_NEED 를 못 찾았다')


# ───────────────────────────────────────── 가짜 컴파일(jo_build.py 자리)
STUB = r'''# -*- coding: utf-8 -*-
# 시험용 가짜 jo_build — 진짜 컴파일 대신 같은 인터페이스(_out\data\*.json · _meta.json · _검산_*.csv)만 만든다.
import os, sys, json, shutil, subprocess, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ['JOPANGI_OUT']
DATA = os.path.join(OUT, 'data')
shutil.rmtree(OUT, ignore_errors=True)          # 진짜는 _out 을 통째로 비우고 다시 만든다
replay = os.environ.get('JO_STUB_REPLAY')       # 진짜 컴파일 산출물을 그대로 다시 놓는다(읽기만 · 같은 산출 재사용)
if replay:
    shutil.copytree(replay, OUT)
else:
    os.makedirs(DATA)
seed = os.environ.get('JO_STUB_SEED', 'A')
clone = os.environ.get('JO_STUB_CLONE', '')
head = ''
if clone:
    head = subprocess.run(['git', '-C', clone, 'rev-parse', '--short=7', 'HEAD'], capture_output=True, text=True).stdout.strip()
cnt = os.environ.get('JO_STUB_COUNT')
if cnt:
    open(cnt, 'a').write('x\n')
print('[stub] 컴파일 seed=%s' % seed)
print('[stub] 컴파일 때 클론 HEAD = %s' % head)
for i in range(1, 6):
    print('[stub] 단계 %d/5 …' % i)
for m in [x for x in os.environ.get('JO_STUB_IMPORT', '').split(',') if x.strip()]:
    try:
        __import__(m.strip())
        print('[stub] import %s OK' % m.strip())
    except Exception as e:
        print('[stub] import %s 실패: %s' % (m.strip(), e))
if replay:
    print('[stub] 진짜 산출물 재생: %s' % replay)
    sys.exit(0)
json.dump({'seed': seed, 'rows': [1, 2, 3]}, open(os.path.join(DATA, 'stub_a.json'), 'w', encoding='utf-8'), ensure_ascii=False)
json.dump({'fixed': 1}, open(os.path.join(DATA, 'stub_b.json'), 'w', encoding='utf-8'), ensure_ascii=False)
open(os.path.join(OUT, '_검산_마크업실패.csv'), 'w', encoding='utf-8').write('x,y\n1,2\n')
rows = [{'판정': 'OK', '코드': 'A', '이름': '조 수', '실측': '1273', '기준': '1273', '비고': ''},
        {'판정': 'WARN', '코드': 'L2', '이름': '조문 장·★ 개정(가짜)', '실측': '장15', '기준': '장 밖 조 0', '비고': '명칭개정 후보'}]
if os.environ.get('JO_STUB_NC'):
    def probe():
        cv = os.environ.get('JO_STUB_CANVAS')
        if cv and os.path.isdir(cv):                  # 진짜 canvas_match(읽기만) — 모듈 머리에서 numpy · 쪽 글자(_pages_words)에서 pdfplumber 를 부른다
            sys.path.insert(0, cv)
            import canvas_match as CM
            pages = CM._pages_words((os.path.join(HERE, '_sample.pdf'), 0, 1))
            return len(pages[0]['words'])
        import numpy                                  # (진짜 폴더가 없을 때만) 같은 길을 흉내
        import pdfplumber
        with pdfplumber.open(os.path.join(HERE, '_sample.pdf')) as pdf:
            return len(pdf.pages[0].extract_words())
    for code, name in (('NC1', '노트↔캔버스 짝(민소 · book_stamp C-1)'), ('NCO', '노트 정리 색(민소 · notecolor A-2)')):
        try:
            n = probe()
            rows.append({'판정': 'INFO', '코드': code, '이름': name, '실측': '단어 %d' % n, '기준': '—', '비고': ''})
        except Exception as e:
            rows.append({'판정': 'WARN', '코드': code, '이름': name, '실측': '실패 — %s' % str(e)[:160], '기준': '—',
                         '비고': '클론의 옛 파일이 남는다'})
meta = {'생성': ('2026-10-04T00:00:00' if not os.environ.get('JO_STUB_META_NOW') else datetime.datetime.now().isoformat(timespec='seconds')),
        '검산': rows, '판정': 'OK', 'NG': []}
if os.environ.get('JO_STUB_NG'):
    meta['판정'] = 'NG'
    meta['NG'] = ['A 조 수 — 1272 (기준 1273)']
json.dump(meta, open(os.path.join(DATA, '_meta.json'), 'w', encoding='utf-8'), ensure_ascii=False)
sys.exit(0)
'''

HOOK_RACE = '''#!/bin/sh
# 시험용 pre-push — push 직전에 「다른 PC」 가 먼저 올린 것처럼 한다(최대 MAX 번)
CNT="%(cnt)s"
MAX=%(max)d
n=$(cat "$CNT" 2>/dev/null || echo 0)
if [ "$n" -lt "$MAX" ]; then
  echo $((n+1)) > "$CNT"
  unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_PREFIX
  cd "%(other)s" || exit 0
  git pull -q --ff-only origin main || exit 0
  echo "{\\"race\\":$n}" > jo/data/other_pc_race$n.json
  git add jo/data/other_pc_race$n.json
  git commit -q -m "jo: data race $n"
  git push -q origin main
fi
exit 0
'''

HOOK_REJECT = '''#!/bin/sh
# 시험용 pre-push — 늘 거절(인터넷이 막힌 것처럼 거절 이유가 「거절」 이 아니다)
echo "pre-push: 시험용 거절" >&2
exit 1
'''

# ── ★ 조이기(2026-10-04 22:4x [채팅] 판정 ① ② ④) — 가짜 해설 짝 만들기 · 헛잣대 칸 이름
HSUL_STUB = r'''# -*- coding: utf-8 -*-
# 시험용 가짜 hsul_build — 진짜 해설 짝 만들기(PDF 쪽 대조) 대신 같은 인터페이스(법 --data D --out OUT --report R)만 흉내: OUT\<법>.json 을 쓴다.
# 부른 횟수 · 그때 minbeoppdf HEAD 를 JO_STUB_HSUL_COUNT 파일에 한 줄씩 남긴다(「만들기 전에 원격을 받았나」 를 재려고).
import os, sys, json, subprocess
law = sys.argv[1]
out = sys.argv[sys.argv.index('--out') + 1]
os.makedirs(out, exist_ok=True)
seed = os.environ.get('JO_STUB_HSUL_SEED') or os.environ.get('JO_STUB_SEED', 'A')
json.dump({'law': law, 'seed': seed}, open(os.path.join(out, law + '.json'), 'w', encoding='utf-8'), ensure_ascii=False)
head = subprocess.run(['git', '-C', os.path.dirname(out), 'rev-parse', '--short=7', 'HEAD'], capture_output=True, text=True).stdout.strip()
cnt = os.environ.get('JO_STUB_HSUL_COUNT')
if cnt:
    open(cnt, 'a', encoding='utf-8').write('%s %s\n' % (law, head))
print('[stub-hsul] %s seed=%s head=%s' % (law, seed, head))
'''

NEW_BAIT = ('Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7')   # 조이기 판 칸 — 바탕(= 조이기 전 정본 d0f4c1d4)에서는 FAIL 로 서야 한다(헛잣대)
OLD_BAIT = ('B3', 'B4', 'B5')                            # 옛 헛잣대(B-10) — 바탕이 push 판 전(29ae7c57)일 때만 FAIL 로 선다

SEQED = '''import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read().replace("pick ", "edit ", 1)
open(p, "w", encoding="utf-8", newline="\\n").write(s)
'''


# ───────────────────────────────────────── 샌드박스
class Res:
    def __init__(self, rc, out, err, secs):
        self.rc, self.out, self.err, self.secs = rc, out, err, secs
        self.lines = out.splitlines()

    def tag(self):
        if len(self.lines) == 4 and self.lines[0] in TAGS:
            return self.lines[0]
        for ln in reversed(self.lines):
            m = re.match(r'^\[(OK|NG|줄)\]', ln)
            if m:
                return m.group(0)
        return ''

    def four(self):
        return len(self.lines) == 4 and self.lines[0] in TAGS


class SB:
    """샌드박스 하나 = 가짜 홈 + 로컬 bare 원격 + 본 클론(홈 안 _roots.DEFAULT 자리) + 「다른 PC」 클론 + ⚙ 폴더(jopangi 사본)"""

    def __init__(self, ctx, name):
        self.ctx, self.name = ctx, name
        self.root = os.path.join(ctx.work, name)
        self.home = os.path.join(self.root, 'home')
        self.genie = os.path.join(self.home, os.path.relpath(_roots.DEFAULT['GENIE_ROOT'], os.path.expanduser('~')))   # 가짜 홈 기준으로 같은 상대 자리 = _roots.DEFAULT['GENIE_ROOT'] → 「본 클론」
        self.origin = os.path.join(self.root, 'origin.git')
        self.other = os.path.join(self.root, 'other')
        self.here = os.path.join(self.root, 'jopangi')
        self.out = os.path.join(self.root, 'out')
        self.local = os.path.join(self.home, 'AppData', 'Local')
        self.roam = os.path.join(self.home, 'AppData', 'Roaming')
        self.tmp = os.path.join(self.root, 'tmp')
        self.vault = os.path.join(self.home, 'Documents', "PA's archive")
        self.pipe_state = os.path.join(self.here, '공통', '_pipeline')
        self.count = os.path.join(self.root, 'compile_count.txt')
        self.hsul_count = os.path.join(self.root, 'hsul_count.txt')   # ★ 조이기 ④ — 가짜 hsul_build 가 한 줄씩(법 · 그때 minbeoppdf HEAD)
        self.py = ctx.py
        self.build()

    # ── env
    def env(self, extra=None):
        e = {k: v for k, v in os.environ.items()
             if not (k.startswith('GIT_') or k.startswith('JO_') or k.startswith('JOPANGI_') or k.startswith('PIP_')
                     or k in ('GENIE_ROOT', 'SPD_ROOT', 'MBPDF_ROOT', 'N_ROOT', 'PYTHONUSERBASE', 'VIRTUAL_ENV'))}
        e.update({'USERPROFILE': self.home, 'HOME': self.home, 'LOCALAPPDATA': self.local, 'APPDATA': self.roam,
                  'TEMP': self.tmp, 'TMP': self.tmp, 'COMPUTERNAME': 'TESTPC',
                  'JOPANGI_OUT': self.out, 'JOPANGI_VAULT': self.vault,
                  'GIT_ALLOW_PROTOCOL': 'file', 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_TERMINAL_PROMPT': '0',
                  'GIT_AUTHOR_NAME': 'jo test', 'GIT_AUTHOR_EMAIL': ('jo' + chr(64) + 'test.invalid'),
                  'GIT_COMMITTER_NAME': 'jo test', 'GIT_COMMITTER_EMAIL': ('jo' + chr(64) + 'test.invalid'),
                  'PYTHONIOENCODING': 'utf-8', 'PYTHONDONTWRITEBYTECODE': '1',
                  'JO_STUB_SEED': 'A', 'JO_STUB_CLONE': self.genie, 'JO_STUB_COUNT': self.count, 'JO_STUB_HSUL_COUNT': self.hsul_count,
                  'JO_STUB_CANVAS': os.path.join(self.ctx.src, '민소', 'canvas')})
        if extra:
            e.update(extra)
        return e

    # ── git
    def G(self, repo, *args, check=True, env=None, input=None):
        assert os.path.normcase(os.path.abspath(repo)).startswith(os.path.normcase(os.path.abspath(self.ctx.work))), '샌드박스 밖 git 금지: ' + repo
        r = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, text=True, encoding='utf-8', errors='replace',
                           env=env or self.env(), input=input)
        if check and r.returncode != 0:
            raise RuntimeError('git %s → %d\n%s' % (' '.join(args), r.returncode, (r.stderr or r.stdout).strip()))
        return r

    def gout(self, repo, *args):
        return self.G(repo, *args).stdout.strip()

    def build(self):
        rm_rf(self.root)
        os.makedirs(self.tmp)
        os.makedirs(self.local)
        os.makedirs(self.roam)
        self.G(self.root, 'init', '-q', '--bare', '-b', 'main', self.origin)
        self.G(self.root, 'clone', '-q', self.origin, self.genie, check=False)
        self.cfg(self.genie)
        wr(os.path.join(self.genie, '.gitattributes'), 'jo/data/*.json -text\n')
        wr(os.path.join(self.genie, 'jo', 'index.html'), '<html>jo app v1</html>\n')
        wr(os.path.join(self.genie, 'jo', 'data', 'seed.json'), '{"seed": 0}')
        wr(os.path.join(self.genie, 'jagwa', 'index.html'), '<html>jagwa v1</html>\n')
        wr(os.path.join(self.genie, 'README.md'), 'sandbox\n')
        self.G(self.genie, 'add', '.')
        self.G(self.genie, 'commit', '-q', '-m', 'seed')
        self.G(self.genie, 'push', '-q', '-u', 'origin', 'main')
        self.S0 = self.gout(self.genie, 'rev-parse', 'HEAD')
        self.G(self.root, 'clone', '-q', self.origin, self.other)
        self.cfg(self.other)
        self.populate_here()
        self.check_remote()

    def cfg(self, repo):
        for k, v in (('user.name', 'jo test'), ('user.email', ('jo' + chr(64) + 'test.invalid')), ('core.autocrlf', 'false'),
                     ('core.safecrlf', 'false'), ('gc.auto', '0'), ('commit.gpgsign', 'false'), ('core.quotepath', 'false')):
            self.G(repo, 'config', k, v)

    def check_remote(self):
        """돌리기 전에 임시 클론의 git remote -v 가 샌드박스 안 로컬 bare 인지 확인한다"""
        for repo in (self.genie, self.other):
            out = self.gout(repo, 'remote', '-v')
            urls = {ln.split()[1] for ln in out.splitlines() if ln.strip()}
            assert urls and all(os.path.normcase(os.path.abspath(u)).startswith(os.path.normcase(os.path.abspath(self.ctx.work))) for u in urls), \
                '원격이 샌드박스 안 로컬 경로가 아니다: %r' % out
        self.remote_v = self.gout(self.genie, 'remote', '-v').splitlines()[0]

    def populate_here(self):
        c, s = self.ctx.consts, self.ctx.src
        os.makedirs(self.here)
        shutil.copyfile(self.ctx.pipe, os.path.join(self.here, 'jo_pipe.py'))
        for f in ('jo_common.py', 'stage_jo.py', 'structure.py'):
            shutil.copyfile(os.path.join(s, f), os.path.join(self.here, f))
        shutil.copyfile(self.ctx.roots_py, os.path.join(self.here, '_roots.py'))
        wr(os.path.join(self.here, 'jo_build.py'), STUB)
        real = {'jo_build.py', 'jo_common.py', 'stage_jo.py', 'structure.py'}
        for f in c['WHITELIST']:
            if f not in real:
                wr(os.path.join(self.here, f), '# 시험용 빈 칸 — exist_gate 가 있는지만 본다\n')
        for f in c['MATERIAL_FILES']:
            wr(os.path.join(self.here, '특상디', f), '{}')
        for d in c['MATERIAL_DIRS']:
            os.makedirs(os.path.join(self.here, d), exist_ok=True)
        base = os.path.join(self.vault, '변리사 시험')
        for d in self.ctx.need + c['VAULT_DIRS']:
            os.makedirs(os.path.join(base, d), exist_ok=True)
        wr(os.path.join(base, self.ctx.need[0], '시험.md'), '# 시험용 노트\n')
        if os.path.isfile(self.ctx.sample_pdf):
            shutil.copyfile(self.ctx.sample_pdf, os.path.join(self.here, '_sample.pdf'))

    # ── 실행
    def run(self, args=(), seed='A', env=None, py=None, timeout=900):
        e = self.env({'JO_STUB_SEED': seed})
        if env:
            e.update(env)
        t0 = time.time()
        p = subprocess.run([py or self.py, os.path.join(self.here, 'jo_pipe.py')] + list(args), cwd=self.here, env=e,
                           capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)
        return Res(p.returncode, p.stdout, p.stderr, time.time() - t0)

    # ── 상태 읽기
    def ohead(self):
        return self.gout(self.origin, 'rev-parse', 'refs/heads/main')

    def head(self, repo=None):
        return self.gout(repo or self.genie, 'rev-parse', 'HEAD')

    def branch(self, repo=None):
        return self.gout(repo or self.genie, 'branch', '--show-current')

    def parent(self, sha, repo=None):
        r = self.G(repo or self.origin, 'rev-parse', sha + '^', check=False)
        return r.stdout.strip() if r.returncode == 0 else ''

    def files_of(self, sha, repo=None):
        return [x for x in self.G(repo or self.origin, 'diff-tree', '--no-commit-id', '--name-only', '-r', '-z', sha).stdout.split('\0') if x]

    def tree_of(self, sha):
        return [x for x in self.G(self.origin, 'ls-tree', '-r', '--name-only', '-z', sha).stdout.split('\0') if x]

    def subject(self, sha, repo=None):
        return self.gout(repo or self.origin, 'log', '-1', '--format=%s', sha)

    def backups(self):
        return [x.strip() for x in self.G(self.genie, 'branch', '--list', 'jo_pipe_bak/*', '--format=%(refname:short)').stdout.splitlines() if x.strip()]

    def reflog(self, repo=None):
        return self.G(repo or self.genie, 'reflog', '--format=%gs', check=False).stdout

    def status(self):
        return self.G(self.genie, 'status', '--porcelain', '-uall').stdout

    def compiles(self):
        return len(open(self.count).read().split()) if os.path.exists(self.count) else 0

    def last_run(self):
        p = os.path.join(self.pipe_state, '_last_run.md')
        return open(p, encoding='utf-8').read() if os.path.exists(p) else ''

    def runs(self):
        d = os.path.join(self.pipe_state, '_runs')
        return sorted(os.listdir(d)) if os.path.isdir(d) else []

    # ── 장면 만들기
    def other_push(self, files, msg):
        self.G(self.other, 'pull', '-q', '--ff-only', 'origin', 'main')
        for rel, txt in files.items():
            wr(os.path.join(self.other, rel), txt)
        self.G(self.other, 'add', '--', *files)
        self.G(self.other, 'commit', '-q', '-m', msg)
        self.G(self.other, 'push', '-q', 'origin', 'main')
        return self.gout(self.other, 'rev-parse', 'HEAD')

    def local_commit(self, files, msg, repo=None):
        repo = repo or self.genie
        for rel, txt in files.items():
            wr(os.path.join(repo, rel), txt)
        self.G(repo, 'add', '--', *files)
        self.G(repo, 'commit', '-q', '-m', msg)
        return self.gout(repo, 'rev-parse', 'HEAD')

    def hook(self, text, repo=None):
        p = os.path.join(repo or self.genie, '.git', 'hooks', 'pre-push')
        wr(p, text)

    # ── ★ 조이기 ④ — 샌드박스 minbeoppdf(비공개 해설 짝 저장소 흉내): 로컬 bare 원격 + 본 클론(가짜 홈 안 _roots.DEFAULT['MBPDF_ROOT'] 자리) + 「다른 PC」 클론 + 가짜 hsul_build
    #    이 PC 의 진짜 minbeoppdf 에는 안 닿는다 — 모든 git 은 G() 가 샌드박스 안만 허용하고 원격은 샌드박스 안 로컬 경로임을 확인한다.
    def with_mbp(self):
        self.mbp = os.path.join(self.home, os.path.relpath(_roots.DEFAULT['MBPDF_ROOT'], os.path.expanduser('~')))
        self.mbp_origin = os.path.join(self.root, 'mbp_origin.git')
        self.mbp_other = os.path.join(self.root, 'mbp_other')
        self.G(self.root, 'init', '-q', '--bare', '-b', 'main', self.mbp_origin)
        self.G(self.root, 'clone', '-q', self.mbp_origin, self.mbp, check=False)
        self.cfg(self.mbp)
        wr(os.path.join(self.mbp, 'README.md'), 'sandbox minbeoppdf\n')
        wr(os.path.join(self.mbp, 'hsul', '민소.json'), '{"law": "민소", "seed": "0"}')
        wr(os.path.join(self.mbp, 'hsul', '특허.json'), '{"law": "특허", "seed": "0"}')
        self.G(self.mbp, 'add', '.')
        self.G(self.mbp, 'commit', '-q', '-m', 'seed')
        self.G(self.mbp, 'push', '-q', '-u', 'origin', 'main')
        self.M0 = self.gout(self.mbp, 'rev-parse', 'HEAD')
        self.G(self.root, 'clone', '-q', self.mbp_origin, self.mbp_other)
        self.cfg(self.mbp_other)
        for repo in (self.mbp, self.mbp_other):
            out = self.gout(repo, 'remote', '-v')
            urls = {ln.split()[1] for ln in out.splitlines() if ln.strip()}
            assert urls and all(os.path.normcase(os.path.abspath(u)).startswith(os.path.normcase(os.path.abspath(self.ctx.work))) for u in urls), \
                'minbeoppdf 원격이 샌드박스 안 로컬 경로가 아니다: %r' % out
        hd = os.path.join(self.here, '민소', 'hsul')
        wr(os.path.join(hd, 'hsul_build.py'), HSUL_STUB)
        wr(os.path.join(hd, 'hsul_설정.json'), '{"docs": {}}\n')

    def mbp_other_push(self, files, msg):
        self.G(self.mbp_other, 'pull', '-q', '--ff-only', 'origin', 'main')
        for rel, txt in files.items():
            wr(os.path.join(self.mbp_other, rel), txt)
        self.G(self.mbp_other, 'add', '--', *files)
        self.G(self.mbp_other, 'commit', '-q', '-m', msg)
        self.G(self.mbp_other, 'push', '-q', 'origin', 'main')
        return self.gout(self.mbp_other, 'rev-parse', 'HEAD')

    def mbp_local_commit(self, files, msg):
        return self.local_commit(files, msg, repo=self.mbp)

    def status_of(self, repo):
        return self.G(repo, 'status', '--porcelain', '-uall').stdout

    def hsul_builds(self):
        """가짜 hsul_build 가 남긴 줄(「법 그때의 minbeoppdf HEAD 7자」)"""
        return open(self.hsul_count, encoding='utf-8').read().split('\n')[:-1] if os.path.exists(self.hsul_count) else []

    def make_stuck_rebase(self, files=None, subject=None):
        """오늘 꼴(10/4 햄찌) — 안 올린 jo: data 커밋 하나 + 원격이 앞섬 → rebase -i 가 마지막 커밋에서 멈춤(남은 일 0 · 작업트리 깨끗 · 분리 HEAD)"""
        self.local_commit(files or {'jo/data/old_run.json': '{"o": 1}'}, subject or (GEN_BASE + '2026-10-04 19:39 (1 files)'))
        self.O = self.other_push({'jo/data/other_pc.json': '{"pc": "other"}'}, GEN_BASE + '2026-10-04 19:40 (1 files)')
        self.G(self.genie, 'fetch', '-q', 'origin')
        sq = os.path.join(self.root, 'seqed.py')
        wr(sq, SEQED)
        e = self.env({'GIT_SEQUENCE_EDITOR': '"%s" "%s"' % (fwd(self.py), fwd(sq)), 'GIT_EDITOR': 'true'})
        self.G(self.genie, 'rebase', '-i', 'origin/main', check=False, env=e)
        gd = os.path.join(self.genie, '.git')
        todo = os.path.join(gd, 'rebase-merge', 'git-rebase-todo')
        left = [x for x in open(todo, encoding='utf-8').read().splitlines() if x.strip() and not x.startswith('#')] if os.path.exists(todo) else ['?']
        assert os.path.isdir(os.path.join(gd, 'rebase-merge')) and not left and not self.branch() and not self.G(self.genie, 'status', '--porcelain', '-uno').stdout.strip(), \
            '멈춘 rebase 장면이 안 섰다: dir=%s left=%s branch=%r' % (os.path.isdir(os.path.join(gd, 'rebase-merge')), left, self.branch())


class Ctx:
    def __init__(self, a):
        self.a = a
        self.pipe = os.path.abspath(a.pipe)
        self.src = os.path.abspath(a.src) if a.src else (os.path.dirname(os.path.abspath(__file__)) if os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jo_common.py')) else _roots.n('jopangi'))
        self.roots_py = os.path.abspath(_roots.__file__)
        self.work = os.path.abspath(a.work) if a.work else os.path.join(tempfile.gettempdir(), 'jopipe_h')
        self.py = sys.executable
        self.consts = load_consts(self.pipe)
        self.need = vault_need(os.path.join(self.src, 'jo_common.py'))
        self.results = []        # (id, 이름, ok, [칸])
        self.sample_pdf = os.path.join(self.work, '_sample.pdf')
        os.makedirs(self.work, exist_ok=True)
        self.make_sample_pdf()

    def make_sample_pdf(self):
        if os.path.isfile(self.sample_pdf):
            return
        try:
            import pymupdf
            d = pymupdf.open()
            pg = d.new_page()
            pg.insert_text((72, 100), 'jopipe sample words for pdfplumber')
            d.save(self.sample_pdf)
        except Exception as e:                      # 없으면 NC 칸만 못 잰다
            print('(샘플 PDF 를 못 만듦: %s)' % e)

    def sb(self, name):
        return SB(self, name)


# ───────────────────────────────────────── 칸 기록
class Item:
    def __init__(self, iid, name):
        self.id, self.name, self.checks, self.vals = iid, name, [], {}

    def chk(self, grp, desc, ok, detail=''):
        self.checks.append((grp, desc, bool(ok), detail))
        return bool(ok)

    @property
    def ok(self):
        return all(c[2] for c in self.checks)

    @property
    def core_ok(self):
        return all(c[2] for c in self.checks if c[0] == 'core')


def four_ok(it, res, tag, line2=None, tag_only_first=True):
    """결과 넉 줄 꼴 — 정확히 넉 줄 · 첫 줄이 태그 · 셋째 줄 「할 일: 」 · 넷째 줄 WARN(또는 기록 안 함)"""
    L = res.lines
    it.chk('fmt', 'stdout 정확히 넉 줄', len(L) == 4, '%d 줄' % len(L))
    it.chk('fmt', '첫 줄 = %s' % tag, bool(L) and L[0] == tag, repr(L[0]) if L else '')
    if len(L) == 4:
        it.chk('fmt', '셋째 줄 「할 일: 」', L[2].startswith('할 일: '), L[2])
        it.chk('fmt', '넷째 줄 WARN 수 · 자세히', bool(re.match(r'^WARN \d+건 · 자세히 = jopangi\\공통\\_pipeline\\_last_run\.md', L[3])) or L[3].startswith('기록 안 함'), L[3])
        if line2 is not None:
            it.chk('fmt', '둘째 줄 꼴', bool(re.match(line2, L[1])), L[1])


# ───────────────────────────────────────── B 1~9 (jo_pipe 본판)
def sc_B1(ctx):
    it = Item('B1', '깨끗한 main · 볼트 바뀜 → push 됨 · 원격 HEAD = 새 커밋 · [OK]')
    sb = ctx.sb('b1')
    r = sb.run(seed='A')
    oh = sb.ohead()
    m = re.match(r'^올라감 · 커밋 ([0-9a-f]{7}) · 1분 뒤 앱 새로고침$', r.lines[1]) if len(r.lines) > 1 else None
    it.chk('core', 'rc 0 · 판정 [OK]', r.rc == 0 and r.tag() == '[OK]', 'rc=%d tag=%s' % (r.rc, r.tag()))
    it.chk('core', '원격 HEAD 가 새 커밋(S0 아님)', oh != sb.S0, 'origin=%s S0=%s' % (oh[:7], sb.S0[:7]))
    it.chk('core', '새 커밋의 부모 = S0(한 줄 이력)', sb.parent(oh) == sb.S0, 'parent=%s' % sb.parent(oh)[:7])
    it.chk('core', '로컬 HEAD = 원격 HEAD · 브랜치 main', sb.head() == oh and sb.branch() == 'main', 'local=%s br=%s' % (sb.head()[:7], sb.branch()))
    fs = sb.files_of(oh)
    it.chk('core', '올린 파일은 전부 jo/ · stub_a.json 포함 · 제목 jo: data', fs and all(f.startswith('jo/') or f == '.gitattributes' for f in fs)
           and 'jo/data/stub_a.json' in fs and sb.subject(oh).startswith(GEN_BASE), '%d개 · %s' % (len(fs), sb.subject(oh)))
    it.chk('core', 'rebase 0 (rebase-merge 없음 · reflog 에 rebase 없음)', not os.path.isdir(os.path.join(sb.genie, '.git', 'rebase-merge'))
           and 'rebase' not in sb.reflog(), '')
    md = sb.last_run()
    it.chk('core', '컴파일은 원격과 같은 HEAD 에서(S0)', ('컴파일 때 클론 HEAD = %s' % sb.S0[:7]) in md, '')
    four_ok(it, r, '[OK]', r'^올라감 · 커밋 [0-9a-f]{7} · 1분 뒤 앱 새로고침$')
    it.chk('fmt', '둘째 줄 커밋 7자 = 원격 HEAD', bool(m) and oh.startswith(m.group(1)), r.lines[1] if len(r.lines) > 1 else '')
    it.vals = {'origin_head': oh[:7], 'stdout': r.lines, 'secs': round(r.secs, 1), 'git remote -v': sb.remote_v}
    return it, r


def sc_B2(ctx):
    it = Item('B2', '원격이 앞섬(다른 클론이 jo/data 커밋 push) → ⚙ → 원격 위에 새 커밋 · push · [OK] · rebase 0')
    sb = ctx.sb('b2')
    O = sb.other_push({'jo/data/other_pc.json': '{"pc": "other"}'}, GEN_BASE + '2026-10-04 09:00 (1 files)')
    r = sb.run(seed='A')
    oh = sb.ohead()
    it.chk('core', 'rc 0 · 판정 [OK]', r.rc == 0 and r.tag() == '[OK]', 'rc=%d tag=%s' % (r.rc, r.tag()))
    it.chk('core', '원격 이력 S0 ← O ← 새 커밋(일직선)', sb.parent(oh) == O and sb.parent(O) == sb.S0, 'parent=%s O=%s' % (sb.parent(oh)[:7], O[:7]))
    tr = sb.tree_of(oh)
    it.chk('core', '새 커밋에 O 의 파일과 내 stub_a.json 이 같이 있다', 'jo/data/other_pc.json' in tr and 'jo/data/stub_a.json' in tr, '')
    it.chk('core', '로컬 = 원격', sb.head() == oh and sb.branch() == 'main', '')
    it.chk('core', 'rebase 0', 'rebase' not in sb.reflog() and not os.path.isdir(os.path.join(sb.genie, '.git', 'rebase-merge')), sb.reflog().splitlines()[0] if sb.reflog() else '')
    md = sb.last_run()
    it.chk('core', '원격을 만들기 전에 먼저 받았다(컴파일 때 클론 HEAD = O)', ('컴파일 때 클론 HEAD = %s' % O[:7]) in md, '')
    it.chk('core', '기록에 「원격을 먼저 받았다」', '원격을 먼저 받았다' in md, '')
    four_ok(it, r, '[OK]')
    it.vals = {'origin_head': oh[:7], 'O': O[:7]}
    return it, r


def sc_B3(ctx):
    it = Item('B3', '오늘 꼴 재현(멈춘 rebase · 남은 일 0 · 깨끗) → 스스로 continue → push · [OK]')
    sb = ctx.sb('b3')
    sb.make_stuck_rebase()
    before_o = sb.ohead()
    gd = os.path.join(sb.genie, '.git')
    r = sb.run(seed='A')
    oh = sb.ohead()
    md = sb.last_run()
    it.chk('core', '판정 [OK] · rc 0', r.rc == 0 and r.tag() == '[OK]', 'rc=%d tag=%s last=%r' % (r.rc, r.tag(), r.lines[-1] if r.lines else ''))
    it.chk('core', '멈춘 rebase 가 풀렸다(rebase-merge 없음) · 브랜치 main', not os.path.isdir(os.path.join(gd, 'rebase-merge')) and sb.branch() == 'main',
           'br=%r' % sb.branch())
    it.chk('core', '스스로 continue 했다(기록)', 'rebase --continue' in md, '')
    it.chk('core', 'push 됐다 — 원격 HEAD 가 앞섰다(O 위에 새 커밋)', oh != before_o and sb.parent(oh) == before_o, 'before=%s after=%s' % (before_o[:7], oh[:7]))
    it.chk('core', '로컬 = 원격', sb.head() == oh, '')
    four_ok(it, r, '[OK]')
    it.vals = {'before': before_o[:7], 'after': oh[:7], 'backups': sb.backups()}
    return it, r


def sc_B4(ctx):
    it = Item('B4', '분리 HEAD + jo/ 만 커밋 둘 → 백업 브랜치 생김 · reset · 다시 만들어 push · [OK]')
    sb = ctx.sb('b4')
    sb.G(sb.genie, 'checkout', '-q', '--detach')
    sb.local_commit({'jo/data/old1.json': '{"a": 1}'}, GEN_BASE + '2026-10-04 19:44 (1 files)')
    tip = sb.local_commit({'jo/data/old1.json': '{"a": 2}'}, GEN_BASE + '2026-10-04 19:51 (1 files)')
    before_o = sb.ohead()
    r = sb.run(seed='B')
    oh = sb.ohead()
    bak = sb.backups()
    it.chk('core', '판정 [OK] · rc 0', r.rc == 0 and r.tag() == '[OK]', 'rc=%d tag=%s last=%r' % (r.rc, r.tag(), r.lines[-1] if r.lines else ''))
    it.chk('core', '백업 브랜치 jo_pipe_bak/* 가 버린 꼭대기 커밋을 가리킨다', len(bak) == 1 and sb.gout(sb.genie, 'rev-parse', bak[0]) == tip, '%s' % bak)
    it.chk('core', 'push 됐다 — 원격 새 커밋의 부모 = 원래 원격(S0)', oh != before_o and sb.parent(oh) == before_o, 'before=%s after=%s' % (before_o[:7], oh[:7]))
    it.chk('core', '버린 커밋은 원격 이력에 없다 · 새 판 내용(seed B)', not sb.G(sb.origin, 'merge-base', '--is-ancestor', tip, oh, check=False).returncode == 0
           and '"seed": "B"' in sb.G(sb.origin, 'show', oh + ':jo/data/stub_a.json', check=False).stdout, '')
    it.chk('core', '본 클론이 main 으로 돌아와 원격과 같다', sb.branch() == 'main' and sb.head() == oh, 'br=%r' % sb.branch())
    four_ok(it, r, '[OK]')
    it.vals = {'tip': tip[:7], 'backup': bak, 'after': oh[:7]}
    return it, r


def sc_B5(ctx):
    it = Item('B5', '로컬 main 에 jo/ 밖 커밋(jagwa/index.html) 하나 → [NG] · 아무것도 안 버림 · push 0')
    sb = ctx.sb('b5')
    C = sb.local_commit({'jagwa/index.html': '<html>jagwa WIP</html>\n'}, 'jagwa: 아직 안 올린 작업')
    before_o = sb.ohead()
    r = sb.run(seed='A')
    it.chk('core', '판정 [NG] · rc 1', r.rc == 1 and r.tag() == '[NG]', 'rc=%d tag=%s last=%r' % (r.rc, r.tag(), r.lines[-1] if r.lines else ''))
    it.chk('core', 'push 0 — 원격 HEAD 그대로', sb.ohead() == before_o, 'before=%s after=%s' % (before_o[:7], sb.ohead()[:7]))
    it.chk('core', '아무것도 안 버렸다 — 로컬 HEAD 그대로 · 백업 브랜치 없음 · 작업트리 깨끗', sb.head() == C and not sb.backups() and sb.branch() == 'main'
           and not sb.status().strip(), 'head=%s backups=%s' % (sb.head()[:7], sb.backups()))
    it.chk('core', '만들기 전에 멈췄다(컴파일 0번)', sb.compiles() == 0, '컴파일 %d번' % sb.compiles())
    leaked = sb.G(sb.origin, 'log', '--name-only', '--format=', '%s..%s' % (sb.S0, sb.ohead())).stdout
    it.chk('core', 'jo/ 밖 커밋(jagwa/index.html)이 원격 이력에 안 나갔다(S0 뒤 전 구간)', 'jagwa/index.html' not in leaked, '새로 올라간 파일에 jagwa 있음' if 'jagwa/index.html' in leaked else '')
    it.chk('fmt', '둘째 줄에 걸린 커밋(7자 · 제목)이 보인다', len(r.lines) == 4 and C[:7] in r.lines[1] and 'jagwa: 아직 안 올린 작업' in r.lines[1], r.lines[1] if len(r.lines) > 1 else '')
    four_ok(it, r, '[NG]')
    it.vals = {'stdout': r.lines}
    return it, r


def sc_B6(ctx):
    it = Item('B6', 'push 거절(그 사이 원격 앞섬 흉내) → 한 번 다시 · [OK]')
    sb = ctx.sb('b6')
    cnt = os.path.join(sb.root, 'hook_count.txt')
    sb.hook(HOOK_RACE % {'cnt': fwd(cnt), 'max': 1, 'other': fwd(sb.other)})
    r = sb.run(seed='A')
    oh = sb.ohead()
    md = sb.last_run()
    race = sb.G(sb.origin, 'log', '--format=%H', '--grep=jo: data race 0', 'main').stdout.split()
    it.chk('core', '판정 [OK] · rc 0', r.rc == 0 and r.tag() == '[OK]', 'rc=%d tag=%s last=%r' % (r.rc, r.tag(), r.lines[-1] if r.lines else ''))
    it.chk('core', '한 번 거절돼 한 번 다시 했다(기록)', 'push 안 됨' in md and '한 번만 다시' in md, '')
    it.chk('core', '원격 이력 S0 ← 남의 커밋 ← 새 커밋(일직선)', len(race) == 1 and sb.parent(oh) == race[0] and sb.parent(race[0]) == sb.S0,
           'race=%s' % [x[:7] for x in race])
    tr = sb.tree_of(oh)
    it.chk('core', '새 커밋에 남의 파일과 내 stub_a.json 이 같이 있다', 'jo/data/other_pc_race0.json' in tr and 'jo/data/stub_a.json' in tr, '')
    it.chk('core', '로컬 = 원격 · push 는 두 번까지만(훅 1회 발동)', sb.head() == oh and open(cnt).read().strip() == '1', '')
    four_ok(it, r, '[OK]', r'^올라감 · 커밋 [0-9a-f]{7} · 1분 뒤 앱 새로고침$')
    it.vals = {'after': oh[:7]}
    return it, r


def sc_B7(ctx):
    it = Item('B7', '바뀐 것 없음 → [OK] 「올릴 것 없음」 · 커밋 0')
    sb = ctx.sb('b7')
    r1 = sb.run(seed='A')
    oh1, h1 = sb.ohead(), sb.head()
    n1 = len(sb.G(sb.genie, 'rev-list', 'HEAD').stdout.split())
    r2 = sb.run(seed='A')
    it.chk('core', '첫 실행 [OK](올라감)', r1.tag() == '[OK]' and oh1 != sb.S0, 'tag=%s' % r1.tag())
    it.chk('core', '둘째 실행 판정 [OK] · rc 0', r2.rc == 0 and r2.tag() == '[OK]', 'rc=%d tag=%s' % (r2.rc, r2.tag()))
    it.chk('core', '커밋 0 — 로컬·원격 HEAD 그대로 · 커밋 수 그대로', sb.ohead() == oh1 and sb.head() == h1
           and len(sb.G(sb.genie, 'rev-list', 'HEAD').stdout.split()) == n1, '')
    four_ok(it, r2, '[OK]', r'^올릴 것 없음\(볼트가 앱과 같음\)$')
    it.vals = {'line2': r2.lines[1] if len(r2.lines) > 1 else ''}
    return it, r2


def sc_B8(ctx):
    it = Item('B8', '워크트리(진짜 줄) → 지금처럼 commit 만 · 「줄 — push 는 합치는 세션이」 · [줄]')
    sb = ctx.sb('b8')
    wt = os.path.join(sb.root, 'wt', 'lane1')
    sb.G(sb.genie, 'worktree', 'add', '-q', '-b', 'worktree-lane1', wt)
    before_o, h0 = sb.ohead(), sb.head(wt)
    main_head = sb.head()
    r = sb.run(seed='A', env={'GENIE_ROOT': wt, 'JOPANGI_CLONE': wt, 'JO_STUB_CLONE': wt})
    it.chk('core', '판정 [줄] · rc 0 · [OK] 아님', r.rc == 0 and r.tag() == '[줄]' and r.tag() != '[OK]', 'rc=%d tag=%s' % (r.rc, r.tag()))
    h1 = sb.head(wt)
    it.chk('core', '워크트리 브랜치에 commit 하나 · 원격 HEAD 그대로(push 0) · 본 클론 무변', h1 != h0 and sb.parent(h1, wt) == h0 and sb.ohead() == before_o
           and sb.head() == main_head, 'wt %s→%s' % (h0[:7], h1[:7]))
    it.chk('core', '기준선(해시 이력 · ID · 입력 시각)을 안 건드렸다', not any(os.path.exists(os.path.join(sb.pipe_state, f)) for f in ('hashlog.json', 'ids_last.json', 'inputs_last.json')), '')
    it.chk('core', '_last_run.md 는 썼다 · 판정 줄 [줄]', '판정 = **[줄]**' in sb.last_run(), '')
    four_ok(it, r, '[줄]', r'^줄 — push 는 합치는 세션이 \(커밋 [0-9a-f]{7} 까지 했다\)$')
    it.vals = {'stdout': r.lines}
    return it, r


def md_block(text):
    m = re.search(r'```\n(.*?)\n```', text, re.S)
    return m.group(1).split('\n') if m else []


def norm(s):
    s = re.sub(r'b9[qv]', 'b9X', s)                       # 두 샌드박스 이름
    s = re.sub(r'\d{4}-\d\d-\d\d \d\d:\d\d(:\d\d)?', 'T', s)
    s = re.sub(r'\b[0-9a-f]{7,40}\b', 'H', s)
    s = re.sub(r'\d+초', 'N초', s)
    s = re.sub(r'\(\d+ ms\)', '(N ms)', s)
    return s


def sc_B9(ctx, results):
    it = Item('B9', '결과 넉 줄: 1 · 5 · 8 에서 stdout 정확히 넉 줄 · _last_run.md 에는 로그 전부가 그대로')
    for iid in ('B1', 'B5', 'B8'):
        rr = results.get(iid)
        ok = bool(rr) and len(rr.lines) == 4 and rr.lines[0] in TAGS
        it.chk('fmt', '%s stdout 정확히 넉 줄 · 첫 줄 태그' % iid, ok, '%s' % (('%d줄 %s' % (len(rr.lines), rr.lines[0] if rr.lines else '')) if rr else '없음'))
    q = ctx.sb('b9q'); rq = q.run(seed='A')
    v = ctx.sb('b9v'); rv = v.run(['--verbose'], seed='A')
    bq, bv = md_block(q.last_run()), md_block(v.last_run())
    it.chk('fmt', '조용한 판 stdout = 넉 줄', len(rq.lines) == 4, '%d줄' % len(rq.lines))
    it.chk('fmt', '--verbose 판 stdout = 로그 + 끝 넉 줄(요약 꼴은 조용한 판과 같다)', len(rv.lines) > 4 and norm('\n'.join(rv.lines[-4:])) == norm('\n'.join(rq.lines)),
           '%d줄' % len(rv.lines))
    it.chk('fmt', '--verbose 가 낸 로그 줄이 _last_run.md 로그에 전부 있다', all(x in bv for x in rv.lines[:-4]), '%d줄 대조' % len(rv.lines[:-4]))
    it.chk('fmt', '_last_run.md 로그는 --verbose 와 무관하게 같다(시각·커밋 빼고)', [norm(x) for x in bq] == [norm(x) for x in bv], '%d줄 · %d줄' % (len(bq), len(bv)))
    it.chk('fmt', '로그에 컴파일 출력(stub 줄)까지 들어 있다 — stdout 에는 안 나왔다', any('[stub] 단계 5/5' in x for x in bq) and not any('[stub]' in x for x in rq.lines),
           '%d줄' % len(bq))
    runs = q.runs()
    it.chk('fmt', '_runs\\<시각>_<PC>.md 가 _last_run.md 와 같은 내용', len(runs) == 1 and re.match(r'^\d{8}-\d{6}_TESTPC\.md$', runs[0]) is not None
           and open(os.path.join(q.pipe_state, '_runs', runs[0]), encoding='utf-8').read() == q.last_run(), '%s' % runs)
    it.vals = {'quiet_lines': len(rq.lines), 'verbose_lines': len(rv.lines), 'log_lines': len(bq)}
    return it, rq


# ───────────────────────────────────────── 더(본판 A-1~A-6 을 빠짐없이 재는 칸)
def sc_X1(ctx):
    it = Item('X1', '멈춘 rebase 가 남은 일이 있고 jo: data 뿐 → --abort 로 풀고 다시 만들어 push [OK]')
    sb = ctx.sb('x1')
    sb.local_commit({'jo/data/old_run.json': '{"o": 1}'}, GEN_BASE + '2026-10-04 19:39 (1 files)')
    sb.local_commit({'jo/data/old_run2.json': '{"o": 2}'}, GEN_BASE + '2026-10-04 19:41 (1 files)')
    sb.other_push({'jo/data/other_pc.json': '{"pc": "other"}'}, GEN_BASE + '2026-10-04 19:40 (1 files)')
    sb.G(sb.genie, 'fetch', '-q', 'origin')
    sq = os.path.join(sb.root, 'seqed.py'); wr(sq, SEQED)       # 첫 pick 을 edit 로 → 둘째 pick 이 남는다
    sb.G(sb.genie, 'rebase', '-i', 'origin/main', check=False, env=sb.env({'GIT_SEQUENCE_EDITOR': '"%s" "%s"' % (fwd(sb.py), fwd(sq)), 'GIT_EDITOR': 'true'}))
    gd = os.path.join(sb.genie, '.git')
    todo = [x for x in open(os.path.join(gd, 'rebase-merge', 'git-rebase-todo'), encoding='utf-8').read().splitlines() if x.strip() and not x.startswith('#')]
    it.chk('core', '장면: 멈춘 rebase 에 남은 일 1', os.path.isdir(os.path.join(gd, 'rebase-merge')) and len(todo) == 1, 'todo=%s' % todo)
    before_o = sb.ohead()
    r = sb.run(seed='A')
    oh = sb.ohead()
    it.chk('core', '판정 [OK]', r.rc == 0 and r.tag() == '[OK]', 'tag=%s last=%r' % (r.tag(), r.lines[-1] if r.lines else ''))
    it.chk('core', '--abort 로 풀었다 · rebase 상태 없음 · main', 'rebase --abort' in sb.last_run() and not os.path.isdir(os.path.join(gd, 'rebase-merge')) and sb.branch() == 'main', '')
    it.chk('core', '버린 jo: data 커밋은 백업 브랜치에 · push 됐다', len(sb.backups()) == 1 and oh != before_o and sb.parent(oh) == before_o, 'backups=%s' % sb.backups())
    return it, r


def sc_X2(ctx):
    it = Item('X2', '멈춘 rebase 에 jo/ 밖 커밋이 섞임 → 손대지 않고 [NG](rebase 상태 그대로 · push 0)')
    sb = ctx.sb('x2')
    sb.local_commit({'jagwa/index.html': '<html>jagwa WIP</html>\n'}, 'jagwa: 내 작업')
    sb.local_commit({'jo/data/old_run.json': '{"o": 1}'}, GEN_BASE + '2026-10-04 19:39 (1 files)')
    sb.other_push({'jo/data/other_pc.json': '{"pc": "other"}'}, GEN_BASE + '2026-10-04 19:40 (1 files)')
    sb.G(sb.genie, 'fetch', '-q', 'origin')
    sq = os.path.join(sb.root, 'seqed.py'); wr(sq, SEQED)
    sb.G(sb.genie, 'rebase', '-i', 'origin/main', check=False, env=sb.env({'GIT_SEQUENCE_EDITOR': '"%s" "%s"' % (fwd(sb.py), fwd(sq)), 'GIT_EDITOR': 'true'}))
    gd = os.path.join(sb.genie, '.git')
    it.chk('core', '장면: 멈춘 rebase', os.path.isdir(os.path.join(gd, 'rebase-merge')), '')
    h0, before_o = sb.head(), sb.ohead()
    r = sb.run(seed='A')
    it.chk('core', '판정 [NG] · rc 1', r.rc == 1 and r.tag() == '[NG]', 'tag=%s' % r.tag())
    it.chk('core', '아무것도 안 건드림 — rebase 상태 · HEAD 그대로 · 백업 없음 · push 0 · 컴파일 0', os.path.isdir(os.path.join(gd, 'rebase-merge')) and sb.head() == h0
           and not sb.backups() and sb.ohead() == before_o and sb.compiles() == 0, '')
    four_ok(it, r, '[NG]')
    return it, r


def sc_X3(ctx):
    it = Item('X3', 'push 가 거절이 아니라 막힘(인터넷 · 권한) → [NG] · [OK] 아님 · 다시 시도 안 함')
    sb = ctx.sb('x3')
    sb.hook(HOOK_REJECT)
    before_o = sb.ohead()
    r = sb.run(seed='A')
    it.chk('core', '판정 [NG] · rc 1 (push 못 했으면 [OK] 아님)', r.rc == 1 and r.tag() == '[NG]', 'tag=%s' % r.tag())
    it.chk('core', '원격 그대로 · 거절이 아니라서 한 번 다시 안 했다(push 시도 1번)', sb.ohead() == before_o and sb.last_run().count('push 안 됨') == 1, '')
    it.chk('core', '둘째 줄에 까닭 · 셋째 줄에 할 일', len(r.lines) == 4 and 'push 실패' in r.lines[1] and r.lines[2].startswith('할 일: ') and len(r.lines[2]) > 8, r.lines[1] if len(r.lines) > 1 else '')
    four_ok(it, r, '[NG]')
    # 다음 ⚙ 가 안 올라간 jo: data 커밋을 버리고 다시 만든다(원격이 풀린 뒤)
    os.remove(os.path.join(sb.genie, '.git', 'hooks', 'pre-push'))
    r2 = sb.run(seed='A')
    it.chk('core', '막힘이 풀린 뒤 ⚙ — 남은 jo: data 커밋을 버리고(백업) 다시 만들어 올라간다', r2.tag() == '[OK]' and sb.ohead() != before_o and len(sb.backups()) == 1,
           'tag=%s backups=%s' % (r2.tag(), sb.backups()))
    return it, r


def sc_X4(ctx):
    it = Item('X4', 'push 가 두 번 거절됨(남이 또 올림) → 한 번만 다시 · [NG]')
    sb = ctx.sb('x4')
    cnt = os.path.join(sb.root, 'hook_count.txt')
    sb.hook(HOOK_RACE % {'cnt': fwd(cnt), 'max': 2, 'other': fwd(sb.other)})
    r = sb.run(seed='A')
    md = sb.last_run()
    it.chk('core', '판정 [NG] · rc 1', r.rc == 1 and r.tag() == '[NG]', 'tag=%s' % r.tag())
    it.chk('core', '다시는 한 번뿐(push 시도 2번 · 훅 2회)', md.count('push 안 됨') == 2 and open(cnt).read().strip() == '2', 'push 안 됨 %d번' % md.count('push 안 됨'))
    it.chk('core', '둘째 줄 「두 번 거절」', len(r.lines) == 4 and '두 번 거절' in r.lines[1], r.lines[1] if len(r.lines) > 1 else '')
    four_ok(it, r, '[NG]')
    return it, r


def sc_X5(ctx):
    it = Item('X5', '--dry-run: 깨끗한 본 클론 → staged 만 보이고 클론 무자국 · 기준선 안 건드림 · rc 0')
    sb = ctx.sb('x5')
    h0, st0, o0 = sb.head(), sb.status(), sb.ohead()
    r = sb.run(['--dry-run'], seed='A')
    it.chk('core', '판정 [OK] · rc 0 · 드라이런 문구', r.rc == 0 and r.tag() == '[OK]' and len(r.lines) == 4 and r.lines[1].startswith('드라이런 — commit 직전에서 멈췄다'), r.lines[1] if len(r.lines) > 1 else '')
    it.chk('core', 'commit 0 · push 0 · 클론 작업트리·색인이 드라이런 전 그대로(되돌림)', sb.head() == h0 and sb.ohead() == o0 and sb.status() == st0, 'status=%r' % sb.status()[:80])
    it.chk('core', '기준선 파일 안 씀(hashlog · ids_last · inputs_last)', not any(os.path.exists(os.path.join(sb.pipe_state, f)) for f in ('hashlog.json', 'ids_last.json', 'inputs_last.json')), '')
    it.chk('core', '_out 은 만들어졌다(다른 도구가 스냅샷으로 쓴다)', os.path.isfile(os.path.join(sb.out, 'data', 'stub_a.json')), '')
    four_ok(it, r, '[OK]')
    return it, r


def sc_X6(ctx):
    it = Item('X6', '--dry-run: 멈춘 rebase 가 있는 본 클론 → 안 건드리고 알리기만 · [NG] · rc 1 · 컴파일 0')
    sb = ctx.sb('x6')
    sb.make_stuck_rebase()
    gd = os.path.join(sb.genie, '.git')
    h0, o0 = sb.head(), sb.ohead()
    r = sb.run(['--dry-run'], seed='A')
    it.chk('core', '판정 [NG] · rc 1 · 「드라이런」 문구 · 스스로 푼다 안내', r.rc == 1 and r.tag() == '[NG]' and len(r.lines) == 4 and r.lines[1].startswith('드라이런:') and '스스로 푼다' in r.lines[2],
           ' / '.join(r.lines[1:3]))
    it.chk('core', '클론 무변 — rebase 상태 그대로 · HEAD 그대로 · 원격 그대로 · 컴파일 0', os.path.isdir(os.path.join(gd, 'rebase-merge')) and sb.head() == h0 and sb.ohead() == o0 and sb.compiles() == 0, '')
    return it, r


def sc_X7(ctx):
    it = Item('X7', '_runs 순환: 이미 35 개 → 최근 30 만 남기고 나머지는 _runs\\_old\\ 로(지우지 않음)')
    sb = ctx.sb('x7')
    d = os.path.join(sb.pipe_state, '_runs')
    os.makedirs(d)
    for i in range(35):
        wr(os.path.join(d, '202610%02d-%06d_OLDPC.md' % (1 + i % 3, i)), 'old %d\n' % i)
    r = sb.run(seed='A')
    now = sorted(f for f in os.listdir(d) if f.endswith('.md'))
    old = sorted(os.listdir(os.path.join(d, '_old'))) if os.path.isdir(os.path.join(d, '_old')) else []
    it.chk('core', '_runs 에 .md 가 정확히 30 개', len(now) == 30, '%d개' % len(now))
    it.chk('core', '_old 에 6 개 · 합계 36 = 지운 것 0', len(old) == 6 and len(now) + len(old) == 36, '%d개' % len(old))
    it.chk('core', '새 기록은 _runs 에 남았다(최신) · 옮겨진 것은 가장 오래된 6 개', any(re.match(r'^\d{8}-\d{6}_TESTPC\.md$', f) for f in now) and old == sorted(
        '202610%02d-%06d_OLDPC.md' % (1 + i % 3, i) for i in range(35))[:6], '')
    return it, r


def sc_X8(ctx):
    it = Item('X8', '잠금: 이미 도는 실행이 있으면 [NG] 넉 줄 · 기록(_last_run.md · _runs\\)은 안 건드림')
    sb = ctx.sb('x8')
    lock = os.path.join(sb.local, 'jopangi', 'lock')
    os.makedirs(lock)
    r = sb.run(seed='A')
    it.chk('core', '판정 [NG] · rc 1 · 이미 돌고 있다', r.rc == 1 and r.tag() == '[NG]' and len(r.lines) == 4 and '이미 돌고 있습니다' in r.lines[1], r.lines[1] if len(r.lines) > 1 else '')
    it.chk('core', '기록 안 건드림(_last_run.md · _runs 없음) · 컴파일 0', not sb.last_run() and not sb.runs() and sb.compiles() == 0, '')
    four_ok(it, r, '[NG]')
    return it, r


def sc_X9(ctx):
    it = Item('X9', '가짜 컴파일이 검산 NG → [NG] · 아무것도 안 올림 · 기록은 남음')
    sb = ctx.sb('x9')
    before_o = sb.ohead()
    r = sb.run(seed='A', env={'JO_STUB_NG': '1'})
    it.chk('core', '판정 [NG] · push 0 · 클론 무변', r.rc == 1 and r.tag() == '[NG]' and sb.ohead() == before_o and sb.head() == sb.S0, 'tag=%s' % r.tag())
    it.chk('core', '기록 남음(_last_run.md · _runs 1개)', '판정 = **[NG]**' in sb.last_run() and len(sb.runs()) == 1, '')
    four_ok(it, r, '[NG]')
    return it, r


def sc_X10(ctx):
    it = Item('X10', '원격 받기가 고치다 만 파일과 겹침 → [NG] · 아무것도 안 잃음(내 고침 그대로)')
    sb = ctx.sb('x10')
    sb.other_push({'jo/data/seed.json': '{"seed": 1}'}, GEN_BASE + '2026-10-04 09:00 (1 files)')
    wr(os.path.join(sb.genie, 'jo', 'data', 'seed.json'), '{"seed": "내가 고치다 만 것"}')
    before_o, h0 = sb.ohead(), sb.head()
    r = sb.run(seed='A')
    it.chk('core', '판정 [NG] · rc 1 · 원격을 받다 막혔다', r.rc == 1 and r.tag() == '[NG]' and len(r.lines) == 4 and '원격을 먼저 받다 막혔다' in r.lines[1], r.lines[1] if len(r.lines) > 1 else '')
    it.chk('core', '고치다 만 파일이 그대로 · HEAD 그대로 · push 0 · 컴파일 0', open(os.path.join(sb.genie, 'jo', 'data', 'seed.json'), encoding='utf-8').read() == '{"seed": "내가 고치다 만 것"}'
           and sb.head() == h0 and sb.ohead() == before_o and sb.compiles() == 0, '')
    four_ok(it, r, '[NG]')
    return it, r


def sc_X11(ctx):
    it = Item('X11', '원격에 못 닿음(인터넷) → 만들기 전에 [NG] · 아무것도 안 바뀜')
    sb = ctx.sb('x11')
    sb.G(sb.genie, 'remote', 'set-url', 'origin', os.path.join(sb.root, 'no_such_origin.git'))
    # 일부러 샌드박스 밖이 아닌 없는 로컬 경로 — 어디에도 안 나간다
    h0 = sb.head()
    r = sb.run(seed='A')
    it.chk('core', '판정 [NG] · rc 1 · 원격을 못 받았다 · 컴파일 0 · HEAD 그대로', r.rc == 1 and r.tag() == '[NG]' and len(r.lines) == 4 and '원격을 못 받았다' in r.lines[1]
           and sb.compiles() == 0 and sb.head() == h0, r.lines[1] if len(r.lines) > 1 else '')
    four_ok(it, r, '[NG]')
    return it, r


def sc_X12(ctx):
    it = Item('X12', '분리 HEAD 인데 jo/ 밖 커밋이 걸림 → 손대지 않고 [NG](분리 HEAD 그대로 · 백업 없음)')
    sb = ctx.sb('x12')
    sb.G(sb.genie, 'checkout', '-q', '--detach')
    tip = sb.local_commit({'jagwa/index.html': '<html>jagwa WIP</html>\n'}, 'jagwa: 내 작업')
    r = sb.run(seed='A')
    it.chk('core', '판정 [NG] · 분리 HEAD 그대로 · 백업 0 · push 0 · 컴파일 0', r.rc == 1 and r.tag() == '[NG]' and sb.head() == tip and not sb.branch() and not sb.backups()
           and sb.ohead() == sb.S0 and sb.compiles() == 0, 'tag=%s br=%r' % (r.tag(), sb.branch()))
    four_ok(it, r, '[NG]')
    return it, r


def sc_X13(ctx):
    it = Item('X13', 'main 이 아닌 브랜치(jo/ 밖 커밋 있음)에 서 있음 → 브랜치 안 바꾸고 [NG]')
    sb = ctx.sb('x13')
    sb.G(sb.genie, 'checkout', '-q', '-b', 'feature-x')
    tip = sb.local_commit({'jagwa/index.html': '<html>jagwa WIP</html>\n'}, 'jagwa: 내 작업')
    r = sb.run(seed='A')
    it.chk('core', '판정 [NG] · 브랜치 feature-x 그대로 · HEAD 그대로 · push 0', r.rc == 1 and r.tag() == '[NG]' and sb.branch() == 'feature-x' and sb.head() == tip and sb.ohead() == sb.S0,
           'tag=%s br=%r' % (r.tag(), sb.branch()))
    four_ok(it, r, '[NG]')
    return it, r


def sc_X14(ctx):
    it = Item('X14', '--no-push: 본 클론에서 commit 까지만 · [OK] · 문구에 「push 안 함」')
    sb = ctx.sb('x14')
    r = sb.run(['--no-push'], seed='A')
    it.chk('core', '판정 [OK] · commit 1 · push 0', r.rc == 0 and r.tag() == '[OK]' and sb.head() != sb.S0 and sb.ohead() == sb.S0, 'tag=%s' % r.tag())
    it.chk('core', '둘째 줄에 「push 안 함」', len(r.lines) == 4 and 'push 안 함' in r.lines[1] and '올라감' not in r.lines[1], r.lines[1] if len(r.lines) > 1 else '')
    four_ok(it, r, '[OK]')
    return it, r


def sc_X15(ctx):
    it = Item('X15', '본 클론이 원격보다 앞섬(안 올린 jo: data 커밋 둘 · main) → 백업 후 버리고 다시 만들어 push')
    sb = ctx.sb('x15')
    sb.local_commit({'jo/data/old1.json': '{"a": 1}'}, GEN_BASE + '2026-10-04 19:44 (1 files)')
    tip = sb.local_commit({'jo/data/old1.json': '{"a": 2}'}, GEN_BASE + '2026-10-04 19:51 (1 files)')
    r = sb.run(seed='A')
    oh = sb.ohead()
    it.chk('core', '판정 [OK] · 백업 브랜치 = 버린 꼭대기 · push 됐다 · 본 클론 = 원격', r.tag() == '[OK]' and len(sb.backups()) == 1 and sb.gout(sb.genie, 'rev-parse', sb.backups()[0]) == tip
           and oh != sb.S0 and sb.parent(oh) == sb.S0 and sb.head() == oh, 'tag=%s backups=%s' % (r.tag(), sb.backups()))
    return it, r


# ───────────────────────────────────────── 조이기(2026-10-04 22:4x [채팅] 판정 ① ② ④ · push 조건 조이기) — Y 칸
#   ① ⚙ 는 자기가 만드는 자리(jo/data · .gitattributes)만 싣는다 · ② _meta.json 하나뿐이면 올릴 것 없음 · ④ minbeoppdf 해설 짝도 같은 차례(멈춘 상태면 hsul 만 WARN · 원격 먼저 받기 · 앞 실행 커밋도 올림)
#   바탕(= 조이기 전 정본 d0f4c1d4)에서는 Y1~Y7 이 전부 FAIL 로 서야 한다(헛잣대 · --expect base).
def sc_Y1(ctx):
    it = Item('Y1', '① 앱 파일은 ⚙ 가 안 싣는다 — 클론에 고치다 만 jo/index.html(미리 stage 한 것 · 새 파일 포함)이 있어도 staged 에 없다 · 올라간 것은 jo/data 뿐 · [OK] · 내 고침 그대로 · jo/data 안 지워진 파일은 같이 올라간다')
    sb = ctx.sb('y1')
    wip = '<html>jo app v2 — 고치다 만 것</html>\n'
    wr(os.path.join(sb.genie, 'jo', 'index.html'), wip)                    # 추적 파일의 고치다 만 것
    wr(os.path.join(sb.genie, 'jo', 'app_new.js'), 'console.log("WIP");\n')   # 새 파일(untracked)
    os.remove(os.path.join(sb.genie, 'jo', 'data', 'seed.json'))           # jo/data 안에서 지워진 추적 파일
    sb.G(sb.genie, 'add', '--', 'jo/index.html')                           # 사람이 미리 stage 해 둔 것 — ⚙ 는 색인을 비우고 시작한다 · 앱은 안 싣는다
    r = sb.run(seed='A')
    oh = sb.ohead()
    fs = sb.files_of(oh)
    ns = sb.G(sb.origin, 'diff-tree', '--no-commit-id', '--name-status', '-r', oh).stdout.splitlines()
    stl = sorted(x for x in sb.status().splitlines() if x.strip())
    it.chk('core', '판정 [OK] · rc 0', r.rc == 0 and r.tag() == '[OK]', 'rc=%d tag=%s last=%r' % (r.rc, r.tag(), r.lines[-1] if r.lines else ''))
    it.chk('core', '올라갔다 — 원격 HEAD 가 앞섬(부모 = S0)', oh != sb.S0 and sb.parent(oh) == sb.S0, 'origin=%s' % oh[:7])
    it.chk('core', '올라간 파일은 전부 jo/data/(또는 .gitattributes) 아래 · stub_a.json 포함', bool(fs) and all(f.startswith('jo/data/') or f == '.gitattributes' for f in fs)
           and 'jo/data/stub_a.json' in fs, '%s' % fs)
    it.chk('core', '앱 파일(jo/index.html · jo/app_new.js)은 커밋에 없다 · 원격의 jo/index.html 은 옛 판 그대로', 'jo/index.html' not in fs and 'jo/app_new.js' not in fs
           and sb.G(sb.origin, 'show', oh + ':jo/index.html').stdout == '<html>jo app v1</html>\n' and 'jo/app_new.js' not in sb.tree_of(oh), '')
    it.chk('core', '내 고침 그대로 — 파일 내용 · 새 파일 · 안 올린 상태(색인은 비워짐)로 남음', open(os.path.join(sb.genie, 'jo', 'index.html'), encoding='utf-8').read() == wip
           and os.path.isfile(os.path.join(sb.genie, 'jo', 'app_new.js')) and stl == [' M jo/index.html', '?? jo/app_new.js'] and not sb.G(sb.genie, 'diff', '--cached', '--name-only').stdout.strip(),
           'status=%s' % stl)
    it.chk('core', 'jo/data 안에서 지워진 추적 파일(seed.json)의 삭제도 같이 올라갔다', 'D\tjo/data/seed.json' in ns and 'jo/data/seed.json' not in sb.tree_of(oh), '%s' % ns)
    it.chk('core', '기록 로그에 「안 실었다」 — 고치다 만 jo/index.html 이름이 보인다(사용자가 알 수 있다)', any('안 실었다' in ln and 'jo/index.html' in ln for ln in md_block(sb.last_run())), '')
    four_ok(it, r, '[OK]', r'^올라감 · 커밋 [0-9a-f]{7} · 1분 뒤 앱 새로고침$')
    it.vals = {'올라간 파일': fs, '작업트리 상태(⚙ 뒤)': stl}
    return it, r


def sc_Y2(ctx):
    it = Item('Y2', '② 바뀐 것이 _meta.json(시각 줄) 하나뿐 → unstage · 「올릴 것 없음」 [OK] · commit 0 · push 0 · 작업트리 앞 판 그대로(다음 원격 받기가 안 막힌다) · 다른 파일과 같이 바뀌면 같이 올림')
    sb = ctx.sb('y2')
    NOW = {'JO_STUB_META_NOW': '1'}              # 가짜 컴파일의 「생성」 이 실행 시각 — 진짜 컴파일처럼 매번 달라진다
    r1 = sb.run(seed='A', env=NOW)
    oh1, h1 = sb.ohead(), sb.head()
    n1 = len(sb.G(sb.genie, 'rev-list', 'HEAD').stdout.split())
    meta1 = sb.G(sb.origin, 'show', oh1 + ':jo/data/_meta.json').stdout
    time.sleep(1.2)
    r2 = sb.run(seed='A', env=NOW)               # 볼트 무변 — 달라진 것은 _meta.json 의 시각 줄뿐
    new_meta = open(os.path.join(sb.out, 'data', '_meta.json'), encoding='utf-8').read()
    it.chk('core', '첫 실행 [OK](올라감 · _meta.json 도 처음 올라감)', r1.tag() == '[OK]' and oh1 != sb.S0 and 'jo/data/_meta.json' in sb.files_of(oh1), 'tag=%s' % r1.tag())
    it.chk('core', '장면: 둘째 실행의 컴파일 산출 _meta.json 은 앞 판과 다르다(시각 줄이 바뀜) · 다른 데이터는 같다', new_meta != meta1 and sb.compiles() == 2, '')
    it.chk('core', '둘째 실행 판정 [OK] · rc 0', r2.rc == 0 and r2.tag() == '[OK]', 'rc=%d tag=%s last=%r' % (r2.rc, r2.tag(), r2.lines[-1] if r2.lines else ''))
    it.chk('core', 'commit 0 · push 0 — 로컬·원격 HEAD 그대로 · 커밋 수 그대로', sb.ohead() == oh1 and sb.head() == h1 and len(sb.G(sb.genie, 'rev-list', 'HEAD').stdout.split()) == n1, '')
    it.chk('core', '색인 비어 있고 작업트리 깨끗 — _meta.json 도 앞 판 그대로 되돌림', not sb.G(sb.genie, 'diff', '--cached', '--name-only').stdout.strip() and not sb.status().strip()
           and open(os.path.join(sb.genie, 'jo', 'data', '_meta.json'), encoding='utf-8').read() == meta1, 'status=%r' % sb.status()[:80])
    it.chk('core', '기록에 「_meta.json … 하나뿐」', '하나뿐이다' in sb.last_run(), '')
    four_ok(it, r2, '[OK]', r'^올릴 것 없음\(볼트가 앱과 같음\)$')
    # 다른 PC 가 _meta.json 을 바꿔 올림(진짜 ⚙ 커밋은 거의 늘 그렇다) → 셋째 ⚙ 가 원격을 먼저 받는다 — 작업트리가 깨끗해야 ff 가 안 막힌다
    O = sb.other_push({'jo/data/_meta.json': '{"생성": "2099-01-01T00:00:00", "from": "other"}', 'jo/data/other_pc.json': '{"pc": "other"}'}, GEN_BASE + '2026-10-04 09:00 (2 files)')
    r3 = sb.run(seed='A', env=NOW)
    it.chk('core', '셋째 ⚙: 원격을 먼저 받았다(ff · 로컬 = O) · [OK] · 올릴 것 없음(다시 _meta.json 만) · 작업트리 깨끗', r3.tag() == '[OK]' and sb.head() == O and sb.ohead() == O and '원격을 먼저 받았다' in sb.last_run()
           and len(r3.lines) == 4 and r3.lines[1] == '올릴 것 없음(볼트가 앱과 같음)' and not sb.status().strip(), 'tag=%s head=%s O=%s %r' % (r3.tag(), sb.head()[:7], O[:7], r3.lines[1] if len(r3.lines) > 1 else ''))
    # 다른 파일과 같이 바뀌면 같이 올린다
    r4 = sb.run(seed='B', env=NOW)
    oh4 = sb.ohead()
    fs4 = sb.files_of(oh4)
    it.chk('core', '넷째 ⚙(seed B — stub_a.json 이 바뀜): _meta.json 과 stub_a.json 이 한 커밋으로 같이 올라갔다 · [OK]', r4.tag() == '[OK]' and oh4 != O and sb.parent(oh4) == O
           and 'jo/data/_meta.json' in fs4 and 'jo/data/stub_a.json' in fs4 and sb.head() == oh4, 'tag=%s files=%s' % (r4.tag(), fs4))
    it.vals = {'둘째 stdout': r2.lines, '넷째 올린 파일': fs4}
    return it, r2


def sc_Y3(ctx):
    it = Item('Y3', '① 버려도 되는 jo: data 커밋은 jo/data 만 건드린 것뿐 — jo/index.html 이 섞인 jo: data 커밋은 안 버리고 [NG](백업 0 · push 0 · 컴파일 0)')
    sb = ctx.sb('y3')
    tip = sb.local_commit({'jo/data/old1.json': '{"a": 1}', 'jo/index.html': '<html>jo app WIP v2</html>\n'}, GEN_BASE + '2026-10-04 19:44 (2 files)')
    before_o = sb.ohead()
    r = sb.run(seed='A')
    it.chk('core', '판정 [NG] · rc 1', r.rc == 1 and r.tag() == '[NG]', 'rc=%d tag=%s' % (r.rc, r.tag()))
    it.chk('core', '아무것도 안 버렸다 — HEAD 그대로 · main · 백업 없음 · push 0 · 컴파일 0', sb.head() == tip and sb.branch() == 'main' and not sb.backups() and sb.ohead() == before_o and sb.compiles() == 0,
           'head=%s backups=%s' % (sb.head()[:7], sb.backups()))
    it.chk('fmt', '둘째 줄에 걸린 커밋(7자)과 「jo/data 밖」이 보인다', len(r.lines) == 4 and tip[:7] in r.lines[1] and 'jo/data 밖' in r.lines[1], r.lines[1] if len(r.lines) > 1 else '')
    four_ok(it, r, '[NG]')
    return it, r


def sc_Y4(ctx):
    it = Item('Y4', '① 멈춘 rebase 를 풀 때도 앱 파일의 고치다 만 것이 있으면 안 건드리고 [NG] — --abort 가 그것을 날릴 수 있다(jo/data 의 고친 것만 풀어 준다)')
    sb = ctx.sb('y4')
    sb.local_commit({'jo/data/old_run.json': '{"o": 1}'}, GEN_BASE + '2026-10-04 19:39 (1 files)')
    sb.local_commit({'jo/data/old_run2.json': '{"o": 2}'}, GEN_BASE + '2026-10-04 19:41 (1 files)')
    sb.other_push({'jo/data/other_pc.json': '{"pc": "other"}'}, GEN_BASE + '2026-10-04 19:40 (1 files)')
    sb.G(sb.genie, 'fetch', '-q', 'origin')
    sq = os.path.join(sb.root, 'seqed.py'); wr(sq, SEQED)
    sb.G(sb.genie, 'rebase', '-i', 'origin/main', check=False, env=sb.env({'GIT_SEQUENCE_EDITOR': '"%s" "%s"' % (fwd(sb.py), fwd(sq)), 'GIT_EDITOR': 'true'}))
    gd = os.path.join(sb.genie, '.git')
    wip = '<html>jo app v2 — 고치다 만 것</html>\n'
    wr(os.path.join(sb.genie, 'jo', 'index.html'), wip)
    h0, before_o = sb.head(), sb.ohead()
    it.chk('core', '장면: 멈춘 rebase(남은 일 있음) + 추적 파일 jo/index.html 을 고치다 만 상태', os.path.isdir(os.path.join(gd, 'rebase-merge')) and ' M jo/index.html' in sb.status().splitlines(), '')
    r = sb.run(seed='A')
    it.chk('core', '판정 [NG] · rc 1', r.rc == 1 and r.tag() == '[NG]', 'rc=%d tag=%s last=%r' % (r.rc, r.tag(), r.lines[-1] if r.lines else ''))
    it.chk('core', '아무것도 안 건드림 — rebase 상태 · HEAD 그대로 · 백업 없음 · push 0 · 컴파일 0', os.path.isdir(os.path.join(gd, 'rebase-merge')) and sb.head() == h0
           and not sb.backups() and sb.ohead() == before_o and sb.compiles() == 0, '')
    it.chk('core', '고치다 만 jo/index.html 이 그대로다(--abort 가 날리지 않았다)', os.path.isfile(os.path.join(sb.genie, 'jo', 'index.html'))
           and open(os.path.join(sb.genie, 'jo', 'index.html'), encoding='utf-8').read() == wip, '')
    four_ok(it, r, '[NG]')
    return it, r


def mbp_scene(sb, kind):
    """minbeoppdf 클론을 멈춘 상태로 만든다 — kind: rebase(충돌로 멈춘 rebase) | merge(충돌 난 merge) | detach(분리된 HEAD)"""
    if kind == 'detach':
        sb.G(sb.mbp, 'checkout', '-q', '--detach')
        return
    sb.mbp_local_commit({'hsul/민소.json': '{"law": "민소", "seed": "local"}'}, 'hsul: 해설 짝 2026-10-04 19:00 (1 files)')
    sb.mbp_other_push({'hsul/민소.json': '{"law": "민소", "seed": "other"}'}, 'hsul: 해설 짝 2026-10-04 19:01 (1 files)')
    sb.G(sb.mbp, 'fetch', '-q', 'origin')
    sb.G(sb.mbp, 'rebase' if kind == 'rebase' else 'merge', 'origin/main', check=False)


def mbp_fp(sb):
    """minbeoppdf 클론 지문 — HEAD · 브랜치 · 작업트리 · 멈춘 상태 · 원격"""
    gd = os.path.join(sb.mbp, '.git')
    return {'head': sb.gout(sb.mbp, 'rev-parse', 'HEAD'), 'branch': sb.branch(sb.mbp), 'status': sb.status_of(sb.mbp),
            'rebase': os.path.isdir(os.path.join(gd, 'rebase-merge')), 'merge': os.path.isfile(os.path.join(gd, 'MERGE_HEAD')),
            'origin': sb.gout(sb.mbp_origin, 'rev-parse', 'refs/heads/main')}


def sc_Y5(ctx):
    it = Item('Y5', '④ minbeoppdf 클론이 멈춘 상태(rebase · merge 중 · 분리 HEAD)면 hsul 만 [WARN] + 할 일 — 클론은 한 글자도 안 건드리고 · 만들기 0 · genie 는 막히지 않는다([OK] · 올라감)')
    last = None
    for kind, label in (('rebase', 'rebase 중'), ('merge', 'merge 중'), ('detach', '분리된 HEAD')):
        sb = ctx.sb('y5_' + kind)
        sb.with_mbp()
        mbp_scene(sb, kind)
        before = mbp_fp(sb)
        stood = {'rebase': before['rebase'], 'merge': before['merge'], 'detach': not before['branch']}[kind]
        it.chk('core', '%s: 장면 — 멈춘 상태가 섰다' % label, stood, 'branch=%r rebase=%s merge=%s' % (before['branch'], before['rebase'], before['merge']))
        r = sb.run(seed='A')
        after = mbp_fp(sb)
        md = sb.last_run()
        it.chk('core', '%s: genie 는 막히지 않았다 — [OK] · rc 0 · 올라감(원격 HEAD 앞섬)' % label, r.rc == 0 and r.tag() == '[OK]' and sb.ohead() != sb.S0 and len(r.lines) == 4 and r.lines[1].startswith('올라감'),
               'rc=%d tag=%s l2=%r' % (r.rc, r.tag(), r.lines[1] if len(r.lines) > 1 else ''))
        it.chk('core', '%s: hsul 만 WARN — 해설짝 WARN 행 · 셋째 줄 할 일에 minbeoppdf · 해설짝 OK 행 없음' % label, bool(re.search(r'^\| WARN \| 해설짝 \|', md, re.M)) and len(r.lines) == 4
               and r.lines[2].startswith('할 일: ') and 'minbeoppdf' in r.lines[2] and not re.search(r'^\| OK \| 해설짝 \|', md, re.M), r.lines[2] if len(r.lines) > 2 else '')
        it.chk('core', '%s: minbeoppdf 클론 무변 — HEAD · 브랜치 · 작업트리 · 멈춘 상태 · 원격 그대로 · 만들기 0번' % label, after == before and not sb.hsul_builds(),
               '만들기 %d번 · head %s→%s' % (len(sb.hsul_builds()), before['head'][:7], after['head'][:7]))
        four_ok(it, r, '[OK]')
        last = r
    return it, last


def sc_Y6(ctx):
    it = Item('Y6', '④ minbeoppdf: 원격을 만들기 전에 먼저 받는다(ff · pull --rebase 0) → 만들기 → commit → push — 다른 PC 가 같은 파일을 먼저 올려도 충돌 없이 올라간다 · [OK]')
    sb = ctx.sb('y6')
    sb.with_mbp()
    O = sb.mbp_other_push({'hsul/민소.json': '{"law": "민소", "seed": "other"}', 'hsul/특허.json': '{"law": "특허", "seed": "other"}'}, 'hsul: 해설 짝 2026-10-04 19:01 (2 files)')
    r = sb.run(seed='A')
    mo = sb.gout(sb.mbp_origin, 'rev-parse', 'refs/heads/main')
    md = sb.last_run()
    builds = sb.hsul_builds()
    fs = sb.files_of(mo, sb.mbp_origin)
    it.chk('core', '판정 [OK] · rc 0 · genie 도 올라갔다', r.rc == 0 and r.tag() == '[OK]' and sb.ohead() != sb.S0, 'rc=%d tag=%s' % (r.rc, r.tag()))
    it.chk('core', 'minbeoppdf 원격 이력 M0 ← 남의 커밋 ← 내 커밋(일직선) · 제목 hsul: 해설 짝', mo != O and sb.parent(mo, sb.mbp_origin) == O and sb.parent(O, sb.mbp_origin) == sb.M0
           and sb.subject(mo, sb.mbp_origin).startswith('hsul: 해설 짝 '), 'parent=%s O=%s' % (sb.parent(mo, sb.mbp_origin)[:7], O[:7]))
    it.chk('core', '올라간 것은 hsul/민소.json · hsul/특허.json 뿐 · 내용 = 이번 만들기(seed A)', sorted(fs) == ['hsul/민소.json', 'hsul/특허.json']
           and '"seed": "A"' in sb.G(sb.mbp_origin, 'show', mo + ':hsul/민소.json').stdout, '%s' % fs)
    it.chk('core', '만들기 전에 원격을 먼저 받았다 — 가짜 만들기가 볼 때 minbeoppdf HEAD = 남의 커밋(O)', len(builds) == 2 and all(b.split()[-1] == O[:7] for b in builds), '%s O=%s' % (builds, O[:7]))
    it.chk('core', 'rebase 0 — reflog 에 rebase 없음 · rebase-merge 없음 · 로컬 = 원격 · main', 'rebase' not in sb.reflog(sb.mbp) and not os.path.isdir(os.path.join(sb.mbp, '.git', 'rebase-merge'))
           and sb.head(sb.mbp) == mo and sb.branch(sb.mbp) == 'main', sb.reflog(sb.mbp).splitlines()[0] if sb.reflog(sb.mbp) else '')
    it.chk('core', '기록: 해설짝 OK 행(commit · push) · 해설짝 WARN 행 없음 · 셋째 줄 할 일 없음', bool(re.search(r'^\| OK \| 해설짝 \|[^\n]*push', md, re.M)) and not re.search(r'^\| WARN \| 해설짝 \|', md, re.M)
           and len(r.lines) == 4 and r.lines[2] == '할 일: 없음', r.lines[2] if len(r.lines) > 2 else '')
    four_ok(it, r, '[OK]', r'^올라감 · 커밋 [0-9a-f]{7} · 1분 뒤 앱 새로고침$')
    it.vals = {'만들기 줄': builds, 'minbeoppdf 원격': mo[:7]}
    return it, r


def sc_Y7(ctx):
    it = Item('Y7', '④ 앞 실행이 못 올린 hsul 커밋(push 실패 · commit 은 남음)은 다음 ⚙ 가 같이 올린다 — 입력이 같아 새로 commit 할 것이 없어도 · 못 올린 판은 WARN + 할 일')
    sb = ctx.sb('y7')
    sb.with_mbp()
    hk = os.path.join(sb.mbp, '.git', 'hooks', 'pre-push')
    sb.hook(HOOK_REJECT, repo=sb.mbp)
    r1 = sb.run(seed='A')
    m_local, m_origin = sb.head(sb.mbp), sb.gout(sb.mbp_origin, 'rev-parse', 'refs/heads/main')
    md1 = sb.last_run()
    it.chk('core', '첫 실행: genie [OK](올라감) · hsul 커밋은 minbeoppdf 에 남고 push 는 거절됨(원격 그대로)', r1.rc == 0 and r1.tag() == '[OK]' and sb.ohead() != sb.S0 and m_local != sb.M0 and m_origin == sb.M0,
           'tag=%s local=%s origin=%s M0=%s' % (r1.tag(), m_local[:7], m_origin[:7], sb.M0[:7]))
    it.chk('core', '첫 실행: 해설짝 WARN 행(push 실패) · 셋째 줄 할 일에 minbeoppdf · 다시 ⚙', bool(re.search(r'^\| WARN \| 해설짝 \|[^\n]*push 실패', md1, re.M)) and len(r1.lines) == 4
           and r1.lines[2].startswith('할 일: ') and 'minbeoppdf' in r1.lines[2] and '다시 ⚙' in r1.lines[2], r1.lines[2] if len(r1.lines) > 2 else '')
    os.remove(hk)                                    # 막힘이 풀림
    r2 = sb.run(seed='A')
    md2 = sb.last_run()
    it.chk('core', '둘째 실행: genie [OK] · 올릴 것 없음 · 같은 hsul 커밋이 올라갔다(원격 = 첫 실행의 로컬 커밋 · 새 commit 0)', r2.rc == 0 and r2.tag() == '[OK]' and len(r2.lines) == 4 and r2.lines[1] == '올릴 것 없음(볼트가 앱과 같음)'
           and sb.gout(sb.mbp_origin, 'rev-parse', 'refs/heads/main') == m_local and sb.head(sb.mbp) == m_local, 'tag=%s origin=%s local=%s' % (
               r2.tag(), sb.gout(sb.mbp_origin, 'rev-parse', 'refs/heads/main')[:7], sb.head(sb.mbp)[:7]))
    it.chk('core', '둘째 실행: 해설짝 OK 행(앞 실행이 못 올린 커밋을 올렸다) · WARN 행 없음 · 셋째 줄 할 일 없음', bool(re.search(r'^\| OK \| 해설짝 \|[^\n]*앞 실행이 못 올린', md2, re.M)) and not re.search(r'^\| WARN \| 해설짝 \|', md2, re.M)
           and len(r2.lines) == 4 and r2.lines[2] == '할 일: 없음', r2.lines[2] if len(r2.lines) > 2 else '')
    four_ok(it, r2, '[OK]', r'^올릴 것 없음\(볼트가 앱과 같음\)$')
    return it, r2


def sc_R1(ctx):
    real = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'jopangi', '_out')
    it = Item('R1', '진짜 컴파일 산출물 재생(내 PC 의 %LOCALAPPDATA%\\jopangi\\_out · 읽기만) — 같은 흐름이 실제 크기 · 실제 _meta.json 에서도 돈다')
    if not os.path.isfile(os.path.join(real, 'data', '_meta.json')):
        it.chk('core', '재생할 진짜 산출물이 이 PC 에 있다', False, real)
        return it, None
    meta = json.load(open(os.path.join(real, 'data', '_meta.json'), encoding='utf-8'))
    warn_real = sum(1 for r in meta['검산'] if r['판정'] == 'WARN')
    nfiles = sum(1 for _r, _d, fs in os.walk(os.path.join(real, 'data')) for f in fs if not f.endswith(('.py', '.bak')))   # stage_jo.stage 가 옮기는 것만
    sb = ctx.sb('r1')
    r1 = sb.run(seed='A', env={'JO_STUB_REPLAY': real})
    oh = sb.ohead()
    fs = sb.files_of(oh)
    md = sb.last_run()
    warn_md = len(re.findall(r'^\| WARN \|', md, re.M))
    it.chk('core', '판정 [OK] · 올라감 · 원격 HEAD = 새 커밋', r1.rc == 0 and r1.tag() == '[OK]' and oh != sb.S0 and sb.parent(oh) == sb.S0, 'tag=%s' % r1.tag())
    it.chk('core', '진짜 data 파일이 전부 올라갔다(전부 jo/ 아래 · 개수 일치)', len(fs) == nfiles and all(f.startswith('jo/') for f in fs), 'data %d개 → 커밋 %d개' % (nfiles, len(fs)))
    it.chk('core', 'WARN 수 = 진짜 _meta.json 의 WARN 행 수(넷째 줄 · 기록 표)', len(r1.lines) == 4 and r1.lines[3].startswith('WARN %d건' % warn_real) and warn_md == warn_real,
           '진짜 %d · 표 %d · 넷째 줄 %s' % (warn_real, warn_md, r1.lines[3] if len(r1.lines) > 3 else ''))
    four_ok(it, r1, '[OK]')
    r2 = sb.run(seed='A', env={'JO_STUB_REPLAY': real})
    it.chk('core', '같은 산출물로 한 번 더 → 올릴 것 없음 · 커밋 0(되돌아감 · ID 기준선 포함 통과)', r2.rc == 0 and r2.tag() == '[OK]' and len(r2.lines) == 4 and r2.lines[1] == '올릴 것 없음(볼트가 앱과 같음)'
           and sb.ohead() == oh, r2.lines[1] if len(r2.lines) > 1 else '')
    it.vals = {'data 파일': nfiles, '진짜 WARN 행': warn_real, '첫 실행 초': round(r1.secs, 1), '둘째 실행 초': round(r2.secs, 1)}
    return it, r1


def sc_X22(ctx):
    it = Item('X22', '오늘 꼴 그대로(10/4 19:44 · 19:51): 멈춘 rebase 위에서 ⚙ 가 분리 HEAD 에 jo: data 커밋 둘을 더 얹은 상태 → continue · 셋 다 백업 후 버리고 다시 만들어 push [OK]')
    sb = ctx.sb('x22')
    sb.make_stuck_rebase()
    sb.local_commit({'jo/data/e844317.json': '{"t": "19:44"}'}, GEN_BASE + '2026-10-04 19:44 (3 files)')
    tip = sb.local_commit({'jo/data/e844317.json': '{"t": "19:51"}'}, GEN_BASE + '2026-10-04 19:51 (1 files)')
    gd = os.path.join(sb.genie, '.git')
    it.chk('core', '장면: 멈춘 rebase 가 남아 있고 분리 HEAD 에 커밋이 얹혀 있다', os.path.isdir(os.path.join(gd, 'rebase-merge')) and not sb.branch() and sb.head() == tip, '')
    before_o = sb.ohead()
    r = sb.run(seed='A')
    oh = sb.ohead()
    it.chk('core', '판정 [OK] · rebase 풀림 · main · push 됐다(원격 위 한 줄)', r.rc == 0 and r.tag() == '[OK]' and not os.path.isdir(os.path.join(gd, 'rebase-merge')) and sb.branch() == 'main'
           and oh != before_o and sb.parent(oh) == before_o and sb.head() == oh, 'tag=%s last=%r' % (r.tag(), r.lines[-1] if r.lines else ''))
    bak = sb.backups()
    it.chk('core', '백업 브랜치 하나 = 얹힌 꼭대기 커밋(셋이 다 백업에 있다) · 원격 이력엔 없다', len(bak) == 1 and sb.gout(sb.genie, 'rev-parse', bak[0]) == tip
           and len(sb.G(sb.genie, 'rev-list', 'origin/main..' + bak[0]).stdout.split()) == 3, 'backups=%s' % bak)
    four_ok(it, r, '[OK]')
    return it, r


def sc_X21(ctx):
    it = Item('X21', '--dry-run: 드라이런 전에 이미 고쳐져 있던 jo/ 파일은 안 건드린다(드라이런이 옮긴 것만 되돌림)')
    sb = ctx.sb('x21')
    wr(os.path.join(sb.genie, 'jo', 'data', 'seed.json'), '{"seed": "내가 고치다 만 것"}')
    st0, h0 = sb.status(), sb.head()
    r = sb.run(['--dry-run'], seed='A')
    it.chk('core', '판정 [OK] · 드라이런 · commit 0', r.rc == 0 and r.tag() == '[OK]' and len(r.lines) == 4 and r.lines[1].startswith('드라이런') and sb.head() == h0, r.lines[1] if len(r.lines) > 1 else '')
    it.chk('core', '고치다 만 파일 그대로 · 작업트리 상태가 드라이런 전과 같다(옮긴 stub 파일만 사라짐)', open(os.path.join(sb.genie, 'jo', 'data', 'seed.json'), encoding='utf-8').read() == '{"seed": "내가 고치다 만 것"}'
           and sb.status() == st0, 'before=%r after=%r' % (st0.strip(), sb.status().strip()))
    four_ok(it, r, '[OK]')
    return it, r


def sc_X20(ctx):
    it = Item('X20', '공개 저장소 가드: jo/ 안에 PDF 가 섞이면 → 전부 unstage · [NG] · 아무것도 안 올림(옛 판 가드 그대로)')
    sb = ctx.sb('x20')
    wr(os.path.join(sb.genie, 'jo', 'data', 'leak.pdf'), '%PDF-1.4 시험용\n')
    before_o, h0 = sb.ohead(), sb.head()
    r = sb.run(seed='A')
    it.chk('core', '판정 [NG] · staged 에 올리면 안 되는 것이 섞였다 · push 0 · commit 0 · 색인 비움', r.rc == 1 and r.tag() == '[NG]' and len(r.lines) == 4 and '올리면 안 되는 것' in r.lines[1]
           and sb.ohead() == before_o and sb.head() == h0 and not sb.G(sb.genie, 'diff', '--cached', '--name-only').stdout.strip(), r.lines[1] if len(r.lines) > 1 else '')
    four_ok(it, r, '[NG]')
    return it, r


def sc_X19(ctx):
    it = Item('X19', 'git 이 안 됨(index.lock — 다른 git 이 도는 중) → 「올릴 것 없음」 [OK] 로 새지 않고 [NG]')
    sb = ctx.sb('x19')
    wr(os.path.join(sb.genie, '.git', 'index.lock'), '')
    before_o, h0 = sb.ohead(), sb.head()
    r = sb.run(seed='A')
    it.chk('core', '판정 [NG] · rc 1 · git reset 이 안 됐다 · push 0 · HEAD 그대로', r.rc == 1 and r.tag() == '[NG]' and len(r.lines) == 4 and 'git reset 이 안 됐다' in r.lines[1]
           and sb.ohead() == before_o and sb.head() == h0, r.lines[1] if len(r.lines) > 1 else '')
    four_ok(it, r, '[NG]')
    os.remove(os.path.join(sb.genie, '.git', 'index.lock'))
    r2 = sb.run(seed='A')
    it.chk('core', '잠금이 풀린 뒤 ⚙ → 올라간다', r2.tag() == '[OK]' and sb.ohead() != before_o, 'tag=%s' % r2.tag())
    return it, r


def sc_X18(ctx):
    it = Item('X18', '멈춘 rebase(남은 일 0 · 깨끗)인데 걸린 커밋이 jo/ 밖(내 작업) → 이어 주지도 않고 [NG](rebase 상태 그대로)')
    sb = ctx.sb('x18')
    sb.make_stuck_rebase({'jagwa/index.html': '<html>jagwa WIP</html>\n'}, 'jagwa: 내 작업')
    gd = os.path.join(sb.genie, '.git')
    h0, before_o = sb.head(), sb.ohead()
    r = sb.run(seed='A')
    it.chk('core', '판정 [NG] · rc 1', r.rc == 1 and r.tag() == '[NG]', 'tag=%s' % r.tag())
    it.chk('core', '아무것도 안 건드림 — rebase 상태 · HEAD 그대로 · 백업 없음 · push 0 · 컴파일 0', os.path.isdir(os.path.join(gd, 'rebase-merge')) and sb.head() == h0
           and not sb.backups() and sb.ohead() == before_o and sb.compiles() == 0, '')
    four_ok(it, r, '[NG]')
    return it, r


def sc_X16(ctx):
    it = Item('X16', '멈춘 merge(충돌 · jo: data 커밋뿐) → --abort 로 풀고 다시 만들어 push [OK]')
    sb = ctx.sb('x16')
    sb.local_commit({'jo/data/seed.json': '{"seed": "local"}'}, GEN_BASE + '2026-10-04 19:39 (1 files)')
    sb.other_push({'jo/data/seed.json': '{"seed": "remote"}'}, GEN_BASE + '2026-10-04 19:40 (1 files)')
    sb.G(sb.genie, 'fetch', '-q', 'origin')
    sb.G(sb.genie, 'merge', 'origin/main', check=False)
    gd = os.path.join(sb.genie, '.git')
    it.chk('core', '장면: MERGE_HEAD 가 있고 충돌 파일이 있다', os.path.isfile(os.path.join(gd, 'MERGE_HEAD')) and 'UU' in sb.G(sb.genie, 'status', '--porcelain', '-uno').stdout, '')
    before_o = sb.ohead()
    r = sb.run(seed='A')
    oh = sb.ohead()
    it.chk('core', '판정 [OK] · merge --abort 로 풀었다 · MERGE_HEAD 없음 · main', r.tag() == '[OK]' and 'merge --abort' in sb.last_run() and not os.path.isfile(os.path.join(gd, 'MERGE_HEAD'))
           and sb.branch() == 'main', 'tag=%s last=%r' % (r.tag(), r.lines[-1] if r.lines else ''))
    it.chk('core', '버린 jo: data 커밋은 백업 브랜치에 · push 됐다(원격 위 한 줄)', len(sb.backups()) == 1 and oh != before_o and sb.parent(oh) == before_o and sb.head() == oh, 'backups=%s' % sb.backups())
    four_ok(it, r, '[OK]')
    return it, r


def sc_X17(ctx):
    it = Item('X17', '--dry-run: 인터넷이 없어도(원격 못 받음) 계속한다 — 컴파일 · staged 까지 · 클론 무자국')
    sb = ctx.sb('x17')
    sb.G(sb.genie, 'remote', 'set-url', 'origin', os.path.join(sb.root, 'no_such_origin.git'))
    h0, st0 = sb.head(), sb.status()
    r = sb.run(['--dry-run'], seed='A')
    it.chk('core', '판정 [OK] · 드라이런 문구 · 컴파일 1 · 클론 그대로', r.rc == 0 and r.tag() == '[OK]' and len(r.lines) == 4 and r.lines[1].startswith('드라이런 — commit 직전에서 멈췄다')
           and sb.compiles() == 1 and sb.head() == h0 and sb.status() == st0, r.lines[1] if len(r.lines) > 1 else '')
    it.chk('core', '기록에 「원격을 못 받았다(드라이런이라 계속한다)」', '원격을 못 받았다(드라이런이라 계속한다)' in sb.last_run(), '')
    four_ok(it, r, '[OK]')
    return it, r


# ───────────────────────────────────────── 라이브러리(add1) — venv 안에서만
def build_probe_wheel(dst_dir, name='jo_pipe_probe_lib', ver='0.0.1'):
    """없는 이름 흉내 말고 「진짜 깔리는 가짜 바퀴」 — --user 기본 형태 시험용(순수 파이썬 · 아무 것도 안 한다)"""
    os.makedirs(dst_dir, exist_ok=True)
    whl = os.path.join(dst_dir, '%s-%s-py3-none-any.whl' % (name, ver))
    di = '%s-%s.dist-info' % (name, ver)
    files = {'%s/__init__.py' % name: b'VALUE = 1\n',
             '%s/METADATA' % di: ('Metadata-Version: 2.1\nName: %s\nVersion: %s\n' % (name.replace('_', '-'), ver)).encode(),
             '%s/WHEEL' % di: b'Wheel-Version: 1.0\nGenerator: harness\nRoot-Is-Purelib: true\nTag: py3-none-any\n'}
    import base64
    rec = []
    for p, b in files.items():
        h = base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b'=').decode()
        rec.append('%s,sha256=%s,%d' % (p, h, len(b)))
    rec.append('%s/RECORD,,' % di)
    files['%s/RECORD' % di] = ('\n'.join(rec) + '\n').encode()
    with zipfile.ZipFile(whl, 'w', zipfile.ZIP_DEFLATED) as z:
        for p, b in files.items():
            z.writestr(p, b)
    return whl


def pip_json(py, env=None):
    r = subprocess.run([py, '-m', 'pip', 'list', '--format=json', '--disable-pip-version-check'], capture_output=True, text=True, env=env)
    try:
        return sorted((x['name'].lower(), x['version']) for x in json.loads(r.stdout))
    except Exception:
        return None


def make_venv(ctx, name):
    vd = os.path.join(ctx.work, name)
    rm_rf(vd)
    subprocess.run([ctx.py, '-m', 'venv', vd], check=True, capture_output=True)
    vpy = os.path.join(vd, 'Scripts', 'python.exe')
    e = {k: v for k, v in os.environ.items() if not k.startswith('PIP_')}
    e['PIP_REQUIRE_VIRTUALENV'] = '1'
    wh = ctx.a.wheelhouse
    cmd = [vpy, '-m', 'pip', 'install', '-q', '--disable-pip-version-check']
    if wh and os.path.isdir(wh):
        cmd += ['--no-index', '--find-links', wh]
    r = subprocess.run(cmd + ['pymupdf', 'numpy'], capture_output=True, text=True, env=e)
    assert r.returncode == 0, 'venv 에 pymupdf · numpy 를 못 깔았다: ' + (r.stderr or r.stdout)[-300:]
    pf = subprocess.run([vpy, '-c', 'import pdfplumber'], capture_output=True, text=True)
    assert pf.returncode != 0, 'venv 에 pdfplumber 가 이미 있다(시험 틀)'
    return vpy


def venv_env(ctx, extra=None):
    e = {'PIP_REQUIRE_VIRTUALENV': '1', 'JO_PIPE_PIP_ARGS': '', 'JO_STUB_NC': '1', 'PIP_DISABLE_PIP_VERSION_CHECK': '1'}
    if ctx.a.wheelhouse and os.path.isdir(ctx.a.wheelhouse):
        e.update({'PIP_NO_INDEX': '1', 'PIP_FIND_LINKS': os.path.abspath(ctx.a.wheelhouse)})
    if extra:
        e.update(extra)
    return e


def nc_rows(md):
    rows = {}
    for ln in md.splitlines():
        m = re.match(r'^\| (\w+) \| (NC1|NCO) \| ([^|]*) \| ([^|]*) \|', ln)
        if m:
            rows[m.group(2)] = (m.group(1), m.group(4).strip())
    return rows


def lib_row(md):
    for ln in md.splitlines():
        if '| 라이브러리 |' in ln:
            return ln
    return ''


def sc_L(ctx, vpy, base_pipe):
    """add1 B-3(헛잣대) → B-1(스스로 깔기 · 두 번째 설치 0 · 시간 차) → B-2(pip 실패)"""
    out = []
    noadd1 = os.path.join(ctx.work, 'jo_pipe_noadd1.py')
    src = open(ctx.pipe, 'rb').read().decode('utf-8')
    pat = "    ok, lmsg = lib_step()\r\n    if not ok:\r\n        return ng(lmsg, R['todo'])\r\n"
    has_add1 = pat in src
    if has_add1:
        open(noadd1, 'wb').write(src.replace(pat, "    pass   # add1 전 판 흉내(헛잣대) — lib_step 호출만 뺀다\r\n").encode('utf-8'))
    else:
        noadd1 = base_pipe or ctx.pipe

    # ── add1 B-3 헛잣대: lib_step 호출이 없는 판 · 같은 venv → NC1 · NCO WARN 「No module named」
    c3 = Ctx_clone(ctx, noadd1)
    it3 = Item('a1-B3', '헛잣대 — add1 전 판 · pdfplumber 뺀 venv → NC1 · NCO WARN 「No module named」')
    sb3 = c3.sb('l3')
    r3 = sb3.run(seed='A', py=vpy, env=venv_env(ctx))
    rows3 = nc_rows(sb3.last_run())
    it3.chk('core', "NC1 · NCO 둘 다 WARN · 「No module named 'pdfplumber'」", rows3.get('NC1', ('', ''))[0] == 'WARN' and rows3.get('NCO', ('', ''))[0] == 'WARN'
            and "No module named 'pdfplumber'" in rows3.get('NC1', ('', ''))[1], '%s' % rows3)
    it3.chk('core', 'venv 는 그대로 pdfplumber 가 없다(아무도 안 깔았다)', subprocess.run([vpy, '-c', 'import pdfplumber'], capture_output=True).returncode != 0, '')
    out.append((it3, r3))

    # ── add1 B-1: 새 판 · 같은 venv → 스스로 깔고 NC1 · NCO 정상
    it1 = Item('a1-B1', 'pdfplumber 뺀 venv 에서 ⚙ → 스스로 깔고 NC1 · NCO 정상 · 두 번째 실행 = 설치 0 · 시간 차 ≤ 2 초')
    sb1 = ctx.sb('l1')
    t0 = time.time()
    r1 = sb1.run(seed='A', py=vpy, env=venv_env(ctx))
    rows1 = nc_rows(sb1.last_run())
    md1 = sb1.last_run()
    it1.chk('core', '판정 [OK] · rc 0', r1.rc == 0 and r1.tag() == '[OK]', 'rc=%d tag=%s last=%r' % (r1.rc, r1.tag(), r1.lines[-1] if r1.lines else ''))
    it1.chk('core', 'pdfplumber 설치함(기록 · 넷째 줄)', '파이썬 라이브러리 pdfplumber 설치함' in md1 and len(r1.lines) == 4 and 'pdfplumber 설치함' in r1.lines[3], r1.lines[3] if len(r1.lines) > 3 else '')
    it1.chk('core', 'NC1 · NCO 정상(WARN 아님 · 「실패」 아님)', all(rows1.get(k, ('WARN', ''))[0] == 'INFO' and not rows1[k][1].startswith('실패') for k in ('NC1', 'NCO')), '%s' % rows1)
    it1.chk('core', 'venv 안에 깔렸다 · 파이썬 전역에는 안 닿았다(PIP_REQUIRE_VIRTUALENV · --user 아님)', subprocess.run([vpy, '-c', 'import pdfplumber, sys; sys.exit(0 if sys.prefix != sys.base_prefix else 1)'], capture_output=True).returncode == 0, '')
    it1.vals['첫 실행(설치 포함) 초'] = round(r1.secs, 1)
    it1.vals['첫 실행 stdout'] = r1.lines
    # 둘째 실행 — 설치 0 · 시간
    new_t, noadd_t, lib_ms = [], [], None
    for k in range(2):
        s2 = ctx.sb('l1_%d' % k)
        ra = s2.run(seed='A', py=vpy, env=venv_env(ctx))
        new_t.append(ra.secs)
        row = lib_row(s2.last_run())
        m = re.search(r'\((\d+) ms\)', row)
        lib_ms = int(m.group(1)) if m else lib_ms
        it1.chk('core', '두 번째 실행 %d — 설치 0 · 「설치함」 없음 · 라이브러리 행 OK' % (k + 1), 'OK' in row and '설치함' not in s2.last_run().split('```')[0] and 'pip install' not in s2.last_run().split('```')[1], row[:90])
        c0 = Ctx_clone(ctx, noadd1)
        s0 = c0.sb('l0_%d' % k)
        rb = s0.run(seed='A', py=vpy, env=venv_env(ctx))
        noadd_t.append(rb.secs)
    diff = min(new_t) - min(noadd_t)
    it1.chk('core', '시간 차 ≤ 2 초(add1 전 판 대비 · 두 번씩 재서 짧은 쪽끼리)', diff <= 2.0 and (lib_ms is None or lib_ms <= 2000), '새 %s · 전 %s → 차 %.2f초 · 라이브러리 확인 %s ms' % (
        [round(x, 2) for x in new_t], [round(x, 2) for x in noadd_t], diff, lib_ms))
    it1.vals.update({'두번째 새 판 초': [round(x, 2) for x in new_t], 'add1 전 판 초': [round(x, 2) for x in noadd_t], '확인 ms': lib_ms})
    out.append((it1, r1))

    # ── add1 B-2: pip 실패(없는 이름 흉내) → [NG] · 셋째 줄 할 일 · 아무것도 안 올림
    it2 = Item('a1-B2', 'pip 실패(없는 이름) → [NG] · 셋째 줄 할 일 · 아무것도 안 올림')
    sb2 = ctx.sb('l2')
    before_o = sb2.ohead()
    r2 = sb2.run(seed='A', py=vpy, env=venv_env(ctx, {'JO_PIPE_EXTRA_LIBS': 'zz_no_such_pkg_jopipe', 'PIP_NO_INDEX': '1'}))
    it2.chk('core', '판정 [NG] · rc 1', r2.rc == 1 and r2.tag() == '[NG]', 'rc=%d tag=%s' % (r2.rc, r2.tag()))
    it2.chk('core', '둘째 줄 「<이름> 설치 실패 · 까닭 첫 줄」', len(r2.lines) == 4 and r2.lines[1].startswith('zz_no_such_pkg_jopipe 설치 실패 · ') and len(r2.lines[1]) > 40, r2.lines[1] if len(r2.lines) > 1 else '')
    it2.chk('core', '셋째 줄 = 할 일(CMD 한 줄 포함)', len(r2.lines) == 4 and r2.lines[2].startswith('할 일: ') and 'pip install' in r2.lines[2], r2.lines[2] if len(r2.lines) > 2 else '')
    it2.chk('core', '아무것도 안 올림 · 컴파일 0 · 클론 무변', sb2.ohead() == before_o and sb2.head() == sb2.S0 and sb2.compiles() == 0, '')
    four_ok(it2, r2, '[NG]')
    it2.vals['stdout'] = r2.lines
    out.append((it2, r2))

    # ── 기본 형태(--user) 시험 — 전역 파이썬 + 가짜 APPDATA · PYTHONUSERBASE(샌드박스) + 가짜 바퀴 · 없는 이름 아님
    it4 = Item('a1-B4', '기본 형태 pip install --user (샌드박스 사용자 자리) → 설치 · 같은 실행의 컴파일이 그 라이브러리를 본다')
    sb4 = ctx.sb('l4')
    wh = os.path.join(sb4.root, 'wheels')
    build_probe_wheel(wh)
    ub = os.path.join(sb4.root, 'userbase')
    r4 = sb4.run(seed='A', env={'JO_PIPE_EXTRA_LIBS': 'jo_pipe_probe_lib', 'PIP_NO_INDEX': '1', 'PIP_FIND_LINKS': wh, 'PYTHONUSERBASE': ub, 'JO_STUB_IMPORT': 'jo_pipe_probe_lib'})
    md4 = sb4.last_run()
    inst = []
    for root, _d, fs in os.walk(ub):
        inst += [f for f in fs if f == '__init__.py' and 'jo_pipe_probe_lib' in root]
    it4.chk('core', '판정 [OK] · 설치함', r4.rc == 0 and r4.tag() == '[OK]' and 'jo_pipe_probe_lib 설치함' in md4, 'tag=%s' % r4.tag())
    it4.chk('core', '샌드박스 사용자 자리(PYTHONUSERBASE)에 깔렸다 — 진짜 사용자 자리 아님', bool(inst), '%s' % inst)
    it4.chk('core', '컴파일(자식 프로세스)이 그 라이브러리를 import 했다', '[stub] import jo_pipe_probe_lib OK' in md4, '')
    out.append((it4, r4))
    return out


class Ctx_clone(Ctx):
    """Ctx 를 다른 --pipe 로(add1 전 판 흉내 · 정본) 쓰는 얕은 사본"""
    def __init__(self, base, pipe):
        self.__dict__.update(base.__dict__)
        self.pipe = os.path.abspath(pipe)
        self.consts = load_consts(self.pipe)


# ───────────────────────────────────────── 안전 대조(시험 앞뒤)
def snapshot(ctx):
    s = {}
    nj = _roots.n('jopangi')
    s['N jo_pipe.py md5'] = md5(os.path.join(nj, 'jo_pipe.py'))
    s['N python_setup.cmd md5'] = md5(_roots.n('python_setup.cmd'))
    pdir = os.path.join(nj, '공통', '_pipeline')
    ent = sorted((f, os.path.getsize(os.path.join(pdir, f)), int(os.path.getmtime(os.path.join(pdir, f)))) for f in os.listdir(pdir) if os.path.isfile(os.path.join(pdir, f)))
    s['N _pipeline 파일(이름·크기·시각)'] = hashlib.md5(json.dumps(ent).encode()).hexdigest()
    s['N _pipeline\\_runs 있나'] = os.path.isdir(os.path.join(pdir, '_runs'))
    for f in ('_last_run.md', 'hashlog.json', 'ids_last.json', 'inputs_last.json', 'hsul_last.json'):
        s['N ' + f + ' md5'] = md5(os.path.join(pdir, f))
    s['전역 pip list'] = hashlib.md5(json.dumps(pip_json(ctx.py)).encode()).hexdigest()
    ap = os.path.join(os.environ.get('APPDATA', ''), 'Python')
    s['진짜 %APPDATA%\\Python 목록'] = hashlib.md5(json.dumps(sorted(os.listdir(ap)) if os.path.isdir(ap) else None).encode()).hexdigest()
    return s


# ───────────────────────────────────────── 본체
ORDER = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10', 'X11', 'X12', 'X13', 'X14', 'X15', 'X16', 'X17', 'X18', 'X19', 'X20', 'X21', 'X22', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'R1', 'L']
FUNCS = {k: globals()['sc_' + k] for k in ORDER if k not in ('B9', 'L')}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pipe', required=True)
    ap.add_argument('--expect', choices=('new', 'base'), default='new')
    ap.add_argument('--only', default='')
    ap.add_argument('--work', default='')
    ap.add_argument('--keep', action='store_true')
    ap.add_argument('--src', default='')
    ap.add_argument('--wheelhouse', default='')
    ap.add_argument('--base-pipe', default='')
    ap.add_argument('--json', default='')
    ap.add_argument('--no-venv', action='store_true')
    ap.add_argument('--bait', choices=('new', 'old'), default='new')
    a = ap.parse_args()
    ctx = Ctx(a)
    need_files = [ctx.consts['P7PDF']] + list(ctx.consts['BLANKPDFS'])
    lost = [p for p in need_files if not os.path.exists(p)]
    if lost:                                   # jo_pipe 의 exist_gate 가 N: 절대 경로 재료를 본다 — 없으면 시험이 의미 없다
        print('ENV: N: 재료가 이 PC 에 없다 — 시험 못 함: %s' % lost)
        return 3
    only = [x.strip() for x in a.only.split(',') if x.strip()] or ORDER
    print('=== jo_pipe_push 하네스 · 시험 대상 %s · md5 %s · 기대 %s ===' % (ctx.pipe, md5(ctx.pipe), a.expect))
    print('    work = %s · src = %s · python = %s' % (ctx.work, ctx.src, ctx.py))
    before = snapshot(ctx)
    items, results, t0 = [], {}, time.time()
    for k in ORDER:
        if k not in only:
            continue
        t1 = time.time()
        try:
            if k == 'B9':
                it, rr = sc_B9(ctx, results)
                items.append(it)
            elif k == 'L':
                if a.no_venv or a.expect == 'base':   # 라이브러리 묶음은 새 판에만(바탕 = 정본에는 라이브러리 단계가 없다)
                    continue
                vpy = make_venv(ctx, 'venv_nopdf')
                for it, rr in sc_L(ctx, vpy, a.base_pipe):
                    items.append(it)
                    print_item(it, time.time() - t1)
                continue
            else:
                it, rr = FUNCS[k](ctx)
                results[k] = rr
                items.append(it)
        except Exception as e:
            import traceback
            it = Item(k, '시험이 죽었다')
            it.chk('core', '예외 없이 끝남', False, traceback.format_exc()[-900:])
            items.append(it)
        print_item(items[-1], time.time() - t1)
    after = snapshot(ctx)
    safe = Item('SAFE', '시험이 진짜를 안 건드렸다(N: 정본 · N: 상태 파일 · 본 genie 클론 · 전역 pip · 진짜 사용자 자리) — 시험 앞뒤 대조')
    for k in before:
        safe.chk('core', k, before[k] == after[k], 'same' if before[k] == after[k] else '%r → %r' % (before[k], after[k]))
    print_item(safe, 0)
    items.append(safe)
    # 진짜 본 genie 클론은 다른 세션이 쓰는 중이라 앞뒤 대조를 단정하지 않는다 — 이 하네스는 그 자리에 git 명령을 한 번도 안 쓴다(G() 가 샌드박스 밖을 assert 로 막는다)
    gm = os.path.join(_roots.DEFAULT['GENIE_ROOT'], '.git')
    print('\n[참고] 본 genie 클론 .git/HEAD = %r (이 하네스는 그 자리에 git 명령을 쓰지 않는다 · 다른 세션이 쓰는 중이라 값은 단정하지 않는다)' % (
        open(os.path.join(gm, 'HEAD'), encoding='utf-8', errors='replace').read().strip() if os.path.isfile(os.path.join(gm, 'HEAD')) else None))
    if not a.keep:
        for n in os.listdir(ctx.work):
            p = os.path.join(ctx.work, n)
            if os.path.isdir(p):
                rm_rf(p)
    n_ok = sum(1 for i in items if i.ok)
    print('\n=== 요약: %d / %d 칸 PASS · %.0f초 ===' % (n_ok, len(items), time.time() - t0))
    if a.json:
        json.dump([{'id': i.id, 'name': i.name, 'ok': i.ok, 'core_ok': i.core_ok, 'vals': i.vals,
                    'checks': [{'grp': c[0], 'desc': c[1], 'ok': c[2], 'detail': c[3]} for c in i.checks]} for i in items],
                  open(a.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if a.expect == 'new':
        return 0 if n_ok == len(items) else 1
    bait_ids = NEW_BAIT if a.bait == 'new' else OLD_BAIT
    bait = [i for i in items if i.id in bait_ids]
    stood = [i for i in bait if not i.core_ok]
    print('=== 헛잣대(%s): %s 가 FAIL 로 섰나 → %s ===' % ('조이기 Y · 바탕 = 조이기 전 정본' if a.bait == 'new' else 'B-10 · 바탕 = push 판 전', ' · '.join(bait_ids),
                                                    ', '.join('%s %s' % (i.id, 'FAIL(섰다)' if not i.core_ok else 'PASS(안 섬)') for i in bait)))
    olds = [i for i in items if i.id not in bait_ids and i.id != 'SAFE']
    print('=== 옛 칸(바탕에서도 전처럼 · 헛잣대 아님): %d 칸 중 PASS %d%s ===' % (len(olds), sum(1 for i in olds if i.ok),
                                                                    '' if all(i.ok for i in olds) else ' · FAIL: ' + ', '.join(i.id for i in olds if not i.ok)))
    return 0 if len(stood) == len(bait_ids) and len(bait) == len(bait_ids) else 1


def print_item(it, secs):
    print('\n[%s] %s %s — %.0f초' % ('PASS' if it.ok else 'FAIL', it.id, it.name, secs))
    for grp, desc, ok, detail in it.checks:
        print('    %s %-4s %s%s' % ('ok  ' if ok else 'FAIL', grp, desc, (' — ' + str(detail)) if detail else ''))
    if it.vals:
        print('    값: ' + json.dumps(it.vals, ensure_ascii=False))
    sys.stdout.flush()


if __name__ == '__main__':
    sys.exit(main())
