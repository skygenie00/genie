# -*- coding: utf-8 -*-
r"""_task_jo_toc_fuse §F 관문 — 데이터(원장 → jimun_7pan · mokcha_병합 융합판) + 앱(순 차례 · 조문 칩 · ▸ 소제목 · 12 실용신안 한 줄 · 머리 한 줄 · 모아보기)

  NEW  = --new <파일>(없으면 genie 작업트리 jo/index.html) · BASE = genie HEAD(f497f05 · md5 6db2c79a)
  데이터 = --data <폴더>(없으면 genie 작업트리 jo/data) · 바탕 데이터 = genie HEAD blob(git show)
  헛잣대 = 바탕에서 FAIL 이어야 한다(관문 규칙 3) — 앱 관문은 BASE 앱 + 새 데이터 · 데이터 관문은 HEAD 데이터
  누름 = page.mouse.click(x, y)(PC) · 손가락 = CDP Input.dispatchTouchEvent(radiusX·Y 22) — el.click()·dispatchEvent 로 PASS 내지 않는다(관문 규칙 1)
  보임 = display ≠ none 그리고 getBoundingClientRect().height > 0(관문 규칙 2)
  9/26 11:46 채팅 답 — 골든은 텍스트 순서 book_T 라 지문 배정·소제목 수는 대조하지 않는다(마디 147·no·제목·깊이·조·리담만) · 담기 = 좌표 원장 책 절

쓰기 : python _harness_jo_toc_fuse.py [--new 파일] [--data 폴더] [--out 폴더] [--only data,base,new,touch]
"""
import csv, hashlib, http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
csv.field_size_limit(10 ** 9)
CJH = r'N:\개인\claude\jopangi\공통\_harness'
sys.path.insert(0, CJH)
import _harness_canvas_jari as CJ          # noqa: E402 — SEED(기록 fetch 돌림 · 바깥 網 막음) · VENDOR · route_filter · NOISE
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


HERE = os.path.dirname(os.path.abspath(__file__))
JP = os.path.dirname(HERE)
OUT = ARG('--out', HERE)
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
GENIE = CJ.GENIE
JOD = os.path.join(GENIE, 'jo')
DATA = ARG('--data', os.path.join(JOD, 'data'))
NEWF = ARG('--new', os.path.join(JOD, 'index.html'))
BASE_REV, BASE_MD5 = 'f497f05', '6db2c79aa04ff70d037954b4a1b82c55'
WORK = os.path.join(tempfile.gettempdir(), 'h_tocfuse')
TESTS = io.open(os.path.join(HERE, '_harness_jo_toc_fuse_tests.js'), encoding='utf-8').read()
READY = "!!window.__HT&&typeof render==='function'"
TOC = os.path.join(JP, '특상디', '_1차객_목차.json')
GOLD = os.path.join(JP, '특상디', '_toc_fuse', '_골든_mokcha_병합.json')
FUSED = os.path.join(JP, '특상디', '_toc_fuse', 'fused.json')
L7CSV = os.path.join(JP, '공통', '_재료', '_제7판_지문원장.csv')
SHOTS = os.path.join(OUT, '_toc_fuse_shots')
SERVERS = {}
RES = []
KEEP = {}
L_221, L_12, L_38, L_381 = '2.2.1 주체 능력', '1.2 국제조약', '3.8 명세서 기재불비(42)', '3.8.1 총설'
L_33, L_8323 = '3.3 {신}신규성(29①)선공기vs청', '8.3.2.3 {직}{이저}이용저촉(98)'


def git(*a, repo=GENIE):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, d[:400]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('NOTE | %s · %s | %s' % (grp, name, d[:400]), flush=True)


def jload_new(name):
    return json.load(open(os.path.join(DATA, name), encoding='utf-8'))


def jload_head(name):
    return json.loads(git('show', 'HEAD:jo/data/' + name).decode('utf-8'))


# ══════════ 데이터 관문 (F1~F4) ══════════
def kind(tag):
    return '변리' if '변리' in tag else '사법' if '사법' in tag else '미기출' if '미기출' in tag else '없음'


