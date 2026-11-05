# _task_jn_cm_1105 — 자과 지학 · 생물 근거 · 지문 · 서랍 손질 + 민법OX 정리 창 근거 댓글 · 공유 [클라우드 · 작은 고침 둘 · main push 한 번]

**화면에서 달라지는 것**
- **자과 지학 · 생물(카드 층)**
  1. 목차 서랍: 지학은 절마다 첫 소단원 머리에, 생물은 머리마다 📋 를 둔다. 누르면 그 절 📋 정리 창이 뜬다(첫 화면 절 머리 📋 와 같은 창).
  2. 「근거」 를 누르면 공식 · 계산 · 함정 · 개념 한 줄이 뜬다(트리거 · 주의점 줄 없음). 고른 유형은 「근거」 뒤와 서랍 그 문제 줄에 글자로 보인다.
  3. 선택지는 한 줄에 하나씩, 줄마다 O△X 를 단다. 〈보기〉 ㄱㄴㄷ 에 O△X 가 있는 문항은 옛 꼴 그대로 둔다. 지문에 △ 가 하나라도 있으면 회독 기록은 그대로 두고, 서랍 그 회독 시간 왼쪽에 작은 노란 △ 만 단다.
  4. 서랍 번호 = 그 갈래(기출/확인문제) 전체를 단원 차례로 늘어놓은 자리다. 거름이나 회차 차례를 바꿔도 번호가 그대로다. 문항 창 제목 · 비교 창 · 찾기 결과 · 코멘트 「N번」 · 연결/쌍둥이 · 답 곁창 · 개념 창 칩 · 쌍둥이 번호 입력도 같은 번호를 쓴다. 속 번호와 기록 열쇠(uid)는 바뀌지 않는다.
  5. 근거를 펴면 「댓」 을 안 눌러도 달린 댓글이 보인다. 다른 문항 댓글 줄에도 끌기 세로줄과 「!」 가 붙는다.
  6. 지문(선택지 · 〈보기〉) 오른쪽에 점 • 을 둔다. 누르면 그 줄 밑에 칸이 열리고, 근거 첫 줄을 골라 바로 댓글을 단다. 댓글에는 그 지문(`jm` · `jt`)이 같이 저장되고 점은 「댓」 으로 바뀐다. 댓글의 지문을 누르면 O/X(`jo`)를 고른다.
  7. 옛 🔗 연결(GGREF)은 동기화가 끝난 뒤 한 번만 스스로 근거 찾기 항목(`g.src` = 임자)으로 옮겨진다. 임자 근거가 없는 연결은 남긴다.
- **민법OX**
  1. 정리 창 근거 줄마다 그 근거의 댓글(↳ 글 + 단 문항 ID)이 보인다.
  2. 문항 창 연결 상자에서는 이 문항이 단 댓글에 테두리를 친다.
  3. 다른 문항 댓글 줄의 +/− 로 그 댓글을 이 문항에도 공유한다(`c.sh` 에 uid). 공유된 문항에서는 같은 파란 ID 로 보인다. 정리 창에서도 된다.
- 바뀌지 않는 것: 저장 파일 · 동기화 길 · 옛 칸. 더해지는 칸은 지학 댓글 `jm` · `jt` · `jo`, 선택지 O△X `BG[uid].c1…`, 민법 댓글 `sh` 뿐이다.

- 판 크기 = 중간(앱 둘 · 지학 패치 40 쌍 · 민법 패치 7 쌍 · 새 파일 0 · 짤 것 0 · 관문 = 공용 `_qa_small_gate.py` + 지난 판 `ox_gate.py`)
- 로컬 필요 = 0
- 시간 = ≈30 분(선례 jagwa_refcm_1105 「보냈어」 01:35 → main 01:47 · 12 분). 이 판 관문은 채팅 컨테이너 잰 값으로 지학 크롬 · 웹킷 + 바탕 크롬 = 15.3 분, 민법 = 3.4 분이다.

