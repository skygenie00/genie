# _task_gg_gk_1113 — 민법OX · 조판기 1차객: 근거를 낱개로 연결 + 다른 기기에서 고친 근거가 문제 화면에서 바로 바뀜 [클라우드 · 앱 둘 · main push 한 번]

**화면에서 달라지는 것**(사용자 11/13 19:45 「이 근거만 연결하고 싶은데 왜 위 근거도 같이 붙어 · 각각 되라고 말했던 것 같은데」 · 11/10 14:54 「↩N 각각으로」 · 11/13 20:14 「(다른 데서 근거를 고쳤는데) 아이패드 문제 창에서 연결 근거로 보고 있는 것이 바로 안 바뀌더라」 · 20:28 「민법앱이랑 조판기앱 지시서 써줘」 · 민법 시안 「근거 낱개로 연결」 v2 그대로)

**가. 민법OX**
1. 근거 칸에 낱말을 치면 뜨는 목록: 문항 줄 안의 근거가 **칸마다 따로** 눌린다 → 누른 그 근거 하나만 걸린다.
   - 문항 글 쪽(근거 칸 밖)을 누르면 그 줄에 보이는 근거만 걸린다 · 이미 건 근거 칸에만 「이미 넣음」.
   - 자판 ↑↓ = 근거 칸마다 · Enter = 고른 칸.
2. 연결 상자: 건 근거만 보인다. 근거 줄마다 ✕ = **그 근거만** 끊기(되묻는 창 「이 근거 하나만」).
   - 마지막 하나를 끊으면 그 문항 연결이 없어진다 · 따로 선 ✕ 줄은 보일 근거가 없을 때만.
3. ↩N 은 근거마다 따로 센다: 제 근거 칩 · 근거 하나만 건 연결 칩 · 누르면 그 근거를 건 문항 창(근거마다 따로 뜸).
4. 근거 점 칸 · 📋 정리 창도 건 근거만.
5. 다른 기기에서 고친 근거 · 연결을 동기화로 받으면, 문제 화면에 떠 있는 근거 줄 · 연결 상자가 그 자리에서 바뀐다.
   - 카드 · 고른 답은 그대로 · 적거나 고치는 중인 칸은 건너뛰고 다음 받기 때.
- 지금까지 건 연결은 그대로다(그 문항 근거 전부) — 필요 없는 근거는 ✕ 로 뺀다.
- 저장: 새 저장 키 0. `ox_q_reflinks[문항].gk = {대상 문항: [근거 k …]}` 칸이 더해질 뿐(없으면 옛 연결 = 전부).

**나. 조판기 1차객(특허 · 상표 · 디보)**
1. 근거 찾기 목록(이미 근거마다 한 줄) → 누른 **그 근거만** 걸린다 · 「이미 넣음」 도 근거마다.
2. 연결 상자: 건 근거만 · 근거 줄마다 ✕ = 그 근거만 끊기 · 연결 칩 숫자 = 건 근거 수.
3. 쓰는 수는 근거마다 따로(연결 상자 줄 · 찾기 줄 · 근거 하나만 건 칩) · 누르면 그 근거 기준 창.
4. 근거 점 칸 · 정리 창도 건 근거만.
5. 다른 기기에서 고친 근거 · 연결을 받으면 떠 있는 근거 줄 · 연결 상자가 그 자리에서 바뀐다(적는 중인 칸은 건너뜀).
6. 결함 하나 같이 고침: 받은 뒤에도 메모리에 든 근거 사본을 안 비워서, 받은 뒤 근거를 하나 고치면 옛 사본 통째가 다시 써져 받은 근거가 덮였다 → 받으면 비운다.
- 저장: 새 저장 키 0. 같은 통(`jopangi.ggref`)의 칸 `~gk|<건 지문>` = `['<대상 지문>|<근거 k>', …]`(값이 배열이라 옛 판 기기도 그대로 돈다).

- 판 크기 = 중간(앱 둘 · 패치 민법 36 + 조판기 23 쌍 · 새 파일 0 · 짤 것 0 · 관문 = `gg_gate.py`(지난 판 그대로 · 이 폴더에만) + 명세 둘)
- 로컬 필요 = 0
- 시간 = ≈30 분(선례 gg_shx_1113 세 앱 17:31 넘김 → 17:49 push · 이 판 관문 채팅 잼 = 민법 4.1 분 + 조판기 7.5 분)

