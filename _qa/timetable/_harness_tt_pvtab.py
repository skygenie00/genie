# -*- coding: utf-8 -*-
"""tt앱 — Share ▸ ⚡벌칙포상 탭 · 카드 칩 A꼴 · 무게 = 점수 검산 (_task_tt_share_pvtab §7 G1~G8).

앱 사본에 날짜 고정(2026-09-16 12:00 KST) + 시드(꼬까·햄찌 9월 스냅샷 · share.json 에 txt·img·pv 항목) + 검사를 넣고
헤드리스 크롬 --dump-dom 으로 <pre id="PVH"> 결과 줄을 받는다. 網은 fetch 통째 거절 · confirm 은 참.
게이트마다 시드를 다시 깐다(loadF 는 부를 때마다 localStorage 를 새로 읽는다) — 화면 DOM · computed style · 저장소 값을 잰다.
가상 시계는 스크립트 도는 동안 멈추니 u·at 차례가 필요한 자리는 __adv(ms) 로 시계를 민다.

쓰기 : python _harness_tt_pvtab.py [--src 앱.html] [--out 폴더]
  --src 를 옛 판(pvtab 전 blob 사본)으로 주면 헛잣대 — G1~G8 · X1·X2 는 거짓이어야 한다(무변 잣대 몇 줄만 참).
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
# --mode gate|regress|smoke (_task_qa_slim2 2026-10-08 · 인자 없으면 gate = 이 판 앞과 같음)
#   regress = 칸 57 = 회귀 56 · 기준 1(SRC 함수) — 띄움 한 번 · 시드 · 검사 글은 gate 와 같다 · --out 기본만 %TEMP%\h_tt_pvtab(gate = 하네스 옆 N: h_pvtab)
#             SRC 무변 대조: git show <--ref> 0 · 「손대지 않는 함수」 = 함수 글자 md5 를 바탕 스냅샷(QC.base)과
#   smoke   = smoke 칸 없음 → 앱을 안 띄우고 「INFO | smoke 칸 없음」 한 줄
#   N:(마이박스) 크롬 프로필을 TEMP 로 옮기는 까닭 — N: 프로필은 띄움마다 느리다: 9/17 tt 회귀(N: 결과 파일 시각) _harness_timetable 76 초 · tt_race 판마다 76~92 초 /
#     10/6 use_count N: 프로필 --dump-dom 180 초 초과 되풀이 → 사용자 「해」로 TEMP(결정로그 10/6 21:36 · 22:0x) / 프로필이 TEMP 인 민법 dump-dom 하네스는 띄움당 9~14 초
#     · 마이박스가 하네스 프로필 폴더 목록을 못 펼쳐 _qa_sync copy 10 분 멈춤 · 실행기 열쇠 셈 멈춤(결정로그 10/2 · 10/4)
import _qa_common as QC   # noqa: E402 — _task_qa_slim2(10/8) A-1 · 실행 모드 --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같음) · import 때 --mode · --snap-in · --snap-out 을 sys.argv 에서 뗀다
import argparse, html as HT, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

if QC.REGRESS:   # regress · smoke — 결과 html · 크롬 프로필(OUT\prof)의 기본 자리를 N:(마이박스) 밖 로컬 임시 폴더로(A-2 · 까닭 = 머리 주석) · --out 을 주면 그 자리 · gate 는 이 판 앞 그대로
    import tempfile as _rg_tf
    _RG_OUT = os.path.join(_rg_tf.gettempdir(), 'h_tt_pvtab')
ap = argparse.ArgumentParser()
ap.add_argument('--src', default=_roots.genie(r"timetable\index.html"))
ap.add_argument('--out', default=_RG_OUT if QC.REGRESS else os.path.join(os.path.dirname(os.path.abspath(__file__)), "h_pvtab"))
ap.add_argument('--ref', default='e574973', help='무변 대조 기준 커밋(pvtab 직전 timetable 커밋)')
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


def snap(total, pv='', pd=0):
    return {'at': 1, 'u': 1, 'total': total, 'memo': '', 'pv': pv, 'pd': pd, 'ss': [], 'it': []}


ME, OT = '꼬까', '햄찌'
# 꼬까 = ⚡ 09/10·09/11(미수행) · 09/12(옛 pd:1 · pvi 없음) · 🍀 09/09 → ⚡3(그중 pd 1) 🍀1 = 「⚡2 🍀1 · 잔액 ⚡1」(G6)
# 햄찌 = ⚡ 09/14 · 🍀 09/15 — 남의 칩(G8)
SEED_FILES = {
    'tt.f.snaps/%s/2026-09.json' % ME: {'v': 1, 'days': {'2026-09-09': snap(620, 'rew'), '2026-09-10': snap(100, 'pen'), '2026-09-11': snap(90, 'pen'),
                                                         '2026-09-12': snap(80, 'pen', 1), '2026-09-13': snap(300)}, 'weeks': {}, 'months': {}},
    'tt.f.snaps/%s/2026-09.json' % OT: {'v': 1, 'days': {'2026-09-14': snap(50, 'pen'), '2026-09-15': snap(650, 'rew')}, 'weeks': {}, 'months': {}},
    'tt.f.share/share.json': {'v': 1, 'items': [
        {'id': 't1', 'ty': 'txt', 'text': '글 하나', 'by': ME, 'at': 1000, 'u': 1000, 'del': False},
        {'id': 'i1', 'ty': 'img', 'img': 'share/x.jpg', 'thumb': 'share/x_t.jpg', 'by': OT, 'at': 900, 'u': 900, 'del': False},
        {'id': 'pA', 'ty': 'pv', 'kind': 'pen', 'who': ME, 't': '스쿼트 50', 'w': 1, 'by': OT, 'at': 2000, 'u': 2000, 'del': False},
        {'id': 'pC', 'ty': 'pv', 'kind': 'pen', 'who': ME, 't': '청소 전체', 'w': 3, 'by': ME, 'at': 2002, 'u': 2002, 'del': False},
        {'id': 'pB', 'ty': 'pv', 'kind': 'pen', 'who': ME, 't': '설거지', 'w': 2, 'by': ME, 'at': 2001, 'u': 2001, 'del': False},
        {'id': 'rA', 'ty': 'pv', 'kind': 'rew', 'who': ME, 't': '케이크', 'w': 1, 'by': ME, 'at': 2003, 'u': 2003, 'del': False},
        {'id': 'rB', 'ty': 'pv', 'kind': 'rew', 'who': ME, 't': '영화', 'w': 2, 'by': ME, 'at': 2004, 'u': 2004, 'del': False},
        {'id': 'hA', 'ty': 'pv', 'kind': 'pen', 'who': OT, 't': '팔굽혀펴기', 'w': 1, 'by': ME, 'at': 2005, 'u': 2005, 'del': False},
    ]},
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
const ME=__ME__,OT=__OT__,M='2026-09';
const SK=w=>'tt.f.snaps/'+w+'/'+M+'.json';
const rd=k=>{try{return JSON.parse(localStorage.getItem(k)||'null')}catch(e){return null}};
const day=(w,d)=>{const f=rd(SK(w));return(f&&f.data&&f.data.days[d])||null};
const dirtyOf=w=>{const f=rd(SK(w));return !!(f&&f.dirty)};
const shareRaw=()=>rd('tt.f.share/share.json');
const pick=e=>e?{pv:e.pv,pd:e.pd,pvi:e.pvi,pvd:e.pvd,pvx:e.pvx,pvb:e.pvb}:null;
const lsAll=()=>{const ks=[];for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k.indexOf('tt.f.')===0)ks.push(k)}ks.sort();return JSON.stringify(ks.map(k=>[k,localStorage.getItem(k)]))};
const closeModals=()=>document.querySelectorAll('.modal').forEach(m=>m.remove());
const reseed=()=>{closeModals();const ks=[];for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k.indexOf('tt.f.snaps/')===0||k==='tt.f.share/share.json')ks.push(k)}
 ks.forEach(k=>localStorage.removeItem(k));
 Object.keys(__SEED).forEach(k=>localStorage.setItem(k,JSON.stringify({data:JSON.parse(JSON.stringify(__SEED[k])),sha:null,dirty:false})));__adv(60000)};
const host=document.createElement('div');host.id='pvHost';host.style.cssText='width:360px;background:#fff';document.body.insertBefore(host,document.body.firstChild);
const card=(w,d)=>{host.innerHTML=dayCard(w,d);return host.querySelector('.card .lb .pvc')};
const openShare=tab=>{ui.view='share';ui.shareTab=tab;render();return document.getElementById('main')};
const lastModal=()=>{const a=document.querySelectorAll('.modal');return a.length?a[a.length-1]:null};
const txt=el=>el?el.textContent.replace(/\s+/g,' ').trim():'';
const nrm=el=>el?el.textContent.replace(/\s+/g,''):'';
const rowOf=(main,md,cls)=>[...main.querySelectorAll('.pvdue .pvrow')].find(r=>txt(r).indexOf(md)===0&&r.querySelector('.chip.'+cls))||null;
const boxOf=(main,w)=>[...main.querySelectorAll('.pvbal>div')].find(x=>txt(x.querySelector('.who'))===w)||null;
const btnTxt=(el,t)=>el?([...el.querySelectorAll('button')].find(b=>txt(b)===t)||null):null;
window.confirm=()=>true;

/* G1 카드 칩 A꼴 — computed style · 옛 판은 20px 채움 원(헛잣대) */
G('G1',()=>{reseed();
 const sty=el=>{const s=getComputedStyle(el),r=el.getBoundingClientRect();return{br:s.borderTopLeftRadius,bg:s.backgroundColor,fs:s.fontSize,lh:s.lineHeight,col:s.color,bc:s.borderTopColor,td:s.textDecorationLine,w:Math.round(r.width),h:Math.round(r.height),tx:el.textContent,cls:el.className}};
 const WHITE='rgb(255, 255, 255)',OR='rgb(216, 67, 21)',GR='rgb(46, 125, 91)';
 const p=card(ME,'2026-09-10'),sp=p?sty(p):null;I('G1 ⚡ 칩(09/10 미수행) computed',JSON.stringify(sp));
 T('G1 ⚡ 칩 = A꼴 — 모서리 3px · 흰 바탕 · 10px · 줄높이 14px · 주황 #d84315 글자·테두리 · 글자 ⚡',!!sp&&sp.br==='3px'&&sp.bg===WHITE&&sp.fs==='10px'&&sp.lh==='14px'&&sp.col===OR&&sp.bc===OR&&sp.tx==='⚡',JSON.stringify(sp));
 const r=card(ME,'2026-09-09'),sr=r?sty(r):null,old=host.innerHTML.indexOf('🏅')>=0;I('G1 🍀 칩(09/09 미수행) computed',JSON.stringify(sr));
 T('G1 🍀 칩 = A꼴 — 초록 #2e7d5b 글자·테두리 · 흰 바탕 · 글자 🍀 · 🏅 없음',!!sr&&sr.br==='3px'&&sr.bg===WHITE&&sr.fs==='10px'&&sr.col===GR&&sr.bc===GR&&sr.tx==='🍀'&&!old,JSON.stringify(sr)+' 🏅='+old);
 const q=card(ME,'2026-09-12'),sq=q?sty(q):null;I('G1 pd 칩(09/12 옛 pd:1) computed',JSON.stringify(sq));
 T('G1 pd 칩 = 회색 취소선 — 글자 #bbb · 테두리 #ccc · line-through · 흰 바탕',!!sq&&sq.td.indexOf('line-through')>=0&&sq.col==='rgb(187, 187, 187)'&&sq.bc==='rgb(204, 204, 204)'&&sq.bg===WHITE,JSON.stringify(sq));
 T('G1 옛 20px 원이 아니다 — 모서리 50% 아님 · 20×20 아님',!!sp&&sp.br!=='50%'&&!(sp.w===20&&sp.h===20),JSON.stringify(sp));
});

/* G2 pvPick — 무게 2 = 누른 칩 + 오래된 칩 · 잔액 1 이면 무게 2 disabled */
G('G2',()=>{reseed();
 const n0=document.querySelectorAll('.modal').length;
 card(ME,'2026-09-11').click();
 const m=lastModal(),n1=document.querySelectorAll('.modal').length;
 const opts=m?[...m.querySelectorAll('.pvopt')]:[];const o=id=>opts.find(x=>x.dataset.id===id)||null;
 I('G2 팝업(09/11 ⚡ · 잔액 2)',txt(m));
 T('G2 제 ⚡ 칩 클릭 = tt 팝업 하나 · 머리 「⚡ 09/11 (금) 벌칙 — 잔액 ⚡2점」 · 제 벌칙 셋이 at 순',n1===n0+1&&opts.map(x=>x.dataset.id).join(',')==='pA,pB,pC'&&txt(m).indexOf('⚡ 09/11 (금) 벌칙 — 잔액 ⚡2점')===0,'modal '+n0+'→'+n1+' · '+opts.map(x=>x.dataset.id).join(',')+' · '+txt(m).slice(0,60));
 const A=o('pA'),B=o('pB'),C=o('pC');
 T('G2 무게 2 「설거지」 = 고를 수 있음 · 「09/10 도 같이」 · 알약 2',!!B&&!B.classList.contains('no')&&txt(B).indexOf('09/10 도 같이')>=0&&txt(B.querySelector('.pvw'))==='2',txt(B));
 T('G2 무게 3 「청소 전체」 = 회색(no · 클릭 없음) · 「⚡ 3 필요 · 지금 2」',!!C&&C.classList.contains('no')&&!C.getAttribute('onclick')&&txt(C).indexOf('⚡ 3 필요 · 지금 2')>=0,txt(C));
 T('G2 처음 켜진 칸 = 첫 가능 항목(스쿼트 50)',!!A&&A.classList.contains('on')&&!!B&&!B.classList.contains('on'),A&&A.className);
 const ok=m&&m.querySelector('#mOk'),no=m&&m.querySelector('#mNo'),offB=m?([...m.querySelectorAll('.box button')].find(b=>/와 상쇄$/.test(txt(b)))||null):null;
 T('G2 단추 = 「수행함」 · 「닫기」 · 「🍀 09/09 와 상쇄」(가장 오래된 🍀)',!!ok&&txt(ok)==='수행함'&&!!no&&txt(no)==='닫기'&&!!offB&&txt(offB)==='🍀 09/09 와 상쇄',[txt(ok),txt(no),txt(offB)].join(' / '));
 __adv(1000);if(B)B.click();if(ok)ok.click();
 const d10=day(ME,'2026-09-10'),d11=day(ME,'2026-09-11'),d12=day(ME,'2026-09-12'),d09=day(ME,'2026-09-09');
 I('G2 수행함 뒤',JSON.stringify({d10:pick(d10),d11:pick(d11)}));
 const pk=e=>!!e&&e.pd===1&&e.pvi==='pB'&&e.pvd==='2026-09-16';
 T('G2 「설거지」 수행함 → 누른 09/11 + 그보다 오래된 09/10 둘 다 pd:1 · pvi=pB · pvd=2026-09-16 · 같은 묶음표 · 팝업 닫힘',pk(d10)&&pk(d11)&&!!d11.pvb&&d11.pvb===d10.pvb&&document.querySelectorAll('.modal').length===n0,JSON.stringify([d10,d11].map(pick)));
 T('G2 묶음 밖 무변(09/12 옛 pd · 09/09 🍀) · 스냅샷 파일 dirty — 무변 잣대(옛 판 pvToggle 도 참)',!!d12&&d12.pd===1&&!d12.pvi&&!!d09&&!d09.pd&&dirtyOf(ME),JSON.stringify([d12,d09].map(pick)));
 const c11=card(ME,'2026-09-11');
 T('G2 카드 칩 = 회색(pd) · title 「설거지 · 09/16 수행」',!!c11&&c11.classList.contains('pd')&&c11.title==='설거지 · 09/16 수행',c11&&(c11.className+' | '+c11.title));
 reseed();
 const r1=pvApply('2026-09-10','pA');
 card(ME,'2026-09-11').click();
 const m2=lastModal(),B2=m2?([...m2.querySelectorAll('.pvopt')].find(x=>x.dataset.id==='pB')||null):null;
 I('G2 잔액 1 팝업',txt(m2));
 T('G2 잔액 1(09/10 을 무게 1 로 갚은 뒤) → 무게 2 「설거지」 회색 · 「⚡ 2 필요 · 지금 1」 · 머리 「잔액 ⚡1점」',r1===true&&!!B2&&B2.classList.contains('no')&&txt(B2).indexOf('⚡ 2 필요 · 지금 1')>=0&&txt(m2).indexOf('잔액 ⚡1점')>=0,'r1='+r1+' · '+txt(B2));
 closeModals();
 const s0=localStorage.getItem(SK(ME)),r2=pvApply('2026-09-11','pB');
 T('G2 잔액 1 에서 pvApply(무게 2) 를 억지로 불러도 거절 · 스냅샷 한 글자도 무변',r2===false&&localStorage.getItem(SK(ME))===s0,'r2='+r2);
 const main=openShare('pv'),sel=main.querySelector('#pvS_2026-09-11'),opB=sel?sel.querySelector('option[value="pB"]'):null;
 T('G2 탭 줄 select 도 무게 2 = disabled option · 「⚡ 2 필요 · 지금 1」',!!opB&&opB.disabled&&opB.textContent.indexOf('⚡ 2 필요 · 지금 1')>=0,opB&&(opB.textContent+' · disabled='+opB.disabled));
});

/* G3 상쇄 — ⚡09/11 ↔ 🍀09/09 · 풀기 · 「상쇄 N」 */
G('G3',()=>{reseed();
 const b0=pvBal(ME);
 card(ME,'2026-09-11').click();const m=lastModal();
 const offB=m?([...m.querySelectorAll('.box button')].find(b=>/와 상쇄$/.test(txt(b)))||null):null;
 __adv(1000);if(offB)offB.click();
 const a=day(ME,'2026-09-11'),b=day(ME,'2026-09-09'),b1=pvBal(ME);
 I('G3 상쇄 뒤',JSON.stringify({a:pick(a),b:pick(b),b0,b1}));
 T('G3 팝업 「🍀 09/09 와 상쇄」 → 09/11⚡·09/09🍀 둘 다 pd:1 · pvx = 서로의 날짜 · 항목 칸 없음 · 팝업 닫힘',!!a&&a.pd===1&&a.pvx==='2026-09-09'&&!!b&&b.pd===1&&b.pvx==='2026-09-11'&&!a.pvi&&!b.pvi&&!lastModal(),JSON.stringify([a,b].map(pick)));
 T('G3 잔액 각각 −1 (⚡ 2→1 · 🍀 1→0)',b0.pen===2&&b0.rew===1&&b1.pen===1&&b1.rew===0,JSON.stringify({b0,b1}));
 const t11=card(ME,'2026-09-11').title,t09=card(ME,'2026-09-09').title;
 T('G3 카드 title 「↔ 09/09 🍀 상쇄」 · 「↔ 09/11 ⚡ 상쇄」',t11==='↔ 09/09 🍀 상쇄'&&t09==='↔ 09/11 ⚡ 상쇄',t11+' | '+t09);
 let main=openShare('pv');const row=rowOf(main,'09/11','k'),fb=btnTxt(row,'풀기');
 T('G3 탭 줄 09/11 = 「상쇄됨 ↔ 09/09 🍀」 + 「풀기」',!!row&&txt(row).indexOf('상쇄됨 ↔ 09/09 🍀')>=0&&!!fb,txt(row));
 __adv(1000);if(fb)fb.click();
 const a2=day(ME,'2026-09-11'),b2=day(ME,'2026-09-09'),bb=pvBal(ME);
 T('G3 「풀기」 → 둘 다 원상(pd:0 · pvx 없음) · 잔액 ⚡2 🍀1',!!a2&&a2.pd===0&&!('pvx' in a2)&&!!b2&&b2.pd===0&&!('pvx' in b2)&&bb.pen===2&&bb.rew===1,JSON.stringify([a2,b2].map(pick))+' '+JSON.stringify(bb));
 main=openShare('pv');const nb=btnTxt(boxOf(main,ME),'상쇄 1');
 T('G3 제 잔액 칸 「상쇄 1」(min ⚡2·🍀1) 살아 있음',!!nb&&!nb.disabled,txt(boxOf(main,ME)));
 __adv(1000);if(nb)nb.click();
 const x10=day(ME,'2026-09-10'),x09=day(ME,'2026-09-09'),x11=day(ME,'2026-09-11');
 T('G3 「상쇄 1」 → 오래된 것끼리 09/10⚡ ↔ 09/09🍀 · 09/11 은 그대로',!!x10&&x10.pvx==='2026-09-09'&&!!x09&&x09.pvx==='2026-09-10'&&!!x11&&!x11.pd,JSON.stringify([x10,x09,x11].map(pick)));
 main=openShare('pv');const bx=boxOf(main,ME),nb0=bx?bx.querySelector('button'):null;
 T('G3 짝이 없으면(🍀 0) 「상쇄 0」 disabled',!!nb0&&txt(nb0)==='상쇄 0'&&nb0.disabled,nb0&&(txt(nb0)+' '+nb0.disabled));
});

/* G4 되돌리기 — 무게 2 묶음이 한 번에 */
G('G4',()=>{reseed();
 const clean=e=>!!e&&e.pd===0&&!('pvi' in e)&&!('pvd' in e)&&!('pvb' in e);
 const r=pvApply('2026-09-11','pB');
 const main=openShare('pv'),row=rowOf(main,'09/10','k'),ub=btnTxt(row,'되돌리기');
 T('G4 탭 줄 09/10 = 「설거지 ✓ 09/16 수행」 + 「되돌리기」',r===true&&!!row&&txt(row).indexOf('설거지 ✓ 09/16 수행')>=0&&!!ub,txt(row));
 __adv(1000);if(ub)ub.click();
 const a=day(ME,'2026-09-10'),b=day(ME,'2026-09-11');
 T('G4 한 줄 「되돌리기」 → 무게 2 로 묶인 09/10·09/11 둘 다 한 번에 pd:0 · pvi·pvd·pvb 삭제',clean(a)&&clean(b),JSON.stringify([a,b].map(pick)));
 reseed();pvApply('2026-09-11','pB');
 card(ME,'2026-09-10').click();const m=lastModal(),ok=m&&m.querySelector('#mOk');
 T('G4 회색 칩 클릭 = 「되돌리기」 팝업 · 「묶인 칩 09/10 · 09/11」',!!ok&&txt(ok)==='되돌리기'&&txt(m).indexOf('묶인 칩 09/10 · 09/11')>=0,txt(m));
 __adv(1000);if(ok)ok.click();
 const a2=day(ME,'2026-09-10'),b2=day(ME,'2026-09-11'),c2=day(ME,'2026-09-12');
 T('G4 팝업 되돌리기 → 둘 다 원상 · 09/12 옛 pd 는 그대로',clean(a2)&&clean(b2)&&!!c2&&c2.pd===1,JSON.stringify([a2,b2,c2].map(pick)));
});

/* G5 목록 — 추가·수정·삭제 · del 표식 · mergeList 최신 u 승 · txt/img 무변 */
G('G5',()=>{reseed();
 const t0=JSON.stringify(shareItems('txt')),i0=JSON.stringify(shareItems('img'));
 const add=(pi,k,name,w)=>{const main=openShare('pv'),n=main.querySelector('#pvN_'+pi+'_'+k),ww=main.querySelector('#pvW_'+pi+'_'+k);if(!n)return false;n.value=name;ww.value=String(w);n.parentNode.querySelector('button').click();return true};
 const c0=shareRaw().data.items.length;
 const e1=add(1,'pen','',2),e2=add(1,'pen','줄넘기',0);
 T('G5 이름 빈 칸 · 무게 0 은 안 받는다',e1&&e2&&shareRaw().data.items.length===c0,c0+'→'+shareRaw().data.items.length);
 __adv(1000);add(1,'pen','줄넘기',2);
 const f1=shareRaw(),it=f1.data.items.find(x=>x.ty==='pv'&&x.t==='줄넘기')||null;
 T('G5 ＋ 추가 → share.json {ty:pv · kind:pen · who:꼬까 · t · w:2 · by:꼬까 · at · u · del:false} · dirty',!!it&&it.kind==='pen'&&it.who===ME&&it.w===2&&it.by===ME&&!!it.at&&!!it.u&&it.del===false&&f1.dirty===true,JSON.stringify(it));
 let main=openShare('pv');const col=[...main.querySelectorAll('.pvcol')][1],pl=col?col.querySelectorAll('.pvlist')[0]:null;
 T('G5 꼬까 기둥 벌칙 표에 줄이 는다(스쿼트 50 · 설거지 · 청소 전체 · 줄넘기)',!!pl&&pl.querySelectorAll('.pvit').length===4&&txt(pl).indexOf('줄넘기')>=0,txt(pl));
 __adv(1000);add(0,'rew','치킨',1);
 const ih=shareRaw().data.items.find(x=>x.ty==='pv'&&x.t==='치킨')||null;
 T('G5 남의 기둥(햄찌 포상)에도 추가 · who=햄찌 · by=꼬까(저장만)',!!ih&&ih.who===OT&&ih.kind==='rew'&&ih.by===ME,JSON.stringify(ih));
 __adv(1000);const u1=it&&it.u;
 if(it)pvItemEdit(it.id);const m=lastModal();
 if(m){m.querySelector('#pvEt').value='줄넘기 500';m.querySelector('#pvEw').value='3';m.querySelector('#mOk').click();}
 const it2=it?(shareRaw().data.items.find(x=>x.id===it.id)||null):null;
 T('G5 ✎ 수정 → t·w 바뀜 · u 커짐 · by 무변',!!it2&&it2.t==='줄넘기 500'&&it2.w===3&&it2.u>u1&&it2.by===ME,JSON.stringify(it2));
 __adv(1000);if(it)pvItemDel(it.id);
 const it3=it?(shareRaw().data.items.find(x=>x.id===it.id)||null):null;
 T('G5 × 삭제 → 항목이 del 표식으로 파일에 남는다 · 목록(pvItems)에서 빠짐',!!it3&&!!it3.del&&pvItems(ME,'pen').every(x=>x.id!==it.id),JSON.stringify(it3));
 const loc=shareRaw().data,rem=JSON.parse(JSON.stringify(loc)),ri=rem.items.find(x=>x.id===it.id);ri.t='옛 이름';ri.del=false;ri.u=it3.u-5000;
 const mg1=mergeFile('share/share.json',loc,rem).items.find(x=>x.id===it.id);
 const rem2=JSON.parse(JSON.stringify(loc)),r2=rem2.items.find(x=>x.id==='pA');r2.t='원격 스쿼트';r2.u=(r2.u||0)+99999;
 const mg2=mergeFile('share/share.json',loc,rem2).items.find(x=>x.id==='pA');
 T('G5 병합(mergeFile→mergeList) = 최신 u 승 — 로컬 삭제가 옛 원격을 이기고 · 새 원격 이름이 로컬을 이긴다',!!mg1&&!!mg1.del&&mg1.t==='줄넘기 500'&&!!mg2&&mg2.t==='원격 스쿼트',JSON.stringify({mg1,mg2}));
 T('G5 shareItems(txt)·(img) 결과 무변',JSON.stringify(shareItems('txt'))===t0&&JSON.stringify(shareItems('img'))===i0,t0+' || '+i0);
});

/* G6 잔액 — ⚡3(그중 pd 1) 🍀1 → 「⚡2 🍀1 · 잔액 ⚡1」 */
G('G6',()=>{reseed();
 const main=openShare('pv'),my=boxOf(main,ME),ot=boxOf(main,OT);
 I('G6 잔액 칸',txt(my)+' || '+txt(ot));
 T('G6 꼬까(⚡3 중 pd 1 · 🍀1) → 「⚡ 2 · 🍀 1 · 잔액 ⚡1」',!!my&&nrm(my.querySelector('.n'))==='⚡2🍀1'&&nrm(my.querySelector('.net'))==='잔액⚡1',txt(my));
 T('G6 햄찌(⚡1 🍀1) → 「잔액 0」',!!ot&&nrm(ot.querySelector('.n'))==='⚡1🍀1'&&nrm(ot.querySelector('.net'))==='잔액0',txt(ot));
 const rows=[...main.querySelectorAll('.pvdue .pvrow')].map(r=>txt(r.querySelector('.d')));
 I('G6 칩 줄 차례',rows.join(' / '));
 T('G6 칩 줄 = 사람별(settings.people 차례) · 오래된 순 — 햄찌 09/14·09/15 → 꼬까 09/09·09/10·09/11·09/12',rows.length===6&&['09/14','09/15','09/09','09/10','09/11','09/12'].every((d,i)=>rows[i].indexOf(d)===0),rows.join(' / '));
});

/* G7 옛 pd:1(pvi 없음) */
G('G7',()=>{reseed();
 const c=card(ME,'2026-09-12'),s=c?getComputedStyle(c):null;
 T('G7 옛 pd:1(pvi 없음) 칩 = 회색(#bbb) · 취소선 · title 「수행함」',!!c&&c.classList.contains('pd')&&c.title==='수행함'&&s.color==='rgb(187, 187, 187)'&&s.textDecorationLine.indexOf('line-through')>=0,c&&(c.className+' | '+c.title+' | '+s.color));
 const main=openShare('pv'),row=rowOf(main,'09/12','k');
 T('G7 탭 줄 09/12 = 「수행함」 + 「되돌리기」',!!row&&txt(row.querySelector('.off'))==='수행함'&&!!btnTxt(row,'되돌리기'),txt(row));
 card(ME,'2026-09-12').click();const m=lastModal(),ok=m&&m.querySelector('#mOk');
 T('G7 옛 pd 칩 클릭 = 「되돌리기」 팝업(이 칩 하나)',!!ok&&txt(ok)==='되돌리기'&&txt(m).indexOf('이 칩이 다시 살아난다')>=0,txt(m));
 __adv(1000);if(ok)ok.click();const e=day(ME,'2026-09-12');
 T('G7 팝업 되돌리기 → 09/12 만 pd:0 · 다른 칩 무변',!!ok&&!!e&&e.pd===0&&day(ME,'2026-09-10').pd===0&&day(ME,'2026-09-09').pd===0,JSON.stringify(pick(e)));
});

/* G8 남의 칩 · 남의 잔액 칸 */
G('G8',()=>{reseed();
 const oc=card(OT,'2026-09-14'),s0=lsAll(),attr=oc?(oc.getAttribute('onclick')||''):'(칩 없음)';
 if(oc)oc.click();
 const s1=lsAll();closeModals();
 const mc=card(ME,'2026-09-11'),mattr=mc?(mc.getAttribute('onclick')||''):'';
 T('G8 남의 칩 = onclick·.on 없음 · 클릭해도 저장소(tt.f.*) 한 글자도 안 바뀜(dirty 0) — 무변 잣대',!!oc&&attr===''&&!oc.classList.contains('on')&&s0===s1,'onclick='+attr+' · 같음='+(s0===s1));
 T('G8 제 칩 = pvPick 팝업 배선(옛 pvToggle 아님)',mattr.indexOf("pvPick('2026-09-11')")>=0&&mattr.indexOf('pvToggle')<0,mattr);
 const main=openShare('pv'),my=boxOf(main,ME),ot=boxOf(main,OT);
 T('G8 남의 잔액 칸엔 「상쇄」 단추 없음 · 제 칸엔 있음',!!ot&&!ot.querySelector('button')&&!!my&&!!my.querySelector('button'),txt(ot)+' || '+txt(my));
 const orows=[...main.querySelectorAll('.pvdue .pvrow')].filter(r=>r.querySelector('.chip.h'));
 T('G8 남의 칩 줄 둘 = 단추·select 없음',orows.length===2&&orows.every(r=>!r.querySelector('button,select')),orows.map(txt).join(' / '));
 T('G8 남의 스냅샷 파일 dirty 아님 — 무변 잣대',!dirtyOf(OT),'');
});

/* X1 서브탭 넷 · 🤖 클로드 빈 탭 · Image/Text 그대로 */
G('X1',()=>{reseed();
 const tabsOf=main=>[...main.querySelectorAll('.views:not(.moretabs) span')];
 const m1=openShare('pv'),tb=tabsOf(m1),on=tb.find(x=>x.classList.contains('on'));
 T('X1 Share 서브탭 넷 = 🖼 Image · 📝 Text · ⚡ 벌칙포상 · 🤖 클로드 · ⚡ 켜짐 · ui.shareTab 저장',tb.map(x=>x.textContent).join('|')==='🖼 Image|📝 Text|⚡ 벌칙포상|🤖 클로드'&&!!on&&on.textContent==='⚡ 벌칙포상'&&!!m1.querySelector('.pvtab'),tb.map(x=>x.textContent).join('|'));
 const m2=openShare('ai');
 /* 2026-09-16 갱신 — pvtab 판에서는 「다음 판」 한 줄, 그다음 판(_task_tt_share_claudetab)에서는 제 탭(.aitab). 어느 쪽이든 ⚡·📝 마크업이 새면 안 된다 */
 T('X1 🤖 클로드 탭 = 제 것을 그린다(pvtab 판 「다음 판」 한 줄 · claudetab 판 .aitab) · ⚡·📝 마크업 아님',(m2.textContent.indexOf('🤖 클로드 — 다음 판')>=0||!!m2.querySelector('.aitab'))&&!m2.querySelector('.pvtab')&&!m2.querySelector('#shT'),txt(m2).slice(-80));
 const m3=openShare('txt');
 T('X1 📝 Text 그대로(쓰기 칸 · 갈래 칩) — 무변 잣대',!!m3.querySelector('#shT')&&!!m3.querySelector('.shcat')&&!m3.querySelector('.pvtab'),'');
 const m4=openShare('img');
 T('X1 🖼 Image 그대로(올리기 칸) — 무변 잣대',!!m4.querySelector('#shF')&&!m4.querySelector('.pvtab'),'');
 const m5=openShare('zz');
 T('X1 모르는 탭 값은 종전대로 Text 로 떨어진다 — 무변 잣대',!!m5.querySelector('#shT'),'');
 ui.shareTab='img';ui.view='day';LS.set('tt.ui',ui);render();
});

/* X2 다시 반영(takeSnap)이 pvi·pvd·pvb·pvx 를 pd 처럼 물려받는다(§2) */
G('X2',()=>{reseed();
 pvApply('2026-09-11','pB');const b=day(ME,'2026-09-11');
 __adv(1000);takeSnap('2026-09-11');const a=day(ME,'2026-09-11');
 T('X2 다시 반영 뒤에도 pd·pvi·pvd·pvb 그대로(pd 와 같은 규칙) · at 은 새로',!!a&&!!b&&a.pd===1&&a.pvi==='pB'&&a.pvd===b.pvd&&a.pvb===b.pvb&&a.at>b.at,JSON.stringify({b:pick(b),a:pick(a)}));
 reseed();pvOffset('2026-09-11','2026-09-09');__adv(1000);takeSnap('2026-09-09');const x=day(ME,'2026-09-09');
 T('X2 다시 반영 뒤에도 상쇄짝 pvx 그대로',!!x&&x.pd===1&&x.pvx==='2026-09-11',JSON.stringify(pick(x)));
});

T('X3 검사 내내 스크립트 오류 0(window error) — 무변 잣대',__errs.length===0,__errs.join(' / '));
const pre=document.createElement('pre');pre.id='PVH';pre.textContent='\n'+R.join('\n')+'\n';document.body.appendChild(pre);
})();
</script>"""


