# -*- coding: utf-8 -*-
r"""tt 관문(지어낸 기록) — tt_gate_c2rreal_1028.py 를 바탕으로 2026-11-14 채팅이 만듦(tt_plan_1114)

  python tt_gate_plan_1114.py --spec <명세.json> --new <패치한 timetable/index.html> --base <판(git)> [--eng chromium,webkit] [--base-eng chromium] [--only 칸이름앞머리,…]
  명세 = {"settle_ms", "data": {기록 경로: JSON 값} — 글자 "{{D1}}" · "{{D2}}" 는 관문이 날짜로 갈음(D1 = 10 주 전 월요일 · D2 = 12 주 뒤 일요일),
          "prelude": 화면마다 setup 앞 JS(문), "screens": {id: {"dev": "pc"|"ph", "setup": JS(식 · async 가능)}},
          "tests": [{"name", "screen", "pre": 누르기 전 JS(식 · async 가능), "act": "none"|"click"|"type"|"select", "sel", "nth", "hold": 누른 채 ms,
                     "text", "keys": [{"press"}|{"type"}], "value", "wait", "expect": 참일 JS 식, "yard": 바탕에서 FAIL 이어야 하면 true}]}
  앱 = 실제 주소(https://skygenie00.github.io/genie/timetable/)로 띄우되 응답은 route 로 이 파일이 줌(네트워크 안 씀)
  기록 = api.github.com contents → 명세 data 의 지어낸 값만(없는 경로 404) · PUT 은 이 관문 안에만 담아 다음 GET 에 돌려줌(원격 쓰기 0) · localStorage tt.cfg = 가짜 토큰 · 사람 꼬까
  화면(screen)마다 새 창 · 새 기록 — 한 화면 안의 칸은 차례대로 이어짐(앞 칸 상태에 기댐) · expect 안에서 window.__reqs = 그 화면에서 받은(GET) 기록 경로들
  결과: 줄마다 「PASS|FAIL | 칸 · 엔진 · 판」 · 끝에 합계 · 종료 코드 = FAIL 수(바탕 칸은 yard 와 다르면 FAIL)
"""
import base64, datetime, hashlib, json, subprocess, sys, time
from urllib.parse import unquote, urlparse
from playwright.sync_api import sync_playwright


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEWF, BASE = ARG('--new'), ARG('--base')
ENGS = [x for x in ARG('--eng', 'chromium,webkit').split(',') if x]
BENGS = [x for x in ARG('--base-eng', 'chromium').split(',') if x]
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
URL = 'https://skygenie00.github.io/genie/timetable/'
API = 'https://api.github.com/repos/zzikkaplan/studyplandata/contents/'
DEV = {'pc': (1100, 800), 'ph': (384, 740)}
KST = datetime.timezone(datetime.timedelta(hours=9))
T = datetime.datetime.now(KST).date()
MON = T - datetime.timedelta(days=T.weekday())
D1, D2 = (MON - datetime.timedelta(days=70)).isoformat(), (MON + datetime.timedelta(days=12 * 7 + 6)).isoformat()
SPEC = json.loads(open(ARG('--spec'), encoding='utf-8').read().replace('{{D1}}', D1).replace('{{D2}}', D2))
SRC = {'NEW': open(NEWF, encoding='utf-8').read()}
if BASE:
    SRC['BASE'] = subprocess.run(['git', 'show', BASE + ':timetable/index.html'], capture_output=True, check=True).stdout.decode('utf-8')
for k, v in SRC.items():
    print('%s md5 %s' % (k, hashlib.md5(v.replace('\r\n', '\n').encode('utf-8')).hexdigest()[:8]), flush=True)
print('프로젝트 %s ~ %s · 오늘 %s' % (D1, D2, T.isoformat()), flush=True)
LINES, FAILS = [], [0]


def out(s):
    print(s, flush=True)
    LINES.append(s)


