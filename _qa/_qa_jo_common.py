# -*- coding: utf-8 -*-
r"""jo 하네스 공용 — _task_qa_slim(2026-10-04) A-1 실행 모드 · A-2 기다리기 · A-3 표본 · §B-4 띄움 셈.

쓰는 법 — 하네스 머리 5줄(_roots 찾기) 바로 뒤, 다른 하네스 import 와 인자 읽기보다 먼저:
    import _qa_jo_common as QJ

모드(인자 --mode · 없으면 gate = 이 판 앞과 같음):
    QJ.MODE     'gate' | 'regress' | 'smoke'
    QJ.GATE     gate 이면 True — 헛잣대 · 그 판에만 뜻 있는 칸(처리안 「관문만」)은 `if QJ.GATE:` 안에 둔다
    QJ.REGRESS  regress 또는 smoke 이면 True — 바탕(BASE) 판을 띄우지 않는다 · 하위 하네스 · 굽기 · git fetch 를 부르지 않는다
    QJ.SMOKE    smoke 이면 True — regress 가운데 smoke 칸만(QJ.want(id, smoke=True))
    이 모듈은 import 때 sys.argv 에서 --mode · --snap-in · --snap-out 을 떼어 낸다 — 하네스의 인자 읽기는 이 판 앞과 같다.

기준 칸(처리안 「기준」 = 바탕 값을 기댓값으로 쓰는 칸):
    bv = QJ.base(cid, v)   regress: 저장된 바탕 스냅샷 값(--snap-in · 없으면 v 자신 = 첫 기록)
    ok = QJ.same(cid, v)   QJ.norm(v) == QJ.base(cid, v)
    cid 는 한 실행 안에서 겹치지 않게(엔진 · 폭을 붙임: 'b4@chromium/1440')
    잰 값은 늘 --snap-out 에 적힌다 → 실행기가 저장본 옆 <열쇠>.base.json 으로 둔다(다음 판의 기댓값).

표본(A-3): QJ.WIDTHS · QJ.widths(app_html) · QJ.sample(seq, n, seed).
기다리기(A-2): QJ.until(page, js, timeout_ms, what) · QJ.sleep(ms, why) — 남는 고정 대기는 까닭을 남긴다.
셈(§B-4): 하네스가 자리마다 QJ.launch('new'|'base') · QJ.sub('git:show-app'|'python:harness'|'python:bake'|'git:fetch'|…) 를 부른다
         → --snap-out 옆 launch.json(regress · smoke 만).
"""
import atexit
import collections
import hashlib
import json
import os
import random
import re
import sys
import threading
import time


def _pop(flag):
    a = sys.argv
    for i, x in enumerate(a):
        if x == flag:
            v = a[i + 1] if i + 1 < len(a) else ''
            del a[i:i + 2]
            return v
        if x.startswith(flag + '='):
            del a[i]
            return x.split('=', 1)[1]
    return None


MODE = (_pop('--mode') or 'gate').strip().lower()
if MODE not in ('gate', 'regress', 'smoke'):
    raise SystemExit('_qa_jo_common: --mode 는 gate | regress | smoke (받은 값 %r)' % MODE)
GATE = MODE == 'gate'
REGRESS = not GATE
SMOKE = MODE == 'smoke'
SNAP_IN = _pop('--snap-in')
SNAP_OUT = _pop('--snap-out')
T0 = time.time()

_lock = threading.Lock()
_SNAP = {}
if SNAP_IN and os.path.isfile(SNAP_IN):
    try:
        with open(SNAP_IN, encoding='utf-8') as _f:
            _SNAP = (json.load(_f) or {}).get('v') or {}
    except Exception as _e:
        _SNAP = {}
        sys.stderr.write('_qa_jo_common: 스냅샷 못 읽음 %s (%s)\n' % (SNAP_IN, _e))
_OUT = {}
_DUP = set()
_CNT = collections.Counter()
_STAGES = []
_WAITS = []


def norm(v):
    """JSON 왕복 꼴(튜플 → 리스트 · 키 문자열) — 스냅샷과 같은 꼴로 맞댄다"""
    return json.loads(json.dumps(v, ensure_ascii=False, sort_keys=True, default=str))


def base(cid, v):
    """기준 칸 — regress: 바탕 스냅샷 값(그 칸이 스냅샷에 없으면 v 자신 = 첫 기록) · 잰 값 v 는 늘 스냅샷 출력에 적힌다"""
    nv = norm(v)
    with _lock:
        if cid in _OUT and _OUT[cid] != nv:
            _DUP.add(cid)
        _OUT[cid] = nv
    if REGRESS and cid in _SNAP:
        return _SNAP[cid]
    return nv


def same(cid, v):
    return norm(v) == base(cid, v)


def base_note(cid):
    """결과 값 끝에 붙일 말 — 기댓값이 어디서 왔나"""
    if not REGRESS:
        return '바탕 띄움'
    return '기준 스냅샷' if cid in _SNAP else '기준 첫 기록(스냅샷 없음)'


def want(cid, smoke=False):
    """이 칸을 이번 모드에서 재나 — gate · regress = 예 · smoke = smoke 칸만"""
    return (not SMOKE) or bool(smoke)


def launch(kind, n=1):
    """앱 띄움 셈 — 'new' | 'base' · 바탕을 띄우는 자리마다 QJ.launch('base')"""
    with _lock:
        _CNT['launch:' + kind] += n


