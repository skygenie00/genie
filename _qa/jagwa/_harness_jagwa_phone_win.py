# -*- coding: utf-8 -*-
r"""_task_jagwa_phone_win §B 관문 — 자과 서재: 폰 창 크기 · 머리 · OMR 비례 · 떠 있는 창 틀 · 곁창 아래 단추 · [공식]·[개념] · 다 팝업 · 그림

  python _harness_jagwa_phone_win.py [--new <앱>] [--img <그림 폴더>] [--eng chromium,webkit] [--only 1,2,...,RF] [--res <결과>] [--vendor <cdnjs 사본 폴더>]

  묶음 RF = _task_jagwa_revfix0928(9/28 검수 고침 여섯 · 칸마다 NEW 열 + 「-헛」 열 = 바탕(HEAD)이 옛 결함을 보이는지 · 헛 칸 PASS = 잣대가 산다)
    RF1 폰 OMR ≡ 손가락 · RF2 PC 목록 창 크기 · RF3 📋·🃏 창 쌓임 · RF4 [공식] 0편 이름 · RF5 물리 누르면 앞 · RF6 폰 ▾ 가림
  --vendor = cdnjs 사본(경로 꼴 /ajax/libs/ 뒤 그대로 · 클라우드처럼 cdnjs 가 막힌 곳만 · 안 주면 종전 그대로 진짜 cdnjs)

  NEW  = --new(없으면 genie 작업트리 jagwa/index.html) · BASE = genie HEAD jagwa/index.html(바로 앞 인도판 = penfinger_add2 fd911d5) — 칸마다 헛잣대(바탕에서 FAIL)
  화면 = 폰 390×844(hasTouch · 손가락 = Chromium CDP 터치 r22 · WebKit touchscreen.tap) · PC 1553×900(마우스)
  데이터 = studyplandata(phys · bio · earth) 로컬 사본을 같은 출처로(penfinger 하네스 INIT 그대로 · 기록 PUT 은 가로채 안 나감) · /img/ = --img 폴더
  ⚠ 자과앱 픽셀 게이트 없음(CLAUDE.md) — 자리 = getBoundingClientRect · 가림 = elementFromPoint · 그려졌는가 = DOM
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import io, json, os, re, sys, time, hashlib, subprocess, http.server, socketserver, threading, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'gigu'))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = _roots.genie()
NEWF = ARG('--new', os.path.join(GENIE, 'jagwa', 'index.html'))
IMG = ARG('--img', os.path.join(GENIE, 'jagwa', 'img'))
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_phone_win_result.txt'))
VENDOR = ARG('--vendor')   # revfix0928 — cdnjs 사본(클라우드) · 없으면 종전 길
_argv = sys.argv; sys.argv = [sys.argv[0]]
import _harness_jagwa_penfinger as H   # noqa: E402  (INIT · SPDROOT)
sys.argv = _argv
from playwright.sync_api import sync_playwright   # noqa: E402
RES = []
NEW14 = ['20250730190042', '20250809215555', '20250820075555', '20250821095424', '20250821141810', '20250821141858', '20250822112559',
         '20250822130514', '20250822130904', '20250822161451', '20250822162425', '20250822162525', '20250822173504', '20250901162019']


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def git(*a):
    return subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


JS = r"""
window.__W={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 R(e){if(!e)return null;const r=e.getBoundingClientRect();return {x:Math.round(r.left*10)/10,y:Math.round(r.top*10)/10,w:Math.round(r.width*10)/10,h:Math.round(r.height*10)/10}},
 vis(e){return !!e&&e.isConnected&&getComputedStyle(e).display!=='none'&&getComputedStyle(e).visibility!=='hidden'&&e.getBoundingClientRect().height>0},
 hit(e){if(!e)return null;try{e.scrollIntoView({block:'center',inline:'nearest'})}catch(_){}const r=e.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2,at=document.elementFromPoint(cx,cy);
   return {cx:Math.round(cx),cy:Math.round(cy),on:!!at&&(at===e||e.contains(at))&&cx>0&&cy>0&&cx<innerWidth&&cy<innerHeight,at:at?(at.id||at.tagName+'.'+at.className):null}},
 has(n){try{return typeof eval(n)!=='undefined'}catch(e){return false}},
 async openNo(no){try{closeView()}catch(e){}await new Promise(r=>setTimeout(r,200));await openView(no);await new Promise(r=>setTimeout(r,1800));return !document.getElementById('view').classList.contains('hide')},
 noOf(code){const r=DATA.find(x=>x[F.CODE]===code);return r?r[F.NO]:null},
 view(){const v=document.getElementById('view');return {rect:__W.R(v),win:v.classList.contains('win'),z:+v.style.zIndex||0,hide:v.classList.contains('hide'),docw:document.documentElement.scrollWidth,vw:innerWidth}},
 omr(){const o=document.getElementById('omrPad'),w=document.getElementById('wrap');return o?{rect:__W.R(o),ow:o.offsetWidth,tf:o.style.transform,wrap:w?w.clientWidth:null,show:o.classList.contains('show')}:null},
 head(){const fb=document.getElementById('fFoldBtn'),fs=document.getElementById('fSum'),sr=document.querySelector('#esh .erow.esearch'),m=sr&&sr.querySelector(':scope>span.mut'),q=document.getElementById('q');
   const chips=[...document.querySelectorAll('.pwchip')].filter(__W.vis).map(b=>({t:__W.tx(b),r:__W.R(b)}));
   const kids=sr?[...sr.children].filter(__W.vis):[];const top=kids.length?Math.min(...kids.map(k=>k.getBoundingClientRect().top)):null;
   const qFirst=!!(q&&__W.vis(q)&&top!=null&&q.getBoundingClientRect().top<=top+2&&kids[0]===q);
   return {fold:fb?__W.tx(fb):null,foldR:__W.R(fb),fsum:__W.vis(fs),mag:__W.vis(m),q:__W.R(q),sr:__W.R(sr),qFirst,chips,bodyfold:document.body.classList.contains('fold'),
     rows:[...document.querySelectorAll('#esh > *')].filter(__W.vis).map(e=>(e.id||e.className).slice(0,30))}},
 pcHead(){const e=document.getElementById('esh');if(!e)return null;const c=e.cloneNode(true);c.querySelectorAll('.pwchip').forEach(x=>x.remove());
   c.querySelectorAll('#fFold').forEach(x=>x.remove());   /* 폰 전용 접기 줄(PC display:none) — 그 안 글자는 PC 화면에 없다 */return __W.tx(c).replace(/\d+/g,'#').slice(0,1200)},
 side(id){const b=document.getElementById(id)||document.querySelector('[data-shkey="'+id+'"]');const p=b&&b.querySelector(':scope>.panel');
   return b?{float:!!p&&p.classList.contains('float'),x:!!p&&!!p.querySelector('.shx'),rect:__W.R(p),z:+b.style.zIndex||0,
     btn:p?[...p.querySelectorAll('button.btn')].map(x=>({t:__W.tx(x),fs:getComputedStyle(x).fontSize,shlink:x.classList.contains('shlink'),bw:getComputedStyle(x).borderTopWidth,deco:getComputedStyle(x).textDecorationLine})):[],
     close:p?[...p.querySelectorAll('button')].filter(x=>__W.tx(x)==='닫기').length:0}:null},
 list(){const b=document.getElementById('pwl');if(!b)return null;const p=b.querySelector('.panel');
   return {kind:b.dataset.kind,title:__W.tx(b.querySelector('.bplh span')),rect:__W.R(p),rows:[...b.querySelectorAll('.pwr')].map(r=>({id:r.dataset.id,tri:__W.tx(r.querySelector('.tri')),none:r.classList.contains('none')})),
     heads:[...b.querySelectorAll('.pwh')].map(__W.tx),float:!!p&&p.classList.contains('float'),z:+b.style.zIndex||0}},
 rowAt(id){const r=document.querySelector('#pwl .pwr[data-id="'+id+'"]');return r?__W.hit(r):null},
 rowBody(id){const r=document.querySelector('#pwl .pwr[data-id="'+id+'"]');const b=r&&r.nextElementSibling;
   return b?{open:!b.classList.contains('hide'),tri:__W.tx(r.querySelector('.tri')),lines:b.querySelectorAll('.thl').length,imgs:[...b.querySelectorAll('img')].map(i=>({src:i.getAttribute('src'),ok:i.complete&&i.naturalWidth>0})),
     cnt:[...b.querySelectorAll('.pwc')].map(__W.tx),katex:b.querySelectorAll('.katex').length,indent:Math.round(parseFloat(getComputedStyle(b).paddingLeft))}:null},
 async imgOk(){const im=[...document.querySelectorAll('#pwl img')];const r=await Promise.all(im.map(i=>new Promise(res=>{const x=new Image();x.onload=()=>res([i.getAttribute('src'),x.naturalWidth>0]);x.onerror=()=>res([i.getAttribute('src'),false]);x.src=i.src})));return r},
 cntAt(i){const c=document.querySelectorAll('#pwl .pwc')[i||0];return c?__W.hit(c):null},
 sheets(){return [...document.querySelectorAll('.sheet')].filter(__W.vis).map(x=>({id:x.id||x.dataset.shkey||x.className.slice(0,20),z:+x.style.zIndex||0}))},
 cqiAt(no){const b=[...document.querySelectorAll('.sheet .cqi')].find(x=>__W.tx(x.querySelector('b'))===String(no));return b?__W.hit(b):null},
 chip(t){const b=[...document.querySelectorAll('.pwchip')].filter(__W.vis).find(x=>__W.tx(x)===t);return b?__W.hit(b):null},
 at(sel){const e=document.querySelector(sel);return e?__W.hit(e):null},
 errs(){return (window.__err||[]).slice(0,10)}
};
"""


def serve(app_text, subj, tag):
    out = os.path.join(H.WORK, 'pw_' + tag); os.makedirs(out, exist_ok=True)
    io.open(os.path.join(out, 'app.html'), 'w', encoding='utf-8', newline='').write(app_text)
    spd = os.path.join(H.SPDROOT, subj)

    class Hh(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=out, **k)

        def log_message(self, *a, **k):
            pass

        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            f = None
            if p.startswith('/img/'):
                f = os.path.join(IMG, p[5:].replace('/', os.sep)); ct = 'image/jpeg'
            elif p.startswith('/data/'):
                rel = p[6:]
                if rel.startswith(subj + '/'):
                    f = os.path.join(spd, rel[len(subj) + 1:].replace('/', os.sep))
                ct = 'application/octet-stream'
            else:
                return super().do_GET()
            if not f or not os.path.isfile(f):
                self.send_response(404); self.end_headers(); return
            b = open(f, 'rb').read()
            self.send_response(200); self.send_header('Content-Type', ct); self.send_header('Content-Length', str(len(b)))
            self.send_header('X-Sha', hashlib.sha1(b).hexdigest()); self.end_headers(); self.wfile.write(b)
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), Hh); srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


class Pg:
    def __init__(self, br, eng, app, subj, tag, phone, vp=None):
        """vp(fix1 RF2) = 창 크기를 따로(PC 1440 · iPad 820) — 안 주면 종전(폰 390 · PC 1553) · touch = 폭 1100 이하면 손가락"""
        self.eng, self.phone = eng, phone
        self.touch = phone if vp is None else vp['width'] <= 1100
        self.srv, port = serve(app, subj, tag + '_' + eng + (('_%d' % vp['width']) if vp else ('_ph' if phone else '_pc')))
        vp = vp or ({'width': 390, 'height': 844} if phone else {'width': 1553, 'height': 900})
        self.vpw = vp
        self.ctx = br.new_context(viewport=vp, device_scale_factor=1, has_touch=True, is_mobile=bool(self.touch and eng == 'chromium'))
        OKNET = ('http://127.0.0.1', 'https://cdnjs.cloudflare.com/', 'https://cdn.jsdelivr.net/', 'https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')

        def _rt(rt):
            u = rt.request.url
            m = re.match(r'https://cdnjs\.cloudflare\.com/ajax/libs/(.+)$', u.split('?')[0]) if VENDOR else None
            if m:   # cdnjs 사본(줄 때만)
                f = os.path.join(VENDOR, *m.group(1).split('/'))
                if os.path.isfile(f):
                    return rt.fulfill(path=f, content_type='text/css' if f.endswith('.css') else ('font/woff2' if f.endswith('.woff2') else 'application/javascript'))
                return rt.abort()
            return rt.continue_() if u.startswith(OKNET) else rt.abort()
        self.ctx.route('**/*', _rt)
        self.ctx.add_init_script(H.INIT.replace('__SUBJ__', subj))
        self.pg = self.ctx.new_page(); self.pg.set_default_timeout(120000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:200]))
        self.pg.goto('http://127.0.0.1:%d/app.html' % port, wait_until='load')
        self.pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=90000)
        self.pg.wait_for_timeout(2500)
        self.pg.evaluate(JS)
        self.cdp = self.ctx.new_cdp_session(self.pg) if eng == 'chromium' else None

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def wait(self, ms):
        self.pg.wait_for_timeout(ms)

    def press(self, at, wait=600):
        """폰 = 손가락(Chromium CDP r22 · WebKit touchscreen.tap) · PC = 마우스"""
        if not at or not at.get('on'):
            return False
        x, y = at['cx'], at['cy']
        if not self.touch:
            self.pg.mouse.click(x, y)
        elif self.cdp:
            pt = {'x': x, 'y': y, 'radiusX': 22, 'radiusY': 22, 'force': 1, 'id': 1}
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [pt]}); self.wait(60)
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        else:
            self.pg.touchscreen.tap(x, y)
        self.wait(wait)
        return True

    def pinch(self, cx, cy, d0, d1, n=10):
        """두 손가락 벌리기(Chromium CDP 만)"""
        if not self.cdp:
            return False
        def pts(d):
            return [{'x': cx - d / 2, 'y': cy, 'radiusX': 22, 'radiusY': 22, 'id': 1}, {'x': cx + d / 2, 'y': cy, 'radiusX': 22, 'radiusY': 22, 'id': 2}]
        self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': pts(d0)})
        for i in range(1, n + 1):
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': pts(d0 + (d1 - d0) * i / n)}); self.wait(20)
        self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); self.wait(800)
        return True

    def drag(self, x0, y0, x1, y1, n=12):
        """≡ 끌기 — 폰 Chromium = CDP 터치 · 그 밖 = 마우스"""
        if self.cdp and self.touch:
            def t(ty, x, y):
                self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': ([] if ty == 'touchEnd' else [{'x': x, 'y': y, 'radiusX': 22, 'radiusY': 22, 'id': 1}])})
            t('touchStart', x0, y0)
            for i in range(1, n + 1):
                t('touchMove', x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.wait(16)
            for _ in range(3):
                t('touchMove', x1, y1); self.wait(30)
            t('touchEnd', x1, y1); self.wait(500)
            return 'cdp-touch'
        m = self.pg.mouse; m.move(x0, y0); m.down()
        for i in range(1, n + 1):
            m.move(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.wait(16)
        m.up(); self.wait(500)
        return 'mouse'

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass
        try:
            self.srv.shutdown()
        except Exception:
            pass


def both(br, eng, subj, phone, fn, vp=None, whos=('NEW', 'BASE')):
    """NEW · BASE 한 벌씩(vp · whos = fix1 RF2 — 창 크기 · 앱 고르기)"""
    out = {}
    for who in whos:
        app = APPS[who]
        q = Pg(br, eng, app, subj, who, phone, vp)
        try:
            out[who] = fn(q)
            out[who + '_err'] = q.errs + (q.ev("()=>__W.errs()") or [])
        finally:
            q.close()
    return out


# ── 1 폰 문제 창 · PC 문제 창 ──
def g1(br, eng):
    def f(q):
        no = q.ev("()=>__W.noOf('PA0702')")
        q.ev("n=>__W.openNo(n)", no)
        v0 = q.ev("()=>__W.view()")
        tg = q.ev("()=>__W.at('#vWinTg')")
        q.press(tg, 900); v1 = q.ev("()=>__W.view()")
        tg2 = q.ev("()=>__W.at('#vWinTg')")
        q.press(tg2, 900); v2 = q.ev("()=>__W.view()")
        return {'v0': v0, 'full': v1, 'back': v2}
    r = both(br, eng, 'phys', True, f)
    n, b = r['NEW'], r['BASE']
    ok = n['v0']['win'] and n['v0']['rect'] and abs(n['v0']['rect']['w'] - 374) <= 1 and abs(n['v0']['rect']['h'] - 726) <= 1 and abs(n['v0']['rect']['x'] - 8) <= 1 and n['v0']['docw'] <= n['v0']['vw']
    T('1', '%s 폰 390×844 PA0702 문제 창 = 떠 있는 창 폭 374 · 높이 726 · 좌 8 · 가로 넘침 0' % eng, ok, n['v0'])
    T('1', '%s 폰 ⤢ 누름(손가락) → 전체(390×844) → 다시 → 창(374×726)' % eng,
      not n['full']['win'] and abs((n['full']['rect'] or {}).get('w', 0) - 390) <= 1 and n['back']['win'] and abs((n['back']['rect'] or {}).get('w', 0) - 374) <= 1, {'전체': n['full'], '창': n['back']})
    T('1-헛', '%s 헛잣대 바탕 — 폰 문제 창 = 전체 390×844' % eng, abs((b['v0']['rect'] or {}).get('w', 0) - 390) <= 1 and abs((b['v0']['rect'] or {}).get('h', 0) - 844) <= 1, b['v0'])

    def fpc(q):
        no = q.ev("()=>__W.noOf('PA0702')")
        q.ev("n=>__W.openNo(n)", no)
        return q.ev("()=>__W.view()")
    r2 = both(br, eng, 'phys', False, fpc)
    T('1', '%s PC 1553×900 문제 창 1000×774 무변(= 바탕)' % eng, r2['NEW']['rect'] == r2['BASE']['rect'] and abs(r2['NEW']['rect']['w'] - 1000) <= 1 and abs(r2['NEW']['rect']['h'] - 774) <= 1, [r2['NEW'], r2['BASE']])
    for who in ('NEW',):
        T('Z', '%s 오류 0(1 묶음 NEW)' % eng, not r[who + '_err'] and not r2[who + '_err'], (r[who + '_err'] + r2[who + '_err'])[:4])


# ── 2 머리 ──
def g2(br, eng):
    def f(q):
        h0 = q.ev("()=>__W.head()")
        fb = q.ev("()=>__W.at('#fFoldBtn')")
        q.press(fb, 700)
        h1 = q.ev("()=>__W.head()")
        return {'접힘': h0, '펼침': h1}
    r = both(br, eng, 'phys', True, f)
    n, b = r['NEW'], r['BASE']
    h1 = n['펼침']
    ok = n['접힘']['fold'] == '▾' and h1['fold'] == '▴' and not n['접힘']['fsum'] and not h1['fsum'] and not h1['mag'] and h1['qFirst']
    T('2', '%s 폰 머리 — #fFoldBtn 「▾」(접힘) → 누름 → 「▴」 · #fSum 안 보임 · 🔍 안 보임 · 검색 칸이 검색 줄 첫 줄(보이는 첫 자식 · 맨 윗줄)' % eng, ok, {'접힘': n['접힘'], '펼침': h1})
    T('2-헛', '%s 헛잣대 바탕 — 「필터 ▾」 · #fSum 보임 · 🔍 보임' % eng, b['접힘']['fold'] == '필터 ▾' and b['접힘']['fsum'] and b['펼침']['mag'], b)

    def fpc(q):
        return q.ev("()=>__W.pcHead()")
    r2 = both(br, eng, 'phys', False, fpc)
    T('2', '%s PC 머리 글 = 바탕(새 칩 [공식]·[개념] 빼고 · 수는 # 로)' % eng, r2['NEW'] == r2['BASE'], [r2['NEW'][:200], r2['BASE'][:200]])


# ── 3 OMR ──
def g3(br, eng):
    def f(q):
        no = q.ev("()=>__W.noOf('PA0702')")
        q.ev("n=>__W.openNo(n)", no)
        q.wait(800)
        o0 = q.ev("()=>__W.omr()")
        o1 = None
        if q.cdp:
            st = q.ev("()=>{const s=document.getElementById('stage');const r=s.getBoundingClientRect();return {x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height*.5)}}")
            q.pinch(st['x'], st['y'], 80, 240)
            q.ev("()=>{try{layoutOmr()}catch(e){}}")
            o1 = q.ev("()=>__W.omr()")
        g = q.ev("()=>__W.at('#omrPad .ogrip')")
        dk = q.drag(g['cx'], g['cy'], g['cx'] + 30, g['cy'] + 40) if g else None
        pos = q.ev("()=>{try{return {own:OPOS[VNO]||null,def:OPOS.def||null}}catch(e){return null}}")
        return {'o0': o0, 'o1': o1, '끌기': dk, 'pos': pos}
    r = both(br, eng, 'phys', True, f)
    n, b = r['NEW'], r['BASE']
    o0 = n['o0'] or {}
    want = 286 * (o0.get('wrap') or 0) / 976.0
    ok = o0.get('rect') and abs(o0['rect']['w'] - want) <= 2
    T('3', '%s 폰 PA0702 #omrPad 폭 = 286 × (쪽 폭 %s ÷ 976) = %.1f ± 2' % (eng, o0.get('wrap'), want), ok, o0)
    if n['o1']:
        o1 = n['o1']; w1 = 286 * (o1.get('wrap') or 0) / 976.0
        T('3', '%s 두 손가락 벌림 뒤 — 쪽 폭 %s → %s · #omrPad 폭 = 같은 비율(± 2)' % (eng, o0.get('wrap'), o1.get('wrap')), o1.get('rect') and abs(o1['rect']['w'] - w1) <= 2 and o1.get('wrap') != o0.get('wrap'), o1)
    T('3', '%s ≡ 끌기(%s) → 자리 저장(OPOS 문항·def)' % (eng, n['끌기']), bool(n['pos'] and n['pos'].get('own') and n['pos'].get('def')), n['pos'])
    T('3-헛', '%s 헛잣대 바탕 — 폰 #omrPad 폭 286(배율 없음)' % eng, (b['o0'] or {}).get('rect') and abs(b['o0']['rect']['w'] - 286) <= 2, b['o0'])


# ── 4 · 5 · 6 떠 있는 창 틀 · conceptStat · 아래 단추 ──
def g4(br, eng):
    def f(q):
        out = {}
        no = q.ev("()=>__W.noOf('PA0702')")
        q.ev("n=>__W.openNo(n)", no)
        # 공식 창 소단원 칩
        q.ev("()=>{const r=rec(VNO);const s=secsFor(r);theorySheet(s.length>1?s:THEORY.sec.slice(0,3),'관문','')}"); q.wait(700)
        a = q.ev("()=>__W.side('sh-theory')")
        q.press(q.ev("()=>{const t=document.querySelectorAll('#sh-theory .thtabs button')[1];return t?__W.hit(t):null}"), 700)
        out['공식 칩'] = [a, q.ev("()=>__W.side('sh-theory')")]
        # 개념 창(conceptSheet) 위 칩
        q.ev("()=>{const r=rec(VNO);conceptSheet(null,r)}"); q.wait(700)
        a = q.ev("()=>__W.side('sh-concept')")
        q.press(q.ev("()=>{const t=document.querySelectorAll('#sh-concept .thtabs button')[1]||document.querySelectorAll('#sh-concept .thtabs button')[0];return t?__W.hit(t):null}"), 700)
        out['개념 창 칩'] = [a, q.ev("()=>__W.side('sh-concept')")]
        # 개념 잇기 개념 누름
        q.ev("()=>{conceptPick(rec(VNO))}"); q.wait(700)
        a = q.ev("()=>__W.side('sh-conceptPick')")
        q.press(q.ev("()=>{const t=[...document.querySelectorAll('#sh-conceptPick .cxi')].find(x=>!x.querySelector('.tag'));return t?__W.hit(t):null}"), 700)
        out['개념 잇기'] = [a, q.ev("()=>__W.side('sh-conceptPick')")]
        # 개념으로 훑기 칩(길게 누르기 대신 오른쪽 누름 = pick → build)
        q.ev("()=>{document.getElementById('btnConcept').onclick()}"); q.wait(900)
        shk = q.ev("()=>{const b=[...document.querySelectorAll('.sheet.shfloat')].pop();return b?(b.id||''):null}")
        a = q.ev("k=>__W.side(k)", shk or 'x')
        q.ev("()=>{const b=[...document.querySelectorAll('.sheet.shfloat')].pop();const t=b&&b.querySelector('#cxClear');t&&t.click()}"); q.wait(700)
        out['개념으로 훑기'] = [a, q.ev("k=>__W.side(k)", shk or 'x')]
        # conceptStat 뒤 📋 창
        q.ev("()=>{document.querySelectorAll('.sheet.shfloat').forEach(x=>x.remove());try{jnOpen(Object.keys(TOC.sec)[0])}catch(e){}}"); q.wait(600)
        q.ev("()=>{try{conceptStat(Object.keys(CB)[0])}catch(e){}}"); q.wait(700)
        out['conceptStat'] = q.ev("()=>({jnw:!!document.getElementById('jnw'),sh:!!document.getElementById('sh-conceptStat')})")
        # 아래 단추 — 풀이 · 공식 · 개념 창
        btn = {}
        for key, ex in (('sol', "()=>{const r=DATA.find(x=>SOL[x[F.VLT]]);if(r)solSheet(r)}"), ('theory', "()=>{const r=rec(VNO);theorySheet(secsFor(r).length?secsFor(r):THEORY.sec.slice(0,1),'관문','')}"),
                        ('concept', "()=>{conceptSheet(null,rec(VNO))}"), ('conceptView', "()=>conceptView(Object.keys(CB).find(k=>(CQ[k]||[]).length))"), ('conceptPick', "()=>conceptPick(rec(VNO))")):
            q.ev(ex); q.wait(700)
            btn[key] = q.ev("k=>__W.side('sh-'+k)", key)
        out['단추'] = btn
        return out
    r = both(br, eng, 'phys', False, f)
    n, b = r['NEW'], r['BASE']
    for k in ('공식 칩', '개념 창 칩', '개념 잇기', '개념으로 훑기'):
        a0, a1 = n[k]
        ok = bool(a0 and a1) and a1['float'] and a1['x'] and a0['rect'] == a1['rect']
        T('4', '%s %s 누른 뒤 — .panel float · ✕ · 자리·크기 = 누르기 전' % (eng, k), ok, {'전': a0, '뒤': a1})
        b0, b1 = b[k]
        T('4-헛', '%s 헛잣대 바탕 %s — 누른 뒤 틀 깨짐(float 없음 또는 자리 (0,0))' % (eng, k), bool(b1) and (not b1['float'] or not b1['x'] or (b1['rect'] or {}).get('x', 0) <= 1), {'전': b0, '뒤': b1})
    T('5', '%s conceptStat 부른 뒤 📋 창(#jnw) 남음 · 「sh-conceptStat」 창 없음' % eng, n['conceptStat']['jnw'] and not n['conceptStat']['sh'], n['conceptStat'])
    T('5-헛', '%s 헛잣대 바탕 — 📋 창 사라짐(sh-conceptStat 로 바뀜)' % eng, not b['conceptStat']['jnw'] or b['conceptStat']['sh'], b['conceptStat'])
    tab = {k: v for k, v in n['단추'].items() if v}
    ok6 = all(v['close'] == 0 and all(x['shlink'] and x['fs'] == '12px' and x['bw'] == '0px' and 'underline' in x['deco'] for x in v['btn']) for k, v in tab.items() if k in ('sol', 'theory', 'concept')) and {'sol', 'theory', 'concept'} <= set(tab)
    T('6', '%s 곁창 아래 — 풀이·공식·개념 창 「닫기」 0 · button.btn = 12px 밑줄 글자(테 0)' % eng, ok6, tab)
    N('6', '%s 바꾼 창 표(창 · 남은 아래 단추 · 걷은 「닫기」)' % eng, {k: [x['t'] for x in v['btn']] for k, v in tab.items()})
    T('6-헛', '%s 헛잣대 바탕 — 「닫기」 있음' % eng, any((v or {}).get('close') for v in b['단추'].values()), {k: (v or {}).get('close') for k, v in b['단추'].items()})
    T('Z', '%s 오류 0(4 묶음 NEW)' % eng, not r['NEW_err'], r['NEW_err'][:4])


# ── 7 · 8 · 9 [공식]·[개념] · 다 팝업 · 그림 ──
def g7(br, eng):
    def f(q):
        out = {'head': q.ev("()=>__W.head()")}
        c = q.ev("()=>__W.chip('공식')")
        out['공식 칩'] = c
        if c:
            q.press(c, 900); out['공식'] = q.ev("()=>__W.list()")
            q.press(q.ev("()=>__W.rowAt('1.1.1')"), 1200); out['공식 1.1.1'] = q.ev("()=>__W.rowBody('1.1.1')")
        c2 = q.ev("()=>__W.chip('개념')")
        out['개념 칩'] = c2
        if c2:
            q.press(c2, 900); out['개념'] = q.ev("()=>__W.list()")
            q.press(q.ev("()=>__W.rowAt('1.1.1')"), 1500); out['개념 1.1.1'] = q.ev("()=>__W.rowBody('1.1.1')")
            # 다 펼쳐 그림 깨짐 셈(없는 14장 포함 · 그림 받기 기다림)
            q.ev("async()=>{for(const r of document.querySelectorAll('#pwl .pwr:not(.none)')){const b=r.nextElementSibling;if(b.classList.contains('hide'))r.click()}}"); q.wait(4000)
            ok_ = q.ev("async()=>await __W.imgOk()")   # 게으른 그림은 화면 밖이면 안 받는다 — 같은 src 를 직접 받아 잰다
            out['그림'] = {'n': len(ok_), 'bad': [s for s, v in ok_ if not v][:10], 'new14': sum(1 for s, v in ok_ if v and any(('p%s.jpg' % g) in s for g in NEW14))}
            q.ev("()=>{const b=document.getElementById('pwl');b.querySelectorAll('.pwb').forEach(x=>x.classList.add('hide'));b.querySelectorAll('.pwr .tri').forEach(t=>{if(t.textContent)t.textContent='▸'})}")
            q.press(q.ev("()=>__W.rowAt('1.1.1')"), 1200)
            ca = q.ev("()=>__W.cntAt(0)")
            q.press(ca, 1200)
            out['개념 창'] = q.ev("()=>__W.sheets()")
            cq = q.ev("()=>__W.cqiAt(6)")
            q.press(cq, 2500)
            out['문제 6'] = {'view': q.ev("()=>__W.view()"), 'sheets': q.ev("()=>__W.sheets()"), 'VNO': q.ev("()=>VNO")}
            q.press(q.ev("()=>__W.at('#vBack')"), 900)
            out['서재 뒤'] = {'view': q.ev("()=>__W.view()"), 'sheets': q.ev("()=>__W.sheets()")}
        return out
    r = both(br, eng, 'phys', True, f)
    n, b = r['NEW'], r['BASE']
    fr = n['head']['foldR'] or {}
    ch = n['head']['chips']
    T('7', '%s 폰 칩 둘 「공식」「개념」 — ▾ 바로 오른쪽(같은 줄 · 차례)' % eng, [c['t'] for c in ch] == ['공식', '개념'] and all(abs(c['r']['y'] - fr.get('y', -99)) <= 4 and c['r']['x'] > fr.get('x', 999) for c in ch), {'▾': fr, '칩': ch})
    T('7-헛', '%s 헛잣대 바탕 — 칩 없음' % eng, not b['head']['chips'] and not b.get('공식 칩'), b['head']['chips'])
    L = n.get('공식') or {}
    T('7', '%s [공식] 목록 창 — 머리 「📐 공식 · 전체 · 물리 목차 51단원」 · 51 줄 · 폭 374 · 높이 72%%(608) · 좌 8' % eng,
      L.get('title') == '📐 공식 · 전체 · 물리 목차 51단원' and len(L.get('rows') or []) == 51 and L.get('rect') and abs(L['rect']['w'] - 374) <= 1 and abs(L['rect']['h'] - 608) <= 1 and abs(L['rect']['x'] - 8) <= 1, L)
    fb = n.get('공식 1.1.1') or {}
    T('7', '%s [공식] 1.1.1 ▸ 손가락 → 본문 펼침 · 「▾」 · 들여 씀 16 · 수식(KaTeX)' % eng, fb.get('open') and fb.get('tri') == '▾' and fb.get('lines', 0) > 3 and abs(fb.get('indent', 0) - 16) <= 1 and fb.get('katex', 0) > 0, fb)
    C = n.get('개념') or {}
    nt = {x['id']: x for x in (C.get('rows') or [])}
    T('7', '%s [개념] 목록 창 — 「💡 개념 · 전체 · 볼트 물리 폴더 51파일」 · 51 줄 · 1.1.2·3.1.3·6.1.3 세모 없음(빈 파일)' % eng,
      C.get('title') == '💡 개념 · 전체 · 볼트 물리 폴더 51파일' and len(nt) == 51 and all(nt.get(k, {}).get('tri') == '' and nt[k]['none'] for k in ('1.1.2', '3.1.3', '6.1.3')) and nt.get('1.1.1', {}).get('tri') in ('▸', '▾'), {'머리': C.get('title'), '빈': [nt.get(k) for k in ('1.1.2', '3.1.3', '6.1.3')], '편': C.get('heads')})
    cb = n.get('개념 1.1.1') or {}
    T('7', '%s [개념] 1.1.1 펼침 — 블록 줄 오른쪽 「5 O2」「1 O1」(기록 사본 기준)' % eng, [x.replace(' ', '') for x in (cb.get('cnt') or [])] == ['5O2', '1O1'], cb)
    g = n.get('그림') or {}
    T('9', '%s [개념] 다 펼침 — 그림 %s 장 깨짐 0 · 새 14 장 보임' % (eng, g.get('n')), g.get('n', 0) >= 68 and not g.get('bad') and g.get('new14') == 14, g)
    p6 = n.get('문제 6') or {}
    sh = [x['id'] for x in (p6.get('sheets') or [])]
    vz = (p6.get('view') or {}).get('z', 0)
    T('8', '%s 다 팝업 — [개념] → 1.1.1 「5 O2」 → 개념 창 → 문제 6 누름 → 문제 창 맨 위(z %s > 곁창) · 목록 창(#pwl)·개념 창 DOM 남음' % (eng, vz),
      p6.get('VNO') == 6 and not (p6.get('view') or {}).get('hide') and 'pwl' in sh and 'sh-conceptView' in sh and all(vz > x['z'] for x in (p6.get('sheets') or [])), p6)
    sb = n.get('서재 뒤') or {}
    T('8', '%s 「서재」로 닫음 → 개념 창·목록 창 보임' % eng, (sb.get('view') or {}).get('hide') and 'sh-conceptView' in [x['id'] for x in (sb.get('sheets') or [])] and 'pwl' in [x['id'] for x in (sb.get('sheets') or [])], sb)
    T('Z', '%s 오류 0(7 묶음 NEW)' % eng, not r['NEW_err'], r['NEW_err'][:4])

    def fo(q):
        return q.ev("()=>({chips:document.querySelectorAll('.pwchip').length,pw:__W.has('pwList')})")
    for subj in ('bio', 'earth'):
        ro = both(br, eng, subj, True, fo)
        T('7', '%s %s — 칩 없음(물리만)' % (eng, subj), ro['NEW']['chips'] == 0, ro['NEW'])


def g8b(br, eng):
    """헛잣대 — 바탕 개념 창 문제 누름 = 다른 창 지움"""
    def f(q):
        q.ev("()=>conceptView(Object.keys(CB).find(k=>(CQ[k]||[]).length>=1))"); q.wait(800)
        q.ev("()=>{try{jnOpen(Object.keys(TOC.sec)[0])}catch(e){}}"); q.wait(500)
        cq = q.ev("()=>{const b=document.querySelector('.cqi');return b?__W.hit(b):null}")
        q.press(cq, 2500)
        return {'sheets': q.ev("()=>__W.sheets()"), 'view': q.ev("()=>__W.view()")}
    r = both(br, eng, 'phys', False, f)
    T('8-헛', '%s 헛잣대 바탕 — 개념 창 문제 누름 → 다른 창(개념 창·📋) 지워짐' % eng, not [x for x in r['BASE']['sheets'] if x['id'] in ('jnw',) or 'thsheet' in x['id']], r['BASE'])
    T('8', '%s 새 판 — 같은 누름 뒤 개념 창·📋 창 남음' % eng, any(x['id'] == 'jnw' for x in r['NEW']['sheets']), r['NEW'])


def d9():
    have = [g for g in NEW14 if os.path.isfile(os.path.join(IMG, 'p%s.jpg' % g))]
    T('9', 'jagwa/img 에 새 그림 14 장(p<ts>.jpg · 긴 변 1000 · JPEG) — %s' % IMG, len(have) == 14, {'있음': len(have)})
    # ★ A-6(d) 9/30 _task_qa_baseline — 헛잣대 바탕을 HEAD 가 아니라 인도 앞 판 fd911d5(penfinger_add2)로 박는다 — 인도(fb89ad2) 뒤 HEAD 에는 그 14 장이 이미 있다
    head = set(x for x in git('ls-tree', '--name-only', 'fd911d5', 'jagwa/img/').decode('utf-8').split('\n') if x)
    T('9-헛', '헛잣대 바탕(fd911d5) — 그 14 장 없음', not any(('jagwa/img/p%s.jpg' % g) in head for g in NEW14), {'fd911d5 에 있음': sum(1 for g in NEW14 if ('jagwa/img/p%s.jpg' % g) in head)})


# ── RF  _task_jagwa_revfix0928 — 9/28 검수 고침 여섯(칸마다 NEW · 「-헛」 = 바탕 HEAD 가 옛 결함을 보임) ──
PD = r"""()=>{window.__pd=[];if(!window.__pdOn){window.__pdOn=1;document.addEventListener('pointerdown',e=>{const t=e.target;(window.__pd=window.__pd||[]).push({c:String(t.className||t.tagName).slice(0,30),o:(t.dataset&&t.dataset.omr)||'',ty:e.pointerType})},true)}return true}"""
HN = "()=>{try{return hist(VNO).length}catch(e){return -1}}"
OP = "()=>{try{return {own:OPOS[VNO]||null,def:OPOS.def||null}}catch(e){return null}}"


def _reboot(q):
    q.pg.reload(wait_until='load')
    q.pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=90000)
    q.wait(2500)
    q.ev(JS)


def rf1(br, eng):
    """A-1 폰 OMR ≡ 손가락 — 누름 대상 = ≡ · 채점 0 · 60px 끌어 저장 · 새로고침 뒤 같음 · ① 톡 무변"""
    def f(q):
        no = q.ev("()=>__W.noOf('PA0702')"); q.ev("n=>__W.openNo(n)", no); q.wait(800)
        q.ev(PD)
        out = {'h0': q.ev(HN)}
        g = q.ev("()=>__W.at('#omrPad .ogrip')")
        q.press(g, 600)
        out['누름'] = q.ev("()=>window.__pd.splice(0)")[:2]
        out['h_tap'] = q.ev(HN) - out['h0']
        q.ev("()=>{document.querySelectorAll('.sheet.shfloat').forEach(x=>x.remove())}")
        g = q.ev("()=>__W.at('#omrPad .ogrip')")
        o0 = q.ev(OP)
        out['끌기'] = q.drag(g['cx'], g['cy'], g['cx'] + 60, g['cy']) if g and g.get('on') else None
        out['pos'] = q.ev(OP)
        out['o0'] = o0
        out['h_drag'] = q.ev(HN) - out['h0']
        _reboot(q)
        q.ev("n=>__W.openNo(n)", no); q.wait(800)
        out['pos2'] = q.ev(OP)
        q.ev(PD)
        h1 = q.ev(HN)
        b1 = q.ev("()=>__W.at('#omrPad button[data-omr=\"①\"]')")
        q.press(b1, 700)
        out['① 누름'] = q.ev("()=>window.__pd.splice(0)")[:1]
        out['h_one'] = q.ev(HN) - h1
        return out
    r = both(br, eng, 'phys', True, f)
    n, b = r['NEW'], r['BASE']
    tg = lambda x: (x or [{}])[0]
    ok1 = tg(n['누름']).get('c', '').startswith('ogrip') and n['h_tap'] == 0
    T('RF1', '%s 폰 PA0702 ≡ 가운데 손가락(%s) → pointerdown 대상 = ≡ · 채점 기록 0' % (eng, 'CDP r22' if eng == 'chromium' else 'tap'), ok1, {'대상': n['누름'], '채점 늘어남': n['h_tap']})
    T('RF1-헛', '%s 헛잣대 바탕 — 대상 ≡ 아님(①·창) 또는 채점 늘어남' % eng, not tg(b['누름']).get('c', '').startswith('ogrip') or b['h_tap'] > 0, {'대상': b['누름'], '채점 늘어남': b['h_tap']})
    pos, pos2 = (n['pos'] or {}), (n['pos2'] or {})
    ok2 = bool(pos.get('own')) and pos.get('own') == pos.get('def') and pos.get('own') != (n['o0'] or {}).get('own') and pos2.get('own') == pos.get('own') and n['h_drag'] == 0
    T('RF1', '%s ≡ 손가락 60px 끌어 놓기(%s) → OPOS[문항] = 새 자리(= def) · 새로고침 뒤 같음 · 채점 0' % (eng, n['끌기']), ok2, {'전': n['o0'], '뒤': pos, '새로고침 뒤': pos2, '채점': n['h_drag']})
    T('RF1-헛', '%s 헛잣대 바탕 — 손가락 끌기 뒤 OPOS null(저장 안 됨)' % eng, not (b['pos'] or {}).get('own'), b['pos'])
    T('RF1', '%s ① 가운데 손가락 톡 → ① 눌림(채점 +1 · 무변)' % eng, tg(n['① 누름']).get('o') == '①' and n['h_one'] == 1, {'대상': n['① 누름'], '채점': n['h_one']})
    T('Z', '%s 오류 0(RF1 NEW)' % eng, not r['NEW_err'], r['NEW_err'][:4])


def rf2(br, eng):
    """A-2 PC [공식]·[개념] 목록 창 = 풀이 곁창 크기·자리(560 × 곁창 높이) · 폰 374×608 무변"""
    def f(q):
        no = q.ev("()=>__W.noOf('PA0702')"); q.ev("n=>__W.openNo(n)", no); q.wait(600)
        out = {}
        for k in ('f', 'c'):
            q.ev("k=>{const o=document.getElementById('pwl');if(o)o.remove();try{delete WIN['pw'+k]}catch(e){}pwList(k)}", k); q.wait(500)
            out[k] = (q.ev("()=>__W.list()") or {}).get('rect')
            q.ev("()=>{const o=document.getElementById('pwl');if(o)o.remove()}")
        q.ev("()=>{try{delete WIN.sol}catch(e){}const r=DATA.find(x=>SOL[x[F.VLT]]);if(r)solSheet(r)}"); q.wait(700)
        s = q.ev("()=>__W.side('sh-sol')")
        out['곁창'] = s and s.get('rect')
        return out
    r = both(br, eng, 'phys', False, f)
    n, b = r['NEW'], r['BASE']
    sd = n['곁창'] or {}
    ok = bool(sd) and all(n[k] and abs(n[k]['w'] - 560) <= 2 and abs(n[k]['h'] - sd['h']) <= 2 and abs(n[k]['x'] - sd['x']) <= 2 and abs(n[k]['y'] - sd['y']) <= 2 for k in ('f', 'c'))
    T('RF2', '%s PC [공식]·[개념] 목록 창 = 560 × 풀이 곁창 높이(± 2) · 자리 = 곁창 첫 자리' % eng, ok, {'공식': n['f'], '개념': n['c'], '풀이 곁창': sd})
    T('RF2-헛', '%s 헛잣대 바탕 — PC 목록 창 600 × 62vh' % eng, bool(b['f']) and abs(b['f']['w'] - 600) <= 2 and abs(b['f']['h'] - 558) <= 2, {'공식': b['f'], '풀이 곁창': b['곁창']})

    def fph(q):
        q.ev("()=>{try{delete WIN.pwf}catch(e){}pwList('f')}"); q.wait(500)
        return (q.ev("()=>__W.list()") or {}).get('rect')
    r2 = both(br, eng, 'phys', True, fph)
    T('RF2', '%s 폰 [공식] 목록 창 374×608 무변(= 바탕)' % eng, bool(r2['NEW']) and r2['NEW'] == r2['BASE'] and abs(r2['NEW']['w'] - 374) <= 1 and abs(r2['NEW']['h'] - 608) <= 1, [r2['NEW'], r2['BASE']])


OVER = r"""(ids)=>{const ps=ids.map(id=>{const b=document.getElementById(id);const p=b&&b.querySelector('.panel');return p?p.getBoundingClientRect():null});if(ps.some(x=>!x))return {miss:ids.filter((id,i)=>!ps[i])};
  const [a,c]=ps,x0=Math.max(a.left,c.left),x1=Math.min(a.right,c.right),y0=Math.max(a.top,c.top),y1=Math.min(a.bottom,c.bottom);if(x1-x0<4||y1-y0<4)return {nov:true};
  const at=document.elementFromPoint((x0+x1)/2,(y0+y1)/2),top=ids.find(id=>{const b=document.getElementById(id);return b&&at&&b.contains(at)})||(at?(at.id||at.className):null);
  return {top:top,z:ids.map(id=>document.getElementById(id).style.zIndex||getComputedStyle(document.getElementById(id)).zIndex)}}"""


def rf3(br, eng):
    """A-3 📋 창 · 🃏 창도 창 띠 — 📋 → [공식] = 목록 위 · [공식] → 📋 = 📋 위 · 띠 z 70~79(띠 위 창 차례 무변)"""
    def f(q):
        no = q.ev("()=>__W.noOf('PA0702')"); q.ev("n=>__W.openNo(n)", no); q.wait(600)
        q.ev("()=>{document.querySelectorAll('.sheet.shfloat').forEach(x=>x.remove())}")
        out = {}
        sec = q.ev("()=>Object.keys(TOC.sec)[0]")
        q.ev("s=>{try{jnOpen(s)}catch(e){}}", sec); q.wait(500); q.ev("()=>pwList('f')"); q.wait(500)
        out['📋→공식'] = q.ev(OVER, ['jnw', 'pwl'])
        q.ev("()=>{['jnw','pwl'].forEach(id=>{const e=document.getElementById(id);if(e)e.remove()})}")
        q.ev("()=>pwList('f')"); q.wait(500); q.ev("s=>{try{jnOpen(s)}catch(e){}}", sec); q.wait(500)
        out['공식→📋'] = q.ev(OVER, ['jnw', 'pwl'])
        q.ev("()=>{['jnw','pwl'].forEach(id=>{const e=document.getElementById(id);if(e)e.remove()})}")
        q.ev("async()=>{try{await mcwOpen('all')}catch(e){}}"); q.wait(600); q.ev("()=>pwList('f')"); q.wait(500)
        out['🃏→공식'] = q.ev(OVER, ['mcw', 'pwl'])
        out['띠 z'] = q.ev("()=>{const z=sel=>{const e=document.querySelector(sel);return e?getComputedStyle(e).zIndex:null};return {jnw:document.getElementById('jnw')?document.getElementById('jnw').style.zIndex:null,pwl:(document.getElementById('pwl')||{style:{}}).style.zIndex,mcw:(document.getElementById('mcw')||{style:{}}).style.zIndex}}")
        return out
    for phone in (True, False):
        dn = '폰' if phone else 'PC'
        r = both(br, eng, 'phys', phone, f)
        n, b = r['NEW'], r['BASE']
        ok = (n['📋→공식'] or {}).get('top') == 'pwl' and (n['공식→📋'] or {}).get('top') == 'jnw' and (n['🃏→공식'] or {}).get('top') == 'pwl'
        zs = [int(v) for v in (n['띠 z'] or {}).values() if v not in (None, '')]
        ok = ok and bool(zs) and all(70 <= z <= 79 for z in zs)
        T('RF3', '%s %s 📋 → [공식] = 목록 위 · [공식] → 📋 = 📋 위 · 🃏 → [공식] = 목록 위 · z 모두 띠 70~79(서브노트 80·참고 97·OCR 98 아래 그대로)' % (eng, dn), ok, n)
        T('RF3-헛', '%s %s 헛잣대 바탕 — 📋 → [공식] 에서 📋(z75 고정)가 위' % (eng, dn), (b['📋→공식'] or {}).get('top') == 'jnw', {'📋→공식': b['📋→공식'], '🃏→공식': b['🃏→공식']})


def rf4(br, eng):
    """A-4 [공식] 첫 편 머리 「0. 단위·기초 · 1」 · 1~6편 머리 무변"""
    def f(q):
        q.ev("()=>pwList('f')"); q.wait(500)
        return (q.ev("()=>__W.list()") or {}).get('heads')
    r = both(br, eng, 'phys', False, f)
    n, b = r['NEW'] or [], r['BASE'] or []
    T('RF4', '%s [공식] 첫 편 머리 = 「0. 단위·기초 · 1」 · 1~6편 머리 = 바탕' % eng, bool(n) and n[0] == '0. 단위·기초 · 1' and n[1:] == b[1:], n[:7])
    T('RF4-헛', '%s 헛잣대 바탕 — 첫 편 머리 이름 빈칸(「0.  · 1」)' % eng, bool(b) and b[0].replace(' ', '') == '0.·1', b[:1])


def rf5(br, eng):
    """A-5 물리 — 문제 창 → 풀이 곁창(곁창 위) → 문제 창 머리 누름 = 문제 창 위 · 곁창 안 단추(✕) 동작 무변"""
    OV = r"""()=>{const v=document.getElementById('view'),s=document.getElementById('sh-sol');const p=s&&s.querySelector('.panel');if(!v||!p)return {miss:true};
      const a=v.getBoundingClientRect(),c=p.getBoundingClientRect(),x0=Math.max(a.left,c.left),x1=Math.min(a.right,c.right),y0=Math.max(a.top,c.top),y1=Math.min(a.bottom,c.bottom);
      if(x1-x0<4||y1-y0<4)return {nov:true};
      const at=document.elementFromPoint((x0+x1)/2,(y0+y1)/2);return {top:v.contains(at)?'view':(s.contains(at)?'sol':(at?at.id||at.className:null)),zv:v.style.zIndex,zs:s.style.zIndex}}"""
    HD = r"""()=>{const v=document.getElementById('view'),h=v.querySelector('.vtop'),s=document.getElementById('sh-sol');const r=h.getBoundingClientRect(),c=s.querySelector('.panel').getBoundingClientRect();
      const t=v.querySelector('#title');if(t){const q=t.getBoundingClientRect(),x=q.left+q.width/2,y=q.top+q.height/2,a=document.elementFromPoint(x,y);   /* 제목 가운데(단추와 멀다 · 손가락 보정이 이웃 단추로 안 감) */
        if(a&&v.contains(a)&&!a.closest('button,a,input,select,[data-tool]')&&!(x>=c.left&&x<=c.right&&y>=c.top&&y<=c.bottom))return {cx:Math.round(x),cy:Math.round(y),on:true,at:'title'}}
      for(let y=r.top+4;y<r.bottom-4;y+=4)for(let x=r.left+40;x<r.right-6;x+=8){if(x>=c.left-2&&x<=c.right+2&&y>=c.top-2&&y<=c.bottom+2)continue;const a=document.elementFromPoint(x,y);
        if(a&&v.contains(a)&&!a.closest('button,a,input,select,[data-tool]'))return {cx:Math.round(x),cy:Math.round(y),on:true,at:(a.id||a.className||a.tagName).slice(0,20)}}return null}"""
    SOL = "()=>{const r=DATA.find(x=>x[F.NO]===VNO&&SOL[x[F.VLT]])||DATA.find(x=>SOL[x[F.VLT]]);if(r)solSheet(r)}"

    def f(q):
        no = q.ev("()=>__W.noOf('PA0702')"); q.ev("n=>__W.openNo(n)", no); q.wait(700)
        q.ev(SOL); q.wait(800)
        out = {}
        x = q.ev("()=>{const b=document.querySelector('#sh-sol .panel .shx');return b?__W.hit(b):null}")
        q.press(x, 600)
        out['✕ 닫힘'] = q.ev("()=>!document.getElementById('sh-sol')")
        q.ev(SOL); q.wait(800)
        out['열고'] = q.ev(OV)
        hd = q.ev(HD)
        q.press(hd, 600)
        out['머리 누름'] = q.ev(OV)
        out['머리 자리'] = hd
        return out
    for phone in (False, True):
        dn = '폰' if phone else 'PC'
        r = both(br, eng, 'phys', phone, f)
        n, b = r['NEW'], r['BASE']
        ok = (n['열고'] or {}).get('top') == 'sol' and (n['머리 누름'] or {}).get('top') == 'view'
        T('RF5', '%s %s 물리 문제 창 → 풀이 곁창(곁창 위) → 문제 창 머리 누름(%s) → 문제 창 위' % (eng, dn, '손가락' if phone else '마우스'), ok, {'열고': n['열고'], '누른 뒤': n['머리 누름'], '자리': n['머리 자리']})
        T('RF5-헛', '%s %s 헛잣대 바탕 — 문제 창 머리를 눌러도 곁창이 위' % (eng, dn), (b['머리 누름'] or {}).get('top') == 'sol', {'누른 뒤': b['머리 누름'], '자리': b['머리 자리']})
        T('RF5', '%s %s 곁창 안 단추(✕) 누름 = 닫힘(= 바탕 · 올리기만 더함)' % (eng, dn), n['✕ 닫힘'] is True and b['✕ 닫힘'] is True, [n['✕ 닫힘'], b['✕ 닫힘']])


def rf6(br, eng):
    """A-6 폰 ▾ — 왼쪽 끝+2 · 가운데 · 오른쪽 끝−2 = #fFoldBtn · #ndGrip 그대로(폭 13) · PC 머리 무변"""
    FB = r"""()=>{const b=document.getElementById('fFoldBtn'),g=document.getElementById('ndGrip');const r=b.getBoundingClientRect(),y=r.top+r.height/2;
      const at=[r.left+2,r.left+r.width/2,r.right-2].map(x=>{const a=document.elementFromPoint(x,y);return a?(a.id||a.className):null});const gr=g.getBoundingClientRect();
      return {at:at,fold:__W.R(b),grip:{w:Math.round(gr.width),x:Math.round(gr.left),vis:__W.vis(g)}}}"""
    for subj in ('phys', 'earth', 'bio'):
        r = both(br, eng, subj, True, lambda q: q.ev(FB))
        n, b = r['NEW'], r['BASE']
        T('RF6', '%s 폰 %s ▾ 왼쪽+2 · 가운데 · 오른쪽−2 = #fFoldBtn · 서랍 손잡이 그대로(폭 13 · 보임)' % (eng, subj), n['at'] == ['fFoldBtn'] * 3 and n['grip']['w'] == 13 and n['grip']['vis'], n)
        T('RF6-헛', '%s 폰 %s 헛잣대 바탕 — ▾ 왼쪽 끝이 손잡이(#ndGrip) 밑' % (eng, subj), b['at'][0] == 'ndGrip', b)
    r2 = both(br, eng, 'phys', False, lambda q: q.ev("()=>__W.pcHead()"))
    T('RF6', '%s PC 머리 글 = 바탕(무변)' % eng, r2['NEW'] == r2['BASE'], [r2['NEW'][:120], r2['BASE'][:120]])


