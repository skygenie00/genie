# -*- coding: utf-8 -*-
"""민법OX _task_ox_card_simple_add11 검산 — 회독 배지 틀린 수 빨강 · 🔍 검색 결과 → 문항 팝업 · 📋 정리칩 「N.」 장도 한 묶음.

  NEW  = genie 작업트리 minbeop/index.html(ink add1 + add11 한 판)
  HEAD = git HEAD(ink 45ec79e · 헛잣대)
  G3 진짜 데이터 = studyplandata 클론(fetch·ff 뒤) minbeop/문항마스터.json 행을 칸만 줄여 앱 buildQuizData 에 그대로 넣는다.
⚠ 앱 onload 는 끈다 · fetch 는 통째로 가짜 · 결과는 console.log('HZR|…') 로 stderr 에서 받는다 · 크롬은 하나씩.

쓰기 : python _harness_card_simple_add11.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

GENIE = _roots.genie()
SP = _roots.spd()
REL = 'minbeop/index.html'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(tempfile.gettempdir(), 'h_card_add11')
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
GATES = ['G1', 'G2', 'G3', 'G10', 'SRC']
COLS = ['uid', '과목', '장', '세부단원', '구분', '기출연도', '회차', '출제연도', '번호', '지문번호', '정답', '문제', '해설', '출처', '상태']


def git(*a, cwd=GENIE):
    r = subprocess.run(['git', '-C', cwd, '-c', 'core.quotepath=false'] + list(a), capture_output=True)
    return r.stdout.decode('utf-8', 'replace')


def census(rows, pat):
    """과목별 목차 줄 수 · 묶음 수 — renderDashboard 가 모으는 규칙(jeongni 하네스 census 와 같다) · 열쇠 정규식만 pat."""
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
            m = re.match(pat, sub)
            keys.add(m.group(0) if m else '@' + label)
        out[subj] = {'rows': len(labels), 'groups': len(keys)}
    return out


def run(tag, src, tests, budget=180000):
    b = src.index('<body'); bb = src.index('>', b) + 1
    html = src[:bb] + SEED + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + tests + html[e:]
    app = os.path.join(OUT, 'app_%s.html' % tag)
    io.open(app, 'w', encoding='utf-8', newline='\n').write(html)
    prof = os.path.join(OUT, 'prof_%s' % tag)
    shutil.rmtree(prof, ignore_errors=True)
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--user-data-dir=' + prof,
                        '--allow-file-access-from-files', '--window-size=1280,900', '--enable-logging=stderr', '--v=0',
                        '--virtual-time-budget=%d' % budget, '--dump-dom', 'file:///' + app.replace('\\', '/')], capture_output=True, timeout=900)
    err = r.stderr.decode('utf-8', 'replace')
    io.open(os.path.join(OUT, 'chrome_err_%s.txt' % tag), 'w', encoding='utf-8').write(err)
    hz = []
    for ln in err.split('\n'):
        i = ln.find('"HZR|')
        if i >= 0:
            j = ln.find('"', i + 5)
            hz.append(urllib.parse.unquote(ln[i + 5:j]))
    print('  [%s] chrome rc %s · HZR 줄 %d' % (tag, r.returncode, len(hz)))
    return [x for x in hz[:-1] if x.strip()] if hz and hz[-1] == 'END' else None


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


def main():
    os.makedirs(OUT, exist_ok=True)
    new = io.open(os.path.join(GENIE, REL.replace('/', os.sep)), encoding='utf-8', newline='').read()
    head = git('show', 'HEAD:' + REL)
    print('HEAD %s' % git('log', '-1', '--format=%h %s').strip())
    mp = os.path.join(SP, 'minbeop', '문항마스터.json')
    raw = open(mp, 'rb').read()
    print('studyplandata %s · 앞/뒤 %s · 문항마스터 %d B · md5 %s' % (git('log', '-1', '--format=%h %ad', '--date=iso', cwd=SP).strip(),
                                                           git('rev-list', '--left-right', '--count', 'HEAD...@{u}', cwd=SP).strip().replace('\t', ' '), len(raw), hashlib.md5(raw).hexdigest()))
    M = json.loads(raw.decode('utf-8'))
    cen_old = census(M['rows'], r'^\d+\.\d+')
    cen_new = census(M['rows'], r'^\d+(?:\.\d+)?')
    print('§3 묶음 수(파이썬) 옛 열쇠 %s · 합 %d' % (json.dumps(cen_old, ensure_ascii=False), sum(v['groups'] for v in cen_old.values())))
    print('§3 묶음 수(파이썬) 새 열쇠 %s · 합 %d' % (json.dumps(cen_new, ensure_ascii=False), sum(v['groups'] for v in cen_new.values())))
    rows = [{k: (str(r.get(k)) if r.get(k) is not None else '') for k in COLS} for r in M['rows'] if r.get('uid') and r.get('문제')]
    for r in rows:
        r['문제'] = 'x'
        r['해설'] = ''
    base = {'subject': '민법총칙', 'chapter': '1. 총칙', 'subChapter': '1.1 민법의 법원', 'subNum': '', 'examMeta': [], 'caseText': '', 'stem': '',
            'status': '', 'excelLogic': '', 'panrye': '', 'source': '변리사 20', 'yuje': ''}
    quiz = []
    longq = '긴 지문 ' + '가나다라마바사아자차카타파하 거너더러머버서어저처커터퍼허 ' * 60
    for n in range(1, 26):
        u = 'Q98%02d' % n
        q = ('공동명의 예금 지문 %s' % u) if n == 2 else (longq + u if n == 12 else '카드 지문 %s — 가나다라마바사아자차카타파하' % u)
        quiz.append(dict(base, id=u, a='O' if n % 2 else 'X', q=q, exp='카드 해설 %s' % u, displayNo=n, probNum=n))
    for no in range(1, 4):
        u = 'Q99%02d' % no
        quiz.append(dict(base, id=u, a='O', q='기출 지문 %s' % u, exp='기출 해설', displayNo=no, probNum=no, subChapter='2.1 기출', source='변리사 16',
                         examYear='2016', examRound='53', examYears=['2016'], examMeta=[{'year': '2016', 'round': '53', 'no': no, 'opt': 1}],
                         examNo=no, examOpt=1, examNoBase=no, examOptBase=1, stem='%d. 다음 설명 중 옳은 것은?' % no))
    P = {'quiz': quiz, 'rows': rows, 'census': cen_new, 'censusTotal': sum(v['groups'] for v in cen_new.values()),
         'skip': [x for x in os.environ.get('HZ_SKIP', '').split(',') if x]}
    js = io.open(os.path.join(HERE, '_harness_card_simple_add11_tests.js'), encoding='utf-8').read()
    tests = '<script>\n' + js.replace('__P__', json.dumps(P, ensure_ascii=False).replace('</', '<\\/')) + '\n</script>\n'
    res = {}
    for tag, src in (('NEW', new), ('HEAD', head)):
        lines = run(tag, src, tests)
        res[tag] = lines
        print('=== %s 판 ===' % tag)
        for ln in (lines or ['결과 줄 없음']):
            print('   ' + (ln if len(ln) < 1600 else ln[:1600] + ' …'))
        if lines:
            print('  합계 PASS %d · FAIL %d' % (sum(1 for x in lines if x.startswith('PASS')), sum(1 for x in lines if x.startswith('FAIL'))))
        print()

    print('=== SRC 소스 대조 (NEW vs HEAD · add11) ===')
    Ln, Lh = new.split('\n'), head.split('\n')
    lits = lambda t: sorted(set(re.findall(r"""['"`](ox_[a-z0-9_]+)['"`]""", t)))
    jump = lambda L: sorted(s.strip() for s in L if len(s) < 3000 and 'jumpFromSearch(' in s)
    jd = [s for s in jump(Lh) if s not in jump(Ln)]
    chk = [('긴 줄(>3000자) 전부 글자까지 같다', [s for s in Ln if len(s) > 3000] == [s for s in Lh if len(s) > 3000]),
           ('SYNC_KEYS 무변 · ox_* 글자 집합 같다', [s for s in Ln if 'const SYNC_KEYS = [' in s] == [s for s in Lh if 'const SYNC_KEYS = [' in s] and lits(new) == lits(head)),
           ('§1 배지 X${wrongN} 이 빨강 span 안 · 옛 X</span>${wrongN} 0', '<span class="text-red-600 font-black">X${wrongN}</span> /${h.total}' in new and 'X</span>${wrongN}' not in new),
           ('§2 jumpFromSearch 함수 무변 · 빠진 호출은 runSearch 결과 단추 하나뿐 %s' % jd, fn_lines(Ln, 'function jumpFromSearch(id) {') == fn_lines(Lh, 'function jumpFromSearch(id) {')
            and len(jd) == 1 and jd[0].startswith("<button onclick=\"jumpFromSearch('${q.id}')\"")),
           ("§2 runSearch 결과 단추 = openQPopup + qpScrollTo('gg'|'top') · qpScrollTo 정의 하나", "onclick=\"openQPopup('${q.id}');qpScrollTo('${q.id}','${searchMode === 'm' ? 'gg' : 'top'}')\"" in new
            and new.count('function qpScrollTo(') == 1),
           ('§3 jnKeyOf 정규식 ^\\d+(?:\\.\\d+)? · openJeongni·jnLabelsOf 무변', r"function jnKeyOf(sub, chapLabel) { const m = /^\d+(?:\.\d+)?/.exec(String(sub || '')); return m ? m[0] : String(chapLabel); }" in new
            and fn_lines(Ln, 'function openJeongni(') == fn_lines(Lh, 'function openJeongni(') and fn_lines(Ln, 'function jnLabelsOf(') == fn_lines(Lh, 'function jnLabelsOf('))]
    for name, ok in chk:
        print('  %-72s %s' % (name, 'PASS' if ok else 'FAIL'))
    g_src = all(ok for _, ok in chk)
    print()
    print('=== 게이트 표 (NEW / HEAD) ===')
    allok = True
    for g in GATES:
        if g == 'SRC':
            print('  %-4s NEW %s' % (g, 'PASS' if g_src else 'FAIL'))
            continue
        t = tally(res.get('NEW'), g)
        print('  %-4s NEW %-8s HEAD %-8s' % (g, t, tally(res.get('HEAD'), g)))
        allok = allok and t != '—' and '/0F' in t
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