## 할 일(차례대로 · 이것만)
0. WebKit 을 세운다(이 저장소 CLAUDE.md 「WebKit」 절). 잰 결과를 커밋 글 첫 줄에 적는다.
1. `git fetch origin main cloud/inbox` 로 바탕을 맞춘다.
   - 바탕 = origin/main(채팅이 잰 때 **67b5f8e**).
   - 맞출 값: `jagwa/index.html` LF md5 **ef6b6c7e** · `minbeop/index.html` **c18d4878** · `_qa/_qa_apply_patches.py` **b8887814** · `_qa/_qa_small_gate.py` **867625c3**.
   - 다르면 멈추고, 커밋 없이 이 줄만 알린다(main 이 두 앱을 안 건드린 커밋만 앞섰으면 그대로 간다).
2. `cloud/inbox` 의 `_qa/cloud_batch/jn_cm_1105/` 에서 다섯 파일을 꺼낸다:
   - `jagwa_patches.txt`(md5 d8bc8905)
   - `spec_jn.json`(f14b7b73)
   - `ox_patches.txt`(58338359)
   - `spec_oxjn.json`(fcd0a5df)
   - `ox_gate.py`(3e563659 = ox_csdrag_1103 과 같음)
3. 바탕 앱을 한 벌 떠 둔다: `git show origin/main:jagwa/index.html > /tmp/base_jagwa.html`. 그다음 패치를 넣는다.
   - `python _qa/_qa_apply_patches.py jagwa_patches.txt jagwa/index.html --expect 6879004a` → 1,656,705 B · 인라인 스크립트 5 개 문법 0(채팅이 잼).
   - `python _qa/_qa_apply_patches.py ox_patches.txt minbeop/index.html --expect 9139bf75` → 1,243,490 B · 인라인 7 개 문법 0.
   - 멈추면(종료 2 · 3) 그 줄만 알린다.
4. 관문 둘을 돌린다(`--spd` = `git clone --depth 1 https://github.com/zzikkaplan/studyplandata` · 받기만 · 쓰기 0 · 채팅이 잰 판 35b57a3).
   - 지학 · 생물:
     `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python _qa/_qa_small_gate.py --spec spec_jn.json --new jagwa/index.html --base /tmp/base_jagwa.html --spd <클론> --eng chromium,webkit --base-eng chromium`
     - `--base` 는 **파일 경로**로 준다.
     - 명세 = 화면 14(PC 7 · 폰 7) · 칸 53. `yard: true` 46 칸은 바탕에서 FAIL 이어야 하고, `yard: false` 7 칸은 바탕도 PASS 여야 한다. 무변 칸 = 펜 켬 · 머리 이름 누름 · 〈보기〉 O△X 문항 옛 꼴 둘 · 「댓」 상자 하나 · 거름 켜도 번호 그대로 · 생물 제목 번호.
     - 옮김 칸(p7 · m7)은 앱이 동기화 뒤 스스로 옮기기를 기다린다(가짜 원격 · 최대 40 초). 「남은 🔗 은 임자 근거 0 인 것뿐 · 근거 찾기 항목 30 넘게」 와 G23-60-06 칸을 잰다.
     - 채팅 컨테이너에서 같은 명령: 새 판 크롬 53/53 · 웹킷 53/53 PASS · 바탕 크롬 헛잣대 46 FAIL · 무변 7 PASS · 합계 FAIL 0 · 15.3 분.
   - 민법:
     `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python ox_gate.py --spec spec_oxjn.json --new minbeop/index.html --base origin/main --spd <클론> --eng chromium,webkit --base-eng chromium`
     - 명세 = 화면 8 · 칸 13. `yard: true` 10 칸 · 무변 3 칸(근거 글 상자 그대로 · 상자 펴기 둘).
     - 채팅 컨테이너에서 같은 명령: 새 판 26/26 PASS · 바탕 헛잣대 10 FAIL · 무변 3 PASS · 합계 FAIL 0 · 크롬 56.8 초 · 웹킷 64.9 초 · 바탕 75.3 초.
   - 명세 칸은 데이터에 있는 문항을 쓴다(G00-37-02 · G26-63-06 · G23-60-06 · B00-37-01 · Q1064 · Q0598 · Q4409). 클론이 그 뒤 바뀌어 setup ERR 이나 FAIL 이 나면, 그 칸만 `--only <칸 이름 앞머리>` 로 다시 돌린다. 앱 결함이면 고치지 말고 칸 이름과 값만 알린다.
