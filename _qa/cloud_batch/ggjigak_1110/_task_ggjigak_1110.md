# _task_ggjigak_1110 — 민법OX 지학식 근거 · 조판기 1차객(특허 · 상표 · 디보) 근거 그 자리 고치기 [클라우드 · 앱 둘 · main push 한 번]

**화면에서 달라지는 것**
- 민법OX(시안 「민법 지학식 근거 시안」 v22 그대로):
  - 근거 댓글 줄마다 그 댓글을 단 문항의 지문이 붙고, 지문을 누르면 O/X 를 고른다. 댓글마다 ! 가 있다.
  - 근거 줄 「:」 → 점 •. 점을 누르면 근거를 골라 댓글을 단다. 칩에는 ↩N · 「댓」 이 붙고, 연결 상자는 머리 줄 없이 왼쪽 점선이다.
  - 연필 ✎ 을 걷고, 길게 누르면 그 자리에서 고친다. 단추 · 테두리는 없고, 밖을 톡 = 저장 · 굴림 = 그대로 · Enter 저장 · Esc 그만.
  - 정리 창 근거 줄에 O/X · ! 가 바로 보인다(바뀐 줄만 다시 그림). 📍 핀이 쉬는 동안 끝없이 다시 그려지던 것을 없앤다.
- 조판기 1차객(특허 · 상표 · 디보 같은 함수 · 시안 「조판기 1차객 근거」 v2 그대로):
  - 근거를 고치거나 더해도 펼친 근거 판이 그대로 남는다. 같은 문항 카드가 한 화면에 둘이면(상표 OX · S 줄) 둘 다 새로 그린다.
  - 근거 「고치기」 · 댓글 「고치기」 · 연결 상자 「✎ 여기서 고치기」 = prompt() 창 · 「저장」「취소」 칸 대신 그 글 자리에서 고친다(민법과 같은 꼴).
- 저장 꼴 · 동기화 길은 무변이다. 새 칸(댓글 jo · bang · jm · sh)은 같은 근거 JSON 안에 싣는다. 옛 앱 기기가 저장해도 사라지지 않음(채팅 잼).

- 판 크기 = 앱 둘(민법 패치 35 쌍 · 조판기 9 쌍) · 새 파일 0(관문 `gg_gate.py` · 명세 둘은 이 폴더에만 · main 에 안 넣음) · 짤 것 0
- 로컬 필요 = 0
- 시간 = ≈30 분(선례 jn_cm_1105 두 앱 한 판 16:10 넘김 → 16:4x 인도 · 이 판 관문 채팅 잼 = 민법 새 판 크롬 2.5 + 웹킷 2.7 분 · 조판기 1.7 + 1.8 분 · 바탕 크롬 민법 7.1 · 조판기 3.4 분)

## 할 일(차례대로 · 이것만)
0. WebKit 을 세운다(이 저장소 CLAUDE.md 「WebKit」 절). 잰 결과를 커밋 글 첫 줄에 적는다.
1. `git fetch origin main cloud/inbox` · 바탕 = main **9510582**(`minbeop/index.html` LF md5 **ed4e306b** · `jo/index.html` **de700f37** · `_qa/_qa_apply_patches.py` **b8887814**) — 다르면 멈추고 커밋 없이 이 줄만 알림(main 이 두 앱을 안 건드린 커밋만 앞섰으면 그대로 간다).
2. `cloud/inbox` 의 `_qa/cloud_batch/ggjigak_1110/` 에서 다섯을 꺼냄: `ox_patches.txt`(md5 e4f0578b) · `jo_patches.txt`(md5 6c003bd8) · `spec_ggox.json`(md5 7e1a9ec7) · `spec_ggjo.json`(md5 3a7425ca) · `gg_gate.py`(md5 784c647f).
3. 패치 넣기:
   - `python _qa/_qa_apply_patches.py ox_patches.txt minbeop/index.html --expect 96e1212c` → 1,262,278 B · 인라인 스크립트 7 · 문법 0
   - `python _qa/_qa_apply_patches.py jo_patches.txt jo/index.html --expect 3c24f7eb` → 1,787,216 B · 인라인 스크립트 1 · 문법 0
   - 둘 다 채팅이 잼. 멈추면(종료 2 · 3) 그 줄만 알림.
