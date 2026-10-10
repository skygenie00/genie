# genie — Claude Code 세션 안내

## 지시서 이름만 오면(사용자 2026-10-10 15:26 · 16:21 · 16:58)

사용자 첫 말이 `_task_*.md` 이름(또는 이름만 · 「○○.md 클라우드 세션에 넘겨」 꼴)이면 그것이 지시서 이름이다.

1. 지시서 이름이 오면 **먼저 `git fetch origin` 하고 찾는다**(클론은 세션을 띄운 때 판이라 새 지시서가 아직 없을 수 있다).
2. 지시서 = `_qa/cloud_batch/<이름>` — **main 에는 없다.** 채팅이 판마다 임시 가지(`cloud/<판>`)에만 올린다.
   `git for-each-ref --sort=-committerdate --format='%(refname:short)' refs/remotes/origin/cloud` 의 차례로 `git show <가지>:_qa/cloud_batch/<이름>` 을 찾는다.
3. 없으면 멈추고 한 줄로 알린다 — 「`<이름>` 이 origin/cloud/* 어디에도 없음」. 짐작해서 하지 않는다.
4. 찾으면 그 지시서를 그대로 한다(push 자리 · 관문 · 헛잣대 · 회귀는 지시서 글대로).
5. 결과 = **커밋 글에만.** `_result.md` · 캡처 · 결과 파일을 main 에 넣지 않는다. 캡처가 필요하면 그 판의 임시 가지에만 올린다(채팅이 검수 뒤 가지째 지운다).
6. main 에 `_qa/cloud_batch/` 를 다시 만들지 않는다.

공개 저장소다 — 개인 기록 · 교재 글 · 결과 값에 사용자 기록이 섞인 것은 넣지 않는다(D11 · 시험 자료는 지어낸 값).

## WebKit(사용자 10/10 14:39 · 19:41 「클라우드에서도 WebKit」)

세션을 시작하거나 지시서를 받으면 맨 먼저 WebKit 을 세운다 — `ls -d /opt/pw-browsers/webkit-* ~/.cache/ms-playwright/webkit-*` → `~/.cache` 에만 있으면 `/opt/pw-browsers/` 에 같은 이름으로 `ln -s` · 둘 다 없으면 `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 -m playwright install --with-deps webkit` → `p.webkit.launch()` 로 잰 결과(버전 또는 오류 첫 줄)를 그 판 커밋 글 첫 줄에. 서면 터치·아이패드 관문은 WebKit 으로도 돈다(로컬로 넘기지 않음).