def rf(br, eng):
    for fn in (rf1, rf2, rf3, rf4, rf5, rf6):
        try:
            fn(br, eng)
        except Exception as e:
            T('RUN', '%s · RF %s 멈춤' % (eng, fn.__name__), False, repr(e)[:600])


# ── RF2  _task_jagwa_revfix0928_fix1 — 0928 검수 고침 여덟(칸마다 NEW · 「-헛」 = 바탕 HEAD(이 판 바로 앞 커밋)가 옛 결함을 보임) ──
VP14 = {'width': 1440, 'height': 900}; VPIP = {'width': 820, 'height': 1180}; VPPH = {'width': 390, 'height': 844}
PANEL = r"""(id)=>{const b=document.getElementById(id);const p=b&&(b.querySelector(':scope>.panel')||b);if(!p)return null;const r=p.getBoundingClientRect();
  return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height),z:+(b.style.zIndex||getComputedStyle(b).zIndex)||0}}"""
GRIPAT = r"""(id)=>{const b=document.getElementById(id);const g=b&&b.querySelector('.twgrip');if(!g)return null;const r=g.getBoundingClientRect();return {cx:r.left+r.width/2,cy:r.top+r.height/2}}"""


def _resize(q, wid, w, h):
    """창 오른쪽 아래 모서리(.twgrip)를 마우스로 끌어 w×h 로"""
    p = q.ev(PANEL, wid); g = q.ev(GRIPAT, wid)
    if not p or not g:
        return None
    q.pg.mouse.move(g['cx'], g['cy']); q.pg.mouse.down()
    for i in range(1, 9):
        q.pg.mouse.move(g['cx'] + (w - p['w']) * i / 8, g['cy'] + (h - p['h']) * i / 8); q.wait(16)
    q.pg.mouse.up(); q.wait(300)
    return q.ev(PANEL, wid)


