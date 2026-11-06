# _task_jagwa_popme_1106 — 자과 지학 · 생물: 목차서랍 작은 창 · 📋 정리 창 근거 밑 댓글 = 그 문제에서 단 댓글만 [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(자과 지학 · 생물 · 목차서랍 O X 작은 창 · 📋 정리 창의 근거 줄 밑 댓글 = `g3PopCsHTML`)
1. 그 문제에서 단 댓글만 보인다 — 이어 둔 근거(`g.src` = 임자)면 임자 근거 `cs` 중 `from` = 이 문제인 것 + 이 문제 사본 `cs` · 제 근거면 `from` 없음(제 것) 또는 이 문제인 것.
2. 다른 문제에서 단 댓글 · 임자 문항 제 댓글은 여기서 빠진다(출처 칩도 없음 · 다 제 것).
- 카드 근거 상자(`g3ChipHTML` · 다른 문제 댓글이 출처 칩과 다 보임) · 지문 「댓」 · 저장 값 · 동기화 무변. 이은 개념(cqx) 댓글 칸 무변.

- 판 크기 = 작음(앱 패치 1 쌍 · 새 파일 0 · 짤 것 0 · 관문 = 공용 `_qa_small_gate.py`)
- 로컬 필요 = 0
- 시간 = ≈5 분(선례 jagwa_jmown_1106 「보냈어」 02:34 → main 02:38 · 4 분 · 이 판 관문 크롬 · 웹킷 + 바탕 크롬 = 1.6 분)

## 할 일(차례대로 · 이것만)
0. WebKit 을 세운다(이 저장소 CLAUDE.md 「WebKit」 절). 잰 결과를 커밋 글 첫 줄에 적는다.
1. `git fetch origin main cloud/inbox` 로 바탕을 맞춘다.
   - 바탕 = origin/main(채팅이 잰 때 **61f8bda**).
   - 맞출 값: `jagwa/index.html` LF md5 **1d7f214d** · `_qa/_qa_apply_patches.py` **b8887814** · `_qa/_qa_small_gate.py` = 61f8bda 판.
   - 다르면 멈추고 커밋 없이 이 줄만 알린다(main 이 jagwa 를 안 건드린 커밋만 앞섰으면 그대로 간다).
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_popme_1106/` 에서 둘을 꺼낸다: `app_patches.txt`(md5 9874cb0e) · `spec_popme.json`(md5 335e677f).
3. 바탕 앱을 한 벌 떠 둔다: `git show origin/main:jagwa/index.html > /tmp/base_jagwa.html`. 그다음 `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect 2e4f70f6` → 1,659,041 B · 인라인 스크립트 5 개 문법 0(채팅이 잼). 멈추면(종료 2 · 3) 그 줄만 알린다.
4. 관문을 돌린다: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python _qa/_qa_small_gate.py --spec spec_popme.json --new jagwa/index.html --base /tmp/base_jagwa.html --spd <클론> --eng chromium,webkit --base-eng chromium`
   - `--spd` = `git clone --depth 1 https://github.com/zzikkaplan/studyplandata`(받기만 · 쓰기 0 · 채팅이 잰 판 642ce9a). `--base` 는 **파일 경로**로 준다.
   - 명세 = 화면 4(PC 셋 · 폰 하나) · 칸 6. `yard: true` 5 칸은 바탕에서 FAIL 이어야 하고, `yard: false` 1 칸(제 댓글만 있는 문항 = 그대로)은 바탕도 PASS 여야 한다.
   - 칸은 데이터에 있는 문항을 쓴다(G11-48-09 · G20-57-01 · G02-39-07). 잣대는 그 문항 기록에서 「그 문제에서 단 댓글」 수를 그때 세어 화면과 맞댄다(값 박지 않음). 클론이 바뀌어 setup ERR 이나 FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시 돌린다. 앱 결함이면 고치지 말고 칸 이름과 값만 알린다.
   - 채팅 컨테이너에서 같은 명령: 새 판 크롬 6/6 · 웹킷 6/6 PASS · 바탕 크롬 헛잣대 5 FAIL · 무변 1 PASS · 합계 FAIL 0 · 1.6 분.
5. 회귀 사슬 · grep 회귀는 안 돌린다(작은 고침).
6. 커밋 하나(`jagwa/index.html`)를 만들고, **genie main 에 fast-forward push**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님).
   - 커밋 글 = WebKit 줄 · 관문 합계 줄 · 앱 md5 · 단계별 분.
   - push 가 막히면 지정 가지에 올리고 그 사실만 알린다.
- 지킬 것:
  - 공개 저장소다. 커밋 글에 기록 값(근거 · 댓글 글 · 수)을 넣지 않는다.
  - `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않는다(채팅이 검수 뒤 걷음).
- 사용자 할 일 = 모든 기기에서 자과 서재를 새로고침 한 번.

## 패치가 하는 일(1 쌍 · 채팅이 1d7f214d 에 넣어 2e4f70f6)
1. `g3PopCsHTML` 의 댓글 모음: 임자 근거 `s.cs` 는 `(c.from || 임자) === 이 문제` 만 · 제 `g.cs` 는 `(c.from || 이 문제) === 이 문제` 만 · 보일 때 `from` 비움(출처 칩 없음). 이은 개념 칸 · 그리기 꼴 무변.
- 11/05 csmig 판의 「작은 창 · 정리 창 = 출처 없는 옛 임자 댓글에 임자 ID 칩」 은 이 판에서 빠진다(임자 댓글 자체가 작은 창에서 빠지므로 · 카드 근거 상자의 칩은 그대로).

## 점검표(채팅)
1. **일꾼** = 클라우드(앱 파일 하나).
2. **차례** = 한 판 · 「~뒤」 없음.
3. **회귀** = 없음(작은 고침 · 관문 6 칸 × 두 엔진 + 바탕).
4. **선례**
   - jagwa_jmown_1106(90bd89b · from 거름 · 명세 꼴) · jagwa_csmig_1105(dfaa7f2 · 이 함수에 임자 ID 칩 넣은 판).
   - `g3PopCsHTML` 부르는 자리 전수 = 서랍 작은 창(g3Pop) · 📋 정리 창(jnRowHTML `ggmine`) 둘.
5. **저장 칸** = 무변.
6. **근거**
   - 사용자 11/05 00:20 「목차서랍에서 그 근거 연결에 댓글 단 문제에서는 그 댓글도 보이게」 · 00:52 「정리 목록 창에서도 그 문제에서 댓글 단 건 그 문제 밑에」 · 11/06 11:20 「목차서랍 작은 창에서 원래 자기 문제에서만 단 댓글만 보이게 하랬는데 왜 다 보여」.
   - 채팅이 원격 기록(11:19)에서 잰 것: 작은 창에 댓글이 뜨는 문항 54 중 44 문항이 다른 문제 댓글까지 보임.
7. **화면 끝** = 첫 절 · 사용자 할 일.
9. **클라우드** = 관문 + 헛잣대만.
10. **더 빨리** = 채팅이 관문 두 엔진을 미리 돌려 FAIL 0.
13. **inbox** = 고정 가지.
14. **세 줄** = 11:2x 사용자에게 먼저 보냄.
15. **과목** = 지학 · 생물 같은 함수(카드 층) · 물리 = 작은 창 댓글 줄 없음(무변).
