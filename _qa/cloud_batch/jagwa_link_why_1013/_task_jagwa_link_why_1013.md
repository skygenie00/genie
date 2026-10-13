# _task_jagwa_link_why_1013 — 자과: 연결 칩 · 연결한 까닭 · 연결 줄 누름 = 문항 창 · 같은 근거 다른 문항 댓글 · 댓글 길게 고치기 · ✕ [클라우드 · 작은 고침 10 분 꼴 · main push 한 번]

**화면에서 달라지는 것**: (지학 · 생물) 문항 창 머리 줄 「🔗 N」 · (세 과목) 첫 화면 목록 줄 「🔗 N」 · 서랍 O X 근거 작은 창 🔗 목록 = 카드 층은 보이는 ID 만(물리는 제목 그대로) + 회색 연결한 까닭 · 줄 길게 = 까닭 적기(머리 🔗 작은 창 줄도 같은 글) · 줄 누름 = 그 문항 창(열려 있으면 옆 작은 창 · 쌍둥이 미리보기 창 안 뜸) · 근거 「댓」 = 같은 근거를 쓰는 다른 문항 댓글도 · 줄 오른쪽 끝 그 문항 ID · 댓글 길게 = 고치기 · 지우기 = ✕.

- 판 크기 = 작음(패치 17 · 짤 것 0)
- 로컬 필요 = 0
- 시간 = ≈10 분(패치 넣기 1 · 관문 Chromium 새 + 바탕 ≈5 · WebKit 새 ≈3 · 커밋 · push 1 — 관문 Chromium 시간은 채팅이 이 명세로 잰 값 5.1 분(27 칸 다 PASS · 바탕 다 FAIL))

## 할 일(차례대로 · 이것만)
1. `git fetch origin main cloud/inbox` · 바탕 = main **d9961b8**(`jagwa/index.html` LF md5 **a5aca5b3**) — 다르면 멈추고 커밋 글 없이 이 줄만 알림.
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_link_why_1013/` 에서 넷을 꺼냄: `_task_jagwa_link_why_1013_patches.txt` · `spec_link_why.json` · `_qa_small_gate.py` · `_qa_apply_patches.py`.
3. `_qa_small_gate.py` · `_qa_apply_patches.py` 를 작업트리 `_qa/` 에 둠(새 공용 도구 — 이 판 커밋에 같이 넣음 · 다음 작은 판부터 지시서가 부름).
4. `python _qa/_qa_apply_patches.py <patches.txt> jagwa/index.html --expect 8e2cf21a` — 멈추면(종료 2 · 3) 그 줄만 알림.
5. 관문: `python _qa/_qa_small_gate.py --spec <spec_link_why.json> --new jagwa/index.html --base d9961b8 --eng chromium,webkit --base-eng chromium`(WebKit 먼저 깔고 · 공용 `_qa_jagwa_common` 길 그대로 · `--vendor` · `--spd` 는 지난 판 하네스와 같이).
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(통째 다시 금지). 앱 결함이면 고치지 말고 칸 이름 · 값만 알림 · 하네스 쪽 흔들림(누를 것 없음 · 늦게 뜸)이면 그 칸 `wait` 만 늘려 한 번 더.
   - 명세 칸 = 채팅 시안 v4(VMkj3478UJ89pPV2C6vmrJ) 점검 27 칸 그대로 · 세 과목 · PC 마우스 · 폰 손가락 · 길게 · Enter 저장 · 헛잣대(바탕 d9961b8 = 다 FAIL).
6. 회귀 사슬 · grep 회귀 안 돌림(규칙 (96) ④ 작은 고침 · (85)).
7. 커밋 하나(`jagwa/index.html` + `_qa/_qa_small_gate.py` + `_qa/_qa_apply_patches.py`) · main 이 바탕 그대로면 fast-forward push · 커밋 글 = 관문 결과 줄 그대로(PASS/FAIL · 엔진 · 바탕) · 앱 md5 · 단계별 분.
- 지킬 것: 공개 저장소 — 시험 글은 명세 안 지어낸 글뿐 · 사용자 기록 0. `cloud/inbox` 가지 · 그 폴더는 건드리지 않음(채팅이 검수 뒤 걷음). `jagwa/theory_fix.json` 은 건드리지 않음.
- 사용자 할 일 = 앱 새로고침 한 번.

## 패치가 하는 일(17 쌍 · 채팅이 a5aca5b3 에 넣어 8e2cf21a · 스크립트 문법 오류 0 잼)
1. 카드 층 머리 `#vLink` 숨김 CSS 걷음 · 카드 층 문항 그리기에 `linkChip()` · 카드 층 `#vLink` 누름 = `relPop`(쌍 1 · 2 · 14).
2. 목록 줄 `.tag.lk` 세 과목(쌍 3).
3. 서랍 작은 창 연결 줄 = 카드 층 ID 만 · `span.g3lkw` 까닭 · `data-lw`(쌍 4) · 연결 작은 창(`relPop`) 연결 탭 줄도(쌍 15).
4. 줄 누름 = vSwapOpen / openView(옛 twinPeek)(쌍 5 · 16).
5. 길게 누름 SEL 에 연결 줄 · 댓글 줄 · `lkwKey` · `lkwOf` · `lkwEdit`(저장 = TFIX `'L|a~b'` 칸 w · 세 과목 tfix 동기화 칸 이미 · 새 저장 칸 0)(쌍 6 · 7 · 8).
6. 같은 근거(같은 칸 · g3Key) 다른 문항 댓글 `.g3oc` · `b.gq`(쌍 10 · 11 · 12 · 13) · CSS(쌍 9).
7. 댓글 = 길게 고치기(`data-gce` · SHELL) · 지우기 ✕ `.ggcx`(쌍 17).

## 점검표(채팅)
1. 일꾼 = 클라우드 · 2. 한 판 · 3. 회귀 = 없음(작은 고침 (96) ④) · 4. 선례 = 공식 칸 `'F|'` TFIX 꼴 · 연결 창 줄 `[data-go]` 길 · 「쓰인 수」 g3Key · 5. 저장 칸 무변 · 6. 근거 = 사용자 10/13 21:27 · 21:39 · 22:03 · 시안 댓글 셋 · 23:40 「작은 판은 10 분 안」 · 10. 더 빨리 = 관문을 새로 짜지 않음(공용 작은 고침 관문 + 시안 명세) · 헛잣대 한 엔진 · 회귀 0 · 13. inbox · 14. 뺀 것 = 하네스 새로 짜기 · 관문 통째 다시 · 회귀 · 15. 과목 맞춤 = 세 과목 다(명세에 물리 · 생물 화면 있음).
