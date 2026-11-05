# _task_jagwa_jmown_1106 — 자과 지학 · 생물: 근거 임자 문항 지문에 다른 문항 지문 댓글이 「댓」 으로 뜨는 것 고침 [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(자과 지학 · 생물 카드 층 · 지문 오른쪽 점)
1. 근거 임자 문항(다른 문항이 이어 둔 근거를 가진 문항)에서, 다른 문항이 제 지문을 골라 단 댓글(임자 근거 `cs` 에 `from` = 그 문항)이 이 문항 같은 열쇠 지문(①… · ㄱ…)의 「댓」 으로 뜨던 것이 없어진다. 「댓」 = 이 문항이 단 지문 댓글(`from` 없음 또는 이 문항)이 있는 자리만.
2. 그 지문 점을 눌러 여는 밑 칸(`.jmbox`)의 근거 밑 댓글 줄(`.jmc`)도 같은 거름.
- 근거 상자 · 작은 창 · 정리 창에 다른 문항 댓글이 출처 칩과 같이 보이는 것은 그대로. 이어 둔 문항 쪽(`from` 으로 이미 거름)도 그대로. 저장 값 · 동기화 길 무변.

- 판 크기 = 작음(앱 패치 2 쌍 · 새 파일 0 · 짤 것 0 · 관문 = 공용 `_qa_small_gate.py`)
- 로컬 필요 = 0
- 시간 = ≈7 분(선례 jagwa_csmig_1105 「보냈어」 18:21 → main 18:26 · 5 분 · 이 판 관문 크롬 · 웹킷 + 바탕 크롬 = 1.9 분)

## 할 일(차례대로 · 이것만)
0. WebKit 을 세운다(이 저장소 CLAUDE.md 「WebKit」 절). 잰 결과를 커밋 글 첫 줄에 적는다.
1. `git fetch origin main cloud/inbox` 로 바탕을 맞춘다.
   - 바탕 = origin/main(채팅이 잰 때 **dfaa7f2**).
   - 맞출 값: `jagwa/index.html` LF md5 **50a0853e** · `_qa/_qa_apply_patches.py` · `_qa/_qa_small_gate.py` = dfaa7f2 판.
   - 다르면 멈추고 커밋 없이 이 줄만 알린다(main 이 jagwa 를 안 건드린 커밋만 앞섰으면 그대로 간다).
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_jmown_1106/` 에서 둘을 꺼낸다: `app_patches.txt`(md5 e8377ea9) · `spec_jmown.json`(md5 263f5c43).
3. 바탕 앱을 한 벌 떠 둔다: `git show origin/main:jagwa/index.html > /tmp/base_jagwa.html`. 그다음 `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect 1d7f214d` → 1,658,673 B · 인라인 스크립트 5 개 문법 0(채팅이 잼). 멈추면(종료 2 · 3) 그 줄만 알린다.
4. 관문을 돌린다: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python _qa/_qa_small_gate.py --spec spec_jmown.json --new jagwa/index.html --base /tmp/base_jagwa.html --spd <클론> --eng chromium,webkit --base-eng chromium`
   - `--spd` = `git clone --depth 1 https://github.com/zzikkaplan/studyplandata`(받기만 · 쓰기 0 · 채팅이 잰 판 d54216e). `--base` 는 **파일 경로**로 준다.
   - 명세 = 화면 3(PC 둘 · 폰 하나) · 칸 5. `yard: true` 3 칸은 바탕에서 FAIL 이어야 하고, `yard: false` 2 칸(근거 상자 출처 칩 · 이어 둔 문항 제 「댓」)은 바탕도 PASS 여야 한다.
   - 칸은 데이터에 있는 문항을 쓴다(G11-48-09 · G20-57-01 · G17-54-02). 잣대는 그 문항 기록에서 「댓」 이어야 할 자리를 그때 세어 화면과 맞댄다(값 박지 않음). 클론이 바뀌어 setup ERR 이나 FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시 돌린다. 앱 결함이면 고치지 말고 칸 이름과 값만 알린다.
   - 채팅 컨테이너에서 같은 명령: 새 판 크롬 5/5 · 웹킷 5/5 PASS · 바탕 크롬 헛잣대 3 FAIL · 무변 2 PASS · 합계 FAIL 0 · 1.9 분.
5. 회귀 사슬 · grep 회귀는 안 돌린다(작은 고침).
6. 커밋 하나(`jagwa/index.html`)를 만들고, **genie main 에 fast-forward push**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님).
   - 커밋 글 = WebKit 줄 · 관문 합계 줄 · 앱 md5 · 단계별 분.
   - push 가 막히면 지정 가지에 올리고 그 사실만 알린다.
- 지킬 것:
  - 공개 저장소다. 커밋 글에 기록 값(근거 · 댓글 글 · 수)을 넣지 않는다.
  - `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않는다(채팅이 검수 뒤 걷음).
- 사용자 할 일 = 모든 기기에서 자과 서재를 새로고침 한 번.

## 패치가 하는 일(2 쌍 · 채팅이 50a0853e 에 넣어 1d7f214d)
1. `jmHasCm`(지문 「댓」 판정): 이 문항 근거 `g.cs` 를 셀 때 `from` 없음 또는 이 문항인 댓글만(이어 둔 쪽 `s.cs` 의 `from === 이 문항` 거름은 그대로).
2. `g3JmBox` 안 `jmc`(밑 칸 근거 밑 댓글 줄): 이어 두지 않은 근거의 `g.cs` 에 같은 거름.

## 점검표(채팅)
1. **일꾼** = 클라우드(앱 파일 하나).
2. **차례** = 한 판 · 「~뒤」 없음.
3. **회귀** = 없음(작은 고침 · 관문 5 칸 × 두 엔진 + 바탕).
4. **선례**
   - jagwa_csmig_1105(dfaa7f2 · 명세 꼴 · 「이어 둔 쪽은 from 으로 거름」 꼴을 임자 쪽에도) · jn_cm_1105(지문 점 · `jmHasCm` · `g3JmBox` 처음 넣은 판).
   - 지문 댓글 읽는 자리 전수 = `jmHasCm` · `g3JmBox` jmc · `ggCsHTML` · `g3PopCsHTML`(뒤 둘 = 근거 상자 · 작은 창 · 정리 창 = 출처 칩 달고 다 보이는 자리 · 무변).
5. **저장 칸** = 무변.
6. **근거**
   - 사용자 11/06 02:10 「지학 198 번 댓글 달지도 않은 지문에 왜 『댓』」 · 02:12 「지시서 써줘」.
   - 채팅이 원격 기록(02:08)에서 잰 것: 거짓 「댓」 문항 5(서랍 143 · 144 · 156 · 184 · 198) · 198 = 다른 문항 다섯이 단 지문 댓글 9 · 198 이 단 것 0.
7. **화면 끝** = 첫 절 · 사용자 할 일.
9. **클라우드** = 관문 + 헛잣대만.
10. **더 빨리** = 채팅이 관문 두 엔진을 미리 돌려 FAIL 0.
13. **inbox** = 고정 가지.
14. **세 줄** = 02:1x 사용자에게 먼저 보냄.
15. **과목** = 지학 · 생물 같은 함수(카드 층) · 물리 = 지문 점 없음(무변).
