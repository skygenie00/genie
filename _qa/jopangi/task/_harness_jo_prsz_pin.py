# -*- coding: utf-8 -*-
r"""_task_jo_prsz_pin §B 관문 — 팝업 크기 손잡이를 창 아래 끝(오른쪽 아래 모서리)에 세운다(글이 짧아도 · 늘려도 · 다시 열어도)

  python _harness_jo_prsz_pin.py [--new <앱 파일 | genie git 판>] [--base <판 = 9a40555>] [--only B1,B2,..] [--eng chromium[,webkit]] [--res <결과 파일>] [--shots <화면 폴더>]

  NEW  = genie 작업트리 jo/index.html(고친 판) · BASE = 바탕(cloud/jo_popsize 끝 9a40555) — 두 판을 같은 기기·같은 차례로 늘 같이 돌려
         헛잣대(바탕 FAIL 이어야 하는 칸)와 무변 칸(바탕과 같은 값)을 한 번에 센다 · 바탕을 못 읽으면 바탕 칸은 「안 잼」
  재는 값 = gap = (창 top + clientTop + clientHeight) − 손잡이(.prsz) getBoundingClientRect().bottom · 맞음 = |gap| ≤ 1(메모 창은 설계 1px — gap ≤ 1)
  데이터 = genie jo/data(실물 · 읽기만) · 기록 = 없음(쪽마다 localStorage 비움 · B4 메모 창만 지어낸 postit 둘) · 밖 주소 404
  기기 = 아이패드 세로 820×1180 · 834×1194 · 폰 390×844(터치 · DSF 2 · 손가락 = Chromium CDP Input.dispatchTouchEvent) · PC 1440×900 · 900×1200(마우스)
         WebKit 은 로컬이 합칠 때(--eng webkit · 끌기 = 신뢰 마우스 — playwright WebKit 끌기 터치 없음 · 도구 한계)
  관문:
    B1 아이패드 세로 · 민소 2차 목차노트 4.2.2. 「기출」 칩 창(글 짧음) 손잡이 터치 — 떼지 않고 +150 · +300 → gap 0 · 뗀 뒤 0(바탕 = 300)
    B2 글 긴 칩 창(칩 수 가장 많은 것) — 굴리기 전 · 끝까지 굴린 뒤 gap 0 · margin-top −16px = 바탕
    B3 B1 창 ✕ → 같은 칩 다시 → 기억 크기 · gap 0(바탕 = 300)
    B4 무변 — 2차 보드 메모 창(안 sized · sized) gap ≤ 1 · 원문 옆 창(wmWin ✎ 마크업 = 높이 줌 · 🔗인 = 높이 없음 · ↩피 = 발 줄) gap 0 — 바탕과 같은 값
    B5 노트 창 4.2.2. — 헤딩 넷 접고 손잡이 +200(짧은 sized 창) → gap 0 · 하나 펴면(굴러감) margin-top −16px · 다시 접으면 gap 0(바탕 = 접은 뒤 gap > 0)
    B6 B3 창 손잡이(모서리)를 잡아 −100 → 첫 pointerdown 이 .prsz · 높이 = 잡을 때 − 100 · gap 0
    B7 머리 더블클릭(기억 지움) → 기본 크기 · gap 0
    B8 폰 390×844 · 목차노트 칩 창 열자마자 gap 0(바탕 = 403) · +300 · 다시 열기 gap 0
    B9 훑기 1440×900 · 900×1200 · 834×1194 · 390×844 — 칩 창 +300(폰 +200) · 다시 열기 · 머리 끌기로 옮긴 뒤 gap 0 · 가로 넘침 0 · 그림
    B0 새 판 페이지 오류 0(pageerror · window error — 「ResizeObserver loop completed」 고리 오류 포함 · 바탕 오류는 값만)
  결과 = 화면 PASS/FAIL 줄 · --res 파일(기본 = 임시 폴더 · _qa 에 결과를 쓰지 않는다)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import hashlib, io, json, os, subprocess, sys, tempfile, threading, time, traceback, urllib.parse   # noqa: E402
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEW = ARG('--new', _roots.genie('jo', 'index.html'))
BASE = ARG('--base', '9a40555')   # cloud/jo_popsize 끝 = 이 판의 바탕
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
TMPD = os.path.join(tempfile.gettempdir(), 'h_jo_prsz_pin')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_jo_prsz_pin_result.txt'))
SHOTS = ARG('--shots', os.path.join(TMPD, 'shots'))
DATA = _roots.genie('jo', 'data')
NOTE = '4.2.2. 당사자결석(257조)(268조)(150③)(148조)'   # 민소 목차노트 — 「기출 1」 칩 창 = 글 짧음 · 노트 창 = 헤딩 넷
CHIP = 'cell|🔗 기출 — ' + NOTE
NOTEK = 'note|민소|' + NOTE + '|'
SEP = '\u001f'
F2461 = '민기출 24-61-2-관할{합}전부구별, 반소이송가부'
PIT = {SEP.join(['card|기출|' + F2461, '1', '2', '설문(1)']): {'t': '메모 창 손잡이 대조(합성)', 'who': '햄찌', 'at': '2026-10-04T00:00:00.000Z', 'ts': '2026-10-04T00:00:00.000Z'},
       SEP.join(['card|기출|' + F2461, '3', '2', '합의관할']): {'t': '두 번째 메모(합성)', 'who': '꼬까', 'at': '2026-10-04T00:00:00.000Z', 'ts': '2026-10-04T00:00:00.000Z'}}
IPAD_UA = 'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
IPHONE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
DEV = {'padP': dict(W=820, H=1180, touch=True, ua=IPAD_UA), 'pad834': dict(W=834, H=1194, touch=True, ua=IPAD_UA),
       'pc': dict(W=1440, H=900, touch=False), 'pc12': dict(W=900, H=1200, touch=False), 'phone': dict(W=390, H=844, touch=True, ua=IPHONE_UA)}

RES = []    # (묶음, 이름, 새 판 판정 True/False/None(INFO), 값)
YARD = []   # (묶음, 이름, 바탕 판정) — 같은 잣대를 바탕 값에(헛잣대 칸만)
ERRS = {}   # 판 → 페이지 오류(pageerror · window error — ResizeObserver 고리 오류도 여기로 온다)
T0 = time.time()


def T(g, name, ok, detail=''):
    RES.append((g, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', g, name, detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)[:700]), flush=True)


def N(g, name, detail=''):
    RES.append((g, name, None, detail))
    print('INFO | %s · %s | %s' % (g, name, detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)[:700]), flush=True)


def TB(g, name, ok_fn, vn, vb, yard=True):
    """새 판 판정 · 같은 잣대로 바탕 판정(yard = 헛잣대 칸이면 YARD 에 · 무변 칸은 따로 「바탕과 같음」으로 잰다)"""
    try:
        okn = bool(ok_fn(vn))
    except Exception:
        okn = False
    T(g, name, okn, {'new': vn, 'base': vb})
    if vb is not None and yard:
        try:
            okb = bool(ok_fn(vb))
        except Exception:
            okb = False
        YARD.append((g, name, okb))


def want(k):
    return not ONLY or k in ONLY


def sfx(eng):
    return '' if eng == 'chromium' else '·' + eng


def git(*a):
    return subprocess.run(['git', '-C', _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def app_src(x):
    if os.path.isfile(x):
        return open(x, 'rb').read().decode('utf-8')
    b = git('show', x + ':jo/index.html')
    return b.decode('utf-8') if b else None


def md5lf(s):
    return hashlib.md5(s.replace('\r\n', '\n').encode('utf-8')).hexdigest()


SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.alert=function(){};window.confirm=function(){return true;};window.prompt=function(){return null;};
(function(){var nf=window.fetch.bind(window);
window.fetch=function(u,o){var s=String((u&&u.url)||u);
 if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));
 return nf(u,o);};
try{localStorage.clear();}catch(e){} try{localStorage.setItem('tt.cfg',JSON.stringify({person:'꼬까'}));}catch(e){}
})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
</script>"""

