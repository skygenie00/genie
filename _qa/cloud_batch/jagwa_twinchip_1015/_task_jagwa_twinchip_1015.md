# _task_jagwa_twinchip_1015 — 자과 물리: 쌍둥이도 서랍 작은 창 · 문제 창 🔗 칩에 [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(물리): 쌍둥이(TW · 연결 LK 와 따로 저장)가 ① 서랍 O△X 작은 창 머리(🔗N · ↩N 옆)에 「쌍N」(첫 화면 쌍 칩 색 #A65B12) · 누르면 연결과 같은 목록(줄 누름 = 그 문항) ② 문제 창 머리 🔗 칩에 「🔗 N · 쌍 M」(누르면 지금처럼 연결 · 쌍둥이 탭 창) · 쌍둥이 잇기 · 끊기 뒤 칩 수 다시. 저장 칸 무변.

- 판 크기 = 작음(앱 패치 5 · 짤 것 0)
- 로컬 필요 = 0
- 시간 = ≈6 분(선례 = jagwa_gscroll_1015 착수 → push 5 분 · 관문 4 칸)

## 할 일(차례대로 · 이것만)
1. `git fetch origin main cloud/inbox` · 바탕 = main **f8df32f**(`jagwa/index.html` LF md5 **f891a510** · `_qa/_qa_small_gate.py` md5 **867625c3**) — 다르면 멈추고 커밋 없이 이 줄만 알림.
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_twinchip_1015/` 에서 둘을 꺼냄: `app_patches.txt`(md5 f2195ffe) · `spec_twin.json`(c5dd6e85).
3. `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect b2ead861` — 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문: `python _qa/_qa_small_gate.py --spec spec_twin.json --new jagwa/index.html --base f8df32f --eng chromium,webkit --base-eng chromium`(`--vendor` · `--spd` · `--notes` 는 지난 판과 같이).
   - 명세 = 채팅 시안(PC · 폰 4 칸) 그대로 · setup 이 115 ↔ 116 쌍둥이를 이음(앱 twinLink · 관문 가짜 원격이라 사용자 기록 무변) · 바탕 f8df32f = 4 칸 다 FAIL(`yard: true`) — 시안 거울로 새 4/4 PASS · 바탕 4 FAIL 잼.
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(통째 다시 금지). 앱 결함이면 고치지 말고 칸 이름 · 값만 알림.
5. 회귀 사슬 · grep 회귀 안 돌림(작은 고침).
6. 커밋 하나(`jagwa/index.html`) · main 이 바탕 그대로면 fast-forward push · 커밋 글 = 관문 결과 줄 그대로(PASS/FAIL · 엔진 · 바탕) · 앱 md5 · 단계별 분.
- 지킬 것: 공개 저장소 — 시험 글은 명세 안 글뿐 · 사용자 기록 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(파일은 채팅이 검수 뒤 지움 · 가지는 그대로 · 가지 지울 일 없음). `jagwa/theory_fix.json` 은 건드리지 않음.
- 사용자 할 일 = 앱 새로고침 한 번.

## 패치가 하는 일(5 쌍 · 채팅이 f891a510 에 넣어 b2ead861 · 1,600,907 B · 인라인 스크립트 문법 오류 0 잼)
1. `g3PopTop` — `tw = twinsOf(no)`(있는 문항만) · 그림 · 연결 · 쌍둥이 다 없을 때만 머리 줄 안 그림.
2. 같은 함수 — ↩N 뒤에 `<button class="g3lk t" data-n="…">쌍N</button>`(누름 = 있던 .g3lk 목록 길 그대로).
3. `linkChip` — 칩 글 = 「🔗 N」 + (쌍둥이 있으면 「 · 쌍 M」) · on = 둘 중 하나라도.
4. `twinLink` 끝 — `linkChip()`.
5. CSS `#g3Pop .g3lk.t{color:#A65B12}`(첫 화면 .tag.tw 색).

## 점검표(채팅)
1. 일꾼 = 클라우드 · 2. 한 판 · 3. 회귀 = 없음(작은 고침) · 4. 선례 = 10/7 사용자 「쌍둥이랑 연결 합쳐 링크 아이콘 하나 · 각각 잇게」(🔗 → 연결 · 쌍둥이 탭) · 첫 화면 줄 「쌍 코드」 칩(.tag.tw) · 작은 창 🔗N ↩N(10/11) · 5. 저장 칸 무변 · 6. 근거 = 사용자 10/15 14:34 「물리에서 문제 연결 링크는 작은 창이나 문제 창 줄에서 나타나는데 왜 쌍둥이 연결은 안 나타나」 · 코드 잼 = g3PopTop · linkChip 둘 다 LK(linksOf)만 셈 · TW(twinsOf) 안 봄 · 10. 더 빨리 = 공용 관문 + 시안 명세 · 13. inbox.
