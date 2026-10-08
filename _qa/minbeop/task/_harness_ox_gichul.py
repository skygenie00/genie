# -*- coding: utf-8 -*-
"""민법OX 기출 칩 → 시험지 팝업 · 교재 팝업 쪽 입력 · 근거 지울 때 걸린 문항 — _task_ox_gichul_pdf §D.

  NEW  = genie 작업트리 minbeop/index.html (고친 판)
  HEAD = git HEAD 의 같은 파일 (헛잣대 · G7 — 여기서 G2·G3 은 **실패해야** 한다)

⚠ 헤드리스가 진짜 망에 안 나간다 — `fetch` 를 갈아 끼워
    · 같은 출처(`/gichul/pdf/…` · `/vendor/…`)만 지나가고
    · `api.github.com` 은 이 스크립트가 띄운 서버의 `/gh/<repo>/<path>` 로 돌린다(로컬 클론에서 읽는다)
    · 나머지 바깥 주소는 통째로 거절한다
⚠ pdf.js 는 CDN 을 안 쓴다 — 한 번 받아 `OUT/vendor` 에 두고 **앱 사본의 상수를 그 자리로 고쳐** 쓴다.
⚠ `window.onload` 는 끈다(가상 시계보다 늦게 끝나 거짓 FAIL 이 난다) · 결과는 `console.log('HZR|…')` 로 stderr 에서 받는다.

쓰기 : python _harness_ox_gichul.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2(10/8) 실행 모드 --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같음) · import 때 --mode · --snap-in · --snap-out 을 sys.argv 에서 뗀다
import gzip, hashlib, io, json, os, re, shutil, socket, subprocess, sys, tempfile, threading, time, urllib.parse, urllib.request
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

sys.stdout.reconfigure(encoding='utf-8')

GENIE = _roots.genie()
SPD = _roots.spd()
MBPDF = _roots.mbpdf()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(tempfile.gettempdir(), 'h_gichul')
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
REL = 'minbeop/index.html'
PDFDIR = os.path.join(GENIE, 'gichul', 'pdf')
PATCH = r'2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2020 2022 2025'.split()
OCR5 = ['2009-1-minbeop.pdf', '2010-1-minbeop.pdf', '2020-1-minbeop.pdf',
        '2022-1-minbeop.pdf', '2025-1-minbeop.pdf']
G3KEY = '재단법인의 설립을 위하여 서면에 의해 출연'
CDN = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/'

RES = []          # (gate, ok, text)


def add(gate, ok, text):
    RES.append((gate, ok, text))
    print('  %s %-4s %s' % ('OK  ' if ok else 'FAIL', gate, text))


def git(*a):
    r = subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a),
                       capture_output=True)
    return r.stdout


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def _rg_md5(v):
    """qa_slim2 regress — 기준 칸 값 줄이기(항목 글 → md5) · gate 에서 안 쓴다"""
    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def _rg_smp(g, t, P):
    """qa_slim2 regress — 표본으로 줄인 칸(시험지 색인 「1~40 각 한 번」)은 값 끝에 「(표본 n/N)」"""
    if g in ('G3', 'G4') and '1~40 각 한 번' in t:
        return t + ' (표본 %d/%d)' % (len(P['files']), 1 + len(OCR5))
    return t


# ══════════════════════════════════════════════════════════════════════════
# G1 · 파일 잣대 (브라우저 없이)
# ══════════════════════════════════════════════════════════════════════════
def gate_files():
    print('\n=== G1 list.json · PDF 13장 ===')
    lst = json.load(io.open(os.path.join(PDFDIR, 'list.json'), encoding='utf-8'))
    add('G1', lst['count'] == 104, 'count = %s (바람 104)' % lst['count'])
    add('G1', len(lst['items']) == 104, 'items = %d' % len(lst['items']))

    patch = json.load(io.open(PATCHJSON, encoding='utf-8'))
    pit = {x['file']: x for x in patch['items']}

    ok = 0
    for f, it in pit.items():
        b = io.open(os.path.join(PDFDIR, f), 'rb').read()
        row = next((x for x in lst['items'] if x['file'] == f), None)
        good = row and row['hash'] == sha256(b) == it['hash'] and row['bytes'] == len(b) == it['bytes']
        ok += bool(good)
        if not good:
            add('G1', False, '%s 어긋남' % f)
    add('G1', ok == 13, '13장 sha256·bytes = 클론 파일 = list_patch : %d/13' % ok)

    # 나머지 91 항목이 HEAD 판과 한 글자도 안 다른가
    if QC.GATE:
        QC.sub('git:show-data')
        old = json.loads(git('show', 'HEAD:gichul/pdf/list.json').decode('utf-8'))
        touched = set(pit)
        oldm = {x['file']: x for x in old['items']}
        diff = [x['file'] for x in lst['items']
                if x['file'] not in touched and json.dumps(oldm.get(x['file']), sort_keys=True, ensure_ascii=False)
                != json.dumps(x, sort_keys=True, ensure_ascii=False)]
    else:   # regress — HEAD 판 list.json 대신 기준 스냅샷(앞 인도판 새 판 list.json 항목마다 md5)
        touched = set(pit)
        oldm = QC.base('G1/list_items', {x['file']: _rg_md5(json.dumps(x, sort_keys=True, ensure_ascii=False)) for x in lst['items']})
        diff = [x['file'] for x in lst['items']
                if x['file'] not in touched and oldm.get(x['file']) != _rg_md5(json.dumps(x, sort_keys=True, ensure_ascii=False))]
    add('G1', not diff, '나머지 %d 항목 무변 (diff %d) %s' % (104 - 13, len(diff), diff[:4]))
    if QC.GATE:   # 헛잣대 — HEAD 판 count 94(그 판에만 뜻) = 관문만
        add('G1', len(old['items']) == 94, 'HEAD 판 count = %d' % len(old['items']))
    return lst


def gate_years(lst):
    print('\n=== G2(파일쪽) 마스터 연도 ⊆ list.json ===')
    rows = json.load(io.open(os.path.join(SPD, 'minbeop', '문항마스터.json'), encoding='utf-8'))['rows']
    years, toks = set(), 0
    for r in rows:
        raw = str(r.get('출제연도', '')).strip()
        if not raw:
            continue
        for t in re.split(r'[,\s;/]+', raw):
            if not t:
                continue
            toks += 1
            years.add(t.split(':')[0])
    have = {x['file'] for x in lst['items']}
    miss = sorted(y for y in years if ('%s-1-minbeop.pdf' % y) not in have)
    add('G2', not miss, '토큰 %d · 연도 %d(%s~%s) · 시험지 없는 해 %s'
        % (toks, len(years), min(years), max(years), miss or '0개'))
    return rows, sorted(years)


def gate_outside():
    """35번이 몇 쪽인지 **앱 밖에서** 잰다 — pdf.js 색인과 맞대 볼 잣대(도구가 달라야 잣대가 된다).

    ⚠ pdftotext 는 이 한컴 PDF 의 **한글을 못 읽는다**(글자가 통째로 빈다 · 2026-09-16 실측 —
      16쪽이 「35.   ? (   )」 처럼만 나온다). 「35.」 자리는 잡으니 **쪽 번호**만 그것으로 재고,
      글자 대조는 `pymupdf` 로 한다.
    """
    print('\n=== G3(파일쪽) 앱 밖에서 잰 2024 35번 쪽 ===')
    p = os.path.join(PDFDIR, '2024-1-minbeop.pdf')
    byno = None
    exe = shutil.which('pdftotext')
    if exe:
        QC.sub('pdftotext')
        r = subprocess.run([exe, '-layout', p, '-'], capture_output=True)
        pages = r.stdout.decode('utf-8', 'replace').split('\f')
        hit = [i + 1 for i, t in enumerate(pages) if re.search(r'^\s*35\s*[.．]', t, re.M)]
        add('G3', len(hit) == 1, 'pdftotext 가 본 35번 쪽 = %s' % hit)
        byno = hit[0] if len(hit) == 1 else None
    else:
        add('G3', False, 'pdftotext 없음')
    try:
        import pymupdf
    except Exception as e:
        add('G3', False, 'pymupdf 없음 %s' % e)
        return byno
    d = pymupdf.open(p)
    flat = [d[i].get_text().replace(' ', '').replace('\n', '') for i in range(d.page_count)]
    d.close()
    kk = [i + 1 for i, t in enumerate(flat) if G3KEY.replace(' ', '') in t]
    add('G3', len(kk) == 1, 'pymupdf 로 「%s」 가 있는 쪽 = %s' % (G3KEY, kk))
    if byno is not None and kk:
        add('G3', byno == kk[0], '두 도구가 같은 쪽을 가리킨다 (%s · %s)' % (byno, kk[0]))
    return byno if byno is not None else (kk[0] if kk else None)

def gate_guards():
    print('\n=== D11 가드 · 줄끝 ===')
    if QC.GATE:   # push 가드(g_push.cmd · .gitignore 글자) — 앱 회귀 아님 · 그 판 인도 가드 = 관문만
        g = io.open(GPUSH, 'rb').read().decode('cp949', 'replace')
        m = re.search(r'^set "PATHS=(.+?)"', g, re.M)
        paths = m.group(1).split() if m else []
        add('D11', 'gichul' in paths and 'minbeop' in paths,
            'ⓐ PATHS(%d) = %s' % (len(paths), ' '.join(paths)))
        # ⚠ 스크립트 머리의 rem 주석에 「Never "git add -A"」 라는 글이 있다 — 주석을 빼고 본다
        cmds = [l for l in g.split('\n') if not re.match(r'^\s*rem\b', l, re.I) and l.strip()]
        bad_add = [l.strip() for l in cmds if re.search(r'\badd\b[^\n]*\s-A\b', l)]
        add('D11', not bad_add, 'ⓒ `git add -A` 안 쓴다 (rem 뺀 명령 %d줄 · 걸린 줄 %s)' % (len(cmds), bad_add))
        stage = [l.strip() for l in cmds if re.search(r'git .*\badd\b', l)]
        add('D11', len(stage) == 1 and '%%P' in stage[0], '스테이징 줄은 PATHS 하나뿐 : %s' % stage)
        add('D11', 'gichul/pdf/' in g, 'ⓑ D21 예외(gichul/pdf/)가 스크립트에 있다')

        gi = io.open(os.path.join(GENIE, '.gitignore'), encoding='utf-8').read()
        add('D11', '!gichul/pdf/*.pdf' in gi, '.gitignore 에 !gichul/pdf/*.pdf')

    app = io.open(os.path.join(GENIE, REL), 'rb').read()
    add('D11', app.count(b'\r\n') == 0, '앱 작업트리 CRLF %d' % app.count(b'\r\n'))
    lj = io.open(os.path.join(PDFDIR, 'list.json'), 'rb').read()
    add('D11', lj.count(b'\r\n') == 0, 'list.json 작업트리 CRLF %d' % lj.count(b'\r\n'))

    # 기출서재 앱 무접촉
    # ⚠ autocrlf=true 라 작업트리 md5 와 blob md5 는 원래 다르다 — git 이 보는 diff 로 잰다
    if QC.GATE:   # git diff HEAD(기출서재 앱 무접촉) — 인도 가드 = 관문만
        d = git('diff', '--name-only', 'HEAD', '--', 'index.html').decode('utf-8').strip()
        add('G5', d == '', '기출서재 genie/index.html 무접촉 (git diff %r)' % d)

    # ox_q_coords · SYNC_KEYS 무변
    new = io.open(os.path.join(GENIE, REL), encoding='utf-8').read()
    if QC.GATE:
        QC.sub('git:show-app')
    oldsrc = git('show', 'HEAD:' + REL).decode('utf-8') if QC.GATE else None   # regress — HEAD 판을 안 푼다: 줄 · 코드 줄 기댓값 = 기준 스냅샷(앞 인도판 새 판 줄)
    for k in ('const SYNC_KEYS =', "var CO_KEY = 'ox_q_coords'"):
        a = [l for l in oldsrc.split('\n') if k in l] if QC.GATE else QC.base('G5/' + k.strip(), [l for l in new.split('\n') if k in l])
        b = [l for l in new.split('\n') if k in l]
        add('G5', a == b, '%s 줄 무변' % k.strip())

    def code_hits(txt, k):
        """주석이 아닌 줄에서만 센다 — 이 판이 더한 것은 「안 쓴다」는 주석뿐이다."""
        out = []
        for l in txt.split('\n'):
            t = l.strip()
            if not t or t.startswith(('*', '/*', '//', '⚠', '- ')):
                continue
            if k in l:
                out.append(t)
        return out

    a, b = (code_hits(oldsrc, 'ox_q_coords') if QC.GATE else QC.base('G5/ox_q_coords_code', code_hits(new, 'ox_q_coords'))), code_hits(new, 'ox_q_coords')
    add('G5', a == b, 'ox_q_coords 를 쓰는 **코드 줄** 무변 %d -> %d %s'
        % (len(a), len(b), [x[:60] for x in b if x not in a]))


# ══════════════════════════════════════════════════════════════════════════
# 헤드리스
# ══════════════════════════════════════════════════════════════════════════
class H(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def translate_path(self, path):
        p = urllib.parse.urlparse(path).path
        if p.startswith('/vendor/'):
            return os.path.join(OUT, 'vendor', os.path.basename(p))
        if p.startswith('/minbeop/h_'):
            return os.path.join(OUT, os.path.basename(p))
        if p.startswith('/gh/'):
            # /gh/<owner>/<repo>/<path…>
            rest = urllib.parse.unquote(p[4:])
            parts = rest.split('/', 2)
            if len(parts) == 3:
                repo, sub = parts[1], parts[2]
                root = MBPDF if repo == 'minbeoppdf' else SPD
                return os.path.join(root, *sub.split('/'))
        return SimpleHTTPRequestHandler.translate_path(self, path)


def serve():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    srv = ThreadingHTTPServer(('127.0.0.1', port), partial(H, directory=GENIE))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, port


def vendor():
    d = os.path.join(OUT, 'vendor')
    os.makedirs(d, exist_ok=True)
    for n in ('pdf.min.js', 'pdf.worker.min.js'):
        f = os.path.join(d, n)
        if os.path.exists(f) and os.path.getsize(f) > 100000:
            continue
        print('  pdf.js 받는 중 — %s' % n)
        with urllib.request.urlopen(CDN + n, timeout=120) as r:
            io.open(f, 'wb').write(r.read())
    return d


SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__CERR=[];(function(){var ce=console.error.bind(console);console.error=function(){try{__CERR.push(Array.prototype.map.call(arguments,function(x){return typeof x==='string'?x:(x&&x.message)||JSON.stringify(x)}).join(' '))}catch(e){}return ce.apply(null,arguments);};})();
window.__ALERTS=[];window.alert=function(m){__ALERTS.push(String(m));};
window.__CONFIRMS=[];window.__CONFIRM_ANS=true;window.confirm=function(m){__CONFIRMS.push(String(m));return window.__CONFIRM_ANS;};window.prompt=function(){return null;};
(function(){
  var real=window.fetch.bind(window);
  var GH=/^https:\/\/api\.github\.com\/repos\/([^/]+)\/([^/]+)\/contents\/([^?]+)/;
  window.__NET=[];
  window.fetch=function(u,o){
    var s=String((u&&u.url)||u||'');
    var m=GH.exec(s);
    if(m){ window.__NET.push('gh:'+m[2]+'/'+decodeURIComponent(m[3])); return real('/gh/'+m[1]+'/'+m[2]+'/'+m[3]); }
    if(/^https?:\/\//.test(s) && s.indexOf(location.origin)!==0){ window.__NET.push('BLOCK:'+s); return Promise.reject(new Error('harness blocked '+s)); }
    window.__NET.push('ok:'+s);
    return real(u,o);
  };
})();
localStorage.clear();
</script>"""


