# -*- coding: utf-8 -*-
r"""tt앱 — 쓰던 글 화면 기억 · 계획 칸 고치기 보존 관문 (tt 둘째 판 · 2026-10-09)
  근거 = 결정로그 10/9 19:48 [채팅] 「tt 쓰던 글 기억(사용자 19:47 허락) 꼴」 · 19:50 [채팅] 「tt_keep_drafts 인도 검수」 ②

  python _harness_tt_drafts2.py [--mode gate|regress|smoke] [--new <앱 html>] [--base <git 판 | 앱 html>] [--res <결과 파일>]
                                [--only T1a,T3,…] [--engines chromium,webkit] [--devs chromium-pc]

  NEW  = 이 판 앱(기본 GENIE_ROOT timetable/index.html — 워크트리·사슬 실행기가 GENIE_ROOT 를 준다 · 없으면 _roots.genie())
  BASE = 헛잣대(기본 genie git 6f4a56d = 10/9 tt_keep_drafts 판 · md5 504be22f) — gate 에서만 띄운다
  기기 = Chromium PC 1100×800(클릭) → 그 브라우저를 닫고 WebKit 폰 390(hasTouch · 진짜 터치 톡 = locator.tap → touchscreen.tap)
         브라우저는 한 번에 하나 · 판(NEW/BASE)·기기마다 새 문맥
  앱 자리 = https://api.github.com/__tt/timetable/index.html 을 route 가 내준다(GitHub API 와 같은 출처 · CORS 없음) · 진짜 網은 통째로 막음
  가짜 GitHub(route · 문맥마다 메모리) = contents GET · PUT · 원격 변경 = todos/공통.json(늘 동기화) + share.json(share 화면일 때) 새 항목
  시드(init script) = 날짜 2026-10-09 12:00 KST · confirm/alert/prompt 스텁 · 오류 모음 · localStorage(share 3 · plan 활동 b1 · food 1 · 시험기록 63회 1차 문항 2)
  재그림 표지 = 동기화 전 #main 첫 자식에 data-hk → 끝난 뒤 사라짐 + 원격 항목이 로컬에 들어옴(그림이 안 바뀐 PASS 없음)
  화면 옮기기 = 사람처럼 누름(PC = 옆 차림 #side · 폰 = 아래 #pnav · 더보기 줄 .moretabs · share 탭 글자 · 칩) — 그 누름의 render 는 _inUi(사용자 조작 안)
  goto(칸마다 처음) = 사용자 조작 밖 화면 옮기기 · 앞 칸 초고 치우기(글 칸을 그려진 값으로 · 화면 기억 _draft 비움 — 바탕엔 없음)

  관문(결정로그 19:48 · 19:50 ② 그대로):
   T1a  share Text 글 → 다른 탭 칩(🖼 Image) → 다시 📝 Text = 글 그대로 · 포커스 안 옮김 → syncAll 뒤에도                       [헛잣대]
   T1b  share Text 글 → shcat 「전체」 칩(그 누름의 render = _inUi) = 글 그대로                                               [헛잣대]
   T1c  share Text 글 → 계획(주월계획) 화면 → 그 화면에서 syncAll → 다시 Share = 그대로                                      [헛잣대]
   T1d  share Text 글 → 설정 화면 → 다시 Share = 그대로                                                                       [헛잣대]
   T2   올리기 → 빈 칸 · 항목 1 → 탭 오감 → 빈 채 → syncAll → 빈 채 → 계획 갔다 옴 → 빈 채(되살아남 0)                        [바탕도 같음]
   T3   계획 리스트 lsInline 이름 칸 고치는 중(포커스 둔 채) 원격 변경 syncAll = 칸 글 그대로 · 포커스·커서 · 아직 저장 안 함     [헛잣대]
   T3s  그 뒤 Enter = 저장(이름 = 친 글) · 칸 닫힘 · syncAll 뒤에도                                                           [바탕 참고]
   T3p  (PC) lsInline 주당(숫자 칸) 같은 잣대 · T3ps 그 뒤 Enter 저장                                                         [헛잣대 · 바탕 참고]
   T4   시험기록 exInline 비고 칸 고치는 중 재그림 = 글 그대로 · 포커스 · 아직 저장 안 함                                       [헛잣대]
   T4s  그 뒤 Enter = 저장(비고 = 친 글) · 칸 닫힘 '📝 …' · syncAll 뒤에도                                                    [바탕 참고]
   T5a~c (PC) 작은 창(PiP) 이날기록 mA·mB 글 → (a) 본창 탭 칩 render (b) syncAll (c) 작은 창 다시 그리기(1 분 타이머 자리) = 그대로 [헛잣대]
   T5s  (PC) 작은 창 「저장」 = 칸 빔 · 본창 탭 칩 · syncAll 뒤에도 빈 채 · 기록 1                                            [바탕도 같음]
        PiP 는 documentPictureInPicture 대신 같은 출처 iframe 을 pipWin 으로(pip() 와 같은 함수 이름 넘김) · INFO T5i = 진짜 작은 창은 .man 을 숨김(앱 CSS)
   T6a~d 다른 id 칸도 화면 기억 — 공통 할일 cmT(타임테이블 → Share → 타임테이블) · 벌칙 pvN_0_pen(⚡ → 📝 → ⚡) ·
        설정 시험 이름(설정 → Share → 설정) · 댓글 shC_t1(댓글 접기 → 펴기) = 그대로                                          [헛잣대]
   T7a~n 「올리기 · 저장」 처리기마다 그 뒤 빈 칸(미리 채운 칸 = 저장값) → 화면·탭 오감 → syncAll 뒤에도 = 되살아남 0             [바탕도 같음]
        a 댓글 Enter · b 🤖 올리기 · c 새 앱 Enter · d 벌칙 ＋ · e 공통 할일 추가 · f 학습 추가 Enter · g 할일+기한 Enter · h 이날기록 저장 ·
        i 새 활동 Enter · j 설정 저장 · k 토큰 저장 후 동기화 · l lsInline 저장 뒤 화면 오감 = 칸 안 열림 · m exInline 저장 뒤 = 안 열림 · n exInline Esc = 취소
   T8   칸을 손으로 다 지우면 기억도 지움(되살린 뒤 지움 → 탭 오감 = 빈 칸)                                                       [바탕도 같음]
   T9   기기 저장 안 함 — 탭 옮긴 뒤 localStorage · sessionStorage 에 친 글 0 · 새로고침 뒤 빈 칸                                [바탕도 같음]
   T0   화면 훑기(share 네 탭 · 계획 둘 · 설정 · 타임테이블 · Archive 음식 · 시험기록) 오류 0 · TX = 그 문맥 끝까지 오류 0
  헛잣대(gate) = 같은 잣대를 BASE 에 돌린 줄 「BASE <기기> · <칸>」(판정 밖) · [헛잣대] 칸은 「<칸>-헛 <기기>」 줄이 바탕 FAIL 이면 PASS
  모드 = gate(NEW + BASE · 결과 N:\개인\claude\timetable\_tt_drafts2\result.txt) · regress(NEW 만 · %TEMP%\h_tt_drafts2) · smoke(NEW · PC · T1a · T2 · T3 · TX)
  ⚠ 고정 대기 없음 — 앱 표지(syncing · _inUi · ui.view · 재그림 표지 · 항목 수)를 기다린다(QC.until)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — 실행 모드 --mode gate|regress|smoke(없으면 gate) · import 때 --mode · --snap-in · --snap-out 을 sys.argv 에서 뗀다
import base64, collections, datetime, hashlib, json, os, subprocess, sys, tempfile, time, traceback, urllib.parse   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEWF = ARG('--new', _roots.genie('timetable', 'index.html'))
BASE = ARG('--base', '6f4a56d')
BASE_MD5 = '504be22f168721b2834f6d021422c1f1'   # 6f4a56d timetable/index.html 524,412 B(10/9 19:32 push · tt_keep_drafts 판)
ONLY = [x.strip() for x in (ARG('--only', '') or '').split(',') if x.strip()]
ENGINES = [x.strip() for x in (ARG('--engines', 'chromium,webkit') or '').split(',') if x.strip()]
DEVS = [x.strip() for x in (ARG('--devs', '') or '').split(',') if x.strip()]
_TMPD = os.path.join(tempfile.gettempdir(), 'h_tt_drafts2')
if QC.GATE:
    _nres = _roots.n('timetable', '_tt_drafts2', 'result.txt')
    RES = ARG('--res', _nres or os.path.join(_TMPD, 'result.txt'))
else:
    RES = ARG('--res', os.path.join(_TMPD, 'result.txt'))

APP_URL = 'https://api.github.com/__tt/timetable/index.html'
GH = 'https://api.github.com/repos/zzikkaplan/studyplandata/contents/'
ME, OT = '꼬까', '햄찌'
T0 = int(datetime.datetime(2026, 10, 9, 9, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))).timestamp() * 1000)

DEV = {
    'chromium-pc': ('chromium', dict(viewport={'width': 1100, 'height': 800})),
    'webkit-phone': ('webkit', dict(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2)),
}
PLAN = {   # 기기마다 돌릴 관문(차례대로) — T0 첫머리(갓 띄운 화면) · T9(새로고침)·TX 끝
    'chromium-pc': ['T0', 'T1a', 'T1b', 'T1c', 'T1d', 'T2', 'T3', 'T3p', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'TX'],
    'webkit-phone': ['T0', 'T1a', 'T1b', 'T1c', 'T1d', 'T2', 'T3', 'T4', 'T6', 'T7w', 'T8', 'T9', 'TX'],
}
SMOKE_PLAN = {'chromium-pc': ['T1a', 'T2', 'T3', 'TX']}

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
EXAM_ID = '63-1-' + ME
EXAM0 = {'v': 1, 'items': [{
    'id': EXAM_ID, 'no': 63, 'cha': 1, 'who': ME, 'date': '2026-02', 'kind': '정규', 'mode': 'q', 'cut': 60,
    'q': [{'s': '특허', 'i': 1, 'my': '1', 'ans': '2', 'ok': False, 'type': '', 'why': '', 'rate': 50, 'redo': '', 'note': ''},
          {'s': '특허', 'i': 2, 'my': '3', 'ans': '3', 'ok': True, 'type': '', 'why': '', 'rate': 70, 'redo': '', 'note': ''}],
    'sum': {}, 'gavg': {}, 'note': '', 'u': 1, 'del': False}]}
SEED = {
    'tt.cfg': {'person': ME, 'token': '', 'lastSync': 0},
    'tt.ui': {'view': 'share', 'shareTab': 'txt', 'date': None, 'galMonth': None},
    'tt.f.share/share.json': {'data': SHARE0, 'sha': 'r0', 'dirty': False},
    'tt.f.plan/' + ME + '.json': {'data': PLAN_V1, 'sha': None, 'dirty': False},
    'tt.f.food/food.json': {'data': FOOD0, 'sha': 'r0', 'dirty': False},
    'tt.f.todos/공통.json': {'data': COMMON0, 'sha': 'r0', 'dirty': False},
    'tt.f.exam/' + ME + '.json': {'data': EXAM0, 'sha': 'r0', 'dirty': False},
}
REMOTE0 = {'share/share.json': SHARE0, 'todos/공통.json': COMMON0, 'food/food.json': FOOD0, 'exam/' + ME + '.json': EXAM0}

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
  act: () => { const a = document.activeElement; return a ? (a.id || (a.tagName + (a.className ? '.' + a.className : ''))) : null },
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
  stores: t => { const hit = []; [['local', localStorage], ['session', sessionStorage]].forEach(([n, st]) => { for (let i = 0; i < st.length; i++) { const k = st.key(i); if (String(st.getItem(k) || '').indexOf(t) >= 0) hit.push(n + ':' + k) } }); return hit },
 };
})();"""
BOOT_JS = ("() => typeof render === 'function' && typeof syncAll === 'function' && typeof keepInputGrab === 'function' && !!window.__hk"
           " && !!document.getElementById('main') && document.getElementById('main').children.length > 0")
