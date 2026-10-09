# -*- coding: utf-8 -*-
r"""tt앱 — 보는 날짜를 바꾸면 「이날기록추가」 시각 칸 둘(mA · mB)을 비움 관문 (tt 작은 판 · 2026-10-10)
  근거 = 결정로그 10/10 00:34 [사용자 · 채팅에서](00:26 「해」 = 보는 날짜를 바꾸면 비움) · 00:34 [채팅] 「tt 작은 판 · 진행」(지시서 파일 없이 그 줄이 지시서)
  고친 자리 = timetable/index.html setDate 한 곳(+ 새 mDayDrop) — 날짜를 바꾸는 길은 다 setDate 로 온다(grep 전수 = 아래 M1 길)

  python _harness_tt_mdate.py [--mode gate|regress|smoke] [--new <앱 html>] [--base <git 판 | 앱 html>] [--res <결과 파일>]
                              [--only M1a,M3,…] [--engines chromium,webkit] [--devs chromium-pc]

  NEW  = 이 판 앱(기본 GENIE_ROOT timetable/index.html — 워크트리·사슬 실행기가 GENIE_ROOT 를 준다 · 없으면 _roots.genie())
  BASE = 헛잣대(기본 genie git 7299ec3 = 10/9 tt 둘째 판 · 0770d21 과 같은 바이트 md5 4c802bce · 만들 때의 _roots.base_rev()) — gate 에서만 띄운다
  기기 = Chromium PC 1100×800(클릭) → 그 브라우저를 닫고 WebKit 폰 390(hasTouch · 진짜 터치 톡 = locator.tap) · 브라우저는 한 번에 하나 · 판·기기마다 새 문맥
  앱 자리 · 가짜 GitHub · 재그림 표지 · 화면 옮기기 = _harness_tt_drafts2.py 꼴 그대로(진짜 網 막음 · confirm/alert/prompt 스텁 · 날짜 2026-10-09 12:00 KST)
  시드 tt.ui = 일간 · 날짜 빈 칸(= 오늘) · 일간·주간·월간 절 다 펼침(월간 칸 누름 길) · share Text · 공통 할일 빈 파일

  관문:
   M1a~l 시각 칸(mA · mB)에 시각을 넣고 「저장」 안 누름 → 날짜 바꿈 = 두 칸 빔 · 화면 기억(_draft)에 mA · mB 없음                    [헛잣대]
         a 일간 › · b 일간 ‹ · c 일간 「오늘」(지난 날에서) · d 일간 날짜 칸 고름 · e 리본 → 이동 창 날짜 「이동」 · f 리본 → 이동 창 「오늘」 ·
         g 주간 블록 누름(그 날 + 세션 편집 창) · h 월간 칸 누름(ttGoDate) · i (폰) 할일 화면 ‹ · j 데일리 모음 카드 → 「이 날 일간으로」 ·
         k (PC) 작은 창(PiP) 칸 + 본창 칸 → 본창 › = 둘 다 빔 · l (PC) 작은 창 칸 → 작은 창 리본 → 이동 창 「이동」
   M2    날짜 바꾼 뒤(›) 다시 그 날짜로 와도(‹) 빔                                                                                   [헛잣대]
   M3    「저장」 누른 기록 무변 — 저장 → › → ‹ = 그 날 기록 그대로(같은 id · 시각) · 옮긴 날 기록 0 · 칸 빔                          [바탕도 같음]
   M3b   넣다 만 시각 → › → 그대로 「저장」 = 옮긴 날 기록 0(칸이 비어 「시작·끝을 채워줘」) — 사용자가 걱정한 해                        [헛잣대]
   M4    다른 칸 기억 그대로 — share Text(shT) · 공통 할일(cmT) 쓰던 글 → 날짜 바꿈 = 칸 · 화면 기억 값 그대로                           [바탕도 같음]
   M5a~e 날짜를 안 바꾸면 mA · mB 쓰던 값 그대로(둘째 판 동작 무변) — a 화면 오감 · b syncAll · c 같은 날 「오늘」 ·
         d 리본 이동 창 같은 날 「이동」 · e 주간 절 ‹(주간 날짜만 바뀜)                                                               [바탕도 같음]
   M6i   (PC · 참고) 날짜 칸이 빈(ui.date null) 채 하루 경계를 넘김 = setDate 를 안 지나 칸이 남음 — 이 판 범위 밖 · 값만 적음           [INFO]
   TX    그 문맥 처음부터 끝까지 스크립트 오류 0
  헛잣대(gate) = 같은 잣대를 BASE 에 돌린 줄 「BASE <기기> · <칸>」(판정 밖) · [헛잣대] 칸은 「<칸>-헛 <기기>」 줄이 바탕 FAIL 이면 PASS
         — 바탕 FAIL 이 하네스 예외이거나 길이 안 됨(날짜가 안 바뀜 등 · void)이면 「가름」 으로 안 셈(값으로 FAIL 이어야)
  M1d 웹킷 = fill 뒤 change 가 안 나면(윈도 웹킷 · 첫 실행 잼) 칸을 떠남(blur) — 실기기는 날짜 고르개가 change 를 냄
  모드 = gate(NEW + BASE · 결과 N:\개인\claude\timetable\_tt_mdate\result.txt) · regress(NEW 만 · %TEMP%\h_tt_mdate) · smoke(NEW · PC · M1a · M2 · M3 · M4 · M5 · TX)
  ⚠ 고정 대기 없음 — 앱 표지(curDate() · ui.view · _inUi · syncing · 재그림 표지 · 기록 수 · 알림 글)를 기다린다(QC.until)

  ── 덧판(2026-10-10 02:03 · 02:58 [채팅] · 워크트리 tt_mdate2) — 할일 세 칸 아홉 · 하루 경계 ──
  근거 = 결정로그 10/10 02:03 [채팅] 「01:58 물음 답 = 같이 비움 · 진행」(사용자 00:26 「해」 · 규칙 ㊢ · 사용자 20:25 「알아서」) · 02:58 [채팅] 「tt 덧판 = cdbce32 위에 02:03 줄 그대로」
  고친 자리 = timetable/index.html mDayDrop 칸 열하나(M_DAY_IDS = mA · mB + addS_0~2 · addT_0~2 · due_0~2) + dayRoll(지난 today() 기억 · render · syncAll 첫머리 —
         visibilitychange 는 syncAll 로 옴 · ui.date 빈 화면에서 today() 가 바뀌면 mDayDrop 한 번)
  BASE 기본값 = cdbce32(724c4ac 판 · mA·mB 비움 · md5 a524629f · 530,320 B) — 위 「BASE = … 7299ec3」 줄은 옛 줄(--base 7299ec3 로 그대로 돌릴 수 있음)
  헛잣대 세대 — 칸마다 since(그 칸이 PASS 가 되는 판: 1 = 724c4ac mA·mB 비움 · 2 = 이 덧판) · 바탕 세대(바탕 md5 로: 7299ec3 = 0 · cdbce32 = 1 · 모르면 --base-gen 또는 1)
         since 가 바탕 세대보다 큰 칸만 헛잣대(바탕 FAIL 이어야) · 아니면 「바탕도 같음」 — cdbce32 바탕이면 옛 M1 · M2 · M3b 는 바탕도 같음 · 새 M7 · M9b~e 가 헛잣대
   M7a~i 할일 세 칸 아홉(a~c addS_0~2 「+ 학습 추가」 · d~f addT_0~2 「+ 할일 추가」 · g~i due_0~2 기한) 칸마다 글/날짜 넣고 Enter 안 누름 →
         › = 빔 · 다시 ‹(그 날) = 빔 · 화면 기억 없음(PC = 일간 화면 오른쪽 세 칸 · 폰 = 아래 「할일」 화면 ‹ ›)                        [헛잣대 · 세대 2]
         ⚠ PC 덧판 칸(M7~M11)은 창 1600×900 — 1100 폭 일간은 세 칸이 132px 라 「+ 할일 추가」(addT) 폭 0(기한 칸 110px 가 다 먹음 · 10/10 03:5x 잰 값 · 눌러지지 않음)
   M8a~b 아홉 칸 쓰던 글 → 날짜 안 바꾸고 a 화면 오감 · b 원격 변경 syncAll = 그대로(둘째 판 동작 무변 · 오늘 따라가는 화면)             [바탕도 같음]
   M9a   하루 경계 — 오늘 따라가는 화면(ui.date 빈 칸)에 열하나(PC = 일간에 다 · 폰 = 일간 mA·mB 는 화면 기억 + 「할일」 화면 아홉) 쓰던 글 →
         가짜 시계 달력 자정 넘김(10-10 00:01 · 하루 시작 dayStart 5 시 전이라 today() 무변) → render = 그대로                            [바탕도 같음]
   M9b~d 이어서 하루 시작 넘김(10-10 05:01 · today() 바뀜 · 시계 옮김과 일으킴은 한 evaluate 안) → b render(사용자 조작 밖) · c visibilitychange ·
         d syncAll = 열하나 빔 · 화면 기억 없음(c · d 는 동기화 끝난 뒤도 · 폰은 그 뒤 일간으로 가 mA · mB 빔까지)                       [헛잣대 · 세대 2]
   M9e   (PC) 작은 창(PiP) 칸 + 본창 칸 → 하루 시작 넘김 → render = 둘 다 빔                                                         [헛잣대 · 세대 2]
   M9i   (참고) 하루 시작 넘김 → visibilitychange · 원격 변경 없음 = 본창을 다시 안 그림(가운데 「오늘」 칸 머리 날짜 = 옛 날) — 앱 기존 동작 · 값만 [INFO]
   M10   날짜 박힌 화면(ui.date = 10-09) 하루 시작 넘김 → render · syncAll = 열하나 그대로(보는 날짜가 안 바뀜 — 판단)                 [바탕도 같음]
   M11a~b 다른 칸 기억 그대로 — share 글(shT) · 공통 할일(cmT) · 지은 기억(계획 목록 lsNT · 메모 snMemo) → a 하루 시작 넘김(render) · b 날짜 바꿈(›) [바탕도 같음]
   M6i 는 그대로 INFO(덧판에서는 빔 — 관문은 M9) · smoke 에 M7 · M9 더함 · 시계 옮긴 칸은 끝에 옮긴 만큼 되돌리고 render(finally)
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
# 옛 줄: BASE = ARG('--base', '7299ec3')
# 옛 줄: BASE_MD5 = '4c802bce41beeecb5b0111c2321f0e3f'   # 7299ec3 = 0770d21 timetable/index.html 529,186 B(10/9 23:18 push · tt 둘째 판)
BASE = ARG('--base', 'cdbce32')   # 덧판(10/10 tt_mdate2) — 헛잣대 = 724c4ac 판(mA·mB 비움 · 7ff353d 합치기 · cdbce32 _qa 커밋 = 같은 앱 바이트)
BASE_MD5 = 'a524629f798eb91371bc2ce5356f7ebd'   # cdbce32 = 7ff353d = 724c4ac timetable/index.html 530,320 B(10/10 01:5x push · tt 작은 판)
GEN_MD5 = {'4c802bce41beeecb5b0111c2321f0e3f': 0, 'a524629f798eb91371bc2ce5356f7ebd': 1}   # 바탕 세대 — 0 = 7299ec3(둘째 판) · 1 = cdbce32(mA·mB 비움)
BASE_GEN = None   # gate 에서 바탕을 꺼낸 뒤 정함(md5 → GEN_MD5 · 모르면 --base-gen 또는 1) · regress · smoke 는 None(바탕 안 띄움)
ONLY = [x.strip() for x in (ARG('--only', '') or '').split(',') if x.strip()]
ENGINES = [x.strip() for x in (ARG('--engines', 'chromium,webkit') or '').split(',') if x.strip()]
DEVS = [x.strip() for x in (ARG('--devs', '') or '').split(',') if x.strip()]
_TMPD = os.path.join(tempfile.gettempdir(), 'h_tt_mdate')
if QC.GATE:
    _nres = _roots.n('timetable', '_tt_mdate', 'result.txt')
    RES = ARG('--res', _nres or os.path.join(_TMPD, 'result.txt'))
else:
    RES = ARG('--res', os.path.join(_TMPD, 'result.txt'))

APP_URL = 'https://api.github.com/__tt/timetable/index.html'
GH = 'https://api.github.com/repos/zzikkaplan/studyplandata/contents/'
ME, OT = '꼬까', '햄찌'
T0 = int(datetime.datetime(2026, 10, 9, 9, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))).timestamp() * 1000)
D0 = '2026-10-09'   # 가짜 시계의 오늘(12:00 KST · 하루 시작 5 시)
TYPED = ['09:00', '10:30']

DEV = {
    'chromium-pc': ('chromium', dict(viewport={'width': 1100, 'height': 800})),
    'webkit-phone': ('webkit', dict(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2)),
}
PLAN = {   # 기기마다 돌릴 관문(차례대로)
    # 옛 줄:     'chromium-pc': ['M1a', 'M1b', 'M1c', 'M1d', 'M1e', 'M1f', 'M1g', 'M1h', 'M1j', 'M1k', 'M1l', 'M2', 'M3', 'M3b', 'M4', 'M5', 'M6i', 'TX'],
    # 옛 줄:     'webkit-phone': ['M1a', 'M1b', 'M1c', 'M1d', 'M1e', 'M1f', 'M1g', 'M1h', 'M1i', 'M1j', 'M2', 'M3', 'M3b', 'M4', 'M5', 'TX'],
    'chromium-pc': ['M1a', 'M1b', 'M1c', 'M1d', 'M1e', 'M1f', 'M1g', 'M1h', 'M1j', 'M1k', 'M1l', 'M2', 'M3', 'M3b', 'M4', 'M5', 'M6i',
                    'M7', 'M8', 'M9', 'M10', 'M11', 'TX'],   # 덧판 — M7~M11 은 TX 앞
    'webkit-phone': ['M1a', 'M1b', 'M1c', 'M1d', 'M1e', 'M1f', 'M1g', 'M1h', 'M1i', 'M1j', 'M2', 'M3', 'M3b', 'M4', 'M5',
                     'M7', 'M8', 'M9', 'M10', 'M11', 'TX'],
}
# 옛 줄: SMOKE_PLAN = {'chromium-pc': ['M1a', 'M2', 'M3', 'M4', 'M5', 'TX']}
SMOKE_PLAN = {'chromium-pc': ['M1a', 'M2', 'M3', 'M4', 'M5', 'M7', 'M9', 'TX']}

# ════════════════════ 시드 ════════════════════
SHARE0 = {'v': 1, 'items': [
    {'id': 't1', 'ty': 'txt', 'text': '씨앗 글 하나', 'by': OT, 'grp': '', 'at': T0, 'u': T0, 'del': False, 'cm': []}]}
COMMON0 = {'v': 1, 'items': []}
SEED = {
    'tt.cfg': {'person': ME, 'token': '', 'lastSync': 0},
    'tt.ui': {'view': 'day', 'shareTab': 'txt', 'date': None, 'galMonth': None, 'ttFold': {'day': False, 'week': False, 'month': False}},
    'tt.f.share/share.json': {'data': SHARE0, 'sha': 'r0', 'dirty': False},
    'tt.f.todos/공통.json': {'data': COMMON0, 'sha': 'r0', 'dirty': False},
}
REMOTE0 = {'share/share.json': SHARE0, 'todos/공통.json': COMMON0}

INIT_JS = r"""(() => {
 if (!String(location.href).startsWith('https://api.github.com/__tt/')) return;
 if (window.__hk) return;
 const R = Date; let OFF = new R('2026-10-09T12:00:00+09:00').getTime() - R.now();
 function D(...a) { return a.length ? new R(...a) : new R(R.now() + OFF) }
 D.prototype = R.prototype; D.now = () => R.now() + OFF; D.parse = R.parse; D.UTC = R.UTC; window.Date = D;
 window.__hkShift = ms => { OFF += ms; return new R(R.now() + OFF).toISOString() };   // M6i(참고) 하루 경계 넘김
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
 };
})();"""
BOOT_JS = ("() => typeof render === 'function' && typeof syncAll === 'function' && typeof setDate === 'function' && typeof keepInputGrab === 'function'"
           " && !!window.__hk && !!document.getElementById('main') && document.getElementById('main').children.length > 0")
# 화면 옮기기(사용자 조작 밖 render) — _harness_tt_drafts2 GOTO_JS 그대로(모달 · 작은 창 흉내 걷기 · #main 글 칸을 그려진 값으로 · 화면 기억 비움 · 포커스 빼기 · 상태 맞춤)
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
# 작은 창 흉내 = documentPictureInPicture 대신 같은 출처 iframe 을 pipWin 으로(_harness_tt_drafts2 T5 꼴) — 앱 CSS 를 안 옮겨 이날기록 칸이 보인다
PIP_OPEN_JS = r"""(names) => {
 let f = document.getElementById('hkPip');
 if (!f) { f = document.createElement('iframe'); f.id = 'hkPip';
  f.style.cssText = 'position:fixed;right:0;bottom:0;width:520px;height:380px;z-index:2147483000;background:#fff;border:2px solid #888';
  document.body.appendChild(f); }
 const w = f.contentWindow; w.document.open(); w.document.write('<!doctype html><html><head><meta charset="utf-8"></head><body></body></html>'); w.document.close();
 names.forEach(n => { try { w[n] = window[n] } catch (e) {} });
 pipWin = w; pipPaint(); return !!w.document.getElementById('mA') }"""
PIP_CLOSE_JS = "() => { try { pipWin = null } catch (e) {} const f = document.getElementById('hkPip'); if (f) f.remove(); return 1 }"
# mA · mB 상태(본창 · 작은 창 · 화면 기억 열쇠)
MSTATE_JS = r"""() => { const g = (D, id) => { const e = D && D.getElementById(id); return e ? e.value : null };
 let pd = null; try { pd = (pipWin && !pipWin.closed) ? pipWin.document : null } catch (e) {}
 return {date: curDate(), view: ui.view, mA: g(document, 'mA'), mB: g(document, 'mB'), pA: pd ? g(pd, 'mA') : null, pB: pd ? g(pd, 'mB') : null,
   draft: ['mA', 'mB', 'pip:mA', 'pip:mB'].filter(k => _draft.has(k)).map(k => k + '=' + (_draft.get(k) || {}).v)} }"""
DRAFT_OTHERS_JS = r"""() => { const o = {}; _draft.forEach((v, k) => { if (!/^(pip:)?m[AB]$/.test(k) && k !== '#ed') o[k] = v && v.v }); return o }"""

# ════════════════════ 결과 ════════════════════
LINES, ROWS = [], []


def out(s):
    print(s, flush=True)
    LINES.append(s)


def J(v, n=1200):
    return json.dumps(v, ensure_ascii=False, default=str)[:n]


# 옛 줄: def rec(S, cid, ok, title, val, hut=False, info=False, void=False):
def rec(S, cid, ok, title, val, hut=False, info=False, void=False, since=1):
    """hut = True(바탕에서 FAIL 이어야 · 헛잣대) · False(바탕도 PASS · 되돌림 막이) · None(바탕은 참고만)
       void = True(재려던 길이 안 됨 — 날짜가 안 바뀜 등 · 바탕 FAIL 이어도 「가름」 으로 안 셈)
       since = 그 칸이 PASS 가 되는 판 세대(덧판 10/10 — 1 = 724c4ac mA·mB 비움 · 2 = 덧판 아홉 · 하루 경계) · 바탕 세대 이하면 헛잣대 아님(eff_hut)"""
    st = 'INFO' if info else ('PASS' if ok else 'FAIL')
    if S.base:
        line = '%s | BASE %s · %s %s | %s' % (st, S.dev, cid, title, J(val))
    else:
        line = '%s | %s %s · %s | %s' % (st, cid, S.dev, title, J(val))
    # 옛 줄: ROWS.append(dict(cid=cid, dev=S.dev, side='base' if S.base else 'new', st=st, title=title, hut=hut, info=info, void=bool(void)))
    ROWS.append(dict(cid=cid, dev=S.dev, side='base' if S.base else 'new', st=st, title=title, hut=hut, info=info, void=bool(void), since=since))
    out(line)
    return ok


def eff_hut(r):
    """덧판 — 헛잣대 세대: hut True 칸도 since 가 바탕 세대(BASE_GEN) 이하면 False(바탕도 같음이어야) · BASE_GEN 없으면(regress · smoke) 그대로"""
    h = r.get('hut')
    if h is True and BASE_GEN is not None and r.get('since', 1) <= BASE_GEN:
        return False
    return h


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
        add('todos/공통.json', {'id': 'rc%d' % n, 't': '원격 공통 %d' % n, 'due': '', 'who': [ME, OT], 'by': OT, 'at': D0,
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
        self.dev, self.base, self.app = dev, base, app
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


# ════════════════════ 손 · 재기(_harness_tt_drafts2 꼴) ════════════════════
LBL = {'day': '타임테이블', 'gal': '데일리 모음', 'pm': '계획관리', 'plan': '주월계획', 'arch': 'Archive', 'share': 'Share', 'set': '설정', 'todo': '할일'}
MORE = ('gal', 'pm', 'plan', 'arch', 'share', 'set')


def val(S, sel):
    return S.page.evaluate("(s) => __hk.val(s)", sel)


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


def goto(S, view, ui=None, wait_sel=None):
    S.page.evaluate(GOTO_JS, {'view': view, 'ui': ui or {}, 'cm': {}, 'aiNew': False})
    if wait_sel:
        QC.until(S.page, "(s) => !!document.querySelector(s)", 8000, '화면 ' + view, arg=wait_sel)
    QC.until(S.page, "() => _inUi === false", 5000, '_inUi 풀림')


def nav(S, view):
    """사람처럼 화면 옮김 — PC = 옆 차림 #side · 폰 = 아래 #pnav(타임테이블 · 할일 · 더보기) + 더보기 줄 .moretabs · 누른 차례를 돌려줌"""
    pg = S.page
    hops = []
    for _ in range(3):
        cur = pg.evaluate("() => ui.view")
        if cur == view:
            break
        if not S.touch:
            hops.append(press(S, ('#side .i', LBL[view])) + ':side')
        elif view in ('day', 'todo'):
            hops.append(press(S, ('#pnav div', LBL[view])) + ':pnav')
        elif cur in MORE:
            hops.append(press(S, ('#main .moretabs span', LBL[view])) + ':moretabs')
        else:
            hops.append(press(S, ('#pnav div', '더보기')) + ':pnav')
        QC.until(pg, "(c) => ui.view !== c && _inUi === false", 5000, '화면 옮김', arg=cur)
    ok = QC.until(pg, "(v) => ui.view === v && _inUi === false", 5000, '화면 ' + view, arg=view)
    return hops, ok


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
    else:   # fill — 날짜·시각·숫자 칸
        loc(S, sel).fill(text)
    return m


