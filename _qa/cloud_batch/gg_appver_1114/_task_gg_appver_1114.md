# _task_gg_appver_1114 — 민법OX · 조판기 · 자과 서재 · 시간표: 새 판 스스로 받기(열릴 때 · 돌아올 때) [클라우드 · 앱 넷 · main push 한 번]

**화면에서 달라지는 것**(사용자 11/14 03:17 「아직 앱에 적용이 안 된 건가」 · 03:24 「왜 안 바뀌어 있지」 · 03:26 「10 분 캐시 설정? 왜 이렇게 설정돼 있는데」 · 03:28 「넣어」)
- 지금: 앱 파일(index.html)이 main 에 올라가도, 기기가 그 파일을 마지막으로 받은 때부터 10 분 동안은 옛 판이 뜬다(GitHub Pages 가 모든 파일에 `cache-control: max-age=600` 을 붙임 · 머리글은 못 바꿈).
- 바뀐 뒤: 앱이 **열릴 때**와 **돌아올 때(화면이 다시 보일 때)** 서버의 앱 파일이 지금 화면의 것과 다르면 스스로 새 판으로 다시 연다.
  - 글 칸에 커서가 있거나(적는 중) · 손을 대고 있거나 · 저장 중이면 건너뛴다(다음에 돌아올 때 다시 본다).
  - 다른 앱만 올라간 배포에는 다시 열지 않는다(파일 글이 같으면 그대로).
  - 화면에 새 글자 · 단추 0. 저장 꼴 · 원격 쓰기 0(받기만 = HEAD 한 번 · 배포가 있었을 때만 GET 한 번).
- 네 앱에 같은 조각 하나씩(파일 끝 `</body>` 바로 앞 · 따로 선 `<script>`).

- 판 크기 = 작음(앱 넷 · 패치 앱마다 1 쌍 · 새 파일 0 · 짤 것 0 · 관문 = `av_gate.py`(새 것 · 이 폴더에만))
- 로컬 필요 = 0
- 시간 = ≈18 분(선례 gg_shn2_1114 두 앱 02:58 넘김 → 03:13 push = 15 분 · 이 판 관문 채팅 잼 = 앱마다 새 판 두 엔진 96 초 + 바탕 74 초 = 넷 합 11.3 분)

## 할 일(차례대로 · 이것만)
0. WebKit 을 세운다(이 저장소 CLAUDE.md 「WebKit」 절). 잰 결과를 커밋 글 첫 줄에 적는다.
1. `git fetch origin main cloud/inbox` · 바탕 = main **d1330ef**(LF md5 `minbeop/index.html` **83e5422d** · `jo/index.html` **5e492e79** · `jagwa/index.html` **61f69712** · `timetable/index.html` **f5a37d49** · `_qa/_qa_apply_patches.py` **b8887814**) — 넷 중 하나라도 다르면 멈추고 커밋 없이 이 줄만 알림(main 이 네 앱을 안 건드린 커밋만 앞섰으면 그대로 간다).
2. `cloud/inbox` 의 `_qa/cloud_batch/gg_appver_1114/` 에서 다섯을 꺼냄: `ox_patches.txt`(md5 7d42a483) · `jo_patches.txt`(md5 a5d8df92) · `jagwa_patches.txt`(md5 6f562f05) · `tt_patches.txt`(md5 3d2640ed) · `av_gate.py`(md5 5965259b).
3. 바탕 사본을 먼저 떠 둔다(관문 바탕 판): `for a in minbeop jo jagwa timetable; do git show d1330ef:$a/index.html > /tmp/base_$a.html; done`
4. 패치(넷 다 채팅이 잼 · 문법 0):
   - `python _qa/_qa_apply_patches.py ox_patches.txt minbeop/index.html --expect adf59933` → 1,316,282 B
   - `python _qa/_qa_apply_patches.py jo_patches.txt jo/index.html --expect fffe2fa8` → 1,840,331 B
   - `python _qa/_qa_apply_patches.py jagwa_patches.txt jagwa/index.html --expect cd13ecc3` → 1,688,218 B
   - `python _qa/_qa_apply_patches.py tt_patches.txt timetable/index.html --expect d8a66738` → 540,078 B
   - 멈추면(종료 2 · 3) 그 줄만 알림.