# 페이지 도구(__PZ) — 재는 것 = DOM 실물(getBoundingClientRect · clientTop · clientHeight · 계산 margin-top · elementFromPoint · S.popCfg) · 누름·끌기는 파이썬이 진짜 손가락·마우스로
TOOLS = r"""
(function(){
const W = ms => new Promise(r => setTimeout(r, ms));
const busyNow = () => { try { return !!busy; } catch (e) { return false; } };
const idle = async () => { for (let i = 0; i < 800; i++){ if (!busyNow()) return true; await W(25); } return false; };
const live = () => { try { return POPS.filter(p => p.isConnected); } catch (e) { return []; } };
const byKey = k => live().find(p => p._pk === k) || null;
const vis = e => !!e && e.isConnected && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden';
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const hit = e => { if (!e) return null; const r = e.getBoundingClientRect(); const cx = r.left + r.width / 2, cy = r.top + r.height / 2; const a = document.elementFromPoint(cx, cy);
  return { cx: +cx.toFixed(1), cy: +cy.toFixed(1), on: !!a && (a === e || e.contains(a)) && cy > 0 && cy < innerHeight && cx > 0 && cx < innerWidth }; };
function gapOf(p){
  if (!p) return null; const g = p.querySelector(':scope > .prsz'); if (!g) return { k: p._pk || null, grip: null };
  const r = p.getBoundingClientRect(), gr = g.getBoundingClientRect(), gx = gr.left + gr.width / 2, gy = gr.top + gr.height / 2, a = document.elementFromPoint(gx, gy);
  const hd = p.querySelector(':scope > .ph'), hr = hd ? hd.getBoundingClientRect() : null, hx = hr ? hr.left + Math.min(hr.width * 0.35, 140) : 0, hy = hr ? hr.top + hr.height / 2 : 0, ha = hr ? document.elementFromPoint(hx, hy) : null;
  return { k: p._pk || null, gap: +((r.top + p.clientTop + p.clientHeight) - gr.bottom).toFixed(1), mt: getComputedStyle(g).marginTop, imt: g.style.marginTop || '',
    x: +r.left.toFixed(1), y: +r.top.toFixed(1), w: +r.width.toFixed(1), h: +r.height.toFixed(1), b: +r.bottom.toFixed(1), sh: p.scrollHeight, ch: p.clientHeight, st: Math.round(p.scrollTop), sized: p.classList.contains('sized'),
    grip: { cx: +gx.toFixed(1), cy: +gy.toFixed(1), on: !!a && (a === g || g.contains(a)) && gy > 0 && gy < innerHeight },
    head: hr ? { cx: +hx.toFixed(1), cy: +hy.toFixed(1), on: !!ha && (ha === hd || hd.contains(ha)) && hy > 0 && hy < innerHeight } : null, vh: innerHeight, vw: innerWidth };
}
window.__PZ = {
  idle,
  errs: () => (window.__ERR || []).slice(),
  async go(o){ await idle(); try { closeAllPops(true); } catch (e) {} Object.assign(S, o || {}); await render(); await idle(); await W(500); return { law: S.law, tab: S.tab, jo: S.jo || null }; },
  mokBtn(){ const b = document.getElementById('mokBtn'); if (!b || !vis(b)) return null; try { b.scrollIntoView({ block: 'nearest', inline: 'center' }); } catch (e) {} return hit(b); },
  hasList(){ return !!byKey('moknote|' + PLAW()); },
  /* 목차노트 목록 창 — 그 줄을 굴려(where) 칩(k) 또는 줄 이름 자리 · note = null 이면 칩 수가 가장 많은 칩(k 갈래 아무거나) */
  async mokRow(note, k, where){ const lp = byKey('moknote|' + PLAW()); if (!lp) return null;
    let r = null, c = null;
    if (note){ r = [...lp.querySelectorAll('.mkr')].find(x => x.dataset.note === note); if (!r) return { err: 'no row' }; c = k ? r.querySelector('.ck[data-k="' + k + '"]') : r.querySelector('.nm'); }
    else { let best = null, bn = -1; lp.querySelectorAll('.mkr .ck').forEach(x => { const n = parseInt((x.textContent || '').replace(/\D+/g, ''), 10) || 0; if (n > bn){ bn = n; best = x; } }); c = best; r = c && c.closest('.mkr'); }
    if (!c) return { err: 'no chip' };
    r.scrollIntoView({ block: where || 'center' }); await W(250);
    return Object.assign(hit(c), { t: txt(c), note: r.dataset.note, key: 'cell|🔗 ' + (c.dataset.k || '') + ' — ' + r.dataset.note }); },
  win(k){ return gapOf(byKey(k)); },
  sel(s, i){ const L = [...document.querySelectorAll(s)].filter(vis); return gapOf(L[i || 0] || null); },
  async waitWin(k, ms){ for (let i = 0; i < (ms || 4000) / 50; i++){ const p = byKey(k); if (p && p.querySelector(':scope > .pb') && p.querySelector(':scope > .pb').children.length){ await W(400); await idle(); return gapOf(p); } await W(50); } return gapOf(byKey(k)); },
  async waitSel(s, ms){ for (let i = 0; i < (ms || 4000) / 50; i++){ const p = [...document.querySelectorAll(s)].filter(vis).pop(); if (p){ await W(450); await idle(); return gapOf(p); } await W(50); } return null; },
  async scrollEnd(k){ const p = byKey(k); if (!p) return null; p.scrollTop = p.scrollHeight; await W(250); return gapOf(p); },
  cfg(k){ try { return JSON.parse(JSON.stringify((S.popCfg || {})[k] || null)); } catch (e) { return null; } },
  closeKey(k){ const p = byKey(k); const x = p && p.querySelector(':scope > .ph > button:not(.pall)'); return x ? hit(x) : null; },
  /* 노트 창 헤딩 접기 단추(.htog) — i 째 · 글(˅ = 펴짐 · › = 접힘) */
  togs(k){ const p = byKey(k); return p ? [...p.querySelectorAll('.htog')].map(t => (t.textContent || '').trim()) : null; },
  tog(k, i){ const p = byKey(k); const t = p && [...p.querySelectorAll('.htog')][i]; if (!t) return null; try { t.scrollIntoView({ block: 'nearest' }); } catch (e) {} return Object.assign(hit(t), { t: (t.textContent || '').trim() }); },
  setPit(o){ try { localStorage.setItem('jopangi.postit', JSON.stringify(o)); PITREC = null; PITIDX.rec = null; PITCIDX.rec = null; } catch (e) { return String(e); } return true; },
  title(code){ const r = [...document.querySelectorAll('#slot .c2row')].find(x => !x.classList.contains('c2ov') && (((x.querySelector('.c2code') || {}).textContent) || '').trim().indexOf(code) === 0);
    const t = r && r.querySelector('.c2t2'); if (!t) return null; try { t.scrollIntoView({ block: 'center' }); } catch (e) {} return hit(t); },
  chip(cls){ const b = [...document.querySelectorAll('#slot .conn .plgb.' + cls)].filter(vis)[0]; if (!b) return null; try { b.scrollIntoView({ block: 'center' }); } catch (e) {} return Object.assign(hit(b), { t: txt(b) }); },
  mkBtn(){ const b = [...document.querySelectorAll('#slot button')].find(x => /^✎ 마크업/.test((x.textContent || '').trim()) && vis(x)); if (!b) return null; try { b.scrollIntoView({ block: 'center' }); } catch (e) {} return hit(b); },
  foot(s){ const p = [...document.querySelectorAll(s)].filter(vis).pop(); return p ? !!p.querySelector(':scope > .wmft') : null; },
  overflow(){ const d = document.documentElement; return { docW: [d.scrollWidth, innerWidth] }; }
};
})();
"""


