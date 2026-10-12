# -*- coding: utf-8 -*-
r"""_task_jagwa_theorybar_1012 §3 관문 [클라우드] — 자과 물리: 근거 공식·개념 찾기 = 볼트 통짜 「물리 목차」 · 개념·이론 창 그림 = 창 안 확대 ·
   위 개념·공식 창 = 절 머리 줄이 붙어 따라오는 손잡이 · 카드 층 2 칸 오류 막이

  python _harness_jagwa_theorybar.py [--new <앱>] [--base <판 = f67f747>] [--eng chromium,webkit] [--only G1,G2,…] [--spd <studyplandata>] [--notes <notes>] [--vendor <cdnjs 사본>] [--res <결과>]

  NEW = genie 작업트리 jagwa/index.html · BASE = 바탕 main f67f747(앱 LF md5 edf2d5c9 · 헛잣대 — G1 · G2 · G4 · G5 · G6 · G8 · G9 바탕 FAIL · G3 · G7 · G10 바탕도 PASS)
  앱 옆 theory_fix.json = 작업트리 jagwa/theory_fix.json(main 그대로 · 두 판 다 같은 자리에 둠 — 바탕 앱은 안 읽음)
  엔진 = Chromium · WebKit · PC 1100×800 마우스 · 폰 384×740 hasTouch(Chromium = CDP 손가락 · WebKit = touchscreen.tap · 두 손가락 = 합성 touch 포인터) · 원격 = 가짜(PUT 밖으로 0)
  시험 글 = 지어낸 것(G8 「쿼즐뭉」 근거) 또는 앱에 이미 있는 THEORY · UNITS 글(낱말 「분리」 · 블록 머리 「(3) 분리」) · 실제 근거 · 기록 글은 출력에 안 옮김(셈 · md5 앞 8 자 · D11)
  칸:
    G1 공식·개념 칸 「분리」 → 「1.3.8」 「(3) 분리」 블록 · 「(4) 충돌,2차원」 블록보다 앞
    G2 그 블록 누름(PC 마우스 · 폰 손가락) → 근거 줄 → 줄 누름 → 쓰인 문항 창 #gguwSec .g3mk = 「(3) 분리」 줄만 · dashed · 창 안 보이는 자리
    G3 옛 근거(ref U:^<UNITS 1.3.8 (1) 블록 a>) → 줄 글 · 쓰인 수 = 바탕 · 줄 누름 = 점선 테두리 있음
    G4 위 「개념」 창 본문 30 % 굴림 → 맨 위 ±6px 에 붙은 .thsec>h3 하나 · sticky · 그 줄 (−200,+150) 끌기 → 창 움직임 · scrollTop 그대로 · 덮개 안 열림
    G5 위 「공식」 창 · 같은 잣대(.pwh)
    G6 개념 · 이론(#tTheory) · 옛 풀이 노트(#tSol) 창 그림 — a[target=_blank] img 0 · 누름 = 주소 그대로 · 새 창 0 · Ctrl+휠 위 4 칸 = 폭 1.3 배↑ · 두 번 누름 = 처음 폭(±2) · 폰 두 손가락 벌림 = 폭↑
    G7 다른 창 무변 — 서랍 근거 작은 창 · 쓰인 문항 창 · 🃏 암기카드 창 손잡이 끌기 = 바탕과 같은 움직임
    G8 지학 · 생물(카드 층) 근거 2 칸 글 찾기 → 페이지 오류 0 · 목록 그려짐 · 고르면 근거 들어감
    G9 theory_fix.json 을 늦게 줌(route 잡아 둠 · 1.5 초 뒤 놓음) · 그 전에 「분리」 한 번 → 늦게 온 뒤 다시 치면 「(3) 분리」
    G10 위 모든 화면 페이지 오류 0 · 가로 넘침 0 · 처음 뜬 새 창 높이 ≤ innerHeight/3(문항 본창 예외)
  모드 — gate = 바탕 띄움 · regress · smoke = 새 판만(smoke = G1 · G10 PC 크롬)
"""
import os as _os_r, sys as _sys_r   # env_lanes — _roots.py 를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402,F401 — --mode · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음
import _qa_jagwa_common as JG   # noqa: E402
import hashlib, json, os, sys, tempfile, time, traceback   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEWF = ARG('--new', _roots.genie('jagwa', 'index.html'))
BASE = ARG('--base', 'f67f747')
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
TMPD = os.path.join(tempfile.gettempdir(), 'h_jagwa_theorybar')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_jagwa_theorybar_result.txt'))
SPD = ARG('--spd', _roots.spd())
NOTES = ARG('--notes', os.path.join(os.path.dirname(_roots.spd()), 'notes'))
VENDOR = ARG('--vendor', os.path.join(TMPD, 'vendor'))
JG.conf(VENDOR_PP=VENDOR, SPD_PP=SPD, NOTES=NOTES, SHOTS=os.path.join(TMPD, 'shots'))
GATE = QC.GATE
if GATE:
    QC.sub('git:show-app')
SRC = {'NEW': JG.app_src(NEWF)}
if GATE:
    SRC['BASE'] = JG.app_src(BASE)
PC, PH = (1100, 800), (384, 740)
RES = []
SMOKE_CELLS = {'G1', 'G10'}
WORD = '분리'
QZ = '쿼즐뭉'                       # G8 지어낸 낱말
QZ_T = '쿼즐뭉 공식 시험근거'        # G8 다른 문항 2 칸에 넣는 지어낸 근거 글


def want(c):
    return (not ONLY or c.upper() in ONLY) and (not QC.SMOKE or c in SMOKE_CELLS)


