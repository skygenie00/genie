# -*- coding: utf-8 -*-
r"""_task_jo_joscreen(+add1) 관문 하네스 — 본판 §G 1~10 · add1 §D 8(대체)·11·12·13 · 더함 8-R(⚙↔앱 규칙 대조) · 14(「이 조 아님 ×」).

  python _harness_jo_joscreen.py [--new <앱>] [--data <jo/data>] [--out <폴더>] [--only a,b,...]

  NEW  = 패치한 앱 + 새 데이터(jimun_특허·상표 = ⚙ jo_link)
  BASE = genie 59b8701(mbsame 인도 판) 앱 + 그 판 jo/data — 칸마다 헛잣대(바탕에서 FAIL)
  누름 = 진짜 포인터(page.mouse · 손가락 = CDP 터치 반지름 22 · 펜 = CDP 펜) · el.click() 없음 · 보임 = display ≠ none · 높이 > 0
  브라우저 = Chromium(1440·1280) + WebKit(아이패드 폭 820) · 직렬
"""
import io, json, os, re, sys, time, hashlib, shutil, subprocess, tempfile, threading, socketserver, http.server, urllib.parse, collections, tarfile
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
JOP = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(JOP, u'공통', u'_harness'))
sys.path.insert(0, JOP)
import _harness_canvas_jari as CJ          # noqa: E402 — SEED · VENDOR · route_filter · NOISE
import jo_link as JL                       # noqa: E402 — ⚙ 규칙(8-R 대조)
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = CJ.GENIE
JOD = os.path.join(GENIE, 'jo')
NEWF = ARG('--new', os.path.join(JOD, 'index.html'))
DATA = ARG('--data', os.path.join(JOD, 'data'))
OUT = ARG('--out', HERE)
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
BASE_REV = ARG('--base', '59b8701')
WORK = os.path.join(tempfile.gettempdir(), 'h_joscreen')
TESTS = io.open(os.path.join(HERE, '_harness_jo_joscreen_tests.js'), encoding='utf-8').read()
READY = "!!window.__JS&&typeof render==='function'"
RES = []
SERVERS = {}
# 지시서 add1 §D-8 — 옛 uid(0d4144c 판) · 지금 데이터는 uid 판 새 uid → 별칭표(uid_alias.json map)로 옮겨 맞댄다
WANT1 = ['P7-0208', 'T9734751', 'T9734755', 'T9128711', 'T9128712', 'T9128713', 'T9128714', 'T9128715', 'T9128727', 'T9128731', 'T9128732']
NOT1 = ['T0340746', 'T0845085', 'T0744777', 'T1754133']


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:300]))


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:300]))


def git(*a):
    return subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def head_tree(sub, dst):
    if os.path.isdir(dst) and os.listdir(dst):
        return dst
    os.makedirs(dst, exist_ok=True)
    raw = git('archive', '--format=tar', BASE_REV, sub)
    with tarfile.open(fileobj=io.BytesIO(raw)) as tf:
        tf.extractall(dst)
    return dst


def serve(tag, src, data):
    key = tag + '|' + data + '|' + hashlib.md5(src.encode('utf-8')).hexdigest()
    if key in SERVERS:
        return SERVERS[key][1]
    out = os.path.join(WORK, 'srv_%s_%d' % (tag, len(SERVERS)))
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    src = src.replace('\r\n', '\n')
    b = src.index('<body'); bb = src.index('>', b) + 1
    AUTO = "<script>try{localStorage.setItem('jopangi_auto',JSON.stringify({important:'v1',at:'2026-08-28T16:48:32.584Z'}));}catch(e){}</script>"
    html = src[:bb] + CJ.SEED + AUTO + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + TESTS + '\n</script>\n' + html[e:]
    io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)
    exam = os.path.join(GENIE, 'gichul', 'pdf')

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=out, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            if p.startswith('/__vendor/'):
                return os.path.join(CJ.VENDOR, p[len('/__vendor/'):].replace('/', os.sep))
            if p.startswith('/data/'):
                return os.path.join(data, p[6:].replace('/', os.sep))
            if p.startswith('/gichul/pdf/'):
                return os.path.join(exam, p[len('/gichul/pdf/'):].replace('/', os.sep))
            if p in ('/index.html', '/'):
                return super().translate_path(path)
            f = os.path.join(JOD, p.lstrip('/').replace('/', os.sep))
            return f if os.path.exists(f) else super().translate_path(path)

        def log_message(self, *a, **k):
            pass
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[key] = (srv, srv.server_address[1])
    return srv.server_address[1]


class Pg:
    def __init__(self, br, tag, src, data, keep=False, W=1440, H=900, touch=False, ctx=None, port=None):
        self.port = port or serve(tag, src, data)
        self.br = br
        self.ctx = ctx or br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, has_touch=touch)
        self.ctx.route('**/*', CJ.route_filter)
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(180000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' else None)
        self.open(keep)
        self.cdp = None

    def open(self, keep=False):
        self.pg.goto('http://127.0.0.1:%d/index.html?tok=1&who=%s%s' % (self.port, urllib.parse.quote('꼬까'), '&keep=1' if keep else ''), wait_until='load', timeout=180000)
        self.pg.wait_for_function(READY, timeout=180000)
        self.pg.wait_for_timeout(700)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def click(self, at, wait=500):
        if not at or not at.get('on'):
            return False
        self.pg.mouse.click(at['cx'], at['cy'])
        self.pg.wait_for_timeout(wait)
        return True

    def hold(self, x, y, ms=600, wait=400):
        """마우스 길게 누르기(진짜 포인터)"""
        self.pg.mouse.move(x, y)
        self.pg.mouse.down()
        self.pg.wait_for_timeout(ms)
        self.pg.mouse.up()
        self.pg.wait_for_timeout(wait)

    def _cdp(self):
        if not self.cdp:
            self.cdp = self.ctx.new_cdp_session(self.pg)
        return self.cdp

    def touch(self, x, y, ms=60, wait=500):
        """손가락 — CDP 터치(반지름 22 · 아이패드 손가락과 같은 면적)"""
        pt = {'x': x, 'y': y, 'radiusX': 22, 'radiusY': 22, 'force': 1, 'id': 1}
        self._cdp().send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [pt]})
        self.pg.wait_for_timeout(ms)
        self._cdp().send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        self.pg.wait_for_timeout(wait)

    def pen(self, x, y, ms=600, wait=400):
        """펜 — CDP 마우스 사건 pointerType pen"""
        c = self._cdp()
        c.send('Input.dispatchMouseEvent', {'type': 'mouseMoved', 'x': x, 'y': y, 'pointerType': 'pen'})
        c.send('Input.dispatchMouseEvent', {'type': 'mousePressed', 'x': x, 'y': y, 'button': 'left', 'buttons': 1, 'clickCount': 1, 'pointerType': 'pen', 'force': 0.5})
        self.pg.wait_for_timeout(ms)
        c.send('Input.dispatchMouseEvent', {'type': 'mouseReleased', 'x': x, 'y': y, 'button': 'left', 'buttons': 0, 'clickCount': 1, 'pointerType': 'pen'})
        self.pg.wait_for_timeout(wait)

    def type(self, s):
        self.pg.keyboard.type(s)

    def errs_all(self):
        return [y for y in (self.errs + (self.ev("()=>__JS.errs()") or [])) if not CJ.NOISE(y)]

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