5. 회귀 사슬 · grep 회귀는 안 돌린다(작은 고침 · 화면 칸이 바뀐 자리마다 관문 칸이 있음).
6. 커밋 둘(`jagwa/index.html` · `minbeop/index.html`)을 만들고, **genie main 에 fast-forward push 한 번**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님).
   - 커밋 글 = WebKit 줄 · 관문 결과 합계 줄 · 앱 md5 · 단계별 분.
   - push 가 막히면 지정 가지에 올리고 그 사실만 알린다.
- 지킬 것:
  - 공개 저장소다. 커밋 글에 기록 값(근거 · 댓글 글 · 수)을 넣지 않는다.
  - `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않는다(채팅이 검수 뒤 걷음).
  - `ox_gate.py` · 명세를 main 에 넣지 않는다.
- 사용자 할 일 = 모든 기기에서 자과 서재 · 민법OX 를 새로고침 한 번.

## 패치가 하는 일
**지학 · 생물(40 쌍 · 채팅이 ef6b6c7e 에 넣어 6879004a · 시안 KWmY9H47tGhuicw3GkoYBj v15 와 같음 · 시안만의 「자동 옮김 끔」 한 쌍은 뺌)** — 손대는 자리는 모두 `CARD_LAYER`(지학 · 생물)만이고 물리는 무변이다.
1. 서랍 📋
   - `navBuild` 소단원 머리에 `.ndjn`(지학 = 절마다 첫 소단원 · 생물 = 머리마다)을 둔다.
   - 창 capture 누름 → `jnOpen(sec)` 을 부르고 서랍 zIndex 를 되돌린다.
2. 근거 유형
   - `typeLbl` · `g3GgPop` 을 카드 층에도 켠다. 카드 층 작은 창은 유형 줄만 보인다(`g3TgHTML` 뺌).
   - 서랍 `.ndty` 는 `ndTail` 을 감싸서 단다.
3. 선택지 O△X
   - `CHOX = CARD_LAYER` · `.choices.chox` · `.row.chr[data-k=cN]` + `.ox`(저장 = `BG[uid].cN` · 회독마다 `nrCarryMem` 이 이력 `b` 로 옮김).
   - 〈보기〉 정오 있는 문항(`ox`)은 옛 꼴. 누름 묶기 = `button[data-c]`.
4. 서랍 △
   - `chHasQ` → `.ndm[data-q="△"]` · CSS `::before` 노랑 900 8px · 시간 `::after` 왼쪽.
5. 번호
   - `dnoFix()` = `shellSeq(listSort(DATA.filter(showKind)))` 차례로 고정 번호 `DNO` / `DNOR` 를 만든다.
   - `dispNo` / `dispRev` 를 서랍 `.ndno` · 문항 창 제목 · 비교 창 제목 · 찾기 `.nsn` · 코멘트 창 · 연결/쌍둥이 · 답 곁창 `.answ` · 개념 창 칩 · 쌍둥이 더하기 입력(`dispRev`) · `navBuild` 끝 열린 제목에 쓴다.
6. 근거 댓글
   - `g3ChipHTML`: 카드 층에 댓글이 있으면 읽기 상자 `.g3cmb.g3cmv` 를 바로 보인다. 「댓」 은 적는 칸까지.
   - `g3OtherCsHTML` 줄 = `data-ck/gk/guid` + `.ggcsdh` + `.ggcbg`.
   - `ggCsBang` / `ggCsMove` 는 지금 문항도 다시 그린다.
7. 옮김
   - `g3RefMig(only)` + `syncRecords` 감쌈 → 첫 동기화 성공 뒤 한 번(`did`) 옛 GGREF u→o 를 o 근거마다 `g3Push`(src 임자)로 넣고 🔗 를 걷는다.
   - 임자 근거가 0 인 연결은 남긴다.
8. 지문 점
   - `jmDotHTML` · `g3JmBox`(줄 밑 `.jmbox` · 근거 첫 줄 `.jmi` · `.jmin` Enter 저장 · Esc 닫기) · `g3JmSave`(ggReply 길 · src 이면 임자 cs 에 from).
   - `#card .jmbox,.jmdot` z-index 8(펜 덮개 `#qink` z6 위).