def _s(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


def h8(s):
    return hashlib.md5(' '.join(str(s or '').split()).encode('utf-8')).hexdigest()[:8]


def R(g, name, new, base=None, d='', yard=True):
    RES.append(dict(g=g, name=name, new=new, base=base, yard=yard, d=d))
    tag = 'INFO' if new is None else ('PASS' if new else 'FAIL')
    yb = '' if base is None else (' · 바탕 ' + (('PASS(바탕도 같음)' if not yard else 'PASS') if base else ('FAIL' if yard else 'FAIL(바탕도 같아야 할 칸)')))
    print('%s | %s · %s%s | %s' % (tag, g, name, yb, _s(d)[:700]), flush=True)


def _h6(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()[:6]


def _pg(br, eng, tag, ver, subj, dev, touch):
    p = JG.Pg_PP(br, eng, '%s-%s-%s' % (tag, eng, _h6(SRC[ver])), SRC[ver], subj, dev, touch=touch, remote=JG.Remote())
    p.wait(800)
    return p


# ══ JS ════════════════════════════════════════════════════════════════════════════════
PICK_JS = r"""(skip)=>{for(const r of DATA){const no=r[F.NO];if(typeof isC==='function'&&isC(r))continue;if((skip||[]).indexOf(no)>=0)continue;if(hist(no).length)continue;
  const u=GGU(r);if(!u||!rowByUid(u)||ggOf(u).length)continue;return no}return null}"""
OPEN_JS = r"""async (no)=>{await openView(no);for(let i=0;i<40;i++){await new Promise(r=>setTimeout(r,100));if(!HASBOOK||QUID===String(qk(no)))break}
  try{setTool('view')}catch(e){}await new Promise(r=>setTimeout(r,500));return VNO}"""
UID_JS = r"""(no)=>GGU(rec(no))"""
UNFOLD_JS = r"""()=>{const v=document.getElementById('view');if(v&&v.classList.contains('g3off')){const b=document.getElementById('g3Fold');if(b)b.click()}return !!v&&!v.classList.contains('g3off')}"""
FIELD = '[data-ggbox="%s|qp-"] .g3f .ggrows .txt'
FOCUS_JS = r"""(q)=>{const e=document.querySelector(q);if(!e)return null;try{e.scrollIntoView({block:'center'})}catch(_){}e.focus();e.value='';const r=e.getBoundingClientRect();return {x:r.left+12,y:r.top+r.height/2,f:document.activeElement===e}}"""
# 찾기 목록 — 줄마다 절(sec 머리 앞 번호) · 「(3) 분리」 · 「(4) 충돌,2차원」 · 누를 자리(블록 첫 줄)
SUG_JS = r"""()=>{const s=[...document.querySelectorAll('.g3sug:not(.hide)')].find(x=>x.getBoundingClientRect().height>0);if(!s)return {sug:false,rows:[]};
  const N=t=>String(t||'').replace(/\s+/g,'');
  const rows=[...s.querySelectorAll('.g3s')].map((e,i)=>{const sec=e.querySelector('.sec'),bt=e.querySelector('.bt')||e,r=(bt.getBoundingClientRect());
    const st=sec?String(sec.textContent).trim():'';return {i,sec:(st.match(/^[\d.]+?(?=\.\s|\s|$)/)||[''])[0],b3:N(bt.textContent).indexOf('(3)분리')===0,b4:N(bt.textContent).indexOf('(4)충돌,2차원')===0,
      cx:r.left+Math.min(r.width/2,60),cy:r.top+Math.min(r.height/2,9),hit:(()=>{const t=document.elementFromPoint(r.left+Math.min(r.width/2,60),r.top+Math.min(r.height/2,9));return !!t&&e.contains(t)})()}});
  return {sug:true,n:rows.length,rows,none:!!s.querySelector('.g3none')}}"""
# 근거 줄(공식·개념) — 그 문항 항목 중 ref 를 준 것 · 누를 자리 = 글(.g3tx)
ITEM_JS = r"""([u,ref])=>{const its=ggOf(u).filter(x=>x&&(x.f||'')==='c'&&(!ref||x.ref===ref||(ref==='T:'&&String(x.ref||'').indexOf('T:')===0)));const g=its[its.length-1];if(!g)return {n:ggOf(u).length,item:null};
  const el=document.querySelector('[data-g3c="'+CSS.escape(u+'|'+g.k)+'"]');let at=null;if(el){const t=el.querySelector('.g3tx')||el;try{t.scrollIntoView({block:'center'})}catch(_){}const r=t.getBoundingClientRect();
    const x=r.left+Math.min(12,r.width/2),y=r.top+Math.min(r.height/2,9),h=document.elementFromPoint(x,y);at={cx:x,cy:y,on:!!h&&el.contains(h)}}
  const use=el?el.querySelector('[data-g3use],.g3n,.g3use'):null;
  return {n:ggOf(u).length,k:g.k,ref:String(g.ref||''),refT:String(g.ref||'').indexOf('T:')===0,at,tx:el?(el.querySelector('.g3tx')||{}).textContent||'':'',use:use?String(use.textContent).trim():null}}"""
# 쓰인 문항 창 — 점선 테두리 블록
GGUW_JS = r"""(ref)=>{const w=document.getElementById('gguw');if(!w)return {win:false};const sec=w.querySelector('#gguwSec'),mk=[...w.querySelectorAll('#gguwSec .g3mk')],p=w.querySelector('.panel')||w;
  const pr=p.getBoundingClientRect(),sr=sec?sec.getBoundingClientRect():pr,m=mk[0];let want=null;
  try{if(ref&&window.G3&&G3.blocks){const b=G3.blocks().find(x=>x.key===ref);if(b)want=b.lines.reduce((s,n)=>s+1+(n.g?1:0),0)}}catch(e){}
  const N=t=>String(t||'').replace(/\s+/g,'');const mr=m?m.getBoundingClientRect():null;
  return {win:true,n:mk.length,kids:m?m.children.length:0,want,t3:m?N(m.textContent).indexOf('(3)분리')>=0:false,oth:m?/\((1|2|4)\)/.test(N(m.textContent).replace(/^\(3\)/,'')):null,
    bs:m?getComputedStyle(m).borderTopStyle:null,top:mr?Math.round(mr.top-sr.top):null,bot:mr?Math.round(sr.bottom-mr.bottom):null,mh:mr?Math.round(mr.height):null,
    winH:Math.round(pr.height),ih:innerHeight}}"""
# G3 — UNITS 1.3.8 「(1)」 블록 앞(a) · 그 블록 글(옛 근거 t)
OLDREF_JS = r"""()=>{const s=((typeof UNITS!=='undefined'&&UNITS.sec)||[]).find(x=>String(x.id)==='1.3.8');if(!s)return null;let cur=[],out=null;
  const flush=()=>{if(!out&&cur.length&&cur.some(n=>/\(1\)/.test(String(n.x||'')))){const a=(cur.find(n=>n.a)||{}).a;if(a)out={a,t:cur.map(n=>String(n.x||'').replace(/<[^>]+>/g,'').trim()).join('\n')}}cur=[]};
  (s.b||[]).forEach(b=>{if(b.t==='br'){flush();return}if(b.t==='tb'){flush();return}if(b.t==='p'&&String(b.x||'').trim())cur.push(b)});flush();return out}"""
SEEDC_JS = r"""async ([no,f,t,ref])=>{const r=rec(no),u=GGU(r);const list=ggOf(u).slice();list.forEach((x,n)=>{if(x&&x.i!==n+1)x.i=n+1});
  const g={k:ggNewKey('g_'),i:list.length+1,t:t,ok:ggMarkNow(no),ts:Date.now(),cs:[],f:f};if(ref)g.ref=ref;list.push(g);await ggSaveList(u,list);try{ggRepaint(u)}catch(e){}return {uid:u,k:g.k}}"""
# 창 하나 — 겉 자리 · 굴림 · 덮개
WIN_JS = r"""(q)=>{const b=document.querySelector(q);if(!b)return null;const p=b.querySelector(':scope>.panel')||b,r=p.getBoundingClientRect(),bd=b.querySelector('#pwlBody');
  return {l:Math.round(r.left),t:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),st:bd?Math.round(bd.scrollTop):null,sh:bd?bd.scrollHeight:null,ch:bd?bd.clientHeight:null,
    onL:b.classList.contains('thcOnL'),onR:b.classList.contains('thcOnR'),ih:innerHeight}}"""
# 개념(.thsec>h3) · 공식(.pwh) 창 — 본문 30 % 굴림 → 맨 위에 붙은 머리 · 잡을 자리
STICK_JS = r"""(sel)=>{const b=document.getElementById('pwl'),bd=b&&b.querySelector('#pwlBody');if(!bd)return null;bd.scrollTop=Math.round(0.3*(bd.scrollHeight-bd.clientHeight));return Math.round(bd.scrollTop)}"""
STUCK_JS = r"""(sel)=>{const b=document.getElementById('pwl'),bd=b&&b.querySelector('#pwlBody');if(!bd)return null;const top=bd.getBoundingClientRect().top;
  const H=[...bd.querySelectorAll(sel)].filter(h=>{const r=h.getBoundingClientRect();return r.height>0&&r.bottom>top});const st=H.filter(h=>Math.abs(h.getBoundingClientRect().top-top)<=6);
  const g=st[0]||H[0];let at=null;if(g){const r=g.getBoundingClientRect(),x=Math.round(r.left+Math.min(40,r.width/3)),y=Math.round(r.top+Math.min(r.height/2,10)),t=document.elementFromPoint(x,y);at={cx:x,cy:y,on:!!t&&(t===g||g.contains(t))}}
  return {n:st.length,pos:st[0]?getComputedStyle(st[0]).position:(H[0]?getComputedStyle(H[0]).position:null),at,st:Math.round(bd.scrollTop)}}"""
# 그림 — 창 안 첫 그림(다 받은 것) · 새 창 밖 a 셈
IMG_JS = r"""async ([wq,iq])=>{const w=document.querySelector(wq);if(!w)return {win:false};const aimg=w.querySelectorAll('a[target=_blank] img').length;
  const L=[...w.querySelectorAll(iq)];let im=null;for(const x of L){try{x.scrollIntoView({block:'center'})}catch(_){}for(let i=0;i<30;i++){if(x.complete&&x.naturalWidth>0)break;await new Promise(r=>setTimeout(r,100))}
    if(x.complete&&x.naturalWidth>0&&x.getBoundingClientRect().width>20){im=x;break}}
  if(!im)return {win:true,aimg,img:false,n:L.length};im.dataset.tbpick='1';try{im.scrollIntoView({block:'center'})}catch(_){}await new Promise(r=>setTimeout(r,200));
  const r=im.getBoundingClientRect(),x=Math.round(r.left+r.width/2),y=Math.round(r.top+Math.min(r.height/2,60)),t=document.elementFromPoint(x,y);
  return {win:true,aimg,img:true,n:L.length,w:Math.round(r.width*10)/10,cx:x,cy:y,on:!!t&&(t===im||im.contains(t)||t.contains(im))}}"""
IMGW_JS = r"""()=>{const im=document.querySelector('img[data-tbpick="1"]');if(!im)return null;return Math.round(im.getBoundingClientRect().width*10)/10}"""
IMGAT_JS = r"""()=>{const im=document.querySelector('img[data-tbpick="1"]');if(!im)return null;try{im.scrollIntoView({block:'nearest'})}catch(_){}const r=im.getBoundingClientRect();
  let L=Math.max(r.left,0),T=Math.max(r.top,0),Rr=Math.min(r.right,innerWidth),B=Math.min(r.bottom,innerHeight);for(let e=im.parentElement;e&&e!==document.body;e=e.parentElement){const cs=getComputedStyle(e);
    if(/(auto|scroll|hidden)/.test(cs.overflowY+cs.overflowX)){const q=e.getBoundingClientRect();L=Math.max(L,q.left);T=Math.max(T,q.top);Rr=Math.min(Rr,q.right);B=Math.min(B,q.bottom)}}
  for(const fy of [0.6,0.75,0.45,0.9,0.3])for(const fx of [0.5,0.3,0.7]){const x=Math.round(L+(Rr-L)*fx),y=Math.round(T+(B-T)*fy),t=document.elementFromPoint(x,y);if(t===im)return {cx:x,cy:y}}
  return {cx:Math.round((L+Rr)/2),cy:Math.round((T+B)/2),miss:1}}"""
UNPICK_JS = r"""()=>{document.querySelectorAll('img[data-tbpick]').forEach(x=>x.removeAttribute('data-tbpick'));return 1}"""
# 두 손가락(WebKit = 합성 touch 포인터 둘 · Chromium 은 CDP)
PINCH_WK = r"""([x,y,d0,d1,n])=>{const t=document.elementFromPoint(x,y);if(!t)return 0;const ev=(ty,id,cx,b)=>{const e=new PointerEvent(ty,{bubbles:true,cancelable:true,composed:true,pointerId:id,pointerType:'touch',isPrimary:id===61,clientX:cx,clientY:y,buttons:b});t.dispatchEvent(e)};
  ev('pointerdown',61,x-d0,1);ev('pointerdown',62,x+d0,1);for(let i=1;i<=n;i++){const d=d0+(d1-d0)*i/n;ev('pointermove',61,x-d,1);ev('pointermove',62,x+d,1)}ev('pointerup',61,x-d1,0);ev('pointerup',62,x+d1,0);return 1}"""
OVERFLOW_JS = r"""()=>({sw:document.documentElement.scrollWidth,iw:innerWidth,ok:document.documentElement.scrollWidth<=innerWidth+1})"""
HAND_JS = r"""(q)=>{const b=document.querySelector(q);if(!b)return null;const h=b.querySelector('.twhandle');if(!h)return {handle:false};const r=h.getBoundingClientRect();
  const pts=[[10,Math.min(8,r.height/2)],[r.width*0.3,r.height/2],[r.width*0.5,Math.min(12,r.height/2)]];for(const [dx,dy] of pts){const x=Math.round(r.left+dx),y=Math.round(r.top+dy),t=document.elementFromPoint(x,y);
    if(t&&h.contains(t)&&!t.closest('button,a,input,textarea,select,[data-nodrag]'))return {handle:true,cx:x,cy:y,cls:String(h.id||h.className).slice(0,30)}}return {handle:true,cx:null}}"""
NOHAND_JS = r"""(q)=>{const b=document.querySelector(q);if(!b)return null;const p=b.querySelector(':scope>.panel')||b,r=p.getBoundingClientRect();
  for(const [fx,fy] of [[0.5,6],[0.3,10],[0.7,14]]){const x=Math.round(r.left+r.width*fx),y=Math.round(r.top+fy),t=document.elementFromPoint(x,y);if(t&&b.contains(t)&&!t.closest('button,a,input,textarea,select'))return {cx:x,cy:y}}return null}"""
DRAWER_OX_JS = r"""(no)=>{const r=rec(no);try{g3PopToggle(no,document.createElement('span'))}catch(e){return 'ERR '+e}return !!document.getElementById('g3Pop')}"""
CARDQ_JS = r"""(n)=>{const out=[];for(const r of DATA){const no=r[F.NO];if(typeof isC==='function'&&isC(r))continue;if(hist(no).length)continue;const u=GGU(r);if(!u||!rowByUid(u)||ggOf(u).length)continue;out.push(no);if(out.length>=n)break}return out}"""
THQ_JS = r"""()=>{for(const r of DATA){if(typeof isC==='function'&&isC(r))continue;try{if(secsFor(r).some(s=>(s.b||[]).some(n=>n.g)))return r[F.NO]}catch(e){}}return null}"""
SOLQ_JS = r"""()=>{for(const r of DATA){if(typeof isC==='function'&&isC(r))continue;const s=(typeof SOL!=='undefined'&&SOL)?SOL[r[F.VLT]]:null;if(s&&(s.g||[]).length)return r[F.NO]}return null}"""
SHEETS_JS = r"""()=>[...document.querySelectorAll('.sheet')].map(s=>{const p=s.querySelector(':scope>.panel')||s,r=p.getBoundingClientRect();return {id:s.id||'',cls:String(s.className).slice(0,40),h:Math.round(r.height),fl:p.classList.contains('float')||s.classList.contains('shfloat')}})"""


def mdrag(p, x, y, dx, dy, n=12):
    p.pg.mouse.move(x, y); p.pg.mouse.down()
    for i in range(1, n + 1):
        p.pg.mouse.move(x + dx * i / n, y + dy * i / n); p.wait(16)
    p.pg.mouse.up(); p.wait(350)


def type_field(p, uid, word):
    at = p.ev(FOCUS_JS, FIELD % uid)
    if not at:
        return None
    p.pg.keyboard.type(word); p.wait(700)
    return p.ev(SUG_JS)


def pick3(s):
    rows = (s or {}).get('rows') or []
    i3 = next((r['i'] for r in rows if r['b3'] and r['sec'] == '1.3.8'), None)
    i4 = next((r['i'] for r in rows if r['b4']), None)
    return i3, i4


def win_h(p, q):
    w = p.ev(WIN_JS, q)
    return None if not w else {'h': w['h'], 'ih': w['ih'], 'ok': w['h'] <= w['ih'] / 3 + 1}


def img_test(p, wq, iq, touch=False):
    """그림 — a[target=_blank] img 셈 · 누름(주소 · 새 창) · Ctrl+휠 위 4 칸 · 두 번 누름(PC) / 두 손가락 벌림(폰)"""
    o = p.ev(IMG_JS, [wq, iq])
    if not o or not o.get('img'):
        return o
    url0, pages0 = p.pg.url, len(p.ctx.pages)
    if touch:
        p.tap(o['cx'], o['cy'], 500)
    else:
        p.click(o['cx'], o['cy'], 600)
    p.wait(400)
    o['누름'] = {'주소 그대로': p.pg.url == url0, '새 창': len(p.ctx.pages) - pages0}
    for pg in p.ctx.pages[pages0:]:
        try:
            pg.close()
        except Exception:
            pass
    if not p.ev("()=>!!document.querySelector('img[data-tbpick=\"1\"]')"):
        o['그림 사라짐'] = True
        return o
    w0 = p.ev(IMGW_JS)
    at = p.ev(IMGAT_JS)
    if not touch:
        p.pg.mouse.move(at['cx'], at['cy'])
        p.pg.keyboard.down('Control')
        for _ in range(4):
            p.pg.mouse.wheel(0, -100); p.wait(90)
        p.pg.keyboard.up('Control'); p.wait(300)
        w1 = p.ev(IMGW_JS)
        at = p.ev(IMGAT_JS)
        p.pg.mouse.dblclick(at['cx'], at['cy']); p.wait(400)
        w2 = p.ev(IMGW_JS)
        o['폭'] = {'처음': w0, 'Ctrl+휠': w1, '두 번 누름': w2}
    else:
        if p.eng == 'webkit':
            p.ev(PINCH_WK, [at['cx'], at['cy'], 20, 80, 12])
        else:
            c = p._cdp()
            x, y = at['cx'], at['cy']
            c.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x - 20, 'y': y, 'radiusX': 6, 'radiusY': 6, 'id': 1}, {'x': x + 20, 'y': y, 'radiusX': 6, 'radiusY': 6, 'id': 2}]})
            for i in range(1, 13):
                d = 20 + 60 * i / 12
                c.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x - d, 'y': y, 'radiusX': 6, 'radiusY': 6, 'id': 1}, {'x': x + d, 'y': y, 'radiusX': 6, 'radiusY': 6, 'id': 2}]}); p.wait(16)
            c.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        p.wait(400)
        o['폭'] = {'처음': w0, '두 손가락': p.ev(IMGW_JS)}
    p.ev(UNPICK_JS)
    return o


