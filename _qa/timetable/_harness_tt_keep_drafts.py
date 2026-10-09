# -*- coding: utf-8 -*-
r"""tt앱 — 본문 입력칸에 쓰던 글이 동기화 재그림에 사라지지 않게(포커스 없어도) 관문 (_task_tt_keep_drafts §B 관문 1~7 · 2026-10-09)

  python _harness_tt_keep_drafts.py [--mode gate|regress|smoke] [--new <앱 html>] [--base <git 판 | 앱 html>] [--res <결과 파일>]
                                    [--only K1a,K3,…] [--engines chromium,webkit]

  NEW  = 이 판 앱(기본 GENIE_ROOT timetable/index.html — 사슬 실행기·워크트리가 GENIE_ROOT 를 준다 · 없으면 _roots.genie())
  BASE = 헛잣대(기본 genie git 4e78d4f = 9/6 keepInput 길 · 포커스 칸만 되살림 · md5 b7d720e2) — gate 에서만 띄운다
  기기 = Chromium PC 1100×800 · Chromium 폰 390(hasTouch · 톡) → 그 브라우저를 닫고 WebKit 폰 390(진짜 터치 톡) — 브라우저는 한 번에 하나 · 판(NEW/BASE)·기기마다 새 문맥
  앱 자리 = https://api.github.com/__tt/timetable/index.html 을 route 가 내준다(GitHub API 와 같은 출처라 CORS 없음) · 진짜 網은 통째로 막음(manifest · 아이콘만 빈 것으로)
  가짜 GitHub(route · 문맥마다 메모리) = contents GET(있으면 {sha,content} · 없으면 404) · PUT(받아 둠)
     원격 변경 = todos/공통.json(늘 동기화되는 파일) + share.json(share 화면일 때)에 상대(햄찌) 새 항목 하나씩
  시드(init script · 앱 스크립트보다 먼저) = 날짜 고정 2026-10-09 12:00 KST · confirm/alert/prompt 스텁 · error·unhandledrejection 모음
     · localStorage(토큰 없음 — 부팅 동기화를 막고 부팅 뒤에 켬 · tt_race 선례) · share.json(txt 1 · app 1 · ai 1) · plan v1(활동 1) · food 1
  재그림 표지 = 동기화 전에 #main 첫 자식에 data-hk 를 달고 끝난 뒤 사라졌는지 + 원격 항목이 로컬 파일에 들어왔는지(그림이 안 바뀐 PASS 는 없다)
     · 「포커스 뺌」은 누른 뒤 activeElement 가 그 칸이 아님을 재고(웹킷 톡이 포커스를 못 빼면 blur() 로 · 값에 적음 — 10/9 잼: 웹킷은 누를 거리 없는 글자 톡에
       포커스가 안 빠짐 · 칩 톡엔 빠짐) · 동기화 직전 칸 값 = 친 글을 잰다(표본 0 PASS 없음)
  관문(지시서 §B):
     K1a/K1b 관문 1 — share Text shT 글 → (a) Text 탭 칩(쓰는 칸 옆 이름 칩 · render 안 부름) (b) 빈 곳 눌러 포커스 뺌 → 원격 share.json 새 항목 syncAll → 글 그대로
     K2      관문 2 — 포커스 둔 채 = 글 · 커서(2,2) · 포커스 그대로(9/6 관문)
     K3      관문 3 — 「올리기」 = 칸 빔 · 항목 1 · 다음 syncAll 두 번 뒤에도 빈 채 · 되살아남 0(폰 = 톡 · 웹킷 = 진짜 터치 톡)
     K4      관문 4 — (폰) 글 → 포커스 뺌 → 숨김 → 원격 변경 → 보임(visibilitychange → 앱이 syncAll) → 글 그대로
     K5-n    관문 5 — §0-5 칸마다(묶음별로 한 번에 치고 포커스 뺌 → 원격 변경 syncAll → 칸마다 그대로) · K5-ns = 그 칸의 저장/올리기 뒤 빈 칸(미리 채운 칸은 저장값)
     K6-n    관문 6 — §A-3 표 처리기(await 뒤 render) 1 shareAddImg(shF 비움) 2 설정 「저장 후 동기화」(tok = 저장값) · 2b 그 재그림에도 다른 칸(시험 이름) 초고 그대로
             3 foodSave(모달 · 다시 열면 빈 칸) — 2 · 2b 는 K5 설정 묶음 안에서 잰다(같은 칸을 씀)
     K7      관문 7 — 화면 훑기(share 네 탭 · 계획 주차별·리스트 · 설정 · 일간 · 할일 · Archive) 오류 0 · K8 = 그 문맥 끝까지 오류 0
     INFO    K1x = shcat 칩(전체…) 누름 = 그 누름의 재그림(_inUi · 사용자 조작 안 render)이라 초고가 지워짐(바탕과 같음 · 지시서 「_inUi 규칙 그대로」)
             K5x = lsInline 칸 수정 중(포커스 둔 채) 동기화 재그림 — render 가 그 칸을 다시 만들지 않아 id 로 못 살림(엔진별 결과를 적음 ·
                   10/9 잼: 크롬 = 지울 때 blur → lsSet 이 저장하나 칸 글자는 옛 이름 · 웹킷 = 사라짐 · 바탕과 같음)
  헛잣대(gate) = 같은 잣대를 BASE 에 돌린 줄은 「BASE <기기> · <칸>」(사슬 b=1 · 판정 밖) · 바탕에서 FAIL 이어야 할 칸(K1a · K1b · K4 · K5 의 id 칸)은
     「<칸>-헛 <기기>」 줄이 바탕 FAIL 이면 PASS(잣대가 가름) · 바탕도 PASS 이면 FAIL
  모드 = gate(NEW + BASE · 결과 N:\개인\claude\timetable\_tt_keep_drafts\result.txt) · regress(NEW 만 · 결과 %TEMP%\h_tt_keep_drafts) · smoke(NEW · PC · K1a · K3 · K8)
  ⚠ 고정 대기 없음 — 앱 표지(syncing · _inUi · 재그림 표지 · 항목 수)를 기다린다(QC.until) · 웹킷은 지울 때 blur 가 안 뜨고 크롬은 뜬다(K5x 참고)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — 실행 모드 --mode gate|regress|smoke(없으면 gate) · import 때 --mode · --snap-in · --snap-out 을 sys.argv 에서 뗀다
import base64, collections, datetime, hashlib, json, os, struct, subprocess, sys, tempfile, time, traceback, urllib.parse, zlib   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEWF = ARG('--new', _roots.genie('timetable', 'index.html'))
BASE = ARG('--base', '4e78d4f')
BASE_MD5 = 'b7d720e2fc51d617f3cff567525b59ea'   # 지시서 §0 — 4e78d4f(= cab7b5a 와 같은 바이트) timetable/index.html 523,169 B
ONLY = [x.strip() for x in (ARG('--only', '') or '').split(',') if x.strip()]
ENGINES = [x.strip() for x in (ARG('--engines', 'chromium,webkit') or '').split(',') if x.strip()]
DEVS = [x.strip() for x in (ARG('--devs', '') or '').split(',') if x.strip()]   # 기기만 골라 돌릴 때(예 chromium-pc)
_TMPD = os.path.join(tempfile.gettempdir(), 'h_tt_keep_drafts')
if QC.GATE:
    _nres = _roots.n('timetable', '_tt_keep_drafts', 'result.txt')
    RES = ARG('--res', _nres or os.path.join(_TMPD, 'result.txt'))
else:
    RES = ARG('--res', os.path.join(_TMPD, 'result.txt'))

APP_URL = 'https://api.github.com/__tt/timetable/index.html'
GH = 'https://api.github.com/repos/zzikkaplan/studyplandata/contents/'
ME, OT = '꼬까', '햄찌'
T0 = int(datetime.datetime(2026, 10, 9, 9, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))).timestamp() * 1000)

DEV = {
    'chromium-pc': ('chromium', dict(viewport={'width': 1100, 'height': 800})),
    'chromium-phone': ('chromium', dict(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2)),
    'webkit-phone': ('webkit', dict(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2)),
}
PLAN = {   # 기기마다 돌릴 관문(차례대로) — K7 은 첫머리(갓 띄운 화면) · K8 은 끝
    'chromium-pc': ['K7', 'K1a', 'K1b', 'K1x', 'K2', 'K3', 'K5', 'K5x', 'K6', 'K8'],
    'chromium-phone': ['K7', 'K1a', 'K1b', 'K2', 'K3', 'K4', 'K5', 'K5x', 'K8'],
    'webkit-phone': ['K7', 'K1a', 'K1b', 'K2', 'K3', 'K4', 'K5x', 'K8'],
}
SMOKE_PLAN = {'chromium-pc': ['K1a', 'K3', 'K8']}

# ════════════════════ 시드 ════════════════════
SHARE0 = {'v': 1, 'items': [
    {'id': 't1', 'ty': 'txt', 'text': '씨앗 글 하나', 'by': OT, 'grp': '', 'at': T0, 'u': T0, 'del': False, 'cm': []},
    {'id': 'a1', 'ty': 'app', 't': 'tt', 'by': ME, 'at': T0 + 1, 'u': T0 + 1, 'del': False},
    {'id': 'p1', 'ty': 'ai', 't': '씨앗 클로드 글', 'apps': ['a1'], 'pin': 0, 'done': 0, 'by': OT, 'at': T0 + 2, 'u': T0 + 2, 'del': False, 'cm': []},
]}
PLAN_V1 = {'v': 1, 'weekStart': '2026-08-03', 'bands': [
    {'id': 'b1', 's': '민법', 'tag': '', 'name': '객1회독', 'w1': 10, 'w2': 12, 'per': 2, 'units': [], 'note': '', 'u': 1, 'del': False}]}
FOOD0 = {'v': 1, 'items': [{'id': 'f1', 'name': '김치볶음밥', 'date': '2026-10-01', 'recipe': '밥 김치', 'note': '', 'imgs': [], 'thumb': '',
                            'by': ME, 'u': 1, 'del': False}]}
COMMON0 = {'v': 1, 'items': []}
SEED = {
    'tt.cfg': {'person': ME, 'token': '', 'lastSync': 0},
    'tt.ui': {'view': 'share', 'shareTab': 'txt', 'date': None, 'galMonth': None},
    'tt.f.share/share.json': {'data': SHARE0, 'sha': 'r0', 'dirty': False},
    'tt.f.plan/' + ME + '.json': {'data': PLAN_V1, 'sha': None, 'dirty': False},
    'tt.f.food/food.json': {'data': FOOD0, 'sha': 'r0', 'dirty': False},
    'tt.f.todos/공통.json': {'data': COMMON0, 'sha': 'r0', 'dirty': False},
}
REMOTE0 = {'share/share.json': SHARE0, 'todos/공통.json': COMMON0, 'food/food.json': FOOD0}

INIT_JS = r"""(() => {
 if (!String(location.href).startsWith('https://api.github.com/__tt/')) return;
 if (window.__hk) return;
 const R = Date; const OFF = new R('2026-10-09T12:00:00+09:00').getTime() - R.now();
 function D(...a) { return a.length ? new R(...a) : new R(R.now() + OFF) }
 D.prototype = R.prototype; D.now = () => R.now() + OFF; D.parse = R.parse; D.UTC = R.UTC; window.Date = D;
 window.__errs = [];
 addEventListener('error', e => __errs.push('error: ' + String(e.message) + ' @' + (e.lineno || '')));
 addEventListener('unhandledrejection', e => __errs.push('rejection: ' + String((e.reason && e.reason.message) || e.reason)));
 window.confirm = () => true; window.alert = () => {}; window.prompt = () => null;
 try { if (!sessionStorage.getItem('__hk_seed')) { localStorage.clear(); const S = __SEED__;
   Object.keys(S).forEach(k => localStorage.setItem(k, JSON.stringify(S[k]))); sessionStorage.setItem('__hk_seed', '1'); } } catch (e) { __errs.push('seed: ' + e.message) }
 window.__hk = {
  q: s => document.querySelector(s),
  val: s => { const e = document.querySelector(s); return e ? e.value : null },
  act: () => { const a = document.activeElement; return a ? (a.id || a.tagName) : null },
  isAct: s => { const e = document.querySelector(s); return !!e && document.activeElement === e },
  mark: () => { const m = document.getElementById('main'); const c = m && m.firstElementChild; if (c) c.setAttribute('data-hk', '1'); return !!c },
  rendered: () => !document.querySelector('#main [data-hk]'),
  lf: p => { try { return JSON.parse(localStorage.getItem('tt.f.' + p) || 'null') } catch (e) { return null } },
  items: p => { const f = __hk.lf(p); return (f && f.data && f.data.items) || [] },
  has: (p, id) => __hk.items(p).some(x => x.id === id),
  vis: h => { Object.defineProperty(document, 'hidden', { configurable: true, get: () => h });
   Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => h ? 'hidden' : 'visible' });
   document.dispatchEvent(new Event('visibilitychange')) },
  mainText: () => (document.getElementById('main') || {}).textContent || '',
 };
})();"""
BOOT_JS = ("() => typeof render === 'function' && typeof syncAll === 'function' && typeof keepInputGrab === 'function' && !!window.__hk"
           " && !!document.getElementById('main') && document.getElementById('main').children.length > 0")
# 화면 옮기기(사용자 조작 밖 render) — 모달 걷기 · #main 글 칸을 그려진 값으로 되돌림(앞 관문 초고 치우기) · 포커스 빼기 · 메모리 상태 맞춤
GOTO_JS = r"""(a) => {
 document.querySelectorAll('.modal').forEach(m => m.remove());
 document.querySelectorAll('#main input, #main textarea').forEach(e => { if (!/^(checkbox|radio|file|button|submit|hidden|range|color)$/i.test(e.type)) e.value = e.defaultValue; });
 if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
 aiDraft = ''; aiNewOn = a.aiNew ? 1 : 0; shCmOpen = Object.assign({}, a.cm || {});
 Object.assign(ui, a.ui || {}); ui.view = a.view; if (a.view === 'share' && !(a.ui && a.ui.shareCat)) ui.shareCat = 'all';
 LS.set('tt.ui', ui); render(); return true }"""


def _png1():
    raw = b'\x00\xff\x00\x00'   # 1×1 빨강(필터 0)
    def ch(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    return b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)) + ch(b'IDAT', zlib.compress(raw)) + ch(b'IEND', b'')


PNG1 = _png1()


def b64json(d):
    return base64.b64encode(json.dumps(d, ensure_ascii=False).encode('utf-8')).decode('ascii')


# ════════════════════ 결과 ════════════════════
LINES, ROWS = [], []
SMOKE_IDS = ('K1a', 'K3', 'K8')


def out(s):
    print(s, flush=True)
    LINES.append(s)


def J(v, n=1200):
    return json.dumps(v, ensure_ascii=False, default=str)[:n]


def rec(S, cid, ok, title, val, hut=False, info=False):
    st = 'INFO' if info else ('PASS' if ok else 'FAIL')
    if S.base:
        line = '%s | BASE %s · %s %s | %s' % (st, S.dev, cid, title, J(val))
    else:
        line = '%s | %s %s · %s | %s' % (st, cid, S.dev, title, J(val))
    ROWS.append(dict(cid=cid, dev=S.dev, side='base' if S.base else 'new', st=st, title=title, hut=hut, info=info))
    out(line)
    return ok


# ════════════════════ 가짜 GitHub · 문맥 ════════════════════
class FakeGH(object):
    def __init__(self, app):
        self.app = app
        self.files = {p: {'sha': 'r0', 'b64': b64json(d)} for p, d in REMOTE0.items()}
        self.k = 0
        self.gets = collections.Counter()
        self.puts = []
        self.blocked = []

    def data(self, p):
        f = self.files.get(p)
        if not f:
            return None
        try:
            return json.loads(base64.b64decode(f['b64']).decode('utf-8'))
        except Exception:
            return None

    def change(self, n, share=True):
        def add(p, it):
            d = self.data(p) or {'v': 1, 'items': []}
            d.setdefault('items', []).append(it)
            self.k += 1
            self.files[p] = {'sha': 'r%d' % self.k, 'b64': b64json(d)}
        add('todos/공통.json', {'id': 'rc%d' % n, 't': '원격 공통 %d' % n, 'due': '', 'who': [ME, OT], 'by': OT, 'at': '2026-10-09',
                                'done': False, 'doneAt': None, 'del': False, 'u': T0 + n * 60000})
        if share:
            add('share/share.json', {'id': 'rs%d' % n, 'ty': 'txt', 'text': '원격 글 %d' % n, 'by': OT, 'grp': '', 'at': T0 + n * 60000,
                                     'u': T0 + n * 60000, 'del': False, 'cm': []})

    def handle(self, route):
        try:
            self._handle(route)
        except Exception as e:   # 문맥이 닫히는 중 등 — 막고 지나감
            try:
                route.abort()
            except Exception:
                pass

    def _handle(self, route):
        req = route.request
        u = req.url
        if u.startswith('blob:') or u.startswith('data:'):
            return route.continue_()   # 웹킷은 blob: 도 route 에 태운다(메모 playwright-webkit-routes-blob-urls)
        bu = u.split('#')[0].split('?')[0]
        if bu == APP_URL:
            return route.fulfill(status=200, content_type='text/html; charset=utf-8', body=self.app)
        if bu.startswith(GH):
            p = urllib.parse.unquote(bu[len(GH):])
            if req.method == 'GET':
                self.gets[p] += 1
                f = self.files.get(p)
                if f is None:
                    return route.fulfill(status=404, content_type='application/json', body='{"message":"Not Found"}')
                return route.fulfill(status=200, content_type='application/json', body=json.dumps({'sha': f['sha'], 'content': f['b64']}))
            if req.method == 'PUT':
                body = json.loads(req.post_data or '{}')
                self.k += 1
                sha = 'w%d' % self.k
                self.files[p] = {'sha': sha, 'b64': body.get('content', '')}
                self.puts.append(p)
                return route.fulfill(status=200, content_type='application/json', body=json.dumps({'content': {'sha': sha}}))
            return route.fulfill(status=405, body='')
        if bu.endswith('manifest.webmanifest'):
            return route.fulfill(status=200, content_type='application/manifest+json', body='{}')
        if bu.endswith('.png'):
            return route.fulfill(status=200, content_type='image/png', body=PNG1)
        self.blocked.append(bu[:120])
        return route.abort()


class Sess(object):
    def __init__(self, browser, dev, app, base):
        self.dev, self.base = dev, base
        eng, opt = DEV[dev]
        self.touch = bool(opt.get('has_touch'))
        try:
            self.ctx = browser.new_context(service_workers='block', locale='ko-KR', timezone_id='Asia/Seoul', **opt)
        except Exception:   # is_mobile 을 못 받는 엔진이면 빼고
            o2 = dict(opt)
            o2.pop('is_mobile', None)
            self.ctx = browser.new_context(service_workers='block', locale='ko-KR', timezone_id='Asia/Seoul', **o2)
        self.gh = FakeGH(app)
        self.ctx.route('**/*', self.gh.handle)
        self.ctx.add_init_script(INIT_JS.replace('__SEED__', json.dumps(SEED, ensure_ascii=False)))
        self.page = self.ctx.new_page()
        self.page.set_default_timeout(15000)
        self.perr, self.cerr = [], []
        self.page.on('pageerror', lambda e: self.perr.append(str(e)[:300]))
        self.page.on('console', lambda m: self.cerr.append(m.text[:300]) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
        self.n = 0
        QC.launch('base' if base else 'new')
        self.page.goto(APP_URL, wait_until='load')
        self.booted = QC.until(self.page, BOOT_JS, 20000, '부팅')
        if self.booted:
            self.page.evaluate("() => { cfg.token = 't_harness'; LS.set('tt.cfg', cfg); return cfg.token }")

    def errs(self):
        e = self.page.evaluate("() => (window.__errs || []).slice()")
        return e + ['pageerror: ' + x for x in self.perr] + ['console: ' + x for x in self.cerr]

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


# ════════════════════ 손 · 재기 ════════════════════
def sel_of(fid):
    return '[id="%s"]' % fid


def val(S, sel):
    return S.page.evaluate("(s) => __hk.val(s)", sel)


def act(S):
    return S.page.evaluate("() => __hk.act()")


def is_act(S, sel):
    return S.page.evaluate("(s) => __hk.isAct(s)", sel)


def loc(S, sel):
    if isinstance(sel, tuple):   # (css, 글 포함)
        return S.page.locator(sel[0], has_text=sel[1]).first
    return S.page.locator(sel).first


def press(S, sel):
    l = loc(S, sel)
    l.scroll_into_view_if_needed(timeout=8000)
    if S.touch:
        l.tap(timeout=8000)
    else:
        l.click(timeout=8000)
    return 'tap' if S.touch else 'click'


def goto(S, view, ui=None, cm=None, ai_new=False, wait_sel=None):
    S.page.evaluate(GOTO_JS, {'view': view, 'ui': ui or {}, 'cm': cm or {}, 'aiNew': bool(ai_new)})
    if wait_sel:
        QC.until(S.page, "(s) => !!document.querySelector(s)", 8000, '화면 ' + view, arg=wait_sel)
    QC.until(S.page, "() => _inUi === false", 5000, '_inUi 풀림')


def focus_field(S, sel):
    m = press(S, sel)
    if not is_act(S, sel):
        loc(S, sel).focus()
        m += '+focus()'
    return m


def put(S, sel, text, how):
    m = focus_field(S, sel)
    if how == 'type':
        S.page.keyboard.insert_text(text)
    else:   # fill — 날짜·시각·숫자 · 미리 채운 칸(값을 갈아 끼움)
        loc(S, sel).fill(text)
    return m


def blur_away(S, blank, sels):
    m = press(S, blank)
    if any(is_act(S, s) for s in sels):
        S.page.evaluate("() => document.activeElement.blur()")
        m += '+blur()'
    return m, act(S)


def sync(S, share=True, trigger='call'):
    """원격 변경 하나 → syncAll(또는 visibilitychange) → 재그림 표지 · 원격 항목 들어옴까지 기다림"""
    S.n += 1
    n = S.n
    pg = S.page
    pg.evaluate("() => { try { clearTimeout(syncT) } catch (e) {} return 1 }")
    QC.until(pg, "() => !syncing && _inUi === false", 20000, '동기화 빔')
    pg.evaluate("() => __hk.mark()")
    S.gh.change(n, share)
    if trigger == 'call':
        pg.evaluate("() => syncAll(true)")
    else:   # 'vis' — 보임(앱이 돌아옴) → 앱 visibilitychange → syncAll(true)
        pg.evaluate("() => __hk.vis(false)")
    ok = QC.until(pg, "(n) => !syncing && __hk.rendered() && __hk.has('todos/공통.json', 'rc' + n)", 20000, '원격 변경 → 재그림', arg=n)
    st = pg.evaluate("(n) => ({rendered: __hk.rendered(), applied: __hk.has('todos/공통.json', 'rc' + n)})", n)
    st['n'] = n
    st['wait'] = ok
    return st


def sync_ok(st):
    return bool(st.get('rendered') and st.get('applied'))


def refill(S, sel, v, how):
    """저장 칸 재기 전 — 앞 단계에서 글이 사라졌으면(바탕) 다시 넣는다(저장 뒤 빈 칸 잣대를 앞 단계와 떼어 잼)"""
    if val(S, sel) == v:
        return False
    put(S, sel, v, how)
    return True


# ════════════════════ 관문 ════════════════════
def k1(S, cid, blank, label):
    goto(S, 'share', {'shareTab': 'txt'}, wait_sel='#shT')
    T = '쓰던 글 %s %s' % (cid, S.dev)
    m1 = put(S, '#shT', T, 'type')
    m2, a1 = blur_away(S, blank, ['#shT'])
    pre = val(S, '#shT')
    st = sync(S)
    after, a2 = val(S, '#shT'), act(S)
    shown = S.page.evaluate("(n) => __hk.mainText().indexOf('원격 글 ' + n) >= 0", st['n'])
    ok = sync_ok(st) and shown and pre == T and a1 != 'shT' and after == T and a2 != 'shT'
    rec(S, cid, ok, 'share Text shT 글 → %s 눌러 포커스 뺌 → 원격 share.json 새 항목 syncAll → 글 그대로(포커스는 안 되살림)' % label,
        dict(typed=T, before_sync=pre, focus=m1, blur=m2, active_after_blur=a1, sync=st, remote_item_shown=shown, after=after, active_after=a2), hut=True)


def k1x(S):
    goto(S, 'share', {'shareTab': 'txt'}, wait_sel='#shT')
    T = '칩 누름 시험 글'
    put(S, '#shT', T, 'type')
    m = press(S, '#main .shcat span')   # 「전체」 칩 — shareCatSet → render(사용자 조작 안)
    after = val(S, '#shT')
    rec(S, 'K1x', None, 'share Text shT 글 → shcat 「전체」 칩 누름(그 누름의 render = _inUi) → 칸 글 = %s' % ('그대로' if after == T else '지워짐'),
        dict(typed=T, press=m, after=after), info=True)


def k2(S):
    goto(S, 'share', {'shareTab': 'txt'}, wait_sel='#shT')
    T = '커서 시험 글 K2'
    m = put(S, '#shT', T, 'type')
    S.page.evaluate("() => { const e = document.getElementById('shT'); e.setSelectionRange(2, 2); return 1 }")
    pre, a1 = val(S, '#shT'), act(S)
    st = sync(S)
    after, a2 = val(S, '#shT'), act(S)
    selr = S.page.evaluate("() => { const e = document.getElementById('shT'); return e ? [e.selectionStart, e.selectionEnd] : null }")
    ok = sync_ok(st) and pre == T and a1 == 'shT' and after == T and a2 == 'shT' and selr == [2, 2]
    rec(S, 'K2', ok, 'share Text shT 포커스 둔 채 원격 변경 syncAll → 글·커서(2,2)·포커스 그대로(9/6 관문)',
        dict(typed=T, focus=m, before_sync=pre, active_before=a1, sync=st, after=after, active_after=a2, sel=selr))


def k3(S):
    goto(S, 'share', {'shareTab': 'txt'}, wait_sel='#shT')
    T = '올리기 시험 글 K3 %s' % S.dev
    put(S, '#shT', T, 'type')
    m = press(S, '#main button[onclick="shareAddText()"]')
    cnt = "(t) => shareItems('txt').filter(x => x.text === t).length"
    QC.until(S.page, "(t) => shareItems('txt').some(x => x.text === t)", 8000, '올린 항목', arg=T)
    a0, c0 = val(S, '#shT'), S.page.evaluate(cnt, T)
    st1 = sync(S)
    a1, c1 = val(S, '#shT'), S.page.evaluate(cnt, T)
    pushed = any(x.get('text') == T for x in ((S.gh.data('share/share.json') or {}).get('items') or []))
    st2 = sync(S)
    a2, c2 = val(S, '#shT'), S.page.evaluate(cnt, T)
    ok = a0 == '' and c0 == 1 and sync_ok(st1) and a1 == '' and c1 == 1 and pushed and sync_ok(st2) and a2 == '' and c2 == 1
    rec(S, 'K3', ok, 'share Text 「올리기」(%s) = 칸 빔 · 항목 1 · syncAll 두 번 뒤에도 빈 채(되살아남 0) · 원격에 올라감' % m,
        dict(text=T, after_post=a0, n_post=c0, sync1=st1, after_sync1=a1, n1=c1, pushed=pushed, sync2=st2, after_sync2=a2, n2=c2))


def k4(S):
    goto(S, 'share', {'shareTab': 'txt'}, wait_sel='#shT')
    T = '앱 나갔다 온 글 K4 %s' % S.dev
    put(S, '#shT', T, 'type')
    m, a1 = blur_away(S, '#main .ttl > b', ['#shT'])
    pre = val(S, '#shT')
    S.page.evaluate("() => { __hk.vis(true); return document.hidden }")
    st = sync(S, trigger='vis')
    after = val(S, '#shT')
    ok = sync_ok(st) and pre == T and a1 != 'shT' and after == T
    rec(S, 'K4', ok, 'share Text shT 글 → 포커스 뺌 → 숨김 → 원격 변경 → 보임(visibilitychange → 앱 syncAll) → 글 그대로',
        dict(typed=T, blur=m, active_after_blur=a1, before=pre, sync=st, after=after), hut=True)


# §0-5 칸 묶음 — (칸, 표시, 선택자(바탕에도 있는 꼴), 넣기, 값, 바탕 FAIL 이어야)
G5 = [
    dict(g='share-txt', view='share', ui={'shareTab': 'txt'}, cm={'t1': True}, blank='#main .ttl > b', wait='[id="shC_t1"]',
         fields=[('K5-1', 'shC_t1(댓글)', '[id="shC_t1"]', 'type', '댓글 초고 K5-1', True)]),
    dict(g='share-ai', view='share', ui={'shareTab': 'ai'}, cm={'p1': True}, ai_new=True, blank='#main .ttl > b', wait='#aiNew',
         fields=[('K5-2', 'aiT(🤖 쓰기 · aiDraft 길)', '#aiT', 'type', '클로드 초고 K5-2', False),
                 ('K5-3', 'aiNew(새 앱)', '#aiNew', 'type', '새앱K5', True),
                 ('K5-4', 'shC_p1(🤖 댓글)', '[id="shC_p1"]', 'type', '클로드 댓글 초고 K5-4', True)]),
    dict(g='share-pv', view='share', ui={'shareTab': 'pv'}, blank='#main .ttl > b', wait='[id="pvN_0_pen"]',
         fields=[('K5-5', 'pvN_0_pen(벌칙 추가)', '[id="pvN_0_pen"]', 'type', '벌칙 초고 K5-5', True),
                 ('K5-6', 'pvW_0_pen(무게 · 미리 1)', '[id="pvW_0_pen"]', 'fill', '3', True)]),
    dict(g='todo', view='todo', blank='#main .ttl > b', wait='#cmT',
         fields=[('K5-7', 'cmT(공통 할일)', '#cmT', 'type', '공통 할일 초고 K5-7', True),
                 ('K5-8', 'cmD(공통 기한)', '#cmD', 'fill', '2026-10-20', True),
                 ('K5-9', 'addS_1(오늘 학습 추가 · 새 id)', '#main .three .col.today input.add[placeholder="+ 학습 추가"]', 'type', '학습 초고 K5-9', True),
                 ('K5-10', 'addT_1(오늘 할일 추가 · 새 id)', '#main .three .col.today input.add[placeholder="+ 할일 추가"]', 'type', '할일 초고 K5-10', True),
                 ('K5-11', 'due_1(오늘 할일 기한)', '[id="due_1"]', 'fill', '2026-10-22', True)]),
    dict(g='day', view='day', blank='#main .mbar .run', wait='#mA',
         fields=[('K5-12', 'mA(이날기록 시작)', '#mA', 'fill', '09:00', True),
                 ('K5-13', 'mB(이날기록 끝)', '#mB', 'fill', '10:30', True)]),
    dict(g='plan', view='plan', ui={'planTab': 'list'}, blank=('#main p', '칸 클릭'), wait='#lsNN',
         fields=[('K5-14', 'lsNT(새 활동 분류)', '#lsNT', 'type', '분류초고', True),
                 ('K5-15', 'lsNN(새 활동 이름)', '#lsNN', 'type', '활동 초고 K5-15', True),
                 ('K5-16', 'lsNW(새 활동 주차)', '#lsNW', 'type', '20~18', True),
                 ('K5-17', 'lsNP(새 활동 주당)', '#lsNP', 'fill', '3', True)]),
    dict(g='set', view='set', blank='#main .ttl > b', wait='#tok',
         fields=[('K5-18', 'tok(토큰 · 미리 채움)', '#tok', 'fill', 'ghp_k5_new_token', True),
                 ('K5-19', 'setXn_ex1(시험 이름 · 새 id)', '#examList input[data-xi="ex1"][data-xk="name"]', 'fill', '제64회 변리사 1차(고침)', True),
                 ('K5-20', 'setXd_ex1(시험 날짜 · 새 id)', '#examList input[data-xi="ex1"][data-xk="date"]', 'fill', '2027-02-27', True),
                 ('K5-21', 'setSn_0(과목 이름 · 새 id)', '#subjList input[data-i="0"][data-k="n"]', 'fill', '민법(고침)', True),
                 ('K5-22', 'rH(분홍 시간)', '#rH', 'fill', '12', True)]),
    dict(g='arch', view='arch', ui={'archTab': 'food'}, blank='#main .ttl > b', wait='#fdQ',
         fields=[('K5-23', 'fdQ(음식 검색 · foodQv 길)', '#fdQ', 'type', '김치', False)]),
]


def g5_group(S, G):
    goto(S, G['view'], G.get('ui'), G.get('cm'), G.get('ai_new'), wait_sel=G['wait'])
    fs = G['fields']
    how_in = {}
    for cid, lab, sel, how, v, hut in fs:
        how_in[cid] = put(S, sel, v, how)
    if G['g'] == 'arch':   # foodQ 는 150ms 뒤에 foodQv 를 바꾼다 — 그 표지를 기다림
        QC.until(S.page, "(v) => foodQv === v", 5000, 'foodQv', arg=fs[0][4])
    m, a1 = blur_away(S, G['blank'], [f[2] for f in fs])
    pre = {cid: val(S, sel) for cid, lab, sel, how, v, hut in fs}
    st = sync(S, share=(G['view'] == 'share'))
    for cid, lab, sel, how, v, hut in fs:
        after = val(S, sel)
        fa = is_act(S, sel)
        ok = sync_ok(st) and pre[cid] == v and after == v and not fa
        rec(S, cid, ok, '%s · %s 글 → 포커스 뺌 → 원격 변경 syncAll → 글 그대로' % (G['g'], lab),
            dict(sel=sel, typed=v, put=how_in[cid], blur=m, active_after_blur=a1, before=pre[cid], sync=st, after=after, refocused=fa), hut=hut)


def _post_sync(S, chk):
    """저장 뒤 한 번 더 원격 변경 syncAll — chk() 가 여전히 참인가"""
    st = sync(S, share=(S.page.evaluate("() => ui.view") == 'share'))
    return st, chk()


def g5_save(S, G):
    g = G['g']
    pg = S.page
    if g == 'share-txt':
        sel, v = '[id="shC_t1"]', '댓글 초고 K5-1'
        rf = refill(S, sel, v, 'type')
        focus_field(S, sel)
        pg.keyboard.press('Enter')
        QC.until(pg, "(v) => (shareFile().data.items.find(x => x.id === 't1').cm || []).some(c => c.t === v)", 8000, '댓글 달림', arg=v)
        a0 = val(S, sel)
        st, a1 = _post_sync(S, lambda: val(S, sel))
        n = pg.evaluate("(v) => (shareFile().data.items.find(x => x.id === 't1').cm || []).filter(c => c.t === v && !c.del).length", v)
        rec(S, 'K5-1s', a0 == '' and sync_ok(st) and a1 == '' and n == 1, 'share-txt · shC_t1 Enter(댓글 달기) 뒤 빈 칸 · syncAll 뒤에도 빈 칸 · 댓글 1',
            dict(refilled=rf, after=a0, sync=st, after_sync=a1, n=n))
    elif g == 'share-ai':
        sel, v = '#aiNew', '새앱K5'
        rf = refill(S, sel, v, 'type')
        focus_field(S, sel)
        pg.keyboard.press('Enter')
        QC.until(pg, "(v) => aiApps().some(x => x.t === v)", 8000, '앱 추가', arg=v)
        a0 = pg.evaluate("() => !!document.getElementById('aiNew')")
        st, a1 = _post_sync(S, lambda: pg.evaluate("() => !!document.getElementById('aiNew')"))
        rec(S, 'K5-3s', a0 is False and sync_ok(st) and a1 is False, 'share-ai · aiNew Enter(앱 넣기) 뒤 칸 닫힘 · syncAll 뒤에도 다시 안 생김',
            dict(refilled=rf, aiNew_after=a0, sync=st, aiNew_after_sync=a1))
        sel, v = '[id="shC_p1"]', '클로드 댓글 초고 K5-4'
        rf = refill(S, sel, v, 'type')
        focus_field(S, sel)
        pg.keyboard.press('Enter')
        QC.until(pg, "(v) => (shareFile().data.items.find(x => x.id === 'p1').cm || []).some(c => c.t === v)", 8000, '🤖 댓글 달림', arg=v)
        a0 = val(S, sel)
        st, a1 = _post_sync(S, lambda: val(S, sel))
        rec(S, 'K5-4s', a0 == '' and sync_ok(st) and a1 == '', 'share-ai · shC_p1 Enter(댓글 달기) 뒤 빈 칸 · syncAll 뒤에도 빈 칸',
            dict(refilled=rf, after=a0, sync=st, after_sync=a1))
        sel, v = '#aiT', '클로드 초고 K5-2'
        rf = refill(S, sel, v, 'type')
        if not pg.evaluate("() => aiSel.length"):
            press(S, ('#main .aicomp .aiapp', 'tt'))
        press(S, '#main .aicomp button.btn.p')
        QC.until(pg, "(v) => aiPosts().some(x => x.t === v)", 8000, '🤖 올림', arg=v)
        a0 = val(S, sel)
        st, a1 = _post_sync(S, lambda: val(S, sel))
        rec(S, 'K5-2s', a0 == '' and sync_ok(st) and a1 == '', 'share-ai · aiT 「올리기」 뒤 빈 칸 · syncAll 뒤에도 빈 칸',
            dict(refilled=rf, after=a0, sync=st, after_sync=a1))
    elif g == 'share-pv':
        r1 = refill(S, '[id="pvN_0_pen"]', '벌칙 초고 K5-5', 'type')
        r2 = refill(S, '[id="pvW_0_pen"]', '3', 'fill')
        press(S, '#main .pvadd:has([id="pvN_0_pen"]) button')
        QC.until(pg, "() => shareItems('pv').some(x => x.t === '벌칙 초고 K5-5' && x.w === 3)", 8000, '벌칙 추가')
        a0 = [val(S, '[id="pvN_0_pen"]'), val(S, '[id="pvW_0_pen"]')]
        st, a1 = _post_sync(S, lambda: [val(S, '[id="pvN_0_pen"]'), val(S, '[id="pvW_0_pen"]')])
        ok = a0 == ['', '1'] and sync_ok(st) and a1 == ['', '1']
        rec(S, 'K5-5s', ok, 'share-pv · pvN_0_pen ＋(추가) 뒤 빈 칸 · syncAll 뒤에도', dict(refilled=r1, after=a0[0], sync=st, after_sync=a1[0]))
        rec(S, 'K5-6s', ok, 'share-pv · pvW_0_pen ＋(추가) 뒤 그려진 값 1 · syncAll 뒤에도', dict(refilled=r2, after=a0[1], sync=st, after_sync=a1[1]))
    elif g == 'todo':
        r1 = refill(S, '#cmT', '공통 할일 초고 K5-7', 'type')
        r2 = refill(S, '#cmD', '2026-10-20', 'fill')
        press(S, '#main button[onclick="cmAdd()"]')
        QC.until(pg, "() => __hk.items('todos/공통.json').some(x => x.t === '공통 할일 초고 K5-7' && x.due === '2026-10-20')", 8000, '공통 할일 추가')
        a0 = [val(S, '#cmT'), val(S, '#cmD')]
        st, a1 = _post_sync(S, lambda: [val(S, '#cmT'), val(S, '#cmD')])
        ok = a0 == ['', ''] and sync_ok(st) and a1 == ['', '']
        rec(S, 'K5-7s', ok, 'todo · cmT 추가 뒤 빈 칸 · syncAll 뒤에도', dict(refilled=r1, after=a0[0], sync=st, after_sync=a1[0]))
        rec(S, 'K5-8s', ok, 'todo · cmD 추가 뒤 빈 칸 · syncAll 뒤에도', dict(refilled=r2, after=a0[1], sync=st, after_sync=a1[1]))
        sS = '#main .three .col.today input.add[placeholder="+ 학습 추가"]'
        r3 = refill(S, sS, '학습 초고 K5-9', 'type')
        focus_field(S, sS)
        pg.keyboard.press('Enter')
        QC.until(pg, "() => todoFile(cfg.person).data.items.some(x => x.t === '학습 초고 K5-9' && x.kind === 'study')", 8000, '학습 추가')
        a0 = val(S, sS)
        st, a1 = _post_sync(S, lambda: val(S, sS))
        rec(S, 'K5-9s', a0 == '' and sync_ok(st) and a1 == '', 'todo · 오늘 「+ 학습 추가」 Enter 뒤 빈 칸 · syncAll 뒤에도', dict(refilled=r3, after=a0, sync=st, after_sync=a1))
        sT = '#main .three .col.today input.add[placeholder="+ 할일 추가"]'
        r4 = refill(S, sT, '할일 초고 K5-10', 'type')
        r5 = refill(S, '[id="due_1"]', '2026-10-22', 'fill')
        focus_field(S, sT)
        pg.keyboard.press('Enter')
        QC.until(pg, "() => todoFile(cfg.person).data.items.some(x => x.t === '할일 초고 K5-10' && x.due === '2026-10-22')", 8000, '할일 추가')
        a0 = [val(S, sT), val(S, '[id="due_1"]')]
        st, a1 = _post_sync(S, lambda: [val(S, sT), val(S, '[id="due_1"]')])
        ok = a0 == ['', ''] and sync_ok(st) and a1 == ['', '']
        rec(S, 'K5-10s', ok, 'todo · 오늘 「+ 할일 추가」 Enter 뒤 빈 칸 · syncAll 뒤에도', dict(refilled=r4, after=a0[0], sync=st, after_sync=a1[0]))
        rec(S, 'K5-11s', ok, 'todo · due_1 할일 추가 뒤 빈 칸 · syncAll 뒤에도', dict(refilled=r5, after=a0[1], sync=st, after_sync=a1[1]))
    elif g == 'day':
        r1 = refill(S, '#mA', '09:00', 'fill')
        r2 = refill(S, '#mB', '10:30', 'fill')
        press(S, '#main button[onclick^="manualSave"]')
        QC.until(pg, "() => sessionsOf(cfg.person, curDate()).some(x => x.a === 540 && x.b === 630)", 8000, '이날기록 저장')
        a0 = [val(S, '#mA'), val(S, '#mB')]
        st, a1 = _post_sync(S, lambda: [val(S, '#mA'), val(S, '#mB')])
        ok = a0 == ['', ''] and sync_ok(st) and a1 == ['', '']
        rec(S, 'K5-12s', ok, 'day · mA 저장 뒤 빈 칸 · syncAll 뒤에도', dict(refilled=r1, after=a0[0], sync=st, after_sync=a1[0]))
        rec(S, 'K5-13s', ok, 'day · mB 저장 뒤 빈 칸 · syncAll 뒤에도', dict(refilled=r2, after=a0[1], sync=st, after_sync=a1[1]))
    elif g == 'plan':
        rr = [refill(S, '#lsNT', '분류초고', 'type'), refill(S, '#lsNN', '활동 초고 K5-15', 'type'),
              refill(S, '#lsNW', '20~18', 'type'), refill(S, '#lsNP', '3', 'fill')]
        focus_field(S, '#lsNN')
        pg.keyboard.press('Enter')
        QC.until(pg, "() => myPlan().bands.some(b => b.name === '활동 초고 K5-15' && !b.del)", 8000, '활동 추가')
        ss = ['#lsNT', '#lsNN', '#lsNW', '#lsNP']
        a0 = [val(S, s) for s in ss]
        st, a1 = _post_sync(S, lambda: [val(S, s) for s in ss])
        ok = a0 == ['', '', '', ''] and sync_ok(st) and a1 == ['', '', '', '']
        for i, cid in enumerate(['K5-14s', 'K5-15s', 'K5-16s', 'K5-17s']):
            rec(S, cid, ok, 'plan · %s 새 활동 Enter 뒤 빈 칸 · syncAll 뒤에도' % ss[i][1:], dict(refilled=rr[i], after=a0[i], sync=st, after_sync=a1[i]))
    elif g == 'set':
        k6_tok(S)
        F = [('K5-19s', '#examList input[data-xi="ex1"][data-xk="name"]', '제64회 변리사 1차(고침)', "() => settings.exams.find(x => x.id === 'ex1').name"),
             ('K5-20s', '#examList input[data-xi="ex1"][data-xk="date"]', '2027-02-27', "() => settings.exams.find(x => x.id === 'ex1').date"),
             ('K5-21s', '#subjList input[data-i="0"][data-k="n"]', '민법(고침)', "() => settings.subjects[0].n"),
             ('K5-22s', '#rH', '12', "() => String(settings.redHours)")]
        rr = [refill(S, s, v, 'fill') for _, s, v, _ in F]
        press(S, '#main button[onclick="applySettings()"]')
        QC.until(pg, "() => settings.redHours === 12", 8000, '설정 저장')
        a0 = [[val(S, s), pg.evaluate(js)] for _, s, v, js in F]
        st, a1 = _post_sync(S, lambda: [[val(S, s), pg.evaluate(js)] for _, s, v, js in F])
        for i, (cid, s, v, js) in enumerate(F):
            ok = a0[i] == [v, v] and sync_ok(st) and a1[i] == [v, v]
            rec(S, cid, ok, 'set · %s 「설정 저장」 뒤 칸 = 저장값(미리 채운 칸) · syncAll 뒤에도' % s, dict(refilled=rr[i], after=a0[i], sync=st, after_sync=a1[i]))


def k5(S):
    for G in G5:
        try:
            g5_group(S, G)
        except Exception as e:
            rec(S, 'K5-%s' % G['g'], False, '%s 묶음 하네스 예외' % G['g'], dict(err=str(e)[:300], tb=traceback.format_exc().splitlines()[-3:]))
            continue
        if G['g'] == 'arch':
            continue
        try:
            g5_save(S, G)
        except Exception as e:
            rec(S, 'K5-%ss' % G['g'], False, '%s 저장 하네스 예외' % G['g'], dict(err=str(e)[:300], tb=traceback.format_exc().splitlines()[-3:]))
    try:
        k5_lsin(S)
    except Exception as e:
        rec(S, 'K5-24', False, 'plan lsInline 하네스 예외', dict(err=str(e)[:300], tb=traceback.format_exc().splitlines()[-3:]))


NAME_TD = "#main .pltab td[onclick*=\"'b1','name'\"]"
ED_IN = '#main .pltab td input[onblur*="lsSet"]'   # lsInline 이 연 칸 수정 칸(새 활동 줄 lsN* 과 가름)


def k5_lsin(S):
    goto(S, 'plan', {'planTab': 'list'}, wait_sel=NAME_TD)
    T = '객1회독 고침'
    press(S, NAME_TD)
    QC.until(S.page, "(s) => !!document.querySelector(s) && document.activeElement === document.querySelector(s)", 5000, '칸 수정 열림', arg=ED_IN)
    S.page.keyboard.insert_text(T)   # lsInline 이 select() 해 둠 — 친 글이 갈아 끼움
    m, a1 = blur_away(S, ('#main p', '칸 클릭'), [ED_IN])
    st = sync(S, share=False)
    name = S.page.evaluate("() => (myPlan().bands.find(b => b.id === 'b1') || {}).name")
    cell = S.page.evaluate("(s) => { const e = document.querySelector(s); return e ? e.textContent : null }", NAME_TD)
    ok = sync_ok(st) and name == T and cell == T
    rec(S, 'K5-24', ok, 'plan · lsInline 이름 칸 글 → 포커스 뺌(onblur = lsSet 저장) → 원격 변경 syncAll → 활동 이름 = 친 글',
        dict(typed=T, blur=m, active_after_blur=a1, sync=st, name=name, cell=cell))


def k5x(S):
    goto(S, 'plan', {'planTab': 'list'}, wait_sel=NAME_TD)
    U = '칸 수정 중 글'
    before_name = S.page.evaluate("() => (myPlan().bands.find(b => b.id === 'b1') || {}).name")
    press(S, NAME_TD)
    QC.until(S.page, "(s) => !!document.querySelector(s) && document.activeElement === document.querySelector(s)", 5000, '칸 수정 열림', arg=ED_IN)
    S.page.keyboard.insert_text(U)
    a0 = act(S)
    st = sync(S, share=False)
    r = S.page.evaluate("""(s) => ({name: (myPlan().bands.find(b => b.id === 'b1') || {}).name,
        editor: !!document.querySelector('#main .pltab td input[onblur*="lsSet"]'), cell: (document.querySelector(s) || {}).textContent || null,
        tables: document.querySelectorAll('#main .pltab').length, active: __hk.act()})""", NAME_TD)
    what = '저장됨(지울 때 blur → lsSet)' if r['name'] == U else ('사라짐' if not r['editor'] else '칸 살아 있음')
    rec(S, 'K5x', None, 'plan · lsInline 칸 수정 중(포커스 둔 채) 원격 변경 syncAll → 친 글 = %s' % what,
        dict(typed=U, before_name=before_name, active_before=a0, sync=st, **r), info=True)


def k6_img(S):
    goto(S, 'share', {'shareTab': 'img'}, wait_sel='#shF')
    loc(S, '#shF').set_input_files(files=[{'name': 'k6.png', 'mimeType': 'image/png', 'buffer': PNG1}])
    n0 = S.page.evaluate("() => document.getElementById('shF').files.length")
    S.page.evaluate("() => __hk.mark()")
    press(S, '#main button[onclick="shareAddImg()"]')
    ok1 = QC.until(S.page, "() => shareItems('img').length === 1 && __hk.rendered()", 15000, '사진 올림 · 재그림')
    a0 = S.page.evaluate("() => { const e = document.getElementById('shF'); return e ? e.files.length : null }")
    st, a1 = _post_sync(S, lambda: S.page.evaluate("() => { const e = document.getElementById('shF'); return e ? e.files.length : null }"))
    ni = S.page.evaluate("() => shareItems('img').length")
    put_n = sum(1 for p in S.gh.puts if p.startswith('share/img/'))
    ok = n0 == 1 and ok1 and a0 == 0 and sync_ok(st) and a1 == 0 and ni == 1 and put_n == 2
    rec(S, 'K6-1', ok, 'shareAddImg(await 뒤 render) — 올린 뒤 shF 빈 칸 · syncAll 뒤에도 · 사진 항목 1 · 사진·썸네일 PUT 2',
        dict(files_before=n0, uploaded=ok1, files_after=a0, sync=st, files_after_sync=a1, img_items=ni, img_puts=put_n))


def k6_tok(S):
    """설정 「저장 후 동기화」 — tok 을 cfg.token 에 넣고 syncAll(await 뒤 render) → 다시 그린 tok = 저장값 · 다른 칸 초고(시험 이름)는 그대로"""
    pg = S.page
    v = 'ghp_k5_new_token'
    rf = refill(S, '#tok', v, 'fill')
    sx = '#examList input[data-xi="ex1"][data-xk="name"]'
    rf2 = refill(S, sx, '제64회 변리사 1차(고침)', 'fill')
    S.n += 1
    n = S.n
    pg.evaluate("() => { try { clearTimeout(syncT) } catch (e) {} return 1 }")
    QC.until(pg, "() => !syncing && _inUi === false", 20000, '동기화 빔')
    pg.evaluate("() => __hk.mark()")
    S.gh.change(n, False)
    press(S, ('#main button', '저장 후 동기화'))
    ok1 = QC.until(pg, "(n) => !syncing && __hk.rendered() && __hk.has('todos/공통.json', 'rc' + n)", 20000, '저장 후 동기화 → 재그림', arg=n)
    a = [val(S, '#tok'), pg.evaluate("() => cfg.token"), val(S, sx)]
    rec(S, 'K6-2', ok1 and a[0] == v and a[1] == v, 'set · 「저장 후 동기화」(await 뒤 render) — 다시 그린 tok = 저장값(cfg.token) · 옛 값 되살아남 0',
        dict(refilled=rf, rerendered=ok1, tok=a[0], cfg_token=a[1]))
    rec(S, 'K6-2b', ok1 and a[2] == '제64회 변리사 1차(고침)', 'set · 「저장 후 동기화」 재그림(await 뒤)에도 다른 칸(시험 이름) 초고 그대로',
        dict(refilled=rf2, rerendered=ok1, exam_name=a[2]), hut=True)


def k6_food(S):
    goto(S, 'arch', {'archTab': 'food'}, wait_sel='#fdQ')
    pg = S.page
    press(S, '#main button[onclick="foodAddModal()"]')
    QC.until(pg, "() => !!document.querySelector('.modal #fdN')", 5000, '음식 모달')
    loc(S, '.modal #fdN').fill('라면 K6-3')
    press(S, '.modal #mOk')
    ok1 = QC.until(pg, "() => foodItems().some(x => x.name === '라면 K6-3') && !document.querySelector('.modal #fdN')", 8000, '음식 저장')
    press(S, '#main button[onclick="foodAddModal()"]')
    QC.until(pg, "() => !!document.querySelector('.modal #fdN')", 5000, '음식 모달 다시')
    a = val(S, '.modal #fdN')
    press(S, '.modal #mNo')
    rec(S, 'K6-3', ok1 and a == '', 'foodSave(모달 · async) — 저장 뒤 모달을 다시 열면 이름 칸 빔', dict(saved=ok1, reopened_name=a))


def k6(S):
    for f in (k6_img, k6_food):
        try:
            f(S)
        except Exception as e:
            rec(S, 'K6-' + f.__name__, False, '%s 하네스 예외' % f.__name__, dict(err=str(e)[:300], tb=traceback.format_exc().splitlines()[-3:]))


SCAN = [('share 🖼 Image', 'share', {'shareTab': 'img'}), ('share 📝 Text', 'share', {'shareTab': 'txt'}),
        ('share ⚡ 벌칙포상', 'share', {'shareTab': 'pv'}), ('share 🤖 클로드', 'share', {'shareTab': 'ai'}),
        ('계획 주차별', 'plan', {'planTab': 'week'}), ('계획 리스트', 'plan', {'planTab': 'list'}),
        ('설정', 'set', {}), ('일간', 'day', {}), ('할일', 'todo', {}), ('Archive', 'arch', {'archTab': 'food'})]


def k7(S):
    per = {}
    for lab, view, ui in SCAN:
        e0 = len(S.errs())
        try:
            if view == 'share':   # share 네 탭은 사람처럼 탭 글자를 누른다(처음 한 번만 화면 옮김)
                if S.page.evaluate("() => ui.view") != 'share':
                    goto(S, 'share', {'shareTab': 'img'}, wait_sel='#main .views')
                tab = {'img': '🖼 Image', 'txt': '📝 Text', 'pv': '⚡ 벌칙포상', 'ai': '🤖 클로드'}[ui['shareTab']]
                press(S, ('#main .views:not(.moretabs) span', tab))
                QC.until(S.page, "(t) => ui.shareTab === t", 5000, '탭 ' + tab, arg=ui['shareTab'])
            else:
                goto(S, view, ui, wait_sel='#main > *')
            ok_draw = S.page.evaluate("() => document.getElementById('main').children.length > 0")
        except Exception as ex:
            ok_draw = False
            per[lab] = 'ex: ' + str(ex)[:120]
            continue
        e1 = S.errs()
        per[lab] = (len(e1) - e0) if ok_draw else 'no-draw'
    bad = {k: v for k, v in per.items() if v != 0}
    rec(S, 'K7', not bad, '화면 훑기(share 네 탭 · 계획 · 설정 · 일간 · 할일 · Archive) 오류 0',
        dict(per_view=per, errs=S.errs()[:5]))


def k8(S):
    e = S.errs()
    rec(S, 'K8', not e, '이 문맥 처음부터 끝까지 스크립트 오류 0(window error · unhandledrejection · pageerror · console.error)',
        dict(n=len(e), errs=e[:6], blocked=sorted(set(S.gh.blocked))[:5]))


RUN = {'K1a': lambda S: k1(S, 'K1a', ('#main .shwho span', ME), 'Text 탭 칩(쓰는 칸 옆 이름 칩 · render 안 부름)'),
       'K1b': lambda S: k1(S, 'K1b', '#main .ttl > b', '빈 곳(Share 제목 글자)'),
       'K1x': k1x, 'K2': k2, 'K3': k3, 'K4': k4, 'K5': k5, 'K5x': k5x, 'K6': k6, 'K7': k7, 'K8': k8}


def run_dev(browser, dev, app, base, plan):
    S = Sess(browser, dev, app, base)
    try:
        if not S.booted:
            rec(S, 'K0', False, '부팅 — render · syncAll · keepInputGrab · #main', dict(errs=S.errs()[:5]))
            return
        for k in plan:
            if ONLY and not any(k == o or k.startswith(o) for o in ONLY):
                continue
            with QC.stage('%s %s %s' % (dev, 'base' if base else 'new', k)):
                try:
                    RUN[k](S)
                except Exception as e:
                    rec(S, k, False, '하네스 예외', dict(err=str(e)[:300], tb=traceback.format_exc().splitlines()[-3:]))
    finally:
        S.close()


def load_base():
    if os.path.isfile(BASE):
        return open(BASE, 'rb').read(), BASE
    QC.sub('git:show-app')
    root = os.environ.get('GENIE_ROOT') or _roots.genie()
    r = subprocess.run(['git', '-C', root, 'show', '%s:timetable/index.html' % BASE], capture_output=True, timeout=60)
    if r.returncode != 0:
        raise SystemExit('바탕 못 꺼냄 — git show %s 실패: %s' % (BASE, r.stderr.decode('utf-8', 'replace')[:200]))
    return r.stdout, 'git %s' % BASE


def main():
    t0 = time.time()
    new = open(NEWF, 'rb').read()
    out('INFO | 판 NEW | %s · %d B · md5 %s · CR %d' % (NEWF, len(new), hashlib.md5(new).hexdigest(), new.count(b'\r')))
    base = None
    if QC.GATE:
        base, bsrc = load_base()
        bm = hashlib.md5(base).hexdigest()
        out('INFO | 판 BASE | %s · %d B · md5 %s%s' % (bsrc, len(base), bm, '' if bm == BASE_MD5 else ' · ⚠ 기대 md5 %s 와 다름' % BASE_MD5))
    plan = SMOKE_PLAN if QC.SMOKE else PLAN
    with sync_playwright() as pw:
        for eng in ('chromium', 'webkit'):   # 브라우저는 한 번에 하나 — 크롬 다 끝나고 닫은 뒤 웹킷
            if eng not in ENGINES:
                continue
            devs = [d for d in plan if DEV[d][0] == eng and (not DEVS or d in DEVS)]
            if not devs:
                continue
            with QC.stage('launch ' + eng):
                br = getattr(pw, eng).launch()
            try:
                for d in devs:
                    run_dev(br, d, new, False, plan[d])
                    if base is not None:
                        run_dev(br, d, base, True, plan[d])
            finally:
                br.close()
    # 헛잣대 줄 — 바탕에서 FAIL 이어야 할 칸
    if QC.GATE:
        for r in [x for x in ROWS if x['side'] == 'new' and x['hut']]:
            b = [x for x in ROWS if x['side'] == 'base' and x['cid'] == r['cid'] and x['dev'] == r['dev']]
            if not b:
                continue
            bst = b[0]['st']
            out('%s | %s-헛 %s · 헛잣대 — 바탕 %s 에서 %s(%s) | %s' % ('PASS' if bst == 'FAIL' else 'FAIL', r['cid'], r['dev'], BASE, bst,
                                                             '잣대가 가름' if bst == 'FAIL' else '잣대가 안 가름', b[0]['title'][:60]))
    ver = [ln for ln in LINES if ln.startswith(('PASS', 'FAIL')) and ' | BASE ' not in ln]
    p = sum(1 for ln in ver if ln.startswith('PASS'))
    f = sum(1 for ln in ver if ln.startswith('FAIL'))
    sec = round(time.time() - t0, 1)
    table = summary_table()
    out('합계  PASS %d · FAIL %d  (mode %s · %.1f 초)' % (p, f, QC.MODE, sec))
    write_res(table, p, f, sec)
    return 0 if f == 0 else 1


def summary_table():
    keys = []
    for r in ROWS:
        k = (r['cid'], r['dev'])
        if k not in keys:
            keys.append(k)
    lines = ['칸 | 기기 | 새 판 | 바탕 | 바탕 기대 | 헛잣대']
    for cid, dev in keys:
        n = [x for x in ROWS if x['cid'] == cid and x['dev'] == dev and x['side'] == 'new']
        b = [x for x in ROWS if x['cid'] == cid and x['dev'] == dev and x['side'] == 'base']
        hut = any(x['hut'] for x in n + b)
        info = any(x['info'] for x in n + b)
        ns = n[0]['st'] if n else '—'
        bs = b[0]['st'] if b else '—'
        if info:
            exp, j = '(INFO)', '—'
        elif not b:
            exp, j = ('FAIL' if hut else 'PASS'), '—'
        elif hut:
            exp, j = 'FAIL', ('OK(가름)' if bs == 'FAIL' else '✗ 안 가름')
        else:
            exp, j = 'PASS', ('바탕도 같음' if bs == 'PASS' else '✗ 바탕 FAIL(뜻밖)')
        lines.append('%s | %s | %s | %s | %s | %s' % (cid, dev, ns, bs, exp, j))
    return lines


def write_res(table, p, f, sec):
    head = ['# _harness_tt_keep_drafts 결과 — %s · mode %s · %.1f 초' % (time.strftime('%Y-%m-%d %H:%M:%S'), QC.MODE, sec),
            '# NEW %s · BASE %s' % (NEWF, BASE if QC.GATE else '(안 띄움)'), '']
    body = '\n'.join(head + LINES + ['', '== 칸별 표(새 판 · 바탕 = 헛잣대) =='] + table + ['', '합계  PASS %d · FAIL %d' % (p, f)]) + '\n'
    d = os.path.dirname(os.path.abspath(RES))
    os.makedirs(d, exist_ok=True)
    data = body.encode('utf-8')
    for _ in range(2):   # 마이박스(N:) 이웃 파일 바꿔 씀 사고 — 쓰고 되읽어 대조(메모 mybox-adjacent-file-write-swaps-contents)
        with open(RES, 'wb') as fh:
            fh.write(data)
        time.sleep(0.5)
        if open(RES, 'rb').read() == data:
            break
    print('결과 → %s (%d B · md5 %s)' % (RES, len(data), hashlib.md5(data).hexdigest()), flush=True)
    for ln in table:
        print('   ' + ln, flush=True)


if __name__ == '__main__':
    sys.exit(main())
