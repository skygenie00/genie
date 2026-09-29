# -*- coding: utf-8 -*-
"""민법OX 문제풀이 형광펜 표시 토글 + 펜 필기모드 검산 — minbeop/task/_task_ox_ink.md §E.

  NEW  = genie 작업트리 minbeop/index.html
  NEW2 = 같은 NEW 를 크롬을 닫고 **같은 프로필로 다시** 연 판(진짜 새로고침 — G8 IndexedDB 가 남는지)
  HEAD = git HEAD (고치기 전 · 헛잣대)
  시험 글 = 같은 폴더의 _harness_ink_tests.js — 헤드리스에서 펜·손가락·마우스 포인터(PointerEvent pointerType)를 합성해 돌린다.
⚠ 앱 onload(IndexedDB 시동)는 끈다 · fetch 는 통째로 가짜(진짜 망에 안 나간다) · 필기는 헤드리스 프로필의 IndexedDB 에 쓴다(NEW·HEAD 는 판마다 프로필을 새로 만든다).
⚠ 결과는 console.log('HZR|…') 로 stderr 에서 받는다.
⚠ VAL 줄(마우스 조작의 저장소·형광펜 상자)은 두 판에 같은 입력을 넣고 파이썬이 글자를 대조한다.

쓰기 : python _harness_ink.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import io, json, os, re, shutil, subprocess, sys, tempfile, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

GENIE = _roots.genie()
REL = 'minbeop/index.html'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(tempfile.gettempdir(), 'h_ink')
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
GATES = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G10', 'SRC']   # G9 = 지난 하네스 회귀(따로) · G11 D11 가드 · G12 Pages 는 push 때
JS_FILES = ('_harness_ink_tests.js',)


def git(*a):
    r = subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a), capture_output=True)
    return r.stdout.decode('utf-8', 'replace')


def build_and_run(tag, src, tests, budget=180000, prof_of=None):
    html = src
    b = html.index('<body')
    bb = html.index('>', b) + 1
    html = html[:bb] + SEED + html[bb:]
    e = html.rindex('</body>')
    html = html[:e] + tests + html[e:]
    app = os.path.join(OUT, 'app_%s.html' % (prof_of or tag))   # 다시 여는 판은 같은 파일 주소여야 같은 IndexedDB(file:// 출처)를 본다
    io.open(app, 'w', encoding='utf-8', newline='\n').write(html)
    prof = os.path.join(OUT, 'prof_%s' % (prof_of or tag))
    if not prof_of:
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
    if L[i].rstrip().endswith('}') and L[i].count('{') == L[i].count('}'):
        return [L[i]]
    ind = len(L[i]) - len(L[i].lstrip())
    for j in range(i + 1, len(L)):
        if L[j] == ' ' * ind + '}':
            return L[i:j + 1]
    return None


def show(tag, lines):
    print('=== %s 판 ===' % tag)
    if lines is None:
        print('  결과 줄 없음 → %s' % os.path.join(OUT, 'chrome_err_%s.txt' % tag.split('(')[0]))
        return
    for ln in lines:
        if not ln.startswith('VAL'):
            print('   ' + (ln if len(ln) < 1600 else ln[:1600] + ' …'))
    print('  합계 PASS %d · FAIL %d' % (sum(1 for x in lines if x.startswith('PASS')), sum(1 for x in lines if x.startswith('FAIL'))))
    print()


def main():
    os.makedirs(OUT, exist_ok=True)
    new = io.open(os.path.join(GENIE, REL.replace('/', os.sep)), encoding='utf-8', newline='').read()
    head = git('show', 'HEAD:' + REL)
    print('HEAD %s' % git('log', '-1', '--format=%h %s').strip())
    base = {'subject': '민법총칙', 'chapter': '1. 총칙', 'subChapter': '1.1 민법의 법원', 'subNum': '', 'examMeta': [],
            'caseText': '', 'stem': '', 'status': '', 'excelLogic': '', 'panrye': '', 'source': '변리사 20'}
    quiz = []
    longq = '긴 지문 ' + '가나다라마바사아자차카타파하 거너더러머버서어저처커터퍼허 ' * 9
    for n in range(1, 26):
        u = 'Q98%02d' % n
        q = (longq + u) if n in (1, 3, 5, 9, 11) else ('카드 지문 %s — 가나다라마바사아자차카타파하' % u)
        quiz.append(dict(base, id=u, a='O' if n % 2 else 'X', q=q, exp='카드 해설 %s\n둘째 줄' % u, displayNo=n, probNum=n,
                         panrye='2000다1234' if n in (5, 6) else ''))
    for no in range(1, 8):
        for opt in (1, 2):
            u = 'Q99%02d' % ((no - 1) * 2 + opt)
            quiz.append(dict(base, id=u, a='O' if opt == 1 else 'X', q='기출 지문 %s' % u, exp='기출 해설 %s' % u, displayNo=no, probNum=no,
                             subChapter='2.1 기출', source='변리사 16', examYear='2016', examRound='53', examYears=['2016'],
                             examMeta=[{'year': '2016', 'round': '53', 'no': no, 'opt': opt}], examNo=no, examOpt=opt, examNoBase=no, examOptBase=opt,
                             stem='%d. 다음 설명 중 옳은 것은?' % no))
    P = {'quiz': quiz, 'skip': [x for x in os.environ.get('HZ_SKIP', '').split(',') if x], 'phase': ''}
    js = ''.join(io.open(os.path.join(HERE, f), encoding='utf-8').read() for f in JS_FILES)
    mk = lambda PP: '<script>\n' + js.replace('__P__', json.dumps(PP, ensure_ascii=False).replace('</', '<\\/')) + '\n</script>\n'
    tests, tests_reload = mk(P), mk(dict(P, phase='reload'))
    res = {}
    only = os.environ.get('HZ_ONLY')
    for tag, src in (('NEW', new), ('HEAD', head)):
        if only and tag != only:
            continue
        lines = build_and_run(tag, src, tests)
        show(tag, lines)
        if tag == 'NEW' and lines is not None and 'G8' not in P['skip']:
            l2 = build_and_run('NEW2', new, tests_reload, prof_of='NEW')
            show('NEW2(같은 프로필로 다시 연 판)', l2)
            lines = lines + (l2 if l2 is not None else ['FAIL | G8 다시 연 판 결과 줄 없음'])
        res[tag] = lines

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

    print('=== SRC 소스 대조 (NEW vs HEAD · 지시서 §D 손대지 않는 것) ===')
    Ln, Lh = new.split('\n'), head.split('\n')
    lits = lambda t: sorted(set(re.findall(r"""['"`](ox_[a-z0-9_]+)['"`]""", t)))
    keep = ['function markHTML(', 'function renderMarked(', 'function applyMark(', 'function onSelectMaybe(', 'function offsetsInNode(',
            'function loadMarks(', 'function saveMarks(', 'function normalizeMarks(', 'function openJeongni(', 'function jnMarksToggle(', 'function jnRowHTML(',
            'function jnBodyHTML(', 'async function syncRecords(', 'function stampAll(', 'async function dbGet(', 'async function dbPut(', 'function dbOpen(',
            'function toggleTag(', 'function togglePeekExp(', 'function oxPaint(', 'function ggLineHTML(', 'function gradeCurrentPage(']
    keep_have = [s for s in keep if fn_lines(Lh, s) is not None]
    keep_diff = [s for s in keep_have if fn_lines(Ln, s) != fn_lines(Lh, s)]
    print('  (대조한 함수 %d · HEAD 에 한 곳으로 없어 뺀 것 %s)' % (len(keep_have), [s for s in keep if s not in keep_have] or '없음'))
    mbb = sorted(set(re.findall(r'^\s*(?:async\s+)?function (mbb?[A-Z][A-Za-z0-9_]*)\s*\(', head, re.M)))
    mbb_diff = [f for f in mbb if fn_lines(Ln, 'function %s(' % f) != fn_lines(Lh, 'function %s(' % f)]
    bi = new.find('★ 09-15 (_task_ox_ink) 문제풀이 필기')
    be = new.find('// --- 태그 (체크) 토글 기능 ---', bi)
    blk = new[bi:be] if bi >= 0 and be > bi else ''
    rq, rqh = fn_lines(Ln, 'function renderQuizPage() {'), fn_lines(Lh, 'function renderQuizPage() {')
    rq_d = sorted(set(rq or []) ^ set(rqh or []))
    chk = [('긴 줄(>3000자) 전부 글자까지 같다', [s for s in Ln if len(s) > 3000] == [s for s in Lh if len(s) > 3000]),
           ('SheetJS 줄(가장 긴 줄) 바이트 무변', max(Ln, key=len) == max(Lh, key=len) and len(max(Ln, key=len)) > 60000),
           ('SYNC_KEYS 무변', [s for s in Ln if 'const SYNC_KEYS = [' in s] == [s for s in Lh if 'const SYNC_KEYS = [' in s]),
           ('ox_* 글자 집합 같다(새 저장소 키 0 · 필기는 SYNC 밖)', lits(new) == lits(head)),
           ('형광펜·정리 창·동기화·IndexedDB 손잡이·카드 조각 함수 %d개 무변 %s' % (len(keep_have), keep_diff or ''), not keep_diff and len(keep_have) >= 18),
           ('교재뷰 mbBook*·mbb* 함수 %d개 무변 %s' % (len(mbb), mbb_diff or ''), not mbb_diff and len(mbb) > 5),
           ('renderQuizPage 바뀐 줄 = 지문·해설 <p> 둘 · 묶음 한 줄 · qiAfterRender 한 줄(옛 3줄 ↔ 새 4줄)', len(rq_d) == 7 and sum(1 for s in rq_d if 'qiAfterRender(pageData)' in s or 'id=\\"qcards\\"' in s or 'id="qcards"' in s) == 2),
           ('필기 덩이 안 localStorage. 0 · ink:q: 키 · dbDel 정의 하나', bool(blk) and 'localStorage.' not in blk and "'ink:q:'" in blk and new.count('async function dbDel(') == 1)]
    for name, ok in chk:
        print('  %-64s %s' % (name, 'PASS' if ok else 'FAIL'))
    if len(rq_d) != 7:
        for s in rq_d:
            print('     ± ' + s.strip()[:200])
    g_src = all(ok for _, ok in chk)
    print()

    print('=== 게이트 표 (NEW / HEAD) ===')
    allok = True
    for g in GATES:
        if g == 'SRC':
            print('  %-4s NEW %-8s HEAD —(소스 대조 · D11 가드·Pages 는 push 때)' % (g, 'PASS' if g_src else 'FAIL'))
            continue
        t = tally(res.get('NEW'), g)
        extra, vok = '', True
        if g in rg:
            vok = all(rg[g]) and cnt_ok
            extra = ' · 회귀 글자 %d/%d %s' % (sum(rg[g]), len(rg[g]), 'PASS' if vok else 'FAIL')
        tok = '/0F' in t
        print('  %-4s NEW %-8s HEAD %-8s%s' % (g, t, tally(res.get('HEAD'), g), extra))
        allok = allok and tok and vok
    nf = res.get('NEW') is None or any(x.startswith('FAIL') for x in res['NEW'])
    ok = (not nf) and g_src and allok
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