def build(tag, src, tests, port):
    html = src.replace(CDN + 'pdf.min.js', '/vendor/pdf.min.js') \
              .replace(CDN + 'pdf.worker.min.js', '/vendor/pdf.worker.min.js')
    b = html.index('<body')
    bb = html.index('>', b) + 1
    html = html[:bb] + SEED + html[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + tests + '\n</script>\n' + html[e:]
    name = 'h_%s.html' % tag
    io.open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n').write(html)
    return 'http://127.0.0.1:%d/minbeop/%s' % (port, name)


def run(tag, url, budget=900000):
    prof = os.path.join(OUT, 'prof_' + tag)
    shutil.rmtree(prof, ignore_errors=True)
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
                        '--no-default-browser-check', '--user-data-dir=' + prof,
                        '--window-size=1280,900', '--enable-logging=stderr', '--v=0',
                        '--virtual-time-budget=%d' % budget, '--dump-dom', url],
                       capture_output=True, timeout=1800)
    err = r.stderr.decode('utf-8', 'replace')
    io.open(os.path.join(OUT, 'chrome_err_%s.txt' % tag), 'w', encoding='utf-8').write(err)
    hz = []
    for ln in err.split('\n'):
        i = ln.find('"HZR|')
        if i >= 0:
            j = ln.find('"', i + 5)
            hz.append(urllib.parse.unquote(ln[i + 5:j]))
    print('  [%s] chrome rc %s · HZR %d' % (tag, r.returncode, len(hz)))
    if hz and hz[-1] == 'END':
        return [x for x in hz[:-1] if x.strip()]
    io.open(os.path.join(OUT, 'hz_%s.txt' % tag), 'w', encoding='utf-8').write('\n'.join(hz))
    return hz or None