# 화면 옮기기(사용자 조작 밖 render) — 모달 걷기 · 작은 창 흉내 걷기 · #main 글 칸을 그려진 값으로(앞 칸 초고 치우기) · 화면 기억 비움(새 판만) · 포커스 빼기 · 상태 맞춤
GOTO_JS = r"""(a) => {
 document.querySelectorAll('.modal').forEach(m => m.remove());
 const f = document.getElementById('hkPip'); if (f) { try { pipWin = null } catch (e) {} f.remove() }
 document.querySelectorAll('#main input, #main textarea').forEach(e => { if (!/^(checkbox|radio|file|button|submit|hidden|range|color)$/i.test(e.type)) e.value = e.defaultValue; });
 if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
 if (typeof _draft !== 'undefined') _draft.clear();
 aiDraft = ''; aiNewOn = a.aiNew ? 1 : 0; aiSel = []; shCmOpen = Object.assign({}, a.cm || {});
 Object.assign(ui, a.ui || {}); ui.view = a.view; if (a.view === 'share' && !(a.ui && a.ui.shareCat)) ui.shareCat = 'all';
 LS.set('tt.ui', ui); render(); return true }"""
PIP_FN = ['startTimer', 'stopTimer', 'manualSave', 'editSession', 'render', 'curDate', 'setDate', 'addDays', 'today', 'toast', 'selRow', 'toggleTodo',
          'pickTodoItem', 'selUnit', 'togglePlanDone', 'startLife', 'lifeModal', 'lifeSetType', 'lifeAddType', 'lifeDelType', 'lifePlanModal', 'lifePlanDel',
          'pmPopup', 'pmFoldTgl', 'pmDelCat2', 'pmDelItem2', 'pmCatModal', 'pmAddItem', 'pmSelect', 'pmDateEdit', 'pmSetDate', 'editTodo', 'catsOf', 'cfg',
          'pmBandTgl', 'pmDelBand', 'pmGoBand', 'pickRow', 'stCatTgl', 'stMoreTgl', 'pipView', 'renderAll', 'ribbonModal', 'ribbonGo', 'startBlocked',
          'ttWkPick', 'ttMoPick', 'ttWkToday', 'ttMoToday', 'settings']   # pip() 가 작은 창에 넘기는 이름 그대로
PIP_OPEN_JS = r"""(names) => {
 let f = document.getElementById('hkPip');
 if (!f) { f = document.createElement('iframe'); f.id = 'hkPip';
  f.style.cssText = 'position:fixed;right:0;bottom:0;width:520px;height:380px;z-index:2147483000;background:#fff;border:2px solid #888';
  document.body.appendChild(f); }
 const w = f.contentWindow; w.document.open(); w.document.write('<!doctype html><html><head><meta charset="utf-8"></head><body></body></html>'); w.document.close();
 names.forEach(n => { try { w[n] = window[n] } catch (e) {} });
 pipWin = w; pipPaint(); return !!w.document.getElementById('mA') }"""

# ════════════════════ 결과 ════════════════════
LINES, ROWS = [], []


def out(s):
    print(s, flush=True)
    LINES.append(s)


def J(v, n=1200):
    return json.dumps(v, ensure_ascii=False, default=str)[:n]


def rec(S, cid, ok, title, val, hut=False, info=False):
    """hut = True(바탕에서 FAIL 이어야 · 헛잣대) · False(바탕도 PASS · 되돌림 막이) · None(바탕은 참고만)"""
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
        except Exception:   # 문맥이 닫히는 중 등 — 막고 지나감
            try:
                route.abort()
            except Exception:
                pass

    def _handle(self, route):
        req = route.request
        u = req.url
        if u.startswith('blob:') or u.startswith('data:') or u.startswith('about:'):
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
            return route.fulfill(status=200, content_type='image/png', body=b'')
        self.blocked.append(bu[:120])
        return route.abort()


