# -*- coding: utf-8 -*-
r"""_task_jagwa_penfinger_add1 §D 관문 — 펜 도구일 때 손가락 톡(선택지 · 〈보기〉 O/△/X · 「정답·해설」·칩) · 끌기 = 굴림 · 손바닥 ·
    길게 누르기 무변 · 펼친 뒤 펜 · 참고 그림 크게 — Chromium + WebKit · 아이패드 세로 820×1180

  NEW   = --new <파일>(없으면 genie 작업트리 jagwa/index.html)
  BASE2 = genie f497f05 blob(본판 인도판 · md5(LF) 0c1f47dd = 0d4144c 판) — 칸마다 헛잣대(고친 칸은 여기서 FAIL 이어야)
  입력 = 진짜 포인터 — Chromium: 손가락 CDP Input.dispatchTouchEvent(radiusX·Y 22) · 펜 CDP Input.dispatchMouseEvent pointerType pen
                        WebKit: 손가락 page.touchscreen.tap(진짜 터치 톡 · WebKit 프로토콜은 톡만 낸다 — 끌기·길게·펜은 Chromium 만)
         el.click()·합성 dispatchEvent 없음 · 보임 = display ≠ none · 높이 > 0 · 화면 안
  몸통(서버 · 앱 흉내 網 · __P 도구)은 본판 하네스(_harness_jagwa_penfinger.py)를 그대로 불러 쓴다.

쓰기 : python _harness_jagwa_penfinger_add1.py [--new 파일] [--only chromium,webkit] [--out 결과파일]
        결과 = 본판 결과 파일(_harness_jagwa_penfinger_result.txt) 끝에 이어 붙인다(--out 이 있으면 그 파일에 새로)
"""
import hashlib, io, json, os, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _harness_jagwa_penfinger as H   # noqa: E402
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEWF = ARG('--new', os.path.join(H.GENIE, 'jagwa', 'index.html'))
OUTF = ARG('--out', os.path.join(HERE, '_harness_jagwa_penfinger_result.txt'))
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
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


