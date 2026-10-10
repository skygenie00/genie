# _task_jg_g3tx_1010 — 자과 물리 근거 줄: Shift+Enter 문단 나눔이 보일 때도 나뉘게

[클라우드] 한 판 · 줄 = jagwa(`jagwa/index.html` 한 파일) · 가지 = 이 가지 `cloud/jg_g3tx_1010`(바탕 genie main 4ce28d0) · 커밋 하나 · push

## 첫 줄 — 이게 끝나면 무엇이 달라지는가
물리 문항 근거 줄(트리거 · 공식 · 기타 세 칸)에 Shift+Enter 로 문단을 나눠 쓴 글이 저장 뒤 보일 때도 그 자리에서 줄이 나뉘어 보인다(지금은 한 줄로 붙어 보임 · 사용자 10/10 13:29).

## §0 잰 것(채팅 · genie 4ce28d0 소스 읽기 · 앱 안 띄움)
1. 저장 = 줄바꿈이 남음: `g3Push` · `ggAdd0` 의 `rows.map(...).join('\n')` · 고치기 칸 `g3EditInline` 은 Enter = 저장 · Shift+Enter = 줄바꿈(`!e.shiftKey`).
2. 보이기 = `g3ChipHTML`(12224 · 12226 줄 근처) `<span class="g3tx">` + `ggMath(ggFlat(g))` · CSS `.g3it .g3tx{flex:1;min-width:0;word-break:break-word;color:#2B3138}` 에 `white-space:pre-wrap` 없음 → \n 이 빈칸으로 뭉개짐. 같은 앱 다른 근거 칸(`.ggrr .t` · `.ggpan .hd .t` · `#gguw .gguh .gg`)은 pre-wrap 있음.
3. 짐작 = CSS 한 줄. 착수 때 실제로 띄워 재고, `ggMath` 가 \n 을 지우거나 바꾸는지도 본다(지우면 그 자리도).

## §A 할 일
1. 물리 근거 줄 글(`.g3tx` · 그 밖에 g3 글을 `ggFlat` 로 그리는 자리 전수 — 착수 때 grep `g3tx|ggFlat(`)이 줄바꿈을 보이게(`white-space:pre-wrap` 또는 같은 뜻) · 첫 줄 높이 · 칩 줄 맞춤 · 단추(👥 · 💬 · ✕) 자리는 한 줄 글일 때 지금과 같게.
2. 고치기 칸(`g3EditInline` textarea)에 그 글을 다시 열면 줄바꿈 그대로(지금도 그럴 것 · 잼).
3. 지학 · 생물 · 다른 화면 무변.

## §B 관문(새 하네스 `jagwa/_harness_jagwa_g3tx.py` · Chromium PC 1100 + 폰 390 hasTouch · 헛잣대 = 4ce28d0)
1. 물리 문항 하나에 근거 글 「첫 문단(Shift+Enter)둘째 문단」 을 칸 셋 각각에 넣고 저장 → 보이는 줄에서 두 문단이 다른 줄(글 상자 줄 수 ≥2 · 둘째 문단 글의 top > 첫 문단 top) · 헛잣대 = 한 줄 FAIL.
2. 한 줄 글 = 바탕과 줄 높이 · 칩 · 단추 자리 같음(±1px).
3. 고치기 칸 다시 열기 = 줄바꿈 그대로.
4. 원격 PUT 막음 · 사본 기록만.
5. **캡처 PNG 넷**(사용자에게 보일 것 · `_qa/cloud_batch/shots_g3tx/`): 폰 390 · PC 1100 각각 바탕(붙어 보임) · 새 판(나뉘어 보임) — 근거 줄이 화면 가운데 보이게.

## §C 클라우드 규칙
- 바탕 = genie main 최신(착수 때 ls-remote · 4ce28d0 과 다르면 그 사이 커밋 보고 §0 다시) · 데이터 = add_repo(owner `zzikkaplan` · repo `studyplandata` · read) → `git clone --depth 1`.
- 회귀 사슬 안 돎 · Chromium 만 · WebKit 은 로컬 몫(꼬리에 적음).
- 커밋 하나 = 앱 + 관문 하네스 + 전수표 `_qa/_qa_chain_list.json` 한 줄 + 캡처 PNG 넷 · 커밋 글 = 단계별 분 · 관문 표 · 다르게 한 것.
- 개인 문항 · 해설 글을 커밋 글 · 하네스 출력 · 캡처에 옮기지 않는다(공개 저장소 · D11) — 캡처의 근거 글은 위 시험 글만 보이게(문항 지문 영역은 잘라 냄).

## §D 로컬(Code) 몫 — 합치기
가지가 올라오면: 합치기 → WebKit 칸(같은 하네스 · 폰) → 회귀 = 근거 줄을 재는 하네스만(grep `g3tx|g3ChipHTML` · 공용 층 아님 → 전체 아님 · 규칙 ★★ 10/10) → push · Pages · 인도 줄(사용자 확인: 폰 · PC 자과 새로고침 → 물리 근거 줄에 Shift+Enter 로 두 문단 → 저장 뒤 두 줄로 보임).
