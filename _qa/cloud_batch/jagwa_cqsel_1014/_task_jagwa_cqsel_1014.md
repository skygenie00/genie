# _task_jagwa_cqsel_1014 — 자과 물리: 교재에 이어 둔 개념 줄도 개념 창에서 줄마다 고르기 [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(물리): 근거 공식·개념 칸의 교재에 이어 둔 개념 줄(예 PA1603 「(1) 탄성충돌」)을 눌러 뜬 개념 창에서 줄 누름 = 고름 · 다시 누름 = 뺌(블록 찾기로 넣은 줄과 같은 꼴 · 옅은 청록) · 고른 줄만 근거 줄 · 서랍 작은 창에(창 차례 · 그림 줄도) · 다 빼면 옛 그대로 블록 통째 · 이 문항만 · 기기끼리 맞춤(동기화 통 cqx).

- 판 크기 = 작음(앱 패치 4 · 짤 것 0)
- 로컬 필요 = 0
- 시간 = ≈8 분(선례 = jagwa_pnframe_1014 착수 → push 6 분 · 관문 16 칸 3.1 분 → 이번 10 칸)

## 할 일(차례대로 · 이것만)
1. `git fetch origin main cloud/inbox` · 바탕 = main **1a7a3da**(`jagwa/index.html` LF md5 **68ac80fb** · `_qa/_qa_small_gate.py` md5 **867625c3**) — 다르면 멈추고 커밋 없이 이 줄만 알림.
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_cqsel_1014/` 에서 둘을 꺼냄: `app_patches.txt`(md5 571d8873) · `spec_cqsel.json`(b2ba0270).
3. `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect f2d7df1c` — 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문: `python _qa/_qa_small_gate.py --spec spec_cqsel.json --new jagwa/index.html --base 1a7a3da --eng chromium,webkit --base-eng chromium`(`--vendor` · `--spd` · `--notes` 는 지난 판과 같이).
   - 명세 = 채팅 시안(PC · 폰 10 칸) 그대로 · 바탕 1a7a3da = 10 칸 다 FAIL(`yard: true`).
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(통째 다시 금지). 앱 결함이면 고치지 말고 칸 이름 · 값만 알림 · 「누를 점이 가려짐」 · 「누를 것 없음」 = 명세 탓 → 진단만 적고 명세 손대지 않음.
5. 회귀 사슬 · grep 회귀 안 돌림(규칙 (96) ④ 작은 고침 · (85)).
6. 커밋 하나(`jagwa/index.html`) · main 이 바탕 그대로면 fast-forward push · 커밋 글 = 관문 결과 줄 그대로(PASS/FAIL · 엔진 · 바탕) · 앱 md5 · 단계별 분.
- 지킬 것: 공개 저장소 — 시험 글은 명세 안 글뿐 · 사용자 기록 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(파일은 채팅이 검수 뒤 지움 · 가지는 그대로 둠 · 가지 지울 일 없음). `jagwa/theory_fix.json` 은 건드리지 않음.
- 사용자 할 일 = 앱 새로고침 한 번.

## 패치가 하는 일(4 쌍 · 채팅이 68ac80fb 에 넣어 f2d7df1c · 1,596,743 B · 인라인 스크립트 문법 오류 0 잼)
1. 쌍 1 — `g3UseWinQ`(이은 개념 줄 누름 = 개념 창) 끝에 `g3CqSelWire(uid,ck)`(쓰인 문항 목록 창은 뺌).
2. 쌍 2 — `g3CqSel` · `g3CqBodyU` · `g3CqSelWire` 새 함수: 고른 줄 = 문항 칸 cqx[qk].s[개념 열쇠](볼트 글 줄 · 그림 'G:이름' · 창 차례) · 누름 = 켬/끔 → `g3CqxSave` · 다시 그림 · 블록 찾기로 넣은 줄 고르기(g3SelWire)와 같은 손 · 같은 CSS.
3. 쌍 3 · 4 — 근거 줄(g3CqHTML) · 서랍 작은 창(g3Pop 이은 개념 줄) = 고른 줄이 있으면 그 줄만 · 없으면 옛 그대로(g3CqBody).

## 점검표(채팅)
1. 일꾼 = 클라우드 · 2. 한 판 · 3. 회귀 = 없음(작은 고침 (96) ④) · 4. 선례 = 블록 찾기로 넣은 줄 고르기(10/10 g3SelWire · 10/14 그림 줄) · 이은 개념 칸 저장(cqx · 10/14 g3drag 칸 o) · 5. 저장 칸 = cqx 칸 안 새 열쇠 s(이미 동기화되는 통) · 6. 근거 = 사용자 18:46 「근거에서 왜 줄마다 선택 안 돼 · PA1603」 · 원격 기록 P123 「(3) 원운동」 고른 줄 9 · P110 · P115 「(1) 탄성충돌」 고른 줄 8 = 그 개념 줄에서 고르던 흐름 · 실제 앱 1a7a3da P156 이은 줄 누름 = 개념 창 g3sel 없음 잼 · 10. 더 빨리 = 공용 관문 + 시안 명세 · 채팅은 클라우드 관문 안 돌림 · 13. inbox · 15. 과목 맞춤 = 물리만(이은 개념 CB = 물리 · 지학 · 생물은 g3UseWinQ 첫 줄에서 돌아감).
