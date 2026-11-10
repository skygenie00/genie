# _task_minbeop_jnjt_1110 — 민법OX 정리 목록 창: 근거 줄 밑 댓글에도 「단 문항 지문」 [클라우드 · 작은 고침 · 앱 하나 · main push 한 번]

**화면에서 달라지는 것**
- 📋 정리 목록 창에서 근거 줄 밑 댓글(↳ 줄)마다 그 위 줄에 「댓글을 단 문항 지문」이 보인다. 카드 근거 판 · 연결 상자 댓글(ggCsHTML → ggFromHead)과 같은 꼴이다.
- 지금은 카드에는 지문이 보이고 정리 창 근거 줄 밑 댓글에는 안 보인다. 11/05 jn_cm 판에서 만든 줄 그리기(jnGgHTML)를 11/10 지학식 근거 판(ggjigak_1110)이 안 고쳤기 때문이다.
- O/X 는 지문 오른쪽에 한 번만 보인다(카드와 같음). 옛 「댓글 글 뒤 O/X」 는 걷는다(겹쳐 두 번 보이지 않게).
- 지문을 톡 → O/X 고르개 → 고르면 저장되고 그 줄이 바로 바뀐다(카드와 같은 길 · ggJoSet → ggJnRepaint).
- 끝의 단 문항 칩 · 연결 근거 문항 칩 · 댓글 ! 빨간 세로줄 · 저장 꼴 · 동기화 길은 무변(보이는 꼴만).

- 판 크기 = 작음(앱 하나 · 패치 3 쌍 · 새 파일 0 · 짤 것 0 · 관문 = `gg_gate.py`(ggjigak_1110 그대로 · 이 폴더에만) + 명세 하나)
- 로컬 필요 = 0
- 시간 = ≈20 분(선례 jagwa_ggmath2_1110 20:17 넘김 → 20:21 인도 · 이 판 관문 채팅 잼 = 새 판 크롬 0.5 + 웹킷 0.5 분 · 바탕 크롬 0.7 분)

## 할 일(차례대로 · 이것만)
0. WebKit 을 세운다(이 저장소 CLAUDE.md 「WebKit」 절). 잰 결과를 커밋 글 첫 줄에 적는다.
1. `git fetch origin main cloud/inbox` · 바탕 = main **a4aa63e**(`minbeop/index.html` LF md5 **96e1212c** · `_qa/_qa_apply_patches.py` **b8887814**) — 다르면 멈추고 커밋 없이 이 줄만 알림(main 이 민법을 안 건드린 커밋만 앞섰으면 그대로 간다).
2. `cloud/inbox` 의 `_qa/cloud_batch/minbeop_jnjt_1110/` 에서 셋을 꺼냄: `ox_patches.txt`(md5 56b50f8b) · `spec_mbjt.json`(md5 7cda62ba) · `gg_gate.py`(md5 784c647f).
3. `python _qa/_qa_apply_patches.py ox_patches.txt minbeop/index.html --expect 52b512aa` → 1,262,591 B · 인라인 스크립트 7 · 문법 0(채팅이 잼). 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문(데이터 = `git clone --depth 1 https://github.com/zzikkaplan/studyplandata` · 받기만 · 쓰기 0):
   - `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python gg_gate.py --spec spec_mbjt.json --new minbeop/index.html --base a4aa63e --spd <클론> --eng chromium,webkit --base-eng chromium`
   - 칸 8 · 헛잣대(바탕 FAIL) 6 · 무변(바탕 PASS) 2(「(준비)」 · 댓글 줄 수).
   - 채팅 잼(studyplandata 4e5eb53): 새 판 크롬 8/8 · 웹킷 8/8 · 바탕 크롬 6 FAIL · 2 PASS · 합계 FAIL 0 · 1.8 분.
   - 화면 = 정리 창 Q1064 줄(PC · 폰 384 터치). 지문 톡 · X 톡은 진짜 누름이다. X 저장 = 관문 가짜 200 · 원격 쓰기 0 · 기록 값 0.
   - 앱 꼴은 cdn.tailwindcss.com 으로 선다. 그 주소가 막혀 「폰 … 가로 안 넘침」 칸만 FAIL 이면, 11/10 ggjigak 때처럼 관문 사본에만 Tailwind(npm @tailwindcss/browser)를 넣어 다시 잰다. 앱 파일에는 넣지 않는다.
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시. 앱 결함이면 고치지 말고 칸 이름과 값만 알림.
5. 회귀 사슬 · grep 회귀 안 돌림(작은 고침 · 보이는 꼴만 · 관문이 바뀐 자리를 다 누름).
6. 커밋 하나(`minbeop/index.html`)를 만들고 **genie main 에 fast-forward push**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님).
   - 커밋 글 = WebKit 줄 · 관문 합계 줄 · 앱 md5 · 단계별 분.
   - push 가 막히면 지정 가지에 올리고 그 사실만 알림.
- 지킬 것: 공개 저장소 — 커밋 글에 기록 값 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(채팅이 검수 뒤 걷음). 명세 · gg_gate.py 를 main 에 넣지 않음.
- 사용자 할 일 = 모든 기기에서 민법OX 새로고침 한 번.

## 패치가 하는 일(3 쌍 · 96e1212c → 52b512aa)
1. `jnGgHTML` 의 `line(c, tail)` → `line(c, tail, gu, gk)`: 줄 맨 앞에 `ggFromHead(c, gu, gk)`(카드와 같은 「지문」 + O/X · 누르면 O/X 고르개) · 그다음 「↳ 댓글 글」 · 옛 글 뒤 O/X 는 걷음.
2. 이 문항 근거 댓글 = `line(c, '', id, g.k)`(임자 = 이 문항).
3. 이 문항이 연결한 근거 댓글 = `line(c, <연결 문항 칩>, u, g.k)`(임자 = 연결 근거 문항).

## 점검표(채팅)
1. **일꾼** = 클라우드(앱 파일 하나). 2. **차례** = 한 판 · 「~뒤」 없음. 3. **회귀** = 없음(보이는 꼴만 · 관문이 바뀐 자리를 누름).
4. **선례** = 카드 댓글 줄 ggCsHTML(4618) → ggFromHead(4319) · 정리 창 jn_cm(11/05) · 지학 정리 창 g3PopCsHTML(지문 「…」 보임) · ggjigak_1110 관문 gg_gate.py.
5. **저장 칸** = 무변(c.jo 는 지금도 쓰는 칸).
6. **근거** = 사용자 11/10 20:32 「민법 정리 목록에서 왜 댓글 지문 안 보여」 · 20:36 「뭐는 보이고 뭐는 안 보이고 기준이 뭐야」.
7. **화면 끝** = 첫 줄 · 사용자 할 일. 9. **클라우드** = 관문 + 헛잣대만. 10. **더 빨리** = 채팅이 관문 두 엔진 + 바탕을 미리 돌려 FAIL 0.
13. **inbox** = 고정 가지. 14. **세 줄** = 20:3x 사용자에게 먼저 보냄.
