# -*- coding: utf-8 -*-
r"""_task_jagwa_uid_unify 관문 「UU」 — 지학·생물 기록 열쇠 uid 옮김(§B · 커밋 ①) · Claude 풀이 창 새 꼴·재료(§E · 커밋 ②③) · 목록·서랍·문제 창·다음 회독(§H · 커밋 ④)
(2026-10-04 · 같은 길 = _harness_jagwa_uid.py(HU: Dev · 기록 route 사본 · PUT 가로채기) · _harness_jagwa_claude_e004.py(CE4: 번호 인자 판 · 창 · 모션 · 기기 둘 · 바탕 열 꼴))

  python _harness_jagwa_uid_unify.py [--only B,E,H] [--eng chromium,webkit] [--root <genie 자리> | --rev <genie 커밋>] [--base <genie 커밋>] [--seed <studyplandata 커밋>] [--res <결과>]

  NEW  = <root>/jagwa/index.html + <root>/jagwa/motion/*   (--root 안 주면 GENIE_ROOT = 본 클론 · 줄 워크트리는 --root C:\...\genie\.claude\worktrees\uid_unify)
         --rev <genie 커밋> 을 주면 작업트리 대신 그 커밋의 jagwa/index.html · motion/* (git show · 읽기만 — 줄 워크트리가 손질 중일 때)
  BASE = genie 커밋 --base(기본 4754b1d = 이 판 앞 바탕)의 jagwa/index.html + jagwa/motion/*   (헛잣대 · 같은 잣대를 바탕에도 대어 「바탕 PASS|FAIL」 칸을 채운다)
         NEW 와 BASE 의 앱·모션이 바이트(LF 기준) 같으면(바탕 그대로 돌릴 때) 한 번만 재서 두 칸에 쓴다 — 헛잣대가 서는지(바탕에서 FAIL 하는지)가 곧 그 줄이다.
  기록 고정본 = studyplandata 커밋 --seed(기본 eb920627 · 10/4 16:10)의 earth·bio·phys 기록.json 과 문항.json · 목차.json …(json 은 git 에서 바로 · 그림·PDF 는 SPD 작업트리) — studyplandata 에 쓰지 않는다.
         기록은 route 사본으로만 먹이고 PUT 은 가로채 몸통만 모은다(밖으로 안 나감 · HU INIT) — 원격 사본은 올린 몸통으로 갈아 끼워 기기 사이 섞기(B-5)를 흉내 낸다.
  문항.json 을 먹이는 길 — 앱은 문항을 ghSha(CUR.DATA_PATH)·ghRaw(…) 로 받아(HU INIT 이 api.github.com/…/contents/<경로> 를 /data/<경로> 로 돌림) sha 가 IndexedDB 캐시(kv earthdata)와 다르면 문항 ·
         목차 · pdf/index.json 을 다시 받아 buildData 로 DATA 를 새로 짓는다. 그래서 B-4 는 Overlay(rec) 에 「earth/문항.json」 = 앞에 가짜 문항(G99-99-99)을 끼운 사본을 넣어 같은 기기를 다시 연다
         (X-Sha = 바이트 sha1 이라 달라진다 · F.NO 가 +1 씩 밀린다).
  기기 하나 = 브라우저 문맥 하나(IndexedDB·localStorage 유지) · 같은 출처에서 앱·데이터를 갈아 끼워 「옛 판 → 새 판」을 잰다.
  ⚠ 자과앱 픽셀 IDENTICAL 게이트 없음(CLAUDE.md 검산 게이트) — 값 · DOM 글자 · getBoundingClientRect · elementFromPoint 로 잰다. 값을 박지 않는다 —
    셈은 고정본에서 재서 맞대고(expect_mig) 지시서 표 값과 같은지도 따로 줄로 센다(S 줄).
  ⚠ 읽는 자리 = 「저장·동기화」 쪽(PUT 몸통 · localStorage u/gone/shadow · IndexedDB kv)이 먼저다 — 새 판이 메모리 dict 를 uid 로 두든 번호로 두든(설계는 Code 몫) 선 위의 모양은 같아야 한다.
  ⚠ 폰 손가락 = Chromium CDP Input.dispatchTouchEvent(접촉 반지름 10px) · WebKit touchscreen.tap. 반지름 22(아이패드 손가락)는 폰 390 에서 카드가 0.5배로 줄어 선택지 단추가 40×15px 라
    바탕에서도 톡이 안 먹는다(필기 덮개 뚫기 판정 — 바탕 동작 · 실측 10/4).

  칸(묶음 · 엔진마다) — 한 줄 = 한 칸. 이름 머리 글자가 묶음.
    S 정적(엔진 `-`)  S-1 고정본(md5 · 63·66·4·3·478·380) · S-2 닻 표(84·111·119·149 ↔ uid) · S-3 재료 넷(D-2 표) · S-4 기출 319 uid 의 회·번 = 데이터 · S-5 제목 규칙(C-1) · S-6 motion(D-1: index.json · 파일 이름 · 바이트)
    B 커밋 ①         B-1 셈 무변 · 열쇠 전부 uid · 불변 통 · 옛 기록 있는 기기(열 때 옮김) · 합성 기록(note·qtype·conc·twin 값 속 번호·ansfix·txt) / B-2 닻(gpt 글 · status h · 도장) · 묘비 · 도장 규칙 · 그림자 /
                      B-3 화면 무변(목록 319줄 전부 · 서랍 · 히트맵 · 카운터 — 바탕과 DOM 맞댐) / B-4 문항.json 앞에 가짜 문항 → 기록이 따라간다 / B-5 옛 판 기기 섞기(두 차례) · 새 판은 번호 열쇠를 안 쓴다(마크·코멘트·Claude 저장 · 가드 0) /
                      B-6 두 번째 열기 멱등 · bak_uid 한 번 · 생물 빈 기록 = 옮김 0 · 물리 기록·화면 무변 / B-7 헛잣대(B-2·B-4 가 바탕에서 FAIL)
    E 커밋 ②③         E-1 창 네 개(제목 · 둘째 줄 · 「▶ 모션」 · iframe · 이웃 문항 · 콘솔) / E-2 읽기 판(절 5 · 첫 문단 Q · QA 줄 0 · 표 1 · 글머리·굵게 셈 = 재료) / E-3 기기 둘(빈 기기 · 옛 기록 기기) /
                      E-4 목록 Claude 태그 / E-5 물리 #72·#97 창 무변 / E-6 헛잣대
    H 커밋 ④         H-1 「NN회 N번」 걷기(서랍 · 목록 · #vT1 · .cmeta · 암기카드·🃏·정리·근거·검색 면 · 확인문제 무변 · 생물 표본) / H-2 「N회독」 칩 · 서랍 회독마다 마크 / H-3 다음 회독(PC 마우스 · 폰 손가락 ① 처음 열기 ② ④ 누름→닫기→열기
                      ③ 보기만 → 이어감 ④ 서랍으로 딴 문항 갔다 오면 새 회독 · 보기 24칸 옮김 · 기기 둘) / H-4 화면 훑기(규칙 60 · 폭 1440·900·834·390 · 판 결함 = 바탕에 없던 넘침·잘림·겹침·가려짐) / H-5 헛잣대
  결과 줄 = `PASS|FAIL|INFO | 바탕 PASS|FAIL|— | 엔진 · 칸 이름 | 값` · 끝 줄 `== PASS n · FAIL m`.
    앞 칸 = 이 판(NEW) · 「바탕」 칸 = 같은 잣대를 바탕 판에 댄 것(— = 바탕에 댈 수 없는 칸: NEW↔BASE 맞대기 · 정적 칸). 바탕 칸이 FAIL 이면 그 칸은 헛잣대가 선 것(감도 있음).
  못 짠 칸(까닭) — 🃏 손필기 암기카드를 펜으로 쓰는 길(pen 포인터만 받는다 · mcard 는 옮김 칸 셈으로만) · 카드 층의 코멘트 UI(#tNote 가 카드 층에서 숨김 → noteSheet 를 열어 같은 저장 길만 탄다) ·
    qtype·conc·twin·ansfix·maskpos·omrpos·link 의 화면 쓰기 길(합성 기록의 옮김으로만) · 물리 다음 회독(VSEEN) 화면 · 회귀 사슬(H-6 = _qa_chain compare — 이 하네스 밖) · 암기카드 창·🃏·정리·근거 쓰임·검색 면은
    함수로 열 수 있는 면만 훑는다(전수 표 「자리 · 지금 글자 · 바꾼 글자」는 앱 쪽 몫).
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT · N_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기 헬퍼(_task_qa_slim2 A-1-2 · 옛 남 하네스 import 를 갈음)
_roots.need_n('jagwa/gigu/claude_motion 재료(채팅이 만든 md · html — N: 에만)')
import io, json, os, re, sys, time, copy, hashlib, subprocess, tempfile   # noqa: E402
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE0 = _roots.genie(); SPD = _roots.spd()
ROOT = ARG('--root', '') or GENIE0
REV = ARG('--rev', '')   # NEW 를 작업트리 대신 genie 커밋에서(줄 워크트리가 아직 손질 중일 때 · git show 로 읽기만 — genie 에 쓰지 않는다)
BASE_REV = ARG('--base', '4754b1d')
FIXC = ARG('--seed', 'eb920627')
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.upper() for x in (ARG('--only', 'B,E,H') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_uid_unify_result.txt'))
MAT = _roots.n('jagwa', 'gigu', 'claude_motion')
RP = 'earth/기록.json'
ROWS = []
NUMK = ['status', 'note', 'qtype', 'conc', 'gpt', 'twin', 'ansfix', 'frm', 'maskpos', 'omrpos', 'mcard', 'link', 'txt']   # 지시서 0-3 번호 열쇠 통 + txt(칸 열쇠 「card:<번호>」 — 🃏 카드 글상자 · 지시서 0-3 「이 밖에 F.NO 를 열쇠로 남기는 자리」)
STAYK = ['bogi', 'unit', 'bpg', 'crop', 'tfix', 'gg', 'ggref', 'pick', 'bref', 'bpit', 'snote']              # 이미 uid 거나(JG_KEYS) 번호가 아닌 통(bref·bpit = 인쇄쪽) — 칸 수·값 그대로
UIDRE = re.compile(r'^[BG]\d\d-\d+-\d+$')   # 기출 uid(지시서 G-1)
ANCH = [('84', 'G03-40-05', 'E002'), ('111', 'G06-43-02', 'E004'), ('119', 'G06-43-10', 'E008'), ('149', 'G09-46-10', 'E001')]   # 지시서 0-6 표
TITLE_END = {'G09-46-10': '정답 ① ㄱ', 'G03-40-05': '정답 ② ㄱ·ㄷ', 'G06-43-02': '정답 ⑤ ㄴ·ㄷ', 'G06-43-10': '정답 ④ (옳지 않은 것)'}   # 지시서 C-1 표
MATS = {'G09-46-10': ('earth_G09-46-10.md', 2630, '3d3c533bc4222ddcf64fd05b5beb2259', '지학QA E001 · 질문일 2026-09-28', (5, 18, 6, 3, 1)),
        'G03-40-05': ('earth_G03-40-05.md', 3316, '8e508d2a3fe8761c591c41cbb9c7c8db', '지학QA E002 · 질문일 2026-09-28', (5, 17, 6, 7, 3)),
        'G06-43-02': ('earth_G06-43-02.md', 2684, '90a1d8acba83b0c7751c303943818e56', '지학QA E004 · 질문일 2026-10-01', (5, 16, 6, 8, 1)),
        'G06-43-10': ('earth_G06-43-10.md', 2382, '754ddc0b36c4887a3c6873d4d62a4532', '지학QA E008 · 질문일 2026-10-04', (5, 11, 6, 7, 1))}   # 지시서 D-2 표(파일 · 크기 · md5 · 첫 줄 · 절·글머리·|줄·굵게·Q줄)
MOTMD5 = {'G09-46-10': ('earth_149.html', 18515, 'b5f777bb61f48dd19ece62d1ecff10c9'), 'G03-40-05': ('earth_84.html', 21246, '662012de2a3bac1e23b51e1e5719f531'),
          'G06-43-02': ('earth_111.html', 28730, '3321be206c34540047ee0251d816580f'), 'G06-43-10': ('earth_119.html', 9202, '6327553947145423d69379ee50c99e7d')}   # 지시서 0-7 표
QA1 = re.compile(r'^(지학|생물)QA [EB]\d{3} · 질문일 \d{4}-\d{2}-\d{2}$')
OLDTT = re.compile(r'\d+회\s*\d+번|\d{4}년 자과 \d+번')   # 기출 「NN회 N번」(지학) · 「YYYY년 자과 N번」(생물 기출 titleOf)
WIDTHS = [1440, 900, 834, 390]


def R(eng, name, okn, okb, val):
    ROWS.append((eng, name, okn, okb, val))
    print('%s | 바탕 %s | %s · %s | %s' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[okn], {True: 'PASS', False: 'FAIL', None: '—'}[okb], eng, name,
          (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str))[:520]), flush=True)


def now_ms():
    return int(time.time() * 1000)


def canon(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def dumps(d):
    return json.dumps(d, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


def git1(repo, *a):
    return JG.git_HU(repo, *a).decode('utf-8', 'replace').strip()


# ══════════ 고정본 · 앱 · 모션 ══════════
def gshow(rel, repo=None, rev=None):
    QC.sub('git:show-data')   # 고정본(studyplandata eb920627) 읽기 — 결정적 입력 · 바탕 앱 아님(regress 에도 남음)
    return JG.git_HU(repo or SPD, 'show', '%s:%s' % (rev or FIXC, rel))


ITEMS = {s: json.loads(gshow('%s/문항.json' % s).decode('utf-8')) for s in ('earth', 'bio')}
RECB = {s: gshow('%s/기록.json' % s) for s in ('earth', 'bio', 'phys')}
RECJ = {s: json.loads(b.decode('utf-8')) for s, b in RECB.items()}
N2U = {s: {str(i + 1): r['uid'] for i, r in enumerate(ITEMS[s])} for s in ITEMS}
U2N = {s: {u: n for n, u in N2U[s].items()} for s in ITEMS}
KIND_G = {s: [r['uid'] for r in ITEMS[s] if UIDRE.match(r['uid'])] for s in ITEMS}


def app_at(root, rev=None):
    if rev:
        return JG.git_HU(root, 'show', '%s:jagwa/index.html' % rev).replace(b'\r\n', b'\n')
    return open(os.path.join(root, 'jagwa', 'index.html'), 'rb').read().replace(b'\r\n', b'\n')


def stat_at(root, rev=None):
    out = {}
    if rev:
        for f in git1(root, 'ls-tree', '--name-only', rev, 'jagwa/motion/').split():
            out['motion/' + f.split('/')[-1]] = JG.git_HU(root, 'show', '%s:%s' % (rev, f))
    else:
        d = os.path.join(root, 'jagwa', 'motion')
        for f in sorted(os.listdir(d)):
            if os.path.isfile(os.path.join(d, f)):
                out['motion/' + f] = open(os.path.join(d, f), 'rb').read()
    # 줄끝 — 작업트리(CRLF)와 git blob(LF)이 갈리므로 글 파일은 LF 로 맞춘다(앱과 같게 · 바이트 무변 맞댐도 LF 기준)
    return {k: (v.replace(b'\r\n', b'\n') if k.lower().endswith(('.html', '.json', '.js', '.css', '.md', '.txt')) else v) for k, v in out.items()}


def mat(uid):
    f = MATS[uid][0]
    return io.open(os.path.join(MAT, f), encoding='utf-8', newline='').read().replace('\r\n', '\n')


def md5(b):
    return hashlib.md5(b).hexdigest()


# ══════════ 기대값 — 고정본에서 재서 맞댄다 ══════════
def expect_mig(rec, n2u):
    """번호 열쇠 통(NUMK) 칸 → uid 로 옮긴 기대 몸통(지시서 A-2) — data · u · 새 묘비 · 비춘 묘비. 표에 없는 번호는 그대로."""
    D, U, G = rec['data'], dict(rec.get('u') or {}), dict(rec.get('gone') or {})
    out = {'data': {}, 'u': U, 'gone': G, 'moved': [], 'stay': []}
    for k, v in D.items():
        if k not in NUMK:
            out['data'][k] = v
            continue
        nv = {}
        for c, val in v.items():
            nc = newcell(k, c, n2u)
            if nc:
                if k in ('twin', 'link') and isinstance(val, list):
                    val = [n2u.get(str(x), x) for x in val]
                nv[nc] = val
                out['moved'].append((k, c, nc))
            else:
                nv[c] = val
                out['stay'].append((k, c))
        out['data'][k] = nv
    for k, c, uid in out['moved']:
        if k + '|' + c in U:
            U[k + '|' + uid] = U.pop(k + '|' + c)
    out['oldtomb'] = sorted(k + '|' + c for k, c, uid in out['moved'])
    mir = {}
    for x, t in (rec.get('gone') or {}).items():
        if '|' not in x:
            continue
        k, c = x.split('|', 1)
        nc = newcell(k, c, n2u) if k in NUMK else None
        if nc:
            kn = k + '|' + nc
            if kn not in U and kn not in (rec.get('gone') or {}) and nc not in out['data'].get(k, {}):
                mir[kn] = t
    out['mirror'] = mir
    return out


def numkey(k, c):
    """그 통의 칸 열쇠 c 가 문항 번호 열쇠인가 — txt 는 「card:<번호>」 · 나머지는 번호 글자(omrpos 「def」 같은 번호 아닌 열쇠는 아님)"""
    return re.fullmatch(r'card:[1-9]\d*', c) is not None if k == 'txt' else re.fullmatch(r'[1-9]\d*', c) is not None


def newcell(k, c, n2u):
    if k == 'txt':
        m = re.fullmatch(r'card:([1-9]\d*)', c)
        return ('card:' + n2u[m.group(1)]) if m and m.group(1) in n2u else None
    return n2u.get(c)


def hsum(st):
    return sum(len((v or {}).get('h') or []) for v in (st or {}).values())


def cell(put, k, uid, no):
    """PUT 몸통에서 한 칸 — (값, 열쇠꼴 'uid'|'번호'|None). 바탕(번호 열쇠)도 읽히게 둘 다 본다."""
    d = ((put or {}).get('data') or {}).get(k) or {}
    if uid in d:
        return d[uid], 'uid'
    if str(no) in d:
        return d[str(no)], '번호'
    return None, None


# ══════════ 기기 ══════════
class Overlay(dict):
    """명시한 사본 먼저 · 없으면 고정본 커밋의 .json 을 git 에서 바로(그림·PDF 는 SPD 작업트리) — studyplandata 에 쓰지 않는다"""
    def __init__(self, ov=None):
        super().__init__(ov or {}); self.cache = {}

    def _lazy(self, rel):
        if not rel.endswith('.json'):
            return None
        if rel not in self.cache:
            QC.sub('git:show-data')   # 고정본 json 지연 읽기(바탕 앱 아님)
            b = JG.git_HU(SPD, 'show', '%s:%s' % (FIXC, rel))
            self.cache[rel] = b if b else None
        return self.cache[rel]

    def __contains__(self, rel):
        return dict.__contains__(self, rel) or self._lazy(rel) is not None

    def __getitem__(self, rel):
        return dict.__getitem__(self, rel) if dict.__contains__(self, rel) else self._lazy(rel)


OKURL = ('http://127.0.0.1', 'https://cdnjs.cloudflare.com/', 'https://cdn.jsdelivr.net/', 'https://fonts.googleapis.com/', 'https://fonts.gstatic.com/', 'blob:', 'data:')

UJS = r"""
window.__U={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 ws:s=>String(s).replace(/\s+/g,' ').trim(),
 vis(e){return !!e&&e.isConnected&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0},
 async settle(path,n){const sl=ms=>new Promise(r=>setTimeout(r,ms));
   for(let i=0;i<(n||2);i++){for(let k=0;k<80&&typeof recBusy!=='undefined'&&recBusy;k++)await sl(100);
     try{await syncRecords(true)}catch(e){return 'ERR '+e}await sl(500)}return (window.__PUTS||[]).length},
 keys(){return SYNC_KEYS.slice()},
 cnt2(){return {jg:window.__JGMIG||0,uid:window.__UIDMIG||0,guard:window.__UIDGUARD||0,ink:window.__UIDINK||0}},
 rows(){const o={};document.querySelectorAll('#list .item').forEach((d,i)=>{const c=d.cloneNode(true);
    c.querySelectorAll('.meta .sub').forEach(x=>x.remove());
    c.querySelectorAll('.meta .tag').forEach(x=>{if(/^\s*\d+회독\s*$/.test(x.textContent))x.remove()});
    c.querySelectorAll('canvas').forEach(x=>x.remove());
    c.querySelectorAll('.ewmt').forEach(x=>x.remove());   /* ★ 묶음(add1 시험 틀림 태그)은 이 칸 몫 아님 — JG2 가 잼 */
    o[d.dataset.uid||('#'+i)]=__U.ws(c.outerHTML)});return o},
 drawer(){const o={};document.querySelectorAll('#ndList .ndrow').forEach(d=>{const r=DATA[+d.dataset.no-1];const c=d.cloneNode(true);
    c.querySelectorAll('.ndt,.ndm,.ndno,.ewmt').forEach(x=>x.remove());c.removeAttribute('data-no');c.removeAttribute('data-sec');/* ★ 2026-10-07 (_task_jagwa_phys_win §A-06) — 시안 ③ 서랍 단원 접기: 줄마다 data-sec(단원 열쇠) · 바탕 4754b1d 엔 없다 */   /* ★ .ewmt = 묶음 add1 태그(JG2 몫) */c.querySelectorAll('[data-nc]').forEach(x=>x.removeAttribute('data-nc'));o[r?r[F.CODE]:('#'+d.dataset.no)]=__U.ws(c.outerHTML)});return o},
 heat(){return [...document.querySelectorAll('#spec i')].map(i=>(i.className||'')+'|'+(i.title||''))},
 cnt(){return ['c0','cO','cQ','cX','cP','cWk','cW'].map(i=>{const e=document.getElementById(i);return e?e.textContent:null})},
 screen(){return {rows:__U.rows(),drawer:__U.drawer(),heat:__U.heat(),cnt:__U.cnt()}},
 gpTags(){return [...document.querySelectorAll('#list .item')].filter(d=>d.querySelector('.tag.gp')).map(d=>d.dataset.uid||'').sort()},
 noOf(uid){const r=DATA.find(x=>x[F.CODE]===uid);return r?r[F.NO]:0},
 async openRow(uid){const no=__U.noOf(uid);try{closeView()}catch(e){}await new Promise(r=>setTimeout(r,150));await openView(no);await new Promise(r=>setTimeout(r,1200));return no},
 sheet(){const s=[...document.querySelectorAll('.sheet')].pop();if(!s)return null;const p=s.querySelector('.panel');
   const h2=p&&[...p.children].find(x=>x.tagName==='H2');const pp=p&&[...p.children].find(x=>x.tagName==='P');const rd=s.querySelector('.gpread');
   const mot=s.querySelector('#gpMot');const cs=e=>e?getComputedStyle(e):null;const pc=cs(pp),mc=cs(mot);
   const g1=rd?rd.querySelector('p.gpp'):null;
   return {h2:__U.tx(h2),p:__U.tx(pp),pspans:pp?[...pp.children].filter(x=>x.tagName==='SPAN').map(__U.tx):[],pdisp:pc?[pc.display,pc.alignItems,pc.columnGap||pc.gap]:null,
     motTx:__U.vis(mot)?__U.tx(mot):'',motInP:!!(pp&&mot&&pp.contains(mot)),motBar:!!s.querySelector('#gpMotBar'),motBarVis:__U.vis(s.querySelector('#gpMotBar')),
     motSt:mc?{bw:mc.borderTopWidth,pad:mc.paddingTop+'/'+mc.paddingLeft,fs:mc.fontSize,ml:mc.marginLeft,bg:mc.backgroundColor,bi:mc.backgroundImage}:null,
     read:!!rd,edit:!!s.querySelector('#gpIn'),
     h3:rd?[...rd.querySelectorAll('h3.gph')].map(__U.tx):[],li:rd?rd.querySelectorAll('ul.gpul li').length:0,ol:rd?rd.querySelectorAll('ol.gpol li').length:0,
     tb:rd?rd.querySelectorAll('table.gptb').length:0,th:rd?rd.querySelectorAll('table.gptb th').length:0,tr:rd?rd.querySelectorAll('table.gptb tbody tr').length:0,
     b:rd?rd.querySelectorAll('b').length:0,script:rd?rd.querySelectorAll('script').length:0,
     p1:g1?g1.innerHTML:'',p1tx:g1?g1.innerText:'',text:rd?rd.textContent:'',nGpp:rd?rd.querySelectorAll('p.gpp').length:0}},
 closeSheets(){document.querySelectorAll('.sheet').forEach(x=>x.remove())},
 async frame(){const f=document.getElementById('gpMotFrame');if(!f)return null;
   for(let i=0;i<60;i++){try{const d=f.contentDocument;if(d&&d.readyState==='complete'&&d.body&&d.body.children.length)break}catch(e){}await new Promise(r=>setTimeout(r,150))}
   await new Promise(r=>setTimeout(r,400));
   let d=null;try{d=f.contentDocument}catch(e){return {src:f.getAttribute('src'),same:false}}
   if(!d)return {src:f.getAttribute('src'),same:false};
   const st=await fetch(f.getAttribute('src'),{cache:'no-store'}).then(r=>r.status).catch(()=>0);
   const r=f.getBoundingClientRect();const sh=[...document.querySelectorAll('.sheet')].pop();const pn=sh&&sh.querySelector('.panel');const pp=pn&&[...pn.children].find(x=>x.tagName==='P');const pr=pp?pp.getBoundingClientRect():null;
   return {src:f.getAttribute('src'),status:st,same:new URL(f.src,location.href).origin===location.origin,h:Math.round(r.height),top:Math.round(r.top),belowP:pr?(r.top>=pr.bottom-1):null,
     canvas:d.querySelectorAll('canvas').length,svg:d.querySelectorAll('svg#fig').length,text:d.body?d.body.textContent.length:0}},
 stores(keys){const o={};keys.forEach(k=>{const v=SYNC_REF[k]?SYNC_REF[k].g():undefined;o[k]=v?JSON.parse(JSON.stringify(v)):null});return o},
 async idb(keys){const o={};for(const k of keys){try{o[k]=await get('kv',k)}catch(e){o[k]='ERR '+e}}return o},
 async inkKeys(){try{return (await keys('ink')).map(String)}catch(e){return []}},
 snap(){const g=s=>document.querySelector(s);const c=g('#card');
   return {vno:typeof VNO!=='undefined'?VNO:null,vT1:__U.tx(g('#vT1')),open:!!g('#view')&&!g('#view').classList.contains('hide'),
     pick:c?[...c.querySelectorAll('.choices button.pick')].map(b=>b.dataset.c):[],
     bogiOn:c?[...c.querySelectorAll('.bogi .row .ox button.on')].map(b=>b.closest('.row').dataset.k+b.dataset.v):[],
     nOx:c?c.querySelectorAll('.bogi .row .ox button').length:0,
     mkOn:['mO','mQ','mX','mP'].filter(i=>g('#'+i)&&g('#'+i).classList.contains('on')).map(i=>i.slice(1)),
     vmOn:c?[...c.querySelectorAll('.vrow [data-vmark].on')].map(b=>b.dataset.vmark):[],
     cmark:c&&c.querySelector('.cmark')?c.querySelector('.cmark').textContent.replace(/\s+/g,' ').trim():null,
     cmeta:c&&c.querySelector('.cmeta')?c.querySelector('.cmeta').textContent.replace(/\s+/g,' ').trim():'',
     layer:g('#tLayer')?g('#tLayer').value:null,layerOpts:g('#tLayer')?[...g('#tLayer').options].map(o=>o.value):[],eye:g('#tLayerEye')?g('#tLayerEye').classList.contains('on'):null,
     tHist:__U.tx(g('#tHist'))}}
};
"""


class Dev2(JG.Dev):
    """기기 하나 — 창 크기 · 손가락 여부를 고를 수 있는 HU.Dev(고정본 json 은 git 에서 · blob 도 통과)"""
    def __init__(self, br, eng, vp=(1280, 900), touch=False):
        self.eng = eng; self.S = JG.Srv(); self.vp = vp; self.touch = touch
        self.ctx = br.new_context(viewport={'width': vp[0], 'height': vp[1]}, device_scale_factor=1, has_touch=touch)
        self.ctx.route('**/*', lambda rt: rt.continue_() if rt.request.url.startswith(OKURL) else rt.abort())
        self.pg = None; self.errs = []; self.cerr = []; self.cdp = None

    def load(self, app, subj, rec=None, static=None):
        QC.launch('base' if (APPS.get('BASE') and app is APPS['BASE'][0] and app is not APPS['NEW'][0]) else 'new')
        self.S.app = app; self.S.spd = SPD
        self.S.rec = Overlay(rec or {}); self.S.static = dict(static or {})
        if self.pg:
            self.pg.close()
        self.ctx.clear_cookies()
        self.pg = self.ctx.new_page(); self.pg.set_default_timeout(25000)   # 행동(locator·click) 시간 제한 — 부팅 기다림은 아래 wait_for_function 이 따로 120초
        self.errs = []; self.cerr = []; self.cdp = None
        self.pg.add_init_script(JG.INIT_HU.replace('__SUBJ__', subj))
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:200]))
        self.pg.on('console', lambda m: self.cerr.append('%s @%s' % (m.text[:200], ((m.location or {}).get('url') or '')[-48:])) if m.type == 'error' else None)
        self.pg.goto('http://127.0.0.1:%d/app.html' % self.S.port, wait_until='load')
        self.pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=120000)
        if subj in ('earth', 'bio'):   # 인라인 물리 DATA(577행)가 먼저 보인다 — 진짜 문항 수가 될 때까지
            try:
                nexp = len(json.loads(self.S.rec['%s/문항.json' % subj].decode('utf-8')))
                self.pg.wait_for_function('DATA.length===%d' % nexp, timeout=120000)
            except Exception as e:
                self.errs.append('boot wait: ' + repr(e)[:120])
        self.pg.evaluate(JG.JS_HU); self.pg.evaluate(UJS)
        for _ in range(120):
            if self.ev("()=>__J.ready()"):
                break
            self.pg.wait_for_timeout(250)
        self.pg.wait_for_timeout(2500)

    def set_rec(self, path, b):
        self.S.rec[path] = b

    def settle(self, path=RP, n=2):
        """동기화를 마친 뒤 마지막 PUT 몸통(파싱) — 앱이 올린 그대로(원격 사본 밖으로 안 나감)"""
        self.ev("p=>__U.settle(p,%d)" % n, path)
        t = self.ev("p=>__J.lastPut(p)", path)
        return json.loads(t) if t else None

    def putraw(self, path=RP):
        return self.ev("p=>__J.lastPut(p)", path)

    def click(self, sel, finger=False, nth=0):
        """그 요소 한가운데를 진짜 누른다(마우스 · 손가락) — 가운데로 굴려 오고, 누를 자리 맨 위가 그 요소가 아니면(가려짐) self.covers 에 남긴다"""
        if not self.ev("a=>{const e=document.querySelectorAll(a[0])[a[1]];if(!e)return false;e.scrollIntoView({block:'center',inline:'nearest'});return true}", [sel, nth]):
            return False
        self.pg.wait_for_timeout(220)
        r = self.ev("a=>{const e=document.querySelectorAll(a[0])[a[1]];if(!e)return null;const b=e.getBoundingClientRect();"
                    "if(b.width<=0||b.height<=0)return null;const cx=b.x+b.width/2,cy=b.y+b.height/2;const t=document.elementFromPoint(cx,cy);"
                    "return {x:cx,y:cy,ok:!!t&&(t===e||e.contains(t)||t.contains(e)),top:t?(t.tagName+'#'+t.id+'.'+String(t.className).slice(0,30)):null}}", [sel, nth])
        if not r:
            return False
        if not r['ok']:
            self.covers = getattr(self, 'covers', []) + [(sel, r['top'])]
        self.tap(r['x'], r['y'], finger)
        return True

    def probe(self, sel, nth=0):
        """굴려 오고(220ms 쉼) 한가운데 맨 위 요소가 그 요소(또는 안·밖)인지 — 안 눌러 본다"""
        self.ev("a=>{const e=document.querySelectorAll(a[0])[a[1]];if(e)e.scrollIntoView({block:'center',inline:'nearest'})}", [sel, nth])
        self.pg.wait_for_timeout(220)
        return self.ev("a=>{const e=document.querySelectorAll(a[0])[a[1]];if(!e)return null;const b=e.getBoundingClientRect();if(b.width<=0||b.height<=0)return null;"
                       "const t=document.elementFromPoint(b.x+b.width/2,b.y+b.height/2);return {ok:!!t&&(t===e||e.contains(t)||t.contains(e)),top:t?(t.tagName+'#'+t.id+'.'+String(t.className).slice(0,30)):null}}", [sel, nth])

    def tap(self, x, y, finger=False):
        if finger and self.touch:
            if self.eng == 'chromium':
                if not self.cdp:
                    self.cdp = self.ctx.new_cdp_session(self.pg)
                # 폰 손가락 = 접촉 반지름 10px(폰 손끝 · 20px 지름). 반지름 22(아이패드 손가락)는 폰 390 에서 카드가 0.5배로 줄어 선택지 단추가 40×15px 라 바탕에서도 톡이 안 먹는다(실측 10/4 — 앱의 필기 덮개 뚫기 판정)
                self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'radiusX': 10, 'radiusY': 10, 'id': 1}]})
                self.pg.wait_for_timeout(70)
                self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
            else:
                self.pg.touchscreen.tap(x, y)
        else:
            self.pg.mouse.click(x, y)
        self.pg.wait_for_timeout(550)


# ══════════ 관찰 · 판정 틀 ══════════
APPS = {}
IDENT = {}
_cache = {}
EXP_E = expect_mig(RECJ['earth'], N2U['earth'])
UIDSET_E = set(N2U['earth'].values())


def OBS(name, fn, br, eng, who, *a, **k):
    """한 시나리오를 (엔진 · 판)마다 한 번만 돈다 — NEW 와 BASE 가 앱·모션까지 같으면 같은 관찰을 두 칸에 쓴다"""
    if QC.REGRESS and who != 'NEW':   # regress — 바탕(4754b1d) 시나리오 0 · GATE 의 「바탕」 칸 = —(헛잣대 · 판정 밖) · GATE2 = 기준 스냅샷(_rg_gate2)
        return None
    key = (name, eng, IDENT[who], repr(a), repr(sorted(k.items())))
    if key not in _cache:
        app, stat = APPS[who]
        t0 = time.time()
        try:
            _cache[key] = fn(br, eng, app, stat, *a, **k)
        except Exception as e:
            import traceback
            _cache[key] = {'__err': repr(e)[:300] + ' @' + traceback.format_exc().strip().split('\n')[-3][:160]}
        print('   · %s %s [%s] %.0f초%s' % (eng, name, who, time.time() - t0, (' ERR ' + _cache[key]['__err']) if '__err' in _cache[key] else ''), flush=True)
    return _cache[key]


def _run(jf, *O):
    if any(o is None for o in O):
        return None, '관찰 없음'
    for o in O:
        if '__err' in o:
            return False, 'ERR ' + o['__err']
    try:
        r = jf(*O)
        return (None if r[0] is None else bool(r[0])), r[1]
    except Exception as e:
        import traceback
        return False, 'judge ERR ' + repr(e)[:200] + ' @' + traceback.format_exc().strip().split('\n')[-3][:140]


def GATE(eng, name, jf, ON, OB):
    """NEW(ON) 와 바탕(OB)에 같은 판정 함수를 댄다 — OB 가 None 이면 바탕 칸 —"""
    okn, dn = _run(jf, ON)
    okb = None
    if OB is not None:
        okb, db = _run(jf, OB)
        if okb is not None and okb != okn:
            dn = (dn if isinstance(dn, str) else json.dumps(dn, ensure_ascii=False, default=str))
    R(eng, name, okn, okb, dn)
    return okn, okb


def GATE2(eng, name, jf, ON, OB, show_base=False):
    """NEW ↔ BASE 맞대기 — 바탕 칸 — (바탕끼리 맞대면 거저 참)"""
    if QC.REGRESS:   # regress — 바탕(OB) 대신 기준 스냅샷(앞 인도판 같은 칸 관찰의 투영 · _rg_gate2)
        return _rg_gate2(eng, name, jf, ON)
    okn, dn = _run(jf, ON, OB)
    R(eng, name, okn, None, dn)
    return okn


# ── _task_qa_slim2 A-1·A-2(10/8 · J2) regress 갈래 — 이름이 `_rg` · `_RG` 로 시작하는 것 = gate 에서 안 쓰는 도우미(gate 에서 도는 줄은 글자 그대로) ──
#   regress = NEW 시나리오만(바탕 4754b1d 앱·모션 풀기 · 바탕 시나리오 0 — OBS) · 옛 판 기기 흉내(olddev · mix · Eold) · 헛잣대 셈(B-7 · E-6 · H-5) · S-6 [BASE] = gate 만
#   GATE2(NEW ↔ 바탕 맞대기 · 처리안 「기준」) = 앞 인도판 같은 칸 관찰의 투영(QC.base) 과 맞댐 — 판정 함수는 그대로 · 두 쪽에 같은 투영(같음 ⟺ 같음 · 긴 글은 md5)
#   smoke = chromium 한 번 — B-1 셈 무변(동기화 한 바퀴 · 두 번째 열기 없음) · E-1 창 제목(첫 uid 하나 · 모션 · 이웃 문항 건넘)
#   고정 대기는 그대로(까닭 = out/a2/J2/_harness_jagwa_uid_unify_표지.md — 문항 바꿈 뒤 showProblem 이 문항 창(sh-gpt …)을 닫는 비동기 · 부팅 뒤 옮김 끝 표지 없음)
def _rg_md5(s):
    return hashlib.md5(('' if s is None else (s if isinstance(s, str) else canon(s))).encode('utf-8')).hexdigest()


def _rg_proj_screen(O):   # j_screen_eq — 목록·서랍 줄 글 = md5(같음 ⟺ 같음) · 히트맵 · 카운터 그대로
    s = O['screen']
    return {'screen': {'rows': {k: _rg_md5(v) for k, v in s['rows'].items()}, 'drawer': {k: _rg_md5(v) for k, v in s['drawer'].items()}, 'heat': s['heat'], 'cnt': s['cnt']}}


def _rg_proj_phys_body(O):   # j_phys_body — nok(data) · u(gg 도장 뺌) · gone 의 canon md5(판정 함수가 두 쪽에 같은 거름을 다시 걸어도 그대로)
    p = O['put'] or {}
    return {'put': {'data': {'md5': _rg_md5(canon(nok(p.get('data'))))}, 'u': {'md5': _rg_md5(canon({k: v for k, v in (p.get('u') or {}).items() if not k.startswith('gg|')}))},
                    'gone': {'md5': _rg_md5(canon(p.get('gone') or {}))}}, 'keys': O.get('keys')}


def _rg_proj_phys_screen(O):   # j_phys_screen — 30 줄 표본 글 그대로(뜻한 차 거름 _b6_norm 이 글에 걸린다)
    return {'list': O['list'], 'drawer': O['drawer'], 'cnt': O['cnt']}


def _rg_proj_E5(O):   # j_E5 — 창 DOM 글 md5 · 제목 · 모션 줄 · iframe src·200
    sk = ('h2', 'motBar', 'motBarVis', 'motTx')
    return {'wins': {no: {'html': _rg_md5(w.get('html')), 'sheet': ({k: w['sheet'].get(k) for k in sk} if w.get('sheet') else None),
                          'frame': ({k: w['frame'].get(k) for k in ('src', 'status')} if w.get('frame') else None)} for no, w in O['wins'].items()}}


def _rg_proj_sweep(O):   # j_sweep — 면마다 넘침·잘림·겹침·가려짐 신호 · 가로 굴림 · 작은 누름
    return {s: ({k: O[s].get(k) for k in ('over', 'clip', 'ovl', 'cov', 'small', 'hscroll')} if O.get(s) else O.get(s)) for s in ('first', 'card', 'claude', 'claude+mot')}


_RG_PROJ = {'j_screen_eq': _rg_proj_screen, 'j_phys_body': _rg_proj_phys_body, 'j_phys_screen': _rg_proj_phys_screen, 'j_E5': _rg_proj_E5,
            'j_H1_ec': lambda O: {'ec': O.get('ec')}, 'j_H2_phys': lambda O: {'chips': O.get('chips')}, 'j_sweep': _rg_proj_sweep}
_RG_POST = {'j_E5': lambda b: {'wins': {int(k): v for k, v in (b.get('wins') or {}).items()}} if isinstance(b, dict) else b}   # JSON 왕복이 창 번호 열쇠를 글자로 바꾼다 → 판정 함수가 읽는 수 열쇠로


def _rg_gate2(eng, name, jf, ON):
    """regress — GATE2 의 바탕(OB) = 기준 스냅샷(앞 인도판 같은 칸 관찰의 투영 · QC.base) · 스냅샷이 없으면 새 판 값 자신(첫 기록) · 판정 함수 그대로"""
    if not isinstance(ON, dict) or '__err' in ON:
        okn, dn = _run(jf, ON, ON)
        R(eng, name, okn, None, dn)
        return okn
    cid = '%s@%s' % (name.split(' — ')[0], eng)
    post = _RG_POST.get(jf.__name__, lambda b: b)
    try:
        pn = _RG_PROJ[jf.__name__](ON)
    except Exception as e:
        R(eng, name, False, None, 'regress 투영 ERR ' + repr(e)[:200])
        return False
    pb = post(QC.base(cid, pn))
    okn, dn = _run(jf, post(QC.norm(pn)), pb)
    if isinstance(dn, dict):
        dn = dict(dn, 기준=QC.base_note(cid))
    R(eng, name, okn, None, dn)
    return okn


# ══════════ B 시나리오 ══════════
def tomb_expect(put, exp, T0, T1):
    g = put.get('gone') or {}
    t0, t1 = T0 - 120000, T1 + 120000
    miss_old = [x for x in exp['oldtomb'] if x not in g or not (t0 <= g[x] <= t1)]
    keep = [x for x, v in exp['gone'].items() if g.get(x) != v]
    miss_mir = [x for x, v in exp['mirror'].items() if g.get(x) != v]
    extra = sorted(set(g) - set(exp['gone']) - set(exp['oldtomb']) - set(exp['mirror']))
    return miss_old, keep, miss_mir, extra


def sc_main(br, eng, app, stat, recb=None, subj='earth', second=True, prior_old=False):
    """지학 원격 사본(고정본)을 실은 빈 기기 — 열고 동기화 뒤: 올린 몸통 · 도장·묘비 · 메모리 통 · 화면 · bak_uid · (두 번째 열기)"""
    recb = recb if recb is not None else RECB[subj]
    path = '%s/기록.json' % subj
    dv = Dev2(br, eng)
    try:
        if prior_old:   # 옛 판(바탕)으로 먼저 열어 옛 기록을 로컬에 받아 둔다 — 새 판은 그 로컬을 「열 때」 옮긴다
            dv.load(APPS['BASE'][0], subj, rec={path: recb}, static=APPS['BASE'][1]); dv.settle(path)
        T0 = now_ms()
        dv.load(app, subj, rec={path: recb}, static=stat)
        put1 = dv.settle(path); raw1 = dv.putraw(path)
        T1 = now_ms()
        keys = dv.ev("()=>__U.keys()")
        O = {'T0': T0, 'T1': T1, 'put': put1, 'keys': keys, 'stores': dv.ev("k=>__U.stores(k)", keys), 'u': dv.ev("()=>__J.u()"), 'gone': dv.ev("()=>__J.gone()"),
             'screen': dv.ev("()=>__U.screen()"), 'bak': dv.ev("async()=>{const v=await get('kv','bak_uid');return v?JSON.stringify(v):null}"),
             'mig': dv.ev("()=>__J.mig()"), 'cnt': dv.ev("()=>__U.cnt2()"), 'errs': dv.errs[:4], 'cerr': list(dv.cerr)[:4],
             'shadow': dv.ev("()=>{try{return JSON.parse(localStorage.getItem(SHADOW_KEY)||'{}')}catch(e){return {}}}"),
             'idb': dv.ev("k=>__U.idb(k)", [k for k in keys if k in NUMK + STAYK]), 'ink': dv.ev("()=>__U.inkKeys()")}
        if second and raw1:
            dv.load(app, subj, rec={path: raw1.encode('utf-8')}, static=stat)
            put2 = dv.settle(path)
            O['second'] = {'put': put2, 'bak': dv.ev("async()=>{const v=await get('kv','bak_uid');return v?JSON.stringify(v):null}"), 'mig': dv.ev("()=>__J.mig()"), 'cnt': dv.ev("()=>__U.cnt2()"),
                           'errs': dv.errs[:4]}
        return O
    finally:
        dv.close()


def syn_rec():
    """합성 기록 — 고정본에 번호 열쇠 칸(note · qtype · conc · twin · ansfix · maskpos · omrpos)을 더한 사본(도장도 같이) — 값 속 번호(twin)와 나머지 통의 옮김을 본다"""
    d = json.loads(RECB['earth'].decode('utf-8'))
    D, U = d['data'], d['u']
    add = [('note', '84', '검산 코멘트 84'), ('note', '296', '검산 코멘트 296'), ('note', '13', '검산 코멘트 13'),
           ('qtype', '84', ['계산', '함정']), ('conc', '111', ['검산개념']), ('twin', '84', [111]), ('twin', '111', [84]), ('ansfix', '84', '②'),
           ('txt', 'card:84', [{'x': 0.1, 'y': 0.2, 't': '검산 글상자'}]), ('txt', 'q:G03-40-05', [{'x': 0.3, 'y': 0.4, 't': '이미 uid 열쇠'}]),
           ('maskpos', '84', {'u': 0.1, 'v': 0.2, 'w': 0.3, 'h': 0.1}), ('omrpos', '84', {'u': 0.5, 'v': 0.6}), ('omrpos', 'def', {'u': 0.7, 'v': 0.8})]
    for i, (k, c, v) in enumerate(add):
        D.setdefault(k, {})[c] = v
        U['%s|%s' % (k, c)] = 1790000000000 + i * 1000
    return d


def sc_syn(br, eng, app, stat):
    d = syn_rec()
    return dict(sc_main(br, eng, app, stat, recb=dumps(d), second=False), rec=d)


# ── 판정 ──
def j_B1_count(O):
    put = O['put']; D = put['data']; F = RECJ['earth']['data']
    fc = {k: len(F.get(k) or {}) for k in NUMK + STAYK}
    pc = {k: len(D.get(k) or {}) for k in NUMK + STAYK}
    st = D.get('status') or {}
    ok = pc == fc and hsum(st) == hsum(F['status'])
    return ok, {'칸수(올린)': {k: v for k, v in pc.items() if v or fc[k]}, '고정본': {k: v for k, v in fc.items() if v}, 'status': len(st), 'h합': hsum(st), 'gpt': pc['gpt'], 'mcard': pc['mcard']}


def j_B1_keys(O):
    D = O['put']['data']
    bad = [(k, c) for k in NUMK for c in (D.get(k) or {}) if numkey(k, c)]
    mem = O['stores']
    badm = [(k, c) for k in NUMK for c in (mem.get(k) or {}) if numkey(k, c)]
    idb = O['idb']
    badi = [(k, c) for k in NUMK for c in ((idb.get(k) if isinstance(idb.get(k), dict) else {}) or {}) if numkey(k, c)]
    return not bad and not badi, {'번호 열쇠(올린 몸통)': bad[:6], '수': len(bad), 'IndexedDB kv(저장)': len(badi), '메모리 통(참고 · 설계 몫)': len(badm)}


def j_B1_mem(O):
    D = O['put']['data']; mem = O['stores']
    bad = [k for k in NUMK if k in mem and mem[k] is not None and canon(mem[k]) != canon(D.get(k) or {})]
    return None, {'올린 몸통과 메모리 통이 다른 칸(참고 — 메모리 dict 를 uid 로 두는 것은 권고 · 설계는 Code 몫)': bad}


def j_B1_stay(O):
    D = O['put']['data']; F = RECJ['earth']['data']
    bad = [k for k in STAYK if k in F and canon(D.get(k) or {}) != canon(F[k])]
    badn = [k for k in STAYK if k not in F and (D.get(k) or {})]
    return not bad and not badn, {'다른 칸': bad, '고정본에 없는데 생김': badn, '비교한 칸': [k for k in STAYK if k in F]}


def j_B2_gpt(O):
    D = O['put']['data']; G = D.get('gpt') or {}; F = RECJ['earth']['data']['gpt']
    want = {u: F[n] for n, u, _ in ANCH}
    ok = set(G) == set(want) and all(G.get(u) == t for u, t in want.items()) and all(t.startswith(u + ' ·') for u, t in G.items())
    return ok, {'gpt 열쇠': sorted(G), '글 같음': {u: G.get(u) == t for u, t in want.items()}, '글이 그 uid 로 시작': {u: (t or '').startswith(u + ' ·') for u, t in G.items()}}


def j_B2_h(O):
    D = O['put']['data']; U = O['put']['u']; F = RECJ['earth']
    st = D.get('status') or {}
    bad = []
    for n, v in F['data']['status'].items():
        uid = N2U['earth'][n]
        if canon((st.get(uid) or {}).get('h')) != canon(v.get('h')):
            bad.append(n)
    badu = [k for k, v in EXP_E['u'].items() if k.split('|')[0] in ('status', 'gpt', 'mcard') and U.get(k) != v]
    return not bad and not badu, {'h 다른 문항(옛 번호)': bad[:6], '수': len(bad), '도장 안 맞은 칸': badu[:5], '도장 칸 수': len(badu), 'u 개수': [len(U), len(EXP_E['u'])]}


def j_B2_tomb(O):
    put = O['put']
    mo, keep, mm, extra = tomb_expect(put, EXP_E, O['T0'], O['T1'])
    oldu = [x for x in EXP_E['oldtomb'] if x in (put.get('u') or {})]
    ok = not mo and not keep and not mm and not extra and not oldu and len(EXP_E['oldtomb']) > 0
    return ok, {'옛 칸 묘비 기대': len(EXP_E['oldtomb']), '빠짐': mo[:4], '원래 묘비 바뀜': keep[:3], '비춤 기대': list(EXP_E['mirror'])[:2], '비춤 빠짐': mm[:2], '늘어난 묘비': extra[:5], '옛 도장 남음': oldu[:3]}


def j_B2_h_stamp(O):
    """status 도장 = 그 칸 h 끝 t(stTime) — 새로 안 찍는다(옛 칸 도장 그대로)"""
    put = O['put']; bad = []
    for k, v in (put['data'].get('status') or {}).items():
        t = ((v.get('h') or [{}])[-1].get('t') or 0)
        if (put['u'] or {}).get('status|' + k) not in (t, None) and k in UIDSET_E:
            bad.append(k)
    return not bad, {'도장 ≠ h 끝 t': bad[:5]}


def j_anchor_table(O=None):
    ok = all(N2U['earth'].get(n) == u for n, u, _ in ANCH)
    return ok, {'번호→uid': {n: N2U['earth'].get(n) for n, _, _ in ANCH}, '지시서 표': {n: u for n, u, _ in ANCH}}


def j_screen_eq(ON, OB):
    a, b = ON['screen'], OB['screen']
    diff = {k: [x for x in a['rows'] if a['rows'].get(x) != b['rows'].get(x)] for k in ('rows',)}
    dd = [x for x in set(a['drawer']) | set(b['drawer']) if a['drawer'].get(x) != b['drawer'].get(x)]
    hd = [i for i, (x, y) in enumerate(zip(a['heat'], b['heat'])) if x != y]
    ok = a['rows'] == b['rows'] and a['drawer'] == b['drawer'] and a['heat'] == b['heat'] and a['cnt'] == b['cnt'] and len(a['rows']) > 0
    return ok, {'목록 줄': len(a['rows']), '다른 줄': diff['rows'][:3], '서랍 줄': len(a['drawer']), '다른 서랍 줄': dd[:3], '히트맵 칸': len(a['heat']), '다른 칸': hd[:3],
                '카운터': [a['cnt'], b['cnt']], '고르게 50줄': 50 if len(a['rows']) >= 50 else len(a['rows'])}


def j_syn_mig(O):
    put = O['put']; d = O['rec']; exp = expect_mig(d, N2U['earth'])
    D = put['data']
    REQ = ('status', 'note', 'qtype', 'conc', 'gpt', 'twin', 'ansfix', 'mcard', 'txt')   # 카드 층이 쓰는 통 — frm(열쇠 「절제목|공식」)·maskpos·omrpos(PDF 뷰어)·link(물리)는 참고
    bad = [k for k in REQ if canon(D.get(k) or {}) != canon(exp['data'].get(k) or {})]
    badu = [k for k, v in exp['u'].items() if k.split('|')[0] in REQ and (put['u'] or {}).get(k) != v]   # 번호 열쇠 통 도장만(gg 같은 옛 통의 도장 갱신은 이 판 몫이 아니다)
    oldu = [x for x in exp['oldtomb'] if x.split('|')[0] in REQ and x in (put['u'] or {})]
    mo, keep, mm, extra = tomb_expect(put, exp, O['T0'], O['T1'])
    mo = [x for x in mo if x.split('|')[0] in REQ]; extra = [x for x in extra if x.split('|')[0] in REQ or True]
    skip_ok = all(D.get(k, {}).get(c) == d['data'][k][c] for k, c in exp['stay'] if k in ('omrpos',))   # 'def' 같은 번호 아닌 열쇠는 그대로
    det = {'다른 통': bad, '도장 안 맞음': badu[:4], '옛 도장 남음': oldu[:3], '묘비 빠짐': mo[:3], '늘어난 묘비': extra[:4], '옮긴 칸': len(exp['moved']), '그대로 둔 칸': exp['stay'][:3],
           'twin': D.get('twin'), 'note 열쇠': sorted((D.get('note') or {}))}
    return not bad and not badu and not oldu and not mo and not extra and skip_ok, det


def j_syn_info(O):
    D = O['put']['data']
    return None, {'maskpos': sorted((D.get('maskpos') or {})), 'omrpos': sorted((D.get('omrpos') or {})), 'ansfix': sorted((D.get('ansfix') or {})), 'qtype': sorted((D.get('qtype') or {})),
                  'conc': sorted((D.get('conc') or {}))}


def j_idem(O):
    s = O.get('second')
    if not s:
        return False, '두 번째 열기 관찰 없음'
    a, b = O['put'], s['put']
    same = canon(a['data']) == canon(b['data']) and canon(a['u']) == canon(b['u']) and canon(a['gone']) == canon(b['gone'])
    bakok = (O['bak'] == s['bak'])
    c2 = s.get('cnt') or {}
    zero = not c2.get('uid') and not c2.get('guard')   # 새 페이지(두 번째 열기)의 옮김·가드 카운터 = 0
    return same and bakok and zero, {'두 번째 열기 옮김·가드 카운터(uid·guard)': [c2.get('uid', 0), c2.get('guard', 0)], 'data·u·gone 같음': same, 'gone 개수': [len(a['gone']), len(b['gone'])], 'u 개수': [len(a['u']), len(b['u'])], 'bak_uid 같음(두 번째에 안 찍음)': bakok,
                          '옮김 수(이 앱 카운터)': [O['mig'], s['mig']]}


def j_bak(O):
    if not O['bak']:
        return False, 'bak_uid 없음(처음 옮길 때 한 번 찍는다 — IndexedDB kv.bak_uid)'
    b = json.loads(O['bak']); txt = O['bak']
    t14 = RECJ['earth']['data']['status']['14']['h'][0]['t']
    has_u = isinstance(b.get('u'), dict) and isinstance(b.get('gone'), dict)
    has_old = str(t14) in txt   # 옮기기 전 사본 = 번호 열쇠 그대로 · 옛 칸 status 14 의 h 끝 t
    return bool(isinstance(b.get('at'), (int, float)) and has_u and has_old), {'키': sorted(b.keys())[:12], 'at': b.get('at'), '옛 값(status 14) 들어 있음': has_old, 'u·gone 있음': has_u, '크기': len(txt)}


def j_B2_shadow(O):
    """그림자(shadow · 기기 localStorage) — 번호 열쇠 통도 옛 칸 값을 그대로 새 열쇠로(새로 안 찍음) · 번호 열쇠 0"""
    sh = O['shadow'] or {}; D = O['put']['data']
    bad = [(k, c) for k in NUMK for c in (sh.get(k) or {}) if numkey(k, c)]
    diff = [k for k in NUMK if set((sh.get(k) or {})) != set(D.get(k) or {})]
    return not bad and not diff, {'shadow 번호 열쇠': bad[:4], '수': len(bad), '올린 몸통과 열쇠가 다른 통': diff}


def fake_item():
    it = copy.deepcopy(ITEMS['earth'][0])
    it.update({'uid': 'G99-99-99', '옛uid': 'G99-99', '유형': '기출', '회차': '99', '연도': '2099', '문번': '1', '문항': '검산용 가짜 문항 — 문항.json 앞에 끼운 한 줄', '정답': '1'})
    return it


def sc_order(br, eng, app, stat):
    """B-4 — 문항.json 사본 앞쪽에 가짜 문항 하나를 끼워 route 로 먹이고 다시 연다(앱은 문항.json 을 ghSha→ghRaw 로 받아 sha 가 다르면 IndexedDB 캐시를 갈아 낀다)"""
    dv = Dev2(br, eng)
    try:
        dv.load(app, 'earth', rec={RP: RECB['earth']}, static=stat)
        put0 = dv.settle(); raw0 = dv.putraw()
        scr0 = dv.ev("()=>__U.screen()"); gp0 = dv.ev("()=>__U.gpTags()"); n0 = dv.ev("()=>DATA.length")
        items2 = [fake_item()] + ITEMS['earth']
        dv.load(app, 'earth', rec={RP: raw0.encode('utf-8'), 'earth/문항.json': dumps(items2)}, static=stat)
        put1 = dv.settle()
        n1 = dv.ev("()=>DATA.length")
        scr1 = dv.ev("()=>__U.screen()"); gp1 = dv.ev("()=>__U.gpTags()")
        no = dv.ev("u=>__U.openRow(u)", 'G06-43-10')
        dv.click('#tGpt'); dv.pg.wait_for_timeout(900)
        sh = dv.ev("()=>__U.sheet()")
        dv.ev("()=>__U.closeSheets()")
        # 옛 번호 119 자리(= 가짜 끼운 뒤 바로 앞 문항) 창도 본다 — 바탕은 여기에 G06-43-10 의 글이 밀려와 뜬다
        no119 = 119
        uid_at119 = dv.ev("n=>DATA[n-1][F.CODE]", no119)
        dv.ev("n=>openView(n)", no119); dv.pg.wait_for_timeout(1000)
        dv.click('#tGpt'); dv.pg.wait_for_timeout(900)
        sh119 = dv.ev("()=>__U.sheet()")
        dv.ev("()=>__U.closeSheets()")
        return {'n': [n0, n1], 'scr0': scr0, 'scr1': scr1, 'gp0': gp0, 'gp1': gp1, 'no': no, 'sheet': sh, 'uid_at119': uid_at119, 'sheet119': sh119, 'put1': put1,
                'errs': dv.errs[:3]}
    finally:
        dv.close()


def b84_edit(dv, uid='G03-40-05', mark='#card .vrow [data-vmark="X"]'):
    """옛 판 기기가 status|84 를 고친다 — 그 문항을 열어 X 를 진짜 누름(h 끝에 한 줄)"""
    dv.ev("u=>__U.openRow(u)", uid)
    ok = dv.click(mark); dv.pg.wait_for_timeout(300)
    dv.ev("()=>{try{closeView()}catch(e){}}")
    return ok


def sc_mix(br, eng, app, stat):
    """B-5 옛 판 기기 섞기 — A = 새 판(지금 재는 판) · B = 옛 판(바탕) · 원격은 올린 몸통으로 갈아 끼운다(route 사본)"""
    appB, statB = APPS['BASE']
    uid = 'G03-40-05'
    base_h = RECJ['earth']['data']['status']['84']['h']
    out = {'base_h': base_h}
    dA = Dev2(br, eng); dB = Dev2(br, eng)
    try:
        # 차례 1 — A 가 옮겨 올린 뒤 B 가 옛 로컬로 고쳐 올리고 A 가 다시 병합
        dB.load(appB, 'earth', rec={RP: RECB['earth']}, static=statB); dB.settle()
        dA.load(app, 'earth', rec={RP: RECB['earth']}, static=stat)
        pA1 = dA.settle(); remote = dA.putraw()
        ok = b84_edit(dB, uid)
        dB.set_rec(RP, remote.encode('utf-8')); pB = dB.settle(); remote2 = dB.putraw()
        dA.set_rec(RP, remote2.encode('utf-8')); pA2 = dA.settle()
        out['o1'] = {'A1': pA1, 'B': pB, 'A2': pA2, 'edit': ok, 'stA': dA.ev("()=>JSON.stringify(SYNC_REF.status.g())"), 'errs': dA.errs[:3]}
    finally:
        dA.close(); dB.close()
    dA = Dev2(br, eng); dB = Dev2(br, eng)
    try:
        # 차례 2 — B 가 먼저 올림(옛 판 몸통) → 그 원격을 새 판 A 가 연다
        dB.load(appB, 'earth', rec={RP: RECB['earth']}, static=statB); dB.settle()
        ok = b84_edit(dB, uid)
        pB = dB.settle(); rawB = dB.putraw()
        dA.load(app, 'earth', rec={RP: rawB.encode('utf-8')}, static=stat)
        pA3 = dA.settle()
        out['o2'] = {'B': pB, 'A': pA3, 'edit': ok, 'errs': dA.errs[:3]}
    finally:
        dA.close(); dB.close()
    return out


def j_mix(O):
    uid = 'G03-40-05'; bh = O['base_h']
    det = {}; ok = True
    for tag, put in (('차례1(A→B→A)', O['o1']['A2']), ('차례2(B→A)', O['o2']['A'])):
        D = put['data']; st = D.get('status') or {}
        h = (st.get(uid) or {}).get('h') or []
        num = [c for c in st if c in N2U['earth']]
        good = h[:len(bh)] == bh and len(h) == len(bh) + 1 and h[-1].get('m') == 'X' and (put['u'] or {}).get('status|' + uid) == h[-1].get('t')
        hn = (st.get('84') or {}).get('h') or []
        det[tag] = {'status|uid h 길이': len(h), '끝 마크': (h[-1] if h else None) and h[-1].get('m'), '번호 칸(수)': len(num), '번호 84 칸 h 길이(옛 판이면 여기)': len(hn), '도장 = 끝 t': (put['u'] or {}).get('status|' + uid) == (h[-1].get('t') if h else None)}
        ok = ok and good and not num
    a, b = (O['o1']['A2']['data']['status'].get(uid) or {}).get('h') or [], (O['o2']['A']['data']['status'].get(uid) or {}).get('h') or []
    same = [x.get('m') for x in a] == [x.get('m') for x in b]
    det['두 차례 결과 같음(마크 열)'] = same
    ok = ok and same and O['o1']['edit'] and O['o2']['edit']
    return ok, det


def sc_writes(br, eng, app, stat):
    """B-5(새 판은 번호 열쇠를 안 쓴다) — 마크(O) · 코멘트 · Claude 풀이를 진짜 눌러 저장한 뒤 올린 몸통·IndexedDB 의 열쇠를 본다"""
    free = [u for u in KIND_G['earth'] if u not in {N2U['earth'][n] for n in RECJ['earth']['data']['status']} and u not in RECJ['earth']['data']['bogi']]
    uid = free[3]
    dv = Dev2(br, eng)
    try:
        dv.load(app, 'earth', rec={RP: RECB['earth']}, static=stat)
        dv.settle()
        no = dv.ev("u=>__U.openRow(u)", uid)
        a = dv.click('#card .vrow [data-vmark="O"]')
        b = c = False
        try:
            dv.ev('n=>noteSheet(n)', no); dv.pg.wait_for_timeout(300)
            dv.pg.locator('#ntIn').fill('검산 코멘트', timeout=6000); b = dv.click('#ntSave'); dv.pg.wait_for_timeout(500)
        except Exception as e:
            b = 'ERR ' + repr(e)[:80]
        try:
            dv.click('#tGpt'); dv.pg.wait_for_timeout(500)
            dv.pg.locator('#gpIn').fill('검산 Claude 글', timeout=6000); c = dv.click('#gpSave'); dv.pg.wait_for_timeout(500)
        except Exception as e:
            c = 'ERR ' + repr(e)[:80]
        dv.ev("()=>__U.closeSheets()")
        put = dv.settle()
        keys = dv.ev("()=>__U.keys()")
        idb = dv.ev("k=>__U.idb(k)", [k for k in keys if k in NUMK])
        return {'uid': uid, 'no': no, 'clicks': [a, b, c], 'put': put, 'idb': idb, 'ink': dv.ev("()=>__U.inkKeys()"), 'errs': dv.errs[:3], 'cerr': list(dv.cerr)[:3], 'cnt': dv.ev("()=>__U.cnt2()")}
    finally:
        dv.close()


def j_writes(O):
    D = O['put']['data']; uid = O['uid']; no = str(O['no'])
    det = {}
    ok = all(x is True for x in O['clicks'])
    for k in ('status', 'note', 'gpt'):
        d = D.get(k) or {}
        det[k] = {'uid 칸': uid in d, '번호 칸': no in d}
        ok = ok and uid in d and no not in d
    badi = [(k, c) for k, v in (O['idb'] or {}).items() if isinstance(v, dict) for c in v if numkey(k, c)]
    numink = [x for x in O['ink'] if re.fullmatch(r'\d+', x)]
    det['IndexedDB kv 번호 열쇠'] = badi[:5]; det['ink 통 번호 열쇠'] = numink[:3]; det['오류'] = (O['errs'] + O['cerr'])[:3]
    guard = (O.get('cnt') or {}).get('guard', 0)
    det['번호 열쇠 가드(막은 칸 수 · 0 이어야)'] = guard
    return ok and not badi and not numink and not O['errs'] and not O['cerr'] and not guard, det


def sc_bio(br, eng, app, stat):
    """B-6 생물 빈 기록 = 옮김 0 — 생물 고정본(모든 통 0칸 · u·gone 0)을 실은 기기"""
    return dict(sc_main(br, eng, app, stat, subj='bio', second=False))


def j_bio(O):
    F = RECJ['bio']; put = O['put']
    same = canon(put['data']) == canon(F['data'])
    c2 = O.get('cnt') or {}
    ok = same and not put['u'] and not put['gone'] and not F['u'] and not F['gone'] and not c2.get('uid') and not c2.get('guard')
    return ok, {'옮김·가드 카운터(uid·guard)': [c2.get('uid', 0), c2.get('guard', 0)], 'data = 고정본': same, 'u': len(put['u']), 'gone': len(put['gone']), '옮김 수(이 앱 카운터)': O['mig'], 'bak_uid': (O['bak'] or '')[:60], '고정본 u·gone': [len(F['u']), len(F['gone'])]}


def sc_phys(br, eng, app, stat):
    """물리 — 올린 몸통 · 목록 30줄 DOM · 서랍 줄 · 「N회독」 칩 · #72 #97 Claude 창(제목 · 모션 단추 줄 · iframe)"""
    path = 'phys/기록.json'
    dv = Dev2(br, eng)
    try:
        dv.load(app, 'phys', rec={path: RECB['phys']}, static=stat)
        put = dv.settle(path)
        pick = """(sel)=>{const L=[...document.querySelectorAll(sel)];const n=L.length;const o=[];for(let i=0;i<30&&n;i++){const e=L[Math.floor(i*n/30)];const c=e.cloneNode(true);
            c.querySelectorAll('canvas,img,.ewmt').forEach(x=>x.remove());o.push(__U.ws(c.outerHTML))}return {n:n,rows:o}}"""   # ★ .ewmt = 묶음 add1 태그(물리 줄에도 · JG2 몫)
        O = {'put': put, 'list': dv.ev(pick, '#list .item'), 'drawer': dv.ev(pick, '#ndList .ndrow'),
             'chips': dv.ev("()=>[...document.querySelectorAll('#list .item .meta .tag')].filter(t=>/^\\d+회독$/.test(t.textContent.trim())).length"),
             'cnt': dv.ev("()=>__U.cnt()"), 'u': dv.ev("()=>__J.u()"), 'gone': dv.ev("()=>__J.gone()"), 'keys': dv.ev("()=>__U.keys()")}
        wins = {}
        for no in (72, 97):
            dv.ev("n=>openView(n)", no); dv.pg.wait_for_timeout(1000)
            dv.click('#tGpt'); dv.pg.wait_for_timeout(900)
            s = dv.ev("()=>{const s=[...document.querySelectorAll('.sheet')].pop();if(!s)return null;const c=s.cloneNode(true);c.querySelectorAll('canvas,img,iframe').forEach(x=>x.remove());return __U.ws(c.outerHTML)}")
            sh = dv.ev("()=>__U.sheet()")
            fr = None
            if sh and sh.get('motBarVis'):
                dv.click('#gpMot'); dv.pg.wait_for_timeout(1500)
                fr = dv.ev("()=>__U.frame()")
            wins[no] = {'html': s, 'sheet': sh, 'frame': fr}
            dv.ev("()=>__U.closeSheets()")
        O['wins'] = wins; O['errs'] = dv.errs[:3]; O['cerr'] = list(dv.cerr)[:3]
        return O
    finally:
        dv.close()


