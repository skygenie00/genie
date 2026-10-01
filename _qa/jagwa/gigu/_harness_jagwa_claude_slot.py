# -*- coding: utf-8 -*-
"""자과앱 「Claude」 칸 · 읽기 판 · 모션 — 헤드리스 검산 (묶음 CL)
(2026-09-22 · gigu/_task_jagwa_claude_slot.md §B)

  CL-1  화면 글자 — 세 과목에서 「GPT」 0 · 「Claude」 가 자리마다 선다
  CL-2  데이터 무변 — kv 'gpt' · SYNC_KEYS · 내보내기 칸 이름 무변 (+ 바탕→새 판 왕복)
  CL-3  읽기 판 — 절 머리 5 · 글머리 줄 수 = 원문 · 주입 헛잣대
  CL-4  고치기 → 저장 → 읽기 판 복귀 · 지우기 회귀
  CL-5  모션 — 72번만 단추 · iframe 200 · 71번 0 · index.json 404 판 0
  CL-6  §A-4 병합 — 빈 기기 · 기록 있는 기기 · 내 것이 더 새것일 때
  CL-0  헛잣대 — 바탕 판에서 CL-1·CL-5 가 하나도 안 통과한다
  CL-Z  원본 대조(파이썬)

⚠ 픽셀 게이트는 쓰지 않는다(CLAUDE.md 「자과앱에는 픽셀 게이트를 걸지 않는다」).
   DOM 존재·개수·글자·getBoundingClientRect 로만 잰다.

    PYTHONIOENCODING=utf-8 python _harness_jagwa_claude_slot.py
"""
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

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _harness_earth_shell as E          # STUB · HEAD · TAIL · CHROME 을 그대로 쓴다

GENIE = E.GENIE
SRC = E.SRC
CHROME = E.CHROME
SPDROOT = E.SPDROOT
MAT = os.path.join(HERE, 'claude_motion')
MOTDIR = os.path.join(GENIE, 'jagwa', 'motion')
OUT = os.path.join(os.environ.get('TEMP', '.'), 'hclaudeslot')
os.makedirs(OUT, exist_ok=True)

BASE_MD5 = '81223389bbd567d199ee999beeb8805e'      # 고침 전(genie 0c19a60 · add19)

MD = io.open(os.path.join(MAT, 'phys_72.md'), encoding='utf-8', newline='').read().replace('\r\n', '\n')
NSEC = len([x for x in MD.split('\n') if re.match(r'^\s*[①-⑩]', x)])
NUL = len([x for x in MD.split('\n') if re.match(r'^\s*-\s+', x)])
NOL = len([x for x in MD.split('\n') if re.match(r'^\s*\d+\.\s+', x)])


def md5lf(b):
    return hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest()


