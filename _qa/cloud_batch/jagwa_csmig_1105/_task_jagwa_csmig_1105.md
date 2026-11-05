# _task_jagwa_csmig_1105 — 자과 지학 · 생물: 고치기 전에 단 근거 댓글에도 출처 · 옮김 소급 [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(자과 지학 · 생물 카드 층 · 근거 세 칸)
1. 이어 둔 항목(`g.src` = 임자 근거)에서는 임자 근거의 옛 댓글이 출처 없이(`from` 없음) 나오던 것이, 이제 끝에 임자 문항 ID 칩(`.ggfrom`)이 붙어 나온다. 누르면 그 문항이 옆에 열린다(refcm 칩과 같은 꼴).
2. 목차서랍 작은 창 · 📋 정리 창의 근거 밑 댓글 줄(`g3PopCsHTML`)도 같다.
3. 고치기 전 이어 둔 항목에 달아 그 문제 사본(`cs`)에만 남은 댓글은, 동기화가 끝난 뒤 한 번 임자 근거 `cs` 로 옮겨진다(`from` = 그 문제 · 같은 `k` 는 건넘 · 사본 `cs` 비움). 이제 임자 문항과 다른 연결 문항에도 보인다.
- 임자 문항에서 제 옛 댓글은 칩 없이 그대로다. 저장 파일 · 동기화 길 · 칸 꼴은 바뀌지 않는다(옮긴 댓글에 `from` 만 더해짐).

- 판 크기 = 작음(앱 패치 3 쌍 · 새 파일 0 · 짤 것 0 · 관문 = 공용 `_qa_small_gate.py`)
- 로컬 필요 = 0
- 시간 = ≈8 분(선례 jagwa_refcm_1105 「보냈어」 01:35 → main 01:47 · 12 분 · 이 판 관문 크롬 · 웹킷 + 바탕 크롬 = 3.2 분)

## 할 일(차례대로 · 이것만)
0. WebKit 을 세운다(이 저장소 CLAUDE.md 「WebKit」 절). 잰 결과를 커밋 글 첫 줄에 적는다.
1. `git fetch origin main cloud/inbox` 로 바탕을 맞춘다.
   - 바탕 = origin/main(채팅이 잰 때 **b458d3b**).
   - 맞출 값: `jagwa/index.html` LF md5 **6879004a** · `_qa/_qa_apply_patches.py` **b8887814** · `_qa/_qa_small_gate.py` **867625c3**.
   - 다르면 멈추고 커밋 없이 이 줄만 알린다(main 이 jagwa 를 안 건드린 커밋만 앞섰으면 그대로 간다).
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_csmig_1105/` 에서 둘을 꺼낸다: `app_patches.txt`(md5 a01f7ac4) · `spec_csmig.json`(md5 614a1286).
3. 바탕 앱을 한 벌 떠 둔다: `git show origin/main:jagwa/index.html > /tmp/base_jagwa.html`. 그다음 `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect 50a0853e` → 1,658,548 B · 인라인 스크립트 5 개 문법 0(채팅이 잼). 멈추면(종료 2 · 3) 그 줄만 알린다.
4. 관문을 돌린다: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python _qa/_qa_small_gate.py --spec spec_csmig.json --new jagwa/index.html --base /tmp/base_jagwa.html --spd <클론> --eng chromium,webkit --base-eng chromium`
   - `--spd` = `git clone --depth 1 https://github.com/zzikkaplan/studyplandata`(받기만 · 쓰기 0 · 채팅이 잰 판 5d56fe3). `--base` 는 **파일 경로**로 준다.
   - 명세 = 화면 3(PC 둘 · 폰 하나) · 칸 5. `yard: true` 4 칸은 바탕에서 FAIL 이어야 하고, `yard: false` 1 칸(임자 문항 제 옛 댓글 = 칩 없음)은 바탕도 PASS 여야 한다.
   - 칸은 데이터에 있는 문항을 쓴다(G17-54-02 ← G16-53-02 · 사본 댓글 G03-40-06 → G16-53-03). 클론이 그 뒤 바뀌어 setup ERR 이나 FAIL 이 나면, 그 칸만 `--only <칸 이름 앞머리>` 로 다시 돌린다. 앱 결함이면 고치지 말고 칸 이름과 값만 알린다.
   - 채팅 컨테이너에서 같은 명령: 새 판 크롬 5/5 · 웹킷 5/5 PASS · 바탕 크롬 헛잣대 4 FAIL · 무변 1 PASS · 합계 FAIL 0 · 3.2 분.
