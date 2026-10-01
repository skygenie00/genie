# -*- coding: utf-8 -*-
r"""_task_jo_theme §B 관문 — 조문 「테마」(서랍 테마 줄·거름 점 · 테마 창 · 목록 창 · 조문 「테마 N」 · 고치기 · 동기화 · 검색) · 팝업 틀 · 8판 교재 창 검색 · 화면 훑기

  python _harness_jo_theme.py [--new <앱>] [--base <앱 파일 | genie git 판>] [--prev <판>] [--vendor <pdf.js 3.11.174 폴더>] [--eng chromium,webkit] [--only B1,..,B24,WK] [--res <결과>] [--yardstick [--yard-app <판>]]

  fix1(_task_jo_theme_fix1 · 8d1383d 위 고침 여덟) = B15~B24 — B15 테마 글 조 링크 꼴 · B16 다른 법 머리 · B17 연결 창·원문 창 틀 · B18 폰 서랍 머리 한 줄 ·
    B19 창 테마 줄 = 서랍 줄 · B20 거름 점 8px · B21 두문자 이름·여러 조 길 · B22 테마 모드 범례 없음 · B23 본판 B1~B14 다시 · B24 화면 훑기(+ 🔗 연결 창 · 원문 창 셋 · 찾기 결과)
    PREV = 8d1383d(본판 · 「안쪽 = 8d1383d」 · 「PC 무변」) · 헛잣대 = --yardstick --yard-app 8d1383d --only B15,..,B22

  NEW  = 이 판 앱(기본 genie jo/index.html) · BASE = 착수 HEAD(기본 genie git 판 cedc251) — --yardstick 이면 BASE 를 NEW 자리에 넣어 B1~B12 가 저마다 FAIL 해야 통과
    (B13 회귀 · B14 화면 훑기 = 새 판 흠 − 바탕 흠이라 헛잣대 해당 없음)
  B-0 합성 재료(D11 — 실제 정리omr 글 0 · 임의 글 속에 조 인용·주체 낱말·두문자를 심는다) = 실행 중에 만든다:
    theme/patent_hr8/테마.json.gz(테마 셋 = 주체능력 · 기일기간 · 분변분재 기간(region · svg)) · words/patent_hr8/글.json.gz(805쪽 · 55 · 776 에 「보정을무효로」) ·
    책메타(합성 pdfMd5) · 빈 pdf 805쪽 — 나머지 minbeoppdf(쪽 words · 다른 교재)는 로컬 클론 읽기만(심볼릭 링크 덧판)
  기록 = 가짜 원격(studyplandata jopangi/기록.json · /__rec/ · 메모리 · 밖으로 안 나감) — 두 기기 흉내 = 문맥 둘이 같은 원격을 나눠 쓴다
  도구 = 같은 폴더 _harness_jo_revfix0929b(서버 · SEED(pdf.js shim · minbeoppdf 길) · __RB 도구 · 기기 흉내 · 터치 · 길게 누르기 · 누름 영역 더듬기)를 불러 쓴다 + 이 판 도구 __TM
  자리 = _roots(GENIE_ROOT · MBPDF_ROOT) — 클라우드: GENIE_ROOT=/home/user/genie MBPDF_ROOT=/home/user/minbeoppdf
  WebKit = 터치 칸(B1 · B6)만 · 이 컴퓨터에 WebKit 이 없으면 「안 잼」
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import base64, gzip, hashlib, io, json, os, re, shutil, sys, tempfile, threading, time, subprocess, urllib.parse   # noqa: E402
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEW = ARG('--new', _roots.genie('jo', 'index.html'))
BASE = ARG('--base', 'cedc251')
PREV = ARG('--prev', '8d1383d')   # fix1 — 본판 커밋(「안쪽 = 8d1383d」 · 「PC 무변」 잣대)
YARD = '--yardstick' in sys.argv
YAPP = ARG('--yard-app', BASE)    # 헛잣대 앱 — 본판 B1~B12 = cedc251 · fix1 B15~B22 = 8d1383d(--yard-app 8d1383d)
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_theme_result.txt'))
MBREAL = ARG('--mbpdf', _roots.mbpdf())
TMP0 = os.path.join(tempfile.gettempdir(), 'h_jotheme')
TMP = os.path.join(TMP0, 'p%d' % os.getpid())   # 덧판 = 돌 때마다 제 자리(두 판 같이 돌려도 서로 안 지움) · 끝나면 지움 · 회귀 로그만 TMP0/reg 에 남긴다
# 도구 하네스(revfix0929b)는 제 인자를 sys.argv 에서 읽는다 — 앱 자리를 넘겨 둔다(BASE 는 이 하네스가 따로 쓴다)
_argv = sys.argv
sys.argv = [sys.argv[0], '--new', NEW] + [x for k in ('--data', '--exam', '--mbpdf', '--vendor') if k in _argv for x in (k, _argv[_argv.index(k) + 1])]
sys.path.insert(0, HERE)
import _harness_jo_revfix0929b as H   # noqa: E402
sys.argv = _argv
T, N, RES = H.T, H.N, H.RES
PC, PC2, PHONE, PAD = H.PC, H.PC2, H.PHONE, H.PAD


def git(*a):
    return subprocess.run(['git', '-C', _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


app_src = H.app_src

# ════════════════════════ B-0 합성 재료 ════════════════════════
SUBJ = ['특허청장', '심사관', '출원인', '특허권자', '대리인', '전용실시권자', '통상실시권자', '법원']   # 여덟 · 「심판」 「기일」 「분변」 은 제 테마 밖 글에 없다(찾기 칸 값이 갈린다)
C_BK, C_RD, C_BL, C_OR, C_PU, C_PK = '#000000', '#d40000', '#0000ff', '#ff6100', '#6300a6', '#d40085'


def L(ind, *runs):
    return {'ind': ind, 'runs': [{'t': t, 'c': c} for t, c in runs]}


SVG3 = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 160">'
        '<text x="10" y="24" font-size="15" fill="#000000">{분변 분재 기간}</text>'
        '<text x="10" y="54" font-size="13" fill="#d40000">분변 분재 = 52조 · 53조 · 52-2 · 67-2</text>'
        '<text x="10" y="84" font-size="13" fill="#0000ff">출원인은 서른 날 안에 낸다</text>'
        '<path d="M10 100 L200 100" stroke="#d40000" fill="none" stroke-width="2"/>'
        '<path d="M10 120 Q100 150 200 120" stroke="#0000ff" fill="none"/>'
        '<path d="M220 40 L400 140" stroke="#ff6100" fill="none"/></svg>')
# fix1 B-0 보탬 — 다른 법 머리 가르기 줄(임의 글 · 실제 정리omr 글 아님) · 분변분재 기간 글·SVG 에 「분변분재」 없음(이름 · 여러 조 길로만 붙는다)
A32_LINE = '제5조및시규11조에따라 · 준용민소16조 · 법원은상33조를 · 이상5조 · (상227조)(디217조) · 특226조 · 시규11조'
A32_WANT = [['5조', '특허법', '제5조'], ['민소16조', '민사소송법', '제16조'], ['상227조', '상표법', '제227조'], ['디217조', '디자인보호법', '제217조'], ['226조', '특허법', '제226조']]
BOXES = {
    'b1': {'p': 1, 'r': [0.05, 0.08, 0.46, 0.34], 'svg': None, 'lines': [
        L(0, ('{주체능력}', C_BK)),
        L(1, ('가) 특허청장은 3조 및 4조의 절차를 밟는다', C_BK)),
        L(1, ('나) 심사관 5조 · 7-2 는 ', C_RD), ('출원인에게 알린다(11조)', C_BL)),
        L(2, ('다) 특허권자와 대리인은 13조 16조 25조를 본다', C_OR)),
        L(2, ('라) 46조 62조 (133③) 206조 — 전용실시권자·통상실시권자', C_PU)),
        L(1, (A32_LINE, C_BK))]},
    'b2': {'p': 2, 'r': [0.52, 0.08, 0.95, 0.40], 'svg': None, 'lines': [
        L(0, ('{기일기간}', C_BK)),
        L(1, ('정사소2만1 → 16조 · ', C_RD), ('책사소2만1 → 17조', C_BL)),
        L(1, ('3조 14조 15조 기간은 법원이 정한다', C_BK)),
        L(2, ('46조 63조 147조 · 186조 190조 224-2', C_PK)),
        L(2, ('민소 16조 준용 · 시규 3조 는 링크 없음', C_PU))]},
    'b3': {'p': 3, 'r': [0.10, 0.20, 0.60, 0.50], 'svg': SVG3, 'lines': []},
}
THEMES = [
    {'id': 't01', 'n': '주체능력', 'boxes': ['b1'], 'region': None, 'jo': ['3', '4', '5', '7-2', '11', '13', '16', '25', '46', '62', '133③', '206'], 'bk': [1, 1, 0]},
    {'id': 't02', 'n': '기일기간', 'boxes': ['b2'], 'region': None, 'jo': ['3', '14', '15', '16', '17', '46', '63', '147', '186', '190', '224-2'], 'bk': [1, 1, 1]},
    {'id': 't03', 'n': '분변분재 기간', 'boxes': ['b3'], 'region': {'p': 3, 'r': [0.10, 0.20, 0.60, 0.50]}, 'jo': ['52', '53', '52-2', '67-2'], 'bk': [0, 0, 1]},
]
ACR = {'정사소2만1': {'m': '합성 뜻 하나', 'jo': ['16']}, '책사소2만1': {'m': '', 'jo': ['17']}, '분변분재': {'m': '합성 뜻 넷', 'jo': ['52', '53', '52-2', '67-2']},
       '출심삼1사': {'m': '합성 뜻 다섯', 'jo': ['3', '14', '300']}}   # fix1 — 여러 조 두문자인데 조 하나(300)가 어느 테마에도 없음 → 안 붙어야
PLANT = {'t01': {'lines': 6, 'links': 17, 'subj': 8, 'acr': 0}, 't02': {'lines': 5, 'links': 12, 'subj': 1, 'acr': 2}, 't03': {'svgtext': 3, 'path': 3, 'links': 4, 'acr': 1}}
Q_BOOK = '보정을무효로'


def blank_pdf(path, n=805):
    from pypdf import PdfWriter
    w = PdfWriter()
    for _ in range(n):
        w.add_blank_page(595, 841)
    with open(path, 'wb') as f:
        w.write(f)


def _ln(src, dst):
    """★ 로컬 윈도(10/2) — 심볼릭 링크 권한이 없으면(WinError 1314) 폴더 = 정션 · 파일 = 하드 링크(같은 볼륨) → 안 되면 복사 · 읽기만"""
    try:
        os.symlink(src, dst)
        return
    except OSError:
        if os.name != 'nt':
            raise
    if os.path.isdir(src):
        import _winapi
        _winapi.CreateJunction(src, dst)
        return
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def build_overlay():
    """덧판 둘 — full(합성 재료 다) · none(테마·쪽 글 없음 = 404) · 나머지는 로컬 클론을 링크(읽기만)"""
    os.makedirs(TMP, exist_ok=True)
    pdf = os.path.join(TMP, 'blank805.pdf')
    if not os.path.isfile(pdf):
        blank_pdf(pdf)
    md5 = hashlib.md5(open(pdf, 'rb').read()).hexdigest()
    real_meta = json.load(open(os.path.join(MBREAL, 'words', 'patent_hr8', '책메타.json'), encoding='utf-8'))
    meta = dict(real_meta, pdfMd5=md5, file='patent_hr8.pdf', builtBy='_harness_jo_theme(합성)')
    theme = {'pdfMd5': 'harness-omr', 'boxes': BOXES, 'themes': THEMES, 'acr': ACR, 'subj': SUBJ}
    pages = []
    for i in range(1, 806):
        t = '합성쪽%d\n가나다라마바사\n아자차카타파하%d' % (i, i)
        if i == 55:
            t = '합성쪽55\n앞글' + Q_BOOK + '뒤글\n가운데\n다시' + Q_BOOK + '끝'
        if i == 776:
            t = '합성쪽776\n여기' + Q_BOOK + '한곳'
        pages.append(t)
    text = {'docid': 'patent_hr8', 'pdfMd5': md5, 'pages': 805, 't': pages}
    out = {}
    for var in ('full', 'none'):
        d = os.path.join(TMP, 'mbp_' + var)
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        for x in os.listdir(MBREAL):
            if x in ('words', 'pdf', 'theme') or x.startswith('.'):
                continue
            _ln(os.path.join(MBREAL, x), os.path.join(d, x))
        os.makedirs(os.path.join(d, 'words'))
        for x in os.listdir(os.path.join(MBREAL, 'words')):
            if x != 'patent_hr8':
                _ln(os.path.join(MBREAL, 'words', x), os.path.join(d, 'words', x))
        w8 = os.path.join(d, 'words', 'patent_hr8')
        os.makedirs(w8)
        for x in os.listdir(os.path.join(MBREAL, 'words', 'patent_hr8')):
            if x not in ('책메타.json', '글.json.gz'):
                _ln(os.path.join(MBREAL, 'words', 'patent_hr8', x), os.path.join(w8, x))
        json.dump(meta, open(os.path.join(w8, '책메타.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        os.makedirs(os.path.join(d, 'pdf'))
        for x in os.listdir(os.path.join(MBREAL, 'pdf')):
            if x != 'patent_hr8.pdf':
                _ln(os.path.join(MBREAL, 'pdf', x), os.path.join(d, 'pdf', x))
        _ln(pdf, os.path.join(d, 'pdf', 'patent_hr8.pdf'))
        if var == 'full':
            with gzip.open(os.path.join(w8, '글.json.gz'), 'wt', encoding='utf-8') as f:
                json.dump(text, f, ensure_ascii=False)
            os.makedirs(os.path.join(d, 'theme', 'patent_hr8'))
            with gzip.open(os.path.join(d, 'theme', 'patent_hr8', '테마.json.gz'), 'wt', encoding='utf-8') as f:
                json.dump(theme, f, ensure_ascii=False)
        out[var] = d
    return out, md5


OVER, PDFMD5 = build_overlay()

# ════════════════════════ 가짜 원격(기록) ════════════════════════
class Remote:
    def __init__(self):
        self.files, self.lock, self.puts = {}, threading.Lock(), 0

    def clear(self):
        with self.lock:
            self.files.clear()
            self.puts = 0

    def rec(self):
        b = self.files.get('jopangi/기록.json')
        return json.loads(b.decode('utf-8')) if b else None


REMOTE = Remote()
SEED_REC = r"""
 var sp=s.indexOf('api.github.com/repos/zzikkaplan/studyplandata/contents/');
 if(sp>=0){var rest2=s.slice(sp+'api.github.com/repos/zzikkaplan/studyplandata/contents/'.length).split('?')[0];
  var h2={};try{var hh=o.headers;var ac=hh&&(typeof hh.get==='function'?hh.get('Accept'):(hh.Accept||hh.accept));if(ac)h2['Accept']=ac;}catch(e){}
  if(o.body)h2['Content-Type']='application/json';
  return nf(location.origin+'/__rec/'+rest2,{method:o.method||'GET',headers:h2,body:o.body});}