def data_gates():
    L7 = {r['ID']: r for r in csv.DictReader(open(L7CSV, encoding='utf-8-sig'))}
    TOCJ = json.load(open(TOC, encoding='utf-8'))
    G = json.load(open(GOLD, encoding='utf-8'))['마디']
    fu = json.load(open(FUSED, encoding='utf-8'))['nodes']
    for tag, P7, MG in (('BASE', jload_head('jimun_7pan.json'), jload_head('mokcha_병합.json')),
                        ('NEW', jload_new('jimun_7pan.json'), jload_new('mokcha_병합.json'))):
        g = '데이터 %s' % tag
        Z = P7['지문']
        ids = [z['id'] for z in Z]
        split = [z for z in Z if z.get('문항')]
        body = [z for z in Z if not z.get('문항')]
        kinds = {}
        for z in body:
            kinds[kind(z['태그'])] = kinds.get(kind(z['태그']), 0) + 1
        yj = sum(1 for z in body if z.get('유제'))
        # F1 — 지문 수: 제7판 OX 줄 1,625(옛) + 사법·미기출·태그없음 300 + 객관식 ①64 선지 320(9/26 사용자 · 채팅 11:46·12:12 로 바뀐 기대)
        #   ★ 9/26 18:27 사용자 「빨간 글(추록) 우선」 — 모아보기 전용이던 P7-2058 은 원장에 두되 제외사유로 뺀다(301 → 300)
        exp = {'total': 2245, 'split': 320, 'split_q': 64, 'body': 1925}
        got = {'total': len(Z), 'split': len(split), 'split_q': len({z['문항'] for z in split}), 'body': len(body)}
        T(g, 'F1 jimun_7pan 지문 = 2,245(옛 1,625 + 사법·미기출·태그없음 300 + 객관식 ①64 문항 선지 320 · P7-2058 은 추록 대체로 뺌) · 헛잣대 바탕 1,625',
          got == exp, {'got': got, '꼴(선지 줄 뺀 책 줄)': kinds, '유제': yj})
        base = {z['id']: z for z in jload_head('jimun_7pan.json')['지문']}
        same = [i for i in base if i in {z['id'] for z in Z}]
        zmap = {z['id']: z for z in Z}
        bad_uid = [(i, base[i].get('uid'), zmap[i].get('uid') if i in zmap else None) for i in base if i not in zmap or zmap[i].get('uid') != base[i].get('uid')]
        # 예외 하나 — pdf 75 · 37번 [14 변리] 은 추록으로 답 O→X 가 되어 리담 짝을 풀고 새 uid(사용자 9/26 18:4x)
        T(g, 'F1b 옛 1,625줄 id·uid 무변 — 단 pdf 75 · 37번(P7-0283) 하나는 추록 가름으로 T1451105 → 새 uid T1451661',
          bad_uid == [('P7-0283', 'T1451105', 'T1451661')] and len(same) == len(base),
          {'옛': len(base), '남음': len(same), 'id·uid 바뀜': bad_uid[:5]})
        # F1e — 추록 우선(9/26 18:27 사용자) · 보이는 글(흰 상자 뒤 옛 글 뺌)로 다시 뽑은 다섯 곳 · 헛잣대 바탕 = 옛 글
        z83 = zmap.get('P7-0283') or {}
        z935, z633, z715 = zmap.get('P7-0293-5') or {}, zmap.get('P7-0633-3') or {}, zmap.get('P7-0715-1') or {}
        rs = {'37번': [z83.get('uid'), z83.get('ox'), '2023후10712' in (z83.get('sol') or ''), '해설 신규성' not in (z83.get('sol') or '')],
              '43번⑤': '2023후10712' in (z935.get('sol') or ''), '24번③': (z633.get('sol') or '').rstrip().endswith('보정을 할 수 없다.'),
              '33번①②': ['16. 8. 12' in (z715.get('sol') or ''), '15. 8. 12' not in (z715.get('sol') or '')], 'P7-2058': 'P7-2058' in zmap}
        T(g, 'F1e 추록 우선 — 37번 새 uid·X·추록 해설 · 43번 ⑤ · 24번 ③ 해설 추록 글 · 33번 ①② 16. 8. 12 · P7-2058 뺌(헛잣대: 바탕 = 옛 글)',
          rs == {'37번': ['T1451661', 'X', True, True], '43번⑤': True, '24번③': True, '33번①②': [True, True], 'P7-2058': False}, rs)
        suns = [z.get('순') for z in Z]
        order = sorted(Z, key=lambda z: (int(z['pdf쪽'] or 0), z['id']))
        T(g, 'F1c 순 = 빠짐없음 · 겹침 없음 · 책 차례(PDF쪽 → P7 id = 좌표 y·x · 선지 줄은 그 문항 자리)',
          all(isinstance(s, int) for s in suns) and len(set(suns)) == len(suns) and [z.get('순') for z in order] == list(range(1, len(Z) + 1)),
          {'순 있음': sum(1 for s in suns if isinstance(s, int)), '겹침': len(suns) - len(set(s for s in suns if s is not None))})
        uids = [z['uid'] for z in Z if z.get('uid')]
        T(g, 'F1d 제7판 줄 uid 겹침 0(관문 Q) · 새 사법·미기출 줄 uid 비움(기록 키 P7:id)',
          len(uids) == len(set(uids)) and all(not z.get('uid') for z in body if kind(z['태그']) in ('사법', '미기출') and z['id'] not in base),
          {'uid': len(uids), '겹침': len(uids) - len(set(uids))})
        # F2 — 골든 대조(마디 147 · no · 제목 · 깊이 · 조 · 리담) · 소제목 = 좌표 재계산(골든은 글 차례라 대조 안 함 · 표는 보고서)
        M = MG['마디']
        sk = len(M) == len(G) and all(a.get('no', '') == b['no'] and a['제목'] == b['제목'] and a['깊이'] == b['깊이'] for a, b in zip(M, G))
        T(g, 'F2a 마디 147 · no·제목·깊이 = 골든(헛잣대: 바탕 136마디)', sk, {'마디': len(M), '골든': len(G)})
        if len(M) == len(G):
            gjo = lambda b: [x.get('c', x.get('sep')) for x in (b.get('조') or [])]
            jd = [(a['no'], a.get('조'), gjo(b)) for a, b in zip(M, G) if (a.get('조') or []) != gjo(b)]
            T(g, 'F2b 조 = 골든(단 3.8.3 「42④⑧」 은 ⑧ 까지 — 골든 mkmg 가 항 첫 글자만 읽은 것 · 한 곳)',
              jd == [('3.8.3', ['특-42-4', '특-42-8'], ['특-42-4'])], jd[:4])
            rd = [(a['no'] or a['id'], sorted(set(a['리담']) - set(b['리담'])), sorted(set(b['리담']) - set(a['리담']))) for a, b in zip(M, G) if set(a['리담']) != set(b['리담'])]
            T(g, 'F2c 리담 = 골든(145마디) · 두 마디는 문항 담기가 바로잡혀 옮김(2019-56-14 : 7.3.2 PBP → 7.3.3 젭슨)',
              rd == [('7.3.2', [], ['2019-56-14']), ('7.3.3', ['2019-56-14'], [])] and sum(len(a['리담']) for a in M) == 373, rd[:4])
            subs = [(a['no'], a.get('소제목')) for a in M if a.get('소제목')]
            T(g, 'F2d 소제목 = 좌표 원장 재계산 67마디 · 3.3 신규성 비움 · 8.3.2.3 Ⅱ 별칭 = {당}통실허심판(138)',
              len(subs) == 67 and not next((a for a in M if a['no'] == '3.3'), {}).get('소제목') and
              any(len(x) == 3 and x[2] == '{당}통실허심판(138)' for x in next((a for a in M if a['no'] == '8.3.2.3'), {}).get('소제목', [])),
              {'마디': len(subs)})
        else:
            T(g, 'F2b~d 조·리담·소제목(마디 수가 달라 못 맞댐)', False, len(M))
        # F3 — OMR 칸 ↔ 책 번호 문항
        if '책수' in TOCJ and len(M) == len(TOCJ['마디']):
            omr = TOCJ['OMR']
            bk = TOCJ['책수']
            ok104 = sum(1 for k in omr if bk.get(k) == omr[k])
            diff = [(m['no'], bk.get(m['id']), omr[m['id']]) for m in TOCJ['마디'] if m['id'] in omr and bk.get(m['id']) != omr[m['id']]]
            T(g, 'F3 OMR 칸 합 1,680 · 책 절 107 중 104 = OMR 칸 수 · 예외 셋(사용자 9/26 18:27 · 책대로) = 진보성 37/38 · 확대선 21/22(책이 6·18번 건너뜀) · 침해 총설 4/3',
              sum(omr.values()) == 1680 and ok104 == 104 and diff == [('3.4', 37, 38), ('3.7', 21, 22), ('8.3.1', 4, 3)], {'104': ok104, '3': diff})
        else:
            T(g, 'F3 OMR 칸 ↔ 책 번호 문항(재료와 마디가 안 맞음 — 바탕)', False, {'마디': len(M)})
        # F4 — 모아보기 140 = 전부 본문 원본 id(새 id 0) · Ⅱ 3번 = 추록 P7-0285(9/26 18:27 사용자 「빨간 글 우선」 · P7-2058 대신)
        pan = [m for m in M if str(m.get('id', '')).startswith('FP')]
        pids = [z for m in pan for z in m['지문']]
        bodyids = {z for m in M if not str(m.get('id', '')).startswith('FP') for z in m['지문']}
        own = [z for z in pids if z not in bodyids]
        g2 = next((m for m in pan if str(m.get('제목', '')).startswith('Ⅱ')), {})
        T(g, 'F4 모아보기 140 = 전부 본문 마디 id(새 id 0) · Ⅱ 특허요건 3번 = 추록 P7-0285(P7-2058 대신)(헛잣대: 바탕 모아보기 없음)',
          len(pids) == 140 and len(set(pids)) == 140 and own == [] and (g2.get('지문') or [None] * 3)[2:3] == ['P7-0285'],
          {'모아보기': len(pids), '본문에 없음': own, 'Ⅱ 3번': (g2.get('지문') or [None] * 3)[2:3]})
        if tag == 'NEW':
            KEEP['data'] = {'M': M, 'P7': Z}