def b64json(d):
    return base64.b64encode(json.dumps(d, ensure_ascii=False).encode('utf-8')).decode('ascii')


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
        self.booted = self.boot()

    def boot(self):
        ok = QC.until(self.page, BOOT_JS, 20000, '부팅')
        if ok:
            self.page.evaluate("() => { cfg.token = 't_harness'; LS.set('tt.cfg', cfg); return cfg.token }")
        return ok

    def errs(self):
        try:
            e = self.page.evaluate("() => (window.__errs || []).slice()")
        except Exception as ex:
            e = ['evaluate: ' + str(ex)[:120]]
        return e + ['pageerror: ' + x for x in self.perr] + ['console: ' + x for x in self.cerr]

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


# ════════════════════ 손 · 재기 ════════════════════
LBL = {'day': '타임테이블', 'gal': '데일리 모음', 'pm': '계획관리', 'plan': '주월계획', 'arch': 'Archive', 'share': 'Share', 'set': '설정'}
TABS = {'img': '🖼 Image', 'txt': '📝 Text', 'pv': '⚡ 벌칙포상', 'ai': '🤖 클로드'}
MORE = ('gal', 'pm', 'plan', 'arch', 'share', 'set')


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
        l.tap(timeout=8000)   # 웹킷 = touchscreen.tap(진짜 터치)
    else:
        l.click(timeout=8000)
    return 'tap' if S.touch else 'click'


def idle(S, what='_inUi 풀림'):
    return QC.until(S.page, "() => _inUi === false && !document.querySelector('.modal')", 5000, what)


def goto(S, view, ui=None, cm=None, ai_new=False, wait_sel=None):
    S.page.evaluate(GOTO_JS, {'view': view, 'ui': ui or {}, 'cm': cm or {}, 'aiNew': bool(ai_new)})
    if wait_sel:
        QC.until(S.page, "(s) => !!document.querySelector(s)", 8000, '화면 ' + view, arg=wait_sel)
    QC.until(S.page, "() => _inUi === false", 5000, '_inUi 풀림')


def nav(S, view):
    """사람처럼 화면 옮김 — PC = 옆 차림 #side · 폰 = 아래 #pnav(타임테이블 · 더보기) + 더보기 줄 .moretabs · 누른 차례를 돌려줌"""
    pg = S.page
    hops = []
    for _ in range(3):
        cur = pg.evaluate("() => ui.view")
        if cur == view:
            break
        if not S.touch:
            hops.append(press(S, ('#side .i', LBL[view])) + ':side')
        elif view == 'day':
            hops.append(press(S, ('#pnav div', '타임테이블')) + ':pnav')
        elif cur in MORE:
            hops.append(press(S, ('#main .moretabs span', LBL[view])) + ':moretabs')
        else:
            hops.append(press(S, ('#pnav div', '더보기')) + ':pnav')
        QC.until(pg, "(c) => ui.view !== c && _inUi === false", 5000, '화면 옮김', arg=cur)
    ok = QC.until(pg, "(v) => ui.view === v && _inUi === false", 5000, '화면 ' + view, arg=view)
    return hops, ok


def tab(S, key):
    m = press(S, ('#main .views:not(.moretabs) span', TABS[key]))
    ok = QC.until(S.page, "(t) => ui.shareTab === t && _inUi === false", 5000, '탭 ' + key, arg=key)
    return m, ok


def focus_field(S, sel):
    m = press(S, sel)
    if not is_act(S, sel):
        loc(S, sel).focus()
        m += '+focus()'
    return m


def put(S, sel, text, how='type'):
    m = focus_field(S, sel)
    if how == 'type':
        S.page.keyboard.insert_text(text)
    else:   # fill — 날짜·시각·숫자 · 미리 채운 칸(값을 갈아 끼움)
        loc(S, sel).fill(text)
    return m


def unfocus(S, sels):
    """칸에서 포커스만 뺌(render 안 부르는 글자 — Share 제목 글자 · 웹킷은 그 톡에 포커스가 안 빠지면 blur())"""
    m = press(S, '#main .ttl > b')
    if any(is_act(S, s) for s in sels):
        S.page.evaluate("() => document.activeElement.blur()")
        m += '+blur()'
    return m


def sync(S, share=True, trigger='call'):
    """원격 변경 하나 → syncAll(true) → 재그림 표지 · 원격 항목 들어옴까지 기다림"""
    S.n += 1
    n = S.n
    pg = S.page
    pg.evaluate("() => { try { clearTimeout(syncT) } catch (e) {} return 1 }")
    QC.until(pg, "() => !syncing && _inUi === false", 20000, '동기화 빔')
    pg.evaluate("() => __hk.mark()")
    S.gh.change(n, share)
    pg.evaluate("() => syncAll(true)")
    ok = QC.until(pg, "(n) => !syncing && __hk.rendered() && __hk.has('todos/공통.json', 'rc' + n)", 20000, '원격 변경 → 재그림', arg=n)
    st = pg.evaluate("(n) => ({rendered: __hk.rendered(), applied: __hk.has('todos/공통.json', 'rc' + n)})", n)
    st['n'] = n
    st['wait'] = ok
    return st


def sync_ok(st):
    return bool(st.get('rendered') and st.get('applied'))


def ex(S, cid, e):
    rec(S, cid, False, '하네스 예외', dict(err=str(e)[:300], tb=traceback.format_exc().splitlines()[-3:]))


# ════════════════════ 관문 T1 · T2 — share Text ════════════════════
def t1a(S):
    goto(S, 'share', {'shareTab': 'txt'}, wait_sel='#shT')
    T = '쓰던 글 T1a %s' % S.dev
    m1 = put(S, '#shT', T)
    m2, ok2 = tab(S, 'img')
    gone = S.page.evaluate("() => !document.getElementById('shT')")
    m3, ok3 = tab(S, 'txt')
    back, a1 = val(S, '#shT'), act(S)
    st = sync(S)
    after = val(S, '#shT')
    ok = ok2 and gone and ok3 and back == T and a1 != 'shT' and sync_ok(st) and after == T
    rec(S, 'T1a', ok, 'share Text 글 → 🖼 Image 탭 칩 → 📝 Text 탭 칩 = 글 그대로 · 포커스 안 옮김 → syncAll 뒤에도',
        dict(typed=T, put=m1, to_img=[m2, ok2], shT_gone_on_img=gone, to_txt=[m3, ok3], back=back, active=a1, sync=st, after_sync=after), hut=True)


def t1b(S):
    goto(S, 'share', {'shareTab': 'txt'}, wait_sel='#shT')
    T = '칩 누름 글 T1b %s' % S.dev
    put(S, '#shT', T)
    S.page.evaluate("() => __hk.mark()")
    m = press(S, '#main .shcat span')   # 「전체」 칩 — shareCatSet → render(사용자 조작 안 · _inUi)
    rr = QC.until(S.page, "() => __hk.rendered() && _inUi === false", 5000, '칩 render')
    after, a1 = val(S, '#shT'), act(S)
    rec(S, 'T1b', rr and after == T, 'share Text 글 → shcat 「전체」 칩(그 누름의 render = _inUi) = 글 그대로',
        dict(typed=T, press=m, rerendered=rr, after=after, active=a1), hut=True)


def t1c(S):
    goto(S, 'share', {'shareTab': 'txt'}, wait_sel='#shT')
    T = '화면 오감 글 T1c %s' % S.dev
    put(S, '#shT', T)
    h1, ok1 = nav(S, 'plan')
    st = sync(S, share=False)
    h2, ok2 = nav(S, 'share')
    QC.until(S.page, "() => !!document.getElementById('shT')", 5000, 'shT 다시')
    after, a1 = val(S, '#shT'), act(S)
    rec(S, 'T1c', ok1 and ok2 and sync_ok(st) and after == T, 'share Text 글 → 주월계획 화면 → 그 화면에서 syncAll → 다시 Share = 글 그대로',
        dict(typed=T, to_plan=[h1, ok1], sync=st, back=[h2, ok2], after=after, active=a1), hut=True)


