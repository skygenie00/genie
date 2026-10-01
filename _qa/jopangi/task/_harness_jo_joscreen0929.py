# -*- coding: utf-8 -*-
"""_task_jo_joscreen0929 관문 — 조판기 조문 화면 손질(서랍 · 연결 줄 · 모드 줄 · 본문 길게 누르기 · 조문 팝업 원문 · 3법 카드 원문 · 원문 보기 설명 글).

쓰는 법(N: jopangi/task/ 또는 genie _qa/jopangi/task/ 에서 · 저장소 = _roots.genie() = GENIE_ROOT · 없으면 ~/Documents/genie)
  python _harness_jo_joscreen0929.py                          # 그 저장소 jo/index.html · Chromium · B-1~B-7 + 회귀 R
  python _harness_jo_joscreen0929.py --html <바탕 index.html> --yardstick
                                                              # 헛잣대 — 바탕(착수 HEAD)에서 B-1~B-7 이 저마다 FAIL 해야 한다
  python _harness_jo_joscreen0929.py --webkit                # 터치 칸(B-2 폰 · B-5)을 WebKit 으로도(깔려 있으면)
  python _harness_jo_joscreen0929.py --only B1,B5            # 일부만
  ★ 2026-09-29 합치기(Code) — 클라우드가 _qa/ 맨 위에 두었던 것을 N: 정본 jopangi/task/ 로 들여오고 genie 는 _qa/jopangi/task/ 로 옮겼다.
    바꾼 것은 _roots 머리 5줄과 ROOT 한 줄뿐(옛: 이 파일의 위 폴더 = 저장소 뿌리 · 옮긴 자리에서는 뿌리가 아니다).

준비: pip install playwright · playwright install chromium (WebKit 은 playwright install webkit).
서버는 스스로 띄운다(127.0.0.1 · 빈 포트): /jo/index.html = --html 파일 · /jo/data/* = 이 저장소 jo/data. 바깥 주소 요청은 막는다(재현성).
화면: PC 1511×1043(사용자 125%) · 폰 390×844 터치 흉내(is_mobile · has_touch · CDP 터치 이벤트로 길게 누르기).
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import argparse
import json
import os
import re
import sys
import threading
import time
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from playwright.sync_api import sync_playwright

ROOT = _roots.genie()   # 합치기(9/29) — 옛: 이 파일의 위 폴더(_qa/ 맨 위에 있을 때만 저장소 뿌리)
DATA = os.path.join(ROOT, 'jo', 'data')
PC = {'width': 1511, 'height': 1043}
PHONE = {'width': 390, 'height': 844}
BK = {'내용': 'rgb(37, 99, 235)', '주체': 'rgb(124, 58, 237)', '기간': 'rgb(5, 150, 105)'}
Q15 = ['제1조', '제2조', '제3조', '제4조', '제5조', '제6조', '제7조', '제7조의2', '제8조', '제9조', '제10조', '제11조', '제12조', '제13조', '제14조', '제15조']
Q15N = [11, 62, 16, 6, 12, 10, 4, 4, 1, 3, 8, 11, 3, 3, 37, 18]
BJNOTE = '사진(특허법 33·34쪽) 실측 조판 — 한 행 길이 고정 · 어절 중간에서 끊는다 · 양끝맞춤. 글자 크기는 바꿀 수 없다(필기가 이 고정에 기댄다).'
LAWS = ['특허법', '상표법', '디자인보호법', '민사소송법']

JS_HELPERS = r"""
window.__findText = function(root, needle, nth){
  nth = nth || 0; if (!root) return null;
  const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT); const nodes = []; let n;
  while ((n = tw.nextNode())) nodes.push(n);
  const str = nodes.map(x => x.nodeValue).join('');
  let p = -1; for (let k = 0; k <= nth; k++){ p = str.indexOf(needle, p + 1); if (p < 0) return null; }
  const at = pos => { let acc = 0; for (const x of nodes){ const L = x.nodeValue.length; if (pos < acc + L) return [x, pos - acc]; acc += L; } const last = nodes[nodes.length - 1]; return [last, last.nodeValue.length]; };
  const [sn, so] = at(p), [en, eo] = at(p + needle.length - 1);
  const r = document.createRange(); r.setStart(sn, so); r.setEnd(en, eo + 1); return r;
};
window.__rectOf = function(r){ const rc = r.getBoundingClientRect(); return {x: rc.left + rc.width / 2, y: rc.top + rc.height / 2, l: rc.left, t: rc.top, r: rc.right, b: rc.bottom}; };
window.__rc = function(e){ if (!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
window.__toasts = [];
(function(){ const f = () => { try { if (typeof toast === 'function' && !toast.__w){ const t0 = toast; const w = function(m, b){ window.__toasts.push(String(m)); return t0(m, b); }; w.__w = 1; toast = w; } } catch (e) {} };
  document.addEventListener('DOMContentLoaded', f); setTimeout(f, 0); setTimeout(f, 800); })();
"""

BARQ = r"""() => { const bars = ['jomk9', 'mkc9', 'c2mark'].map(id => document.getElementById(id)).filter(b => b && !b.hidden);
  const s = getSelection(); let sr = null; if (s.rangeCount && !s.isCollapsed) sr = __rc(s.getRangeAt(0));
  return {pit: document.querySelectorAll('.pitmenu').length, pitText: [...document.querySelectorAll('.pitmenu')].map(m => m.textContent), sel: String(s), selRect: sr,
    bars: bars.map(b => ({id: b.id, rect: __rc(b), paint: b.querySelectorAll('button[data-m]').length,
      row2: [...b.querySelectorAll('.mk9r2 button')].filter(x => !x.hidden && x.offsetParent).map(x => x.textContent.trim())})),
    pops: POPS.map(p => (p.querySelector('.pt') || {}).textContent)}; }"""


# ─────────────── 서버 ───────────────
def serve(html_path):
    html_path = os.path.abspath(html_path)

    class H(SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
            if p in ('/jo/', '/jo/index.html'):
                return html_path
            if p.startswith('/jo/data/'):
                return os.path.join(DATA, p[len('/jo/data/'):].replace('/', os.sep))
            return os.path.join(ROOT, '__nope__')

    httpd = ThreadingHTTPServer(('127.0.0.1', 0), H)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, 'http://127.0.0.1:%d/jo/index.html' % httpd.server_address[1]


# ─────────────── 결과 ───────────────
class R:
    def __init__(self):
        self.rows = []   # (gate, id, ok, detail)
        self.notes = []

    def ck(self, gate, cid, ok, detail=''):
        self.rows.append((gate, cid, bool(ok), detail))
        print('  %-5s %-6s %s  %s' % (gate, cid, 'PASS' if ok else 'FAIL', detail), flush=True)
        return ok

    def note(self, s):
        self.notes.append(s)
        print('  · ' + s, flush=True)

    def gate_ok(self, gate):
        rs = [r for r in self.rows if r[0] == gate]
        return bool(rs) and all(r[2] for r in rs)


# ─────────────── 쪽 여는 도구 ───────────────
def new_page(br, url, phone=False, ui=None, ls=None, errs=None):
    kw = dict(viewport=PHONE, is_mobile=True, has_touch=True, device_scale_factor=3) if phone else dict(viewport=PC)
    ctx = br.new_context(**kw)
    ctx.route(lambda u: not u.startswith('http://127.0.0.1'), lambda route: route.abort())
    init = {'jopangi_ui': json.dumps(ui if ui is not None else ({'trw': 276} if not phone else {}), ensure_ascii=False)}
    for k, v in (ls or {}).items():
        init[k] = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    ctx.add_init_script("if(!sessionStorage.getItem('__h')){sessionStorage.setItem('__h','1');const I=%s;for(const k in I)localStorage.setItem(k,I[k]);}" % json.dumps(init, ensure_ascii=False))
    ctx.add_init_script(JS_HELPERS)
    pg = ctx.new_page()
    if errs is not None:
        pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(url)
    pg.wait_for_function("typeof S!=='undefined' && typeof busy!=='undefined' && !busy && document.querySelector('#slot .main')", timeout=60000)
    idle(pg)
    return ctx, pg


def idle(pg, extra=150):
    pg.wait_for_function("typeof busy!=='undefined' && !busy", timeout=60000)
    pg.wait_for_timeout(extra)


def go_jo(pg, law, jo, extra=''):
    pg.evaluate("([l,k]) => { closeAllPops(true); S.tab='jo'; S.law=l; S.jo=k; %s render(); }" % extra, [law, jo])
    idle(pg)
    pg.wait_for_function("k => { const t = document.querySelector('#slot .main .jotitle'); return t && t.textContent.indexOf(k) === 0; }", arg=jo, timeout=60000)
    idle(pg, 250)


def pop_wait(pg, key, t=15000):
    """POPS 맨 위 팝업 제목에 key 가 들고 몸이 다 그려질 때까지"""
    pg.wait_for_function("k => { const p = POPS[POPS.length - 1]; if (!p) return false; const t = (p.querySelector('.pt') || {}).textContent || ''; return t.indexOf(k) >= 0 && t.indexOf('불러오는 중') < 0; }", arg=key, timeout=t)
    pg.wait_for_timeout(250)


WK_LONG = r"""([x, y, ty]) => { const t = ty === 'pointerdown' ? document.elementFromPoint(x, y) : (window.__tlT || document.elementFromPoint(x, y));
  if (ty === 'pointerdown') window.__tlT = t;
  t.dispatchEvent(new PointerEvent(ty, {bubbles: true, cancelable: true, composed: true, pointerId: 7, pointerType: 'touch', isPrimary: true,
    clientX: x, clientY: y, button: 0, buttons: ty === 'pointerdown' ? 1 : 0}));
  if (ty === 'pointerup') t.dispatchEvent(new Event('touchend', {bubbles: true, cancelable: true, composed: true}));   // 실기기처럼 손을 뗄 때 touchend 도(선택으로 막대를 띄우는 길)
  return t.tagName; }"""


def touch_long(ctx, pg, x, y, ms=700, mid=None):
    if ctx.browser and ctx.browser.browser_type.name != 'chromium':
        # 합치기(9/29 Code) — WebKit: Playwright 는 진짜 터치를 붙잡고 있지 못한다(톡만 · CDP 없음).
        # 앱 길게 누르기 = 줄 pointerdown 뒤 500ms 타이머(pitWire) — 같은 자리에 합성 touch 포인터를 같은 시간 보내 그 길을 잰다.
        pg.evaluate(WK_LONG, [x, y, 'pointerdown'])
        if mid:
            pg.wait_for_timeout(200)
            mid()
            pg.wait_for_timeout(max(0, ms - 200))
        else:
            pg.wait_for_timeout(ms)
        pg.evaluate(WK_LONG, [x, y, 'pointerup'])
        pg.wait_for_timeout(350)
        return
    cdp = ctx.new_cdp_session(pg)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]})
    if mid:
        pg.wait_for_timeout(200)
        mid()
        pg.wait_for_timeout(max(0, ms - 200))
    else:
        pg.wait_for_timeout(ms)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    pg.wait_for_timeout(350)
    try:
        cdp.detach()
    except Exception:
        pass


def tap_sel(pg, sel):
    rc = pg.evaluate("s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }", sel)
    if not rc:
        return False
    pg.touchscreen.tap(rc[0], rc[1])
    return True


def word_pos(pg, root_js, needle, nth=0):
    return pg.evaluate("([n, k]) => { const root = %s; const r = __findText(root, n, k); if (!r) return null; (r.startContainer.parentElement || root).scrollIntoView({block: 'center'}); return __rectOf(r); }" % root_js, [needle, nth])


def law_counts():
    """목록 자료에서 접기1 · 접기2 · 펴기에 보일 줄 수(1차객 uzLvApply 규칙: 접기 L = 깊이 L 이상 머리를 접음)"""
    out = {}
    for law in LAWS:
        L = json.load(open(os.path.join(DATA, 'jo_%s_목록.json' % law), encoding='utf-8'))
        H, J = L.get('장', []), L['조']
        n1 = sum(1 for h in H if h.get('lv') == 1)
        n2 = sum(1 for h in H if h.get('lv') == 2)
        under2 = sum(1 for x in J if x.get('j') is not None and H[x['j']].get('lv') == 2)
        # ★ A-6(a) 9/30 _task_qa_baseline — revfix0930 A-4: 층 → 깊이(lv − 그 법 맨 위 lv + 1)로 단계 접기(민소 편 lv 0 → 접기1 편 · 접기2 +장 · 접기3 +절 · 펴기)
        #   깊이 L 접기 = 깊이 ≤ L 머리 + 제 머리(j) 깊이 ≤ L−1 인 조 · 펴기 = 머리 전부 + 조 전부 · 맨 위 lv 1 인 세 법은 옛 식과 같은 값
        top = min([h.get('lv', 1) for h in H] or [1])
        dep = lambda h: h.get('lv', 1) - top + 1
        o = {'lv1': n1, 'lv2': n2, 'jo': len(J), 'open': len(H) + len(J)}
        for d in range(1, max([dep(h) for h in H] or [0]) + 1):
            o['fold%d' % d] = sum(1 for h in H if dep(h) <= d) + sum(1 for x in J if x.get('j') is None or dep(H[x['j']]) <= d - 1)
        out[law] = o
    return out


# ─────────────── B-1 서랍 ───────────────
def b1(br, url, R):
    G = 'B1'
    errs = []
    ctx, pg = new_page(br, url, errs=errs)
    go_jo(pg, '특허법', '제1조')
    t = pg.evaluate("[...document.querySelectorAll('.tree .r em.jcol3')].map(e => e.textContent).join('')")
    R.ck(G, '1a', '✏' not in t and '🔗' not in t, '줄 끝 ✏️·🔗 글자 %d·%d' % (t.count('✏'), t.count('🔗')))
    ns = pg.evaluate("ks => ks.map(k => { const b = document.querySelector('.tree .r[data-jo=\"' + k + '\"] button.jck'); if (!b) return null; const n = b.querySelector('.jckn'); return n ? +n.textContent : 0; })", Q15)
    R.ck(G, '1b', ns == Q15N, '제1~15조 정오문제 수 %s' % ns)
    # 체크 → 팔레트 → 빨
    ok = pg.evaluate("() => !!document.querySelector('.tree .r[data-jo=\"제6조\"] button.jck')")
    if ok:
        pg.click('.tree .r[data-jo="제6조"] button.jck')
        pg.wait_for_timeout(200)
    pal = pg.evaluate("() => { const p = document.querySelector('.jckpal'); return p ? {rc: __rc(p), sw: p.querySelectorAll('.jcksw').length, clr: !!p.querySelector('.jckclr')} : null; }")
    inside = bool(pal) and pal['rc'][0] >= 0 and pal['rc'][1] >= 0 and pal['rc'][2] <= PC['width'] and pal['rc'][3] <= PC['height']
    R.ck(G, '1c', bool(pal) and pal['sw'] == 6 and pal['clr'] and inside, '팔레트 %s' % pal)
    if pal:
        pg.click('.jckpal .jcksw[data-ck="빨"]')
        idle(pg)
    st = pg.evaluate("() => { const b = document.querySelector('.tree .r[data-jo=\"제6조\"] button.jck'); const r = b && b.querySelector('rect'); return {jo: S.jo, fill: r ? r.getAttribute('fill') : null, ck: localStorage.getItem('jopangi.jocheck')}; }")
    ck = json.loads(st['ck'] or '{}')
    R.ck(G, '1d', st['jo'] == '제1조' and st['fill'] == '#dc2626' and ck == {'특허법:제6조': '빨'}, '빨 칠함 · S.jo=%s · 아이콘 %s · jocheck %s' % (st['jo'], st['fill'], ck))
    pg.evaluate("stampAll()")
    pg.reload()
    pg.wait_for_function("typeof S!=='undefined' && typeof busy!=='undefined' && !busy && document.querySelector('.tree .r')", timeout=60000)
    idle(pg, 400)
    f2 = pg.evaluate("() => { const b = document.querySelector('.tree .r[data-jo=\"제6조\"] button.jck'); const r = b && b.querySelector('rect'); return r ? r.getAttribute('fill') : null; }")
    R.ck(G, '1e', f2 == '#dc2626', '새로고침 뒤 %s' % f2)
    # 칩 목록
    has_chip = pg.evaluate("() => !!document.querySelector('.jtbar .jckf')")
    menu = []
    if has_chip:
        pg.click('.jtbar .jckf')
        pg.wait_for_timeout(200)
        menu = pg.evaluate("[...document.querySelectorAll('.jckmenu > *')].map(x => x.classList.contains('jckmsep') ? '—' : x.textContent.trim())")
    R.ck(G, '1f', menu == ['전체 268', '★ 2년 내 개정 12', '—', '빨강 1', '주황 0', '노랑 0', '초록 0', '파랑 0', '보라 0'], '칩 목록 %s' % menu)
    rows = []
    if menu:
        pg.click('.jckmenu .jckmo[data-flt="빨"]')
        idle(pg)
        rows = pg.evaluate("() => ({jo: [...document.querySelectorAll('.tree .r[data-jo]')].map(r => r.dataset.jo), chip: document.querySelector('.jtbar .jckf').textContent.trim(), step: (document.querySelector('.jtbar .jstep') || {}).disabled})")
    R.ck(G, '1g', bool(rows) and rows['jo'] == ['제6조'] and rows['chip'] == '빨강 1 ▾' and rows['step'] is True, '빨 거름 %s' % rows)
    if rows:
        pg.click('.jtbar .jckf')
        pg.wait_for_timeout(150)
        pg.click('.jckmenu .jckmo[data-flt="★"]')
        idle(pg)
    stp = pg.evaluate("() => ({chip: (document.querySelector('.jtbar .jckf') || {}).textContent, dis: (document.querySelector('.jtbar .jstep') || {}).disabled, n: document.querySelectorAll('.tree .r[data-jo]').length})")
    R.ck(G, '1h', stp.get('dis') is True and (stp.get('chip') or '').startswith('★ 2년 내 개정 12'), '★ 거름 중 접기 dis %s' % stp)
    if rows:
        pg.click('.jtbar .jckf')
        pg.wait_for_timeout(150)
        pg.click('.jckmenu .jckmo[data-flt=""]')
        idle(pg)
    seq = []
    for _ in range(3):
        if not pg.evaluate("() => !!document.querySelector('.jtbar .jstep')"):
            break
        tx = pg.evaluate("document.querySelector('.jtbar .jstep').textContent")
        pg.click('.jtbar .jstep')
        idle(pg)
        seq.append((tx, pg.evaluate("document.querySelectorAll('.tree .r').length")))
    R.ck(G, '1i', seq == [('접기1', 13), ('접기2', 260), ('펴기', 283)], '단계 접기 %s' % seq)
    # 절 머리 누름
    n0 = pg.evaluate("document.querySelectorAll('.tree .r').length")
    res = None
    if pg.evaluate("() => !!document.querySelector('.tree .r.jsub[data-hi=\"11\"]')"):
        pg.click('.tree .r.jsub[data-hi="11"]')
        idle(pg)
        a = pg.evaluate("[...document.querySelectorAll('.tree .r[data-jo]')].filter(r => /^제(19[2-8])조/.test(r.dataset.jo)).length")
        pg.click('.tree .r.jsub[data-hi="12"]')
        idle(pg)
        b_ = pg.evaluate("[...document.querySelectorAll('.tree .r[data-jo]')].filter(r => { const m = /^제(\\d+)조/.exec(r.dataset.jo); return m && +m[1] >= 192 && +m[1] <= 214; }).length")
        res = (n0, a, b_, pg.evaluate("document.querySelectorAll('.tree .r').length"), pg.evaluate("[...document.querySelectorAll('.tree .r.jsub')].map(r => r.textContent.slice(0, 2))"))
        pg.click('.tree .r.jsub[data-hi="11"]')
        idle(pg)
        pg.click('.tree .r.jsub[data-hi="12"]')
        idle(pg)
    R.ck(G, '1j', bool(res) and res[0] == 283 and res[1] == 0 and res[2] == 0 and res[3] == 260 and res[4] == ['▸ ', '▸ '], '절 머리 누름(283 → 제1절 접힘 → 제2절 접힘) %s' % (res,))
    # 조 번호 누름 = 원문 팝업 · 줄 나머지 = 이동
    pg.evaluate("document.querySelector('.tree .r[data-jo=\"제7조\"]').scrollIntoView({block: 'center'})")
    pg.click('.tree .r[data-jo="제7조"] .jno')
    try:
        pop_wait(pg, '제7조', 8000)
    except Exception:
        pass
    p1 = pg.evaluate("() => ({jo: S.jo, pops: POPS.map(p => (p.querySelector('.pt') || {}).textContent)})")
    pg.evaluate("closeAllPops(true)")
    pg.click('.tree .r[data-jo="제7조"] .jtt')
    idle(pg)
    p2 = pg.evaluate("S.jo")
    R.ck(G, '1k', p1['jo'] == '제1조' and any('제7조' in (t or '') for t in p1['pops']) and p2 == '제7조', '조 번호 = 팝업 %s · 줄 나머지 = 이동 %s' % (p1, p2))
    # 지우기 → 묘비
    pg.evaluate("document.querySelector('.tree .r[data-jo=\"제6조\"]').scrollIntoView({block: 'center'})")
    tomb = None
    if pg.evaluate("() => !!document.querySelector('.tree .r[data-jo=\"제6조\"] button.jck')"):
        pg.click('.tree .r[data-jo="제6조"] button.jck')
        pg.wait_for_timeout(150)
        if pg.evaluate("() => !!document.querySelector('.jckpal .jckclr')"):
            pg.click('.jckpal .jckclr')
            idle(pg)
        pg.evaluate("stampAll()")
        tomb = pg.evaluate("() => ({ck: localStorage.getItem('jopangi.jocheck'), gone: Object.keys(JSON.parse(localStorage.getItem('jopangi_sync_gone') || '{}')).filter(k => k.indexOf('jopangi.jocheck|') === 0)})")
    R.ck(G, '1l', bool(tomb) and json.loads(tomb['ck'] or '{}') == {} and tomb['gone'] == ['jopangi.jocheck|특허법:제6조'], '지우기 → 묘비 %s' % tomb)
    # 네 법 셈
    exp = law_counts()
    got = {}
    for law in LAWS:
        go_jo(pg, law, first_jo(law))
        c = {}
        for _ in range(4):
            if not pg.evaluate("() => !!document.querySelector('.jtbar .jstep')"):
                break
            tx = pg.evaluate("document.querySelector('.jtbar .jstep').textContent")
            if tx in c:
                break
            pg.click('.jtbar .jstep')
            idle(pg)
            c[tx] = pg.evaluate("document.querySelectorAll('.tree .r').length")
        got[law] = dict({'fold%d' % d: c.get('접기%d' % d) for d in (1, 2, 3) if d < 3 or '접기3' in c}, open=c.get('펴기'))   # ★ A-6(a) 9/30 — 깊이 셋(민소 편 층)이면 접기3 도
        R.note('%s 셈: lv1 %d · lv2 %d · 조 %d → 접기1 %s · 접기2 %s · 펴기 %s (자료 셈 %d · %d · %d)' % (
            law, exp[law]['lv1'], exp[law]['lv2'], exp[law]['jo'], got[law]['fold1'], got[law]['fold2'], got[law]['open'], exp[law]['fold1'], exp[law]['fold2'], exp[law]['open']))
    R.ck(G, '1m', all(got[l] == {k: v for k, v in exp[l].items() if k.startswith('fold') or k == 'open'} for l in LAWS), '네 법 접기 셈 = 자료 셈')
    R.ck(G, '1z', not errs, 'JS 오류 %s' % errs[:3])
    ctx.close()


def first_jo(law):
    L = json.load(open(os.path.join(DATA, 'jo_%s_목록.json' % law), encoding='utf-8'))
    return L['조'][0]['k']


# ─────────────── B-2 조문 팝업 원문 ───────────────
POPQ = r"""async ([law, k]) => {
  const p = POPS[POPS.length - 1]; const t = p.querySelector('.pb').textContent;
  const B = await get('jo_' + law + '_본문.json'); const o = wmOrig(B.조[k]).slice(1).join('');
  const nz = s => s.replace(/\s+/g, '');
  const bad = ['---', 'related', '#^', '#특허/', '🔗 링크한 항', '(요건)'].filter(x => t.indexOf(x) >= 0);
  if (/["“”] ?["“”]/.test(t)) bad.push('두 겹 따옴표');
  return {bad: bad, same: nz(t) === nz(o), tl: nz(t).length, ol: nz(o).length, rc: __rc(p)}; }"""


def b2(br, url, R, engine='chromium'):
    G = 'B2'
    errs = []
    if engine == 'chromium':
        ctx, pg = new_page(br, url, errs=errs)
        go_jo(pg, '특허법', '제1조')
        for k in ['제6조', '제2조', '제11조', '제55조', '제132조의17']:
            pg.evaluate("k => { closeAllPops(true); popJo('특허법', k, {clientX: 600, clientY: 300}, 1); }", k)
            pop_wait(pg, k)
            r = pg.evaluate(POPQ, ['특허법', k])
            R.ck(G, '2a-' + k, not r['bad'] and r['same'], '%s 팝업 볼트 찌꺼기 %s · 원문과 같음 %s (%d/%d자)' % (k, r['bad'], r['same'], r['tl'], r['ol']))
        # 본문 링크 「제55조제1항」
        go_jo(pg, '특허법', '제6조')
        pos = word_pos(pg, "document.querySelector('#slot .main .box')", '제55조제1항')
        pg.mouse.click(pos['x'], pos['y'])
        pop_wait(pg, '제55조')
        pg.wait_for_timeout(300)
        rc = pg.evaluate("__rc(POPS[POPS.length - 1])")
        R.ck(G, '2b', rc[1] >= 0 and rc[3] <= PC['height'] and rc[2] <= PC['width'], 'PC 제6조 본문 「제55조제1항」 → 창 %s (bottom ≤ 1043)' % rc)
        # 끌기 · 크기 조절
        hd = pg.evaluate("(() => { const p = POPS[POPS.length - 1]; const h = p.querySelector('.ph .pt').getBoundingClientRect(); return [h.left + 20, h.top + h.height / 2]; })()")
        before = pg.evaluate("__rc(POPS[POPS.length - 1])")
        pg.mouse.move(hd[0], hd[1])
        pg.mouse.down()
        pg.mouse.move(hd[0] - 150, hd[1] - 60, steps=6)
        pg.mouse.up()
        moved = pg.evaluate("__rc(POPS[POPS.length - 1])")
        rs = pg.evaluate("(() => { const s = POPS[POPS.length - 1].querySelector('.prsz'); if (!s) return null; const r = s.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; })()")
        sized = None
        if rs:
            pg.mouse.move(rs[0], rs[1])
            pg.mouse.down()
            pg.mouse.move(rs[0] + 60, rs[1] - 40, steps=6)
            pg.mouse.up()
            sized = pg.evaluate("__rc(POPS[POPS.length - 1])")
        R.ck(G, '2c', moved[0] == before[0] - 150 and moved[1] == before[1] - 60 and bool(sized) and (sized[2] - sized[0]) > (moved[2] - moved[0]),
             '끌기 %s → %s · 크기 조절 → %s' % (before, moved, sized))
        R.ck(G, '2z', not errs, 'JS 오류 %s' % errs[:3])
        ctx.close()
    # 폰
    errs2 = []
    ctx, pg = new_page(br, url, phone=True, errs=errs2)
    go_jo(pg, '특허법', '제6조', "S.treeHid=true;")
    pos = word_pos(pg, "document.querySelector('#slot .main .box')", '제55조제1항')
    pg.touchscreen.tap(pos['x'], pos['y'])
    pop_wait(pg, '제55조')
    pg.wait_for_timeout(300)
    r = pg.evaluate("""(() => { const p = POPS[POPS.length - 1]; const x = [...p.querySelectorAll(':scope > .ph > button')].find(b => b.textContent.trim() === '✕');
      const xr = x ? x.getBoundingClientRect() : null; const hit = xr ? document.elementFromPoint(xr.left + xr.width / 2, xr.top + xr.height / 2) : null;
      return {rc: __rc(p), w: Math.round(p.getBoundingClientRect().width), x: xr ? __rc(x) : null, xhit: !!(hit && x && (hit === x || x.contains(hit)))}; })()""")
    rc = r['rc']
    R.ck(G, '2d' + ('' if engine == 'chromium' else '-wk'), abs(r['w'] - (PHONE['width'] - 16)) <= 1 and rc[0] >= 0 and rc[1] >= 0 and rc[2] <= PHONE['width'] and rc[3] <= PHONE['height'] and r['xhit'],
         '폰(%s) 창 폭 %d · 자리 %s · ✕ %s 보임 %s' % (engine, r['w'], rc, r['x'], r['xhit']))
    t = pg.evaluate(POPQ, ['특허법', '제55조'])
    R.ck(G, '2e' + ('' if engine == 'chromium' else '-wk'), not t['bad'] and t['same'], '폰(%s) 제55조 팝업 원문 %s %s' % (engine, t['bad'], t['same']))
    R.ck(G, '2y' + ('' if engine == 'chromium' else '-wk'), not errs2, 'JS 오류(폰) %s' % errs2[:3])
    ctx.close()


# ─────────────── B-3 연결 줄 ───────────────
def b3(br, url, R):
    G = 'B3'
    errs = []
    ctx, pg = new_page(br, url, errs=errs)
    go_jo(pg, '특허법', '제6조')
    ch = pg.evaluate("[...document.querySelectorAll('#slot .conn')][0].textContent")
    R.ck(G, '3a', '🔗인2' in ch and '↩피3' in ch and '📜' not in ch, '제6조 연결 줄 「%s」' % ch)
    li = None
    if pg.evaluate("() => !!document.querySelector('#slot .conn .plgb.wmin')"):
        pg.click('#slot .conn .plgb.wmin')
        idle(pg, 400)
        li = pg.evaluate("(() => { const p = wmWinOf('ci'); return p ? {t: p.querySelector('.pt').textContent, j: [...p.querySelectorAll('.ci')].map(c => c.dataset.jo)} : null; })()")
    R.ck(G, '3b', bool(li) and li['j'] == ['제55조', '제132조의17'] and li['t'].startswith('🔗 인용 2 · 제6조 본문이 적은 조'), '🔗 목록 %s' % li)
    lp = None
    if li:
        pg.click('#slot .conn .plgb.wmpi')
        idle(pg, 400)
        lp = pg.evaluate("(() => { const p = wmWinOf('ci'); return p ? {t: p.querySelector('.pt').textContent, j: [...p.querySelectorAll('.ci')].map(c => c.dataset.jo), f: (p.querySelector('.wmft') || {}).textContent} : null; })()")
    R.ck(G, '3c', bool(lp) and lp['j'] == ['제132조의5', '제141조', '제46조'] and lp['t'].startswith('↩ 피인용 3 · 본문에 「제6조」를 적은 조'), '↩ 목록 %s' % lp)
    af = None
    if lp:
        pg.click('.wm-ci .ci[data-jo="제46조"]')
        pop_wait(pg, '제46조')
        af = pg.evaluate("({jo: S.jo, ci: !!wmWinOf('ci'), top: (POPS[POPS.length - 1].querySelector('.pt') || {}).textContent})")
        t = pg.evaluate(POPQ, ['특허법', '제46조'])
        af['orig'] = t['same'] and not t['bad']
    R.ck(G, '3d', bool(af) and af['jo'] == '제6조' and af['ci'] and '제46조' in af['top'] and af['orig'], '항목 누름 = 원문 팝업 · S.jo 무변 · 목록 창 남음 %s' % af)
    go_jo(pg, '특허법', '제1조', "S.ciWin='';")
    z = pg.evaluate("[...document.querySelectorAll('#slot .conn .plgb.wmci')].map(b => [b.textContent, b.classList.contains('wait'), getComputedStyle(b).opacity])")
    R.ck(G, '3e', bool(z) and z[0][0] == '🔗인0' and z[0][1] and float(z[0][2]) < 0.6, '🔗인 0 조(제1조) 흐림 %s' % z)
    R.note('꼬리 줄(↩ 창) = %s' % ((lp or {}).get('f')))
    R.ck(G, '3z', not errs, 'JS 오류 %s' % errs[:3])
    ctx.close()


# ─────────────── B-4 모드 줄 ───────────────
def b4(br, url, R, src):
    G = 'B4'
    errs = []
    ctx, pg = new_page(br, url, ui={'trw': 276, 'jbs': 1}, errs=errs)   # 옛 jbs(★ 중요 빈칸만 켬) 값이 남은 기기
    go_jo(pg, '특허법', '제6조')
    r = pg.evaluate("""(() => { const m = document.querySelector('#slot .main');
      const its = [...m.querySelectorAll('.jomt button')].map(b => ({t: b.textContent.trim(), c: getComputedStyle(b).color, fs: getComputedStyle(b).fontSize, fw: getComputedStyle(b).fontWeight, k: b.dataset.bk || ''}));
      return {pill: m.querySelectorAll('.modebar, .modebar .mode, button.mode').length, its: its, txt: m.textContent}; })()""")
    R.ck(G, '4a', r['pill'] == 0 and len(r['its']) >= 5, '알약·상자 %d · 글자 %s' % (r['pill'], [x['t'] for x in r['its']]))
    fsok = bool(r['its']) and all(x['fs'] == '11px' and x['fw'] == '800' for x in r['its'])
    colok = all(any(x['k'] == k and x['c'] == c for x in r['its']) for k, c in BK.items())
    R.ck(G, '4b', fsok and colok, '11px 800 %s · 색 셋 = BK_COLOR %s' % (fsok, colok))
    R.ck(G, '4c', '소제목만' not in r['txt'] and '중요 빈칸만' not in r['txt'] and 'bkImportant' not in src and 'joBlankStar' not in src,
         '「소제목만」·「중요 빈칸만」 화면 0 · bkImportant %d · joBlankStar %d (소스)' % (src.count('bkImportant'), src.count('joBlankStar')))
    n_in = None
    if pg.evaluate("() => !!document.querySelector('.jomt button[data-bk=\"내용\"]')"):
        pg.click('.jomt button[data-bk="내용"]')
        idle(pg, 300)
        n_in = pg.evaluate("document.querySelectorAll('#slot .main input.bkin').length")
    R.ck(G, '4d', bool(n_in) and n_in == 12, '빈칸 모드(내용) 제6조 input %s (옛 「중요 아님」 조 · 옛 jbs=1 기기)' % n_in)
    mul = None
    if n_in is not None:
        pg.click('.jomt button[data-bk="주체"]')
        idle(pg, 300)
        mul = pg.evaluate("""(() => ({on: [...document.querySelectorAll('.jomt button.on')].map(b => b.textContent.trim()), jb: S.joBlank, n: document.querySelectorAll('#slot .main input.bkin').length,
          ul: [...document.querySelectorAll('.jomt button.on')].map(b => { const s = getComputedStyle(b); return s.textDecorationLine + '/' + s.textDecorationThickness; }),
          mk: (() => { const b = [...document.querySelectorAll('.jomt button')].find(x => x.textContent.indexOf('마크업') >= 0); return b ? [b.disabled, getComputedStyle(b).opacity] : null; })() }))()""")
    R.ck(G, '4e', bool(mul) and mul['jb'] == {'내용': True, '주체': True, '기간': False} and mul['n'] == 13 and all(u.startswith('underline/2px') for u in mul['ul']) and mul['mk'] and mul['mk'][0],
         '다중선택 %s' % mul)
    wk = None
    if mul:
        pg.click('.jomt button[data-bk="내용"]')
        idle(pg)
        pg.click('.jomt button[data-bk="주체"]')
        idle(pg)
        pg.evaluate("[...document.querySelectorAll('.jomt button')].find(x => x.textContent.indexOf('마크업') >= 0).click()")
        idle(pg, 400)
        w1 = pg.evaluate("!!document.querySelector('.pop.wm-mk')")
        pg.evaluate("[...document.querySelectorAll('.jomt button')].find(x => x.textContent.indexOf('마크업') >= 0).click()")
        idle(pg, 300)
        w2 = pg.evaluate("!!document.querySelector('.pop.wm-mk')")
        wk = (w1, w2, pg.evaluate("[...document.querySelectorAll('.jomt button.on')].map(b => b.textContent.trim())"))
    R.ck(G, '4f', bool(wk) and wk[0] and not wk[1] and wk[2] == ['본문'], '마크업 창 열고 닫기 · 본문 켜짐 %s' % (wk,))
    R.ck(G, '4z', not errs, 'JS 오류 %s' % errs[:3])
    ctx.close()


# ─────────────── B-5 길게 누르기 ───────────────
def b5(br, url, R, engine='chromium'):
    G = 'B5'
    sfx = '' if engine == 'chromium' else '-wk'
    errs = []
    ctx, pg = new_page(br, url, phone=True, errs=errs)
    go_jo(pg, '특허법', '제6조', "S.treeHid=true;")
    box = "document.querySelector('#slot .main .box')"
    pos = word_pos(pg, box, '대리인')
    touch_long(ctx, pg, pos['x'], pos['y'])
    q = pg.evaluate(BARQ)
    bar = q['bars'][0] if len(q['bars']) == 1 else None
    R.ck(G, '5a' + sfx, q['pit'] == 0 and bool(bar) and bar['id'] == 'jomk9' and bar['paint'] == 9 and bar['row2'] == ['🗒 메모', '✎ 수정', '🏷 태그'],
         '조문 「대리인」 700ms: .pitmenu %d · 막대 %s' % (q['pit'], q['bars']))
    R.ck(G, '5b' + sfx, bool(bar) and bool(q['selRect']) and bar['rect'][1] >= q['selRect'][3], '막대 %s 선택 %s 아래' % (bar and bar['rect'], q['selRect']))
    memo = None
    if bar and tap_sel(pg, '#jomk9 .mk9r2 button[data-pit="memo"]'):
        pg.wait_for_timeout(400)
        memo = pg.evaluate("POPS.map(p => (p.querySelector('.pt') || {}).textContent)")
    R.ck(G, '5c' + sfx, bool(memo) and any('「대리인은」' in (t or '') for t in memo), '🗒 메모 → %s' % memo)
    go_jo(pg, '특허법', '제6조', "S.treeHid=true;")
    pos = word_pos(pg, box, '대리인')
    touch_long(ctx, pg, pos['x'], pos['y'])
    ed = None
    if tap_sel(pg, '#jomk9 .mk9r2 button[data-pit="edit"]'):
        pg.wait_for_timeout(400)
        ed = pg.evaluate("[...document.querySelectorAll('#slot .main .eqedit textarea')].map(t => t.value.slice(0, 20))")
    R.ck(G, '5d' + sfx, bool(ed) and ed[0].startswith('국내에 주소'), '✎ 수정 → 수정 칸 %s' % ed)
    go_jo(pg, '특허법', '제6조', "S.treeHid=true;")
    pos = word_pos(pg, box, '대리인')
    touch_long(ctx, pg, pos['x'], pos['y'])
    pg.evaluate("window.__toasts = []")
    tg1 = None
    if tap_sel(pg, '#jomk9 .mk9r2 button[data-tag]'):
        pg.wait_for_timeout(400)
        tg1 = pg.evaluate("({pops: POPS.map(p => (p.querySelector('.pt') || {}).textContent), toasts: window.__toasts.slice()})")
    go_jo(pg, '특허법', '제6조', "S.treeHid=true;")
    pos = word_pos(pg, box, '국내에')
    touch_long(ctx, pg, pos['x'], pos['y'])
    tg2 = None
    if tap_sel(pg, '#jomk9 .mk9r2 button[data-tag]'):
        pg.wait_for_timeout(400)
        tg2 = pg.evaluate("POPS.map(p => (p.querySelector('.pt') || {}).textContent)")
    R.ck(G, '5e' + sfx, bool(tg1) and any('걸쳐서 겹친다' in t for t in tg1['toasts']) and bool(tg2) and any('선택한 글에 붙이기' in (t or '') for t in tg2),
         '🏷 태그: 「대리인은」 = 겹침 막음 toast %s · 「국내에」 = 스티커 창 %s' % (tg1 and tg1['toasts'], tg2))
    # 기본 선택이 먼저
    go_jo(pg, '특허법', '제6조', "S.treeHid=true;")
    pos = word_pos(pg, box, '대리인')
    touch_long(ctx, pg, pos['x'], pos['y'], mid=lambda: pg.evaluate("() => { const r = __findText(document.querySelector('#slot .main .box'), '대리인은'); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }"))
    q = pg.evaluate(BARQ)
    R.ck(G, '5f' + sfx, q['pit'] == 0 and len(q['bars']) == 1 and q['bars'][0]['id'] == 'jomk9', '폰 기본 선택이 먼저: .pitmenu %d · 막대 %s' % (q['pit'], [b['id'] for b in q['bars']]))
    # 조문 팝업 본문
    pg.evaluate("getSelection().removeAllRanges(); closeAllPops(true); popJo('특허법', '제6조', {clientX: 20, clientY: 120}, 1)")
    pop_wait(pg, '제6조')
    pos = word_pos(pg, "POPS[POPS.length - 1].querySelector('.pb')", '특별히')
    touch_long(ctx, pg, pos['x'], pos['y'])
    q = pg.evaluate(BARQ)
    R.ck(G, '5g' + sfx, q['pit'] == 0 and len(q['bars']) == 1 and q['bars'][0]['id'] == 'jomk9' and q['bars'][0]['paint'] == 9 and len(q['bars'][0]['row2']) == 3,
         '조문 팝업 본문 「특별히」: .pitmenu %d · 막대 %s' % (q['pit'], q['bars']))
    pg.evaluate("getSelection().removeAllRanges(); closeAllPops(true);")
    # 1차객 카드(정오문제 창 · mlnLidCard)
    go_jo(pg, '특허법', '제6조', "S.treeHid=true; S.joPanel=true;")
    pg.wait_for_function("() => document.querySelector('.wm-jp [data-mk]') && [...document.querySelectorAll('.wm-jp [data-mk]')].some(h => h._pitInfo)", timeout=60000)
    pos = pg.evaluate("() => { const h = [...document.querySelectorAll('.wm-jp [data-mk]')].find(x => x._pitInfo); h.scrollIntoView({block: 'center'}); const r = __findText(h, '영업소가'); return r ? __rectOf(r) : null; }")
    q = None
    if pos:
        touch_long(ctx, pg, pos['x'], pos['y'])
        q = pg.evaluate(BARQ)
    R.ck(G, '5h' + sfx, bool(q) and q['pit'] == 0 and len(q['bars']) == 1 and q['bars'][0]['id'] == 'mkc9' and q['bars'][0]['paint'] == 9 and q['bars'][0]['row2'] == ['🗒 메모', '✎ 수정'] and q['bars'][0]['rect'][1] >= q['selRect'][3],
         '1차객 카드: %s' % (q and {'pit': q['pit'], 'bars': q['bars'], 'sel': q['sel']}))
    pg.evaluate("getSelection().removeAllRanges(); closeAllPops(true); S.joPanel=false;")
    # 2차 문제 창(⑦ 팝업 · renderBody mark)
    pg.evaluate("""async () => { const B2 = await get('2cha_본문_기출_특허.json'); for (const f of Object.keys(B2)){ const co = (B2[f].행 || []).find(r => r.co === 'question' && r.rows && r.rows.length); if (co){ popCallout(co, f, {clientX: 20, clientY: 120}, '기출', 0); break; } } }""")
    pg.wait_for_function("() => document.querySelector('.pop [data-c2mark]')", timeout=30000)
    pg.wait_for_timeout(300)
    pos = pg.evaluate("() => { const h = [...document.querySelectorAll('.pop [data-c2mark]')].find(x => /[가-힣]{3,}/.test(x.textContent)); h.scrollIntoView({block: 'center'}); const m = /[가-힣]{3,}/.exec(h.textContent); const r = __findText(h, m[0]); return Object.assign(__rectOf(r), {w: m[0]}); }")
    touch_long(ctx, pg, pos['x'], pos['y'])
    q = pg.evaluate(BARQ)
    R.ck(G, '5i' + sfx, q['pit'] == 0 and len(q['bars']) == 1 and q['bars'][0]['id'] == 'c2mark' and q['bars'][0]['paint'] == 9 and q['bars'][0]['row2'] == ['🗒 메모', '✎ 수정'] and q['bars'][0]['rect'][1] >= q['selRect'][3],
         '2차 문제 창 「%s」: %s' % (pos['w'], {'pit': q['pit'], 'bars': q['bars']}))
    pg.evaluate("getSelection().removeAllRanges(); closeAllPops(true);")
    # 판례 줄 = pitmenu 그대로
    pg.evaluate("""async () => { const SUM = await get(PF('요약')); const id = Object.keys(SUM).find(k => SUM[k] && SUM[k].행 && SUM[k].행.filter(r => (r.t || '').trim().length > 10).length > 3); S.tab = 'prec'; S.prec = id; S.precTab = '요약'; S.listHid = true; S.treeHid = true; render(); }""")
    idle(pg, 500)
    pg.wait_for_function("() => [...document.querySelectorAll('#slot .main .box .ln')].some(l => l._pitInfo)", timeout=30000)
    pos = pg.evaluate("() => { const l = [...document.querySelectorAll('#slot .main .box .ln')].find(x => x._pitInfo && /[가-힣]{3,}/.test(x.textContent)); l.scrollIntoView({block: 'center'}); const m = /[가-힣]{3,}/.exec(l.textContent); const r = __findText(l, m[0]); return Object.assign(__rectOf(r), {w: m[0], t: l._pitInfo.target}); }")
    if engine == 'chromium':
        cdp = ctx.new_cdp_session(pg)
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': pos['x'], 'y': pos['y']}]})
        pg.wait_for_timeout(700)
        q = pg.evaluate(BARQ)
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    else:   # 합치기(9/29) — WebKit 은 합성 touch 포인터(touch_long 과 같은 길)
        pg.evaluate(WK_LONG, [pos['x'], pos['y'], 'pointerdown'])
        pg.wait_for_timeout(700)
        q = pg.evaluate(BARQ)
        pg.evaluate(WK_LONG, [pos['x'], pos['y'], 'pointerup'])
    R.ck(G, '5j' + sfx, q['pit'] == 1 and not q['bars'], '판례 줄(%s 「%s」) 길게 누르기 = .pitmenu %d %s · 막대 %d' % (pos['t'], pos['w'], q['pit'], q['pitText'], len(q['bars'])))
    R.ck(G, '5z' + sfx, not errs, 'JS 오류 %s' % errs[:3])
    ctx.close()


# ─────────────── B-6 3법 카드 ───────────────
def b6(br, url, R):
    G = 'B6'
    errs = []
    ctx, pg = new_page(br, url, errs=errs)
    go_jo(pg, '특허법', '제6조', "uiThToggle('c3', true);")
    pg.wait_for_function("() => document.querySelectorAll('.thwrap.c3 .thcol .bj2').length >= 3", timeout=30000)
    cards = pg.evaluate("""[...document.querySelectorAll('.thwrap.c3 .thcol')].filter(c => c.querySelector('.bj2')).map(c => {
      const words = []; let gi = 0; c.querySelector('.bj2').querySelectorAll(':scope > div').forEach((d, li) => { [...d.childNodes].forEach(n => { const t = n.textContent; if (!t.trim()) return;
        const cls = n.nodeType === 1 ? n.className : ''; t.trim().split(/\\s+/).forEach(w => { words.push([gi++, w, cls]); }); }); });
      return {h: c.querySelector('.thhd').textContent, t: c.querySelector('.bj2').textContent, red: words.filter(w => w[2] === 'c3red').map(w => w[0] + ':' + w[1]), dim: words.filter(w => w[2] === 'c3dim').map(w => w[0] + ':' + w[1])}; })""")
    k6 = next((c for c in cards if c['h'].startswith('특허') and '제6조' in c['h']), None)
    t7 = next((c for c in cards if c['h'].startswith('상표') and '제7조' in c['h']), None)
    R.ck(G, '6a', bool(k6) and '---' not in k6['t'] and '<개정' not in k6['t'] and 'related' not in k6['t'], '특허 제6조 카드 --- %s · 개정 꼬리표 %s' % (k6 and k6['t'].count('---'), k6 and k6['t'].count('<개정')))
    R.ck(G, '6b', bool(t7) and t7['t'].count('(이하 "상표등록출원"이라 한다)') == 1 and not re.search(r'["“”] ?["“”]', t7['t']),
         '상표 제7조 카드 「(이하 "상표등록출원"이라 한다)」 %s벌' % (t7 and t7['t'].count('(이하 "상표등록출원"이라 한다)')))
    for c in cards:
        R.note('3법 카드 %s: c3red %d %s · c3dim %d %s' % (c['h'], len(c['red']), c['red'], len(c['dim']), c['dim']))
    # 제목 누름 = 원문 팝업
    ok_t = None
    if t7:
        pg.evaluate("[...document.querySelectorAll('.thwrap.c3 .thcol .thhd b')].find(b => b.textContent === '제7조' && b.closest('.thcol').querySelector('.thhd').textContent.startsWith('상표')).click()")
        pop_wait(pg, '제7조')
        tt = pg.evaluate(POPQ, ['상표법', '제7조'])
        ok_t = tt['same'] and not tt['bad']
    R.ck(G, '6c', bool(ok_t), '상표 제7조 카드 제목 누름 = 원문 팝업 %s' % ok_t)
    # 「다만,」 새 줄
    go_jo(pg, '특허법', '제11조', "uiThToggle('c3', true);")
    pg.wait_for_function("() => document.querySelectorAll('.thwrap.c3 .thcol .bj2').length >= 1", timeout=30000)
    dm = pg.evaluate("[...document.querySelectorAll('.thwrap.c3 .thcol')].filter(c => c.querySelector('.bj2')).map(c => [c.querySelector('.thhd').textContent, c.querySelectorAll('.bj2 .dmn.dmnbr').length, c.querySelector('.bj2').textContent.indexOf('다만,') >= 0])")
    R.ck(G, '6d', bool(dm) and dm[0][1] >= 1 and all((x[1] >= 1) == x[2] for x in dm), '「다만,」 새 줄(특허 제11조 3법) %s' % dm)
    pg.evaluate("uiThToggle('', true)")
    R.ck(G, '6z', not errs, 'JS 오류 %s' % errs[:3])
    ctx.close()


# ─────────────── B-7 원문 보기 설명 글 ───────────────
def b7(br, url, R, src):
    G = 'B7'
    errs = []
    ctx, pg = new_page(br, url, errs=errs)
    go_jo(pg, '특허법', '제6조')
    pg.click('#slot .main .box.fold')
    pop_wait(pg, '원문')
    n1 = pg.evaluate("[...document.querySelectorAll('.bjnote')].filter(x => x.offsetParent && x.getClientRects().length).length")
    pg1 = pg.evaluate("!!document.querySelector('.pop .origbody .bjwrap .bjline')")
    R.ck(G, '7a', n1 == 0 and pg1, '떠 있는 원문 창 .bjnote 보임 %d · 조판 %s' % (n1, pg1))
    ctx.close()
    ink = {'jo|특허법:제6조': {'s': [{'c': '#D93B3B', 'w': 2, 'p': [[0.1, 0.1, 1], [0.2, 0.15, 1]]}], 'ts': '2026-09-29T00:00:00.000Z'}}
    ctx, pg = new_page(br, url, ls={'jopangi.ink': ink}, errs=errs)
    go_jo(pg, '특허법', '제6조')
    r = pg.evaluate("({lock: !!([...document.querySelectorAll('#slot .main .box.fold .badge')].find(b => b.textContent.indexOf('필기 때문에') >= 0)), n: [...document.querySelectorAll('.bjnote')].filter(x => x.offsetParent && x.getClientRects().length).length, page: !!document.querySelector('#slot .main .box.fold .origbody .bjwrap .bjline')})")
    R.ck(G, '7b', r['lock'] and r['page'] and r['n'] == 0, '필기로 잠긴 펼침 %s' % r)
    ok = False
    i = src.find(BJNOTE)
    while i >= 0:
        if src.rfind('/*', 0, i) > src.rfind('*/', 0, i):
            ok = True
            break
        i = src.find(BJNOTE, i + 1)
    R.ck(G, '7c', ok and ("el('div','bjnote'" not in src), '소스 주석에 문장 %s · bjnote 만드는 줄 %d' % (ok, src.count("el('div','bjnote'")))
    R.ck(G, '7z', not errs, 'JS 오류 %s' % errs[:3])
    ctx.close()


# ─────────────── 회귀 R(이 저장소 안에서 돌릴 수 있는 것) ───────────────
def regress(br, url, R, src, base_src):
    G = 'R'
    errs = []
    ctx, pg = new_page(br, url, errs=errs)
    # R1 네 법 조문 화면
    r1 = []
    for law in LAWS:
        ks = pg.evaluate("async l => { const L = await get('jo_' + l + '_목록.json'); const a = L.조; return [a[0].k, a[Math.floor(a.length / 2)].k, a[a.length - 1].k]; }", law)
        for k in ks:
            go_jo(pg, law, k)
            r1.append(pg.evaluate("k => ({k: k, t: (document.querySelector('#slot .main .jotitle') || {}).textContent || '', body: document.querySelectorAll('#slot .main .box .ln').length, jck: document.querySelectorAll('.tree button.jck').length})", k))
    R.ck(G, 'R1', all(x['t'].startswith(x['k']) and x['jck'] > 0 for x in r1) and not errs, '네 법 조문 화면(처음·가운데·끝 조) %s · 오류 %s' % ([(x['k'], x['body'], x['jck']) for x in r1], errs[:2]))
    # R2 탭 순회
    tabs = []
    for tb in ['prec', 'jimun', 'cha2', 'omr', 'jo']:
        pg.evaluate("t => { closeAllPops(true); S.law = '특허법'; S.tab = t; render(); }", tb)
        idle(pg, 600)
        tabs.append((tb, pg.evaluate("document.querySelector('#slot').children.length")))
    R.ck(G, 'R2', all(n > 0 for _, n in tabs) and not errs, '탭 순회 %s · 오류 %s' % (tabs, errs[:2]))
    # R3 동기화 jo
    old = re.search(r"const SYNC_KEYS = \[(.*?)\]", base_src, re.S)
    old_keys = re.findall(r"'([^']+)'", old.group(1)) if old else []
    sk = pg.evaluate("SYNC_KEYS.slice()")
    mg = pg.evaluate("""() => {
      localStorage.removeItem('jopangi.jocheck'); stampAll();
      const T = Date.now() + 5000;
      const r1 = recMerge({u: {'jopangi.jocheck|상표법:제7조': T}, gone: {}, data: {'jopangi.jocheck': {'상표법:제7조': '파'}}});
      const a = JSON.parse(localStorage.getItem('jopangi.jocheck') || '{}');
      const r2 = recMerge({u: {}, gone: {'jopangi.jocheck|상표법:제7조': T + 1000}, data: {'jopangi.jocheck': {}}});
      const b = JSON.parse(localStorage.getItem('jopangi.jocheck') || '{}');
      jckPut('특허법', '제9조', '초'); stampAll();
      const pl = recPayload(); const inPl = pl.data['jopangi.jocheck'];
      const lab = recLabel('jopangi.jocheck');
      jckPut('특허법', '제9조', ''); stampAll();
      return {r1: r1, a: a, r2: r2, b: b, inPl: inPl, lab: lab}; }""")
    R.ck(G, 'R3', all(('jopangi.' + k) in sk for k in old_keys) and sk[-1] == 'jopangi.jocheck' and len(sk) == len(old_keys) + 1
         and mg['a'] == {'상표법:제7조': '파'} and mg['b'] == {} and mg['inPl'] == {'특허법:제9조': '초'} and mg['lab'] == '☑ 조 체크 색',
         '동기화: 키 %d → %d(끝 jocheck) · 원격 칸 받음 %s · 원격 묘비 지움 %s · 올릴 data %s · 이름 %s' % (len(old_keys), len(sk), mg['a'], mg['b'], mg['inPl'], mg['lab']))
    # R4 마크업 창 켜기 → 본문에 얹힘
    go_jo(pg, '특허법', '제55조', "S.mkWin=true;")
    pg.wait_for_function("() => document.querySelector('.pop.wm-mk .sh')", timeout=20000)
    b0 = pg.evaluate("document.querySelector('#slot .main .box').textContent.indexOf('(요건)')")
    pg.evaluate("[...document.querySelectorAll('.pop.wm-mk .sh')].find(s => s.dataset.sub === '항 소제목').querySelector('button.tx:not(.g)').click()")
    idle(pg, 300)
    b1_ = pg.evaluate("document.querySelector('#slot .main .box').textContent.indexOf('(요건)')")
    mk = pg.evaluate("localStorage.getItem('jopangi.mkon')")
    pg.evaluate("wmAll(WMX, false)")
    idle(pg, 200)
    pg.evaluate("S.mkWin=false; closeAllPops(true); render();")
    idle(pg)
    R.ck(G, 'R4', b0 < 0 and b1_ >= 0 and bool(mk) and '항 소제목' in mk, '마크업 창 「항 소제목 켜기」 → 본문 (요건) %d→%d · mkon %s' % (b0, b1_, (mk or '')[:60]))
    # R5 조문 칠(PC 끌어 고르기 → 막대 → 노랑)
    go_jo(pg, '특허법', '제6조')
    pos = word_pos(pg, "document.querySelector('#slot .main .box')", '특허관리인')
    pg.evaluate("() => { const r = __findText(document.querySelector('#slot .main .box'), '특허관리인'); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }")
    pg.mouse.move(pos['x'], pos['y'])
    pg.mouse.up()
    pg.wait_for_timeout(250)
    q = pg.evaluate(BARQ)
    painted = None
    if q['bars'] and q['bars'][0]['id'] == 'jomk9':
        pg.click('#jomk9 button[data-m="y"]')
        pg.wait_for_timeout(250)
        painted = pg.evaluate("({jm: localStorage.getItem('jopangi.jomark'), n: document.querySelectorAll('#slot .main .box span.jmk').length})")
        pg.evaluate("localStorage.removeItem('jopangi.jomark'); render();")
        idle(pg)
    R.ck(G, 'R5', bool(painted) and '"y"' in (painted['jm'] or '') and painted['n'] >= 5, '조문 칠(PC) 막대 %s → %s' % ([b['id'] for b in q['bars']], painted))
    # R6 1차객 형광펜
    go_jo(pg, '특허법', '제6조', "S.joPanel=true;")
    pg.wait_for_function("() => [...document.querySelectorAll('.wm-jp [data-mk]')].some(h => h._pitInfo)", timeout=60000)
    pg.evaluate("() => { const h = [...document.querySelectorAll('.wm-jp [data-mk]')].find(x => x._pitInfo); const r = __findText(h, '영업소가'); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }")
    pg.wait_for_timeout(300)
    q = pg.evaluate(BARQ)
    m6 = None
    if q['bars'] and q['bars'][0]['id'] == 'mkc9':
        pg.click('#mkc9 button[data-m="g"]')
        pg.wait_for_timeout(250)
        m6 = pg.evaluate("({mk: Object.keys(JSON.parse(localStorage.getItem('jopangi.markup') || '{}')).length, n: document.querySelectorAll('.wm-jp mark.mkc').length})")
    pg.evaluate("S.joPanel=false; closeAllPops(true); render();")
    idle(pg)
    R.ck(G, 'R6', bool(m6) and m6['mk'] >= 1 and m6['n'] >= 1, '1차객 형광펜 막대 %s → %s' % ([b['id'] for b in q['bars']], m6))
    # R7 2차 문제 창 형광펜
    pg.evaluate("""async () => { const B2 = await get('2cha_본문_기출_특허.json'); for (const f of Object.keys(B2)){ const co = (B2[f].행 || []).find(r => r.co === 'question' && r.rows && r.rows.length); if (co){ popCallout(co, f, {clientX: 20, clientY: 120}, '기출', 0); break; } } }""")
    pg.wait_for_function("() => document.querySelector('.pop [data-c2mark]')", timeout=30000)
    pg.evaluate("() => { const h = [...document.querySelectorAll('.pop [data-c2mark]')].find(x => /[가-힣]{3,}/.test(x.textContent)); const m = /[가-힣]{3,}/.exec(h.textContent); const r = __findText(h, m[0]); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }")
    pg.wait_for_timeout(450)
    q = pg.evaluate(BARQ)
    m7 = None
    if q['bars'] and q['bars'][0]['id'] == 'c2mark':
        pg.click('#c2mark button[data-m="b"]')
        pg.wait_for_timeout(250)
        m7 = pg.evaluate("({c2: Object.keys(JSON.parse(localStorage.getItem('jopangi.c2mark') || '{}')).length, n: document.querySelectorAll('.pop span.c2mk').length})")
    pg.evaluate("closeAllPops(true)")
    R.ck(G, 'R7', bool(m7) and m7['c2'] >= 1 and m7['n'] >= 1, '2차 문제 창 형광펜 막대 %s → %s' % ([b['id'] for b in q['bars']], m7))
    # R8 빈칸 채점
    go_jo(pg, '특허법', '제6조', "S.joBlank={내용:true,주체:false,기간:false};")
    r8 = pg.evaluate("""() => { const i = document.querySelector('#slot .main input.bkin'); i.value = i.dataset.ans; i.dispatchEvent(new Event('blur'));
      [...document.querySelectorAll('#slot .main .bkbar button')].find(b => b.textContent.indexOf('채점') >= 0).click();
      const v = JSON.parse(localStorage.getItem('jopangi.blank') || '{}')['특허법:제6조']; return v ? {n: v.n, r: v.r} : null; }""")
    pg.evaluate("S.joBlank={내용:false,주체:false,기간:false}; uiSave(); render();")
    idle(pg)
    R.ck(G, 'R8', bool(r8) and r8['n'] == 1, '빈칸 채점 → jopangi.blank %s' % r8)
    # R9 원문 보기 창 · 조판
    pg.click('#slot .main .box.fold')
    pop_wait(pg, '원문')
    r9 = pg.evaluate("({page: !!document.querySelector('.pop .origbody .bjwrap .bjline'), w: Math.round(POPS[POPS.length - 1].getBoundingClientRect().width)})")
    pg.evaluate("closeAllPops(true)")
    R.ck(G, 'R9', r9['page'], '원문 보기 창 %s' % r9)
    # R10 3법 카드 칸 길게 누르기(조·항 칸) · 카드 폭
    go_jo(pg, '특허법', '제6조', "uiThToggle('c3', true);")
    pg.wait_for_function("() => document.querySelectorAll('.thwrap.c3 .thcol .bj2').length >= 3", timeout=30000)
    w10 = pg.evaluate("[...document.querySelectorAll('.thwrap.c3 .thcol')].filter(c => c.querySelector('.bj2')).map(c => Math.round(c.getBoundingClientRect().width))")
    pg.evaluate("uiThToggle('', true); render();")
    idle(pg)
    R.ck(G, 'R10', bool(w10) and all(190 <= w <= 241 for w in w10), '3법 카드 폭 %s (240 고정 · 이 판 밖)' % w10)
    R.ck(G, 'Rz', not errs, 'JS 오류 %s' % errs[:3])
    ctx.close()
    # R11 폰 서랍: 체크 팔레트 누름이 서랍을 안 닫는다
    errs2 = []
    ctx, pg = new_page(br, url, phone=True, errs=errs2)
    go_jo(pg, '특허법', '제1조', "S.treeHid=false;")
    pg.evaluate("document.querySelector('.tree .r[data-jo=\"제3조\"]').scrollIntoView({block: 'center'})")
    r11 = None
    if tap_sel(pg, '.tree .r[data-jo="제3조"] button.jck'):
        pg.wait_for_timeout(250)
        pal = pg.evaluate("__rc(document.querySelector('.jckpal'))")
        tap_sel(pg, '.jckpal .jcksw[data-ck="파"]')
        idle(pg, 300)
        r11 = {'pal': pal, 'treeHid': pg.evaluate("S.treeHid"), 'ck': pg.evaluate("localStorage.getItem('jopangi.jocheck')"), 'jo': pg.evaluate("S.jo")}
    R.ck(G, 'R11', bool(r11) and r11['pal'] and r11['pal'][2] <= PHONE['width'] and r11['treeHid'] is False and json.loads(r11['ck'] or '{}') == {'특허법:제3조': '파'} and r11['jo'] == '제1조',
         '폰 서랍 팔레트 %s' % r11)
    R.ck(G, 'Ry', not errs2, 'JS 오류(폰) %s' % errs2[:3])
    ctx.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--html', default=os.path.join(ROOT, 'jo', 'index.html'))
    ap.add_argument('--base-html', default=None, help='회귀 R3 옛 SYNC_KEYS 대조용(기본 = --html 과 같은 파일에서 jocheck 를 뺀 것)')
    ap.add_argument('--yardstick', action='store_true', help='헛잣대 — B-1~B-7 이 저마다 FAIL 해야 통과')
    ap.add_argument('--webkit', action='store_true', help='터치 칸(B-2 폰 · B-5)을 WebKit 으로도')
    ap.add_argument('--only', default='')
    ap.add_argument('--no-regress', action='store_true')
    a = ap.parse_args()
    src = open(a.html, encoding='utf-8').read()
    base_src = open(a.base_html, encoding='utf-8').read() if a.base_html else src.replace(", 'jocheck']", "]")
    only = set(x.strip().upper() for x in a.only.split(',') if x.strip())
    httpd, url = serve(a.html)
    R_ = R()
    t0 = time.time()
    print('관문 _task_jo_joscreen0929 · %s · %s' % (os.path.relpath(a.html, ROOT) if a.html.startswith(ROOT) else a.html, url))
    with sync_playwright() as p:
        br = p.chromium.launch()
        steps = [('B1', lambda: b1(br, url, R_)), ('B2', lambda: b2(br, url, R_)), ('B3', lambda: b3(br, url, R_)), ('B4', lambda: b4(br, url, R_, src)),
                 ('B5', lambda: b5(br, url, R_)), ('B6', lambda: b6(br, url, R_)), ('B7', lambda: b7(br, url, R_, src))]
        if not a.no_regress and not a.yardstick:
            steps.append(('R', lambda: regress(br, url, R_, src, base_src)))
        for name, fn in steps:
            if only and name not in only:
                continue
            print('── %s' % name, flush=True)
            try:
                fn()
            except Exception as e:
                R_.ck(name, 'ERR', False, '돌다 멈춤: %s' % str(e).splitlines()[0][:300])
        br.close()
        if a.webkit and not a.yardstick:
            print('── WebKit(터치 칸 B-2 폰 · B-5)', flush=True)
            try:
                wk = p.webkit.launch()
            except Exception as e:
                wk = None
                R_.note('WebKit 안 잼 — 띄우지 못함: %s' % str(e).splitlines()[0][:200])
            if wk:
                for name, fn in [('B2', lambda: b2(wk, url, R_, 'webkit')), ('B5', lambda: b5(wk, url, R_, 'webkit'))]:
                    if only and name not in only:
                        continue
                    try:
                        fn()
                    except Exception as e:
                        R_.ck(name, 'ERR-wk', False, 'WebKit 돌다 멈춤: %s' % str(e).splitlines()[0][:300])
                wk.close()
    httpd.shutdown()
    gates = [g for g in ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'R'] if any(r[0] == g for r in R_.rows)]
    print('\n══ 요약 (%.0f초)' % (time.time() - t0))
    for g in gates:
        rs = [r for r in R_.rows if r[0] == g]
        nf = sum(1 for r in rs if not r[2])
        print('  %-3s %s  (%d 칸 중 FAIL %d)' % (g, 'PASS' if nf == 0 else 'FAIL', len(rs), nf))
    if a.yardstick:
        bg = [g for g in gates if g.startswith('B')]
        ok = bool(bg) and all(not R_.gate_ok(g) for g in bg)
        print('  헛잣대 %s — 바탕에서 %s' % ('OK' if ok else '틀림', ', '.join('%s %s' % (g, 'FAIL' if not R_.gate_ok(g) else 'PASS(!)') for g in bg)))
        return 0 if ok else 1
    return 0 if all(R_.gate_ok(g) for g in gates) else 1


if __name__ == '__main__':
    sys.exit(main())
