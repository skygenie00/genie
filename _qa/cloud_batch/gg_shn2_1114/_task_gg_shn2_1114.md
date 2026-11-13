# _task_gg_shn2_1114 — 민법OX · 조판기 1차객: 「+」 로 붙은 ID 2 개 이상이면 숫자 · 작은 ID 목록 창 + 연결 상자에서 임자가 단 댓글에도 ID [클라우드 · 앱 둘 · main push 한 번]

(gg_shn_1114 를 갈음한다 — 그 폴더는 걷었다. 이 판만 한다.)

**화면에서 달라지는 것**(사용자 11/14 01:32 「댓글에 + 로 달리는 uid 가 가로로 너무 늘어난다 · 2 개 이상이면 uid 갯수 숫자로 · 그 숫자 누르면 uid 리스트 팝업창이 작게 · 심플하게」 · 01:43 「지시서 써줘 · 조판기 1차객도 포함해서」 · 02:17 「지문 댓글에 uid 가 안 붙어 있는데 왜 이런 거야」 · 민법 시안 「같이 쓰는 ID 숫자로」 v2 그대로)

**가. 민법OX**(제 근거 판 · 연결해 온 근거 상자의 댓글 줄 — 같은 함수)
1. 댓글 줄 오른쪽 칸: 「+」 로 붙은 문항 ID 가 **2 개 이상이면 숫자 하나**(파란 둥근 칸)로 보인다. 1 개면 지금처럼 ID 그대로.
   - 세는 것 = 지문 · 글을 안 붙인 ID. 지문을 붙인 ID 는 지금처럼 제 줄에 보인다.
   - 댓글을 단 문항 ID(맨 앞) · 날짜 · 「+ / −」 · ✕ 는 그대로.
2. 숫자를 누르면 그 밑(자리가 없으면 위)에 작은 ID 목록 창이 뜬다(높이 화면 1/3 안 · ID 한 줄씩).
   - 목록의 ID 를 누르면 그 문제가 뜨고 목록은 닫힌다(지금 ID 누름과 같음).
   - 목록의 ID 를 길게 누르면 지문 · 글 붙이기 칸이 그 댓글 줄 밑에 뜬다(지금 길게 누름과 같음).
   - 같은 숫자 다시 누름 · 목록 밖 누름 · Esc · 굴림 = 닫힘.
3. **연결 상자**에서 근거 임자 문항이 스스로 단 댓글 줄: 지금은 임자 문항 지문만 뜨고 ID 가 없다 → 그 문항 ID 도 맨 앞에 보인다(누르면 그 문제). 제 근거 판은 그대로(ID 없음).

**나. 조판기 1차객(특허 · 상표 · 디보)** — 같은 꼴(같이 쓰는 지문 ID 2 개 이상 → 숫자 · 목록 창 · ID 누름 = 그 지문 · 길게 누름 = 지문 · 글 붙이기 / 연결 상자에서 임자 지문이 스스로 단 댓글에도 그 지문 ID).

- 저장 꼴은 그대로다(그리기만 바뀜 · 새 저장 키 0).
- 판 크기 = 작음(앱 둘 · 패치 민법 6 + 조판기 6 쌍 · 새 파일 0 · 짤 것 0 · 관문 = `gg_gate.py`(지난 판 그대로 · 이 폴더에만) + 명세 둘)
- 로컬 필요 = 0
- 시간 = ≈18 분(선례 gg_ownsh_1113 두 앱 22:43 넘김 → 22:55 push = 12 분 · 이 판 관문 채팅 잼 = 민법 4.8 분 + 조판기 8.1 분)

