# _task_jagwa_chv_1106 — 자과 지학 · 생물: 회독 창 「N회독」 = 그 회독 지문 · 〈보기〉 O△X · 고른 답이 카드에 보이고 고칠 수 있다 [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(자과 지학 · 생물 · 카드 층 문항 창 · 회독 기록 작은 창 `#hsPop`)
1. 회독 창에서 「N회독」(지난 회독)을 누르면 카드의 선택지 줄 O△X · 〈보기〉 O△X 에 그 회독에 체크한 값이 뜬다(지금은 필기만 바뀌고 O△X 는 지금 회독 빈 칸 그대로).
2. 그 회독에 고른 답(선택지 `pick` 테두리)도 뜬다 · 지난 회독을 보는 동안은 해설을 안 펴도 정답 테두리(`markAns` · `.ans`)와 〈보기〉 맞음 · 틀림 색(`markWrong` · 그 회독 O·X 대 정오)이 뜬다(사용자 22:11 「틀렸는데 그럼 정답은 뭔데 · 테두리 안 해?」).
3. 그 회독을 보는 동안 O△X 를 누르면 **그 회독 기록**이 고쳐진다(status `h[i].b` · 지금 회독 칸 `BG` 무변) · 서랍 △ 도 바로 따라감(`navSync`).
4. 지난 회독을 보다가 선택지를 고르면 → 카드 O△X 는 지금 회독 칸으로 돌아오고, 답은 옛처럼 지금 회독에 기록.
5. 카드를 다시 그리면(같은 문항을 다시 누름 · 새 열람) 지금 회독 보기로(필기도 `qLoad` 가 지금 회독으로 — 옛 그대로).
- 회독 창 꼴 · 「N회독」 줄이 보이는 규칙 · 마크 고치기 · ✕ · 지금 회독 O△X 저장(`BG` · `nrCarryMem` 옮김) · 물리 무변 · 저장 칸 새것 0.

- 판 크기 = 작음(앱 패치 7 쌍 · 새 파일 0 · 짤 것 0 · 관문 = 공용 `_qa_small_gate.py`)
- 로컬 필요 = 0
- 시간 = ≈5 분(선례 cmn_1106 「보냈어」 15:26 → main 15:29 · jmown 4 분 · 이 판 관문 크롬 · 웹킷 + 바탕 크롬 = 1.9 분)

## 할 일(차례대로 · 이것만)
0. WebKit 을 세운다(이 저장소 CLAUDE.md 「WebKit」 절). 잰 결과를 커밋 글 첫 줄에 적는다.
1. `git fetch origin main cloud/inbox` 로 바탕을 맞춘다.
   - 바탕 = origin/main(채팅이 잰 때 **da4ee42**).
   - 맞출 값: `jagwa/index.html` LF md5 **a9dcf1d5** · `_qa/_qa_apply_patches.py` **b8887814** · `_qa/_qa_small_gate.py` **867625c3**.
   - 다르면 멈추고 커밋 없이 이 줄만 알린다(main 이 jagwa 를 안 건드린 커밋만 앞섰으면 그대로 간다).
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_chv_1106/` 에서 둘을 꺼낸다: `app_patches.txt`(md5 0b931010) · `spec_chv.json`(md5 9ca169a6).
3. 바탕 앱을 한 벌 떠 둔다: `git show origin/main:jagwa/index.html > /tmp/base_jagwa.html`. 그다음 `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect 4ff30587` → 1,661,511 B · 인라인 스크립트 5 개 문법 0(채팅이 잼). 멈추면(종료 2 · 3) 그 줄만 알린다.
4. 관문을 돌린다: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python _qa/_qa_small_gate.py --spec spec_chv.json --new jagwa/index.html --base /tmp/base_jagwa.html --spd <클론> --eng chromium,webkit --base-eng chromium`
   - `--spd` = `git clone --depth 1 https://github.com/zzikkaplan/studyplandata`(받기만 · 쓰기 0 · 채팅이 잰 판 3c2bfe5). `--base` 는 **파일 경로**로 준다.
   - 명세 = 화면 4(PC 셋 · 폰 하나) · 칸 15. `yard: true` 11 칸은 바탕에서 FAIL 이어야 하고, `yard: false` 4 칸(회독 창 열림 · 답 고르면 지금 회독 칸 · 회독 창 안 열고 누르면 지금 회독 칸)은 바탕도 PASS 여야 한다.
   - 칸은 데이터에 있는 문항을 쓴다(지난 회독 기록 b 가 있는 지문 O△X 문항 · 〈보기〉 O△X 문항 하나씩). 잣대는 그 문항 기록 `h[0]` 에서 그때 읽어 화면과 맞댄다(값 박지 않음). 클론이 바뀌어 setup ERR 이나 FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시 돌린다. 앱 결함이면 고치지 말고 칸 이름과 값만 알린다.
   - 채팅 컨테이너에서 같은 명령: 새 판 크롬 15/15 · 웹킷 15/15 PASS · 바탕 크롬 헛잣대 10 FAIL · 무변 5 PASS · 합계 FAIL 0 · 1.9 분.
