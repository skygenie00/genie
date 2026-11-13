# _task_gg_shx_1113 — 자과(지학 · 생물) · 민법OX · 조판기 1차객: 댓글에 지문 · 글 붙이기 + 민법 풀이 창 △ [클라우드 · 앱 셋 · main push 한 번]

**화면에서 달라지는 것**(사용자 11/13 13:25 「댓글에 + → 지금 문항 지문 붙이기」 · 13:37 「+ 누른 댓글에 속한 것으로 · 합쳐진 형식」 · 13:46 「uid 오른쪽 · 원래 댓글 uid 밑에 정렬」 · 13:58 「📖 p쪽 단추 지우고 목차 서랍 앞 번호」 · 14:24 「민법: + 로 들어간 uid 를 길게 누르면 지문 · 추가 댓글 / 풀이 창 헷갈림 태그 왼쪽에 표시」 · 14:48 「세모만」 · 15:07 「생물에도 · 조판기 1차객 특상디에도」 · 16:37 「지시서 써줘」 · 시안 셋 그대로)

**가. 자과 서재 — 지학 · 생물(카드 층 · 물리 무변)**
1. 근거 댓글 줄마다 오른쪽 문항 ID 밑에 「+」. 톡 → 그 줄 바로 밑에 지금 보는 문항의 지문 목록 + 적는 칸.
2. 지문을 고르고 Enter(글은 비워도 됨) → 새 댓글 줄이 아니라 **그 댓글 안에 합쳐진 줄**: 「지문」 · O/X · 쓴 글 · 붙인 문항 ID · ✕. 그 지문 점이 「댓」.
   - 자리: 글은 댓글 글 바로 밑 · 붙인 문항 ID 는 원래 댓글 ID 바로 밑(오른쪽 끝 맞춤) · ✕ 는 댓글 ✕ 밑 · 「+」 는 ID 들 맨 밑.
3. 이미 붙인 지문을 다시 고르면 적는 칸에 쓴 글이 들어와 고침 · 붙인 지문 톡 → O/X 고르개(그 줄에만) · ✕ → 그 줄만 뺌.
4. 붙은 줄을 길게 누르면 그 줄 고치기 칸이 열린다(댓글 글 고치기 칸은 안 열림 · 붙인 문항이 지금 문항일 때).
5. 지문 점 칸 · 서랍 작은 창 · 📋 정리 창 · 검색 줄에도 붙인 줄이 같이 보인다(그 문항 줄에 「붙인 지문」 + 그 댓글 글 + 붙여 쓴 글).
6. 📋 정리 창 문항 줄 머리 = 「📖 p쪽」 단추 대신 목차 서랍 앞 번호(굵게) + 문항 ID. 교재 쪽 칩은 문항 창에 그대로.
- 저장: 새 저장 키 0. 댓글에 `sh=[{u: 붙인 문항, jm, jt, jo?, t?, ts}]` 칸이 더해질 뿐(옛 기록 그대로 읽힘).

**나. 민법OX**
1. 연결 상자 남의 댓글 「+」 = 지금처럼 오른쪽 칸에 이 문항 ID 만 들어간다. 그 **ID 를 길게 누르면(0.55 초)** 그 줄 밑에 그 문항 지문 + 적는 칸.
2. Enter → 그 댓글 줄 안 밑 한 줄: 「지문」 · O/X · 쓴 글 · ID(원래 댓글 ID 밑 · 오른쪽 끝). 글 없이 Enter = 지문만.
3. 붙은 지문 톡 → O/X 고르개 · 붙은 줄 길게 누름 → 그 줄 고치기(댓글 글 고치기 칸은 안 열림).
4. 「−」(같이 쓰기 그만): 붙여 쓴 글이 있으면 되묻는 창(「붙여 쓴 글도 지워진다」) → 「같이 쓰기 그만」 을 눌러야 빠짐 · 지문만 붙였으면 바로 빠짐.
5. 📋 정리 창 근거 줄: 같이 쓰는 댓글에 붙여 쓴 글도 같이 보임.
6. 문제 풀이 창: 헷갈림 태그 **바로 왼쪽에 △**(OMR 표시가 있는 문항만 · 눌러도 아무 일 없음 · 📍 단추는 그 앞).
   - 표시 값은 이 판 인도 뒤 채팅이 앱 저장 길로 넣는다(이 판은 보이는 자리 · 저장 칸만).
- 저장: 댓글에 `shx={문항 ID: {t?, jo?}}` 칸(`sh` 는 그대로 문항 ID 배열) · 새 저장 키 하나 `ox_q_omr`({문항 ID: 't'} · SYNC_KEYS 끝에 더함).