def quiet(S):
    """걸어 둔 동기화(scheduleSync 4 초)를 걷고 도는 동기화가 끝나길 기다림 — 손 사이에 끼어드는 재그림을 줄임"""
    S.page.evaluate("() => { try { clearTimeout(syncT) } catch (e) {} return 1 }")
    return QC.until(S.page, "() => !syncing && _inUi === false", 20000, '동기화 빔')


def sync(S, share=True):
    """원격 변경 하나 → syncAll(true) → 재그림 표지 · 원격 항목 들어옴까지 기다림"""
    S.n += 1
    n = S.n
    pg = S.page
    quiet(S)
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


def day(S, date):
    """일간 화면을 그 날짜로(사용자 조작 밖 · 앞 칸 초고 · 화면 기억 비움) — 주간·월간 절 날짜는 오늘로"""
    goto(S, 'day', {'date': date, 'wkDate': None, 'moMonth': None}, wait_sel='#mA')
    return QC.until(S.page, "(d) => curDate() === d", 5000, '날짜 ' + str(date), arg=date or D0)


def put_m(S, a=TYPED[0], b=TYPED[1]):
    m = [put(S, '#mA', a, 'fill'), put(S, '#mB', b, 'fill')]
    return m, [val(S, '#mA'), val(S, '#mB')]