def payload(rows, years):
    keep = ['uid', '번호', '하위', '문제', '정답', '해설', '과목', '장', '세부단원', '구분',
            '기출연도', '회차', '문번', '지문', '출제연도', '출처', '상태', '메모', '개념', '암기', '중요']
    bset = {s['uid'] for s in BORDER}
    out, chip = [], []
    for r in rows:
        if not r.get('uid') or not r.get('문제'):
            continue
        has_exam = bool(str(r.get('출제연도', '')).strip())
        if not (has_exam or r['uid'] in bset):
            continue
        o = {k: r.get(k, '') for k in keep}
        if r['uid'] not in bset:
            o['해설'] = str(o.get('해설', ''))[:400]
        out.append(o)
    # 칩을 그릴 문항 — 해마다 몇 개 + 여러 해 걸린 것 + Q0292
    per, multi = {}, []
    for r in out:
        raw = str(r.get('출제연도', '')).strip()
        if not raw:
            continue
        ts = [t for t in re.split(r'[,\s;/]+', raw) if t]
        if len(ts) > 1 and len(multi) < 12:
            multi.append(r['uid'])
        y = ts[0].split(':')[0]
        per.setdefault(y, [])
        if len(per[y]) < 4:
            per[y].append(r['uid'])
    ids = []
    for y in sorted(per):
        ids += per[y]
    ids += multi
    if 'Q0292' in {r['uid'] for r in out}:
        ids = ['Q0292'] + ids
    ids = list(dict.fromkeys(ids))[:110]
    return {'rows': out, 'chipIds': ids, 'years': years,
            'files': ['2024-1-minbeop.pdf'] + OCR5, 'g3key': G3KEY,
            'border': BORDER, 'nav': NAV, 'e': EPAY}


