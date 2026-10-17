# _task_jagwa_thbang_1017 — 자과 물리: ! 켠 공식·개념 = 통짜 창 붉은 세로줄 · ! 근거 있는 문항 = 목차 서랍 줄 붉은 세로줄 [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**: ① 통짜 물리 목차 창(어디서 열든 — 목차 창 · 공식·개념 줄 누름 창 · 개념/쓰인 문항 창 · 근거 블록 창)에서 어느 문항이든 ! 를 켠 공식·개념 근거의 블록 줄 = 왼쪽 붉은 세로줄 3px ② 목차 서랍에서 ! 근거가 하나라도 있는 문항 줄 = 왼쪽 세로줄 붉게(지금 문항 줄의 청록 세로줄 자리 · 없는 줄은 그대로) ③ ! 를 켜고 끄면 서랍 줄이 그 자리에서 바뀜. 저장 칸 무변.

- 판 크기 = 작음(앱 패치 8 · 짤 것 0)
- 로컬 필요 = 0
- 시간 = ≈5 분(선례 = jagwa_bangline_1017 착수 → push 5 분 · 관문 6 칸 / 이 판 8 칸)

## 할 일(차례대로 · 이것만)
1. `git fetch origin main cloud/inbox` · 바탕 = main **1735e44**(`jagwa/index.html` LF md5 **f16103c2** · `_qa/_qa_small_gate.py` md5 **867625c3**) — 다르면 멈추고 커밋 없이 이 줄만 알림.
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_thbang_1017/` 에서 둘을 꺼냄: `app_patches.txt`(md5 95116fa0) · `spec_thbang.json`(e06fb138).
3. `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect 1c93b70e` — 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문: `python _qa/_qa_small_gate.py --spec spec_thbang.json --new jagwa/index.html --base 1735e44 --eng chromium,webkit --base-eng chromium`(`--vendor` · `--spd` · `--notes` 는 지난 판과 같이).
   - 명세 = 채팅 시안(PC · 폰 8 칸) 그대로 · setup 이 115 근거 셋(공식·개념 T: ! 켬 · 공식·개념 U: ! 켬 · 트리거 끔)을 메모리에만 넣음(저장 안 함 · 사용자 기록 무변) · 바탕 1735e44 = 8 칸 다 FAIL(`yard: true`) — 시안 거울로 새 8/8 PASS · 바탕 8 FAIL 잼.
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(통째 다시 금지). 앱 결함이면 고치지 말고 칸 이름 · 값만 알림.
5. 회귀 사슬 · grep 회귀 안 돌림(작은 고침).
6. 커밋 하나(`jagwa/index.html`) · main 이 바탕 그대로면 fast-forward push · 커밋 글 = 관문 결과 줄 그대로(PASS/FAIL · 엔진 · 바탕) · 앱 md5 · 단계별 분.
- 지킬 것: 공개 저장소 — 시험 글은 명세 안 글뿐 · 사용자 기록 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(파일은 채팅이 검수 뒤 지움 · 가지는 그대로 · 가지 지울 일 없음). `jagwa/theory_fix.json` 은 건드리지 않음.
- 사용자 할 일 = 앱 새로고침 한 번.

## 패치가 하는 일(8 쌍 · 채팅이 f16103c2 에 넣어 1c93b70e · 1,603,642 B · 인라인 스크립트 문법 오류 0 잼)
1~3. `secHTML(sec)`(통짜 절을 그리는 한 곳 · theorySheet · 목차 줄 누름 · 개념/쓰인 문항 창 · g3SecMark 가 다 부름) — 머리에서 `g3BangNodes()` 를 한 번 받아 그 Set 에 든 줄(.thl) · 그림 칸(.thpicbox)에 class `thbang`.
4. `g3BangNodes()` 새 함수(g3SecMark 옆) — GG 전체에서 `bang` · 칸 c · `ref` 있는 근거만: `T:` 는 블록 첫 줄부터 다음 들임 0 줄/br 앞까지 · `U:^id` 는 있던 `g3SecHit(sec,id).all`(점선 짝 길 그대로). 교재 모드(HASBOOK)면 빈 Set.
5. `navBuild` 서랍 줄(.ndrow) 만들 때 `ggBangAny(GGU(r))` 면 class `ndbang`.
6. `ggBangPaint(uid)` — 있던 `any` 를 그 문항 서랍 줄 `ndbang` 에도 씀(켜고 끄면 그 자리).
7. `ggRepaint` 감싸기(서랍 .ndox 다시 칠하는 곳) — 같은 줄 `ndbang` 도 다시 칠함.
8. CSS — `.ndrow.ndbang{border-left-color:var(--red)}` · `.thl.thbang,.thpicbox.thbang{box-shadow:inset 3px 0 0 var(--red)}`.

## 점검표(채팅)
1. 일꾼 = 클라우드 · 2. 한 판 · 3. 회귀 = 없음(작은 고침) · 4. 선례 = bangline(1735e44 · ggBangPaint 의 [data-gbbox] 길) · g3SecHit(secline · 점선 짝) · `.ndrow.cur` 세로줄 자리 · 5. 저장 칸 무변 · 6. 근거 = 사용자 10/17 17:12 「공식·개념에도 ! 해 놨으면 통짜 물리 목차 창에서도 왼쪽에 빨간 세로줄 · 이 창 열리는 어느 곳에서도 · ! 근거 있는 문제는 목차 서랍에서도 문항 왼쪽에 빨간 세로줄」 · 10. 더 빨리 = 공용 관문 + 시안 명세 · 13. inbox.
