# _task_jagwa_pnframe_1014 — 자과: 제목 고치는 칸 테두리 누름 = 파랑 ↔ 검정 · 두 번 톡톡 걷음 [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(세 과목 · 고치는 칸이 같은 함수): 제목을 길게 눌러 고치는 칸(서랍 줄 · 문제 창 제목 · 첫 화면 목록)이 테두리 틀(5px)로 둘러싸이고, 틀 색 = 그 제목 색(파랑 / 검정) · 틀을 누르면 바로 파랑 ↔ 검정(기기끼리 맞춤 · 고치는 칸은 그대로 열림 · 글 고치기 · ✓ · Enter 무변) · 서랍 제목 두 번 톡톡은 걷음(사용자 17:53 「아이패드에서도 잘 안 되고 오류 나기 쉬워」).

- 판 크기 = 작음(앱 패치 2 · 짤 것 0)
- 로컬 필요 = 0
- 시간 = ≈12 분(선례 = jagwa_link_why_1013 12 분 · jagwa_bundle4_1014 관문 29 칸 14 분 → 이번 16 칸)

## 할 일(차례대로 · 이것만)
1. `git fetch origin main cloud/inbox` · 바탕 = main **833cabe**(`jagwa/index.html` LF md5 **483a10dd** · `_qa/_qa_small_gate.py` md5 **867625c3**) — 다르면 멈추고 커밋 없이 이 줄만 알림.
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_pnframe_1014/` 에서 둘을 꺼냄: `app_patches.txt`(md5 6ead43e0) · `spec_pnframe.json`(3d2f4a7e).
3. `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect 68ac80fb` — 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문: `python _qa/_qa_small_gate.py --spec spec_pnframe.json --new jagwa/index.html --base 833cabe --eng chromium,webkit --base-eng chromium`(`--vendor` · `--spd` · `--notes` 는 지난 판과 같이).
   - 명세 = 채팅 시안(PC · 폰 16 칸) 그대로 · 바탕 833cabe = `yard: true` 15 칸 FAIL · 「폰 두 번 톡톡 = 색 그대로」 1 칸만 바탕도 PASS(시안 거울로 잼).
   - 테두리 누름 칸은 틀 가장자리(왼쪽 2px)에 pointerdown 을 보내는 식(가운데 누름은 입력 칸이라 관문 누름으로 못 잼).
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(통째 다시 금지). 앱 결함이면 고치지 말고 칸 이름 · 값만 알림 · 「누를 점이 가려짐」 · 「누를 것 없음」 = 명세 탓 → 진단만 적고 명세 손대지 않음.
5. 회귀 사슬 · grep 회귀 안 돌림(규칙 (96) ④ 작은 고침 · (85)).
6. 커밋 하나(`jagwa/index.html`) · main 이 바탕 그대로면 fast-forward push · 커밋 글 = 관문 결과 줄 그대로(PASS/FAIL · 엔진 · 바탕) · 앱 md5 · 단계별 분.
- 지킬 것: 공개 저장소 — 시험 글은 명세 안 지어낸 글뿐 · 사용자 기록 0. `cloud/inbox` 가지 · 그 폴더는 건드리지 않음(채팅이 검수 뒤 걷음). `jagwa/theory_fix.json` 은 건드리지 않음.
- 사용자 할 일 = 앱 새로고침 한 번.

## 패치가 하는 일(2 쌍 · 채팅이 483a10dd 에 넣어 68ac80fb · 1,594,358 B · 인라인 스크립트 문법 오류 0 잼)
1. 쌍 1 — 서랍 제목 두 번 톡톡 손(pointerup 잡기) 걷음 · `pnFrame(el)` = 제목 고치는 칸의 입력 칸을 `span.pnfr` 로 감쌈 · 틀 색 = `TFIX[uid].nmk`(있으면 검정) · 틀(입력 칸 밖) pointerdown = nmk 켬/끔 · 칸 그대로 · 입력 칸 포커스 돌림 · `ndEdit` · `vtEdit` · `pnEdit` 를 감싸 고치는 칸이 열린 뒤 pnFrame.
2. 쌍 2 — CSS: 틀 5px · 파랑 #4F86D9 / 검정 #1F2329 · 안 입력 칸 테두리 0.

## 점검표(채팅)
1. 일꾼 = 클라우드 · 2. 한 판 · 3. 회귀 = 없음(작은 고침 (96) ④) · 4. 선례 = 지난 판 pnBlk(10/14 bundle4) · 제목 고치는 칸 iedOpen(10/13 ndEdit · vtEdit) · 5. 저장 칸 무변(TFIX nmk) · 6. 근거 = 사용자 17:35 「두 번 톡톡 잘 안 돼 · 문제 창만 열리고」 · 17:53 「테두리 눌러서 파랑 검정」 · 내장 브라우저 실제 앱 폭 612 마우스 두 번 누름 잼(둘째 누름 = 문항 창 필기 판) · 10. 더 빨리 = 공용 관문 + 시안 명세 · 채팅은 클라우드 관문 안 돌림 · 회귀 0 · 13. inbox(먼저 넣은 jagwa_dbltap_1014 는 걷음) · 14. 뺨 것 = 두 번 톡톡 고침 판 · 15. 과목 맞춤 = 세 과목 제목 고치는 칸(ndEdit · vtEdit · pnEdit 같은 함수 · 시안 · 명세 = 물리).