def win_drag(p, q, dx=-60, dy=40):
    h = p.ev(HAND_JS, q)
    if h and h.get('handle') is False:   # 손잡이 없는 창 — 위쪽 안을 잡고 끌어 봄(움직임 = 바탕과 맞댐)
        at = p.ev(NOHAND_JS, q)
        h = {'handle': False, 'cx': at and at['cx'], 'cy': at and at['cy'], 'cls': '(손잡이 없음 · 위쪽 안)'}
    if not h or not h.get('cx'):
        return {'손잡이': h}
    w0 = p.ev(WIN_JS, q)
    mdrag(p, h['cx'], h['cy'], dx, dy)
    w1 = p.ev(WIN_JS, q)
    return {'손잡이': h.get('cls'), 'd': [w1['l'] - w0['l'], w1['t'] - w0['t']] if w0 and w1 else None}


# ══ 흐름 ════════════════════════════════════════════════════════════════════════════════
def safe(o, k, fn):
    try:
        o[k] = fn()
    except Exception:
        o[k] = {'하네스 오류': traceback.format_exc()[-500:]}


def flow_pc(br, eng, ver):
    """물리 PC 1100×800 마우스 — G1 · G2 · G3 · G4 · G5 · G6(개념 · 이론 · 풀이 노트) · G7 · G10"""
    o, H = {}, {}
    p = _pg(br, eng, 'tbPC', ver, 'phys', PC, False)
    try:
        no = p.ev(PICK_JS, []); p.ev(OPEN_JS, no); uid = p.ev(UID_JS, no)
        H['문항 본창'] = 'skip'
        p.ev(UNFOLD_JS); p.ev("(u)=>g3Sel(u,'c')", uid); p.wait(300)
        s = type_field(p, uid, WORD)
        i3, i4 = pick3(s)
        o['G1'] = {'줄': (s or {}).get('n'), '(3) 분리': i3, '(4) 충돌,2차원': i4, '절': [r['sec'] for r in (s or {}).get('rows') or []][:8]}
        o['G10o'] = {'G1': p.ev(OVERFLOW_JS)['ok']}
        # G2 — 그 블록 마우스 누름 → 근거 줄 → 줄 누름 → 쓰인 문항 창
        if i3 is not None:
            r3 = s['rows'][i3]
            p.click(r3['cx'], r3['cy'], 700)
            it = p.ev(ITEM_JS, [uid, 'T:'])
            g2 = {'근거 줄': bool(it.get('item') is not False and it.get('k')), 'ref T:': it.get('refT')}
            if it.get('at') and it['at'].get('on'):
                p.click(it['at']['cx'], it['at']['cy'], 1100)
                g2['창'] = p.ev(GGUW_JS, it.get('ref'))
                H['쓰인 문항 창'] = win_h(p, '#gguw')
                o['G10o']['G2'] = p.ev(OVERFLOW_JS)['ok']
                p.ev("()=>{const w=document.getElementById('gguw');if(w)w.remove();return 1}")
            o['G2'] = g2
        else:
            o['G2'] = {'블록 없음': True}
        p.ev("(q)=>{const e=document.querySelector(q);if(e){e.value='';e.blur()}return 1}", FIELD % uid)
        # G3 — 옛 근거(ref U:^a) · G7 쓰인 문항 창 끌기
        def g3():
            ob = p.ev(OLDREF_JS)
            if not ob:
                return {'UNITS 1.3.8 (1) 없음': True}
            no2 = p.ev(PICK_JS, [no]); sd = p.ev(SEEDC_JS, [no2, 'c', ob['t'], 'U:^' + ob['a']])
            p.ev(OPEN_JS, no2); p.ev(UNFOLD_JS); p.wait(300)
            it = p.ev(ITEM_JS, [sd['uid'], 'U:^' + ob['a']])
            r = {'ref': 'U:^…', '글': h8(it.get('tx')), '쓰인 수': it.get('use'), '창': None}
            if it.get('at') and it['at'].get('on'):
                p.click(it['at']['cx'], it['at']['cy'], 1100)
                gw = p.ev(GGUW_JS, None)
                r['창'] = {'점선': gw.get('n'), 'dashed': gw.get('bs')}
                o['G7'] = {'쓰인 문항 창': win_drag(p, '#gguw')}
                p.ev("()=>{const w=document.getElementById('gguw');if(w)w.remove();return 1}")
            return r
        safe(o, 'G3', g3)
        # G4 · G6 개념 — 위 「개념」 창
        def g4():
            p.ev("()=>{const o=document.getElementById('pwl');if(o)o.remove();try{pwList('c')}catch(e){return 'ERR '+e}return 1}"); p.wait(700)
            H['개념 창'] = win_h(p, '#pwl')
            w0 = p.ev(WIN_JS, '#pwl'); p.ev(STICK_JS, '.thsec>h3'); p.wait(300)
            sk = p.ev(STUCK_JS, '.thsec>h3')
            r = {'붙은 머리': sk and sk.get('n'), 'position': sk and sk.get('pos')}
            if sk and sk.get('at') and sk['at'].get('on'):
                st0 = p.ev(WIN_JS, '#pwl')
                mdrag(p, sk['at']['cx'], sk['at']['cy'], -200, 150)
                w1 = p.ev(WIN_JS, '#pwl')
                r.update({'창 옮김': [w1['l'] - st0['l'], w1['t'] - st0['t']], 'scrollTop': [st0['st'], w1['st']], '덮개': [w1['onL'], w1['onR']]})
            r['처음'] = w0 and {'l': w0['l'], 't': w0['t']}
            o['G10o']['G4'] = p.ev(OVERFLOW_JS)['ok']
            return r
        safe(o, 'G4', g4)
        safe(o, 'G6c', lambda: img_test(p, '#pwl', '.thpic'))
        p.ev("()=>{const o=document.getElementById('pwl');if(o)o.remove();return 1}")
        # G5 — 위 「공식」 창
        def g5():
            p.ev("()=>{try{pwList('f')}catch(e){return 'ERR '+e}return 1}"); p.wait(800)
            H['공식 창'] = win_h(p, '#pwl')
            p.ev(STICK_JS, '.pwh'); p.wait(300)
            sk = p.ev(STUCK_JS, '.pwh')
            r = {'붙은 머리': sk and sk.get('n'), 'position': sk and sk.get('pos')}
            if sk and sk.get('at') and sk['at'].get('on'):
                st0 = p.ev(WIN_JS, '#pwl')
                mdrag(p, sk['at']['cx'], sk['at']['cy'], -200, 150)
                w1 = p.ev(WIN_JS, '#pwl')
                r.update({'창 옮김': [w1['l'] - st0['l'], w1['t'] - st0['t']], 'scrollTop': [st0['st'], w1['st']], '덮개': [w1['onL'], w1['onR']]})
            o['G10o']['G5'] = p.ev(OVERFLOW_JS)['ok']
            p.ev("()=>{const o=document.getElementById('pwl');if(o)o.remove();return 1}")
            return r
        safe(o, 'G5', g5)
        # G6 이론 창(#tTheory)
        def g6t():
            nt = p.ev(THQ_JS); p.ev(OPEN_JS, nt); p.wait(300)
            p.ev("()=>{const b=document.getElementById('tTheory');if(b)b.click();return !!b}"); p.wait(900)
            H['이론 창'] = win_h(p, '#sh-theory')
            r = img_test(p, '#sh-theory', '.thpic')
            o['G10o']['G6t'] = p.ev(OVERFLOW_JS)['ok']
            p.ev("()=>{const s=document.getElementById('sh-theory');if(s)s.remove();return 1}")
            return r
        safe(o, 'G6t', g6t)
        # G6 옛 풀이 노트(#tSol)
        def g6s():
            ns = p.ev(SOLQ_JS); p.ev(OPEN_JS, ns); p.wait(300)
            p.ev("()=>{const b=document.getElementById('tSol');if(b)b.click();return !!b}"); p.wait(900)
            q = p.ev("()=>{const S=[...document.querySelectorAll('.sheet.thsheet')].filter(s=>s.id!=='sh-theory');const s=S[S.length-1];if(!s)return null;s.dataset.tbsol='1';return 1}")
            H['풀이 노트'] = win_h(p, '[data-tbsol="1"]') if q else None
            r = img_test(p, '[data-tbsol="1"]', '.solpic') if q else {'창': None}
            o['G10o']['G6s'] = p.ev(OVERFLOW_JS)['ok']
            p.ev("()=>{const s=document.querySelector('[data-tbsol=\"1\"]');if(s)s.remove();return 1}")
            return r
        safe(o, 'G6s', g6s)
        # G7 — 서랍 근거 작은 창 · 🃏 암기카드 창
        def g7():
            r = dict(o.get('G7') or {})
            nq = p.ev(PICK_JS, [])
            p.ev(OPEN_JS, nq)
            if p.ev(DRAWER_OX_JS, nq) is True:
                p.wait(500); H['서랍 근거 작은 창'] = win_h(p, '#g3Pop')
                r['서랍 근거 작은 창'] = win_drag(p, '#g3Pop')
                p.ev("()=>{try{g3PopClose()}catch(e){}return 1}")
            p.ev("(no)=>{try{mcardWin(no)}catch(e){return 'ERR '+e}return 1}", nq); p.wait(700)
            H['암기카드 창'] = win_h(p, '.sheet.mcwin')
            r['암기카드 창'] = win_drag(p, '.sheet.mcwin')
            p.ev("()=>{const s=document.querySelector('.sheet.mcwin');if(s)s.remove();try{MCW=null}catch(e){}return 1}")
            return r
        safe(o, 'G7', g7)
        o['G10'] = {'오류': (p.errs or [])[:4], '넘침 0': o.get('G10o'), '첫 높이': H}
    finally:
        p.close()
    return o