5. 회귀 사슬 · grep 회귀는 안 돌린다(작은 고침).
6. 커밋 하나(`jagwa/index.html`)를 만들고, **genie main 에 fast-forward push**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님).
   - 커밋 글 = WebKit 줄 · 관문 합계 줄 · 앱 md5 · 단계별 분.
   - push 가 막히면 지정 가지에 올리고 그 사실만 알린다.
- 지킬 것:
  - 공개 저장소다. 커밋 글에 기록 값(근거 · 댓글 글 · 수)을 넣지 않는다.
  - `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않는다(채팅이 검수 뒤 걷음).
- 사용자 할 일 = 모든 기기에서 자과 서재를 새로고침 한 번(첫 동기화 뒤 옛 댓글 옮김이 한 번 돎).

## 패치가 하는 일(3 쌍 · 채팅이 6879004a 에 넣어 50a0853e)
1. `g3ChipHTML`: 이어 둔 항목의 임자 댓글(`srcH`)을 그릴 때 `from` 없는 댓글은 `from = 임자 uid` 를 붙인 사본으로 넘긴다. 칩은 `ggFromHTML` 이 그린다. 저장 값은 바뀌지 않는다.
2. `g3PopCsHTML`: 같은 처리를 한다(보는 문항이 임자면 그대로).
3. `g3CsMig()`(window 에도) + `syncRecords` 감쌈:
   - 첫 동기화 성공 뒤 한 번(`did`) 돈다.
   - 이어 둔 항목(src 임자 ≠ 자기)의 `cs` 를 임자 근거 `cs` 끝에 `{…c, from: c.from || 그 문제}` 로 넣는다. 같은 `k` 는 건너뛴다.
   - 사본 `cs` 를 `[]` 로 비우고 두 문항을 `ggSaveList` → 다시 그린다. 옮긴 것이 있으면 400 ms 뒤 `syncRecords(true)`.
   - 선례 = refcm `g3RefMig` 꼴.

## 점검표(채팅)
1. **일꾼** = 클라우드(앱 파일 하나).
2. **차례** = 한 판 · 「~뒤」 없음.
3. **회귀** = 없음(작은 고침 · 관문 5 칸 × 두 엔진 + 바탕).
4. **선례**
   - jagwa_refcm_1105(67b5f8e · `ggFromHTML` · `g3RefMig` 동기화 뒤 한 번 꼴) · jn_cm_1105(b458d3b · `_qa_small_gate.py` 명세 꼴).
   - 댓글 그리는 자리 전수 = 이어 둔 항목 상자(`g3ChipHTML` srcH) · 작은 창 · 정리 창(`g3PopCsHTML`) · 임자 쪽 다른 문항 댓글(`g3OtherCsHTML` = 이미 `c.from || o.u` · 무변).
5. **저장 칸** = 옮긴 댓글에 `from` 더함 · 사본 `cs` 비움 · 그 밖 무변.
6. **근거**
   - 사용자 11/05 18:01 「앱 고치기 전에 단 댓글들엔 소급 적용 안 됐어? 143 번에서 근거 연결했는데 다른 문제에서 단 댓글 출처가 안 떠」 · 18:09 「지시서 써줘」.
   - 채팅이 원격 기록(18:01)에서 잰 것: 이어 둔 임자 41 · 출처 없는 임자 댓글 4 · 사본에만 남은 댓글 4 · 패치 판에서 옮김 4 · 남은 사본 0 · 143 번 칩 「G16-53-02」.
7. **화면 끝** = 첫 절 · 사용자 할 일.
9. **클라우드** = 관문 + 헛잣대만.
10. **더 빨리** = 채팅이 관문 두 엔진을 미리 돌려 FAIL 0.
13. **inbox** = 고정 가지.
14. **세 줄** = 18:1x 사용자에게 먼저 보냄.
15. **과목** = 지학 · 생물 같은 함수(`CARD_LAYER`) · 물리 = `g3CsMig` 가 `CARD_LAYER` 로 막힘 · 칩 처리는 이어 둔 항목이 있을 때만.