def nok(d):
    d = json.loads(json.dumps(d or {}))
    if d.get('solx') == {}:   # ★ 2026-10-07 (_task_jagwa_phys_win §A-30) — 시안 ㉖ 물리 SYNC_KEYS 에 solx(오린 것) 더함 → 올린 몸통에 빈 통 {} 이 실린다 · 바탕 4754b1d 엔 없는 키라 빈 것만 뺀다(오린 것이 있으면 남아 걸린다)
        d.pop('solx')
    for v in (d.get('gg') or {}).values():
        for g in (v or []):
            if isinstance(g, dict):
                g.pop('k', None)
    return d


def j_phys_body(ON, OB):
    a, b = ON['put'], OB['put']
    nu = lambda u: {k: v for k, v in (u or {}).items() if not k.startswith('gg|')}   # gg 도장 = 근거 되살림이 열 때마다 지금 시각으로 찍음(두 번 돌린 바탕끼리도 다름 · 이 판과 무관)
    ok = canon(nok(a['data'])) == canon(nok(b['data'])) and canon(nu(a['u'])) == canon(nu(b['u'])) and canon(a['gone']) == canon(b['gone'])
    return ok, {'data=바탕': canon(nok(a['data'])) == canon(nok(b['data'])), 'u=바탕(gg 도장 뺌)': canon(nu(a['u'])) == canon(nu(b['u'])), 'gone=바탕': canon(a['gone']) == canon(b['gone']), '칸(물리)': ON['keys']}


