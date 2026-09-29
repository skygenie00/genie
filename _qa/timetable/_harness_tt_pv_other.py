# -*- coding: utf-8 -*-
"""tt앱 — 벌칙포상 수행·메모를 두 사람 다 쓸 수 있게 (_task_tt_pv_other §C G1~G7).

앱 사본에 날짜 고정(2026-09-16 12:00 KST) + 시드(꼬까·햄찌 9월 스냅샷 · share.json) + 검사를 넣고
헤드리스 크롬 --dump-dom 으로 <pre id="PVH"> 결과 줄을 받는다. 網은 fetch 통째 거절 · confirm 은 참.
게이트마다 시드를 다시 깐다(loadF 는 부를 때마다 localStorage 를 새로 읽는다).

⚠ 가장 중요한 잣대 — **상대 스냅샷 파일이 바이트째 무변**인가. 그 파일은 그 사람 두 기기가 병합하는 자리다.

쓰기 : python _harness_tt_pv_other.py [--src 앱.html] [--out 폴더]
  --src 를 옛 판(HEAD blob 사본)으로 주면 헛잣대 — G1~G5 가 거짓이어야 한다(G7).
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import argparse, html as HT, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

ap = argparse.ArgumentParser()
ap.add_argument('--src', default=_roots.genie(r"timetable\index.html"))
ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "h_pvother"))
A = ap.parse_args()
SRC, OUT = os.path.abspath(A.src), os.path.abspath(A.out)
os.makedirs(OUT, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ANCHOR = "<script>\n/* ============================================================\n   타임테이블 v1"

PIN = ("<script>(function(){const R=Date;let OFF=new R('2026-09-16T12:00:00+09:00').getTime()-R.now();"
       "function D(...a){return a.length?new R(...a):new R(R.now()+OFF)}D.prototype=R.prototype;"
       "D.now=()=>R.now()+OFF;D.parse=R.parse;D.UTC=R.UTC;window.Date=D;window.__adv=ms=>{OFF+=ms};"
       "window.__errs=[];addEventListener('error',e=>__errs.push(String(e.message)+' @'+(e.lineno||'')));"
       "window.fetch=()=>Promise.reject(new Error('harness: network blocked'));})();</script>")

ME, OT = '꼬까', '햄찌'


def snap(total, pv='', pd=0, **kw):
    e = {'at': 1, 'u': 1, 'total': total, 'memo': '', 'pv': pv, 'pd': pd, 'ss': [], 'it': []}
    e.update(kw)
    return e


SEED_FILES = {
    # 꼬까(나) — ⚡ 09/10·09/11 미수행 · 09/12 옛 pd:1(스냅샷에만) · 🍀 09/09 · 09/13 메모
    'tt.f.snaps/%s/2026-09.json' % ME: {'v': 1, 'days': {
        '2026-09-09': snap(620, 'rew'), '2026-09-10': snap(100, 'pen'), '2026-09-11': snap(90, 'pen'),
        '2026-09-12': snap(80, 'pen', 1), '2026-09-13': snap(300, '', 0, memo='내 옛 메모')},
        'weeks': {'W02': {'memo': '내 주 메모', 'u': 5}}, 'months': {}},
    # 햄찌(상대) — ⚡ 09/14·09/16 · 🍀 09/15 · 메모 하나(이관에 안 끌려와야 한다)
    'tt.f.snaps/%s/2026-09.json' % OT: {'v': 1, 'days': {
        '2026-09-14': snap(50, 'pen'), '2026-09-15': snap(650, 'rew'),
        '2026-09-16': snap(60, 'pen', 0, memo='상대 옛 메모')}, 'weeks': {}, 'months': {}},
    'tt.f.share/share.json': {'v': 1, 'items': [
        {'id': 'pA', 'ty': 'pv', 'kind': 'pen', 'who': ME, 't': '스쿼트 50', 'w': 1, 'by': ME, 'at': 2000, 'u': 2000, 'del': False},
        {'id': 'pB', 'ty': 'pv', 'kind': 'pen', 'who': ME, 't': '설거지', 'w': 2, 'by': ME, 'at': 2001, 'u': 2001, 'del': False},
        {'id': 'rA', 'ty': 'pv', 'kind': 'rew', 'who': ME, 't': '케이크', 'w': 1, 'by': ME, 'at': 2003, 'u': 2003, 'del': False},
        {'id': 'hA', 'ty': 'pv', 'kind': 'pen', 'who': OT, 't': '팔굽혀펴기', 'w': 1, 'by': ME, 'at': 2005, 'u': 2005, 'del': False},
        {'id': 'hB', 'ty': 'pv', 'kind': 'pen', 'who': OT, 't': '방 치우기', 'w': 2, 'by': ME, 'at': 2006, 'u': 2006, 'del': False},
        {'id': 'hR', 'ty': 'pv', 'kind': 'rew', 'who': OT, 't': '치킨', 'w': 1, 'by': ME, 'at': 2007, 'u': 2007, 'del': False},
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
const raw=k=>localStorage.getItem(k)||'';
const shareItemsAll=()=>{const f=rd('tt.f.share/share.json');return(f&&f.data&&f.data.items)||[]};
const pvdOf=(w,d)=>shareItemsAll().find(x=>x.id==='pvd|'+w+'|'+d)||null;
const memoItem=(w,k,key)=>shareItemsAll().find(x=>x.id==='memo|'+w+'|'+k+'|'+key)||null;
const dirtyOf=p=>{const f=rd('tt.f.'+p);return !!(f&&f.dirty)};
const closeModals=()=>document.querySelectorAll('.modal').forEach(m=>m.remove());
const reseed=()=>{closeModals();const ks=[];for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k.indexOf('tt.f.')===0)ks.push(k)}
 ks.forEach(k=>localStorage.removeItem(k));localStorage.removeItem('tt.pvd_migrated');
 Object.keys(__SEED).forEach(k=>localStorage.setItem(k,JSON.stringify({data:JSON.parse(JSON.stringify(__SEED[k])),sha:null,dirty:false})));__adv(60000)};
const host=document.createElement('div');host.id='pvHost';host.style.cssText='width:360px;background:#fff';document.body.insertBefore(host,document.body.firstChild);
const card=(w,d)=>{host.innerHTML=dayCard(w,d);return host.querySelector('.card .lb .pvc')};
const openShare=tab=>{ui.view='share';ui.shareTab=tab;render();return document.getElementById('main')};
const lastModal=()=>{const a=document.querySelectorAll('.modal');return a.length?a[a.length-1]:null};
const txt=el=>el?el.textContent.replace(/\s+/g,' ').trim():'';
/* 사람 자리(.chip.h / .chip.k)는 settings.people 차례에 달렸다 — 반에 박지 말고 **이름**으로 찾는다 */
const rowOf=(main,md,w)=>[...main.querySelectorAll('.pvdue .pvrow')].find(r=>txt(r).indexOf(md)===0&&txt(r.querySelector('.chip'))===w)||null;
const boxOf=(main,w)=>[...main.querySelectorAll('.pvbal>div')].find(x=>txt(x.querySelector('.who'))===w)||null;
const btnTxt=(el,t)=>el?([...el.querySelectorAll('button')].find(b=>txt(b)===t)||null):null;
window.confirm=()=>true;
const NEW=(typeof pvState==='function');

/* ═══ G1 상대 칩을 눌러 정해 준다 — 상대 스냅샷 파일은 바이트째 무변 ═══ */
G('G1',()=>{reseed();
 const otBefore=raw('tt.f.snaps/'+OT+'/'+M+'.json'),meBefore=raw('tt.f.snaps/'+ME+'/'+M+'.json');
 const ch=card(OT,'2026-09-14');
 I('G1 상대 ⚡ 칩',ch?ch.outerHTML.slice(0,160):'없음');
 T('G1 상대 칩에 onclick 이 있다',!!ch&&/pvPick\(/.test(ch.getAttribute('onclick')||''),ch?String(ch.getAttribute('onclick')):'칩 없음');
 T('G1 상대 칩에도 .on',!!ch&&ch.classList.contains('on'),ch?ch.className:'');
 if(ch)ch.click();
 const m=lastModal();
 I('G1 팝업',txt(m).slice(0,120));
 T('G1 상대 칩 클릭 = 팝업이 뜬다',!!m,'팝업 없음');
 T('G1 팝업 머리에 누구 것인지',!!m&&!!m.querySelector('h4 .chip')&&txt(m.querySelector('h4 .chip'))===OT,m?txt(m.querySelector('h4')):'');
 const opts=m?[...m.querySelectorAll('.pvopt')]:[];
 I('G1 고를 항목',opts.map(x=>x.dataset.id).join(','));
 T('G1 그 사람 항목만 뜬다(hA·hB)',opts.map(x=>x.dataset.id).join(',')==='hA,hB',opts.map(x=>x.dataset.id).join(','));
 __adv(1000);
 const o=opts.find(x=>x.dataset.id==='hA');if(o)o.click();
 const ok=m&&m.querySelector('#mOk');if(ok)ok.click();
 const it=pvdOf(OT,'2026-09-14');
 I('G1 share 항목',JSON.stringify(it));
 T('G1 share.json 에 pvd|상대|날 1건',!!it&&it.ty==='pvd'&&it.who===OT&&it.d==='2026-09-14'&&it.pd===1&&it.pvi==='hA'&&it.pvd==='2026-09-16',JSON.stringify(it));
 T('G1 by = 누른 사람(나)',!!it&&it.by===ME,it?String(it.by):'');
 T('G1 ★ 상대 스냅샷 파일이 바이트째 무변',raw('tt.f.snaps/'+OT+'/'+M+'.json')===otBefore,'바뀜');
 T('G1 내 스냅샷도 무변',raw('tt.f.snaps/'+ME+'/'+M+'.json')===meBefore,'바뀜');
 T('G1 dirty 는 share.json 만',dirtyOf('share/share.json')&&!dirtyOf('snaps/'+OT+'/'+M+'.json')&&!dirtyOf('snaps/'+ME+'/'+M+'.json'),
   'share='+dirtyOf('share/share.json')+' ot='+dirtyOf('snaps/'+OT+'/'+M+'.json')+' me='+dirtyOf('snaps/'+ME+'/'+M+'.json'));
 const ch2=card(OT,'2026-09-14');
 T('G1 칩이 회색 취소선으로 바뀐다',!!ch2&&ch2.classList.contains('pd'),ch2?ch2.className:'');
});

/* ═══ G2 되돌리기 · 무게 2 묶음 · 상쇄 · 「상쇄 N」 ═══ */
G('G2',()=>{reseed();
 const n0=shareItemsAll().length;
 __adv(1000);pvApply('2026-09-14','hA',OT);
 const n1=shareItemsAll().length;
 __adv(1000);pvUndo('2026-09-14',OT);
 const it=pvdOf(OT,'2026-09-14'),n2=shareItemsAll().length;
 I('G2 되돌린 뒤',JSON.stringify(it));
 T('G2 되돌리기 = pd:0 으로 덮임(항목 수 그대로 · del 없음)',!!it&&it.pd===0&&!it.del&&n2===n1&&n1===n0+1,
   'n '+n0+'→'+n1+'→'+n2+' · '+JSON.stringify(it));
 T('G2 되돌린 뒤 pvi·pvd 가 없다',!!it&&!it.pvi&&!it.pvd,JSON.stringify(it));
 /* 무게 2 = 두 칩 묶음 */
 reseed();__adv(1000);
 const done=pvApply('2026-09-14','hB',OT);        /* 팔굽혀펴기 아닌 무게 2 「방 치우기」 — ⚡ 두 장 필요 */
 const a=pvdOf(OT,'2026-09-14'),b=pvdOf(OT,'2026-09-16');
 I('G2 무게 2',JSON.stringify([done,a&&a.pvb,b&&b.pvb]));
 T('G2 무게 2 = 상대 ⚡ 두 칩이 같은 묶음표로 함께',done===true&&!!a&&!!b&&a.pd===1&&b.pd===1&&a.pvb&&a.pvb===b.pvb,
   JSON.stringify([a&&a.pd,b&&b.pd,a&&a.pvb,b&&b.pvb]));
 __adv(1000);pvUndo('2026-09-14',OT);
 const a2=pvdOf(OT,'2026-09-14'),b2=pvdOf(OT,'2026-09-16');
 T('G2 묶음 되돌리기 = 둘 다 살아난다',!!a2&&a2.pd===0&&!!b2&&b2.pd===0,JSON.stringify([a2&&a2.pd,b2&&b2.pd]));
 /* 상쇄 */
 reseed();__adv(1000);
 const off=pvOffset('2026-09-14','2026-09-15',OT);
 const x1=pvdOf(OT,'2026-09-14'),x2=pvdOf(OT,'2026-09-15');
 T('G2 상쇄 = 짝끼리 pvx',off===true&&!!x1&&x1.pvx==='2026-09-15'&&!!x2&&x2.pvx==='2026-09-14',JSON.stringify([x1,x2]));
 /* 「상쇄 N」 두 사람 다 */
 reseed();
 const main=openShare('pv');
 const bo=boxOf(main,OT),bm=boxOf(main,ME);
 I('G2 잔액 칸',txt(bm)+' || '+txt(bo));
 T('G2 「상쇄 N」 이 두 사람 다 있다',!!btnTxt(bo,'상쇄 1')&&!!btnTxt(bm,'상쇄 1'),txt(bm)+' || '+txt(bo));
 T('G2 상대 「상쇄」 단추가 그 사람 who 로 배선',!!bo&&/pvOffsetN\('햄찌'\)/.test(bo.innerHTML),bo?bo.innerHTML.slice(0,200):'');
 /* 상대 칩 줄 */
 const due=main?main.querySelector('.pvdue'):null;
 const allRows=main?[...main.querySelectorAll('.pvdue .pvrow')]:[];
 I('G2 pvdue 줄 수',allRows.length+' · '+allRows.map(x=>txt(x).slice(0,22)).join(' / '));
 I('G2 people',JSON.stringify(settings.people));
 const r=rowOf(main,'09/14',OT);
 I('G2 상대 칩 줄',txt(r));
 T('G2 상대 줄에 select 가 있다',!!r&&!!r.querySelector('select'),txt(r));
 T('G2 상대 줄에 「수행함」·「상쇄」',!!btnTxt(r,'수행함')&&!!btnTxt(r,'상쇄'),txt(r));
 T('G2 상대 줄이 `—` 가 아니다',!!r&&txt(r).indexOf('—')<0||!!(r&&r.querySelector('select')),txt(r));
 /* 줄에서 직접 수행함 */
 const sel=r&&r.querySelector('select');
 if(sel){sel.value='hA';__adv(1000);btnTxt(r,'수행함').click()}
 const rowIt=pvdOf(OT,'2026-09-14');
 T('G2 상대 줄 「수행함」 이 그 사람 것으로 저장된다',!!rowIt&&rowIt.who===OT&&rowIt.pd===1&&rowIt.pvi==='hA',JSON.stringify(rowIt));
});

/* ═══ G3 잔액 — 옛 스냅샷 pd · share 항목 · 둘 다(share 승) ═══ */
G('G3',()=>{reseed();
 const b0=pvBal(ME);
 I('G3 옛 pd 만(09/12)',JSON.stringify(b0));
 T('G3 스냅샷 옛 pd 를 그대로 센다 — ⚡2 🍀1',b0.pen===2&&b0.rew===1,JSON.stringify(b0));
 /* share 에 09/10 을 수행으로 → ⚡1 */
 __adv(1000);pvApply('2026-09-10','pA',ME);
 const b1=pvBal(ME);
 T('G3 share 항목이 더해지면 ⚡1',b1.pen===1&&b1.rew===1,JSON.stringify(b1));
 /* 둘 다 있는 칩 — 09/12 는 스냅샷 pd:1 인데 share 가 pd:0 이면 **share 가 이긴다** */
 __adv(1000);pvWrite(ME,[['2026-09-12',z=>{z.pd=0;delete z.pvi;delete z.pvd;delete z.pvx;delete z.pvb}]]);
 const b2=pvBal(ME);
 I('G3 share 가 이긴 뒤',JSON.stringify(b2));
 T('G3 둘 다 있으면 share 가 이긴다 — 09/12 가 되살아나 ⚡2',b2.pen===2&&b2.rew===1,JSON.stringify(b2));
 T('G3 스냅샷 옛 pd 는 안 지운다(되돌릴 수 있게)',(rd(SK(ME)).data.days['2026-09-12']||{}).pd===1,
   JSON.stringify(rd(SK(ME)).data.days['2026-09-12']));
});

/* ═══ G4 이관 — 내 것만 · 한 번만 ═══ */
G('G4',()=>{reseed();
 const n0=shareItemsAll().length;
 const a=pvdMigrate();
 const n1=shareItemsAll().length;
 const got=shareItemsAll().filter(x=>x.ty==='pvd'||x.ty==='memo');
 I('G4 옮긴 것',got.map(x=>x.id).sort().join(' / '));
 T('G4 첫 실행 = 내 pd 1 + 내 memo 2 = 3건',a===3&&n1===n0+3,'n '+n0+'→'+n1+' · a='+a);
 T('G4 pvd|나|09-12 가 있다',!!pvdOf(ME,'2026-09-12'),JSON.stringify(pvdOf(ME,'2026-09-12')));
 T('G4 memo|나|days|09-13 · memo|나|weeks|W02',!!memoItem(ME,'days','2026-09-13')&&!!memoItem(ME,'weeks','W02'),got.map(x=>x.id).join(','));
 T('G4 ★ 상대 스냅샷 메모는 안 옮긴다',!memoItem(OT,'days','2026-09-16'),JSON.stringify(memoItem(OT,'days','2026-09-16')));
 T('G4 u 는 원래 e.u',(pvdOf(ME,'2026-09-12')||{}).u===1,JSON.stringify(pvdOf(ME,'2026-09-12')));
 const b=pvdMigrate();
 T('G4 두 번째 실행은 0건',b===0&&shareItemsAll().length===n1,'b='+b+' n='+shareItemsAll().length);
 T('G4 이관 표시가 남는다',!!LS.get('tt.pvd_migrated'),String(LS.get('tt.pvd_migrated')));
});

/* ═══ G5 메모 — 상대 것도 고쳐진다 · 스냅샷 무변 ═══ */
G('G5',()=>{reseed();
 const otBefore=raw('tt.f.snaps/'+OT+'/'+M+'.json');
 /* 일간 */
 snapView(OT,'2026-09-16');
 let m=lastModal(),ta=m&&m.querySelector('#snMemo');
 I('G5 상대 일간 메모 칸',ta?('readonly='+ta.hasAttribute('readonly')+' val='+ta.value):'없음');
 T('G5 상대 일간 메모가 readonly 가 아니다',!!ta&&!ta.hasAttribute('readonly'),ta?'readonly':'칸 없음');
 T('G5 옛 스냅샷 메모가 보인다',!!ta&&ta.value==='상대 옛 메모',ta?ta.value:'');
 if(ta){ta.value='내가 고친 상대 메모';__adv(1000);const ok=m.querySelector('#mOk');if(ok)ok.click()}
 const mi=memoItem(OT,'days','2026-09-16');
 T('G5 memo|상대|days|날 항목이 생긴다',!!mi&&mi.memo==='내가 고친 상대 메모'&&mi.by===ME,JSON.stringify(mi));
 T('G5 ★ 상대 스냅샷 파일 무변',raw('tt.f.snaps/'+OT+'/'+M+'.json')===otBefore,'바뀜');
 closeModals();
 snapView(OT,'2026-09-16');
 m=lastModal();ta=m&&m.querySelector('#snMemo');
 T('G5 다시 열면 그 값',!!ta&&ta.value==='내가 고친 상대 메모',ta?ta.value:'');
 closeModals();
 /* 주간 */
 snapViewW(OT,'2026-09-14');
 m=lastModal();ta=m&&m.querySelector('#snMemo');
 T('G5 상대 주간 메모 칸이 readonly 아님',!!ta&&!ta.hasAttribute('readonly'),ta?'readonly':'칸 없음');
 if(ta){ta.value='상대 주 메모';__adv(1000);const ok=m.querySelector('#mOk');if(ok)ok.click()}
 T('G5 memo|상대|weeks 항목',!!shareItemsAll().find(x=>x.ty==='memo'&&x.who===OT&&x.kind==='weeks'&&x.memo==='상대 주 메모'),
   JSON.stringify(shareItemsAll().filter(x=>x.ty==='memo').map(x=>x.id)));
 closeModals();
 /* 월간 */
 snapViewM(OT,'2026-09');
 m=lastModal();ta=m&&m.querySelector('#snMemo');
 T('G5 상대 월간 메모 칸이 readonly 아님',!!ta&&!ta.hasAttribute('readonly'),ta?'readonly':'칸 없음');
 if(ta){ta.value='상대 달 메모';__adv(1000);const ok=m.querySelector('#mOk');if(ok)ok.click()}
 T('G5 memo|상대|months 항목',!!memoItem(OT,'months','2026-09')&&memoItem(OT,'months','2026-09').memo==='상대 달 메모',
   JSON.stringify(memoItem(OT,'months','2026-09')));
 T('G5 ★ 메모 셋을 써도 상대 스냅샷 파일 무변',raw('tt.f.snaps/'+OT+'/'+M+'.json')===otBefore,'바뀜');
 closeModals();
});

/* ═══ 무변 — 일간 잔액줄·타이머 자리 ═══ */
G('X1',()=>{reseed();
 T('X1 pvDayBalHTML 이 그대로 있다',typeof pvDayBalHTML==='function',typeof pvDayBalHTML);
 const h=pvDayBalHTML();
 T('X1 일간 잔액줄이 두 사람을 그린다',h.indexOf(ME)>=0&&h.indexOf(OT)>=0,h.slice(0,160));
 T('X1 takeSnap·dayRows 는 그대로',typeof takeSnap==='function'&&typeof dayRows==='function','');
 T('X1 스크립트 오류 0',(window.__errs||[]).length===0,JSON.stringify((window.__errs||[]).slice(0,4)));
 I('X1 NEW',String(NEW));
});

const pre=document.createElement('pre');pre.id='PVH';pre.textContent=R.join('\n');document.body.appendChild(pre);
})();
</script>"""