def mstate(S):
    return S.page.evaluate(MSTATE_JS)


def mvals(S):
    return [val(S, '#mA'), val(S, '#mB')]


def at_day(S, d, what='날짜 바뀜 · 일간'):
    return QC.until(S.page, "(d) => curDate() === d && ui.view === 'day' && _inUi === false && !!document.getElementById('mA')", 8000, what, arg=d)


def sess_list(S, d, a, b):
    return S.page.evaluate("([d, a, b]) => sessionsOf(cfg.person, d).filter(x => x.a === a && x.b === b).map(x => x.id + '|' + x.d + '|' + x.a + '-' + x.b)", [d, a, b])


def pip_open(S):
    return S.page.evaluate(PIP_OPEN_JS, PIP_FN)


def pip_fill(S, a, b):
    fr = S.page.frame_locator('#hkPip')
    fr.locator('#mA').fill(a)
    fr.locator('#mB').fill(b)
    S.page.evaluate("() => { const d = document.getElementById('hkPip').contentWindow.document; if (d.activeElement && d.activeElement.blur) d.activeElement.blur(); return 1 }")
    return S.page.evaluate("""() => { const d = document.getElementById('hkPip').contentWindow.document; const g = id => { const e = d.getElementById(id); return e ? e.value : null }; return [g('mA'), g('mB')] }""")


# ════════════════════ M1 — 날짜 바꾸는 길마다 = mA · mB 빔 ════════════════════
DAYNAV = '#sec_day .secnav button'
RIBBON = '#sec_day .ribbon[onclick^="ribbonModal(\'day\'"]'


def m1(S, cid, title, start, target, hand, after=None):
    day(S, start)
    pm, before = put_m(S)
    S.page.evaluate("() => __hk.mark()")
    how = hand(S)
    okd = at_day(S, target)
    rr = S.page.evaluate("() => __hk.rendered()")
    st = mstate(S)
    ok = before == TYPED and okd and rr and st['mA'] == '' and st['mB'] == '' and not st['draft']
    rec(S, cid, ok, title + ' = mA · mB 빔 · 화면 기억 없음', dict(start=start, target=target, typed=TYPED, put=pm, before=before, how=how,
                                                              date_ok=okd, rerendered=rr, after=st), hut=True, void=not (okd and rr))
    if after:
        after(S)