def _want(q, w, h):
    vw, vh = q.vpw['width'], q.vpw['height']
    return {'w': max(280, min(vw - 16, w)), 'h': max(200, min(vh - 16, h))}


def rf2_1(br, eng):
    """B1(검수 1) [공식] 목록 창 크기 기억 — 끌어 460×498 → 새로고침 → 다시 열기 = 그 크기(화면 안) · 기억 없을 때 PC 560×648 무변"""
    for dn, vp in (('PC 1440', VP14), ('iPad 820', VPIP), ('폰 390', VPPH)):
        def f(q):
            out = {'처음': None}
            q.ev("()=>{try{pwList('f')}catch(e){}}"); q.wait(500)
            out['처음'] = q.ev(PANEL, 'pwl')
            out['끈 뒤'] = _resize(q, 'pwl', 460, 498)
            out['원함'] = _want(q, 460, 498)
            _reboot(q); q.ev("()=>{try{pwList('f')}catch(e){}}"); q.wait(500)
            out['새로고침 뒤'] = q.ev(PANEL, 'pwl')
            return out
        r = both(br, eng, 'phys', vp == VPPH, f, vp)
        n, b = r['NEW'], r['BASE']
        ok = bool(n['새로고침 뒤']) and abs(n['새로고침 뒤']['w'] - n['원함']['w']) <= 2 and abs(n['새로고침 뒤']['h'] - n['원함']['h']) <= 2
        if dn == 'PC 1440':
            ok = ok and n['처음'] and (n['처음']['w'], n['처음']['h']) == (560, 648)
        T('RF2-B1', '%s %s [공식] 목록 창 끌어 460×498 → 새로고침 → 다시 열기 = %s(화면 안)%s' % (eng, dn, '%(w)d×%(h)d' % n['원함'], ' · 기억 없을 때 560×648' if dn == 'PC 1440' else ''), ok,
          {k: n[k] for k in ('처음', '끈 뒤', '새로고침 뒤')})
        T('RF2-B1-헛', '%s %s 헛잣대 바탕 — 새로고침 뒤 크기 기억 안 읽힘(첫 크기)' % (eng, dn), bool(b['새로고침 뒤']) and b['처음'] and (b['새로고침 뒤']['w'], b['새로고침 뒤']['h']) == (b['처음']['w'], b['처음']['h']),
          {k: b[k] for k in ('처음', '새로고침 뒤')})


