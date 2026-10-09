# -*- coding: utf-8 -*-
r"""_task_jo_2cha_minso_board_fix1 §B 관문 — 2차 보드 본문 안 조문 링크 줄바꿈(폰 GS 보드 가로 넘침 고침)

  python _harness_jo_2cha_minso_board_fix1.py [--new <앱 파일 | genie git 판>] [--base <판 = f4c91af>] [--only B1,B2,..] [--eng chromium[,webkit]] [--res <결과 파일>] [--shots <화면 폴더>]

  NEW  = genie 작업트리 jo/index.html(고친 판) · BASE = 바탕(cloud/jo_2cha_minso_board 끝 f4c91af) — 헛잣대(B1 바탕 FAIL) · B3·B4 무변 맞대기
         바탕을 못 읽으면 바탕 칸은 「안 잼」
  데이터 = genie jo/data(실물 · 읽기만) · 기록 = 없음(쪽마다 localStorage 비움 · tt.cfg person 만 · 토큰 없음) · 밖 주소 404
  기기 = 폰 390×844 · 아이패드 834×1194(터치 · DSF 2 · 손가락 = Chromium CDP Input.dispatchTouchEvent · WebKit 은 touchscreen.tap) · PC 1440×900 · 900×900(마우스)
  관문:
    B1 폰 · 민소 → 2차 → GS → 회차별 · 단계 「펴기」(all) → .main scrollWidth ≤ clientWidth · 넘친 요소 0(넘치면 요소 · 글 앞 40자 · 폭)
    B2 훑기 — 기출 · GS(회차별 all · 단원별 all) · 사례 × 1440 · 900 · 834 · 390 — .main 가로 넘침 0 · 그림
    B3 보드 본문 링크 — 살아 있는 .joLink 누름 → 이어지는 창(조문 창) = 바탕과 같음 · .dead 누름 = 무반응(창 0 · 탭 그대로) = 바탕과 같음 · 둘 다 줄바꿈 꼴(white-space normal)
    B4 다른 화면 무변 표본 — 카드 창(코드 숫자 → .pop.k-cell) 안 .joLink 계산 white-space = nowrap(바탕과 같음)
  결과 = 화면 PASS/FAIL 줄 · --res 파일(기본 = 임시 폴더 · _qa 에 결과를 쓰지 않는다)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402 — _task_qa_fix1 A-4(2026-10-09) 실행 모드 --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같다) · import 때 sys.argv 에서 --mode · --snap-in · --snap-out 을 뗀다(아래 ARG 보다 먼저) · 새 갈래는 모두 QJ.GATE / QJ.REGRESS / QJ.SMOKE 안
# ── 모드(_task_qa_fix1 A-4 · 꼴 = 10/4 _task_qa_slim · 이 판의 앞 하네스 _harness_jo_2cha_minso_board.py 와 같은 꼴) ──
#   gate(인자 없음) = 이 판 앞과 같음 — 바탕 f4c91af 를 git show 로 풀어 새 판과 같은 차례로 띄움(헛잣대 · 「바탕과 같음」 칸)
#   regress = 새 판만 띄움(바탕 git show 0 · 바탕 쪽 띄움 0 · 그림 안 찍음) · 헛잣대 안 돎 · 「바탕과 같음」 칸 셋(B1 그 링크 꼴 · B3 · B4)은 기준 스냅샷
#             (QJ.base — 실행기가 --snap-in 으로 준 앞 인도판 새 판 값 · 없으면 첫 기록) · 나머지 칸은 새 판 조건 그대로(B2 훑기 · 두 엔진 그대로)
#   smoke   = regress 가운데 Chromium · B1 만 — 폰 390 민소 2차 GS 회차별 「펴기」 → .main 가로 넘침 0 · 그 링크 줄바꿈 꼴 · 그 링크 꼴 = 기준(쪽 한 번)
#   셈(§B-4) = P() 마다 QJ.launch('new'|'base') · 바탕 풀기 QJ.sub('git:show-app') — regress · smoke 에서 base · git:show-app = 0
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
BASE = ARG('--base', 'f4c91af')   # cloud/jo_2cha_minso_board 끝 = 이 판의 바탕
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
if QJ.SMOKE:   # smoke(_task_qa_fix1 A-4) — Chromium 만 · 칸 = B1 셋(폰 390 · 민소 2차 GS 회차별 「펴기」 → .main 가로 넘침 0 · 그 링크 줄바꿈 꼴 · 그 링크 꼴 = 기준) — 이 판(fix1)이 고친 바로 그 화면 · 쪽 한 번
    ONLY = ['B1']
    ENGS = [x for x in ENGS if x == 'chromium']
TMPD = os.path.join(tempfile.gettempdir(), 'h_jo_c2fix1')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_jo_2cha_minso_board_fix1_result.txt'))
SHOTS = ARG('--shots', os.path.join(TMPD, 'shots'))
DATA = _roots.genie('jo', 'data')
LONG = '사례 3-17-3-민기출-법인공시송달위법유효,추완상소O,재심3호O'   # §0 넘친 링크(.joLink.dead · 폭 321)
SYN_CARD = '민기초-25-4회-2-'                                         # 그 링크가 든 GS 카드
IPAD_UA = 'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
IPHONE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
DEV = {'pc': dict(W=1440, H=900, touch=False), 'pc900': dict(W=900, H=900, touch=False),
       'pad': dict(W=834, H=1194, touch=True, ua=IPAD_UA), 'phone': dict(W=390, H=844, touch=True, ua=IPHONE_UA)}

RES = []    # (묶음, 이름, 새 판 판정 True/False/None(INFO), 값)
YARD = []   # (묶음, 이름, 바탕 판정)
T0 = time.time()


def T(g, name, ok, detail=''):
    RES.append((g, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', g, name, detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)[:700]), flush=True)


def N(g, name, detail=''):
    RES.append((g, name, None, detail))
    print('INFO | %s · %s | %s' % (g, name, detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)[:700]), flush=True)


def TB(g, name, ok_fn, vn, vb):
    """새 판 판정 + 같은 잣대로 바탕 판정(헛잣대 재료) — 바탕 값이 없으면 새 판만"""
    try:
        okn = bool(ok_fn(vn))
    except Exception:
        okn = False
    T(g, name, okn, {'new': vn, 'base': vb})
    if vb is not None:
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

# 페이지 도구(__FX) — 재는 것 = DOM 실물(scrollWidth · clientWidth · getBoundingClientRect · 계산 스타일 · POPS · S) · 누름은 파이썬이 진짜 손가락·마우스로
TOOLS = r"""
(function(){
const W = ms => new Promise(r => setTimeout(r, ms));
const busyNow = () => { try { return !!busy; } catch (e) { return false; } };
const idle = async () => { for (let i = 0; i < 1200; i++){ if (!busyNow()) return true; await W(25); } return false; };
const live = () => { try { return POPS.filter(p => p.isConnected); } catch (e) { return []; } };
const vis = e => !!e && e.isConnected && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden';
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const hit = e => { if (!e) return null; const r = e.getBoundingClientRect(); const cx = r.left + Math.min(r.width / 2, 30), cy = r.top + Math.min(r.height / 2, 9); const a = document.elementFromPoint(cx, cy);
  return { cx: +cx.toFixed(1), cy: +cy.toFixed(1), w: +r.width.toFixed(1), on: !!a && (a === e || e.contains(a)) && cy > 0 && cy < innerHeight && cx > 0 && cx < innerWidth }; };
const main = () => document.querySelector('#slot .main');
window.__FX = {
  idle,
  errs: () => (window.__ERR || []).slice(),
  async go(o){ await idle(); try { closeAllPops(true); } catch (e) {} Object.assign(S, { law: '민사소송법', tab: 'cha2', series: '', yearFilter: '', cha2Sel: null, cha2Filter: {} }, o || {}); await render(); await idle(); await W(700); await idle(); return this.state(); },
  state(){ const m = main(); return { kind: S.boardKind, ord: (typeof c2Ord === 'function') ? c2Ord() : null, lv: JSON.parse(JSON.stringify(S.c2lv || null)), lvBtn: txt(document.querySelector('#slot .uzstep.c2lv')),
    bodies: document.querySelectorAll('#slot .c2bw').length, rows: document.querySelectorAll('#slot .c2row').length, cells: document.querySelectorAll('#slot .c2cell, #slot .cell').length, main: m ? [m.scrollWidth, m.clientWidth] : null }; },
  lvBtn(){ const b = document.querySelector('#slot .uzstep.c2lv'); if (!b || !vis(b)) return null; try { b.scrollIntoView({ block: 'nearest' }); } catch (e) {} return Object.assign(hit(b), { t: txt(b) }); },
  /* .main 가로 넘침 — 넘친 요소(안쪽 오른쪽 끝 너머) 중 가장 안쪽 것들(글 앞 40자 · 폭) */
  over(){ const m = main(); if (!m) return null; const mr = m.getBoundingClientRect(), lim = mr.left + m.clientWidth + 0.5; const out = [];
    const sl = m.scrollLeft; m.scrollLeft = 0;
    m.querySelectorAll('*').forEach(e => { if (out.length >= 12) return; const r = e.getBoundingClientRect(); if (!r.width || r.right <= lim) return;
      if ([...e.children].some(c => c.getBoundingClientRect().right > lim)) return;   /* 가장 안쪽만 */
      out.push({ el: e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).join('.') : ''), t: txt(e).slice(0, 40), w: +r.width.toFixed(1), right: +r.right.toFixed(1), inBw: !!e.closest('.c2bw') }); });
    m.scrollLeft = sl;
    return { sw: m.scrollWidth, cw: m.clientWidth, n: out.length, els: out }; },
  linkLong(t){ const L = [...document.querySelectorAll('#slot .c2bw .joLink')].filter(e => txt(e) === t); const e = L[0]; if (!e) return null; const cs = getComputedStyle(e), r = e.getClientRects();
    return { n: L.length, dead: e.classList.contains('dead'), ws: cs.whiteSpace, ow: cs.overflowWrap, lines: r.length, w: +e.getBoundingClientRect().width.toFixed(1), col: cs.color, bg: cs.backgroundColor, td: cs.textDecorationStyle, cur: cs.cursor }; },
  /* 보드 본문 링크 — 살아 있는 것(첫째) · .dead(첫째) — 두 판이 같은 데이터 · 같은 차례라 같은 링크 */
  link(dead){ const e = [...document.querySelectorAll('#slot .c2bw .joLink' + (dead ? '.dead' : ':not(.dead)'))].filter(vis)[0]; if (!e) return null;
    try { e.scrollIntoView({ block: 'center' }); } catch (x) {} const cs = getComputedStyle(e); return Object.assign(hit(e), { t: txt(e).slice(0, 40), ws: cs.whiteSpace, row: (e.closest('.c2row') || {}).dataset ? e.closest('.c2row').dataset.ck : null }); },
  pops(){ return live().map(p => ({ k: p._pk || null, t: txt(p.querySelector(':scope > .ph .pt')).slice(0, 60) })); },
  where(){ return { tab: S.tab, law: S.law, jo: S.jo || null, kind: S.boardKind }; },
  /* 카드 창 — 첫 .joLink 가 든 카드의 코드 숫자 자리 */
  codeOfLink(){ const e = [...document.querySelectorAll('#slot .c2bw .joLink')].filter(vis)[0]; const r = e && e.closest('.c2row'); const c = r && r.querySelector('.c2code'); if (!c) return null;
    try { c.scrollIntoView({ block: 'center' }); } catch (x) {} return Object.assign(hit(c), { ck: r.dataset.ck }); },
  cardLink(){ const p = live().filter(q => q.classList.contains('k-cell')).pop(); if (!p) return null; const e = p.querySelector('.joLink'); if (!e) return { card: true, link: null, t: txt(p.querySelector('.ph .pt')).slice(0, 60) };
    const cs = getComputedStyle(e); return { card: true, t: txt(p.querySelector('.ph .pt')).slice(0, 60), link: txt(e).slice(0, 40), ws: cs.whiteSpace, ow: cs.overflowWrap, inBw: !!e.closest('.c2bw') }; }
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


def syn_live(b):
    """B3 덧판 — 실물 2차 보드 본문의 .joLink 는 네 법 다 .dead 뿐이라(살아 있는 것 0) 그 카드(민기초-25-4회-2- · .dead 가 첫 줄)의 끝 줄 뒤에
    살아 있는 조문 링크 줄 하나를 더한다 — 꼴 = jo_민사소송법_본문.json 의 L 사건({k:'L', a, b, to:'민소-제…', j:'제…조'}) · 파일은 안 건드림(메모리 덧판)
    ⚠ .dead 줄 바로 뒤에 두면 크롬 모바일 손가락 자리 맞춤(누름 대상 보정)이 .dead 톡을 이웃 살아 있는 링크로 옮긴다 — 그래서 카드 끝(넉 줄 아래)"""
    j = json.loads(b.decode('utf-8'))
    rows = j[SYN_CARD]['행']
    lt = '민소-제259조(중복된 소제기의 금지)'
    rows.append({'t': lt + ' — 합성 링크(관문 B3)', 'i': 0, 'e': [{'k': 'L', 'a': 0, 'b': len(lt), 'to': lt, 'j': '제259조'}]})
    return json.dumps(j, ensure_ascii=False).encode('utf-8')


def serve(tag, src, over=None):
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
                if over and os.path.basename(f) in over and os.path.isfile(f):
                    return self._send(200, over[os.path.basename(f)](open(f, 'rb').read()))
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
    def __init__(self, br, eng, tag, src, dev, over=None):
        self.eng, self.tag, self.dev = eng, tag, dev
        QJ.launch('base' if tag.startswith('BASE') else 'new')   # 셈(§B-4) — 바탕 판 쪽(태그 BASE…)은 'base' · regress · smoke 에서는 0
        d = DEV[dev]
        self.touch = d['touch']
        port = serve(tag, src, over)
        kw = dict(viewport={'width': d['W'], 'height': d['H']})
        if d['touch']:
            kw.update(device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=d.get('ua'))
        self.ctx = br.new_context(**kw)
        self.ctx.route('**/*', lambda r: r.continue_() if r.request.url.startswith('http://127.0.0.1') else r.abort())
        self.pg = self.ctx.new_page()
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:300]))
        self.cdp = self.ctx.new_cdp_session(self.pg) if (eng == 'chromium' and d['touch']) else None
        self.pg.goto('http://127.0.0.1:%d/jo/index.html' % port, wait_until='load', timeout=120000)
        self.pg.wait_for_function("!!window.__FX&&typeof render==='function'&&typeof popCard4==='function'&&!!document.querySelector('#slot')", timeout=120000)
        self.pg.wait_for_timeout(1200)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def idle(self, ms=300):
        self.pg.wait_for_timeout(ms)
        self.ev("()=>__FX.idle()")

    def tap(self, at, wait=700):
        """한 번 누름 — 터치 기기 = 손가락(CDP 또는 touchscreen) · PC = 마우스"""
        if not at or not at.get('on'):
            return False
        self.pg.wait_for_timeout(150)
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

    def shot(self, name):
        if QJ.REGRESS:   # regress · smoke — 그림 안 찍음(눈으로 보는 용 · 판정 아님 · 시간)
            return
        try:
            os.makedirs(SHOTS, exist_ok=True)
            self.pg.screenshot(path=os.path.join(SHOTS, '%s_%s_%s.png' % (self.tag, self.dev, name)))
        except Exception:
            pass

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


