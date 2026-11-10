# _task_ggjt_1110 — 민법OX · 자과: 댓글엔 늘 「그 지문」 — 정리 창 줄 · 근거 검색 결과 [클라우드 · 작은 고침 · 앱 둘 · main push 한 번]

**화면에서 달라지는 것**
- 민법 📋 정리 목록 창: 근거 줄 밑 댓글(↳ 줄)마다 그 위 줄에 「댓글을 단 문항 지문」 + O/X 가 보인다. 카드 근거 판 · 연결 상자 댓글(ggCsHTML → ggFromHead)과 같은 꼴이다.
  - 지문을 톡 → O/X 고르개 → 고르면 저장되고 그 줄이 바로 바뀐다(카드와 같은 길).
  - 옛 「댓글 글 뒤 O/X」 는 걷는다(두 번 안 보이게).
- 근거 검색 결과(민법: 위 검색 줄 근거 갈래 · 카드 「근거에서 찾기」 / 자과: 위 검색 줄 · 카드 안 찾기): 걸린 근거마다 「i. 근거」 줄, 그 밑에 걸린 댓글 하나하나를 「그 지문」 O/X 줄 + 「↳ 댓글」 줄로 보인다.
  - 지금은 첫 근거 하나 + 첫 댓글 하나만, 지문 · O/X 없이 보인다.
  - 찾는 까닭(사용자 20:48): 지금 푸는 지문과 같은 쟁점의 근거를 찾아 연결하는 것 → 그 근거를 어느 지문에 어떻게(O/X) 썼는지 보여야 고를 수 있다.
  - 지문 = 민법은 댓글을 단 문항(c.from || 근거 임자) 지문 · 자과는 댓글 지문(c.jt · 지문 점 없이 단 옛 댓글은 지문 줄 없이 ↳ 만).
  - 「지문」 줄은 90 자에서 안 자른다(판단 재료). 찾은 낱말은 줄마다 노랑 표시 — 카드 안 찾기(고르는 목록)도.
  - 아무 데도 안 걸린 문항 · 검색어 없음 = 옛 그대로(첫 근거 한 줄).
- 저장 꼴 · 동기화 길 · 고르기(누름 = 연결 · 문항 창) 무변(보이는 꼴만).

- 판 크기 = 작음(앱 둘 · 민법 패치 8 쌍 · 자과 4 쌍 · 새 파일 0 · 짤 것 0 · 관문 = 민법 `gg_gate.py`(ggjigak_1110 그대로) · 자과 공용 `_qa/_qa_small_gate.py` + 명세 둘)
- 로컬 필요 = 0
- 시간 = ≈30 분(선례 ggjigak_1110 두 앱 19:05 넘김 → 19:31 인도 · 이 판 관문 채팅 잼 = 민법 새 판 크롬 1.2 + 웹킷 1.3 분 · 바탕 1.4 분 · 자과 0.4 분)

## 할 일(차례대로 · 이것만)
0. WebKit 을 세운다(이 저장소 CLAUDE.md 「WebKit」 절). 잰 결과를 커밋 글 첫 줄에 적는다.
1. `git fetch origin main cloud/inbox` · 바탕 = main **a4aa63e**(`minbeop/index.html` LF md5 **96e1212c** · `jagwa/index.html` LF md5 **506744ee** · `_qa/_qa_apply_patches.py` **b8887814** · `_qa/_qa_small_gate.py` **867625c3**) — 다르면 멈추고 커밋 없이 이 줄만 알림(main 이 두 앱을 안 건드린 커밋만 앞섰으면 그대로 간다).
2. `cloud/inbox` 의 `_qa/cloud_batch/ggjt_1110/` 에서 다섯을 꺼냄: `ox_patches.txt`(md5 bf20a6ab) · `jagwa_patches.txt`(md5 a2942c16) · `spec_mbjt.json`(md5 8f29b60d) · `spec_jgs.json`(md5 c32cc444) · `gg_gate.py`(md5 784c647f).
3. 바탕을 떠 둠: `git show origin/main:jagwa/index.html > /tmp/base_jagwa.html`. 그다음
   - `python _qa/_qa_apply_patches.py ox_patches.txt minbeop/index.html --expect bfd268bc` → 1,264,357 B · 인라인 7 · 문법 0
   - `python _qa/_qa_apply_patches.py jagwa_patches.txt jagwa/index.html --expect 300a7c0e` → 1,667,534 B · 인라인 5 · 문법 0(둘 다 채팅이 잼)
   - 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문(데이터 = `git clone --depth 1 https://github.com/zzikkaplan/studyplandata` · 받기만 · 쓰기 0):
   - 민법: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python gg_gate.py --spec spec_mbjt.json --new minbeop/index.html --base a4aa63e --spd <클론> --eng chromium,webkit --base-eng chromium`
     - 칸 13 · 헛잣대 10 · 무변 3. 채팅 잼(studyplandata 4e5eb53): 새 판 크롬 · 웹킷 13/13 · 바탕 10 FAIL · 3 PASS · 합계 FAIL 0 · 4.0 분.
   - 자과: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python _qa/_qa_small_gate.py --spec spec_jgs.json --new jagwa/index.html --base /tmp/base_jagwa.html --spd <클론> --eng chromium,webkit --base-eng chromium`
     - 칸 6 · 헛잣대 4 · 무변 2. 채팅 잼: 새 판 크롬 · 웹킷 6/6 · 바탕 4 FAIL · 2 PASS · 합계 FAIL 0 · 0.4 분.
   - 시험 댓글 · 근거 · 지문(「관문낱말 하나」 · 「시험 근거 글」 · 「ㄱ. 시험 지문 글」 · GX-OWN)은 명세가 지어 넣는 글이다. 저장 = 관문 가짜 200 · 원격 쓰기 0 · 기록 값 0. 지문 톡 · X 톡 · 검색 줄 치기는 진짜 누름 · 진짜 타자.
   - 민법 앱 꼴은 cdn.tailwindcss.com 으로 선다. 그 주소가 막혀 폰 「가로 안 넘침」 칸만 FAIL 이면, 11/10 ggjigak 때처럼 관문 사본에만 Tailwind(npm @tailwindcss/browser)를 넣어 다시 잰다. 앱 파일에는 넣지 않는다.
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시. 앱 결함이면 고치지 말고 칸 이름과 값만 알림.
5. 회귀 사슬 · grep 회귀 안 돌림(작은 고침 · 보이는 꼴만 · 관문이 바뀐 자리를 다 누름).
6. 커밋 하나(`minbeop/index.html` · `jagwa/index.html`)를 만들고 **genie main 에 fast-forward push**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님).
   - 커밋 글 = WebKit 줄 · 관문 합계 줄 둘 · 앱 md5 둘 · 단계별 분.
   - push 가 막히면 지정 가지에 올리고 그 사실만 알림.