def t1d(S):
    goto(S, 'share', {'shareTab': 'txt'}, wait_sel='#shT')
    T = '설정 오감 글 T1d %s' % S.dev
    put(S, '#shT', T)
    h1, ok1 = nav(S, 'set')
    h2, ok2 = nav(S, 'share')
    QC.until(S.page, "() => !!document.getElementById('shT')", 5000, 'shT 다시')
    after = val(S, '#shT')
    rec(S, 'T1d', ok1 and ok2 and after == T, 'share Text 글 → 설정 화면 → 다시 Share = 글 그대로',
        dict(typed=T, to_set=[h1, ok1], back=[h2, ok2], after=after), hut=True)


def t2(S):
    goto(S, 'share', {'shareTab': 'txt'}, wait_sel='#shT')
    T = '올리기 글 T2 %s' % S.dev
    put(S, '#shT', T)
    m = press(S, '#main button[onclick="shareAddText()"]')
    cnt = "(t) => shareItems('txt').filter(x => x.text === t).length"
    QC.until(S.page, "(t) => shareItems('txt').some(x => x.text === t) && _inUi === false", 8000, '올린 항목', arg=T)
    a0, c0 = val(S, '#shT'), S.page.evaluate(cnt, T)
    tab(S, 'img')
    tab(S, 'txt')
    a1 = val(S, '#shT')
    st = sync(S)
    a2 = val(S, '#shT')
    h1, _ = nav(S, 'plan')
    h2, _ = nav(S, 'share')
    QC.until(S.page, "() => !!document.getElementById('shT')", 5000, 'shT 다시')
    a3, c3 = val(S, '#shT'), S.page.evaluate(cnt, T)
    ok = a0 == '' and c0 == 1 and a1 == '' and sync_ok(st) and a2 == '' and a3 == '' and c3 == 1
    rec(S, 'T2', ok, '「올리기」(%s) = 칸 빔 · 항목 1 → 탭 오감 → 빈 채 → syncAll → 빈 채 → 계획 갔다 옴 → 빈 채(되살아남 0)' % m,
        dict(text=T, after_post=a0, n_post=c0, after_tabs=a1, sync=st, after_sync=a2, nav=[h1, h2], after_nav=a3, n_end=c3))


# ════════════════════ 관문 T3 · T4 — 칸 고치기(lsInline · exInline) ════════════════════
def ls_td(k):
    return "#main .pltab td[onclick*=\"'b1','%s'\"]" % k


ED_LS = '#main .pltab td input[onblur*="lsSet"]'   # lsInline 이 연 칸 수정 칸


def band(S):
    return S.page.evaluate("() => { const b = myPlan().bands.find(x => x.id === 'b1'); return b ? {name: b.name, per: b.per} : null }")


def ed_state(S, sel):
    return S.page.evaluate("""(s) => { const e = document.querySelector(s); const a = document.activeElement;
        let ss = null, se = null; try { ss = e ? e.selectionStart : null; se = e ? e.selectionEnd : null } catch (x) {}
        return {editor: !!e, value: e ? e.value : null, focused: !!e && a === e, sel: [ss, se], active: __hk.act()} }""", sel)


def t3(S, k='name', cid='T3'):
    goto(S, 'plan', {'planTab': 'list'}, wait_sel=ls_td(k))
    b0 = band(S)
    T = '객1회독 고침 %s' % S.dev[:2] if k == 'name' else '7'
    m = press(S, ls_td(k))
    QC.until(S.page, "(s) => !!document.querySelector(s) && document.activeElement === document.querySelector(s)", 5000, '칸 수정 열림', arg=ED_LS)
    S.page.keyboard.insert_text(T)   # lsInline 이 select() 해 둠 — 친 글이 갈아 끼움
    pre = ed_state(S, ED_LS)
    st = sync(S, share=False)
    after = ed_state(S, ED_LS)
    b1 = band(S)
    key = 'name' if k == 'name' else 'per'
    unsaved = b1 is not None and b1[key] == b0[key]
    sel_ok = after['sel'] == [len(T), len(T)] or k != 'name'   # 숫자 칸은 selection 을 못 잼
    ok = sync_ok(st) and pre['value'] == T and after['editor'] and after['value'] == T and after['focused'] and sel_ok and unsaved
    rec(S, cid, ok, '계획 리스트 lsInline %s 칸 고치는 중(포커스 둔 채) 원격 변경 syncAll = 칸 글 그대로 · 포커스·커서 · 아직 저장 안 함' % k,
        dict(typed=T, press=m, before=pre, sync=st, after=after, band_before=b0, band_after=b1, unsaved=unsaved), hut=True)
    # 그 뒤 Enter = 저장
    S.page.keyboard.press('Enter')
    want = T if k == 'name' else 7
    sv = QC.until(S.page, "([k, w, s]) => { const b = myPlan().bands.find(x => x.id === 'b1'); return !!b && b[k] === w && !document.querySelector(s) && _inUi === false }",
                  5000, '칸 저장', arg=[key, want, ED_LS])
    st2 = sync(S, share=False)
    b2 = band(S)
    cell = S.page.evaluate("(s) => { const e = document.querySelector(s); return e ? e.textContent : null }", ls_td(k))
    ed2 = S.page.evaluate("(s) => !!document.querySelector(s)", ED_LS)
    ok2 = sv and sync_ok(st2) and b2 is not None and b2[key] == want and not ed2 and (cell == T if k == 'name' else cell is not None and str(want) in cell)
    rec(S, cid + 's', ok2, 'lsInline %s 칸 그 뒤 Enter = 저장(친 글) · 칸 닫힘 · syncAll 뒤에도' % k,
        dict(saved_wait=sv, sync=st2, band=b2, cell=cell, editor_after=ed2), hut=None)


EX_TD = "#main td.exic[onclick$=\",0,'note')\"]"
ED_EX = '#main td.exic input.exie'


def ex_note(S):
    return S.page.evaluate("(id) => { const x = examGet(id); return x ? x.q[0].note : null }", EXAM_ID)


def goto_exam(S):
    goto(S, 'arch', {'archTab': 'exam', 'exTab': 'db', 'exCha': 1, 'exWho': ME, 'exSel': EXAM_ID, 'exChip': 'all'}, wait_sel=EX_TD)


def t4(S):
    goto_exam(S)
    n0 = ex_note(S)
    T = '비고 초고 T4 %s' % S.dev[:2]
    m = press(S, EX_TD)
    QC.until(S.page, "(s) => !!document.querySelector(s) && document.activeElement === document.querySelector(s)", 5000, '비고 칸 열림', arg=ED_EX)
    S.page.keyboard.insert_text(T)
    pre = ed_state(S, ED_EX)
    st = sync(S, share=False)
    after = ed_state(S, ED_EX)
    n1 = ex_note(S)
    ok = sync_ok(st) and pre['value'] == T and after['editor'] and after['value'] == T and after['focused'] and after['sel'] == [len(T), len(T)] and n1 == n0
    rec(S, 'T4', ok, '시험기록 exInline 비고 칸 고치는 중(포커스 둔 채) 원격 변경 syncAll = 칸 글 그대로 · 포커스·커서 · 아직 저장 안 함',
        dict(typed=T, press=m, before=pre, sync=st, after=after, note_before=n0, note_after_sync=n1), hut=True)
    S.page.keyboard.press('Enter')
    sv = QC.until(S.page, "([id, t, s]) => { const x = examGet(id); return !!x && x.q[0].note === t && !document.querySelector(s) && _inUi === false }",
                  5000, '비고 저장', arg=[EXAM_ID, T, ED_EX])
    st2 = sync(S, share=False)
    cell = S.page.evaluate("(s) => { const e = document.querySelector(s); return e ? e.textContent : null }", EX_TD)
    ed2 = S.page.evaluate("(s) => !!document.querySelector(s)", ED_EX)
    n2 = ex_note(S)
    ok2 = sv and sync_ok(st2) and n2 == T and not ed2 and cell == '📝 ' + T
    rec(S, 'T4s', ok2, 'exInline 비고 그 뒤 Enter = 저장(친 글) · 칸 닫힘 「📝 …」 · syncAll 뒤에도',
        dict(saved_wait=sv, sync=st2, note=n2, cell=cell, editor_after=ed2), hut=None)