# ══════════ 앱 — 서버 · 쪽 ══════════
def serve(tag, src, mode='new'):
    key = tag + '|' + mode
    if key in SERVERS:
        return SERVERS[key][1]
    out = os.path.join(WORK, 'srv_%s_%s' % (tag, mode)); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    src = src.replace('\r\n', '\n')
    b = src.index('<body'); bb = src.index('>', b) + 1
    html = src[:bb] + CJ.SEED + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + TESTS + '\n</script>\n' + html[e:]
    io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)
    rev = None
    if mode == 'rev':   # 헛잣대 재료 — 2.2.1 의 지문 목록을 거꾸로(순 정렬이 없으면 거꾸로 그린다)
        mg = json.load(open(os.path.join(DATA, 'mokcha_병합.json'), encoding='utf-8'))
        for m in mg['마디']:
            if m.get('no') == '2.2.1':
                m['지문'] = list(reversed(m['지문']))
        rev = os.path.join(out, '_rev_mokcha.json')
        json.dump(mg, open(rev, 'w', encoding='utf-8'), ensure_ascii=False)

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=out, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            if p.startswith('/__vendor/'):
                return os.path.join(CJ.VENDOR, p[len('/__vendor/'):].replace('/', os.sep))
            if p.startswith('/data/'):
                if rev and p == '/data/mokcha_병합.json':
                    return rev
                return os.path.join(DATA, p[6:].replace('/', os.sep))
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
    def __init__(self, br, tag, src, W=1440, H=900, touch=False, mode='new'):
        self.tag, self.touch = tag, touch
        self.port = serve(tag, src, mode)
        self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, has_touch=touch)
        self.ctx.route('**/*', CJ.route_filter)
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(180000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' else None)
        self.cdp = self.ctx.new_cdp_session(self.pg) if touch else None
        self.pg.goto('http://127.0.0.1:%d/index.html?tok=1&who=%s' % (self.port, urllib.parse.quote('꼬까')), wait_until='load', timeout=180000)
        self.pg.wait_for_function(READY, timeout=180000)
        self.pg.wait_for_timeout(600)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def until(self, expr, arg=None, ms=15000):
        t0 = time.time()
        while time.time() - t0 < ms / 1000:
            v = self.ev(expr, arg)
            if v:
                return v
            self.pg.wait_for_timeout(80)
        return self.ev(expr, arg)

    def tap(self, x, y):
        """CDP 진짜 터치 한 번(반지름 22 — 아이패드 손가락 · 반지름 1 은 크기 판정 버그를 가린다)"""
        pt = [{'x': x, 'y': y, 'id': 1, 'radiusX': 22, 'radiusY': 22, 'force': 1}]
        self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': pt})
        self.pg.wait_for_timeout(60)
        self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})

    def click(self, at, wait=500):
        """진짜 포인터 — PC = mouse.click · 터치 문맥 = CDP 터치 · 자리가 가려 있으면(elementFromPoint ≠ 대상) 안 누르고 False"""
        if not at or not at.get('on'):
            return False
        if self.touch:
            self.tap(at['cx'], at['cy'])
        else:
            self.pg.mouse.click(at['cx'], at['cy'])
        self.pg.wait_for_timeout(wait)
        return True

    def shot(self, name):
        os.makedirs(SHOTS, exist_ok=True)
        f = os.path.join(SHOTS, name + '.png')
        try:
            tmp = os.path.join(WORK, name + '.png')
            self.pg.screenshot(path=tmp)
            b = open(tmp, 'rb').read()
            for _ in range(3):
                open(f, 'wb').write(b); time.sleep(0.5)
                if open(f, 'rb').read() == b:
                    break
            return f
        except Exception as e:
            return 'shot 실패 ' + repr(e)[:120]

    def errs_all(self):
        return [y for y in (self.errs + (self.ev("()=>__HT.errs()") or [])) if not CJ.NOISE(y)]

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


