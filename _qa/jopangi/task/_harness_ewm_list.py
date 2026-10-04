# -*- coding: utf-8 -*-
r"""_task_ewm_list §B 관문 — 시험 틀림 수 「61x1 63x2」(조판기 · 민법OX 서랍 · 첫 화면 단원·장·회차 줄) + 1:1 자리 「63-13-X」(검색 · 기출뷰 문항 머리 · 연결 목록)

  python _harness_ewm_list.py [--jo <앱 | genie 판>] [--mb <앱 | genie 판>] [--base 67e423e] [--apps jo,mb] [--only B1,B2,..]
        [--tw <Tailwind CSS 사본>] [--res <결과 파일>] [--shots <그림 폴더>]

  NEW  = genie 작업트리 jo/index.html · minbeop/index.html(고친 판) · BASE = 바탕 main 67e423e — 두 판을 같은 기기 · 같은 차례로 늘 같이 돌려
         헛잣대(바탕 FAIL 이어야 하는 칸)와 무변 칸(바탕과 같은 값)을 한 번에 센다 · 바탕을 못 읽으면 바탕 칸은 「안 잼」
  시험 기록 = 하네스가 실행 중에 지어냄(exam_rec · 값 지어냄 · 저장소에 파일로 안 둠) — 가짜 원격이 studyplandata exam/꼬까.json 자리에 준다
    ⚠ 진짜 기록(SPD exam/꼬까.json · minbeop/기록.json · claude.json)은 열지 않는다 — 가짜 원격은 그 자리를 지어낸 기록 · 메모리(새 기기) · 404 로만 대답한다
    61회 · 63회(cha 1 · mode q) 특허 · 상표 · 디보 · 민법 틀린 줄 + ok true 줄 · 화학 줄 · 지운 회차(62) · 2차(63) · 점수만(61) 을 섞음
  데이터 = 조판기 genie jo/data(읽기만) · 민법 SPD minbeop/문항마스터 · 문항메타 · 기출키(읽기만 · 쪽 안에서만 · 결과엔 수 · 열쇠만)
  기대값 = 하네스가 따로 셈(앱 ewmMap · ewmIdx · ewmCountTxt 안 씀) —
    조판기: 지어낸 기록 (회, 번) → 리담 문제 지문 열쇠(VJ.qs 연도 · 시험문번) + 책 · 문항째 카드(시험문번 · 연도 / uid) → 줄 열쇠(서랍 · 첫 화면 줄 규칙
            mgKeys · mlnKeys · uzSub · uzUnkKeys — 줄 이름으로 찾음)마다 (회, 번) 중복 없이 → 「<회>x<수>」 · 줄 열쇠 수 = 그 줄에 적힌 수(맞춤 확인)
    민법:   문항마스터 출제연도 · 회차 · 문번(파이썬) → Q-id → 줄(서랍 = trScan idsF · 첫 화면 = chapUidsOf)마다 같은 셈
  관문:
    B1 표시 수 — 조판기 세 법 · 민법 서랍 · 첫 화면 단원 · 장 줄마다 .ewmn 글 = 하네스 셈 · 틀린 것 없는 줄 = 글 0 · 편 카드 머리 · 해 머리 = 0 ·
       ok true · 화학 · 지운 회차 · 2차 · 점수만 = 0(그 줄이 걸린 줄은 뺀 값) · 같은 줄에 같은 문제 지문 여럿 = 한 번 · 앱 표(ewmMap · ewmIdx) = 하네스 표
    B2 회차 줄 — J2 · J4 · M2 · M4 = 그 회 틀린 문제 수(법별) · 단원 줄과 같은 문제 집합 맞댐(걸친 문제 · 단원에 없는 문제 목록)
    B3 1:1 자리 — J5 검색 · J6 기출뷰 문항 머리 · J7 연결 목록 · 같은 판례 목록 · M5 검색 · M6 기출뷰 문항 머리에 「<회>-<번>-X」 ·
       J5 · M5 누르면 펼침 한 줄(내 답 · 정답 · 평균 정답률) · 다시 누르면 접힘 · 줄 누름 안 샘 · J7 누름 없음(줄 누름 = 지문 팝업 = 바탕과 같은 창)
    B4 늦게 받기 — 기록 응답 2 초 늦춤 → 첫 화면이 먼저 · 받은 뒤 서랍 · 첫 화면에 나타남(값 = B1 셈) · 스크롤 자리 그대로 ·
       민법 renderDashboard 부름 0 · 첫 화면 마디 그대로(통째 다시 그리기 0)
    B5 꼴 — .ewmn 계산값 10.5px · 700 · rgb(220, 38, 38) · 바탕 투명 · 테두리 0 · nowrap · margin-left 4px · 소문자 x ·
       줄 높이 = 바탕 ±1px(1440 · 834 · 390) · 390 가로 넘침 0 · 줄 누름 = 바탕과 같은 일(누름 가로챔 0)
    B6 안 넣는 자리 — OMR 판 · 회독 비교 · 히트맵에 .ewmn 0 · 「-X」 수 = 바탕
    B7 훑기(규칙 60) — 두 앱 첫 화면 · 서랍 · 검색 · 기출뷰 × 1440 · 834 · 390 그림 · .ewmn · 「-X」 겹침 · 잘림 · 가려짐 · 화면 밖 0 · 가로 넘침
    B0 새 판 페이지 오류 0
  엔진 = Chromium(터치 칸 아님 · 834 · 390 = 모바일 뷰포트 + 마우스 누름) · 클라우드 = cdn 막힘 → --tw(민법 Tailwind v3 로 미리 구운 CSS)
  결과 = 화면 PASS/FAIL 줄 · --res(기본 = 임시 폴더 · _qa 에 결과를 쓰지 않는다) · 그림 = --shots(기본 = 임시 폴더)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import base64, hashlib, json, os, re, subprocess, sys, tempfile, threading, time, traceback, urllib.parse   # noqa: E402
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


BASE = ARG('--base', '67e423e')   # genie main 67e423e = 이 판의 바탕(두 앱 파일 = 4754b1d)
APPS = [x for x in (ARG('--apps', 'jo,mb') or '').split(',') if x]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
TWCSS = ARG('--tw')
TMPD = os.path.join(tempfile.gettempdir(), 'h_ewm_list')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_ewm_list_result.txt'))
SHOTS = ARG('--shots', os.path.join(TMPD, 'shots'))
JODATA = _roots.genie('jo', 'data')
SPD = _roots.spd()
REL = {'jo': 'jo/index.html', 'mb': 'minbeop/index.html'}
NEWA = {'jo': ARG('--jo', _roots.genie('jo', 'index.html')), 'mb': ARG('--mb', _roots.genie('minbeop', 'index.html'))}
NAME = {'jo': '조판기', 'mb': '민법OX'}
IPAD_UA = 'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
IPHONE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
DEV = {1440: dict(W=1440, H=900, mob=False), 834: dict(W=834, H=1194, mob=True, ua=IPAD_UA), 390: dict(W=390, H=844, mob=True, ua=IPHONE_UA)}
WIDTHS = (1440, 834, 390)
DELAY = 2000   # B4 — 기록 응답 늦춤(ms)

RES = []    # (묶음, 이름, 새 판 판정 True/False/None(INFO), 값)
YARD = []   # (묶음, 이름, 바탕 판정) — 같은 잣대를 바탕 값에(헛잣대 칸만 · 다 FAIL 이어야 함)
ERRS = {}   # 판 → 페이지 오류
STEP = []   # (단계, 초)
T0 = time.time()


def _s(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


def T(g, name, ok, detail=''):
    RES.append((g, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', g, name, _s(detail)[:900]), flush=True)
    return bool(ok)


def N(g, name, detail=''):
    RES.append((g, name, None, detail))
    print('INFO | %s · %s | %s' % (g, name, _s(detail)[:1400]), flush=True)


def TB(g, name, ok_fn, vn, vb, yard=True, show=None):
    """새 판 판정 · 같은 잣대로 바탕 판정(yard = 헛잣대 칸이면 YARD 에) · show = 찍을 꼴(판정은 원값)"""
    try:
        okn = bool(ok_fn(vn))
    except Exception:
        okn = False
    sh = show or (lambda x: x)
    T(g, name, okn, {'new': sh(vn), 'base': sh(vb) if vb is not None else None})
    if vb is not None and yard:
        try:
            okb = bool(ok_fn(vb))
        except Exception:
            okb = False
        YARD.append((g, name, okb))
    return okn


def want(k):
    return not ONLY or k in ONLY


def git(*a):
    return subprocess.run(['git', '-C', _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def app_src(app, x):
    if os.path.isfile(x):
        return open(x, 'rb').read().decode('utf-8')
    b = git('show', x + ':' + REL[app])
    return b.decode('utf-8') if b else None


def md5lf(s):
    return hashlib.md5(s.replace('\r\n', '\n').encode('utf-8')).hexdigest()


# ════════════════════════ 시험 기록 — 하네스가 실행 중에 지어냄(값 지어냄 · 파일 안 둠) ════════════════════════
def exam_rec():
    def q(s, i, ok=False, my='1', ans='2', rate=48.5):
        return {'s': s, 'i': i, 'ok': ok, 'my': my, 'ans': ans, 'rate': rate}
    return {'v': 1, 'who': '꼬까(하네스가 지어낸 기록 · 진짜 아님)', 'items': [
        {'id': '61', 'no': 61, 'cha': 1, 'mode': 'q', 'q': [
            q('특허', 3), q('특허', 7, my='4', ans='5', rate=33.3), q('특허', 4, ok=True, my='2', ans='2'),
            q('상표', 22), q('상표', 25, my='3', ans='1'), q('디보', 33), q('민법', 5), q('민법', 12, my='3', ans='1', rate=40.0), q('화학', 3)]},
        {'id': '63', 'no': 63, 'cha': 1, 'mode': 'q', 'q': [
            q('특허', 5), q('특허', 13, my='2', ans='4', rate=61.2), q('특허', 6), q('상표', 24), q('디보', 35), q('디보', 38),
            q('민법', 13, my='5', ans='2', rate=57.0), q('민법', 20), q('민법', 21, ok=True, my='1', ans='1'), q('화학', 13)]},
        {'id': '62', 'no': 62, 'cha': 1, 'mode': 'q', 'del': True, 'q': [q('특허', 1), q('상표', 21), q('민법', 1)]},
        {'id': '63-2', 'no': 63, 'cha': 2, 'mode': 'q', 'q': [q('특허', 2), q('민법', 2)]},
        {'id': '61-s', 'no': 61, 'cha': 1, 'mode': 'score', 'q': [q('특허', 8), q('민법', 8)]},
    ]}


EXJ = exam_rec()
EXB = json.dumps(EXJ, ensure_ascii=False).encode('utf-8')


def ex_rows(j):
    """틀림 줄(cha 1 · mode q · del 아님 · ok === false · 화학 뺌) · 뺀 줄(까닭) — 앱과 따로 하네스가 거른다"""
    keep, drop = [], []
    for it in (j or {}).get('items') or []:
        m = re.match(r'\d+', str(it.get('id') or ''))
        r = int(it.get('no') or 0) or (int(m.group(0)) if m else 0)
        why = '2차' if it.get('cha') != 1 else ('점수만' if it.get('mode') != 'q' else ('지운 회차' if it.get('del') else ''))
        for x in it.get('q') or []:
            w = why or ('맞힘' if x.get('ok') is not False else ('화학' if str(x.get('s')) == '화학' else ''))
            row = {'r': r, 's': str(x.get('s')), 'i': int(x.get('i'))}
            if w:
                row['why'] = w
                drop.append(row)
            else:
                keep.append(row)
    return keep, drop


WR, WX = ex_rows(EXJ)
LAWS = ('특허법', '상표법', '디자인보호법')
LAWN = {'특허': '특허법', '상표': '상표법', '디보': '디자인보호법'}


def wr_of(law):
    return [[x['r'], x['i']] for x in WR if LAWN.get(x['s'], x['s']) == law]


def wx_of(law):
    return [[x['r'], x['i']] for x in WX if LAWN.get(x['s'], x['s']) == law]


def round_exp(pairs):
    """{해: '<회>x<수>'} — 그 회 틀린 문제(번 중복 없이)"""
    by = {}
    for r, i in pairs:
        by.setdefault(r, set()).add(i)
    return {str(r + 1963): '%dx%d' % (r, len(v)) for r, v in by.items() if v}


# ════════════════════════ 민법 — 문항마스터(파이썬) → Q-id 별 (회|번) ════════════════════════
_MB = {}


def mb_master():
    if 'b' not in _MB:
        _MB['b'] = open(os.path.join(SPD, 'minbeop', '문항마스터.json'), 'rb').read()
    return _MB['b']


def mb_meta(r):
    """앱 buildQuizData 의 examMeta 꼴 — (해, 회, 번)"""
    yr = str(r.get('기출연도') or '').strip()
    if not yr:
        return []
    multi = str(r.get('출제연도') or '').strip()
    out = []
    for tok in ([t for t in re.split(r'[,\s]+', multi) if t] if multi else [yr]):
        y, no, opt = (tok.split(':') + ['', ''])[:3]
        rd = str(r.get('회차') or '').strip() if y == yr else str(int(y) - 1963)
        n = (int(no) if re.fullmatch(r'\d+', no or '') else 0) if no else (int(r.get('문번') or 0) if y == yr else 0)
        out.append((y, int(rd or 0) or (int(y) - 1963), n))
    return out


def mb_maps():
    rows = [r for r in json.loads(mb_master().decode('utf-8'))['rows'] if r.get('uid') and r.get('문제')]
    wr = {(r, i) for r, i in wr_of('민법')}
    wx = wr | {(r, i) for r, i in wx_of('민법')}
    QM, QMX = {}, {}
    for r in rows:
        for y, rd, n in mb_meta(r):
            p = '%d|%d' % (rd, n)
            if (rd, n) in wr and p not in QM.setdefault(r['uid'], []):
                QM[r['uid']].append(p)
            if (rd, n) in wx and p not in QMX.setdefault(r['uid'], []):
                QMX[r['uid']].append(p)
    return {k: v for k, v in QM.items() if v}, {k: v for k, v in QMX.items() if v}


# ════════════════════════ 가짜 원격 · 서버 ════════════════════════
class Remote:
    """exam/꼬까.json = 지어낸 기록 · minbeop 문항 셋 = SPD(읽기만) · 그 밖 = 메모리(새 기기 · PUT 받아 둠) 또는 404"""
    RO = ('minbeop/문항마스터.json', 'minbeop/문항메타.json', 'minbeop/기출키.json')

    def __init__(self):
        self.files, self.puts, self.lock = {}, [], threading.Lock()

    def get(self, repo, path):
        if repo.endswith('/studyplandata') and path == 'exam/꼬까.json':
            return EXB
        with self.lock:
            if repo + ':' + path in self.files:
                return self.files[repo + ':' + path]
        if repo.endswith('/studyplandata') and path in self.RO:
            if path == 'minbeop/문항마스터.json':
                return mb_master()
            f = os.path.join(SPD, *path.split('/'))
            return open(f, 'rb').read() if os.path.isfile(f) else None
        return None

    def put(self, repo, path, body):
        with self.lock:
            self.files[repo + ':' + path] = body
            self.puts.append((repo + ':' + path, len(body)))
        return hashlib.sha1(body).hexdigest()


def route_handler(remote):
    def h(route):
        req = route.request
        u = req.url
        if u.startswith('http://127.0.0.1'):
            return route.continue_()
        m = re.match(r'https://api\.github\.com/repos/([^/]+/[^/]+)/contents/([^?]+)', u)
        if m:
            repo, path = m.group(1), urllib.parse.unquote(m.group(2))
            if req.method == 'PUT':
                try:
                    data = base64.b64decode(json.loads(req.post_data or '{}').get('content', ''))
                except Exception:
                    return route.fulfill(status=422, body='{}', content_type='application/json')
                sha = remote.put(repo, path, data)
                return route.fulfill(status=200, body=json.dumps({'content': {'sha': sha}}), content_type='application/json')
            b = remote.get(repo, path)
            if b is None:
                return route.fulfill(status=404, body='{"message":"Not Found"}', content_type='application/json')
            if 'raw' in ((req.headers or {}).get('accept', '')):
                return route.fulfill(status=200, body=b, content_type='application/octet-stream')
            return route.fulfill(status=200, body=json.dumps({'sha': hashlib.sha1(b).hexdigest(), 'size': len(b)}), content_type='application/json')
        if u.startswith('https://api.github.com'):
            return route.fulfill(status=404, body='{"message":"Not Found"}', content_type='application/json')
        if u.startswith('https://cdn.tailwindcss.com') and not TWCSS:
            return route.continue_()   # 본 PC = 진짜 Tailwind cdn · 클라우드 = --tw 사본을 글에 넣었다
        return route.abort()
    return h


TW_TAG = '<script src="https://cdn.tailwindcss.com"></script>'


def mb_html(src):
    if TWCSS and TW_TAG in src:
        return src.replace(TW_TAG, '<style>/* harness: Tailwind v3 사본(--tw) */\n' + open(TWCSS, encoding='utf-8').read() + '\n</style>', 1)
    return src


SERVERS = {}


def serve(app, tag, src):
    if (app, tag) in SERVERS:
        return SERVERS[(app, tag)][1]
    body = (mb_html(src) if app == 'mb' else src).encode('utf-8')
    top = '/jo/' if app == 'jo' else '/minbeop/'

    class Hd(SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, data, ct='application/json'):
            self.send_response(code)
            self.send_header('Content-Type', ct)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            p = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
            if p in (top, top + 'index.html'):
                return self._send(200, body, 'text/html; charset=utf-8')
            if app == 'jo' and p.startswith('/jo/data/'):
                f = os.path.join(JODATA, *[x for x in p[len('/jo/data/'):].split('/') if x])
                if os.path.isfile(f):
                    return super().do_GET()
            return self._send(404, b'{"message":"Not Found"}')

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
            if p.startswith('/jo/data/'):
                return os.path.join(JODATA, *[x for x in p[len('/jo/data/'):].split('/') if x])
            return os.path.join(HERE, '__없음__')

    srv = ThreadingHTTPServer(('127.0.0.1', 0), Hd)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[(app, tag)] = (srv, srv.server_address[1])
    return srv.server_address[1]


# ════════════════════════ 쪽 도구 ════════════════════════
# 처음 스크립트(앱보다 먼저) — 기록 응답 늦춤 · 시각 · 오류 · 토큰(tt.cfg) · 막는 창
PROBE = r"""(function(){ if (window.__EH) return; var D = __D__, READY = __R__;
 var H = window.__EH = { tReady: 0, tReq: 0, tEx: 0, nEx: 0, errs: [] };
 window.addEventListener('error', function(e){ H.errs.push(String(e.message || '').slice(0, 200) + ' @' + (e.lineno || '')); });
 window.addEventListener('unhandledrejection', function(e){ H.errs.push('reject: ' + String((e.reason && e.reason.message) || e.reason).slice(0, 200)); });
 var of = window.fetch;
 window.fetch = function(u, o){ var s = String((u && u.url) || u), d = s; try { d = decodeURIComponent(s); } catch (e) {}
   if (/exam\/꼬까\.json/.test(d)){ H.nEx++; if (!H.tReq) H.tReq = performance.now();
     var go = function(){ return of.call(window, u, o).then(function(r){ H.tEx = performance.now(); return r; }, function(e){ H.tEx = performance.now(); throw e; }); };
     return D ? new Promise(function(res){ setTimeout(res, D); }).then(go) : go(); }
   return of.apply(window, arguments); };
 var iv = setInterval(function(){ try { if (!H.tReady && READY()){ H.tReady = performance.now(); clearInterval(iv); } } catch (e) {} }, 20);
 window.alert = function(){}; window.confirm = function(){ return true; }; window.prompt = function(){ return null; };
 try { if (!sessionStorage.getItem('__h')){ sessionStorage.setItem('__h', '1'); localStorage.clear(); localStorage.setItem('tt.cfg', __CFG__); } } catch (e) {}
 try { if (navigator.serviceWorker) navigator.serviceWorker.register = function(){ return Promise.reject(new Error('sw blocked')); }; } catch (e) {}
})();"""
READY = {'jo': "function(){ var s = document.querySelector('#slot'); return typeof render === 'function' && !!s && s.children.length > 0; }",
         'mb': "function(){ return typeof quizData !== 'undefined' && quizData.length > 0 && !!document.querySelector('#dashboard-container > *'); }"}

# 두 앱 같이 — 꼴 · 겹침 · 잘림 · 높이 · 넘침 · 누름 자리
EV = r"""(function(){ if (window.__EV) return;
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const vis = e => { if (!e || !e.isConnected || !e.getClientRects().length) return false; const s = getComputedStyle(e); return s.visibility !== 'hidden' && s.display !== 'none'; };
const desc = e => e ? (e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\s+/).slice(0, 3).join('.') : '')).slice(0, 64) : 'null';
const hit = e => { if (!e) return null; const r = e.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2, a = document.elementFromPoint(cx, cy);
  return { cx: +cx.toFixed(1), cy: +cy.toFixed(1), on: !!a && (a === e || e.contains(a)) && cx > 0 && cy > 0 && cx < innerWidth && cy < innerHeight, at: desc(a), t: txt(e).slice(0, 40) }; };