def h_ribbon(S, pick=None):
    m = press(S, RIBBON)
    QC.until(S.page, "() => !!document.querySelector('.modal #rbD') && _inUi === false", 5000, '이동 창')
    rb = val(S, '.modal #rbD')
    if pick == 'today':
        m2 = press(S, ('.modal button', '오늘'))
    else:
        if pick:
            loc(S, '.modal #rbD').fill(pick)
        m2 = press(S, '.modal #mOk')
    return [m, 'rbD=%s' % rb, 'pick=%s' % pick, m2]


def m1c_hand(S):
    return press(S, (DAYNAV, '오늘'))


def h_input(S):
    l = loc(S, '#sec_day .secnav input[type="date"]')
    l.fill('2026-10-05')   # 누르지 않고 채움(크롬 날짜 고르개 · drafts2 T7g 잼) — 크롬은 fill 이 change 를 냄
    how = ['fill(일간 날짜 칸)']
    if not QC.until(S.page, "(d) => curDate() === d", 1500, '날짜 칸 change(fill)', arg='2026-10-05'):
        # 웹킷(윈도 빌드 · 첫 실행 01:4x 잼)은 fill 뒤 change 가 안 남 — 칸을 떠나야(blur) 글 칸처럼 change(실기기는 고르개가 냄)
        l.blur()
        how.append('blur')
    how.append('type=' + S.page.evaluate("() => { const i = document.createElement('input'); i.type = 'date'; return i.type }"))
    return how


def close_modal(S):
    try:
        press(S, '.modal #mNo')
    except Exception:
        S.page.evaluate("() => { document.querySelectorAll('.modal').forEach(m => m.remove()); return 1 }")
    QC.until(S.page, "() => !document.querySelector('.modal') && _inUi === false", 5000, '창 닫힘')


def m1g(S):
    S.page.evaluate("""() => { if (!sessionsOf(cfg.person, '2026-10-07').some(x => x.id === 'hk7'))
        upsertSession({id: 'hk7', d: '2026-10-07', s: '민법', p: '', i: '', a: 600, b: 660, plan: '', cat: ''}); return 1 }""")
    quiet(S)
    sel = '#sec_week .wcol b[onclick*="editSession(\'hk7\'"]'

    def hand(S):
        m = press(S, sel)
        md = QC.until(S.page, "() => !!document.querySelector('.modal #eA2')", 5000, '세션 편집 창')
        return [m, 'session_modal=%s' % md]
    m1(S, 'M1g', '주간 블록 누름(setDate + 세션 편집 창)', D0, '2026-10-07', hand, after=close_modal)


def m1i(S):
    def hand(S):
        h1, ok1 = nav(S, 'todo')
        m = press(S, ('#main .ttl .nav button', '‹'))
        okd = QC.until(S.page, "(d) => curDate() === d && _inUi === false", 5000, '할일 화면 날짜', arg='2026-10-08')
        h2, ok2 = nav(S, 'day')
        return [h1, ok1, m, okd, h2, ok2]
    m1(S, 'M1i', '할일 화면(폰 아래 「할일」) ‹ → 다시 타임테이블', D0, '2026-10-08', hand)


def m1j(S):
    sn = S.page.evaluate("() => { takeSnap('2026-10-08'); return !!snapOf(cfg.person, '2026-10-08') }")
    quiet(S)
    card = '#main .card[onclick="snapView(\'%s\',\'2026-10-08\')"]' % ME

    def hand(S):
        h1, ok1 = nav(S, 'gal')
        QC.until(S.page, "(s) => !!document.querySelector(s)", 5000, '모음 카드', arg=card)
        m = press(S, card)
        md = QC.until(S.page, "() => !!document.querySelector('.modal') && _inUi === false", 5000, '모음 창')
        m2 = press(S, ('.modal button', '이 날 일간으로'))
        return [h1, ok1, 'snap=%s' % sn, m, md, m2]
    m1(S, 'M1j', '데일리 모음 카드 → 「이 날 일간으로」', D0, '2026-10-08', hand)


def m1k(S):
    has_css = b'.pipwrap .mbar .man{display:none}' in S.app
    rec(S, 'M1ki', None, '참고 — 진짜 작은 창(pip())은 앱 CSS 「.pipwrap .mbar .man{display:none}」 로 이날기록 칸을 숨김 = %s(이 하네스는 iframe 이라 칸이 보임)'
        % ('있음' if has_css else '없음'), dict(css_rule=has_css), info=True)
    day(S, D0)
    pm, before = put_m(S)
    opened = pip_open(S)
    pv0 = pip_fill(S, '08:00', '08:40')
    S.page.evaluate("() => __hk.mark()")
    how = press(S, (DAYNAV, '›'))
    okd = at_day(S, '2026-10-10')
    st = mstate(S)
    ok = opened and before == TYPED and pv0 == ['08:00', '08:40'] and okd and st['mA'] == '' and st['mB'] == '' and st['pA'] == '' and st['pB'] == '' and not st['draft']
    rec(S, 'M1k', ok, '(PC) 작은 창(PiP) 칸 + 본창 칸에 시각 → 본창 › = 둘 다 빔 · 화면 기억(mA · pip:mA …) 없음',
        dict(opened=opened, before=before, pip_before=pv0, how=how, date_ok=okd, after=st), hut=True, void=not (opened and okd))
    S.page.evaluate(PIP_CLOSE_JS)


def m1l(S):
    day(S, D0)
    pm, before = put_m(S)
    opened = pip_open(S)
    pv0 = pip_fill(S, '08:00', '08:40')
    fr = S.page.frame_locator('#hkPip')
    fr.locator('.pipwrap .ribbon').first.click()
    PM = "() => { const d = document.getElementById('hkPip').contentWindow.document; return !!d.querySelector('.modal #rbD') }"
    md = QC.until(S.page, PM, 5000, '작은 창 이동 창')
    fr.locator('.modal #rbD').fill('2026-10-02')
    fr.locator('.modal #mOk').click()
    okd = QC.until(S.page, "(d) => curDate() === d && !document.getElementById('hkPip').contentWindow.document.querySelector('.modal')", 8000, '작은 창에서 날짜 바뀜', arg='2026-10-02')
    st = mstate(S)
    ok = opened and before == TYPED and pv0 == ['08:00', '08:40'] and md and okd and st['mA'] == '' and st['mB'] == '' and st['pA'] == '' and st['pB'] == '' and not st['draft']
    rec(S, 'M1l', ok, '(PC) 작은 창 칸 + 본창 칸에 시각 → 작은 창 리본 → 이동 창 날짜 「이동」 = 둘 다 빔 · 화면 기억 없음',
        dict(opened=opened, before=before, pip_before=pv0, pip_modal=md, date_ok=okd, after=st), hut=True, void=not (opened and md and okd))
    S.page.evaluate(PIP_CLOSE_JS)


# ════════════════════ M2 · M3 · M3b ════════════════════
def m2(S):
    day(S, D0)
    pm, before = put_m(S)
    h1 = press(S, (DAYNAV, '›'))
    ok1 = at_day(S, '2026-10-10')
    s1 = mstate(S)
    h2 = press(S, (DAYNAV, '‹'))
    ok2 = at_day(S, D0)
    s2 = mstate(S)
    ok = before == TYPED and ok1 and ok2 and s1['mA'] == '' and s1['mB'] == '' and s2['mA'] == '' and s2['mB'] == '' and not s2['draft']
    rec(S, 'M2', ok, '시각 넣고 저장 안 누름 → › → 다시 ‹(그 날짜로 돌아옴) = 빔', dict(typed=TYPED, before=before, next=[h1, ok1, s1], back=[h2, ok2, s2]),
        hut=True, void=not (ok1 and ok2))


def m3(S):
    day(S, D0)
    pm, before = put_m(S, '13:00', '14:10')
    m = press(S, '#main button[onclick^="manualSave"]')
    sv = QC.until(S.page, "([d, a, b]) => sessionsOf(cfg.person, d).some(x => x.a === a && x.b === b) && _inUi === false", 8000, '이날기록 저장', arg=[D0, 780, 850])
    quiet(S)
    L0, s0 = sess_list(S, D0, 780, 850), mstate(S)
    h1 = press(S, (DAYNAV, '›'))
    ok1 = at_day(S, '2026-10-10')
    s1, L1 = mstate(S), sess_list(S, '2026-10-10', 780, 850)
    h2 = press(S, (DAYNAV, '‹'))
    ok2 = at_day(S, D0)
    s2, L2 = mstate(S), sess_list(S, D0, 780, 850)
    ok = (before == ['13:00', '14:10'] and sv and len(L0) == 1 and ok1 and L1 == [] and ok2 and L2 == L0
          and all(x['mA'] == '' and x['mB'] == '' for x in (s0, s1, s2)))
    rec(S, 'M3', ok, '「저장」 누른 기록 무변 — 저장 → › → ‹ = 그 날 기록 그대로(같은 id · 시각) · 옮긴 날 기록 0 · 칸 빔',
        dict(before=before, press=m, saved=sv, rec_before=L0, after_save=s0, next=[h1, ok1, s1, L1], back=[h2, ok2, s2, L2]))