# ════════════════════ 관문 T5 — 작은 창(PiP) 이날기록 칸 ════════════════════
def pip_vals(S):
    return S.page.evaluate("""() => { const f = document.getElementById('hkPip'); const d = f && f.contentWindow && f.contentWindow.document;
        const g = id => { const e = d && d.getElementById(id); return e ? e.value : null }; return [g('mA'), g('mB')] }""")


def t5(S, app):
    has_css = b'.pipwrap .mbar .man{display:none}' in app
    rec(S, 'T5i', None, '참고 — 진짜 작은 창(pip())은 앱 CSS 「.pipwrap .mbar .man{display:none}」 로 이날기록 칸을 숨김 = %s(이 하네스는 iframe 이라 칸이 보임)'
        % ('있음' if has_css else '없음'), dict(css_rule=has_css), info=True)
    goto(S, 'share', {'shareTab': 'txt'}, wait_sel='#shT')
    opened = S.page.evaluate(PIP_OPEN_JS, PIP_FN)
    fr = S.page.frame_locator('#hkPip')
    A, B = '09:00', '10:30'
    fr.locator('#mA').fill(A)
    fr.locator('#mB').fill(B)
    S.page.evaluate("() => { const d = document.getElementById('hkPip').contentWindow.document; if (d.activeElement && d.activeElement.blur) d.activeElement.blur(); return 1 }")
    v0 = pip_vals(S)
    # (a) 본창 탭 칩 render(_inUi) → pipPaint
    S.page.evaluate("() => { const d = document.getElementById('hkPip').contentWindow.document; const r = d.querySelector('.pipwrap'); if (r) r.setAttribute('data-hk', '1'); return 1 }")
    ma, oka = tab(S, 'img')
    rp = S.page.evaluate("() => !document.getElementById('hkPip').contentWindow.document.querySelector('.pipwrap[data-hk]')")
    va = pip_vals(S)
    rec(S, 'T5a', opened and oka and rp and va == [A, B], '작은 창 이날기록 mA·mB 글 → 본창 탭 칩(render · _inUi → 작은 창 다시 그림) = 그대로',
        dict(opened=opened, before=v0, press=ma, repainted=rp, after=va), hut=True)
    # (b) syncAll
    S.page.evaluate("() => { const r = document.getElementById('hkPip').contentWindow.document.querySelector('.pipwrap'); if (r) r.setAttribute('data-hk', '1'); return 1 }")
    st = sync(S)
    rp = S.page.evaluate("() => !document.getElementById('hkPip').contentWindow.document.querySelector('.pipwrap[data-hk]')")
    vb = pip_vals(S)
    rec(S, 'T5b', sync_ok(st) and rp and vb == [A, B], '작은 창 이날기록 글 → 원격 변경 syncAll(작은 창 다시 그림) = 그대로',
        dict(sync=st, repainted=rp, after=vb), hut=True)
    # (c) 작은 창만 다시 그리기(1 분 타이머 · pipView 자리)
    vc0 = S.page.evaluate("() => { const r = document.getElementById('hkPip').contentWindow.document.querySelector('.pipwrap'); if (r) r.setAttribute('data-hk', '1'); pipPaint(); return !document.getElementById('hkPip').contentWindow.document.querySelector('.pipwrap[data-hk]') }")
    vc = pip_vals(S)
    rec(S, 'T5c', vc0 and vc == [A, B], '작은 창 이날기록 글 → 작은 창만 다시 그리기(pipPaint · 1 분 타이머 자리) = 그대로',
        dict(repainted=vc0, after=vc), hut=True)
    # (s) 작은 창 「저장」
    n0 = S.page.evaluate("() => sessionsOf(cfg.person, curDate()).filter(x => x.a === 540 && x.b === 630).length")
    if pip_vals(S) != [A, B]:   # 바탕은 앞에서 지워짐 — 저장 잣대를 따로 재려고 다시 넣음
        fr.locator('#mA').fill(A)
        fr.locator('#mB').fill(B)
    fr.locator('.man button', has_text='저장').first.click()
    sv = QC.until(S.page, "(n) => sessionsOf(cfg.person, curDate()).filter(x => x.a === 540 && x.b === 630).length === n + 1", 8000, '작은 창 저장', arg=n0)
    v1 = pip_vals(S)
    tab(S, 'txt')
    v2 = pip_vals(S)
    st2 = sync(S)
    v3 = pip_vals(S)
    ok = sv and v1 == ['', ''] and v2 == ['', ''] and sync_ok(st2) and v3 == ['', '']
    rec(S, 'T5s', ok, '작은 창 「저장」 = 칸 빔 · 기록 1 → 본창 탭 칩 → 빈 채 → syncAll → 빈 채(되살아남 0)',
        dict(saved=sv, after_save=v1, after_tab=v2, sync=st2, after_sync=v3))
    S.page.evaluate("() => { pipWin = null; const f = document.getElementById('hkPip'); if (f) f.remove(); return 1 }")


# ════════════════════ 관문 T6 — 다른 id 칸도 화면 기억 ════════════════════
def t6(S):
    pg = S.page
    # a 공통 할일(타임테이블 화면)
    try:
        goto(S, 'day', wait_sel='#cmT')
        T = '공통 할일 초고 T6a'
        put(S, '#cmT', T)
        h1, ok1 = nav(S, 'share')
        h2, ok2 = nav(S, 'day')
        QC.until(pg, "() => !!document.getElementById('cmT')", 5000, 'cmT 다시')
        a = val(S, '#cmT')
        rec(S, 'T6a', ok1 and ok2 and a == T, '공통 할일 cmT 글 → Share 화면 → 다시 타임테이블 = 그대로', dict(typed=T, nav=[h1, h2], after=a), hut=True)
    except Exception as e:
        ex(S, 'T6a', e)
    # b 벌칙 추가(⚡ 탭)
    try:
        goto(S, 'share', {'shareTab': 'pv'}, wait_sel='[id="pvN_0_pen"]')
        T = '벌칙 초고 T6b'
        put(S, '[id="pvN_0_pen"]', T)
        tab(S, 'txt')
        tab(S, 'pv')
        a = val(S, '[id="pvN_0_pen"]')
        rec(S, 'T6b', a == T, '벌칙 추가 pvN_0_pen 글 → 📝 Text 탭 → 다시 ⚡ 탭 = 그대로', dict(typed=T, after=a), hut=True)
    except Exception as e:
        ex(S, 'T6b', e)
    # c 설정 시험 이름(미리 채운 칸)
    try:
        sx = '#examList input[data-xi="ex1"][data-xk="name"]'
        goto(S, 'set', wait_sel=sx)
        T = '제64회 변리사 1차(초고 T6c)'
        put(S, sx, T, 'fill')
        h1, ok1 = nav(S, 'share')
        h2, ok2 = nav(S, 'set')
        QC.until(pg, "(s) => !!document.querySelector(s)", 5000, '설정 다시', arg=sx)
        a = val(S, sx)
        saved = pg.evaluate("() => settings.exams.find(x => x.id === 'ex1').name")
        rec(S, 'T6c', ok1 and ok2 and a == T and saved != T, '설정 시험 이름(미리 채운 칸) 글 → Share 화면 → 다시 설정 = 그대로(아직 저장 안 함)',
            dict(typed=T, nav=[h1, h2], after=a, saved=saved), hut=True)
    except Exception as e:
        ex(S, 'T6c', e)
    # d 댓글(접기 → 펴기)
    try:
        goto(S, 'share', {'shareTab': 'txt'}, cm={'t1': True}, wait_sel='[id="shC_t1"]')
        T = '댓글 초고 T6d'
        put(S, '[id="shC_t1"]', T)
        press(S, '#main [onclick="shareCmTog(\'t1\')"]')
        QC.until(pg, "() => !document.getElementById('shC_t1') && _inUi === false", 5000, '댓글 접힘')
        press(S, '#main [onclick="shareCmTog(\'t1\')"]')
        QC.until(pg, "() => !!document.getElementById('shC_t1') && _inUi === false", 5000, '댓글 펴짐')
        a = val(S, '[id="shC_t1"]')
        rec(S, 'T6d', a == T, '댓글 shC_t1 글 → 댓글 접기 → 다시 펴기 = 그대로', dict(typed=T, after=a), hut=True)
    except Exception as e:
        ex(S, 'T6d', e)


