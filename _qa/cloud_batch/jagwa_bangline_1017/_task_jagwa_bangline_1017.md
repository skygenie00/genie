# _task_jagwa_bangline_1017 — 자과 물리: ! 누른 근거 왼쪽 붉은 세로선(문제 창 · 서랍 작은 창) [클라우드 · 작은 고침 · main push 한 번]

**화면에서 달라지는 것**(근거 세 칸): 문제 창 근거 줄에서 ! 를 켠 줄 = 왼쪽 끌기 세로선(.g3dh)이 회색 → 붉은색 · ! 를 켜고 끄면 그 자리에서 바로 바뀜(ggBangPaint · data-gbbox) · 목차 서랍 작은 창(#g3Pop) 근거 목록에서 ! 켠 근거 = 왼쪽 붉은 세로선 3px. 저장 칸 무변.

- 판 크기 = 작음(앱 패치 5 · 짤 것 0)
- 로컬 필요 = 0
- 시간 = ≈5 분(선례 = jagwa_twcount_1015 착수 → push 4 분 · 관문 6 칸)

## 할 일(차례대로 · 이것만)
1. `git fetch origin main cloud/inbox` · 바탕 = main **d3472b0**(`jagwa/index.html` LF md5 **e119fb30** · `_qa/_qa_small_gate.py` md5 **867625c3**) — 다르면 멈추고 커밋 없이 이 줄만 알림.
2. `cloud/inbox` 의 `_qa/cloud_batch/jagwa_bangline_1017/` 에서 둘을 꺼냄: `app_patches.txt`(md5 1fb2929f) · `spec_bangline.json`(7b43ab30).
3. `python _qa/_qa_apply_patches.py app_patches.txt jagwa/index.html --expect f16103c2` — 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문: `python _qa/_qa_small_gate.py --spec spec_bangline.json --new jagwa/index.html --base d3472b0 --eng chromium,webkit --base-eng chromium`(`--vendor` · `--spd` · `--notes` 는 지난 판과 같이).
   - 명세 = 채팅 시안(PC · 폰 6 칸) 그대로 · setup 이 115 근거 둘(트리거 ! 켬 · 주의점 끔)을 메모리에만 넣음(저장 안 함 · 사용자 기록 무변) · 바탕 d3472b0 = 6 칸 다 FAIL(`yard: true`) — 시안 거울로 새 6/6 PASS · 바탕 6 FAIL 잼.
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시(통째 다시 금지). 앱 결함이면 고치지 말고 칸 이름 · 값만 알림.
5. 회귀 사슬 · grep 회귀 안 돌림(작은 고침).
6. 커밋 하나(`jagwa/index.html`) · main 이 바탕 그대로면 fast-forward push · 커밋 글 = 관문 결과 줄 그대로(PASS/FAIL · 엔진 · 바탕) · 앱 md5 · 단계별 분.
- 지킬 것: 공개 저장소 — 시험 글은 명세 안 글뿐 · 사용자 기록 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(파일은 채팅이 검수 뒤 지움 · 가지는 그대로 · 가지 지울 일 없음). `jagwa/theory_fix.json` 은 건드리지 않음.
- 사용자 할 일 = 앱 새로고침 한 번.

## 패치가 하는 일(5 쌍 · 채팅이 e119fb30 에 넣어 f16103c2 · 1,601,757 B · 인라인 스크립트 문법 오류 0 잼)
1~2. `g3ChipHTML` 두 줄(공식·개념 · 트리거/주의점) — 줄 div 에 `g.bang` 이면 class `bang` · `data-gbbox="uid|k"`(있던 ggBangPaint 가 [data-gbbox] 의 bang class 를 그 자리에서 뒤집음).
3~4. `g3PopToggle` 근거 목록(공식·개념 블록 줄 · 트리거/주의점 줄) — 같은 class `bang` · `data-gbbox`.
5. CSS — `.g3f .g3list .g3r.bang .g3dh::before{background:var(--red)}` · `#g3Pop .g3pf .it.bang{border-left:3px solid var(--red);padding-left:5px}`.

## 점검표(채팅)
1. 일꾼 = 클라우드 · 2. 한 판 · 3. 회귀 = 없음(작은 고침) · 4. 선례 = 옛 근거 판 `.ggpan.bang{border-left:3px solid var(--red)}`(지금도 앱 안) · ggBangPaint 의 [data-gbbox] 길 · 5. 저장 칸 무변 · 6. 근거 = 사용자 10/17 14:56 「! 누르면 원래 왼쪽 세로선도 빨개졌었어 · 세로선 붉은색 · 목차 서랍 작은 창에서도 ! 누른 근거는 왼쪽에 붉은 세로선」 · 10. 더 빨리 = 공용 관문 + 시안 명세 · 13. inbox.
