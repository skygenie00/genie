# -*- coding: utf-8 -*-
"""_qa_chain — 하네스 사슬 실행기 · 저장본(바탕 결과) · 값으로 맞대기 · 흔들림 (_task_qa_baseline 2026-09-30 A-1~A-5)

  python _qa_chain.py census [--write]      N: 정본 하네스(_qa_sync.harnesses) ↔ 전수표(_qa_chain_list.json) 줄 — 빠진 것 · 없어진 것
                                            --write = 빠진 줄을 기본값(태그 「미분류」)으로 더한다 — 태그 · 무엇 · 인자 꼴은 사람이 채운다
  python _qa_chain.py check                 전수표 검사 — 줄 수 = 하네스 수(앱마다) · 무엇 · 태그 · 입력 빈칸 0 · 어긋나면 종료 코드 1
  python _qa_chain.py run <앱> [--scope 태그,…] [--only 이름,…] [--rev <커밋> | --root <genie 자리>] [--label 이름] [--reuse]
        그 앱 사슬(전수표 chains 에 그 앱이 든 하네스 · 태그로 거름)을 차례로 돌린다 — 겹쳐 돌리지 않는다(잠금 파일)
        --rev  = genie 그 커밋을 분리 워크트리(<genie>\\.claude\\worktrees\\qa_<커밋7>)로 꺼내 그 자리에서(⚙ 가 본 폴더를 바꿔도 안 흔들림)
        --root = 그 자리 그대로(줄 워크트리 · 안 커밋한 고침 포함) · 둘 다 없으면 GENIE_ROOT(없으면 본 폴더) 그대로
        --reuse = 같은 열쇠 저장본이 있으면 안 돌린다 · --label = 같은 열쇠가 있어도 <열쇠>@<label>.json 으로 따로 둔다(되풀이 잣대)
  python _qa_chain.py compare <앱> [--scope …] [--only …] [--rev <새 커밋> | --root <새 판 자리>] [--base <바탕 커밋 = main>] [--no-flaky]
        규칙 (57) 회귀 — 하네스마다 바탕 열쇠 저장본과 새 판 결과를 값으로 맞댄다(A-4) · 저장본이 없거나 입력이 바뀐 하네스만 바탕에서 돌린다(A-3)
        · 새 판 열쇠 = 바탕 열쇠(입력 같음)면 새 판에서도 안 돌린다 · 새 FAIL · FAIL 값 바뀜이 나온 하네스만 한 번 더(A-5 흔들림)
  python _qa_chain.py plan <앱> [--scope …] [--only …] [--rev|--root …] [--base …]   compare 가 무엇을 돌릴지만(안 돌림)
  python _qa_chain.py show <앱> [--scope …] [--rev|--root …]                          그 판 열쇠의 저장본 요약
  python _qa_chain.py diff <앱> <실행 기록 A> <실행 기록 B>                            두 실행 기록(_qa_results\\<앱>\\_runs\\*.json)을 항목 값으로 맞댄다
  python _qa_chain.py reparse <앱>                                                    저장본 원문을 지금 받개로 다시 읽는다(받개를 고친 뒤)
  앱 = jo(조판기) · jagwa(자과) · minbeop(민법) · timetable(시간표) · gichul(기출서재) · chem(화학) · root(맨 위 공용 도구)

  열쇠(A-3) = 하네스 파일 md5 + 인자 꼴 + 읽는 입력(전수표 inputs — genie 파일 blob · 폴더 = 그 아래 blob 목록 · N:·기록 파일 md5) 해시 + 브라우저 판
  입력은 짐작하지 않는다 — 돌릴 때 _qa_trace\\sitecustomize.py 가 하네스(와 하위 파이썬)가 연 파일을 적고, 실행기가 전수표 inputs 에 더한다.
  하네스가 N:·genie·기록 자리에 쓴 파일은 추적 장치가 먼저 떠 두고 실행기가 하네스가 끝나면 되돌린다(새로 만든 것은 지운다) — 결과 파일은 먼저 건진다.
  저장본 = N:\\개인\\claude\\_qa_results\\<앱>\\<열쇠>.json(N: 에만 · genie _qa 에 안 올림 — 값에 사용자 기록이 섞일 수 있다)
  흔들림 = N:\\개인\\claude\\_qa_flaky.json · N: 이 없으면(클라우드) 저장본은 %TEMP%\\qa_chain\\results 에 두고 N: 입력 하네스는 「N: 필요」로 건넌다(A-7-4).
"""
import fnmatch
import os as _os_r, sys as _sys_r   # env_lanes — _roots.py 를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import ctypes
import glob
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))          # N:\개인\claude 또는 genie\_qa
NR = _roots.n_root()                                        # N: 작업 폴더(없으면 None — 클라우드)
# 관문 모래상자(_harness_qa_baseline)는 아래 넷을 환경으로 바꿔 N: 저장본을 안 건드린다
LIST = os.environ.get('QA_CHAIN_LIST') or os.path.join(HERE, '_qa_chain_list.json')
HHOME = os.environ.get('QA_CHAIN_HHOME') or HERE                     # 전수표 file 칸의 기준 자리
TRACE_DIR = os.path.join(HERE, '_qa_trace')
WORK = os.environ.get('QA_CHAIN_WORK') or os.path.join(tempfile.gettempdir(), 'qa_chain')   # ★ env_clean B-3(10/8) — 무리마다 실행기 자리(잠금 · 실행 결과)를 TEMP 사본 없이 가름 · 옛 줄: WORK = os.path.join(tempfile.gettempdir(), 'qa_chain')
# ★ env_clean B-1 · B-2(10/8) — 하네스마다 임시 폴더 %TEMP%\pa_qa\<실행 id>\<하네스>_<시각>(TEMP · TMP · TMPDIR) · 끝나면 지움 · 실행 시작에 죽은 실행 몫 쓸기
#   까닭: 하네스의 tempfile · 크롬 · playwright 프로필 · 앱 사본이 %TEMP% 바로 밑에 쌓여 C: 가 찼다(10/8 14:38 여유 0.38 GB · 회귀가 Errno 28 로 죽음)
BASE_TEMP = tempfile.gettempdir()
PA = os.environ.get('QA_CHAIN_PA') or os.path.join(BASE_TEMP, 'pa_qa')
RUN_ID = time.strftime('%Y%m%d-%H%M%S') + '_p%d' % os.getpid()
PA_SEED = (('h_gichul', 'vendor'), ('h_jagwa', 'vendor'))   # 하네스가 TEMP 에서 찾는 pdf.js 사본 — 있으면 하네스 임시 폴더에 떠 줌(없으면 하네스가 받거나 cdnjs)
# ★ _task_qa_fix1 A-5(10/9) — 씨앗을 뜨는 자리를 TEMP 밖 공용 사본으로(하네스 쪽 자리 · PA_SEED 상대 꼴은 그대로 · 옛 줄 = 위 PA_SEED 줄과 pa_make 의 「# 옛 줄」)
#   까닭: 윈도 저장소 센스(켜 둠 · 사용자 10/9 18:27)가 C: 가 찰 때 %TEMP% 를 지우며 h_gichul\vendor 도 지운 것으로 보임(10/8 14:33 jo_cvfind 「pdfjsLib is not defined」 · 9/23 · 10/1 같은 꼴 · 짐작)
#   공용 사본 = %LOCALAPPDATA%\pa_qa\vendor\<PA_SEED 상대 꼴>(QA_CHAIN_VENDOR 로 바꿈) · 실행 시작(run · compare · run_one 을 바로 부르는 드라이버는 첫 pa_make)에 vendor_check:
#   받는 씨앗(PA_GET = h_gichul\vendor 의 pdf.js 둘)은 없음 · 크기 · md5 다름(깨짐 · 판 다름)이면 cdnjs 3.11.174 에서 받아 채움 → 받기 실패면 옛 자리(%TEMP%\h_gichul\vendor)가 성하면 그것(사본 자리에도 떠 둠)
#   → 둘 다 없으면 실행 첫 줄에 경고 한 줄(하네스는 그대로 돎) · 그 밖 씨앗(h_jagwa\vendor)은 자리만 — 사본 자리에 있으면 그것 · 없으면 옛 자리(받지 않음 · 자과 하네스는 없으면 진짜 cdnjs)
PA_VENDOR = os.environ.get('QA_CHAIN_VENDOR') or os.path.join(os.environ.get('LOCALAPPDATA') or os.path.expanduser('~'), 'pa_qa', 'vendor')
PDFJS = ('3.11.174', {'pdf.min.js': (320004, '96de323330f8b8336f637a0051835e00'),        # cdnjs 3.11.174 바이트(10/9 19:5x 받아 잼 = 10/8 19:40 손 채움 사본과 같음)
                      'pdf.worker.min.js': (1087212, 'a53a71a2a5d618ed0f86ebf099db032a')})
PDFJS_URL = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/%s/%s'
PA_GET = {('h_gichul', 'vendor'): PDFJS}   # 받아 채우는 씨앗 — 그 밖 PA_SEED 는 자리만
PA_SRC = {}   # 씨앗 → 이 실행에서 떠 줄 자리(vendor_check 가 정함 · None = 성한 사본 없음)
PA_LEFT = []
RESD = os.environ.get('QA_CHAIN_RES') or (os.path.join(NR, '_qa_results') if NR else os.path.join(WORK, 'results'))
FLAKY = os.environ.get('QA_CHAIN_FLAKY') or (os.path.join(NR, '_qa_flaky.json') if NR else os.path.join(WORK, '_qa_flaky.json'))
APPS = {'jo': '조판기', 'jagwa': '자과', 'minbeop': '민법', 'timetable': '시간표', 'gichul': '기출서재', 'chem': '화학', 'root': '맨 위 공용'}
FOLDER_APP = {'jopangi': 'jo', 'jagwa': 'jagwa', 'minbeop': 'minbeop', 'timetable': 'timetable', '기출서재': 'gichul', 'chem': 'chem'}
APP_FILE = {'jo': 'jo/index.html', 'jagwa': 'jagwa/index.html', 'minbeop': 'minbeop/index.html', 'timetable': 'timetable/index.html',
            'gichul': 'gichul/index.html', 'chem': 'chem/index.html'}
ST = ('PASS', 'FAIL', 'INFO', 'WARN', 'SKIP')


def say(*a):
    print(*a, flush=True)


# ── N: 안전 쓰기(마이박스 — 잇달아 쓰면 이웃 파일 내용으로 바뀐 일이 있다 · 쓰고 0.5초 뒤 되읽어 대조) ──────────────
def nwrite(path, data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for _ in range(4):
        with open(path, 'wb') as f:
            f.write(data)
        time.sleep(0.5)
        with open(path, 'rb') as f:
            if f.read() == data:
                return
    raise SystemExit('NG 쓰기 확인 실패(되읽은 바이트가 다름): %s' % path)


def jload(path, default=None):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def jdump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1) + '\n'


