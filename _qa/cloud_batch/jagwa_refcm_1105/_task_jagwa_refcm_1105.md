# _task_jagwa_refcm_1105 — 자과 지학: 연결한 근거에 다른 문제에서 댓글 · 출처 · 서랍 작은 창 · 정리 창 · Enter/Tab · 댓글 끌기 · 댓글 ! [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(지학 · 카드 층 근거 세 칸):
1. 근거 찾기로 넣은 항목(`g.src` 가 임자 문항 근거를 가리킴)의 「댓」 칸에 **임자 근거의 댓글**이 먼저 보이고, 거기서 단 댓글은 **임자 근거에 저장**되며 끝에 단 문항 ID(`from`)가 붙음 — 누르면 그 문항이 옆에 열림.
2. 목차서랍 **작은 창**(g3Pop) · 📋 **정리 창**(jn)에서 근거 항목 밑에 그 근거의 댓글(↳ 글 + 출처 ID)이 보임.
3. 댓글 칸 · 근거 적는 칸 · 댓글 고치기 칸: **Enter = 저장 · Shift+Enter = 줄바꿈 · Tab = 빈칸 넷**(칸 밖으로 안 나감) · 한글 조합 중 Enter 는 저장 안 함.
4. 댓글 왼쪽 세로줄을 **끌어 댓글끼리 차례** 바꿈(민법 ox_csdrag 꼴).
5. 댓글에도 **「!」** — 누르면 그 댓글 세로줄 빨강 · 목차서랍 그 문제 줄 빨간 세로줄(근거 ! 와 같은 기능).
- 이미 있는 근거 · 댓글 · 기록 꼴 무변(댓글에 `from` · `bang` 칸만 더해짐 · 저장 파일 · 동기화 길 그대로).

- 판 크기 = 작음(앱 패치 22 쌍 · 새 파일 0 · 짤 것 0)
- 로컬 필요 = 0
- 시간 = ≈6 분(선례 jagwa_imgkey_1025 「보냈어」 → main ≈4 분 · 이 판 관문 두 엔진 2.2 분)