4. 관문(데이터 = `git clone --depth 1 https://github.com/zzikkaplan/studyplandata` · 받기만 · 쓰기 0):
   - 민법: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python gg_gate.py --spec spec_ggox.json --new minbeop/index.html --base 9510582 --spd <클론> --eng chromium,webkit --base-eng chromium`
     - 칸 78 · 헛잣대(바탕 FAIL) 70 · 무변 8(📍 핀 둘 · 준비 셋 · ! 끔 · 폰 ③ 펼침 · 바탕 PASS)
     - 채팅 잼: 새 판 크롬 78/78 · 웹킷 78/78 · FAIL 0 · 바탕 크롬 70 FAIL · 8 PASS · 크롬 2.5 · 웹킷 2.7 · 바탕 7.1 분
   - 조판기: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python gg_gate.py --spec spec_ggjo.json --new jo/index.html --base 9510582 --spd <클론> --root jo --eng chromium,webkit --base-eng chromium`
     - 칸 30(특허 PC · 폰 · 상표 PC · 폰 · 디보 PC) · 다 헛잣대
     - 채팅 잼: 새 판 크롬 30/30 · 웹킷 30/30 · 바탕 30 다 FAIL · 합계 FAIL 0 · 크롬 1.7 · 웹킷 1.8 · 바탕 3.4 분
   - 관문은 앱이 쓰는 CDN(cdn.tailwindcss.com 등)을 그대로 받는다(글 크기 칸이 Tailwind 를 씀).
     - CDN 이 막혀 글 크기 · 자리 칸만 FAIL 이면 그 칸 이름과 값만 알리고 나머지 PASS 면 간다.
   - 시험 근거 · 댓글은 명세가 지어 넣는 글(「시험 근거 하나(지어낸 글)」 · 「관문 시험 댓글(지어낸 글)」 · 원격 쓰기 = 관문 가짜 200 · 기록 값 0).
   - 민법 칸은 기록의 Q0598 근거(`g_Q0598_muc1kec2_wh0x` · 댓글 6) · Q1064 연결을 쓴다. 클론에 없으면 그 줄만 알림.
   - FAIL 이 나면 그 칸만 `--only <칸 이름 앞머리>` 로 다시. 앱 결함이면 고치지 말고 칸 이름과 값만 알림.
5. 회귀 사슬 · grep 회귀 안 돌림(이 판 관문이 바뀐 함수 · 화면을 다 누름 · 클라우드 규칙 85).
6. 커밋 하나(`minbeop/index.html` · `jo/index.html`)를 만들고 **genie main 에 fast-forward push**(사용자 지시 · 본인 공부 앱 · 운영 배포 아님).
   - 커밋 글 = WebKit 줄 · 관문 합계 줄 둘 · 앱 md5 둘 · 단계별 분.
   - push 가 막히면 지정 가지에 올리고 그 사실만 알림.
- 지킬 것: 공개 저장소 — 커밋 글에 기록 값 0. `cloud/inbox` 가지와 그 폴더 파일은 건드리지 않음(채팅이 검수 뒤 걷음). `gg_gate.py` · 명세를 main 에 넣지 않음.
- 사용자 할 일 = 모든 기기에서 민법OX · 조판기 새로고침 한 번.

## 패치가 하는 일
**민법(35 쌍 · ed4e306b → 96e1212c)**
1. 댓글 줄: `.ggfrom/.ggjt` 단 문항 지문(q.q 통째 · 진하게 남색) · 누르면 O/X(c.jo) · 댓글마다 ! (c.bang · 그 줄만 빨간 왼줄) · 오른쪽 칸 uid · sh · 날짜 · ✕(폭 600px 미만 세로 · 넘으면 가로).
2. 근거 줄 「:」 → 점 `.ggjmdot` · 누르면 `.ggjmbox`(이 문항 · 연결 근거 첫 줄 · 그 밑에 이 문항 댓글 전부) · 골라 Enter = 댓글 {jm:'q'} · 연결 근거면 from = 이 문항.
3. 칩: 모든 자기 칩 안 ↩N · 이 문항이 그 근거에 댓글 달았으면 「댓」(ggMeCm) · 연결 칩 uid 걷음.
4. 연결 상자: 🔗 머리 · 「1.」 걷음 · 근거 줄 오른쪽 uid(누르면 그 문제) · 댓 · ✕(연결 끊기 · 되묻기 그대로) · 왼쪽 긴 점선.
5. ✎ 걷음 · 길게 누름(550ms · 손 뗄 때 · 뒤따르는 click 700ms 먹음 · 지학 SHELL 꼴) = ggIed 그 자리 고치기(textarea 를 글과 같은 꼴로).
   - 밖 톡(8px · 700ms 안) = 누른 것이 먼저 제 일을 한 뒤 저장. 관문 잼: 고치는 중 다른 댓글 ! 톡 → 저장 + ! 둘 다.
   - 굴림 · 끌기 = 그대로. 댓글 지문 위 길게 = 댓글 글만 고침.
