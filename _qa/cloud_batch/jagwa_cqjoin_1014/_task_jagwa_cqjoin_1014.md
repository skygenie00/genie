# _task_jagwa_cqjoin_1014 — 자과 물리: 교재 개념 줄 = 블록 찾기로 넣은 근거와 한 갈래 [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(물리): 근거 공식·개념 칸의 교재에 이어 둔 개념 줄(예 PA1603 「(1) 탄성충돌」)을 누르면 그 개념이 블록 찾기로 넣은 근거와 같은 항목으로 합쳐지고(같은 개념 열쇠 · 보이던 줄 그대로 · 같은 자리 · 그 줄 댓글 옮김) 넣은 근거 창이 열림 → 줄 고르기 · 고치기 · 끌기 · 댓글 · 쓰인 수가 블록 찾기로 넣은 줄(P123 「(3) 원운동」 · P110 「(1) 탄성충돌」)과 똑같음. 교재 이음 자체는 안 건드림.

- 판 크기 = 작음(앱 패치 2 · 짤 것 0)
- 로컬 필요 = 0
- 시간 = ≈8 분(선례 = jagwa_pnframe_1014 착수 → push 6 분 · 관문 16 칸 3.1 분 → 이번 8 칸)

## 할 일(차례대로 · 이것만)
1. `git fetch origin main cloud/inbox` · 바탕 = main **1a7a3da**(`jagwa/index.html` LF md5 **68ac80fb** · `_qa/_qa_small_gate.py` md5 **867625c3**) — 다르면 멈추고 커밋 없이 이 줄만 알림.
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_cqjoin_1014/` 에서 둘을 꺼냄: `app_patches.txt`(md5 c58f8f09) · `spec_cqjoin.json`(cc23e951).
3. `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect 951a9bff` — 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문: `python _qa/_qa_small_gate.py --spec spec_cqjoin.json --new jagwa/index.html --base 1a7a3da --eng chromium,webkit --base-eng chromium`(`--vendor` · `--spd` · `--notes` 는 지난 판과 같이).
   - 명세 = 채팅 시안(PC · 폰 8 칸) 그대로 · 바탕 1a7a3da = 8 칸 다 FAIL(`yard: true` · 시안 거울로 잼).
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(통째 다시 금지). 앱 결함이면 고치지 말고 칸 이름 · 값만 알림 · 「누를 점이 가려짐」 · 「누를 것 없음」 = 명세 탓 → 진단만 적고 명세 손대지 않음.
5. 회귀 사슬 · grep 회귀 안 돌림(규칙 (96) ④ 작은 고침 · (85)).
6. 커밋 하나(`jagwa/index.html`) · main 이 바탕 그대로면 fast-forward push · 커밋 글 = 관문 결과 줄 그대로(PASS/FAIL · 엔진 · 바탕) · 앱 md5 · 단계별 분.
- 지킬 것: 공개 저장소 — 시험 글은 명세 안 지어낸 글뿐 · 사용자 기록 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(파일은 채팅이 검수 뒤 지움 · 가지는 그대로 · 가지 지울 일 없음). `jagwa/theory_fix.json` 은 건드리지 않음.
- 사용자 할 일 = 앱 새로고침 한 번.

## 패치가 하는 일(2 쌍 · 채팅이 68ac80fb 에 넣어 951a9bff · 1,596,323 B · 인라인 스크립트 문법 오류 0 잼)
1. 쌍 1 — `g3UseWinQ`(교재 개념 줄 누름) 첫머리: 쓰인 문항 목록 창이 아니고 그 개념 블록(U:^개념 id)이 있으면 `g3CqJoin` 으로 감(없으면 옛 그대로).
2. 쌍 2 — `g3CqJoin` 새 함수: `g3Push(uid,'c',{ref:'U:^'+개념 id, sl: 블록 줄 전부, t})` = 블록 찾기로 넣기와 같은 길(같은 열쇠라 교재 줄은 g3Cq 거름으로 숨음) · 그 줄 댓글(cqx c[개념 키]) → 항목 cs · 차례(cqx o 의 'q:개념 키' 자리) → 'g:항목 키' · 끝에 `g3UseWin('c',…)` = 넣은 근거 창(줄 고르기 g3SelWire).

## 점검표(채팅)
1. 일꾼 = 클라우드 · 2. 한 판 · 3. 회귀 = 없음(작은 고침 (96) ④) · 4. 선례 = 블록 찾기로 넣기(g3Pick → g3Push · 같은 열쇠 U:^ 면 교재 줄 숨음 · P123 · P110 · P115 원격 기록) · 5. 저장 칸 무변(GG 공식·개념 항목 · cqx o · c) · 6. 근거 = 사용자 18:46 「근거에서 왜 줄마다 선택 안 돼 · PA1603」 · 20:04~20:13 「교재 개념 줄을 블록 찾기로 넣은 줄과 같은 항목 하나로 합쳐 · 바꿔」 · 10. 더 빨리 = 공용 관문 + 시안 명세 · 채팅은 클라우드 관문 안 돌림 · 13. inbox(먼저 올린 jagwa_cqsel_1014 는 걷음) · 14. 뺀 것 = 줄 고르기만 따로 붙이는 판(cqsel) · 15. 과목 맞춤 = 물리만(교재 개념 CB = 물리 · 지학 · 생물은 g3UseWinQ 첫 줄에서 돌아감).
