# -*- coding: utf-8 -*-
r"""_task_ox_home_tidy §C 관문 — 민법OX 첫 화면·서랍·태그 아이콘 다듬기(§A 시험 스물아홉) + 메모·논리 걷어 내기(§B G-B1~G-B5)

  python _harness_ox_home_tidy.py [--new <앱 파일 | genie 판>] [--base <판 = e425f97>] [--data-rev <studyplandata 판 = 42664d8>] [--spd <studyplandata 자리>]
                                  [--only C,B1,B2,B3,B4,B5] [--no-base] [--tw <Tailwind CSS 사본>] [--res <결과 파일>] [--shots <그림 폴더>]

  NEW = genie 작업트리 minbeop/index.html(고친 판) · BASE = 바탕 e425f97(헛잣대) — 두 판을 같은 차례 · 같은 데이터로 늘 같이 돌림
  틀 = 시안 도구 _tools/art_app/snap.py(채팅 10/6 · 시안 v16 점검)의 SHIM 그대로(tt.cfg 토큰 'demo' · GitHub contents API → 데이터 파일 · PUT = 가짜 성공 · 그 밖 http 404)
       + _harness_ox_gg_phone.py 의 결과 꼴(PASS/FAIL 줄 · 헛잣대 · 단계별 초) · alert/confirm 은 시안처럼 막음(confirm = 취소)
  데이터 = studyplandata <data-rev> 의 minbeop/ 다섯 파일(문항마스터 · 기록 · 기출키 · claude · 문항메타) — git show 로 읽기만(SPD_ROOT · 판이 없으면 종료 3)
  C  화면 넷 — 한 문맥(저장소 하나 = 시안의 같은 출처 iframe 넷): p1 = PC 1100×800 서랍 접힘 · m1 = 폰 390×780 서랍 접힘 · p2 = PC 서랍 열림 · m2 = 폰 서랍 열림
       ready(지시서 §C) → 첫 동기화 끝(recBusy 풀림 · 시안보다 한 단계 더 기다림) → 2 초 → setup(trFold) · 시험은 지시서 차례 그대로(앞 시험이 바꾼 상태를 뒤 시험이 씀)
       누름 = Playwright 진짜 누름(시안은 거울 → 엔진으로 넘김) · type = 누르고 글자 치기(30ms) · wait 기본 1000 · expect = 앱 안 전역 eval · same = 앱 안 개수 적기만
       C01~C29 지시서 §C 시험(잰 값 window.__df · __tr · __hh · __gr 같이 적음) · 헛잣대 = 바탕에서 같은 시험 → 무변 셋(서랍 손잡이 → 열림 · 검색 선의 · 약점 → 문제 화면)만 PASS 여야
         · 식이 바탕에서도 참인 셋(23 PC 제목 줄 · 24 물권 칩 · 27 채각 칩 — NONDISC 까닭)은 적기만 · 24+ · 27+ = 목록 과목 카드 1 개(same)로 가름
       CE 페이지 오류 0(pageerror · window error · unhandledrejection) — 화면 넷
  B1 흡수 이름 grep 0 · ox_q_memos · ox_q_logic = SYNC_KEYS · migrateLegacyRecords 두 줄만(정적) · 헛잣대 = 바탕 걸림
  B2 새 기기 꼴(표시키 없음 · 메모 A = 근거 지운 묘비 · 메모 B = 같은 글 src 빠짐 · 논리 C = 고친 글) 시동 + 첫 동기화(원격 기록 없음 → 첫 올림) 뒤 근거 무변 · 헛잣대 = 바탕은 A·B·C 에 붙음
  B3 엑셀 불러오기(mergeExcelRecords 보충 · 덮어쓰기 · 합성 행) — ox_q_memos · ox_q_logic 무변 · 태그 · 연결 = 바탕과 같음 · 헛잣대 = 바탕은 두 저장소가 바뀜
  B4 엑셀 내보내기(exportExcelFile · aoa 를 받아 봄) — 「메모」「논리」 열 = 원본 행 그대로: 두 저장소 빔(무변 칸 · 바탕도 PASS · 바탕과 aoa 같음) / 두 저장소에 다른 글(헛잣대 = 바탕은 저장소 글)
  B5 근거 연결 검색(kind geunge) · 문제/근거 검색 · refTextOf · 문항 팝업 근거 칸 · 쓰임 창 · 연결 끊기(geunge) 글자 = 바탕과 같음(표시키 켠 기존 기기 꼴 · 같은 데이터)
  그림(--shots · _qa 밖): 새 판 폰 첫 화면 · [1] · [2] · 서랍 [2] + PC 첫 화면 · PC 서랍 열림 · 바탕 폰·PC 첫 화면(맞대 보기)
  엔진 = Chromium · 클라우드 = cdn 막힘 → --tw · 본 PC = cdn 그대로
  결과 = 화면 PASS/FAIL 줄 · --res(기본 = 임시 폴더 · _qa 에 결과를 쓰지 않는다)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import hashlib, json, os, re, subprocess, sys, tempfile, threading, time, traceback, urllib.parse   # noqa: E402
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEW = ARG('--new', _roots.genie('minbeop', 'index.html'))
BASE = ARG('--base', 'e425f97')   # genie main e425f97 = 이 판의 바탕
DREV = ARG('--data-rev', '42664d8')   # studyplandata 42664d8 = 10/6 15:46 기록(지시서 §0 · 시안 데이터)
SPD = ARG('--spd', _roots.spd())
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
NOBASE = '--no-base' in sys.argv
TWCSS = ARG('--tw')
TMPD = os.path.join(tempfile.gettempdir(), 'h_ox_home_tidy')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_ox_home_tidy_result.txt'))
SHOTS = ARG('--shots', os.path.join(TMPD, 'shots'))
REL = 'minbeop/index.html'
REPO = 'zzikkaplan/studyplandata'
DFILES = ['minbeop/문항마스터.json', 'minbeop/기록.json', 'minbeop/기출키.json', 'minbeop/claude.json', 'minbeop/문항메타.json']
READY = "typeof quizData!=='undefined'&&quizData.length>0&&document.querySelectorAll('#hm-subjects button').length>1&&document.getElementById('trlist').children.length>0"
SETTLE = 2000
VIEWS = {'pc': (1100, 800), 'ph': (390, 780)}
SCREENS = [('p1', 'pc', 'trFold(true)'), ('m1', 'ph', 'trFold(true)'), ('p2', 'pc', 'trFold(false)'), ('m2', 'ph', 'trFold(false)')]
UNCHANGED = ('PC · 서랍 손잡이 → 열림', 'PC 서랍 열림 · 검색 「선의」', '폰 · 🔥 약점 → 문제 화면')   # 지시서 §C 헛잣대 — 바탕도 PASS 인 무변 칸
# 시험 식이 바탕에서도 참이 되는 칸(2026-10-06 첫 실행 · 바탕 e425f97 잼) — 헛잣대로 못 가름 · 까닭과 가르는 칸을 같이 적는다(숨기지 않음)
NONDISC = {'PC · 제목 오른쪽 한 줄': 'PC 1100 은 바탕도 제목 오른쪽 한 줄(A-2 는 폰 줄바꿈 고침) — 가르는 칸 = 22 폰',
           '폰 · 물권 칩 → 목록 물권만': '식이 hmSubject 만 봄(바탕도 칩이 hmSubject 를 바꿈) — 가르는 값 = same(목록 과목 카드 수 · 새 1 / 바탕 5) → 24+ 줄',
           'PC 서랍 열림 · 채각 칩': '식이 hmSubject 만 봄 — 가르는 값 = same(목록 과목 카드 수) → 27+ 줄'}
SHOT_AFTER = {'폰 · [N] 1번 → 장 줄만': ('m1', 'fold1'), '폰 · [N] 2번 → 장 줄 + 🃏·📋 칩 줄': ('m1', 'fold2'),
              '폰 서랍 · [N] 2번 → 장 줄 + 묶음 첫 줄': ('m2', 'drawer_fold2')}

# 지시서 §C 시험 표 — 글자 그대로(지시서 ```json 블록 · 시안 설정 snap_minbeop_hm.json 의 tests 와 같음)
TESTS = json.loads(r'''[
 {
  "name": "PC · 회독 칩 헷갈림 노랑 · 페이크 파란 세모 빨간 f",
  "screen": "p1",
  "click": "#data-label",
  "expect": "(()=>{const b=[...document.querySelectorAll('#dashboard-container button')].find(x=>/회독/.test(x.textContent)&&x.querySelector('svg[aria-label=\"헷갈림\"]'));if(!b)return false;const cf=b.querySelector('svg[aria-label=\"헷갈림\"] path'),fk=b.querySelector('svg[aria-label=\"페이크\"]');return cf.getAttribute('stroke')==='#EAB308'&&!!fk&&fk.querySelector('path').getAttribute('stroke')==='#2563EB'&&fk.querySelector('text').textContent==='f'&&fk.querySelector('text').getAttribute('fill')==='#DC2626'&&!/🌀|⚠/.test(b.textContent)})()"
 },
 {
  "name": "PC 서랍 · 변리사 기출 과목 해·회 줄에도 🃏·📋 · 📋 누르면 그 해 정리 창",
  "screen": "p2",
  "click": "#trhead button:has-text('변리사 기출')",
  "wait": 1200,
  "expect": "(()=>{const ch=[...document.querySelectorAll('#trlist .trch')];const ok=ch.length>0&&ch.every(x=>x.querySelector('.trcc.jn')&&x.querySelector('.trcc:not(.jn)'));ch[0].querySelector('.trcc.jn').click();const w=[...document.querySelectorAll('.oxwin[data-jnlabels]')].pop();const r=ok&&!!w&&/년 제\\d+회/.test(w.getAttribute('data-jnlabels'));if(w){const h=w.querySelector('.oxwin-head');if(h&&h.lastElementChild)h.lastElementChild.click();}trPickSubj('민법총칙');return r&&!document.querySelector('.oxwin[data-jnlabels]')})()"
 },
 {
  "name": "폰 · 변리사 기출 카드엔 [N] 없음 · 다른 과목엔 있음",
  "screen": "m1",
  "click": "#data-label",
  "expect": "(()=>{const cs=[...document.querySelectorAll('#dashboard-container [data-dfold]')];const ex=cs.find(c=>/변리사 기출/.test(c.querySelector('h2').textContent));return !!ex&&!ex.querySelector('[data-dfoldbtn]')&&cs.filter(c=>c!==ex).every(c=>c.querySelector('[data-dfoldbtn]'))})()"
 },
 {
  "name": "폰 서랍 · [N] 1번 → 장 줄만",
  "screen": "m2",
  "click": "#trhead .trdf",
  "expect": "(()=>{const L=document.getElementById('trlist');const it=[...L.querySelectorAll('.trit')],ch=[...L.querySelectorAll('.trch')];const subj=(document.querySelector('#trhead button.on')||{}).textContent;window.__tr=[trDFoldOf(subj),it.length,ch.length];return trDFoldOf(subj)===1&&it.length===0&&ch.length>0&&document.querySelector('#trhead .trdf').textContent==='[1]'})()"
 },
 {
  "name": "폰 서랍 · [N] 2번 → 장 줄 + 묶음 첫 줄",
  "screen": "m2",
  "click": "#trhead .trdf",
  "expect": "(()=>{const L=document.getElementById('trlist');const it=[...L.querySelectorAll('.trit')],ch=[...L.querySelectorAll('.trch')];const subj=(document.querySelector('#trhead button.on')||{}).textContent;window.__tr=[trDFoldOf(subj),it.length,ch.length];return trDFoldOf(subj)===2&&it.length===document.querySelectorAll('#dashboard-container [data-dfold]')[0].querySelectorAll('[data-jn]').length&&ch.length>0})()"
 },
 {
  "name": "폰 서랍 · [N] 3번 → 다 펼침",
  "screen": "m2",
  "click": "#trhead .trdf",
  "expect": "(()=>{const L=document.getElementById('trlist');const it=[...L.querySelectorAll('.trit')],ch=[...L.querySelectorAll('.trch')];const subj=(document.querySelector('#trhead button.on')||{}).textContent;window.__tr=[trDFoldOf(subj),it.length,ch.length];return trDFoldOf(subj)===0&&it.length>=document.querySelectorAll('#dashboard-container [data-dfold]')[0].querySelectorAll('[data-trrow]').length})()"
 },
 {
  "name": "PC 서랍 · 장 줄 🃏·📋 칩 + 📋 누르면 장 정리 창",
  "screen": "p2",
  "click": "#trlist .trch .trcc.jn",
  "expect": "(()=>{const c=document.querySelector('#trlist .trch');const w=[...document.querySelectorAll('.oxwin[data-jnlabels]')].pop();return !!c.querySelector('.trcc:not(.jn)')&&!!w&&/1\\. 총칙/.test(w.textContent)&&w.getAttribute('data-jnlabels').split('|||').length>1&&getComputedStyle(document.getElementById('tree')).display!=='none'})()"
 },
 {
  "name": "PC 서랍 · 장 줄 🃏 누르면 장 암기노트 창",
  "screen": "p2",
  "click": "#trlist .trch .trcc:not(.jn)",
  "expect": "[...document.querySelectorAll('.oxwin')].some(w=>/🃏 암기노트 · 1\\. 총칙/.test(w.textContent))"
 },
 {
  "name": "폰 서랍 · 긴 장 이름에도 📋 칩 안 잘림",
  "screen": "m2",
  "click": "#trhead .trdf",
  "expect": "(()=>{const r=[...document.querySelectorAll('#trlist .trch')].every(ch=>{const j=ch.querySelector('.trcc.jn');if(!j)return true;const a=j.getBoundingClientRect(),b=ch.getBoundingClientRect();return a.right<=b.right+0.5});trDFold((document.querySelector('#trhead button.on')||{}).textContent);trDFold((document.querySelector('#trhead button.on')||{}).textContent);return r})()"
 },
 {
  "name": "폰 · [N] 1번 → 장 줄만",
  "screen": "m1",
  "click": "[data-dfoldbtn]",
  "expect": "(()=>{const card=document.querySelector('#dashboard-container [data-dfold]');const vis=r=>r.offsetParent!==null;const ch=[...card.querySelectorAll('[data-dchap]')];const hc=ch.filter(x=>x.querySelector('[data-trchap]'));const inR=hc.flatMap(x=>[...x.querySelectorAll('[data-trrow]')]);const flat=ch.filter(x=>!x.querySelector('[data-trchap]')).flatMap(x=>[...x.querySelectorAll('[data-trrow]')]);const jn=inR.filter(r=>r.querySelector('[data-jn]'));const hd=[...card.querySelectorAll('[data-trchap]')];const b=card.querySelector('[data-dfoldbtn]'),h2=card.querySelector('h2');window.__df=[card.getAttribute('data-dfold'),inR.filter(vis).length,jn.length,flat.filter(vis).length,flat.length,hd.filter(vis).length,hd.length];return b.parentElement===h2&&getComputedStyle(b).backgroundColor==='rgba(0, 0, 0, 0)'&&card.getAttribute('data-dfold')==='1'&&b.textContent==='[1]'&&inR.filter(vis).length===0&&flat.every(vis)&&hd.every(vis)})()"
 },
 {
  "name": "폰 · [N] 2번 → 장 줄 + 🃏·📋 칩 줄",
  "screen": "m1",
  "click": "[data-dfoldbtn]",
  "expect": "(()=>{const card=document.querySelector('#dashboard-container [data-dfold]');const vis=r=>r.offsetParent!==null;const ch=[...card.querySelectorAll('[data-dchap]')];const hc=ch.filter(x=>x.querySelector('[data-trchap]'));const inR=hc.flatMap(x=>[...x.querySelectorAll('[data-trrow]')]);const flat=ch.filter(x=>!x.querySelector('[data-trchap]')).flatMap(x=>[...x.querySelectorAll('[data-trrow]')]);const jn=inR.filter(r=>r.querySelector('[data-jn]'));const hd=[...card.querySelectorAll('[data-trchap]')];const b=card.querySelector('[data-dfoldbtn]'),h2=card.querySelector('h2');window.__df=[card.getAttribute('data-dfold'),inR.filter(vis).length,jn.length,flat.filter(vis).length,flat.length,hd.filter(vis).length,hd.length];return b.parentElement===h2&&getComputedStyle(b).backgroundColor==='rgba(0, 0, 0, 0)'&&card.getAttribute('data-dfold')==='2'&&inR.filter(vis).length===jn.length&&jn.every(vis)&&jn.length>0&&jn.length<inR.length&&hd.every(vis)&&flat.every(vis)})()"
 },
 {
  "name": "폰 · [N] 3번 → 다 펼침",
  "screen": "m1",
  "click": "[data-dfoldbtn]",
  "expect": "(()=>{const card=document.querySelector('#dashboard-container [data-dfold]');const vis=r=>r.offsetParent!==null;const ch=[...card.querySelectorAll('[data-dchap]')];const hc=ch.filter(x=>x.querySelector('[data-trchap]'));const inR=hc.flatMap(x=>[...x.querySelectorAll('[data-trrow]')]);const flat=ch.filter(x=>!x.querySelector('[data-trchap]')).flatMap(x=>[...x.querySelectorAll('[data-trrow]')]);const jn=inR.filter(r=>r.querySelector('[data-jn]'));const hd=[...card.querySelectorAll('[data-trchap]')];const b=card.querySelector('[data-dfoldbtn]'),h2=card.querySelector('h2');window.__df=[card.getAttribute('data-dfold'),inR.filter(vis).length,jn.length,flat.filter(vis).length,flat.length,hd.filter(vis).length,hd.length];return b.parentElement===h2&&getComputedStyle(b).backgroundColor==='rgba(0, 0, 0, 0)'&&card.getAttribute('data-dfold')==='0'&&inR.every(vis)&&flat.every(vis)})()"
 },
 {
  "name": "PC · [N] 1번 → 장 줄만",
  "screen": "p1",
  "click": "[data-dfoldbtn]",
  "expect": "(()=>{const card=document.querySelector('#dashboard-container [data-dfold]');const vis=r=>r.offsetParent!==null;const ch=[...card.querySelectorAll('[data-dchap]')];const hc=ch.filter(x=>x.querySelector('[data-trchap]'));const inR=hc.flatMap(x=>[...x.querySelectorAll('[data-trrow]')]);const flat=ch.filter(x=>!x.querySelector('[data-trchap]')).flatMap(x=>[...x.querySelectorAll('[data-trrow]')]);const jn=inR.filter(r=>r.querySelector('[data-jn]'));const hd=[...card.querySelectorAll('[data-trchap]')];const b=card.querySelector('[data-dfoldbtn]'),h2=card.querySelector('h2');window.__df=[card.getAttribute('data-dfold'),inR.filter(vis).length,jn.length,flat.filter(vis).length,flat.length,hd.filter(vis).length,hd.length];return b.parentElement===h2&&getComputedStyle(b).backgroundColor==='rgba(0, 0, 0, 0)'&&card.getAttribute('data-dfold')==='1'&&inR.filter(vis).length===0&&hd.every(vis)})()"
 },
 {
  "name": "폰 · 과목 제목 칸 위아래 4px",
  "screen": "m1",
  "click": "#data-label",
  "expect": "(()=>{const h=[...document.querySelectorAll('#dashboard-container h2')][0].parentElement;const r=h.getBoundingClientRect(),cs=getComputedStyle(h);window.__hh=[r.height,cs.paddingTop,cs.paddingBottom];return cs.paddingTop==='4px'&&cs.paddingBottom==='4px'&&r.height<=34})()"
 },
 {
  "name": "PC · 과목 제목 칸 위아래 4px",
  "screen": "p1",
  "click": "#data-label",
  "expect": "(()=>{const h=[...document.querySelectorAll('#dashboard-container h2')][0].parentElement;const r=h.getBoundingClientRect(),cs=getComputedStyle(h);window.__hh=[r.height,cs.paddingTop,cs.paddingBottom];return cs.paddingTop==='4px'&&cs.paddingBottom==='4px'&&r.height<=34})()"
 },
 {
  "name": "폰 · 「필터 ▾」 + 정정 칩 한 줄",
  "screen": "m1",
  "click": "#data-label",
  "expect": "(()=>{const s=document.getElementById('review-filter'),lab=s.parentElement,row=lab.closest('div.border-b'),fx=document.querySelector('#fix-chip-slot button'),w=document.getElementById('weak-count').closest('button');const a=w.getBoundingClientRect(),b=lab.getBoundingClientRect(),f=fx&&fx.getBoundingClientRect();return lab.textContent.replace(/\\s+/g,' ').trim().startsWith('필터 ▾')&&getComputedStyle(s).opacity==='0'&&!!fx&&f.top<a.bottom&&f.bottom>a.top&&b.top<a.bottom&&f.left>=b.right&&row.scrollWidth<=row.clientWidth&&f.right<=innerWidth&&!document.querySelector('#dashboard-container > div.mb-3.flex.justify-end')})()"
 },
 {
  "name": "PC · 「필터 ▾」 + 정정 칩 한 줄",
  "screen": "p1",
  "click": "#data-label",
  "expect": "(()=>{const s=document.getElementById('review-filter'),lab=s.parentElement,row=lab.closest('div.border-b'),fx=document.querySelector('#fix-chip-slot button'),w=document.getElementById('weak-count').closest('button');const a=w.getBoundingClientRect(),b=lab.getBoundingClientRect(),f=fx&&fx.getBoundingClientRect();return lab.textContent.replace(/\\s+/g,' ').trim().startsWith('필터 ▾')&&getComputedStyle(s).opacity==='0'&&!!fx&&f.top<a.bottom&&f.bottom>a.top&&b.top<a.bottom&&f.left>=b.right&&row.scrollWidth<=row.clientWidth&&f.right<=innerWidth&&!document.querySelector('#dashboard-container > div.mb-3.flex.justify-end')})()"
 },
 {
  "name": "폰 · 서랍 손잡이 ①② (접힘 6·30px 열림 · 열림 터치 6px 닫힘 · 마우스 6px 끌기)",
  "screen": "m1",
  "click": "#data-label",
  "expect": "(()=>{const g=document.getElementById('trGrip'),b=g.getBoundingClientRect(),y=b.top+200,x=b.left+6;const run=(fold,type,dx)=>{trFold(fold);const P=(t,xx)=>g.dispatchEvent(new PointerEvent(t,{bubbles:true,cancelable:true,clientX:xx,clientY:y,pointerId:7,pointerType:type,isPrimary:true,buttons:t==='pointerup'?0:1}));P('pointerdown',x);if(dx)P('pointermove',x+dx);P('pointerup',x+dx);return !document.getElementById('tree').classList.contains('fold')};const r=[run(true,'touch',6),run(true,'touch',30),run(true,'mouse',30),run(false,'touch',6),run(false,'mouse',6)];trFold(true);window.__gr=r;return r[0]&&r[1]&&r[2]&&!r[3]&&r[4]})()"
 },
 {
  "name": "PC · 서랍 손잡이 ①② 같은 잣대",
  "screen": "p2",
  "click": "#data-label",
  "expect": "(()=>{const g=document.getElementById('trGrip'),b=g.getBoundingClientRect(),y=b.top+200,x=b.left+6;const run=(fold,type,dx)=>{trFold(fold);const P=(t,xx)=>g.dispatchEvent(new PointerEvent(t,{bubbles:true,cancelable:true,clientX:xx,clientY:y,pointerId:7,pointerType:type,isPrimary:true,buttons:t==='pointerup'?0:1}));P('pointerdown',x);if(dx)P('pointermove',x+dx);P('pointerup',x+dx);return !document.getElementById('tree').classList.contains('fold')};const r=[run(true,'touch',6),run(true,'touch',30),run(true,'mouse',30),run(false,'touch',6),run(false,'mouse',6)];trFold(false);window.__gr=r;return r[0]&&r[1]&&r[2]&&!r[3]&&r[4]})()"
 },
 {
  "name": "폰 · 약점~필터 한 줄",
  "screen": "m1",
  "click": "#review-filter",
  "expect": "(()=>{const s=document.getElementById('review-filter'),row=s.closest('div.border-b'),w=document.getElementById('weak-count').closest('button');const a=w.getBoundingClientRect(),b=s.getBoundingClientRect();return !/빠른 실행/.test(row.textContent)&&b.top<a.bottom&&b.bottom>a.top&&row.scrollWidth<=row.clientWidth&&b.right<=innerWidth})()"
 },
 {
  "name": "PC · 약점~필터 한 줄",
  "screen": "p1",
  "click": "#review-filter",
  "expect": "(()=>{const s=document.getElementById('review-filter'),row=s.closest('div.border-b'),w=document.getElementById('weak-count').closest('button');const a=w.getBoundingClientRect(),b=s.getBoundingClientRect();return !/빠른 실행/.test(row.textContent)&&b.top<a.bottom&&b.bottom>a.top})()"
 },
 {
  "name": "폰 · 제목 오른쪽 한 줄",
  "screen": "m1",
  "click": "#data-label",
  "expect": "(()=>{const a=document.querySelector('#home-screen h1').getBoundingClientRect(),b=document.getElementById('data-label').getBoundingClientRect();return b.left>=a.right&&b.top<a.bottom&&b.bottom>a.top&&b.right<=innerWidth})()"
 },
 {
  "name": "PC · 제목 오른쪽 한 줄",
  "screen": "p1",
  "click": "#data-label",
  "expect": "(()=>{const a=document.querySelector('#home-screen h1').getBoundingClientRect(),b=document.getElementById('data-label').getBoundingClientRect(),s=document.getElementById('data-label');return b.left>=a.right&&b.top<a.bottom&&b.bottom>a.top&&s.scrollWidth<=s.clientWidth})()"
 },
 {
  "name": "폰 · 물권 칩 → 목록 물권만",
  "screen": "m1",
  "click": "#hm-subjects button",
  "nth": 2,
  "expect": "hmSubject==='물권법'",
  "same": "#dashboard-container h2"
 },
 {
  "name": "PC · 서랍 손잡이 → 열림",
  "screen": "p1",
  "click": "#trGrip",
  "expect": "!document.getElementById('tree').classList.contains('fold')"
 },
 {
  "name": "PC 서랍 열림 · 검색 「선의」",
  "screen": "p2",
  "type": "#search-input",
  "text": "선의",
  "expect": "!document.getElementById('search-results').classList.contains('hide')",
  "same": "#search-results > *"
 },
 {
  "name": "PC 서랍 열림 · 채각 칩",
  "screen": "p2",
  "click": "#hm-subjects button",
  "nth": 4,
  "expect": "hmSubject==='채권각론'",
  "same": "#dashboard-container h2"
 },
 {
  "name": "폰 · 🔥 약점 → 문제 화면",
  "screen": "m1",
  "click": "button:has-text('약점')",
  "expect": "!document.getElementById('quiz-screen').classList.contains('hide')"
 },
 {
  "name": "폰 · 문제풀이 태그 헷갈림 노랑 · 페이크 파란 세모 빨간 f",
  "screen": "m1",
  "click": "#progress-text",
  "expect": "(()=>{const cf=document.querySelector('[id^=\"tag-confuse-\"] svg path'),fk=document.querySelector('[id^=\"tag-fake-\"] svg');return !!cf&&cf.getAttribute('stroke')==='#EAB308'&&!!fk&&fk.querySelector('text').textContent==='f'&&fk.querySelector('text').getAttribute('fill')==='#DC2626'&&fk.querySelector('path').getAttribute('stroke')==='#2563EB'})()"
 }
]''')

RES = []    # (관문, 이름, 새 판 판정 True/False/None(INFO), 값)
YARD = []   # (관문, 이름, 바탕 판정, 바탕이 PASS 여야 하나 — True · False · None(못 가르는 칸 · 적기만))
ERRS = {}
STEP = []
T0 = time.time()


def _s(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


def T(g, name, ok, detail=''):
    RES.append((g, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', g, name, _s(detail)[:900]), flush=True)
    return bool(ok)


def N(g, name, detail=''):
    RES.append((g, name, None, detail))
    print('INFO | %s · %s | %s' % (g, name, _s(detail)[:900]), flush=True)


def Y(g, name, okb, want_pass=False):
    YARD.append((g, name, bool(okb), want_pass))


LABEL_JS = """() => ({label: (document.getElementById('search-mode-m') || {}).textContent || null,
  memoCount: (typeof memoCount === 'function') ? memoCount() : null, puts: (window.__PUTS || []).length})"""


def want(k):
    return not ONLY or k in ONLY


def git(*a):
    return subprocess.run(['git', '-C', _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def app_src(x):
    if os.path.isfile(x):
        return open(x, 'rb').read().decode('utf-8')
    b = git('show', x + ':' + REL)
    return b.decode('utf-8') if b else None


def md5lf(s):
    return hashlib.md5(s.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def data_files():
    out = {}
    for f in DFILES:
        r = subprocess.run(['git', '-C', SPD, 'show', DREV + ':' + f], capture_output=True)
        if r.returncode or not r.stdout:
            return None, f
        out[f] = r.stdout
    return out, None


# ════════════════════════ 틀 — 시안 도구 snap.py 의 SHIM(같은 꼴) + 오류 받기 · alert/confirm 막기 ════════════════════════
SHIM = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__ALERTS=[];window.alert=function(m){__ALERTS.push(String(m));};window.confirm=function(m){__ALERTS.push('confirm '+String(m));return false;};window.prompt=function(){return null;};
window.__PUTS=[];
(function(){
 try{var c=JSON.parse(localStorage.getItem('tt.cfg')||'{}');if(!c.token){c.token='demo';c.person=c.person||'꼬까';localStorage.setItem('tt.cfg',JSON.stringify(c))}}catch(e){}
 var FMAP=__FMAP__, REPO=__REPO__;
 var of=window.fetch.bind(window);
 window.fetch=async function(u,o){
  var url=String(u&&u.url||u);
  var m=/^https:\/\/api\.github\.com\/repos\/([^\/]+\/[^\/]+)\/contents\/([^?]*)/.exec(url);
  if(!m){ if(/^https?:/.test(url)&&!/cdn\.tailwindcss|cdnjs|jsdelivr|unpkg/.test(url)) return new Response('',{status:404}); return of(u,o); }
  var repo=m[1], path=decodeURIComponent(m[2]), meth=String((o&&o.method)||'GET').toUpperCase();
  var hd=(o&&o.headers)||{}, acc=String(hd.Accept||hd.accept||'');
  var J={'Content-Type':'application/json'};
  if(meth==='PUT'){ window.__PUTS.push(path); return new Response(JSON.stringify({content:{sha:'demo-'+Date.now()}}),{status:200,headers:J}); }
  if(repo!==REPO) return new Response('',{status:404});
  var f=FMAP[path]; if(!f) return new Response('',{status:404});
  if(acc.indexOf('raw')<0) return new Response(JSON.stringify({sha:'demo1-'+path}),{status:200,headers:J});
  try{var r=await of(f); if(!r.ok) return new Response('',{status:404}); return r}catch(e){return new Response('',{status:404})}
 };
})();
</script>"""