# ── 전수표 ─────────────────────────────────────────────────────────────────────────────────────
def census_load():
    c = jload(LIST)
    if c is None:
        raise SystemExit('전수표 없음: %s' % LIST)
    return c


def census_save(c):
    c['rows'].sort(key=lambda r: (r['app'], r['file']))
    nwrite(LIST, jdump(c))


def n_harnesses():
    """N: 정본 하네스(_qa_sync 와 같은 모음) — N: 기준 상대 경로(/)"""
    if not NR:
        return None
    sys.path.insert(0, NR)
    import _qa_sync
    return sorted(os.path.relpath(p, NR).replace(os.sep, '/') for p in _qa_sync.harnesses())


def app_of(rel):
    top = rel.split('/')[0] if '/' in rel else ''
    return FOLDER_APP.get(top, 'root')


def row_by_name(c):
    return {os.path.basename(r['file'])[:-3].replace('_harness_', ''): r for r in c['rows']}


def rname(r):
    return os.path.basename(r['file'])[:-3].replace('_harness_', '')


def rows_for(c, app, scope=None, only=None):
    out = []
    for r in c['rows']:
        if app not in (r.get('chains') or [r['app']]):
            continue
        if only and rname(r) not in only:
            continue
        if scope and 'all' not in scope and not (set(scope) & set(r.get('tags') or [])):
            continue
        out.append(r)
    return out


# ── 해시 · 열쇠 ─────────────────────────────────────────────────────────────────────────────────
_HC = None


def _hcache():
    global _HC
    if _HC is None:
        _HC = jload(os.path.join(WORK, 'hcache.json'), {}) or {}
    return _HC


def _hcache_save():
    if _HC is not None:
        os.makedirs(WORK, exist_ok=True)
        with open(os.path.join(WORK, 'hcache.json'), 'w', encoding='utf-8') as f:
            json.dump(_HC, f)


def fmd5(p):
    """파일 md5(크기 · 고친 시각으로 캐시) — 없으면 'missing'"""
    try:
        st = os.stat(p)
    except OSError:
        return 'missing'
    if os.path.isdir(p):
        return 'dir'
    hc = _hcache()
    k = os.path.normcase(os.path.abspath(p))
    sig = '%d:%d' % (st.st_size, st.st_mtime_ns)
    v = hc.get(k)
    if v and v[0] == sig:
        return v[1]
    h = hashlib.md5()
    try:
        with open(p, 'rb') as f:
            for b in iter(lambda: f.read(1 << 20), b''):
                h.update(b)
    except OSError as e:   # 마이박스 자리표 · 잠긴 파일 — 열쇠 재기에서 죽지 않는다(그 칸 = unreadable · 다음에 다시 읽힘)
        return 'unreadable:%s' % getattr(e, 'errno', '')
    hc[k] = [sig, h.hexdigest()]
    return h.hexdigest()


def git(repo, *a, check=True):
    r = subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True)
    if check and r.returncode:
        raise SystemExit('NG git %s: %s' % (' '.join(a), r.stderr.decode('utf-8', 'replace')[:300]))
    return r.stdout.decode('utf-8', 'replace')


class Ctx:
    """한 판(genie) — 입력 해시를 낸다.
       rev 판(--rev · --base) = 커밋만 쥐고 열쇠는 git 객체(ls-tree)로 잰다 · 하네스를 돌릴 때만 분리 워크트리(qa_<커밋7>)를 꺼낸다(ensure)
       · 이 실행이 만든 워크트리만 지운다(drop) — 다른 실행이 쓰는 워크트리를 지우지 않게
       root 판(--root · GENIE_ROOT) = 그 자리 그대로(안 커밋한 고침은 hash-object 로)"""

    def __init__(self, root=None, rev=None, label=''):
        self.label = label
        self.created = False
        self._tree = None
        self._dirty = None
        if root:
            self.root = os.path.abspath(root)
            self.repo = self.root
            self.rev = False
            self.head = git(self.root, 'rev-parse', 'HEAD').strip()
        else:
            self.repo = main_clone()
            self.head = git(self.repo, 'rev-parse', '--verify', rev + '^{commit}').strip()
            self.rev = True
            self.root = None

    @property
    def owned(self):
        """실행기 몫 워크트리(qa_<커밋7>) — 하네스가 바꾸면 되돌려도 된다"""
        return self.rev

    def ensure(self):
        if self.root is None:
            wt = os.path.join(self.repo, '.claude', 'worktrees', 'qa_' + self.head[:7])
            if os.path.isdir(wt):
                if git(wt, 'rev-parse', 'HEAD', check=False).strip() != self.head:
                    raise SystemExit('NG %s 가 있는데 HEAD 가 %s 가 아님 — 손으로 보고 지울 것' % (wt, self.head[:7]))
                if git(wt, 'status', '--porcelain', '--untracked-files=all').strip():
                    reset_wt(wt)
            else:
                say('워크트리 만듦: %s (%s)' % (wt, self.head[:7]))
                git(self.repo, 'worktree', 'add', '--detach', wt, self.head)
                self.created = True
            self.root = wt
        return self.root

    def drop(self):
        if self.created and self.root:
            git(self.repo, 'worktree', 'remove', '--force', self.root, check=False)
            self.created = False
            self.root = None

    def tree(self):
        if self._tree is None:
            t = {}
            for ent in git(self.repo, 'ls-tree', '-r', '-z', self.head).split('\0'):
                if '\t' in ent:
                    meta, p = ent.split('\t', 1)
                    t[p] = meta.split()[2]
            self._tree = t
            self._dirty = {}
            if not self.rev:
                st = git(self.root, 'status', '--porcelain', '-z', '--untracked-files=all')
                for ent in [x for x in st.split('\0') if x]:
                    if re.match(r'^[ MADRCU?!]{2} ', ent) and ent[:2].strip():
                        self._dirty[ent[3:]] = ent[:2]
        return self._tree

    def blob(self, p):
        t = self.tree()
        if p in self._dirty:
            fp = os.path.join(self.root, *p.split('/'))
            if not os.path.exists(fp):
                return 'missing'
            return git(self.root, 'hash-object', '--', p).strip()
        return t.get(p, 'missing')

    def dirhash(self, d):
        t = self.tree()
        pre = d.rstrip('/') + '/'
        ks = sorted(set([k for k in t if k.startswith(pre)] + [k for k in self._dirty if k.startswith(pre)]))
        h = hashlib.sha1()
        for k in ks:
            h.update(('%s %s\n' % (k, self.blob(k))).encode('utf-8'))
        return '%d:%s' % (len(ks), h.hexdigest()[:16])

    def dirty(self):
        self.tree()
        return dict(self._dirty)


def other_root(name):
    if name == 'n':
        return NR
    if name == 'spd':
        return _roots.root('SPD_ROOT')
    if name == 'mbpdf':
        return _roots.root('MBPDF_ROOT')
    if name == 'lad':
        return os.path.join(os.environ.get('LOCALAPPDATA') or '', 'jopangi')   # ⚙ 로컬 산출(_out) — 임시 폴더·파이썬 설치는 자리 밖
    if name == 'vault':   # 옵시디언 볼트(jo_common 과 같은 자리 · ⚙ 재료) — 볼트 노트를 읽는 하네스의 열쇠에 든다
        return os.environ.get('JOPANGI_VAULT') or os.path.join(os.path.expanduser('~'), 'Documents', "PA's archive")
    return None


def in_hash(pat, ctx):
    """입력 한 줄의 해시 — 'genie:jo/index.html' · 'genie:jo/data/**' · 'genie:@HEAD' · 'n:…' · 'spd:…' · 'mbpdf:…' · 'lad:…' · 'vault:…' · 'net:…'"""
    r, _, p = pat.partition(':')
    if r == 'genie':
        if p == '@HEAD':
            return ctx.head
        if p.endswith('/**'):
            return ctx.dirhash(p[:-3])
        return ctx.blob(p)
    if r == 'net':
        return 'net'
    base = other_root(r)
    if not base:
        return 'no-root'
    fp = os.path.join(base, *p[:-3].split('/')) if p.endswith('/**') else os.path.join(base, *p.split('/'))
    if p.endswith('/**'):
        if not os.path.isdir(fp):
            return 'missing'
        h = hashlib.sha1()
        n = 0
        for dp, dns, fns in os.walk(fp, onerror=lambda e: None):
            dns.sort()
            for fn in sorted(fns):
                q = os.path.join(dp, fn)
                h.update(('%s %s\n' % (os.path.relpath(q, fp).replace(os.sep, '/'), fmd5(q))).encode('utf-8'))
                n += 1
        return '%d:%s' % (n, h.hexdigest()[:16])
    return fmd5(fp)


_BR = {}


def browser(engs):
    """브라우저 판 — 쓰는 엔진 것만(크롬이 올라도 playwright 하네스 열쇠는 그대로)"""
    out = {}
    engs = set(engs or [])
    if engs & {'chromium', 'webkit', 'firefox'}:
        if 'pw' not in _BR:
            try:
                from importlib.metadata import version
                v = version('playwright')
            except Exception:
                v = '?'
            d = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'ms-playwright')
            dirs = sorted(x for x in (os.listdir(d) if os.path.isdir(d) else []) if x.split('-')[0] in ('chromium', 'webkit', 'firefox'))
            _BR['pw'] = v + ' ' + ' '.join(dirs)
        out['pw'] = _BR['pw']
    if 'chrome' in engs:
        if 'chrome' not in _BR:
            exe = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
            v = '?'
            if os.path.exists(exe):
                r = subprocess.run(['powershell', '-NoProfile', '-Command', "(Get-Item '%s').VersionInfo.ProductVersion" % exe], capture_output=True, text=True)
                v = (r.stdout or '?').strip()
            _BR['chrome'] = v
        out['chrome'] = _BR['chrome']
    return out


def hfile(r):
    return os.path.join(HHOME, *r['file'].split('/'))


def argv_tpl(r, app):
    a = r.get('argv') or {}
    return a.get(app, a.get('*', []))


# ── 실행 모드(_task_qa_slim A-1 · 10/4) ───────────────────────────────────────────────────────────
# 전수표 줄에 modes 칸이 있는 jo 하네스만 — argv 의 「{mode}」 자리가 gate 면 빈 것(이 판 앞과 같은 argv) ·
# regress · smoke 면 --mode <m> --snap-out <out>\snap.json [--snap-in <바탕 저장본 옆 .base.json>].
# modes 칸이 없는 줄(다른 앱 · 아직 안 고친 하네스)은 열쇠 · argv 가 이 판 앞과 같다(§B-7).
# ★ _task_qa_slim2 A-1-1(10/8) — 자과 · 민법 · 시간표도 같은 모드 갈래(그 앱 줄도 modes 칸을 단 것만 · 안 단 줄은 옛 꼴 그대로)
# 옛 줄: MODE_APPS = ('jo',)
MODE_APPS = ('jo', 'jagwa', 'minbeop', 'timetable')


