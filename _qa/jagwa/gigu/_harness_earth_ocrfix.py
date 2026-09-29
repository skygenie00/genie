# -*- coding: utf-8 -*-
r"""_task_jagwa_earth_ocrfix §H 관문 + _task_jagwa_earth_jeongo(+add1) §D·§F 관문 — 한 하네스

  바탕 둘은 studyplandata 커밋에 못 박는다(작업트리가 인도본으로 바뀌어도 헛잣대가 선다)
    BASE_OCR = 182e1f37:earth/문항.json(ocrfix 앞) — H 묶음(ocrfix 9/24)의 헛잣대
    BASE_JG  = 352fc227:earth/문항.json(ocrfix 인도판 = jeongo 앞) — J(본판)·F(add1) 묶음의 헛잣대
  새 값 = BASE_JG 사본에 _ocrfix_earth.py write 를 두 번(멱등) — 인도본(studyplandata 작업트리)과 바이트가 같아야 한다
  앱 = genie 작업트리 jagwa/index.html(코드 무접촉) · 로컬 띄움 — GitHub 요청을 로컬 studyplandata 로 돌리고 earth/문항.json 만 사본으로 가로챈다
  누름 = 진짜 포인터(PC page.mouse · 손가락 CDP 터치 반지름 22 · el.click() 안 씀) · 보임 = display ≠ none 이고 높이 > 0
  〈보기〉 O/X 보임 = 줄마다 O 단추를 누르고 「정답 · 해설」을 펼치면 앱이 정답 O 줄 = right(청록) · 정답 X 줄 = wrong(빨강)으로 칠한다

쓰기 : python _harness_earth_ocrfix.py        결과 = _harness_earth_jeongo_result.txt(9/24 결과 _harness_earth_ocrfix_result.txt 는 그대로 둔다)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import collections, hashlib, http.server, importlib.util, io, json, os, random, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
GENIE = _roots.genie()
SPDROOT = _roots.spd()
SRC = os.path.join(GENIE, 'jagwa', 'index.html')
QJ = os.path.join(SPDROOT, 'earth', '문항.json')
FIX = os.path.join(HERE, '_ocrfix', 'ocrfix_earth.json')
WORK = os.path.join(tempfile.gettempdir(), 'h_ocrfix'); os.makedirs(WORK, exist_ok=True)
NEWQ = os.path.join(WORK, '문항_new.json')
FIXED = ['G48-03', 'G36-02', 'G43-01', 'G40-09', 'C3-066']
_spec = importlib.util.spec_from_file_location('hes', os.path.join(HERE, '_harness_earth_shell.py'))
_hes = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_hes)
STUB = _hes.STUB
RES = []


def T(name, ok, detail=''):
    RES.append(('PASS' if ok else 'FAIL', name, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('%s | %s | %s' % ('PASS' if ok else 'FAIL', name, d[:300]), flush=True)


def N(name, detail=''):
    RES.append(('NOTE', name, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('NOTE | %s | %s' % (name, d[:300]), flush=True)


INIT = r"""
(()=>{
  try{localStorage.setItem('subj','earth')}catch(e){}
  try{localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}))}catch(e){}
  window.__err=[];
  window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+(e.lineno||''))});
  window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
  const nf=window.fetch.bind(window);
  window.fetch=async function(url,opt){
    opt=opt||{};const u=String(url);
    const m=/api\.github\.com\/repos\/([^\/]+\/[^\/]+)\/contents\/([^?]+)/.exec(u);
    if(!m){ if(/^https?:/i.test(u)&&u.indexOf(location.origin)!==0)
              return {ok:false,status:599,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
            return nf(url,opt) }
    const path=decodeURIComponent(m[2]);
    if((opt.method||'GET')==='PUT')return {ok:true,status:200,json:async()=>({content:{sha:'x'}}),text:async()=>''};
    const r=await nf('/data/'+encodeURI(path),{cache:'no-store'});
    if(!r.ok)return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
    const acc=(opt.headers||{}).Accept||'';
    if(acc.indexOf('raw')>=0)return r;
    return {ok:true,status:200,json:async()=>({sha:r.headers.get('X-Sha')||'sha'}),text:async()=>JSON.stringify({sha:r.headers.get('X-Sha')||'sha'})};
  };
})();
"""


def serve(qjson, outdir, app=None):   # app = 앱 파일(없으면 genie 작업트리 · ★ add2 K-3 이 바탕 앱 f497f05·d27c43a 를 넘긴다)
    os.makedirs(outdir, exist_ok=True)
    src = io.open(app or SRC, encoding='utf-8').read()
    html = src.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js',
                       STUB.replace('__SUBJ__', 'earth') + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    io.open(os.path.join(outdir, 'app.html'), 'w', encoding='utf-8', newline='').write(html)
    spd = os.path.join(SPDROOT, 'earth')

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=outdir, **k)

        def log_message(self, *a, **k):
            pass

        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            if p.startswith('/data/'):
                rel = p[6:]
                if not rel.startswith('earth/'):
                    self.send_response(404); self.end_headers(); return
                f = qjson if rel == 'earth/문항.json' else os.path.join(spd, rel[6:].replace('/', os.sep))
                if not os.path.isfile(f):
                    self.send_response(404); self.end_headers(); return
                b = open(f, 'rb').read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', str(len(b)))
                self.send_header('X-Sha', hashlib.sha1(b).hexdigest())
                self.end_headers(); self.wfile.write(b); return
            return super().do_GET()

    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


PROBE = r"""async (uids)=>{
  const wait=ms=>new Promise(r=>setTimeout(r,ms));
  const tx=e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'';
  const out={};
  for(const u of uids){
    const r=DATA.find(x=>x[F.CODE]===u);if(!r){out[u]={miss:true};continue}
    const no=r[F.NO];
    try{FL.q=u;FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';FL.past=isC(r)?'p':'';draw();}catch(e){}   /* 지학 목록 = 기출 / 확인문제(FL.past='p') 둘 중 하나 */
    await wait(250);
    const it=[...document.querySelectorAll('#list .item')].find(x=>x.dataset.uid===u||tx(x.querySelector('.num'))===u);
    const prev=it?tx(it.querySelector('.prev')):null;
    try{await openView(no);}catch(e){}
    await wait(700);
    const ch=[...document.querySelectorAll('#card .choices button')].map(b=>tx(b).replace(/^[①②③④⑤]\s*/,''));
    const bg={};document.querySelectorAll('#card .bogi .row').forEach(el=>{const k=el.dataset.k;const t=el.querySelector('.t');
      if(!t){bg[k]=null;return}const c=t.cloneNode(true);c.querySelectorAll('.tfx,.bexp').forEach(x=>x.remove());bg[k]=tx(c);});
    out[u]={prev,ch,bg,tf:(typeof TFIX!=='undefined'&&TFIX[u])?Object.keys(TFIX[u]):[]};
    try{closeView()}catch(e){}
    await wait(150);
  }
  try{FL.q='';FL.past='';draw()}catch(e){}
  return out}"""


def probe(qjson, tag, uids):
    from playwright.sync_api import sync_playwright
    srv, port = serve(qjson, os.path.join(WORK, 'srv_' + tag))
    R = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        ctx = br.new_context(viewport={'width': 1440, 'height': 950})
        ctx.add_init_script(INIT)
        pg = ctx.new_page()
        pg.goto('http://127.0.0.1:%d/app.html' % port, wait_until='load')
        pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>600', timeout=90000)
        pg.wait_for_timeout(2500)
        R['n'] = pg.evaluate('DATA.length')
        R['items'] = pg.evaluate(PROBE, uids)
        R['err'] = pg.evaluate('(window.__err||[]).slice(0,8)')
        br.close()
    srv.shutdown()
    return R


def _main_ocrfix_0924():   # 9/24 ocrfix 판 main — 기록으로 둔다(부르지 않음 · 아래 main 이 H 묶음을 바탕 커밋에 못 박아 다시 잰다)
    t0 = time.time()
    raw = open(QJ, 'rb').read()
    D0 = json.loads(raw.decode('utf-8'))
    FX = json.load(open(FIX, encoding='utf-8'))
    # ① 적용 스크립트 — 사본에 두 번(멱등) · 왕복 무변
    shutil.copy(QJ, NEWQ)
    env = dict(os.environ, PYTHONIOENCODING='utf-8', OCRFIX_QJ=NEWQ, OCRFIX_TABLE=FIX)
    r1 = subprocess.run([sys.executable, os.path.join(HERE, '_ocrfix_earth.py'), 'write'], capture_output=True, env=env).stdout.decode('utf-8', 'replace')
    b1 = open(NEWQ, 'rb').read()
    r2 = subprocess.run([sys.executable, os.path.join(HERE, '_ocrfix_earth.py'), 'write'], capture_output=True, env=env).stdout.decode('utf-8', 'replace')
    b2 = open(NEWQ, 'rb').read()
    T('H-5 적용 두 번 = 같은 결과(멱등) · 왕복 무변 · 검산 OK', b1 == b2 and 'OK  json 왕복 무변' in r1 and '검산 OK' in r1 and '바뀐 칸 0' in r2,
      {'1회': [x for x in r1.splitlines() if '칸' in x or 'md5' in x][:3], '2회': [x for x in r2.splitlines() if '칸' in x][:2]})
    D1 = json.loads(b1.decode('utf-8'))
    # ② 대상 census(고치기 전 · 뒤)
    census = lambda P: subprocess.run([sys.executable, os.path.join(HERE, '_ocrfix', 'ocr_census.py'), P], capture_output=True,
                                      env=dict(os.environ, PYTHONIOENCODING='utf-8')).stdout.decode('utf-8', 'replace').splitlines()
    c0, c1 = census(QJ), census(NEWQ)
    N('H-1 대상 census — 고치기 전', c0[:2])
    N('H-1 대상 census — 고친 뒤(남은 것 · 까닭은 수행 결과)', c1[:2])
    T('H-1 고친 문항 수 = 고침표 문항 수 · 고침표 uid 는 모두 대상 안', len(FX) > 0 and all(u in {r['uid'] for r in D0} for u in FX), {'고침표': len(FX)})
    # ③ D-1 · D-2
    mr = subprocess.run([sys.executable, os.path.join(HERE, '_ocrfix', 'ocr_check.py'), NEWQ], capture_output=True,
                        env=dict(os.environ, PYTHONIOENCODING='utf-8')).stdout.decode('utf-8', 'replace')
    try:
        CK = json.loads(mr.strip().splitlines()[-1])
    except Exception:
        CK = {'err': mr[-400:]}
    # 어긋남은 「원본 그림을 다시 봐도 판독이 맞은」 정오 의심(ocrfix_lists.json) 과 **똑같아야** 한다 — 새 어긋남 하나라도 생기면 FAIL
    LS = json.load(open(os.path.join(HERE, '_ocrfix', 'ocrfix_lists.json'), encoding='utf-8'))
    sus = sorted(x['uid'] for x in LS['정오_의심'])
    bad1 = sorted(x[0] for x in CK.get('d1_bad') or [])
    T('H-2 D-1 정오 대조 — 정답 선택지가 조합형이고 정오가 다 찬 %s 문항 · 어긋남 = 정오 의심 목록(원본 재확인 · 정오는 판 1·2 가 깨진 OCR 글자에서 뽑은 값) 그대로' % CK.get('d1_n'),
      CK.get('d1_n', 0) > 0 and bad1 == sus, {'n': CK.get('d1_n'), '어긋남': len(bad1), '목록 밖 어긋남': sorted(set(bad1) - set(sus)), '목록에만': sorted(set(sus) - set(bad1))})
    T('H-3 D-2 CHOICE_LETTERS 일치(답 없음 표시 뺌)', CK.get('d2_n', 0) > 0 and not CK.get('d2_bad'), {'n': CK.get('d2_n'), 'bad': CK.get('d2_bad')})
    T('D-3 조합형 다섯 서로 다름 · 빈 선택지 = 원본 선택지가 넷인 문항뿐(그림 선택지 뺌)', not CK.get('d3_dup') and sorted(CK.get('d3_empty') or []) == sorted(LS['선택지_넷']),
      {'dup': CK.get('d3_dup'), 'empty': CK.get('d3_empty'), '선택지 넷': LS['선택지_넷']})
    # 옛 값에서는 같은 잣대가 어긋나야 잣대다(헛잣대)
    mr0 = subprocess.run([sys.executable, os.path.join(HERE, '_ocrfix', 'ocr_check.py'), QJ], capture_output=True,
                         env=dict(os.environ, PYTHONIOENCODING='utf-8')).stdout.decode('utf-8', 'replace')
    try:
        CK0 = json.loads(mr0.strip().splitlines()[-1])
    except Exception:
        CK0 = {}
    T('H-2·3 헛잣대 — 옛 문항.json: D-1 이 잴 수 있는 문항이 거의 없고 D-2 가 거의 다 어긋난다', CK0.get('d1_n', 999) < 20 and len(CK0.get('d2_bad') or []) >= 40,
      {'옛 d1_n': CK0.get('d1_n'), '옛 d2 어긋남': len(CK0.get('d2_bad') or []), '옛 빈 선택지': len(CK0.get('d3_empty') or [])})
    # ④ 앱으로 확인
    rnd = random.Random(20260924)
    pool = sorted(u for u in FX if u not in FIXED)
    uids = FIXED + rnd.sample(pool, min(20, len(pool)))
    B = probe(QJ, 'old', uids)
    A = probe(NEWQ, 'new', uids)
    by1 = {r['uid']: r for r in D1}
    good, bad, base_bad = 0, [], 0
    for u in uids:
        r = by1.get(u); a = A['items'].get(u) or {}; b = B['items'].get(u) or {}
        tf = set(a.get('tf') or [])
        want_ch = [c for i, c in enumerate(r['선택지']) if 'c%d' % (i + 1) not in tf]
        got_ch = [c for i, c in enumerate(a.get('ch') or []) if 'c%d' % (i + 1) not in tf]
        if not any(str(c or '').strip() for c in r['선택지']):
            ok_ch = not (a.get('ch') or [])          # 그림 선택지(다섯 다 빈칸) — 앱은 선택지 칸을 안 그린다
        else:
            ok_ch = got_ch == want_ch and len(a.get('ch') or []) == 5
        want_bg = {x['키']: x['내용'] for x in (r.get('보기') or []) if 'b' + x['키'] not in tf and x.get('내용')}
        ok_bg = all((a.get('bg') or {}).get(k) == v for k, v in want_bg.items())
        stem = str(r['문항']).split(' ⏎ ')[0]
        ok_pv = ('q' in tf) or (a.get('prev') is not None and stem[:20] in (a.get('prev') or '').replace('…', ''))
        if ok_ch and ok_bg and ok_pv:
            good += 1
        else:
            bad.append({'u': u, 'ch': [got_ch, want_ch] if not ok_ch else None, 'bg': None if ok_bg else [a.get('bg'), want_bg], 'pv': None if ok_pv else [a.get('prev'), stem[:30]]})
        fx = FX.get(u, {})
        bb = [c for i, c in enumerate(b.get('ch') or []) if 'c%d' % (i + 1) not in tf]
        if ('선택지' in fx and bb != want_ch) or ('보기' in fx and any((b.get('bg') or {}).get(k) != v for k, v in want_bg.items())):
            base_bad += 1
    T('H-4 앱 — 표본 %d(무작위 20 + 다섯) 첫 화면 줄 미리보기 · 문제 창 선택지 다섯 · 〈보기〉 줄 = 새 값(손값 없는 칸)' % len(uids), not bad and A['n'] == len(D1),
      {'good': good, 'bad': bad[:4], 'n': A['n']})
    T('H-4 헛잣대 — 옛 문항.json 으로는 고친 칸이 어긋난다(표본 대부분)', base_bad >= max(1, len(uids) // 2), {'어긋남': base_bad, '표본': len(uids)})
    T('H-4 페이지 오류 0', not A['err'], A['err'])
    lines = ['# _harness_earth_ocrfix — %s' % time.strftime('%Y-%m-%d %H:%M'),
             '옛 문항.json md5 %s · 새(사본) md5 %s · 앱 genie 작업트리 jagwa/index.html md5(LF) %s' % (
                 hashlib.md5(raw).hexdigest(), hashlib.md5(b1).hexdigest(), hashlib.md5(open(SRC, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()), '']
    for s, n, d in RES:
        dd = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)
        lines.append('%s | %s | %s' % (s, n, dd[:900]))
    nf = sum(1 for x in RES if x[0] == 'FAIL')
    lines += ['', '합계  PASS %d · FAIL %d · NOTE %d  (%.0f초)' % (sum(1 for x in RES if x[0] == 'PASS'), nf, sum(1 for x in RES if x[0] == 'NOTE'), time.time() - t0)]
    txt = '\n'.join(lines) + '\n'
    f = os.path.join(HERE, '_harness_earth_ocrfix_result.txt')
    for _ in range(3):
        io.open(f, 'w', encoding='utf-8', newline='\n').write(txt); time.sleep(0.5)
        if io.open(f, encoding='utf-8').read() == txt:
            break
    print(lines[-1])
    return nf


# ════════════ jeongo(+add1) — 2026-09-27 ════════════
BASE_JG_REV, BASE_OCR_REV = '352fc227', '182e1f37'
LJ = os.path.join(HERE, '_ocrfix', 'ocrfix_lists.json')
FWCH = '（）、，：；［］｛｝＜＞！'
FWT = str.maketrans({'（': '(', '）': ')', '、': ',', '，': ',', '：': ':', '；': ';', '［': '[', '］': ']', '｛': '{', '｝': '}', '＜': '<', '＞': '>', '！': '!'})
JQ = ['G45-09', 'G41-02', 'C5-095', 'C1-024', 'G36-06', 'G36-02', 'G34-02', 'G37-02']   # 앱 표본(본판 §D-7 셋 + add1 §F-8)


def blob(rev, path):
    return subprocess.run(['git', '-C', SPDROOT, 'show', '%s:%s' % (rev, path)], capture_output=True).stdout


def apply(src_bytes, tag, lists=None, times=2):
    """src 사본에 _ocrfix_earth.py write 를 times 번 — (바이트들, 출력들)"""
    p = os.path.join(WORK, '문항_%s.json' % tag)
    open(p, 'wb').write(src_bytes)
    env = dict(os.environ, PYTHONIOENCODING='utf-8', OCRFIX_QJ=p, OCRFIX_TABLE=FIX, OCRFIX_LISTS=lists or LJ)
    outs, bs = [], []
    for _ in range(times):
        outs.append(subprocess.run([sys.executable, os.path.join(HERE, '_ocrfix_earth.py'), 'write'], capture_output=True, env=env).stdout.decode('utf-8', 'replace'))
        bs.append(open(p, 'rb').read())
    return p, bs, outs


def check(path):
    mr = subprocess.run([sys.executable, os.path.join(HERE, '_ocrfix', 'ocr_check.py'), path], capture_output=True,
                        env=dict(os.environ, PYTHONIOENCODING='utf-8')).stdout.decode('utf-8', 'replace')
    try:
        return json.loads(mr.strip().splitlines()[-1])
    except Exception:
        return {'err': mr[-400:]}


def cells(r):
    """글 칸(칸 이름, 값) — 문항 · 선택지 · 보기 내용 · 해설 · 해설2 · 참고"""
    yield '문항', r.get('문항')
    for i, c in enumerate(r.get('선택지') or []):
        yield 'c%d' % (i + 1), c
    for b in (r.get('보기') or []):
        yield 'b' + str(b.get('키')), b.get('내용')
    for k in ('해설', '해설2', '참고'):
        if k in r:
            yield k, r.get(k)


def oxset(r, v='O'):
    return {b['키'] for b in (r.get('보기') or []) if b.get('정오') == v}


def bogi_lines(r):
    return len(set(re.findall(r'(?:^|⏎ )\s*([ㄱ-ㅅ])\s*[.．]', str(r.get('문항') or ''))))


OPEN_JS = r"""async (u)=>{ const wait=ms=>new Promise(r=>setTimeout(r,ms));
  const r=DATA.find(x=>x[F.CODE]===u); if(!r) return {miss:true};
  try{closeView()}catch(e){}
  try{FL.q=u;FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';FL.past=isC(r)?'p':'';draw();}catch(e){}
  await wait(250); try{await openView(r[F.NO]);}catch(e){} await wait(700);
  const d=document.querySelector('#cDet'); if(d&&d.open){d.open=false;try{CARD.open=false;markWrong();markAns()}catch(e){}} await wait(150);
  return {ok:!!document.querySelector('#card .q'), keys:[...document.querySelectorAll('#card .bogi .row')].map(e=>e.dataset.k)}; }"""
RECT_JS = r"""(sel)=>{ const vis=e=>{if(!e)return false;const s=getComputedStyle(e),r=e.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&r.height>0};
  const e=sel.split('||').map(s=>document.querySelector(s.trim())).find(vis); if(!e) return null; e.scrollIntoView({block:'center'});
  const r=e.getBoundingClientRect(); const cx=r.left+r.width/2, cy=r.top+r.height/2;
  /* 펜 모드면 필기 덮개(#qink)가 맨 위다 — 앱의 덮개 뚫기(inkPierce)가 밑의 단추로 넘긴다 · 과녁은 덮개 밑 첫 요소로 잰다 */
  const at=document.elementsFromPoint(cx,cy).filter(x=>!x.closest('#qink'))[0];
  return {x:cx,y:cy,w:r.width,h:r.height,hit:!!(at&&(at===e||e.contains(at))),sel:e.id||e.tagName}; }"""
STATE_JS = r"""()=>{ const vis=e=>{if(!e)return false;const s=getComputedStyle(e),r=e.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&r.height>0};
  const rows=[...document.querySelectorAll('#card .bogi .row')].map(el=>{const t=el.querySelector('.t');
    return {k:el.dataset.k,ans:el.dataset.ans,right:el.classList.contains('right'),wrong:el.classList.contains('wrong'),color:t?getComputedStyle(t).color:null,vis:vis(el)}});
  const q=document.querySelector('#card .q');
  const ch=[...document.querySelectorAll('#card .choices button')].map(b=>({t:b.textContent.replace(/\s+/g,' ').trim(),h:Math.round(b.getBoundingClientRect().height),vis:vis(b)}));
  return {rows, q:q?q.textContent.replace(/\s+/g,' ').trim():null, qvis:vis(q), ch, open:!!(document.querySelector('#cDet')||{}).open, err:(window.__err||[]).slice(0,4)}; }"""


def probe_jeongo(qjson, tag, touch=False, tool=None, app=None):
    """tool='view' — 손가락 관문은 「보기」 도구에서 잰다: 펜 도구에선 손가락 톡이 필기 덮개(#qink)에 막히는 앱 결함(D2-1)이 있고
       그것은 _task_jagwa_penfinger_add1 §A 몫이다(이 판은 데이터만 · 앱 코드 무접촉)
       ★ add2 K-3 — penfinger_add1(d27c43a)이 그 결함을 고쳤다 → 펜 도구 그대로(tool=None · 앱 기본 = pen) 손가락으로도 잰다 · app = 바탕 앱 파일"""
    from playwright.sync_api import sync_playwright
    srv, port = serve(qjson, os.path.join(WORK, 'srv_' + tag), app)
    R = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        ctx = br.new_context(viewport={'width': 820, 'height': 1180} if touch else {'width': 1440, 'height': 950}, has_touch=touch)
        ctx.add_init_script(INIT)
        pg = ctx.new_page()
        cdp = ctx.new_cdp_session(pg) if touch else None

        def press(rc):
            if not rc:
                return False
            if touch:
                cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': rc['x'], 'y': rc['y'], 'radiusX': 22, 'radiusY': 22}]})
                cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
            else:
                pg.mouse.click(rc['x'], rc['y'])
            pg.wait_for_timeout(220)
            return True
        pg.goto('http://127.0.0.1:%d/app.html' % port, wait_until='load')
        pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>600', timeout=90000)
        pg.wait_for_timeout(2500)
        if tool:
            pg.evaluate("t=>{try{setTool(t)}catch(e){window.__terr=String(e)}}", tool)
            pg.wait_for_timeout(200)
        R['_tool'] = pg.evaluate("()=>TOOL&&TOOL.mode")
        for u in JQ:
            o = pg.evaluate(OPEN_JS, u)
            hits = []
            for k in (o.get('keys') or []):
                rc = pg.evaluate(RECT_JS, '#card .bogi .row[data-k="%s"] .ox button.O' % k)
                hits.append([k, bool(rc and rc['hit'])])
                press(rc)
            sm = pg.evaluate(RECT_JS, '#cDetBtn || #cDet summary')   # 떠 있는 문제 창은 summary 를 숨기고 「정답·해설 ▸」(#cDetBtn)을 세운다
            press(sm)
            st = pg.evaluate(STATE_JS)
            st['hits'] = hits; st['sumHit'] = bool(sm and sm['hit'])
            R[u] = st
        br.close()
    srv.shutdown()
    return R


def main():
    t0 = time.time()
    RAW_JG, RAW_OCR = blob(BASE_JG_REV, 'earth/문항.json'), blob(BASE_OCR_REV, 'earth/문항.json')
    DJG, DOCR = json.loads(RAW_JG.decode('utf-8')), json.loads(RAW_OCR.decode('utf-8'))
    FX = json.load(open(FIX, encoding='utf-8'))
    LS = json.load(open(LJ, encoding='utf-8'))
    SUS = {x['uid'] for x in LS['정오_의심']}
    PART = LS.get('부분정답') or {}
    DROP = LS.get('보기_걷기') or {}
    N('바탕', {'BASE_JG': [BASE_JG_REV, hashlib.md5(RAW_JG).hexdigest()[:8], len(DJG)], 'BASE_OCR': [BASE_OCR_REV, hashlib.md5(RAW_OCR).hexdigest()[:8], len(DOCR)],
              '고침표': len(FX), '보기_걷기': len(DROP), '부분정답': PART})
    # ── 적용(멱등 · 재생성 = 인도본 · ocrfix 앞 데이터에서도 같음)
    NEWQ, (b1, b2), (r1, r2) = apply(RAW_JG, 'jg')
    T('H-5 · J-6 · F-7 적용 두 번 = 같은 바이트(멱등) · 왕복 무변 · 검산 OK · 두 번째 「바뀐 칸 0」', b1 == b2 and 'OK  json 왕복 무변' in r1 and '검산 OK' in r1 and '바뀐 칸 0' in r2,
      {'1회': [x for x in r1.splitlines() if x[:1] in '①②③④' or 'md5' in x][:6], '2회': [x for x in r2.splitlines() if '바뀐 칸' in x][:2]})
    _, (bo,), _ = apply(RAW_OCR, 'ocr', times=1)
    T('J-6 되살아나지 않음 — ocrfix 앞 데이터(182e1f37)에 한 번 입혀도 같은 바이트(판 1·2 로 다시 만든 뒤 한 번 돌리는 길)', bo == b1, {'같음': bo == b1, 'md5': hashlib.md5(bo).hexdigest()[:8]})
    cur = open(QJ, 'rb').read()
    T('J-6 인도본(studyplandata earth/문항.json) = 재생성(BASE_JG + 스크립트)', cur == b1, {'인도본 md5': hashlib.md5(cur).hexdigest()[:8], '재생성 md5': hashlib.md5(b1).hexdigest()[:8], 'B': len(b1)})
    D1 = json.loads(b1.decode('utf-8'))
    BJ, BN = {r['uid']: r for r in DJG}, {r['uid']: r for r in D1}
    # ── H 묶음(ocrfix 9/24) — 바탕 = 182e1f37
    census = lambda P: subprocess.run([sys.executable, os.path.join(HERE, '_ocrfix', 'ocr_census.py'), P], capture_output=True,
                                      env=dict(os.environ, PYTHONIOENCODING='utf-8')).stdout.decode('utf-8', 'replace').splitlines()
    pocr = os.path.join(WORK, '문항_182e1f37.json'); open(pocr, 'wb').write(RAW_OCR)
    N('H-1 대상 census — ocrfix 앞', census(pocr)[:2])
    N('H-1 대상 census — 지금(남은 것 · 까닭은 수행 결과)', census(NEWQ)[:2])
    T('H-1 고침표 uid 는 모두 대상 안', len(FX) > 0 and all(u in BN for u in FX), {'고침표': len(FX)})
    pjg = os.path.join(WORK, '문항_jg_base.json'); open(pjg, 'wb').write(RAW_JG)
    CK, CKJ, CKO = check(NEWQ), check(pjg), check(pocr)
    T('H-3 · J-4 D-2 CHOICE_LETTERS 일치(답 없음 표시 뺌)', CK.get('d2_n', 0) > 0 and not CK.get('d2_bad'), {'n': CK.get('d2_n'), 'bad': CK.get('d2_bad')})
    T('D-3 · J-4 조합형 다섯 서로 다름 · 빈 선택지 = 원본 선택지가 넷인 문항뿐(그림 선택지 뺌)', not CK.get('d3_dup') and sorted(CK.get('d3_empty') or []) == sorted(LS['선택지_넷']),
      {'dup': CK.get('d3_dup'), 'empty': CK.get('d3_empty'), '선택지 넷': LS['선택지_넷']})
    T('H-2·3 헛잣대 — ocrfix 앞(182e1f37): D-1 이 잴 수 있는 문항이 거의 없고 D-2 가 거의 다 어긋난다', CKO.get('d1_n', 999) < 20 and len(CKO.get('d2_bad') or []) >= 40,
      {'d1_n': CKO.get('d1_n'), 'd2 어긋남': len(CKO.get('d2_bad') or [])})
    # ── J-1 D-1 어긋남 0
    bad1 = sorted(x[0] for x in CK.get('d1_bad') or [])
    badj = sorted(x[0] for x in CKJ.get('d1_bad') or [])
    T('J-1 D-1 어긋남 0 — 정답 선택지가 조합형이고 정오가 다 찬 %s 문항(부분정답은 해설 키와 맞댐)' % CK.get('d1_n'), CK.get('d1_n', 0) >= 152 and not bad1, {'n': CK.get('d1_n'), '어긋남': bad1})
    T('J-1-헛 헛잣대 — 바탕(352fc227) 어긋남 = 정오 의심 23 ∪ 부분정답(C1-024 는 겹침) = 25', set(badj) == SUS | set(PART) and len(badj) == 25, {'바탕 어긋남': len(badj), '목록 밖': sorted(set(badj) - SUS - set(PART))})
    # ── J-2 · F-2 뒤집힘 = 23 ∪ 부분정답
    flip, fill = [], []
    for u, a in BJ.items():
        b = BN[u]
        oa = {x['키']: x.get('정오') for x in (a.get('보기') or [])}
        ob = {x['키']: x.get('정오') for x in (b.get('보기') or [])}
        ks = [k for k in ob if k in oa]
        if any(oa[k] != ob[k] for k in ks):
            (flip if all(oa[k] in ('O', 'X') for k in ks) else fill).append(u)
    T('J-2 · F-2 뒤집힌 문항 = 정오 의심 23 ∪ 부분정답 · 목록 밖 0', set(flip) == SUS | set(PART), {'뒤집힘': len(flip), '목록 밖': sorted(set(flip) - SUS - set(PART)), '목록에만': sorted((SUS | set(PART)) - set(flip)), '새로 참': fill})
    # ── J-3 없는 보기 키 0
    extra_new = [u for u in DROP if len(BN[u].get('보기') or []) != bogi_lines(BN[u])]
    extra_base = [u for u in DROP if len(BJ[u].get('보기') or []) > bogi_lines(BJ[u])]
    allx = [r['uid'] for r in D1 if (r.get('보기') or []) and bogi_lines(r) and len(r['보기']) > bogi_lines(r)]
    T('J-3 없는 보기 키 0 — 12 문항 보기 수 = 원본 〈보기〉 줄 수 · 전수 키 > 줄 0', not extra_new and not allx, {'어긋남': extra_new, '전수': allx})
    T('J-3-헛 헛잣대 — 바탕 12 문항 키 > 줄', len(extra_base) == 12, {'바탕': len(extra_base)})
    # ── F-1 부분정답
    pok = {u: sorted(oxset(BN[u])) == sorted(PART[u]) for u in PART}
    T('F-1 부분정답 — C1-024 · G36-06 · G36-02 O 집합 = 해설 O 집합', all(pok.values()) and len(PART) == 3, {u: [''.join(sorted(oxset(BN[u]))), ''.join(PART[u])] for u in PART})
    T('F-1-헛 헛잣대 — 바탕 셋 다 어긋남', all(sorted(oxset(BJ[u])) != sorted(PART[u]) for u in PART), {u: ''.join(sorted(oxset(BJ[u]))) for u in PART})
    L0 = dict(LS); L0.pop('부분정답', None)
    lp = os.path.join(WORK, 'lists_no_part.json'); io.open(lp, 'w', encoding='utf-8').write(json.dumps(L0, ensure_ascii=False))
    _, (bv,), _ = apply(RAW_JG, 'nopart', lists=lp, times=1)
    V = {r['uid']: r for r in json.loads(bv.decode('utf-8'))}
    c024 = {x['키']: x['정오'] for x in V['C1-024']['보기']}
    T('F-1-헛 본판 규칙만(부분정답 목록 없이) 돌린 판 — C1-024 ㄱ = X(이 add1 이 없으면 틀린다)', c024.get('ㄱ') == 'X', {'C1-024': c024})
    # ── F-3 전각 · F-4 「。」 · F-5 선택지 해설
    def fwcount(D):
        n, par = 0, []
        for r in D:
            for k, t in cells(r):
                t = str(t or '')
                n += sum(t.count(c) for c in FWCH)
        return n
    def dots(D):
        return sum(str(t or '').count('。') for r in D for k, t in cells(r))
    def longch(D):
        out = []
        for r in D:
            ch = [str(c or '') for c in (r.get('선택지') or [])]
            if len(ch) != 5:
                continue
            for i, c in enumerate(ch):
                av = sum(len(x) for j, x in enumerate(ch) if j != i) / 4.0
                if len(c) > 80 and len(c) > 3 * av:
                    out.append('%s:%d' % (r['uid'], i + 1))
        return out
    newbad = []
    for u, a in BJ.items():
        cb = dict(cells(a)); cn = dict(cells(BN[u]))
        for k, t in cn.items():
            t = str(t or ''); s = str(cb.get(k) or '')
            was = all(s.count(p) + s.count(fp) == s.count(q) + s.count(fq) for p, q, fp, fq in (('(', ')', '（', '）'), ('[', ']', '［', '］'), ('{', '}', '｛', '｝')))
            now = all(t.count(p) == t.count(q) for p, q in (('(', ')'), ('[', ']'), ('{', '}')))
            if was and not now:
                newbad.append('%s:%s' % (u, k))
    fwb, fwn = fwcount(DJG), fwcount(D1)
    T('F-3 전각 문장부호 13 글자 0(모든 칸) · 괄호 짝이 새로 틀어진 칸 0', fwn == 0 and not newbad, {'새': fwn, '새로 틀어진 칸': newbad[:6]})
    T('F-3-헛 헛잣대 — 바탕 1,632 글자', fwb == 1632, {'바탕': fwb})
    T('F-4 「。」 0(모든 칸)', dots(D1) == 0, {'새': dots(D1)})
    T('F-4-헛 헛잣대 — 바탕 68', dots(DJG) == 68, {'바탕': dots(DJG)})
    lc_new, lc_base = longch(D1), longch(DJG)
    kept = {}
    for x in lc_base:
        u, i = x.split(':'); i = int(i)
        old, new = str(BJ[u]['선택지'][i - 1]), str(BN[u]['선택지'][i - 1])
        tail = old[len(new):] if old.startswith(new) else old
        nz = lambda s: re.sub(r'[\s⏎]+', '', str(s or '').translate(FWT))
        sol = nz(BJ[u].get('해설'))
        kept[x] = [len(new), nz(tail)[:12], bool(sol) and (nz(tail) in sol or nz(tail).replace(sol, '') == '')]   # C4-016 은 해설이 두 벌 붙어 있었다
    T('F-5 선택지에 붙은 해설 0(3배·80자 잣대) · 걷은 글은 바탕 해설 칸에 이미 있음(글을 잃지 않음)', not lc_new and len(kept) == 4 and all(v[2] for v in kept.values()), {'새': lc_new, '걷은 넷': kept})
    T('F-5-헛 헛잣대 — 바탕 넷(G32-07 · G37-02 · C3-021 · C4-016)', sorted(lc_base) == sorted(['G32-07:5', 'G37-02:5', 'C3-021:5', 'C4-016:5']), {'바탕': lc_base})
    # ── J-5 · F-6 다른 칸 무변 — 바뀐 칸은 모두 까닭이 있다
    why = collections.Counter(); odd = []
    FXN = {u: {k: (v.translate(FWT) if isinstance(v, str) else ([x.translate(FWT) if isinstance(x, str) else x for x in v] if isinstance(v, list) else ({kk: vv.translate(FWT) for kk, vv in v.items()} if isinstance(v, dict) else v))) for k, v in f.items()} for u, f in FX.items()}
    if len(D1) != len(DJG) or [r['uid'] for r in D1] != [r['uid'] for r in DJG]:
        odd.append('행 수·차례')
    for u, a in BJ.items():
        b = BN[u]; f = FXN.get(u, {})
        if list(a.keys()) != list(b.keys()):
            odd.append('%s 열 차례' % u); continue
        for k in a:
            if a[k] == b[k]:
                continue
            if k == '보기':
                A = [x for x in a[k] if x.get('키') not in (DROP.get(u) or [])]
                if len(A) != len(a[k]):
                    why['보기 줄 걷기'] += len(a[k]) - len(A)
                for x, y in zip(A, b[k]):
                    for kk in x:
                        if x[kk] == y.get(kk):
                            continue
                        if kk == '내용':
                            tv = (f.get('보기') or {}).get(x.get('키'))
                            why['보기 내용 ' + ('고침표' if tv is not None and y[kk] == tv else ('반각' if y[kk] == str(x[kk]).translate(FWT) else '??'))] += 1
                        elif kk == '정오':
                            why['정오'] += 1
                            if u not in SUS | set(PART):
                                odd.append('%s 정오 %s' % (u, x.get('키')))
                        else:
                            odd.append('%s 보기 %s' % (u, kk))
                if len(A) != len(b[k]):
                    odd.append('%s 보기 줄 수' % u)
            elif k == '선택지':
                if len(a[k]) != len(b[k]):
                    odd.append('%s 선택지 칸 수' % u)
                for i, (x, y) in enumerate(zip(a[k], b[k])):
                    if x == y:
                        continue
                    tv = (f.get('선택지') or [None] * 5)[i]
                    why['선택지 ' + ('고침표' if y == tv else ('반각' if y == str(x).translate(FWT) else '??'))] += 1
            elif k in ('문항', '해설', '해설2', '참고'):
                tv = f.get(k)
                why[k + ' ' + ('고침표' if tv is not None and b[k] == tv else ('반각' if b[k] == str(a[k]).translate(FWT) else '??'))] += 1
            else:
                odd.append('%s %s' % (u, k))
    odd += [k for k in why if k.endswith('??')]
    T('J-5 · F-6 다른 칸 무변 — 행 704 · 행·열 차례 · 바뀐 칸은 모두 까닭(고침표 · 반각 · 보기 줄 걷기 · 정오 23∪부분정답) · 까닭 모를 칸 0', not odd and len(D1) == 704, {'까닭': dict(why), '까닭 모름': odd[:8]})
    # ── J-7 · F-8 앱(진짜 포인터 · 손가락)
    # 9/24 H-4 — 고친 칸이 앱에 새 값으로 보인다(표본 25 · 바탕 = ocrfix 앞) — 회귀로 그대로
    rnd = random.Random(20260924)
    pool = sorted(u for u in FX if u not in FIXED)
    uids = FIXED + rnd.sample(pool, min(20, len(pool)))
    HB, HA = probe(pocr, 'old', uids), probe(NEWQ, 'new', uids)
    good, bad, base_bad = 0, [], 0
    for u in uids:
        r = BN.get(u); a = HA['items'].get(u) or {}; b = HB['items'].get(u) or {}
        tf = set(a.get('tf') or [])
        want_ch = [c for i, c in enumerate(r['선택지']) if 'c%d' % (i + 1) not in tf]
        got_ch = [c for i, c in enumerate(a.get('ch') or []) if 'c%d' % (i + 1) not in tf]
        ok_ch = (not (a.get('ch') or [])) if not any(str(c or '').strip() for c in r['선택지']) else (got_ch == want_ch and len(a.get('ch') or []) == 5)
        want_bg = {x['키']: x['내용'] for x in (r.get('보기') or []) if 'b' + x['키'] not in tf and x.get('내용')}
        ok_bg = all((a.get('bg') or {}).get(k) == v for k, v in want_bg.items())
        stem = str(r['문항']).split(' ⏎ ')[0]
        ok_pv = ('q' in tf) or (a.get('prev') is not None and stem[:20] in (a.get('prev') or '').replace('…', ''))
        if ok_ch and ok_bg and ok_pv:
            good += 1
        else:
            bad.append({'u': u, 'ch': [got_ch, want_ch] if not ok_ch else None, 'bg': None if ok_bg else [a.get('bg'), want_bg], 'pv': None if ok_pv else [a.get('prev'), stem[:30]]})
        fx = FX.get(u, {})
        bb = [c for i, c in enumerate(b.get('ch') or []) if 'c%d' % (i + 1) not in tf]
        if ('선택지' in fx and bb != want_ch) or ('보기' in fx and any((b.get('bg') or {}).get(k) != v for k, v in want_bg.items())):
            base_bad += 1
    T('H-4 앱 — 표본 %d(무작위 20 + 다섯) 첫 화면 줄 미리보기 · 문제 창 선택지 다섯 · 〈보기〉 줄 = 새 값(손값 없는 칸)' % len(uids), not bad and HA['n'] == len(D1), {'good': good, 'bad': bad[:4], 'n': HA['n']})
    T('H-4 헛잣대 — ocrfix 앞(182e1f37) 문항.json 으로는 고친 칸이 어긋난다(표본 대부분)', base_bad >= max(1, len(uids) // 2), {'어긋남': base_bad, '표본': len(uids)})
    T('H-4 페이지 오류 0', not HA['err'], HA['err'])
    A = probe_jeongo(NEWQ, 'jnew'); At = probe_jeongo(NEWQ, 'jnewt', touch=True, tool='view'); B = probe_jeongo(pjg, 'jbase')
    # (옛 「J-7 INFO 펜 도구 손가락」 줄은 ★ add2 K-3 관문으로 갈음 — penfinger_add1 이 앱 결함을 고쳤다)
    def okbogi(P, u, D):
        s = P.get(u) or {}; r = D[u]
        rows = s.get('rows') or []
        right = {x['k'] for x in rows if x['right']}; wrong = {x['k'] for x in rows if x['wrong']}
        return bool(rows) and all(x['vis'] for x in rows) and right == oxset(r) and wrong == oxset(r, 'X') and s.get('open') and s.get('sumHit') and all(h for _, h in s.get('hits') or []), \
            {'O(청록)': ''.join(sorted(right)), 'X(빨강)': ''.join(sorted(wrong)), '정답 O': ''.join(sorted(oxset(r))), '줄': ''.join(x['k'] for x in rows), '색': sorted({x['color'] for x in rows if x['right'] or x['wrong']}), '누름 맞음': [h for _, h in s.get('hits') or []], '펼침': s.get('open')}
    for tag, P in (('책상 · %s 도구' % A.get('_tool'), A), ('손가락 · 아이패드 폭 · %s 도구' % At.get('_tool'), At)):
        res = {u: okbogi(P, u, BN) for u in ('G45-09', 'G41-02', 'C5-095')}
        T('J-7 앱(%s) — G45-09 · G41-02 · C5-095 〈보기〉 O 누름 → 「정답 · 해설」 펼침 → O/X 가 정답 선택지 글자대로 보임 · G41-02 ㅁ 줄 없음' % tag,
          all(v[0] for v in res.values()) and 'ㅁ' not in [x['k'] for x in P['G41-02']['rows']], {u: v[1] for u, v in res.items()})
        res2 = {u: okbogi(P, u, BN) for u in ('C1-024', 'G36-06', 'G36-02')}
        T('F-8 앱(%s) — C1-024 〈보기〉 ㄱ·ㄹ·ㅁ = O · ㄴ·ㄷ = X 보임(G36-06 · G36-02 도 해설 키대로)' % tag,
          all(v[0] for v in res2.values()) and ''.join(sorted(oxset(BN['C1-024']))) == 'ㄱㄹㅁ', {u: v[1] for u, v in res2.items()})
        q = P['G34-02']; c = P['G37-02']['ch']
        T('F-8 앱(%s) — G34-02 문항에 「20℃로」 보임 · G37-02 ⑤ = 한 줄 선택지(높이 ≤ ① 높이 + 2)' % tag,
          bool(q.get('qvis') and '20℃로' in (q.get('q') or '') and len(c) == 5 and c[4]['vis'] and c[4]['h'] <= c[0]['h'] + 2 and c[4]['t'] == '⑤ 전향력이 작용하는 위도여야 한다.'),
          {'G34-02': (q.get('q') or '')[:40], '⑤': c[4] if len(c) == 5 else c, '①': c[0] if c else None})
        T('J-7 · F-8 페이지 오류 0(%s)' % tag, not any((P[u].get('err') or []) for u in JQ), [P[u].get('err') for u in JQ if P[u].get('err')][:3])
    resb = {u: okbogi(B, u, BJ) for u in ('G45-09', 'C5-095', 'C1-024', 'G36-06', 'G36-02')}
    T('J-7 · F-8 헛잣대 — 바탕 데이터: 앱이 보여 주는 O 집합이 정답 선택지 글자·해설 키와 어긋남(G45-09 · C5-095 · C1-024 · G36-06 · G36-02) · G41-02 ㅁ 줄 있음 · G34-02 「20。0로」 · G37-02 ⑤ 여러 줄',
      all(any(x['right'] for x in (B[u].get('rows') or [])) and B[u].get('open') for u in resb)   # 탐침이 실제로 칠했다(헛돌면 거저 참이 된다)
      and all(''.join(sorted({x['k'] for x in (B[u].get('rows') or []) if x['right']})) != ''.join(sorted(oxset(BN[u]))) for u in resb)
      and 'ㅁ' in [x['k'] for x in B['G41-02']['rows']] and '20。0로' in (B['G34-02'].get('q') or '') and B['G37-02']['ch'][4]['h'] > B['G37-02']['ch'][0]['h'] * 2,
      {u: v[1]['O(청록)'] for u, v in resb.items()})
    # ── ★ add2(9/27 · _task_jagwa_earth_jeongo_add2) K 묶음 — 그림 대조 되돌림 · C1-031 σ · 다른 칸 무변(바탕 19bc5b2f) · 펜 도구 손가락
    ADD2_REV = '19bc5b2f'
    RAW_19 = blob(ADD2_REV, 'earth/문항.json'); B19 = {r['uid']: r for r in json.loads(RAW_19.decode('utf-8'))}
    REVS = [('C2-093', '해설', '1500 m/s로 일정하다고', '1500 m/s 로 일정하다고'), ('C2-093', '해설', '4500(m)이다. 그런데', '4500(m) 이다. 그런데'),
            ('C4-046', '해설', '위 그림처럼 왼쪽', '위 그럼처럼 왼쪽'), ('G60-01', '해설', '103° ~ 180°이다', '103° ~180°이다')]
    k1 = [[u, str(BN[u][k]).count(good), str(BN[u][k]).count(bad), str(B19[u][k]).count(bad)] for u, k, bad, good in REVS]
    T('K-1 대조표 「원본과 다름」 4 조각 되돌림 — 새 데이터 = 원본 글(띄움 둘 · 「그럼처럼」 · 「~180°」) · 헛잣대: 바탕 19bc5b2f 는 손질된 글',
      all(g == 1 and b == 0 and b19 == 1 for _, g, b, b19 in k1), k1)
    T('K-2 C1-031 해설 적위 기호 = 원본 그림 σ(600dpi 확대 · δ 아님) — 무변 잣대(바탕도 σ)',
      'σ(적위)' in BN['C1-031']['해설'] and 'δ' not in BN['C1-031']['해설'] and 'σ(적위)' in B19['C1-031']['해설'], BN['C1-031']['해설'][40:110])
    difc = []
    for u, a in B19.items():
        b = BN.get(u)
        if b is None or list(a.keys()) != list(b.keys()):
            difc.append([u, '열']); continue
        difc += [[u, k] for k in a if a[k] != b[k]]
    back = {}
    for u, k, bad, good in REVS:
        back[(u, k)] = back.get((u, k), str(BN[u][k])).replace(good, bad)
    T('K-4 다른 칸 무변 — 바탕 19bc5b2f 와 바뀐 칸 = C2-093 · C4-046 · G60-01 해설 셋뿐 · 행 704 · 되돌림을 거꾸로 입히면 바탕 글과 같다(멱등은 H-5)',
      sorted(map(tuple, difc)) == sorted({(u, k) for u, k, _, _ in REVS}) and len(BN) == len(B19) == 704 and all(back[x] == B19[x[0]][x[1]] for x in back),
      {'바뀐 칸': difc, '거꾸로 = 바탕': {'%s %s' % x: back[x] == B19[x[0]][x[1]] for x in back}})
    # K-3 펜 도구 그대로 손가락(CDP 터치 r22) — 본판 §D-7 다시 · 바탕 앱 f497f05 → FAIL(헛잣대) · d27c43a(penfinger_add1) → PASS · 지금 작업트리 → PASS
    apps = {}
    for rev in ('f497f05', 'd27c43a'):
        ap = os.path.join(WORK, 'app_%s.html' % rev)
        open(ap, 'wb').write(subprocess.run(['git', '-C', GENIE, 'show', rev + ':jagwa/index.html'], capture_output=True).stdout)
        apps[rev] = ap
    for nm, ap, want in (('바탕 f497f05', apps['f497f05'], False), ('d27c43a', apps['d27c43a'], True), ('작업트리', None, True)):
        P = probe_jeongo(NEWQ, 'k3_' + nm.split()[-1], touch=True, app=ap)
        res = {u: okbogi(P, u, BN) for u in ('G45-09', 'G41-02', 'C5-095', 'C1-024')}
        ok = P.get('_tool') == 'pen' and all(v[0] for v in res.values()) and 'ㅁ' not in [x['k'] for x in P['G41-02']['rows']]
        md = hashlib.md5(open(ap or SRC, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:8]
        T('K-3 앱 %s(md5(LF) %s · %s 도구) 손가락 CDP r22 — G45-09 · G41-02 · C5-095 · C1-024 〈보기〉 O 누름 → 「정답 · 해설」 → O/X 가 정답대로 보임%s'
          % (nm, md, P.get('_tool'), ' — 헛잣대(이 앱은 FAIL 이어야 PASS)' if not want else ''), ok == want,
          {'잰 값': ok, '기대': want, '표': {u: v[1] for u, v in res.items()}, '오류': [P[u].get('err') for u in JQ if P.get(u, {}).get('err')][:2]})
    # ── 적어 둘 것(수행 결과 표)
    N('F-3 반각 바꾼 글자(글자별 · 바탕)', {c: sum(str(t or '').count(c) for r in DJG for k, t in cells(r)) for c in FWCH})
    dc = []
    for u, a in BJ.items():
        cn = dict(cells(BN[u]))
        for k, t in cells(a):
            t = str(t or '')
            if '。' in t:
                i = t.index('。'); new = str(cn.get(k) or '(걷힘)')
                dc.append([u, k, t.count('。'), t[max(0, i - 8):i + 6].replace('⏎', '/'), new[max(0, i - 8):i + 6].replace('⏎', '/')])
    N('F-4 「。」 칸(uid · 칸 · 개수 · 전 · 후 — 첫 「。」 둘레)', dc)
    lines = ['# _harness_earth_ocrfix(jeongo) — %s' % time.strftime('%Y-%m-%d %H:%M'),
             '바탕 %s(md5 %s) · 새(재생성) md5 %s · 인도본 md5 %s · 앱 genie 작업트리 jagwa/index.html md5(LF) %s' % (
                 BASE_JG_REV, hashlib.md5(RAW_JG).hexdigest()[:8], hashlib.md5(b1).hexdigest()[:8], hashlib.md5(cur).hexdigest()[:8],
                 hashlib.md5(open(SRC, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:8]), '']
    for s, n, d in RES:
        dd = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)
        lines.append('%s | %s | %s' % (s, n, dd[:1500]))
    nf = sum(1 for x in RES if x[0] == 'FAIL')
    lines += ['', '합계  PASS %d · FAIL %d · NOTE %d  (%.0f초)' % (sum(1 for x in RES if x[0] == 'PASS'), nf, sum(1 for x in RES if x[0] == 'NOTE'), time.time() - t0)]
    txt = '\n'.join(lines) + '\n'
    f = os.path.join(HERE, '_harness_earth_jeongo_result.txt')
    for _ in range(3):
        io.open(f, 'w', encoding='utf-8', newline='\n').write(txt); time.sleep(0.5)
        if io.open(f, encoding='utf-8').read() == txt:
            break
    print(lines[-1])
    return nf


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
