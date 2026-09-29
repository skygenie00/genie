# -*- coding: utf-8 -*-
"""민법OX 📋 정리 팝업(+add1 형광펜·토글 · +add2 진행중 버리기) 검산 — minbeop/task/_task_ox_jeongni_popup.md §G · add1 §4 · add2 §2.

  NEW  = genie 작업트리 minbeop/index.html
  HEAD = git HEAD (고치기 전 · 헛잣대)
  시험 글 = 같은 폴더의 _harness_jeongni_tests.js + _harness_jeongni_tests2.js
⚠ 앱 onload(IndexedDB 시동)는 끈다 · fetch 는 통째로 가짜(진짜 망에 안 나간다).
⚠ 결과는 DOM 이 아니라 console.log('HZR|…') 로 stderr 에서 받는다(민법OX 헤드리스 크롬은 시험 뒤 죽는 일이 있다).
⚠ G3 진짜 데이터 = studyplandata 클론 minbeop/문항마스터.json 행을 칸만 줄여 앱 buildQuizData 에 그대로 넣는다.
   묶음 수 기준값(§0)은 이 파일이 파이썬으로 따로 센다 — 앱이 그린 📋 수와 대조.
⚠ G1.l · G6 은 두 판에 같은 입력을 넣고 나온 글자를 파이썬이 대조한다(VAL 줄).

쓰기 : python _harness_jeongni.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import io, json, os, re, shutil, subprocess, sys, tempfile, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

GENIE = _roots.genie()
SP = _roots.spd()
REL = 'minbeop/index.html'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(tempfile.gettempdir(), 'h_jeongni')
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
GATES = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G12', 'G13', 'G14', 'G15']
JS_FILES = ('_harness_jeongni_tests.js', '_harness_jeongni_tests2a.js', '_harness_jeongni_tests2b.js', '_harness_jeongni_tests2c.js')
COLS = ['uid', '문제', '정답', '과목', '장', '세부단원', '구분', '기출연도', '회차', '문번', '지문', '출제연도', '번호', '하위']


def git(*a):
    r = subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a), capture_output=True)
    return r.stdout.decode('utf-8', 'replace')


def census(rows):
    """§0 — 과목별 소단원 행 수 · 「N.N」 묶음 수 (renderDashboard 가 모으는 규칙 그대로 · 필터 all)."""
    s = lambda v: '' if v is None else str(v).strip()
    grouped = {}
    for r in rows:
        if not r.get('uid') or not r.get('문제'):
            continue
        gubun = s(r.get('구분')) or '본편'
        sub = s(r.get('세부단원')) + ('(%s)' % gubun if gubun != '본편' else '')
        subj, chap = s(r.get('과목')), s(r.get('장'))
        yr = s(r.get('기출연도'))
        if yr:
            multi = s(r.get('출제연도'))
            for t in ([x for x in re.split(r'[,\s]+', multi) if x] if multi else [yr]):
                y = t.split(':')[0]
                ec = '%s년 제%s회' % (y, s(r.get('회차')) if y == yr else str(int(y) - 1963))
                grouped.setdefault('변리사 기출', {})[ec] = ec
        label = '%s > %s' % (chap, sub) if sub else chap
        grouped.setdefault(subj, {})[label] = sub or chap
    out = {}
    for subj, labels in grouped.items():
        keys = set()
        for label, sub in labels.items():
            m = re.match(r'^\d+\.\d+', sub)
            keys.add(m.group(0) if m else '@' + label)
        out[subj] = {'rows': len(labels), 'groups': len(keys)}
    return out


def build_and_run(tag, src, tests, budget=120000):
    html = src
    b = html.index('<body')
    bb = html.index('>', b) + 1
    html = html[:bb] + SEED + html[bb:]
    e = html.rindex('</body>')
    html = html[:e] + tests + html[e:]
    app = os.path.join(OUT, 'app_%s.html' % tag)
    io.open(app, 'w', encoding='utf-8', newline='\n').write(html)
    prof = os.path.join(OUT, 'prof_%s' % tag)
    shutil.rmtree(prof, ignore_errors=True)
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
                        '--user-data-dir=' + prof, '--allow-file-access-from-files', '--window-size=1280,900',
                        '--enable-logging=stderr', '--v=0',
                        '--virtual-time-budget=%d' % budget, '--dump-dom', 'file:///' + app.replace('\\', '/')],
                       capture_output=True, timeout=900)
    err = r.stderr.decode('utf-8', 'replace')
    io.open(os.path.join(OUT, 'chrome_err_%s.txt' % tag), 'w', encoding='utf-8').write(err)
    hz = []
    for ln in err.split('\n'):
        i = ln.find('"HZR|')
        if i >= 0:
            j = ln.find('"', i + 5)
            hz.append(urllib.parse.unquote(ln[i + 5:j]))
    if os.environ.get('HZ_LOG'):
        print('  [%s] chrome rc %s · HZR 줄 %d' % (tag, r.returncode, len(hz)))
    if hz and hz[-1] == 'END':
        return [x for x in hz[:-1] if x.strip()]
    io.open(os.path.join(OUT, 'dom_%s.html' % tag), 'w', encoding='utf-8').write(r.stdout.decode('utf-8', 'replace'))
    return None


def gate_of(line):
    try:
        return line.split(' | ')[1].split(' ')[0]
    except Exception:
        return ''


def tally(lines, g):
    ls_ = [x for x in (lines or []) if x.startswith(('PASS', 'FAIL')) and gate_of(x) == g]
    if not ls_:
        return '—'
    p = sum(1 for x in ls_ if x.startswith('PASS'))
    return '%dP/%dF' % (p, len(ls_) - p)


def main():
    os.makedirs(OUT, exist_ok=True)
    new = io.open(os.path.join(GENIE, REL.replace('/', os.sep)), encoding='utf-8', newline='').read()
    head = git('show', 'HEAD:' + REL)
    M = json.load(io.open(os.path.join(SP, 'minbeop', '문항마스터.json'), encoding='utf-8'))
    cen = census(M['rows'])
    print('§0 묶음 기준값(파이썬) : %s · 합 %d' % (json.dumps(cen, ensure_ascii=False), sum(v['groups'] for v in cen.values())))
    rows = [{k: (str(r.get(k)) if r.get(k) is not None else '') for k in COLS} for r in M['rows'] if r.get('uid') and r.get('문제')]
    for r in rows:
        r['문제'] = 'x'
    base = {'a': 'O', 'subject': '민법총칙', 'chapter': '1. 총칙', 'subChapter': '1.1 민법의 법원', 'subNum': '', 'pending': False,
            'examMeta': [], 'caseText': '', 'stem': '', 'status': '', 'excelLogic': '', 'panrye': ''}
    quiz = []
    spec = [('Q9901', 1, {'source': '변리사 20', 'panrye': '2000다1', 'q': '더미 지문 Q9901 — ' + '가나다라마바사아자차카타파하 ' * 6,
                          'exp': '더미 해설 Q9901 <b>꺾쇠</b> & 첫 줄\n둘째 줄'}),
            ('Q9902', 2, {'source': '', 'panrye': '2000다1', 'q': '더미 지문 Q9902 짧음', 'exp': '해설 Q9902'}),
            ('Q9903', 3, {'source': '변리사 21', 'excelLogic': '논리 글 하나', 'q': '더미 지문 Q9903', 'exp': '해설 Q9903'}),
            ('Q9904', 4, {'source': '변리사 22', 'subChapter': '1.2 신의칙', 'q': '더미 지문 Q9904', 'exp': '해설 Q9904'})]
    for u, n, extra in spec:
        quiz.append(dict(base, id=u, displayNo=n, probNum=n, **extra))
    quiz.append(dict(base, id='Q9905', q='기출 지문 Q9905', exp='기출 해설', displayNo=5, probNum=5, source='변리사 16',
                     examYear='2016', examRound='53', examYears=['2016'], examMeta=[{'year': '2016', 'round': '53', 'no': 1, 'opt': 1}],
                     examNo=1, examOpt=1, examNoBase=1, examOptBase=1, stem='다음 설명 중 옳은 것은?'))
    quiz.append(dict(base, id='Q9906', a='X', subChapter='1.1 민법의 법원(7판신설)', q='더미 지문 Q9906', exp='해설 Q9906', displayNo=6, probNum=6, source='변리사 23'))
    P = {'quiz': quiz, 'rows': rows, 'census': cen, 'censusTotal': sum(v['groups'] for v in cen.values()),
         'skip': [x for x in os.environ.get('HZ_SKIP', '').split(',') if x]}
    js = ''.join(io.open(os.path.join(HERE, f), encoding='utf-8').read() for f in JS_FILES)
    tests = '<script>\n' + js.replace('__P__', json.dumps(P, ensure_ascii=False).replace('</', '<\\/')) + '\n</script>\n'
    res = {}
    only = os.environ.get('HZ_ONLY')
    for tag, src in (('NEW', new), ('HEAD', head)):
        if only and tag != only:
            continue
        lines = build_and_run(tag, src, tests)
        res[tag] = lines
        print('=== %s 판 ===' % tag)
        if lines is None:
            print('  결과 줄 없음 → %s' % os.path.join(OUT, 'chrome_err_%s.txt' % tag))
            continue
        for ln in lines:
            if ln.startswith('VAL'):
                continue
            print('   ' + (ln if len(ln) < 700 else ln[:700] + ' …'))
        print('  합계 PASS %d · FAIL %d' % (sum(1 for x in lines if x.startswith('PASS')), sum(1 for x in lines if x.startswith('FAIL'))))
        print()

    print('=== 회귀 대조 — 같은 입력의 글자 (NEW vs HEAD) ===')
    vals = {t: [x for x in (res.get(t) or []) if x.startswith('VAL | ')] for t in ('NEW', 'HEAD')}
    rg = {}
    for a, b in zip(vals['NEW'], vals['HEAD']):
        name = a.split(' | ')[1]
        ok = a == b and name == b.split(' | ')[1]
        g = name.split('.')[0]
        rg.setdefault(g, []).append(ok)
        print('  %-24s %s' % (name, 'PASS 글자까지 같다' if ok else 'FAIL 다르다'))
        if not ok:
            io.open(os.path.join(OUT, 'val_%s_NEW.txt' % name), 'w', encoding='utf-8').write(a)
            io.open(os.path.join(OUT, 'val_%s_HEAD.txt' % name), 'w', encoding='utf-8').write(b)
    cnt_ok = len(vals['NEW']) == len(vals['HEAD']) and len(vals['NEW']) > 0
    print('  VAL 줄 NEW %d · HEAD %d' % (len(vals['NEW']), len(vals['HEAD'])))
    print()

    print('=== G10 소스 (NEW vs HEAD) ===')
    Ln, Lh = new.split('\n'), head.split('\n')
    lits = lambda t: sorted(set(re.findall(r"""['"`](ox_[a-z0-9_]+)['"`]""", t)))
    chk = [("pastBadgeHtml 줄 그대로", [s for s in Ln if 'pastBadgeHtml' in s] == [s for s in Lh if 'pastBadgeHtml' in s]),
           ('긴 줄(>3000자) 전부 글자까지 같다', [s for s in Ln if len(s) > 3000] == [s for s in Lh if len(s) > 3000]),
           ('SheetJS 929줄 바이트 무변', len(Ln) > 928 and Ln[928] == Lh[928] and len(Ln[928]) > 60000),
           ('SYNC_KEYS 무변', [s for s in Ln if 'const SYNC_KEYS = [' in s] == [s for s in Lh if 'const SYNC_KEYS = [' in s]),
           ("새 저장소 키 0 (ox_* 글자 집합 같다)", lits(new) == lits(head))]
    for name, ok in chk:
        print('  %-36s %s' % (name, 'PASS' if ok else 'FAIL'))
    if lits(new) != lits(head):
        print('   더해진 키 %s · 빠진 키 %s' % (sorted(set(lits(new)) - set(lits(head))), sorted(set(lits(head)) - set(lits(new)))))
    g10 = all(ok for _, ok in chk)
    print()

    print('=== 게이트 표 (NEW / HEAD) ===')
    allok = True
    for g in GATES:
        if g == 'G10':
            print('  %-4s NEW %-8s HEAD —(소스 대조 · push 때 D11 가드 따로)' % (g, 'PASS' if g10 else 'FAIL'))
            continue
        t = tally(res.get('NEW'), g)
        extra = ''
        vok = True
        if g in rg:
            vok = all(rg[g]) and cnt_ok
            extra = ' · 회귀 글자 %d/%d %s' % (sum(rg[g]), len(rg[g]), 'PASS' if vok else 'FAIL')
        tok = ('/0F' in t) if t != '—' else (g in rg)          # G6 은 회귀 글자 대조만 있는 게이트
        print('  %-4s NEW %-8s HEAD %-8s%s' % (g, t, tally(res.get('HEAD'), g), extra))
        allok = allok and vok and tok
    nf = res.get('NEW') is None or any(x.startswith('FAIL') for x in res['NEW'])
    ok = (not nf) and g10 and allok and cnt_ok
    print()
    print('종합 : %s' % ('ALL PASS' if ok else 'FAIL 있음'))
    return 0 if ok else 1


SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__CERR=[];(function(){var ce=console.error.bind(console);console.error=function(){try{__CERR.push(Array.prototype.map.call(arguments,function(x){return typeof x==='string'?x:(x&&x.message)||JSON.stringify(x)}).join(' '))}catch(e){}return ce.apply(null,arguments);};})();
window.__ALERTS=[];window.alert=function(m){__ALERTS.push(String(m));};
window.__CONFIRMS=[];window.__CONFIRM_ANS=true;window.confirm=function(m){__CONFIRMS.push(String(m));return window.__CONFIRM_ANS;};window.prompt=function(){return null;};
window.fetch=function(){return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));};
localStorage.clear();
</script>"""

if __name__ == '__main__':
    sys.exit(main())
