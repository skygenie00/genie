# -*- coding: utf-8 -*-
r"""_task_jagwa_penfinger_add2 §E 관문 — 펜 도구 두 손가락 확대(D1) · 펜보다 먼저 얹은 손바닥 · 확대 그림 흰 바탕(D2) ·
    덮개 밑 톡 뒤 키보드 click(D4) · 펼친 뒤 글상자(#qtxt) · add1 관문 3a·4 다시 짬(D3) — Chromium + WebKit · 아이패드 세로 820×1180

  NEW   = --new <파일>(없으면 genie 작업트리 jagwa/index.html)
  BASE3 = genie d27c43a blob(add1 인도판 · md5(LF) 91ebc381) — 1~5 헛잣대(고친 칸은 여기서 FAIL 이어야)
  BASE2 = genie f497f05 blob(본판 인도판 · md5(LF) 0c1f47dd) — 2(손바닥 · 두 판 다 창 뜸) · 6a·6b(add1 이 고친 것 — add1 앞 판에서 FAIL 이어야) 헛잣대
  입력 = 진짜 포인터 — Chromium: 손가락 CDP Input.dispatchTouchEvent(radiusX·Y 22 · 두 손가락 = id 1·2 · 손바닥 = 반지름 40) ·
                        펜 CDP Input.dispatchMouseEvent pointerType pen · 마우스 page.mouse · 키보드 page.keyboard
         WebKit: 손가락 page.touchscreen.tap(톡만 — 두 손가락·길게·손바닥·끌기·펜은 Chromium 만) · 마우스·키보드
         el.click()·합성 dispatchEvent 없음(키보드 앞 focus() 한 번만 — 누름은 진짜 키) · 보임 = display ≠ none · 높이 > 0 · 화면 안
  몸통(서버 · 앱 흉내 網 · __P 도구)은 본판·add1 하네스를 그대로 불러 쓴다.

쓰기 : python _harness_jagwa_penfinger_add2.py [--new 파일] [--only chromium,webkit] [--apps BASE2,BASE3,NEW] [--out 결과파일]
        결과 = 본판 결과 파일(_harness_jagwa_penfinger_result.txt) 끝에 이어 붙인다(--out 이 있으면 그 파일에 새로)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기 헬퍼(_task_qa_slim2 A-1-2 · 옛 남 하네스 import 를 갈음)
import hashlib, io, json, os, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# ← jagwa/gigu/_harness_jagwa_penfinger.py:35-35 SAMPLE 사본(글자 그대로 · 갈래 ③ · JG 밖 — 띄우기가 아니라 옮기지 않음)
SAMPLE = {'bio': 'B20-57-05', 'earth': 'G11-48-03'}   # ★ jagwa_uid(9/29) — 옛 G57-05 · G48-03(문항 번호 새 꼴)
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEWF = ARG('--new', os.path.join(_roots.genie(), 'jagwa', 'index.html'))
OUTF = ARG('--out', os.path.join(HERE, '_harness_jagwa_penfinger_result.txt'))
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
APPS = [x for x in (ARG('--apps', '') or 'BASE2,BASE3,NEW').split(',') if x]
BASE3_REV, BASE3_MD5 = 'd27c43a', '91ebc381'
BASE2_REV, BASE2_MD5 = 'f497f05', '0c1f47dd30e0b0c551dfe46948b034bc'
RES = []


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, d[:320]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('NOTE | %s · %s | %s' % (grp, name, d[:320]), flush=True)


JS3 = r"""
Object.assign(window.__P,{
 nm(q){return q?(q.id?'#'+q.id:'')+(q.tagName||'').toLowerCase()+'.'+String(q.className&&q.className.baseVal!=null?q.className.baseVal:q.className||'').split(' ').join('.'):null},
 /* 뒷정리 — 글자 고치기·그림 막·떠 있는 창은 걷고, 처음부터 있는 창(#book · #bkq)은 숨기기만(지우면 교재 창이 다시 안 뜬다) */
 closeAll3(){document.querySelectorAll('#tfxSheet,#ocrrfz').forEach(x=>x.remove());
   try{if(typeof BK!=='undefined'&&BK.open&&typeof bkClose==='function')bkClose()}catch(e){}
   document.querySelectorAll('.sheet').forEach(x=>{if(x.id==='book'||x.id==='bkq')x.classList.add('hide');else x.remove()});return 1},
 zoomGet(){try{return Math.round(INKG_EA.pinch.get()*1000)/1000}catch(e){return null}},
 zoomReset(){try{const w=document.getElementById('cardwrap');if(w&&document.getElementById('card')){const r=w.getBoundingClientRect();INKG_EA.pinch.set(1,r.left+r.width/2,r.top+r.height/2)}}catch(e){}return __P.zoomGet()},
 topUnder(x,y){const c=document.getElementById('card'),ink=c&&c.querySelector('#qink');const top=document.elementFromPoint(x,y);let under=null;
   if(ink){const k=ink.style.pointerEvents;ink.style.pointerEvents='none';under=document.elementFromPoint(x,y);ink.style.pointerEvents=k}
   return {top:__P.nm(top),under:__P.nm(under)}},
 /* 두 요소 — 둘의 가운데가 창 가운데에 오게 굴린 뒤 각 가운데 점(둘 다 화면 안이어야) */
 pair(s1,s2){const c=document.getElementById('card');const e1=c.querySelector(s1),e2=c.querySelector(s2);if(!e1||!e2)return null;
   const w=document.getElementById('cardwrap'),wr=w.getBoundingClientRect(),r1=e1.getBoundingClientRect(),r2=e2.getBoundingClientRect();
   w.scrollTop+=(r1.top+r1.height/2+r2.top+r2.height/2)/2-(wr.top+wr.height/2);
   const a=e1.getBoundingClientRect(),b=e2.getBoundingClientRect();
   const A={x:Math.round(a.left+a.width/2),y:Math.round(a.top+a.height/2)},B={x:Math.round(b.left+b.width/2),y:Math.round(b.top+b.height/2)};
   return {a:Object.assign(A,__P.topUnder(A.x,A.y)),b:Object.assign(B,__P.topUnder(B.x,B.y)),on:[A,B].every(p=>p.y>90&&p.y<innerHeight-90),
     dist:Math.round(Math.hypot(A.x-B.x,A.y-B.y))}},
 /* 창 가운데로 굴리지 않고 찾는 펜 빈 자리(손바닥 둘레 90px 밖 · 밑에 진짜 단추 없음) */
 penSpotNS(sels,avoid){const c=document.getElementById('card'),ink=c.querySelector('#qink'),PH=typeof PEN_HIT!=='undefined'?PEN_HIT:undefined;
   for(const sel of sels){const e=c.querySelector(sel);if(!e)continue;const r=e.getBoundingClientRect();
     for(const fy of [.5,.3,.7])for(const fx of [.12,.25,.4,.55]){const x=Math.round(r.left+r.width*fx),y=Math.round(r.top+r.height*fy);
       if(y<=60||y>=innerHeight-60||x<10||x>innerWidth-90)continue;if(avoid&&Math.hypot(x-avoid.x,y-avoid.y)<90)continue;
       const u=ink?underInk(x,y,ink,PH):null;if(!u){const t=document.elementFromPoint(x,y);return {x,y,sel,top:__P.nm(t),inInk:!!(t&&t.closest&&t.closest('#qink'))}}}}
   return null},
 /* 창 쪽 click·pointerdown 기록(창 capture — 문서 capture 의 먹기보다 먼저 본다) */
 logOn(){if(window.__clog)return 1;window.__clog=[];window.__pdlog=[];
   addEventListener('click',e=>{__clog.push({t:Math.round(performance.now()),tr:e.isTrusted,d:e.detail,pt:e.pointerType||'',tg:__P.nm(e.target)})},true);
   addEventListener('pointerdown',e=>{__pdlog.push({pt:e.pointerType,w:Math.round(e.width),h:Math.round(e.height),syn:!!e.__syn,tg:__P.nm(e.target)})},true);return 1},
 clog(){const a=(window.__clog||[]).slice();if(window.__clog)window.__clog.length=0;return a},
 pdlog(){const a=(window.__pdlog||[]).slice();if(window.__pdlog)window.__pdlog.length=0;return a},
 zoom3(){const z=document.getElementById('ocrrfz');if(!z)return null;const im=z.querySelector('img');if(!im)return {vis:__P.vis(z),img:false};
   const r=im.getBoundingClientRect(),s=getComputedStyle(im),nw=im.naturalWidth,nh=im.naturalHeight;let cw=r.width,chh=r.height;
   if(s.objectFit==='contain'&&nw&&nh){const k=Math.min(r.width/nw,r.height/nh);cw=nw*k;chh=nh*k}
   return {vis:__P.vis(z)&&__P.vis(im),boxW:Math.round(r.width*10)/10,boxH:Math.round(r.height*10)/10,w:Math.round(cw*10)/10,h:Math.round(chh*10)/10,nw,nh,fit:s.objectFit,
     bg:s.backgroundColor,rad:[s.borderTopLeftRadius,s.borderTopRightRadius,s.borderBottomRightRadius,s.borderBottomLeftRadius],zbg:getComputedStyle(z).backgroundColor,
     want:Math.round(Math.min(innerWidth*.96,innerHeight*.92*nw/nh)*10)/10}},
 qtxtH(){const c=document.getElementById('card'),t=c&&c.querySelector('#qtxt');
   return t?{h:Math.round(t.getBoundingClientRect().height),sh:Math.round(parseFloat(t.style.height)||0),cardH:c.scrollHeight,txton:c.classList.contains('txton'),qtxt:typeof QTXT!=='undefined'?QTXT:null}:null},   /* h = 화면(카드 배율 곱함) · sh = 층 자체 높이 */
 tboxes(){const c=document.getElementById('card');return [...c.querySelectorAll('#qtxt .tbox')].map(b=>{const r=b.getBoundingClientRect();
   return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),vis:__P.vis(b),tx:__P.tx(b).slice(0,20)}})},
 spot(sel,fx,fy){const c=document.getElementById('card');const e=c.querySelector(sel);if(!e)return null;e.scrollIntoView({block:'center'});
   const r=e.getBoundingClientRect(),x=Math.round(r.left+r.width*(fx==null?.3:fx)),y=Math.round(r.top+Math.min(r.height-3,Math.max(3,r.height*(fy==null?.5:fy))));
   const t=document.elementFromPoint(x,y);return {x,y,top:__P.nm(t),inTxt:!!(t&&t.closest&&t.closest('#qtxt')),elH:Math.round(r.height)}},
 btn(id){const b=document.getElementById(id);if(!b)return null;const r=b.getBoundingClientRect();const x=Math.round(r.left+r.width/2),y=Math.round(r.top+r.height/2);
   return {x,y,vis:__P.vis(b),on:b.classList.contains('on'),top:__P.nm(document.elementFromPoint(x,y))}},
 solTabs(){const c=document.getElementById('card');return [...c.querySelectorAll('.soltabs button')].map(b=>{const x=c.querySelector('.soltx[data-st="'+b.dataset.st+'"]');
   return {st:b.dataset.st,t:__P.tx(b),on:b.classList.contains('on'),txVis:x?(!x.hidden&&x.getBoundingClientRect().height>0):null}})},
 bookVis(){const b=document.getElementById('book');if(!b)return null;const p=b.querySelector('.panel')||b,s=getComputedStyle(b),r=p.getBoundingClientRect();
   return {hide:b.classList.contains('hide'),disp:s.display,h:Math.round(r.height),vis:!b.classList.contains('hide')&&s.display!=='none'&&r.height>0}},
 qsvg(){try{qSvg();return +document.querySelector('#qink').getAttribute('height')}catch(e){return 'ERR '+e}}
});
"""


# _task_qa_fix1 §A-3(10/9) — 부팅 표지: 카드 층 문항 다 읽음(DATA_V) · 첫 syncRecords 끝(recBusy 거짓 · lastSync ≥ 쪽 열림 또는 recErr) — JG.P2 의 고정 2.5 초 뒤에 regress 에서만 더 기다린다(gate 무변)
_QF_BOOT = "()=>(typeof CARD_LAYER==='undefined'||!CARD_LAYER||typeof DATA_V==='undefined'||DATA_V>0)&&typeof recBusy!=='undefined'&&!recBusy&&((((typeof lsObj==='function'&&typeof SMETA_KEY!=='undefined')?(lsObj(SMETA_KEY).lastSync||0):0)>=performance.timeOrigin)||(typeof recErr!=='undefined'&&!!recErr))"


class P3(JG.P2):
    """한 판 · 한 과목 · 엔진 — add1 P2(820×1180 · 터치 켬) + 두 손가락 · 기록 도구"""
    def __init__(self, br, app, subj, tag, engine, vh=1180):
        super().__init__(br, app, subj, tag, engine, vh)
        if not QC.GATE:   # ★ _task_qa_fix1 §A-3 — 부하에서 늦는 문항 읽기 · 첫 동기화를 끝까지(표지가 오면 바로 · 상한 15 초)
            QC.until(self.pg, _QF_BOOT, 15000, 'penfinger_add2 부팅 — 카드 층 문항 다 읽음 · 첫 syncRecords 끝(JG.P2 고정 2.5 초 뒤)')
        self.pg.evaluate(JS3)
        self.pg.evaluate("()=>__P.logOn()")

    def t2(self, ty, pts, r=22):
        """CDP 터치 — pts = [(id, x, y), …] · touchEnd 는 빈 목록(남은 손가락 전부 뗌)"""
        self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': [
            {'x': x, 'y': y, 'radiusX': r, 'radiusY': r, 'id': i} for (i, x, y) in pts]})


def scen(br, app, tag, subj, engine):
    g = '%s %s %s' % (tag, engine, subj)
    u = SAMPLE[subj]
    cr = engine == 'chromium'
    QC.launch('base' if tag.startswith('BASE') else 'new')   # 셈(§B-4)
    p = P3(br, app, subj, 'a2_%s_%s_%s' % (tag, engine, subj), engine)

    def fresh(tool='pen', ans=False, pg=None):
        q = pg or p
        q.ev("()=>__P.closeAll3()"); q.ev("()=>__P.closeSheet()"); q.ev("()=>__P.zoomReset()")
        ok = q.ev("u=>__P.open(u)", u)
        if ans:
            q.ev("()=>__P.ans()")
        q.ev("m=>__P.tool(m)", tool); q.wait(300)
        QC.until(q.pg, "m=>{const c=document.getElementById('card');return !!c&&typeof TOOL!=='undefined'&&TOOL.mode===m&&(m!=='pen'||(!!c.querySelector('#qink')&&c.classList.contains('penon')))}", 5000,
                 'penfinger_add2 fresh — 문제 창 카드 · 도구 바뀜(펜 = 덮개 #qink · penon) · _task_qa_fix1 §A-3(10/8 웹킷 생물 0 「ink null」 · 고정 300ms 뒤 · 안 오면 상한 뒤 그대로)', arg=tool)
        q.ev("()=>__P.clog()"); q.ev("()=>__P.pdlog()")
        return ok

    def unpicked(s):
        return next(c for c in (3, 2, 4, 1, 5) if c not in (s['pick'] or []))

    try:
        ok = fresh('pen')
        s0 = p.ev("()=>__P.st()")
        T(g, '0 %s 문제 창 · 펜 도구(덮개가 카드를 덮는다) · 확대 1' % u,
          ok and s0['mode'] == 'pen' and (p.ev("()=>__P.ink()") or {}).get('penon') and p.ev("()=>__P.zoomGet()") == 1,
          {'mode': s0['mode'], 'ink': p.ev("()=>__P.ink()"), 'z': p.ev("()=>__P.zoomGet()")})
        if QC.SMOKE:   # smoke — 0(펜 도구 덮개 · 확대 1) + Z(페이지 오류 0)만
            er = p.errs + (p.ev("()=>__P.errs()") or [])
            T(g, 'Z 페이지 오류 0', not er, er[:5])
            return
        if cr:
            # ── 1 D1 — 두 손가락 벌림 900ms(둘째 손가락 40ms 뒤) · ①+⑤ · 문제 글+〈보기〉 ㄴ ──
            r1, ok1 = {}, True
            for nm, s1, s2 in (('①+⑤', '.choices button[data-c="1"]', '.choices button[data-c="5"]'),
                               ('문제 글+〈보기〉ㄴ', '.q', '.bogi .row[data-k="ㄴ"] .t')):
                fresh('pen')
                s = p.ev("()=>__P.st()")
                pr = p.ev("a=>__P.pair(a[0],a[1])", [s1, s2])
                if not pr or not pr['on']:
                    r1[nm] = {'자리 없음': pr}; ok1 = False; continue
                a, b = pr['a'], pr['b']
                p.t2('touchStart', [(1, a['x'], a['y'])]); p.wait(40)
                p.t2('touchStart', [(1, a['x'], a['y']), (2, b['x'], b['y'])])
                n, D = 18, 70
                for i in range(1, n + 1):
                    p.t2('touchMove', [(1, a['x'], round(a['y'] - D * i / n)), (2, b['x'], round(b['y'] + D * i / n))]); p.wait(50)
                p.wait(150)
                mid = {'창': p.ev("()=>__P.sheets()"), 'z': p.ev("()=>__P.zoomGet()"), 'sheet': p.ev("()=>__P.st()")['sheet']}
                p.t2('touchEnd', []); p.wait(700)
                t = p.ev("()=>__P.st()")
                pd = p.ev("()=>__P.pdlog()")
                r = {'시작': {'1': [a['top'], a['under']], '2': [b['top'], b['under']], '사이': pr['dist']}, '확대': [1, mid['z']],
                     '창(누른 채)': [mid['창'], mid['sheet']], '창(뗀 뒤)': [p.ev("()=>__P.sheets()"), t['sheet']], 'pick': [s['pick'], t['pick']],
                     '누름': [(x['pt'], x['w'], x['syn']) for x in pd]}
                r1[nm] = r
                ok1 = ok1 and mid['창'] == 0 and r['창(뗀 뒤)'][0] == 0 and (mid['z'] or 0) > 1.05 and t['pick'] == s['pick']
                p.ev("()=>__P.closeSheet()")
            T(g, '1 D1 펜 도구 · 두 손가락 900ms 벌림(①+⑤ · 문제 글+〈보기〉 ㄴ) → 글자 고치기 창 0(누른 채·뗀 뒤) · 확대됨(> 1.05) · 고름 무변(헛잣대: 바탕 d27c43a = 창 뜸 · f497f05 = PASS = add1 회귀 확인)', ok1, r1)
            # ── 1b 두 손가락이 다 떨어지면 풀린다 — 곧이어 한 손가락 톡 → 골라짐(무변 잣대 · 새 깃발이 안 남는지) ──
            fresh('pen')
            s = p.ev("()=>__P.st()"); c1 = unpicked(s)
            a = p.ev("c=>__P.at('.choices button[data-c=\"'+c+'\"]',.5,.5)", c1)
            p.ftap(a['x'], a['y']); t = p.ev("()=>__P.st()")
            T(g, '1b 두 손가락을 뗀 뒤 한 손가락 톡 · 선택지(%s) → 골라짐 · 창 0(무변 잣대 — BASE2 는 add1 앞이라 덮개 밑 톡이 원래 안 됨)' % c1, t['pick'] == [c1] and not t['sheet'],
              {'pick': [s['pick'], t['pick']], '위': a['top'], '밑': a['under'], 'sheet': t['sheet']})
            # ── 2 손바닥 먼저 — 넓은 접촉(반지름 40) 700ms → 창 0 · 얹은 채 펜 획 +1 보임 · 뗀 뒤도 창 0 · 안 골라짐 ──
            r2, ok2 = {}, True
            for nm in ('문제 글', '선택지'):
                fresh('pen')
                s = p.ev("()=>__P.st()"); c2 = unpicked(s)
                a = p.ev("()=>__P.at('.q',.72,.5)") if nm == '문제 글' else p.ev("c=>__P.at('.choices button[data-c=\"'+c+'\"]',.5,.5)", c2)
                sp = p.ev("a=>__P.penSpotNS(['.q','.bogi','.choices','.ggwrap'],a)", {'x': a['x'], 'y': a['y']})
                if not sp:
                    r2[nm] = {'펜 자리 없음': a}; ok2 = False; continue
                p.t2('touchStart', [(1, a['x'], a['y'])], r=40); p.wait(700)
                n_in = [p.ev("()=>__P.sheets()"), p.ev("()=>__P.st()")['sheet']]
                p.pdrag(sp['x'], sp['y'], sp['x'] + 70, sp['y'] + 2)
                t = p.ev("()=>__P.st()"); ls = p.ev("()=>__P.lastStroke()")
                p.t2('touchEnd', [], r=40); p.wait(600)
                t2 = p.ev("()=>__P.st()")
                pd = p.ev("()=>__P.pdlog()")
                r = {'손바닥': [a['top'], a['under']], '접촉 폭': [(x['pt'], x['w'], x['h']) for x in pd if x['pt'] == 'touch' and not x['syn']],
                     '창(700ms)': n_in, '획': [s['strokes'], t['strokes']], '획 상자': ls, '펜 자리': [sp['sel'], sp['top']],
                     '창(뗀 뒤)': [p.ev("()=>__P.sheets()"), t2['sheet']], 'pick': [s['pick'], t2['pick']]}
                r2[nm] = r
                ok2 = ok2 and n_in[0] == 0 and t['strokes'] == s['strokes'] + 1 and bool(ls) and ls['w'] >= 50 and ls['on'] \
                    and r['창(뗀 뒤)'][0] == 0 and t2['pick'] == s['pick']
                p.ev("()=>__P.closeSheet()")
            T(g, '2 손바닥 먼저 — 펜 도구 · 넓은 접촉(반지름 40) 700ms 문제 글·선택지 위 → 창 0 · 얹은 채 펜 획 +1 보임 · 뗀 뒤 창 0 · 안 골라짐(헛잣대: 바탕 d27c43a·f497f05 = 창 뜸 · 획 0)', ok2, r2)
        # ── 3 D2 참고 그림(생물) — 그림 자체 흰 바탕·둥근 6 · 그림 상자 = 그림(가장자리 빈 칸 없음) · 크기 add1 관문 8 그대로 · 바깥 톡 닫힘 ──
        if subj == 'bio':
            r3 = {}
            for tool in ('pen', 'view'):
                fresh(tool, ans=True)
                im = p.ev("()=>__P.refImg()")
                if not im:
                    r3[tool] = '그림 못 받음'; continue
                p.ftap(im['x'], im['y']); z = p.ev("()=>__P.zoom3()")
                p.ftap(8, 8); z2 = p.ev("()=>__P.zoom3()")
                r3[tool] = {'그림 위': im['top'], '크게': z, '바깥 톡 뒤': z2}
                p.ev("()=>__P.closeAll3()")
            good = lambda v: isinstance(v, dict) and bool(v.get('크게')) and v['크게'].get('vis') and v['크게']['bg'] == 'rgb(255, 255, 255)' \
                and v['크게']['rad'] == ['6px'] * 4 and abs(v['크게']['boxW'] - v['크게']['w']) <= 1 and abs(v['크게']['boxH'] - v['크게']['h']) <= 1 \
                and v['크게']['w'] >= v['크게']['want'] - 2 and v.get('바깥 톡 뒤') is None
            T(g, '3 D2 참고 그림 손가락 톡(펜·보기 도구) → 그림 computed 바탕 흰색 · 모서리 6px 넷 · 그림 상자 = 그린 그림(±1px) · 폭 ≥ min(96vw, 92vh×비율) − 2 · 바깥 톡 닫힘(헛잣대: 바탕 d27c43a = 투명 · 96vw×92vh 상자)',
              good(r3.get('pen')) and good(r3.get('view')), r3)
        # ── 4 D4 — 덮개 밑 톡(〈보기〉 O) 직후 0.7초 안 키보드 Enter 로 「정답·해설」 단추 → 동작함 ──
        #    Chromium = 1.1초 길게 톡(크롬 길게 누르기 — 뒤따르는 진짜 click 이 없다 · 아이패드 사파리도 길게 누르면 click 이 없다)
        #    WebKit = 보통 톡(진짜 click 이 따라온다 — 그 click 이 먹힘 한 번을 쓰므로 바탕도 안 먹힐 수 있다 · 결과로 가른다)
        fresh('pen', ans=True)
        rows = p.ev("()=>__P.oxRows()") or []
        if rows:
            k = rows[0]
            a = p.ev("s=>__P.at(s,.5,.5)", '.bogi .row[data-k="%s"] .ox button[data-v="O"]' % k)
            o0 = p.ev("k=>__P.ox(k)", k); d0 = p.ev("()=>__P.det()")
            p.ev("()=>__P.clog()")
            if cr:
                p.t2('touchStart', [(1, a['x'], a['y'])]); p.wait(60); p.t2('touchEnd', [])
            else:
                p.pg.touchscreen.tap(a['x'], a['y'])
            t_up = time.time(); p.wait(150)
            o1 = p.ev("k=>__P.ox(k)", k)
            p.ev("()=>{const b=document.getElementById('cDetBtn');b.focus();return document.activeElement===b}")   # 키보드 초점만 — 누름은 진짜 키
            p.pg.keyboard.press('Enter'); dt = round(time.time() - t_up, 3)
            p.wait(400)
            d1 = p.ev("()=>__P.det()"); cl = p.ev("()=>__P.clog()")
            on = lambda o: [x['v'] for x in (o or []) if x['on']]
            if ('O' in on(o1)) == ('O' in on(o0)):   # ★ _task_qa_fix1 §A-3 — 톡 뒤 150ms 에 O 가 아직 안 바뀌었으면(10/8 웹킷 지학 4a 「O [[], []]」) 키 타이밍(dt)은 그대로 두고 O 만 표지로 더 기다려 다시 잰다
                QC.until(p.pg, "a=>(__P.ox(a[0])||[]).some(x=>x.v==='O'&&x.on)!==a[1]", 3000, 'penfinger_add2 4a 덮개 밑 톡 → 〈보기〉 O 바뀜', arg=[k, 'O' in on(o0)])
                o1 = p.ev("k=>__P.ox(k)", k)
            r4 = {'톡': 'CDP 톡' if cr else 'touchscreen.tap', '위': a['top'], '밑': a['under'], 'O': [on(o0), on(o1)],
                  '정답·해설': [d0, d1], 'Enter 까지 초': dt, 'click': cl}
            T(g, '4a D4 덮개 밑 톡(〈보기〉 %s O) 직후 %.2f초 키보드 Enter → 「정답·해설」 여닫힘(헛잣대: 웹킷 바탕 d27c43a = 톡 뒤 진짜 click 이 없어 남은 먹기가 키보드 click 을 먹음 · 크롬은 진짜 touch click 이 먹기를 써서 바탕도 안 먹힘 → 크롬 헛잣대는 4b)' % (k, dt),
              (('O' in on(o1)) != ('O' in on(o0))) and d1 != d0 and dt < 0.65, r4)
        else:
            N(g, '4a 〈보기〉 O/△/X 칸 없음', rows)
        if cr:
            # ── 4b D4 — 덮개 밑 문제 글 왼쪽 끝을 손가락 700ms → 「✎ 글자 고치기」 창 → 뗀 뒤 곧바로 창 「닫기」에 키보드 Enter → 창 닫힘 ──
            #    뗀 손가락의 진짜 click 은 창 바탕에 떨어져 창 먹기(A'')가 가져간다 → 덮개 밑 톡의 먹기 한 번(tapT)이 남은 채 키보드 click 이 온다
            #    = D4 가 실제로 먹히는 꼴(아이패드는 길게 누른 톡 뒤 click 이 아예 없다 · 헤드리스 크롬은 보통 톡도 click 을 내서 4a 로는 헛잣대가 안 선다)
            fresh('pen')
            a = p.ev("()=>__P.at('.q',.02,.5)")   # 왼쪽 끝 — 창 판(가운데) 밖 = 창 바탕
            p.ev("()=>__P.clog()")
            p.t2('touchStart', [(1, a['x'], a['y'])]); p.wait(700)
            n_in = p.ev("()=>__P.sheets()")
            p.t2('touchEnd', []); t_up = time.time(); p.wait(120)
            top_up = p.ev("a=>__P.nm(document.elementFromPoint(a.x,a.y))", {'x': a['x'], 'y': a['y']})
            fo = p.ev("()=>{const b=document.querySelector('#tfxSheet #tfxNo');if(!b)return false;b.focus();return document.activeElement===b}")
            p.pg.keyboard.press('Enter'); dt = round(time.time() - t_up, 3)
            p.wait(400)
            n_out = p.ev("()=>__P.sheets()"); cl = p.ev("()=>__P.clog()")
            onbd = any(c['pt'] == 'touch' and (c['tg'] or '').startswith('#tfxSheet') for c in cl)
            r4b = {'누른 곳': [a['top'], a['under'], a['x'], a['y']], '창(700ms)': n_in, '뗀 자리 맨 위': top_up, '닫기 초점': fo, 'Enter 까지 초': dt,
                   '창(Enter 뒤)': n_out, '진짜 click 이 창 바탕에': onbd, 'click': cl}
            T(g, '4b D4 덮개 밑 문제 글 손가락 700ms → 글자 고치기 창 → 뗀 뒤 %.2f초 「닫기」에 키보드 Enter → 창 닫힘(헛잣대: 바탕 d27c43a = 남은 먹기가 키보드 click 을 먹어 창이 남음)' % dt,
              n_in == 1 and fo and onbd and n_out == 0 and dt < 0.65, r4b)
        # ── 6a D3 — add1 관문 3a 다시: 펼친 해설 안 덮개 **밑** 단추(생물 = 해설 탭 · 지학 = 교재/부록 쪽 칩) 손가락 톡 → 제 동작 ──
        fresh('pen', ans=True)
        hq = p.ev("()=>__P.qsvg()")   # 덮개를 펼친 카드 높이로(add1 앞 판 f497f05 는 펼쳐도 안 늘어난다 — 「덮개 밑」 조건을 세 판 같게)
        if subj == 'bio':
            tabs = p.ev("()=>__P.solTabs()") or []
            off = next((x for x in tabs if not x['on']), None)
            if off:
                a = p.ev("s=>__P.at(s,.5,.5)", '.soltabs button[data-st="%s"]' % off['st'])
                p.ftap(a['x'], a['y']); t6 = p.ev("()=>__P.solTabs()")
                hit = next((x for x in t6 if x['st'] == off['st']), {})
                T(g, '6a D3 펼친 해설 탭 「%s」(덮개 밑) 손가락 톡 → 그 탭 켜짐 · 그 해설 보임(헛잣대: add1 앞 판 f497f05 = 무반응)' % off['t'],
                  'qink' in (a['top'] or '') and hit.get('on') and hit.get('txVis'), {'덮개 높이': hq, '위': a['top'], '밑': a['under'], '탭': [tabs, t6]})
            else:
                N(g, '6a 해설 탭 없음', tabs)
        else:
            a = p.ev("()=>__P.at('.sol .jump .tag.page',.5,.5)")
            if a:
                b0 = p.ev("()=>__P.bookVis()")
                p.ftap(a['x'], a['y']); p.wait(600); b1 = p.ev("()=>__P.bookVis()")
                T(g, '6a D3 펼친 해설 「교재/부록 쪽」 칩(덮개 밑) 손가락 톡 → 교재 창 보임(헛잣대: add1 앞 판 f497f05 = 무반응)',
                  'qink' in (a['top'] or '') and not (b0 or {}).get('vis') and (b1 or {}).get('vis'), {'덮개 높이': hq, '위': a['top'], '밑': a['under'], '교재 창': [b0, b1]})
                p.ev("()=>__P.closeAll3()")
            else:
                N(g, '6a 교재/부록 쪽 칩 없음', a)
        if cr:
            # ── 6b D3 — add1 관문 4 다시: 같은 덮개 밑 선택지 — 끌면 굴림(안 골라짐 · 창 0) · 톡 하면 골라짐 ──
            #    (add1 앞 판은 덮개 밑으로 손가락을 한 번도 안 넘겨 끌기는 늘 굴림이다 — 끌기만으로는 헛잣대가 안 선다 · 같은 자리 톡을 짝으로)
            QC.launch('base' if tag.startswith('BASE') else 'new')   # 셈(§B-4)
            q7 = P3(br, app, subj, 'a2_%s_%s_%s_700' % (tag, engine, subj), engine, vh=700)
            try:
                fresh('pen', ans=True, pg=q7)
                s = q7.ev("()=>__P.st()"); c4 = unpicked(s)
                a = q7.ev("c=>__P.at('.choices button[data-c=\"'+c+'\"]',.5,.5)", c4)
                s = q7.ev("()=>__P.st()")
                mx = s['sh'] - s['ch']
                dy = -40 if s['top'] + 40 <= mx else (40 if s['top'] >= 40 else 0)
                q7._t('touchStart', [(a['x'], a['y'])], 22)
                for i in range(1, 15):
                    q7._t('touchMove', [(a['x'], a['y'] + dy * i / 14)], 22); q7.wait(50)
                for _ in range(5):
                    q7._t('touchMove', [(a['x'], a['y'] + dy)], 22); q7.wait(30)
                q7._t('touchEnd', [], 22); q7.wait(800)
                t = q7.ev("()=>__P.st()")
                a2 = q7.ev("c=>__P.at('.choices button[data-c=\"'+c+'\"]',.5,.5)", c4)
                q7.ftap(a2['x'], a2['y']); t2 = q7.ev("()=>__P.st()")
                r6b = {'표적': c4, '굴릴 자리': mx, '끈 쪽': dy, '굴림': [s['top'], t['top']], 'pick': [s['pick'], t['pick'], t2['pick']],
                       '창': [t['sheet'], t2['sheet']], '위': [a['top'], a2['top']], '밑': [a['under'], a2['under']]}
                T(g, '6b D3 펜 도구 · 덮개 밑 선택지(%s) — 40px 끌기(700ms) → 굴림 ≥ 25 · 안 골라짐 · 창 0 / 0.8초 뒤 같은 선택지 톡 → 골라짐(헛잣대: add1 앞 판 f497f05 = 톡 무반응)' % c4,
                  dy != 0 and abs(t['top'] - s['top']) >= 25 and t['pick'] == s['pick'] and not t['sheet'] and t2['pick'] == [c4] and not t2['sheet'], r6b)
                q7.ev("()=>__P.closeSheet()")
            finally:
                q7.close()
            # ── 6c 길게 누르기 무변 — 문제 글 손가락 600ms → 글자 고치기 한 번 · 뗀 뒤에도 남음(펜·보기) ──
            r6 = {}
            for tool in ('pen', 'view'):
                fresh(tool)
                a = p.ev("()=>__P.at('.q',.3,.5)")
                p._t('touchStart', [(a['x'], a['y'])], 22); p.wait(600)
                n_in = p.ev("()=>__P.sheets()")
                p._t('touchEnd', [], 22); p.wait(500)
                r6[tool] = {'누른 채': n_in, '뗀 뒤': p.ev("()=>__P.sheets()"), 'sheet': p.ev("()=>__P.st()")['sheet'], '위': a['top']}
                p.ev("()=>__P.closeSheet()")
            T(g, '6c 문제 글 손가락 600ms → 「✎ 글자 고치기 — 문제」 한 번 · 뗀 뒤에도 남음 — 펜·보기 도구(무변 잣대 · 세 판 PASS)',
              all(v['누른 채'] == 1 and v['뗀 뒤'] == 1 and v['sheet'] == '✎ 글자 고치기 — 문제' for v in r6.values()), r6)
        # ── 5 #qtxt — 글상자 켠 채 「정답·해설」 펼침 → 해설 글 위 마우스 톡 → 새 글상자 보임 · 글자 들어감 ──
        fresh('view')
        tb = p.ev("()=>__P.btn('tTxt')")
        if tb and tb['vis']:
            p.pg.mouse.click(tb['x'], tb['y']); p.wait(300)
            h0 = p.ev("()=>__P.qtxtH()")
            a = p.ev("()=>__P.at('#cDetBtn',.5,.5)")
            p.pg.mouse.click(a['x'], a['y']); p.wait(700)
            h1 = p.ev("()=>__P.qtxtH()"); d1 = p.ev("()=>__P.det()")
            sp = p.ev("()=>__P.spot('.sol .soltx',.3,.4)") or p.ev("()=>__P.spot('.sol',.3,.6)")
            n0 = p.ev("()=>__P.tboxes()") or []
            if cr:
                p.pg.mouse.click(sp['x'], sp['y'])      # 책상 = 마우스
            else:
                p.pg.touchscreen.tap(sp['x'], sp['y'])  # 아이패드 = 손가락 톡(웹킷 마우스는 기본 동작이 새 글상자 초점을 빼앗아 글자가 안 들어간다 — 앱 무관 · 첫 판)
            p.wait(400)
            p.pg.keyboard.type('ab'); p.wait(400)
            n1 = p.ev("()=>__P.tboxes()") or []
            new = [x for x in n1 if x not in n0]
            r5 = {'글상자 단추': tb, '높이(켠 뒤·펼친 뒤)': [h0, h1], '펼침': d1, '톡 자리': sp, '글상자': [len(n0), len(n1)], '새 것': new}
            T(g, '5 #qtxt 글상자 켬 → 「정답·해설」 펼침 → 해설 글 위 톡(크롬 마우스 · 웹킷 손가락) → 새 글상자 +1 보임 · 층 높이 = 카드 높이 · 글자 「ab」(크롬만 — 웹킷은 바탕 d27c43a 도 새 글상자에 키 입력이 안 들어감 · 앱 무관 · 값은 새 것.tx)(헛잣대: 바탕 = 글상자 층이 펼치기 전 높이 · 0)',
              d1 and sp.get('inTxt') and len(n1) == len(n0) + 1 and len(new) == 1 and new[0]['vis'] and ('ab' in new[0]['tx'] or not cr) and abs(new[0]['y'] - sp['y']) <= 40
              and (h1 or {}).get('sh', 0) >= (h1 or {}).get('cardH', 1e9) - 2, r5)
            p.pg.mouse.click(tb['x'], tb['y']); p.wait(200)   # 글상자 끔
        else:
            N(g, '5 글상자 단추(#tTxt) 없음', tb)
        er = p.errs + (p.ev("()=>__P.errs()") or [])
        T(g, 'Z 페이지 오류 0', not er, er[:5])
    except Exception as ex:
        T(g, '묶음 예외', False, repr(ex)[:400])
    finally:
        p.close()


def report(t0, md5s, engines):
    lines = ['', '# ─── add2(9/27 · _task_jagwa_penfinger_add2) — %s ───' % time.strftime('%Y-%m-%d %H:%M'),
             'NEW = %s (md5(LF) %s) · BASE3 = genie %s (md5(LF) %s · add1 인도판) · BASE2 = genie %s (md5(LF) %s · 본판 인도판) · 엔진 %s · 820×1180 · 표본 생물 G57-05 · 지학 G48-03'
             % (NEWF, md5s['NEW'][:8], BASE3_REV, md5s['BASE3'][:8], BASE2_REV, md5s['BASE2'][:8], '+'.join(engines)),
             '입력 = Chromium CDP 터치(반지름 22 · 두 손가락 id 1·2 · 손바닥 반지름 40)·CDP 펜·page.mouse·page.keyboard · WebKit touchscreen.tap·mouse·keyboard — 합성 이벤트·el.click 없음', '']
    for grp, name, ok, d in RES:
        dd = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)
        lines.append('%s | %s · %s | %s' % ('NOTE' if ok is None else 'PASS' if ok else 'FAIL', grp, name, dd[:900]))
    cnt = lambda pre: (sum(1 for x in RES if x[2] is True and x[0].startswith(pre)), sum(1 for x in RES if x[2] is False and x[0].startswith(pre)))
    np_, nf = cnt('NEW')
    # 헛잣대 — 바탕 판마다 FAIL 이어야 할 칸(그 밖 칸은 PASS 여야 · 무변 잣대)
    #    WebKit 은 덮개 밑 톡 뒤 진짜 click 이 안 와서(아이패드와 같은 꼴) 보통 톡(4a)에서 바탕이 키보드 click 을 먹는다 = 헛잣대 · 크롬은 진짜 click 이 먹기를 써서 4b 가 세운다
    EXPECT_FAIL = {('BASE3', 'chromium'): {'1', '2', '3', '4b', '5'},       # add2 가 고친 칸
                   ('BASE3', 'webkit'): {'3', '4a', '5'},
                   ('BASE2', 'chromium'): {'1b', '2', '3', '4a', '5', '6a', '6b'},   # add1 앞 판 — 덮개 밑 톡이 원래 없음(1b·4a·6a·6b) · 손바닥 · 그림 크기 · 글상자
                   ('BASE2', 'webkit'): {'3', '4a', '5', '6a'}}
    null = {}
    for pre in ('BASE3', 'BASE2'):
        good, bad = 0, []
        for grp, name, ok, _ in RES:
            if ok is None or not grp.startswith(pre):
                continue
            gid = name.split(' ')[0]
            eng = grp.split(' ')[1]
            exp_fail = gid in EXPECT_FAIL.get((pre, eng), set())
            if (not ok) == exp_fail:
                good += 1
            else:
                bad.append('%s %s(%s)' % (grp.split(' ', 1)[1], gid, 'PASS' if ok else 'FAIL'))
        null[pre] = (good, bad)
    b3p, b3f = cnt('BASE3')
    b2p, b2f = cnt('BASE2')
    lines += ['', 'add2 헛잣대(BASE3 d27c43a) — PASS %d · FAIL %d · 기대와 맞음 %d · 어긋남 %s (FAIL 이어야: 크롬 1·2·3·4b·5 · 웹킷 3·4a·5 · 나머지 PASS)' % (b3p, b3f, null['BASE3'][0], null['BASE3'][1] or 0),
              'add2 헛잣대(BASE2 f497f05) — PASS %d · FAIL %d · 기대와 맞음 %d · 어긋남 %s (FAIL 이어야: 크롬 1b·2·3·4a·5·6a·6b · 웹킷 3·4a·5·6a · 1 = PASS = add1 회귀 확인)' % (b2p, b2f, null['BASE2'][0], null['BASE2'][1] or 0),
              'add2 합계(NEW)  PASS %d · FAIL %d  (%.0f초)' % (np_, nf, time.time() - t0)]
    txt = '\n'.join(lines) + '\n'
    old = '' if ARG('--out') else (io.open(OUTF, encoding='utf-8').read() if os.path.exists(OUTF) else '')
    out = old.rstrip('\n') + '\n' + txt if old else txt.lstrip('\n')
    for _ in range(3):
        io.open(OUTF, 'w', encoding='utf-8', newline='\n').write(out); time.sleep(0.5)
        if io.open(OUTF, encoding='utf-8').read() == out:
            break
    print('\n'.join(lines[-3:]))
    return nf


def main():
    t0 = time.time()
    apps, md5s = {}, {}
    new = io.open(NEWF, encoding='utf-8', newline='').read()
    apps['NEW'] = new
    if QC.GATE:
        for nm, rev in (('BASE3', BASE3_REV), ('BASE2', BASE2_REV)):
            QC.sub('git:show-app')
            apps[nm] = subprocess.run(['git', '-C', _roots.genie(), 'show', rev + ':jagwa/index.html'], capture_output=True).stdout.decode('utf-8')
    for nm, t in apps.items():
        md5s[nm] = hashlib.md5(t.replace('\r\n', '\n').encode('utf-8')).hexdigest()
    if QC.GATE:
        T('땅값', 'BASE3 = add1 인도판(d27c43a · 91ebc381) · BASE2 = 본판 인도판(f497f05 · 0c1f47dd) · NEW 는 add2 표시가 있다',
          md5s['BASE3'].startswith(BASE3_MD5) and md5s['BASE2'] == BASE2_MD5 and '★ penfinger add2' in new and '★ penfinger add2' not in apps['BASE3'],
          {k: v[:8] for k, v in md5s.items()})
    else:   # regress · smoke — 바탕 판 둘 풀기 0 · 땅값 칸 = 관문만 · report 머리 줄 자리만 채움
        md5s.update({'BASE3': '(regress)', 'BASE2': '(regress)'})
    engines = [e for e in ('chromium', 'webkit') if (not ONLY or e in ONLY) and (e == 'chromium' or not QC.SMOKE)]   # smoke — Chromium 만
    with sync_playwright() as pw:
        for eng in engines:
            br = getattr(pw, eng).launch()
            for subj in (('bio', 'earth') if not QC.SMOKE else ('bio',)):   # smoke — 생물 한 번
                for nm in (('BASE2', 'BASE3', 'NEW') if QC.GATE else ('NEW',)):   # regress — 바탕 판 둘(헛잣대 측정 줄) 안 돎
                    if nm in APPS:
                        scen(br, apps[nm], nm, subj, eng)
            br.close()
    return report(t0, md5s, engines)


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