def keys_of(M, i, P7map, byId):
    n = M[i]
    ks = []
    for q in n['리담']:
        for z in (byId.get(q) or {}).get('지문', []):
            ks.append(z.get('uid') or ('L:%s#%s' % (q, z['n'])))
    for p in n['지문']:
        z = P7map.get(p)
        if z:
            ks.append(z.get('uid') or 'P7:' + z['id'])
    return ks


# ══════════ 책상(마우스) ══════════
def scen(br, src, tag, touch=False):
    g = '%s %s' % (tag, '손가락' if touch else '책상')
    p = Pg(br, tag, src, 1440, 900, touch=touch)

    def sec(name, fn):
        try:
            fn()
        except Exception as ex:
            T(g, name + ' 묶음 예외', False, repr(ex)[:400])

    def home():
        return p.ev("async()=>await __HT.home()")

    # F6 — 조문 칩(서랍 · 첫 화면)
    def s6():
        home()
        at = p.ev("([l,c])=>__HT.jtChip(l,c)", [L_221, '특3'])
        st0 = p.ev("()=>__HT.state()")
        clicked = p.click(at, 900)
        pop = p.until("()=>__HT.joPop('제3조')&&__HT.joPop('제3조').title.indexOf('미성년자')>=0?__HT.joPop('제3조'):null", None, 8000)
        st1 = p.ev("()=>__HT.state()")
        T(g, 'F6a 서랍 2.2.1 「특3」 누름 → 「특허 제3조 미성년자 등의 행위능력」 팝업 보임 · S.mok 무변(헛잣대: 바탕 칩 없음)',
          clicked and bool(pop) and pop['vis'] and pop['title'] == '특허 제3조 미성년자 등의 행위능력' and st1['mok'] == st0['mok'] == '',
          {'칩': at and {k: at.get(k) for k in ('text', 'on', 'at', 'fs', 'fw')}, 'pop': pop, 'mok': [st0['mok'], st1['mok']]})
        T(g, 'F6c 서랍 칩 글자 9.5px · 굵기 500', bool(at) and at.get('fs') == '9.5px' and at.get('fw') == '500', at and [at.get('fs'), at.get('fw')])
        if tag == 'NEW' and not touch:
            p.shot('NEW_F6_drawer_chip_pop')
        p.ev("()=>__HT.closeAll()"); p.pg.wait_for_timeout(200)
        at2 = p.ev("([l,c])=>__HT.homeChip(l,c)", [L_221, '특3'])
        clicked2 = p.click(at2, 900)
        pop2 = p.until("()=>__HT.joPop('제3조')", None, 8000)
        st2 = p.ev("()=>__HT.state()")
        T(g, 'F6b 첫 화면 2.2.1 「특3」 누름 → 같은 팝업 보임 · 줄 누름(단원 열기)으로 안 샘 · 칩 11px',
          clicked2 and bool(pop2) and pop2['vis'] and pop2['title'] == '특허 제3조 미성년자 등의 행위능력' and st2['mok'] == '' and (at2 or {}).get('fs') == '11px',
          {'칩': at2 and {k: at2.get(k) for k in ('text', 'on', 'at', 'fs')}, 'pop': pop2, 'mok': st2['mok']})
        p.ev("()=>__HT.closeAll()")

    # F7 — 소제목 ▸
    def s7():
        home()
        t0 = p.ev("l=>__HT.subTg(l)", L_12)
        st0 = p.ev("()=>__HT.state()")
        l0 = p.ev("l=>__HT.subList(l)", L_12)
        c1 = p.click(t0, 400)
        l1 = p.ev("l=>__HT.subList(l)", L_12); t1 = p.ev("l=>__HT.subTg(l)", L_12); st1 = p.ev("()=>__HT.state()")
        T(g, 'F7a 1.2 국제조약 ▸ 누름 → 목록 보임(7줄) · 「▾」 · S.mok 무변 · 처음엔 접힘(헛잣대: 바탕 ▸ 없음)',
          c1 and bool(l0) and l0.get('list') and not l0['vis'] and l1['vis'] and len(l1['rows']) == 7 and (t1 or {}).get('t') == '▾' and st1['mok'] == st0['mok'] == '',
          {'전': l0 and l0.get('vis'), '뒤': l1 and {'vis': l1.get('vis'), 'n': len(l1.get('rows') or [])}, '글': (t1 or {}).get('t'), 'mok': st1['mok'], 'rows': (l1 or {}).get('rows', [])[:3]})
        if tag == 'NEW' and not touch:
            p.shot('NEW_F7_sub_open')
        c2 = p.click(p.ev("l=>__HT.subTg(l)", L_12), 400)
        l2 = p.ev("l=>__HT.subList(l)", L_12); t2 = p.ev("l=>__HT.subTg(l)", L_12)
        T(g, 'F7b 다시 누르면 안 보임(화면 기준) · 「▸」', c2 and bool(l2) and l2.get('list') and not l2['vis'] and (t2 or {}).get('t') == '▸', {'vis': l2 and l2.get('vis'), '글': (t2 or {}).get('t')})
        T(g, 'F7c ▸ 꼴 — 11px · 굵기 400 · #8a8479 · 누름 자리 14px · 원래 「›」 숨김(화살표 하나)',
          bool(t0) and t0['fs'] == '11px' and t0['fw'] == '400' and t0['color'] == 'rgb(138, 132, 121)' and abs(t0['w'] - 14) < 0.6 and
          not (p.ev("l=>__HT.homeRowInfo(l)", L_12) or {}).get('ar'), t0 and {k: t0[k] for k in ('fs', 'fw', 'color', 'w')})
        s33 = p.ev("l=>__HT.subTg(l)", L_33)
        r33 = p.ev("l=>__HT.homeRowInfo(l)", L_33)
        T(g, 'F7d 3.3 신규성은 ▸ 없음(사용자 「여기만 글 없애 줘」) · 줄은 있음', s33 is None and bool(r33), {'▸': s33, '줄': bool(r33)})
        p.click(p.ev("l=>__HT.subTg(l)", L_8323), 400)
        l3 = p.ev("l=>__HT.subList(l)", L_8323)
        T(g, 'F7e 8.3.2.3 목록에 「Ⅱ 통상실시권 허여심판 = {당}통실허심판(138)  8문제」', bool(l3) and l3.get('vis') and any('= {당}통실허심판(138)' in r['t'] for r in l3['rows']),
          (l3 or {}).get('rows'))
        if tag == 'NEW' and not touch:
            p.shot('NEW_F7_sub_8323')
        p.click(p.ev("l=>__HT.subTg(l)", L_8323), 300)

    # F8 — 12 실용신안 편 한 줄
    def s8():
        home()
        so = p.ev("()=>__HT.solo()")
        ch = p.ev("l=>__HT.cardHead(l)", '12 실용신안')
        exp = KEEP.get('n12')
        T(g, 'F8a 첫 화면 편 줄 「12 실용신안 총 %s문제」 · 회독 칸(단추) · 🃏 · 17px 굵게 · 12px 16px · 편 머리 바탕(헛잣대: 바탕 「총 0문제」 머리)' % exp,
          bool(so) and so['text'].startswith('▸12 실용신안') and so['tot'] == '총 %s문제' % exp and so['go'] and so['card'] and so['fs'] == '17px' and so['fw'] == '700' and
          so['pad'] == '12px 16px' and so['bg'] == 'rgb(246, 244, 239)' and ch is None,
          {'solo': so and {k: so[k] for k in ('text', 'tot', 'goTxt', 'fs', 'fw', 'pad', 'bg')}, '옛 머리': ch})
        T(g, 'F8b 「12. 실용신안」 줄이 따로 없다(첫 화면에 그 이름 한 번)', p.ev("l=>__HT.homeNames(l)", '12 실용신안') == 1 and p.ev("l=>__HT.homeNames(l)", '12. 실용신안') == 0,
          [p.ev("l=>__HT.homeNames(l)", '12 실용신안'), p.ev("l=>__HT.homeNames(l)", '12. 실용신안')])
        i12 = p.ev("n=>__HT.Mi(n)", '12')
        c = p.click(so, 1200)
        st = p.until("()=>__HT.state().mok&&__HT.cards().length?__HT.state():null", None, 15000)
        cards = p.ev("()=>__HT.cards()")
        T(g, 'F8c 편 줄 누름 → S.mok === __mg%s · 문항이 열림' % i12, c and bool(st) and st['mok'] == '__mg%s' % i12 and len(cards) > 0,
          {'mok': st and st['mok'], '카드': len(cards or [])})

    # F9 — 머리 같은 이름 두 번 → 한 줄
    def s9():
        home()
        n38 = p.ev("l=>__HT.jtCount(l)", L_38)
        i38 = p.ev("n=>__HT.Mi(n)", '3.8')
        T(g, 'F9a 서랍 「3.8 명세서 기재불비」 이름 줄 = 머리 하나(헛잣대: 바탕 2)', n38 == 1, n38)
        at = p.ev("l=>__HT.jtName(l)", L_38)
        c = p.click(at, 900)
        st = p.until("m=>__HT.state().mok===m?__HT.state():null", '__mg%s' % i38, 10000)
        T(g, 'F9b 서랍 머리 이름 누름 → S.mok === __mg%s(바로 밑 문항)' % i38, c and bool(st), {'mok': p.ev("()=>__HT.state()")['mok'], 'at': at and at.get('at')})
        v0 = p.ev("l=>__HT.jtVis(l)", L_381)
        ar = p.ev("l=>__HT.jtArrow(l)", L_38)
        c2 = p.click(ar, 500)
        v1 = p.ev("l=>__HT.jtVis(l)", L_381); st2 = p.ev("()=>__HT.state()")
        T(g, 'F9c 서랍 ▾ 누름 → 3.8.1 줄 안 보임 · S.mok 무변(헛잣대: 바탕 ▾ 없음)', c2 and v0 == [True] and v1 in ([], [False]) and st2['mok'] == '__mg%s' % i38,
          {'3.8.1 전': v0, '뒤': v1, 'mok': st2['mok'], '▾': ar and ar.get('t')})
        p.click(p.ev("l=>__HT.jtArrow(l)", L_38), 400)
        home()
        nh = p.ev("l=>__HT.homeNames(l)", L_38)
        hd = p.ev("l=>__HT.homeHead(l)", L_38)
        c3 = p.click(hd, 1000)
        st3 = p.until("m=>__HT.state().mok===m?__HT.state():null", '__mg%s' % i38, 10000)
        T(g, 'F9d 첫 화면 3.8 머리 한 줄(이름 한 번) · 머리 누름 → 열림(헛잣대: 바탕 = 안 열림 · 이름 둘)',
          nh == 1 and c3 and bool(st3) and bool(hd) and hd.get('go'), {'이름 수': nh, 'mok': p.ev("()=>__HT.state()")['mok'], 'title': hd and hd.get('title')})

    # F5 — 줄 순서(2.2.1)
    def s5():
        home()
        c = p.click(p.ev("l=>__HT.jtName(l)", L_221), 1000)
        p.until("()=>__HT.cards().length", None, 10000)
        cs = [x for x in p.ev("()=>__HT.cards()") if x['p7']]
        sun = [x['sun'] for x in cs]
        T(g, 'F5a 2.2.1 주체 능력 문항 화면 — 제7판 줄 차례 = 순 오름차순', c and len(sun) > 5 and all(sun[i] < sun[i + 1] for i in range(len(sun) - 1)),
          {'줄': len(sun), '순 앞': sun[:6]})

    for nm, fn in (('F6', s6), ('F7', s7), ('F8', s8), ('F9', s9), ('F5', s5)):
        sec(nm, fn)
    if not touch:
        sec('F10', lambda: s10(p, g, tag))
        sec('F12', lambda: s12(p, g, tag))
    es = p.errs_all()
    T(g, 'Z 페이지 오류 0', not es, es[:5])
    p.close()


