# -*- coding: utf-8 -*-
r"""물리 문항 창 머리 단추 손가락 누를 자리 30 관문(자과 · 2026-10-10 jagwa_batch ③)

  python _harness_jagwa_touch30.py [--new <앱>] [--base <git 판 | 파일>] [--only t1,t2,...] [--plan all|phys-touch] [--res <결과>] [--vendor <cdnjs 사본>] [--mode gate|regress|smoke]

  근거 = 10/7 `_task_jagwa_phys_win` §A-04 「손가락 기기 누를 자리 30px」 · 22px 겉모양 = 사용자 10/8 18:24(v21) 결정이라 그대로 · 결정로그 10/9 22:27 [채팅] · 10/10 00:52 [채팅]
  단추 여섯 = #view .vtop> #vBack(서재 ✕) · #g3Fold(▾) · #tm(시계) · #vWinTg(⤢) · #vPrev(◀) · #vNext(▶) · 물리만(body[data-layer="pdf"])
  기기 = 폰 390×844 · iPad 820×1180(손가락 · CDP) · 문항 창 두 꼴(처음 = 창 · ⤢ 뒤 = 전체) · PC 1100(마우스 · 무변만)
    t1 누를 자리 ≥ 30 — 단추 가운데에서 elementFromPoint 로 위 · 아래 · 왼 · 오른 그 단추가 잡히는 데까지(높이 · 폭) · 손가락 기기만
    t2 겹침 0 — 머리 안 누를 것(여섯 · 🔗 · 펜 알약 단추 · 근거 줄 것)마다 제 겉 상자 안 점 25 개가 다 제 것(이웃 투명 자리가 안 뺏음)
    t3 머리 밖 안 덮음 — 머리 상자 위 · 아래 1px 바깥 줄(여섯 단추 폭)에서 여섯 단추가 안 잡힘
    t4 머리 그림 = 바탕 — 머리 줄 · 자식마다 겉 상자(getBoundingClientRect) · 계산 스타일(글자 · 색 · 바탕 · 테두리 · 안여백 · 높이 · 폭 · 줄 높이 · 둥근 모 · 그림자 · 투명도)
    t5 CDP 진짜 톡 반지름 22(크롬 터치 맞춤 켬) — 단추 가운데 · 새 자리 끝 2px 안 = 그 단추 · 머리 밖 3px = 머리 단추 아님(누름 일은 window 잡아채기로 막고 눌린 것만 적음)
    t6 지학 · 생물 머리 무변(폰 · 같은 잣대 t4 + 누를 자리 = 바탕)   t7 PC(마우스) 물리 머리 무변(t4 + 누를 자리 = 바탕)
    t8 화면 훑기 small(누를 자리 < 30 · 여섯) 0 · 옛 잣대 JG.TOOLS sweep(36 · 겉 상자/누를 자리) 결과는 적기만
  헛잣대 = 바탕 7299ec3(_roots.base_rev()) — 누를 자리 22 → t1 · t8 FAIL
  ⚠ 10/10 jagwa_batch — ③ 은 이 판에서 뗐다(결정로그 10/10 03:24 [채팅] · 본 세션 03:2x 알림) · 앱 고침 없음 → 지금은 잴 도구(t1 · t8 = 바탕 · 새 판 둘 다 FAIL) ·
    지시 그대로는 못 함: 같은 열에 쌓인 단추(창 꼴 ✕ 위 · ▾ 아래 가운데 사이 26px · 머리 53px / 폰 전체 ✕ · ▶ · ▾ 셋 · 머리 77px / iPad 전체 머리 27px) →
    30 · 겹침 0 · 머리 안을 같이 못 지킴 · 안(--new 에 안 사본 · --base 에 지금 판 · --plan phys-touch)을 고른 뒤 관문으로 쓰고 그때 전수표 한 줄
  ⚠ 자과앱 픽셀 게이트 없음(CLAUDE.md) — getBoundingClientRect · getComputedStyle · elementFromPoint · CDP 톡
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기(Pg_PP · PHONE · PAD)
import io, json, os, sys, tempfile, time   # noqa: E402
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = _roots.genie()
NEWF = ARG('--new', os.path.join(GENIE, 'jagwa', 'index.html'))
BASEARG = ARG('--base', None)
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_touch30_result.txt'))
VENDOR = ARG('--vendor', os.path.join(tempfile.gettempdir(), 'h_jgbatch', 'vendor'))
JG.conf(VENDOR_PP=VENDOR)
PCDEV = (1100, 800)
PLAN = ARG('--plan', 'all')   # all | phys-touch(물리 폰 · iPad 만 — 안 시험)
SIX = ['vBack', 'g3Fold', 'tm', 'vWinTg', 'vPrev', 'vNext']
ROWS = []
from playwright.sync_api import sync_playwright   # noqa: E402

TJS = r"""
window.__T={
 SIX:['vBack','g3Fold','tm','vWinTg','vPrev','vNext'],
 PROPS:['fontSize','fontWeight','fontFamily','color','backgroundColor','borderTopWidth','borderRightWidth','borderBottomWidth','borderLeftWidth','borderTopColor','borderTopStyle',
   'paddingTop','paddingRight','paddingBottom','paddingLeft','marginTop','marginRight','marginBottom','marginLeft','height','width','minHeight','minWidth','lineHeight',
   'borderTopLeftRadius','boxShadow','opacity','transform','display','order','alignSelf','verticalAlign','textAlign','visibility'],
 r(e){const b=e.getBoundingClientRect();return [Math.round(b.left*100)/100,Math.round(b.top*100)/100,Math.round(b.width*100)/100,Math.round(b.height*100)/100]},
 vis(e){return !!e&&e.isConnected&&getComputedStyle(e).display!=='none'&&getComputedStyle(e).visibility!=='hidden'&&e.getBoundingClientRect().width>0&&e.getBoundingClientRect().height>0},
 own(e,x,y){const a=document.elementFromPoint(x,y);return !!a&&(a===e||e.contains(a))},
 hit(e){const b=e.getBoundingClientRect(),cx=b.left+b.width/2,cy=b.top+b.height/2;if(!__T.own(e,cx,cy))return {h:0,w:0,on:false,up:0,dn:0};
   let u=0,d=0,l=0,rt=0;while(u<60&&cy-u-1>=0&&__T.own(e,cx,cy-u-1))u++;while(d<60&&cy+d+1<innerHeight&&__T.own(e,cx,cy+d+1))d++;
   while(l<80&&cx-l-1>=0&&__T.own(e,cx-l-1,cy))l++;while(rt<80&&cx+rt+1<innerWidth&&__T.own(e,cx+rt+1,cy))rt++;
   /* 위 · 아래 끝은 가운데 줄만이 아니라 폭 전체에서 가장 짧은 자리(왼 · 가운데 · 오른 다섯 줄) — 모서리만 짧은 자리를 놓치지 않게 */
   let hmin=1e9;for(const fx of [0.15,0.3,0.5,0.7,0.85]){const x=b.left+b.width*fx;if(!__T.own(e,x,cy)){continue}let uu=0,dd=0;
     while(uu<60&&cy-uu-1>=0&&__T.own(e,x,cy-uu-1))uu++;while(dd<60&&cy+dd+1<innerHeight&&__T.own(e,x,cy+dd+1))dd++;hmin=Math.min(hmin,uu+dd+1)}
   return {h:u+d+1,w:l+rt+1,on:true,up:Math.round((b.top-(cy-u))*10)/10,dn:Math.round(((cy+d+1)-b.bottom)*10)/10,hmin:hmin===1e9?0:hmin,
     top:Math.round((cy-u)*10)/10,bot:Math.round((cy+d+1)*10)/10}},
 head(){const v=document.getElementById('view'),t=document.querySelector('#view .vtop');if(!t||!__T.vis(t))return null;
   const cs=getComputedStyle(t);const kids=[...t.children].filter(__T.vis);
   const sty=e=>{const c=getComputedStyle(e);const o={};__T.PROPS.forEach(p=>o[p]=c[p]);return o};
   return {layer:document.body.dataset.layer||'',coarse:matchMedia('(pointer:coarse)').matches,win:v.classList.contains('win'),vw:innerWidth,
     vtop:{r:__T.r(t),s:sty(t),rowGap:cs.rowGap,wrap:cs.flexWrap},
     kids:kids.map(e=>({k:e.id?'#'+e.id:e.tagName.toLowerCase()+'.'+String(e.className||'').split(' ')[0],r:__T.r(e),s:sty(e),t:(e.textContent||'').trim().slice(0,10)}))}},
 six(){const t=document.querySelector('#view .vtop');const out={};__T.SIX.forEach(id=>{const e=document.getElementById(id);
     if(!e||!__T.vis(e)||!t.contains(e)){out[id]=null;return}out[id]={r:__T.r(e),hit:__T.hit(e)}});return out},
 /* t2 — 머리 안 누를 것마다 제 겉 상자 안 점 5×5 가 다 제 것인가 */
 steal(){const t=document.querySelector('#view .vtop');const A=[...t.querySelectorAll('button,[role=button],input,select,textarea,a[href],[data-ggrt],[data-ggtog],[data-ggbang],.g3lb')].filter(__T.vis);
   const bad=[];A.forEach(e=>{const b=e.getBoundingClientRect();if(b.width<3||b.height<3)return;let n=0,m=0,who={};
     for(const fx of [0.12,0.31,0.5,0.69,0.88])for(const fy of [0.12,0.31,0.5,0.69,0.88]){const x=b.left+b.width*fx,y=b.top+b.height*fy;if(x<0||y<0||x>=innerWidth||y>=innerHeight)continue;m++;
       const a=document.elementFromPoint(x,y);if(a&&(a===e||e.contains(a)))n++;else{const w=a?(a.closest('button,[id]')||a):null;const k=w?(w.id||w.tagName):'null';who[k]=(who[k]||0)+1}}
     if(m&&n<m)bad.push({e:e.id||e.tagName.toLowerCase()+'.'+String(e.className||'').split(' ')[0]+':'+(e.textContent||'').trim().slice(0,6),own:n,of:m,who})});
   return {n:A.length,bad}},
 /* t3 — 머리 상자 위 · 아래 1px 바깥 줄에서 여섯이 잡히나 */
 outside(){const t=document.querySelector('#view .vtop'),b=t.getBoundingClientRect();const res=[];
   __T.SIX.forEach(id=>{const e=document.getElementById(id);if(!e||!__T.vis(e))return;const q=e.getBoundingClientRect();
     for(const y of [b.top-1,b.bottom+1]){if(y<0||y>=innerHeight)continue;for(const fx of [0.1,0.5,0.9]){const x=q.left+q.width*fx;const a=document.elementFromPoint(x,y);
       if(a&&(a===e||e.contains(a)))res.push({id,y:Math.round(y*10)/10,x:Math.round(x)})}}});return {top:Math.round(b.top*10)/10,bottom:Math.round(b.bottom*10)/10,hits:res}},
 /* t5 — 누름 잡아채기(window capture · 앱 일 막음) */
 arm(){window.__TAP=[];if(window.__tapArmed)return;window.__tapArmed=1;
   /* 누름 앞 이벤트(touchstart · pointerdown …)는 앱에 안 넘기기만(preventDefault 안 함 — 하면 브라우저가 click 을 안 낸다) · click 은 막고 적음 */
   const f=e=>{if(!window.__tapOn)return;const b=e.target&&e.target.closest?e.target.closest('button,[id]'):null;window.__TAP.push({t:e.type,id:b?(b.id||b.tagName):null,inHead:!!(e.target&&e.target.closest&&e.target.closest('#view .vtop'))});
     e.stopImmediatePropagation();if(e.type==='click')e.preventDefault()};
   ['click','pointerdown','pointerup','mousedown','mouseup','touchstart','touchend'].forEach(ty=>window.addEventListener(ty,f,{capture:true,passive:false}))},
 errs(){return (window.__err||[]).slice(0,6)}
};
"""


def R(g, dv, name, okn, okb, val):
    ROWS.append((g, dv, name, okn, okb, val))
    print('%s | 바탕 %s | %s · %s · %s | %s' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, dv, name,
          (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str))[:800]), flush=True)


APPS = {}


def tap22(p, x, y):
    """CDP 진짜 톡 · 반지름 22(크롬 터치 맞춤이 켜지는 손가락 크기) → 눌린 것(click 의 단추 id)"""
    p.ev("()=>{window.__TAP=[];window.__tapOn=1}")
    c = p._cdp()
    c.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'radiusX': 22, 'radiusY': 22, 'force': 1, 'id': 1}]})
    p.pg.wait_for_timeout(50)
    c.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    p.pg.wait_for_timeout(250)
    L = p.ev("()=>{window.__tapOn=0;return window.__TAP.slice()}")
    cl = [x for x in L if x['t'] == 'click']
    pd = [x for x in L if x['t'] in ('pointerdown', 'touchstart')]
    return (cl[0]['id'] if cl else None), (pd[0]['id'] if pd else None), len(L)


def measure(br, who, subj, dev, touch, do_tap):
    """한 판 · 한 과목 · 한 기기 — 문항 창 처음 꼴(창) · ⤢ 뒤 꼴(전체) 둘을 잰다"""
    QC.launch('new' if who == 'NEW' else 'base')
    p = JG.Pg_PP(br, 'chromium', 'tc_%s_%s_%dx%d' % (who, subj, dev[0], dev[1]), APPS[who], subj, dev, touch=touch, remote=JG.Remote())   # 문맥마다 새 가짜 원격
    out = {}
    try:
        QC.until(p.pg, "()=>(typeof CARD_LAYER==='undefined'||!CARD_LAYER||(typeof DATA_V!=='undefined'&&DATA_V>0))&&(typeof GG_READY==='undefined'||!!GG_READY)", 60000, '과목 문항(DATA_V) · 근거(GG_READY) 읽힘')
        p.ev(TJS)
        no = p.ev("()=>DATA[Math.min(10,DATA.length-1)][F.NO]")
        p.ev("n=>openView(n)", no)
        QC.until(p.pg, "()=>{const t=document.querySelector('#view .vtop');return !!t&&!document.getElementById('view').classList.contains('hide')&&t.getBoundingClientRect().height>0}", 15000, '문항 창 머리')
        QC.sleep(1500, '문항 창 열림 뒤 머리 줄 자식(▾ · 펜 알약 · 근거 줄) 늦게 끼움 — 표지 없음', p.pg)
        for mode in ('처음', '⤢ 뒤'):
            if mode == '⤢ 뒤':
                p.ev("()=>{const b=document.getElementById('vWinTg');if(b)b.click()}")
                QC.sleep(1200, '⤢ 뒤 창 ↔ 전체 다시 그림(vwApply 60ms + 다시 맞춤) — 표지 없음', p.pg)
            h = p.ev("()=>__T.head()")
            six = p.ev("()=>__T.six()")
            st = p.ev("()=>__T.steal()")
            ou = p.ev("()=>__T.outside()")
            taps = {}
            if do_tap and touch:
                p.ev("()=>__T.arm()")
                for id_ in SIX:
                    s = six.get(id_)
                    if not s:
                        continue
                    x0, y0, w, hh = s['r']
                    cx, cy = x0 + w / 2, y0 + hh / 2
                    hb = s['hit']
                    pts = {'가운데': (cx, cy)}
                    if hb and hb.get('on'):
                        pts['자리 위 끝 2px 안'] = (cx, hb['top'] + 2)
                        pts['자리 아래 끝 2px 안'] = (cx, hb['bot'] - 2)
                    r = {}
                    for nm, (x, y) in pts.items():
                        if 0 <= y < dev[1]:
                            r[nm] = tap22(p, x, y)[0]
                    taps[id_] = r
                # 머리 밖 3px(아래) — 여섯 단추 x 자리마다
                hb = h['vtop']['r']
                outs = {}
                for id_ in SIX:
                    s = six.get(id_)
                    if not s:
                        continue
                    x = s['r'][0] + s['r'][2] / 2
                    y = hb[1] + hb[3] + 3
                    if y < dev[1]:
                        outs[id_] = tap22(p, x, y)[0]
                taps['_머리 밖 3px'] = outs
            out[mode] = {'head': h, 'six': six, 'steal': st, 'outside': ou, 'taps': taps}
        p.pg.evaluate(JG.TOOLS)
        out['sweep36'] = p.ev("([s,t])=>__H.sweep(s,t)", ['#view .vtop', touch])
        out['errs'] = p.ev("()=>__T.errs()") + p.errs[:3]
    finally:
        p.close()
    return out


def same_head(a, b):
    """t4 — 머리 줄 · 자식 겉 상자 · 계산 스타일 같나(±0.05px) → 다른 자리 목록"""
    if not a or not b:
        return ['머리 없음 %s/%s' % (bool(a), bool(b))]
    diff = []
    if any(abs(x - y) > 0.05 for x, y in zip(a['vtop']['r'], b['vtop']['r'])):
        diff.append(('머리 상자', a['vtop']['r'], b['vtop']['r']))
    for k, v in a['vtop']['s'].items():
        if b['vtop']['s'].get(k) != v:
            diff.append(('머리 ' + k, v, b['vtop']['s'].get(k)))
    ka = {x['k']: x for x in a['kids']}
    kb = {x['k']: x for x in b['kids']}
    if list(ka) != list(kb):
        diff.append(('자식 차례', list(ka), list(kb)))
    for k in ka:
        if k not in kb:
            continue
        if any(abs(x - y) > 0.05 for x, y in zip(ka[k]['r'], kb[k]['r'])):
            diff.append((k + ' 상자', ka[k]['r'], kb[k]['r']))
        for p_, v in ka[k]['s'].items():
            if kb[k]['s'].get(p_) != v:
                diff.append((k + ' ' + p_, v, kb[k]['s'].get(p_)))
        if ka[k]['t'] != kb[k]['t'] and k not in ('#tm',):
            diff.append((k + ' 글', ka[k]['t'], kb[k]['t']))
    return diff


def main():
    APPS['NEW'] = open(NEWF, 'rb').read().replace(b'\r\n', b'\n').decode('utf-8')
    base_rev = BASEARG or _roots.base_rev()
    if QC.GATE:
        if BASEARG and os.path.isfile(BASEARG):
            APPS['BASE'] = open(BASEARG, 'rb').read().replace(b'\r\n', b'\n').decode('utf-8')
        else:
            QC.sub('git:show-app')
            APPS['BASE'] = JG.app_src(base_rev)
    t0 = time.time()
    plan = [('phys', '폰390', JG.PHONE, True, True), ('phys', 'iPad820', JG.PAD, True, True), ('phys', 'PC1100', PCDEV, False, False),
            ('earth', '폰390', JG.PHONE, True, False), ('bio', '폰390', JG.PHONE, True, False)]
    if QC.SMOKE:
        plan = plan[:1]
    if PLAN == 'phys-touch':   # 안 시험 — 물리 폰 · iPad 만
        plan = plan[:2]
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        try:
            for subj, dname, dev, touch, do_tap in plan:
                with QC.stage('%s %s' % (subj, dname)):
                    V = {}
                    for who in (('NEW', 'BASE') if QC.GATE else ('NEW',)):
                        try:
                            V[who] = measure(br, who, subj, dev, touch, do_tap)
                        except Exception as e:
                            V[who] = {'err': 'ERR ' + repr(e)[:300]}
                    tag = 'chromium·%s·%s' % (dname, subj)
                    n = V['NEW']
                    b = V.get('BASE') or {}
                    if n.get('err'):
                        R('t0', tag, '띄움', False, None, n)
                        continue
                    for mode in ('처음', '⤢ 뒤'):
                        nm, bm = n[mode], b.get(mode)
                        tg = '%s·%s' % (tag, mode)
                        win = nm['head']['win'] if nm['head'] else None
                        if subj == 'phys' and touch:
                            def t1(m):
                                bad = {k: (v['hit']['h'], v['hit']['w'], v['hit'].get('hmin')) for k, v in m['six'].items() if v and (v['hit']['h'] < 30 or v['hit']['w'] < 30 or v['hit'].get('hmin', 0) < 30)}
                                seen = [k for k, v in m['six'].items() if v]
                                return (len(seen) >= 5 and not bad), {'잰 단추': seen, '30 밑': bad,
                                                                      '누를 자리(높이×폭 · 위/아래 더한 px)': {k: (v['hit']['h'], v['hit']['w'], v['hit']['up'], v['hit']['dn']) for k, v in m['six'].items() if v},
                                                                      '겉 상자': {k: v['r'][2:] for k, v in m['six'].items() if v}, '창': win}
                            okn, vn = t1(nm)
                            okb, vb = t1(bm) if bm else (None, None)
                            if not ONLY or 't1' in ONLY:
                                R('t1', tg, '여섯 누를 자리 ≥ 30(높이 · 폭 · 폭 다섯 줄 가장 짧은 높이)', okn, okb, {'NEW': vn, 'BASE': vb})
                            if not ONLY or 't8' in ONLY:
                                R('t8', tg, '화면 훑기 small(누를 자리 < 30 · 여섯) 0', okn, okb, {'small': sorted(vn['30 밑']), 'BASE small': sorted((vb or {}).get('30 밑') or [])})
                        if not ONLY or 't2' in ONLY:
                            okn = not nm['steal']['bad']
                            okb = (not bm['steal']['bad']) if bm else None
                            R('t2', tg, '겹침 0 — 머리 안 누를 것마다 제 겉 상자 점 25 개가 다 제 것', okn, okb, {'NEW': nm['steal'], 'BASE': bm['steal'] if bm else None})
                        if not ONLY or 't3' in ONLY:
                            okn = not nm['outside']['hits']
                            R('t3', tg, '머리 밖(위 · 아래 1px) 안 덮음', okn, (not bm['outside']['hits']) if bm else None, {'NEW': nm['outside'], 'BASE': bm['outside'] if bm else None})
                        if not ONLY or 't4' in ONLY or 't6' in ONLY or 't7' in ONLY:
                            g = 't4' if (subj == 'phys' and touch) else ('t7' if subj == 'phys' else 't6')
                            if QC.GATE:
                                d = same_head(nm['head'], bm['head'] if bm else None)
                            else:
                                d = [] if QC.same('%s.head@%s' % (g, tg), nm['head']) else ['스냅샷과 다름']
                            extra = {}
                            if g in ('t6', 't7') and bm:
                                hn = {k: (v['hit']['h'], v['hit']['w']) for k, v in nm['six'].items() if v}
                                hb2 = {k: (v['hit']['h'], v['hit']['w']) for k, v in bm['six'].items() if v}
                                extra = {'누를 자리 NEW': hn, '누를 자리 BASE': hb2}
                                if hn != hb2:
                                    d.append(('누를 자리', hn, hb2))
                            R(g, tg, {'t4': '머리 그림 = 바탕(겉 상자 · 계산 스타일)', 't6': '지학 · 생물 머리 무변(겉 · 스타일 · 누를 자리)', 't7': 'PC(마우스) 물리 머리 무변(겉 · 스타일 · 누를 자리)'}[g],
                              not d, None, {'다른 자리': d[:12], '다른 수': len(d), **extra})
                        if nm.get('taps') and (not ONLY or 't5' in ONLY):
                            bad = {}
                            for id_, r in nm['taps'].items():
                                if id_.startswith('_'):
                                    continue
                                for k2, got in r.items():
                                    if got != id_:
                                        bad['%s %s' % (id_, k2)] = got
                            outb = {k: v for k, v in nm['taps'].get('_머리 밖 3px', {}).items() if v in SIX}
                            okn = not bad and not outb
                            bt = bm.get('taps') if bm else None
                            R('t5', tg, 'CDP 톡 반지름 22 — 가운데 · 새 자리 끝 2px 안 = 그 단추 · 머리 밖 3px = 머리 단추 아님', okn, None,
                              {'틀림': bad, '머리 밖에서 단추': outb, 'NEW': nm['taps'], 'BASE': bt})
                    if not ONLY or 't8' in ONLY:
                        R('t8i', tag, '(적기만) 옛 잣대 JG.TOOLS sweep(36 · 머리 줄)', True, None, {'NEW': [x for x in n.get('sweep36', []) if x.startswith('small')][:10],
                                                                                              'BASE': [x for x in b.get('sweep36', []) if x.startswith('small')][:10]})
                    if n.get('errs'):
                        R('t0', tag, '페이지 오류 0', False, None, n['errs'])
        finally:
            br.close()
    npass = sum(1 for r in ROWS if r[3]); nfail = sum(1 for r in ROWS if not r[3])
    vac = [r for r in ROWS if r[4] is True and r[0] in ('t1', 't8')]
    print('\n== PASS %d · FAIL %d · 헛잣대(바탕도 PASS · t1 · t8) %d · %.0f초' % (npass, nfail, len(vac), time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · jagwa_touch30 · NEW %s · 바탕 %s · 모드 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), os.path.basename(NEWF), base_rev if QC.GATE else '(regress)', QC.MODE))
        for g, dv, n_, okn, okb, v in ROWS:
            f.write('%s | 바탕 %s | %s · %s · %s | %s\n' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, dv, n_,
                    (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str))[:3000]))
        f.write('== PASS %d · FAIL %d · 헛잣대 %d\n' % (npass, nfail, len(vac)))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
