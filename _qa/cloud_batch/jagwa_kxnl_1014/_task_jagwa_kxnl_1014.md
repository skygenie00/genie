# _task_jagwa_kxnl_1014 — 자과 물리: 수식 안 \\ 줄바꿈 = 옵시디언처럼 한 줄 [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(물리): 볼트 글 `$L=\\I\omega$` · `$\\I=mr^2$` 처럼 수식 안에 `\\` 가 든 줄(교재 개념 16 곳)이 근거 줄 · 서랍 작은 창에서 「L =」 / 「Iω」 두 줄로 떨어지던 것 → 옵시디언처럼 한 줄(「L=Iω」). `\begin{aligned}` 같은 환경 안 `\\`(줄 나눔)는 그대로.

- 판 크기 = 작음(앱 패치 1 · 짤 것 0)
- 로컬 필요 = 0
- 시간 = ≈6 분(선례 = jagwa_cqjoin_1014 착수 → push 5 분 · 관문 8 칸 3.0 분 → 이번 6 칸)

## 할 일(차례대로 · 이것만)
1. `git fetch origin main cloud/inbox` · 바탕 = main **c5a3b3a**(bffcf20 + theory_fix.json 만 바뀜 · `jagwa/index.html` LF md5 **951a9bff** · `_qa/_qa_small_gate.py` md5 **867625c3**) — 다르면 멈추고 커밋 없이 이 줄만 알림.
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_kxnl_1014/` 에서 둘을 꺼냄: `app_patches.txt`(md5 b4c3df53) · `spec_kxnl.json`(10aad335).
3. `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect da1c14ba` — 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문: `python _qa/_qa_small_gate.py --spec spec_kxnl.json --new jagwa/index.html --base bffcf20 --eng chromium,webkit --base-eng chromium`(`--vendor` · `--spd` · `--notes` 는 지난 판과 같이).
   - 명세 = 채팅 시안(PC · 폰 6 칸) 그대로 · 바탕 bffcf20 = 「근거 줄 L=Iω 한 줄」 2 칸 FAIL(`yard: true`) · 나머지 4 칸 바탕도 PASS(`yard: false` · 시안 거울로 잼).
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(통째 다시 금지). 앱 결함이면 고치지 말고 칸 이름 · 값만 알림.
5. 회귀 사슬 · grep 회귀 안 돌림(규칙 (96) ④ 작은 고침 · (85)).
6. 커밋 하나(`jagwa/index.html`) · main 이 바탕 그대로면 fast-forward push · 커밋 글 = 관문 결과 줄 그대로(PASS/FAIL · 엔진 · 바탕) · 앱 md5 · 단계별 분.
- 지킬 것: 공개 저장소 — 시험 글은 명세 안 글뿐 · 사용자 기록 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(파일은 채팅이 검수 뒤 지움 · 가지는 그대로 · 가지 지울 일 없음). `jagwa/theory_fix.json` 은 건드리지 않음.
- 사용자 할 일 = 앱 새로고침 한 번.

## 패치가 하는 일(1 쌍 · 채팅이 951a9bff 에 넣어 da1c14ba · 1,597,055 B · 인라인 스크립트 문법 오류 0 잼)
- `function kx(el){` 앞에 `kxNL`(환경 `\begin` 이 없으면 `\\` → 빈칸) · `katex.renderToString` · `katex.render` 를 한 번 감쌈(KaTeX 늦게 뜨면 50ms 마다 기다림) = 근거 줄(g3K) · 자동 그리기(kx · auto-render) 같은 길. 실제 앱(bffcf20 · P156 「② 강체 각운동량」) 에 같은 감쌈을 넣어 잼: 줄 높이 39.6 → 19.8px · 줄바꿈 1 → 0.

## 점검표(채팅)
1. 일꾼 = 클라우드 · 2. 한 판 · 3. 회귀 = 없음(작은 고침 (96) ④) · 4. 선례 = 옵시디언 MathJax(환경 밖 \\ 무시) · 5. 저장 칸 무변 · 6. 근거 = 사용자 21:31 그림 「② 강체 각운동량 : L = / Iω 왜 이렇게 떨어져 있어」 · 볼트 `1.5.14. 각운동량 보존법칙.md` 3 줄 `$L=\\I\omega$` 잼 · 교재 개념 CB 16 곳 · 개별 파일 11 곳 · 10. 더 빨리 = 공용 관문 + 시안 명세 · 13. inbox · 15. 과목 맞춤 = 세 과목 같은 KaTeX 감쌈(지학 · 생물 수식에 \\ 있는지는 안 잼 · 있으면 같이 한 줄).