def flow_phone(br, eng, ver):
    """물리 폰 384×740 손가락 — G2(손가락) · G6(두 손가락 벌림)"""
    o = {}
    q = _pg(br, eng, 'tbPH', ver, 'phys', PH, True)
    try:
        no = q.ev(PICK_JS, []); q.ev(OPEN_JS, no); uid = q.ev(UID_JS, no)
        q.ev(UNFOLD_JS); q.ev("(u)=>g3Sel(u,'c')", uid); q.wait(300)
        s = type_field(q, uid, WORD)
        i3, _ = pick3(s)
        g2 = {'(3) 분리': i3}
        if i3 is not None:
            r3 = s['rows'][i3]
            q.tap(r3['cx'], r3['cy'], 700)
            it = q.ev(ITEM_JS, [uid, 'T:'])
            g2['근거 줄'] = bool(it.get('k')); g2['ref T:'] = it.get('refT')
            if it.get('at') and it['at'].get('on'):
                q.tap(it['at']['cx'], it['at']['cy'], 1100)
                g2['창'] = q.ev(GGUW_JS, it.get('ref'))
                q.ev("()=>{const w=document.getElementById('gguw');if(w)w.remove();return 1}")
        o['G2'] = g2
        q.ev("(q)=>{const e=document.querySelector(q);if(e){e.value='';e.blur()}return 1}", FIELD % uid)
        def g6():
            q.ev("()=>{const o=document.getElementById('pwl');if(o)o.remove();try{pwList('c')}catch(e){return 'ERR '+e}return 1}"); q.wait(700)
            return img_test(q, '#pwl', '.thpic', touch=True)
        safe(o, 'G6c', g6)
        o['오류'] = (q.errs or [])[:4]
        o['넘침'] = q.ev(OVERFLOW_JS)
    finally:
        q.close()
    return o