def inject(src):
    src = src.replace('\r\n', '\n')
    b = src.index('<body'); bb = src.index('>', b) + 1
    html = src[:bb] + SEED + src[bb:]
    e = html.rindex('</body>')
    return html[:e] + '<script>\n' + TOOLS + '\n</script>\n' + html[e:]


SERVERS = {}


def serve(tag, src):
    if tag in SERVERS:
        return SERVERS[tag][1]
    body = inject(src).encode('utf-8')

    class Hd(SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, data, ct='application/json'):
            self.send_response(code)
            self.send_header('Content-Type', ct)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            p = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
            if p in ('/jo/', '/jo/index.html'):
                return self._send(200, body, 'text/html; charset=utf-8')
            if p.startswith('/jo/data/'):
                f = os.path.join(DATA, *[x for x in p[len('/jo/data/'):].split('/') if x])
                if os.path.isfile(f):
                    return super().do_GET()
            return self._send(404, b'{"message":"Not Found"}')

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
            if p.startswith('/jo/data/'):
                return os.path.join(DATA, *[x for x in p[len('/jo/data/'):].split('/') if x])
            return os.path.join(HERE, '__없음__')

    srv = ThreadingHTTPServer(('127.0.0.1', 0), Hd)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


class P:
    """한 쪽(page) — 판(tag) · 기기(dev) · 엔진"""
    def __init__(self, br, eng, tag, src, dev):
        self.eng, self.tag, self.dev = eng, tag, dev
        d = DEV[dev]
        self.touch = d['touch']
        port = serve(tag, src)
        kw = dict(viewport={'width': d['W'], 'height': d['H']})
        if d['touch']:
            kw.update(device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=d.get('ua'))
        self.ctx = br.new_context(**kw)
        self.ctx.route('**/*', lambda r: r.continue_() if r.request.url.startswith('http://127.0.0.1') else r.abort())
        self.pg = self.ctx.new_page()
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:300]))
        self.cdp = self.ctx.new_cdp_session(self.pg) if (eng == 'chromium' and d['touch']) else None
        self.how = 'touch' if self.cdp else ('mouse(WebKit 끌기 도구 한계)' if d['touch'] else 'mouse')
        self.pg.goto('http://127.0.0.1:%d/jo/index.html' % port, wait_until='load', timeout=120000)
        self.pg.wait_for_function("!!window.__PZ&&typeof render==='function'&&typeof popSizable==='function'&&!!document.querySelector('#slot')", timeout=120000)
        self.pg.wait_for_timeout(1200)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def idle(self, ms=300):
        self.pg.wait_for_timeout(ms)
        self.ev("()=>__PZ.idle()")

    def tap(self, at, wait=600):
        if not at or not at.get('on'):
            return False
        self.pg.wait_for_timeout(120)
        x, y = at['cx'], at['cy']
        if self.cdp:
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'id': 1}]})
            self.pg.wait_for_timeout(40)
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        elif self.touch:
            self.pg.touchscreen.tap(x, y)
        else:
            self.pg.mouse.click(x, y)
        self.idle(wait)
        return True

    def hold(self, at, stages, measure, n=10):
        """잡은 자리에서 손을 떼지 않고 누적 (dx, dy) 자리마다 measure() · 끝에 뗌 · (값 목록, 뗀 뒤 값)"""
        if not at:
            return [], None
        x0, y0 = at['cx'], at['cy']; cx, cy = x0, y0; out = []
        if self.cdp:
            t = lambda ty, x, y: self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': ([] if ty == 'touchEnd' else [{'x': x, 'y': y, 'id': 1}])})
            t('touchStart', x0, y0); self.pg.wait_for_timeout(30)
        else:
            self.pg.mouse.move(x0, y0); self.pg.mouse.down()
        for dx, dy in stages:
            tx, ty = x0 + dx, y0 + dy
            for i in range(1, n + 1):
                x, y = cx + (tx - cx) * i / n, cy + (ty - cy) * i / n
                if self.cdp:
                    t('touchMove', x, y)
                else:
                    self.pg.mouse.move(x, y)
                self.pg.wait_for_timeout(16)
            cx, cy = tx, ty
            self.pg.wait_for_timeout(120)
            out.append(measure())
        if self.cdp:
            t('touchEnd', cx, cy)
        else:
            self.pg.mouse.up()
        self.idle(400)
        return out, measure()

    def drag(self, at, dx, dy):
        vals, end = self.hold(at, [(dx, dy)], lambda: None)
        return True

    def dbl(self, at):
        """머리 더블클릭 — 마우스(터치 기기도 · 더블탭 확대와 섞이지 않게)"""
        if not at:
            return False
        self.pg.mouse.dblclick(at['cx'], at['cy'])
        self.idle(500)
        return True

    def shot(self, name):
        try:
            os.makedirs(SHOTS, exist_ok=True)
            self.pg.screenshot(path=os.path.join(SHOTS, '%s_%s_%s.png' % (self.tag, self.dev, name)))
        except Exception:
            pass

    def close(self):
        try:
            ERRS.setdefault(self.tag, []).extend(list(self.ev("()=>__PZ.errs()") or []) + self.errs)
        except Exception:
            pass
        try:
            self.ctx.close()
        except Exception:
            pass


