# -*- coding: utf-8 -*-
r"""민법OX · 조판기 작은 고침 관문 — ox_gate.py(11/02 ox_gglive_1102 · 3e563659) 그대로 + 11/10 ggjigak_1110: 명세 "app"(minbeop | jo) · 폰 384×740 터치 · act click 에 "hold"(누른 채 ms = 길게 누름) · act "drag"(칸 가운데 눌러 dy 끌기) · act type 뒤 "enter" · "keys"(차례로 누름) · 조판기 = 상대 주소 data/… 를 --root(저장소 jo/) 파일로

  python gg_gate.py --spec <명세.json> --new <패치한 앱 index.html> --base <판(git)> --spd <studyplandata 클론> [--root <jo 폴더 · 조판기만>] [--eng chromium,webkit] [--base-eng chromium] [--only 칸이름앞머리,…]
  명세 = {"settle_ms", "prelude": 화면마다 setup 앞 JS(문), "screens": {id: {"dev": "pc"|"ph", "setup": JS(식 · async 가능)}},
          "tests": [{"name", "screen", "act": "click"|"type"|"press"|"none", "sel", "nth", "text"(type), "key"(press · 지금 초점 칸에), "wait", "expect": 엔진에서 참일 JS 식, "yard": 바탕에서 FAIL 이어야 하면 true}]}
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
APP = SPEC.get('app', 'minbeop')
ROOT = ARG('--root')
URL = 'https://skygenie00.github.io/genie/' + APP + '/'
API = 'https://api.github.com/repos/zzikkaplan/studyplandata/contents/'
DEV = {'pc': (1100, 800), 'ph': (384, 740)}
SRC = {'NEW': open(NEWF, encoding='utf-8').read()}
if BASE:
    SRC['BASE'] = subprocess.run(['git', 'show', BASE + ':' + APP + '/index.html'], capture_output=True, check=True).stdout.decode('utf-8')
for k, v in SRC.items():
    print('%s md5 %s' % (k, hashlib.md5(v.encode('utf-8')).hexdigest()[:8]), flush=True)
LINES, FAILS = [], [0]


def out(s):
    print(s, flush=True)
    LINES.append(s)


def route(html):
    def h(r):
        u = r.request.url
        if any(h in u for h in ('cdn.tailwindcss.com', 'cdnjs.cloudflare.com', 'cdn.jsdelivr.net', 'unpkg.com')):   # ★ 11/10 — 앱이 쓰는 CDN(Tailwind 등)은 그대로 받음(시안 snap 과 같게 · 안 받으면 text-[10.5px] 같은 꼴이 안 서서 글 크기 칸이 다름 · 잼)
            return r.continue_()
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
        if ROOT and u.split('?')[0].startswith(URL):   # ★ 11/10 — 조판기 상대 주소(data/…) = 저장소 jo/ 파일(읽기만)
            f = os.path.join(ROOT, *unquote(urlparse(u).path)[len(urlparse(URL).path):].split('/'))
            if os.path.isfile(f):
                ct = 'application/json; charset=utf-8' if f.endswith('.json') else 'application/octet-stream'
                return r.fulfill(status=200, content_type=ct, body=open(f, 'rb').read())
        return r.fulfill(status=404, body='')
    return h


def run(br, eng, ver, sid, tests):
    sc = SPEC['screens'][sid]
    W, H = DEV[sc.get('dev', 'pc')]
    ctx = br.new_context(viewport={'width': W, 'height': H}, has_touch=sc.get('dev') == 'ph', is_mobile=sc.get('dev') == 'ph')   # ★ 11/10 — 폰 = 터치 + (pointer:coarse) 규칙 켬(시안 snap 과 같게)
    ctx.add_init_script("try{localStorage.setItem('tt.cfg',JSON.stringify({token:'gate',person:'꼬까'}))}catch(e){}")
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
    pg.route('**/*', route(SRC[ver]))
    res = {}
    try:
        pg.goto(URL)
        pg.wait_for_function(SPEC.get('ready', "typeof quizData!=='undefined'&&quizData.length>0"), timeout=90000)
        if SPEC.get('prelude'):
            pg.evaluate('()=>{' + SPEC['prelude'] + '}')
        r = pg.evaluate('async()=>{try{return await (async()=>(' + sc.get('setup', '0') + '))()}catch(e){return "setup ERR "+e}}')
        if isinstance(r, str) and 'ERR' in r:
            res['__setup'] = r
        pg.wait_for_timeout(int(SPEC.get('settle_ms', 4000)))
        for t in tests:
            try:
                if t.get('act', 'none') == 'click':
                    pg.locator(t['sel']).nth(t.get('nth', 0)).click(timeout=8000, delay=int(t.get('hold', 0)))   # ★ 11/10 — hold ms = 길게 누름
                elif t.get('act') == 'drag':   # ★ 11/10 — 칸 가운데를 눌러 dy · dx 만큼 끌고 뗌(굴림 · 끌기는 고치기를 안 끝내야 함)
                    l = pg.locator(t['sel']).nth(t.get('nth', 0)); l.scroll_into_view_if_needed(timeout=8000); bb = l.bounding_box(); x0, y0 = bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2
                    pg.mouse.move(x0, y0); pg.mouse.down(); pg.mouse.move(x0 + t.get('dx', 0), y0 + t.get('dy', 0), steps=12); pg.mouse.up()
                elif t.get('act') == 'type':
                    pg.locator(t['sel']).nth(t.get('nth', 0)).click(timeout=8000)
                    pg.keyboard.type(t['text'], delay=60)
                    if t.get('enter'): pg.keyboard.press('Enter')   # ★ 11/10
                    for k in t.get('keys', []): pg.keyboard.press(k)   # ★ 11/10 — 차례로(Escape 등)
                elif t.get('act') == 'press':
                    pg.keyboard.press(t['key'])
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
