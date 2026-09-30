# -*- coding: utf-8 -*-
r"""_task_jo_c2card(+add1) §H 관문 — A 칩 · A-6 세로줄·태그 · B 접기 n · C 조문 글자 링크 · D 연결 · E 형광펜 · F 정렬 이름 · G 짝(데이터) · G 앱 · 편집 도구(D-4)

  NEW  = --new <파일>(없으면 genie 작업트리 jo/index.html) · BASE = genie 06fd454(md5 3898dea6 — 이 판의 바탕 = canvas_relayout 인도 판)
  데이터 = genie 작업트리 jo/data(두 판 같은 것) · 해설·교재 = 로컬 minbeoppdf 클론(SEED fetch 가 /__book/ 으로 돌린다)
  헛잣대(규칙) = 같은 관문을 BASE 에 먼저 — 새 기능 관문은 BASE 에서 「없음」이 나와야 잣대가 산 것이다
  엔진 = chromium · webkit 책상 1440×900(마우스) · 아이패드 1024×1366(chromium = CDP 진짜 터치) · 폰 390×844(chromium · 형광펜 막대 자리)
  잣대 = DOM 실물 · getBoundingClientRect · elementFromPoint · 계산 스타일 · 저장소 값 · 앱 상태 — 픽셀 비교는 안 한다

쓰기 : python _harness_jo_c2card.py [--new 파일] [--out 폴더] [--only A,A6,B,C,D,E,F,G,GAPP,EQ] [--eng chromium|webkit]
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
_NR = _roots.need_n('민소 해설 재료(_hsul_proto · hsul 보고) · ⚙ editq_apply')   # env_lanes_fix(9/29) — N: 작업 폴더 · 없으면(클라우드) 「N: 필요 — 클라우드 불가(…)」 종료 코드 3
import hashlib, http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
CJH = os.path.dirname(os.path.abspath(__file__))   # env_lanes_fix(9/29) — 같은 폴더(N: · genie _qa 같은 모양 · 옛: N: 고정 자리)
sys.path.insert(0, CJH)
import _harness_canvas_jari as CJ          # noqa: E402 — SEED(기록·교재 fetch 돌림 · 저장소 비우기) · route_filter · VENDOR
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


HERE = os.path.dirname(os.path.abspath(__file__))
OUT = ARG('--out', HERE)
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
ENGS = [ARG('--eng')] if ARG('--eng') else ['chromium', 'webkit']
GENIE = CJ.GENIE
JOD = os.path.join(GENIE, 'jo')
NEWF = ARG('--new', os.path.join(JOD, 'index.html'))
BASE_REV, BASE_MD5 = '06fd454', '3898dea6ee2767968642e12fff35e687'
MB = _roots.mbpdf()
JOP = os.path.join(_NR, 'jopangi')
PROTO = os.path.join(JOP, '민소', '_hsul_proto')
EDITQ = os.path.join(JOP, 'editq_apply.py')
WORK = os.path.join(tempfile.gettempdir(), 'h_c2card')
TESTS = io.open(os.path.join(HERE if os.path.exists(os.path.join(HERE, '_harness_jo_c2card_tests.js')) else CJH, '_harness_jo_c2card_tests.js'), encoding='utf-8').read()
READY = "!!window.__HC2&&typeof render==='function'&&typeof popCard4==='function'"
SERVERS = {}
RES = []
T0 = time.time()


def say(ok, name, detail=''):
    RES.append(('PASS' if ok is True else 'FAIL' if ok is False else 'INFO', name, detail))
    print(RES[-1][0], '|', name, '|', str(detail)[:300], flush=True)


def git(*a, repo=GENIE):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def serve(tag, src):
    if tag in SERVERS:
        return SERVERS[tag][1]
    out = os.path.join(WORK, 'srv_' + tag); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    src = src.replace('\r\n', '\n')
    b = src.index('<body'); bb = src.index('>', b) + 1
    html = src[:bb] + CJ.SEED + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + TESTS + '\n</script>\n' + html[e:]
    io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=out, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            if p.startswith('/__vendor/'):
                return os.path.join(CJ.VENDOR, p[len('/__vendor/'):].replace('/', os.sep))
            if p.startswith('/__book/'):
                return os.path.join(MB, p[len('/__book/'):].replace('/', os.sep))
            if p.startswith('/data/'):
                return os.path.join(JOD, 'data', p[6:].replace('/', os.sep))
            if p in ('/index.html', '/'):
                return super().translate_path(path)
            f = os.path.join(JOD, p.lstrip('/').replace('/', os.sep))
            return f if os.path.exists(f) else super().translate_path(path)

        def log_message(self, *a, **k):
            pass
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


class P:
    def __init__(self, br, eng, tag, src, W, H, mode='desk', q='tok=1'):
        self.eng, self.tag, self.mode = eng, tag, mode
        self.touch = mode in ('pad', 'phone')
        self.port = serve(tag, src)
        if self.touch:
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=CJ.IPAD_UA)
        else:
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1)
        self.ctx.route('**/*', CJ.route_filter)
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(180000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' and 'Failed to load resource' not in m.text else None)
        self.cdp = self.ctx.new_cdp_session(self.pg) if (eng == 'chromium' and self.touch) else None
        self.load(q)

    def load(self, q):
        self.pg.goto('http://127.0.0.1:%d/index.html?%s&who=%s' % (self.port, q, urllib.parse.quote('꼬까')), wait_until='load', timeout=180000)
        self.pg.wait_for_function(READY, timeout=180000)
        self.pg.wait_for_timeout(1200)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def H(self, fn, *a):
        return self.pg.evaluate('a=>__HC2.%s(...a)' % fn, list(a))

    def w(self, ms):
        self.pg.wait_for_timeout(ms)

    def click(self, r, wait=450):
        if not r:
            return False
        x, y = r['cx'], r['cy']
        if self.cdp:
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'id': 1}]}); self.w(50)
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        elif self.touch:
            self.pg.touchscreen.tap(x, y)
        else:
            self.pg.mouse.click(x, y)
        self.w(wait)
        return True

    def mdrag(self, x0, y0, x1, y1, n=12, wait=500):
        m = self.pg.mouse
        m.move(x0, y0); m.down()
        for i in range(1, n + 1):
            m.move(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.w(16)
        m.up(); self.w(wait)

    def tdrag(self, x0, y0, x1, y1, n=12, wait=500):
        def t(ty, pts):
            self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': pts})
        t('touchStart', [{'x': x0, 'y': y0, 'id': 1}])
        for i in range(1, n + 1):
            t('touchMove', [{'x': x0 + (x1 - x0) * i / n, 'y': y0 + (y1 - y0) * i / n, 'id': 1}]); self.w(16)
        for _ in range(3):
            t('touchMove', [{'x': x1, 'y': y1, 'id': 1}]); self.w(30)
        t('touchEnd', []); self.w(wait)

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


# ══════════ 고정물(데이터에서 고른다 · 수를 박지 않는다) ══════════
def fixtures():
    D = os.path.join(JOD, 'data')
    J = lambda n: json.load(io.open(os.path.join(D, n), encoding='utf-8'))
    fx = {}
    N = J('note_민소.json')
    fx['tagnote'] = next(f for f, v in N.items() if '#민소/문학판검' in json.dumps(v, ensure_ascii=False))
    dep = {}
    for kind in ('기출', 'GS', '사례'):
        for k, c in J('2cha_본문_%s_민소.json' % kind).items():
            hs = [r['h'] for r in c.get('행') or [] if r.get('h') and not r.get('co')]
            if hs:
                dep.setdefault(max(hs) - min(hs) + 1, (kind, k))
    fx['dep'] = {d: dep[d] for d in (1, 3, 5) if d in dep}
    GS = J('2cha_본문_GS_민소.json')
    fx['star'] = next(k for k, c in GS.items() if any((r.get('h') or 0) >= 2 and '★' in (r.get('t') or '') for r in c['행']))
    fx['club'] = next(k for k, c in GS.items() if any((r.get('h') or 0) >= 2 and '♣' in (r.get('t') or '') for r in c['행']))
    TK = J('2cha_본문_기출_특허.json')
    fx['tk_other'] = next(k for k in sorted(TK) if '26-63' not in k)
    fx['tk_case'] = sorted(J('2cha_본문_사례_특허.json'))[0]
    fx['ms_gs'] = sorted(GS)[3]
    return fx


def c2jo_census():
    """fm 조문 낱말 — 앱 c2JoParse 와 같은 정규식으로 전 법·전 보드 · 못 읽은 수"""
    rx = re.compile(r'^(\d+)(?:-(\d+)|조의(\d+))?조?([①-⑳]*)(\d*)([가나다라마바사아자차카타파하])?(후단|전단|단서|본문|후|전|본|단)?$')
    D = os.path.join(JOD, 'data'); ok = bad = 0; bads = {}; cards = 0
    for f in sorted(os.listdir(D)):
        if not re.match(r'2cha_본문_.+\.json$', f):
            continue
        J = json.load(io.open(os.path.join(D, f), encoding='utf-8'))
        if not isinstance(J, dict):
            continue
        for k, c in J.items():
            v = (c.get('fm') or {}).get('조문')
            vs = v if isinstance(v, list) else [v]
            if not any(str(x or '').strip() for x in vs):
                continue
            cards += 1
            for s in vs:
                for seg in re.split(r'(?=\(\d+\))', str(s or '')):
                    seg = re.sub(r'^\(\d+\)\s*', '', seg.strip())
                    for tk in seg.split():
                        if not tk or tk == '_':
                            continue
                        if rx.match(re.sub(r'^(민소|특|상|디)(?=\d)', '', tk)):
                            ok += 1
                        else:
                            bad += 1; bads[tk] = bads.get(tk, 0) + 1
    return cards, ok, bad, bads


# ══════════ A · A-6 · B · C · D · E · F · G 앱 ══════════
def run_app(br, eng, src, tag, fx, base=False):
    """tag = 'new'|'base' · base 는 헛잣대(새 기능 없음이 나와야 한다)"""
    pfx = '[%s·%s] ' % (eng, tag)
    p = P(br, eng, tag + '_' + eng, src, 1440, 900)
    try:
        has = p.H('has')
        say(True if not base else None, pfx + '앱 도구', has)
        # ── A 칩 ──
        if not ONLY or 'A' in ONLY:
            o = p.H('open', '기출', '민소', '민기출 25-62-4')
            hs = p.H('heads') or []
            h2 = [h for h in hs if h['lv'] >= 2]
            chips = [h for h in h2 if h['a'] is not None and h['b'] is not None]
            if base:
                say(len(chips) == 0, pfx + 'A 헛잣대 — 바탕엔 칩 0', '헤딩 %d · 칩 %d' % (len(h2), len(chips)))
            else:
                say(len(h2) == 18 and len(chips) == 18, pfx + 'A-1 25-62-4 번호 헤딩 18줄에 칩 두 칸', '헤딩 %d · 칩 %d' % (len(h2), len(chips)))
                sec = []; s = 0; i2 = 0
                for h in hs:
                    if h['lv'] == 1:
                        s += 1; i2 = 0
                    else:
                        i2 += 1; sec.append((s, i2, h))
                want_a = {(1, 4), (1, 5), (1, 8), (2, 6)}
                want_b = {(1, 5): '학판검', (1, 8): '학판검', (2, 4): '학판검', (2, 6): '학판검', (2, 5): '#'}
                bad_a = [(s, i, h['a']) for s, i, h in sec if (h['a'] == '주') != ((s, i) in want_a)]
                bad_b = [(s, i, h['b']) for s, i, h in sec if h['b'] != want_b.get((s, i), '')]
                say(not bad_a, pfx + 'A-2 ♥ 줄(설문1 4·5·8 · 설문2 6) = [주] · 나머지 없음', bad_a or [(s, i) for s, i, h in sec if h['a'] == '주'])
                say(not bad_b, pfx + 'A-3 둘째 칸 = 설문1 5·8 · 설문2 4·6 [학판검] · 설문2 5 [#]', bad_b or {'%d-%d' % (s, i): h['b'] for s, i, h in sec if h['b']})
                full = [h for h in chips if h['a'] and h['b']]   # 두 칸 다 찬 줄(「없음」 점은 여백 1px 꼴이라 따로)
                g = [(h['g1'], h['g2'], h['g3']) for h in full]
                ok = bool(g) and all(x[0] is not None and abs(x[0] - 3) <= 0.8 and abs(x[1] - 2) <= 0.8 and x[2] is not None and abs(x[2] - 2) <= 0.8 for x in g)
                say(ok, pfx + 'A-1 틈 번호↔칩 3 · 칩↔칩 2 · 칩↔글 2px(±0.8 · 두 칸 다 찬 줄 %d)' % len(full), g[:4])
                say(all(h['fs'] == '9px' for h in chips if h['a']) and all(h['sameLine'] for h in chips), pfx + 'A-1 칩 글자 9px · 번호·칩·글 한 줄', [(h['fs'], h['sameLine']) for h in chips[:3]])
                noh = [h['text'][:14] for h in chips if re.search(r'[♥♣★]', h['text'])]
                say(not noh, pfx + 'A-2 ♥♣★ 기호는 그릴 때 지움(글에 안 보임)', noh[:3])
                # 목록으로 [최] → 새로고침 뒤 그대로 → 처음값으로 되돌리면 칸 지움
                r = p.H('chipHit', 1, 'm'); p.click(r, 350)
                m = p.H('menu')
                say(m.get('open') and [o['t'] for o in m['opts']] == ['[주]', '[부]', '[추]', '[최]', '없음'] and [o['t'] for o in m['opts'] if o['sel']] == ['없음'],
                    pfx + 'A-4 칩 누름 → 아래로 목록(글자만 · 지금 값 옅게)', m.get('opts') and [(o['t'], o['sel']) for o in m['opts']])
                below = m.get('open') and r and m['r']['y'] >= r['b'] - 1
                say(bool(below), pfx + 'A-4 목록이 칩 바로 아래', (r and r['b'], m.get('r') and m['r']['y']))
                p.click(next(o['r'] for o in m['opts'] if o['t'] == '[최]'), 350)
                ht = p.H('htag'); key = [k for k in ht if k.endswith('|문제의 소재')]
                say(len(key) == 1 and ht[key[0]]['a'] == '최' and not p.H('menu')['open'], pfx + 'A-5 [최] 고름 → 닫힘 · jopangi.c2htag 한 칸', {k: ht[k] for k in key})
                p.load('tok=1&keep=1'); p.H('open', '기출', '민소', '민기출 25-62-4')
                h1 = (p.H('heads') or [])[1]
                say(h1['a'] == '최' and h1['al'] == '[최]', pfx + 'A-5 새로고침 뒤 그대로 [최]', (h1['a'], h1['al']))
                r = p.H('chipHit', 1, 'm'); p.click(r, 300)
                m = p.H('menu'); p.click(next(o['r'] for o in m['opts'] if o['t'] == '없음'), 300)
                ht = p.H('htag')
                say(not [k for k in ht if k.endswith('|문제의 소재')], pfx + 'A-5 처음값(없음)으로 되돌리면 칸이 지워짐', list(ht)[:3])
                # 키보드 — Enter 로 열고 ↓ Enter 로 고르기 · Esc 닫기 · 밖 누름 닫기
                p.H('chipHit', 3, 'x'); p.ev("()=>{const p=[...POPS].reverse().find(x=>(x._pk||'').indexOf('🧾')>=0);const c=[...p.querySelectorAll('.rbody.card > .ln.rh')][3].querySelector('.c2x');c.focus();}")
                p.pg.keyboard.press('Enter'); p.w(250)
                f0 = p.H('menu').get('focus'); p.pg.keyboard.press('ArrowDown'); p.w(100); f1 = p.H('menu').get('focus')
                p.pg.keyboard.press('Escape'); p.w(150)
                say(f0 and f1 and f0 != f1 and not p.H('menu')['open'], pfx + 'A-4 Enter 열기 · ↓ 옮김 · Esc 닫기', (f0, f1))
                r = p.H('chipHit', 3, 'x'); p.click(r, 250); p.pg.mouse.click(20, 880); p.w(250)
                say(not p.H('menu')['open'], pfx + 'A-4 밖을 누르면 닫힘')
                # ♣ · ★ 카드
                for code, want in ((fx['club'], '추'), (fx['star'], '최')):
                    p.H('open', 'GS', '민소', code)
                    hh = [h for h in (p.H('heads') or []) if h['a'] == want]
                    say(len(hh) >= 1, pfx + 'A-2 %s 헤딩 → [%s] (%s)' % ('♣' if want == '추' else '★', want, code[:24]), [h['text'][:24] for h in hh[:2]])
        # ── A-6 ──
        if not ONLY or 'A6' in ONLY:
            p.H('open', '기출', '민소', '민기출 25-62-4')
            ex = p.H('embx')
            hp = [e for e in ex if 'bk-hp' in e['cls']]; sh = [e for e in ex if 'bk-sh' in e['cls']]
            if base:
                say(len(hp) + len(sh) == 0, pfx + 'A-6 헛잣대 — 바탕엔 세로줄 색 0', len(ex))
            else:
                say(len(hp) == 4 and len(sh) == 1 and all(e['bl'] == 'rgb(226, 177, 0)' for e in hp) and all(e['bl'] == 'rgb(139, 92, 246)' for e in sh),
                    pfx + 'A-6 25-62-4 임베드 세로줄 노랑 4 · 보라 1', [(e['cls'], e['bl']) for e in hp + sh])
            tv = p.H('tagVis', '.pop')
            say((tv['visible'] == 0 and tv['occ'] > 0) if not base else (tv['visible'] > 0), pfx + 'A-6 카드 임베드 「#민소/문학판검」 보이는 글자 %s' % ('0' if not base else '>0(헛잣대)'), tv)
            p.ev("a=>{closeAllPops();return popNote(a,null,{clientX:300,clientY:80},1);}", fx['tagnote']); p.w(1500)
            tv = p.H('tagVis', '.pop')
            say((tv['visible'] == 0 and tv['occ'] > 0) if not base else (tv['visible'] > 0), pfx + 'A-6 노트 팝업(%s) 「#민소/문학판검」 보이는 글자 %s' % (fx['tagnote'][:14], '0' if not base else '>0'), tv)
            sc = p.H('searchCount', '문학판검')
            say(None, pfx + 'A-6 통합 검색 「문학판검」 결과 수', sc)
            RESV.setdefault('search', {})[tag + eng] = sc.get('n')
        # ── B 접기 n ──
        if not ONLY or 'B' in ONLY:
            for d, (kind, code) in sorted(fx['dep'].items()):
                p.H('open', kind, '민소', code)
                f0 = p.H('fold')
                if base:
                    say(f0['btn'] is None, pfx + 'B 헛잣대 — 바탕엔 「접기」 없음 (%s)' % code[:20], f0['btn'])
                    continue
                seq = [f0]
                for _ in range(d + 1):
                    p.click(p.H('foldClick'), 300); seq.append(p.H('fold'))
                labels = [s['btn']['t'] for s in seq]
                ok = labels == ['접기 %d' % i for i in range(d + 1)] + ['접기 0']
                vis = [(s['visible'], s['by']) for s in seq]
                ok2 = seq[0]['visible'] == seq[0]['total'] and seq[-1]['visible'] == seq[-1]['total'] and seq[1]['by'].get('body', 0) == 0 \
                    and sum(v for k, v in seq[1]['by'].items() if k != 'body') == sum(v for k, v in seq[0]['by'].items() if k != 'body') \
                    and all(seq[i]['visible'] >= seq[i + 1]['visible'] for i in range(1, d)) and all(s['callouts'] == seq[0]['callouts'] for s in seq)
                say(ok and ok2, pfx + 'B-1 목차 %d단계 카드(%s %s) 누를 때마다 0→…→%d→0 · 보이는 줄' % (d, kind, code[:18], d), (labels, vis))
                if d >= 2:
                    for _ in range(2):
                        p.click(p.H('foldClick'), 250)
                    fb = p.H('fold'); tg = fb['tg']
                    hs = p.H('heads'); idx = next((i for i, g in enumerate(tg) if g == '›'), None)
                    before = fb['visible']
                    if idx is not None:
                        p.click(p.H('togHit', idx), 300)
                    fa = p.H('fold')
                    say(idx is not None and fa['visible'] > before and fa['btn']['t'] == '접기 2', pfx + 'B-1 접기 2 에서 › 로 한 줄 펴기(%s)' % code[:16], (before, fa['visible'], (hs[idx]['text'][:20] if idx is not None else None)))
                st = f0['btn']
                say(st['fs'] == '11px' and st['bw'] == '0px' and st['t'] == '접기 0', pfx + 'B-1 「접기 n」 글자만 11px · 테두리 0 (%s)' % code[:16], st)
            p.H('open', '기출', '민소', '민기출 25-62-4')
            ct = p.H('cltab'); order = p.H('tabsOrder')
            if not base:
                say(ct and ct['fs'] == '11px' and ct['bw'] == '0px', pfx + 'B-2 Claude 탭 11px · 테두리 0', ct)
                say(order and 'cltab' in order[3] and 'c2fold' in order[4], pfx + 'B-1 「접기 n」 = Claude 바로 오른쪽', order)
        # ── C 조문 ──
        if not ONLY or 'C' in ONLY:
            p.H('open', '기출', '민소', '민기출 25-62-4')
            fj = p.H('fmJo')
            if base:
                say(fj is None, pfx + 'C-3 헛잣대 — 바탕엔 fm 조문 글자 링크 없음')
            else:
                say(fj and fj['segs'] == ['설(1)민소218①민소216①', '설(2)민소396조민소71조민소76①②'] and not fj['bad'], pfx + 'C-3 fm 조문 = 설(N) + 파란 글자 링크', fj and fj['segs'])
                b0 = fj['btns'][0]
                say(b0['fs'] == '11px' and b0['color'] == 'rgb(47, 111, 208)' and b0['bw'] == '0px' and b0['bg'] in ('rgba(0, 0, 0, 0)', 'transparent'), pfx + 'C-1 꼴 11px 파랑 · 알약 없음', b0)
                p.click(p.H('fmJoHit', 0), 1500)
                jp = p.H('joPop')
                say(jp and jp['title'].startswith('민소 제218조') and '📖' not in jp['title'] and jp['jhl'] >= 1, pfx + 'C-1 민소218① → 조문 팝업(📖 뗌 · ① 칠함)', jp)
                r0 = jp['rect']; h = jp['head']
                p.mdrag(h['x'] + 40, h['cy'], h['x'] + 140, h['cy'] + 60, wait=300)
                j2 = p.H('joPop')
                say(abs(j2['rect']['x'] - r0['x'] - 100) < 4 and abs(j2['rect']['y'] - r0['y'] - 60) < 4, pfx + 'C-1 조문 팝업 머리 끌기(마우스)', (r0['x'], r0['y'], j2['rect']['x'], j2['rect']['y']))
                p.ev("()=>closeAllPops()"); p.H('open', '기출', '민소', '민기출 25-62-4')
                p.click(p.H('fmJoHit', 4), 1500)
                jp = p.H('joPop')
                say(jp and jp['jhl'] >= 2 and '1·2항' in (jp['chip'] or ''), pfx + 'C-3 민소76①② → 두 항 칠함 · 머리 「→ 제1·2항」', jp and (jp['jhl'], jp['chip'], jp['hangs']))
            # 1차객 셋 + 원문
            gh = p.H('gaekHome', 4)
            say(None, pfx + '1차객 문제로 감(조문 넷 이상)', gh)
            for kind, name in (('jo', 'C-2① joChip'), ('more', 'C-2① ＋N'), ('jos', 'C-2② JOS'), ('josdead', 'C-2② JOS 시행규칙(흐림)'), ('won', '「⚖ … 원문」')):
                root = '#slot'
                if kind == 'jos':
                    say(None, pfx + '제7판 카드 P7-0073(특허법 제5조 · 시행규칙 제11조) 그림', p.H('p7Jos', 'P7-0073'))
                if kind in ('jos', 'josdead', 'won'):
                    root = '#hz_p7box'
                g = p.H('gaekChip', kind, root)
                if g.get('miss'):
                    say(None, pfx + name + ' — 이 판 1차객에 없음', g); continue
                if kind == 'won':
                    say(g['cls'] == 'jowon' and g['t'].startswith('⚖') and g['href'], pfx + name + ' 그대로(법제처 링크)', (g['t'], (g['href'] or '')[:40]))
                    continue
                if base:
                    say(None, pfx + name + ' 바탕 꼴', (g['cls'], g['t'])); continue
                isj = 'c2jb' in g['cls'] and not g['t'].startswith('⚖')
                say(isj and g['fs'] == '11px' and g['color'] == 'rgb(47, 111, 208)', pfx + name + ' = 파란 글자 링크', (g['cls'], g['t'], g['fs'], g['color']))
                if kind in ('jo', 'jos') and g.get('on'):
                    p.click(g, 1200); jp = p.H('joPop')
                    say(bool(jp) and jp['pk'].startswith('jo|특허법|'), pfx + name + ' 누름 → 조문 팝업', jp and jp['title'])
                    p.ev("()=>{POPS.filter(x=>(x._pk||'').indexOf('jo|')===0).forEach(closeOne);}")
                if kind == 'josdead':
                    say(g['op'] == '0.6', pfx + name + ' 흐림 · 누름 없음', (g['op'], g['cursor']))
            RESV.setdefault('won', {})[tag + eng] = p.H('wonDom', '#hz_p7box')
            p.H('p7Close')
            # 채점 탭 c2LinkEl jo
            p.H('open', '기출', '민소', '민기출 26-63-1')
            gj = p.H('gradeJo')
            if not gj.get('miss'):
                if base:
                    say(None, pfx + 'C-2③ 채점 탭 조문 칩 바탕 꼴', (gj['cls'], gj['t']))
                else:
                    say('c2jb' in gj['cls'] and not gj['t'].startswith('⚖'), pfx + 'C-2③ 채점 탭 조문 = 파란 글자(판례 알약과 구별)', (gj['cls'], gj['t'], gj['color']))
                    p.click(gj, 1200); jp = p.H('joPop')
                    say(bool(jp), pfx + 'C-2③ 누름 → 조문 팝업', jp and jp['title'])
            else:
                say(None, pfx + 'C-2③ 채점 탭 조문 칩 못 찾음', gj)
        # ── D 연결 ──
        if (not ONLY or 'D' in ONLY) and not base:
            p.load('tok=1'); p.H('open', '기출', '민소', '민기출 25-62-4')
            lk = p.H('lk')
            say(lk and [b['t'] for b in lk['btns']][:1] == ['↩링크3'] and lk['btns'][-1]['t'] == '✎ 연결' and lk['btns'][0]['color'] == 'rgb(30, 58, 138)', pfx + 'D-1 25-62-4 ↩링크3 · ✎ 연결', lk)
            p.click(p.H('lkHit', 'mine'), 900)
            w = p.H('lkWin')
            say(w and len(w['rows']) == 3, pfx + 'D-1 ↩링크 창 줄 셋(종류·이름·문제 글)', w and [r['t'][:40] for r in w['rows']])
            n0 = len(p.H('pops'))
            p.click(p.H('lkRowHit', 0), 1500)
            ps = p.H('pops')
            say(len(ps) == n0 + 1 and ps[-1].startswith('cell|🧾'), pfx + 'D-1 줄 누름 → 그 카드 팝업', ps[-1:])
            p.H('open', '기출', '민소', '민기출 25-62-4')
            p.click(p.H('lkHit', 'ed'), 900)
            res = p.H('lkSearch', '보조참가')
            say(len(res) >= 1, pfx + 'D-1 ✎ 연결 찾기(제목·문제 글·쟁점)', res[:3])
            p.click(p.H('lkResHit', 0), 600)
            q = p.H('eq'); lk2 = p.H('lk')
            say(len(q) == 1 and q[0]['kind'] == '연결 넣기' and q[0]['part'] == 'fm.연결사례' and q[0]['target'].startswith('card|기출|민기출 25-62-4') and q[0]['quote'].startswith('[[')
                and lk2['btns'][0]['t'] == '↩링크4', pfx + 'D-2 넣기 → 수정 큐 1 · ↩링크4', (q, lk2['btns'][0]['t']))
            chip = p.H('eqChip')
            say('1' in (chip or ''), pfx + 'D-2 머리 「✎ 수정 N」 바로 바뀜', chip)
            w = p.H('lkWin'); i_app = next((i for i, r in enumerate(w['rows']) if '넣기' in r['src']), None)
            p.click(p.H('lkRowHit', i_app, '.x'), 500)
            q = p.H('eq'); lk2 = p.H('lk')
            say(len(q) == 0 and lk2['btns'][0]['t'] == '↩링크3', pfx + 'D-2 ↶ 취소 → 큐 0 · ↩링크3', (len(q), lk2['btns'][0]['t']))
            w = p.H('lkWin'); i_v = next((i for i, r in enumerate(w['rows']) if r['src'] == '볼트'), None)
            p.click(p.H('lkRowHit', i_v, '.x.del'), 500)
            q = p.H('eq'); w = p.H('lkWin')
            say(len(q) == 1 and q[0]['kind'] == '연결 빼기' and 'gone' in w['rows'][i_v]['cls'] and '빼기' in w['rows'][i_v]['src'], pfx + 'D-2 볼트 연결 ✕ → 빼기 대기 · 줄 그음', (q, w['rows'][i_v]))
            op = p.ev("()=>{popEq(null);const b=POPS[POPS.length-1];const sel=[...b.querySelectorAll('select')].find(s=>[...s.options].some(o=>o.value==='연결 넣기'));const r=[...b.querySelectorAll('.eqrow')];return {kinds:sel?[...sel.options].map(o=>o.value):null,rows:r.map(x=>x.querySelector('.eqk').textContent.slice(-40)),ed:r.map(x=>{const e=[...x.querySelectorAll('button')].find(y=>y.textContent.indexOf('다시 고치기')>=0);return e?e.style.display:'?';})};}")
            say(op['kinds'] and '연결 빼기' in op['kinds'] and len(op['rows']) == 1 and '연결 빼기' in op['rows'][0] and op['ed'] == ['none'], pfx + 'D-3 ✎ 수정 큐 목록 창에 이 종류(다시 고치기 없음)', op)
            p.ev("()=>closeAllPops()")
        # ── E 형광펜 ──
        if (not ONLY or 'E' in ONLY) and not base:
            p.load('tok=1'); p.H('open', '기출', '민소', '민기출 25-62-4')
            c = p.H('callout', 'question')
            say(len(c['rows']) >= 1 and c['sel'] == 'text', pfx + 'E-1 ⑦ 문제 팝업 줄 = 형광펜 대상 · 글 선택 됨', (c['pk'], len(c['rows']), c['sel']))
            r = p.H('markRowRect', 0, 2, 11)
            p.mdrag(r['x0'], r['y0'], r['x1'], r['y1'], wait=500)
            mb = p.H('markBar')
            say(mb['shown'] and mb['below'] and len(mb['btns']) == 9, pfx + 'E-2 드래그 → 도구 아홉이 선택 아래', mb)
            p.click(p.H('markBtnHit', 'y'), 400)
            mk = p.H('marks'); k0 = r['key']
            say(mk.get(k0) == [[2, 12, 'y']], pfx + 'E-3 형광 y → jopangi.c2mark 칸 [[2,12,y]]', mk.get(k0))
            r = p.H('markRowRect', 0, 6, 15); p.mdrag(r['x0'], r['y0'], r['x1'], r['y1'], wait=500); p.click(p.H('markBtnHit', 'u'), 400)
            mk = p.H('marks')
            say(mk.get(k0) == [[2, 6, 'y'], [6, 16, 'u']], pfx + 'E-2 겹침 = 나중 것이 덮음(밑줄 빨강)', mk.get(k0))
            r = p.H('markRowRect', 0, 8, 9); p.mdrag(r['x0'], r['y0'], r['x1'], r['y1'], wait=500); p.click(p.H('markBtnHit', ''), 400)
            mk = p.H('marks'); sp = p.H('markSpans')
            say(mk.get(k0) == [[2, 6, 'y'], [6, 8, 'u'], [10, 16, 'u']], pfx + 'E-2 🧽 지우개', mk.get(k0))
            p.load('tok=1&keep=1'); p.H('open', '기출', '민소', '민기출 25-62-4'); p.H('callout', 'question')
            sp2 = p.H('markSpans')
            dif = next((i for i, (x, y) in enumerate(zip(sp, sp2)) if x != y), None)
            say(sp2 == sp and 'linear-gradient' in sp2[0] and p.H('marks').get(k0) == mk.get(k0), pfx + 'E-3 새로고침 뒤 같음(칠한 조각 글자·꼴 그대로)', (len(sp), len(sp2), dif, (sp[dif][:160], sp2[dif][:160]) if dif is not None else None, mk.get(k0), p.H('marks').get(k0)))
            p.ev("()=>closeAllPops()"); p.H('open', '기출', '민소', '민기출 25-62-4')
            c2 = p.H('callout', 'note')
            if c2.get('miss'):
                say(None, pfx + 'E-1 📄 과거문 없음(이 카드)', c2)
            else:
                r = p.H('markRowRect', 0, 0, 5); p.mdrag(r['x0'], r['y0'], r['x1'], r['y1'], wait=500); p.click(p.H('markBtnHit', 'g'), 400)
                mk = p.H('marks')
                say(mk.get(r['key']) == [[0, 6, 'g']], pfx + 'E-1 📄 과거문 팝업도 형광펜', (r['key'][-30:], mk.get(r['key'])))
            # 길게 누르기 메뉴는 그대로
            r = p.H('markRowRect', 0, 3, 4); p.pg.mouse.move(r['x0'], r['y0']); p.pg.mouse.down(); p.w(750); p.pg.mouse.up(); p.w(300)
            pm = p.ev("()=>!!document.querySelector('.pitmenu, .pitask, .pmenu')")
            say(None, pfx + 'E-2 글줄 길게 누르기 메뉴(그대로 · 참고)', pm)
        # ── F ──
        if not ONLY or 'F' in ONLY:
            lab = {k: p.H('sortLabel', k) for k in ('기출', 'GS', '사례')}
            if base:
                say(all(v and v['first'] == '해례·회차 순' for v in lab.values()), pfx + 'F 헛잣대 — 바탕 「해례·회차 순」', {k: v and v['first'] for k, v in lab.items()})
            else:
                say(lab['기출']['first'] == '회차 순' and lab['GS']['first'] == '회차 순' and lab['사례']['first'] == '사례 순' and all(v['vals'][0] == 'order' for v in lab.values()),
                    pfx + 'F 기출·GS = 「회차 순」 · 사례 = 「사례 순」 (값 order 무변)', {k: v['first'] for k, v in lab.items()})
        # ── G 앱 ──
        if not ONLY or 'GAPP' in ONLY:
            p.load('tok=1')
            hsd = {}
            for kind, subj, code, nm in (('기출', '특허', fx['tk_other'], '특허 기출 다른 회차'), ('사례', '특허', fx['tk_case'], '특허 사례'), ('GS', '민소', fx['ms_gs'], '민소 GS')):
                p.H('open', kind, subj, code); t = p.H('hsTab')
                hsd[nm] = (t['panel'], p.H('hsContent'))
            RESV.setdefault('hs_other', {})[tag + eng] = hsd
            if not base:
                p.H('open', '기출', '민소', '민기출 25-62-4'); t = p.H('hsTab')
                say(t['panel'] and t['bsel'] == ['📘 윤곽 민사소송법 기출집*', '📗 민소 핸드북', '📋 채점표 목차'] and t['tops'][0].startswith('제62회 [문제-4] 해설 · 38~42쪽 (PDF 39~43)'),
                    pfx + 'G-6 25-62-4 해설 탭 자료 고르기 줄 · 머리 한 줄', (t['bsel'], t['tops']))
                pk = p.H('hsPick', '핸드북')
                say(pk and pk['on'] == '📗 민소 핸드북' and any('itm' in r and '4-5-2E' in r for r in pk['rows']), pfx + 'G-6 고르기 줄 전환 → 핸드북(초록 항목 줄)', pk and pk['rows'][:3])
                r = p.H('hsRowHit', '변종뒤승계인'); p.click(r, 400)
                w = p.pg.wait_for_function("()=>{const p=[...POPS].reverse().find(x=>x._hs);return p&&p.querySelector('.pg canvas')&&p._hs.st.n>0;}", timeout=90000); p.w(1200)
                hw = p.H('hsWin')
                say(hw['title'].startswith('📗 민소 핸드북 284쪽') and len(hw['bands']) == 1 and hw['canvas'] and hw['foot'].startswith('자동 — '), pfx + 'G-6 「4. 변종뒤승계인」 → 284쪽 쪽 창 · 노랑 띠', hw)
                bb, pr = hw['bandR'], hw['bodyR']
                say(bb and pr and pr['y'] - 2 <= bb['y'] <= pr['b'], pfx + 'G-6 띠가 창 안에 보임(띠 위 80px 로 굴림)', (bb and bb['y'], pr and (pr['y'], pr['b']), hw['scroll']))
                p.click(p.H('hsNav', 1), 1500); h2 = p.H('hsWin')
                p.click(p.H('hsNav', -1), 1500); h3 = p.H('hsWin')
                say(h2['p'] == 285 and h3['p'] == 284 and len(h2['bands']) == 0 and len(h3['bands']) == 1, pfx + 'G-6 쪽 창 ‹ ›', (h2['title'], h3['title']))
                pa = p.H('hsPageAt', 0.3); p.click({'cx': pa['x'], 'cy': pa['y']}, 1500)
                hj = p.H('hsJari'); kk = [k for k in hj if 'minso_hb' in k]; hw = p.H('hsWin')
                say(len(kk) == 1 and hj[kk[0]].get('p') == 284 and abs(hj[kk[0]]['y2'] - hj[kk[0]]['y'] - 40) < 0.3 and hw['foot'].startswith('📌') and hw['rv'],
                    pfx + 'G-6 쪽 누름 → 📌 손값 jopangi.c2hsjari {p,y,y2(+40),t,who}', {k: hj[k] for k in kk})
                p.load('tok=1&keep=1'); p.H('open', '기출', '민소', '민기출 25-62-4'); p.H('hsTab'); p.H('hsPick', '핸드북')
                r = p.H('hsRowHit', '변종뒤승계인')
                say(r and r['pin'] and r['pg'] == '284쪽', pfx + 'G-6 새로고침 뒤 목록 줄 📌 · 쪽', r and (r['pin'], r['pg']))
                p.click(r, 400); p.pg.wait_for_function("()=>{const p=[...POPS].reverse().find(x=>x._hs);return p&&p.querySelector('.pg canvas')&&p._hs.st.n>0;}", timeout=90000); p.w(1200)
                p.click(p.H('hsRevertHit'), 1200)
                hj = p.H('hsJari'); hw = p.H('hsWin')
                say(hj.get(kk[0], {}).get('auto') is True and hw['foot'].startswith('자동'), pfx + 'G-6 「자동으로 되돌리기」 = {auto:true} 로 덮음(칸 남김)', hj.get(kk[0]))
                p.H('open', '기출', '특허', '특기출 26-63-3'); t = p.H('hsTab')
                say(t['panel'] and [b.rstrip('*') for b in t['bsel']] == ['📄 홍기석 해설', '📄 한빛 해설', '📄 박형준 풀답안', '📄 박형준 보충', '📝 박지환 총평', '📋 채점표 목차'],
                    pfx + 'add1 특허 26-63-3 고르기 줄(해설원천 → 기준 글 → 📋)', t['bsel'])
                p.H('open', '기출', '특허', '특기출 26-63-1'); t = p.H('hsTab')
                say(t['panel'] and '📄 박형준 보충' not in t['bsel'], pfx + 'add1 박형준 보충은 문제3 에만', t['bsel'])
        say(not [e for e in p.errs if 'harness' not in e], pfx + '페이지 오류 0', p.errs[:4])
    finally:
        p.close()


def run_notoken(br, src):
    p = P(br, 'chromium', 'new_nt', src, 1440, 900)
    try:
        p.H('noToken'); p.H('open', '기출', '민소', '민기출 25-62-4'); t = p.H('hsTab')
        say('토큰이 없다' in (t['warn'] or '') and not t['panel'] and '채점표' in t['text'], '[chromium·new] G-6 토큰 없는 기기 — cvbWhy 문구 + 채점표 목차', t['warn'])
    finally:
        p.close()


def run_touch(br, src):
    p = P(br, 'chromium', 'new_pad', src, 1024, 1366, mode='pad')
    try:
        p.H('open', '기출', '민소', '민기출 25-62-4')
        r = p.H('chipHit', 2, 'm'); p.click(r, 400); m = p.H('menu')
        say(m.get('open'), '[chromium·pad] A-4 손가락 톡 → 목록', m.get('opts') and len(m['opts']))
        if m.get('open'):
            p.click(next(o['r'] for o in m['opts'] if o['t'] == '[부]'), 400)
            h = p.H('heads')[2]
            say(h['a'] == '부', '[chromium·pad] A-4 손가락으로 [부] 고름', h['a'])
        p.click(p.H('fmJoHit', 0), 1500)
        jp = p.H('joPop'); h = jp['head']
        p.tdrag(h['x'] + 40, h['cy'], h['x'] + 120, h['cy'] + 70, wait=400)
        j2 = p.H('joPop')
        say(abs(j2['rect']['x'] - jp['rect']['x'] - 80) < 6 and abs(j2['rect']['y'] - jp['rect']['y'] - 70) < 6, '[chromium·pad] C-1 조문 팝업 머리 끌기(진짜 터치)', (jp['rect']['x'], jp['rect']['y'], j2['rect']['x'], j2['rect']['y']))
    finally:
        p.close()


def run_phone(br, src):
    p = P(br, 'chromium', 'new_phone', src, 390, 844, mode='phone')
    try:
        p.H('open', '기출', '민소', '민기출 25-62-4'); p.H('callout', 'question')
        p.H('selectText', 0, 1, 9); p.w(600)
        mb = p.H('markBar')
        say(mb['shown'] and mb['below'], '[chromium·phone] E-2 폰 폭 — 도구가 선택 아래', mb)
    finally:
        p.close()


# ══════════ D-4 편집 도구(볼트 사본) ══════════
def run_editq():
    sys.path.insert(0, JOP)
    import jo_common as JC
    vb, _m, _t = JC.find_vault()
    W = os.path.join(WORK, 'editq'); shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
    V = os.path.join(W, 'vault'); os.makedirs(V)
    picks = {}
    for dp, dn, fn in os.walk(vb):
        for f in fn:
            if not f.endswith('.md'):
                continue
            pth = os.path.join(dp, f)
            b = open(pth, 'rb').read()
            if '연결사례'.encode() not in b:
                continue
            t = b.decode('utf-8', 'replace')
            if 'list' not in picks and re.search(r'^연결사례:\n  - "\[\[', t, re.M):
                picks['list'] = pth
            elif 'empty' not in picks and re.search(r'^연결사례:\n(?!\s*-)', t, re.M) and f.startswith('민기출'):
                picks['empty'] = pth
            elif 'inline' not in picks and re.search(r'^연결사례: ""', t, re.M):
                picks['inline'] = pth
        if len(picks) == 3:
            break
    rel = {}
    for k, pth in picks.items():
        r = os.path.relpath(pth, vb); d = os.path.join(V, r); os.makedirs(os.path.dirname(d), exist_ok=True); shutil.copyfile(pth, d); rel[k] = r
    L = open(os.path.join(V, rel['list']), encoding='utf-8').read()
    have = re.findall(r'^  - "\[\[([^\]]+)\]\]"', L, re.M)
    nm = lambda r: os.path.basename(r)[:-3]
    items = [dict(k='t_add', kind='연결 넣기', target='card|기출|' + nm(rel['list']), quote='[[하네스 새 연결]]', file=rel['list']),
             dict(k='t_del', kind='연결 빼기', target='card|기출|' + nm(rel['list']), quote='[[' + have[0] + ']]', file=rel['list']),
             dict(k='t_have', kind='연결 넣기', target='card|기출|' + nm(rel['list']), quote='[[' + have[-1] + ']]', file=rel['list']),
             dict(k='t_gone', kind='연결 빼기', target='card|기출|' + nm(rel['empty']), quote='[[없는 이름]]', file=rel['empty']),
             dict(k='t_empty', kind='연결 넣기', target='card|기출|' + nm(rel['empty']), quote='[[첫 연결]]', file=rel['empty']),
             dict(k='t_inline', kind='연결 넣기', target='card|사례|' + nm(rel['inline']), quote='[[한 줄 값 펴기]]', file=rel['inline'])]
    for x in items:
        x.update(at='2026-09-24T14:00', who='나', part='fm.연결사례', st='대기')
    recp = os.path.join(W, '기록.json')
    open(recp, 'wb').write(json.dumps({'data': {'jopangi.editq': items}, 'u': {}}, ensure_ascii=False, separators=(',', ':')).encode('utf-8'))
    orig = {k: open(os.path.join(V, r), 'rb').read() for k, r in rel.items()}
    env = dict(os.environ, PYTHONIOENCODING='utf-8', EDITQ_VAULT=V, EDITQ_REC=recp, EDITQ_OUT=os.path.join(W, 'out'))
    r = subprocess.run([sys.executable, EDITQ, 'plan'], capture_output=True, text=True, encoding='utf-8', env=env)
    tab = [ln for ln in r.stdout.splitlines() if ln.startswith('| 연결')]
    say(len(tab) == 6 and '── 연결사례 갈래(fm.연결사례) 6건 ──' in r.stdout, 'D-4 editq_apply.py plan — 연결사례 갈래 따로 표(넣기·빼기)', tab)
    r = subprocess.run([sys.executable, EDITQ, 'apply'], capture_output=True, text=True, encoding='utf-8', env=env)
    fn = next((ln.split('→', 1)[1].strip() for ln in r.stdout.splitlines() if ln.startswith('결과 →')), None)
    out = {x['k']: x for x in json.load(open(fn, encoding='utf-8'))['items']} if fn else {}
    now = {k: open(os.path.join(V, rr), 'rb').read() for k, rr in rel.items()}
    ok_add = out.get('t_add', {}).get('res') == '반영' and b'  - "[[\xed\x95\x98\xeb\x84\xa4\xec\x8a\xa4 \xec\x83\x88 \xec\x97\xb0\xea\xb2\xb0]]"\n' in now['list']
    ok_del = out.get('t_del', {}).get('res') == '반영' and ('"[[' + have[0] + ']]"').encode('utf-8') not in now['list']
    ok_have = out.get('t_have', {}).get('res') == '반영' and '이미 있음' in ' '.join(out.get('t_have', {}).get('notes', []))
    ok_gone = out.get('t_gone', {}).get('res') == '보류' and '⑤' in out.get('t_gone', {}).get('why', '')
    say(ok_add and ok_del and ok_have and ok_gone, 'D-4 apply(볼트 사본) — 넣기 · 빼기 · 이미 있음(반영·할 일 없음) · 이미 없음(보류 ⑤)', {k: (v.get('res'), v.get('why'), v.get('notes')) for k, v in out.items()})
    # 바뀐 곳 밖 바이트 동일 · 줄끝 · BOM
    def diff1(a, b):
        i = 0
        while i < min(len(a), len(b)) and a[i] == b[i]:
            i += 1
        j = 0
        while j < min(len(a), len(b)) - i and a[len(a) - 1 - j] == b[len(b) - 1 - j]:
            j += 1
        return a[i:len(a) - j], b[i:len(b) - j]
    # 기대 바이트를 통째로 지어 맞댄다(바뀐 곳 밖 바이트 동일의 증명)
    lines = orig['list'].decode('utf-8').splitlines(keepends=True)
    k0 = next(i for i, l in enumerate(lines) if l.startswith('연결사례:'))
    items_i = [i for i in range(k0 + 1, len(lines)) if lines[i].startswith('  - ')]
    items_i = items_i[:next((j for j in range(len(items_i)) if items_i[j] != k0 + 1 + j), len(items_i))]
    exp = lines[:]; exp.insert(items_i[-1] + 1, '  - "[[하네스 새 연결]]"\n'); del exp[items_i[0]]
    e_list = ''.join(exp).encode('utf-8')
    e_empty = orig['empty'].replace('연결사례:\n'.encode('utf-8'), '연결사례:\n  - "[[첫 연결]]"\n'.encode('utf-8'), 1)
    e_inline = orig['inline'].replace('연결사례: ""\n'.encode('utf-8'), '연결사례:\n  - "[[한 줄 값 펴기]]"\n'.encode('utf-8'), 1)
    lines_only = all(b'\r' not in now[k] and not now[k].startswith(b'\xef\xbb\xbf') for k in rel)
    say(lines_only and now['list'] == e_list and now['empty'] == e_empty and now['inline'] == e_inline,
        'D-4 기대 바이트와 통째로 같음(바뀐 곳 밖 동일) · LF · BOM 없음 · 목록 끝 넣기+첫 줄 빼기 · 빈 칸 첫 줄 · 한 줄 값 「""」 펴기',
        {k: (len(orig[k]), len(now[k])) for k in rel})
    say(not [f for f in os.listdir(os.path.dirname(os.path.join(V, rel['list']))) if f.startswith('.editq_')], 'D-4 임시 파일 안 남음')
    return rel


# ══════════ G 짝(데이터) ══════════
def run_gdata():
    H = {law: json.load(io.open(os.path.join(MB, 'hsul', law + '.json'), encoding='utf-8')) for law in ('민소', '특허')}
    C = H['민소']['cards']
    say(len(C) == 76, 'G 민소 기출 76장 전부 짝', len(C))
    gc = next(s for s in C['민기출 25-62-4']['srcs'] if s['docid'] == 'minso_gc')
    M = json.load(open(os.path.join(PROTO, 'hs_map.json'), encoding='utf-8'))
    rows = [r for r in gc['rows'] if 'ci' in r]
    bad = [r['ci'] for r in rows if not (M.get(str(r['ci'])) and M[str(r['ci'])]['p'] == r['p'] and abs(M[str(r['ci'])]['y'] - r['y']) < 0.11)]
    say(len(rows) == 18 and not bad, 'G-3 25-62-4 기출집 18줄 = hs_map.json(p · y)', (len(rows), bad))
    hb = next(s for s in C['민기출 25-62-4']['srcs'] if s['docid'] == 'minso_hb')
    T = json.load(open(os.path.join(PROTO, 'hb_rows_62_4.json'), encoding='utf-8'))
    mine = [r for r in hb['rows'] if 'ci' in r or 'item' in r]
    bad = [(a.get('t') or a.get('item'))[:16] for a, b in zip(mine, T) for k in ('p', 'y', 'p2', 'y2') if k in b and a.get(k) is not None and abs(float(a[k]) - float(b[k])) > 0.11]
    say(len(mine) == 20 and not bad and [r['item'] for r in mine if 'item' in r] == ['4-5-2E', '5-11-3'], 'G-4 25-62-4 핸드북 = hb_rows_62_4.json(항목 4-5-2E · 5-11-3 · 줄 18)', (len(mine), bad))
    rep = json.load(open(os.path.join(JOP, '민소', 'hsul', '_hsul_report_민소.json'), encoding='utf-8'))
    ev = rep['hb']['ev']
    say(ev['tag']['top1'] >= 93 and ev['tag']['top3'] >= 96 and ev['tag']['n'] == 97, 'G-4 핸드북 잣대(08~25회) 태그 곱 1등 ≥93/97 · 3등 안 ≥96/97', {k: (v['top1'], v['top3'], v['n']) for k, v in ev.items()})
    want = {'25-62-1': ['3-10-1', '5-15-3B', '4-7-2A'], '25-62-2': ['3-18-1A', '6-1-4'], '25-62-3': ['6-6', '4-6-1B', '2-12-1B'], '25-62-4': ['4-5-2E', '5-11-3']}
    got = {c: [r['item'] for s in C['민기출 ' + c]['srcs'] if s['docid'] == 'minso_hb' for r in s['rows'] if 'item' in r] for c in want}
    say(got == want, 'G-4 62회 10설문 핸드북 항목', got)
    tbl = {}
    for k, v in C.items():
        for s in v['srcs']:
            t = tbl.setdefault(s['docid'], dict(cards=0, rows=0, lo=0, none=0))
            t['cards'] += 1; t['rows'] += sum(1 for r in s['rows'] if 'ci' in r); t['lo'] += sum(1 for r in s['rows'] if r.get('lo')); t['none'] += sum(1 for r in s['rows'] if r.get('none'))
    say(None, 'G 76장 자료별 줄 수 · 「핸드북에 없음」 · lo(≈)', tbl)
    TKc = H['특허']['cards']
    t2 = {k[:14]: {s['docid']: (sum(1 for r in s['rows'] if 'ci' in r), sum(1 for r in s['rows'] if r.get('lo'))) for s in v['srcs']} for k, v in TKc.items()}
    say(len(TKc) == 4 and all(len(v) >= 4 for v in t2.values()), 'add1 특허 26-63-1~4 × 자료 줄 수 · lo', t2)


def main():
    os.makedirs(WORK, exist_ok=True)
    fx = fixtures()
    say(None, '고정물', fx)
    new_src = open(NEWF, 'rb').read().decode('utf-8')
    base_b = git('show', BASE_REV + ':jo/index.html')
    say(hashlib.md5(base_b.replace(b'\r\n', b'\n')).hexdigest() == BASE_MD5, 'BASE = %s md5(LF) %s' % (BASE_REV, BASE_MD5[:8]))
    base_src = base_b.decode('utf-8')
    say(None, 'NEW = %s md5(LF) %s' % (NEWF, hashlib.md5(new_src.replace('\r\n', '\n').encode('utf-8')).hexdigest()))
    if not ONLY or 'C' in ONLY:
        cards, ok, bad, bads = c2jo_census()
        other = {k: v for k, v in bads.items() if re.match(r'^(부경|민(?!소)|의정서|등록령|상법)', k)}
        say(len(bads) - len(other) <= 1, 'C-3 fm 조문 census — 카드 %d · 낱말 읽음 %d · 못 읽음 %d(앱에 없는 법 %d · 그 밖 %d) — 못 읽은 것은 글자 그대로' % (cards, ok, bad, sum(other.values()), bad - sum(other.values())), bads)
    if not ONLY or 'G' in ONLY:
        run_gdata()
    if not ONLY or 'EQ' in ONLY:
        run_editq()
    with sync_playwright() as pw:
        for eng in ENGS:
            br = getattr(pw, eng).launch()
            try:
                run_app(br, eng, base_src, 'base', fx, base=True)
                run_app(br, eng, new_src, 'new', fx)
            finally:
                br.close()
        if 'chromium' in ENGS and (not ONLY or 'GAPP' in ONLY or 'A' in ONLY or 'E' in ONLY):
            br = pw.chromium.launch()
            try:
                if not ONLY or 'GAPP' in ONLY:
                    run_notoken(br, new_src)
                if not ONLY or 'A' in ONLY or 'C' in ONLY:
                    run_touch(br, new_src)
                if not ONLY or 'E' in ONLY:
                    run_phone(br, new_src)
            finally:
                br.close()
    # 바탕과 같음
    for eng in ENGS:
        if 'search' in RESV and ('base' + eng) in RESV['search']:
            a, b = RESV['search'].get('base' + eng), RESV['search'].get('new' + eng)
            say(None if a == 0 else (a == b and a is not None), '[%s] A-6 통합 검색 「문학판검」 결과 수 = 바탕%s' % (eng, ' — 두 판 0건(앱 통합 검색 범위에 목차노트 글이 없다 · 헛잣대라 게이트 아님)' if a == 0 else ''), (a, b))
        if 'won' in RESV and ('base' + eng) in RESV['won']:
            a, b = RESV['won'].get('base' + eng), RESV['won'].get('new' + eng)
            say(bool(a) and a == b, '[%s] C 「⚖ … 원문」 DOM · 링크 = 바탕' % eng, (len(a or []), (a or [''])[:2]))
        if 'hs_other' in RESV and ('base' + eng) in RESV['hs_other']:
            a, b = RESV['hs_other']['base' + eng], RESV['hs_other']['new' + eng]
            for nm in a:
                say(a[nm] == b[nm], '[%s] G-6 %s 해설 탭 = 바탕(DOM)' % (eng, nm), (len(a[nm][1] or ''), len(b[nm][1] or ''), b[nm][0]))
    np_ = sum(1 for r in RES if r[0] == 'PASS'); nf = sum(1 for r in RES if r[0] == 'FAIL'); ni = sum(1 for r in RES if r[0] == 'INFO')
    body = '# _harness_jo_c2card 결과 %s (%.0f초)\n\nPASS %d · FAIL %d · INFO %d\n\n' % (time.strftime('%m-%d %H:%M'), time.time() - T0, np_, nf, ni) + \
           '\n'.join('%s | %s | %s' % (a, b, str(c)[:600]) for a, b, c in RES) + '\n'
    out = os.path.join(OUT, '_harness_jo_c2card_result.txt')
    data = body.encode('utf-8')
    for _ in range(4):
        open(out, 'wb').write(data); time.sleep(0.5)
        if open(out, 'rb').read() == data:
            break
    print('PASS %d · FAIL %d · INFO %d → %s' % (np_, nf, ni, out))


RESV = {}
if __name__ == '__main__':
    main()