SEED_JS = r"""(()=>{ try{ if(localStorage.getItem('__hb_seed')) return; const S=__SEED__;
  for(const k in S) localStorage.setItem(k, typeof S[k]==='string'?S[k]:JSON.stringify(S[k])); localStorage.setItem('__hb_seed','1'); }catch(e){} })();"""

# B2 · B3 — 새 기기 꼴(흡수 표시키 없음) · 글은 지어냄 · 문항 번호는 §0-B 의 실제 사례 자리를 빌림(글은 안 빌림)
GB_MEMO_A, GB_MEMO_B, GB_LOGIC_C = 'Q0258', 'Q0292', 'Q0147'
B2_SEED = {
    'ox_uid_migrated': '1', 'ox_gg_okreset': '1', 'ox_auto_important_v2': '1',
    'ox_q_memos': {GB_MEMO_A: '메모 A — 흡수 뒤 근거에서 지운 글(지어냄)', GB_MEMO_B: '메모 B — 흡수 뒤 src 만 빠진 같은 글(지어냄)'},
    'ox_q_logic': {GB_LOGIC_C: '논리 C — 흡수 뒤 고친 글의 옛 판(지어냄)'},
    'ox_q_geunge': {GB_MEMO_B: [{'k': 'g_%s_hb1' % GB_MEMO_B, 'i': 1, 't': '메모 B — 흡수 뒤 src 만 빠진 같은 글(지어냄)', 'ok': None, 'ts': 1789000000000, 'cs': []}],
                    GB_LOGIC_C: [{'k': 'g_%s_hb1' % GB_LOGIC_C, 'i': 1, 't': '논리 C — 고친 글(지어냄)', 'ok': None, 'ts': 1789000000000, 'cs': []}]},
    'ox_sync_gone': {'ox_q_geunge|' + GB_MEMO_A: 1789000000000},
}
# B5 — 기존 기기 꼴(흡수 표시키 켬 · 바탕도 흡수가 안 돎 → 같은 근거 상태에서 맞댐)
B5_SEED = {'ox_gg_memo_merged': '{"at":1,"moved":0,"links":0}', 'ox_gg_logic_merged': '{"at":1,"moved":0,"links":0}'}