def pair(br, eng, dev, sn, sb):
    return P(br, eng, 'NEW', sn, dev), (P(br, eng, 'BASE', sb, dev) if sb else None)


def both(a, b, fn):
    return fn(a), (fn(b) if b else None)


def ok1(v):
    return v is not None and v.get('gap') is not None and abs(v['gap']) <= 1


def gx(v):
    return None if not v else {k: v.get(k) for k in ('gap', 'mt', 'h', 'y', 'sized', 'st', 'sh', 'ch')}


def eqv(a, b, keys=('gap', 'mt', 'h')):
    return bool(a) and bool(b) and all((abs(a[k] - b[k]) <= 1 if isinstance(a.get(k), (int, float)) and isinstance(b.get(k), (int, float)) else a.get(k) == b.get(k)) for k in keys)


def open_mok(p, law='민사소송법'):
    p.ev("o=>__PZ.go(o)", {'law': law, 'tab': 'cha2', 'boardKind': '기출'})
    return p.tap(p.ev("()=>__PZ.mokBtn()"), 900)


def open_chip(p, note=NOTE, k='기출', where='center'):
    """목록 창(없으면 연다)에서 그 줄을 굴리고 칩 톡 → 칩 창(열쇠 · 값)"""
    if not p.ev("()=>__PZ.hasList()"):
        p.tap(p.ev("()=>__PZ.mokBtn()"), 900)
    at = p.ev("([n,k,w])=>__PZ.mokRow(n,k,w)", [note, k, where])
    if not at or not at.get('on'):
        return None, at
    p.tap(at, 700)
    return at.get('key'), p.ev("([k,ms])=>__PZ.waitWin(k,ms)", [at.get('key'), 5000])