def base_env():
    hd = head_tree('jo/data', os.path.join(WORK, 'head_' + BASE_REV, 'jo_data'))
    return git('show', '%s:jo/index.html' % BASE_REV).decode('utf-8'), os.path.join(hd, 'jo', 'data')


def new_env():
    return io.open(NEWF, encoding='utf-8').read(), DATA


def alias_map():
    A = json.load(io.open(os.path.join(DATA, 'uid_alias.json'), encoding='utf-8'))
    return A.get('map', {})


def envs():
    bs, bd = base_env()
    ns, nd = new_env()
    return (('BASE', bs, bd), ('NEW', ns, nd))


def envs3():
    """BASE = 바탕 앱 + 바탕 데이터 · BASEN = 바탕 앱 + 새 데이터(UI 만 가르는 헛잣대) · NEW"""
    bs, bd = base_env()
    ns, nd = new_env()
    return {'BASE': (bs, bd), 'BASEN': (bs, nd), 'NEW': (ns, nd)}


# ══════════ 8 · 8-R 데이터 관문(⚙ jo_link) ══════════
CHAT = {u'특허': {u'①': 1789, u'②': 266, u'③': 35, u'④': 405, u'없음': 19, 'um': 13, 'rows': 1802},
        u'상표': {u'①': 954, u'②': 64, u'③': 0, u'④': 0, u'없음': 82, 'um': 48, 'rows': 1002}}


def p7jo_py(s, jokey):
    """앱 p7Jo 를 파이썬으로(새 규칙 = jo_link.other_law) — 8-R 대조용"""
    out, seen = [], set()

    def add(k):
        if k and k not in seen:
            seen.add(k); out.append(k)
    for m in re.finditer(u'法\\s*(\\d+)(?:조)?(?:의\\s*(\\d+))?', s):
        add(u'제' + m.group(1) + u'조' + (u'의' + m.group(2) if m.group(2) else u''))
    for m in re.finditer(u'제\\s?(\\d+)조(?:의\\s?(\\d+))?', s):
        n = m.group(1) + (u'의' + m.group(2) if m.group(2) else u'')
        if JL.other_law(n, s, u'특허법'):
            continue
        k = u'제' + m.group(1) + u'조' + (u'의' + m.group(2) if m.group(2) else u'')
        if k not in jokey:
            continue
        add(k)
    for m in re.finditer(u'施規\\s*(\\d+)(?:의\\s*(\\d+))?', s):
        add(u'施規 ' + m.group(1) + (u'의' + m.group(2) if m.group(2) else u''))
    return out[:5]


def data_gates():
    bs, bd = base_env()
    for law in (u'특허', u'상표'):
        B = json.load(io.open(os.path.join(bd, 'jimun_%s.json' % law), encoding='utf-8'))
        Nw = json.load(io.open(os.path.join(DATA, 'jimun_%s.json' % law), encoding='utf-8'))
        KEYS = {x['k'] for x in json.load(io.open(os.path.join(DATA, 'jo_%s_목록.json' % {u'특허': u'특허법', u'상표': u'상표법'}[law]), encoding='utf-8'))[u'조']}
        res = JL.apply(JOP, law, B[u'문제'], KEYS)
        diff = [(qa['id'], za['n']) for qa, qb in zip(B[u'문제'], Nw[u'문제']) for za, zb in zip(qa[u'지문'], qb[u'지문']) if za['jo'] != zb['jo']]
        other = 0
        for qa, qb in zip(B[u'문제'], Nw[u'문제']):
            for za, zb in zip(qa[u'지문'], qb[u'지문']):
                if {k: v for k, v in za.items() if k != 'jo'} != {k: v for k, v in zb.items() if k != 'jo'}:
                    other += 1
        T('8', u'%s — 인도 데이터 지문 조 = ⚙ jo_link(바탕 원장 조) · 조 밖 칸 무변' % law, not diff and not other, {'다름': diff[:6], '조 밖 다름': other})
        st = res['stat']
        ch = CHAT[law]
        dev = {k: (st[k], ch[k], (round(100.0 * (st[k] - ch[k]) / ch[k], 2) if ch[k] else (0 if st[k] == 0 else 999))) for k in (u'①', u'②', u'③', u'④', u'없음')}
        dev['못 짝지음'] = (len(res['unmatched']), ch['um'])
        dev['리담 행'] = (res['rows'], ch['rows'])
        T('8', u'%s — 갈래 수 채팅 값 대조(±2%%)' % law, all(abs(v[2]) <= 2 for k, v in dev.items() if len(v) == 3) and len(res['unmatched']) == ch['um'] and res['rows'] == ch['rows'], dev)
        T('8', u'%s — 짝지은 리담 기출 행의 조가 그 지문 조에 다 있음(없는 것 0)' % law, not res['miss'], {'짝지음': res['matched'], '없음': len(res['miss'])})
        N('8', u'%s — 못 짝지음 %d(연도 · 문번 · 조 · 선지 앞 40자)' % (law, len(res['unmatched'])),
          [u'%s · %s · 제%s조 · %s' % (r.get('year'), r.get('problemNumber'), r.get('pathSlug'), re.sub(u'\\s+', u' ', r.get('bodyMd') or u'')[:40]) for r in res['unmatched']])
        N('8', u'%s — 목록 밖 법 이름(보고)' % law, dict(res['names']))
        LN = {u'특허': u'특허법', u'상표': u'상표법'}[law]
        have = {x['k'] for x in json.load(io.open(os.path.join(DATA, 'jo_%s_목록.json' % LN), encoding='utf-8'))[u'조']}
        gone = collections.Counter()
        for q in Nw[u'문제']:
            for z in q[u'지문']:
                for c in z['jo']:
                    n = JL.jo_num(c, u'특' if law == u'특허' else u'상')
                    k = (u'제' + n.replace(u'의', u'조의') if u'의' in n else u'제' + n + u'조') if n else None
                    if k and k not in have:
                        gone[k] += 1
        N('8', u'%s — 앱 조 목록에 없는 조(삭제 조 등 · 조문 화면이 없어 패널로 못 봄)로 이은 지문 조 수' % law, dict(gone.most_common()))
        if law == u'특허':
            N('8', u'특허 — ③ 으로 비운 %d(연도-회-번 · 선지 · uid)' % len(res['emptied3']),
              [u'%s-%s-%s · %s · %s' % (q[u'연도'], q[u'회차'], q.get(u'시험문번') or q[u'문번'], z.get(u'기호') or z['n'], z.get('uid')) for q, z in res['emptied3']])
    # 8-R ⚙ ↔ 앱 규칙 대조 재료(파이썬 쪽 값)
    B = json.load(io.open(os.path.join(bd, 'jimun_특허.json'), encoding='utf-8'))
    pairs, want = [], []
    for q in B[u'문제']:
        for z in q[u'지문']:
            for c in z['jo']:
                n = JL.jo_num(c, u'특')
                if n is None:
                    continue
                pairs.append([z.get('sol') or '', n, u'특허법'])
                want.append(JL.other_law(n, z.get('sol') or '', u'특허법'))
    BS = json.load(io.open(os.path.join(bd, 'jimun_상표.json'), encoding='utf-8'))
    for q in BS[u'문제']:
        for z in q[u'지문']:
            for c in z['jo']:
                n = JL.jo_num(c, u'상')
                if n is None:
                    continue
                pairs.append([z.get('sol') or '', n, u'상표법'])
                want.append(JL.other_law(n, z.get('sol') or '', u'상표법'))
    P7 = json.load(io.open(os.path.join(DATA, 'jimun_7pan.json'), encoding='utf-8'))
    JK = {x['k'] for x in json.load(io.open(os.path.join(DATA, 'jo_특허법_목록.json'), encoding='utf-8'))[u'조']}
    p7want = {z['id']: p7jo_py(z.get('sol') or '', JK) for z in P7[u'지문']}
    return pairs, want, p7want