## 할 일(차례대로 · 이것만)
0. WebKit 을 세운다(이 저장소 CLAUDE.md 「WebKit」 절). 잰 결과를 커밋 글 첫 줄에 적는다.
1. `git fetch origin main cloud/inbox` · 바탕 = main **c043762**(`minbeop/index.html` LF md5 **38c398b7** · `jo/index.html` **e5f73142** · `_qa/_qa_apply_patches.py` **b8887814**) — 다르면 멈추고 커밋 없이 이 줄만 알림(main 이 두 앱을 안 건드린 커밋만 앞섰으면 그대로 간다).
2. `cloud/inbox` 의 `_qa/cloud_batch/gg_gk_1113/` 에서 다섯을 꺼냄: `ox_patches.txt`(md5 86802ac2) · `jo_patches.txt`(md5 b13e8eff) · `spec_minbeop.json`(md5 5409ac3c) · `spec_jo.json`(md5 bcc84557) · `gg_gate.py`(md5 784c647f).
3. 패치:
   - `python _qa/_qa_apply_patches.py ox_patches.txt minbeop/index.html --expect 56e0b81a` → 1,306,232 B · 인라인 7 · 문법 0
   - `python _qa/_qa_apply_patches.py jo_patches.txt jo/index.html --expect 4c8d5847` → 1,832,196 B · 인라인 1 · 문법 0(둘 다 채팅이 잼)
   - 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문(저장소 뿌리에서 · 데이터 = `git clone --depth 1 https://github.com/zzikkaplan/studyplandata` · 받기만 · 쓰기 0 · 채팅 잼 = studyplandata e6f2bda):
   - 민법: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python gg_gate.py --spec spec_minbeop.json --new minbeop/index.html --base c043762 --spd <클론> --eng chromium,webkit --base-eng chromium`
     - 칸 30(문제 화면 PC 20 · 폰 5 · 근거 임자 문항 화면 PC 5) · 헛잣대(바탕 FAIL) 25 · 무변(바탕 PASS) 5. 채팅 잼: 새 판 크롬 30/30(64 초) · 웹킷 30/30(75 초) · 바탕 25 FAIL · 5 PASS(106 초) · 합계 FAIL 0.
     - 민법 앱 꼴은 cdn.tailwindcss.com 으로 선다. 그 주소가 막혀 「가로 안 넘침」 · 자리 칸만 FAIL 이면, gg_shx_1113 때처럼 관문 사본에만 Tailwind 를 넣어 다시 잰다. 앱 파일에는 넣지 않는다.
   - 조판기: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python gg_gate.py --spec spec_jo.json --new jo/index.html --base c043762 --spd <클론> --root jo --eng chromium,webkit --base-eng chromium`
     - **`--root jo` = 작업 폴더의 jo/(안에 data/ 가 있어야 함)** — 빈 폴더면 지문이 0 장이라 거의 다 FAIL.
     - 칸 49(특허 PC 14 · 특허 폰 15 · 상표 PC 10 · 디보 PC 10) · 헛잣대 45 · 무변 4. 채팅 잼: 새 판 크롬 49/49(121 초) · 웹킷 49/49(122 초) · 바탕 45 FAIL · 4 PASS(206 초) · 합계 FAIL 0.
   - 명세가 근거 · 연결을 **지어낸 글**로 넣고 잰다(문항 · 지문 ID 만 씀 · 기록 글 0). 저장 = 관문 가짜 200 · 원격 쓰기 0.
   - 되묻는 창(confirm)은 「취소」 로 답한다 → 「그대로」 를 재고, 「확인」 뒤 모습은 「(준비)」 칸이 끊는 함수를 불러서 잰다.
   - 「받은 뒤」 칸 = 그 화면에서 받는 함수(ghSha · ghRaw)만 잠깐 갈아 다른 기기에서 고친 것처럼 받게 한 뒤 잰다(끝나면 되돌림).
   - 누름 · 치기 = 진짜 누름 · 자판. FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(앞 칸 상태에 기대는 칸은 그 화면 첫 칸부터). 앱 결함이면 고치지 말고 칸 이름과 값만 알림.
5. 회귀: 채팅이 지난 판 명세 넷을 새 앱에 미리 돌렸다 — 민법 gg_shx_1113(24 칸) 크롬 · 웹킷 48 PASS · minbeop_ink3_1112(30 칸) 60 PASS · 조판기 gg_shx_1113(32 칸) 64 PASS · jo_gg_1112(49 칸) 98 PASS · FAIL 0. 클라우드는 회귀 사슬 · grep 회귀 안 돌림.
6. 커밋 하나(`minbeop/index.html` · `jo/index.html`)를 만들고 **genie main 에 fast-forward push**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님).
   - 커밋 글 = WebKit 줄 · 관문 합계 줄 둘 · 앱 md5 둘 · 단계별 분.
   - push 가 막히면 지정 가지에 올리고 그 사실만 알림.
- 지킬 것: 공개 저장소 — 커밋 글에 기록 값 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(채팅이 검수 뒤 걷음). 명세 · gg_gate.py 를 main 에 넣지 않음.
- 사용자 할 일 = 모든 기기에서 민법OX · 조판기 새로고침 한 번.

