# -*- coding: utf-8 -*-
r"""_task_jo_popsize §B 관문 — 팝업 크기 손잡이: 세로는 손가락을 그대로 따라간다(화면 아래로 나가도 됨 · 240 으로 튀지 않음)

  python _harness_jo_popsize.py [--new <앱 파일 | genie git 판>] [--base <판 = f4c91af>] [--only B1,B2,..] [--eng chromium[,webkit]] [--res <결과 파일>] [--shots <화면 폴더>]

  NEW  = genie 작업트리 jo/index.html(고친 판) · BASE = 바탕(cloud/jo_2cha_minso_board 끝 f4c91af)
         두 판을 같은 기기·같은 차례로 늘 같이 돌린다 — 헛잣대(B1~B6 바탕 FAIL)와 B7(가로·옮기기 = 바탕과 같음)을 한 번에 센다 · 바탕을 못 읽으면 둘 다 「안 잼」
  데이터 = genie jo/data(실물 · 읽기만) · 기록 = 없음(쪽마다 localStorage 비움 · tt.cfg person 만 · 토큰 없음) · 밖 주소 404
  기기 = 아이패드 세로 820×1180 · 가로 1180×820 · 폰 390×844(터치 · DSF 2) · PC 1440×900(마우스)
  손가락 = Chromium CDP Input.dispatchTouchEvent(톡 · 끌기 — 화면 밖 자리까지 끌 수 있다)
         WebKit(로컬이 합칠 때 · B1 B2 B5 만) = 톡은 touchscreen.tap · 끌기는 신뢰 마우스(playwright WebKit 은 끌기 터치가 없다 — 도구 한계 · 결과에 적는다)
  관문:
    B1 아이패드 세로 · 민소 → 2차 → 목차노트 → 4.2.2. 당사자결석 「기출」 칩 창(위 1042 · 높이 130) 손잡이 +150 → 280 · −150 → 240 · 위 무변 · 아래 화면 밖
    B2 같은 창(새 쪽) 머리 위로 600 → 손잡이 +400 → 530 → 머리 아래로 500(아래 화면 밖) → 손잡이 +60 → 590 · 위 무변
    B3 목차노트 목록 창(인라인 max-height) 손잡이 +200 → 늘어남(아이패드 세로 · 가로)
    B4 PC 카드 창(popCard4 · 민소 2차 기출 24-61-2 코드) 손잡이 +300 · −200 · −600 → 마우스 그대로 · 240 아래로 안 줄음
    B5 폰 목차노트 → 노트 창 손잡이 +200 → 늘어남 · 화면 밖 · 기억 높이(popCfg.note) · 다시 열면(값)
    B6 원문 창(wmWin · 조문 ✎ 마크업 창 · 특허 제140조) 손잡이 +300(아래 화면 밖) → 그 높이(아이패드 가로 · PC)
    B7 가로·창 옮기기 무변 — B1~B6 의 폭 · left · 머리 끌기(좌우·위아래) · 손잡이 가로 끌기 결과 = 바탕
    ※ 10/4 잣대 고침(prsz_pin 뒤 꼴 · 근거 = _task_jo_prsz_pin 첫 줄 「손잡이가 창 오른쪽 아래 모서리에 선다」 · 사용자 10/4 02:34 「아래 부분과 핸들이 안 보이도록 해도 되니까」 ·
       결정로그 10/4 13:0x [채팅] 「하네스 잣대 고칠 것 = popsize 손잡이 화면 밖 칸(prsz_pin 뒤 꼴로)」 「다시 줄일 땐 머리를 위로 끌어 올린 뒤」):
       창 아래가 화면 밖이면 손잡이도 화면 밖이라 못 잡는다 → B1 −150 · B2 +60 · B2 손잡이 ←90 은 잡기 전에 lift(머리를 위로 끌어 창 아래 = 화면 − 40)
       · 새 판·바탕 같은 규칙(창 아래로 가름 — 바탕 sticky 손잡이는 화면 안이어도 같이 끌어 올려 B7 맞대기 자리를 맞춤) · 「위 무변」 = 끌어 올린 뒤 자리와 맞댐
    훑기 네 기기 — 가로 넘침 0 · 창 머리 화면 안(다시 잡힘) · 그림
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
BASE = ARG('--base', 'f4c91af')   # cloud/jo_2cha_minso_board 끝 = 이 판의 바탕
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
TMPD = os.path.join(tempfile.gettempdir(), 'h_jo_popsize')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_jo_popsize_result.txt'))
SHOTS = ARG('--shots', os.path.join(TMPD, 'shots'))
DATA = _roots.genie('jo', 'data')
NOTE = '4.2.2. 당사자결석(257조)(268조)(150③)(148조)'   # 민소 목차노트 — 아이패드 세로에서 목록 아래쪽 줄(§0)
CHIP = 'cell|🔗 기출 — ' + NOTE                          # popNoteList 창 열쇠(jo_mokchip_fix1 — 자르지 않음)
CODE = '24-61-2'                                         # B4 카드 창 — 민소 2차 기출
JO = ('특허법', '제140조')                                # B6 원문 창 — jo_wonmun 관문과 같은 조
IPAD_UA = 'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
IPHONE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
DEV = {'padP': dict(W=820, H=1180, touch=True, ua=IPAD_UA), 'padL': dict(W=1180, H=820, touch=True, ua=IPAD_UA),
       'pc': dict(W=1440, H=900, touch=False), 'phone': dict(W=390, H=844, touch=True, ua=IPHONE_UA)}

RES = []    # (묶음, 이름, 새 판 판정 True/False/None(INFO), 값)
YARD = []   # (묶음, 이름, 바탕 판정) — 같은 잣대를 바탕 값에 — 헛잣대
SAME = []   # (묶음, 자리, 새 판 값, 바탕 값) — B7 가로·옮기기 맞대기
T0 = time.time()


def T(g, name, ok, detail=''):
    RES.append((g, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', g, name, detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)[:700]), flush=True)


def N(g, name, detail=''):
    RES.append((g, name, None, detail))
    print('INFO | %s · %s | %s' % (g, name, detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)[:700]), flush=True)


def TB(g, name, ok_fn, vn, vb):
    """새 판 판정 + 같은 잣대로 바탕 판정(헛잣대 재료) — 바탕 값이 없으면(바탕 안 잼) 새 판만"""
    okn = False
    try:
        okn = bool(ok_fn(vn))
    except Exception:
        okn = False
    T(g, name, okn, {'new': vn, 'base': vb})
    if vb is not None:
        okb = False
        try:
            okb = bool(ok_fn(vb))
        except Exception:
            okb = False
        YARD.append((g, name, okb))


def same(g, where, vn, vb):
    if vb is not None:
        SAME.append((g, where, vn, vb))


def want(k):
    return not ONLY or k in ONLY


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
var Q=new URLSearchParams(location.search);
if(Q.get('keep')!=='1'){try{localStorage.clear();}catch(e){} try{localStorage.setItem('tt.cfg',JSON.stringify({person:'꼬까'}));}catch(e){}}
})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
</script>"""

