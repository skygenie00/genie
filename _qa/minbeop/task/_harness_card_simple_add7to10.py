# -*- coding: utf-8 -*-
"""민법OX card_simple add7(카드 「관련 문제」 줄 → 머리 칩 「↩링크N」「↩백링크N」) · add8(비교 창 → 문항 팝업 · 「✏️ 연결」) · add9(회독 배지 빨간 X · 태그 단추 바탕·테두리 없이) · add10(근거에서 찾기 타자 밀림) 검산
 — minbeop/task/_task_ox_card_simple_add7.md G21 · _add8.md G22 · _add9.md G23 · _add10.md G24.
⚠ G24 는 같은 입력의 찾기 결과 HTML 을 두 판에서 받아 글자까지 대조한다(VAL).

  NEW  = genie 작업트리 minbeop/index.html
  HEAD = git HEAD (고치기 전 · 헛잣대)
  시험 글 = 같은 폴더의 _harness_card_simple_add7to10_tests.js
⚠ 앱 onload(IndexedDB 시동)는 끈다 · fetch 는 통째로 가짜(진짜 망에 안 나간다).
⚠ 결과는 console.log('HZR|…') 로 stderr 에서 받는다(민법OX 헤드리스 크롬은 시험 뒤 죽는 일이 있다).

쓰기 : python _harness_card_simple_add7to10.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import io, json, os, re, shutil, subprocess, sys, tempfile, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

GENIE = _roots.genie()
REL = 'minbeop/index.html'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(tempfile.gettempdir(), 'h_card_simple_add7to10')
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
GATES = ['G21', 'G22', 'G23', 'G24', 'G10', 'SRC']   # SRC = 소스 대조(D11 가드·Pages 는 push 때 따로)
JS_FILES = ('_harness_card_simple_add7to10_tests.js',)
GONE_FNS = ['linkedBadgesHTML', 'linkBtnHTML', 'labelOfUid', 'cmpExtraHTML', 'cmpToggle', 'cmpEditHTML', 'cmpSave']


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
        return [L[i]]   # 한 줄 함수(ggKeyDown 등) — 뒤 함수의 } 까지 딸려 오면 거짓 다름이 난다
    ind = len(L[i]) - len(L[i].lstrip())
    for j in range(i + 1, len(L)):
        if L[j] == ' ' * ind + '}':
            return L[i:j + 1]
    return None


def main():
    if QC.SMOKE:   # smoke — 이 하네스엔 smoke 칸이 없다(A-0 처리표 · _task_qa_slim2) · 크롬을 띄우기 전에 끝낸다
        print('INFO | smoke 칸 없음')
        return 0
    os.makedirs(OUT, exist_ok=True)
    new = io.open(os.path.join(GENIE, REL.replace('/', os.sep)), encoding='utf-8', newline='').read()
    if QC.GATE:
        QC.sub('git:show-app')
        head = git('show', 'HEAD:' + REL)
        print('HEAD %s' % git('log', '-1', '--format=%h %s').strip())
    else:
        head = None   # regress — 바탕(HEAD) 앱 풀기·띄우기 0(사슬에선 HEAD = 새 판 · A-0 W3 뜻밖에 4) · VAL · SRC 대조는 기준 스냅샷
    base = {'subject': '민법총칙', 'chapter': '1. 총칙', 'subChapter': '1.1 민법의 법원', 'subNum': '', 'examMeta': [],
            'caseText': '', 'stem': '', 'status': '', 'excelLogic': '', 'panrye': '', 'source': '변리사 20'}
    quiz = []
    for n in range(1, 26):
        u = 'Q98%02d' % n
        quiz.append(dict(base, id=u, a='O' if n % 2 else 'X', q='카드 지문 %s — 가나다라마바사아자차카타파하' % u, exp='카드 해설 %s\n둘째 줄' % u,
                         displayNo=n, probNum=n))
    for n in range(1, 121):                                  # add10 G24 — 찾기 시험 단원 120문항(근거는 시험 글이 넣는다)
        u = 'Q7%03d' % n
        quiz.append(dict(base, id=u, chapter='9. 찾기', subChapter='9.1 찾기 시험', a='O', q='찾기 시험 지문 %s' % u, exp='해설 %s' % u, displayNo=n, probNum=n))
    for no in range(1, 8):
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
        if QC.REGRESS and tag == 'HEAD':   # regress — HEAD(바탕) 판은 헛잣대 몫(관문만) · 같은 입력 글자(VAL)는 기준 스냅샷과 맞댄다
            continue
        QC.launch('base' if tag == 'HEAD' else 'new')
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

    if QC.REGRESS:   # regress — 같은 입력의 찾기 결과 글자(G24 VAL)를 바탕(앞 인도판) 스냅샷과 맞댄다(줄마다 md5 · 길이)
        import hashlib as _hl
        print('=== 회귀 대조 — 같은 입력의 글자 (NEW vs 기준 스냅샷) ===')
        vals = {'NEW': [x for x in (res.get('NEW') or []) if x.startswith('VAL | ')]}
        rg = {}
        for a in vals['NEW']:
            name = a.split(' | ')[1]
            ok = QC.same('VAL.' + name, [_hl.md5(a.encode('utf-8')).hexdigest()[:16], len(a)])
            rg.setdefault(name.split('.')[0], []).append(ok)
            print('  %-28s %s' % (name, 'PASS 글자까지 같다' if ok else 'FAIL 다르다'))
            if not ok:
                io.open(os.path.join(OUT, 'val_%s_NEW.txt' % name), 'w', encoding='utf-8').write(a)
        nb = QC.base('VAL.n', len(vals['NEW']))
        cnt_ok = len(vals['NEW']) == nb and len(vals['NEW']) > 0
        print('  VAL 줄 NEW %d · 기준 %d (%s)' % (len(vals['NEW']), nb, QC.base_note('VAL.n')))
        print()
    if QC.GATE:
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

    if QC.REGRESS:   # regress — NEW·HEAD 맞대던 여섯 칸(긴 줄 · SheetJS · SYNC_KEYS · ox_* · gg* 함수 · 다섯 함수)은 기준 스냅샷(앞 인도판 · md5)과 · 나머지는 NEW 글자만(gate 와 같은 식)
        import hashlib as _hl
        print('=== SRC 소스 대조 (NEW vs 기준 스냅샷 · add7 §1·§4 · add8 · add9 · add10) ===')
        Ln = new.split('\n')
        lits = lambda t: sorted(set(re.findall(r"""['"`](ox_[a-z0-9_]+)['"`]""", t)))
        md = lambda xs: None if xs is None else _hl.md5('\n'.join(xs).encode('utf-8')).hexdigest()[:16]
        gg_new = sorted(set(re.findall(r'^\s*(?:async\s+)?function (gg[A-Za-z0-9_]*)\s*\(', new, re.M)) - {'ggMaxOf', 'ggLineHTML', 'ggTextOf', 'ggPickLine'})
        gg_now = {f: md(fn_lines(Ln, 'function %s(' % f)) for f in gg_new}
        gg_head = QC.base('SRC.gg', gg_now)   # 기준 = 앞 인도판의 gg* 함수 이름 → 몸통 md5(스냅샷 없으면 지금 값 = 첫 기록)
        gg_diff = [f for f in sorted(gg_head) if gg_now.get(f) is None or gg_now.get(f) != gg_head[f]]
        left = [f for f in GONE_FNS if re.search(r'\b%s\s*\(' % f, new)]
        slq = fn_lines(Ln, 'function showLinkedQuestion(')
        f5 = [md(fn_lines(Ln, s)) for s in ('function useUnlink(', 'function refPut(', 'function refOf(', 'function mergeExcelRecords(', 'async function exportExcelFile(')]
        chk = [('긴 줄(>3000자) 전부 글자까지 같다', QC.same('SRC.long', md([s for s in Ln if len(s) > 3000]))),
               ('SheetJS 줄(가장 긴 줄) 바이트 무변', QC.same('SRC.sheetjs', md([max(Ln, key=len)])) and len(max(Ln, key=len)) > 60000),
               ('SYNC_KEYS 무변', QC.same('SRC.synckeys', md([s for s in Ln if 'const SYNC_KEYS = [' in s]))),
               ('ox_* 글자 집합 같다(새 저장소 키 0)', QC.same('SRC.oxlits', lits(new))),
               ('걷은 함수 7 — 「이름(」 글자 0 %s' % (left or ''), not left),
               ("linked-badges- 0 · cmp- 0 · 비교 창 범위 0 · sizeKey 'cmp' 0", 'linked-badges-' not in new and 'cmp-' not in new
                and not re.search(r'(?<![A-Za-z0-9_])cp-', new) and "sizeKey: 'cmp'" not in new),
               ('showLinkedQuestion = openQPopup 껍데기(oxWinOpen 0)', slq is not None and any('openQPopup(' in s for s in slq) and not any('oxWinOpen(' in s for s in slq)),
               ('근거 함수 gg* %d개 무변(ggMaxOf·ggLineHTML·ggTextOf·ggPickLine 말고 · ggLogicMergeOnce 포함) %s' % (len(gg_head), gg_diff or ''), not gg_diff and len(gg_head) > 20),
               ('useUnlink · refPut · refOf · mergeExcelRecords · exportExcelFile 무변', None not in f5 and QC.same('SRC.fns5', f5))]
        print('  (기준: %s)' % QC.base_note('SRC.synckeys'))
    if QC.GATE:
        print('=== SRC 소스 대조 (NEW vs HEAD · add7 §1·§4 · add8 · add9 · add10) ===')
        Ln, Lh = new.split('\n'), head.split('\n')
        lits = lambda t: sorted(set(re.findall(r"""['"`](ox_[a-z0-9_]+)['"`]""", t)))
        gg_head = sorted(set(re.findall(r'^\s*(?:async\s+)?function (gg[A-Za-z0-9_]*)\s*\(', head, re.M)) - {'ggMaxOf', 'ggLineHTML', 'ggTextOf', 'ggPickLine'})
        gg_diff = [f for f in gg_head if fn_lines(Ln, 'function %s(' % f) != fn_lines(Lh, 'function %s(' % f) or fn_lines(Ln, 'function %s(' % f) is None]
        left = [f for f in GONE_FNS if re.search(r'\b%s\s*\(' % f, new)]
        slq = fn_lines(Ln, 'function showLinkedQuestion(')
        chk = [('긴 줄(>3000자) 전부 글자까지 같다', [s for s in Ln if len(s) > 3000] == [s for s in Lh if len(s) > 3000]),
               ('SheetJS 줄(가장 긴 줄) 바이트 무변', max(Ln, key=len) == max(Lh, key=len) and len(max(Ln, key=len)) > 60000),
               ('SYNC_KEYS 무변', [s for s in Ln if 'const SYNC_KEYS = [' in s] == [s for s in Lh if 'const SYNC_KEYS = [' in s]),
               ('ox_* 글자 집합 같다(새 저장소 키 0)', lits(new) == lits(head)),
               ('걷은 함수 7 — 「이름(」 글자 0 %s' % (left or ''), not left),
               ("linked-badges- 0 · cmp- 0 · 비교 창 범위 0 · sizeKey 'cmp' 0", 'linked-badges-' not in new and 'cmp-' not in new
                and not re.search(r'(?<![A-Za-z0-9_])cp-', new) and "sizeKey: 'cmp'" not in new),
               ('showLinkedQuestion = openQPopup 껍데기(oxWinOpen 0)', slq is not None and any('openQPopup(' in s for s in slq) and not any('oxWinOpen(' in s for s in slq)),
               ('근거 함수 gg* %d개 무변(ggMaxOf·ggLineHTML·ggTextOf·ggPickLine 말고 · ggLogicMergeOnce 포함) %s' % (len(gg_head), gg_diff or ''), not gg_diff and len(gg_head) > 20),
               ('useUnlink · refPut · refOf · mergeExcelRecords · exportExcelFile 무변',
                all(fn_lines(Ln, s) == fn_lines(Lh, s) is not None for s in ('function useUnlink(', 'function refPut(', 'function refOf(', 'function mergeExcelRecords(', 'async function exportExcelFile(')))]
    chk.append(("add9 — 회독 배지 🔴 0 · 빨간 X · styleMap 0 · 옛 태그 채움 class 0 · TAGCLS 새 글자",
                '🔴${wrongN}' not in new and '<span class="text-red-600 font-black">X</span>${wrongN}' in new and 'styleMap' not in new
                and 'tag-btn min-w-[24px]' not in new
                and "const TAGCLS = 'tag-btn w-[22px] h-[22px] inline-flex items-center justify-center p-0 bg-transparent border-0 text-[13px]';" in new))
    lsb = '\n'.join(fn_lines(Ln, "function linkSearch(ownerId, kind, sc = '') {") or [])
    chk.append(('add10 — linkSearch 안 ggStore() 1 · quizData.find 0 · ggTextOf( 0 · 근거 찾기 칸 oninput = linkSearchSoon · onfocus = linkSearch',
                lsb.count('ggStore()') == 1 and 'quizData.find' not in lsb and 'ggTextOf(' not in lsb
                and 'oninput="linkSearchSoon(' in new and 'onfocus="linkSearch(' in new))
    for name, ok in chk:
        print('  %-52s %s' % (name, 'PASS' if ok else 'FAIL'))
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