## 할 일(차례대로 · 이것만)
1. `git fetch origin main cloud/inbox` · 바탕 = main **081c03a**(`jagwa/index.html` LF md5 **75506fcb** · `_qa/_qa_small_gate.py` md5 **867625c3** · `_qa/_qa_apply_patches.py` md5 **b8887814**) — 다르면 멈추고 커밋 없이 이 줄만 알림.
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_refcm_1105/` 에서 둘을 꺼냄: `app_patches.txt`(md5 34d1c427) · `spec_refcm.json`(md5 73a646d2).
3. 바탕 앱을 한 벌 떠 둠(`git show 081c03a:jagwa/index.html > /tmp/base_081c03a.html`) 뒤 `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect ef6b6c7e` — 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문: `python _qa/_qa_small_gate.py --spec spec_refcm.json --new jagwa/index.html --base /tmp/base_081c03a.html --eng chromium,webkit --base-eng chromium`(`--vendor` · `--spd` · `--notes` 는 지난 판과 같이 · `--base` 는 **파일 경로**로 — 커밋 이름을 주면 「바탕 앱을 못 읽었다」 로 멈춤을 채팅이 잼).
   - 명세 = PC 둘(p1 이어 둔 항목 댓글 칸 열림 · p2 시험 댓글 둘 심음) · 폰 하나 × 18 칸 · `yard: true` 14 칸 = 바탕 FAIL · `yard: false` 4 칸 = 바탕도 PASS(Tab 누름 · Shift+Enter 저장 안 함 · 한글 조합 Enter 누름 · 작은 창 닫기).
   - 시험 데이터 = 명세 setup 이 메모리에만 심는 지어낸 글 「(시험 글) …」 · 원격 쓰기 없음.
   - 채팅 컨테이너에서 같은 명령(크롬 · 웹킷): 새 판 36/36 PASS · 바탕 크롬 yard 14 FAIL · 무변 4 PASS · 2.2 분.
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시. 앱 결함이면 고치지 말고 칸 이름 · 값만 알림.
5. 회귀 사슬 · grep 회귀 안 돌림(작은 고침).
6. 커밋 하나(`jagwa/index.html`) · main 이 바탕 그대로면 **genie main 에 fast-forward push**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님) · 커밋 글 = 관문 결과 줄 그대로 · 앱 md5 · 단계별 분. push 가 막히면 지정 가지에 올리고 그 사실만 알림.
- 지킬 것: 공개 저장소 — 시험 글은 명세 안 글뿐 · 사용자 기록 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음.
- 사용자 할 일 = 모든 기기 앱 새로고침 한 번.

## 패치가 하는 일(22 쌍 · 채팅이 75506fcb 에 넣어 ef6b6c7e · 1,639,419 B · 인라인 스크립트 문법 0)
1. `ggFromHTML(c)` 새 함수 = 댓글 끝 출처 ID 칩(`.ggfrom` · data-go 길 = 옆에 열기 vSwapOpen) · data-go 처리 closest 목록에 `.ggfrom`.
2. `g3OtherCsHTML` 출처 = `c.from` 먼저.
3. `g3ChipHTML`: `ggSrcOf(g)` 가 있으면 댓글 상자에 임자 근거 댓글(`data-ggcs="임자uid|k|…"`)을 먼저 · 그다음 이 항목 자기 댓글 · 「다른 문제 댓글」 목록에서 임자는 뺌(두 번 안 보이게).
4. `ggReply`: 항목에 `ggSrcOf` 가 있으면 댓글을 임자 근거 `cs` 에 `{k,t,ts,from:이 문항}` 로 넣고 임자 저장 · 두 문항 다시 그림.
5. `g3PopCsHTML(uid,g)`(window 에도) = 근거 밑 댓글 줄(임자 cs + 자기 cs · 개념 묶음 `__cq` 은 그 댓글) → 작은 창 세 갈래 · 정리 창 `jnRowHTML` 근거 줄에 붙임.
6. 키: Tab = 빈칸 넷(`.ggrow .txt` · `[data-ggcin]` · `.ggedin` · `.cein` · `.g3ed textarea` · setRangeText + input) · `.ggedin/.cein` Enter = 저장 누름 · Enter 처리마다 `!e.isComposing`.
7. `ggCsHTML` 줄 = `data-gk/data-guid` · 끌기 세로줄 `.ggcsdh` · 「!」 단추 `.ggcbg[data-ggcbang]` · `ggCsBang`(c.bang 뒤집기 → 저장 · ggBangPaint) · `ggCsMove` + 끌기(민법 ox_csdrag 옮김 · 끈 뒤 600 ms 누름 삼킴) · `ggBangAny` 가 댓글 bang 도 셈.
8. CSS = `.ggfrom` · `.g3prc` · `.ggcsdh` · `.ggcbg` · `.ggcs.bang` 빨간 세로줄.

## 점검표(채팅)
1. 일꾼 = 클라우드 · 2. 한 판(같은 앱 파일 하나) · 3. 회귀 = 없음(작은 고침 · 관문 18 칸 × 두 엔진 + 바탕 무변 4 칸) · 4. 선례 = 민법 ox_csdrag_1103(cdaa723 · 댓글 끌기 · 정리 창) · 10/11 결정(지학 연결 = 근거 찾기 g.src 임자 · GGREF 🔗 상자 아님 · 쓸모없음 305) · jagwa_imgkey_1025(같은 길) · 5. 저장 칸 = 댓글 `from` · `bang` 두 칸 더함 · 저장 파일 · 동기화 무변 · 6. 근거 = 사용자 11/05 00:20 · 00:27 · 00:40 · 00:46 · 00:52 · 00:56 · 01:02 「지시서 써줘」 · 시안 VvTodtrsWEsj3TF3pAWa41 v7 · 7. 화면 끝 = 첫 절 다섯 줄 · 관문 칸이 그 줄마다 · 9. 클라우드 = 관문만 · 10. 더 빨리 = 회귀 0 · 관문 2.2 분 · 13. 클라우드 먼저 · 14. 세 줄 먼저 = 01:2x 사용자에게 보냄 · 15. 과목 = 지학 카드 층(댓글 줄 · 키 · 끌기 · ! 는 공용 함수 — 물리 화면은 관문에서 안 잼) · 20. inbox.