def load_border():
    """_border_eval.tsv 에서 표본 일곱 건 — 세 책이 다 들어가게 고르고, 고르는 차례를 고정한다."""
    p = os.path.join(os.path.dirname(HERE), 'out', '_border_eval.tsv')
    by = {}
    with io.open(p, encoding='utf-8') as f:
        head = f.readline().rstrip('\n').split('\t')
        iu, idc, ip, iok = head.index('uid'), head.index('docid'), head.index('p'), head.index('ok')
        for ln in f:
            c = ln.rstrip('\n').split('\t')
            if len(c) <= iok or c[iok] != '1':
                continue
            by.setdefault(c[idc], []).append({'uid': c[iu], 'docid': c[idc], 'p': int(c[ip])})
    out = []
    for d in sorted(by):
        rs = sorted(by[d], key=lambda x: (x['uid'], x['p']))
        step = max(1, len(rs) // 3)
        out += rs[::step][:3]
    return out[:7]


PATCHJSON = os.path.join(os.path.dirname(os.path.dirname(HERE)), '기출서재', 'gichul_new', 'list_patch.json')
GPUSH = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'g_push.cmd')

# 교재 쪽 이동 잣대 — 책메타.json 정본값(7_1 pages 605/off -10 · 7_2 pages 467/off +590 · 9 pages 847/off -11)
NAV = [
    {'name': '7_1 끝쪽에서 ▶ 는 채권법 1쪽', 'kind': 'step', 'docid': 'minbeop7_1', 'p': 605, 'dir': 1, 'want': 'minbeop7_2:1'},
    {'name': '7_2 첫쪽에서 ◀ 는 민총물권 끝쪽', 'kind': 'step', 'docid': 'minbeop7_2', 'p': 1, 'dir': -1, 'want': 'minbeop7_1:605'},
    {'name': '7_2 끝쪽에서 ▶ 는 없다', 'kind': 'step', 'docid': 'minbeop7_2', 'p': 467, 'dir': 1, 'want': 'null'},
    {'name': '7_1 첫쪽에서 ◀ 는 없다', 'kind': 'step', 'docid': 'minbeop7_1', 'p': 1, 'dir': -1, 'want': 'null'},
    {'name': '9판 인쇄 100쪽 = PDF 111', 'kind': 'print', 'docid': 'minbeop9', 'v': 100, 'want': 'minbeop9:111'},
    {'name': '9판 인쇄 836쪽 = 끝쪽 847', 'kind': 'print', 'docid': 'minbeop9', 'v': 836, 'want': 'minbeop9:847'},
    {'name': '9판 인쇄 837쪽은 범위 밖', 'kind': 'print', 'docid': 'minbeop9', 'v': 837, 'want': 'null'},
    {'name': '7_1 인쇄 52쪽 = PDF 62', 'kind': 'print', 'docid': 'minbeop7_1', 'v': 52, 'want': 'minbeop7_1:62'},
    {'name': '7_1 에서 인쇄 700쪽은 채권법으로', 'kind': 'print', 'docid': 'minbeop7_1', 'v': 700, 'want': 'minbeop7_2:110'},
    {'name': '7_1 에서 인쇄 1058쪽은 범위 밖', 'kind': 'print', 'docid': 'minbeop7_1', 'v': 1058, 'want': 'null'},
]
EPAY = {'owner': 'Q0002', 'a': 'Q0001', 'b': 'Q0003', 'solo': 'Q0005'}
BORDER = []


