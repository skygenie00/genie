# -*- coding: utf-8 -*-
r"""_task_jagwa_bio_ocrfix_add2 §B 관문 — 비고·교재문장 전각 → 반각 · 타기출 카드 제목 출처 · 멱등 · 다른 칸 무변

  바탕(헛잣대) = studyplandata 0675d712 의 bio/문항.json(add1 인도판 · md5 0fd627d1 — git 에서 꺼내 못 박는다)
  새 값 = 바탕 사본에 _ocrfix_bio.py write 를 두 번(멱등) — 인도 뒤면 studyplandata 로컬 bio/문항.json 과 바이트가 같아야 한다
  앱 = genie 작업트리 jagwa/index.html(앱은 안 고친다) · 누름 = page.mouse · 손가락 = CDP 터치 r22(Chromium) · WebKit = mouse · el.click() 없음
  몸통(서버 · 앱 흉내 網 · __h 도구)은 본판 하네스(_harness_bio_ocrfix.py)를 그대로 불러 쓴다.

쓰기 : python _harness_bio_ocrfix_add2.py [--out 파일]   결과 = _harness_bio_ocrfix_result.txt 끝에 이어 붙인다(--out 이면 그 파일에 새로)
"""
import collections, hashlib, io, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _harness_bio_ocrfix as B   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


OUTF = ARG('--out', os.path.join(HERE, '_harness_bio_ocrfix_result.txt'))
BASE_REV, BASE_MD5 = '0675d712', '0fd627d17ba8ed34eb1186af633f042b'
WORK = os.path.join(B.WORK, 'add2'); os.makedirs(WORK, exist_ok=True)
BASEQ, NEWQ = os.path.join(WORK, '문항_base.json'), os.path.join(WORK, '문항_new.json')
FWS = '（）、，：；［］｛｝＜＞！'
FWT = str.maketrans({c: h for c, h in zip(FWS, '(),,:;[]{}<>!')})
TITLES = {'T012': '타기출 · 2014년 서울시', 'T013': '타기출 · 학력평가', 'T015': '타기출 · 의대편입'}
RES = []