## 할 일(차례대로 · 이것만)
0. WebKit 을 세운다(이 저장소 CLAUDE.md 「WebKit」 절). 잰 결과를 커밋 글 첫 줄에 적는다.
1. `git fetch origin main cloud/inbox` · 바탕 = main **b33be58**(`minbeop/index.html` LF md5 **33725c42** · `jo/index.html` **1baf536b** · `_qa/_qa_apply_patches.py` **b8887814**) — 다르면 멈추고 커밋 없이 이 줄만 알림(main 이 두 앱을 안 건드린 커밋만 앞섰으면 그대로 간다).
2. `cloud/inbox` 의 `_qa/cloud_batch/gg_shn2_1114/` 에서 다섯을 꺼냄: `ox_patches.txt`(md5 e6c3bc37) · `jo_patches.txt`(md5 4d60677e) · `spec_minbeop.json`(md5 44202213) · `spec_jo.json`(md5 6ce1838f) · `gg_gate.py`(md5 784c647f).
3. 패치:
   - `python _qa/_qa_apply_patches.py ox_patches.txt minbeop/index.html --expect 83e5422d` → 1,312,310 B · 문법 0
   - `python _qa/_qa_apply_patches.py jo_patches.txt jo/index.html --expect 5e492e79` → 1,836,359 B · 문법 0(둘 다 채팅이 잼)
   - 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문(저장소 뿌리에서 · 데이터 = `git clone --depth 1 https://github.com/zzikkaplan/studyplandata` · 받기만 · 쓰기 0):
   - 민법: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python gg_gate.py --spec spec_minbeop.json --new minbeop/index.html --base b33be58 --spd <클론> --eng chromium,webkit --base-eng chromium`
     - 칸 29(임자 문항 화면 PC 13 · 폰 11 · 같이 쓰는 문항 화면 PC 5) · 헛잣대(바탕 FAIL) 24 · 무변(바탕 PASS) 5. 채팅 잼: 새 판 chromium 29/29(51 초) · webkit 29/29(55 초) · 바탕 24 FAIL + 5 PASS(185 초) · 합계 FAIL 0.
     - 민법 앱 꼴은 cdn.tailwindcss.com 으로 선다. 그 주소가 막혀 「가로 안 넘침」 · 자리 칸만 FAIL 이면 관문 사본에만 Tailwind 를 넣어 다시 잰다. 앱 파일에는 넣지 않는다.
   - 조판기: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python gg_gate.py --spec spec_jo.json --new jo/index.html --base b33be58 --spd <클론> --root jo --eng chromium,webkit --base-eng chromium`
     - **`--root jo` = 작업 폴더의 jo/(안에 data/ 가 있어야 함)** — 빈 폴더면 지문이 0 장이라 거의 다 FAIL.
     - 칸 44(특허 PC 11 · 특허 폰 11 · 상표 PC 11 · 디보 PC 11) · 헛잣대 36 · 무변 8. 채팅 잼: 새 판 chromium 44/44(96 초) · webkit 44/44(97 초) · 바탕 36 FAIL + 8 PASS(294 초) · 합계 FAIL 0.
   - 명세가 근거 · 댓글 · 같이 쓰는 ID 를 **지어낸 글**로 넣고 잰다(문항 · 지문 ID 만 씀 · 기록 글 0). 저장 = 관문 가짜 200 · 원격 쓰기 0.
   - 누름 · 길게 누름 · 치기 = 진짜 누름 · 자판(조판기 「연결 상자 임자 ID 누름」 한 칸만 화면을 안 옮기려고 요소 click() 으로 잼). FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(앞 칸 상태에 기대는 칸은 그 화면 첫 칸부터). 앱 결함이면 고치지 말고 칸 이름과 값만 알림.
5. 회귀: 채팅이 지난 판 명세 일곱을 새 앱에 미리 돌렸다(새 판만 · 두 엔진 · FAIL 0) — 민법 gg_ownsh_1113 · gg_gk_1113 · gg_shx_1113 / 조판기 gg_ownsh_1113 · gg_gk_1113 · gg_shx_1113 · jo_gg_1112. 클라우드는 회귀 사슬 · grep 회귀 안 돌림.
6. 커밋 하나(`minbeop/index.html` · `jo/index.html`)를 만들고 **genie main 에 fast-forward push**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님).
   - 커밋 글 = WebKit 줄 · 관문 합계 줄 둘 · 앱 md5 둘 · 단계별 분.
   - push 가 막히면 지정 가지에 올리고 그 사실만 알림.
- 지킬 것: 공개 저장소 — 커밋 글에 기록 값 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(채팅이 검수 뒤 걷음). 명세 · gg_gate.py 를 main 에 넣지 않음.
- 사용자 할 일 = 모든 기기에서 민법OX · 조판기 새로고침 한 번.

