# 타임테이블 (timetable)

두 사람(햄찌·꼬까)의 공부 타이머·기록·계획 앱. 단일 HTML · 라이브러리 없음 · PWA.
배포 = https://skygenie00.github.io/genie/timetable/

## 저장소 둘

| 무엇 | 어디 |
|---|---|
| 앱 코드 (이 폴더) | `skygenie00/genie` — 공개, GitHub Pages |
| 데이터 | `zzikkaplan/studyplandata` — **Private**. `settings.json` · `sessions/<사람>/YYYY-MM.json` · `todos/<사람>.json` · `plan/<사람>.json`. 앱이 각자 토큰으로 직접 읽고 씀 |

- 토큰은 앱 설정 화면에만 넣는다. 브라우저 저장소에 산다. **코드·README·커밋 어디에도 적지 않는다.**
- 공개 저장소(genie)에 데이터 JSON·PDF 를 올리지 않는다.

## 파일

- `index.html` — 앱 전부 (화면·타이머·동기화·계획 엔진).
- `sw.js` — 서비스워커. 껍데기만 캐시, GitHub API 는 캐시하지 않음. **파일을 고치면 `V` 를 올린다.**
- `manifest.webmanifest` · `icon.svg` — PWA 껍데기.

## 설계 요약 (v1)

- v1 범위: 타이머·세션·일간/주간/월간·데일리 모음(햄찌 좌·꼬까 우)·할일(어제/오늘/내일, 학습과 할일 분리, 이월)·오프라인 큐·GitHub 동기화·PWA·크롬 문서 PiP(시트+MiMi 바 통째).
- 시간 규칙: 하루는 05:00 에 시작(설정 가능). 그 전 시각은 전날로 치고 분 값에 1440 을 더해 저장.
- 세션 = `{id,d,s(과목),p(계획),i(항목),a(시작분),b(끝분),k(○×△),u(수정시각),del}`. 사람별·월별 파일이라 두 사람 사이 충돌 없음. 같은 사람 두 기기는 id 기준 병합, `u` 큰 쪽 승리, 삭제는 `del:true` 표식.
- 동기화: 저장 4초 뒤 자동 push, 90초마다 대기분 재시도, 온라인 복귀·탭 복귀 시 pull. 409/422 면 다시 받아 병합 후 재시도 1회. 상대 파일은 읽기만.
- 로컬 키: `tt.cfg`(사람·토큰) `tt.settings` `tt.f.<path>`(파일 캐시+dirty+sha) `tt.run`(진행 중 타이머) `tt.form`.
- 색: 데일리 10h 이상 분홍 · 6h 이상 하늘(설정). 주차 번호는 W1 = 2026-08-03 기준(계획 설정에서 변경 가능).

## v2 — 계획 (A단계 반영)

- `plan/<사람>.json` = 띠(bands: 과목·활동·주차 w1~w2·주당 처리량 per·단원 id 목록)+단원 DB(units)+요일별 처리량(daily)+월간 목표(goals)+기준선(baselines).
- 오늘 학습: 활성 띠마다 그 날 quota+밀림 개수를 단원 DB 에서 자동으로 꺼내 어제/오늘/내일에 보여준다. 체크 = `done[bandId]=날짜`. todos 파일에는 쓰지 않는다.
- 주차계획 화면: PC 는 주차 보드(띠 늘리기 손잡이·원계획 그림자·이정표), 폰은 한 주씩 카드. 띠 클릭 = 편집.
- 병합: bands·milestones·units[과목] 은 id·u·del 규칙, daily·goals·baselines·weekStart 는 파일 수준 `pu` 큰 쪽 통째.
- B단계 예정: 월간(목표·달성·그래프·단원 DB·기준선 고정), 재배치 적용, STOP 자동 완료, 상대 밀림 표시.
