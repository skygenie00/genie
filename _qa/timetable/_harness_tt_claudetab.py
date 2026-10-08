# -*- coding: utf-8 -*-
"""tt앱 — Share ▸ 🤖 클로드 탭 검산 (_task_tt_share_claudetab §4 G1~G7).

앱 사본에 날짜 고정(2026-09-16 12:00 KST) + 시드(share.json = txt 1 · img 1 · pv 2 · app·ai 는 0건) + 검사를 넣고
헤드리스 크롬 --dump-dom 으로 <pre id="AIH"> 결과 줄을 받는다. 網은 fetch 통째 거절 · confirm 은 참.
게이트마다 시드를 다시 깔고(loadF 는 부를 때마다 localStorage 를 새로 읽는다) 화면 DOM·저장소 값을 잰다.
가상 시계는 스크립트 도는 동안 멈추니 at·u 차례가 필요한 자리는 __adv(ms) 로 민다.

쓰기 : python _harness_tt_claudetab.py [--src 앱.html] [--out 폴더]
  --src 를 옛 판(claudetab 전 = pvtab 판 사본)으로 주면 헛잣대 — G1~G6 은 거짓이어야 하고 G7(무변)만 참이다.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
# --mode gate|regress|smoke (_task_qa_slim2 2026-10-08 · 인자 없으면 gate = 이 판 앞과 같음)
#   regress = 칸 39 = 회귀 37 · 기준 1(SRC 함수) · 관문만 1(SRC shareHTML 한 줄) — 띄움 한 번 · 시드 · 검사 글은 gate 와 같다 · --out 기본만 %TEMP%\h_tt_claudetab(gate = 하네스 옆 N: h_claudetab)
#             SRC 무변 대조: git show <--ref> 0 · 「손대지 않는 함수」 = 함수 글자 md5 를 바탕 스냅샷(QC.base)과 · 「shareHTML 은 ai 갈래 한 줄만 다르다」 = gate 만
#   smoke   = smoke 칸 없음 → 앱을 안 띄우고 「INFO | smoke 칸 없음」 한 줄
#   N:(마이박스) 크롬 프로필을 TEMP 로 옮기는 까닭 — N: 프로필은 띄움마다 느리다: 9/17 tt 회귀(N: 결과 파일 시각) _harness_timetable 76 초 · tt_race 판마다 76~92 초 /
#     10/6 use_count N: 프로필 --dump-dom 180 초 초과 되풀이 → 사용자 「해」로 TEMP(결정로그 10/6 21:36 · 22:0x) / 프로필이 TEMP 인 민법 dump-dom 하네스는 띄움당 9~14 초
#     · 마이박스가 하네스 프로필 폴더 목록을 못 펼쳐 _qa_sync copy 10 분 멈춤 · 실행기 열쇠 셈 멈춤(결정로그 10/2 · 10/4)
import _qa_common as QC   # noqa: E402 — _task_qa_slim2(10/8) A-1 · 실행 모드 --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같음) · import 때 --mode · --snap-in · --snap-out 을 sys.argv 에서 뗀다
import argparse, html as HT, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

if QC.REGRESS:   # regress · smoke — 결과 html · 크롬 프로필(OUT\prof)의 기본 자리를 N:(마이박스) 밖 로컬 임시 폴더로(A-2 · 까닭 = 머리 주석) · --out 을 주면 그 자리 · gate 는 이 판 앞 그대로
    import tempfile as _rg_tf
    _RG_OUT = os.path.join(_rg_tf.gettempdir(), 'h_tt_claudetab')
ap = argparse.ArgumentParser()
ap.add_argument('--src', default=_roots.genie(r"timetable\index.html"))
ap.add_argument('--out', default=_RG_OUT if QC.REGRESS else os.path.join(os.path.dirname(os.path.abspath(__file__)), "h_claudetab"))
ap.add_argument('--ref', default='714c685', help='무변 대조 기준 커밋(claudetab 직전 = pvtab 판)')
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
SEED_FILES = {
    'tt.f.share/share.json': {'v': 1, 'items': [
        {'id': 't1', 'ty': 'txt', 'text': '글 하나 **굵게**', 'by': ME, 'at': 1000, 'u': 1000, 'del': False,
         'cm': [{'id': 'c1', 'by': OT, 't': '댓글 하나', 'at': 1100, 'u': 1100, 'del': False}]},
        {'id': 'i1', 'ty': 'img', 'img': 'share/x.jpg', 'thumb': 'share/x_t.jpg', 'by': OT, 'at': 900, 'u': 900, 'del': False},
        {'id': 'pA', 'ty': 'pv', 'kind': 'pen', 'who': ME, 't': '스쿼트 50', 'w': 1, 'by': OT, 'at': 2000, 'u': 2000, 'del': False},
        {'id': 'rA', 'ty': 'pv', 'kind': 'rew', 'who': ME, 't': '케이크', 'w': 1, 'by': ME, 'at': 2003, 'u': 2003, 'del': False},
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
const ME=__ME__,OT=__OT__;
const rd=k=>{try{return JSON.parse(localStorage.getItem(k)||'null')}catch(e){return null}};
const shareRaw=()=>rd('tt.f.share/share.json');
const items=ty=>((shareRaw()||{data:{items:[]}}).data.items||[]).filter(x=>x.ty===ty);
const closeModals=()=>document.querySelectorAll('.modal').forEach(m=>m.remove());
const txt=el=>el?el.textContent.replace(/\s+/g,' ').trim():'';
const hash=s=>{let h=5381;for(let i=0;i<s.length;i++)h=((h*33)^s.charCodeAt(i))>>>0;return h.toString(36)+'/'+s.length};
const openShare=tab=>{ui.view='share';ui.shareTab=tab;render();return document.getElementById('main')};
const lastModal=()=>{const a=document.querySelectorAll('.modal');return a.length?a[a.length-1]:null};
const btnTxt=(el,t)=>el?([...el.querySelectorAll('button')].find(b=>txt(b)===t)||null):null;
const reseed=()=>{closeModals();
 Object.keys(__SEED).forEach(k=>localStorage.setItem(k,JSON.stringify({data:JSON.parse(JSON.stringify(__SEED[k])),sha:null,dirty:false})));
 aiDraft='';aiSel=[];aiPin=0;aiNewOn=0;aiOpenSet={};aiEditSel=[];shCmOpen={};
 ui.aiView='open';ui.aiApp='all';LS.set('tt.ui',ui);__adv(60000)};
const addRaw=arr=>{const f=shareFile();arr.forEach(x=>f.data.items.push(JSON.parse(JSON.stringify(x))));f.dirty=true;saveF('share/share.json',f)};
const addApp=name=>{aiNewOpen();const el=document.getElementById('aiNew');if(el)el.value=name;aiAppAdd();__adv(1000);
 const a=items('app').filter(x=>!x.del);return a.length?a[a.length-1].id:null};
const postNow=(t,apps,pin)=>{aiDraft=t;aiSel=apps.slice();aiPin=pin?1:0;const r=aiPost();__adv(1000);
 const p=items('ai').filter(x=>!x.del);return r?p[p.length-1].id:null};
const cardOf=(main,id)=>main.querySelector('#ai-'+id);
window.confirm=()=>true;

/* G1 앱 사전 — 빈 상태 · 추가 · 중복 거부 · 글 달린 앱 삭제 거부 */
G('G1',()=>{reseed();
 let main=openShare('ai');
 const comp=main.querySelector('.aicomp'),newB=comp?comp.querySelector('.aiapp.new'):null;
 I('G1 빈 사전 쓰기 칸',txt(comp));
 T('G1 앱 사전이 비면 쓰기 칸에 「＋ 새 앱」만(코드가 다섯을 심지 않는다) · 올리기 disabled',!!comp&&!!newB&&txt(newB)==='＋ 새 앱'&&comp.querySelectorAll('.aiapp').length===1&&!!btnTxt(comp,'올리기')&&btnTxt(comp,'올리기').disabled,txt(comp));
 const id1=addApp('민법OX');
 const ap=items('app').filter(x=>!x.del);
 T('G1 「＋ 새 앱」 → ty:app 1건 {t:민법OX · by:꼬까 · at · u · del:false} · 바로 골라짐',ap.length===1&&ap[0].t==='민법OX'&&ap[0].by===ME&&!!ap[0].at&&!!ap[0].u&&ap[0].del===false&&aiSel.indexOf(id1)>=0,JSON.stringify(ap));
 addApp('민법ox');addApp(' 민법OX');
 T('G1 같은 이름 재추가 거부(대소문자·공백 무시) — 1건 그대로',items('app').filter(x=>!x.del).length===1,JSON.stringify(items('app')));
 const id2=addApp('tt');
 T('G1 다른 이름은 는다 — 2건 · 만든 차례',items('app').filter(x=>!x.del).length===2&&aiApps().map(x=>x.t).join(',')==='민법OX,tt',aiApps().map(x=>x.t).join(','));
 const pid=postNow('글 하나',[id1],0);
 const r=aiAppDel(id1);
 T('G1 글이 달린 앱은 못 지운다(aiAppDel 거절 · 앱 살아 있음)',!!pid&&r===false&&items('app').filter(x=>!x.del).length===2,'r='+r);
 const r2=aiAppDel(id2);
 T('G1 글 없는 앱은 지워진다(del 표식)',r2===true&&items('app').filter(x=>!x.del).length===1&&items('app').some(x=>x.id===id2&&x.del),JSON.stringify(items('app')));
});

/* G2 올리기 — 앱 0개 disabled · 앱 둘 · 📌 · at·by */
G('G2',()=>{reseed();
 const a1=addApp('민법OX'),a2=addApp('tt');
 aiSel=[];render();
 let main=openShare('ai');let comp=main.querySelector('.aicomp');
 T('G2 앱 0개면 「올리기」 disabled',!!btnTxt(comp,'올리기')&&btnTxt(comp,'올리기').disabled,txt(comp));
 aiSelTog(a1);aiSelTog(a2);
 main=openShare('ai');comp=main.querySelector('.aicomp');
 const ta=comp.querySelector('#aiT');ta.value='민법OX 검색 결과 팝업 · tt 동기화';ta.dispatchEvent(new Event('input'));
 const pk=comp.querySelector('#aiPk');pk.click();
 const ob=btnTxt(comp,'올리기');
 T('G2 앱 둘 고르면 칩 on · 「올리기」 살아남 · 초고는 aiDraft 에(oninput 배선)',!ob.disabled&&aiDraft.indexOf('동기화')>0&&comp.querySelectorAll('.aiapp.on').length===2&&aiPin===1,'draft='+aiDraft+' pin='+aiPin);
 __adv(1000);ob.click();
 const p=items('ai').filter(x=>!x.del);
 I('G2 올린 글',JSON.stringify(p[0]));
 T('G2 올리기 → ty:ai 1건 {apps 2개 · pin:1 · done:0 · by:꼬까 · at · u · cm:[]} · 쓰기 칸 비움',p.length===1&&(p[0].apps||[]).length===2&&p[0].apps.indexOf(a1)>=0&&p[0].apps.indexOf(a2)>=0&&p[0].pin===1&&p[0].done===0&&p[0].by===ME&&!!p[0].at&&Array.isArray(p[0].cm)&&aiDraft===''&&aiSel.length===0&&aiPin===0,JSON.stringify(p[0]));
 main=openShare('ai');const card=cardOf(main,p[0].id);
 T('G2 글 한 장 = 앱 칩 둘 · 「글쓴이 · MM/DD HH:MM」 · 📌 켜짐 · 본문 마크다운',!!card&&card.querySelectorAll('.hd .aiapp').length===2&&txt(card.querySelector('.hd .t')).indexOf(ME)===0&&card.querySelector('.hd .pin').classList.contains('on')&&!!card.querySelector('.body.md'),txt(card).slice(0,90));
});

/* G3 완료 — done·dt · 보관함 앱 두 묶음 · 되돌리기 */
G('G3',()=>{reseed();
 const a1=addApp('민법OX'),a2=addApp('tt');
 const pid=postNow('완료 시험 글',[a1,a2],0);
 let main=openShare('ai');
 const ck=cardOf(main,pid).querySelector('.ck');
 __adv(1000);ck.click();
 const x=items('ai').find(z=>z.id===pid);
 I('G3 완료 뒤',JSON.stringify({done:x.done,dt:!!x.dt}));
 T('G3 체크 → done:1 · dt 있음',!!x&&x.done===1&&!!x.dt,JSON.stringify(x&&{done:x.done,dt:x.dt}));
 main=openShare('ai');
 T('G3 (add1 갱신) 진행중 칸에서 사라지고 보관함 칸으로 간다 — 옛 「알약」 잣대는 3분할로 없어졌다',!cardOf(main,pid)&&!!main.querySelector('.aibox.arc .aiarc')&&txt(main.querySelector('.aibox.arc')).indexOf('완료 시험 글')>0,txt(main.querySelector('.aibox.arc')).slice(0,80));
 main=openShare('ai');
 const heads=[...main.querySelectorAll('.aiarc h4')].map(h=>txt(h));
 const rows=[...main.querySelectorAll('.aiarc .r')];
 const want='✓ '+shareTime(x.dt);
 I('G3 보관함',heads.join(' / ')+' || '+rows.map(txt).join(' / '));
 T('G3 보관함에 앱 두 묶음 모두 보인다 · 「✓ MM/DD HH:MM」 = dt',heads.length===2&&heads[0].indexOf('민법OX')===0&&heads[1].indexOf('tt')===0&&rows.length===2&&rows.every(r=>txt(r.querySelector('.d'))===want),heads.join(' / ')+' | '+want);
 const rb=btnTxt(rows[0],'되돌리기');
 __adv(1000);rb.click();
 const y=items('ai').find(z=>z.id===pid);
 T('G3 「되돌리기」 → done:0 · dt 없음 · 진행중 복귀',!!y&&y.done===0&&!('dt' in y)&&(ui.aiView='open',!!cardOf(openShare('ai'),pid)),JSON.stringify(y&&{done:y.done,dt:y.dt}));
});

/* G4 포스트잇 — pin·done 거르기 · 120자+… · 마크다운 벗기기 · 클릭 */
G('G4',()=>{reseed();
 const a1=addApp('민법OX');
 const long='# 제목 **굵게** '+'가'.repeat(130);
 const pA=postNow(long,[a1],1),pB=postNow('핀 없는 글',[a1],0),pC=postNow('완료된 핀 글',[a1],1);
 aiDoneTog(pC);
 let main=openShare('ai');
 const pis=[...main.querySelectorAll('.aipi')],ids=pis.map(e=>e.id);
 I('G4 포스트잇 판',ids.join(','));
 T('G4 (add1 갱신) 📌 인 글만 판에 — 핀 없는 글은 없고, 완료된 핀 글은 회색 종이로 있다(옛 「done:0 만」 잣대 갱신)',pis.length===2&&ids.indexOf('aipi-'+pA)>=0&&ids.indexOf('aipi-'+pC)>=0&&ids.indexOf('aipi-'+pB)<0&&main.querySelector('#aipi-'+pC).classList.contains('done'),ids.join(','));
 const sc=main.querySelector('#aipi-'+pA+' .sc');
 T('G4 (add1 갱신) 본문은 안 자른다 — 종이 안에 글 전체가 들어가고 넘치면 스크롤(옛 「120자+…」 잣대 갱신)',!!sc&&txt(sc).indexOf('제목 굵게')===0&&txt(sc).length>120&&sc.scrollHeight>=sc.clientHeight,'len='+txt(sc).length+' scroll='+sc.scrollHeight+'/'+sc.clientHeight);
 T('G4 포스트잇에 글쓴이·앱 칩·댓글 수',txt(main.querySelector('#aipi-'+pA+' .who'))===ME&&main.querySelectorAll('#aipi-'+pA+' .apps .aiapp').length===1&&txt(main.querySelector('#aipi-'+pA+' .off'))==='댓글 0',txt(main.querySelector('#aipi-'+pA)));
 const el=main.querySelector('#aipi-'+pA),r=el.getBoundingClientRect();
 const pe=(t,x,y)=>el.dispatchEvent(new PointerEvent(t,{bubbles:true,cancelable:true,pointerId:1,pointerType:'mouse',button:0,buttons:t==='pointerup'?0:1,clientX:x,clientY:y}));
 pe('pointerdown',r.left+4,r.top+4);pe('pointermove',r.left+5,r.top+5);pe('pointerup',r.left+5,r.top+5);
 T('G4 (add1 갱신) 누르면 팝업이 열린다(옛 「진행중 보기로 이동」 잣대 갱신)',!!document.getElementById('aiPop'),'');
 closeModals();
});

/* G5 권한 — 남의 글 수정·삭제 없음 · 📌·완료·댓글은 있음 · 남의 댓글 삭제 없음 */
G('G5',()=>{reseed();
 const a1=addApp('민법OX');
 addRaw([{id:'o1',ty:'ai',t:'햄찌가 쓴 글',apps:[a1],pin:0,done:0,by:OT,at:3000,u:3000,del:false,
   cm:[{id:'oc1',by:OT,t:'햄찌 댓글',at:3100,u:3100,del:false},{id:'oc2',by:ME,t:'내 댓글',at:3200,u:3200,del:false}]}]);
 const mine=postNow('내가 쓴 글',[a1],0);
 let main=openShare('ai');
 const o=cardOf(main,'o1'),m=cardOf(main,mine);
 const ft=el=>txt(el.querySelector('.ft'));
 I('G5 남의 글 발치',ft(o)+' || 내 글 '+ft(m));
 T('G5 남의 글엔 「수정·삭제」 없음 · 📌·완료 네모·댓글은 있음',!!o&&ft(o).indexOf('수정')<0&&ft(o).indexOf('삭제')<0&&ft(o).indexOf('댓글')>=0&&!!o.querySelector('.ck')&&!!o.querySelector('.hd .pin'),ft(o));
 T('G5 내 글엔 「수정·삭제」 있음',!!m&&ft(m).indexOf('수정')>=0&&ft(m).indexOf('삭제')>=0,ft(m));
 const r=aiDel('o1');
 T('G5 aiDel 을 억지로 불러도 남의 글은 안 지워진다',r===false&&items('ai').some(x=>x.id==='o1'&&!x.del),'r='+r);
 shareCmTog('o1');main=openShare('ai');
 const cms=[...cardOf(main,'o1').querySelectorAll('.shcmi')];
 T('G5 댓글 — 남의 댓글엔 × 없음 · 내 댓글엔 있음(Text 탭과 같은 함수)',cms.length===2&&!cms[0].querySelector('span[onclick^="shareCmDel"]')&&!!cms[1].querySelector('span[onclick^="shareCmDel"]'),cms.map(txt).join(' / '));
 const el=document.getElementById('shC_o1');el.value='내가 다는 댓글';__adv(1000);shareCmAdd('o1');
 const oo=items('ai').find(x=>x.id==='o1');
 T('G5 남의 글에도 댓글은 누구나 단다(cm 3개 · by 꼬까)',(oo.cm||[]).filter(c=>!c.del).length===3&&oo.cm[2].by===ME,JSON.stringify((oo.cm||[]).map(c=>c.by+':'+c.t)));
 const pin0=items('ai').find(x=>x.id==='o1').pin;aiPinPost('o1');
 T('G5 남의 글에도 📌·완료는 누구나',items('ai').find(x=>x.id==='o1').pin!==pin0,'');
});

/* G6 앱 거르개 — 세 보기 모두 · 개수 = 실제 수 */
G('G6',()=>{reseed();
 const a1=addApp('민법OX'),a2=addApp('tt');
 const p1=postNow('a1 진행중',[a1],0),p2=postNow('a2 진행중 핀',[a2],1),p3=postNow('a1 완료',[a1],0);
 aiDoneTog(p3);
 ui.aiApp=a1;let main=openShare('ai');
 I('G6 a1 세 칸',txt(main.querySelector('.aibox')).slice(0,36)+' || 보관함 '+txt(main.querySelector('.aibox.arc')).slice(0,36));
 T('G6 (add1 갱신) 앱 a1 = 진행중 칸 a1 글만 · 포스트잇 판 0장 · 보관함도 a1 묶음만(옛 「알약」 잣대 갱신)',!!cardOf(main,p1)&&!cardOf(main,p2)&&main.querySelectorAll('.aipi').length===0&&main.querySelectorAll('.aiarc h4').length===1&&txt(main.querySelector('.aiarc h4')).indexOf('민법OX')===0,
   'pi='+main.querySelectorAll('.aipi').length+' arc='+[...main.querySelectorAll('.aiarc h4')].map(txt).join('|'));
 ui.aiApp=a2;main=openShare('ai');
 T('G6 (add1 갱신) 앱 a2 = 진행중 1(핀 글) · 포스트잇 한 장 · 보관함은 비었다',!!cardOf(main,p2)&&!cardOf(main,p1)&&main.querySelectorAll('.aipi').length===1&&txt(main.querySelector('.aibox.arc')).indexOf('보관함이 비었어')>0,
   'pi='+main.querySelectorAll('.aipi').length+' arc='+txt(main.querySelector('.aibox.arc')).slice(0,40));
 ui.aiApp='all';main=openShare('ai');
 const chips=[...main.querySelectorAll('.aisub.apps .aiapp')].map(txt);
 I('G6 앱 칩 개수(진행중 보기)',chips.join(' / '));
 T('G6 앱 칩 개수 = 그 보기 안 실제 수(전체 2 · 민법OX 1 · tt 1)',chips.length===3&&chips[0].replace(/\s/g,'')==='전체2'&&chips[1].replace(/\s/g,'')==='민법OX1'&&chips[2].replace(/\s/g,'')==='tt1',chips.join(' / '));
});

/* G7 다른 탭 무변 */
G('G7',()=>{reseed();
 /* 무변 줄을 먼저 잰다 — 옛 판(헛잣대)에서도 여기까지는 돌아야 「무변」이 뜻을 갖는다 */
 const t0=JSON.stringify(shareItems('txt')),i0=JSON.stringify(shareItems('img')),v0=JSON.stringify(shareItems('pv'));
 const m3=openShare('txt');
 I('G7 Text 탭 HTML 해시(두 판 대조용)',hash(shareHTML()));
 T('G7 Text 탭 그대로 — 쓰기 칸 · 갈래 칩 · 댓글 토글 · ai 마크업 없음 — 무변 잣대',!!m3.querySelector('#shT')&&!!m3.querySelector('.shcat')&&!!m3.querySelector('.shcm .tg')&&!m3.querySelector('.aitab'),'');
 const m4=openShare('pv');
 T('G7 ⚡ 벌칙포상 탭 그대로(잔액 칸·목록 두 기둥) — 무변 잣대',!!m4.querySelector('.pvtab')&&!!m4.querySelector('.pvbal')&&m4.querySelectorAll('.pvcol').length===2,'');
 const m5=openShare('img');
 T('G7 🖼 Image 탭 그대로 — 무변 잣대',!!m5.querySelector('#shF')&&!m5.querySelector('.aitab'),'');
 const a1=addApp('민법OX');postNow('글',[a1],1);
 T('G7 app·ai 를 더해도 shareItems(txt)·(img)·(pv) 결과 무변',JSON.stringify(shareItems('txt'))===t0&&JSON.stringify(shareItems('img'))===i0&&JSON.stringify(shareItems('pv'))===v0,t0+' || '+i0+' || '+v0);
 const tabs=[...openShare('ai').querySelectorAll('.views:not(.moretabs) span')].map(s=>s.textContent);
 T('G7 서브탭 넷 그대로 · 🤖 가 이제 빈 탭이 아니다',tabs.join('|')==='🖼 Image|📝 Text|⚡ 벌칙포상|🤖 클로드'&&!!document.querySelector('#main .aitab')&&document.getElementById('main').textContent.indexOf('다음 판')<0,tabs.join('|'));
});

/* X1 보관함 줄 펼침 — 본문 + 댓글(달기까지) */
G('X1',()=>{reseed();
 const a1=addApp('민법OX');
 const pid=postNow('보관함 펼침 시험 글 본문',[a1],0);
 aiDoneTog(pid);
 ui.aiView='arc';let main=openShare('ai');
 const row=main.querySelector('.aiarc .r');
 row.click();main=document.getElementById('main');
 const op=main.querySelector('.aiopen');
 T('X1 보관함 줄을 누르면 그 자리에서 본문이 펼쳐진다(글 한 장 그대로)',!!op&&!!op.querySelector('.ainote')&&txt(op).indexOf('보관함 펼침 시험 글 본문')>=0,txt(op).slice(0,60));
 shareCmTog(pid);main=openShare('ai');
 const inp=document.getElementById('shC_'+pid);
 if(inp){inp.value='보관함에서 단 댓글';__adv(1000);shareCmAdd(pid)}
 const x=items('ai').find(z=>z.id===pid);
 T('X1 펼친 자리에서 댓글도 달린다',!!inp&&(x.cm||[]).filter(c=>!c.del).length===1&&x.cm[0].t==='보관함에서 단 댓글',JSON.stringify((x.cm||[]).map(c=>c.t)));
 main=openShare('ai');const row2=main.querySelector('.aiarc .r');row2.click();
 T('X1 다시 누르면 접힌다',!document.getElementById('main').querySelector('.aiopen'),'');
});

T('X2 검사 내내 스크립트 오류 0(window error) — 무변 잣대',__errs.length===0,__errs.join(' / '));
const pre=document.createElement('pre');pre.id='AIH';pre.textContent='\n'+R.join('\n')+'\n';document.body.appendChild(pre);
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
    함수마다 글자 md5 를 바탕 스냅샷(QC.base · 칸 'SRC.fn|<함수 머리>')과 맞댄다. 못 찾은 함수(fn_text = None)는 gate 처럼 바뀐 것으로 센다(_harness_tt_claudetab.py)"""
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
    if QC.SMOKE:   # smoke — 이 하네스엔 smoke 칸이 없다(처리표 칸 39 · smoke 0) — 앱을 띄우기 전에 끝
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
    mm = re.search(r'<pre id="AIH">(.*?)</pre>', dom, re.S)
    lines = [s.strip() for s in HT.unescape(mm.group(1)).split('\n') if s.strip()] if mm else []
    if not lines:
        print('결과 줄 없음 — 부팅 사망? dom %d bytes → %s' % (len(dom), os.path.join(OUT, 'dom.html')))
        return 1
    if QC.GATE:   # gate — --ref 고정 옛 커밋(git show)과 글자 대조(이 판 앞 그대로)
        QC.sub('git:show-app')   # §B-4 셈 — 옛 커밋 앱 풀기(regress 0)
        g = subprocess.run(['git', '-C', GENIE, 'show', A.ref + ':timetable/index.html'], capture_output=True, timeout=60)
        if g.returncode == 0:
            ref = g.stdout.decode('utf-8')
            # add1 갱신 — shareCmAdd(입력칸 id 인자)·pvTabHTML(잔액 칸 공용 함수화)은 add1 이 일부러 고쳤다. 그 둘은 add1 하네스가 「한 줄만 다르다」로 따로 잰다
            names = ['function shMd(', 'function mergeList(', 'function mergeFile(', 'function shareItems(', 'function upsertShare2(', 'function shareFile(',
                     'function shareKeep(', 'function shareAddText(', 'function shareCmTog(', 'function shareCmDel(',
                     'function shareDel(', 'function shareEdit(', 'function pvApply(', 'function pvChip(', 'function dayCard(']
            bad = [n for n in names if fn_text(src, n) is None or fn_text(src, n) != fn_text(ref, n)]
            lines.append(('PASS' if not bad else 'FAIL') + ' | SRC 손대지 않는 함수 %d개 = %s 과 글자 같음(마크다운·병합·share 읽기쓰기·댓글·⚡탭·dayCard) — 무변 잣대' % (len(names), A.ref)
                         + ('' if not bad else ' | ' + ', '.join(bad)))
            a, b = fn_text(src, 'function shareHTML('), fn_text(ref, 'function shareHTML(')
            da = [x for x in (a or '').split('\n') if x not in (b or '').split('\n')]
            db = [x for x in (b or '').split('\n') if x not in (a or '').split('\n')]
            okh = (len(da) == 0 and len(db) == 0) or (len(da) == 1 and len(db) == 1 and "tab==='ai'" in da[0] and "tab==='ai'" in db[0])
            lines.append(('PASS' if okh else 'FAIL') + ' | SRC shareHTML 은 ai 갈래 한 줄만 다르다(Image·Text·⚡ 갈래 글자 무변) — 무변 잣대'
                         + ('' if okh else ' | NEW만 %d줄 %s / 옛판만 %d줄 %s' % (len(da), da[:2], len(db), db[:2])))
        else:
            lines.append('INFO | SRC 무변 대조 못 함 | git show %s 실패' % A.ref)
    else:   # regress — git show 0 · 「손대지 않는 함수 N개 = --ref 글자」(처리표 기준) = 함수마다 글자 md5 를 바탕 스냅샷(QC.base)과 맞댄다 · 「shareHTML 은 ai 갈래 한 줄만 다르다」 = gate 만(인도 판 diff 셈 · 처리표 관문만)
        names = ['function shMd(', 'function mergeList(', 'function mergeFile(', 'function shareItems(', 'function upsertShare2(', 'function shareFile(',
                 'function shareKeep(', 'function shareAddText(', 'function shareCmTog(', 'function shareCmDel(',
                 'function shareDel(', 'function shareEdit(', 'function pvApply(', 'function pvChip(', 'function dayCard(']   # gate 의 names 와 같은 목록(바꾸면 둘 다)
        bad = _rg_fn_bad(src, names)
        lines.append(('PASS' if not bad else 'FAIL') + ' | SRC 손대지 않는 함수 %d개 = %s 과 글자 같음(마크다운·병합·share 읽기쓰기·댓글·⚡탭·dayCard) — 무변 잣대' % (len(names), A.ref)
                     + ' | ' + (', '.join(bad) + ' · ' if bad else '') + _rg_note(names))
    for ln in lines:
        print('   ' + ln)
    f = sum(1 for ln in lines if ln.startswith('FAIL'))
    p = sum(1 for ln in lines if ln.startswith('PASS'))
    print('\n합계  PASS %d · FAIL %d  (src %s · %d B)' % (p, f, SRC, os.path.getsize(SRC)))
    return 0 if f == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
