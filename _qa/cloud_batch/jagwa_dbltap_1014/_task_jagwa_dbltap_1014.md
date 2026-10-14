# _task_jagwa_dbltap_1014 — 자과 물리 폰: 서랍 고친 제목 두 번 톡톡이 문항 창 자리에서도 잡히게 [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(물리 · 폰): 서랍 고친 제목(파랑)을 두 번 톡톡 하면, 첫 톡(그 문항 열기)이 문항 창을 서랍 위로 올리거나 줄을 몇 px 굴려도 둘째 톡이 잡혀 검정 ↔ 파랑이 바뀜(옛 = 둘째 톡이 문항 창 필기 판 · 옆 칸에 떨어져 안 바뀜) · 둘째 톡은 창 · 필기 판에 넘기지 않음 · PC · 한 번 톡 = 옛 그대로.

- 판 크기 = 작음(앱 패치 1 · 짤 것 0)
- 로컬 필요 = 0
- 시간 = ≈12 분(선례 = jagwa_link_why_1013 12 분 · jagwa_bundle4_1014 관문 29 칸 14 분 → 이번 14 칸)

## 할 일(차례대로 · 이것만)
1. `git fetch origin main cloud/inbox` · 바탕 = main **833cabe**(`jagwa/index.html` LF md5 **483a10dd** · `_qa/_qa_small_gate.py` md5 **867625c3**) — 다르면 멈추고 커밋 없이 이 줄만 알림.
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_dbltap_1014/` 에서 둘을 꺼냄: `app_patches.txt`(md5 4599c70f) · `spec_dbltap.json`(fe00a8b4).
3. `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect 3fffd377` — 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문: `python _qa/_qa_small_gate.py --spec spec_dbltap.json --new jagwa/index.html --base 833cabe --eng chromium,webkit --base-eng chromium`(`--vendor` · `--spd` · `--notes` 는 지난 판과 같이).
   - 명세 = 지난 판(jagwa_bundle4_1014) 명세의 서랍 화면 둘(ucp1 · ucm1) 14 칸 그대로 · 차례도 그대로(작은 창 칸 뒤 두 번 톡톡 = 지난 판에서 폰 FAIL 이 난 꼴) · `yard` = 지난 판 커밋 글의 그 칸 값(바탕 833cabe = 폰 두 번 톡톡 넷 FAIL · 나머지 PASS).
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(통째 다시 금지). 앱 결함이면 고치지 말고 칸 이름 · 값 · 둘째 톡이 떨어진 자리(elementFromPoint)만 알림 · 「누를 점이 가려짐」 · 「누를 것 없음」 = 명세 탓 → 진단만 적고 명세 손대지 않음.
5. 회귀 사슬 · grep 회귀 안 돌림(규칙 (96) ④ 작은 고침 · (85)).
6. 커밋 하나(`jagwa/index.html`) · main 이 바탕 그대로면 fast-forward push · 커밋 글 = 관문 결과 줄 그대로(PASS/FAIL · 엔진 · 바탕) · 앱 md5 · 단계별 분.
- 지킬 것: 공개 저장소 — 시험 글은 명세 안 지어낸 글뿐 · 사용자 기록 0. `cloud/inbox` 가지 · 그 폴더는 건드리지 않음(채팅이 검수 뒤 걷음). `jagwa/theory_fix.json` 은 건드리지 않음.
- 사용자 할 일 = 앱 새로고침 한 번.

## 패치가 하는 일(1 쌍 · 채팅이 483a10dd 에 넣어 3fffd377 · 1,593,922 B · 인라인 스크립트 문법 오류 0 잼)
- 서랍 제목 두 번 톡톡 손(pnBlk) — 첫 톡 = 옛 그대로(고친 제목 .ndtt 위 pointerup 이면 자리 · 시각 적음) · 둘째 톡 = pointerdown 이 첫 톡 자리 24px · 400ms 안이면 무엇 위든(문항 창 · 필기 판 CANVAS#inkc · 옆 칸) 잡기 단계에서 먹고(그 pointerdown · move · up · 따라오는 click 을 앱에 안 넘김) pointerup 에서 그 제목 nmk 켬/끔 · 시안(거울 누름) 14/14 PASS 그대로.

## 점검표(채팅)
1. 일꾼 = 클라우드 · 2. 한 판 · 3. 회귀 = 없음(작은 고침 (96) ④) · 4. 선례 = 지난 판 pnBlk(10/14 bundle4 쌍 25) · 끌기 놓은 뒤 click 먹기(G3DRAG · window 잡기) · 5. 저장 칸 무변(TFIX nmk) · 6. 근거 = 지난 판 관문 FAIL 진단 ①②(커밋 833cabe 글) · 사용자 17:31 「지시서」 · 10. 더 빨리 = 공용 관문 + 지난 판 명세 그대로(서랍 화면만) · 채팅은 클라우드 관문 안 돌림 · 회귀 0 · 13. inbox · 14. 뺨 것 = 지난 판 명세 쪽 칸(ed 폰 길게 바탕 접힘 경합) · 15. 과목 맞춤 = 물리 서랍(고친 제목 두 번 톡톡) · 폰 좌표 누름은 관문만 잼(시안 거울은 요소 누름).
