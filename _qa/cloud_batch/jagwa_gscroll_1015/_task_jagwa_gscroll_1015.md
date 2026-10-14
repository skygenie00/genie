# _task_jagwa_gscroll_1015 — 자과 물리: 긴 근거 손가락 · 휠로 굴림(서랍 작은 창 · 문제 창) [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(물리): ① 서랍 O△X 작은 창(#g3Pop)이 화면보다 길면 아래가 잘려 못 봄 → 화면 높이까지 · 넘치면 창 안에서 굴림(연결 창 #rlPop 과 같은 꼴). ② 문제 창 근거 칸(#ggphys)은 창 머리(.vtop · 끌기 손잡이 · touch-action none) 안이라 굴릴 칸이 없어, 근거가 길면 창 밖으로 넘쳐 잘리고 문제 칸이 0 으로 눌림 → 근거 칸 = 문항 창 높이의 45% 까지(최소 120px · 창 크기 바꾸면 따라감) · 넘치면 칸 안에서 손가락(touch-action pan-y) · 휠로 굴림. 머리 끌기는 근거 칸에서 이미 빠져 있음(data-nodrag · 무변).

- 판 크기 = 작음(앱 패치 4 · 짤 것 0)
- 로컬 필요 = 0
- 시간 = ≈6 분(선례 = jagwa_cqjoin_1014 착수 → push 5 분 · 관문 4 칸)

## 할 일(차례대로 · 이것만)
1. `git fetch origin main cloud/inbox` · 바탕 = main **b1de652**(`jagwa/index.html` LF md5 **1cfa31d7** · `_qa/_qa_small_gate.py` md5 **867625c3**) — 다르면 멈추고 커밋 없이 이 줄만 알림.
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_gscroll_1015/` 에서 둘을 꺼냄: `app_patches.txt`(md5 d219ee4d) · `spec_gscroll.json`(1a53221c).
3. `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect f891a510` — 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문: `python _qa/_qa_small_gate.py --spec spec_gscroll.json --new jagwa/index.html --base b1de652 --eng chromium,webkit --base-eng chromium`(`--vendor` · `--spd` · `--notes` 는 지난 판과 같이).
   - 명세 = 채팅 시안(PC · 폰 4 칸) 그대로 · 근거 글은 setup 이 넣는 지어낸 글(P115 에 30 줄) · 바탕 b1de652 = 4 칸 다 FAIL(`yard: true`) — 시안 거울로 새 4/4 PASS · 바탕 4 FAIL 잼.
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(통째 다시 금지). 앱 결함이면 고치지 말고 칸 이름 · 값만 알림.
5. 회귀 사슬 · grep 회귀 안 돌림(작은 고침).
6. 커밋 하나(`jagwa/index.html`) · main 이 바탕 그대로면 fast-forward push · 커밋 글 = 관문 결과 줄 그대로(PASS/FAIL · 엔진 · 바탕) · 앱 md5 · 단계별 분.
- 지킬 것: 공개 저장소 — 시험 글은 명세 안 글뿐 · 사용자 기록 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(파일은 채팅이 검수 뒤 지움 · 가지는 그대로 · 가지 지울 일 없음). `jagwa/theory_fix.json` 은 건드리지 않음.
- 사용자 할 일 = 앱 새로고침 한 번.

## 패치가 하는 일(4 쌍 · 채팅이 1cfa31d7 에 넣어 f891a510 · 1,600,089 B · 인라인 스크립트 문법 오류 0 잼)
1. `#g3Pop` CSS 에 `max-height:calc(100vh - 16px);overflow-y:auto;overscroll-behavior:contain`(#rlPop 과 같은 꼴 · 자리 잡기 코드는 offsetHeight 를 쓰므로 그대로 화면 안).
2. `#view .vtop>#ggphys` CSS 에 `max-height:45vh;overflow-y:auto;overscroll-behavior:contain;touch-action:pan-y`(45vh = 아래 3 이 못 돌 때 기본값).
3. 근거 칸을 머리에 붙인 뒤 `ggphysFit()` + `#view` ResizeObserver 한 번(창 크기 바꾸면 따라감).
4. `ggphysFit()` = 근거 칸 max-height = max(120, 문항 창 clientHeight × 0.45)px(머리 안에 있을 때만).

## 점검표(채팅)
1. 일꾼 = 클라우드 · 2. 한 판 · 3. 회귀 = 없음(작은 고침) · 4. 선례 = 연결 창 #rlPop(max-height calc(100vh - 16px) · overflow auto) · 근거 칸 data-nodrag(physphone A-5) 그대로 · 5. 저장 칸 무변 · 6. 근거 = 사용자 10/15 01:30 「근거들이 길 때 작은 창에서도 문제 창에서도 손으로 위로 올릴 수 없어?」 · 실제 앱(b1de652 · 내장 브라우저 · 떠 있는 창 612×696) P115 = 머리 701px > 창 498px · 근거 칸 overflow visible · 문제 칸 0 잼 · 작은 창 = 시안 거울 1133px > 화면 800 · overflow visible 잼 · 10. 더 빨리 = 공용 관문 + 시안 명세 · 13. inbox · 진짜 손가락 굴림은 관문 밖(사용자 기기에서 확인).