def gs_all(p):
    """민소 → 2차 → GS → 회차별(단계 기본 2) → 「펴기」 단추를 진짜로 누름 → all"""
    s0 = p.ev("o=>__FX.go(o)", {'boardKind': 'GS', 'c2ord': 'round', 'c2lv': {'unit': 3, 'round': 2}, 'c2sec': {}, 'c2rl': {}})
    b = p.ev("()=>__FX.lvBtn()")
    p.tap(b, 1500)
    p.idle(800)
    return s0, b, p.ev("()=>__FX.state()")


def B1(br, eng, sn, sb):
    g = 'B1' + sfx(eng)
    vals = {}
    for tag, src in (('NEW', sn), ('BASE', sb)):
        if not src:
            continue
        p = P(br, eng, tag, src, 'phone')
        try:
            s0, b, s1 = gs_all(p)
            ov = p.ev("()=>__FX.over()")
            lk = p.ev("t=>__FX.linkLong(t)", LONG)
            if tag == 'NEW':
                N(g, '실물 2차 GS 본문 .joLink 셈(폰 · all) — 살아 있는 것 · .dead(살아 있는 링크 누름은 B3 합성 덧판으로)', p.ev("()=>({live:document.querySelectorAll('#slot .c2bw .joLink:not(.dead)').length,dead:document.querySelectorAll('#slot .c2bw .joLink.dead').length})"))
            vals[tag] = {'단추': b and b.get('t'), 'lv': s1['lv'], 'bodies': s1['bodies'], 'main': [ov['sw'], ov['cw']], 'n': ov['n'], 'els': ov['els'][:4], 'long': lk}
            p.shot('B1')
        finally:
            p.close()
    vn, vb = vals.get('NEW'), vals.get('BASE')
    TB(g, '폰 390×844 · 민소 2차 GS · 회차별 · 「펴기」 누름 → all(본문 다 펴짐) · .main scrollWidth ≤ clientWidth · 넘친 요소 0(바탕 f4c91af = 「사례 3-17-3-…」 .joLink.dead 넘침)',
       lambda v: v['lv'] and v['lv'].get('round') == 'all' and v['bodies'] > 0 and v['main'][0] <= v['main'][1] and v['n'] == 0, vn, vb)
    TB(g, '그 링크(「사례 3-17-3-민기출-…」 .dead) = 보드 본문 안 · white-space normal · overflow-wrap anywhere · 여러 줄 · 꼴(색·바탕·점선 밑줄·누름 없음) 그대로',
       lambda v: v['long'] and v['long']['dead'] and v['long']['ws'] == 'normal' and v['long']['ow'] == 'anywhere' and v['long']['lines'] >= 2, vn, vb)
    if vn and vb and vn.get('long') and vb.get('long'):
        a, b = vn['long'], vb['long']
        T(g, '그 링크 꼴 = 바탕(색 · 바탕색 · 밑줄 꼴 · 커서) — 줄바꿈만 다름', all(a[k] == b[k] for k in ('col', 'bg', 'td', 'cur')), {'new': a, 'base': b})
    if QJ.REGRESS and vn and vn.get('long'):   # 기준 칸(regress · smoke) — 바탕(f4c91af) 대신 기준 스냅샷(앞 인도판 새 판의 같은 링크 꼴 · 색 · 바탕색 · 밑줄 꼴 · 커서) · 새 판에 그 링크가 없으면 위 둘째 칸이 이미 FAIL
        a = {k: vn['long'][k] for k in ('col', 'bg', 'td', 'cur')}
        b = QJ.base('B1-꼴@' + eng, a)
        T(g, '그 링크 꼴 = 바탕(색 · 바탕색 · 밑줄 꼴 · 커서) — 줄바꿈만 다름', QJ.norm(a) == b, {'new': a, 'base': b, '기준': QJ.base_note('B1-꼴@' + eng)})