- 지킬 것: 공개 저장소 — 커밋 글에 기록 값 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(채팅이 검수 뒤 걷음). 명세 · gg_gate.py 를 main 에 넣지 않음.
- 사용자 할 일 = 모든 기기에서 민법OX · 자과 서재 새로고침 한 번.

## 패치가 하는 일
- 민법(8 쌍 · 96e1212c → bfd268bc)
  1~3. `jnGgHTML` 의 `line(c, tail)` → `line(c, tail, gu, gk)`: 줄 맨 앞 `ggFromHead(c, gu, gk)` · 그다음 「↳ 글」 · 글 뒤 O/X 걷음 · 부르는 두 자리에 임자 · 근거 키를 넘김.
  4. `ggPickLine`: 검색어가 있으면 걸린 근거마다 「i. 근거」 + 걸린 댓글마다 「「지문」 O/X」 줄 · 「↳ 댓글」 줄 · 안 걸리면 옛 줄.
  5~6. 위 검색 줄(runSearch 근거 갈래): 줄 하나하나를 그림(지문 줄은 작은 회색) · 줄마다 낱말 표시.
  7~8. 카드 「근거에서 찾기」(linkSearch): 「지문」 줄은 안 자름 · 줄마다 낱말 표시.
- 자과(4 쌍 · 506744ee → 300a7c0e)
  1. `ggPickLine`: 민법과 같은 꼴(지문 = c.jt).
  2. `ggResRowHTML`: 「지문」 줄은 안 자름.
  3. 낱말 표시를 카드 안 찾기(pick)에도.
  4. 줄마다 낱말 표시.

## 점검표(채팅)
1. **일꾼** = 클라우드(앱 파일 둘). 2. **차례** = 한 판 · 「~뒤」 없음. 3. **회귀** = 없음(보이는 꼴만 · 관문이 바뀐 자리를 누름).
4. **선례** = 카드 댓글 줄 ggCsHTML → ggFromHead · 정리 창 jn_cm(11/05) · 검색 결과 = 10/14 쓸모없음 100 「찾은 줄 하나하나 · 자리 · 낱말 표시」 · 09/14 「댓글도 본문과 같은 자격으로 찾는다」 · ggjigak_1110 관문.
   - 댓글을 그리는 자리 전수(민법 · 채팅 잼 6 곳): 카드 · 연결 상자 = 이미 지문 / 정리 창 · 검색 결과 = 이 판 / 지문 점 창(지문 바로 밑 목록) · 댓글 지우기 창(첫 줄 되묻기) = 지문 필요 없음.
5. **저장 칸** = 무변.
6. **근거** = 사용자 11/10 20:32 「민법 정리 목록에서 왜 댓글 지문 안 보여」 · 20:36 「뭐는 보이고 뭐는 안 보이고 기준이 뭐야」 · 20:48 「검색이 제일 중요 · 뭘 봐야 목적 달성?」.
7. **화면 끝** = 첫 줄 · 사용자 할 일. 9. **클라우드** = 관문 + 헛잣대만. 10. **더 빨리** = 채팅이 관문 두 엔진 + 바탕을 미리 돌려 FAIL 0.
13. **inbox** = 고정 가지(옛 minbeop_jnjt_1110 = 이 판에 합쳐 걷음). 14. **세 줄** = 20:5x 사용자에게 먼저 보냄.