def B1_3_6_7_2(br, eng, sn, sb):
    """아이패드 세로 한 쪽에서 차례로 — B1(늘림) → B3(다시 열기) → B6(모서리에서 −100) → B7(더블클릭) → B2(글 긴 창)"""
    s = sfx(eng)
    a, b = pair(br, eng, 'padP', sn, sb)
    try:
        both(a, b, open_mok)
        o = both(a, b, lambda p: open_chip(p)[1])
        if not (o[0] and o[0].get('grip')):
            T('B1' + s, '칩 창 열림', False, o[0])
            return
        cw = lambda p: p.ev("k=>__PZ.win(k)", CHIP)
        # B1 — 떼지 않고 +150 · +300(끄는 도중 · ResizeObserver 를 안 기다리는 pointermove 의 prszPin)
        h1 = both(a, b, lambda p: p.hold(cw(p)['grip'], [(0, 150), (0, 300)], lambda: cw(p)))
        vn = {'열자마자': gx(o[0]), '+150': gx(h1[0][0][0]), '+300': gx(h1[0][0][1]), '뗀 뒤': gx(h1[0][1])}
        vb = {'열자마자': gx(o[1]), '+150': gx(h1[1][0][0]), '+300': gx(h1[1][0][1]), '뗀 뒤': gx(h1[1][1])} if b else None
        N('B1' + s, '아이패드 세로 820×1180 · 4.2.2. 「기출」 칩 창 처음(%s)' % a.how, {'new': vn['열자마자'], 'base': vb and vb['열자마자']})
        TB('B1' + s, '글 짧은 칩 창 손잡이 터치 — 끄는 도중 +150 · +300 · 뗀 뒤 gap 0(바탕 = 늘린 만큼) · 높이 = 처음 + 300(popsize 식 무변)',
           lambda v: ok1(v['+150']) and ok1(v['+300']) and ok1(v['뗀 뒤']) and abs(v['뗀 뒤']['h'] - v['열자마자']['h'] - 300) <= 1, vn, vb)
        hb = h1[0][1] and h1[0][1]['h']
        a.shot('B1'); b and b.shot('B1')
        # B3 — ✕ 닫고 같은 칩 다시 → 기억 크기
        def reopen(p):
            p.tap(p.ev("k=>__PZ.closeKey(k)", CHIP), 500)
            gone = p.ev("k=>__PZ.win(k)", CHIP) is None
            return gone, open_chip(p)[1]
        r3 = both(a, b, reopen)
        vn3 = {'닫힘': r3[0][0], '다시': gx(r3[0][1]), '기억': a.ev("k=>__PZ.cfg(k)", 'list')}
        vb3 = {'닫힘': r3[1][0], '다시': gx(r3[1][1]), '기억': b.ev("k=>__PZ.cfg(k)", 'list')} if b else None
        TB('B3' + s, '✕ 닫고 같은 칩 다시 → 기억 크기(높이 = 늘린 높이) · gap 0(바탕 = 300)',
           lambda v: v['닫힘'] and ok1(v['다시']) and v['기억'] and abs(v['다시']['h'] - v['기억']['h']) <= 1, vn3, vb3)
        a.shot('B3'); b and b.shot('B3')
        # B6 — 모서리 손잡이를 잡아 −100
        g6 = both(a, b, lambda p: cw(p))
        d6 = both(a, b, lambda p: p.hold(cw(p)['grip'], [(0, -100)], lambda: cw(p))[1])
        f6 = lambda h0: max(min(240, h0), h0 - 100)
        vn6 = {'잡을 때': gx(g6[0]), '잡힘': (g6[0] or {}).get('grip', {}).get('on'), '−100': gx(d6[0])}
        vb6 = {'잡을 때': gx(g6[1]), '잡힘': (g6[1] or {}).get('grip', {}).get('on'), '−100': gx(d6[1])} if b else None
        TB('B6' + s, '모서리 손잡이를 잡아 −100 → 첫 누름이 .prsz · 높이 = max(min(240, 잡을 때), 잡을 때 − 100) · gap 0',
           lambda v: v['잡힘'] and v['잡을 때'] and v['−100'] and abs(v['−100']['h'] - f6(v['잡을 때']['h'])) <= 1 and ok1(v['−100']), vn6, vb6)
        # B7 — 머리 더블클릭 = 기억 지움 → 기본 크기
        d7 = both(a, b, lambda p: (p.dbl(cw(p)['head']), cw(p), p.ev("k=>__PZ.cfg(k)", 'list'))[1:])
        vn7 = {'창': gx(d7[0][0]), '기억': d7[0][1]}
        vb7 = {'창': gx(d7[1][0]), '기억': d7[1][1]} if b else None
        TB('B7' + s, '머리 더블클릭(기억 지움) → 기본 크기(sized 풀림 · 기억 없음) · gap 0', lambda v: v['창'] and not v['창']['sized'] and v['기억'] is None and ok1(v['창']), vn7, vb7, yard=False)
        if vb7:
            T('B7' + s, '바탕과 같은 값(gap · margin-top · 높이)', eqv(vn7['창'], vb7['창']), {'new': vn7['창'], 'base': vb7['창']})
        # B2 — 글 긴 칩 창(칩 수 가장 많은 것) — 굴리기 전 · 끝까지 굴린 뒤
        def longw(p):
            at = p.ev("([n,k,w])=>__PZ.mokRow(n,k,w)", [None, None, 'center'])
            p.tap(at, 700)
            w0 = p.ev("([k,ms])=>__PZ.waitWin(k,ms)", [at.get('key'), 5000])
            w1 = p.ev("k=>__PZ.scrollEnd(k)", at.get('key'))
            return {'칩': at.get('t'), '줄': at.get('note'), '굴리기 전': gx(w0), '끝까지': gx(w1)}
        l2 = both(a, b, longw)
        TB('B2' + s, '글 긴 칩 창(%s · %s) — 굴리기 전 · 끝까지 굴린 뒤 gap 0 · margin-top −16px(sticky 그대로)' % ((l2[0] or {}).get('칩'), ((l2[0] or {}).get('줄') or '')[:16]),
           lambda v: ok1(v['굴리기 전']) and ok1(v['끝까지']) and v['끝까지']['st'] > 0 and v['굴리기 전']['mt'] == '-16px' and v['끝까지']['mt'] == '-16px', l2[0], l2[1], yard=False)
        if l2[1]:
            T('B2' + s, '바탕과 같은 값(gap · margin-top · 높이 · 굴린 자리)', eqv(l2[0]['굴리기 전'], l2[1]['굴리기 전']) and eqv(l2[0]['끝까지'], l2[1]['끝까지'], ('gap', 'mt', 'h', 'st')), {'new': l2[0], 'base': l2[1]})
        a.shot('B2'); b and b.shot('B2')
    finally:
        a.close(); b and b.close()