## 패치가 하는 일
- 민법(6 쌍 · 33725c42 → 83e5422d)
  - 1. 새 함수 `ggShIdsHTML(c)`(안 붙인 같이 쓰는 ID 가 2 개 이상이면 숫자 `.ggshn` + 숨겨 둔 원래 ID 들 `.ggshhold` · 아니면 지금 ID 그대로) · `ggShnTog` · `ggShnClose`(목록 창 `.ggshpop` = body 에 fixed) · `ggShnSrc`(목록 안 ID → 그 댓글 줄의 원래 ID) · 꾸밈 · 닫는 손잡이(밖 누름 · Esc · 굴림 · 창 크기).
  - 2. `ggCsHTML` 오른쪽 칸의 같이 쓰는 ID 들 → `ggShIdsHTML(c)`.
  - 3. `ggShxHTML` 자리 채움 — 숫자 하나로 바뀐 폭에 맞춤.
  - 4 · 5. 길게 누름 손잡이: 목록 안 ID 면 원래 ID 로 이어 주고 · 붙이기 칸이 뜨면 목록은 닫힘.
  - 6. `ggCsHTML` 맨 앞 ID = `c.from` 이 없으면 연결 상자(del 아님)에서는 근거 임자 문항 ID — 지문 머리(`ggFromHead` = c.from 없으면 임자 지문)와 같은 조건.
- 조판기(6 쌍 · 1baf536b → 5e492e79)
  - 1. 꾸밈(`.ggshn` · `.ggshpop`).
  - 2 · 3. `ggCsRow`: 안 붙인 ID 단추를 모아 2 개 이상이면 숫자 단추 하나(누르면 `ggShnTog(nb, 단추들)`) · 아니면 지금처럼 오른쪽 칸에.
  - 4. `ggShnTog` · `ggShnClose`(목록 창에 **진짜 ID 단추를 옮겨 담음** — 누름 · 길게 누름이 그대로) · 닫는 손잡이 · `ggShxBox` 가 뜨면 목록 닫힘.
  - 5 · 6. `ggCsRow`: 연결 상자(me ≠ owner)에서 임자 지문이 스스로 단 댓글에도 임자 지문 ID 단추 · 붙은 줄 자리 채움이 그 ID 를 맨 앞 ID 로 침.

## 점검표(채팅)
1. **일꾼** = 클라우드(앱 파일 둘). 2. **차례** = 한 판 · 「~뒤」 없음. 3. **회귀** = 채팅이 미리 돌림(위 5).
4. **선례** = 민법 11/05 같이 쓰는 ID 칩 · 11/10 `ggFromHead`(지문 머리) · 11/13 `ggShxBox` · `ggCsOwnSh` 위에 얹음 — 자리 전수: 같이 쓰는 ID · 단 문항 ID 를 그리는 곳 = 민법 `ggCsHTML` 한 곳(제 근거 판 · 연결 상자 같이 씀) + `ggShxHTML`(붙은 줄 · 자리 채움) / 조판기 `ggCsRow` 한 곳.
5. **저장 칸** = 무변(그리기만) · SYNC_KEYS 무변 · 옛 판 기기와 섞여도 같음.
6. **근거** = 첫 줄 사용자 말. 7. **화면 끝** = 첫 줄 · 사용자 할 일.
8. **자료** = 민법 시안 YSPuqP3BkbwLHHfHkywLWB v2 · 설정 정본 N: `_tools\art_app\snap_minbeop_shn_1114.json` · 조판기는 시안 없이 민법 꼴대로(사용자 01:43 · 1차객은 민법과 같게).
9. **클라우드** = 관문 + 헛잣대만. 10. **더 빨리** = 채팅이 관문 두 엔진 + 바탕 + 지난 판 회귀를 미리 돌림 · 두 앱 한 판 · push 한 번.
11. **2 시간 한도** = 관문 둘 합 ≈13 분. 12. **전수** = 화면마다 잼(민법 PC 둘 · 폰 / 조판기 특허 PC · 폰 · 상표 PC · 디보 PC).
13. **inbox** = 고정 가지. 14. **세 줄** = 사용자에게 먼저 보냄.
15. **과목 · 법** = 민법 한 앱 · 조판기는 1차객 세 법 같은 함수 · 자과는 해당 없음(사용자 말 = 민법 · 조판기 1차객).
- 시안과 다른 점: 없음(시안 패치 6 쌍 그대로) · 관문 명세만 기록 글 대신 지어낸 근거 · 댓글로.
- 못 잰 것: 아이패드 진짜 손가락 톡 · 길게 누름 · 화면 키보드.
