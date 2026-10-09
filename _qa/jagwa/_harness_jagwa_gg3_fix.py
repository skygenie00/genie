# -*- coding: utf-8 -*-
r"""_task_jagwa_gg3 앱 결함 고침 ①② 관문 — 사용자 10/9 19:17(Code 창) · 결정로그 19:05 · 19:12 [채팅] 관문 그대로

  python _harness_jagwa_gg3_fix.py [--mode gate|regress|smoke] [--new <고친 앱>] [--base <git 판 | 파일>] [--eng chromium,webkit] [--res <결과>]

  세 판: BASE = cab7b5a(LF 48330c0f · 패치 없음) · P42 = BASE 에 `jagwa\gg3\patches_gg3.json` 42 를 넣어 이 안에서 지은 판(시안 v57 · 고치기 전) · NEW = 고친 판(GENIE_ROOT jagwa/index.html)
  ① 머리 줄 CSS 는 물리에만 — 지학 · 생물 문항 창 머리(.vtop · 그 자식 · .t1 · .t2)의 계산 스타일(배치 값 빼고) NEW = BASE · 물리 NEW = P42(:where 특이도 0)
     헛잣대: 지학 · 생물 P42 ≠ BASE(샘) · PC 1100×800(fine) + 폰 384×740(coarse) · Chromium
  ② 폰 접힌 손잡이 30px 걷음 — 폰 384×740 · 세 과목 · 서랍 접힘 · 첫 화면:
     F2-a ▾(#fFoldBtn) 가운데 진짜 톡 = 머리 펼침(body.fold 바뀜) · 서랍 접힌 그대로
     F2-b ▾ 누름 자리 ≥ 36×36(elementFromPoint 훑기) · = BASE(revfix0929 A-6)
     F2-c 접힌 서랍 = 화면 왼쪽 반에서 오른쪽 130px 밀기 = 펴짐(v56 · v57) · 문항 안 열림
     F2-d 13px 손잡이(#ndGrip 보이는 띠 가운데) 진짜 톡 = 펴짐 · 문항 안 열림
     헛잣대(gate · Chromium): P42 = ▾ 가운데 톡이 서랍을 엶 · 누름 자리 < 36 / BASE = 밀기 없음(안 펴짐)
     톡 = Chromium CDP 진짜 터치 · WebKit touchscreen.tap · 밀기 = Chromium CDP touchMove(진짜) · WebKit 합성(pointer + TouchEvent · 도구 한계)
  모드: gate = 세 판 · regress = NEW 만(① 지학 · 생물 기준 = 스냅샷 · 물리 = P42 맞대기는 관문만) · smoke = NEW Chromium 폰 지학 ① · F2-a
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
BASE_MD5 = '48330c0f4a4e3e503d1cf1f67de75545'   # cab7b5a jagwa/index.html(LF)
PATCHES = os.path.join(HERE, 'gg3', 'patches_gg3.json')   # 패치 42(N: jagwa\gg3\ · genie _qa 사본에서도 같은 자리)
VENDOR = ARG('--vendor', os.path.join(tempfile.gettempdir(), 'h_jagwa', 'vendor'))
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_gg3_fix_result.txt'))
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
JG.conf(VENDOR_PP=VENDOR)
PHONE = (384, 740)
PCD = (1100, 800)
RES = []


def T(g, name, ok, detail=''):
    RES.append(('PASS' if ok else 'FAIL', g, name))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('%s | %s %s | %s' % ('PASS' if ok else 'FAIL', g, name, d[:700]), flush=True)
    return ok


def N(g, name, detail=''):
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('INFO | %s %s | %s' % (g, name, d[:900]), flush=True)


_SYNCED = "()=>typeof recBusy!=='undefined'&&!recBusy&&(((lsObj(SMETA_KEY).lastSync||0)>=performance.timeOrigin)||!!recErr)"

# 머리 계산 스타일(배치에 따라 바뀌는 높이 · 폭은 뺌 — 창 폭이 1/2 로 바뀌어 제목이 감기는 것과 가름)
HDR = r"""()=>{const v=document.querySelector('#view .vtop');if(!v)return null;
 const P=['display','min-height','padding-top','padding-bottom','padding-left','padding-right','row-gap','column-gap','background-color','background-image',
   'border-top-width','border-top-style','box-shadow','font-size','font-weight','line-height','min-width','color','border-radius','flex-direction','justify-content'];
 const pick=e=>{const s=getComputedStyle(e);return P.map(k=>k+':'+s.getPropertyValue(k)).join(';')};
 const key=c=>c.id?'#'+c.id:'.'+(String(c.className||'').split(' ')[0]||c.tagName.toLowerCase());
 const o={'.vtop':pick(v)};
 [...v.children].forEach(c=>{const k=key(c);o[k]=getComputedStyle(c).display==='none'?'display:none':pick(c)});
 ['.t1','.t2'].forEach(q=>{const e=v.querySelector(q);if(e)o[q]=getComputedStyle(e).display==='none'?'display:none':pick(e)});
 return o}"""
OPEN1 = "async()=>{try{closeView()}catch(e){}const r=DATA.find(x=>x&&x[F.NO]);await openView(r[F.NO]);return r[F.NO]}"
FOLD = "()=>{const d=document.getElementById('navdr');return !!d&&d.classList.contains('fold')}"
BFOLD = "()=>document.body.classList.contains('fold')"
VIEWOPEN = "()=>!document.getElementById('view').classList.contains('hide')"
SKIP = '#view,.sheet,.thcSide,.thcScrim,#pwl,.vpin,#g3Pop,#tyPop,#g3Af,input,textarea,select,canvas,#qink,#inkc,#ndGrip,.stage'   # 패치 #41 「안 받는 자리」 그대로
PICK_LEFT = r"""([W,H,skip])=>{for(let y=Math.round(H*0.72);y>Math.round(H*0.3);y-=20)for(let x=40;x<Math.round(W*0.45);x+=20){const e=document.elementFromPoint(x,y);
  if(e&&!(e.closest&&e.closest(skip)))return {x,y,at:e.id?'#'+e.id:e.tagName.toLowerCase()+'.'+String(e.className||'').slice(0,24)}}return null}"""
FBTN = r"""()=>{const b=document.getElementById('fFoldBtn');if(!b)return null;const r=b.getBoundingClientRect();if(!r.width)return null;
  const cx=r.left+r.width/2,cy=r.top+r.height/2,a=document.elementFromPoint(cx,cy);const hb=__H.hitBox(b);
  return {cx,cy,l:Math.round(r.left),r:Math.round(r.right),t:Math.round(r.top),b:Math.round(r.bottom),on:!!a&&(a===b||b.contains(a)),at:a?(a.id?'#'+a.id:a.tagName.toLowerCase()):null,hit:hb}}"""
GRIP = r"""()=>{const g=document.getElementById('ndGrip');if(!g)return null;const r=g.getBoundingClientRect();if(!r.height)return null;const x=Math.round(r.left+r.width/2),y=Math.round(r.top+Math.min(300,r.height/2));
  const a=document.elementFromPoint(x,y);return {x,y,w:Math.round(r.width),on:!!a&&(a===g||g.contains(a))}}"""
J_SYN = r"""
window.__F3={how:null,
 tev(type,t0,x,y,active){let ev=null;
  try{const tt=new Touch({identifier:11,target:t0,clientX:x,clientY:y,pageX:x+scrollX,pageY:y+scrollY,screenX:x,screenY:y,radiusX:11,radiusY:11,force:1});
   ev=new TouchEvent(type,{bubbles:true,cancelable:true,composed:true,touches:active?[tt]:[],targetTouches:active?[tt]:[],changedTouches:[tt]});if(!__F3.how)__F3.how='TouchEvent'}catch(e){ev=null}
  if(!ev){ev=new Event(type,{bubbles:true,cancelable:true,composed:true});const o={identifier:11,target:t0,clientX:x,clientY:y,pageX:x+scrollX,pageY:y+scrollY,screenX:x,screenY:y},L=active?[o]:[];
   Object.defineProperty(ev,'touches',{value:L});Object.defineProperty(ev,'targetTouches',{value:L});Object.defineProperty(ev,'changedTouches',{value:[o]});__F3.how='Event+touches'}
  return ev},
 pe(type,x,y){return new PointerEvent(type,{bubbles:true,cancelable:true,composed:true,pointerId:21,pointerType:'touch',isPrimary:true,clientX:x,clientY:y,button:type==='pointermove'?-1:0,buttons:type==='pointerup'?0:1,width:22,height:22})},
 swipe([x0,y0,x1,y1,n]){const t0=document.elementFromPoint(x0,y0)||document.body;
  t0.dispatchEvent(__F3.pe('pointerdown',x0,y0));t0.dispatchEvent(__F3.tev('touchstart',t0,x0,y0,true));
  for(let i=1;i<=n;i++){const x=x0+(x1-x0)*i/n,y=y0+(y1-y0)*i/n;t0.dispatchEvent(__F3.pe('pointermove',x,y));t0.dispatchEvent(__F3.tev('touchmove',t0,x,y,true))}
  t0.dispatchEvent(__F3.pe('pointerup',x1,y1));t0.dispatchEvent(__F3.tev('touchend',t0,x1,y1,false));return __F3.how}
};
"""


class Pg(JG.Pg_PP):
    """JG.Pg_PP — 부팅 뒤 고정 대기 대신 표지(첫 syncRecords 끝) · 합성 밀기 도구"""

    def _ready(self):
        self.pg.wait_for_function(self.READY, timeout=90000)
        try:
            self.pg.wait_for_function(self.PDFS, timeout=180000)
        except Exception:
            pass
        QC.until(self.pg, _SYNCED, 8000, 'gg3_fix 부팅 뒤 첫 syncRecords 끝')
        self.pg.evaluate(JG.TOOLS)
        self.pg.evaluate(J_SYN)


def page(br, eng, tag, src, subj, dev):
    QC.launch('base' if tag[0] in 'BP' else 'new')
    return Pg(br, eng, tag + subj + str(dev[0]), src, subj, dev, touch=(dev == PHONE), who='gg3fix')


TLOG = r"""()=>{if(window.__tlg)return;window.__tlg=[];['touchstart','touchend','touchcancel'].forEach(t=>document.addEventListener(t,e=>{window.__tlg.push([t,Math.round(performance.now()),e.cancelable])},{capture:true,passive:true}))}"""


def swipe(p, x0, y0, x1, y1):
    p.ev(TLOG); p.ev('()=>{window.__tlg.length=0}')
    if p.eng == 'webkit':
        how = p.ev('a=>__F3.swipe(a)', [x0, y0, x1, y1, 8])
    else:
        c = p._cdp()
        c.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x0, 'y': y0, 'radiusX': 6, 'radiusY': 6, 'id': 1}]})
        for i in range(1, 6):   # ★ 10/9 20:4x — 기다림 없이 다섯 번(옛 = 16ms × 8 · 짐 클 때 앱 문턱 0.8 초를 넘김)
            c.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x0 + (x1 - x0) * i / 5.0, 'y': y0 + (y1 - y0) * i / 5.0, 'radiusX': 6, 'radiusY': 6, 'id': 1}]})
        c.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        how = 'cdp'
    lg = p.ev('()=>window.__tlg.slice()') or []
    st = [x for x in lg if x[0] == 'touchstart']; en = [x for x in lg if x[0] in ('touchend', 'touchcancel')]
    ms = (en[-1][1] - st[0][1]) if (st and en) else None
    return {'how': how, 'log': [x[0] for x in lg], 'ms': ms}


def hdr(p):
    p.ev(OPEN1)
    QC.until(p.pg, VIEWOPEN, 8000, 'gg3_fix 문항 창 열림')
    QC.sleep(600, '문항 창 머리 그리기 끝(표지 없음)', p.pg)
    return p.ev(HDR)


def f2(p):
    """폰 · 첫 화면 · 서랍 접힘 — ▾ 톡 · 누름 자리 · 밀기 · 손잡이 톡"""
    R = {}
    W, H = p.dev
    p.ev('()=>{try{closeView()}catch(e){}ndResFold(true)}')
    QC.sleep(700, '서랍 깜박 막이(편 직후 0.6 초) 넘김', p.pg)
    R['bfold0'] = p.ev(BFOLD)
    b = p.ev(FBTN)
    R['btn'] = b
    if b and b.get('cx'):
        p.tap(b['cx'], b['cy'], wait=0)
        QC.sleep(900, '진짜 톡 뒤 터치 대체 누르기(60ms) · 머리 펼침 그리기', p.pg)
        R['bfold1'] = p.ev(BFOLD)
        R['dfold1'] = p.ev(FOLD)
        R['view1'] = p.ev(VIEWOPEN)
        if R['bfold1'] != R['bfold0']:   # 되돌려 둠(다음 칸이 같은 첫 화면에서)
            b2 = p.ev(FBTN)
            if b2 and b2.get('on'):
                p.tap(b2['cx'], b2['cy'], wait=0)
                QC.sleep(700, '머리 되돌림', p.pg)
    p.ev('()=>{try{closeView()}catch(e){}ndResFold(true)}')
    QC.sleep(700, '서랍 깜박 막이 넘김', p.pg)
    pt = p.ev(PICK_LEFT, [W, H, SKIP])
    R['swipe_pt'] = pt
    if pt:
        R['swipe_how'] = swipe(p, pt['x'], pt['y'], pt['x'] + 130, pt['y'] + 6)
        QC.sleep(500, '밀기 뒤 펴기 반영', p.pg)
        R['swipe_open'] = not p.ev(FOLD)
        if not R['swipe_open'] and ((R['swipe_how'] or {}).get('ms') or 0) > 700:   # 다시 잼 — 밀기가 앱 문턱(0.8 초)을 넘겼으면(짐 탓) 한 번 더
            p.ev('()=>ndResFold(true)'); QC.sleep(700, '서랍 깜박 막이 넘김(다시 잼)', p.pg)
            R['swipe_again'] = swipe(p, pt['x'], pt['y'], pt['x'] + 130, pt['y'] + 6)
            QC.sleep(500, '밀기 뒤 펴기 반영', p.pg)
            R['swipe_open'] = not p.ev(FOLD)
        R['swipe_view'] = p.ev(VIEWOPEN)
    p.ev('()=>{try{closeView()}catch(e){}ndResFold(true)}')
    QC.sleep(700, '서랍 깜박 막이 넘김', p.pg)
    g = p.ev(GRIP)
    R['grip'] = g
    if g:
        p.tap(g['x'], g['y'], wait=0)
        QC.sleep(900, '손잡이 톡 뒤 펴기 · 유령 click 틈', p.pg)
        R['grip_open'] = not p.ev(FOLD)
        R['grip_view'] = p.ev(VIEWOPEN)
    p.ev('()=>ndResFold(false)')
    R['err'] = (p.errs or [])[:4] + (p.ev('()=>(window.__err||[]).slice(0,4)') or [])
    return R


def build_p42(base_src):
    P = json.load(io.open(PATCHES, encoding='utf-8'))
    P = P['patches'] if isinstance(P, dict) else P
    t = base_src.replace('\r\n', '\n')
    for i, (o, n) in enumerate(P):
        o = o.replace('\r\n', '\n'); n = n.replace('\r\n', '\n')
        if t.count(o) != 1:
            raise SystemExit('P42 짓기 — 패치 #%d 옛 글 %d 회' % (i, t.count(o)))
        t = t.replace(o, n, 1)
    return t


def main():
    t_all = time.time()
    src = {'N': io.open(NEW, encoding='utf-8', newline='').read()}
    if QC.GATE:
        QC.sub('git:show-app')
        b = JG.app_src(BASE)
        if BASE == 'cab7b5a' and hashlib.md5(b.replace('\r\n', '\n').encode('utf-8')).hexdigest() != BASE_MD5:
            raise SystemExit('바탕 md5 다름')
        src['B'] = b
        src['P'] = build_p42(b)
        N('판', '세 판 LF md5', {k: hashlib.md5(v.replace('\r\n', '\n').encode('utf-8')).hexdigest()[:8] for k, v in src.items()})
    from playwright.sync_api import sync_playwright
    D = {}
    with sync_playwright() as pw:
        for eng in (ENGS if not QC.SMOKE else ['chromium']):
            br = getattr(pw, eng).launch()
            try:
                subs = ('earth', 'bio', 'phys') if not QC.SMOKE else ('earth',)
                for subj in subs:
                    for dev in ((PHONE, PCD) if (eng == 'chromium' and not QC.SMOKE) else (PHONE,)):
                        for tag in (('N', 'B', 'P') if (QC.GATE and eng == 'chromium') else ('N',)):
                            if subj == 'phys' and tag == 'B' and dev == PCD:
                                continue   # 물리 ① = NEW ↔ P42 만(바탕 머리는 물리에서 바뀌는 게 뜻)
                            k = '%s/%s/%s/%d' % (eng, tag, subj, dev[0])
                            print('… ' + k, flush=True)
                            r = {}
                            try:
                                p = page(br, eng, tag, src[tag], subj, dev)
                            except Exception as e:
                                D[k] = {'boot': 'NG ' + str(e)[:200]}
                                continue
                            try:
                                if dev == PHONE:
                                    r['f2'] = f2(p)
                                if eng == 'chromium':
                                    r['hdr'] = hdr(p)
                                r['boot'] = 'ok'
                            except Exception as e:
                                r['exc'] = str(e)[:240]
                            finally:
                                p.close()
                            D[k] = r
            finally:
                br.close()
    # ── 판정 ──
    g = lambda k: D.get(k) or {}
    for subj in (('earth', 'bio', 'phys') if not QC.SMOKE else ('earth',)):
        for dev in ((PHONE, PCD) if not QC.SMOKE else (PHONE,)):
            dn = '폰384' if dev == PHONE else 'PC1100'
            n = g('chromium/N/%s/%d' % (subj, dev[0])).get('hdr')
            if subj in ('earth', 'bio'):
                bv = g('chromium/B/%s/%d' % (subj, dev[0])).get('hdr') if QC.GATE else None
                want = QC.base('hdr/%s/%d' % (subj, dev[0]), bv if QC.GATE else n)
                diff = sorted(k for k in set((n or {}).keys()) | set((want or {}).keys()) if (n or {}).get(k) != (want or {}).get(k))
                T('①[%s·%s]' % (subj, dn), '문항 창 머리 계산 스타일 = 바탕 cab7b5a(머리 CSS 샘 0)', bool(n) and bool(want) and not diff,
                  {'다른 칸': diff[:8], '새': {k: (n or {}).get(k) for k in diff[:3]}, '바탕': {k: (want or {}).get(k) for k in diff[:3]}, '기준': QC.base_note('hdr/%s/%d' % (subj, dev[0]))})
                if QC.GATE:
                    pv = g('chromium/P/%s/%d' % (subj, dev[0])).get('hdr')
                    pd = sorted(k for k in set((pv or {}).keys()) | set((bv or {}).keys()) if (pv or {}).get(k) != (bv or {}).get(k))
                    T('①[%s·%s]' % (subj, dn), '★헛잣대 — 패치 42 판(고치기 전)은 머리가 바탕과 다르다(샘)', bool(pd), {'다른 칸': pd[:8]})
            elif QC.GATE:
                pv = g('chromium/P/%s/%d' % (subj, dev[0])).get('hdr')
                diff = sorted(k for k in set((n or {}).keys()) | set((pv or {}).keys()) if (n or {}).get(k) != (pv or {}).get(k))
                T('①[phys·%s]' % dn, '물리 문항 창 머리 계산 스타일 = 패치 42 판(시안 v57 · :where 특이도 0)', bool(n) and bool(pv) and not diff, {'다른 칸': diff[:8]})
    for eng in (ENGS if not QC.SMOKE else ['chromium']):
        for subj in (('earth', 'bio', 'phys') if not QC.SMOKE else ('earth',)):
            pre = '②[%s·%s·폰384]' % (eng, subj)
            n = g('%s/N/%s/%d' % (eng, subj, PHONE[0]))
            f = n.get('f2') or {}
            if n.get('boot') != 'ok':
                T(pre, '부팅', False, n)
                continue
            b = f.get('btn') or {}
            T(pre, 'F2-a 첫 화면 ▾ 가운데 진짜 톡 = 머리 펼침(body.fold 바뀜) · 서랍 접힌 그대로 · 문항 안 열림',
              b.get('on') is True and f.get('bfold1') is not None and f.get('bfold1') != f.get('bfold0') and f.get('dfold1') is True and f.get('view1') is False,
              {k: f.get(k) for k in ('bfold0', 'btn', 'bfold1', 'dfold1', 'view1')})
            if QC.SMOKE:
                continue
            hit = b.get('hit') or {}
            bh = None
            if QC.GATE and eng == 'chromium':
                bh = ((g('chromium/B/%s/%d' % (subj, PHONE[0])).get('f2') or {}).get('btn') or {}).get('hit')
            want = QC.base('fhit/%s/%s' % (eng, subj), bh if (QC.GATE and eng == 'chromium') else hit)
            T(pre, 'F2-b ▾ 누름 자리 ≥ 36×36 · 바탕과 같음(revfix0929 A-6)', (hit.get('w') or 0) >= 36 and (hit.get('h') or 0) >= 36 and (not want or (hit.get('w'), hit.get('h')) == ((want or {}).get('w'), (want or {}).get('h'))),
              {'새': hit, '바탕': want, '기준': QC.base_note('fhit/%s/%s' % (eng, subj))})
            T(pre, 'F2-c 접힌 서랍 = 화면 왼쪽 반에서 오른쪽 밀기 = 펴짐(v56 · v57) · 문항 안 열림', f.get('swipe_open') is True and f.get('swipe_view') is False,
              {k: f.get(k) for k in ('swipe_pt', 'swipe_how', 'swipe_again', 'swipe_open', 'swipe_view')})
            T(pre, 'F2-d 13px 손잡이 진짜 톡 = 펴짐 · 문항 안 열림', f.get('grip_open') is True and f.get('grip_view') is False,
              {k: f.get(k) for k in ('grip', 'grip_open', 'grip_view')})
            T(pre, 'JS 오류 0', not f.get('err'), f.get('err'))
            if QC.GATE and eng == 'chromium':
                pf = g('chromium/P/%s/%d' % (subj, PHONE[0])).get('f2') or {}
                pb = pf.get('btn') or {}
                T(pre, '★헛잣대 — 패치 42 판: ▾ 가운데 톡이 서랍을 엶(머리 안 펼침) 또는 누름 자리 < 36',
                  (pf.get('dfold1') is False) or (pb.get('hit') or {}).get('w', 99) < 36, {'btn': pb, 'dfold1': pf.get('dfold1'), 'bfold': [pf.get('bfold0'), pf.get('bfold1')]})
                bf = g('chromium/B/%s/%d' % (subj, PHONE[0])).get('f2') or {}
                T(pre, '★헛잣대 — 바탕: 왼쪽 반 밀기로 안 펴짐(밀기 없음)', bf.get('swipe_open') is False, {k: bf.get(k) for k in ('swipe_open', 'grip_open')})
                N(pre, '바탕 손잡이 진짜 톡(바탕은 무거운 누름 뒤 터치 대체 누르기가 한 번 더 눌러 되접힐 수 있음 = 패치 #37 · #38 이 고친 v52 버그)', {k: bf.get(k) for k in ('grip_open', 'grip_view')})
    p = sum(1 for x in RES if x[0] == 'PASS')
    f = sum(1 for x in RES if x[0] == 'FAIL')
    tail = '\n합계  PASS %d · FAIL %d · %.1f 분 · mode %s' % (p, f, (time.time() - t_all) / 60, QC.MODE)
    print(tail, flush=True)
    try:
        raw = os.path.join(tempfile.gettempdir(), 'h_gg3fix')
        os.makedirs(raw, exist_ok=True)
        json.dump(D, io.open(os.path.join(raw, 'raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
        io.open(OUTF, 'w', encoding='utf-8').write('\n'.join('%s | %s %s' % x for x in RES) + '\n' + tail + '\n')
    except Exception as e:
        print('INFO | 결과 파일 못 씀 | %s' % e, flush=True)
    sys.exit(0 if not f else 1)


if __name__ == '__main__':
    main()