def rule_gates(br, pairs, want, p7want):
    E = envs3()
    for tag in ('BASE', 'NEW'):
        src, data = E[tag]
        p = Pg(br, 'rule' + tag, src, data)
        try:
            got = p.ev("ps=>__JS.ruleJS(ps)", pairs)
            p7 = p.ev("()=>__JS.p7JoAll()")
            bad = [i for i, (a, b) in enumerate(zip(got or [], want)) if a != b] if got is not None else None
            bad7 = [k for k in p7want if (p7 or {}).get(k) != p7want[k]]
            ok = got is not None and len(got) == len(want) and not bad and not bad7
            nm = u'⚙ jo_link.other_law ↔ 앱 joOtherLaw — 리담 해설 조 %d 쌍 판정 같음 · 제7판 해설 p7Jo %d 지문 = 파이썬 새 규칙' % (len(want), len(p7want))
            if tag == 'NEW':
                T('8-R', nm, ok, {'쌍 다름': (bad or [])[:6], '제7판 다름': bad7[:6], '다른 법 판정 수': sum(1 for x in want if x)})
            else:
                T('8-R-헛', u'헛잣대 — 바탕 앱(joOtherLaw 없음 · 옛 JO_OTHER 14자 창)은 어긋난다', not ok, {'앱 판정': got is not None, '제7판 다름': len(bad7), '예': bad7[:6]})
            N('8-R', tag + u' 오류', p.errs_all()[:5])
        finally:
            p.close()


# ══════════ 1 · 3 머리 · 본문 칸 ══════════
def head_ok(h):
    it = h['items']
    four = [x for x in it if re.match(u'^(📜|☑|⚖|🧾)', x['t'])]
    return (h['lawChip'] == 0 and not h['pre'] and re.match(u'^시행 \\d{4}-\\d{2}-\\d{2}$', h['sihaeng'] or '') and not h['connK']
            and not h['c3chip'] and not h['themeChip'] and not h['cardChip'] and not h['clock']
            and len(four) == 4 and len(it) == 4
            and all(x['bg'] in ('rgba(0, 0, 0, 0)', 'transparent') and x['bw'] == '0px' and x['fs'] == '11px' and x['fw'] == '800' for x in four))


def head_gates(br, wk):
    E = envs3()
    for tag in ('BASE', 'NEW'):
        src, data = E[tag]
        for bname, b, W in (('Chromium', br, 1440), ('WebKit', wk, 820)):
            if tag == 'BASE' and bname == 'WebKit':
                continue
            p = Pg(b, 'head' + tag + bname, src, data, W=W, H=1000)
            try:
                for law in (u'특허법', u'상표법', u'디자인보호법'):
                    p.ev("a=>__JS.jo(a[0],a[1],{panel:true})", [law, u'제1조'])
                    h = p.ev("()=>__JS.head()")
                    ok = bool(head_ok(h))
                    ed = p.ev("()=>__JS.hasEditLine()")
                    if tag == 'NEW':
                        T('1', u'%s 제1조 머리(%s %d) — 법 칩·🕐·파일 이름·「이 조문 연결」·3법/테마/카드 칩 DOM 0 · 남은 칩 넷 = 바탕 투명·테 0·11px·800' % (law, bname, W), ok,
                          {'시행': h['sihaeng'], '칩': [(x['t'], x['bg'], x['bw'], x['fs'], x['fw']) for x in h['items']]})
                        T('3', u'%s 제1조 본문 칸(%s) — 「내 편집본」 글자 0' % (law, bname), not ed, {'본문 첫': p.ev("()=>__JS.bodyText()")[:60]})
                    else:
                        T('1-헛', u'헛잣대 — 바탕 %s 제1조 머리는 옛 꼴' % law, not ok, {'앞': h['pre'], '시행': h['sihaeng'], '칩': [x['t'] for x in h['items']]})
                        T('3-헛', u'헛잣대 — 바탕 %s 본문 칸에 「내 편집본」 있음' % law, ed, '')
                N('1', tag + bname + u' 오류', p.errs_all()[:5])
            finally:
                p.close()