def _b6_norm(rows, kind):   # ★ 2026-10-08 (_task_jagwa_phys_win §A-36·37 · §A-06 · §A-34·35 · §A-41·47 · §A-03) 물리 목록·서랍 줄의 뜻한 차만 뗌(두 판 모두 · 새 판 표지가 있을 때만 부름)
    out = []
    for x in rows:
        if kind == 'list':
            x = re.sub(r'\s*<span class="vno"[^>]*>[^<]*</span>', '', x)               # §A-36 ㊴ V 글자(새 판)
            x = re.sub(r'\s*<span class="tag (?:tg|tc|tt|te)">[^<]*</span>', '', x)    # 그 자리 기출·확인·타기출·예상 딱지(바탕)
            x = re.sub(r'\s*<span class="tag vlt">[^<]*</span>', '', x)                # §A-37 「볼트 N」 칩(바탕)
        else:
            x = re.sub(r' data-sec="[^"]*"', '', x)                                     # §A-06 서랍 줄 절 표지(접힌 단원 숨김)
            x = x.replace('class="ndno ph"', 'class="ndno"')                            # §A-34 번호 칸 ph
            x = re.sub(r'<i class="ndv"[^>]*>[^<]*</i>', '', x)                         # §A-35 번호 앞 V 글자
            x = re.sub(r'<span class="ndtt"[^>]*>([^<]*)</span>', r'\1', x)             # §A-41·47 제목 span.ndtt(길게 눌러 고치기)
            x = re.sub(r'((?:<b class="ndm[^"]*">[^<]*</b>)+)', lambda m: re.findall(r'<b class="ndm[^"]*">[^<]*</b>', m.group(1))[-1], x)   # §A-03 꼬리 회독마다 → 마지막 회독 것만(바탕 꼴)
        out.append(x)
    return out