def m3b(S):
    day(S, D0)
    pm, before = put_m(S, '13:20', '14:20')
    h1 = press(S, (DAYNAV, '›'))
    okd = at_day(S, '2026-10-10')
    s1 = mstate(S)
    n0 = sess_list(S, '2026-10-10', 800, 860)
    S.page.evaluate("() => { const t = document.getElementById('toast'); if (t) t.textContent = ''; return 1 }")
    m = press(S, '#main button[onclick^="manualSave"]')
    tw = QC.until(S.page, "() => _inUi === false && !!(document.getElementById('toast') || {}).textContent", 5000, '저장 누른 뒤 알림')
    toast = S.page.evaluate("() => (document.getElementById('toast') || {}).textContent || ''")
    quiet(S)
    n1 = sess_list(S, '2026-10-10', 800, 860)
    ok = before == ['13:20', '14:20'] and okd and n0 == [] and n1 == []
    rec(S, 'M3b', ok, '넣다 만 시각 → › → 그대로 「저장」 = 옮긴 날 기록 0(칸이 비어 「시작·끝을 채워줘」)',
        dict(before=before, next=[h1, okd], after_next=s1, rec_before=n0, press=m, toast_wait=tw, toast=toast, rec_after=n1), hut=True, void=not (okd and tw))


# ════════════════════ M4 · M5 · M6i ════════════════════
def m4(S):
    goto(S, 'share', {'shareTab': 'txt', 'date': D0, 'wkDate': None, 'moMonth': None}, wait_sel='#shT')
    T = 'M4 share 글 %s' % S.dev[:2]
    put(S, '#shT', T)
    h1, ok1 = nav(S, 'day')
    QC.until(S.page, "() => !!document.getElementById('cmT') && !!document.getElementById('mA')", 5000, '일간 칸')
    C = 'M4 공통 글 %s' % S.dev[:2]
    put(S, '#cmT', C)
    pm, before = put_m(S)
    o0 = S.page.evaluate(DRAFT_OTHERS_JS)
    h2 = press(S, (DAYNAV, '›'))
    okd = at_day(S, '2026-10-10')
    cm, o1, st = val(S, '#cmT'), S.page.evaluate(DRAFT_OTHERS_JS), mstate(S)
    h3, ok3 = nav(S, 'share')
    QC.until(S.page, "() => !!document.getElementById('shT')", 5000, 'shT 다시')
    sh = val(S, '#shT')
    ok = ok1 and okd and ok3 and cm == C and sh == T and o1.get('shT') == T and o1.get('cmT') == C
    rec(S, 'M4', ok, '다른 칸 기억 그대로 — share Text(shT) · 공통 할일(cmT) 쓰던 글 → 날짜 바꿈(›) = 칸 · 화면 기억 값 그대로',
        dict(shT=T, cmT=C, to_day=[h1, ok1], draft_others_before=o0, next=[h2, okd], cmT_after=cm, draft_others_after=o1, m_after=st,
             to_share=[h3, ok3], shT_after=sh))


def m5(S):
    day(S, D0)
    pm, before = put_m(S)
    # a 화면 오감
    try:
        h1, ok1 = nav(S, 'share')
        h2, ok2 = nav(S, 'day')
        QC.until(S.page, "() => !!document.getElementById('mA')", 5000, 'mA 다시')
        a, da = mvals(S), S.page.evaluate("() => curDate()")
        rec(S, 'M5a', before == TYPED and ok1 and ok2 and a == TYPED and da == D0, '날짜 안 바꾸고 Share 화면 → 다시 타임테이블 = mA · mB 그대로',
            dict(before=before, nav=[h1, ok1, h2, ok2], after=a, date=da))
    except Exception as e:
        ex(S, 'M5a', e)
    # b syncAll
    try:
        st = sync(S, share=False)
        b = mvals(S)
        rec(S, 'M5b', sync_ok(st) and b == TYPED, '날짜 안 바꾸고 원격 변경 syncAll(재그림) = 그대로', dict(sync=st, after=b))
    except Exception as e:
        ex(S, 'M5b', e)
    # c 같은 날 「오늘」(판단 — 같은 날로 「바꿈」은 지우지 않음)
    try:
        S.page.evaluate("() => __hk.mark()")
        m = press(S, (DAYNAV, '오늘'))
        rr = QC.until(S.page, "() => __hk.rendered() && _inUi === false && !!document.getElementById('mA')", 5000, '「오늘」 render')
        c, dc = mvals(S), S.page.evaluate("() => curDate()")
        rec(S, 'M5c', rr and c == TYPED and dc == D0, '오늘을 보는 중에 「오늘」(같은 날로 setDate · render) = 그대로', dict(press=m, rerendered=rr, after=c, date=dc))
    except Exception as e:
        ex(S, 'M5c', e)
    # d 리본 이동 창 같은 날 「이동」
    try:
        S.page.evaluate("() => __hk.mark()")
        hs = h_ribbon(S, None)
        rr = QC.until(S.page, "() => __hk.rendered() && !document.querySelector('.modal') && _inUi === false && !!document.getElementById('mA')", 5000, '같은 날 이동 render')
        d, dd = mvals(S), S.page.evaluate("() => curDate()")
        rec(S, 'M5d', rr and d == TYPED and dd == D0 and ('rbD=' + D0) in hs, '리본 → 이동 창 날짜 그대로 「이동」(같은 날 setDate) = 그대로', dict(hand=hs, rerendered=rr, after=d, date=dd))
    except Exception as e:
        ex(S, 'M5d', e)
    # e 주간 절 ‹(주간 날짜만 · 일간 날짜 무변)
    try:
        wk0 = S.page.evaluate("() => ttWkD()")
        m = press(S, ('#sec_week .secnav button', '‹'))
        okw = QC.until(S.page, "(w) => ttWkD() !== w && _inUi === false && !!document.getElementById('mA')", 5000, '주간 ‹', arg=wk0)
        e_, wk1, de = mvals(S), S.page.evaluate("() => ttWkD()"), S.page.evaluate("() => curDate()")
        rec(S, 'M5e', okw and e_ == TYPED and de == D0, '주간 절 ‹(주간 날짜만 바뀜 · 일간 날짜 그대로) = 그대로', dict(press=m, week=[wk0, wk1], after=e_, date=de))
    except Exception as e:
        ex(S, 'M5e', e)


def m6i(S):
    goto(S, 'day', {'date': None, 'wkDate': None, 'moMonth': None}, wait_sel='#mA')
    pm, before = put_m(S)
    d0 = S.page.evaluate("() => curDate()")
    clk = S.page.evaluate("() => __hkShift(24 * 3600 * 1000)")
    S.page.evaluate("() => { render(); return 1 }")   # 타이머 · 동기화 자리의 재그림(사용자 조작 밖)
    st = mstate(S)
    S.page.evaluate("() => __hkShift(-24 * 3600 * 1000)")
    S.page.evaluate("() => { render(); return 1 }")
    # 옛 줄: rec(S, 'M6i', None, '참고 — 날짜 칸이 빈(ui.date null · 설치 뒤 날짜를 한 번도 안 옮긴 기기) 채 하루 경계를 넘김 = setDate 를 안 지나 mA · mB 남음(이 판 범위 밖)',
    rec(S, 'M6i', None, '참고 — 날짜 칸이 빈(ui.date null · 설치 뒤 날짜를 한 번도 안 옮긴 기기) 채 하루 경계를 넘김(+24 시간 → render) = 724c4ac 판은 setDate 를 안 지나 mA · mB 남음 · 덧판은 빔(관문 = M9)',
        dict(before=before, date_before=d0, clock=clk, after=st), info=True)


# ════════════════════ 덧판(10/10 02:03 · 02:58 [채팅] · tt_mdate2) — 할일 세 칸 아홉 · 하루 경계 ════════════════════
NINE = ['addS_0', 'addS_1', 'addS_2', 'addT_0', 'addT_1', 'addT_2', 'due_0', 'due_1', 'due_2']
ELEVEN = ['mA', 'mB'] + NINE
NINE_VAL = {'addS_0': '어제 학습 쓰던 글', 'addS_1': '오늘 학습 쓰던 글', 'addS_2': '내일 학습 쓰던 글',
            'addT_0': '어제 할일 쓰던 글', 'addT_1': '오늘 할일 쓰던 글', 'addT_2': '내일 할일 쓰던 글',
            'due_0': '2026-10-20', 'due_1': '2026-10-21', 'due_2': '2026-10-22'}