window.__EV = {
  txt, vis, desc, hit,
  W: ms => new Promise(r => setTimeout(r, ms)),
  css(sel){ const e = [...document.querySelectorAll(sel)].find(vis); if (!e) return null; const s = getComputedStyle(e);
    return { t: txt(e), fs: s.fontSize, fw: s.fontWeight, c: s.color, bg: s.backgroundColor, bw: [s.borderTopWidth, s.borderRightWidth, s.borderBottomWidth, s.borderLeftWidth].join(' '),
      ws: s.whiteSpace, ml: s.marginLeft, pd: [s.paddingTop, s.paddingRight, s.paddingBottom, s.paddingLeft].join(' '), sh: s.boxShadow, rad: s.borderRadius, cur: s.cursor, td: s.textDecorationLine,
      tag: e.tagName, click: typeof e.onclick === 'function' || e.hasAttribute('onclick') }; },
  cnt(within){ const r = typeof within === 'string' ? document.querySelector(within) : within; return r ? { n: r.querySelectorAll('.ewmn').length, x: r.querySelectorAll('.ewmx').length, kids: r.querySelectorAll('*').length } : null; },
  nAll(sel){ return [...document.querySelectorAll(sel)].filter(vis).length; },
  texts(sel){ return [...document.querySelectorAll(sel)].map(txt); },
  rowIdx(rowSel, inSel){ const L = [...document.querySelectorAll(rowSel)]; return L.findIndex(r => vis(r) && r.querySelector(inSel) && vis(r.querySelector(inSel))); },
  rowAt(rowSel, j, inSel){ const r = [...document.querySelectorAll(rowSel)][j]; if (!r) return null; const e = inSel ? r.querySelector(inSel) : r; if (!e) return null;
    try { e.scrollIntoView({ block: 'center', inline: 'nearest' }); } catch (x) {} return Object.assign(hit(e), { row: txt(r).slice(0, 60) }); },
  chk(sel){
    const out = { n: 0, cov: [], clip: [], ovl: [], offx: [] };
    [...document.querySelectorAll(sel)].filter(vis).forEach(e => {
      out.n++;
      try { e.scrollIntoView({ block: 'center', inline: 'nearest' }); } catch (x) {}
      const r = e.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2, lb = txt(e) + ' @' + desc(e.parentElement);
      if (r.left < -0.5 || r.right > innerWidth + 0.5) out.offx.push(lb);
      const a = document.elementFromPoint(cx, cy); if (!(a && (a === e || e.contains(a)))) out.cov.push(lb + ' ← ' + desc(a));
      for (let p = e.parentElement; p && p !== document.body && p !== document.documentElement; p = p.parentElement){ const cs = getComputedStyle(p);
        if (/(hidden|clip|auto|scroll)/.test(cs.overflowX + ' ' + cs.overflowY)){ const pr = p.getBoundingClientRect();
          if (r.left < pr.left - 0.5 || r.right > pr.right + 0.5 || r.top < pr.top - 0.5 || r.bottom > pr.bottom + 0.5){ out.clip.push(lb + ' ⊄ ' + desc(p)); break; } } }
      [e.previousElementSibling, e.nextElementSibling].forEach(s => { if (!s || !vis(s)) return; const q = s.getBoundingClientRect();
        const ov = Math.max(0, Math.min(r.right, q.right) - Math.max(r.left, q.left)) * Math.max(0, Math.min(r.bottom, q.bottom) - Math.max(r.top, q.top)); if (ov > 1) out.ovl.push(lb + ' × ' + desc(s) + ' ' + ov.toFixed(1)); });
    });
    ['cov', 'clip', 'ovl', 'offx'].forEach(k => { out[k + 'N'] = out[k].length; out[k] = out[k].slice(0, 5); });
    return out; },
  heights(sels){ const o = {}; sels.forEach(s => { o[s] = [...document.querySelectorAll(s)].filter(vis).map(e => [+e.getBoundingClientRect().height.toFixed(1), e.querySelector('.ewmn') ? 1 : 0, txt(e).slice(0, 24), e.scrollWidth - e.clientWidth]); }); return o; },
  over(){ const d = document.documentElement; return { sw: d.scrollWidth, iw: innerWidth, bw: document.body.scrollWidth }; },
  errs(){ return ((window.__EH || {}).errs || []).slice(); },
  eh(){ const H = window.__EH || {}; return { tReady: +(H.tReady || 0).toFixed(0), tReq: +(H.tReq || 0).toFixed(0), tEx: +(H.tEx || 0).toFixed(0), nEx: H.nEx, now: +performance.now().toFixed(0) }; },
  btn(fn){ let b = document.getElementById('__evbtn'); if (b) b.remove(); b = document.createElement('button'); b.id = '__evbtn'; b.textContent = '·';
    b.style.cssText = 'position:fixed;left:6px;bottom:6px;z-index:2147483646;width:28px;height:22px;opacity:.6'; b.onclick = ev => { b.remove(); fn(ev); }; document.body.appendChild(b); return hit(b); },
  scrollerOf(e){ for (let p = e; p && p !== document.body && p !== document.documentElement; p = p.parentElement){ const cs = getComputedStyle(p); if (/(auto|scroll)/.test(cs.overflowY) && p.scrollHeight > p.clientHeight + 4) return p; } return document.scrollingElement; },
  toFirst(sel){ const e = [...document.querySelectorAll(sel)].find(vis); if (!e) return null; try { e.scrollIntoView({ block: 'center', inline: 'nearest' }); } catch (x) {} return hit(e); }
};
})();"""

# 조판기 — 하네스 열쇠 지도 · 줄 이름 → 줄 열쇠 · 서랍 · 첫 화면 · 1:1 자리
JO = r"""(function(){ if (window.__EL) return;
const W = ms => new Promise(r => setTimeout(r, ms));
const busyNow = () => { try { return !!busy; } catch (e) { return false; } };
const idle = async () => { for (let i = 0; i < 1600; i++){ if (!busyNow()) return true; await W(25); } return false; };
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const byRI = (a, b) => { const x = a.split('|').map(Number), y = b.split('|').map(Number); return x[0] - y[0] || x[1] - y[1]; };
const fmt = ps => { const by = {}; ps.forEach(p => { const r = +p.split('|')[0]; by[r] = (by[r] || 0) + 1; }); return Object.keys(by).map(Number).sort((a, b) => a - b).map(r => r + 'x' + by[r]).join(' '); };
const mk = ps => ps.slice().sort(byRI).map(p => p.replace('|', '-') + '-X');
let JM = {}, JMX = {};
const expOf = (keys, MP) => { const s = new Set(), nv = []; (keys || []).forEach(k => (MP[k] || []).forEach(p => { nv.push(p); s.add(p); })); return { t: fmt([...s]), nv: fmt(nv), ps: [...s].sort(byRI) }; };
const row = (k, lab, n, et, ks) => { if (ks === null) return { k, lab, n, ewmn: et, amb: 1 }; if (ks === undefined) return { k, lab, n, ewmn: et, keysN: null };
  const e = expOf(ks, JM), x = expOf(ks, JMX); return { k, lab, n, ewmn: et, keysN: ks.length, exp: e.t, naive: e.nv, expX: x.t, ps: e.ps }; };
const ewmnOf = r => [...r.querySelectorAll('.ewmn')].map(txt).join(' / ');
/* 하네스 열쇠 지도 — (회, 번) → 리담 문제 지문 전부 + 책 지문 · 문항째 카드(시험문번 · 연도 / uid) · 앱 ewmMap 안 씀 */
function mapOf(WRl){
  const m = {}, add = (k, p) => { if (!k) return; const L = m[k] = m[k] || []; if (L.indexOf(p) < 0) L.push(p); };
  const P = (VJ && VJ.P7map) || {}, O = (MLN && MLN.ok && MLN.obj) || {};
  (WRl || []).forEach(([r, i]) => { const y = String(r + 1963), p = r + '|' + i;
    (VJ.qs || []).forEach(q => { if (String(q.연도) === y && String(q.시험문번 || '') === String(i)) (q.지문 || []).forEach(z => add(z.uid || ('L:' + q.id + '#' + z.n), p)); });
    const hz = z => { if (String(z.시험문번 || '') === String(i) && ewmYear(z) === y) return true; const pu = jxeParseUid(z.uid); return !!(pu && pu.law === S.law && pu.no === i && String(pu.y) === y); };
    Object.keys(P).forEach(id => { const z = P[id]; if (z && hz(z)) add(z.uid || ('P7:' + z.id), p); });
    Object.keys(O).forEach(id => { const o = O[id]; if (o && hz(o)) add(o.uid || ('P7:' + o.id), p); });
  });
  return m;
}
/* 줄 이름 → 줄 열쇠(서랍 jtPaint · jtOwnRows · 첫 화면 mbDash · mdpHead · mdpOwnRows 와 같은 규칙 · 바탕 함수만 부름) */
function dicts(){
  const J = JTDATA, M = J.M, byId = J.byId, P7map = J.P7map, mln = !!(MLN && MLN.ok);
  const kidOf = i => (i + 1 < M.length) && (M[i + 1].깊이 > M[i].깊이);
  const lab = i => ((M[i].no ? M[i].no + (M[i].깊이 === 1 ? '. ' : ' ') : '') + M[i].제목);
  const nm0 = i => ((M[i].no ? String(M[i].no) + ' ' : '') + M[i].제목);
  const H = {}, L = {}, SO = {}, amb = [];
  const put = (D, k, v) => { if (!(k in D)){ D[k] = v; return; } if (D[k] && D[k].join('\u0001') === v.join('\u0001')) return; if (D[k] !== null) amb.push(k); D[k] = null; };
  M.forEach((n, i) => {
    const lb = lab(i);
    if (kidOf(i)){
      put(H, lb, uzSub(M, i));
      if (mln){ const d = mlnDirect(M, i, VJ.P7map, VJ.byId); ['n', 'u', 'v'].forEach(ln => { const ks = uzF(d[ln].map(mlnCardKey)); if (ks.length) put(L, lb + MLN_NAME[ln], ks); }); }
      return;
    }
    const own = mgKeys(M, i, byId, P7map);
    const lines = mln ? MLN_LNS.map(ln => [ln, mlnKeys(M, i, ln, P7map, byId)]).filter(x => x[1].length) : [];
    (lines.length ? lines : [['b', own]]).forEach(([ln, ks]) => put(L, lb + (MLN_NAME[ln] || ''), ks));
    if (n.깊이 === 1 && own.length){
      const ls = mln ? MLN_LNS.map(ln => [ln, mlnKeys(M, i, ln, VJ.P7map, byId)]).filter(x => x[1].length) : [];
      const L0 = ls.length ? ls[0] : ['b', own];
      put(SO, nm0(i) + (L0[0] !== 'b' ? MLN_NAME[L0[0]] : ''), ls.length > 1 ? uzSub(M, i) : L0[1]);
      ls.slice(1).forEach(([ln, ks]) => put(L, nm0(i) + MLN_NAME[ln], ks));
    }
  });
  put(L, '미분류 (리담)', uzUnkKeys(J.qs, M));
  return { H, L, SO, amb };
}
window.__EL = {
  idle, W,
  st: () => (typeof EWM === 'undefined' ? '정의 없음' : EWM.st),
  async go(o){ await idle(); try { closeAllPops(true); } catch (e) {} Object.assign(S, o || {}); await render(); await idle(); await W(250);
    return { law: S.law, tab: S.tab, jt: S.jimunTab, dash: !!document.querySelector('#slot .mbdash'), drawer: !!document.querySelector('#jtlist .jtit') }; },
  async mln(){ try { await jpMlnReady(); } catch (e) {} for (let i = 0; i < 150 && !(MLN && MLN.ok); i++) await W(100); return !!(MLN && MLN.ok); },
  setMap(a, b){ JM = mapOf(a); JMX = mapOf(b); return { n: Object.keys(JM).length, nx: Object.keys(JMX).length }; },
  mapCmp(){ if (typeof ewmMap !== 'function') return null; const a = ewmMap(), d = [];
    const ks = new Set(Object.keys(a).filter(k => !/^Q\|/.test(k)).concat(Object.keys(JM)));
    ks.forEach(k => { const x = (a[k] || []).map(v => v.r + '|' + v.i).sort(byRI).join(','), y = (JM[k] || []).slice().sort(byRI).join(','); if (x !== y) d.push([k, x, y]); });
    return { n: ks.size, nd: d.length, diff: d.slice(0, 8) }; },
  drawer(){
    const t = document.getElementById('jtlist'); if (!t || !JTDATA) return null;
    const D = dicts(), out = [];
    [...t.children].forEach(r => {
      const et = ewmnOf(r);
      if (r.classList.contains('jtch')){ const nm = r.querySelector(':scope > .jtnm');
        if (!nm){ out.push({ k: 'g', lab: txt(r).slice(0, 24), ewmn: et }); return; }
        const lb = txt(nm); out.push(Object.assign(row('h', lb, +txt(r.querySelector(':scope > .n')), et, D.H[lb]), { d2: r.classList.contains('d2') ? 1 : 0 })); return; }
      if (r.classList.contains('jtych')){ out.push({ k: 'yh', lab: txt(r.querySelector('.tx')), ewmn: et }); return; }
      if (!r.classList.contains('jtit')) return;
      const l1 = r.querySelector(':scope > .l1'), lb = txt(l1 && l1.querySelector(':scope > .tx'));
      if (r.classList.contains('jtyit')){ out.push({ k: 'y', lab: lb, y: r.dataset.gy, ewmn: et }); return; }
      out.push(row('l', lb, +txt(l1 && l1.querySelector(':scope > .n')), et, D.L[lb]));
    });
    return { rows: out, nAmb: D.amb.length, amb: D.amb.slice(0, 6) };
  },
  dash(){
    const d = document.querySelector('#slot .mbdash'); if (!d || !JTDATA) return null;
    const D = dicts(), out = [];
    const totN = e => { const m = /(\d+)/.exec(txt(e)); return m ? +m[1] : null; };
    d.querySelectorAll('.mbur, .mbch > .hh, .mbsj > .hd').forEach(r => {
      const et = ewmnOf(r);
      if (r.matches('.mbsj > .hd')){ out.push({ k: 'card', lab: txt(r).slice(0, 30), ewmn: et }); return; }
      if (r.matches('.mbch > .hh')){ const lb = txt(r.querySelector(':scope > .nm')); out.push(row('h', lb, totN(r.querySelector(':scope > .tot')), et, D.H[lb])); return; }
      const L = r.querySelector(':scope > .l'), lb = txt(L && L.querySelector(':scope > .nm')), n = totN(L && L.querySelector(':scope > .tot'));
      if (r.dataset.giy){ out.push({ k: 'y', lab: lb, y: r.dataset.giy, ewmn: et }); return; }
      if (r.classList.contains('mdph')){ out.push(row('h', lb, n, et, D.H[lb])); return; }
      if (r.classList.contains('mbsolo')){ out.push(row('s', lb, n, et, D.SO[lb])); return; }
      out.push(row('l', lb, n, et, D.L[lb]));
    });
    return { rows: out, nAmb: D.amb.length, amb: D.amb.slice(0, 6), empty: txt(d.querySelector('.mbempty')) || null };
  },
  /* J5 — 🔍 검색: 틀린 문제(pair) 지문 하나의 글 조각으로 찾고 줄마다 표시 = 하네스 지도(mbSearchRun 의 차례 규칙 그대로 기대 차례) */
  async j5(pair){
    const P = OXPOOL || {}, ks = Object.keys(P);
    const kB = ks.find(k => (JM[k] || []).indexOf(pair) >= 0 && String((P[k] || {}).t || '').length > 24); if (!kB) return { err: 'no key ' + pair };
    const t = String(P[kB].t); let q = '';
    for (let L = 14; L <= Math.min(64, t.length); L += 5){ q = t.slice(0, L).trim(); if (ks.filter(k => String((P[k] || {}).t || '').includes(q)).length <= 3) break; }
    S.oxQMode = 'q'; S.oxQ = q; if (MBSR && MBSR.inp) MBSR.inp.value = q; mbSearchRun(); await W(250);
    const idk = uidSearchKeys(q, P);
    const hit = idk.concat(ks.filter(k => idk.indexOf(k) < 0 && (String((P[k] || {}).t || '').includes(q) || String((P[k] || {}).name || '').includes(q)))).filter(k => uzPass(k)).slice(0, 200);
    const rows = MBSR && MBSR.box ? [...MBSR.box.querySelectorAll(':scope > .rr')] : [];
    return { q, kB, j: hit.indexOf(kB), n: rows.length, nHit: hit.length, rows: rows.map((r, j) => ({ got: [...r.querySelectorAll('.ewmx')].map(txt), want: mk(JM[hit[j]] || []) })) };
  },
  /* J6 — 기출뷰 해 y 쪽 전부 · 문항 머리(.exv-head 바로 밑 .ewmx) */
  async j6(y){
    try { closeAllPops(true); } catch (e) {} S.tab = 'jimun'; S.omr = false; S.exvPg = S.exvPg || {}; mbGiGo(y);
    for (let i = 0; i < 150 && !document.querySelector('#slot .exv-q'); i++) await W(100); await idle();
    const list = (MBHEAD && MBHEAD.list) || [], pk = PLAW() + ':' + y, nPg = Math.max(1, Math.ceil(list.length / 5)), heads = {};
    for (let pg = 0; pg < nPg; pg++){ S.exvPg[pk] = pg; await render(); await idle(); await W(150);
      document.querySelectorAll('#slot .exv-head').forEach(h => { const no = parseInt(txt(h.querySelector('.exv-no')), 10); if (no) heads[no] = [...h.querySelectorAll(':scope > .ewmx')].map(txt); }); }
    return { n: list.length, nPg, heads };
  },
  async exvAt(y, no){ S.tab = 'jimun'; S.omr = false; S.exvPg = S.exvPg || {}; mbGiGo(y);
    for (let i = 0; i < 150 && !document.querySelector('#slot .exv-q'); i++) await W(100); await idle();
    const list = (MBHEAD && MBHEAD.list) || [], ix = list.findIndex(q => +giNo(q) === +no); S.exvPg[PLAW() + ':' + y] = ix >= 0 ? Math.floor(ix / 5) : 0; await render(); await idle(); await W(200);
    const h = [...document.querySelectorAll('#slot .exv-head')].find(x => parseInt(txt(x.querySelector('.exv-no')), 10) === +no); if (h) try { h.scrollIntoView({ block: 'center' }); } catch (e) {}
    return !!h; },
  /* J7 — 🔗 연결 목록 · 같은 판례 목록(메모리 덧판 LKREC · 저장 안 함) */
  j7prep(kind, pair){
    const P = OXPOOL || {}, ks = Object.keys(P);
    const kB = ks.find(k => (JM[k] || []).indexOf(pair) >= 0), nonW = ks.filter(k => !JM[k] && !JMX[k] && String((P[k] || {}).t || '').length > 10);
    const kA = nonW[0], kC = nonW[1]; if (!kB || !kC) return { err: 'no keys' };
    try { closeAllPops(true); } catch (e) {}
    if (kind === 'link'){ LKREC = Object.assign({}, lkAll()); LKREC[kA] = { v: [kB, kC] }; }
    window.__j7 = { kind, kA, kB, kC, n0: POPS.filter(p => p.isConnected).length };
    const at = __EV.btn(ev => kind === 'link' ? linkListPop([kA], ev) : mlnListPop('🔗 같은 판례 · 하네스', [kB, kC], ev));
    return { kA, kB, kC, at, want: mk(JM[kB] || []) };
  },
  j7read(){ const o = window.__j7 || {}; const p = POPS.filter(x => x.isConnected).pop(); if (!p) return { err: 'no pop' };
    const rows = o.kind === 'link' ? [...p.querySelectorAll('.lnkrow')] : [...p.querySelectorAll('.mlnlist > .r')];
    const tag = rows[0] && rows[0].querySelector('.ewmt');
    const R = rows.map(r => ({ tags: [...r.querySelectorAll('.ewmx')].map(txt), cls: [...r.querySelectorAll('.ewmx')].map(e => e.className) }));
    const cur = e => e ? getComputedStyle(e).cursor : null;
    let at = null; if (tag){ try { tag.scrollIntoView({ block: 'center' }); } catch (e) {} at = __EV.hit(tag); }
    const rowAt = rows[0] ? (() => { const n = rows[0].querySelector('.qb, b'); const e = n || rows[0]; try { e.scrollIntoView({ block: 'center' }); } catch (x) {} return __EV.hit(e); })() : null;
    return { pk: p._pk, rows: R, nRows: rows.length, curTag: cur(tag), curRow: cur(rows[0]), at, rowAt, tagClick: tag ? (typeof tag.onclick === 'function') : null };
  },
  pops(){ const L = POPS.filter(p => p.isConnected); return { n: L.length, last: L.length ? L[L.length - 1]._pk : null, ewml: document.querySelectorAll('.ewml').length }; },
  /* B6 — 회독 비교(rndPop · 지어낸 회독 둘 — 메모리만 · 저장 안 함) */
  b6rnd(){
    const J = JTDATA, M = J.M; let i0 = -1, keys = [];
    for (let i = 0; i < M.length; i++){ if (i + 1 < M.length && M[i + 1].깊이 > M[i].깊이) continue; const ks = mgKeys(M, i, J.byId, J.P7map); if (ks.some(k => JM[k])){ i0 = i; keys = ks; break; } }
    if (i0 < 0) return { err: 'no row' };
    const scope = 'mok|' + PLAW() + '|__mg' + i0, wk = keys.find(k => JM[k]);
    RNDREC = Object.assign({}, rndAll()); RNDREC[scope] = [1, 2].map(n => ({ n: n, date: '2026-10-0' + n, total: keys.length, done: keys.length, right: keys.length - 1, wrong: 1, confuse: 0, semi: 0, fake: 0,
      ts: '2026-10-0' + n + 'T00:00:00.000Z', wrongK: [wk], confuseK: [], semiK: [] }));
    const at = __EV.btn(ev => rndPop(scope, keys, '하네스 회독 비교', ev)); return { scope, n: keys.length, at };
  },
  popCnt(){ const p = POPS.filter(x => x.isConnected).pop(); return p ? Object.assign(__EV.cnt(p), { pk: p._pk }) : null; },
  /* B4 — 늦게 받기: 1차객 첫 화면으로 · 스크롤 · 그 전 수 */
  async b4prep(){
    await window.__EL.go({ law: '특허법', tab: 'jimun', jimunTab: 'ox', mok: null, oxQ: '', jtFold: false, jtCh: {}, mbCh: {} });
    const tDash = performance.now(), dash = document.querySelector('#slot .mbdash');
    const sc = dash ? __EV.scrollerOf(dash) : null, ds = __EV.scrollerOf(document.querySelector('#jtlist .jtit') || document.getElementById('jtlist'));
    if (sc) sc.scrollTop = 520; if (ds) ds.scrollTop = 260; await W(120);
    window.__b4 = { sc: sc ? __EV.desc(sc) : null, ds: ds ? __EV.desc(ds) : null };
    return { tDash: +tDash.toFixed(0), eh: __EV.eh(), st: window.__EL.st(), sc: window.__b4.sc, ds: window.__b4.ds, top: sc ? sc.scrollTop : null, dtop: ds ? ds.scrollTop : null,
      nE: document.querySelectorAll('.ewmn').length };
  },
  b4after(){
    const dash = document.querySelector('#slot .mbdash'), sc = dash ? __EV.scrollerOf(dash) : null, ds = __EV.scrollerOf(document.querySelector('#jtlist .jtit') || document.getElementById('jtlist'));
    return { eh: __EV.eh(), st: window.__EL.st(), sc: sc ? __EV.desc(sc) : null, ds: ds ? __EV.desc(ds) : null, top: sc ? sc.scrollTop : null, dtop: ds ? ds.scrollTop : null,
      nDrawer: document.querySelectorAll('#jtlist .ewmn').length, nDash: document.querySelectorAll('#slot .mbdash .ewmn').length };
  }
};
})();"""

# 민법 — Q-id 지도(파이썬이 줌) · 서랍(과목마다) · 첫 화면 · 1:1 자리 · B4 · B6
MB = r"""(function(){ if (window.__ML) return;
const W = ms => new Promise(r => setTimeout(r, ms));
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const byRI = (a, b) => { const x = a.split('|').map(Number), y = b.split('|').map(Number); return x[0] - y[0] || x[1] - y[1]; };
const fmt = ps => { const by = {}; ps.forEach(p => { const r = +p.split('|')[0]; by[r] = (by[r] || 0) + 1; }); return Object.keys(by).map(Number).sort((a, b) => a - b).map(r => r + 'x' + by[r]).join(' '); };
const mk = ps => ps.slice().sort(byRI).map(p => p.replace('|', '-') + '-X');
let QM = {}, QMX = {};
const expOf = (ids, MP) => { const s = new Set(), nv = []; (ids || []).forEach(k => (MP[k] || []).forEach(p => { nv.push(p); s.add(p); })); return { t: fmt([...s]), nv: fmt(nv), ps: [...s].sort(byRI) }; };
const row = (k, s, lab, n, et, ids) => { if (!ids) return { k, s, lab, n, ewmn: et, keysN: null };
  const e = expOf(ids, QM), x = expOf(ids, QMX); return { k, s, lab, n, ewmn: et, keysN: ids.length, exp: e.t, naive: e.nv, expX: x.t, ps: e.ps }; };
const ewmnOf = r => [...r.querySelectorAll('.ewmn')].map(txt).join(' / ');
function drawerRows(s, G, out){
  [...document.querySelectorAll('#trlist > .trch, #trlist > .trit')].forEach(r => {
    const et = ewmnOf(r);
    if (r.classList.contains('trch')){ const cm = txt(r.children[1]);
      if (s === '변리사 기출'){ out.push({ k: 'yh', s, lab: cm, ewmn: et }); return; }
      out.push(row('h', s, cm, +txt(r.querySelector(':scope > .n')), et, G[cm] ? Object.values(G[cm]).flatMap(x => x.idsF) : null)); return; }
    const key = r.getAttribute('data-trk') || '', lb = key.split('|||').slice(1).join('|||'), n = +txt(r.querySelector('.l1 > .n'));
    if (s === '변리사 기출'){ out.push({ k: 'y', s, lab: lb, y: (/^(\d{4})년/.exec(lb) || [])[1] || '', ewmn: et, n }); return; }
    let ids = null; for (const cm in G){ if (G[cm][lb]){ ids = G[cm][lb].idsF; break; } }
    out.push(row('l', s, lb, n, et, ids));
  });
}
window.__ML = {
  W,
  st: () => (typeof EWM === 'undefined' ? '정의 없음' : EWM.st),
  setMap(a, b){ QM = a || {}; QMX = b || {}; return Object.keys(QM).length; },
  mapCmp(){ if (typeof ewmIdx !== 'function') return null; const a = ewmIdx(), d = [];
    const ks = new Set(Object.keys(a).filter(k => !/^Q:/.test(k)).concat(Object.keys(QM)));
    ks.forEach(k => { const x = (a[k] || []).map(v => v.r + '|' + v.i).sort(byRI).join(','), y = (QM[k] || []).slice().sort(byRI).join(','); if (x !== y) d.push([k, x, y]); });
    return { n: ks.size, nd: d.length, diff: d.slice(0, 8) }; },
  async drawerAll(){
    const T = trScan(), out = [], cur = trLS(TR_SUBJ, '');
    for (const s of T.order){ trPickSubj(s); await W(30); drawerRows(s, T.G[s] || {}, out); }
    trPickSubj(cur || T.order[0]); await W(30);
    return { rows: out, order: T.order };
  },
  drawerCur(){ const T = trScan(), on = document.querySelector('#trhead button.on'), s = on ? txt(on) : ''; const out = []; drawerRows(s, T.G[s] || {}, out); return { s, rows: out }; },
  dash(){
    const out = [];
    document.querySelectorAll('#dashboard-container [data-trchap], #dashboard-container [data-trrow]').forEach(r => {
      const et = ewmnOf(r);
      if (r.hasAttribute('data-trrow')){ const a = r.getAttribute('data-trrow').split('|||'), s = a[0], lb = a.slice(1).join('|||'), box = r.firstElementChild;
        if (s === '변리사 기출'){ const c = box && box.querySelector('[data-exvcount]'), m = /(\d+)지문/.exec(txt(c));
          out.push({ k: 'y', s, lab: lb, y: (/^(\d{4})년/.exec(lb) || [])[1] || '', ewmn: et, n: m ? +m[1] : null, ids: chapUidsOf(s, lb).length }); return; }
        const c = box && [...box.children].find(e => e.tagName === 'SPAN' && /^총 \d+문제$/.test(txt(e)));
        out.push(row('l', s, lb, c ? +(/\d+/.exec(txt(c))[0]) : null, et, chapUidsOf(s, lb))); return; }
      const a = r.getAttribute('data-trchap').split('|||'), s = a[0], cm = a.slice(1).join('|||');
      if (s === '변리사 기출'){ out.push({ k: 'yh', s, lab: cm, ewmn: et }); return; }
      const labs = [...(r.parentElement || r).querySelectorAll('[data-trrow]')].map(x => x.getAttribute('data-trrow').split('|||').slice(1).join('|||'));
      const c = [...r.children].find(e => /^총 \d+문제$/.test(txt(e)));
      out.push(row('h', s, cm, c ? +(/\d+/.exec(txt(c))[0]) : null, et, [...new Set(labs.flatMap(l => chapUidsOf(s, l)))]));
    });
    document.querySelectorAll('#dashboard-container h2').forEach(h => out.push({ k: 'card', lab: txt(h).slice(0, 24), ewmn: ewmnOf(h) }));
    return { rows: out };
  },
  /* M5 — 🔍 검색: 틀린 문제 지문(qid) 글 조각 · 결과 줄마다 표시 = 하네스 지도 */
  async m5(qid){
    const q = quizData.find(x => x.id === qid); if (!q) return { err: 'no q ' + qid };
    const t = String(q.q || ''); let s = '';
    for (let L = 12; L <= Math.min(60, t.length); L += 4){ s = t.slice(0, L).trim(); if (quizData.filter(x => String(x.q).toLowerCase().includes(s.toLowerCase())).length <= 3) break; }
    try { setSearchMode('q'); } catch (e) {}
    const inp = document.getElementById('search-input'); inp.value = s; runSearch(); await W(300);
    const rows = [...document.querySelectorAll('#search-results > button')];
    return { s, qid, n: rows.length, rows: rows.map(b => { const m = /ID (\S+)/.exec(txt(b.querySelector('div'))), id = m ? m[1] : '';
      return { id, got: [...b.querySelectorAll('.ewmx')].map(txt), want: mk(QM[id] || []), tag: (b.querySelector('.ewmx') || {}).tagName || null }; }) };
  },
  m5pick(qid){ const b = [...document.querySelectorAll('#search-results > button')].find(x => new RegExp('ID ' + qid + '(\\s|$)').test(txt(x.querySelector('div'))));
    const e = b && b.querySelector('.ewmx'); if (!e) return null; try { e.scrollIntoView({ block: 'center' }); } catch (x) {}
    return Object.assign(__EV.hit(e), { lines: b.querySelectorAll('.ewml').length }); },
  m5after(qid){ const b = [...document.querySelectorAll('#search-results > button')].find(x => new RegExp('ID ' + qid + '(\\s|$)').test(txt(x.querySelector('div'))));
    const L = b ? [...b.querySelectorAll('.ewml')] : []; return { lines: L.length, t: L.map(txt), wins: document.querySelectorAll('.oxwin').length, res: !document.getElementById('search-results').classList.contains('hide') }; },
  /* M6 — 기출뷰 해 y 쪽 전부 · 문항 머리(.exv-head 바로 밑 .ewmx) */
  async m6(y){
    document.querySelectorAll('.oxwin').forEach(x => x.remove()); try { goHome(); } catch (e) {}
    const rd = (quizData.find(q => (q.examMeta || []).some(m => String(m.year) === String(y)) && String(q.examYear) === String(y)) || {}).examRound || String(+y - 1963);
    startQuiz('변리사 기출', y + '년 제' + rd + '회');
    for (let i = 0; i < 200 && !document.querySelector('#quiz-container .exv-q'); i++) await W(100); await W(300);
    const heads = {}; let prev = '';
    for (let pg = 0; pg < 40; pg++){ currentPageIndex = pg; renderQuizPage(); await W(220);
      const qs = [...document.querySelectorAll('#quiz-container .exv-q[data-exq]')], sig = qs.map(q => q.getAttribute('data-exq')).join(',');
      if (!sig || sig === prev) break; prev = sig;
      qs.forEach(q => { heads[q.getAttribute('data-exq')] = [...q.querySelectorAll(':scope > .exv-head > .ewmx')].map(txt); }); }
    currentPageIndex = 0; renderQuizPage(); await W(200);
    return { exv: typeof exvOn === 'function' ? exvOn() : null, heads };
  },
  async m6at(key){ let prev = '';
    for (let pg = 0; pg < 40 && !document.querySelector('#quiz-container .exv-q[data-exq="' + key + '"]'); pg++){ currentPageIndex = pg; renderQuizPage(); await W(220);
      const sig = [...document.querySelectorAll('#quiz-container .exv-q[data-exq]')].map(q => q.getAttribute('data-exq')).join(','); if (!sig || sig === prev) break; prev = sig; }
    const h = document.querySelector('#quiz-container .exv-q[data-exq="' + key + '"] > .exv-head'); if (h) try { h.scrollIntoView({ block: 'center' }); } catch (e) {} return !!h; },
  /* B6 — 회독 비교(지어낸 회독 둘 — 이 쪽 localStorage 만) · OMR · 히트맵 */
  b6cmp(){
    const T = trScan(); let s0 = '', l0 = '', ids = [];
    for (const s of T.order){ if (s === '변리사 기출') continue; for (const cm in T.G[s]) for (const lb in T.G[s][cm]){ const r = T.G[s][cm][lb]; if (!l0 && r.ids.some(id => QM[id])){ s0 = s; l0 = lb; ids = r.ids; } } }
    if (!l0) return { err: 'no row' };
    const sf = (document.getElementById('source-filter') || {}).value || 'all', rf = (document.getElementById('review-filter') || {}).value || 'all';
    const all = JSON.parse(localStorage.getItem('ox_chap_history') || '{}'), mk2 = n => { const m = {}; ids.slice(0, 12).forEach((id, j) => m[id] = (j + n) % 3 !== 0); return m; };
    all[s0 + '||' + l0 + '||' + sf + '||' + rf] = [1, 2].map(n => ({ date: '2026-10-0' + n, score: 8, total: Math.min(12, ids.length), marks: mk2(n) }));
    localStorage.setItem('ox_chap_history', JSON.stringify(all));
    openCompareModal(s0, l0); return { s: s0, lab: l0, n: ids.length, open: !document.getElementById('compare-modal').classList.contains('hide') };
  },
  /* B4 — 늦게 받기: 첫 화면 renderDashboard 부름 셈 · 첫 화면 마디 표 · 서랍 펴고 스크롤 */
  async b4prep(){
    window.__rd = []; const o = renderDashboard;
    renderDashboard = function(){ window.__rd.push({ t: +performance.now().toFixed(0), s: String(new Error().stack || '').split('\n').slice(2, 5).map(x => x.trim()).join(' | ').slice(0, 240) }); return o.apply(this, arguments); };
    const dc = document.getElementById('dashboard-container'); window.__b4 = { first: dc.firstElementChild, n: dc.children.length }; window.__b4.first.__keep = 1;
    const tr = document.getElementById('tree'); if (tr && tr.classList.contains('fold') && typeof trFold === 'function') trFold(false);
    await W(80);
    window.scrollTo(0, 900); const tl = document.getElementById('trlist'); if (tl) tl.scrollTop = 260; await W(120);
    return { tW: +performance.now().toFixed(0), eh: __EV.eh(), st: window.__ML.st(), y: Math.round(scrollY), ty: tl ? tl.scrollTop : null, nE: document.querySelectorAll('.ewmn').length };
  },
  b4after(){ const tl = document.getElementById('trlist');
    return { eh: __EV.eh(), st: window.__ML.st(), rd: (window.__rd || []).slice(0, 6), nRd: (window.__rd || []).length, keep: !!(window.__b4 && window.__b4.first.isConnected && window.__b4.first.__keep),
      y: Math.round(scrollY), ty: tl ? tl.scrollTop : null, nDrawer: document.querySelectorAll('#trlist .ewmn').length, nDash: document.querySelectorAll('#dashboard-container .ewmn').length }; }
};
})();"""


class Pg:
    """한 쪽 — 앱 · 판(tag) · 폭(w) · 기록 늦춤(delay)"""

    def __init__(self, br, app, tag, src, w=1440, delay=0):
        self.app, self.tag, self.w = app, tag, w
        d = DEV[w]
        kw = dict(viewport={'width': d['W'], 'height': d['H']})
        if d['mob']:
            kw.update(device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=d['ua'])
        self.ctx = br.new_context(**kw)
        self.remote = Remote()
        self.ctx.route('**/*', route_handler(self.remote))
        cfg = json.dumps({'token': 'harness-token', 'person': '꼬까'})
        self.ctx.add_init_script(PROBE.replace('__D__', str(int(delay))).replace('__R__', READY[app]).replace('__CFG__', json.dumps(cfg)))
        self.ctx.add_init_script(EV)
        self.ctx.add_init_script(JO if app == 'jo' else MB)
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(180000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:300]))
        port = serve(app, tag, src)
        self.t0 = time.time()
        self.pg.goto('http://127.0.0.1:%d/%s/index.html' % (port, 'jo' if app == 'jo' else 'minbeop'), wait_until='load', timeout=180000)
        self.pg.wait_for_function('() => !!(window.__EH && window.__EH.tReady)', timeout=180000)
        self.pg.wait_for_timeout(300)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def wait(self, ms):
        self.pg.wait_for_timeout(ms)

    def until(self, js, ms=15000, step=200):
        t0 = time.time()
        v = None
        while time.time() - t0 < ms / 1000.0:
            try:
                v = self.ev(js)
            except Exception:
                v = None
            if v:
                return v
            self.wait(step)
        return v

    def st(self):
        return self.ev("() => typeof EWM === 'undefined' ? '정의 없음' : EWM.st")

    def ewm_ok(self, ms=20000):
        return self.until("() => typeof EWM !== 'undefined' && (EWM.st === 'ok' || EWM.st === 'fail' || EWM.st === 'none')", ms) and self.st()

    def click(self, at, wait=450):
        if not at or not at.get('on'):
            return False
        self.pg.mouse.click(at['cx'], at['cy'])
        self.wait(wait)
        return True

    def shot(self, name):
        try:
            os.makedirs(SHOTS, exist_ok=True)
            f = os.path.join(SHOTS, '%s_%s_%d_%s.png' % (self.app, self.tag, self.w, name))
            self.pg.screenshot(path=f)
            return f
        except Exception as e:
            return 'shot err ' + str(e)[:80]

    def close(self):
        try:
            ERRS.setdefault('%s %s' % (NAME[self.app], self.tag), []).extend(list(self.ev("() => __EV.errs()") or []) + self.errs)
        except Exception:
            ERRS.setdefault('%s %s' % (NAME[self.app], self.tag), []).extend(self.errs)
        try:
            self.ctx.close()
        except Exception:
            pass


# ════════════════════════ 판정 ════════════════════════
def judge(rows, ry=None, ky=('h', 'l', 's')):
    """줄 목록 → 셈 칸(값이 틀린 줄 · 열쇠 못 찾은 줄 · 줄 수 안 맞는 줄 …)"""
    st = {'rows': 0, 'nz': 0, 'bad': [], 'nokey': [], 'amb': 0, 'nmis': [], 'dedup': 0, 'excl': 0, 'zbad': [], 'y': 0, 'ybad': [], 'zero': 0}
    for r in rows or []:
        k = r.get('k')
        if k in ky:
            st['rows'] += 1
            if r.get('amb'):
                st['amb'] += 1
                continue
            if r.get('keysN') is None:
                st['nokey'].append(r.get('lab'))
                continue
            if r.get('n') is not None and r['n'] != r['keysN']:
                st['nmis'].append([r.get('lab'), r['n'], r['keysN']])
            if r['exp']:
                st['nz'] += 1
            else:
                st['zero'] += 1
            if r['naive'] != r['exp']:
                st['dedup'] += 1
            if r['expX'] != r['exp']:
                st['excl'] += 1
            if (r.get('ewmn') or '') != r['exp']:
                st['bad'].append([r.get('s', '') + ' ' + str(r.get('lab'))[:40], r.get('ewmn'), r['exp']])
        elif k == 'y':
            st['y'] += 1
            want_y = (ry or {}).get(str(r.get('y')), '')
            if (r.get('ewmn') or '') != want_y:
                st['ybad'].append([r.get('lab'), r.get('ewmn'), want_y])
        else:
            if r.get('ewmn'):
                st['zbad'].append([k, r.get('lab'), r.get('ewmn')])
    for x in ('bad', 'nokey', 'nmis', 'zbad', 'ybad'):
        st[x + 'N'] = len(st[x])
        st[x] = st[x][:5]
    return st


def ok_rows(st):
    return st and st['rows'] > 0 and not st['badN'] and not st['nokeyN'] and not st['zbadN']


def ok_y(st):
    return st and st['y'] > 0 and not st['ybadN']


def brief(st):
    return {k: st[k] for k in ('rows', 'nz', 'zero', 'badN', 'bad', 'nokeyN', 'nokey', 'amb', 'zbadN', 'zbad', 'dedup', 'excl')} if st else None


def union_rep(rows, pairs):
    """단원 줄(l · s) 합집합 · 걸친 문제(두 줄 넘게) · 단원에 없는 문제 · 회마다 줄 수의 합"""
    U, where, summ = set(), {}, {}
    for r in rows or []:
        if r.get('k') not in ('l', 's') or not r.get('ps'):
            continue
        for p in r['ps']:
            U.add(p)
            where.setdefault(p, []).append(str(r.get('lab'))[:28])
        for t in (r.get('exp') or '').split():
            a, b = t.split('x')
            summ[a] = summ.get(a, 0) + int(b)
    want_p = {'%d|%d' % (r, i) for r, i in pairs}
    return {'합집합': sorted(U, key=lambda p: tuple(map(int, p.split('|')))), '단원에 없음': sorted(want_p - U), '기록에 없는데 줄에': sorted(U - want_p),
            '걸친 문제': {p: v for p, v in where.items() if len(v) > 1}, '회마다 줄 수의 합': summ}


# ════════════════════════ 관문 ════════════════════════
def jo_rows(p, law):
    p.ev("o => __EL.go(o)", {'law': law, 'tab': 'jimun', 'jimunTab': 'ox', 'mok': None, 'oxQ': '', 'jtFold': False, 'jtCh': {}, 'mbCh': {}, 'omr': False})
    mln = p.ev("() => __EL.mln()")
    p.ev("o => __EL.go(o)", {'law': law, 'tab': 'jimun', 'jimunTab': 'ox', 'mok': None, 'oxQ': '', 'jtFold': False, 'jtCh': {}, 'mbCh': {}, 'omr': False})
    nm = p.ev("([a, b]) => __EL.setMap(a, b)", [wr_of(law), wr_of(law) + wx_of(law)])
    return {'mln': mln, 'map': nm, 'cmp': p.ev("() => __EL.mapCmp()"), 'dr': p.ev("() => __EL.drawer()"), 'da': p.ev("() => __EL.dash()")}


def B1_B2_jo(pn, pb):
    for law in LAWS:
        ry = round_exp(wr_of(law))
        rn = jo_rows(pn, law)
        rb = jo_rows(pb, law) if pb else None
        g = 'B1'
        T(g, '조판기 %s 하네스 지도 = 앱 ewmMap(Q| 문항 열쇠 뺌)' % law, rn['cmp'] and rn['cmp']['nd'] == 0 and rn['map']['n'] > 0,
          {'MLN': rn['mln'], '지도 열쇠': rn['map'], '앱과 다름': rn['cmp'], '바탕 앱과 다름': rb and rb['cmp']})
        for where, key in (('서랍', 'dr'), ('첫 화면', 'da')):
            sn = judge((rn[key] or {}).get('rows'), ry)
            sb = judge((rb[key] or {}).get('rows'), ry) if rb else None
            if (rn[key] or {}).get('empty') and not sn['rows'] and not sn['y'] and (not rb or (rb[key] or {}).get('empty')):
                N(g, '조판기 %s %s — 「%s」(바탕 같음 · 줄 없음 = 해당 없음)' % (law, where, rn[key]['empty']), {'rows': 0})
                continue
            TB(g, '조판기 %s %s 단원 · 장 줄 「61x1 63x2」 = 하네스 셈(틀림 없는 줄 · 머리 = 0)' % (law, where), ok_rows, brief(sn), brief(sb))
            T(g, '조판기 %s %s 줄 열쇠 맞춤(하네스 열쇠 수 = 줄에 적힌 수 · 이름 겹침 %d)' % (law, where, (rn[key] or {}).get('nAmb', -1)),
              sn['rows'] > 0 and not sn['nmisN'] and not sn['nokeyN'], {'줄': sn['rows'], '수 다름': sn['nmisN'], '보기': sn['nmis'], '열쇠 없음': sn['nokeyN'], '겹침': (rn[key] or {}).get('amb')})
            N(g, '조판기 %s %s 중복 · 뺀 줄' % (law, where), {'같은 문제 지문 여럿 걸린 줄(중복 없이 셈)': sn['dedup'], 'ok true · 지운 회차 · 2차 · 점수만이 걸린 줄(뺀 값)': sn['excl'], '수 있는 줄': sn['nz']})
            TB('B2', '조판기 %s %s 회차 줄 = 그 회 틀린 문제 수 %s' % (law, where, ry), ok_y, {'y': sn['y'], 'ybadN': sn['ybadN'], 'ybad': sn['ybad']},
               sb and {'y': sb['y'], 'ybadN': sb['ybadN'], 'ybad': sb['ybad']})
        N('B2', '조판기 %s 회차 줄 ↔ 서랍 단원 줄 문제 집합' % law, union_rep((rn['dr'] or {}).get('rows'), wr_of(law)))


def B1_B2_mb(pn, pb, QM, QMX):
    ry = round_exp(wr_of('민법'))
    out = {}
    for p in [x for x in (pn, pb) if x]:
        p.ev("([a, b]) => __ML.setMap(a, b)", [QM, QMX])
        out[p.tag] = {'cmp': p.ev("() => __ML.mapCmp()"), 'dr': p.ev("() => __ML.drawerAll()"), 'da': p.ev("() => __ML.dash()")}
    rn, rb = out['NEW'], out.get('BASE')
    T('B1', '민법 하네스 지도(문항마스터 파이썬) = 앱 ewmIdx(Q: 문항 열쇠 뺌)', rn['cmp'] and rn['cmp']['nd'] == 0 and rn['cmp']['n'] > 0,
      {'Q-id': len(QM), '앱과 다름': rn['cmp'], '바탕 앱과 다름': rb and rb['cmp']})
    for where, key in (('서랍', 'dr'), ('첫 화면', 'da')):
        sn = judge(rn[key]['rows'], ry)
        sb = judge(rb[key]['rows'], ry) if rb else None
        TB('B1', '민법 %s 단원 · 장 줄 「61x1 63x2」 = 하네스 셈(틀림 없는 줄 · 과목 머리 = 0)' % where, ok_rows, brief(sn), brief(sb))
        T('B1', '민법 %s 줄 열쇠 맞춤(하네스 Q-id 수 = 줄에 적힌 수)' % where, sn['rows'] > 0 and not sn['nmisN'] and not sn['nokeyN'],
          {'줄': sn['rows'], '수 다름': sn['nmisN'], '보기': sn['nmis'], '열쇠 없음': sn['nokeyN']})
        N('B1', '민법 %s 중복 · 뺀 줄' % where, {'같은 문제 지문 여럿 걸린 줄(중복 없이 셈)': sn['dedup'], 'ok true · 지운 회차 · 2차 · 점수만이 걸린 줄(뺀 값)': sn['excl'], '수 있는 줄': sn['nz']})
        TB('B2', '민법 %s 「변리사 기출」 회차 줄 = 그 회 틀린 문제 수 %s' % (where, ry), ok_y, {'y': sn['y'], 'ybadN': sn['ybadN'], 'ybad': sn['ybad']},
           sb and {'y': sb['y'], 'ybadN': sb['ybadN'], 'ybad': sb['ybad']})
    N('B2', '민법 회차 줄 ↔ 서랍 단원 줄 문제 집합', union_rep(rn['dr']['rows'], wr_of('민법')))


def B3_jo(pn, pb):
    law = '특허법'
    for p in [x for x in (pn, pb) if x]:
        jo_rows(p, law)
    # J5 검색
    v = {}
    for p in [x for x in (pn, pb) if x]:
        p.ev("o => __EL.go(o)", {'law': law, 'tab': 'jimun', 'jimunTab': 'ox', 'mok': None, 'oxQ': '', 'jtFold': True, 'omr': False})
        v[p.tag] = p.ev("(x) => __EL.j5(x)", '63|13')
    def j5ok(x):
        return x and not x.get('err') and x['j'] >= 0 and x['n'] > 0 and all(r['got'] == r['want'] for r in x['rows']) and any(r['want'] for r in x['rows'])
    TB('B3', 'J5 조판기 🔍 검색 결과 줄마다 「63-13-X」 = 하네스 지도', j5ok, v.get('NEW'), v.get('BASE'),
       show=lambda x: x and ({k: x.get(k) for k in ('q', 'j', 'n', 'nHit', 'err')} | {'rows': (x.get('rows') or [])[:4]}))
    if v.get('NEW') and v['NEW'].get('j', -1) >= 0:
        j = v['NEW']['j']
        at = pn.ev("([j]) => __EV.rowAt('.mbres > .rr', j, '.ewmx')", [j])
        p0 = pn.ev("() => __EL.pops()")
        pn.click(at, 500)
        p1 = pn.ev("() => __EL.pops()")
        ln = pn.ev("([j]) => { const r = [...document.querySelectorAll('.mbres > .rr')][j]; return r ? [...r.querySelectorAll('.ewml')].map(e => __EV.txt(e)) : null; }", [j])
        pn.click(pn.ev("([j]) => __EV.rowAt('.mbres > .rr', j, '.ewmx')", [j]), 400)
        ln2 = pn.ev("([j]) => { const r = [...document.querySelectorAll('.mbres > .rr')][j]; return r ? r.querySelectorAll('.ewml').length : null; }", [j])
        T('B3', 'J5 누르면 펼침 한 줄(내 답 · 정답 · 평균 정답률) · 다시 누르면 접힘 · 줄 누름(지문 팝업) 안 샘',
          at and at.get('on') and ln and len(ln) == 1 and re.match(r'^내 답 .+ · 정답 .+ · 평균 정답률 .+$', ln[0] or '') and ln2 == 0 and p1['n'] == p0['n'],
          {'at': at, '펼침': ln, '다시 누름 뒤': ln2, '팝업 수 앞/뒤': [p0['n'], p1['n']]})
    # J6 기출뷰 문항 머리
    for y in ('2024', '2026'):
        h = {}
        for p in [x for x in (pn, pb) if x]:
            h[p.tag] = p.ev("(y) => __EL.j6(y)", y)
        r = int(y) - 1963
        want_h = {str(i): ['%d-%d-X' % (r, i)] for rr, i in wr_of(law) if rr == r}

        def j6ok(x, want_h=want_h):
            if not x or not x.get('heads'):
                return False
            got = {str(k): v for k, v in x['heads'].items()}
            return all(got.get(k) == v for k, v in want_h.items()) and all((v == [] or k in want_h) for k, v in got.items())
        def j6s(x):
            if not x:
                return None
            got = {str(k): v for k, v in (x.get('heads') or {}).items()}
            return {'문항': x.get('n'), '쪽': x.get('nPg'), '표시 문항': {k: v for k, v in got.items() if v}, '기대': want_h}
        TB('B3', 'J6 조판기 %s 기출뷰 %s 문항 머리 「%d-<번>-X」(틀린 문항만 · 하나씩)' % (law, y, r), j6ok, h.get('NEW'), h.get('BASE'), show=j6s)
    # J7 연결 목록 · 같은 판례 목록
    for kind, nm in (('link', '🔗 연결 목록(linkListPop)'), ('mln', '같은 판례 목록(mlnListPop)')):
        res = {}
        for p in [x for x in (pn, pb) if x]:
            p.ev("o => __EL.go(o)", {'law': law, 'tab': 'jimun', 'jimunTab': 'ox', 'mok': None, 'oxQ': '', 'jtFold': True, 'omr': False})
            pr = p.ev("([k, x]) => __EL.j7prep(k, x)", [kind, '63|13'])
            p.click(pr.get('at'), 600)
            rd = p.ev("() => __EL.j7read()")
            c0 = p.ev("() => __EL.pops()")
            at = rd.get('at') if p.tag == 'NEW' else rd.get('rowAt')
            p.click(at, 600)
            c1 = p.ev("() => __EL.pops()")
            res[p.tag] = {'prep': {k: pr.get(k) for k in ('want',)}, 'read': rd, 'pop': [c0, c1]}

        def j7ok(x):
            rd = x['read']
            return (not rd.get('err') and rd['nRows'] >= 2 and rd['rows'][0]['tags'] == x['prep']['want'] and rd['rows'][1]['tags'] == []
                    and all('ewmt' in c for c in rd['rows'][0]['cls']))
        TB('B3', 'J7 조판기 %s — 틀린 지문 줄에 누름 없는 「63-13-X」 · 안 틀린 줄 0' % nm, j7ok, res['NEW'], res.get('BASE'),
           show=lambda x: x and {'want': x['prep']['want'], 'rows': x['read'].get('rows'), 'cursor 표시/줄': [x['read'].get('curTag'), x['read'].get('curRow')]})
        if res.get('BASE'):
            nn, bb = res['NEW'], res['BASE']
            T('B3', 'J7 %s 표시를 누르면 = 줄 누름(지문 팝업 · 바탕에서 줄을 누른 것과 같은 창) · 펼침 줄 0 · 표시 onclick 없음' % nm,
              nn['pop'][1]['n'] == nn['pop'][0]['n'] + 1 and nn['pop'][1]['last'] == bb['pop'][1]['last'] and nn['pop'][1]['ewml'] == 0 and nn['read'].get('tagClick') is False
              and nn['read'].get('curTag') == nn['read'].get('curRow'),
              {'새 판 팝업': nn['pop'], '바탕 팝업': bb['pop'], 'cursor': [nn['read'].get('curTag'), nn['read'].get('curRow')]})


def B3_mb(pn, pb, QM):
    qid = next((k for k, v in sorted(QM.items()) if '63|13' in v), None)
    v = {}
    for p in [x for x in (pn, pb) if x]:
        p.ev("() => { try { goHome(); } catch (e) {} }")
        p.wait(300)
        v[p.tag] = p.ev("(q) => __ML.m5(q)", qid)

    def m5ok(x):
        return x and not x.get('err') and x['n'] > 0 and any(r['id'] == qid and r['got'] == r['want'] and r['want'] for r in x['rows']) and all(r['got'] == r['want'] for r in x['rows'])
    TB('B3', 'M5 민법 🔍 검색 결과 줄마다 「63-13-X」 = 하네스 지도(Q-id %s)' % qid, m5ok, v.get('NEW'), v.get('BASE'),
       show=lambda x: x and {'s': x.get('s'), 'n': x.get('n'), 'err': x.get('err'), 'rows': (x.get('rows') or [])[:4]})
    at = pn.ev("(q) => __ML.m5pick(q)", qid)
    if at:
        a0 = pn.ev("(q) => __ML.m5after(q)", qid)
        pn.click(at, 500)
        a1 = pn.ev("(q) => __ML.m5after(q)", qid)
        pn.click(pn.ev("(q) => __ML.m5pick(q)", qid), 400)
        a2 = pn.ev("(q) => __ML.m5after(q)", qid)
        T('B3', 'M5 누르면 펼침 한 줄(내 답 · 정답 · 평균 정답률) · 다시 누르면 접힘 · 결과 줄 누름(문항 팝업) 안 샘',
          at.get('on') and a1['lines'] == 1 and re.match(r'^내 답 .+ · 정답 .+ · 평균 정답률 .+$', (a1['t'] or [''])[0]) and a2['lines'] == 0 and a1['wins'] == a0['wins'] and a1['res'],
          {'at': at, '앞': a0, '누름 뒤': a1, '다시 누름 뒤': a2, '표시 꼴': (v['NEW']['rows'] or [{}])[0].get('tag')})
    for y in ('2024', '2026'):
        r = int(y) - 1963
        want_h = {'%s:%d' % (y, i): ['%d-%d-X' % (r, i)] for rr, i in wr_of('민법') if rr == r}
        h = {}
        for p in [x for x in (pn, pb) if x]:
            h[p.tag] = p.ev("(y) => __ML.m6(y)", y)

        def m6ok(x, want_h=want_h):
            if not x or not x.get('heads'):
                return False
            got = x['heads']
            return all(got.get(k) == v for k, v in want_h.items()) and all((v == [] or k in want_h) for k, v in got.items())
        def m6s(x):
            return x and {'기출뷰': x.get('exv'), '문항': len(x.get('heads') or {}), '표시 문항': {k: v for k, v in (x.get('heads') or {}).items() if v}, '기대': want_h}
        TB('B3', 'M6 민법 기출뷰 %s 문항 머리 「%d-<번>-X」(틀린 문항만 · 하나씩)' % (y, r), m6ok, h.get('NEW'), h.get('BASE'), show=m6s)
    for p in [x for x in (pn, pb) if x]:
        p.ev("() => { document.querySelectorAll('.oxwin').forEach(x => x.remove()); try { goHome(); } catch (e) {} }")


STY = {'fs': '10.5px', 'fw': '700', 'c': 'rgb(220, 38, 38)', 'bg': 'rgba(0, 0, 0, 0)', 'bw': '0px 0px 0px 0px', 'ws': 'nowrap', 'ml': '4px', 'pd': '0px 0px 0px 0px', 'sh': 'none'}


def sty_ok(c):
    return bool(c) and all(str(c.get(k)) == v for k, v in STY.items()) and re.fullmatch(r'\d+x\d+( \d+x\d+)*', c.get('t') or '') and not c.get('click')


def B5_style(pn, pb, app):
    if app == 'jo':
        for p in [x for x in (pn, pb) if x]:
            p.ev("o => __EL.go(o)", {'law': '특허법', 'tab': 'jimun', 'jimunTab': 'ox', 'mok': None, 'oxQ': '', 'jtFold': False, 'jtCh': {}, 'mbCh': {}, 'omr': False})
            p.ev("() => __EL.mln()")
            p.ev("o => __EL.go(o)", {'law': '특허법', 'tab': 'jimun', 'jimunTab': 'ox', 'mok': None, 'oxQ': '', 'jtFold': False, 'jtCh': {}, 'mbCh': {}, 'omr': False})
    else:
        for p in [x for x in (pn, pb) if x]:
            p.ev("() => { document.querySelectorAll('.oxwin').forEach(x => x.remove()); try { goHome(); } catch (e) {} if (typeof trFold === 'function') trFold(false); }")
    sels = (('서랍', '#jtlist .ewmn'), ('첫 화면', '#slot .mbdash .ewmn')) if app == 'jo' else (('서랍', '#trlist .ewmn'), ('첫 화면', '#dashboard-container .ewmn'))
    for where, sel in sels:
        cn = pn.ev("(s) => __EV.css(s)", sel)
        cb = (pb.ev("(s) => __EV.css(s)", sel) or {'없음': '바탕엔 .ewmn 이 없다'}) if pb else None
        TB('B5', '%s %s .ewmn 꼴 10.5px · 700 · rgb(220,38,38) · 바탕 투명 · 테두리 0 · nowrap · margin-left 4px · 「<회>x<수>」 소문자 · onclick 없음' % (NAME[app], where), sty_ok, cn, cb)


def hcmp(hn, hb):
    """같은 선택자 줄 높이 — 새 판에 .ewmn 이 있는 줄만 바탕 같은 차례 줄과 맞댐"""
    out = {}
    for s, L in (hn or {}).items():
        B = (hb or {}).get(s) or []
        idx = [j for j, x in enumerate(L) if x[1]]
        d = [round(abs(L[j][0] - B[j][0]), 1) for j in idx if j < len(B)]
        big = [[L[j][2], B[j][0], L[j][0]] for j in idx if j < len(B) and abs(L[j][0] - B[j][0]) > 1]
        ovr = [[L[j][2], B[j][3], L[j][3]] for j in idx if j < len(B) and L[j][3] > max(0, B[j][3]) + 1]
        out[s] = {'줄': len(L), '바탕 줄': len(B), '.ewmn 줄': len(idx), '최대 차': max(d) if d else None, '1 넘음': len(big), '보기(이름 · 바탕 · 새 판)': big[:4],
                  '줄 밖 밀림(바탕보다 넘침 · px)': len(ovr), '밀림 보기(이름 · 바탕 · 새 판)': ovr[:4]}
    return out


def h_ok(c):
    return all(v['줄'] == v['바탕 줄'] and v['.ewmn 줄'] > 0 and (v['최대 차'] is not None and v['최대 차'] <= 1) and not v['줄 밖 밀림(바탕보다 넘침 · px)'] for v in c.values())


def B5_click_jo(pn, pb):
    law = '특허법'
    for p in (pn, pb):
        p.ev("o => __EL.go(o)", {'law': law, 'tab': 'jimun', 'jimunTab': 'ox', 'mok': None, 'oxQ': '', 'jtFold': False, 'jtCh': {}, 'mbCh': {}, 'omr': False})
    cases = (('서랍 단원 줄', '#jtlist > .jtit:not(.jtyit)', '.ewmn', '.l1 > .n', "() => ({ mok: S.mok, tab: S.jimunTab, y: S.year || null })"),
             ('서랍 회차 줄', '#jtlist > .jtyit', '.ewmn', '.l1 > .n', "() => ({ mok: S.mok, tab: S.jimunTab, y: S.year || null })"),
             ('첫 화면 단원 줄', '#slot .mbdash .mbur:not(.mdph):not([data-giy])', '.ewmn', '.l > .tot', "() => ({ mok: S.mok, tab: S.jimunTab, y: S.year || null })"),
             ('첫 화면 회차 줄', '#slot .mbdash .mbur[data-giy]', '.ewmn', '.l > .tot', "() => ({ mok: S.mok, tab: S.jimunTab, y: S.year || null })"))
    for nm, rs, ins, alt, rd in cases:
        j = pn.ev("([a, b]) => __EV.rowIdx(a, b)", [rs, ins])
        if j is None or j < 0:
            T('B5', '조판기 %s 누름 — .ewmn 있는 줄 없음' % nm, False, '')
            continue
        atn = pn.ev("([a, j, b]) => __EV.rowAt(a, j, b)", [rs, j, ins])
        atb = pb.ev("([a, j, b]) => __EV.rowAt(a, j, b)", [rs, j, alt])
        pn.click(atn, 700)
        pb.click(atb, 700)
        vn, vb = pn.ev(rd), pb.ev(rd)
        T('B5', '조판기 %s 의 「61x1」 글자 누름 = 바탕에서 그 줄 누름(같은 일 · 가로챔 0)' % nm, atn and atn.get('on') and vn == vb and (vn.get('mok') or vn.get('y')),
          {'새 판 누른 곳': atn, '새 판 뒤': vn, '바탕 뒤': vb})
        for p in (pn, pb):
            p.ev("o => __EL.go(o)", {'law': law, 'tab': 'jimun', 'jimunTab': 'ox', 'mok': None, 'oxQ': '', 'year': None, 'jtFold': False, 'jtCh': {}, 'mbCh': {}, 'omr': False})


def B5_click_mb(pn, pb):
    for p in (pn, pb):
        p.ev("() => { try { goHome(); } catch (e) {} const t = document.getElementById('tree'); if (t && t.classList.contains('fold') && typeof trFold === 'function') trFold(false); }")
        p.wait(300)
    # 서랍 단원 줄 — trGo(첫 화면 그 줄로 굴리고 칠함)
    rs = '#trlist > .trit'
    subj = pn.ev("() => { const T = trScan(); for (const s of T.order){ trPickSubj(s); if (document.querySelector('#trlist > .trit .ewmn')) return s; } return null; }")
    pb.ev("(s) => trPickSubj(s)", subj)
    j = pn.ev("([a, b]) => __EV.rowIdx(a, b)", [rs, '.ewmn'])
    rd = "() => { const r = [...document.querySelectorAll('[data-trrow]')].find(x => x.style.backgroundColor); return { hl: r ? r.getAttribute('data-trrow') : null, home: !document.getElementById('home-screen').classList.contains('hide') }; }"
    if j is not None and j >= 0:
        for p in (pn, pb):
            p.ev("() => window.scrollTo(0, 0)")
        atn = pn.ev("([a, j, b]) => __EV.rowAt(a, j, b)", [rs, j, '.ewmn'])
        atb = pb.ev("([a, j, b]) => __EV.rowAt(a, j, b)", [rs, j, '.l1 > .n'])
        pn.click(atn, 150)
        pb.click(atb, 150)
        vn, vb = pn.ev(rd), pb.ev(rd)
        T('B5', '민법 서랍 단원 줄(%s) 의 「61x1」 글자 누름 = 바탕에서 그 줄 누름(첫 화면 그 줄로 · 가로챔 0)' % subj, atn and atn.get('on') and vn == vb and vn.get('hl'),
          {'새 판 누른 곳': atn, '새 판 뒤': vn, '바탕 뒤': vb})
    else:
        T('B5', '민법 서랍 누름 — .ewmn 있는 줄 없음', False, subj)
    # 첫 화면 단원 줄 — 줄 누름 없음(바탕 = 수 글자 누름 → 아무 일 없음)
    for p in (pn, pb):
        p.ev("() => { try { goHome(); } catch (e) {} const t = document.getElementById('tree'); if (t && innerWidth < 900 && typeof trFold === 'function') trFold(true); }")
        p.wait(300)
    rs = '#dashboard-container [data-trrow]'
    j = pn.ev("([a, b]) => __EV.rowIdx(a, b)", [rs, '.ewmn'])
    rd = ("() => ({ home: !document.getElementById('home-screen').classList.contains('hide'), modal: [...document.querySelectorAll('.fixed:not(.hide)')].filter(e => e.offsetParent || getComputedStyle(e).position === 'fixed').length,"
          " win: document.querySelectorAll('.oxwin').length, y: Math.round(scrollY) })")
    if j is not None and j >= 0:
        atn = pn.ev("([a, j, b]) => __EV.rowAt(a, j, b)", [rs, j, '.ewmn'])
        atb = pb.ev("([a, j]) => { const r = [...document.querySelectorAll(a)][j]; const e = r && [...r.firstElementChild.children].find(x => /^총 \\d+문제$/.test(__EV.txt(x)) || x.hasAttribute('data-exvcount')); if (!e) return null; e.scrollIntoView({ block: 'center' }); return __EV.hit(e); }", [rs, j])
        bn, bb = pn.ev(rd), pb.ev(rd)
        pn.click(atn, 500)
        pb.click(atb, 500)
        vn, vb = pn.ev(rd), pb.ev(rd)
        T('B5', '민법 첫 화면 단원 줄 의 「61x1」 글자 누름 = 바탕에서 수 글자 누름(아무 일 없음 · 화면 · 창 · 스크롤 무변)', atn and atn.get('on') and vn == bn and vb == bb and vn['home'],
          {'새 판 누른 곳': atn, '새 판 앞/뒤': [bn, vn], '바탕 앞/뒤': [bb, vb]})


def B4_jo(br, srcs):
    out = {}
    for tag, src in srcs:
        p = Pg(br, 'jo', tag + '_late', src, 1440, delay=DELAY)
        pre = p.ev("() => __EL.b4prep()")
        if tag == 'NEW':
            p.until("() => typeof EWM !== 'undefined' && EWM.st === 'ok' && document.querySelectorAll('#slot .mbdash .ewmn').length > 0 && !busy", 15000)
        else:
            p.until("() => typeof EWM !== 'undefined' && EWM.st === 'ok'", 15000)
        p.wait(1200)
        post = p.ev("() => __EL.b4after()")
        rows = None
        if tag == 'NEW':
            p.ev("([a, b]) => __EL.setMap(a, b)", [wr_of('특허법'), wr_of('특허법') + wx_of('특허법')])
            rows = {'dr': judge((p.ev("() => __EL.drawer()") or {}).get('rows'), round_exp(wr_of('특허법'))),
                    'da': judge((p.ev("() => __EL.dash()") or {}).get('rows'), round_exp(wr_of('특허법')))}
        out[tag] = {'pre': pre, 'post': post, 'rows': rows}
        p.close()
    n, b = out['NEW'], out.get('BASE')
    T('B4', '조판기 첫 화면이 먼저(1차객 첫 화면 시각 < 기록 받은 시각 · 받기 전 .ewmn 0)',
      n['pre']['eh']['tEx'] == 0 and n['pre']['nE'] == 0 and n['post']['eh']['tEx'] > n['pre']['tDash'] and n['pre']['st'] == 'wait',
      {'첫 화면 ms': n['pre']['tDash'], '기록 요청 ms': n['post']['eh']['tReq'], '받음 ms': n['post']['eh']['tEx'], '받기 전 EWM': n['pre']['st']})
    TB('B4', '조판기 받은 뒤 서랍 · 첫 화면에 「61x1 63x2」 나타남(render 길 · 값 = B1 셈)',
       lambda x: x['nDrawer'] > 0 and x['nDash'] > 0 and (x.get('rows') is None or (ok_rows(x['rows']['dr']) and ok_rows(x['rows']['da']))),
       {'nDrawer': n['post']['nDrawer'], 'nDash': n['post']['nDash'], 'rows': n['rows'] and {k: brief(v) for k, v in n['rows'].items()}},
       b and {'nDrawer': b['post']['nDrawer'], 'nDash': b['post']['nDash']})
    T('B4', '조판기 받은 뒤 스크롤 자리 그대로(첫 화면 · 서랍)', n['pre']['top'] == n['post']['top'] and n['pre']['dtop'] == n['post']['dtop'],
      {'새 판 첫 화면 앞/뒤': [n['pre']['sc'], n['pre']['top'], n['post']['top']], '서랍 앞/뒤': [n['pre']['ds'], n['pre']['dtop'], n['post']['dtop']],
       '바탕 첫 화면 앞/뒤': b and [b['pre']['top'], b['post']['top']], '바탕 서랍 앞/뒤': b and [b['pre']['dtop'], b['post']['dtop']]})


def B4_mb(br, srcs, QM, QMX):
    out = {}
    for tag, src in srcs:
        p = Pg(br, 'mb', tag + '_late', src, 1440, delay=DELAY)
        pre = p.ev("() => __ML.b4prep()")
        if tag == 'NEW':
            p.until("() => typeof EWM !== 'undefined' && EWM.st === 'ok' && document.querySelectorAll('#dashboard-container .ewmn').length > 0", 15000)
        else:
            p.until("() => typeof EWM !== 'undefined' && EWM.st === 'ok'", 15000)
        p.wait(1500)
        post = p.ev("() => __ML.b4after()")
        rows = None
        if tag == 'NEW':
            p.ev("([a, b]) => __ML.setMap(a, b)", [QM, QMX])
            ry = round_exp(wr_of('민법'))
            dc = p.ev("() => __ML.drawerCur()")
            rows = {'s': dc.get('s'), 'dr': judge(dc.get('rows'), ry), 'da': judge((p.ev("() => __ML.dash()") or {}).get('rows'), ry)}
        out[tag] = {'pre': pre, 'post': post, 'rows': rows}
        p.close()
    n, b = out['NEW'], out.get('BASE')
    T('B4', '민법 첫 화면이 먼저(첫 화면 시각 < 기록 받은 시각 · 받기 전 .ewmn 0)',
      n['pre']['eh']['tEx'] == 0 and n['pre']['nE'] == 0 and n['post']['eh']['tEx'] > n['post']['eh']['tReady'] > 0,
      {'첫 화면 ms': n['post']['eh']['tReady'], '요청 ms': n['post']['eh']['tReq'], '받음 ms': n['post']['eh']['tEx'], '받기 전 EWM': n['pre']['st']})
    TB('B4', '민법 받은 뒤 서랍 · 첫 화면에 「61x1 63x2」 제자리 칠함(ewmPaintAll · 값 = B1 셈)',
       lambda x: x['nDrawer'] > 0 and x['nDash'] > 0 and (x.get('rows') is None or (ok_rows(x['rows']['dr']) and ok_rows(x['rows']['da']))),
       {'nDrawer': n['post']['nDrawer'], 'nDash': n['post']['nDash'], 'rows': n['rows'] and {'서랍 과목': n['rows']['s'], 'dr': brief(n['rows']['dr']), 'da': brief(n['rows']['da'])}},
       b and {'nDrawer': b['post']['nDrawer'], 'nDash': b['post']['nDash']})
    T('B4', '민법 통째 다시 그리기 0(받은 뒤 renderDashboard 부름 0 · 첫 화면 마디 그대로)', n['post']['nRd'] == 0 and n['post']['keep'],
      {'새 판 부름': n['post']['nRd'], '보기': n['post']['rd'], '마디 그대로': n['post']['keep'], '바탕 부름': b and b['post']['nRd'], '바탕 마디': b and b['post']['keep']})
    T('B4', '민법 받은 뒤 스크롤 자리 그대로(창 · 서랍)', n['pre']['y'] == n['post']['y'] and n['pre']['ty'] == n['post']['ty'],
      {'새 판 창 앞/뒤': [n['pre']['y'], n['post']['y']], '서랍 앞/뒤': [n['pre']['ty'], n['post']['ty']], '바탕': b and [b['pre']['y'], b['post']['y'], b['pre']['ty'], b['post']['ty']]})


def B6_jo(pn, pb):
    law = '특허법'
    r = {}
    for p in (pn, pb):
        p.ev("o => __EL.go(o)", {'law': law, 'tab': 'jimun', 'jimunTab': 'ox', 'mok': None, 'oxQ': '', 'jtFold': False, 'jtCh': {}, 'mbCh': {}, 'omr': False})
        p.ev("([a, b]) => __EL.setMap(a, b)", [wr_of(law), wr_of(law) + wx_of(law)])
        hm = p.ev("() => __EV.cnt('#slot .mbhm')")
        pr = p.ev("() => __EL.b6rnd()")
        p.click(pr.get('at'), 600)
        rnd = p.ev("() => __EL.popCnt()")
        p.ev("o => __EL.go(o)", {'law': law, 'tab': 'jimun', 'jimunTab': 'gichul', 'year': '2026', 'omr': True})
        p.wait(300)
        omr = p.ev("() => __EV.cnt('.omrwrap')")
        p.ev("o => __EL.go(o)", {'law': law, 'tab': 'jimun', 'jimunTab': 'ox', 'year': None, 'mok': None, 'omr': False})
        r[p.tag] = {'히트맵': hm, '회독 비교': rnd, 'OMR': omr}
    for k in ('히트맵', '회독 비교', 'OMR'):
        a, b = r['NEW'][k], r['BASE'][k]
        T('B6', '조판기 %s 에 .ewmn 0 · 「-X」 수 = 바탕' % k, a and a['kids'] > 5 and a['n'] == 0 and b and a['x'] == b['x'], {'새 판': a, '바탕': b})


def B6_mb(pn, pb, QM, QMX):
    r = {}
    for p in (pn, pb):
        p.ev("([a, b]) => __ML.setMap(a, b)", [QM, QMX])
        p.ev("() => { document.querySelectorAll('.oxwin').forEach(x => x.remove()); try { goHome(); } catch (e) {} }")
        p.wait(300)
        hm = p.ev("() => __EV.cnt('#hm-section')")
        cm = p.ev("() => __ML.b6cmp()")
        p.wait(500)
        cmp = p.ev("() => __EV.cnt('#compare-body')")
        p.ev("() => { try { closeCompareModal(); } catch (e) { document.getElementById('compare-modal').classList.add('hide'); } }")
        p.ev("async () => { document.querySelectorAll('.oxwin').forEach(x => x.remove()); try { goHome(); } catch (e) {} startQuiz('변리사 기출', '2026년 제63회'); for (let i = 0; i < 200 && !document.querySelector('#quiz-container .exv-q'); i++) await new Promise(r => setTimeout(r, 100)); }")
        p.wait(400)
        p.ev("() => openOmrPad()")
        p.wait(600)
        omr = p.ev("() => __EV.cnt('#oxwin-omr')")
        p.ev("() => { document.querySelectorAll('.oxwin').forEach(x => x.remove()); try { goHome(); } catch (e) {} }")
        r[p.tag] = {'히트맵': hm, '회독 비교': cmp, 'OMR': omr, 'cmp': cm}
    for k in ('히트맵', '회독 비교', 'OMR'):
        a, b = r['NEW'][k], r['BASE'][k]
        T('B6', '민법 %s 에 .ewmn 0 · 「-X」 수 = 바탕' % k, a and a['kids'] > 5 and a['n'] == 0 and b and a['x'] == b['x'], {'새 판': a, '바탕': b, '비교 단원': r['NEW']['cmp'] if k == '회독 비교' else None})


def chk_ok(c):
    return c and c['n'] > 0 and not c['covN'] and not c['clipN'] and not c['ovlN'] and not c['offxN']


def scan_jo(p, w):
    """조판기 화면 넷(첫 화면 · 서랍 · 검색 · 기출뷰) — 겹침 · 잘림 · 높이 · 넘침 · 그림"""
    law, out = '특허법', {}
    phone = w <= 480
    p.ev("o => __EL.go(o)", {'law': law, 'tab': 'jimun', 'jimunTab': 'ox', 'mok': None, 'oxQ': '', 'jtFold': phone, 'jtCh': {}, 'mbCh': {}, 'omr': False})
    p.ev("() => __EL.mln()")
    p.ev("o => __EL.go(o)", {'law': law, 'tab': 'jimun', 'jimunTab': 'ox', 'mok': None, 'oxQ': '', 'jtFold': phone, 'jtCh': {}, 'mbCh': {}, 'omr': False})
    p.ev("([a, b]) => __EL.setMap(a, b)", [wr_of(law), wr_of(law) + wx_of(law)])
    FIT = "() => [...document.querySelectorAll('#slot .mbur.ewmfit')].map(r => __EV.txt(r.querySelector('.nm')).slice(0, 20))"
    out['첫 화면'] = {'chk': p.ev("(s) => __EV.chk(s)", '#slot .mbdash .ewmn'), 'h': p.ev("(s) => __EV.heights(s)", ['#slot .mbdash .mbur', '#slot .mbdash .mbch > .hh']),
                   'over': p.ev("() => __EV.over()"), 'fit': p.ev(FIT)}
    p.ev("(s) => __EV.toFirst(s)", '#slot .mbdash .mbur .ewmn')
    out['첫 화면']['shot'] = p.shot('dash')
    if w == 834:   # 폭만 바뀜(서랍 접기 = jtPaint 만 · render 없음) → ResizeObserver 다음 틀에 다시 잼
        p.ev("() => { S.jtFold = true; jtPaint(); }")
        p.wait(500)
        out['첫 화면(서랍 접어 폭 바뀜)'] = {'chk': p.ev("(s) => __EV.chk(s)", '#slot .mbdash .ewmn'), 'h': p.ev("(s) => __EV.heights(s)", ['#slot .mbdash .mbur', '#slot .mbdash .mbch > .hh']),
                                     'over': p.ev("() => __EV.over()"), 'fit': p.ev(FIT)}
        p.ev("() => { S.jtFold = false; jtPaint(); }")
        p.wait(500)
    if phone:
        p.ev("o => __EL.go(o)", {'jtFold': False})
    out['서랍'] = {'chk': p.ev("(s) => __EV.chk(s)", '#jtlist .ewmn'), 'h': p.ev("(s) => __EV.heights(s)", ['#jtlist > .jtch', '#jtlist > .jtit']), 'over': p.ev("() => __EV.over()")}
    p.ev("(s) => __EV.toFirst(s)", '#jtlist .jtit .ewmn')
    out['서랍']['shot'] = p.shot('drawer')
    p.ev("o => __EL.go(o)", {'jtFold': True if phone else False})
    p.ev("(x) => __EL.j5(x)", '63|13')
    out['검색'] = {'chk': p.ev("(s) => __EV.chk(s)", '.mbres .ewmx'), 'over': p.ev("() => __EV.over()")}
    p.ev("(s) => __EV.toFirst(s)", '.mbres .ewmx')
    out['검색']['shot'] = p.shot('search')
    p.ev("o => __EL.go(o)", {'oxQ': ''})
    p.ev("([y, n]) => __EL.exvAt(y, n)", ['2026', 13])
    out['기출뷰'] = {'chk': p.ev("(s) => __EV.chk(s)", '#slot .exv-head > .ewmx'), 'over': p.ev("() => __EV.over()")}
    p.ev("(s) => __EV.toFirst(s)", '#slot .exv-head > .ewmx')
    out['기출뷰']['shot'] = p.shot('exv')
    p.ev("o => __EL.go(o)", {'law': law, 'tab': 'jimun', 'jimunTab': 'ox', 'year': None, 'mok': None, 'omr': False, 'jtFold': phone})
    return out


def scan_mb(p, w, QM, QMX, subj):
    out = {}
    narrow = w < 900
    p.ev("([a, b]) => __ML.setMap(a, b)", [QM, QMX])
    p.ev("(n) => { document.querySelectorAll('.oxwin').forEach(x => x.remove()); try { goHome(); } catch (e) {} if (typeof trFold === 'function') trFold(n); }", narrow)
    p.wait(300)
    out['첫 화면'] = {'chk': p.ev("(s) => __EV.chk(s)", '#dashboard-container .ewmn'),
                   'h': p.ev("(s) => __EV.heights(s)", ['#dashboard-container [data-trrow]', '#dashboard-container [data-trchap]']), 'over': p.ev("() => __EV.over()")}
    p.ev("(s) => __EV.toFirst(s)", '#dashboard-container [data-trrow] .ewmn')
    out['첫 화면']['shot'] = p.shot('dash')
    p.ev("(s) => { if (typeof trFold === 'function') trFold(false); trPickSubj(s); }", subj)
    p.wait(250)
    out['서랍'] = {'chk': p.ev("(s) => __EV.chk(s)", '#trlist .ewmn'), 'h': p.ev("(s) => __EV.heights(s)", ['#trlist > .trch', '#trlist > .trit']), 'over': p.ev("() => __EV.over()")}
    p.ev("(s) => __EV.toFirst(s)", '#trlist .trit .ewmn')
    out['서랍']['shot'] = p.shot('drawer')
    p.ev("() => trPickSubj('변리사 기출')")
    p.wait(200)
    out['서랍 기출'] = {'chk': p.ev("(s) => __EV.chk(s)", '#trlist .ewmn'), 'h': p.ev("(s) => __EV.heights(s)", ['#trlist > .trit']), 'over': p.ev("() => __EV.over()")}
    p.ev("(s) => __EV.toFirst(s)", '#trlist .trit .ewmn')
    out['서랍 기출']['shot'] = p.shot('drawer_gi')
    p.ev("(s) => { trPickSubj(s); if (typeof trFold === 'function') trFold(innerWidth < 900); }", subj)
    qid = next((k for k, v in sorted(QM.items()) if '63|13' in v), None)
    p.ev("(q) => __ML.m5(q)", qid)
    out['검색'] = {'chk': p.ev("(s) => __EV.chk(s)", '#search-results .ewmx'), 'over': p.ev("() => __EV.over()")}
    p.ev("(s) => __EV.toFirst(s)", '#search-results .ewmx')
    out['검색']['shot'] = p.shot('search')
    p.ev("() => { const i = document.getElementById('search-input'); i.value = ''; runSearch(); }")
    p.ev("async () => { document.querySelectorAll('.oxwin').forEach(x => x.remove()); try { goHome(); } catch (e) {} startQuiz('변리사 기출', '2026년 제63회'); for (let i = 0; i < 200 && !document.querySelector('#quiz-container .exv-q'); i++) await new Promise(r => setTimeout(r, 100)); }")
    p.ev("(k) => __ML.m6at(k)", '2026:13')
    p.wait(250)
    out['기출뷰'] = {'chk': p.ev("(s) => __EV.chk(s)", '#quiz-container .exv-head > .ewmx'), 'over': p.ev("() => __EV.over()")}
    p.ev("(s) => __EV.toFirst(s)", '#quiz-container .exv-head > .ewmx')
    out['기출뷰']['shot'] = p.shot('exv')
    p.ev("() => { document.querySelectorAll('.oxwin').forEach(x => x.remove()); try { goHome(); } catch (e) {} }")
    return out


def B5_B7(br, app, srcs, pages, QM=None, QMX=None):
    subj = None
    if app == 'mb':
        subj = pages['NEW'].ev("() => { const q = quizData.find(x => (x.examMeta || []).some(m => String(m.year) === '2026' && +m.no === 13)); return q ? q.subject : null; }")
    for w in WIDTHS:
        res = {}
        for tag, src in srcs:
            p = pages[tag] if w == 1440 else Pg(br, app, tag + '_%d' % w, src, w)
            if w != 1440:
                p.ewm_ok()
            res[tag] = scan_jo(p, w) if app == 'jo' else scan_mb(p, w, QM, QMX, subj)
            if w != 1440:
                p.close()
        n, b = res['NEW'], res.get('BASE')
        for scr, v in n.items():
            T('B7', '%s %d %s — 「%s」 %d개 겹침 · 잘림 · 가려짐 · 화면 밖 0 · 가로 넘침 %s(바탕 %s)' % (
                NAME[app], w, scr, '61x1' if scr.startswith(('첫 화면', '서랍')) else '63-13-X', (v['chk'] or {}).get('n', 0),
                v['over']['sw'] - v['over']['iw'], b and b[scr]['over']['sw'] - b[scr]['over']['iw']),
              chk_ok(v['chk']) and (v['over']['sw'] <= v['over']['iw'] or (b and v['over']['sw'] <= b[scr]['over']['sw'])),
              {'chk': v['chk'], 'over': v['over'], 'shot': os.path.basename(v.get('shot') or ''), '한 줄로 맞춘 줄(.ewmfit)': v.get('fit')})
            if 'h' in v and b:
                c = hcmp(v['h'], b[scr]['h'])
                T('B5', '%s %d %s 줄 높이 = 바탕 ±1px(.ewmn 있는 줄)' % (NAME[app], w, scr), h_ok(c), c)
        if w == 390:
            T('B5', '%s 390 가로 넘침 0(화면 넷)' % NAME[app], all(v['over']['sw'] <= v['over']['iw'] for v in n.values()),
              {k: [v['over']['sw'], v['over']['iw']] for k, v in n.items()})


def census(app):
    """자리 수 — 새 판 글에서 ewm_list 자리 표지 셈(★ ewm_list)"""
    s = app_src(app, NEWA[app]) or ''
    return len(re.findall(r'★ ewm_list', s))


def main():
    os.makedirs(TMPD, exist_ok=True)
    srcs = {}
    for app in APPS:
        sn, sb = app_src(app, NEWA[app]), app_src(app, BASE)
        srcs[app] = [('NEW', sn)] + ([('BASE', sb)] if sb else [])
        print('INFO | %s 새 판 md5(LF) %s · %s B · 바탕 %s md5(LF) %s · %s B' % (NAME[app], md5lf(sn), len(sn.encode('utf-8')), BASE,
              sb and md5lf(sb), sb and len(sb.encode('utf-8'))), flush=True)
    QM, QMX = mb_maps() if 'mb' in APPS else ({}, {})
    N('기록', '지어낸 시험 기록(하네스 실행 중 · 파일 없음)', {'틀림 줄': ['%s %d-%d' % (x['s'], x['r'], x['i']) for x in WR],
                                                   '뺀 줄': ['%s %d-%d %s' % (x['s'], x['r'], x['i'], x['why']) for x in WX]})
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for app in APPS:
            t1 = time.time()
            pages = {tag: Pg(br, app, tag, src, 1440) for tag, src in srcs[app]}
            for p in pages.values():
                st = p.ewm_ok()
                N('B0', '%s %s 기록 받기 EWM.st' % (NAME[app], p.tag), st)
            pn, pb = pages['NEW'], pages.get('BASE')
            STEP.append(('%s 쪽 열기' % NAME[app], round(time.time() - t1)))
            for gk, fn in (('B1', lambda: B1_B2_jo(pn, pb) if app == 'jo' else B1_B2_mb(pn, pb, QM, QMX)),
                           ('B3', lambda: B3_jo(pn, pb) if app == 'jo' else B3_mb(pn, pb, QM)),
                           ('B6', lambda: B6_jo(pn, pb) if app == 'jo' else B6_mb(pn, pb, QM, QMX)),
                           ('B5', lambda: (B5_style(pn, pb, app), B5_click_jo(pn, pb) if app == 'jo' else B5_click_mb(pn, pb))),
                           ('B7', lambda: B5_B7(br, app, srcs[app], pages, QM, QMX)),
                           ('B4', lambda: B4_jo(br, srcs[app]) if app == 'jo' else B4_mb(br, srcs[app], QM, QMX))):
                if not (want(gk) or (gk == 'B1' and want('B2'))):
                    continue
                t2 = time.time()
                try:
                    fn()
                except Exception as e:
                    T(gk, '%s %s 실행 오류' % (NAME[app], gk), False, traceback.format_exc()[-1500:])
                STEP.append(('%s %s' % (NAME[app], gk), round(time.time() - t2)))
            for p in pages.values():
                p.close()
        br.close()
    base_msgs = {re.sub(r' @\d*$', '', m) for k, v in ERRS.items() if ' BASE' in k for m in v}
    for k, v in ERRS.items():
        if ' NEW' in k:
            own = [m for m in v if re.sub(r' @\d*$', '', m) not in base_msgs]
            T('B0', '%s 페이지 오류 0(바탕에도 같은 글로 나는 오류는 값만 · %d)' % (k, len(v) - len(own)), not own, {'새 판만': own[:5], '바탕과 같음': sorted({m for m in v if m not in own})[:3]})
        else:
            N('B0', '%s 페이지 오류' % k, v[:5])
    n_pass = sum(1 for r in RES if r[2] is True)
    n_fail = sum(1 for r in RES if r[2] is False)
    y_bad = [y for y in YARD if y[2]]
    lines = ['', '=' * 100, '_harness_ewm_list — PASS %d · FAIL %d · INFO %d · %d초' % (n_pass, n_fail, sum(1 for r in RES if r[2] is None), round(time.time() - T0)),
             '헛잣대(바탕 %s · 같은 차례 · FAIL 이어야 함): %d 칸 중 바탕이 통과한 칸 %d' % (BASE, len(YARD), len(y_bad))]
    lines += ['  바탕 통과(헛잣대 실패): %s · %s' % (g, nm) for g, nm, _ in y_bad]
    lines += ['자리 수(★ ewm_list 표지): ' + ' · '.join('%s %d' % (NAME[a], census(a)) for a in APPS)]
    lines += ['단계별 초: ' + ' · '.join('%s %d' % s for s in STEP)]
    lines += ['FAIL: %s · %s' % (r[0], r[1]) for r in RES if r[2] is False]
    print('\n'.join(lines), flush=True)
    os.makedirs(os.path.dirname(OUTF), exist_ok=True)
    with open(OUTF, 'w', encoding='utf-8') as f:
        for g, nm, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ('INFO' if ok is None else ('PASS' if ok else 'FAIL'), g, nm, _s(d)))
        f.write('\n'.join(lines) + '\n')
    print('결과 파일: %s · 그림: %s' % (OUTF, SHOTS), flush=True)
    return 0 if not n_fail and not y_bad else 1


if __name__ == '__main__':
    sys.exit(main())