def rf2_2(br, eng):
    """B2(검수 2) shFloat 곁창(풀이 곁창 · 공식 창) 같은 잣대"""
    OPEN = {'sol': "()=>{const r=DATA.find(x=>SOL[x[F.VLT]]);if(r)solSheet(r)}", 'type': "()=>{try{typeSheet(VNO)}catch(e){}}"}
    for key, js in OPEN.items():
        def f(q):
            no = q.ev("()=>__W.noOf('PA0702')"); q.ev("n=>__W.openNo(n)", no); q.wait(500)
            q.ev(js); q.wait(700)
            out = {'처음': q.ev(PANEL, 'sh-' + key)}
            out['끈 뒤'] = _resize(q, 'sh-' + key, 460, 498)
            out['원함'] = _want(q, 460, 498)
            _reboot(q); q.ev("n=>__W.openNo(n)", no); q.wait(500); q.ev(js); q.wait(700)
            out['새로고침 뒤'] = q.ev(PANEL, 'sh-' + key)
            return out
        r = both(br, eng, 'phys', False, f, VP14)
        n, b = r['NEW'], r['BASE']
        ok = bool(n['새로고침 뒤']) and abs(n['새로고침 뒤']['w'] - n['원함']['w']) <= 2 and abs(n['새로고침 뒤']['h'] - n['원함']['h']) <= 2
        T('RF2-B2', '%s PC 1440 곁창 %s 끌어 460×498 → 새로고침 → 다시 열기 = 460×498' % (eng, key), ok, {k: n[k] for k in ('처음', '끈 뒤', '새로고침 뒤')})
        T('RF2-B2-헛', '%s 헛잣대 바탕 — 곁창 %s 크기 기억 안 읽힘(바탕 흠)' % (eng, key), bool(b['새로고침 뒤']) and (b['새로고침 뒤']['w'], b['새로고침 뒤']['h']) == (b['처음']['w'], b['처음']['h']),
          {k: b[k] for k in ('처음', '새로고침 뒤')})


