# -*- coding: utf-8 -*-
"""민법OX ① 자리 그림 · ② 자리 가져오기(ref) · ③④ 댓글 · ⑤ 회독 표시 — _task_ox_jari_thumb §E.

  NEW  = genie 작업트리 minbeop/index.html (고친 판)
  HEAD = git HEAD 의 같은 파일 (헛잣대 · E-5 는 여기서도 **깨지지 않아야** 한다)

⚠ 헤드리스가 진짜 망에 안 나간다 — `fetch` 를 통째로 가짜로 만든다.
⚠ `window.onload` 는 끈다(가상 시계보다 늦게 끝나 거짓 FAIL) · 결과는 `console.log('HZR|…')` 로 stderr 에서 받는다.
⚠ 근거 창은 網을 타므로 열지 않는다 — `window.mbBook.listHTML/picFill`(검산용 내보내기)로 목록 HTML 을 그 자리에서 잰다.

쓰기 : python _harness_ox_jari_thumb.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2(10/8) 실행 모드 --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같음) · import 때 --mode · --snap-in · --snap-out 을 sys.argv 에서 뗀다
import hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

GENIE = _roots.genie()
SPD = _roots.spd()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(tempfile.gettempdir(), 'h_jarithumb')
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
REL = 'minbeop/index.html'
GPUSH = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'g_push.cmd')

RES = []


def add(gate, ok, text):
    RES.append((gate, ok, text))
    print('  %s %-5s %s' % ('OK  ' if ok else 'FAIL', gate, text))


def git(*a):
    return subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a),
                          capture_output=True).stdout


SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__ALERTS=[];window.alert=function(m){__ALERTS.push(String(m));};
window.__CONFIRMS=[];window.__CONFIRM_ANS=true;window.confirm=function(m){__CONFIRMS.push(String(m));return window.__CONFIRM_ANS;};window.prompt=function(){return null;};
window.__NET=[];window.fetch=function(u){window.__NET.push(String((u&&u.url)||u));return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));};
localStorage.clear();
</script>"""


def build(tag, src, tests):
    b = src.index('<body')
    bb = src.index('>', b) + 1
    html = src[:bb] + SEED + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + tests + '\n</script>\n' + html[e:]
    p = os.path.join(OUT, 'h_%s.html' % tag)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(html)
    return p


def run(tag, path, budget=600000):
    prof = os.path.join(OUT, 'prof_' + tag)
    shutil.rmtree(prof, ignore_errors=True)
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
                        '--no-default-browser-check', '--user-data-dir=' + prof,
                        '--allow-file-access-from-files', '--window-size=1280,900',
                        '--enable-logging=stderr', '--v=0',
                        '--virtual-time-budget=%d' % budget, '--dump-dom',
                        'file:///' + path.replace('\\', '/')],
                       capture_output=True, timeout=1200)
    err = r.stderr.decode('utf-8', 'replace')
    io.open(os.path.join(OUT, 'chrome_err_%s.txt' % tag), 'w', encoding='utf-8').write(err)
    hz = []
    for ln in err.split('\n'):
        i = ln.find('"HZR|')
        if i >= 0:
            j = ln.find('"', i + 5)
            hz.append(urllib.parse.unquote(ln[i + 5:j]))
    print('  [%s] chrome rc %s · HZR %d' % (tag, r.returncode, len(hz)))
    io.open(os.path.join(OUT, 'lines_%s.txt' % tag), 'w', encoding='utf-8').write('\n'.join(hz))
    return [x for x in hz if x.strip() and x != 'END']