def mode_of(r, app, ctx):
    ms = r.get('modes') or []
    if app not in MODE_APPS or not ms:
        return None
    if '{mode}' not in argv_tpl(r, app):   # ★ _task_qa_slim2(10/8) — 그 사슬 argv 에 {mode} 자리가 없으면 모드 없음(옛 꼴) · 사슬마다 들인 때가 다른 하네스(exam_wrong_mark = jo 만 {mode}) · jo 줄 52 는 다 {mode} 있음(무변)
        return None
    m = getattr(ctx, 'mode', None) or ('regress' if 'regress' in ms else 'gate')
    if m == 'smoke' and 'smoke' not in ms:
        return 'regress' if 'regress' in ms else 'gate'
    return m if m in ms else 'gate'


def snap_path(app, key):
    return os.path.join(RESD, app, '%s.base.json' % key)


def key_of(r, app, ctx, snap=None):
    # key_skip = 열쇠에서 뺄 입력 꼴(fnmatch · 전수표 줄 칸) — 판정에 안 쓰이는 INFO 셈만 읽는 파일(gaek_uid C8: N: md 전부 · 볼트 전부 — 결정로그 한 줄에도 열쇠가 바뀌었다 · 10/1)
    skip = r.get('key_skip') or []
    ins = [p for p in sorted(r.get('inputs') or []) if not any(fnmatch.fnmatchcase(p, s) for s in skip)]
    parts = {'h': fmd5(hfile(r)), 'argv': argv_tpl(r, app), 'br': browser(r.get('eng')),
             'in': {p: in_hash(p, ctx) for p in ins}}
    if skip:
        parts['skip'] = skip
    m = mode_of(r, app, ctx)
    if m:
        parts['mode'] = m                    # A-1-3 — gate 결과와 regress 결과가 섞이지 않게
        if snap and m != 'gate' and os.path.isfile(snap):
            parts['snap'] = fmd5(snap)       # 기준 칸 판정이 맞댄 바탕 스냅샷
    k = hashlib.sha1(json.dumps(parts, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()[:16]
    return k, parts


def res_path(app, key, label=''):
    return os.path.join(RESD, app, '%s%s.json' % (key, ('@' + label) if label else ''))


# ── 판 자리(워크트리) ───────────────────────────────────────────────────────────────────────────
def main_clone():
    g = _roots.root('GENIE_ROOT')
    common = git(g, 'rev-parse', '--path-format=absolute', '--git-common-dir').strip()
    return os.path.dirname(common)


def reset_wt(wt):
    git(wt, 'checkout', '--', '.', check=False)
    git(wt, 'clean', '-fdq', check=False)


def ctx_from(args, which='new'):
    if which == 'base':
        return Ctx(rev=args.get('--base') or 'main', label='base')
    if args.get('--rev'):
        return Ctx(rev=args['--rev'], label='rev')
    return Ctx(root=args.get('--root') or _roots.root('GENIE_ROOT'), label='root')


# ── 잠금(사슬 둘을 겹쳐 돌리지 않는다) ────────────────────────────────────────────────────────────
def _alive(pid):
    if os.name != 'nt':
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    k = ctypes.windll.kernel32
    h = k.OpenProcess(0x1000, False, pid)
    if not h:
        return False
    code = ctypes.c_ulong()
    k.GetExitCodeProcess(h, ctypes.byref(code))
    k.CloseHandle(h)
    return code.value == 259


def lock():
    os.makedirs(WORK, exist_ok=True)
    lf = os.path.join(WORK, 'lock.json')
    old = jload(lf)
    if old and old.get('pid') != os.getpid() and _alive(old.get('pid', 0)):
        raise SystemExit('NG 다른 사슬이 돈다(pid %s · %s · %s) — 겹쳐 돌리지 않는다' % (old['pid'], old.get('when'), old.get('cmd')))
    with open(lf, 'w', encoding='utf-8') as f:
        json.dump({'pid': os.getpid(), 'when': time.strftime('%Y-%m-%d %H:%M:%S'), 'cmd': ' '.join(sys.argv[1:])}, f, ensure_ascii=False)
    return lf


# ── env_clean B-1 · B-2 · B-5(10/8) — 하네스 임시 폴더 · 쓸기 · 실행 결과 폴더 셋만 ──────────────────────────────
def _rm_ro(fn, p, exc):
    try:
        os.chmod(p, 0o666)
        fn(p)
    except Exception:
        pass


def pa_make(name, stamp):
    """하네스 하나의 임시 폴더 — 씨앗(pdf.js 사본)을 떠 둠"""
    d = os.path.join(PA, RUN_ID, '%s_%s' % (name, stamp))
    os.makedirs(d, exist_ok=True)
    if not PA_SRC:
        vendor_check()   # ★ _task_qa_fix1 A-5 — run_one 을 바로 부르는 드라이버(cmd_run · cmd_compare 밖)도 첫 하네스 앞에서 한 번
    for sub in PA_SEED:
        # 옛 줄: src = os.path.join(BASE_TEMP, *sub)
        src = PA_SRC.get(sub, os.path.join(BASE_TEMP, *sub))   # ★ _task_qa_fix1 A-5 — 공용 사본(%LOCALAPPDATA%\pa_qa\vendor) · 받기 실패면 옛 자리 · 성한 것 없으면 None(안 뜸 = 옛 꼴의 「없으면」)
        if src and os.path.isdir(src):
            try:
                shutil.copytree(src, os.path.join(d, *sub), dirs_exist_ok=True)
            except Exception:
                pass
    return d


def _vend_file_ok(p, size, md5):
    try:
        if os.path.getsize(p) != size:
            return False
        with open(p, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest() == md5
    except OSError:
        return False


def _vend_ok(d, files):
    """★ _task_qa_fix1 A-5 — 사본 폴더 d 의 파일이 그 판 바이트인가(없음 · 크기 0 · 크기 · md5 다름 = 깨짐 · 판 다름 = 아님)"""
    return bool(d) and os.path.isdir(d) and all(_vend_file_ok(os.path.join(d, f), sz, md) for f, (sz, md) in files.items())


def _vend_put(d, f, data):
    """d\\f 에 바꿔 넣기 — 임시 이름(공용 사본 밑 _dl · 씨앗 폴더 밖)에 쓰고 os.replace(반쯤 쓴 파일이 씨앗 폴더에 안 남게 · 다른 실행이 같이 넣어도 하나만 이김)"""
    os.makedirs(d, exist_ok=True)
    tmpd = os.path.join(PA_VENDOR, '_dl')
    os.makedirs(tmpd, exist_ok=True)
    tmp = os.path.join(tmpd, '%s.%d.part' % (f, os.getpid()))
    with open(tmp, 'wb') as fh:
        fh.write(data)
    try:
        os.replace(tmp, os.path.join(d, f))
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass


def _vend_get(d, ver, files):
    """cdnjs 에서 받아 d 에 채움(이미 성한 파일은 둠 · 받은 바이트의 크기 · md5 를 맞춘 뒤에만 넣음) — 실패 까닭(없으면 None)"""
    import urllib.request
    for f, (sz, md) in files.items():
        if _vend_file_ok(os.path.join(d, f), sz, md):
            continue
        try:
            data = urllib.request.urlopen(PDFJS_URL % (ver, f), timeout=60).read()
        except Exception as e:
            return '%s 받기 %s' % (f, str(e)[:80])
        if len(data) != sz or hashlib.md5(data).hexdigest() != md:
            return '%s 받은 바이트가 %s 판과 다름(%d B · md5 %s)' % (f, ver, len(data), hashlib.md5(data).hexdigest()[:8])
        try:
            _vend_put(d, f, data)
        except OSError as e:
            if not _vend_file_ok(os.path.join(d, f), sz, md):   # 다른 실행이 같은 때 넣었으면 성한 것이 이미 있다
                return '%s 넣기 %s' % (f, str(e)[:80])
    return None


def vendor_check():
    """★ _task_qa_fix1 A-5 — 실행 시작에 씨앗마다 떠 줄 자리를 정한다(PA_SRC) · 받는 씨앗은 없음 · 깨짐이면 cdnjs 에서 받아 채움 · 성한 것이 없으면 경고 한 줄"""
    warn = []
    for sub in PA_SEED:
        home = os.path.join(PA_VENDOR, *sub)
        old = os.path.join(BASE_TEMP, *sub)
        get = PA_GET.get(sub)
        if not get:   # 자리만(h_jagwa\vendor) — 사본 자리에 무엇이 있으면 그것 · 없으면 옛 자리(옛 꼴 그대로)
            try:
                PA_SRC[sub] = home if os.path.isdir(home) and os.listdir(home) else old
            except OSError:
                PA_SRC[sub] = old
            continue
        ver, files = get
        if _vend_ok(home, files):
            PA_SRC[sub] = home
            continue
        try:
            why = _vend_get(home, ver, files)
        except Exception as e:
            why = '받기 %s' % str(e)[:80]
        if why is None and _vend_ok(home, files):
            say('  pdf.js 사본 받아 채움(cdnjs %s → %s)' % (ver, home))
            PA_SRC[sub] = home
            continue
        if _vend_ok(old, files):
            try:   # 옛 자리가 성하면 공용 사본 자리에도 떠 둠(다음 실행부터 TEMP 가 지워져도 됨)
                for f in files:
                    with open(os.path.join(old, f), 'rb') as fh:
                        _vend_put(home, f, fh.read())
            except Exception:
                pass
            PA_SRC[sub] = home if _vend_ok(home, files) else old
            say('  ⚠ pdf.js 사본: cdnjs 받기 실패(%s) → 옛 자리 %s 를 씀' % (why, old))
            continue
        PA_SRC[sub] = None
        warn.append('%s 없음 · 깨짐(받기 실패: %s · 옛 자리 %s 도 없음 · 깨짐)' % (home, why, old))
    if warn:
        say('⚠ pdf.js 사본 없음 — %s · 하네스는 그대로 돎(pdf.js 쓰는 하네스는 「pdfjsLib 없음」 으로 FAIL 날 수 있음 · cdnjs %s 손 채움 = CLAUDE.md 「무더기 FAIL 은 환경부터」)'
            % (' / '.join(warn), PDFJS[0]))
    return warn


def pa_drop(d, keep, out):
    """하네스 임시 폴더 지움 — 전수표 keep 칸(그 폴더 기준 상대 이름)은 out\\kept 로 옮긴 뒤 · 못 지운 것은 다음 실행 쓸기 몫"""
    for k in keep or []:
        src = os.path.join(d, *k.split('/'))
        if os.path.exists(src):
            try:
                dst = os.path.join(out, 'kept', *k.split('/'))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(src, dst)
            except Exception:
                pass
    for i in range(3):
        shutil.rmtree(d, onerror=_rm_ro)
        if not os.path.exists(d):
            return True
        time.sleep(2)
    PA_LEFT.append(d)
    say('  ⚠ 하네스 임시 폴더를 다 못 지움(잠김 · 다음 실행 쓸기 몫): %s' % d)
    return False


def pa_sweep(max_age=3600):
    """실행 시작 쓸기 — pa_qa 아래 실행 폴더 가운데 그 실행기 프로세스가 없고 max_age 초 넘은 것(앞 실행이 죽어 못 지운 몫)"""
    if not os.path.isdir(PA):
        return 0
    n = 0
    for e in list(os.scandir(PA)):
        if not e.is_dir() or e.name == RUN_ID:
            continue
        m = re.search(r'_p(\d+)$', e.name)
        pid = int(m.group(1)) if m else 0
        try:
            age = time.time() - e.stat().st_mtime
        except OSError:
            continue
        if (pid and _alive(pid)) or age < max_age:
            continue
        shutil.rmtree(e.path, onerror=_rm_ro)
        n += 0 if os.path.exists(e.path) else 1
    if n:
        say('  쓸기: 앞 실행이 남긴 하네스 임시 폴더 %d 지움(%s)' % (n, PA))
    return n


def pa_end():
    """이 실행의 pa_qa 폴더 — 하네스마다 지웠으니 빈 껍데기만 · 남은 것(잠김)은 다음 실행 쓸기 몫"""
    d = os.path.join(PA, RUN_ID)
    if os.path.isdir(d):
        shutil.rmtree(d, onerror=_rm_ro)


def out_trim(app, keep=3):
    """실행 결과 폴더 WORK\\<앱>\\<하네스>\\<시각> — 하네스마다 최근 keep 개만(저장본 · 스냅샷은 N: 에 따로 · 이 폴더를 안 가리킴)"""
    base = os.path.join(WORK, app)
    if not os.path.isdir(base):
        return 0
    n = 0
    for h in os.scandir(base):
        if not h.is_dir():
            continue
        ds = sorted((x for x in os.scandir(h.path) if x.is_dir() and re.match(r'^\d{8}-\d{6}$', x.name)), key=lambda x: x.name)
        for x in (ds[:-keep] if len(ds) > keep else []):
            shutil.rmtree(x.path, onerror=_rm_ro)
            n += 0 if os.path.exists(x.path) else 1
    return n


# ── 항목 받개(A-2-2 · 재는 것은 안 바꾸고 출력만 모은다) ─────────────────────────────────────────────
RX_PIPE = re.compile(r'^\s*(PASS|FAIL|INFO|WARN|SKIP)\s*\|\s?(.*)$')
RX_END = re.compile(r'^\s*([A-Z][A-Za-z0-9_\-\[\]]{0,15})\s*\|\s*(.*?)\s*\|\s*(PASS|FAIL)\s*$')
RX_GRP = re.compile(r'^\s*((?:[A-Za-z0-9][A-Za-z0-9\-\.]{0,9}\s+){1,2})(PASS|FAIL)\b\s*(.*)$')
RX_BARE = re.compile(r'^\s*(PASS|FAIL)\b[ \t]*(\S.*)$')
# 칸 넷 줄 「PASS | 바탕 FAIL | 제목 | 값」 — 둘째 칸이 바탕 판 판정(jagwa_search · jagwa_claude_e001 · 「바탕 —」 = 바탕 안 잼)
# 해시 꼴 낱말 — 16진 6~40자 · 숫자가 하나 이상(숫자만인 해시도 · INFO 줄 id 에서만 <H>)
RX_HEXW = re.compile(r'\b(?=[0-9a-f]*\d)[0-9a-f]{6,40}\b')
RX_BVERD = re.compile(r'^(?:바탕|BASE\d?)\s+(?:PASS|FAIL|INFO|WARN|SKIP|—|-)$')
RX_SUM = re.compile(r'^\s*(PASS|FAIL)\s*\d+\s*[·,/|]\s*(FAIL|PASS)\s*\d+')
RX_SUMG = re.compile(r'^\s*(PASS|FAIL)\s*\(\s*\d+\s*칸')
VOLATILE = [
    (re.compile(r'[A-Za-z]:[\\/]+Users[\\/]+[^\\/]+[\\/]+AppData[\\/]+Local[\\/]+Temp[\\/]+[^\s\'"|,;)\]}]*', re.I), '<TMP>'),
    (re.compile(r'/tmp/[^\s\'"|,;)\]}]*'), '<TMP>'),
    (re.compile(r'[A-Za-z]:[\\/]+Users[\\/]+[^\\/]+[\\/]+Documents[\\/]+genie(?:[\\/]+\.claude[\\/]+worktrees[\\/]+[^\\/\s\'"|]+)?', re.I), '<GENIE>'),
    (re.compile(r'(?:127\.0\.0\.1|localhost):\d+'), '<HOST>'),
    (re.compile(r'\b20\d\d-\d\d-\d\d[T ]\d\d:\d\d(?::\d\d(?:\.\d+)?)?Z?'), '<TS>'),
    (re.compile(r'\b\d{1,2}:\d\d:\d\d\b'), '<HMS>'),
    (re.compile(r'\b1[6-9]\d{11}\b'), '<EPOCH>'),
    (re.compile(r'\b\d+(?:\.\d+)?\s?ms\b'), '<DUR>'),
    (re.compile(r'\b\d+(?:\.\d+)?\s?초'), '<DUR>'),
    (re.compile(r'\bpid[ =:]\d+', re.I), 'pid=<N>'),
    (re.compile(r'blob:[^\s\'"|,;)\]}]+'), '<BLOB>'),
]
RX_CODE = re.compile(r'^[\[\(]?[A-Za-z]{0,4}-?\d+[a-z]?(?:[\-\.]\d+[a-z]?)*(?:-헛)?[\]\)]?$')
# 바탕 판 측정 줄(헛잣대 재료) — 하네스가 바탕 판에 같은 잣대를 돌려 찍은 날값 줄. 새 기능 잣대는 바탕에서 FAIL 이어야 잣대가 산다
# (예: omrpop 「헛잣대(BASE) — PASS 3 · FAIL 14 (새 기능 잣대는 FAIL 이어야 잣대)」) → 판정 FAIL 과 섞지 않고 b=1 로 따로 센다(st 는 찍힌 그대로)
# BASE 뒤 숫자(BASE2 · BASE3 = 바탕 판 여럿 — penfinger_add1/add2 「BASE2 = 본판 인도판 f497f05」)도 같은 뜻
RX_BLINE = re.compile(r'^(?:(?:BASE\d?|SIAN)\s+(?:\[|chromium|webkit|책상|터치|폰|패드|pad|desk|phone|bio|earth|phys|거꾸로|·)|[^\s·|\[]{1,6}\s+BASE\d?\s+(?:·|chromium|webkit)|\[[^\]]*\bBASE\d?\])')   # A-6(d) 9/30 — toc_fuse 「BASE 거꾸로 재료」 · toc_fuse_add1 「SIAN 책상」(시안 = 바탕 + 한 줄 헛잣대)도 바탕 측정 줄


def normv(s):
    for rx, to in VOLATILE:
        s = rx.sub(to, s)
    return s


def strip_bar(s):
    """제목 끝 「 |」 떼기 — 값이 빈 FAIL 줄(「FAIL | 제목 |」)만 끝에 「 |」가 붙어 PASS 가 되면 항목 이름이 갈리던 것(9/30 gg_guard 에서 드러남) · 꼬리 「 #k」 는 둔다"""
    return re.sub(r'\s*\|(\s*#\d+)?\s*$', lambda m: m.group(1) or '', s)


def norm_id(title):
    t = normv(title).strip()
    toks = t.split()
    keep = []
    for i, w in enumerate(toks):
        if i < 3 and len(w) <= 10 and RX_CODE.match(w):
            keep.append(w)
        else:
            keep.append(re.sub(r'\d+(?:[.,]\d+)*', '#', w))
    return ' '.join(keep)[:240].rstrip()   # 자른 끝 빈칸 떼기(9/30 — 표에서 읽은 id 와 짝이 안 맞았다)


def parse(text):
    items = []
    seen = {}
    for ln in text.splitlines():
        ln = ln.rstrip()
        if not ln or RX_SUM.match(ln) or RX_SUMG.match(ln):
            continue
        st = title = val = None
        m = RX_PIPE.match(ln)
        if m:
            st = m.group(1)
            title, _, val = m.group(2).partition(' | ')
            if val and RX_BVERD.match(title.strip()):   # 제목 = 셋째 칸 · 바탕 판정은 값 앞에(9/30 — 둘째 칸을 제목으로 읽어 id 가 「바탕 PASS #k」로 뭉개졌다)
                bv = title.strip()
                title, _, val = val.partition(' | ')
                val = '[' + bv + '] ' + val
        else:
            m = RX_END.match(ln)
            if m:
                st, title, val = m.group(3), m.group(1) + ' ' + m.group(2), ''
            else:
                m = RX_GRP.match(ln)
                if m and not RX_SUM.match(m.group(2) + ' ' + m.group(3)) and not re.match(r'^\(\s*\d+\s*칸', m.group(3)):
                    st, title, val = m.group(2), ' '.join(m.group(1).split()) + ' ' + m.group(3), ''
                else:
                    m = RX_BARE.match(ln)
                    if m:
                        st = m.group(1)
                        sp = re.split(r'\s{2,}', m.group(2).strip(), maxsplit=1)
                        title, val = sp[0], (sp[1] if len(sp) > 1 else '')
        if not st:
            continue
        title = strip_bar(title.strip())
        ident = norm_id(RX_HEXW.sub('<H>', title) if st == 'INFO' else title)   # INFO 줄은 지금 커밋 해시를 제목에 찍기도 한다(판정 줄은 그대로)
        k = seen.get(ident, 0)
        seen[ident] = k + 1
        v = normv(title + ' | ' + (val or '').strip())
        it = {'id': ident + ('' if k == 0 else ' #%d' % (k + 1)), 'st': st, 't': title[:300],
              'v': v[:3000], 'vh': hashlib.md5(v.encode('utf-8')).hexdigest()[:12]}
        if RX_BLINE.match(title):
            it['b'] = 1
        items.append(it)
    return items


def counts(items):
    """PASS · FAIL · INFO … = 판정 줄 · B:PASS · B:FAIL = 바탕 판 측정 줄(헛잣대 재료)"""
    c = {}
    for it in items:
        k = ('B:' if it.get('b') else '') + it['st']
        c[k] = c.get(k, 0) + 1
    return c


# ── 한 하네스 돌리기 ─────────────────────────────────────────────────────────────────────────────
def trace_roots(ctx):
    rs = [('genie', ctx.root)]
    if NR:
        rs.append(('n', NR))
    for nm in ('spd', 'mbpdf'):
        p = other_root(nm)
        if p and os.path.isdir(p):
            rs.append((nm, p))
    lad = other_root('lad')
    if os.path.isdir(lad):
        rs.append(('lad', lad))
    vl = other_root('vault')
    if vl and os.path.isdir(vl):
        rs.append(('vault', vl))
    return rs


def fill(tpl, ctx, app, out, mode=None, snap=None):
    appf = os.path.join(ctx.root, *APP_FILE.get(app, 'jo/index.html').split('/'))
    m = {'{app}': appf, '{data}': os.path.join(ctx.root, 'jo', 'data'), '{exam}': os.path.join(ctx.root, 'gichul', 'pdf'),
         '{out}': out, '{res}': os.path.join(out, 'result.txt'), '{genie}': ctx.root, '{n}': NR or '',
         '{mbpdf}': _roots.root('MBPDF_ROOT'), '{spd}': _roots.root('SPD_ROOT')}
    res = []
    for a in tpl:
        if a == '{mode}':                    # A-1-3 — gate(또는 모드 없음)면 빈 자리 = 이 판 앞 argv
            if mode and mode != 'gate':
                res += ['--mode', mode, '--snap-out', os.path.join(out, 'snap.json')]
                if snap and os.path.isfile(snap):
                    res += ['--snap-in', snap]
            continue
        for k, v in m.items():
            a = a.replace(k, v)
        res.append(a)
    return res


def kill_tree(pid):
    if os.name == 'nt':
        subprocess.run(['taskkill', '/PID', str(pid), '/T', '/F'], capture_output=True)
    else:
        try:
            os.killpg(pid, 9)
        except Exception:
            pass


def read_trace(path):
    recs = []
    if os.path.exists(path):
        with open(path, encoding='utf-8', errors='replace') as f:
            for ln in f:
                try:
                    recs.append(json.loads(ln))
                except Exception:
                    pass
    return recs


def restore(recs, rootmap, bak, out):
    """추적 장치가 떠 둔 원래 파일로 되돌린다 · 새로 만든 파일은 결과 폴더로 건지고 지운다 · 새 폴더는 비면 지운다"""
    first = {}
    for d in recs:
        if d.get('k') == 'w':
            first.setdefault((d['r'], d['p']), d)
    got, back, gone, left = [], [], [], []
    wdir = os.path.join(out, 'written')
    for (r, p), d in first.items():
        base = rootmap.get(r)
        if not base:
            continue
        fp = os.path.join(base, *p.split('/'))
        if os.path.isfile(fp) and re.search(r'(result|report|_결과)', os.path.basename(fp), re.I):
            os.makedirs(wdir, exist_ok=True)
            try:
                shutil.copy2(fp, os.path.join(wdir, os.path.basename(fp)))
                got.append('%s:%s' % (r, p))
            except Exception:
                pass
        b = os.path.join(bak, r, *p.split('/'))
        if not d.get('new'):
            if os.path.isfile(b):
                cur = open(fp, 'rb').read() if os.path.isfile(fp) else None
                old = open(b, 'rb').read()
                if cur != old:
                    # 옛 꼴: 쓰기 실패(PermissionError)가 실행 전체를 죽였다 — ★ _task_qa_slim2(10/8 13:15 timetable gate · 잠긴 h\\app.html) 세 번 다시 · 안 되면 left
                    err = None
                    for _try in range(3):
                        try:
                            if r == 'n':
                                nwrite(fp, old)
                            else:
                                os.makedirs(os.path.dirname(fp), exist_ok=True)
                                with open(fp, 'wb') as f:
                                    f.write(old)
                            err = None
                            break
                        except (PermissionError, OSError) as e:
                            err = e
                            time.sleep(1)
                    if err is None:
                        back.append('%s:%s' % (r, p))
                    else:
                        left.append('%s:%s(되돌림 실패 %s)' % (r, p, type(err).__name__))
            else:
                left.append('%s:%s(떠 둔 것 없음)' % (r, p))
        else:
            if os.path.isfile(fp):
                try:
                    os.remove(fp)
                    gone.append('%s:%s' % (r, p))
                except Exception as e:
                    left.append('%s:%s(%s)' % (r, p, e))
    dirs = sorted({(d['r'], d['p']) for d in recs if d.get('k') == 'mkdir'}, key=lambda x: -x[1].count('/'))
    for r, p in dirs:
        base = rootmap.get(r)
        fp = os.path.join(base, *p.split('/')) if base else None
        if fp and os.path.isdir(fp) and not os.listdir(fp):
            try:
                os.rmdir(fp)
            except Exception:
                pass
    return {'건짐': got, '되돌림': back, '지움': gone, '남음': left}


def traced_inputs(recs, r_row, app, tpl):
    """추적 기록 → 입력 목록(새로 만들고 지운 파일 · 추적 장치 자신 빼고 · 한 폴더 30 넘으면 그 폴더 통째)"""
    newf = {(d['r'], d['p']) for d in recs if d.get('k') == 'w' and d.get('new')}
    got = set()
    for d in recs:
        if d.get('k') in ('open', 'mod'):
            rp = (d['r'], d['p'])
            if rp in newf or d['p'].startswith('_qa_trace/') or d['p'].startswith('.git/') or '/.git/' in d['p']:
                continue
            if d['r'] == 'genie' and d['p'].startswith('.claude/'):
                continue
            if d['r'] == 'n' and d['p'].startswith('_qa_results/'):
                continue   # 10/4 — regress --snap-in 으로 읽은 바탕 스냅샷(<열쇠>.base.json)은 입력이 아니다(열쇠의 snap 칸이 이미 담음 · 입력에 들면 다음 판 바탕 열쇠가 안 맞음 — ⑧ 회귀 기록 47)
            got.add('%s:%s' % rp)
    by = {}
    for x in got:
        r, _, p = x.partition(':')
        by.setdefault((r, p.rsplit('/', 1)[0] if '/' in p else ''), []).append(x)
    res = set()
    for (r, d), xs in by.items():
        if len(xs) > 30 and d:
            res.add('%s:%s/**' % (r, d))
        else:
            res |= set(xs)
    appfile = APP_FILE.get(app)
    if appfile:
        res.add('genie:' + appfile)
    if any('{data}' in a for a in tpl) and not any(x.startswith('genie:jo/data/') for x in res):
        res.add('genie:jo/data/**')
    if any('{exam}' in a for a in tpl) and not any(x.startswith('genie:gichul/pdf/') for x in res):
        res.add('genie:gichul/pdf/**')
    # 폴더 통째가 있으면 그 아래 낱개는 뺀다
    dirs = [x[:-3] for x in res if x.endswith('/**')]
    return sorted(x for x in res if x.endswith('/**') or not any(x.startswith(d + '/') for d in dirs))


def run_one(r, app, ctx, c, label='', note='', snap=None):
    name = rname(r)
    tpl = argv_tpl(r, app)
    md = mode_of(r, app, ctx)
    if r.get('skip'):
        return {'harness': r['file'], 'name': name, 'skip': r['skip'], 'items': [], 'sec': 0}
    if not NR:
        # 클라우드(N: 없음 · 이 실행기가 genie/_qa 사본에서 돈다) — N: 입력 가운데 _qa 사본에 없는 것이 있으면 안 돌리고 「N: 필요」(A-7-4 · env_lanes_fix 종료 코드 3 과 같은 뜻)
        miss = [x for x in (r.get('inputs') or []) if x.startswith('n:') and not os.path.exists(os.path.join(HERE, *x[2:].replace('/**', '').split('/')))]
        if miss:
            return {'harness': r['file'], 'name': name, 'skip': 'N: 필요(%s)' % ' · '.join(m[2:] for m in miss[:3]), 'items': [], 'sec': 0}
    ctx.ensure()
    stamp = time.strftime('%Y%m%d-%H%M%S')
    out = os.path.join(WORK, app, name, stamp)
    os.makedirs(out, exist_ok=True)
    bak = os.path.join(out, 'bak')
    tr = os.path.join(out, 'trace.jsonl')
    roots = trace_roots(ctx)
    env = dict(os.environ)
    env.update({'GENIE_ROOT': ctx.root, 'PYTHONUTF8': '1', 'PYTHONIOENCODING': 'utf-8', 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONUNBUFFERED': '1',
                'QA_TRACE_OUT': tr, 'QA_TRACE_BAK': bak, 'QA_TRACE_ROOTS': ';'.join('%s=%s' % x for x in roots),
                'PYTHONPATH': TRACE_DIR + (os.pathsep + env['PYTHONPATH'] if env.get('PYTHONPATH') else '')})
    hx = pa_make(name, stamp)   # ★ env_clean B-1 — 하네스의 tempfile · 크롬 · playwright 프로필 · 앱 사본이 다 이 밑에(끝나면 지움)
    env.update({'TEMP': hx, 'TMP': hx, 'TMPDIR': hx})
    for k, v in (r.get('env') or {}).items():
        env[k] = v
    argv = [sys.executable, hfile(r)] + fill(tpl, ctx, app, out, md, snap)
    pre_dirty = ctx.dirty() if not ctx.owned else None
    t0 = time.time()
    to = r.get('timeout') or 3600
    with open(os.path.join(out, 'stdout.txt'), 'wb') as so, open(os.path.join(out, 'stderr.txt'), 'wb') as se:
        p = subprocess.Popen(argv, cwd=os.path.dirname(hfile(r)), env=env, stdout=so, stderr=se, stdin=subprocess.DEVNULL,
                             creationflags=(0x00000200 if os.name == 'nt' else 0))
        timed_out = False
        try:
            rc = p.wait(timeout=to)
        except subprocess.TimeoutExpired:
            kill_tree(p.pid)
            timed_out = True
            rc = -9
            try:
                p.wait(timeout=30)
            except Exception:
                pass
    sec = round(time.time() - t0, 1)
    recs = read_trace(tr)
    rootmap = dict(roots)
    rest = restore(recs, rootmap, bak, out)
    wt_note = ''
    if ctx.owned:
        if git(ctx.root, 'status', '--porcelain', '--untracked-files=all').strip():
            wt_note = 'genie 작업트리를 바꿈 → 되돌림'
            reset_wt(ctx.root)
    else:
        ctx._tree = None
        if ctx.dirty() != pre_dirty:
            wt_note = '⚠ genie 자리 상태가 돌기 전과 다름'
    stdout = open(os.path.join(out, 'stdout.txt'), 'rb').read().decode('utf-8', 'replace')
    stderr = open(os.path.join(out, 'stderr.txt'), 'rb').read().decode('utf-8', 'replace')
    pa_drop(hx, r.get('keep'), out)   # ★ env_clean B-1 — 결과는 out(N: 저장본) · 하네스 임시 폴더는 여기서 지움(시간 넘김 · 실패 모두 이 줄을 지남)
    src, text = 'stdout', stdout
    want = r.get('res') or 'stdout'
    cands = []
    if want.startswith('here:'):
        cands = [os.path.join(out, 'written', nm) for nm in want[5:].split('+')]
    elif want != 'stdout':
        for w in want.split('+'):
            f = fill([w], ctx, app, out)[0]
            cands += sorted(glob.glob(f)) if '*' in f else [f]
    got = []
    for cf in cands:
        if os.path.isfile(cf):
            t = open(cf, 'rb').read().decode('utf-8', 'replace')
            if re.search(r'^\s*(PASS|FAIL)\b', t, re.M) or re.search(r'\|\s*(PASS|FAIL)\s*$', t, re.M):
                got.append((os.path.basename(cf), t))
    if got:
        src, text = '+'.join(x[0] for x in got), '\n'.join(x[1] for x in got)
    items = parse(text)
    if src != 'stdout' and not items:
        items = parse(stdout)
        src = 'stdout'
    if timed_out:
        items.append({'id': '(시간 초과)', 'st': 'FAIL', 't': '(시간 초과 %ds)' % to, 'v': 'timeout', 'vh': 'timeout'})
    elif rc == 3 and 'N: 필요' in stdout:
        return {'harness': r['file'], 'name': name, 'skip': 'N: 필요', 'items': [], 'sec': sec}
    elif rc not in (0, 1) and not items:
        tail = (stderr.strip().splitlines() or stdout.strip().splitlines() or [''])[-1][:300]
        items.append({'id': '(실행)', 'st': 'FAIL', 't': '(실행 실패 rc=%s)' % rc, 'v': normv('rc=%s %s' % (rc, tail)), 'vh': 'rc%s' % rc})
    elif not items:
        items.append({'id': '(항목 없음)', 'st': 'FAIL', 't': '(PASS/FAIL 줄 0 · rc=%s)' % rc, 'v': 'rc=%s' % rc, 'vh': 'noitems'})
    # 입력(추적) → 전수표 · 열쇠는 새 입력으로
    ins = traced_inputs(recs, r, app, tpl)
    if md in ('gate', 'smoke') and r.get('inputs') and not (r.get('inputs_src') or '').startswith('정적'):
        pass   # 10/4 — 모드 있는 줄은 regress 추적만 전수표 입력에 합친다(smoke 는 읽는 파일이 적어 폴더 통째(/**) 대신 낱개가 · gate 는 바탕 몫 파일이 더 들어 regress 저장본 열쇠를 흔든다 · book8 +4 사고)
    elif (r.get('inputs_src') or '').startswith('정적') or not r.get('inputs'):
        r['inputs'] = sorted(ins)            # 첫 추적 — 짐작한 입력을 잰 값으로 갈아 넣는다
        r['inputs_src'] = '추적'
    else:
        r['inputs'] = sorted(set(r['inputs']) | set(ins))
        r['inputs_src'] = '추적'
    if md in (None, 'gate', 'regress'):
        # 옛 줄: r['last_sec' if md != 'regress' else 'last_sec_regress'] = sec   # A-1 — regress 시간은 따로(gate last_sec 은 사슬 어림 · 관문 몫)
        r[{'regress': 'last_sec_regress', 'smoke': 'last_sec_smoke'}.get(md, 'last_sec')] = sec   # ★ _task_qa_slim2(10/8) — smoke 시간이 gate last_sec 을 덮어쓰던 것 → smoke 는 따로
    key, parts = key_of(r, app, ctx, snap)
    rec = {'harness': r['file'], 'name': name, 'app': app, 'key': key, 'keyparts': parts, 'genie': ctx.head, 'root': ctx.label,
           'when': time.strftime('%Y-%m-%d %H:%M:%S'), 'sec': sec, 'rc': rc, 'src': src, 'counts': counts(items), 'items': items,
           'argv': [os.path.basename(a) if os.path.isabs(a) else a for a in argv[2:]], 'restore': rest, 'wt': wt_note,
           'raw': text[:400000], 'err': stderr[-3000:], 'note': note, 'label': label}
    if md:
        rec['mode'] = md
    sj = None
    if md and md != 'gate':
        sp_out = os.path.join(out, 'snap.json')
        sj = open(sp_out, 'rb').read().decode('utf-8') if os.path.isfile(sp_out) else None
        lp = os.path.join(out, 'launch.json')
        rec['launch'] = jload(lp) if os.path.isfile(lp) else None   # §B-4 — 바탕 띄움 · 하위 하네스 · 굽기 셈
        rec['snap_in'] = os.path.basename(snap) if snap and os.path.isfile(snap) else ''
    rp = res_path(app, key, label)
    nwrite(rp, jdump(rec)) if NR else _w(rp, jdump(rec))
    if label and label != 'again' and not os.path.exists(res_path(app, key)):
        mp = res_path(app, key)            # 이름표 실행도 그 열쇠의 저장본 칸이 비었으면 채운다(첫 결과 = 저장본)
        nwrite(mp, jdump(rec)) if NR else _w(mp, jdump(rec))
    if sj is not None and label != 'again':
        # A-1-3 — 기준 칸 스냅샷 = 저장본 옆 <열쇠>.base.json · 바탕 스냅샷과 맞댄 새 판 결과는 스냅샷 없는 열쇠로도 둔다
        # (인도 판의 회귀 결과가 곧 다음 판의 저장본 — 다음 compare 의 바탕 열쇠는 스냅샷 없이 셈)
        keys = [key]
        if parts.get('snap'):
            k0, _ = key_of(r, app, ctx)
            keys.append(k0)
            if not os.path.exists(res_path(app, k0)):
                r0 = dict(rec, key=k0, note=(note + ' · 스냅샷 없는 열쇠로도 둠').strip(' ·'))
                nwrite(res_path(app, k0), jdump(r0)) if NR else _w(res_path(app, k0), jdump(r0))
        for k in keys:
            nwrite(snap_path(app, k), sj) if NR else _w(snap_path(app, k), sj)
    return rec


def _w(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)


def line_of(rec):
    if rec.get('skip'):
        return '%s %-26s 건넘(%s)' % (time.strftime('%H:%M:%S'), rec['name'], rec['skip'])
    c = rec['counts']
    x = ' · '.join(y for y in (rec.get('wt'), ('되돌림 %d' % len(rec['restore']['되돌림'])) if rec['restore']['되돌림'] else '',
                                ('남음 %d' % len(rec['restore']['남음'])) if rec['restore']['남음'] else '') if y)
    return '%s %-26s rc=%s %5.0fs PASS %d FAIL %d INFO %d · %s · 열쇠 %s%s' % (
        time.strftime('%H:%M:%S'), rec['name'], rec['rc'], rec['sec'], c.get('PASS', 0), c.get('FAIL', 0), c.get('INFO', 0),
        rec['src'], rec['key'], (' · ' + x) if x else '')


def save_run(app, runid, recs, meta):
    man = {'run': runid, 'app': app, 'meta': meta,
           'rows': [{'harness': x['harness'], 'name': x['name'], 'key': x.get('key'), 'label': x.get('label', ''), 'sec': x.get('sec', 0),
                     'rc': x.get('rc'), 'counts': x.get('counts', {}), 'skip': x.get('skip', ''), 'reused': x.get('reused', False)} for x in recs]}
    p = os.path.join(RESD, app, '_runs', runid + '.json')
    nwrite(p, jdump(man)) if NR else _w(p, jdump(man))
    return p


def load_rec(app, key, label=''):
    return jload(res_path(app, key, label))


# ── 명령 ────────────────────────────────────────────────────────────────────────────────────────
def cmd_census(args):
    c = jload(LIST) or {'v': 1, 'apps': APPS, 'rows': []}
    have = {r['file'] for r in c['rows']}
    hs = n_harnesses()
    if hs is None:
        raise SystemExit('N: 이 없어 N: 정본 하네스를 셀 수 없다')
    miss = [h for h in hs if h not in have]
    gone = sorted(have - set(hs))
    say('N: 정본 하네스 %d · 전수표 줄 %d · 빠짐 %d · 없어진 하네스 줄 %d' % (len(hs), len(c['rows']), len(miss), len(gone)))
    for h in miss:
        say('  빠짐 ', h)
    for h in gone:
        say('  없어짐', h)
    if args.get('--write') and miss:
        for h in miss:
            c['rows'].append({'file': h, 'app': app_of(h), 'chains': [app_of(h)], 'what': '', 'tags': ['미분류'], 'eng': [],
                              'inputs': [], 'inputs_src': '', 'argv': {'*': []}, 'res': 'stdout', 'last_sec': None})
        census_save(c)
        say('더함 %d — 무엇 · 태그 · 인자 꼴을 채울 것' % len(miss))
    return 1 if (miss or gone) else 0


def cmd_check(args):
    c = census_load()
    bad = []
    hs = n_harnesses()
    rows = {r['file']: r for r in c['rows']}
    if hs is not None:
        for h in hs:
            if h not in rows:
                bad.append('전수표에 줄 없음: ' + h)
        for f in rows:
            if f not in hs:
                bad.append('하네스 없는 줄: ' + f)
        per = {}
        for h in hs:
            per.setdefault(app_of(h), [0, 0])[0] += 1
        for r in c['rows']:
            per.setdefault(r['app'], [0, 0])[1] += 1
        for a, (x, y) in sorted(per.items()):
            say('  %-9s 하네스 %3d · 줄 %3d%s' % (a, x, y, '' if x == y else '  ← 어긋남'))
    for r in c['rows']:
        for k in ('what', 'tags', 'inputs'):
            if not r.get(k) or r.get(k) == ['미분류']:
                bad.append('%s 빈칸: %s' % (k, r['file']))
        if r['app'] != app_of(r['file']):
            bad.append('앱이 폴더와 다름: %s (%s)' % (r['file'], r['app']))
    for b in bad:
        say('FAIL', b)
    say('check %s — 줄 %d · 어긋남 %d' % ('OK' if not bad else 'NG', len(c['rows']), len(bad)))
    return 1 if bad else 0


def parse_args(av):
    out, pos, i = {}, [], 0
    while i < len(av):
        a = av[i]
        if a.startswith('--'):
            if i + 1 < len(av) and not av[i + 1].startswith('--') and a not in ('--reuse', '--write', '--no-flaky', '--keep-root', '--dry'):
                out[a] = av[i + 1]
                i += 2
                continue
            out[a] = True
        else:
            pos.append(a)
        i += 1
    return out, pos


def lst(v):
    return [x for x in (v or '').split(',') if x] if isinstance(v, str) else None


def arg_mode(args):
    """--mode gate|regress|smoke — 없으면 None(jo = regress · 판 관문은 --mode gate) · --scope smoke 만이면 smoke"""
    m = args.get('--mode') if isinstance(args.get('--mode'), str) else None
    if m and m not in ('gate', 'regress', 'smoke'):
        raise SystemExit('--mode 는 gate | regress | smoke')
    if not m and lst(args.get('--scope')) == ['smoke']:
        m = 'smoke'
    return m


def cmd_run(args, pos):
    app = pos[0]
    c = census_load()
    rows = rows_for(c, app, lst(args.get('--scope')), lst(args.get('--only')))
    if not rows:
        raise SystemExit('돌릴 하네스 0 — 앱·범위를 볼 것')
    lf = lock()
    vendor_check()   # ★ _task_qa_fix1 A-5 — pdf.js 사본(없음 · 깨짐이면 받아 채움 · 둘 다 없으면 이 줄이 실행 첫 줄 경고)
    pa_sweep()   # ★ env_clean B-2
    ctx = ctx_from(args)
    ctx.mode = arg_mode(args)
    runid = time.strftime('%Y%m%d-%H%M') + '_run' + ('_' + args['--label'] if args.get('--label') else '')
    say('== run %s · 하네스 %d · genie %s (%s) · %s · 모드 %s' % (app, len(rows), ctx.head[:7], ctx.root or '분리 워크트리 — 돌릴 때 꺼냄', runid,
                                                          ctx.mode or ('regress(jo 기본)' if app in MODE_APPS else '없음')))
    recs, t0 = [], time.time()
    try:
        for r in rows:
            if args.get('--reuse') and not r.get('skip'):
                k, _ = key_of(r, app, ctx)
                old = load_rec(app, k)
                if old:
                    old['reused'] = True
                    recs.append(old)
                    say('%s %-26s 저장본 그대로(열쇠 %s)' % (time.strftime('%H:%M:%S'), old['name'], k))
                    continue
            rec = run_one(r, app, ctx, c, label=args.get('--label', '') if isinstance(args.get('--label'), str) else '')
            recs.append(rec)
            say(line_of(rec))
            if not rec.get('skip'):
                census_save(c)
        _hcache_save()
        man = save_run(app, runid, recs, {'genie': ctx.head, 'root': ctx.root or ('qa_' + ctx.head[:7]), 'scope': args.get('--scope', ''), 'sec': round(time.time() - t0)})
        tot = {}
        for x in recs:
            for k, v in (x.get('counts') or {}).items():
                tot[k] = tot.get(k, 0) + v
        say('== 끝 · %d초 · PASS %d · FAIL %d · INFO %d · 실행 기록 %s' % (time.time() - t0, tot.get('PASS', 0), tot.get('FAIL', 0), tot.get('INFO', 0), man))
    finally:
        if not args.get('--keep-root'):
            ctx.drop()
        pa_end()   # ★ env_clean B-1 · B-5
        out_trim(app)
        try:
            os.remove(lf)
        except Exception:
            pass
    return 0


def classify(base_items, new_items):
    """A-4 — 새 FAIL · FAIL 값 바뀜 · 원래 FAIL · 새 PASS · 사라진 항목 · 새 항목(INFO·WARN 은 안 가른다)"""
    B = {x['id']: x for x in base_items}
    N = {x['id']: x for x in new_items}
    out = {'새 FAIL': [], 'FAIL 값 바뀜': [], '원래 FAIL': [], '새 PASS': [], '사라진 항목': [], '새 항목': [], '바탕 측정 바뀜': [], '같음': 0}
    for i, b in B.items():
        n = N.get(i)
        if n is None:
            if b['st'] in ('PASS', 'FAIL'):
                out['바탕 측정 바뀜' if b.get('b') else '사라진 항목'].append((b, None))
            continue
        if b.get('b') or n.get('b'):
            if b['st'] != n['st'] or b['vh'] != n['vh']:
                out['바탕 측정 바뀜'].append((b, n))
            else:
                out['같음'] += 1
            continue
        if b['st'] == 'PASS' and n['st'] == 'FAIL':
            out['새 FAIL'].append((b, n))
        elif b['st'] == 'FAIL' and n['st'] == 'FAIL':
            (out['원래 FAIL'] if b['vh'] == n['vh'] else out['FAIL 값 바뀜']).append((b, n))
        elif b['st'] == 'FAIL' and n['st'] == 'PASS':
            out['새 PASS'].append((b, n))
        else:
            out['같음'] += 1
    for i, n in N.items():
        if i not in B and n['st'] in ('PASS', 'FAIL'):
            if n['st'] == 'FAIL' and not n.get('b'):
                # _task_qa_slim(10/4) — 바탕에 없던 칸이 새 판에서 FAIL = 새 FAIL(바탕 b=None) · 10/4 묶은 회귀에서 2cha_unit_b7 「.ysel 예외」 ·
                # ms_canvas_relayout 웹킷 예외가 「사라진 + 새 항목」으로 숨어 「한 번 더」도 안 돌았다(§B-1 조사 · 결정로그 10/4 07:49)
                out['새 FAIL'].append((None, n))
            else:
                out['바탕 측정 바뀜' if n.get('b') else '새 항목'].append((None, n))
    return out


def flaky_add(rec, item_id, v1, v2, st1, st2):
    fl = jload(FLAKY, []) or []
    fl.append({'harness': rec['harness'], 'item': item_id, 'date': time.strftime('%Y-%m-%d %H:%M'), 'values': [v1[:600], v2[:600]], 'st': [st1, st2]})
    s = jdump(fl)
    nwrite(FLAKY, s) if NR else _w(FLAKY, s)
    return sum(1 for x in fl if x['harness'] == rec['harness'] and x['item'] == item_id)


def plan(app, rows, bctx, nctx):
    out = []
    for r in rows:
        if r.get('skip'):
            out.append((r, None, None, 'skip'))
            continue
        bk, _ = key_of(r, app, bctx)
        nk, _ = key_of(r, app, nctx) if nctx is not bctx else (bk, None)
        out.append((r, bk, nk, None))
    return out


def cmd_plan(args, pos):
    app = pos[0]
    c = census_load()
    rows = rows_for(c, app, lst(args.get('--scope')), lst(args.get('--only')))
    bctx = ctx_from(args, 'base')
    nctx = ctx_from(args)
    bctx.mode = nctx.mode = arg_mode(args)
    try:
        nb = nn = 0
        # ★ _task_qa_slim2 A-1-4(10/8) — 시간 합: 돌 것마다 last_sec(regress 면 last_sec_regress 먼저) · 잰 적 없으면 따로 셈 · 무리 k(--lanes · 기본 3) 벽시계 = 긴 것부터 고르게(LPT) 나눈 무리 합의 최댓값
        bs, ns, unk = [], [], []
        for r, bk, nk, sk in plan(app, rows, bctx, nctx):
            if sk:
                say('%-26s 건넘(%s)' % (rname(r), r['skip']))
                continue
            has = os.path.exists(res_path(app, bk))
            same = bk == nk
            nhas = same or os.path.exists(res_path(app, nk))   # 새 판 저장본이 이미 있으면 새 판에서도 안 돎(run --reuse · compare --reuse 와 같음)
            nb += (not has)
            # 옛 줄: nn += (not same)
            nn += (not nhas)
            m = mode_of(r, app, nctx)
            sec = (r.get('last_sec_smoke') if m == 'smoke' else None) or (r.get('last_sec_regress') if m in ('regress', 'smoke') else None) or r.get('last_sec')   # ★ 10/8 smoke 는 smoke 시간 먼저
            if not has:
                (bs if sec else unk).append(float(sec or 0))
            if not nhas:
                (ns if sec else unk).append(float(sec or 0))
            say('%-26s 바탕 %s %s · 새 판 %s%s' % (rname(r), bk, '저장본 있음' if has else '→ 바탕에서 돎', '= 바탕(안 돎)' if same else nk + (' 저장본 있음' if nhas else ' → 새 판에서 돎'),
                                             (' · %.1f 분' % (float(sec) / 60) if sec else ' · 잰 적 없음') if (not has or not nhas) else ''))
        k = int(args.get('--lanes')) if isinstance(args.get('--lanes'), str) and args.get('--lanes').isdigit() else 3
        lanes = [0.0] * max(1, k)
        for s in sorted(bs + ns, reverse=True):
            lanes[lanes.index(min(lanes))] += s
        # 옛 줄: say('== plan · 하네스 %d · 바탕에서 돌 것 %d · 새 판에서 돌 것 %d' % (len(rows), nb, nn))
        say('== plan · 하네스 %d · 바탕에서 돌 것 %d(last_sec 합 %.1f 분) · 새 판에서 돌 것 %d(%.1f 분)%s · 무리 %d 면 벽시계 ≈ %.1f 분' % (
            len(rows), nb, sum(bs) / 60, nn, sum(ns) / 60, (' · 잰 적 없음 %d(시간 셈 밖)' % len(unk)) if unk else '', k, max(lanes) / 60))
    finally:
        bctx.drop()
        nctx.drop()
    return 0


def cmd_compare(args, pos):
    app = pos[0]
    c = census_load()
    scope = lst(args.get('--scope'))
    rows = rows_for(c, app, scope, lst(args.get('--only')))
    if not rows:
        raise SystemExit('돌릴 하네스 0')
    lf = lock()
    vendor_check()   # ★ _task_qa_fix1 A-5 — pdf.js 사본(없음 · 깨짐이면 받아 채움 · 둘 다 없으면 이 줄이 실행 첫 줄 경고)
    pa_sweep()   # ★ env_clean B-2
    bctx = ctx_from(args, 'base')
    nctx = ctx_from(args)
    bctx.mode = nctx.mode = arg_mode(args)
    runid = time.strftime('%Y%m%d-%H%M') + '_compare'
    say('== compare %s · 하네스 %d · 바탕 %s · 새 판 %s (%s) · 범위 %s · 모드 %s' % (app, len(rows), bctx.head[:7], nctx.head[:7], nctx.root or '분리 워크트리', scope or '전체',
                                                                  nctx.mode or ('regress(jo 기본)' if app in MODE_APPS else '없음')))
    t0 = time.time()
    rep = []
    try:
        for r in rows:
            if r.get('skip'):
                rep.append({'name': rname(r), 'skip': r['skip']})
                say('%s %-26s 건넘(%s)' % (time.strftime('%H:%M:%S'), rname(r), r['skip']))
                continue
            bk, _ = key_of(r, app, bctx)
            base = load_rec(app, bk)
            bsec = 0
            if base is None:
                base = run_one(r, app, bctx, c, note='compare 바탕')
                census_save(c)
                bsec = base.get('sec', 0)
                say(line_of(base) + ' [바탕]')
                bk = base.get('key', bk)
            # A-1-3 — regress · smoke: 새 판의 기준 칸은 바탕 저장본 옆 스냅샷(<바탕 열쇠>.base.json)과 맞댄다
            sp = snap_path(app, bk) if mode_of(r, app, nctx) not in (None, 'gate') else None
            sp = sp if sp and os.path.isfile(sp) else None
            nk0, _ = key_of(r, app, nctx)
            nk, _ = key_of(r, app, nctx, sp)
            nsec = 0
            if nk0 == bk:
                new = base
                say('%s %-26s 새 판 입력 = 바탕 입력(열쇠 %s) — 안 돎' % (time.strftime('%H:%M:%S'), rname(r), nk0))
            else:
                new = load_rec(app, nk) if args.get('--reuse') else None
                if new is None:
                    new = run_one(r, app, nctx, c, note='compare 새 판', snap=sp)
                    census_save(c)
                    nsec = new.get('sec', 0)
                    say(line_of(new) + ' [새 판]')
            if base.get('skip') or new.get('skip'):
                rep.append({'name': rname(r), 'skip': base.get('skip') or new.get('skip')})
                continue
            cl = classify(base['items'], new['items'])
            fl = []
            if not args.get('--no-flaky') and (cl['새 FAIL'] or cl['FAIL 값 바뀜']) and new is not base:
                again = run_one(r, app, nctx, c, label='again', note='흔들림 확인', snap=sp)
                say(line_of(again) + ' [한 번 더]')
                nsec += again.get('sec', 0)
                A = {x['id']: x for x in again['items']}
                for cat in ('새 FAIL', 'FAIL 값 바뀜'):
                    keep = []
                    for b, n in cl[cat]:
                        a = A.get(n['id'])
                        if a is None or a['st'] != n['st'] or a['vh'] != n['vh']:
                            k = flaky_add(new, n['id'], n['v'], a['v'] if a else '(없음)', n['st'], a['st'] if a else '-')
                            fl.append((cat, b, n, a, k))
                        else:
                            keep.append((b, n))
                    cl[cat] = keep
            rep.append({'name': rname(r), 'file': r['file'], 'bkey': bk, 'nkey': new.get('key'), 'bsec': bsec, 'nsec': nsec, 'cl': cl, 'fl': fl,
                        'same_key': new is base})
        _hcache_save()
    finally:
        bctx.drop()
        nctx.drop()
        pa_end()   # ★ env_clean B-1 · B-5
        out_trim(app)
        try:
            os.remove(lf)
        except Exception:
            pass
    return report(app, runid, rep, bctx, nctx, scope, time.time() - t0)


def fmt_pair(b, n):
    bv = (b or {}).get('v', '') if b else '(없음)'
    nv = (n or {}).get('v', '') if n else '(없음)'
    return '바탕 %s %s\n        새 판 %s %s' % ((b or {}).get('st', '-'), bv[:400], (n or {}).get('st', '-'), nv[:400])


def report(app, runid, rep, bctx, nctx, scope, sec):
    L = ['== compare %s · 바탕 %s · 새 판 %s · 범위 %s · %d초' % (app, bctx.head[:7], nctx.head[:7], ','.join(scope) if scope else '전체', sec), '']
    tot = {k: 0 for k in ('새 FAIL', 'FAIL 값 바뀜', '원래 FAIL', '새 PASS', '사라진 항목', '새 항목', '바탕 측정 바뀜')}
    nfl = 0
    L.append('하네스별 — 새 FAIL · FAIL 값 바뀜 · 원래 FAIL · 새 PASS · 사라진 · 새 항목 · 흔들림 · 바탕 돎(초) · 새 판 돎(초)')
    for x in rep:
        if x.get('skip'):
            L.append('  %-26s 건넘(%s)' % (x['name'], x['skip']))
            continue
        cl = x['cl']
        for k in tot:
            tot[k] += len(cl[k])
        nfl += len(x['fl'])
        L.append('  %-26s %3d %3d %3d %3d %3d %3d %3d  %s  %s' % (x['name'], len(cl['새 FAIL']), len(cl['FAIL 값 바뀜']), len(cl['원래 FAIL']), len(cl['새 PASS']),
                                                            len(cl['사라진 항목']), len(cl['새 항목']), len(x['fl']),
                                                            ('%5.0f' % x['bsec']) if x['bsec'] else '저장본', ('%5.0f' % x['nsec']) if x['nsec'] else ('입력 같음' if x['same_key'] else '저장본')))
    L.append('')
    L.append('합 — 새 FAIL %(새 FAIL)d · FAIL 값 바뀜 %(FAIL 값 바뀜)d · 원래 FAIL %(원래 FAIL)d · 새 PASS %(새 PASS)d · 사라진 항목 %(사라진 항목)d · 새 항목 %(새 항목)d · 바탕 측정 바뀜 %(바탕 측정 바뀜)d' % tot
             + ' · 흔들림 %d' % nfl)
    for cat in ('새 FAIL', 'FAIL 값 바뀜', '사라진 항목', '새 PASS', '새 항목', '바탕 측정 바뀜'):
        rows = [(x['name'], b, n) for x in rep if not x.get('skip') for b, n in x['cl'][cat]]
        if not rows:
            continue
        L.append('')
        L.append('── %s %d%s' % (cat, len(rows), '' if cat in ('새 FAIL', 'FAIL 값 바뀜', '사라진 항목') else ' (참고)'))
        for nm, b, n in rows:
            L.append('  %s · %s' % (nm, (n or b)['t'][:200]))
            L.append('        ' + fmt_pair(b, n))
    fls = [(x['name'],) + f for x in rep if not x.get('skip') for f in x['fl']]
    if fls:
        L.append('')
        L.append('── 흔들림 %d (한 번 더 돌린 값이 달랐다 — _qa_flaky.json)' % len(fls))
        for nm, cat, b, n, a, k in fls:
            L.append('  %s · %s (%s로 보였던 것 · 누적 %d회%s)' % (nm, n['t'][:180], cat, k, ' · 3회 넘음 → 하네스 고칠 목록' if k > 3 else ''))
    txt = '\n'.join(L) + '\n'
    say(txt)
    p = os.path.join(RESD, app, '_runs', runid + '.txt')
    nwrite(p, txt) if NR else _w(p, txt)
    man = {'run': runid, 'app': app, 'base': bctx.head, 'new': nctx.head, 'scope': scope, 'sec': round(sec), 'tot': tot, 'flaky': nfl,
           'rows': [{'name': x['name'], 'skip': x.get('skip', ''), 'bkey': x.get('bkey'), 'nkey': x.get('nkey'), 'bsec': x.get('bsec'), 'nsec': x.get('nsec'),
                     'n': {k: len(v) for k, v in x['cl'].items() if k != '같음'} if x.get('cl') else {},
                     'ids': {k: [(n or b)['id'] for b, n in v] for k, v in x['cl'].items() if k not in ('같음', '원래 FAIL')} if x.get('cl') else {},
                     'flaky': [n['id'] for _, b, n, a, k in x.get('fl', [])]} for x in rep]}
    q = os.path.join(RESD, app, '_runs', runid + '.json')
    nwrite(q, jdump(man)) if NR else _w(q, jdump(man))
    say('보고 %s' % p)
    return 2 if (tot['새 FAIL'] or tot['FAIL 값 바뀜'] or tot['사라진 항목']) else 0


def cmd_show(args, pos):
    app = pos[0]
    c = census_load()
    rows = rows_for(c, app, lst(args.get('--scope')), lst(args.get('--only')))
    ctx = ctx_from(args)
    try:
        for r in rows:
            if r.get('skip'):
                say('%-26s 건넘(%s)' % (rname(r), r['skip']))
                continue
            k, _ = key_of(r, app, ctx)
            rec = load_rec(app, k)
            say('%-26s 열쇠 %s %s' % (rname(r), k, ('PASS %d FAIL %d · %.0fs · %s' % (rec['counts'].get('PASS', 0), rec['counts'].get('FAIL', 0), rec['sec'], rec['when'])) if rec else '저장본 없음'))
    finally:
        ctx.drop()
    return 0


def cmd_reparse(args, pos):
    """저장본 원문(raw)을 지금 받개로 다시 읽는다 — 받개를 고친 뒤(열쇠 · 잰 것은 그대로 · 항목 줄 읽기만)"""
    app = pos[0]
    d = os.path.join(RESD, app)
    n = m = 0
    byk = {}
    for f in sorted(os.listdir(d)):
        if not f.endswith('.json') or f.startswith('_'):
            continue
        p = os.path.join(d, f)
        rec = jload(p)
        if not rec or 'raw' not in rec:
            continue
        m += 1
        syn = [x for x in rec['items'] if x['id'].startswith('(')]
        items = parse(rec['raw'])
        if not items or any(x['id'] == '(시간 초과)' for x in syn):
            items += [x for x in syn if x['id'] not in {y['id'] for y in items}]
        if items != rec['items']:
            rec['items'], rec['counts'] = items, counts(items)
            nwrite(p, jdump(rec)) if NR else _w(p, jdump(rec))
            n += 1
        byk[f[:-5]] = rec['counts']
    rd = os.path.join(d, '_runs')
    for f in sorted(os.listdir(rd)) if os.path.isdir(rd) else []:
        if f.endswith('.json') and '_run' in f:
            p = os.path.join(rd, f)
            man = jload(p)
            ch = False
            for x in man.get('rows', []):
                k = (x.get('key') or '') + (('@' + x['label']) if x.get('label') else '')
                if k in byk and x.get('counts') != byk[k]:
                    x['counts'] = byk[k]
                    ch = True
            if ch:
                nwrite(p, jdump(man)) if NR else _w(p, jdump(man))
    say('reparse %s — 저장본 %d · 바뀐 것 %d' % (app, m, n))
    return 0


def cmd_diff(args, pos):
    app, a, b = pos[0], pos[1], pos[2]
    A = jload(os.path.join(RESD, app, '_runs', a if a.endswith('.json') else a + '.json'))
    B = jload(os.path.join(RESD, app, '_runs', b if b.endswith('.json') else b + '.json'))
    bn = {x['name']: x for x in B['rows']}
    tot = {}
    diffs = []
    for x in A['rows']:
        y = bn.get(x['name'])
        if not y or x.get('skip') or y.get('skip'):
            continue
        ra, rb = load_rec(app, x['key'], x.get('label', '')), load_rec(app, y['key'], y.get('label', ''))
        cl = classify(ra['items'], rb['items'])
        for k, v in cl.items():
            if k != '같음':
                tot[k] = tot.get(k, 0) + len(v)
                if k != '원래 FAIL':
                    diffs += [(x['name'], k, p, q) for p, q in v]
    say('== diff %s %s ↔ %s · %s' % (app, a, b, ' · '.join('%s %d' % kv for kv in tot.items())))
    for nm, k, p, q in diffs:
        say('  %s · %s · %s' % (nm, k, (q or p)['t'][:160]))
        say('        ' + fmt_pair(p, q))
    return 0


def main(av):
    if not av or av[0] in ('-h', '--help'):
        say(__doc__)
        return 0
    args, pos = parse_args(av[1:])
    cmd = av[0]
    if cmd == 'census':
        return cmd_census(args)
    if cmd == 'check':
        return cmd_check(args)
    if cmd in ('run', 'compare', 'plan', 'show', 'diff', 'reparse') and (not pos or pos[0] not in APPS):
        raise SystemExit('앱을 줄 것: %s' % ' · '.join(APPS))
    return {'run': cmd_run, 'compare': cmd_compare, 'plan': cmd_plan, 'show': cmd_show, 'diff': cmd_diff, 'reparse': cmd_reparse}[cmd](args, pos)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