def rf2_3(br, eng):
    """B3(검수 5) PC 1440 · iPad 820 — 문제 창이 떠 있을 때 목록 창 첫 자리 = 오른쪽(자리 있으면 문제 창 옆 · 없으면 화면 오른쪽 끝) · 문제 창과 겹친 넓이 ≤ cedc251"""
    OV = r"""()=>{const v=document.getElementById('view'),b=document.getElementById('pwl');const p=b&&b.querySelector('.panel');if(!v||!p)return null;
      const a=v.getBoundingClientRect(),c=p.getBoundingClientRect(),w=Math.max(0,Math.min(a.right,c.right)-Math.max(a.left,c.left)),h=Math.max(0,Math.min(a.bottom,c.bottom)-Math.max(a.top,c.top));
      return {view:[Math.round(a.left),Math.round(a.top),Math.round(a.width),Math.round(a.height)],list:[Math.round(c.left),Math.round(c.top),Math.round(c.width),Math.round(c.height)],over:Math.round(w*h),right:Math.round(innerWidth-c.right)}}"""
    for dn, vp in (('PC 1440', VP14), ('iPad 820', VPIP)):
        def f(q):
            no = q.ev("()=>__W.noOf('PA0702')"); q.ev("n=>__W.openNo(n)", no); q.wait(600)
            q.ev("()=>{try{pwList('f')}catch(e){}}"); q.wait(500)
            return q.ev(OV)
        r = both(br, eng, 'phys', False, f, vp, ('NEW', 'BASE', 'C0'))
        n, b, c0 = r['NEW'], r['BASE'], r['C0']
        okp = bool(n) and (n['right'] == 8 or n['list'][0] >= n['view'][0] + n['view'][2] + 7) and n['list'][1] == n['view'][1]
        T('RF2-B3', '%s %s 목록 창 첫 자리 = 문제 창 오른쪽(자리 있으면) 또는 화면 오른쪽 끝(8) · 위 끝 = 문제 창 위 끝' % (eng, dn), okp, {'새': n})
        ra = lambda x: round(x['over'] / (x['list'][2] * x['list'][3]), 3) if x else None
        T('RF2-B3', '%s %s 겹친 넓이 %s ≤ cedc251 %s(글자 그대로) — 목록 창 넓이 비 새 %s · cedc251 %s(0928 A-2 로 창이 560×72%% · cedc251 = 600×62vh)' % (eng, dn, n and n['over'], c0 and c0['over'], ra(n), ra(c0)),
          bool(n) and n['over'] <= (c0 or {}).get('over', -1), {'새': n, 'cedc251': c0})
        T('RF2-B3-헛', '%s %s 헛잣대 바탕 — 목록 창이 화면 가운데(문제 창을 덮음 · 겹친 넓이 > cedc251)' % (eng, dn), bool(b) and b['over'] > (c0 or {}).get('over', 1e9), b)