def s10(p, g, tag):
    """모아보기 — 같은 키 · mokIndex = 본문 마디 · 셈"""
    p.ev("async()=>await __HT.home()")
    p.ev("async()=>{if(typeof UZGK!=='undefined'){UZGK='x';await __HT.rr();}return 1}")   # ★ mbsame_add3 §A-8(9/27) — 모아보기(미기출) = 기타 · 첫 화면 처음 = 기출이라 기타로 돌려 잰다(옛 판 = UZGK 없음 · 무동작)
    D = KEEP['data']
    M = D['M']
    iII = next(i for i, m in enumerate(M) if m.get('제목') == 'Ⅱ 특허요건')
    first = M[iII]['지문'][0]
    z = next(x for x in D['P7'] if x['id'] == first)
    key = z.get('uid') or 'P7:' + z['id']
    at = p.ev("l=>{const r=__HT.homeRow(l);return r?__HT.hitOn(r.querySelector('.nm')):null}", 'Ⅱ 특허요건')
    c = p.click(at, 1200)
    p.until("()=>__HT.cards().length", None, 10000)
    ob = p.ev("([k,v])=>__HT.oxBtn(k,v)", [key, 'O'])
    c2 = p.click(ob, 600)
    rec = p.ev("k=>__HT.oxRec(k)", key)
    body_i = next(i for i, m in enumerate(M) if first in m['지문'] and not str(m['id']).startswith('FP'))
    mi = p.ev("async id=>await __HT.mokIndexOf(id)", first)
    p.ev("async i=>{S.mok='__mg'+i;S.oxPage=null;await __HT.rr();return 1}", body_i)
    p.until("()=>__HT.cards().length", None, 10000)
    ob2 = p.ev("([k,v])=>__HT.oxBtn(k,v)", [key, 'O'])
    T(g, 'F10a 모아보기 Ⅱ 특허요건 첫 문항 O 찍기(mouse.click) → 본문 원래 마디(%s)에서도 같은 표시가 보임(같은 키 %s)' % (M[body_i]['no'], key),
      c and c2 and (rec or {}).get('m') == 'O' and bool(ob2) and ob2['sel'], {'rec': rec, '본문 O sel': ob2 and ob2['sel']})
    T(g, 'F10b 그 지문의 mokIndex = 먼저 나온 본문 마디(모아보기 아님)', mi == body_i, {'mokIndex': mi, '본문': body_i, '모아보기': iII})
    p.ev("async()=>{if(typeof UZGK!=='undefined')UZGK='g';await __HT.home();return 1}")   # ★ mbsame_add3 §A-8 — 기출(처음 값)로 되돌림
    ht = p.ev("()=>__HT.heat()")
    ct = p.ev("()=>__HT.cardTots()")
    pan = next((x for x in ct if x['h'] == '미기출 판례 모아보기'), None)
    T(g, 'F10c 히트맵 「전체」 = 지문 풀(같은 키 한 번 · 모아보기 겹침 없음) = %s · 모아보기 카드 「총 140문제」' % KEEP.get('pool'),
      bool(ht) and ht['sum'] == ht['pool'] == KEEP.get('pool') and bool(pan) and pan['tot'] == '총 140문제', {'heat': ht and {'sum': ht['sum'], 'pool': ht['pool']}, '모아보기': pan})
    p.ev("k=>{try{oxClear(k)}catch(e){}return 1}", key)


