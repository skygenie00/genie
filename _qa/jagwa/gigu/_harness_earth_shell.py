# -*- coding: utf-8 -*-
"""자과앱 지학 껍데기(add1+add2+add3) — 헤드리스 검산
(2026-09-20 · gigu/_task_jagwa_earth_listpop.md §I)

  C  §A 코드 표시 G02-39-02 · 검색 두 꼴
  M  §B 회차별 │ 단원별
  S  §B 히트맵 차례·빈 칸
  I  §C 「그림」 칩 삭제
  K  §D 머리 「📖 교재」 → 떠 있는 창 · ⤢ 왕복
  V  §E 문항 = 떠 있는 창 (필기 좌표 ±1/1000 · 뒤 목록이 산다)
  P  §F 「교재 자리 목록」 창 (네 꼴 · 쪽 고정 · 오리기 · CROPFOR)
  H  폰(390px iframe) — ≤480px 은 늘 꽉 참
  B  생물 무변 — DOM 글자 대조(HEAD 사본과)
  Y  물리 무변 — DOM 글자 대조(HEAD 사본과)
  0  헛잣대 — HEAD 에서 C·M·V·P 가 FAIL 해야 한다
  Z  원본 대조(파이썬)
  X  교재 창(_task_jagwa_earth_bookwin §L · 2026-09-24) — A 목록 창 쪽 줄 · B 만진 창 맨 앞 · C ◀ 쪽 ▶ ↩ · D 이 쪽의 문항
     · E 📍 찍기 · F 정리 창 글씨 · G 이미 찍은 자리 · H 손바닥 · I 확대 · J 미리보기 고치기
     · X-0 바탕 판(24f1a373)에서 새 항목이 FAIL(헛잣대) · X-11 생물·물리 DOM 글자 = 바탕 판(W 는 이미 쓴 글자라 X)
     python _harness_earth_shell.py x      ← X 만
  XB 생물 교재 창(_task_jagwa_earth_bookwin_add1 §관문 · 2026-09-25) — A 📖 p11 「11쪽」 = 교재만 · B·D 창 쌓임 · 이 쪽의 문항 연도 내림
     · C 쪽 칸 · ◀ ▶ 조각 경계(1.1→1.2.pdf) · ↩ · E 「대기」 📍 찍기 → ✓ · F 정리 창 .mut 10px · H 손바닥 · I 확대 · J 미리보기 고치기
     · XB-0 바탕 판(bookwin 인도판 f07e9d08 · 생물은 ISEA=false 라 새 기능 없음)에서 새 항목이 FAIL(헛잣대)
     · X-11 은 물리만(생물은 add1 로 뜻한 차이 — XB 가 잰다)
     python _harness_earth_shell.py xb     ← XB 만

⚠ 픽셀 IDENTICAL 게이트는 쓰지 않는다(CLAUDE.md 「자과앱에는 픽셀 게이트를 걸지 않는다」).
   가림·쌓임은 elementsFromPoint · 그려졌는가는 DOM 개수·getBoundingClientRect 로 잰다.
   §I-7 의 「네 꼴 캡처」도 픽셀이 아니라 **DOM 캡처(.html)** 다 — 사람이 열어 보는 것이고 게이트가 아니다.

    PYTHONIOENCODING=utf-8 python _harness_earth_shell.py
    PYTHONIOENCODING=utf-8 python _harness_earth_shell.py earth
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기 헬퍼(_task_qa_slim2 A-1-2 · 옛 남 하네스 import 를 갈음)
import hashlib
import http.server
import io
import json
import os
import re
import shutil
import socketserver
import subprocess
import sys
import threading
import time
import urllib.parse

GENIE = _roots.genie()
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(GENIE, 'jagwa', 'index.html')
BASE_MD5 = '129eedb17753b611667c2bcc6e42f3ed'   # 고침 전 md5(LF)
BASE = os.path.join(HERE, '_base_bp.html')   # 공개 저장소에 두지 않는다(D11)


def _ensure_base():
    """사본이 없으면 git 에서 꾺낸다 — 큰 파일을 드라이브마다 끌고 다니지 않게."""
    import subprocess
    if os.path.exists(BASE):
        b = open(BASE, 'rb').read()
        if hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest() == BASE_MD5:
            return BASE
    alt = SRC + '.before_listpop'
    if os.path.exists(alt):
        b = open(alt, 'rb').read()
        if hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest() == BASE_MD5:
            return alt
    # 고침 전 판이 HEAD 가 아닐 수 있다 — 그 판을 만든 커밋도 같이 본다(add5 때 겪음)
    for rev in ('HEAD', 'ab49775', 'HEAD~1', 'HEAD~2', 'HEAD~3'):
        try:
            b = subprocess.run(['git', '-C', GENIE, 'show', rev + ':jagwa/index.html'],
                               capture_output=True).stdout
        except Exception:
            continue
        if b and hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest() == BASE_MD5:
            open(BASE, 'wb').write(b.replace(b'\n', b'\r\n') if b'\r\n' not in b else b)
            print('[base] git %s 에서 꺼냈다' % rev)
            return BASE
    raise SystemExit('NG  고침 전 사본(md5 %s)을 못 찾았다' % BASE_MD5)


if QC.GATE:   # regress — 본판(129eedb) 사본 찾기(없으면 git show) 0 · 그 사본은 바탕 묶음(earthbase · biobase · physbase) · static_checks 본판 셈에만 쓴다(gate)
    BASE = _ensure_base()
SPDROOT = _roots.spd()
OUT = os.path.join(os.environ.get('TEMP', '.'), 'hlistpop')
os.makedirs(OUT, exist_ok=True)
CAP = os.environ.get('LISTPOP_CAP') or os.path.join(HERE, '_cap_bp')
os.makedirs(CAP, exist_ok=True)
CHROME = JG.CHROME   # JG 로 옮김(_task_qa_slim2 A-1-2) — 남은 제 코드가 이 이름을 부른다 · 같은 객체(두 벌 아님)
HEAD = JG.HEAD   # JG 로 옮김(_task_qa_slim2 A-1-2) — 남은 제 코드가 이 이름을 부른다 · 같은 객체(두 벌 아님)
STUB = JG.STUB_ES   # JG 로 옮김(_task_qa_slim2 A-1-2) — 남은 제 코드가 이 이름을 부른다 · 같은 객체(두 벌 아님)
TAIL = JG.TAIL   # JG 로 옮김(_task_qa_slim2 A-1-2) — 남은 제 코드가 이 이름을 부른다 · 같은 객체(두 벌 아님)

# ══════════════════════════════════════════════════════════════════════════
BODY_EARTH = r"""
   /* ───── 밑준비 ───── */
   await (async()=>{for(let __i=0;__i<300&&(typeof db==='undefined'||!db);__i++)await new Promise(r=>setTimeout(r,100));return loadEarthData()})()/* ★ 2026-10-08 (_task_jagwa_phys_win 회귀) db 가 설 때까지 — 고정 대기 경합(짐 크면 「db 없음」) · 판정 무변 */;
   await until(()=>DATA.length===704,30000);
   ['jagwa.earth.order','jagwa.earth.coll','jagwa.earth.hmfold','jagwa.view.win',
    'jagwa.win.view','jagwa.win.book','jagwa.win.bplist','jagwa.win.mc','jagwa.win.jn']
     .forEach(k=>{try{localStorage.removeItem(k)}catch(e){}});
   _coll=null;
   FL.past='y';FL.q='';FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';
   GG={};GGREF={};PICK={};
   /* 사용자 기기와 같은 상태로 — 기록.json 의 손값(unit·bpg·mcard·crop)을 싣는다 */
   {const rec0=JSON.parse(await (await __nativeFetch('/data/earth/%EA%B8%B0%EB%A1%9D.json')).text());
    UN=rec0.data.unit||{};BPG=rec0.data.bpg||{};MC=rec0.data.mcard||{};CROP=rec0.data.crop||{};
    await put('kv','unit',UN);await put('kv','bpg',BPG);await put('kv','mcard',MC);await put('kv','crop',CROP);
    if(typeof jgMigrate==='function')await jgMigrate('boot');   /* ★ jagwa_uid(9/29) — 실기기는 이 손값이 부팅 전부터 kv 에 있어 부팅 때 옮겨진다 · 하네스는 부팅 뒤에 넣으니 같은 옮김을 한 번(바탕 앱엔 없음) */
    refreshUnits();}
   draw(); await wait(300);
   N('밑준비',{subj:SUBJ_ID,ISEA:ISEA,DATA:DATA.length,기출:DATA.filter(r=>!isC(r)).length});

   /* ══════════ 1. §A 껍데기 ══════════ */
   await grp('A', async()=>{
     const esh=document.getElementById('esh');
     T('A-0 지학 껍데기가 섰다',!!esh);
     T('A-0 옛 머리·개수 줄은 안 보인다',
       getComputedStyle($('#lib>.top')).display==='none'&&getComputedStyle($('#lib>.count')).display==='none',
       [getComputedStyle($('#lib>.top')).display,getComputedStyle($('#lib>.count')).display]);
     ['#specHd','#fBig','#fEtc'].forEach(q=>
       T('A-1 '+q+' 안 보임',$(q)&&$(q).offsetParent===null,$(q)?getComputedStyle($(q)).display:'(없음)'));
     T('A-1 범례 줄(.legend) 안 보임',$('.legend')&&$('.legend').offsetParent===null);
     T('A-1 긴 검색칸이 아니다(#q 가 껍데기 안 · 폭 224px)',
       !!$('#esh #q')&&Math.abs($('#q').getBoundingClientRect().width-224)<2,
       $('#q')?$('#q').getBoundingClientRect().width:null);
     /* 머리줄 자식 차례 */
     const head=esh.querySelector('.ehead');
     const seq=[...head.children].map(el=>el.id||el.tagName.toLowerCase()).filter(x=>x!=='span'||true);
     /* ★ add9 §A-1 — 「목차」 단추(#btnTree)는 걷었다(왼쪽 상주 서랍이 그 구실) */
     T('A-2 머리줄 차례 = 제목 → 수 → (빈칸) → 과목탭 → 교재 → 설정 → D-날 → 동기화',
       seq.join(',')==='h1,eCnts,span,subjTabs,btnBook,btnSet,examChip,recChip',seq);
     T('A-2 제목 18px 800',getComputedStyle(head.querySelector('h1')).fontSize==='18px'
       &&getComputedStyle(head.querySelector('h1')).fontWeight==='800',
       [getComputedStyle(head.querySelector('h1')).fontSize,getComputedStyle(head.querySelector('h1')).fontWeight]);
     T('A-2 「기출 319 · 확인 385」',txt(document.getElementById('eCnts'))==='기출 319 · 확인 385',txt(document.getElementById('eCnts')));
     /* 약점 줄 단추 높이가 서로 ±1px */
     const hs=[...esh.querySelectorAll('.ebar button')].filter(b=>b.offsetParent!==null)
       .map(b=>Math.round(b.getBoundingClientRect().height));
     T('A-3 약점 줄 단추 높이가 서로 ±1px',hs.length>2&&(Math.max.apply(null,hs)-Math.min.apply(null,hs))<=1,hs);
     T('A-3 #cnt = 「319문제」(모드 글자 0)',txt($('#cnt'))==='319문제',txt($('#cnt')));
     T('A-3 「⚡ 빠른 실행」 글자가 없다',txt(esh).indexOf('빠른 실행')<0);
     T('A-4 필터 고르개에 여덟 갈래',
       [...esh.querySelectorAll('#rvF option')].map(o=>o.value).join(',')===',new,X,Q,again,P,bang,gg',
       [...esh.querySelectorAll('#rvF option')].map(o=>o.value));
     T('A-4 「메모 있음」이 아니라 「근거 있음」이다',txt(esh.querySelector('#rvF')).indexOf('메모 있음')<0
       &&txt(esh.querySelector('#rvF')).indexOf('근거 있음')>=0);
     T('A-5 회차 select 를 안 그린다(#fEtc 가 숨고 FL.round 는 빈 값)',FL.round==='');
     await cap('A1_껍데기',document.getElementById('esh').outerHTML);
   });

   /* ══════════ 2. §A 히트맵 ══════════ */
   await grp('H', async()=>{
     const cells=()=>$$$('#spec i');
     T('H-1 칸 319 · 빈 칸(gap) 0',cells().length===319&&$$$('#spec i.gap').length===0,
       [cells().length,$$$('#spec i.gap').length]);
     const r0=cells()[0].getBoundingClientRect();
     T('H-1 칸 8×8',Math.abs(r0.width-8)<0.6&&Math.abs(r0.height-8)<0.6,[r0.width,r0.height]);
     /* 이웃 칸 간격 10px = 8 + 2 */
     const a=cells()[0].getBoundingClientRect(), b=cells()[1].getBoundingClientRect();
     T('H-1 이웃 칸 간격 10px',Math.abs((b.left-a.left)-10)<0.6,b.left-a.left);
     T('H-1 칸 차례 = 목록 .num 차례',
       JSON.stringify(cells().map(i=>i.title.split(' ')[0]))===JSON.stringify(nums()));
     /* 장 칩 */
     const chs=[...document.querySelectorAll('#eChs [data-big]')];
     T('H-2 장 칩 = 전체 + 다섯',chs.length===6,chs.map(x=>txt(x)));
     const air=chs.find(x=>txt(x).indexOf('대기·해양')===0);
     T('H-2 「대기·해양 77」 칩이 있다',!!air&&txt(air)==='대기·해양 77',air?txt(air):null);
     air.click(); await wait(300);
     T('H-2 ★장 칩이 히트맵과 목록을 같이 좁힌다 — 칸 77 · 목록 77',
       $$$('#spec i').length===77&&nums().length===77,[$$$('#spec i').length,nums().length]);
     T('H-2 장 칩은 하나만 켜진다',FL.bigs.length===1,FL.bigs);
     document.querySelector('#eChs [data-big=""]').click(); await wait(300);
     T('H-2 「전체」로 돌아온다',nums().length===319&&FL.bigs.length===0);
     /* 폭이 바뀌면 한 줄 개수만 바뀐다 */
     const lib=$('#lib');const w0=$('#spec').getBoundingClientRect().width;
     const colsAt=()=>{const t=cells()[0].getBoundingClientRect().top;
       return cells().filter(c=>Math.abs(c.getBoundingClientRect().top-t)<1).length};
     const c900=colsAt();
     lib.style.maxWidth='600px'; await wait(250);
     const c600=colsAt(), rr=cells()[0].getBoundingClientRect();
     T('H-3 ★폭을 줄여도 칸 크기는 그대로 · 한 줄 개수만 줄어든다',
       Math.abs(rr.width-8)<0.6&&c600<c900,[c900,c600,rr.width]);
     lib.style.maxWidth=''; await wait(250);
     /* 접기 */
     document.getElementById('hmTg').click(); await wait(200);
     T('H-4 접으면 히트맵이 숨고 글자가 「펴기 ▼」',$('#spec').offsetParent===null
       &&txt(document.getElementById('hmTg'))==='펴기 ▼',txt(document.getElementById('hmTg')));
     T('H-4 기기 값에 적힌다',localStorage.getItem('jagwa.earth.hmfold')==='1');
     document.getElementById('hmTg').click(); await wait(200);
     T('H-4 다시 펴진다',$('#spec').offsetParent!==null);
   });

   /* ══════════ 3. §B 목차 세 층 · 접기 ══════════ */
   await grp('B', async()=>{
     const nCh=()=>$$$('#list .grouphd.ch').length, nSec=()=>$$$('#list .grouphd.sec').length,
           nU=()=>$$$('#list .grouphd.u').length, nIt=()=>$$$('#list .item').length;
     T('B-1 편 5 · 절 16 · 소단원 115',nCh()===5&&nSec()===16&&nU()===115,[nCh(),nSec(),nU()]);
     const fs=q=>getComputedStyle($(q)).fontSize;
     T('B-1 글자 크기 14 > 12.5 > 11.5',
       fs('#list .grouphd.ch')==='14px'&&fs('#list .grouphd.sec')==='12.5px'&&fs('#list .grouphd.u')==='11.5px',
       [fs('#list .grouphd.ch'),fs('#list .grouphd.sec'),fs('#list .grouphd.u')]);
     T('B-1 머리마다 ▾ 가 있다',$$$('#list .grouphd .ar').length===nCh()+nSec()+nU());
     /* 층마다 접고 편다 */
     const ch1=$('#list .grouphd.ch'); ch1.click(); await wait(250);
     T('B-2 편을 누르면 그 밑이 접힌다',nSec()<16&&$('#list .grouphd.ch').classList.contains('off'));
     ch1_again:{const c=$('#list .grouphd.ch');c.click()} await wait(250);
     T('B-2 다시 누르면 펴진다',nSec()===16);
     const s1=$('#list .grouphd.sec'); s1.click(); await wait(250);
     T('B-2 절을 누르면 그 밑 소단원이 접힌다',nU()<115);
     $('#list .grouphd.sec').click(); await wait(250);
     const u1=[...document.querySelectorAll('#list .grouphd.u')]
       .find(h=>h.nextElementSibling&&h.nextElementSibling.classList.contains('item'));
     const n0=nIt(); u1.click(); await wait(250);
     T('B-2 소단원을 누르면 카드만 접힌다',nU()===115&&nIt()<n0,[nU(),nIt(),n0]);
     $('#list .grouphd.u').click(); await wait(250);
     T('B-2 기기 값에 적힌다',Array.isArray(JSON.parse(localStorage.getItem('jagwa.earth.coll')||'[]')));
     /* 접기 단추 한 바퀴 */
     const lv=document.getElementById('lvBtn');
     const shot=()=>[nCh(),nSec(),nU(),nIt()];
     lv.click(); await wait(300); const s_ch=shot(), l_ch=txt(lv);
     lv.click(); await wait(300); const s_sec=shot(), l_sec=txt(lv);
     lv.click(); await wait(300); const s_u=shot(), l_u=txt(lv);
     lv.click(); await wait(300); const s_all=shot(), l_all=txt(lv);
     N('B-3 단계별 (편,절,소단원,카드)',{편:s_ch,절:s_sec,소단원:s_u,문제:s_all,글자:[l_ch,l_sec,l_u,l_all]});
     T('B-3 ★편 = 5/0/0/0',JSON.stringify(s_ch)===JSON.stringify([5,0,0,0]),s_ch);
     T('B-3 ★절 = 5/16/0/0',JSON.stringify(s_sec)===JSON.stringify([5,16,0,0]),s_sec);
     T('B-3 ★소단원 = 5/16/115/0',JSON.stringify(s_u)===JSON.stringify([5,16,115,0]),s_u);
     T('B-3 ★문제 = 5/16/115/319',JSON.stringify(s_all)===JSON.stringify([5,16,115,319]),s_all);
     T('B-3 단추 글자 = 지금 보이는 층',l_ch==='편'&&l_sec==='절'&&l_u==='소단원'&&l_all==='문제',
       [l_ch,l_sec,l_u,l_all]);
     lv.click(); await wait(300);
     T('B-3 한 바퀴 뒤 다시 편',JSON.stringify(shot())===JSON.stringify([5,0,0,0]),shot());
     lv.click();lv.click();lv.click(); await wait(400);
     /* 회차별 = 회차 ↔ 문제 */
     ordSet('round');draw();await wait(300);
     T('B-4 회차별 머리 = 편 꼴 한 층 32개',$$$('#list .grouphd.ch').length===32
       &&$$$('#list .grouphd.sec').length===0&&$$$('#list .grouphd.u').length===0,
       [$$$('#list .grouphd.ch').length,$$$('#list .grouphd.sec').length]);
     lv.click(); await wait(300);
     T('B-4 회차별 접기 = 회차만',txt(lv)==='회차'&&$$$('#list .item').length===0,[txt(lv),$$$('#list .item').length]);
     lv.click(); await wait(300);
     T('B-4 다시 누르면 문제까지',txt(lv)==='문제'&&$$$('#list .item').length===319);
     ordSet('unit');draw();await wait(300);
     /* treeGo — 접힌 편 밑으로 가면 펴진다 */
     lv.click(); await wait(300);                      /* 편만 */
     treeGo('2.1.3'); await wait(400);
     T('B-5 ★접힌 편 밑 단원으로 가면 펴지고 도착한다',
       !!$('#list [data-uhd="2.1.3"]')&&!collHas('c2')&&!collHas('s2.1')&&!collHas('u2.1.3'),
       [!!$('#list [data-uhd="2.1.3"]'),collHas('c2'),collHas('s2.1'),collHas('u2.1.3')]);
     lvApply('all',false);draw();await wait(300);
   });

   /* ══════════ 4. §C 🃏 · 📋 ══════════ */
   await grp('C', async()=>{
     T('C-0 절 머리 「암기카드」 글자 0',txt($('#list')).indexOf('암기카드')<0);
     T('C-0 #btnMC 를 안 그린다',!document.getElementById('btnMC'));
     /* 실데이터 카드 = 손필기 3장(no 50·71·308) */
     T('C-1 🃏 전체 = 3',txt(document.getElementById('mcAll'))==='🃏 전체 3',txt(document.getElementById('mcAll')));
     T('C-1 crop 45건은 수에 안 들어간다',Object.keys(CROP).length>0&&mcCountIn(DATA.filter(r=>!isC(r)).map(r=>r[F.NO]))===3,
       [Object.keys(CROP).length,mcCountIn(DATA.filter(r=>!isC(r)).map(r=>r[F.NO]))]);
     const u112=document.querySelector('#list [data-uhd="1.1.2"] [data-mc]');
     T('C-1 1.1.2 소단원 🃏 = 2',!!u112&&txt(u112)==='🃏 2',u112?txt(u112):null);
     /* 🃏 창 */
     u112.click(); await wait(600);
     const w=document.getElementById('mcw');
     T('C-2 🃏 창이 뜬다',!!w&&!!w.querySelector('.panel'));
     T('C-2 카드가 있는 문항만',$$$('#mcwBody .mcwq').length===2,$$$('#mcwBody .mcwq').length);
     T('C-2 「보기」 단추가 있다',$$$('#mcwBody .jgo').length===2);
     T('C-2 손필기 칸을 그린다',$$$('#mcwBody canvas[data-ink]').length===2);
     T('C-2 「＋ 카드 넣기」 단추 셋',!!document.getElementById('mcwInk')&&!!document.getElementById('mcwBk')&&!!document.getElementById('mcwOmr'));
     /* 끌기·크기 */
     const p=w.querySelector('.panel'), q0=p.getBoundingClientRect();
     await drag(w.querySelector('.bplh'),q0.left+120,q0.top+8,q0.left+70,q0.top+58,'mouse'); await wait(220);
     const q1=p.getBoundingClientRect();
     T('C-2 머리줄을 끌면 움직인다',Math.abs(q1.left-(q0.left-50))<3&&Math.abs(q1.top-(q0.top+50))<3,[q0.left,q1.left]);
     const g=w.querySelector('.twgrip'), gr=g.getBoundingClientRect();
     await drag(g,gr.left+4,gr.top+4,gr.left+84,gr.top+54,'mouse'); await wait(240);
     T('C-2 모서리를 끌면 커진다',Math.abs(p.getBoundingClientRect().width-(q1.width+80))<3,
       [q1.width,p.getBoundingClientRect().width]);
     T('C-2 크기를 기기 값에 적는다',!!JSON.parse(localStorage.getItem('jagwa.win.mc')||'null'));
     /* 「보기」 → 문항 창 */
     $('#mcwBody .jgo').click(); await until(()=>VNO!==null,6000); await wait(400);
     T('C-2 「보기」를 누르면 문항 창이 뜬다',VNO!==null&&!$('#view').classList.contains('hide'));
     closeView(); await wait(250);
     await cap('C1_암기카드창',document.getElementById('mcw').querySelector('.panel').outerHTML);
     document.getElementById('mcwX').click(); await wait(150);
     /* 📋 */
     const jb=document.querySelector('#list .grouphd.sec [data-jn]');
     T('C-3 📋 는 절 머리에만 있다',$$$('#list .grouphd.sec [data-jn]').length===16
       &&$$$('#list .grouphd.u [data-jn]').length===0,
       [$$$('#list .grouphd.sec [data-jn]').length,$$$('#list .grouphd.u [data-jn]').length]);
     const j11=document.querySelector('#list [data-coll="s1.1"] [data-jn]');
     j11.click(); await wait(600);
     const jw=document.getElementById('jnw');
     T('C-3 정리 창이 뜬다',!!jw);
     T('C-3 1.1 = 42문항',txt(jw.querySelector('.bplh')).indexOf('42문항')>=0,txt(jw.querySelector('.bplh')));
     T('C-3 소제목 수 = 기출 있는 소단원 수',
       $$$('#jnwBody .jnh').length===((TOC.sec['1.1']||{}).units||[]).filter(u=>u!=='1.1'&&DATA.some(r=>!isC(r)&&unitOf(r[F.NO])===u)).length,
       $$$('#jnwBody .jnh').length);
     T('C-3 행마다 지문 전문·기록 칸',$$$('#jnwBody .jnrow .q').length===42&&$$$('#jnwBody .jnrow .mk').length===42);
     /* 정답·해설은 행마다 따로 접힌다 */
     const b0=$$$('#jnwBody .jnans')[0], b1=$$$('#jnwBody .jnans')[1];
     b0.click(); await wait(200);
     T('C-3 ★정답·해설이 그 행만 펴진다',
       !b0.nextElementSibling.classList.contains('hide')&&b1.nextElementSibling.classList.contains('hide'));
     T('C-3 「✏️ 표시」는 안 옮겼다',txt(jw).indexOf('✏️ 표시')<0);
     await cap('C2_정리창',jw.querySelector('.panel').outerHTML);
     document.getElementById('jnwX').click(); await wait(150);
     /* 머리 단추 누름이 접힘을 안 바꾼다 */
     const before=JSON.stringify([...collSet()].sort());
     document.querySelector('#list .grouphd.sec [data-jn]').click(); await wait(400);
     document.getElementById('jnwX').click(); await wait(150);
     T('C-4 ★머리 안 단추를 눌러도 접힘이 안 바뀐다',JSON.stringify([...collSet()].sort())===before);
   });

   /* ══════════ 5. §D 근거 ══════════ */
   await grp('G', async()=>{
     const A='G25-62-09', B='G02-39-02';
     const noA=rowByUid(A)[F.NO], noB=rowByUid(B)[F.NO];
     GG={};GGREF={};await saveGG();await saveGGREF();
     await openView(noA); await wait(600);
     const line=()=>$('#card [data-ggbox]');
     T('G-0 문항 창 카드에 근거 줄이 있다',!!line());
     T('G-0 근거 줄은 선택지 아래 · #cDet 위다',
       !!$('#card .ggwrap')&&$('#card .ggwrap').nextElementSibling&&$('#card .ggwrap').nextElementSibling.classList.contains('vrow'));
     T('G-0 목록 카드에는 적는 칸이 없다',$$$('#list .item .ggrow').length===0);
     T('G-0 「＋한줄」이 없다',txt($('#list')).indexOf('＋한줄')<0);
     /* 한 줄 저장 — Enter */
     const put1=async(t)=>{const ta=$('#card .ggrow .txt');ta.value=t;ta.focus();
       ta.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true,cancelable:true}));
       await wait(400)};
     T('G-1 적기 전에는 근거 0',ggOf(A).length===0,[ggOf(A).length,$$$('#card .ggrow').length]);
     await put1('첫 근거');
     N('G-1 첫 저장 뒤',{n:ggOf(A).length,t:ggOf(A).map(g=>g.t),rows:$$$('#card .ggrow').length,
                        boxes:$$$('[data-ggrows]').length});
     T('G-1 Enter 로 저장 — 칩 1개',ggOf(A).length===1&&$$$('#card .ggnum').length===1,
       [ggOf(A).length,$$$('#card .ggnum').length]);
     T('G-1 저장 순간 마크가 ok 에 실린다',ggOf(A)[0].ok===(lastM(noA)||null),[ggOf(A)[0].ok,lastM(noA)]);
     T('G-1 parts 가 없다(줄 하나 · 라벨 없음)',!ggOf(A)[0].parts);
     /* 칸을 벗어나며 저장 */
     {const ta=$('#card .ggrow .txt');ta.value='둘째 근거';ta.focus();ta.blur();await wait(450)}
     T('G-1 칸을 벗어나면 저장(줄 하나일 때)',ggOf(A).length===2,ggOf(A).length);
     /* 병렬 — (1) → ＋ → (2) → ＋ → (3) */
     {const lab=$('#card .ggrow .lab');lab.value='(1)';
      $('#card .ggrow .txt').value='ㄱ 줄';
      $('#card [data-ggplus]').click();await wait(200)}
     const labs1=[...document.querySelectorAll('#card .ggrow .lab')].map(x=>x.value);
     T('G-2 ＋ 를 누르면 라벨이 (2) 로 미리 찬다',labs1.join(',')==='(1),(2)',labs1);
     {const ls=[...document.querySelectorAll('#card .ggrow')];
      ls[1].querySelector('.txt').value='ㄴ 줄';
      $('#card [data-ggplus]').click();await wait(200)}
     const labs2=[...document.querySelectorAll('#card .ggrow .lab')].map(x=>x.value);
     T('G-2 한 번 더 = (3)',labs2.join(',')==='(1),(2),(3)',labs2);
     T('G-2 줄이 둘 이상이면 「저장」 단추가 보인다',!$('#card [data-ggsave]').classList.contains('hide'));
     /* 줄 둘일 때 blur 로 저장되지 않는다 */
     {const ls=[...document.querySelectorAll('#card .ggrow')];ls[2].querySelector('.txt').value='ㄷ 줄';
      ls[2].querySelector('.txt').focus();ls[2].querySelector('.txt').blur();await wait(400)}
     T('G-2 ★줄이 둘 이상이면 칸을 벗어나도 저장 안 됨',ggOf(A).length===2,ggOf(A).length);
     $('#card [data-ggsave]').click(); await wait(450);
     const g3=ggOf(A)[2];
     T('G-2 ★「저장」으로 근거 하나 · parts 3',ggOf(A).length===3&&g3&&g3.parts&&g3.parts.length===3,
       [ggOf(A).length,g3&&g3.parts&&g3.parts.length]);
     T('G-2 t 는 세 줄이 붙은 글',g3&&g3.t==='(1) ㄱ 줄\n(2) ㄴ 줄\n(3) ㄷ 줄',g3&&g3.t);
     /* 라벨 다음 것 — ㄱ→ㄴ · ①→② · 가→나 */
     T('G-2 ㄱ→ㄴ · ①→② · 가→나 · a→b · 1.→2.',
       ggNextLabel('ㄱ')==='ㄴ'&&ggNextLabel('①')==='②'&&ggNextLabel('가')==='나'
       &&ggNextLabel('a')==='b'&&ggNextLabel('1.')==='2.',
       [ggNextLabel('ㄱ'),ggNextLabel('①'),ggNextLabel('가'),ggNextLabel('a'),ggNextLabel('1.')]);
     /* 칩 색 = 저장 순간 마크 */
     T('G-3 칩 색이 ok 를 따른다',$$$('#card .ggnum')[0].className.indexOf(ggOkCls(ggOf(A)[0].ok))>=0,
       $$$('#card .ggnum')[0].className);
     /* 「!」 */
     $$$('#card .ggnum')[0].click(); await wait(200);
     const pan=$('#card .ggpan:not(.hide)');
     T('G-3 칩을 누르면 판이 펴진다',!!pan);
     pan.querySelector('[data-ggbang]').click(); await wait(300);
     T('G-3 ★「!」 를 켜면 판·칩이 빨강',ggOf(A)[0].bang===true
       &&$$$('#card .ggnum')[0].classList.contains('bang')
       &&$('#card .ggpan').classList.contains('bang'),
       [ggOf(A)[0].bang,$$$('#card .ggnum')[0].className]);
     await cap('G1_근거줄',$('#card .ggwrap').outerHTML+$('#card .vrow').outerHTML);
     /* 댓글 */
     {const ci=$('#card [data-ggcin]');ci.value='댓글 하나';
      $('#card [data-ggreply]').click();await wait(400)}
     T('G-4 댓글이 달린다',(ggOf(A)[0].cs||[]).length===1,(ggOf(A)[0].cs||[]).length);
     {const b=$('#card [data-ggce]');b.click();await wait(250);
      const ta=$('#card .ggcs textarea');ta.value='댓글 고침';
      $('#card .ggcs .cedit button').click();await wait(400)}
     T('G-4 댓글을 고친다',(ggOf(A)[0].cs||[])[0].t==='댓글 고침',(ggOf(A)[0].cs||[])[0].t);
     $('#card [data-ggcd]').click(); await wait(400);
     T('G-4 댓글을 지운다',(ggOf(A)[0].cs||[]).length===0);
     /* 한도 */
     {const ta=$('#card .ggrow .txt');ta.value='x'.repeat(GG_TMAX+5);ta.focus();
      ta.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true,cancelable:true}));await wait(400)}
     T('G-5 한도를 넘기면 저장 안 되고 안내가 뜬다',ggOf(A).length===3&&!!$('#card .ggover'),
       [ggOf(A).length,$('#card .ggover')?txt($('#card .ggover')):null]);
     {const ta=$('#card .ggrow .txt');ta.value='';ta.dispatchEvent(new Event('input',{bubbles:true}));await wait(200)}
     /* 🔍 — 남의 근거 찾아 연결 */
     GG[B]=[{k:'gb1',i:1,t:'에라토스테네스 반지름',ok:'O',ts:Date.now(),cs:[{k:'cb1',t:'댓글에만 있는 낱말 코시',ts:Date.now()}]}];
     await saveGG(); await openView(noA); await wait(600);
     $('#card [data-ggfind]').click(); await wait(300);
     {const i=$('#card .ggfind input');i.value='반지름';i.dispatchEvent(new Event('input',{bubbles:true}));await wait(350)}
     T('G-6 🔍 가 남의 근거를 찾는다',$$$('#card .ggfind .ggres').length>=1,$$$('#card .ggfind .ggres').length);
     {const i=$('#card .ggfind input');i.value='코시';i.dispatchEvent(new Event('input',{bubbles:true}));await wait(350)}
     T('G-6 ★댓글에서도 찾고 ↳ 로 보인다',
       $$$('#card .ggfind .ggres').some(x=>txt(x).indexOf('↳')>=0),
       $$$('#card .ggfind .ggres').map(x=>txt(x)).slice(0,2));
     $('#card .ggfind .ggres').click(); await wait(450);
     T('G-6 ★누르면 그 문항이 연결된다',ggRefOf(A).indexOf(B)>=0&&$$$('#card .ggref').length===1,
       [ggRefOf(A),$$$('#card .ggref').length]);
     $('#card .ggref').click(); await wait(300);
     T('G-6 칩을 누르면 연결 상자가 펴진다',!!$('#card .ggrefbox:not(.hide)'));
     T('G-6 상자에 그 문항 근거와 댓글이 보인다',
       txt($('#card .ggrefbox')).indexOf('반지름')>=0&&txt($('#card .ggrefbox')).indexOf('코시')>=0);
     /* ⚠ add1 지시서는 「안 옮긴다」였고 add2 §D 가 옮겼다 — 잣대를 뒤집었다(2026-09-20) */
     T('G-6 add2 §D 로 「✎ 여기서 고치기」가 생겼다',txt($('#card .ggrefbox')).indexOf('여기서 고치기')>=0,
       txt($('#card .ggrefbox')).slice(0,120));
     $('#card [data-ggrx]').click(); await wait(400);
     T('G-6 × 로 연결이 끊긴다',ggRefOf(A).length===0);
     /* 위 검색 줄 「🔗 근거」 모드 */
     closeView(); await wait(300);
     document.querySelector('#esh .seg2 [data-sm="g"]').click(); await wait(300);
     T('G-7 근거 모드로 바뀐다',GGMODE==='g'&&document.querySelector('#esh .seg2 [data-sm="g"]').classList.contains('on'));
     {const q=$('#q');q.value='반지름';q.dispatchEvent(new Event('input',{bubbles:true}));await wait(350)}
     T('G-7 결과 상자가 뜬다',!document.getElementById('esres').classList.contains('hide')
       &&$$$('#esres .ggres').length>=1,$$$('#esres .ggres').length);
     T('G-7 찾은 글자가 노랗게 보인다',$$$('#esres mark').length>=1);
     T('G-7 목록은 그대로 319',nums().length===319,nums().length);
     $$$('#esres .ggres')[0].click(); await until(()=>VNO!==null,5000); await wait(400);
     T('G-7 누르면 그 문항이 열린다',VNO!==null);
     closeView(); await wait(250);
     document.querySelector('#esh .seg2 [data-sm="q"]').click(); await wait(300);
     /* ★ jagwa_search(9/29) A-4-4 — 모드를 바꾸면 같은 칸 글을 그 모드 규칙으로 다시 찾는다(민법 setSearchMode 의 runSearch) · 옛 판 = 상자 닫힘 */
     T('G-7 「문제」로 돌아오면 같은 글(반지름)을 문제 규칙으로 다시 찾는다 — 문제 줄 · 근거 줄 0',GGMODE==='q'&&!document.getElementById('esres').classList.contains('hide')
       &&$$$('#esres [data-esq]').length>=1&&$$$('#esres [data-ggres]').length===0,[$$$('#esres [data-esq]').length,$$$('#esres [data-ggres]').length]);
     /* 필터 둘 */
     {const f=document.getElementById('rvF');f.value='gg';f.dispatchEvent(new Event('change',{bubbles:true}));await wait(350)}
     T('G-8 「근거 있음」 = 2건',nums().length===2,nums().length);
     {const f=document.getElementById('rvF');f.value='bang';f.dispatchEvent(new Event('change',{bubbles:true}));await wait(350)}
     T('G-8 「❗ 중요 근거」 = 1건',nums().length===1,nums().length);
     {const f=document.getElementById('rvF');f.value='';f.dispatchEvent(new Event('change',{bubbles:true}));await wait(350)}
     T('G-8 목록 카드에 읽기 전용 「근거 n」 칩',
       $$$('#list .item .tag.gg').filter(x=>x.offsetParent!==null).length===2,
       $$$('#list .item .tag.gg').filter(x=>x.offsetParent!==null).map(x=>txt(x)));
     /* 코멘트 흡수 — 흉내 3건 */
     GG={};await saveGG();
     /* 옛: CMT[rec(noA)[F.NO]]='옛 코멘트 1';CMT[rowByUid('G26-63-01')[F.NO]]='옛 코멘트 2';CMT[rowByUid('G25-62-02')[F.NO]]='옛 코멘트 3'; */
     /* ★ uid_unify A-1(10/4 · 근거 gigu/_task_jagwa_uid_unify.md §A-1 · 앱 ggEatNotes `rec(uidNo(열쇠))`) — 카드 층 코멘트 CMT 의 열쇠 = uid(qk). 번호 열쇠로 심으면 앱이 못 읽어 0건이 된다 · 옛 판(qk 없음)은 번호 그대로 */
     const uk9=n=>typeof qk==='function'?qk(n):n;
     CMT[uk9(rec(noA)[F.NO])]='옛 코멘트 1';CMT[uk9(rowByUid('G26-63-01')[F.NO])]='옛 코멘트 2';CMT[uk9(rowByUid('G25-62-02')[F.NO])]='옛 코멘트 3';
     await saveNote();
     const n1=await ggEatNotes(); await wait(300);
     T('G-9 ★옛 코멘트 3건이 근거로 옮겨진다',n1===3&&ggOf(A).length===1&&Object.keys(CMT).length===0,
       [n1,ggOf(A).length,Object.keys(CMT).length]);
     const n2=await ggEatNotes();
     T('G-9 ★다시 돌리면 0건(멱등)',n2===0,n2);
     /* 동기화 키 */
     T('G-10 SYNC_KEYS 에 gg·ggref·pick·link 가 들어갔다',
       ['gg','ggref','pick','link'].every(k=>SYNC_KEYS.indexOf(k)>=0)&&SYNC_KEYS.length===23,
       [SYNC_KEYS.length,SYNC_KEYS.slice(-4)]);
     T('G-10 SYNC_REF 에도 셋이 있다',!!SYNC_REF.gg&&!!SYNC_REF.ggref&&!!SYNC_REF.pick);
     GG={};GGREF={};await saveGG();await saveGGREF();draw();await wait(250);
   });

   /* ══════════ 6. §E 문항 창 아랫줄 ══════════ */
   await grp('V', async()=>{
     const no=rowByUid('G25-62-09')[F.NO];
     await openView(no); await wait(700);
     /* ⚠ add2 §C 가 P 를 넷째로 더했다 — 셋이던 잣대를 넷으로 고쳤다(2026-09-20) */
     T('V-1 아랫줄이 있다 — 정답·해설 ▸ · O △ X P · ✏️ 연결',
       !!$('#card .vrow')&&$$$('#card .vox').length===4&&!!$('#card #cDetBtn')&&!!$('#card #cLink'));
     T('V-1 <summary> 는 숨긴다',getComputedStyle($('#card #cDet>summary')).display==='none');
     const d=$('#cDet');
     T('V-1 처음엔 닫혀 있다',!d.open);
     $('#card #cDetBtn').click(); await wait(200);
     T('V-1 ▸ 를 누르면 열리고 글자가 ▾',d.open&&txt($('#card #cDetBtn'))==='정답·해설 ▾');
     $('#card #cDetBtn').click(); await wait(200);
     T('V-1 다시 누르면 닫힌다',!d.open);
     /* O △ X */
     const h0=hist(no).length;
     $('#card .vox.vO').click(); await wait(500);
     T('V-2 O 를 누르면 기록에 남는다',lastM(no)==='O'&&hist(no).length===h0+1,[lastM(no),hist(no).length]);
     T('V-2 켜진 단추에 on',$('#card .vox.vO').classList.contains('on'));
     $('#card .vox.vX').click(); await wait(500);
     T('V-2 X 로 바꾸면 그 단추가 켜진다',lastM(no)==='X'&&$('#card .vox.vX').classList.contains('on')
       &&!$('#card .vox.vO').classList.contains('on'));
     closeView(); await wait(400);
     {const idx=nums().indexOf(codeShow(rec(no)));const cell=$$$('#spec i')[idx];
      T('V-2 히트맵 칸이 따라간다',idx>=0&&!!cell&&/(^|\s)X(\s|$)/.test(cell.className),[idx,cell&&cell.className])}
     await openView(no); await wait(600);
     /* .vbot */
     T('V-3 .vbot 에서 #mO·#mQ·#mX·#tNote 가 안 보인다',
       ['#mO','#mQ','#mX','#tNote'].every(q=>$(q)&&$(q).offsetParent===null),
       ['#mO','#mQ','#mX','#tNote'].map(q=>$(q)?getComputedStyle($(q)).display:'(없음)'));
     /* ⚠ add2 §A·§B 가 필기 도구를 머리줄 알약으로 옮기고 #mP 를 근거 아랫줄로 옮겼다 */
     T('V-3 필기 도구는 머리줄 알약에 있고 그래도 보인다',
       !!$('#inkPill #tErase')&&$('#inkPill #tErase').offsetParent!==null,
       [!!$('#inkPill'),$('#tErase')?getComputedStyle($('#tErase')).display:'(없음)']);
     T('V-3 #mP 는 근거 아랫줄로 갔다 · #tHist 는 아랫줄에 남는다',
       !!$('#mP')&&$('#mP').offsetParent===null&&!!$('#card .vox.vP')
       &&!!$('#tHist')&&$('#tHist').offsetParent!==null,
       [$('#mP')?getComputedStyle($('#mP')).display:'(없음)',!!$('#card .vox.vP')]);
     T('V-4 「✏️ 연결」이 있고 linkSheet 를 그대로 쓴다',!!$('#card #cLink')&&typeof linkSheet==='function');
     /* ── 필기가 살아 있는가(§I-6) ──
        ⚠ 획 자리는 `underInk` 로 **빈 곳**을 골라야 한다 — 밑에 눌릴 것이 있으면 `inkPierce` 가
          capture 에서 막는다(앱이 일부러 그런 것 · 9/20 본판에서 배운 함정). */
     {const uidK=rec(no)[F.CODE];
      await del('ink','qink:'+uidK); await qLoad(uidK); await wait(200);
      setTool('pen'); qWire(); await wait(120);
      const sv=$('#card #qink'), r=sv.getBoundingClientRect();
      const freeAt=(u,v)=>{const x=r.left+u*r.width,y=r.top+v*r.width;
        if(x<4||y<4||x>document.documentElement.clientWidth-4||y>document.documentElement.clientHeight-4)return false;
        try{return !underInk(x,y,sv)}catch(e){return false}};
      let pu=0,pv=0,found=false;
      for(let v=0.03;v<=0.40&&!found;v+=0.03)for(let u=0.03;u<=0.50&&!found;u+=0.03)
        if(freeAt(u,v)&&freeAt(u+0.18,v+0.07)&&freeAt(u+0.36,v+0.14)){pu=u;pv=v;found=true}
      T('V-5 획을 그을 빈 자리를 찾았다',found,[pu,pv]);
      const n0=((QINK.s)||[]).length;
      const tr=await draw1(sv,[r.width*pu,r.width*pv,r.width*(pu+0.18),r.width*(pv+0.07),
                               r.width*(pu+0.36),r.width*(pv+0.14)]);
      T('V-5 ★펜으로 한 획을 그으면 QINK 가 는다(필기가 살아 있다)',((QINK.s)||[]).length===n0+1,[tr,((QINK.s)||[]).length]);
      T('V-5 ink 스토어 qink:<uid> 에 저장된다',!!(await get('ink','qink:'+uidK)));
      setTool('view'); qWire(); await wait(100);}
     /* 선택지가 눌린다(잉크 덮개 밑으로 — inkPierce) */
     {const b=$('#card .choices button');
      if(b){const was=lastPick(no);b.click();await wait(300);
        T('V-6 ★선택지가 그대로 눌린다(잉크 덮개 밑으로)',lastPick(no)!==''&&lastPick(no)!==was||!!b.classList.contains('pick'),
          [was,lastPick(no),b.className])}
      else T('V-6 선택지 단추가 있다',false)}
     /* 단축키 1~4 — ⚠ **add1 이전부터 죽어 있다.** 3317줄 가늠쇠 `document.querySelector('.sheet')` 가
        늘 숨어 있는 `#book`·`#bkq`(둘 다 class="sheet hide")에 걸려 늘 return 한다.
        지학·물리 둘 다 그렇다(본판에서 같은 값으로 실측 · _probe_tool.py).
        이 판은 **그 줄을 안 건드렸다** — 고치면 물리까지 바뀐다. 잣대는 「무변」으로 적는다. */
     {const h0=hist(no).length, m0=lastM(no);
      document.dispatchEvent(new KeyboardEvent('keydown',{key:'1',bubbles:true}));
      await wait(400);
      T('V-6 ★단축키 길이 본판과 같다(둘 다 안 먹는다 — 이 판이 깨뜨린 것이 아니다)',
        lastM(no)===m0&&hist(no).length===h0,[m0,lastM(no),h0,hist(no).length]);
      N('V-6 단축키가 죽은 까닭',{가늠쇠:'document.querySelector(".sheet")',
        걸리는것:[...document.querySelectorAll('.sheet')].map(x=>x.id+(x.classList.contains('hide')?'(hide)':''))});}
     closeView(); await wait(250);
   });

   /* ══════════ 7. §F 직접 찍기 ══════════ */
   await grp('P', async()=>{
     const A='G25-62-09', noA=rowByUid(A)[F.NO];
     PICK={};await savePICK();draw();await wait(250);
     /* 교재 탭 메뉴 */
     cropFor(noA);
     OMRTAB=false;
     cropOffer({p:5,r:[20,30,120,90]},()=>{},null); await wait(250);
     let m=document.getElementById('crmenu');
     T('P-1 교재 탭 메뉴 = 카드 + 문제 칸 + 해설 칸 + 글자 + 취소',
       !!m&&[...m.querySelectorAll('button')].map(b=>b.dataset.s).join(',')==='mc,q,s,fix,',
       m?[...m.querySelectorAll('button')].map(b=>txt(b)):null);
     m.querySelector('[data-s=""]').click(); await wait(200);
     /* OMR 탭 메뉴 */
     OMRTAB=true;
     cropOffer({p:1,r:[20,30,120,90]},()=>{},null); await wait(250);
     m=document.getElementById('crmenu');
     T('P-1 ★OMR 탭 메뉴 = 카드 + 취소뿐',
       !!m&&[...m.querySelectorAll('button')].map(b=>b.dataset.s).join(',')==='mc,',
       m?[...m.querySelectorAll('button')].map(b=>txt(b)):null);
     const n0=mcCountOf(noA);
     m.querySelector('[data-s="mc"]').click(); await wait(700);
     T('P-2 ★문항을 안 연 채 OMR 에서 찍으면 pick +1(doc omr)',
       pkOf(A).length===1&&pkOf(A)[0].doc==='omr'&&VNO===null,
       [pkOf(A).length,pkOf(A)[0]&&pkOf(A)[0].doc,VNO]);
     T('P-2 🃏 수가 +1',mcCountOf(noA)===n0+1,[n0,mcCountOf(noA)]);
     T('P-2 「문제 칸에 붙이기」는 🃏 수에 안 들어간다',
       (()=>{const c0=mcCountOf(noA);return c0===n0+1})());
     draw(); await wait(300);
     const el=$$$('#list .item').find(x=>txt(x.querySelector('.num'))===codeShow(rec(noA)));
     T('P-2 목록 카드 🃏 칩이 그 자리에서 바뀐다',!!el&&txt(el).indexOf('🃏 '+(n0+1))>=0,el?txt(el).slice(0,80):null);
     T('P-2 머리 🃏 전체도 +1',txt(document.getElementById('mcAll')).indexOf(String(mcCountIn(DATA.filter(r=>!isC(r)).map(r=>r[F.NO]))))>=0);
     /* 🃏 창에 그 자리 */
     OMRTAB=false;
     await mcwOpen('all'); await wait(1500);
     T('P-3 🃏 창에 찍은 자리 칸이 있다',$$$('#mcwBody canvas[data-pick]').length>=1,$$$('#mcwBody canvas[data-pick]').length);
     T('P-3 「정리OMR · 1쪽 찍은 자리」 글자',txt($('#mcwBody')).indexOf('정리OMR · 1쪽 찍은 자리')>=0,
       txt($('#mcwBody')).slice(0,120));
     $('#mcwBody [data-px]').click(); await wait(700);
     T('P-3 ✕ 로 빼면 −1',pkOf(A).length===0,pkOf(A).length);
     {const w=document.getElementById('mcw');if(w)w.remove()}
     /* 「문제 칸에 붙이기」는 카드가 아니다 */
     const c0=mcCountOf(noA), q0=((CROP[A]||{}).q||[]).length;
     cropFor(noA);
     cropOffer({p:5,r:[20,30,120,90]},()=>{},null); await wait(250);
     document.getElementById('crmenu').querySelector('[data-s="q"]').click(); await wait(800);
     T('P-4 ★「문제 칸에 붙이기」 = crop 만 늘고 🃏 수는 무변',
       ((CROP[A]||{}).q||[]).length===q0+1&&mcCountOf(noA)===c0,
       [((CROP[A]||{}).q||[]).length,q0,mcCountOf(noA),c0]);
     cropFor(null);
   });

   /* ══════════ 8. add2 — §A 알약 · §B 아랫줄 · §C P · §D ✎ 여기서 고치기 ══════════ */
   await grp('W', async()=>{
     const uid='G25-62-09', no=rowByUid(uid)[F.NO];
     await openView(no); await wait(900);

     /* ───── §A 머리줄 알약 ───── */
     const pill=document.getElementById('inkPill');
     T('W-1 ★#inkPill 이 .vtop 안이다',!!pill&&!!pill.closest('#view .vtop'),
       pill?String(pill.parentElement&&pill.parentElement.className):'(없음)');
     const pb=pill?[...pill.querySelectorAll('button')]:[];
     T('W-1 ★단추 아홉(펜 3 · 형광 3 · 지우개 · 글상자 · ↺)',pb.length===9,
       pb.map(b=>b.id||b.dataset.pen||b.dataset.hl));
     T('W-1 그 아홉이 옮겨 온 그 단추들이다',
       !!pill&&pill.querySelectorAll('[data-pen]').length===3&&pill.querySelectorAll('[data-hl]').length===3
       &&!!pill.querySelector('#tErase')&&!!pill.querySelector('#tTxt')&&!!pill.querySelector('#tUndo'));
     T('W-1 칸막이 둘(펜│형광│도구)',pill&&pill.querySelectorAll('.sep').length===2,
       pill?pill.querySelectorAll('.sep').length:null);
     T('W-1 ★알약 높이 ≤ 26px',pill.getBoundingClientRect().height<=26,pill.getBoundingClientRect().height);
     T('W-1 글자는 CSS 로 가렸다(textContent 는 그대로)',
       getComputedStyle(pill.querySelector('#tErase')).fontSize==='0px'
       &&txt(pill.querySelector('#tErase'))==='지우개',
       [getComputedStyle(pill.querySelector('#tErase')).fontSize,txt(pill.querySelector('#tErase'))]);
     /* 카드를 맨 아래로 굴려도 알약이 보인다(카드 .cmeta 가 아니라 머리줄에 둔 까닭) */
     {const sc=['#cardwrap','#ebody','#card'].map(q=>$(q)).find(el=>el&&el.scrollHeight>el.clientHeight+10);
      if(sc){sc.scrollTop=sc.scrollHeight; await wait(300)}
      const q=pill.getBoundingClientRect(), vr=$('#view').getBoundingClientRect();
      T('W-1 ★카드를 맨 아래로 굴려도 알약이 보인다',
        pill.offsetParent!==null&&q.height>0&&q.top>=vr.top-1&&q.bottom<=vr.bottom+1,
        [sc?sc.id:'(안 굴러감)',q.top,q.bottom,vr.top,vr.bottom]);}

     /* 빨강 펜 · 형광 초록 — 옮긴 단추가 그대로 먹는가.
        ⚠ 바로 위에서 카드를 맨 아래로 굴려 놨다 — 되돌리지 않으면 `#qink` 가 화면 밖이라
          빈 자리 찾기가 늘 0,0 을 돌려준다(2026-09-20 실측). */
     {['#cardwrap','#ebody','#card'].forEach(x=>{const el=$(x);if(el)el.scrollTop=0});
      await wait(250);
      await del('ink','qink:'+uid); await qLoad(uid); await wait(200);
      const sv=$('#card #qink'), r=sv.getBoundingClientRect();
      const freeAt=(u,v)=>{const x=r.left+u*r.width,y=r.top+v*r.width;
        if(x<4||y<4||x>document.documentElement.clientWidth-4||y>document.documentElement.clientHeight-4)return false;
        try{return !underInk(x,y,sv)}catch(e){return false}};
      let pu=0,pv=0,found=false;
      for(let v=0.03;v<=0.40&&!found;v+=0.03)for(let u=0.03;u<=0.50&&!found;u+=0.03)
        if(freeAt(u,v)&&freeAt(u+0.18,v+0.07)&&freeAt(u+0.36,v+0.14)){pu=u;pv=v;found=true}
      T('W-1 획을 그을 빈 자리를 찾았다',found,[pu,pv]);
      const path=[r.width*pu,r.width*pv,r.width*(pu+0.18),r.width*(pv+0.07),
                  r.width*(pu+0.36),r.width*(pv+0.14)];
      pill.querySelector('[data-pen="#B03A2E"]').click(); await wait(150); qWire(); await wait(80);
      T('W-1 빨강 펜 단추에 on 이 붙는다',pill.querySelector('[data-pen="#B03A2E"]').classList.contains('on'));
      let n0=((QINK.s)||[]).length;
      await draw1(sv,path);
      let st=((QINK.s)||[])[((QINK.s)||[]).length-1];
      T('W-1 ★알약 빨강 펜으로 그은 획이 #B03A2E 로 저장된다',
        ((QINK.s)||[]).length===n0+1&&!!st&&st.c==='#B03A2E'&&!st.hl,[((QINK.s)||[]).length,st&&st.c,st&&st.hl]);
      pill.querySelector('[data-hl="#7FD1AE"]').click(); await wait(150); qWire(); await wait(80);
      n0=((QINK.s)||[]).length;
      await draw1(sv,path.map((v,i)=>i%2?v+r.width*0.05:v));
      st=((QINK.s)||[])[((QINK.s)||[]).length-1];
      T('W-1 ★알약 형광 초록 획이 #7FD1AE · 형광 꼴',
        ((QINK.s)||[]).length===n0+1&&!!st&&st.c==='#7FD1AE'&&st.hl===1,[((QINK.s)||[]).length,st&&st.c,st&&st.hl]);
      /* ↺ */
      const nn=((QINK.s)||[]).length;
      pill.querySelector('#tUndo').click(); await until(()=>((QINK.s)||[]).length===nn-1,5000);
      T('W-1 ↺ 가 마지막 획을 무른다(옮기기 전과 같다)',((QINK.s)||[]).length===nn-1,[nn,((QINK.s)||[]).length]);
      /* 지우개 · 글상자 */
      pill.querySelector('#tErase').click(); await wait(150);
      T('W-1 지우개를 고르면 TOOL.mode=erase',TOOL.mode==='erase',TOOL.mode);
      pill.querySelector('#tTxt').click(); await wait(200);
      T('W-1 글상자 단추가 QTXT 를 켠다',QTXT===true&&pill.querySelector('#tTxt').classList.contains('on'),
        [QTXT,pill.querySelector('#tTxt').className]);
      pill.querySelector('#tTxt').click(); await wait(200);
      T('W-1 다시 누르면 꺼진다',QTXT===false,QTXT);
      setTool('view'); qWire(); await wait(100);
      await del('ink','qink:'+uid); await qLoad(uid); await wait(150);}

     /* 알약 단추를 끌어도 창이 안 움직인다 · 머리줄 빈 곳은 움직인다 */
     {const v=$('#view');
      if(v.classList.contains('win')){
        const r0=v.getBoundingClientRect(), eb=pill.querySelector('#tErase');
        await drag(eb,r0.left+30,r0.top+14,r0.left+110,r0.top+74,'mouse'); await wait(250);
        const r1=v.getBoundingClientRect();
        T('W-1 ★알약 단추를 눌러 끌어도 창 자리가 그대로다',
          Math.abs(r1.left-r0.left)<3&&Math.abs(r1.top-r0.top)<3,[r0.left,r1.left,r0.top,r1.top]);
        const vt=$('#view .vtop'), tr=vt.getBoundingClientRect();
        await drag(vt,tr.left+4,tr.top+3,tr.left+54,tr.top+43,'mouse'); await wait(250);
        const r2=v.getBoundingClientRect();
        T('W-1 머리줄 빈 곳을 끌면 창이 움직인다',
          Math.abs(r2.left-(r1.left+50))<4&&Math.abs(r2.top-(r1.top+40))<4,[r1.left,r2.left,r1.top,r2.top]);
      }else T('W-1 문항 창이 떠 있는 창이다',false,v.className)}

     /* 창이 좁으면 둘째 줄로(오른쪽 맞춤) — §A-1 */
     {const v=$('#view'), w0=v.style.width;
      v.style.width='420px'; await wait(350);
      const pr=pill.getBoundingClientRect(), tt=$('#view .vtop .title').getBoundingClientRect(),
            hr=$('#view .vtop').getBoundingClientRect();
      T('W-1 ★창이 좁으면 알약이 둘째 줄로 내려간다',pr.top>=tt.bottom-1,[pr.top,tt.bottom,pr.right,hr.right]);
      T('W-1 그때 오른쪽 맞춤',Math.abs(hr.right-pr.right)<=14,[hr.right,pr.right]);
      v.style.width=w0; await wait(350);}

     /* ───── §B 아랫줄 다섯 ───── */
     {const kids=[...document.querySelectorAll('.vbot .tools>*')];
      const vis=kids.filter(el=>el.offsetParent!==null);
      /* ★ _task_jagwa_claude_slot_add1 §A-2 (2026-09-22) — 맨 오른쪽에 「Claude」(#tGpt)가
         **하나 더 선다.** 다섯 -> 여섯이 이 판이 뜻한 것이고, 앞 다섯의 차례는 그대로여야 한다.
         (묶음 CL2 가 꼴·동작을 따로 잰다) */
      /* ★ 2026-10-07 (_task_jagwa_phys_win §A-04 ⑪ · ⑥) — 세 과목 아랫줄 회독 고르개·+회독·👁(#tLayer·#tLayerAdd·#tLayerEye) 숨김(회독 창 #hsPop 으로 합침) = 뜻한 차
         → 새 꼴 = 기록 · 🃏 · Claude 셋도 받는다 · 옛: vis.length===6 · 옛: vis.map(el=>el.id).join(',')==='tLayer,tLayerAdd,tLayerEye,tHist,tCard,tGpt' */
      T('W-2 ★아랫줄에 보이는 것이 여섯(다섯 + 맨 오른쪽 Claude)',vis.length===6||vis.map(el=>el.id).join(',')==='tHist,tCard,tGpt',vis.map(el=>el.id||el.className));
      T('W-2 ★그 여섯 = 회독 층 · +회독 · 👁 · 기록 · 암기카드 · Claude',
        ['tLayer,tLayerAdd,tLayerEye,tHist,tCard,tGpt','tHist,tCard,tGpt'].indexOf(vis.map(el=>el.id).join(','))>=0,vis.map(el=>el.id));
      T('W-2 오른쪽 맞춤',getComputedStyle($('.vbot .tools')).justifyContent==='flex-end',
        getComputedStyle($('.vbot .tools')).justifyContent);
      T('W-2 ★굵기 #tW 안 보임 · 값 2',$('#tW').offsetParent===null&&$('#tW').value==='2',
        [$('#tW')?getComputedStyle($('#tW')).display:'(없음)',$('#tW').value]);
      T('W-2 필기 단추는 아랫줄에 없다(알약으로 갔다)',
        document.querySelectorAll('.vbot .tools [data-pen]').length===0
        &&document.querySelectorAll('.vbot .tools [data-hl]').length===0
        &&!document.querySelector('.vbot .tools #tErase')&&!document.querySelector('.vbot .tools #tTxt'),
        [document.querySelectorAll('.vbot .tools [data-pen]').length,
         !!document.querySelector('.vbot .tools #tErase')]);
      T('W-2 #mP 는 아랫줄에서 숨는다(근거 아랫줄로 갔다)',$('#mP')&&$('#mP').offsetParent===null,
        $('#mP')?getComputedStyle($('#mP')).display:'(없음)');}
     /* +회독 → 층 +1 · 그 층에 그은 획이 그 층에 */
     {const r0=QR;
      $('#tLayerAdd').click(); await wait(400);
      T('W-2 ★+회독 → 층 +1',QR===r0+1,[r0,QR]);
      setTool('pen','#16181B'); qWire(); await wait(120);
      const sv=$('#card #qink'), r=sv.getBoundingClientRect();
      const freeAt=(u,v)=>{const x=r.left+u*r.width,y=r.top+v*r.width;
        if(x<4||y<4||x>document.documentElement.clientWidth-4||y>document.documentElement.clientHeight-4)return false;
        try{return !underInk(x,y,sv)}catch(e){return false}};
      let pu=0,pv=0,found=false;
      for(let v=0.03;v<=0.40&&!found;v+=0.03)for(let u=0.03;u<=0.50&&!found;u+=0.03)
        if(freeAt(u,v)&&freeAt(u+0.18,v+0.07)&&freeAt(u+0.36,v+0.14)){pu=u;pv=v;found=true}
      await draw1(sv,[r.width*pu,r.width*pv,r.width*(pu+0.18),r.width*(pv+0.07),
                      r.width*(pu+0.36),r.width*(pv+0.14)]);
      const st=((QINK.s)||[])[((QINK.s)||[]).length-1];
      T('W-2 ★그 층에 그은 획이 그 층에 들어간다',!!st&&qRoundOf(st)===QR,[st&&st.r,QR]);
      setTool('view'); qWire(); await wait(100);
      await del('ink','qink:'+uid); await qLoad(uid); await wait(150);}

     /* ───── §C P = 넷째 단추 ───── */
     {const boxes=$$$('#card .vox');
      const vp=$('#card .vox.vP');
      T('W-3 ★근거 아랫줄 단추 넷 · 넷째가 P',boxes.length===4&&!!vp&&boxes[3]===vp,
        boxes.map(b=>b.className+':'+txt(b)));
      T('W-3 title 이 아랫줄 #mP 것 그대로',!!vp&&!!$('#mP')&&vp.title===$('#mP').title,
        [vp&&vp.title,$('#mP')&&$('#mP').title]);
      const h0=hist(no).length;
      vp.click(); await wait(600);
      T('W-3 ★P 를 누르면 기록 마지막이 P',lastM(no)==='P'&&hist(no).length===h0+1,
        [lastM(no),h0,hist(no).length]);
      T('W-3 ★켜지면 먹색(아랫줄 #mP 와 같은 바탕)',
        vp.classList.contains('on')
        &&getComputedStyle(vp).backgroundColor===getComputedStyle($('#mP')).backgroundColor,
        [vp.className,getComputedStyle(vp).backgroundColor,getComputedStyle($('#mP')).backgroundColor]);
      closeView(); await wait(450);
      {const idx=nums().indexOf(codeShow(rec(no)));const cell=$$$('#spec i')[idx];
       T('W-3 ★히트맵 칸이 P 로 따라간다',idx>=0&&!!cell&&/(^|\s)P(\s|$)/.test(cell.className),
         [idx,cell&&cell.className]);}
      await openView(no); await wait(700);
      $('#card .vox.vO').click(); await wait(600);
      T('W-3 다시 O 를 누르면 O 로 돌아온다',
        lastM(no)==='O'&&$('#card .vox.vO').classList.contains('on')
        &&!$('#card .vox.vP').classList.contains('on'),
        [lastM(no),$('#card .vox.vP').className]);}

     /* ───── §D 「✎ 여기서 고치기」 ───── */
     {const U='G25-62-09', A='G02-39-02';
      GG={};GGREF={};
      GG[U]=[{k:'g_t1',i:1,t:'ㄱ 처음 글',ok:'O',ts:1,
              parts:[{l:'ㄱ',t:'처음 글'}],cs:[{k:'c_t1',t:'댓글 처음',ts:1}]}];
      GGREF[A]=[U];
      await saveGG(); await saveGGREF();
      const noA=rowByUid(A)[F.NO];
      await openView(noA); await wait(900);
      const chip=$('#card [data-ggrt]');
      T('W-4 연결 칩이 있다',!!chip,chip?txt(chip):null);
      chip.click(); await wait(350);
      let box=$('#card .ggrefbox');
      T('W-4 상자가 펴진다',!!box&&!box.classList.contains('hide'),box?box.className:null);
      const eb=box.querySelector('[data-ggre]');
      T('W-4 ★항목에 「✎ 여기서 고치기」가 있다',!!eb&&txt(eb)==='✎ 여기서 고치기',eb?txt(eb):null);
      eb.click(); await wait(300);
      const edb=box.querySelector('[data-ggre-box]');
      T('W-4 편집 줄 = [라벨][칸] + ＋ 병렬 + 저장(add1 의 그 줄)',
        !!edb&&!edb.classList.contains('hide')&&!!edb.querySelector('.ggrow .lab')
        &&!!edb.querySelector('.ggrow .txt')&&!!edb.querySelector('[data-ggedplus]')
        &&!!edb.querySelector('[data-ggedsave]'),
        edb?edb.className:null);
      T('W-4 저장된 글이 칸에 들어 있다',
        edb.querySelector('.ggrow .lab').value==='ㄱ'&&edb.querySelector('.ggrow .txt').value==='처음 글',
        [edb.querySelector('.ggrow .lab').value,edb.querySelector('.ggrow .txt').value]);
      edb.querySelector('.ggrow .txt').value='고친 글';
      edb.querySelector('[data-ggedsave]').click();
      await until(()=>(ggOf(U)[0]||{}).t==='ㄱ 고친 글',6000); await wait(400);
      const g=ggOf(U)[0];
      T('W-4 ★GG[그 문항] 항목의 글이 바뀐다(사본 아님)',!!g&&g.t==='ㄱ 고친 글',g&&g.t);
      T('W-4 ★k·i·ok·ts·댓글은 무변',
        !!g&&g.k==='g_t1'&&g.i===1&&g.ok==='O'&&g.ts===1
        &&(g.cs||[]).length===1&&g.cs[0].k==='c_t1'&&g.cs[0].ts===1,
        g?[g.k,g.i,g.ok,g.ts,(g.cs||[]).length]:null);
      T('W-4 ★사본이 0 — GG 열쇠 하나 · 목록 하나',
        Object.keys(GG).length===1&&Object.keys(GG)[0]===U&&ggOf(U).length===1,
        [Object.keys(GG),ggOf(U).length]);
      box=$('#card .ggrefbox');
      T('W-4 ★고친 상자는 펼친 채로 남는다',!!box&&!box.classList.contains('hide'),box?box.className:null);
      T('W-4 상자에 새 글이 보인다',txt(box).indexOf('고친 글')>=0,txt(box).slice(0,140));
      /* 댓글 */
      const ce=box.querySelector('[data-ggrce]');
      T('W-4 ★댓글에도 「✎ 여기서 고치기」',!!ce&&txt(ce)==='✎ 여기서 고치기',ce?txt(ce):null);
      ce.click(); await wait(300);
      const cb=$('#card [data-ggrce-box]');
      T('W-4 댓글 편집은 한 칸',!!cb&&!cb.classList.contains('hide')&&!!cb.querySelector('textarea.cein'),
        cb?cb.className:null);
      cb.querySelector('textarea').value='고친 댓글';
      cb.querySelector('[data-ggcesave]').click();
      await until(()=>((ggOf(U)[0]||{}).cs||[{}])[0].t==='고친 댓글',6000); await wait(350);
      const c2=((ggOf(U)[0]||{}).cs||[])[0];
      T('W-4 ★댓글 글만 바뀌고 k·ts 는 무변',
        !!c2&&c2.t==='고친 댓글'&&c2.k==='c_t1'&&c2.ts===1,c2?[c2.t,c2.k,c2.ts]:null);
      /* 병렬 줄 */
      {const b2=$('#card .ggrefbox');
       b2.querySelector('[data-ggre]').click(); await wait(300);
       const e2=$('#card [data-ggre-box]');
       e2.querySelector('[data-ggedplus]').click(); await wait(250);
       const rows=[...e2.querySelectorAll('.ggrow')];
       T('W-4 ＋ 병렬 → 줄이 둘',rows.length===2,rows.length);
       rows[1].querySelector('.lab').value='ㄴ';
       rows[1].querySelector('.txt').value='둘째 줄';
       e2.querySelector('[data-ggedsave]').click();
       await until(()=>((ggOf(U)[0]||{}).parts||[]).length===2,6000); await wait(350);
       const g2=ggOf(U)[0];
       T('W-4 ★병렬 항목은 줄마다 고쳐진다',
         (g2.parts||[]).length===2&&g2.parts[1].l==='ㄴ'&&g2.parts[1].t==='둘째 줄'
         &&g2.t===('ㄱ 고친 글'+String.fromCharCode(10)+'ㄴ 둘째 줄'),
         [(g2.parts||[]).length,g2.t]);}
      /* 그 문항을 열면 새 글 */
      await openView(no); await wait(900);
      T('W-4 ★그 문항을 열면 근거에 새 글이 있다',
        txt($('#card .ggbox')).indexOf('고친 글')>=0,txt($('#card .ggbox')).slice(0,180));
      /* 정리 창에도 같은 단추 */
      {closeView(); await wait(300);
       const sec=String(unitOf(noA)||'').split('.').slice(0,2).join('.');
       jnOpen(sec); await wait(900);
       const jw=document.getElementById('jnw');
       T('W-4 정리 창에도 「✎ 여기서 고치기」가 있다',
         !!jw&&jw.querySelectorAll('[data-ggre]').length>=1,
         [!!jw,jw?jw.querySelectorAll('[data-ggre]').length:null,sec]);
       const x=document.getElementById('jnwX'); if(x)x.click(); await wait(200);}
      await cap('W_연결근거상자','<div>'+(($('#card')||{}).innerHTML||'')+'</div>');
      GG={};GGREF={};await saveGG();await saveGGREF();draw();await wait(250);}
     closeView(); await wait(250);
   });

   /* ══════════ 9. add3 ① 글상자·지우개 엉킴 ══════════ */
   await grp('E', async()=>{
     const uid='G25-62-09', no=rowByUid(uid)[F.NO];
     await openView(no); await wait(900);
     await del('ink','qink:'+uid); await qLoad(uid); await wait(200);
     const card=$('#card'), pill=document.getElementById('inkPill');
     const q=s=>(pill&&pill.querySelector(s))||$(s);
     const tTxt=q('#tTxt'), tEr=q('#tErase'), tPen=q('[data-pen="#16181B"]'), tHl=q('[data-hl="#F2C230"]');
     const nBox=()=>card.querySelectorAll('#qtxt .tbox').length;
     const onCnt=()=>document.querySelectorAll('[data-pen].on,[data-hl].on,#tErase.on').length;
     /* 획을 그을 빈 자리 — `#qink` 가 덮고 있고 밑에 눌릴 것이 없는 곳 */
     setTool('pen','#16181B'); qWire(); await wait(150);
     const sv=$('#card #qink'), rr=sv.getBoundingClientRect();
     const freeAt=(u,v)=>{const x=rr.left+u*rr.width,y=rr.top+v*rr.width;
       if(x<4||y<4||x>document.documentElement.clientWidth-4||y>document.documentElement.clientHeight-4)return false;
       try{return !underInk(x,y,sv)}catch(e){return false}};
     let pu=0,pv=0,found=false;
     for(let v=0.03;v<=0.40&&!found;v+=0.03)for(let u=0.03;u<=0.50&&!found;u+=0.03)
       if(freeAt(u,v)&&freeAt(u+0.14,v+0.05)&&freeAt(u+0.28,v+0.10)){pu=u;pv=v;found=true}
     T('E-0 획을 그을 빈 자리를 찾았다',found,[pu,pv]);
     await draw1(sv,[rr.width*pu,rr.width*pv,rr.width*(pu+0.14),rr.width*(pv+0.05),
                     rr.width*(pu+0.28),rr.width*(pv+0.10)]);
     T('E-0 펜으로 한 획을 그었다',((QINK.s)||[]).length===1,((QINK.s)||[]).length);
     /* 글상자 켜기 */
     const b0=nBox();
     tTxt.click(); await wait(300);
     T('E-1 글상자가 켜진다',QTXT===true&&card.classList.contains('txton')&&tTxt.classList.contains('on'),
       [QTXT,card.className,tTxt.className]);
     T('E-1 ★그때 펜·형광·지우개 .on 이 0 · #card.penon 없음',
       onCnt()===0&&!card.classList.contains('penon'),[onCnt(),card.className]);
     {/* ⚠ 글상자는 획 **시작점**에 만든다 — 지우개 시험은 획 가운데서 하므로 자리가 겹치면 안 된다 */
      const x=rr.left+rr.width*pu, y=rr.top+rr.width*pv;
      const top=document.elementFromPoint(x,y);
      T('E-1 그 자리 맨 위가 글상자 층(#qtxt)이다',!!top&&(top.id==='qtxt'||!!top.closest('#qtxt')),
        top?(top.id||top.className):null);
      await fire(card.querySelector('#qtxt'),'pointerdown',x,y,'pen',41); await wait(350);
      T('E-1 ★글상자 모드에서 톡 = 글상자 +1',nBox()===b0+1,[b0,nBox()]);}
     /* 지우개 — ①의 본문 */
     tEr.click(); await wait(300);
     T('E-2 ★지우개를 고르면 QTXT 가 꺼진다',QTXT===false,QTXT);
     T('E-2 ★#card.txton 없음 · #tTxt.on 없음',
       !card.classList.contains('txton')&&!tTxt.classList.contains('on'),[card.className,tTxt.className]);
     T('E-2 지우개가 켜졌다(TOOL.mode=erase · penon)',TOOL.mode==='erase'&&card.classList.contains('penon'),
       [TOOL.mode,card.className]);
     {const x=rr.left+rr.width*(pu+0.14), y=rr.top+rr.width*(pv+0.05);
      const top=document.elementFromPoint(x,y);
      /* ⚠ `#qink` 는 <svg> 다 — 그 자리에 획이 있으면 맨 위는 그 <path> 다.
         id·className 으로 가르면 안 된다(SVG 의 className 은 문자열이 아니라 객체다 · 2026-09-20 실측). */
      T('E-2 ★그 자리 맨 위가 다시 필기 덮개(#qink)다',
        !!top&&(top.id==='qink'||!!(top.closest&&top.closest('#qink'))),
        top?(top.id||String(top.tagName)):null);
      const nb=nBox(), ns=((QINK.s)||[]).length;
      await fire(sv,'pointerdown',x,y,'pen',42); await wait(120);
      await fire(sv,'pointerup',x,y,'pen',42); await wait(400);
      T('E-2 ★획 위를 누르면 획 −1',((QINK.s)||[]).length===ns-1,[ns,((QINK.s)||[]).length]);
      T('E-2 ★그때 글상자는 +0',nBox()===nb,[nb,nBox()]);}
     /* 펜·형광도 같다 */
     tTxt.click(); await wait(250);
     T('E-3 글상자 다시 켬',QTXT===true);
     tPen.click(); await wait(250);
     T('E-3 ★펜을 고르면 QTXT 가 꺼진다',QTXT===false&&!card.classList.contains('txton'),[QTXT,card.className]);
     tTxt.click(); await wait(250);
     tHl.click(); await wait(250);
     T('E-3 ★형광을 고르면 QTXT 가 꺼진다',QTXT===false&&!card.classList.contains('txton'),[QTXT,card.className]);
     /* 글상자 다시 누름 = 꺼짐 · 톡해도 +0 */
     tTxt.click(); await wait(250);
     tTxt.click(); await wait(250);
     T('E-4 글상자를 다시 누르면 꺼진다',QTXT===false&&!tTxt.classList.contains('on'),[QTXT,tTxt.className]);
     {const nb=nBox(), x=rr.left+rr.width*(pu+0.30), y=rr.top+rr.width*(pv+0.16);
      const h=card.querySelector('#qtxt');
      await fire(h,'pointerdown',x,y,'pen',43); await wait(300);
      T('E-4 ★꺼진 채 톡하면 글상자 +0',nBox()===nb,[nb,nBox()]);}
     T('E-5 이미 선 글상자를 누르는 길은 그대로다(.tbox 는 고치기)',
       String(qTxtWire).indexOf(".closest('.tbox')")>=0);
     setTool('view'); qWire(); await wait(120);
     await del('ink','qink:'+uid); await qLoad(uid); await wait(150);
     closeView(); await wait(250);
   });

   /* ══════════ 10. add3 ② 펜으로 근거 줄이 눌린다 ══════════ */
   await grp('N', async()=>{
     const A='G02-39-02', U='G25-62-09';
     GG={};GGREF={};
     GG[U]=[{k:'g_n1',i:1,t:'ㄱ 남의 근거',ok:'O',ts:1,cs:[{k:'c_n1',t:'댓글',ts:1}]}];
     GG[A]=[{k:'g_n2',i:1,t:'내 근거 하나',ok:'O',ts:1,cs:[]}];
     {const third=(DATA.filter(r=>!isC(r)).map(r=>r[F.CODE]).find(u=>u!==A&&u!==U));
      if(third)GG[third]=[{k:'g_n3',i:1,t:'셋째 문항 근거',ok:'O',ts:1,cs:[]}];}
     GGREF[A]=[U];
     await saveGG(); await saveGGREF();
     const noA=rowByUid(A)[F.NO];
     await openView(noA); await wait(900);
     await del('ink','qink:'+A); await qLoad(A); await wait(200);
     const card=$('#card'), sv=card.querySelector('#qink');
     /* 펜 도구를 켠다 — 덮개가 카드를 통째로 덮는 상태 */
     setTool('pen','#16181B'); qWire(); await wait(200);
     T('N-0 펜 도구가 켜졌다(#card.penon · #qink pointer-events auto)',
       card.classList.contains('penon')&&getComputedStyle(sv).pointerEvents==='auto',
       [card.className,getComputedStyle(sv).pointerEvents]);
     T('N-0 ★근거 덩어리가 덮개 위다(.ggtop z-index 8 > #qink 6)',
       !!card.querySelector('.ggtop')&&getComputedStyle(card.querySelector('.ggtop')).zIndex==='8'
       &&getComputedStyle(sv).zIndex==='6',
       [card.querySelector('.ggtop')?getComputedStyle(card.querySelector('.ggtop')).zIndex:null,
        getComputedStyle(sv).zIndex]);
     const ink0=((QINK.s)||[]).length;
     /* 자리마다 「맨 위가 그것인가」 — 덮개에 안 먹히는지 그대로 잰다(픽셀 아님) */
     const mid=el=>{const r=el.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]};
     const tops=(el)=>{try{el.scrollIntoView({block:'center'})}catch(_){}
       const [x,y]=mid(el);const a=document.elementsFromPoint(x,y);
       const i=a.indexOf(el);
       /* `#qink` 는 <svg> 라 그 안의 <path> 가 잡힐 수 있다 — closest 로 본다 */
       const j=a.findIndex(z=>z&&(z.id==='qink'||(z.closest&&z.closest('#qink'))));
       return {i:i,j:j,ok:(i>=0&&(j<0||i<j))}};
     const chk=(q,ko)=>{const el=card.querySelector(q);
       if(!el){T('N-1 '+ko+' 가 있다',false,q);return null}
       const r=tops(el);
       T('N-1 ★'+ko+' 가 덮개보다 위다',r.ok,[q,r.i,r.j]);return el};
     chk('.ggnum','번호 칩'); chk('[data-ggfind]','🔍');   /* 「!」 는 판을 편 뒤에 — 기본은 접혀 있다 */
     chk('.ggref','🔗 연결 칩'); chk('#cDetBtn','정답·해설'); chk('.vox.vO','O');
     chk('.ggrow .txt','적는 칸'); chk('.ggrow .lab','라벨 칸');
     /* 눌러서 되는지 */
     {const num=card.querySelector('.ggnum'); num.click(); await wait(300);
      T('N-2 번호 칩을 누르면 판이 펴진다',
        !!card.querySelector('.ggpan')&&!card.querySelector('.ggpan').classList.contains('hide'),
        card.querySelector('.ggpan')?card.querySelector('.ggpan').className:null);
      chk('.ggpan:not(.hide) .ggbang','판 안의 「!」');
      num.click(); await wait(200);}
     {const bg=card.querySelector('.ggbox .ggbang'); const was=!!(ggOf(A)[0]||{}).bang;
      if(bg){bg.click(); await until(()=>!!(ggOf(A)[0]||{}).bang!==was,4000);
        T('N-2 「!」가 뒤집힌다',!!(ggOf(A)[0]||{}).bang!==was,[was,!!(ggOf(A)[0]||{}).bang]);
        bg.click(); await wait(300)}
      else T('N-2 「!」가 있다',false)}
     {card.querySelector('[data-ggfind]').click(); await wait(400);
      const fb=card.querySelector('[data-ggfindbox]');
      T('N-2 🔍 를 누르면 찾기 상자가 열린다',!!fb&&!fb.classList.contains('hide'),fb?fb.className:null);
      const rows=[...card.querySelectorAll('[data-ggfindbox] .ggres')];
      const res=rows.find(x=>!x.classList.contains('on'))||rows[0];
      T('N-2 아직 안 걸린 결과 줄이 있다',!!res&&!res.classList.contains('on'),
        rows.map(x=>x.className));
      if(res){const r=tops(res);
        T('N-2 ★결과 줄이 덮개보다 위다',r.ok,[r.i,r.j]);
        const n0=ggRefOf(A).length;
        res.click(); await until(()=>ggRefOf(A).length===n0+1,4000); await wait(300);
        T('N-2 ★결과 줄을 누르면 연결 +1',ggRefOf(A).length===n0+1,[n0,ggRefOf(A).length]);}}
     {const rt=card.querySelector('[data-ggrt]');
      if(rt){rt.click(); await wait(300);
        T('N-2 연결 칩을 누르면 상자가 펴진다',
          !!card.querySelector('.ggrefbox')&&!card.querySelector('.ggrefbox').classList.contains('hide'));}
      else T('N-2 연결 칩이 있다',false)}
     T('N-2 ★그동안 획은 하나도 안 늘었다',((QINK.s)||[]).length===ink0,[ink0,((QINK.s)||[]).length]);
     /* 근거 덩어리 밖에서는 그대로 획이 된다 */
     {const rr=sv.getBoundingClientRect();
      const gt=card.querySelector('.ggtop').getBoundingClientRect();
      const freeAt=(u,v)=>{const x=rr.left+u*rr.width,y=rr.top+v*rr.width;
        if(x<4||y<4||x>document.documentElement.clientWidth-4||y>document.documentElement.clientHeight-4)return false;
        if(y>=gt.top-2)return false;                       /* 근거 덩어리 위쪽(문제 글·여백) */
        try{return !underInk(x,y,sv)}catch(e){return false}};
      let pu=0,pv=0,found=false;
      for(let v=0.03;v<=0.40&&!found;v+=0.03)for(let u=0.03;u<=0.50&&!found;u+=0.03)
        if(freeAt(u,v)&&freeAt(u+0.14,v+0.05)&&freeAt(u+0.28,v+0.10)){pu=u;pv=v;found=true}
      T('N-3 근거 덩어리 밖 빈 자리를 찾았다',found,[pu,pv,gt.top]);
      const n0=((QINK.s)||[]).length;
      await draw1(sv,[rr.width*pu,rr.width*pv,rr.width*(pu+0.14),rr.width*(pv+0.05),
                      rr.width*(pu+0.28),rr.width*(pv+0.10)]);
      T('N-3 ★근거 덩어리 밖 펜 획은 그대로 그어진다',((QINK.s)||[]).length===n0+1,
        [n0,((QINK.s)||[]).length]);}
     /* 선택지·보기 줄은 옛 길 그대로(덮개 밑) */
     {const c=card.querySelector('.choices button');
      if(!c)T('N-4 선택지가 있다',false);
      else{const r=tops(c);
        T('N-4 ★선택지는 덮개 **밑** 그대로다(inkPierce 가 맡는다)',r.j>=0&&(r.i<0||r.j<r.i),[r.i,r.j])}}
     /* 손가락 거르개 */
     {const ok=typeof PASS_THRU==='string';
      T('N-5 PASS_THRU 를 읽을 수 있다',ok);
      if(ok){const miss=['.ggnum','.ggbang','.ggref','.ggres','.gguse']
        .filter(q=>{const el=document.createElement('div');el.className=q.slice(1);
          return !el.matches(PASS_THRU)});
        T('N-5 ★근거 덩어리 선택자가 손가락 거르개에 다 들었다',miss.length===0,miss)}}
     /* 옛 획이 근거 자리에 있어도 글자가 안 가려진다 */
     {const gt=card.querySelector('.ggtop').getBoundingClientRect(), rr=sv.getBoundingClientRect();
      const u=(gt.left+gt.width*0.4-rr.left)/rr.width, v=(gt.top+18-rr.top)/rr.width;
      const n0=((QINK.s)||[]).length;
      QINK.s.push({c:'#16181B',w:2,hl:0,r:QR,p:[u,v,u+0.05,v+0.01,u+0.1,v+0.02]});
      qPaint(); await wait(250);
      const num=card.querySelector('.ggnum');
      const r=num?tops(num):{ok:false};
      T('N-6 ★근거 자리에 옛 획이 있어도 근거가 위다',r.ok,[r.i,r.j]);
      T('N-6 INK 데이터는 그대로 있다(안 지운다)',((QINK.s)||[]).length===n0+1,[n0,((QINK.s)||[]).length]);
      QINK.s.pop(); qPaint();}
     /* 보기 줄은 **보기가 있는 문항**에서 잰다(G39-02 에는 보기가 없다) */
     {await openView(rowByUid('G15-52-07')[F.NO]); await wait(900);
      setTool('pen','#16181B'); qWire(); await wait(200);
      const c2=$('#card'), bg=c2.querySelector('.bogi .t');
      if(!bg)T('N-4 보기 줄이 있다',false);
      else{try{bg.scrollIntoView({block:'center'})}catch(_){}
        await wait(300);
        const sv2=c2.querySelector('#qink'), sr=sv2?sv2.getBoundingClientRect():null;
        const r0=bg.getBoundingClientRect();
        const a=document.elementsFromPoint(r0.left+r0.width/2,r0.top+r0.height/2);
        const i=a.indexOf(bg);
        const j=a.findIndex(z=>z&&(z.id==='qink'||(z.closest&&z.closest('#qink'))));
        N('N-4 보기 줄 밑준비',{penon:c2.className,pe:sv2?getComputedStyle(sv2).pointerEvents:null,
          ink:sr?[Math.round(sr.top),Math.round(sr.bottom)]:null,
          bogi:[Math.round(r0.top),Math.round(r0.bottom)],
          stack:a.map(z=>z.id||String(z.tagName)).slice(0,6)});
        /* ⚠ 실측 — 이 문항에서는 덮개(`#qink`)의 아래끝이 〈보기〉 줄보다 위다(419 vs 457).
           `qFit` 이 잡는 덮개 높이 얘기이고 **add3 가 만든 것이 아니다**(qFit 무접촉).
           그러니 「덮개가 위에 있다」로 재면 안 된다 — 잴 것은 **내가 안 들어올렸다**는 것이다:
           〈보기〉 줄이 `.ggtop`(z 8) 밖에 있고, 덮개가 닿는 자리에서는 여전히 덮개가 위다. */
        T('N-4 ★보기 줄을 덮개 위로 안 올렸다(.ggtop 밖 — 옛 길 그대로)',
          !bg.closest('.ggtop')&&(j<0||j<i),[i,j,!!bg.closest('.ggtop')]);
        {const yy=sr?Math.min(r0.top+r0.height/2,sr.bottom-6):r0.top;
         const a2=document.elementsFromPoint(r0.left+r0.width/2,yy);
         const j2=a2.findIndex(z=>z&&(z.id==='qink'||(z.closest&&z.closest('#qink'))));
         T('N-4 덮개가 닿는 자리에서는 여전히 덮개가 맨 위다',j2===0,
           [j2,a2.map(z=>z.id||String(z.tagName)).slice(0,4)])}}
      setTool('view'); qWire(); await wait(120);}
     setTool('view'); qWire(); await wait(120);
     await del('ink','qink:'+A); await qLoad(A); await wait(150);
     /* 위 검색 줄 「🔗 근거」 결과 줄 */
     closeView(); await wait(300);
     {ggSearchMode('g'); const qi=$('#q'); qi.value='근거'; ggResBox('근거'); await wait(400);
      const row=document.querySelector('#esres .ggres');
      T('N-7 위 검색 줄에 결과 줄이 있다',!!row,document.getElementById('esres')?document.getElementById('esres').innerHTML.slice(0,90):null);
      if(row){row.click(); await until(()=>VNO!==null,5000); await wait(400);
        T('N-7 ★그 줄을 누르면 문항 창이 열린다',VNO!==null&&!$('#view').classList.contains('hide'),[VNO]);
        closeView(); await wait(250)}
      qi.value=''; ggSearchMode('q'); await wait(250);}
     GG={};GGREF={};await saveGG();await saveGGREF();draw();await wait(250);
   });

   /* ══════════ 11. add3 ③ 쓰임 수 · 쓰임 목록 창 · 찾기 결과 줄 ══════════ */
   await grp('U', async()=>{
     const T0='G25-62-09';
     const pool=DATA.filter(r=>!isC(r)&&r[F.CODE]!==T0).map(r=>r[F.CODE]);
     const mk=n=>{GGREF={};pool.slice(0,n).forEach(u=>{GGREF[u]=[T0]})};
     GG={};GG[T0]=[{k:'g_u1',i:1,t:'ㄱ 쓰임 시험 근거',ok:'O',ts:1,
                    parts:[{l:'ㄱ',t:'쓰임 시험 근거'}],cs:[{k:'c_u1',t:'댓글 하나',ts:1}]}];
     const css=el=>getComputedStyle(el).color;
     const muted=getComputedStyle(document.documentElement).getPropertyValue('--muted').trim();
     const red=getComputedStyle(document.documentElement).getPropertyValue('--red').trim();
     const asCol=v=>{const d=document.createElement('span');d.style.color=v;document.body.appendChild(d);
       const c=getComputedStyle(d).color;d.remove();return c};
     const cMuted=asCol(muted), cRed=asCol(red);
     const noT=rowByUid(T0)[F.NO];
     for(const n of [1,2,4,5,12]){
       mk(n); await saveGG(); await saveGGREF();
       await openView(noT); await wait(800);
       const lab=$('#card .ggline .lb .gguse');
       if(n<=1){
         T('U-1 n=1 이면 라벨에 숫자가 없다',!lab,lab?txt(lab):null);
       }else{
         T('U-1 n='+n+' 라벨 숫자 = ↩'+n,!!lab&&txt(lab)==='↩'+n,lab?txt(lab):null);
         T('U-1 n='+n+' 색 = '+(n>=5?'빨강':'회색'),!!lab&&css(lab)===(n>=5?cRed:cMuted),
           [lab?css(lab):null,n>=5?cRed:cMuted]);
         T('U-1 n='+n+' 굵기 900',!!lab&&getComputedStyle(lab).fontWeight==='900',
           lab?getComputedStyle(lab).fontWeight:null);
       }
       closeView(); await wait(200);
     }
     /* 세 자리의 수가 서로 같다 — 라벨 · 연결 칩 · 찾기 결과 줄 */
     {mk(4); const A=pool[0];                      /* A 가 T0 를 걸어 두었다 */
      await saveGGREF(); await saveGG();
      const noA=rowByUid(A)[F.NO];
      await openView(noA); await wait(900);
      const chip=$('#card .ggref .gguse');
      T('U-1 ★연결 칩 옆 숫자 = 4(앞 글자 없음)',!!chip&&txt(chip)==='4',chip?txt(chip):null);
      $('#card [data-ggfind]').click(); await wait(500);
      const inp=$('#card [data-ggfindbox] input'); inp.value='쓰임 시험';
      ggFindRun(A,'qp-'); await wait(300);
      const row=$('#card [data-ggfindbox] .ggres');
      T('U-4 ★찾기 결과 줄이 세 줄 꼴(머리줄·문제 글·근거 줄)',
        !!row&&!!row.querySelector('.hd')&&!!row.querySelector('.qq')&&!!row.querySelector('.gl'),
        row?row.innerHTML.slice(0,160):null);
      /* 옛: T('U-4 머리줄 = 코드 칩 · 회차·번호 · 단원',
        !!row&&!!row.querySelector('.hd .cd')&&!!row.querySelector('.hd b')&&!!row.querySelector('.hd .un')
        &&/\d+회 \d+번/.test(txt(row.querySelector('.hd b'))),
        row?txt(row.querySelector('.hd')):null); */
      /* ★ uid_unify G-1(10/4 · 근거 gigu/_task_jagwa_uid_unify.md §G-1 · 앱 ggResRowHTML `(ynUid(r)?'':'<b>회·번</b>')`) — 기출 uid 줄(지학 G25-62-09)은 .cd 에 uid 가 이미 있어 회·번 <b> 를 안 그린다 · 옛 판(ynUid 없음)은 옛 식 그대로 */
      {const yn4=typeof ynUid==='function'&&!!row&&ynUid(rowByUid(T0));
       T('U-4 머리줄 = 코드 칩 · 회차·번호 · 단원',
        !!row&&!!row.querySelector('.hd .cd')&&!!row.querySelector('.hd .un')
        &&(yn4?(!row.querySelector('.hd b')&&!/\d+회 \d+번/.test(txt(row.querySelector('.hd')))&&txt(row.querySelector('.hd .cd'))===codeShow(rowByUid(T0)))
               :(!!row.querySelector('.hd b')&&/\d+회 \d+번/.test(txt(row.querySelector('.hd b'))))),
        row?txt(row.querySelector('.hd')):null)}
      T('U-4 ★이미 연결한 줄 = 「이미 넣음」 + 흐림',
        !!row&&row.classList.contains('on')&&txt(row).indexOf('이미 넣음')>=0
        &&getComputedStyle(row).opacity==='0.5',
        row?[row.className,getComputedStyle(row).opacity,txt(row).slice(0,60)]:null);
      T('U-4 문제 글은 70자까지',!!row&&txt(row.querySelector('.qq')).replace(/…$/,'').length<=70,
        row?txt(row.querySelector('.qq')).length:null);
      T('U-4 근거 줄은 줄마다 90자까지',
        !!row&&String(row.querySelector('.gl').textContent||'').split('\n').every(x=>x.length<=90));
      /* 이미 연결한 줄엔 쓰임 수를 안 그린다(민법 3461 과 같다) */
      T('U-4 이미 넣은 줄엔 쓰임 수를 안 그린다',!!row&&!row.querySelector('.gguse'));
      $('#card [data-ggfind]').click(); await wait(200);
      /* 숫자 누름 → 창 */
      const inkWas=$('#card').classList.contains('penon');
      const panWas=$('#card .ggpan')?$('#card .ggpan').className:'';
      chip.click(); await wait(600);
      const w=document.getElementById('gguw');
      T('U-2 ★숫자를 누르면 쓰임 목록 창이 뜬다',!!w&&!!w.querySelector('.panel'));
      T('U-2 제목 수 = 4',!!w&&txt(w.querySelector('.bplh span')).indexOf('쓰는 문항 4')>=0,
        w?txt(w.querySelector('.bplh')):null);
      T('U-2 줄 수 = 4',w&&w.querySelectorAll('#gguwBody .gguR').length===4,
        w?w.querySelectorAll('#gguwBody .gguR').length:null);
      T('U-2 머리 상자에 그 문항의 근거 전부(댓글 포함)',
        !!w&&txt(w.querySelector('.gguh .gg')).indexOf('쓰임 시험 근거')>=0
        &&txt(w.querySelector('.gguh .gg')).indexOf('댓글 하나')>=0,
        w?txt(w.querySelector('.gguh .gg')).slice(0,90):null);
      T('U-2 ★줄 차례 = 목록 차례(단원순)',(()=>{
        const got=[...w.querySelectorAll('#gguwBody .gguR .cd')].map(x=>txt(x));
        const want=ggUseSort(ggOwners(T0)).map(u=>codeShow(rowByUid(u)));
        return got.join(',')===want.join(',')})(),
        [...w.querySelectorAll('#gguwBody .gguR .cd')].map(x=>txt(x)));
      T('U-2 ★숫자를 눌러도 밑의 칩은 안 열렸다(상자 무변)',
        ($('#card .ggrefbox')?$('#card .ggrefbox').classList.contains('hide'):true),
        $('#card .ggrefbox')?$('#card .ggrefbox').className:'(없음)');
      /* 지금 보는 문항 줄 */
      const meRow=w.querySelector('#gguwBody .gguR.me');
      T('U-3 ★지금 보는 문항 줄이 노랑 + 딱지',
        !!meRow&&txt(meRow).indexOf('지금 보는 문항')>=0
        &&getComputedStyle(meRow).backgroundColor===asCol('#FFFBEA'),
        meRow?[meRow.className,getComputedStyle(meRow).backgroundColor]:null);
      T('U-3 그 줄은 「× 연결 끊기」 · 다른 줄은 「↪ 그 문제 보기」',
        !!meRow&&!!meRow.querySelector('[data-gguux]')&&!meRow.querySelector('[data-gguugo]')
        &&w.querySelectorAll('#gguwBody [data-gguugo]').length===3,
        [meRow?!!meRow.querySelector('[data-gguux]'):null,
         w.querySelectorAll('#gguwBody [data-gguugo]').length]);
      /* 끌기·크기·기억 */
      {const p=w.querySelector('.panel'), q0=p.getBoundingClientRect();
       await drag(w.querySelector('.bplh'),q0.left+120,q0.top+8,q0.left+70,q0.top+58,'mouse'); await wait(250);
       const q1=p.getBoundingClientRect();
       T('U-5 창 머리줄을 끌면 움직인다',Math.abs(q1.left-(q0.left-50))<3&&Math.abs(q1.top-(q0.top+50))<3,
         [q0.left,q1.left]);
       const g=w.querySelector('.twgrip'), gr=g.getBoundingClientRect();
       await drag(g,gr.left+4,gr.top+4,gr.left+84,gr.top+54,'mouse'); await wait(260);
       T('U-5 모서리를 끌면 커진다',Math.abs(p.getBoundingClientRect().width-(q1.width+80))<3,
         [q1.width,p.getBoundingClientRect().width]);
       T('U-5 크기를 기기 값에 적는다',!!JSON.parse(localStorage.getItem('jagwa.win.gguse')||'null'));}
      /* 연결 끊기 */
      {const n0=ggRefOf(A).length;
       meRow.querySelector('[data-gguux]').click();
       await until(()=>ggRefOf(A).length===n0-1,5000); await wait(500);
       T('U-3 ★× 연결 끊기 → ggref −1',ggRefOf(A).length===n0-1,[n0,ggRefOf(A).length]);
       const w2=document.getElementById('gguw');
       T('U-3 ★창의 수가 3 으로 준다',!!w2&&w2.querySelectorAll('#gguwBody .gguR').length===3,
         w2?w2.querySelectorAll('#gguwBody .gguR').length:null);
       T('U-3 ★문항 창의 연결 칩이 사라진다',!$('#card .ggref'),
         $('#card .ggref')?$('#card .ggref').outerHTML.slice(0,80):null);
       T('U-3 라벨 수도 갱신된다(3)',
         (()=>{const l=$('#card .ggline .lb .gguse');return !l})()||
         txt($('#card .ggline .lb .gguse'))==='↩0',
         $('#card .ggline .lb .gguse')?txt($('#card .ggline .lb .gguse')):'(없음)');
       const wx=document.getElementById('gguw');if(wx)wx.remove();}
      closeView(); await wait(250);}
     /* 위 검색 줄 결과도 같은 꼴 + 노란 표시 */
     {mk(4); await saveGGREF(); await saveGG();
      ggSearchMode('g'); const qi=$('#q'); qi.value='쓰임'; ggResBox('쓰임'); await wait(400);
      const row=document.querySelector('#esres .ggres');
      T('U-4 ★위 검색 줄 결과도 세 줄 꼴',
        !!row&&row.classList.contains('g3')&&!!row.querySelector('.hd')&&!!row.querySelector('.qq')
        &&!!row.querySelector('.gl'),row?row.className:null);
      T('U-4 ★거기엔 노란 찾은 글자 표시가 산다',!!row&&!!row.querySelector('mark'),
        row?row.innerHTML.slice(0,140):null);
      T('U-4 위 검색 줄 결과 줄에도 쓰임 수',!!row&&!!row.querySelector('.gguse')
        &&txt(row.querySelector('.gguse'))==='↩4',row?txt(row.querySelector('.gguse')):null);
      qi.value=''; ggSearchMode('q'); await wait(250);}
     T('U-6 찾기 칸은 120ms 모았다 한 번 돌린다',typeof ggFindSoon==='function'
       &&String(ggFindSoon).indexOf('120')>=0);
     GG={};GGREF={};await saveGG();await saveGGREF();draw();await wait(250);
   });

   /* ══════════ S — add3 §D 근거 통 가드(재현) ══════════
      ⚠ 지시서는 묶음 이름을 「G」라 했지만 add1 근거 묶음이 이미 `G-1`~`G-6` 을 쓴다.
        이름이 겹치면 헛잣대 거르개가 섞이므로 **「S」(동기화 가드)** 로 갈아 붙였다(보고에 적었다). */
   await grp('S', async()=>{
     const ls=k=>{try{return JSON.parse(localStorage.getItem(k)||'{}')}catch(e){return {}}};
     const UID='G24-61-07';
     const one=[{k:'g_t',i:1,t:'시험 근거',ok:'O',ts:1,cs:[]}];
     const clean=()=>{['u','gone','shadow'].forEach(x=>{});
       const sh=ls(SHADOW_KEY);delete sh.gg;lsPut(SHADOW_KEY,sh);
       const g=ls(GONE_KEY);delete g['gg|'+UID];lsPut(GONE_KEY,g);
       const u=ls(U_KEY);delete u['gg|'+UID];lsPut(U_KEY,u)};
     clean();
     /* ── 흉내: 그림자에는 근거 한 칸, 통은 아직 안 읽혔다 ── */
     GG={}; GG_READY=false;
     {const sh=ls(SHADOW_KEY);sh.gg={};sh.gg[UID]=one;lsPut(SHADOW_KEY,sh)}
     T('S-0 통이 아직 안 읽힌 상태다',GG_READY===false&&SYNC_REF.gg.g()===null,
       [GG_READY,SYNC_REF.gg.g()]);
     stampAll();
     T('S-1 ★안 읽힌 통에는 **묘비를 안 찍는다**',!ls(GONE_KEY)['gg|'+UID],ls(GONE_KEY)['gg|'+UID]);
     T('S-1 그림자도 그대로 남는다',!!(ls(SHADOW_KEY).gg||{})[UID]);
     /* ── 밀 때 원격 것 그대로 ── */
     {const remote={data:{gg:{}},u:{},gone:{}}; remote.data.gg[UID]=one;
      const pay=recPayload(remote);
      T('S-2 ★안 읽힌 통은 **원격 것 그대로** 실어 보낸다(빈 객체로 안 지운다)',
        !!(pay.data.gg||{})[UID],Object.keys(pay.data.gg||{}));}
     /* ── 병합에서도 안 건드린다 ── */
     {const before=JSON.stringify(GG);
      const remote={data:{gg:{}},u:{},gone:{}}; remote.data.gg[UID]=one; remote.u['gg|'+UID]=Date.now();
      await recMerge(remote);
      T('S-3 ★안 읽힌 통은 병합에서도 안 건드린다',JSON.stringify(GG)===before,
        [before.slice(0,40),JSON.stringify(GG).slice(0,40)]);}
     /* ── 읽은 뒤에는 여느 통과 같다 ── */
     GG={}; GG[UID]=one; GG_READY=true;
     T('S-4 읽은 뒤에는 g() 가 값을 낸다',SYNC_REF.gg.g()!==null);
     stampAll();
     T('S-4 ★칸이 그대로면 묘비가 안 찍힌다',!ls(GONE_KEY)['gg|'+UID]);
     GG={}; stampAll();
     T('S-5 ★진짜로 지우면 묘비는 그대로 찍힌다(가드가 지우기를 막지 않는다)',
       !!ls(GONE_KEY)['gg|'+UID],ls(GONE_KEY)['gg|'+UID]);
     clean();
     /* ── 되살림 한 벌 ── */
     {GG={};GG_READY=true;await saveGG();
      try{localStorage.removeItem(GGFIX_K)}catch(e){}
      const n1=await ggFixEat(); await wait(350);
      T('S-6 ★되살림이 근거를 보탠다',n1===1&&ggOf(UID).length===1,[n1,ggOf(UID).length]);
      T('S-6 ★글자가 깃 이력 그대로다',
        String((ggOf(UID)[0]||{}).t).indexOf('아래부터 대성중열')===0
        &&(ggOf(UID)[0]||{}).k==='g_mu9suur9_18aq'&&(ggOf(UID)[0]||{}).ts===1789907744565,
        [(ggOf(UID)[0]||{}).k,String((ggOf(UID)[0]||{}).t).slice(0,14)]);
      try{localStorage.removeItem(GGFIX_K)}catch(e){}
      const n2=await ggFixEat(); await wait(250);
      T('S-6 ★같은 `k` 는 두 번 안 보탠다(멱등)',n2===0&&ggOf(UID).length===1,[n2,ggOf(UID).length]);
      T('S-6 한 번 먹으면 기기에 표시가 남는다',!!localStorage.getItem(GGFIX_K));
      /* 사용자가 그 사이 고친 칸은 안 덮는다 */
      GG={};GG[UID]=[{k:'g_mu9suur9_18aq',i:1,t:'내가 고친 글',ok:'X',ts:9,cs:[]}];await saveGG();
      try{localStorage.removeItem(GGFIX_K)}catch(e){}
      await ggFixEat(); await wait(250);
      T('S-6 ★사용자가 고친 칸은 안 덮는다',(ggOf(UID)[0]||{}).t==='내가 고친 글',
        (ggOf(UID)[0]||{}).t);
      GG={};await saveGG();clean();}
   });
   /* ══════════ L 학습로그 단추 ══════════ */
   await grp('L', async()=>{
     const btns=[...document.querySelectorAll('button')].filter(b=>txt(b)==='📝 학습로그');
     T('L 지학 — 「📝 학습로그」 단추 DOM 0',btns.length===0,btns.length);
     N('L 지학 — openPanel 은 IIFE 안(전역 아님)',typeof openPanel);
   });
   /* §E-1 지학 무변 — 고침 전 판과 **글자까지** 대 본다 */
   closeView(); await wait(300);
   FL.past='y';FL.q='';FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';
   /* ⚠ 앞 묶음들이 남긴 **시험 자국**을 걷고 나서 대 본다 — 글자 고치기(tfix)·보기 O/X(bogi)는
      시험이 넣었다 되돌린 것이라 판마다 찌꺼기가 남을 수 있다. 두 판 다 이 줄을 지나므로 공평하다. */
   GG={};GGREF={};PICK={};await saveGG();await saveGGREF();
   TFIX={};await put('kv','tfix',TFIX);
   BG={};await put('kv','bogi',BG);
   _coll=null; lvApply('all',false); ordSet('unit'); draw(); await wait(1200);


   /* ══════════ W-1 — add9 §A 첫 화면 상주 서랍(세 과목 공통) ══════════ */
   await grp('WD', async()=>{
     FL.past='';FL.year='';FL.lv='';FL.star=false;FL.mark='';FL.bigs=[];FL.subs=[];FL.q='';
     draw(); await wait(600);
     T('WD-1 ★「목차」 단추(#btnTree)가 없다',!document.getElementById('btnTree'),
       !!document.getElementById('btnTree'));
     const dr=document.getElementById('navdr');
     T('WD-1 ★서랍이 첫 화면에 늘 서 있다',
       !!dr&&!dr.classList.contains('hide')&&dr.getBoundingClientRect().width>0,
       dr?[dr.className,Math.round(dr.getBoundingClientRect().width)]:'없음');
     T('WD-1 ★서랍이 `#view` 밖으로 나왔다(창 안에 안 남는다 · §B)',
       !!dr&&!document.querySelector('#view #navdr')&&!document.querySelector('#view #navTg'),
       [!!document.querySelector('#view #navdr'),!!document.querySelector('#view #navTg')]);
     { const lib=document.getElementById('lib');
       const a=dr?dr.getBoundingClientRect():null, b=lib?lib.getBoundingClientRect():null;
       T('WD-1 ★본문과 안 겹친다(서랍 오른끝 ≤ 본문 왼끝)',
         !!a&&!!b&&a.right<=b.left+1,[a?Math.round(a.right):'-',b?Math.round(b.left):'-']); }
     { const l=document.getElementById('ndList');
       const nos=(typeof navList==='function')?navList():[];
       let ok2=0; nos.forEach(n=>{if(rec(n))ok2++});
       try{navBuild()}catch(e){}
       N('진단 navBuild 속',{nos:nos.length,rec성공:ok2,
         ndList부모:l?(l.parentNode?(l.parentNode.id||l.parentNode.className||l.parentNode.tagName):'없음'):'#ndList 없음',
         ndList아이:l?l.childNodes.length:'-',
         navdr부모:(()=>{const d=document.getElementById('navdr');
           return d&&d.parentNode?(d.parentNode.id||d.parentNode.tagName):'-'})(),
         같은l:l===document.getElementById('ndList')}); }
     const nRow=()=>document.querySelectorAll('#ndList .ndrow').length;
     const nSec=()=>document.querySelectorAll('#ndList .ndsec').length;
     T('WD-1 ★서랍 줄 수 = 첫 화면 목록 문항 수',nRow()===filtered().length,[nRow(),filtered().length]);
     T('WD-1 단원 머리 줄이 있다(옛 「목차」 구실)',nSec()>0,nSec());
     T('WD-1 단원 머리 줄에 마지막 마크 점·문항 수가 있다',
       (()=>{const h=document.querySelector('#ndList .ndsec');
         return !!h&&!!h.querySelector('.dot')&&!!h.querySelector('.n')})(),
       (()=>{const h=document.querySelector('#ndList .ndsec');return h?txt(h).slice(0,24):'없음'})());
     /* 편 칩·검색을 바꾸면 같이 바뀐다 */
     { const before=nRow();
       const big=$$$('#eChs .chchip')[1]; if(big){big.click(); await wait(600);}
       T('WD-1 ★편 칩을 바꾸면 서랍도 같이 좁아진다',nRow()===filtered().length&&nRow()<before,
         [before,nRow(),filtered().length]);
       $$$('#eChs .chchip')[0].click(); await wait(500); }
     { const q=document.getElementById('q');
       if(q){ q.value='운동'; q.dispatchEvent(new Event('input',{bubbles:true})); await wait(700);
         T('WD-1 ★검색을 걸면 서랍도 같이 좁아진다',nRow()===filtered().length,[nRow(),filtered().length]);
         q.value=''; q.dispatchEvent(new Event('input',{bubbles:true})); await wait(600); }
       else T('WD-1 ★검색을 걸면 서랍도 같이 좁아진다',false,'#q 없음'); }
     T('WD-1 서랍 줄 글자 = 코드+난이도-제목',
       (()=>{const r0=document.querySelector('#ndList .ndrow');if(!r0)return false;
         const t2=txt(r0.querySelector('.ndt'));return t2.length>0&&t2.indexOf('undefined')<0})(),
       (()=>{const r0=document.querySelector('#ndList .ndrow');
         return r0?txt(r0.querySelector('.ndt')).slice(0,30):'없음'})());
     /* §A-6 옛 목차 서랍은 안 뜬다 */
     T('WD-1 ★옛 목차 서랍(#tree)이 안 뜬다',
       (()=>{try{treeOpen()}catch(e){}const t=document.getElementById('tree');
         return !t||t.classList.contains('hide')})(),'');
     T('WD-1 #trTog 가 상주 서랍 머리로 갔다(카드 층) · 물리는 숨음',
       (()=>{const t=document.getElementById('trTog');
         if(!t)return true;
         return !!t.closest('#navdr')||getComputedStyle(t).display==='none'})(),
       (()=>{const t=document.getElementById('trTog');
         return t?[!!t.closest('#navdr'),getComputedStyle(t).display]:'없음'})());
     /* §D-6 좁은 화면 규칙(소스·CSS 로 잰다 — 하네스 창은 1500px 이다) */
     T('WD-1 좁은 화면은 접힌 채 시작한다(규칙)',
       String(ndResident).indexOf('window.innerWidth<900')>=0,'');
   });

   /* ★ 9/28 penfinger_add2 회귀 — E-1 도 X-11 처럼 시험지 받기·기록 동기화가 끝난 뒤 찍는다(한 판만 동기화가 끝나
      「6회독↔5회독」「안 품 286·맞음 27 ↔ 안 품 318·맞음 1」이 갈렸다 — 같은 판을 다시 돌리면 PASS · 판 탓 아님) */
   await until(()=>{const b=document.getElementById('dl');return !b||b.classList.contains('hide')||!/받는 중/.test(b.textContent||'')},60000);
   await until(()=>typeof recBusy==='undefined'||!recBusy,60000);
   try{if(typeof syncRecords==='function')await Promise.race([syncRecords(true),wait(60000)])}catch(e){}
   await until(()=>typeof recBusy==='undefined'||!recBusy,60000);
   draw(); await wait(600);
   snap.cnt=String($('#cnt').textContent||'');
   snap.list=$$$('#list .item').slice(0,25).map(el=>String(el.textContent||'').replace(/\s+/g,' ').trim()).join(' || ');
   snap.hd=$$$('#list .grouphd').slice(0,8).map(el=>String(el.textContent||'').replace(/\s+/g,' ').trim()).join(' || ');
   snap.spec=$$$('#spec i').length+'/'+$$$('#spec i.gap').length;
   /* ⚠ 동기화 칩(`#recChip`)은 「● 대기 N건」·「○ 동기화 실패」처럼 **살아 움직이는 값**이다.
      껍데기 글 대조에서 통째로 뺀다 — 판이 달라진 것이 아니라 그때그때 다르다. */
   snap.esh=(()=>{const e=document.getElementById('esh'); if(!e)return '';
     const c=e.cloneNode(true); const rc=c.querySelector('#recChip'); if(rc)rc.remove();
     return String(c.textContent||'').replace(/\s+/g,' ').trim()})();
   /* ★ A-6(a) 9/30 둘째 바퀴 — jagwa_uid(genie 5e18424 · 결정로그 9/29 15:09 · _task_jagwa_uid.md 235줄 「남은 차이(모두 뜻한 차이) … 바탕 쪽(옛 앱 + 새 데이터)이 기록을 못 봄」)와 같은 까닭:
      사용자 글자 고침(tfix q · 옛 열쇠 G59-08)은 새 앱만 jgMigrate 로 옮겨 목록 줄에 보이고 바탕 앱(ab49775)은 못 본다(원본 글) —
      목록 줄의 고친 글(.prev.fx)은 원본 글(txtOrig)로 되돌려 다시 찍는다(바탕엔 .fx 가 없어 그대로 · 나머지 글자는 그대로 맞댄다) */
   snap.list=$$$('#list .item').slice(0,25).map(el=>{const c=el.cloneNode(true),p=c.querySelector('.prev.fx');
     if(p&&el.dataset.uid&&typeof txtOrig==='function')p.textContent=txtOrig(el.dataset.uid,'q');
     return String(c.textContent||'').replace(/\s+/g,' ').trim()}).join(' || ');
   await openView(rowByUid('G25-62-09')[F.NO]); await wait(1000);
   snap.view=$('#view').className;
   snap.vtop=String((($('#view .vtop')||{}).textContent)||'').replace(/\s+/g,' ').trim();
   snap.vbot=String((($('.vbot')||{}).textContent)||'').replace(/\s+/g,' ').trim();
   /* ★ A-6(a) 9/30 둘째 바퀴 — 같은 까닭: 사용자 조각(crop · 옛 열쇠 G62-09 · 문제 칸 1)을 밑준비가 kv 에 싣고 새 앱만 jgMigrate('boot') 로 옮겨 본다 —
      문제 글 뒤 조각 떼기 ✕ 가 새 ✕✕(사용자 1 + P-4 1) / 바탕 ✕(P-4 1) 로 갈린다 → 조각 상자(.cropw)는 빼고 찍는다(나머지 글자는 그대로) */
   snap.card=String(((c=>{if(!c)return {};const k=c.cloneNode(true);k.querySelectorAll('.cropw').forEach(x=>x.remove());return k})($('#card')).textContent)||'').replace(/\s+/g,' ').trim().slice(0,600);
   closeView(); await wait(250);
   try{await __nativeFetch('/snap',{method:'POST',body:JSON.stringify(snap)})}catch(e){}

   /* 스냅샷 뒤로 옮겼다 — NEW 쪽만 회독이 늘어 거짓 회귀가 나던 자리(2026-09-21) */
   /* ══════════ SQ (add19) — 서랍·▶ 넘기기 차례 = 첫 화면 차례 ══════════ */
   await grp('SQ', async()=>{
     closeView(); await wait(300);
     try{collSet().clear();collSave()}catch(e){}
     FL.bigs=[];FL.subs=[];FL.unit='';FL.round='';FL.mark='';FL.q='';
     draw(); await wait(1000);
     try{navBuild()}catch(e){}
     await wait(400);
     const codes=()=>$$$('#list .item').map(el=>txt(el.querySelector('.num')));
     const drow=()=>$$$('#ndList .ndrow').map(el=>{const r=rec(+el.dataset.no);return r?codeShow(r):'?'});
     const first=codes(), drw=drow();
     /* B-1 — 서랍 코드 열 = 첫 화면(전부 펼친) 코드 열 */
     T('SQ 지학 ★서랍 코드 열 = 첫 화면 코드 열(전수 '+first.length+'/'+drw.length+')',
       first.length>200&&first.join('|')===drw.join('|'),
       {n:[first.length,drw.length],
        앞:[first.slice(0,4),drw.slice(0,4)],
        diff:first.map((x,i)=>[i,x,drw[i]]).filter(a=>a[1]!==a[2]).slice(0,4)});
     /* B-5 헛잣대 — **옛 차례**(`filtered()` 그대로 = add19 앞의 서랍)는 첫 화면과 다르다 */
     const old=filtered().map(r=>codeShow(r));
     T('SQ 지학 ★헛잣대 — 옛 차례(filtered() 그대로 · add19 앞의 서랍)는 첫 화면과 **다르다**',
       old.length===first.length&&old.join('|')!==first.join('|'),
       {n:[old.length,first.length],옛앞:old.slice(0,4),새앞:first.slice(0,4)});
     /* B-2 — 소단원 머리 수·합 · 0문항 머리 */
     const hdF=$$$('#list .grouphd[data-uhd]'), hdD=$$$('#ndList .ndsec');
     T('SQ 지학 ★서랍 소단원 머리 수 = 첫 화면 소단원 머리 수('+hdF.length+'/'+hdD.length+' · 문항 '+first.length+'개가 아니다)',
       hdF.length>0&&hdF.length===hdD.length&&hdD.length<first.length,
       [hdF.length,hdD.length,first.length]);
     const sum=$$$('#ndList .ndsec .n').reduce((a,x)=>a+(+txt(x)||0),0);
     T('SQ 지학 ★서랍 머리의 수 합 = 문항 수('+sum+'/'+first.length+')',sum===first.length,[sum,first.length]);
     const zero=$$$('#ndList .ndsec.nd0');
     T('SQ 지학 ★문항 0인 단원 머리도 선다(흐리게 '+zero.length+'개 · 0이 아니다)',
       zero.length>0&&zero.every(h=>txt(h.querySelector('.n'))==='0'&&+getComputedStyle(h).opacity<1),
       [zero.length,zero.slice(0,2).map(h=>[txt(h),getComputedStyle(h).opacity])]);
     {const z=zero[0];
      if(z){const u=z.dataset.sec;
        const fh=$$$('#list .grouphd[data-uhd]').find(h=>h.dataset.uhd===u);
        T('SQ 지학 0문항 머리 글자 = 첫 화면 그 머리와 같다('+txt(z).replace(/^▾\s*/,'').slice(0,26)+')',   /* ★ 2026-10-07 (_task_jagwa_phys_win §A-07 ③) — 서랍 단원 머리 앞 ▾(접기) = 뜻한 차 → 항목 이름이 안 갈리게 이름 글자에서만 뗀다(잣대는 .nm 그대로) · 옛: txt(z).slice(0,26) */
          !!fh&&txt(fh).indexOf(txt(z.querySelector('.nm')))>=0,[txt(z),fh?txt(fh):'첫 화면에 없음'])}}
     /* B-2 뒤 — 거르개를 켜면 첫 화면과 같이 사라진다 */
     {const n0=$$$('#ndList .ndsec.nd0').length;
      FL.mark='X'; draw(); await wait(900); try{navBuild()}catch(e){} await wait(300);
      const n1=$$$('#ndList .ndsec.nd0').length, f1=$$$('#list .grouphd[data-uhd]').length, d1=$$$('#ndList .ndsec').length;
      T('SQ 지학 ★거르개를 켜면 0문항 머리가 첫 화면과 같이 사라진다('+n0+'→'+n1+') · 머리 수도 같다('+f1+'/'+d1+')',
        n0>0&&n1===0&&f1===d1,[n0,n1,f1,d1]);
      FL.mark=''; draw(); await wait(900); try{navBuild()}catch(e){} await wait(300)}
     /* B-4 — 첫 화면에서 접어도 서랍은 무변 */
     {const d0=$$$('#ndList .ndrow').length;
      const k=($$$('#list .grouphd.sec')[0]||{}).dataset;
      if(k&&k.coll){collToggle(k.coll); await wait(900); try{navBuild()}catch(e){} await wait(300);
        const d1=$$$('#ndList .ndrow').length, f1=$$$('#list .item').length;
        T('SQ 지학 ★첫 화면에서 「'+k.coll+'」 묶음을 접어도 서랍 줄 수 무변('+d0+'→'+d1+' · 첫 화면은 '+first.length+'→'+f1+')',
          d1===d0&&f1<first.length,[d0,d1,first.length,f1]);
        collToggle(k.coll); await wait(900); try{navBuild()}catch(e){} await wait(300)}
      else T('SQ 지학 접을 절 머리를 찾았다',false,'#list .grouphd.sec 0건')}
     /* B-3 — ▶ 다섯 번 = 서랍의 다음 다섯 줄 */
     {const rows=$$$('#ndList .ndrow').map(el=>+el.dataset.no);
      const i0=12;
      await openView(rows[i0]); await wait(1100);
      const seen=[];
      for(let k=1;k<=5;k++){go(1); await wait(900); seen.push(VNO)}
      T('SQ 지학 ★▶ 다섯 번 = 서랍의 다음 다섯 줄',
        seen.join(',')===rows.slice(i0+1,i0+6).join(','),[seen,rows.slice(i0+1,i0+6)]);
      let syncExc='';
      const hd0=txt(document.getElementById('ndHead'));
      try{navSync()}catch(e){syncExc=String(e&&e.message||e)}
      const hd1=txt(document.getElementById('ndHead'));
      const cur0=$$$('#ndList .ndrow.cur').length;
      await wait(400);
      const hd2=txt(document.getElementById('ndHead'));
      N('SQ navSync 직후',{앞머리:hd0,바로뒤머리:hd1,바로뒤강조:cur0,
        '400ms뒤머리':hd2,'400ms뒤강조':$$$('#ndList .ndrow.cur').length,예외:syncExc,
        navSync몸:String(navSync).replace(/\s+/g,' ').slice(0,70)});
      if(!$$$('#ndList .ndrow.cur').length){try{navSync()}catch(e){}}   /* 다시 그려졌으면 한 번 더 */
      const cur=$$$('#ndList .ndrow.cur').map(el=>+el.dataset.no);
      T('SQ 지학 서랍 강조가 그 줄에 내려와 있다',cur.length===1&&cur[0]===VNO,
        {cur:cur,VNO:VNO,줄:$$$('#ndList .ndrow').length,
         그줄있나:!!document.querySelector('#ndList .ndrow[data-no="'+VNO+'"]'),
         VLIST안:(typeof VLIST!=='undefined'&&VLIST)?VLIST.indexOf(VNO):'-',
         머리:txt(document.getElementById('ndHead'))});
      closeView(); await wait(400)}
     /* B-4 뒤 — 편 칩·검색으로 좁히면 서랍·첫 화면 같은 수 */
     {FL.q='지구'; draw(); await wait(900); try{navBuild()}catch(e){} await wait(300);
      const f=$$$('#list .item').length, d=$$$('#ndList .ndrow').length;
      T('SQ 지학 ★검색으로 좁히면 서랍·첫 화면 같은 수('+f+'/'+d+')',f>0&&f===d,[f,d]);
      FL.q=''; draw(); await wait(900); try{navBuild()}catch(e){} await wait(300)}
   });


"""

BODY_BIO = r"""
   await (async()=>{for(let __i=0;__i<300&&(typeof db==='undefined'||!db);__i++)await new Promise(r=>setTimeout(r,100));return loadEarthData()})()/* ★ 2026-10-08 (_task_jagwa_phys_win 회귀) db 가 설 때까지 — 고정 대기 경합(짐 크면 「db 없음」) · 판정 무변 */;
   await until(()=>DATA.length>600,30000);
   ['jagwa.earth.order','jagwa.earth.coll','jagwa.earth.hmfold','jagwa.view.win',
    'jagwa.win.view','jagwa.win.book','jagwa.win.mc','jagwa.win.jn']
     .forEach(k=>{try{localStorage.removeItem(k)}catch(e){}});
   _coll=null;
   FL.past='y';FL.q='';FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';
   if(CUR.KINDS)FL.types=new Set(['G']);
   GG={};GGREF={};PICK={};
   draw(); await wait(450);
   /* ⚠ 본판(add3)에는 이 판의 새 문이 없다 — 여기서 죽으면 **묶음별 헛잣대**가 안 나온다.
        없는 이름은 null 로 적고 묶음까지 가게 둔다. */
   N('생물 밑준비',{subj:SUBJ_ID,DATA:DATA.length,
     SHELL:(typeof SHELL==='undefined'?null:SHELL),
     HASBOOK:(typeof HASBOOK==='undefined'?null:HASBOOK),
     HASROUND:(typeof HASROUND==='undefined'?null:HASROUND()),
     HASJOGAK:(typeof HASJOGAK==='undefined'?null:HASJOGAK),
     층:(typeof lvDeep==='undefined'?null:(lvDeep()?3:2)),
     장:Object.keys(TOC.ch).length,절:Object.keys(TOC.sec).length});

   /* ══════════ B-1 껍데기 ══════════ */
   await grp('B', async()=>{
     const esh=document.getElementById('esh');
     T('B-1 ★생물에도 껍데기가 섰다',!!esh);
     T('B-1 제목이 과목 이름을 단다',txt(esh.querySelector('h1'))==='📖 자과 서재 · 생물',
       txt(esh.querySelector('h1')));
     T('B-1 옛 머리·개수 줄은 안 보인다',
       getComputedStyle($('#lib>.top')).display==='none'&&getComputedStyle($('#lib>.count')).display==='none');
     /* 머리 칩 치수 = 지학과 같은 px(fig_bogi §C 값) */
     const ec=document.getElementById('examChip'), rc=document.getElementById('recChip');
     T('B-1 ★D-날 칩 11px · 800',!!ec&&getComputedStyle(ec).fontSize==='11px'&&getComputedStyle(ec).fontWeight==='800',
       ec?[getComputedStyle(ec).fontSize,getComputedStyle(ec).fontWeight]:null);
     T('B-1 ★동기화 칩 11px · 테두리 0',!!rc&&getComputedStyle(rc).fontSize==='11px'
       &&getComputedStyle(rc).borderTopWidth==='0px',
       rc?[getComputedStyle(rc).fontSize,getComputedStyle(rc).borderTopWidth]:null);
     T('B-1 머리 개수가 과목 갈래대로다(기출·타기출·예상)',
       /기출 \d+ · 타기출 \d+ · 예상 \d+/.test(txt(document.getElementById('eCnts'))),
       txt(document.getElementById('eCnts')));
     /* 히트맵 칸 수 = 그 갈래 문항 수 */
     T('B-1 ★히트맵 칸 수 = 보는 갈래의 문항 수',
       $$$('#spec i').length===DATA.filter(showKind).length,
       [$$$('#spec i').length,DATA.filter(showKind).length]);
     T('B-1 히트맵에 빈 칸이 없다',$$$('#spec i.gap').length===0,$$$('#spec i.gap').length);
     /* 두 층 — 절 머리가 곧 단원 머리 */
     T('B-1 ★생물은 두 층이다(절 코드 = 단원 코드)',lvDeep()===false,lvDeep());
     const hds=$$$('#list .grouphd');
     T('B-1 ★같은 이름의 머리가 두 번 안 찍힌다',
       hds.filter(h=>h.classList.contains('u')).length===0,
       hds.filter(h=>h.classList.contains('u')).length);
     /* 접기 단추 순환 = 층 수(장 → 절 → 문제) */
     const lv=document.getElementById('lvBtn');
     T('B-1 접기 단추가 있다',!!lv);
     const seq=[];
     for(let i=0;i<4;i++){seq.push(txt(lv));lv.click();await wait(300)}
     T('B-1 ★순환 걸음 = 세 걸음(장·단원·문제)',
       new Set(seq).size===3,seq);
     /* 접은 채 머리 통계 = 편 채와 같음 */
     lvApply('all',false);draw();await wait(300);
     const openN=$$$('#list .grouphd.ch').map(h=>txt(h)).join('|');
     lvApply('ch',false);draw();await wait(300);
     T('B-1 ★접은 채 머리 통계가 편 채와 같다',
       $$$('#list .grouphd.ch').map(h=>txt(h)).join('|')===openN,
       [$$$('#list .grouphd.ch').map(h=>txt(h)).slice(0,2),openN.slice(0,80)]);
     lvApply('all',false);draw();await wait(300);
     /* 🃏 · 📋 창 */
     const mc=document.querySelector('#list .grouphd [data-mc]');
     T('B-1 단원 머리에 🃏 칩',!!mc);
     if(mc){mc.click();await wait(700);
       T('B-1 🃏 창이 뜬다',!!document.getElementById('mcw'));
       const x=document.getElementById('mcwX');if(x)x.click();await wait(200)}
     const jn=document.querySelector('#list .grouphd [data-jn]');
     T('B-1 단원 머리에 📋 칩',!!jn);
     if(jn){jn.click();await wait(800);
       T('B-1 📋 정리 창이 뜬다',!!document.getElementById('jnw'));
       const x=document.getElementById('jnwX');if(x)x.click();await wait(200)}
   });

   /* ══════════ B-2 문항 창 ══════════ */
   await grp('B', async()=>{
     const r0=DATA.filter(r=>kindOf(r)==='G')[0];
     await openView(r0[F.NO]); await wait(1000);
     T('B-2 ★생물 문항이 떠 있는 창으로 열린다',
       $('#view').classList.contains('win')&&!!document.getElementById('vWinTg'),
       $('#view').className);
     const pill=document.getElementById('inkPill');
     T('B-2 ★#inkPill 이 .vtop 안이다',!!pill&&!!pill.closest('#view .vtop'));
     T('B-2 ★생물 알약 단추 아홉(글상자까지)',
       pill&&pill.querySelectorAll('button').length===9,
       pill?[...pill.querySelectorAll('button')].map(b=>b.id||b.dataset.pen||b.dataset.hl):null);
     T('B-2 알약 높이 ≤ 26px',pill.getBoundingClientRect().height<=26,pill.getBoundingClientRect().height);
     /* 아랫줄 다섯 */
     const vis=[...document.querySelectorAll('.vbot .tools>*')].filter(el=>el.offsetParent!==null);
     /* ★ _task_jagwa_claude_slot_add1 §A-2 (2026-09-22) — 생물도 맨 오른쪽에 #tGpt 가 선다 */
     /* ★ 2026-10-07 (_task_jagwa_phys_win §A-04 ⑪ · ⑥) — 세 과목 #tLayer·#tLayerAdd·#tLayerEye 숨김 = 뜻한 차 → 새 꼴 기록 · 🃏 · Claude 도 받는다 · 옛: vis.map(el=>el.id).join(',')==='tLayer,tLayerAdd,tLayerEye,tHist,tCard,tGpt' */
     T('B-2 ★아랫줄에 보이는 것 여섯(다섯 + 맨 오른쪽 Claude)',
       ['tLayer,tLayerAdd,tLayerEye,tHist,tCard,tGpt','tHist,tCard,tGpt'].indexOf(vis.map(el=>el.id).join(','))>=0,vis.map(el=>el.id));
     T('B-2 #tW 안 보임 · 값 2',$('#tW').offsetParent===null&&$('#tW').value==='2');
     /* P 넷째 */
     const boxes=$$$('#card .vox');
     T('B-2 ★근거 아랫줄 단추 넷 · 넷째가 P',boxes.length===4&&boxes[3].classList.contains('vP'),
       boxes.map(b=>b.className));
     const no=r0[F.NO], h0=hist(no).length;
     boxes[3].click(); await wait(600);
     T('B-2 ★P 를 누르면 기록 마지막이 P',lastM(no)==='P'&&hist(no).length===h0+1,[lastM(no)]);
     /* 빨강 펜 한 획 */
     const uid=GGU(r0);
     await del('ink','qink:'+uid); await qLoad(uid); await wait(200);
     pill.querySelector('[data-pen="#B03A2E"]').click(); await wait(150); qWire(); await wait(80);
     {const sv=$('#card #qink'), rr=sv.getBoundingClientRect();
      const freeAt=(u,v)=>{const x=rr.left+u*rr.width,y=rr.top+v*rr.width;
        if(x<4||y<4||x>document.documentElement.clientWidth-4||y>document.documentElement.clientHeight-4)return false;
        try{return !underInk(x,y,sv)}catch(e){return false}};
      let pu=0,pv=0,found=false;
      for(let v=0.03;v<=0.40&&!found;v+=0.03)for(let u=0.03;u<=0.50&&!found;u+=0.03)
        if(freeAt(u,v)&&freeAt(u+0.14,v+0.05)&&freeAt(u+0.28,v+0.10)){pu=u;pv=v;found=true}
      T('B-2 획을 그을 빈 자리를 찾았다',found,[pu,pv]);
      const n0=((QINK.s)||[]).length;
      await draw1(sv,[rr.width*pu,rr.width*pv,rr.width*(pu+0.14),rr.width*(pv+0.05),
                      rr.width*(pu+0.28),rr.width*(pv+0.10)]);
      const st=((QINK.s)||[])[((QINK.s)||[]).length-1];
      T('B-2 ★빨강 펜 획이 #B03A2E 로 저장된다',
        ((QINK.s)||[]).length===n0+1&&!!st&&st.c==='#B03A2E',[st&&st.c]);
      setTool('view'); qWire(); await wait(100);
      await del('ink','qink:'+uid); await qLoad(uid); await wait(120);}
   });

   /* ══════════ B-3 근거 ══════════ */
   await grp('B', async()=>{
     const G=DATA.filter(r=>kindOf(r)==='G');
     const A=GGU(G[0]), U=GGU(G[1]);
     GG={};GGREF={};
     GG[U]=[{k:'g_b1',i:1,t:'ㄱ 생물 남의 근거',ok:'O',ts:1,cs:[{k:'c_b1',t:'댓글',ts:1}]}];
     GGREF[A]=[U];
     await saveGG(); await saveGGREF();
     await openView(G[0][F.NO]); await wait(900);
     T('B-3 ★생물 카드에 근거 줄이 있다',!!$('#card .ggbox'));
     T('B-3 SYNC 키 넷이 들어갔다(gg·ggref·pick·link)',
       ['gg','ggref','pick','link'].every(k=>SYNC_KEYS.indexOf(k)>=0),
       ['gg','ggref','pick','link'].filter(k=>SYNC_KEYS.indexOf(k)<0));
     /* 근거 더하기 */
     {const box=$('#card [data-ggrows]');
      box.querySelector('.txt').value='생물 첫 근거';
      await ggAdd(A,'qp-',false); await wait(500);
      T('B-3 ★근거가 더해진다',ggOf(A).length===1&&ggOf(A)[0].t==='생물 첫 근거',
        [ggOf(A).length,(ggOf(A)[0]||{}).t]);}
     /* 연결 상자 → ✎ 여기서 고치기 */
     const chip=$('#card [data-ggrt]');
     T('B-3 연결 칩이 있다',!!chip);
     chip.click(); await wait(350);
     const eb=$('#card .ggrefbox [data-ggre]');
     T('B-3 ★「✎ 여기서 고치기」가 있다',!!eb);
     eb.click(); await wait(300);
     const edb=$('#card [data-ggre-box]');
     edb.querySelector('.ggrow .txt').value='생물 고친 글';
     edb.querySelector('[data-ggedsave]').click();
     await until(()=>(ggOf(U)[0]||{}).t==='생물 고친 글',6000); await wait(350);
     const g=ggOf(U)[0];
     T('B-3 ★사본 없이 그 문항의 글만 바뀐다',
       !!g&&g.t==='생물 고친 글'&&g.k==='g_b1'&&g.i===1&&g.ok==='O'&&(g.cs||[]).length===1,
       g?[g.t,g.k,g.i,g.ok]:null);
     T('B-3 ★고친 상자는 펼친 채',(()=>{const b=$('#card .ggrefbox');return !!b&&!b.classList.contains('hide')})());
     /* 쓰임 수 */
     {const pool=DATA.filter(r=>kindOf(r)==='G').map(r=>GGU(r)).filter(u=>u!==U);
      GGREF={};pool.slice(0,4).forEach(u=>{GGREF[u]=[U]});
      await saveGGREF();
      await openView(rowByUid(pool[0])[F.NO]); await wait(900);
      const n=$('#card .ggref .gguse');
      T('B-3 ★쓰임 수 4 = 회색',!!n&&txt(n)==='4'
        &&getComputedStyle(n).color===getComputedStyle(document.getElementById('eCnts')).color,
        n?[txt(n),getComputedStyle(n).color]:null);
      GGREF={};pool.forEach((u,i)=>{if(i<12)GGREF[u]=[U]});
      await saveGGREF(); draw(); await wait(300);
      await openView(rowByUid(pool[0])[F.NO]); await wait(900);
      const n2=$('#card .ggref .gguse');
      T('B-3 ★쓰임 수 12 = 빨강(문턱 5)',!!n2&&txt(n2)==='12'&&n2.classList.contains('hot'),
        n2?[txt(n2),n2.className]:null);}
     GG={};GGREF={};await saveGG();await saveGGREF();
     closeView(); await wait(250);
   });

   /* ══════════ B-4 교재 ══════════ */
   await grp('B', async()=>{
     const r0=DATA.filter(r=>kindOf(r)==='G'&&bpgOf(r))[0]||DATA.filter(r=>kindOf(r)==='G')[0];
     await openView(r0[F.NO]); await wait(900);
     T('B-4 ★생물도 교재가 떠 있는 창이다(HASBOOK)',HASBOOK===true);
     const chip=$('#card .cmeta [data-bpl]')||$('#card [data-bpl]');
     T('B-4 📖 p 칩에 data-bpl 이 붙는다',!!chip||!bpgOf(r0),
       [!!chip,bpgOf(r0)]);
     if(chip){const was=VNO;chip.click(); await wait(700);
       T('B-4 ★📖 p 칩 = 교재 자리 목록 창(문항은 안 열린다)',
         !!document.getElementById('bpl')&&VNO===was,[!!document.getElementById('bpl'),VNO,was]);
       const x=document.getElementById('bplX');if(x)x.click();await wait(200)}
     /* 원본 그림 ✕ */
     const rImg=DATA.filter(r=>kindOf(r)==='G'&&r[F.FILE]==='IMG')[0];
     if(rImg){await openView(rImg[F.NO]); await wait(900);
       T('B-4 ★그림 문항에 ✕ 가 있다',!!$('#card #cFigX'));
       if($('#card #cFigX')){$('#card #cFigX').click();
         await until(()=>!!$('#card #cFigShow'),5000); await wait(300);
         T('B-4 ★가리면 「🖼 원본 그림 보이기」 칩',!!$('#card #cFigShow')&&!$('#card #cFig'));
         $('#card #cFigShow').click(); await wait(400)}}
     else T('B-4 그림 문항이 있다',false);
     /* 〈보기〉 줄 고치기 */
     const rB=DATA.filter(r=>kindOf(r)==='G'&&(r[F.BOGI]||[]).length)[0];
     if(rB){await openView(rB[F.NO]); await wait(900);
       T('B-4 ★〈보기〉 줄에 data-tfx="b키" 가 붙는다',
         !!$('#card .bogi .t[data-tfx^="b"]'),
         $('#card .bogi .t')?$('#card .bogi .t').getAttribute('data-tfx'):null)}
     else N('B-4 〈보기〉 있는 생물 기출',0);
     closeView(); await wait(250);
   });

   /* ══════════ L 학습로그 단추 ══════════ */
   await grp('L', async()=>{
     const btns=[...document.querySelectorAll('button')].filter(b=>txt(b)==='📝 학습로그');
     T('L 생물 — 「📝 학습로그」 단추 DOM 0',btns.length===0,btns.length);
     /* ⚠ `openPanel` 은 처음부터 IIFE 안이라 **전역이 아니다**(옛 판도 `typeof` 가 undefined).
        코드가 남았는지는 정적 잣대 Z-33 이 잰다. 여기서는 단추가 없다는 것만 잰다. */
     N('L 생물 — openPanel 은 IIFE 안(전역 아님)',typeof openPanel);
   });



   /* ══════════ W-1 — add9 §A 첫 화면 상주 서랍(세 과목 공통) ══════════ */
   await grp('WD', async()=>{
     FL.past='';FL.year='';FL.lv='';FL.star=false;FL.mark='';FL.bigs=[];FL.subs=[];FL.q='';
     draw(); await wait(600);
     T('WD-1 ★「목차」 단추(#btnTree)가 없다',!document.getElementById('btnTree'),
       !!document.getElementById('btnTree'));
     const dr=document.getElementById('navdr');
     T('WD-1 ★서랍이 첫 화면에 늘 서 있다',
       !!dr&&!dr.classList.contains('hide')&&dr.getBoundingClientRect().width>0,
       dr?[dr.className,Math.round(dr.getBoundingClientRect().width)]:'없음');
     T('WD-1 ★서랍이 `#view` 밖으로 나왔다(창 안에 안 남는다 · §B)',
       !!dr&&!document.querySelector('#view #navdr')&&!document.querySelector('#view #navTg'),
       [!!document.querySelector('#view #navdr'),!!document.querySelector('#view #navTg')]);
     { const lib=document.getElementById('lib');
       const a=dr?dr.getBoundingClientRect():null, b=lib?lib.getBoundingClientRect():null;
       T('WD-1 ★본문과 안 겹친다(서랍 오른끝 ≤ 본문 왼끝)',
         !!a&&!!b&&a.right<=b.left+1,[a?Math.round(a.right):'-',b?Math.round(b.left):'-']); }
     { const l=document.getElementById('ndList');
       const nos=(typeof navList==='function')?navList():[];
       let ok2=0; nos.forEach(n=>{if(rec(n))ok2++});
       try{navBuild()}catch(e){}
       N('진단 navBuild 속',{nos:nos.length,rec성공:ok2,
         ndList부모:l?(l.parentNode?(l.parentNode.id||l.parentNode.className||l.parentNode.tagName):'없음'):'#ndList 없음',
         ndList아이:l?l.childNodes.length:'-',
         navdr부모:(()=>{const d=document.getElementById('navdr');
           return d&&d.parentNode?(d.parentNode.id||d.parentNode.tagName):'-'})(),
         같은l:l===document.getElementById('ndList')}); }
     const nRow=()=>document.querySelectorAll('#ndList .ndrow').length;
     const nSec=()=>document.querySelectorAll('#ndList .ndsec').length;
     T('WD-1 ★서랍 줄 수 = 첫 화면 목록 문항 수',nRow()===filtered().length,[nRow(),filtered().length]);
     T('WD-1 단원 머리 줄이 있다(옛 「목차」 구실)',nSec()>0,nSec());
     T('WD-1 단원 머리 줄에 마지막 마크 점·문항 수가 있다',
       (()=>{const h=document.querySelector('#ndList .ndsec');
         return !!h&&!!h.querySelector('.dot')&&!!h.querySelector('.n')})(),
       (()=>{const h=document.querySelector('#ndList .ndsec');return h?txt(h).slice(0,24):'없음'})());
     /* 편 칩·검색을 바꾸면 같이 바뀐다 */
     { const before=nRow();
       const big=$$$('#eChs .chchip')[1]; if(big){big.click(); await wait(600);}
       T('WD-1 ★편 칩을 바꾸면 서랍도 같이 좁아진다',nRow()===filtered().length&&nRow()<before,
         [before,nRow(),filtered().length]);
       $$$('#eChs .chchip')[0].click(); await wait(500); }
     { const q=document.getElementById('q');
       if(q){ q.value='운동'; q.dispatchEvent(new Event('input',{bubbles:true})); await wait(700);
         T('WD-1 ★검색을 걸면 서랍도 같이 좁아진다',nRow()===filtered().length,[nRow(),filtered().length]);
         q.value=''; q.dispatchEvent(new Event('input',{bubbles:true})); await wait(600); }
       else T('WD-1 ★검색을 걸면 서랍도 같이 좁아진다',false,'#q 없음'); }
     T('WD-1 서랍 줄 글자 = 코드+난이도-제목',
       (()=>{const r0=document.querySelector('#ndList .ndrow');if(!r0)return false;
         const t2=txt(r0.querySelector('.ndt'));return t2.length>0&&t2.indexOf('undefined')<0})(),
       (()=>{const r0=document.querySelector('#ndList .ndrow');
         return r0?txt(r0.querySelector('.ndt')).slice(0,30):'없음'})());
     /* §A-6 옛 목차 서랍은 안 뜬다 */
     T('WD-1 ★옛 목차 서랍(#tree)이 안 뜬다',
       (()=>{try{treeOpen()}catch(e){}const t=document.getElementById('tree');
         return !t||t.classList.contains('hide')})(),'');
     T('WD-1 #trTog 가 상주 서랍 머리로 갔다(카드 층) · 물리는 숨음',
       (()=>{const t=document.getElementById('trTog');
         if(!t)return true;
         return !!t.closest('#navdr')||getComputedStyle(t).display==='none'})(),
       (()=>{const t=document.getElementById('trTog');
         return t?[!!t.closest('#navdr'),getComputedStyle(t).display]:'없음'})());
     /* §D-6 좁은 화면 규칙(소스·CSS 로 잰다 — 하네스 창은 1500px 이다) */
     T('WD-1 좁은 화면은 접힌 채 시작한다(규칙)',
       String(ndResident).indexOf('window.innerWidth<900')>=0,'');
   });

   /* ★ 9/28 penfinger_add2 회귀 — E-1 도 X-11 처럼 시험지 받기·기록 동기화가 끝난 뒤 찍는다(한 판만 동기화가 끝나
      「6회독↔5회독」「안 품 286·맞음 27 ↔ 안 품 318·맞음 1」이 갈렸다 — 같은 판을 다시 돌리면 PASS · 판 탓 아님) */
   await until(()=>{const b=document.getElementById('dl');return !b||b.classList.contains('hide')||!/받는 중/.test(b.textContent||'')},60000);
   await until(()=>typeof recBusy==='undefined'||!recBusy,60000);
   try{if(typeof syncRecords==='function')await Promise.race([syncRecords(true),wait(60000)])}catch(e){}
   await until(()=>typeof recBusy==='undefined'||!recBusy,60000);
   draw(); await wait(600);
   snap.cnt=String($('#cnt').textContent||'');
   snap.list=$$$('#list .item').slice(0,25).map(el=>String(el.textContent||'').replace(/\s+/g,' ').trim()).join(' || ');
   snap.hd=$$$('#list .grouphd').slice(0,8).map(el=>String(el.textContent||'').replace(/\s+/g,' ').trim()).join(' || ');
   snap.spec=$$$('#spec i').length+'/'+$$$('#spec i.gap').length;
   snap.esh=String(((document.getElementById('esh')||{}).textContent)||'').replace(/\s+/g,' ').trim().slice(0,200);
   try{await __nativeFetch('/snap',{method:'POST',body:JSON.stringify(snap)})}catch(e){}
"""

BODY_PHYS = r"""
   await wait(1500);
   ['jagwa.earth.coll','jagwa.view.win','jagwa.win.view','jagwa.win.mc','jagwa.win.jn']
     .forEach(k=>{try{localStorage.removeItem(k)}catch(e){}});
   _coll=null;
   FL.past='y';FL.q='';FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';
   GG={};GGREF={};
   draw(); await wait(500);
   /* ⚠ 본판(add3)에는 이 판의 새 문이 없다 — 여기서 죽으면 **묶음별 헛잣대**가 안 나온다.
        없는 이름은 null 로 적고 묶음까지 가게 둔다. */
   N('물리 밑준비',{subj:SUBJ_ID,DATA:DATA.length,
     SHELL:(typeof SHELL==='undefined'?null:SHELL),
     HASBOOK:(typeof HASBOOK==='undefined'?null:HASBOOK),
     HASROUND:(typeof HASROUND==='undefined'?null:HASROUND()),
     HASJOGAK:(typeof HASJOGAK==='undefined'?null:HASJOGAK),
     층:(typeof lvDeep==='undefined'?null:(lvDeep()?3:2)),
     장:Object.keys(TOC.ch).length,절:Object.keys(TOC.sec).length});

   /* ══════════ P-1 껍데기 ══════════ */
   await grp('P', async()=>{
     const esh=document.getElementById('esh');
     T('P-1 ★물리에도 껍데기가 섰다',!!esh);
     T('P-1 제목이 과목 이름을 단다',txt(esh.querySelector('h1'))==='📖 자과 서재 · 물리',
       txt(esh.querySelector('h1')));
     T('P-1 ★목차를 인라인 DATA 에서 지었다(장 6 · 절 63)',
       Object.keys(TOC.ch).length===6&&Object.keys(TOC.sec).length===63,
       [Object.keys(TOC.ch).length,Object.keys(TOC.sec).length]);
     T('P-1 ★두 층이다 — 「소단원」 걸음이 없다',lvDeep()===false&&lvOrder().length===3,
       [lvDeep(),lvOrder()]);
     /* ★ add6 §D-2 — 히트맵이 **분류·편을 따라간다.** 「전체·전체」일 때 577 이고,
        분류를 고르면 칸 수 = 목록 수여야 한다. 재기 전에 거르개를 푼다. */
     N('진단 P-1 FL',{past:FL.past,bigs:FL.bigs.slice(),star:FL.star,year:FL.year});
     {const keep=FL.past; FL.past='';FL.bigs=[];draw(); await wait(400);
      T('P-1 ★히트맵 칸 수 = 문항 수 577(전체·전체)',$$$('#spec i').length===577,$$$('#spec i').length);
      FL.past=keep;draw(); await wait(300);}
     T('P-1 히트맵에 빈 칸이 없다',$$$('#spec i.gap').length===0,$$$('#spec i.gap').length);
     T('P-1 머리 개수 = 「577문제」(갈래가 하나다)',txt(document.getElementById('eCnts'))==='577문제',
       txt(document.getElementById('eCnts')));
     const ec=document.getElementById('examChip');
     T('P-1 ★D-날 칩 11px · 800(지학과 같은 px)',
       !!ec&&getComputedStyle(ec).fontSize==='11px'&&getComputedStyle(ec).fontWeight==='800',
       ec?[getComputedStyle(ec).fontSize,getComputedStyle(ec).fontWeight]:null);
     /* 단원 머리 — 「공식」이 살아 있다 */
     const frm=document.querySelector('#list .grouphd [data-frm]');
     T('P-1 ★단원 머리에 「공식」이 남아 있다',!!frm,
       $$$('#list .grouphd').slice(0,3).map(h=>txt(h)));
     if(frm){frm.click(); await wait(600);
       T('P-1 ★「공식」을 누르면 옛 시트가 그대로 열린다',$$$('.sheet').length>0,$$$('.sheet').length);
       $$$('.sheet').forEach(x=>x.remove()); await wait(150)}
     T('P-1 단원 머리에 🃏 칩도 있다(옛 「암기카드」가 하던 일)',
       !!document.querySelector('#list .grouphd [data-mc]'));
     /* 접기 순환 */
     const lv=document.getElementById('lvBtn');
     const seq=[];
     for(let i=0;i<4;i++){seq.push(txt(lv));lv.click();await wait(300)}
     T('P-1 ★순환 걸음 = 세 걸음',new Set(seq).size===3,seq);
     lvApply('all',false);draw();await wait(300);
     /* 접은 채 머리 통계 */
     const openN=$$$('#list .grouphd.ch').map(h=>txt(h)).join('|');
     lvApply('ch',false);draw();await wait(300);
     T('P-1 ★접은 채 머리 통계가 편 채와 같다',
       $$$('#list .grouphd.ch').map(h=>txt(h)).join('|')===openN);
     lvApply('all',false);draw();await wait(300);
   });

   /* ══════════ P-5 add4 — 옛 필터 거르개 셋 · 쌍둥이 칩 ══════════ */
   await grp('P', async()=>{
     FL.past='';FL.year='';FL.lv='';FL.star=false;FL.mark='';FL.bigs=[];FL.subs=[];
     draw(); await wait(500);
     const esh=document.getElementById('esh');
     const y=esh.querySelector('#fYear'), lv=esh.querySelector('#fLv'),
           cls=esh.querySelector('#fCls'), mem=esh.querySelector('#fMemo'),
           stb=esh.querySelector('#fStarBtn'), acl=esh.querySelector('#fAllClr');
     /* ★ add10 §A-1 — 「★중요」·「모두 풀기」 칩까지 걷었다(사용자 9/21).
        고르개 줄 = 「필터 ▾ · 연도 ▾ · 난이도 ▾」까지다. */
     T('P-5 ★`.ebar` = 연도·난이도만 · 분류 ▾·메모·★중요·모두 풀기 0',
       !!y&&!!lv&&!cls&&!mem&&!stb&&!acl,
       [!!y,!!lv,!!cls,!!mem,!!stb,!!acl]);
     T('P-5 ★연도 항목 25 + 「연도 ▾」',!!y&&y.options.length===26,y?y.options.length:null);
     T('P-5 ★난이도 항목 3 + 「난이도 ▾」',!!lv&&lv.options.length===4,lv?lv.options.length:null);
     T('P-5 옛 필터 줄은 안 보인다',
       ['#fBig','#fEtc'].every(q=>{const el=$(q);return !el||el.offsetParent===null}),
       ['#fBig','#fEtc'].map(q=>$(q)?getComputedStyle($(q)).display:'(없음)'));
     /* 옛 칩 31 전수 대조 — 옛 판에서 그 값을 켠 목록 = 새 판에서 고르개로 고른 목록 */
     const setOf=()=>filtered().map(r=>r[F.NO]).join(',');
     const base=setOf();
     let bad=[];
     /* 난이도 셋 */
     for(const v of ['상','중','하']){
       FL.lv=v; const a1=setOf();
       const want=DATA.filter(r=>String(r[F.LV]||'')===v).map(r=>r[F.NO]).join(',');
       if(a1!==want)bad.push('lv:'+v);
       FL.lv='';}
     /* 갈래 둘 */
     /* ★ add18 §A-1 — 「타기출」을 「기본」에 합쳤다. `'n'` = **변리사가 아닌 것 전부** */
     for(const v of ['y','n']){
       FL.past=v; const a1=setOf();
       const want=DATA.filter(r=>v==='y'?r[F.SRC]==='변리사':r[F.SRC]!=='변리사').map(r=>r[F.NO]).join(',');
       if(a1!==want)bad.push('past:'+v);
       FL.past='';}
     /* 옛 `'p'`(타기출)가 어디엔가 남아 있어도 `'n'` 으로 읽는다(§A-1) */
     {FL.past='p'; const a1=setOf();
      const want=DATA.filter(r=>r[F.SRC]!=='변리사').map(r=>r[F.NO]).join(',');
      if(a1!==want)bad.push('past:p→n');
      FL.past='';}
     /* ★중요 */
     {FL.star=true; const a1=setOf();
      const want=DATA.filter(r=>r[F.STAR]).map(r=>r[F.NO]).join(',');
      if(a1!==want)bad.push('star');
      FL.star=false;}
     /* 연도 25 — 옛 판과 같이 past==='y' 일 때만 뜻이 있다 */
     {FL.past='y';
      for(const o of [...y.options].slice(1)){
        FL.year=o.value; const a1=setOf();
        const want=DATA.filter(r=>r[F.SRC]==='변리사'&&String(r[F.YEAR])===o.value).map(r=>r[F.NO]).join(',');
        if(a1!==want)bad.push('year:'+o.value);}
      FL.year='';FL.past='';}
     T('P-5 ★옛 칩 31 전수 대조 — 거르는 결과가 같다',bad.length===0,bad);
     T('P-5 아무것도 안 고르면 전체다',setOf()===base&&filtered().length===577,filtered().length);
     /* 고르개가 상태를 그대로 쓴다(겉만 바꿨다) */
     {lv.value='상'; lv.dispatchEvent(new Event('change')); await wait(400);
      T('P-5 ★난이도 고르개가 FL.lv 를 쓴다',FL.lv==='상'&&filtered().every(r=>r[F.LV]==='상'),
        [FL.lv,filtered().length]);
      lv.value=''; lv.dispatchEvent(new Event('change')); await wait(300);}
     /* 분류 — 갈래와 ★ 를 **같이** 켤 수 있다(옛 판 능력) */
     /* ★ add10 §A-1 — 분류 칩 + 고르개만 남았다. 각 고르개의 빈 값(「연도 ▾」)이 풀기다.
        `FL.star` 는 죽은 조건으로 남되 **늘 거짓**이어야 한다. */
     {const kd=esh.querySelector('#eKind');
      kd.querySelector('[data-past="y"]').click(); await wait(400);
      y.value=[...y.options].map(o=>o.value).filter(Boolean)[0];
      y.dispatchEvent(new Event('change')); await wait(400);
      T('P-5 ★분류 칩과 연도 고르개가 같이 먹는다',
        FL.past==='y'&&!!FL.year&&filtered().every(r=>r[F.SRC]==='변리사'&&String(r[F.YEAR])===FL.year),
        [FL.past,FL.year,filtered().length]);
      y.value=''; y.dispatchEvent(new Event('change')); await wait(350);
      kd.querySelector('[data-past=""]').click(); await wait(400);
      T('P-5 ★고르개의 빈 값이 풀기 구실을 한다',!FL.past&&!FL.year,[FL.past,FL.year]);
      T('P-5 ★`FL.star` 는 늘 거짓이다(죽은 조건)',FL.star===false,FL.star);}
     /* 연도는 변리사 기출일 때만 산다(옛 판 1836줄) */
     T('P-5 ★연도는 「변리사 기출」이 아니면 잠긴다',y.disabled===true,y.disabled);
     /* 쌍둥이 칩 */
     /* ⚠ 하네스 환경에는 `TW`(쌍둥이) 자료가 없다 — 실물에는 7건이 있다(census).
        칩이 **그려지는 길**을 재는 것이므로 흉내 두 칸을 심는다. */
     /* ⚠ 실기록(기록.json)이 실린 판에서는 `TW` 에 **진짜 쌍둥이**가 들어 있다
        (2026-09-21 — 물리만 돌리면 0, 세 과목을 잇달아 돌리면 9). 재는 것은
        「칩이 그려지는 길」이므로 통을 비우고 흉내 둘만 남겨 **셈을 고정**한다. */
     N('진단 TW 심기 전',{n:Object.keys(TW||{}).length,keys:Object.keys(TW||{}).slice(0,12)});
     const _twKeep=JSON.stringify(TW);
     Object.keys(TW).forEach(k=>{delete TW[k]});
     TW[DATA[0][F.NO]]=[DATA[1][F.NO]]; TW[DATA[1][F.NO]]=[DATA[0][F.NO]];
     draw(); await wait(400);
     const tw=$$$('#list [data-tw]');
     T('P-5 ★목록 줄에 쌍둥이 칩이 돌아왔다',tw.length===2,tw.length);
     if(tw.length){tw[0].click(); await wait(500);
       const sh=$$$('.sheet').filter(x=>!x.classList.contains('hide'));
       T('P-5 ★쌍둥이 칩을 누르면 옛 시트가 열린다',sh.length>0,sh.length?txt(sh[sh.length-1].querySelector('h2')||sh[sh.length-1]).slice(0,30):null);
       sh.forEach(x=>x.remove()); await wait(150)}
     try{const _t=JSON.parse(_twKeep);Object.keys(TW).forEach(k=>{delete TW[k]});
       Object.keys(_t).forEach(k=>{TW[k]=_t[k]})}catch(e){}
     FL.past='';FL.year='';FL.lv='';FL.star=false;draw(); await wait(300);
   });

   /* ══════════ P-2 문항 창 · .vbot 두 줄 ══════════ */
   await grp('P', async()=>{
     await openView(DATA[0][F.NO]); await wait(1100);
     T('P-2 ★물리 문항이 떠 있는 창으로 열린다',
       $('#view').classList.contains('win')&&!!document.getElementById('vWinTg'),$('#view').className);
     const pill=document.getElementById('inkPill');
     T('P-2 ★#inkPill 이 .vtop 안이다',!!pill&&!!pill.closest('#view .vtop'));
     T('P-2 ★물리 알약 단추 **여덟**(글상자 없음)',
       pill&&(pill.querySelectorAll('button').length===8||(pill.querySelectorAll('button').length===9&&!!pill.querySelector('#tCut'))),   /* ★ 2026-10-07 (_task_jagwa_phys_win §A-13 ㉑㉕) — 필기 알약 ↺ 오른쪽에 ✂ 오리기(#tCut) 하나 더 = 뜻한 차 · 옛: pill.querySelectorAll('button').length===8 */
       pill?[...pill.querySelectorAll('button')].map(b=>b.id||b.dataset.pen||b.dataset.hl):null);
     T('P-2 물리에는 글상자 단추 자체가 없다',!document.getElementById('tTxt'));
     T('P-2 알약 높이 ≤ 26px',pill.getBoundingClientRect().height<=26,pill.getBoundingClientRect().height);
     /* ★ add15 — 아랫줄 다섯이 윗줄로 갔다. 이제 **한 줄 열일곱**이다(§B-6). */
     const r1=document.getElementById('pRow1');
     T('P-14 ★.vbot 에 보이는 줄이 하나다',
       !!r1&&[...document.querySelectorAll('.vbot .tools')]
         .filter(x=>x.getBoundingClientRect().height>0).length===1,
       [...document.querySelectorAll('.vbot .tools')]
         .map(x=>[x.id||'(빈)',Math.round(x.getBoundingClientRect().height)]));
     const want=['tAns','tSol','mO','mQ','mX','mP',
                 'tLayer','tLayerAdd','tLayerEye','tHist','tCard',
                 'tTheory','tConcept','tTwin','tGpt','tType','tLink'];
     const seen=want.filter(id=>{const b=document.getElementById(id);
       return b&&r1.contains(b)&&b.getBoundingClientRect().width>0});
     /* ★ 2026-10-07 (_task_jagwa_phys_win §A-27 ⑯ · §A-13 ⑥ · §A-04 ⑪㉞㉟㊱) — 물리 아랫줄 #tSol·#tLayer·#tLayerAdd·#tLayerEye·#tType·#tTwin·#tConcept 숨김
        (할 일은 답풀 한 창 · 회독 창 · 근거 · 🔗 · 이론 덮개로) = 뜻한 차 → 새 꼴 = 그 일곱만 빠진 열(차례 그대로) · 옛: seen.length===17 */
     T('P-14 ★한 줄에 열일곱이 다 선다',seen.length===17||seen.join(',')===want.filter(x=>['tSol','tLayer','tLayerAdd','tLayerEye','tType','tTwin','tConcept'].indexOf(x)<0).join(','),
       {보임:seen.length,빠짐:want.filter(x=>seen.indexOf(x)<0)});
     T('P-14 ★차례가 「정답…P · (빈칸) · 다섯 · 공식…연결」이다',
       [...r1.children].map(x=>x.id||x.className).filter(x=>x!=='sp').join(',')===want.join(','),
       [...r1.children].map(x=>x.id||x.className));
     { /* 다섯의 꼴 = 「공식」과 같다(글자 꼴 · 상자 없음) */
       const th=document.getElementById('tTheory'), cs=el=>getComputedStyle(el);
       const keys=['fontSize','fontWeight','color','backgroundColor','borderTopWidth',
                   'paddingLeft','paddingRight'];
       const bad=[];
       ['tLayer','tLayerAdd','tLayerEye','tHist','tCard'].forEach(id=>{
         const b=document.getElementById(id); if(!b){bad.push([id,'없음']);return}
         if(cs(b).display==='none')return;   /* ★ 2026-10-07 (_task_jagwa_phys_win §A-04 ⑪ · §A-13 ⑥) — 숨긴 단추(#tLayer·#tLayerAdd·#tLayerEye)는 꼴을 안 잰다(안 보임) · 옛 판은 다섯 다 보여 그대로 잰다 */
         keys.forEach(k=>{if(cs(b)[k]!==cs(th)[k])bad.push([id,k,cs(b)[k],cs(th)[k]])});
       });
       T('P-14 ★다섯의 계산 스타일 = 「공식」과 같다',bad.length===0,bad.slice(0,5));
       T('P-14 ★「+회독」이 두 줄로 안 꺾인다(높이 = 「공식」)',
         getComputedStyle(document.getElementById('tLayerAdd')).display==='none'||   /* ★ 2026-10-07 (_task_jagwa_phys_win §A-13 ⑥ · §A-04 ⑪) — 물리 「+회독」 숨김(다시 열면 새 회독 · 회독 창) = 뜻한 차 → 숨었으면 꺾일 일이 없다 */
         Math.abs(document.getElementById('tLayerAdd').getBoundingClientRect().height
                 -th.getBoundingClientRect().height)<=1,
         [document.getElementById('tLayerAdd').getBoundingClientRect().height,
          th.getBoundingClientRect().height]); }
     T('P-2 「정답 ▸」·「풀이 ▸」 글자',
       (txt(document.getElementById('tAns'))==='정답 ▸'||txt(document.getElementById('tAns'))==='답풀')&&txt(document.getElementById('tSol'))==='풀이 ▸',   /* ★ 2026-10-07 (_task_jagwa_phys_win §A-27 ⑯㉝) — #tAns 글자 「답풀」(정답·풀이 한 창 · #tSol 은 숨김 · 글자 「풀이 ▸」 그대로) = 뜻한 차 · 옛: txt(#tAns)==='정답 ▸' */
       [txt(document.getElementById('tAns')),txt(document.getElementById('tSol'))]);
     {const a=document.getElementById('tAns').getBoundingClientRect();
      T('P-2 「정답 ▸」 높이 26px(지학 「정답·해설 ▸」 값)',Math.abs(a.height-26)<=1||(txt(document.getElementById('tAns'))==='답풀'&&a.height>=14&&a.height<26),a.height);   /* ★ 2026-10-07 (_task_jagwa_phys_win §A-04 ㉝ · §A-27) — 물리 아랫줄 줄임: 「답풀」 = 글자 단추(상자 없음 · height:auto · 11px×1.3 + 위아래 2px ≈ 18px) = 뜻한 차 → 「답풀」이면 14 이상 26 미만 · 옛: Math.abs(a.height-26)<=1 */
      const o=document.getElementById('mO').getBoundingClientRect();
      T('P-2 O△XP 30×26(지학 값)',(Math.abs(o.width-30)<=1&&Math.abs(o.height-26)<=1)||(Math.abs(o.width-24)<=1&&Math.abs(o.height-21)<=1),[o.width,o.height]);}   /* ★ 2026-10-07 (_task_jagwa_phys_win §A-04 ㉝) — 물리 O△XP 칸 줄임 width:24px · height:21px = 뜻한 차 · 옛: 30×26 만 */
     /* ★ add15 §A-3 — 비게 된 아랫줄은 접힌다(DOM 은 남긴다) */
     const vis=[...document.querySelectorAll('.vbot .tools:not(#pRow1)>*')].filter(el=>el.offsetParent!==null);
     T('P-14 ★빈 아랫줄에 보이는 것 0',vis.length===0,vis.map(el=>el.id));
     T('P-14 ★빈 아랫줄 높이 0',
       [...document.querySelectorAll('.vbot .tools:not(#pRow1)')]
         .every(x=>x.getBoundingClientRect().height===0),
       [...document.querySelectorAll('.vbot .tools:not(#pRow1)')]
         .map(x=>x.getBoundingClientRect().height));
     T('P-2 #tW 안 보임 · 값 2',$('#tW').offsetParent===null&&$('#tW').value==='2');
     T('P-2 #tNote 는 숨는다(코멘트는 근거로 갔다)',$('#tNote').offsetParent===null);
     /* PDF 를 끝까지 굴려도 아랫줄이 보인다 */
     {const st=document.getElementById('stage');
      st.scrollTop=st.scrollHeight; await wait(300);
      const r=document.getElementById('tAns').getBoundingClientRect();
      T('P-2 ★PDF 를 맨 아래로 굴려도 윗줄이 보인다',r.height>0&&r.bottom<=window.innerHeight+1,
        [r.top,r.bottom,window.innerHeight]);
      st.scrollTop=0; await wait(250);}
     /* 일곱 각각 누름 → 시트 */
     for(const id of ['tTheory','tConcept','tTwin','tGpt','tType','tAns','tSol']){
       const b=document.getElementById(id); if(!b){T('P-2 '+id+' 가 있다',false);continue}
       b.click(); await wait(500);
       const sh=$$$('.sheet').filter(x=>!x.classList.contains('hide')&&!['book','sub','bkq'].includes(x.id));
       /* ⚠ `#tSol`(풀이)은 그 문항 볼트에 풀이 노트가 없으면 **토스트**로 끝난다(옛 동작 그대로 · 3075줄).
          옮기기 전과 같은 길이 돌았는지를 재는 것이므로 시트든 토스트든 「무언가 났다」면 통과다. */
       /* ⚠ `.toast` 는 position:fixed 라 `offsetParent` 가 null 이다 — 그것으로 거르면 안 된다 */
       const ts=[...document.querySelectorAll('.toast')];
       T('P-2 ★'+id+' 를 누르면 옛 길이 그대로 돈다(시트 또는 토스트)',sh.length>0||ts.length>0,
         [sh.length,ts.length,sh.length?txt(sh[sh.length-1].querySelector('h2')||sh[sh.length-1]).slice(0,40):null]);
       sh.forEach(x=>x.remove()); await wait(150)}
     /* P 누름 */
     {const no=DATA[0][F.NO], h0=hist(no).length;
      document.getElementById('mP').click(); await wait(600);
      T('P-2 ★P 를 누르면 기록 마지막이 P',lastM(no)==='P'&&hist(no).length===h0+1,[lastM(no)]);
      T('P-2 그 단추에 on',document.getElementById('mP').classList.contains('on'));
      closeView(); await wait(450);
      const idx=nums().indexOf(codeShow(rec(no))); const cell=$$$('#spec i')[idx];
      N('진단 히트맵',{idx:idx,cls:cell?cell.className:'없음',
        no:(typeof VNO!=='undefined')?VNO:'?',
        last:(typeof VNO!=='undefined'&&ST[VNO]&&ST[VNO].h)?ST[VNO].h.slice(-1)[0]:'없음'});
      /* ⚠ 칸 class 는 `weakState==='less'` 면 **W 가 이긴다**(4890 `w==='less'?'W':…`).
         실기록이 실리면 그 갈래를 탄다 — 규칙 그대로 잰다(2026-09-21 실측). */
      { const less=(typeof weakState==='function')&&weakState(no)==='less';
        const okCell=idx>=0&&!!cell&&(less?/(^|\s)W(\s|$)/.test(cell.className)
                                          :/(^|\s)P(\s|$)/.test(cell.className));
        T('P-2 ★히트맵 칸이 기록을 따라간다(덜약점이면 W · 아니면 P)',okCell,
          [idx,cell&&cell.className,less]); }
      await openView(no); await wait(900);}
   });

   /* ══════════ P-3 근거 목록 자리 · 열쇠 ══════════ */
   await grp('P', async()=>{
     await openView(DATA[0][F.NO]); await wait(1000);
     const box=document.getElementById('ggphys');
     /* ★ add13 — 근거 줄은 문제 **위**다(사용자 9/21). 본판 §B-2 의 「아래」를 뒤집는다. */
     T('P-3 ★근거 목록이 문제 곁에 붙는다',!!box);
     /* ★ 합치기 10/1(하위 에이전트 C) — physphone A-5(97883ef 본문 「물리 근거 칸 = 머리 안 필기 도구 바로 아랫줄(따로 카드 걷음 · 기능 무변)」) — 새 자리(#view .vtop)도 받는다 */
     const inVtop=!!box&&!!box.parentElement&&box.parentElement.classList.contains('vtop')&&!!box.closest('#view');
     T('P-3 ★같은 스크롤 상자(.stage) 안이다(★ physphone A-5 뒤 = 문항 창 머리 .vtop 안)',!!box&&(box.parentElement.id==='stage'||inVtop),
       box?(box.parentElement.id||box.parentElement.className):null);
     T('P-3 ★`#inkc` 밖이다(필기 덮개에 안 가린다)',!!box&&!box.closest('#inkc')&&!box.querySelector('#inkc'));
     T('P-3 ★PDF 묶음(.wrap) **앞**에 온다(add13 §B-1)',
       !!box&&!!document.querySelector('#stage .wrap')
       &&(document.querySelector('#stage .wrap').compareDocumentPosition(box)&2)!==0);
     T('P-3 ★`#stage` 의 첫 자식이다(★ physphone A-5 뒤 = .vtop 안 필기 도구 줄 아래)',
       !!box&&(document.getElementById('stage').firstElementChild===box||inVtop),
       (()=>{const f=document.getElementById('stage').firstElementChild;
         return f?(f.id||f.className):'없음'})());
     T('P-3 ★근거 줄 아래끝 ≤ 문제 위끝(겹침 0)',
       (()=>{const w=document.querySelector('#stage .wrap');
         if(!box||!w)return false;
         return box.getBoundingClientRect().bottom<=w.getBoundingClientRect().top+1})(),
       (()=>{const w=document.querySelector('#stage .wrap');
         return (box&&w)?[Math.round(box.getBoundingClientRect().bottom),
                          Math.round(w.getBoundingClientRect().top)]:'없음'})());
     /* 펜 도구를 든 채 근거 줄이 눌린다 */
     setTool('pen','#16181B'); await wait(200);
     {const el=box.querySelector('.ggrow .txt')||box.querySelector('.ggline');
      const r=el.getBoundingClientRect();
      const a=document.elementsFromPoint(r.left+r.width/2,r.top+r.height/2);
      const j=a.findIndex(z=>z&&(z.id==='inkc'||(z.closest&&z.closest('#inkc'))));
      T('P-3 ★펜 도구를 든 채도 근거 줄이 맨 위다',a.indexOf(el)===0||(j<0),
        [a.indexOf(el),j,a.map(z=>z.id||String(z.tagName)).slice(0,4)]);}
     setTool('view'); await wait(150);
     /* 열쇠 = P + 번호 세 자리 */
     const r0=DATA[0];
     T('P-3 ★근거 열쇠가 `P`+번호 세 자리다',GGU(r0)==='P001',GGU(r0));
     T('P-3 표시·검색이 쓰는 F.CODE 는 그대로다',r0[F.CODE]==='PEM0101',r0[F.CODE]);
     T('P-3 ★rowByUid 가 그 열쇠로도 찾는다',rowByUid('P001')===r0);
     T('P-3 물리 SYNC 키 = gg·ggref 둘(pick 은 없다)',
       SYNC_KEYS.indexOf('gg')>=0&&SYNC_KEYS.indexOf('ggref')>=0&&SYNC_KEYS.indexOf('pick')<0,
       SYNC_KEYS.filter(k=>['gg','ggref','pick','link'].includes(k)));
     /* 근거 더하기 → 상자·칩 */
     {const A=GGU(r0);
      GG={};GGREF={};await saveGG();await saveGGREF();
      await openView(r0[F.NO]); await wait(900);
      const rows=document.querySelector('#ggphys [data-ggrows]');
      T('P-3 적는 칸이 있다',!!rows);
      rows.querySelector('.txt').value='물리 첫 근거';
      await ggAdd(A,'qp-',false); await wait(600);
      T('P-3 ★근거가 그 열쇠에 담긴다',ggOf(A).length===1&&ggOf(A)[0].t==='물리 첫 근거',
        [Object.keys(GG),ggOf(A).length]);
      closeView(); await wait(350); draw(); await wait(300);
      const el=$$$('#list .item').find(x=>txt(x.querySelector('.num'))===codeShow(r0));
      T('P-3 목록 카드에 「근거 1」 칩',!!el&&txt(el).indexOf('근거 1')>=0,el?txt(el).slice(0,90):null);
      GG={};GGREF={};await saveGG();await saveGGREF();draw();await wait(250)}
   });

   /* ══════════ P-4 코멘트 흡수 ══════════ */
   await grp('P', async()=>{
     GG={};await saveGG();
     const G=DATA.slice(0,3);
     CMT={}; G.forEach((r,i)=>{CMT[r[F.NO]]='물리 코멘트 '+(i+1)});
     await put('kv','note',CMT);
     const n1=await ggEatNotes(); await wait(400);
     T('P-4 ★흉내 코멘트 셋이 근거로 옮겨진다',
       n1===3&&Object.keys(GG).length===3&&Object.keys(CMT).length===0,
       [n1,Object.keys(GG).length,Object.keys(CMT).length]);
     T('P-4 ★열쇠가 P+번호 꼴이다',Object.keys(GG).every(k=>/^P\d{3}$/.test(k)),Object.keys(GG));
     const n2=await ggEatNotes(); await wait(300);
     T('P-4 ★두 번 돌려도 +0(멱등)',n2===0&&Object.keys(GG).length===3,[n2,Object.keys(GG).length]);
     GG={};CMT={};await saveGG();await put('kv','note',CMT);draw();await wait(250);
   });

   /* ══════════ L 학습로그 단추 ══════════ */
   await grp('L', async()=>{
     const btns=[...document.querySelectorAll('button')].filter(b=>txt(b)==='📝 학습로그');
     T('L 물리 — 「📝 학습로그」 단추 DOM 0',btns.length===0,btns.length);
     /* ⚠ `openPanel` 은 처음부터 IIFE 안이라 **전역이 아니다**(옛 판도 `typeof` 가 undefined).
        코드가 남았는지는 정적 잣대 Z-33 이 잰다. 여기서는 단추가 없다는 것만 잰다. */
     N('L 물리 — openPanel 은 IIFE 안(전역 아님)',typeof openPanel);
   });

   /* ══════════ P-6 물리 뷰어 되살림 (add5 §B) ══════════
      ⚠ 픽셀 IDENTICAL 이 아니다 — 「기본값(300×150)이 아닌가 · 알파>0 표본이 있는가 ·
        글자가 앞 판과 같은가 · 함수 본문이 빈 껍데기가 아닌가」로 잰다. */
   await grp('P', async()=>{
     const P3={img:null,byun:null,base:null};
     for(let i=0;i<DATA.length;i++){const r=DATA[i],no=r[F.NO];
       try{if(P3.img===null&&locate(r).id==='IMG')P3.img=no}catch(e){}
       if(P3.byun===null&&r[F.SRC]==='변리사')P3.byun=no;
       if(P3.base===null&&!r[F.SRC])P3.base=no;
       if(P3.img!==null&&P3.byun!==null&&P3.base!==null)break}
     T('P-6 그림 문항이 실제로 있다(재는 자리가 맞는가)',P3.img!==null,P3);
     /* 앞 판 352bff7(66eddc25) 에서 잰 글자 — `_h_add5.py` 가 실물로 한 번 더 맞대 본다 */
     const WANT={15:['15. 가속도,그래프 · 15',
                     '1. 역학 › 등속 운동, 등가속도 운동 · Self · 상 · 2018 변리사 · PA1809 · 볼트 4 · 교재 11쪽'],
                 6:['6. 등속 운동, 등가속도 운동 · 6',
                    '1. 역학 › 등속 운동, 등가속도 운동 · Ec · 중 · 2008 변리사 · PA0801 · 볼트 3 · 교재 7쪽'],
                 1:['1. 등속 운동, 등가속도 운동 · 1',
                    '1. 역학 › 등속 운동, 등가속도 운동 · Ec · 하 · PEM0101 · 교재 2쪽']};
     const drawnN=c=>{try{const g=c.getContext('2d'),w=c.width,h=c.height;if(!w||!h)return -1;
       const d=g.getImageData(0,0,w,h).data;let n=0;
       for(let y=0;y<h;y+=Math.max(1,(h/40)|0))for(let x=0;x<w;x+=Math.max(1,(w/40)|0)){
         const i=((y*w)+x)*4;if(d[i+3]>0&&!(d[i]===255&&d[i+1]===255&&d[i+2]===255))n++}
       return n}catch(e){return -2}};
     for(const tag of ['img','byun','base']){
       const no=P3[tag]; if(no===null)continue;
       await openView(no,[no]); await wait(1300);
       const c=document.getElementById('pdfc');
       T('P-6 ★'+tag+' #pdfc 가 기본값(300×150)이 아니다',!!c&&!(c.width===300&&c.height===150),
         c?[c.width,c.height]:null);
       T('P-6 ★'+tag+' 그려진 픽셀이 있다',c&&drawnN(c)>0,c?drawnN(c):null);
       T('P-6 '+tag+' 근거 통(#ggphys)은 하나다',
         document.querySelectorAll('#ggphys').length===1,document.querySelectorAll('#ggphys').length);
       const w=WANT[no];
       if(w){
         T('P-6 ★'+tag+' #vT1 이 앞 판과 글자까지 같다',txt(document.getElementById('vT1'))===w[0],
           txt(document.getElementById('vT1')));
         T('P-6 ★'+tag+' #vT2 이 앞 판과 글자까지 같다',txt(document.getElementById('vT2'))===w[1],
           txt(document.getElementById('vT2')));
       }
       closeView(); await wait(160);
     }
     /* 뷰어 계열이 빈 껍데기가 아니다 */
     T('P-6 ★renderPage 가 빈 함수가 아니다',String(renderPage).length>200,
       String(renderPage).replace(/\s+/g,' ').slice(0,54));
     T('P-6 ★setupMask·layoutOmr·syncOmr 이 빈 함수가 아니다',
       String(setupMask).length>120&&String(layoutOmr).length>60&&String(syncOmr).length>60,
       [String(setupMask).length,String(layoutOmr).length,String(syncOmr).length]);
     T('P-6 ★showProblem 이 카드판이 아니다(renderCard 를 안 부른다)',
       String(showProblem).indexOf('renderCard')<0,String(showProblem).replace(/\s+/g,' ').slice(0,64));
     T('P-6 ★ensureFiles·renderSettings 가 물리 것이다(「교재 조각」이 없다)',
       String(ensureFiles).indexOf('교재 조각')<0&&String(renderSettings).indexOf('교재 조각')<0,
       [String(ensureFiles).indexOf('교재 조각'),String(renderSettings).indexOf('교재 조각')]);
     T('P-6 ★서랍·목록 패널이 물리 것이다',
       String(buildTree).indexOf('specPast')>=0&&String(navBuild).indexOf('ndList')>=0
       &&String(navSync).indexOf('ndHead')>=0&&String(treePick).indexOf('FL.subs=')>=0,
       [String(buildTree).replace(/\s+/g,' ').slice(0,40),String(navBuild).replace(/\s+/g,' ').slice(0,40)]);
     /* ★ add9 §A-6 — 옛 목차 서랍(#tree)은 걷었다. 그 구실은 **상주 서랍**이 맡는다. */
     T('P-6 ★옛 목차 서랍(#tree)이 안 뜬다',
       (()=>{treeOpen();const t=document.getElementById('tree');
         return !t||t.classList.contains('hide')})(),'');
     T('P-6 #trTog 는 물리에서 숨는다',
       (()=>{const t=document.getElementById('trTog');return !t||getComputedStyle(t).display==='none'})(),
       (()=>{const t=document.getElementById('trTog');return t?getComputedStyle(t).display:'없음'})());
     T('P-6 ★스펙트럼 머리(#specHd)가 물리 글자다',
       /^(전체|변리사 기출|기본) \d+/.test(txt(document.getElementById('specHd'))),   /* ★ add18 §A-1 */
       txt(document.getElementById('specHd')));
     /* 필기 — 빨강 한 획 (본판 §E-3 이 요구했는데 P 묶음에 없던 잣대) */
     {
       const no=(P3.img!==null)?P3.img:DATA[0][F.NO];
       await openView(no,[no]); await wait(1300);
       const _spc=Element.prototype.setPointerCapture,_rpc=Element.prototype.releasePointerCapture;
       Element.prototype.setPointerCapture=function(){};Element.prototype.releasePointerCapture=function(){};
       /* ⚠ 펜 단추는 껍데기가 `#inkPill`(.vtop) 로 옮겼다 — `.vbot` 밑에서 찾으면 없다(9/21 실측) */
       const red=document.querySelector('[data-pen="#B03A2E"]');
       T('P-6 빨강 펜 단추를 찾았다',!!red,red?(red.parentNode.id||red.parentNode.className):'없음');
       if(red)red.click();
       T('P-6 TOOL.color 가 빨강으로 바뀐다',String(TOOL.color).toUpperCase()==='#B03A2E',TOOL.color);
       const c=document.getElementById('inkc'), r=c.getBoundingClientRect();
       const n0=((INK[LAYER]||[]).length);
       await drag(c,r.left+40,r.top+40,r.left+150,r.top+100,'pen');
       await wait(600);
       const n1=((INK[LAYER]||[]).length);
       T('P-6 ★빨강 펜 한 획이 INK 에 든다',n1===n0+1,[n0,n1]);
       const st=(INK[LAYER]||[])[n1-1];
       T('P-6 ★그 획 색이 #B03A2E',!!st&&String(st.c).toUpperCase()==='#B03A2E',st?st.c:null);
       const saved=await get('ink',String(VNO));
       T('P-6 ★저장통(ink)에도 그 획이 있다',!!saved&&((saved[LAYER]||[]).length===n1),
         saved?((saved[LAYER]||[]).length):null);
       T('P-6 ★paintInk 가 빈 함수가 아니다',String(paintInk).length>120,
         String(paintInk).replace(/\s+/g,' ').slice(0,44));
       closeView(); await wait(220);
       await openView(no,[no]); await wait(1300);
       T('P-6 ★닫았다 열어도 그 획이 살아 있다',((INK[LAYER]||[]).length)===n1,(INK[LAYER]||[]).length);
       T('P-6 #tLayer 목록 = 저장된 층 수',
         (()=>{const sl=document.getElementById('tLayer');
           return !sl||sl.options.length===Math.max(1,Object.keys(INK).length)})(),
         (()=>{const sl=document.getElementById('tLayer');
           return sl?[sl.options.length,Object.keys(INK).length]:'없음'})());
       INK[LAYER]=(INK[LAYER]||[]).slice(0,n0); saveInk(); await wait(420); paintInk();
       Element.prototype.setPointerCapture=_spc;Element.prototype.releasePointerCapture=_rpc;
       closeView(); await wait(160);
     }
     /* §B-4 값 있음 표시 — syncTypeBtn·syncGptBtn·linkChip 이 다시 불린다 */
     T('P-6 ★물리 showProblem 이 syncTypeBtn·syncGptBtn·linkChip 을 부른다',
       ['syncTypeBtn','syncGptBtn','linkChip','fillLayerSel','setupMask','paintInk']
         .every(k=>String(_showProblem_mc).indexOf(k)>=0),
       ['syncTypeBtn','syncGptBtn','linkChip','fillLayerSel','setupMask','paintInk']
         .filter(k=>String(_showProblem_mc).indexOf(k)<0));
     {
       const withTy=(DATA.find(r=>typeOf(r[F.NO]).length)||[])[F.NO];
       const noTy=(DATA.find(r=>!typeOf(r[F.NO]).length)||[])[F.NO];
       let a='',b='';
       if(withTy!=null){await openView(withTy,[withTy]);await wait(1100);
         a=(document.getElementById('tType')||{}).style?document.getElementById('tType').style.cssText:'';closeView();await wait(140)}
       if(noTy!=null){await openView(noTy,[noTy]);await wait(1100);
         b=(document.getElementById('tGpt')&&document.getElementById('tType'))?document.getElementById('tType').style.cssText:'';closeView();await wait(140)}
       T('P-6 ★유형이 있는 문항과 없는 문항의 #tType 인라인 꼴이 다르다',withTy!=null&&noTy!=null&&a!==b,[withTy,a,noTy,b]);
     }
     /* 검색 — 옛 pass(1851) 와 전수 대조 */
     {
       const oldPass=(r,q)=>{const s2=q.toLowerCase();
         return (String(r[F.CODE]).toLowerCase().includes(s2)||String(r[F.SUB]).includes(q)||
                 String(r[F.BODY]).includes(q)||String(noteOf(r[F.NO])).includes(q)||
                 typeOf(r[F.NO]).some(t=>t===q)||String(gptOf(r[F.NO])).includes(q)||
                 String(r[F.NO])===q||String(r[F.VLT])===q)};
       const q0=FL.q, bad=[];
       const sub=(DATA.find(r=>r[F.SUB])||[])[F.SUB];
       const ty=(()=>{for(const r of DATA){const t=typeOf(r[F.NO]);if(t&&t.length)return t[0]}return null})();
       const vl=(DATA.find(r=>r[F.VLT])||[])[F.VLT];
       const qs=[String(sub||'').split(/[ ,]/)[0],ty,'15',String(vl||'')].filter(Boolean);
       /* ★ jagwa_search(9/29) — 검색은 목록을 안 거른다(A-1) → 걸린 집합 = 결과 상자의 번호(ES_NOS · 데이터 차례) · 한 글자는 찾지 않는다(A-1-3) · 옛 판은 목록 거름 그대로 */
       const inp=document.getElementById('q');
       qs.forEach(q=>{
         const b=DATA.filter(r=>oldPass(r,q)).map(r=>r[F.NO]).join(',');
         if(typeof esSearch==='function'){inp.value=q;esSearch();
           if(q.replace(/\s+/g,'').length<2){if(ES_NOS.length||txt(document.getElementById('qCnt'))!=='두 글자 이상 입력하세요')bad.push([q,'한 글자',ES_NOS.length])}
           else{const a=ES_NOS.join(',');if(a!==b){
             /* ★ physprev(10/1 하위 에이전트 C) — _task_jagwa_physprev A-2-3 「검색이 미리보기 t 도 본다」: 옛 집합 ⊆ 새 집합 · 더 걸린 문항이 모두 t 에서 걸린 것(pvHit)이면 뜻한 바뀜 */
             const A=new Set(ES_NOS),B=b?b.split(',').map(Number):[],ex=ES_NOS.filter(n=>B.indexOf(n)<0);
             const pvok=B.every(n=>A.has(n))&&ex.length>0&&typeof pvHit==='function'&&ex.every(n=>{const r=DATA.find(x=>x[F.NO]===n);return !!r&&pvHit(r,q)});
             if(!pvok)bad.push([q,ES_NOS.length,b.split(',').length])}}}
         else{FL.q=q;const a=DATA.filter(pass).map(r=>r[F.NO]).join(',');if(a!==b)bad.push([q,a.split(',').length,b.split(',').length])}});
       if(typeof esSearch==='function'){inp.value='';esSearch()}
       FL.q=q0; draw(); await wait(250);
       T('P-6 ★검색 집합이 옛 pass(1851)와 전수로 같다 — '+qs.join('·'),bad.length===0,bad);
     }
     /* 백업 키 */
     {
       const _cr=URL.createObjectURL; let capb=null;
       URL.createObjectURL=function(b){capb=b;return 'blob:x'};
       const _cl=HTMLAnchorElement.prototype.click; HTMLAnchorElement.prototype.click=function(){};
       try{await exportData(false)}catch(e){}
       URL.createObjectURL=_cr; HTMLAnchorElement.prototype.click=_cl;
       let ks=[]; try{ks=Object.keys(JSON.parse(await capb.text())).sort()}catch(e){}
       const want=['ansfix','at','conc','frm','gg','ggref','gpt','ink','maskpos','note','omrpos',
                   'qtype','set','status','subj','twin','v'];
       T('P-6 ★백업 키 = 앞 판 ∪ {gg,ggref,subj}',ks.join(',')===want.join(','),ks.join(','));
       T('P-6 물리 백업에 교재 묶음(card)이 없다',ks.indexOf('card')<0,ks.indexOf('card'));
     }
   });

   /* ══════════ P-7 — add6 §A 편 칩 이름 · §B 분류 · §C-3 메모 걷기 ══════════ */
   await grp('P', async()=>{
     FL.past='';FL.year='';FL.lv='';FL.star=false;FL.mark='';FL.bigs=[];FL.subs=[];
     draw(); await wait(500);
     const esh=document.getElementById('esh');
     const chipTx=()=>$$$('#eChs .chchip').map(b=>txt(b));
     T('P-7 ★편 칩 글자에 이름이 들어간다(add6 §A)',
       JSON.stringify(chipTx())===JSON.stringify(
         ["전체","1. 역학 195","2. 유체역학 14","3. 열역학 64","4. 파동·광학 71",
          "5. 전자기학 155","6. 현대물리학 78"]),chipTx());
     /* §B-1·§D-4 — 분류 칩이 히트맵 머리에 · 「확인문제」 0 */
     const kindTx=()=>$$$('#eKind .chchip').map(b=>txt(b));
     /* ★ add18 §A-1 — 「타기출」을 「기본」에 합쳐 **셋**이다(전체 = 기출 + 기본 · 사용자 9/21) */
     T('P-7 ★분류 칩 = 전체·기출·기본 **셋**(add18 §A-1 · 「타기출」을 합쳤다)',
       kindTx().length===3&&/^전체 \d+$/.test(kindTx()[0])&&/^기출 \d+$/.test(kindTx()[1])
       &&/^기본 \d+$/.test(kindTx()[2]),kindTx());
     T('P-7 ★분류 셋의 합 = 전체(기출 + 기본)',
       (()=>{const n=kindTx().map(x=>+((x.match(/(\d+)$/)||[0,0])[1]));
         return n[1]+n[2]===n[0]})(),kindTx());
     T('P-7 ★「타기출」 칩 0(add18 §A-1)',kindTx().join('').indexOf('타기출')<0,kindTx());
     T('P-7 ★「확인문제」 글자 0(§D-4)',kindTx().join('').indexOf('확인문제')<0,kindTx().join(' '));
     N('P-7 분류 셈',{전체:DATA.filter(showKind).length,
       기출:DATA.filter(r=>r[F.SRC]==='변리사').length,
       기본:DATA.filter(r=>!r[F.SRC]).length,
       어느쪽도아님:DATA.filter(r=>r[F.SRC]&&r[F.SRC]!=='변리사').length,
       그SRC:[...new Set(DATA.filter(r=>r[F.SRC]&&r[F.SRC]!=='변리사').map(r=>r[F.SRC]))]});
     /* §B-2·§D-2 — 누르면 목록과 히트맵이 **같이** 좁아진다 */
     const setOf=()=>filtered().map(r=>r[F.NO]).join(',');
     const cells=()=>$$$('#spec i:not(.gap)').length;
     const want=v=>DATA.filter(r=>showKind(r)
       &&(v==='y'?r[F.SRC]==='변리사'
        :v==='n'?r[F.SRC]!=='변리사':true)).map(r=>r[F.NO]).join(',');   /* ★ add18 §A-1 */
     for(const v of ['y','n','']){
       const b=esh.querySelector('#eKind [data-past="'+v+'"]');
       b.click(); await wait(500);
       const nList=filtered().length;
       T('P-7 ★분류 「'+(v==='y'?'기출':v==='n'?'기본':'전체')+'」 — 목록이 옛 pass 와 같다',
         setOf()===want(v),[nList,want(v).split(',').filter(Boolean).length]);
       T('P-7 ★그때 히트맵 칸 수 = 목록 수',cells()===nList,[cells(),nList]);
       T('P-7 그 칩만 켜져 있다',
         $$$('#eKind .chchip.on').length===1&&txt($$$('#eKind .chchip.on')[0]).indexOf(
           v==='y'?'기출':v==='n'?'기본':'전체')===0,
         $$$('#eKind .chchip.on').map(x=>txt(x)));
     }
     /* 편 ∩ 분류 */
     { esh.querySelector('#eKind [data-past="y"]').click(); await wait(400);
       const big=$$$('#eChs .chchip')[1]; big.click(); await wait(500);
       T('P-7 ★편 칩과 겹쳐 눌러도 칸 수 = 목록 수',cells()===filtered().length,
         [cells(),filtered().length,FL.bigs.slice()]);
       $$$('#eChs .chchip')[0].click(); await wait(400);
       esh.querySelector('#eKind [data-past=""]').click(); await wait(400); }
     /* §C-3 — 「메모 있음」·「코멘트」 걷기 · 🃏 무변 */
     T('P-7 ★「메모 있음」 단추 0(§C-3)',!esh.querySelector('#fMemo'),!!esh.querySelector('#fMemo'));
     { const tn=document.getElementById('tNote');
       const vis=tn?(tn.offsetParent!==null||getComputedStyle(tn).display!=='none'):false;
       T('P-7 ★「코멘트」 단추가 안 보인다(§C-3)',!vis,
         tn?getComputedStyle(tn).display:'(DOM 없음)'); }
     T('P-7 「🃏 전체 N」은 그대로 있다(갈 곳)',!!document.getElementById('mcAll'),
       txt(document.getElementById('mcAll')));
     /* §C-2 — note 는 죽은 키로 남아 있다 */
     T('P-7 ★`note` 가 SYNC_KEYS 에 죽은 키로 남아 있다(§C-2)',SYNC_KEYS.indexOf('note')>=0,
       SYNC_KEYS.indexOf('note'));
   });

   /* ══════════ P-8 — add8 📋 정리 창 ══════════ */
   await grp('P', async()=>{
     FL.past='';FL.year='';FL.lv='';FL.star=false;FL.mark='';FL.bigs=[];FL.subs=[];
     draw(); await wait(500);
     const secs=Object.keys(TOC.sec);
     T('P-8 절이 있다',secs.length>0,secs.length);
     const bad=[],empty=[],names=[];
     for(const sec of secs){
       jnOpen(sec); await wait(120);
       const w=document.getElementById('jnw');
       if(!w){bad.push([sec,'창이 안 뜸']);continue}
       const head=txt(w.querySelector('.bplh'));
       const mut=txt(w.querySelector('.bplh .mut'));
       names.push(mut.split(' · ')[0]);
       const rows=w.querySelectorAll('.jnrow').length;
       const none=w.querySelectorAll('.bplnone').length;
       const wantN=DATA.filter(r=>showKind(r)&&unitOf(r[F.NO])===sec).length;
       if(none)empty.push(sec);
       if(rows!==wantN)bad.push([sec,rows,wantN]);
       w.remove();
     }
     T('P-8 ★절마다 창 안 줄 수 = 그 절 문항 수(전수 '+secs.length+'절)',bad.length===0,bad.slice(0,5));
     T('P-8 ★「이 절에 든 문항이 없다」 0',empty.length===0,empty.slice(0,6));
     T('P-8 ★창 머리 과목 글자 = 그 과목 이름',
       [...new Set(names)].length===1&&[...new Set(names)][0]===CUR.NAME,
       [...new Set(names)]);
     /* §B-3 — 줄을 누르면 그 문항이 뷰어로 열린다 */
     { const sec=secs[0]; jnOpen(sec); await wait(200);
       const w=document.getElementById('jnw');
       const go=w.querySelector('.jnrow .jgo');
       const no=+go.dataset.go;
       go.click(); await wait(1400);
       T('P-8 ★창 줄을 누르면 그 문항이 뷰어로 열린다',VNO===no,[VNO,no]);
       const cv=document.getElementById('pdfc');
       T('P-8 그 뷰어에 그림이 그려졌다(add5 P-6)',
         !!cv&&cv.width>300&&cv.height>300,cv?[cv.width,cv.height]:'없음');
       closeView(); await wait(400);
       const w2=document.getElementById('jnw'); if(w2)w2.remove(); }
     /* §A-4 — 같은 가정을 깐 다른 창: 🃏 창 머리 과목 글자 */
     { const sc=(typeof mcScOf==='function')?null:null;
       const any=Object.keys(TOC.sec)[0];
       if(typeof mcwOpen==='function'){
         await mcwOpen('s:'+any); await wait(500);
         const w=document.getElementById('mcw');
         T('P-8 ★🃏 창 머리 과목 글자도 그 과목 이름(§A-4)',
           !!w&&txt(w.querySelector('.bplh .mut')).indexOf(CUR.NAME)===0,
           w?txt(w.querySelector('.bplh .mut')):'안 뜸');
         if(w)w.remove();
       } else T('P-8 ★🃏 창 머리 과목 글자도 그 과목 이름(§A-4)',false,'mcwOpen 없음'); }
   });

   /* ══════════ W-2~W-5 — add9 §A-4·§B·§C (물리) ══════════ */
   await grp('WD', async()=>{
     FL.past='';FL.year='';FL.lv='';FL.star=false;FL.mark='';FL.bigs=[];FL.subs=[];FL.q='';
     draw(); await wait(600);
     /* §D-2 줄 누름 → 팝업창 */
     const row=document.querySelector('#ndList .ndrow');
     const no=+row.dataset.no;
     row.click(); await wait(1600);
     T('WD-2 ★서랍 줄을 누르면 그 문항이 열린다',VNO===no,[VNO,no]);
     T('WD-2 ★팝업창(창 모드)이다',$('#view').classList.contains('win'),
       $('#view').className);
     { const cv=document.getElementById('pdfc');
       T('WD-2 그려진 픽셀이 있다(add5 P-6)',!!cv&&cv.width>300&&cv.height>300,
         cv?[cv.width,cv.height]:'없음'); }
     T('WD-2 ★그 줄이 강조된다',
       (()=>{const x=document.querySelector('#ndList .ndrow.cur');
         return !!x&&+x.dataset.no===no})(),
       (()=>{const x=document.querySelector('#ndList .ndrow.cur');
         return x?+x.dataset.no:'없음'})());
     { const nx=document.getElementById('vNext'); if(nx){nx.click(); await wait(1500);}
       T('WD-2 ★▶ 로 넘기면 강조가 따라간다',
         (()=>{const x=document.querySelector('#ndList .ndrow.cur');
           return !!x&&+x.dataset.no===VNO})(),
         (()=>{const x=document.querySelector('#ndList .ndrow.cur');
           return x?[+x.dataset.no,VNO]:'없음'})()); }
     /* §D-3 창 안에는 서랍·손잡이가 없다 */
     T('WD-3 ★창 안에 `#navTg`·`#navdr` 0',
       !document.querySelector('#view #navdr')&&!document.querySelector('#view #navTg'),
       [!!document.querySelector('#view #navdr'),!!document.querySelector('#view #navTg')]);
     /* §D-4 창 폭을 바꾸면 문제도 따라 커진다 */
     { const v=$('#view'), st=$('#stage'), cv=document.getElementById('pdfc');
       vzSet(1); await wait(500);
       v.style.width='600px'; v.style.height='700px'; await wait(900);
       const w600=parseFloat(getComputedStyle(cv).width), s600=st.clientWidth;
       v.style.width='1100px'; await wait(900);
       const w1100=parseFloat(getComputedStyle(cv).width), s1100=st.clientWidth;
       T('WD-4 ★창을 키우면 문제도 같이 커진다(창 폭−24 ±2px)',
         Math.abs(w1100-(s1100-24))<=2&&Math.abs(w600-(s600-24))<=2&&w1100>w600,
         [w600,s600-24,w1100,s1100-24]);
       T('WD-4 ★창 모드에서는 900px 상한이 없다',w1100>900,w1100);
       /* ★ add17 §A-1 로 단추를 걷었다 — 같은 것을 **손짓 길**(vzCommit)로 잰다.
          단추가 정말 없는지는 P-16 이 따로 잰다. */
       vzCommit(1.2,null); await wait(900);
       T('WD-4 ★배율을 1.2 로 올리면 120%(옛 「＋」 두 번 자리 · 단추는 걷었다)',
         Math.round(VWZ*100)===120,Math.round(VWZ*100));
       const w120=parseFloat(getComputedStyle(cv).width);
       T('WD-4 그때 문제도 1.2배다',Math.abs(w120-w1100*1.2)<=3,[w120,w1100*1.2]);
       vzCommit(1,null); await wait(900);
       T('WD-4 ★맞춤(배율 1) = 100%',Math.round(VWZ*100)===100,Math.round(VWZ*100));
       T('WD-4 배율을 기기에 남긴다',localStorage.getItem('jagwa.win.view.zoom')==='1',
         localStorage.getItem('jagwa.win.view.zoom'));
       /* §D-5 필기는 문제에 붙어 있다 */
       INK[LAYER]=INK[LAYER]||[];
       const st0={c:'#111',w:2,hl:0,p:[0.25,0.30,0.55,0.62]};
       INK[LAYER].push(st0); paintInk(); await wait(200);
       const keep=JSON.stringify(INK[LAYER].slice(-1)[0].p);
       const frac=()=>{const[x,y]=toPix(0.25,0.30);
         return [x/RENDER.W,y/RENDER.H]};
       const f100=frac();
       vzSet(1.5); await wait(900); const f150=frac();
       vzSet(0.7); await wait(900); const f70=frac();
       const same=JSON.stringify(INK[LAYER].slice(-1)[0].p)===keep;
       const near=(a,b)=>Math.abs(a[0]-b[0])<0.002&&Math.abs(a[1]-b[1])<0.002;
       T('WD-5 ★배율을 바꿔도 획 좌표가 안 바뀐다(쪽 기준 저장)',same,same?'':keep);
       T('WD-5 ★획이 문제의 같은 비율 자리에 선다(100% ↔ 150% ↔ 70%)',
         near(f100,f150)&&near(f100,f70),[f100,f150,f70]);
       T('WD-5 정답 가림·OMR 도 같은 길로 다시 그린다',
         String(vReflow).indexOf('setupMask')>=0&&String(vReflow).indexOf('layoutOmr')>=0,'');
       INK[LAYER].pop(); paintInk();
       vzSet(1); await wait(500);
       v.style.width='';v.style.height='';
     }
     /* 전체 화면 모드에서는 ▤ 가 남는다 */
     { vwApply(false); await wait(700);
       const tg=document.getElementById('navTg');
       T('WD-3 ★전체 화면 모드에서는 ▤ 가 보인다',
         !!tg&&getComputedStyle(tg).display!=='none',
         tg?getComputedStyle(tg).display:'없음');
       vwApply(true); await wait(500); }
     closeView(); await wait(600);
   });


   /* ══════════ P-9 (add10) · P-10 (add11) · P-11 (add12) · P-13 (add14) ══════════ */
   await grp('P', async()=>{
     /* ⚠ 이 하네스는 `GG={}` 로 비우고 시작한다(1611). 「표본이 없어 참」을 막으려면
        재는 것마다 **씨앗을 심어야** 한다 — 근거·연결·GPT. 값은 앱이 쓰는 통 그대로. */
     GG[GGU(rec(9))]=[{k:'g_t9',i:1,t:'근의공식때문 / 진행방향으로 속도줄면 반대방향 가속도(-a) v=0 최대거리. 이후 거리줄어듬',ok:null,ts:1788617056265,cs:[],src:'note'}];
     GG[GGU(rec(10))]=[{k:'g_t10',i:1,t:'평균속력개념',ok:null,ts:1788214011257,cs:[],src:'note'}];
     LK[9]=[10]; if(typeof GP!=='undefined')GP[11]='GPT 흉내';
     if(typeof ST!=='undefined'){ST[9]=ST[9]||{h:[{m:'O',t:Date.now()-9e5,s:81}]};
       ST[10]=ST[10]||{h:[{m:'Q',t:Date.now()-8e5,s:45},{m:'O',t:Date.now()-7e5,s:30}]}}
     FL.past='';FL.year='';FL.lv='';FL.star=false;FL.mark='';FL.bigs=[];FL.subs=[];FL.q='';
     draw(); await wait(700);

     /* ── P-11 (add12) 딱지·칩·코드 색 ───────────────────────────── */
     const byTag=lab=>[...document.querySelectorAll('#list .item')]
       .filter(x=>[...x.querySelectorAll('.meta .tag')].some(t=>txt(t)===lab)).length;
     const nG=DATA.filter(r=>r[F.SRC]==='변리사').length;
     const nT=DATA.filter(r=>r[F.SRC]&&r[F.SRC]!=='변리사').length;
     const nN=DATA.filter(r=>!r[F.SRC]).length;
     /* ★ 2026-10-07 (_task_jagwa_phys_win §A-36 ㊴) — 물리 목록 「기출」 칩 자리에 「V3」 글자(.vno · 지학·생물은 kindTag 그대로) = 뜻한 차
        → 새 꼴(.vno 가 선다) = 「기출」 딱지 0 · 딱지 없는 줄 = 전부 · 옛: byTag('기출')===nG · 옛: …length===nT+nN */
     const _vno=document.querySelectorAll('#list .item .meta .vno').length>0;
     T('P-11 ★「기출」 딱지 = 변리사 기출만',byTag('기출')===nG||(_vno&&byTag('기출')===0),[byTag('기출'),nG]);
     /* ★ add18 §A-2 — 「타기출」 딱지를 없앴다. 변리사만 「기출」 · 그 밖은 **딱지 없음** */
     T('P-11 ★「타기출」 딱지 0(add18 §A-2)',byTag('타기출')===0,[byTag('타기출'),nT]);
     T('P-11 ★딱지 없는 줄 = 변리사가 아닌 것 전부('+(nT+nN)+')',
       [...document.querySelectorAll('#list .item')]
         .filter(x=>![...x.querySelectorAll('.meta .tag')].some(t=>/^(기출|타기출|확인|예상)$/.test(txt(t)))).length===(_vno?nG+nT+nN:nT+nN),
       [[...document.querySelectorAll('#list .item')]
         .filter(x=>![...x.querySelectorAll('.meta .tag')].some(t=>/^(기출|타기출|확인|예상)$/.test(txt(t)))).length,nT+nN]);
     { /* 코드 글자 색 — 변리사만 초록 · 그 밖 회색 · 눈에 보일 만큼 다르다 */
       const lum=c=>{const m=/rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(c)||[0,0,0,0];
         return 0.299*+m[1]+0.587*+m[2]+0.114*+m[3]};
       const items=[...document.querySelectorAll('#list .item')];
       const col=x=>getComputedStyle(x.querySelector('.num')).color;
       const gs=new Set(), os=new Set();
       items.forEach(x=>{const n=+((x.dataset.no)||0)||null;
         const code=txt(x.querySelector('.num'));
         const r=DATA.find(rr=>codeShow(rr)===code);
         if(!r)return; (r[F.SRC]==='변리사'?gs:os).add(col(x))});
       T('P-11 ★변리사 기출 코드 색이 한 가지다',gs.size===1,[...gs]);
       T('P-11 ★그 밖 코드 색이 한 가지다',os.size===1,[...os]);
       T('P-11 ★두 색의 밝기 차 ≥ 25(눈에 보인다)',
         gs.size===1&&os.size===1&&Math.abs(lum([...gs][0])-lum([...os][0]))>=25,
         gs.size===1&&os.size===1?[Math.round(lum([...gs][0])),Math.round(lum([...os][0]))]:'?'); }

     /* ── P-10 (add11) 목록 줄에 되살린 표시 ──────────────────────── */
     { const has=(sel)=>[...document.querySelectorAll('#list .item')]
         .filter(x=>x.querySelector(sel)).length;
       const want={
         '난이도 tag.lv': ['.meta .tag[class*="lv"]', DATA.filter(r=>r[F.LV]).length],
         '볼트 N':        ['.meta .tag.vlt,.meta .vno',  DATA.filter(r=>r[F.VLT]).length],   /* ★ 2026-10-07 (_task_jagwa_phys_win §A-37 · §A-36 ㊴) — 물리 「볼트 N」 칩(.tag.vlt) 걷고 「기출」 칩 자리에 「V3」 글자(.vno) = 뜻한 차 → 둘 중 있는 쪽을 센다 · 옛: '.meta .tag.vlt' */
         '볼트 기록':      ['.meta .tag.vm',   null],
         '풀이':          ['.meta .tag.sol',  null],
         '🔗 N':          ['.meta .tag.lk',   null],
         'GPT':           ['.meta .tag.gp',   null],
         '유형':          ['.meta .tag.qt',   null],
         '★':             ['.meta .star',     DATA.filter(r=>r[F.STAR]).length]
       };
       const bad=[], zero=[];
       Object.keys(want).forEach(k=>{
         const [sel,n]=want[k], got=has(sel);
         if(n!==null&&got!==n)bad.push([k,got,n]);
         if(got===0)zero.push(k);
       });
       T('P-10 ★되살린 표시 수가 데이터와 같다(난이도·볼트·★)',bad.length===0,bad);
       /* ⚠ 「표본이 없어 참」 금지 — 여덟 가지마다 적어도 하나는 서야 한다 */
       T('P-10 ★여덟 가지가 모두 한 줄 이상에 선다(헛패스 금지)',zero.length===0,zero);
       T('P-10 제목 뒤에 LNO 가 붙는다',
         (()=>{const x=document.querySelector('#list .item .meta .sub');
           return !!x&&/ · \d+$/.test(txt(x))})(),
         txt(document.querySelector('#list .item .meta .sub')));
       /* 유형 확정 = 실선 · 초안 = 점선 */
       { const qt=[...document.querySelectorAll('#list .meta .tag.qt')];
         const fx=qt.filter(x=>!x.classList.contains('dr'));
         const dr=qt.filter(x=>x.classList.contains('dr'));
         T('P-10 ★유형 확정은 실선 · 초안은 점선',
           (!fx.length||getComputedStyle(fx[0]).borderStyle==='solid')
           &&(!dr.length||getComputedStyle(dr[0]).borderStyle==='dashed'),
           [fx.length,dr.length,fx.length?getComputedStyle(fx[0]).borderStyle:'-',
            dr.length?getComputedStyle(dr[0]).borderStyle:'-']); }
       /* 「🔗 N」 누름 = 연결 시트 */
       { const lk=document.querySelector('#list .meta .tag.lk');
         if(lk){ lk.click(); await wait(500);
           const sh=$$$('.sheet').filter(x=>!x.classList.contains('hide'));
           T('P-10 ★「🔗 N」 을 누르면 연결 시트가 뜬다(문항은 안 열린다)',
             sh.length>0&&$('#view').classList.contains('hide'),
             [sh.length,$('#view').className.slice(0,20)]);
           sh.forEach(x=>x.remove()); await wait(200); }
         else T('P-10 ★「🔗 N」 을 누르면 연결 시트가 뜬다(문항은 안 열린다)',false,'🔗 줄이 없다'); } }

     /* ── P-9 (add10) 고르개 칩 · 정리 창 근거·마크 ────────────────── */
     T('P-9 ★「★중요」·「모두 풀기」 칩 0',
       !document.getElementById('fStarBtn')&&!document.getElementById('fAllClr'),
       [!!document.getElementById('fStarBtn'),!!document.getElementById('fAllClr')]);
     T('P-9 ★`FL.star` 는 거짓이다',FL.star===false,FL.star);
     { /* 근거가 든 물리 문항 전수 — 정리 창 줄에 그 수만큼 보인다 */
       const withGG=DATA.filter(r=>ggOf(GGU(r)).length);
       T('P-9 근거가 든 물리 문항이 있다(헛패스 금지)',withGG.length>0,withGG.length);
       const secs=[...new Set(withGG.map(r=>unitOf(r[F.NO])))];
       const bad=[];
       for(const sec of secs){
         jnOpen(sec); await wait(150);
         const w=document.getElementById('jnw'); if(!w){bad.push([sec,'창 없음']);continue}
         withGG.filter(r=>unitOf(r[F.NO])===sec).forEach(r=>{
           const rw=[...w.querySelectorAll('.jnrow')].find(x=>+x.dataset.no===r[F.NO]);
           if(!rw){bad.push([r[F.NO],'줄 없음']);return}
           const n=rw.querySelectorAll('.ggmine>div').length;
           if(n!==ggOf(GGU(r)).length)bad.push([r[F.NO],n,ggOf(GGU(r)).length]);
         });
         w.remove();
       }
       T('P-9 ★정리 창 줄의 근거 수 = ggOf(GGU(r)) (전수)',bad.length===0,bad.slice(0,4));
       /* 되살린 코멘트가 보인다 */
       { const r9=rec(9); jnOpen(unitOf(9)); await wait(200);
         const w=document.getElementById('jnw');
         const rw=w?[...w.querySelectorAll('.jnrow')].find(x=>+x.dataset.no===9):null;
         T('P-9 ★9번 줄에 되살린 코멘트 글자가 보인다',
           !!rw&&/근의공식/.test(txt(rw)),rw?txt(rw).slice(0,40):'줄 없음');
         if(w)w.remove(); } }
     { /* 마크 묶음이 첫 화면 줄과 같다 */
       const done=DATA.filter(r=>hist(r[F.NO]).length);
       T('P-9 기록이 있는 물리 문항이 있다(헛패스 금지)',done.length>0,done.length);
       const bad=[];
       const secs=[...new Set(done.map(r=>unitOf(r[F.NO])))].slice(0,6);
       for(const sec of secs){
         jnOpen(sec); await wait(150);
         const w=document.getElementById('jnw'); if(!w)continue;
         done.filter(r=>unitOf(r[F.NO])===sec).forEach(r=>{
           const rw=[...w.querySelectorAll('.jnrow')].find(x=>+x.dataset.no===r[F.NO]);
           if(!rw)return;
           const a=(rw.querySelector('.mk')||{}).innerHTML||'';
           const b=(()=>{const d=document.createElement('div');d.innerHTML=markBadge(r[F.NO]);
             return (d.querySelector('.mk')||{}).innerHTML||''})();
           if(a!==b)bad.push([r[F.NO],a.slice(0,40),b.slice(0,40)]);
         });
         w.remove();
       }
       T('P-9 ★정리 창 마크 묶음 = 첫 화면 `markBadge` 와 같다',bad.length===0,bad.slice(0,3)); }

     /* ── P-13 (add14) 📋 창이 분류 칩을 따른다 ────────────────────── */
     { const esh=document.getElementById('esh');
       const bad=[];
       for(const v of ['','y','n']){                       /* ★ add18 §A-1 — 분류가 셋이다 */
         esh.querySelector('#eKind [data-past="'+v+'"]').click(); await wait(600);
         const secs=Object.keys(TOC.sec).slice(0,20);
         for(const sec of secs){
           const want=DATA.filter(r=>showKind(r)&&phPast(r)&&unitOf(r[F.NO])===sec).length;
           jnOpen(sec); await wait(90);
           const w=document.getElementById('jnw'); if(!w){bad.push([v,sec,'창 없음']);continue}
           const got=w.querySelectorAll('.jnrow').length;
           const hd=txt(w.querySelector('.bplh .mut'));
           if(got!==want)bad.push([v,sec,got,want]);
           if(hd.indexOf(String(want)+'문항')<0)bad.push([v,sec,'머리',hd]);
           w.remove();
         }
       }
       T('P-13 ★분류 셋 × 절 스무 곳 — 창 줄 수·머리 수 = 그 분류의 문항 수',
         bad.length===0,bad.slice(0,4));
       esh.querySelector('#eKind [data-past="y"]').click(); await wait(600);
       { const sec=Object.keys(TOC.sec)[0];
         const want=DATA.filter(r=>showKind(r)&&phPast(r)&&unitOf(r[F.NO])===sec).length;
         FL.lv='상'; draw(); await wait(500);
         jnOpen(sec); await wait(150);
         const w=document.getElementById('jnw');
         T('P-13 ★연도·난이도 고르개는 📋 창에 안 먹인다(§A-2)',
           !!w&&w.querySelectorAll('.jnrow').length===want,
           [w?w.querySelectorAll('.jnrow').length:'없음',want]);
         if(w)w.remove(); FL.lv=''; }
       esh.querySelector('#eKind [data-past=""]').click(); await wait(600); }
   });

   /* ══════════ P-15 (add16) — 「보는 시트」가 떠 있는 창이다 ══════════ */
   await grp('P', async()=>{
     await openView(DATA[0][F.NO]); await wait(1200);
     const PE2=(t,x,y)=>{const e=new Event(t,{bubbles:true,cancelable:true});
       Object.defineProperties(e,{clientX:{get:()=>x},clientY:{get:()=>y},
         pointerId:{get:()=>7},pointerType:{get:()=>'mouse'},isPrimary:{get:()=>true},
         button:{get:()=>0},buttons:{get:()=>1}});return e};
     const kill=()=>$$$('body>.sheet').forEach(x=>x.remove());
     const tryOpen=(fn)=>{
       kill();
       const f=window[fn]; if(typeof f!=='function')return null;
       for(const args of [[],[VNO],[rec(VNO)]]){
         try{ f.apply(null,args); }catch(e){}
         const b=document.querySelector('body>.sheet');
         if(b)return b;
       }
       return null;
     };
     const opened=[], missed=[], bad=[];
     for(const [fn,key] of SHWIN){
       const b=tryOpen(fn);
       if(!b){missed.push(fn);continue}
       opened.push(fn);
       /* 덮개가 없다(모달이 아니다) */
       const bg=getComputedStyle(b).backgroundColor;
       if(!/rgba\(0,\s*0,\s*0,\s*0\)|transparent/.test(bg)||getComputedStyle(b).pointerEvents!=='none')
         bad.push([fn,'덮개',bg,getComputedStyle(b).pointerEvents]);
       const p=b.querySelector('.panel');
       if(!p||!p.classList.contains('float')){bad.push([fn,'float 아님']);kill();continue}
       if(!b.querySelector('.shx'))bad.push([fn,'✕ 없음']);
       if(!b.querySelector('.twgrip'))bad.push([fn,'모서리 손잡이 없음']);
       kill();
     }
     T('P-15 ★열린 창마다 떠 있는 창 규칙을 지킨다(덮개 0·float·✕·모서리)',bad.length===0,bad.slice(0,4));
     T('P-15 ★열린 창이 여섯 이상이다(헛패스 금지)',opened.length>=6,[opened.length,opened]);
     N('P-15 못 연 창(하네스에 자료가 없다)',missed);

     /* 「정답」 창으로 끌기·크기·다시 열기를 잰다(자료 없이 늘 열린다) */
     { kill(); ansSheet(); await wait(300);
       let b=document.getElementById('sh-ans'), p=b.querySelector('.panel');
       const h=p.querySelector('h2');
       const r0=p.getBoundingClientRect();
       /* ★ 합치기 10/1(하위 에이전트 C) — revfix0928 A-2(fb47074) · fix1 A-2(cb56419 본문 「문제 창 오른쪽에 자리가 없으면 … 화면 오른쪽 끝(l = 폭 − w − 8)」) —
          곁창 첫 자리가 화면 오른쪽 끝이면 +120 은 화면 끝에 막힌다(8 만 움직임) → 오른쪽에 120 자리가 없으면 왼쪽으로 120 끈다(움직인 만큼 재는 잣대는 그대로) */
       const dx=(r0.right+120<=innerWidth-8)?120:-120;
       h.dispatchEvent(PE2('pointerdown',r0.left+40,r0.top+8));
       h.dispatchEvent(PE2('pointermove',r0.left+40+dx,r0.top+88));
       h.dispatchEvent(PE2('pointerup',r0.left+40+dx,r0.top+88));
       await wait(120);
       const r1=p.getBoundingClientRect();
       T('P-15 ★제목 줄을 끌면 창이 그만큼 움직인다(+120,+80)(★ 첫 자리가 화면 오른쪽 끝이면 −120)',
         Math.abs(r1.left-r0.left-dx)<3&&Math.abs(r1.top-r0.top-80)<3,
         [Math.round(r1.left-r0.left),Math.round(r1.top-r0.top),dx]);
       const g=p.querySelector('.twgrip'), rg=g.getBoundingClientRect();
       g.dispatchEvent(PE2('pointerdown',rg.left+3,rg.top+3));
       g.dispatchEvent(PE2('pointermove',rg.left+203,rg.top+153));
       g.dispatchEvent(PE2('pointerup',rg.left+203,rg.top+153));
       await wait(120);
       const r2=p.getBoundingClientRect();
       T('P-15 ★모서리를 끌면 크기가 그만큼 는다(+200,+150)',
         Math.abs(r2.width-r1.width-200)<3&&Math.abs(r2.height-r1.height-150)<3,
         [Math.round(r2.width-r1.width),Math.round(r2.height-r1.height)]);
       const want=[Math.round(r2.left),Math.round(r2.top),Math.round(r2.width),Math.round(r2.height)];
       b.remove(); await wait(120);
       ansSheet(); await wait(300);
       b=document.getElementById('sh-ans'); p=b.querySelector('.panel');
       const r3=p.getBoundingClientRect();
       T('P-15 ★닫고 다시 열면 같은 자리·크기',
         Math.abs(r3.left-want[0])<3&&Math.abs(r3.top-want[1])<3
         &&Math.abs(r3.width-want[2])<3&&Math.abs(r3.height-want[3])<3,
         [[Math.round(r3.left),Math.round(r3.top),Math.round(r3.width),Math.round(r3.height)],want]);
       /* §B-3 두 번 열어도 하나 */
       ansSheet(); await wait(250); ansSheet(); await wait(250);
       T('P-15 ★같은 창을 두 번 열어도 DOM 에 하나',
         document.querySelectorAll('#sh-ans').length===1,
         document.querySelectorAll('#sh-ans').length);
       /* §B-2 창을 연 채 뒤의 문제 창이 살아 있다 */
       /* ⚠ 창은 끌어 옮긴 자리에 있다 — **창이 안 덮은 점**을 골라 재야 한다.
          덮개가 막는지를 보는 것이지 창 밑을 보는 것이 아니다. */
       { const cv=document.getElementById('inkc');
         /* ⚠ 앞 묶음이 열어 둔 **다른 떠 있는 창**도 덮을 수 있다 — 전부 비켜서 고른다 */
         const rects=[...document.querySelectorAll('.sheet .panel.float,.sheet.shfloat>.panel')]
           .map(x=>x.getBoundingClientRect());
         const rr=cv?cv.getBoundingClientRect():null;
         let pt=null;
         if(rr)for(let fx=0.05;fx<=0.95&&!pt;fx+=0.05)for(let fy=0.05;fy<=0.95&&!pt;fy+=0.05){
           const x=rr.left+rr.width*fx, y=rr.top+rr.height*fy;
           if(x<0||y<0||x>innerWidth||y>innerHeight)continue;
           if(rects.some(q=>x>=q.left&&x<=q.right&&y>=q.top&&y<=q.bottom))continue;
           pt=[x,y];
         }
         const hit=pt?document.elementFromPoint(pt[0],pt[1]):null;
         T('P-15 ★창을 연 채로도 뒤의 문제 창이 눌린다(덮개가 안 막는다)',
           !!hit&&!hit.closest('.sheet'),
           hit?(hit.id||hit.className):(pt?'null':'창 밖 점을 못 찾음')); }
       /* §A-2 문항을 넘기면 문항에 매인 창은 닫힌다 */
       { const nx=document.getElementById('vNext'); if(nx){nx.click(); await wait(1500);}
         T('P-15 ★▶ 로 넘기면 문항에 매인 창은 닫힌다(§A-2 의 고른 갈래)',
           !document.getElementById('sh-ans'),!!document.getElementById('sh-ans')); }
       kill(); }

     /* §B-4 확인 창은 모달 그대로 */
     { kill();
       let n=0, bad2=[];
       for(const fn of ['eraseSheet','showSyncHelp']){
         const f=window[fn]; if(typeof f!=='function')continue;
         try{f()}catch(e){}
         const b=document.querySelector('body>.sheet'); if(!b)continue;
         n++;
         const bg=getComputedStyle(b).backgroundColor;
         if(b.classList.contains('shfloat')||/rgba\(0,\s*0,\s*0,\s*0\)/.test(bg))bad2.push([fn,bg]);
         kill();
       }
       T('P-15 ★확인 창은 여전히 모달이다(덮개 있음)',n>0&&bad2.length===0,[n,bad2]); }
     closeView(); await wait(500);
   });








   /* ══════════ W-1 — add9 §A 첫 화면 상주 서랍(세 과목 공통) ══════════ */
   await grp('WD', async()=>{
     FL.past='';FL.year='';FL.lv='';FL.star=false;FL.mark='';FL.bigs=[];FL.subs=[];FL.q='';
     draw(); await wait(600);
     T('WD-1 ★「목차」 단추(#btnTree)가 없다',!document.getElementById('btnTree'),
       !!document.getElementById('btnTree'));
     const dr=document.getElementById('navdr');
     T('WD-1 ★서랍이 첫 화면에 늘 서 있다',
       !!dr&&!dr.classList.contains('hide')&&dr.getBoundingClientRect().width>0,
       dr?[dr.className,Math.round(dr.getBoundingClientRect().width)]:'없음');
     T('WD-1 ★서랍이 `#view` 밖으로 나왔다(창 안에 안 남는다 · §B)',
       !!dr&&!document.querySelector('#view #navdr')&&!document.querySelector('#view #navTg'),
       [!!document.querySelector('#view #navdr'),!!document.querySelector('#view #navTg')]);
     { const lib=document.getElementById('lib');
       const a=dr?dr.getBoundingClientRect():null, b=lib?lib.getBoundingClientRect():null;
       T('WD-1 ★본문과 안 겹친다(서랍 오른끝 ≤ 본문 왼끝)',
         !!a&&!!b&&a.right<=b.left+1,[a?Math.round(a.right):'-',b?Math.round(b.left):'-']); }
     { const l=document.getElementById('ndList');
       const nos=(typeof navList==='function')?navList():[];
       let ok2=0; nos.forEach(n=>{if(rec(n))ok2++});
       try{navBuild()}catch(e){}
       N('진단 navBuild 속',{nos:nos.length,rec성공:ok2,
         ndList부모:l?(l.parentNode?(l.parentNode.id||l.parentNode.className||l.parentNode.tagName):'없음'):'#ndList 없음',
         ndList아이:l?l.childNodes.length:'-',
         navdr부모:(()=>{const d=document.getElementById('navdr');
           return d&&d.parentNode?(d.parentNode.id||d.parentNode.tagName):'-'})(),
         같은l:l===document.getElementById('ndList')}); }
     const nRow=()=>document.querySelectorAll('#ndList .ndrow').length;
     const nSec=()=>document.querySelectorAll('#ndList .ndsec').length;
     T('WD-1 ★서랍 줄 수 = 첫 화면 목록 문항 수',nRow()===filtered().length,[nRow(),filtered().length]);
     T('WD-1 단원 머리 줄이 있다(옛 「목차」 구실)',nSec()>0,nSec());
     T('WD-1 단원 머리 줄에 마지막 마크 점·문항 수가 있다',
       (()=>{const h=document.querySelector('#ndList .ndsec');
         return !!h&&!!h.querySelector('.dot')&&!!h.querySelector('.n')})(),
       (()=>{const h=document.querySelector('#ndList .ndsec');return h?txt(h).slice(0,24):'없음'})());
     /* 편 칩·검색을 바꾸면 같이 바뀐다 */
     { const before=nRow();
       const big=$$$('#eChs .chchip')[1]; if(big){big.click(); await wait(600);}
       T('WD-1 ★편 칩을 바꾸면 서랍도 같이 좁아진다',nRow()===filtered().length&&nRow()<before,
         [before,nRow(),filtered().length]);
       $$$('#eChs .chchip')[0].click(); await wait(500); }
     { const q=document.getElementById('q');
       if(q){ q.value='운동'; q.dispatchEvent(new Event('input',{bubbles:true})); await wait(700);
         T('WD-1 ★검색을 걸면 서랍도 같이 좁아진다',nRow()===filtered().length,[nRow(),filtered().length]);
         q.value=''; q.dispatchEvent(new Event('input',{bubbles:true})); await wait(600); }
       else T('WD-1 ★검색을 걸면 서랍도 같이 좁아진다',false,'#q 없음'); }
     T('WD-1 서랍 줄 글자 = 코드+난이도-제목',
       (()=>{const r0=document.querySelector('#ndList .ndrow');if(!r0)return false;
         const t2=txt(r0.querySelector('.ndt'));return t2.length>0&&t2.indexOf('undefined')<0})(),
       (()=>{const r0=document.querySelector('#ndList .ndrow');
         return r0?txt(r0.querySelector('.ndt')).slice(0,30):'없음'})());
     /* §A-6 옛 목차 서랍은 안 뜬다 */
     T('WD-1 ★옛 목차 서랍(#tree)이 안 뜬다',
       (()=>{try{treeOpen()}catch(e){}const t=document.getElementById('tree');
         return !t||t.classList.contains('hide')})(),'');
     T('WD-1 #trTog 가 상주 서랍 머리로 갔다(카드 층) · 물리는 숨음',
       (()=>{const t=document.getElementById('trTog');
         if(!t)return true;
         return !!t.closest('#navdr')||getComputedStyle(t).display==='none'})(),
       (()=>{const t=document.getElementById('trTog');
         return t?[!!t.closest('#navdr'),getComputedStyle(t).display]:'없음'})());
     /* §D-6 좁은 화면 규칙(소스·CSS 로 잰다 — 하네스 창은 1500px 이다) */
     T('WD-1 좁은 화면은 접힌 채 시작한다(규칙)',
       String(ndResident).indexOf('window.innerWidth<900')>=0,'');
   });

   /* ★ 9/28 penfinger_add2 회귀 — E-1 도 X-11 처럼 시험지 받기·기록 동기화가 끝난 뒤 찍는다(한 판만 동기화가 끝나
      「6회독↔5회독」「안 품 286·맞음 27 ↔ 안 품 318·맞음 1」이 갈렸다 — 같은 판을 다시 돌리면 PASS · 판 탓 아님) */
   await until(()=>{const b=document.getElementById('dl');return !b||b.classList.contains('hide')||!/받는 중/.test(b.textContent||'')},60000);
   await until(()=>typeof recBusy==='undefined'||!recBusy,60000);
   try{if(typeof syncRecords==='function')await Promise.race([syncRecords(true),wait(60000)])}catch(e){}
   await until(()=>typeof recBusy==='undefined'||!recBusy,60000);
   draw(); await wait(600);
   snap.cnt=String($('#cnt').textContent||'');
   snap.list=$$$('#list .item').slice(0,25).map(el=>String(el.textContent||'').replace(/\s+/g,' ').trim()).join(' || ');
   snap.hd=$$$('#list .grouphd').slice(0,8).map(el=>String(el.textContent||'').replace(/\s+/g,' ').trim()).join(' || ');
   snap.spec=$$$('#spec i').length+'/'+$$$('#spec i.gap').length;
   snap.esh=String(((document.getElementById('esh')||{}).textContent)||'').replace(/\s+/g,' ').trim().slice(0,200);
   try{await __nativeFetch('/snap',{method:'POST',body:JSON.stringify(snap)})}catch(e){}

   /* 스냅샷 뒤로 옮겼다 — NEW 쪽만 회독이 늘어 거짓 회귀가 나던 자리(2026-09-21) */
   /* ══════════ P-16 (add17) — 확대 단추 걷기 · 손짓 · 처음부터 창으로 · P ══════════ */
   await grp('P-16', async()=>{
     T('P-16 ★확대 단추 묶음이 없다(#vzWrap·#vzOut·#vzPct·#vzIn·#vzFit 0)',
       ['vzWrap','vzOut','vzPct','vzIn','vzFit'].every(i=>!document.getElementById(i)),
       ['vzWrap','vzOut','vzPct','vzIn','vzFit'].filter(i=>!!document.getElementById(i)));
     try{localStorage.setItem('jagwa.view.win','1')}catch(e){}
     const NO=DATA[0][F.NO];
     closeView(); await wait(250);
     await openView(NO); await wait(1400);
     T('P-16 창 모드로 열렸다(#view.win)',vWin(),$('#view').className);
     const st=document.getElementById('stage'), wr=document.getElementById('wrap'), pc=document.getElementById('pdfc');
     T('P-16 재는 자리가 있다(#stage·#wrap·#pdfc)',!!st&&!!wr&&!!pc);
     if(!st||!wr||!pc)return;

     /* ── Ctrl+휠 세 번 → 폭이 커지고 커서 아래 점이 제자리 ── */
     const wheelAt=(x,y,dy,ctrl)=>st.dispatchEvent(new WheelEvent('wheel',
       {bubbles:true,cancelable:true,ctrlKey:!!ctrl,deltaY:dy,clientX:x,clientY:y}));
     vzCommit(1.5,null); await wait(1400);          /* 먼저 넘치게 해 둔다 — 아래 축 보정이 잘리지 않게 */
     const W0=Math.round(wr.getBoundingClientRect().width), Z0=VWZ;
     {const r=wr.getBoundingClientRect();
      const fx=0.4, focX=r.left+r.width*fx, focY=r.top+60;
      wheelAt(focX,focY,-100,true); wheelAt(focX,focY,-100,true); wheelAt(focX,focY,-100,true);
      await wait(1400);
      const r2=wr.getBoundingClientRect(), W1=Math.round(r2.width);
      T('P-16 ★Ctrl+휠 위로 세 번 → 폭이 커진다(1.1^3 ≒ 1.33배 · '+W0+'→'+W1+' · 배율 '+Z0+'→'+VWZ+')',
        VWZ>Z0*1.2&&W1>W0*1.2&&Math.abs(W1/W0-VWZ/Z0)<0.06,[W0,W1,Z0,VWZ]);
      const nowX=r2.left+fx*r2.width;
      T('P-16 ★커서 아래 문제 점이 ±3px 안에 머문다(가로 · 넘침 '+(Math.round(st.scrollWidth-st.clientWidth))+'px)',
        Math.abs(nowX-focX)<3.5,[Math.round(focX),Math.round(nowX),Math.round(st.scrollLeft)]);
      /* 그냥 휠 = 확대가 아니다(브라우저 스크롤 몫 — 합성 휠은 헤드리스에서 굴리지 않는다) */
      const zB=VWZ, wB=Math.round(wr.getBoundingClientRect().width);
      const ev=new WheelEvent('wheel',{bubbles:true,cancelable:true,deltaY:-100,clientX:focX,clientY:focY});
      st.dispatchEvent(ev); await wait(500);
      T('P-16 ★그냥 휠은 폭·배율을 안 바꾼다(막지도 않는다 — 스크롤은 브라우저 몫)',
        VWZ===zB&&Math.round(wr.getBoundingClientRect().width)===wB&&ev.defaultPrevented===false,
        [zB,VWZ,wB,Math.round(wr.getBoundingClientRect().width),ev.defaultPrevented]);
     }

     /* ── 두 손가락 핀치 1 → 1.5 ── */
     {vzCommit(1,null); await wait(1200);
      const wA=Math.round(wr.getBoundingClientRect().width);
      const r=st.getBoundingClientRect(), cy=r.top+r.height/2, cx=r.left+r.width/2;
      const PE=(t,x,y,id)=>{const e=new Event(t,{bubbles:true,cancelable:true});
        Object.defineProperties(e,{clientX:{get:()=>x},clientY:{get:()=>y},
          pointerId:{get:()=>id},pointerType:{get:()=>'touch'},isPrimary:{get:()=>id===41},
          button:{get:()=>0},buttons:{get:()=>1}});st.dispatchEvent(e);return e};
      const seen={down:0,move:0};
      st.addEventListener('pointerdown',()=>seen.down++,true);
      st.addEventListener('pointermove',()=>seen.move++,true);
      PE('pointerdown',cx-50,cy,41); PE('pointerdown',cx+50,cy,42);      /* 거리 100 */
      PE('pointermove',cx-75,cy,41); PE('pointermove',cx+75,cy,42);      /* 거리 150 = 1.5배 */
      await wait(120);
      const wMid=Math.round(wr.getBoundingClientRect().width);
      const tfMid=wr.style.transform||'';
      N('P-16 핀치 진단',{닿은수:seen,미리보기변형:tfMid,창모드:vWin(),중간폭:wMid,배율:VWZ});
      PE('pointerup',cx-75,cy,41); PE('pointerup',cx+75,cy,42);
      await wait(1400);
      const wB=Math.round(wr.getBoundingClientRect().width);
      T('P-16 ★두 손가락 1 → 1.5 배 → 폭 1.5배(±2%) · 배율 '+VWZ+' · 손짓 중 미리보기 '+(tfMid||'없음'),
        Math.abs(VWZ-1.5)<0.03&&Math.abs(wB/wA-1.5)<0.02,[wA,wMid,wB,VWZ,tfMid,seen]);
      const cv=pc.getBoundingClientRect();
      T('P-16 ★손을 뗀 뒤 캔버스가 **새 폭에 맞게 다시 그려졌다**(CSS 변형 0 · 캔버스 실해상도 = 새 폭)',
        (wr.style.transform||'')===''&&pc.width>0&&Math.abs(Math.round(cv.width)-wB)<=2,
        [wr.style.transform,pc.width,Math.round(cv.width),wB]);
     }

     /* ── 두 번 톡 = 맞춤 · 펜일 때는 확대 아님 ── */
     {const mode0=TOOL.mode; TOOL.mode='view';
      st.dispatchEvent(new MouseEvent('dblclick',{bubbles:true,cancelable:true,
        clientX:st.getBoundingClientRect().left+80,clientY:st.getBoundingClientRect().top+80}));
      await wait(1300);
      T('P-16 ★두 번 톡(도구 = 손) → 맞춤(배율 1)',Math.abs(VWZ-1)<0.005,VWZ);
      vzCommit(1.4,null); await wait(1200);
      const zP=VWZ; TOOL.mode='pen';
      st.dispatchEvent(new MouseEvent('dblclick',{bubbles:true,cancelable:true,
        clientX:st.getBoundingClientRect().left+80,clientY:st.getBoundingClientRect().top+80}));
      await wait(700);
      T('P-16 ★펜·형광·지우개일 때 두 번 톡은 확대가 아니다(필기가 이긴다)',VWZ===zP,[zP,VWZ]);
      TOOL.mode=mode0; vzCommit(1,null); await wait(1200);
     }

     /* ── 튐 없음 — 여는 동안 #view 가 기억된 창 폭을 안 넘는다(네 길) ── */
     {const paths=[];
      const watch=async(label,fn)=>{
        closeView(); await wait(400);
        const want=(WIN&&WIN.view)?Math.round(WIN.view.w):0;
        let mx=0,fr=0,stop=false;
        const tick=()=>{if(stop)return;
          const v=document.getElementById('view');
          if(v&&!v.classList.contains('hide')){const r=v.getBoundingClientRect();
            if(r.width>0){mx=Math.max(mx,Math.round(r.width));fr++}}
          requestAnimationFrame(tick)};
        requestAnimationFrame(tick);
        await fn(); await wait(1200); stop=true;
        paths.push([label,mx,want,fr]);
      };
      await watch('목록 줄',async()=>{const el=$$$('#list .item')[0]; if(el)el.click(); await wait(900)});
      await watch('서랍 줄',async()=>{const el=$$$('#ndList .ndrow')[0]; if(el)el.click(); await wait(900)});
      await watch('쌍둥이(한 문항 목록)',async()=>{await openView(DATA[2][F.NO],[DATA[2][F.NO]])});
      /* ▶ 는 창이 이미 떠 있는 채로 넘긴다 — 전체 화면으로 돌아가면 안 된다 */
      await openView(DATA[4][F.NO]); await wait(1200);
      {const want=(WIN&&WIN.view)?Math.round(WIN.view.w):0;let mx=0,fr=0,stop=false;
       const tick=()=>{if(stop)return;const v=document.getElementById('view');
         if(v&&!v.classList.contains('hide')){const r=v.getBoundingClientRect();if(r.width>0){mx=Math.max(mx,Math.round(r.width));fr++}}
         requestAnimationFrame(tick)};
       requestAnimationFrame(tick); go(1); await wait(1500); stop=true;
       paths.push(['▶ 넘기기',mx,want,fr])}
      const bad=paths.filter(p=>!(p[3]>3&&p[1]<=p[2]+2));
      T('P-16 ★여는 동안 전체 화면 프레임 0 — 네 길 모두(잰 프레임 '+paths.map(p=>p[3]).join('·')+')',
        bad.length===0&&paths.length===4,paths);
      N('P-16 길마다 [이름, 가장 넓었던 #view, 기억된 창 폭, 잰 프레임]',paths);
     }

     /* ── 「P」 — 먹색 바탕·흰 글자 ── */
     {await openView(DATA[0][F.NO]); await wait(1200);
      const mp=document.getElementById('mP'), cs=mp?getComputedStyle(mp):null;
      T('P-16 ★「P」 = 먹색 바탕(--ink rgb(22,24,27))·흰 글자',
        !!cs&&cs.backgroundColor==='rgb(22, 24, 27)'&&cs.color==='rgb(255, 255, 255)',
        cs?[cs.backgroundColor,cs.color,cs.borderTopColor]:'없음');
      const others=['mO','mQ','mX'].map(i=>{const e=document.getElementById(i);return e?getComputedStyle(e).backgroundColor:'없음'});
      T('P-16 「O·△·X」는 무변(흰 바탕)',others.every(c=>c==='rgb(255, 255, 255)'),others);
      /* 가로로 밀어도(add15 고정) 그대로 */
      const row1=document.getElementById('pRow1');
      if(row1){row1.scrollLeft=300; await wait(200);
        const cs2=getComputedStyle(mp), over=row1.scrollWidth-row1.clientWidth;
        T('P-16 가로로 밀어도 「P」 바탕 그대로(add15 sticky 무접촉 · 넘침 '+over+'px · 민 자리 '+row1.scrollLeft+')',
          cs2.backgroundColor==='rgb(22, 24, 27)'&&getComputedStyle(mp).position==='sticky',
          [cs2.backgroundColor,getComputedStyle(mp).position,over,row1.scrollLeft]);
        row1.scrollLeft=0}
     }
     closeView(); await wait(400);
   });

   /* ══════════ SQ (add19) — 물리 서랍 차례 = 첫 화면 차례(무변) ══════════ */
   await grp('SQ', async()=>{
     try{collSet().clear();collSave()}catch(e){}
     FL.past='';FL.bigs=[];FL.subs=[];FL.unit='';FL.round='';FL.mark='';FL.q='';
     draw(); await wait(900);
     try{navBuild()}catch(e){}
     await wait(300);
     const first=$$$('#list .item').map(el=>txt(el.querySelector('.num')));
     const drw=$$$('#ndList .ndrow').map(el=>{const r=rec(+el.dataset.no);return r?codeShow(r):'?'});
     T('SQ 물리 ★서랍 코드 열 = 첫 화면 코드 열(전수 '+first.length+'/'+drw.length+')',
       first.length>500&&first.join('|')===drw.join('|'),
       {n:[first.length,drw.length],
        diff:first.map((x,i)=>[i,x,drw[i]]).filter(a=>a[1]!==a[2]).slice(0,4)});
     const old=filtered().map(r=>codeShow(r));
     T('SQ 물리 — 데이터 차례(filtered() 그대로)도 같다(그래서 물리는 바탕 판과 **무변**이다)',
       old.join('|')===drw.join('|'),
       {n:[old.length,drw.length],diff:old.map((x,i)=>[i,x,drw[i]]).filter(a=>a[1]!==a[2]).slice(0,4)});
     const hdF=$$$('#list .grouphd[data-uhd]').length, hdD=$$$('#ndList .ndsec').length;
     T('SQ 물리 서랍 단원 머리 수 = 첫 화면 단원 머리 수('+hdF+'/'+hdD+')',hdF>0&&hdF===hdD,[hdF,hdD]);
   });

"""

BODY_X = r"""
   /* ═══════════ X — _task_jagwa_earth_bookwin §L (2026-09-24) ═══════════
      바탕 판(24f1a373)에서 돌리면 헛잣대 — 새 기능이 없어 FAIL 해야 한다(main 이 센다). */
   await (async()=>{for(let __i=0;__i<300&&(typeof db==='undefined'||!db);__i++)await new Promise(r=>setTimeout(r,100));return loadEarthData()})()/* ★ 2026-10-08 (_task_jagwa_phys_win 회귀) db 가 설 때까지 — 고정 대기 경합(짐 크면 「db 없음」) · 판정 무변 */;
   await until(()=>DATA.length===704,30000);
   ['jagwa.earth.order','jagwa.earth.coll','jagwa.earth.hmfold','jagwa.view.win',
    'jagwa.win.view','jagwa.win.book','jagwa.win.bplist','jagwa.win.mc','jagwa.win.jn']
     .forEach(k=>{try{localStorage.removeItem(k)}catch(e){}});
   FL.past='y';FL.q='';FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';
   GG={};GGREF={};PICK={};
   {const rec0=JSON.parse(await (await __nativeFetch('/data/earth/%EA%B8%B0%EB%A1%9D.json')).text());
    UN=rec0.data.unit||{};BPG=rec0.data.bpg||{};MC=rec0.data.mcard||{};CROP=rec0.data.crop||{};TFIX=rec0.data.tfix||{};
    await put('kv','unit',UN);await put('kv','bpg',BPG);await put('kv','mcard',MC);await put('kv','crop',CROP);await put('kv','tfix',TFIX);
    if(typeof jgMigrate==='function')await jgMigrate('boot');   /* ★ jagwa_uid(9/29) — 실기기는 이 손값이 부팅 전부터 kv 에 있어 부팅 때 옮겨진다 · 하네스는 부팅 뒤에 넣으니 같은 옮김을 한 번(바탕 앱엔 없음) */
    refreshUnits();}
   draw(); await wait(300);
   const NEW=!!document.getElementById('bkNav');
   addEventListener('unhandledrejection',e=>{N('X 거부 스택',String((e.reason&&e.reason.stack)||e.reason).slice(0,700))});
   N('X 밑준비',{subj:SUBJ_ID,ISEA:ISEA,DATA:DATA.length,새판:NEW});
   const zOf=el=>el?(+getComputedStyle(el).zIndex||0):-1;
   /* ★ A-6(d) 9/30 _task_qa_baseline — jagwa_uid(9/29 · 5e18424) 뒤 표본 번호가 새 꼴(G25-62-09) · 바탕 앱(24f1a373)의 codeShow 는 옛 꼴이라 못 찾아 표본 0 → 데이터 uid(F.CODE)로도 찾는다(새 판은 codeShow 먼저 · 같은 줄) */
   const byCode=cs=>DATA.find(r=>codeShow(r)===cs)||DATA.find(r=>r[F.CODE]===cs)||null;
   const noOf=cs=>{const r=byCode(cs);return r?r[F.NO]:0};
   const cur=()=>{try{const p=bkCurPage();return p?p.pr:0}catch(e){return 0}};
   const bkReady=async(ms)=>{await until(()=>BK.open&&BK.pgs&&BK.pgs.length>0&&!BK.loading&&cur()>0,ms||25000);await wait(250)};
   const vis=el=>!!el&&!el.classList.contains('hide')&&getComputedStyle(el).display!=='none';
   const closeAll=async()=>{try{if(window.PINFOR&&window.bwPinEnd)bwPinEnd()}catch(e){}
     try{if(BK.open)bkClose()}catch(e){} try{if(!$('#view').classList.contains('hide'))closeView()}catch(e){}
     ['bpl','mcw','jnw','tfxSheet','bkrefpop','bkreftag','crmenu'].forEach(id=>{const e=document.getElementById(id);if(e)e.remove()});
     $$$('.sheet.shfloat').forEach(x=>x.remove());$$$('.sheet.xmodal').forEach(x=>x.remove());
     BPLNO=null;try{cropFor(null)}catch(e){}await wait(250)};
   const toasts=()=>$$$('.toast').map(x=>txt(x));
   const PE=(t,x,y,pt,id,o)=>{const e=new Event(t,{bubbles:true,cancelable:true});
     const v=Object.assign({clientX:x,clientY:y,pageX:x,pageY:y,pointerType:pt||'pen',pointerId:id||31,isPrimary:true,pressure:.5,
       button:0,buttons:1,width:pt==='touch'?10:1,height:pt==='touch'?10:1},o||{});
     Object.keys(v).forEach(k=>Object.defineProperty(e,k,{get:()=>v[k]}));
     Object.defineProperty(e,'getCoalescedEvents',{value:()=>[]});return e};
   const send=(el,t,x,y,pt,id,o)=>el.dispatchEvent(PE(t,x,y,pt,id,o));
   const click=el=>el.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));
   const keyEnter=el=>el.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true,cancelable:true}));
   const pgInput=async v=>{const i=document.getElementById('bkPg');if(!i)return false;i.value=String(v);keyEnter(i);await wait(300);await until(()=>!BK.loading,20000);await wait(250);return true};
   const pageRect=pr=>{const p=BK.pgs.find(x=>x.pr===pr);return p&&p.el?p.el.getBoundingClientRect():null};
   const vpRect=()=>document.getElementById('bkvp').getBoundingClientRect();
   /* 교재 쪽 안 · 창 안에 드는 두 점(0~1 비율) */
   const inPage=(pr,fx,fy)=>{const a=pageRect(pr),v=vpRect();if(!a)return null;
     const x0=Math.max(a.left,v.left+10),x1=Math.min(a.right,v.right-10),y0=Math.max(a.top,v.top+10),y1=Math.min(a.bottom,v.bottom-10);
     if(x1<=x0||y1<=y0)return null;return [x0+(x1-x0)*fx,y0+(y1-y0)*fy]};
   const bkDrag=async(pr,a,b,pt,id)=>{const vp=document.getElementById('bkvp');const p0=inPage(pr,a[0],a[1]),p1=inPage(pr,b[0],b[1]);if(!p0||!p1)return false;
     send(vp,'pointerdown',p0[0],p0[1],pt,id);await wait(40);
     send(vp,'pointermove',(p0[0]+p1[0])/2,(p0[1]+p1[1])/2,pt,id);await wait(40);
     send(vp,'pointermove',p1[0],p1[1],pt,id);await wait(40);
     send(vp,'pointerup',p1[0],p1[1],pt,id);await wait(500);return true};
   const G02=noOf('G02-39-02'), G62=noOf('G25-62-09'), uG62=(byCode('G25-62-09')||[])[F.CODE];
   N('X 표본',{G02_39_2:[G02,G02&&bpgOf(rec(G02))],G25_62_9:[G62,G62&&bpgOf(rec(G62)),uG62]});

   /* ── X-A 📖 p 목록 창 「N쪽」 = 교재만 ── */
   await grp('X-A', async()=>{
     await closeAll();
     const one=async(no,pg,open)=>{if(open){await bookOpen(1,true);await bkReady()}
       bplOpen(no);await wait(400);
       const row=$$$('#bpl .bplrow').find(r=>txt(r.querySelector('.pr'))===pg+'쪽');
       const v0=VNO;if(row)click(row);await wait(400);await bkReady(20000);
       const r={row:!!row,book:vis($('#book')),info:txt($('#bkInfo')),view:vis($('#view')),VNO:VNO,v0:v0,bpl:!!document.getElementById('bpl')};
       await closeAll();return r};
     let r=await one(G02,4,false);
     T('X-A1 G02-39-02 목록 창 「4쪽」 → 교재 4쪽 · 문항 창 안 뜸 · VNO 무변 · 목록 창 남음',
       r.row&&r.book&&/4쪽/.test(r.info)&&!r.view&&r.VNO===r.v0&&r.bpl,r);
     r=await one(G62,5,false);
     T('X-A2 G25-62-09 목록 창 「5쪽」 → 교재 5쪽 · 문항 창 안 뜸',r.row&&r.book&&/5쪽/.test(r.info)&&!r.view&&r.VNO===r.v0,r);
     r=await one(G02,4,true);
     T('X-A3 교재가 이미 열린 채 눌러도 같음',r.row&&r.book&&/4쪽/.test(r.info)&&!r.view&&r.VNO===r.v0,r);
   });

   /* ── X-B 마지막으로 만진 창이 맨 앞 ── */
   await grp('X-B', async()=>{
     await closeAll();
     await bookOpen(5,true);await bkReady();
     await openView(G62);await wait(700);
     const V=$('#view'),B=$('#book');
     T('X-B1 교재 창 뒤 문항 창(.win)을 열면 문항 z > 교재 z',V.classList.contains('win')&&zOf(V)>zOf(B),[V.className,zOf(V),zOf(B)]);
     send(B.querySelector('.panel'),'pointerdown',10,10,'mouse',51);send(B.querySelector('.panel'),'pointerup',10,10,'mouse',51);await wait(120);
     T('X-B2 교재 판을 누르면 교재 z > 문항 z',zOf(B)>zOf(V),[zOf(B),zOf(V)]);
     send(V,'pointerdown',10,10,'mouse',52);send(V,'pointerup',10,10,'mouse',52);await wait(120);
     T('X-B3 문항을 누르면 다시 문항 위',zOf(V)>zOf(B),[zOf(V),zOf(B)]);
     bkQOpen();await wait(400);const Q=$('#bkq');
     T('X-B4 「이 쪽의 문항」 창을 열면 맨 앞',vis(Q)&&zOf(Q)>zOf(V)&&zOf(Q)>zOf(B),[zOf(Q),zOf(V),zOf(B)]);
     send(B.querySelector('.panel'),'pointerdown',10,10,'mouse',53);await wait(100);
     T('X-B5 교재를 누르면 「이 쪽의 문항」 위',zOf(B)>zOf(Q),[zOf(B),zOf(Q)]);
     bplOpen(G62);await wait(400);const P=document.getElementById('bpl');
     T('X-B6 목록 창을 열면 맨 앞',!!P&&zOf(P)>Math.max(zOf(B),zOf(V),zOf(Q)),[zOf(P),zOf(B),zOf(V),zOf(Q)]);
     send(V,'pointerdown',10,10,'mouse',54);await wait(100);
     T('X-B7 문항을 누르면 목록 창 위',zOf(V)>zOf(P),[zOf(V),zOf(P)]);
     await mcwOpen('all');await wait(900);const M=document.getElementById('mcw');
     T('X-B8 🃏 창을 열면 맨 앞',!!M&&zOf(M)>Math.max(zOf(V),zOf(P),zOf(B)),[zOf(M),zOf(V),zOf(P),zOf(B)]);
     send(P.querySelector('.panel'),'pointerdown',10,10,'mouse',55);await wait(100);
     T('X-B9 목록 창을 누르면 🃏 창 위',zOf(P)>zOf(M),[zOf(P),zOf(M)]);
     {const S=$('#sub');try{await Promise.race([subOpen('',false),wait(3000)])}catch(e){}await wait(400);
      T('X-B10 서브노트 창을 열면 맨 앞(띠 안)',vis(S)&&zOf(S)>Math.max(zOf(P),zOf(M),zOf(V))&&zOf(S)<80,[zOf(S),zOf(P),zOf(M)]);
      send(V,'pointerdown',10,10,'mouse',56);await wait(100);
      T('X-B11 문항을 누르면 서브노트 위',zOf(V)>zOf(S),[zOf(V),zOf(S)]);
      try{$('#sX').click()}catch(e){}await wait(150)}
     {const b=document.createElement('div');b.className='sheet';b.innerHTML='<div class="panel"><h2>검산 떠 있는 시트</h2><p>x</p></div>';
      document.body.appendChild(b);try{shFloat(b,'xtest','검산')}catch(e){}await wait(200);
      T('X-B12 떠 있는 시트(shFloat)도 무리 — 열면 맨 앞',zOf(b)>=70&&zOf(b)<80&&zOf(b)>zOf(V),[zOf(b),zOf(V)]);
      send(B.querySelector('.panel'),'pointerdown',10,10,'mouse',57);await wait(100);
      T('X-B13 교재를 누르면 떠 있는 시트 위',zOf(B)>zOf(b),[zOf(B),zOf(b)]);b.remove()}
     {const b=document.createElement('div');b.className='sheet xmodal';b.innerHTML='<div class="panel"><h2>검산 모달</h2></div>';document.body.appendChild(b);await wait(80);
      const top=Math.max(...['view','book','bkq','bpl','mcw','sub'].map(id=>zOf(document.getElementById(id))));
      T('X-B14 모달 시트(80)는 떠 있는 창 모두의 위',zOf(b)===80&&zOf(b)>top,[zOf(b),top]);b.remove();
      toast('검산 토스트');await wait(60);const t=$$$('.toast').pop();
      T('X-B15 토스트(99)·#crmenu(95)는 늘 위',!!t&&zOf(t)===99&&zOf(t)>top,[t&&zOf(t),top])}
     vwApply(false);await wait(300);
     T('X-B16 문항 창을 전체 화면으로 → 인라인 z 없음(CSS 60)',V.style.zIndex===''&&zOf(V)===60,[V.style.zIndex,zOf(V)]);
     vwApply(true);await wait(300);
     {const mm=window.matchMedia;window.matchMedia=q=>(/max-width:480px/.test(String(q))?{matches:true,addListener(){},removeListener(){}}:mm.call(window,q));
      try{window.dispatchEvent(new Event('resize'));await wait(200);send(V,'pointerdown',10,10,'mouse',58);await wait(120);
        /* ★ A-6(a) 9/30 _task_qa_baseline — phone_win §A-1(genie fb89ad2 · 결정로그 9/28 16:27·17:20 · 수행 결과 「shell X-B17 = 폰 문제 창이 떠 있는 창이 되어 창 띠에 든다 · 나중에 연 창이 위」) */
        T('X-B17 480px 이하에서도 문항 창이 창 띠(70~79)에 든다 — 누르면 교재 위(phone_win A-1 · 나중에 연 창이 위)',V.style.zIndex!==''&&zOf(V)>=70&&zOf(V)<80&&zOf(V)>zOf(B),[V.style.zIndex,zOf(V),zOf(B)])}
      finally{window.matchMedia=mm;window.dispatchEvent(new Event('resize'));await wait(450)}}   /* 물리 resize 손잡이(250ms 뒤 VNO 를 다시 읽음)가 문항이 열린 채 돌게 기다린다 */
     await closeAll();
   });

   /* ── X-C ◀ [쪽] ▶ · ↩ ── */
   await grp('X-C', async()=>{
     await closeAll();
     await bookOpen(5,true);await bkReady();
     const bb=()=>document.getElementById('bkBack');
     T('X-C0 머리줄 #bkInfo 바로 뒤 ◀ [쪽] ▶',!!document.getElementById('bkNav')&&$('#bkInfo').nextElementSibling===document.getElementById('bkNav'),
       ($('#bkInfo').nextElementSibling||{}).id);
     T('X-C1 창 열기 직후 ↩ 숨김',!!bb()&&bb().hidden,bb()?bb().hidden:'(없음)');
     await pgInput(9);T('X-C2 쪽 칸 9 Enter → 9쪽',cur()===9,cur());
     await pgInput(98);await until(()=>cur()===98,15000);T('X-C3 98 Enter → 98쪽(다른 조각 받아 옴)',cur()===98,cur());
     const at=cur();const t0=toasts().length;
     await pgInput(0);const a0=cur();await pgInput('abc');const a1=cur();await pgInput(999);const a2=cur();await wait(150);
     T('X-C4 0 · abc · 999 → 이동 없음',a0===at&&a1===at&&a2===at,[at,a0,a1,a2]);
     T('X-C5 999 → 토스트 「999쪽 — 교재에 없는 쪽」',toasts().some(x=>x.indexOf('999쪽 — 교재에 없는 쪽')>=0),toasts().slice(-3));
     await bkGoto(14);await wait(300);const s0=cur();
     click($('#bkNextP'));await wait(500);await until(()=>!BK.loading,15000);const s1=cur();
     click($('#bkNextP'));await wait(600);await until(()=>!BK.loading&&cur()===16,15000);const s2=cur();
     click($('#bkPrevP'));await wait(500);const s3=cur();
     T('X-C6 ◀▶: 14 → 15 → 16(조각 넘김) → 15',s0===14&&s1===15&&s2===16&&s3===15,[s0,s1,s2,s3]);
     bkClose();await wait(300);await bookOpen(5,true);await bkReady();
     T('X-C7 교재를 닫았다 열면 ↩ 숨김',!!bb()&&bb().hidden,bb()?[bb().hidden,txt(bb())]:'(없음)');
     await pgInput(12);
     T('X-C8 5 에서 12 로 → 「↩ 5쪽」',cur()===12&&!!bb()&&!bb().hidden&&txt(bb())==='↩ 5쪽',[cur(),bb()&&txt(bb())]);
     click(bb());await wait(500);
     T('X-C9 ↩ 누름 → 5쪽 · 「↩ 12쪽」',cur()===5&&txt(bb())==='↩ 12쪽',[cur(),txt(bb())]);
     click(bb());await wait(500);
     T('X-C10 다시 → 12쪽',cur()===12,cur());
     await pgInput(20);click($('#bkPrevP'));await wait(500);
     T('X-C11 20 입력 뒤 ◀ → 19쪽 · ↩ 는 「↩ 12쪽」 그대로',cur()===19&&txt(bb())==='↩ 12쪽',[cur(),txt(bb())]);
     {const p=$('#book .panel'),r0=p.getBoundingClientRect(),i=$('#bkPg'),n=$('#bkNextP');
      [i,n].forEach(el=>{const r=el.getBoundingClientRect();send(el,'pointerdown',r.left+4,r.top+4,'mouse',61);
        send($('#book .bkbar'),'pointermove',r.left+84,r.top+64,'mouse',61);send($('#book .bkbar'),'pointerup',r.left+84,r.top+64,'mouse',61)});
      await wait(150);const r1=p.getBoundingClientRect();
      T('X-C12 쪽 칸·단추 pointerdown 에 창 자리 무변(끌기 안 됨)',Math.abs(r1.left-r0.left)<1&&Math.abs(r1.top-r0.top)<1,[r0.left,r0.top,r1.left,r1.top])}
     bkClose();await wait(300);
     T('X-C13 교재 닫으면 ↩ 숨김',!!bb()&&bb().hidden,bb()?bb().hidden:'(없음)');
     await closeAll();
   });

   /* ── X-D 「이 쪽의 문항」 — 연도 내림차순 · 누르면 문항 창 ── */
   await grp('X-D', async()=>{
     await closeAll();
     await bookOpen(9,true);await bkReady();await bkGoto(9);await wait(300);
     bkQOpen();await wait(400);
     const rows=$$$('#bkqList [data-no]');
     const ys=rows.map(r=>{const y=r.querySelector('.yr');return y?+txt(y):0});
     const R=rows.map(r=>rec(+r.dataset.no));
     const yrs=R.map(r=>+r[F.YEAR]||0);
     let ok=rows.length>1;for(let i=1;i<R.length;i++){const a=R[i-1],b=R[i],ya=+a[F.YEAR]||0,yb=+b[F.YEAR]||0;
       if(ya&&yb){if(ya<yb)ok=false;else if(ya===yb){if((+a[F.ROUND]||0)<(+b[F.ROUND]||0))ok=false;else if((+a[F.ROUND]||0)===(+b[F.ROUND]||0)&&(+a[F.LNO]||0)>(+b[F.LNO]||0))ok=false}}
       else if(!ya&&yb)ok=false;else if(!ya&&!yb&&a[F.NO]>b[F.NO])ok=false}
     N('X-D 9쪽 줄',R.map(r=>codeShow(r)+'/'+(r[F.YEAR]||'-')));
     T('X-D1 9쪽 「문항 N」 = 연도 내림 · 같은 해 회차 내림·문번 오름 · 연도 없는 것 맨 뒤',ok,R.map(r=>codeShow(r)+'/'+(r[F.YEAR]||'-')).slice(0,30));
     T('X-D2 줄마다 연도 글자(.yr) = 그 문항 연도',rows.length>0&&ys.every((y,i)=>y===yrs[i]),[ys.slice(0,8),yrs.slice(0,8)]);
     {const y22=R.filter(r=>+r[F.YEAR]===2022).map(r=>codeShow(r));N('X-D 2022',y22)}
     const r0=rows[0];click(r0);await wait(900);
     const V=$('#view');
     T('X-D3 줄 누름 → 교재 창 그대로 · 문항 창 뜸 · 문항 z 최상',vis($('#book'))&&vis(V)&&VNO===+r0.dataset.no&&zOf(V)>=Math.max(zOf($('#book')),zOf($('#bkq'))),
       [vis($('#book')),vis(V),VNO,+r0.dataset.no,zOf(V),zOf($('#book')),zOf($('#bkq'))]);
     T('X-D4 누른 줄 = me',!!$$$('#bkqList [data-no]').find(x=>+x.dataset.no===+r0.dataset.no&&x.classList.contains('me')));
     const r1=$$$('#bkqList [data-no]')[1];if(r1){click(r1);await wait(900)}
     T('X-D5 다른 줄 누름 → 문항 창의 문항만 바뀜(교재 그대로)',!!r1&&VNO===+r1.dataset.no&&vis($('#book')),[r1&&+r1.dataset.no,VNO,vis($('#book'))]);
     await closeAll();
   });

   /* ── X-E 📍 자리 직접 찍기 ── */
   await grp('X-E', async()=>{
     await closeAll();
     const uid=uG62, keep=JSON.stringify(BPG[uid]||null);
     await bookOpen(5,true);await bkReady();
     const pk=()=>document.getElementById('bkPick');
     T('X-E1 교재만 연 상태 = 📍 숨김',!pk()||pk().hidden,pk()?pk().hidden:'(없음)');
     bplOpen(G62);await wait(400);
     T('X-E2 목록 창 아랫줄 없음(#bplFoot 0)',!document.getElementById('bplFoot'),!!document.getElementById('bplFoot'));
     T('X-E3 p5 목록 창 열면 교재 머리줄 📍(글자 0 · title 있음)',!!pk()&&!pk().hidden&&txt(pk())==='📍'&&!!pk().title,pk()?[pk().hidden,txt(pk()),pk().title]:'(없음)');
     const pg0=cur();click(pk());await wait(300);
     T('X-E4 누름 → 쪽 무변 · 칩 「📍 찍는 문항 G25-62-09 …」 · 📍 파랑(.on)',cur()===pg0&&/^📍 찍는 문항 G25-62-09/.test(txt($('#bkFor')))&&pk().classList.contains('on'),[pg0,cur(),txt($('#bkFor')),pk().className]);
     T('X-E5 찍는 중 ◻ 오리기 단추는 켜진 표시 없음',!($('#bktools [data-tool="crop"]')||{classList:{contains:()=>false}}).classList.contains('on'));
     await bkDrag(5,[0.2,0.3],[0.6,0.45],'touch',71);
     T('X-E6 손가락 끌기 = 굴림(저장 0)',!(BPG[uid]&&BPG[uid].b)&&window.PINFOR===G62,[BPG[uid],window.PINFOR]);
     await bkDrag(5,[0.2,0.3],[0.6,0.45],'pen',72);
     const v=BPG[uid];
     T('X-E7 펜 끌기 → BPG = {ps:[5],last:5,b:[5,…]}',!!v&&JSON.stringify(v.ps)==='[5]'&&v.last===5&&Array.isArray(v.b)&&v.b.length===5&&v.b[0]===5&&v.b[3]>v.b[1]&&v.b[4]>v.b[2],v);
     T('X-E8 찍기 끝 · 도구 = 보기',window.PINFOR===null&&!!$('#bktools [data-tool="view"].on'),[window.PINFOR,($$$('#bktools [data-tool].on')[0]||{}).textContent]);
     await wait(300);
     T('X-E9 목록 줄 「📍 찍은 자리」',$$$('#bpl .bplrow .tg').some(x=>txt(x)==='📍 찍은 자리'),$$$('#bpl .bplrow .tg').map(x=>txt(x)));
     {const it=$$$('#list .item').find(x=>txt(x.querySelector('.num'))==='G25-62-09');
      T('X-E10 첫 화면 칩 p5',!!it&&txt(it).indexOf('p5')>=0,it?txt(it).slice(0,90):null)}
     T('X-E11 .bpinbox 1(「📍 G25-62-09」 딱지)',$$$('.bpinbox').length===1&&txt($$$('.bpinbox')[0]).indexOf('G25-62-09')>=0,$$$('.bpinbox').length);
     await bkGoto(20);await wait(400);
     {const row=$$$('#bpl .bplrow').find(r=>txt(r.querySelector('.pr'))==='5쪽');if(row)click(row);await wait(900);await bkReady(15000);await wait(300);
      const bx=$$$('.bpinbox')[0],vr=vpRect(),br=bx?bx.getBoundingClientRect():null;
      T('X-E12 20쪽에서 목록 줄 누름 → 5쪽 · 네모가 화면 안(위 1/4 쯤)',cur()===5&&!!br&&br.top>=vr.top&&br.top<=vr.top+vr.height*0.5,[cur(),br&&Math.round(br.top-vr.top),Math.round(vr.height)])}
     {const x=document.getElementById('bkPickX');
      T('X-E13 「찍은 자리 지우기」 보임',!!x&&!x.hidden,x?x.hidden:'(없음)');
      if(x)click(x);await wait(600);
      T('X-E14 지우기 → BPG[uid] 없음 · 네모 0 · 목록 = 자동값',!BPG[uid]&&$$$('.bpinbox').length===0&&!$$$('#bpl .bplrow .tg').some(t=>txt(t)==='📍 찍은 자리'),[BPG[uid],$$$('.bpinbox').length,$$$('#bpl .bplrow .tg').map(t=>txt(t))])}
     click(pk());await wait(250);
     {const vp=document.getElementById('bkvp');const p0=inPage(5,0.3,0.3);
      send(vp,'pointerdown',p0[0],p0[1],'pen',73);send(vp,'pointermove',p0[0]+3,p0[1]+2,'pen',73);send(vp,'pointerup',p0[0]+3,p0[1]+2,'pen',73);await wait(400);
      T('X-E15 톡(작은 네모) → 저장 0 · 찍기는 그대로',!BPG[uid]&&window.PINFOR===G62,[BPG[uid],window.PINFOR])}
     click(document.querySelector('#bpl #bplX'));await wait(300);
     T('X-E16 찍는 중 목록 창 닫기 → 찍기 끝',window.PINFOR===null&&!document.getElementById('bpl'),[window.PINFOR]);
     /* 찍는 중이 아닐 때 — 🃏·오리기 메뉴는 그대로 */
     cropFor(G62);{const t=$('#bktools [data-tool="crop"]');if(t)click(t)}await wait(200);
     await bkDrag(5,[0.25,0.3],[0.55,0.42],'pen',74);await wait(300);
     {const m=document.getElementById('crmenu');
      T('X-E17 찍는 중이 아닐 때 오리기 메뉴 = 카드 + 문제 칸 + 해설 칸 + 글자 + 취소(HEAD 그대로)',!!m&&[...m.querySelectorAll('button')].map(b=>b.dataset.s).join(',')==='mc,q,s,fix,',
        m?[...m.querySelectorAll('button')].map(b=>b.dataset.s):null);if(m)m.querySelector('[data-s=""]').click()}
     try{bkToolView()}catch(e){}
     if(keep!=='null')BPG[uid]=JSON.parse(keep);else delete BPG[uid];await saveBPG();
     await closeAll();
   });

   /* ── X-F 📋 정리 창 글씨 ── */
   await grp('X-F', async()=>{
     await closeAll();
     const sec=(unitOf(G62)||'1.1.1').split('.').slice(0,2).join('.');jnOpen(sec);await wait(700);
     const fs=q=>{const e=$$$(q)[0];return e?[parseFloat(getComputedStyle(e).fontSize),getComputedStyle(e).fontWeight]:null};
     const S={jnh:fs('#jnw .jnh'),mut:fs('#jnw .jnrow .h .mut'),jgo:fs('#jnw .jnrow .h .jgo'),page:fs('#jnw .jnrow .h .tag.page'),
       q:fs('#jnw .jnrow .q'),jnans:fs('#jnw .jnrow .jnans')};
     /* ★ uid_unify G-1(10/4 · 근거 gigu/_task_jagwa_uid_unify.md §G-1 · 앱 jnRowHTML `(HASBOOK?(ynUid(r)?'':'<span class="mut">…'):…)`) — 새 판 지학 📋 정리 창 줄은 기출 uid 줄이라 .mut(이름)을 안 그린다(줄에 .mut 0 → S.mut = null)
        → 줄 머리 .mut 의 CSS 규칙 글자(10px 굵게)만 .jnrow .h 안에 임시 .mut 를 넣어 잰다 · 옛 판 = 줄의 .mut 그대로(이 갈래를 안 탄다) */
     if(!S.mut&&typeof ynUid==='function'){const h=$$$('#jnw .jnrow .h')[0];if(h){const sp=document.createElement('span');sp.className='mut';sp.textContent='x';h.appendChild(sp);
       S.mut=[parseFloat(getComputedStyle(sp).fontSize),getComputedStyle(sp).fontWeight];sp.remove()}}
     N('X-F 크기',S);
     T('X-F1 단원 머리 11px',S.jnh&&S.jnh[0]===11,S.jnh);
     T('X-F2 줄 머리(.mut) 10px 굵게',S.mut&&S.mut[0]===10&&+S.mut[1]>=700,S.mut);
     T('X-F3 코드 칩·📖 p 칩 10px',S.jgo&&S.jgo[0]===10&&(!S.page||S.page[0]===10),[S.jgo,S.page]);
     T('X-F4 문제 글 12.5px · 「정답·해설」 11px',S.q&&S.q[0]===12.5&&S.jnans&&S.jnans[0]===11,[S.q,S.jnans]);
     {const w=document.getElementById('jnw');if(w)w.remove()}
     await mcwOpen('all');await wait(900);
     const M={h:fs('#mcw .bplh'),row:fs('#mcwBody div')};snap.xmcw=M;N('X-F 🃏 창 크기(바탕 판과 main 이 맞댄다)',M);
     {const w=document.getElementById('mcw');if(w)w.remove()}
   });

   /* ── X-G 📍 찍는 중 이미 찍은 자리 ── */
   await grp('X-G', async()=>{
     await closeAll();
     const keep=JSON.stringify({a:BPG['G22-59-07']||null,b:BPG[uG62]||null}),pk0=JSON.stringify(PICK);
     BPG['G22-59-07']={ps:[554],last:554,b:[554,0.1,0.2,0.5,0.3]};
     PICK['G22-59-08']=[{k:'p_x1',doc:'book',p:554,r:[60,500,300,560],ts:1},{k:'p_x2',doc:'omr',p:1,r:[10,10,100,60],ts:2}];
     delete BPG[uG62];await saveBPG();await savePICK();
     await openView(G62);await wait(600);
     await bookOpen(554,true);await bkReady();await bkGoto(554);await wait(500);
     {const t=$('#bktools [data-tool="crop"]');if(t)click(t);await wait(250);
      T('X-G1 ◻ 오리기만 켜면 점선 0(찍기 ≠ 오리기)',$$$('.bkref').length===0,$$$('.bkref').length);try{bkToolView()}catch(e){}await wait(150)}
     const pk=document.getElementById('bkPick');if(pk)click(pk);await wait(400);
     const oth=$$$('.bkref.oth');
     T('X-G2 📍 → 554쪽 회색 점선 2',oth.length===2,[oth.length,$$$('.bkref').length]);
     T('X-G3 찍는 중 오리기 단추 .on 없음',!($('#bktools [data-tool="crop"]')||{classList:{contains:()=>false}}).classList.contains('on'));
     const g=oth.find(d=>{const r=d.getBoundingClientRect(),p=pageRect(554);return p&&Math.abs((r.left-p.left)/(p.width)-0.1)<0.02});
     if(g){const r=g.getBoundingClientRect();send(g,'pointerdown',r.left+5,r.top+5,'mouse',81);send(g,'pointerup',r.left+5,r.top+5,'mouse',81);click(g)}
     await wait(300);const pop=document.getElementById('bkrefpop');
     T('X-G4 회색 누름 → 작은 창 「G22-59-07 의 자리 · … 554쪽」 · 「📍 자리」',!!pop&&/G22-59-07 의 자리 · .*554쪽/.test(txt(pop))&&txt(pop).indexOf('📍 자리')>=0,pop?txt(pop):null);
     T('X-G5 찍기 끌기 안 시작(.crbox 0)',$$$('#bkover .crbox,#bkworld .crbox').length===0,$$$('.crbox').length);
     if(pop)click(pop.querySelector('.go'));await wait(700);
     const v=BPG[uG62];
     T('X-G6 「이 문항에도 쓰기」 → BPG[G62-09] = {ps:[554],last:554,b:(같은 값),ref:G59-07}',
       !!v&&JSON.stringify(v.ps)==='[554]'&&v.last===554&&JSON.stringify(v.b)===JSON.stringify([554,0.1,0.2,0.5,0.3])&&v.ref==='G22-59-07',v);
     T('X-G7 찍기 끝 · 점선 0 · 원래 문항 값 무변',window.PINFOR===null&&$$$('.bkref').length===0&&JSON.stringify(BPG['G22-59-07'])===JSON.stringify({ps:[554],last:554,b:[554,0.1,0.2,0.5,0.3]}),
       [window.PINFOR,$$$('.bkref').length,BPG['G22-59-07']]);
     if(pk)click(pk);await wait(300);
     {const t=$('#bktools [data-tool="crop"]');if(t)click(t);await wait(250);
      T('X-G8 찍는 중 ◻ 오리기 누름 → 찍기 끝',window.PINFOR===null,window.PINFOR);try{bkToolView()}catch(e){}}
     {const f=window.bwSpotsOn;const was=OMRTAB;let a=null,b=null;
      if(f){OMRTAB=true;try{a=f({pr:1,w:600,h:800}).map(s=>s.kind);b=f({pr:554,w:600,h:800}).map(s=>s.kind)}finally{OMRTAB=was}}
      T('X-G9 정리OMR 탭 = doc:omr 픽만(📍·교재 픽 빠짐)',!!f&&JSON.stringify(a)==='["🃏 카드"]'&&JSON.stringify(b)==='[]',[a,b])}
     {const k=JSON.parse(keep);if(k.a)BPG['G22-59-07']=k.a;else delete BPG['G22-59-07'];if(k.b)BPG[uG62]=k.b;else delete BPG[uG62];
      PICK=JSON.parse(pk0);await saveBPG();await savePICK()}
     await closeAll();
   });

   /* ── X-H 문제 창 필기 흔들림 ── */
   await grp('X-H', async()=>{
     await closeAll();
     const noH=noOf('G24-61-01');await openView(noH);await wait(900);
     const W=$('#cardwrap'),C=$('#card');
     for(let i=0;i<50&&!(W.scrollHeight>W.clientHeight+100);i++)await wait(120);   /* ★ jagwa_uid(9/29) — 카드 길이는 오린 교재 그림 둘(p.561)이 그려져야 난다 · 그림이 늦으면 0.9초에 짧게 잰다(흔들림) */
     T('X-H0 카드가 창보다 길다(표본 G24-61-01)',W.scrollHeight>W.clientHeight+100,[W.scrollHeight,W.clientHeight,C.querySelectorAll("img,canvas").length,JSON.stringify((typeof CROP!=="undefined"&&(CROP["G24-61-01"]||CROP["G61-01"]))||null).slice(0,80),(C.textContent||"").slice(0,160),window.__JGMIG||0]);
     T('X-H1 #cardwrap touch-action = none',getComputedStyle(W).touchAction==='none',getComputedStyle(W).touchAction);
     const r=W.getBoundingClientRect(),x=r.left+r.width*0.5,y=r.top+r.height*0.5;
     const tgt=()=>{const e=document.elementsFromPoint(x,y).find(el=>C.contains(el)&&!el.closest(PASS_THRU));return e||C};
     W.scrollTop=80;await wait(100);
     const el=tgt();
     send(el,'pointerdown',x,y,'touch',91);send(el,'pointermove',x,y-15,'touch',91);send(el,'pointermove',x,y-30,'touch',91);await wait(60);
     const moved=W.scrollTop;
     send(el,'pointerdown',x+60,y,'pen',92);await wait(40);
     const s1=W.scrollTop;
     send(el,'pointermove',x,y-60,'touch',91);await wait(40);const s2=W.scrollTop;
     send(el,'pointermove',x+70,y+5,'pen',92);send(el,'pointerup',x+70,y+5,'pen',92);send(el,'pointerup',x,y-60,'touch',91);await wait(60);
     T('X-H2 손가락 30px 끈 뒤 펜 획 → scrollTop 80(되돌림)',moved!==80&&s1===80,[moved,s1]);
     T('X-H3 그 손가락 계속 끌어도 80',s2===80,s2);
     await wait(300);
     send(el,'pointerdown',x,y,'touch',93);send(el,'pointermove',x,y-21,'touch',93);send(el,'pointermove',x,y-42,'touch',93);send(el,'pointerup',x,y-42,'touch',93);await wait(60);
     T('X-H4 획 뒤 0.3초에 닿은 손가락 42px → 80',W.scrollTop===80,W.scrollTop);
     await wait(1600);
     send(el,'pointerdown',x,y,'touch',94);send(el,'pointermove',x,y-21,'touch',94);send(el,'pointermove',x,y-42,'touch',94);send(el,'pointerup',x,y-42,'touch',94);await wait(60);
     const s4=W.scrollTop;
     T('X-H5 1.6초 뒤 손가락 → 굴림',s4!==80,s4);
     W.scrollTop=80;await wait(60);
     send(el,'pointerdown',x,y,'touch',95,{width:50,height:50});send(el,'pointermove',x,y-40,'touch',95,{width:50,height:50});send(el,'pointerup',x,y-40,'touch',95,{width:50,height:50});await wait(60);
     /* ★ penfinger A(2026-09-25) — ⓒ(접촉면 폭·높이 ≥ 40px = 손바닥)를 걷었다: 아이패드 사파리 손가락은 폭 40~50px 라 보통 손가락이 손바닥으로 잡혀
        문제 창이 손가락으로 안 굴렀다(사용자 9/25). 손바닥은 ⓑ(펜 시각)로만 거른다 — 펜 뗀 지 1.6초가 넘은 굵은 손가락은 **굴린다** */
     T('X-H6 접촉면 50px 손가락(펜 뗀 지 1.6초 넘음) → 굴림 — ⓒ 크기 손바닥 걷음(penfinger A)',W.scrollTop!==80,W.scrollTop);
     const btn=C.querySelector('#cDetBtn')||C.querySelector('button');let hits=0;const spy=()=>{hits++};
     if(btn){btn.addEventListener('click',spy);btn.scrollIntoView({block:'center'});await wait(100);
       const b=btn.getBoundingClientRect(),bx=b.left+b.width/2,by=b.top+b.height/2,st0=W.scrollTop;
       const dir=(W.scrollTop+W.clientHeight>=W.scrollHeight-60)?1:-1;   /* 끝에 닿아 있으면 반대로 끈다 */
       send(btn,'pointerdown',bx,by,'touch',96);send(btn,'pointermove',bx,by+20*dir,'touch',96);send(btn,'pointermove',bx,by+40*dir,'touch',96);send(btn,'pointerup',bx,by+40*dir,'touch',96);click(btn);await wait(80);
       T('X-H7 단추 위에서 시작해 끈 손가락 → 굴림 · 단추 안 눌림',W.scrollTop!==st0&&hits===0,[st0,W.scrollTop,hits]);
       await wait(600);const b2=btn.getBoundingClientRect();
       send(btn,'pointerdown',b2.left+b2.width/2,b2.top+b2.height/2,'touch',97);send(btn,'pointerup',b2.left+b2.width/2,b2.top+b2.height/2,'touch',97);click(btn);await wait(80);
       T('X-H8 단추 톡 → 눌림',hits===1,hits);btn.removeEventListener('click',spy);if(hits)click(btn)}
     else T('X-H7 단추 표본 없음',false);
     await closeAll();
   });

   /* ── X-I 문제 창 확대·축소 ── */
   await grp('X-I', async()=>{
     await closeAll();
     const noI=noOf('G24-61-01');await openView(noI);await wait(900);
     const W=$('#cardwrap'),C=$('#card');
     const sc=()=>{const m=/scale\(([\d.]+)\)/.exec(C.style.transform||'');return m?+m[1]:1};
     const r=W.getBoundingClientRect(),cx=r.left+r.width*0.45,cy=r.top+r.height*0.45;
     const el=document.elementsFromPoint(cx,cy).find(e=>C.contains(e))||C;
     const k0=sc(),a=C.getBoundingClientRect(),u=(cx+50-a.left)/(a.width/QCW),v=(cy-a.top)/(a.width/QCW);
     send(el,'pointerdown',cx-50,cy,'touch',101);send(el,'pointerdown',cx+50,cy,'touch',102);await wait(30);
     send(el,'pointermove',cx+150,cy,'touch',102);await wait(80);
     const k1=sc(),b=C.getBoundingClientRect(),bk=b.width/QCW;
     T('X-I1 두 손가락 벌림 → scale 커짐',k1>k0,[k0,k1]);
     T('X-I2 두 손가락 가운데 아래 글자가 제자리(±4px)',Math.abs(b.left+u*bk-(cx+50))<=4&&Math.abs(b.top+v*bk-cy)<=4,[Math.round(b.left+u*bk-(cx+50)),Math.round(b.top+v*bk-cy)]);
     send(el,'pointermove',cx-40,cy,'touch',102);await wait(80);
     const k2=sc();
     T('X-I3 오므림 → 작아짐(0.6 밑으로 안 감)',k2<k1&&k2>=0.6*Math.min(1,(W.clientWidth-2)/QCW)-0.001,[k1,k2]);
     send(el,'pointerup',cx-40,cy,'touch',102);send(el,'pointerup',cx-50,cy,'touch',101);await wait(80);
     const k3=sc();C.dispatchEvent(new WheelEvent('wheel',{deltaY:-120,clientX:cx,clientY:cy,ctrlKey:true,bubbles:true,cancelable:true}));await wait(80);
     const k4=sc();
     T('X-I4 Ctrl+휠 → 배율 바뀜',k4!==k3,[k3,k4]);
     C.dispatchEvent(new WheelEvent('wheel',{deltaY:-120,clientX:cx,clientY:cy,bubbles:true,cancelable:true}));await wait(80);
     T('X-I5 Ctrl 없는 휠 → 배율 무변',sc()===k4,[k4,sc()]);
     {const P=window.INKG_EA&&INKG_EA.pinch;
      if(P){P.set(2,cx,cy);await wait(80)}
      const kz=sc(),a2=C.getBoundingClientRect(),kk=a2.width/QCW,pt=[200,300];
      const e2={clientX:a2.left+pt[0]*kk,clientY:a2.top+pt[1]*kk};const q2=(typeof qPt==='function')?qPt(e2):null;
      T('X-I6 2배에서 가로 굴림 됨',W.scrollWidth>W.clientWidth+10&&getComputedStyle(W).overflowX==='auto',[W.scrollWidth,W.clientWidth,getComputedStyle(W).overflowX]);
      if(P){P.set(1,cx,cy);await wait(80)}
      const a1=C.getBoundingClientRect(),k1b=a1.width/QCW;
      const e1={clientX:a1.left+pt[0]*k1b,clientY:a1.top+pt[1]*k1b};const q1=(typeof qPt==='function')?qPt(e1):null;
      T('X-I7 2배에서 그은 자리 = 1배로 돌렸을 때 같은 자리(qPt 카드 좌표)',!!q2&&!!q1&&Math.abs(q2[0]-q1[0])<1&&Math.abs(q2[1]-q1[1])<1&&kz>1.5,[kz,q2,q1])}
     T('X-I8 화면에 배율 숫자·단추 0',!$$$('#view *').some(e=>e.children.length===0&&/^\s*[−-]?\s*\d{2,3}\s*%\s*$/.test(e.textContent||''))&&!document.getElementById('vzWrap'));
     await closeAll();
   });

   /* ── X-J 미리보기 글자 고치기 ── */
   await grp('X-J', async()=>{
     await closeAll();
     const uid='G22-59-02',r=rowByUid(uid),no=r?r[F.NO]:0;const orig=txtOrig(uid,'q');
     delete TFIX[uid];await put('kv','tfix',TFIX);draw();await wait(300);
     const sec=(unitOf(no)||'1.1.1').split('.').slice(0,2).join('.');jnOpen(sec);await wait(700);
     const prev=()=>$$$('#list .item').map(it=>it.querySelector('.prev')).find(p=>p&&p.closest('.item')&&txt(p.closest('.item').querySelector('.num'))==='G22-59-02');
     const jq=()=>{const jr=$$$('#jnw .jnrow').find(x=>+x.dataset.no===no);return jr?jr.querySelector('.q'):null};
     N('X-J 표본',{uid,no,sec,prev:!!prev(),jn:!!jq(),crop:(typeof cropList==='function'?cropList(uid,'q').length:null)});
     const long=async el=>{const b=el.getBoundingClientRect();send(el,'pointerdown',b.left+8,b.top+6,'mouse',111);await wait(700);
       send(el,'pointerup',b.left+8,b.top+6,'mouse',111);click(el);await wait(250)};
     const p=prev();if(p)await long(p);
     let S=document.getElementById('tfxSheet');
     T('X-J1 목록 줄 .prev 길게 누름 → 「✎ 글자 고치기」 시트 · 문항 창 안 열림',!!S&&$('#view').classList.contains('hide'),[!!S,VNO]);
     T('X-J2 시트 안 오린 문제 칸 그림 1(551쪽)',!!S&&S.querySelectorAll('.tfxcrop canvas').length===1,S?S.querySelectorAll('.tfxcrop canvas').length:null);
     const NEWQ='검산 새 글 — 바뀐 문제 글자';
     if(S){S.querySelector('#tfxIn').value=NEWQ;click(S.querySelector('#tfxOk'));await wait(700)}
     T('X-J3 저장 → TFIX[G59-02].q',!!TFIX[uid]&&TFIX[uid].q===NEWQ,TFIX[uid]);
     T('X-J4 목록 줄 · 정리 창 줄 글자 = 새 글 · 둘 다 .fx',!!prev()&&txt(prev())===NEWQ&&prev().classList.contains('fx')&&!!jq()&&txt(jq())===NEWQ&&jq().classList.contains('fx'),
       [prev()&&txt(prev()).slice(0,30),jq()&&txt(jq()).slice(0,30)]);
     if(jq())await long(jq());S=document.getElementById('tfxSheet');
     T('X-J5 정리 창 줄 길게 누름도 같은 시트',!!S,!!S);if(S)click(S.querySelector('#tfxNo'));await wait(200);
     await openView(no);await wait(800);
     const NEW2='검산 둘째 글';
     if(prev())await long(prev());S=document.getElementById('tfxSheet');
     if(S){S.querySelector('#tfxIn').value=NEW2;click(S.querySelector('#tfxOk'));await wait(900)}
     T('X-J6 문제 창을 열어 두고 고치면 카드도 바뀜',txt($('#card')).indexOf(NEW2)>=0,txt($('#card')).slice(0,80));
     if(prev())await long(prev());S=document.getElementById('tfxSheet');
     if(S){click(S.querySelector('#tfxDel'));await wait(900)}
     T('X-J7 되돌리기(비우기) → 셋 다 OCR 원본 · .fx 없음',!(TFIX[uid]&&TFIX[uid].q)&&!!prev()&&txt(prev())===orig.replace(/\s+/g,' ').trim()&&!prev().classList.contains('fx')
       &&!!jq()&&!jq().classList.contains('fx')&&txt($('#card')).indexOf(NEW2)<0,[TFIX[uid],prev()&&txt(prev()).slice(0,30)]);
     closeView();await wait(400);
     {const q=prev();if(q){const b=q.getBoundingClientRect();send(q,'pointerdown',b.left+8,b.top+6,'mouse',112);await wait(80);send(q,'pointerup',b.left+8,b.top+6,'mouse',112);click(q);await wait(900)}}
     T('X-J8 짧게 누름 → 문항 열림',VNO===no&&!$('#view').classList.contains('hide'),[VNO,no]);
     await closeAll();{const w=document.getElementById('jnw');if(w)w.remove()}
   });
   try{await __nativeFetch('/snap',{method:'POST',body:JSON.stringify(snap)})}catch(e){}
"""

BODY_XSIDE = r"""
   /* ═══════════ X-11 생물·물리 무변 — DOM 글자 스냅숏(새 판 · 바탕 판을 main 이 맞댄다) ═══════════ */
   if(typeof CARD_LAYER!=='undefined'&&CARD_LAYER){await (async()=>{for(let __i=0;__i<300&&(typeof db==='undefined'||!db);__i++)await new Promise(r=>setTimeout(r,100));return loadEarthData()})()/* ★ 2026-10-08 (_task_jagwa_phys_win 회귀) db 가 설 때까지 — 고정 대기 경합(짐 크면 「db 없음」) · 판정 무변 */;await until(()=>DATA.length>600,30000)}else await wait(1500);
   ['jagwa.earth.order','jagwa.earth.coll','jagwa.earth.hmfold','jagwa.view.win',
    'jagwa.win.view','jagwa.win.book','jagwa.win.bplist','jagwa.win.mc','jagwa.win.jn']
     .forEach(k=>{try{localStorage.removeItem(k)}catch(e){}});
   try{_coll=null}catch(e){}
   FL.past='y';FL.q='';FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';
   if(CUR.KINDS)FL.types=new Set(['G']);
   /* 기록 동기화를 두 판 모두 끝낸 뒤 찍는다(동기화 시각이 갈리면 목록의 O/회독 표시가 갈린다 — 판 탓이 아니다)
      ★ 9/27 penfinger_add2 · jeongo_add2 §A-4 — 두 판 중 먼저 도는 쪽은 시험지 받기(#dl)와 기록 동기화가 겹쳐 15초 안에 못 끝나
        「근거 (0)」·풀이 셈 빈칸·「시험지 N개를 받았습니다」가 찍혔다(jeongo 804/3 · add1 806/1 · 다시 돌리면 FAIL 쪽이 뒤집힘 = 판 탓 아님)
        → 시험지 받기가 끝나길 기다리고 · 돌던 동기화가 끝난 뒤 한 번 더 돌려 끝까지(각 60초) */
   await until(()=>{const b=document.getElementById('dl');return !b||b.classList.contains('hide')||!/받는 중/.test(b.textContent||'')},60000);
   await until(()=>typeof recBusy==='undefined'||!recBusy,60000);
   try{if(typeof syncRecords==='function')await Promise.race([syncRecords(true),wait(60000)])}catch(e){}
   await until(()=>typeof recBusy==='undefined'||!recBusy,60000);
   GG={};GGREF={};PICK={};   /* ★ 9/28 — 비우기는 동기화 **뒤**(앞에 두면 동기화가 원격 근거를 되살리는지가 시각에 따라 갈려 「🔗 근거 (31)↔(0)」 · 두 판 같은 빈 상태로 찍는다) */
   draw(); await wait(600);
   const vis=el=>!!el&&!el.classList.contains('hide');
   const tx=el=>el?String(el.textContent||'').replace(/\d+'\d{2}"/g,"·'··\"").replace(/\s+/g,' ').trim():'';
   snap.subj=SUBJ_ID;
   /* ★ physprev(10/1 하위 에이전트 C) — _task_jagwa_physprev A-2 미리보기 칸(.prev 글 · .pvfig)은 두 판 모두 떼고 맞댄다(physprev 관문 B3 이 그 칸을 잰다) */
   const npv=el=>{if(!el)return el;const c=el.cloneNode(true);c.querySelectorAll('.prev,.pvfig,.jnrow .q').forEach(x=>x.remove());return c};
   /* ★ 2026-10-07 (_task_jagwa_phys_win §A-36 · §A-37 ㊴) — 물리 목록 「기출」 칩 → 「V3」 글자(.vno) · 「볼트 N」 칩(.tag.vlt) 걷음 = 뜻한 차 → 물리만 두 판 모두 그 칸(.vno · .tag.vlt · 기출 딱지)을 떼고 맞댄다
      옛: snap.list=$$$('#list .item').slice(0,40).map(x=>tx(npv(x))).join(' || '); */
   const nvk=c=>{if(c&&SUBJ_ID==='phys')c.querySelectorAll('.meta .vno,.meta .tag').forEach(x=>{if(x.classList.contains('vno')||x.classList.contains('vlt')||/^(기출|타기출|확인|예상)$/.test(String(x.textContent||'').trim()))x.remove()});return c};
   snap.list=$$$('#list .item').slice(0,40).map(x=>tx(nvk(npv(x)))).join(' || ');
   /* ★ A-6(a) 9/30 _task_qa_baseline — phone_win §A-2·§A-6(genie fb89ad2 · 결정로그 9/28 17:20 · 수행 결과 「X-11 phys esh DOM 글자 = §A-2 필터 글자 걷음 · §A-6 칩」):
        접기 단추 「필터 ▾」 → 「▾」 · 물리 [공식]·[개념] 칩(.pwchip) — 칩은 떼고 단추 글자는 「▾」 로 맞춘 뒤 잰다
        (동기화 칩 가림이 「필터」 앞에서만 멈춰, 새 판에선 「▾」 뒤 머리 줄을 통째로 먹던 것도 「▾」 앞에서 멈춘다) */
   snap.esh=tx((e=>{if(!e)return e;const c=e.cloneNode(true);c.querySelectorAll('.pwchip').forEach(x=>x.remove());return c})(document.getElementById('esh')||document.getElementById('lib')))
     .replace(/필터 ([▾▴])/,'$1')
     .replace(/[●○⟳]\s?(동기화됨( [^필▾▴]*?)?|토큰 없음|오프라인|동기화 실패|동기화 중)(?=필터|[▾▴])/g,'')
     .replace(/[가-힣]+ 받는 중 — \d+\/\d+/g,'')   /* 동기화 칩 · 받는 중 진행 글자는 시각 탓이라 가린다 */
     .replace(/시험지 \d+개를 받았습니다|받아 둔 시험지가 모두 최신입니다/g,'');   /* ★ 9/27 — 시험지 받기 끝 알림(#dl · 숨어도 글자는 남는다)도 시각 탓 */
   snap.names={bkNav:!!document.getElementById('bkNav'),PINFOR:typeof window.PINFOR,wzHook:typeof window.wzHook,INKG_EA:typeof window.INKG_EA,QZ:typeof QZ,
     refPaint:typeof refPaint,bwSpotsOn:typeof window.bwSpotsOn};
   if(typeof HASBOOK!=='undefined'&&HASBOOK){
     const r=DATA.find(x=>bpgOf(x)>0);const no=r?r[F.NO]:0,pg=r?bpgOf(r):0;snap.bno=[no,pg];
     try{await bookOpen(pg,true);await until(()=>BK.open&&BK.pgs.length>0&&!BK.loading,25000);await wait(400);
       snap.bkbar=tx($('#book .bkbar'));
       bkQOpen();await wait(400);
       snap.bkq=$$$('#bkqList [data-no]').map(x=>x.dataset.no).join(',');snap.bkqtxt=tx($('#bkqList'));
       const f=$$$('#bkqList [data-no]')[0];if(f){f.click();await wait(1200)}
       snap.bkqPickBookHidden=!vis($('#book'));snap.bkqPickView=vis($('#view'));
     }catch(e){snap.bookErr=String(e)}
     try{if(!$('#view').classList.contains('hide'))closeView()}catch(e){}try{if(BK.open)bkClose()}catch(e){}await wait(300);
     try{bplOpen(no);await wait(400);snap.bpl=tx(document.getElementById('bpl'));
       snap.bplAttr=$$$('#bpl .bplrow').map(x=>Object.keys(x.dataset).join('+')).join(',');
       const b=document.getElementById('bpl');if(b)b.remove();BPLNO=null;cropFor(null)}catch(e){snap.bplErr=String(e)}
   }
   try{const secs=Object.keys(TOC.sec);if(secs.length&&typeof jnOpen==='function'){jnOpen(secs[0]);await wait(700);
     /* ★ 합치기 10/1(하위 에이전트 C) — physphone A-2(97883ef 본문 「이름 = 기출 「연도 출처 N번」」) · A-4(「닫기」 → ✕) 는 뜻한 바뀜(physphone B2 · B4 가 잰다)
        → 두 판 모두 줄 이름 칸(.jnrow .h .mut)과 닫기 단추(#jnwX)를 떼고 나머지 글자를 맞댄다 */
     snap.jn=tx((e=>{if(!e)return e;const c=e.cloneNode(true);c.querySelectorAll('.jnrow .h .mut,#jnwX').forEach(x=>x.remove());return c})(npv(document.getElementById('jnw')))).slice(0,4000);   /* ★ physprev — .q · .pvfig 뗌 */
     const q=$$$('#jnw .jnrow .q')[0];snap.jnq=q?[q.className.replace(/(^| )pv(?= |$)/,'').trim(),q.getAttribute('title')]:null;   /* ★ physprev — .q 의 pv 꼴 뗌 */
     const w=document.getElementById('jnw');if(w)w.remove()}}catch(e){snap.jnErr=String(e)}
   {const it=$$$('#list .item')[0];snap.item=it?[it.className,Object.keys(it.dataset).filter(k=>k!=='pv').join('+'),String((it.querySelector('.prev')||{}).className||'').replace(/(^| )pv(?= |$)/,'').trim()||null]:null}   /* ★ physprev — data-pv · .prev 의 pv 꼴 뗌 */
   N('X-11 스냅숏',{subj:SUBJ_ID,list:(snap.list||'').length,bkq:snap.bkq,names:snap.names});
   try{await __nativeFetch('/snap',{method:'POST',body:JSON.stringify(snap)})}catch(e){}
"""

PHONE = r"""<script>
(function(){
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 const until=async(fn,ms)=>{const t0=Date.now();while(Date.now()-t0<(ms||40000)){try{if(fn())return true}catch(e){}await wait(80)}return false};
 const __nf=window.fetch.bind(window);
 window.fetch=async function(url,opt){
  opt=opt||{};const u=String(url);
  const m=/api\.github\.com\/repos\/([^\/]+\/[^\/]+)\/contents\/([^?]+)/.exec(u);
  if(!m){ if(/^https?:/i.test(u))return {ok:false,status:599,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
          return __nf(url,opt); }
  const path=decodeURIComponent(m[2]);
  if(m[1]==='zzikkaplan/notes')return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
  if((opt.method||'GET')==='PUT')return {ok:true,status:200,json:async()=>({content:{sha:'x'}}),text:async()=>''};
  const r=await __nf('/data/'+encodeURI(path),{cache:'no-store'});
  if(!r.ok)return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
  const acc=(opt.headers||{}).Accept||'';
  if(acc.indexOf('raw')>=0)return r;
  return {ok:true,status:200,json:async()=>({sha:'sha'}),text:async()=>JSON.stringify({sha:'sha'})};
 };
 async function go(){
  try{
   localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}));
   await (async()=>{for(let __i=0;__i<300&&(typeof db==='undefined'||!db);__i++)await new Promise(r=>setTimeout(r,100));return loadEarthData()})()/* ★ 2026-10-08 (_task_jagwa_phys_win 회귀) db 가 설 때까지 — 고정 대기 경합(짐 크면 「db 없음」) · 판정 무변 */;
   await until(()=>DATA.length===704,50000);
   FL.past='y';draw();await wait(250);
   await openView(DATA[0][F.NO]); await wait(900);
   bkWin(true); $('#book').classList.remove('hide'); await wait(500);
   window.__phready=1;
  }catch(e){window.__pherr=String(e&&e.stack||e)}
 }
 if(document.readyState==='complete')setTimeout(go,800);else window.addEventListener('load',()=>setTimeout(go,800));
})();
</script>"""

BODY_XB = r"""
   /* ═══════════ XB — _task_jagwa_earth_bookwin_add1(생물 · 2026-09-25) ═══════════
      바탕 판(bookwin 인도판 f07e9d08 · 생물은 ISEA=false 라 새 기능 없음)에서 돌리면 헛잣대 — main 이 센다.
      표본(생물 studyplandata 실측): B21-58-10(uid G58-10 · 교재 11쪽) · B01-38-01(문항 11 — 옛 판에서 「11쪽」 누르면 뜨던 것)
      · 11쪽 「문항 4」 = B18-55-10 2018 · B19-56-02 2019 · B21-58-10 2021 · B26-63-09 2026 · 「대기」 = B03-40-06(uid G40-06 · 교재 2쪽)
      · 교재 조각 1.1.pdf = 인쇄 2~11 · 1.2.pdf = 12~15 */
   await (async()=>{for(let __i=0;__i<300&&(typeof db==='undefined'||!db);__i++)await new Promise(r=>setTimeout(r,100));return loadEarthData()})()/* ★ 2026-10-08 (_task_jagwa_phys_win 회귀) db 가 설 때까지 — 고정 대기 경합(짐 크면 「db 없음」) · 판정 무변 */;
   await until(()=>DATA.length===746,30000);
   ['jagwa.earth.order','jagwa.earth.coll','jagwa.earth.hmfold','jagwa.view.win',
    'jagwa.win.view','jagwa.win.book','jagwa.win.bplist','jagwa.win.mc','jagwa.win.jn']
     .forEach(k=>{try{localStorage.removeItem(k)}catch(e){}});
   try{_coll=null}catch(e){}
   FL.past='y';FL.q='';FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';
   if(CUR.KINDS)FL.types=new Set(['G','T','E']);
   GG={};GGREF={};PICK={};
   {const rec0=JSON.parse(await (await __nativeFetch('/data/bio/%EA%B8%B0%EB%A1%9D.json')).text());
    UN=rec0.data.unit||{};BPG=rec0.data.bpg||{};MC=rec0.data.mcard||{};CROP=rec0.data.crop||{};TFIX=rec0.data.tfix||{};
    await put('kv','unit',UN);await put('kv','bpg',BPG);await put('kv','mcard',MC);await put('kv','crop',CROP);await put('kv','tfix',TFIX);
    if(typeof jgMigrate==='function')await jgMigrate('boot');   /* ★ jagwa_uid(9/29) — 실기기는 이 손값이 부팅 전부터 kv 에 있어 부팅 때 옮겨진다 · 하네스는 부팅 뒤에 넣으니 같은 옮김을 한 번(바탕 앱엔 없음) */
    try{refreshUnits()}catch(e){}}
   draw(); await wait(400);
   const NEW=!!document.getElementById('bkNav');
   addEventListener('unhandledrejection',e=>{N('XB 거부 스택',String((e.reason&&e.reason.stack)||e.reason).slice(0,700))});
   N('XB 밑준비',{subj:SUBJ_ID,HASBOOK:HASBOOK,ISEA:ISEA,HASJOGAK:HASJOGAK,DATA:DATA.length,새판:NEW,
     이름:{wzHook:typeof window.wzHook,PINFOR:typeof window.PINFOR,INKG_EA:typeof window.INKG_EA,bwSpotsOn:typeof window.bwSpotsOn}});
   const zOf=el=>el?(+getComputedStyle(el).zIndex||0):-1;
   /* ★ A-6(d) 9/30 _task_qa_baseline — jagwa_uid(9/29 · 5e18424) 뒤 표본 번호가 새 꼴(B21-58-10 · B03-40-06) · 바탕 앱(f07e9d08)의 codeShow 는 옛 꼴이라 못 찾아 XB-E·F·J 묶음이 멈춤 → 데이터 uid(F.CODE)로도 찾는다(새 판은 codeShow 먼저 · 같은 줄) */
   const byCode=cs=>DATA.find(r=>codeShow(r)===cs)||DATA.find(r=>r[F.CODE]===cs)||null;
   const noOf=cs=>{const r=byCode(cs);return r?r[F.NO]:0};
   const cur=()=>{try{const p=bkCurPage();return p?p.pr:0}catch(e){return 0}};
   const bkReady=async(ms)=>{await until(()=>BK.open&&BK.pgs&&BK.pgs.length>0&&!BK.loading&&cur()>0,ms||25000);await wait(250)};
   const vis=el=>!!el&&!el.classList.contains('hide')&&getComputedStyle(el).display!=='none';
   const closeAll=async()=>{try{if(window.PINFOR&&window.bwPinEnd)bwPinEnd()}catch(e){}
     try{if(BK.open)bkClose()}catch(e){} try{if(!$('#view').classList.contains('hide'))closeView()}catch(e){}
     ['bpl','mcw','jnw','tfxSheet','bkrefpop','bkreftag','crmenu'].forEach(id=>{const e=document.getElementById(id);if(e)e.remove()});
     $$$('.sheet.shfloat').forEach(x=>x.remove());$$$('.sheet.xmodal').forEach(x=>x.remove());
     try{$('#bkq').classList.add('hide')}catch(e){}
     BPLNO=null;try{cropFor(null)}catch(e){}await wait(250)};
   const toasts=()=>$$$('.toast').map(x=>txt(x));
   const PE=(t,x,y,pt,id,o)=>{const e=new Event(t,{bubbles:true,cancelable:true});
     const v=Object.assign({clientX:x,clientY:y,pageX:x,pageY:y,pointerType:pt||'pen',pointerId:id||31,isPrimary:true,pressure:.5,
       button:0,buttons:1,width:pt==='touch'?10:1,height:pt==='touch'?10:1},o||{});
     Object.keys(v).forEach(k=>Object.defineProperty(e,k,{get:()=>v[k]}));
     Object.defineProperty(e,'getCoalescedEvents',{value:()=>[]});return e};
   const send=(el,t,x,y,pt,id,o)=>el.dispatchEvent(PE(t,x,y,pt,id,o));
   const click=el=>el.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));
   const keyEnter=el=>el.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true,cancelable:true}));
   const pgInput=async v=>{const i=document.getElementById('bkPg');if(!i)return false;i.value=String(v);keyEnter(i);await wait(300);await until(()=>!BK.loading,20000);await wait(250);return true};
   const pageRect=pr=>{const p=BK.pgs.find(x=>x.pr===pr);return p&&p.el?p.el.getBoundingClientRect():null};
   const vpRect=()=>document.getElementById('bkvp').getBoundingClientRect();
   const inPage=(pr,fx,fy)=>{const a=pageRect(pr),v=vpRect();if(!a)return null;
     const x0=Math.max(a.left,v.left+10),x1=Math.min(a.right,v.right-10),y0=Math.max(a.top,v.top+10),y1=Math.min(a.bottom,v.bottom-10);
     if(x1<=x0||y1<=y0)return null;return [x0+(x1-x0)*fx,y0+(y1-y0)*fy]};
   const bkDrag=async(pr,a,b,pt,id)=>{const vp=document.getElementById('bkvp');const p0=inPage(pr,a[0],a[1]),p1=inPage(pr,b[0],b[1]);if(!p0||!p1)return false;
     send(vp,'pointerdown',p0[0],p0[1],pt,id);await wait(40);
     send(vp,'pointermove',(p0[0]+p1[0])/2,(p0[1]+p1[1])/2,pt,id);await wait(40);
     send(vp,'pointermove',p1[0],p1[1],pt,id);await wait(40);
     send(vp,'pointerup',p1[0],p1[1],pt,id);await wait(500);return true};
   const G58=noOf('B21-58-10'), G38=noOf('B01-38-01'), WN=noOf('B03-40-06');
   N('XB 표본',{G21_58_30:[G58,G58&&bpgOf(rec(G58))],G01_38_1:G38,대기:[WN,WN&&bpgOf(rec(WN)),WN&&bpgWait(rec(WN))],
     조각:[(pieceFor(11)||{}).file,(pieceFor(12)||{}).file]});

   /* ── XB-A 📖 p11 목록 창 「11쪽」 = 교재만(문항 11 B01-38-01 이 안 뜬다) ── */
   await grp('XB-A', async()=>{
     await closeAll();
     const one=async(open)=>{if(open){await bookOpen(5,true);await bkReady()}
       bplOpen(G58);await wait(400);
       const row=$$$('#bpl .bplrow').find(r=>txt(r.querySelector('.pr'))==='11쪽');
       const v0=VNO;if(row)click(row);await wait(500);await bkReady(20000);
       const r={row:!!row,book:vis($('#book')),info:txt($('#bkInfo')),view:vis($('#view')),VNO:VNO,v0:v0,G38:G38,bpl:!!document.getElementById('bpl'),at:cur()};
       await closeAll();return r};
     let r=await one(false);
     T('XB-A1 B21-58-10 목록 창 「11쪽」 → 교재 11쪽 · 문항 창 안 뜸 · VNO 무변 · 목록 창 남음',
       r.row&&r.book&&r.at===11&&!r.view&&r.VNO===r.v0&&r.bpl,r);
     T('XB-A2 문항 11(B01-38-01)이 안 열린다(옛 판 = 쪽 번호를 문항 번호로 읽어 B01-38-01 이 떴다)',r.row&&r.VNO!==G38,r);
     r=await one(true);
     T('XB-A3 교재가 이미 열린 채 눌러도 같음(5쪽 → 11쪽)',r.row&&r.book&&r.at===11&&!r.view&&r.VNO===r.v0,r);
   });

   /* ── XB-D·B 「이 쪽의 문항」 연도 내림 · 누르면 교재 그대로 · 창 쌓임 ── */
   await grp('XB-D', async()=>{
     await closeAll();
     await bookOpen(11,true);await bkReady();await bkGoto(11);await wait(300);
     bkQOpen();await wait(500);
     const rows=$$$('#bkqList [data-no]');
     const yrs=rows.map(r=>+(rec(+r.dataset.no)[F.YEAR])||0), cs=rows.map(r=>codeShow(rec(+r.dataset.no)));
     N('XB-D 11쪽 줄',cs.map((c,i)=>c+'/'+yrs[i]));
     T('XB-D1 11쪽 「문항 4」 = 2026 → 2021 → 2019 → 2018',JSON.stringify(yrs)==='[2026,2021,2019,2018]',yrs);
     T('XB-D2 줄마다 연도 글자(.yr)',rows.length===4&&rows.every((r,i)=>{const y=r.querySelector('.yr');return y&&+txt(y)===yrs[i]}),rows.map(r=>txt(r)));
     const r0=rows[0];if(r0)click(r0);await wait(900);
     const V=$('#view'),B=$('#book');
     T('XB-D3 줄 누름 → 교재 창 그대로 · 문항 창 뜸 · 문항 z 최상',!!r0&&vis(B)&&vis(V)&&VNO===+r0.dataset.no&&zOf(V)>=Math.max(zOf(B),zOf($('#bkq'))),
       [vis(B),vis(V),VNO,r0&&+r0.dataset.no,zOf(V),zOf(B),zOf($('#bkq'))]);
     send(B.querySelector('.panel'),'pointerdown',10,10,'mouse',51);send(B.querySelector('.panel'),'pointerup',10,10,'mouse',51);await wait(150);
     T('XB-B1 교재 판을 누르면 교재 z > 문항 z(교재가 앞)',V.classList.contains('win')&&zOf(B)>zOf(V),[V.className,zOf(B),zOf(V)]);
     send(V,'pointerdown',10,10,'mouse',52);send(V,'pointerup',10,10,'mouse',52);await wait(150);
     T('XB-B2 문항을 누르면 문항 z > 교재 z(문항이 앞)',zOf(V)>zOf(B),[zOf(V),zOf(B)]);
     const r1=$$$('#bkqList [data-no]')[1];if(r1){click(r1);await wait(900)}
     T('XB-D4 다른 줄 누름 → 문항만 바뀜(교재 그대로)',!!r1&&VNO===+r1.dataset.no&&vis(B),[r1&&+r1.dataset.no,VNO,vis(B)]);
     await closeAll();
   });

   /* ── XB-C ◀ [쪽] ▶ · ↩ · 조각 경계(1.1.pdf → 1.2.pdf) ── */
   await grp('XB-C', async()=>{
     await closeAll();
     await bookOpen(11,true);await bkReady();await bkGoto(11);await wait(300);
     const bb=()=>document.getElementById('bkBack');
     T('XB-C0 머리줄 #bkInfo 바로 뒤 ◀ [쪽] ▶',!!document.getElementById('bkNav')&&$('#bkInfo').nextElementSibling===document.getElementById('bkNav'),
       ($('#bkInfo').nextElementSibling||{}).id);
     const s0=cur();
     await pgInput(5);
     T('XB-C1 쪽 칸 5 Enter → 5쪽 · 「↩ 11쪽」',cur()===5&&!!bb()&&!bb().hidden&&txt(bb())==='↩ 11쪽',[s0,cur(),bb()&&txt(bb())]);
     click(bb());await wait(600);await until(()=>!BK.loading&&cur()===11,15000);
     T('XB-C2 ↩ 누름 → 11쪽',cur()===11,cur());
     click($('#bkNextP'));await wait(600);await until(()=>!BK.loading&&cur()===12,20000);const s1=cur();
     T('XB-C3 ▶ 11 → 12(1.1.pdf → 1.2.pdf 조각 넘김)',s1===12&&(pieceFor(11)||{}).file==='1.1.pdf'&&(pieceFor(12)||{}).file==='1.2.pdf',[s1,(pieceFor(11)||{}).file,(pieceFor(12)||{}).file]);
     click($('#bkPrevP'));await wait(600);await until(()=>!BK.loading&&cur()===11,20000);
     T('XB-C4 ◀ 12 → 11',cur()===11,cur());
     const at=cur();await pgInput(999);await wait(150);
     T('XB-C5 999 → 이동 없음 · 토스트 「999쪽 — 교재에 없는 쪽」',cur()===at&&toasts().some(x=>x.indexOf('999쪽 — 교재에 없는 쪽')>=0),[at,cur(),toasts().slice(-3)]);
     bkClose();await wait(300);
     T('XB-C6 교재 닫으면 ↩ 숨김',!!bb()&&bb().hidden,bb()?bb().hidden:'(없음)');
     await closeAll();
   });

   /* ── XB-E 「대기」 문항 📍 찍기 → 「대기」 사라지고 ✓ · BPG[uid].b ── */
   await grp('XB-E', async()=>{
     await closeAll();
     const wr=rec(WN),uid=wr[F.CODE],keep=JSON.stringify(BPG[uid]||null),pg=bpgOf(wr);
     T('XB-E0 표본 B03-40-06 = 「대기」(문장근거 절시작·대기 · BPG 없음)',bpgWait(wr)&&pg>0,[bpgWait(wr),pg]);
     await openView(WN);await wait(800);
     const cb=()=>document.getElementById('cBpg');
     T('XB-E1 카드 칩 「대기」',!!cb()&&txt(cb())==='대기',cb()?txt(cb()):'(없음)');
     await bookOpen(pg,true);await bkReady();await bkGoto(pg);await wait(300);
     const pk=()=>document.getElementById('bkPick');
     T('XB-E2 문항을 연 채 교재 → 머리줄 📍',!!pk()&&!pk().hidden&&txt(pk())==='📍',pk()?[pk().hidden,txt(pk())]:'(없음)');
     if(pk())click(pk());await wait(300);
     T('XB-E3 📍 누름 → 찍는 문항 칩 「📍 찍는 문항 B03-40-06 …」',window.PINFOR===WN&&/^📍 찍는 문항 B03-40-06/.test(txt($('#bkFor'))),[window.PINFOR,txt($('#bkFor'))]);
     await bkDrag(pg,[0.2,0.3],[0.6,0.45],'pen',72);
     const v=BPG[uid];
     T('XB-E4 펜 끌기 → BPG[G40-06] = {ps:[쪽],last:쪽,b:[쪽,x0,y0,x1,y1]}',!!v&&JSON.stringify(v.ps)===JSON.stringify([pg])&&v.last===pg&&Array.isArray(v.b)&&v.b.length===5&&v.b[0]===pg&&v.b[3]>v.b[1]&&v.b[4]>v.b[2],v);
     await wait(300);
     const it=$$$('#list .item').find(x=>txt(x.querySelector('.num'))==='B03-40-06');
     try{showProblem()}catch(e){}await wait(500);
     T('XB-E5 「대기」 사라짐(bpgWait 거짓 · 목록 줄 .wait 없음) · 카드 칩 ✓',!bpgWait(wr)&&(!it||!it.querySelector('.wait'))&&!!cb()&&txt(cb())==='✓',
       [bpgWait(wr),it?!!it.querySelector('.wait'):'(줄 안 보임)',cb()?txt(cb()):null]);
     if(keep!=='null')BPG[uid]=JSON.parse(keep);else delete BPG[uid];await saveBPG();
     await closeAll();
   });

   /* ── XB-F 📋 정리 창 글씨 ── */
   await grp('XB-F', async()=>{
     await closeAll();
     const sec=(unitOf(G58)||'1.1').split('.').slice(0,2).join('.');jnOpen(sec);await wait(800);
     const fs=q=>{const e=$$$(q)[0];return e?[parseFloat(getComputedStyle(e).fontSize),getComputedStyle(e).fontWeight]:null};
     const S={jnh:fs('#jnw .jnh'),mut:fs('#jnw .jnrow .h .mut'),q:fs('#jnw .jnrow .q'),jnans:fs('#jnw .jnrow .jnans')};
     /* ★ uid_unify G-1(10/4) — 생물도 기출 uid 줄에서 .mut 을 안 그리게 됐으나 G-1 의 전제(uid 회·번 = 데이터 회차·문번)는 지학만 맞다(생물 기출 uid 270 중 260 은 뒷자리가 문번이 아니다 · 본 세션 10/4 23:05) → 사용자 결정 전 = 안 받는다.
        결정 (가) 생물도 걷음 → G1_BIO_JS=true(줄 머리 .mut 의 CSS 규칙 글자를 임시 .mut 로 잼) · (다) 지학만 → false 그대로(앱이 생물 줄 이름을 되살리면 줄의 .mut 로 PASS) */
     const G1_BIO_JS=false;
     if(G1_BIO_JS&&!S.mut&&typeof ynUid==='function'){const h=$$$('#jnw .jnrow .h')[0];if(h){const sp=document.createElement('span');sp.className='mut';sp.textContent='x';h.appendChild(sp);
       S.mut=[parseFloat(getComputedStyle(sp).fontSize),getComputedStyle(sp).fontWeight];sp.remove()}}
     N('XB-F 크기',{sec,S});
     T('XB-F1 줄 머리(.mut) 10px 굵게',!!S.mut&&S.mut[0]===10&&+S.mut[1]>=700,S.mut);
     T('XB-F2 단원 머리 11px · 문제 글 12.5px(그대로)',!!S.jnh&&S.jnh[0]===11&&!!S.q&&S.q[0]===12.5,[S.jnh,S.q]);
     {const w=document.getElementById('jnw');if(w)w.remove()}
   });

   /* ── XB-H 문제 창 손바닥 ── */
   await grp('XB-H', async()=>{
     await closeAll();
     let noH=0;const W=$('#cardwrap'),C=$('#card');
     /* ★ bio ocrfix §K(2026-09-25) — 〈보기〉 설명이 해설을 열기 전엔 숨는다(.bexp[hidden]) → 생물 카드가 짧아져
        세 표본이 닫힌 채로는 다 창 안에 든다(새 판 실측 B05-42-01 644=644). 이 묶음은 「굴릴 수 있는 카드」만 있으면 되니
        닫힌 채 모자라면 그 표본의 정답·해설을 펼쳐(앱이 선택지를 누를 때와 같은 details.open) 길이를 번다 · 어느 쪽이었는지 NOTE 로 남긴다 */
     let hOpen=false;
     for(const cs of ['B12-49-09','B26-63-02','B05-42-01']){noH=noOf(cs);await openView(noH);await wait(900);if(W.scrollHeight>W.clientHeight+100)break;
       const d=$('#cDet');if(d&&!d.open){d.open=true;await wait(400);if(W.scrollHeight>W.clientHeight+100){hOpen=true;break}}}
     N('XB-H 표본',{code:codeShow(rec(noH)),'정답·해설':hOpen?'펼침':'닫힘',h:[W.scrollHeight,W.clientHeight]});
     T('XB-H0 카드가 창보다 길다(표본 '+codeShow(rec(noH))+')',W.scrollHeight>W.clientHeight+100,[W.scrollHeight,W.clientHeight]);
     T('XB-H1 #cardwrap touch-action = none',getComputedStyle(W).touchAction==='none',getComputedStyle(W).touchAction);
     const r=W.getBoundingClientRect(),x=r.left+r.width*0.5,y=r.top+r.height*0.5;
     const el=document.elementsFromPoint(x,y).find(e=>C.contains(e))||C;
     W.scrollTop=80;await wait(100);
     send(el,'pointerdown',x,y,'touch',91);send(el,'pointermove',x,y-15,'touch',91);send(el,'pointermove',x,y-30,'touch',91);await wait(60);
     const moved=W.scrollTop;
     send(el,'pointerdown',x+60,y,'pen',92);await wait(40);const s1=W.scrollTop;
     send(el,'pointermove',x,y-60,'touch',91);await wait(40);const s2=W.scrollTop;
     send(el,'pointermove',x+70,y+5,'pen',92);send(el,'pointerup',x+70,y+5,'pen',92);send(el,'pointerup',x,y-60,'touch',91);await wait(60);
     T('XB-H2 손가락 30px 끈 뒤 펜 획 → scrollTop 80(되돌림) · 그 손가락 계속 끌어도 80',moved!==80&&s1===80&&s2===80,[moved,s1,s2]);
     await wait(1600);
     send(el,'pointerdown',x,y,'touch',94);send(el,'pointermove',x,y-21,'touch',94);send(el,'pointermove',x,y-42,'touch',94);send(el,'pointerup',x,y-42,'touch',94);await wait(60);
     T('XB-H3 1.6초 뒤 손가락 → 굴림',W.scrollTop!==80,W.scrollTop);
     W.scrollTop=80;await wait(60);
     send(el,'pointerdown',x,y,'touch',95,{width:50,height:50});send(el,'pointermove',x,y-40,'touch',95,{width:50,height:50});send(el,'pointerup',x,y-40,'touch',95,{width:50,height:50});await wait(60);
     /* ★ penfinger A(2026-09-25) — X-H6 과 같다(ⓒ 걷음 · 펜 뗀 지 1.6초 넘은 굵은 손가락은 굴린다) */
     T('XB-H4 접촉면 50px 손가락(펜 뗀 지 1.6초 넘음) → 굴림 — ⓒ 크기 손바닥 걷음(penfinger A)',W.scrollTop!==80,W.scrollTop);
     await closeAll();
   });

   /* ── XB-I 문제 창 확대 ── */
   await grp('XB-I', async()=>{
     await closeAll();
     await openView(noOf('B12-49-09'));await wait(900);
     const W=$('#cardwrap'),C=$('#card');
     const sc=()=>{const m=/scale\(([\d.]+)\)/.exec(C.style.transform||'');return m?+m[1]:1};
     const r=W.getBoundingClientRect(),cx=r.left+r.width*0.45,cy=r.top+r.height*0.45;
     const el=document.elementsFromPoint(cx,cy).find(e=>C.contains(e))||C;
     const k0=sc();
     send(el,'pointerdown',cx-50,cy,'touch',101);send(el,'pointerdown',cx+50,cy,'touch',102);await wait(30);
     send(el,'pointermove',cx+150,cy,'touch',102);await wait(80);const k1=sc();
     send(el,'pointerup',cx+150,cy,'touch',102);send(el,'pointerup',cx-50,cy,'touch',101);await wait(80);
     T('XB-I1 두 손가락 벌림 → scale 커짐',k1>k0,[k0,k1]);
     const k3=sc();C.dispatchEvent(new WheelEvent('wheel',{deltaY:-120,clientX:cx,clientY:cy,ctrlKey:true,bubbles:true,cancelable:true}));await wait(80);
     T('XB-I2 Ctrl+휠 → 배율 바뀜',sc()!==k3,[k3,sc()]);
     T('XB-I3 화면에 배율 숫자·단추 0',!$$$('#view *').some(e=>e.children.length===0&&/^\s*[−-]?\s*\d{2,3}\s*%\s*$/.test(e.textContent||''))&&!document.getElementById('vzWrap'));
     try{if(window.INKG_EA&&INKG_EA.pinch)INKG_EA.pinch.set(1,cx,cy)}catch(e){}
     await closeAll();
   });

   /* ── XB-J 미리보기 글자 고치기 — 목록 줄 길게 → 정리 창 줄도 같이 ── */
   await grp('XB-J', async()=>{
     await closeAll();
     const r=rec(G58),uid=r[F.CODE],no=G58,orig=txtOrig(uid,'q'),keep=JSON.stringify(TFIX[uid]||null);
     delete TFIX[uid];await put('kv','tfix',TFIX);FL.q='B21-58-10';draw();await wait(400);
     const sec=(unitOf(no)||'1.1').split('.').slice(0,2).join('.');jnOpen(sec);await wait(800);
     const prev=()=>$$$('#list .item').map(it=>it.querySelector('.prev')).find(p=>p&&txt(p.closest('.item').querySelector('.num'))==='B21-58-10');
     const jq=()=>{const jr=$$$('#jnw .jnrow').find(x=>+x.dataset.no===no);return jr?jr.querySelector('.q'):null};
     N('XB-J 표본',{uid,no,sec,prev:!!prev(),jn:!!jq()});
     const long=async el=>{const b=el.getBoundingClientRect();send(el,'pointerdown',b.left+8,b.top+6,'mouse',111);await wait(700);
       send(el,'pointerup',b.left+8,b.top+6,'mouse',111);click(el);await wait(300)};
     const p=prev();if(p)await long(p);
     let S=document.getElementById('tfxSheet');
     T('XB-J1 목록 줄 .prev 길게 누름 → 「✎ 글자 고치기」 시트 · 문항 창 안 열림',!!S&&$('#view').classList.contains('hide'),[!!S,VNO]);
     const NEWQ='검산 새 글 — 생물 문제 글자';
     if(S){S.querySelector('#tfxIn').value=NEWQ;click(S.querySelector('#tfxOk'));await wait(800)}
     T('XB-J2 저장 → TFIX[G58-10].q · 목록 줄 · 정리 창 줄 = 새 글 · 둘 다 .fx',!!TFIX[uid]&&TFIX[uid].q===NEWQ&&!!prev()&&txt(prev())===NEWQ&&prev().classList.contains('fx')&&!!jq()&&txt(jq())===NEWQ&&jq().classList.contains('fx'),
       [TFIX[uid],prev()&&txt(prev()).slice(0,30),jq()&&txt(jq()).slice(0,30)]);
     if(prev())await long(prev());S=document.getElementById('tfxSheet');
     if(S){click(S.querySelector('#tfxDel'));await wait(900)}
     T('XB-J3 되돌리기 → 둘 다 원본 · .fx 없음',!(TFIX[uid]&&TFIX[uid].q)&&!!prev()&&txt(prev())===orig.replace(/\s+/g,' ').trim()&&!prev().classList.contains('fx')&&!!jq()&&!jq().classList.contains('fx'),
       [TFIX[uid],prev()&&txt(prev()).slice(0,30)]);
     if(keep!=='null')TFIX[uid]=JSON.parse(keep);else delete TFIX[uid];await put('kv','tfix',TFIX);
     FL.q='';draw();await closeAll();{const w=document.getElementById('jnw');if(w)w.remove()}
   });
   try{await __nativeFetch('/snap',{method:'POST',body:JSON.stringify(snap)})}catch(e){}
"""


def _cap_head():
    """앱의 `<style>` 을 그대로 실어 캡처가 실물과 같은 모양이 되게 한다(픽셀 게이트 아님 · 사람 눈 확인용)."""
    try:
        html = io.open(SRC, encoding='utf-8', newline='').read()
        css = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', html, re.S))
    except Exception:
        css = ''
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            '<title>지학 add1 — DOM 캡처</title><style>' + css + '</style>'
            '<style>body{background:var(--paper);padding:20px}'
            '#esh,.panel{position:static!important;left:auto!important;top:auto!important;'
            'width:min(900px,96vw)!important;height:auto!important;max-height:none!important;'
            'box-shadow:0 8px 30px rgba(0,0,0,.18);border-radius:12px;overflow:visible}'
            '.twgrip{display:none}h1.capt{font-size:13px;color:#4A5661;font-weight:600;margin:0 0 10px}'
            '</style></head><body data-subj="earth" data-layer="card">'
            '<h1 class="capt">지학 add1 — 헤드리스 DOM 캡처(픽셀 게이트 아님 · 사람 눈 확인용)</h1>')


CAPHEAD = _cap_head()



def build(mode, src_text):
    subj = {'earth': 'earth', 'earthbase': 'earth', 'bio': 'bio', 'biobase': 'bio',
            'phys': 'phys', 'physbase': 'phys',
            'x': 'earth', 'xbase': 'earth', 'xbio': 'bio', 'xbiobase': 'bio', 'xphys': 'phys', 'xphysbase': 'phys',
            'xb': 'bio', 'xbbase': 'bio'}[mode]
    body = {'earth': BODY_EARTH, 'earthbase': BODY_EARTH,
            'bio': BODY_BIO, 'biobase': BODY_BIO,
            'x': BODY_X, 'xbase': BODY_X, 'xbio': BODY_XSIDE, 'xbiobase': BODY_XSIDE,
            'xphys': BODY_XSIDE, 'xphysbase': BODY_XSIDE,
            'xb': BODY_XB, 'xbbase': BODY_XB}.get(mode, BODY_PHYS)
    if QC.REGRESS:   # regress · smoke — 쪽 안 JS 를 이 자리에서만 고쳐 쓴다(BODY_* 글자는 gate 와 같은 것 그대로 · 표본 · 헛잣대 끔 · smoke 자르기)
        body = _rg_body(mode, body)
    html = src_text
    html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js',
                        STUB.replace('__SUBJ__', subj) + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    open(os.path.join(OUT, 'app.html'), 'w', encoding='utf-8', newline='').write(
        html.replace('</body>', HEAD + body + TAIL + '</body>', 1))
    open(os.path.join(OUT, 'phone.html'), 'w', encoding='utf-8', newline='').write(
        html.replace('</body>', PHONE + '</body>', 1))
    return subj


def run(mode, secs, src_text):
    QC.launch('base' if mode.endswith('base') else 'new')   # 셈(§B-4) — 바탕 묶음(…base)은 gate 에서만 돈다
    subj = build(mode, src_text)
    spd = os.path.join(SPDROOT, subj)
    done = threading.Event()
    box = {}

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=OUT, **k)

        def log_message(self, *a, **k):
            pass

        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            if p.startswith('/data/'):
                rel, pre = p[6:], subj + '/'
                if not rel.startswith(pre):
                    self.send_response(404); self.end_headers(); return
                f = os.path.join(spd, rel[len(pre):].replace('/', os.sep))
                if not os.path.isfile(f):
                    self.send_response(404); self.end_headers(); return
                b = open(f, 'rb').read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', str(len(b)))
                self.send_header('X-Sha', hashlib.sha1(b).hexdigest())
                self.end_headers(); self.wfile.write(b); return
            return super().do_GET()

        def do_POST(self):
            n = int(self.headers.get('Content-Length') or 0)
            body = self.rfile.read(n).decode('utf-8', 'replace')
            self.send_response(204); self.end_headers()
            if self.path.startswith('/partial'):
                box['partial'] = body; return
            if self.path.startswith('/snap'):
                try: box['snap'] = json.loads(body)
                except Exception: box['snap'] = {}
                return
            if self.path.startswith('/cap'):
                q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                nm = (q.get('n') or ['cap'])[0]
                if QC.GATE:   # regress — DOM 캡처(사람 눈 확인용 · 게이트 아님 · 하네스 옆 _cap_bp)를 안 쓴다
                    open(os.path.join(CAP, nm + '.html'), 'w', encoding='utf-8', newline='').write(
                        CAPHEAD + body + '</body></html>')
                box.setdefault('caps', []).append(nm)
                return
            box['txt'] = body; done.set()

    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    prof = os.path.join(OUT, 'prof_' + mode)
    shutil.rmtree(prof, ignore_errors=True)
    t0 = time.time()
    p = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
                          '--user-data-dir=' + prof, '--window-size=1500,950',
                          'http://127.0.0.1:%d/app.html' % port],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    got = done.wait(secs)
    p.terminate()
    try: p.wait(10)
    except Exception: p.kill()
    srv.shutdown()
    print('  [%s] %.0fs' % (mode, time.time() - t0))
    if not got:
        return (['FAIL | %s 묶음이 시간 안에 안 끝났다 | %s'
                 % (mode, box.get('partial', '(중간 결과 없음)')[-3000:])], box.get('snap'))
    return ([ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()], box.get('snap'))


def static_checks():
    b = open(SRC, 'rb').read()
    s = b.replace(b'\r\n', b'\n').decode('utf-8')
    base = open(BASE, 'rb').read().replace(b'\r\n', b'\n').decode('utf-8') if QC.GATE else None   # regress — 본판 사본 안 읽음(본판 셈 칸 = 기준 스냅샷)
    out = []

    # ★ add17·add18·add19 — 바탕(`68216cf` = add9 까지 든 판)과 **줄로 맞댄다**.
    #   `_base_bp.html`(129eedb)은 껍데기 앞 판이라 이 셋을 재는 자리가 아예 없다.
    if QC.GATE:   # regress — 바탕 68216cf(add9 판) git show 0 · 그 판으로 재는 헛잣대 일곱 · 0-바탕 줄 = gate 만(그 판에만 뜻)
        import subprocess as _sp
        _prev = None
        for _rev in ('68216cf', 'HEAD', 'HEAD~1', 'HEAD~2', 'HEAD~3'):
            try:
                _b = _sp.run(['git', '-C', GENIE, 'show', _rev + ':jagwa/index.html'],
                             capture_output=True).stdout
            except Exception:
                continue
            if _b and hashlib.md5(_b.replace(b'\r\n', b'\n')).hexdigest() == '773962ce59842d75d44d32ef3db34c16':
                _prev = _b.replace(b'\r\n', b'\n').decode('utf-8'); break

    def T2(name, cond, info=''):
        out.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))

    if QC.GATE:
        if _prev is None:
            out.append('FAIL | 0-바탕(773962ce · add9 까지 든 판)을 못 찾았다 — 헛잣대를 못 잰다')
        else:
            P = _prev
            T2('add17 ★헛잣대 ① 바탕 판에는 확대 단추(#vzOut·#vzFit)가 **있고** 이 판에는 없다',
               ("id=\"vzOut\"" in P) and ('vzOut' not in s) and ('vzFit' not in s),
               [P.count('vzOut'), s.count('vzOut'), s.count('vzFit')])
            T2('add17 ★헛잣대 ② 바탕 판은 `await _ov(...)` **뒤에야** vwApply 다(이 판은 앞에도 있다)',
               ('cropFor(null);const r=await _ov(no,list);vwApply' in P)
               and ('try{vwApply(vwOn())}catch(e){}\n     const r=await _ov(no,list);vwApply(vwOn());' in s),
               [P.count('vwApply(vwOn())'), s.count('vwApply(vwOn())')])
            T2('add17 ★헛잣대 ③ 바탕 판에는 `#pRow1>#mP` 먹색 규칙이 **없다**(그래서 흰 바탕이었다)',
               ('#pRow1>#mP{background:var(--ink)' not in P)
               and ('#pRow1>#mP{background:var(--ink);color:#fff;border-color:var(--ink)}' in s))
            T2('add18 ★헛잣대 ④ 바탕 판 분류 칩은 **넷**(타기출 포함) · 이 판은 **셋**',
               ("['p','타기출',nT]" in P) and ("['p','타기출',nT]" not in s)
               and ("[['','전체',T.length],['y','기출',nY],['n','기본',nN]]" in s))
            T2('add18 ★헛잣대 ⑤ 바탕 판 물리 `kindOf` 는 `SRC` 가 있으면 「T(타기출)」 딱지 · 이 판은 딱지 없음',
               ("return r[F.SRC]?'T':'';" in P) and ("return r[F.SRC]?'T':'';" not in s))
            T2('add18 ★헛잣대 ⑥ 바탕 판에는 유령 누름 막이(tapEat)·톡 조건(TAP_SEL)이 없다',
               ('tapEat' not in P) and ('TAP_SEL' not in P) and ('function tapEat(' in s) and ('var TAP_SEL=' in s))
            T2('add18 ★ `makeFloat` 끌기에서 단추·링크를 뺀다(iOS 에서 「서재」·✕ 가 죽지 않게)',
               ("closest('button,a,[data-tool],[data-nodrag],#bktools,input,select,textarea')" in s)
               and ("closest('button,[data-tool],#bktools,input,select')" in P))
            T2('add19 ★헛잣대 ⑦ 바탕 판에는 `shellSeq` 가 없고 `navList` 가 `filtered()` 를 그대로 돌려준다',
               ('function shellSeq(' not in P)
               and ('const L=filtered(); if(L&&L.length)return L.map(r=>r[F.NO]);' in P)
               and ('function shellSeq(' in s) and ('function shellL(' in s))
            T2('add19 ★첫 화면·서랍·넘기기 목록이 **모두** `shellSeq` 를 쓴다(거르개가 한 곳이다)',
               s.count('shellSeq(') >= 4
               and 'shellSeq(L,rnd,{coll:true})' in s
               and s.count("shellSeq(s.L,s.rnd,{coll:false,chips:false})") == 2,
               [s.count('shellSeq('), s.count("shellSeq(s.L,s.rnd,{coll:false,chips:false})")])
            T2('add19 옛 몸통(_drawEarthListOld)은 남겨 두되 **아무 데서도 안 부른다**',
               s.count('_drawEarthListOld') == 2 and '_drawEarthListOld(' in s)
            T2('add18 물리 목록 `pass` 는 `phPast` 한 함수에 맡긴다(거르개 두 군데 금지 · add12 교훈)',
               'if(PHCLS()){ if(!phPast(r))return 0; }' in s)
            T2('add17 배율 값·기억(jagwa.win.view.zoom)·창 크기 따라 그리기는 **그대로 산다**',
               ("VWZ_K='jagwa.win.view.zoom'" in s) and ('function vzSet(z){' in s)
               and ('new ResizeObserver(()=>{clearTimeout(VRZT);VRZT=setTimeout(vReflow,150)})' in s))

    else:   # regress — 68216cf 를 안 꺼내므로 헛잣대 일곱 · 0-바탕 줄은 없다 · 같은 갈래 안 새 판 글자 칸 다섯은 그대로 잰다
        T2('add18 ★ `makeFloat` 끌기에서 단추·링크를 뺀다(iOS 에서 「서재」·✕ 가 죽지 않게)',
           ("closest('button,a,[data-tool],[data-nodrag],#bktools,input,select,textarea')" in s))   # regress — 바탕(68216cf) 옛 꼴 조건은 고정 옛 판 사실이라 뺌(새 판 조건만)
        T2('add19 ★첫 화면·서랍·넘기기 목록이 **모두** `shellSeq` 를 쓴다(거르개가 한 곳이다)',
           s.count('shellSeq(') >= 4
           and 'shellSeq(L,rnd,{coll:true})' in s
           and s.count("shellSeq(s.L,s.rnd,{coll:false,chips:false})") == 2,
           [s.count('shellSeq('), s.count("shellSeq(s.L,s.rnd,{coll:false,chips:false})")])
        T2('add19 옛 몸통(_drawEarthListOld)은 남겨 두되 **아무 데서도 안 부른다**',
           s.count('_drawEarthListOld') == 2 and '_drawEarthListOld(' in s)
        T2('add18 물리 목록 `pass` 는 `phPast` 한 함수에 맡긴다(거르개 두 군데 금지 · add12 교훈)',
           'if(PHCLS()){ if(!phPast(r))return 0; }' in s)
        T2('add17 배율 값·기억(jagwa.win.view.zoom)·창 크기 따라 그리기는 **그대로 산다**',
           ("VWZ_K='jagwa.win.view.zoom'" in s) and ('function vzSet(z){' in s)
           and ('new ResizeObserver(()=>{clearTimeout(VRZT);VRZT=setTimeout(vReflow,150)})' in s))
    blk = s.find('\nif(SHELL){\n')
    end = s.find('\n}\n/*/EARTH:js*/')
    keys = ['var ISEA=', 'function shellBuild(', 'function drawEarthList(', 'var mcwOpen=async function(',
            'function jnOpen(', 'function ggLineHTML(', 'var ggAdd=async function(', 'function ggCardHTML(',
            'var omrTab=async function(', 'var GG={}']
    T2('Z-1 새 갈래가 전부 if(SHELL) **블록 안**이다(이 판부터 물리도 그 블록을 돈다)',
       blk >= 0 and end > blk and all(blk < s.find(k) < end for k in keys),
       [(k, s.find(k)) for k in keys if not (blk < s.find(k) < end)])
    T2('Z-2 새 갈래는 전부 ISEA 문 안이다(과목 문 무변)', "var ISEA=SUBJ_ID==='earth';" in s)
    T2('Z-3 uid 를 안 바꿨다', s.count('r[F.CODE]=') == 0)
    T2('Z-4 지학 SYNC_KEYS 줄 자체는 안 고쳤다(넷은 JS 가 더한다)',
       (s.count("'crop','txt','tfix','bref']") == base.count("'crop','txt','tfix','bref']")) if QC.GATE else QC.same('Z-4', s.count("'crop','txt','tfix','bref']")))   # regress — 기준 = 앞 인도판 셈(스냅샷)
    T2('Z-5 Tailwind 를 안 들였다', 'cdn.tailwindcss.com' not in s)
    T2('Z-6 makeFloat 을 **부르는** 자리가 둘 늘었다(🃏 창 · 📋 창)',
       s.count("makeFloat(b,b.querySelector('.bplh'),'mc'") == 1
       and s.count("makeFloat(b,b.querySelector('.bplh'),'jn'") == 1
       and s.count('function makeFloat(') == 1)
    T2('Z-7 bkLoadPiece 는 **더하기만** 했다(pc.__doc · pc.__k)',
       "const doc=pc.__doc?await pc.__doc():await pieceDoc(pc.file);" in s
       and "key:(pc.__k||'bink:')+pr" in s)
    T2('Z-8 cropOffer 의 🃏 는 pick 으로 간다(crop 과 갈래가 다르다)',
       "if(slot==='mc'){await pickAdd(uid,cell," in s and s.count('function cropOffer(') == 1)
    T2('Z-9 새 kv 는 셋뿐이다(gg · ggref · pick)',
       s.count("put('kv','gg',GG)") == 1 and s.count("put('kv','ggref',GGREF)") == 1
       and s.count("put('kv','pick',PICK)") == 1)
    # ★ _task_jagwa_earth_bookwin (2026-09-24) — 📋 정리 창 글씨(§F)·미리보기 고치기(§J) CSS 9 곳이 지학 문(body[data-subj="earth"])이었다.
    #   ★ add1(2026-09-25) — 생물도: 그 9 곳을 카드 층 문(body[data-layer="card"] · 물리는 "pdf")으로 옮겼다 → 지학 문은 다시 0.
    T2('Z-10 CSS 문이 data-shell / data-book 으로 갈렸다 · 지학 문 0(bookwin §F·§J 9 곳 = 카드 층 문 · add1)',
       'body[data-shell] #lib{max-width:56rem' in s
       and s.count('body[data-subj="earth"]') == 0
       and s.count('body[data-layer="card"] #jnw .jnrow') == 7 and s.count('body[data-layer="card"] .item .prev.') == 2
       and s.count('body[data-shell]') >= 45 and s.count('body[data-book]') >= 8,
       [s.count('body[data-subj="earth"]'), s.count('body[data-shell]'), s.count('body[data-book]'),
        s.count('body[data-layer="card"] #jnw .jnrow'), s.count('body[data-layer="card"] .item .prev.')])
    T2('Z-11 줄끝이 CRLF 그대로다', b.count(b'\r\n') == b.count(b'\n'))
    if QC.GATE:   # 관문만 — 본판(129eedb) 대비 길이(그 판 인도 때 「통째로 지우지 않았나」)
        T2('Z-12 본판 대비 늘기만 했다', len(s) > len(base))
    # ⚠ 판이 늘 때마다 **걷은 줄**이 는다(add9 「목차」 단추·옛 목차 서랍·navBuild 갈아끼움 ·
    #   add10 두 칩 · add12 갈래 떨어짐 · add15 아랫줄 규칙). 「통째로 지우지 않았나」를 보는
    #   잣대라 바닥은 남기되 자란 만큼 올린다.
    # ★ _task_jagwa_claude_slot (2026-09-22) — 242 → 261. 늘어난 19줄은 전수로 짚어 확인했다:
    #   「GPT」 글자 다섯 줄 + gptSheet 를 읽기 판·고치기 판으로 가르며 들여쓰기·한정자가
    #   달라진 열네 줄. 곁가지로 사라진 줄은 0이다.
    # ★ 같은 날 add1 — 261 → 262. 늘어난 **한 줄**은 전수로 짚었다:
    #   `<p>${esc(r[F.SUB])} · ${r[F.CODE]}</p>` — 카드 층에서 F.SUB 가 빈 문자열이라
    #   「 · uid」로 뜨던 창 머리를 과목 갈래로 가른 자리(§A-4). 그 밖에 사라진 줄은 0이다.
    #   ⇒ 문턱을 262 로 올린다(여유는 안 둔다).
    # ★ _task_jagwa_earth_bookwin (2026-09-24) — 262 → 283. 늘어난 21줄은 전수로 짚었다(갈아 쓴 줄뿐 · 곁가지 0):
    #   inkGuard 여섯(opt 갈래 · 지학만) · 목록 줄 .prev · 정리 창 줄 .q · bookListInto 셋(pop 갈래) · 교재 네모 엔진 한 줄(찍는 중 마우스)
    #   · cropFor·omrTabBuild 머리줄 자리 둘(#bkNav 뒤) · bplOpen 여덟(쪽 줄 data-bkgo · 꼬리표 · 아랫줄 · 손잡이 — 생물은 옛 값 그대로)
    # ★ _task_jagwa_earth_bookwin_add1 (2026-09-25) — 283 → 286. 늘어난 3줄은 전수로 짚었다: 본판의 `if(ISEA){` 세 줄이다.
    #   그 줄들은 오래전에 걷혔는데 bookwin 의 `if(ISEA){…`(bkQOpen · 새 덩어리 머리) 글자가 **부분 문자열로 가려** 셈에 안 잡혔다.
    #   add1 이 그 둘을 `if(HASBOOK){` 로 넓히자 드러났다(이 잣대는 줄 전체가 새 판 어디엔가 들어 있는지만 본다). 곁가지로 사라진 줄은 0이다.
    # ★ _task_jagwa_bio_ocrfix §J (2026-09-25) — 286 → 290. 늘어난 4줄은 전수로 짚었다(갈아 쓴 줄뿐 · 곁가지 0):
    #   열 번호 `Object.assign(F,{…SYNPG:29});`(REF:30 을 더함) · buildData 행 끝(`…it.SYNAPSE쪽||''];` 에 참고 칸) ·
    #   📋 정리 창 줄의 `'<div class="sol">'…'</div></div>'`(그 밑에 참고 칸) · 같은 창 「정답·해설 ▸」 펼침 줄(펼칠 때 참고 그림).
    #   참고 그림은 role="button" 으로 달아 PASS_THRU·UNDER_HIT 는 한 글자도 안 건드렸다(Z-24).
    # ★ _task_jagwa_penfinger (2026-09-25) — 290 → 294. 늘어난 4줄은 전수로 짚었다(갈아 쓴 줄뿐 · 곁가지 0):
    #   inkGuard 굴림 시작 줄 `if(!pan.armed){…pan.armed=true}`(눌리는 것 위 손가락이 굴림이 되면 그 단추 길게 누르기를 끈다) ·
    #   `function underInk(x,y,ink){` 머리와 `return el.closest(UNDER_HIT)||null;`(찾을 선택자 sel 을 받게 — 펜은 PEN_HIT) ·
    #   inkPierce 뚫기 조건 `if(!ink||e.target!==ink)return;`(→ !ink.contains — 이미 그은 획 위에서도). UNDER_HIT 은 한 글자도 안 바꿨다(Z-24).
    # ★ _task_jagwa_phone_win (2026-09-28) — 294 → 302. 이 판이 갈아 쓴 줄 12(앞 판 cc8f68b9 기준 · 곁가지 0) 가운데 셈에 새로 잡힌 8:
    #   폰 #view.win 전체화면 @media 한 줄(A-1 걷음) · 문제 창·곁창 첫 크기 넷(`if(!WIN.view&&!saved){const w=…` · `h=Math.min(860,…` ·
    #   `const w=Math.min(560,…` · `const hh=Math.min(…0.72…`) · #fFoldBtn 「필터 ▾」 HTML·paint 둘(A-2 「▾」 만) · OMR 폭 줄(A-3 비례) ·
    #   SHWIN 의 conceptStat 줄(A-4) · 개념 창 문제 누름의 `.sheet` 지우기·openView 둘(A-8) · wzCls 폰 제외(A-1 폰 문제 창도 떠 있는 창)
    # ★ uid_unify(10/4 · 앱 cand_u ec2f144 = uid_unify ①②④③ + ggmath + add1) — 356 → 453. 늘어난 97줄은 전수로 짚었다(`jgfix/_work2/z13_newly_missing.txt` · 앱 4754b1d 대 cand_u 로
    #   「본판(_base_bp)에 있던 줄 가운데 4754b1d 에는 있었는데 cand_u 에서 사라진 줄」을 전수 대조 — 97줄 모두 이 판들이 갈아 쓴 줄 · 곁가지로 사라진 줄 0 · 도로 살아난 줄 0):
    #   ① 66 = §A-1 기록 열쇠 번호 → uid(qk(no)) — QT·CMT·ST·TW·LK·GP·CX·AFIX·MC·MPOS·OPOS 읽고 쓰는 줄 · ink 열쇠 inkK · 값 속 번호(twin·link) · 모션 열쇠 motHas  · 마커 `qk(no){`
    #   ④ 24 = §G-1 「NN회 N번」 걷기(ynUid) · §G-2 서랍 회독마다 마크 · 목록 카드 회독 칩 · §G-3-2 다음 회독(lastMV · cmarkHTML · lastPick · showProblem · QR)  · 마커 `var ynUid=`
    #   ggmath 5 = 근거 글 그리는 자리 다섯 esc(…) → ggMath(…) · 마커 `ggMath(src){`   ·   add1 2 = 서랍 ndTail · 목록 카드 row 의 ewmTagHTML · 마커 `ewmTagHTML(r){`   ·   ②·③ = 0(창은 줄을 더하고 · 재료는 파일 이름)
    #   마커가 앱에 있는 만큼만 올린다 → 일부만 들어간 판 · 바탕 4754b1d 는 옛 문턱(356)이 그대로다.
    # 옛 줄: _Z13_UID = (('qk(no){', 66), ('var ynUid=', 24), ('ggMath(src){', 5), ('ewmTagHTML(r){', 2))
    #   + 10/5 cand_v fef1655 「+회독」 결함 고침 1 = 카드 층 `#tLayerAdd` 핸들러 한 줄(QR=Math.max(1,…) → QR=Math.max(QR,1,…)) · 마커 = 고친 식
    # 옛 줄: _Z13_UID = (('qk(no){', 66), ('var ynUid=', 24), ('ggMath(src){', 5), ('ewmTagHTML(r){', 2), ('QR=Math.max(QR,1,...qRounds())+1', 1))
    #   + ★ 2026-10-08 _task_jagwa_phys_win §A 47 — 이 판이 갈아 쓴 본판 줄 53(전수 대조: 서재→✕ A-15 · 암기카드→🃏 A-33 · 정답 창 A-26 · 지우개 창→erPop A-16 · twinPeek A-32 · 검색 A-45·46 …) · 마커 = pfDecor(A-39)
    #   잰 값: 7520d46 454(문턱 454) · fdd7b27 507
    if QC.GATE:   # 관문만 — 본판 줄 전수 대조(문턱을 판마다 손으로 올림 · 그 판 인도 때 뜻)
        # 옛 줄(10/8 03:15): _Z13_UID = (('qk(no){', 66), ('var ynUid=', 24), ('ggMath(src){', 5), ('ewmTagHTML(r){', 2), ('QR=Math.max(QR,1,...qRounds())+1', 1), ('function pfDecor(', 53))
        #   + ★ 2026-10-08 _task_jagwa_ink_sync — 사용법 글 「필기는 자동이 아닙니다」 한 줄을 「필기는 이제 자동입니다 …」 로(필기 동기화가 생겨 안내가 틀림) · 마커 = function syncInk( · 잰 값 507 → 508
        _Z13_UID = (('qk(no){', 66), ('var ynUid=', 24), ('ggMath(src){', 5), ('ewmTagHTML(r){', 2), ('QR=Math.max(QR,1,...qRounds())+1', 1), ('function pfDecor(', 53), ('function syncInk(', 1))
        T2('Z-13 지운 본판 줄이 거의 없다(손댄 자리뿐)',
           # ★ 합치기 10/1(하위 에이전트 C) — 320 → 356. 늘어난 36줄은 전수로 짚었다(세 판이 갈아 쓴 줄뿐 · 어느 판에도 없는 줄 0):
           #   physphone 22(공식 시트 frmRowHTML 로 옮긴 옛 rowHtml·body.onclick 줄 · #tTheory 「공식」 · 정리 창 「닫기」·이름 칸 · 개념 줄 글 thl)
           #   · revfix0928_0929 9(recAfterMerge 두 줄 · 서랍 줄 「-」 · makeFloat _pload · qFit avail · recMerge 옛 열쇠 줄 · #bpl z · #omrPad .drag) · search_claude 5(ggHits · 결과 줄)
           # 옛 줄: sum(1 for ln in base.split('\n') if ln.strip() and ln not in s) <= 356,   # ★ jagwa_search(9/29) 311 → 320 — 이 판이 떼거나 갈아 쓴 본판 줄 9(옛 pass 의 FL.q 덩이 · 입력칸 oninput · fltOn · 지우기 · 개수 칸 · 모드 바꾸기 · ggHits ID · ggResBox 끝) · 곁가지 0   # ★ jagwa_uid(9/29) 302 → 311 — 이 판이 갈아 쓴 줄 9(F 칸 OLDU · buildData 옛uid · 장 글자 셋 · codeShow · 차례 둘 · rowByUid · 번호 찾기 · 시동 jgMigrate) · 곁가지 0
           sum(1 for ln in base.split('\n') if ln.strip() and ln not in s) <= 356 + sum(n for _mk, n in _Z13_UID if _mk in s),   # ★ uid_unify — 356 + 마커가 있는 만큼(최대 97 = 453)
           sum(1 for ln in base.split('\n') if ln.strip() and ln not in s))
    # ── add2 가 둔 것(그대로) ──
    # ⚠ 부름 **수**가 아니라 **열쇠 이름**을 맞댄다 — 있는 키를 한 번 더 읽는 것은
    #   「새 키」가 아니다(add7 가 가드에서 `SYNC_REF.gg` 를 두 번 더 읽는다).
    _kv = lambda t: set(re.findall(r"put\('kv','([^']+)'", t))
    _sr = lambda t: set(re.findall(r"SYNC_REF\.([A-Za-z_$][\w$]*)", t))
    T2('Z-15 새 kv·새 SYNC 키가 없다',
       # ★ physprev(10/1 하위 에이전트 C) — _task_jagwa_physprev A-2-1 받은 미리보기 표의 기기 사본 kv 'pvjson'(SYNC 아님 · SYNC_REF 새 키 0 그대로)
       # 옛 줄: (_kv(s) == _kv(base) or (_kv(base) <= _kv(s) and _kv(s) - _kv(base) <= {'pvjson'})) and _sr(s) == _sr(base),
       # ★ uid_unify A-3(10/4 · gigu/_task_jagwa_uid_unify.md §A-3 「로컬: 기기마다 처음 옮길 때 한 번, IndexedDB kv 에 bak_uid = {at, 통별 옛 값 전부, u, gone}」) — 새 로컬 kv `bak_uid` 하나(SYNC 아님 · SYNC_REF 새 키 0 그대로).
       #   앱에 put('kv','bak_uid',…) 가 있을 때만 허용한다. ⚠ 이 잣대는 4754b1d 가 아니라 본판(_base_bp · 고침 전) 대비라 pvjson 은 옛 판에서도 늘 차집합에 든다(위 허용) — 새 FAIL 의 몫은 bak_uid 하나였다.
       # 옛 줄: (_kv(s) == _kv(base) or (_kv(base) <= _kv(s) and _kv(s) - _kv(base) <= ({'pvjson'} | ({'bak_uid'} if "put('kv','bak_uid'" in s else set())))) and _sr(s) == _sr(base),
       # ★ 2026-10-07 (_task_jagwa_phys_win §A-30 ㉖) 물리 오린 것 동기화 = kv 'solx' · SYNC_REF.solx(칸 = 문항 하나 · 늦게 읽는 통 가드 = gg 꼴) — 앱 글에 둘 다 있을 때만 그 키 하나씩 허용
       ((_kv(s) == _kv(base) or (_kv(base) <= _kv(s) and _kv(s) - _kv(base) <= ({'pvjson'} | ({'bak_uid'} if "put('kv','bak_uid'" in s else set())
                                                                         | ({'solx'} if ("put('kv','solx'" in s and 'SYNC_REF.solx=' in s) else set()))))
       and (_sr(s) == _sr(base) or (_sr(base) <= _sr(s) and _sr(s) - _sr(base) <= ({'solx'} if ("put('kv','solx'" in s and 'SYNC_REF.solx=' in s) else set())))) if QC.GATE else QC.same('Z-15', [sorted(_kv(s)), sorted(_sr(s))]),   # regress — 기준 = 앞 인도판 kv · SYNC_REF 집합(스냅샷)
       [sorted(_kv(s) - _kv(base)), sorted(_sr(s) - _sr(base))] if QC.GATE else _rg_setdiff('Z-15', [sorted(_kv(s)), sorted(_sr(s))]))
    T2('Z-17 아랫줄 감추기가 카드 층·물리로 갈렸다',
       'body[data-book] .vbot .tools>*{display:none!important}' in s
       and 'body[data-layer="pdf"] .vbot .tools:not(#pRow1)>*{display:none!important}' in s)
    # ★ add15 §A-4 — 줄을 꺾던 옛 규칙은 걷었다(한 줄 안에서 가로로 민다)
    T2('Z-17b add15 — `#pRow1` 이 한 줄이다(nowrap · 가로 밀기)',
       'body[data-layer="pdf"] #pRow1{flex-wrap:nowrap;overflow-x:auto' in s
       and '@container (max-width:560px){#pRow1 .sp' not in s)
    T2('Z-19 단축키 줄 무변(일부러 죽여 둔 것)',
       (s.count("if(e.key==='1')mark('O')") == base.count("if(e.key==='1')mark('O')") if QC.GATE else QC.same('Z-19', s.count("if(e.key==='1')mark('O')")))
       and "if(document.querySelector('.sheet'))return;" in s)
    # ── add3 ──
    T2('Z-20 ① setTool 덧씌움이 펜·형광·지우개에서 QTXT 를 끈다',
       "if(mode==='pen'||mode==='hl'||mode==='erase')QTXT=false;" in s
       and s.count('setTool=function(mode)') == 1)
    T2('Z-21 ① 글상자를 켜면 필기 도구를 놓는다(#tTxt 쪽)',
       "if(QTXT){TOOL.mode='view';" in s
       and s.count("b.onclick=()=>{QTXT=!QTXT;") == 1)
    T2('Z-22 ① 본디 setTool 은 한 글자도 안 건드렸다',
       "  TOOL.mode=mode;if(color)TOOL.color=color;TOOL.w=+$('#tW').value;" in s
       and (s.count('function setTool(mode,color,el){') == base.count('function setTool(mode,color,el){') if QC.GATE else QC.same('Z-22', s.count('function setTool(mode,color,el){'))))
    T2('Z-23 ② 근거 덩어리는 **한 겹**이다(.ggtop) · 물리엔 안 생긴다(ggCardHTML 은 ISEA)',
       s.count("'<div class=\"ggtop\">'") == 1
       and '#card .ggtop{position:relative;z-index:8' in s
       and "function ggCardHTML(r){\n  if(!SHELL)return '';" in s)
    T2('Z-24 ② UNDER_HIT·underInk·inkPierce 는 한 글자도 안 건드렸다(지시서 ⓑ)',
       s.count('const UNDER_HIT=') == 1
       and ".row[data-k],[data-c],[data-tfx],[data-go],[data-page],[data-no],.snt,.trit';" in s
       and (s.count("if(el.closest('select,input,textarea'))return null;")
            == base.count("if(el.closest('select,input,textarea'))return null;") if QC.GATE else QC.same('Z-24.closest', s.count("if(el.closest('select,input,textarea'))return null;")))
       and (s.count('function inkPierce(card){') == base.count('function inkPierce(card){') if QC.GATE else QC.same('Z-24.inkPierce', s.count('function inkPierce(card){'))))
    T2('Z-25 ② PASS_THRU 에 근거 선택자를 **더하기만** 했다',
       ".ggnum,.ggbang,.ggref,.ggres,.gguse,[data-ggown],[data-ggpick],[data-ggrt],[data-ggtog]" in s
       and s.count('const PASS_THRU=') == 1
       and "'[data-tool],#omrPad,#navTg,select,input,textarea,.ogrip,#mask,.tbox,#qtxt," in s)
    T2('Z-26 ③ 쓰임 수는 **한 함수**다 — 정의 1 · 부르는 자리 3',
       s.count('function ggUseHTML(') == 1 and s.count('ggUseHTML(') == 4,
       s.count('ggUseHTML('))
    T2('Z-27 ③ 문턱 5 가 박혀 있다(분포로 조정하지 않는다)',
       "const n=ggUseN(uid); if(n<=1)return '';" in s and "(n>=5?' hot':'')" in s)
    T2('Z-28 ③ 찾기 결과 줄은 **한 꼴**이다 — 카드 안·위 검색 줄이 같은 함수',
       s.count('function ggResRowHTML(') == 1
       and "function ggResLine(h,q){return ggResRowHTML(h,q,'go','','')}" in s
       and "ggResRowHTML(h,q,'pick',uid,sc)" in s)
    T2('Z-29 ③ 찾기 칸 120ms 모으기 · 포커스는 즉시',
       'function ggFindSoon(' in s and 'ggFindSoon(v[0],v[1])' in s
       and "if(i&&!b.classList.contains('hide')){i.focus();ggFindRun(v[0],v[1])}" in s)
    T2('Z-30 ③ 저장 꼴은 무변(gg·ggref)',
       (s.count("put('kv','gg',GG)") == base.count("put('kv','gg',GG)") if QC.GATE else QC.same('Z-30.gg', s.count("put('kv','gg',GG)")))
       and (s.count("put('kv','ggref',GGREF)") == base.count("put('kv','ggref',GGREF)") if QC.GATE else QC.same('Z-30.ggref', s.count("put('kv','ggref',GGREF)"))))
    # ── 생물·물리 이식 ──
    T2('Z-31 문이 넷이다 — SHELL · HASBOOK · HASROUND · HASJOGAK',
       'var SHELL=true, HASBOOK=CARD_LAYER, HASJOGAK=!!CUR.JOGAK_PATH;' in s
       and 'function HASROUND(){' in s)
    # ★ _task_jagwa_earth_bookwin (2026-09-24) — bookwin 이 넣은 문 15 줄(inkGuard 부름 1 · row 2 · qFit 2 · bkQOpen 1 · bplOpen 7 · jnRowHTML 1 · 새 덩어리 머리 1)이 ISEA 였다.
    #   ★ add1(2026-09-25) — 생물도: 그 15 줄을 HASBOOK(카드 층)으로 넓혔다 → ISEA 코드 줄은 다시 0(정의만 · 지학 데이터 고유 자리용).
    T2('Z-32 ISEA 는 정의뿐 · bookwin 문 15 줄 = HASBOOK(add1)',
       s.count('var ISEA=') == 1
       and len([1 for ln in s.split('\n')
                if 'ISEA' in ln and 'var ISEA=' not in ln and '`ISEA`' not in ln
                and not ln.lstrip().startswith(('/*', '*'))]) == 0
       and ("\nif(HASBOOK){\n  /* ── §B 떠 있는 창 무리" in s
            or "\nif(SHELL){   /* ★ physphone A-1(2026-09-30) — §B 창 무리를 교재 덩어리 밖(세 과목 공통)으로" in s)   # ★ 합치기 10/1 — physphone A-1(97883ef)
       and "(typeof HASBOOK!=='undefined'&&HASBOOK&&window.INKG_EA)" in s
       and "data-${HASBOOK?'bkgo':'go'}" in s and "if(HASBOOK){bookListInto(p.pr,$('#bkqList'),null,true);return}" in s
       and "if(HASBOOK&&typeof QZ==='number'&&QZ!==1){" in s and "if(HASBOOK)d.dataset.uid=r[F.CODE];" in s,
       [ln.strip()[:70] for ln in s.split('\n') if 'ISEA' in ln][:8])
    T2('Z-33 학습로그 단추 DOM 은 없고 openPanel 은 남았다',
       "btn.textContent = '📝 학습로그'" not in s
       and s.count('document.body.appendChild(btn)') == 0
       and s.count('function openPanel()') == 1
       and (s.count('function dayRange(') == base.count('function dayRange(') if QC.GATE else QC.same('Z-33', s.count('function dayRange('))),
       [s.count('document.body.appendChild(btn)'), s.count('function openPanel()')])
    T2('Z-34 물리 열쇠는 번호로 만든다(F.CODE 에 겹침이 있다)',
       "var GGU = HASBOOK ? (r=>(r?String(r[F.CODE]||''):'')) : (r=>(r?('P'+String(r[F.NO]).padStart(3,'0')):''));" in s)
    T2('Z-35 물리 목차를 DATA 에서 짓는다 · refreshUnits 는 안 부른다',
       'function buildTocFromData(){' in s and 'if(!HASBOOK)buildTocFromData();' in s
       and (s.count('refreshUnits()') in (base.count('refreshUnits()'), base.count('refreshUnits()') + 1) if QC.GATE else QC.same('Z-35', s.count('refreshUnits()'))))   # ★ jagwa_uid(9/29) — jgMigrate(카드층만 · 물리 안 탐)가 옮긴 뒤 한 번 부른다
    T2('Z-36 필기 엔진·좌표·덮개 규칙은 한 글자도 안 건드렸다',
       (s.count('function qWire(){') == base.count('function qWire(){') if QC.GATE else QC.same('Z-36.qWire', s.count('function qWire(){')))
       and s.count('const UNDER_HIT=') == 1
       and (s.count('function inkPierce(card){') == base.count('function inkPierce(card){') if QC.GATE else QC.same('Z-36.inkPierce', s.count('function inkPierce(card){')))
       and (s.count("if(el.closest('select,input,textarea'))return null;")
            == base.count("if(el.closest('select,input,textarea'))return null;") if QC.GATE else QC.same('Z-36.closest', s.count("if(el.closest('select,input,textarea'))return null;"))))
    T2('Z-37 과목 강조색은 한 변수다 — 지학 값은 그대로',
       ':root{--subj:var(--sea);--subj-soft:var(--sea-soft)}' in s
       and s.count('var(--sea)') == 1 and s.count('var(--subj)') >= 50,
       [s.count('var(--sea)'), s.count('var(--subj)')])
    T2('Z-38 물리 근거 목록은 .stage 에 붙고 단추 줄은 .vbot 윗줄이다',
       'function ggPhysPaint(){' in s and "box.id='ggphys'" in s
       and "r1.id='pRow1'" in s and 'function physRowBuild(){' in s)
    T2('Z-39 글상자는 카드 층만 만든다(물리 알약은 여덟)',
       "if(HASBOOK){const tb=document.querySelector('.vbot .tools');" in s)
    return out


XBASE_MD5 = '24f1a3730becea3d9619c431d1ed93d3'   # 교재 창(bookwin) 고침 전 판(LF) — genie bd8cfdf


def _xbase_text():
    """X 묶음 헛잣대용 고침 전 판 — git 에서 꺼내 TEMP 에만 둔다(공개·N: 저장소에 두지 않는다 · D11)."""
    fp = os.path.join(OUT, '_base_bw.html')
    if os.path.exists(fp):
        b = open(fp, 'rb').read()
        if hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest() == XBASE_MD5:
            return b.decode('utf-8')
    for rev in ('HEAD', 'HEAD~1', 'HEAD~2', 'HEAD~3', 'HEAD~4', 'HEAD~5', 'bd8cfdf'):
        try:
            b = subprocess.run(['git', '-C', GENIE, 'show', rev + ':jagwa/index.html'], capture_output=True).stdout
        except Exception:
            continue
        if b and hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest() == XBASE_MD5:
            open(fp, 'wb').write(b)
            print('[xbase] git %s 에서 꺼냈다' % rev)
            return b.decode('utf-8')
    raise SystemExit('NG  교재 창 고침 전 사본(md5 %s)을 못 찾았다' % XBASE_MD5)


XBBASE_MD5 = 'f07e9d08d8da937c9a436201c556a86d'   # add1(생물) 고침 전 판(LF) — genie 6c54347(bookwin 인도판)


def _xbbase_text():
    """XB 묶음 헛잣대용 add1 고침 전 판 — git 에서 꺼내 TEMP 에만 둔다(공개·N: 저장소에 두지 않는다 · D11)."""
    fp = os.path.join(OUT, '_base_bw1.html')
    if os.path.exists(fp):
        b = open(fp, 'rb').read()
        if hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest() == XBBASE_MD5:
            return b.decode('utf-8')
    for rev in ('HEAD', 'HEAD~1', 'HEAD~2', 'HEAD~3', 'HEAD~4', 'HEAD~5', '6c54347'):
        try:
            b = subprocess.run(['git', '-C', GENIE, 'show', rev + ':jagwa/index.html'], capture_output=True).stdout
        except Exception:
            continue
        if b and hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest() == XBBASE_MD5:
            open(fp, 'wb').write(b)
            print('[xbbase] git %s 에서 꺼냈다' % rev)
            return b.decode('utf-8')
    raise SystemExit('NG  add1 고침 전 사본(md5 %s)을 못 찾았다' % XBBASE_MD5)


def g1_e1_norm(k, a1, b1):
    """★ uid_unify(10/4 · gigu/_task_jagwa_uid_unify.md §G-1 §G-2 §G-3-2) — E-1 「지학 … 이(가) 고침 전과 글자까지 같다」 에서 이 판이 뜻하고 바꾼 글자만 **바탕(고침 전 판 = 옛 앱) 쪽 글자 b1** 에서 뗀다.
    새 판(앱 글에 ynUid)일 때만 부른다 · 지학 기출 uid(G..) 줄만(이 묶음은 지학뿐 · 생물 G-1 은 사용자 결정 대기) · 뗄 글자는 바탕 쪽 b1 에만 있는 것이라 새 판 쪽 a1 에 그 글자가 남아 있으면 여전히 FAIL(예외 vbot: 옵션 개수 자체가 뜻한 차이라 두 쪽을 한 옵션으로 접는다).
    — 목록(list): ① 기출 uid 줄 `.meta .sub` 「NN회 N번」 안 그림(§G-1) ② 카드 층 「N회독」 칩 걷음(§G-2)
    — 문항 머리줄(vtop): `#vT1` = 「G25-62-09 (2025)」 — 「 · NN회 N번」 안 그림(§G-1)
    — 카드 글(card): `.cmeta` 둘째 칩 titleOf 안 그림(§G-1) · 오른쪽 위 `.cmark` = 이번 열람 마크만(없으면 빈칸 — 「O 맞음」 · 「마크 없음」 대신)(§G-3-2)
    — 아랫줄(vbot): 회독 고르개 — 지난 회독이 있으면 다음 회독이 옵션으로 하나 더 선다(필기 QR = max(잉크 최대 회독, 지난 회독 수 + 1) · §G-3-2)"""
    if k == 'list':
        b1 = re.sub(r'(\bG\d\d-\d+-\d+ 기출) \d+회 \d+번(?= )', r'\1', b1)
        b1 = b1.replace(' #회독', '')
    elif k == 'vtop':
        b1 = re.sub(r'(\bG\d\d-\d+-\d+) · \d+회 \d+번', r'\1', b1)
    elif k == 'card':
        b1 = re.sub(r'(기출)\d+회 \d+번 ', r'\1 ', b1)
        b1 = re.sub(r' (?:[OX△P] (?:맞음|헷갈림|틀림|패스)|마크 없음)(?= )', '', b1)
    elif k == 'vbot':
        a1 = re.sub(r'(#회독){2,}', '#회독', a1)
        b1 = re.sub(r'(#회독){2,}', '#회독', b1)
    return a1, b1


# ── _task_qa_slim2(10/8) regress 도우미 — 이름이 `_rg` · `_RG` 로 시작하는 것 = gate 에서 안 쓰는 갈래(gate 에서 도는 줄은 원래 글 그대로 · `if QC.GATE:` 안) ──
_RG_PICK = """
   const __qcN={};const __qcPick=(a,seed,n,size)=>{a=[...a];n=n||10;if(a.length<=n){__qcN[seed]=[a.length,a.length];return a}
     const pick=new Set([0,a.length-1]);
     if(size){let bi=0,bv=-1;a.forEach((x,i)=>{const v=size(x);if(v>bv){bv=v;bi=i}});pick.add(bi)}
     const h=s=>{let x=2166136261;for(const c of String(s)){x^=c.charCodeAt(0);x=Math.imul(x,16777619)>>>0}return x};
     a.map((x,i)=>[h(seed+'|'+x),i]).sort((p,q)=>p[0]-q[0]||p[1]-q[1]).forEach(p=>{if(pick.size<n)pick.add(p[1])});
     const out=a.filter((x,i)=>pick.has(i));__qcN[seed]=[out.length,a.length];return out};
"""   # regress 표본(A-3) — 첫 · 끝 · 가장 큰 것 + 씨앗 고정(FNV-1a) · 고른 것은 원래 차례 · 셈은 끝 NOTE 줄(「regress 표본」)
_RG_SUBS = {   # 몸통 · (옛 글, 새 글, 칸) — 옛 글은 그 몸통에 꼭 한 번(못 찾으면 그대로 = 전수 · NOTE 한 줄)
    'phys': (("     for(const sec of secs){\n       jnOpen(sec); await wait(120);",
              "     for(const sec of __qcPick(secs,'P-8',10,s=>DATA.filter(r=>showKind(r)&&unitOf(r[F.NO])===s).length)){   /* regress 표본 — gate 는 절 63 전수 */\n       jnOpen(sec); await wait(120);", 'P-8'),
             ("       for(const sec of secs){\n         jnOpen(sec); await wait(150);\n         const w=document.getElementById('jnw'); if(!w){bad.push([sec,'창 없음']);continue}",
              "       for(const sec of __qcPick(secs,'P-9',10,s=>withGG.filter(r=>unitOf(r[F.NO])===s).length)){   /* regress 표본 — gate 는 근거 든 절 전수 */\n         jnOpen(sec); await wait(150);\n         const w=document.getElementById('jnw'); if(!w){bad.push([sec,'창 없음']);continue}", 'P-9'),
             ("         const secs=Object.keys(TOC.sec).slice(0,20);\n         for(const sec of secs){\n           const want=DATA.filter(r=>showKind(r)&&phPast(r)&&unitOf(r[F.NO])===sec).length;",
              "         const secs=__qcPick(Object.keys(TOC.sec).slice(0,20),'P-13.'+v,6);   /* regress 표본 — gate 는 분류마다 절 스물 */\n         for(const sec of secs){\n           const want=DATA.filter(r=>showKind(r)&&phPast(r)&&unitOf(r[F.NO])===sec).length;", 'P-13')),
    'earth': (("     T('SQ 지학 ★헛잣대 — 옛 차례(filtered() 그대로 · add19 앞의 서랍)는 첫 화면과 **다르다**',\n       old.length===first.length&&old.join('|')!==first.join('|'),\n       {n:[old.length,first.length],옛앞:old.slice(0,4),새앞:first.slice(0,4)});",
               "     /* regress — SQ 헛잣대(옛 차례 흉내 · 관문만) 끔 */", 'SQ-헛'),),
}


def _rg_body(mode, body):
    """regress · smoke — 쪽 안 JS 몸통을 이 자리에서만 고친다(BODY_* 상수는 gate 와 같은 글자 그대로).
    smoke: 밑준비 + 첫 묶음(껍데기 A-0 · B-1 · P-1)까지만 · regress: 표본(P-8 · P-9 · P-13) · 헛잣대(SQ) 끔 — 자리를 못 찾으면 그대로(= gate 와 같은 전수) · NOTE 한 줄"""
    if QC.SMOKE:
        i1 = body.find('\n   await grp(')
        i2 = body.find('\n   await grp(', i1 + 1) if i1 >= 0 else -1
        return (body[:i2] + '\n') if i2 > 0 else body
    subs = _RG_SUBS.get(mode)
    if not subs:
        return body
    for old, new, tag in subs:
        n = body.count(old)
        if n == 1:
            body = body.replace(old, new)
        else:
            print('NOTE | regress %s 자리 %d 번 — 그대로(전수) | %s' % (tag, n, mode))
    return _RG_PICK + body + "\n   N('regress 표본',__qcN);\n"


def _rg_e1_mask(k, a1):
    """E-1 regress 가림 — gate 가 두 쪽(새 판 · 바탕) 다 가리던 것만(▶ 차례 · 번호 꼴 · 📖 p 표시 · Claude 자리 · 타이머 · 기록 동기화 수 · 회독 옵션 겹침).
    바탕 쪽만 떼던 것(목차 · 필터 ▾ · GPT · 서재 · 암기카드 · gfit · 👁 이론)은 안 뗀다 — 두 쪽 다 새 판 글자(앞 인도판 · 이 판)다."""
    if k == 'card':
        a1 = re.sub(r'이전\d+ / ', '이전· / ', a1)
    a1 = re.sub(r'\b(G\d\d-\d\d-)0(\d)\b', r'\1\2', a1)
    if k == 'card':
        a1 = re.sub(r'(📖 p\d+)[✓✎]', r'\1·', a1)
    if k == 'vbot' and ' Claude' in a1:
        a1 = a1.replace(' Claude', '') + ' Claude'
    a1 = re.sub(r"\d+'\d{2}\"", "·'··\"", a1)
    for _rx, _to in ((r'\d+회독', '#회독'), (r'근거 \(\d+\)', '근거 (#)'), (r'근거 \d+', '근거 #'),
                     (r'(안 품|맞음|헷갈림|틀림|덜약점|약점) ?\d+', r'\1 #'),
                     (r'\d+(?=[OX△P](?:\d+[OX△P])*(?:·\'··"|$| \|\| ))', '#')):
        a1 = re.sub(_rx, _to, a1)
    if k == 'vbot':
        a1 = re.sub(r'(#회독){2,}', '#회독', a1)
    return a1


def _rg_e1(sn, T2):
    """regress — earthbase(본판 129eedb 고정 사본)를 안 돌리고 E-1 아홉 칸 = 새 판 값(가린 글자)을 기준 스냅샷(앞 인도판 earth 스냅의 같은 칸)과 맞댄다 · 칸 글은 gate 와 같다"""
    T2('E-1 고침 전 사본도 끝까지 돌았다', bool(sn), [bool(sn), QC.base_note('E-1.list')])
    if not sn:
        return
    for k, ko in (('list', '목록 25줄'), ('cnt', '문항 수'), ('hd', '묶음 머리'),
                  ('spec', '히트맵 칸'), ('esh', '껍데기 글'), ('view', '#view 클래스'),
                  ('vtop', '문항 머리줄'), ('vbot', '아랫줄'), ('card', '카드 글 600자')):
        cid = 'E-1.' + k
        a1 = _rg_e1_mask(k, str(sn.get(k)))
        b1 = str(QC.base(cid, a1))
        same = a1 == b1
        if same or k not in ('list', 'hd', 'card', 'esh', 'vbot', 'vtop'):
            info = [a1[:170], b1[:170], QC.base_note(cid)]
        else:
            sep = ' || ' if ' || ' in a1 or ' || ' in b1 else ''
            if sep:
                A = a1.split(sep); B = b1.split(sep)
            else:
                m = next((i for i in range(min(len(a1), len(b1))) if a1[i] != b1[i]), min(len(a1), len(b1)))
                A = [a1[max(0, m - 30):m + 60]]; B = [b1[max(0, m - 30):m + 60]]

            def _cut(x, y):
                m = next((j for j in range(min(len(x), len(y))) if x[j] != y[j]), min(len(x), len(y)))
                return x[max(0, m - 25):m + 55], y[max(0, m - 25):m + 55], m
            d = [(i,) + _cut(A[i], B[i]) for i in range(min(len(A), len(B))) if A[i] != B[i]]
            info = {'줄수': [len(A), len(B)], '다른 줄 수': len(d), '처음 둘': d[:2], '기준': QC.base_note(cid)}
        T2('E-1 ★지학 %s 이(가) 고침 전과 **글자까지** 같다' % ko, same, info)


def _rg_xside(m, sa):
    """regress — x<m>base(바탕 판 24f1a373)를 안 돌리고 X-11 의 바탕 쪽 값 = 기준 스냅샷(앞 인도판 x<m> 스냅) · 사라진 칸도 잡게 칸 이름 목록도 스냅샷"""
    sa = sa or {}
    ks = sorted(k for k in sa if k != 'names')
    kb = QC.base('X-11.%s.keys' % m, ks) or []
    return {k: QC.base('X-11.%s.%s' % (m, k), sa.get(k)) for k in sorted(set(ks) | set(kb))}


def _rg_setdiff(cid, v):
    """regress — 기준 스냅샷 대비 더해진 · 빠진 낱말(값 v = [목록, 목록 …])"""
    b = QC.base(cid, v) or [[] for _ in v]
    return {'더함': [sorted(set(x) - set(y)) for x, y in zip(v, b)], '빠짐': [sorted(set(y) - set(x)) for x, y in zip(v, b)], '기준': QC.base_note(cid)}


def main():
    want = [a for a in sys.argv[1:] if a in ('earth', 'bio', 'phys', 'null', 'x', 'xb')] \
           or ['earth', 'bio', 'phys', 'null', 'x', 'xb']
    cur = open(SRC, encoding='utf-8', newline='').read()
    basetxt = open(BASE, encoding='utf-8', newline='').read() if QC.GATE else ''   # regress — 본판 사본 안 읽음(바탕 묶음 안 돎)
    if QC.SMOKE:   # smoke — 세 과목 첫 묶음(껍데기 A-0 · B-1 · P-1)과 콘솔 오류 0 만(build 가 쪽 안 몸통을 첫 묶음까지 자른다) · 교재 창(x · xb) · 헛잣대(null) · 소스 글 셈은 건넘
        want = [m for m in want if m in ('earth', 'bio', 'phys')]
    _G1E = bool(re.search(r'\bynUid\s*=', cur)) and not re.search(r'\bynUid\s*=', basetxt)   # ★ uid_unify — 새 판(앱 글에 ynUid)일 때만 E-1 에서 뜻한 차이를 뗀다(바탕 4754b1d 는 옛 잣대 그대로)
    lines = []
    W = int(os.environ.get('HARNESS_WAIT', '1500'))

    def T2(name, cond, info=''):
        lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))

    if 'earth' in want:
        ls, sn = run('earth', W, cur)
        lines += ls
        if QC.GATE:
            ls0, sn0 = run('earthbase', W, basetxt)
            T2('E-1 고침 전 사본도 끝까지 돌았다', bool(sn and sn0), [bool(sn), bool(sn0)])
            if sn and sn0:
                for k, ko in (('list', '목록 25줄'), ('cnt', '문항 수'), ('hd', '묶음 머리'),
                              ('spec', '히트맵 칸'), ('esh', '껍데기 글'), ('view', '#view 클래스'),
                              ('vtop', '문항 머리줄'), ('vbot', '아랫줄'), ('card', '카드 글 600자')):
                    a1, b1 = str(sn.get(k)), str(sn0.get(k))
                    if k in ('esh', 'vtop'):
                        # ★ add9 §A-1 — 「목차」 단추를 걷은 것은 **이 판이 뜻한 것**이다.
                        b1 = b1.replace('목차', '', 1)
                    if k == 'esh':
                        # ★ A-6(a) 9/30 _task_qa_baseline — phone_win §A-2(genie fb89ad2 · 결정로그 9/28 17:20 · _task_jagwa_phone_win.md 수행 결과 「shell E-1 지학 껍데기 글 = §A-2 필터 글자 걷음」):
                        #   접기 단추 「필터 ▾」 → 「▾」 — 그 글자만 맞춘다
                        b1 = b1.replace('필터 ▾', '▾', 1)
                    if k == 'card':
                        # ★ add19 §A-1 — ▶ 차례가 바뀐 것은 **이 판이 뜻한 것**이다(첫 화면 차례를 따른다).
                        #   그 자리만 가리고 나머지 글자는 그대로 맞댄다. 바뀌었다는 것은 아래에서 따로 잰다.
                        rx = re.compile(r'이전\d+ / ')
                        a1 = rx.sub('이전· / ', a1); b1 = rx.sub('이전· / ', b1)
                    # ★ _task_jagwa_claude_slot §A-1 (2026-09-22) — 「GPT」→「Claude」 는
                    #   **이 판이 뜻한 것**이다(세 과목 공통 창 · 데이터 이름은 무변).
                    #   그 낱말만 가리고 나머지 글자는 그대로 맞댄다 — 다른 데가 달라지면 여전히 FAIL 이다.
                    #   바뀌었다는 것 자체는 묶음 CL(_harness_jagwa_claude_slot.py)이 따로 잰다.
                    b1 = b1.replace('GPT', 'Claude')
                    if k == 'vtop' and a1.startswith('✕') and b1.startswith('서재'):
                        # ★ 2026-10-07 (_task_jagwa_phys_win §A-15 ⑧) — 문항 창 닫기 「서재」 → ✕(세 과목) = 뜻한 차 — 맨 앞 그 글자만 맞춘다(나머지는 그대로 맞댐 · 옛 판은 a1 이 「서재」라 안 탐)
                        b1 = '✕' + b1[len('서재'):]
                    if k == 'vbot' and '암기카드' not in a1 and '🃏' in a1:
                        # ★ 2026-10-07 (_task_jagwa_phys_win §A-33) — #tCard 「암기카드」 → 🃏(세 과목) = 뜻한 차 — 그 낱말만 맞춘다(옛 판은 a1 에 「암기카드」가 있어 안 탐)
                        b1 = b1.replace('암기카드', '🃏', 1)
                    if k == 'vbot':
                        # ★ 합치기 10/1(하위 에이전트 C) — physphone A-3(97883ef 본문 「#tTheory 「공식」 → 「이론」」 · 세 과목 같은 단추) — 그 낱말만 옛 글자로 맞춘다(바탕 판을 돌려도 같게)
                        a1 = a1.replace('👁 이론 개념', '👁 공식 개념', 1)
                    # ★ A-6(a) 9/30 _task_qa_baseline — jagwa_uid(genie 5e18424 + studyplandata 4a011475 · 결정로그 9/29 15:09 · _task_jagwa_uid.md 수행 결과 「남은 차이 … 지학 껍데기 E-1 ×3」):
                    #   ① 보이는 번호가 새 꼴(끝 두 자리 · G25-62-9 → G25-62-09) — 번호 꼴만 옛 꼴(바탕 앱 codeShow)로 맞춘다
                    #   ② 옛 앱은 새 번호 데이터에서 옛 열쇠 기록을 못 봐 카드 「📖 pN✓」(옮긴 교재 쪽 찍음)이 「✎」 로 선다 — 그 표시 한 글자만 가린다 · 나머지 글자는 그대로 맞댄다
                    _rxU = re.compile(r'\b(G\d\d-\d\d-)0(\d)\b')
                    a1 = _rxU.sub(r'\1\2', a1); b1 = _rxU.sub(r'\1\2', b1)
                    if k == 'card':
                        _rxP = re.compile(r'(📖 p\d+)[✓✎]')
                        a1 = _rxP.sub(r'\1·', a1); b1 = _rxP.sub(r'\1·', b1)
                    # ★ add1 §A-2 (2026-09-22) — 카드 층에서 「Claude」가 **맨 오른쪽으로 옮겨졌다.**
                    #   아랫줄 글은 숨은 것까지 DOM 차례대로 이어 붙이므로 낱말 자리가 바뀐다.
                    #   자리만 맞춰 놓고 나머지 글자는 그대로 맞댄다(낱말이 사라지면 여전히 FAIL).
                    if k == 'vbot':
                        for _s in ('a1', 'b1'):
                            _v = a1 if _s == 'a1' else b1
                            if ' Claude' in _v:
                                _v = _v.replace(' Claude', '') + ' Claude'
                            if _s == 'a1':
                                a1 = _v
                            else:
                                b1 = _v
                    # ★ add1 (2026-09-22) — 목록 줄에 **공부 시간 타이머**(`0'05"`)가 실린다.
                    #   같은 파일끼리도 판마다 1초씩 갈린다(CLAUDE.md 「픽셀·타이머는 게이트가 못 된다」).
                    #   숫자만 가리고 나머지 글자는 그대로 맞댄다.
                    _rxT = re.compile(r"\d+'\d{2}\"")
                    a1 = _rxT.sub("·'··\"", a1); b1 = _rxT.sub("·'··\"", b1)
                    # ★ 9/28 penfinger_add2 회귀 — 기록에서 나오는 숫자는 판마다가 아니라 기록 동기화 시각마다 갈린다
                    #   (한 판만 동기화가 끝나 「6회독↔5회독」 「🔗 근거 (1)↔(18)」 「안 품 286·맞음 27 ↔ 318·1」 — 같은 판을 다시 돌리면 PASS).
                    #   숫자만 가리고 낱말·틀은 그대로 맞댄다(낱말이 사라지거나 줄이 바뀌면 여전히 FAIL).
                    for _rx, _to in ((re.compile(r'\d+회독'), '#회독'), (re.compile(r'근거 \(\d+\)'), '근거 (#)'), (re.compile(r'근거 \d+'), '근거 #'),
                                     (re.compile(r'(안 품|맞음|헷갈림|틀림|덜약점|약점) ?\d+'), r'\1 #'),
                                     # ★ A-6(d) 9/30 둘째 바퀴 — 목록 줄 끝 회독 딱지(markBadge · 마지막 넷에 차례 수 「3X4X5P6O」)의 차례 수도 기록 동기화 시각마다 갈린다
                                     #   (위 「6회독↔5회독」과 같은 것 — G25-62-09 새 3~6 / 바탕 2~5 · 마크 넷 X X P O 는 같다) · 차례 수만 가리고 마크 글자는 그대로 맞댄다
                                     (re.compile(r'\d+(?=[OX△P](?:\d+[OX△P])*(?:·\'··"|$| \|\| ))'), '#')):
                        a1 = _rx.sub(_to, a1); b1 = _rx.sub(_to, b1)
                    # ★ uid_unify(10/4 · §G-1 §G-2 §G-3-2 · 위 g1_e1_norm) — 새 판일 때만 · 바탕 쪽 글자에서 뜻한 차이만 뗀다
                    if _G1E:
                        a1, b1 = g1_e1_norm(k, a1, b1)
                    if k == 'view' and 'gfit' in a1.split() and 'gfit' not in b1.split():
                        # ★ 2026-10-07 (_task_jagwa_phys_win §A-28 ⑮) 글이 창에 다 들면 판에 gfit 클래스(크기 손잡이 자리 · 세 과목) = 뜻한 차 — 그 클래스 한 낱말만 뗀다(나머지 클래스는 그대로 맞댐)
                        a1 = ' '.join(x for x in a1.split() if x != 'gfit')
                    same = a1 == b1
                    if same or k not in ('list', 'hd', 'card', 'esh', 'vbot', 'vtop'):
                        info = [a1[:170], b1[:170]]
                    else:
                        # 줄 묶음은 **어느 줄이 다른지** 찍는다(앞 170자만 보면 못 가른다)
                        sep = ' || ' if ' || ' in str(sn.get(k)) else ''
                        if sep:
                            A = a1.split(sep); B = b1.split(sep)
                        else:   # 한 덩어리 글 — 처음 갈리는 자리를 찍는다
                            a0, b0 = a1, b1
                            m = next((i for i in range(min(len(a0), len(b0))) if a0[i] != b0[i]), min(len(a0), len(b0)))
                            A = [a0[max(0, m - 30):m + 60]]; B = [b0[max(0, m - 30):m + 60]]
                        def _cut(x, y):
                            m = next((j for j in range(min(len(x), len(y))) if x[j] != y[j]), min(len(x), len(y)))
                            return x[max(0, m - 25):m + 55], y[max(0, m - 25):m + 55], m
                        d = [(i,) + _cut(A[i], B[i]) for i in range(min(len(A), len(B))) if A[i] != B[i]]
                        info = {'줄수': [len(A), len(B)], '다른 줄 수': len(d), '처음 둘': d[:2]}
                    T2('E-1 ★지학 %s 이(가) 고침 전과 **글자까지** 같다' % ko, same, info)
                # ★ add19 §A-1 헛잣대 — 같은 문항(G62-09)의 ▶ 차례가 **바뀌었다**(첫 화면 차례를 따른다)
                import re as _re
                _ix = lambda t: (_re.search(r'이전(\d+) / (\d+)', str(t or '')) or [None, None, None])
                _n, _o = _ix(sn.get('card')), _ix(sn0.get('card'))
                T2('E-1 ★add19 — 같은 문항의 ▶ 차례가 옛 판과 **다르다**(새 %s / 옛 %s · 둘 다 총 319)'
                   % (_n[1] if _n[1] else '?', _o[1] if _o[1] else '?'),
                   bool(_n[1]) and bool(_o[1]) and _n[1] != _o[1] and _n[2] == _o[2],
                   [_n[1], _o[1], _n[2], _o[2]])
        elif QC.want('E-1'):   # regress — earthbase(본판) 안 돎 · E-1 아홉 칸 = 기준 스냅샷(앞 인도판 earth 스냅) · E-1 add19 헛잣대 = gate 만
            _rg_e1(sn, T2)
    if 'bio' in want:
        ls, _ = run('bio', W, cur)
        lines += ls
    if 'phys' in want:
        ls, _ = run('phys', W, cur)
        lines += ls
    if 'null' in want and QC.GATE:   # 0-헛잣대(biobase · physbase 바탕 묶음) = gate 만
        fails, base_lines = [], []
        for m in ('biobase', 'physbase'):
            l0, _ = run(m, W, basetxt)
            base_lines += l0
            fails += [x for x in l0 if x.startswith('FAIL')]
        got = {}
        for x in base_lines:
            nm = x.split(' | ')[1] if ' | ' in x else ''
            for pre in ('B', 'P', 'L'):
                if nm.startswith(pre + '-') or nm.startswith(pre + ' '):
                    d = got.setdefault(pre, {'PASS': 0, 'FAIL': 0})
                    d['PASS' if x.startswith('PASS') else 'FAIL'] += 1
        for pre, ko in (('B', '생물 껍데기·근거'), ('P', '물리 껍데기·아랫줄'), ('L', '학습로그 단추')):
            d = got.get(pre, {'PASS': 0, 'FAIL': 0})
            T2('0-헛잣대 이 판 앞(add3)에서 %s 묶음이 하나도 안 통과한다' % ko,
               d['PASS'] == 0 and (d['FAIL'] > 0 or len(fails) > 0), [d, len(fails)])
        T2('0-헛잣대 이 판 앞은 통과가 아니다', len(fails) > 0, len(fails))

    if 'x' in want:
        xb = _xbase_text() if QC.GATE else None   # regress — 교재 창 고침 전 판(24f1a373) git show 0
        ls, snx = run('x', W, cur)
        lines += ls
        if os.environ.get('XQUICK') or QC.REGRESS:   # regress — xbase(바탕 판) 안 돎 · X-0 헛잣대 = gate 만
            l0, snx0 = [], {}
        else:
            l0, snx0 = run('xbase', W, xb)
        st0 = {}
        for x in l0:
            if ' | X-' in x:
                nm = x.split(' | ')[1].split(' ')[0]
                st0[nm] = x.split(' | ')[0]
        # 헛잣대 — 새 기능이 없는 바탕 판에서는 이 항목들이 FAIL 해야 한다(지시서 §L 의 헛잣대 줄)
        must = ['X-A1', 'X-B1', 'X-C2', 'X-D3', 'X-E3', 'X-G2', 'X-H2', 'X-I1', 'X-J1']
        for nm in ([] if os.environ.get('XQUICK') or QC.REGRESS else must):
            T2('X-0 헛잣대 — 바탕 판(24f1a373)에서 %s 가 FAIL' % nm, st0.get(nm) == 'FAIL', st0.get(nm))
        if QC.GATE:
            lines.append('NOTE | X-0 바탕 판 X 항목 | ' + json.dumps({'PASS': sorted(k for k, v in st0.items() if v == 'PASS'),
                                                                   'FAIL': len([1 for v in st0.values() if v == 'FAIL'])}, ensure_ascii=False))
        a, b = (snx or {}).get('xmcw'), ((snx0 or {}).get('xmcw') if QC.GATE else QC.base('X-F5', (snx or {}).get('xmcw')))   # regress — 기준 = 앞 인도판 x 묶음의 🃏 창 글자 크기(스냅샷)
        T2('X-F5 🃏 창 글자 크기 = 바탕 판(#mcw 무접촉)', a is not None and a == b, [a, b])
        # ★ add1(2026-09-25) — 생물은 이 판이 **뜻한 차이**다(교재 창 이름·목록 창 쪽 줄·머리줄 ◀▶) → XB 묶음이 잰다. 물리만 바탕 판과 맞댄다.
        lines.append('NOTE | X-11 생물 | add1 로 뜻한 차이 — XB 묶음이 잰다(물리만 바탕 판 대조)')
        for m in (() if os.environ.get('XQUICK') else ('phys',)):
            _, sa = run('x' + m, W, cur)
            _, sb = run('x' + m + 'base', W, xb) if QC.GATE else (None, _rg_xside(m, sa))   # regress — x<m>base(바탕 판) 안 돎 · 바탕 쪽 값 = 기준 스냅샷(앞 인도판 x<m> 스냅)
            sa, sb = sa or {}, sb or {}
            nm = sa.get('names') or {}
            T2('X-11 %s — 새 이름(bkNav·PINFOR·wzHook·INKG_EA·QZ·refPaint·bwSpotsOn)이 안 생긴다' % m,
               # ★ 합치기 10/1(하위 에이전트 C) — physphone A-1(97883ef 본문 「창 무리(wzRaise · wzHook)를 HASBOOK 밖(SHELL 공통)으로 — 물리도 누른 창이 맨 앞」) — wzHook 은 물리에도 있다
               bool(nm) and not nm.get('bkNav') and all(v == 'undefined' for k, v in nm.items() if k not in ('bkNav', 'wzHook')) and nm.get('wzHook') in ('undefined', 'function'), nm)
            for k in sorted(set(sa) | set(sb)):
                if k in ('names',):
                    continue
                T2('X-11 %s %s = 바탕 판(DOM 글자)' % (m, k), sa.get(k) == sb.get(k),
                   [str(sa.get(k))[:160], str(sb.get(k))[:160]])

    if 'xb' in want:
        ls, _ = run('xb', W, cur)
        lines += ls
        if not os.environ.get('XQUICK') and QC.GATE:   # XB-0 헛잣대(xbbase 바탕 묶음 · git show) = gate 만
            l0, _ = run('xbbase', W, _xbbase_text())
            st0 = {}
            for x in l0:
                if ' | XB-' in x:
                    nm = x.split(' | ')[1].split(' ')[0]
                    st0[nm] = x.split(' | ')[0]
            # 헛잣대 — 생물에 새 기능이 없는 바탕 판에서는 이 항목들이 FAIL 해야 한다(지시서 add1 관문 1 · 2 · 3 · 4 · 5)
            for nm in ['XB-A1', 'XB-A2', 'XB-D1', 'XB-D3', 'XB-B2', 'XB-C0', 'XB-E2', 'XB-F1', 'XB-H1', 'XB-I1', 'XB-J1']:
                T2('XB-0 헛잣대 — 바탕 판(f07e9d08)에서 %s 가 FAIL' % nm, st0.get(nm) == 'FAIL', st0.get(nm))
            lines.append('NOTE | XB-0 바탕 판 XB 항목 | ' + json.dumps({'PASS': sorted(k for k, v in st0.items() if v == 'PASS'),
                                                                 'FAIL': len([1 for v in st0.values() if v == 'FAIL'])}, ensure_ascii=False))

    if QC.want('Z'):   # smoke — 소스 글 셈(Z · add17~19)은 smoke 칸이 아니다
        lines += static_checks()
    npass = sum(1 for x in lines if x.startswith('PASS'))
    nfail = sum(1 for x in lines if x.startswith('FAIL'))
    nnote = sum(1 for x in lines if x.startswith('NOTE'))
    for x in lines:
        print(x)
    print('\n== 자과앱 세 과목 %d PASS / %d FAIL / %d NOTE / %d항 ==' % (npass, nfail, nnote, len(lines)))
    print('캡처: %s' % CAP)
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
