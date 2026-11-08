# _task_jagwa_cpic_1108 — 자과 물리: Claude 창을 열면 그림이 바로 보이게(555 번) [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(자과 물리 · 문제 창 「Claude」 단추)
1. 555 번에서 「Claude」 를 누르면 창 머리(「555번 Claude 풀이」 · 코드 줄) 바로 아래에 그림이 곧바로 보인다. 「▶ 모션」 같은 단추를 한 번 더 누르지 않는다.
2. 그림은 답풀 창 그림과 같은 꼴(`.solz` 틀 · `img.solpic` · 두 손가락 · Ctrl+휠 확대 · 두 번 톡 = 처음 크기 = `solxZoom`).
3. 어느 문항에 그림을 띄울지는 `jagwa/motion/index.json` 의 새 칸 `"pic":{"phys":[555]}` 로 정한다. 그림 파일 = `jagwa/img/claude/<과목>_<번호>.jpg`(카드 층 과목은 uid).
- 「pic」 에 없는 문항 · 「▶ 모션」(72 · 97 · 지학 넷) · Claude 풀이 글 읽기 · 고치기 · 저장 = 그대로. 기록 · 동기화 길 무변.

- 판 크기 = 작음(앱 패치 1 쌍 · 새 파일 1(`jagwa/img/claude/phys_555.jpg` = inbox base64 두 조각을 이어 풂) · 바꾸는 자원 1(`jagwa/motion/index.json` = inbox 판으로 갈음) · 짤 것 0 · 관문 = 공용 `_qa_small_gate.py`)
- 로컬 필요 = 0
- 시간 = ≈7 분(선례 jagwa_jmown_1106 · csmig 「보냈어」 → main 5 분 · 이 판 관문 크롬 + 바탕 크롬 = 2.0 분)

## 할 일(차례대로 · 이것만)
0. WebKit 을 세운다(이 저장소 CLAUDE.md 「WebKit」 절). 잰 결과를 커밋 글 첫 줄에 적는다.
1. `git fetch origin main cloud/inbox` 로 바탕을 맞춘다.
   - 바탕 = origin/main(채팅이 잰 때 **06ac7e1**).
   - 맞출 값: `jagwa/index.html` LF md5 **4ff30587**(1,661,511 B) · `jagwa/motion/index.json` md5 **5bbd4e7a** · `jagwa/img/claude/` 없음.
   - 다르면 멈추고 커밋 없이 이 줄만 알린다(main 이 jagwa 를 안 건드린 커밋만 앞섰으면 그대로 간다).
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_cpic_1108/` 에서 다섯을 꺼낸다: `app_patches.txt`(md5 e3dec6bc) · `spec_cpic.json`(md5 7907409b) · `index.json`(md5 00a6b571) · `phys_555.jpg.b64.1`(64a5a446) · `phys_555.jpg.b64.2`(ea66fd98).
   - 그림 = 두 조각을 차례로 이어 base64 풀기: `cat phys_555.jpg.b64.1 phys_555.jpg.b64.2 | base64 -d > jagwa/img/claude/phys_555.jpg`(폴더 새로) → md5 **ebeddc72**(52,385 B · 993×534). 다르면 멈춘다.
   - `index.json` 을 `jagwa/motion/index.json` 에 덮어쓴다(옛 칸 그대로 + `"pic":{"phys":[555]}`).
3. 바탕 앱을 한 벌 떠 둔다: `git show origin/main:jagwa/index.html > /tmp/base_jagwa.html`. 그다음 `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect 504c6a7b` → 1,662,543 B. 멈추면(종료 2 · 3) 그 줄만 알린다.
4. 관문을 돌린다: `GENIE_ROOT=<이 클론> PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python _qa/_qa_small_gate.py --spec spec_cpic.json --new jagwa/index.html --base /tmp/base_jagwa.html --spd <클론> --eng chromium,webkit --base-eng chromium`
   - `GENIE_ROOT` 를 이 클론으로 준다(관문 서버가 `motion/index.json` · `img/claude/` 를 거기서 읽는다 · 안 주면 `~/Documents/genie` 를 찾아 모션 목록이 빈다).
   - `--spd` = `git clone --depth 1 https://github.com/zzikkaplan/studyplandata`(받기만 · 쓰기 0). `--base` 는 **파일 경로**로 준다.
   - 명세 = 화면 3(물리 PC 555 · 폰 555 · PC 72) · 칸 5. `yard: true` 3 칸(PC 그림 보임 · 그림 자리 · 폰 그림 창 폭 안)은 바탕에서 FAIL 이어야 하고, `yard: false` 2 칸(555 「▶ 모션」 안 섬 · 72 = 그림 없고 「▶ 모션」 그대로)은 바탕도 PASS 여야 한다.
   - 채팅 컨테이너에서 같은 명령(크롬만): 새 판 5/5 PASS · 바탕 헛잣대 3 FAIL · 무변 2 PASS · 합계 FAIL 0 · 2.0 분. 웹킷은 채팅 컨테이너에 없어 안 잼.
   - 앱 결함이면 고치지 말고 칸 이름과 값만 알린다.