def B2(br, eng, sn):
    """훑기 — 기출 · GS(회차별 all · 단원별 all) · 사례 × 네 폭"""
    g = '훑기' + sfx(eng)
    states = [('기출 회차별 all', {'boardKind': '기출', 'c2ord': 'round', 'c2lv': {'unit': 'all', 'round': 'all'}}),
              ('기출 단원별 all', {'boardKind': '기출', 'c2ord': 'unit', 'c2lv': {'unit': 'all', 'round': 'all'}}),
              ('GS 회차별 all', {'boardKind': 'GS', 'c2ord': 'round', 'c2lv': {'unit': 'all', 'round': 'all'}}),
              ('GS 단원별 all', {'boardKind': 'GS', 'c2ord': 'unit', 'c2lv': {'unit': 'all', 'round': 'all'}}),
              ('사례', {'boardKind': '사례'})]
    for dev in ('pc', 'pc900', 'pad', 'phone'):
        p = P(br, eng, 'NEW', sn, dev)
        try:
            res = []
            for nm, o in states:
                s = p.ev("o=>__FX.go(o)", dict(o, c2sec={}, c2rl={}))
                ov = p.ev("()=>__FX.over()")
                res.append({'s': nm, 'bodies': s['bodies'], 'main': [ov['sw'], ov['cw']], 'n': ov['n'], 'els': ov['els'][:3]})
                if nm.startswith('GS 회차별'):
                    p.shot('sweep_gs')
            ok = all(r['main'][0] <= r['main'][1] and r['n'] == 0 for r in res) and all(r['bodies'] > 0 for r in res if r['s'] != '사례')
            T(g, '%s %d×%d — 기출·GS(회차별 all · 단원별 all · 본문 다 펴짐) · 사례 — .main 가로 넘침 0' % (dev, DEV[dev]['W'], DEV[dev]['H']), ok, res)
        finally:
            p.close()


