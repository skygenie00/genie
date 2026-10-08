# -*- coding: utf-8 -*-
"""tt앱 — 클로드 탭 3분할 · 포스트잇 이동/크기/스크롤/팝업 · 일간 발치 두 줄 · 머리줄 잔액 검산
   (_task_tt_share_claudetab_add1 §G G1~G7).

앱 사본에 날짜 고정(2026-09-16 12:00 KST) + 시드(share.json = 앱 2 · 글 4 · 세션 두 사람 · 스냅샷 ⚡2) + 검사를 넣고
헤드리스 크롬 --dump-dom 으로 <pre id="A1H"> 결과 줄을 받는다. 網은 fetch 통째 거절 · confirm 은 참.
폭 700 한 기둥은 같은 CSS 를 700px iframe 에 넣어 computed 로 잰다(창은 500 밑으로 못 줄인다).

쓰기 : python _harness_tt_claudetab_add1.py [--src 앱.html] [--out 폴더]
  --src 를 옛 판(claudetab 본판 사본)으로 주면 헛잣대 — G1~G7 이 거짓이어야 한다.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
# --mode gate|regress|smoke (_task_qa_slim2 2026-10-08 · 인자 없으면 gate = 이 판 앞과 같음)
#   regress = 칸 35 = 회귀 32 · 기준 1(SRC 함수) · 관문만 2(SRC pvTabHTML · shareCmAdd 줄 수) — 띄움 한 번 · 시드 · 검사 글은 gate 와 같다 · --out 기본만 %TEMP%\h_tt_ct_add1(gate = 하네스 옆 N: h_ct_add1)
#             SRC 무변 대조: git show <--ref> 0 · 「손대지 않는 함수」 = 함수 글자 md5 를 바탕 스냅샷(QC.base)과 · 「pvTabHTML 잔액 칸 한 줄」 · 「shareCmAdd 두 줄」 = gate 만
#   smoke   = smoke 칸 없음 → 앱을 안 띄우고 「INFO | smoke 칸 없음」 한 줄
#   N:(마이박스) 크롬 프로필을 TEMP 로 옮기는 까닭 — N: 프로필은 띄움마다 느리다: 9/17 tt 회귀(N: 결과 파일 시각) _harness_timetable 76 초 · tt_race 판마다 76~92 초 /
#     10/6 use_count N: 프로필 --dump-dom 180 초 초과 되풀이 → 사용자 「해」로 TEMP(결정로그 10/6 21:36 · 22:0x) / 프로필이 TEMP 인 민법 dump-dom 하네스는 띄움당 9~14 초
#     · 마이박스가 하네스 프로필 폴더 목록을 못 펼쳐 _qa_sync copy 10 분 멈춤 · 실행기 열쇠 셈 멈춤(결정로그 10/2 · 10/4)
import _qa_common as QC   # noqa: E402 — _task_qa_slim2(10/8) A-1 · 실행 모드 --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같음) · import 때 --mode · --snap-in · --snap-out 을 sys.argv 에서 뗀다
import argparse, html as HT, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

if QC.REGRESS:   # regress · smoke — 결과 html · 크롬 프로필(OUT\prof)의 기본 자리를 N:(마이박스) 밖 로컬 임시 폴더로(A-2 · 까닭 = 머리 주석) · --out 을 주면 그 자리 · gate 는 이 판 앞 그대로
    import tempfile as _rg_tf
    _RG_OUT = os.path.join(_rg_tf.gettempdir(), 'h_tt_ct_add1')
ap = argparse.ArgumentParser()
ap.add_argument('--src', default=_roots.genie(r"timetable\index.html"))
ap.add_argument('--out', default=_RG_OUT if QC.REGRESS else os.path.join(os.path.dirname(os.path.abspath(__file__)), "h_ct_add1"))
ap.add_argument('--ref', default='9b89e12', help='무변 대조 기준 커밋(add1 직전 = claudetab 본판)')
A = ap.parse_args()
SRC, OUT = os.path.abspath(A.src), os.path.abspath(A.out)
GENIE = _roots.genie()
os.makedirs(OUT, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ANCHOR = "<script>\n/* ============================================================\n   타임테이블 v1"

PIN = ("<script>(function(){const R=Date;let OFF=new R('2026-09-16T12:00:00+09:00').getTime()-R.now();"
       "function D(...a){return a.length?new R(...a):new R(R.now()+OFF)}D.prototype=R.prototype;"
       "D.now=()=>R.now()+OFF;D.parse=R.parse;D.UTC=R.UTC;window.Date=D;window.__adv=ms=>{OFF+=ms};"
       "window.__errs=[];addEventListener('error',e=>__errs.push(String(e.message)+' @'+(e.lineno||'')));"
       "window.fetch=()=>Promise.reject(new Error('harness: network blocked'));})();</script>")

ME, OT = '꼬까', '햄찌'
LONG = '\n'.join('긴 글 %d 줄 — 포스트잇 안에서 스크롤이 되는지 본다' % i for i in range(1, 41))


def snap(total, pv='', pd=0):
    return {'at': 1, 'u': 1, 'total': total, 'memo': '', 'pv': pv, 'pd': pd, 'ss': [], 'it': []}


SEED_FILES = {
    'tt.f.share/share.json': {'v': 1, 'items': [
        {'id': 'a1', 'ty': 'app', 't': 'tt앱', 'by': ME, 'at': 1000, 'u': 1000, 'del': False},
        {'id': 'a2', 'ty': 'app', 't': '민법앱', 'by': ME, 'at': 1001, 'u': 1001, 'del': False},
        {'id': 'P1', 'ty': 'ai', 't': LONG, 'apps': ['a1'], 'pin': 1, 'done': 0, 'by': ME, 'at': 3000, 'u': 3000, 'del': False, 'cm': [],
         'pos': {'x': 20, 'y': 20, 'w': 190, 'h': 130}},
        {'id': 'P2', 'ty': 'ai', 't': '완료된 핀 글', 'apps': ['a1'], 'pin': 1, 'done': 1, 'dt': 1789500000000, 'by': ME, 'at': 2900, 'u': 2900,
         'del': False, 'cm': [], 'pos': {'x': 230, 'y': 20, 'w': 180, 'h': 100}},
        {'id': 'P3', 'ty': 'ai', 't': '핀 없는 글', 'apps': ['a1'], 'pin': 0, 'done': 0, 'by': ME, 'at': 2800, 'u': 2800, 'del': False, 'cm': []},
        {'id': 'P4', 'ty': 'ai', 't': '다른 앱 핀 글', 'apps': ['a2'], 'pin': 1, 'done': 0, 'by': OT, 'at': 2700, 'u': 2700, 'del': False, 'cm': []},
        {'id': 't1', 'ty': 'txt', 'text': '글 하나', 'by': ME, 'at': 900, 'u': 900, 'del': False},
    ]},
    # G6 — 나(꼬까) 어제 340분 = 05:40 · 상대(햄찌) 어제 255분 = 04:15 · 오늘 80분 = 01:20
    'tt.f.sessions/%s/2026-09.json' % ME: {'v': 1, 'sessions': [{'id': 'm1', 'd': '2026-09-15', 's': '민법', 'a': 600, 'b': 940, 'u': 1}]},
    'tt.f.sessions/%s/2026-09.json' % OT: {'v': 1, 'sessions': [{'id': 'o1', 'd': '2026-09-15', 's': '민법', 'a': 600, 'b': 855, 'u': 1},
                                                                {'id': 'o2', 'd': '2026-09-16', 's': '물리', 'a': 600, 'b': 680, 'u': 1}]},
    # G7 — 꼬까 ⚡2 미수행 · 햄찌 칩 없음
    'tt.f.snaps/%s/2026-09.json' % ME: {'v': 1, 'days': {'2026-09-13': snap(100, 'pen'), '2026-09-14': snap(90, 'pen')}, 'weeks': {}, 'months': {}},
    'tt.f.snaps/%s/2026-09.json' % OT: {'v': 1, 'days': {}, 'weeks': {}, 'months': {}},
}
SEED = ("<script>localStorage.clear();"
        "localStorage.setItem('tt.cfg',JSON.stringify({person:%s,token:'',lastSync:0}));"
        "window.__SEED=%s;"
        "Object.keys(__SEED).forEach(k=>localStorage.setItem(k,JSON.stringify({data:__SEED[k],sha:null,dirty:false})));"
        "</script>") % (json.dumps(ME), json.dumps(SEED_FILES))

TESTS = r"""<script>
(function(){
const R=[];
const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+((i!==undefined&&!c)?' | '+String(i):''));
const I=(n,v)=>R.push('INFO | '+n+' | '+String(v));
const G=(name,fn)=>{try{fn()}catch(e){T(name+' 예외 — 이 게이트의 뒷줄은 못 잼',false,String(e&&e.message)+' @ '+String((e&&e.stack)||'').split('\n').slice(1,2).join(''))}};
const ME=__ME__,OT=__OT__;
const rd=k=>{try{return JSON.parse(localStorage.getItem(k)||'null')}catch(e){return null}};
const shareRaw=()=>rd('tt.f.share/share.json');
const post=id=>((shareRaw()||{data:{items:[]}}).data.items||[]).find(x=>x.id===id)||null;
const closeAll=()=>document.querySelectorAll('.modal').forEach(m=>m.remove());
const txt=el=>el?el.textContent.replace(/\s+/g,' ').trim():'';
const nrm=el=>el?el.textContent.replace(/\s+/g,''):'';
const openShare=tab=>{ui.view='share';ui.shareTab=tab;render();return document.getElementById('main')};
const reseed=()=>{closeAll();
 Object.keys(__SEED).forEach(k=>localStorage.setItem(k,JSON.stringify({data:JSON.parse(JSON.stringify(__SEED[k])),sha:null,dirty:false})));
 aiDraft='';aiSel=[];aiPin=0;aiNewOn=0;aiOpenSet={};aiEditSel=[];shCmOpen={};aiPopId=null;
 ui.aiApp='all';delete ui.aiPop;LS.set('tt.ui',ui);__adv(60000)};
const pev=(el,type,x,y)=>{const e=new PointerEvent(type,{bubbles:true,cancelable:true,pointerId:1,pointerType:'mouse',button:0,buttons:type==='pointerup'?0:1,clientX:x,clientY:y});el.dispatchEvent(e);return e};
const drag=(el,fromEl,dx,dy,steps)=>{const r=(fromEl||el).getBoundingClientRect();const x=r.left+4,y=r.top+4;
 pev(fromEl||el,'pointerdown',x,y);pev(el,'pointermove',x+dx,y+dy);pev(el,'pointerup',x+dx,y+dy)};
window.confirm=()=>true;

/* G1 3분할 */
G('G1',()=>{reseed();
 const m=openShare('ai');
 const sp=m.querySelector('.aisplit'),lf=sp&&sp.querySelector(':scope > .aileft'),rt=sp&&sp.querySelector(':scope > .airight');
 const boxes=rt?rt.querySelectorAll(':scope > .aibox'):[];
 I('G1 3분할 뼈대',(sp?'aisplit ':'')+(lf?'aileft ':'')+(rt?'airight ':'')+'aibox='+boxes.length+' · cols='+(sp?getComputedStyle(sp).gridTemplateColumns:'-'));
 T('G1 .aisplit > .aileft + .airight(.aibox 둘) · 넓은 창에서 두 기둥',!!sp&&!!lf&&boxes.length===2&&getComputedStyle(sp).gridTemplateColumns.split(' ').length===2,
   (sp?getComputedStyle(sp).gridTemplateColumns:'-')+' · aibox='+boxes.length);
 T('G1 보기 알약(진행중/📌/보관함) 없음 · 앱 거르개 줄은 하나',m.querySelectorAll('.aipill').length===0&&m.querySelectorAll('.aisub').length===1&&txt(m).indexOf('📌 포스트잇')>0,
   'aipill='+m.querySelectorAll('.aipill').length+' aisub='+m.querySelectorAll('.aisub').length);
 T('G1 왼쪽 = 포스트잇 판 · 오른쪽 위 = 쓰기 칸 + 글 · 오른쪽 아래 = 보관함',!!lf.querySelector('.aiboard')&&!!boxes[0].querySelector('.aicomp')&&!!boxes[1].querySelector('.aiarc'),
   (lf.querySelector('.aiboard')?'board ':'')+(boxes[0]&&boxes[0].querySelector('.aicomp')?'comp ':'')+(boxes[1]&&boxes[1].querySelector('.aiarc')?'arc':''));
 /* 폭 700 = 한 기둥 — 같은 CSS 를 700px iframe 에 넣어 잰다 */
 const css=[...document.querySelectorAll('style')].map(s=>s.textContent).join('\n');
 const f=document.createElement('iframe');f.style.cssText='width:700px;height:400px;border:0';document.body.appendChild(f);
 const doc=f.contentDocument;doc.open();doc.write('<!doctype html><meta charset="utf-8"><style>'+css+'</style><body>'+aiTabHTML()+'</body>');doc.close();
 const sp2=doc.querySelector('.aisplit'),c2=sp2?getComputedStyle(sp2).gridTemplateColumns:'';
 I('G1 폭 700 grid-template-columns',c2);
 T('G1 폭 700 이하 = 한 기둥',!!sp2&&c2.split(' ').length===1,c2);
 f.remove();
});

/* G2 포스트잇 대상 */
G('G2',()=>{reseed();
 const m=openShare('ai');
 const ids=[...m.querySelectorAll('.aipi')].map(e=>e.id);
 I('G2 판 위 포스트잇',ids.join(','));
 T('G2 pin:1 은 완료된 글도 붙는다(P1·P2·P4) · pin:0(P3) 은 없다',ids.length===3&&ids.indexOf('aipi-P1')>=0&&ids.indexOf('aipi-P2')>=0&&ids.indexOf('aipi-P4')>=0,ids.join(','));
 const p2=m.querySelector('#aipi-P2');
 T('G2 완료된 글 = 회색 종이(.done) · 오른쪽 아래 「✓ MM/DD HH:MM」',!!p2&&p2.classList.contains('done')&&txt(p2.querySelector('.off')).indexOf('✓')===0&&getComputedStyle(p2).backgroundColor==='rgb(236, 236, 236)',
   (p2?p2.className+' | '+txt(p2.querySelector('.off'))+' | '+getComputedStyle(p2).backgroundColor:'없음'));
 ui.aiApp='a1';const m2=openShare('ai');
 const ids2=[...m2.querySelectorAll('.aipi')].map(e=>e.id);
 T('G2 앱 거르개가 판에도 먹는다(a1 = P1·P2 만)',ids2.length===2&&ids2.indexOf('aipi-P4')<0,ids2.join(','));
 ui.aiApp='all';
});

/* G3 이동·크기 */
G('G3',()=>{reseed();
 let m=openShare('ai');
 let el=m.querySelector('#aipi-P1');
 const p0=post('P1').pos,u0=post('P1').u;
 drag(el,null,60,40);
 const p1=post('P1').pos,u1=post('P1').u;
 I('G3 끌기 뒤 pos',JSON.stringify({p0,p1}));
 T('G3 (20,20) → +60/+40 끌면 pos.x/y 가 그만큼 움직여 저장 · u 갱신 · 크기 무변',!!p1&&p1.x===p0.x+60&&p1.y===p0.y+40&&p1.w===p0.w&&p1.h===p0.h&&u1>u0,JSON.stringify(p1));
 m=openShare('ai');el=m.querySelector('#aipi-P1');
 drag(el,el.querySelector('.rz'),40,30);
 const p2=post('P1').pos;
 T('G3 오른쪽 아래 손잡이로 크기 — w/h 만 는다',!!p2&&p2.w===p1.w+40&&p2.h===p1.h+30&&p2.x===p1.x&&p2.y===p1.y,JSON.stringify(p2));
 m=openShare('ai');el=m.querySelector('#aipi-P1');
 drag(el,el.querySelector('.rz'),-500,-500);
 const p3=post('P1').pos;
 T('G3 최소 120×80 밑으로 안 간다',!!p3&&p3.w===120&&p3.h===80,JSON.stringify(p3));
 m=openShare('ai');el=m.querySelector('#aipi-P1');
 const before=JSON.stringify(post('P1').pos);
 drag(el,null,4,0);
 T('G3 4px 끌기는 클릭 = 팝업이 열리고 자리는 안 바뀐다',!!document.getElementById('aiPop')&&JSON.stringify(post('P1').pos)===before,
   JSON.stringify(post('P1').pos)+' pop='+!!document.getElementById('aiPop'));
 closeAll();
});

/* G4 종이 안 스크롤 */
G('G4',()=>{reseed();
 const m=openShare('ai');
 const el=m.querySelector('#aipi-P1'),sc=el.querySelector('.sc');
 I('G4 .sc scrollHeight/clientHeight',sc.scrollHeight+'/'+sc.clientHeight);
 T('G4 긴 글은 종이 안에서 스크롤된다(scrollHeight > clientHeight) · touch-action pan-y',sc.scrollHeight>sc.clientHeight&&getComputedStyle(sc).touchAction==='pan-y',
   sc.scrollHeight+'/'+sc.clientHeight+' · '+getComputedStyle(sc).touchAction);
 const before=JSON.stringify(post('P1').pos);
 const r=sc.getBoundingClientRect();
 pev(sc,'pointerdown',r.left+20,r.top+20);pev(el,'pointermove',r.left+90,r.top+70);pev(el,'pointerup',r.left+90,r.top+70);
 T('G4 글 위에서 끌어도 자리는 안 바뀐다(스크롤이지 이동이 아니다) · 팝업도 안 열린다',JSON.stringify(post('P1').pos)===before&&!document.getElementById('aiPop'),
   JSON.stringify(post('P1').pos));
 closeAll();
});

/* G5 팝업 */
G('G5',()=>{reseed();
 let m=openShare('ai');
 const el=m.querySelector('#aipi-P1');
 drag(el,null,2,2);
 const pop=document.getElementById('aiPop');
 I('G5 팝업 제목줄',txt(pop&&pop.querySelector('.bar')));
 T('G5 클릭 → 창 하나 · 제목줄(앱 칩·글쓴이·📌·수정·완료·×) · 본문 · 댓글 칸',document.querySelectorAll('.aipop').length===1&&!!pop.querySelector('.bar .aiapp')&&txt(pop.querySelector('.bar')).indexOf('수정')>0&&!!pop.querySelector('.bd')&&!!pop.querySelector('#aiPopIn'),
   txt(pop&&pop.querySelector('.bar')));
 const g0=JSON.stringify(ui.aiPop||null),f0=localStorage.getItem('tt.f.share/share.json');
 const bar=pop.querySelector('.bar'),r=bar.getBoundingClientRect();
 pev(bar,'pointerdown',r.left+40,r.top+6);pev(pop,'pointermove',r.left+40+35,r.top+6+25);pev(pop,'pointerup',r.left+40+35,r.top+6+25);
 const g1=ui.aiPop;
 I('G5 팝업 자리',g0+' → '+JSON.stringify(g1));
 T('G5 제목줄을 끌면 ui.aiPop 에 자리가 남는다(기기별) · 공용 파일은 무변',!!g1&&typeof g1.x==='number'&&g0!==JSON.stringify(g1)&&localStorage.getItem('tt.f.share/share.json')===f0,
   JSON.stringify(g1));
 const w0=pop.getBoundingClientRect().width;
 const rz=pop.querySelector('.rz'),rr=rz.getBoundingClientRect();
 pev(rz,'pointerdown',rr.left+4,rr.top+4);pev(pop,'pointermove',rr.left+4+40,rr.top+4+30);pev(pop,'pointerup',rr.left+4+40,rr.top+4+30);
 T('G5 손잡이로 창 크기 · ui.aiPop.w 가 는다',ui.aiPop.w>=Math.round(w0)+35,'w '+w0+' → '+ui.aiPop.w);
 const inp=document.getElementById('aiPopIn');inp.value='팝업에서 단 댓글';__adv(1000);
 [...pop.querySelectorAll('button')].find(b=>txt(b)==='달기').click();
 const cm=(post('P1').cm||[]).filter(c=>!c.del);
 T('G5 팝업에서 댓글 — 본판과 같은 cm 꼴 {id,by,t,at,u,del} · 팝업은 열린 채 다시 그린다',cm.length===1&&cm[0].by===ME&&cm[0].t==='팝업에서 단 댓글'&&!!cm[0].at&&!!cm[0].u&&cm[0].del===false&&!!document.getElementById('aiPop')&&txt(document.getElementById('aiPop')).indexOf('팝업에서 단 댓글')>0,
   JSON.stringify(cm));
 document.querySelector('#aiPop .bar .x').click();
 T('G5 × 로 닫힌다',!document.getElementById('aiPop')&&!document.getElementById('aiPopWrap'),'');
});

/* G6 일간 발치 두 줄 */
G('G6',()=>{reseed();
 const D='2026-09-16';
 const h=sheetHTML(ME,D,sessionsOf(ME,D));
 const two=(h.match(/<div class="ydtwo"[\s\S]*?<\/div><\/div>/)||[''])[0];
 const foot=(h.match(/<div class="foot">([\s\S]*?)<div>Total/)||[])[1]||'';
 const plain=two.replace(/<[^>]*>/g,'|').replace(/\|+/g,'|');
 I('G6 두 줄 블록',plain);
 T('G6 두 줄 — 「꼬까 어제 05:40」 / 「햄찌 어제 04:15 · 오늘 01:20」',two.indexOf('어제 <b>05:40</b>')>=0&&two.indexOf('어제 <b>04:15</b>')>=0&&two.indexOf('오늘 <b>01:20</b>')>=0&&two.split('<div>').length-1===2,plain);
 /* 보정(사용자 9/16) — 자리가 시안 ③ 대로 왼쪽 Time Table 기둥 아래인가 */
 const host=document.getElementById('a1Host')||(()=>{const e=document.createElement('div');e.id='a1Host';e.style.cssText='width:760px;background:#fff';document.body.insertBefore(e,document.body.firstChild);return e})();
 host.innerHTML=h;
 const yd=host.querySelector('.ydtwo'),ft=host.querySelector('.foot');
 T('G6 두 줄의 부모가 Time Table 기둥이다(.tt 바로 뒤) · .stc 안이 아니다',!!yd&&!yd.closest('.stc')&&!!yd.previousElementSibling&&yd.previousElementSibling.classList.contains('tt')&&!!yd.parentNode.querySelector(':scope > .hd')&&txt(yd.parentNode.querySelector(':scope > .hd'))==='Time Table',
   (yd?('prev='+(yd.previousElementSibling&&yd.previousElementSibling.className)+' · stc안='+!!yd.closest('.stc')+' · 기둥머리='+txt(yd.parentNode.querySelector(':scope > .hd'))):'.ydtwo 없음'));
 T('G6 .foot 에는 「어제」 글자가 없다(Start/Stop/Total 만)',!!ft&&txt(ft).indexOf('어제')<0&&txt(ft).indexOf('Start')>=0&&txt(ft).indexOf('Total')>=0,txt(ft));
 const css=[...document.querySelectorAll('style')].map(s=>s.textContent).join('\n');
 const fr=document.createElement('iframe');fr.style.cssText='width:390px;height:700px;border:0';document.body.appendChild(fr);
 const doc=fr.contentDocument;doc.open();doc.write('<!doctype html><meta charset="utf-8"><style>'+css+'</style><body>'+h+'</body>');doc.close();
 const lns=[...doc.querySelectorAll('.ydtwo > div')];
 I('G6 폭 390 줄 너비(scrollWidth/clientWidth)',lns.map(e=>e.scrollWidth+'/'+e.clientWidth).join(' · '));
 T('G6 폭 390 에서 두 줄이 안 꺾인다(각 줄 scrollWidth ≤ clientWidth)',lns.length===2&&lns.every(e=>e.scrollWidth<=e.clientWidth),lns.map(e=>e.scrollWidth+'/'+e.clientWidth).join(' · '));
 fr.remove();
 T('G6 Total 은 옛 판과 같은 셈(오늘 내 세션 0 = 00:00)',h.indexOf('class="big"')>0&&h.indexOf('>00:00</span>')>0,(h.match(/class="big"[^>]*>([^<]*)</)||[])[1]);
 const hw=sheetHTML(ME,D,sessionsOf(ME,D),{axis:'week'});
 T('G6 주 축에는 안 붙는다(옛 규칙 그대로)',hw.indexOf('ydtot')<0,'');
 localStorage.removeItem('tt.f.sessions/'+OT+'/2026-09.json');
 const h2=sheetHTML(ME,D,sessionsOf(ME,D));
 T('G6 상대 세션 파일이 아직 없으면 --:-- (0 으로 속이지 않는다)',h2.indexOf('어제 <b>--:--</b>')>=0&&h2.indexOf('오늘 <b>--:--</b>')>=0&&h2.indexOf('어제 <b>05:40</b>')>=0,
   (h2.match(/<div class="ydtwo"[\s\S]*?<\/div><\/div>/)||[''])[0].replace(/<[^>]*>/g,'|'));
});

/* G7 일간 머리줄 잔액 */
G('G7',()=>{reseed();
 ui.view='day';render();
 const sec=document.getElementById('sec_day'),bal=sec&&sec.querySelector('.ttsh .daybal');
 I('G7 머리줄 잔액',txt(bal));
 T('G7 일간 머리줄 오른쪽에 두 사람 잔액 — 「햄찌 ⚡0 🍀0 잔액 0 | 꼬까 ⚡2 🍀0 잔액 ⚡2」',!!bal&&nrm(bal)==='햄찌⚡0🍀0잔액0|꼬까⚡2🍀0잔액⚡2',txt(bal));
 const ones=bal?[...bal.querySelectorAll('.one')]:[];
 const m2=openShare('pv');const boxes=[...m2.querySelectorAll('.pvbal>div')];
 const boxTxt=b=>nrm(b.querySelector('.who'))+nrm(b.querySelector('.n'))+nrm(b.querySelector('.net'));
 I('G7 ⚡탭 위 칸',boxes.map(b=>txt(b)).join(' || '));
 T('G7 글자·칩이 벌칙포상 탭 위 칸과 같다(같은 함수)',ones.length===2&&boxes.length===2&&nrm(ones[0])===boxTxt(boxes[0])&&nrm(ones[1])===boxTxt(boxes[1]),
   ones.map(nrm).join(' / ')+' vs '+boxes.map(boxTxt).join(' / '));
 ui.view='day';render();
 const before=document.querySelectorAll('#sec_day .daybal').length;
 ttFold('day');
 const sec2=document.getElementById('sec_day');
 T('G7 절을 접어도 잔액은 보인다',before===1&&!!sec2&&!!sec2.querySelector('.ttsh .daybal')&&!sec2.querySelector('.ttsec .tt'),
   'folded daybal='+(sec2?!!sec2.querySelector('.ttsh .daybal'):'-'));
 ttFold('day');
 const wk=document.getElementById('sec_week'),mo=document.getElementById('sec_month');
 T('G7 주간·월간 머리줄은 옛 판 그대로(잔액 없음)',!!wk&&!wk.querySelector('.daybal')&&!!mo&&!mo.querySelector('.daybal'),'');
 const chip=bal&&bal.getAttribute('onclick')||'';
 T('G7 누르면 Share ▸ ⚡벌칙포상으로 간다',chip.indexOf("ui.shareTab='pv'")>=0&&chip.indexOf("setView('share')")>=0,chip.slice(0,80));
});

T('X 검사 내내 스크립트 오류 0(window error) — 무변 잣대',__errs.length===0,__errs.join(' / '));
const pre=document.createElement('pre');pre.id='A1H';pre.textContent='\n'+R.join('\n')+'\n';document.body.appendChild(pre);
})();
</script>"""


def fn_text(t, sig):
    Lx = t.split('\n')
    h = [i for i, s in enumerate(Lx) if sig in s]
    if len(h) != 1:
        return None
    i = h[0]
    if Lx[i].rstrip().endswith('}') and Lx[i].count('{') == Lx[i].count('}'):
        return Lx[i]
    depth, out = 0, []
    for k in range(i, len(Lx)):
        out.append(Lx[k])
        depth += Lx[k].count('{') - Lx[k].count('}')
        if depth <= 0 and k > i:
            break
    return '\n'.join(out)


def _rg_fn_bad(src, names, tag='SRC.fn'):
    """regress — 「손대지 않는 함수 N개 = --ref 글자」(처리표 기준)의 regress 갈래: --ref 고정 옛 커밋을 git show 로 풀지 않고
    함수마다 글자 md5 를 바탕 스냅샷(QC.base · 칸 'SRC.fn|<함수 머리>')과 맞댄다. 못 찾은 함수(fn_text = None)는 gate 처럼 바뀐 것으로 센다(_harness_tt_claudetab_add1.py)"""
    import hashlib
    bad = []
    for n in names:
        t = fn_text(src, n)
        ok = QC.same('%s|%s' % (tag, n), None if t is None else hashlib.md5(t.encode('utf-8')).hexdigest())
        if t is None or not ok:
            bad.append(n)
    return bad


def _rg_note(names, tag='SRC.fn'):
    """기준 값이 어디서 왔나(QC.base_note) — 함수마다 같은 스냅샷이라 한 줄로 모은다"""
    return ' / '.join(sorted({QC.base_note('%s|%s' % (tag, n)) for n in names}))


def main():
    if QC.SMOKE:   # smoke — 이 하네스엔 smoke 칸이 없다(처리표 칸 35 · smoke 0) — 앱을 띄우기 전에 끝
        print('INFO | smoke 칸 없음')
        return 0
    src = open(SRC, encoding='utf-8').read()
    assert ANCHOR in src, 'seed anchor not found'
    h = src.replace(ANCHOR, PIN + SEED + ANCHOR, 1)
    tests = TESTS.replace('__ME__', json.dumps(ME)).replace('__OT__', json.dumps(OT))
    h = h.replace('</body>', tests + '</body>', 1)
    app = os.path.join(OUT, 'app.html')
    open(app, 'w', encoding='utf-8', newline='\n').write(h)
    QC.launch('new')   # §B-4 셈 — 새 판 앱 띄움 1(바탕 띄움 없음 · --ref 는 글자 대조만)
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
                        '--user-data-dir=' + os.path.join(OUT, 'prof'),
                        '--allow-file-access-from-files', '--window-size=1280,900',
                        '--virtual-time-budget=8000', '--dump-dom',
                        'file:///' + app.replace('\\', '/')],
                       capture_output=True, timeout=240)
    dom = r.stdout.decode('utf-8', 'replace')
    open(os.path.join(OUT, 'dom.html'), 'w', encoding='utf-8').write(dom)
    mm = re.search(r'<pre id="A1H">(.*?)</pre>', dom, re.S)
    lines = [s.strip() for s in HT.unescape(mm.group(1)).split('\n') if s.strip()] if mm else []
    if not lines:
        print('결과 줄 없음 — 부팅 사망? dom %d bytes → %s' % (len(dom), os.path.join(OUT, 'dom.html')))
        return 1
    if QC.GATE:   # gate — --ref 고정 옛 커밋(git show)과 글자 대조(이 판 앞 그대로)
        QC.sub('git:show-app')   # §B-4 셈 — 옛 커밋 앱 풀기(regress 0)
        g = subprocess.run(['git', '-C', GENIE, 'show', A.ref + ':timetable/index.html'], capture_output=True, timeout=60)
        if g.returncode == 0:
            ref = g.stdout.decode('utf-8')
            names = ['function shMd(', 'function mergeList(', 'function mergeFile(', 'function shareItems(', 'function upsertShare2(', 'function shareFile(',
                     'function shareKeep(', 'function shareCmTog(', 'function shareCmDel(', 'function shareDel(', 'function shareEdit(', 'function pvCalc(',
                     'function pvBal(', 'function pvChip(', 'function pvApply(', 'function dayCard(', 'function modal(', 'function ttRows(', 'function mbarHTML(']
            bad = [n for n in names if fn_text(src, n) is None or fn_text(src, n) != fn_text(ref, n)]
            lines.append(('PASS' if not bad else 'FAIL') + ' | SRC 손대지 않는 함수 %d개 = %s 과 글자 같음(마크다운·병합·share·⚡·일간 격자·mbar) — 무변 잣대' % (len(names), A.ref)
                         + ('' if not bad else ' | ' + ', '.join(bad)))
            a, b = fn_text(src, 'function pvTabHTML('), fn_text(ref, 'function pvTabHTML(')
            da = [x for x in (a or '').split('\n') if x not in (b or '').split('\n')]
            okp = len(da) <= 1
            lines.append(('PASS' if okp else 'FAIL') + ' | SRC pvTabHTML 은 잔액 칸 한 줄만 바뀌었다(같은 함수를 쓰게 · 글자는 무변) — 무변 잣대'
                         + ('' if okp else ' | ' + ' / '.join(x[:60] for x in da[:3])))
            c, d = fn_text(src, 'function shareCmAdd('), fn_text(ref, 'function shareCmAdd(')
            dc = [x for x in (c or '').split('\n') if x not in (d or '').split('\n')]
            okc = len(dc) == 2 and 'inputId' in (c or '') and src.count("shareCmAdd('") == ref.count("shareCmAdd('")
            lines.append(('PASS' if okc else 'FAIL') + ' | SRC shareCmAdd 는 두 줄만 다르다(입력칸 id 인자) · 옛 부르는 자리 %d 곳 그대로 — 무변 잣대'
                         % ref.count("shareCmAdd('") + ('' if okc else ' | 다른 줄 %d · 부르는 자리 %d' % (len(dc), src.count("shareCmAdd('"))))
        else:
            lines.append('INFO | SRC 무변 대조 못 함 | git show %s 실패' % A.ref)
    else:   # regress — git show 0 · 「손대지 않는 함수 N개 = --ref 글자」(처리표 기준) = 함수마다 글자 md5 를 바탕 스냅샷(QC.base)과 맞댄다 · 「pvTabHTML 잔액 칸 한 줄」 · 「shareCmAdd 두 줄」 = gate 만(인도 판 diff 셈 · 처리표 관문만)
        names = ['function shMd(', 'function mergeList(', 'function mergeFile(', 'function shareItems(', 'function upsertShare2(', 'function shareFile(',
                 'function shareKeep(', 'function shareCmTog(', 'function shareCmDel(', 'function shareDel(', 'function shareEdit(', 'function pvCalc(',
                 'function pvBal(', 'function pvChip(', 'function pvApply(', 'function dayCard(', 'function modal(', 'function ttRows(', 'function mbarHTML(']   # gate 의 names 와 같은 목록(바꾸면 둘 다)
        bad = _rg_fn_bad(src, names)
        lines.append(('PASS' if not bad else 'FAIL') + ' | SRC 손대지 않는 함수 %d개 = %s 과 글자 같음(마크다운·병합·share·⚡·일간 격자·mbar) — 무변 잣대' % (len(names), A.ref)
                     + ' | ' + (', '.join(bad) + ' · ' if bad else '') + _rg_note(names))
    for ln in lines:
        print('   ' + ln)
    f = sum(1 for ln in lines if ln.startswith('FAIL'))
    p = sum(1 for ln in lines if ln.startswith('PASS'))
    print('\n합계  PASS %d · FAIL %d  (src %s · %d B)' % (p, f, SRC, os.path.getsize(SRC)))
    return 0 if f == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
