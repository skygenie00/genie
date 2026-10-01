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
    def __init__(self, br, eng, app, subj, tag, phone):
        self.eng, self.phone = eng, phone
        self.srv, port = serve(app, subj, tag + '_' + eng + ('_ph' if phone else '_pc'))
        vp = {'width': 390, 'height': 844} if phone else {'width': 1553, 'height': 900}
        self.ctx = br.new_context(viewport=vp, device_scale_factor=1, has_touch=True, is_mobile=bool(phone and eng == 'chromium'))
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
        if not self.phone:
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
        if self.cdp and self.phone:
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


def both(br, eng, subj, phone, fn):
    """NEW · BASE 한 벌씩"""
    out = {}
    for who, app in (('NEW', APPS['NEW']), ('BASE', APPS['BASE'])):
        q = Pg(br, eng, app, subj, who, phone)
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
    head = set(x for x in git('ls-tree', '--name-only', 'HEAD', 'jagwa/img/').decode('utf-8').split('\n') if x)
    T('9-헛', '헛잣대 바탕(HEAD) — 그 14 장 없음', not any(('jagwa/img/p%s.jpg' % g) in head for g in NEW14), {'HEAD 에 있음': sum(1 for g in NEW14 if ('jagwa/img/p%s.jpg' % g) in head)})


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


PARTS = [('1', g1), ('2', g2), ('3', g3), ('4', g4), ('7', g7), ('8', g8b), ('RF', rf)]
APPS = {}


def main():
    t0 = time.time()
    APPS['NEW'] = io.open(NEWF, encoding='utf-8').read()
    APPS['BASE'] = git('show', 'HEAD:jagwa/index.html').decode('utf-8')
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
        f.write('\n==== %s · phone_win · NEW %s(md5 LF %s) · BASE HEAD %s · 그림 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), NEWF,
                hashlib.md5(APPS['NEW'].replace('\r\n', '\n').encode('utf-8')).hexdigest()[:8], git('rev-parse', '--short', 'HEAD').decode().strip(), IMG, ','.join(ENGS)))
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[ok], g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:900]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
