# _task_jagwa_bangline2_1018 — 자과 물리: ! 켠 공식·개념 = 고른 줄만 붉은 세로줄 [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**: 개념 창에서 줄을 골라 둔 공식·개념 근거(g.sl)에 ! 를 켜면 통짜 물리 목차 창(어디서 열든)에서 그 고른 줄 · 그림만 왼쪽 붉은 세로줄 · 줄을 안 고른 근거는 지금처럼 블록 줄 전부. 저장 칸 무변.

- 판 크기 = 작음(앱 패치 1 · 짤 것 0)
- 로컬 필요 = 0
- 시간 = ≈5 분(선례 = jagwa_thbang_1017 착수 → push 6 분 · 관문 8 칸 / 이 판 6 칸)

## 할 일(차례대로 · 이것만)
1. `git fetch origin main cloud/inbox` · 바탕 = main **cbcd19e**(`jagwa/index.html` LF md5 **1c93b70e** · `_qa/_qa_small_gate.py` md5 **867625c3**) — 다르면 멈추고 커밋 없이 이 줄만 알림.
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_bangline2_1018/` 에서 둘을 꺼냄: `app_patches.txt`(md5 1a1b7e84) · `spec_bangline2.json`(085d89d2).
3. `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect 3deb0180` — 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문: `python _qa/_qa_small_gate.py --spec spec_bangline2.json --new jagwa/index.html --base cbcd19e --eng chromium,webkit --base-eng chromium`(`--vendor` · `--spd` · `--notes` 는 지난 판과 같이).
   - 명세 = 채팅 시안(PC · 폰 6 칸) 그대로 · setup 이 모든 근거 ! 를 메모리에서 끄고 115 · 116 근거 셋(고른 줄 한 줄 ! · 고른 줄 없음 ! · 옛 글로 고른 줄 + 그림 !)을 메모리에만 넣음(저장 안 함 · 사용자 기록 무변) · `yard: true` 4 칸 = 바탕 FAIL · `yard: false` 2 칸(고른 줄 없는 ! = 옛 그대로) = 바탕도 PASS — 시안 거울로 새 6/6 PASS · 바탕 그대로 잼.
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(통째 다시 금지). 앱 결함이면 고치지 말고 칸 이름 · 값만 알림.
5. 회귀 사슬 · grep 회귀 안 돌림(작은 고침).
6. 커밋 하나(`jagwa/index.html`) · main 이 바탕 그대로면 fast-forward push · 커밋 글 = 관문 결과 줄 그대로(PASS/FAIL · 엔진 · 바탕) · 앱 md5 · 단계별 분.
- 지킬 것: 공개 저장소 — 시험 글은 명세 안 글뿐 · 사용자 기록 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(파일은 채팅이 검수 뒤 지움 · 가지는 그대로 · 가지 지울 일 없음). `jagwa/theory_fix.json` 은 건드리지 않음.
- 사용자 할 일 = 앱 새로고침 한 번.

## 패치가 하는 일(1 쌍 · 채팅이 1c93b70e 에 넣어 3deb0180 · 1,604,875 B · 시안 페이지 오류 0)
1. `g3BangNodes()` — 블록 줄 범위(T: = 블록 첫 줄 ~ 다음 들임 0 줄/br 앞 · U: = g3SecHit .all · 둘 다 옛 그대로)를 구한 뒤, 근거에 `g.sl`(개념 창 줄 고르기 g3SelWire 가 넣는 그 줄 data-bx 글 · 그림은 'G:이름')이 있으면 그 줄만 Set 에 넣음 · 찾는 차례 = 범위 안 같은 글 → 절 안 같은 글 → 번호 표시 · 괄호 · 꺾쇠 · 빈칸 뺀 글이 같은 줄(볼트 통짜를 고쳐 글이 조금 바뀜 줄 · 예 「(3) 등압팽창」 → 「(3)(P)등압팽창」) · `g.sl` 이 없으면 옛 그대로 범위 전부.

## 점검표(채팅)
1. 일꾼 = 클라우드 · 2. 한 판 · 3. 회귀 = 없음(작은 고침) · 4. 선례 = g3SelWire(개념 창 고른 줄 = data-bx 글 · 'on' 칠하기) · thbang(16a9fd6 · g3BangNodes 범위 길) · 5. 저장 칸 무변 · 6. 근거 = 사용자 10/18 01:09 「물리앱에서 pa2109 봐봐. 한 줄만 ! 했는데, 통짜목차 파일 보면 그 절 전부다에 빨간세로줄 가 있어」(잼: 고른 줄 한 줄짜리 U: 근거 하나가 3.2.5 에 붉은 줄 15 줄) · 10. 더 빨리 = 공용 관문 + 시안 명세 · 13. inbox.