5. 관문(저장소 뿌리에서 · 데이터 클론 필요 없음 · 바깥 주소는 관문이 다 막음) — 앱 `a` = minbeop · jo · jagwa · timetable 넷 각각:
   - 새 판: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python av_gate.py --app $a --file $a/index.html --mode new --eng chromium,webkit` → 칸 7 × 두 엔진 = 14 PASS · 합계 FAIL 0(채팅 잼 넷 다 · 엔진마다 48 초).
   - 바탕 판: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python av_gate.py --app $a --file /tmp/base_$a.html --mode base --eng chromium` → 헛잣대 4(바탕 FAIL) · 무변 3(바탕 PASS) · 합계 FAIL 0(채팅 잼 넷 다 · 74 초).
   - 관문이 하는 일: 앱 파일 하나를 `cache-control: max-age=600` 을 붙이는 작은 서버(127.0.0.1 · GitHub Pages 흉내)로 띄우고, 서버 쪽 파일을 바꿔 가며 화면이 스스로 다시 열리는지 진짜 브라우저로 잰다.
   - 칸 일곱: ① 서버 그대로면 다시 안 열림(무변) ② 서버에 새 판 → 돌아오면 다시 열림(헛잣대) ③ 한 번만 다시 열림 · 주소 그대로(헛잣대) ④ 파일 같고 ETag 만 바뀐 배포 → 다시 안 열림(무변) ⑤ 글 칸에 커서 → 다시 안 열림(무변) ⑥ 커서를 뺀 뒤 돌아오면 다시 열림(헛잣대) ⑦ 앱을 새로 엶(10 분 캐시 안) → 곧 새 판(헛잣대).
   - INFO 줄의 「새로 열 때 처음 뜬 판」: 크롬 = 3(캐시의 옛 판이 먼저 뜨고 곧 새 판으로) · 웹킷 = 4(바로 새 판)가 채팅 잰 값이다. 달라도 칸이 PASS 면 된다.
   - 기다림이 고정 값이라(판 바꾼 뒤 5.6 초) 기계가 느려 한 칸만 FAIL 이면 `--gap 8` 로 그 앱만 다시 잰다. 그래도 FAIL 이면 고치지 말고 칸 이름과 값만 알림.
6. 회귀: 채팅이 지난 판 명세 셋을 새 앱에 미리 돌렸다(새 판만 · 두 엔진 · FAIL 0) — 민법 gg_shn2_1114 58 PASS · 조판기 gg_shn2_1114 88 PASS · 자과 gg_shx_1113 76 PASS. 시간표는 명세가 없어 이 관문 + 문법 검사만. 클라우드는 회귀 사슬 · grep 회귀 안 돌림.
7. 커밋 하나(네 앱 `index.html`)를 만들고 **genie main 에 fast-forward push**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님).
   - 커밋 글 = WebKit 줄 · 관문 합계 줄(앱 넷) · 앱 md5 넷 · 단계별 분.
   - push 가 막히면 지정 가지에 올리고 그 사실만 알림.
- 지킬 것:
  - 공개 저장소 — 커밋 글에 기록 값 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(채팅이 검수 뒤 걷음). `av_gate.py` 를 main 에 넣지 않음.
  - **노션 등 커넥터에 적지 않는다** — 결과는 커밋 글에만(이 저장소 CLAUDE.md 5 번). 적으려 하면 사용자에게 허용 창이 떠서 판이 멈춘다(사용자 11/14 03:07). 검색 · 읽기는 그대로.
- 사용자 할 일 = 이 판이 올라간 뒤 모든 기기에서 네 앱을 **한 번** 새로고침(이 조각이 든 판을 받는 것까지는 지금처럼 10 분 걸릴 수 있음 · 그 다음 판부터 스스로 받음).