def B3(br, eng, sn, sb):
    g = 'B3' + sfx(eng)
    vals = {}
    for tag, src in (('NEW', sn), ('BASE', sb)):
        if not src:
            continue
        p = P(br, eng, tag + '+합성', src, 'phone', {'2cha_본문_GS_민소.json': syn_live})
        try:
            gs_all(p)
            lv = p.ev("()=>__FX.link(false)")
            n0 = len(p.ev("()=>__FX.pops()"))
            p.tap(lv, 900)
            if QJ.REGRESS:   # regress · smoke — 이어지는 창을 앱 표지(POPS 에 새 창)로 기다림(최대 5 초) · gate 는 900ms 고정 그대로 — 10/8 gate · 10/9 jo4 regress 에서 WebKit 이 900ms 안에 창을 안 띄운 적 있음(open [] · 같은 칸 FAIL)
                QJ.until(p.pg, "n=>{try{return POPS.filter(x=>x.isConnected).length>n}catch(e){return false}}", 5000, 'B3 이어지는 창(POPS 새 창)', arg=n0)
            pl = p.ev("()=>__FX.pops()")
            w1 = p.ev("()=>__FX.where()")
            p.ev("()=>{try{closeAllPops(true);}catch(e){}return 1;}")
            p.idle(300)
            dd = p.ev("()=>__FX.link(true)")
            n1 = len(p.ev("()=>__FX.pops()"))
            p.tap(dd, 700)
            pd = p.ev("()=>__FX.pops()")
            w2 = p.ev("()=>__FX.where()")
            vals[tag] = {'live': lv and {k: lv.get(k) for k in ('t', 'ws', 'row', 'on')}, 'liveOpen': [x for x in pl][-1:] if len(pl) > n0 else [], 'w1': w1,
                         'dead': dd and {k: dd.get(k) for k in ('t', 'ws', 'row', 'on')}, 'deadPops': len(pd) - n1, 'w2': w2}
            p.shot('B3')
        finally:
            p.close()
    vn, vb = vals.get('NEW'), vals.get('BASE')
    T(g, '살아 있는 .joLink(합성 덧판 — 실물 본문엔 살아 있는 것 0) 누름 → 이어지는 창 하나(조문 창 민소 제259조) · 탭 그대로(2차) · 보드 본문 줄바꿈 꼴(white-space normal)',
      bool(vn) and vn['live'] and vn['live']['ws'] == 'normal' and len(vn['liveOpen']) == 1 and vn['w1']['tab'] == 'cha2', vn and {'live': vn['live'], 'open': vn['liveOpen'], 'where': vn['w1']})
    T(g, '.dead 누름 → 무반응(새 창 0 · 탭 그대로)', bool(vn) and vn['dead'] and vn['deadPops'] == 0 and vn['w2']['tab'] == 'cha2', vn and {'dead': vn['dead'], 'pops': vn['deadPops'], 'where': vn['w2']})
    if vb:
        N(g, '바탕(f4c91af + 같은 덧판) 값', vb)
    if vn and vb:
        T(g, '바탕과 같음 — 같은 링크(글 · 카드) · 이어지는 창 제목 · .dead 무반응',
          vn['live'] and vb['live'] and vn['live']['t'] == vb['live']['t'] and vn['live']['row'] == vb['live']['row'] and [x['t'] for x in vn['liveOpen']] == [x['t'] for x in vb['liveOpen']]
          and vn['dead']['t'] == vb['dead']['t'] and vn['deadPops'] == vb['deadPops'] == 0,
          {'new': [vn['live'] and vn['live']['t'], vn['liveOpen'], vn['dead'] and vn['dead']['t']], 'base': [vb['live'] and vb['live']['t'], vb['liveOpen'], vb['dead'] and vb['dead']['t']]})
    if QJ.REGRESS and vn:   # 기준 칸 — 바탕(f4c91af + 같은 덧판) 대신 기준 스냅샷(앞 인도판 새 판의 같은 링크 글 · 카드 · 이어지는 창 · .dead 글) · .dead 무반응(새 창 0)은 새 판 조건 그대로
        # 이어지는 창은 창 열쇠(_pk · 'jo|민사소송법|제259조')로 맞댄다 — 제목 글은 누른 뒤 900ms 에 「제259조 — 불러오는 중」 이 끼어 때에 따라 갈림(10/8 gate webkit B3 FAIL 둘 · 10/9 jo4 regress webkit 스냅샷이 「불러오는 중」 — 잼) · 제목은 값으로만
        a = [vn['live'] and vn['live']['t'], vn['live'] and vn['live']['row'], [x['k'] for x in vn['liveOpen']], vn['dead'] and vn['dead']['t']]
        b = QJ.base('B3@' + eng, a)
        T(g, '바탕과 같음 — 같은 링크(글 · 카드) · 이어지는 창 제목 · .dead 무반응', bool(vn['live']) and bool(vn['dead']) and QJ.norm(a) == b and vn['deadPops'] == 0,
          {'new': a, 'base': b, '창 제목(값만)': [x['t'] for x in vn['liveOpen']], '기준': QJ.base_note('B3@' + eng)})