def B5(br, eng, sn, sb):
    s = sfx(eng)
    g = 'B5' + s
    a, b = pair(br, eng, 'padP', sn, sb)
    try:
        both(a, b, open_mok)
        nw = lambda p: p.ev("k=>__PZ.win(k)", NOTEK)

        def opennote(p):
            at = p.ev("([n,k,w])=>__PZ.mokRow(n,k,w)", [NOTE, None, 'center'])
            p.tap(at, 800)
            return p.ev("([k,ms])=>__PZ.waitWin(k,ms)", [NOTEK, 5000])
        n0 = both(a, b, opennote)

        def foldall(p):
            for i in range(8):
                ts = p.ev("k=>__PZ.togs(k)", NOTEK) or []
                j = next((x for x, t in enumerate(ts) if t == '˅'), None)
                if j is None:
                    break
                p.tap(p.ev("([k,i])=>__PZ.tog(k,i)", [NOTEK, j]), 400)
            return p.ev("k=>__PZ.togs(k)", NOTEK), nw(p)
        f0 = both(a, b, foldall)
        g1 = both(a, b, lambda p: p.hold(nw(p)['grip'], [(0, 200)], lambda: nw(p))[1])

        def unfold(p):
            p.tap(p.ev("([k,i])=>__PZ.tog(k,i)", [NOTEK, 0]), 600)
            return nw(p)
        u = both(a, b, unfold)

        def refold(p):
            p.ev("k=>{const p=POPS.find(x=>x._pk===k);if(p)p.scrollTop=0;return 1;}", NOTEK)
            p.tap(p.ev("([k,i])=>__PZ.tog(k,i)", [NOTEK, 0]), 600)
            return nw(p)
        r = both(a, b, refold)
        vn = {'처음': gx(n0[0]), '다 접음': [f0[0][0], gx(f0[0][1])], '+200(짧은 sized)': gx(g1[0]), '하나 폄': gx(u[0]), '다시 접음': gx(r[0])}
        vb = {'처음': gx(n0[1]), '다 접음': [f0[1][0], gx(f0[1][1])], '+200(짧은 sized)': gx(g1[1]), '하나 폄': gx(u[1]), '다시 접음': gx(r[1])} if b else None
        TB(g, '노트 창 4.2.2. — 헤딩 넷 다 접고 손잡이 +200(글보다 큰 창) → gap 0 · 하나 펴면 굴러감 margin-top −16px · 다시 접으면 gap 0(바탕 = 접은 뒤 gap > 0)',
           lambda v: ok1(v['+200(짧은 sized)']) and v['하나 폄']['sh'] > v['하나 폄']['ch'] and v['하나 폄']['mt'] == '-16px' and ok1(v['하나 폄']) and ok1(v['다시 접음']), vn, vb)
        a.shot('B5'); b and b.shot('B5')
    finally:
        a.close(); b and b.close()