EXP11 = dict(NINE_VAL, mA=TYPED[0], mB=TYPED[1])
COLN = {'0': '어제', '1': '오늘', '2': '내일'}
KIND = {'addS': '「+ 학습 추가」', 'addT': '「+ 할일 추가」', 'due': '기한'}
TODONAV = '#main .ttl .nav button'   # 할일 화면 ‹ 오늘 ›(navBtns)
D1 = '2026-10-10'
PC_WIDE = {'width': 1600, 'height': 900}   # 덧판 PC 칸 창(1100 폭 일간 addT 폭 0 — 위 머리글)
OTHERS_SEED = {'lsNT': '계획 목록 쓰던 글(지은 기억)', 'snMemo': '메모 쓰던 글(지은 기억)'}
# 칸 상태 — 본창 값(없으면 null) · 작은 창 mA·mB · 화면 기억 열쇠(본창 · 'pip:') · 가운데 「오늘」 칸 머리 날짜 · 가짜 시계
FST_JS = r"""(ids) => { const g = (D, id) => { const e = D && D.getElementById(id); return e ? e.value : null };
 let pd = null; try { pd = (pipWin && !pipWin.closed) ? pipWin.document : null } catch (e) {}
 const v = {}; ids.forEach(id => { v[id] = g(document, id) });
 const c = document.querySelector('#main .three .col.today');
 return {date: curDate(), today: today(), uiDate: ui.date || null, view: ui.view, val: v, pA: pd ? g(pd, 'mA') : null, pB: pd ? g(pd, 'mB') : null,
   draft: ids.concat(ids.map(i => 'pip:' + i)).filter(k => _draft.has(k)).map(k => k + '=' + (_draft.get(k) || {}).v),
   col: c ? c.getAttribute('data-caldate') : null, clock: new Date().toISOString()} }"""
# 가짜 시계를 t 로 옮기고 같은 evaluate 안에서 바로 trig(render · vis = visibilitychange · sync = syncAll(true) · none) → 칸 상태 — 사이에 타이머 · 동기화가 못 낌
ROLL_JS = (r"""([t, trig, ids]) => { const d = new Date(t).getTime() - Date.now(); __hkShift(d);
 if (trig === 'render') render(); else if (trig === 'vis') document.dispatchEvent(new Event('visibilitychange')); else if (trig === 'sync') syncAll(true);
 const st = (""" + FST_JS + r""")(ids); st.shift = d; st.trig = trig; return st }""")


def fst(S, ids):
    return S.page.evaluate(FST_JS, ids)


def roll(S, t, trig, ids):
    return S.page.evaluate(ROLL_JS, [t, trig, ids])


def clock_mark(S):
    """시계 옮기기 전 표 — (가짜 시계 ms, 실제 초) · 되돌릴 때 그 사이 흐른 실제 시간만큼 더한 자리로(옮기다 예외가 나도 원래 흐름으로)"""
    return (S.page.evaluate("() => Date.now()"), time.time())


def unroll(S, mark):
    """가짜 시계 되돌림(표 뒤 흐른 만큼만 더한 원래 흐름) → render(사용자 조작 밖 · 덧판은 여기서 지난 today() 를 다시 맞춤 = mA·mB·아홉 한 번 더 비움) · finally 에서 부름(예외 삼킴)"""
    try:
        quiet(S)
        want = mark[0] + int((time.time() - mark[1]) * 1000)
        return S.page.evaluate("(w) => { __hkShift(w - Date.now()); render(); return [today(), curDate(), new Date().toISOString()] }", want)
    except Exception as e:
        return 'unroll 예외: %s' % str(e)[:120]


def t_start(S):
    """하루 시작(dayStart) 넘긴 시각 · 달력 자정 넘긴 시각(today() 무변)"""
    ds = S.page.evaluate("() => dayStart()")
    return ds, D1 + 'T%02d:01:00+09:00' % ds, D1 + 'T00:01:00+09:00'


def wide(S):
    """덧판 PC 칸 — 창을 1600×900 으로(1100 폭 일간은 addT 폭 0 · 폰은 그대로) · 돌려줌 = 창 폭"""
    if not S.touch and S.page.viewport_size != PC_WIDE:
        S.page.set_viewport_size(PC_WIDE)
        QC.until(S.page, "(w) => innerWidth === w", 3000, '창 ' + str(PC_WIDE['width']), arg=PC_WIDE['width'])
    return S.page.evaluate("() => innerWidth")


def lbl(fid):
    k, n = fid.split('_')
    return '%s 칸 %s' % (COLN[n], KIND[k])


def put9(S, ids):
    """아홉 칸 중 ids 에 넣음(Enter 안 누름) — 글 칸 = 눌러 포커스 → insert_text(keydown 없음 = 안 더해짐) ·
       기한(날짜) 칸 = 누르지 않고 fill(크롬 날짜 고르개 잼 · 윈도 웹킷은 type=text)"""
    hows = []
    for i in ids:
        if i.startswith('due_'):
            l = loc(S, '#' + i)
            l.scroll_into_view_if_needed(timeout=8000)
            l.fill(NINE_VAL[i])
            hows.append(i + ':fill')
        else:
            hows.append(i + ':' + put(S, '#' + i, NINE_VAL[i]))
    return hows


def kept(st, ids):
    """남았나 — 화면에 있는 칸은 값 · 화면에 없는 칸(폰 할일 화면의 mA · mB)은 화면 기억 값 · 돌려줌 = 어긋난 칸"""
    dr = dict(x.split('=', 1) for x in st['draft'] if not x.startswith('pip:'))
    return [i for i in ids if (dr.get(i) if st['val'].get(i) is None else st['val'].get(i)) != EXP11[i]]


def emptied(st, ids):
    """비었나 — 화면에 있는 칸 값 '' · 화면 기억(본창 · 작은 창)에 하나도 없음 · 돌려줌 = 어긋난 것"""
    return [i for i in ids if st['val'].get(i) not in ('', None)] + ['기억:' + x for x in st['draft']]


# ── M7 — 아홉 칸 각각: 넣고 › = 빔 · ‹ = 빔 ──
def m7(S):
    wide(S)
    for k, fid in zip('abcdefghi', NINE):
        try:
            m7_one(S, 'M7' + k, fid)
        except Exception as e:
            ex(S, 'M7' + k, e)


def m7_one(S, cid, fid):
    view, nv = ('todo', TODONAV) if S.touch else ('day', DAYNAV)
    goto(S, view, {'date': D0, 'wkDate': None, 'moMonth': None}, wait_sel='#' + fid)
    QC.until(S.page, "(d) => curDate() === d", 5000, '날짜 ' + D0, arg=D0)
    how = put9(S, [fid])
    v0 = val(S, '#' + fid)
    W = "([d, f]) => curDate() === d && _inUi === false && !!document.getElementById(f)"
    h1 = press(S, (nv, '›'))
    ok1 = QC.until(S.page, W, 8000, '› 뒤 ' + fid, arg=[D1, fid])
    s1 = fst(S, [fid])
    h2 = press(S, (nv, '‹'))
    ok2 = QC.until(S.page, W, 8000, '‹ 뒤 ' + fid, arg=[D0, fid])
    s2 = fst(S, [fid])
    b = ['›:' + x for x in emptied(s1, [fid])] + ['‹:' + x for x in emptied(s2, [fid])]
    ok = v0 == NINE_VAL[fid] and ok1 and ok2 and not b
    rec(S, cid, ok, '%s(%s)에 %s 넣고 Enter 안 누름 → %s › = 빔 · 다시 ‹(그 날) = 빔 · 화면 기억 없음'
        % (fid, lbl(fid), '날짜' if fid.startswith('due_') else '글', '할일 화면' if S.touch else '일간'),
        dict(bad=b, view=view, put=how, before=v0, next=[h1, ok1, s1], back=[h2, ok2, s2]), hut=True, void=not (ok1 and ok2), since=2)


# ── M8 — 날짜 안 바꾸면 아홉 칸 그대로 ──
def m8(S):
    wide(S)
    view = 'todo' if S.touch else 'day'
    goto(S, view, {'date': None, 'wkDate': None, 'moMonth': None}, wait_sel='#addS_1')
    QC.until(S.page, "(d) => curDate() === d && !ui.date", 5000, '오늘 따라감', arg=D0)
    how = put9(S, NINE)
    v0 = fst(S, NINE)
    pre = v0['val'] == NINE_VAL
    try:
        h1, ok1 = nav(S, 'share')
        h2, ok2 = nav(S, view)
        QC.until(S.page, "() => !!document.getElementById('addS_1')", 5000, '아홉 칸 다시')
        sa = fst(S, NINE)
        b = kept(sa, NINE)
        rec(S, 'M8a', pre and ok1 and ok2 and not b and sa['date'] == D0, '아홉 칸 쓰던 글 → 날짜 안 바꾸고 Share 화면 → 다시 %s = 그대로' % LBL[view],
            dict(bad=b, put=how, before=v0['val'], nav=[h1, ok1, h2, ok2], after=sa))
    except Exception as e:
        ex(S, 'M8a', e)
    try:
        st = sync(S, share=False)
        sb = fst(S, NINE)
        b = kept(sb, NINE)
        rec(S, 'M8b', pre and sync_ok(st) and not b and sb['date'] == D0, '아홉 칸 쓰던 글 → 날짜 안 바꾸고 원격 변경 syncAll(재그림) = 그대로',
            dict(bad=b, sync=st, after=sb))
    except Exception as e:
        ex(S, 'M8b', e)


