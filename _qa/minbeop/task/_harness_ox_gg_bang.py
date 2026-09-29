# -*- coding: utf-8 -*-
"""민법OX 근거 「!」 표시 · 정리 창 「! N」 필터 · 「받아 둔 교재·시험지 지우기」 — _task_ox_gg_bang §D.

  NEW  = genie 작업트리 minbeop/index.html (고친 판)
  HEAD = git HEAD 의 같은 파일 (헛잣대 · G6 — 여기서 G1·G4 는 **실패해야** 한다)

⚠ 헤드리스가 진짜 망에 안 나간다 — `fetch` 를 통째로 가짜로 만든다(PDF 도 목록도 안 받는다).
⚠ `window.onload` 는 끈다(가상 시계보다 늦게 끝나 거짓 FAIL) · 결과는 `console.log('HZR|…')` 로 stderr 에서 받는다.
⚠ 문항은 `buildQuizData(P.rows)` 로 그 자리에서 심는다 — 서버를 안 거친다.

쓰기 : python _harness_ox_gg_bang.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

GENIE = _roots.genie()
SPD = _roots.spd()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(tempfile.gettempdir(), 'h_ggbang')
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
REL = 'minbeop/index.html'
GPUSH = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'g_push.cmd')

RES = []


def add(gate, ok, text):
    RES.append((gate, ok, text))
    print('  %s %-4s %s' % ('OK  ' if ok else 'FAIL', gate, text))


def git(*a):
    return subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a),
                          capture_output=True).stdout


SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__CERR=[];(function(){var ce=console.error.bind(console);console.error=function(){try{__CERR.push(Array.prototype.map.call(arguments,function(x){return typeof x==='string'?x:(x&&x.message)||JSON.stringify(x)}).join(' '))}catch(e){}return ce.apply(null,arguments);};})();
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
    byuid = {}
    for r in rows:
        if r.get('uid') and r.get('문제'):
            byuid[r['uid']] = {k: (str(r.get(k, ''))[:300] if k == '해설' else r.get(k, '')) for k in keep}
    # 서로 다른 **두 단원**에서 문항 넷을 고른다(G4 가 단원 두 개를 봐야 한다)
    grp = {}
    for r in rows:
        if not (r.get('uid') and r.get('문제')):
            continue
        g = '%s · %s' % (r.get('과목', ''), r.get('세부단원', '') or r.get('장', ''))
        grp.setdefault(g, []).append(r['uid'])
    gs = [g for g in sorted(grp) if len(grp[g]) >= 3]
    a, own, b = grp[gs[0]][0], grp[gs[0]][1], grp[gs[0]][2]
    c = grp[gs[1]][0]
    d = grp[gs[2]][0]          # 켜지지 않는 세 번째 단원 — G4 가 「줄어드는지」를 재려면 있어야 한다
    pick = [a, own, b, c, d]
    # 카드에 그릴 문항 + 같은 단원 몇 개(분포가 단원 여럿을 갖게)
    more = []
    for g in gs[:6]:
        more += grp[g][:3]
    ids = list(dict.fromkeys(pick + more))
    src = git('show', 'HEAD:' + REL).decode('utf-8')
    sk = re.search(r'const SYNC_KEYS = \[(.+?)\];', src, re.S).group(1)
    sync = ','.join(re.findall(r"'([^']+)'", sk))
    return {'rows': [byuid[u] for u in ids if u in byuid],
            'a': a, 'own': own, 'b': b, 'c': c, 'd': d, 'syncKeys': sync}


def gate_files():
    print('\n=== D11 가드 · 줄끝 · 무접촉 ===')
    g = io.open(GPUSH, 'rb').read().decode('cp949', 'replace')
    paths = re.search(r'^set "PATHS=(.+?)"', g, re.M).group(1).split()
    add('D11', 'minbeop' in paths, 'ⓐ PATHS(%d) = %s' % (len(paths), ' '.join(paths)))
    cmds = [l for l in g.split('\n') if not re.match(r'^\s*rem\b', l, re.I) and l.strip()]
    bad = [l.strip() for l in cmds if re.search(r'\badd\b[^\n]*\s-A\b', l)]
    add('D11', not bad, 'ⓒ `git add -A` 안 쓴다 (걸린 줄 %s)' % bad)
    app = io.open(os.path.join(GENIE, REL), 'rb').read()
    add('D11', app.count(b'\r\n') == 0, '앱 작업트리 CRLF %d' % app.count(b'\r\n'))
    add('D11', hashlib.md5(app).hexdigest() != hashlib.md5(git('show', 'HEAD:' + REL)).hexdigest(),
        '앱이 실제로 바뀌었다 md5 %s' % hashlib.md5(app).hexdigest()[:12])
    # 다른 앱 무접촉 (G5)
    ch = [l for l in git('diff', '--name-only', 'HEAD').decode('utf-8').split('\n') if l.strip()]
    add('G5', ch == [REL], '바뀐 파일은 %s 하나뿐 : %s' % (REL, ch))


def main():
    os.makedirs(OUT, exist_ok=True)
    print('OUT =', OUT)
    gate_files()

    print('\n=== 헤드리스 ===')
    P = payload()
    print('  문항 %d · A=%s OWN=%s B=%s C=%s D=%s' % (len(P['rows']), P['a'], P['own'], P['b'], P['c'], P['d']))
    tests = io.open(os.path.join(HERE, '_harness_ox_gg_bang_tests.js'), encoding='utf-8').read()
    js = tests.replace('__P__', json.dumps(P, ensure_ascii=False))

    outs = {}
    for tag, src in (('NEW', io.open(os.path.join(GENIE, REL), encoding='utf-8').read()),
                     ('HEAD', git('show', 'HEAD:' + REL).decode('utf-8'))):
        outs[tag] = run(tag, build(tag, src, js))

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
            body = x.split(' | ', 1)[1]
            g = body.split(' ')[0]
            if not re.match(r'^G\d$', g):
                g = 'SRC'
            add(g, x.startswith('PASS'), body)
        elif x.startswith('INFO'):
            print('       ' + x)

    vn, vh = vals(outs['NEW']), vals(outs['HEAD'])
    for k in sorted(vn):
        if k.startswith(('G2.', 'G3.', 'G4.', 'G7.', 'SRC.')):
            print('       %-16s %s' % (k, vn[k][:150]))

    print('\n=== G6 헛잣대 (HEAD 판) ===')
    hf = [x for x in outs['HEAD'] if x.startswith(('PASS', 'FAIL'))]
    for g in ('G1', 'G4'):
        gl = [x for x in hf if x.split(' | ')[1].split(' ')[0] == g]
        bad = [x for x in gl if x.startswith('FAIL')]
        add('G6', len(gl) > 0 and len(bad) > 0, '옛 판 %s : %d줄 중 FAIL %d' % (g, len(gl), len(bad)))
    add('G6', vh.get('SRC.ggBangToggle') == '"undefined"',
        '옛 판에 ggBangToggle 없음 (%s)' % vh.get('SRC.ggBangToggle'))
    add('G6', vn.get('SRC.ggBangToggle') == '"function"',
        '새 판에 ggBangToggle 있음 (%s)' % vn.get('SRC.ggBangToggle'))
    add('G6', vh.get('SRC.mbForgetPrompt') == '"undefined"',
        '옛 판에 mbForgetPrompt 없음 (%s)' % vh.get('SRC.mbForgetPrompt'))

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