def payload():
    rows = json.load(io.open(os.path.join(SPD, 'minbeop', '문항마스터.json'), encoding='utf-8'))['rows']
    keep = ['uid', '번호', '하위', '문제', '정답', '해설', '과목', '장', '세부단원', '구분',
            '기출연도', '회차', '문번', '지문', '출제연도', '출처', '상태']
    byuid, order = {}, []
    for r in rows:
        if r.get('uid') and r.get('문제') and r['uid'] not in byuid:
            byuid[r['uid']] = {k: (str(r.get(k, ''))[:300] if k == '해설' else r.get(k, '')) for k in keep}
            order.append(r['uid'])
    ids = order[:8]
    if QC.GATE:
        QC.sub('git:show-app')
    src = git('show', 'HEAD:' + REL).decode('utf-8') if QC.GATE else io.open(os.path.join(GENIE, REL), encoding='utf-8').read()   # regress — HEAD 판을 안 푼다: SYNC_KEYS · MBB_VOL 첫 책은 새 판 글에서(사슬 gate 에서도 HEAD = 새 판)
    sk = re.search(r'const SYNC_KEYS = \[(.+?)\];', src, re.S).group(1)
    sync = ','.join(re.findall(r"'([^']+)'", sk))
    m = re.search(r'MBB_VOL\s*=\s*\{([^}]*)\}', src)
    bookdoc = ''
    if m:
        dm = re.search(r"'([^']+)'\s*:", m.group(1))
        if dm:
            bookdoc = dm.group(1)
    return {'rows': [byuid[u] for u in ids], 'a': ids[0], 'b': ids[1], 'c': ids[2],
            'syncKeys': sync, 'bookDoc': bookdoc}


def gate_files():
    print('\n=== §0 · D11 가드 · 줄끝 · 무접촉 ===')
    if QC.GATE:   # push 가드(g_push.cmd 글자) — 앱 회귀 아님 · 그 판 인도 가드 = 관문만
        g = io.open(GPUSH, 'rb').read().decode('cp949', 'replace')
        paths = re.search(r'^set "PATHS=(.+?)"', g, re.M).group(1).split()
        add('D11', 'minbeop' in paths, 'ⓐ PATHS(%d) = %s' % (len(paths), ' '.join(paths)))
        cmds = [l for l in g.split('\n') if not re.match(r'^\s*rem\b', l, re.I) and l.strip()]
        bad = [l.strip() for l in cmds if re.search(r'\badd\b[^\n]*\s-A\b', l)]
        add('D11', not bad, 'ⓒ `git add -A` 안 쓴다 (걸린 줄 %s)' % bad)
    app = io.open(os.path.join(GENIE, REL), 'rb').read()
    if QC.GATE:
        QC.sub('git:show-app')
    head = git('show', 'HEAD:' + REL) if QC.GATE else None   # regress — HEAD 판을 안 푼다
    if QC.GATE:   # 착수 md5 = 지시서 값(고정 옛 판) — 관문만
        add('E-1', hashlib.md5(head).hexdigest() == '209bcf17ec519b4b12e4004498126a04',
            '착수 HEAD md5 = 지시서 §0 값 (%d B · %s)' % (len(head), hashlib.md5(head).hexdigest()[:12]))
    add('D11', app.count(b'\r\n') == 0, '앱 작업트리 CRLF %d' % app.count(b'\r\n'))
    if QC.GATE:   # 인도 때 작업트리 · HEAD diff 가드 = 관문만(사슬은 깨끗한 워크트리 · HEAD = 새 판)
        add('E-1', hashlib.md5(app).hexdigest() != hashlib.md5(head).hexdigest(),
            '끝 판 %d B · md5(LF) %s' % (len(app), hashlib.md5(app).hexdigest()))
        ch = [l for l in git('diff', '--name-only', 'HEAD').decode('utf-8').split('\n') if l.strip()]
        add('E-9', ch == [REL], '바뀐 파일은 %s 하나뿐 : %s' % (REL, ch))
    txt = app.decode('utf-8')
    if QC.GATE:
        add('E-9', txt.count('SYNC_KEYS') == head.decode('utf-8').count('SYNC_KEYS')
            and re.search(r'const SYNC_KEYS = \[(.+?)\];', txt, re.S).group(1)
            == re.search(r'const SYNC_KEYS = \[(.+?)\];', head.decode('utf-8'), re.S).group(1),
            'SYNC_KEYS 줄 무변')
    else:   # regress — HEAD 판 대신 기준 스냅샷(앞 인도판 새 판의 「SYNC_KEYS」 낱말 수 · 줄)
        skv = [txt.count('SYNC_KEYS'), re.search(r'const SYNC_KEYS = \[(.+?)\];', txt, re.S).group(1)]
        add('E-9', skv == QC.base('E-9/SYNC_KEYS', skv), 'SYNC_KEYS 줄 무변')
    # E-4 — 화면이 없어도 재는 자리: 갈래가 소스에 박혀 있다
    pa = txt[txt.index('function paint()'):txt.index('function boxCss')]
    add('E-4', "if (!isMine && V.mode === 'pick')" in pa,
        '뷰 모드에서는 남의 상자에 포인터·클릭을 안 단다(pick 일 때만)')
    add('E-4', pa.count("box.style.pointerEvents") == 1 and "box.style.pointerEvents = 'auto'" in pa,
        '상자에 pointer-events 를 켜는 자리는 그 한 곳뿐(층 L 의 종전 두 줄은 무변)')
    bd = txt[txt.index('function bindDrag()'):txt.index('async function saveRect')]
    add('E-4', 'if (V.refPop) { start = null;' in bd,
        '팝업이 떠 있으면 드래그를 시작하지 않는다(닫기만)')
    add('E-9', 'ox_mem_cards' not in re.sub(r'/\*.*?\*/', '', txt[txt.index('function mbbPicDraw'):txt.index('function mbbPicFill')], flags=re.S),
        '① 그림 코드가 ox_mem_cards 를 안 건드린다')