# ── M9 — 하루 경계(오늘 따라가는 화면) ──
def m9_fill(S, date=None):
    """열하나 넣기 — PC = 일간(열하나 다 화면) · 폰 = 일간 mA·mB → 아래 「할일」 화면(아홉 · mA·mB 는 화면 기억) · date None = 오늘 따라감"""
    goto(S, 'day', {'date': date, 'wkDate': None, 'moMonth': None}, wait_sel='#mA')
    QC.until(S.page, "([d, u]) => curDate() === d && (ui.date || null) === u", 5000, '날짜 ' + str(date), arg=[date or D0, date])
    pm, before = put_m(S)
    hops = None
    if S.touch:
        hops = nav(S, 'todo')
        QC.until(S.page, "() => !!document.getElementById('addS_1')", 5000, '할일 화면 칸')
    how = put9(S, NINE)
    quiet(S)
    st0 = fst(S, ELEVEN)
    pre = before == TYPED and not kept(st0, ELEVEN) and st0['date'] == (date or D0) and st0['uiDate'] == date
    return pre, dict(put_m=pm, before=before, nav=hops, put9=how, pre=st0)


def phone_day(S):
    """폰 — 할일 화면에서 일간으로 가 mA · mB(화면 기억이 다시 그려지나) · PC = None"""
    if not S.touch:
        return None
    h, ok = nav(S, 'day')
    QC.until(S.page, "() => !!document.getElementById('mA')", 5000, 'mA 다시')
    return dict(nav=[h, ok], st=fst(S, ['mA', 'mB']))


def m9(S):
    wide(S)
    ds, t_roll, t_mid = t_start(S)
    where = '할일 화면 아홉 + 일간 mA·mB(화면 기억)' if S.touch else '일간 열하나'
    # a · b — 달력 자정(today() 무변) → render = 그대로 · 이어서 하루 시작 → render = 빔
    mk = None
    try:
        pre, info = m9_fill(S)
        mk = clock_mark(S)
        sa = roll(S, t_mid, 'render', ELEVEN)
        ba = kept(sa, ELEVEN)
        rec(S, 'M9a', pre and sa['today'] == D0 and sa['date'] == D0 and not ba,
            '오늘 따라가는 화면(%s) 쓰던 글 → 달력 자정 넘김(10-10 00:01 · 하루 시작 %d 시 전이라 today() 무변) → render = 그대로' % (where, ds),
            dict(bad=ba, after=sa, fill=info))
        sb = roll(S, t_roll, 'render', ELEVEN)
        bb = emptied(sb, ELEVEN)
        pdy = phone_day(S)
        if pdy:
            bb += ['일간 ' + x for x in emptied(pdy['st'], ['mA', 'mB'])]
        okd = sb['today'] == D1 and sb['date'] == D1
        rec(S, 'M9b', pre and okd and not bb, '이어서 하루 시작 넘김(10-10 %02d:01 · today() 바뀜) → render(사용자 조작 밖) = 열하나 빔 · 화면 기억 없음' % ds,
            dict(bad=bb, after=sb, phone_day=pdy), hut=True, void=not (pre and okd), since=2)
    except Exception as e:
        ex(S, 'M9b', e)
    finally:
        if mk:
            unroll(S, mk)
    # c · d — visibilitychange · syncAll(시계 옮김과 같은 evaluate 안 · 동기화 끝난 뒤도 잼)
    for cid, trig, nm in (('M9c', 'vis', 'visibilitychange(앱을 다시 봄 → syncAll)'), ('M9d', 'sync', 'syncAll(true)')):
        mk = None
        try:
            pre, info = m9_fill(S)
            mk = clock_mark(S)
            s = roll(S, t_roll, trig, ELEVEN)
            b = emptied(s, ELEVEN)
            quiet(S)
            s2 = fst(S, ELEVEN)
            b2 = emptied(s2, ELEVEN)
            if cid == 'M9c':
                rec(S, 'M9i', None, '참고 — 하루 시작 넘김 → visibilitychange · 원격 변경 없음 = 본창을 다시 안 그림(가운데 「오늘」 칸 머리 날짜 = 옛 날 · 앱 기존 동작 · 이 판 범위 밖)',
                    dict(date=s['date'], col_now=s['col'], col_after_sync=s2['col'], view=s['view']), info=True)
            pdy = phone_day(S)
            if pdy:
                b2 += ['일간 ' + x for x in emptied(pdy['st'], ['mA', 'mB'])]
            okd = s['today'] == D1 and s['date'] == D1
            rec(S, cid, pre and okd and not b and not b2,
                '오늘 따라가는 화면(%s) 쓰던 글 → 하루 시작 넘김(10-10 %02d:01) → %s = 열하나 빔 · 화면 기억 없음(동기화 끝난 뒤도)' % (where, ds, nm),
                dict(bad=b, bad_after_sync=b2, after=s, after_sync=s2, phone_day=pdy, fill=info), hut=True, void=not (pre and okd), since=2)
        except Exception as e:
            ex(S, cid, e)
        finally:
            if mk:
                unroll(S, mk)
    if not S.touch:
        m9e(S, t_roll)


def m9e(S, t_roll):
    mk = None
    try:
        goto(S, 'day', {'date': None, 'wkDate': None, 'moMonth': None}, wait_sel='#mA')
        QC.until(S.page, "(d) => curDate() === d && !ui.date", 5000, '오늘 따라감', arg=D0)
        pm, before = put_m(S)
        opened = pip_open(S)
        pv0 = pip_fill(S, '08:00', '08:40')
        quiet(S)
        mk = clock_mark(S)
        s = roll(S, t_roll, 'render', ['mA', 'mB'])
        b = emptied(s, ['mA', 'mB']) + [k + '=' + str(s[k]) for k in ('pA', 'pB') if s[k] != '']
        okd = s['today'] == D1 and s['date'] == D1
        ok = opened and before == TYPED and pv0 == ['08:00', '08:40'] and okd and not b
        rec(S, 'M9e', ok, '(PC) 작은 창(PiP) 칸 + 본창 칸에 시각 → 하루 시작 넘김 → render = 둘 다 빔 · 화면 기억(mA · pip:mA …) 없음',
            dict(bad=b, opened=opened, before=before, pip_before=pv0, after=s), hut=True, void=not (opened and okd), since=2)
    except Exception as e:
        ex(S, 'M9e', e)
    finally:
        if mk:
            unroll(S, mk)
        S.page.evaluate(PIP_CLOSE_JS)


# ── M10 — 날짜 박힌 화면은 하루가 넘어가도 그대로(판단) ──
def m10(S):
    wide(S)
    ds, t_roll, _ = t_start(S)
    mk = None
    try:
        pre, info = m9_fill(S, D0)
        mk = clock_mark(S)
        s1 = roll(S, t_roll, 'render', ELEVEN)
        s2 = roll(S, t_roll, 'sync', ELEVEN)
        quiet(S)
        s3 = fst(S, ELEVEN)
        b = ['render:' + x for x in kept(s1, ELEVEN)] + ['sync:' + x for x in kept(s2, ELEVEN)] + ['뒤:' + x for x in kept(s3, ELEVEN)]
        pdy = None
        if S.touch:
            h, ok = nav(S, 'day')
            QC.until(S.page, "() => !!document.getElementById('mA')", 5000, 'mA 다시')
            pdy = dict(nav=[h, ok], st=fst(S, ['mA', 'mB']))
            b += ['일간 ' + x for x in kept(pdy['st'], ['mA', 'mB'])]
        okd = s1['today'] == D1 and s1['date'] == D0 and s3['date'] == D0
        rec(S, 'M10', pre and okd and not b,
            '날짜 박힌 화면(ui.date = 10-09 · %s) 쓰던 글 → 하루 시작 넘김(10-10 %02d:01 · today() 바뀜 · 보는 날짜 그대로) → render · syncAll = 열하나 그대로(판단)'
            % ('할일 화면 아홉 + 일간 mA·mB' if S.touch else '일간 열하나', ds),
            dict(bad=b, render=s1, sync=s2, after_sync=s3, phone_day=pdy, fill=info))
    except Exception as e:
        ex(S, 'M10', e)
    finally:
        if mk:
            unroll(S, mk)