def route(html, mem, reqs):
    def h(r):
        u = r.request.url
        if u.split('?')[0] == URL:
            return r.fulfill(status=200, content_type='text/html; charset=utf-8', body=html)
        if u.startswith(API):
            p = unquote(urlparse(u).path.split('/contents/', 1)[1])
            if r.request.method == 'PUT':
                try:
                    mem[p] = base64.b64decode(json.loads(r.request.post_data or '{}').get('content', '')).decode('utf-8')
                except Exception:
                    pass
                return r.fulfill(status=200, content_type='application/json', body=json.dumps({'content': {'sha': 'gate-%d' % int(time.time() * 1000)}}))
            if r.request.method != 'GET':
                return r.fulfill(status=200, content_type='application/json', body='{}')
            reqs.append(p)
            if p not in mem:
                return r.fulfill(status=404, body='')
            b = mem[p].encode('utf-8')
            if 'raw' in (r.request.headers.get('accept') or ''):
                return r.fulfill(status=200, content_type='text/plain; charset=utf-8', body=b)
            return r.fulfill(status=200, content_type='application/json',
                             body=json.dumps({'sha': hashlib.sha1(b).hexdigest(), 'content': base64.b64encode(b).decode()}))
        return r.fulfill(status=404, body='')
    return h


def run(br, eng, ver, sid, tests):
    sc = SPEC['screens'][sid]
    W, H = DEV[sc.get('dev', 'pc')]
    ctx = br.new_context(viewport={'width': W, 'height': H}, has_touch=sc.get('dev') == 'ph', timezone_id='Asia/Seoul', locale='ko-KR')
    ctx.add_init_script("try{localStorage.setItem('tt.cfg',JSON.stringify({token:'gate',person:'꼬까'}))}catch(e){}")
    pg = ctx.new_page()
    errs, reqs = [], []
    mem = {k: json.dumps(v, ensure_ascii=False) for k, v in SPEC.get('data', {}).items()}
    pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
    pg.route('**/*', route(SRC[ver], mem, reqs))
    res = {}
    EV = lambda js: pg.evaluate('async()=>{try{return await (async()=>(' + js + '))()}catch(e){return "ERR "+e}}')
    try:
        pg.goto(URL)
        pg.wait_for_function("typeof myPlan==='function'&&typeof syncAll==='function'", timeout=30000)
        pg.evaluate('async()=>{await syncAll(true)}')
        if SPEC.get('prelude'):
            pg.evaluate('()=>{' + SPEC['prelude'] + '}')
        r = EV(sc.get('setup', '0'))
        if isinstance(r, str) and r.startswith('ERR'):
            res['__setup'] = r
        pg.wait_for_timeout(int(SPEC.get('settle_ms', 1500)))
        for t in tests:
            try:
                if t.get('pre'):
                    r = EV(t['pre'])
                    if isinstance(r, str) and r.startswith('ERR'):
                        raise Exception('pre ' + r)
                    pg.wait_for_timeout(250)
                a = t.get('act', 'none')
                if a != 'none':
                    loc = pg.locator(t['sel']).nth(t.get('nth', 0))
                    if a == 'select':
                        loc.select_option(t['value'], timeout=8000)
                    else:
                        loc.click(timeout=8000, delay=int(t.get('hold', 0)))
                        if a == 'type':
                            pg.keyboard.type(t.get('text', ''), delay=20)
                            for k in t.get('keys', []):
                                if 'press' in k:
                                    pg.keyboard.press(k['press'])
                                else:
                                    pg.keyboard.type(k['type'], delay=20)
                pg.wait_for_timeout(int(t.get('wait', 500)))
                pg.evaluate('(a)=>{window.__reqs=a}', list(reqs))
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
                    ok, why = res.get(t['name'], (False, '안 돎'))
                    want = ok if ver == 'NEW' else (ok != bool(t.get('yard')))
                    if not want:
                        FAILS[0] += 1
                    tag = 'PASS' if want else 'FAIL'
                    note = '' if ver == 'NEW' else (' · 바탕 %s(%s)' % ('FAIL' if not ok else 'PASS', '헛잣대' if t.get('yard') else '무변'))
                    out('%s | %s · %s · %s%s%s' % (tag, t['name'], eng, ver, note, '' if want else ' | ' + why))
            out('INFO | %s · %s · %.1f 초' % (ver, eng, time.time() - T0))
            br.close()
out('합계 FAIL %d' % FAILS[0])
sys.exit(FAILS[0])
