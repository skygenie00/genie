# -*- coding: utf-8 -*-
"""민법OX _task_ox_ink_add1 검산 — 문제풀이 축소 되돌리기 · 「🔗 판 N」 · 렌더 한 번 = 저장소 한 번 · 필기모드 손가락은 브라우저 스크롤.

  NEW  = genie 작업트리 minbeop/index.html(add1 + card_simple add11 한 판)
  HEAD = git HEAD(ink 45ec79e · 헛잣대)
  판 셋 — main(가상 시계 · 창 1280 · _harness_ink_add1_tests.js) · g1(가상 시계 · iframe 390·768·1280 · 같은 시험 글 g1 갈래)
          · perf(실시간 · 가상 시계 없음 · _harness_ink_add1_perf.js — 문항 5,548 · 근거 1,195문항 흉내)
⚠ 앱 onload 는 끈다 · fetch 는 통째로 가짜 · 결과는 console.log('HZR|…') 로 stderr 에서 받는다 · 크롬은 하나씩.
⚠ VAL 줄은 두 판에 같은 입력을 넣고 파이썬이 글자를 대조한다 · G6(전환 시간)은 두 판의 MEAS 를 파이썬이 견준다.

쓰기 : python _harness_ink_add1.py   (HZ_PHASE=main,g1,perf 중 골라 돌릴 수 있다 · HZ_ONLY=NEW|HEAD)
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
OUT = os.path.join(tempfile.gettempdir(), 'h_ink_add1')
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
GATES = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G10', 'VAL', 'SRC']
WIDTHS = [('w390', 390), ('w768', 768), ('w1280', 1280)]


def git(*a):
    r = subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a), capture_output=True)
    return r.stdout.decode('utf-8', 'replace')


def app_html(src, js):
    b = src.index('<body')
    bb = src.index('>', b) + 1
    html = src[:bb] + SEED + src[bb:]
    e = html.rindex('</body>')
    return html[:e] + '<script>\n' + js + '\n</script>\n' + html[e:]


def run_chrome(tag, path, ends, budget=None, win='1280,900', timeout=900):
    prof = os.path.join(OUT, 'prof_%s' % tag)
    shutil.rmtree(prof, ignore_errors=True)
    args = [CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--user-data-dir=' + prof,
            '--allow-file-access-from-files', '--window-size=' + win, '--enable-logging=stderr', '--v=0']
    if budget:
        args.append('--virtual-time-budget=%d' % budget)
    r = subprocess.run(args + ['--dump-dom', 'file:///' + path.replace('\\', '/')], capture_output=True, timeout=timeout)
    err = r.stderr.decode('utf-8', 'replace')
    io.open(os.path.join(OUT, 'chrome_err_%s.txt' % tag), 'w', encoding='utf-8').write(err)
    hz = []
    for ln in err.split('\n'):
        i = ln.find('"HZR|')
        if i >= 0:
            j = ln.find('"', i + 5)
            hz.append(urllib.parse.unquote(ln[i + 5:j]))
    got = [e for e in ends if e in hz]
    print('  [%s] chrome rc %s · HZR 줄 %d · 끝 표 %d/%d' % (tag, r.returncode, len(hz), len(got), len(ends)))
    if len(got) != len(ends):
        return None
    return [x for x in hz if x.strip() and not x.startswith('END')]


def gate_of(line):
    try:
        g = line.split(' | ')[1].split(' ')[0]
        return 'VAL' if g == 'GV' else g
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
    print('=== %s ===' % tag)
    if lines is None:
        print('  결과 줄 없음')
        return
    for ln in lines:
        if not ln.startswith('VAL'):
            print('   ' + (ln if len(ln) < 1600 else ln[:1600] + ' …'))
    print('  합계 PASS %d · FAIL %d' % (sum(1 for x in lines if x.startswith('PASS')), sum(1 for x in lines if x.startswith('FAIL'))))
    print()


def quiz_data():
    base = {'subject': '민법총칙', 'chapter': '1. 총칙', 'subChapter': '1.1 민법의 법원', 'subNum': '', 'examMeta': [],
            'caseText': '', 'stem': '', 'status': '', 'excelLogic': '', 'panrye': '', 'source': '변리사 20', 'yuje': ''}
    longq = '긴 지문 ' + '가나다라마바사아자차카타파하 거너더러머버서어저처커터퍼허 ' * 9
    pan = {5: '2000다1234', 6: '2000다1234', 7: '99다5678', 8: '99다5678'}
    yj = {3: 'Q9804', 10: 'Q9804, q9812', 11: 'Q9811, Q9804', 13: 'Q9804,Q9804'}
    quiz = []
    for n in range(1, 26):
        u = 'Q98%02d' % n
        q = (longq + u) if n in (1, 3, 5, 9, 11) else ('카드 지문 %s — 가나다라마바사아자차카타파하' % u)
        quiz.append(dict(base, id=u, a='O' if n % 2 else 'X', q=q, exp='카드 해설 %s\n둘째 줄' % u, displayNo=n, probNum=n, panrye=pan.get(n, ''), yuje=yj.get(n, '')))
    quiz.append(dict(base, id='Q9803', subChapter='2.2 중복', a='O', q='같은 id 둘째 줄', exp='중복', displayNo=1, probNum=1, yuje='Q9805'))
    for no in range(1, 8):
        for opt in (1, 2):
            u = 'Q99%02d' % ((no - 1) * 2 + opt)
            quiz.append(dict(base, id=u, a='O' if opt == 1 else 'X', q='기출 지문 %s' % u, exp='기출 해설 %s' % u, displayNo=no, probNum=no,
                             subChapter='2.1 기출', source='변리사 16', examYear='2016', examRound='53', examYears=['2016'],
                             examMeta=[{'year': '2016', 'round': '53', 'no': no, 'opt': opt}], examNo=no, examOpt=opt, examNoBase=no, examOptBase=opt,
                             stem='%d. 다음 설명 중 옳은 것은?' % no))
    return quiz


def main():
    os.makedirs(OUT, exist_ok=True)
    new = io.open(os.path.join(GENIE, REL.replace('/', os.sep)), encoding='utf-8', newline='').read()
    head = git('show', 'HEAD:' + REL)
    print('HEAD %s' % git('log', '-1', '--format=%h %s').strip())
    phases = [x for x in os.environ.get('HZ_PHASE', 'main,g1,perf').split(',') if x]
    only = os.environ.get('HZ_ONLY')
    skip = [x for x in os.environ.get('HZ_SKIP', '').split(',') if x]
    tjs = io.open(os.path.join(HERE, '_harness_ink_add1_tests.js'), encoding='utf-8').read()
    pjs = io.open(os.path.join(HERE, '_harness_ink_add1_perf.js'), encoding='utf-8').read()
    Q = quiz_data()
    mk = lambda js, PP: js.replace('__P__', json.dumps(PP, ensure_ascii=False).replace('</', '<\\/'))
    res, meas = {}, {}
    for tag, src in (('NEW', new), ('HEAD', head)):
        if only and tag != only:
            continue
        lines = []
        if 'main' in phases:
            p = os.path.join(OUT, 'app_main_%s.html' % tag)
            io.open(p, 'w', encoding='utf-8', newline='\n').write(app_html(src, mk(tjs, {'quiz': Q, 'skip': skip, 'phase': 'main'})))
            got = run_chrome('main_%s' % tag, p, ['END'], budget=240000)
            show('%s · main' % tag, got)
            lines += got if got is not None else ['FAIL | G10 main 결과 줄 없음']
        if 'g1' in phases:
            p = os.path.join(OUT, 'app_g1_%s.html' % tag)
            io.open(p, 'w', encoding='utf-8', newline='\n').write(app_html(src, mk(tjs, {'quiz': Q, 'skip': [], 'phase': 'g1', 'order': {w: i for i, (w, _) in enumerate(WIDTHS)}})))
            wrap = os.path.join(OUT, 'wrap_g1_%s.html' % tag)
            io.open(wrap, 'w', encoding='utf-8', newline='\n').write('<!doctype html><meta charset="utf-8"><body style="margin:0">'
                + ''.join('<iframe src="app_g1_%s.html#%s" style="display:block;width:%dpx;height:760px;border:0"></iframe>' % (tag, w, px) for w, px in WIDTHS) + '</body>')
            got = run_chrome('g1_%s' % tag, wrap, ['END:%s' % w for w, _ in WIDTHS], budget=120000, win='1320,2400')
            show('%s · g1(iframe 390·768·1280)' % tag, got)
            lines += got if got is not None else ['FAIL | G1 g1 결과 줄 없음']
        if 'perf' in phases:
            p = os.path.join(OUT, 'app_perf_%s.html' % tag)
            io.open(p, 'w', encoding='utf-8', newline='\n').write(app_html(src, mk(pjs, {'n': 5548, 'gg': 1195, 'ggLen': 300})))
            got = run_chrome('perf_%s' % tag, p, ['END'], budget=None, timeout=1500)
            show('%s · perf(실시간)' % tag, got)
            lines += got if got is not None else ['FAIL | G5 perf 결과 줄 없음']
        res[tag] = lines
        meas[tag] = {x.split(' | ')[1]: json.loads(x.split(' | ', 2)[2]) for x in lines if x.startswith('MEAS | ')}

    print('=== 회귀 대조 — 같은 입력의 글자 (NEW vs HEAD) ===')
    vals = {t: [x for x in (res.get(t) or []) if x.startswith('VAL | ')] for t in ('NEW', 'HEAD')}
    vok = {}
    for a, b in zip(vals['NEW'], vals['HEAD']):
        name = a.split(' | ')[1]
        ok = a == b and name == b.split(' | ')[1]
        vok[name] = ok
        print('  %-24s %s' % (name, 'PASS 글자까지 같다' if ok else 'FAIL 다르다'))
        if not ok:
            io.open(os.path.join(OUT, 'val_%s_NEW.txt' % name), 'w', encoding='utf-8').write(a)
            io.open(os.path.join(OUT, 'val_%s_HEAD.txt' % name), 'w', encoding='utf-8').write(b)
    cnt_ok = len(vals['NEW']) == len(vals['HEAD'])
    print('  VAL 줄 NEW %d · HEAD %d' % (len(vals['NEW']), len(vals['HEAD'])))
    print()

    extra = []
    if 'perf' in phases and 'G6' in meas.get('NEW', {}) and 'G6' in meas.get('HEAD', {}):
        n6, h6 = meas['NEW']['G6'], meas['HEAD']['G6']
        ratio = h6['toggleSum'] / max(n6['toggleSum'], 0.01)
        print('=== G6 전환 시간(qiToggle 왕복 2회 · 헤드리스 PC · 실시간) — 옛 판 %.1fms → 새 판 %.1fms (%.0f배) · 렌더 가운데값 %.1fms → %.1fms ===' % (h6['toggleSum'], n6['toggleSum'], ratio, h6['renderMed'], n6['renderMed']))
        print('  옛 판 %s\n  새 판 %s' % (h6['toggle'], n6['toggle']))
        extra.append(('PASS' if n6['toggleSum'] < h6['toggleSum'] / 10 else 'FAIL') + ' | G6 qiToggle 왕복 2회 — 새 판이 옛 판보다 10배 넘게 빠르다 | %.1f → %.1f ms' % (h6['toggleSum'], n6['toggleSum']))
        for t in ('NEW', 'HEAD'):
            pf = meas[t].get('PROF')
            if pf:
                print('  %s 프로파일(렌더 평균 %sms) %s' % (t, pf['render'], pf['helpers']))
        print()
    if 'g1' in phases and 'G1.w390' in meas.get('HEAD', {}):
        h390 = meas['HEAD']['G1.w390']
        mk_ = re.match(r'^scale\(([0-9.]+)\)$', str(h390.get('tf', '')))
        nul = bool(mk_) and 0.35 < float(mk_.group(1)) < 0.45
        print('=== G1 헛잣대 — 옛 판 390 폭 transform = %r (안쪽 폭 %s ÷ 900) → %s ===' % (h390.get('tf'), h390.get('inner'), '약 0.4 배 축소가 나온다 · 잣대가 맞다' if nul else '★ 0.4 언저리 축소가 아니다 — 잣대가 틀렸다'))
        extra.append(('PASS' if nul else 'FAIL') + ' | G1 헛잣대 — 옛 판 390 폭에서 transform 이 scale(0.4 언저리) | %s' % h390.get('tf'))
        for t in ('NEW', 'HEAD'):
            print('  %s %s' % (t, {w: meas[t].get('G1.' + w) for w, _ in WIDTHS}))
        print()

    print('=== SRC 소스 대조 (NEW vs HEAD · add1) ===')
    Ln, Lh = new.split('\n'), head.split('\n')
    lits = lambda t: sorted(set(re.findall(r"""['"`](ox_[a-z0-9_]+)['"`]""", t)))
    body = lambda sig: '\n'.join(fn_lines(Ln, sig) or [])
    keep = ['function markHTML(', 'function renderMarked(', 'function applyMark(', 'function onSelectMaybe(', 'function offsetsInNode(', 'function loadMarks(',
            'function saveMarks(', 'function normalizeMarks(', 'function openJeongni(', 'function jnRowHTML(', 'function jnBodyHTML(', 'async function syncRecords(',
            'function stampAll(', 'async function dbGet(', 'async function dbPut(', 'function dbOpen(', 'async function dbDel(', 'function toggleTag(', 'function togglePeekExp(',
            'function oxPaint(', 'function ggLineHTML(', 'function gradeCurrentPage(', 'function qiPierce(', 'function qiUnder(', 'function qiSynth(', 'function qiToggle(',
            'function qiTool(', 'function qiToolsPaint(', 'function qiTapSkip(', 'function openQPopup(', 'function yujeOf(', 'function samePanrye(', 'function myLinkChipHTML(']
    keep_have = [s for s in keep if fn_lines(Lh, s) is not None]
    keep_diff = [s for s in keep_have if fn_lines(Ln, s) != fn_lines(Lh, s)]
    rq = body('function renderQuizPage() {').split('\n')
    chk = [('긴 줄(>3000자) 전부 글자까지 같다', [s for s in Ln if len(s) > 3000] == [s for s in Lh if len(s) > 3000]),
           ('SheetJS 줄(가장 긴 줄) 바이트 무변', max(Ln, key=len) == max(Lh, key=len) and len(max(Ln, key=len)) > 60000),
           ('SYNC_KEYS 무변', [s for s in Ln if 'const SYNC_KEYS = [' in s] == [s for s in Lh if 'const SYNC_KEYS = [' in s]),
           ('ox_* 글자 집합 같다(새 저장소 키 0)', lits(new) == lits(head)),
           ('§A #qcards{width:100%;max-width:900px;margin:0 auto} · transform-origin 0 · qcardsFit 몸통 = return 1 · qiScale 0',
            '#qcards{position:relative;width:100%;max-width:900px;margin:0 auto}' in new and 'transform-origin:top left' not in new
            and [s.strip() for s in (fn_lines(Ln, 'function qcardsFit() {') or [])] == ['function qcardsFit() {', 'return 1;', '}'] and not re.search(r'\bqiScale\b', new)),
           ('§A qiPathD·qiEraseAt 에 QI_W 0 · qiWire 가 W = 덮개 폭 · 묶음 w 저장·읽기(옛 값 = QI_W)',
            'QI_W' not in body('function qiPathD(p) {') and 'QI_W' not in body('function qiEraseAt(uid, x, y, W) {') and 'W = r.width || 1' in body('function qiWire(sv, uid) {')
            and '{ w: v.w || QI_W, s: v.s }' in body('function qiSave(uid) {') and '{ w: +v.w || QI_W, s: v.s } : { w: QI_W, s: [] }' in body('async function qiLoad(uids) {')),
           ('§B samePanryeChipHTML 옛 「같은 판례」 갈래 0 · 카드 호출 (item, true)', '같은 판례</span>' not in new and "${item.pending ? '' : samePanryeChipHTML(item, true)}" in new),
           ('§E renderQuizPage 첫 줄 qpCacheOpen · qiAfterRender 다음 줄 qpCacheClose · userLinks = linkStore()',
            len(rq) > 3 and rq[1].strip().startswith('qpCacheOpen();') and any(rq[k].strip().startswith('qiAfterRender(pageData);') and rq[k + 1].strip().startswith('qpCacheClose();') for k in range(len(rq) - 1))
            and any(s.strip().startswith('const userLinks = linkStore();') for s in rq)),
           ('§E ggStore·linkStore·refStore·loadQTypes·yujeBackOf 첫머리가 캐시',
            'if (GG_PAGE) return GG_PAGE;' in body('function ggStore() {') and 'if (LINK_PAGE) return LINK_PAGE;' in body('function linkStore() {')
            and 'if (REF_PAGE) return REF_PAGE;' in body('function refStore() {') and 'if (QTYPE_PAGE) return QTYPE_PAGE;' in body('function loadQTypes() {')
            and 'if (YUJE_PAGE) return' in body('function yujeBackOf(id) {')),
           ('§F qiGuard 안 scrollTop·수동 굴림 0 · #qcards 줄 touch-action:none 0 · 필기모드일 때만 터치 막기 손잡이',
            'scrollTop' not in body('function qiGuard() {') and 'pan = ' not in body('function qiGuard() {')
            and not any('#qcards' in s and 'touch-action:none' in s for s in Ln) and 'qiTouchWire();' in body('function qiAfterRender(pageData) {')),
           ('형광펜·정리 창·동기화·IndexedDB·펜 톡·덮개 뚫기·팝업 함수 %d개 무변 %s' % (len(keep_have), keep_diff or ''), not keep_diff and len(keep_have) >= 28)]
    for name, ok in chk:
        print('  %-70s %s' % (name, 'PASS' if ok else 'FAIL'))
    g_src = all(ok for _, ok in chk)
    print()

    print('=== 게이트 표 (NEW / HEAD) ===')
    allok = True
    nl = (res.get('NEW') or []) + extra
    for g in GATES:
        if g == 'SRC':
            print('  %-4s NEW %-8s' % (g, 'PASS' if g_src else 'FAIL'))
            continue
        t = tally(nl, g)
        vx = ''
        if g == 'G4':
            vx = ' · VAL %s' % ('PASS' if vok.get('G4.jeongni') else 'FAIL')
            allok = allok and bool(vok.get('G4.jeongni'))
        if g == 'VAL':
            gv = [k for k in vok if k.startswith('GV.')]
            vx = ' · 카드 글자 %d/%d' % (sum(1 for k in gv if vok[k]), len(gv))
            allok = allok and gv and all(vok[k] for k in gv) and cnt_ok
        print('  %-4s NEW %-8s HEAD %-8s%s' % (g, t, tally(res.get('HEAD'), g), vx))
        allok = allok and t != '—' and '/0F' in t
    nf = any(x.startswith('FAIL') for x in nl) or 'NEW' not in res
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