def flow_card(br, eng, ver):
    """지학 · 생물 PC — G8 근거 2 칸 글 찾기(다른 문항 2 칸에 지어낸 근거)"""
    out = {}
    for subj in ('earth', 'bio'):
        o = {}
        p = _pg(br, eng, 'tbC' + subj, ver, subj, PC, False)
        try:
            a, b = (p.ev(CARDQ_JS, 2) + [None, None])[:2]
            sd = p.ev(SEEDC_JS, [b, 'c', QZ_T, None])
            p.ev(OPEN_JS, a); uid = p.ev(UID_JS, a)
            p.ev("(q)=>{const e=document.querySelector(q);if(e)try{e.scrollIntoView({block:'center'})}catch(_){}return !!e}", '[data-ggbox="%s|qp-"]' % uid); p.wait(200)
            e0 = len(p.errs or [])
            p.ev("(u)=>g3Sel(u,'c')", uid); p.wait(300)
            s = type_field(p, uid, QZ)
            rows = (s or {}).get('rows') or []
            o['목록'] = {'그려짐': bool(s and s.get('sug')), '줄': len(rows), '맞는 것 없음 글': bool(s and s.get('none'))}
            n0 = p.ev("(u)=>ggOf(u).length", uid)
            if rows and rows[0].get('hit'):
                p.click(rows[0]['cx'], rows[0]['cy'], 700)
            n1 = p.ev("(u)=>ggOf(u).length", uid)
            it = p.ev("(u)=>{const g=ggOf(u).slice(-1)[0];return g?{f:g.f||null,src:!!g.src,t:window.__tbH?null:null}:null}", uid)
            o['근거'] = {'수': [n0, n1], '칸 c': (it or {}).get('f') == 'c', 'src(같은 근거)': (it or {}).get('src')}
            o['오류'] = (p.errs or [])[e0:e0 + 4]
            o['넘침'] = p.ev(OVERFLOW_JS)['ok']
        except Exception:
            o['하네스 오류'] = traceback.format_exc()[-500:]
        finally:
            p.close()
        out[subj] = o
    return out