def main():
    if QC.SMOKE:   # smoke 칸 없음(A-0) — 앱을 띄우기 전에 한 줄 찍고 끝
        print('INFO | smoke 칸 없음 | 자리 그림 · 자리 가져오기 · 댓글 · 회독 표시 하네스 — smoke 칸 없음(A-0) · 앱 안 띄움', flush=True)
        return 0
    os.makedirs(OUT, exist_ok=True)
    print('OUT =', OUT)
    gate_files()

    print('\n=== 헤드리스 ===')
    P = payload()
    print('  문항 %d · A=%s B=%s C=%s · bookDoc=%s' % (len(P['rows']), P['a'], P['b'], P['c'], P['bookDoc'] or '(없음)'))
    tests = io.open(os.path.join(HERE, '_harness_ox_jari_thumb_tests.js'), encoding='utf-8').read()
    js = tests.replace('__P__', json.dumps(P, ensure_ascii=False))

    outs = {}
    for tag, src in ((('NEW', io.open(os.path.join(GENIE, REL), encoding='utf-8').read()),
                      ('HEAD', git('show', 'HEAD:' + REL).decode('utf-8'))) if QC.GATE else
                     (('NEW', io.open(os.path.join(GENIE, REL), encoding='utf-8').read()),)):   # regress — 새 판만(HEAD 판 = 헛잣대 · ok/ng 찍기만 · 사슬에선 HEAD = 새 판)
        QC.launch('new' if tag == 'NEW' else 'base')
        outs[tag] = run(tag, build(tag, src, js))

    for tag in (('NEW', 'HEAD') if QC.GATE else ('NEW',)):
        print('\n=== 헤드리스 결과 (%s) ===' % tag)
        for x in outs[tag]:
            if x.startswith(('PASS', 'FAIL')):
                ok = x.startswith('PASS')
                body = x.split(' | ', 1)[1]
                if tag == 'NEW':
                    add(body.split(' ')[0], ok, body)
                else:
                    print('  %s %s' % ('ok  ' if ok else 'ng  ', body[:130]))
            elif x.startswith('INFO'):
                print('  ----  %s' % x.split(' | ', 1)[1][:160])
            elif x.startswith('VAL'):
                print('  ----  %s' % x.split(' | ', 1)[1][:200])

    nf = [r for r in RES if not r[1]]
    print('\n==== PASS %d · FAIL %d ====' % (len(RES) - len(nf), len(nf)))
    for g, ok, t in nf:
        print('   FAIL %-5s %s' % (g, t[:150]))
    return 1 if nf else 0


if __name__ == '__main__':
    sys.exit(main())