# ════════════════════ 관문 T7 — 「올리기 · 저장」 뒤 되살아남 0 ════════════════════
def away_back(S, view, wait_sel):
    """화면 하나 갔다 옴(사람 누름) — share 면 다른 탭 칩, 아니면 다른 화면"""
    if view == 'share':
        cur = S.page.evaluate("() => ui.shareTab")
        tab(S, 'img' if cur != 'img' else 'txt')
        tab(S, cur)
    else:
        nav(S, 'share' if view != 'share' else 'plan')
        nav(S, view)
    QC.until(S.page, "(s) => !!document.querySelector(s)", 5000, '다시 그림', arg=wait_sel)


def chk_after(S, cid, title, view, sels, want, wait_sel, info, share_sync=None):
    a0 = [val(S, s) for s in sels]
    away_back(S, view, wait_sel)
    a1 = [val(S, s) for s in sels]
    st = sync(S, share=(view == 'share') if share_sync is None else share_sync)
    a2 = [val(S, s) for s in sels]
    ok = a0 == want and a1 == want and sync_ok(st) and a2 == want
    info = dict(info)
    info.update(after_save=a0, after_away_back=a1, sync=st, after_sync=a2, want=want)
    rec(S, cid, ok, title, info)


def t7a(S):
    goto(S, 'share', {'shareTab': 'txt'}, cm={'t1': True}, wait_sel='[id="shC_t1"]')
    sel, v = '[id="shC_t1"]', '댓글 T7a %s' % S.dev[:2]
    put(S, sel, v)
    S.page.keyboard.press('Enter')
    QC.until(S.page, "(v) => (shareFile().data.items.find(x => x.id === 't1').cm || []).some(c => c.t === v) && _inUi === false", 8000, '댓글 달림', arg=v)
    chk_after(S, 'T7a', '댓글 shC_t1 Enter(달기) 뒤 빈 칸 → 탭 오감 → syncAll 뒤에도', 'share', [sel], [''], sel, dict(typed=v))


def t7b(S):
    goto(S, 'share', {'shareTab': 'ai'}, wait_sel='#aiT')
    v = '클로드 글 T7b'
    put(S, '#aiT', v)
    press(S, ('#main .aicomp .aiapp', 'tt'))
    QC.until(S.page, "() => aiSel.length > 0 && _inUi === false", 5000, '앱 고름')
    press(S, '#main .aicomp button.btn.p')
    QC.until(S.page, "(v) => aiPosts().some(x => x.t === v) && _inUi === false", 8000, '🤖 올림', arg=v)
    chk_after(S, 'T7b', '🤖 aiT 「올리기」 뒤 빈 칸 → 탭 오감 → syncAll 뒤에도', 'share', ['#aiT'], [''], '#aiT', dict(typed=v))


def t7c(S):
    goto(S, 'share', {'shareTab': 'ai'}, ai_new=True, wait_sel='#aiNew')
    v = '새앱T7c'
    put(S, '#aiNew', v)
    S.page.keyboard.press('Enter')
    QC.until(S.page, "(v) => aiApps().some(x => x.t === v) && !document.getElementById('aiNew') && _inUi === false", 8000, '앱 넣음', arg=v)
    press(S, '#main .aicomp .aiapp.new')
    QC.until(S.page, "() => !!document.getElementById('aiNew') && _inUi === false", 5000, '새 앱 칸 다시')
    a = val(S, '#aiNew')
    rec(S, 'T7c', a == '', '🤖 새 앱 aiNew Enter(넣기) 뒤 「＋ 새 앱」 다시 열면 빈 칸', dict(typed=v, reopened=a))


def t7d(S):
    goto(S, 'share', {'shareTab': 'pv'}, wait_sel='[id="pvN_0_pen"]')
    put(S, '[id="pvN_0_pen"]', '벌칙 T7d %s' % S.dev[:2])
    put(S, '[id="pvW_0_pen"]', '3', 'fill')
    press(S, '#main .pvadd:has([id="pvN_0_pen"]) button')
    QC.until(S.page, "() => shareItems('pv').some(x => x.t.indexOf('벌칙 T7d') === 0 && x.w === 3) && _inUi === false", 8000, '벌칙 추가')
    chk_after(S, 'T7d', '⚡ 벌칙 ＋(추가) 뒤 이름 빈 칸 · 무게 = 그려진 1 → 탭 오감 → syncAll 뒤에도', 'share',
              ['[id="pvN_0_pen"]', '[id="pvW_0_pen"]'], ['', '1'], '[id="pvN_0_pen"]', {})


def t7e(S):
    goto(S, 'day', wait_sel='#cmT')
    put(S, '#cmT', '공통 할일 T7e %s' % S.dev[:2])
    put(S, '#cmD', '2026-10-20', 'fill')
    press(S, '#main button[onclick="cmAdd()"]')
    QC.until(S.page, "() => __hk.items('todos/공통.json').some(x => x.t.indexOf('공통 할일 T7e') === 0 && x.due === '2026-10-20') && _inUi === false", 8000, '공통 할일 추가')
    chk_after(S, 'T7e', '공통 할일 「추가」 뒤 cmT · cmD 빈 칸 → 화면 오감 → syncAll 뒤에도', 'day', ['#cmT', '#cmD'], ['', ''], '#cmT', {})


def t7f(S):
    goto(S, 'day', wait_sel='[id="addS_1"]')
    put(S, '[id="addS_1"]', '학습 T7f')
    S.page.keyboard.press('Enter')
    QC.until(S.page, "() => todoFile(cfg.person).data.items.some(x => x.t === '학습 T7f' && x.kind === 'study') && _inUi === false", 8000, '학습 추가')
    chk_after(S, 'T7f', '오늘 「+ 학습 추가」 Enter 뒤 빈 칸 → 화면 오감 → syncAll 뒤에도', 'day', ['[id="addS_1"]'], [''], '[id="addS_1"]', {})


def t7g(S):
    goto(S, 'day', wait_sel='[id="addT_1"]')
    # PC 타임테이블 화면의 오늘 칸은 좁아 할일 칸 가운데를 다른 요소가 덮음 — 클릭이 8 초 막힘(10/9 첫·둘째 판 잼 · 바탕도 같음 · 앱 무관) → 누르지 않고 포커스 · 덮은 요소는 값에 적음
    hit = S.page.evaluate("""() => { const a = document.getElementById('addT_1'), d = document.getElementById('due_1'); const r = a.getBoundingClientRect(), q = d.getBoundingClientRect();
        const e = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
        return {addT: [Math.round(r.left), Math.round(r.width)], due: [Math.round(q.left), Math.round(q.width)], at_center: e ? (e.id || e.tagName + '.' + e.className) : null} }""")
    loc(S, '[id="addT_1"]').focus()
    S.page.keyboard.insert_text('할일 T7g')
    loc(S, '[id="due_1"]').fill('2026-10-22')   # 날짜 칸도 누르지 않고 채움(크롬 날짜 고르개가 옆 칸을 덮음 · 첫 판 잼)
    loc(S, '[id="addT_1"]').focus()
    S.page.keyboard.press('Enter')
    QC.until(S.page, "() => todoFile(cfg.person).data.items.some(x => x.t === '할일 T7g' && x.due === '2026-10-22') && _inUi === false", 8000, '할일 추가')
    chk_after(S, 'T7g', '오늘 「+ 할일 추가」 + 기한 Enter 뒤 둘 다 빈 칸 → 화면 오감 → syncAll 뒤에도', 'day',
              ['[id="addT_1"]', '[id="due_1"]'], ['', ''], '[id="addT_1"]', dict(layout=hit))