def T(name, ok, detail=''):
    RES.append(('PASS' if ok else 'FAIL', name, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('%s | %s | %s' % ('PASS' if ok else 'FAIL', name, d[:300]), flush=True)


def N(name, detail=''):
    RES.append(('NOTE', name, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('NOTE | %s | %s' % (name, d[:300]), flush=True)


def fwcount(v):
    """행 안 모든 글(문자열 · 목록 · 칸 안까지)의 바꿈표 글자 수"""
    if isinstance(v, str):
        return sum(v.count(c) for c in FWS)
    if isinstance(v, list):
        return sum(fwcount(x) for x in v)
    if isinstance(v, dict):
        return sum(fwcount(x) for x in v.values())
    return 0


APPJS = r"""
Object.assign(window.__h,{
 item(u){const it=[...document.querySelectorAll('#list .item')].find(x=>x.dataset.uid===u||__h.tx(x.querySelector('.num'))===u);if(!it)return null;
   it.scrollIntoView({block:'center'});const r=it.getBoundingClientRect();const x=r.left+Math.min(r.width/2,60),y=r.top+r.height/2;const t=document.elementFromPoint(x,y);
   return {x,y,vis:__h.vis(it),hit:!!t&&(t===it||it.contains(t))}},
 title(){const t=document.getElementById('vT1');return t?{t:__h.tx(t),vis:__h.vis(t)}:null},
 note(){const c=document.getElementById('card');const n=c&&c.querySelector('.cnote');return n?{t:__h.tx(n),vis:__h.vis(n)}:null},
 sum(){const s=document.querySelector('#cDet>summary');if(!s)return null;s.scrollIntoView({block:'center'});const r=s.getBoundingClientRect();return {x:r.left+Math.min(r.width/2,60),y:r.top+r.height/2}}
});
"""


def launch(pw, eng, app, qjson, tag, touch):
    srv, port = B.serve(app, qjson, 'bio', tag)
    br = getattr(pw, eng).launch()
    kw = dict(viewport={'width': 1440, 'height': 950}, device_scale_factor=1)
    if touch:
        kw.update(has_touch=True)
    ctx = br.new_context(**kw)
    ctx.add_init_script(B.INIT.replace('__SUBJ__', 'bio'))
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:%d/app.html' % port, wait_until='load')
    pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=90000)
    pg.wait_for_timeout(2500)
    pg.evaluate(B.JS_HELP)
    pg.evaluate(APPJS)
    cdp = ctx.new_cdp_session(pg) if (touch and eng == 'chromium') else None
    return srv, br, pg, cdp, errs


def press(pg, cdp, p):
    if not p:
        return False
    if cdp:
        tp = {'x': p['x'], 'y': p['y'], 'radiusX': 22, 'radiusY': 22, 'id': 1}
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [tp]}); pg.wait_for_timeout(60)
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    else:
        pg.mouse.click(p['x'], p['y'])
    pg.wait_for_timeout(900)
    return True


def app_flow(pw, eng, app, qjson, tag, touch):
    srv, br, pg, cdp, errs = launch(pw, eng, app, qjson, tag, touch)
    out = {}
    try:
        for u in TITLES:
            pg.evaluate("()=>{try{closeView()}catch(e){}}"); pg.wait_for_timeout(200)
            pg.evaluate('u=>__h.show(u)', u); pg.wait_for_timeout(300)
            it = pg.evaluate('u=>__h.item(u)', u)
            d = {'줄': it, '누름': press(pg, cdp, it)}
            d['제목'] = pg.evaluate('()=>__h.title()')
            s = pg.evaluate('()=>__h.sum()')
            d['정답·해설'] = press(pg, cdp, s)
            d['비고'] = pg.evaluate('()=>__h.note()')
            out[u] = d
        pg.evaluate("()=>{try{closeView()}catch(e){}}")
        out['err'] = errs + (pg.evaluate('()=>(window.__err||[]).slice(0,5)') or [])
    finally:
        br.close(); srv.shutdown()
    return out


def main():
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    raw = subprocess.run(['git', '-C', B.SPDROOT, 'show', BASE_REV + ':bio/문항.json'], capture_output=True).stdout
    T('땅값 — 바탕 = studyplandata %s bio/문항.json(add1 인도판 · md5 0fd627d1)' % BASE_REV, hashlib.md5(raw).hexdigest() == BASE_MD5, hashlib.md5(raw).hexdigest())
    open(BASEQ, 'wb').write(raw); open(NEWQ, 'wb').write(raw)
    env = dict(os.environ, PYTHONIOENCODING='utf-8', OCRFIX_QJ=NEWQ, OCRFIX_TABLE=B.FIX)
    r1 = subprocess.run([sys.executable, os.path.join(HERE, '_ocrfix_bio.py'), 'write'], capture_output=True, env=env).stdout.decode('utf-8', 'replace')
    b1 = open(NEWQ, 'rb').read()
    r2 = subprocess.run([sys.executable, os.path.join(HERE, '_ocrfix_bio.py'), 'write'], capture_output=True, env=env).stdout.decode('utf-8', 'replace')
    b2 = open(NEWQ, 'rb').read()
    now = open(B.QJ, 'rb').read()
    D0 = json.loads(raw.decode('utf-8')); D1 = json.loads(b1.decode('utf-8'))
    # ── 1 데이터 ──
    f0, f1 = sum(fwcount(r) for r in D0), sum(fwcount(r) for r in D1)
    by0 = collections.Counter(); by1 = collections.Counter()
    for r in D0:
        for k, v in r.items():
            by0[k] += fwcount(v)
    for r in D1:
        for k, v in r.items():
            by1[k] += fwcount(v)
    T('B-1 바꿈표 글자(13) 모든 칸 0 — 행의 모든 글(보기·참고 안까지)', f1 == 0, {'새': f1, '칸별(새)': {k: v for k, v in by1.items() if v}})
    T('B-1 헛잣대 — 바탕 320(비고 174 · 교재문장 146)', f0 == 320 and by0.get('비고') == 174 and by0.get('교재문장') == 146, {'바탕': f0, '칸별': {k: v for k, v in by0.items() if v}})
    src = lambda D: sum(1 for r in D if '출처 ［' in (r.get('비고') or ''))
    T('B-1 비고 「출처 ［」 0 · 반각 「출처 [」 = 83 + 259', src(D1) == 0 and sum(1 for r in D1 if '출처 [' in (r.get('비고') or '')) == 342, {'전각': src(D1), '반각': sum(1 for r in D1 if '출처 [' in (r.get('비고') or ''))})
    T('B-1 헛잣대 — 바탕 비고 「출처 ［」 83', src(D0) == 83, src(D0))
    viol, par = [], []
    for a, b in zip(D0, D1):
        if a['uid'] != b['uid'] or list(a.keys()) != list(b.keys()):
            viol.append((a['uid'], '행·열')); continue
        for k in a:
            if k in ('교재문장', '비고'):
                if b[k] != (a[k].translate(FWT) if isinstance(a[k], str) else a[k]):
                    viol.append((a['uid'], k))
                if isinstance(b[k], str) and any(b[k].count(x) != b[k].count(y) for x, y in (('(', ')'), ('[', ']'), ('{', '}'))) \
                        and all(a[k].count(x) + a[k].count(fx) == a[k].count(y) + a[k].count(fy) for x, y, fx, fy in (('(', ')', '（', '）'), ('[', ']', '［', '］'), ('{', '}', '｛', '｝'))):
                    par.append('%s:%s' % (a['uid'], k))
            elif a[k] != b[k]:
                viol.append((a['uid'], k))
    T('B-1 고친 칸 밖 바이트 같음(교재문장·비고 = 반각 바꿈만) · 행 746 · 행·열 차례 · 괄호 짝이 새로 틀어진 칸 0', not viol and not par and len(D1) == 746, {'어긋남': viol[:8], '새로 틀어짐': par, '행': len(D1)})
    ch = sum(1 for a, b in zip(D0, D1) for k in ('교재문장', '비고') if a.get(k) != b.get(k))
    N('B-1 바뀐 칸 = 교재문장 %d · 비고 %d(글자 %d)' % (sum(1 for a, b in zip(D0, D1) if a.get('교재문장') != b.get('교재문장')), sum(1 for a, b in zip(D0, D1) if a.get('비고') != b.get('비고')), f0 - f1), ch)
    T('B-1 쓰기 두 번 = 같은 바이트(멱등) · 왕복 무변 · 검산 OK · 두 번째 「바뀐 칸 0」', b1 == b2 and 'OK  json 왕복 무변' in r1 and '검산 OK' in r1 and '바뀐 칸 0' in r2,
      {'1회': [x for x in r1.splitlines() if x.startswith(('①', '②', '   모든 칸', '옛 md5'))][:4], '2회': [x for x in r2.splitlines() if '바뀐 칸' in x][:1]})
    T('B-1 인도본(studyplandata 로컬 bio/문항.json) = 재생성(바탕 + 스크립트) — 인도 전이면 로컬 = 바탕', now == b1 or now == raw,
      {'로컬': hashlib.md5(now).hexdigest()[:8], '재생성': hashlib.md5(b1).hexdigest()[:8], '바탕': hashlib.md5(raw).hexdigest()[:8]})
    # ── 2 앱 ──
    app = io.open(B.SRC, encoding='utf-8', newline='').read()
    with sync_playwright() as pw:
        A = {'Chromium 마우스': app_flow(pw, 'chromium', app, NEWQ, 'a2n_m', False), 'Chromium 손가락': app_flow(pw, 'chromium', app, NEWQ, 'a2n_t', True),
             'WebKit 마우스': app_flow(pw, 'webkit', app, NEWQ, 'a2n_w', False),
             '바탕 Chromium': app_flow(pw, 'chromium', app, BASEQ, 'a2b_m', False), '바탕 WebKit': app_flow(pw, 'webkit', app, BASEQ, 'a2b_w', False)}

    def ok_title(a, u):
        t = ((a.get(u) or {}).get('제목') or {}).get('t') or ''
        return TITLES[u] in t
    for k in ('Chromium 마우스', 'Chromium 손가락', 'WebKit 마우스'):
        a = A[k]
        notes = {u: ((a.get(u) or {}).get('비고') or {}) for u in TITLES}
        T('B-2 앱 [%s] — 목록 줄 누름 → 문제 창 제목 = 「타기출 · 2014년 서울시」「타기출 · 학력평가」「타기출 · 의대편입」 · 「정답·해설」 누름 → .cnote 보임 · 전각 0' % k,
          all(ok_title(a, u) for u in TITLES) and all(n.get('vis') and not any(c in (n.get('t') or '') for c in FWS) for n in notes.values()) and not a.get('err'),
          {u: [((a.get(u) or {}).get('제목') or {}).get('t'), (notes[u].get('t') or '')[:40], (a.get(u) or {}).get('줄', {}).get('hit') if (a.get(u) or {}).get('줄') else None] for u in TITLES} | {'err': a.get('err')})
    for k in ('바탕 Chromium', '바탕 WebKit'):
        b = A[k]
        T('B-2 헛잣대 %s — 바탕 데이터: 제목 「타기출 · SYNAPSE p…」 · .cnote 에 전각' % k,
          all('SYNAPSE p' in (((b.get(u) or {}).get('제목') or {}).get('t') or '') for u in TITLES) and any(any(c in ((((b.get(u) or {}).get('비고') or {}).get('t')) or '') for c in FWS) for u in TITLES),
          {u: [((b.get(u) or {}).get('제목') or {}).get('t'), ((((b.get(u) or {}).get('비고') or {}).get('t')) or '')[:40]] for u in TITLES})
    # ── 기록 ──
    lines = ['', '# ─── add2(9/28 · _task_jagwa_bio_ocrfix_add2) — %s ───' % time.strftime('%Y-%m-%d %H:%M'),
             '바탕 = studyplandata %s bio/문항.json(md5 %s) · 새 = 바탕 + _ocrfix_bio.py(md5 %s) · 앱 genie 작업트리 jagwa/index.html md5(LF) %s'
             % (BASE_REV, hashlib.md5(raw).hexdigest()[:8], hashlib.md5(b1).hexdigest()[:8], hashlib.md5(open(B.SRC, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:8]), '']
    for s, n, d in RES:
        dd = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)
        lines.append('%s | %s | %s' % (s, n, dd[:900]))
    nf = sum(1 for x in RES if x[0] == 'FAIL')
    lines += ['', 'add2 합계  PASS %d · FAIL %d · NOTE %d  (%.0f초)' % (sum(1 for x in RES if x[0] == 'PASS'), nf, sum(1 for x in RES if x[0] == 'NOTE'), time.time() - t0)]
    txt = '\n'.join(lines) + '\n'
    old = '' if ARG('--out') else (io.open(OUTF, encoding='utf-8').read() if os.path.exists(OUTF) else '')
    out = (old.rstrip('\n') + '\n' + txt) if old else txt.lstrip('\n')
    for _ in range(3):
        io.open(OUTF, 'w', encoding='utf-8', newline='\n').write(out); time.sleep(0.5)
        if io.open(OUTF, encoding='utf-8').read() == out:
            break
    print(lines[-1])
    return nf


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