"""
_anchor = " if(/cdnjs\\.cloudflare\\.com"
if SEED_REC not in H.SEED:
    assert _anchor in H.SEED, 'revfix0929b SEED 모양이 바뀌었다'
    H.SEED = H.SEED.replace(_anchor, SEED_REC + _anchor, 1)
SERVERS = {}


def serve_theme(tag, src):
    """tag 마다 서버 하나 · 앱 = 메모리(SEED + 도구) · /__book/ = 덧판(tag 가 'none:' 으로 시작하면 재료 없는 덧판) · /__rec/ = 가짜 원격"""
    if tag in SERVERS:
        return SERVERS[tag][1]
    body = H.inject(src).encode('utf-8')
    mb = OVER['none'] if tag.startswith('none:') else OVER['full']

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
            if p.startswith('/__rec/'):
                k = p[len('/__rec/'):]
                with REMOTE.lock:
                    b = REMOTE.files.get(k)
                if b is None:
                    return self._send(404, b'{"message":"Not Found"}')
                if 'raw' in (self.headers.get('Accept') or ''):
                    return self._send(200, b, 'application/octet-stream')
                return self._send(200, json.dumps({'sha': hashlib.sha1(b).hexdigest(), 'size': len(b)}).encode())
            return super().do_GET()

        def do_PUT(self):
            p = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
            if not p.startswith('/__rec/'):
                return self._send(405, b'{}')
            k = p[len('/__rec/'):]
            n = int(self.headers.get('Content-Length') or 0)
            try:
                j = json.loads(self.rfile.read(n).decode('utf-8') or '{}')
                data = base64.b64decode(j.get('content', ''))
            except Exception:
                return self._send(422, b'{}')
            with REMOTE.lock:
                cur = REMOTE.files.get(k)
                if cur is not None and j.get('sha') and j.get('sha') != hashlib.sha1(cur).hexdigest():
                    return self._send(409, b'{"message":"conflict"}')
                REMOTE.files[k] = data
                REMOTE.puts += 1
            return self._send(200, json.dumps({'content': {'sha': hashlib.sha1(data).hexdigest()}}).encode())

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
            for pre, root in (('/jo/data/', H.DATA), ('/gichul/pdf/', H.EXAM), ('/__book/', mb)):
                if p.startswith(pre):
                    return os.path.join(root, *[x for x in p[len(pre):].split('/') if x])
            if p.startswith('/__vendor/'):
                parts = [x for x in p[len('/__vendor/'):].split('/') if x]
                f = os.path.join(H.VENDOR, *parts)
                return f if os.path.exists(f) else os.path.join(H.VENDOR, 'build', *parts)
            return os.path.join(HERE, '__없음__')

    srv = ThreadingHTTPServer(('127.0.0.1', 0), Hd)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


H.serve = serve_theme   # 도구 하네스의 Pg 가 이 서버를 쓴다(덧판 · 가짜 원격)

# ════════════════════════ 이 판 도구 __TM ════════════════════════
TM_TOOLS = r"""<script>
(function(){
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const vis = e => !!e && e.isConnected && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden' && e.getBoundingClientRect().height > 0;
const wait = ms => new Promise(r => setTimeout(r, ms));
const skel = e => { const c = e.cloneNode(true); c.querySelectorAll('*').forEach(n => { [...n.childNodes].forEach(t => { if (t.nodeType === 3) t.remove(); }); n.removeAttribute('style'); n.removeAttribute('title'); n.removeAttribute('data-tm'); }); [...c.childNodes].forEach(t => { if (t.nodeType === 3) t.remove(); }); c.removeAttribute('style'); c.removeAttribute('data-tm'); return c.outerHTML; };
const hex = c => { const m = /rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(c || ''); return m ? '#' + [m[1], m[2], m[3]].map(x => (+x).toString(16).padStart(2, '0')).join('') : c; };
window.__TM = {
  txt, vis, skel, hex, wait,
  ready: async () => { for (let i = 0; i < 400; i++){ if (typeof TM !== 'undefined' && TM.st !== 'wait') return TM.st; await wait(50); } return 'timeout'; },
  pop: pre => (typeof POPS !== 'undefined' ? POPS : []).filter(x => (x._pk || '') === pre || (x._pk || '').indexOf(pre) === 0).pop() || null,
  treeSkel(){ const t = document.querySelector('#slot .tree'); if (!t) return null; const c = t.cloneNode(true); c.querySelectorAll('.tmtg,.tmdot').forEach(n => n.remove()); return c.outerHTML; },
  rows(){ return [...document.querySelectorAll('#slot .tree .r.tmr')].map(r => ({ id: r.dataset.tm, t: txt(r.querySelector('.jno')), d2: txt(r.querySelector('.tmd2')), s: txt(r.querySelector('.tms')), cls: r.className,
    dots: [...r.querySelectorAll('.bkm3 .bkmk')].map(d => hex(getComputedStyle(d).backgroundColor)), h: Math.round(r.getBoundingClientRect().height) })); },
  joRows(){ return [...document.querySelectorAll('#slot .tree .r[data-jo]')].length; },
  dot(){ const d = document.querySelector('.jtbar .tmdot'); return d ? { bg: hex(getComputedStyle(d).backgroundColor), bd: hex(getComputedStyle(d).borderTopColor), chip: txt(document.querySelector('.jtbar .jckf')) } : null; },
  deco(e){ if (!e) return null; const c = getComputedStyle(e); return { line: c.textDecorationLine, style: c.textDecorationStyle, dcol: c.textDecorationColor, th: c.textDecorationThickness, off: c.textUnderlineOffset, cur: c.cursor, col: c.color }; },
  frame(w){ if (!w) return null; const c = getComputedStyle(w), ph = w.querySelector(':scope > .ph'), h = getComputedStyle(ph), t = ph.querySelector('.cftt') || ph.querySelector('.pt'), tc = getComputedStyle(t),
      xb = ph.querySelector(':scope > button.cfx') || ph.querySelector(':scope > button:not(.pall)'), xc = getComputedStyle(xb), bd = w.querySelector(':scope > .pb'), r = w.getBoundingClientRect();
    return { bg: c.backgroundColor, bd: c.borderTopColor, bw: c.borderTopWidth, rad: c.borderTopLeftRadius, sh: c.boxShadow, hbg: h.backgroundColor, hbd: h.borderBottomColor, hbw: h.borderBottomWidth,
      ts: tc.fontSize, tw: tc.fontWeight, tc: tc.color, xc: xc.color, xbd: xc.borderTopColor, xbw: xc.borderTopWidth, xr: xc.borderTopLeftRadius, xbg: xc.backgroundColor,
      inner: { hpad: h.padding, hcur: h.cursor, bbg: bd ? getComputedStyle(bd).backgroundColor : null, bpad: bd ? getComputedStyle(bd).padding : null, w: Math.round(r.width), rsz: !!w.querySelector(':scope > .prsz'), font: c.fontSize + ' ' + c.fontFamily.slice(0, 20) } }; },
  subjOn(){ return [...document.querySelectorAll('#slot .tree .r[data-jo] .bkm3')].filter(b => { const d = b.querySelectorAll('.bkmk')[1]; return d && !!d.style.background; }).length; },
  sweep(sel, touch){ const out = []; const sig = e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '.' + String(e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className).split(' ').filter(x => x && !/^(on|cur|hid|z|sel|fold|tmlp|tmon)$/.test(x)).slice(0, 2).join('.') + ':' + txt(e).replace(/\d+/g, '#').slice(0, 14));
    const se = document.scrollingElement; if (se.scrollWidth > innerWidth + 1) out.push('page-hscroll');
    const roots = [...document.querySelectorAll(sel)].filter(vis); if (!roots.length) return ['(뿌리 없음) ' + sel];
    const all = []; roots.forEach(r => { all.push(r); r.querySelectorAll('*').forEach(e => all.push(e)); });
    const V = [...new Set(all)].filter(e => e.getClientRects().length && vis(e)).slice(0, 6000);
    V.forEach(e => { const cs = getComputedStyle(e), ox = cs.overflowX;
      if ((ox === 'auto' || ox === 'scroll') && e.scrollWidth > e.clientWidth + 1 && e.clientWidth > 0) out.push('hscroll:' + sig(e));
      if ((ox === 'hidden' || ox === 'clip') && e.scrollWidth > e.clientWidth + 1 && e.clientWidth > 0 && cs.textOverflow !== 'ellipsis' && e.children.length === 0 && txt(e)) out.push('clip:' + sig(e));
      const r = e.getBoundingClientRect(); if (r.width > 0 && (r.right > innerWidth + 1 || r.left < -1) && cs.position !== 'fixed' && !e.closest('.pop') && getComputedStyle(e.parentElement || e).overflowX === 'visible') out.push('offscreen:' + sig(e)); });
    const ACT = 'button, a[href], [role=button], .wmlk, .jno, input, select, textarea, .tmds, .thac, .throw2, .tmadd .jtt, .tmaddr, .cv-bssn, .cv-bsone';
    /* 작은 누름에서 빼는 것 — 글 줄 안 링크(.wmlk · 글 속 두문자 = 바탕 조문 글 링크와 같은 꼴) · 테마 줄 이름(누름 = 줄 전체 · 줄 ≥ 36) · 지시서가 크기를 정한 것(검색 input 28 · 찾기 input 30 · 팝업 머리 단추 = A-7 틀) */
    const NOSMALL = '.wmlk, .thl .thac, .thfig *, .tmr .jno, input, .pop > .ph > button';
    const A = V.filter(e => e.matches(ACT) && !e.disabled && getComputedStyle(e).pointerEvents !== 'none');
    const fl = e => { for (let q = e; q && q !== document.body; q = q.parentElement){ const ps = getComputedStyle(q).position; if (ps === 'fixed' || ps === 'sticky') return !roots.some(r => r === q || q.contains(r)); } return false; };
    const AS = A.filter(e => !fl(e));
    for (let i = 0; i < AS.length; i++) for (let j = i + 1; j < AS.length; j++){ const a = AS[i], b = AS[j]; if (a.contains(b) || b.contains(a)) continue;
      const p = a.getBoundingClientRect(), q = b.getBoundingClientRect(), ix = Math.min(p.right, q.right) - Math.max(p.left, q.left), iy = Math.min(p.bottom, q.bottom) - Math.max(p.top, q.top);
      if (ix > 2 && iy > 2) out.push('overlap:' + sig(a) + '|' + sig(b)); }
    if (touch) A.filter(e => !e.matches(NOSMALL)).slice(0, 300).forEach(e => { if (!fl(e)) try { e.scrollIntoView({ block: 'center', inline: 'nearest' }); } catch (x) {} const h = __RB.hitBox(e), r = e.getBoundingClientRect();
      if (h.on && ((Math.round(r.height) < 36 && h.h < 36) || (Math.round(r.width) < 36 && h.w < 36))) out.push('small:' + sig(e)); });
    return [...new Set(out)]; }
};
})();
</script>"""
if TM_TOOLS not in H.TOOLS:
    H.TOOLS = H.TOOLS + '\n' + TM_TOOLS

EXP_ROWS = {'t01': ('{주체능력}', '두0', '§12', [1, 1, 0]), 't02': ('{기일기간}', '두2', '§11', [1, 1, 1]), 't03': ('{분변분재 기간}', '두1', '§4', [0, 0, 1])}
BKC = ['#2563eb', '#7c3aed', '#059669']


def page(br, tag, src, dev, ls=None, keep_remote=False):
    if not keep_remote:
        REMOTE.clear()   # 관문마다 새 원격 — 앞 관문이 올린 기록(4초 뒤 저절로 맞춤)이 새 기기로 새어 들지 않게
    p = H.dev_page(br, tag, src, dev, ls=ls)
    p.ev("async () => await __TM.ready()")
    return p


def jo(p, k='제3조', tree=True):
    p.ev("async a => await __RB.jo('특허법', a[0], a[1])", [k, tree])


def at(p, sel, nth=0):
    return p.ev("([s, n]) => { const e = [...document.querySelectorAll(s)].filter(__TM.vis)[n]; return e ? __RB.hitOn(e) : null; }", [sel, nth])


def lp(p, a, ms=700):
    """길게 누르기 — 손가락 문맥 = 진짜 터치(CDP · WebKit = 합성 touch) · 마우스 문맥 = mouse down/up"""
    if not a or not a.get('on'):
        return False
    if p.touch:
        H.long_press(p, a['cx'], a['cy'], ms)
    else:
        p.pg.mouse.move(a['cx'], a['cy'])
        p.pg.mouse.down()
        p.wait(ms)
        p.pg.mouse.up()
        p.wait(350)
    return True


def rec(p):
    return p.ev("() => JSON.parse(localStorage.getItem('jopangi.theme') || '{}')")


def b1(br, src, base_src, tag):
    G = 'B1'
    ok = True
    for dn, dev in (('PC', PC), ('폰390', PHONE)):
        p = page(br, tag + dn, src, dev)
        jo(p)
        pb = page(br, tag + 'B' + dn, base_src, dev)
        jo(pb)
        base_tree = pb.ev("() => document.querySelector('#slot .tree').outerHTML")
        pb.close()
        tree0 = p.ev("() => __TM.treeSkel()")
        b = p.ev("() => { const b = document.querySelector('.jtbar .tmtg'); if (!b) return null; const s = document.querySelector('.jtbar .jstep:not(.tmtg)'); const cs = getComputedStyle(b), c2 = s ? getComputedStyle(s) : null;"
                 " return { t: __TM.txt(b), cls: b.className, same: !!c2 && cs.fontSize === c2.fontSize && cs.fontWeight === c2.fontWeight && cs.color === c2.color && cs.borderTopWidth === c2.borderTopWidth && cs.backgroundColor === c2.backgroundColor, hit: __RB.hitBox(b) }; }")
        g1 = bool(b) and b['t'] == '테마 3' and 'uzstep' in b['cls'] and 'jstep' in b['cls'] and b['same'] and (not p.touch or (b['hit']['h'] >= 36 and b['hit']['w'] >= 36))
        ok = ok and g1
        T(G, '%s 「테마 3」 글자 = 「접기1」 꼴(.uzstep.jstep) · 누름 ≥ 36(손가락)' % dn, g1, b)
        p.press(at(p, '.jtbar .tmtg'), 500)
        rows = p.ev("() => __TM.rows()")
        want = [(k,) + v for k, v in EXP_ROWS.items()]
        good = len(rows) == 3 and all(r['id'] == w[0] and r['t'] == w[1] and r['d2'] == w[2] and r['s'] == w[3] and 'r' in r['cls'].split() and
                                      [d == BKC[i] for i, d in enumerate(r['dots'])] == [bool(x) for x in w[4]] for r, w in zip(rows, want))
        tall = (not p.touch) or all(r['h'] >= 36 for r in rows)
        g2 = good and tall
        ok = ok and g2
        T(G, '%s 테마 줄 3(.r 꼴 · 점 색 = bk · 「두N」 「§N」 값%s)' % (dn, ' · 줄 높이 ≥ 36' if p.touch else ''), g2, rows)
        t2 = p.ev("() => __TM.txt(document.querySelector('.jtbar .tmtg'))")
        p.press(at(p, '.jtbar .tmtg'), 500)
        tree1 = p.ev("() => __TM.treeSkel()")
        g3 = t2 == '목차' and tree1 == tree0 == base_tree
        ok = ok and g3
        T(G, '%s 「목차」 → 조 줄 복원 · 서랍 outerHTML = 바탕(테마 글자 · 거름 점 빼고)' % dn, g3, {'글자': t2, '처음 = 복원': tree0 == tree1, '= 바탕': tree1 == base_tree, '길이': [len(tree1 or ''), len(base_tree or '')]})
        if p.errs:
            ok = False
            T(G, '%s JS 오류' % dn, False, p.errs[:3])
        p.close()
    # 다른 두 법 서랍 = 거름 점 하나만 더(「테마 N」 은 특허법만) · 나머지 outerHTML = 바탕
    p, pb = page(br, tag + 'L', src, PC), page(br, tag + 'LB', base_src, PC)
    oth = {}
    for law in ('상표법', '디자인보호법'):
        for q in (p, pb):
            q.ev("async a => await __RB.jo(a[0], a[1], true)", [law, '제1조'])
        n = p.ev("() => ({ dot: document.querySelectorAll('.jtbar .tmdot').length, tg: document.querySelectorAll('.jtbar .tmtg').length, skel: __TM.treeSkel() })")
        oth[law] = {'점': n['dot'], '테마 글자': n['tg'], '= 바탕': n['skel'] == pb.ev("() => document.querySelector('#slot .tree').outerHTML")}
    g4 = all(v['점'] == 1 and v['테마 글자'] == 0 and v['= 바탕'] for v in oth.values())
    ok = ok and g4
    T(G, 'PC 상표 · 디보 서랍 = 거름 점 하나만 더(「테마 N」 없음) · 나머지 outerHTML = 바탕', g4, oth)
    p.close()
    pb.close()
    return ok


def b2(br, src, base_src, tag):
    G = 'B2'
    p = page(br, tag, src, PC)
    jo(p)
    if not p.ev("() => !!document.querySelector('.jtbar .tmdot')"):   # 헛잣대(바탕) — 점이 없으면 잰 값으로 FAIL(멈춤 아님)
        T(G, '거름 점(.jtbar .tmdot · 「전체 N ▾」 뒤) 있음', False, {'점': None, '머리': p.ev("() => __TM.txt(document.querySelector('.jtbar'))")})
        p.close()
        return False
    n_all = p.ev("() => __TM.joRows()")
    seq = [p.ev("() => __TM.dot()")]
    cnt = {}
    for i in range(4):
        p.press(at(p, '.jtbar .tmdot'), 450)
        d = p.ev("() => __TM.dot()")
        seq.append(d)
        cnt[i] = (p.ev("() => __TM.joRows()"), d['chip'])
        if i == 1:
            subj_rows = p.ev("() => __TM.subjOn()")
            p.press(at(p, '.jtbar .tmtg'), 500)
            th = [r['id'] for r in p.ev("() => __TM.rows()")]
            p.press(at(p, '.jtbar .tmtg'), 500)
    pb = page(br, tag + 'B', base_src, PC)
    jo(pb)
    base_subj = pb.ev("() => [...document.querySelectorAll('#slot .tree .r[data-jo] .bkm3')].filter(b => { const d = b.querySelectorAll('.bkmk')[1]; return d && !!d.style.background; }).length")
    pb.close()
    cols = [x['bg'] for x in seq]
    g1 = cols == ['#ffffff', BKC[0], BKC[1], BKC[2], '#ffffff'] and seq[0]['bd'] != '#ffffff'
    T(G, '누름 4번 = 빈 → 파 → 보 → 초 → 빈', g1, cols)
    g2 = cnt[1][0] == base_subj == subj_rows and cnt[1][1] == '주체 %d ▾' % base_subj and th == ['t01', 't02']
    T(G, '보라 = 조 줄 수 = 주체 점 켜진 조(바탕 %d) · 머리 「주체 %d ▾」 · 테마 줄 = bk[1] 인 것' % (base_subj, base_subj), g2, {'조 줄': cnt[1], '켜진 점 셈': subj_rows, '테마': th})
    g3 = cnt[3][0] == n_all and cnt[3][1] == '전체 %d ▾' % n_all
    T(G, '빈 = 전체(%d)' % n_all, g3, cnt[3])
    ok = g1 and g2 and g3 and not p.errs
    if p.errs:
        T(G, 'JS 오류', False, p.errs[:3])
    p.close()
    return ok


def b3(br, src, tag):
    G = 'B3'
    p = page(br, tag, src, PC)
    jo(p)
    if not p.ev("() => typeof tmWin === 'function'"):   # 헛잣대(바탕) — 테마 창이 없으면 잰 값으로 FAIL
        T(G, '테마 창(theme|t02) 열림', False, {'tmWin': False, '서랍 테마 줄': p.ev("() => document.querySelectorAll('#slot .tree .r.tmr').length"), '창': p.ev("() => POPS.map(x => x._pk)")})
        p.close()
        return False
    p.ev("() => tmWin('t02', null)")
    p.wait(500)
    w = p.ev("""() => { const w = __TM.pop('theme|t02'); if (!w) return null; const hd = w.querySelector('.ph');
      return { t: __TM.txt(w.querySelector('.pt')), hdKids: [...hd.children].map(e => e.tagName.toLowerCase() + '.' + e.className), thl: w.querySelectorAll('.thl').length,
        cols: [...w.querySelectorAll('.thl')].map(l => [...l.children].map(s => __TM.hex(s.style.color))), lk: w.querySelectorAll('.wmlk').length, sb: w.querySelectorAll('.thsb').length, ac: w.querySelectorAll('.thac').length }; }""")
    want_cols = [[r['c'] for r in ln['runs']] for ln in BOXES['b2']['lines']]
    g1 = bool(w) and w['t'] == '{기일기간} · 두2 §11' and w['thl'] == PLANT['t02']['lines'] and w['cols'] == want_cols and w['lk'] == PLANT['t02']['links'] and w['sb'] == PLANT['t02']['subj'] and w['ac'] == PLANT['t02']['acr'] \
        and all(not re.search(r'tm|jo', k) for k in w['hdKids'][1:])
    T(G, '테마 창 제목 「{기일기간} · 두2 §11」 · 머리에 조 목록 0 · .thl 줄 수 · run 색 · 조 링크 · 주체 · 두문자 = 재료', g1, w)
    a = p.ev("""() => { const w = __TM.pop('theme|t02'); const l = [...w.querySelectorAll('.wmlk')].find(x => x.dataset.k === '제16조' && x.dataset.law === '특허법'); return l ? __RB.hitOn(l) : null; }""")
    p.press(a, 1500)
    g2 = p.ev("() => !!POPS.find(x => x._pk === 'jo|특허법|제16조')")
    other = p.ev("() => { const w = __TM.pop('theme|t02'); const l = [...w.querySelectorAll('.wmlk')].map(x => x.dataset.law + ':' + x.dataset.k); return l; }")
    T(G, '조 링크 누름 → 조문 팝업(키 jo|특허법|제16조) · 다른 법(민소) 링크 · 시규 = 링크 없음', g2 and '민사소송법:제16조' in other and len([x for x in other if x.startswith('특허법:제3조')]) == 1, {'열림': g2, '링크': other})
    p.ev("() => { const p0 = POPS.find(x => x._pk === 'jo|특허법|제16조'); if (p0) closeOne(p0); }")
    a = p.ev("() => { const w = __TM.pop('theme|t02'); return __RB.hitOn(w.querySelector('.thac')); }")
    p.press(a, 300)
    m1 = p.ev("() => { const w = __TM.pop('theme|t02'); const m = w.querySelector('.thacm'); return m ? __TM.txt(m) : null; }")
    a = p.ev("() => { const w = __TM.pop('theme|t02'); return __RB.hitOn(w.querySelector('.thac')); }")
    p.press(a, 300)
    m2 = p.ev("() => { const w = __TM.pop('theme|t02'); return !!w.querySelector('.thacm'); }")
    g3 = bool(m1) and m1.startswith('정사소2만1') and not m2
    T(G, '두문자 누름 → 그 자리 아래 뜻 한 줄 토글', g3, [m1, m2])
    p.ev("() => tmWin('t03', null)")
    p.wait(500)
    s = p.ev("() => { const w = __TM.pop('theme|t03'); return w ? { svg: w.querySelectorAll('.thfig svg').length, text: w.querySelectorAll('.thfig svg text').length, path: w.querySelectorAll('.thfig svg path').length, lk: w.querySelectorAll('.thfig .wmlk').length, thl: w.querySelectorAll('.thl').length } : null; }")
    g4 = bool(s) and s['svg'] == 1 and s['text'] == PLANT['t03']['svgtext'] and s['path'] == PLANT['t03']['path'] and s['lk'] == PLANT['t03']['links'] and s['thl'] == 0
    T(G, '분변분재 = svg(text 수 · path 수 = 재료 · 글 속 조 링크)', g4, s)
    ok = bool(g1 and g2 and g3 and g4) and not p.errs
    if p.errs:
        T(G, 'JS 오류', False, p.errs[:3])
    p.close()
    return ok


def b4(br, src, tag):
    G = 'B4'
    p = page(br, tag, src, PC)
    jo(p)
    if not p.ev("() => typeof tmListWin === 'function'"):   # 헛잣대(바탕) — 목록 창이 없으면 잰 값으로 FAIL
        T(G, '두문자·조 목록 창(themelist|t03) 열림', False, {'tmListWin': False, '「두N §N」': p.ev("() => document.querySelectorAll('#slot .tree .tmds').length"), '창': p.ev("() => POPS.map(x => x._pk)")})
        p.close()
        return False
    p.ev("() => tmListWin('t03', null)")
    p.wait(700)
    r3 = p.ev("() => { const w = __TM.pop('themelist|t03'); const r = w && w.querySelector('.throw2'); return r ? { l: __TM.txt(r.querySelector('.tmjs')), r: __TM.txt(r.querySelector('.tmar')), h: Math.round(r.getBoundingClientRect().height) } : null; }")
    g1 = bool(r3) and r3['l'] == '52조 · 53조 · 52-2조 · 67-2조' and r3['r'] == '분변분재' and r3['h'] >= 36
    T(G, '분변분재 맨 위 줄 = 「52조 · 53조 · 52-2조 · 67-2조 | 분변분재」(≥ 36)', g1, r3)
    p.ev("() => tmListWin('t02', null)")
    p.wait(700)
    r16 = p.ev("() => { const w = __TM.pop('themelist|t02'); const r = [...w.querySelectorAll('.throw2.tmjr')].find(x => x.dataset.lk === '특허법:제16조'); return r ? { n: __TM.txt(r.querySelector('.tmjn')), t: __TM.txt(r.querySelector('.tmjt')), r: __TM.txt(r.querySelector('.tmar')), c: getComputedStyle(r.querySelector('.tmjn')).color } : null; }")
    g2 = bool(r16) and r16['n'] == '제16조' and r16['r'] == '정사소2만1' and r16['t'] != '' and r16['c'] == 'rgb(29, 78, 216)'
    T(G, '기일기간 16조 줄 오른쪽 「정사소2만1」(제N조 파랑 굵게 · 제목)', g2, r16)
    a = p.ev("() => { const w = __TM.pop('themelist|t02'); const r = [...w.querySelectorAll('.throw2.tmjr')].find(x => x.dataset.lk === '특허법:제14조'); return __RB.hitOn(r.querySelector('.tmjt')); }")
    p.press(a, 1500)
    g3 = p.ev("() => !!POPS.find(x => x._pk === 'jo|특허법|제14조')")
    T(G, '조 줄 누름 → 조문 팝업', g3, g3)
    ok = bool(g1 and g2 and g3) and not p.errs
    if p.errs:
        T(G, 'JS 오류', False, p.errs[:3])
    p.close()
    return ok


def b5(br, src, tag):
    G = 'B5'
    p = page(br, tag, src, PC)
    jo(p, '제3조')
    tb = p.ev("() => { const b = document.querySelector('.jomt .tmjo'); return b ? { t: __TM.txt(b), c: __TM.hex(getComputedStyle(b).color), n: getComputedStyle(b.querySelector('.n')).fontWeight, bd: getComputedStyle(b).borderTopWidth, bg: getComputedStyle(b).backgroundColor } : null; }")
    g1 = bool(tb) and tb['t'] == '테마 2' and tb['c'] == '#a16207' and int(tb['n']) >= 700 and tb['bg'] in ('rgba(0, 0, 0, 0)', 'transparent')
    T(G, '제3조 「테마 2」(#a16207 · 숫자 굵게 · 알약 없음) — 합성 재료의 조 목록 그대로면 제3조 = 주체능력 · 기일기간 둘', g1, tb)
    p.press(at(p, '.jomt .tmjo'), 500)
    p.ev("() => { document.querySelector('.jtbar .tmtg').click(); }")
    p.idle(300)
    sk = p.ev("""() => { const w = __TM.pop('themeof|특허법|제3조'); if (!w) return null; const rs = [...w.querySelectorAll('.tmof .r.tmr')];
      const tr = [...document.querySelectorAll('#slot .tree .r.tmr')]; const by = id => tr.find(x => x.dataset.tm === id);
      return { t: __TM.txt(w.querySelector('.pt')), n: rs.length, same: rs.every(r => { const d = by(r.dataset.tm); return d && __TM.skel(d) === __TM.skel(r); }), x: rs.map(r => !!r.querySelector('.tmx')) }; }""")
    g2 = bool(sk) and sk['n'] == 2 and sk['same'] and sk['t'] == '제3조 · 테마 2' and sk['x'] == [False, False]
    T(G, '연결 창 = 연결 줄 2(서랍 테마 줄과 outerHTML 구조 같음 · 재료 연결 = ✕ 없음)', g2, sk)
    srch = lambda q: p.ev("""async q => { const w = __TM.pop('themeof|특허법|제3조'); const i = w.querySelector('.thsrch input'); i.value = q; w.querySelector('.thsrch .tmsgo').click(); await __TM.wait(200);
      const w2 = __TM.pop('themeof|특허법|제3조'); return [...w2.querySelectorAll('.tmres .r.tmr')].map(r => [r.dataset.tm, !!r.querySelector('.tmplus')]); }""", q)
    r_sim, r_gi, r_bb = srch('심판'), srch('기일'), srch('분변')
    g3 = r_sim == [] and r_gi == [] and r_bb == [['t03', True]]
    T(G, '찾기 「심판」 → 0 · 「기일」 → 0(기일기간은 이미 이음 — 결과 줄마다 ＋ 가 있게 이은 테마는 뺀다) · 「분변」 → 1(끝 ＋)', g3, {'심판': r_sim, '기일': r_gi, '분변': r_bb})
    a = p.ev("() => { const w = __TM.pop('themeof|특허법|제3조'); const r = w.querySelector('.tmres .r.tmr[data-tm=t03] .tmplus'); return r ? __RB.hitOn(r) : null; }")
    p.press(a, 700)
    rc = rec(p)
    st = p.ev("() => { const w = __TM.pop('themeof|특허법|제3조'); return { t: __TM.txt(w.querySelector('.pt')), x: [...w.querySelectorAll('.tmof .r.tmr')].map(r => [r.dataset.tm, !!r.querySelector('.tmx')]), btn: __TM.txt(document.querySelector('.jomt .tmjo')) }; }")
    g4 = (rc.get('link') or {}).get('특허법:제3조') == ['t03'] and st['btn'] == '테마 3' and ['t03', True] in st['x'] and st['t'] == '제3조 · 테마 3'
    T(G, '＋ → 기록 link["특허법:제3조"] · 「테마 3」 · 그 줄만 끝 ✕', g4, {'link': rc.get('link'), '창': st})
    a = p.ev("() => { const w = __TM.pop('themeof|특허법|제3조'); const r = w.querySelector('.tmof .r.tmr[data-tm=t03] .tmx'); return r ? __RB.hitOn(r) : null; }")
    p.press(a, 700)
    rc = rec(p)
    st2 = p.ev("() => __TM.txt(document.querySelector('.jomt .tmjo'))")
    g5 = not (rc.get('link') or {}).get('특허법:제3조') and st2 == '테마 2'
    T(G, '줄 끝 ✕ → 풂(「테마 2」)', g5, {'link': rc.get('link'), '글자': st2})
    jo(p, '제4조')
    n4 = p.ev("() => __TM.txt(document.querySelector('.jomt .tmjo'))")
    p.press(at(p, '.jomt .tmjo'), 500)
    r4 = p.ev("""async () => { const w = __TM.pop('themeof|특허법|제4조'); const i = w.querySelector('.thsrch input'); i.value = '기일'; w.querySelector('.thsrch .tmsgo').click(); await __TM.wait(200);
      return [...__TM.pop('themeof|특허법|제4조').querySelectorAll('.tmres .r.tmr')].map(r => r.dataset.tm); }""")
    g6 = n4 == '테마 1' and r4 == ['t02']
    T(G, '제4조 「테마 1」 · 거기서 「기일」 → 1(기일기간)', g6, {'글자': n4, '기일': r4})
    ok = bool(g1 and g2 and g3 and g4 and g5 and g6) and not p.errs
    if p.errs:
        T(G, 'JS 오류', False, p.errs[:3])
    p.close()
    return ok


EDITOR = r"""() => { const e = [...document.querySelectorAll('.tmed')]; return { n: e.length, btns: e.map(x => x.querySelectorAll('button').length), inp: e.map(x => x.querySelectorAll('input').length),
  foc: !!document.activeElement && document.activeElement.classList.contains('thed'), ok: e[0] ? __RB.hitBox(e[0].querySelector('.tmok')) : null, v: e[0] ? e[0].querySelector('input').value : null }; }"""


def type_ok(p, text):
    p.pg.keyboard.press('Control+A')
    if text:
        p.pg.keyboard.type(text)
    else:
        p.pg.keyboard.press('Backspace')
    a = p.ev("() => { const b = document.querySelector('.tmed .tmok'); return b ? __RB.hitOn(b) : null; }")
    p.press(a, 600)


def b6(br, src, tag, devs=(('폰390', PHONE), ('PC', PC))):
    G = 'B6'
    ok = True
    for dn, dev in devs:
        p = page(br, tag + dn, src, dev)
        jo(p)
        p.press(at(p, '.jtbar .tmtg'), 500)
        a = p.ev("() => __RB.hitOn(document.querySelector('#slot .tree .r.tmr[data-tm=t02] .jno'))")
        lp(p, a, 700)
        e = p.ev(EDITOR)
        g1 = e['n'] == 1 and e['btns'] == [1] and e['inp'] == [1] and e['foc'] and e['v'] == '기일기간' and e['ok'] and e['ok']['h'] >= 36 and e['ok']['w'] >= 36
        T(G, '%s 서랍 이름 길게(%s 700ms) → 입력 칸 + ✓ 하나(다른 단추 0 · ✓ ≥ 36 · 포커스)' % (dn, '터치' if p.touch else '마우스'), g1, e)
        type_ok(p, '기일·기간')
        nm = p.ev("() => __TM.txt(document.querySelector('#slot .tree .r.tmr[data-tm=t02] .jno'))")
        p.ev("() => tmWin('t02', null)")
        p.wait(400)
        wt = p.ev("() => __TM.txt(__TM.pop('theme|t02').querySelector('.pt'))")
        rc = rec(p)
        g2 = nm == '{기일·기간}' and wt.startswith('{기일·기간}') and (rc.get('t02') or {}).get('n') == '기일·기간'
        T(G, '%s 「기일·기간」 ✓ → 서랍 · 창 제목 · 기록 n' % dn, g2, {'서랍': nm, '창': wt, '기록': rc.get('t02')})
        p.ev("() => closeAllPops(true)")
        a = p.ev("() => __RB.hitOn(document.querySelector('#slot .tree .r.tmr[data-tm=t01] .jno'))")
        lp(p, a, 700)
        p.pg.keyboard.type('없앨 글')
        p.press(p.ev("() => __RB.hitOn(document.querySelector('.jtbar .jckf'))"), 400) if False else None
        out = p.ev("() => { const e = document.querySelector('.jomt'); return e ? __RB.hitOn(e) : null; }")
        # ★ 로컬 10/2 — 폰 390 에서 .jomt 위 30px 이 편집 중인 테마 줄(.r.tmr.tmon · ✓ 아래 여백) 안에 떨어져 「바깥」이 아니었다(elementsFromPoint 잼)
        #   → 그 점이 편집 줄 안이면 서랍 안 · 마지막 줄 아래 빈 자리를 누른다(편집 줄 밖 · 폰에서 서랍 밖을 누르면 서랍이 닫혀 뒤 칸이 못 돎 · §B-6 「바깥 누름 → 취소」 그대로)
        inrow = p.ev("a => { const e = document.elementFromPoint(a[0], a[1]); return !!(e && e.closest('.r.tmr.tmon, .tmed')); }", [out['cx'], out['cy'] - 30])
        if inrow:
            em = p.ev("() => { const t = document.querySelector('#slot > .tree'); if (!t) return null; const rs = [...t.querySelectorAll('.r')].filter(r => r.getClientRects().length); const tb = t.getBoundingClientRect(); const lb = rs.length ? rs[rs.length - 1].getBoundingClientRect().bottom : tb.top; const y = Math.min(lb + 40, tb.bottom - 10); return { cx: tb.left + 60, cy: y, ok: y > lb + 5 }; }")
            if em and em.get('ok'):
                out = dict(out, cx=em['cx'], cy=em['cy'] + 30)
        if p.touch:
            p.tap(out['cx'], out['cy'] - 30, 400)
        else:
            p.click(out['cx'], out['cy'] - 30, 400)
        cancel = p.ev("() => ({ n: document.querySelectorAll('.tmed').length, t: __TM.txt(document.querySelector('#slot .tree .r.tmr[data-tm=t01] .jno')) })")
        g3 = cancel['n'] == 0 and cancel['t'] == '{주체능력}' and not (rec(p).get('t01') or {}).get('n')
        T(G, '%s 바깥 누름 → 취소' % dn, g3, cancel)
        a = p.ev("() => __RB.hitOn(document.querySelector('#slot .tree .r.tmr[data-tm=t03] .jno'))")
        lp(p, a, 700)
        type_ok(p, '')
        rows = [r['id'] for r in p.ev("() => __TM.rows()")]
        g4 = rows == ['t01', 't02'] and (rec(p).get('t03') or {}).get('gone') == 1
        T(G, '%s 비우고 ✓ → 목록에서 빠짐 + gone' % dn, g4, {'줄': rows, '기록': rec(p).get('t03')})
        if dn == '폰390' or len(devs) == 1:
            # 테마 창 줄 · 두문자 뜻 · 목록 창 조 줄 지움 · 「＋ 테마」 · 두 칸 동시 0
            p.ev("() => tmWin('t02', null)")
            p.wait(400)
            a = p.ev("() => { const w = __TM.pop('theme|t02'); return __RB.hitOn(w.querySelectorAll('.thl')[2]); }")
            lp(p, a, 700)
            e2 = p.ev(EDITOR)
            type_ok(p, '고친 셋째 줄')
            l2 = p.ev("() => __TM.txt(__TM.pop('theme|t02').querySelectorAll('.thl')[2])")
            g5 = e2['n'] == 1 and ((rec(p).get('t02') or {}).get('l') or {}).get('b2|2') == '고친 셋째 줄' and l2 == '고친 셋째 줄'
            T(G, '%s 테마 창 줄 길게 → 고침 → 기록 l["b2|2"] · 창 즉시' % dn, g5, {'칸': e2, '줄': l2, '기록': (rec(p).get('t02') or {}).get('l')})
            a = p.ev("() => { const w = __TM.pop('theme|t02'); const b = [...w.querySelectorAll('.thac')].find(x => x.dataset.w === '책사소2만1'); return __RB.hitOn(b); }")
            lp(p, a, 700)
            type_ok(p, '합성 뜻 둘')
            g6 = ((rec(p).get('acr') or {}).get('책사소2만1') or {}).get('m') == '합성 뜻 둘'
            T(G, '%s 두문자 뜻 적기 → 기록 acr.m' % dn, g6, rec(p).get('acr'))
            p.ev("() => tmListWin('t02', null)")
            p.wait(600)
            a = p.ev("() => { const w = __TM.pop('themelist|t02'); const r = [...w.querySelectorAll('.throw2.tmjr')].find(x => x.dataset.lk === '특허법:제190조'); return __RB.hitOn(r.querySelector('.tmjn')); }")
            lp(p, a, 700)
            type_ok(p, '')
            rc = rec(p)
            lst = p.ev("() => [...__TM.pop('themelist|t02').querySelectorAll('.throw2.tmjr')].map(r => r.dataset.lk)")
            g7 = '190' in ((rc.get('t02') or {}).get('jo-') or []) and '특허법:제190조' not in lst
            T(G, '%s 목록 창 조 줄 지움 → jo- · 줄 빠짐' % dn, g7, {'jo-': (rc.get('t02') or {}).get('jo-'), '남은 줄 수': len(lst)})
            p.ev("() => closeAllPops(true)")
            a = p.ev("() => __RB.hitOn(document.querySelector('#slot .tree .r.tmaddr'))")
            p.press(a, 500)
            type_ok(p, '새 합성 테마')
            rows2 = p.ev("() => __TM.rows().map(r => r.t)")
            g8 = '{새 합성 테마}' in rows2 and any((v or {}).get('n') == '새 합성 테마' for k, v in rec(p).items() if k.startswith('u'))
            T(G, '%s 「＋ 테마」 → 새 테마 줄 · 기록' % dn, g8, rows2)
            a1 = p.ev("() => __RB.hitOn(document.querySelector('#slot .tree .r.tmr[data-tm=t01] .jno'))")
            lp(p, a1, 700)
            n1 = p.ev("() => document.querySelectorAll('.tmed').length")
            a2 = p.ev("() => __RB.hitOn(document.querySelector('#slot .tree .r.tmr[data-tm=t02] .jno'))")
            lp(p, a2, 700)
            n2 = p.ev("() => document.querySelectorAll('.tmed').length")
            g9 = n1 == 1 and n2 == 1
            T(G, '%s 두 입력 칸 동시 0(다른 칸을 열면 먼저 닫힘)' % dn, g9, [n1, n2])
            ok = ok and g5 and g6 and g7 and g8 and g9
        ok = ok and g1 and g2 and g3 and g4
        if p.errs:
            ok = False
            T(G, '%s JS 오류' % dn, False, p.errs[:3])
        p.close()
    return ok


SYNC = "async () => { stampAll(); await syncRecords(true); return recLastErr || ''; }"


def b7(br, src, base_src, tag):
    G = 'B7'
    ok = True
    REMOTE.clear()
    A = page(br, tag + 'A', src, PC)
    last = A.ev("() => SYNC_KEYS[SYNC_KEYS.length - 1]")
    g0 = last == 'jopangi.theme'
    T(G, '새 키 jopangi.theme · SYNC_KEYS 끝', g0, last)
    A.ev("() => { const r = JSON.parse(localStorage.getItem('jopangi.theme') || '{}'); r.t01 = { n: '주체능력A' }; localStorage.setItem('jopangi.theme', JSON.stringify(r)); }")
    e1 = A.ev(SYNC)
    r1 = (REMOTE.rec() or {})
    d1 = (r1.get('data') or {}).get('jopangi.theme') or {}
    g1 = not e1 and (d1.get('t01') or {}).get('n') == '주체능력A' and bool((r1.get('u') or {}).get('jopangi.theme|t01'))
    T(G, 'A 이름 고침 → 올린 몸통 data 에 그 칸 + 칸 도장', g1, {'err': e1, 'data': d1, 'u': {k: v for k, v in (r1.get('u') or {}).items() if 'theme' in k}})
    B = page(br, tag + 'B', src, PC, keep_remote=True)
    B.ev(SYNC)
    jo(B)
    B.ev("() => document.querySelector('.jtbar .tmtg').click()")
    B.idle(300)
    bn = B.ev("() => __TM.rows().map(r => r.t)")
    g2 = '{주체능력A}' in bn
    T(G, '새 기기 B 맞춤 → 받은 이름이 서랍에', g2, bn)
    # 칸 단위 병합 — A 는 t02 이름 · B 는 두문자 사전(acr 칸) · 서로 다른 칸이라 둘 다 산다
    A.ev("() => { const r = JSON.parse(localStorage.getItem('jopangi.theme') || '{}'); r.t02 = { n: '기일기간A' }; localStorage.setItem('jopangi.theme', JSON.stringify(r)); }")
    B.ev("() => { const r = JSON.parse(localStorage.getItem('jopangi.theme') || '{}'); r.acr = { '책사소2만1': { m: 'B 가 적은 뜻' } }; localStorage.setItem('jopangi.theme', JSON.stringify(r)); }")
    A.ev(SYNC)
    B.ev(SYNC)
    A.ev(SYNC)
    ra, rb = rec(A), rec(B)
    g3 = ra == rb and (ra.get('t02') or {}).get('n') == '기일기간A' and ((ra.get('acr') or {}).get('책사소2만1') or {}).get('m') == 'B 가 적은 뜻' and (ra.get('t01') or {}).get('n') == '주체능력A'
    T(G, '두 기기 병합 = 칸 단위(A 의 t02 · B 의 acr 둘 다 산다)', g3, {'A': ra, 'B': rb})
    # 묘비 — B 가 손 연결 칸(link)을 만들었다 지우면 A 에서도 안 되살아난다(칸 전체 지움 = 동기화 묘비)
    B.ev("() => { const r = JSON.parse(localStorage.getItem('jopangi.theme') || '{}'); r.link = { '특허법:제9조': ['t01'] }; localStorage.setItem('jopangi.theme', JSON.stringify(r)); }")
    B.ev(SYNC)
    A.ev(SYNC)
    had = 'link' in rec(A)
    B.ev("() => { const r = JSON.parse(localStorage.getItem('jopangi.theme') || '{}'); delete r.link; localStorage.setItem('jopangi.theme', JSON.stringify(r)); }")
    B.ev(SYNC)
    A.ev(SYNC)
    r4 = REMOTE.rec() or {}
    g4 = had and 'link' not in rec(A) and bool((r4.get('gone') or {}).get('jopangi.theme|link'))
    T(G, '묘비 — B 가 지운 칸(link) = A 에서도 지워짐 · 원격 gone 도장', g4, {'A 가 받았었나': had, 'A 지금': list(rec(A).keys()), 'gone': {k: v for k, v in (r4.get('gone') or {}).items() if 'theme' in k}})
    # 옛 판 기기(키 없음) 올림 → data 에서 빠짐 → 새 판 A 다시 맞춤 → 되살아남
    O = page(br, tag + 'O', base_src, PC, keep_remote=True)
    O.ev(SYNC)
    r5 = REMOTE.rec() or {}
    lost = 'jopangi.theme' not in (r5.get('data') or {})
    keep_u = any(k.startswith('jopangi.theme|') for k in (r5.get('u') or {}))
    C = page(br, tag + 'C', src, PC, keep_remote=True)
    C.ev(SYNC)
    c0 = rec(C)
    A.ev(SYNC)
    r6 = REMOTE.rec() or {}
    back = ((r6.get('data') or {}).get('jopangi.theme') or {}).get('t01', {}).get('n') == '주체능력A'
    C.ev(SYNC)
    c1 = rec(C)
    N(G, '옛 판 기기 틈(잰 것)', {'옛 판 올림 뒤 data.jopangi.theme': '빠짐' if lost else '남음', '도장 u': '남음' if keep_u else '빠짐', '그 사이 새 기기 C': c0 or '못 받음',
                             '새 판 A 다시 맞춤 뒤': '되살아남' if back else '안 돌아옴', 'C 다시 맞춤 뒤 t01': (c1.get('t01') or {}).get('n')})
    g5 = lost and keep_u and back and (c1.get('t01') or {}).get('n') == '주체능력A' and not O.errs
    T(G, '옛 판 기기(키 없음) 올림 뒤 새 판 다시 맞춤 → 되살아남(새 기기도 받음 · 옛 판 오류 0)', g5, {'빠짐': lost, 'u': keep_u, '되살아남': back, 'C': c1.get('t01'), '옛 판 오류': O.errs[:2]})
    for q in (A, B, O, C):
        if q.errs:
            ok = False
            T(G, 'JS 오류', False, q.errs[:3])
        q.close()
    return ok and g0 and g1 and g2 and g3 and g4 and g5


SK = r"""async ([q, scopes]) => { openSk(); Object.keys(SKON).forEach(k => { SKON[k] = scopes.indexOf(k) >= 0; }); skPaint(); const i = document.getElementById('skin'); i.value = q; await skRun({ target: i });
  const box = document.getElementById('skres'); const grp = [...box.querySelectorAll('.grp')].map(g => __TM.txt(g));
  const rows = [...box.querySelectorAll('.res')].map(r => ({ h: __TM.txt(r.querySelector('b')), x: __TM.txt(r.querySelector('.x')), tag: __TM.txt(r.querySelector('.lawtag')), ic: __TM.txt(r.querySelector('.skic')) })); return { grp, rows }; }"""


def b8(br, src, base_src, tag):
    G = 'B8'
    p = page(br, tag, src, PC)
    jo(p)
    r = p.ev(SK, ['정사소', ['jo']])
    th = [x for x in r['rows'] if x['tag'] == '테마']
    g1 = '🧩 테마 — 1건' in r['grp'] and len(th) == 1 and th[0]['h'] == '{기일기간}' and '정사소' in th[0]['x']
    T(G, '🔍 「정사소」 → 결과 줄 「{기일기간} …」', g1, r)
    a = p.ev("() => { const d = [...document.querySelectorAll('#skres .res')].find(x => __TM.txt(x.querySelector('b')) === '{기일기간}'); return d ? __RB.hitOn(d) : null; }")
    p.press(a, 700)
    g2 = p.ev("() => !!POPS.find(x => x._pk === 'theme|t02') && document.getElementById('sk').style.display === 'none'")
    T(G, '결과 줄 누름 → 테마 창', g2, g2)
    pb = page(br, tag + 'B', base_src, PC)
    jo(pb)
    same = {}
    for q in ('기간', '특허청장'):
        rn = p.ev(SK, [q, ['jo', 'prec']])
        rb = pb.ev(SK, [q, ['jo', 'prec']])
        gn = [g for g in rn['grp'] if not g.startswith('🧩 테마')]
        same[q] = (gn == rb['grp'], [x for x in rn['rows'] if x['tag'] != '테마'] == rb['rows'], gn[:2], rb['grp'][:2])
    pb.close()
    g3 = all(v[0] and v[1] for v in same.values())
    T(G, '조문·판례 결과 무변(바탕과 갈래 머리 수·줄 같음)', g3, same)
    ok = g1 and g2 and g3 and not p.errs
    if p.errs:
        T(G, 'JS 오류', False, p.errs[:3])
    p.close()
    return ok


KINDS = ['cell', 'q', 'fn', '', 'canvas', 'claude', 'wm', 'ncbook', 'cflw', 'c2unit']
FRAME = r"""(kinds) => kinds.map(k => { const b = popShell(k, '틀 ' + (k || '기본'), 'frame|' + k); const p = b.parentNode, cs = getComputedStyle(p), ph = p.querySelector('.ph'), hs = getComputedStyle(ph), pt = getComputedStyle(p.querySelector('.pt')), x = getComputedStyle(ph.querySelector('button'));
  const o = { k: k, bg: cs.backgroundColor, bd: cs.borderTopColor, bw: cs.borderTopWidth, rad: cs.borderTopLeftRadius, sh: cs.boxShadow, hbg: hs.backgroundColor, hbd: hs.borderBottomColor, ptw: pt.fontWeight, ptc: pt.color, pts: pt.fontSize,
    xb: x.borderTopColor, xc: x.color, xw: x.fontWeight, w: Math.round(p.getBoundingClientRect().width) }; closeOne(p); return o; })"""


def b9(br, src, base_src, tag):
    G = 'B9'
    p = page(br, tag, src, PC)
    jo(p)
    fr = p.ev(FRAME, KINDS)
    pb = page(br, tag + 'B', base_src, PC)
    jo(pb)
    frb = pb.ev(FRAME, KINDS)
    good = [f for f in fr if f['bg'] == 'rgb(255, 255, 255)' and f['bd'] == 'rgb(203, 213, 225)' and f['bw'] == '1px' and f['rad'] == '12px' and 'rgba(0, 0, 0, 0.28)' in f['sh'] and f['hbg'] == 'rgb(248, 250, 252)'
            and f['ptw'] == '800' and f['ptc'] == 'rgb(17, 24, 39)' and f['xb'] == 'rgb(209, 213, 219)' and f['xc'] == 'rgb(107, 114, 128)']
    g1 = len(good) == len(KINDS)
    T(G, 'popShell 10종 — .pop 흰/#cbd5e1/12/그림자 · .ph #f8fafc · 제목 800 #111827 · ✕ 회색 테두리 · k-q·k-fn·k-cell 색 0', g1, {'맞음': len(good), '어긋남': [f for f in fr if f not in good][:3]})
    g2 = [f['w'] for f in fr] == [f['w'] for f in frb]
    T(G, '폭 = 바탕(종류별 폭 유지)', g2, {'새 판': [f['w'] for f in fr], '바탕': [f['w'] for f in frb]})
    memo = p.ev("""async () => { pitEdit('jo|특허법:제3조', '0', 0, '틀', null); await __TM.wait(300); const w = POPS[POPS.length - 1]; const ta = w.querySelector('textarea.memoin'), sv = w.querySelector('.memobtn .tool.on'), dl = [...w.querySelectorAll('.memobtn .tool')].find(b => !b.classList.contains('on'));
      const o = { ta: getComputedStyle(ta).backgroundColor, tab: getComputedStyle(ta).borderTopColor, sv: getComputedStyle(sv).backgroundColor, svc: getComputedStyle(sv).color, dl: dl ? getComputedStyle(dl).borderTopColor : null }; closeOne(w); return o; }""")
    g3 = memo['ta'] == 'rgb(255, 255, 255)' and memo['tab'] == 'rgb(203, 213, 225)' and memo['sv'] == 'rgb(17, 24, 39)' and memo['svc'] == 'rgb(255, 255, 255)' and memo['dl'] == 'rgb(209, 213, 219)'
    T(G, '메모 창 textarea 흰 · 저장 #111827 · 🗑 삭제 회색 테두리', g3, memo)
    a = p.ev("() => { const l = document.querySelector('#slot .main .box .wmlk'); return l ? __RB.hitOn(l) : null; }")
    p.press(a, 1500)
    go1 = p.ev("() => { const w = POPS.filter(x => (x._pk || '').indexOf('jo|') === 0).pop(); const b = w && w.querySelector('.ph .ptgo button'); return b ? { t: __TM.txt(b), bw: getComputedStyle(b).borderTopWidth, c: getComputedStyle(b).color, fw: getComputedStyle(b).fontWeight } : null; }")
    p.ev("() => closeAllPops(true)")
    jo(p, '제29조')
    go2 = p.ev("""async () => { const c = [...document.querySelectorAll('.conn .plgb')].find(b => /2차문제 [1-9]/.test(__TM.txt(b))); if (!c) return 'no-2cha'; c.click(); await __TM.wait(400);
      const w = POPS[POPS.length - 1]; const r = w.querySelector('.lnkrow'); if (!r) return 'no-row'; r.click(); await __TM.wait(900); const q = POPS[POPS.length - 1]; const b = q.querySelector('.ph .ptgo button');
      return b ? { t: __TM.txt(b), bw: getComputedStyle(b).borderTopWidth, c: getComputedStyle(b).color, fw: getComputedStyle(b).fontWeight, inBody: !!q.querySelector('.pb > button.tool.on') } : 'no-btn'; }""")
    ok_go = lambda g: isinstance(g, dict) and g['t'] == '이동 ↗' and g['bw'] == '0px' and g['c'] == 'rgb(29, 78, 216)' and g['fw'] == '600'
    g4 = ok_go(go1) and ok_go(go2) and not go2.get('inBody')
    T(G, '머리 「이동 ↗」 글자(테두리 0 · #1d4ed8 · 600) 두 곳(조문 팝업 · 2차 문제 창)', g4, {'조문': go1, '2차': go2})
    drag = []
    for q in (p, pb):
        d = q.ev("""async () => { closeAllPops(true); const b = popShell('', '끌기', 'drag|x'); const w = b.parentNode; w.style.left = '300px'; w.style.top = '200px'; await __TM.wait(50);
          const h = w.querySelector('.ph').getBoundingClientRect(), s = w.querySelector('.prsz'); return { hx: h.left + 60, hy: h.top + h.height / 2, sx: s ? s.getBoundingClientRect().left + 8 : null, sy: s ? s.getBoundingClientRect().top + 8 : null }; }""")
        q.pg.mouse.move(d['hx'], d['hy'])
        q.pg.mouse.down()
        q.pg.mouse.move(d['hx'] + 80, d['hy'] + 40, steps=5)
        q.pg.mouse.up()
        q.wait(200)
        pos = q.ev("() => { const w = POPS[POPS.length - 1]; return [Math.round(parseFloat(w.style.left)), Math.round(parseFloat(w.style.top))]; }")
        s2 = q.ev("() => { const s = POPS[POPS.length - 1].querySelector('.prsz'); const r = s.getBoundingClientRect(); return [r.left + 8, r.top + 8]; }")
        q.pg.mouse.move(s2[0], s2[1])
        q.pg.mouse.down()
        q.pg.mouse.move(s2[0] + 60, s2[1] + 50, steps=5)
        q.pg.mouse.up()
        q.wait(200)
        sz = q.ev("() => { const w = POPS[POPS.length - 1]; const r = w.getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; }")
        drag.append((pos, sz))
    pb.close()
    g5 = drag[0] == drag[1]
    T(G, '끌기·크기 조절 = 바탕', g5, {'새 판': drag[0], '바탕': drag[1]})
    ok = g1 and g2 and g3 and g4 and g5 and not p.errs
    if p.errs:
        T(G, 'JS 오류', False, p.errs[:3])
    p.close()
    return ok


def b10(br, src, base_src, tag):
    G = 'B10'
    CMP = {'cX1': {'id': 'cX1', 'name': '관문 비교', 'cols': [{'law': '특허법', 'k': '제3조'}]}}
    out = {}
    for which, s in (('new', src), ('base', base_src)):
        p = page(br, tag + which, s, PC, ls={'jopangi.compare': CMP})
        jo(p, '제3조')
        out[which] = p.ev("""() => { const m = document.querySelector('#slot .main'); const c3 = m.querySelector('.thwrap.c3');
          return { thbot: !!document.getElementById('thbot'), chip: m.querySelectorAll('.chip.c-theme').length, lab: [...m.querySelectorAll('.conn .k')].map(e => __TM.txt(e)), c3: c3 ? c3.outerHTML : null, cmp: localStorage.getItem('jopangi.compare') }; }""")
        p.close()
    n, b = out['new'], out['base']
    g1 = not n['thbot'] and n['chip'] == 0 and '🧩 테마·비교' not in n['lab'] and b['thbot'] and b['chip'] >= 1
    T(G, '옛 「🧩 테마·비교 / ＋ 비교 만들기」 줄 0(바탕엔 있음)', g1, {'새 판': [n['thbot'], n['chip'], n['lab']], '바탕': [b['thbot'], b['chip'], b['lab']]})
    g2 = n['c3'] == b['c3'] and n['c3'] is not None
    T(G, '「3법 비교」 패널 = 바탕(outerHTML)', g2, {'같음': n['c3'] == b['c3'], '있음': n['c3'] is not None})
    g3 = json.loads(n['cmp'] or '{}') == CMP == json.loads(b['cmp'] or '{}')
    T(G, 'jopangi.compare 무변', g3, n['cmp'])
    return g1 and g2 and g3


BOOK = r"""async ([page, ctx]) => { closeAllPops(true); window.__saved = null; viewCanvas.jari.book8({ book: 'patent_hr8', page: page }, null, ctx ? { save: x => { window.__saved = x; } } : undefined);
  for (let i = 0; i < 300; i++){ const w = POPS.find(x => x._pk === 'cv|book|patent_hr8'); if (w && w.querySelector('.cv-bookpg canvas')) break; await __TM.wait(50); } await __TM.wait(400); return !!POPS.find(x => x._pk === 'cv|book|patent_hr8'); }"""
BW = "() => POPS.find(x => x._pk === 'cv|book|patent_hr8')"


def b11(br, src, tag):
    G = 'B11'
    ok = True
    p = page(br, tag, src, PC)
    opened = p.ev(BOOK, [300, True])
    for _ in range(40):
        if p.ev("() => { const w = POPS.find(x => x._pk === 'cv|book|patent_hr8'); return !!(w && w.querySelector('.cv-bs input')); }"):
            break
        p.wait(100)
    c = p.ev("() => { const w = POPS.find(x => x._pk === 'cv|book|patent_hr8'); const i = w && w.querySelector('.cv-booknav .cv-bs input'), g = w && w.querySelector('.cv-bs .cv-bsgo'); return i ? { h: Math.round(i.getBoundingClientRect().height), w: Math.round(i.getBoundingClientRect().width), go: __RB.hitBox(g), pk: !!w.querySelector('[data-pk]') } : null; }")
    g1 = opened and bool(c) and c['h'] == 28 and c['w'] <= 260 and c['go']['h'] >= 36 and c['go']['w'] >= 36 and c['pk']
    T(G, '칸(머리 아래 · input 28 · ≤ 260 · 🔍 ≥ 36 · 📍 찍기 그대로)', g1, c)
    srch = lambda q: p.ev("""async q => { const w = POPS.find(x => x._pk === 'cv|book|patent_hr8'); const i = w.querySelector('.cv-bs input'); i.value = q; w.querySelector('.cv-bs .cv-bsgo').click(); await __TM.wait(300);
      const L = w.querySelector('.cv-bsres'); return { hid: L.hidden, hd: __TM.txt(L.querySelector('.cv-bshd')), pg: [...L.querySelectorAll('.cv-bspg')].map(e => __TM.txt(e)), sn: [...L.querySelectorAll('.cv-bssn')].map(e => __TM.txt(e)), mk: [...L.querySelectorAll('.cv-bssn mark')].map(e => __TM.txt(e)) }; }""", q)
    r = srch('보정을 무효로')
    g2 = not r['hid'] and r['hd'].startswith('「보정을 무효로」 총 2쪽 · 3곳') and r['pg'] == ['p.45 PDF 55 · 2곳', 'p.766 PDF 776 · 1곳'] and r['mk'] == [Q_BOOK] * 3
    T(G, '「보정을 무효로」 → 총 2쪽 · 3곳(공백 뺀 부분 문자열 · 조각 = 앞 14 · mark · 뒤 14)', g2, r)
    a = p.ev("() => __RB.hitOn(POPS.find(x => x._pk === 'cv|book|patent_hr8').querySelector('.cv-bssn'))")
    p.press(a, 400)
    for _ in range(60):
        if p.ev("() => POPS.find(x => x._pk === 'cv|book|patent_hr8').querySelectorAll('.cv-bshit').length > 0"):
            break
        p.wait(100)
    bx = p.ev("""() => { const w = POPS.find(x => x._pk === 'cv|book|patent_hr8'); const hs = [...w.querySelectorAll('.cv-bookpg .cv-bshit')]; const cs = hs[0] ? getComputedStyle(hs[0]) : null;
      return { p: w._cvb.st.p, k: [...new Set(hs.map(h => h.dataset.k))].length, cur: hs.filter(h => h.classList.contains('cur')).map(h => h.dataset.k), pe: cs && cs.pointerEvents, z: cs && cs.zIndex, one: __TM.txt(w.querySelector('.cv-bsone')), list: !!w.querySelector('.cv-bslist') }; }""")
    g3 = bx['p'] == 55 and bx['k'] == 2 and bx['cur'] == ['0'] and bx['pe'] == 'none' and bx['z'] == '2'
    T(G, '조각 누름 → 쪽 55 이동 + 노란 상자 2(누른 곳 주황 테 · 누름 없음 · z 2)', g3, bx)
    g4 = bx['one'] == '1/3곳 · p.45 목록 ▾' and not bx['list']
    T(G, '목록 접힘 = 한 줄 「k/M곳 · p.N 목록 ▾」', g4, bx['one'])
    p.ev("() => POPS.find(x => x._pk === 'cv|book|patent_hr8').querySelector('[data-nx]').click()")
    p.wait(900)
    nx = p.ev("() => { const w = POPS.find(x => x._pk === 'cv|book|patent_hr8'); return [w._cvb.st.p, w.querySelectorAll('.cv-bshit').length]; }")
    p.ev("() => POPS.find(x => x._pk === 'cv|book|patent_hr8').querySelector('[data-pv]').click()")
    p.wait(1200)
    pv = p.ev("() => { const w = POPS.find(x => x._pk === 'cv|book|patent_hr8'); return [w._cvb.st.p, [...new Set([...w.querySelectorAll('.cv-bshit')].map(h => h.dataset.k))].length]; }")
    g5 = nx == [56, 0] and pv[0] == 55 and pv[1] == 2
    T(G, '◀▶ 넘기면 그 쪽 상자만(56 = 0 · 55 = 2)', g5, {'▶': nx, '◀': pv})
    # 찍기 유지 — 📍 찍기 → 끌어 상자 → 이 자리 저장 = 부른 쪽 저장
    p.ev("() => POPS.find(x => x._pk === 'cv|book|patent_hr8').querySelector('[data-pk]').click()")
    p.wait(300)
    ov = p.ev("""() => { const w = POPS.find(x => x._pk === 'cv|book|patent_hr8'), o = w.querySelector('.cv-pickov'); if (!o) return null; const r = o.getBoundingClientRect(), pr = w.getBoundingClientRect(), nav = w.querySelector('.cv-booknav').getBoundingClientRect();
      const top = Math.max(r.top, nav.bottom) + 30, bot = Math.min(r.bottom, pr.bottom) - 30; if (bot - top < 80) return null; const y = top + (bot - top) * 0.3; return { x: r.left + r.width * 0.3, y: y, w: r.width, at: document.elementFromPoint(r.left + r.width * 0.3, y) === o }; }""")
    if ov:
        p.pg.mouse.move(ov['x'], ov['y'])
        p.pg.mouse.down()
        p.pg.mouse.move(ov['x'] + 120, ov['y'] + 50, steps=6)
        p.pg.mouse.up()
        p.wait(300)
    sv = p.ev("() => { const w = POPS.find(x => x._pk === 'cv|book|patent_hr8'); const b = w && w.querySelector('[data-sv]'); return b ? __RB.hitOn(b) : null; }")
    p.press(sv, 600)
    saved = p.ev("() => window.__saved")
    g6 = bool(ov) and bool(saved) and saved.get('p') == 55 and len(saved.get('r') or []) == 4
    T(G, '찍기 유지(📍 찍기 → 끌기 → 이 자리 저장 = 부른 쪽 저장)', g6, {'덮개': bool(ov), '저장': saved})
    p.ev(BOOK, [300, False])
    for _ in range(40):
        if p.ev("() => { const w = POPS.find(x => x._pk === 'cv|book|patent_hr8'); return !!(w && w.querySelector('.cv-bs input')); }"):
            break
        p.wait(100)
    r1 = srch('보')
    g7 = r1['hid']
    T(G, '한 글자 X(목록 없음)', g7, r1)
    st = p.ev("""async () => { const w = POPS.find(x => x._pk === 'cv|book|patent_hr8'); const nav = w.querySelector('.cv-booknav'); w.scrollTop = 600; await __TM.wait(200);
      const r = w.getBoundingClientRect(), b = w.querySelector('.cv-bs input').getBoundingClientRect(); return { pos: getComputedStyle(nav).position, inNav: !!nav.querySelector('.cv-bs'), sc: w.scrollTop, vis: b.top >= r.top - 1 && b.bottom <= r.bottom + 1 }; }""")
    g8 = st['pos'] == 'sticky' and st['inNav'] and st['vis'] and st['sc'] > 0
    T(G, 'sticky — 검색칸 = 머리(.cv-booknav · sticky) 안 · 쪽을 내려도 창 안에 보임', g8, st)
    ok = ok and g1 and g2 and g3 and g4 and g5 and g6 and g7 and g8
    if p.errs:
        ok = False
        T(G, 'JS 오류', False, p.errs[:3])
    p.close()
    q = page(br, 'none:' + tag, src, PC)
    q.ev(BOOK, [300, True])
    q.wait(1500)
    n0 = q.ev("() => { const w = POPS.find(x => x._pk === 'cv|book|patent_hr8'); return w ? { bs: !!w.querySelector('.cv-bs'), canvas: !!w.querySelector('.cv-bookpg canvas') } : null; }")
    g9 = bool(n0) and not n0['bs'] and n0['canvas']
    T(G, '쪽 글 404 → 칸 0(교재 창은 그대로)', g9, n0)
    other = q.ev("""async () => { closeAllPops(true); viewCanvas.book({ book: '핵심', page: 20 }, null, null); for (let i = 0; i < 200; i++){ const w = POPS.find(x => x._pk === 'cv|book|minso_hs'); if (w && (w.querySelector('.cv-bookpg canvas') || w.querySelector('.cv-card'))) break; await __TM.wait(50); }
      const w = POPS.find(x => x._pk === 'cv|book|minso_hs'); return w ? { bs: !!w.querySelector('.cv-bs'), nav: !!w.querySelector('.cv-booknav') } : null; }""")
    g10 = bool(other) and not other['bs']
    T(G, '다른 교재 창(핵심 민소) DOM 에 검색칸 없음', g10, other)
    q.close()
    return ok and g9 and g10


def b12(br, src, base_src, tag):
    G = 'B12'
    p = page(br, 'none:' + tag, src, PC)
    jo(p, '제3조')
    st = p.ev("() => ({ st: typeof TM === 'object' ? TM.st : null, btn: (() => { const b = document.querySelector('.jtbar .tmtg'); return b ? { t: __TM.txt(b), dis: b.disabled } : null; })(), jo: (() => { const b = document.querySelector('.jomt .tmjo'); return b ? { t: __TM.txt(b), c: __TM.hex(getComputedStyle(b).color) } : null; })() })")
    g1 = st['st'] == 'none' and st['btn'] == {'t': '테마 0', 'dis': True} and st['jo'] == {'t': '테마 0', 'c': '#9ca3af'}
    T(G, '재료 404 → 서랍 「테마 0」 · 조문 「테마 0」 회색', g1, st)
    n0 = p.ev("() => POPS.length")
    for sel in ('.jomt .tmjo', '.jtbar .tmtg'):
        a = at(p, sel)
        if a:
            p.press(a, 500)
    n1 = p.ev("() => POPS.length")
    err = p.ev("() => ({ toast: [...document.querySelectorAll('#toasts .toast')].map(t => __TM.txt(t)), err: __RB.errs() })")
    g2 = n0 == n1 == 0 and not err['toast'] and not err['err'] and not p.errs
    T(G, '창 안 뜸 · 오류 문구 0', g2, {'창': [n0, n1], '문구': err})
    tree = p.ev("() => __TM.treeSkel()")
    jomt = p.ev("() => { const m = document.querySelector('.jomt').cloneNode(true); m.querySelectorAll('.tmjo').forEach(x => x.remove()); return m.outerHTML; }")
    pb = page(br, 'none:' + tag + 'B', base_src, PC)
    jo(pb, '제3조')
    tree_b = pb.ev("() => document.querySelector('#slot .tree').outerHTML")
    jomt_b = pb.ev("() => document.querySelector('.jomt').outerHTML")
    pb.close()
    g3 = tree == tree_b and jomt == jomt_b
    T(G, '나머지 DOM = 바탕(서랍 · 모드 줄 — 테마 글자·점 빼고)', g3, {'서랍': tree == tree_b, '모드 줄': jomt == jomt_b})
    p.close()
    return g1 and g2 and g3


# ── B-13 회귀 — 같은 폴더 하네스를 새 판 · 바탕(cedc251) 두 번 돌려 칸마다 견줌(바탕 PASS → 새 판 FAIL = 회귀) · 나머지 조판기 사슬 = 합칠 때 본 세션 ──
REGS = (('revfix0929b', '_harness_jo_revfix0929b.py'), ('revfix0930', '_harness_jo_revfix0930.py'))
REG_REST = ('book8', 'cardfix', 'cvfind', 'gaek_mbsame', 'gaek_uid', 'hdrfold', 'joscreen', 'joscreen0929', 'markfix', 'p8sol', 'p8up', 'revfix0928', 'revfix0928night',
            'revfix0928pm', 'revfix0929', 'toc_fuse', 'toc_fuse_add1', 'uid_add3', 'uidmbs2', 'wonmun', '동기화 jo')
# 뜻한 변경 — 이 지시서가 바꾼 것을 옛 하네스가 옛 꼴로 잰 칸(이름 앞머리 · 까닭 · 잣대 함수(새 판 로그) 없으면 None)
def _cell(raw, name):
    """옛 하네스 새 판 로그에서 그 칸 값(JSON 이면 풀어서) — 없으면 None"""
    for ln in raw.splitlines():
        m = re.match(r'\s*(PASS|FAIL)\s*\|\s*(.+?)\s\|\s(.*)$', ln)
        if m and m.group(2).strip() == name:
            try:
                return json.loads(m.group(3))
            except Exception:
                return m.group(3)
    return None


def _exp_step(raw):
    """접기1 = 바탕 그대로 + 뒤에 「테마 N」 하나만 더"""
    try:
        ka, kb = _cell(raw, 'B8 · PC 접기1 = 착수 판')
        return len(ka) == len(kb) + 1 and ka[:-1] == kb and str(ka[-1][0]).startswith('테마 ')
    except Exception:
        return False


def _exp_move(g, dn):
    """새로 생긴 흠 = 이름만 바뀐 「이동 ↗」 단추 하나(바탕 「뷰로 이동 ↗」 도 작았다 · 없어짐 목록이 이름을 찍으면 거기 있어야)"""
    def f(raw):
        v = _cell(raw, '%s · %s 조문 팝업 새로 생긴 흠 0' % (g, dn))
        gone = v.get('없어짐') if isinstance(v, dict) else None
        return isinstance(v, dict) and v.get('새로') == ['small:button.plgb.tmgo:이동 ↗'] and (not isinstance(gone, list) or 'small:button.plgb:뷰로 이동 ↗' in gone)
    return f


def _exp_only(name, sig):
    """그 칸의 새로 생긴 흠 = 지시서가 정한 그 하나뿐"""
    def f(raw):
        v = _cell(raw, name)
        return isinstance(v, dict) and v.get('새로') == [sig]
    return f


def _exp_hdbtn(raw):
    """팝업 머리 단추 = 바탕과 같은 단추(글자 차례) · 높이 = A-7 틀 값(12px · 줄 1.5 · 위아래 2px · 테 1px = 24)"""
    try:
        ka, kb = _cell(raw, 'B5 · PC 팝업 머리 단추 = 착수 HEAD')
        return [x[0] for x in ka] == [x[0] for x in kb] and all(round(x[2]) == 24 for x in ka)
    except Exception:
        return False


def _exp_fold(raw):
    """세 법 접기 글자·동작 = 바탕(칸 값 셋째 참) — DOM 차이(거름 점 · 특허 「테마 N」)는 이 하네스 B1 이 빼고 = 바탕으로 잰다"""
    try:
        v = _cell(raw, 'B6 · 특허 · 상표 · 디보 서랍 DOM · 접기 글자·동작 = 착수 HEAD')
        return len(v) == 3 and all(x[2] is True for x in v)
    except Exception:
        return False


def _exp_pinwin(raw):
    """교재 자리 창 = 바탕보다 머리만큼 큼(A-7 머리 31.4 → 39px) — 자리마다 위나 아래 한쪽 끝은 바탕 그대로 · 큰 만큼(d)은 모든 자리에서 같고 ≤ 12"""
    try:
        v = _cell(raw, 'B8 · 폰 390 교재 자리 창 = 착수 HEAD(±2 · 칩 y 300→420→600→420)')
        ds = []
        for a, b in zip(v['new'], v['base']):
            if abs(a[0] - b[0]) <= 1:
                ds.append(a[1] - b[1])
            elif abs(a[1] - b[1]) <= 1:
                ds.append(b[0] - a[0])
            else:
                return False
        return len(ds) == 4 and max(ds) - min(ds) <= 1 and 0 < min(ds) and max(ds) <= 12
    except Exception:
        return False


EXPECT = {'revfix0929b': (
    ('B8 · PC 접기1 = 착수 판', 'A-1 서랍 머리 「테마 N」 = 접기1 꼴(.uzstep.jstep) 하나 더 — 접기1 크기·자리는 바탕 그대로(잣대: 새 판 목록 = 바탕 목록 + 「테마 N」 하나)', _exp_step),
    ('B12 · 폰390 조문 팝업 새로 생긴 흠 0', 'A-7 머리 「뷰로 이동 ↗」 → 「이동 ↗」(같은 단추 · 글자·색만 · 바탕에서도 작던 단추 — 잣대: 새로 = 그 단추 하나)', _exp_move('B12', '폰390')),
    ('B12 · iPad834 조문 팝업 새로 생긴 흠 0', 'A-7 머리 「뷰로 이동 ↗」 → 「이동 ↗」(위와 같음)', _exp_move('B12', 'iPad834')),
    ('B12 · 폰390 조문 화면(서랍) 새로 생긴 흠 0', 'fix1 A-34-3 거름 점 누름 = 높이 36 · 가로 = 이웃 누름과 안 겹치는 만큼(14) — 지시서가 정한 값(잣대: 새로 = 그 점 하나)', _exp_only('B12 · 폰390 조문 화면(서랍) 새로 생긴 흠 0', 'small:i.bkmk.dot:')),
    ('B12 · iPad834 조문 화면(서랍) 새로 생긴 흠 0', 'fix1 A-34-3 거름 점 가로 14(위와 같음)', _exp_only('B12 · iPad834 조문 화면(서랍) 새로 생긴 흠 0', 'small:i.bkmk.dot:'))),
    'revfix0930': (
    ('B5 · PC 팝업 머리 단추 = 착수 HEAD', 'A-7 팝업 머리 단추 = 민법 oxwin 값(12px 700 · 테 #d1d5db · 둥글기 6 · 2px 8px) — 크기가 틀 값으로(잣대: 같은 단추 · 높이 24)', _exp_hdbtn),
    ('B6 · 특허 · 상표 · 디보 서랍 DOM · 접기 글자·동작 = 착수 HEAD', 'A-1 서랍 머리 거름 점(세 법) + 「테마 N」(특허) — 접기 글자·동작 = 바탕(잣대) · 나머지 DOM = 바탕은 이 하네스 B1(특허 · 상표 · 디보)이 잰다', _exp_fold),
    ('B8 · 폰 390 교재 자리 창 = 착수 HEAD', 'A-7 머리(여백 7px 10px · 밑줄 1px · 제목 13px) = 창 머리 31.4 → 39px — 창이 그만큼 큼(잣대: 한쪽 끝 그대로 · 모든 자리 같은 d ≤ 12)', _exp_pinwin),
    ('B9 · 폰390 조문 팝업 새로 생긴 흠 0', 'A-7 「뷰로 이동 ↗」 → 「이동 ↗」(같은 단추 · 바탕 흠이 새 이름으로 · ✕ 는 틀 값으로 커져 흠에서 빠짐)', _exp_move('B9', '폰390')),
    ('B9 · iPad834 조문 팝업 새로 생긴 흠 0', 'A-7 「뷰로 이동 ↗」 → 「이동 ↗」(위와 같음)', _exp_move('B9', 'iPad834'))) + tuple(
    ('B9 · %s 조문 화면(%s) 새로 생긴 흠 0' % (dn, w), 'fix1 A-34-3 거름 점 누름 = 높이 36 · 가로 = 이웃 누름과 안 겹치는 만큼(14) — 지시서가 정한 값(잣대: 새로 = 그 점 하나)',
     _exp_only('B9 · %s 조문 화면(%s) 새로 생긴 흠 0' % (dn, w), 'small:i.bkmk.dot:')) for dn in ('폰390', 'iPad834') for w in ('서랍', '민소 서랍'))}


def reg_parse(txt):
    out = {}
    for ln in txt.splitlines():
        m = re.match(r'\s*(PASS|FAIL)\s*\|\s*(.+?)(?:\s\|\s|$)', ln)
        if m:
            out.setdefault(m.group(2).strip(), []).append(m.group(1))
    return out


def reg_run(fn, app_text, which):
    d = os.path.join(TMP0, 'reg', fn.replace('.py', '') + '_' + which)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    af = os.path.join(d, 'app.html')
    open(af, 'wb').write(app_text.encode('utf-8'))
    cmd = [sys.executable, os.path.join(HERE, fn), '--new', af, '--eng', 'chromium', '--res', os.path.join(d, 'result.txt')]
    if '--vendor' in sys.argv:
        cmd += ['--vendor', ARG('--vendor')]
    t0 = time.time()
    try:
        cp = subprocess.run(cmd, capture_output=True, timeout=3000, cwd=d, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
        out = cp.stdout.decode('utf-8', 'replace') + '\n' + cp.stderr.decode('utf-8', 'replace')
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b'').decode('utf-8', 'replace') + '\n[시간 넘김]'
    out = out.replace(d, '<TMP>')
    open(os.path.join(TMP0, 'reg', fn.replace('.py', '') + '_' + which + '.log'), 'w', encoding='utf-8').write(out)
    return reg_parse(out), '%.0f초' % (time.time() - t0), out


def b13(src, base_src):
    G = 'B13'
    ok = True
    for name, fn in REGS:
        rn, tn, raw = reg_run(fn, src, 'new')
        rb, tb, _ = reg_run(fn, base_src, 'base')
        if not rn and not rb:
            N(G, name, '안 돔(PASS/FAIL 줄 0) · 로그 ' + os.path.join(TMP0, 'reg'))
            continue
        reg0 = sorted(k for k in rn if 'FAIL' in rn[k] and k in rb and 'FAIL' not in rb[k])
        reg0 += sorted(k for k in rb if k not in rn and 'PASS' in rb[k] and 'FAIL' not in rb[k])
        exp = EXPECT.get(name, ())
        why = lambda k: next(((w, v) for p_, w, v in exp if k.startswith(p_)), None)
        meant = [(k, why(k)[0]) for k in reg0 if why(k) and (why(k)[1] is None or why(k)[1](raw))]
        reg = [k for k in reg0 if k not in dict(meant)]
        g = not reg
        ok = ok and g
        T(G, '%s 회귀 0(바탕 PASS → 새 판 FAIL 인 칸 0)' % name, g,
          {'새 판': '%d PASS / %d FAIL' % (sum(v.count('PASS') for v in rn.values()), sum(v.count('FAIL') for v in rn.values())),
           '바탕': '%d PASS / %d FAIL' % (sum(v.count('PASS') for v in rb.values()), sum(v.count('FAIL') for v in rb.values())),
           '회귀': reg[:8], '뜻한 변경': meant, '둘 다 FAIL': sorted(k for k in rn if 'FAIL' in rn[k] and 'FAIL' in rb.get(k, []))[:6], '시간': [tn, tb]})
    N(G, '나머지 조판기 사슬 + WebKit 터치 칸 + 동기화 jo', 'N: 필요 — 합칠 때 본 세션(' + ' · '.join(REG_REST) + ')')
    N(G, 'qa_baseline 저장본(_qa_chain compare)', '바탕 cedc251 에 _qa_chain 없음 → 안 함')
    return ok


# ── B-14 화면 훑기(규칙 60) — 서랍(테마 · 거름) · 테마 창 · 목록 창 · 연결 창 · 조문 팝업 · 메모 창 · 8판 창 — 폰 · 아이패드 · PC · 새 판 흠 − 바탕 흠 = 0 ──
def sweep_screens(br, src, tag, dev, base=False):
    p = page(br, tag, src, dev)
    touch = dev in (PHONE, PAD)
    sw = lambda sel: p.ev("a => __TM.sweep(a[0], a[1])", [sel, touch])
    out = {}
    jo(p, '제3조')
    if not base:
        p.ev("() => document.querySelector('.jtbar .tmtg').click()")
        p.idle(300)
    out['서랍 테마'] = sw('#slot .tree')
    if not base:
        p.ev("() => { document.querySelector('.jtbar .tmtg').click(); }")
        p.idle(300)
        p.ev("() => { tmDotSet(2); render(); }")
        p.idle(300)
    out['서랍 거름'] = sw('#slot .tree')
    if not base:
        p.ev("() => { tmDotSet(0); render(); }")
        p.idle(300)
        for k, js, key in (('테마 창', "() => tmWin('t02', null)", 'theme|t02'), ('목록 창', "() => tmListWin('t02', null)", 'themelist|t02'),
                           ('연결 창', "() => tmOfWin('특허법', '제3조', null)", 'themeof|')):
            p.ev("() => closeAllPops(true)")
            p.ev(js)
            p.wait(700)
            p.ev("k => { const w = __TM.pop(k); if (w) w.setAttribute('data-sw', '1'); }", key)
            out[k] = sw('[data-sw="1"]')
            p.ev("() => document.querySelectorAll('[data-sw]').forEach(x => x.removeAttribute('data-sw'))")
    p.ev("() => closeAllPops(true)")
    a = p.ev("() => { const l = document.querySelector('#slot .main .box .wmlk'); return l ? __RB.hitOn(l) : null; }")
    p.press(a, 1500)
    p.ev("() => { const w = POPS.filter(x => (x._pk || '').indexOf('jo|') === 0).pop(); if (w) w.setAttribute('data-sw', '1'); }")
    out['조문 팝업'] = sw('[data-sw="1"]')
    p.ev("() => { document.querySelectorAll('[data-sw]').forEach(x => x.removeAttribute('data-sw')); closeAllPops(true); }")
    p.ev("async () => { pitEdit('jo|특허법:제3조', '0', 0, '틀', null); await __TM.wait(300); POPS[POPS.length - 1].setAttribute('data-sw', '1'); }")
    out['메모 창'] = sw('[data-sw="1"]')
    p.ev("() => { document.querySelectorAll('[data-sw]').forEach(x => x.removeAttribute('data-sw')); closeAllPops(true); }")
    p.ev(BOOK, [300, True])
    if not base:
        for _ in range(40):
            if p.ev("() => { const w = POPS.find(x => x._pk === 'cv|book|patent_hr8'); return !!(w && w.querySelector('.cv-bs input')); }"):
                break
            p.wait(100)
        p.ev("""async () => { const w = POPS.find(x => x._pk === 'cv|book|patent_hr8'); const i = w.querySelector('.cv-bs input'); i.value = '보정을 무효로'; w.querySelector('.cv-bs .cv-bsgo').click(); await __TM.wait(300); }""")
    p.ev("() => { const w = POPS.find(x => x._pk === 'cv|book|patent_hr8'); if (w) w.setAttribute('data-sw', '1'); }")
    out['8판 창'] = sw('[data-sw="1"]')
    errs = p.errs[:]
    p.close()
    return out, errs


# 글자만 바뀐 같은 요소(지시서가 글자를 정했다) — 바탕 흠과 같은 흠으로 센다(바탕에서도 작던 것 · 이 판이 새로 만든 흠 아님)
B14_SAME = {'small:button.tool.jckf:주체 # ▾': 'small:button.tool.jckf:전체 # ▾',   # A-1 거름 점 켠 칩 글자 「주체 175 ▾」 = 바탕 「전체 268 ▾」 칩 그대로
            'small:button.plgb.tmgo:이동 ↗': 'small:button.plgb:뷰로 이동 ↗'}        # A-7 「뷰로 이동 ↗」 → 「이동 ↗」(같은 단추 · 글자·색만)


# 지시서가 값을 정한 것 — 흠으로 세지 않되 칸마다 적는다(fix1 A-34-3: 거름 점 누름 = 높이 36 · 가로는 이웃 누름과 안 겹치는 만큼 → 14 · 결과 절에 값)
ACCEPT = {'small:i.bkmk.dot:': 'fix1 A-34-3 거름 점 누름 가로 = 이웃과 안 겹치는 만큼(14) · 높이 36'}


def b14(br, src, base_src, tag):
    G = 'B14'
    ok = True
    for dn, dev in (('폰390', PHONE), ('iPad834', PAD), ('PC', PC2)):
        n, en = sweep_screens(br, src, tag + 'N' + dn, dev)
        b, eb = sweep_screens(br, base_src, tag + 'B' + dn, dev, base=True)
        for scr in n:
            nn, bb = {B14_SAME.get(x, x) for x in n[scr]}, set(b.get(scr, []))
            new = sorted(nn - bb - set(ACCEPT))
            good = not new
            ok = ok and good
            T(G, '%s %s 새로 생긴 흠 0' % (dn, scr), good, {'새로': new[:8], '없어짐': sorted(bb - nn)[:4], '남은(바탕에도)': len(nn & bb),
                                                      '글자만 바뀐 같은 요소': sorted(set(n[scr]) & set(B14_SAME)), '지시서가 정한 값': sorted(nn & set(ACCEPT))})
        if en:
            ok = False
            T(G, '%s JS 오류' % dn, False, en[:3])
    return ok


# ════════════════════════ _task_jo_theme_fix1 — B15~B24(8d1383d 위 고침 여덟 · 헛잣대 = 8d1383d 에서 B15~B22 FAIL) ════════════════════════
FW = {'bg': 'rgb(255, 255, 255)', 'bd': 'rgb(203, 213, 225)', 'bw': '1px', 'rad': '12px', 'sh': 'rgba(0, 0, 0, 0.28) 0px 12px 40px 0px', 'hbg': 'rgb(248, 250, 252)',
      'hbd': 'rgb(229, 231, 235)', 'hbw': '1px', 'ts': '13px', 'tw': '800', 'tc': 'rgb(17, 24, 39)', 'xc': 'rgb(107, 114, 128)', 'xbd': 'rgb(209, 213, 219)', 'xbw': '1px', 'xr': '6px', 'xbg': 'rgb(255, 255, 255)'}
WINS = [('🔗 연결 창', 'cflw'), ('원문 창 마크업', 'mk'), ('원문 창 정오문제', 'jp'), ('원문 창 인용', 'ci')]
# 창 하나만 열고 [data-fw] 표 — 연결 창 = cfLinkWin(카드 열쇠) · 원문 창 = 바탕 상태값(S.mkWin · S.joPanel · S.ciWin)으로 그리기(render 는 겹 부름을 버리므로 뜰 때까지 다시 부름)
OPENW = r"""async (k) => { closeAllPops(true); S.mkWin = false; S.joPanel = false; S.ciWin = ''; document.querySelectorAll('[data-fw]').forEach(x => x.removeAttribute('data-fw'));
  const find = () => k === 'cflw' ? POPS.find(x => x._cflw && (x._pk || '').indexOf('cflw|') === 0) : wmWinOf(k);
  if (k === 'cflw') cfLinkWin('T1552093', null);
  else { if (k === 'mk') S.mkWin = true; if (k === 'jp') S.joPanel = true; if (k === 'ci'){ S.ciWin = S.law + ':' + S.jo; S.ciKind = 'in'; } }
  for (let i = 0; i < 60; i++){ const w = find(); if (w){ w.setAttribute('data-fw', '1'); await __TM.wait(150); return true; } if (k !== 'cflw' && i % 8 === 0) render(); await __TM.wait(100); }
  return false; }"""
CLOSEW = "async () => { closeAllPops(true); S.mkWin = false; S.joPanel = false; S.ciWin = ''; await __TM.wait(50); }"


def b15(br, src, tag):
    """A-31 테마 창 글 속 조 링크 = 본문 링크(.wml .wmlk) 꾸밈 그대로 · 글자색 = 그 run 색 · 누르면 popJo"""
    G = 'B15'
    p = page(br, tag, src, PC)
    jo(p, '제3조')
    body = p.ev("() => __TM.deco(document.querySelector('#slot .main .wml .wmlk'))")
    p.ev("() => tmWin('t02', null)")
    p.wait(500)
    th = p.ev("() => { const w = __TM.pop('theme|t02'); return [...w.querySelectorAll('.thl a.wmlk')].map(a => Object.assign(__TM.deco(a), { run: __TM.hex(a.closest('.thl > span, .thl span[style]') ? getComputedStyle(a.closest('.thl > span, .thl span[style]')).color : ''), me: __TM.hex(getComputedStyle(a).color), k: a.dataset.law + ':' + a.dataset.k })); }")
    keys = ('line', 'style', 'dcol', 'th', 'off', 'cur')
    same = bool(body) and bool(th) and all(all(x[k] == body[k] for k in keys) for x in th)
    runc = bool(th) and all(x['me'] == x['run'] for x in th)
    g1 = same and runc and body['line'] == 'underline' and body['style'] == 'dotted' and body['cur'] == 'pointer'
    T(G, '테마 창 .thl a.wmlk 꾸밈 = 본문 .wml .wmlk(밑줄 · 점선 · 색 · 굵기 · 간격 · 손가락) · 글자색 = 그 run 색', g1,
      {'본문': body, '테마 링크 수': len(th or []), '첫 링크': (th or [None])[0], '다른 것': [x['k'] for x in (th or []) if not all(x[k] == body[k] for k in keys) or x['me'] != x['run']][:4]})
    a = p.ev("() => { const w = __TM.pop('theme|t02'); const l = [...w.querySelectorAll('.thl .wmlk')].find(x => x.dataset.k === '제16조' && x.dataset.law === '특허법'); return l ? __RB.hitOn(l) : null; }")
    p.press(a, 1500)
    g2 = p.ev("() => !!POPS.find(x => x._pk === 'jo|특허법|제16조')")
    T(G, '누르면 popJo(jo|특허법|제16조 · 바탕과 같음)', g2, g2)
    ok = g1 and g2 and not p.errs
    if p.errs:
        T(G, 'JS 오류', False, p.errs[:3])
    p.close()
    return ok


def b16(br, src, tag):
    """A-32 다른 법 머리 — 두 글자(시규·민소) = 늘 머리 · 한 글자(상·디) 앞 한글 = 링크 없음 · 머리 없는 수 = 특허법 · 실제 재료 모양(B3) 링크 수 무변"""
    G = 'B16'
    p = page(br, tag, src, PC)
    jo(p, '제3조')
    p.ev("() => tmWin('t01', null)")
    p.wait(500)
    got = p.ev("t => { const w = __TM.pop('theme|t01'); const l = [...w.querySelectorAll('.thl')].find(x => x.textContent.indexOf(t) >= 0); return l ? [...l.querySelectorAll('.wmlk')].map(a => [a.textContent, a.dataset.law, a.dataset.k]) : null; }", A32_LINE[:8])
    g1 = got == A32_WANT
    T(G, '「%s」 링크 = 제5조 특허 · 민소16조 → 민사소송법 · (상227조) 상표법 · (디217조) 디자인보호법 · 특226조 특허 / 및시규11조 · 법원은상33조 · 이상5조 · 공백 뒤 시규11조 = 0' % A32_LINE, g1, {'링크': got, '바람': A32_WANT})
    a = p.ev("() => { const w = __TM.pop('theme|t01'); const l = [...w.querySelectorAll('.thl .wmlk')].find(x => x.dataset.law === '민사소송법'); return l ? __RB.hitOn(l) : null; }")
    p.press(a, 1500)
    g2 = p.ev("() => !!POPS.find(x => x._pk === 'jo|민사소송법|제16조')")
    T(G, '「민소16조」 누름 → jo|민사소송법|제16조', g2, g2)
    p.ev("() => closeAllPops(true)")
    p.ev("() => tmWin('t02', null)")
    p.wait(400)
    n2 = p.ev("() => __TM.pop('theme|t02').querySelectorAll('.thl .wmlk').length")
    p.ev("() => tmWin('t03', null)")
    p.wait(400)
    n3 = p.ev("() => __TM.pop('theme|t03').querySelectorAll('.thfig .wmlk').length")
    g3 = n2 == PLANT['t02']['links'] and n3 == PLANT['t03']['links']
    T(G, '실제 재료 모양 회귀 = 본판 B3 조 링크 수 무변(기일기간 %d · 분변분재 svg %d)' % (PLANT['t02']['links'], PLANT['t03']['links']), g3, [n2, n3])
    ok = g1 and g2 and g3 and not p.errs
    if p.errs:
        T(G, 'JS 오류', False, p.errs[:3])
    p.close()
    return ok


def _drag(q, sel):
    """머리 끌기(+80, +40) · 크기 손잡이 끌기(+60, +50) → [자리, 크기]"""
    d = q.ev("""s => { const w = document.querySelector(s); w.style.left = '300px'; w.style.top = '160px'; const h = w.querySelector(':scope > .ph').getBoundingClientRect(), z = w.querySelector(':scope > .prsz');
      return { hx: h.left + 40, hy: h.top + h.height / 2, ok: !!z }; }""", sel)
    q.pg.mouse.move(d['hx'], d['hy'])
    q.pg.mouse.down()
    q.pg.mouse.move(d['hx'] + 80, d['hy'] + 40, steps=5)
    q.pg.mouse.up()
    q.wait(200)
    pos = q.ev("s => { const w = document.querySelector(s); return [Math.round(parseFloat(w.style.left)), Math.round(parseFloat(w.style.top))]; }", sel)
    sz = None
    if d['ok']:
        z = q.ev("s => { const r = document.querySelector(s).querySelector(':scope > .prsz').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }", sel)
        q.pg.mouse.move(z[0], z[1])
        q.pg.mouse.down()
        q.pg.mouse.move(z[0] + 60, z[1] + 50, steps=5)
        q.pg.mouse.up()
        q.wait(200)
        sz = q.ev("s => { const r = document.querySelector(s).getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; }", sel)
    return [pos, sz]


def b17(br, src, prev_src, tag):
    """A-33 🔗 연결 창 · 원문 창 셋 = A-7 틀 값(popShell 10종과 같은 값) · 안쪽(머리 여백 · 끌기 · 본문 바탕 · 폭 · 크기 조절) = 8d1383d"""
    G = 'B17'
    res = {}
    for nm_, s_ in (('new', src), ('prev', prev_src)):
        p = page(br, tag + nm_, s_, PC)
        jo(p, '제6조')
        ref = p.ev("() => { const b = popShell('', '틀', 'frame|ref'); const o = __TM.frame(b.parentNode); closeOne(b.parentNode); return o; }")
        out, dr = {}, {}
        for wn, k in WINS:
            out[wn] = p.ev("() => __TM.frame(document.querySelector('[data-fw]'))") if p.ev(OPENW, k) else None
            if out[wn] and k in ('cflw', 'mk'):
                dr[wn] = _drag(p, '[data-fw]')
        p.ev(CLOSEW)
        res[nm_] = (ref, out, dr, p.errs[:])
        p.close()
    ref, out, dr, errs = res['new']
    _, outp, drp, _ = res['prev']
    bad = {wn: {k: f[k] for k in FW if f[k] != FW[k]} if f else '안 뜸' for wn, f in out.items()}
    g1 = all(v == {} for v in bad.values())
    T(G, '연결 창 · 마크업 · 정오문제 · 인용 창 틀 = §A-33-1 값(테 #cbd5e1 · 12 · 그림자 · 머리 #f8fafc · 밑줄 #e5e7eb · 제목 13 800 #111827 · ✕ = 머리 단추 꼴)', g1, {'어긋남': bad})
    g2 = bool(ref) and all(f and all(f[k] == ref[k] for k in FW) for f in out.values())
    T(G, '네 창 틀 = popShell 틀(본판 B9 값)과 같음', g2, {'popShell': {k: ref[k] for k in ('bd', 'rad', 'hbg', 'tc', 'xbd')} if ref else None})
    inner = {wn: (out[wn] or {}).get('inner') for wn in out}
    innerp = {wn: (outp[wn] or {}).get('inner') for wn in outp}
    g3 = all(inner[wn] and inner[wn] == innerp.get(wn) for wn in inner)
    T(G, '안쪽 = 8d1383d(머리 여백 · 끌기 cursor · 본문 바탕·여백 · 폭 · 크기 손잡이 · 글꼴)', g3, {wn: [inner[wn], innerp.get(wn)] for wn in inner if inner[wn] != innerp.get(wn)} or inner['🔗 연결 창'])
    g4 = dr == drp and len(dr) == 2
    T(G, '끌기 · 크기 조절 = 8d1383d(연결 창 · 마크업 창)', g4, {'새 판': dr, '8d1383d': drp})
    ok = g1 and g2 and g3 and g4 and not errs
    if errs:
        T(G, 'JS 오류', False, errs[:3])
    return ok


HEAD = r"""() => { const b = document.querySelector('.jtbar'), r = b.getBoundingClientRect(), tr = document.querySelector('#slot .tree').getBoundingClientRect();
  const it = ['.jckf', '.tmdot', '.jstep:not(.tmtg)', '.tmtg'].map(s => b.querySelector(s)).filter(Boolean).map(e => { const q = e.getBoundingClientRect(); return { c: e.className.split(' ').pop(), l: Math.round(q.left * 10) / 10, t: Math.round(q.top * 10) / 10, w: Math.round(q.width * 10) / 10, h: Math.round(q.height * 10) / 10, cy: q.top + q.height / 2, r: q.right }; });
  return { h: Math.round(r.height * 10) / 10, it: it, trL: tr.left, trR: tr.right, vw: innerWidth }; }"""
TGT3 = r"""() => { const d = document.querySelector('.jtbar .tmdot'), s = document.querySelector('.jtbar .jstep:not(.tmtg)'), t = document.querySelector('.jtbar .tmtg'); d.scrollIntoView({block: 'center'});
  const f = x => { const a = __RB.tgt(x, ''); return { dw: a.dw, dh: a.dh, steal: a.steal, near: a.near, center: a.center, ex: a.ex }; }; return { step: __TM.txt(s), dot: f(d), stp: f(s), tm: f(t), hb: __RB.hitBox(d) }; }"""


def b18(br, src, base_src, prev_src, tag):
    """A-34 폰·아이패드 서랍 머리 한 줄 · 높이 = 바탕 cedc251 ±1 · 거름 점 누름 높이 ≥ 36 · 둘레 겹침 0(접기 단추 글자 셋 다) · 화면 밖 0 · 거름 점 순환 무변 · PC 무변"""
    G = 'B18'
    ok = True
    for dn, dev in (('폰390', PHONE), ('iPad834', PAD)):
        p = page(br, tag + dn, src, dev)
        jo(p, '제3조')
        pb = page(br, tag + 'B' + dn, base_src, dev)
        jo(pb, '제3조')
        hb = pb.ev("() => Math.round(document.querySelector('.jtbar').getBoundingClientRect().height * 10) / 10")
        pb.close()
        hd = p.ev(HEAD)
        cy0 = hd['it'][0]['cy'] if hd['it'] else 0
        one = len(hd['it']) == 4 and all(abs(x['cy'] - cy0) <= 2 for x in hd['it'])
        g1 = one and abs(hd['h'] - hb) <= 1
        ok = ok and g1
        T(G, '%s 서랍 머리 한 줄(넷 가운데 높이 ±2) · 높이 = 바탕 cedc251 ±1' % dn, g1, {'높이': [hd['h'], hb], '넷': [[x['c'], x['l'], x['t'], x['w'], x['h']] for x in hd['it']]})
        tg = []
        for i in range(3):
            tg.append(p.ev(TGT3))
            p.ev("() => document.querySelector('.jtbar .jstep:not(.tmtg)').click()")
            p.idle(300)
        g2 = all(m['dot']['dh'] >= 36 and m['dot']['center'] and m['dot']['steal'] == 0 and m['dot']['near'] == 0 and m['stp']['steal'] == 0 and m['tm']['steal'] == 0 for m in tg)
        ok = ok and g2
        T(G, '%s 거름 점 누름 높이 ≥ 36 · 가로 %s · 둘레 겹침 0(접기 단추 「%s」 셋 다 · 거름 점·접기·테마 N 가로챔 0)' % (dn, tg[0]['dot']['dw'], ' · '.join(m['step'] for m in tg)), g2,
          [{'접기': m['step'], '점': [m['dot']['dw'], m['dot']['dh'], m['dot']['steal'], m['dot']['near']], '접기 둘레': [m['stp']['dw'], m['stp']['dh'], m['stp']['steal']], '테마 N': [m['tm']['dw'], m['tm']['dh'], m['tm']['steal']]} for m in tg])
        off = [x['c'] for x in hd['it'] if x['l'] < hd['trL'] - 0.5 or x['r'] > min(hd['trR'], hd['vw']) + 0.5]
        g3 = not off
        ok = ok and g3
        T(G, '%s 머리 요소 화면·서랍 밖 0' % dn, g3, off)
        seq = []
        for i in range(4):
            p.press(at(p, '.jtbar .tmdot'), 450)
            seq.append(p.ev("() => __TM.dot().bg"))
        g4 = seq == [BKC[0], BKC[1], BKC[2], '#ffffff']
        ok = ok and g4
        T(G, '%s 거름 점 손가락 네 번 = 파 → 보 → 초 → 빈(본판 B2 무변)' % dn, g4, seq)
        if p.errs:
            ok = False
            T(G, '%s JS 오류' % dn, False, p.errs[:3])
        p.close()
    pc = {}
    for nm_, s_ in (('new', src), ('prev', prev_src)):
        q = page(br, tag + 'pc' + nm_, s_, PC2)
        jo(q, '제3조')
        pc[nm_] = q.ev(HEAD)
        q.close()
    a, b = pc['new'], pc['prev']
    keep = lambda h: [[x['c'], x['t'], x['h']] for x in h['it'] if x['c'] != 'tmdot']
    g5 = a['h'] == b['h'] and keep(a) == keep(b)
    ok = ok and g5
    T(G, 'PC 서랍 머리 = 8d1383d(높이 · 칩·접기·테마 N 줄 자리 — 거름 점만 12 → 8)', g5, {'새 판': [a['h'], keep(a)], '8d1383d': [b['h'], keep(b)]})
    return ok


ROW = r"""(sel) => [...document.querySelectorAll(sel)].filter(__TM.vis).map(r => { const c = getComputedStyle(r), j = r.querySelector('.jno'), jc = getComputedStyle(j), rr = r.getBoundingClientRect(), jr = j.getBoundingClientRect(), em = r.querySelector('em.jcol3').getBoundingClientRect();
  const tail = [...r.children].filter(x => x.matches('.tmx, .tmplus')).reduce((s, x) => s + x.getBoundingClientRect().width + parseFloat(getComputedStyle(x).marginLeft || 0) + parseFloat(c.columnGap || 0), 0);
  return { id: r.dataset.tm, h: Math.round(rr.height), pl: c.paddingLeft, jx: Math.round(jr.left - rr.left), deco: jc.textDecorationLine + ' ' + jc.textDecorationStyle, fs: jc.fontSize, col: jc.color, rad: c.borderTopLeftRadius,
    dots: [...r.querySelectorAll('.bkm3 .bkmk')].map(d => Math.round(d.getBoundingClientRect().width)), emR: Math.round(rr.right - em.right - tail) }; })"""
ROWK = ('h', 'pl', 'jx', 'deco', 'fs', 'col', 'rad', 'dots', 'emR')


def b19(br, src, tag):
    """A-36 같은 테마 — 서랍 줄 ↔ 연결 창 줄 ↔ 찾기 결과 줄: 높이 · 안쪽 13 · 이름 점선 밑줄 · 글자 크기·색 · 점 지름 · 「두N §N」 자리(✕·＋ 칸 빼고) 같음 · ✕/＋ 누름 ≥ 36 · 줄 누름 → 테마 창"""
    G = 'B19'
    ok = True
    for dn, dev in (('PC', PC), ('폰390', PHONE)):
        p = page(br, tag + dn, src, dev)
        jo(p, '제3조')
        p.press(at(p, '.jtbar .tmtg'), 500)
        tree = {r['id']: r for r in p.ev(ROW, '#slot .tree .r.tmr')}
        p.press(at(p, '.jtbar .tmtg'), 500)
        p.ev("() => { closeAllPops(true); tmOfWin('특허법', '제3조', null); }")
        p.wait(500)
        p.ev("() => { const w = document.querySelector('.pop.tmofw'); w.querySelector('.thsrch input').value = '분변'; w.querySelector('.thsrch .tmsgo').click(); }")
        p.wait(400)
        res = p.ev(ROW, '.pop .tmres .r.tmr')
        plus = p.ev("() => { const b = document.querySelector('.pop .tmres .tmplus'); return b ? __RB.hitBox(b) : null; }")
        p.press(p.ev("() => __RB.hitOn(document.querySelector('.pop .tmres .tmplus'))"), 500)
        p.wait(300)
        of = p.ev(ROW, '.pop .tmof .r.tmr')
        x = p.ev("() => { const b = document.querySelector('.pop .tmof .tmx'); return b ? __RB.hitBox(b) : null; }")
        rows = [('연결 창', r) for r in of] + [('찾기 결과', r) for r in res]
        diff = [(w, r['id'], {k: [r[k], tree.get(r['id'], {}).get(k)] for k in ROWK if r[k] != tree.get(r['id'], {}).get(k) and not (k == 'emR' and abs(r[k] - tree.get(r['id'], {}).get(k, -99)) <= 1)}) for w, r in rows]
        diff = [d for d in diff if d[2]]
        g1 = len(of) == 3 and len(res) == 1 and not diff and all(r['pl'] == '13px' and r['deco'] == 'underline dotted' for _, r in rows)
        ok = ok and g1
        T(G, '%s 서랍 줄 = 연결 창 줄 3 = 찾기 결과 줄(높이 · 안쪽 13 · 이름 점선 · 글자 · 점 지름 · 「두N §N」 자리 · 둥글기 0)' % dn, g1, {'다름': diff[:4], '서랍 t01': tree.get('t01'), '창 t01': (of or [None])[0]})
        if p.touch:
            g2 = bool(x) and bool(plus) and x['h'] >= 36 and x['w'] >= 36 and plus['h'] >= 36 and plus['w'] >= 36
            ok = ok and g2
            T(G, '%s ✕ · ＋ 누름 ≥ 36' % dn, g2, {'✕': x and [x['w'], x['h']], '＋': plus and [plus['w'], plus['h']]})
        a = p.ev("() => __RB.hitOn(document.querySelector('.pop .tmof .r.tmr[data-tm=t01] .jno'))")
        p.press(a, 600)
        g3 = bool(p.ev("() => __TM.pop('theme|t01')"))
        ok = ok and g3
        T(G, '%s 연결 창 줄 누름 → 테마 창(무변)' % dn, g3, g3)
        if p.errs:
            ok = False
            T(G, '%s JS 오류' % dn, False, p.errs[:3])
        p.close()
    return ok


def b20(br, src, tag):
    """A-37 거름 점 지름 8 = 조 줄 .bkmk.dot · 켜진 색 = BK_COLOR 셋 · 빈 = 8px 고리"""
    G = 'B20'
    ok = True
    for dn, dev in (('PC', PC), ('폰390', PHONE)):
        p = page(br, tag + dn, src, dev)
        jo(p, '제3조')
        sz = p.ev("() => { const t = document.querySelector('.jtbar .tmdot').getBoundingClientRect(), r = document.querySelector('#slot .tree .r[data-jo] .bkm3 .bkmk.dot').getBoundingClientRect(); return { dot: [t.width, t.height], row: [r.width, r.height] }; }")
        bk = p.ev("() => [BK_COLOR.내용, BK_COLOR.주체, BK_COLOR.기간].map(x => String(x).toLowerCase())")
        st = [p.ev("() => { const d = document.querySelector('.jtbar .tmdot'), c = getComputedStyle(d), r = d.getBoundingClientRect(); return [__TM.hex(c.backgroundColor), __TM.hex(c.borderTopColor), r.width, r.height]; }")]
        for i in range(4):
            p.press(at(p, '.jtbar .tmdot'), 450)
            st.append(p.ev("() => { const d = document.querySelector('.jtbar .tmdot'), c = getComputedStyle(d), r = d.getBoundingClientRect(); return [__TM.hex(c.backgroundColor), __TM.hex(c.borderTopColor), r.width, r.height]; }"))
        g = sz['dot'] == sz['row'] == [8, 8] and [x[0] for x in st[1:4]] == bk and all(x[2:] == [8, 8] for x in st) and st[0][:2] == ['#ffffff', '#9ca3af'] and st[4][:2] == ['#ffffff', '#9ca3af']
        ok = ok and g
        T(G, '%s 거름 점 지름 8 = 조 줄 점 · 켜짐 = BK_COLOR(%s) · 빈 = 8px 고리(#9ca3af · 흰)' % (dn, ' · '.join(bk)), g, {'크기': sz, '차례': st})
        p.close()
    return ok


def b21(br, src, tag):
    """A-38 두문자 붙이기 넓힘 — 이름 길 · 여러 조(⊆ 테마 조) 길 · 조 하나 밖 = 안 붙음 · 기일기간 두2 무변 · 이름 고치면 다시 셈"""
    G = 'B21'
    p = page(br, tag, src, PHONE)
    jo(p, '제3조')
    p.press(at(p, '.jtbar .tmtg'), 500)
    rows = {r['id']: r['d2'] for r in p.ev("() => __TM.rows()")}
    th = dict(p.ev("() => tmModel().map(t => [t.id, tmThAcr(t).map(x => x.w).sort()])"))
    intext = p.ev("() => { const t = tmModel().find(x => x.id === 't03'); return tmText(t).indexOf('분변분재') >= 0; }")
    g1 = rows.get('t03') == '두1' and th.get('t03') == ['분변분재'] and not intext
    T(G, '{분변분재 기간} 「두1」 — 글·SVG 에 「분변분재」 없음(이름 · 여러 조 길로 붙음)', g1, {'줄': rows, '두문자': th, '글에 있음': intext})
    p.ev("() => tmListWin('t03', null)")
    p.wait(600)
    r3 = p.ev("() => { const w = __TM.pop('themelist|t03'); const r = w && w.querySelector('.throw2.tmmulti'); return r ? [__TM.txt(r.querySelector('.tmjs')), __TM.txt(r.querySelector('.tmar'))] : null; }")
    g2 = r3 == ['52조 · 53조 · 52-2조 · 67-2조', '분변분재']
    T(G, '목록 창 맨 위 줄 「52조 · 53조 · 52-2조 · 67-2조 | 분변분재」(본판 B4 무변)', g2, r3)
    g3 = all('출심삼1사' not in v for v in th.values()) and rows.get('t02') == '두2' and th.get('t02') == ['정사소2만1', '책사소2만1'] and rows.get('t01') == '두0'
    T(G, '여러 조 두문자인데 조 하나 밖(출심삼1사 = 3·14·300) = 어느 테마에도 안 붙음 · 기일기간 「두2」 · 주체능력 「두0」 무변', g3, {'줄': rows, '두문자': th})
    p.ev("() => closeAllPops(true)")
    out = []
    for name in ('분변·분재 기간 책사소2만1', '분변·분재 기간'):
        a = p.ev("() => __RB.hitOn(document.querySelector('#slot .tree .r.tmr[data-tm=t03] .jno'))")
        lp(p, a, 700)
        type_ok(p, name)
        p.idle(300)
        out.append([name, {r['id']: r['d2'] for r in p.ev("() => __TM.rows()")}.get('t03'), dict(p.ev("() => tmModel().map(t => [t.id, tmThAcr(t).map(x => x.w).sort()])")).get('t03'), (rec(p).get('t03') or {}).get('n')])
    g4 = out[0][1] == '두2' and out[0][2] == ['분변분재', '책사소2만1'] and out[1][1] == '두1' and out[1][2] == ['분변분재'] and out[1][3] == '분변·분재 기간'
    T(G, '이름 길게 눌러 고침 → 고친 이름으로 다시 셈(「분변·분재 기간 책사소2만1」 = 두2 · 「분변·분재 기간」 = 두1 — 이름 길 빠져도 여러 조 길로 분변분재)', g4, out)
    ok = g1 and g2 and g3 and g4 and not p.errs
    if p.errs:
        T(G, 'JS 오류', False, p.errs[:3])
    p.close()
    return ok


def b22(br, src, base_src, tag):
    """A-41 테마 줄 서랍 = 범례 0 · 「목차」 → 1(outerHTML = 바탕) · 재료 404 → 1"""
    G = 'B22'
    p = page(br, tag, src, PC)
    jo(p, '제3조')
    n0 = p.ev("() => document.querySelectorAll('#slot .tree .legend').length")
    p.press(at(p, '.jtbar .tmtg'), 500)
    n1 = p.ev("() => document.querySelectorAll('#slot .tree .legend').length")
    p.press(at(p, '.jtbar .tmtg'), 500)
    lg = p.ev("() => [...document.querySelectorAll('#slot .tree .legend')].map(x => x.outerHTML)")
    pb = page(br, tag + 'B', base_src, PC)
    jo(pb, '제3조')
    lgb = pb.ev("() => [...document.querySelectorAll('#slot .tree .legend')].map(x => x.outerHTML)")
    pb.close()
    g1 = n0 == 1 and n1 == 0 and len(lg) == 1 and lg == lgb
    T(G, '테마 줄 서랍 .legend 0 · 「목차」 → 1(outerHTML = 바탕 cedc251)', g1, {'목차': n0, '테마': n1, '돌아옴': len(lg), '= 바탕': lg == lgb})
    p.close()
    q = page(br, 'none:' + tag, src, PC)
    jo(q, '제3조')
    n4 = q.ev("() => ({ lg: document.querySelectorAll('#slot .tree .legend').length, btn: (document.querySelector('.jtbar .tmtg') || {}).disabled })")
    q.close()
    g2 = n4 == {'lg': 1, 'btn': True}
    T(G, '재료 404(테마 0 · 테마 줄 아님) → 범례 1', g2, n4)
    return g1 and g2


def sweep_fix1(br, src, tag, dev, base=False):
    """B-24 화면 — 서랍(목차 · 테마 · 거름) · 테마 창 · 목록 창 · 연결 창 · 찾기 결과 · 🔗 연결 창 · 원문 창 셋(바탕엔 테마 화면 없음)"""
    p = page(br, tag, src, dev)
    touch = dev in (PHONE, PAD)
    sw = lambda sel: p.ev("a => __TM.sweep(a[0], a[1])", [sel, touch])
    mark = "k => { document.querySelectorAll('[data-sw]').forEach(x => x.removeAttribute('data-sw')); const w = __TM.pop(k); if (w) w.setAttribute('data-sw', '1'); }"
    out = {}
    jo(p, '제3조')
    out['서랍 목차'] = sw('#slot .tree')
    if not base:   # 바탕(cedc251)엔 테마 줄·거름 점이 없어 같은 서랍(목차)을 잰다 — 본판 B14 와 같은 길
        p.ev("() => document.querySelector('.jtbar .tmtg').click()")
        p.idle(300)
    out['서랍 테마'] = sw('#slot .tree')
    if not base:
        p.ev("() => document.querySelector('.jtbar .tmtg').click()")
        p.idle(300)
        p.ev("() => { tmDotSet(2); render(); }")
        p.idle(300)
    out['서랍 거름'] = sw('#slot .tree')
    if not base:
        p.ev("() => { tmDotSet(0); render(); }")
        p.idle(300)
        for k, js, key in (('테마 창', "() => tmWin('t02', null)", 'theme|t02'), ('목록 창', "() => tmListWin('t02', null)", 'themelist|t02'), ('연결 창', "() => tmOfWin('특허법', '제3조', null)", 'themeof|')):
            p.ev("() => closeAllPops(true)")
            p.ev(js)
            p.wait(700)
            p.ev(mark, key)
            out[k] = sw('[data-sw="1"]')
        p.ev("() => { const w = document.querySelector('.pop.tmofw'); w.querySelector('.thsrch input').value = '분변'; w.querySelector('.thsrch .tmsgo').click(); }")
        p.wait(400)
        p.ev(mark, 'themeof|')
        out['찾기 결과'] = sw('[data-sw="1"]')
    p.ev("() => closeAllPops(true)")
    if p.ev(OPENW, 'cflw'):
        out['🔗 연결 창'] = sw('[data-fw="1"]')
    jo(p, '제6조')
    for wn, k in WINS[1:]:
        if p.ev(OPENW, k):
            out[wn] = sw('[data-fw="1"]')
    p.ev(CLOSEW)
    errs = p.errs[:]
    p.close()
    return out, errs


def b24(br, src, base_src, tag):
    G = 'B24'
    ok = True
    for dn, dev in (('폰390', PHONE), ('iPad834', PAD), ('PC', PC2)):
        n, en = sweep_fix1(br, src, tag + 'N' + dn, dev)
        b, eb = sweep_fix1(br, base_src, tag + 'B' + dn, dev, base=True)
        for scr in n:
            nn, bb = {B14_SAME.get(x, x) for x in n[scr]}, set(b.get(scr, []))
            new = sorted(nn - bb - set(ACCEPT))
            good = not new
            ok = ok and good
            T(G, '%s %s 새로 생긴 흠 0' % (dn, scr), good, {'새로': new[:8], '바탕 흠(바탕 cedc251 에도)': sorted(nn & bb)[:6], '없어짐': sorted(bb - nn)[:4], '지시서가 정한 값': sorted(nn & set(ACCEPT))})
        miss = [w for w in ('🔗 연결 창', '원문 창 마크업', '원문 창 정오문제', '원문 창 인용') if w not in n]
        if miss:
            ok = False
            T(G, '%s 창 안 뜸' % dn, False, miss)
        if en:
            ok = False
            T(G, '%s JS 오류' % dn, False, en[:3])
    return ok


def webkit_try(pw):
    try:
        return pw.webkit.launch()
    except Exception as e:
        N('WK', 'WebKit 안 잼', str(e).splitlines()[0][:160])
        return None


ORDER = ['B%d' % i for i in range(1, 25)]


def main():
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    base_src = app_src(BASE)
    if YARD:
        src = app_src(YAPP)
        print('헛잣대 — 앱 = %s · 고른 관문이 저마다 FAIL 해야 통과(본판 B1~B12 = cedc251 · fix1 B15~B22 = 8d1383d)' % YAPP)
    else:
        src = app_src(NEW)
        print('관문 _task_jo_theme(+fix1) · 앱 = %s · 바탕 = %s · fix1 바탕 = %s · 덧판 = %s' % (NEW, BASE, PREV, OVER['full']))
    prev_cache = {}
    prev_src = lambda: prev_cache.setdefault('s', app_src(PREV))
    got, tm = {}, {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        steps = [('B1', lambda: b1(br, src, base_src, 'b1')), ('B2', lambda: b2(br, src, base_src, 'b2')), ('B3', lambda: b3(br, src, 'b3')),
                 ('B4', lambda: b4(br, src, 'b4')), ('B5', lambda: b5(br, src, 'b5')), ('B6', lambda: b6(br, src, 'b6')),
                 ('B7', lambda: b7(br, src, base_src, 'b7')), ('B8', lambda: b8(br, src, base_src, 'b8')), ('B9', lambda: b9(br, src, base_src, 'b9')),
                 ('B10', lambda: b10(br, src, base_src, 'b10')), ('B11', lambda: b11(br, src, 'b11')), ('B12', lambda: b12(br, src, base_src, 'b12')),
                 ('B14', lambda: b14(br, src, base_src, 'b14')),
                 ('B15', lambda: b15(br, src, 'b15')), ('B16', lambda: b16(br, src, 'b16')), ('B17', lambda: b17(br, src, prev_src(), 'b17')),
                 ('B18', lambda: b18(br, src, base_src, prev_src(), 'b18')), ('B19', lambda: b19(br, src, 'b19')), ('B20', lambda: b20(br, src, 'b20')),
                 ('B21', lambda: b21(br, src, 'b21')), ('B22', lambda: b22(br, src, base_src, 'b22')), ('B24', lambda: b24(br, src, base_src, 'b24'))]
        for g, fn in steps:
            if ONLY and g not in ONLY:
                continue
            if YARD and g in ('B14', 'B24'):
                N(g, '헛잣대 해당 없음', '화면 훑기 = 새 판 흠 − 바탕 흠 · 바탕끼리 견주면 늘 0')
                continue
            print('── %s' % g, flush=True)
            t1 = time.time()
            try:
                got[g] = bool(fn())
            except Exception as e:
                got[g] = False
                T(g, '돌다 멈춤', False, str(e).splitlines()[0][:300])
            tm[g] = time.time() - t1
            print('   (%s %.0f초)' % (g, tm[g]), flush=True)
        br.close()
        if 'webkit' in ENGS and not YARD and (not ONLY or 'WK' in ONLY):
            wk = webkit_try(pw)
            if wk:
                for g, fn in (('B1', lambda: b1(wk, src, base_src, 'wk1')), ('B6', lambda: b6(wk, src, 'wk6', devs=(('폰390', PHONE),)))):
                    try:
                        fn()
                    except Exception as e:
                        T(g + '-wk', 'WebKit 돌다 멈춤', False, str(e).splitlines()[0][:200])
                wk.close()
    if not YARD and (not ONLY or 'B13' in ONLY):
        print('── B13', flush=True)
        t1 = time.time()
        try:
            got['B13'] = bool(b13(src, base_src))
        except Exception as e:
            got['B13'] = False
            T('B13', '돌다 멈춤', False, str(e).splitlines()[0][:300])
        tm['B13'] = time.time() - t1
    if not YARD and all(('B%d' % i) in got for i in range(1, 15)):   # fix1 B-23 — 본판 B1~B14 다시(같은 실행) · 바뀐 값은 결과 절
        bad = [g for g in ['B%d' % i for i in range(1, 15)] if not got[g]]
        got['B23'] = not bad
        T('B23', '본판 B1~B14 다시 = 모두 PASS(fix1 바탕 8d1383d 위 · 합성 재료 보탬 뒤)', got['B23'], {'FAIL 관문': bad})
    lines = []
    print('\n══ 요약 (%.0f초)%s' % (time.time() - t0, ' — 헛잣대' if YARD else ''))
    for g in [x for x in ORDER if x in got]:
        cells = [r for r in RES if r[0] == g and r[2] is not None]
        nf = sum(1 for r in cells if not r[2])
        verdict = ('FAIL(헛잣대 통과)' if not got[g] else 'PASS(헛잣대 실패)') if YARD else ('PASS' if got[g] else 'FAIL')
        s = '  %-4s %s (%d 칸 중 FAIL %d · %.0f초)' % (g, verdict, len(cells), nf, tm.get(g, 0))
        print(s)
        lines.append(s)
    with open(OUTF, 'w', encoding='utf-8', newline='\n') as f:
        for r in RES:
            d = r[3] if isinstance(r[3], str) else json.dumps(r[3], ensure_ascii=False, default=str)
            f.write('%s | %s · %s | %s\n' % ('INFO' if r[2] is None else ('PASS' if r[2] else 'FAIL'), r[0], r[1], d))
        f.write('\n'.join(lines) + '\n')
    print('결과 → %s' % OUTF)


if __name__ == '__main__':
    try:
        main()
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