## 패치가 하는 일
- 민법(36 쌍 · 38c398b7 → 56e0b81a)
  - 1 · 2. 저장: `refGk` · `refGkSet` · `ggOfL`(건 근거만) · `refPut` 이 남는 대상의 `gk` 칸을 지킴.
  - 3~6. 쓰임 수: `useOwnersG`(그 근거 하나를 건 문항 · 옛 연결은 같이 셈) · `useNumHTML` · `useLabelHTML(…, gk)` · 제 근거 칩.
  - 7~11 · 15. 쓰인 곳 창 `useWin(…, gk)`(머리 = 그 근거 글만 · 창 열쇠에 근거 k) · `useUnlink(…, gk)`.
  - 12~14. `useNumRepaint`: 넷째 인자 · 칩마다 제 근거 수 · 근거 기준 창도 갈음.
  - 16~20. 연결 칩 · `ggRefBoxHTML` · `ggRefRowHTML`: 건 근거만 · 줄마다 ✕(`data-ggrefx`).
  - 21~23. `ggRefAdd(…, gk)` · `addRefId(…, gk)`.
  - 24. `ggRefDelAsk` · `ggRefDel(…, gk)`: 남는 근거가 있으면 그 근거만 뺌(옛 연결 = 전부 → 나머지 낱개).
  - 25 · 26. 점 칸 `ggJmBox` · 정리 창 `jnGgHTML`.
  - 27~30. `ggPickSegs` + `linkSearch` 결과 줄: 근거 칸 `.ggseg[data-ggseg]` · 줄 머리 = 보이는 근거들.
  - 31~33. `ggLiveMove`(근거 칸마다) · Enter = `.ggsel` · CSS.
  - 34~36. `REC_GT`(받은 근거 · 연결 칸) · `syncRecords` 끝에서 첫 화면이 아니면 `recGgRepaint`.
- 조판기(23 쌍 · e5f73142 → 4c8d5847)
  - 1. 저장: `ggGkCell` · `ggRefGk` · `ggRefGkSet` · `ggOfL` · `ggOwnersG` · `ggRefAdd(…, gk)` · `ggRefDel(…, gk)`.
  - 2~7. `ggUseEl(…, gk)` · `ggUseWin(…, gk)`.
  - 8~10. 연결 칩(건 근거 수 · 쓰는 수).
  - 11 · 12. 점 칸 · 정리 창.
  - 13~16. `ggRefBox`: 건 근거만 · 줄마다 ✕(`data-ggrefx`).
  - 17 · 18. `ggFindRun`: 줄 `data-ggseg` · 누른 근거만 · 「이미 넣음」 근거마다.
  - 19~21. `REC_GT` · `syncRecords` 끝 `recGgRepaint` · `ggHostBusy`.
  - 22. `ggRepaint` 가 받은 뒤 갈음 때 적는 중인 칸을 건너뜀.
  - 23. `recDropCache` 에 `GGREC` · `GRREC` 비우기.

## 점검표(채팅)
1. **일꾼** = 클라우드(앱 파일 둘). 2. **차례** = 한 판 · 「~뒤」 없음. 3. **회귀** = 채팅이 미리 돌림(위 5).
4. **선례** = 민법 11/03 `useNumRepaint`(연결 숫자 그 자리 갈음) · `ggRefPaintOthers` · 11/10 근거 찾기 줄 꼴(ggPickLine) · 치는 대로 찾기(ggLiveMove) 위에 얹음 / 조판기 jo_gg_1112 `ggRefBox` · `ggFindRun` · `ggRepaint` 그대로 씀 · 자과 지학은 처음부터 근거 블록 단위 연결.
5. **저장 칸** = 민법 `ox_q_reflinks[문항].gk` · 조판기 `jopangi.ggref` 의 `~gk|…` 칸 · 새 키 0 · SYNC_KEYS 무변 · 옛 판 기기가 그 문항 연결을 고치면 낱개 표시가 빠져 다시 전부로 보임(→ 모든 기기 새로고침).
6. **근거** = 첫 줄 사용자 말. 7. **화면 끝** = 첫 줄 · 사용자 할 일.
8. **자료** = 민법 시안 69gRrkqYpe1Pxjzm62FD6T v2 · 설정 정본 N: `_tools\art_app\snap_minbeop_reflink_gk_1113.json` · 조판기는 시안 없이 민법 꼴대로(사용자 20:28 지시서 바로).
9. **클라우드** = 관문 + 헛잣대만. 10. **더 빨리** = 채팅이 관문 두 엔진 + 바탕 + 지난 판 회귀를 미리 돌림 · 두 앱 한 판 · push 한 번.
11. **2 시간 한도** = 관문 둘 합 ≈11.6 분. 12. **전수** = 화면마다 잼(민법 PC 둘 · 폰 / 조판기 특허 PC · 폰 · 상표 PC · 디보 PC).
13. **inbox** = 고정 가지. 14. **세 줄** = 사용자에게 먼저 보냄.
15. **과목 · 법** = 민법 한 앱 · 조판기는 1차객 세 법 같은 함수 · 자과(지학 · 생물 · 물리)는 해당 없음(지학식 근거는 처음부터 근거 단위).
- 시안과 다른 점: 앱 주석 한 줄에서 사용자 말 속 근거 제목 글을 뺌(공개 저장소) · 시안 전용이던 「✕ 되묻지 않고 바로」 는 안 넣음(실제 앱은 되묻는 창 그대로).
- 못 잰 것: 아이패드 진짜 손가락 톡 · 화면 키보드 · 되묻는 창 「확인」 누름(함수로만 잼) · 진짜 두 기기 사이 받기(그 화면에서 받는 함수만 갈아 잼).