def j_phys_screen(ON, OB):
    # 옛 줄: ok = ON['list'] == OB['list'] and ON['drawer'] == OB['drawer'] and ON['cnt'] == OB['cnt'] and ON['list']['n'] > 0
    if any('class="ndtt"' in x for x in (ON.get('drawer') or {}).get('rows') or []):   # ★ 2026-10-08 (_task_jagwa_phys_win) 새 판 표지 — 두 판 모두 뜻한 차만 떼고 맞댐(가림은 값에 남김)
        ON = dict(ON, list=dict(ON['list'], rows=_b6_norm(ON['list']['rows'], 'list')), drawer=dict(ON['drawer'], rows=_b6_norm(ON['drawer']['rows'], 'drawer')), b6mask=True)
        OB = dict(OB, list=dict(OB['list'], rows=_b6_norm(OB['list']['rows'], 'list')), drawer=dict(OB['drawer'], rows=_b6_norm(OB['drawer']['rows'], 'drawer')))
    ok = ON['list'] == OB['list'] and ON['drawer'] == OB['drawer'] and ON['cnt'] == OB['cnt'] and ON['list']['n'] > 0
    diff = [i for i, (x, y) in enumerate(zip(ON['list']['rows'], OB['list']['rows'])) if x != y]
    ddiff = [i for i, (x, y) in enumerate(zip(ON['drawer']['rows'], OB['drawer']['rows'])) if x != y]
    return ok, {'목록 줄': [ON['list']['n'], OB['list']['n']], '다른 줄(30 표본)': diff[:4], '서랍 줄': [ON['drawer']['n'], OB['drawer']['n']], '다른 서랍 줄': ddiff[:4], '카운터 같음': ON['cnt'] == OB['cnt'],
                **({'가림(§A · 뜻한 차)': 'V 글자·기출 딱지·볼트 N(목록) · data-sec·ph·V·ndtt·꼬리 마지막 회독(서랍)'} if ON.get('b6mask') else {}),
                **({'첫 다른 줄': [ON['list']['rows'][diff[0]][:300], OB['list']['rows'][diff[0]][:300]]} if diff else {}),
                **({'첫 다른 서랍 줄': [ON['drawer']['rows'][ddiff[0]][:300], OB['drawer']['rows'][ddiff[0]][:300]]} if ddiff else {})}   # ★ 2026-10-08 (_task_jagwa_phys_win) 남은 차는 글자로 남김


# ══════════ E 시나리오 ══════════
def E_rec():
    d = json.loads(RECB['earth'].decode('utf-8')); t = now_ms()
    for uid in MATS:
        d['data']['gpt'][uid] = mat(uid); d['u']['gpt|' + uid] = t
    return d


def sc_E(br, eng, app, stat):
    """§E — 원격 사본 = 고정본 + 재료 넷(gpt[uid] · 도장 = 지금 · 번호 칸 gpt[84·111·119·149] 는 안 건드림) · 빈 기기 · 창 네 개 · 옆 문항 · 목록 태그"""
    d = E_rec()
    dv = Dev2(br, eng)
    try:
        dv.load(app, 'earth', rec={RP: dumps(d)}, static=stat)
        put = dv.settle()
        O = {'rec': d, 'put': put, 'gpTags': dv.ev("()=>__U.gpTags()"), 'u': dv.ev("()=>__J.u()")}
        wins = {}
        for uid in (MATS if not QC.SMOKE else list(MATS)[:1]):   # smoke — 첫 uid 하나(E-1 제목 칸)
            no = dv.ev("u=>__U.openRow(u)", uid)
            dv.click('#tGpt'); dv.pg.wait_for_timeout(900)
            w = {'no': no, 'sheet': dv.ev("()=>__U.sheet()")}
            if (w['sheet'] or {}).get('motTx') == '▶ 모션' and not QC.SMOKE:   # smoke — 모션 건넘
                dv.click('#gpMot'); dv.pg.wait_for_timeout(1800)
                w['frame'] = dv.ev("()=>__U.frame()"); w['after'] = dv.ev("()=>__U.sheet()")
            dv.ev("()=>__U.closeSheets()")
            nb = {}
            for dn in ((-1, 1) if not QC.SMOKE else ()):   # smoke — 이웃 문항 건넘
                dv.ev("n=>openView(n)", no + dn); dv.pg.wait_for_timeout(900)
                dv.click('#tGpt'); dv.pg.wait_for_timeout(600)
                s = dv.ev("()=>__U.sheet()")
                nb[dn] = {'uid': dv.ev("n=>DATA[n-1][F.CODE]", no + dn), 'sheet': bool(s), 'motTx': (s or {}).get('motTx'), 'h2': (s or {}).get('h2')}
                dv.ev("()=>__U.closeSheets()")
            w['nb'] = nb
            wins[uid] = w
        O['wins'] = wins; O['errs'] = dv.errs[:3]; O['cerr'] = list(dv.cerr)[:8]
        return O
    finally:
        dv.close()


def sc_E_old(br, eng, app, stat):
    """§E-3 옛 기록 있는 기기 — 옛 판(바탕)으로 고정본을 받아 둔 기기에 새 판을 올려 재료가 든 원격을 받는다(옛 글이 새 글을 못 이긴다)"""
    appB, statB = APPS['BASE']
    d = E_rec()
    dv = Dev2(br, eng)
    try:
        dv.load(appB, 'earth', rec={RP: RECB['earth']}, static=statB); dv.settle()
        oldgp = dv.ev("()=>Object.fromEntries(Object.entries(GP))")
        dv.load(app, 'earth', rec={RP: dumps(d)}, static=stat)
        put = dv.settle()
        return {'rec': d, 'put': put, 'oldgp': oldgp, 'errs': dv.errs[:3]}
    finally:
        dv.close()