JS2 = r"""
Object.assign(window.__P,{
 vis(el){if(!el||!el.isConnected)return false;const s=getComputedStyle(el);if(s.display==='none'||s.visibility==='hidden')return false;
   const r=el.getBoundingClientRect();if(!(r.height>0&&r.width>0))return false;return r.bottom>0&&r.right>0&&r.top<innerHeight&&r.left<innerWidth},
 picks(){const c=document.getElementById('card');return [...c.querySelectorAll('.choices button.pick')].map(b=>({c:+b.dataset.c,vis:__P.vis(b)}))},
 ox(k){const c=document.getElementById('card');const row=[...c.querySelectorAll('.bogi .row')].find(r=>r.dataset.k===k);if(!row)return null;
   return [...row.querySelectorAll('.ox button')].map(b=>({v:b.dataset.v,on:b.classList.contains('on'),vis:__P.vis(b)}))},
 oxRows(){const c=document.getElementById('card');return [...c.querySelectorAll('.bogi .row')].filter(r=>r.querySelector('.ox button')).map(r=>r.dataset.k)},
 sheet(){const s=[...document.querySelectorAll('.sheet')].filter(x=>x.id!=='tfxSheet').pop();return s?{h2:__P.tx(s.querySelector('h2')),vis:__P.vis(s.querySelector('.panel')||s)}:null},
 sheetsAll(){return document.querySelectorAll('.sheet').length},
 closeAll(){document.querySelectorAll('.sheet,#ocrrfz').forEach(x=>x.remove());return 1},
 det(){const d=document.getElementById('cDet');return !!(d&&d.open)},
 detClose(){const d=document.getElementById('cDet');if(d)d.open=false;return 1},
 ink(){const c=document.getElementById('card'),sv=c&&c.querySelector('#qink');if(!sv)return null;const r=sv.getBoundingClientRect();
   return {h:+sv.getAttribute('height'),cardH:c.scrollHeight,bottom:Math.round(r.bottom),penon:c.classList.contains('penon')}},
 lastStroke(){const ps=[...document.querySelectorAll('#qink path[data-j]')];const p=ps.pop();if(!p)return null;const b=p.getBoundingClientRect();
   return {n:ps.length+1,w:Math.round(b.width),h:Math.round(b.height),x:Math.round(b.left),y:Math.round(b.top),on:b.bottom>0&&b.top<innerHeight&&b.right>0&&b.left<innerWidth}},
 /* 참고 그림 — 받아질 때까지 기다린 뒤 창 가운데로 굴리고 가운데 점 */
 async refImg(){const t0=Date.now();let im=null;
   while(Date.now()-t0<15000){im=document.querySelector('#card .rfimg img');if(im&&im.complete&&im.naturalWidth>0)break;await new Promise(r=>setTimeout(r,100))}
   if(!im||!im.naturalWidth)return null;im.scrollIntoView({block:'center'});await new Promise(r=>setTimeout(r,200));
   const r=im.getBoundingClientRect();const x=Math.round(r.left+r.width/2),y=Math.round(r.top+r.height/2);const top=document.elementFromPoint(x,y);
   return {x,y,w:Math.round(r.width),nw:im.naturalWidth,nh:im.naturalHeight,top:top?(top.id||top.tagName.toLowerCase()):null}},
 zoom(){const z=document.getElementById('ocrrfz');if(!z)return null;const im=z.querySelector('img');const r=im.getBoundingClientRect();const s=getComputedStyle(im);
   const nw=im.naturalWidth,nh=im.naturalHeight;let cw=r.width,chh=r.height;
   if(s.objectFit==='contain'&&nw&&nh){const k=Math.min(r.width/nw,r.height/nh);cw=nw*k;chh=nh*k}
   return {vis:__P.vis(z),boxW:Math.round(r.width),boxH:Math.round(r.height),w:Math.round(cw*10)/10,h:Math.round(chh*10)/10,nw,nh,fit:s.objectFit,
     want:Math.round(Math.min(innerWidth*.96,innerHeight*.92*nw/nh)*10)/10,vw:innerWidth,vh:innerHeight}},
 /* 획을 그을 빈 자리 — 그 요소 안에서 밑에 진짜 단추(PEN_HIT)가 없는 점 */
 penSpot(sel){const c=document.getElementById('card');const e=c.querySelector(sel);if(!e)return null;e.scrollIntoView({block:'center'});
   const r=e.getBoundingClientRect(),ink=c.querySelector('#qink');
   for(const fy of [.5,.3,.7])for(const fx of [.2,.35,.5]){const x=Math.round(r.left+r.width*fx),y=Math.round(r.top+r.height*fy);
     if(y<=0||y>=innerHeight-4)continue;const u=ink?underInk(x,y,ink,PEN_HIT):null;if(!u){const t=document.elementFromPoint(x,y);
       return {x,y,top:t?(t.id||t.tagName.toLowerCase()):null,inInk:!!(t&&t.closest&&t.closest('#qink'))}}}
   return null}
});
"""


