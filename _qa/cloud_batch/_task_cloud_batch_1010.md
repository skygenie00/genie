# _task_cloud_batch_1010 — 클라우드 세션 하나 몫(앱 고침 · 관문 · 차례로 둘) · 로컬은 조판기 · tt 고침 + 합치기 · 회귀

(10/10 00:4x 고침 — 사용자 00:36 「클라우드 세션 하나만」 · 규칙 68 · 00:5x 다시 고침: 자과 판은 로컬로 — 클라우드는 ① 민법 한 판만)

이 파일과 지시서 셋은 genie 가지 `cloud/batch_1010` 의 `_qa/cloud_batch/` 에 있다(로컬 Code 가 올림). 클라우드는 N: 을 못 본다 — 지시서 안 `N:\…` 자리는 genie `_qa/…` 같은 자리로 읽는다 · 데이터 = add_repo(owner `zzikkaplan` · repo `studyplandata` · read) → `git clone --depth 1`.

## 클라우드 규칙(지시서 본문보다 먼저)
1. 바탕 = genie main **최신**(착수 때 ls-remote · 지시서 §0 의 7299ec3 와 앱 md5 다르면 그 사이 커밋을 보고 §0 다시 잼).
2. 몫 = 지시서 §A(고침) + §B(관문 하네스 + 헛잣대 + 화면 훑기) 만 · **회귀 사슬 안 돎**(로컬이 합칠 때 한 번) · Chromium 만(터치 = CDP `Input.dispatchTouchEvent`) · WebKit 칸은 「로컬 몫」 으로 꼬리에 적음.
3. 판마다 새 가지 · 커밋 하나(앱 + 그 판 관문 하네스 `_qa/<앱>/_harness_….py` + 전수표 `_qa/_qa_chain_list.json` 한 줄) · push · 커밋 글 = 단계별 분 · 관문 표(새 판 PASS/FAIL · 헛잣대 FAIL 수) · 지시서와 다르게 한 것.
4. 개인 문항 · 해설 글을 커밋 글 · 하네스 출력에 옮기지 않는다(공개 저장소 · D11).

## 클라우드 ① — 민법 한 판(가지 `cloud/ox_batch_1010`)
한 커밋에 셋: ① `_task_search_all.md` 의 **민법 몫**(runSearch · linkSearch · lwFind · runSearchOmr) ② `_task_ox_queue_compare.md`(⚡ 채점 창 지난 결과 · 계속 틀림 · 극복함 = 마지막 지난 결과 · §B-2 실데이터 기대값 그대로) ③ **연결한 근거 줄 폰 꼴** — `ggRefRowHTML` 본문 줄 · 댓글 줄: 줄 `flex-wrap` · 글 덩어리 `flex:1 1 18rem;min-width:0` · 「✎ 여기서 고치기」 `ml-auto`(폰 = 글 한 폭 · 단추 아랫줄 오른쪽 · PC 넓으면 한 줄) = 같은 앱 `ggPanelHTML`(10/6 ox_gg_phone) 꼴 그대로 · 관문: 폰 390 · PC 1100 연결한 근거 펼침 — 글 폭 ≥ 줄 폭 90 %(폰) · 단추 누를 자리 ≥ 36 · 겹침 0 · 누름 = 고치기 칸 열림 · 헛잣대 7299ec3(폰 글 폭 ≈ 반).

## (로컬 몫으로 옮김) 자과 한 판 — 클라우드는 하지 않는다
가지 `cloud/jagwa_batch_1010` — ① `_task_search_all.md` 의 **자과 몫**(esSearch · linkSheet · ggFindRun) ② 연결한 근거 줄 폰 꼴 — `.ggrr` · `.ggrc2` 를 `flex-wrap` · `.t{flex:1 1 18rem;min-width:0}` · `.lk{margin-left:auto}`(클라우드 ① ③ 과 같은 잣대) ③ **물리 문항 창 머리 단추 손가락 누를 자리 30px** — 겉모양(22px) 무변 · `(pointer:coarse)` 에서만 서재 · ▾ · 시계 · ⤢ · ◀ · ▶ 둘레 투명 누를 자리 30px(머리 줄 높이 · 이웃 단추와 누를 자리 겹침 0 · 머리 밖 본문 안 덮음) · 근거 = 10/7 `_task_jagwa_phys_win` §A-04 · 관문 = 폰 · iPad 폭에서 여섯 누를 자리 ≥ 30 · 겹침 0 · 머리 그림 = 바탕 7299ec3 과 같음.

## 로컬(Code)이 직접 고칠 둘(클라우드 몫 아님 · 하위 에이전트 · 브라우저는 자리 나는 대로)
1. 조판기 — `_task_search_all.md` 의 **조판기 몫**(ggFindRun · mbSearchRun · c2EditWin · popJimun · 착수 grep 더함).
2. tt — tt 작은 판: 보는 날짜를 바꾸는 함수 전수(grep `curDate`)에서 「이날기록추가」 시각 칸 `mA` · `mB` 의 쓰던 글 기억(draftDrop) 지우고 칸 비움 · 다른 칸 기억 무변 · 관문: 시각 넣고 저장 안 누름 → 날짜 바꿈 = 두 칸 빔 · 그 날짜로 돌아와도 빔 · 저장한 기록 무변 · share Text 기억 그대로 · 헛잣대 = 바탕(남음 FAIL).

## 로컬(Code) 몫 — 지시서 셋 §C 그대로
클라우드 가지(① 민법)가 올라오면(ls-remote) 합치기 → WebKit 칸 → 그 앱 회귀(지시서 회귀 줄 · 검색 · 채점 · 근거 하네스만 · 자과는 qa_fix1 고친 하네스 바탕 위 compare) → push → Pages. 그동안 브라우저 = post7299(qa_fix1 고친 하네스로 자과 전체 한 번 · 00:15 줄) → qa_fix1 나머지.