OMRPT = r"""()=>{const p=document.getElementById('omrPad'),g=p.querySelector('.ogrip'),b=p.querySelector('button[data-omr]');const gr=g.getBoundingClientRect(),br=b.getBoundingClientRect(),mid=(gr.right+br.left)/2,y=(gr.top+gr.bottom)/2;
  return {gc:[gr.left+gr.width/2,y],gr1:[gr.right-1,y],m1:[mid-1,y],p1:[mid+1,y],b1:[br.left+br.width/2,(br.top+br.bottom)/2],mid:mid,gap:br.left-gr.right}}"""


def rf2_4(br, eng):
    """B4(검수 3) 폰 390 · iPad 820 — 마우스 포인터(터치 보정 없음)로 ≡ 가운데 · ≡ 오른쪽 −1 · 가운데 선 −1 = ≡ 잡기 · 가운데 선 +1 · ① 가운데 = ① · 끌기 60px 저장 · 새로고침 뒤 같음 · 손가락 흉내도 같음"""
    PK = "()=>{if(!window.__pkOn){window.__pkOn=1;window.__pk=[];const o=window.omrPick;window.omrPick=function(c){window.__pk.push(c);return o.apply(this,arguments)}}return (window.__pk||[]).splice(0)}"   # 고른 답 셈(같은 답 두 번째는 채점 기록이 안 늘어 hist 로는 못 셈)

    def f(q, mode):
        no = q.ev("()=>__W.noOf('PA0702')"); q.ev("n=>__W.openNo(n)", no); q.wait(800)
        q.ev("()=>{document.querySelectorAll('.sheet.shfloat').forEach(x=>x.remove())}")
        out = {}
        q.ev(PK)
        for k in ('gc', 'gr1', 'm1', 'p1', 'b1'):
            pt = q.ev(OMRPT); x, y = pt[k]
            q.ev(PK); h0 = q.ev(HN); o0 = q.ev(OP)
            if mode == 'mouse':
                q.pg.mouse.move(x, y); q.pg.mouse.down()
                for i in range(1, 7):
                    q.pg.mouse.move(x + 60 * i / 6 if k in ('gc', 'gr1', 'm1') else x, y); q.wait(16)
                q.pg.mouse.up(); q.wait(600)
            else:
                if k in ('gc', 'gr1', 'm1'):
                    q.drag(x, y, x + 60, y)
                else:
                    q.press({'cx': x, 'cy': y, 'on': True}, 600)
            o1 = q.ev(OP)
            out[k] = {'고름': q.ev(PK), '채점': q.ev(HN) - h0, '옮김': bool(o1 and (o1.get('own') != (o0 or {}).get('own'))), 'x': round(x, 1)}
            q.ev("()=>{document.querySelectorAll('.sheet.shfloat').forEach(x=>x.remove())}"); q.wait(200)   # 답을 고르면 풀이 곁창이 OMR 위에 뜬다 — 다음 누름 전에 걷는다
            if k in ('gc', 'gr1', 'm1'):
                out[k]['pos'] = o1
        out['간격'] = round(pt['gap'], 1)
        _reboot(q); q.ev("n=>__W.openNo(n)", no); q.wait(800)
        out['새로고침 뒤'] = q.ev(OP)
        return out
    for dn, vp in (('폰 390', VPPH), ('iPad 820', VPIP)):
        for mode in ('mouse', 'touch'):
            r = both(br, eng, 'phys', vp == VPPH, lambda q: f(q, mode), vp)
            n, b = r['NEW'], r['BASE']
            okg = all(n[k]['옮김'] and not n[k]['고름'] for k in ('gc', 'gr1', 'm1'))
            oko = all(n[k]['고름'] == ['①'] and not n[k]['옮김'] for k in ('p1', 'b1'))
            last = n['m1'].get('pos') or {}
            ok = okg and oko and (n['새로고침 뒤'] or {}).get('own') == last.get('own')
            T('RF2-B4', '%s %s %s — ≡ 가운데·오른끝−1·가운데 선−1 = 잡기(60px 끌어 저장 · 채점 0) · 가운데 선+1·① 가운데 = ①(채점 +1) · 새로고침 뒤 같음 · 틈 %spx' % (eng, dn, '마우스' if mode == 'mouse' else '손가락', n['간격']),
              ok, {k: n[k] for k in ('gc', 'gr1', 'm1', 'p1', 'b1')})
            if mode == 'mouse':   # 손가락 흉내는 크로미움 터치 보정(0928 :active)이 바탕도 맞게 옮겨 잡아 헛잣대가 안 된다 — 마우스(보정 없음)만 잰다
                T('RF2-B4-헛', '%s %s 마우스 헛잣대 바탕 — 가운데 선 ±1(틈)에서 잡기·① 둘 다 아님' % (eng, dn),
                  not (b['m1']['옮김'] and b['p1']['고름'] == ['①']), {k: b[k] for k in ('m1', 'p1')})
            else:
                N('RF2-B4i', '%s %s 손가락 흉내 바탕(참고 · 크로미움 보정)' % (eng, dn), {k: b[k] for k in ('m1', 'p1')})