## 패치가 하는 일(네 앱 같은 조각 · 앱마다 1 쌍 = 파일 끝 `</body>` 앞에 `<script>` 하나)
- 열릴 때: 제 주소를 `cache:'force-cache'` 로 한 번 읽어 **지금 화면의 판** 글 지문(길이 + 해시)과 ETag 를 잡는다(캐시에서 읽음 = 통신 0).
- 볼 때(열린 직후 · `visibilitychange` · `pageshow` · `focus` · 5 초에 한 번까지): `HEAD`(no-store)로 ETag 를 보고 같으면 끝. 다르면 `GET`(no-store)으로 글을 받아 지문을 견준다.
  - 같으면(다른 앱만 올라간 배포) ETag 만 새로 기억.
  - 다르면: 글 칸 커서 · 손 대는 중(pointerdown 뒤 10 초 안) → 건너뜀 / 저장 중(`recBusy` · 시간표 `syncing`) → 3 초 뒤 다시(다섯 번까지) / 아니면 제 주소를 `cache:'reload'` 로 받아 캐시를 새 판으로 갈고 `location.reload()`.
  - 다시 열었는데도 옛 판이면 한 번만 `?v=<시각>` 꼬리를 붙여 새로 받고, 그 뒤로는 더 돌지 않는다(`sessionStorage` `appver_tried` = 이 탭에만 · 기록 저장 꼴과 무관).
- `file:` 로 연 사본에서는 아무것도 안 함.

## 점검표(채팅)
1. **일꾼** = 클라우드(앱 파일 넷). 2. **차례** = 한 판 · 「~뒤」 없음. 3. **회귀** = 채팅이 미리 돌림(위 6).
4. **선례** = 11/08 19:2x · 11/09 12:5x 잰 것(index.html 만 Pages max-age=600 · 기록 · 그림 파일은 앱이 no-store 로 받아 바로 보임 · 민법 · 조판기 · 자과에 서비스 워커 · 자동 새로고침 0) — 자리 전수: Pages 에 올라가는 앱 = `minbeop` · `jo` · `jagwa` · `timetable` · `chem` · 뿌리 `index.html`(기출 서재). 이 판 = 사용자에게 말한 넷. `chem` · 기출 서재는 안 넣음.
5. **저장 칸** = 무변 · SYNC_KEYS 무변 · `sessionStorage` 한 칸(`appver_tried`)은 탭이 닫히면 사라짐.
6. **근거** = 첫 줄 사용자 말 · 응답 머리글 03:25 잼(`cache-control: max-age=600` · ETag = 배포 시각-크기 · 03:3x 네 앱 last-modified 가 안 바뀐 앱까지 같은 배포 시각 = ETag 만으로는 못 가림).
7. **화면 끝** = 첫 줄 · 사용자 할 일. 8. **자료** = 시안 없음(화면 요소 0 · 사용자 「넣어」).
9. **클라우드** = 관문 + 헛잣대만. 10. **더 빨리** = 채팅이 새 판 두 엔진 + 바탕 + 지난 판 회귀를 미리 돌림 · 네 앱 한 판 · push 한 번.
11. **2 시간 한도** = 관문 넷 합 ≈11 분. 12. **전수** = 앱 넷 × 엔진 둘.
13. **inbox** = 고정 가지. 14. **세 줄** = 사용자에게 먼저 보냄.
15. **과목 · 법** = 해당 없음(앱 껍데기).
- 시간표 앱은 서비스 워커(`sw.js` = 통신 먼저 · no-cache)가 있어 **새로 열 때**는 지금도 새 판을 받는다. 이 조각은 열어 둔 채 돌아올 때 몫이다. 관문 서버에는 `sw.js` 가 없어 서비스 워커 낀 길은 못 쟀다.
- 다시 열리면 앱은 첫 화면부터 뜬다(문제 풀던 자리 · 열어 둔 창은 손으로 새로고침한 것과 같게 닫힘 · 적어서 저장된 기록은 그대로).
- 못 잰 것: 아이패드 실물(홈 화면 앱 · 사파리)의 캐시 동작 · 시간표 서비스 워커 낀 길 · 저장 중 건너뛰기(함수 길만 있고 관문 칸 없음).
