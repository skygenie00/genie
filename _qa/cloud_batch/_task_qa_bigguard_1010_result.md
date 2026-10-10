# _task_qa_bigguard_1010 결과 — 큰 판 회귀의 낭비를 실행기가 스스로 막게 [클라우드 · 2026-10-10]

- WebKit(★ 맨 먼저): `playwright._impl._errors.Error: BrowserType.launch: Executable doesn't exist at /opt/pw-browsers/webkit-2215/pw_run.sh` (클라우드에 WebKit 없음 · 이 판은 브라우저를 안 씀)
- 바탕: genie main 43c09e0(착수 07:15 UTC ls-remote = 커밋 전 다시 잼 = 그대로) · 앱 파일 무접촉
- 바뀐 파일: `_qa/_qa_chain.py` · `_qa/_tools/`(새 넷: `qa_affected.py` · `shared_names.py` · `shared_names.json` · `_harness_qa_bigguard.py`) ·
  `_qa/_qa_chain_list.json`(관문 한 줄) · `_qa/_qa_sync.py`(_tools 셋을 모음에 · 4 줄) · `_qa/cloud_batch/` 이 파일 · 맨 위 `CLAUDE.md`(§G)

## 무엇이 달라졌나(실행기 기본값)

| 절 | 전 | 이제 |
|---|---|---|
| A 다시 돌기 | `run` 은 늘 돎(`--reuse` 줄 때만 저장본) · `compare` 새 판도 늘 돎 | **기본 = 같은 열쇠 저장본이 있으면 안 돎**(run · compare 바탕 · 새 판 · 「한 번 더」) · 다시 = `--fresh --why "<까닭>"` 둘 다 — `--why` 없으면 거부 · 종료 코드 2 · 까닭은 실행 기록(`_runs/*.json` meta · compare 보고 머리) |
| A 다음 판 바탕 | (잼) push 한 판의 새 판 결과 열쇠 = 다음 판 바탕 열쇠 — **이미 같았음**(모래상자 E1-6 · 바탕 실행기도 PASS) | 그대로 |
| B 고르기 | 범위 태그(`--scope`)를 사람이 고름 · 앱 파일을 읽는 하네스 전부 | **compare · plan 기본 = `--affected`**(바탕..새 판 diff) — 첫 줄 `== 고름: …` 에 까닭 · 공용 층을 건드린 판만 그 앱 전체 · 손으로 전체 = `--all --why` · `--only` 는 그대로 |
| C 2 시간 | 한 부름이 끝까지 · 꺼지면 처음부터 | 돌기 전 어림(실행기 하나 = 차례로 · 무리 1) > 90 분 → ≤ 80 분 덩어리마다 하위 프로세스 · 하네스마다 저장본 + `_qa_results/<앱>/_run_state.json` · 같은 명령을 다시 부르면 끝난 하네스는 건넘 · `--budget 분`(기본 100) 을 다음 덩어리가 넘기면 멈춤 = 종료 코드 4 |
| D 끝 시각 | 사람 · 모델이 짐작 | 시작 때 · 하네스마다 `_qa_results/<앱>/_eta.txt` 덮어씀(+ `N:\개인\claude\_code_now.md` 에 「회귀」 칸이 있으면 그 칸): 남은 하네스 수 · 남은 last_sec 합 ÷ 무리 수 → 끝 어림 · 시작 어림 · 지금까지 실제−어림 · 30 분 넘게 밀리면 머리 `★ 밀림 +N 분 · 까닭(가장 늦은 하네스 셋)` |

## B 고르기 규칙(`_tools/qa_affected.py` · `_tools/shared_names.py`)