# ══════════ 2 · 12 · 8 · 11 · 13 패널 ══════════
def panel_gates(br, wk):
    E = envs3()
    AM = alias_map()
    want1 = [AM.get(x, x) for x in WANT1]
    not1 = [AM.get(x, x) for x in NOT1] + ['TR91043']
    for tag in ('BASE', 'BASEN', 'NEW'):
        src, data = E[tag]
        p = Pg(br, 'panel' + tag, src, data, W=1440, H=1000)
        try:
            p.ev("()=>__JS.jo('특허법','제1조',{panel:true,f:'all',p:0})")
            chip, alln = p.ev("()=>__JS.chipN()"), p.ev("()=>__JS.panelAll()")
            ids = p.ev("()=>__JS.panelAllIds()")
            seq = [(x.get('id') if x.get('kind') == 'P' else x['sid']) for x in ids]
            sids = [x['sid'] for x in ids]
            if tag == 'NEW':
                T('2', u'제1조 칩 N = 패널 「전체」 N = 11', chip == alln == 11, {'칩': chip, '패널': alln})
                T('8', u'제1조 패널 11 · 차례 uid 대조(P7-0208 → 1997-34-8 ①⑤ → 1991-28-1 ①~⑤ → 1991-28-4 ①④⑤)', seq == want1, {'패널': seq, '기대': want1})
                T('8', u'제1조 패널에 없음 — T0340746·T0845085·T0744777·T1754133(별칭 → %s) · 1991-28-4 ③(TR91043)' % ','.join(not1[:4]), not (set(not1) & set(sids)), sorted(set(not1) & set(sids)))
            elif tag == 'BASE':
                T('8-헛', u'헛잣대 — 바탕(앱+데이터) 제1조 패널 = 넷 있음 · 노하우(1991-28-1) 없음', (set(not1[:4]) <= set(sids)) and not (set(want1[3:8]) & set(sids)), {'패널': seq})
                T('2-헛', u'헛잣대 — 바탕 제1조 칩 ≠ 패널', chip != alln, {'칩': chip, '패널': alln})
            # 11 최신 연도부터
            def mono(xs):
                bad = []
                for a, b in zip(xs, xs[1:]):
                    if (b['y'] > a['y']) or (b['y'] == a['y'] and a['kind'] == 'L' and b['kind'] == 'L' and (b['no'], b['ch']) < (a['no'], a['ch'])):
                        bad.append((a['sid'], a['y'], a.get('no'), b['sid'], b['y'], b.get('no')))
                return bad
            orders = {u'특허 제1조': ids}
            for law, k in ((u'특허법', u'제29조'), (u'상표법', u'제34조')):
                p.ev("a=>__JS.jo(a[0],a[1],{panel:true,f:'all',p:0})", [law, k])
                orders[law[:2] + ' ' + k] = p.ev("()=>__JS.panelAllIds()")
            p.ev("()=>__JS.jo('특허법','제29조',{panel:true,f:'L',p:0})")
            lonly = p.ev("()=>__JS.panelAllIds()")
            bads = {k: mono(v) for k, v in orders.items()}
            bads[u'특허 제29조 기출 거름'] = mono(lonly)
            full29 = [x['sid'] for x in orders[u'특허 제29조'] if x['kind'] == 'L']
            same_l = [x['sid'] for x in lonly] == full29
            if tag == 'NEW':
                T('11', u'최신 연도부터 — 제1조·제29조·상표 제34조 · 제29조 「기출」 거름 · 모든 쪽(쪽 넘김) 연도 ↓ · 같은 해 문번 ↑ · 선지 ↑', not any(bads.values()) and same_l,
                  {'어긋남': {k: v[:3] for k, v in bads.items()}, '거름 차례 = 전체의 기출 차례': same_l, '수': {k: len(v) for k, v in orders.items()}})
                T('11', u'제1조 1번 = P7-0208 · 2번 = 1997', len(ids) > 1 and ids[0].get('id') == 'P7-0208' and ids[1]['y'] == 1997, [(x.get('id'), x['y']) for x in ids[:3]])
                top29 = orders[u'특허 제29조'][0] if orders[u'특허 제29조'] else {}
                N('11', u'제29조 맨 위', {'sid': top29.get('sid'), '연도': top29.get('y')})
            elif tag == 'BASEN':
                y = [x['y'] for x in ids]
                T('11-헛', u'헛잣대 — 바탕 앱(+새 데이터) 제1조: 1991 이 1997 보다 위', 1991 in y and 1997 in y and y.index(1991) < y.index(1997), [(x.get('id') or x['sid'], x['y']) for x in ids])
            # 13 쪽 줄
            p.ev("()=>__JS.jo('특허법','제1조',{panel:true,f:'all',p:0})")
            pr_all = p.ev("()=>__JS.pageRow()")
            p.ev("()=>__JS.jo('특허법','제1조',{panel:true,f:'P',p:0})")
            pr_one, n_one = p.ev("()=>__JS.pageRow()"), p.ev("()=>__JS.panelCards().length")
            nmh = p.ev("()=>__JS.drawer().nmH")
            if tag == 'NEW':
                T('13', u'쪽 줄 — 제1조 전체(11 → 3 쪽) 보임 · 「제7판」 거름(1장) DOM 0 · 서랍 이름 줄 = 한 줄', bool(pr_all and pr_all['vis']) and pr_one is None and n_one == 1 and nmh == [20],
                  {'전체': pr_all, '제7판': pr_one, '장': n_one, '이름 높이': nmh})
            elif tag == 'BASEN':
                T('13-헛', u'헛잣대 — 바탕 앱: 1 쪽인데 「쪽 1」 보임', bool(pr_one and pr_one['vis']), {'제7판': pr_one, '이름 높이': nmh})
            N('panel', tag + u' 오류', p.errs_all()[:5])
        finally:
            p.close()
    # 12 전 조 칩 = 패널(렌더 · Chromium)
    for tag in ('BASE', 'NEW'):
        src, data = E[tag]
        p = Pg(br, 'all' + tag, src, data, W=1440, H=900)
        try:
            out = {}
            for law in (u'특허법', u'상표법', u'디자인보호법'):
                out[law] = p.ev("l=>__JS.chipVsPanelAll(l)", law)
            if tag == 'NEW':
                T('12', u'전 조 칩 N = 패널 「전체」 N(특허 268 · 상표 244 · 디보 238 · 다름 0)', all(not v['diff'] for v in out.values()),
                  {k: (v['n'], len(v['diff']), v['diff'][:3]) for k, v in out.items()})
            else:
                T('12-헛', u'헛잣대 — 바탕 칩(리담만) ≠ 패널 조 수(채팅 198)', any(v['diff'] for v in out.values()), {k: (v['n'], len(v['diff'])) for k, v in out.items()})
        finally:
            p.close()
    # WebKit(아이패드 폭) — 제1조 칩·패널·차례
    src, data = E['NEW']
    p = Pg(wk, 'panelWK', src, data, W=820, H=1100)
    try:
        p.ev("()=>__JS.jo('특허법','제1조',{panel:true,f:'all',p:0})")
        ids = p.ev("()=>__JS.panelAllIds()")
        T('11', u'WebKit 820 — 제1조 칩 11 = 패널 11 · 1번 P7-0208 · 2번 1997', p.ev("()=>__JS.chipN()") == 11 == p.ev("()=>__JS.panelAll()") and ids and ids[0].get('id') == 'P7-0208' and ids[1]['y'] == 1997,
          [(x.get('id') or x['sid'], x['y']) for x in (ids or [])[:4]])
        N('panel', u'WebKit 오류', p.errs_all()[:5])
    finally:
        p.close()


# ══════════ 4 · 5 3법 비교 ══════════
def open_c3(p, tag):
    """3법 칸을 진짜 포인터로 연다 — NEW = 칸 머리 「펴기 ▼」 · 바탕 = 머리 칩 「⇄ 3법 대응」"""
    if p.ev("()=>{const w=__JS.c3();return !!(w&&w.cols&&w.cols.length)}"):
        return True
    at = p.ev("()=>__JS.c3fold()") if tag == 'NEW' else p.ev("()=>__JS.atText('#slot .main .conn button','3법 대응')")
    ok = p.click(at, 900)
    p.ev("()=>__JS.wait(300)")
    return ok and p.ev("()=>{const w=__JS.c3();return !!(w&&w.cols&&w.cols.length)}")


def c3_ok(c):
    if not c or not c['cols']:
        return False
    sang = [x for x in c['cols'] if x['law'] == u'상표']
    return (c['headB'] == u'3법 비교' and not c['cdim'] and c['cand'] == 0 and c['candBtn'] == 0
            and not any(re.match(r'^[0-9.]+$', b) for x in c['cols'] for b in x['badges'])
            and all(x['dashed'] != 'dashed' for x in c['cols'] if 'add' not in x['cls'])
            and sang and sang[0]['k'] == u'제1조' and c['add'] and c['add']['on'] and c['add']['inRow'] and c['rowWrap'] == 'wrap')