def s12(p, g, tag):
    """객관식 선지 줄 — 「N번 - (k)」 · 종합사례 상자"""
    D = KEEP['data']
    M = D['M']
    for pid, box in (('P7-0137', True), ('P7-1785', False)):
        i = next(j for j, m in enumerate(M) if pid + '-1' in m['지문'] and not str(m['id']).startswith('FP'))
        p.ev("async i=>{S.mok='__mg'+i;S.oxPage=null;await __HT.rr();return 1}", i)
        p.until("()=>__HT.cards().length", None, 10000)
        pg = p.ev("async id=>{const all=__HT.cards();const c=all.find(x=>x.p7===id+'-1');if(!c)return {miss:true,n:all.length};return {miss:false}}", pid)
        if pg.get('miss'):   # 20장씩 쪽 — 그 줄이 있는 쪽으로
            p.ev("async([id])=>{for(let k=0;k<20;k++){S.oxPage=k;await __HT.rr();if(__HT.cards().some(x=>x.p7===id+'-1'))return k;}return -1}", [pid])
        cs = [x for x in p.ev("()=>__HT.cards()") if x['p7'] and x['p7'].startswith(pid + '-')]
        bx = p.ev("()=>__HT.cases()")
        seq = [x['seq'] for x in cs]
        n0 = re.match(r'^(\d+)번', seq[0] or '') if seq else None
        okseq = bool(n0) and seq == ['%s번 - (%d)' % (n0.group(1), k) for k in range(1, 6)]
        if box:
            okb = all(x['inCase'] for x in cs) and any(b['h'] == '[종합사례 원문] - %s번' % n0.group(1) and b['n'] >= 5 for b in bx) if n0 else False
        else:
            okb = not any(x['inCase'] for x in cs)
        T(g, 'F12 객관식 %s → 선지 줄 5 · 번호 「N번 - (1)~(5)」 · %s' % (pid, '종합사례 상자 한 벌 「[종합사례 원문] - N번」' if box else '상자 없음(단순 「…설명으로 옳지 않은 것은?」)'),
          len(cs) == 5 and okseq and okb, {'번호': seq, '상자': bx[:2], '마디': M[i]['no']})
        if tag == 'NEW' and box:
            p.shot('NEW_F12_case_box')