- 공용 층 이름표 `_tools/shared_names.json` = 스크립트가 앱마다 뽑음(main 43c09e0 · jo 1915 함수 중 726 · jagwa 1194/487 · minbeop 1466/509 · timetable 755/258 · chem 86/39):
  인라인 `<script>` 를 글자 · 주석 · 정규식 · 템플릿까지 가려 읽고 이름 있는 함수(선언 · `x=function` · `x=(…)=>`)마다
  **부르는 자리 ≥ 3**(주석 밖 `이름(` · 인라인 `on…="이름("` 포함 · `.이름(` 메서드 · 정의 자리 뺌) 또는 **몸에 localStorage · indexedDB · fetch( · 'PUT'** 이면 공용.
  실행기는 바탕 앱 md5 가 json 과 같으면 그 표 · 다르면 같은 규칙으로 바탕에서 다시 뽑음(0.5~1 초).
- 판 diff(git diff -U0)에서 — 주석만 바뀐 덩이는 뺌:
  - 바뀐 줄을 몸에 품은 함수 **전부**(안쪽 → 바깥) + 그 줄에서 정의된 한 줄 함수(`var ynUid=r=>…`) = 바뀐 함수 → 공용이면 **전체**
  - 바뀐 줄이 부르는 앱 함수가 공용이면 **전체**(「+회독」 줄이 부르는 qFillSel · qPaint) — 단 「도구 함수」는 부르기만 하면 안 셈(아래 정한 것 1)
  - 아니면 글자: 바뀐 함수 · 그 함수를 부르는 자리(≤ 2)의 함수 · 맨 위 자리면 그 줄 id · CSS 규칙 선택자(그 규칙 통째) · id · 글자 상수(기록 열쇠 꼴)
    → 하네스 소스(+ 입력에 든 로컬 .py)에 그 글자가 든 하네스(선택자는 통째 글자 또는 그 선택자의 낱 이름이 **다** 들어야) · 전수표 inputs 에 그 길 · 글자가 든 하네스
    · 그 판이 더하거나 바꾼 하네스(판 관문) · 태그 smoke 하나(여기서 돌 수 있는 것 · 앱 파일을 읽는 것 · 가장 짧은 것 차례)

## 관문(`_qa/_tools/_harness_qa_bigguard.py --yard` · 모래상자 · N: 무접촉)

| 칸 | 잣대 | 새 실행기 | 헛잣대(바탕 실행기 43c09e0) |
|---|---|---|---|
| E1-1 | 저장본 있는 판 다시 run → 안 돎 | PASS(돈 0 · 저장본 그대로 10) | FAIL(10 다시 돎) |
| E1-2 | run `--fresh` 만 → 거부 · 2 | PASS(rc 2 · 돈 0) | FAIL(rc 0 · 10 돎) |
| E1-3 | run `--fresh --why` → 돎 · 까닭이 실행 기록에 | PASS(10 · meta.why) | FAIL(why 없음) |
| E1-4 | 같은 compare 다시 → 바탕 · 새 판 저장본 | PASS(돈 0) | FAIL(새 판 10 다시) |
| E1-5 | compare `--fresh` 만 → 거부 · 2 | PASS | FAIL(rc 0 · 10 돎) |
| E1-6(잼) | 새 판 결과 = 다음 판 바탕(바탕 안 돎) | PASS | PASS(이미 열쇠가 같음 — 헛잣대 셈 밖) |
| E2-1 | 4ce28d0..e7fd97b(CSS 세 줄) = g3tx · smoke 하나 | PASS(2/57 = jagwa_g3tx · phys) | FAIL(57/57) |
| E2-2 | 67e423e..783799b(uid 묶음 · 기록 열쇠) = 공용 → 전체 | PASS(57/57 · qk · uidNo …) | FAIL(고름 줄 없음) |
| E2-3 | 1b4a4c2..2340c46(「+회독」) = 공용 → 전체 | PASS(57/57 · qFillSel · qPaint) | FAIL(고름 줄 없음) |
| E3-1 | 어림 150 분 → 덩어리 둘(≤ 80 분) | PASS(75 + 75 분) | FAIL(상태 없음) |
| E3-2 | 첫 덩어리 중간에 죽임 → 다시 = 남은 것만 | PASS(끝난 2 건넘 · 남은 8 만 · 겹침 0) | FAIL(10 다시) |
| E3-3 | 이어 돈 뒤 상태 끝 · 남은 0 | PASS | FAIL |
| E3-4 | `--budget 60` → 덩어리 하나 뒤 4 → 다시 = 나머지 | PASS(5 + 5 · rc 4 → 0) | FAIL(한 번에 10 · 둘째 10 다시) |
| E4-1 | `_eta.txt` 하네스마다(남은 6→1 · ÷ 무리 · 끝 어림) | PASS | FAIL(파일 없음) |
| E4-2 | 가짜 last_sec 늘림 → `★ 밀림 +42 분 · 까닭(fk_06 +15 분 · fk_05 +15 분 · fk_04 +15 분)` | PASS | FAIL |
| E4-3 | `_code_now.md` 「회귀」 칸 덮어씀(다른 칸 그대로) | PASS | FAIL |
| YARD | 바탕 실행기로 E1~E4 다 FAIL | PASS(E1 5/5 · E2 3/3 · E3 4/4 · E4 3/3) | — |

새 실행기 PASS 17 · FAIL 0(YARD 포함) · 관문 한 번 ≈ 3 분(새 · 바탕 둘 다)

## --affected 자체 시험 셋(실제 genie 이력 · 실제 전수표 · 하네스 소스)

1. `4ce28d0..e7fd97b` — `== 고름: 공용 층 안 건드림 → 하네스 2/57 — jagwa_g3tx(판 관문(하네스 새로)) · phys(smoke 하나(29초))`
   (CSS 선택자 `.g3s .bt1` · `#g3Pop .g3pf .it` · `.g3it .g3tx` 통째 · 낱 이름 셋 다 = g3tx 소스만 · `.g3tx` 만 쓰는 gg3 · gg3_webkit · ggmath 는 안 탐)
   · smoke 하나 = 클라우드에서는 phys(order 는 N: 필요) · 로컬이면 가장 짧은 order(15초)
2. `67e423e..783799b` — `== 고름: 공용 층 건드림 → jagwa 전체 57 — qk · uidNo · inkK · typeOf · typeFixed · noteOf 외 76`
3. `1b4a4c2..2340c46` — `== 고름: 공용 층 건드림 → jagwa 전체 57 — qFillSel · qPaint`(바뀐 줄 = 맨 위 `#tLayerAdd` 손잡이 · 부르는 qFillSel 부름 4 · qPaint 12)

참고(잼 · 관문 밖) — main 지난 판(그 판 앞 → 그 판): 자과 25 판 중 전체 21(합치기 · 기록 · 동기화 판) · 좁힘 4(e7fd97b 2 · 95cc766 셸 CSS 7 · 5f61ed7 터치 CSS 15 등)
· 조판기 13 판 전부 전체(합치기 판들이 공용 함수 몸을 고침) — 큰 합치기 판은 여전히 전체, 작은 고침 판에서 줄어든다.

## 지시서와 다르게 정한 것 · 알아 둘 것

1. **도구 함수**(공용 가운데 앱 상태를 안 만지는 작은 함수 — 맨 위 · 저장 API 없음 · 몸 ≤ 240 자 · 부르는 앱 함수가 도구뿐 · 바깥 이름에 = · push 안 함: `$` · `esc` · `toast` · `rec` … 자과 110)는
   바뀐 줄이 **부르기만** 하면 공용 층을 건드린 것으로 안 셈(몸을 고치면 셈). 안 그러면 `$(` 가 든 JS 줄은 다 전체가 된다. `put` · `get`(IndexedDB 래퍼)은 도구 아님.
2. 저장 API 에 `.transaction(` · `objectStore` · `sessionStorage` 도 넣음(IndexedDB 래퍼 `tx` 가 indexedDB 글자를 안 씀).
3. 안쪽 함수(같은 이름 지역 함수 `draw` 13 개 …)는 `바깥>안` 이름으로 따로 셈(부르는 자리 = 바깥 함수 몸 안) — 한 이름으로 뭉쳐 다 공용이 되던 것.
4. 끝 어림의 무리 수 = 1(실행기 하나는 차례로 돎) · 덩어리 셈도 무리 1 벽시계 — `plan` 의 「무리 3 벽시계」 는 여러 줄로 나눌 때 그대로 둠.
5. `--budget`(기본 100 분)·종료 코드 4 를 더함 — 덩어리를 다 한 부름에서 돌면 그 부름이 2 시간을 넘으므로 다음 덩어리가 예산을 넘기면 멈추고 「같은 명령을 다시」.
6. 잠금: 덩어리 하위 프로세스는 부른 실행기의 잠금을 넘겨받음(`QA_CHAIN_PARENT`) · 리눅스에서 거둬지지 않은 죽은 프로세스(좀비)를 산 것으로 보던 것 고침(E3 에서 드러남).
7. `_qa/_qa_sync.py` 4 줄(줄 밖 · `_qa/` 안) — `_tools/` 셋을 모음에 안 넣으면 `copy` 가 `_qa` 에서 지우고 `check` 가 json 을 「스크립트 아닌 것」으로 셈.
8. `--label` 되풀이 · 옛 관문 `_harness_qa_baseline` B-2(같은 커밋 두 번) · B-4(plan 셈)는 이제 저장본 · `--affected` 기본을 따름 — 되풀이는 `--fresh --why`.
9. 같은 앱을 두 줄(무리)에서 겹쳐 돌리면 `_run_state.json` · `_eta.txt` 를 서로 덮음(파일 자리가 지시서대로 앱마다 하나).
10. `_config.yml` 이 없어 Pages exclude 는 안 함(만들면 `_qa` 밖 파일이 하나 더) — `CLAUDE.md` 는 Pages 에 보일 수 있음(저장소가 공개라 글은 이미 공개).
11. 클라우드에서는 진짜 앱 하네스로 compare 를 안 돌림(브라우저 · studyplandata · N:) — 실제 이력으로는 plan(고르기 · 덩어리 셈)만 잼.

## 단계별 분(UTC 10/10)

| 단계 | UTC | 분 |
|---|---|---|
| 착수 — git fetch · 지시서(main 43c09e0) · WebKit 줄 · 작업트리 · 실행기 · 모래상자 _harness_qa_baseline · 전수표(smoke 112) · 자체 시험 diff · 자과 함수 셈 | 07:15–07:28 | 13 |
| §B 공용 층 이름표(shared_names.py) · 고르기(qa_affected.py) · 자체 시험 셋 · 지난 판 38 맞대기 · 다듬기(스크립트 겹침 · 템플릿 글 · 안쪽 함수 · 도구 함수 · @media 선택자 · 한 줄 정의) | 07:28–07:50 | 22 |
| §A·C·D 실행기 고침(저장본 기본 · --fresh --why · 고름 · 덩어리 · 상태 · 끝 어림 · 잠금 넘김) | 07:50–07:56 | 6 |
| §E 관문 짓기 · 다듬기(가짜 하네스 바이트 · 좀비 잠금 · 예산 잣대) · 첫 전체 관문 + 헛잣대 | 07:56–08:03 | 7 |
| 마무리(잠금 먼저 · 덩어리 흔들림 한 번) · shared_names.json · 전수표 줄 · _qa_sync · CLAUDE.md · check | 08:03–08:05 | 2 |
| 마지막 관문 + 헛잣대(188초) · 실행기 밑에서 관문(전수표 줄 그대로 `run root --only qa_bigguard` · 189초 · PASS 17) | 08:05–08:12 | 7 |
| 결과 파일 · 커밋 · push | 08:12–08:16 | 4 |

## 그 뒤(주니어 채팅)

N: 정본에 들일 것 — `_qa_chain.py` · `_qa_chain_list.json`(관문 한 줄) · `_qa_sync.py` · `_tools\`(`qa_affected.py` · `shared_names.py` · `shared_names.json` · `_harness_qa_bigguard.py`)
· Code CLAUDE.md 「회귀」 절 한 줄: 「기본 = --affected · 저장본(옛 --reuse) · 다시 = --fresh --why · 2 시간 넘으면 종료 코드 4 = 같은 명령 다시」