ZTOP = r"""(ids)=>{const ps=ids.map(id=>{const b=document.getElementById(id);const p=b&&(b.querySelector(':scope>.panel')||b);return p?p.getBoundingClientRect():null});if(ps.some(x=>!x))return {miss:ids.filter((id,i)=>!ps[i])};
  const [a,c]=ps,x0=Math.max(a.left,c.left),x1=Math.min(a.right,c.right),y0=Math.max(a.top,c.top),y1=Math.min(a.bottom,c.bottom);if(x1-x0<4||y1-y0<4)return {nov:true};
  const at=document.elementFromPoint((x0+x1)/2,(y0+y1)/2),top=ids.find(id=>{const b=document.getElementById(id);return b&&at&&b.contains(at)})||(at?(at.id||at.className):null);
  return {top:top,z:ids.map(id=>+(document.getElementById(id).style.zIndex||getComputedStyle(document.getElementById(id)).zIndex))}}"""


def rf2_5(br, eng):
    """B5(검수 4) 물리 PC #gguw ↔ [공식] · 지학 #bpl ↔ 📋 — 나중에 연 창이 위 · 머리 누름 = 그 창 위 · z 70~79"""
    GG = "()=>{const r=DATA.find(x=>ggOf(GGU(x)).length>0)||DATA[0];ggUseWin(GGU(r),'')}"
    def fp(q):
        no = q.ev("()=>__W.noOf('PA0702')"); q.ev("n=>__W.openNo(n)", no); q.wait(500)
        out = {}
        q.ev(GG); q.wait(500); q.ev("()=>pwList('f')"); q.wait(500)
        out['gguw→공식'] = q.ev(ZTOP, ['gguw', 'pwl'])
        q.ev("()=>{['gguw','pwl'].forEach(id=>{const e=document.getElementById(id);if(e)e.remove()})}")
        q.ev("()=>pwList('f')"); q.wait(500); q.ev(GG); q.wait(500)
        out['공식→gguw'] = q.ev(ZTOP, ['gguw', 'pwl'])
        return out
    r = both(br, eng, 'phys', False, fp, VP14)
    n, b = r['NEW'], r['BASE']
    zs = [z for v in n.values() for z in (v or {}).get('z', [])]
    ok = (n['gguw→공식'] or {}).get('top') == 'pwl' and (n['공식→gguw'] or {}).get('top') == 'gguw' and zs and all(70 <= z <= 79 for z in zs)
    T('RF2-B5', '%s 물리 PC #gguw → [공식] = [공식] 위 · [공식] → #gguw = #gguw 위 · z 70~79' % eng, ok, n)
    T('RF2-B5-헛', '%s 헛잣대 바탕 — #gguw(z80 고정)가 늘 위' % eng, (b['gguw→공식'] or {}).get('top') == 'gguw', b)

    def fe(q):
        no = q.ev("()=>DATA.find(r=>!isC(r))[F.NO]"); q.ev("n=>__W.openNo(n)", no); q.wait(500)
        out = {}; sec = q.ev("()=>Object.keys(TOC.sec)[0]")
        q.ev("n=>bplOpen(n)", no); q.wait(500); q.ev("s=>{try{jnOpen(s)}catch(e){}}", sec); q.wait(500)
        out['bpl→📋'] = q.ev(ZTOP, ['bpl', 'jnw'])
        q.ev("()=>{['bpl','jnw'].forEach(id=>{const e=document.getElementById(id);if(e)e.remove()})}")
        q.ev("s=>{try{jnOpen(s)}catch(e){}}", sec); q.wait(500); q.ev("n=>bplOpen(n)", no); q.wait(500)
        out['📋→bpl'] = q.ev(ZTOP, ['bpl', 'jnw'])
        return out
    r = both(br, eng, 'earth', False, fe, VP14)
    n, b = r['NEW'], r['BASE']
    zs = [z for v in n.values() for z in (v or {}).get('z', [])]
    ok = (n['bpl→📋'] or {}).get('top') == 'jnw' and (n['📋→bpl'] or {}).get('top') == 'bpl' and zs and all(70 <= z <= 79 for z in zs)
    T('RF2-B5', '%s 지학 PC #bpl → 📋 = 📋 위 · 📋 → #bpl = #bpl 위 · z 70~79' % eng, ok, n)
    T('RF2-B5-헛', '%s 헛잣대 바탕 — #bpl(z76 고정) 차례가 연 차례와 다름' % eng, not ((b['bpl→📋'] or {}).get('top') == 'jnw' and (b['📋→bpl'] or {}).get('top') == 'bpl'), b)


DLJS = r"""()=>{const b=document.getElementById('dl');b.classList.remove('hide');b.classList.remove('err');b.textContent='시험지 6개를 받았습니다';
  const g=document.getElementById('ndGrip').getBoundingClientRect();const rg=document.createRange();rg.selectNodeContents(b);const t=[...rg.getClientRects()];
  const bad=[];document.querySelectorAll('#esh *').forEach(e=>{const cs=getComputedStyle(e);if(cs.display==='none'||cs.visibility==='hidden')return;
    if(![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))return;const r=e.getBoundingClientRect();if(r.width<=0||r.top>420)return;
    const q=document.createRange();q.selectNodeContents(e);const L=Math.min(...[...q.getClientRects()].map(x=>x.left));if(L<g.right+1)bad.push((e.id||e.className||e.tagName).slice(0,16)+'「'+e.textContent.trim().slice(0,10)+'」'+Math.round(L))});
  const r=b.getBoundingClientRect();return {grip:Math.round(g.right),text0:t.length?Math.round(t[0].left):null,box:[Math.round(r.left),Math.round(r.width)],bad:bad}}"""


def rf2_6(br, eng):
    """B6(검수 6) 폰 390 세 과목 — 머리 아래 띠 첫 글자 x ≥ 손잡이 오른쪽 + 1 · 손잡이와 겹친 글자 0"""
    for subj in ('phys', 'earth', 'bio'):
        r = both(br, eng, subj, True, lambda q: q.ev(DLJS))
        n, b = r['NEW'], r['BASE']
        T('RF2-B6', '%s 폰 %s 띠 「시험지 6개를 받았습니다」 첫 글자 x %s ≥ 손잡이 오른쪽 %s + 1 · 머리 글자 겹침 0' % (eng, subj, n['text0'], n['grip']), n['text0'] >= n['grip'] + 1 and not n['bad'], n)
        T('RF2-B6-헛', '%s 폰 %s 헛잣대 바탕 — 띠 글자가 손잡이에 붙음(x < 손잡이 + 1)' % (eng, subj), b['text0'] < b['grip'] + 1, b)


HIT = r"""(sel)=>{const L=[...document.querySelectorAll(sel)].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.top>=0&&r.bottom<=innerHeight});const e=L[0];if(!e)return null;
  const r=e.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2,own=a=>!!a&&(a===e||e.contains(a));
  let t=null,b=null;for(let y=Math.floor(r.top-24);y<=Math.ceil(r.bottom+24);y++){if(own(document.elementFromPoint(cx,y+0.5))){if(t===null)t=y;b=y+1}}
  let l=null,rr=null;for(let x=Math.floor(r.left-24);x<=Math.ceil(r.right+24);x++){if(own(document.elementFromPoint(x+0.5,cy))){if(l===null)l=x;rr=x+1}}
  return {vis:[Math.round(r.left*10)/10,Math.round(r.top*10)/10,Math.round(r.width*10)/10,Math.round(r.height*10)/10],hit:{w:l===null?0:rr-l,h:t===null?0:b-t,t,b,l,r:rr},lines:Math.round(r.height/parseFloat(getComputedStyle(e).lineHeight||'16')||1)}}"""
TARGETS = [('phys', 'first', ['#fFoldBtn', '.pwchip.ph']), ('phys', 'jnw', ['#jnw .jgo', '.jnrow .jnans', '#jnwX']),
           ('bio', 'mcw', ['#mcwX', '#mcwSel', '#mcwInk', '#mcwBk', '#mcwOmr']), ('earth', 'jnw', ['#jnwX'])]


def rf2_7(br, eng):
    """B7(검수 7) 폰 390 작은 누름 대상 — 누름 칸 ≥ 36(못 되면 값) · 보이는 사각형 = 바탕 · 이웃 누름 칸 겹침 0 · 지학 「닫기」 한 줄"""
    def f(q, scr, sels):
        if scr == 'jnw':
            q.ev("()=>{try{jnOpen(Object.keys(TOC.sec)[0])}catch(e){}}"); q.wait(700)
        elif scr == 'mcw':
            q.ev("async()=>{try{await mcwOpen('all')}catch(e){}}"); q.wait(800)
        return {s: q.ev(HIT, s) for s in sels}
    for subj, scr, sels in TARGETS:
        r = both(br, eng, subj, True, lambda q: f(q, scr, sels))
        n, b = r['NEW'], r['BASE']
        for s in sels:
            x, y = n.get(s), b.get(s)
            if not x:
                T('RF2-B7', '%s 폰 %s %s %s — 없음' % (eng, subj, scr, s), False, x); continue
            want36 = s not in ('#mcwSel',)
            same = s == '#jnwX' or (y and x['vis'][2:] == y['vis'][2:])   # 보이는 크기(폭·높이) — 자리는 「닫기」가 한 줄이 되며 머리가 낮아져 위로 갈 수 있다
            okk = (x['hit']['h'] >= 36 or s in ('#mcwInk', '#mcwBk', '#mcwOmr') and x['hit']['h'] >= 34 or not want36) and same
            if s == '#jnwX':
                okk = okk and x['vis'][3] < 30
            T('RF2-B7', '%s 폰 %s %s %s — 누름 칸 %d×%d(보이는 %s×%s · 바탕 누름 %s)' % (eng, subj, scr, s, x['hit']['w'], x['hit']['h'], x['vis'][2], x['vis'][3], y and '%d×%d' % (y['hit']['w'], y['hit']['h'])),
              okk, {'새': x, '바탕': y})
        # 이웃 겹침 — 누름 칸 사각형끼리
        bx = [(s, v['hit']) for s, v in n.items() if v and v['hit']['t'] is not None and v['hit']['l'] is not None]
        ov = [(a[0], c[0]) for i, a in enumerate(bx) for c in bx[i + 1:] if min(a[1]['r'], c[1]['r']) - max(a[1]['l'], c[1]['l']) > 0.5 and min(a[1]['b'], c[1]['b']) - max(a[1]['t'], c[1]['t']) > 0.5]
        T('RF2-B7', '%s 폰 %s %s 누름 칸 겹침 0' % (eng, subj, scr), not ov, ov)
    r = both(br, eng, 'phys', True, lambda q: q.ev(HIT, '.pwchip.ph'))
    T('RF2-B7-헛', '%s 폰 헛잣대 바탕 — [공식] 칩 누름 높이 < 36' % eng, (r['BASE'] or {}).get('hit', {}).get('h', 99) < 36, r['BASE'])


