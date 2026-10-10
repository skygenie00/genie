# genie — Claude Code 세션 안내

## 지시서 이름만 오면(사용자 2026-10-10 15:26 · `_qa/cloud_batch/_task_qa_bigguard_1010.md` §G)

사용자 첫 말이 `_task_*.md` 이름(또는 이름만 · 「○○.md 클라우드 세션에 넘겨」 꼴)이면 그것이 지시서 이름이다.

1. 지시서 이름이 오면 **먼저 `git fetch origin` 하고 찾는다**(클론은 세션을 띄운 때 판이라 새 지시서가 아직 없을 수 있다).
2. 지시서 = `_qa/cloud_batch/<이름>` — `origin/main` 에서 찾고, 없으면 가장 최근 `origin/cloud/*` 가지에서 찾는다
   (`git for-each-ref --sort=-committerdate --format='%(refname:short)' refs/remotes/origin/cloud` 의 차례 · `git show <가지>:_qa/cloud_batch/<이름>`).
3. 둘 다 없으면 멈추고 한 줄로 알린다 — 「`<이름>` 이 origin/main · origin/cloud/* 어디에도 없음」. 짐작해서 하지 않는다.
4. 찾으면 그 지시서를 그대로 한다(가지 · push 자리 · 관문 · 헛잣대 · 회귀는 지시서 글대로).
5. 결과 = 커밋 글 + 그 지시서 파일 옆 `_qa/cloud_batch/<이름>_result.md`(`<이름>` = `.md` 를 뺀 지시서 이름 · 예: `_task_qa_bigguard_1010_result.md`).

공개 저장소다 — 개인 기록 · 교재 글 · 결과 값에 사용자 기록이 섞인 것은 넣지 않는다(D11 · 시험 자료는 지어낸 값).
