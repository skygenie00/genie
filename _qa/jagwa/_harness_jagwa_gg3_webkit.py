# -*- coding: utf-8 -*-
r"""_task_jagwa_gg3 §B-4 — 자과 물리 「근거 세 칸」 WebKit 터치 칸(로컬 몫 §L-1-2 · 클라우드엔 WebKit 이 없다)

  python _harness_jagwa_gg3_webkit.py [--mode gate|regress|smoke] [--new <앱 파일>] [--base <git 판 | 파일>] [--only W1,W2,..] [--dev 폰384,iPad820] [--res <결과>]

  NEW  = genie jagwa/index.html(GENIE_ROOT) · BASE = cab7b5a(LF md5 48330c0f · 패치 없음) = 헛잣대(gate 만)
  엔진 = WebKit 하나 · 기기 = 폰 384×740 · 아이패드 820×1180(hasTouch · DPR 2) · 데이터 = studyplandata 로컬 사본(JG Remote · PUT 은 안에 담김)
  누름 = 톡은 **진짜 터치**(page.touchscreen.tap) · 밀기 · 길게 누르기 · 흔들린 톡은 **합성**(Playwright WebKit 은 톡만 진짜 터치 · CDP 없음 = 도구 한계):
        누른 요소에 pointer(touch · 터치의 암묵 붙잡기처럼 같은 요소) 와 TouchEvent(못 만들면 Event + touches 값)를 실제 차례(down→start→(move→touchmove)…→up→end)로
        · iOS 유령 click 흉내 = 뗀 자리 요소에 click(W3 둘째 · W5 · W6)
  칸(§B-4):
    W1 서랍 손가락 밀기 — 접힘 → 화면 왼쪽 반에서 오른쪽 130px = 펴짐 · 펴진 서랍 줄에서 왼쪽 120px = 접힘 · 문항 안 열림
    W2 개념 창 덮개 밀기와 안 부딪힘 — 서랍 접고 개념 창(71) 오른쪽 덮개 · 덮개 오른쪽 밀기 = 덮개만 닫힘 · 본문 오른쪽 밀기 = 목차 덮개 · 서랍 그대로
    W3 접힌 손잡이 6px 흔들림 톡 = 펴짐(유령 click 없이 · 있이) · 진짜 톡 = 펴짐 · 문항 안 열림
    W4 서랍 줄 진짜 톡으로 65 연 뒤 ▾ 진짜 톡 한 번 = 근거 줄 한 번만 바뀜
    W5 OMR ④ 길게 누름(0.9 초) = 작은 정정 창(①~⑤ · 머리 줄 없음 · 높이 ≤ 1/3) · 채점 0(뒤따른 유령 click 포함) · 정정 창 ② 진짜 톡 = 저장 · 닫힘(뒤에 되돌림)
    W6 근거 줄 항목 길게 누름 = 그 자리 고치기 칸(글 = 그 항목 · ✓) · Esc = 그만(글 무변)
    W7 문맥 메뉴 0 — 길게 누르는 중 contextmenu 가 막힘(OMR 단추 · 근거 줄)
    W8 JS 오류 0
  헛잣대(gate · 바탕 cab7b5a) — W1 · W3 흔들림 · W5 · W7(OMR)이 옛 동작(못 펴짐 · 정정 창 없음 · 유령 click 에 채점 · 메뉴 안 막힘)인지 ·
    W2 · W4 · W6 · W7(근거 줄)은 바탕에 그 칸이 없다(새 칸 — 「바탕에 없음」).
  ⚠ 합성 밀기는 실기기의 pointercancel(브라우저가 굴림을 잡을 때) · 손가락 면적을 못 낸다 — 실기기 확인은 사용자 확인 줄(§C-6)에.
  ⚠ 자과앱 픽셀 게이트 없음(CLAUDE.md) — 값(클래스 · elementFromPoint · getBoundingClientRect · 기록 수)으로만 잰다.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기(Pg_PP · Remote · route_handler · TOOLS)
import hashlib, io, json, os, sys, tempfile, time   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEW = ARG('--new', _roots.genie('jagwa', 'index.html'))
BASE = ARG('--base', 'cab7b5a')
BASE_MD5 = '48330c0f4a4e3e503d1cf1f67de75545'   # cab7b5a jagwa/index.html(LF) — 지시서 머리 「바탕」
VENDOR = ARG('--vendor', os.path.join(tempfile.gettempdir(), 'h_jagwa', 'vendor'))
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_gg3_webkit_result.txt'))
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
DEVS_ALL = (('폰384', (384, 740)), ('iPad820', (820, 1180)))
DSEL = [x.strip() for x in (ARG('--dev', '') or '').split(',') if x.strip()]
JG.conf(VENDOR_PP=VENDOR)

RES = []


def T(dev, name, ok, detail=''):
    RES.append(('PASS' if ok else 'FAIL', dev, name))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('%s | WK[%s] %s | %s' % ('PASS' if ok else 'FAIL', dev, name, d[:700]), flush=True)
    return ok


def N(dev, name, detail=''):
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('INFO | WK[%s] %s | %s' % (dev, name, d[:900]), flush=True)


def want(k):
    return (not ONLY) or (k in ONLY)


_SYNCED = "()=>typeof recBusy!=='undefined'&&!recBusy&&(((lsObj(SMETA_KEY).lastSync||0)>=performance.timeOrigin)||!!recErr)"   # 앱 recBoot() 첫 syncRecords 끝

# ── 합성 손짓(WebKit) — 누른 요소에 pointer(touch) + TouchEvent 를 실제 차례로 ──
J_SYN = r"""
window.__G3W={how:null,
 sig(e){return e?(e.id?'#'+e.id:e.tagName.toLowerCase()+'.'+String(e.className&&e.className.baseVal!==undefined?e.className.baseVal:(e.className||'')).slice(0,30)):null},
 tev(type,t0,x,y,active){let ev=null;
  try{const tt=new Touch({identifier:11,target:t0,clientX:x,clientY:y,pageX:x+scrollX,pageY:y+scrollY,screenX:x,screenY:y,radiusX:11,radiusY:11,force:1});
   ev=new TouchEvent(type,{bubbles:true,cancelable:true,composed:true,touches:active?[tt]:[],targetTouches:active?[tt]:[],changedTouches:[tt]});if(!__G3W.how)__G3W.how='TouchEvent'}catch(e){ev=null}
  if(!ev){ev=new Event(type,{bubbles:true,cancelable:true,composed:true});
   const o={identifier:11,target:t0,clientX:x,clientY:y,pageX:x+scrollX,pageY:y+scrollY,screenX:x,screenY:y},L=active?[o]:[];
   Object.defineProperty(ev,'touches',{value:L});Object.defineProperty(ev,'targetTouches',{value:L});Object.defineProperty(ev,'changedTouches',{value:[o]});__G3W.how='Event+touches'}
  return ev},
 pe(type,x,y){return new PointerEvent(type,{bubbles:true,cancelable:true,composed:true,pointerId:21,pointerType:'touch',isPrimary:true,clientX:x,clientY:y,
  button:type==='pointermove'?-1:0,buttons:(type==='pointerup'||type==='pointercancel')?0:1,width:22,height:22,pressure:type==='pointerup'?0:0.5})},
 swipe([x0,y0,x1,y1,n,ghost]){const t0=document.elementFromPoint(x0,y0)||document.body;
  t0.dispatchEvent(__G3W.pe('pointerdown',x0,y0));t0.dispatchEvent(__G3W.tev('touchstart',t0,x0,y0,true));
  for(let i=1;i<=n;i++){const x=x0+(x1-x0)*i/n,y=y0+(y1-y0)*i/n;t0.dispatchEvent(__G3W.pe('pointermove',x,y));t0.dispatchEvent(__G3W.tev('touchmove',t0,x,y,true))}
  t0.dispatchEvent(__G3W.pe('pointerup',x1,y1));const te=__G3W.tev('touchend',t0,x1,y1,false);t0.dispatchEvent(te);
  let g=null;if(ghost&&!te.defaultPrevented){const el=document.elementFromPoint(x1,y1)||document.body;g=__G3W.sig(el);
   el.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,composed:true,clientX:x1,clientY:y1,detail:1}))}
  return {at:__G3W.sig(t0),how:__G3W.how,ghost:g}},
 lpDown([x,y]){const t0=document.elementFromPoint(x,y)||document.body;window.__lpT=t0;
  t0.dispatchEvent(__G3W.pe('pointerdown',x,y));t0.dispatchEvent(__G3W.tev('touchstart',t0,x,y,true));return {at:__G3W.sig(t0),how:__G3W.how}},
 lpCtx([x,y]){const t0=window.__lpT||document.elementFromPoint(x,y);const ev=new MouseEvent('contextmenu',{bubbles:true,cancelable:true,composed:true,clientX:x,clientY:y,button:2,buttons:0});
  t0.dispatchEvent(ev);let cs=null;try{const s=getComputedStyle(t0);cs={callout:s.webkitTouchCallout||s.getPropertyValue('-webkit-touch-callout')||null,select:s.webkitUserSelect||s.userSelect||null}}catch(e){}
  return {prevented:ev.defaultPrevented,at:__G3W.sig(t0),css:cs}},
 lpCtxAt([x,y]){const t0=document.elementFromPoint(x,y)||document.body;const ev=new MouseEvent('contextmenu',{bubbles:true,cancelable:true,composed:true,clientX:x,clientY:y,button:2,buttons:0});
  t0.dispatchEvent(ev);return {prevented:ev.defaultPrevented,at:__G3W.sig(t0)}},
 lpUp([x,y,ghost]){const t0=window.__lpT||document.elementFromPoint(x,y)||document.body;
  t0.dispatchEvent(__G3W.pe('pointerup',x,y));const te=__G3W.tev('touchend',t0,x,y,false);t0.dispatchEvent(te);
  let g=null;if(ghost&&!te.defaultPrevented){const el=document.elementFromPoint(x,y)||document.body;g=__G3W.sig(el);
   el.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,composed:true,clientX:x,clientY:y,detail:1}))}
  window.__lpT=null;return {ghost:g}}
};
"""

FOLD = "()=>{const d=document.getElementById('navdr');return !!d&&d.classList.contains('fold')}"
VIEWOPEN = "()=>!document.getElementById('view').classList.contains('hide')"
G3OFF = "()=>document.getElementById('view').classList.contains('g3off')"
SKIP = '#view,.sheet,.thcSide,.thcScrim,#pwl,.vpin,#g3Pop,#tyPop,#g3Af,input,textarea,select,canvas,#qink,#inkc,#ndGrip,.stage'   # 패치 #41 「안 받는 자리」 그대로
PICK_LEFT = r"""([W,H,skip])=>{for(let y=Math.round(H*0.72);y>Math.round(H*0.3);y-=20)for(let x=40;x<Math.round(W*0.45);x+=20){const e=document.elementFromPoint(x,y);
  if(e&&!(e.closest&&e.closest(skip)))return {x,y,at:__G3W.sig(e)}}return null}"""
ROWPT = r"""()=>{const d=document.getElementById('navdr');if(!d)return null;const dr=d.getBoundingClientRect();const rows=[...document.querySelectorAll('#ndList .ndrow')].filter(r=>{const b=r.getBoundingClientRect();return b.height>0&&b.top>dr.top+80&&b.bottom<Math.min(dr.bottom,innerHeight)-40});
  const r=rows[Math.floor(rows.length/2)];if(!r)return null;const b=r.getBoundingClientRect();const x=Math.round(Math.min(b.right-24,dr.left+dr.width*0.8)),y=Math.round(b.top+b.height/2);return {x,y,at:__G3W.sig(document.elementFromPoint(x,y)),no:r.dataset.no}}"""
GRIP = r"""()=>{const g=document.getElementById('ndGrip');if(!g)return null;const r=g.getBoundingClientRect();if(!r.height)return null;const x=Math.round(r.left+r.width/2),y=Math.round(r.top+Math.min(300,r.height/2));
  const a=document.elementFromPoint(x,y);return {x,y,w:Math.round(r.width),h:Math.round(r.height),on:!!a&&(a===g||g.contains(a)),at:__G3W.sig(a)}}"""
HITQ = r"""([sel,i])=>{const e=document.querySelectorAll(sel)[i||0];return e?__H.hit(e):null}"""
AFINFO = r"""()=>{const a=document.getElementById('g3Af');if(!a)return {n:0};const r=a.getBoundingClientRect();return {n:a.querySelectorAll('[data-af]').length,h:Math.round(r.height),ih:innerHeight,h2:!!a.querySelector('h2'),head:(a.querySelector('.afh')||{}).textContent||''}}"""


class Pg(JG.Pg_PP):
    """JG.Pg_PP(톡 = touchscreen.tap · 데이터 = Remote) — 부팅 뒤 고정 1.5 초 대신 표지(첫 syncRecords 끝) · 합성 손짓 도구 J_SYN"""

    def _ready(self):
        self.pg.wait_for_function(self.READY, timeout=90000)
        try:   # 물리 = 시험지 여섯(JG.Pg_PP._ready 와 같음)
            self.pg.wait_for_function(self.PDFS, timeout=180000)
        except Exception:
            pass
        QC.until(self.pg, _SYNCED, 8000, 'gg3_webkit 부팅 뒤 첫 syncRecords 끝(recBusy 거짓 · lastSync ≥ 쪽 열림 또는 recErr)')
        self.pg.evaluate(JG.TOOLS)
        self.pg.evaluate(J_SYN)


def page(br, tag, src, dev):
    QC.launch('base' if tag.startswith('B') else 'new')
    return Pg(br, 'webkit', tag, src, 'phys', dev, who='gg3wk')


def sleep(p, ms, why):
    QC.sleep(ms, why, p.pg)


# ════════════════ 칸마다 재기(R 에 값만 · 판정은 아래) ════════════════
def w1(p, R):
    W, H = p.dev
    p.ev('()=>{try{closeView()}catch(e){}ndResFold(true)}')
    sleep(p, 700, '서랍 깜박 막이(편 직후 0.6 초 접지 않음) 넘김')
    R['w1_fold0'] = p.ev(FOLD)
    pt = p.ev(PICK_LEFT, [W, H, SKIP])
    R['w1_pt'] = pt
    if not pt:
        return
    R['w1_ev1'] = p.ev('a=>__G3W.swipe(a)', [pt['x'], pt['y'], pt['x'] + 130, pt['y'] + 6, 8, False])
    sleep(p, 400, '밀기 뒤 접기·펴기 반영')
    R['w1_open'] = not p.ev(FOLD)
    R['w1_view1'] = p.ev(VIEWOPEN)
    sleep(p, 700, '서랍 깜박 막이(편 직후 0.6 초 접지 않음) 넘김')
    rp = p.ev(ROWPT)
    R['w1_row'] = rp
    if rp and R['w1_open']:
        R['w1_ev2'] = p.ev('a=>__G3W.swipe(a)', [rp['x'], rp['y'], rp['x'] - 120, rp['y'] + 4, 8, False])
        sleep(p, 400, '밀기 뒤 접기·펴기 반영')
        R['w1_close'] = p.ev(FOLD)
        R['w1_view2'] = p.ev(VIEWOPEN)
    p.ev('()=>{try{closeView()}catch(e){}ndResFold(false)}')


def w3(p, R):
    p.ev('()=>{try{closeView()}catch(e){}ndResFold(true)}')
    sleep(p, 700, '서랍 깜박 막이 넘김')
    g = p.ev(GRIP)
    R['w3_grip'] = g
    if not g:
        return
    R['w3_ev1'] = p.ev('a=>__G3W.swipe(a)', [g['x'], g['y'], g['x'] + 6, g['y'], 1, False])
    sleep(p, 700, '손잡이 톡 뒤 펴기 반영')
    R['w3_jit'] = not p.ev(FOLD)
    R['w3_view1'] = p.ev(VIEWOPEN)
    p.ev('()=>ndResFold(true)')
    sleep(p, 700, '서랍 깜박 막이 넘김')
    g = p.ev(GRIP) or g
    R['w3_ev2'] = p.ev('a=>__G3W.swipe(a)', [g['x'], g['y'], g['x'] + 6, g['y'], 1, True])
    sleep(p, 1000, '유령 click 뒤 서랍 막이(0.6 초) · 다시 접히는지 볼 틈')
    R['w3_jitg'] = not p.ev(FOLD)
    R['w3_view2'] = p.ev(VIEWOPEN)
    p.ev('()=>ndResFold(true)')
    sleep(p, 700, '서랍 깜박 막이 넘김')
    g = p.ev(GRIP) or g
    p.tap(g['x'], g['y'], wait=0)
    sleep(p, 1000, '진짜 톡 뒤 터치 대체 누르기(60ms) · 유령 click 틈')
    R['w3_tap'] = not p.ev(FOLD)
    R['w3_view3'] = p.ev(VIEWOPEN)
    p.ev('()=>{try{closeView()}catch(e){}ndResFold(false)}')


def w2(p, R):
    W, H = p.dev
    p.ev('()=>{try{closeView()}catch(e){}ndResFold(true)}')
    sleep(p, 700, '서랍 깜박 막이 넘김')
    R['w2_set'] = p.ev(r"""()=>{const r=rec(71);if(!r)return 'no-rec';const cs=conceptsOf(r);if(!cs||!cs.length)return 'no-concept';conceptSheet(cs[0].k,r);
      const s=document.getElementById('sh-concept');if(!s)return 'no-sheet';if(!s.__g3cwOpen)return 'no-open';s.__g3cwOpen('R');return 'ok'}""")
    if R['w2_set'] != 'ok':
        return
    QC.until(p.pg, "()=>{const s=document.getElementById('sh-concept');return !!s&&s.classList.contains('thcOnR')}", 4000, 'W2 개념 창 오른쪽 덮개 열림')
    QC.until(p.pg, "()=>{const R=document.querySelector('#sh-concept .thcR');if(!R)return false;const b=R.getBoundingClientRect();return b.width>0&&b.left>=0&&b.right<=innerWidth+1}", 3000, 'W2 덮개가 화면 안에 자리 잡음(판이 makeFloat 로 자리 잡은 뒤 · 열자마자 재면 옛 판 폭 기준 자리)')
    c = p.ev(r"""()=>{const s=document.getElementById('sh-concept'),R=s&&s.querySelector('.thcR');if(!R)return null;const r=R.getBoundingClientRect();
      const x=Math.round(r.left+10),y=Math.round(r.top+r.height/2),a=document.elementFromPoint(x,y);return {x,y,on:!!a&&R.contains(a),at:__G3W.sig(a),onR:s.classList.contains('thcOnR')}}""")
    R['w2_cover'] = c
    if not c or not c.get('on'):
        return
    R['w2_ev1'] = p.ev('a=>__G3W.swipe(a)', [c['x'], c['y'], c['x'] + 120, c['y'] + 4, 8, False])
    sleep(p, 500, '덮개 밀기 뒤 반영')
    R['w2_coverClosed'] = p.ev("()=>{const s=document.getElementById('sh-concept');return !!s&&!s.classList.contains('thcOnR')}")
    R['w2_fold1'] = p.ev(FOLD)
    b = p.ev(r"""([W])=>{const s=document.getElementById('sh-concept'),P=s&&s.querySelector('.panel');if(!P)return null;const r=P.getBoundingClientRect();
      for(let y=Math.round(r.top+r.height*0.55);y<r.bottom-10;y+=16)for(let x=Math.round(Math.max(r.left+16,8));x<Math.min(r.right-130,W*0.48);x+=12){const a=document.elementFromPoint(x,y);
        if(a&&P.contains(a)&&!a.closest('button,a,input,textarea,.thcSide,.thcScrim'))return {x,y,at:__G3W.sig(a)}}
      const x=Math.round(r.left+16),y=Math.round(r.top+r.height*0.6),a=document.elementFromPoint(x,y);return {x,y,at:__G3W.sig(a),fallback:true}}""", [W])
    R['w2_body'] = b
    if b:
        R['w2_ev2'] = p.ev('a=>__G3W.swipe(a)', [b['x'], b['y'], b['x'] + 120, b['y'] + 4, 8, False])
        sleep(p, 500, '본문 밀기 뒤 반영')
        R['w2_toc'] = p.ev("()=>{const s=document.getElementById('sh-concept');return !!s&&s.classList.contains('thcOnL')}")
        R['w2_fold2'] = p.ev(FOLD)
    p.ev("()=>{const s=document.getElementById('sh-concept');if(s)s.remove();ndResFold(false)}")


def open65(p, R, pre):
    """서랍 줄(65 제목 칸 .ndt)을 진짜 톡 → 65 본창"""
    p.ev('()=>{try{closeView()}catch(e){}ndResFold(false)}')
    sleep(p, 700, '서랍 깜박 막이 넘김')
    a = p.ev(HITQ, ['#ndList .ndrow[data-no="65"] .ndt', 0])
    R[pre + '_row'] = a
    if not a or not a.get('on'):
        return False
    p.tap(a['cx'], a['cy'], wait=0)
    ok = QC.until(p.pg, "()=>typeof VNO!=='undefined'&&VNO===65&&!document.getElementById('view').classList.contains('hide')", 10000, '서랍 줄 톡 → 65 본창')
    R[pre + '_open'] = ok
    QC.until(p.pg, "()=>typeof window.G3!=='object'||(!!document.getElementById('g3Fold')&&!!document.querySelector('#view .g3list,#view #ggphys'))", 20000, '본창 g3 근거 줄(▾ · 항목 줄) 섬 — 바탕은 g3 없음이라 곧바로 · 부팅 뒤 첫 열기는 시험지 그리기 뒤라 짐 클 때 13 초(10/9 20:1x 잼)')
    sleep(p, 300, '본창 그리기 끝(표지 뒤 여유)')
    return ok


def w4(p, R):
    if not open65(p, R, 'w4'):
        return
    R['w4_has'] = p.ev("()=>!!document.getElementById('g3Fold')")
    if not R['w4_has']:
        return
    R['w4_off0'] = p.ev(G3OFF)
    f = p.ev(HITQ, ['#g3Fold', 0])
    R['w4_btn'] = f
    if not f or not f.get('on'):
        return
    p.tap(f['cx'], f['cy'], wait=0)
    sleep(p, 1500, '터치 대체 누르기 타이머(60ms) · 무거운 다시 그리기 뒤 겹누름이 날 틈(v52)')
    R['w4_off1'] = p.ev(G3OFF)


def w5(p, R):
    if not p.ev(VIEWOPEN):
        if not open65(p, R, 'w5'):
            return
    R['w5_no'] = p.ev('()=>VNO')
    R['w5_h0'] = p.ev('()=>hist(VNO).length')
    b = p.ev(HITQ, ['#omrPad button[data-omr]', 3])
    R['w5_btn'] = b
    if not b or not b.get('on'):
        return
    R['w5_down'] = p.ev('a=>__G3W.lpDown(a)', [b['cx'], b['cy']])
    sleep(p, 300, '누르는 중 문맥 메뉴(문턱 0.55 초 전 · 같은 요소)')
    R['w7a0'] = p.ev('a=>__G3W.lpCtx(a)', [b['cx'], b['cy']])
    sleep(p, 600, '길게 누르기 문턱 0.55 초(앱 타이머) + 여유(짐 클 때 경합 · 10/8 900ms)')
    R['w7a'] = p.ev('a=>__G3W.lpCtxAt(a)', [b['cx'], b['cy']])   # 길게 누름 뒤 그 자리 맨 위 요소(창이 바뀌었으면 그 요소)
    R['w5_up'] = p.ev('a=>__G3W.lpUp(a)', [b['cx'], b['cy'], True])
    sleep(p, 900, '뗀 뒤 유령 click · 채점 반영 틈')
    R['w5_af'] = p.ev(AFINFO)
    R['w5_h1'] = p.ev('()=>hist(VNO).length')
    if (R['w5_af'] or {}).get('n'):
        a2 = p.ev(HITQ, ['#g3Af [data-af]', 1])
        R['w5_a2'] = a2
        if a2 and a2.get('on'):
            R['w5_af0'] = p.ev("()=>(AFIX||{})[qk(VNO)]||null")
            p.tap(a2['cx'], a2['cy'], wait=0)
            QC.until(p.pg, "()=>!document.getElementById('g3Af')", 5000, 'W5 정정 창 ② 톡 → 닫힘')
            sleep(p, 600, '정정 저장(put kv) 뒤')
            R['w5_fix'] = p.ev("()=>(AFIX||{})[qk(VNO)]||null")
            R['w5_closed'] = p.ev("()=>!document.getElementById('g3Af')")
            R['w5_h2'] = p.ev('()=>hist(VNO).length')
            p.ev("async a0=>{if(a0)AFIX[qk(VNO)]=a0;else delete AFIX[qk(VNO)];await put('kv','ansfix',AFIX);syncOmr()}", R.get('w5_af0'))   # 되돌림


def w6(p, R):
    if not p.ev(VIEWOPEN):
        if not open65(p, R, 'w6'):
            return
    if not p.ev("()=>!!document.getElementById('g3Fold')"):
        R['w6_skip'] = '▾ 없음(바탕)'
        return
    if p.ev(G3OFF):
        f = p.ev(HITQ, ['#g3Fold', 0])
        if f and f.get('on'):
            p.tap(f['cx'], f['cy'], wait=0)
            sleep(p, 1200, '근거 줄 펴기')
    sel = "#view .g3list .g3r[data-g3k][data-f=\"t\"] .g3tx, #view .g3list .g3r[data-g3k][data-f=\"w\"] .g3tx"
    if not p.ev('s=>!!document.querySelector(s)', sel):
        R['w6_seed'] = p.ev("async()=>{await G3.push('P065','t',{t:'시험 트리거 gg3wk'});return !!document.querySelector('#view .g3list .g3r[data-f=\"t\"]')}")
        sleep(p, 600, '심은 항목 그리기')
    t = p.ev(HITQ, [sel, 0])
    R['w6_tx'] = t
    if not t or not t.get('on'):
        return
    R['w6_key'] = p.ev("s=>{const e=document.querySelector(s);const r=e&&e.closest('.g3r');return r?r.getAttribute('data-g3k'):null}", sel)
    R['w6_down'] = p.ev('a=>__G3W.lpDown(a)', [t['cx'], t['cy']])
    sleep(p, 300, '누르는 중 문맥 메뉴(문턱 0.55 초 전 · 같은 요소)')
    R['w7b0'] = p.ev('a=>__G3W.lpCtx(a)', [t['cx'], t['cy']])
    sleep(p, 600, '길게 누르기 문턱 0.55 초 + 여유')
    R['w7b'] = p.ev('a=>__G3W.lpCtxAt(a)', [t['cx'], t['cy']])   # 길게 누름 뒤 그 자리 맨 위 요소(글 → 고치기 칸으로 갈렸으면 그 칸)
    R['w6_up'] = p.ev('a=>__G3W.lpUp(a)', [t['cx'], t['cy'], True])
    sleep(p, 600, '뗀 뒤 유령 click 틈')
    R['w6_ed'] = p.ev(r"""(k)=>{const ed=document.querySelector('#view .g3list .g3r .g3ed');if(!ed)return {ed:false};const ta=ed.querySelector('textarea');const a=String(k||'').split('|');
      let same=null;try{same=ta.value===ggFlat(ggItem(a[0],a[1]))}catch(e){same='exc '+e.message}
      return {ed:true,ok:!!ed.querySelector('.g3ok'),same,focus:document.activeElement===ta,len:ta.value.length}}""", R['w6_key'])
    R['w6_t0'] = p.ev("k=>{const a=String(k||'').split('|');try{return ggFlat(ggItem(a[0],a[1]))}catch(e){return null}}", R['w6_key'])
    if (R['w6_ed'] or {}).get('ed'):
        if not R['w6_ed'].get('focus'):
            p.ev("()=>{const t=document.querySelector('#view .g3list .g3ed textarea');if(t)t.focus()}")
        p.pg.keyboard.press('Escape')
        sleep(p, 500, 'Esc 뒤 다시 그리기')
        R['w6_esc'] = p.ev("()=>!document.querySelector('#view .g3list .g3ed')")
        R['w6_t1'] = p.ev("k=>{const a=String(k||'').split('|');try{return ggFlat(ggItem(a[0],a[1]))}catch(e){return null}}", R['w6_key'])


def errs(p):
    return (p.errs or [])[:6] + (p.ev('()=>(window.__err||[]).slice(0,6)') or [])


def run_dev(br, dn, dev, src_new, src_base):
    """한 기기 — NEW(전 칸) · BASE(gate · 헛잣대 칸)"""
    out = {}
    for tag, src in (('N', src_new), ('B', src_base)):
        if src is None:
            continue
        R = {}
        t0 = time.time()
        try:
            p = page(br, tag + dn, src, dev)
        except Exception as e:
            out[tag] = {'boot': 'NG ' + str(e)[:200]}
            continue
        R['boot'] = 'ok'
        steps = [('W1', w1), ('W3', w3)]
        if tag == 'N':
            steps += [('W2', w2), ('W4', w4), ('W5', w5), ('W6', w6)]
        else:
            steps += [('W5', w5)]
        if QC.SMOKE:
            steps = [s for s in steps if s[0] in ('W1', 'W5')]
        for k, fn in steps:
            if not want(k) and not (k == 'W5' and want('W7')) and not (k == 'W6' and want('W7')):
                continue
            try:
                fn(p, R)
            except Exception as e:
                R[k.lower() + '_exc'] = str(e)[:240]
        R['how'] = p.ev('()=>window.__G3W&&__G3W.how')
        R['err'] = errs(p)
        R['sec'] = round(time.time() - t0, 1)
        p.close()
        out[tag] = R
    return out


def judge(dn, n, o):
    """n = 새 판 값 · o = 바탕 값(gate) — 칸마다 PASS/FAIL · 헛잣대"""
    if n.get('boot') != 'ok':
        T(dn, '부팅(새 판)', False, n)
        return
    N(dn, '합성 손짓 꼴 · 걸린 초', {'how': n.get('how'), 'sec': n.get('sec')})
    if want('W1'):
        T(dn, 'W1-a 서랍 접힘 → 화면 왼쪽 반에서 오른쪽 손가락 밀기 = 펴짐 · 문항 안 열림',
          n.get('w1_fold0') is True and n.get('w1_open') is True and n.get('w1_view1') is False,
          {k: n.get(k) for k in ('w1_fold0', 'w1_pt', 'w1_ev1', 'w1_open', 'w1_view1', 'w1_exc')})
        if not QC.SMOKE:
            T(dn, 'W1-b 펴진 서랍 줄에서 왼쪽 손가락 밀기 = 접힘 · 문항 안 열림',
              n.get('w1_close') is True and n.get('w1_view2') is False,
              {k: n.get(k) for k in ('w1_row', 'w1_ev2', 'w1_close', 'w1_view2')})
        if QC.GATE and o:
            T(dn, '★헛잣대 W1 — 바탕은 같은 밀기에 서랍이 안 펴진다(밀기 없음)', o.get('w1_fold0') is True and o.get('w1_open') is False,
              {k: o.get(k) for k in ('w1_fold0', 'w1_pt', 'w1_ev1', 'w1_open', 'w1_exc')})
    if want('W2') and not QC.SMOKE:
        T(dn, 'W2-a 개념 창(71) 오른쪽 덮개를 오른쪽으로 밀기 = 덮개만 닫힘 · 서랍 접힌 그대로',
          n.get('w2_set') == 'ok' and n.get('w2_coverClosed') is True and n.get('w2_fold1') is True,
          {k: n.get(k) for k in ('w2_set', 'w2_cover', 'w2_ev1', 'w2_coverClosed', 'w2_fold1', 'w2_exc')})
        T(dn, 'W2-b 개념 창 본문을 오른쪽으로 밀기 = 목차 덮개 · 서랍 접힌 그대로',
          n.get('w2_toc') is True and n.get('w2_fold2') is True,
          {k: n.get(k) for k in ('w2_body', 'w2_ev2', 'w2_toc', 'w2_fold2')})
        c, b = n.get('w2_cover') or {}, n.get('w2_body') or {}
        W = dict(DEVS_ALL)[dn][0]
        N(dn, 'W2 밀기 시작 자리가 서랍 밀기 자리(화면 왼쪽 반)인가 — 아니면 그 칸의 「서랍 그대로」 는 서랍 쪽에서 거저 참',
          {'덮개 x0': c.get('x'), '본문 x0': b.get('x'), 'W/2': W / 2.0,
           '덮개 왼쪽 반': (c.get('x') or 9999) < W / 2.0, '본문 왼쪽 반': (b.get('x') or 9999) < W / 2.0})
        if QC.GATE:
            N(dn, 'W2 바탕 — 덮개 밀기 칸 없음(개념 창 덮개 = 이 판 새 칸)', '바탕에 없음')
    if want('W3') and not QC.SMOKE:
        T(dn, 'W3-a 접힌 손잡이 6px 흔들림 톡 = 펴짐 · 문항 안 열림', n.get('w3_jit') is True and n.get('w3_view1') is False,
          {k: n.get(k) for k in ('w3_grip', 'w3_ev1', 'w3_jit', 'w3_view1', 'w3_exc')})
        T(dn, 'W3-b 흔들림 톡 + 뗀 자리 유령 click = 펴진 채(다시 안 접힘) · 문항 안 열림', n.get('w3_jitg') is True and n.get('w3_view2') is False,
          {k: n.get(k) for k in ('w3_ev2', 'w3_jitg', 'w3_view2')})
        T(dn, 'W3-c 접힌 손잡이 진짜 톡 = 펴짐 · 문항 안 열림', n.get('w3_tap') is True and n.get('w3_view3') is False,
          {k: n.get(k) for k in ('w3_tap', 'w3_view3')})
        if QC.GATE and o:
            T(dn, '★헛잣대 W3 — 바탕은 6px 흔들림 톡에 안 펴진다(끌기로 침)', o.get('w3_jit') is False,
              {k: o.get(k) for k in ('w3_grip', 'w3_ev1', 'w3_jit', 'w3_exc')})
            N(dn, 'W3 바탕 진짜 톡(바탕도 같음 기대)', {k: o.get(k) for k in ('w3_tap', 'w3_view3', 'w3_jitg')})
    if want('W4') and not QC.SMOKE:
        T(dn, 'W4 서랍 줄 진짜 톡으로 65 연 뒤 ▾ 진짜 톡 한 번 = 근거 줄 한 번만 바뀜',
          n.get('w4_open') is True and n.get('w4_has') is True and n.get('w4_off1') is not None and n.get('w4_off1') == (not n.get('w4_off0')),
          {k: n.get(k) for k in ('w4_row', 'w4_open', 'w4_has', 'w4_btn', 'w4_off0', 'w4_off1', 'w4_exc')})
        if QC.GATE:
            N(dn, 'W4 바탕 — ▾(#g3Fold) 없음(이 판 새 칸)', '바탕에 없음')
    if want('W5') or want('W7'):
        af = n.get('w5_af') or {}
        T(dn, 'W5-a OMR ④ 길게 누름 = 작은 정정 창(①~⑤ · 머리 줄 없음 · 높이 ≤ 화면 1/3)',
          af.get('n') == 5 and not af.get('h2') and (af.get('h') or 9999) <= (af.get('ih') or 0) / 3.0,
          {k: n.get(k) for k in ('w5_no', 'w5_btn', 'w5_down', 'w5_af', 'w5_exc')})
        T(dn, 'W5-b 길게 누름 · 뗀 뒤 유령 click 에도 채점 0(기록 수 그대로)',
          n.get('w5_h0') is not None and n.get('w5_h1') == n.get('w5_h0'),
          {k: n.get(k) for k in ('w5_h0', 'w5_h1', 'w5_up')})
        if not QC.SMOKE:
            T(dn, 'W5-c 정정 창 ② 진짜 톡 = 정답 ② 저장 · 창 닫힘 · 채점 0(뒤에 되돌림)',
              n.get('w5_fix') == '②' and n.get('w5_closed') is True and n.get('w5_h2') == n.get('w5_h0'),
              {k: n.get(k) for k in ('w5_a2', 'w5_af0', 'w5_fix', 'w5_closed', 'w5_h2')})
        T(dn, 'W7-a OMR 단추 길게 누르는 중 문맥 메뉴 막힘(contextmenu preventDefault)', (n.get('w7a') or {}).get('prevented') is True and (n.get('w7a0') or {}).get('prevented') is True, {'누르는 중': n.get('w7a0'), '길게 누름 뒤': n.get('w7a')})
        if QC.GATE and o:
            oa = o.get('w5_af') or {}
            T(dn, '★헛잣대 W5 — 바탕은 길게 눌러도 정정 창이 없고 뗀 뒤 유령 click 에 채점된다',
              oa.get('n', 0) == 0 and o.get('w5_h0') is not None and (o.get('w5_h1') or 0) == o.get('w5_h0') + 1,
              {k: o.get(k) for k in ('w5_no', 'w5_btn', 'w5_af', 'w5_h0', 'w5_h1', 'w5_up', 'w5_exc', 'w5_row', 'w5_open')})
            T(dn, '★헛잣대 W7 — 바탕 OMR 단추는 문맥 메뉴를 안 막는다', (o.get('w7a') or {}).get('prevented') is False and (o.get('w7a0') or {}).get('prevented') is False, {'누르는 중': o.get('w7a0'), '길게 누름 뒤': o.get('w7a')})
    if (want('W6') or want('W7')) and not QC.SMOKE:
        ed = n.get('w6_ed') or {}
        T(dn, 'W6-a 근거 줄 항목 길게 누름 = 그 자리 고치기 칸(글 = 그 항목 · ✓)',
          ed.get('ed') is True and ed.get('ok') is True and ed.get('same') is True,
          {k: n.get(k) for k in ('w6_seed', 'w6_tx', 'w6_key', 'w6_down', 'w6_ed', 'w6_skip', 'w6_exc')})
        T(dn, 'W6-b 고치기 칸 Esc = 닫힘 · 글 무변', n.get('w6_esc') is True and n.get('w6_t1') == n.get('w6_t0'),
          {k: n.get(k) for k in ('w6_esc', 'w6_t0', 'w6_t1')})
        T(dn, 'W7-b 근거 줄 길게 누르는 중 문맥 메뉴 막힘', (n.get('w7b') or {}).get('prevented') is True and (n.get('w7b0') or {}).get('prevented') is True, {'누르는 중': n.get('w7b0'), '길게 누름 뒤': n.get('w7b')})
        if QC.GATE:
            N(dn, 'W6 · W7-b 바탕 — 근거 줄 항목(.g3list) 없음(이 판 새 칸)', '바탕에 없음')
    T(dn, 'W8 JS 오류 0(새 판)', not n.get('err'), n.get('err'))


def main():
    t_all = time.time()
    src_new = io.open(NEW, encoding='utf-8', newline='').read()
    src_base = None
    if QC.GATE:
        QC.sub('git:show-app')
        src_base = JG.app_src(BASE)
        m = hashlib.md5(src_base.replace('\r\n', '\n').encode('utf-8')).hexdigest()
        if BASE == 'cab7b5a' and m != BASE_MD5:
            raise SystemExit('바탕 앱 md5 가 다르다: %s ≠ %s' % (m, BASE_MD5))
        if hashlib.md5(src_new.replace('\r\n', '\n').encode('utf-8')).hexdigest() == m:
            print('INFO | 새 판 = 바탕(같은 글) — 헛잣대만 뜻이 있다', flush=True)
    devs = [d for d in DEVS_ALL if (not DSEL or d[0] in DSEL)]
    if QC.SMOKE:
        devs = devs[:1]
    from playwright.sync_api import sync_playwright
    D = {}
    with sync_playwright() as pw:
        br = pw.webkit.launch()
        try:
            for dn, dev in devs:
                print('… %s' % dn, flush=True)
                D[dn] = run_dev(br, dn, dev, src_new, src_base)
        finally:
            br.close()
    for dn, dev in devs:
        judge(dn, D[dn].get('N') or {}, D[dn].get('B') if QC.GATE else None)
    p = sum(1 for x in RES if x[0] == 'PASS')
    f = sum(1 for x in RES if x[0] == 'FAIL')
    tail = '\n합계  PASS %d · FAIL %d · %.1f 분 · mode %s' % (p, f, (time.time() - t_all) / 60, QC.MODE)
    print(tail, flush=True)
    try:
        raw = os.path.join(tempfile.gettempdir(), 'h_gg3wk')
        os.makedirs(raw, exist_ok=True)
        json.dump(D, io.open(os.path.join(raw, 'raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
        io.open(OUTF, 'w', encoding='utf-8').write('\n'.join('%s | WK[%s] %s' % x for x in RES) + '\n' + tail + '\n')
    except Exception as e:
        print('INFO | 결과 파일 못 씀 | %s' % e, flush=True)
    sys.exit(0 if not f else 1)


if __name__ == '__main__':
    main()