SERVERS = {}


def inject(src, fmap):
    src = src.replace('\r\n', '\n')
    TW = '<script src="https://cdn.tailwindcss.com"></script>'
    if TWCSS and TW in src:
        src = src.replace(TW, '<style>/* harness: Tailwind v3 사본(--tw) */\n' + open(TWCSS, encoding='utf-8').read() + '\n</style>', 1)
    shim = SHIM.replace('__FMAP__', json.dumps(fmap, ensure_ascii=False)).replace('__REPO__', json.dumps(REPO))
    t = re.search(r'<title>[^<]*</title>', src)
    return src[:t.end()] + shim + src[t.end():]   # 시안과 같은 자리(<title> 바로 뒤)


def serve(key, src, data, with_rec=True):
    if key in SERVERS:
        return SERVERS[key][1]
    names = [f for f in DFILES if with_rec or not f.endswith('기록.json')]
    fmap = {f: 'd/%d.json' % DFILES.index(f) for f in names}
    body = inject(src, fmap).encode('utf-8')
    files = {'/minbeop/' + fmap[f]: data[f] for f in names}

    class Hd(SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            p = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
            if p in ('/minbeop/', '/minbeop/index.html'):
                d, code, ct = body, 200, 'text/html; charset=utf-8'
            elif p in files:
                d, code, ct = files[p], 200, 'application/json; charset=utf-8'
            else:
                d, code, ct = b'{"message":"Not Found"}', 404, 'application/json'
            self.send_response(code)
            self.send_header('Content-Type', ct)
            self.send_header('Content-Length', str(len(d)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(d)

    srv = ThreadingHTTPServer(('127.0.0.1', 0), Hd)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[key] = (srv, srv.server_address[1])
    return srv.server_address[1]


def route_fn(r):
    u = r.request.url
    if u.startswith('http://127.0.0.1') or (u.startswith('https://cdn.tailwindcss.com') and not TWCSS):
        return r.continue_()
    return r.abort()


def new_ctx(br, seed=None):
    ctx = br.new_context(viewport={'width': 1100, 'height': 800}, accept_downloads=True)
    ctx.route('**/*', route_fn)
    if seed:
        ctx.add_init_script(SEED_JS.replace('__SEED__', json.dumps(seed, ensure_ascii=False)))
    return ctx


def open_page(ctx, url, view, label):
    pg = ctx.new_page()
    W, H = VIEWS[view]
    pg.set_viewport_size({'width': W, 'height': H})
    pg.set_default_timeout(60000)
    errs = []
    pg.on('pageerror', lambda e: errs.append('page: ' + str(e)[:300]))
    pg.goto(url, wait_until='commit', timeout=120000)
    return {'pg': pg, 'errs': errs, 'label': label}


def boot(sc, setup=None):
    """ready → 첫 동기화 끝(recBusy 풀림) → 2 초 → setup — 걸린 초"""
    pg, t1 = sc['pg'], time.time()
    try:
        pg.wait_for_function('() => ' + READY, timeout=60000, polling=250)
        sc['ready'] = True
    except Exception:
        sc['ready'] = False   # 시안처럼 60 초 뒤엔 그대로 감
    try:
        pg.wait_for_function("() => typeof recBusy !== 'undefined' && !recBusy", timeout=60000, polling=250)
    except Exception:
        pass
    pg.wait_for_timeout(SETTLE)
    if setup:
        sc['setup'] = pg.evaluate("(s) => { try { (0, eval)(s); return true; } catch (e) { return 'ERR ' + e; } }", setup)
    sc['boot_sec'] = round(time.time() - t1, 1)
    return sc['boot_sec']


def idle(pg, extra=1500):
    for _ in range(2):
        try:
            pg.wait_for_function("() => typeof recBusy !== 'undefined' && !recBusy", timeout=60000, polling=250)
        except Exception:
            pass
        pg.wait_for_timeout(extra)


def errs_of(sc):
    try:
        e = sc['pg'].evaluate("() => ({err: (window.__ERR || []).slice(), alerts: (window.__ALERTS || []).slice()})")
    except Exception:
        e = {'err': [], 'alerts': []}
    return sc['errs'] + e['err'], e['alerts']


def shot(sc, tag, name, clip_sel=None):
    try:
        os.makedirs(SHOTS, exist_ok=True)
        f = os.path.join(SHOTS, 'ox_home_tidy_%s_%s.png' % (tag, name))
        pg = sc['pg']
        if clip_sel:
            r = pg.evaluate("(s) => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return {x: b.left + scrollX, y: b.top + scrollY, w: b.width, h: b.height}; }", clip_sel)
            if r and r['h'] > 0:
                W = pg.viewport_size['width']
                pg.screenshot(path=f, full_page=True, clip={'x': 0, 'y': max(0, r['y'] - 8), 'width': W, 'height': min(r['h'] + 16, 3200)})
                return f
        pg.screenshot(path=f)
        return f
    except Exception as e:
        return 'shot err ' + str(e)[:120]


# ════════════════════════ C — 화면 넷 · 시험 스물아홉 ════════════════════════
def run_c(br, tag, src, data):
    port = serve((tag, 'main'), src, data)
    url = 'http://127.0.0.1:%d/minbeop/index.html' % port
    ctx = new_ctx(br)
    S, out = {}, {'tests': [], 'shots': {}}
    t1 = time.time()
    try:
        for sid, view, setup in SCREENS:
            S[sid] = open_page(ctx, url, view, sid)
        for sid, view, setup in SCREENS:
            boot(S[sid], setup)
        out['boot'] = {sid: {'ready': S[sid].get('ready'), 'setup': S[sid].get('setup'), 'sec': S[sid].get('boot_sec')} for sid in S}
        # 「근거 (N)」 글자 vs 실제 memoCount() — 화면 넷이 저장소 하나를 같이 쓰므로 먼저 받은 쪽만 got=true 로 다시 그린다(한 탭 기기와 다름 · 적기만)
        out['label'] = {sid: S[sid]['pg'].evaluate(LABEL_JS) for sid in S}
        STEP.append(('%s 화면 넷 시동' % tag, round(time.time() - t1)))
        if tag == 'NEW':
            out['shots']['m1_home'] = shot(S['m1'], tag, 'phone_home')
            out['shots']['p1_home'] = shot(S['p1'], tag, 'pc_home')
            out['shots']['p2_drawer'] = shot(S['p2'], tag, 'pc_drawer_open')
        else:
            out['shots']['m1_home'] = shot(S['m1'], tag, 'phone_home')
            out['shots']['p1_home'] = shot(S['p1'], tag, 'pc_home')
        t2 = time.time()
        for i, t in enumerate(TESTS, 1):
            sc = S[t['screen']]
            pg = sc['pg']
            t3 = time.time()
            try:
                pg.evaluate("() => { window.__df = window.__tr = window.__hh = window.__gr = undefined; }")
            except Exception:
                pass
            try:
                loc = pg.locator(t.get('click') or t.get('type')).nth(t.get('nth', 0))
                loc.scroll_into_view_if_needed(timeout=5000)
                loc.click(timeout=5000)
                if 'type' in t:
                    pg.keyboard.type(t['text'], delay=30)
                    if t.get('enter'):
                        pg.keyboard.press('Enter')
                pg.wait_for_timeout(t.get('wait', 1000))
                ok = pg.evaluate("(x) => { try { return !!(0, eval)(x); } catch (e) { return 'ERR ' + e; } }", t['expect'])
            except Exception as ex:
                ok = 'ERR ' + str(ex).strip().split('\n')[0][:160]
            same = None
            try:
                if t.get('same'):
                    same = pg.evaluate("(s) => document.querySelectorAll(s).length", t['same'])
                vals = pg.evaluate("() => ({df: window.__df, tr: window.__tr, hh: window.__hh, gr: window.__gr})")
                vals = {k: v for k, v in (vals or {}).items() if v is not None}
            except Exception as ex:
                vals = {'err': str(ex)[:100]}
            out['tests'].append({'i': i, 'name': t['name'], 'screen': t['screen'], 'ok': ok, 'same': same, 'vals': vals, 'sec': round(time.time() - t3, 1)})
            if tag == 'NEW' and t['name'] in SHOT_AFTER:
                sid, nm = SHOT_AFTER[t['name']]
                out['shots'][nm] = shot(S[sid], tag, 'phone_' + nm, None if sid == 'm2' else '#dashboard-container [data-dfold]')
        STEP.append(('%s 시험 스물아홉' % tag, round(time.time() - t2)))
    except Exception:
        out['err'] = traceback.format_exc()[-1500:]
    for sid in S:
        e, al = errs_of(S[sid])
        ERRS.setdefault('%s %s' % (tag, sid), []).extend(e)
        out.setdefault('alerts', {})[sid] = al[:5]
    try:
        ctx.close()
    except Exception:
        pass
    return out


# ════════════════════════ B — 메모·논리 걷기 ════════════════════════
B_SITES = re.compile(r'ggMemoMergeOnce|ggLogicMergeOnce|ggMemoMergeBoot|ggLogicMergeBoot|ggMergeBoots|ox_gg_memo_merged|ox_gg_logic_merged')


def b1(src):
    L = src.replace('\r\n', '\n').split('\n')
    names = sorted({m.group(0) for m in B_SITES.finditer(src)})
    nn = len(B_SITES.findall(src))
    keep = []
    for i, x in enumerate(L, 1):
        if 'ox_q_memos' in x or 'ox_q_logic' in x:
            kind = 'SYNC_KEYS' if 'const SYNC_KEYS' in x else ('migrateLegacyRecords' if "for (const K of ['ox_q_tags', 'ox_q_memos'" in x else '그 밖')
            keep.append([i, kind])
    other = [k for k in keep if k[1] == '그 밖']
    ok = nn == 0 and not other and sorted(k[1] for k in keep) == ['SYNC_KEYS', 'migrateLegacyRecords']
    return ok, {'흡수 이름 걸림': nn, '이름': names, '저장소 이름 줄': keep}


B2_READ = """() => { const g = k => localStorage.getItem(k);
  return {geunge: g('ox_q_geunge'), memos: g('ox_q_memos'), logic: g('ox_q_logic'), reflinks: g('ox_q_reflinks'),
          mk1: g('ox_gg_memo_merged'), mk2: g('ox_gg_logic_merged'), puts: (window.__PUTS || []).slice(), q: quizData.length}; }"""

B3_RUN = """() => { const get = k => { try { return JSON.parse(localStorage.getItem(k) || '{}') || {}; } catch (e) { return {}; } };
  const pick = (o, ks) => { const r = {}; ks.forEach(k => { if (Object.prototype.hasOwnProperty.call(o, k)) r[k] = o[k]; }); return r; };
  const U = ['Q0001', 'Q0258', 'Q0292'];
  const before = {m: get('ox_q_memos'), l: get('ox_q_logic')};
  mergeExcelRecords([{uid: 'Q0001', 메모: '엑셀 메모 1(지어냄)', 논리: '엑셀 논리 1(지어냄)', 페이크: 'Y', 연결: 'Q0002, Q0003'},
                     {uid: 'Q0258', 메모: '엑셀 메모 2(지어냄)', 논리: '', 중요: 'Y'}], false);
  const a = {m: get('ox_q_memos'), l: get('ox_q_logic'), t: pick(get('ox_q_tags'), U), k: pick(get('ox_q_links'), U)};
  mergeExcelRecords([{uid: 'Q0001', 메모: '', 논리: '엑셀 논리 덮어쓰기(지어냄)', 암기: 'Y', 연결: ''},
                     {uid: 'Q0258', 메모: '', 논리: ''},
                     {uid: 'Q0292', 메모: '엑셀 메모 3(지어냄)', 논리: '엑셀 논리 3(지어냄)', 개념: 'Y', 연결: 'Q0001'}], true);
  const b = {m: get('ox_q_memos'), l: get('ox_q_logic'), t: pick(get('ox_q_tags'), U), k: pick(get('ox_q_links'), U)};
  return {before, a, b}; }"""

B4_RUN = """async () => {
  const o = XLSX.utils.aoa_to_sheet; let cap = null;
  XLSX.utils.aoa_to_sheet = function (a) { cap = a; return o.apply(this, arguments); };
  const sha = async s => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)))).map(b => b.toString(16).padStart(2, '0')).join('').slice(0, 16);
  const rows = (await dbGet('rows')) || [];
  const run = async () => { cap = null; await exportExcelFile(); return cap; };
  localStorage.setItem('ox_q_memos', '{}'); localStorage.setItem('ox_q_logic', '{}');
  const A = await run();
  if (!A) { XLSX.utils.aoa_to_sheet = o; return {err: '내보내기 aoa 없음', rows: rows.length}; }
  const H = A[0], im = H.indexOf('메모'), il = H.indexOf('논리'), iu = H.indexOf('uid');
  const w = (r, c) => String(r[c] ?? '');
  let bad = 0, mN = 0, lN = 0;
  for (let i = 0; i < rows.length; i++) {
    const g = A[i + 1] || [];
    if (String(g[im] ?? '') !== w(rows[i], '메모') || String(g[il] ?? '') !== w(rows[i], '논리')) bad++;
    if (w(rows[i], '메모')) mN++; if (w(rows[i], '논리')) lN++;
  }
  const hA = await sha(JSON.stringify(A));
  const u1 = String(rows[0].uid), u2 = String(rows[1].uid);
  localStorage.setItem('ox_q_memos', JSON.stringify({[u1]: '앱 메모(지어냄 · 내보내기 헛잣대)'}));
  localStorage.setItem('ox_q_logic', JSON.stringify({[u2]: '앱 논리(지어냄 · 내보내기 헛잣대)'}));
  const B = await run();
  XLSX.utils.aoa_to_sheet = o;
  const rowOf = u => (B || []).find((r, i) => i > 0 && String(r[iu]) === u) || [];
  return {cols: H, iMemo: im, iLogic: il, rows: rows.length, out: A.length - 1, bad, rowsWithMemo: mN, rowsWithLogic: lN, hashA: hA,
          b: {u1, got1: String(rowOf(u1)[im] ?? ''), want1: w(rows[0], '메모'), u2, got2: String(rowOf(u2)[il] ?? ''), want2: w(rows[1], '논리')}}; }"""

B5_RUN = """async () => {
  const T = e => e ? (e.textContent || '').replace(/\\s+/g, ' ').trim() : '';
  const W = ms => new Promise(r => setTimeout(r, ms));
  const rs = refStore();
  const owners = Object.keys(rs).sort().filter(o => refOf(o, 'geunge').length && quizData.some(q => String(q.id) === o));
  if (!owners.length) return {err: '근거 연결 있는 문항 없음'};
  const owner = owners[0], target = refOf(owner, 'geunge')[0];
  const out = {owner, target, nOwners: owners.length, refs0: refOf(owner, 'geunge').slice(),
               label0: T(document.getElementById('search-mode-m')), memoCount0: memoCount()};
  const host = document.createElement('div'); host.style.cssText = 'position:fixed;left:-9999px;top:0;width:600px';
  host.innerHTML = '<input id="link-search-geunge-' + owner + '"><div id="link-results-geunge-' + owner + '"></div>';
  document.body.appendChild(host);
  out.ls = {};
  for (const term of ['선의', '대리', '취소']) {
    document.getElementById('link-search-geunge-' + owner).value = term;
    linkSearch(owner, 'geunge', '');
    const box = document.getElementById('link-results-geunge-' + owner);
    out.ls[term] = {n: box.querySelectorAll('button').length, t: T(box).slice(0, 4000)};
  }
  host.remove();
  out.sr = {};
  for (const [mode, term] of [['q', '선의'], ['m', '선의'], ['m', '대리']]) {
    setSearchMode(mode); const si = document.getElementById('search-input'); si.value = term; runSearch();
    out.sr[mode + ':' + term] = {cnt: T(document.getElementById('search-count')), n: document.querySelectorAll('#search-results > button').length,
                                 t: T(document.getElementById('search-results')).slice(0, 6000)};
  }
  setSearchMode('q'); document.getElementById('search-input').value = ''; runSearch();
  out.refText = refTextOf(target, 'geunge');
  document.querySelectorAll('.oxwin').forEach(w => w.remove());
  openQPopup(owner); await W(500);
  const pw = document.getElementById('oxwin-q-' + owner);
  out.popup = {shown: !!pw, chips: [...document.querySelectorAll('[id^="qp-gg-chip-' + owner + '-"]')].map(T),
               refChips: pw ? [...pw.querySelectorAll('span,button')].filter(e => /^🔗 Q\\d/.test(T(e))).map(T).slice(0, 20) : [],
               text: T(pw).slice(0, 6000)};
  document.querySelectorAll('.oxwin').forEach(w => w.remove());
  useWin('geunge', target, owner); await W(400);
  out.use0 = T(document.getElementById('oxwin-use-geunge-' + target)).slice(0, 3000);
  useUnlink('geunge', owner, target); await W(500);
  out.after = {refs: refOf(owner, 'geunge').slice(), owners: useOwners('geunge', target).length,
               use1: T(document.getElementById('oxwin-use-geunge-' + target)).slice(0, 3000)};
  return out; }"""


def run_b(br, tag, src, data):
    out = {}
    # B2 — 새 기기 꼴 · 원격 기록 없음(첫 올림) · 시동 + 첫 동기화 뒤
    if want('B2') or want('B3') or want('B4'):
        t1 = time.time()
        port = serve((tag, 'nolog'), src, data, with_rec=False)
        ctx = new_ctx(br, B2_SEED)
        sc = open_page(ctx, 'http://127.0.0.1:%d/minbeop/index.html' % port, 'pc', 'b2')
        try:
            boot(sc)
            idle(sc['pg'], 2500)
            out['B2'] = sc['pg'].evaluate(B2_READ)
            STEP.append(('%s B2 새 기기 시동' % tag, round(time.time() - t1)))
            if want('B3'):
                t1 = time.time()
                out['B3'] = sc['pg'].evaluate(B3_RUN)
                STEP.append(('%s B3 엑셀 불러오기' % tag, round(time.time() - t1)))
            if want('B4'):
                t1 = time.time()
                out['B4'] = sc['pg'].evaluate(B4_RUN)
                STEP.append(('%s B4 엑셀 내보내기' % tag, round(time.time() - t1)))
        except Exception:
            out['errB'] = traceback.format_exc()[-1500:]
        e, al = errs_of(sc)
        ERRS.setdefault('%s B2·B3·B4' % tag, []).extend(e)
        try:
            ctx.close()
        except Exception:
            pass
    # B5 — 기존 기기 꼴(표시키 켬) · 같은 데이터
    if want('B5'):
        t1 = time.time()
        port = serve((tag, 'main'), src, data)
        ctx = new_ctx(br, B5_SEED)
        sc = open_page(ctx, 'http://127.0.0.1:%d/minbeop/index.html' % port, 'pc', 'b5')
        try:
            boot(sc)
            idle(sc['pg'], 1500)
            out['B5'] = sc['pg'].evaluate(B5_RUN)
        except Exception:
            out['errB5'] = traceback.format_exc()[-1500:]
        e, al = errs_of(sc)
        ERRS.setdefault('%s B5' % tag, []).extend(e)
        try:
            ctx.close()
        except Exception:
            pass
        STEP.append(('%s B5 근거 연결·검색' % tag, round(time.time() - t1)))
    return out


# ════════════════════════ 판정 ════════════════════════
def tok(x):
    return x is True


def judge_c(n, b):
    if n.get('err'):
        T('C', '새 판 하네스 실행', False, n['err'])
    if b and b.get('err'):
        T('C', '바탕 하네스 실행', False, b['err'])
    N('C', '새 판 시동(ready · setup · 초)', n.get('boot'))
    if b:
        N('C', '바탕 시동(ready · setup · 초)', b.get('boot'))
    N('C', '「근거 (N)」 글자 · 실제 memoCount() · 가짜 올림 수 — 화면 넷 한 저장소(먼저 받은 쪽만 다시 그림 · 적기만)', {'new': n.get('label'), 'base': (b or {}).get('label')})
    bt = {t['i']: t for t in (b or {}).get('tests', [])}
    for t in n.get('tests', []):
        bb = bt.get(t['i'])
        det = {'new': {k: t[k] for k in ('ok', 'same', 'vals', 'sec') if t.get(k) not in (None, {}, [])}}
        if bb:
            det['base'] = {k: bb[k] for k in ('ok', 'same', 'vals', 'sec') if bb.get(k) not in (None, {}, [])}
        T('C', '%02d %s [%s]' % (t['i'], t['name'], t['screen']), tok(t['ok']), det)
        if bb:
            Y('C', '%02d %s' % (t['i'], t['name']), tok(bb['ok']), True if t['name'] in UNCHANGED else (None if t['name'] in NONDISC else False))
        if t['name'] in NONDISC and t.get('same') is not None:   # 보강 — 칩 시험의 가르는 값(목록 과목 카드 수)
            T('C', '%02d+ %s — 목록 과목 카드 1 개(same %s)' % (t['i'], t['name'], t.get('same')), t.get('same') == 1, {'new': t.get('same'), 'base': bb and bb.get('same')})
            if bb:
                Y('C', '%02d+ %s 목록 과목 카드 1 개' % (t['i'], t['name']), bb.get('same') == 1)
    if len(n.get('tests', [])) != len(TESTS):
        T('C', '시험 수 = 지시서 %d' % len(TESTS), False, len(n.get('tests', [])))


def same_json(a, b):
    return json.dumps(a, ensure_ascii=False, sort_keys=True) == json.dumps(b, ensure_ascii=False, sort_keys=True)


def judge_b(sn, sb, n, b):
    if want('B1'):
        okn, dn = b1(sn)
        T('B1', '흡수 이름 grep 0 · ox_q_memos · ox_q_logic = SYNC_KEYS · migrateLegacyRecords 두 줄만', okn, {'new': dn, 'base': sb and b1(sb)[1]})
        if sb:
            Y('B1', '흡수 이름 grep 0', b1(sb)[0])
    for k in ('errB', 'errB5'):
        if n.get(k):
            T('B', '새 판 ' + k, False, n[k])
        if b and b.get(k):
            T('B', '바탕 ' + k, False, b[k])
    seedg = B2_SEED['ox_q_geunge']

    def b2ok(x):
        if not x:
            return False
        g = json.loads(x.get('geunge') or '{}')
        return (same_json(g, seedg) and not x.get('mk1') and not x.get('mk2') and same_json(json.loads(x.get('memos') or '{}'), B2_SEED['ox_q_memos'])
                and same_json(json.loads(x.get('logic') or '{}'), B2_SEED['ox_q_logic']) and 'minbeop/기록.json' in (x.get('puts') or []) and x.get('q', 0) > 0)

    def b2view(x):
        if not x:
            return x
        g = json.loads(x.get('geunge') or '{}')
        return {'근거': {u: [[it.get('t'), it.get('src')] for it in g.get(u, [])] for u in (GB_MEMO_A, GB_MEMO_B, GB_LOGIC_C)},
                '표시키': [x.get('mk1'), x.get('mk2')], '올림': x.get('puts'), '문항': x.get('q')}
    if want('B2'):
        T('B2', '새 기기 꼴 시동 + 첫 동기화 뒤 근거 무변(메모 A 묘비 · 메모 B 같은 글 · 논리 C 고친 글) · 표시키 안 생김 · 원문 두 저장소 무변',
          b2ok(n.get('B2')), {'new': b2view(n.get('B2')), 'base': b and b2view(b.get('B2'))})
        if b:
            Y('B2', '새 기기 꼴 근거 무변', b2ok(b.get('B2')))
    if want('B3'):
        x, y = n.get('B3'), (b or {}).get('B3')

        def b3ok(x):
            return bool(x) and same_json(x['a']['m'], x['before']['m']) and same_json(x['a']['l'], x['before']['l']) and same_json(x['b']['m'], x['before']['m']) and same_json(x['b']['l'], x['before']['l'])

        tl = lambda v: v and {'a': {'t': v['a']['t'], 'k': v['a']['k']}, 'b': {'t': v['b']['t'], 'k': v['b']['k']}}
        # 연결은 「들어감」 — 시동 때 서버 문항의 「연결」 열이 이미 넣은 것(Q0001 → Q4737)에 더해진다(보충 = 합집합)
        tl_ok = (bool(x) and x['a']['t'].get('Q0001', {}).get('fake') is True and {'Q0002', 'Q0003'} <= set(x['a']['k'].get('Q0001') or [])
                 and 'Q0001' not in x['b']['k'] and x['b']['k'].get('Q0292') == ['Q0001'] and (x['b']['t'].get('Q0001') or {}).get('memo') is True)
        dk = lambda o, p: sorted(k for k in set(o) | set(p) if o.get(k) != p.get(k))
        T('B3', '엑셀 불러오기(보충 → 덮어쓰기) — ox_q_memos · ox_q_logic 무변 · 태그 · 연결은 들어감' + (' · 태그 · 연결 = 바탕과 같음' if y else ''),
          b3ok(x) and tl_ok and (not y or same_json(tl(x), tl(y))),
          {'new': x and {'메모 바뀐 칸': dk(x['before']['m'], x['b']['m']) + dk(x['before']['m'], x['a']['m']), '논리 바뀐 칸': dk(x['before']['l'], x['b']['l']) + dk(x['before']['l'], x['a']['l']),
                         '메모 수': len(x['before']['m']), '논리 수': len(x['before']['l']), **tl(x)},
           'base': y and {'메모 바뀐 칸(보충 · 덮어쓰기)': [dk(y['before']['m'], y['a']['m']), dk(y['before']['m'], y['b']['m'])],
                          '논리 바뀐 칸(보충 · 덮어쓰기)': [dk(y['before']['l'], y['a']['l']), dk(y['before']['l'], y['b']['l'])],
                          '논리 수(시동 때 서버 문항 「논리」 열이 이미 넣음)': len(y['before']['l']), '태그·연결 같음': same_json(tl(x), tl(y)) if x else None}})
        if y:
            Y('B3', '엑셀 불러오기 두 저장소 무변', b3ok(y))
    if want('B4'):
        x, y = n.get('B4'), (b or {}).get('B4')

        def b4a(x):
            return bool(x) and not x.get('err') and '메모' in x['cols'] and '논리' in x['cols'] and x['bad'] == 0 and x['out'] == x['rows'] > 0

        def b4b(x):
            return bool(x) and not x.get('err') and x['b']['got1'] == x['b']['want1'] and x['b']['got2'] == x['b']['want2']

        short = lambda v: v and {k: v.get(k) for k in ('rows', 'out', 'bad', 'rowsWithMemo', 'rowsWithLogic', 'iMemo', 'iLogic', 'hashA', 'err')}
        T('B4', '엑셀 내보내기(두 저장소 빔) — 「메모」「논리」 열 남음 · 칸 = 원본 행 그대로(전 행)' + (' · 바탕과 aoa 같음' if y else ''),
          b4a(x) and (not y or (x['hashA'] == y['hashA'] and x['cols'] == y['cols'])), {'new': short(x), 'base': short(y)})
        if y:
            Y('B4', '엑셀 내보내기 두 저장소 빔(무변 칸)', b4a(y), True)
        T('B4', '엑셀 내보내기(두 저장소에 다른 글) — 「메모」「논리」 칸 = 원본 행(저장소 글 안 나감)', b4b(x), {'new': x and x.get('b'), 'base': y and y.get('b')})
        if y:
            Y('B4', '엑셀 내보내기 두 저장소 글 안 나감', b4b(y))
    if want('B5'):
        x, y = n.get('B5'), (b or {}).get('B5')
        nonvac = bool(x) and not x.get('err') and any(v['n'] for v in x['ls'].values()) and x['sr']['q:선의']['n'] > 0 and x['popup']['shown'] and x['use0'] and len(x['after']['refs']) == len(x['refs0']) - 1
        T('B5', '근거 연결 검색(geunge) · 문제/근거 검색 · refTextOf · 팝업 근거 칸 · 쓰임 창 · 연결 끊기 — 바탕과 글자까지 같음' + ('' if y else '(바탕 안 돎)'),
          nonvac and (not y or same_json(x, y)),
          {'new': x and {'owner': x.get('owner'), 'target': x.get('target'), '찾기 수': x and {k: v['n'] for k, v in (x.get('ls') or {}).items()},
                         '검색 수': x and {k: v['n'] for k, v in (x.get('sr') or {}).items()}, '끊기 전/뒤': [x.get('refs0'), (x.get('after') or {}).get('refs')]},
           '바탕과 같음': (same_json(x, y) if (x and y) else None),
           '다른 칸': (sorted(k for k in set(x) | set(y) if not same_json(x.get(k), y.get(k))) if (x and y) else None)})


def main():
    os.makedirs(TMPD, exist_ok=True)
    sn = app_src(NEW)
    sb = None if NOBASE else app_src(BASE)
    data, miss = data_files()
    print('INFO | 새 판 md5(LF) %s · %s B · 바탕 %s md5(LF) %s · %s B · 데이터 studyplandata %s %s' % (
        md5lf(sn), len(sn.encode('utf-8')), BASE, sb and md5lf(sb), sb and len(sb.encode('utf-8')), DREV,
        '없음(%s)' % miss if miss else ' · '.join('%s %d B' % (os.path.basename(f), len(data[f])) for f in DFILES)), flush=True)
    if miss:
        print('데이터 없음 — studyplandata %s 의 %s 를 못 읽음(SPD_ROOT=%s · git fetch 뒤 다시)' % (DREV, miss, SPD), flush=True)
        return 3
    if sb is None and not NOBASE:
        print('INFO | 바탕 %s 를 못 읽음 — 헛잣대 없이 돎' % BASE, flush=True)
    R = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for tag, src in (('NEW', sn), ('BASE', sb)):
            if src is None:
                continue
            R[tag] = {}
            if want('C'):
                R[tag]['C'] = run_c(br, tag, src, data)
            if any(want(k) for k in ('B2', 'B3', 'B4', 'B5')):
                R[tag]['B'] = run_b(br, tag, src, data)
        br.close()
    n, b = R.get('NEW', {}), R.get('BASE')
    if want('C'):
        judge_c(n.get('C', {}), b and b.get('C'))
    judge_b(sn, sb, n.get('B', {}), b and b.get('B'))
    base_msgs = {m for k, v in ERRS.items() if k.startswith('BASE') for m in v}
    for k, v in ERRS.items():
        if k.startswith('NEW'):
            own = [m for m in v if m not in base_msgs]
            T('CE', '%s 페이지 오류 0(pageerror · window error · unhandledrejection · 바탕에도 나는 것 %d)' % (k, len(v) - len(own)), not own, own[:5])
        else:
            N('CE', '%s 페이지 오류' % k, v[:5])
    sh = (n.get('C') or {}).get('shots') or {}
    sh.update({'BASE ' + k: v for k, v in ((b or {}).get('C') or {}).get('shots', {}).items()})
    if sh:
        N('CS', '그림(눈으로 볼 것)', sh)
    n_pass = sum(1 for r in RES if r[2] is True)
    n_fail = sum(1 for r in RES if r[2] is False)
    y_bad = [y for y in YARD if y[3] is not None and y[2] != y[3]]
    y_nd = [y for y in YARD if y[3] is None]
    lines = ['', '=' * 100, '_harness_ox_home_tidy — PASS %d · FAIL %d · %d초' % (n_pass, n_fail, round(time.time() - T0)),
             '헛잣대(바탕 %s · 같은 차례 · 무변 칸만 PASS 여야): %d 칸 중 어긋난 칸 %d · 못 가르는 칸 %d(적기만)' % (BASE, len(YARD), len(y_bad), len(y_nd))]
    lines += ['  어긋남 — %s · %s · 바탕 %s(%s 여야)' % (g, nm, 'PASS' if ok else 'FAIL', 'PASS' if wp else 'FAIL') for g, nm, ok, wp in y_bad]
    lines += ['  못 가름 — %s · %s · 바탕 %s · %s' % (g, nm, 'PASS' if ok else 'FAIL', NONDISC.get(nm.split(' ', 1)[1] if ' ' in nm else nm, '')) for g, nm, ok, wp in y_nd]
    lines += ['단계별 초: ' + ' · '.join('%s %d' % s for s in STEP)]
    lines += ['FAIL: %s · %s' % (r[0], r[1]) for r in RES if r[2] is False]
    print('\n'.join(lines), flush=True)
    os.makedirs(os.path.dirname(OUTF), exist_ok=True)
    with open(OUTF, 'w', encoding='utf-8') as f:
        for gg, nm, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ('INFO' if ok is None else ('PASS' if ok else 'FAIL'), gg, nm, _s(d)))
        f.write('\n'.join(lines) + '\n')
    print('결과 파일: %s · 그림: %s' % (OUTF, SHOTS), flush=True)
    return 0 if not n_fail and not y_bad else 1


if __name__ == '__main__':
    sys.exit(main())