def B4(br, eng, sn, sb):
    g = 'B4' + sfx(eng)
    vals = {}
    for tag, src in (('NEW', sn), ('BASE', sb)):
        if not src:
            continue
        p = P(br, eng, tag, src, 'phone')
        try:
            gs_all(p)
            c = p.ev("()=>__FX.codeOfLink()")
            p.tap(c, 1200)
            vals[tag] = dict(p.ev("()=>__FX.cardLink()") or {}, ck=c and c.get('ck'))
            p.shot('B4')
        finally:
            p.close()
    vn, vb = vals.get('NEW'), vals.get('BASE')
    T(g, '카드 창(코드 숫자 → .pop.k-cell) 안 .joLink 계산 white-space = nowrap(공용 규칙 그대로 · .c2bw 밖)',
      bool(vn) and vn.get('link') and vn.get('ws') == 'nowrap' and not vn.get('inBw'), vn)
    if vn and vb:
        T(g, '바탕과 같음(같은 카드 · 같은 링크 · white-space · overflow-wrap)', all(vn.get(k) == vb.get(k) for k in ('ck', 'link', 'ws', 'ow')), {'new': vn, 'base': vb})
    if QJ.REGRESS and vn:   # 기준 칸 — 바탕 대신 기준 스냅샷(앞 인도판 새 판의 같은 카드 · 같은 링크 · white-space · overflow-wrap)
        a = {k: vn.get(k) for k in ('ck', 'link', 'ws', 'ow')}
        b = QJ.base('B4@' + eng, a)
        T(g, '바탕과 같음(같은 카드 · 같은 링크 · white-space · overflow-wrap)', QJ.norm(a) == b, {'new': vn, 'base': b, '기준': QJ.base_note('B4@' + eng)})