def flow_g9(br, eng, ver):
    """theory_fix.json 을 잡아 둠(route) → 「분리」 한 번 → 1.5 초 뒤 놓음 → 다시 「분리」"""
    o = {}
    p = _pg(br, eng, 'tbG9', ver, 'phys', PC, False)
    try:
        held = []
        p.ctx.route('**/theory_fix.json', lambda rt: held.append(rt))
        t0 = time.time()
        p.reload()
        no = p.ev(PICK_JS, []); p.ev(OPEN_JS, no); uid = p.ev(UID_JS, no)
        p.ev(UNFOLD_JS); p.ev("(u)=>g3Sel(u,'c')", uid); p.wait(300)
        s1 = type_field(p, uid, WORD)
        fix1 = p.ev("()=>!!window.THEORY_FIX")
        p.wait(max(0, int(1500 - (time.time() - t0) * 1000)))
        for rt in held:
            try:
                rt.continue_()
            except Exception:
                pass
        p.wait(1000)
        fix2 = p.ev("()=>!!window.THEORY_FIX")
        s2 = type_field(p, uid, WORD)
        o = {'잡은 요청': len(held), '놓기 전 THEORY_FIX': fix1, '놓은 뒤': fix2, '앞 (3) 분리': pick3(s1)[0], '뒤 (3) 분리': pick3(s2)[0],
             '앞 (4) 충돌,2차원(고친 절에만)': pick3(s1)[1], '뒤 (4) 충돌,2차원': pick3(s2)[1],
             '놓기까지 초': round(time.time() - t0, 1), '오류': (p.errs or [])[:3]}
    finally:
        p.close()
    return o