def typein(p, v):
    """조·항 칸 입력 — 진짜 포인터로 칸을 누르고 글을 친다 · 값이 안 들어갔으면 한 번 더(누름이 빗나간 것 · 까닭은 칸 정보에)"""
    for i in range(2):
        at = p.ev("()=>__JS.c3pickInput()")
        p.click(at, 200)
        p.pg.keyboard.press('Control+A'); p.type(v); p.pg.wait_for_timeout(700)
        pk = p.ev("()=>__JS.c3pick()")
        if pk and pk.get('inp') == v:
            return dict(pk, tries=i + 1)
    return dict(pk or {}, miss=at, tries=2)


def c3_gates(br, wk):
    # ★ jo_wonmun(9/27) — 정오문제가 본문 위에 뜨는 창(칩 아래 470×640)이 되어 3법 칸(펴기 ▼ · 상표 카드 머리)을 가린다 → 3법 관문은 창 없이(panel:false) 잰다 · 옛 오른쪽 패널은 본문을 좁혔을 뿐 가리지 않았다
    E = envs3()
    # 4 — 꼴(1280 크로미움 · 820 웹킷) · 헛잣대 바탕
    for tag, b, bname, W in (('NEW', br, 'Chromium', 1280), ('NEW', wk, 'WebKit', 820), ('BASE', br, 'Chromium', 1280)):
        src, data = E[tag]
        p = Pg(b, 'c3' + tag + bname, src, data, W=W, H=1000, touch=(bname == 'WebKit'))
        try:
            p.ev("()=>__JS.jo('특허법','제1조',{panel:false})")
            shut = p.ev("()=>__JS.c3()")
            opened = open_c3(p, tag)
            c = p.ev("()=>__JS.c3()")
            ok = c3_ok(c)
            if tag == 'NEW':
                T('4', u'3법 닫힘(%s) — 칸 머리 「3법 비교 · 펴기 ▼」 만(칩 없이 여는 길)' % bname, bool(shut) and shut['headB'] == u'3법 비교' and not shut['cols'] and any(u'펴기' in x for x in shut['btns']), shut)
                T('4', u'3법 비교(%s %d) — 이름 · 설명 글 0 · 점수 0 · 후보 단추 0 · 점선 0 · 상표 = 제1조(1등 후보) · 「+ 조문 추가」 보임(잘림 0) · 줄바꿈' % (bname, W), bool(opened and ok),
                  {'머리': c and c['head'], '카드': c and [(x['law'], x['k'], x['badges'], x['dashed']) for x in c['cols']], '추가': c and c['add'], 'wrap': c and c['rowWrap']})
            else:
                T('4-헛', u'헛잣대 — 바탕 3법 칸은 옛 꼴(⇄ 3법 대응 · 설명 · 점수 · 후보 단추 · 점선)', not ok,
                  {'머리': c and c['head'], '후보 단추': c and c['candBtn'], '점선': c and c['cand'], 'wrap': c and c['rowWrap']})
            N('4', tag + bname + u' 오류', p.errs_all()[:5])
        finally:
            p.close()
    # 5 — 길게 누르기(마우스 · 손가락 · 펜) · 조/항 바꾸기 · 자동 짝 · 짧게 누르기 · 새로고침
    for tag in ('BASEN', 'NEW'):
        src, data = E[tag]
        p = Pg(br, 'lp' + tag, src, data, W=1280, H=1000, touch=True)
        try:
            def fresh():
                p.ev("()=>__JS.jo('특허법','제1조',{panel:false})")
                open_c3(p, 'NEW' if tag == 'NEW' else 'BASE')
                return p.ev("()=>__JS.c3headAt('상표')")
            got = {}
            for how in ('mouse', 'finger', 'pen'):
                h = fresh()
                if not h:
                    got[how] = None
                    continue
                if how == 'mouse':
                    p.hold(h['px'], h['py'], 600)
                elif how == 'finger':
                    p.touch(h['px'], h['py'], 600)
                else:
                    p.pen(h['px'], h['py'], 600)
                pk = p.ev("()=>__JS.c3pick()")
                got[how] = [bool(pk and pk['vis'] and pk['under'] and pk['law'] == u'상표법'), (pk or {}).get('inp')]
            if tag == 'BASEN':
                T('5-헛', u'헛잣대 — 바탕 앱: 상표 카드 머리를 600ms 눌러도 칸이 안 열림', not any(v and v[0] for v in got.values()), got)
                continue
            T('5', u'상표 카드 머리 600ms 누름 → 카드 바로 아래 조·항 칸 — 마우스 · 손가락(CDP 터치 r22) · 펜(CDP 펜)', all(v and v[0] for v in got.values()), got)
            # 8px 넘게 움직이면 취소
            h = fresh()
            p.pg.mouse.move(h['px'], h['py']); p.pg.mouse.down(); p.pg.mouse.move(h['px'] + 12, h['py'] + 2, steps=3); p.pg.wait_for_timeout(650); p.pg.mouse.up(); p.pg.wait_for_timeout(300)
            T('5', u'누른 채 12px 움직이면 취소(칸 안 열림)', p.ev("()=>__JS.c3pick()") is None, '')
            # 104 · 조 전체 → 바꾸기
            h = fresh(); p.hold(h['px'], h['py'], 600)
            pk = typein(p, '104')
            p.click(p.ev("()=>__JS.c3pickBtn('^바꾸기$')"), 1200)
            c = p.ev("()=>__JS.c3()")
            sang = [x for x in (c or {}).get('cols', []) if x['law'] == u'상표']
            tf = p.ev("()=>__JS.themefix()")
            T('5', u'조 「104」 + 항 「조 전체」 → 바꾸기 → 상표 카드 = 제104조 · 손값 themefix = 「제104조」', bool(sang) and sang[0]['k'] == u'제104조' and (tf.get(u'특허법:제1조') or {}).get(u'상표법') == u'제104조',
              {'항 목록(104)': pk and pk['opts'], '카드': sang and sang[0]['k'], 'themefix': tf})
            # 35 · ② → 그 항 줄만
            h = p.ev("()=>__JS.c3headAt('상표')"); p.hold(h['px'], h['py'], 600)
            pk = typein(p, '35')
            p.pg.select_option('#slot .c3pick select', u'②'); p.pg.wait_for_timeout(200)
            p.click(p.ev("()=>__JS.c3pickBtn('^바꾸기$')"), 1200)
            body = p.ev("()=>__JS.c3body('상표')")
            rows = p.ev("()=>__JS.c3hangRows('상표법','제35조','②')")
            want = re.sub(r'\s+', ' ', ' '.join(rows)).strip()
            c = p.ev("()=>__JS.c3()")
            sang = [x for x in (c or {}).get('cols', []) if x['law'] == u'상표']
            tf = p.ev("()=>__JS.themefix()")
            T('5', u'조 「35」 + 항 ② → 카드 = 제35조② · 본문 = 그 항 줄만(호 포함) · 손값 「제35조②」', bool(sang) and sang[0]['k'] == u'제35조②' and body == want and (tf.get(u'특허법:제1조') or {}).get(u'상표법') == u'제35조②',
              {'항 목록(35)': pk and pk['opts'], '카드': sang and sang[0]['k'], '본문': (body or '')[:80], '그 항': want[:80]})
            # 자동 짝으로
            h = p.ev("()=>__JS.c3headAt('상표')"); p.hold(h['px'], h['py'], 600)
            p.click(p.ev("()=>__JS.c3pickBtn('자동 짝')"), 1200)
            c = p.ev("()=>__JS.c3()")
            sang = [x for x in (c or {}).get('cols', []) if x['law'] == u'상표']
            tf = p.ev("()=>__JS.themefix()")
            T('5', u'「자동 짝으로」 → 상표 카드 = 제1조 · 손값 지움', bool(sang) and sang[0]['k'] == u'제1조' and u'상표법' not in (tf.get(u'특허법:제1조') or {}), {'카드': sang and sang[0]['k'], 'themefix': tf})
            # 짧게 누름 = 조문 팝업(칸 안 열림)
            h = p.ev("()=>__JS.c3headAt('상표')")
            p.pg.mouse.click(h['bx']['cx'], h['bx']['cy']); p.pg.wait_for_timeout(900)
            T('5', u'짧게 누름(조 글자) → 조문 팝업 · 칸 안 열림', u'jo|상표법|제1조' in (p.ev("()=>__JS.popKeys()") or []) and p.ev("()=>__JS.c3pick()") is None, p.ev("()=>__JS.popKeys()"))
            p.ev("()=>{try{closeAllPops()}catch(e){}}")
            # 새로고침 뒤 유지 — 제104조로 두고 keep=1 로 다시 열기
            h = p.ev("()=>__JS.c3headAt('상표')"); p.hold(h['px'], h['py'], 600)
            pk3 = typein(p, '104')
            p.click(p.ev("()=>__JS.c3pickBtn('^바꾸기$')"), 1200)
            tf_before = p.ev("()=>__JS.themefix()")
            p.open(keep=True)
            p.ev("()=>__JS.jo('특허법','제1조',{panel:false})")
            open_c3(p, 'NEW')
            c = p.ev("()=>__JS.c3()")
            sang = [x for x in (c or {}).get('cols', []) if x['law'] == u'상표']
            T('5', u'새로고침 뒤 유지 — 상표 카드 = 제104조(손값 · 기록 jopangi.themefix = 동기화 키)', bool(sang) and sang[0]['k'] == u'제104조' and p.ev("()=>__JS.syncHas('themefix')"),
              {'카드': sang and sang[0]['k'], '3법 열림 기억': p.ev("()=>__JS.uiTh()"), '칸': pk3, '새로고침 전 손값': tf_before})
            N('5', tag + u' 오류', p.errs_all()[:5])
        finally:
            p.close()
    # 5 — WebKit(아이패드 폭 · 마우스 길게 · 톡)
    src, data = E['NEW']
    p = Pg(wk, 'lpWK', src, data, W=820, H=1100, touch=True)
    try:
        p.ev("()=>__JS.jo('특허법','제1조',{panel:false})")
        open_c3(p, 'NEW')
        h = p.ev("()=>__JS.c3headAt('상표')")
        p.hold(h['px'], h['py'], 600)
        pk = p.ev("()=>__JS.c3pick()")
        p.ev("()=>__JS.jo('특허법','제1조',{panel:false})")
        h = p.ev("()=>__JS.c3headAt('상표')")
        p.pg.touchscreen.tap(h['bx']['cx'], h['bx']['cy']); p.pg.wait_for_timeout(900)
        keys = p.ev("()=>__JS.popKeys()")
        T('5', u'WebKit 820 — 마우스 600ms 누름 → 칸 열림 · 톡(짧게) → 조문 팝업(칸 안 열림)', bool(pk and pk['vis'] and pk['under']) and u'jo|상표법|제1조' in (keys or []) and p.ev("()=>__JS.c3pick()") is None,
          {'칸': pk, '팝업': keys})
        N('5', u'WebKit 오류', p.errs_all()[:5])
    finally:
        p.close()