**다. 조판기 1차객(특허 · 상표 · 디보)**
1. 나-1~5 와 같은 기능(연결 상자 다른 지문 댓글 「+」 → ID 길게 누름 → 그 지문 + 글 → 댓글 줄 안 밑 한 줄 · 지문 톡 O/X · 붙은 줄 길게 눌러 고침 · 정리 창 근거 칸).
2. 「−」: 붙여 쓴 글이 있으면 되묻는 창(confirm) · 지문만 붙였으면 바로 빠짐.
- 저장: 새 저장 키 0. 댓글에 `shx` 칸.

- 판 크기 = 중간(앱 셋 · 패치 자과 16 + 민법 15 + 조판기 6 쌍 · 새 파일 0 · 짤 것 0 · 관문 = 민법 · 조판기 `gg_gate.py`(지난 판 그대로 · 이 폴더에만) · 자과 공용 `_qa/_qa_small_gate.py` + 명세 셋)
- 로컬 필요 = 0
- 시간 = ≈35 분(선례 ggjigak_1110 두 앱 한 판 19:05 넘김 → 19:31 인도 · 이 판 관문 채팅 잼 = 자과 2.6 분 + 민법 3.2 분 + 조판기 6.5 분)

## 할 일(차례대로 · 이것만)
0. WebKit 을 세운다(이 저장소 CLAUDE.md 「WebKit」 절). 잰 결과를 커밋 글 첫 줄에 적는다.
1. `git fetch origin main cloud/inbox` · 바탕 = main **133b0bd**(`jagwa/index.html` LF md5 **da942595** · `minbeop/index.html` **c85c81ae** · `jo/index.html` **6f11ae88** · `_qa/_qa_apply_patches.py` **b8887814** · `_qa/_qa_small_gate.py` **867625c3**) — 다르면 멈추고 커밋 없이 이 줄만 알림(main 이 세 앱을 안 건드린 커밋만 앞섰으면 그대로 간다).
2. `cloud/inbox` 의 `_qa/cloud_batch/gg_shx_1113/` 에서 일곱을 꺼냄: `jagwa_patches.txt`(md5 1e1cbb6f) · `ox_patches.txt`(md5 39d11a26) · `jo_patches.txt`(md5 74ae57a4) · `spec_jagwa.json`(md5 04482fe0) · `spec_minbeop.json`(md5 5afcb27d) · `spec_jo.json`(md5 ca1e7188) · `gg_gate.py`(md5 784c647f).
3. 바탕을 떠 둠: `git show origin/main:jagwa/index.html > /tmp/base_jagwa.html`. 그다음
   - `python _qa/_qa_apply_patches.py jagwa_patches.txt jagwa/index.html --expect 61f69712` → 1,684,246 B · 인라인 5 · 문법 0
   - `python _qa/_qa_apply_patches.py ox_patches.txt minbeop/index.html --expect 38c398b7` → 1,295,727 B · 인라인 7 · 문법 0
   - `python _qa/_qa_apply_patches.py jo_patches.txt jo/index.html --expect e5f73142` → 1,827,519 B · 인라인 1 · 문법 0(셋 다 채팅이 잼)
   - 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문(저장소 뿌리에서 · 데이터 = `git clone --depth 1 https://github.com/zzikkaplan/studyplandata` · 받기만 · 쓰기 0 · 채팅 잼 = studyplandata 5cf3ee8):
   - 자과: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python _qa/_qa_small_gate.py --spec spec_jagwa.json --new jagwa/index.html --base /tmp/base_jagwa.html --spd <클론> --eng chromium,webkit --base-eng chromium`
     - 칸 38(지학 PC · 지학 폰 · 생물 PC) · 헛잣대(바탕 FAIL) 35 · 무변(바탕 PASS) 3. 채팅 잼: 새 판 크롬 38/38 · 웹킷 38/38 · 바탕 35 FAIL · 3 PASS · 합계 FAIL 0 · 2.6 분.
     - 생물은 기록에 근거가 없어 명세가 근거 · 댓글을 지어 넣고 잰다.
   - 민법: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python gg_gate.py --spec spec_minbeop.json --new minbeop/index.html --base 133b0bd --spd <클론> --eng chromium,webkit --base-eng chromium`
     - 칸 24(PC · 폰) · 헛잣대 22 · 무변 2. 채팅 잼: 새 판 크롬 24/24(42 초) · 웹킷 24/24(47 초) · 바탕 22 FAIL · 2 PASS(102 초) · 합계 FAIL 0.
     - △ 칸은 명세가 그 브라우저 저장 칸(`ox_q_omr`)에 문항 둘을 넣고 본다(지어낸 표시).
     - 민법 앱 꼴은 cdn.tailwindcss.com 으로 선다. 그 주소가 막혀 「가로 안 넘침」 · 자리 맞춤 칸만 FAIL 이면, 11/10 ggjigak 때처럼 관문 사본에만 Tailwind(npm @tailwindcss/browser)를 넣어 다시 잰다. 앱 파일에는 넣지 않는다.
   - 조판기: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python gg_gate.py --spec spec_jo.json --new jo/index.html --base 133b0bd --spd <클론> --root jo --eng chromium,webkit --base-eng chromium`
     - **`--root jo` = 작업 폴더의 jo/(안에 data/ 가 있어야 함)** — 빈 폴더면 지문이 0 장이라 거의 다 FAIL.
     - 칸 32(특허 PC · 특허 폰 · 상표 PC · 디보 PC) · 헛잣대 26 · 무변 6. 채팅 잼: 새 판 크롬 32/32(97 초) · 웹킷 32/32(99 초) · 바탕 26 FAIL · 6 PASS(196 초) · 합계 FAIL 0.
     - 되묻는 창(confirm)은 관문이 「취소」 로 답한다 → 「그대로」 를 잰다(「확인」 갈래는 안 잼).
   - 누름 = 진짜 누름(길게 누름 800ms 포함). 「(준비)」 · 「(정리)」 칸은 앱 함수를 불러 상태를 놓는다. 시험 글은 지어낸 글 · 저장 = 관문 가짜 200 · 원격 쓰기 0 · 기록 값 0.
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(앞 칸 상태에 기대는 칸은 그 화면 앞 칸부터). 앱 결함이면 고치지 말고 칸 이름과 값만 알림.
5. 회귀: 채팅이 지난 판 명세 셋을 새 앱에 미리 돌렸다 — 민법 minbeop_ink3_1112(30 칸) 크롬 · 웹킷 60 PASS · 조판기 jo_gg_1112(49 칸) 크롬 · 웹킷 98 PASS · 자과 ggjt_1110 자과 몫(6 칸) 크롬 · 웹킷 12 PASS · FAIL 0. 클라우드는 회귀 사슬 · grep 회귀 안 돌림.
6. 커밋 하나(`jagwa/index.html` · `minbeop/index.html` · `jo/index.html`)를 만들고 **genie main 에 fast-forward push**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님).
   - 커밋 글 = WebKit 줄 · 관문 합계 줄 셋 · 앱 md5 셋 · 단계별 분.
   - push 가 막히면 지정 가지에 올리고 그 사실만 알림.
- 지킬 것: 공개 저장소 — 커밋 글에 기록 값 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(채팅이 검수 뒤 걷음). 명세 · gg_gate.py 를 main 에 넣지 않음.
- 사용자 할 일 = 모든 기기에서 자과 서재 · 민법OX · 조판기 새로고침 한 번.

## 패치가 하는 일
- 자과(16 쌍 · da942595 → 61f69712 · 카드 층 댓글 줄 둘레)
  - 1 · 15. CSS: 카드 층 댓글 줄 `.ggcs.ggcsg` = 격자 여섯 칸(손잡이 · ! · 날짜 · 글 · 문항 ID · ✕) · 붙인 줄 `.ggsh`(display:contents) · 「+」 `.ggjp` · 정리 창 번호 `.jnno`.
  - 2~5. `ggCsHTML`: 줄에 `ggcsg` · 줄 수 `--gr` · ID 칸 밑 「+」 · 줄 끝에 붙인 줄(새 함수 `ggShHTML`).
  - 6~10. 붙인 줄을 같이 셈 · 보임: `jmHasCm`(지문 점 「댓」) · 점 칸 목록 · 작은 창 · 정리 창 댓글 · 검색 줄 · 검색 거르개.
  - 11 · 12. `g3JoSet(…, sh)`: 붙인 줄 O/X 는 그 줄에만.
  - 13. 새 함수 `g3ShBox`(지문 고르는 칸) · `g3ShSave` · `g3ShDel` · `jmDotsPaint` + 누름 · 길게 누름 묶음.
  - 14. `jnRowHTML` 줄 머리: 카드 층(HASBOOK)이면 「📖 p쪽」 단추 대신 `dispNo(no)`.
  - 16. 옛 길게 누름(댓글 글 그 자리 고치기)은 붙은 줄 위에서 건너뜀.
- 민법(15 쌍 · c85c81ae → 38c398b7)
  - 1~3. `ggCsHTML` 줄: 같이 쓰는 ID 칩에 `.ggshid[data-shu]` · 줄 끝에 붙은 줄(`ggShxHTML`).
  - 4 · 5. 새 함수 `ggShxHTML` · `ggShxSave` · `ggShxBox` + 길게 누름 묶음(550ms · 뒤따르는 톡은 먹음 · 손 뗄 때 커서 한 번 더) · CSS.
  - 6 · 7. `ggJoSet(guid,gk,ck,v,sh)`: 붙은 줄 O/X.
  - 8 · 9. `ggCsShare(…, go)`: 붙여 쓴 글이 있으면 되묻는 창(`oxWinOpen` · `button.ggshgo`) · 빼면 `shx` 그 칸도 지움.
  - 10. 옛 길게 누름 건너뛰기 목록에 `.ggshrow` · `.ggshxbox`.
  - 11. `jnGgHTML`: 같이 쓰는 댓글 줄에 붙여 쓴 글.
  - 12 · 13. 문제 카드 태그 줄 앞 `omrMarkHTML(id)` = `ox_q_omr[id]` 가 있으면 `<span class="omrmk">△</span>`.
  - 14. `SYNC_KEYS` 끝에 `ox_q_omr`.
  - 15. `injectPins`: 📍 단추를 표시 앞에 넣음(△ 가 헷갈림 바로 왼쪽에 남게).
- 조판기(6 쌍 · 6f11ae88 → e5f73142)
  - 1 · 2. `ggCsRow`: 같이 쓰는 ID 칩 길게 누름(`data-gglp`) → 새 함수 `ggShxBox` · 붙은 줄 `.ggshrow`.
  - 3. 「−」: 붙여 쓴 글이 있으면 confirm · 빼면 `shx` 그 칸도 지움.
  - 4. 옛 길게 누름 건너뛰기 목록.
  - 5. CSS(`.ggcs.ggcs2` 줄 꺾기 · 붙은 줄 자리).
  - 6. `jnGgBox` 근거 칸 줄에 붙여 쓴 글.

## 점검표(채팅)
1. **일꾼** = 클라우드(앱 파일 셋). 2. **차례** = 한 판 · 「~뒤」 없음. 3. **회귀** = 채팅이 미리 돌림(위 5).
4. **선례** = 자과 11/05 지문 점 → 댓글(`g3JmBox` · jm · jt · jo)과 같은 꼴 칸 · 민법 11/05 같이 쓰기(`ggCsShare` · sh) 위에 얹음 · 조판기 jo_gg_1112 `ggCsRow` · 길게 누름 묶음(`data-gglp`) 그대로 씀.
5. **저장 칸** = 자과 댓글 `sh[]` · 민법 · 조판기 댓글 `shx{}` · 민법 새 키 `ox_q_omr` 하나(SYNC_KEYS · 옛 판 기기는 모르는 키를 잠깐 떨굴 수 있음 → 값 넣기는 모든 기기 새로고침 뒤).
6. **근거** = 첫 줄 사용자 말. 7. **화면 끝** = 첫 줄 · 사용자 할 일.
8. **자료** = 시안 QPPJXvJfuRubDctMS7qfKt v6 · 6y83wV18RVUsHQtgrzBRie v2 · DJMHxGFh24P8iLi2GDgqsG v1 · 설정 정본 N: `_tools\art_app\snap_jagwa_jpadd_1113.json` · `snap_minbeop_shx_omr_1113.json` · `snap_jo_shx_1113.json`.
9. **클라우드** = 관문 + 헛잣대만. 10. **더 빨리** = 채팅이 관문 두 엔진 + 바탕 + 지난 판 회귀를 미리 돌림 · 세 앱을 한 판 · push 한 번.
11. **2 시간 한도** = 관문 셋 합 ≈12.3 분. 12. **전수** = 화면마다 잼(자과 지학 PC · 폰 · 생물 PC / 민법 PC · 폰 / 조판기 특허 PC · 폰 · 상표 PC · 디보 PC).
13. **inbox** = 고정 가지. 14. **세 줄** = 사용자에게 먼저 보냄.
15. **과목 · 법** = 자과는 카드 층(지학 · 생물) 같은 코드 · 물리는 댓글 줄 꼴 · 정리 창 줄 머리 무변(`gk!=null&&CARD_LAYER` · HASBOOK 일 때만) / 조판기는 1차객 세 법 같은 함수.
- 바탕 메모: 자과 시안은 300a7c0e 위에서 만들었고, 그 뒤 main 이 133b0bd(da942595 · 통짜 물리 번호 바꿈)로 가서 같은 16 쌍을 새 바탕에 다시 댔다(쌍마다 찾는 글 1 회 · 두 결과의 차이 = 그 번호 바꿈 줄뿐 · 관문은 새 바탕으로 다시 잼).
- 못 잰 것: 아이패드 진짜 손가락 · 펜 길게 누름 · 화면 키보드 — 인도 뒤 사용자 확인. 조판기 confirm 「확인」 갈래.