def base_text():
    keep = os.path.join(os.environ.get('TEMP', '.'), 'jagwa_base_claude_slot.html')
    for p in (keep,):
        if os.path.exists(p):
            b = open(p, 'rb').read()
            if md5lf(b) == BASE_MD5:
                return b.replace(b'\r\n', b'\n').decode('utf-8')
    for rev in ('0c19a60', 'HEAD', 'HEAD~1', 'HEAD~2'):
        b = subprocess.run(['git', '-C', GENIE, 'show', rev + ':jagwa/index.html'],
                           capture_output=True).stdout
        if b and md5lf(b) == BASE_MD5:
            open(keep, 'wb').write(b.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n'))
            return b.replace(b'\r\n', b'\n').decode('utf-8')
    raise SystemExit('NG  바탕 판(md5 %s)을 못 찾았다' % BASE_MD5)


# ══════════════════════════════════════════════════════════════════════════
BODY_CL = r"""
   await wait(1500);
   const MD=__MD__, NSEC=__NSEC__, NUL=__NUL__, NOL=__NOL__;
   const P=(SUBJ_ID==='phys');
   if(typeof CARD_LAYER!=='undefined'&&CARD_LAYER&&typeof loadEarthData==='function'){
     try{await loadEarthData()}catch(e){}
   }
   FL.past='';FL.q='';FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';FL.lv='';FL.star=false;FL.year='';
   draw(); await wait(600);
   const NO = P?72:((DATA[0]||[])[F.NO]);
   N('CL 밑준비',{subj:SUBJ_ID,DATA:DATA.length,NO:NO,
     SHELL:(typeof SHELL==='undefined'?null:SHELL),
     CARD:(typeof CARD_LAYER==='undefined'?null:CARD_LAYER),
     code:(NO!=null&&rec(NO))?rec(NO)[F.CODE]:null});
   const sheetNow=()=>document.getElementById('sh-gpt')||$$$('body>.sheet').pop()||null;
   const killSheets=()=>{$$$('body>.sheet').forEach(x=>x.remove())};
   const bodyText=()=>{const c=document.body.cloneNode(true);
     [...c.querySelectorAll('script,style')].forEach(x=>x.remove());
     return String(c.textContent||'')};
   const SCLOSE='<'+'/script>';

   /* ══════════ CL-2 왕복 — 바탕 판이 저장한 글을 새 판이 그대로 읽는가 ══════════
      ⚠ **CL-1 보다 먼저** 잰다. CL-1 이 GP[NO] 에 같은 글을 넣으므로 뒤에 재면 거저 참이 된다. */
   const SEEDED=localStorage.getItem('CL_SEEDED');
   await grp('CL2', async()=>{
     if(!SEEDED){N('CL-2 왕복 모드가 아니다(seed 없음)',null);return}
     const n=+SEEDED;
     T('CL-2 ★바탕 판에서 저장한 글이 새 판에서 글자 그대로 읽힌다',gptOf(n)===MD,
       [(gptOf(n)||'').length,MD.length,(gptOf(n)||'').slice(0,30)]);
     T('CL-2 ★그 글이 목록에서 「Claude」 태그로 선다',
       $$$('#list .item .tag.gp').some(x=>txt(x)==='Claude'),
       $$$('#list .item .tag.gp').map(x=>txt(x)).slice(0,3));
     await openView(n); await wait(1100);
     T('CL-2 ★그 글이 툴바에서 「Claude ✓」 로 선다',
       txt(document.getElementById('tGpt'))==='Claude ✓',txt(document.getElementById('tGpt')));
     killSheets(); gptSheet(n); await wait(700);
     const sh=sheetNow();
     T('CL-2 ★그 글이 읽기 판으로 뜬다',!!sh&&!!sh.querySelector('.gpread'),!!sh);
     killSheets();
   });

   /* ══════════ CL-1 화면 글자 (세 과목) ══════════ */
   await grp('CL1', async()=>{
     if(NO==null){T('CL-1 문항이 있다',false,null);return}
     GP[NO]=MD; await saveGP();
     draw(); await wait(700);
     const tags=$$$('#list .item .tag.gp').map(x=>txt(x));
     await openView(NO); await wait(1100);
     const btn=document.getElementById('tGpt');
     /* ⚠ 보라 태그와 단추 ✓ 는 **물리 갈래**다(바탕 그대로):
          태그 5292 `const PH=!HASBOOK` · ✓ 는 5349 `if(HASBOOK)showProblem=…` 가
          syncGptBtn 을 부르는 옛 showProblem 을 갈아 끼워서 카드 층에서는 안 돈다.
        그래서 물리에서만 값을 박아 재고, 카드 층은 **바탕 판과 맞대서** 잰다(아래 실측). */
     if(P){
       T('CL-1 목록 보라 태그가 「Claude」다',
         tags.length>0&&tags.every(t=>t==='Claude'),tags.slice(0,4));
       T('CL-1 툴바 단추 = 「Claude ✓」',txt(btn)==='Claude ✓',txt(btn));
     }
     N('CL-1 실측 태그·단추',{tags:tags.slice(0,4),btn:txt(btn)});
     gptSheet(NO); await wait(700);
     const sh=sheetNow();
     T('CL-1 창 제목 = 「N번 Claude 풀이」',
       !!sh&&txt(sh.querySelector('h2')).indexOf(NO+'번 Claude 풀이')===0,
       sh?txt(sh.querySelector('h2')):null);
     const all=bodyText(), hit=all.indexOf('GPT');
     T('CL-1 ★화면 글자에 「GPT」 가 0곳이다',
       hit<0, hit<0?0:all.slice(Math.max(0,hit-70),hit+40));
     T('CL-1 화면에 「Claude」 가 있다',all.indexOf('Claude')>=0);
     killSheets(); await wait(150);
   });

   /* ══════════ CL-2 데이터 무변 ══════════ */
   await grp('CL2', async()=>{
     T('CL-2 SYNC_KEYS 에 gpt 가 그대로 있다',SYNC_KEYS.indexOf('gpt')>=0,SYNC_KEYS.indexOf('gpt'));
     N('CL-2 SYNC_KEYS',SYNC_KEYS.slice());
     const kv=await get('kv','gpt');
     T('CL-2 ★IndexedDB 칸 이름이 gpt 그대로고 글이 같다',
       !!kv&&kv[NO]===MD,kv?Object.keys(kv).length:null);
   });

   if(P){
   /* ══════════ CL-3 읽기 판 ══════════ */
   await grp('CL3', async()=>{
     GP[NO]=MD; await saveGP();
     killSheets(); gptSheet(NO); await wait(700);
     const sh=sheetNow(), rd=sh&&sh.querySelector('.gpread');
     T('CL-3 읽기 판이 먼저 뜬다 · textarea 가 없다',!!rd&&!sh.querySelector('#gpIn'),
       [!!rd,!!(sh&&sh.querySelector('#gpIn'))]);
     T('CL-3 절 머리 개수 = 원문 ①~⑤',
       !!rd&&rd.querySelectorAll('.gph').length===NSEC,
       [rd?rd.querySelectorAll('.gph').length:null,NSEC]);
     const hs=rd?[...rd.querySelectorAll('.gph')].map(x=>txt(x)):[];
     T('CL-3 절 머리 다섯이 ①②③④⑤ 로 시작한다',
       hs.map(h=>h.charAt(0)).join('')==='①②③④⑤',hs);
     T('CL-3 글머리 줄 수 = 원문 `- ` 줄 수',
       !!rd&&rd.querySelectorAll('.gpul li').length===NUL,
       [rd?rd.querySelectorAll('.gpul li').length:null,NUL]);
     T('CL-3 번호 줄 수 = 원문 `1. ` 줄 수',
       !!rd&&rd.querySelectorAll('.gpol li').length===NOL,
       [rd?rd.querySelectorAll('.gpol li').length:null,NOL]);
     T('CL-3 첫 줄(코드·정답)이 문단으로 남았다',
       !!rd&&txt(rd).indexOf('PA2502')>=0,txt(rd).slice(0,40));
   });

   /* ══════════ CL-3 표 — 재료에 0건이라 **손으로 지어** 잰다(표본 0 PASS 는 헛패스) ══════════ */
   await grp('CL3', async()=>{
     const tb='① 표 시험\n\n| 보기 | 값 | 판정 |\n|---|---:|---|\n| ① | 10 | vx 만 |\n'
             +'| ③ | 10√5 | **정답** |\n\n뒤 문단\n';
     GP[NO]=tb; await saveGP();
     killSheets(); gptSheet(NO); await wait(800);
     const sh=sheetNow(), rd=sh&&sh.querySelector('.gpread');
     const t=rd&&rd.querySelector('table.gptb');
     T('CL-3 표 — <table class="gptb"> 가 하나 섰다',
       !!rd&&rd.querySelectorAll('table.gptb').length===1,
       rd?rd.querySelectorAll('table.gptb').length:null);
     T('CL-3 표 — 머리 칸 3 · 몸 줄 2 · 몸 칸 6',
       !!t&&t.querySelectorAll('thead th').length===3
          &&t.querySelectorAll('tbody tr').length===2
          &&t.querySelectorAll('tbody td').length===6,
       t?[t.querySelectorAll('thead th').length,t.querySelectorAll('tbody tr').length,
          t.querySelectorAll('tbody td').length]:null);
     T('CL-3 표 — 가름줄(|---|)이 칸으로 안 남았다',
       !!t&&txt(t).indexOf('---')<0,t?txt(t).slice(0,60):null);
     T('CL-3 표 — 칸 안 **굵게** 가 <b> 로 산다',
       !!t&&t.querySelectorAll('td b').length===1,
       t?t.querySelectorAll('td b').length:null);
     T('CL-3 표 — 표 앞 절 머리와 뒤 문단이 그대로 산다',
       !!rd&&rd.querySelectorAll('.gph').length===1&&rd.querySelectorAll('.gpp').length===1
          &&txt(rd).indexOf('뒤 문단')>0,
       rd?[rd.querySelectorAll('.gph').length,rd.querySelectorAll('.gpp').length]:null);
     GP[NO]=MD; await saveGP(); killSheets();
   });

   /* ══════════ CL-3 주입 헛잣대 ══════════ */
   await grp('CL3', async()=>{
     const bad='① 주입 시험\n- <script>window.__pwn=1;'+SCLOSE+'\n'
              +'- <img src=x onerror="window.__pwn=2">\n- **굵게** 도 된다\n';
     GP[NO]=bad; await saveGP();
     killSheets(); gptSheet(NO); await wait(800);
     const sh=sheetNow(), rd=sh&&sh.querySelector('.gpread');
     T('CL-3 주입 — <script> 가 글자로 보인다',
       !!rd&&txt(rd).indexOf('<script>')>=0,rd?txt(rd).slice(0,110):null);
     T('CL-3 주입 — 읽기 판 안에 script·img 요소가 0개다',
       !!rd&&rd.querySelectorAll('script,img').length===0,
       rd?rd.querySelectorAll('script,img').length:null);
     T('CL-3 주입 — 실행되지 않았다',typeof window.__pwn==='undefined',
       (typeof window.__pwn==='undefined')?null:window.__pwn);
     T('CL-3 **굵게** 는 <b> 로 산다',!!rd&&rd.querySelectorAll('b').length>=1,
       rd?rd.querySelectorAll('b').length:null);
     GP[NO]=MD; await saveGP(); killSheets();
   });

   /* ══════════ CL-4 고치기 → 저장 → 읽기 판 · 지우기 회귀 ══════════ */
   await grp('CL4', async()=>{
     GP[NO]=MD; await saveGP();
     await openView(NO); await wait(900);
     killSheets(); gptSheet(NO); await wait(700);
     let sh=sheetNow();
     T('CL-4 읽기 판에 「고치기」 단추가 있다',!!sh.querySelector('#gpEdit'));
     sh.querySelector('#gpEdit').click(); await wait(400);
     sh=sheetNow();
     const ta=sh.querySelector('#gpIn');
     T('CL-4 고치기 → 옛 textarea 꼴 넷이 그대로다',
       !!ta&&!!sh.querySelector('#gpPaste')&&!!sh.querySelector('#gpDel')
           &&!!sh.querySelector('#gpNo')&&!!sh.querySelector('#gpSave'),
       [!!ta,!!sh.querySelector('#gpPaste'),!!sh.querySelector('#gpDel'),
        !!sh.querySelector('#gpNo'),!!sh.querySelector('#gpSave')]);
     T('CL-4 textarea 에 원문이 들어 있다',!!ta&&ta.value===MD,ta?ta.value.length:null);
     ta.value=MD+'\n- 덧붙인 줄';
     sh.querySelector('#gpSave').click(); await wait(900);
     sh=sheetNow();
     T('CL-4 ★저장하면 읽기 판으로 돌아온다',
       !!sh&&!!sh.querySelector('.gpread')&&!sh.querySelector('#gpIn'),
       [!!sh,!!(sh&&sh.querySelector('.gpread')),!!(sh&&sh.querySelector('#gpIn'))]);
     T('CL-4 저장된 글에 덧붙인 줄이 있다',(gptOf(NO)||'').indexOf('덧붙인 줄')>0);
     T('CL-4 글머리가 하나 늘어 보인다',
       !!sh&&sh.querySelectorAll('.gpul li').length===NUL+1,
       [sh?sh.querySelectorAll('.gpul li').length:null,NUL+1]);
     /* 지우기 — 지금 동작 회귀 */
     sh.querySelector('#gpEdit').click(); await wait(400);
     sh=sheetNow();
     sh.querySelector('#gpDel').click(); await wait(900);
     T('CL-4 지우기 → 창이 닫힌다',!document.getElementById('sh-gpt'));
     T('CL-4 지우기 → 글이 사라졌다',!gptOf(NO),gptOf(NO));
     T('CL-4 지우기 → 단추에서 ✓ 가 사라졌다',
       txt(document.getElementById('tGpt'))==='Claude',txt(document.getElementById('tGpt')));
     draw(); await wait(500);
     T('CL-4 지우기 → 목록 보라 태그가 사라졌다',
       $$$('#list .item .tag.gp').length===0,$$$('#list .item .tag.gp').length);
     GP[NO]=MD; await saveGP(); killSheets();
   });

   /* ══════════ CL-5 모션 ══════════ */
   await grp('CL5', async()=>{
     GP[NO]=MD; await saveGP();
     killSheets(); gptSheet(NO); await wait(1100);
     let sh=sheetNow();
     const bar=sh&&sh.querySelector('#gpMotBar');
     const mb=bar&&bar.querySelector('#gpMot');
     T('CL-5 ★72번에 「▶ 모션」 단추가 선다',
       !!bar&&bar.style.display!=='none'&&txt(mb)==='▶ 모션',
       [!!bar,bar?bar.style.display:null,txt(mb)]);
     T('CL-5 모션 목록을 읽었다',
       (typeof MOT!=='undefined')&&!!MOT&&Array.isArray(MOT.phys)&&MOT.phys.indexOf(72)>=0,
       (typeof MOT!=='undefined')?MOT:'MOT 없음');
     if(!mb){T('CL-5 단추가 없어 나머지를 못 잰다',false,null);return}
     mb.click(); await wait(600);
     const f=sh.querySelector('#gpMotFrame');
     T('CL-5 누르면 iframe 이 뜬다',
       !!f&&sh.querySelector('#gpMotBox').style.display!=='none',!!f);
     T('CL-5 iframe 이 같은 오리진 motion/phys_72.html 이다',
       !!f&&new URL(f.src,location.href).origin===location.origin
          &&/\/motion\/phys_72\.html$/.test(new URL(f.src,location.href).pathname),
       f?f.src:null);
     const fr=f?f.getBoundingClientRect():null;
     T('CL-5 iframe 높이가 480px 이고 폭이 창을 채운다',
       !!fr&&Math.abs(fr.height-480)<2&&fr.width>100,
       fr?[Math.round(fr.width),Math.round(fr.height)]:null);
     let st=0;try{const r=await __nativeFetch('motion/phys_72.html');st=r.status}catch(e){st=-1}
     T('CL-5 motion/phys_72.html 이 200 이다',st===200,st);
     /* 같은 오리진이라 iframe 안을 읽을 수 있다 — 쪽이 **실제로 떴는지**까지 잰다.
        ⚠ 그림이 눈에 보이는가는 게이트에 넣지 않는다(CLAUDE.md) — 사용자 확인 항목이다. */
     await wait(900);
     let cd=null; try{cd=f.contentDocument}catch(e){}
     const cvz=cd&&cd.getElementById('cv');
     T('CL-5 모션 쪽이 iframe 안에서 떴다(그림판 · 재생 단추 · 눈금)',
       !!cd&&!!cvz&&!!cd.getElementById('play')&&!!cd.getElementById('ts'),
       cd?[!!cvz,!!cd.getElementById('play'),!!cd.getElementById('ts')]:'contentDocument 못 읽음');
     T('CL-5 모션 그림판이 폭을 잡았다(스크립트가 돌았다)',
       !!cvz&&cvz.width>0&&cvz.getBoundingClientRect().width>100,
       cvz?[cvz.width,Math.round(cvz.getBoundingClientRect().width)]:null);
     /* ⚠ 정적 HTML 은 vy 「20」 · 자리 「0, 0」 인데 `draw()` 가 `toFixed(1)` 로 다시 쓴다.
        그래서 「20.0」·「0.0, 0.0」 이 곧 **스크립트가 돌았다는 증거**다(2026-09-22 실측).
        vx 는 코드가 다시 쓰지 않아 정적 값 「10」 그대로여야 한다 — 문제의 vx 가 10 이다. */
     T('CL-5 모션 쪽 첫 값이 문제 그대로다(vx 10 · vy 20.0 · 자리 0.0, 0.0)',
       !!cd&&txt(cd.getElementById('mvx'))==='10'
          &&txt(cd.getElementById('mvy'))==='20.0'
          &&txt(cd.getElementById('mpos'))==='0.0, 0.0',
       cd?[txt(cd.getElementById('mvx')),txt(cd.getElementById('mvy')),
           txt(cd.getElementById('mpos'))]:null);
     mb.click(); await wait(400);
     T('CL-5 다시 누르면 닫힌다',
       sh.querySelector('#gpMotBox').style.display==='none',
       sh.querySelector('#gpMotBox').style.display);
     killSheets();
     /* 71번엔 단추가 없다 */
     GP[71]=MD; await saveGP();
     gptSheet(71); await wait(1000);
     sh=sheetNow();
     const b71=sh&&sh.querySelector('#gpMotBar');
     T('CL-5 ★71번엔 모션 단추가 없다',!!b71&&b71.style.display==='none',
       b71?b71.style.display:'#gpMotBar 자체가 없다');
     delete GP[71]; await saveGP(); killSheets();
   });

   /* ══════════ CL-6 §A-4 병합 ══════════ */
   await grp('CL6', async()=>{
     if(typeof recMerge!=='function'){T('CL-6 recMerge 가 있다',false,null);return}
     const mkR=t=>({v:1,savedAt:'x',by:'검산',data:{gpt:{'72':MD}},u:{'gpt|72':t},gone:{}});
     /* 실물 기록과 같게 — 기기에는 gpt|72 도장이 **한 곳도 없다**(studyplandata 실측) */
     const clr=()=>{[U_KEY,GONE_KEY].forEach(k=>{const o=JSON.parse(localStorage.getItem(k)||'{}');
       delete o['gpt|72'];localStorage.setItem(k,JSON.stringify(o))})};
     /* ⓐ 빈 기기 */
     GP={}; await put('kv','gpt',GP); stampAll(); clr();
     const st0=JSON.stringify(ST),qt0=JSON.stringify(QT),cx0=JSON.stringify(CX);
     let res=await recMerge(mkR(Date.now()));
     T('CL-6 ⓐ 빈 기기 — GP[72] 가 원문 글자 그대로 들어왔다',gptOf(72)===MD,
       [res.took,(gptOf(72)||'').length,MD.length]);
     T('CL-6 ⓐ status·qtype·conc 는 무변',
       JSON.stringify(ST)===st0&&JSON.stringify(QT)===qt0&&JSON.stringify(CX)===cx0);
     T('CL-6 ⓐ 지워진 칸 0',res.del===0,res.del);
     /* ⓑ 기록 있는 기기 */
     GP={'65':'내가 쓴 65번 풀이','66':'내가 쓴 66번 풀이'}; await put('kv','gpt',GP);
     stampAll(); clr();
     const st1=JSON.stringify(ST);
     res=await recMerge(mkR(Date.now()));
     T('CL-6 ⓑ 기록 있는 기기 — GP[72] 가 원문 글자 그대로 들어왔다',gptOf(72)===MD,
       [res.took,(gptOf(72)||'').length]);
     T('CL-6 ⓑ 내 65·66 은 무변',
       GP['65']==='내가 쓴 65번 풀이'&&GP['66']==='내가 쓴 66번 풀이',[GP['65'],GP['66']]);
     T('CL-6 ⓑ status 무변',JSON.stringify(ST)===st1);
     T('CL-6 ⓑ 지워진 칸 0',res.del===0,res.del);
     /* ⓒ 내가 더 새것이면 안 덮는다 */
     GP={'72':'내가 먼저 쓴 72번'}; await put('kv','gpt',GP); stampAll();
     res=await recMerge(mkR(Date.now()-600000));
     T('CL-6 ⓒ 내 것이 더 새것이면 원격이 못 덮는다',gptOf(72)==='내가 먼저 쓴 72번',gptOf(72));
     /* 되돌리기 */
     GP={}; GP[NO]=MD; await put('kv','gpt',GP);
   });
   }

   T('CL 콘솔 오류 0',(window.__err||[]).length===0,window.__err);
"""


def build(mode, src_text, subj):
    html = src_text
    html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js',
                        E.STUB.replace('__SUBJ__', subj)
                        + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    body = (BODY_CL.replace('__MD__', json.dumps(MD, ensure_ascii=False))
                   .replace('__NSEC__', str(NSEC)).replace('__NUL__', str(NUL))
                   .replace('__NOL__', str(NOL)))
    open(os.path.join(OUT, 'app.html'), 'w', encoding='utf-8', newline='').write(
        html.replace('</body>', E.HEAD + body + E.TAIL + '</body>', 1))
    # 바탕 판에 글을 저장해 두고 새 판으로 넘어가는 쪽(왕복 · CL-2)
    seed = ("<script>(function(){const t=" + json.dumps(MD, ensure_ascii=False) + ";"
            "function go(){try{GP[72]=t;saveGP().then(()=>{"
            "localStorage.setItem('CL_SEEDED','72');location.replace('app.html')})}"
            "catch(e){localStorage.setItem('CL_SEEDERR',String(e));location.replace('app.html')}}"
            "window.addEventListener('load',()=>setTimeout(go,2500));})()</script>")
    open(os.path.join(OUT, 'seed.html'), 'w', encoding='utf-8', newline='').write(
        base_text().replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js',
                            E.STUB.replace('__SUBJ__', 'phys')
                            + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
                   .replace('</body>', seed + '</body>', 1))
    # 모션 파일 — 404 판에서는 목록을 안 내놓는다
    m = os.path.join(OUT, 'motion')
    shutil.rmtree(m, ignore_errors=True)
    os.makedirs(m, exist_ok=True)
    shutil.copyfile(os.path.join(MOTDIR, 'phys_72.html'), os.path.join(m, 'phys_72.html'))
    if mode != 'phys404':
        shutil.copyfile(os.path.join(MOTDIR, 'index.json'), os.path.join(m, 'index.json'))


def run(mode, subj, src_text, secs=260, start='app.html'):
    build(mode, src_text, subj)
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
                if rel == subj + '/기록.json':
                    # ★ 2026-10-01 claude_p002 — 물리 기록에 Claude 풀이 97(gpt 칸)을 적재하자 왕복 판(cross)이 visibilitychange 동기화로 그 칸을 받아
                    #   CL-4 「지우기 → 목록 보라 태그 0」 이 1 로 FAIL 했다(실측 CL-1 태그 ["Claude","Claude"] · 앱은 옳다 · 바탕0 은 기록 gpt 가 72 하나라 안 드러남)
                    #   → 기록 사본에서 gpt 칸과 그 도장만 비운다(CL2 9/30 _task_qa_baseline A-6(d) 와 같은 꼴 · 이 묶음은 제가 넣은 GP 로만 잰다 · 다른 칸 그대로)
                    j = json.loads(b.decode('utf-8'))
                    j.setdefault('data', {})['gpt'] = {}
                    for kk in ('u', 'gone'):
                        j[kk] = {x: y for x, y in (j.get(kk) or {}).items() if not str(x).startswith('gpt|')}
                    b = json.dumps(j, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
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
            if self.path.startswith('/snap') or self.path.startswith('/cap'):
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
                          'http://127.0.0.1:%d/%s' % (port, start)],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    got = done.wait(secs)
    p.terminate()
    try:
        p.wait(10)
    except Exception:
        p.kill()
    srv.shutdown()
    print('  [%s] %.0fs' % (mode, time.time() - t0))
    if not got:
        return ['FAIL | %s 묶음이 시간 안에 안 끝났다 | %s'
                % (mode, box.get('partial', '(중간 결과 없음)')[-2500:])]
    return [ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()]


def static_checks():
    out = []

    def T(name, cond, info=''):
        out.append(('PASS' if cond else 'FAIL') + ' | ' + name
                   + ('' if cond else ' | ' + json.dumps(info, ensure_ascii=False, default=str)))

    def N(name, info=''):
        out.append('NOTE | ' + name + ' | ' + json.dumps(info, ensure_ascii=False, default=str))

    raw = open(SRC, 'rb').read()
    s = raw.replace(b'\r\n', b'\n').decode('utf-8')
    base = base_text()
    # ★ A-6(d) 9/30 _task_qa_baseline — 아래 셋(소스 「GPT」 한 줄 · syncGptBtn 수 · 사라진 바탕 줄)은 이 판(claude_slot) 인도 검산이다 → 새 쪽을 인도 판 f810502 로 박는다
    #   (두 커밋 사이 0c19a60 ↔ f810502 · 인도 결과 _harness_jagwa_claude_slot_result_20260922.txt 176/0 · 결정로그 9/22 00:49). 뒤 판이 뜻해서 소스를 바꿨다 —
    #   add1 007fde4 §A-3 syncGptBtn 3→7 · jagwa_search eb1113e A-1 이 옛 기록 주석(add5 · 「GPT」)이 든 FL.q 덩이를 뗌 · 사라진 줄 28 → 110(뒤 판 여럿). 그 밖 칸은 지금 소스(s)
    s_dl = subprocess.run(['git', '-C', GENIE, 'show', 'f810502:jagwa/index.html'], capture_output=True).stdout.replace(b'\r\n', b'\n').decode('utf-8')

    # ── 줄끝 ──
    T('CL-Z 줄끝이 CRLF 그대로다(외톨이 LF 0)',
      raw.count(b'\r\n') > 9000 and raw.replace(b'\r\n', b'').count(b'\n') == 0,
      [raw.count(b'\r\n'), raw.replace(b'\r\n', b'').count(b'\n')])

    # ── §A-1 보이는 글자 ──
    vis = [l for l in s_dl.split('\n') if 'GPT' in l]   # ★ A-6(d) — 인도 판 f810502(위 s_dl) · jagwa_search(eb1113e)가 그 주석 줄을 뗐다
    T('CL-Z 소스에 남은 「GPT」 는 옛 기록 주석 한 줄뿐이다',
      len(vis) == 1 and 'add5' in vis[0], [v.strip()[:90] for v in vis])

    # ── 데이터 이름 무변 ──
    for pat, ko in [(r"SYNC_KEYS:\['status'", 'SYNC_KEYS 줄'),
                    (r"gpt\s*:\s*GP", '내보내기 칸 gpt:GP'),
                    (r"put\('kv','gpt'", "put\\('kv','gpt'\\)"),
                    (r"get\('kv','gpt'", "get\\('kv','gpt'\\)"),
                    (r"const gptOf=", 'gptOf 정의'),
                    (r"\['gptSheet','gpt'\]", 'SHWIN 표'),
                    (r"'gpt','twin'", "SHPERQ·SYNC_KEYS 의 'gpt'"),
                    (r'id="tGpt"', '단추 id tGpt'),
                    (r'class="tag gp"', '태그 class gp'),
                    (r'\bsyncGptBtn\b', 'syncGptBtn')]:
        a, b = len(re.findall(pat, s_dl if ko == 'syncGptBtn' else s)), len(re.findall(pat, base))   # ★ A-6(d) — syncGptBtn 만 인도 판 f810502(add1 §A-3 이 부름 넷을 더함 · 이름은 그대로)
        T('CL-2 데이터 이름 무변 — %s : 바탕과 같은 수다' % ko, a == b and a > 0, [a, b])

    for i, ln in enumerate(base.split('\n')):
        if 'SYNC_KEYS:[' in ln:
            T('CL-2 SYNC_KEYS 줄이 바탕에 있던 그대로다 (%d번째 줄)' % (i + 1),
              ln in s, ln.strip()[:80])

    # ── 더하기만 했나 ──
    T('CL-Z 바탕보다 줄이 늘기만 했다',
      len(s.split('\n')) >= len(base.split('\n')),
      [len(s.split('\n')), len(base.split('\n'))])
    gone = [l for l in set(base.split('\n')) - set(s_dl.split('\n')) if l.strip()]   # ★ A-6(d) — 인도 판 f810502(위 s_dl)
    T('CL-Z 사라진 바탕 줄은 gptSheet·글자 고친 자리뿐이다 (%d줄)' % len(gone),
      len(gone) <= 48, [g.strip()[:70] for g in gone[:12]])
    N('CL-Z 사라진 바탕 줄', [g.strip()[:70] for g in gone])

    # ── 새 이름이 겹치지 않았나 ──
    for nm in ['gpRender', 'gpInline', 'gpCells', 'gpIsSep', 'motLoad', 'motHas',
               'GP_SEC', 'GP_UL', 'GP_OL']:
        T('CL-Z 새 이름 %s 가 바탕에 없던 이름이다' % nm, nm not in base, nm)
        # ⚠ GP_SEC·GP_UL·GP_OL 은 `const A=…, B=…, C=…;` 한 줄이라
        #   `const 이름` 만 보면 뒤 둘을 0으로 센다. 쉼표 선언도 같이 본다.
        decl = re.findall(r'(?:(?:const|var|let|function)\s+|,\s*)' + nm + r'\s*[=(]', s)
        T('CL-Z 새 이름 %s 가 한 번만 정의된다' % nm, len(decl) == 1, decl)

    # ── §A-3 파일 ──
    for f, mat in [('phys_72.html', os.path.join(MAT, 'phys_72.html'))]:
        p = os.path.join(MOTDIR, f)
        # ★ A-6(d) 9/30 _task_qa_baseline — 줄끝만 뺀 바이트로 맞댄다: 새로 만든 작업트리(qa 워크트리 · core.autocrlf)는 CRLF 로 풀림(6,159 = 6,093 + 66) · git blob = 재료(LF) 그대로
        ok = os.path.isfile(p) and open(p, 'rb').read().replace(b'\r\n', b'\n') == open(mat, 'rb').read().replace(b'\r\n', b'\n')
        T('CL-Z motion/%s 이 재료와 바이트가 같다' % f, ok,
          [os.path.getsize(p) if os.path.isfile(p) else None, os.path.getsize(mat)])
    ij = os.path.join(MOTDIR, 'index.json')
    try:
        j = json.load(open(ij, encoding='utf-8'))
    except Exception as e:
        j = None
        N('CL-Z index.json 읽기 실패', str(e))
    # 2026-09-29 claude_e001 — 지학 149·84 를 더했다(earth 키). 이 묶음이 지킬 것은 물리 값 [72] 무변이다.
    # ★ 2026-10-01 claude_p002 — 물리 97 을 끝에 더했다(phys = [72, 97]). 「phys = [72]」 는 값을 박은 잣대라 뒤 판마다 거짓 FAIL
    #   → 「phys 맨 앞 = 72 그대로」 로 갈음(72 가 빠지거나 앞자리를 내주면 여전히 FAIL)
    T('CL-Z motion/index.json 의 phys 맨 앞 = 72 무변(9/29 claude_e001 부터 earth · 10/1 claude_p002 부터 phys 97 더함)',
      isinstance(j, dict) and (j.get('phys') or [])[:1] == [72], j)
    T('CL-Z motion 폴더에 .pdf 가 없다(공개 저장소)',
      not [x for x in os.listdir(MOTDIR) if x.lower().endswith('.pdf')],
      os.listdir(MOTDIR))
    T('CL-Z motion/phys_72.html 에 바깥 주소가 없다(CDN 0)',
      not re.search(r'(src|href)\s*=\s*["\']https?://',
                    open(os.path.join(MOTDIR, 'phys_72.html'), encoding='utf-8').read()))
    return out


def main():
    src = io.open(SRC, encoding='utf-8', newline='').read().replace('\r\n', '\n')
    cur = md5lf(open(SRC, 'rb').read())
    print('[src ] md5(LF) %s' % cur)
    if cur == BASE_MD5:
        raise SystemExit('NG  아직 고치기 전 판이다 — _patch_jagwa_claude_slot.py 를 먼저 돌려라')
    base = base_text()
    lines = []
    meas = {}

    keyset = {}

    def grab(mode, r):
        """모드별 실측을 받아 둔다 — 카드 층 태그·✓ 와 SYNC_KEYS 는 바탕과 맞대야 한다."""
        for x in r:
            if '실측 태그·단추' in x:
                try:
                    meas[mode] = json.loads(x.split('|', 2)[2].strip())
                except Exception:
                    meas[mode] = None
            elif 'CL-2 SYNC_KEYS' in x and x.startswith('NOTE'):
                try:
                    keyset[mode] = json.loads(x.split('|', 2)[2].strip())
                except Exception:
                    keyset[mode] = None

    only = [a for a in sys.argv[1:] if not a.startswith('-')]
    for mode, subj, txt_, secs, start in [
            ('phys', 'phys', src, 320, 'app.html'),
            ('bio', 'bio', src, 260, 'app.html'),
            ('earth', 'earth', src, 260, 'app.html'),
            ('phys404', 'phys', src, 260, 'app.html'),
            ('cross', 'phys', src, 300, 'seed.html'),
            ('physbase', 'phys', base, 260, 'app.html'),
            ('biobase', 'bio', base, 260, 'app.html'),
            ('earthbase', 'earth', base, 260, 'app.html')]:
        if only and mode not in only:
            continue
        r = run(mode, subj, txt_, secs, start)
        grab(mode, r)
        if mode in ('biobase', 'earthbase'):
            continue
        tag = {'phys': '물리', 'bio': '생물', 'earth': '지학',
               'phys404': '물리·목록404', 'cross': '물리·바탕왕복', 'physbase': '바탕(헛잣대)'}[mode]
        if mode == 'phys404':
            got = [x for x in r if 'CL-5' in x]
            nop = sum(1 for x in got if x.startswith('PASS') and '단추가 선다' in x)
            lines.append(('PASS' if nop == 0 else 'FAIL')
                         + ' | CL-5 ★index.json 을 404 로 만든 판에서는 모션 단추가 0이다')
            err = [x for x in r if x.startswith('FAIL') and '콘솔 오류' in x]
            lines.append(('PASS' if not err else 'FAIL')
                         + ' | CL-5 index.json 404 판에서도 콘솔 오류가 0이다'
                         + ('' if not err else ' | ' + err[0][:200]))
            lines.append('NOTE | CL-5 404 판 CL-5 줄 | '
                         + json.dumps([x[:110] for x in got], ensure_ascii=False))
            continue
        if mode == 'physbase':
            for pre, ko in (('CL-1', '화면 글자'), ('CL-5', '모션')):
                d = [x for x in r if pre in x]
                np_ = sum(1 for x in d if x.startswith('PASS'))
                nf = sum(1 for x in d if x.startswith('FAIL'))
                lines.append(('PASS' if (np_ == 0 and nf > 0) else 'FAIL')
                             + ' | CL-0 헛잣대 — 바탕 판에서 %s(%s) 묶음이 하나도 안 통과한다' % (pre, ko)
                             + ('' if (np_ == 0 and nf > 0) else ' | ' + json.dumps([np_, nf])))
            continue
        lines += [x.replace('| CL', '| [%s] CL' % tag, 1) for x in r]

    # ── 카드 층(생물·지학) 태그·✓ 는 바탕과 **같아야** 한다(글자만 달라진다) ──
    # ★ A-6(a) 9/30 _task_qa_baseline — claude_slot_add1(genie 007fde4 · 결정로그 9/22 02:36 · _task_jagwa_claude_slot_add1.md §A-3 ✓ 따라오기 · §A-5 목록 줄 보라 태그
    #   5308 `PH&&` 걷음)부터 카드 층도 물리처럼 글 넣은 줄에 보라 「Claude」 태그 하나 · 단추 「Claude ✓」 가 선다(바탕 0c19a60 은 태그 0 · 「GPT」) — 새 기대로
    for sub, ko in (('bio', '생물'), ('earth', '지학')):
        a, b = meas.get(sub), meas.get(sub + 'base')
        if a is None or b is None:
            continue
        okt = a['tags'] == ['Claude'] and b['tags'] == []
        lines.append(('PASS' if okt else 'FAIL')
                     + ' | CL-1 [%s] 목록 보라 태그 = 글 넣은 줄 「Claude」 하나(add1 §A-5 · 바탕 0개)' % ko
                     + ('' if okt else ' | ' + json.dumps([a['tags'], b['tags']], ensure_ascii=False)))
        ok = (b['btn'] == 'GPT' and a['btn'] == 'Claude ✓')
        lines.append(('PASS' if ok else 'FAIL')
                     + ' | CL-1 [%s] 툴바 단추 = 바탕 「GPT」 자리에 「Claude ✓」(add1 §A-3 ✓ 따라옴 · 바탕은 ✓ 없음)' % ko
                     + ('' if ok else ' | ' + json.dumps([b['btn'], a['btn']], ensure_ascii=False)))
    # ── SYNC_KEYS **실행값**이 세 과목 다 바탕과 같은 배열인가(§B-2) ──
    for sub, ko in (('phys', '물리'), ('bio', '생물'), ('earth', '지학')):
        a, b = keyset.get(sub), keyset.get(sub + 'base')
        if a is None or b is None:
            lines.append('FAIL | CL-2 [%s] SYNC_KEYS 실행값을 못 받았다' % ko
                         + ' | ' + json.dumps([a, b], ensure_ascii=False))
            continue
        # ★ 합치기 10/1(하위 에이전트 C) — physphone A-2(97883ef 본문 「물리 SYNC 키 tfix 하나 더함」) — 물리만 바탕 배열 끝에 tfix 하나를 받는다(생물·지학은 글자까지 같아야)
        same = a == b or (sub == 'phys' and a == b + ['tfix'])
        lines.append(('PASS' if same else 'FAIL')
                     + ' | CL-2 [%s] ★SYNC_KEYS 실행값이 바탕과 글자까지 같다(%d칸)' % (ko, len(b))
                     + ('' if same else ' | ' + json.dumps([a, b], ensure_ascii=False)))

    pb = meas.get('physbase')
    if pb:
        lines.append(('PASS' if pb['btn'] == 'GPT ✓' else 'FAIL')
                     + ' | CL-0 헛잣대 — 바탕 물리 단추는 「GPT ✓」 였다'
                     + ('' if pb['btn'] == 'GPT ✓' else ' | ' + json.dumps(pb['btn'], ensure_ascii=False)))
        lines.append(('PASS' if pb['tags'] and all(t == 'GPT' for t in pb['tags']) else 'FAIL')
                     + ' | CL-0 헛잣대 — 바탕 물리 목록 태그는 「GPT」 였다'
                     + ('' if pb['tags'] else ' | ' + json.dumps(pb['tags'], ensure_ascii=False)))

    lines += static_checks()
    npass = sum(1 for x in lines if x.startswith('PASS'))
    nfail = sum(1 for x in lines if x.startswith('FAIL'))
    nnote = sum(1 for x in lines if x.startswith('NOTE'))
    for x in lines:
        print(x)
    print('\n== 묶음 CL  %d PASS / %d FAIL / %d NOTE / %d항 ==' % (npass, nfail, nnote, len(lines)))
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