# ══════════ 6 조문 팝업 ══════════
def pop_gates(br, wk):
    E = envs3()
    for tag, b, bname, W in (('NEW', br, 'Chromium', 1440), ('NEW', wk, 'WebKit', 820), ('BASE', br, 'Chromium', 1440)):
        src, data = E[tag]
        p = Pg(b, 'pop' + tag + bname, src, data, W=W, H=1000)
        try:
            p.ev("()=>__JS.jo('특허법','제29조',{panel:false})")
            g = p.ev("a=>__JS.popjo(a[0],a[1])", [u'상표법', u'제1조'])
            ok = bool(g and g.get('found') and g['inHead'] and not g['inBody'] and g['afterTitle'] and g['bg'] in ('rgba(0, 0, 0, 0)', 'transparent') and g['fs'] == '11px' and g['bw'] == '0px')
            if tag == 'NEW':
                clicked = p.click(g, 900)
                st = p.ev("()=>__JS.state()")
                T('6', u'조문 팝업(%s) 「뷰로 이동 ↗」 = 머리 줄 안 · 제목 바로 뒤 · 바탕 투명 · 11px · 누르면 그 조 뷰' % bname, ok and clicked and st['tab'] == 'jo' and st['law'] == u'상표법' and st['jo'] == u'제1조' and st['pops'] == 0,
                  {'단추': g, '누른 뒤': st})
            else:
                T('6-헛', u'헛잣대 — 바탕 「뷰로 이동 ↗」 = 본문 맨 위 파란 알약', not ok, {'머리 안': g and g.get('inHead'), '본문 안': g and g.get('inBody'), '바탕': g and g.get('bg'), '크기': g and g.get('fs')})
            N('6', tag + bname + u' 오류', p.errs_all()[:5])
        finally:
            p.close()