_DD = re.compile(r"draftDrop\([^()]*\);?")   # ★ 2026-10-09 tt 둘째 판(채팅 19:48 ② · 사용자 19:47) — 처리기에 더한 draftDrop(…) 부름은 함수 글자 대조에서 뺌


def fn_text(t, sig):
    Lx = _DD.sub('', t).split('\n')   # 옛 줄: Lx = t.split('\n')
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
    함수마다 글자 md5 를 바탕 스냅샷(QC.base · 칸 'SRC.fn|<함수 머리>')과 맞댄다. 못 찾은 함수(fn_text = None)는 gate 처럼 바뀐 것으로 센다(_harness_tt_pvtab.py)"""
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
    if QC.SMOKE:   # smoke — 이 하네스엔 smoke 칸이 없다(처리표 칸 57 · smoke 0) — 앱을 띄우기 전에 끝
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
    mm = re.search(r'<pre id="PVH">(.*?)</pre>', dom, re.S)
    lines = [s.strip() for s in HT.unescape(mm.group(1)).split('\n') if s.strip()] if mm else []
    if not lines:
        print('결과 줄 없음 — 부팅 사망? dom %d bytes → %s' % (len(dom), os.path.join(OUT, 'dom.html')))
        return 1
    # 소스 무변(§6) — pvtab 직전 커밋의 같은 함수와 글자 대조
    if QC.GATE:   # gate — --ref 고정 옛 커밋(git show)과 글자 대조(이 판 앞 그대로)
        QC.sub('git:show-app')   # §B-4 셈 — 옛 커밋 앱 풀기(regress 0)
        g = subprocess.run(['git', '-C', GENIE, 'show', A.ref + ':timetable/index.html'], capture_output=True, timeout=60)
        if g.returncode == 0:
            ref = g.stdout.decode('utf-8')
            # 2026-09-16 갱신 — shareCmAdd 는 claudetab add1 이 「입력칸 id」 인자를 더했다(부르는 자리는 무변). 그 한 자리는 add1 하네스가 따로 잰다
            names = ['function pvCalc(', 'function mergeList(', 'function mergeFile(', 'function shareItems(', 'function upsertShare2(', 'function shareFile(',
                     'function snapOf(', 'function snapFileF(', 'function modal(', 'function shareKeep(', 'function shareAddText(',
                     'function shareCmDel(', 'function scheduleSync(', 'function dayCard(', 'function snapView(']
            bad = [n for n in names if fn_text(src, n) is None or fn_text(src, n) != fn_text(ref, n)]
            lines.append(('PASS' if not bad else 'FAIL') + ' | SRC 손대지 않는 함수 %d개 = %s 과 글자 같음(pvCalc·병합·share 읽기쓰기·팝업·동기화·dayCard) — 무변 잣대' % (len(names), A.ref)
                         + ('' if not bad else ' | ' + ', '.join(bad)))
        else:
            lines.append('INFO | SRC 무변 대조 못 함 | git show %s 실패' % A.ref)
    else:   # regress — git show 0 · 「손대지 않는 함수 N개 = --ref 글자」(처리표 기준) = 함수마다 글자 md5 를 바탕 스냅샷(QC.base)과 맞댄다
        names = ['function pvCalc(', 'function mergeList(', 'function mergeFile(', 'function shareItems(', 'function upsertShare2(', 'function shareFile(',
                 'function snapOf(', 'function snapFileF(', 'function modal(', 'function shareKeep(', 'function shareAddText(',
                 'function shareCmDel(', 'function scheduleSync(', 'function dayCard(', 'function snapView(']   # gate 의 names 와 같은 목록(바꾸면 둘 다)
        bad = _rg_fn_bad(src, names)
        lines.append(('PASS' if not bad else 'FAIL') + ' | SRC 손대지 않는 함수 %d개 = %s 과 글자 같음(pvCalc·병합·share 읽기쓰기·팝업·동기화·dayCard) — 무변 잣대' % (len(names), A.ref)
                     + ' | ' + (', '.join(bad) + ' · ' if bad else '') + _rg_note(names))
    for ln in lines:
        print('   ' + ln)
    f = sum(1 for ln in lines if ln.startswith('FAIL'))
    p = sum(1 for ln in lines if ln.startswith('PASS'))
    print('\n합계  PASS %d · FAIL %d  (src %s · %d B)' % (p, f, SRC, os.path.getsize(SRC)))
    return 0 if f == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