# ══════════ 다른 법(상표) 1차객 첫 화면·서랍 — 바탕과 맞대기 ══════════
def other_law(br, src, tag):
    p = Pg(br, tag, src)
    try:
        out = p.ev("""async()=>{try{closeAllPops();}catch(e){}S.law='상표법';S.tab='jimun';S.jimunTab='ox';S.mok='';S.oxQueue='';S.oxQ='';
          await render();for(let i=0;i<200&&typeof busy!=='undefined'&&busy;i++)await new Promise(r=>setTimeout(r,25));await new Promise(r=>setTimeout(r,400));
          const d=document.querySelector('.mbdash'),j=document.getElementById('jtlist');
          const pos=e=>e?[...e.querySelectorAll('.n,.tot,.nm,.tx')].slice(0,80).map(x=>{const r=x.getBoundingClientRect();return Math.round(r.left)+','+Math.round(r.top)}).join(';'):'';
          return {dash:d?d.innerText.length+':'+d.querySelectorAll('*').length:null,jt:j?j.innerText.length+':'+j.querySelectorAll('*').length:null,pos:pos(d)+'|'+pos(j)};}""")
        KEEP.setdefault('other', {})[tag] = out
        N('%s 상표' % tag, '상표 1차객 첫 화면·서랍 DOM(글자 수:요소 수 · 자리) — 맞대기는 끝에', out)
    finally:
        p.close()