# ══════════ 7 서랍 ══════════
def drawer_gates(br, wk):
    E = envs3()
    for tag, b, bname in (('NEW', br, 'Chromium'), ('NEW', wk, 'WebKit'), ('BASE', br, 'Chromium')):
        src, data = E[tag]
        p = Pg(b, 'dr' + tag + bname, src, data, W=(820 if bname == 'WebKit' else 1440), H=1000)
        try:
            res = {}
            for w in (212, 260, 320):
                p.ev("w=>__JS.jo('특허법','제1조',{panel:false,treeW:w})", w)
                res[w] = p.ev("()=>__JS.drawer()")
            if tag == 'NEW':
                okc = all(len(v['bkLeft']) == 1 and len(v['edLeft']) == 1 and len(v['lkLeft']) <= 1 for v in res.values())
                lg = res[212]['legend']
                T('7', u'서랍(%s) 212·260·320px — 빈칸 표지 왼쪽 끝 1 가지 · ✏️ 1 가지 · 🔗 1 가지' % bname, okc, {w: (v['bkLeft'], v['edLeft'], v['lkLeft']) for w, v in res.items()})
                T('7', u'서랍(%s) — 막대 0 · 범례 새 글 · ✏️(U+FE0F) · ★ 개정일 = 이름 바로 뒤' % bname,
                  all(v['bars'] == 0 for v in res.values()) and lg.startswith(u'●●● = 빈칸 내용·주체·기간 · 밑줄 색 = 통과율(≥90 초록 · ≥60 노랑 · 그 외 빨강) · 누르면 그 빈칸') and u'✏️N 내 형광·마크업 수 · 🔗N 인용 링크 수' in lg
                  and bool(res[212]['edEmoji']) and bool(res[212]['starAfterName']) and res[212]['starAfterName']['prev'] == 'nm' and not res[212]['starAfterName']['inEm'],
                  {'범례': lg, '✏': res[212]['edSample'], '★': res[212]['starAfterName']})
                if bname == 'Chromium':
                    col = p.ev("()=>__JS.bkColor()")
                    shade = {}
                    for pk, want in ((95, 'rgb(22, 163, 74)'), (70, 'rgb(217, 119, 6)'), (30, 'rgb(220, 38, 38)')):
                        p.ev("v=>__JS.fakeBlank('제1조',{내용:v})", pk)
                        p.ev("()=>__JS.jo('특허법','제1조',{panel:false,treeW:212})")
                        d = p.ev("()=>__JS.dotOf('제1조')")
                        shade[pk] = [d[0]['bg'], d[0]['sh'], want in (d[0]['sh'] or '')]
                    p.ev("()=>__JS.jo('특허법','제1조',{panel:false,treeW:320})")
                    wide = p.ev("()=>__JS.dotOf('제1조')")
                    T('7', u'흉내 채점 기록(제1조 내용 95·70·30) — 점 색 = 종류 색(내용 파랑) · 밑줄 = 통과율 색(초록·노랑·빨강) · 넓은 서랍 글자도 같은 규칙',
                      all(v[0] == 'rgb(37, 99, 235)' and v[2] for v in shade.values()) and bool(wide) and wide[0]['bg'].startswith('rgba(37, 99, 235') and 'rgb(220, 38, 38)' in wide[0]['sh'],
                      {'점': shade, '넓은 서랍': wide[:1], 'BK_COLOR': col})
            else:
                T('7-헛', u'헛잣대 — 바탕 서랍 212px: 빈칸 표지 자리 여럿(채팅 9) · ✏ 여럿(5) · 막대 있음', len(res[212]['bkLeft']) > 1 and len(res[212]['edLeft']) > 1 and res[212]['bars'] > 0,
                  {w: (len(v['bkLeft']), len(v['edLeft']), v['bars']) for w, v in res.items()})
            N('7', tag + bname + u' 오류', p.errs_all()[:5])
        finally:
            p.close()


# ══════════ 9 카드 꼴 ══════════
def card_gates(br):
    E = envs3()
    for tag in ('BASEN', 'NEW'):
        src, data = E[tag]
        p = Pg(br, 'card' + tag, src, data, W=1440, H=1000)
        try:
            p.ev("()=>__JS.jo('특허법','제1조',{panel:true,f:'all',p:0})")
            sid = 'TR91011'
            p.ev("s=>__JS.pageOf(s)", sid)
            pc = p.ev("s=>__JS.cardShape(s)", sid)
            uc = p.ev("s=>__JS.unitShapeOf(s)", sid)
            f3 = p.ev("()=>__JS.find2003()")
            c3 = None
            if f3:
                p.ev("k=>__JS.jo('특허법',k,{panel:true,f:'all',p:0})", f3['k'])
                p.ev("s=>__JS.pageOf(s)", f3['sid'])
                c3 = p.ev("s=>__JS.cardShape(s)", f3['sid'])
            same = bool(pc and uc and pc['heads'] == uc['heads'] and 'mlnz' in pc['cls'])
            yr = bool(c3 and c3['qbn'] == 0 and not re.search(u'2003·\\d+번', c3['text']) and any(re.match(u'^2003:\\?:', y) for y in c3['yearChips']))
            if tag == 'NEW':
                T('9', u'패널 카드 = 1차객 단원 카드 빌더(mlnLidCard) — 같은 클래스·칩 차례(TR91011)', same, {'패널': pc and pc['heads'], '단원': uc and uc['heads'], 'cls': pc and pc['cls']})
                T('9', u'2003 카드 — 「2003·N번」 글자 0 · 「기출 · 연도·번」 칩 0 · 출제연도 칩 「2003:?:선지」', yr, {'조': f3, '카드': c3})
            else:
                T('9-헛', u'헛잣대 — 바탕 패널 리담 카드 = 전용 꼴(qhd · 「기출 · 2003·N번」)', not same and not yr, {'패널': pc and pc['heads'][:6], '2003': c3 and (c3['qbn'], c3['text'][:60])})
            N('9', tag + u' 오류', p.errs_all()[:5])
        finally:
            p.close()


# ══════════ 14 「이 조 아님 ×」 ══════════
def jn_gates(br):
    E = envs3()
    for tag in ('BASEN', 'NEW'):
        src, data = E[tag]
        p = Pg(br, 'jn' + tag, src, data, W=1440, H=1000)
        try:
            p.ev("()=>__JS.jo('특허법','제1조',{panel:true})")
            m = p.ev("()=>__JS.pickMulti()")
            if not m:
                T('14', u'두 조에 걸린 리담 지문 찾기', False, '')
                continue
            a, b2, sid = m['a'], m['b'], m['sid']
            p.ev("k=>__JS.jo('특허법',k,{panel:true,f:'all',p:0})", a)
            n0 = [p.ev("()=>__JS.chipN()"), p.ev("()=>__JS.panelAll()")]
            p.ev("s=>__JS.pageOf(s)", sid)
            at = p.ev("s=>__JS.typeJoAt(s)", sid)
            if at:
                p.hold(at['cx'], at['cy'], 600)
            menu = p.ev("()=>__JS.jnMenu()")
            if tag == 'BASEN':
                T('14-헛', u'헛잣대 — 바탕 앱: 조 칩을 길게 눌러도 「이 조 아님 ×」 칸 없음', not menu, {'지문': m, '칸': menu})
                continue
            ok1 = bool(menu and any(r[0] == a and u'이 조 아님 ×' in r[2] for r in menu['rows']))
            p.click(p.ev("a=>__JS.jnBtn(a[0],a[1])", [a, u'이 조 아님']), 900)
            p.ev("()=>{try{closeAllPops()}catch(e){}}")
            p.ev("k=>__JS.jo('특허법',k,{panel:true,f:'all',p:0})", a)
            n1 = [p.ev("()=>__JS.chipN()"), p.ev("()=>__JS.panelAll()")]
            ids1 = [x['sid'] for x in p.ev("()=>__JS.panelAllIds()")]
            rec = p.ev("()=>__JS.jonot()")
            T('14', u'조 칩 600ms 누름 → 「이 조 아님 ×」 → 그 조 칩·패널 %s → %s(카드 빠짐) · 손값 jopangi.jonot · 동기화 키' % (n0[1], n1[1]),
              ok1 and n1[0] == n1[1] == n0[1] - 1 and sid not in ids1 and rec == {sid: [a]} and p.ev("()=>__JS.syncHas('jonot')"),
              {'지문': m, '칸': menu, '앞': n0, '뒤': n1, '기록': rec})
            p.open(keep=True)
            p.ev("k=>__JS.jo('특허법',k,{panel:true,f:'all',p:0})", a)
            n2 = [p.ev("()=>__JS.chipN()"), p.ev("()=>__JS.panelAll()")]
            p.ev("k=>__JS.jo('특허법',k,{panel:true,f:'all',p:0})", b2)
            p.ev("s=>__JS.pageOf(s)", sid)
            at = p.ev("s=>__JS.typeJoAt(s)", sid)
            if at:
                p.hold(at['cx'], at['cy'], 600)
            menu2 = p.ev("()=>__JS.jnMenu()")
            p.click(p.ev("a=>__JS.jnBtn(a[0],a[1])", [a, u'되살리기']), 900)
            p.ev("()=>{try{closeAllPops()}catch(e){}}")
            p.ev("k=>__JS.jo('특허법',k,{panel:true,f:'all',p:0})", a)
            n3 = [p.ev("()=>__JS.chipN()"), p.ev("()=>__JS.panelAll()")]
            T('14', u'새로고침 뒤 유지(%s) · 다른 조(%s) 카드에서 길게 눌러 「되살리기」 → %s · 기록 칸 지움' % (n2[1], b2, n3[1]),
              n2 == n1 and bool(menu2 and any(r[0] == a and 'gone' in r[1] for r in menu2['rows'])) and n3 == n0 and not (p.ev("()=>__JS.jonot()") or {}),
              {'새로고침': n2, '칸': menu2, '되살린 뒤': n3, '기록': p.ev("()=>__JS.jonot()")})
            N('14', tag + u' 오류', p.errs_all()[:5])
        finally:
            p.close()