def t7h(S):
    goto(S, 'day', wait_sel='#mA')
    put(S, '#mA', '13:00', 'fill')
    put(S, '#mB', '14:10', 'fill')
    press(S, '#main button[onclick^="manualSave"]')
    QC.until(S.page, "() => sessionsOf(cfg.person, curDate()).some(x => x.a === 780 && x.b === 850) && _inUi === false", 8000, '이날기록 저장')
    chk_after(S, 'T7h', '이날기록 mA · mB 「저장」 뒤 빈 칸 → 화면 오감 → syncAll 뒤에도', 'day', ['#mA', '#mB'], ['', ''], '#mA', {})


def t7i(S):
    goto(S, 'plan', {'planTab': 'list'}, wait_sel='#lsNN')
    put(S, '#lsNT', '분류T7i')
    put(S, '#lsNW', '20~18')
    put(S, '#lsNP', '3', 'fill')
    put(S, '#lsNN', '활동 T7i')
    S.page.keyboard.press('Enter')
    QC.until(S.page, "() => myPlan().bands.some(b => b.name === '활동 T7i' && !b.del) && _inUi === false", 8000, '활동 추가')
    ss = ['#lsNT', '#lsNN', '#lsNW', '#lsNP']
    chk_after(S, 'T7i', '새 활동 줄 Enter(추가) 뒤 분류·이름·주차·주당 빈 칸 → 화면 오감 → syncAll 뒤에도', 'plan', ss, ['', '', '', ''], '#lsNN', {})


def t7j(S):
    sx = '#examList input[data-xi="ex1"][data-xk="name"]'
    goto(S, 'set', wait_sel=sx)
    v1, v2 = '제64회 변리사 1차(저장 T7j)', '11'
    put(S, sx, v1, 'fill')
    put(S, '#rH', v2, 'fill')
    press(S, '#main button[onclick="applySettings()"]')
    QC.until(S.page, "(v) => settings.redHours === 11 && settings.exams.find(x => x.id === 'ex1').name === v && _inUi === false", 8000, '설정 저장', arg=v1)
    chk_after(S, 'T7j', '설정 「설정 저장」 뒤 칸 = 저장값(미리 채운 칸) → 화면 오감 → syncAll 뒤에도', 'set', [sx, '#rH'], [v1, v2], sx, {}, share_sync=False)


def t7k(S):
    goto(S, 'set', wait_sel='#tok')
    v = 'ghp_t7k_token'
    put(S, '#tok', v, 'fill')
    n = S.n + 1
    S.n = n
    S.page.evaluate("() => { try { clearTimeout(syncT) } catch (e) {} return 1 }")
    QC.until(S.page, "() => !syncing && _inUi === false", 20000, '동기화 빔')
    S.gh.change(n, False)
    press(S, ('#main button', '저장 후 동기화'))
    QC.until(S.page, "(n) => !syncing && __hk.has('todos/공통.json', 'rc' + n) && _inUi === false", 20000, '저장 후 동기화', arg=n)
    chk_after(S, 'T7k', '설정 토큰 「저장 후 동기화」(await 뒤 render) 뒤 칸 = 저장값 → 화면 오감 → syncAll 뒤에도', 'set', ['#tok'], [v], '#tok',
              dict(cfg_token=S.page.evaluate("() => cfg.token")), share_sync=False)


def t7l(S):
    goto(S, 'plan', {'planTab': 'list'}, wait_sel=ls_td('name'))
    T = '활동 저장 T7l'
    press(S, ls_td('name'))
    QC.until(S.page, "(s) => !!document.querySelector(s) && document.activeElement === document.querySelector(s)", 5000, '칸 수정 열림', arg=ED_LS)
    S.page.keyboard.insert_text(T)
    S.page.keyboard.press('Enter')
    QC.until(S.page, "([t, s]) => myPlan().bands.find(x => x.id === 'b1').name === t && !document.querySelector(s) && _inUi === false", 5000, '칸 저장', arg=[T, ED_LS])
    away_back(S, 'plan', ls_td('name'))
    e1 = S.page.evaluate("(s) => !!document.querySelector(s)", ED_LS)
    st = sync(S, share=False)
    e2 = S.page.evaluate("(s) => !!document.querySelector(s)", ED_LS)
    cell = S.page.evaluate("(s) => { const e = document.querySelector(s); return e ? e.textContent : null }", ls_td('name'))
    rec(S, 'T7l', not e1 and sync_ok(st) and not e2 and cell == T, 'lsInline Enter(저장) 뒤 화면 오감 · syncAll = 칸 수정 다시 안 열림 · 칸 = 저장값',
        dict(typed=T, editor_after_nav=e1, sync=st, editor_after_sync=e2, cell=cell))


def t7m(S):
    goto_exam(S)
    T = '비고 저장 T7m'
    press(S, EX_TD)
    QC.until(S.page, "(s) => !!document.querySelector(s) && document.activeElement === document.querySelector(s)", 5000, '비고 칸 열림', arg=ED_EX)
    S.page.evaluate("(s) => { document.querySelector(s).select(); return 1 }", ED_EX)   # exInline 은 포커스만(고름 없음) — 앞 칸(T4) 비고를 갈아 끼우려고 전체 고름(10/9 첫 판 잼: 이어 붙음)
    S.page.keyboard.insert_text(T)
    S.page.keyboard.press('Enter')
    QC.until(S.page, "([id, t, s]) => examGet(id).q[0].note === t && !document.querySelector(s) && _inUi === false", 5000, '비고 저장', arg=[EXAM_ID, T, ED_EX])
    nav(S, 'share')
    nav(S, 'arch')
    QC.until(S.page, "(s) => !!document.querySelector(s)", 5000, '시험기록 다시', arg=EX_TD)
    e1 = S.page.evaluate("(s) => !!document.querySelector(s)", ED_EX)
    st = sync(S, share=False)
    e2 = S.page.evaluate("(s) => !!document.querySelector(s)", ED_EX)
    cell = S.page.evaluate("(s) => { const e = document.querySelector(s); return e ? e.textContent : null }", EX_TD)
    rec(S, 'T7m', not e1 and sync_ok(st) and not e2 and cell == '📝 ' + T, 'exInline 비고 Enter(저장) 뒤 화면 오감 · syncAll = 칸 수정 다시 안 열림 · 칸 = 저장값',
        dict(typed=T, editor_after_nav=e1, sync=st, editor_after_sync=e2, cell=cell))


def t7n(S):
    goto_exam(S)
    n0 = ex_note(S)
    press(S, EX_TD)
    QC.until(S.page, "(s) => !!document.querySelector(s) && document.activeElement === document.querySelector(s)", 5000, '비고 칸 열림', arg=ED_EX)
    S.page.keyboard.insert_text('취소할 글')
    S.page.keyboard.press('Escape')
    QC.until(S.page, "(s) => !document.querySelector(s) && _inUi === false", 5000, '비고 칸 닫힘', arg=ED_EX)
    st = sync(S, share=False)
    e2 = S.page.evaluate("(s) => !!document.querySelector(s)", ED_EX)
    n1 = ex_note(S)
    rec(S, 'T7n', sync_ok(st) and not e2 and n1 == n0, 'exInline 비고 Esc(취소) = 저장 안 함 · syncAll 뒤 칸 수정 다시 안 열림',
        dict(note_before=n0, sync=st, editor_after_sync=e2, note_after=n1))


T7_PC = [t7a, t7b, t7c, t7d, t7e, t7f, t7g, t7h, t7i, t7j, t7k, t7l, t7m, t7n]
T7_PHONE = [t7a, t7d, t7e, t7h, t7l, t7m]


def t7(S, fns):
    for f in fns:
        try:
            f(S)
        except Exception as e:
            ex(S, f.__name__.upper(), e)