def main():
    src_new = app_src(NEW)
    # 옛 줄: src_base = app_src(BASE)
    if QJ.GATE:
        QJ.sub('git:show-app')   # 셈 — 바탕 앱 풀기(regress · smoke 는 0)
    src_base = app_src(BASE) if QJ.GATE else None   # regress · smoke — 바탕(f4c91af)을 안 푼다(git show 0) → 바탕 쪽 띄움 0 · 헛잣대 없음 · 「바탕과 같음」 칸 = 기준 스냅샷
    if not src_new:
        raise SystemExit('앱을 못 읽었다: ' + NEW)
    print('NEW  = %s · md5(LF) %s · %d B(LF)' % (NEW, md5lf(src_new), len(src_new.replace('\r\n', '\n').encode('utf-8'))))
    # 옛 줄: print('BASE = %s · %s' % (BASE, ('md5(LF) ' + md5lf(src_base)) if src_base else '못 읽음(안 잼 — 헛잣대·맞대기 없이)'))
    if QJ.GATE:
        print('BASE = %s · %s' % (BASE, ('md5(LF) ' + md5lf(src_base)) if src_base else '못 읽음(안 잼 — 헛잣대·맞대기 없이)'))
    else:
        print('BASE = %s · 안 풂(%s — 헛잣대 없음 · 「바탕과 같음」 칸 = 기준 스냅샷)' % (BASE, QJ.MODE))
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
                for k, fn in (('B1', lambda: B1(br, eng, src_new, src_base)), ('B2', lambda: B2(br, eng, src_new)),
                              ('B3', lambda: B3(br, eng, src_new, src_base)), ('B4', lambda: B4(br, eng, src_new, src_base))):
                    if not want(k):
                        continue
                    t1 = time.time()
                    try:
                        fn()
                    except Exception as e:
                        T(k + sfx(eng), '실행 오류', False, '%s: %s' % (type(e).__name__, str(e)[:300]))
                        traceback.print_exc()
                    phase[k + sfx(eng)] = round(time.time() - t1, 1)
            finally:
                br.close()
    by = {}
    for gg, nm, okb in YARD:
        by.setdefault(gg, []).append(okb)
    for gg in sorted(by):
        oks = by[gg]
        T('헛잣대', gg, not all(oks), '바탕 FAIL %d / %d' % (oks.count(False), len(oks)))
    if QJ.REGRESS:   # regress · smoke — 바탕을 안 띄웠다(헛잣대는 gate 몫)
        N('헛잣대', '안 돎 — 바탕 %s 안 띄움(헛잣대는 gate 몫 · 「바탕과 같음」 칸 = 기준 스냅샷)' % BASE, QJ.MODE)
    ok = [r for r in RES if r[2] is True]
    bad = [r for r in RES if r[2] is False]
    lines = ['_harness_jo_2cha_minso_board_fix1 — PASS %d · FAIL %d · %s초' % (len(ok), len(bad), round(time.time() - T0, 1)),
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