def rf2_8(br, eng):
    """B8(검수 8) 생물 폰 390 — 목록 맨 아래(굴림 끝) 마지막 줄 bottom ≤ 화면 높이 − 8 · 📋 창 굴림 끝 마지막 줄 ≤ 창 아래 − 8"""
    LB = r"""()=>{window.scrollTo(0,1e9);const its=[...document.querySelectorAll('#list .item')];const last=its[its.length-1];
      const tags=last?[...last.querySelectorAll('.tag,.jgo')].filter(t=>t.getBoundingClientRect().height>0).map(t=>Math.round(t.getBoundingClientRect().bottom)):[];
      return {vh:innerHeight,last:last?Math.round(last.getBoundingClientRect().bottom):null,tagMax:tags.length?Math.max(...tags):null}}"""
    JB = r"""async()=>{try{jnOpen(Object.keys(TOC.sec)[0])}catch(e){}await new Promise(r=>setTimeout(r,700));const b=document.getElementById('jnwBody');if(!b)return null;b.scrollTop=b.scrollHeight;
      const p=b.getBoundingClientRect();const L=[...b.querySelectorAll('.tag,.jgo,.jnans,button')].filter(e=>e.getBoundingClientRect().height>0);return {bodyBottom:Math.round(p.bottom),last:L.length?Math.round(Math.max(...L.map(e=>e.getBoundingClientRect().bottom))):null}}"""
    r = both(br, eng, 'bio', True, lambda q: {'목록': q.ev(LB), '📋': q.ev(JB)})
    n, b = r['NEW'], r['BASE']
    ok = n['목록']['last'] <= n['목록']['vh'] - 8 and (n['📋'] or {}).get('last', 1e9) <= (n['📋'] or {}).get('bodyBottom', 0) - 8
    T('RF2-B8', '%s 생물 폰 목록 굴림 끝 마지막 줄 bottom %s ≤ %s − 8 · 📋 창 굴림 끝 %s ≤ %s − 8' % (eng, n['목록']['last'], n['목록']['vh'], (n['📋'] or {}).get('last'), (n['📋'] or {}).get('bodyBottom')), ok, n)
    T('RF2-B8-헛', '%s 헛잣대 바탕 — 목록 마지막 줄이 화면 아래 끝에 붙음(> 높이 − 8)' % eng, b['목록']['last'] > b['목록']['vh'] - 8, b)


SW2 = r"""(touch)=>{const vw=innerWidth,vh=innerHeight,de=document.documentElement;
 const ACT='button,a[href],input,select,[onclick],.chip,.chchip,.pwchip,.jgo,[data-go],[data-omr],.ogrip';
 const sig=e=>{let s=e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(e.classList.length?'.'+[...e.classList].slice(0,2).join('.'):'');const t=(e.textContent||'').replace(/\s+/g,' ').trim().replace(/\d+/g,'#').slice(0,10);return s+'「'+t+'」'};
 const els=[...document.querySelectorAll(ACT)].filter(e=>{const cs=getComputedStyle(e);if(cs.display==='none'||cs.visibility==='hidden')return false;const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.bottom>0&&r.right>0&&r.top<vh&&r.left<vw});
 const over=[],cover=[],small=[],coverBy={};
 for(const e of els){const r=e.getBoundingClientRect();if(r.right>vw+1)over.push(sig(e));
   const cx=Math.min(vw-1,Math.max(0,r.left+r.width/2)),cy=Math.min(vh-1,Math.max(0,r.top+r.height/2)),at=document.elementFromPoint(cx,cy);if(at&&!(at===e||e.contains(at)||at.contains(e))){const sg=sig(e),w=at.closest('.sheet')||at.closest('[id]');cover.push(sg);(coverBy[sg]=coverBy[sg]||[]).push(w?(w.id||w.className):at.tagName)}
   if(touch){let h=0;for(let y=Math.floor(r.top-20);y<=Math.ceil(r.bottom+20);y++){const a=document.elementFromPoint(cx,y+0.5);if(a&&(a===e||e.contains(a)))h++}if(h<36)small.push(sig(e))}}
 return {docow:de.scrollWidth-de.clientWidth,over,cover,small,coverBy}}"""


def rf2_12(br, eng):
    """B12 화면 훑기 — 세 과목 × PC 1440 · iPad 820 · 폰 390 · 첫 화면 · 문제 창 · 📋 · [공식] · 🃏 · #gguw — 새로 생긴 넘침·덮임·작은 누름(누름 칸 < 36) 0"""
    import collections
    def f(q, subj):
        touch = q.touch; out = {}
        out['첫 화면'] = q.ev(SW2, touch)
        no = q.ev("()=>__W.noOf('PA0702')") if subj == 'phys' else q.ev("()=>DATA.find(r=>!isC(r))[F.NO]")
        q.ev("n=>__W.openNo(n)", no); q.wait(500); out['문제 창'] = q.ev(SW2, touch)
        q.ev("()=>{try{jnOpen(Object.keys(TOC.sec)[0])}catch(e){}}"); q.wait(600); out['📋'] = q.ev(SW2, touch)
        if subj == 'phys':
            q.ev("()=>{try{pwList('f')}catch(e){}}"); q.wait(500); out['[공식]'] = q.ev(SW2, touch)
        q.ev("async()=>{try{await mcwOpen('all')}catch(e){}}"); q.wait(700); out['🃏'] = q.ev(SW2, touch)
        q.ev("()=>{const r=DATA.find(x=>ggOf(GGU(x)).length>0)||DATA[0];try{ggUseWin(GGU(r),'')}catch(e){}}"); q.wait(500); out['#gguw'] = q.ev(SW2, touch)
        return out
    newonly, rows, acc = [], [], []
    for subj in ('phys', 'earth', 'bio'):
        for dn, vp in (('PC 1440', VP14), ('iPad 820', VPIP), ('폰 390', VPPH)):
            r = both(br, eng, subj, vp == VPPH, lambda q: f(q, subj), vp)
            for scr in r['NEW']:
                nn, bb = r['NEW'][scr], (r['BASE'] or {}).get(scr) or {}
                line = {'칸': '%s · %s · %s' % (subj, dn, scr), '쪽 넘침': [nn['docow'], bb.get('docow')]}
                for cat in ('over', 'cover', 'small'):
                    d = collections.Counter(nn[cat]) - collections.Counter(bb.get(cat) or [])
                    line[cat] = [len(nn[cat]), len(bb.get(cat) or [])]
                    for s, k in d.items():
                        by = sorted(set((nn.get('coverBy') or {}).get(s) or [])) if cat == 'cover' else []
                        if by == ['pwl'] and scr in ('[공식]', '🃏'):   # 뜻한 차이 — A-2 목록 창(#pwl) 첫 자리가 화면 오른쪽 끝(t = 문제 창 위)으로 옮겨 덮는 것(연 차례대로 위)
                            acc.append({'칸': line['칸'], '신호': s, '수': k, '덮은 창': 'pwl'}); continue
                        newonly.append({'칸': line['칸'], '종류': cat, '신호': s, '수': k, '덮은 것': by})
                if nn['docow'] > (bb.get('docow') or 0):
                    newonly.append({'칸': line['칸'], '종류': '쪽 넘침', '신호': '%s > %s' % (nn['docow'], bb.get('docow'))})
                rows.append(line)
    T('RF2-B12', '%s 화면 훑기 — 세 과목 × PC 1440 · iPad 820 · 폰 390 × 첫 화면·문제 창·📋·[공식]·🃏·#gguw — 새로 생긴 넘침·덮임·작은 누름 0(뜻한 차이 %d = 목록 창 자리 A-2)' % (eng, len(acc)), not newonly,
      {'새로 생긴 것': newonly[:20], '뜻한 차이(A-2 목록 창이 덮음)': acc, '표': rows})
    N('RF2-B12', '%s 뜻한 차이 — 목록 창(#pwl)이 화면 오른쪽 끝으로 옮겨 새로 덮은 것' % eng, acc)


def rf2g(br, eng):
    for fn in (rf2_1, rf2_2, rf2_3, rf2_4, rf2_5, rf2_6, rf2_7, rf2_8, rf2_12):
        if ONLY2 and fn.__name__.split('_')[1] not in ONLY2:
            continue
        try:
            fn(br, eng)
        except Exception as e:
            T('RUN', '%s · RF2 %s 멈춤' % (eng, fn.__name__), False, repr(e)[:600])


ONLY2 = [x for x in (ARG('--rf2', '') or '').split(',') if x]   # fix1 RF2 — 칸 고르기(1,2,…,12)


PARTS = [('1', g1), ('2', g2), ('3', g3), ('4', g4), ('7', g7), ('8', g8b), ('RF', rf), ('RF2', rf2g)]
APPS = {}


def main():
    t0 = time.time()
    APPS['NEW'] = io.open(NEWF, encoding='utf-8').read()
    APPS['BASE'] = git('show', 'fd911d5:jagwa/index.html').decode('utf-8')   # ★ A-6(d) 9/30 _task_qa_baseline — 헛잣대 바탕 = 인도 앞 판 fd911d5(penfinger_add2 · docstring 「바로 앞 인도판」 · 인도 결과 「BASE HEAD 775457c」 = 같은 jagwa) · 인도(fb89ad2) 뒤 HEAD 는 이 판 자신
    APPS['C0'] = git('show', 'cedc251:jagwa/index.html').decode('utf-8')   # fix1 RF2-B3 — 겹친 넓이 잣대(cedc251)
    if not ONLY or '9' in ONLY:
        d9()
    with sync_playwright() as pw:
        for eng in ENGS:
            br = getattr(pw, eng).launch()
            try:
                for k, fn in PARTS:
                    if ONLY and k not in ONLY:
                        continue
                    print('── %s · %s' % (eng, k), flush=True)
                    try:
                        fn(br, eng)
                    except Exception as e:
                        T('RUN', '%s · %s 묶음이 멈춤' % (eng, k), False, repr(e)[:600])
            finally:
                br.close()
    npass = sum(1 for r in RES if r[2] is True); nfail = sum(1 for r in RES if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · phone_win · NEW %s(md5 LF %s) · BASE fd911d5 · genie HEAD %s · 그림 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), NEWF,
                hashlib.md5(APPS['NEW'].replace('\r\n', '\n').encode('utf-8')).hexdigest()[:8], git('rev-parse', '--short', 'HEAD').decode().strip(), IMG, ','.join(ENGS)))
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[ok], g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:900]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