def B4(br, eng, sn, sb):
    s = sfx(eng)
    g = 'B4' + s
    a, b = pair(br, eng, 'pc', sn, sb)
    try:
        def memo(p):
            p.ev("o=>__PZ.setPit(o)", PIT)
            p.ev("o=>__PZ.go(o)", {'law': '민사소송법', 'tab': 'cha2', 'boardKind': '기출', 'c2ord': 'unit', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}, 'c2mx': {}})
            p.tap(p.ev("c=>__PZ.title(c)", '24-61-2'), 900)
            p.ev("([s,ms])=>__PZ.waitSel(s,ms)", ['.pop.mpop', 4000])
            m0 = p.ev("([s,i])=>__PZ.sel(s,i)", ['.pop.mpop', 0])   # 첫 메모 창(끌기 뒤에도 같은 창을 잰다)
            m1 = None
            if m0 and m0.get('grip'):
                p.drag(m0['grip'], 40, 60)
                m1 = p.ev("([s,i])=>__PZ.sel(s,i)", ['.pop.mpop', 0])
            return {'안 sized': m0 and {k: m0.get(k) for k in ('gap', 'mt', 'h', 'w')}, 'sized(+40 · +60)': m1 and {k: m1.get(k) for k in ('gap', 'mt', 'h', 'w')}}
        mm = both(a, b, memo)
        okm = lambda v: v['안 sized'] and v['sized(+40 · +60)'] and all(v[k]['gap'] is not None and -0.5 <= v[k]['gap'] <= 1.5 for k in ('안 sized', 'sized(+40 · +60)'))
        T(g, '2차 보드 메모 창(.pop.mpop · 안 sized · sized) gap ≤ 1(설계 1px · 이 판 안 건드림)', okm(mm[0]), {'new': mm[0], 'base': mm[1]})
        if mm[1]:
            T(g, '메모 창 = 바탕과 같은 값', all(eqv(mm[0][k], mm[1][k], ('gap', 'mt', 'h', 'w')) for k in ('안 sized', 'sized(+40 · +60)')), {'new': mm[0], 'base': mm[1]})

        def side(p):
            p.ev("o=>__PZ.go(o)", {'law': '특허법', 'tab': 'jo', 'jo': '제140조', 'mkWin': False, 'ciWin': '', 'joPanel': False})
            out = {}
            p.tap(p.ev("()=>__PZ.mkBtn()"), 900)
            out['✎ 마크업(높이 줌)'] = gx(p.ev("([s,ms])=>__PZ.waitSel(s,ms)", ['.pop.wm-mk', 4000]))
            p.tap(p.ev("c=>__PZ.chip(c)", 'wmin'), 900)
            w = p.ev("([s,ms])=>__PZ.waitSel(s,ms)", ['.pop.wm-ci', 4000])
            out['🔗인(높이 없음)'] = dict(gx(w) or {}, foot=p.ev("s=>__PZ.foot(s)", '.pop.wm-ci'))
            p.tap(p.ev("c=>__PZ.chip(c)", 'wmpi'), 900)
            w = p.ev("([s,ms])=>__PZ.waitSel(s,ms)", ['.pop.wm-ci', 4000])
            out['↩피(발 줄)'] = dict(gx(w) or {}, foot=p.ev("s=>__PZ.foot(s)", '.pop.wm-ci'))
            return out
        sd = both(a, b, side)
        T(g, '원문 옆 창(wmWin · flex) — ✎ 마크업(높이 줌) · 🔗인(높이 없음) · ↩피(발 줄 wmWinFoot 넣은 뒤) gap 0', all(ok1(v) for v in sd[0].values()) and sd[0]['↩피(발 줄)'].get('foot') is True, {'new': sd[0], 'base': sd[1]})
        if sd[1]:
            T(g, '옆 창 = 바탕과 같은 값', all(eqv(sd[0][k], sd[1][k]) for k in sd[0]), {'new': sd[0], 'base': sd[1]})
        a.shot('B4'); b and b.shot('B4')
    finally:
        a.close(); b and b.close()


def B8(br, eng, sn, sb):
    s = sfx(eng)
    g = 'B8' + s
    a, b = pair(br, eng, 'phone', sn, sb)
    try:
        both(a, b, open_mok)
        o = both(a, b, lambda p: open_chip(p)[1])
        if not (o[0] and o[0].get('grip')):
            T(g, '폰 칩 창 열림', False, o[0])
            return
        cw = lambda p: p.ev("k=>__PZ.win(k)", CHIP)
        d = both(a, b, lambda p: p.hold(cw(p)['grip'], [(0, 300)], lambda: cw(p))[1])

        def reopen(p):
            p.tap(p.ev("k=>__PZ.closeKey(k)", CHIP), 500)
            return open_chip(p)[1]
        r = both(a, b, reopen)
        vn = {'열자마자': gx(o[0]), '+300': gx(d[0]), '다시 열기': gx(r[0])}
        vb = {'열자마자': gx(o[1]), '+300': gx(d[1]), '다시 열기': gx(r[1])} if b else None
        TB(g, '폰 390×844 · 목차노트 칩 창 열자마자 gap 0(바탕 = 아래 70%% 칸 − 글) · 손잡이 +300 · 다시 열기 gap 0', lambda v: ok1(v['열자마자']) and ok1(v['+300']) and ok1(v['다시 열기']), vn, vb)
        a.shot('B8'); b and b.shot('B8')
    finally:
        a.close(); b and b.close()