class P2(H.P):
    """한 판 · 한 과목 · 엔진(chromium · webkit) — 820×1180(아이패드 세로) · 터치 켬"""
    def __init__(self, br, app, subj, tag, engine, vh=1180):
        self.engine = engine
        self.srv, port = H.serve(app, subj, tag)
        self.ctx = br.new_context(viewport={'width': 820, 'height': vh}, device_scale_factor=1, has_touch=True)
        OKNET = ('http://127.0.0.1', 'https://cdnjs.cloudflare.com/', 'https://cdn.jsdelivr.net/', 'https://fonts.googleapis.com/', 'https://fonts.gstatic.com/',
                 'blob:', 'data:')   # WebKit 은 blob: 그림 요청도 route 를 지난다 — 막으면 참고 그림이 안 뜬다(9/27 첫 판 「그림 못 받음」)
        self.ctx.route('**/*', lambda rt: rt.continue_() if rt.request.url.startswith(OKNET) else rt.abort())
        self.ctx.add_init_script(H.INIT.replace('__SUBJ__', subj))
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(120000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:200]))
        self.pg.goto('http://127.0.0.1:%d/app.html' % port, wait_until='load')
        self.pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=90000)
        self.pg.wait_for_timeout(2500)
        self.pg.evaluate(H.JS)
        self.pg.evaluate(JS2)
        self.cdp = self.ctx.new_cdp_session(self.pg) if engine == 'chromium' else None

    def ftap(self, x, y, r=22):
        if self.cdp:
            self._t('touchStart', [(x, y)], r); self.wait(60)
            self._t('touchEnd', [], r)
        else:
            self.pg.touchscreen.tap(x, y)
        self.wait(450)

    def pdown(self, x, y):
        self._p('mouseMoved', x, y, 'none', 0); self._p('mousePressed', x, y)

    def pup(self, x, y):
        self._p('mouseReleased', x, y, 'left', 0)