5. 회귀 사슬 · grep 회귀는 안 돌린다(작은 고침).
6. 커밋 하나(`jagwa/index.html` · `jagwa/img/claude/phys_555.jpg` · `jagwa/motion/index.json`)를 만들고, **genie main 에 fast-forward push**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님).
   - 커밋 글 = WebKit 줄 · 관문 합계 줄 · 앱 md5 · 단계별 분.
   - push 가 막히면 지정 가지에 올리고 그 사실만 알린다.
- 지킬 것:
  - 공개 저장소다. 커밋 글에 기록 값을 넣지 않는다.
  - `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않는다(채팅이 검수 뒤 걷음).
- 사용자 할 일 = 모든 기기에서 자과 서재를 새로고침 한 번.

## 패치가 하는 일(1 쌍 · 채팅이 4ff30587 에 넣어 504c6a7b)
1. `gptSheet`(Claude 창) — 창을 붙인 바로 뒤 `motLoad()` 가 끝나면 `MOT.pic[SUBJ_ID]` 에 이 문항(물리 = 번호 · 카드 층 = uid)이 있을 때 `#gpMotBox` 앞에 `.gppic` 틀 하나(`.solz` + `img.solpic` src = `img/claude/<과목>_<번호>.jpg`)를 넣고 `solxZoom` 을 건다.
   - 찾는 기준 = `host`(#gpBody) — PC 는 곁창(shFloat)이 판을 옮겨 처음 `b` 가 떨어지므로 `host.parentNode` 로 찾는다(채팅 첫 판이 `b` 로 찾다가 PC 칸 FAIL · 고침).
   - 이미 있으면 다시 안 넣음 · 그림이 목록에 없으면 아무것도 안 함 · 잘못되면 콘솔 한 줄.

## 점검표(채팅)
1. **일꾼** = 클라우드(앱 파일 + 그림 + 모션 목록 · 커밋 하나).
2. **차례** = 한 판 · 「~뒤」 없음.
3. **회귀** = 없음(작은 고침 · 관문 5 칸 × 두 엔진 + 바탕).
4. **선례**
   - jagwa_jmown_1106(작은 고침 지시서 · 명세 꼴) · E008(10/4 · Claude 칸 그림 = 「▶ 모션」 iframe) · 답풀 창 `ansSheet`(`.solz` · `img.solpic` · `solxZoom`) · 그림 바이트 = 채팅 커넥터가 글만 올려서 base64 조각으로 inbox(사용자 손 0 · 사용자 18:49 「cmd 더블클릭 시키지 마」).
   - 그림 = 보낸 그림을 JPEG 품질 75 로 다시 저장(160,143 → 52,385 B · 993×534 그대로 · 채팅이 글씨 자리 확대해 봄).
   - Claude 창 그림 자리 전수 = `gptSheet` 하나(세 과목 같은 함수 · 물리 = 옛 꼴 #gpMotBar · 카드 층 = #gpSub).
5. **저장 칸** = 무변(motion/index.json = 자원 파일 · 「pic」 칸은 옛 앱이 안 읽음).
6. **근거**
   - 사용자 11/08 18:15 그림 붙여 「물리 555 번 답풀에 올려줘」 · 18:20 「그럼 클로드로 올리는 건?」 · 18:28 「▶ 모션 없이 클로드 누르면 바로 저 그림 · 지시서」.
   - 채팅이 잰 것: 555 = PEQ0804 · 볼트 풀이 노트 번호 0 · Claude 글 없음(phys 기록 gpt 키 = 72 · 97) · motion/index.json = phys [72, 97].
7. **화면 끝** = 첫 절 · 사용자 할 일.
9. **클라우드** = 관문 + 헛잣대만.
10. **더 빨리** = 채팅이 관문(크롬 + 바탕)을 미리 돌려 FAIL 0.
13. **inbox** = 고정 가지.
14. **세 줄** = 18:3x 사용자에게 먼저 보냄.
15. **과목** = 세 과목 같은 함수 · 이번 목록은 물리 555 하나 · 지학 · 생물은 목록이 없어 무변.
