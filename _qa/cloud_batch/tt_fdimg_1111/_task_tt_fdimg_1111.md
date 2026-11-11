# _task_tt_fdimg_1111 — tt Food diary: 이미 쓴 항목에 사진 추가 [클라우드 · 작은 고침 · 앱 하나 · main push 한 번]

**화면에서 달라지는 것**
- Archive → 🍚 Food diary → 카드 → ✎(항목 편집) 창 맨 아래에 「사진 추가」 칸(여러 장 고르기)이 생긴다. 새 항목 창의 「사진」 칸과 같은 꼴이다.
  - 아래 줄에 「지금 사진 N장 · 고른 사진은 뒤에 붙어」 를 보인다.
- 저장하면 고른 사진을 기기에서 압축(긴 변 1800 · 품질 85 · 새 항목과 같음)해 저장소에 올리고, 항목 사진 뒤에 붙인다.
  - 옛 사진 · 차례는 그대로다. 경로 = `food/img/<id>_<시각>_<n>.jpg` 라서 옛 파일과 안 겹친다.
  - 썸네일이 없던 항목(사진 없이 만든 항목)은 첫 추가 사진으로 `food/thumb/<id>.jpg` 를 만든다 → 카드에 사진이 뜬다.
  - 업로드가 실패해도 고친 글은 저장한다(새 항목 foodSave 와 같은 길).
- 사진을 안 고르면 옛 편집 그대로(글만 저장). 저장 꼴(items 의 imgs · thumb 칸) · 동기화 길 무변.

- 판 크기 = 작음(앱 하나 · 패치 1 쌍 = 편집 창 칸 + 새 함수 foodAddImgs · 새 파일 0 · 짤 것 0 · 관문 = `tt_gate.py`(tt_recimp_1106 그대로) + 명세 하나)
- 로컬 필요 = 0
- 시간 = ≈15 분(선례 tt_recimp_1106 10:38 넘김 → 10:4x 인도 · 이 판 관문 채팅 잼 = 크롬 11.5 초 · 웹킷 12.0 초 · 바탕 6.6 초)

## 할 일(차례대로 · 이것만)
0. WebKit 을 세운다(이 저장소 CLAUDE.md 「WebKit」 절). 잰 결과를 커밋 글 첫 줄에 적는다.
1. `git fetch origin main cloud/inbox` · 바탕 = main 890901f(`timetable/index.html` LF md5 **9c68b4d9** = 61f8bda 뒤 무변 · `_qa/_qa_apply_patches.py` **b8887814**) — 다르면 멈추고 커밋 없이 이 줄만 알림(main 이 tt 를 안 건드린 커밋만 앞섰으면 그대로 간다).
2. `cloud/inbox` 의 `_qa/cloud_batch/tt_fdimg_1111/` 에서 셋을 꺼냄: `app_patches.txt`(md5 1fa23724) · `spec_ttph.json`(md5 52bd3105) · `tt_gate.py`(md5 6079bef3).
3. `python _qa/_qa_apply_patches.py app_patches.txt timetable/index.html --expect 9298daf6` → 533,889 B · 인라인 1 · 문법 0(채팅이 잼). 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문(데이터 = `git clone --depth 1 https://github.com/zzikkaplan/studyplandata` · 받기만 · 쓰기 0):
   - `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python tt_gate.py --spec spec_ttph.json --new timetable/index.html --base 61f8bda --spd <클론> --eng chromium,webkit --base-eng chromium`
   - 칸 6 · 헛잣대(바탕 FAIL) 5 · 무변(바탕 PASS) 1(사진 없이 이름만 고침).
   - 채팅 잼(studyplandata 4e5eb53): 새 판 크롬 6/6 · 웹킷 6/6 · 바탕 크롬 5 FAIL · 1 PASS · 합계 FAIL 0 · 0.5 분.
   - 시험 항목 · 사진(id gatefd1 · 「관문 음식」 · 캔버스로 그린 40×30 사진)은 명세가 지어 넣는 것이다. 사진 올리기 = 관문 가짜 200 · 원격 쓰기 0 · 기록 값 0. 사진 고르기는 파일 칸에 DataTransfer 로 넣고 진짜 「저장」 단추를 누른다.
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시. 앱 결함이면 고치지 말고 칸 이름과 값만 알림.
5. 회귀 사슬 · grep 회귀 안 돌림(작은 고침 · 편집 창 한 곳 · 관문이 바뀐 길을 다 누름).
6. 커밋 하나(`timetable/index.html`)를 만들고 **genie main 에 fast-forward push**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님).
   - 커밋 글 = WebKit 줄 · 관문 합계 줄 · 앱 md5 · 단계별 분.
   - push 가 막히면 지정 가지에 올리고 그 사실만 알림.
- 지킬 것: 공개 저장소 — 커밋 글에 기록 값 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(채팅이 검수 뒤 걷음). 명세 · tt_gate.py 를 main 에 넣지 않음.
- 사용자 할 일 = 모든 기기에서 tt 새로고침 한 번.

## 패치가 하는 일(1 쌍 · 9c68b4d9 → 9298daf6)
- `foodEdit` 창 끝에 `<input id="fdF" type="file" accept="image/*" multiple>` + 「지금 사진 N장」 줄 · 저장 때 고른 파일이 있으면 새 `foodAddImgs(x, 파일들)`(async) · 없으면 옛 그대로 `upsertFood(x);render()`.
- `foodAddImgs` = foodSave 의 사진 부분과 같은 길(imgCompress → ghPutRaw) · imgs 뒤에 붙임 · 썸네일 없을 때만 만듦 · 끝에 upsertFood · render.

## 점검표(채팅)
1. **일꾼** = 클라우드(앱 파일 하나). 2. **차례** = 한 판 · 「~뒤」 없음. 3. **회귀** = 없음(편집 창 한 곳 · 관문이 바뀐 길을 누름).
4. **선례** = 새 항목 foodAddModal · foodSave(8/29 feedback13 · food/img · food/thumb) · Share 사진 올리기(shareAddImg) · tt_recimp_1106 관문 tt_gate.py.
5. **저장 칸** = 무변(imgs · thumb 는 지금도 쓰는 칸).
6. **근거** = 사용자 11/11 11:13 「tt 앱 fooddiary 이미 쓴 글에 사진 추가할 방법이 없어 · 고쳐줘」.
7. **화면 끝** = 첫 줄 · 사용자 할 일. 9. **클라우드** = 관문 + 헛잣대만. 10. **더 빨리** = 채팅이 관문 두 엔진 + 바탕을 미리 돌려 FAIL 0.
13. **inbox** = 고정 가지. 14. **세 줄** = 11:1x 사용자에게 먼저 보냄.
- 이 판에 안 넣은 것: 사진 빼기 · 순서 바꾸기(사용자가 말한 것 = 추가만).
