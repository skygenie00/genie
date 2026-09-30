# -*- coding: utf-8 -*-
r"""_task_jo_book8 §B 관문 하네스 — 특허법 해례 제8판 교재 올리기(굽기 · 대응표 · 앱 「📚 교재 자리」 8판 줄).

  python _harness_jo_book8.py --new <앱> [--data <jo/data>] [--exam <gichul/pdf>] [--res <결과>] [--eng chromium,webkit] [--only d1,d2,a3,...]

  NEW  = 이 판 앱 · BASE = genie HEAD(jo_p8up 인도판 = 바로 앞 인도판) 앱 — 칸마다 헛잣대(바탕에서 FAIL) · 데이터는 둘 다 genie jo/data(이 판은 데이터 무변)
  교재 = 비공개 minbeoppdf 로컬 클론(pdf/ · words/patent_hr8/ · 대응.json) — 페이지 fetch 를 같은 출처 /__book/ 으로 돌려 준다(토큰 없이 · SEED) · pdf.js = 로컬 vendor
  누름 = 진짜 포인터(page.mouse · 손가락 = Chromium CDP 터치 r22 · WebKit touchscreen.tap) · 보임 = display ≠ none · 높이 > 0 · 자리 = elementFromPoint
  ⚠ 8판 PDF 는 워터마크 헛잣대(센 수)에만 연다 — 값은 안 찍는다.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
_NR = _roots.need_n('민법 교재 낱말 굽기 스크립트(minbeop/script/_book_words_build.py)')   # env_lanes_fix(9/29) — N: 작업 폴더 · 없으면(클라우드) 「N: 필요 — 클라우드 불가(…)」 종료 코드 3
import io, json, os, re, sys, time, gzip, glob, shutil, hashlib, tempfile, subprocess, threading, socketserver, http.server, urllib.parse, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
JOP = os.path.dirname(HERE)


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


_NEW = ARG('--new')
_DATA = ARG('--data', _roots.genie(r'jo\data'))
_EXAM = ARG('--exam')
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_book8_result.txt'))
MBP = ARG('--mbpdf', _roots.mbpdf())
W8 = os.path.join(MBP, 'words', 'patent_hr8')
PDF8 = os.path.join(JOP, '특상디', '_pdf', '특허법 해례 기출 객관식 제8판.pdf')
BAKE = os.path.join(_NR, 'minbeop', 'script', '_book_words_build.py')
sys.argv = [sys.argv[0], '--new', _NEW, '--data', _DATA, '--base', 'HEAD'] + (['--exam', _EXAM] if _EXAM else [])
sys.path.insert(0, HERE)
sys.path.insert(0, JOP)
import _harness_jo_gaek_mbsame as M   # noqa: E402
import _book8_map as BM               # noqa: E402
from playwright.sync_api import sync_playwright   # noqa: E402
M.TESTS = M.TESTS + '\n' + io.open(os.path.join(HERE, '_harness_jo_uidmbs2_tests.js'), encoding='utf-8').read() \
    + '\n' + io.open(os.path.join(HERE, '_harness_jo_book8_tests.js'), encoding='utf-8').read()
M.WORK = M.WORK + '_b8'
RES = []
SAMPLE = [('TJ0100001', 'P7-0000-1'), ('T2562011', 'P7-0089'), ('T1552093', 'P7-1662')]
WMRX = re.compile(r'@|01[016789][-\s./]?\d{3,4}[-\s./]?\d{4}')


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def jl(p):
    return json.loads(open(p, 'rb').read().decode('utf-8'))


# ── mbsame 서버에 /__book/ 길을 더한다(M.serve 를 갈아 끼움 · Pg 가 모듈 이름으로 부른다) ──
_serve0 = M.serve
BOOKREQ = collections.Counter()


def serve(tag, src, data, exam):
    key = tag + '|' + data + '|' + exam
    if key in M.SERVERS:
        return M.SERVERS[key][1]
    out = os.path.join(M.WORK, 'srv_%s_%d' % (tag, len(M.SERVERS)))
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    src = src.replace('\r\n', '\n')
    b = src.index('<body'); bb = src.index('>', b) + 1
    AUTO = "<script>try{localStorage.setItem('jopangi_auto',JSON.stringify({important:'v1',at:'2026-08-28T16:48:32.584Z'}));}catch(e){}</script>"
    html = src[:bb] + M.CJ.SEED + AUTO + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + M.TESTS + '\n</script>\n' + html[e:]
    io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=out, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            if p.startswith('/__vendor/'):
                return os.path.join(M.CJ.VENDOR, p[len('/__vendor/'):].replace('/', os.sep))
            if p.startswith('/__book/'):
                BOOKREQ[tag + '|' + p.split('/')[2]] += 1
                return os.path.join(MBP, p[len('/__book/'):].replace('/', os.sep))
            if p.startswith('/data/'):
                return os.path.join(data, p[6:].replace('/', os.sep))
            if p.startswith('/gichul/pdf/'):
                return os.path.join(exam, p[len('/gichul/pdf/'):].replace('/', os.sep))
            if p in ('/index.html', '/'):
                return super().translate_path(path)
            f = os.path.join(M.JOD, p.lstrip('/').replace('/', os.sep))
            return f if os.path.exists(f) else super().translate_path(path)

        def log_message(self, *a, **k):
            pass
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    M.SERVERS[key] = (srv, srv.server_address[1])
    return srv.server_address[1]


M.serve = serve


class Pg(M.Pg):
    def __init__(self, br, eng, tag, src, data, exam, W=1440, H=900, **k):
        self.eng = eng
        ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, has_touch=True)
        super().__init__(br, tag + '_' + eng, src, data, exam, ctx=ctx, **k)

    def tap(self, at, wait=500):
        if not at or not at.get('on'):
            return False
        if self.eng == 'webkit':
            self.pg.touchscreen.tap(at['cx'], at['cy'])
            self.pg.wait_for_timeout(wait)
            return True
        return super().tap(at, wait)

    def press(self, at, how, wait=500):
        return self.tap(at, wait) if how == 'touch' else self.click(at, wait)

    def drag(self, x0, y0, x1, y1, n=14):
        m = self.pg.mouse
        m.move(x0, y0); m.down()
        for i in range(1, n + 1):
            m.move(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.pg.wait_for_timeout(16)
        m.up()
        return 'mouse'


def home(p, gk='g', law='특허법'):
    p.ev("l=>__HM.home(l)", law)
    if p.ev("()=>__UZ.has('UZGK')"):
        p.ev("v=>__UZ.gk(v)", gk)


def go_key(p, k):
    home(p)   # 1차객 재료(VJ)가 선 뒤에 갈래를 잰다(없으면 uzIsGi 가 늘 기출)
    gk = p.ev("k=>{try{return uzIsGi(k)?'g':'x'}catch(e){return 'g'}}", k)
    home(p, gk)
    sel = p.ev("k=>__UZ.selOfKey(k)", k)
    if not sel:
        return None
    p.ev("s=>__HM.go(s)", sel)
    pg = p.ev("k=>{const P=(OXPOOL||{})[k];if(!P)return null;const d=P.dom;const c=document.getElementById(d);return c?null:(OXDOMPG||{})[d]}", k)
    if pg:
        p.ev("n=>__HM.page(n)", pg)
    p.pg.wait_for_timeout(300)
    return sel


def open_card(p, k):
    """그 지문 카드를 화면에 — 단원 줄에 서면 그 줄 · 마디에 안 붙은 지문(P7-0000-1 등)은 사람처럼 🔍 검색 줄 누름 → 지문 팝업"""
    if go_key(p, k):
        return 'unit'
    home(p, p.ev("k=>{try{return uzIsGi(k)?'g':'x'}catch(e){return 'g'}}", k))   # go_key 가 이미 첫 화면을 열어 VJ 가 서 있다
    p.click(p.ev("()=>__HM.at('#slot .mbsr input')"), 200)
    p.pg.keyboard.type(k); p.pg.wait_for_timeout(800)
    row = p.ev("()=>{const r=[...document.querySelectorAll('#slot .mbres .rr')].find(x=>typeof x.onclick==='function');if(!r)return null;r.scrollIntoView({block:'center'});"
               "const b=r.getBoundingClientRect(),at=document.elementFromPoint(b.left+b.width/2,b.top+b.height/2);return {cx:b.left+b.width/2,cy:b.top+b.height/2,on:!!at&&r.contains(at)};}")
    p.click(row, 1500)
    return 'search' if row else None


# ══════════ 데이터 관문 ══════════
def page_chars(p):
    o = json.loads(gzip.decompress(open(os.path.join(W8, 'ox_book_patent_hr8_p%d.json.gz' % p), 'rb').read()).decode('utf-8'))
    return [(r[0], int(r[1]), int(r[2])) for r in (l.split('\t') for l in o['words'].split('\n') if l)]


def rect_text(p, r):
    """r = 0~2000 · 자리 상자 안 글자(흐름 차례 · KEEP 만 · 명칭 맞춤)"""
    return BM.norm(''.join(c for c, x, y in page_chars(p) if r[0] <= x <= r[2] and r[1] <= y <= r[3]))


def d_b1():
    """§B-1 굽기 — 책메타 · 워터마크 0 · 멱등 · 원격 = 로컬"""
    G = '1'
    meta = jl(os.path.join(W8, '책메타.json'))
    T(G, '책메타 — docid patent_hr8 · pages 805 · pdfMd5 = 원본 94f115f0… · printOffset −10 · 쪽 파일 805 · pageHash 805',
      meta.get('pages') == 805 and meta.get('pdfMd5') == '94f115f0a0e2d4387278e600e12fb753' and meta.get('printOffset') == -10
      and len(glob.glob(os.path.join(W8, 'ox_book_patent_hr8_p*.json.gz'))) == 805 and len(meta.get('pageHash') or []) == 805,
      {k: meta.get(k) for k in ('docid', 'file', 'pages', 'pdfMd5', 'printOffset', 'unit', 'norm', 'wmDropped')})
    at = ph = band = 0
    for p in range(1, 806):
        cs = page_chars(p)
        s = ''.join(c for c, _, _ in cs)
        at += s.count('@'); ph += len(re.findall(r'(?<!\d)01[016789][-.]?\d{3,4}[-.]?\d{4}(?!\d)', s)); band += sum(1 for _, _, y in cs if y >= 1974)
    T(G, '글자층 805 쪽 — 「@」 0 · 휴대전화 꼴(앞뒤 숫자 없음) 0 · 쪽 아래 띠(y ≥ 1974 = 830pt) 글자 0', at == 0 and ph == 0 and band == 0, {'@': at, '전화 꼴': ph, '아래 띠': band})
    import pymupdf
    doc = pymupdf.open(PDF8)
    raw = sum(1 for pg in doc for b in pg.get_text('rawdict')['blocks'] if b.get('type') == 0 for l in b['lines']
              if WMRX.search(''.join(c['c'] for s in l['spans'] for c in s['chars'])))
    T(G + '-헛', '헛잣대 — 원본 PDF 글자층(빼기 전)에는 워터마크 꼴 줄이 있다(센 수만 · 값 안 찍음)', raw > 0, {'워터마크 꼴 줄': raw})
    # 멱등 — 새 자리에 두 번 굽기 → 쪽 바이트 = 올린 것 · 책메타(builtAt 빼고) 같음 · 두 번째 = 첫 번째(바이트)
    tmp = os.path.join(tempfile.gettempdir(), 'h_book8_bake')
    shutil.rmtree(tmp, ignore_errors=True)
    env = dict(os.environ, MINBEOP_BOOK_OUT=tmp, PYTHONIOENCODING='utf-8')
    outs = []
    for _ in range(2):
        subprocess.run([sys.executable, BAKE, 'patent_hr8'], env=env, capture_output=True)
        d = os.path.join(tmp, 'patent_hr8')
        outs.append({f: hashlib.md5(open(os.path.join(d, f), 'rb').read()).hexdigest() for f in os.listdir(d)})
    mine = {f: hashlib.md5(open(os.path.join(W8, f), 'rb').read()).hexdigest() for f in os.listdir(W8) if f.endswith('.gz')}
    m2 = jl(os.path.join(tmp, 'patent_hr8', '책메타.json'))
    same_meta = {k: v for k, v in m2.items() if k != 'builtAt'} == {k: v for k, v in meta.items() if k != 'builtAt'}
    T(G, '멱등 — 새 자리에 두 번 구움 → 두 번째 = 첫 번째(806 파일 바이트) · 쪽 805 = 올린 것(바이트) · 책메타 = 올린 것(builtAt 빼고)',
      outs[0] == outs[1] and all(outs[0].get(f) == h for f, h in mine.items()) and len(mine) == 805 and same_meta,
      {'파일': len(outs[0]), '쪽 같음': sum(1 for f, h in mine.items() if outs[0].get(f) == h), '책메타': same_meta})
    # 원격 = 로컬(비공개 저장소 · 받는 쪽 md5)
    git = lambda *a: subprocess.run(['git', '-C', MBP, '-c', 'core.quotepath=false'] + list(a), capture_output=True)
    git('fetch', '-q')
    rem = {}
    for f in ('pdf/patent_hr8.pdf', 'words/patent_hr8/책메타.json', 'words/patent_hr8/대응.json', 'words/patent_hr8/ox_book_patent_hr8_p401.json.gz'):
        b = git('show', 'origin/main:' + f).stdout
        loc = open(os.path.join(MBP, f.replace('/', os.sep)), 'rb').read() if os.path.exists(os.path.join(MBP, f.replace('/', os.sep))) else None
        rem[f] = [hashlib.md5(b).hexdigest()[:8] if b else None, hashlib.md5(loc).hexdigest()[:8] if loc else None]
    T(G, '비공개 저장소 원격(origin/main) = 로컬 md5 — pdf(94f115f0) · 책메타 · 대응.json · 쪽 한 장', all(a and a == b for a, b in rem.values()) and rem['pdf/patent_hr8.pdf'][0] == '94f115f0', rem)


def d_b2():
    """§B-2 대응표 — 셈 · 채팅 표 대조 · 표본 셋 자리 글 = 지문 글"""
    G = '2'
    D = jl(os.path.join(W8, '대응.json'))
    meta = D.get('_meta') or {}
    rows = {k: v for k, v in D.items() if not k.startswith('_')}
    J = jl(os.path.join(_DATA, 'jimun_7pan.json'))
    p7 = [z for z in J['지문'] if not z['id'].startswith('P8-')]
    p7u = {z['uid'] for z in p7}
    have = sum(1 for u in p7u if rows.get(u))
    hi = sum(1 for u in p7u if rows.get(u) and rows[u][0].get('c') == '높음')
    ref = jl(os.path.join(HERE, '_ref_book8_pos.json'))
    same = sum(1 for u, v in ref.items() if rows.get(u) and rows[u][0]['p'] == v['p8pdf'])
    bad = [u for u, v in rows.items() if any(not (1 <= c['p'] <= 805) or len(c['r']) != 4 or not all(0 <= x <= 2000 for x in c['r']) or c['how'] not in ('글', '명칭', '조각') for c in v)]
    book_text = [u for u, v in rows.items() if any(set(c) - {'p', 'r', 's', 'how', 'c'} for c in v)]
    T(G, '대응표 — 제7판 지문 %d(uid %d) 중 자리 있음 %d · 확신 높음 %d · 채팅 표 1등 쪽 같음 %d / %d · 8판 새 19 · 리담 34 · 줄 꼴(p · r 0~2000 · s · how · c) · 책 글 칸 0'
      % (len(p7), len(p7u), have, hi, same, len(ref)),
      have >= len(p7u) - 10 and not bad and not book_text and all(rows.get('T8N%04d' % k) for k in range(1, 20)) and meta.get('ref_same') == same,
      {'meta': meta.get('counts'), '꼴 어긋남': bad[:5], '책 글 칸': book_text[:5]})
    miss = [(z['id'], z['uid'], (z.get('판8') or {}).get('cat')) for z in p7 if not rows.get(z['uid'])]
    N(G, '대응표에 없는 제7판 지문 %d — 모두 p8up 「8판에 없음」이면 맞음' % len(miss), miss)
    T(G, '못 찾은 지문 = 전부 「8판에 없음」(p8up 판8.cat 없음)', all(c == '없음' for _, _, c in miss), miss)
    by = {}
    for z in J['지문']:
        by.setdefault(z['uid'], z)
    TQ = jl(os.path.join(_DATA, 'jimun_특허.json'))
    lid = {z['uid']: z for q in TQ['문제'] for z in q['지문'] if z.get('uid')}
    out = {}
    for u, i in SAMPLE:
        z = by.get(u) or lid.get(u)
        q = BM.norm(BM.strip_tags(BM.p7text(BM.stmt(z['t'])))) if z else ''
        r = (rows.get(u) or [None])[0]
        got = rect_text(r['p'], r['r']) if r else ''
        out[u] = {'id': i, '쪽': r and r['p'], '인쇄': r and r['p'] - 10, 'how': r and r['how'], 'c': r and r.get('c'), '자리 글 ⊇ 지문 글': bool(q) and q in got, '지문 길이': len(q), '자리 글 길이': len(got)}
    T(G, '표본 셋 — P7-0000-1(TJ0100001) · P7-0089(T2562011 · 12-유제) · T1552093(제140조 창) — 1등 자리 상자 안 글자층 ⊇ 지문 글', all(v['자리 글 ⊇ 지문 글'] for v in out.values()), out)
    # 채팅 표와 다른 까닭(1등 쪽 다름) — 갈래만
    P = BM.load_pages()
    cat = collections.Counter(); ex = collections.defaultdict(list)
    for u, v in ref.items():
        r = (rows.get(u) or [None])[0]
        if r and r['p'] == v['p8pdf']:
            continue
        z = by.get(u); t = BM.norm(BM.strip_tags(BM.p7text(BM.stmt(z['t'])))) if z else ''
        cp = v['p8pdf']
        if not r:
            c = '여기 못 찾음(8판에 없음)'
        elif cp in P and t and t in P[cp]['m']:
            c = '같은 글 두 자리 — 여기 = 번호 바로 뒤·발문 뒤·어림 쪽 쪽'
        elif cp > BM.BODY_END and r['p'] <= BM.BODY_END:
            c = '채팅 = 뒤 묶음 되풀이 · 여기 = 본문'
        elif cp in P and t[:24] and t[:24] in P[cp]['m']:
            c = '채팅 쪽엔 앞 24자만 같음(다른 지문) · 여기 = 통째'
        else:
            c = '채팅 쪽에 그 글 없음 · 여기 = %s' % r['how']
        cat[c] += 1; ex[c].append('%s %s→%s' % (v['id'], cp, r['p'] if r else None))
    N(G, '채팅 표(앞 24자)와 1등 쪽이 다른 %d — 까닭 갈래' % sum(cat.values()), {c: [n, ex[c][:6]] for c, n in cat.most_common()})


# ══════════ 앱 관문 ══════════
def open_box(q, k, how='mouse'):
    q.ev("()=>__B8.closeBox()")
    at = q.ev("k=>__B8.idAt(k)", k)
    q.press(at, how, 700)
    return at, q.ev("()=>__B8.boxReady()")


def g_a3(p, b, eng):
    """§B-3 앱 — ID 칩 → 「📚 교재 자리」 8판 줄 · 누름 → 쪽 창 · 칠한 자리 = 대응표 자리"""
    G = 'a3'
    D = jl(os.path.join(W8, '대응.json'))
    for u, i in SAMPLE:
        for how in (('mouse', 'touch') if u == SAMPLE[1][0] else ('mouse',)):
            via = open_card(p, u)
            at, bx = open_box(p, u, how)
            bx = p.ev("()=>__B8.snipReady()") or bx
            r0 = (D.get(u) or [None])[0]
            row = (bx or {}).get('rows', [None])[0] if (bx or {}).get('rows') else None
            ok1 = bool(at and at.get('on') and bx and row and r0) and not bx['next'] and row['k'] == '특허법 해례 8판' and row['p'] in ('%d쪽' % (r0['p'] - 10), 'p.%d' % (r0['p'] - 10)) \
                and ('PDF %d' % r0['p']) in row['m'] and any(m.startswith('확신 ') for m in row['m']) and 4 <= len(row['sn']) <= 41 and row['vis'] and bx['omrRows'][:1] == ['정리OMR']
            ra = p.ev("()=>__B8.rowAt(0)")
            p.press(ra, how, 900)
            bk = p.ev("()=>__B8.bookReady()")
            want = [x / 20 for x in r0['r']] if r0 else None
            hl = (bk or {}).get('hl')
            ok2 = bool(bk and bk.get('n') and bk.get('page') == r0['p'] and hl and hl['vis'] and want
                       and abs(hl['l'] - want[0]) < 0.2 and abs(hl['t'] - want[1]) < 0.2 and abs(hl['w'] - (want[2] - want[0])) < 0.2 and abs(hl['h'] - (want[3] - want[1])) < 0.2
                       and '특허법 해례 8판' in (bk.get('title') or '') and ('%d쪽' % (r0['p'] - 10)) in (bk.get('nav') or '') and not bk.get('err'))
            T(G, '%s %s(%s) %s · 카드 = ' % (eng, u, i, '마우스' if how == 'mouse' else '손가락') + ('단원 줄' if via == 'unit' else '🔍 검색 → 지문 팝업(마디에 안 붙은 지문)') + ' — ID 칩 → 「📚 교재 자리」: 정리OMR 줄 아래 「특허법 해례 8판 · %s쪽(revfix0928night 뒤 p.N) · PDF %s · 확신 %s」 + 둘째 줄 그 자리 글 · 「다음 판에서…」 0 → 줄 누름 → 교재 창 PDF %s · 칠한 자리 = 대응표 r(±0.2%%)'
              % (r0 and r0['p'] - 10, r0 and r0['p'], r0 and r0.get('c'), r0 and r0['p']),
              ok1 and ok2, {'칩': at, '창': bx, '쪽 창': bk, '대응 r%': want})
    go_key(b, SAMPLE[1][0])
    at, bb = open_box(b, SAMPLE[1][0])
    T(G + '-헛', '%s 헛잣대 바탕 — 「📚 교재 자리」에 8판 줄 없음 · 「다음 판에서…」 글 있음' % eng, bool(bb) and not bb.get('p8u') and bb.get('next'), bb)
    p.ev("()=>__B8.closeAll()")


def g_a4(p, b, eng, br):
    """§B-4 직접 찍기 — 저장 · 새로고침 뒤 유지 · 대응표보다 먼저 · 되돌리기 · 다른 기기(동기화)"""
    G = 'a4'
    u = SAMPLE[1][0]
    go_key(p, u)
    open_box(p, u)
    pk = p.ev("()=>__B8.btnAt('자리 직접 찍기')")
    p.click(pk, 900)
    bk = p.ev("()=>__B8.bookReady()")
    pg = p.ev("()=>__B8.bookAt('pg')")
    F = [0.20, 0.30, 0.62, 0.36]
    kind = p.drag(pg['x'] + pg['w'] * F[0], pg['y'] + pg['h'] * F[1], pg['x'] + pg['w'] * F[2], pg['y'] + pg['h'] * F[3]) if pg else None
    p.pg.wait_for_timeout(400)
    bk2 = p.ev("()=>__B8.book()")
    sv = p.ev("()=>__B8.bookAt('sv')")
    p.click(sv, 900)
    pin = p.ev("u=>__B8.pin(u)", u)
    ok = bool(bk and bk.get('ov') and bk.get('pkOn') and bk2 and bk2.get('box') and '이 자리 저장' in (bk2.get('sv') or '') and pin and pin.get('by') == 'hand'
              and pin.get('b') == 'patent_hr8' and all(abs(a - c) < 0.006 for a, c in zip(pin.get('r') or [], F)))
    T(G, '%s 「📍 자리 직접 찍기」 → 교재 창 찍기 켬(덮개) · 끌기(%s) → 「이 자리 저장 · p.N」 → 기록 jopangi.canvasjari 칸 p8|%s = {by:hand · b:patent_hr8 · r = 끈 자리 ±0.6%%}' % (eng, kind, u), ok,
      {'창': {k: (bk or {}).get(k) for k in ('page', 'ov', 'pkOn')}, '상자': (bk2 or {}).get('box'), '저장 단추': (bk2 or {}).get('sv'), '칸': pin})
    bx = p.ev("()=>__B8.picReady()")
    T(G, '%s 저장 뒤 「📚 교재 자리」 창 — 첫 줄 = 「찍어 둔 자리」(대응표 줄 대신) + 그림 + 「자동으로 되돌리기」' % eng,
      bool(bx) and bx['rows'][:1] and '찍어 둔 자리' in bx['rows'][0]['m'] and bx['rows'][0]['pdf'] == pin.get('p') and bx['pic'] and any('자동으로 되돌리기' in x['t'] for x in bx['btns']) and len(bx['rows']) == 1,
      bx)
    # 다른 기기 — 이 기기 기록을 원격으로 올리고(가짜 원격 · SEED) 새 기기가 받아 같은 자리
    p.ev("()=>syncRecords(true)")
    p.pg.wait_for_timeout(1500)
    remote = p.ev("()=>window.__REMOTE&&window.__REMOTE.text")
    p.pg.goto('http://127.0.0.1:%d/index.html?tok=1&keep=1' % p.port, wait_until='load', timeout=180000)
    p.pg.wait_for_function(M.READY, timeout=180000); p.pg.wait_for_timeout(900)
    go_key(p, u)
    _, bx2 = open_box(p, u)
    T(G, '%s 새로고침 뒤 — 찍어 둔 자리 그대로 첫 줄(대응표보다 먼저)' % eng, bool(bx2) and bx2['rows'][:1] and '찍어 둔 자리' in bx2['rows'][0]['m'], bx2)
    ns, nd, ne = M.new_env()
    q = None
    try:
        q = Pg(br, eng, 'b8R', ns, nd, ne, remote=remote)
        q.until("()=>typeof syncRecords==='function'", ms=5000)
        q.ev("()=>syncRecords(true)"); q.pg.wait_for_timeout(1500)
        go_key(q, u)
        _, bx3 = open_box(q, u)
        pin3 = q.ev("u=>__B8.pin(u)", u)
        T(G, '%s 다른 기기(가짜 원격으로 받음) — 같은 칸 p8|%s · 「📚 교재 자리」 첫 줄 = 찍어 둔 자리 · 쪽 같음' % (eng, u),
          bool(remote) and bool(pin3) and pin3.get('r') == pin.get('r') and bool(bx3) and bx3['rows'][:1] and '찍어 둔 자리' in bx3['rows'][0]['m'], {'원격': bool(remote), '칸': pin3, '창': bx3})
    finally:
        if q:
            q.close()
    rv = p.ev("()=>__B8.btnAt('자동으로 되돌리기')")
    p.click(rv, 900)
    bx4 = p.ev("()=>__B8.snipReady()")
    pin4 = p.ev("u=>__B8.pin(u)", u)
    T(G, '%s 「자동으로 되돌리기」 → 칸 {auto:true}(안 지움) · 첫 줄 = 대응표 1등(확신 글자)' % eng,
      bool(pin4) and pin4.get('auto') is True and bool(bx4) and bx4['rows'][:1] and any(m.startswith('확신') for m in bx4['rows'][0]['m']), {'칸': pin4, '창': bx4})
    # 캔버스 「교재 확정 N 고아」 셈에 안 든다(p8 칸은 블록이 아니다) — 정리캔버스 = 민소 법 · 정리 탭에서만 선다 · 헛잣대 = 바탕 앱은 같은 칸을 고아로 센다
    def orph_of(q):
        q.ev("u=>{const A=JSON.parse(localStorage.getItem('jopangi.canvasjari')||'{}');A['p8|'+u]={by:'hand',b:'patent_hr8',p:33,r:[0.1,0.1,0.2,0.2],t:Date.now()};localStorage.setItem('jopangi.canvasjari',JSON.stringify(A));try{recDropCache();}catch(e){}}", u)
        o = q.ev("async()=>{try{closeAllPops();}catch(e){}S.law='민사소송법';S.tab='omr';await render();for(let i=0;i<300&&!document.getElementById('cvJariOrph');i++)await new Promise(r=>setTimeout(r,100));"
                 "await new Promise(r=>setTimeout(r,1200));return __B8.orphBadge();}")
        q.ev("()=>{S.law='특허법';S.tab='jimun';S.jimunTab='ox';return render();}")
        q.pg.wait_for_timeout(800)
        return o
    orph, orphb = orph_of(p), orph_of(b)
    T(G, '%s 민소 정리 탭 캔버스 머리 「교재 확정 N 고아」 — 1차객 8판 칸(p8|uid)은 세지 않음(배지 숨음)' % eng, bool(orph) and not orph.get('vis'), orph)
    T(G + '-헛', '%s 헛잣대 바탕 — 같은 칸을 「교재 확정 1 고아」로 센다' % eng, bool(orphb) and orphb.get('vis') and '고아' in (orphb.get('t') or ''), orphb)


def g_a5(p, b, eng):
    """§B-5 캐시 — 두 번째 열 때 bookpdf:patent_hr8(네트워크 0) · 민법앱과 같은 DB·열쇠"""
    G = 'a5'
    u = SAMPLE[2][0]
    tag = 'p8N_' + eng

    def reload():
        p.pg.goto('http://127.0.0.1:%d/index.html?tok=1&keep=1' % p.port, wait_until='load', timeout=180000)
        p.pg.wait_for_function(M.READY, timeout=180000); p.pg.wait_for_timeout(900)
    p.ev("()=>__B8.idbDel('bookpdf:patent_hr8')")   # 앞 묶음이 이미 재워 두었다 — 비우고 새로 연다
    reload()
    go_key(p, u)
    open_box(p, u)
    n0 = BOOKREQ[tag + '|pdf']
    p.click(p.ev("()=>__B8.rowAt(0)"), 900)
    bk = p.ev("()=>__B8.bookReady()")
    n1 = BOOKREQ[tag + '|pdf']
    st1 = p.ev("()=>__B8.stat()")
    idb = None
    for _ in range(60):
        idb = p.ev("()=>__B8.idb('bookpdf:patent_hr8')")
        if idb and idb.get('has'):
            break
        p.pg.wait_for_timeout(500)
    reload()
    go_key(p, u)
    open_box(p, u)
    n2 = BOOKREQ[tag + '|pdf']
    p.click(p.ev("()=>__B8.rowAt(0)"), 900)
    bk2 = p.ev("()=>__B8.bookReady()")
    n3 = BOOKREQ[tag + '|pdf']
    st2 = p.ev("()=>__B8.stat()")
    T(G, '%s 첫 열기 = 저장소에서 받음(PDF 요청 %d) → IndexedDB ox_master_db/rows 「bookpdf:patent_hr8」(pdfMd5 = 책메타) → 새로고침 뒤 두 번째 열기 = 이 기기에 재운 것(PDF 요청 0 · stat.from cache)' % (eng, n1 - n0),
      n1 - n0 >= 1 and (st1 or {}).get('from') == 'net' and bool(idb) and idb.get('has') and idb.get('md5') == '94f115f0a0e2d4387278e600e12fb753' and n3 - n2 == 0 and (st2 or {}).get('from') == 'cache' and (bk2 or {}).get('cvsW', 0) > 0,
      {'요청': [n1 - n0, n3 - n2], 'stat': [st1, st2], 'idb': idb, '첫 창': {k: (bk or {}).get(k) for k in ('page', 'cvsW', 'err')}})
    mb = io.open(os.path.join(M.GENIE, 'minbeop', 'index.html'), encoding='utf-8').read()
    T(G, '민법앱과 같은 열쇠 — 민법앱 코드도 IndexedDB 「ox_master_db」 · 칸 「rows」 · 열쇠 「bookpdf:」 + docid(같은 출처 github.io)',
      "indexedDB.open('ox_master_db'" in mb.replace('"', "'") and "'bookpdf:'" in mb.replace('"', "'"), '')


BR = {}
PARTS = [('a3', g_a3), ('a4', g_a4), ('a5', g_a5)]
DPARTS = [('d1', d_b1), ('d2', d_b2)]


def run_engine(pw, eng):
    br = getattr(pw, eng).launch()
    BR[eng] = br
    ns, nd, ne = M.new_env()
    bs, bd, be = M.base_env()
    try:
        p = Pg(br, eng, 'p8N', ns, nd, ne)
        b = Pg(br, eng, 'p8B', bs, bd, be)
        try:
            for k, fn in PARTS:
                if ONLY and k not in ONLY:
                    continue
                print('── %s · %s' % (eng, k), flush=True)
                try:
                    fn(p, b, eng, br) if k == 'a4' else fn(p, b, eng)
                except Exception as e:
                    T('RUN', u'%s · %s 묶음이 멈춤' % (eng, k), False, repr(e)[:600])
            T('ERR', u'%s — NEW 앱 오류 0' % eng, not p.errs_all(), p.errs_all()[:6])
        finally:
            p.close(); b.close()
    finally:
        br.close()


def main():
    shutil.rmtree(os.path.join(M.WORK, 'head'), ignore_errors=True)
    os.makedirs(M.WORK, exist_ok=True)
    t0 = time.time()
    for k, fn in DPARTS:
        if not ONLY or k in ONLY:
            try:
                fn()
            except Exception as e:
                T('RUN', u'%s 데이터 묶음이 멈춤' % k, False, repr(e)[:600])
    if not ONLY or any(k in ONLY for k, _ in PARTS):
        with sync_playwright() as pw:
            for eng in ENGS:
                RES.append(('ENG', eng, None, ''))
                run_engine(pw, eng)
    npass = sum(1 for r in RES if r[2] is True); nfail = sum(1 for r in RES if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · %s · NEW %s · 데이터 %s · 바탕 HEAD %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), 'book8', os.path.basename(_NEW), _DATA,
                M.git('rev-parse', '--short', 'HEAD').decode().strip(), ','.join(ENGS)))
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[ok], g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:900]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