6. 글 크기 = 지학 비율(근거 11.5 · 댓글 10.5 · 날짜 9.5) · ✕ 셋 = 지학 `.ggcx` 회색.
7. 정리 창(openJeongni · jnGgHTML): 「🔗 1.」 걷음 · 연결 댓글 uid 끝으로 · O/X · ! 빨간 줄. 저장 뒤 `ggJnRepaint(uid)` = 바뀐 문항 줄 + 그 문항을 연결한 줄만 · `qpCacheOpen/Close` 로 기록 한 번 풂.
   - 채팅 잼: 옛 통째 다시 그리기 58 줄 259 ms · 253 줄 783 ms → 5.9 · 30.1 ms.
   - storage 이벤트(다른 탭) = 통째.
8. 쓰임 창(useWin): 부제 · 줄 · 「그 문제 보기」 걷음 · 줄 누름 = 그 문제.
9. 자기 근거 머리 「맞음 · 날짜」 걷음 · ggRepaintChip 이 머리 둘째 칸을 덮어 댓 · ✕ 를 지우던 원래 결함 고침. 근거 ! = 머리 줄만 붉음.
10. 📍 핀 `refreshPins` = 값이 다를 때만 className · filter · textContent · title 을 씀.
    - 원래 앱은 MutationObserver → refreshPins → 같은 글 다시 씀 → childList → 끝없이 돌았음(채팅 잼: 쉬는 동안 4 초 902 바뀜 → 0~2).

**조판기(9 쌍 · de700f37 → 3c24f7eb)**
1. `ggRepaint`: 다시 짓기 전 펼친 근거 판(data-gbbox) · 숨긴 연결 상자 기억 → 다시 지은 뒤 그대로 · 같은 `data-ggu` 칸 전부(옛 = 첫 칸만).
2. `joIed`(= 민법 ggIed 꼴) 새 함수 · 근거 「고치기」(옛 「저장」「취소」 칸) · 댓글 「고치기」(옛 prompt) · 연결 상자 「✎ 여기서 고치기」(옛 prompt) = 그 자리.
   - 단추 글자 · 자리 그대로. 고치는 중 그 단추를 다시 누르면 닫기만 한다.
3. `.joied` 꼴(글과 같은 글꼴 · 밑줄 한 줄).

## 점검표(채팅)
1. **일꾼** = 클라우드(앱 파일 둘). 2. **차례** = 한 판 · 「~뒤」 없음. 3. **회귀** = 없음(관문이 바뀐 함수 · 네 화면 · 세 법을 다 누름 · 클라우드 85).
4. **선례**
   - 지학 iedOpen(11741) · SHELL 길게 누름(11762~11774) · jmDotHTML/g3JmBox(6902 · 13593~13614) · `.ggcx` = 민법 꼴의 바탕.
   - qpCacheOpen(09-16 「렌더 한 번 = 저장소 한 번」) = 정리 창 빠르게.
   - jn_cm_1105 · cmn_1106 = 두 앱 한 판 · 관문 꼴(ox_gate.py → gg_gate.py).
5. **저장 칸** = 같은 근거 JSON(ox_q_geunge = SYNC_KEYS · 칸 단위 recMerge 통째 값 · 채팅 잼) · 새 열쇠 0.
6. **근거** = 사용자 11/10 13:18 ~ 18:14 시안 댓글 · 채팅 줄(결정로그 11/10 줄 · 쓸모없음 376~408).
   - 16:01 · 16:09 「저장 취소 단추 · 가로 폭」 · 15:53 「아이패드 굴림 · Esc 만」 → 단추 없는 그 자리 고치기.
   - 17:10 「조판기 판 접힘 · prompt 고쳐」 · 17:31 「상표 디보는」.
7. **화면 끝** = 첫 줄 · 사용자 할 일. 8. **자료** = 시안 둘(민법 WpT9viaVWJrt89Vv4BiNjX v22 · 조판기 5sE8GxpHJXZy8N7WN43Btr v2) · 설정 정본 N: `_tools\art_app\snap_minbeop_ggjigak_1110.json` · `snap_jo_gaek_ggied_1110.json`.
9. **클라우드** = 관문 + 헛잣대만. 10. **더 빨리** = 채팅이 관문 두 앱 × 두 엔진 + 바탕을 미리 돌려 FAIL 0.
13. **inbox** = 고정 가지. 14. **세 줄** = 18:2x 사용자에게 먼저 보냄.
15. **과목 · 법** = 민법 한 앱 · 조판기 1차객 세 법 같은 함수(특허 · 상표 · 디보 화면 다 잼 · 디보는 미분류 1,030 장이라 PC 만).
