# -*- coding: utf-8 -*-
r"""앱 무관 회귀 헬퍼 QC — _task_qa_slim2 A-1-2(2026-10-08) · 실제 몸 = _qa_jo_common.py(QJ · 10/4 _task_qa_slim) 한 벌을 이 이름으로 다시 내보냄(같은 함수 두 벌 없음 ㊜).

왜 몸이 jo 쪽에 남나: jo 사슬 전수표 50 줄의 입력(저장본 열쇠)에 n:_qa_jo_common.py 가 들어 있다(10/8 잼). 그 파일 바이트를 바꾸면
jo 저장본 열쇠 50 이 다 바뀌어 §B-7 「jo 열쇠 · 결과 그대로」가 깨진다 → 몸은 그 파일에 바이트 그대로 두고, 자과 · 민법 · 시간표는 이 이름으로 부른다.

쓰는 법(자과 · 민법 · 시간표 하네스) — 머리 5 줄(_roots 찾기) 바로 뒤, 다른 하네스 import 와 인자 읽기보다 먼저:
    import _qa_common as QC

  QC.MODE 'gate'|'regress'|'smoke' · QC.GATE · QC.REGRESS(regress 또는 smoke) · QC.SMOKE — import 때 sys.argv 에서 --mode · --snap-in · --snap-out 을 뗀다
  기준 칸: QC.base(cid, v) · QC.same(cid, v) · QC.norm(v) · QC.base_note(cid)
  smoke: QC.want(cid, smoke=True)
  셈(§B-4): QC.launch('new'|'base') · QC.sub('git:show-app'|'git:archive'|'git:fetch'|'python:harness'|'python:bake'|'pdftotext'|…) — regress 에서 base · git:* · python:harness · python:bake = 0
  기다림(A-2): QC.until(page, js, timeout_ms, '표지') · QC.sleep(ms, '까닭', page) · 단계 시간 with QC.stage('B3'):
  표본(A-3): QC.WIDTHS · QC.widths(앱 경로) · QC.sample(seq, n, '<하네스>') · QC.rng(seed)
  스냅샷 · 셈은 끝에 저절로(atexit) — QC.flush() 로 당겨 적을 수 있음
"""
from _qa_jo_common import *   # noqa: F401,F403  — MODE · GATE · REGRESS · SMOKE · SNAP_IN · SNAP_OUT · T0 · WIDTHS · FAIL_WIDTHS · norm · base · same · base_note · want · launch · sub · stage · until · sleep · app_breaks · widths · sample · rng · flush
import _qa_jo_common as _QJ   # noqa: E402  — 몸(상태 · atexit) 은 이 모듈 하나

HELPER = 'qa_common'   # 이 이름으로 불렀다는 표지(셈 · 보고용)