def parse_mat(txt):
    """gpRender 가 세는 것을 파이썬으로 — 절 · 글머리 · 표(th·tbody tr) · 굵게 · Q 줄 · 첫 줄(QA)"""
    L = txt.replace('\r\n', '\n').split('\n')
    qa = L[0] if L and QA1.match(L[0]) else None
    body = L[2:] if (qa and len(L) > 1 and not L[1].strip()) else (L[1:] if qa else L)
    sec = [l for l in body if '|' not in l and re.match(r'^\s*[①-⑩]', l)]
    li = [l for l in body if '|' not in l and re.match(r'^\s*-\s+', l)]
    tl = [l for l in body if '|' in l]
    sep = lambda r: ('-' in r) and re.fullmatch(r'[\s|:\-]+', r) is not None
    rows = [r for r in tl if not sep(r)]
    th = len([c for c in rows[0].strip().strip('|').split('|')]) if (len(tl) > 1 and sep(tl[1]) and rows) else 0
    tr = len(rows) - (1 if th else 0)
    bold = sum(len(re.findall(r'\*\*([^*]+)\*\*', l)) for l in body if not sep(l))
    q = [l for l in body if re.match(r'^\*\*Q\d*\.', l)]
    return {'qa': qa, 'body': '\n'.join(body), 'sec': [re.sub(r'\*\*([^*]+)\*\*', r'\1', re.sub(r'^\s*([①-⑩])\s*', r'\1 ', s).strip()) for s in sec], 'li': len(li), 'tb': 1 if tl else 0, 'th': th, 'tr': tr,
            'b': bold, 'q': len(q), 'pipe': len(tl), 'lines': body}


def norm(s):
    return re.sub(r'\s+', '', s or '')


def title_rule(uid):
    """지시서 C-1 — uid + ' Claude' + (정답 있으면 ' · 정답 ' + CIRC[정답−1] + 선택지글(ㄱ~ㅎ·㉠~㉭·쉼표·빈칸만이면 ' ' + 그 글 · 쉼표+빈칸 → · · ㉠㉡㉢… → ㄱㄴㄷ…) + (문항에 옳지 않은 있으면 ' (옳지 않은 것)'))"""
    r = ITEMS['earth'][int(U2N['earth'][uid]) - 1]
    CIRC = '①②③④⑤⑥⑦⑧'
    a = int(r.get('정답') or 0)
    t = uid + ' Claude'
    if a:
        t += ' · 정답 ' + CIRC[a - 1]
        c = (r.get('선택지') or [''] * a)[a - 1] if len(r.get('선택지') or []) >= a else ''
        if c and re.fullmatch(r'[ㄱ-ㅎ㉠-㉭,\s]+', c):
            c2 = re.sub(r',\s*', '·', c.strip())
            c2 = ''.join('ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ'[ord(x) - 0x3260] if '㉠' <= x <= '㉭' else x for x in c2)
            t += ' ' + c2
        if '옳지 않은' in (r.get('문항') or ''):
            t += ' (옳지 않은 것)'
    return t


# ══════════ E 판정 ══════════
def j_E1_title(O, uid):
    w = O['wins'][uid]; s = w['sheet'] or {}
    want = '%s Claude · %s' % (uid, TITLE_END[uid])
    h2 = (s.get('h2', '') or '').replace('✕', '').strip()   # 창 틀이 h2 안에 ✕ 를 넣는다(72번 Claude 풀이✕)
    ok = h2 == want and '번호' not in h2 and not re.search(r'\d+번', h2) and title_rule(uid) == want
    return ok, {'제목': h2, '기대(지시서 C-1)': want, '규칙 계산': title_rule(uid), '번호 글자': '번호' in h2}


def j_E1_line2(O, uid):
    w = O['wins'][uid]; s = w['sheet'] or {}
    want = MATS[uid][3]
    d = s.get('pdisp') or []
    ok = s.get('pspans') == [want] and d[:2] == ['flex', 'baseline'] and (len(d) > 2 and d[2] in ('8px', '8px 8px')) and not s.get('motBar')
    return ok, {'둘째 줄 왼쪽': s.get('pspans'), '기대': want, 'display·align·gap': d, '옛 #gpMotBar 줄': s.get('motBar'), '둘째 줄 전체': s.get('p')}


def j_E1_mot(O, uid):
    w = O['wins'][uid]; s = w['sheet'] or {}; f = w.get('frame') or {}; a = w.get('after') or {}
    st = s.get('motSt') or {}
    btn = s.get('motTx') == '▶ 모션' and s.get('motInP') and st.get('bw') == '0px' and st.get('pad') in ('0px/0px',) and st.get('fs') == '13px' and st.get('bi') == 'none' \
        and (st.get('bg') in ('rgba(0, 0, 0, 0)', 'transparent'))
    fr = f.get('src') == 'motion/earth_%s.html' % uid and f.get('status') == 200 and f.get('same') and abs((f.get('h') or 0) - 480) <= 2 and f.get('belowP') is True and (f.get('text') or 0) > 0
    closed = a.get('motTx') == '▼ 모션 닫기'
    return btn and fr and closed, {'단추': {'글자': s.get('motTx'), '둘째 줄 안': s.get('motInP'), '스타일': st}, 'iframe': {k: f.get(k) for k in ('src', 'status', 'same', 'h', 'belowP', 'canvas', 'svg', 'text')}, '열린 뒤 글자': a.get('motTx')}


def j_E1_nb(O):
    det = {}; ok = True
    for uid, w in O['wins'].items():
        n = w['nb']
        good = all(n[k]['sheet'] and not n[k]['motTx'] for k in (-1, 1)) and (w['sheet'] or {}).get('motTx') == '▶ 모션'
        det[uid] = {'앞뒤 문항': [n[-1]['uid'], n[1]['uid']], '이웃 모션 글자': [n[-1]['motTx'], n[1]['motTx']], '자기 모션 글자': (w['sheet'] or {}).get('motTx')}
        ok = ok and good
    return ok, det


def j_E1_err(O):
    merr = [x for x in (O['cerr'] or []) if 'motion/' in x]
    return not merr and not O['errs'], {'모션 쪽 콘솔 오류': merr[:3], 'pageerror': O['errs'], '앱 콘솔(참고)': (O['cerr'] or [])[:3]}


def j_E2(O, uid):
    w = O['wins'][uid]; s = w['sheet'] or {}
    m = parse_mat(mat(uid))
    t = MATS[uid][4]
    h3 = s.get('h3') or []
    secs_ok = len(h3) == 5 and [x[:1] for x in h3] == list('①②③④⑤') and not any(x.startswith('⑥') for x in h3) and [norm(x) for x in h3] == [norm(x) for x in m['sec']]
    p1 = s.get('p1') or ''
    p1_ok = p1.startswith('<b>Q') and (p1.count('<b>Q') == m['q'])
    qa_in = bool(QA1.search(s.get('text', ''))) or MATS[uid][3] in s.get('text', '') or re.search(r'QA [EB]\d{3}', s.get('text', '')) is not None
    cnt = {'li': s.get('li') == m['li'], 'ol': s.get('ol') == 0, 'tb': s.get('tb') == 1 == m['tb'], 'th': s.get('th') == m['th'], 'tr': s.get('tr') == m['tr'], 'b': s.get('b') == m['b']}
    txt = norm(s.get('text', ''))
    miss = [l for l in m['lines'] if l.strip() and '|' not in l and norm(re.sub(r'\*\*([^*]+)\*\*', r'\1', re.sub(r'^\s*(-\s+|[①-⑩]\s*)', '', l))) not in txt]
    ok = secs_ok and p1_ok and not qa_in and all(cnt.values()) and s.get('script') == 0 and not miss and s.get('read') and not s.get('edit')
    return ok, {'h3': h3, '기대 절': m['sec'], '첫 p.gpp <b>Q 시작·Q줄 수': [p1.startswith('<b>Q'), p1.count('<b>Q'), m['q']], 'QA 줄 본문에': qa_in,
                '셈(화면=재료)': cnt, '화면': {k: s.get(k) for k in ('li', 'tb', 'th', 'tr', 'b', 'script')}, '재료': {k: m[k] for k in ('li', 'tb', 'th', 'tr', 'b')}, '본문에 안 보이는 줄': miss[:2]}


def j_E_mat_static(O=None):
    """재료 넷 — 크기·md5·첫 줄·절·글머리·| 줄·굵게·Q 줄 = 지시서 D-2 표(다르면 멈추고 보고) · 셈은 재료 글에서 다시 센 값"""
    bad = {}
    for uid, (f, size, md, first, cnt) in MATS.items():
        b = open(os.path.join(MAT, f), 'rb').read()
        m = parse_mat(mat(uid))
        got = (len(m['sec']), m['li'], m['pipe'], m['b'], m['q'])
        okk = len(b) == size and md5(b) == md and m['qa'] == first and got == cnt and b.endswith(b'\n') and not b.endswith(b'\n\n') and b'\r' not in b
        if not okk:
            bad[uid] = {'크기·md5': [len(b), md5(b)[:8]], '첫 줄': m['qa'], '셈': got, '표': cnt}
    return not bad, bad or {u: '크기·md5·첫 줄·셈 모두 표와 같음' for u in MATS}


def j_E3(O):
    """빈 기기 — 올린 몸통 gpt = 재료 글자 전수 · 번호 gpt 칸 0 · 도장 = 재료 도장(새 칸이 이김)"""
    put = O['put']; G = (put['data'].get('gpt') or {}); d = O['rec']
    num = [c for c in G if c in N2U['earth']]
    ok = all(G.get(u) == mat(u) for u in MATS) and not num and set(G) == set(MATS) and all((put['u'] or {}).get('gpt|' + u) == d['u']['gpt|' + u] for u in MATS)
    tomb = [x for x in ('gpt|' + n for n, _, _ in ANCH) if x not in (put['gone'] or {})]
    return ok and not tomb, {'gpt 열쇠': sorted(G), '글 같음': {u: G.get(u) == mat(u) for u in MATS}, '번호 gpt 칸': num, '재료 도장 그대로': {u: (put['u'] or {}).get('gpt|' + u) == d['u']['gpt|' + u] for u in MATS},
                             '옛 번호 칸 묘비 빠짐': tomb}


def j_E3_old(O):
    put = O['put']; G = (put['data'].get('gpt') or {}); d = O['rec']
    num = [c for c in G if c in N2U['earth']]
    oldmine = {u: O['oldgp'].get(n) for n, u, _ in ANCH}
    ok = all(G.get(u) == mat(u) for u in MATS) and not num and all(G.get(u) != oldmine[u] for u in MATS)
    return ok, {'gpt 열쇠': sorted(G), '새 글(재료)이 이김': {u: G.get(u) == mat(u) for u in MATS}, '옛 글이 남음': {u: G.get(u) == oldmine[u] for u in MATS}, '번호 칸': num, '옛 기기가 받아 둔 번호 칸 수': len(O['oldgp'])}


def j_E4(O):
    want = sorted(MATS)
    return O['gpTags'] == want, {'.tag.gp 줄(uid)': O['gpTags'], '기대': want}


def j_E5(ON, OB):
    det = {}; ok = True
    for no in (72, 97):
        a, b = ON['wins'][no], OB['wins'][no]
        s = a['sheet'] or {}; f = a['frame'] or {}
        lit = (s.get('h2') or '').replace('✕', '').strip() == '%d번 Claude 풀이' % no and s.get('motBar') and s.get('motBarVis') and s.get('motTx') == '▶ 모션' and f.get('src') == 'motion/phys_%d.html' % no and f.get('status') == 200
        same = a['html'] == b['html'] and (a['frame'] or {}).get('src') == (b['frame'] or {}).get('src')
        det[no] = {'제목': (s.get('h2') or '').replace('✕', '').strip(), '단추 줄': s.get('motBar'), 'iframe': f.get('src'), '200': f.get('status'), '바탕과 DOM 같음': same}
        ok = ok and lit and same
    return ok, det


# ══════════ H 시나리오 ══════════
SURF = {
    'mcardWin': ("n=>{mcardWin(n);const e=document.querySelector('.mcwin .mch');return e?e.textContent:null}", "()=>{const x=document.getElementById('mcX');if(x)x.click()}"),
    'mcwOpen': ("()=>{mcwOpen('all');const e=document.getElementById('mcw');return e?e.textContent:null}", "()=>{const e=document.getElementById('mcw');if(e)e.remove()}"),
    'jnOpen': ("n=>{const u=unitOf(n);jnOpen(secOf(u));const e=document.getElementById('jnw');return e?e.textContent:null}", "()=>{const e=document.getElementById('jnw');if(e)e.remove()}"),
    'ggUseWin': ("()=>{const t=Object.keys(GG).find(k=>GGU&&DATA.find(r=>r[F.CODE]===k));if(!t)return null;ggUseWin(t,t);const e=document.getElementById('gguw');return e?e.textContent:null}", "()=>{const e=document.getElementById('gguw');if(e)e.remove()}"),
    'search': ("()=>{const q=document.getElementById('q');if(!q)return null;q.value='대기';esSearch();const e=document.getElementById('esres');return e&&!e.classList.contains('hide')?e.textContent:null}",
               "()=>{const q=document.getElementById('q');if(q){q.value='';esSearch()}}"),
}


def sc_H1(br, eng, app, stat, subj='earth', recb=None):
    """H-1·H-2 — 서랍 줄 · 목록 줄 · 문제 창 머리 · .cmeta · 암기카드·정리·근거·검색 면의 「NN회 N번」 · 「N회독」 칩 · 서랍 마크 · 확인문제 줄"""
    recb = recb if recb is not None else RECB[subj]
    path = '%s/기록.json' % subj
    dv = Dev2(br, eng, vp=(1280, 900))
    try:
        dv.load(app, subj, rec={path: recb}, static=stat)
        dv.settle(path)
        O = {'subj': subj}
        O['drawer'] = dv.ev("""()=>[...document.querySelectorAll('#ndList .ndrow')].map(d=>{const r=DATA[+d.dataset.no-1];const tl=d.querySelector('.ndtail');
            return {uid:r?r[F.CODE]:'',kind:r?kindOf(r):'',no:+d.dataset.no,ndt:__U.tx(d.querySelector('.ndt')),ndm:[...d.querySelectorAll('.ndtail .ndm')].map(x=>x.textContent.trim()),
              ndmc:[...d.querySelectorAll('.ndtail .ndm')].map(x=>x.className),ndw:d.querySelectorAll('.ndtail .ndw').length,order:tl?[...tl.children].map(x=>x.className.split(' ')[0]):[]}})""")
        O['list'] = dv.ev("""()=>[...document.querySelectorAll('#list .item')].map(d=>({uid:d.dataset.uid||'',ec:d.classList.contains('ec'),sub:d.querySelector('.meta .sub')?__U.tx(d.querySelector('.meta .sub')):null,
            chips:[...d.querySelectorAll('.meta .tag')].map(t=>__U.tx(t)),meta:__U.tx(d.querySelector('.meta'))}))""")
        # 확인문제 줄(기출 칩 → 확인문제 칩) — 서랍·목록
        O['ec'] = dv.ev("""()=>{try{FL.past='p';draw()}catch(e){return null}try{navBuild()}catch(e){}
            const L=[...document.querySelectorAll('#list .item.ec')].slice(0,40).map(d=>({uid:d.dataset.uid||'',sub:d.querySelector('.meta .sub')?__U.tx(d.querySelector('.meta .sub')):null,chips:[...d.querySelectorAll('.meta .tag')].map(t=>__U.tx(t))}));
            const D=[...document.querySelectorAll('#ndList .ndrow')].slice(0,40).map(d=>({no:+d.dataset.no,ndt:__U.tx(d.querySelector('.ndt'))}));
            try{FL.past='y';draw();navBuild()}catch(e){}return {list:L,drawer:D}}""")
        # 문제 창 — 표본 기출 하나
        sample = 'G25-62-09' if subj == 'earth' else next(u for u in KIND_G['bio'])
        O['sample'] = sample
        r = ITEMS[subj][int(U2N[subj][sample]) - 1]
        O['year'] = str(r.get('연도'))
        no = dv.ev("u=>__U.openRow(u)", sample)
        O['card'] = dv.ev("()=>({vT1:__U.tx(document.getElementById('vT1')),cmeta:[...document.querySelectorAll('#card .cmeta .tag')].map(t=>__U.tx(t)),cmetaTx:__U.tx(document.querySelector('#card .cmeta'))})")
        dv.ev("()=>{try{closeView()}catch(e){}}")
        # 면 훑기
        surf = {}
        for name, (op, cl) in SURF.items():
            try:
                arg = no if name in ('mcardWin', 'jnOpen') else None
                if name == 'mcardWin':
                    dv.ev("n=>openView(n)", no); dv.pg.wait_for_timeout(700)
                t = dv.ev(op, arg) if arg is not None else dv.ev(op)
                dv.pg.wait_for_timeout(500)
                surf[name] = t if t is None else str(t)[:12000]
                dv.ev(cl)
                if name == 'mcardWin':
                    dv.ev("()=>{try{closeView()}catch(e){}}")
            except Exception as e:
                surf[name] = 'ERR ' + repr(e)[:100]
        O['surf'] = surf; O['no'] = no
        O['errs'] = dv.errs[:3]
        return O
    finally:
        dv.close()


def weak(h):
    s = ''
    for x in h:
        m = x.get('m')
        if m in ('X', 'Q'):
            s = 'weak'
        elif m == 'O':
            s = 'less' if s == 'weak' else ('' if s == 'less' else s)
    return s


def j_H1(O):
    subj = O['subj']
    bad = []
    G = [d for d in O['drawer'] if d['kind'] == 'G']
    dr_bad = [d['uid'] for d in G if d['ndt'] != d['uid'] or OLDTT.search(d['ndt'])]
    li = [x for x in O['list'] if not x['ec']]
    li_bad = [x['uid'] for x in li if x['sub'] or OLDTT.search(x['meta'])]
    c = O['card']; sample = O['sample']
    card_ok = c['vT1'] == '%s (%s)' % (sample, O['year']) and not OLDTT.search(c['cmetaTx']) and not any(OLDTT.search(t) for t in c['cmeta'])
    surf = O['surf']
    opened = {k: v for k, v in surf.items() if isinstance(v, str) and not v.startswith('ERR')}
    s_bad = {k: OLDTT.findall(v)[:2] for k, v in opened.items() if OLDTT.search(v)}
    s_nouid = [k for k, v in opened.items() if sample not in v and k not in ('search', 'ggUseWin')]   # 검색·근거 쓰임은 표본 uid 가 안 걸릴 수 있다(걸린 문항 글자만)
    ok = len(G) > 0 and not dr_bad and not li_bad and card_ok and not s_bad and len(opened) >= 2
    return ok, {'서랍 기출 줄': len(G), '서랍 uid≠.ndt': dr_bad[:3], '수': len(dr_bad), '목록 기출 줄': len(li), '목록 .sub·회번 남음': li_bad[:3], '문제 창': {'#vT1': c['vT1'], '기대': '%s (%s)' % (sample, O['year']), '.cmeta': c['cmeta']},
                '면 훑기(열린 면)': {k: len(v) for k, v in opened.items()}, '회·번 남은 면': s_bad, '표본 uid 안 보이는 면': s_nouid, '못 연 면': {k: v for k, v in surf.items() if v is None or (isinstance(v, str) and v.startswith('ERR'))}}