# ── M11 — 다른 칸 기억 그대로(하루 경계 · 날짜 바꿈) ──
def m11(S):
    wide(S)
    ds, t_roll, _ = t_start(S)
    goto(S, 'share', {'shareTab': 'txt', 'date': None, 'wkDate': None, 'moMonth': None}, wait_sel='#shT')
    T = 'M11 share 글 %s' % S.dev[:2]
    put(S, '#shT', T)
    h1, ok1 = nav(S, 'day')
    QC.until(S.page, "() => !!document.getElementById('cmT') && !!document.getElementById('mA')", 5000, '일간 칸')
    C = 'M11 공통 글 %s' % S.dev[:2]
    put(S, '#cmT', C)
    seed = S.page.evaluate("(o) => { Object.keys(o).forEach(k => _draft.set(k, {v: o[k], dv: ''})); return Object.keys(o).filter(k => _draft.has(k)) }", OTHERS_SEED)
    pm, before = put_m(S)
    quiet(S)
    want = dict(OTHERS_SEED, shT=T, cmT=C)
    o0 = S.page.evaluate(DRAFT_OTHERS_JS)
    mk = None
    try:   # a 하루 시작 넘김(오늘 따라감) → render
        mk = clock_mark(S)
        sa = roll(S, t_roll, 'render', ['mA', 'mB', 'cmT'])
        oa = S.page.evaluate(DRAFT_OTHERS_JS)
        b = [k for k, v in want.items() if oa.get(k) != v] + ([] if sa['val'].get('cmT') == C else ['cmT 칸'])
        okd = sa['today'] == D1 and sa['date'] == D1
        rec(S, 'M11a', ok1 and before == TYPED and okd and not b,
            '다른 칸 기억 그대로 — share 글(shT) · 공통 할일(cmT) · 지은 기억(계획 목록 lsNT · 메모 snMemo) → 하루 시작 넘김(오늘 따라감 · render) = 값 그대로',
            dict(bad=b, to_day=[h1, ok1], seed=seed, before=o0, after=oa, m_after=sa))
    except Exception as e:
        ex(S, 'M11a', e)
    finally:
        if mk:
            unroll(S, mk)
    try:   # b 날짜 바꿈(일간 ›)
        QC.until(S.page, "(d) => curDate() === d && _inUi === false && !!document.getElementById('cmT')", 5000, '되돌림 뒤 일간', arg=D0)
        ob0 = S.page.evaluate(DRAFT_OTHERS_JS)
        h2 = press(S, (DAYNAV, '›'))
        okd = at_day(S, D1)
        ob, cmb = S.page.evaluate(DRAFT_OTHERS_JS), val(S, '#cmT')
        h3, ok3 = nav(S, 'share')
        QC.until(S.page, "() => !!document.getElementById('shT')", 5000, 'shT 다시')
        shv = val(S, '#shT')
        b = [k for k, v in want.items() if ob.get(k) != v] + ([] if cmb == C else ['cmT 칸']) + ([] if shv == T else ['shT 칸'])
        rec(S, 'M11b', okd and ok3 and not b, '다른 칸 기억 그대로 — 같은 넷(지은 기억 포함) → 날짜 바꿈(일간 ›) = 칸 · 화면 기억 값 그대로',
            dict(bad=b, before=ob0, next=[h2, okd], after=ob, cmT_after=cmb, to_share=[h3, ok3], shT_after=shv))
    except Exception as e:
        ex(S, 'M11b', e)


def tx(S):
    e = S.errs()
    rec(S, 'TX', not e, '이 문맥 처음부터 끝까지 스크립트 오류 0(window error · unhandledrejection · pageerror · console.error)',
        dict(n=len(e), errs=e[:6], blocked=sorted(set(S.gh.blocked))[:5]))


RUN = {
    'M1a': lambda S: m1(S, 'M1a', '일간 ›', D0, '2026-10-10', lambda S: press(S, (DAYNAV, '›'))),
    'M1b': lambda S: m1(S, 'M1b', '일간 ‹', D0, '2026-10-08', lambda S: press(S, (DAYNAV, '‹'))),
    'M1c': lambda S: m1(S, 'M1c', '일간 「오늘」(지난 날 10-06 에서)', '2026-10-06', D0, m1c_hand),
    'M1d': lambda S: m1(S, 'M1d', '일간 날짜 칸 고름(10-05)', D0, '2026-10-05', h_input),
    'M1e': lambda S: m1(S, 'M1e', '리본 → 이동 창 날짜(10-03) 「이동」', D0, '2026-10-03', lambda S: h_ribbon(S, '2026-10-03')),
    'M1f': lambda S: m1(S, 'M1f', '리본 → 이동 창 「오늘」(10-03 에서)', '2026-10-03', D0, lambda S: h_ribbon(S, 'today')),
    'M1g': m1g,
    'M1h': lambda S: m1(S, 'M1h', '월간 칸 누름(ttGoDate 10-14)', D0, '2026-10-14', lambda S: press(S, '#sec_month .d[onclick="ttGoDate(\'2026-10-14\')"]')),
    'M1i': m1i, 'M1j': m1j, 'M1k': m1k, 'M1l': m1l,
    'M2': m2, 'M3': m3, 'M3b': m3b, 'M4': m4, 'M5': m5, 'M6i': m6i, 'TX': tx,
    'M7': m7, 'M8': m8, 'M9': m9, 'M10': m10, 'M11': m11,   # 덧판(10/10 tt_mdate2)
}


def run_dev(browser, dev, app, base, plan):
    S = Sess(browser, dev, app, base)
    try:
        if not S.booted:
            rec(S, 'TB', False, '부팅 — render · syncAll · setDate · keepInputGrab · #main', dict(errs=S.errs()[:5]))
            return
        for k in plan:
            if ONLY and not any(k == o or k.startswith(o) or o.startswith(k) for o in ONLY):
                continue
            with QC.stage('%s %s %s' % (dev, 'base' if base else 'new', k)):
                try:
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
    global BASE_GEN   # 덧판 — 헛잣대 세대
    t0_ = time.time()
    new = open(NEWF, 'rb').read()
    out('INFO | 판 NEW | %s · %d B · md5 %s · CR %d' % (NEWF, len(new), hashlib.md5(new).hexdigest(), new.count(b'\r')))
    base = None
    if QC.GATE:
        base, bsrc = load_base()
        bm = hashlib.md5(base).hexdigest()
        out('INFO | 판 BASE | %s · %d B · md5 %s%s' % (bsrc, len(base), bm, '' if bm == BASE_MD5 else ' · ⚠ 기대 md5 %s 와 다름' % BASE_MD5))
        BASE_GEN = int(ARG('--base-gen', GEN_MD5.get(bm, 1)))
        out('INFO | 바탕 세대 %d(%s) — since 가 이보다 큰 칸만 헛잣대(바탕 FAIL 이어야) · 아니면 바탕도 같음' % (BASE_GEN, '알려진 md5' if bm in GEN_MD5 else '모르는 md5 → --base-gen 또는 1'))
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
        # 옛 줄: for r in [x for x in ROWS if x['side'] == 'new' and x['hut'] is True and not x['info']]:
        for r in [x for x in ROWS if x['side'] == 'new' and eff_hut(x) is True and not x['info']]:
            b = [x for x in ROWS if x['side'] == 'base' and x['cid'] == r['cid'] and x['dev'] == r['dev']]
            if not b:
                continue
            bst = b[0]['st']
            gar = bst == 'FAIL' and b[0]['title'] != '하네스 예외' and not b[0]['void']   # 바탕 FAIL 이 하네스 예외 · 길 안 됨이면 가른 것이 아님(값으로 FAIL 이어야)
            hut_n += 1
            hut_ok += 1 if gar else 0
            out('%s | %s-헛 %s · 헛잣대 — 바탕 %s 에서 %s(%s) | %s' % ('PASS' if gar else 'FAIL', r['cid'], r['dev'], BASE, bst,
                                                             '잣대가 가름' if gar else ('하네스 예외 · 길 안 됨 — 안 가름' if bst == 'FAIL' else '잣대가 안 가름'), b[0]['title'][:60]))
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
        # 옛 줄: hut = n[0]['hut'] if n else (b[0]['hut'] if b else False)
        hut = eff_hut(n[0]) if n else (eff_hut(b[0]) if b else False)   # 덧판 — 헛잣대 세대
        info = any(x['info'] for x in n + b)
        ns = n[0]['st'] if n else '—'
        bs = b[0]['st'] if b else '—'
        if info:
            exp, j = '(INFO)', '—'
        elif not b:
            exp, j = ('FAIL' if hut is True else 'PASS' if hut is False else '(참고)'), '—'
        elif hut is True:
            exp, j = 'FAIL', ('✗ 바탕 하네스 예외' if bs == 'FAIL' and b[0]['title'] == '하네스 예외' else '✗ 바탕 길 안 됨' if bs == 'FAIL' and b[0]['void']
                              else 'OK(가름)' if bs == 'FAIL' else '✗ 안 가름')
        elif hut is None:
            exp, j = '(참고)', '바탕 ' + bs
        else:
            exp, j = 'PASS', (('바탕도 같음' if ns == 'PASS' else '✗ 새 판만 FAIL') if bs == 'PASS' else '✗ 바탕 FAIL(뜻밖)')
        lines.append('%s | %s | %s | %s | %s | %s' % (cid, dev, ns, bs, exp, j))
    return lines


def write_res(table, p, f, sec, head):
    hd = ['# _harness_tt_mdate 결과 — %s · mode %s · %.1f 초' % (time.strftime('%Y-%m-%d %H:%M:%S'), QC.MODE, sec),
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
