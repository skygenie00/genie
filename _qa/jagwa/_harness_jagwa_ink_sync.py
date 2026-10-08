# -*- coding: utf-8 -*-
r"""_task_jagwa_ink_sync §B 관문 — 자과 필기(손글씨) 기기끼리 동기화(물리 문항 · 지학/생물 카드 · 교재 쪽 · 서브노트)

  python _harness_jagwa_ink_sync.py [--new <앱>] [--base <앱 파일 | genie git 판>] [--spd <studyplandata>] [--vendor <cdnjs 사본>]
                                     [--only I1,I3,…] [--yard all|base,mem,ord|none] [--webkit 1|0] [--res <결과>] [--work <임시>]

  NEW  = 이 판 앱(기본 GENIE_ROOT jagwa/index.html — 사슬 실행기가 GENIE_ROOT 를 준다 · 없으면 _roots.genie())
  BASE = 바탕(기본 genie git 331faa9 — 동기화 없는 판 · 헛잣대 ㉠ · §B-9 옛 판 기기)
  데이터 = studyplandata(--spd · 없으면 SPD_ROOT · _roots.spd()) — 기록.json(처음 원격) · 문항 · 목차 · 교재 조각 · 시험지(111 만 · 기기마다)
  기기 하나 = 브라우저 문맥 하나(IndexedDB · localStorage 따로) — A = 폰 390(터치 · 모바일) · B = PC 1100 · 그 밖 C(옛 판) · D(시계 +1 시간) · E(첫 동기화 150) · W(webkit 폰)
  가짜 GitHub(route · 메모리 · 진짜 git 꼴 — 문맥 여럿이 같은 저장소를 본다 · 밖으로 안 나감):
     blob sha = sha1("blob <바이트 수>\0"+글) · 나무(재귀 아님) · 커밋 · ref(main 하나)
     GET git/ref/heads/main · git/commits/<sha> · git/trees/<sha> · git/blobs/<sha>(base64 · 60 자 줄바꿈)
     POST git/trees(base_tree 위 중첩 경로 → 하위 나무 새로) · POST git/commits · PATCH git/refs/heads/main(앞서 감기 아니면 422)
     contents(기록 동기화 · 같은 ref): GET raw/json · PUT = 파일 sha 다르면 409 · 맞으면 새 커밋으로 ref 를 옮김 · 나무에 없는 자리 = studyplandata 사본(읽기만)
     흉내: 다음 n 번 <상태>(403 · 422 …) · 분당 쓰기 80 넘으면 403(보조 한도) · 붙잡기(한 기기 PATCH 를 잡아 두고 다른 기기 기록 PUT 뒤에 풀기) · 길마다 요청 수 셈
  그 밖 바깥 = 막음 — cdnjs 는 --vendor 사본(없으면 하네스가 시작할 때 한 번 받아 둠 · 그것도 안 되면 막음) · blob:/data: 그대로
  앱 고침 0 — 필기를 심는 길 = 앱 길 그대로(물리 = 문항 열고 INK[LAYER].push + saveInk 또는 화면 펜(CDP pen · 지우개) · ↶ · 층 고르개 · 지금 회독 지우기
     · 카드 = QINK(화면 펜 지우개 · erPop) · 교재 = zInkCommit(BK,…) · 들이기 = importData(내보내기 받은 파일)
     옛 필기(이미 쓴 것 · §B-1 · 2 · 11 · 12) = putRaw 로 IndexedDB 에 넣고 kv inkinit 없는 첫 시동 — 넣는 동안 그 기기 git 길은 503(시동 고리가 먼저 받아 덮지 않게)
     하네스가 끄는 것 하나: 3 분 고리(setInterval 180000) — 고리는 직접 부른다(syncInk · syncRecords → inkKick) · alert/confirm/prompt 막음(선례 INIT 꼴)
     잼 장치: paintInk 횟수 엿보기(I10) · inkCycle · uidMigrateImport 부른 때 적기(I13) — 원래 함수를 그대로 부른다
  헛잣대: ㉠ 바탕 331faa9(동기화 없음 → I1 · I2 · I3 FAIL) ㉡ 새 판 inkApplyLocal 「if(mem){」→「if(false){」(메모리 사본 갱신 끔 → I14b · I10 FAIL)
          ㉢ inkToLocal 「.sort((a,b)=>(G[a].o-G[b].o)||…)」→「.sort()」(o 차례 무시 → I14e FAIL) — 바꾼 판은 하네스 서버가 내준다(앱 파일 무접촉)
          헛잣대 칸(id 꼬리 -헛)은 그 판에서 잣대가 FAIL 하면 PASS 로 센다(= 잣대가 가름)
  결과 줄 = PASS|FAIL|INFO | <id> · <글> | <값 JSON>(사슬 받개 RX_PIPE 꼴) · 끝 = INFO | 합계 …
  ⚠ 자과앱 픽셀 게이트 없음(CLAUDE.md) — IndexedDB 값 · 메모리 사본 · DOM 개수 · 원격 파일(가짜 저장소 · 글 풀어 셈)로 잰다
  틀 = moolri/_harness_jagwa_physphone.py 의 serve · route · INIT 꼴(옮겨 씀 · 부르지 않음) · 기기 둘 = gigu/_harness_jagwa_uid_unify.py · _harness_jagwa_revfix0929.py 꼴
  결함 후보 재기 X0~X2(--probe 0 이면 안 함) = §B 밖 · INFO 줄(「재현됨」 = 그 결함이 있다) · 합계 PASS/FAIL 에 안 셈
  자리: N: 밖에서 돌릴 때는 PYTHONPATH 에 N:\개인\claude(_roots) · 데이터 = --spd(예 Documents\spd_wt\c42085f)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import base64, collections, hashlib, http.server, json, math, mimetypes, os, re, subprocess, sys, tempfile, threading, time, traceback, urllib.parse, urllib.request   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
T0 = time.time()


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = os.environ.get('GENIE_ROOT') or _roots.genie()
NEWF = ARG('--new', os.path.join(GENIE, 'jagwa', 'index.html'))
BASE = ARG('--base', '331faa9')
SPD = ARG('--spd', os.environ.get('SPD_ROOT') or _roots.spd())
NOTES = ARG('--notes', os.path.join(os.path.dirname(_roots.spd()), 'notes'))   # 선례(physphone) 꼴 — SPD_ROOT 옆 notes
WORK = ARG('--work', os.path.join(tempfile.gettempdir(), 'h_ink'))
VENDOR = ARG('--vendor', os.path.join(WORK, 'vendor'))
ONLY = [x.strip() for x in (ARG('--only', '') or '').split(',') if x.strip()]
YARD = [x.strip() for x in (ARG('--yard', 'all') or '').split(',') if x.strip()]
if 'all' in YARD:
    YARD = ['base', 'mem', 'ord']
if 'none' in YARD:
    YARD = []
WEBKIT = (ARG('--webkit', '1') or '1') != '0'
OUTF = ARG('--res', os.path.join(WORK, '_harness_jagwa_ink_sync_result.txt'))
os.makedirs(WORK, exist_ok=True)
_TMP = os.path.join(WORK, 'tmp')   # Playwright 프로필 · 내려받기 = 여기(로컬 디스크 · 지시서 「%TEMP%\h_ink\ 아래」)
os.makedirs(_TMP, exist_ok=True)
os.environ['TEMP'] = os.environ['TMP'] = _TMP

PHONE = (390, 844)
PC = (1100, 800)
GRID = 10000
YNAME = {'base': '㉠ 바탕 %s' % BASE, 'mem': '㉡ 메모리 사본 갱신 끔', 'ord': '㉢ o 차례 무시'}

# 시험 자리(물리 = 문항 번호 · 지학/생물 = uid) — 지난 회독 없는 문항(기록 status 1~72 · 97 밖) · 지난 회독이 있어야 하는 칸만 5(1 개) · 21 · 22(2 개)
P = dict(I1a=75, I1b=202, I1c=203, I2=210, I4=215, I5=21, I6=220, I7=225, I8a=230, I8b=231, I10=5, I12=240,
         I14a=80, I14c=252, I14d=22, I14e=255, X0=260, X1=262, X2=264)
PROBE = (ARG('--probe', '1') or '1') != '0'   # X0~X2 = 결함 후보 재기(§B 밖 · INFO 줄 · 합계에 안 셈)
I11_KEYS = [str(n) for n in range(381, 531)]   # 150 열쇠
EU = dict(I1='G95-32-01', W='G95-32-07')
BU = dict(I1='B00-37-01')
PDF_NEED = {'111'}   # 화면 펜으로 긋는 물리 문항(75 · 80)이 사는 시험지 하나만 받는다(6.3MB)


def _hist_counts(subj):
    """<과목>/기록.json data.status[열쇠].h 수 = 앱 hist(no) 길이(문항을 열면 그만큼 지난 회독 층 · 가림) — 못 읽으면 None"""
    try:
        d = json.load(open(os.path.join(SPD, subj, '기록.json'), encoding='utf-8'))
        st = (d.get('data') or {}).get('status') or {}
        return {str(k): len((v or {}).get('h') or []) for k, v in st.items() if isinstance(v, dict)}
    except Exception:
        return None


# 자료 전제(시험 자리의 지난 회독 수) — c42085f 에서 고른 자리. 기록이 바뀌어 어긋나면 화면 펜이 아닌 물리 칸은 같은 수의 다른 문항으로 갈아 끼우고 INFO 에 적는다
HC = {s: _hist_counts(s) for s in ('phys', 'earth', 'bio')}
P_NEED = dict(I5=2, I10=1, I14d=2)            # 그 밖 물리 자리 = 0(지난 회독 없음)
P_FIXED = ('I1a', 'I14a', 'I1b', 'I1c', 'I2')  # I1a · I14a = 화면 펜(시험지 111 에 사는 문항) · I1b · I1c · I2 = 옛 필기 씨앗(SEEDS) — 못 갈아 끼움(어긋나면 적기만)
P_REMAP, P_BAD = {}, {}
if HC['phys'] is not None:
    _used = set(P.values()) | set(range(381, 531)) | {271}   # 271 = I13 옛 꼴(순배열) 열쇠
    for _k in list(P):
        _w = P_NEED.get(_k, 0)
        if HC['phys'].get(str(P[_k]), 0) == _w:
            continue
        _c = [] if _k in P_FIXED else [n for n in range(23, 381) if n not in _used and HC['phys'].get(str(n), 0) == _w]
        if _c:
            P_REMAP[_k] = [P[_k], _c[0]]
            P[_k] = _c[0]
            _used.add(_c[0])
        else:
            P_BAD[_k] = [P[_k], '지난 회독 %d · 바람 %d' % (HC['phys'].get(str(P[_k]), 0), _w)]
for _s, _d in (('earth', EU), ('bio', BU)):   # 카드 자리 — 지난 회독 0 이어야(열면 QR = 지난 수 + 1 · 가림) · 어긋나면 적기만
    for _k, _u in _d.items():
        if HC[_s] is not None and HC[_s].get(_u, 0):
            P_BAD['%s.%s' % (_s, _k)] = [_u, '지난 회독 %d · 바람 0' % HC[_s][_u]]


# ════════════════════ 결과 ════════════════════
RES = []
_OF = open(OUTF, 'w', encoding='utf-8')


def out(s):
    print(s, flush=True)
    try:
        _OF.write(s + '\n'); _OF.flush()
    except Exception:
        pass


def J(v, n=1600):
    return json.dumps(v, ensure_ascii=False, default=str)[:n]


def R(tid, title, ok, val):
    RES.append({'id': tid, 'st': 'PASS' if ok else 'FAIL', 'title': title})
    out('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', tid, title, J(val)))
    return ok


def INFO(tid, title, val):
    out('INFO | %s · %s | %s' % (tid, title, J(val, 2400)))


def Y(tid, yard, title, check_ok, val):
    """헛잣대 — 그 판에서 잣대가 FAIL 이면 PASS(잣대가 가름)"""
    ok = not check_ok
    RES.append({'id': tid + '-헛', 'st': 'PASS' if ok else 'FAIL', 'yard': yard, 'title': title})
    out('%s | %s-헛 · %s 에서 %s · %s | %s' % ('PASS' if ok else 'FAIL', tid, YNAME[yard],
        '잣대 FAIL(가름)' if ok else '잣대 PASS(못 가름)', title, J(val)))
    return ok


def want(tid):
    return not ONLY or tid in ONLY


# ════════════════════ 획 · 비교 ════════════════════
def ln(u0, v0, u1, v1, n=7, c='#16181B', w=2, hl=0, r=None):
    """곧은 획(쪽 소수 · 점 n) — 지우개가 한 획만 잡게 자리를 띄워 쓴다"""
    p = []
    for i in range(n):
        t = i / (n - 1)
        p += [round(u0 + (u1 - u0) * t, 5), round(v0 + (v1 - v0) * t, 5)]
    d = {'c': c, 'w': w, 'hl': hl, 'p': p}
    if r is not None:
        d['r'] = r
    return d


def dot(u, v, c='#16181B', w=2):
    return {'c': c, 'w': w, 'hl': 0, 'p': [u, v]}


def load_material():
    """실기록 손필기 — studyplandata phys/기록.json mcard(1/1000 정수) → 쪽 소수(÷1000) · 없으면 빈 목록(시험은 곧은 획으로 · 값에 적음)"""
    f = os.path.join(SPD, 'phys', '기록.json')
    try:
        rec = json.load(open(f, encoding='utf-8'))
        mc = rec['data']['mcard']
        outl = []
        for k in sorted(mc, key=lambda x: int(x) if str(x).isdigit() else 0):
            for s in (mc[k] or {}).get('s', []):
                p = [v / 1000 for v in s.get('p', [])]
                if len(p) >= 2:
                    outl.append({'c': s.get('c', '#16181B'), 'w': s.get('w', 2), 'hl': 1 if s.get('hl') else 0, 'p': p})
        return outl, 'studyplandata phys/기록.json mcard(%s) %d 획 · 점 %d · 1/1000 정수 → 쪽 소수' % (
            ','.join(sorted(mc)), len(outl), sum(len(x['p']) // 2 for x in outl))
    except Exception as e:
        return [], '재료 없음(%s) — 곧은 획으로 대신' % str(e)[:80]


MAT, MAT_SRC = load_material()


def mat(i, j):
    if len(MAT) >= j:
        return [dict(x) for x in MAT[i:j]]
    return [ln(0.10 + 0.02 * k, 0.40, 0.30 + 0.02 * k, 0.48, n=40, c='#243a5e') for k in range(i, j)]


def js_round(v):
    return math.floor(v + 0.5)


def grid_dedupe(p):
    """앱 inkEnc 와 같은 「같은 점 거름」 — 10000 칸 반올림 뒤 바로 앞 점과 같으면 뺀다"""
    o = []
    lx = ly = None
    for i in range(0, len(p) - 1, 2):
        x, y = js_round(p[i] * GRID), js_round(p[i + 1] * GRID)
        if x == lx and y == ly:
            continue
        o += [p[i], p[i + 1]]
        lx, ly = x, y
    return o


def sig(st):
    p = grid_dedupe(st.get('p') or [])
    return (st.get('c'), float(st.get('w') or 0), 1 if st.get('hl') else 0, st.get('r'), tuple(js_round(v * GRID) for v in p))


def sig_s(s):   # 값에 적는 짧은 꼴
    return '%s/%s%s@%s' % (s[0], s[1], ('/r%s' % s[3]) if s[3] is not None else '', ','.join(str(x) for x in s[4][:2]))


def groups(val):
    if not isinstance(val, dict):
        return {}
    if isinstance(val.get('s'), list):
        return {'s': val['s']}
    return {str(k): v for k, v in val.items() if isinstance(v, list)}


def mset(val):
    c = collections.Counter()
    for g, L in groups(val).items():
        for s in L:
            if isinstance(s, dict) and isinstance(s.get('p'), list):
                c[(g, sig(s))] += 1
    return c


def mset_show(c):
    return sorted('%s:%s×%d' % (g, sig_s(s), n) for (g, s), n in c.items())


def cmp_list(orig, got, tol=1e-4 + 1e-12):
    """원본 획 목록 ↔ 받은 획 목록 — 개수 · 차례 · 칸(c · w · hl · r) · 좌표(같은 점 거름 뒤 ≤ 1/10000)"""
    if len(orig) != len(got):
        return False, {'개수': [len(orig), len(got)]}
    worst, drop = 0.0, 0
    for i, (a, b) in enumerate(zip(orig, got)):
        if a.get('c') != b.get('c') or a.get('r') != b.get('r') or float(a.get('w') or 0) != float(b.get('w') or 0) or bool(a.get('hl')) != bool(b.get('hl')):
            return False, {'i': i, '칸': [[a.get('c'), a.get('w'), a.get('hl'), a.get('r')], [b.get('c'), b.get('w'), b.get('hl'), b.get('r')]]}
        pa = grid_dedupe(a.get('p') or [])
        drop += (len(a.get('p') or []) - len(pa)) // 2
        pb = b.get('p') or []
        if len(pa) != len(pb):
            return False, {'i': i, '점 수': [len(pa) // 2, len(pb) // 2]}
        for x, y in zip(pa, pb):
            worst = max(worst, abs(x - y))
    return worst <= tol, {'획': len(orig), '최대 차': worst, '거른 점': drop}


def cmp_val(orig, got):
    go, gg = groups(orig), groups(got)
    res, ok = {}, True
    for g in sorted(set(go) | set(gg)):
        a, b = go.get(g, []), gg.get(g, [])
        if not a and not b:
            continue
        o, d = cmp_list(a, b)
        res[g] = d
        ok = ok and o
    return ok, res


# ════════════════════ 가짜 GitHub ════════════════════
def sha1(b):
    return hashlib.sha1(b).hexdigest()


def blob_sha(b):
    return sha1(b'blob %d\0' % len(b) + b)


VEND_FAIL = set()
VEND_GOT = []
VEND_FILES = ('pdf.js/3.11.174/pdf.min.js', 'pdf.js/3.11.174/pdf.worker.min.js', 'pdf-lib/1.17.1/pdf-lib.min.js',
              'KaTeX/0.16.9/katex.min.js', 'KaTeX/0.16.9/katex.min.css', 'KaTeX/0.16.9/contrib/auto-render.min.js')


def vendor_file(rel):
    f = os.path.join(VENDOR, *rel.split('/'))
    if os.path.isfile(f):
        return f
    if rel in VEND_FAIL or re.search(r'\.(woff2?|ttf|eot|map)$', rel):
        return None
    try:   # 브라우저 밖(파이썬)에서 한 번 받아 둔다 — 브라우저 길은 늘 사본만(CLAUDE.md 「cdnjs 에서 같은 판을 받아 채우고」)
        b = urllib.request.urlopen('https://cdnjs.cloudflare.com/ajax/libs/' + rel, timeout=30).read()
        os.makedirs(os.path.dirname(f), exist_ok=True)
        open(f, 'wb').write(b)
        VEND_GOT.append([rel, len(b)])
        return f
    except Exception as e:
        VEND_FAIL.add(rel)
        VEND_GOT.append([rel, '못 받음 ' + str(e)[:60]])
        return None


class World:
    """가짜 저장소 하나(zzikkaplan/studyplandata · 가지 main) — 기기(문맥) 여럿이 같은 것을 본다"""
    REPO = 'zzikkaplan/studyplandata'
    WRITES = ('commit-post', 'tree-post', 'blob-post', 'ref-patch', 'contents-put')

    def __init__(self, name):
        self.name = name
        self.blobs, self.trees, self.commits = {}, {}, {}
        self.seq = 0
        self.ref = self.write_commit(self.write_tree([]), [], 'init(하네스)', 'h')
        self.cnt = collections.Counter()
        self.log = []
        self.rules = []
        self.limit = None
        self.wtimes = collections.deque()
        self.wmax = 0
        self.hold = None
        self.held = []
        self.puts = []
        self.ink_log = []
        self.other = {}

    # ── git 물건 ──
    def put_blob(self, b):
        s = blob_sha(b)
        self.blobs[s] = b
        return s

    def write_tree(self, ents):
        ents = sorted([dict(e) for e in ents], key=lambda e: e['name'] + ('/' if e['type'] == 'tree' else ''))
        raw = b''.join(('%s %s' % ('40000' if e['type'] == 'tree' else e['mode'], e['name'])).encode('utf-8') + b'\0' + bytes.fromhex(e['sha']) for e in ents)
        s = sha1(b'tree %d\0' % len(raw) + raw)
        self.trees[s] = ents
        return s

    def write_commit(self, tree, parents, msg, who):
        self.seq += 1
        raw = ('tree %s\n' % tree + ''.join('parent %s\n' % p for p in parents) +
               'author %s <h@h> %d +0900\ncommitter %s <h@h> %d +0900\n\n%s\n' % (who, 1700000000 + self.seq, who, 1700000000 + self.seq, msg)).encode('utf-8')
        s = sha1(b'commit %d\0' % len(raw) + raw)
        self.commits[s] = {'tree': tree, 'parents': list(parents), 'message': msg, 'who': who, 'seq': self.seq}
        return s

    def update_tree(self, base, ch):
        """base 나무 위에 ch({경로: blob sha | None}) — 중첩 경로는 하위 나무를 새로 짓는다"""
        ents = {e['name']: dict(e) for e in (self.trees.get(base) or [])} if base else {}
        sub = {}
        for path, s in ch.items():
            path = path.strip('/')
            if '/' in path:
                h, rest = path.split('/', 1)
                sub.setdefault(h, {})[rest] = s
            elif s is None:
                ents.pop(path, None)
            else:
                ents[path] = {'name': path, 'mode': '100644', 'type': 'blob', 'sha': s}
        for h, c in sub.items():
            cur = ents.get(h)
            ns = self.update_tree(cur['sha'] if cur and cur['type'] == 'tree' else None, c)
            if self.trees[ns]:
                ents[h] = {'name': h, 'mode': '040000', 'type': 'tree', 'sha': ns}
            else:
                ents.pop(h, None)
        return self.write_tree(list(ents.values()))

    def lookup(self, tree, path):
        parts = [x for x in path.split('/') if x]
        cur = tree
        for i, nm in enumerate(parts):
            e = next((x for x in (self.trees.get(cur) or []) if x['name'] == nm), None)
            if not e:
                return None
            if i == len(parts) - 1:
                return e
            if e['type'] != 'tree':
                return None
            cur = e['sha']
        return None

    def root(self):
        return self.commits[self.ref]['tree']

    def read_path(self, path):
        e = self.lookup(self.root(), path)
        return self.blobs.get(e['sha']) if e and e['type'] == 'blob' else None

    def is_ancestor(self, a, b):
        seen, st = set(), [b]
        while st:
            c = st.pop()
            if c == a:
                return True
            if c in seen or c not in self.commits:
                continue
            seen.add(c)
            st.extend(self.commits[c]['parents'])
        return False

    @staticmethod
    def local(repo, path):
        rt = NOTES if repo.endswith('/notes') else SPD
        f = os.path.join(rt, *[p for p in path.split('/') if p])
        return open(f, 'rb').read() if os.path.isfile(f) else None

    # ── 보기 ──
    def ink_files(self, subj):
        e = self.lookup(self.root(), subj + '/ink')
        if not e or e['type'] != 'tree':
            return {}
        return {x['name']: x['sha'] for x in self.trees[e['sha']] if x['type'] == 'blob'}

    def ink_raw(self, subj, key):
        return self.read_path('%s/ink/%s.json' % (subj, str(key).replace(':', '~')))

    def ink_doc(self, subj, key):
        b = self.ink_raw(subj, key)
        return json.loads(b.decode('utf-8')) if b else None

    def n(self, dev=None, kind=None, st=None):
        return sum(v for (d, k, s), v in self.cnt.items() if (dev is None or d == dev) and (kind is None or k == kind) and (st is None or s == st))

    def snap(self):
        return dict(self.cnt)

    def delta(self, s0):
        d = collections.Counter()
        for (dv, k, s), v in self.cnt.items():
            x = v - s0.get((dv, k, s), 0)
            if x:
                d['%s %s %s' % (dv, k, s)] = x
        return dict(sorted(d.items()))

    def inject(self, dev, kind, status, n=1):
        self.rules.append({'dev': dev, 'kind': kind, 'status': status, 'n': n, 'hit': 0})

    def release(self):
        H, self.held = self.held, []
        for (route, dev, m, k, rest, body, hdr) in H:
            self._serve(route, dev, m, k, rest, body, hdr)
        return len(H)

    # ── route ──
    def handler(self, dev):
        def h(route):
            try:
                return self._h(route, dev)
            except Exception as e:
                self.log.append([round(time.time() - T0, 2), dev.name, 'ERR', str(e)[:200]])
                try:
                    return route.fulfill(status=500, body='{"message":"harness error"}', content_type='application/json')
                except Exception:
                    return None
        return h

    @staticmethod
    def kind(m, rest):
        if rest.startswith('git/ref/'):
            return 'ref'
        if rest.startswith('git/refs/'):
            return 'ref-patch' if m == 'PATCH' else 'refs'
        for nm in ('commits', 'trees', 'blobs'):
            if rest.startswith('git/' + nm):
                return nm[:-1] + ('-post' if m == 'POST' else '-get')
        if rest.startswith('contents/'):
            return 'contents-put' if m == 'PUT' else 'contents-get'
        return 'repo' if rest == '' else 'other'

    def _h(self, route, dev):
        req = route.request
        u = req.url
        if u.startswith(('http://127.0.0.1', 'blob:', 'data:')):
            return route.continue_()
        if u.startswith('https://cdnjs.cloudflare.com/ajax/libs/'):
            rel = urllib.parse.unquote(u.split('/ajax/libs/', 1)[1].split('?')[0])
            f = vendor_file(rel)
            if f:
                ct = 'text/css' if f.endswith('.css') else 'application/javascript'
                return route.fulfill(status=200, body=open(f, 'rb').read(), content_type=ct)
            self.cnt[(dev.name, 'cdn-abort', 0)] += 1
            return route.abort()
        if not u.startswith('https://api.github.com/repos/'):
            self.cnt[(dev.name, 'abort', 0)] += 1
            return route.abort()
        pq = u[len('https://api.github.com/repos/'):].split('?', 1)
        segs = pq[0].split('/', 2)
        repo = '/'.join(segs[:2])
        rest = urllib.parse.unquote(segs[2]) if len(segs) > 2 else ''
        m = req.method
        k = self.kind(m, rest)
        if repo != self.REPO:
            return self._other(route, dev, repo, rest, m, k, req)
        if dev.block_git and rest.startswith('git/'):
            return self._res(route, dev, m, k, rest, 503, {'message': 'blocked(하네스 — 옛 필기 심는 중)'})
        for r in self.rules:
            if r['n'] > 0 and r['dev'] in (None, dev.name) and r['kind'] in (None, k):
                r['n'] -= 1
                r['hit'] += 1
                return self._res(route, dev, m, k, rest, r['status'], {'message': 'harness inject %d' % r['status']})
        if k in self.WRITES:
            now = time.time()
            self.wtimes.append(now)
            while self.wtimes and self.wtimes[0] < now - 60:
                self.wtimes.popleft()
            self.wmax = max(self.wmax, len(self.wtimes))
            if self.limit and len(self.wtimes) > self.limit:
                return self._res(route, dev, m, k, rest, 403, {'message': 'You have exceeded a secondary rate limit(harness)'})
        if self.hold and self.hold['dev'] == dev.name and self.hold['kind'] == k:
            self.hold = None
            self.held.append((route, dev, m, k, rest, req.post_data, dict(req.headers or {})))
            self.cnt[(dev.name, k, 'held')] += 1
            return None
        return self._serve(route, dev, m, k, rest, req.post_data, dict(req.headers or {}))

    def _res(self, route, dev, m, k, rest, st, obj):
        self.cnt[(dev.name, k, st)] += 1
        self.log.append([round(time.time() - T0, 2), dev.name, m, k, rest[:70], st])
        return route.fulfill(status=st, body=json.dumps(obj, ensure_ascii=False), content_type='application/json; charset=utf-8')

    def _other(self, route, dev, repo, rest, m, k, req):
        """notes 등 다른 저장소 — 로컬 사본 읽기만 · PUT = 메모리(밖으로 안 나감)"""
        if k == 'contents-get':
            pth = rest[len('contents/'):]
            b = self.other.get((repo, pth))
            if b is None:
                b = self.local(repo, pth)
            if b is None:
                return self._res(route, dev, m, k, rest, 404, {'message': 'Not Found'})
            if 'raw' in (req.headers or {}).get('accept', ''):
                self.cnt[(dev.name, k, 200)] += 1
                return route.fulfill(status=200, body=b, content_type='application/octet-stream')
            return self._res(route, dev, m, k, rest, 200, {'path': pth, 'sha': blob_sha(b), 'size': len(b), 'type': 'file'})
        if k == 'contents-put':
            try:
                B = json.loads(req.post_data or '{}')
                self.other[(repo, rest[len('contents/'):])] = base64.b64decode(B.get('content', ''))
            except Exception:
                return self._res(route, dev, m, k, rest, 422, {'message': 'bad'})
            return self._res(route, dev, m, k, rest, 200, {'content': {'sha': 'x'}})
        return self._res(route, dev, m, k, rest, 404, {'message': 'Not Found'})

    def _serve(self, route, dev, m, k, rest, body, hdr):
        try:
            B = json.loads(body) if body else {}
        except Exception:
            B = None
        nf = {'message': 'Not Found'}
        last = rest.rsplit('/', 1)[-1]
        if k == 'ref':
            return self._res(route, dev, m, k, rest, 200, {'ref': 'refs/heads/main', 'object': {'sha': self.ref, 'type': 'commit'}})
        if k == 'commit-get':
            c = self.commits.get(last)
            if not c:
                return self._res(route, dev, m, k, rest, 404, nf)
            return self._res(route, dev, m, k, rest, 200, {'sha': last, 'tree': {'sha': c['tree']}, 'parents': [{'sha': p} for p in c['parents']], 'message': c['message']})
        if k == 'tree-get':
            t = self.trees.get(last)
            if t is None:
                return self._res(route, dev, m, k, rest, 404, nf)
            return self._res(route, dev, m, k, rest, 200, {'sha': last, 'truncated': False, 'tree': [
                dict({'path': e['name'], 'mode': e['mode'], 'type': e['type'], 'sha': e['sha']}, **({'size': len(self.blobs.get(e['sha'], b''))} if e['type'] == 'blob' else {})) for e in t]})
        if k == 'blob-get':
            b = self.blobs.get(last)
            if b is None:
                return self._res(route, dev, m, k, rest, 404, nf)
            c64 = base64.b64encode(b).decode('ascii')
            c64 = '\n'.join(c64[i:i + 60] for i in range(0, len(c64), 60)) + '\n'
            return self._res(route, dev, m, k, rest, 200, {'sha': last, 'size': len(b), 'content': c64, 'encoding': 'base64'})
        if k == 'tree-post':
            if not isinstance(B, dict) or not isinstance(B.get('tree'), list):
                return self._res(route, dev, m, k, rest, 422, {'message': 'tree 없음'})
            base = B.get('base_tree')
            if base and base not in self.trees:
                return self._res(route, dev, m, k, rest, 422, {'message': 'base_tree 없음'})
            ch = {}
            for e in B['tree']:
                p_ = str(e.get('path') or '')
                if e.get('content') is not None:
                    ch[p_] = self.put_blob(str(e['content']).encode('utf-8'))
                elif e.get('sha') is None:
                    ch[p_] = None
                elif e['sha'] in self.blobs:
                    ch[p_] = e['sha']
                else:
                    return self._res(route, dev, m, k, rest, 422, {'message': 'sha 없음'})
            ns = self.update_tree(base, ch)
            return self._res(route, dev, m, k, rest, 201, {'sha': ns, 'tree': [{'path': e['name'], 'mode': e['mode'], 'type': e['type'], 'sha': e['sha']} for e in self.trees[ns]]})
        if k == 'commit-post':
            t, ps = (B or {}).get('tree'), (B or {}).get('parents') or []
            if t not in self.trees or any(p not in self.commits for p in ps):
                return self._res(route, dev, m, k, rest, 422, {'message': 'tree/parents 없음'})
            s = self.write_commit(t, ps, str(B.get('message', '')), dev.name)
            return self._res(route, dev, m, k, rest, 201, {'sha': s, 'tree': {'sha': t}, 'parents': [{'sha': p} for p in ps], 'message': B.get('message')})
        if k == 'ref-patch':
            s = (B or {}).get('sha')
            if s not in self.commits:
                return self._res(route, dev, m, k, rest, 422, {'message': 'commit 없음'})
            if not B.get('force') and not self.is_ancestor(self.ref, s):
                return self._res(route, dev, m, k, rest, 422, {'message': 'Update is not a fast forward'})
            self.ref = s
            mm = re.search(r'필기 (\d+)\s*$', self.commits[s]['message'])
            self.ink_log.append({'dev': dev.name, 'n': int(mm.group(1)) if mm else None, 'seq': self.commits[s]['seq'], 'msg': self.commits[s]['message']})
            return self._res(route, dev, m, k, rest, 200, {'ref': 'refs/heads/main', 'object': {'sha': s, 'type': 'commit'}})
        if k == 'contents-get':
            pth = rest[len('contents/'):]
            mm = re.match(r'^phys/pdf/(.+)\.pdf$', pth)
            if mm and dev.pdfs is not None and mm.group(1) not in dev.pdfs:
                return self._res(route, dev, m, k, rest, 404, {'message': 'Not Found(하네스 — 이 기기는 이 시험지를 안 받음)'})
            b = self.read_path(pth)
            if b is None:
                b = self.local(self.REPO, pth)
            if b is None:
                return self._res(route, dev, m, k, rest, 404, nf)
            if 'raw' in (hdr or {}).get('accept', ''):
                self.cnt[(dev.name, k, 200)] += 1
                return route.fulfill(status=200, body=b, content_type='application/octet-stream')
            return self._res(route, dev, m, k, rest, 200, {'name': pth.rsplit('/', 1)[-1], 'path': pth, 'sha': blob_sha(b), 'size': len(b), 'type': 'file'})
        if k == 'contents-put':
            pth = rest[len('contents/'):]
            try:
                data = base64.b64decode((B or {}).get('content', ''))
            except Exception:
                return self._res(route, dev, m, k, rest, 422, {'message': 'content'})
            cur = self.read_path(pth)
            if cur is None:
                cur = self.local(self.REPO, pth)
            if cur is not None:
                if not B.get('sha'):
                    return self._res(route, dev, m, k, rest, 422, {'message': '"sha" wasn\'t supplied'})
                if B['sha'] != blob_sha(cur):
                    return self._res(route, dev, m, k, rest, 409, {'message': '%s does not match' % pth})
            bs = self.put_blob(data)
            c = self.write_commit(self.update_tree(self.root(), {pth: bs}), [self.ref], str(B.get('message', '')), dev.name)
            self.ref = c
            self.puts.append({'dev': dev.name, 'path': pth, 'text': data.decode('utf-8', 'replace'), 'seq': self.commits[c]['seq']})
            return self._res(route, dev, m, k, rest, 200, {'content': {'sha': bs, 'path': pth}, 'commit': {'sha': c}})
        if k == 'repo':
            return self._res(route, dev, m, k, rest, 200, {'full_name': self.REPO, 'private': True})
        return self._res(route, dev, m, k, rest, 404, nf)


# ════════════════════ 앱 내주기 ════════════════════
class AppServer:
    """판마다 서버 하나(127.0.0.1 빈 포트) — 앱 글(메모리 · 길마다) · 그 밖 = GENIE jagwa/ 아래 파일"""

    def __init__(self, pages):
        self.pages = {k: (v.encode('utf-8') if isinstance(v, str) else v) for k, v in pages.items()}
        me = self
        base = os.path.join(GENIE, 'jagwa')

        class Hd(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                p = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
                if p in me.pages:
                    b, ct = me.pages[p], 'text/html; charset=utf-8'
                else:
                    f = os.path.normpath(os.path.join(base, *[x for x in p.split('/') if x and x != '..']))
                    if not f.startswith(os.path.normpath(base)) or not os.path.isfile(f):
                        self.send_response(404)
                        self.end_headers()
                        return
                    b, ct = open(f, 'rb').read(), (mimetypes.guess_type(f)[0] or 'application/octet-stream')
                self.send_response(200)
                self.send_header('Content-Type', ct)
                self.send_header('Content-Length', str(len(b)))
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                self.wfile.write(b)

        self.srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Hd)
        self.srv.daemon_threads = True
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.port = self.srv.server_address[1]

    def close(self):
        try:
            self.srv.shutdown()
        except Exception:
            pass


INIT = r"""
(()=>{
  if(!sessionStorage.getItem('__hk')){sessionStorage.setItem('__hk','1');
    try{localStorage.setItem('tt.cfg',JSON.stringify({token:'harness-token',person:'__WHO__'}))}catch(e){}}
  window.__err=[];
  window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+(e.lineno||''))});
  window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
  window.alert=function(){};window.confirm=function(){return true};window.prompt=function(){return null};
  /* 3 분 고리만 끈다 — 고리는 하네스가 직접 부른다(syncInk · syncRecords → inkKick) */
  {const _si=window.setInterval;window.__si0=0;window.setInterval=function(f,ms){if(+ms===180000){window.__si0++;return 0}return _si.apply(window,arguments)}}
  const OFF=__OFF__;
  if(OFF){const _D=Date;class D extends _D{constructor(...a){if(a.length===0)super(_D.now()+OFF);else super(...a)}static now(){return _D.now()+OFF}};window.Date=D}
  window.addEventListener('pointerup',()=>{window.__lastUp=performance.now()},true);
})();
"""

READY = r"""()=>{try{if(typeof DATA==='undefined'||!DATA.length||typeof draw!=='function')return false;
  if(typeof CARD_LAYER!=='undefined'&&CARD_LAYER&&(typeof DATA_V==='undefined'||!DATA_V))return false;return true}catch(e){return false}}"""

KJS = r"""
window.__K={
 sleep:ms=>new Promise(r=>setTimeout(r,ms)),
 busy(){return (typeof recBusy!=='undefined'&&recBusy)||(typeof INKBUSY!=='undefined'&&INKBUSY)},
 async idle(ms){const t0=performance.now();ms=ms||90000;while(performance.now()-t0<ms){if(!__K.busy()){await __K.sleep(150);if(!__K.busy())return true}await __K.sleep(50)}return false},
 has(){return typeof syncInk==='function'&&typeof INKST!=='undefined'},
 chip(){const c=document.getElementById('recChip');return c?c.textContent:''},
 chipErr(){const c=document.getElementById('recChip');return !!c&&c.classList.contains('err')},
 st(){if(!__K.has())return {none:1,rec:__K.chip()};
   return {st:Object.assign({},INKST),dirty:INKDIRTY.size,dk:[...INKDIRTY].slice(0,6),add:INKADDONLY.size,err:INKERR,chip:inkChip(),rec:__K.chip(),recErr:__K.chipErr(),loaded:INKLOADED,busy:INKBUSY,bad:[...INKBADK].slice(0,8)}},
 async ink(){if(!__K.has())return __K.rec();await __K.idle();await syncInk();await __K.idle();return __K.st()},
 async rec(){await __K.idle();try{await syncRecords(true)}catch(e){}await __K.idle();return __K.st()},
 async get(k){const v=await get('ink',k);return (v===undefined||v===null)?null:JSON.parse(JSON.stringify(v))},
 async putRaw(k,v){return await (typeof putRaw==='function'?putRaw:put)('ink',k,v)},
 async put(k,v){return await put('ink',k,v)},
 async resetInit(){await del('kv','inkinit');await del('kv','inkdirty');await del('kv','inkaddonly');return 1},
 async keys(){return (await keys('ink')).map(String)},
 curKey(){try{return CARD_LAYER?(QUID?qKey(QUID):null):(VNO?String(inkK(VNO)):null)}catch(e){return null}},
 async open(no){const k=__K.curKey();let was=false;try{if(VNO){was=true;closeView()}}catch(e){}
   if(was&&k&&typeof INKDIRTY!=='undefined'&&INKDIRTY.has(k)){await __K.sleep(1200);await __K.idle()}else await __K.sleep(150);
   window.__openErr='';try{await openView(no)}catch(e){window.__openErr=String(e&&e.message||e)}await __K.sleep(800);return VNO},
 async close(){const k=__K.curKey();try{closeView()}catch(e){}if(k&&typeof INKDIRTY!=='undefined'&&INKDIRTY.has(k)){await __K.sleep(1200);await __K.idle()}return 1},
 phys(){const L=Object.keys(INK);return {VNO,LAYER,LAYERS,HIDEOLD,keys:L,n:Object.fromEntries(L.map(x=>[x,(INK[x]||[]).length])),
   vis:L.filter(x=>!(HIDEOLD&&+x!==LAYER)).reduce((s,x)=>s+(INK[x]||[]).length,0),err:window.__openErr||''}},
 card(){return {QUID,QR,QHIDE,n:((QINK&&QINK.s)||[]).length,rounds:qRounds(),err:window.__openErr||''}}
};
"""

SETTLE = r"""async()=>{const t0=performance.now();const sl=ms=>new Promise(r=>setTimeout(r,ms));
  const nw=typeof INKST!=='undefined';
  const recDone=()=>{try{const m=lsObj(SMETA_KEY);return (m.lastSync||0)>=Date.now()-performance.now()-50||!!recErr||!recToken()}catch(e){return true}};
  await sl(200);
  while(performance.now()-t0<60000){
    const rb=typeof recBusy!=='undefined'&&recBusy, ib=nw&&INKBUSY;
    if(!rb&&!ib&&(nw?INKST.cyc>=1:recDone())){await sl(300);if(!(typeof recBusy!=='undefined'&&recBusy)&&!(nw&&INKBUSY))return {ok:true,ms:Math.round(performance.now()-t0),cyc:nw?INKST.cyc:null}}
    await sl(80)}
  return {ok:false,ms:Math.round(performance.now()-t0),cyc:nw?INKST.cyc:null,rb:typeof recBusy!=='undefined'&&recBusy}}"""

SEED = r"""async V=>{for(const k of Object.keys(V))await __K.putRaw(k,V[k]);await __K.resetInit();return (await keys('ink')).length}"""

OPEN = r"""async no=>{await __K.open(no);return __K.phys()}"""

DRAW = r"""async a=>{if(String(VNO)!==String(a.no))await __K.open(a.no);
  if(a.layer!==null&&a.layer!==undefined){let g=0;while(!(String(a.layer) in INK)&&g++<12){document.getElementById('tLayerAdd').click();await __K.sleep(60)}
    const s=document.getElementById('tLayer');s.value=String(a.layer);s.onchange({target:s})}
  for(const st of a.strokes)(INK[LAYER]=INK[LAYER]||[]).push(JSON.parse(JSON.stringify(st)));
  paintInk();saveInk();await __K.sleep(a.wait||500);return __K.phys()}"""

LAYER_SEL = r"""L=>{const s=document.getElementById('tLayer');s.value=String(L);s.onchange({target:s});return typeof LAYER!=='undefined'&&!CARD_LAYER?LAYER:QR}"""

ERASE_TOOL = r"""()=>{const b=document.getElementById('tErase');if(TOOL.mode!=='erase')b.click();return TOOL.mode}"""

ERASE_SHEET_CUR = r"""async()=>{const b=document.getElementById('tErase');if(TOOL.mode!=='erase')b.click();await __K.sleep(80);
  if(!document.getElementById('erPop'))b.click();await __K.sleep(150);const e=document.querySelector('#erPop #eL');if(!e)return 'erPop 없음';e.click();await __K.sleep(600);return 'ok'}"""

TOOL_VIEW = r"""()=>{try{setTool('view')}catch(e){}return TOOL.mode}"""

CANVAS_PT = r"""([u,v])=>{const c=document.getElementById('inkc');if(!c)return null;
  const at=()=>{const r=c.getBoundingClientRect();const x=r.left+u*r.width,y=r.top+v*r.height;const e=document.elementFromPoint(x,y);return {x,y,u,v,on:!!e&&e===c,top:e?(e.id||e.tagName):null,rw:r.width,rh:r.height}};
  let a=at();if(!a.on){c.scrollIntoView({block:'start'});a=at()}if(!a.on){c.scrollIntoView({block:'center'});a=at()}
  return Object.assign(a,{rot:RENDER.rot,W:RENDER.W,H:RENDER.H})}"""

CARD_PT = r"""([u,v])=>{const sv=document.querySelector('#card #qink');if(!sv)return null;
  const at=()=>{const r=sv.getBoundingClientRect(),k=r.width/QCW;const x=r.left+u*QCW*k,y=r.top+v*QCW*k;const e=document.elementFromPoint(x,y);return {x,y,u,v,on:!!e&&(e===sv||sv.contains(e)),top:e?(e.id||e.tagName):null,k}};
  let a=at();if(!a.on){sv.scrollIntoView({block:'start'});a=at()}if(!a.on){sv.scrollIntoView({block:'center'});a=at()}return a}"""


def pick_pt(dev, js, cands):
    """후보 자리(쪽 소수) 가운데 그 요소가 정말 맨 위인(elementFromPoint) 첫 자리 — 가리개 · 도구줄이 덮은 자리를 피한다"""
    first = None
    for c in cands:
        a = dev.ev(js, list(c))
        if a and first is None:
            first = a
        if a and a.get('on'):
            return a
    return first

OPEN_CARD = r"""async no=>{await __K.open(no);const uid=String(qk(no));
  for(let i=0;i<80;i++){if(QUID===uid&&QINK&&Array.isArray(QINK.s)&&document.querySelector('#card #qink'))break;await __K.sleep(100)}
  await __K.sleep(300);return __K.card()}"""

BK_OPEN = r"""async pr=>{await bkOpen(pr);for(let i=0;i<150;i++){if(BK.ready&&BK.pgs.length)break;await __K.sleep(100)}await __K.sleep(600);
  return {n:BK.pgs.length,keys:BK.pgs.map(p=>p.key).slice(0,12),open:BK.open}}"""

BK_COMMIT = r"""async a=>{const i=BK.pgs.findIndex(p=>p.key===a.key);if(i<0)return {err:'쪽 없음',keys:BK.pgs.map(p=>p.key).slice(0,10)};
  const P=BK.pgs[i],p=[];for(const [u,v] of a.pts)p.push(u*P.w,v*P.h);
  await zInkCommit(BK,{i,c:a.c,w:a.w,hl:0,p});const S=(BK.ink[a.key]&&BK.ink[a.key].s)||[];
  return {n:S.length,last:S.length?JSON.parse(JSON.stringify(S[S.length-1])):null}}"""

BK_STATE = r"""k=>{const p=BK.pgs.find(x=>x.key===k);const sv=p&&BK.svgOf(p);const S=(BK.ink[k]&&BK.ink[k].s)||[];
  return {same:BK.ink[k]===window.__bkRef,n:S.length,paths:sv?sv.querySelectorAll('path[data-j]').length:null,s:JSON.parse(JSON.stringify(S))}}"""

WK_PEN = r"""a=>{const pts=a.pts;let t=document.elementFromPoint(pts[0][0],pts[0][1]);const sv=document.querySelector(a.sel);
  const hit=!!t&&!!sv&&(t===sv||sv.contains(t));if(!hit)t=sv;if(!t)return {err:'없음'};
  const mk=(ty,x,y,b)=>{const init={bubbles:true,cancelable:true,composed:true,pointerId:11,pointerType:'pen',isPrimary:true,clientX:x,clientY:y,button:0,buttons:b,pressure:b?0.5:0};
    let ev;try{ev=new PointerEvent(ty,Object.assign({},init,{coalescedEvents:[new PointerEvent(ty,init)]}))}catch(e){ev=new PointerEvent(ty,init)}return ev};
  t.dispatchEvent(mk('pointerdown',pts[0][0],pts[0][1],1));
  for(const [x,y] of pts.slice(1))t.dispatchEvent(mk('pointermove',x,y,1));
  const l=pts[pts.length-1];t.dispatchEvent(mk('pointerup',l[0],l[1],0));return {hit,tag:t.id||t.tagName}}"""


class Dev:
    """기기 하나 = 브라우저 문맥 하나 — 과목은 ?subj= 로 갈아 연다(과목마다 IndexedDB 가 따로)"""

    def __init__(self, br, world, srv, name, view='pc', skew_ms=0, pdfs=None, eng='chromium'):
        self.world, self.srv, self.name, self.eng, self.view = world, srv, name, eng, view
        self.pdfs = pdfs
        self.block_git = False
        W, Hh = PHONE if view == 'phone' else PC
        kw = dict(viewport={'width': W, 'height': Hh}, device_scale_factor=2 if view == 'phone' else 1, accept_downloads=True)
        if view == 'phone':
            kw['has_touch'] = True
            if eng != 'webkit':
                kw['is_mobile'] = True
        self.ctx = br.new_context(**kw)
        self.ctx.route('**/*', world.handler(self))
        self.ctx.add_init_script(INIT.replace('__WHO__', name).replace('__OFF__', str(int(skew_ms))))
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(150000)
        self.errs, self.warns, self.notes = [], [], []
        self.pg.on('pageerror', lambda e: self.errs.append(str(e)[:240]))
        self.pg.on('console', self._con)
        self.subj = self.path = None
        self._c = None
        self.boots = 0

    def _con(self, msg):
        try:
            if msg.type in ('warning', 'error') and len(self.warns) < 400:
                self.warns.append(msg.text[:200])
        except Exception:
            pass

    def goto(self, subj, path='/app.html'):
        self.pg.goto('http://127.0.0.1:%d%s?subj=%s' % (self.srv.port, path, subj), wait_until='load')
        self.subj, self.path = subj, path
        self._ready()

    def reload(self):
        self.pg.reload(wait_until='load')
        self._ready()

    def ensure(self, subj, path='/app.html'):
        if self.subj != subj or self.path != path:
            self.goto(subj, path)

    def _ready(self):
        self.boots += 1
        self.pg.wait_for_function(READY, timeout=180000)
        if self.subj == 'phys' and (self.pdfs is None or self.pdfs):
            need = sorted(self.pdfs) if self.pdfs is not None else ['111', '222', '333', '444', '555', '666']
            try:
                self.pg.wait_for_function("n=>typeof HAVE!=='undefined'&&n.every(f=>HAVE[f])", arg=need, timeout=180000)
            except Exception:
                self.notes.append('시험지 기다림 넘침 %s' % need)
        self.pg.evaluate(KJS)
        r = self.pg.evaluate(SETTLE)
        if not r.get('ok'):
            self.notes.append('시동 고리 기다림 넘침 %s' % J(r))
        if self.ev("()=>__K.has()&&INKST.cyc<1"):
            self.ink()

    def ev(self, js, arg=None):
        return self.pg.evaluate(js, arg) if arg is not None else self.pg.evaluate(js)

    def ink(self):
        return self.ev("()=>__K.ink()")

    def rec(self):
        return self.ev("()=>__K.rec()")

    def st(self):
        return self.ev("()=>__K.st()")

    def get(self, k):
        return self.ev("k=>__K.get(k)", str(k))

    def wait(self, ms):
        self.pg.wait_for_timeout(ms)

    def has_sync(self):
        return bool(self.ev("()=>__K.has()"))

    def old_ink(self, subj, vals, path='/app.html'):
        """옛 필기(이미 쓴 것) — git 길을 막고(503) 앱을 연 뒤 putRaw 로 넣고 kv inkinit 를 지운다 → 막음을 풀고 새로 시동(첫 동기화)"""
        self.block_git = True
        try:
            if self.subj == subj and self.path == path:
                self.reload()
            else:
                self.goto(subj, path)
            n = self.ev(SEED, vals)
        finally:
            self.block_git = False
        self.reload()
        return n

    def cdp(self):
        if self._c is None:
            self._c = self.ctx.new_cdp_session(self.pg)
        return self._c

    def pen(self, pts):
        """진짜 펜 포인터(CDP Input.dispatchMouseEvent pointerType=pen) — 앱 pointerdown 은 펜만 받는다"""
        c = self.cdp()
        x, y = pts[0]
        c.send('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': x, 'y': y, 'pointerType': 'pen'})
        c.send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': x, 'y': y, 'button': 'left', 'buttons': 1, 'clickCount': 1, 'pointerType': 'pen', 'force': 0.5})
        for (x, y) in pts[1:]:
            c.send('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': x, 'y': y, 'button': 'left', 'buttons': 1, 'pointerType': 'pen', 'force': 0.5})
        c.send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': x, 'y': y, 'button': 'left', 'buttons': 0, 'clickCount': 1, 'pointerType': 'pen'})

    def errors(self):
        try:
            e = self.ev("()=>(window.__err||[]).slice(0,6)")
        except Exception:
            e = []
        return (self.errs[:4] + e)[:8]

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


# ════════════════════ 시험 ════════════════════
def seeds():
    S = {}
    S['I1p'] = {
        str(P['I1a']): {'0': [ln(0.10, 0.10, 0.30, 0.10), ln(0.10, 0.15, 0.30, 0.15, c='#B03A2E'), ln(0.10, 0.20, 0.30, 0.20, c='#1B7F4B')],
                        '1': [ln(0.55, 0.27, 0.85, 0.27, c='#16181B'), ln(0.55, 0.33, 0.85, 0.33, c='#B03A2E'), ln(0.55, 0.39, 0.85, 0.39, c='#2456A6')]},
        str(P['I1b']): {'0': mat(0, 5), '1': mat(5, 9)},
        str(P['I1c']): {'0': mat(9, 12), '1': mat(12, 16)},
    }
    common = ln(0.30, 0.70, 0.60, 0.72, c='#7A3E9D')
    S['I2A'] = {'0': [ln(0.10, 0.50, 0.30, 0.52), ln(0.10, 0.56, 0.30, 0.58, c='#B03A2E'), common, dot(0.62, 0.62), dot(0.62, 0.62)]}
    S['I2B'] = {'0': [ln(0.50, 0.50, 0.70, 0.52, c='#2456A6'), ln(0.50, 0.56, 0.70, 0.58, c='#1B7F4B'), common]}
    card = lambda: {'s': [ln(0.08, 0.06, 0.40, 0.06, r=1), ln(0.08, 0.11, 0.40, 0.11, c='#B03A2E', r=1), ln(0.08, 0.16, 0.40, 0.16, c='#1B7F4B', r=1),
                          ln(0.55, 0.06, 0.90, 0.06, c='#2456A6', r=2), ln(0.55, 0.11, 0.90, 0.11, r=2), ln(0.55, 0.16, 0.90, 0.16, c='#B03A2E', r=2)]}
    S['I1e'] = {'qink:' + EU['I1']: card(), 'bink:16': {'s': mat(16, 20)}, 'note:1': {'s': mat(20, 24)}}
    S['I1b_bio'] = {'qink:' + BU['I1']: card(), 'bink:10': {'s': mat(24, 28)}}
    return S


SEEDS = seeds()


def fname(k):
    return str(k).replace(':', '~') + '.json'


def boot(W, A, B, bio=True):
    """옛 필기 첫 시동 — A · B 가 물리(I1 · I2) · 지학(I1 카드 · 교재 · 서브노트) · 생물(I15) 옛 필기를 들고 새 판을 처음 연다"""
    S, r = SEEDS, {}
    s0 = W.snap()
    A.old_ink('phys', dict(S['I1p'], **{str(P['I2']): S['I2A']}))
    stA = A.st()
    B.old_ink('phys', {str(P['I2']): S['I2B']})
    stB = B.st()
    A.ink()
    r['phys_files'] = W.ink_files('phys')
    r['B_phys'] = {k: B.get(k) for k in S['I1p']}
    r['I2'] = {'A': A.get(P['I2']), 'B': B.get(P['I2'])}
    r['st'] = {'A': stA, 'B': stB}
    A.old_ink('earth', S['I1e'])
    B.goto('earth')
    r['earth_files'] = W.ink_files('earth')
    r['B_earth'] = {k: B.get(k) for k in S['I1e']}
    if bio:
        A.old_ink('bio', S['I1b_bio'])
        B.goto('bio')
        r['bio_files'] = W.ink_files('bio')
        r['B_bio'] = {k: B.get(k) for k in S['I1b_bio']}
    r['req'] = W.delta(s0)
    return r


def judge_I1(r):
    """원격 파일 6(물리 3 · 지학 3) · B 받은 값 = A 옛 필기(획 수 · 차례 · 좌표 ≤ 1/10000) — (전체, 값, 물리 몫, 지학 몫)"""
    S = SEEDS
    fp, fe = [fname(k) for k in S['I1p']], [fname(k) for k in S['I1e']]
    hp = [f for f in fp if f in r['phys_files']]
    he = [f for f in fe if f in r['earth_files']]
    cmp, okp, oke = {}, len(hp) == 3, len(he) == 3
    for k in S['I1p']:
        o, d = cmp_val(S['I1p'][k], r['B_phys'].get(k))
        cmp[k] = d if o else {'FAIL': d}
        okp = okp and o
    for k in S['I1e']:
        o, d = cmp_val(S['I1e'][k], r['B_earth'].get(k))
        cmp[k] = d if o else {'FAIL': d}
        oke = oke and o
    stA = r['st']['A']
    return okp and oke, {'원격 파일(I1 열쇠)': '%d/6' % (len(hp) + len(he)), '없음': [f for f in fp + fe if f not in hp + he], 'B 받은 값': cmp,
                         'A 시동 고리': stA.get('st') if isinstance(stA, dict) and 'st' in stA else stA}, okp, oke


def judge_I2(r):
    S = SEEDS
    want_ = mset(S['I2A']) | mset(S['I2B'])   # 합집합(겹친 획 한 번 · 점 획 둘은 그 기기에 두 번 있던 만큼)
    a, b = mset(r['I2']['A']), mset(r['I2']['B'])
    ok = a == want_ and b == want_
    dots = sum(n for (g, s), n in a.items() if len(s[4]) == 2)
    return ok, {'바라는 획': sum(want_.values()), 'A': sum(a.values()), 'B': sum(b.values()), 'A 점 획': dots,
                '겹친 획(A)': a.get(('0', sig(S['I2A']['0'][2])), 0), 'A 모자람': mset_show(want_ - a)[:6], 'A 넘침': mset_show(a - want_)[:6],
                'B 모자람': mset_show(want_ - b)[:6], 'B 넘침': mset_show(b - want_)[:6]}


def judge_bio1(r):
    S = SEEDS
    ok = all(fname(k) in r.get('bio_files', {}) for k in S['I1b_bio'])
    cmp = {}
    for k in S['I1b_bio']:
        o, d = cmp_val(S['I1b_bio'][k], (r.get('B_bio') or {}).get(k))
        cmp[k] = d if o else {'FAIL': d}
        ok = ok and o
    return ok, {'원격 파일': sorted(r.get('bio_files', {}))[:6], 'B 받은 값': cmp}


def t_I3(W, A, B):
    """B 가 물리 문항(75)에서 지우개로 1 층 획 하나 · 0 층은 「지금 회독 지우기」 → A 에서 그 획들 없음 · 나머지 그대로"""
    no, k = P['I1a'], str(P['I1a'])
    A.ensure('phys')
    B.ensure('phys')
    s0 = B.ev(OPEN, no)
    mode = B.ev(ERASE_TOOL)
    pt = pick_pt(B, CANVAS_PT, [(0.70, 0.27), (0.60, 0.27), (0.80, 0.27), (0.55, 0.27), (0.85, 0.27)])   # 1 층 첫 획(0.55~0.85 · 0.27)의 점
    if pt and pt.get('on'):
        B.pen([(pt['x'], pt['y']), (pt['x'] + 1, pt['y'])])
    B.wait(600)
    s1 = B.ev("()=>__K.phys()")
    B.ev(LAYER_SEL, 0)
    sh = B.ev(ERASE_SHEET_CUR)
    s2 = B.ev("()=>__K.phys()")
    B.ev(TOOL_VIEW)
    B.ink()
    A.ink()
    a = A.get(k)
    exp = {'0': [], '1': SEEDS['I1p'][k]['1'][1:]}
    ok, d = cmp_val(exp, a)
    doc = W.ink_doc('phys', k)
    return ok, {'B 연 뒤': s0.get('n'), 'B 층': s0.get('LAYER'), '지우개': mode, '누른 자리': pt and {kk: pt[kk] for kk in ('on', 'top')},
                'B 지우개 뒤': s1.get('n'), '지금 회독 지우기': sh, 'B 뒤': s2.get('n'), 'A 값 대조': d,
                '원격 지운 수(x)': len((doc or {}).get('x', {})), 'B 오류': B.errors()}


def t_card3(W, A, B, subj, uid):
    """카드(지학 · 생물) — B 가 화면 펜 지우개로 2 회독 획 하나 · 1 회독은 「지금 회독 지우기」 → A 에서 없음 · 나머지 그대로"""
    A.ensure(subj)
    B.ensure(subj)
    k = 'qink:' + uid
    no = B.ev("u=>uidNo(u)", uid)
    c0 = B.ev(OPEN_CARD, no)
    mode = B.ev(ERASE_TOOL)
    pt = pick_pt(B, CARD_PT, [(0.725, 0.06), (0.6667, 0.06), (0.7833, 0.06), (0.6083, 0.06), (0.8417, 0.06)])   # 2 회독 첫 획(0.55~0.90 · 0.06)의 점
    if pt and pt.get('on'):
        B.pen([(pt['x'], pt['y']), (pt['x'] + 1, pt['y'])])
    B.wait(700)
    c1 = B.ev("()=>__K.card()")
    B.ev(LAYER_SEL, 1)
    sh = B.ev(ERASE_SHEET_CUR)
    c2 = B.ev("()=>__K.card()")
    B.ev(TOOL_VIEW)
    B.ink()
    A.ink()
    a = A.get(k)
    seed = SEEDS['I1e' if subj == 'earth' else 'I1b_bio'][k]['s']
    ok, d = cmp_val({'s': seed[4:6]}, a)
    return ok, {'B 연 뒤': c0, '지우개': mode, '누른 자리': pt and {kk: pt.get(kk) for kk in ('on', 'top')}, 'B 지우개 뒤': c1.get('n'),
                '지금 회독 지우기': sh, 'B 뒤': c2.get('n'), 'A 값 대조': d, 'B 오류': B.errors()}


def t_I4(W, A, B):
    """↶ 건너감 — B 가 긋고 동기화 → A 에 옴 → B ↶ → 동기화 → A 에서 없음"""
    no, k = P['I4'], str(P['I4'])
    A.ensure('phys')
    B.ensure('phys')
    b1 = ln(0.20, 0.20, 0.45, 0.24, c='#B03A2E')
    B.ev(DRAW, {'no': no, 'layer': None, 'strokes': [b1]})
    B.ink()
    A.ink()
    got1 = sig(b1) in [x[1] for x in mset(A.get(k))]
    B.ev("()=>{document.getElementById('tUndo').click();return 1}")
    B.wait(600)
    sb = B.ev("()=>__K.phys()")
    B.ink()
    A.ink()
    gone = sig(b1) not in [x[1] for x in mset(A.get(k))]
    doc = W.ink_doc('phys', k) or {}
    return got1 and gone, {'A 에 옴': got1, 'B ↶ 뒤 획': sb.get('n'), 'A 에서 없음': gone, '원격 x': len(doc.get('x', {}))}


def t_I5(W, A, B):
    """빈 층이 안 덮음 — A 가 21(지난 회독 2) 2 회독(1 층)에 획 · B 는 그 뒤 열기만(빈 1·2 층이 메모리에 섬) → 동기화 → A 의 1 층 그대로"""
    no, k = P['I5'], str(P['I5'])
    A.ensure('phys')
    B.ensure('phys')
    a1, a2 = ln(0.15, 0.30, 0.40, 0.30, c='#2456A6'), ln(0.15, 0.36, 0.40, 0.36, c='#B03A2E')
    sa = A.ev(DRAW, {'no': no, 'layer': 1, 'strokes': [a1, a2]})
    A.ink()
    sb0 = B.ev(OPEN, no)
    B.ink()
    sb1 = B.ev("()=>__K.phys()")
    A.ink()
    av = A.get(k)
    keep = mset(av)
    ok1 = keep[('1', sig(a1))] == 1 and keep[('1', sig(a2))] == 1
    b1 = ln(0.60, 0.50, 0.80, 0.52, c='#1B7F4B')
    B.ev(DRAW, {'no': no, 'layer': None, 'strokes': [b1]})
    B.ink()
    A.ink()
    k2 = mset(A.get(k))
    ok2 = k2[('1', sig(a1))] == 1 and k2[('1', sig(a2))] == 1 and sum(n for (g, s), n in k2.items() if s == sig(b1)) == 1
    doc = W.ink_doc('phys', k) or {}
    return ok1 and ok2 and sb1.get('n', {}).get('1') == 2, {
        'A 층(지난 회독 2)': [sa.get('LAYER'), sa.get('keys')], 'B 열기만': [sb0.get('keys'), sb0.get('n')],
        'B 동기화 뒤 메모리': sb1.get('n'), 'A 1 층 남음': ok1, 'B 가 2 층에 한 획 더 뒤 A': ok2, '원격 x': len(doc.get('x', {}))}


def t_I6(W, A, B):
    """동시 · 겹침 — A · B 가 같은 문항 다른 층 · 같은 층에 각자 → 둘 다 남음 · A 필기 PATCH 를 붙잡은 사이 B 기록 동기화(+필기)가 ref 를 옮김 → 422 → 다시 한 번"""
    no, k = P['I6'], str(P['I6'])
    A.ensure('phys')
    B.ensure('phys')
    a1 = ln(0.10, 0.60, 0.30, 0.62, c='#16181B')
    b2 = ln(0.50, 0.60, 0.70, 0.62, c='#2456A6')
    b1 = ln(0.50, 0.70, 0.70, 0.72, c='#B03A2E')
    A.ev(DRAW, {'no': no, 'layer': 0, 'strokes': [a1]})
    B.ev(DRAW, {'no': no, 'layer': 0, 'strokes': [b2]})
    B.ev(DRAW, {'no': no, 'layer': 1, 'strokes': [b1]})
    r0 = A.st()['st']['retry']
    n422 = W.n('A', 'ref-patch', 422)
    put0 = len(W.puts)
    W.hold = {'dev': 'A', 'kind': 'ref-patch'}
    A.ev("()=>{window.__bgp=__K.ink();return 1}")
    t = time.time()
    while not W.held and time.time() - t < 30:
        A.wait(50)
    held = len(W.held)
    sb = B.rec()   # 기록 동기화(contents PUT · 같은 ref) → 끝에 inkKick(B 필기 커밋)
    rel = W.release()
    W.hold = None
    sa = A.ev("()=>window.__bgp")
    B.ink()
    A.ink()
    want_ = collections.Counter({('0', sig(a1)): 1, ('0', sig(b2)): 1, ('1', sig(b1)): 1})
    ma, mb = mset(A.get(k)), mset(B.get(k))
    retry = (sa or {}).get('st', {}).get('retry', 0) - r0
    d422 = W.n('A', 'ref-patch', 422) - n422
    rec_put = [p['dev'] + ' ' + p['path'] for p in W.puts[put0:]]
    ok = ma == want_ and mb == want_ and held == 1 and retry == 1 and d422 == 1 and any(x.startswith('B ') for x in rec_put)
    return ok, {'붙잡음': held, '풂': rel, '그사이 기록 PUT': rec_put, 'A 422': d422, 'A 다시 수': retry, 'A 오류 칩': (sa or {}).get('err'),
                'A': mset_show(ma), 'B': mset_show(mb), 'B 칩': (sb or {}).get('chip')}


def t_I7(W, A, B):
    """글자 왕복 — 실기록 손필기 획(쪽 소수) → 글자 → 소수 → 글자 = 같은 글자 · 동기화로 건너간 획도 같은 글자 · 다시 동기화해도 커밋 0"""
    no, k = P['I7'], str(P['I7'])
    A.ensure('phys')
    B.ensure('phys')
    M = mat(0, 28)
    rt = A.ev(r"""S=>{let bad=0,pts=0,dup=0;const first=[];for(const st of S){const e1=inkEnc(st),d=inkDec(e1),e2=inkEnc(d);if(e1!==e2){bad++;if(first.length<2)first.push([e1.slice(0,80),e2.slice(0,80)])}
      pts+=st.p.length/2;dup+=st.p.length/2-d.p.length/2}return {n:S.length,bad,pts,dup,first}}""", M)
    A.ev(DRAW, {'no': no, 'layer': 0, 'strokes': M})
    eA = A.ev("k=>get('ink',k).then(v=>(v['0']||[]).map(s=>inkEnc(s)))", k)
    A.ink()
    B.ink()
    eB = B.ev("k=>get('ink',k).then(v=>v?(v['0']||[]).map(s=>inkEnc(s)):[])", k)
    same_e = eA == eB
    ok_c, d = cmp_val({'0': M}, B.get(k))
    c0, cA0, cB0 = len(W.ink_log), A.st()['st'], B.st()['st']
    A.ink()
    B.ink()
    B.ev(OPEN, no)
    B.ev("()=>__K.close()")
    A.ink()
    B.ink()
    cA1, cB1 = A.st()['st'], B.st()['st']
    commits = len(W.ink_log) - c0
    ok = rt['bad'] == 0 and same_e and ok_c and commits == 0
    return ok, {'재료': MAT_SRC, '왕복': rt, 'A 글자 = B 글자': same_e, '획 수': [len(eA), len(eB)], 'B 값 대조': d, '다시 동기화 커밋': commits,
                '다시 동기화 받기(dl)': [cA1['dl'] - cA0['dl'], cB1['dl'] - cB0['dl']]}


def t_I8(W, A, B):
    """크기(INFO) — 표본 문항(실기록 획 넷 층 · 점 ≈10,800) 파일 · 점당 B · 한 층 그렸다 다 지우기 10 번 뒤(같은 획 · 다른 획)"""
    A.ensure('phys')
    M = mat(0, 28)
    res = {}
    for nm, no, shift in (('같은 획', P['I8a'], 0.0), ('다른 획', P['I8b'], 0.002)):
        k = str(no)
        for L in range(4):
            A.ev(DRAW, {'no': no, 'layer': L, 'strokes': M, 'wait': 400})
        A.ink()
        raw0 = W.ink_raw('phys', k) or b''
        doc = json.loads(raw0.decode('utf-8')) if raw0 else {}
        pts = epart = 0
        for g in (doc.get('g') or {}).values():
            for r in g.values():
                if 'e' in r:
                    b = r['e'][r['e'].rfind('|') + 1:]
                    pts += b.count(';') + 1 if b else 0
                    epart += len(b.encode('utf-8'))
        size0 = len(raw0)
        for i in range(1, 11):
            S = [dict(s, p=[round(v + (shift * i if j % 2 == 0 else 0), 6) for j, v in enumerate(s['p'])]) for s in M]
            A.ev(DRAW, {'no': no, 'layer': 4, 'strokes': S, 'wait': 380})
            A.ink()
            A.ev(r"""async()=>{INK[LAYER]=[];paintInk();saveInk();await __K.sleep(400);return 1}""")   # 지금 회독 지우기(eraseSheet onCur 와 같은 세 줄)
            A.ink()
        size1 = len(W.ink_raw('phys', k) or b'')
        res[nm] = {'점': pts, '파일 B': size0, '점당 B(파일)': round(size0 / max(1, pts), 2), '점당 B(점 글자)': round(epart / max(1, pts), 2),
                   '≤80KB': size0 <= 80 * 1024, '10 번 뒤 B': size1, '배': round(size1 / max(1, size0), 3), '≤1.2배': size1 <= 1.2 * size0}
    return res


def t_I9(W, A, B, br, srv):
    """옛 판과 섞임 — 바탕 기기 C 가 기록을 올려도 phys/ink 그대로 · 새 판 필기 안 잃음 · 기록.json 열쇠 · 값 무변(같은 기기 바탕 PUT ↔ 새 판 PUT)"""
    A.ensure('phys')
    keysA = [str(P[x]) for x in ('I1a', 'I2', 'I7')]
    before = W.ink_files('phys')
    valA0 = {k: A.get(k) for k in keysA}
    C = Dev(br, W, srv, 'C', view='pc', pdfs=set())
    try:
        p0 = len(W.puts)
        C.goto('phys', '/base.html')
        C.rec()
        put_base = [p for p in W.puts[p0:] if p['dev'] == 'C' and p['path'] == 'phys/기록.json']
        after = W.ink_files('phys')
        s0 = A.st()['st']
        A.ink()
        s1 = A.st()['st']
        valA1 = {k: A.get(k) for k in keysA}
        p1 = len(W.puts)
        C.goto('phys', '/app.html')   # 같은 기기(같은 출처)를 새 판으로
        C.rec()
        put_new = [p for p in W.puts[p1:] if p['dev'] == 'C' and p['path'] == 'phys/기록.json']
        cmpd = {}
        okr = bool(put_base and put_new)
        if okr:
            jb, jn = json.loads(put_base[-1]['text']), json.loads(put_new[-1]['text'])
            kb, kn = sorted(jb), sorted(jn)
            dkb, dkn = sorted((jb.get('data') or {})), sorted((jn.get('data') or {}))
            diff = [x for x in sorted(set(kb) | set(kn)) if x != 'savedAt' and jb.get(x) != jn.get(x)]
            cmpd = {'바탕 열쇠': kb, '새 판 열쇠': kn, 'data 열쇠 같음': dkb == dkn, '값 다른 칸(savedAt 뺌)': diff, 'data 칸 수': len(dkn)}
            okr = kb == kn and dkb == dkn and not diff
        same_ink = before == after
        keep = all(cmp_val(valA0[k], valA1[k])[0] for k in keysA)
        ok = same_ink and keep and s1['dl'] - s0['dl'] == 0 and s1['commit'] - s0['commit'] == 0 and okr
        return ok, {'바탕 PUT': len(put_base), 'phys/ink 그대로': same_ink, '파일 수': len(after), 'A 받기 · 커밋': [s1['dl'] - s0['dl'], s1['commit'] - s0['commit']],
                    'A 필기 그대로': keep, '기록.json': cmpd, 'C 오류': C.errors()}
    finally:
        C.close()


def t_I10(W, A, B):
    """열린 창 다시 그림 — A 가 5(지난 회독 1 · 가림 켜짐)를 열어 둔 채 B 가 획 → A 동기화 → A 화면 획 수 늘어남 · 층 · 가림 그대로 → A 가 그 자리에서 한 획 더 → B 의 획 그대로"""
    no, k = P['I10'], str(P['I10'])
    A.ensure('phys')
    B.ensure('phys')
    a0 = A.ev(OPEN, no)
    A.ev(r"""()=>{if(!window.__pspy){const p=paintInk;paintInk=function(){window.__pc=(window.__pc||0)+1;return p.apply(this,arguments)};window.__pspy=1}window.__inkRef=INK;return 1}""")
    b1 = ln(0.30, 0.30, 0.50, 0.32, c='#2456A6')
    B.ev(DRAW, {'no': no, 'layer': None, 'strokes': [b1]})
    B.ink()
    pc0 = A.ev("()=>window.__pc||0")
    A.ink()
    a1 = A.ev("()=>Object.assign(__K.phys(),{same:INK===window.__inkRef,pc:window.__pc||0})")
    ok1 = a1['vis'] == a0['vis'] + 1 and a1['LAYER'] == a0['LAYER'] and a1['HIDEOLD'] == a0['HIDEOLD'] and a1['same'] and a1['pc'] > pc0
    s1 = ln(0.30, 0.42, 0.50, 0.44, c='#B03A2E')
    A.ev(DRAW, {'no': no, 'layer': None, 'strokes': [s1]})
    A.ink()
    B.ink()
    mb = mset(B.get(k))
    ok2 = sum(n for (g, s), n in mb.items() if s == sig(b1)) == 1 and sum(n for (g, s), n in mb.items() if s == sig(s1)) == 1
    return ok1 and ok2, {'A 연 뒤': {x: a0.get(x) for x in ('LAYER', 'HIDEOLD', 'vis', 'n')}, 'A 동기화 뒤': {x: a1.get(x) for x in ('LAYER', 'HIDEOLD', 'vis', 'n', 'same')},
                         '다시 그림 수': a1['pc'] - pc0, 'A 화면 늘어남': ok1, 'A 한 획 더 뒤 B': mset_show(mb), 'B 획 남음': ok2}


def t_I11(W, br, srv):
    """첫 동기화 나눠 올림 — 기기 E 에 옛 필기 150 열쇠 → 고리 60 · 60 · (403 흉내 = 멈춤) · 30 · 고리당 커밋 1 · 칩 「필기 n 대기」 90 → 30 → 사라짐"""
    E = Dev(br, W, srv, 'E', view='pc', pdfs=set())
    try:
        vals = {k: {'0': [ln(0.1 + (int(k) % 7) * 0.05, 0.1, 0.3 + (int(k) % 7) * 0.05, 0.12, n=5)]} for k in I11_KEYS}
        W.limit = 80
        W.wtimes.clear()   # 흉내 한도는 이 칸부터 센다 — 앞 칸들(I8 등)의 쓰기가 1 분 창에 남아 E 의 첫 쓰기부터 403 이 났다(1 차 실행 · 분당 141)
        W.wmax = 0
        c0 = len(W.ink_log)
        E.goto('phys')
        E.old_ink('phys', vals)
        seq = [E.st()]
        seq.append(E.ink())
        W.inject('E', 'tree-post', 403, 1)
        seq.append(E.ink())
        seq.append(E.ink())
        W.limit = None
        commits = [x['n'] for x in W.ink_log[c0:] if x['dev'] == 'E']
        files = W.ink_files('phys')
        have = sum(1 for k in I11_KEYS if fname(k) in files)
        dirt = [s.get('dirty') for s in seq]
        chips = [s.get('chip') for s in seq]
        recs = [s.get('rec') for s in seq]
        errs = [s.get('err') for s in seq]
        recerr = [s.get('recErr') for s in seq]
        # 3876491 — inkChip 은 올릴 필기가 있을 때만 · 실패면 「필기 한도 · n 대기」 + #recChip err
        ok = (commits == [60, 60, 30] and dirt == [90, 30, 30, 0] and chips[0] == '필기 90 대기' and chips[1] == '필기 30 대기'
              and errs[2] == '필기 한도' and chips[2] == '필기 한도 · 30 대기' and chips[3] == '' and have == 150
              and '필기 90 대기' in (recs[0] or '') and '필기 한도 · 30 대기' in (recs[2] or '') and recerr[2] is True
              and '필기' not in (recs[3] or '') and recerr[3] is False)
        return ok, {'커밋(열쇠 수)': commits, '더러움': dirt, '칩': chips, '기록 칩': recs, '기록 칩 err': recerr, '오류': errs, '원격 150 중': have,
                    '분당 쓰기 최대(흉내 한도 80)': W.wmax, 'E 오류': E.errors()}, E
    except Exception:
        W.limit = None
        E.close()
        raise


def t_I12(W, A, br, srv):
    """시계 어긋남 — 기기 D(Date +1 시간) 첫 동기화 뒤 A 가 지운 획이 A · D 에서 다 없음 · D 가 새로 그은 획이 A 에서 보임"""
    no, k = P['I12'], str(P['I12'])
    A.ensure('phys')
    D = Dev(br, W, srv, 'D', view='pc', skew_ms=3600000, pdfs=set())
    try:
        d1, d2, d3 = ln(0.10, 0.20, 0.30, 0.20), ln(0.10, 0.30, 0.30, 0.30, c='#B03A2E'), ln(0.10, 0.40, 0.30, 0.40, c='#2456A6')
        D.goto('phys')
        skew = D.ev("()=>Date.now()-performance.timeOrigin-performance.now()")
        D.old_ink('phys', {k: {'0': [d1, d2, d3]}})
        A.ink()
        doc0 = W.ink_doc('phys', k) or {}
        t_d1 = [r['t'] for g in doc0.get('g', {}).values() for r in g.values()]
        A.ev(OPEN, no)
        A.ev(r"""a=>{const [x,y]=toPix(a[0],a[1]);eraseAt(x,y);paintInk();saveInk();return (INK[LAYER]||[]).length}""", [0.20, 0.20])   # 지우개(pointer 와 같은 eraseAt · endDraw 의 paintInk+saveInk)
        A.wait(500)
        A.ink()
        doc1 = W.ink_doc('phys', k) or {}
        D.ink()
        mA, mD = mset(A.get(k)), mset(D.get(k))
        gone = ('0', sig(d1)) not in mA and ('0', sig(d1)) not in mD and mA[('0', sig(d2))] == 1 and mD[('0', sig(d2))] == 1
        d4 = ln(0.50, 0.50, 0.70, 0.50, c='#1B7F4B')
        D.ev(DRAW, {'no': no, 'layer': 0, 'strokes': [d4]})
        D.ink()
        A.ink()
        seen = mset(A.get(k))[('0', sig(d4))] == 1
        xs = list((doc1.get('x') or {}).values())
        return gone and seen, {'D 시계 앞섬(ms)': round(skew), 'D 획 t − 지금': [round(t - time.time() * 1000) for t in t_d1][:3], '원격 x': xs[:3],
                               'x > t': bool(xs) and min(xs) > max(t_d1 or [0]) - 1, 'A·D 에서 지운 획 없음': gone, 'D 새 획 A 에 보임': seen, 'D 오류': D.errors()}
    finally:
        D.close()


def t_I13(W, A, B):
    """동기화 밖 열쇠 — 카드 층 맨 uid · 옮기지 못한 번호 · diag: · ink_orphan: · 옛 꼴(순배열) · 다른 글자 → 원격에 안 생김 · 들이기 중 syncInk 안 돎(옮김 끝난 뒤)"""
    st = ln(0.2, 0.2, 0.4, 0.2)
    out_ = {}
    ok = True

    def keys_part(subj, K):
        A.ensure(subj)
        w0 = len(A.warns)
        dk = A.ev(r"""async K=>{for(const k of Object.keys(K))await __K.put(k,K[k]);return [...INKDIRTY].filter(k=>k in K)}""", K)
        A.ink()
        files = W.ink_files(subj)
        made = [k for k in K if fname(k) in files]
        dk2 = A.ev("K=>[...INKDIRTY].filter(k=>k in K)", K)
        warn = [w for w in A.warns[w0:] if '동기화 밖' in w]
        out_[subj] = {'더러움 표시된 것(넣은 직후)': dk, '원격에 생긴 것': made, '고리 뒤 더러움': dk2, '콘솔 경고': warn[:3]}
        return not made and not dk2

    ok = keys_part('earth', {'G95-32-03': {'s': [st]}, '9999': {'s': [st]}, 'diag:h1': {'s': [st]}, 'ink_orphan:G95-32-04': {'s': [st]},
                             'qink:G95-32-05': [st], 'qink:가나': {'s': [st]}})
    # 들이기 중 syncInk — 지학 A 에서 내보낸 백업을 들이며 5ms 마다 inkKick
    with A.pg.expect_download(timeout=60000) as dl:
        A.ev("()=>{exportData(false);return 1}")
    txt = open(dl.value.path(), encoding='utf-8').read()
    gi = A.ev(r"""async t=>{window.__ic=[];window.__mig=[];
      if(!window.__icw){const c=inkCycle;inkCycle=async function(){window.__ic.push({t:performance.now(),imp:INKIMPORT,uid:UID_BUSY});return c.apply(this,arguments)};
        const m=uidMigrateImport;uidMigrateImport=async function(){const a=performance.now();try{return await m.apply(this,arguments)}finally{window.__mig.push([a,performance.now()])}};window.__icw=1}
      const kick=setInterval(()=>{try{inkKick()}catch(e){}},5);const t0=performance.now();let err='';
      try{await importData(new File([t],'b.json',{type:'application/json'}))}catch(e){err=String(e)}
      const t1=performance.now();await __K.sleep(400);clearInterval(kick);await __K.idle();
      const during=window.__ic.filter(x=>x.t>=t0&&x.t<=t1),after=window.__ic.filter(x=>x.t>t1);
      return {err,ms:Math.round(t1-t0),during:during.length,bad:window.__ic.filter(x=>x.imp>0||x.uid>0).length,after:after.length,
        mig:window.__mig.map(m=>[Math.round(m[0]-t0),Math.round(m[1]-t0)]),firstAfter:after.length?Math.round(after[0].t-t0):null}}""", txt)
    mig_ok = bool(gi.get('mig')) and (gi.get('firstAfter') is None or gi['firstAfter'] >= gi['mig'][-1][1])
    o2 = gi.get('bad') == 0 and gi.get('during') == 0 and mig_ok and not gi.get('err')
    out_['들이기'] = dict(gi, **{'옮김 뒤 첫 고리': mig_ok, '백업 B': len(txt)})
    ok3 = keys_part('phys', {'diag:p1': {'0': [st]}, 'ink_orphan:12': {'0': [st]}, 'bink:3': {'s': [st]}, 'qink:G1': {'s': [st]}, '271': [st]})
    return ok and o2 and ok3, out_


def t_I14a(W, A, B):
    """획을 긋고 300ms 안에 동기화 → 그 획 안 잃음(그 고리는 그 열쇠를 건너뜀 · 다음 고리에 올라감) — B 가 먼저 같은 문항을 올려 둬 받을 것이 있게"""
    no, k = P['I14a'], str(P['I14a'])
    A.ensure('phys')
    B.ensure('phys')
    b1 = ln(0.60, 0.15, 0.85, 0.15, c='#2456A6')
    B.ev(DRAW, {'no': no, 'layer': 0, 'strokes': [b1]})
    B.ink()
    A.ev(OPEN, no)
    A.ev("()=>{const b=document.querySelector('[data-pen]');if(b)b.click();return TOOL.mode}")
    p0 = pick_pt(A, CANVAS_PT, [(0.20, 0.30), (0.20, 0.55), (0.55, 0.55), (0.30, 0.75)])
    p1 = A.ev(CANVAS_PT, [p0['u'] + 0.25, p0['v'] + 0.03])
    pts = [(p0['x'] + (p1['x'] - p0['x']) * i / 8, p0['y'] + (p1['y'] - p0['y']) * i / 8) for i in range(9)]
    A.pen(pts)
    r = A.ev(r"""async()=>{const t=performance.now(),s0=INKST.skip,n=(INK[LAYER]||[]).length;await syncInk();await __K.idle();
      return {gap:Math.round(t-(window.__lastUp||0)),skip:INKST.skip-s0,n,n1:(INK[LAYER]||[]).length,mode:TOOL.mode}}""")
    doc1 = W.ink_doc('phys', k) or {}
    alive1 = sum(1 for g in doc1.get('g', {}).values() for x in g.values() if 'e' in x)
    A.wait(600)
    A.ink()
    B.ink()
    A.ev(TOOL_VIEW)
    ma, mb = mset(A.get(k)), mset(B.get(k))
    drawn = [s for (g, s) in ma if s != sig(b1)]
    kept = bool(drawn) and len(drawn) == 1 and ma[('0', sig(b1))] == 1 and mb[('0', drawn[0])] == 1
    ok = r['gap'] < 300 and r['n1'] >= 1 and r['n1'] == r['n'] and kept
    return ok, {'그은 뒤 동기화까지 ms(< 300 이어야 잰 것)': r['gap'], '그 고리 건너뜀(skip)': r['skip'], '첫 고리 뒤 원격 산 획(1 = 다음 고리로 미룸)': alive1,
                'A 메모리 획(고리 앞 · 뒤)': [r['n'], r['n1']], '다음 고리 뒤 A': mset_show(ma), 'B': mset_show(mb), '안 잃음': kept,
                '펜': p0 and {x: p0.get(x) for x in ('on', 'top')}, '도구': r.get('mode')}


def t_I14b(W, A, B):
    """교재 쪽 캐시(BK.ink)가 산 채 원격 갱신 → 그 자리 객체 안에서 맞춤 → 한 획 더 → 다른 기기 획 남음"""
    A.ensure('earth')
    B.ensure('earth')
    key = 'bink:17'
    oa = A.ev(BK_OPEN, 17)
    s1 = A.ev(BK_COMMIT, {'key': key, 'pts': [[0.10 + 0.02 * i, 0.20] for i in range(8)], 'c': '#243a5e', 'w': 1.2})
    A.ink()
    B.ev(BK_OPEN, 17)
    B.ink()
    s2 = B.ev(BK_COMMIT, {'key': key, 'pts': [[0.10 + 0.02 * i, 0.35] for i in range(8)], 'c': '#B03A2E', 'w': 1.2})
    B.ink()
    A.ev("k=>{window.__bkRef=BK.ink[k];return !!window.__bkRef}", key)
    A.ink()
    a1 = A.ev(BK_STATE, key)
    s3 = A.ev(BK_COMMIT, {'key': key, 'pts': [[0.10 + 0.02 * i, 0.50] for i in range(8)], 'c': '#1B7F4B', 'w': 1.2})
    A.ink()
    B.ink()
    bv = B.get(key)
    mb = mset(bv)
    refs = [x.get('last') for x in (s1, s2, s3)]
    ok_refs = all(isinstance(x, dict) for x in refs)
    have = [mb[('s', sig(x))] == 1 if isinstance(x, dict) else False for x in refs]
    ok1 = a1.get('n') == 2 and a1.get('same') is True and a1.get('paths') in (None, 2)
    ok = ok_refs and ok1 and all(have)
    return ok, {'A 쪽': oa.get('n'), 'A 받은 뒤 캐시': {x: a1.get(x) for x in ('n', 'same', 'paths')}, 'B 에 남은 획(s1 · s2 · s3)': have, 'B 값 획 수': len((bv or {}).get('s', []))}


def t_I14c(W, A, B, E):
    """옛 백업 들이기 → 다른 기기의 새 획 남음(B) · 원격 파일에서도 산 채(글자 e) · 들인 기기 A 화면도 다음 고리에서 합친 값(§A-4)"""
    no, k = P['I14c'], str(P['I14c'])
    A.ensure('phys')
    B.ensure('phys')
    a1 = ln(0.15, 0.25, 0.40, 0.25)
    A.ev(DRAW, {'no': no, 'layer': 0, 'strokes': [a1]})
    A.ink()
    with A.pg.expect_download(timeout=60000) as dl:
        A.ev("()=>{exportData(false);return 1}")
    txt = open(dl.value.path(), encoding='utf-8').read()
    bk = json.loads(txt)
    B.ink()
    b1 = ln(0.15, 0.45, 0.40, 0.45, c='#B03A2E')
    B.ev(DRAW, {'no': no, 'layer': 0, 'strokes': [b1]})
    B.ink()
    A.ev("()=>__K.close()")
    A.ink()
    before = mset(A.get(k))
    imp = A.ev(r"""async t=>{let err='';try{await importData(new File([t],'b.json',{type:'application/json'}))}catch(e){err=String(e)}await __K.sleep(300);
      return {err,add:[...INKADDONLY].length,dirty:INKDIRTY.size}}""", txt)
    after_imp = mset(A.get(k))
    hb = lambda dv: mset(dv.get(k))[('0', sig(b1))] == 1

    def rdoc():
        d = W.ink_doc('phys', k) or {}
        x = d.get('x') or {}
        return {'산 획(글자 있음)': sum(1 for g in (d.get('g') or {}).values() for i, r in g.items() if 'e' in r and r['t'] > x.get(i, 0)),
                '산 획(글자 없음)': sum(1 for g in (d.get('g') or {}).values() for i, r in g.items() if 'e' not in r and r['t'] > x.get(i, 0)),
                '지운 획': len(x)}
    steps = []
    A.ink()
    steps.append(['① A 들인 뒤 첫 고리', {'원격': rdoc(), 'A b1': hb(A)}])
    e_has = None
    if E is not None:
        E.ensure('phys')
        E.ink()
        e_has = hb(E)
        steps.append(['② 셋째 기기 E 받음', {'E b1': e_has}])
    B.ink()
    steps.append(['③ B 고리', {'원격': rdoc(), 'B b1': hb(B)}])
    A.ink()
    steps.append(['④ A 고리', {'원격': rdoc(), 'A b1': hb(A)}])
    B.ink()
    endB = hb(B)
    steps.append(['⑤ B 고리(끝)', {'원격': rdoc(), 'B b1': endB}])
    A.ink()
    endA = hb(A)
    endR = rdoc()
    steps.append(['⑥ A 고리(끝)', {'원격': endR, 'A b1': endA}])
    first = steps[0][1]
    ok = endB and endA and endR['산 획(글자 있음)'] == 2 and first['원격']['산 획(글자 있음)'] == 2 and first['A b1'] and (e_has is not False)
    return ok, {'백업 안 이 문항': bool((bk.get('ink') or {}).get(k)), '들이기 전 A': sum(before.values()), '들인 직후 A': sum(after_imp.values()), '들이기': imp,
                '차례': steps, '끝 — B b1(§B-14ⓒ)': endB, '끝 — A b1(§A-4 다음 고리 합친 값)': endA, '끝 — 원격 산 획 2': endR['산 획(글자 있음)'] == 2}


def t_I14d(W, A, B):
    """1 층이 빈 물리 문항(0 · 2 층 획) · 지난 회독 2 개인 다른 기기가 열기 → 2 층 획 남음(빈 층 메움 · 덮어쓰지 않음)"""
    no, k = P['I14d'], str(P['I14d'])
    A.ensure('phys')
    B.ensure('phys')
    a0, a2 = ln(0.10, 0.12, 0.30, 0.12), ln(0.10, 0.50, 0.30, 0.50, c='#B03A2E')
    A.ev(DRAW, {'no': no, 'layer': 0, 'strokes': [a0]})
    sa = A.ev(DRAW, {'no': no, 'layer': 2, 'strokes': [a2]})
    A.ink()
    doc = W.ink_doc('phys', k) or {}
    B.ink()
    bv0 = B.get(k)
    sb = B.ev(OPEN, no)
    b2 = ln(0.50, 0.50, 0.70, 0.50, c='#2456A6')
    B.ev(DRAW, {'no': no, 'layer': None, 'strokes': [b2]})
    B.ink()
    A.ink()
    ma = mset(A.get(k))
    ok = sb.get('n', {}).get('2') == 1 and ma[('2', sig(a2))] == 1 and ma[('0', sig(a0))] == 1 and sum(n for (g, s), n in ma.items() if s == sig(b2)) == 1
    return ok, {'A 층': [sa.get('LAYER'), sa.get('keys')], '원격 무리': sorted((doc.get('g') or {}).keys()), 'B 받은 값 층': sorted(groups(bv0).keys()),
                'B 연 뒤': [sb.get('LAYER'), sb.get('n')], 'A 뒤': mset_show(ma)}


def t_I14e(W, A, B):
    """동기화 뒤 ↶ 가 마지막에 그은 획을 뺌 — B 가 획 다섯(그은 차례 ≠ id 차례)을 올림 → A 받음 → A ↶ → 마지막 획만 빠짐 · B 도 같은 차례"""
    no, k = P['I14e'], str(P['I14e'])
    A.ensure('phys')
    B.ensure('phys')
    cand = [ln(0.10, 0.10 + 0.06 * i, 0.35, 0.10 + 0.06 * i, c=['#16181B', '#B03A2E', '#2456A6', '#1B7F4B', '#7A3E9D'][i]) for i in range(5)]
    ids = B.ev("S=>inkEntries({0:S},'L').map(x=>x.id)", cand)
    order = sorted(range(5), key=lambda i: ids[i], reverse=True)   # 그은 차례 = id 큰 것부터(id 차례와 거꾸로)
    drawn = [cand[i] for i in order]
    for s in drawn:
        B.ev(DRAW, {'no': no, 'layer': 0, 'strokes': [s], 'wait': 350})
    B.ink()
    A.ink()
    av = A.get(k)
    ord_ok = [sig(x) for x in (av or {}).get('0', [])] == [sig(x) for x in drawn]
    A.ev(OPEN, no)
    A.ev("()=>{document.getElementById('tUndo').click();return 1}")
    A.wait(600)
    A.ink()
    B.ink()
    av2, bv2 = A.get(k), B.get(k)
    sa, sb = [sig(x) for x in (av2 or {}).get('0', [])], [sig(x) for x in (bv2 or {}).get('0', [])]
    want_ = [sig(x) for x in drawn[:4]]
    ok = ord_ok and sa == want_ and sb == want_
    return ok, {'A 받은 차례 = 그은 차례': ord_ok, 'A ↶ 뒤 = 앞 넷': sa == want_, 'B 같은 차례': sb == want_,
                'A 차례(색)': [s[0] for s in sa], '바람(색)': [s[0] for s in want_], 'id 차례 마지막 = 처음 그은 획': ids[order[0]] == max(ids)}


def t_I15w(W, br_wk, srv_wk):
    """webkit 폰(390 · 터치 문맥)에서 화면 펜으로 지학 카드에 긋기(합성 pen 포인터 — 앱이 펜만 받음) → 동기화 → 원격에 그 획"""
    Wd = Dev(br_wk, W, srv_wk, 'W', view='phone', eng='webkit', pdfs=set())
    try:
        Wd.goto('earth')
        no = Wd.ev("u=>uidNo(u)", EU['W'])
        c0 = Wd.ev(OPEN_CARD, no)
        Wd.ev("()=>{const b=document.querySelector('[data-pen]');if(b)b.click();try{qWire()}catch(e){}return TOOL.mode}")
        p0 = pick_pt(Wd, CARD_PT, [(0.20, 0.10), (0.20, 0.25), (0.50, 0.25), (0.30, 0.40)])
        p1 = Wd.ev(CARD_PT, [p0['u'] + 0.40, p0['v'] + 0.04])
        pts = [[p0['x'] + (p1['x'] - p0['x']) * i / 10, p0['y'] + (p1['y'] - p0['y']) * i / 10] for i in range(11)]
        hit = Wd.ev(WK_PEN, {'sel': '#card #qink', 'pts': pts})
        Wd.wait(500)
        c1 = Wd.ev("()=>__K.card()")
        mem = Wd.ev("()=>JSON.parse(JSON.stringify(QINK.s))")
        Wd.ink()
        st = Wd.st()
        crypto_ok = Wd.ev("()=>!!(window.crypto&&crypto.subtle)")
        doc = W.ink_doc('earth', 'qink:' + EU['W']) or {}
        alive = [r for g in (doc.get('g') or {}).values() for r in g.values() if 'e' in r]
        return {'열기': c0, '펜 맞음': hit, '그은 뒤 획': c1.get('n'), '획 점': [len(s.get('p', [])) // 2 for s in mem], '원격 산 획': len(alive),
                'crypto.subtle': crypto_ok, '칩': st.get('chip'), 'W 오류': Wd.errors(), 'mem': mem}
    finally:
        Wd.close()


# ════════════════════ 결함 후보 재기(§B 밖 · INFO) ════════════════════
CLOSE_VIA = r"""async a=>{const k=a.k,c0=INKST.cyc,d0=INKDIRTY.has(k);
  if(a.via==='btn')document.getElementById('vBack').click();else closeView();
  await __K.sleep(2500);await __K.idle();
  return {via:a.via,'닫기 전 더러움':d0,'고리 수':INKST.cyc-c0,'닫은 뒤 더러움':INKDIRTY.has(k),'창 닫힘':document.getElementById('view').classList.contains('hide')}}"""


def x_close_btn(W, A, B):
    """X0 — 문항 창 ✕(#vBack · 「닫기 (서재로)」) 로 닫을 때 필기 킥 — 감싸개(closeView)를 거치나 · 견줌 = closeView()(Esc 길)"""
    no, k = P['X0'], str(P['X0'])
    B.ensure('phys')
    s1, s2 = ln(0.12, 0.22, 0.40, 0.24, c='#2456A6'), ln(0.12, 0.32, 0.40, 0.34, c='#B03A2E')
    B.ev(OPEN, no)
    B.ev(DRAW, {'no': no, 'layer': 0, 'strokes': [s1]})
    bind = B.ev("()=>{const b=document.getElementById('vBack');return {onclick:b&&b.onclick?String(b.onclick).slice(0,60):null,'onclick===closeView':!!b&&b.onclick===closeView}}")
    r1 = B.ev(CLOSE_VIA, {'k': k, 'via': 'btn'})
    B.ev(OPEN, no)
    B.ev(DRAW, {'no': no, 'layer': 0, 'strokes': [s2]})
    r2 = B.ev(CLOSE_VIA, {'k': k, 'via': 'fn'})
    hit = bool(r1.get('닫기 전 더러움')) and r1.get('고리 수') == 0 and r1.get('닫은 뒤 더러움') is True and r2.get('고리 수', 0) >= 1 and r2.get('닫은 뒤 더러움') is False
    return hit, {'✕ 단추 onclick': bind, '✕ 로 닫음': r1, 'closeView() 로 닫음': r2}


def x_inflight(W, A, B):
    """X1 — 고리가 올리는 사이(PATCH 대기) 같은 열쇠에 그은 획 — 고리 끝에 더러움 표시가 지워지나 · 그 뒤 고리 · 다른 기기"""
    no, k = P['X1'], str(P['X1'])
    A.ensure('phys')
    B.ensure('phys')
    s1, s2 = ln(0.12, 0.40, 0.40, 0.42, c='#1B7F4B'), ln(0.12, 0.50, 0.40, 0.52, c='#7A3E9D')
    A.ev(DRAW, {'no': no, 'layer': 0, 'strokes': [s1]})
    W.hold = {'dev': 'A', 'kind': 'ref-patch'}
    A.ev("()=>{window.__bgx=__K.ink();return 1}")
    t = time.time()
    while not W.held and time.time() - t < 30:
        A.wait(50)
    held = len(W.held)
    A.ev(DRAW, {'no': no, 'layer': 0, 'strokes': [s2], 'wait': 700})   # 저장(300ms)이 붙잡힌 PATCH 동안 끝남
    mid = A.ev("k=>({dirty:INKDIRTY.has(k),busy:INKBUSY})", k)
    rel = W.release()
    W.hold = None
    A.ev("()=>window.__bgx")
    after = A.ev("k=>INKDIRTY.has(k)", k)
    A.ev("()=>__K.close()")
    A.wait(1500)
    A.ink()
    B.ink()
    doc = W.ink_doc('phys', k) or {}
    alive = [r['e'] for g in (doc.get('g') or {}).values() for i, r in g.items() if 'e' in r and r['t'] > (doc.get('x') or {}).get(i, 0)]
    ma, mb = mset(A.get(k)), mset(B.get(k))
    s2A, s2B = ma[('0', sig(s2))], mb[('0', sig(s2))]
    hit = held == 1 and mid.get('dirty') is True and after is False and s2A == 1 and s2B == 0
    return hit, {'붙잡음': held, '풂': rel, '그사이 그은 뒤(고리 도는 중)': mid, '고리 끝 뒤 더러움': after, '닫고 고리 한 번 더 뒤 원격 산 획': len(alive),
                 'A 로컬 s2': s2A, 'B s2': s2B, 'A': mset_show(ma), 'B': mset_show(mb)}


GATE_WRAP = r"""()=>{if(!window.__rmw){const m=recMerge,a=recAfterMerge;window.__rmw=[];
    recMerge=async function(){window.__rm0=performance.now();window.__inMerge=1;if(window.__gate)await window.__gate;return await m.apply(this,arguments)};
    recAfterMerge=async function(){try{return await a.apply(this,arguments)}finally{window.__inMerge=0;window.__rmw.push(Math.round(performance.now()-window.__rm0))}}}
  return 1}"""


def x_merge_addonly(W, A, B):
    """X2 — 기록 동기화 병합 중(UID_BUSY>0) 저장된 지움 — 더함만으로 들어가나 · 원격 · 다른 기기 · 다음 고리들(자연 창 길이 잼)"""
    no, k = P['X2'], str(P['X2'])
    A.ensure('phys')
    B.ensure('phys')
    s1, s2 = ln(0.10, 0.20, 0.35, 0.20), ln(0.10, 0.30, 0.35, 0.30, c='#B03A2E')
    A.ev(DRAW, {'no': no, 'layer': 0, 'strokes': [s1, s2]})
    A.ink()
    B.ink()
    A.ev(GATE_WRAP)
    for _ in range(3):
        A.rec()
    nat = A.ev("()=>window.__rmw.slice()")
    A.ev("()=>{window.__gate=new Promise(r=>window.__gateOpen=r);window.__bgr=__K.rec();return 1}")
    t = time.time()
    while not A.ev("()=>!!window.__inMerge&&UID_BUSY>0") and time.time() - t < 30:
        A.wait(50)
    er = A.ev(r"""async a=>{const [x,y]=toPix(a[0],a[1]);eraseAt(x,y);paintInk();saveInk();await __K.sleep(700);
      return {n:(INK[0]||[]).length,uid:UID_BUSY,add:INKADDONLY.has(a[2]),dirty:INKDIRTY.has(a[2])}}""", [0.225, 0.20, k])   # s1 의 넷째 점(지우개 반지름 7·scale px — 점 위를 누름)
    A.ev("()=>{window.__gateOpen();window.__gate=null;return 1}")
    A.ev("()=>window.__bgr")
    A.ev("()=>__K.idle()")
    id1 = A.ev("S=>inkEntries({0:S},'L')[0].id", [s1])
    steps = []

    def rs1():
        d = W.ink_doc('phys', k) or {}
        r = (d.get('g') or {}).get('0', {}).get(id1)
        if not r:
            return '없음'
        return ('산·글자' if 'e' in r else '산·글자 없음') if r['t'] > (d.get('x') or {}).get(id1, 0) else '지움'

    def snap(nm):
        steps.append([nm, {'원격 s1': rs1(), 'A s1': mset(A.get(k))[('0', sig(s1))], 'B s1': mset(B.get(k))[('0', sig(s1))]}])
    snap('① 병합 중 지움 → 그 고리(A · 기록 동기화 끝 inkKick)')
    B.ink()
    snap('② B 고리')
    A.ink()
    snap('③ A 고리')
    B.ink()
    snap('④ B 고리')
    hit = er.get('n') == 1 and bool(er.get('add')) and steps[0][1]['원격 s1'] != '지움'
    return hit, {'자연 병합 창 ms(기록 동기화 3 번 · recMerge 들어감 ~ recAfterMerge 끝)': nat, '지움 저장 때': er, '차례': steps}


# ════════════════════ 판 굴리기 ════════════════════
def app_src(x):
    if os.path.isfile(x):
        return open(x, 'rb').read().decode('utf-8')
    b = subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false', 'show', x + ':jagwa/index.html'], capture_output=True).stdout
    if not b:
        raise SystemExit('바탕 앱을 못 읽었다: ' + x)
    return b.decode('utf-8')


def patch_ink(src, a, b):
    """필기 동기화 덩이 안에서만 한 줄 바꿈(헛잣대 ㉡ · ㉢) — 바뀐 수가 1 이 아니면 None"""
    s = src.find('필기 동기화(jagwa/_task_jagwa_ink_sync.md')
    e = src.find('/* ═══ 필기 동기화 끝 ═══ */')
    if s < 0 or e < 0:
        return None, 0
    seg = src[s:e]
    n = seg.count(a)
    if n != 1:
        return None, n
    return src[:s] + seg.replace(a, b) + src[e:], 1


def run_test(tid, title, fn, *a, yard=None):
    """시험 하나 — 새 판이면 R · 헛잣대 판이면 Y · 예외 = FAIL(값에 예외)"""
    t = time.time()
    try:
        ok, val = fn(*a)
    except Exception as e:
        # 새 판 = FAIL · 헛잣대 판 = 「못 잼」(잣대가 가른 것이 아니므로 헛잣대 칸 FAIL 이 되게 ok=True 로 넘김)
        ok, val = (True if yard else False), {'예외(못 잼)': str(e).split('\n')[0][:300], '자리': traceback.format_exc().strip().split('\n')[-3:]}
    val = dict(val) if isinstance(val, dict) else {'값': val}
    val['초'] = round(time.time() - t, 1)
    SECS[(yard or 'new') + ' ' + tid] = val['초']
    if yard:
        return Y(tid, yard, title, ok, val)
    return R(tid, title, ok, val)


SECS = {}
PROBES = {}
TITLES = {
    'I1': '옛 필기 올라감 — A 물리 3(층 0·1) + 지학 카드 · 교재 쪽 · 서브노트 → 원격 파일 6 · B 같은 획 수 · 좌표 차 ≤ 1/10000 · 차례',
    'I2': '둘 다 옛 필기 — 같은 문항 서로 다른 획 + 겹친 획 하나 + 같은 자리 점 획 둘 → 양쪽 합집합 · 겹친 획 한 번 · 점 획 둘 다',
    'I3': '지움 건너감 — B 지우개 한 획 · 「지금 회독 지우기」 → A 에서 그 획들 없음 · 나머지 그대로(물리 · 화면 펜)',
    'I4': '↶ 건너감 — B 긋고 동기화 → ↶ → 동기화 → A 에서 그 획 없음',
    'I5': '빈 층이 안 덮음 — B 가 열기만 해 빈 2 회독 층이 메모리에 섬 → 동기화 → A 의 2 회독 획 그대로',
    'I6': '동시 · 겹침 — 같은 문항 다른 층 · 같은 층 각자 획 → 둘 다 남음 · 기록 PUT 과 ref 다툼 → 422 다시 한 번',
    'I7': '글자 왕복 — 손필기 획 글자 → 소수 → 글자 = 같은 글자 · 다시 동기화 커밋 0',
    'I9': '옛 판과 섞임 — 바탕 기기 기록 PUT 뒤 phys/ink 그대로 · 새 판 필기 안 잃음 · 기록.json 열쇠 · 값 무변',
    'I10': '열린 창 다시 그림 — A 가 연 채 B 획 → A 화면 획 수 늘어남 · 층 · 가림 그대로 → A 한 획 더 → B 획 그대로',
    'I11': '첫 동기화 나눠 올림 — 150 열쇠 → 60 · 60 · 30 · 고리당 커밋 1 · 칩 90 → 30 → 사라짐 · 403 이면 그 고리 멈춤 · 다음 고리 이어감',
    'I12': '시계 어긋남 — D(+1 시간) 첫 동기화 뒤 A 가 지운 획 A · D 다 없음 · D 새 획 A 에 보임',
    'I13': '동기화 밖 열쇠 — 맨 uid · 옮기지 못한 번호 · diag: · ink_orphan: · 순배열 · 다른 글자 → 원격 0 · 들이기 중 syncInk 안 돎',
    'I14a': '획 긋고 300ms 안에 동기화 → 그 획 안 잃음(다음 고리에 올라감)',
    'I14b': '교재 쪽 캐시 산 채 원격 갱신 → 한 획 더 → 다른 기기 획 남음',
    'I14c': '옛 백업 들이기 → 다른 기기의 새 획 남음(원격 · 들인 기기 다음 고리 포함)',
    'I14d': '1 층이 빈 물리 문항 · 기록 2 개인 다른 기기가 열기 → 2 층 획 남음',
    'I14e': '동기화 뒤 ↶ 가 마지막에 그은 획을 뺌',
    'I15-물리': '물리 폰 390(A) ↔ PC 1100(B) — I1 물리 몫 · I3',
    'I15-지학': '지학 폰 390(A) ↔ PC 1100(B) — I1 지학 몫(카드 · 교재 · 서브노트) · I3 카드(화면 펜 지우개 · 지금 회독 지우기)',
    'I15-생물': '생물 폰 390(A) ↔ PC 1100(B) — I1(카드 · 교재) · I3 카드',
    'I15-webkit': 'webkit 폰 한 번 — 화면 펜(합성 pen 포인터)으로 긋기 → 동기화 → 다른 기기(Chromium PC)에 같은 획',
}
XTITLES = {
    'X0': '문항 창 ✕(#vBack)로 닫으면 필기 킥이 안 도나(✕ 의 onclick = 감싸기 전 closeView) · 견줌 closeView()',
    'X1': '고리가 올리는 사이(PATCH 대기) 같은 열쇠에 그은 획 — 고리 끝에 더러움 표시가 지워져 안 올라가나',
    'X2': '기록 동기화 병합 중(UID_BUSY>0)에 저장된 지움 — 더함만으로 들어가 원격에 산 채(글자 없음) 올라가나',
}


def main():
    new_src = open(NEWF, 'rb').read().decode('utf-8')
    base_src = app_src(BASE)
    mem_src, n_mem = patch_ink(new_src, 'if(mem){', 'if(false){')
    ord_src, n_ord = patch_ink(new_src, '.sort((a,b)=>(G[a].o-G[b].o)||(a<b?-1:a>b?1:0))', '.sort()')
    for rel in VEND_FILES:
        vendor_file(rel)
    md5 = lambda s: hashlib.md5(s.replace('\r\n', '\n').encode('utf-8')).hexdigest()[:8]
    INFO('I0', '판 · 자리', {'NEW': NEWF, 'NEW md5(LF)': md5(new_src), '동기화 덩이': 'syncInk' in new_src and 'inkCycle' in new_src,
                            'BASE': BASE, 'BASE md5(LF)': md5(base_src), 'BASE 에 syncInk': 'function syncInk' in base_src,
                            '㉡ 바꿈': n_mem, '㉢ 바꿈': n_ord, 'SPD': SPD, '재료': MAT_SRC, 'vendor': VENDOR, '받은 vendor': VEND_GOT,
                            '자료 전제(지난 회독 수)': {'읽음': {s: HC[s] is not None for s in HC}, '갈아 끼움': P_REMAP, '어긋남(그 칸 FAIL 은 자료 탓일 수 있음)': P_BAD}})
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        wk_res = None
        WW = World('WW')
        if WEBKIT and want('I15-webkit'):
            srv_w = AppServer({'/app.html': new_src})
            try:
                brw = pw.webkit.launch()
                try:
                    wk_res = t_I15w(WW, brw, srv_w)
                except Exception as e:
                    wk_res = {'예외': str(e).split('\n')[0][:300], '자리': traceback.format_exc().strip().split('\n')[-3:]}
                finally:
                    brw.close()
            finally:
                srv_w.close()
        br = pw.chromium.launch(args=['--no-sandbox'])
        try:
            if wk_res is not None:
                srv_v = AppServer({'/app.html': new_src})
                V = Dev(br, WW, srv_v, 'V', view='pc', pdfs=set())
                try:
                    t = time.time()
                    mem = wk_res.pop('mem', None) if isinstance(wk_res, dict) else None
                    V.goto('earth')
                    vv = V.get('qink:' + EU['W'])
                    ok, d = (cmp_val({'s': mem}, vv) if mem else (False, '그은 획 없음'))
                    pts_ok = bool(mem) and all(len(s.get('p', [])) >= 4 for s in mem)
                    wk_res.update({'V(Chromium PC) 받은 값 대조': d, '여러 점': pts_ok, '초': round(time.time() - t, 1)})
                    R('I15-webkit', TITLES['I15-webkit'], ok and pts_ok and wk_res.get('원격 산 획') == 1 and len(mem or []) == 1, wk_res)
                finally:
                    V.close()
                    srv_v.close()
            # ── 새 판 ──
            main_ids = [x for x in TITLES if x != 'I15-webkit'] + ['I8'] + (list(XTITLES) if PROBE else [])
            if any(want(x) for x in main_ids):
                W1 = World('W1')
                srv = AppServer({'/app.html': new_src, '/base.html': base_src})
                A = Dev(br, W1, srv, 'A', view='phone', pdfs=set(PDF_NEED))
                B = Dev(br, W1, srv, 'B', view='pc', pdfs=set(PDF_NEED))
                E = None
                try:
                    t = time.time()
                    r = boot(W1, A, B, bio=True)
                    SECS['new boot'] = round(time.time() - t, 1)
                    INFO('I1', '첫 시동 요청 수(길마다 · 기기마다)', r['req'])
                    ok1, v1, okp1, oke1 = judge_I1(r)
                    v1['초(시동 묶음)'] = SECS['new boot']
                    R('I1', TITLES['I1'], ok1, v1)
                    ok2, v2 = judge_I2(r)
                    R('I2', TITLES['I2'], ok2, v2)
                    okb1, vb1 = judge_bio1(r)
                    res15 = {'물리': {'I1': okp1}, '지학': {'I1': oke1}, '생물': {'I1': okb1}}
                    if want('I15-생물'):
                        R('I15-생물', TITLES['I15-생물'] + ' — I1(카드 · 교재)', okb1, vb1)
                        res15['생물']['I3'] = run_test('I15-생물', TITLES['I15-생물'] + ' — I3 카드(화면 펜 지우개 · 지금 회독 지우기)', t_card3, W1, A, B, 'bio', BU['I1'])
                    if want('I15-지학'):
                        res15['지학']['I3'] = run_test('I15-지학', TITLES['I15-지학'] + ' — I3 카드', t_card3, W1, A, B, 'earth', EU['I1'])
                    if want('I14b'):
                        run_test('I14b', TITLES['I14b'], t_I14b, W1, A, B)
                    if want('I13'):
                        run_test('I13', TITLES['I13'], t_I13, W1, A, B)
                    if want('I3') or want('I15-물리'):
                        res15['물리']['I3'] = run_test('I3', TITLES['I3'], t_I3, W1, A, B)
                    for tid, fn in (('I4', t_I4), ('I5', t_I5), ('I6', t_I6), ('I7', t_I7), ('I10', t_I10), ('I14a', t_I14a), ('I14d', t_I14d), ('I14e', t_I14e)):
                        if want(tid):
                            run_test(tid, TITLES[tid], fn, W1, A, B)
                    if want('I8'):
                        t = time.time()
                        try:
                            v8 = t_I8(W1, A, B)
                        except Exception as e:
                            v8 = {'예외': str(e).split('\n')[0][:300], '자리': traceback.format_exc().strip().split('\n')[-3:]}
                        v8['초'] = round(time.time() - t, 1)
                        INFO('I8', '크기(FAIL 아님 · 넘으면 보고) — 점당 B ≤ 6 · 표본 파일 ≤ 80KB · 그렸다 다 지우기 10 번 뒤 ≤ 1.2 배', v8)
                    if want('I9'):
                        run_test('I9', TITLES['I9'], t_I9, W1, A, B, br, srv)
                    if want('I11') or want('I14c'):
                        t = time.time()
                        try:
                            ok11, v11, E = t_I11(W1, br, srv)
                        except Exception as e:
                            ok11, v11 = False, {'예외': str(e).split('\n')[0][:300], '자리': traceback.format_exc().strip().split('\n')[-3:]}
                        v11['초'] = round(time.time() - t, 1)
                        SECS['new I11'] = v11['초']
                        if want('I11'):
                            R('I11', TITLES['I11'], ok11, v11)
                    if want('I12'):
                        run_test('I12', TITLES['I12'], t_I12, W1, A, br, srv)
                    if want('I14c'):
                        run_test('I14c', TITLES['I14c'], t_I14c, W1, A, B, E)
                    for subj in ('물리', '지학', '생물'):
                        if want('I15-' + subj) and 'I3' in res15[subj]:
                            R('I15-' + subj, TITLES['I15-' + subj] + ' — 묶음', all(res15[subj].values()), res15[subj])
                    if PROBE:
                        for xid, fn in (('X0', x_close_btn), ('X1', x_inflight), ('X2', x_merge_addonly)):
                            if not want(xid):
                                continue
                            t = time.time()
                            try:
                                hit, v = fn(W1, A, B)
                            except Exception as e:
                                hit, v = None, {'예외(못 잼)': str(e).split('\n')[0][:300], '자리': traceback.format_exc().strip().split('\n')[-3:]}
                            v['초'] = round(time.time() - t, 1)
                            SECS['probe ' + xid] = v['초']
                            PROBES[xid] = {True: '재현됨', False: '재현 안 됨', None: '못 잼'}[hit]
                            INFO(xid, '결함 후보 · %s — %s' % (XTITLES[xid], {True: '재현됨', False: '재현 안 됨', None: '못 잼'}[hit]), v)
                    INFO('I0', '새 판 요청 합계(기기 · 길 · 상태)', W1.delta({}))
                    INFO('I0', '기기 메모', {d.name: {'시동': d.boots, '메모': d.notes[:4], '페이지 오류': d.errs[:3]} for d in (A, B) + ((E,) if E else ())})
                finally:
                    for d in (A, B, E):
                        if d:
                            d.close()
                    srv.close()
            # ── 헛잣대 ──
            for yd in YARD:
                src = {'base': base_src, 'mem': mem_src, 'ord': ord_src}[yd]
                tests = [x for x in {'base': ['I1', 'I2', 'I3'], 'mem': ['I10', 'I14b'], 'ord': ['I14e']}[yd] if want(x)]
                if not tests:
                    continue
                if src is None:
                    for tid in tests:
                        Y(tid, yd, '헛잣대 판을 못 지음(바꿀 줄 수 ≠ 1)', True, {})
                    continue
                Wy = World('Y' + yd)
                srv_y = AppServer({'/app.html': src})
                A2 = Dev(br, Wy, srv_y, 'A', view='phone', pdfs=set(PDF_NEED) if yd == 'base' else set())
                B2 = Dev(br, Wy, srv_y, 'B', view='pc', pdfs=set(PDF_NEED) if yd == 'base' else set())
                try:
                    if yd == 'base':
                        t = time.time()
                        try:
                            r = boot(Wy, A2, B2, bio=False)
                            ok1, v1 = judge_I1(r)[:2]
                            ok2, v2 = judge_I2(r)
                        except Exception as e:
                            # 시동 묶음이 깨지면 잣대가 가른 것이 아니다 — 헛잣대 칸은 FAIL(못 잼)로 남긴다
                            ok1 = ok2 = True
                            v1 = v2 = {'예외(못 잼)': str(e).split('\n')[0][:300], '자리': traceback.format_exc().strip().split('\n')[-3:]}
                        SECS['base boot'] = round(time.time() - t, 1)
                        if 'I1' in tests:
                            Y('I1', yd, TITLES['I1'], ok1, v1)
                        if 'I2' in tests:
                            Y('I2', yd, TITLES['I2'], ok2, v2)
                        if 'I3' in tests:
                            run_test('I3', TITLES['I3'], t_I3, Wy, A2, B2, yard=yd)
                    else:
                        for tid in tests:
                            run_test(tid, TITLES[tid], {'I10': t_I10, 'I14b': t_I14b, 'I14e': t_I14e}[tid], Wy, A2, B2, yard=yd)
                finally:
                    A2.close()
                    B2.close()
                    srv_y.close()
        finally:
            br.close()
    # ── 합계 ──
    new = [r for r in RES if not r['id'].endswith('-헛')]
    yd = [r for r in RES if r['id'].endswith('-헛')]
    per = {}
    for r in yd:
        p = per.setdefault(YNAME[r['yard']], {'칸': 0, '잣대 FAIL(헛 PASS)': 0})
        p['칸'] += 1
        p['잣대 FAIL(헛 PASS)'] += r['st'] == 'PASS'
    INFO('합계', '새 판 PASS %d / %d · 헛잣대 PASS %d / %d' % (sum(r['st'] == 'PASS' for r in new), len(new), sum(r['st'] == 'PASS' for r in yd), len(yd)),
         {'새 판 FAIL': [r['id'] for r in new if r['st'] == 'FAIL'], '헛잣대': per, '헛잣대 FAIL(못 가름)': [r['id'] for r in yd if r['st'] == 'FAIL'],
          '결함 후보(X · §B 밖)': PROBES, '초': round(time.time() - T0), '칸마다 초': SECS})


if __name__ == '__main__':
    try:
        main()
    finally:
        try:
            _OF.close()
        except Exception:
            pass