# ══ 판정 ════════════════════════════════════════════════════════════════════════════════
def jG2(g):
    w = (g or {}).get('창') or {}
    return bool(g) and bool(g.get('ref T:')) and w.get('win') and w.get('n') == 1 and w.get('t3') and w.get('oth') is False and w.get('want') is not None \
        and w.get('kids') == w.get('want') and w.get('bs') == 'dashed' and (w.get('top') or -1) >= 0 and (w.get('bot') if w.get('bot') is not None else -1) >= 0


def jSTICK(g, sel):
    g = g or {}
    mv = g.get('창 옮김') or [0, 0]
    st = g.get('scrollTop') or [None, -1]
    return g.get('붙은 머리') == 1 and g.get('position') == 'sticky' and (abs(mv[0]) + abs(mv[1])) >= 100 and mv[1] > 0 and st[0] == st[1] and g.get('덮개') == [False, False]


def jIMG(g, touch=False):
    g = g or {}
    w = g.get('폭') or {}
    if not g.get('img') or g.get('aimg') != 0:
        return False
    if not touch:
        k = g.get('누름') or {}
        return k.get('주소 그대로') and k.get('새 창') == 0 and w.get('처음') and w.get('Ctrl+휠') and w['Ctrl+휠'] >= w['처음'] * 1.3 and w.get('두 번 누름') is not None and abs(w['두 번 누름'] - w['처음']) <= 2
    return w.get('처음') and w.get('두 손가락') and w['두 손가락'] > w['처음'] + 2 and (g.get('누름') or {}).get('새 창') == 0


def judge(o, ph, cd, g9, base=None):
    """→ {칸: (ok, 값)} · base = 바탕 흐름 값(G3 · G7 은 바탕과 맞댐)"""
    J = {}
    g1 = (o or {}).get('G1') or {}
    J['G1'] = (g1.get('(3) 분리') is not None and (g1.get('(4) 충돌,2차원') is None or g1['(3) 분리'] < g1['(4) 충돌,2차원']), g1)
    J['G2'] = (jG2((o or {}).get('G2')) and jG2((ph or {}).get('G2')), {'PC 마우스': (o or {}).get('G2'), '폰 손가락': (ph or {}).get('G2')})
    g3 = (o or {}).get('G3') or {}
    b3 = (base or {}).get('G3') if base else None
    same3 = (b3 is None) or (g3.get('글') == b3.get('글') and g3.get('쓰인 수') == b3.get('쓰인 수'))
    J['G3'] = (bool(g3.get('창')) and (g3['창'].get('점선') or 0) >= 1 and same3, {'새 판': g3, '바탕': b3})
    J['G4'] = (jSTICK((o or {}).get('G4'), '.thsec>h3'), (o or {}).get('G4'))
    J['G5'] = (jSTICK((o or {}).get('G5'), '.pwh'), (o or {}).get('G5'))
    def c6(g):
        g = g or {}
        if not g.get('img'):
            return {k: g.get(k) for k in ('win', 'aimg', 'img', 'n', '하네스 오류') if k in g}
        k, w = g.get('누름') or {}, g.get('폭') or {}
        return {'a새창그림': g.get('aimg'), '주소그대로': k.get('주소 그대로'), '새창': k.get('새 창'), '폭': list(w.values())}
    J['G6'] = (jIMG((o or {}).get('G6c')) and jIMG((o or {}).get('G6t')) and jIMG((o or {}).get('G6s')) and jIMG((ph or {}).get('G6c'), True),
               {'개념': c6((o or {}).get('G6c')), '이론': c6((o or {}).get('G6t')), '풀이 노트': c6((o or {}).get('G6s')), '폰 개념(두 손가락)': c6((ph or {}).get('G6c'))})
    g7 = (o or {}).get('G7') or {}
    b7 = (base or {}).get('G7') if base else None
    def mv(x):
        return (x or {}).get('d')
    keys = ('쓰인 문항 창', '서랍 근거 작은 창', '암기카드 창')
    if b7 is None:
        ok7 = all(mv(g7.get(k)) and (abs(mv(g7[k])[0]) + abs(mv(g7[k])[1])) > 0 for k in keys)
    else:
        ok7 = all(mv(g7.get(k)) is not None and mv(b7.get(k)) is not None and all(abs(a - b) <= 2 for a, b in zip(mv(g7[k]), mv(b7[k]))) for k in keys)
    J['G7'] = (ok7, {'새 판': {k: mv(g7.get(k)) for k in keys}, '바탕': {k: mv((b7 or {}).get(k)) for k in keys} if b7 is not None else None, '손잡이': {k: (g7.get(k) or {}).get('손잡이') for k in keys}})
    ok8, d8 = True, {}
    for subj in ('earth', 'bio'):
        x = (cd or {}).get(subj) or {}
        ok = (not x.get('오류')) and (x.get('목록') or {}).get('그려짐') and (x.get('목록') or {}).get('줄', 0) >= 1 and (x.get('근거') or {}).get('수', [0, 0])[1] == (x.get('근거') or {}).get('수', [0, 0])[0] + 1 \
            and (x.get('근거') or {}).get('칸 c') and '하네스 오류' not in x
        ok8 = ok8 and bool(ok); d8[subj] = x
    J['G8'] = (ok8, d8)
    g = g9 or {}
    J['G9'] = (g.get('잡은 요청', 0) >= 1 and g.get('놓기 전 THEORY_FIX') is False and g.get('놓은 뒤') is True and g.get('뒤 (3) 분리') is not None
               and g.get('앞 (4) 충돌,2차원(고친 절에만)') is None and g.get('뒤 (4) 충돌,2차원') is not None and not g.get('오류'), g)
    t = (o or {}).get('G10') or {}
    hs = {k: v for k, v in (t.get('첫 높이') or {}).items() if isinstance(v, dict)}
    ovs = list((t.get('넘침 0') or {}).values()) + [bool(((ph or {}).get('넘침') or {}).get('ok'))]
    J['G10'] = (not t.get('오류') and not (ph or {}).get('오류') and all(ovs) and all(v['ok'] for v in hs.values()), {'오류': t.get('오류'), '폰 오류': (ph or {}).get('오류'), '넘침 0': ovs, '첫 높이': hs})
    return J