# ══════════ 10 회귀 — 조문 탭 밖 DOM(같은 새 데이터로 바탕 앱 ↔ 새 앱) · 기록 키 ══════════
def reg_gates(br):
    E = envs3()
    shots, keys = {}, {}
    for tag in ('BASE', 'BASEN', 'NEW'):
        src, data = E[tag]
        p = Pg(br, 'reg' + tag, src, data, W=1440, H=1000)
        try:
            keys[tag] = p.ev("()=>__JS.gaekHome('특허법').then(()=>__JS.poolKeys())")
            if tag == 'BASE':
                continue
            out = {}
            out[u'1차객 특허 첫 화면'] = p.ev("()=>__JS.dump()")
            p.ev("()=>__JS.gaekGo('__미분류')")
            out[u'1차객 특허 미분류'] = p.ev("()=>__JS.dump()")
            for law in (u'상표법', u'디자인보호법'):
                p.ev("l=>__JS.gaekHome(l)", law)
                out[u'1차객 ' + law[:2] + u' 첫 화면'] = p.ev("()=>__JS.dump()")
            for t, extra, nm in (('prec', {'law': u'특허법'}, u'판례 특허'), ('prec', {'law': u'상표법'}, u'판례 상표'), ('cha2', {'law': u'특허법'}, u'2차 특허'), ('omr', {'law': u'특허법'}, u'정리 특허')):
                p.ev("a=>__JS.tab(a[0],a[1])", [t, extra])
                out[nm] = p.ev("()=>__JS.dump()")
            shots[tag] = out
            N('10', tag + u' 오류', p.errs_all()[:5])
        finally:
            p.close()
    import difflib
    summ = {}
    for k in shots['NEW']:
        A = shots['BASEN'].get(k, '').split('\n'); C = shots['NEW'].get(k, '').split('\n')
        sm = difflib.SequenceMatcher(None, A, C, autojunk=False)
        ops = [(t, ' / '.join(A[i1:i2])[:80], ' / '.join(C[j1:j2])[:80]) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal']
        summ[k] = {'줄': [len(A), len(C)], '바뀐 조각': len(ops), '예': ops[:4]}
    T('10', u'조문 탭 밖 화면 글 = 바탕 앱(같은 새 데이터) — 1차객 첫 화면 셋·특허 미분류·판례 특허/상표·2차·정리', all(v['바뀐 조각'] == 0 for v in summ.values()), summ)
    b, n = set(keys['BASE'] or []), set(keys['NEW'] or [])
    T('10', u'기록 열쇠 무변 — 1차객 특허 풀 열쇠(바탕 앱+데이터) = 새 앱+새 데이터', b == n and len(b) > 300, {'바탕': len(b), '새': len(n), '없어짐': sorted(b - n)[:6], '새로': sorted(n - b)[:6]})
    io.open(os.path.join(WORK, 'reg_joscreen_screens.json'), 'w', encoding='utf-8').write(json.dumps(shots, ensure_ascii=False))


def report():
    P = sum(1 for r in RES if r[2] is True)
    F = [r for r in RES if r[2] is False]
    lines = ['# _harness_jo_joscreen 결과 — %s' % time.strftime('%Y-%m-%d %H:%M'), '',
             'NEW 앱 %s (LF md5 %s) · NEW 데이터 %s · BASE %s' % (NEWF, hashlib.md5(open(NEWF, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:8], DATA, BASE_REV),
             'PASS %d · FAIL %d · INFO %d' % (P, len(F), sum(1 for r in RES if r[2] is None)), '']
    for g, n, ok, d in RES:
        lines.append('%s | %s · %s | %s' % ('INFO' if ok is None else ('PASS' if ok else 'FAIL'), g, n,
                                           d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str)[:1500]))
    f = os.path.join(OUT, '_harness_jo_joscreen_result.txt')
    io.open(f, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print('\n== PASS %d · FAIL %d → %s' % (P, len(F), f))
    return len(F)


def main():
    os.makedirs(WORK, exist_ok=True)
    pairs = want = p7want = None
    if not ONLY or 'data' in ONLY or 'rule' in ONLY:
        pairs, want, p7want = data_gates()
    parts = [('rule', None), ('head', head_gates), ('panel', panel_gates), ('c3', c3_gates), ('pop', pop_gates), ('drawer', drawer_gates),
             ('card', card_gates), ('jn', jn_gates), ('reg', reg_gates)]
    if any(not ONLY or k in ONLY for k, _ in parts):
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            wk = pw.webkit.launch()
            try:
                for k, fn in parts:
                    if ONLY and k not in ONLY:
                        continue
                    try:
                        if k == 'rule':
                            rule_gates(br, pairs, want, p7want)
                        elif fn in (head_gates, panel_gates, c3_gates, pop_gates, drawer_gates):
                            fn(br, wk)
                        else:
                            fn(br)
                    except Exception as e:
                        T('RUN', u'%s 묶음이 멈춤' % k, False, repr(e)[:600])
            finally:
                wk.close()
                br.close()
    sys.exit(1 if report() else 0)


if __name__ == '__main__':
    main()
