# _task_cmn_1106 — 자과(지학 · 생물) · 민법OX: 근거 하나당 댓글 개수 한도(20) 없앰 [클라우드 · 작은 고침 · 앱 둘 · main push 한 번]

**화면에서 달라지는 것**: 한 근거에 댓글이 20 개 차도 더 달린다(카드 「댓」 칸 · 지문 점 댓글 · 이어 둔 근거에서 단 댓글 · 민법 연결 상자 댓글). 「댓글은 한 근거에 20개까지」 안내 · 지문 점 댓글이 조용히 안 저장되던 것 없어짐. **글자 한도(근거 4,000 자 · 댓글 하나 2,000 자) 그대로.** 저장 꼴 · 동기화 길 무변.

- 판 크기 = 작음(앱 둘 · 각 패치 1 쌍 · 새 파일 0 · 짤 것 0 · 관문 = 자과 공용 `_qa_small_gate.py` · 민법 = 이 폴더 `ox_gate.py`(jn_cm_1105 판 그대로))
- 로컬 필요 = 0
- 시간 = ≈6 분(선례 jagwa_popme_1106 · jn_cm_1105 두 앱 한 판 18 분 · 이 판 관문 자과 0.4 분 · 민법 0.5 분)

## 할 일(차례대로 · 이것만)
0. WebKit 을 세운다(이 저장소 CLAUDE.md 「WebKit」 절). 잰 결과를 커밋 글 첫 줄에 적는다.
1. `git fetch origin main cloud/inbox` · 바탕 = main **4e5cc52**(`jagwa/index.html` LF md5 **2e4f70f6** · `minbeop/index.html` **9139bf75** · `_qa/_qa_apply_patches.py` **b8887814** · `_qa/_qa_small_gate.py` **867625c3**) — 다르면 멈추고 커밋 없이 이 줄만 알림(main 이 두 앱을 안 건드린 커밋만 앞섰으면 그대로 간다).
2. `cloud/inbox` 의 `_qa/cloud_batch/cmn_1106/` 에서 다섯을 꺼냄: `jagwa_patches.txt`(md5 c04e46b5) · `ox_patches.txt`(md5 20c80162) · `spec_cn.json`(md5 87b417a0) · `spec_cnox.json`(md5 8a1200ff) · `ox_gate.py`(md5 3e563659).
3. 바탕 둘을 떠 둠: `git show origin/main:jagwa/index.html > /tmp/base_jagwa.html`. 그다음
   - `python _qa/_qa_apply_patches.py jagwa_patches.txt jagwa/index.html --expect a9dcf1d5` → 1,659,275 B · 인라인 스크립트 5 문법 0
   - `python _qa/_qa_apply_patches.py ox_patches.txt minbeop/index.html --expect ed4e306b` → 1,243,724 B · 인라인 스크립트 7 문법 0(둘 다 채팅이 잼). 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문(데이터 = `git clone --depth 1 https://github.com/zzikkaplan/studyplandata` · 받기만 · 쓰기 0):
   - 자과: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python _qa/_qa_small_gate.py --spec spec_cn.json --new jagwa/index.html --base /tmp/base_jagwa.html --spd <클론> --eng chromium,webkit --base-eng chromium` — 칸 4 · yard 3(바탕 FAIL) · 무변 1(글자 한도 · 바탕 PASS).
   - 민법: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python ox_gate.py --spec spec_cnox.json --new minbeop/index.html --base 4e5cc52 --spd <클론> --eng chromium,webkit --base-eng chromium` — 칸 3 · yard 2 · 무변 1.
   - 시험 댓글 20 개는 명세가 메모리에 지어 넣는 글(「관문 시험 댓글 n」 · 원격 쓰기 = 관문 가짜 200 · 기록 값 0).
   - 채팅 컨테이너에서 같은 명령: 자과 새 판 크롬 4/4 · 웹킷 4/4 · 바탕 3 FAIL · 1 PASS · FAIL 0 · 0.4 분 / 민법 새 판 3/3 × 두 엔진 · 바탕 2 FAIL · 1 PASS · FAIL 0 · 0.5 분.
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시. 앱 결함이면 고치지 말고 칸 이름과 값만 알림.
5. 회귀 사슬 · grep 회귀 안 돌림(작은 고침 · 바뀐 것 = 상수 한 줄씩).
6. 커밋 하나(`jagwa/index.html` · `minbeop/index.html`)를 만들고 **genie main 에 fast-forward push**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님) · 커밋 글 = WebKit 줄 · 관문 합계 줄 둘 · 앱 md5 둘 · 단계별 분. push 가 막히면 지정 가지에 올리고 그 사실만 알림.
- 지킬 것: 공개 저장소 — 커밋 글에 기록 값 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(채팅이 검수 뒤 걷음). `ox_gate.py` 를 main 에 넣지 않음.
- 사용자 할 일 = 모든 기기에서 자과 서재 · 민법OX 새로고침 한 번.

## 패치가 하는 일(앱마다 1 쌍)
1. 자과 `var GG_TMAX=4000, GG_CMAX=2000, GG_CN=20;` → `GG_CN=Infinity` (2e4f70f6 → a9dcf1d5). 쓰는 자리 넷(ggReply 두 길 · g3JmSave 두 길) 그대로 · 한도에 안 닿음.
2. 민법 `const GG_TMAX = 4000, GG_CMAX = 2000, GG_CN = 20;` → `GG_CN = Infinity` (9139bf75 → ed4e306b). 쓰는 자리 둘(ggReply · ggRefReply) 그대로.

## 점검표(채팅)
1. **일꾼** = 클라우드(앱 파일 둘). 2. **차례** = 한 판 · 「~뒤」 없음. 3. **회귀** = 없음(작은 고침 · 무변 칸 = 글자 한도).
4. **선례** = jn_cm_1105(두 앱 한 판 · ox_gate.py) · jagwa_popme_1106(명세 꼴) · 9/15 결정 「글자 한도는 둔다(파일이 커지면 동기화가 길어짐)」 = 글자 한도 그대로.
5. **저장 칸** = 무변. 6. **근거** = 사용자 11/06 15:11 「근거 하나당 댓글 개수 제한 왜 둔 거야」 · 15:17 「제안이 뭔데」 · 15:20 「민법 앱도 같이 바꿔줘」. 채팅이 잰 것: 개수 20 = 근거 없이 민법에서 옮긴 값 · 지학 기록 댓글 66 개 18,659 B · 한 근거 최대 16.
7. **화면 끝** = 첫 줄 · 사용자 할 일. 9. **클라우드** = 관문 + 헛잣대만. 10. **더 빨리** = 채팅이 관문 두 엔진을 미리 돌려 FAIL 0.
13. **inbox** = 고정 가지. 14. **세 줄** = 15:2x 사용자에게 먼저 보냄. 15. **과목** = 자과 세 과목 같은 상수(물리도 한도 없어짐 · 물리 근거 댓글 꼴 무변).
