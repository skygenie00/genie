# -*- coding: utf-8 -*-
"""민법OX 논리 → 근거 흡수 · 논리 UI 걷기 검산 — minbeop/task/_task_ox_logic_merge.md §D.

  NEW  = genie 작업트리 minbeop/index.html
  HEAD = git HEAD (고치기 전 · 헛잣대)
  시험 글 = 같은 폴더의 _harness_logic_merge_tests.js
  기록 = studyplandata 클론 origin/main 의 minbeop/기록.json(읽기만) — G1·G2 샘플 5문항 · G7 자리
⚠ 앱 onload(IndexedDB 시동)는 끈다 · fetch 는 통째로 가짜(진짜 망에 안 나간다).
⚠ 결과는 console.log('HZR|…') 로 stderr 에서 받는다(민법OX 헤드리스 크롬은 시험 뒤 죽는 일이 있다).
⚠ VAL 줄(유사문제 저장 · 엑셀 내보내기)은 두 판에 같은 입력을 넣고 파이썬이 글자를 대조한다.

쓰기 : python _harness_logic_merge.py
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
OUT = os.path.join(tempfile.gettempdir(), 'h_logic_merge')
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
GATES = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G9', 'SRC']   # SRC = 소스 대조(지시서 G10 D11 가드·G11 Pages 는 push 때 따로)
JS_FILES = ('_harness_logic_merge_tests.js',)
GONE_FNS = ['logicOf', 'logicStore', 'logicCount', 'toggleLogic', 'revealLogic', 'ggBoxHasText', 'refBoxHTML', 'refBtnsHTML',
            'refChipsHTML', 'refSync', 'delRefId', 'refHasText', 'cmpFieldHTML']


def git(*a, repo=GENIE):
    r = subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True)
    return r.stdout.decode('utf-8', 'replace')


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
    print('  [%s] chrome rc %s · HZR 줄 %d' % (tag, r.returncode, len(hz)))
    if hz and hz[-1] == 'END':
        return [x for x in hz[:-1] if x.strip()]
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


def fn_lines(L, sig):
    idx = [i for i, s in enumerate(L) if len(s) < 3000 and sig in s]
    if len(idx) != 1:
        return None
    i = idx[0]
    ind = len(L[i]) - len(L[i].lstrip())
    for j in range(i + 1, len(L)):
        if L[j] == ' ' * ind + '}':
            return L[i:j + 1]
    return None


def record_sample():
    raw = subprocess.run(['git', '-C', SP, '-c', 'core.quotepath=false', 'show', 'origin/main:minbeop/기록.json'], capture_output=True).stdout
    rec = json.loads(raw.decode('utf-8'))
    data = rec.get('data') or {}
    lg = data.get('ox_q_logic') or {}
    ne = {k: str(v) for k, v in lg.items() if str(v or '').strip()}
    gg = data.get('ox_q_geunge') or {}
    ggu = {k: v for k, v in gg.items() if isinstance(v, list) and v}
    spec = lambda v: any(c in v for c in '<>&"\'\n')
    with_gg = sorted(set(ne) & set(ggu), key=lambda k: (not spec(ne[k]), k))[:2]
    no_gg = sorted((k for k in ne if k not in ggu), key=lambda k: (not spec(ne[k]), k))[:3]
    sample = {'logic': {k: lg[k] for k in with_gg + no_gg}, 'geunge': {k: gg[k] for k in with_gg},
              'srcLogicUid': with_gg[0], 'spec': [k for k in with_gg + no_gg if spec(ne[k])]}
    log = git('log', '-1', '--format=%h %ad', '--date=iso', 'origin/main', '--', 'minbeop/기록.json', repo=SP).strip()
    print('기록 origin/main %s · %d B · 논리 %d · 근거 문항 %d · 샘플 근거 있음 %s · 근거 없음 %s · src:logic 미리 %s' % (
        log, len(raw), len(ne), len(ggu), with_gg, no_gg, with_gg[0]))
    return sample, {'data': data, 'u': rec.get('u') or {}, 'gone': rec.get('gone') or {}}


def main():
    os.makedirs(OUT, exist_ok=True)
    new = io.open(os.path.join(GENIE, REL.replace('/', os.sep)), encoding='utf-8', newline='').read()
    head = git('show', 'HEAD:' + REL)
    print('HEAD %s' % git('log', '-1', '--format=%h %s').strip())
    sample, rec = record_sample()
    base = {'subject': '민법총칙', 'chapter': '1. 총칙', 'subChapter': '1.1 민법의 법원', 'subNum': '', 'examMeta': [],
            'caseText': '', 'stem': '', 'status': '', 'excelLogic': '', 'panrye': '', 'source': '변리사 20'}
    quiz = []
    for n in range(1, 26):
        u = 'Q98%02d' % n
        quiz.append(dict(base, id=u, a='O' if n % 2 else 'X', q='카드 지문 %s — 가나다라마바사아자차카타파하' % u, exp='카드 해설 %s\n둘째 줄' % u,
                         displayNo=n, probNum=n))
    quiz[2]['excelLogic'] = '논리 글 하나'
    for n, u in enumerate(sorted(sample['logic']), 1):          # 샘플 5문항 = 「1.2 논리 샘플」 단원
        quiz.append(dict(base, id=u, subChapter='1.2 논리 샘플', a='O', q='샘플 지문 %s' % u, exp='샘플 해설 %s' % u, displayNo=n, probNum=n))
    for no in range(1, 8):
        for opt in (1, 2):
            u = 'Q99%02d' % ((no - 1) * 2 + opt)
            quiz.append(dict(base, id=u, a='O' if opt == 1 else 'X', q='기출 지문 %s' % u, exp='기출 해설 %s' % u, displayNo=no, probNum=no,
                             subChapter='2.1 기출', source='변리사 16', examYear='2016', examRound='53', examYears=['2016'],
                             examMeta=[{'year': '2016', 'round': '53', 'no': no, 'opt': opt}], examNo=no, examOpt=opt, examNoBase=no, examOptBase=opt,
                             stem='%d. 다음 설명 중 옳은 것은?' % no))
    rows = [{'번호': 1, '문제': '카드 지문 Q9801', '정답': 'O', '해설': '해설', 'uid': 'Q9801', '과목': '민법총칙', '논리': '엑셀 원래 논리'},
            {'번호': 2, '문제': '카드 지문 Q9802', '정답': 'X', '해설': '해설', 'uid': 'Q9802', '과목': '민법총칙', '논리': ''}]
    P = {'quiz': quiz, 'sample': sample, 'rec': rec, 'rows': rows, 'skip': [x for x in os.environ.get('HZ_SKIP', '').split(',') if x]}
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
            if not ln.startswith('VAL'):
                print('   ' + (ln if len(ln) < 900 else ln[:900] + ' …'))
        print('  합계 PASS %d · FAIL %d' % (sum(1 for x in lines if x.startswith('PASS')), sum(1 for x in lines if x.startswith('FAIL'))))
        print()

    print('=== 회귀 대조 — 같은 입력의 글자 (NEW vs HEAD) ===')
    vals = {t: [x for x in (res.get(t) or []) if x.startswith('VAL | ')] for t in ('NEW', 'HEAD')}
    rg = {}
    for a, b in zip(vals['NEW'], vals['HEAD']):
        name = a.split(' | ')[1]
        ok = a == b and name == b.split(' | ')[1]
        rg.setdefault(name.split('.')[0], []).append(ok)
        print('  %-28s %s' % (name, 'PASS 글자까지 같다' if ok else 'FAIL 다르다'))
        if not ok:
            io.open(os.path.join(OUT, 'val_%s_NEW.txt' % name), 'w', encoding='utf-8').write(a)
            io.open(os.path.join(OUT, 'val_%s_HEAD.txt' % name), 'w', encoding='utf-8').write(b)
    cnt_ok = len(vals['NEW']) == len(vals['HEAD']) and len(vals['NEW']) > 0
    print('  VAL 줄 NEW %d · HEAD %d' % (len(vals['NEW']), len(vals['HEAD'])))
    print()

    print('=== SRC 소스 대조 (NEW vs HEAD · 지시서 §C·§B-4) ===')
    Ln, Lh = new.split('\n'), head.split('\n')
    lits = lambda t: sorted(set(re.findall(r"""['"`](ox_[a-z0-9_]+)['"`]""", t)))
    gg_head = sorted(set(re.findall(r'^\s*(?:async\s+)?function (gg[A-Za-z0-9_]*)\s*\(', head, re.M)) - {'ggMemoMergeBoot', 'ggBoxHasText'})
    gg_diff = [f for f in gg_head if fn_lines(Ln, 'function %s(' % f) != fn_lines(Lh, 'function %s(' % f) or fn_lines(Ln, 'function %s(' % f) is None]
    left = [f for f in GONE_FNS if re.search(r'\b%s\s*\(' % f, new)]
    chk = [('긴 줄(>3000자) 전부 글자까지 같다', [s for s in Ln if len(s) > 3000] == [s for s in Lh if len(s) > 3000]),
           ('SheetJS 줄(가장 긴 줄) 바이트 무변', max(Ln, key=len) == max(Lh, key=len) and len(max(Ln, key=len)) > 60000),
           ('SYNC_KEYS 무변', [s for s in Ln if 'const SYNC_KEYS = [' in s] == [s for s in Lh if 'const SYNC_KEYS = [' in s]),
           ('ox_* 글자 집합 = HEAD + ox_gg_logic_merged 하나', lits(new) == sorted(set(lits(head)) | {'ox_gg_logic_merged'}) and 'ox_gg_logic_merged' not in lits(head)),
           ('걷은 함수 13 — 「이름(」 글자 0 %s' % (left or ''), not left),
           ('mergeExcelRecords · exportExcelFile 무변(엑셀 논리 열)', fn_lines(Ln, 'function mergeExcelRecords(') == fn_lines(Lh, 'function mergeExcelRecords(') is not None
            and fn_lines(Ln, 'async function exportExcelFile(') == fn_lines(Lh, 'async function exportExcelFile(') is not None),
           ('근거 함수 gg* %d개 무변(ggMemoMergeBoot·ggBoxHasText 말고) %s' % (len(gg_head), gg_diff or ''), not gg_diff and len(gg_head) > 20),
           ('useUnlink · refPut · refOf · refStore 무변', all(fn_lines(Ln, 'function %s(' % f) == fn_lines(Lh, 'function %s(' % f) is not None for f in ('useUnlink', 'refPut', 'refOf'))
            and [s for s in Ln if 'function refStore()' in s] == [s for s in Lh if 'function refStore()' in s]),
           ('recBoot 이 syncRecords().then(ggMergeBoots, ggMergeBoots)', 'syncRecords().then(ggMergeBoots, ggMergeBoots);' in new and 'then(ggMemoMergeBoot' not in new),
           ("search-mode-l 0 · setSearchMode('l') 0", 'search-mode-l' not in new and "setSearchMode('l')" not in new)]
    for name, ok in chk:
        print('  %-48s %s' % (name, 'PASS' if ok else 'FAIL'))
    g11 = all(ok for _, ok in chk)
    print()

    print('=== 게이트 표 (NEW / HEAD) ===')
    allok = True
    for g in GATES:
        if g == 'SRC':
            print('  %-4s NEW %-8s HEAD —(소스 대조 · 지시서 G10 D11 가드·G11 Pages 는 push 때)' % (g, 'PASS' if g11 else 'FAIL'))
            continue
        t = tally(res.get('NEW'), g)
        extra, vok = '', True
        if g in rg:
            vok = all(rg[g]) and cnt_ok
            extra = ' · 회귀 글자 %d/%d %s' % (sum(rg[g]), len(rg[g]), 'PASS' if vok else 'FAIL')
        tok = ('/0F' in t) if t != '—' else (g in rg)
        print('  %-4s NEW %-8s HEAD %-8s%s' % (g, t, tally(res.get('HEAD'), g), extra))
        allok = allok and vok and tok
    nf = res.get('NEW') is None or any(x.startswith('FAIL') for x in res['NEW'])
    ok = (not nf) and g11 and allok and cnt_ok
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
