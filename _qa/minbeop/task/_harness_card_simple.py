# -*- coding: utf-8 -*-
"""민법OX 카드 심플 · OMR 떠 있는 창 · 아래 알약 · 학습로그 단추 걷기 · 정리 행 연결칩 상자 검산 — minbeop/task/_task_ox_card_simple.md §G.

  NEW  = genie 작업트리 minbeop/index.html
  HEAD = git HEAD (고치기 전 · 헛잣대)
  시험 글 = 같은 폴더의 _harness_card_simple_tests.js + _harness_card_simple_tests2.js
⚠ 앱 onload(IndexedDB 시동)는 끈다 · fetch 는 통째로 가짜(진짜 망에 안 나간다).
⚠ 결과는 console.log('HZR|…') 로 stderr 에서 받는다(채점을 돌린 민법OX 헤드리스 크롬은 시험 뒤 죽는 일이 있다).
⚠ VAL 줄(G3 .result-badge·q-box · G8 카드 칩)은 두 판에 같은 입력을 넣고 파이썬이 글자를 대조한다.
⚠ 레이아웃·계산 스타일은 DOM 을 넣은 틱이 아니라 한 틱 뒤에 잰다(Tailwind CDN 늦은 생성).

쓰기 : python _harness_card_simple.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2(10/8) 실행 모드 --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같음) · import 때 --mode · --snap-in · --snap-out 을 sys.argv 에서 뗀다
import io, json, os, re, shutil, subprocess, sys, tempfile, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

GENIE = _roots.genie()
REL = 'minbeop/index.html'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(tempfile.gettempdir(), 'h_card_simple')
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
GATES = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G10', 'G11', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18', 'G19']
JS_FILES = ('_harness_card_simple_tests.js', '_harness_card_simple_tests2.js', '_harness_card_simple_tests3.js')


def git(*a):
    r = subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a), capture_output=True)
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
    if os.environ.get('HZ_LOG'):
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


def main():
    if QC.REGRESS:   # regress · smoke(_task_qa_slim2 A-1) — 이 하네스 칸 117 = 합침→_harness_card_simple_add6 115(같은 파이썬 · tests.js · tests2.js · tests3 ≈ tests3_add6) · 뺌 1(G17 「파랑 굵게」 옛 잣대 — add6 이 「검정 굵게」로 같은 자리를 잰다) · 관문만 1(HEAD 판 헛잣대) → 앱을 안 띄운다(바탕 띄움 · git show 0)
        print('INFO | %s 칸 없음 | 칸 117 = 합침→_harness_card_simple_add6 115 · 뺌 1(G17 옛 잣대) · 관문만 1(HEAD 판 헛잣대) — 앱 안 띄움 · 그 칸은 _harness_card_simple_add6 이 잰다' % QC.MODE, flush=True)
        return 0
    os.makedirs(OUT, exist_ok=True)
    new = io.open(os.path.join(GENIE, REL.replace('/', os.sep)), encoding='utf-8', newline='').read()
    QC.sub('git:show-app')
    head = git('show', 'HEAD:' + REL)
    base = {'subject': '민법총칙', 'chapter': '1. 총칙', 'subChapter': '1.1 민법의 법원', 'subNum': '', 'examMeta': [],
            'caseText': '', 'stem': '', 'status': '', 'excelLogic': '', 'panrye': '', 'source': '변리사 20'}
    quiz = []
    for n in range(1, 26):                                   # 단원 25문항 = 20 + 5 (두 쪽)
        u = 'Q98%02d' % n
        quiz.append(dict(base, id=u, a='O' if n % 2 else 'X', q='카드 지문 %s — 가나다라마바사아자차카타파하' % u, exp='카드 해설 %s\n둘째 줄' % u,
                         displayNo=n, probNum=n))
    quiz[2]['excelLogic'] = '논리 글 하나'                    # Q9803 은 논리 단추가 보인다
    for no in range(1, 8):                                   # 기출 7문제 × 지문 2 = 14 (다섯 문제씩 두 쪽)
        for opt in (1, 2):
            u = 'Q99%02d' % ((no - 1) * 2 + opt)
            quiz.append(dict(base, id=u, a='O' if opt == 1 else 'X', q='기출 지문 %s' % u, exp='기출 해설 %s' % u, displayNo=no, probNum=no,
                             subChapter='2.1 기출', source='변리사 16', examYear='2016', examRound='53', examYears=['2016'],
                             examMeta=[{'year': '2016', 'round': '53', 'no': no, 'opt': opt}], examNo=no, examOpt=opt, examNoBase=no, examOptBase=opt,
                             stem='%d. 다음 설명 중 옳은 것은?' % no))
    P = {'quiz': quiz, 'skip': [x for x in os.environ.get('HZ_SKIP', '').split(',') if x]}
    js = ''.join(io.open(os.path.join(HERE, f), encoding='utf-8').read() for f in JS_FILES)
    tests = '<script>\n' + js.replace('__P__', json.dumps(P, ensure_ascii=False).replace('</', '<\\/')) + '\n</script>\n'
    res = {}
    only = os.environ.get('HZ_ONLY')
    for tag, src in (('NEW', new), ('HEAD', head)):
        if only and tag != only:
            continue
        QC.launch('new' if tag == 'NEW' else 'base')
        lines = build_and_run(tag, src, tests)
        res[tag] = lines
        print('=== %s 판 ===' % tag)
        if lines is None:
            print('  결과 줄 없음 → %s' % os.path.join(OUT, 'chrome_err_%s.txt' % tag))
            continue
        for ln in lines:
            if not ln.startswith('VAL'):
                print('   ' + (ln if len(ln) < 700 else ln[:700] + ' …'))
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

    print('=== G11 소스 (NEW vs HEAD) ===')
    Ln, Lh = new.split('\n'), head.split('\n')
    lits = lambda t: sorted(set(re.findall(r"""['"`](ox_[a-z0-9_]+)['"`]""", t)))
    chk = [("pastBadgeHtml 줄 그대로", [s for s in Ln if 'pastBadgeHtml' in s] == [s for s in Lh if 'pastBadgeHtml' in s]),
           ('긴 줄(>3000자) 전부 글자까지 같다', [s for s in Ln if len(s) > 3000] == [s for s in Lh if len(s) > 3000]),
           ('SheetJS 줄(가장 긴 줄) 바이트 무변 — 줄 번호가 아니라 글자로 찾는다', max(Ln, key=len) == max(Lh, key=len) and len(max(Ln, key=len)) > 60000),
           ('SYNC_KEYS 무변', [s for s in Ln if 'const SYNC_KEYS = [' in s] == [s for s in Lh if 'const SYNC_KEYS = [' in s]),
           ("새 저장소 키 0 (ox_* 글자 집합 같다)", lits(new) == lits(head)),
           ('G7 openPanel 함수는 남아 있다(IIFE 안 · 소스로 잰다)', new.count('function openPanel()') == 1),
           ("G7 학습로그 단추를 만드는 줄 0", "btn.textContent = '📝 학습로그';" not in new),
           ('라디오 name="answer_${item.id}" O·X 한 번씩', new.count('name="answer_${item.id}" value="O"') == 1 and new.count('name="answer_${item.id}" value="X"') == 1)]
    for name, ok in chk:
        print('  %-40s %s' % (name, 'PASS' if ok else 'FAIL'))
    g11 = all(ok for _, ok in chk)
    print()

    print('=== 게이트 표 (NEW / HEAD) ===')
    allok = True
    for g in GATES:
        if g == 'G11':
            print('  %-4s NEW %-8s HEAD —(소스 대조 · push 때 D11 가드 따로)' % (g, 'PASS' if g11 else 'FAIL'))
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