def B9(br, eng, sn):
    g = '훑기' + sfx(eng)
    for dev in ('pc', 'pc12', 'pad834', 'phone'):
        p = P(br, eng, 'NEW', sn, dev)
        try:
            open_mok(p)
            k, w0 = open_chip(p)
            cw = lambda q: q.ev("k=>__PZ.win(k)", CHIP)
            dy = 200 if dev == 'phone' else 300
            w1 = p.hold(w0['grip'], [(0, dy)], lambda: cw(p))[1] if w0 and w0.get('grip') else None
            p.tap(p.ev("k=>__PZ.closeKey(k)", CHIP), 500)
            w2 = open_chip(p)[1]
            w3 = None
            if w2 and w2.get('head'):
                p.hold(w2['head'], [(-40, -120)], lambda: None)
                w3 = cw(p)
            ov = p.ev("()=>__PZ.overflow()")
            p.shot('sweep')
            vals = {'처음': gx(w0), '+%d' % dy: gx(w1), '다시 열기': gx(w2), '머리 끌기 뒤': gx(w3) and dict(gx(w3), x=w3['x']), 'docW': ov['docW']}
            ok = all(ok1(x) for x in (w0, w1, w2, w3)) and ov['docW'][0] <= ov['docW'][1] and w3 and w2 and (abs(w3['y'] - w2['y']) > 1 or abs(w3['x'] - w2['x']) > 1)
            T(g, '%s %d×%d — 칩 창 처음 · +%d · 다시 열기 · 머리 끌기로 옮긴 뒤 gap 0 · 가로 넘침 0' % (dev, DEV[dev]['W'], DEV[dev]['H'], dy), ok, vals)
        finally:
            p.close()


def main():
    src_new = app_src(NEW)
    src_base = app_src(BASE)
    if not src_new:
        raise SystemExit('앱을 못 읽었다: ' + NEW)
    print('NEW  = %s · md5(LF) %s · %d B(LF)' % (NEW, md5lf(src_new), len(src_new.replace('\r\n', '\n').encode('utf-8'))))
    print('BASE = %s · %s' % (BASE, ('md5(LF) ' + md5lf(src_base)) if src_base else '못 읽음(안 잼 — 헛잣대·맞대기 없이)'))
    os.makedirs(TMPD, exist_ok=True)
    phase = {}
    with sync_playwright() as pw:
        for eng in ENGS:
            try:
                br = getattr(pw, eng).launch()
            except Exception as e:
                N('엔진', '%s 안 잼(이 기계에 없음)' % eng, str(e).splitlines()[0][:160])
                continue
            try:
                groups = [('B1', lambda: B1_3_6_7_2(br, eng, src_new, src_base)), ('B5', lambda: B5(br, eng, src_new, src_base)),
                          ('B4', lambda: B4(br, eng, src_new, src_base)), ('B8', lambda: B8(br, eng, src_new, src_base)), ('B9', lambda: B9(br, eng, src_new))]
                for k, fn in groups:
                    if not (want(k) or (k == 'B1' and any(want(x) for x in ('B2', 'B3', 'B6', 'B7')))):
                        continue
                    t1 = time.time()
                    try:
                        fn()
                    except Exception as e:
                        T(k + sfx(eng), '실행 오류', False, '%s: %s' % (type(e).__name__, str(e)[:300]))
                        traceback.print_exc()
                    phase[('B1·B3·B6·B7·B2' if k == 'B1' else k) + sfx(eng)] = round(time.time() - t1, 1)
            finally:
                br.close()
    en = [e for e in ERRS.get('NEW', []) if 'Failed to load resource' not in e]
    T('B0', '새 판 페이지 오류 0(pageerror · window error — ResizeObserver 고리 오류 포함)', not en, en[:5])
    if 'BASE' in ERRS:
        N('B0', '바탕 페이지 오류(값만)', [e for e in ERRS['BASE'] if 'Failed to load resource' not in e][:5])
    by = {}
    for gg, nm, okb in YARD:
        by.setdefault(gg, []).append(okb)
    for gg in sorted(by):
        oks = by[gg]
        T('헛잣대', gg, not all(oks), '바탕 FAIL %d / %d' % (oks.count(False), len(oks)))
    ok = [r for r in RES if r[2] is True]
    bad = [r for r in RES if r[2] is False]
    lines = ['_harness_jo_prsz_pin — PASS %d · FAIL %d · %s초' % (len(ok), len(bad), round(time.time() - T0, 1)),
             'NEW md5(LF) ' + md5lf(src_new) + ' · BASE ' + BASE, '단계별 초 ' + json.dumps(phase, ensure_ascii=False)]
    for g_, nm, o, d in RES:
        lines.append('%s | %s · %s | %s' % ('INFO' if o is None else ('PASS' if o else 'FAIL'), g_, nm, d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str)[:900]))
    os.makedirs(os.path.dirname(OUTF), exist_ok=True)
    io.open(OUTF, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines[:3]))
    print('결과 → ' + OUTF)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