9. 지문 보이기
   - `ggCsHTML` / `g3PopCsHTML` 에 `.ggjt「jt」` + `.ggjo` 를 붙인다.
   - `.ggjt` 누름 → `.ggjox` O X → `g3JoSet`.

**민법(7 쌍 · c18d4878 → 9139bf75 · 시안 3jTnevfBkHwCHrubvEK5q8 v4 와 같음)**
1. `jnGgHTML(id,txt)`: 정리 창 근거 상자 → 근거 줄마다 ↳ 댓글 + from 칩 · 공유받은 댓글 「↳ 🔗u 글」 · `data-jngg`.
2. `ggRefRowHTML` 댓글 줄: from === 이 문항이거나 sh 에 들면 `.ggme`(파란 테두리 1.5px).
3. `.ggcsh` +/− → `ggCsShare(uid,u,k,ck,sc)`(c.sh 넣고 빼기 · `ggSaveList(u)` · 다시 그림 · `[data-jngg]` 갈음).
4. sh 칩 `.ggshid` = from 칩과 같은 파랑 · 「+」 글자 없음.

## 점검표(채팅)
1. **일꾼** = 클라우드(앱 파일 둘만 · N: 0).
2. **차례** = 한 판 두 앱(사용자 11:12 ~ 15:29 지학 시안 댓글 · 13:18 ~ 14:56 민법 시안 댓글 → 15:38 「지시서 써줘」 = 묶음) · 「~뒤」 없음(파일이 달라 서로 안 막음).
3. **회귀** = 없음(작은 고침 · 관문 66 칸 × 두 엔진 + 바탕).
4. **선례**
   - jagwa_refcm_1105(main 67b5f8e · 같은 근거 댓글 함수 · `_qa_small_gate.py` 명세 꼴) · ox_csdrag_1103(cdaa723 · `ox_gate.py` · 댓글 끌기).
   - 물리 근거 유형(typeLbl · g3GgPop)을 카드 층에 켬.
   - 첫 화면 절 머리 📋(jnChipHTML) 꼴 = 서랍([쓸모없음 306] 뒤 절마다 첫 소단원).
   - 민법 연결 상자(ggRefRowHTML) · 정리 창(jnRowHTML).
5. **저장 칸** = 지학 댓글 `jm` · `jt` · `jo` · `BG` cN · 민법 댓글 `sh` 를 더함 · 옛 칸 · 파일 · 동기화 무변 · 옮김 = 있던 GGREF 를 근거 찾기 항목으로(사용자 12:58 「① 로」).
6. **근거** = 사용자 11/05 11:12 · 11:24 · 11:31 · 11:41 · 12:15 · 12:17 · 12:21 · 12:27 · 12:29 · 12:31 · 12:35 · 12:55 · 12:58 · 13:18 · 14:01 · 14:10 · 14:28 · 14:31 · 14:49 · 14:56 · 15:05 · 15:29 「번호 유지」 · 15:38 「지시서 써줘」 · 시안 v15 · v4 시험 PASS(지학 51/52 · 남은 하나 = 시안 화면끼리 IndexedDB 를 같이 쓰는 흔들림 · 관문은 화면마다 따로라 PASS).
7. **화면 끝** = 첫 절 · 사용자 할 일.
9. **클라우드** = 관문 + 헛잣대만.
10. **더 빨리** = 채팅이 관문 두 엔진을 미리 돌려 FAIL 0 · 두 앱 한 세션.
13. **inbox** = 고정 가지.
14. **세 줄** = 15:3x 사용자에게 먼저 보냄.
15. **과목** = 지학 · 생물 둘 다 칸이 있음(p5 · m5) · 물리 = 손댄 함수가 `CARD_LAYER` 로 막힘 · 공용 댓글 함수 줄 꼴만(관문 밖).