def report():
    lines = []
    head = ['# _harness_jo_toc_fuse 결과 — %s' % time.strftime('%Y-%m-%d %H:%M'),
            'NEW = %s (md5 LF %s) · BASE = genie %s (md5 %s) · 데이터 = %s' % (
                NEWF, hashlib.md5(io.open(NEWF, encoding='utf-8', newline='').read().replace('\r\n', '\n').encode('utf-8')).hexdigest()[:8], BASE_REV, BASE_MD5[:8], DATA)]
    for grp, name, ok, d in RES:
        dd = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str)
        lines.append('%s | %s · %s | %s' % ('NOTE' if ok is None else 'PASS' if ok else 'FAIL', grp, name, dd[:900]))
    npass = sum(1 for r in RES if r[2] is True and not r[0].startswith(('BASE', '데이터 BASE')))
    nfail = sum(1 for r in RES if r[2] is False and not r[0].startswith(('BASE', '데이터 BASE')))
    bpass = sum(1 for r in RES if r[2] is True and r[0].startswith(('BASE', '데이터 BASE')))
    bfail = sum(1 for r in RES if r[2] is False and r[0].startswith(('BASE', '데이터 BASE')))
    head.append('새 판 PASS %d · FAIL %d · 바탕(헛잣대) PASS %d · FAIL %d' % (npass, nfail, bpass, bfail))
    f = os.path.join(OUT, '_harness_jo_toc_fuse_result.txt')
    txt = '\n'.join(head + [''] + lines) + '\n'
    for _ in range(3):
        io.open(f, 'w', encoding='utf-8', newline='\n').write(txt); time.sleep(0.5)
        if io.open(f, encoding='utf-8').read() == txt:
            break
    print('\n'.join(head))


def main():
    os.makedirs(WORK, exist_ok=True)
    base_src = git('show', 'HEAD:jo/index.html').decode('utf-8')
    assert hashlib.md5(base_src.encode('utf-8')).hexdigest() == BASE_MD5, 'HEAD 가 바탕(f497f05)이 아니다'
    new_src = io.open(NEWF, encoding='utf-8', newline='').read()
    if not ONLY or 'data' in ONLY:
        data_gates()
    else:
        KEEP['data'] = {'M': jload_new('mokcha_병합.json')['마디'], 'P7': jload_new('jimun_7pan.json')['지문']}
    D = KEEP['data']
    P7map = {z['id']: z for z in D['P7']}
    JM = jload_new('jimun_특허.json')
    byId = {q['id']: q for q in JM['문제']}
    i12 = next(i for i, m in enumerate(D['M']) if m.get('no') == '12')
    KEEP['n12'] = len(keys_of(D['M'], i12, P7map, byId))
    pool = set()
    for q in JM['문제']:
        for z in q['지문']:
            pool.add(z.get('uid') or ('L:%s#%s' % (q['id'], z['n'])))
    for z in D['P7']:
        if not z.get('병합'):
            pool.add(z.get('uid') or 'P7:' + z['id'])
    KEEP['pool'] = len(pool)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        if not ONLY or 'base' in ONLY:
            scen(br, base_src, 'BASE')
            # F5 헛잣대 — 2.2.1 지문 목록을 거꾸로 준 재료(순 정렬이 없으면 거꾸로 그린다)
            for tag, src in (('BASE', base_src), ('NEW', new_src)):
                p = Pg(br, tag, src, mode='rev')
                try:
                    p.ev("async()=>await __HT.home()")
                    p.click(p.ev("l=>__HT.jtName(l)", L_221), 1000)
                    p.until("()=>__HT.cards().length", None, 10000)
                    sun = [x['sun'] for x in p.ev("()=>__HT.cards()") if x['p7']]
                    T('%s 거꾸로 재료' % tag, 'F5b 2.2.1 지문 목록을 거꾸로 준 재료에서도 순 오름차순으로 그린다(헛잣대: 바탕은 거꾸로 그대로)',
                      len(sun) > 5 and all(sun[i] < sun[i + 1] for i in range(len(sun) - 1)), {'순 앞': sun[:6]})
                finally:
                    p.close()
            other_law(br, base_src, 'BASE')
        if not ONLY or 'new' in ONLY:
            scen(br, new_src, 'NEW')
            other_law(br, new_src, 'NEW')
        if not ONLY or 'touch' in ONLY:
            scen(br, new_src, 'NEW', touch=True)
        br.close()
    if 'BASE' in KEEP.get('other', {}) and 'NEW' in KEEP.get('other', {}):
        T('NEW 상표', 'E 상표 1차객 첫 화면·서랍 = 바탕(글자 수·요소 수·자리)', KEEP['other']['BASE'] == KEEP['other']['NEW'], KEEP['other'])
    report()


if __name__ == '__main__':
    main()
