# -*- coding: utf-8 -*-
r"""jagwa_recstore_1019 §F 관문을 회귀 사슬에서 돌리는 껍데기(2026-10-19 Code) — 몸 = 맨 위 `_qa_tabguard_gate.py`(지시서가 정한 자리 그대로 · genie `_qa/_qa_tabguard_gate.py`)
  python jagwa/_harness_jagwa_recstore.py <앱 index.html> [--eng chromium,webkit] [--port 0]
  인자는 그대로 넘기고 그 종료 코드를 그대로 돌려준다 · 결과 줄 = 몸이 찍는 「PASS|FAIL | <엔진> <칸> | <값>」
  껍데기를 두는 까닭: _qa_sync 모음 = _harness_*.py + 그것이 부르는 모듈 — 몸만 두면 전수표 줄을 못 달고(전수표 어긋남) `_qa_sync copy` 가 _qa 사본을 지운다."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(os.path.dirname(HERE), '_qa_tabguard_gate.py')
sys.exit(subprocess.run([sys.executable, GATE] + sys.argv[1:]).returncode)
