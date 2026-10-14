# _task_jagwa_thpic_ndtitle_1014 — 자과: 물리 근거에 통짜 물리목차 그림 넣기 · 목차 서랍 줄 길게 = 제목 고치기(세 과목) [클라우드 · 작은 고침 10 분 꼴 · main push 한 번]

**화면에서 달라지는 것**: (물리) 근거 공식·개념 칸 찾기 목록에 그 블록 그림이 작게 같이 뜸 · 넣은 근거 줄 누름 = 개념 창 · 그림 누름 = 그 그림 고르기(다시 누름 = 뺌) → 근거 줄에 그림 · 안 고르면 옛 그대로 블록 첫 글 줄 · 옛 근거 열쇠 무변. (세 과목) 목차 서랍 줄 어디를 길게 눌러도 그 줄 제목 고치는 칸 · 카드 층(지학 · 생물)은 옛 꼬리(「2024년 자과 21번」 · 지학 기출 = 없음) 자리에 칸이 뜸 · 저장 = 새 제목만(파랑) · 문제 창 머리 제목 같이 · 그만두면 옛 그대로.

- 판 크기 = 작음(패치 12 · 짤 것 0)
- 로컬 필요 = 0
- 시간 = ≈12 분(선례 = jagwa_link_why_1013 착수 → push 12 분 · 같은 공용 관문 · 명세 칸 18)

## 할 일(차례대로 · 이것만)
1. `git fetch origin main cloud/inbox` · 바탕 = main **317fea7**(`jagwa/index.html` LF md5 **8e2cf21a**) — 다르면 멈추고 커밋 글 없이 이 줄만 알림.
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_thpic_ndtitle_1014/` 에서 둘을 꺼냄: `_task_jagwa_thpic_ndtitle_1014_patches.txt` · `spec_thpic_ndtitle.json`.
3. `python _qa/_qa_apply_patches.py <patches.txt> jagwa/index.html --expect 32fd1f26` — 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문: `python _qa/_qa_small_gate.py --spec <spec_thpic_ndtitle.json> --new jagwa/index.html --base 317fea7 --eng chromium,webkit --base-eng chromium`(`--vendor` · `--spd` · `--notes` 는 지난 판과 같이).
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(통째 다시 금지). 앱 결함이면 고치지 말고 칸 이름 · 값만 알림 · 하네스 쪽 흔들림(누를 것 없음 · 늦게 뜸)이면 그 칸 `wait` 만 늘려 한 번 더.
   - 명세 칸 = 채팅 시안 둘(6cmgyKxyw4Jc1B3MzGaYCk v1 · MNtSVYqCikJJYJLh9pKyA3 v2) 점검 18 칸 그대로 · 세 과목 · PC 마우스 · 폰 손가락 · 길게 · Enter 저장 · 헛잣대(바탕 317fea7 = 다 FAIL).
5. 회귀 사슬 · grep 회귀 안 돌림(규칙 (96) ④ 작은 고침 · (85)).
6. 커밋 하나(`jagwa/index.html`) · main 이 바탕 그대로면 fast-forward push · 커밋 글 = 관문 결과 줄 그대로(PASS/FAIL · 엔진 · 바탕) · 앱 md5 · 단계별 분.
- 지킬 것: 공개 저장소 — 시험 글은 명세 안 지어낸 글뿐 · 사용자 기록 0. `cloud/inbox` 가지 · 그 폴더는 건드리지 않음(채팅이 검수 뒤 걷음). `jagwa/theory_fix.json` 은 건드리지 않음.
- 사용자 할 일 = 앱 새로고침 한 번.

## 패치가 하는 일(12 쌍 · 채팅이 8e2cf21a 에 넣어 32fd1f26 · 1,580,965 B · 인라인 스크립트 다섯 문법 오류 0 잼)
1. 근거 2 칸 찾기 블록(g3Blocks · 통짜 THEORY)에 그림만 있는 줄도 담음 — 앞 글 줄 블록 · 블록 첫머리면 다음 글 줄과 · 블록 번호 n 무변(옛 근거 열쇠 그대로) · 블록 글 = 글 줄만(옛 그대로)(쌍 1 · 2).
2. `g3Img` · `g3CText`(고른 줄 'G:그림' = 그림 · 안 고르면 블록 첫 글 줄) · `g3BlkLines`(찾기 목록에 그림)(쌍 3 · 4).
3. secHTML 그림 상자 `data-bx="G:그림"` · 개념 창 고르기 = `[data-bx]`(그림 누름 = 고르기 · g.t 엔 그림 이름 안 넣음)(쌍 5~8) · CSS(쌍 9 · 10).
4. 길게 누름 SEL 에 `#ndList .ndrow .ndt` · fire = 카드 층 줄 옛 꼬리 자리에 `.ndtt` 칸 → ndEdit · 끝나면 ndTitlePaint(쌍 11 · 12).

## 점검표(채팅)
1. 일꾼 = 클라우드 · 2. 한 판(겹치는 자리 0) · 3. 회귀 = 없음(작은 고침 (96) ④) · 4. 선례 = 개념 창 줄 고르기(10/10 18:30 g3SelWire) · 서랍 제목 고치기(ndEdit · iedOpen) · 5. 저장 칸 무변(근거 g.sl · TFIX PN_SLOT) · 6. 근거 = 사용자 10/14 10:12 · 10:13 「고쳐」 · 11:16 · 시안 댓글 11:21 · 10. 더 빨리 = 공용 관문 + 시안 명세 · 채팅은 관문 안 돌림 · 회귀 0 · 13. inbox · 14. 뺀 것 = 하네스 새로 짜기 · 관문 통째 다시 · 회귀 · 15. 과목 맞춤 = 그림 = 물리만(통짜 목차는 물리) · 서랍 = 세 과목.
