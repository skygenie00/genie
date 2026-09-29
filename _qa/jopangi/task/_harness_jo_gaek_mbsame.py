# -*- coding: utf-8 -*-
r"""_task_jo_gaek_mbsame(+add1) 관문 하네스 — 본판 §G 1~15 + add1 §D 1~7.

  python _harness_jo_gaek_mbsame.py [--new <앱>] [--data <jo/data>] [--exam <gichul/pdf>] [--out <폴더>] [--only a,b,...]

  NEW  = 패치한 앱(기본 genie 작업트리 jo/index.html) + 새 데이터 + 새 시험지(기본 genie 작업트리)
  BASE = genie HEAD(17094a5 = uid 판) 앱 + HEAD jo/data + HEAD gichul/pdf — 칸마다 헛잣대(바탕에서 FAIL)
  누름 = 진짜 포인터(page.mouse · 손가락 = CDP 터치 반지름 22) · 보임 = display ≠ none · 높이 > 0 · 자리 = elementFromPoint
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import io, json, os, re, sys, time, csv, hashlib, shutil, subprocess, tempfile, threading, socketserver, http.server, urllib.parse, collections, tarfile
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), u'공통', u'_harness'))
import _harness_canvas_jari as CJ          # noqa: E402 — SEED · VENDOR · route_filter · NOISE
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = CJ.GENIE
JOD = os.path.join(GENIE, 'jo')
NEWF = ARG('--new', os.path.join(JOD, 'index.html'))
DATA = ARG('--data', os.path.join(JOD, 'data'))
EXAM = ARG('--exam', os.path.join(GENIE, 'gichul', 'pdf'))
OUT = ARG('--out', HERE)
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
BASE_REV = ARG('--base', '17094a5')
WORK = os.path.join(tempfile.gettempdir(), 'h_gaekmbs')
TESTS = io.open(os.path.join(HERE, '_harness_jo_gaek_mbsame_tests.js'), encoding='utf-8').read()
READY = "!!window.__HM&&typeof render==='function'"
TAB = os.path.join(os.path.dirname(HERE), u'특상디', u'_gaek_mb', u'_객관식63_판정.csv')
RES = []
SERVERS = {}


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:300]))


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:300]))


def git(*a):
    return subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def head_tree(sub, dst):
    """genie HEAD 의 폴더 하나를 풀어 둔다(바탕 데이터·시험지)"""
    if os.path.isdir(dst) and os.listdir(dst):
        return dst
    os.makedirs(dst, exist_ok=True)
    raw = git('archive', '--format=tar', BASE_REV, sub)
    with tarfile.open(fileobj=io.BytesIO(raw)) as tf:
        tf.extractall(dst)
    return dst


def serve(tag, src, data, exam):
    key = tag + '|' + data + '|' + exam
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
    def __init__(self, br, tag, src, data, exam, remote=None, keep=False, W=1440, H=900, port=None, ctx=None, touch=False):
        self.port = port or serve(tag, src, data, exam)
        self.ctx = ctx or br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, has_touch=touch)
        self.ctx.route('**/*', CJ.route_filter)
        if remote is not None:
            self.ctx.add_init_script('window.__REMOTE={text:%s,sha:"H_seed",puts:0};' % json.dumps(remote, ensure_ascii=False))
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(180000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' else None)
        self.pg.goto('http://127.0.0.1:%d/index.html?tok=1&who=%s%s' % (self.port, urllib.parse.quote('꼬까'), '&keep=1' if keep else ''), wait_until='load', timeout=180000)
        self.pg.wait_for_function(READY, timeout=180000)
        self.pg.wait_for_timeout(700)
        self.cdp = None

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def until(self, expr, arg=None, ms=15000):
        t0 = time.time()
        while time.time() - t0 < ms / 1000:
            v = self.ev(expr, arg)
            if v:
                return v
            self.pg.wait_for_timeout(100)
        return self.ev(expr, arg)

    def click(self, at, wait=500):
        if not at or not at.get('on'):
            return False
        self.pg.mouse.click(at['cx'], at['cy'])
        self.pg.wait_for_timeout(wait)
        return True

    def tap(self, at, wait=500):
        """손가락 — CDP 터치(반지름 22 · 아이패드 손가락과 같은 면적)"""
        if not at or not at.get('on'):
            return False
        if not self.cdp:
            self.cdp = self.ctx.new_cdp_session(self.pg)
        pt = {'x': at['cx'], 'y': at['cy'], 'radiusX': 22, 'radiusY': 22, 'force': 1, 'id': 1}
        self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [pt]})
        self.pg.wait_for_timeout(60)
        self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        self.pg.wait_for_timeout(wait)
        return True

    def errs_all(self):
        return [y for y in (self.errs + (self.ev("()=>__HM.errs()") or [])) if not CJ.NOISE(y)]

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


def base_env():
    hd = head_tree('jo/data', os.path.join(WORK, 'head', 'jo_data'))
    he = head_tree('gichul/pdf', os.path.join(WORK, 'head', 'gichul_pdf'))
    return git('show', '%s:jo/index.html' % BASE_REV).decode('utf-8'), os.path.join(hd, 'jo', 'data'), os.path.join(he, 'gichul', 'pdf')


def new_env():
    return io.open(NEWF, encoding='utf-8').read(), DATA, EXAM


# ══════════ 데이터 관문(§A-4 · §C 시험지 · 11 · 5) ══════════
def data_gates():
    P = json.load(io.open(os.path.join(DATA, 'jimun_7pan.json'), encoding='utf-8'))
    bs, bd, be = base_env()
    B = json.load(io.open(os.path.join(bd, 'jimun_7pan.json'), encoding='utf-8'))
    Z = {z['id']: z for z in P['지문']}
    T7 = list(csv.DictReader(io.StringIO(open(TAB, 'rb').read().decode('utf-8-sig'))))
    bad, cnt_lines, cnt_tab, one, e1 = [], 0, 0, [], None
    circ = u'①②③④⑤'
    for tr in T7:
        pid, gal = tr['P7 id'], tr[u'갈래'][:1]
        tab = dict(re.findall(u'([①-⑤ㄱ-ㅅ가-사])\\s*([OX])', tr[u'선지별 O/X']))
        kids = {z[u'선지'] if isinstance(z.get(u'선지'), str) else circ[z[u'선지'] - 1]: z for z in P['지문'] if z.get(u'문항') == pid}
        if gal in 'AB':
            cnt_tab += len(tab); cnt_lines += len(kids)
            for lab, ox in tab.items():
                z = kids.get(lab)
                if not z or z['ox'] != ox:
                    bad.append((pid, lab, ox, z and z['ox']))
        elif gal == 'C':
            one.append((pid, len(kids), pid in {o['id'] for o in P[u'객관식']}))
        else:
            e1 = (pid, len(kids), Z.get(pid) is not None)
    T('11', u'객관식 A·B 56 문항 — 쪼갠 줄 수 = 표 선지 수 · 줄마다 정답 = 표 O/X', not bad and cnt_lines == cnt_tab, {'줄': cnt_lines, '표': cnt_tab, '어긋남': bad[:6]})
    T('11', u'C 6 문항째 한 카드(쪼갠 줄 0 · 객관식에 남음)', len(one) == 6 and all(k == 0 and o for _, k, o in one), one)
    N('11', u'E 1(P7-0069) — 표의 「14번 · 답 O · 한 줄」 은 책 pdf 26쪽 14번(P7-0068 · 이미 OX 한 줄)이고 P7-0069 는 15번 「모두 고르기」 → 손대지 않음(지시서 「표와 다르면 멈추고 보고」)', e1)
    z8 = [z for z in P['지문'] if z.get(u'문항') == 'P7-1209']
    T('11', u'pdf 356쪽 8번(P7-1209) 추록 답 ③ · ㄹ O · 줄 ㄱX ㄴX ㄷO ㄹO ㅁX', ''.join(z['ox'] for z in sorted(z8, key=lambda x: x[u'선지'])) == 'XXOOX', [(z[u'선지'], z['ox']) for z in z8])
    bsplit = sum(1 for z in B['지문'] if z.get(u'문항') in {tr['P7 id'] for tr in T7})
    T('11-헛', u'헛잣대 — 바탕은 63 문항이 쪼갠 줄 0(한 줄씩·객관식)', bsplit == 0, {'바탕 쪼갠 줄': bsplit})
    # 시험지 목록(§C · add1 §B)
    L0 = open(os.path.join(EXAM, 'list.json'), 'rb').read()
    Lh = git('show', '%s:gichul/pdf/list.json' % BASE_REV)   # blob 그대로(git archive 는 autocrlf 로 CRLF 가 된다)
    lists = {}
    for k in ('teukheo', 'sangpyo', 'dibo'):
        p = os.path.join(EXAM, 'list_%s.json' % k)
        J = json.load(io.open(p, encoding='utf-8')) if os.path.exists(p) else {'items': []}
        ok = []
        for it in J['items']:
            f = os.path.join(EXAM, it['file'])
            b = open(f, 'rb').read() if os.path.exists(f) else b''
            ok.append(len(b) == it['bytes'] and hashlib.sha256(b).hexdigest() == it['hash'])
        lists[k] = (len(J['items']), all(ok))
    T('5', u'list_teukheo/sangpyo/dibo.json 19 · 19 · 19 · 바이트·sha256 = 파일', all(v == (19, True) for v in lists.values()), lists)
    T('5', u'기출서재 list.json 바이트 무변(바탕과 같음)', L0 == Lh, {'새': len(L0), '바탕': len(Lh)})
    T('5-헛', u'헛잣대 — 바탕 genie 에 list_teukheo.json 없음', not os.path.exists(os.path.join(be, 'list_teukheo.json')), be)


# ══════════ 앱 관문 ══════════
def unit_gates(br):
    ns, nd, ne = new_env()
    bs, bd, be = base_env()
    p = Pg(br, 'unitN', ns, nd, ne)
    try:
        p.ev("()=>__HM.home('특허법')")
        ok = p.ev("()=>__HM.ok()")
        N('0', u'NEW 켜짐', ok)
        lc = p.ev("()=>__HM.lineCensus()")
        fs = p.ev("()=>__HM.firstScreenCounts()")
        dw = p.ev("()=>__HM.drawerCounts()")
        mism = [k for k, v in fs['map'].items() if k in dw and dw[k] != v]
        T('1', u'단원 줄 — 흡수 + (변형) + (미수록) = 리담 선지 전체(붙은 마디마다) · (변형)∩본편 uid = 기출변형 두 곳', lc.get('sumOK'),
          {k: lc.get(k) for k in ('b', 'u', 'v', 'absSeen', 'lidSeen', 'vAbs', 'nodes')})
        T('1', u'단원 줄 — 첫 화면 줄 셈 = 서랍 줄 셈(다름 0) · 단원 줄(미수록·변형) 줄이 선다', not mism and fs['lines'] > 0, {'첫 화면 줄': fs['rows'], '단원 줄': fs['lines'], '다름': mism[:5]})
        heat = p.ev("()=>__HM.heatTotal()")
        N('1', u'히트맵 칸(풀 열쇠) — 본편 전부 + 문항째 카드 + 흡수 안 된 리담 선지 · 같은 열쇠 한 번', heat)
        # 2 · 한 지문 = 한 카드 — 균등론
        gi = p.ev("()=>__HM.nodeByTitle('균등론')")
        res = {}
        for ln in ('b', 'u', 'v'):
            sel = '__mg%d%s' % (gi, '' if ln == 'b' else '~' + ln)
            p.ev("s=>__HM.go(s)", sel)
            uc = p.ev("()=>__HM.unitCards()")
            res[ln] = {'n': uc['n'], 'qcard': uc['qcard'], 'kinds': collections.Counter(uc['kinds']), 'labs': uc['labs'][:4], 'boxes': uc['boxes']}
        p.ev("s=>__HM.go(s)", '__mg%d' % gi)
        so = p.ev("()=>__HM.sunOrder()")
        ab = p.ev("()=>__HM.absorbedCheck('2010','8','3')")
        T('2', u'한 지문 = 한 카드 — 단원 화면 qCard 0(본편·미수록·변형) · 본편 차례 = 순', all(v['qcard'] == 0 for v in res.values()) and so['ok'],
          {'균등론': res, '순': so})
        T('2', u'리담 2010-47 8번 (3) = 본편 제7판 줄에 흡수(따로 카드 없음)', ab.get('cls') == 'a' and ab.get('p7') and not ab.get('zcard'), ab)
        # 3 · 번호
        yj = p.ev("()=>__HM.p7ByPdf(430,'유제')")
        y12 = p.ev("()=>__HM.p7ByPdf(339,'.')")
        k25 = yj[0]['key'] if yj else None
        sp = [x for x in y12 if x.get(u'문항')]
        info25 = info12 = None
        if k25:
            p.ev("k=>__HM.goKey(k)", k25); info25 = p.ev("k=>__HM.cardInfo(k)", k25)
        if sp:
            p.ev("k=>__HM.goKey(k)", sp[2]['key'] if len(sp) > 2 else sp[0]['key']); info12 = p.ev("k=>__HM.cardInfo(k)", sp[2]['key'] if len(sp) > 2 else sp[0]['key'])
        multi = p.ev("()=>{const o=Object.values(VJ.P7map).filter(z=>/-유제\\d$/.test(z.책번호||''));return o.slice(0,4).map(z=>[z.id,z.책번호,z.pdf쪽]);}")
        T('3', u'번호 — pdf 430 「25-유제」 꼴 · 「11-유제1」「11-유제2」 꼴 · 쪼갠 객관식 「12번 - (3)」(pdf 339) · 머리 카드 순번 없음',
          bool(info25 and re.search(u'-유제$', info25['bk']) and info12 and re.search(u'번 - \\(\\d\\)$', info12['bk']) and multi and not info25['hasSeqHead'] and not info12['hasSeqHead']),
          {'430': info25 and info25['bk'], '339': info12 and info12['bk'], '유제N': multi})
        # 4 · 칩 차례 · 📍
        i4 = info12 or info25
        seq = [k for k, _ in (i4 or {}).get('seq', [])]
        want = [u'출처', u'유형', u'출제연도', u'ID']
        pos = [seq.index(k) if k in seq else -1 for k in want]
        order_ok = all(x >= 0 for x in pos) and pos == sorted(pos) and (u'🃏' in seq and seq.index(u'🃏') > pos[-1])
        T('4', u'칩 차례 — 출처 → 유형 → 출제연도 → ID → (↩·📎·📖·🔗) → 🃏 · 📍 = 오른쪽 아이콘 첫째 · 출처 「NN 변리」 · ID = uid 만',
          bool(order_ok and i4['icons'] and i4['icons'][0] == u'📍' and re.match(u'^\\d\\d ', dict(i4['seq']).get(u'출처', '')) and not dict(i4['seq']).get('ID', '').startswith('ID ')),
          {'차례': seq, '아이콘': (i4 or {}).get('icons', [])[:7]})
        errs = p.errs_all()
        T('APP', u'오류 0(NEW 단원·카드)', not errs, errs[:4])
    finally:
        p.close()
    q = Pg(br, 'unitB', bs, bd, be)
    try:
        q.ev("()=>__HM.home('특허법')")
        fsb = q.ev("()=>__HM.firstScreenCounts()")
        T('1-헛', u'헛잣대 — 바탕 첫 화면에 단원 줄(미수록·변형) 0', fsb['lines'] == 0, {'바탕 단원 줄': fsb['lines']})
        gi = q.ev("()=>__HM.nodeByTitle('균등론')")
        q.ev("s=>__HM.go(s)", '__mg%d' % gi)
        ucb = q.ev("()=>__HM.unitCards()")
        T('2-헛', u'헛잣대 — 바탕 균등론 화면에 리담 묶음 카드(qCard) 있음', ucb['qcard'] > 0, {'qcard': ucb['qcard'], 'n': ucb['n']})
        k = q.ev("()=>{const z=Object.values(VJ.P7map).find(z=>String(z.pdf쪽)==='339');return z?oxKeyP7(z):null}")
        if k:
            q.ev("k=>{const P=(OXPOOL||{})[k];return P?gotoJimun('P',P.id,P.dom):null}", k); q.pg.wait_for_timeout(800)
        ib = q.ev("k=>__HM.cardInfo(k)", k) if k else None
        T('3·4-헛', u'헛잣대 — 바탕 카드 머리에 순번 「N번」 · 📍 가 오른쪽 첫째 아님', bool(ib and (ib['hasSeqHead'] or not ib['icons'] or ib['icons'][0] != u'📍')), ib)
    finally:
        q.close()


def chip_gates(br):
    ns, nd, ne = new_env()
    bs, bd, be = base_env()
    p = Pg(br, 'chipN', ns, nd, ne)
    try:
        p.ev("()=>__HM.home('특허법')")
        # 5 · 2016 칩 → 시험지 · 2005 흐림 → 토스트
        k16 = p.ev("""()=>{const q=(VJ.qs||[]).find(q=>String(q.연도)==='2016'&&q.시험문번);if(!q)return null;const z=q.지문[2];
          const k=oxKeyLid(q,z);const P=OXPOOL[k];return P?k:null}""")
        c16 = None
        if k16:
            p.ev("k=>__HM.goKey(k)", k16)
            p.pg.wait_for_timeout(1500); p.ev("k=>__HM.goKey(k)", k16)
            c16 = p.ev("([k,r])=>__HM.chipAt(k,r)", [k16, '^2016:\\d+:'])
        clicked = p.click(c16, 2500)
        pop = p.until("()=>{const x=__HM.pop('^cv\\\\|exam\\\\|2016-1-teukheo');return x&&x.canvas&&x.bdVis?x:null}", ms=20000)
        T('5', u'출제연도 칩 「2016:N:선지」 page.mouse.click → 그 해 특허 시험지 쪽 팝업 보임 · 문번 빨간 테 · 선지 노란 띠', bool(clicked and pop and pop['vis'] and pop['bd'] and pop['bn']), {'칩': c16 and c16.get('t'), '창': pop})
        p.ev("()=>__HM.closeAll()")
        k05 = p.ev("""()=>{const q=(VJ.qs||[]).find(q=>String(q.연도)==='2005');if(!q)return null;return oxKeyLid(q,q.지문[0])}""")
        c05 = None
        if k05:
            p.ev("k=>__HM.goKey(k)", k05); c05 = p.ev("([k,r])=>__HM.chipAt(k,r)", [k05, '^2005:'])
        p.ev("()=>{window.__TOASTS.length=0}")
        p.click(c05, 800)
        pops05 = p.ev("()=>__HM.popKeys()")
        toasts = p.ev("()=>__HM.toasts()")
        faded_ok = bool(c05 and 'fd' in c05['cls'] and (any(u'시험지가 없' in t for t in toasts) or any(x.startswith('gi|') for x in pops05)))
        T('5', u'2005 칩 흐림(opacity .45) → 누르면 토스트 「그 해 시험지가 없습니다」(문번 모름 「?」 이면 그 해 기출뷰 문항 팝업)', faded_ok, {'칩': c05, '토스트': toasts, '창': pops05})
        p.ev("()=>__HM.closeAll()")
        yrs = {}
        for y in range(2008, 2027):
            for law in (u'특허법', u'상표법', u'디자인보호법'):
                r = p.ev("([l,y])=>__HM.jxeIdx(l,y)", [law, y])
                n0 = {u'특허법': 20, u'상표법': 10, u'디자인보호법': 10}[law]
                yrs['%d %s' % (y, law[:2])] = (r or {}).get('found')
        low = {k: v for k, v in yrs.items() if not v}
        N('5', u'해마다 시험지 문번 잡힘 수(앱 색인 = 민법 mbxIndex 규칙 · 법마다 자른 PDF 에 든 문번)', yrs)
        T('5', u'해마다 · 법마다 문번 0 인 시험지 없음(57장)', not low, low)
        # 12 · 링크 4 + 상표 칩
        res12 = {}
        for pid in ('P7-0004', 'P7-0021'):
            kk = p.ev("id=>{const z=VJ.P7map[id];return z?oxKeyP7(z):null}", pid)
            p.ev("k=>__HM.goKey(k)", kk); p.pg.wait_for_timeout(1500); p.ev("k=>__HM.goKey(k)", kk)
            res12[pid] = {'chips': p.ev("k=>__HM.chips(k)", kk), 'src': (p.ev("k=>__HM.cardInfo(k)", kk) or {}).get('seq', [[None, None]])[0][1]}
        c4 = [c[0] for c in (res12['P7-0004']['chips'] or [])]
        c21 = [c[0] for c in (res12['P7-0021']['chips'] or [])]
        T('12', u'링크 틀림 — pdf 13쪽 1번(TH050004) 출처 「05 변리」 그대로 · 칩 「2003:?:③」 + 「상표 2003:?:③」 보임 · pdf 16쪽 17번(TR03071) 「2003:?:①」 + 「상표 2003:?:①」',
          res12['P7-0004']['src'] == u'05 변리' and u'2003:?:③' in c4 and u'상표 2003:?:③' in c4 and u'2003:?:①' in c21 and u'상표 2003:?:①' in c21, res12)
        kk = p.ev("id=>oxKeyP7(VJ.P7map[id])", 'P7-0004')
        p.ev("k=>__HM.goKey(k)", kk)
        cs = p.ev("([k,r])=>__HM.chipAt(k,r)", [kk, u'^상표 2003'])
        p.click(cs, 1500)
        gp = p.until("()=>__HM.popKeys().find(x=>/^gi\\|상표법\\|/.test(x))", ms=6000)
        p.ev("()=>__HM.closeAll()")
        ct = p.ev("([k,r])=>__HM.chipAt(k,r)", [kk, u'^2003'])
        p.click(ct, 1500)
        gt = p.until("()=>__HM.popKeys().find(x=>/^gi\\|/.test(x))", ms=6000)
        T('12', u'칩 누름 → 각 법 기출뷰 그 문항 팝업(상표 칩 = 상표 · 특허 칩 = 특허 · 문번 모름)', bool(gp and gt), {'상표': gp, '특허': gt})
        p.ev("()=>__HM.closeAll()")
        # add1 D5 · 상표·디보 칩
        res5 = {}
        for law in (u'상표법', u'디자인보호법'):
            p.ev("l=>__HM.home(l)", law)
            k = p.ev("""()=>{const q=(VJ.qs||[]).find(q=>String(q.연도)==='2016'&&q.시험문번);return q?oxKeyLid(q,q.지문[0]):null}""")
            p.ev("()=>__HM.go('__미분류')")
            p.ev("k=>{const P=(OXPOOL||{})[k];const pg=(OXDOMPG||{})[P&&P.dom];return pg!=null?__HM.page(pg):null}", k)
            cc = p.ev("""k=>{const q=(VJ.qs||[]).find(q=>q.지문.some(z=>oxKeyLid(q,z)===k));const c=document.getElementById('qb-'+q.id);if(!c)return null;
              const b=[...c.querySelectorAll('.jxec')].find(x=>/^2016:\\d+:/.test(x.textContent));if(!b)return null;b.scrollIntoView({block:'center'});
              const r=b.getBoundingClientRect();const at=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return {cx:r.left+r.width/2,cy:r.top+r.height/2,on:!!at&&(at===b||b.contains(at)),t:b.textContent}}""", k)
            p.click(cc, 2500)
            f = '2016-1-%s' % ('sangpyo' if law == u'상표법' else 'dibo')
            pw = p.until("f=>{const x=__HM.pop('^cv\\\\|exam\\\\|'+f);return x&&x.canvas&&x.bdVis?x:null}", f, ms=20000)
            res5[law] = {'칩': cc and cc.get('t'), '창': pw and {k2: pw[k2] for k2 in ('pk', 'vis', 'bd', 'bn')}}
            p.ev("()=>__HM.closeAll()")
        T('D5', u'add1 — 상표·디보 1차객 2016 칩 page.mouse.click → 그 법 시험지 쪽 팝업 보임 · 문번 빨간 테', all(v['창'] and v['창']['vis'] and v['창']['bd'] for v in res5.values()), res5)
        # add1 D6 · 다섯 해(2020)
        p.ev("()=>__HM.home('특허법')")
        r20 = {}
        for law in (u'특허법', u'상표법', u'디자인보호법'):
            r20[law] = p.ev("([l,y])=>__HM.jxeIdx(l,y)", [law, 2020])
        k20 = p.ev("""()=>{const q=(VJ.qs||[]).find(q=>String(q.연도)==='2020'&&q.시험문번);return q?oxKeyLid(q,q.지문[1]):null}""")
        p.ev("k=>__HM.goKey(k)", k20); p.pg.wait_for_timeout(800)
        c20 = p.ev("([k,r])=>__HM.chipAt(k,r)", [k20, '^2020:\\d+:'])
        p.click(c20, 2500)
        pw20 = p.until("()=>{const x=__HM.pop('^cv\\\\|exam\\\\|2020-1-teukheo');return x&&x.canvas&&x.bdVis?x:null}", ms=20000)
        T('D6', u'add1 — 다섯 해(ABBYY 판) 2020 특허 칩 → 빨간 테 보임 · 2020 세 법 문번 잡힘', bool(pw20 and pw20['bd']) and all((v or {}).get('found') for v in r20.values()), {'창': pw20, '색인': r20})
        errs = p.errs_all()
        T('APP', u'오류 0(NEW 칩·시험지)', not errs, errs[:4])
    finally:
        p.close()
    q = Pg(br, 'chipB', bs, bd, be)
    try:
        q.ev("()=>__HM.home('특허법')")
        kk = q.ev("id=>{const z=VJ.P7map[id];return z?oxKeyP7(z):null}", 'P7-0004')
        q.ev("k=>{const P=(OXPOOL||{})[k];return P?gotoJimun('P',P.id,P.dom):null}", kk); q.pg.wait_for_timeout(900)
        cb = q.ev("k=>__HM.chips(k)", kk)
        T('5·12-헛', u'헛잣대 — 바탕 카드에 출제연도 칩(→ 시험지) 없음', not cb, cb)
    finally:
        q.close()


def card_gates(br):
    ns, nd, ne = new_env()
    bs, bd, be = base_env()
    p = Pg(br, 'cardN', ns, nd, ne)
    try:
        p.ev("()=>__HM.home('특허법')")
        # 6 · (변형) 📖 · 흡수된 기출변형 선지 O → 본편 같은 카드도 O
        vk = p.ev("""()=>{for(let i=0;i<VJ.M.length;i++){const d=mlnDirect(VJ.M,i,VJ.P7map,VJ.byId);const c=d.v.find(c=>mlnBestBon(c.q,c.z));if(c)return {i,k:oxKeyLid(c.q,c.z),uid:c.z.uid,abs:MLN.p7uid.has(c.z.uid)}}return null}""")
        r6 = {}
        if vk:
            p.ev("s=>__HM.go(s)", '__mg%d~v' % vk['i'])
            pg = p.ev("k=>(OXDOMPG||{})['qb-'+k]", vk['k'])
            if pg:
                p.ev("n=>__HM.page(n)", pg)
            bb = p.ev("([k,r])=>__HM.btnIn(k,r)", [vk['k'], u'^📖'])
            p.click(bb, 1200)
            r6['📖'] = bb and bb.get('t'); r6['창'] = p.until("()=>__HM.popKeys().find(x=>/^q\\|📝 지문 /.test(x))", ms=5000)
            p.ev("()=>__HM.closeAll()")
        T('6', u'(변형) 카드 📖 page.mouse.click → 본문(닮은 책 줄) 지문 팝업', bool(r6.get('창')), {'표본': vk, **r6})
        ak = p.ev("""()=>{for(let i=0;i<VJ.M.length;i++){const d=mlnDirect(VJ.M,i,VJ.P7map,VJ.byId);const c=d.v.find(c=>MLN.p7uid.has(c.z.uid));if(c)return {i,k:oxKeyLid(c.q,c.z)}}return null}""")
        r6b = {}
        if ak:
            p.ev("s=>__HM.go(s)", '__mg%d~v' % ak['i'])
            pg = p.ev("k=>(OXDOMPG||{})['qb-'+k]", ak['k'])
            if pg:
                p.ev("n=>__HM.page(n)", pg)
            ob = p.ev("k=>{const c=document.getElementById('qb-'+k);const b=c&&[...c.querySelectorAll('.oxrow button')].find(x=>x.textContent.trim()==='O');if(!b)return null;b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();const at=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return{cx:r.left+r.width/2,cy:r.top+r.height/2,on:!!at&&(at===b||b.contains(at))}}", ak['k'])
            p.click(ob, 600)
            r6b['기록'] = p.ev("k=>__HM.oxRec(k)", ak['k'])
            p.ev("k=>__HM.goKey(k)", ak['k'])
            r6b['본편 카드'] = p.ev("k=>{const c=document.getElementById('qb-'+k);if(!c)return null;const b=[...c.querySelectorAll('.oxrow button')].find(x=>x.textContent.trim()==='O');return {mln:c.dataset.mln||'',sel:b?b.className:null}}", ak['k'])
        T('6', u'흡수된 기출변형 선지에서 O page.mouse.click → 본편 같은 uid 카드도 O(같은 열쇠)', bool(r6b.get('기록') and r6b['기록'].get('m') == 'O' and r6b.get('본편 카드') and 'sel' in str(r6b['본편 카드'].get('sel'))), {'표본': ak, **r6b})
        # 7 · 종합사례 상자
        p.ev("k=>__HM.goKey(k)", p.ev("()=>{const z=Object.values(VJ.P7map).find(z=>String(z.pdf쪽)==='340'&&z.문항);return z?oxKeyP7(z):null}"))
        box340 = p.ev("""()=>{const zs=Object.values(VJ.P7map).filter(z=>String(z.pdf쪽)==='340'&&z.문항);if(!zs.length)return null;const q=zs[0].문항;
          const cs=zs.filter(z=>z.문항===q).map(z=>document.getElementById('qb-'+oxKeyP7(z)));const bx=cs.map(c=>c&&c.closest('.p7case'));return {q,n:cs.length,inBox:bx.filter(Boolean).length,oneBox:new Set(bx).size===1&&!!bx[0],bk:zs[0].책번호}}""")
        # 제7판 쪼갠 문항은 모두 조건·사례형 발문(단순 꼴 0) — 단순 「옳지 않은 것은?」 표본은 리담 선지 카드 무리((미수록)·(변형))에서
        simple = p.ev("""()=>{for(let i=0;i<VJ.M.length;i++){const d=mlnDirect(VJ.M,i,VJ.P7map,VJ.byId);for(const ln of ['u','v']){const c=d[ln].find(c=>c.kind==='Z'&&!mlnBoxL(c.q)&&/옳지\s*않은|옳은|틀린/.test(c.q.발문||''));
          if(c)return {id:c.q.id,k:oxKeyLid(c.q,c.z),i:i,ln:ln,t:String(c.q.발문||'').slice(0,40),p7simple:Object.values(VJ.P7map).filter(z=>z.문항&&z.사례&&!mlnBoxP(z)).length}}}return null}""")
        sb = None
        if simple:
            p.ev("s=>__HM.go(s)", '__mg%d~%s' % (simple['i'], simple['ln']))
            pg = p.ev("k=>(OXDOMPG||{})['qb-'+k]", simple['k'])
            if pg:
                p.ev("n=>__HM.page(n)", pg)
            sb = p.ev("k=>{const c=document.getElementById('qb-'+k);return c?!!c.closest('.p7case'):null}", simple['k'])
        T('7', u'종합사례 상자 — pdf 340쪽 사례형 문항 줄이 한 상자 · 단순 「옳지 않은 것은?」 꼴은 상자 없음', bool(box340 and box340['oneBox'] and box340['inBox'] == box340['n'] and simple and sb is False), {'340': box340, '단순': simple, '상자 안': sb})
        # 14 · (미수록) ↔ h 📖
        kL = p.ev("()=>{const L=MLN.lid['T1350065']||[];return L.length?oxKeyLid(L[0].q,L[0].z):null}")
        r14 = {'리담': kL}
        if kL:
            # T1350065 는 리담 두 문항(2004-41-15 · 2013-50-18)에 같은 글 — 지시서 표본 2013-50 6번 ⑤ 자리로
            ni = p.ev("()=>{const q=(VJ.qs||[]).find(q=>q.id==='2013-50-18');return q?MLN.lidnode[q.id]:null}")
            r14['줄'] = ('__mg%d~u' % ni) if ni is not None else ''
            if ni is not None:
                p.ev("s=>__HM.go(s)", r14['줄'])
                pg = p.ev("k=>(OXDOMPG||{})['qb-'+k]", kL)
                if pg:
                    p.ev("n=>__HM.page(n)", pg)
            r14['카드'] = p.ev("k=>{const c=document.getElementById('qb-'+k);return c?c.dataset.mln:null}", kL)
            bb = p.ev("([k,r])=>__HM.btnIn(k,r)", [kL, u'^📖'])
            p.click(bb, 1200)
            r14['창'] = p.until("()=>__HM.popKeys().find(x=>/T1350065h/.test(x))", ms=5000)
            p.ev("()=>__HM.closeAll()")
            kh = p.ev("()=>{const z=Object.values(VJ.P7map).find(z=>z.uid==='T1350065h');return z?oxKeyP7(z):null}")
            p.ev("k=>__HM.goKey(k)", kh)
            bh = p.ev("([k,r])=>__HM.btnIn(k,r)", [kh, u'^📖'])
            p.click(bh, 1200)
            r14['거꾸로'] = p.until("()=>__HM.popKeys().find(x=>/T1350065$/.test(x))", ms=5000)
            p.ev("()=>__HM.closeAll()")
        T('14', u'(미수록)↔h 📖 — 리담 2013-50 6번 ⑤ T1350065 가 (미수록) · 📖 누름 → 제7판 T1350065h 팝업 보임 · 거꾸로도', bool(r14.get('카드') == 'u' and r14.get('창') and r14.get('거꾸로')), r14)
        # 11 · 쪼갠 선지 O 누름 → 그 uid 만 기록(pdf 23쪽 1번 (가))
        kg = p.ev("()=>{const z=Object.values(VJ.P7map).find(z=>z.문항==='P7-0055'&&z.선지==='가');return z?oxKeyP7(z):null}")
        p.ev("k=>__HM.goKey(k)", kg)
        before = p.ev("()=>Object.keys(oxAll()).length")
        ob = p.ev("k=>{const c=document.getElementById('qb-'+k);const b=c&&[...c.querySelectorAll('.oxrow button')].find(x=>x.textContent.trim()==='O');if(!b)return null;b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();const at=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return{cx:r.left+r.width/2,cy:r.top+r.height/2,on:!!at&&(at===b||b.contains(at))}}", kg)
        p.click(ob, 500)
        after = p.ev("()=>Object.keys(oxAll()).length")
        rg = p.ev("k=>__HM.oxRec(k)", kg)
        T('11', u'표본 pdf 23쪽 1번 (가) 줄 O page.mouse.click → 그 uid 만 기록(열쇠 +1)', bool(rg and rg.get('m') == 'O' and after - before == 1), {'열쇠': kg, '기록': rg, '늘어난 열쇠': after - before})
        errs = p.errs_all()
        T('APP', u'오류 0(NEW 카드)', not errs, errs[:4])
    finally:
        p.close()
    q = Pg(br, 'cardB', bs, bd, be)
    try:
        q.ev("()=>__HM.home('특허법')")
        kh = q.ev("()=>{const z=Object.values(VJ.P7map).find(z=>z.uid==='T1350065h');return z?oxKeyP7(z):null}")
        q.ev("k=>{const P=(OXPOOL||{})[k];return P?gotoJimun('P',P.id,P.dom):null}", kh); q.pg.wait_for_timeout(900)
        bh = q.ev("([k,r])=>__HM.btnIn(k,r)", [kh, u'^📖'])
        T('6·14-헛', u'헛잣대 — 바탕 카드에 📖 없음', not bh, bh)
    finally:
        q.close()


class _GiDone(Exception):
    pass


def gi_gates_exv(p):
    """★ mbsame_add3 §A-2(9/27) — 기출뷰가 민법 exv 틀로 바뀐 뒤 옛 관문 8·9 를 같은 뜻으로 잰다.
       고르기(마우스·손가락) · OMR 시계 · 제출(OMR 「제출」) → 발문 줄 결과 · 채점 뒤 지문 X → 1차객 기록 · 옛 gi.year 옮기기(add3 §A-1 ⓒ 규칙) · 첫 화면 기출 줄(add3 §A-1 ⓑ 스냅숏 규칙).
       「다시 풀기」 는 add3 §A-2 ② 에서 걷었다(첫 화면 「N회독」 이 맡음 · uidmbs2 하네스 a3-1) — 여기서는 INFO."""
    ks = p.ev("()=>__HM.exvKeys()") or []
    k1, k2 = (ks + [None, None])[:2]
    p.click(p.ev("([k,n])=>__HM.exvNumAt(k,n)", [k1, 2]), 400)
    p.tap(p.ev("([k,n])=>__HM.exvNumAt(k,n)", [k2, 3]), 400)
    s1, s2 = p.ev("k=>__HM.exvState(k)", k1), p.ev("k=>__HM.exvState(k)", k2)
    T('8', u'기출뷰 2019 — 선지 번호 고르기(마우스 · 손가락) [새 기출뷰 exv]', bool(s1 and s1['sel'] == [2] and s2 and s2['sel'] == [3]), {'마우스': s1 and s1['sel'], '손가락': s2 and s2['sel'], '문항': [k1, k2]})
    p.ev("y=>__HM.omrOpen(y)", '2019')
    pb = p.ev("()=>__HM.omkBtn('pl')")
    p.click(pb, 3450)
    t3 = p.ev("()=>__HM.omk()")
    pb = p.ev("()=>__HM.omkBtn('pl')"); p.click(pb, 300)
    T('8', u'OMR 시계 ▶ 3초 → 00H00M03S(시각으로 셈) [새 기출뷰]', bool(t3 and re.match(r'^00H00M0[34]S$', t3['t'])), t3)
    n = p.ev("()=>(GIOMR||[]).length")
    p.ev("([y,ms])=>__HM.omkFake(y,ms)", ['2019', int(n * 1.75 * 60000) + 185000])
    ov = p.ev("()=>__HM.omk()")
    T('8', u'한도(문항 수 × 1.75분)+3:05 → 숫자 빨강 + 「초과 +00H03M05S」 [새 기출뷰]', bool(ov and ov['over'] and u'초과 +00H03M05S' in ov['ov'] and ov['tColor'] in ('rgb(220, 38, 38)',)), ov)
    rs = p.ev("()=>__HM.omkBtn('rs')"); p.click(rs, 200)
    mid = p.ev("()=>__HM.omk()")
    rs = p.ev("()=>__HM.omkBtn('rs')"); p.click(rs, 300)
    z0 = p.ev("()=>__HM.omk()")
    T('8', u'↺ 한 번 = 안 지움(빨강) · 두 번 = 0 [새 기출뷰]', bool(mid and mid['rs']['sure'] and mid['t'] != '00H00M00S' and z0 and z0['t'] == '00H00M00S'), {'한 번': mid, '두 번': z0})
    p.ev("()=>{(GIOMR||[]).forEach((q,i)=>{if(!(giOf(giKey(q))||{}).p)giPut(giKey(q),{p:String((i%5)+1)});});return render()}")
    sb = p.ev("()=>__HM.omrSubmitAt()")
    p.click(sb, 1200)
    st = p.ev("k=>__HM.exvState(k)", k1)
    T('8', u'제출(OMR 「제출」) → 발문 줄 오른쪽 「O 맞음」/「X 틀림 · 정답 N」 보임 · 머리 딱지 없음 [새 기출뷰]', bool(sb and st and st['resVis'] and re.match(u'^(O 맞음|X 틀림 · 정답 )', st['res']) and not st['headBadge']), {'제출': bool(sb), '상태': st})
    keys = p.ev("k=>__HM.exvCardKeys(k)", k1) or []
    xb = p.ev("([k,i,v])=>__HM.exvPostOx(k,i,v)", [k1, 0, 'X'])
    p.click(xb, 600)
    rk = p.ev("k=>__HM.oxRec(k)", keys[0]) if keys else None
    wk = p.ev("k=>__HM.weakHas(k)", keys[0]) if keys else None
    T('8', u'채점 뒤 지문 칸 X page.mouse.click → 그 uid 가 1차객 지문 기록(p X)·틀리면 약점 큐 [새 기출뷰]', bool(rk and rk.get('p') == 'X' and (rk.get('ok') or wk)), {'기록': rk, '약점': wk})
    p.ev("()=>__HM.home('특허법')")
    g = p.ev("k=>__HM.goKey(k)", keys[0]) if keys else None
    rk2 = p.ev("k=>{const c=document.getElementById('qb-'+k);return c?{on:!!c,mln:c.dataset.mln||'',rec:oxOf(k)}:null}", keys[0]) if keys else None
    T('8', u'그 지문의 1차객 카드에도 같은 기록(같은 열쇠 · 흡수면 본편 카드)', bool(rk2 and (rk2['rec'] or {}).get('p') == 'X'), {'이동': g, '카드': rk2})
    N('8', u'「다시 풀기」 → giround 2건 — 새 기출뷰에서 걷음(mbsame_add3 §A-2 ② · 다시 풀기 = 첫 화면 「N회독」) · uidmbs2 하네스 a3-1 이 맡음')
    mg = p.ev("""()=>{giYearPut('2016',{sub:'2026-09-01T10:00:00Z',n:20,right:15});const A=giAll();A[PLAW()+':2016:3']={p:'2',ok:true,g:1};A[PLAW()+':2016:4']={p:'5'};
      GIREC=A;lsWrite(GI_KEY,A,'t');return grndList('2016').map(r=>({ok:r.ok,n:r.n,mig:!!r.mig,picks:r.picks,ms:r.ms}))}""")
    T('8', u'옛 gi.year 한 번 값 → 1회독으로 옮김(범위 안 고른 답이 있을 때만 · 채점된 답만 picks · 시간 없음 · add3 §A-1 ⓒ)', bool(mg and len(mg) == 1 and mg[0]['mig'] and mg[0]['picks'] == {'3': '2'} and mg[0]['ms'] is None), mg)
    p.ev("([y,r])=>__HM.grndFake(y,r)", ['2018', [{'date': '2026-09-20', 'ok': 16, 'n': 20, 'ms': 38 * 60000, 'picks': {'1': '1'}}, {'date': '2026-09-21', 'ok': 15, 'n': 20, 'ms': 40 * 60000, 'picks': {'1': '1'}}]])
    p.ev("()=>{const A=giAll();A[PLAW()+':2017:1']={p:'2'};GIREC=A;lsWrite(GI_KEY,A,'t');return 1}")
    p.ev("()=>__HM.home('특허법')")
    r18, r17 = p.ev("y=>__HM.giRow(y)", '2018'), p.ev("y=>__HM.giRow(y)", '2017')
    ok9 = bool(r18 and re.search(u'\\d+문항 · \\d+지문', r18['tot']) and len(r18['boxes']) == 2 and re.search(u'16/20 X4 · 38m', r18['boxes'][0]['t'])
               and not re.search(u'🌀', r18['boxes'][0]['t']) and r18['boxes'][1]['ov'] and r18['go'] == u'3회독'
               and r17 and u'진행중' in r17['run'] and u'⏱' not in r17['run'] and r17['go'] == u'이어서')
    T('9', u'첫 화면 기출 줄 — 「N문항 · M지문」 · 회독 상자 둘(「16/20 X4 · 38m」 · 스냅숏 없는 옛 회독은 아랫줄 비움 = add3 §A-1 ⓑ) · 한도 넘은 분 빨강 · 진행중 주황(⏱ 없음) · 「이어서」/「N회독」', ok9, {'2018': r18, '2017': r17})
    errs = p.errs_all()
    T('APP', u'오류 0(NEW 기출뷰)', not errs, errs[:4])


def gi_gates(br):
    ns, nd, ne = new_env()
    bs, bd, be = base_env()
    p = Pg(br, 'giN', ns, nd, ne, touch=True)
    try:
        p.ev("()=>__HM.home('특허법')")
        p.ev("()=>{window.confirm=()=>true}")
        p.ev("y=>__HM.gi(y)", '2019')
        if p.ev("()=>__HM.exvOn()"):
            gi_gates_exv(p)   # ★ mbsame_add3 §A-2(9/27) — 새 기출뷰(민법 exv 틀)에서 같은 것을 잰다(옛 몸은 건너뛰고 바탕 헛잣대는 그대로)
            raise _GiDone()
        cid = p.ev("()=>__HM.giFirst()")
        a1 = p.ev("([c,n])=>__HM.giNumAt(c,n)", [cid, 2])
        p.click(a1, 400)
        cid2 = p.ev("()=>document.querySelectorAll('[id^=\"gi-\"]')[1].id")
        a2 = p.ev("([c,n])=>__HM.giNumAt(c,n)", [cid2, 3])
        p.tap(a2, 400)
        s1, s2 = p.ev("c=>__HM.giState(c)", cid), p.ev("c=>__HM.giState(c)", cid2)
        T('8', u'기출뷰 2019 — 선지 번호 고르기(마우스 · 손가락)', bool(s1 and s1['sel'][1] and s2 and s2['sel'][2]), {'마우스': s1 and s1['sel'], '손가락': s2 and s2['sel']})
        # OMR 시계
        p.ev("y=>__HM.omrOpen(y)", '2019')
        pb = p.ev("()=>__HM.omkBtn('pl')")
        p.click(pb, 3450)   # 앱은 0.25초마다 그린다 — 3.2초면 누름 지연에 따라 00H00M02S 가 찍힌다(9/27 한 번) · 3.45초면 [3.2, 3.45] → 3초
        t3 = p.ev("()=>__HM.omk()")
        pb = p.ev("()=>__HM.omkBtn('pl')"); p.click(pb, 300)
        T('8', u'OMR 시계 ▶ 3초 → 00H00M03S(시각으로 셈)', bool(t3 and re.match(r'^00H00M0[34]S$', t3['t'])), t3)
        n = p.ev("()=>(GIOMR||[]).length")
        p.ev("([y,ms])=>__HM.omkFake(y,ms)", ['2019', int(n * 1.75 * 60000) + 185000])
        ov = p.ev("()=>__HM.omk()")
        T('8', u'한도(문항 수 × 1.75분)+3:05 → 숫자 빨강 + 「초과 +00H03M05S」', bool(ov and ov['over'] and u'초과 +00H03M05S' in ov['ov'] and ov['tColor'] in ('rgb(220, 38, 38)',)), ov)
        rs = p.ev("()=>__HM.omkBtn('rs')"); p.click(rs, 200)
        mid = p.ev("()=>__HM.omk()")
        rs = p.ev("()=>__HM.omkBtn('rs')"); p.click(rs, 300)
        z0 = p.ev("()=>__HM.omk()")
        T('8', u'↺ 한 번 = 안 지움(빨강) · 두 번 = 0', bool(mid and mid['rs']['sure'] and mid['t'] != '00H00M00S' and z0 and z0['t'] == '00H00M00S'), {'한 번': mid, '두 번': z0})
        p.ev("()=>{S.omr=false;return render()}")
        p.ev("()=>{(GIOMR||[]).forEach((q,i)=>{if(!(giOf(giKey(q))||{}).p)giPut(giKey(q),{p:String((i%5)+1)});});return render()}")
        sb = p.ev("()=>__HM.giSubmitAt()")
        p.click(sb, 800)
        st = p.ev("c=>__HM.giState(c)", cid)
        T('8', u'제출 → 발문 줄 오른쪽 「O 맞음」/「X 틀림 · 정답 N」 보임 · 머리 「맞음/틀림」 딱지 없음', bool(st and st['resVis'] and re.match(u'^(O 맞음|X 틀림 · 정답 )', st['res']) and not any(x in (u'맞음', u'틀림') for x in st['headBadge'])), st)
        keys = p.ev("c=>__HM.giCardKeys(c)", cid)
        xb = p.ev("([c,i,v])=>__HM.stmtBtnAt(c,i,v)", [cid, 0, 'X'])
        p.click(xb, 500)
        rk = p.ev("k=>__HM.oxRec(k)", keys[0])
        wk = p.ev("k=>__HM.weakHas(k)", keys[0])
        T('8', u'채점 뒤 선지 줄 X page.mouse.click → 그 uid 가 1차객 지문 기록(p X)·틀리면 약점 큐', bool(rk and rk.get('p') == 'X' and (rk.get('ok') or wk)), {'기록': rk, '약점': wk})
        p.ev("()=>__HM.home('특허법')")
        g = p.ev("k=>__HM.goKey(k)", keys[0])
        rk2 = p.ev("k=>{const c=document.getElementById('qb-'+k);return c?{on:!!c,mln:c.dataset.mln||'',rec:oxOf(k)}:null}", keys[0])
        T('8', u'그 지문의 1차객 카드에도 같은 기록(같은 열쇠 · 흡수면 본편 카드)', bool(rk2 and (rk2['rec'] or {}).get('p') == 'X'), {'이동': g, '카드': rk2})
        p.ev("y=>__HM.gi(y)", '2019')
        rb = p.ev("()=>__HM.giResetAt()"); p.click(rb, 800)
        p.ev("()=>{(GIOMR||[]).forEach((q,i)=>giPut(giKey(q),{p:String(((i+1)%5)+1)}));return render()}")
        sb = p.ev("()=>__HM.giSubmitAt()"); p.click(sb, 800)
        gr = p.ev("y=>__HM.grnd(y)", '2019')
        T('8', u'「다시 풀기」 뒤 다시 제출 → jopangi.giround 2건(이력 안 지움 · 제출마다 하나)', bool(gr and len(gr) == 2 and not any(x['mig'] for x in gr)), gr)
        mg = p.ev("""()=>{giYearPut('2016',{sub:'2026-09-01T10:00:00Z',n:20,right:15});const A=giAll();A[PLAW()+':2016:3']={p:'2',ok:true,g:1};A[PLAW()+':2016:4']={p:'5'};
          GIREC=A;lsWrite(GI_KEY,A,'t');return grndList('2016').map(r=>({ok:r.ok,n:r.n,mig:!!r.mig,picks:r.picks,ms:r.ms}))}""")
        T('8', u'옛 gi.year 한 번 값 → 1회독으로 옮김(채점된 답만 picks · 시간 없음)', bool(mg and len(mg) == 1 and mg[0]['mig'] and mg[0]['ok'] == 15 and mg[0]['picks'] == {'3': '2'} and mg[0]['ms'] is None), mg)
        # 9 · 첫 화면 기출 줄
        p.ev("([y,r])=>__HM.grndFake(y,r)", ['2018', [{'date': '2026-09-20', 'ok': 16, 'n': 20, 'ms': 38 * 60000, 'picks': {}}, {'date': '2026-09-21', 'ok': 15, 'n': 20, 'ms': 40 * 60000, 'picks': {}}]])
        p.ev("()=>{const A=giAll();A[PLAW()+':2017:1']={p:'2'};GIREC=A;lsWrite(GI_KEY,A,'t');return 1}")
        p.ev("()=>__HM.home('특허법')")
        r18, r17 = p.ev("y=>__HM.giRow(y)", '2018'), p.ev("y=>__HM.giRow(y)", '2017')
        ok9 = bool(r18 and re.search(u'\\d+문항 · \\d+지문', r18['tot']) and len(r18['boxes']) == 2 and re.search(u'16/20 X4 · 38m', r18['boxes'][0]['t'])
                   and re.search(u'🌀\\d+ ⚠\\d+ X\\d+ /\\d+', r18['boxes'][0]['t']) and r18['boxes'][1]['ov'] and r18['go'] == u'3회독'
                   and r17 and u'진행중' in r17['run'] and u'⏱' not in r17['run'] and r17['go'] == u'이어서')
        T('9', u'첫 화면 기출 줄 — 「N문항 · M지문」 · 회독 파란 상자 두 줄(「16/20 X4 · 38m」/「🌀 ⚠ X /M」) · 분만 · 한도 넘은 분 빨강 · 진행중 주황(⏱ 없음) · 「이어서」/「N회독」', ok9, {'2018': r18, '2017': r17})
        errs = p.errs_all()
        T('APP', u'오류 0(NEW 기출뷰)', not errs, errs[:4])
    except _GiDone:
        pass
    finally:
        p.close()
    q = Pg(br, 'giB', bs, bd, be)
    try:
        q.ev("()=>__HM.home('특허법')")
        q.ev("()=>{window.confirm=()=>true}")
        q.ev("y=>__HM.gi(y)", '2019')
        q.ev("y=>{S.omr=true;return render()}", '2019')
        ob = q.ev("()=>__HM.omk()")
        r18 = q.ev("y=>__HM.giRow(y)", '2019')
        T('8·9-헛', u'헛잣대 — 바탕 OMR 시계 없음 · 첫 화면 기출 줄에 회독 상자 없음', not ob and not (r18 and r18['boxes']), {'시계': ob, '줄': r18})
    finally:
        q.close()


def rec_gates(br):
    ns, nd, ne = new_env()
    bs, bd, be = base_env()
    p = Pg(br, 'recN', ns, nd, ne)
    try:
        p.ev("()=>__HM.home('특허법')")
        k = p.ev("()=>{const z=Object.values(VJ.P7map).find(z=>z.문항==='P7-0137'&&z.선지===2);return oxKeyP7(z)}")
        gk = p.ev("k=>__HM.goKey(k)", k)
        scope = 'mok|특허|' + gk['sel']
        p.ev("([s,k,d])=>__HM.rndFake(s,k,false,d)", [scope, k, '2026-09-20'])
        p.ev("k=>__HM.goKey(k)", k)
        so = p.ev("k=>__HM.stripOpen(k)", k); p.click(so, 400)
        cs = p.ev("k=>__HM.rgbStyle(k)", k)
        T('10', u'기록 칸 단추 꼴 = span 칸 꼴(.mbrec .c — 굵기 800 · 테 1px solid · 22×20 · 글 12px)', bool(cs and cs['fw'] == '800' and cs['bw'] == '1px' and cs['bs'] == 'solid' and cs['w'] == 22 and cs['h'] == 20 and cs['fs'] == '12px'), cs)
        cz = p.ev("k=>__HM.rgbStyle(k,'.mbrec .c.rgb{border:0;font:inherit;padding:0}')", k)
        T('10-헛', u'헛잣대 — 옛 단추 규칙(border:0 · font:inherit · 9/27 회귀)을 얹으면 굵기·테가 무너진다', bool(cz and (cz['fw'] != '800' or cz['bw'] != '1px')), cz)
        c0 = p.ev("k=>__HM.stripCellAt(k,0)", k); p.click(c0, 400)
        s1 = p.ev("k=>__HM.stripCells(k)", k)
        x1 = p.ev("k=>__HM.stripXAt(k)", k); p.click(x1, 300)
        s2 = p.ev("k=>__HM.stripCells(k)", k)
        r_mid = p.ev("s=>__HM.rndOf(s)", scope)
        x2 = p.ev("k=>__HM.stripXAt(k)", k); p.click(x2, 800)
        r_end = p.ev("s=>__HM.rndOf(s)", scope)
        gone = p.ev("()=>__HM.gone()")
        T('10', u'기록 칸 page.mouse.click → 출처 글 보임(「m/d · 단원 · N회독째」 · 「이번」 없음)', bool(s1 and s1['infoVis'] and re.match(r'^\d+/\d+ · .+ · \d+회독째', s1['info']) and u'이번' not in s1['info']), s1)
        T('10', u'× 한 번 = 안 지워짐(빨강) · 두 번 = 지워짐 · 묘비 1', bool(x1 and r_mid and r_mid[-1]['all'] == 1 and r_end and r_end[-1]['all'] == 0 and r_end[-1]['wrong'] == 0 and gone and len(gone) == 1),
          {'한 번 뒤': r_mid, '두 번 뒤': r_end, '묘비': gone})
        # 지금 칸 지우기 → oxOf 재계산 · 약점에서 빠짐
        p.ev("k=>{oxPut(k,{p:'O',ok:false});return render()}", k)
        w0 = p.ev("k=>__HM.oxState(k)", k)
        p.ev("k=>__HM.goKey(k)", k)
        so = p.ev("k=>__HM.stripOpen(k)", k); p.click(so, 400)
        cc = p.ev("k=>{const c=document.getElementById('qb-'+k);const b=c&&[...c.querySelectorAll('.mbrecw .rgb')].pop();if(!b)return null;b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();const at=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return{cx:r.left+r.width/2,cy:r.top+r.height/2,on:!!at&&(at===b||b.contains(at))}}", k)
        p.click(cc, 300)
        for _ in range(2):
            xx = p.ev("k=>__HM.stripXAt(k)", k); p.click(xx, 500)
        w1 = p.ev("k=>__HM.oxState(k)", k)
        rec = p.ev("k=>__HM.oxRec(k)", k)
        T('10', u'지금 칸(마감 전) 지움 → 그 지문 기록 p·ok 지움 · 약점(틀림 상태)에서 빠짐', w0 == 3 and w1 != 3 and not (rec or {}).get('p'), {'전': w0, '뒤': w1, '기록': rec})
        # 되살림 흉내 → 쓸기
        p.ev("([s,k])=>{const A=rndAll();const r=A[s][A[s].length-1];r.allK.push(k);r.wrongK.push(k);r.wrong=1;RNDREC=A;lsWrite(RND_KEY,A,'t');return 1}", [scope, k])
        sw = p.ev("()=>__HM.sweep()")
        T('10', u'되살아난 칸(동기화 흉내) → 쓸기 1 · 묘비는 비우지 않음', sw == 1 and len(p.ev("()=>__HM.gone()")) >= 1, {'쓸기': sw})
        sk = p.ev("()=>__HM.syncKeys()")
        T('10', u'SYNC_KEYS 에 jopangi.giround · jopangi.recgone', bool(sk and any(x.endswith('giround') for x in sk) and any(x.endswith('recgone') for x in sk)), sk[-4:] if sk else sk)
        # 13 · 정리 창 — 단원 줄 📋
        gi = p.ev("()=>__HM.nodeByTitle('균등론')")
        p.ev("()=>__HM.home('특허법')")
        res = {}
        for ln, suf in (('b', ''), ('u', u' (미수록)')):
            lab = p.ev("i=>{const M=VJ.M;return (M[i].no?M[i].no+' ':'')+M[i].제목}", gi) + suf
            jb = p.ev("n=>__HM.rowJnByName(n)", lab)
            p.click(jb, 800)
            w = p.ev("n=>__HM.jnWin('📋 정리 · '+n.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&'))", lab)
            cards = p.ev("k=>{const s=mlnSel(k[0],k[1]);const F=(typeof uzCards==='function')?uzCards:(x=>x);return mokCells(F(mokCards(k[0],k[1]))).length}", [gi, ln])   # ★ mbsame_add3 §A-6·§A-8(9/27) — 화면 카드 = 한 거름(처음 = 기출)을 지난 카드 · 옛 판 = uzCards 없음 · 무변
            res[ln] = {'창': w, '카드 칸': cards}
            p.ev("()=>__HM.closeAll()")
        ok13a = all(v['창'] and v['창']['rows'] == v['카드 칸'] and v['창']['jnrec'] == 0 and v['창']['tg'] for v in res.values())
        T('13', u'정리 창 — 단원 줄(본편·(미수록)) 📋 page.mouse.click → 그 줄 지문 수 = 카드 수 · 번호 단추 바로 뒤 출제연도 칩 · 기록 칸 줄(글자 하나 아님) · 「✏️ 표시」', ok13a, res)
        # 기출 해 📋 — 흉내 2회독
        p.ev("([y,r])=>__HM.grndFake(y,r)", ['2019', [{'date': '2026-09-19', 'ok': 9, 'n': 18, 'ms': 1, 'picks': {'1': '2'}}, {'date': '2026-09-20', 'ok': 10, 'n': 18, 'ms': 1, 'picks': {'1': '3'}}]])
        mk = p.ev("()=>{const q=(VJ.qs||[]).find(q=>String(q.연도)==='2019');return q?oxKeyLid(q,q.지문[0]):null}")
        p.ev("k=>__HM.mkPut(k)", mk)
        p.ev("()=>__HM.home('특허법')")
        jb = p.ev("y=>__HM.giRowJn(y)", '2019'); p.click(jb, 900)
        w = p.ev("()=>__HM.jnWin('📋 정리 · 2019')")
        c0 = p.ev("()=>__HM.jnInWin('📋 정리 · 2019','.jnxq .grc',0)"); p.click(c0, 300)
        gri = p.ev("()=>__HM.jnGri('📋 정리 · 2019')")
        nq = p.ev("()=>((VJ.qs||[]).filter(q=>String(q.연도)==='2019').length)")
        T('13', u'기출 2019 📋 → 「문제 N」 = 문항 수 · 흉내 2회독 = 문제마다 칸 2 · 칸 누름 → 「m/d · N회독째 · 고른 · 정답」 보임', bool(w and w['qn'] == nq and w['grc'] == 2 * nq and gri and gri['vis'] and re.search(u'회독째 · 고른 .+ · 정답', gri['t'])), {'창': w, '문항': nq, '칸 글': gri})
        # ✏️ 표시 끄기 — 창 안 형광펜
        tg = p.ev("()=>__HM.jnInWin('📋 정리 · 2019','.jnxtg',0)"); p.click(tg, 300)
        w2 = p.ev("()=>__HM.jnWin('📋 정리 · 2019')")
        on_bg = (w or {}).get('marks') or []
        T('13', u'「✏️ 표시」 끄면 이 창 안 형광펜 안 보임(켜짐 = 칠함 · 끔 = 바탕 투명) · 단원 화면 S.mkOff 와 따로',
          bool(on_bg and on_bg[0] != 'rgba(0, 0, 0, 0)' and w2 and w2['off'] and w2['marks'] and w2['marks'][0] == 'rgba(0, 0, 0, 0)' and not p.ev("()=>!!S.mkOff")), {'켜짐': on_bg, '끔': w2 and w2['marks']})
        p.ev("()=>__HM.closeAll()")
        errs = p.errs_all()
        T('APP', u'오류 0(NEW 기록 칸·정리 창)', not errs, errs[:4])
    finally:
        p.close()
    q = Pg(br, 'recB', bs, bd, be)
    try:
        q.ev("()=>__HM.home('특허법')")
        sk = q.ev("()=>__HM.syncKeys()")
        r19 = q.ev("y=>__HM.giRow(y)", '2019')
        jn0 = q.ev("()=>{const r=[...document.querySelectorAll('#slot .mbur')].find(x=>/^2019년/.test((x.querySelector('.nm')||{}).textContent||''));return r?{t:r.textContent.replace(/\s+/g,' ').slice(0,80),jn:!!r.querySelector('.mbchip.jn')}:null}")
        T('10·13-헛', u'헛잣대 — 바탕 SYNC_KEYS 에 recgone 없음 · 기출 해 줄에 📋 없음', bool(sk and not any(x.endswith('recgone') for x in sk) and jn0 and not jn0['jn']), {'sk': sk[-3:] if sk else sk, '줄': jn0})
    finally:
        q.close()


def depth_gates(br):
    ns, nd, ne = new_env()
    bs, bd, be = base_env()
    p = Pg(br, 'dpN', ns, nd, ne, touch=True)
    try:
        p.ev("()=>__HM.home('특허법')")
        heads = {}
        for no in ('8.2.3', '8.3.2', '8.3.3', '8.3.4', '9.1.2'):
            h = p.ev("n=>__HM.head(n)", no)
            heads[no] = h and re.search(u'총 (\\d+)문제', h['t']).group(1)
        dw = p.ev("()=>__HM.drawerCounts()")
        dmap = {no: dw.get('H:' + p.ev("n=>{const i=__HM.nodeIdx(n);const M=VJ.M;return (M[i].no?M[i].no+' ':'')+M[i].제목}", no)) for no in heads}
        zero = p.ev("()=>[...document.querySelectorAll('#slot .mbur.mdph')].filter(r=>/총 0문제/.test(r.textContent)).length")
        T('D1', u'add1 머리 셈 — 첫 화면 머리 = 서랍 같은 마디 셈(다름 0) · 「총 0문제」 머리 0', all(str(dmap[k]) == str(v) for k, v in heads.items()) and zero == 0, {'첫 화면': heads, '서랍': dmap, '총0': zero})
        N('D1', u'add1 머리 셈 쪼개 보기 — 그 마디와 아래 전부: 본편 b · (미수록) u · (변형) v(셈 = b+u+v) · 붙은 리담 선지 lid 중 흡수 abs(본편 제7판 줄로 감)',
          {no: p.ev("n=>__HM.subCensus(n)", no) for no in heads})
        kids0 = p.ev("n=>__HM.kidRows(n)", '8.3.2')
        a = p.ev("n=>__HM.head(n)", '8.3.2'); p.click(a, 600)
        kids1 = p.ev("n=>__HM.kidRows(n)", '8.3.2')
        a = p.ev("n=>__HM.head(n)", '8.3.2'); p.tap(a, 600)
        kids2 = p.ev("n=>__HM.kidRows(n)", '8.3.2')
        a = p.ev("n=>__HM.head(n)", '8.3.2'); p.click(a, 600)
        mb = p.ev("()=>__HM.mbCh()"); jt = p.ev("()=>__HM.jtCh()")
        p.pg.goto(p.pg.url.split('&keep=')[0] + '&keep=1', wait_until='load')   # 새로고침(저장소 그대로 — keep 없이 열면 SEED 가 비운다)
        p.pg.wait_for_function(READY); p.pg.wait_for_timeout(800)
        p.ev("()=>__HM.home('특허법')")
        kids3 = p.ev("n=>__HM.kidRows(n)", '8.3.2')
        T('D2', u'add1 머리 누름 — 8.3.2 ▾ page.mouse.click → 깊이 4 줄 전부 안 보임 · 손가락 톡 → 다시 보임 · 새로고침 뒤 접힘 유지 · 서랍 접힘(jtCh)과 따로',
          all(x['vis'] for x in kids0) and not any(x['vis'] for x in kids1) and all(x['vis'] for x in kids2) and not any(x['vis'] for x in kids3) and mb != '{}' and jt == '{}',
          {'처음': sum(x['vis'] for x in kids0), '마우스 뒤': sum(x['vis'] for x in kids1), '손가락 뒤': sum(x['vis'] for x in kids2), '새로고침 뒤': sum(x['vis'] for x in kids3), 'mbCh': mb, 'jtCh': jt})
        a = p.ev("n=>__HM.head(n)", '8.3.2'); p.click(a, 600)
        hn = p.ev("n=>__HM.head(n)", '8.3.2')
        kids = p.ev("n=>__HM.kidRows(n)", '8.3.2')
        dx = [round(k['x'] - hn['nmx'], 1) for k in kids if k.get('vis')]
        T('D3', u'add1 깊이 보임 — 8.3.2 아래 깊이 4 줄 이름 x − 머리 이름 x ≥ 12px · 머리 굵기 800 · 세로 줄(inset 1px · 구분선 회색 --line #e3e0d8 — 원칙 빨강 --rule 아님) 보임',
          bool(dx and min(dx) >= 12 and hn['fw'] in ('800', 'bold') and all('inset' in (k.get('line') or '') and 'rgb(227, 224, 216)' in (k.get('line') or '') for k in kids if k.get('vis'))), {'dx': dx[:6], 'fw': hn['fw'], 'fs': hn['fs'], 'line': kids[0].get('line') if kids else None})
        errs = p.errs_all()
        T('APP', u'오류 0(NEW 첫 화면 깊이)', not errs, errs[:4])
    finally:
        p.close()
    ph = Pg(br, 'dpNph', ns, nd, ne, W=390, H=844, touch=True)
    try:
        ph.ev("()=>__HM.home('특허법')")
        f = ph.ev("r=>__HM.rowFit(r)", '^8\\.3\\.4\\.5 ')
        T('D4', u'add1 폰 폭 390px — 8.3.4.5 줄 이름 안 잘림(이름 오른쪽 ≤ 줄 오른쪽 · 말줄임·넘침 숨김 없음) · 가로 스크롤 0', bool(f and f['nmR'] <= f['rowR'] + 1 and not f['clip'] and f['docSW'] <= f['docCW'] + 1), f)
    finally:
        ph.close()
    q = Pg(br, 'dpB', bs, bd, be)
    try:
        q.ev("()=>__HM.home('특허법')")
        hb = q.ev("n=>__HM.head(n)", '8.3.2')
        z0 = q.ev("()=>[...document.querySelectorAll('#slot .mbur')].filter(r=>/총 0문제/.test(r.textContent)&&/^.?8\\.2\\.3|^.?8\\.3\\.[234]|^.?9\\.1\\.2/.test(r.querySelector('.nm')?r.querySelector('.nm').textContent.trim():'')).length")
        T('D1·D2·D3-헛', u'헛잣대 — 바탕 첫 화면에 깊이 3 머리 줄 없음 · 그 다섯이 「총 0문제」', not hb and z0 == 5, {'머리': hb, '총0': z0})
        bdw = q.ev("()=>__HM.drawerCounts()")
        N('D1-헛', u'바탕 서랍 머리 셈(같은 다섯 마디 · 본판 §A 전 셈)',
          {no: bdw.get('H:' + q.ev("n=>{const i=__HM.nodeIdx(n);const M=VJ.M;return (M[i].no?M[i].no+' ':'')+M[i].제목}", no)) for no in ('8.2.3', '8.3.2', '8.3.3', '8.3.4', '9.1.2')})
    finally:
        q.close()


def sync_gates(br):
    """§E — 새 동기화 키 둘(jopangi.giround · jopangi.recgone): 새 판 A 가 올림 → 옛 판 B(바탕 앱)가 받아 올림(옛 판은 모르는 키를 data 에서 뺀다) → 새 판 A 가 되살린다.
       원격 = 메모리(SEED 가 GitHub 대신 대답) · 시작값 = studyplandata jopangi/기록.json"""
    ns, nd, ne = new_env()
    bs, bd, be = base_env()
    REC = _roots.spd(r'jopangi\기록.json')
    r0 = io.open(REC, encoding='utf-8').read()
    ctxA = br.new_context(viewport={'width': 1300, 'height': 900}, device_scale_factor=1)
    portA = serve('syncA', ns, nd, ne)
    a = Pg(br, 'syncA', ns, nd, ne, remote=r0, port=portA, ctx=ctxA)
    out = {}
    try:
        a.ev("()=>__HM.home('특허법')")
        a.ev("()=>__HM.sync()")
        a.ev("()=>__HM.seedNewKeys()")
        a.ev("()=>__HM.sync()")
        t1 = a.ev("()=>__HM.remote()")
        d1 = json.loads(t1 or '{}').get('data', {})
        out['A 올림'] = {'giround': 'jopangi.giround' in d1, 'recgone': 'jopangi.recgone' in d1}
        b = Pg(br, 'syncB', bs, bd, be, remote=t1)
        try:
            b.ev("()=>__HM.home('특허법')")
            b.ev("()=>__HM.sync()")
            t2 = b.ev("()=>__HM.remote()")
        finally:
            b.close()
        d2 = json.loads(t2 or '{}').get('data', {})
        u2 = json.loads(t2 or '{}').get('u', {})
        out['B(옛 판) 올린 뒤'] = {'giround': 'jopangi.giround' in d2, 'recgone': 'jopangi.recgone' in d2,
                                 '도장': sum(1 for k in u2 if k.startswith('jopangi.giround') or k.startswith('jopangi.recgone'))}
        a.ev("t=>__HM.setRemote(t)", t2)
        a.ev("()=>__HM.sync()")
        t3 = a.ev("()=>__HM.remote()")
        d3 = json.loads(t3 or '{}').get('data', {})
        out['A 다시 맞춘 뒤'] = {'giround': 'jopangi.giround' in d3, 'recgone': 'jopangi.recgone' in d3, '이 기기': a.ev("()=>__HM.localNewKeys()")}
    finally:
        a.close()
    N('10s', u'옛 판 기기가 올리면 새 키 둘이 원격 data 에서 빠지는가(ncomr·notecolor·clfix 와 같은 창)', out.get('B(옛 판) 올린 뒤'))
    T('10s', u'새 판 A 가 올림 → (옛 판 B 가 뺀 뒤) 새 판 A 가 다음 맞추기에서 되살려 올림 · 이 기기 값 그대로', bool(out.get('A 올림', {}).get('giround') and out['A 올림'].get('recgone')
      and out.get('A 다시 맞춘 뒤', {}).get('giround') and out['A 다시 맞춘 뒤'].get('recgone')), out)


def reg_gates(br):
    """§G-15 — 기록 열쇠 무변(바탕 풀 열쇠 ⊆ 새 풀 · 새 열쇠 = 새로 쪼갠 줄·문항째 카드뿐) · 다른 법(상표·디보)·특허 미분류 화면 글 대조(칩 글자 가림)"""
    ns, nd, ne = new_env()
    bs, bd, be = base_env()
    shots, keys = {}, {}
    for tag, src, data, exam in (('BASE', bs, bd, be), ('NEW', ns, nd, ne)):
        p = Pg(br, 'reg' + tag, src, data, exam)
        try:
            out = {}
            p.ev("()=>__HM.home('특허법')")
            keys[tag] = p.ev("()=>Object.keys(OXPOOL||{})")
            p.ev("()=>__HM.go('__미분류')")
            out[u'특허 미분류'] = p.ev("()=>__HM.dump()")
            for law in (u'상표법', u'디자인보호법'):
                p.ev("l=>__HM.home(l)", law)
                out[law[:2] + u' 첫 화면'] = p.ev("()=>__HM.dump()")
                p.ev("()=>__HM.go('__미분류')")
                out[law[:2] + u' 미분류'] = p.ev("()=>__HM.dump()")
            shots[tag] = out
        finally:
            p.close()
    P = json.load(io.open(os.path.join(DATA, 'jimun_7pan.json'), encoding='utf-8'))
    newids = set()
    for z in P['지문']:
        if re.search(u'-[1-7ㄱ-ㅅ가-사]$', z['id']):
            newids.add(z['uid'])
    for o in P[u'객관식']:
        newids.add(o['uid'])
    # ★ uid_add2 §D(9/27) — 우리 데이터에 없던 기출 문항을 넣었다(1998-35-5 · 2016 시험 3·4·11번 · 2018 시험 4번 · 연도 모름 PM-0506) — 그 선지 열쇠도 까닭 있는 새 열쇠
    NEWQ = {u'1998-35-5', u'2016-53-B3', u'2016-53-B4', u'2016-53-B11', u'2018-55-B4', u'--0506'}
    for q in json.load(io.open(os.path.join(DATA, u'jimun_특허.json'), encoding='utf-8'))[u'문제']:
        if q['id'] in NEWQ:
            newids.update(z.get('uid') for z in q.get(u'지문') or [] if z.get('uid'))
    b, n = set(keys['BASE']), set(keys['NEW'])
    lost = sorted(b - n)
    extra = sorted(n - b)
    odd = [k for k in extra if k not in newids]
    T('15', u'기록 열쇠 — 바탕 풀 열쇠가 새 풀에 다 있음(없어진 열쇠 0) · 새 열쇠는 새로 쪼갠 줄·문항째 카드뿐', not lost and not odd,
      {'바탕': len(b), '새': len(n), '없어짐': lost[:8], '새 열쇠': len(extra), '까닭 모를 새 열쇠': odd[:8]})
    import difflib
    CHIP = re.compile(u'(?:상표 )?\\d{4}:(?:\\d+|\\?)(?::[^\\s·]{1,2})?')
    summ = {}
    for k in shots['NEW']:
        A = CHIP.sub('', shots['BASE'].get(k, '')).split('\n'); C = CHIP.sub('', shots['NEW'].get(k, '')).split('\n')
        sm = difflib.SequenceMatcher(None, A, C, autojunk=False)   # 줄 단위 — 글자 단위는 미분류 화면에서 20분 넘게 걸렸다(9/27)
        ops = [(t, ' / '.join(A[i1:i2])[:60], ' / '.join(C[j1:j2])[:60]) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal']
        summ[k] = {'같은 줄 비율': round(sm.ratio(), 4), '줄 수': [len(A), len(C)], '바뀐 조각': len(ops), '예': ops[:5]}
    N('15', u'다른 법·미분류 화면 글 바탕 대조(출제연도 칩 글자 가림) — 달라진 조각(까닭은 수행 결과)', summ)
    # 칩 줄(가리면 빈 줄)을 빼면 한 줄도 다르지 않아야 한다 — 이 판이 그 화면에 더한 것은 출제연도 칩뿐
    same, chipln = {}, {}
    for k in shots['NEW']:
        A = [l for l in (CHIP.sub('', x).strip() for x in shots['BASE'].get(k, '').split('\n')) if l and l != u'·']
        C = [l for l in (CHIP.sub('', x).strip() for x in shots['NEW'].get(k, '').split('\n')) if l and l != u'·']
        sm = difflib.SequenceMatcher(None, A, C, autojunk=False)
        same[k] = [round(sm.ratio(), 4), len(A), len(C)]
        chipln[k] = len(shots['NEW'].get(k, '').split('\n')) - len(shots['BASE'].get(k, '').split('\n'))
    T('15', u'다른 법(상표·디보 첫 화면·미분류)·특허 미분류 화면 글 = 바탕(출제연도 칩 줄만 뺌) — 같은 줄 비율 1.0', all(v[0] == 1.0 and v[1] == v[2] for v in same.values()), {'같음': same, '더해진 줄(칩)': chipln})
    T('15-헛', u'헛잣대 — 칩 줄을 안 빼면 바뀐 조각이 잡힌다(대조가 눈을 뜨고 있다)', any(v['바뀐 조각'] > 0 for v in summ.values()), {k: v['바뀐 조각'] for k, v in summ.items()})
    io.open(os.path.join(WORK, 'reg_mbs_screens.json'), 'w', encoding='utf-8').write(json.dumps(shots, ensure_ascii=False))


def report():
    P = sum(1 for r in RES if r[2] is True)
    F = [r for r in RES if r[2] is False]
    lines = ['# _harness_jo_gaek_mbsame 결과 — %s' % time.strftime('%Y-%m-%d %H:%M'), '',
             'NEW 앱 %s (LF md5 %s) · NEW 데이터 %s · 시험지 %s · BASE %s' % (NEWF, hashlib.md5(open(NEWF, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:8], DATA, EXAM, BASE_REV),
             'PASS %d · FAIL %d · INFO %d' % (P, len(F), sum(1 for r in RES if r[2] is None)), '']
    for g, n, ok, d in RES:
        lines.append('%s | %s · %s | %s' % ('INFO' if ok is None else ('PASS' if ok else 'FAIL'), g, n,
                                           d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str)[:1200]))
    f = os.path.join(OUT, '_harness_jo_gaek_mbsame_result.txt')
    io.open(f, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print('\n== PASS %d · FAIL %d → %s' % (P, len(F), f))
    return len(F)


def main():
    os.makedirs(WORK, exist_ok=True)
    if not ONLY or 'data' in ONLY:
        data_gates()
    parts = [('unit', unit_gates), ('chip', chip_gates), ('card', card_gates), ('gi', gi_gates), ('rec', rec_gates), ('depth', depth_gates), ('sync', sync_gates), ('reg', reg_gates)]
    if any(not ONLY or k in ONLY for k, _ in parts):
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            try:
                for k, fn in parts:
                    if not ONLY or k in ONLY:
                        try:
                            fn(br)
                        except Exception as e:
                            T('RUN', u'%s 묶음이 멈춤' % k, False, repr(e)[:600])
            finally:
                br.close()
    sys.exit(1 if report() else 0)


if __name__ == '__main__':
    main()