# 페이지 도구(__PS) — 재는 것 = DOM 실물(getBoundingClientRect · 인라인 style · 계산 max-height · elementFromPoint · S.popCfg) · 누름·끌기는 파이썬이 진짜 손가락·마우스로
TOOLS = r"""
(function(){
const W = ms => new Promise(r => setTimeout(r, ms));
const busyNow = () => { try { return !!busy; } catch (e) { return false; } };
const idle = async () => { for (let i = 0; i < 600; i++){ if (!busyNow()) return true; await W(25); } return false; };
const live = () => { try { return POPS.filter(p => p.isConnected); } catch (e) { return []; } };
const byKey = k => live().find(p => p._pk === k) || null;
const vis = e => !!e && e.isConnected && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden';
const hit = e => { if (!e) return null; const r = e.getBoundingClientRect(); let cx = r.left + r.width / 2, cy = r.top + r.height / 2; const a = document.elementFromPoint(cx, cy);
  return { cx: +cx.toFixed(1), cy: +cy.toFixed(1), x: +r.left.toFixed(1), y: +r.top.toFixed(1), w: +r.width.toFixed(1), h: +r.height.toFixed(1),
    on: !!a && (a === e || e.contains(a)) && cy > 0 && cy < innerHeight && cx > 0 && cx < innerWidth }; };
function info(p){
  if (!p) return null; const r = p.getBoundingClientRect(), g = p.querySelector(':scope > .prsz'), hd = p.querySelector(':scope > .ph');
  const gr = g ? g.getBoundingClientRect() : null, hr = hd ? hd.getBoundingClientRect() : null;
  const gx = gr ? gr.left + gr.width / 2 : 0, gy = gr ? gr.top + gr.height / 2 : 0;
  const hx = hr ? hr.left + Math.min(hr.width * 0.35, 140) : 0, hy = hr ? hr.top + hr.height / 2 : 0;
  const at = (x, y, e) => { const a = document.elementFromPoint(x, y); return !!a && !!e && (a === e || e.contains(a)); };
  return { k: p._pk || null, sz: p._sz || null, x: +r.left.toFixed(1), y: +r.top.toFixed(1), w: +r.width.toFixed(1), h: +r.height.toFixed(1), b: +r.bottom.toFixed(1), r: +r.right.toFixed(1),
    ih: p.style.height || '', imh: p.style.maxHeight || '', cmh: getComputedStyle(p).maxHeight, sized: p.classList.contains('sized'), sh: p.scrollHeight,
    grip: gr ? { cx: +gx.toFixed(1), cy: +gy.toFixed(1), on: gy > 0 && gy < innerHeight && at(gx, gy, g) } : null,
    head: hr ? { cx: +hx.toFixed(1), cy: +hy.toFixed(1), h: +hr.height.toFixed(1), on: hy > 0 && hy < innerHeight && at(hx, hy, hd) } : null,
    vw: innerWidth, vh: innerHeight };
}
window.__PS = {
  idle,
  errs: () => (window.__ERR || []).slice(),
  async go(o){ await idle(); try { closeAllPops(true); } catch (e) {} Object.assign(S, o || {}); await render(); await idle(); await W(500); return { law: S.law, tab: S.tab, jo: S.jo || null }; },
  mokBtn(){ const b = document.getElementById('mokBtn'); if (!b || !vis(b)) return null; try { b.scrollIntoView({ block: 'nearest', inline: 'center' }); } catch (e) {} return hit(b); },
  /* 목차노트 목록 창 — 그 줄을 목록 아래 끝으로 굴리고 칩(k) 또는 줄 이름 자리 */
  async mokRow(note, k, where){ const lp = byKey('moknote|' + PLAW()); if (!lp) return null;
    const r = [...lp.querySelectorAll('.mkr')].find(x => x.dataset.note === note); if (!r) return { err: 'no row' };
    r.scrollIntoView({ block: where || 'end' }); await W(200);
    const c = k ? r.querySelector('.ck[data-k="' + k + '"]') : r.querySelector('.nm'); return c ? Object.assign(hit(c), { t: (c.textContent || '').trim() }) : { err: 'no chip' }; },
  mokList(){ return info(byKey('moknote|' + PLAW())); },
  win(k){ return info(byKey(k)); },
  sel(s){ return info([...document.querySelectorAll(s)].filter(vis).pop() || null); },
  last(){ const L = live(); return info(L[L.length - 1] || null); },
  keys(){ return live().map(p => p._pk); },
  async waitWin(k, ms){ for (let i = 0; i < (ms || 3000) / 50; i++){ const p = byKey(k); if (p && p.querySelector(':scope > .pb') && p.querySelector(':scope > .pb').children.length) { await W(300); await idle(); return info(p); } await W(50); } return info(byKey(k)); },
  async waitSel(s, ms){ for (let i = 0; i < (ms || 3000) / 50; i++){ const p = [...document.querySelectorAll(s)].filter(vis).pop(); if (p) { await W(400); await idle(); return info(p); } await W(50); } return null; },
  cfg(){ try { return JSON.parse(JSON.stringify(S.popCfg || {})); } catch (e) { return {}; } },
  closeKey(k){ const p = byKey(k); const x = p && p.querySelector(':scope > .ph > button:not(.pall)'); return x ? hit(x) : null; },
  rowCode(code){ const r = [...document.querySelectorAll('#slot .c2row')].find(x => !x.classList.contains('c2ov') && (((x.querySelector('.c2code') || {}).textContent) || '').trim().indexOf(code) === 0);
    const c = r && r.querySelector('.c2code'); if (!c) return null; try { c.scrollIntoView({ block: 'center' }); } catch (e) {} return hit(c); },
  mkBtn(){ const b = [...document.querySelectorAll('#slot button')].find(x => /^✎ 마크업/.test((x.textContent || '').trim()) && vis(x)); if (!b) return null; try { b.scrollIntoView({ block: 'center' }); } catch (e) {} return hit(b); },
  overflow(){ const d = document.documentElement; return { docW: [d.scrollWidth, innerWidth],
    pops: live().map(p => { const r = p.getBoundingClientRect(), hd = p.querySelector(':scope > .ph'), hr = hd ? hd.getBoundingClientRect() : r;
      return { k: (p._pk || p.className).slice(0, 40), l: Math.round(r.left), r: Math.round(r.right), t: Math.round(r.top), b: Math.round(r.bottom), headIn: hr.top >= 0 && hr.bottom <= innerHeight && hr.left < innerWidth - 40 && hr.right > 40, xin: r.left >= -1 && r.right <= innerWidth + 1 }; }) }; }
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
        self.pg.wait_for_function("!!window.__PS&&typeof render==='function'&&typeof popSizable==='function'&&!!document.querySelector('#slot')", timeout=120000)
        self.pg.wait_for_timeout(1200)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def idle(self, ms=300):
        self.pg.wait_for_timeout(ms)
        self.ev("()=>__PS.idle()")

    def tap(self, at, wait=500):
        """한 번 누름 — 터치 기기 = 손가락(CDP 또는 touchscreen) · PC = 마우스"""
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

    def drag(self, at, dx, dy, n=14):
        """끌기 — 잡을 자리(at.cx·cy)에서 dx·dy 만큼(화면 밖 자리까지) · 터치 = CDP touchStart→touchMove×n→touchEnd · 마우스 = down→move×n→up"""
        if not at:
            return False
        x0, y0 = at['cx'], at['cy']
        if self.cdp:
            t = lambda ty, x, y: self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': ([] if ty == 'touchEnd' else [{'x': x, 'y': y, 'id': 1}])})
            t('touchStart', x0, y0); self.pg.wait_for_timeout(30)
            for i in range(1, n + 1):
                t('touchMove', x0 + dx * i / n, y0 + dy * i / n); self.pg.wait_for_timeout(16)
            t('touchEnd', x0 + dx, y0 + dy)
        else:
            m = self.pg.mouse
            m.move(x0, y0); m.down()
            for i in range(1, n + 1):
                m.move(x0 + dx * i / n, y0 + dy * i / n); self.pg.wait_for_timeout(16)
            m.up()
        self.idle(350)
        return True

    def hold(self, at, stages, measure, n=10):
        """손을 떼지 않고 여러 자리로 — stages = 잡은 자리에서의 누적 (dx, dy) 목록 · 자리마다 measure() 값 · 끝에 뗌(뗀 뒤 저장)"""
        if not at:
            return []
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
            self.pg.wait_for_timeout(80)
            out.append(measure())
        if self.cdp:
            t('touchEnd', cx, cy)
        else:
            self.pg.mouse.up()
        self.idle(350)
        return out

    def shot(self, name):
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


def pair(br, eng, dev, src_new, src_base):
    a = P(br, eng, 'NEW', src_new, dev)
    b = P(br, eng, 'BASE', src_base, dev) if src_base else None
    return a, b


def both(a, b, fn):
    """같은 차례를 두 판에 — fn(page) → 값 · 바탕이 없으면 None"""
    vn = fn(a)
    vb = fn(b) if b else None
    return vn, vb


def hgt(v):
    return v and v.get('h')


def sfx(eng):
    return '' if eng == 'chromium' else '·' + eng


def eq(a, b, tol=1.0):
    return a is not None and b is not None and abs(a - b) <= tol


# ── 목차노트 칩 창(B1 · B2) ──
def open_chip(p):
    """민소 → 2차 → 목차노트(#mokBtn) → 목록 창에서 4.2.2. 줄을 아래 끝으로 → 「기출」 칩 톡 → 칩 창"""
    p.ev("o=>__PS.go(o)", {'law': '민사소송법', 'tab': 'cha2', 'boardKind': '기출'})
    if not p.tap(p.ev("()=>__PS.mokBtn()"), 900):
        return {'err': 'mokBtn'}
    if not p.ev("()=>__PS.mokList()"):
        return {'err': 'list'}
    at = p.ev("([n,k])=>__PS.mokRow(n,k)", [NOTE, '기출'])
    if not at or not at.get('on'):
        return {'err': 'chip', 'at': at}
    p.tap(at, 600)
    w = p.ev("([k,ms])=>__PS.waitWin(k,ms)", [CHIP, 4000])
    return w or {'err': 'win'}


def grip(p, getw, dx, dy):
    """그 창 손잡이(.prsz)를 지금 자리에서 dx·dy 끌기 → 끈 뒤 창"""
    w = getw(p)
    if not w or not w.get('grip'):
        return None
    p.drag(w['grip'], dx, dy)
    return getw(p)


def head(p, getw, dx, dy):
    w = getw(p)
    if not w or not w.get('head') or not w['head'].get('on'):
        return None
    p.drag(w['head'], dx, dy)
    return getw(p)


def lift(p, getw, room=40):
    """prsz_pin 뒤 꼴(10/4 고침 · 머리글 ※) — 창 아래가 화면 밖이면(손잡이도 화면 밖) 머리를 (아래 − 화면 + room) 만큼 위로 끌고 → (끈 뒤 창, 끈 거리 · 0 = 안 끎 · None = 머리 못 잡음)"""
    w = getw(p)
    if not w or w['b'] <= w['vh'] - 4:
        return w, 0
    dy = -round(w['b'] - w['vh'] + room)
    if head(p, getw, 0, dy) is None:
        return getw(p), None
    return getw(p), dy


def geo(w):
    return None if not w else {'x': w['x'], 'y': w['y'], 'w': w['w'], 'h': w['h'], 'b': w['b']}


def B1(br, eng, sn, sb):
    g = 'B1' + sfx(eng)
    a, b = pair(br, eng, 'padP', sn, sb)
    try:
        cw = lambda p: p.ev("k=>__PS.win(k)", CHIP)
        w0n, w0b = both(a, b, open_chip)
        N(g, '아이패드 세로 820×1180 · 4.2.2. 「기출」 칩 창 처음 자리(지시서 실측 위 1042 · 높이 130 — 다르면 값만)', {'new': geo(w0n) or w0n, 'base': geo(w0b) or w0b, 'how': a.how})
        if not (w0n and w0n.get('grip')):
            T(g, '칩 창 열림', False, w0n)
            return
        w1n, w1b = both(a, b, lambda p: grip(p, cw, 0, 150))
        exp1 = lambda w0: w0['h'] + 150
        TB(g, '손잡이 +150 → 높이 = 잡을 때 + 150(280) · 위 무변 · 아래 화면 밖 허용(줄이지 않음)',
           lambda v: v[1] and eq(v[1]['h'], exp1(v[0])) and eq(v[1]['y'], v[0]['y']) and (v[0]['y'] + exp1(v[0]) <= v[1]['vh'] or v[1]['b'] > v[1]['vh']),
           [geo(w0n), dict(geo(w1n) or {}, vh=(w1n or {}).get('vh'))], [geo(w0b), dict(geo(w1b) or {}, vh=(w1b or {}).get('vh'))] if b else None)
        l2 = both(a, b, lambda p: lift(p, cw))   # prsz_pin 뒤 꼴 — 아래가 화면 밖이면 머리를 먼저 위로(10/4 고침 · 머리글 ※)
        N(g, '−150 앞 lift(prsz_pin 뒤 꼴 · 머리를 위로 끈 거리)', {'new': l2[0][1], 'base': l2[1][1] if b else None})
        w2n, w2b = both(a, b, lambda p: grip(p, cw, 0, -150))
        TB(g, '이어서 −150 → max(min(240, 잡을 때 높이), 잡을 때 − 150)(= 240) · 위 무변',
           lambda v: v[1] and eq(v[1]['h'], max(min(240, v[0]['h']), v[0]['h'] - 150)) and eq(v[1]['y'], v[0]['y']),
           [geo(l2[0][0]), geo(w2n)], [geo(l2[1][0]), geo(w2b)] if b else None)
        for i, (vn, vb) in enumerate([(w0n, w0b), (w1n, w1b), (w2n, w2b)]):
            same(g, ['처음', '+150', '−150'][i], vn and [vn['x'], vn['w']], vb and [vb['x'], vb['w']])
        a.shot('B1'); b and b.shot('B1')
        N(g, '손잡이 자리(끈 뒤 · 창이 글보다 크면 sticky 손잡이는 글 끝에 선다 — 지금 꼴 그대로)', {'new': (w2n or {}).get('grip'), 'base': (w2b or {}).get('grip')})
    finally:
        a.close(); b and b.close()


def B2(br, eng, sn, sb):
    g = 'B2' + sfx(eng)
    a, b = pair(br, eng, 'padP', sn, sb)
    try:
        cw = lambda p: p.ev("k=>__PS.win(k)", CHIP)
        w0n, w0b = both(a, b, open_chip)
        if not (w0n and w0n.get('grip')):
            T(g, '칩 창 열림', False, w0n)
            return
        s1 = both(a, b, lambda p: head(p, cw, 0, -600))
        s2 = both(a, b, lambda p: grip(p, cw, 0, 400))
        s3 = both(a, b, lambda p: head(p, cw, 0, 500))
        l4 = both(a, b, lambda p: lift(p, cw))   # prsz_pin 뒤 꼴 — 아래가 화면 밖이라 머리를 먼저 위로(10/4 고침 · 머리글 ※ · 새 판·바탕 같은 거리)
        s4 = both(a, b, lambda p: grip(p, cw, 0, 60))
        pick = lambda k: [geo(x[k]) for x in ((w0n, w0b), s1, s2, s3, s4)] + [geo(l4[k][0]) if l4[k] else None]   # [5] = 잡을 때(lift 뒤)
        N(g, '+60 앞 lift(prsz_pin 뒤 꼴 · 머리를 위로 끈 거리)', {'new': l4[0][1], 'base': l4[1][1] if b else None})
        vn, vb = pick(0), (pick(1) if b else None)
        TB(g, '머리 위로 600 → 위 = 처음 − 600(%d)' % round(w0n['y'] - 600), lambda v: v[1] and eq(v[1]['y'], v[0]['y'] - 600) and eq(v[1]['h'], v[0]['h']), vn[:2], vb and vb[:2])
        TB(g, '손잡이 +400 → 높이 = 처음 + 400(530) · 위 무변', lambda v: v[2] and eq(v[2]['h'], v[1]['h'] + 400) and eq(v[2]['y'], v[1]['y']), vn[:3], vb and vb[:3])
        TB(g, '머리 아래로 500 → 위 + 500 · 아래 화면 밖', lambda v: v[3] and eq(v[3]['y'], v[2]['y'] + 500) and v[3]['b'] > DEV['padP']['H'], vn[:4], vb and vb[:4])
        TB(g, '손잡이 +60 → 높이 = 잡을 때 + 60(590 · 바탕 240) · 위 무변', lambda v: v[4] and v[5] and eq(v[4]['h'], v[5]['h'] + 60) and eq(v[4]['y'], v[5]['y']), vn, vb)
        # B7 재료 — 머리 끌기 좌우 · 손잡이 가로
        s5 = both(a, b, lambda p: head(p, cw, -180, 0))
        s6 = both(a, b, lambda p: head(p, cw, 120, -40))
        both(a, b, lambda p: lift(p, cw))   # prsz_pin 뒤 꼴(10/4 고침) — 손잡이 화면 밖이면 머리를 먼저 위로 · 「손잡이 ←90」 맞대기는 [x, w] 라 y 무관
        s7 = both(a, b, lambda p: grip(p, cw, -90, 0))
        for i, (x, y) in enumerate(((w0n, w0b), s1, s2, s3, s4, s5, s6, s7)):
            nm = ['처음', '머리 ↑600', '손잡이 +400', '머리 ↓500', '손잡이 +60', '머리 ←180', '머리 →120·↑40', '손잡이 ←90'][i]
            same(g, nm, x and ([x['x'], x['y'], x['w']] if i in (1, 3, 5, 6) else [x['x'], x['w']]), y and ([y['x'], y['y'], y['w']] if i in (1, 3, 5, 6) else [y['x'], y['w']]))
        a.shot('B2'); b and b.shot('B2')
    finally:
        a.close(); b and b.close()


def B3(br, eng, sn, sb):
    g = 'B3' + sfx(eng)
    for dev in ('padP', 'padL'):
        a, b = pair(br, eng, dev, sn, sb)
        try:
            def openl(p):
                p.ev("o=>__PS.go(o)", {'law': '민사소송법', 'tab': 'cha2', 'boardKind': '기출'})
                p.tap(p.ev("()=>__PS.mokBtn()"), 900)
                return p.ev("()=>__PS.mokList()")
            lw = lambda p: p.ev("()=>__PS.mokList()")
            l0 = both(a, b, openl)
            l1 = both(a, b, lambda p: grip(p, lw, 0, 200))
            vn = [l0[0] and dict(geo(l0[0]), imh=l0[0]['imh']), l1[0] and dict(geo(l1[0]), imh=l1[0]['imh'])]
            vb = [l0[1] and dict(geo(l0[1]), imh=l0[1]['imh']), l1[1] and dict(geo(l1[1]), imh=l1[1]['imh'])] if b else None
            TB(g, '%s %d×%d — 목차노트 목록 창(인라인 max-height %s) 손잡이 +200 → 높이 +200 · 위 무변(바탕 = max-height 에 막힘)' % ('아이패드 세로' if dev == 'padP' else '아이패드 가로', DEV[dev]['W'], DEV[dev]['H'], (l0[0] or {}).get('imh')),
               lambda v: v[0] and v[1] and v[0]['imh'] not in ('', 'none') and eq(v[1]['h'], v[0]['h'] + 200) and eq(v[1]['y'], v[0]['y']), vn, vb)
            same(g, dev + ' 처음', l0[0] and [l0[0]['x'], l0[0]['w']], l0[1] and [l0[1]['x'], l0[1]['w']])
            same(g, dev + ' +200', l1[0] and [l1[0]['x'], l1[0]['w']], l1[1] and [l1[1]['x'], l1[1]['w']])
            a.shot('B3'); b and b.shot('B3')
        finally:
            a.close(); b and b.close()


def B4(br, eng, sn, sb):
    g = 'B4' + sfx(eng)
    a, b = pair(br, eng, 'pc', sn, sb)
    try:
        def openc(p):
            p.ev("o=>__PS.go(o)", {'law': '민사소송법', 'tab': 'cha2', 'boardKind': '기출', 'c2ord': 'unit'})
            p.tap(p.ev("c=>__PS.rowCode(c)", CODE), 900)
            return p.ev("()=>__PS.last()")
        c0 = both(a, b, openc)
        if not (c0[0] and c0[0].get('grip')):
            T(g, '카드 창 열림', False, c0[0])
            return
        kn, kb = c0[0]['k'], (c0[1] or {}).get('k')
        cwn = lambda p: p.ev("k=>__PS.win(k)", kn if p.tag == 'NEW' else kb)
        # 한 번 잡고(마우스를 떼지 않고) +300 → −200(= +100) → 더 위로(= −600) — +300 뒤 손잡이는 화면 밖이라 다시 잡을 수 없다(지시서 「손가락을 그대로 따라감」)
        st = both(a, b, lambda p: p.hold(cwn(p)['grip'], [(0, 300), (0, 100), (0, -600)], lambda: geo(cwn(p))))
        fin = both(a, b, lambda p: geo(cwn(p)))
        vn = [geo(c0[0])] + list(st[0]) + [fin[0]]
        vb = ([geo(c0[1])] + list(st[1]) + [fin[1]]) if b else None
        N(g, 'PC 1440×900 마우스 · 카드 창 %s 처음' % kn, {'new': vn[0], 'base': vb and vb[0]})
        TB(g, '잡고 +300 → 높이 = 잡을 때 + 300(아래 화면 밖이어도 · 줄이지 않음) · 위 무변', lambda v: v[1] and eq(v[1]['h'], v[0]['h'] + 300) and eq(v[1]['y'], v[0]['y']), vn[:2], vb and vb[:2])
        TB(g, '떼지 않고 −200(= 잡을 때 + 100) → 마우스 그대로', lambda v: v[2] and eq(v[2]['h'], v[0]['h'] + 100) and eq(v[2]['y'], v[0]['y']), vn[:3], vb and vb[:3])
        TB(g, '더 위로(= 잡을 때 − 600) → 240 아래로 안 줄음(= max(min(240, 잡을 때), 잡을 때 − 600)) · 뗀 뒤 그대로', lambda v: v[3] and eq(v[3]['h'], max(min(240, v[0]['h']), v[0]['h'] - 600)) and v[4] and eq(v[4]['h'], v[3]['h']), vn, vb)
        for i in range(5):
            same(g, ['처음', '+300', '+100', '−600', '뗀 뒤'][i], vn[i] and [vn[i]['x'], vn[i]['w']], vb and vb[i] and [vb[i]['x'], vb[i]['w']])
        a.shot('B4'); b and b.shot('B4')
    finally:
        a.close(); b and b.close()


def B5(br, eng, sn, sb):
    g = 'B5' + sfx(eng)
    a, b = pair(br, eng, 'phone', sn, sb)
    try:
        nk = 'note|민소|' + NOTE + '|'

        def openn(p):
            p.ev("o=>__PS.go(o)", {'law': '민사소송법', 'tab': 'cha2', 'boardKind': '기출'})
            p.tap(p.ev("()=>__PS.mokBtn()"), 900)
            at = p.ev("([n,k,w])=>__PS.mokRow(n,k,w)", [NOTE, None, 'center'])
            p.tap(at, 600)
            return p.ev("([k,ms])=>__PS.waitWin(k,ms)", [nk, 4000])
        nw = lambda p: p.ev("k=>__PS.win(k)", nk)
        n0 = both(a, b, openn)
        if not (n0[0] and n0[0].get('grip')):
            T(g, '노트 창 열림', False, n0[0])
            return
        n1 = both(a, b, lambda p: grip(p, nw, 0, 200))
        cf = both(a, b, lambda p: (p.ev("()=>__PS.cfg()") or {}).get('note'))
        vn = [dict(geo(n0[0]), imh=n0[0]['imh']), n1[0] and dict(geo(n1[0]), imh=n1[0]['imh'], vh=n1[0]['vh'])]
        vb = [dict(geo(n0[1]), imh=n0[1]['imh']), n1[1] and dict(geo(n1[1]), imh=n1[1]['imh'], vh=n1[1]['vh'])] if b and n0[1] else None
        TB(g, '폰 390×844 · 목차노트 노트 창(아래 70%% · 인라인 max-height %s) 손잡이 +200 → 높이 + 200 · 위 무변 · 아래 화면 밖' % n0[0]['imh'],
           lambda v: v[1] and eq(v[1]['h'], v[0]['h'] + 200) and eq(v[1]['y'], v[0]['y']) and v[1]['b'] > v[1]['vh'], vn, vb)
        TB(g, '기억 높이(jopangi_ui pop_note.h) = 끈 높이', lambda v: v[0] and v[1] and eq(v[0].get('h'), v[1]['h']), [cf[0], vn[1]], [cf[1], vb[1]] if vb else None)
        same(g, '처음', [n0[0]['x'], n0[0]['w']], n0[1] and [n0[1]['x'], n0[1]['w']])
        same(g, '+200', n1[0] and [n1[0]['x'], n1[0]['w']], n1[1] and [n1[1]['x'], n1[1]['w']])
        a.shot('B5'); b and b.shot('B5')

        def reopen(p):
            p.tap(p.ev("k=>__PS.closeKey(k)", nk), 500)
            gone = p.ev("k=>__PS.win(k)", nk) is None
            at = p.ev("([n,k,w])=>__PS.mokRow(n,k,w)", [NOTE, None, 'center'])
            p.tap(at, 600)
            w = p.ev("([k,ms])=>__PS.waitWin(k,ms)", [nk, 4000])
            return {'닫힘': gone, '다시': geo(w), 'imh': w and w['imh'], 'cfg_h': ((p.ev("()=>__PS.cfg()") or {}).get('note') or {}).get('h')}
        r = both(a, b, reopen)
        N(g, '닫고 다시 열기 — 기억 높이로 열리나(폰 = 지금 vvFit·mokPlace 70% 규칙대로 줄면 그대로 · 값만)', {'new': r[0], 'base': r[1]})
        a.shot('B5re'); b and b.shot('B5re')
    finally:
        a.close(); b and b.close()


def B6(br, eng, sn, sb):
    g = 'B6' + sfx(eng)
    for dev in ('padL', 'pc'):
        a, b = pair(br, eng, dev, sn, sb)
        try:
            def openm(p):
                p.ev("o=>__PS.go(o)", {'law': JO[0], 'tab': 'jo', 'jo': JO[1], 'mkWin': False})
                p.tap(p.ev("()=>__PS.mkBtn()"), 900)
                return p.ev("([s,ms])=>__PS.waitSel(s,ms)", ['.pop.wm-mk', 4000])
            mw = lambda p: p.ev("s=>__PS.sel(s)", '.pop.wm-mk')
            m0 = both(a, b, openm)
            if not (m0[0] and m0[0].get('grip')):
                T(g, '%s 원문(마크업) 창 열림' % dev, False, m0[0])
                continue
            # 가로 먼저(손잡이가 둘 다 화면 안일 때) — +300 뒤에는 새 판 손잡이가 화면 밖이라 다시 못 잡는다(지시서 「화면 밖 허용」)
            mx = both(a, b, lambda p: grip(p, mw, -80, 0))
            same(g, dev + ' 손잡이 ←80', mx[0] and [mx[0]['x'], mx[0]['w'], mx[0]['h']], mx[1] and [mx[1]['x'], mx[1]['w'], mx[1]['h']])
            m1 = both(a, b, lambda p: grip(p, mw, 0, 300))
            vn = [geo(mx[0]), m1[0] and dict(geo(m1[0]), vh=m1[0]['vh'])]
            vb = [geo(mx[1]), m1[1] and dict(geo(m1[1]), vh=m1[1]['vh'])] if b and mx[1] else None
            TB(g, '%s %d×%d %s — 원문 창(wmWin ✎ 마크업 · %s %s) 손잡이 +300 → 높이 + 300 · 위 무변 · 아래 화면 밖(바탕 = 남은 높이로 잘림)' % (
                '아이패드 가로' if dev == 'padL' else 'PC', DEV[dev]['W'], DEV[dev]['H'], a.how, JO[0], JO[1]),
               lambda v: v[1] and eq(v[1]['h'], v[0]['h'] + 300) and eq(v[1]['y'], v[0]['y']) and v[1]['b'] > v[1]['vh'], vn, vb)
            same(g, dev + ' 처음', [m0[0]['x'], m0[0]['w']], m0[1] and [m0[1]['x'], m0[1]['w']])
            same(g, dev + ' +300', m1[0] and [m1[0]['x'], m1[0]['w']], m1[1] and [m1[1]['x'], m1[1]['w']])
            a.shot('B6'); b and b.shot('B6')
        finally:
            a.close(); b and b.close()


def B7():
    g = 'B7'
    if not SAME:
        N(g, '맞댈 값 없음(바탕 안 잼)', '')
        return
    by = {}
    for gg, where, vn, vb in SAME:
        ok = vn is not None and vb is not None and len(vn) == len(vb) and all(abs(x - y) <= 1.0 for x, y in zip(vn, vb))
        by.setdefault(gg, []).append((where, ok, vn, vb))
    for gg, xs in by.items():
        bad = [x for x in xs if not x[1]]
        T(g, '%s — 폭 · left · 머리 끌기(좌우·위아래) · 손잡이 가로 결과 = 바탕(%d 자리)' % (gg, len(xs)), not bad, bad[:4] if bad else [x[0] for x in xs])


def sweep(br, eng, sn):
    """화면 훑기 — 네 기기에서 창을 키운 뒤 가로 넘침 0 · 창 머리 화면 안(다시 잡힘) · 창 좌우 화면 안 · 그림"""
    g = '훑기'
    for dev in ('padP', 'padL', 'pc', 'phone'):
        p = P(br, eng, 'NEW', sn, dev)
        try:
            p.ev("o=>__PS.go(o)", {'law': '민사소송법', 'tab': 'cha2', 'boardKind': '기출'})
            p.tap(p.ev("()=>__PS.mokBtn()"), 900)
            lw = lambda q: q.ev("()=>__PS.mokList()")
            grip(p, lw, 0, 160)
            at = p.ev("([n,k,w])=>__PS.mokRow(n,k,w)", [NOTE, '기출', 'center'])
            p.tap(at, 600)
            cw = lambda q: q.ev("k=>__PS.win(k)", CHIP)
            if p.ev("([k,ms])=>__PS.waitWin(k,ms)", [CHIP, 4000]):
                grip(p, cw, 0, 220)
            ov = p.ev("()=>__PS.overflow()")
            p.shot('sweep')
            ok = ov['docW'][0] <= ov['docW'][1] and all(x['headIn'] and x['xin'] for x in ov['pops']) and len(ov['pops']) >= 1
            T(g, '%s %d×%d — 목록 창 +160 · 칩 창 +220 뒤 가로 넘침 0 · 창 머리 화면 안 · 창 좌우 화면 안(아래 끝은 화면 밖 허용)' % (dev, DEV[dev]['W'], DEV[dev]['H']), ok, ov)
        finally:
            p.close()


def main():
    src_new = app_src(NEW)
    src_base = app_src(BASE)
    if not src_new:
        raise SystemExit('앱을 못 읽었다: ' + NEW)
    print('NEW  = %s · md5(LF) %s · %d B(LF)' % (NEW, md5lf(src_new), len(src_new.replace('\r\n', '\n').encode('utf-8'))))
    print('BASE = %s · %s' % (BASE, ('md5(LF) ' + md5lf(src_base)) if src_base else '못 읽음(안 잼 — B7·헛잣대 없이)'))
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
                groups = [('B1', B1), ('B2', B2), ('B3', B3), ('B4', B4), ('B5', B5), ('B6', B6)]
                if eng != 'chromium':
                    groups = [x for x in groups if x[0] in ('B1', 'B2', 'B5')]   # WebKit = 지시서 터치 칸(1·2·5)만
                for k, fn in groups:
                    if not want(k):
                        continue
                    t1 = time.time()
                    try:
                        fn(br, eng, src_new, src_base)
                    except Exception as e:
                        T(k, '%s 실행 오류' % eng, False, '%s: %s' % (type(e).__name__, str(e)[:300]))
                        traceback.print_exc()
                    phase['%s%s' % (k, '' if eng == 'chromium' else '·' + eng)] = round(time.time() - t1, 1)
                if eng == 'chromium' and (want('B7') or not ONLY):
                    B7()
                if eng == 'chromium' and want('SWEEP'):
                    t1 = time.time()
                    sweep(br, eng, src_new)
                    phase['훑기'] = round(time.time() - t1, 1)
            finally:
                br.close()
    by = {}
    for gg, nm, okb in YARD:
        by.setdefault(gg, []).append(okb)
    for gg in sorted(by):
        oks = by[gg]
        T('헛잣대', gg, not all(oks), '바탕 FAIL %d / %d' % (oks.count(False), len(oks)))
    ok = [r for r in RES if r[2] is True]
    bad = [r for r in RES if r[2] is False]
    lines = ['_harness_jo_popsize — PASS %d · FAIL %d · %s초' % (len(ok), len(bad), round(time.time() - T0, 1)),
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