def scen(br, app, tag, subj, engine, keep):
    g = '%s %s %s' % (tag, engine, subj)
    u = H.SAMPLE[subj]
    p = P2(br, app, subj, '%s_%s_%s' % (tag, engine, subj), engine)
    cr = engine == 'chromium'

    def fresh(tool='pen', ans=False):
        p.ev("()=>__P.closeAll()"); p.ev("()=>__P.closeSheet()")
        ok = p.ev("u=>__P.open(u)", u)
        if ans:
            p.ev("()=>__P.ans()")
        p.ev("m=>__P.tool(m)", tool); p.wait(300)
        return ok

    try:
        ok = fresh('pen')
        s0 = p.ev("()=>__P.st()")
        T(g, '0 %s 문제 창 · 펜 도구(덮개가 카드를 덮는다)' % u, ok and s0['mode'] == 'pen' and (p.ev("()=>__P.ink()") or {}).get('penon'), {'mode': s0['mode'], 'ink': p.ev("()=>__P.ink()")})
        # ── 1 손가락 톡 · 선택지 — 지금 안 골라진 것(기록에 남은 고름이 있으면 ③ 대신 다른 번호 · 첫 판은 실물 기록의 ③ 이 이미 골라져 거저 PASS 였다) ──
        fresh('pen')
        s = p.ev("()=>__P.st()")
        c1 = next(c for c in (3, 2, 4, 1, 5) if c not in (s['pick'] or []))
        a = p.ev("c=>__P.at('.choices button[data-c=\"'+c+'\"]',.5,.5)", c1)
        p.ftap(a['x'], a['y']); t = p.ev("()=>__P.st()"); pk = p.ev("()=>__P.picks()")
        r1 = {'표적': c1, '위': a['top'], '밑': a['under'], 'pick': [s['pick'], t['pick']], '보임': pk, '획': t['strokes'] - s['strokes'], '창': p.ev("()=>__P.sheetsAll()")}
        keep.setdefault('1', {})[g] = r1
        T(g, '1 펜 도구 · 안 골라진 선택지(%s) 가운데 손가락 톡 → 고름 표시 보임 · 획 0 · 창 0(헛잣대: 바탕 무반응)' % c1,
          'qink' in (a['top'] or '') and t['pick'] == [c1] and any(x['c'] == c1 and x['vis'] for x in pk) and r1['획'] == 0 and r1['창'] == 0, r1)
        # ── 2 손가락 톡 · 〈보기〉 O 두 번 = 한 번 바뀌고 다시 제자리(실물 기록에 이미 O 가 켜진 줄도 있다 — 켜짐/꺼짐을 처음 상태 기준으로) ──
        fresh('pen', ans=True)
        rows = p.ev("()=>__P.oxRows()") or []
        if rows:
            k = rows[0]
            a = p.ev("s=>__P.at(s,.5,.5)", '.bogi .row[data-k="%s"] .ox button[data-v="O"]' % k)
            o0 = p.ev("k=>__P.ox(k)", k); p.ftap(a['x'], a['y']); o1 = p.ev("k=>__P.ox(k)", k)
            a2 = p.ev("s=>__P.at(s,.5,.5)", '.bogi .row[data-k="%s"] .ox button[data-v="O"]' % k)
            p.ftap(a2['x'], a2['y']); o2 = p.ev("k=>__P.ox(k)", k)
            on = lambda o: [x['v'] for x in (o or []) if x['on']]
            vis = [x['vis'] for x in ((o1 if 'O' in on(o1) else o2) or []) if x['v'] == 'O']
            r2 = {'줄': k, '위': a['top'], '밑': a['under'], 'on': [on(o0), on(o1), on(o2)], '켜진 O 보임': vis}
            T(g, '2 펼친 카드 〈보기〉 %s 줄 O 칸 손가락 톡 → 켜짐/꺼짐 바뀜 · 다시 톡 → 제자리 · 켜진 O 보임(헛잣대: 바탕 무반응)' % k,
              'qink' in (a['top'] or '') and (('O' in on(o1)) != ('O' in on(o0))) and on(o2) == on(o0) and vis == [True], r2)
        else:
            N(g, '2 〈보기〉 O/△/X 칸 없음(정오 없는 문항)', rows)
        # ── 3 「정답 · 해설」(근거 층 · 덮개 위) · 머리줄 칩(덮개 밑 · 🔖 단원 매칭) ──
        fresh('pen')
        a = p.ev("()=>__P.at('#cDetBtn',.5,.5)")
        d0 = p.ev("()=>__P.det()"); p.ftap(a['x'], a['y']); d1 = p.ev("()=>__P.det()")
        c = p.ev("()=>__P.at('#cMatch',.5,.5)")
        p.ftap(c['x'], c['y']); sh = p.ev("()=>__P.sheet()")
        r3 = {'정답·해설': [d0, d1], '정답·해설 위': a['top'], '칩 위': c['top'], '칩 밑': c['under'], '칩 창': sh}
        T(g, '3 손가락 톡 「정답·해설 ▸」 → 펼침 · 머리줄 칩(단원 매칭) 톡 → 제 창이 뜨고 남는다(헛잣대: 바탕 칩 무반응)',
          d0 is False and d1 is True and bool(sh) and sh.get('vis') and '단원 매칭' in (sh.get('h2') or ''), r3)
        keep.setdefault('3', {})[g] = r3
        p.ev("()=>__P.closeAll()")
        if cr:
            # ── 4 손가락 끌기 = 굴림(안 골라진 선택지 위에서 시작 · 40px · 천천히 700ms — 길게 누르기 시계도 안 뜬다)
            #    창 높이 700 으로 새로 연 판 — 1180 에선 지학 G48-03 카드가 문제 창(뜬창 · 860)에 다 들어가 굴릴 자리가 없고,
            #    이미 뜬 창은 뷰포트를 줄여도 안 줄어든다(둘째 판 굴릴 자리 0 → 제자리 누름 850ms = 길게 누르기 창)
            p0 = p
            p = P2(br, app, subj, '%s_%s_%s_700' % (tag, engine, subj), engine, vh=700)
            fresh('pen', ans=True)
            s = p.ev("()=>__P.st()")
            c4 = next(c for c in (3, 2, 4, 1, 5) if c not in (s['pick'] or []))
            a = p.ev("c=>__P.at('.choices button[data-c=\"'+c+'\"]',.5,.5)", c4)
            s = p.ev("()=>__P.st()")
            mx = s['sh'] - s['ch']
            dy = -40 if s['top'] + 40 <= mx else (40 if s['top'] >= 40 else 0)   # 굴릴 자리가 있는 쪽으로(위로 끌면 내용이 올라가 scrollTop 이 는다)
            p._t('touchStart', [(a['x'], a['y'])], 22)
            for i in range(1, 15):
                p._t('touchMove', [(a['x'], a['y'] + dy * i / 14)], 22); p.wait(50)
            for _ in range(5):
                p._t('touchMove', [(a['x'], a['y'] + dy)], 22); p.wait(30)
            p._t('touchEnd', [], 22); p.wait(500)
            t = p.ev("()=>__P.st()")
            r4 = {'표적': c4, '굴릴 자리': mx, '끈 쪽': dy, '굴림': [s['top'], t['top']], 'pick': [s['pick'], t['pick']], '창': t['sheet'], '펼침': s['det'], '위': a['top'], '밑': a['under']}
            T(g, '4 안 골라진 선택지(%s) 위에서 시작한 손가락 40px 끌기(700ms) → 카드 굴림 ≥ 25 · 그 선택지 안 골라짐 · 글자 고치기 창 안 뜸(무변 잣대 — 바탕도 굴림)' % c4,
              dy != 0 and abs(t['top'] - s['top']) >= 25 and t['pick'] == s['pick'] and not t['sheet'], r4)
            p.ev("()=>__P.closeSheet()")
            p.close(); p = p0
            # ── 5 손바닥 — 펜 닿는 중 톡 · 펜 뗀 뒤 palmMs 안 톡 → 안 골라짐 · 그 뒤 톡 → 골라짐 ──
            fresh('pen')
            s = p.ev("()=>__P.st()")
            c5 = next(c for c in (3, 2, 4, 1, 5) if c not in (s['pick'] or []))
            a = p.ev("c=>__P.at('.choices button[data-c=\"'+c+'\"]',.5,.5)", c5)
            sp = p.ev("s=>__P.penSpot(s)", '.q')
            r5 = {'표적': c5, '처음': s['pick'], '펜 자리': sp}
            if sp:
                # 펜은 긋는 채로(20px) — 글자 위에 가만히 대면 펜 길게 누르기(550ms)가 「글자 고치기」 창을 띄운다(첫 판이 그랬다 · 앱 탓 아님)
                p.pdown(sp['x'], sp['y'])
                for i in range(1, 6):
                    p._p('mouseMoved', sp['x'] + 4 * i, sp['y']); p.wait(16)
                p.ftap(a['x'], a['y']); r5['펜 닿는 중'] = p.ev("()=>__P.st()")['pick']
                r5['창'] = p.ev("()=>__P.st()")['sheet']
                p.pup(sp['x'] + 20, sp['y']); p.wait(300)
                p.ftap(a['x'], a['y']); r5['뗀 뒤 0.7초 안'] = p.ev("()=>__P.st()")['pick']
                p.wait(1400)
                p.ftap(a['x'], a['y']); r5['1.6초 뒤'] = p.ev("()=>__P.st()")['pick']
            T(g, '5 손바닥 — 펜 닿는 중 선택지(%s) 톡 → 안 골라짐 · 펜 뗀 뒤 palmMs(1.2초) 안 톡 → 안 골라짐 · 그 뒤 톡 → 골라짐(헛잣대: 바탕은 끝까지 안 골라짐)' % c5,
              bool(sp) and not r5.get('창') and c5 not in (r5.get('펜 닿는 중') or []) and c5 not in (r5.get('뗀 뒤 0.7초 안') or []) and r5.get('1.6초 뒤') == [c5], r5)
            # ── 6 길게 누르기 무변 — 문제 글 손가락 600ms → 글자 고치기 한 번 · 뗀 뒤에도 남음 ──
            r6 = {}
            for tool in ('pen', 'view'):
                fresh(tool)
                a = p.ev("()=>__P.at('.q',.3,.5)")
                p._t('touchStart', [(a['x'], a['y'])], 22); p.wait(600)
                n_in = p.ev("()=>document.querySelectorAll('#tfxSheet').length")
                p._t('touchEnd', [], 22); p.wait(500)
                r6[tool] = {'누른 채': n_in, '뗀 뒤': p.ev("()=>document.querySelectorAll('#tfxSheet').length"), 'sheet': p.ev("()=>__P.st()")['sheet'], '위': a['top']}
                p.ev("()=>__P.closeSheet()")
            T(g, '6 문제 글 손가락 600ms → 「✎ 글자 고치기 — 문제」 한 번(두 번 안 열림) · 뗀 뒤에도 남음 — 펜·보기 도구(무변 잣대)',
              all(v['누른 채'] == 1 and v['뗀 뒤'] == 1 and v['sheet'] == '✎ 글자 고치기 — 문제' for v in r6.values()), r6)
            # ── 7 펼친 뒤 펜 — 새 카드 → 「정답·해설 ▸」 손가락 톡으로 펼침 → 곧바로 해설 글·참고 칸 위 펜 획 ──
            fresh('pen')
            a = p.ev("()=>__P.at('#cDetBtn',.5,.5)")
            i0 = p.ev("()=>__P.ink()")
            p.ftap(a['x'], a['y'])
            i1 = p.ev("()=>__P.ink()")
            r7 = {'덮개 높이': [i0 and i0['h'], i1 and i1['h']], '카드 높이': [i0 and i0['cardH'], i1 and i1['cardH']]}
            tg = [('해설 글', '.sol .soltx')] + ([('참고 칸', '.ocrref .rft')] if subj == 'bio' else [])
            okk = True
            for nm, sel in tg:
                sp = p.ev("s=>__P.penSpot(s)", sel)
                if not sp:
                    r7[nm] = '자리 없음'; okk = False; continue
                s = p.ev("()=>__P.st()")
                p.pdrag(sp['x'], sp['y'], sp['x'] + 70, sp['y'] + 2)
                t = p.ev("()=>__P.st()"); ls = p.ev("()=>__P.lastStroke()")
                r7[nm] = {'획': [s['strokes'], t['strokes']], '덮개 위': sp['inInk'], '획 상자': ls}
                okk = okk and t['strokes'] == s['strokes'] + 1 and bool(ls) and ls['w'] >= 50 and ls['on']
            T(g, '7 새 카드 → 「정답·해설」 펼침 → 곧바로 %s 위 펜 60~70px → 획 +1 · 보임(헛잣대: 바탕 0 — 덮개가 펼치기 전 높이)' % ' · '.join(n for n, _ in tg), okk, r7)
        # ── 8 참고 그림(생물) — 펜 도구 손가락 톡 → 크게 보임 · 화면에 맞게 · 바깥 톡 → 닫힘 / 보기 도구도 크기 ──
        if subj == 'bio':
            r8 = {}
            for tool in ('pen', 'view'):
                fresh(tool, ans=True)
                im = p.ev("()=>__P.refImg()")
                if not im:
                    r8[tool] = '그림 못 받음'; continue
                p.ftap(im['x'], im['y']); z = p.ev("()=>__P.zoom()")
                p.ftap(8, 8); z2 = p.ev("()=>__P.zoom()")
                r8[tool] = {'그림 위': im['top'], '원본': [im['nw'], im['nh']], '크게': z, '바깥 톡 뒤': z2}
                p.ev("()=>__P.closeAll()")
            fit = lambda v: isinstance(v, dict) and bool(v.get('크게')) and v['크게']['vis'] and v['크게']['w'] >= v['크게']['want'] - 2 and v.get('바깥 톡 뒤') is None
            T(g, '8 참고 그림 손가락 톡(펜 도구) → #ocrrfz 보임 · 그림 폭 ≥ min(96vw, 92vh×비율) − 2px · 바깥 톡 → 닫힘 · 보기 도구도 같은 크기(헛잣대: 바탕 = 펜 도구 안 열림 · 353px)',
              fit(r8.get('pen')) and fit(r8.get('view')), r8)
            keep.setdefault('8', {})[g] = r8
        er = p.errs + (p.ev("()=>__P.errs()") or [])
        T(g, 'Z 페이지 오류 0', not er, er[:5])
    except Exception as ex:
        T(g, '묶음 예외', False, repr(ex)[:400])
    finally:
        p.close()