NAMES = {
    'G1': '공식·개념 칸 「분리」 → 「1.3.8 (3) 분리」 블록 · 「(4) 충돌,2차원」 블록보다 앞',
    'G2': '그 블록 누름(마우스 · 손가락) → 근거 줄 → 줄 누름 → 쓰인 문항 창 .g3mk = 「(3) 분리」 줄만 · dashed · 창 안',
    'G3': '옛 근거(ref U:^ UNITS 1.3.8 (1) 블록) → 줄 글 · 쓰인 수 = 바탕 · 줄 누름 = 점선 테두리',
    'G4': '위 「개념」 창 30 % 굴림 → 맨 위 .thsec>h3 하나 sticky · 그 줄 (−200,+150) 끌기 = 창 움직임 · scrollTop 그대로 · 덮개 안 열림',
    'G5': '위 「공식」 창 · 같은 잣대(.pwh)',
    'G6': '개념 · 이론 · 옛 풀이 노트 그림 — a[target=_blank] img 0 · 누름 = 주소 그대로 · 새 창 0 · Ctrl+휠 4 칸 ≥ 1.3 배 · 두 번 누름 = 처음 폭(±2) · 폰 두 손가락 = 폭↑',
    'G7': '다른 창 무변 — 서랍 근거 작은 창 · 쓰인 문항 창 · 🃏 암기카드 창 손잡이 끌기 = 바탕과 같은 움직임',
    'G8': '지학 · 생물 근거 2 칸 글 찾기 → 페이지 오류 0 · 목록 그려짐 · 고르면 근거 들어감',
    'G9': 'theory_fix.json 늦게(route 잡아 둠 1.5 초) · 앞서 「분리」 한 번 → 늦게 온 뒤 다시 치면 「(3) 분리」(g3TBReset)',
    'G10': '위 화면 페이지 오류 0 · 가로 넘침 0 · 처음 뜬 새 창 높이 ≤ innerHeight/3(문항 본창 예외)',
}
SAME = {'G3', 'G7', 'G10'}   # 지시서 헛잣대 — 바탕도 PASS 여야 맞는 칸


def main():
    os.makedirs(TMPD, exist_ok=True)
    R('B0', '판 · 자리', None, None, {'NEW': NEWF, 'md5(LF)': {k: hashlib.md5(v.replace('\r\n', '\n').encode('utf-8')).hexdigest()[:8] for k, v in SRC.items()},
                                     'BASE': BASE if GATE else '(regress · smoke = 안 띄움)', 'theory_fix.json': h8(open(_roots.genie('jagwa', 'theory_fix.json'), encoding='utf-8').read()) if os.path.isfile(_roots.genie('jagwa', 'theory_fix.json')) else None,
                                     '엔진': ENGS})
    res, t0 = {}, time.time()
    vers = ['NEW'] + (['BASE'] if GATE else [])
    with sync_playwright() as pw:
        brs = {e: getattr(pw, e).launch() for e in (ENGS if not QC.SMOKE else ['chromium'])}
        for eng in brs:
            for ver in vers:
                QC.launch('base' if ver == 'BASE' else 'new')
                t1 = time.time()
                x = {}
                for k, fn in (('pc', flow_pc), ('ph', flow_phone), ('cd', flow_card), ('g9', flow_g9)):
                    if QC.SMOKE and k != 'pc':
                        continue
                    try:
                        x[k] = fn(brs[eng], eng, ver)
                    except Exception:
                        x[k] = {'하네스 오류': traceback.format_exc()[-700:]}
                res[(ver, eng)] = x
                R('B0', '%s %s 돎' % (ver, eng), None, None, '%.1f 분' % ((time.time() - t1) / 60))
        for b in brs.values():
            b.close()
    for eng in (ENGS if not QC.SMOKE else ['chromium']):
        n = res.get(('NEW', eng)) or {}
        b = res.get(('BASE', eng))
        jb = judge(b.get('pc'), b.get('ph'), b.get('cd'), b.get('g9'), base=b.get('pc')) if b else {}   # 바탕 G3 · G7 = 바탕 자신과 맞댐(바탕도 PASS 여야 할 칸 · 움직임 0 인 손잡이 없는 창 포함)
        bpc = (b or {}).get('pc') if b else None
        if not GATE:   # regress — G3 · G7 바탕 값 = 기준 스냅샷(앞 관문 판 값 · 없으면 이 판 값 = 무변)
            npc = n.get('pc') or {}
            bpc = {'G3': QC.base('G3@%s' % eng, npc.get('G3')), 'G7': QC.base('G7@%s' % eng, npc.get('G7'))}
        jn = judge(n.get('pc'), n.get('ph'), n.get('cd'), n.get('g9'), base=bpc)
        for c in NAMES:
            if not want(c):
                continue
            ok, d = jn[c]
            bb = jb.get(c) if jb else None
            R('%s[%s]' % (c, eng), NAMES[c], bool(ok), None if bb is None else bool(bb[0]), {'새 판': d, '바탕': bb[1]} if bb is not None else d, yard=(c not in SAME))
    newp = [x for x in RES if x['new'] is not None]
    yard = [x for x in RES if x['base'] is not None and x['yard']]
    same = [x for x in RES if x['base'] is not None and not x['yard']]
    R('B9', '합 — 새 판 PASS %d · FAIL %d · 헛잣대(새 칸 바탕 FAIL) %d/%d · 바탕도 같음 칸 바탕 PASS %d/%d · %.1f 분' % (
        sum(1 for x in newp if x['new']), sum(1 for x in newp if not x['new']), sum(1 for x in yard if not x['base']), len(yard),
        sum(1 for x in same if x['base']), len(same), (time.time() - t0) / 60), None)
    os.makedirs(os.path.dirname(os.path.abspath(OUTF)), exist_ok=True)
    with open(OUTF, 'w', encoding='utf-8') as f:
        for x in RES:
            tag = 'INFO' if x['new'] is None else ('PASS' if x['new'] else 'FAIL')
            yb = '' if x['base'] is None else (' · 바탕 ' + (('PASS(바탕도 같음)' if not x['yard'] else 'PASS') if x['base'] else ('FAIL' if x['yard'] else 'FAIL(바탕도 같아야 할 칸)')))
            f.write('%s | %s · %s%s | %s\n' % (tag, x['g'], x['name'], yb, _s(x['d'])[:700]))
    return 0 if newp and all(x['new'] for x in newp) else 1


if __name__ == '__main__':
    sys.exit(main())