def j_H1_ec(ON, OB):
    a, b = ON['ec'], OB['ec']
    if not a or not b:
        return False, '확인문제 줄을 못 열었다'
    ok = canon(a) == canon(b) and len(a['list']) > 0 and any(x['sub'] for x in a['list'])
    return ok, {'목록 확인문제 줄': len(a['list']), '서랍 확인문제 줄': len(a['drawer']), '표본': a['list'][:1] and a['list'][0], '바탕과 같음': canon(a) == canon(b)}


def j_H2_chips(O):
    ch = [x['uid'] for x in O['list'] if any(re.fullmatch(r'\d+회독', t) for t in x['chips'])]
    return not ch, {'N회독 칩이 남은 줄': ch[:4], '수': len(ch), '목록 줄': len(O['list'])}


def j_H2_phys(ON, OB):
    return ON['chips'] == OB['chips'] and ON['chips'] > 0, {'물리 목록 N회독 칩': [ON['chips'], OB['chips']]}


def j_H2_drawer(O):
    F = RECJ['earth']['data']['status']
    bad = []; bad_w = []
    for d in O['drawer']:
        n = U2N['earth'].get(d['uid'])
        h = (F.get(n) or {}).get('h') or []
        if len(d['ndm']) != len(h):
            bad.append((d['uid'], len(d['ndm']), len(h)))
        if d['ndw'] != (1 if weak(h) == 'less' else 0):
            bad_w.append(d['uid'])
    r = next((d for d in O['drawer'] if d['uid'] == 'G24-61-07'), None)
    g = r and r['ndw'] == 1 and r['ndm'] == ['O', '△', 'O'] and r['ndmc'] == ['ndm ndmO', 'ndm ndmQ', 'ndm ndmO'] and r['order'][:1] == ['ndw'] and r['order'][1:4] == ['ndm'] * 3
    return bool(g) and not bad and not bad_w, {'G24-61-07': r and {'점': r['ndw'], '마크': r['ndm'], '클래스': r['ndmc'], '순서': r['order']}, '마크 수 ≠ h 길이': bad[:5], '수': len(bad), '덜약점 점 다름': bad_w[:3], '서랍 줄': len(O['drawer'])}


def j_H1_bio(O):
    """★ 채팅 10/4 23:1x 판정 (가) — G-1 은 지학만 · 생물 기출 줄은 회·번을 그대로 보인다(uid 뒷자리 ≠ 문번 · 260/270) → 서랍 .ndt = 「uid+난이도 · 제목」 · 목록 .sub 있음 · #vT1 = 「uid · 제목 (연도)」 · 「N회독」 칩 0(G-2 는 생물도)"""
    G = [d for d in O['drawer'] if d['kind'] == 'G']
    # 옛 줄: dr_bad = [d['uid'] for d in G if d['ndt'] != d['uid']]
    dr_bad = [d['uid'] for d in G if not (d['ndt'].startswith(d['uid']) and ' · ' in d['ndt'])]
    # 옛 줄: li_bad = [x['uid'] for x in O['list'] if not x['ec'] and (x['sub'] or OLDTT.search(x['meta']))]
    li_bad = [x['uid'] for x in O['list'] if not x['ec'] and not x['sub']]
    c = O['card']
    chips = [x['uid'] for x in O['list'] if any(re.fullmatch(r'\d+회독', t) for t in x['chips'])]
    # 옛 줄: return len(G) > 0 and not dr_bad and not li_bad and c['vT1'] == '%s (%s)' % (O['sample'], O['year']) and not chips, {…}
    vok = c['vT1'].startswith(O['sample'] + ' · ') and c['vT1'].endswith('(%s)' % O['year'])
    return len(G) > 0 and not dr_bad and not li_bad and vok and not chips, {
        '서랍 기출 줄': len(G), '서랍 .ndt 에 회·번 없음': dr_bad[:3], '목록 .sub 없음': li_bad[:3], '#vT1': c['vT1'], '기대': '%s · <제목> (%s)' % (O['sample'], O['year']), 'N회독 칩': chips[:3]}


def bio_fake_rec():
    """생물 표본 하나(가짜 기록) — 번호 열쇠로(원격이 지금 그 꼴) 기출 한 문항에 두 회독 · 보기 없음"""
    d = json.loads(RECB['bio'].decode('utf-8'))
    uid = KIND_G['bio'][0]; no = U2N['bio'][uid]
    t = now_ms() - 86400000 * 3
    d['data']['status'][no] = {'h': [{'m': 'X', 't': t, 's': 40}, {'m': 'O', 't': t + 60000, 's': 22}]}
    d['u']['status|' + no] = t + 60000
    return d, uid, no


def sc_H1_bio(br, eng, app, stat):
    d, uid, no = bio_fake_rec()
    o = sc_H1(br, eng, app, stat, subj='bio', recb=dumps(d))
    o['fake'] = (uid, no)
    return o


def j_H2_bio(O):
    uid, no = O['fake']
    r = next((d for d in O['drawer'] if d['uid'] == uid), None)
    return bool(r) and len(r['ndm']) == 2 and r['ndw'] == (1 if weak([{'m': 'X'}, {'m': 'O'}]) == 'less' else 0) and r['ndm'] == ['X', 'O'], {'가짜 기록 표본': uid, '서랍 마크': r and r['ndm'], '덜약점 점(X→O = 덜약점)': r and r['ndw']}


# ── H-3 다음 회독 ──
def cellinfo(put, uid, no):
    h, kf = cell(put, 'status', uid, no)
    b, _ = cell(put, 'bogi', uid, no)
    return {'h': (h or {}).get('h') if isinstance(h, dict) else None, 'key': kf, 'bogi': b, 'stamp': ((put or {}).get('u') or {}).get('status|' + (uid if kf == 'uid' else str(no)))}


def sc_H3(br, eng, app, stat, phone=False):
    vp = (390, 844) if phone else (1280, 900)
    dv = Dev2(br, eng, vp=vp, touch=phone)
    fing = phone
    uid = 'G24-61-07'; no = int(U2N['earth'][uid])
    free = [u for u in KIND_G['earth'] if u not in {N2U['earth'][n] for n in RECJ['earth']['data']['status']} and u not in RECJ['earth']['data']['bogi']]
    fb = [u for u in free if any(b.get('정오') for b in (ITEMS['earth'][int(U2N['earth'][u]) - 1].get('보기') or []))]
    X, Y, Z = fb[0], free[1], free[2]
    kx = next(b['키'] for b in (ITEMS['earth'][int(U2N['earth'][X]) - 1].get('보기') or []) if b.get('정오'))   # X 에서 〈보기〉를 누를 첫 줄(정오가 있는 줄)
    O = {'uid': uid, 'X': X, 'Y': Y, 'Z': Z, 'kx': kx, 'phone': phone, 'finger': fing}
    try:
        dv.load(app, 'earth', rec={RP: RECB['earth']}, static=stat)
        dv.settle()

        def openq(u):
            for _ in range(3):   # 눌렀는데 안 열렸으면(창이 그대로 닫혀 있음) 한 번 더
                ok = dv.click('#list .item[data-uid="%s"]' % u, finger=fing); dv.pg.wait_for_timeout(1300)
                if dv.ev("u=>{const v=document.getElementById('view');return !v.classList.contains('hide')&&VNO===__U.noOf(u)}", u):
                    return ok
            return False

        def closeq():
            for _ in range(3):   # 눌렀는데 안 닫혔으면 한 번 더
                ok = dv.click('#vBack', finger=fing); dv.pg.wait_for_timeout(500)
                if dv.ev("()=>document.getElementById('view').classList.contains('hide')"):
                    return ok
            return False

        def wire(u):
            return cellinfo(dv.settle(RP, 1), u, int(U2N['earth'][u]))
        # (a) 처음 열기
        O['open1'] = openq(uid); O['s1'] = dv.ev("()=>__U.snap()"); O['w1'] = wire(uid)
        # (b) ④ 누름 → ㄱ 보기 O → 닫기 → 다시 열기
        O['pick4'] = dv.click('#card .choices button[data-c="4"]', finger=fing); O['s2'] = dv.ev("()=>__U.snap()"); O['w2'] = wire(uid)
        O['bogiG'] = dv.click('#card .bogi .row[data-k="ㄱ"] .ox button[data-v="O"]', finger=fing); O['s3'] = dv.ev("()=>__U.snap()"); O['w3'] = wire(uid)
        O['close'] = closeq(); O['reopen'] = openq(uid); O['s4'] = dv.ev("()=>__U.snap()"); O['w4'] = wire(uid)
        closeq()
        # (c) 보기만 누르고 답 체크 없이 닫기 → 다시 열기
        O['openX'] = openq(X); O['sx0'] = dv.ev("()=>__U.snap()")
        O['bogiX'] = dv.click('#card .bogi .row[data-k="%s"] .ox button[data-v="O"]' % kx, finger=fing); O['sx1'] = dv.ev("()=>__U.snap()"); O['wx1'] = wire(X)
        closeq(); O['reopenX'] = openq(X); O['sx2'] = dv.ev("()=>__U.snap()"); O['wx2'] = wire(X)
        closeq()
        # (d) 창 열린 채 서랍 줄로 다른 문항 → 돌아와 선택지 누름
        O['openY'] = openq(Y); noY = dv.ev("u=>__U.noOf(u)", Y); noZ = dv.ev("u=>__U.noOf(u)", Z)
        O['pickY1'] = dv.click('#card .choices button[data-c="1"]', finger=fing); O['wy1'] = wire(Y)

        def drawer_go(n):
            vis = dv.ev("n=>{const e=document.querySelector('#ndList .ndrow[data-no=\"'+n+'\"]');if(!e)return false;const b=e.getBoundingClientRect();return b.width>0&&b.height>0&&b.right>0&&b.left<window.innerWidth}", n)
            if not vis:   # 폰 — 상주 서랍이 접혀(.fold 13px) 있다 → 손잡이 #ndGrip 을 눌러 편다
                dv.click('#ndGrip', finger=fing); dv.pg.wait_for_timeout(600)
            pr = dv.probe('#ndList .ndrow[data-no="%d"]' % n)
            if pr is None or not pr['ok']:
                return pr or {'ok': False, 'top': '줄 없음'}   # 가려져 못 누른다 — 폰은 상주 서랍이 문제 창 밑에 깔린다
            return dv.click('#ndList .ndrow[data-no="%d"]' % n, finger=fing)
        O['drawZ'] = drawer_go(noZ)
        if isinstance(O['drawZ'], dict):
            O['blocked'] = O['drawZ']; O['errs'] = dv.errs[:3]; O['cerr'] = list(dv.cerr)[:3]; O['covers'] = getattr(dv, 'covers', [])[:6]
            return O
        dv.pg.wait_for_timeout(900); O['vnoZ'] = dv.ev("()=>VNO"); O['noZ'] = noZ
        O['drawY'] = drawer_go(noY); dv.pg.wait_for_timeout(900); O['sy_back'] = dv.ev("()=>__U.snap()"); O['noY'] = noY
        O['pickY2'] = dv.click('#card .choices button[data-c="2"]', finger=fing); O['sy2'] = dv.ev("()=>__U.snap()"); O['wy2'] = wire(Y)
        O['errs'] = dv.errs[:3]; O['cerr'] = list(dv.cerr)[:3]; O['covers'] = getattr(dv, 'covers', [])[:6]
        return O
    finally:
        dv.close()


B3 = {'ㄱ': 'O', 'ㄴ': 'O', 'ㄷ': 'X'}


def pure_b(b):
    return {k: v for k, v in (b or {}).items() if not str(k).startswith('_')}


def j_H3a(O):
    s = O['s1']; w = O['w1']
    ok = O['open1'] and s['pick'] == [] and s['bogiOn'] == [] and s['mkOn'] == [] and s['vmOn'] == [] and s['cmark'] in ('', None)
    return ok, {'열림': O['open1'], '고른 선택지': s['pick'], '보기 on': s['bogiOn'], '마크 줄 on(#mO~#mP · .vrow)': [s['mkOn'], s['vmOn']], '.cmark': s['cmark'], '회독 수(h)': len(w['h'] or [])}


def j_H3a2(O):
    s = O['s1']; w = O['w1']
    ok = s['layer'] == '4' and s['eye'] is True
    return ok, {'회독 고르개 값': s['layer'], '고르개 항목': s['layerOpts'], '👁(QHIDE) 켬': s['eye']}


def j_H3a3(O):
    s = O['s1']; w = O['w1']; h = w['h'] or []
    last = h[-1] if h else {}
    ok = len(h) == 3 and pure_b(last.get('b')) == B3 and not (w['bogi'] or {}) and w['stamp'] == last.get('t')
    return ok, {'h 길이': len(h), 'h 끝 b': last.get('b'), 'BG[uid]': w['bogi'], '도장 = h 끝 t': w['stamp'] == last.get('t'), '열쇠꼴': w['key']}


def j_H3b(O):
    s2, w2, s3, w3, s4, w4 = O['s2'], O['w2'], O['s3'], O['w3'], O['s4'], O['w4']
    h2 = w2['h'] or []; h4 = w4['h'] or []
    a = O['pick4'] and len(h2) == 4 and h2[-1].get('m') == 'O' and str(h2[-1].get('a')) == '4'
    b = O['bogiG'] and s3['bogiOn'] == ['ㄱO'] and (w3['bogi'] or {}).get('ㄱ') == 'O'
    c = O['reopen'] and s4['pick'] == [] and s4['bogiOn'] == [] and s4['layer'] == '5' and len(h4) == 4 and pure_b(h4[-1].get('b')) == {'ㄱ': 'O'} and not pure_b(w4['bogi'])
    return a and b and c, {'④ 누름 → h 길이·끝': [len(h2), h2[-1].get('m') if h2 else None], 'ㄱ 보기 O': [s3['bogiOn'], w3['bogi']], '가려서 못 누른 자리': O.get('covers'), '다시 열기': {'고른 선택지': s4['pick'], '보기 on': s4['bogiOn'], '회독 고르개': s4['layer'], 'h 길이': len(h4),
                                                                                   'h 끝 b': h4[-1].get('b') if h4 else None, 'BG': w4['bogi'], '.cmark': s4['cmark']}}


def j_H3c(O):
    s0, s1, s2, w2 = O['sx0'], O['sx1'], O['sx2'], O['wx2']
    kx = O['kx']
    ok = O['openX'] and O['bogiX'] and s1['bogiOn'] == [kx + 'O'] and O['reopenX'] and s2['bogiOn'] == [kx + 'O'] and len(w2['h'] or []) == 0 and s2['layer'] == '1'
    return ok, {'열기 전 보기 on': s0['bogiOn'], '누른 뒤': s1['bogiOn'], '닫았다 다시 열기': s2['bogiOn'], 'h 길이': len(w2['h'] or []), '회독 고르개': s2['layer']}


def j_H3d(O):
    if O.get('blocked'):
        return None, {'서랍 줄이 문제 창에 가려 못 누른다(폰 390: 상주 서랍이 창 밑에 깔린다 — PC 칸으로 갈음)': O['blocked']}
    wy1, wy2 = O['wy1'], O['wy2']
    n1 = len(wy1['h'] or []); n2 = len(wy2['h'] or [])
    ok = O['openY'] and O['pickY1'] and n1 == 1 and O['drawZ'] and O['vnoZ'] == O['noZ'] and O['drawY'] and O['sy_back']['vno'] == O['noY'] and O['pickY2'] and n2 == n1 + 1 and O['sy_back']['pick'] == []
    return ok, {'첫 선택지 뒤 h': n1, '서랍으로 Z 로 갔다(VNO)': [O['vnoZ'], O['noZ']], '돌아온 뒤 고른 선택지': O['sy_back']['pick'], '돌아와 선택지 누른 뒤 h': n2, '(쌓임 = 2 · 갈아 끼움 = 1)': [n1, n2], '가려서 못 누른 자리': O.get('covers')}


def sc_H3_dev2(br, eng, app, stat):
    """H-3 기기 둘 — A 에서 보기만 누름 → B 에서 열기 → 그 보기 그대로 (_v 는 기기 저장이 아니라 bogi 칸 안 = 동기화)"""
    uid = 'G24-61-07'
    dA = Dev2(br, eng); dB = Dev2(br, eng)
    try:
        dA.load(app, 'earth', rec={RP: RECB['earth']}, static=stat); dA.settle()
        dA.click('#list .item[data-uid="%s"]' % uid); dA.pg.wait_for_timeout(1300)
        okA = dA.click('#card .bogi .row[data-k="ㄴ"] .ox button[data-v="X"]')
        sA = dA.ev("()=>__U.snap()")
        putA = dA.settle(RP, 1); raw = dA.putraw()
        dB.load(app, 'earth', rec={RP: raw.encode('utf-8')}, static=stat); dB.settle()
        dB.click('#list .item[data-uid="%s"]' % uid); dB.pg.wait_for_timeout(1300)
        sB = dB.ev("()=>__U.snap()")
        return {'okA': okA, 'sA': sA, 'sB': sB, 'wA': cellinfo(putA, uid, int(U2N['earth'][uid]))}
    finally:
        dA.close(); dB.close()


def j_H3e(O):
    ok = O['okA'] and O['sA']['bogiOn'] == ['ㄴX'] and O['sB']['bogiOn'] == O['sA']['bogiOn'] and O['sB']['pick'] == [] and O['sB']['layer'] == '4'
    return ok, {'A 보기 on': O['sA']['bogiOn'], 'B 열기 보기 on': O['sB']['bogiOn'], 'B 고른 선택지': O['sB']['pick'], 'B 회독 고르개': O['sB']['layer'], 'A 가 올린 bogi': O['wA']['bogi']}


def sc_H3_24(br, eng, app, stat):
    """G-3-4 — 지금 있는 〈보기〉 O△X(지학 24칸)는 업데이트 뒤 처음 열 때 그 문항 마지막 회독 h 항목 b 로 옮겨진다(안 지움) · 회독이 0 인 문항은 그대로"""
    F = RECJ['earth']['data']
    dv = Dev2(br, eng)
    try:
        dv.load(app, 'earth', rec={RP: RECB['earth']}, static=stat)
        dv.settle()
        for uid in F['bogi']:
            dv.ev("u=>__U.openRow(u)", uid)
        dv.ev("()=>{try{closeView()}catch(e){}}")
        put = dv.settle()
        out = {}
        for uid, b0 in F['bogi'].items():
            n = U2N['earth'][uid]
            h0 = (F['status'].get(n) or {}).get('h') or []
            ci = cellinfo(put, uid, n)
            out[uid] = {'h0': len(h0), 'h': len(ci['h'] or []), 'b_last': pure_b((ci['h'] or [{}])[-1].get('b')) if ci['h'] else None, 'bogi': pure_b(ci['bogi']), 'b0': pure_b(b0)}
        return {'cells': out, 'errs': dv.errs[:3]}
    finally:
        dv.close()


def j_H3_24(O):
    bad = []; moved = 0; stay = 0
    for uid, c in O['cells'].items():
        if c['h0'] >= 1:
            if c['b_last'] == c['b0'] and not c['bogi'] and c['h'] == c['h0']:
                moved += 1
            else:
                bad.append(uid)
        else:
            if c['bogi'] == c['b0'] and c['h'] == 0:
                stay += 1
            else:
                bad.append(uid)
    return not bad and len(O['cells']) == 24, {'보기 칸 수': len(O['cells']), '마지막 회독 h 끝 b 로 옮겨짐(안 지움)': moved, '회독 0 이라 그대로': stay, '어긋남': bad[:4], '수': len(bad)}