# ════════════════════ 관문 T8 · T9 · T0 · TX ════════════════════
def t8(S):
    goto(S, 'share', {'shareTab': 'txt'}, wait_sel='#shT')
    T = '지울 글 T8'
    put(S, '#shT', T)
    tab(S, 'img')
    tab(S, 'txt')
    a0 = val(S, '#shT')
    loc(S, '#shT').fill('')   # 손으로 다 지움(input 이벤트)
    tab(S, 'img')
    tab(S, 'txt')
    a1 = val(S, '#shT')
    rec(S, 'T8', a1 == '', '칸을 손으로 다 지우면 기억도 지움 — 지운 뒤 탭 오감 = 빈 칸(되살아남 0)', dict(typed=T, restored_before_clear=a0, after=a1))


def t9(S):
    goto(S, 'share', {'shareTab': 'txt'}, wait_sel='#shT')
    T = '기기 저장 시험 T9 %s' % S.dev[:2]
    put(S, '#shT', T)
    tab(S, 'img')
    hits = S.page.evaluate("(t) => __hk.stores(t)", T)
    S.page.reload(wait_until='load')
    booted = S.boot()
    view = S.page.evaluate("() => [ui.view, ui.shareTab]")
    if view[1] != 'txt':
        tab(S, 'txt')
    QC.until(S.page, "() => !!document.getElementById('shT')", 5000, 'shT')
    a = val(S, '#shT')
    rec(S, 'T9', not hits and booted and a == '', '기기 저장 안 함 — 탭 옮긴 뒤 localStorage · sessionStorage 에 친 글 0 · 새로고침 뒤 빈 칸',
        dict(typed=T, store_hits=hits, rebooted=booted, ui=view, after_reload=a))


SCAN = [('share 🖼 Image', 'share', {'shareTab': 'img'}), ('share 📝 Text', 'share', {'shareTab': 'txt'}),
        ('share ⚡ 벌칙포상', 'share', {'shareTab': 'pv'}), ('share 🤖 클로드', 'share', {'shareTab': 'ai'}),
        ('계획 주차별', 'plan', {'planTab': 'week'}), ('계획 리스트', 'plan', {'planTab': 'list'}),
        ('설정', 'set', {}), ('타임테이블', 'day', {}), ('Archive 음식', 'arch', {'archTab': 'food'}),
        ('Archive 시험기록', 'arch', {'archTab': 'exam', 'exTab': 'db', 'exCha': 1, 'exWho': ME, 'exSel': EXAM_ID})]


def t0(S):
    per = {}
    for lab, view, ui in SCAN:
        e0 = len(S.errs())
        try:
            goto(S, view, ui, wait_sel='#main > *')
            ok_draw = S.page.evaluate("() => document.getElementById('main').children.length > 0")
        except Exception as e:
            per[lab] = 'ex: ' + str(e)[:120]
            continue
        per[lab] = (len(S.errs()) - e0) if ok_draw else 'no-draw'
    bad = {k: v for k, v in per.items() if v != 0}
    rec(S, 'T0', not bad, '화면 훑기(share 네 탭 · 계획 둘 · 설정 · 타임테이블 · Archive 음식 · 시험기록) 오류 0', dict(per_view=per, errs=S.errs()[:5]))


def tx(S):
    e = S.errs()
    rec(S, 'TX', not e, '이 문맥 처음부터 끝까지 스크립트 오류 0(window error · unhandledrejection · pageerror · console.error)',
        dict(n=len(e), errs=e[:6], blocked=sorted(set(S.gh.blocked))[:5]))


RUN = {'T0': t0, 'T1a': t1a, 'T1b': t1b, 'T1c': t1c, 'T1d': t1d, 'T2': t2,
       'T3': lambda S: t3(S, 'name', 'T3'), 'T3p': lambda S: t3(S, 'per', 'T3p'), 'T4': t4,
       'T5': None, 'T6': t6, 'T7': lambda S: t7(S, T7_PC), 'T7w': lambda S: t7(S, T7_PHONE), 'T8': t8, 'T9': t9, 'TX': tx}


def run_dev(browser, dev, app, base, plan):
    S = Sess(browser, dev, app, base)
    try:
        if not S.booted:
            rec(S, 'TB', False, '부팅 — render · syncAll · keepInputGrab · #main', dict(errs=S.errs()[:5]))
            return
        for k in plan:
            if ONLY and not any(k == o or k.startswith(o) or o.startswith(k) for o in ONLY):
                continue
            with QC.stage('%s %s %s' % (dev, 'base' if base else 'new', k)):
                try:
                    if k == 'T5':
                        t5(S, app)
                    else:
                        RUN[k](S)
                except Exception as e:
                    ex(S, k, e)
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
    t0_ = time.time()
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
    hut_n = hut_ok = 0
    if QC.GATE:   # 헛잣대 줄 — 바탕에서 FAIL 이어야 할 칸
        for r in [x for x in ROWS if x['side'] == 'new' and x['hut'] is True and not x['info']]:
            b = [x for x in ROWS if x['side'] == 'base' and x['cid'] == r['cid'] and x['dev'] == r['dev']]
            if not b:
                continue
            bst = b[0]['st']
            hut_n += 1
            hut_ok += 1 if bst == 'FAIL' else 0
            out('%s | %s-헛 %s · 헛잣대 — 바탕 %s 에서 %s(%s) | %s' % ('PASS' if bst == 'FAIL' else 'FAIL', r['cid'], r['dev'], BASE, bst,
                                                             '잣대가 가름' if bst == 'FAIL' else '잣대가 안 가름', b[0]['title'][:60]))
    newl = [x for x in ROWS if x['side'] == 'new' and not x['info']]
    np_ = sum(1 for x in newl if x['st'] == 'PASS')
    nf = sum(1 for x in newl if x['st'] == 'FAIL')
    ver = [ln for ln in LINES if ln.startswith(('PASS', 'FAIL')) and ' | BASE ' not in ln]
    p = sum(1 for ln in ver if ln.startswith('PASS'))
    f = sum(1 for ln in ver if ln.startswith('FAIL'))
    sec = round(time.time() - t0_, 1)
    table = summary_table()
    head = '새 판 칸 PASS %d · FAIL %d · 헛잣대 바탕 FAIL %d/%d(가름)' % (np_, nf, hut_ok, hut_n)
    out('%s · 합계 PASS %d · FAIL %d  (mode %s · %.1f 초)' % (head, p, f, QC.MODE, sec))
    write_res(table, p, f, sec, head)
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
        hut = n[0]['hut'] if n else (b[0]['hut'] if b else False)
        info = any(x['info'] for x in n + b)
        ns = n[0]['st'] if n else '—'
        bs = b[0]['st'] if b else '—'
        if info:
            exp, j = '(INFO)', '—'
        elif not b:
            exp, j = ('FAIL' if hut is True else 'PASS' if hut is False else '(참고)'), '—'
        elif hut is True:
            exp, j = 'FAIL', ('OK(가름)' if bs == 'FAIL' else '✗ 안 가름')
        elif hut is None:
            exp, j = '(참고)', '바탕 ' + bs
        else:
            exp, j = 'PASS', (('바탕도 같음' if ns == 'PASS' else '✗ 새 판만 FAIL') if bs == 'PASS' else '✗ 바탕 FAIL(뜻밖)')
        lines.append('%s | %s | %s | %s | %s | %s' % (cid, dev, ns, bs, exp, j))
    return lines


def write_res(table, p, f, sec, head):
    hd = ['# _harness_tt_drafts2 결과 — %s · mode %s · %.1f 초' % (time.strftime('%Y-%m-%d %H:%M:%S'), QC.MODE, sec),
          '# NEW %s · BASE %s' % (NEWF, BASE if QC.GATE else '(안 띄움)'), '# ' + head, '']
    body = '\n'.join(hd + LINES + ['', '== 칸별 표(새 판 · 바탕 = 헛잣대) =='] + table + ['', '합계  PASS %d · FAIL %d' % (p, f)]) + '\n'
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
