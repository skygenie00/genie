# _task_tt_recimp_1106 — tt 📥 학습기록 가져오기 창: 날짜가 많으면 「가져오기」 단추가 화면 밖 → 목록만 굴림 [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(tt · 📥 학습기록 가져오기 · 직접 읽기 · 붙여넣기 인식 뒤 날짜 목록): 날짜 목록(`#recPv`)이 화면 높이 42 % 에서 멈추고 그 안에서 굴러감 · 창 상자도 화면 90 % 를 넘으면 상자 안에서 굴러감 → 「가져오기」 · 「닫기」 가 늘 화면 안. 날짜 줄 꼴 · 체크 · 펼침 · 가져오기 동작 · 기록 무변.

- 판 크기 = 작음(앱 패치 2 쌍 · 새 파일 0 · 짤 것 0 — 관문 스크립트 `tt_gate.py` 는 이 폴더에 채팅이 둠 · tt_c2rreal_1028 판 그대로)
- 로컬 필요 = 0
- 시간 = ≈5 분(선례 jagwa_jmown_1106 「보냈어」 → main 4 분 · 이 판 관문 두 엔진 + 바탕 41 초)

## 할 일(차례대로 · 이것만)
0. WebKit 을 세운다(이 저장소 CLAUDE.md 「WebKit」 절). 잰 결과를 커밋 글 첫 줄에 적는다.
1. `git fetch origin main cloud/inbox` · 바탕 = main **90bd89b**(`timetable/index.html` LF md5 **8a310644** · `_qa/_qa_apply_patches.py` md5 **b8887814**) — 다르면 멈추고 커밋 없이 이 줄만 알림(main 이 timetable 을 안 건드린 커밋만 앞섰으면 그대로 간다).
2. `cloud/inbox` 의 `_qa/cloud_batch/tt_recimp_1106/` 에서 셋을 꺼냄: `app_patches.txt`(md5 edb4f8cd) · `spec_recimp.json`(md5 0b2539f4) · `tt_gate.py`(md5 6079bef3).
3. `python _qa/_qa_apply_patches.py app_patches.txt timetable/index.html --expect 9c68b4d9` → 532,245 B · 인라인 스크립트 문법 0(채팅이 잼). 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python tt_gate.py --spec spec_recimp.json --new timetable/index.html --base 90bd89b --spd <studyplandata 클론> --eng chromium,webkit --base-eng chromium`
   - `--spd` = `git clone --depth 1 https://github.com/zzikkaplan/studyplandata`(받기만 · 쓰기 0 · PUT 은 관문이 가짜 200).
   - 명세 = PC 1100 · 폰 384 × 5 칸 = 10 칸 · 날짜 60 일은 명세가 지어낸 시험 줄(2025-01-01 ~ · 「관문시험」 · 기록 값 0) · `yard: true` 8 칸 = 바탕 FAIL(단추 화면 안 · 목록만 굴림 · 상자 화면 안 · 가져오기 누름 → 창 닫힘) · `yard: false` 2 칸 = 바탕도 PASS(날짜 60 · 체크 60).
   - 채팅 컨테이너에서 같은 명령(크롬 · 웹킷): 새 판 20/20 PASS · 바탕 크롬 yard 8 FAIL · 무변 2 PASS · 합계 FAIL 0 · 41 초.
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시. 앱 결함이면 고치지 말고 칸 이름만 알림.
5. 회귀 사슬 · grep 회귀 안 돌림(작은 고침 · 바뀐 것 = 가져오기 창 글 두 군데 style).
6. 커밋 하나(`timetable/index.html`) · main 이 바탕 그대로면 **genie main 에 fast-forward push**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님) · 커밋 글 = WebKit 줄 · 관문 결과 줄 · 앱 md5 · 단계별 분. push 가 막히면 지정 가지에 올리고 그 사실만 알림.
- 지킬 것: 공개 저장소 — 커밋 글에 기록 값 0 · 사용자 기록 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(채팅이 검수 뒤 걷음). `tt_gate.py` 를 main 에 넣지 않음.
- 사용자 할 일 = 모든 기기 tt 새로고침 한 번.

## 패치가 하는 일(2 쌍 · 채팅이 8a310644 에 넣어 9c68b4d9 · 532,245 B)
1. `recImportModal` 상자 — `style="max-width:560px"` 에 `max-height:90vh;overflow:auto` 를 더함(같은 앱 pmPop 82vh · foodV 86vh · shV 88vh 와 같은 꼴).
2. `recImportModal` 미리보기 `#recPv` — `max-height:42vh;overflow:auto` 를 더함(날짜 목록만 굴림 · 단추 늘 보임).

## 점검표(채팅)
1. **일꾼** = 클라우드(앱 파일 하나). 2. **차례** = 한 판 · 「~뒤」 없음. 3. **회귀** = 없음(작은 고침 · 무변 2 칸 × 두 엔진).
4. **선례** = tt_c2rreal_1028(tt_gate.py · 같은 길) · 같은 앱 창 막이 = pmPop · foodV · shV(상자 max-height + overflow:auto) · galDD · cbmM(flex 세로 + max-height) · 막이 없는 창 = calZoomM · calDayM · bpModal · aiPopWrap · recImpM(이 판은 recImpM 만 · 나머지는 사용자 짚은 것 아님).
5. **저장 칸** = 무변. 6. **근거** = 사용자 11/06 10:23 그림 「학습기록 불러오기 하려는데 이렇게 길어서 누를 수가 없는데」 · 10:25 「지시서 써줘」.
7. **화면 끝** = 첫 줄 · 사용자 할 일. 9. **클라우드** = 관문 + 헛잣대만. 10. **더 빨리** = 채팅이 관문 두 엔진을 미리 돌려 FAIL 0.
13. **inbox** = 고정 가지. 14. **세 줄** = 10:2x 사용자에게 먼저 보냄.