def sub(kind, n=1):
    """하위 프로세스 셈 — 'git:show-app'(바탕 풀기) · 'git:archive' · 'git:fetch' · 'python:harness'(하위 하네스) · 'python:bake'(굽기) · 'pdftotext' …"""
    with _lock:
        _CNT['sub:' + kind] += n


class stage(object):
    """단계 시간(§B-3 단계별 분) — with QJ.stage('B3 목록 창'): …"""

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.t = time.time()
        return self

    def __exit__(self, *a):
        with _lock:
            _STAGES.append([self.name, round(time.time() - self.t, 2)])
        return False


def until(page, js, timeout_ms=15000, what='', arg=None):
    """조건 기다림(A-2-3) — 앱이 이미 내놓는 표지(요소 · 글 · 클래스 · __HM 같은 하네스 표지)만 · 걸린 시간을 남긴다"""
    t = time.time()
    try:
        if arg is None:
            page.wait_for_function(js, timeout=timeout_ms)
        else:
            page.wait_for_function(js, arg=arg, timeout=timeout_ms)
        ok = True
    except Exception:
        ok = False
    with _lock:
        _WAITS.append(['until', what or js[:60], round(time.time() - t, 3), ok])
    return ok


def sleep(ms, why, page=None):
    """남는 고정 대기 — 까닭을 꼭 적는다(A-2-3) · page 를 주면 page.wait_for_timeout(그동안 route · 요청이 돈다 —
    time.sleep 은 Playwright 동기 API 에서 route 처리를 멈춰 선 요청이 멎는다 · 일꾼 S3 10/4 보고)"""
    with _lock:
        _WAITS.append(['sleep', why, ms / 1000.0, True])
    if page is not None:
        page.wait_for_timeout(ms)
    else:
        time.sleep(ms / 1000.0)


WIDTHS = [320, 360, 390, 414, 768, 834, 1024, 1280, 1440, 1920]
FAIL_WIDTHS = [390, 768, 820, 830, 834, 850, 858, 1024, 1238, 1250, 1266, 1280, 1440]   # 9/20~10/3 넘침 · 줄 나뉨 FAIL 폭 — _qa_slim\fail_widths.md 로 채움
_RX_BREAK = re.compile(r'@(?:media|container)[^{]*?\(\s*(?:max|min)-width\s*:\s*(\d+(?:\.\d+)?)px\s*\)')


def app_breaks(app_html_path):
    """앱 꺾임 폭(CSS @media · @container 의 max/min-width px 값 전부)"""
    try:
        with open(app_html_path, encoding='utf-8', errors='replace') as f:
            s = f.read()
    except Exception:
        return []
    return sorted({int(float(x)) for x in _RX_BREAK.findall(s)})


def widths(app_html_path=None, lo=300, hi=1920, extra=()):
    """표본 폭 = WIDTHS + 앱 꺾임 폭 ±1 + 지난 FAIL 폭 + extra · lo~hi 안"""
    w = set(WIDTHS) | set(FAIL_WIDTHS) | set(extra)
    if app_html_path:
        for b in app_breaks(app_html_path):
            w |= {b - 1, b, b + 1}
    return sorted(x for x in w if lo <= x <= hi)


def sample(seq, n, seed='qa_slim'):
    """씨앗 고정 표본 — 고른 것은 원래 차례 그대로"""
    seq = list(seq)
    if n >= len(seq):
        return seq

    def key(i):
        s = json.dumps(seq[i], ensure_ascii=False, sort_keys=True, default=str)
        return hashlib.md5(('%s|%s' % (seed, s)).encode('utf-8')).hexdigest()
    pick = set(sorted(range(len(seq)), key=key)[:n])
    return [x for i, x in enumerate(seq) if i in pick]


def rng(seed='qa_slim'):
    return random.Random(seed)


def flush():
    """스냅샷 · 셈을 지금 적는다(atexit 에서도 부른다) — regress · smoke 만"""
    if GATE or not SNAP_OUT:
        return
    try:
        d = os.path.dirname(os.path.abspath(SNAP_OUT))
        os.makedirs(d, exist_ok=True)
        with _lock:
            snap = {'v': _OUT, 'mode': MODE, 'dup': sorted(_DUP), 'from': SNAP_IN or '', 'n': len(_OUT),
                    'at': time.strftime('%Y-%m-%d %H:%M:%S')}
            lj = {'mode': MODE, 'cnt': dict(_CNT), 'sec': round(time.time() - T0, 1), 'stages': list(_STAGES),
                  'until_n': sum(1 for w in _WAITS if w[0] == 'until'),
                  'until_sec': round(sum(w[2] for w in _WAITS if w[0] == 'until'), 1),
                  'until_timeout': sum(1 for w in _WAITS if w[0] == 'until' and not w[3]),
                  'sleep_n': sum(1 for w in _WAITS if w[0] == 'sleep'),
                  'sleep_sec': round(sum(w[2] for w in _WAITS if w[0] == 'sleep'), 1),
                  'sleep_why': sorted({w[1] for w in _WAITS if w[0] == 'sleep'})}
        with open(SNAP_OUT, 'w', encoding='utf-8') as f:
            json.dump(snap, f, ensure_ascii=False, sort_keys=True)
        with open(os.path.join(d, 'launch.json'), 'w', encoding='utf-8') as f:
            json.dump(lj, f, ensure_ascii=False, sort_keys=True)
    except Exception as e:
        sys.stderr.write('_qa_jo_common: 스냅샷 · 셈 못 적음 (%s)\n' % e)


atexit.register(flush)
