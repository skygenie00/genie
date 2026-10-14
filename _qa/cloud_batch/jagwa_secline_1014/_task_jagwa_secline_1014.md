# _task_jagwa_secline_1014 — 자과 물리: 옛 개별 단원 파일블록 줄도 통짜 「물리 목차」 글로 + 수식 안 \\ 한 줄 [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(물리): 근거 「공식·개념」 칸에 처음부터 뜨는 줄(문항 노트 임베드가 가리키는 옛 개별 단원 파일블록) · 서랍 작은 창 · 그 줄을 넣은 뒤 개념 창이 옛 개별 파일 사본 글 대신 **통짜 「물리 목차」 글**(theory_fix.json 반영)로 나옴. 예) PA1603 「(1) 탄성충돌」 → 「반발계수e=1 (e쓰면 운E보존쓴거)」 · 「② 강체 각운동량 : L=Iω」 한 줄. 수식 안 `\\`(환경 밖)는 옵시디언처럼 한 줄.
짝짓기는 새로 짜지 않음 — 앱에 이미 있는 점선 짝(g3SecMark 의 개별 블록 ↔ 통짜 줄 맞댐)을 함수 하나(g3SecHit)로 떼어 점선 · 근거 줄 · 작은 창 · 넣은 뒤 개념 창이 같이 씀. 맞댈 때 `\\` 는 뺌(볼트 `\\I` → `I` 고친 뒤에도 짝). 시안 거울로 잰 짝 = 143 중 138(나머지 5 = 통짜에 같은 줄이 없어 옛 글 그대로).

- 판 크기 = 작음(앱 패치 5 · 짤 것 0)
- 로컬 필요 = 0
- 시간 = ≈6 분(선례 = jagwa_cqjoin_1014 착수 → push 5 분 · 관문 8 칸)

## 할 일(차례대로 · 이것만)
1. `git fetch origin main cloud/inbox` · 바탕 = main **c5a3b3a**(`jagwa/index.html` LF md5 **951a9bff** · `jagwa/theory_fix.json` 있음 · `_qa/_qa_small_gate.py` md5 **867625c3**) — 다르면 멈추고 커밋 없이 이 줄만 알림.
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_secline_1014/` 에서 둘을 꺼냄: `app_patches.txt`(md5 ac85c6f2) · `spec_secline.json`(1127ddc9).
3. `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect 1cfa31d7` — 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문: `python _qa/_qa_small_gate.py --spec spec_secline.json --new jagwa/index.html --base c5a3b3a --eng chromium,webkit --base-eng chromium`(`--vendor` · `--spd` · `--notes` 는 지난 판과 같이).
   - 명세 = 채팅 시안(PC · 폰 8 칸) 그대로 · 바탕 c5a3b3a = 6 칸 FAIL(`yard: true`) · 「환경 안 \\」 2 칸은 바탕도 PASS(`yard: false`) — 시안 거울로 새 8/8 PASS · 바탕 6 FAIL 잼.
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(통째 다시 금지). 앱 결함이면 고치지 말고 칸 이름 · 값만 알림.
5. 회귀 사슬 · grep 회귀 안 돌림(작은 고침).
6. 커밋 하나(`jagwa/index.html`) · main 이 바탕 그대로면 fast-forward push · 커밋 글 = 관문 결과 줄 그대로(PASS/FAIL · 엔진 · 바탕) · 앱 md5 · 단계별 분.
- 지킬 것: 공개 저장소 — 시험 글은 명세 안 글뿐 · 사용자 기록 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(파일은 채팅이 검수 뒤 지움 · 가지는 그대로 · 가지 지울 일 없음). `jagwa/theory_fix.json` 은 건드리지 않음.
- 사용자 할 일 = 앱 새로고침 한 번.

## 패치가 하는 일(5 쌍 · 채팅이 951a9bff 에 넣어 1cfa31d7 · 1,598,697 B · 인라인 스크립트 문법 오류 0 잼)
1. `kxNL` — 환경(`\begin`) 밖 `\\` 를 빈칸으로 · `katex.renderToString` · `katex.render` 감쌈(근거 줄 g3K · 자동 그리기 kx 같은 길).
2. `g3SecMark` 앞머리 → `g3SecHit(secId,id)`(옛 짝 그대로 떼어냄 · 맞댐 정규화에서 `\\` 를 `\` 로 바꾸던 것 → 뺌) + `g3SecLines(H)`(짝 범위의 글 · 그림 줄) · `g3SecMark` 는 그것을 부름.
3. `g3SecMark` 의 짝 계산 두 줄 → `H.all` 쓰기(점선 범위 = 옛과 같음).
4. `g3CqBody` — 짝이 있으면 통짜 줄(들임 · 그림 포함)로 그림 · 없으면 옛 글.
5. `g3Blocks` — 찾기 블록과 짝 못 지은 옛 개별 단원 파일블록(넣으면 근거 · 개념 창 줄)도 글은 통짜 줄로(열쇠 무변).

## 점검표(채팅)
1. 일꾼 = 클라우드 · 2. 한 판(inbox 의 jagwa_kxnl_1014 를 이 판으로 갈음 · kxNL 같이 듦) · 3. 회귀 = 없음(작은 고침) · 4. 선례 = 앱 점선 짝 g3SecMark(10/12 15:3x) 그대로 씀 · 5. 저장 칸 무변(넣은 근거 글은 넣을 때 통짜 글로 저장 · 옛에 넣은 것은 그대로) · 6. 근거 = 사용자 22:01 「앱에서 고친 게 안 보일 거면 내가 왜 통짜를 고치겠냐」 · 22:20 「이 짝짓기 세 번째」 · 10. 더 빨리 = 공용 관문 + 시안 명세 · 13. inbox.