# ══════════ H-4 화면 훑기(규칙 60) ══════════
SWEEP_JS = r"""
window.__U.sweep=function(sel){
  let root=null;if(sel==='@sheet'){const L=[...document.querySelectorAll('.sheet')];root=L.length?L[L.length-1]:null}else root=sel?document.querySelector(sel):document.body;
  if(!root)return null;
  const W=window.innerWidth,H=window.innerHeight;
  const vis=e=>{const r=e.getBoundingClientRect();if(r.width<=0||r.height<=0)return false;const cs=getComputedStyle(e);return cs.display!=='none'&&cs.visibility!=='hidden'&&cs.opacity!=='0'};
  const desc=e=>{let d=e.tagName.toLowerCase();if(e.id)d+='#'+e.id;const c=(typeof e.className==='string'?e.className:'').trim();if(c)d+='.'+c.split(/\s+/).slice(0,2).join('.');return d};
  const scroller=e=>{for(let p=e.parentElement;p;p=p.parentElement){const cs=getComputedStyle(p);if(/(auto|scroll)/.test(cs.overflowX))return true;if(p===document.body)break}return false};
  const all=[...root.querySelectorAll('*')].filter(vis);
  const o={over:new Set(),clip:new Set(),ovl:new Set(),cov:new Set(),small:new Set()};
  for(const e of all){const r=e.getBoundingClientRect();const cs=getComputedStyle(e);
    if((r.right>W+1||r.left<-1)&&!scroller(e))o.over.add(desc(e));
    if(e.children.length===0&&(e.textContent||'').trim()&&e.scrollWidth>e.clientWidth+1&&/(hidden|clip)/.test(cs.overflowX)&&cs.textOverflow!=='ellipsis')o.clip.add(desc(e))}
  const ints=all.filter(e=>e.matches('button,a[href],select,input,textarea,[data-v],[data-vmark],[data-c],[data-go],.tag[data-page],.tag[data-unit],#gpMot')&&!e.closest('#list,#spec,#ndList'));
  const iv=ints.filter(e=>{const r=e.getBoundingClientRect();return r.bottom>0&&r.top<H&&r.right>0&&r.left<W});
  for(let i=0;i<iv.length;i++){const a=iv[i],ra=a.getBoundingClientRect();
    if(Math.min(ra.width,ra.height)<24)o.small.add(desc(a));
    const cx=ra.left+ra.width/2,cy=ra.top+ra.height/2;
    if(cx>=0&&cx<W&&cy>=0&&cy<H){const t=document.elementFromPoint(cx,cy);if(t&&t!==a&&!a.contains(t)&&!t.contains(a))o.cov.add(desc(a)+'<-'+desc(t))}
    for(let j=i+1;j<iv.length;j++){const b=iv[j];if(a.contains(b)||b.contains(a))continue;const rb=b.getBoundingClientRect();
      const w=Math.min(ra.right,rb.right)-Math.max(ra.left,rb.left),h=Math.min(ra.bottom,rb.bottom)-Math.max(ra.top,rb.top);
      if(w>3&&h>3)o.ovl.add(desc(a)+'×'+desc(b))}}
  return {hscroll:document.documentElement.scrollWidth-W,over:[...o.over],clip:[...o.clip],ovl:[...o.ovl],cov:[...o.cov],small:[...o.small],n:all.length,iv:iv.length}
};
"""


def sc_sweep(br, eng, app, stat, w):
    h = 844 if w <= 400 else 900
    dv = Dev2(br, eng, vp=(w, h), touch=(w <= 400))
    try:
        dv.load(app, 'earth', rec={RP: dumps(E_rec())}, static=stat)
        dv.ev(SWEEP_JS)
        dv.settle()
        O = {'w': w}
        O['first'] = dv.ev("()=>__U.sweep('body')")
        dv.ev("u=>__U.openRow(u)", 'G24-61-07'); dv.pg.wait_for_timeout(800)
        O['card'] = dv.ev("()=>__U.sweep('#view')")
        dv.ev("()=>{try{closeView()}catch(e){}}")
        dv.ev("u=>__U.openRow(u)", 'G06-43-10'); dv.pg.wait_for_timeout(600)
        dv.click('#tGpt'); dv.pg.wait_for_timeout(900)
        O['claude'] = dv.ev("()=>__U.sweep('@sheet')")
        if dv.click('#gpMot'):
            dv.pg.wait_for_timeout(1500)
            O['claude+mot'] = dv.ev("()=>__U.sweep('@sheet')")
        else:
            O['claude+mot'] = O['claude']
        O['errs'] = dv.errs[:3]
        return O
    finally:
        dv.close()


def j_sweep(ON, OB):
    new = {}; abs_n = {}; old = {}
    for surf in ('first', 'card', 'claude', 'claude+mot'):
        a, b = ON.get(surf), OB.get(surf)
        if a is None or b is None:
            new[surf] = '면을 못 열었다(NEW %s · 바탕 %s)' % (a is not None, b is not None)
            continue
        for cat in ('over', 'clip', 'ovl', 'cov'):
            nn = sorted(set(a[cat]) - set(b[cat]))
            if nn:
                new['%s/%s' % (surf, cat)] = nn[:3]
            if a[cat]:
                abs_n['%s/%s' % (surf, cat)] = len(a[cat])
            if b[cat]:
                old['%s/%s' % (surf, cat)] = len(b[cat])
        if a['hscroll'] > 1 and b['hscroll'] <= 1:
            new['%s/가로 굴림' % surf] = a['hscroll']
    return not new, {'판 결함(바탕에 없던 넘침·잘림·겹침·가려짐)': new, '지금 있는 것(칸/수)': abs_n, '바탕부터 있던 흠(수)': old,
                     '누르기 작은 것(<24px)': {s: len((ON.get(s) or {}).get('small') or []) for s in ('first', 'card', 'claude')}}


# ══════════ 정적 칸 ══════════
def static_gates():
    eng = '-'
    # 고정본 · 지시서 0 실측
    e, b = RECB['earth'], RECB['bio']
    F = RECJ['earth']
    R(eng, 'S-1 고정본 — studyplandata %s earth/기록.json md5 = 지시서 0-5(b9e41f03…) · bio(18d0775f…) · status 칸·h 합·gpt·mcard·u·gone' % FIXC,
      md5(e) == 'b9e41f03aacd6c382326f547cd16c9dc' and md5(b) == '18d0775f1f104c5d3c9df91c63c5c349' and len(F['data']['status']) == 63 and hsum(F['data']['status']) == 66 and len(F['data']['gpt']) == 4
      and len(F['data']['mcard']) == 3 and len(F['u']) == 478 and len(F['gone']) == 380 and sorted(k for k in F['gone'] if k.startswith('status|')) == ['status|260'], None,
      {'earth md5': md5(e)[:8], 'bio md5': md5(b)[:8], 'status': len(F['data']['status']), 'h 합': hsum(F['data']['status']), 'gpt': sorted(F['data']['gpt']), 'mcard': sorted(F['data']['mcard']), 'u': len(F['u']), 'gone': len(F['gone']),
       '번호 아닌 통 0칸(note·qtype·conc·twin·ansfix·frm·maskpos·omrpos·link)': {k: len(F['data'].get(k) or {}) for k in ('note', 'qtype', 'conc', 'twin', 'ansfix', 'frm', 'maskpos', 'omrpos', 'link')}})
    okn, dn = j_anchor_table()
    R(eng, 'S-2 닻 — 문항.json 지금 판의 번호 → uid = 지시서 0-6 표(84·111·119·149) · gpt 글 첫 줄이 그 uid', okn and all(F['data']['gpt'][n].startswith(u + ' ·') for n, u, _ in ANCH), None, dn)
    okn, dn = j_E_mat_static()
    R(eng, 'S-3 재료 넷(claude_motion) — 크기·md5·첫 줄·절·글머리·| 줄·굵게·Q 줄 = 지시서 D-2 표', okn, None, dn)
    ok319 = all(r['uid'].split('-')[1] == str(r['회차']) and int(r['uid'].split('-')[2]) == int(r['문번']) for r in ITEMS['earth'] if UIDRE.match(r['uid']))
    bad = [r['uid'] for r in ITEMS['earth'] if UIDRE.match(r['uid']) and not (r['uid'].split('-')[1] == str(r['회차']) and int(r['uid'].split('-')[2]) == int(r['문번']))]
    R(eng, 'S-4 지학 기출 %d — uid 의 회·번 = 데이터 「회차」·「문번」(어긋남 %d) → 「NN회 N번」을 걷어도 빠지는 정보 없음(지시서 G 0-8)' % (len(KIND_G['earth']), len(bad)), ok319 and len(KIND_G['earth']) == 319, None, {'기출 수': len(KIND_G['earth']), '어긋남': bad[:3]})
    for uid in MATS:
        pass
    ok_t = all(title_rule(u) == '%s Claude · %s' % (u, TITLE_END[u]) for u in MATS)
    R(eng, 'S-5 제목 규칙(지시서 C-1)을 데이터에서 계산한 값 = C-1 표(%s)' % ' · '.join(TITLE_END.values()), ok_t, None, {u: title_rule(u) for u in MATS})
    # 모션 재료(D-1) — NEW 와 바탕의 motion 폴더(LF 기준 바이트 대조)
    sb = APPS['BASE'][1] if QC.GATE else None   # regress — 바탕(4754b1d) 모션 폴더 안 풂
    for who in (('NEW', 'BASE') if QC.GATE else ('NEW',)):   # regress — [BASE] 줄(INFO · 관문만) 건넘
        stt = APPS[who][1]
        try:
            ix = json.loads(stt['motion/index.json'])
        except Exception:
            ix = {}
        names = sorted(k[7:] for k in stt)
        want_ix = {'phys': [72, 97], 'earth': ['G09-46-10', 'G03-40-05', 'G06-43-02', 'G06-43-10']}
        # 옛 줄: files_ok = all(('earth_%s.html' % u) in names and stt['motion/earth_%s.html' % u] == sb['motion/' + MOTMD5[u][0]] for u in MATS)   # git mv — 옛 이름 파일과 바이트 같음
        def _hfix(b0, u):   # ★ 채팅 10/4 23:1x ② — 「크게 보기 ↗」 href 한 곳만 새 이름(그 밖 바이트 무변)
            o = ('href="%s"' % MOTMD5[u][0]).encode()
            return b0.replace(o, ('href="earth_%s.html"' % u).encode()) if b0 and b0.count(o) == 1 else None
        files_ok = all(('earth_%s.html' % u) in names and stt['motion/earth_%s.html' % u] == _hfix(sb['motion/' + MOTMD5[u][0]], u) for u in MATS) if QC.GATE else \
            all(('earth_%s.html' % u) in names and QC.same('S-6.motion/' + u, md5(stt['motion/earth_%s.html' % u])) for u in MATS)   # regress — 새 이름 파일 바이트 = 기준 스냅샷(앞 인도판 같은 파일 md5 · 바탕 옛 이름 파일 대신)
        href_old = [u for u in MATS if ('earth_%s.html' % u) in names and ('href="%s"' % MOTMD5[u][0]).encode() in stt['motion/earth_%s.html' % u]]
        oldf = [MOTMD5[u][0] for u in MATS if MOTMD5[u][0] in names]
        R(eng, 'S-6 motion(D-1) [%s] — index.json = 지시서 D-1 · earth_<uid>.html 넷 = 옛 earth_<번호>.html 바이트(LF 기준) · 옛 이름 0 · .pdf 0' % who,
          (ix == want_ix and files_ok and not oldf and not href_old and not [k for k in stt if k.lower().endswith('.pdf')]) if who == 'NEW' else None, None,
          {'index.json': ix, '새 이름 파일': [n for n in names if n.startswith('earth_G')], '옛 이름 남음': oldf, '바이트 같음(href 한 곳 뺌)': files_ok, '옛 이름 href 남음': href_old,
           '지시서 0-7 md5(작업트리 줄끝 기준)': {u: MOTMD5[u][2][:8] for u in MATS}})


# ══════════ 묶음 ══════════
def run_B(br, eng):
    on = OBS('main', sc_main, br, eng, 'NEW') if not QC.SMOKE else OBS('main', sc_main, br, eng, 'NEW', second=False); ob = OBS('main', sc_main, br, eng, 'BASE')   # smoke — 두 번째 열기 없음
    GATE(eng, 'B-1 셈 무변 — 지학 원격 사본(고정본)을 실은 빈 기기 열고 동기화 뒤: status · gpt · mcard · 다른 통 칸 수·h 합 = 고정본(지시서 63·66·4·3)', j_B1_count, on, ob)
    if QC.SMOKE:   # smoke — B-1 셈 무변(동기화 한 바퀴)만
        return
    GATE(eng, 'B-1 열쇠 — 번호 열쇠 통(status·note·qtype·conc·gpt·twin·ansfix·frm·maskpos·omrpos·mcard·link) 열쇠 전부 uid · 번호 열쇠 0(올린 몸통 · 메모리 · IndexedDB)', j_B1_keys, on, ob)
    GATE(eng, 'B-1 메모리 통 = 올린 몸통(번호 열쇠 통)', j_B1_mem, on, ob)
    GATE(eng, 'B-1 불변 — bogi·unit·bpg·crop·tfix·gg·ggref·pick·bref·bpit·txt 칸 수·값 = 고정본 바이트(bref·bpit 열쇠는 쪽 그대로)', j_B1_stay, on, ob)
    GATE(eng, 'B-2 닻 — gpt 열쇠 = G03-40-05·G06-43-02·G06-43-10·G09-46-10 · 글 = 옮기기 전 84·111·119·149 글(바이트) · 글 첫 줄이 그 uid', j_B2_gpt, on, ob)
    GATE(eng, 'B-2 닻 — status 63칸 h 배열 = 옮기기 전 같은 문항 h(t·m·s·a·auto 전부) · 도장 u(status·gpt·mcard)는 옛 칸 값 그대로', j_B2_h, on, ob)
    GATE(eng, 'B-2 묘비 — 옛 칸 「키|번호」 묘비(지금 시각) · 번호 묘비 status|260 → status|<uid> 비춤 · 원래 묘비 무변 · 다른 묘비 안 늘고 · 옛 도장 안 남음', j_B2_tomb, on, ob)
    GATE(eng, 'B-2 도장 규칙 — status 도장 = h 끝 t(stTime) 그대로(새로 안 찍음)', j_B2_h_stamp, on, ob)
    GATE(eng, 'B-2 그림자 — shadow 의 번호 열쇠 통도 새 열쇠로(번호 열쇠 0 · 올린 몸통과 열쇠 같음)', j_B2_shadow, on, ob)
    GATE2(eng, 'B-3 화면 무변 — 옮긴 뒤 지학 목록(%d줄 전부 · 고르게 50 포함)·서랍·히트맵·카운터(회독 수·O△X 칩·🃏·근거 칩·Claude 태그)가 바탕 화면과 같다(「N회독」 칩 · 「NN회 N번」 · 서랍 마크 줄만 뺌 — ④ 몫)' % len((ob if QC.GATE else on).get('screen', {}).get('rows', {})) if (ob if QC.GATE else on) and 'screen' in (ob if QC.GATE else on) else 'B-3 화면 무변', j_screen_eq, on, ob)   # regress — 바탕 관찰 없음 → 칸 이름의 줄 수는 새 판 관찰에서(gate 와 같은 칸 id)
    GATE(eng, 'B-6 두 번째 열기 — 올린 data·u·gone 이 첫 열기와 같다(옮김 0 · 묘비 비춤 0 · 도장 새로 0) · bak_uid 는 한 번만(두 번째에 안 바뀜)', j_idem, on, ob)
    GATE(eng, 'B-6 bak_uid — 처음 옮길 때 한 번 IndexedDB kv.bak_uid = {at · 통별 옛 값 전부 · u · gone}(옛 값 status 14 가 들어 있다)', j_bak, on, ob)
    # 옛 기록 있는 기기 — 옛 판(바탕)으로 고정본을 받아 둔 기기를 새 판으로 연다(「열 때」 옮김 · 병합 뒤 옮김과 갈래가 다르다)
    if QC.GATE:   # 옛 판 기기 흉내(바탕 앱 4754b1d 로 먼저 받아 둠 = 바탕 띄움) — uid 옮김 판에만 뜻 · regress 끔(관문만)
        oo = OBS('olddev', sc_main, br, eng, 'NEW', prior_old=True, second=False); oob = OBS('olddev', sc_main, br, eng, 'BASE', prior_old=True, second=False)
        GATE(eng, 'B-1 옛 기록 있는 기기(열 때 옮김) — 칸 수·h 합 = 고정본 · 번호 열쇠 통 열쇠 전부 uid(올린 몸통·메모리·IndexedDB)', lambda O: (j_B1_count(O)[0] and j_B1_keys(O)[0], {'셈': j_B1_count(O)[1], '열쇠': j_B1_keys(O)[1]}), oo, oob)
        GATE(eng, 'B-1 옛 기록 있는 기기(열 때 옮김) — 불변 통 = 고정본 바이트', j_B1_stay, oo, oob)
        GATE(eng, 'B-2 옛 기록 있는 기기(열 때 옮김) — gpt 닻 · status 63칸 h · 도장 그대로', lambda O: (j_B2_gpt(O)[0] and j_B2_h(O)[0], {'gpt': j_B2_gpt(O)[1], 'status·도장': j_B2_h(O)[1]}), oo, oob)
        GATE(eng, 'B-2 옛 기록 있는 기기(열 때 옮김) — 옛 칸 묘비(지금 시각) · 번호 묘비 비춤 · 늘어난 묘비 0 · 옛 도장 안 남음', j_B2_tomb, oo, oob)
        GATE(eng, 'B-6 옛 기록 있는 기기(열 때 옮김) — bak_uid 한 번 찍힘 = 옮기기 전 옛 값(번호 열쇠) 사본', j_bak, oo, oob)
    # 합성 기록 — 값 속 번호 · 나머지 통
    sn = OBS('syn', sc_syn, br, eng, 'NEW'); sb = OBS('syn', sc_syn, br, eng, 'BASE')
    GATE(eng, 'B-1 합성 기록 — 번호 열쇠 통(note·qtype·conc·twin·ansfix)에 칸을 더해 먹임: 열쇠 uid · 값 속 번호(twin)도 uid · 도장 그대로 · 옛 칸 묘비 · 번호 아닌 열쇠(omrpos「def」)는 그대로', j_syn_mig, sn, sb)
    GATE(eng, 'B-1 합성 기록(참고) — maskpos·omrpos(PDF 뷰어 통)·ansfix 번호 칸 → uid 로 옮겨졌나', j_syn_info, sn, sb)
    GATE2(eng, 'B-3 합성 기록 화면 — 코멘트(서랍 🗒)·목록·히트맵이 바탕과 같다(note 3칸 · twin · qtype · conc 더한 기록)', j_screen_eq, sn, sb)
    # B-4
    od = OBS('order', sc_order, br, eng, 'NEW'); odb = OBS('order', sc_order, br, eng, 'BASE')
    def j_B4a(O):
        s = O['sheet'] or {}; rd = s.get('text', '')
        ok = s.get('read') and 'G06-43-10 · 2006' in rd and O['n'][1] == O['n'][0] + 1
        return ok, {'DATA 수': O['n'], '가짜 끼운 뒤 G06-43-10 의 번호': O['no'], '창': {'read': s.get('read'), '글 앞머리': rd[:60]}, '옛 번호 119 자리 문항': O['uid_at119']}
    GATE(eng, 'B-4 문항 순서 — 문항.json 앞에 가짜 문항을 끼워 다시 열어도 G06-43-10 창의 Claude 풀이가 G06-43-10 에 뜬다(옛 판은 밀려간다 = 헛잣대)', j_B4a, od, odb)
    def j_B4b(O):
        gp0, gp1 = O['gp0'], O['gp1']
        ok = gp1 == gp0 == sorted(MATS) and True
        return ok, {'.tag.gp 줄(끼우기 앞)': gp0, '(끼운 뒤)': gp1}
    GATE(eng, 'B-4 문항 순서 — 끼운 뒤에도 Claude 태그(.tag.gp)가 네 uid 줄에만 있다', j_B4b, od, odb)
    def j_B4c(O):
        a = O['scr0']['rows']; b = {u: v for u, v in O['scr1']['rows'].items() if u != 'G99-99-99'}
        diff = [u for u in a if a[u] != b.get(u)]
        d0 = O['scr0']['drawer']; d1 = {u: v for u, v in O['scr1']['drawer'].items() if u != 'G99-99-99'}
        dd = [u for u in d0 if d0[u] != d1.get(u)]
        return not diff and not dd and len(a) > 0 and len(O['scr1']['rows']) == len(a) + 1, {'목록 줄 수': [len(a), len(O['scr1']['rows'])], '기록이 따라가지 않은 줄(전수)': diff[:4], '수': len(diff), '서랍 어긋남': dd[:3]}
    GATE(eng, 'B-4 문항 순서 — 가짜 문항을 끼워도 모든 문항(%d줄)의 마크·회독 수·Claude 태그·🃏·근거 칩이 같은 uid 에 붙어 있다' % len(od.get('scr0', {}).get('rows', {})) if 'scr0' in od else 'B-4 순서', j_B4c, od, odb)
    # B-5
    if QC.GATE:   # 옛 판 기기 섞기(기기 B = 바탕 앱 4754b1d) — uid 옮김 판에만 뜻 · regress 끔(관문만)
        mx = OBS('mix', sc_mix, br, eng, 'NEW'); mxb = OBS('mix', sc_mix, br, eng, 'BASE')
        GATE(eng, 'B-5 옛 판 기기 섞기 — A(새 판)가 옮기고 올림 → B(옛 판)가 옛 로컬로 status|84 를 고쳐 올림 → A 가 다시 병합: status|G03-40-05 = B 의 고친 값(도장이 늦어서) · 번호 칸 다시 0 · 반대 차례(B 먼저)도 같은 결과', j_mix, mx, mxb)
    wr = OBS('writes', sc_writes, br, eng, 'NEW'); wrb = OBS('writes', sc_writes, br, eng, 'BASE')
    GATE(eng, 'B-5 새 판은 번호 열쇠를 쓰지 않는다 — 마크(O)·코멘트·Claude 풀이를 진짜 눌러 저장한 뒤 올린 몸통·IndexedDB kv 열쇠 = uid · ink 통 번호 열쇠 0 · 콘솔 오류 0', j_writes, wr, wrb)
    # B-6 생물 · 물리
    bi = OBS('bio', sc_bio, br, eng, 'NEW'); bib = OBS('bio', sc_bio, br, eng, 'BASE')
    GATE(eng, 'B-6 생물 빈 기록 — 올린 data = 고정본(전 칸 0) · u·gone 0 = 옮김 0', j_bio, bi, bib)
    ph = OBS('phys', sc_phys, br, eng, 'NEW'); phb = OBS('phys', sc_phys, br, eng, 'BASE')
    GATE2(eng, 'B-6 물리 기록 바이트 무변 — 올린 data·u·gone = 바탕(근거 난수 k 뺌)', j_phys_body, ph, phb)
    GATE2(eng, 'B-6 물리 화면 무변 — 목록 30줄(고르게)·서랍 30줄·카운터 DOM 글자 = 바탕', j_phys_screen, ph, phb)