def report(t0, newmd5, bmd5, engines):
    lines = ['', '# ─── add1(9/27 · _task_jagwa_penfinger_add1) — %s ───' % time.strftime('%Y-%m-%d %H:%M'),
             'NEW = %s (md5(LF) %s) · BASE2 = genie %s (md5(LF) %s) · 엔진 %s · 820×1180 · 표본 생물 G57-05 · 지학 G48-03'
             % (NEWF, newmd5, BASE2_REV, bmd5, '+'.join(engines)),
             '입력 = Chromium CDP 터치(반지름 22)·CDP 펜 · WebKit touchscreen.tap(톡만 — 끌기·길게·펜은 Chromium) — 합성 이벤트·el.click 없음', '']
    for grp, name, ok, d in RES:
        dd = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)
        lines.append('%s | %s · %s | %s' % ('NOTE' if ok is None else 'PASS' if ok else 'FAIL', grp, name, dd[:700]))
    new = [x for x in RES if x[2] is not None and not x[0].startswith('BASE2')]
    base = [x for x in RES if x[2] is not None and x[0].startswith('BASE2')]
    np_, nf = sum(1 for x in new if x[2]), sum(1 for x in new if not x[2])
    bp, bf = sum(1 for x in base if x[2]), sum(1 for x in base if not x[2])
    lines += ['', 'add1 헛잣대(BASE2) — PASS %d · FAIL %d (고친 칸은 FAIL 이어야 · 4·6 무변 잣대와 0·Z 는 PASS)' % (bp, bf),
              'add1 합계(NEW)  PASS %d · FAIL %d  (%.0f초)' % (np_, nf, time.time() - t0)]
    txt = '\n'.join(lines) + '\n'
    if ARG('--out'):
        old = ''
    else:
        old = io.open(OUTF, encoding='utf-8').read() if os.path.exists(OUTF) else ''
    out = old.rstrip('\n') + '\n' + txt if old else txt.lstrip('\n')
    for _ in range(3):
        io.open(OUTF, 'w', encoding='utf-8', newline='\n').write(out); time.sleep(0.5)
        if io.open(OUTF, encoding='utf-8').read() == out:
            break
    print('\n'.join(lines[-3:]))
    return nf


def main():
    t0 = time.time()
    new = io.open(NEWF, encoding='utf-8', newline='').read()
    newmd5 = hashlib.md5(new.replace('\r\n', '\n').encode('utf-8')).hexdigest()
    base = subprocess.run(['git', '-C', H.GENIE, 'show', BASE2_REV + ':jagwa/index.html'], capture_output=True).stdout.decode('utf-8')
    bmd5 = hashlib.md5(base.replace('\r\n', '\n').encode('utf-8')).hexdigest()
    T('땅값', 'BASE2 = 본판 인도판(f497f05 · 0c1f47dd)', bmd5 == BASE2_MD5, bmd5)
    engines = [e for e in ('chromium', 'webkit') if not ONLY or e in ONLY]
    keep = {}
    with sync_playwright() as pw:
        for eng in engines:
            br = getattr(pw, eng).launch()
            for subj in ('bio', 'earth'):
                scen(br, base, 'BASE2', subj, eng, keep)
                scen(br, new, 'NEW', subj, eng, keep)
            br.close()
    return report(t0, newmd5, bmd5, engines)


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