def main():
    global BORDER
    if QC.SMOKE:   # smoke 칸 없음(A-0) — 앱을 띄우기 전에 한 줄 찍고 끝
        print('INFO | smoke 칸 없음 | 기출 칩 → 시험지 · 교재 쪽 · 근거 지울 때 걸린 문항 하네스 — smoke 칸 없음(A-0) · 앱 안 띄움', flush=True)
        return 0
    os.makedirs(OUT, exist_ok=True)
    print('OUT =', OUT)

    lst = gate_files()
    rows, years = gate_years(lst)
    pt_page = gate_outside() if QC.GATE else None   # regress(A-6) — PDF 전쪽 글자 뽑기(pdftotext · pymupdf) 0 · G3 쪽 대조는 기준 스냅샷
    gate_guards()

    BORDER = load_border()
    print('\n=== 헤드리스 ===')
    print('  G5 표본 —', ', '.join('%s@%s p%d' % (b['uid'], b['docid'], b['p']) for b in BORDER))
    vendor()
    srv, port = serve()
    tests = io.open(os.path.join(HERE, '_harness_ox_gichul_tests.js'), encoding='utf-8').read()
    P = payload(rows, years)
    if QC.REGRESS:   # regress(A-3 표본) — 시험지 색인(pdf.js 전쪽)은 2024(G3) + OCR 다섯 가운데 한 장(씨앗 고정) · 여섯 장 전수는 시험지 · 색인을 건드린 판의 관문(gate)
        P['files'] = ['2024-1-minbeop.pdf'] + QC.sample(OCR5, 1, 'ox_gichul')
    js = tests.replace('__P__', json.dumps(P, ensure_ascii=False))

    new_src = io.open(os.path.join(GENIE, REL), encoding='utf-8').read()
    if QC.GATE:
        QC.sub('git:show-app')
    head_src = git('show', 'HEAD:' + REL).decode('utf-8') if QC.GATE else None   # regress — HEAD 판을 안 푼다(G7 헛잣대 재료 · 사슬에선 HEAD = 새 판)

    outs = {}
    for tag, src in ((('NEW', new_src), ('HEAD', head_src)) if QC.GATE else (('NEW', new_src),)):   # regress — 새 판만
        QC.launch('new' if tag == 'NEW' else 'base')
        url = build(tag, src, js, port)
        outs[tag] = run(tag, url) or []
        io.open(os.path.join(OUT, 'lines_%s.txt' % tag), 'w', encoding='utf-8').write('\n'.join(outs[tag]))
    srv.shutdown()

    def vals(L):
        d = {}
        for x in L:
            if x.startswith('VAL | '):
                _, k, v = x.split(' | ', 2)
                d[k] = v
        return d

    print('\n=== 헤드리스 결과 (NEW) ===')
    for x in outs['NEW']:
        if x.startswith(('PASS', 'FAIL')):
            g = x.split(' | ')[1].split(' ')[0]
            add(g, x.startswith('PASS'), x.split(' | ', 1)[1] if QC.GATE else _rg_smp(g, x.split(' | ', 1)[1], P))
        elif x.startswith('INFO'):
            print('       ' + x)

    # G5 — 교재 테두리 NEW == HEAD
    vn, vh = vals(outs['NEW']), (vals(outs['HEAD']) if QC.GATE else QC.base('G5/border', {k: v for k, v in vals(outs['NEW']).items() if k.startswith('G5.border.')}))   # regress — 교재 테두리 기댓값 = 기준 스냅샷(앞 인도판 새 판 테두리 값)
    bk = [k for k in vn if k.startswith('G5.border.')]
    same = [k for k in bk if vn.get(k) == vh.get(k)]
    add('G5', bk and len(same) == len(bk),
        '교재 테두리 표본 %d건 NEW==HEAD %d건 %s'
        % (len(bk), len(same), [k for k in bk if k not in same][:3]))
    for k in sorted(bk):
        print('       %s = %s' % (k.replace('G5.border.', ''), vn.get(k)))

    # G3 — 색인 쪽이 pdftotext 와 같은가
    try:
        pg = json.loads(vn.get('page.2024-1-minbeop.pdf', '{}'))
        if QC.REGRESS:   # regress — pdftotext(앱 밖 PDF 전쪽 뽑기) 대신 기준 스냅샷(앞 인도판 새 판 pdf.js 색인 35번 쪽 — gate 에선 pdftotext 와 같았던 값)
            pt_page = QC.base('G3/page35', pg.get('35'))
        add('G3', pt_page is not None and str(pg.get('35')) == str(pt_page),
            'pdf.js 색인 35번 쪽 %s = pdftotext %s' % (pg.get('35'), pt_page))
    except Exception as e:
        add('G3', False, '쪽 대조 실패 %s' % e)

    # G7 — 헛잣대: 옛 판에서 G2·G3 이 실패해야 한다
    print('\n=== G7 헛잣대 (HEAD 판) ===')
    if QC.GATE:   # 헛잣대(옛 판 = HEAD) — 관문만
        hf = [x for x in outs['HEAD'] if x.startswith(('PASS', 'FAIL'))]
        for g in ('G2', 'G3'):
            gl = [x for x in hf if x.split(' | ')[1].split(' ')[0] == g]
            fails = [x for x in gl if x.startswith('FAIL')]
            add('G7', len(gl) > 0 and len(fails) > 0,
                '옛 판 %s : %d줄 중 FAIL %d' % (g, len(gl), len(fails)))
        add('G7', vh.get('SRC.mbExam') == '"undefined"',
            '옛 판에 mbExam 없음 (%s)' % vh.get('SRC.mbExam'))
    add('G7', vn.get('SRC.mbExam') == '"object"',
        '새 판에 mbExam 있음 (%s)' % vn.get('SRC.mbExam'))

    # 망 — 바깥으로 안 나갔는가
    for tag in (('NEW', 'HEAD') if QC.GATE else ('NEW',)):   # regress — 새 판만
        nv = vals(outs[tag]).get('NET.block', '[]')
        add('D11', nv in ('[]', 'null'), '%s 판이 막힌 바깥 주소를 부른 일 %s' % (tag, nv))

    print('\n' + '=' * 68)
    gs = {}
    for g, ok, _ in RES:
        a, b = gs.get(g, (0, 0))
        gs[g] = (a + (1 if ok else 0), b + 1)
    for g in sorted(gs):
        p, n = gs[g]
        print('  %-5s %d/%d %s' % (g, p, n, 'OK' if p == n else '*** FAIL'))
    bad = [(g, t) for g, ok, t in RES if not ok]
    print('  합계 %d/%d' % (sum(p for p, _ in gs.values()), sum(n for _, n in gs.values())))
    if bad:
        print('\n  못 넘은 것:')
        for g, t in bad:
            print('   - %-4s %s' % (g, t))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