def run_E(br, eng):
    en = OBS('E', sc_E, br, eng, 'NEW'); eb = OBS('E', sc_E, br, eng, 'BASE')
    if QC.REGRESS:   # regress — 바탕 관찰 없음(아래 'wins' in eb 가드가 바탕 칸을 — 로)
        eb = {}
    if 'wins' not in en:
        R(eng, 'E-1 창 — 시나리오가 안 돌았다', False, None, en.get('__err'))
        return
    if QC.SMOKE:   # smoke — E-1 창 제목(첫 uid 하나)만
        for uid in list(MATS)[:1]:
            GATE(eng, 'E-1 창 %s — 제목 = 「%s」(C-1 표 · 「번호」 글자 0)' % (uid, '%s Claude · %s' % (uid, TITLE_END[uid])), lambda O, u=uid: j_E1_title(O, u), en, None)
        return
    for uid in MATS:
        GATE(eng, 'E-1 창 %s — 제목 = 「%s」(C-1 표 · 「번호」 글자 0)' % (uid, '%s Claude · %s' % (uid, TITLE_END[uid])), lambda O, u=uid: j_E1_title(O, u), en, eb if 'wins' in eb else None)
        GATE(eng, 'E-1 창 %s — 둘째 줄 = flex·baseline·8px · 왼쪽 span = 「%s」(D-2 표 첫 줄) · 옛 #gpMotBar 줄 0' % (uid, MATS[uid][3]), lambda O, u=uid: j_E1_line2(O, u), en, eb if 'wins' in eb else None)
        GATE(eng, 'E-1 창 %s — 오른쪽 「▶ 모션」(테두리·안쪽 여백 0 · 13px) → 눌러 iframe motion/earth_%s.html 200 · 480px · 그 줄 아래 · 글자 「▼ 모션 닫기」' % (uid, uid), lambda O, u=uid: j_E1_mot(O, u), en, eb if 'wins' in eb else None)
    GATE(eng, 'E-1 「▶ 모션」은 네 창에만 — 앞뒤 문항(118·120 자리 uid 등) 창에는 단추 0', j_E1_nb, en, eb if 'wins' in eb else None)
    GATE(eng, 'E-1 콘솔 — 모션 iframe 쪽 오류 0 · pageerror 0', j_E1_err, en, eb if 'wins' in eb else None)
    for uid in MATS:
        GATE(eng, 'E-2 읽기 판 %s — h3.gph 5(①~⑤ 차례 · ⑥ 0 · 재료 절 이름과 같음) · 첫 p.gpp 가 <b>Q 로 시작 · QA 줄 본문에 0 · table.gptb 1 · script 0 · 글머리·표·굵게 셈 = 재료 · 본문 줄 전부 보임' % uid, lambda O, u=uid: j_E2(O, u), en, eb if 'wins' in eb else None)
    GATE(eng, 'E-3 기기 둘 — 빈 기기: 동기화 + 옮김 뒤 올린 gpt[uid] = 재료 글자 전수(%d·%d·%d·%d자) · 번호 gpt 칸 0 · 재료 도장 그대로' % tuple(MATS[u][1] for u in MATS), j_E3, en, eb if 'wins' in eb else None)
    if QC.GATE:   # 옛 기록 있는 기기(바탕 앱 4754b1d 로 먼저 받아 둠 = 바탕 띄움) — uid 옮김 판에만 뜻 · regress 끔(관문만)
        eo = OBS('Eold', sc_E_old, br, eng, 'NEW'); ebo = OBS('Eold', sc_E_old, br, eng, 'BASE')
        GATE(eng, 'E-3 기기 둘 — 옛 기록 있는 기기(옛 판으로 고정본을 받아 둠 → 새 판): 옛 글(번호 칸)이 새 글을 못 이긴다 · gpt[uid] = 재료 · 번호 칸 0', j_E3_old, eo, ebo)
    GATE(eng, 'E-4 목록 — .tag.gp 는 네 uid 줄에만', j_E4, en, eb if 'wins' in eb else None)
    ph = OBS('phys', sc_phys, br, eng, 'NEW'); phb = OBS('phys', sc_phys, br, eng, 'BASE')
    GATE2(eng, 'E-5 물리 무변 — 물리 #72 · #97 창 DOM = 바탕(제목 「72번 Claude 풀이」 · 「▶ 모션」 단추 줄 · phys_72.html 200)', j_E5, ph, phb)


def run_H(br, eng):
    h1 = OBS('H1', sc_H1, br, eng, 'NEW'); h1b = OBS('H1', sc_H1, br, eng, 'BASE')
    GATE(eng, 'H-1 회·번 — 서랍 기출 줄 .ndt = 「uid」 · 목록 카드 .meta .sub 안 그림 · #vT1 = 「G25-62-09 (2025)」 · .cmeta 칩 안 그림 · 암기카드·🃏·정리·근거 쓰임·검색 면에도 「NN회 N번」 0', j_H1, h1, h1b)
    GATE2(eng, 'H-1 확인문제 줄 무변 — 목록 .sub·칩 · 서랍 .ndt 가 바탕과 같다(「N장 확인문제 M번」 그대로)', j_H1_ec, h1, h1b)
    hb = OBS('H1bio', sc_H1_bio, br, eng, 'NEW'); hbb = OBS('H1bio', sc_H1_bio, br, eng, 'BASE')
    # 옛 줄: GATE(eng, 'H-1 생물 기출 표본(가짜 기록) — 서랍 .ndt = uid · 목록 .sub 0 · #vT1 = 「uid (연도)」 · 「N회독」 칩 0', j_H1_bio, hb, hbb)
    GATE(eng, 'H-1 생물 기출 표본(가짜 기록) — 회·번 그대로(G-1 지학만 · 채팅 10/4 23:1x (가)) · 서랍 .ndt = 「uid · 제목」 · 목록 .sub 있음 · #vT1 = 「uid · 제목 (연도)」 · 「N회독」 칩 0', j_H1_bio, hb, hbb)
    GATE(eng, 'H-2 칩 — 카드 층 목록 줄 「N회독」 칩 0(지학)', j_H2_chips, h1, h1b)
    GATE(eng, 'H-2 칩 — 카드 층 목록 줄 「N회독」 칩 0(생물 표본 기록)', j_H2_chips, hb, hbb)
    ph = OBS('phys', sc_phys, br, eng, 'NEW'); phb = OBS('phys', sc_phys, br, eng, 'BASE')
    GATE2(eng, 'H-2 물리 목록 「N회독」 칩 무변 — 칩 수 = 바탕(> 0)', j_H2_phys, ph, phb)
    GATE(eng, 'H-2 서랍 마크 — G24-61-07 줄 = 덜약점 점 + 「O △ O」(ndm ndmO·ndmQ·ndmO) · 줄마다 마크 수 = h 길이 · 덜약점 점 무변', j_H2_drawer, h1, h1b)
    GATE(eng, 'H-2 서랍 마크(생물 표본) — 가짜 기록 두 회독 줄 = 「X O」', j_H2_bio, hb, hbb)
    for phone in (False, True):
        tag = '폰 390×844 손가락' if phone else 'PC 1280×900 마우스'
        s3 = OBS('H3', sc_H3, br, eng, 'NEW', phone=phone); s3b = OBS('H3', sc_H3, br, eng, 'BASE', phone=phone)
        GATE(eng, 'H-3 다음 회독(%s) ① G24-61-07 처음 열기 — 고른 선택지 0 · 보기 on 0 · 마크 줄 on 0 · .cmark 빈칸' % tag, j_H3a, s3, s3b)
        GATE(eng, 'H-3 다음 회독(%s) ① 회독 고르개 4 · 👁 켬(지난 필기는 👁 로 본다)' % tag, j_H3a2, s3, s3b)
        GATE(eng, 'H-3 다음 회독(%s) ① 지난 보기 = h 끝 b {ㄱO ㄴO ㄷX}(옮김 · 안 지움) · BG 비움 · 회독 3 그대로 · 도장 = h 끝 t' % tag, j_H3a3, s3, s3b)
        GATE(eng, 'H-3 다음 회독(%s) ② ④ 누름 → O 기록(h 4) → ㄱ 보기 O → 닫기 → 다시 열기: 고른 선택지 0 · 보기 on 0 · 회독 고르개 5 · h 끝 b = {ㄱ:O}' % tag, j_H3b, s3, s3b)
        GATE(eng, 'H-3 다음 회독(%s) ③ 보기만 누르고 답 체크 없이 닫기 → 다시 열기 → 그 보기 그대로(이어감 · 회독 안 쌓임)' % tag, j_H3c, s3, s3b)
        GATE(eng, 'H-3 다음 회독(%s) ④ 창 열린 채 서랍 줄로 다른 문항 → 돌아와 선택지 누름 → 새 회독으로 쌓임(바탕은 갈아 끼움 = FAIL)' % tag, j_H3d, s3, s3b)
    c24 = OBS('H3_24', sc_H3_24, br, eng, 'NEW'); c24b = OBS('H3_24', sc_H3_24, br, eng, 'BASE')
    GATE(eng, 'H-3 지금 있는 〈보기〉 O△X 24칸 — 업데이트 뒤 처음 열 때 마지막 회독 h 끝 b 로 옮겨짐(안 지움 · 회독 0 인 문항은 그대로)', j_H3_24, c24, c24b)
    d2 = OBS('H3dev2', sc_H3_dev2, br, eng, 'NEW'); d2b = OBS('H3dev2', sc_H3_dev2, br, eng, 'BASE')
    GATE(eng, 'H-3 기기 둘 — A 에서 보기만 누름 → B(빈 기기)에서 열기 → 그 보기 그대로(_v 는 bogi 칸 안 = 동기화)', j_H3e, d2, d2b)
    for w in WIDTHS:
        sw = OBS('sweep', sc_sweep, br, eng, 'NEW', w=w); swb = OBS('sweep', sc_sweep, br, eng, 'BASE', w=w)
        GATE2(eng, 'H-4 화면 훑기(규칙 60) 폭 %d — 지학 첫 화면 · 문제 창 · Claude 창(모션 연 뒤까지): 판 결함 0(가로 넘침 · 잘림 · 겹침 · 가려진 단추 — 바탕에 없던 것)' % w, j_sweep, sw, swb)


def hetjassdae():
    """B-7 · E-6 · H-5 헛잣대 — 바탕에서 지시서가 못 박은 칸이 FAIL 인가(바탕 칸 = FAIL)"""
    def pick(prefixes):
        # ③(보기만 누르고 닫았다 열면 이어감)은 바탕도 같은 동작이라 헛잣대 칸이 아니다 — 센 칸에서 뺀다
        return [(r[0], r[1][:40], r[3]) for r in ROWS if any(r[1].startswith(p) for p in prefixes) and r[3] is not None and '③ 보기만' not in r[1]]
    groups = [('B-7 헛잣대 — 바탕(이 판 앞 index.html)에서 B-2(닻 · 묘비) · B-4(문항 순서)가 FAIL', ('B-2 닻', 'B-2 묘비', 'B-4')),
              ('E-6 헛잣대 — 바탕(커밋 ① 앞)에서 E-1(창 · 제목 · 둘째 줄 · 모션) · E-2(읽기 판) · E-3(기기 둘)이 FAIL', ('E-1 창', 'E-2', 'E-3')),
              ('H-5 헛잣대 — 바탕에서 H-1(회·번) · H-2(칩·마크) · H-3(다음 회독)이 FAIL', ('H-1 회·번', 'H-1 생물', 'H-2 칩', 'H-2 서랍', 'H-3 다음 회독'))]
    for name, pref in groups:
        L = pick(pref)
        if not L:
            continue
        stands = [x for x in L if x[2] is False]
        okgroup = all(x[2] is False for x in L)
        R('-', name, okgroup, None, {'바탕에서 FAIL': len(stands), '바탕에서 PASS(헛잣대가 안 서는 칸)': [(e, n) for e, n, o in L if o is True][:6], '칸 수': len(L)})


def main():
    t0 = time.time()
    appN = app_at(GENIE0, REV) if REV else app_at(ROOT); statN = stat_at(GENIE0, REV) if REV else stat_at(ROOT)
    if QC.GATE:   # 바탕(4754b1d) 앱 · 모션 풀기(git show · ls-tree) — 헛잣대 · 「= 바탕」 기댓값 재료
        QC.sub('git:show-app'); QC.sub('git:ls-tree')
        appB = app_at(GENIE0, BASE_REV); statB = stat_at(GENIE0, BASE_REV)
    else:   # regress — 바탕 풀기 0 · 바탕 시나리오 0(OBS) · 「= 바탕」 칸 = 기준 스냅샷
        appB, statB = b'', {}
    APPS['NEW'] = (appN, statN); APPS['BASE'] = (appB, statB)
    ident = lambda a, s: md5(a) + md5(json.dumps({k: md5(v) for k, v in sorted(s.items())}).encode())
    IDENT['NEW'] = ident(appN, statN); IDENT['BASE'] = ident(appB, statB)
    same = IDENT['NEW'] == IDENT['BASE']
    print('NEW = %s jagwa/index.html(LF %d B · md5 %s) · BASE = genie %s(LF %d B · md5 %s) · %s · 고정본 studyplandata %s · 엔진 %s · 묶음 %s' % (
        ('genie 커밋 ' + REV) if REV else ROOT, len(appN), md5(appN)[:8], BASE_REV, len(appB), md5(appB)[:8], '앱·모션 같음(바탕 그대로 돌림 — 헛잣대가 서는지가 곧 이 줄)' if same else '앱 다름', FIXC, ','.join(ENGS), ','.join(ONLY)), flush=True)
    if ('B' in ONLY or 'E' in ONLY or 'H' in ONLY) and not QC.SMOKE:   # smoke — 정적 칸 건넘
        static_gates()
    with sync_playwright() as pw:
        for eng in (ENGS if not QC.SMOKE else [e for e in ENGS if e == 'chromium'][:1]):   # smoke — chromium 한 판
            br = getattr(pw, eng).launch()
            try:
                for g, fn in ((('B', run_B), ('E', run_E), ('H', run_H)) if not QC.SMOKE else (('B', run_B), ('E', run_E))):   # smoke — H 묶음 smoke 칸 없음
                    if g in ONLY:
                        print('── %s · %s' % (eng, g), flush=True)
                        try:
                            fn(br, eng)
                        except Exception as e:
                            import traceback
                            R(eng, '%s 묶음 멈춤' % g, False, None, repr(e)[:300] + ' @' + traceback.format_exc().strip().split('\n')[-3][:200])
            finally:
                br.close()
    if QC.GATE:   # 헛잣대 셈(B-7 · E-6 · H-5 — 바탕 칸이 FAIL 인가) — regress 는 바탕 칸이 없어 0
        hetjassdae()
    for eng in ENGS + ['-']:
        c = {}
        for r in ROWS:
            if r[0] != eng:
                continue
            g = r[1][:1]
            if g in 'BEHS':
                c[g] = c.get(g, 0) + 1
        if c and eng != '-':
            R(eng, '묶음별 칸 수 — B(기록 열쇠 uid) %d · E(Claude 창·재료) %d · H(목록·서랍·문제 창·다음 회독) %d' % (c.get('B', 0), c.get('E', 0), c.get('H', 0)), None, None, c)
    npass = sum(1 for r in ROWS if r[2] is True); nfail = sum(1 for r in ROWS if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as fo:
        fo.write('\n==== %s · jagwa_uid_unify UU(하네스 md5 %s) · NEW %s(md5 %s) · 바탕 genie %s(md5 %s) · %s · 고정본 %s · genie ROOT HEAD %s · 엔진 %s · 묶음 %s ====\n' % (
            time.strftime('%Y-%m-%d %H:%M'), md5(open(os.path.abspath(__file__), 'rb').read())[:8], ('genie 커밋 ' + REV) if REV else ROOT, md5(appN)[:8], BASE_REV, md5(appB)[:8], '앱·모션 같음(바탕 그대로)' if same else '앱 다름', FIXC, REV or git1(ROOT, 'rev-parse', '--short', 'HEAD'), ','.join(ENGS), ','.join(ONLY)))
        for eng, nm, okn, okb, v in ROWS:
            fo.write('%s | 바탕 %s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[okn], {True: 'PASS', False: 'FAIL', None: '—'}[okb], eng, nm,
                     (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str))[:1500]))
        fo.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