5. 회귀 사슬 · grep 회귀는 안 돌린다(작은 고침).
6. 커밋 하나(`jagwa/index.html`)를 만들고, **genie main 에 fast-forward push**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님).
   - 커밋 글 = WebKit 줄 · 관문 합계 줄 · 앱 md5 · 단계별 분.
   - push 가 막히면 지정 가지에 올리고 그 사실만 알린다.
- 지킬 것:
  - 공개 저장소다. 커밋 글에 기록 값(문항 · O△X · 답 · 수)을 넣지 않는다.
  - `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않는다(채팅이 검수 뒤 걷음).
- 사용자 할 일 = 모든 기기에서 자과 서재를 새로고침 한 번.

## 패치가 하는 일(7 쌍 · 채팅이 a9dcf1d5 에 넣어 4ff30587)
1. `bogiOf` 자리에 `CHV`(보는 지난 회독 번호 · 그 문항 `VNO` · 그 열람 `VSEEN` 동안만) · `chvEnt`(그 회독 기록 항목 · 지금 열람 앞 것만) · `bogiOf` = 지난 회독 보는 중이면 그 항목 `b` · 아니면 `BG` 그대로 · `chvPaint`(카드 O△X `on` · 선택지 `pick` · `markWrong` · `markAns` 다시 칠함) · `chvSet(i)`.
2. 카드 층 `showProblem` 의 새 열람 줄 뒤 `CHV=null`(카드를 다시 그리면 지금 회독).
3. 카드 `.ox` 누름: 지난 회독 보는 중이면 그 항목 `b` 를 고치고 `ST` 저장(`saveST` · 회독 창 마크 고치기와 같은 길) → `chvPaint` · `navSync` 후 끝 · 아니면 옛 길(`BG`) 그대로.
4. 회독 창 「N회독」 누름: `inkSet(i)` 뒤 카드 층이면 `chvSet(i)`.
5. `pickChoice` 첫머리: 지난 회독 보는 중이면 `CHV=null` · `chvPaint` 뒤 옛 길(지금 회독에 기록).
6. `markWrong`: 맞음 · 틀림 색 = `CARD.open || chvEnt()`(보기 설명 `.bexp` 는 `CARD.open` 그대로).
7. `markAns`: 정답 테두리 = `CARD.open || chvEnt()`.

## 점검표(채팅)
1. **일꾼** = 클라우드(앱 파일 하나).
2. **차례** = 한 판 · 「~뒤」 없음.
3. **회귀** = 없음(작은 고침 · 관문 15 칸 × 두 엔진 + 바탕).
4. **선례**
   - 회독 창 마크 고치기(`histSheet` · `x.m` → `ST` → `saveST`) = 지난 회독 기록을 고치는 길 그대로 · 저장 칸 무변.
   - `nrCarryMem`(uid_unify G-3-2) = 지난 회독 O△X 를 `h` 끝 항목 `b` 로 옮겨 둔 자리 · `chHasQ` = 서랍 △ 가 그 `b` 를 읽는 자리.
   - `bogiOf` 부르는 자리 전수 = `renderCard` · `markWrong` 둘(`renderCard` 는 비교 창 그림 `g3CardSnap` 도 부름 → 거기선 `VNO` 가 다른 문항이라 `BG` 그대로 · `CHV=null` 은 `showProblem` 에만 둠).
5. **저장 칸** = 무변(status `h[i].b` 는 11/05 판부터 있던 칸).
6. **근거**
   - 사용자 11/06 22:11 시안 댓글 「이게 내가 체크한 정답이야? 틀렸는데 그럼 정답은 뭔데? 테두리 안해?」
   - 사용자 11/06 21:38 「지문마다 O△X 체크한 거 창 닫고 다시 열 때 1회독 눌러도 안 보여」 · 21:45 「고칠 수 있게도 · 정답 체크한 것도 보이게」.
   - 채팅이 원격 기록(21:40)에서 잰 것: 지학 지난 회독 b 있음 44 · 그중 선택지 O△X 5 — 값은 남고 그리는 자리 0.
7. **화면 끝** = 첫 절 · 사용자 할 일.
9. **클라우드** = 관문 + 헛잣대만.
10. **더 빨리** = 채팅이 관문 두 엔진을 미리 돌려 FAIL 0.
13. **inbox** = 고정 가지.
14. **세 줄** = 21:4x · 22:1x 사용자에게 먼저 보냄.
15. **과목** = 지학 · 생물 같은 함수(카드 층 `HASBOOK`) · 물리 = `chvEnt` 가 늘 null(무변).
