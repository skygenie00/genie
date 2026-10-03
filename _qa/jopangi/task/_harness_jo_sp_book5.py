# -*- coding: utf-8 -*-
r"""_task_jo_sp_book5(+_add1) §B-3~§B-6 관문 — 상표 1차객 「📚 교재 자리」 뷰객 5판(tm_view5) · 책 표 한 벌(특허 patent_hr8 무변) · 앱(시험 데이터)

  python _harness_jo_sp_book5.py [--new <앱 파일 | genie git 판>] [--base <판>] [--eng chromium,webkit] [--only B3,B4,..] [--res <결과(기본 = 임시 폴더)>] [--yardstick]
        [--vendor <pdf.js 3.11.174 폴더>] [--exam <시험지 폴더>] [--mbpdf <minbeoppdf 클론>]

  저장소 자료 = 하네스 route 사본(book8 하네스 꼴 · 같은 출처 /__book/) — minbeoppdf 클론 위에 덧판:
    words/tm_view5/ = _fx_sp_book5(지어낸 값: 책메타 pages 549 · printOffset −11 · 쪽 글자층 다섯 쪽 · 글.json.gz · 대응.json 표본 uid 셋) ·
    pdf/tm_view5.pdf = 하네스가 짓는 시험 PDF(549 쪽 · 514.8×714.5 · 「TM5 TEST p.N」 · 바이트 멱등 · md5 = 책메타 pdfMd5) · 그 밖(patent_hr8 등) = 클론 그대로
    ⚠ 진짜 뷰객 5판(글·PDF)은 열지 않는다(클론 작업트리에 없어도 · 있어도 덧판이 가린다) · 카드 = sp_view4 시험 데이터(_fx_sp_view4 · 지어낸 글)
  관문:
    B3 상표 「📚 교재 자리」 5판 줄 — 책 카드 SV110001 · 문항째 SV211020 · 리담 S2663211 · 대응표 없음 SV110003 · ID 칩 진짜 누름(PC 마우스 · 폰 손가락)
       → 「정리OMR 은 특허만 있다」 + 교재 칸 · 줄 = 「상표법 뷰객 5판 · p.(PDF−11) · PDF N · 확신」 + 둘째 줄 = 그 자리 글자층 글 · 「후보 2」 · 「📍 자리 직접 찍기」 ·
       줄 누름 → 교재 창 「📘 상표법 뷰객 5판」 그 쪽 · 노란 자리 상자(r) · 「교재에서 찾기」 칸
    B4 자리 직접 찍기 — 쪽 창 찍기(끌기) → 「이 자리 저장」 → 기록 jopangi.canvasjari 칸 v5|uid = {by:hand · b:tm_view5 · p · r} · 알림 「뷰객 5판 p.N」 ·
       첫 줄 「찍어 둔 자리」 + 그림 + 「자동으로 되돌리기」 · 새로고침 뒤 그대로 · 다른 기기(가짜 원격) 그대로 · 되돌리기 = {auto:true} · 민소 정리캔버스 「교재 확정 N 고아」 = v5 칸 안 셈
    B5 PDF 재움 · 교재 찾기 — 첫 열기 = 저장소(PDF 요청 ≥1) → IndexedDB bookpdf:tm_view5(pdfMd5 = 책메타) → 새로고침 뒤 = 이 기기(요청 0 · from cache) ·
       「교재에서 찾기」 시험낱말 → 3쪽 4곳 · 누름 → 그 쪽 노란 상자 수
    B6 특허 8판 무변 — patent_hr8 박힌 자리 = 책 표 하나(주석 밖 글자) · 특허 「📚 교재 자리」 8판 칸(표본 셋) DOM = 바탕 · 8판 교재 창 머리·상자 = 바탕 ·
       특허 찍기 기록·알림 = 바탕 · p8Guess · k8 · meta8 = 바탕
  헛잣대 = --yardstick : 바탕(e281d6b = cloud/jo_sp_view5 끝) + 같은 시험 자료 → B3~B5 묶음마다 FAIL · B6 = 박힌 자리 칸만(바탕 FAIL) · 나머지는 바탕끼리라 해당 없음
  도구 = 같은 폴더 _harness_jo_sp_view4(+ revfix0929b 서버 · SEED · 기기 · 가짜 원격 · __RB) · 자리 = _roots(GENIE_ROOT · MBPDF_ROOT) · WebKit 없으면 「안 잼」
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import collections, gzip, hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, time, urllib.parse   # noqa: E402
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer   # noqa: E402
import threading   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEW = ARG('--new', _roots.genie('jo', 'index.html'))
BASE = ARG('--base', 'e281d6b')   # cloud/jo_sp_view5 끝(sp_book5 바탕)
YARD = '--yardstick' in sys.argv
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
OUTF = ARG('--res', os.path.join(tempfile.gettempdir(), 'h_jobk5', '_harness_jo_sp_book5_result.txt'))   # 기본 = 임시 폴더(_qa 에 결과를 쓰지 않는다)
MBP0 = ARG('--mbpdf', _roots.mbpdf())
TMP = os.path.join(tempfile.gettempdir(), 'h_jobk5', 'p%d' % os.getpid())
os.makedirs(TMP, exist_ok=True)
FX = os.path.join(HERE, '_fx_sp_book5')
_argv = sys.argv[:]
sys.argv = [_argv[0]] + [x for k in ('--exam', '--vendor') if k in _argv for x in (k, _argv[_argv.index(k) + 1])]
sys.path.insert(0, HERE)
import _harness_jo_sp_view4 as SV   # noqa: E402
sys.argv = _argv
H = SV.H
PC, PHONE = (1440, 900), H.PHONE
DOC5, DOC8 = 'tm_view5', 'patent_hr8'


def git(*a):
    return subprocess.run(['git', '-C', _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def app_src(x):
    if os.path.isfile(x):
        return open(x, 'rb').read().decode('utf-8')
    b = git('show', x + ':jo/index.html')
    if not b:
        raise SystemExit('앱을 못 읽었다: ' + x)
    return b.decode('utf-8')


def md5lf(s):
    return hashlib.md5(s.replace('\r\n', '\n').encode('utf-8')).hexdigest()


RES = []


def T(g, name, ok, detail=''):
    RES.append((g, name, bool(ok), detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', g, name, d[:700]), flush=True)
    return bool(ok)


def N(g, name, detail=''):
    RES.append((g, name, None, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('INFO | %s · %s | %s' % (g, name, d[:1000]), flush=True)


# ════════════════════════ 시험 PDF — 지어낸 쪽(_fx_sp_book5 책메타 pdfMd5 와 같은 바이트) ════════════════════════
W_PT, H_PT, PAGES5 = 514.8, 714.5, 549
LINE_X0, LINE_ADV, LINE_Y0, LINE_DY = 160, 44, 360, 100   # 글자층 0~2000 · 글자 왼쪽 아래(밑줄) — 시험 데이터 짓기와 같은 값
BARS = {22: [23, 23, 18, 14], 23: [20, 18, 16], 124: [25, 25, 12], 200: [24, 26, 12], 310: [25, 17, 14]}   # 쪽 → 줄마다 글자 수(옅은 막대)


def make_pdf(pages=PAGES5, bars=BARS):
    objs = [b'<< /Type /Catalog /Pages 2 0 R >>',
            ('<< /Type /Pages /Kids [%s] /Count %d >>' % (' '.join('%d 0 R' % (4 + 2 * i) for i in range(pages)), pages)).encode(),
            b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>']
    for i in range(pages):
        p = i + 1
        cs = ['BT /F1 22 Tf 40 %.1f Td (TM5 TEST p.%d) Tj ET' % (H_PT - 44, p), 'BT /F1 9 Tf 40 %.1f Td (harness fixture - invented page) Tj ET' % (H_PT - 60)]
        for li, n in enumerate(bars.get(p, [])):
            cs.append('0.85 g %.2f %.2f %.2f %.2f re f 0 g' % (LINE_X0 / 2000 * W_PT, H_PT - (LINE_Y0 + LINE_DY * li) / 2000 * H_PT, (n + 2) * LINE_ADV / 2000 * W_PT, 9.0))
        c = '\n'.join(cs).encode()
        objs.append(('<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.1f %.1f] /Resources << /Font << /F1 3 0 R >> >> /Contents %d 0 R >>' % (W_PT, H_PT, 5 + 2 * i)).encode())
        objs.append(b'<< /Length ' + str(len(c)).encode() + b' >>\nstream\n' + c + b'\nendstream')
    out = bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
    offs = []
    for k, o in enumerate(objs):
        offs.append(len(out))
        out += ('%d 0 obj\n' % (k + 1)).encode() + o + b'\nendobj\n'
    xref = len(out)
    out += ('xref\n0 %d\n' % (len(objs) + 1)).encode() + b'0000000000 65535 f \n'
    for o in offs:
        out += ('%010d 00000 n \n' % o).encode()
    out += ('trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n' % (len(objs) + 1, xref)).encode()
    return bytes(out)


PDF5 = make_pdf()
META5 = json.load(open(os.path.join(FX, '책메타.json'), encoding='utf-8'))
MAP5 = json.load(open(os.path.join(FX, '대응.json'), encoding='utf-8'))
TXT5 = json.loads(gzip.decompress(open(os.path.join(FX, '글.json.gz'), 'rb').read()).decode('utf-8'))


def words5(p):
    o = json.loads(gzip.decompress(open(os.path.join(FX, 'ox_book_%s_p%d.json.gz' % (DOC5, p)), 'rb').read()).decode('utf-8'))
    return o


def snip(p, r):
    """앱 ncSnip 과 같은 셈(쪽 글자층 · r 0~2000 → 앞 두 줄 · 넓은 틈 = 빈칸)"""
    o = words5(p)
    Wp, Hp = o['w'], o['h']
    x0, y0, x1, y1 = (r[0] / 2000 * Wp, r[1] / 2000 * Hp, r[2] / 2000 * Wp, r[3] / 2000 * Hp)
    Y0, Y1, X0, X1 = (y0 - 1) / Hp * 2000, (y1 + 3) / Hp * 2000, (x0 - 2) / Wp * 2000, (x1 + 2) / Wp * 2000
    cs = []
    for ln in o['words'].split('\n'):
        a = ln.split('\t')
        if len(a) < 3:
            continue
        x, y = float(a[1]), float(a[2])
        if Y0 <= y <= Y1 and X0 <= x <= X1:
            cs.append((a[0], x, y))
    cs.sort(key=lambda c: (c[2], c[1]))
    L = []
    for c in cs:
        if L and c[2] - L[-1]['y'] <= 6:
            L[-1]['c'].append(c)
        else:
            L.append({'y': c[2], 'c': [c]})
    out = []
    for l in L[:2]:
        c = sorted(l['c'], key=lambda q: q[1])
        d = sorted(v for v in (c[i + 1][1] - c[i][1] for i in range(len(c) - 1)) if v > 0)
        md = d[len(d) >> 1] if d else 0
        out.append(''.join((' ' if i and md and q[1] - c[i - 1][1] > md * 1.28 else '') + q[0] for i, q in enumerate(c)))
    return ' '.join(out)


def sn40(p, r):
    t = snip(p, r)
    return (t[:40] + '…') if t else ''


# ════════════════════════ /__book/ 덧판(클론 + 시험 tm_view5) · 서버 ════════════════════════
BOOKREQ = collections.Counter()
SEARCH8 = '시험팔판찾기낱말'   # 8판 「교재에서 찾기」 시험 낱말(지어낸 쪽 글일 때) · 클론에 진짜 쪽 글이 있으면 흔한 두 글자 「특허」로 찾고 수만 맞댄다(책 글을 찍지 않는다)
FX8 = [False]   # 덧판에 지어낸 8판 쪽 글을 넣었나


def book_root():
    d = os.path.join(TMP, 'book')
    if os.path.isdir(d):
        return d
    os.makedirs(d)
    for x in (os.listdir(MBP0) if os.path.isdir(MBP0) else []):
        if x in ('.git', 'words', 'pdf'):
            continue
        SV._ln(os.path.join(MBP0, x), os.path.join(d, x))
    for sub in ('words', 'pdf'):
        os.makedirs(os.path.join(d, sub))
        src = os.path.join(MBP0, sub)
        for x in (os.listdir(src) if os.path.isdir(src) else []):
            if x in (DOC5, DOC5 + '.pdf'):
                continue   # 진짜 뷰객 5판은 가린다
            SV._ln(os.path.join(src, x), os.path.join(d, sub, x))
    w8s, w8 = os.path.join(MBP0, 'words', DOC8), os.path.join(d, 'words', DOC8)
    if os.path.isdir(w8s) and not os.path.isfile(os.path.join(w8s, '글.json.gz')):   # 클론에 8판 쪽 글이 없으면(클라우드 옛 판) 지어낸 쪽 글 하나 — 8판 「교재에서 찾기」 칸을 바탕·새 판 둘 다 세워 맞댄다
        os.remove(w8)
        os.makedirs(w8)
        for x in os.listdir(w8s):
            SV._ln(os.path.join(w8s, x), os.path.join(w8, x))
        m8 = json.load(open(os.path.join(w8s, '책메타.json'), encoding='utf-8'))
        t8 = [''] * int(m8.get('pages') or 805)
        t8[499] = SEARCH8 + '지어낸시험글'
        t8[32] = '앞쪽' + SEARCH8
        raw = json.dumps({'docid': DOC8, 'pdfMd5': m8.get('pdfMd5'), 'pages': len(t8), 'builtBy': '_harness_jo_sp_book5 시험 쪽 글(지어낸 값)', 't': t8}, ensure_ascii=False).encode('utf-8')
        bio = io.BytesIO()
        with gzip.GzipFile(fileobj=bio, mode='wb', mtime=0) as f:
            f.write(raw)
        open(os.path.join(w8, '글.json.gz'), 'wb').write(bio.getvalue())
        FX8[0] = True
    w5 = os.path.join(d, 'words', DOC5)
    os.makedirs(w5)
    for x in os.listdir(FX):
        shutil.copyfile(os.path.join(FX, x), os.path.join(w5, x))
    open(os.path.join(d, 'pdf', DOC5 + '.pdf'), 'wb').write(PDF5)
    return d


BOOK = book_root()


def serve_b5(tag, src):
    if tag in SV.SERVERS:
        return SV.SERVERS[tag][1]
    body = H.inject(src).encode('utf-8')

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
            if p.startswith('/__book/'):
                BOOKREQ[p[len('/__book/'):]] += 1
            if p.startswith('/__rec/'):
                k = p[len('/__rec/'):]
                with SV.REMOTE.lock:
                    b = SV.REMOTE.files.get(k)
                if b is None:
                    return self._send(404, b'{"message":"Not Found"}')
                if 'raw' in (self.headers.get('Accept') or ''):
                    return self._send(200, b, 'application/octet-stream')
                return self._send(200, json.dumps({'sha': hashlib.sha1(b).hexdigest(), 'size': len(b)}).encode())
            return super().do_GET()

        def do_PUT(self):
            import base64
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
            with SV.REMOTE.lock:
                SV.REMOTE.files[k] = data
            return self._send(200, json.dumps({'content': {'sha': hashlib.sha1(data).hexdigest()}}).encode())

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
            for pre, root in (('/jo/data/', SV.DATA_FOR.get(tag, SV.DATA)), ('/gichul/pdf/', H.EXAM), ('/__book/', BOOK)):
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
    SV.SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


H.serve = serve_b5   # revfix0929b Pg 가 모듈 이름 serve 로 부른다 · sp_view4 serve_sv(/__book/ 없음)를 갈아 끼움
_TAGN = [0]


def open_pg(br, src, dev=PC, ls=None, keep_remote=False, tag=None):
    """새 쪽 = 새 기기(가짜 원격 비움) · keep_remote = 같은 원격을 보는 다른 기기 · tag 같으면 같은 서버(같은 앱)"""
    if not keep_remote:
        SV.REMOTE.clear()
    if tag is None:
        _TAGN[0] += 1
        tag = 'b5_%d' % _TAGN[0]
    p = H.dev_page(br, tag, src, dev, ls=ls)
    p.ev(B5_JS)
    p._tag = tag
    return p


B5_JS = r"""() => { if (window.__B5) return 1;
const wait = ms => new Promise(r => setTimeout(r, ms));
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const vis = e => !!e && e.isConnected && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden' && e.getBoundingClientRect().height > 0;
const hit = e => { if (!e) return null; try { e.scrollIntoView({ block: 'center', inline: 'nearest' }); } catch (x) {} const r = e.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2, a = document.elementFromPoint(cx, cy);
  return { cx: cx, cy: cy, w: r.width, h: r.height, on: !!a && (a === e || e.contains(a)) && cy > 0 && cy < innerHeight }; };
const pops = () => (typeof POPS !== 'undefined' ? POPS : []);
const boxPop = () => pops().filter(x => (x._pk || '').indexOf('cell|📚 교재 자리') === 0).pop();
const bookPop = d => pops().filter(x => x._pk === 'cv|book|' + d).pop();
window.__B5 = {
  go: async (kind, id, dom, law, ln) => { try{ closeAllPops(); }catch(e){} await gotoJimun(kind, id, dom, ln || '', law); await wait(600);
    for (let i = 0; i < 100 && typeof busy !== 'undefined' && busy; i++) await wait(100);
    if (!document.getElementById(dom) && typeof UZGK !== 'undefined'){ UZGK = UZGK === 'g' ? 'x' : 'g'; S.oxPage = null; await render(); await wait(300);
      const pg = (typeof OXDOMPG !== 'undefined' && OXDOMPG || {})[dom]; if (pg != null && pg !== S.oxPage){ S.oxPage = pg; await render(); await wait(300); } }
    return !!document.getElementById(dom); },
  idAt: (dom, uid) => { const c = document.getElementById(dom); const b = c ? [...c.querySelectorAll('.qb.id')].find(x => txt(x) === uid) : null; return hit(b); },
  box: () => { const w = boxPop(); if (!w) return null; const h = w.querySelector('.mbb8');
    return { title: txt(w.querySelector('.pt')), bk: h ? (h.dataset.bk || '') : null, p8u: h ? h.dataset.p8u : null,
      none: [...w.querySelectorAll('.mbbnone')].map(txt), sec: h ? txt(h.querySelector('.ncb-sec')) : null, omr: [...w.querySelectorAll('.mbbrow')].filter(r => !r.closest('.mbb8')).map(r => txt(r.querySelector('.hd .k'))),
      rows: h ? [...h.querySelectorAll('.mbbrow')].map(r => ({ k: txt(r.querySelector('.hd .k')), p: txt(r.querySelector('.hd .p')), m: [...r.querySelectorAll('.hd .m')].map(txt), sn: txt(r.querySelector('.sn')), book: r.dataset.book, pg: r.dataset.p, vis: vis(r) })) : [],
      btns: h ? [...h.querySelectorAll('.ncb-more')].map(b => txt(b)) : [], pic: !!(h && h.querySelector('.ncb-pic canvas')), loading: !!(h && /받는 중/.test(txt(h))), html: h ? h.innerHTML : null, full: txt(w.querySelector('.pb')) }; },
  boxReady: async (pic) => { for (let i = 0; i < 400; i++){ const b = __B5.box(); if (b && !b.loading && (b.rows.length ? (b.rows[0].sn || !b.rows[0].vis) : (b.none.length > 1 || b.bk === null)) && (!pic || b.pic)){ await wait(500); return __B5.box(); } await wait(50); } return __B5.box(); },
  rowAt: i => { const w = boxPop(); const r = w && w.querySelectorAll('.mbb8 .mbbrow')[i || 0]; return hit(r); },
  btnAt: re => { const w = boxPop(); const rx = new RegExp(re); const b = w && [...w.querySelectorAll('.mbb8 .ncb-more')].find(x => rx.test(txt(x))); return hit(b); },
  book: d => { const w = bookPop(d); if (!w) return { n: 0 }; const nav = w.querySelector('.cv-booknav'), hl = w.querySelector('.cv-bookhl'), cvs = w.querySelector('.cv-bookpg canvas'), bx = w.querySelector('.cv-pickbox'), L = w.querySelector('.cv-bsres');
    const st = (window.__jocvb && window.__jocvb.C.stat[d]) || {};
    return { n: pops().filter(x => (x._pk || '').indexOf('cv|book|') === 0).length, title: txt(w.querySelector('.pt')), nav: txt(nav), page: nav && nav.querySelector('#cvBookP') ? +nav.querySelector('#cvBookP').value : null,
      hl: hl ? { l: parseFloat(hl.style.left), t: parseFloat(hl.style.top), w: parseFloat(hl.style.width), h: parseFloat(hl.style.height), vis: vis(hl) } : null,
      pick: { on: !!w.querySelector('.cv-booknav [data-pk].on'), ov: !!w.querySelector('.cv-pickov'), sv: txt(w.querySelector('.cv-booknav [data-sv]')), box: bx ? [bx.style.left, bx.style.top, bx.style.width, bx.style.height] : null },
      bs: !!w.querySelector('.cv-bs input'), bsList: L && !L.hidden ? txt(L).slice(0, 200) : '', bsRows: L ? L.querySelectorAll('.cv-bssn').length : 0, hits: w.querySelectorAll('.cv-bshit').length, cur: w.querySelectorAll('.cv-bshit.cur').length,
      cvsW: cvs ? cvs.width : 0, loading: /받는 중/.test(txt(w)), err: /받지 못했다/.test(txt(w)) ? txt(w).slice(0, 200) : null, from: st.from || null, pages: st.pages || null }; },
  bookReady: async d => { for (let i = 0; i < 600; i++){ const b = __B5.book(d); if (b.n && (b.cvsW > 0 || b.err) && !b.loading){ await wait(300); return __B5.book(d); } await wait(50); } return __B5.book(d); },
  bookAt: (d, what, j) => { const w = bookPop(d); if (!w) return null;
    if (what === 'pg'){ const t = w.querySelector('.cv-bookpg'); if (!t) return null; try { t.scrollIntoView({ block: 'nearest' }); } catch (e) {} const r = t.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; }
    const t = what === 'pk' ? w.querySelector('.cv-booknav [data-pk]') : what === 'sv' ? w.querySelector('.cv-booknav [data-sv]') : what === 'bsin' ? w.querySelector('.cv-bs input') : what === 'bsgo' ? w.querySelector('.cv-bs .cv-bsgo') : what === 'res' ? w.querySelectorAll('.cv-bsres .cv-bssn')[j || 0] : null;
    return hit(t); },
  pin: k => { try { return (JSON.parse(localStorage.getItem('jopangi.canvasjari') || '{}'))[k] || null; } catch (e) { return null; } },
  keys: () => { try { return Object.keys(JSON.parse(localStorage.getItem('jopangi.canvasjari') || '{}')); } catch (e) { return []; } },
  toast: () => [...document.querySelectorAll('#toasts .toast')].map(txt).join(' | '),
  idb: async k => await new Promise(res => { let rq; try { rq = indexedDB.open('ox_master_db', 1); } catch (e) { return res({ err: String(e) }); }
    rq.onupgradeneeded = () => { const db = rq.result; if (!db.objectStoreNames.contains('rows')) db.createObjectStore('rows'); };
    rq.onsuccess = () => { const db = rq.result; let g; try { g = db.transaction('rows', 'readonly').objectStore('rows').get(k); } catch (e) { return res({ err: String(e) }); }
      g.onsuccess = () => { const v = g.result; res(v ? { has: true, md5: v.pdfMd5 || null, n: (v.buf && v.buf.byteLength) || 0 } : { has: false }); }; g.onerror = () => res({ has: false }); };
    rq.onerror = () => res({ err: 'open' }); }),
  api: () => { try { const J = viewCanvas.jari; return { k8: !!J.k8 && typeof J.k8.get === 'function' && typeof J.k8.put === 'function' && typeof J.k8.raw === 'function', meta8: typeof J.meta8 === 'function', book8: typeof J.book8 === 'function',
    guess: typeof p8Guess === 'function' ? [p8Guess('T1552093'), p8Guess('TJ0100001'), p8Guess('T2562011')] : null, name8: viewCanvas.hsBook.name('patent_hr8'), name5: viewCanvas.hsBook.name('tm_view5') }; } catch (e) { return { err: String(e) }; } },
  orph: async () => { try{ closeAllPops(true); }catch(e){} S.law = '민사소송법'; S.tab = 'omr'; await render(); for (let i = 0; i < 200; i++){ if (document.getElementById('cvJariOrph')) break; await wait(50); } await wait(400);
    const w = document.getElementById('cvJariOrph'); return w ? { t: txt(w), vis: vis(w) || w.style.display !== 'none' && !!txt(w) } : null; },
  closeAll: () => { try { closeAllPops(true); } catch (e) {} return 1; }
};
return 1; }"""


# ════════════════════════ 표본(시험 데이터) ════════════════════════
C_BOOK = ('P', 'V4-A1-OX1', 'qb-SV110001', 'SV110001')     # 책 카드 — 대응표 1등 22 + 후보 23 · 200
C_OBJ = ('P', 'V4-B2-S20', 'qb-SV211020', 'SV211020')      # 문항째 카드 — 124
C_LID = ('L', '2026-63-1', 'qb-S2663211', 'S2663211', 'u')  # 리담 카드(책 줄에 안 흡수 = 단원 (미수록) 줄) — 310
C_NONE = ('P', 'V4-A1-OX3', 'qb-SV110003', 'SV110003')     # 대응표 없음 — 찍기(첫 쪽 = 책 줄 pdf쪽 23)
OFF5 = META5['printOffset']
P8S = [('P', 'P7-1662', 'qb-T1552093', 'T1552093'), ('P', 'P7-0089', 'qb-T2562011', 'T2562011'), ('P', 'P7-0000-1', 'qb-TJ0100001', 'TJ0100001')]   # 특허 8판 표본(book8 표본 셋)


def row_want(u):
    out = []
    for i, s in enumerate(MAP5.get(u) or []):
        out.append({'k': META5 and '상표법 뷰객 5판', 'p': 'p.%d' % (s['p'] + OFF5), 'm': ['PDF %d' % s['p']] + ([('확신 ' + s['c'])] if i == 0 and s.get('c') else (['후보'] if i else [])),
                    'sn': sn40(s['p'], s['r'])})
    return out


def go(p, c):
    return p.ev("([k, i, d, l, n]) => __B5.go(k, i, d, l, n)", [c[0], c[1], c[2], '상표법' if c[3].startswith('S') else '특허법', c[4] if len(c) > 4 else ''])


def press(p, at, wait=700):
    if not at or not at.get('on'):
        return False
    (p.tap if p.touch else p.click)(at['cx'], at['cy'], wait)
    return True


def open_box(p, c):
    ok = go(p, c)
    at = p.ev("([d, u]) => __B5.idAt(d, u)", [c[2], c[3]]) if ok else None
    press(p, at)
    b = p.ev("() => __B5.boxReady()")
    return ok, at, b


def drag(p, x0, y0, x1, y1, n=12):
    if p.touch:
        p.ev("([a, b, c, d]) => { const ov = document.querySelector('.cv-pickov'); if (!ov) return 0; const mk = (t, x, y) => ov.dispatchEvent(new PointerEvent(t, {bubbles: true, cancelable: true, pointerId: 9, pointerType: 'touch', isPrimary: true, clientX: x, clientY: y, button: 0, buttons: t === 'pointerup' ? 0 : 1}));"
             " mk('pointerdown', a, b); for (let i = 1; i <= 12; i++) mk('pointermove', a + (c - a) * i / 12, b + (d - b) * i / 12); mk('pointerup', c, d); return 1; }", [x0, y0, x1, y1])
        p.wait(300)
        return
    m = p.pg.mouse
    m.move(x0, y0)
    m.down()
    for i in range(1, n + 1):
        m.move(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n)
        p.wait(16)
    m.up()
    p.wait(300)


# ════════════════════════ 관문 ════════════════════════
def b3(br, src, dev=PC, g='B3'):
    ok = True
    p = open_pg(br, src, dev)
    try:
        hand = '손가락' if p.touch else '마우스'
        cases = (C_BOOK, C_OBJ, C_LID, C_NONE) if not p.touch else (C_BOOK,)
        for c in cases:
            on, at, b = open_box(p, c)
            want = row_want(c[3])
            got = [{k: r[k] for k in ('k', 'p', 'm', 'sn')} for r in ((b or {}).get('rows') or [])][:1]
            if want:
                good = bool(b) and b.get('bk') == DOC5 and b.get('sec') == '교재' and '정리OMR 은 특허만 있다' in (b.get('none') or []) and got == want[:1] \
                    and (('후보 %d' % min(2, len(want) - 1)) in b['btns'] if len(want) > 1 else not any(x.startswith('후보') for x in b['btns'])) and '📍 자리 직접 찍기' in b['btns']
                ok &= T(g, '%s %s ID 칩 %s 누름 → 「정리OMR 은 특허만 있다」 + 교재 칸 · 1등 줄 「%s · %s · %s」 + 둘째 줄 = 자리 글자층 글 · %s「📍 자리 직접 찍기」' % (
                    c[1], c[3], hand, want[0]['k'], want[0]['p'], ' · '.join(want[0]['m']), ('「후보 %d」 · ' % min(2, len(want) - 1)) if len(want) > 1 else ''), good,
                    {'누름': at, '창': {k: (b or {}).get(k) for k in ('title', 'bk', 'none', 'sec', 'rows', 'btns')}, '기대 1등': want[0]})
            else:
                good = bool(b) and b.get('bk') == DOC5 and '뷰객 5판 — 자리 없음 · 직접 찍기' in (b.get('none') or []) and not b.get('rows') and b.get('btns') == ['📍 자리 직접 찍기']
                ok &= T(g, '%s %s(대응표 없음) %s → 「뷰객 5판 — 자리 없음 · 직접 찍기」 + 「📍 자리 직접 찍기」' % (c[1], c[3], hand), good, {'누름': at, '창': {k: (b or {}).get(k) for k in ('bk', 'none', 'rows', 'btns')}})
            if c is C_BOOK:
                if not p.touch:
                    press(p, p.ev("() => __B5.btnAt('^후보')"), 500)
                    b2 = p.ev("() => __B5.box()")
                    p.wait(800)
                    b2 = p.ev("() => __B5.box()")
                    got2 = [{k: r[k] for k in ('k', 'p', 'm', 'sn')} for r in ((b2 or {}).get('rows') or [])]
                    ok &= T(g, '%s 「후보 2」 누름 → 둘째·셋째 줄(p.%d · p.%d · 「후보」 · 자리 글자층 글)' % (c[3], want[1]['p'] and MAP5[c[3]][1]['p'] + OFF5, MAP5[c[3]][2]['p'] + OFF5), got2 == want, {'줄': got2, '기대': want})
                press(p, p.ev("() => __B5.rowAt(0)"), 600)
                k = p.ev("(d) => __B5.bookReady(d)", DOC5)
                s0 = MAP5[c[3]][0]
                hl_want = {'l': s0['r'][0] / 20, 't': s0['r'][1] / 20, 'w': (s0['r'][2] - s0['r'][0]) / 20, 'h': (s0['r'][3] - s0['r'][1]) / 20}
                hl = (k or {}).get('hl') or {}
                good = k.get('n') == 1 and k.get('title') == '📘 상표법 뷰객 5판' and k.get('page') == s0['p'] and ('%d쪽' % (s0['p'] + OFF5)) in k.get('nav', '') and ('/ %d' % PAGES5) in k.get('nav', '') \
                    and '상표법 뷰객 5판' in k.get('nav', '') and k.get('cvsW', 0) > 0 and not k.get('err') and bool(hl) and hl.get('vis') and all(abs(hl.get(x, -9) - hl_want[x]) < 0.05 for x in hl_want) and k.get('bs')
                ok &= T(g, '%s 1등 줄 %s → 교재 창 「📘 상표법 뷰객 5판」 PDF %d(%d쪽 · / %d) · 노란 자리 상자 = 대응표 r · 「교재에서 찾기」 칸' % (c[3], hand, s0['p'], s0['p'] + OFF5, PAGES5), good,
                        {'창': {x: k.get(x) for x in ('n', 'title', 'page', 'nav', 'hl', 'bs', 'cvsW', 'err')}, '기대 상자': hl_want})
            p.ev("() => __B5.closeAll()")
        return ok
    finally:
        p.close()


def b4(br, src):
    ok = True
    p = open_pg(br, src)
    try:
        c = C_NONE
        u = c[3]
        on, at, b = open_box(p, c)
        press(p, p.ev("() => __B5.btnAt('자리 직접 찍기')"), 700)
        k = p.ev("(d) => __B5.bookReady(d)", DOC5)
        guess = int(SV.ROWBY[c[1]]['pdf쪽'])
        ok &= T('B4', '%s 「📍 자리 직접 찍기」 → 교재 창 찍기 켬(덮개 · 📍 찍기 on) · 첫 쪽 = 책 줄 pdf쪽 %d(대응표 없음 어림)' % (u, guess),
                k.get('n') == 1 and k.get('page') == guess and k['pick']['on'] and k['pick']['ov'], {'창': {x: k.get(x) for x in ('title', 'page', 'pick', 'err')}})
        pg = p.ev("(d) => __B5.bookAt(d, 'pg')", DOC5)
        if pg:
            drag(p, pg['x'] + pg['w'] * 0.2, pg['y'] + pg['h'] * 0.3, pg['x'] + pg['w'] * 0.8, pg['y'] + pg['h'] * 0.4)
        k2 = p.ev("(d) => __B5.book(d)", DOC5)
        sv_at = p.ev("(d) => __B5.bookAt(d, 'sv')", DOC5)
        press(p, sv_at, 700)
        toast = p.ev("() => __B5.toast()")
        rec = p.ev("(k) => __B5.pin(k)", 'v5|' + u)
        keys = p.ev("() => __B5.keys()")
        rr = (rec or {}).get('r') or []
        good = bool(rec) and rec.get('by') == 'hand' and rec.get('b') == DOC5 and rec.get('p') == guess and len(rr) == 4 and all(abs(a - e) <= 0.006 for a, e in zip(rr, [0.2, 0.3, 0.8, 0.4])) \
            and ('p8|' + u) not in keys and ('교재 자리를 찍었다 — 뷰객 5판 p.%d' % (guess + OFF5)) in toast
        ok &= T('B4', '끌기 → 「이 자리 저장」 → 기록 jopangi.canvasjari 칸 v5|%s = {by:hand · b:tm_view5 · p:%d · r = 끈 자리 ±0.6%%} · p8 칸 없음 · 알림 「뷰객 5판 p.%d」' % (u, guess, guess + OFF5), good,
                {'끈 뒤 저장 단추': (k2 or {}).get('pick'), '기록': rec, '알림': toast})
        b2 = p.ev("() => __B5.boxReady(true)")
        r0 = ((b2 or {}).get('rows') or [{}])[0]
        good = bool(b2) and r0.get('p') == 'p.%d' % (guess + OFF5) and '찍어 둔 자리' in r0.get('m', []) and b2.get('pic') and '자동으로 되돌리기' in b2.get('btns', [])
        ok &= T('B4', '저장 뒤 「📚 교재 자리」 — 첫 줄 = 「찍어 둔 자리」 p.%d + 그림 + 「자동으로 되돌리기」' % (guess + OFF5), good, {'줄': (b2 or {}).get('rows'), '단추': (b2 or {}).get('btns'), '그림': (b2 or {}).get('pic')})
        # 새로고침 뒤
        p.pg.reload()
        p.pg.wait_for_function("typeof S!=='undefined' && typeof busy!=='undefined' && !busy && window.__RB", timeout=90000)
        p.idle()
        p.ev(B5_JS)
        on, at, b3_ = open_box(p, c)
        r0 = ((b3_ or {}).get('rows') or [{}])[0]
        ok &= T('B4', '새로고침 뒤 — 찍어 둔 자리 그대로 첫 줄', bool(b3_) and '찍어 둔 자리' in r0.get('m', []) and r0.get('p') == 'p.%d' % (guess + OFF5), {'줄': (b3_ or {}).get('rows')})
        # 다른 기기(같은 가짜 원격)
        q = open_pg(br, src, PC, keep_remote=True, tag=p._tag)
        try:
            q.wait(800)
            on, at, bq = open_box(q, c)
            r0 = ((bq or {}).get('rows') or [{}])[0]
            ok &= T('B4', '다른 기기(가짜 원격으로 받음) — 같은 칸 v5|%s · 첫 줄 = 찍어 둔 자리 · 쪽 같음' % u,
                    bool(bq) and '찍어 둔 자리' in r0.get('m', []) and r0.get('p') == 'p.%d' % (guess + OFF5) and bool(q.ev("(k) => __B5.pin(k)", 'v5|' + u)), {'줄': (bq or {}).get('rows')})
        finally:
            q.close()
        # 되돌리기
        press(p, p.ev("() => __B5.btnAt('자동으로 되돌리기')"), 700)
        b4_ = p.ev("() => __B5.boxReady()")
        rec2 = p.ev("(k) => __B5.pin(k)", 'v5|' + u)
        ok &= T('B4', '「자동으로 되돌리기」 → 칸 {auto:true}(안 지움) · 창 = 「뷰객 5판 — 자리 없음 · 직접 찍기」', bool(rec2) and rec2.get('auto') is True and bool(b4_) and '뷰객 5판 — 자리 없음 · 직접 찍기' in b4_.get('none', []),
                {'기록': rec2, '창': {x: (b4_ or {}).get(x) for x in ('none', 'rows', 'btns')}})
        return ok
    finally:
        p.close()


def b4_orph(br, src):
    """민소 정리캔버스 「교재 확정 N 고아」 — 1차객 교재 손값 칸(v5|uid)은 블록이 아니라 세지 않는다"""
    seed = {'jopangi.canvasjari': {'v5|SV110001': {'by': 'hand', 'b': DOC5, 'p': 22, 'r': [0.1, 0.2, 0.9, 0.3], 't': 1759420800000}}}
    p = open_pg(br, src, PC, ls=seed)
    try:
        o = p.ev("() => __B5.orph()")
        return T('B4', '민소 정리 탭 캔버스 머리 「교재 확정 N 고아」 — 1차객 5판 칸(v5|uid)은 세지 않음(배지 숨음 · 글 없음)', bool(o) is True and not o.get('t'), o)
    finally:
        p.close()


def b5(br, src):
    ok = True
    p = open_pg(br, src)
    try:
        c = C_BOOK
        BOOKREQ.clear()
        on, at, b = open_box(p, c)
        press(p, p.ev("() => __B5.rowAt(0)"), 600)
        k = p.ev("(d) => __B5.bookReady(d)", DOC5)
        n1 = BOOKREQ['pdf/%s.pdf' % DOC5]
        idb = None
        for _ in range(60):
            idb = p.ev("(k) => __B5.idb(k)", 'bookpdf:' + DOC5)
            if idb and idb.get('has'):
                break
            p.wait(250)
        good = k.get('from') == 'net' and n1 >= 1 and bool(idb) and idb.get('has') and idb.get('md5') == META5['pdfMd5'] and idb.get('n') == len(PDF5)
        ok &= T('B5', '첫 열기 = 저장소에서 받음(PDF 요청 %d) → IndexedDB ox_master_db/rows 「bookpdf:tm_view5」(pdfMd5 = 책메타 %s · %d B)' % (n1, META5['pdfMd5'][:8], len(PDF5)), good,
                {'창': {x: k.get(x) for x in ('from', 'pages', 'nav')}, 'idb': idb})
        p.pg.reload()
        p.pg.wait_for_function("typeof S!=='undefined' && typeof busy!=='undefined' && !busy && window.__RB", timeout=90000)
        p.idle()
        p.ev(B5_JS)
        BOOKREQ.clear()
        on, at, b = open_box(p, c)
        press(p, p.ev("() => __B5.rowAt(0)"), 600)
        k2 = p.ev("(d) => __B5.bookReady(d)", DOC5)
        n2 = BOOKREQ['pdf/%s.pdf' % DOC5]
        ok &= T('B5', '새로고침 뒤 두 번째 열기 = 이 기기에 재운 것(PDF 요청 0 · from cache · 「이 기기에 재워 둔 것」)', k2.get('from') == 'cache' and n2 == 0 and '이 기기에 재워 둔 것' in k2.get('nav', ''),
                {'창': {x: k2.get(x) for x in ('from', 'nav')}, 'PDF 요청': n2})
        # 교재에서 찾기
        q = '시험낱말뷰객'
        hits = [(i + 1, t.count(q)) for i, t in enumerate(TXT5['t']) if q in t]
        tot = sum(n for _, n in hits)
        press(p, p.ev("(d) => __B5.bookAt(d, 'bsin')", DOC5), 200)
        p.pg.keyboard.type(q)
        p.pg.keyboard.press('Enter')
        p.wait(700)
        k3 = p.ev("(d) => __B5.book(d)", DOC5)
        good = k3.get('bsRows') == tot and ('%d곳' % tot) in k3.get('bsList', '') and ('%d쪽' % len(hits)) in k3.get('bsList', '')
        ok &= T('B5', '「교재에서 찾기」 「%s」 → 목록 %d쪽 %d곳(쪽 글 글.json.gz)' % (q, len(hits), tot), good, {'목록': k3.get('bsList'), '줄': k3.get('bsRows'), '기대': hits})
        last = len(hits) and hits[-1]
        press(p, p.ev("([d, j]) => __B5.bookAt(d, 'res', j)", [DOC5, tot - 1]), 900)
        k4 = p.ev("(d) => __B5.book(d)", DOC5)
        for _ in range(20):
            if k4.get('hits') == last[1]:
                break
            p.wait(200)
            k4 = p.ev("(d) => __B5.book(d)", DOC5)
        ok &= T('B5', '찾은 곳(끝 줄) 누름 → PDF %d 쪽 · 노란 상자 %d(누른 곳 주황 테 1)' % (last[0], last[1]), k4.get('page') == last[0] and k4.get('hits') == last[1] and k4.get('cur') >= 1,
                {'창': {x: k4.get(x) for x in ('page', 'hits', 'cur', 'bsList')}})
        return ok
    finally:
        p.close()


B6_BOX = r"""async ([kind, id, dom, u]) => { const w = ms => new Promise(r => setTimeout(r, ms)); await __B5.go(kind, id, dom, '특허법');
  const at = __B5.idAt(dom, u); return at; }"""


def b6(br, src, base_src):
    ok = True
    # 박힌 자리 — 주석 밖 'patent_hr8' 글자(책 표 정의 하나만)
    def places(s):
        out = []
        for m in re.finditer(r'patent_hr8', s):
            a = m.start()
            if s.rfind('/*', 0, a) > s.rfind('*/', 0, a):
                continue   # 덩이 주석 안
            ln0 = s.rfind('\n', 0, a) + 1
            line = s[ln0:a]
            if re.search(r'(^|\s)//', line):
                continue
            out.append(s[ln0:s.find('\n', a)].strip()[:90])
        return out
    pn, pb = places(src), places(base_src)
    ok &= T('B6', 'patent_hr8 박힌 자리 = 책 표 하나(주석 밖 글자 %d · 바탕 %d)' % (len(pn), len(pb)), len(pn) == 1 and 'BOOK_TB' in pn[0], {'새': pn, '바탕': pb})
    if YARD:
        return ok
    got = {}
    for who, s in (('new', src), ('base', base_src)):
        p = open_pg(br, s)
        try:
            out = {}
            for c in P8S:
                at = p.ev(B6_BOX, list(c))
                press(p, at)
                b = p.ev("() => __B5.boxReady()")
                out[c[3]] = {'html': (b or {}).get('html'), 'omr': (b or {}).get('omr'), 'rows': [(r['k'], r['p'], r['m'], len(r['sn'] or '')) for r in (b or {}).get('rows') or []], 'btns': (b or {}).get('btns')} if b else None   # 둘째 줄 글 = 길이만(책 글 안 찍음)
                if c is P8S[0] and b and b.get('rows'):
                    press(p, p.ev("() => __B5.rowAt(0)"), 600)
                    k = p.ev("(d) => __B5.bookReady(d)", DOC8)
                    out['book'] = {x: k.get(x) for x in ('n', 'title', 'nav', 'page', 'hl', 'bs', 'err')}
                    if k.get('bs'):
                        press(p, p.ev("(d) => __B5.bookAt(d, 'bsin')", DOC8), 200)
                        p.pg.keyboard.type(SEARCH8 if FX8[0] else '특허')
                        p.pg.keyboard.press('Enter')
                        p.wait(900)
                        kb_ = p.ev("(d) => __B5.book(d)", DOC8)
                        m_ = re.search(r'총 (\d+)쪽 · (\d+)곳', kb_.get('bsList') or '')
                        out['book']['찾기'] = {'낱말': '시험 낱말' if FX8[0] else '특허', '쪽': int(m_.group(1)) if m_ else None, '곳': int(m_.group(2)) if m_ else None, '줄': kb_.get('bsRows')}   # 수만(책 글 안 찍음)
                    p.ev("() => __B5.closeAll()")
                    # 찍기 → 저장(특허 칸 p8|uid)
                    at = p.ev(B6_BOX, list(c))
                    press(p, at)
                    p.ev("() => __B5.boxReady()")
                    press(p, p.ev("() => __B5.btnAt('자리 직접 찍기')"), 700)
                    p.ev("(d) => __B5.bookReady(d)", DOC8)
                    pg = p.ev("(d) => __B5.bookAt(d, 'pg')", DOC8)
                    if pg:
                        drag(p, pg['x'] + pg['w'] * 0.25, pg['y'] + pg['h'] * 0.5, pg['x'] + pg['w'] * 0.75, pg['y'] + pg['h'] * 0.56)
                    press(p, p.ev("(d) => __B5.bookAt(d, 'sv')", DOC8), 700)
                    rec = p.ev("(k) => __B5.pin(k)", 'p8|' + c[3]) or {}
                    out['pick'] = {'rec': {x: rec.get(x) for x in ('by', 'b', 'p', 'r')}, 'toast': p.ev("() => __B5.toast()"), 'v5': [k for k in p.ev("() => __B5.keys()") if k.startswith('v5|')]}
                p.ev("() => __B5.closeAll()")
            out['api'] = p.ev("() => __B5.api()")   # 특허 카드를 연 뒤(VJ = 특허) — p8Guess 가 표본 줄 쪽을 잰다
            got[who] = out
        finally:
            p.close()
    n, b = got['new'], got['base']
    def brief(x):
        return {'omr': x.get('omr'), 'rows': x.get('rows'), 'btns': x.get('btns'), 'html md5': hashlib.md5((x.get('html') or '').encode('utf-8')).hexdigest()[:12]} if x else None
    for c in P8S:
        ok &= T('B6', '특허 %s(%s) 「📚 교재 자리」 — 정리OMR 줄 · 8판 칸 DOM(줄 · 둘째 줄 글 · 단추) = 바탕' % (c[1], c[3]), n.get(c[3]) == b.get(c[3]) and bool((n.get(c[3]) or {}).get('html')),
                {'새': brief(n.get(c[3])), '바탕': brief(b.get(c[3]))})
    ok &= T('B6', '특허 8판 교재 창(1등 줄) — 제목 · 머리 · 쪽 · 노란 상자 · 「교재에서 찾기」 칸 · 찾기 쪽·곳 수 = 바탕', n.get('book') == b.get('book') and bool(n.get('book')) and n['book'].get('title') == '📘 특허법 해례 8판'
            and n['book'].get('bs') and bool((n['book'].get('찾기') or {}).get('줄')), {'새': n.get('book'), '바탕': b.get('book')})
    ok &= T('B6', '특허 찍기 → 저장 — 칸 p8|uid {by · b:patent_hr8 · p · r} · 알림 「해례 8판 p.N」 = 바탕 · v5 칸 0', n.get('pick') == b.get('pick') and (n.get('pick') or {}).get('rec', {}).get('b') == DOC8 and '해례 8판 p.' in (n.get('pick') or {}).get('toast', ''),
            {'새': n.get('pick'), '바탕': b.get('pick')})
    na, ba = dict(n.get('api') or {}), dict(b.get('api') or {})
    nm5 = na.pop('name5', None)
    ba.pop('name5', None)
    ok &= T('B6', 'k8 · meta8 · book8 · p8Guess(표본 셋 · 특허 재료 뒤) · 8판 이름 = 바탕 · 5판 이름 「상표법 뷰객 5판」', na == ba and na.get('k8') and nm5 == '상표법 뷰객 5판' and any(x and x > 1 for x in (na.get('guess') or [])),
            {'새': n.get('api'), '바탕': b.get('api')})
    return ok


def b0():
    ok = True
    md5 = hashlib.md5(PDF5).hexdigest()
    pages = sorted({s['p'] for k, v in MAP5.items() if k != '_meta' for s in v})
    ok &= T('B0', '시험 자료 꼴 — 책메타 tm_view5 · pages 549 · printOffset −11 · pageHash 549 · 시험 PDF md5 = 책메타 = 글.json.gz pdfMd5 · 대응표 uid 셋(_meta) · 대응표 쪽마다 쪽 글자층',
            META5.get('docid') == DOC5 and META5.get('pages') == 549 and META5.get('printOffset') == -11 and len(META5.get('pageHash') or []) == 549 and md5 == META5.get('pdfMd5') == TXT5.get('pdfMd5')
            and '_meta' in MAP5 and len([k for k in MAP5 if k != '_meta']) == 3 and all(os.path.isfile(os.path.join(FX, 'ox_book_%s_p%d.json.gz' % (DOC5, x))) for x in pages) and len(TXT5.get('t') or []) == 549,
            {'pdf': [len(PDF5), md5], '책메타': {k: META5.get(k) for k in ('docid', 'pages', 'printOffset', 'pdfMd5')}, '대응 쪽': pages})
    return ok


def webkit_try(pw):
    try:
        return pw.webkit.launch()
    except Exception as e:
        N('WK', 'WebKit 안 잼', str(e).splitlines()[0][:160])
        return None


def main():
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    src = app_src(NEW)
    base_src = app_src(BASE)
    if YARD:
        src = base_src
    print('══ sp_book5 §A-4 %s · 바탕 %s · 앱 md5(LF) %s · 바탕 %s · /__book/ 덧판 %s' % ('헛잣대' if YARD else '새 판', BASE, md5lf(src), md5lf(base_src), BOOK))
    got, times = {}, {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        steps = [('B0', lambda: b0()), ('B3', lambda: b3(br, src)), ('B3-폰', lambda: b3(br, src, PHONE, 'B3-폰')), ('B4', lambda: b4(br, src) & b4_orph(br, src)),
                 ('B5', lambda: b5(br, src)), ('B6', lambda: b6(br, src, base_src))]
        for g, fn in steps:
            if ONLY and not any(g.upper() == o or g.upper().startswith(o) for o in ONLY):
                continue
            if YARD and g == 'B0':
                continue
            print('── %s' % g, flush=True)
            t1 = time.time()
            try:
                got[g] = bool(fn())
            except Exception as e:
                got[g] = False
                T(g, '돌다 멈춤', False, repr(e)[:300])
            times[g] = round(time.time() - t1)
            print('   (%s %d초)' % (g, times[g]), flush=True)
        br.close()
        if 'webkit' in ENGS and not YARD and (not ONLY or any(o.startswith('B3') for o in ONLY)):
            wk = webkit_try(pw)
            if wk:
                try:
                    got['B3-wk'] = bool(b3(wk, src, PHONE, 'B3-wk'))
                finally:
                    wk.close()
    lines = []
    print('\n══ 요약 (%.0f초)%s' % (time.time() - t0, ' — 헛잣대' if YARD else ''))
    for g in got:
        cells = [r for r in RES if r[0] == g and r[2] is not None]
        nf = sum(1 for r in cells if not r[2])
        verdict = (('FAIL(헛잣대 통과)' if not got[g] else 'PASS(헛잣대 실패)') if YARD else ('PASS' if got[g] else 'FAIL'))
        s = '  %-6s %s (%d 칸 중 FAIL %d · %s초)' % (g, verdict, len(cells), nf, times.get(g, '-'))
        print(s)
        lines.append(s)
    os.makedirs(os.path.dirname(os.path.abspath(OUTF)), exist_ok=True)
    with open(OUTF, 'w', encoding='utf-8', newline='\n') as f:
        for r in RES:
            d = r[3] if isinstance(r[3], str) else json.dumps(r[3], ensure_ascii=False, default=str)
            f.write('%s | %s · %s | %s\n' % ('INFO' if r[2] is None else ('PASS' if r[2] else 'FAIL'), r[0], r[1], d))
        f.write('\n'.join(lines) + '\n')
    print('결과 → %s' % OUTF)


if __name__ == '__main__':
    main()