def main():
    src = open(SRC, encoding='utf-8').read()
    assert ANCHOR in src, 'seed anchor not found'
    h = src.replace(ANCHOR, PIN + SEED + ANCHOR, 1)
    tests = TESTS.replace('__ME__', json.dumps(ME)).replace('__OT__', json.dumps(OT))
    h = h.replace('</body>', tests + '</body>', 1)
    app = os.path.join(OUT, 'app.html')
    open(app, 'w', encoding='utf-8', newline='\n').write(h)
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
                        '--user-data-dir=' + os.path.join(OUT, 'prof'),
                        '--allow-file-access-from-files', '--window-size=1280,900',
                        '--virtual-time-budget=12000', '--dump-dom',
                        'file:///' + app.replace('\\', '/')],
                       capture_output=True, timeout=300)
    dom = r.stdout.decode('utf-8', 'replace')
    open(os.path.join(OUT, 'dom.html'), 'w', encoding='utf-8').write(dom)
    mm = re.search(r'<pre id="PVH">(.*?)</pre>', dom, re.S)
    lines = [s.strip() for s in HT.unescape(mm.group(1)).split('\n') if s.strip()] if mm else []
    if not lines:
        print('결과 줄 없음 — 부팅 사망? dom %d bytes → %s' % (len(dom), os.path.join(OUT, 'dom.html')))
        return 1
    for l in lines:
        print('   ' + l)
    p = sum(1 for l in lines if l.startswith('PASS'))
    f = sum(1 for l in lines if l.startswith('FAIL'))
    print('\n합계  PASS %d · FAIL %d  (src %s · %d B)' % (p, f, SRC, os.path.getsize(SRC)))
    return 0 if not f else 1


if __name__ == '__main__':
    sys.exit(main())
