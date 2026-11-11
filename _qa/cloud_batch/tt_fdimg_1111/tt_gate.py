# -*- coding: utf-8 -*-
r"""tt 작은 고침 관문 — 공용 _qa_small_gate.py 가 자과 전용이라 tt(timetable) 판에 쓰는 같은 꼴 명세 관문 (2026-10-28 채팅 · tt_c2rreal_1028)

  python tt_gate.py --spec <명세.json> --new <패치한 timetable/index.html> --base <판(git)> --spd <studyplandata 클론> [--eng chromium,webkit] [--base-eng chromium] [--only 칸이름앞머리,…]
  명세 = {"settle_ms", "prelude": 화면마다 setup 앞 JS(문), "screens": {id: {"dev": "pc"|"ph", "setup": JS(식 · async 가능)}},
          "tests": [{"name", "screen", "act": "click"|"none", "sel", "nth", "wait", "expect": 엔진에서 참일 JS 식, "yard": 바탕에서 FAIL 이어야 하면 true}]}
  앱 = 실제 주소(https://skygenie00.github.io/genie/timetable/)로 띄우되 응답은 route 로 이 파일이 줌(네트워크 안 씀)
  기록 = api.github.com contents → --spd 클론 파일(읽기만 · PUT 은 가짜 200 · 원격 쓰기 0) · localStorage tt.cfg = 가짜 토큰 · 사람 꼬까
  결과: 줄마다 「PASS|FAIL | 칸 · 엔진 · 판」 · 끝에 합계 · 종료 코드 = FAIL 수(바탕 칸은 yard 와 다르면 FAIL)
"""
import base64, hashlib, json, os, subprocess, sys, time
from urllib.parse import unquote, urlparse
from playwright.sync_api import sync_playwright


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


SPEC = json.load(open(ARG('--spec'), encoding='utf-8'))
NEWF, BASE, SPD = ARG('--new'), ARG('--base'), ARG('--spd')
ENGS = [x for x in ARG('--eng', 'chromium,webkit').split(',') if x]
BENGS = [x for x in ARG('--base-eng', 'chromium').split(',') if x]
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
URL = 'https://skygenie00.github.io/genie/timetable/'
API = 'https://api.github.com/repos/zzikkaplan/studyplandata/contents/'
DEV = {'pc': (1100, 800), 'ph': (384, 740)}
SRC = {'NEW': open(NEWF, encoding='utf-8').read()}
if BASE:
    SRC['BASE'] = subprocess.run(['git', 'show', BASE + ':timetable/index.html'], capture_output=True, check=True).stdout.decode('utf-8')
for k, v in SRC.items():
    print('%s md5 %s' % (k, hashlib.md5(v.encode('utf-8')).hexdigest()[:8]), flush=True)
LINES, FAILS = [], [0]


def out(s):
    print(s, flush=True)
    LINES.append(s)


def route(html):
    def h(r):
        u = r.request.url
        if u.split('?')[0] == URL:
            return r.fulfill(status=200, content_type='text/html; charset=utf-8', body=html)
        if u.startswith(API):
            if r.request.method != 'GET':
                return r.fulfill(status=200, content_type='application/json', body=json.dumps({'content': {'sha': 'gate-%d' % time.time()}}))
            p = unquote(urlparse(u).path.split('/contents/', 1)[1])
            f = os.path.join(SPD, *p.split('/'))
            if not os.path.isfile(f):
                return r.fulfill(status=404, body='')
            b = open(f, 'rb').read()
            if 'raw' in (r.request.headers.get('accept') or ''):
                return r.fulfill(status=200, content_type='text/plain; charset=utf-8', body=b)
            return r.fulfill(status=200, content_type='application/json',
                             body=json.dumps({'sha': hashlib.sha1(b).hexdigest(), 'content': base64.b64encode(b).decode()}))
        return r.fulfill(status=404, body='')
    return h


def run(br, eng, ver, sid, tests):
    sc = SPEC['screens'][sid]
    W, H = DEV[sc.get('dev', 'pc')]
    ctx = br.new_context(viewport={'width': W, 'height': H}, has_touch=sc.get('dev') == 'ph')
    ctx.add_init_script("try{localStorage.setItem('tt.cfg',JSON.stringify({token:'gate',person:'꼬까'}))}catch(e){}")
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
    pg.route('**/*', route(SRC[ver]))
    res = {}
    try:
        pg.goto(URL)
        pg.wait_for_function("typeof examGet==='function'&&typeof anaIdx==='function'", timeout=30000)
        if SPEC.get('prelude'):
            pg.evaluate('()=>{' + SPEC['prelude'] + '}')
        r = pg.evaluate('async()=>{try{return await (async()=>(' + sc.get('setup', '0') + '))()}catch(e){return "setup ERR "+e}}')
        if isinstance(r, str) and 'ERR' in r:
            res['__setup'] = r
        pg.wait_for_timeout(int(SPEC.get('settle_ms', 4000)))
        for t in tests:
            try:
                if t.get('act', 'none') == 'click':
                    pg.locator(t['sel']).nth(t.get('nth', 0)).click(timeout=8000)
                pg.wait_for_timeout(int(t.get('wait', 600)))
                v = pg.evaluate('()=>(' + t['expect'] + ')')
                res[t['name']] = (v is True, '' if v is True else str(v)[:300])
            except Exception as e:
                res[t['name']] = (False, 'ERR ' + str(e).split('\n')[0][:200])
    finally:
        res['__errs'] = errs
        ctx.close()
    return res


with sync_playwright() as P:
    for ver, engs in (('NEW', ENGS), ('BASE', BENGS if BASE else [])):
        for eng in engs:
            br = getattr(P, eng).launch()
            T0 = time.time()
            for sid in SPEC['screens']:
                ts = [t for t in SPEC['tests'] if t['screen'] == sid and (not ONLY or any(t['name'].startswith(o) for o in ONLY))]
                if not ts:
                    continue
                res = run(br, eng, ver, sid, ts)
                if res.get('__setup'):
                    out('FAIL | setup %s · %s · %s | %s' % (sid, eng, ver, res['__setup']))
                    FAILS[0] += 1
                if res['__errs']:
                    out('FAIL | 페이지 오류 %s · %s · %s | %s' % (sid, eng, ver, ' / '.join(res['__errs'][:3])))
                    FAILS[0] += 1
                for t in ts:
                    ok, why = res[t['name']]
                    want = ok if ver == 'NEW' else (ok != bool(t.get('yard')))
                    if not want:
                        FAILS[0] += 1
                    tag = 'PASS' if want else 'FAIL'
                    note = '' if ver == 'NEW' else (' · 바탕 %s(%s)' % ('FAIL' if not ok else 'PASS', '헛잣대' if t.get('yard') else '무변'))
                    out('%s | %s · %s · %s%s%s' % (tag, t['name'], eng, ver, note, '' if want else ' | ' + why))   # 까닭은 기대와 다를 때만(헛잣대 FAIL 값 = 기록 값이라 안 찍음 · 공개 저장소)
            out('INFO | %s · %s · %.1f 초' % (ver, eng, time.time() - T0))
            br.close()
out('합계 FAIL %d' % FAILS[0])
sys.exit(FAILS[0])
