# _task_jagwa_twcount_1015 — 자과 물리: 트리거 · 주의점 인용 숫자 합침 [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(물리 · 지학 · 생물 근거 1 · 3 칸): 같은 글이 어느 문항엔 트리거 · 어느 문항엔 주의점에 있어도 줄 옆 인용 숫자(문제 창 근거 줄 · 서랍 작은 창) = 두 칸 합친 문항 수 · 숫자 누름 창 목록도 합침. 공식·개념(2 칸) 무변 · 저장 칸 무변.

- 판 크기 = 작음(앱 패치 1 · 짤 것 0)
- 로컬 필요 = 0
- 시간 = ≈6 분(선례 = jagwa_twinchip_1015 착수 → push 6 분 · 관문 6 칸)

## 할 일(차례대로 · 이것만)
1. `git fetch origin main cloud/inbox` · 바탕 = main **87a3695**(`jagwa/index.html` LF md5 **b2ead861** · `_qa/_qa_small_gate.py` md5 **867625c3**) — 다르면 멈추고 커밋 없이 이 줄만 알림.
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_twcount_1015/` 에서 둘을 꺼냄: `app_patches.txt`(md5 90adfa62) · `spec_twcount.json`(d9f1dac1).
3. `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect e119fb30` — 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문: `python _qa/_qa_small_gate.py --spec spec_twcount.json --new jagwa/index.html --base 87a3695 --eng chromium,webkit --base-eng chromium`(`--vendor` · `--spd` · `--notes` 는 지난 판과 같이).
   - 명세 = 채팅 시안(PC · 폰 6 칸) 그대로 · setup 이 115 트리거 · 116 주의점에 같은 지어낸 글을 메모리에만 넣음(저장 안 함 · 사용자 기록 무변) · 바탕 87a3695 = 6 칸 다 FAIL(`yard: true` · 숫자 1 · 줄 1) — 시안 거울로 새 6/6 PASS · 바탕 6 FAIL 잼.
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(통째 다시 금지). 앱 결함이면 고치지 말고 칸 이름 · 값만 알림.
5. 회귀 사슬 · grep 회귀 안 돌림(작은 고침).
6. 커밋 하나(`jagwa/index.html`) · main 이 바탕 그대로면 fast-forward push · 커밋 글 = 관문 결과 줄 그대로(PASS/FAIL · 엔진 · 바탕) · 앱 md5 · 단계별 분.
- 지킬 것: 공개 저장소 — 시험 글은 명세 안 글뿐 · 사용자 기록 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(파일은 채팅이 검수 뒤 지움 · 가지는 그대로 · 가지 지울 일 없음). `jagwa/theory_fix.json` 은 건드리지 않음.
- 사용자 할 일 = 앱 새로고침 한 번.

## 패치가 하는 일(1 쌍 · 채팅이 b2ead861 에 넣어 e119fb30 · 1,601,225 B · 인라인 스크립트 문법 오류 0 잼)
1. `g3Users(f,key)` — f 가 트리거(t) · 주의점(w)이면 두 칸 항목을 같이 셈(찾기 g3SugList 댓글 v38 「트리거랑 주의점은 검색 범위 같게」 와 같은 범위) · 공식·개념(c)은 그대로. 이 함수를 쓰는 셋(근거 줄 숫자 g3UseHTML · 작은 창 숫자 .g3pn · 숫자 누름 창 g3UseWin 목록)이 다 따라감.

## 점검표(채팅)
1. 일꾼 = 클라우드 · 2. 한 판 · 3. 회귀 = 없음(작은 고침) · 4. 선례 = 10/8 댓글 v38(찾기는 두 칸 합침 · 그때 「근거 줄 쓰인 수(g3Users)는 그대로」 로 남겨 둔 것을 이번에 같게) · 10/14 15:19 작은 창 트리거 · 주의점 숫자(같은 g3Users) · 5. 저장 칸 무변 · 6. 근거 = 사용자 10/15 15:18 「근거가 트리거에 있든 주의점에 있든 연결 인용 숫자는 그냥 통틀어서 나오게」 · 10. 더 빨리 = 공용 관문 + 시안 명세 · 13. inbox.
