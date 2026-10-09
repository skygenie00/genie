# -*- coding: utf-8 -*-
r"""_task_jagwa_revfix0929 §B 관문 — 자과 검수 결함 고침(jagwa_uid · jagwa_search 검수 9/29) + 바탕 흠 넷

  python _harness_jagwa_revfix0929.py [--new <앱>] [--base <앱 파일 | git rev>] [--eng chromium,webkit] [--only b1,b2,...] [--vendor <cdnjs 사본>] [--res <결과>]

  NEW = genie 작업트리 jagwa/index.html · BASE(헛잣대) = 착수 때 genie HEAD(기본 HEAD — 이 판을 커밋한 뒤에는 --base <앞 커밋>)
  데이터 = studyplandata 작업트리(새 uid · 옛uid 칸) · 옛 데이터 = 새 uid 커밋(jagwa_uid)^ 의 과목 폴더 맨 위 JSON(git show · 그림·PDF 없음)
  기록 = studyplandata earth/기록.json 을 가짜 원격으로 — 작업트리 = 9/29 옛 열쇠 원격 · origin/main = 기기가 옮겨 올린 원격(읽기만)
        PUT 은 앱 fetch 를 가로채 몸통만 모은다(밖으로 안 나감 · 기록 쓰기 0)
  기기 하나 = 브라우저 문맥 하나(IndexedDB·localStorage 유지) — 같은 출처에서 앱·데이터·원격을 갈아 끼운다(_harness_jagwa_uid 의 Srv · __J)
  관문마다 NEW 는 PASS · BASE 는 FAIL(헛잣대 열) — 지켜야 할 옛 동작 칸(바탕도 참)은 「바탕 = 기준」
  --vendor = cdnjs.cloudflare.com/ajax/libs/… 사본 폴더(줄 때만 · cdnjs 가 막힌 곳) · 안 주면 cdnjs 그대로
  ⚠ 자과앱 픽셀 게이트 없음(CLAUDE.md) — DOM 글자 · 자리 · 개수 · 실제 마우스·손가락 누름
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기 헬퍼(_task_qa_slim2 A-1-2 · 옛 남 하네스 import 를 갈음)
import tempfile   # noqa: E402 — 옛 남 하네스 속성(HU.tempfile · B.WORK)을 갈음
import io, json, os, re, sys, time, copy
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# ← jagwa/_harness_jagwa_search.py:77-87 typeq 사본(글자 그대로 · 갈래 ④ · JG 밖 — 띄우기가 아니라 옮기지 않음)
def typeq(dv, text, enter=False):
    loc = dv.pg.locator('#q')
    if not loc.is_visible():
        return
    loc.click()
    loc.fill('')
    if text:
        dv.pg.keyboard.type(text, delay=5)
    if enter:
        dv.pg.keyboard.press('Enter')
    dv.pg.wait_for_timeout(250)

# ← jagwa/_harness_jagwa_search.py:90-91 st 사본(글자 그대로 · 갈래 ④ · JG 밖 — 띄우기가 아니라 옮기지 않음)
def st(dv):
    return dv.ev("()=>__S.st()")

# ← jagwa/_harness_jagwa_search.py:297-306 PHQ_JS 사본(글자 그대로 · 갈래 ③ · JG 밖 — 띄우기가 아니라 옮기지 않음)
PHQ_JS = r"""()=>{const out=[];const pick=(a)=>{for(const x of a){const v=String(x||'').trim();if(v.replace(/\s+/g,'').length>=2&&!out.includes(v)){out.push(v);return}}};
  const D=DATA;
  pick([D[0][F.CODE]]);pick([String(D[40][F.CODE]).slice(0,4)]);pick([String(D[200][F.CODE]).toLowerCase()]);pick([D[300][F.CODE]]);
  pick([D[10][F.SUB]]);pick([D[120][F.SUB]]);pick([D[400][F.SUB]]);
  [5,77,150,260,333,480].forEach(i=>{const b=String(D[i%D.length][F.BODY]||'').replace(/\s+/g,' ');pick([b.slice(10,15),b.slice(20,24)])});
  pick(['속력']);pick(['전기장']);pick(['15']);pick(['101']);
  const t=D.map(r=>typeOf(r[F.NO])).find(a=>a&&a.length);if(t)pick([t[0]]);
  const g=D.map(r=>String(gptOf(r[F.NO])||'')).find(x=>x.length>8);if(g)pick([g.slice(2,7)]);
  pick([String(D[99][F.VLT]||'')]);pick(['가속도']);pick(['운동량']);
  return out.slice(0,20)}"""


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = _roots.genie(); SPD = _roots.spd()
NEWF = ARG('--new', os.path.join(GENIE, 'jagwa', 'index.html'))
BASEF = ARG('--base', 'HEAD')
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
VENDOR = ARG('--vendor')
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_revfix0929_result.txt'))
WORK = os.path.join(tempfile.gettempdir(), 'h_jagwa_rf0929')
os.makedirs(WORK, exist_ok=True)
KEYS = ['bogi', 'unit', 'bpg', 'crop', 'tfix', 'gg', 'ggref', 'pick']
ROWS = []   # (관문, 엔진, 이름, NEW ok, BASE ok | None, 잰 값)
APPS = {}
from playwright.sync_api import sync_playwright   # noqa: E402


def R(g, eng, name, okn, okb, val):
    ROWS.append((g, eng, name, okn, okb, val))
    print('%s | 바탕 %s | %s · %s · %s | %s' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, eng, name,
          (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str))[:600]), flush=True)


def want(g):
    return not ONLY or g in ONLY


# ── qa_slim2(2026-10-08) regress 도우미 — 이름이 `_rg` · `_RG` 로 시작 = gate 에서 안 쓰는 갈래(gate 에서 도는 줄은 원래 글 그대로)
_RG_BOOT = "()=>__J.ready()&&typeof recBusy!=='undefined'&&!recBusy&&(((window.__PUTS||[]).length>0)||!!recErr)"   # 표지 = 앱 recBoot() 의 첫 syncRecords 끝(recBusy 거짓 · PUT 1 번 이상 또는 recErr) · INIT_HU 가 토큰을 넣어 부팅마다 맞춤 · PUT 을 한다


def _rg_cid(eng, *a):
    """기준 칸 id — 엔진 · 기기 · 과목 · 말을 붙여 한 실행 안에서 겹치지 않게(QC.base)"""
    return '@'.join([a[0], eng]) + ('/' + '/'.join(str(x) for x in a[1:]) if len(a) > 1 else '')


def _rg_pv(x):
    """b3 물리 한 말의 결과를 스냅샷 꼴로 — 줄 HTML · 나머지 글은 md5(12) · 「상위 100건」 꼬리는 남겨 pv_same 이 그대로 맞댄다"""
    import hashlib
    if not isinstance(x, dict):
        return x
    h = lambda s: hashlib.md5(str(s).encode('utf-8')).hexdigest()[:12]
    rest = x.get('rest') or ''
    return {'nos': list(x.get('nos') or []), 'only': list(x.get('only') or []), 'kind': list(x.get('kind') or []),
            'rows': [[n, h(t)] for n, t in (x.get('rows') or [])], 'rest': h(rest.replace(CAPNOTE, '')) + (CAPNOTE if CAPNOTE in rest else ''),
            'tt': list(x.get('tt') or [])}


def _rg_ren_sig(v):
    """b8 바탕 스냅샷(앞 인도판 NEW 훑기)도 새 판과 같은 이름 맞춤(_ren)으로 — sweep_cmp 는 새 판 쪽만 _ren 을 건다"""
    if not isinstance(v, dict):
        return v
    o = dict(v)
    for cat in ('over', 'clip', 'cover', 'small'):
        if isinstance(o.get(cat), list):
            o[cat] = [_ren(s) for s in o[cat]]
    return o


# ══════════ 기기 ══════════
OKNET = ('http://127.0.0.1', 'https://cdnjs.cloudflare.com/', 'https://cdn.jsdelivr.net/', 'https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')


def _route(rt):
    u = rt.request.url
    m = re.match(r'https://cdnjs\.cloudflare\.com/ajax/libs/(.+)$', u.split('?')[0]) if VENDOR else None
    if m:   # cdnjs 사본(줄 때만)
        f = os.path.join(VENDOR, *m.group(1).split('/'))
        if os.path.isfile(f):
            return rt.fulfill(path=f, content_type='text/css' if f.endswith('.css') else ('font/woff2' if f.endswith('.woff2') else 'application/javascript'))
        return rt.abort()
    return rt.continue_() if u.startswith(OKNET) else rt.abort()


def _init9():
    """HU.INIT + PUT 시각(performance.now) + console.info 자취(__LOG) — 옮김(jgMigrate 끝 줄)과 PUT 의 차례를 잰다"""
    s = JG.INIT_HU
    a = "window.__err=[];window.__PUTS=[];"
    b = "window.__PUTS.push({path,text:"
    assert s.count(a) == 1 and s.count(b) == 1
    s = s.replace(a, a + "window.__LOG=[];{const _ci=console.info.bind(console);console.info=function(){try{window.__LOG.push([performance.now()].concat([].slice.call(arguments,0,7).map(x=>(x&&typeof x==='object')?JSON.stringify(x):x)))}catch(e){}return _ci.apply(null,arguments)}}")
    return s.replace(b, "window.__PUTS.push({t:performance.now(),path,text:")


INIT9 = _init9()


class Dev:
    """기기 하나(문맥 하나) — load(앱, 데이터 폴더, 과목, 원격) 로 같은 출처에서 다시 연다 · vp = 창 크기 · touch 폰·iPad"""
    def __init__(self, br, eng, vp=None, mobile=False):
        self.eng = eng; self.S = JG.Srv()
        self.vp = vp or {'width': 1553, 'height': 900}
        self.phone = self.vp['width'] <= 480
        self.ctx = br.new_context(viewport=self.vp, device_scale_factor=1, has_touch=True, is_mobile=bool(mobile and eng == 'chromium'))
        self.ctx.route('**/*', _route)
        self.pg = None; self.errs = []; self.cdp = None

    def load(self, app, spd, subj, rec=None, wait=2500):
        QC.launch('base' if (APPS.get('BASE') is not None and app is APPS.get('BASE')) else 'new')   # 셈(§B-4) — regress 는 바탕 앱을 안 띄운다
        self.S.app = app; self.S.spd = spd; self.S.rec = dict(rec or {}); self.S.static = {}
        if self.pg:
            self.pg.close()
        self.pg = self.ctx.new_page(); self.pg.set_default_timeout(150000)
        self.pg.add_init_script(INIT9.replace('__SUBJ__', subj))
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:200]))
        self.pg.goto('http://127.0.0.1:%d/app.html' % self.S.port, wait_until='load')
        self.pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=120000)
        self.pg.evaluate(JG.JS_HU); self.pg.evaluate(JG.SJS); self.pg.evaluate(J9)
        for _ in range(120):
            if self.ev("()=>__J.ready()"):
                break
            self.pg.wait_for_timeout(250)
        if QC.GATE:
            self.pg.wait_for_timeout(wait)
        else:   # regress — 고정 2.5 초 대신 표지(첫 기록 맞춤 끝) · 상한 = 같은 2.5 초(못 만나면 gate 와 같은 시간)
            # 옛 줄: QC.until(self.pg, _RG_BOOT, wait, 'revfix0929 부팅 뒤 첫 syncRecords 끝(recBusy 거짓 · PUT 1+ 또는 recErr)')
            QC.until(self.pg, _RG_BOOT, max(wait, 15000), 'revfix0929 부팅 뒤 첫 syncRecords 끝(recBusy 거짓 · PUT 1+ 또는 recErr) · _task_qa_fix1 §A-3 상한 15 초(부하에서 늦는 첫 동기화를 끝까지 · 표지가 오면 바로)')
        self.cdp = self.ctx.new_cdp_session(self.pg) if self.eng == 'chromium' else None
        return self

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def settle(self, n=60):
        """기록 맞춤이 끝날 때까지(recBusy 거짓 · PUT 수 그대로)"""
        last = -1
        for _ in range(n):
            st = self.ev("()=>({b:typeof recBusy!=='undefined'&&recBusy,n:(window.__PUTS||[]).length})")
            if not st['b'] and st['n'] == last:
                return st['n']
            last = st['n']; self.pg.wait_for_timeout(300)
        return last

    def tap(self, x, y, wait=500):
        """폰·iPad = 손가락(Chromium CDP r22 · WebKit touchscreen.tap) · PC = 마우스"""
        if self.vp['width'] > 1100:
            self.pg.mouse.click(x, y)
        elif self.cdp:
            pt = {'x': x, 'y': y, 'radiusX': 22, 'radiusY': 22, 'force': 1, 'id': 1}
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [pt]}); self.pg.wait_for_timeout(60)
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        else:
            self.pg.touchscreen.tap(x, y)
        self.pg.wait_for_timeout(wait)

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass
        try:
            self.S.srv.shutdown()
        except Exception:
            pass


J9 = r"""
window.__R9={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 R(e){if(!e)return null;const r=e.getBoundingClientRect();return {l:Math.round(r.left*10)/10,r:Math.round(r.right*10)/10,t:Math.round(r.top*10)/10,b:Math.round(r.bottom*10)/10,w:Math.round(r.width*10)/10,h:Math.round(r.height*10)/10}},
 vis(e){if(!e||!e.isConnected)return false;const cs=getComputedStyle(e);if(cs.display==='none'||cs.visibility==='hidden')return false;const r=e.getBoundingClientRect();return r.width>0&&r.height>0},
 noOf(c){const r=DATA.find(x=>x[F.CODE]===c||String(codeShow(x))===c);return r?r[F.NO]:0},
 async open(no){try{closeView()}catch(e){}await new Promise(r=>setTimeout(r,200));await openView(no);await new Promise(r=>setTimeout(r,1500));return !document.getElementById('view').classList.contains('hide')},
 log(){return (window.__LOG||[]).slice()},
 puts(){return (window.__PUTS||[]).map(p=>({t:p.t,path:p.path,text:p.text}))},
 ls(){const o={};[U_KEY,GONE_KEY,SHADOW_KEY].forEach(k=>o[k]=localStorage.getItem(k)||'');return o}
};
"""


# ══════════ 데이터 · 원격 ══════════
def old_data():
    """새 uid 커밋 앞 판 — earth·bio 폴더 맨 위 JSON 만(git show · 그림·PDF 없음 = 404 · 기록 맞춤에 안 쓴다)"""
    d = os.path.join(WORK, 'spd_old')
    if os.path.isfile(os.path.join(d, 'earth', '문항.json')) and os.path.isfile(os.path.join(d, 'bio', '문항.json')):
        return d
    QC.sub('git:show-data')   # 셈 — studyplandata 옛 데이터(jagwa_uid^) 풀기 · TEMP 에 없을 때만(앱 풀기 아님)
    rev = JG.git_HU(SPD, 'log', '--format=%h', '-1', '--grep=jagwa_uid', '--', 'earth/문항.json').decode().strip() or '4a01147'
    for s in ('earth', 'bio'):
        os.makedirs(os.path.join(d, s), exist_ok=True)
        for p in JG.git_HU(SPD, 'ls-tree', '--name-only', rev + '^', s + '/').decode('utf-8').split('\n'):
            p = p.strip().strip('"')
            if p.endswith('.json'):
                open(os.path.join(d, p.replace('/', os.sep)), 'wb').write(JG.git_HU(SPD, 'show', '%s^:%s' % (rev, p)))
    return d


def o2n(subj='earth'):
    return {r['옛uid']: r['uid'] for r in json.loads(open(os.path.join(SPD, subj, '문항.json'), 'rb').read().decode('utf-8')) if r.get('옛uid')}


def rec_old():
    return open(os.path.join(SPD, 'earth', '기록.json'), 'rb').read()   # 작업트리 = 9/29 옛 열쇠 원격(44a39616 · 옛 열쇠 묘비 crop|G47-07 하나)


def rec_now():
    QC.sub('git:show-data')   # 셈 — studyplandata origin/main 기록(데이터 · 앱 풀기 아님)
    try:
        b = JG.git_HU(SPD, 'show', 'origin/main:earth/기록.json')
        return b if b.strip().startswith(b'{') else None
    except Exception:
        return None


def B(o):
    return json.dumps(o, ensure_ascii=False).encode('utf-8')


def keycount(body, O2N):
    """몸통 셈 — data 옛 열쇠 · u 옛 열쇠 · gone 옛 열쇠 · data 새 열쇠"""
    D = body.get('data', {}) or {}; U = body.get('u', {}) or {}; G = body.get('gone', {}) or {}
    news = set(O2N.values())
    old = lambda x: x.split('|', 1)[0] in KEYS and x.split('|', 1)[1] in O2N
    return {'data 옛': sum(1 for k in KEYS for c in (D.get(k) or {}) if c in O2N),
            'data 새': sum(1 for k in KEYS for c in (D.get(k) or {}) if c in news and c not in O2N),
            'u 옛': sum(1 for x in U if old(x)), 'gone 옛': sum(1 for x in G if old(x)),
            '통별 data 옛': {k: sum(1 for c in (D.get(k) or {}) if c in O2N) for k in KEYS}}


def app_src(x):
    if os.path.isfile(x):
        return open(x, 'rb').read().replace(b'\r\n', b'\n')
    return JG.git_HU(GENIE, 'show', '%s:jagwa/index.html' % x)


# ══════════ B-1 · B-2 기록 옮김 ══════════
def _puts(dv):
    return [dict(p, body=json.loads(p['text'])) for p in dv.ev("()=>__R9.puts()") if p.get('path') == 'earth/기록.json' and p.get('text')]


def _r0(dt):
    """9/29 원격(옛 열쇠) 에서 지운 칸 crop|G47-07 을 묘비 대신 값으로 — 도장 = 묘비 시각 + dt(ms)"""
    R1 = json.loads(rec_old()); T1 = R1['gone']['crop|G47-07']
    R0 = copy.deepcopy(R1); del R0['gone']['crop|G47-07']
    R0['data']['crop']['G47-07'] = copy.deepcopy(next(iter(R1['data']['crop'].values())))
    R0['u']['crop|G47-07'] = T1 + dt
    return R0, T1


def b1a(br, eng, app):
    """옛 판 기기가 원격에서 지워진 옛 열쇠 칸을 가진 채 새 판 → 새 열쇠 칸 0 · PUT 0 · gone[새] · 멱등"""
    R0, T1 = _r0(-86400000)
    dv = Dev(br, eng)
    try:
        dv.load(app, old_data(), 'earth', rec={'earth/기록.json': B(R0)}); dv.settle()
        had = dv.ev("()=>Object.prototype.hasOwnProperty.call(CROP,'G47-07')")
        dv.load(app, SPD, 'earth', rec={'earth/기록.json': rec_old()}); dv.settle()
        loc = dv.ev("()=>Object.prototype.hasOwnProperty.call(CROP,'G10-47-07')")
        P = _puts(dv); last = P[-1]['body'] if P else {}
        inp = sum(1 for p in P if 'G10-47-07' in ((p['body'].get('data') or {}).get('crop') or {}))
        g = dv.ev("()=>__J.gone()")
        ls1 = dv.ev("()=>__R9.ls()"); n2 = dv.ev("async()=>{try{return await jgMigrate('again')}catch(e){return 'ERR '+e}}"); ls2 = dv.ev("()=>__R9.ls()")
        dv.load(app, SPD, 'earth', rec={'earth/기록.json': B(last)}); dv.settle()
        mig2 = dv.ev("()=>__J.mig()"); P2 = _puts(dv); b2 = P2[-1]['body'] if P2 else {}
        same2 = all(json.dumps(b2.get(k), sort_keys=True) == json.dumps(last.get(k), sort_keys=True) for k in ('data', 'u', 'gone'))
        val = {'옛 판에서 값 가짐': had, '새 판 로컬 crop G10-47-07': loc, 'PUT 에 그 칸': '%d/%d' % (inp, len(P)),
               '로컬 gone[crop|G10-47-07]': g.get('crop|G10-47-07'), 'PUT gone[crop|G10-47-07]': (last.get('gone') or {}).get('crop|G10-47-07'), '원격 묘비 T1': T1,
               '두 번째 jgMigrate': n2, '바이트 같음(u·gone·shadow)': ls1 == ls2, '두 번째 열림 옮김': mig2, '두 번째 PUT data·u·gone = 첫': same2, '오류': dv.errs[:2]}
        ok = had and not loc and inp == 0 and len(P) > 0 and g.get('crop|G10-47-07') and (last.get('gone') or {}).get('crop|G10-47-07') and n2 == 0 and ls1 == ls2 and mig2 == 0 and same2 and not dv.errs
        return bool(ok), val
    finally:
        dv.close()


def b1b(br, eng, app):
    """반대 — 그 칸 도장이 묘비보다 새로우면 옮긴다(새 열쇠 칸 · PUT 에 있음)"""
    R0, T1 = _r0(3600000)
    dv = Dev(br, eng)
    try:
        dv.load(app, old_data(), 'earth', rec={'earth/기록.json': B(R0)}); dv.settle()
        had = dv.ev("()=>Object.prototype.hasOwnProperty.call(CROP,'G47-07')")
        dv.load(app, SPD, 'earth', rec={'earth/기록.json': rec_old()}); dv.settle()
        loc = dv.ev("()=>Object.prototype.hasOwnProperty.call(CROP,'G10-47-07')")
        P = _puts(dv); last = P[-1]['body'] if P else {}
        inp = 'G10-47-07' in ((last.get('data') or {}).get('crop') or {})
        u = (last.get('u') or {}).get('crop|G10-47-07')
        return bool(had and loc and inp and u == T1 + 3600000), {'옛 판에서 값 가짐(도장 = 묘비 + 1시간)': had, '새 판 로컬 G10-47-07': loc, 'PUT data': inp, 'PUT u': u, '오류': dv.errs[:2]}
    finally:
        dv.close()


def b1c(br, eng, app):
    """이미 받은 옛 열쇠 묘비(옛 판에서 맞춤) → 새 판 jgMigrate 가 새 열쇠에 비춤(같은 시각) · PUT 에도"""
    dv = Dev(br, eng)
    try:
        dv.load(app, old_data(), 'earth', rec={'earth/기록.json': rec_old()}); dv.settle()
        g0 = dv.ev("()=>__J.gone()").get('crop|G47-07')
        dv.load(app, SPD, 'earth', rec={'earth/기록.json': rec_old()}); dv.settle()
        g = dv.ev("()=>__J.gone()"); P = _puts(dv); last = P[-1]['body'] if P else {}
        lg = [x for x in dv.ev("()=>__R9.log()") if len(x) > 2 and x[1] == 'jagwa uid 옮김']
        return bool(g0 and g.get('crop|G10-47-07') == g0 and (last.get('gone') or {}).get('crop|G10-47-07') == g0), \
            {'옛 판 로컬 gone[crop|G47-07]': g0, '새 판 gone[crop|G10-47-07]': g.get('crop|G10-47-07'), 'PUT gone': (last.get('gone') or {}).get('crop|G10-47-07'),
             '옛 묘비 그대로': g.get('crop|G47-07'), '옮김 자취': [x[1:7] for x in lg][:3]}
    finally:
        dv.close()


def b1d(br, eng, app):
    """안전 — 이미 옮긴 원격(origin/main · 옮김 묘비 373 + 새 칸 값)으로 빈 기기 → 새 칸 값 하나도 안 지움 · 옮김 묘비를 새 칸에 안 비춤"""
    RN = rec_now()
    if not RN:
        return None, 'origin/main:earth/기록.json 없음(가져오지 않음) — 건너뜀'
    O2N = o2n(); rn = json.loads(RN); D = rn.get('data', {})
    want_k = {k: sorted((D.get(k) or {}).keys()) for k in KEYS}
    dv = Dev(br, eng)
    try:
        dv.load(app, SPD, 'earth', rec={'earth/기록.json': RN}); dv.settle()
        st = dv.ev("k=>__J.stores(k)", KEYS); P = _puts(dv); last = P[-1]['body'] if P else {}
        loc_same = {k: sorted((st.get(k) or {}).keys()) == want_k[k] for k in KEYS}
        put_same = {k: sorted(((last.get('data') or {}).get(k) or {}).keys()) == want_k[k] for k in KEYS}
        G = last.get('gone') or {}
        moved_new_tomb = [x for x in G if x.split('|', 1)[0] in KEYS and x.split('|', 1)[1] in set(O2N.values()) and x != 'crop|G10-47-07']
        n_live = sum(len(v) for v in want_k.values())
        ok = all(loc_same.values()) and all(put_same.values()) and not moved_new_tomb and len(P) > 0
        return bool(ok), {'원격 새 칸 값': n_live, '로컬 칸 = 원격': all(loc_same.values()), 'PUT data 칸 = 원격': all(put_same.values()),
                          '새 열쇠 묘비(crop|G10-47-07 밖)': len(moved_new_tomb), 'gone[crop|G10-47-07]': G.get('crop|G10-47-07'), '오류': dv.errs[:2]}
    finally:
        dv.close()


def literal_rule():
    """글자 그대로(모든 옛 묘비 → 새 열쇠 max) 라면 origin/main 원격에서 묘비에 질 새 칸 값 수(도장 ≤ 묘비)"""
    RN = rec_now()
    if not RN:
        return None
    O2N = o2n(); rn = json.loads(RN); D = rn.get('data', {}); U = rn.get('u', {}); G = rn.get('gone', {})
    n = 0
    for x, t in G.items():
        k, o = x.split('|', 1)
        if k in KEYS and o in O2N and O2N[o] in (D.get(k) or {}) and (U.get(k + '|' + O2N[o]) or 0) <= t:
            n += 1
    return {'옛 열쇠 묘비': sum(1 for x in G if x.split('|', 1)[0] in KEYS and x.split('|', 1)[1] in O2N), '지워질 새 칸 값': n,
            '원격 savedAt': rn.get('savedAt'), '묘비 시각들': sorted({t for x, t in G.items() if x.split('|', 1)[0] in KEYS and x.split('|', 1)[1] in O2N})[-3:]}


def b2(br, eng, app):
    """빈 기기 첫 PUT — 옛 열쇠 원격(9/29) · 몸통 옛 열쇠 0 · u 옛 0 · 옛 열쇠 묘비 = 옮긴 칸 + 원래 묘비 · 차례 = 옮김 끝 → PUT"""
    O2N = o2n(); R1 = json.loads(rec_old())
    moved = sum(1 for k in KEYS for c in (R1['data'].get(k) or {}) if c in O2N)
    orig = sum(1 for x in R1.get('gone', {}) if x.split('|', 1)[0] in KEYS and x.split('|', 1)[1] in O2N)
    dv = Dev(br, eng)
    try:
        dv.load(app, SPD, 'earth', rec={'earth/기록.json': rec_old()}); dv.settle()
        P = _puts(dv)
        if not P:
            return False, {'PUT': 0, '오류': dv.errs[:2]}
        kc = keycount(P[0]['body'], O2N)
        lg = [x for x in dv.ev("()=>__R9.log()") if len(x) > 2 and x[1] == 'jagwa uid 옮김' and x[2] == 'merge']
        tm = lg[0][0] if lg else None
        order = ('옮김 끝(%.0fms) → PUT(%.0fms)' % (tm, P[0]['t'])) if tm is not None and tm < P[0]['t'] else \
                ('PUT(%.0fms) → 옮김 끝(%s)' % (P[0]['t'], ('%.0fms' % tm) if tm is not None else '없음'))
        ok = kc['data 옛'] == 0 and kc['u 옛'] == 0 and kc['gone 옛'] == moved + orig and tm is not None and tm < P[0]['t']
        return bool(ok), {'첫 PUT': {k: v for k, v in kc.items()}, '옮긴 칸 + 원래 묘비': '%d + %d' % (moved, orig), '차례': order,
                          '옮김 자취': [x[2:6] for x in lg][:2], 'PUT 수': len(P)}
    finally:
        dv.close()


# ══════════ B-3 검색 결과 줄 ══════════
ROWJS = r"""()=>{const b=document.getElementById('esres');const rows=b?[...b.querySelectorAll('[data-esq]')]:[];
  return {nl:rows.filter(d=>(d.textContent||'').includes('⏎')).length,boxNl:b?(b.textContent||'').split('⏎').length-1:0,
    none:rows.filter(d=>!d.querySelector('mark')).map(d=>__R9.tx(d.querySelector('.cd'))),
    body:rows.filter(d=>__R9.tx(d.querySelector('.gl i'))==='본문').length}}"""


def _sq(dv, w):
    typeq(dv, w)
    s = st(dv); x = dv.ev(ROWJS)
    return s, {'건': s['qcnt'], '줄': s['n'], '표시 없는 줄': len(x['none']), '⏎ 줄': x['nl'], '💬 본문': x['body'], '표시 없는 줄 보기': x['none'][:4]}


def b3(br, eng, app):
    out = {}
    dv = Dev(br, eng).load(app, SPD, 'earth', rec={'earth/기록.json': rec_old()})
    try:
        for w in ('맨틀', '지진', '마그마', '이다'):
            s, o = _sq(dv, w)
            if w == '맨틀':
                row = next((r for r in s['rows'] if r['code'] == 'G03-40-05'), None)
                o['G03-40-05'] = {'칸': row['lab'], 'mark': row['marks'], '💬': row['chat']} if row else None
            out['지학 ' + w] = o
        out['오류 지학'] = dv.errs[:2]
    finally:
        dv.close()
    dv = Dev(br, eng).load(app, SPD, 'bio', rec={})
    try:
        for w in ('DNA', '세포막', '효소', '오답해설', '정답해설', '이다', '자료해석 2탄', '자료해석⏎2탄'):
            out['생물 ' + w] = _sq(dv, w)[1]
        out['오류 생물'] = dv.errs[:2]
    finally:
        dv.close()
    m = out['지학 맨틀']; g = m.get('G03-40-05') or {}
    ok = (m['건'] == '42건' and m['표시 없는 줄'] == 0 and g.get('칸') == '본문' and g.get('mark', 0) >= 1
          and out['생물 DNA']['표시 없는 줄'] == 0 and out['생물 오답해설']['⏎ 줄'] == 0 and out['생물 자료해석 2탄']['건'] == '1건'
          and out['생물 자료해석⏎2탄']['건'] == '1건' and not out['오류 지학'] and not out['오류 생물'])
    return bool(ok), out


PVJS = r"""(q)=>{ /* ★ physprev(10/2) — _task_jagwa_physprev 57줄(A-2-3): 물리만 t 로만 걸린 줄(only) · 조각이 t 인 줄(kind) · 결과 줄을 번호마다(rows) · 나머지 글(rest) */
 const ph=typeof HASBOOK!=='undefined'&&!HASBOOK&&typeof pvHit==='function'&&typeof esHit==='function'&&typeof esPhysHit==='function';
 const only=[],kind=[];
 if(ph){ES_NOS.forEach(n=>{const r=DATA.find(x=>x[F.NO]===n);const h=r?esHit(r,q):null;if(h&&h.k==='prev')kind.push(n)});
   const keep=window.pvHit;try{window.pvHit=undefined;ES_NOS.forEach(n=>{const r=DATA.find(x=>x[F.NO]===n);if(r&&!esPhysHit(r,q))only.push(n)})}finally{window.pvHit=keep}}
 const box=document.getElementById('esres');
 const rows=box?[...box.children].filter(e=>e.dataset&&e.dataset.esq).map(e=>[+e.dataset.esq,e.outerHTML]):[];
 let rest='';if(box){const c=box.cloneNode(true);[...c.children].forEach(e=>{if(e.dataset&&e.dataset.esq)e.remove()});rest=c.innerHTML}
 /* ★ 2026-10-07 (_task_jagwa_phys_win §A-45) — 물리 위 검색이 보이는 제목(titleOf)·고친 제목(pnFix)도 찾음 → 그 둘로 걸리는 번호 tt(앱 esPhysHit 글에 titleOf(r) 가 있을 때만 · 옛 판은 빈 목록)
    옛 줄: return {nos:ES_NOS.slice(),only,kind,rows,rest}} */
 const tt=(ph&&String(esPhysHit).indexOf('titleOf(r)')>=0)?ES_NOS.filter(n=>{const r=DATA.find(x=>x[F.NO]===n);return !!r&&(String(titleOf(r)).includes(q)||String(pnFix(r)||'').includes(q))}):[];
 return {nos:ES_NOS.slice(),only,kind,rows,rest,tt}}"""
CAPNOTE = '<div class="bplnone">상위 100건만 표시했습니다. 검색어를 더 좁혀보세요.</div>'


def pv_same(n, b):
    """★ physprev(10/2) — 근거 = _task_jagwa_physprev 57줄(A-2-3) · 말 하나의 새 판(n) · 바탕(b) 결과를 맞댄다 → (같음, 적을 값)
       집합 = 새 판 걸린 것 − t 로만 걸린 것 == 바탕 걸린 것 · 줄 HTML = 둘 다 보이는 줄 중 조각이 t 인 줄을 뺀 것끼리 같고 차례도 같음
       · 바탕에 보이는데 새 판에 안 보이는 줄은 새 판이 100줄 상한에 닿았을 때만(t 로 더 걸려 밀림) · 나머지 글은 「상위 100건」 꼬리를 빼고 같음"""
    if not isinstance(n, dict) or not isinstance(b, dict):
        return n == b, {}
    only, kind = set(n.get('only') or []), set(n.get('kind') or []) | set(b.get('kind') or [])
    nn = [x for x in n['nos'] if x not in only]
    bb = [x for x in b['nos'] if x not in set(b.get('only') or [])]
    rn = [(x, h) for x, h in n['rows'] if x not in kind]
    rb = [(x, h) for x, h in b['rows'] if x not in kind]
    hn, hb = dict(rn), dict(rb)
    common = [x for x, _ in rn if x in hb]
    html_bad = [x for x in common if hn[x] != hb[x]]
    order_ok = common == [x for x, _ in rb if x in hn]
    miss = [x for x, _ in rb if x not in hn]
    cap_ok = not miss or len(n['rows']) >= 100
    # ★ 2026-10-07 (_task_jagwa_phys_win §A-45) — 새 판 물리 위 검색이 보이는 제목·고친 제목도 찾음 → 바탕에 없고 tt 에 든 번호(tx)는 「제목으로 더 걸림」 = 뜻한 차 · 그 밖은 옛 잣대 그대로(옛 판은 tt 가 비어 tx 0)
    tt, bset = set(n.get('tt') or []), set(bb)
    tx = [x for x in nn if x not in bset and x in tt]
    # 옛 줄: extra = [x for x, _ in rn if x not in hb]
    extra = [x for x, _ in rn if x not in hb and x not in tx]
    extra_ok = not extra or len(b['rows']) >= 100
    rest_ok = n['rest'].replace(CAPNOTE, '') == b['rest'].replace(CAPNOTE, '') \
        and ((CAPNOTE in n['rest']) == (len(n['nos']) > 100)) and ((CAPNOTE in b['rest']) == (len(b['nos']) > 100))
    # 옛 줄: same = nn == bb and not html_bad and order_ok and cap_ok and extra_ok and rest_ok
    same = (nn == bb or (bool(tx) and [x for x in nn if x not in tx] == bb)) and not html_bad and order_ok and cap_ok and extra_ok and rest_ok   # ★ 2026-10-07 (_task_jagwa_phys_win §A-45) — 집합 = 바탕 + 제목으로 더 걸린 것(차례 그대로)
    info = {'t 로만': len(only), '조각 t': len(kind), '상한 밀림': len(miss)} if (only or kind or miss) else {}
    if tx:   # ★ 2026-10-07 (_task_jagwa_phys_win §A-45) — 제목으로 더 걸린 번호 수는 값에 남김
        info['제목으로 더 걸림'] = len(tx)
    if not same:
        info.update({'집합 같음': nn == bb, '줄 HTML 다름': html_bad[:5], '차례': order_ok, '상한': [len(n['rows']), len(b['rows']), miss[:5]], '더 보임': extra[:5], '나머지 글': rest_ok})
    return same, info


def b3p(br, eng, app):
    """물리 — 걸린 집합(ES_NOS) · 결과 상자 HTML 을 말마다(바탕과 견준다)"""
    dv = Dev(br, eng).load(app, SPD, 'phys', rec={})
    try:
        Q = dv.ev(PHQ_JS)
        res = {}
        for q in Q:
            typeq(dv, q)
            res[q] = dv.ev(PVJS, q)   # ★ physprev(10/2) — 걸린 집합 · 결과 줄을 번호마다(옛 [ES_NOS, innerHTML] 대신 · 맞대기는 pv_same)
        return res
    finally:
        dv.close()


# ══════════ B-4 폰 문항 창 카드 ══════════
CARDJS = r"""()=>{const w=document.getElementById('cardwrap'),c=document.getElementById('card'),v=document.getElementById('view');
  if(!w||!c||!__R9.vis(w)){const st=v&&v.querySelector('.stage,#stage');return {nocard:true,mode:v&&v.classList.contains('win')?'창':'전체',
    viewOw:v?Math.max(0,v.scrollWidth-v.clientWidth):null,stage:st?__R9.R(st):null,view:__R9.R(v)}}
  const pr=parseFloat(getComputedStyle(w).paddingRight)||0;
  const sel=[...c.querySelectorAll('.ox button, button.vox, button.pl, #cLink, #cNext, .cmark')].filter(__R9.vis);
  const bad=[];   /* 필기 층(#qink)·글상자 층(#qtxt)은 카드 전체를 덮는다(펜이 켜진 채 손가락 톡은 inkPierce 가 밑으로 넘김) — 그 층을 뺀 맨 위 */
  const top=(x,y)=>document.elementsFromPoint(x,y).find(e=>!(e.closest&&e.closest('#qink,#qtxt')))||null;
  /* 세로로만 굴린다 — scrollIntoView 는 overflow-x:hidden 틀도 옆으로 굴려 잘린 단추를 끌어온다(손가락으로는 못 하는 굴림) */
  w.scrollLeft=0;const W0=w.getBoundingClientRect();
  for(const b of sel){const r0=b.getBoundingClientRect();w.scrollTop+=(r0.top+r0.height/2)-(W0.top+W0.height/2);w.scrollLeft=0;
    const r=b.getBoundingClientRect(),y=r.top+r.height/2;   /* 왼쪽 끝 · 가운데 · 오른쪽 끝 — 잘린 단추는 가운데는 눌려도 오른쪽 끝이 틀 밖이다 */
    for(const x of [r.left+1.5,r.left+r.width/2,r.right-1.5]){const at=top(x,y);
      if(!(at&&(at===b||b.contains(at)))){bad.push((b.id||b.className||b.tagName)+':'+__R9.tx(b).slice(0,8)+'@'+Math.round(x)+','+Math.round(y)+'→'+(at?(at.id||String(at.className).slice(0,16)||at.tagName):'없음'));break}}}
  w.scrollLeft=0;const W=w.getBoundingClientRect(),C=c.getBoundingClientRect();
  return {sl:w.scrollLeft,mode:v.classList.contains('win')?'창':'전체',wrap:[Math.round(W.left),Math.round(W.right)],card:[Math.round(C.left*10)/10,Math.round(C.right*10)/10],
    gapL:Math.round((C.left-W.left)*10)/10,gapR:Math.round((W.right-C.right)*10)/10,inFrame:C.right<=W.right-pr+0.5,tf:c.style.transform,btn:sel.length,bad:bad.slice(0,6),
    det:!!(c.querySelector('details')||{}).open}}"""
SAMPLES = {'bio': ['B20-57-05', 'B01-38-01', 'B012T'], 'earth': ['G95-32-01', 'G1-010C', 'G03-40-05'], 'phys': None}


def b4(br, eng, app):
    out = {}; ok = True
    for subj in ('bio', 'earth', 'phys'):
        dv = Dev(br, eng, {'width': 390, 'height': 844}, mobile=True).load(app, SPD, subj, rec={'earth/기록.json': rec_old()} if subj == 'earth' else {})
        try:
            codes = SAMPLES[subj] or dv.ev("()=>[DATA[0],DATA[200],DATA[400]].filter(Boolean).map(r=>r[F.CODE])")
            for cd in codes:
                no = dv.ev("c=>__R9.noOf(c)", cd)
                if not no:
                    out['%s %s' % (subj, cd)] = '행 없음'; ok = False; continue
                dv.ev("n=>__R9.open(n)", no)
                m = [dv.ev(CARDJS)]
                if not m[0].get('nocard'):
                    dv.ev("()=>{const d=document.querySelector('#card details');if(d){d.open=true;d.dispatchEvent(new Event('toggle'))}}"); dv.pg.wait_for_timeout(500)
                    m.append(dv.ev(CARDJS))
                dv.ev("()=>{try{vwApply(false)}catch(e){}}"); dv.pg.wait_for_timeout(700)
                m.append(dv.ev(CARDJS))
                dv.ev("()=>{try{vwApply(true)}catch(e){}}"); dv.pg.wait_for_timeout(400)
                for x in m:
                    if x.get('nocard'):
                        ok = ok and (x.get('viewOw') or 0) <= 1
                    else:
                        ok = ok and x['inFrame'] and abs(x['gapL'] - x['gapR']) <= 1 and not x['bad'] and x['btn'] > 0
                out['%s %s' % (subj, cd)] = m
                print('   b4 %s %s %s' % (subj, cd, ' | '.join(('%s 틀 밖' % x['mode']) if x.get('nocard') is None and False else
                      ('%s 카드 없음 넘침 %s' % (x['mode'], x.get('viewOw'))) if x.get('nocard') else
                      ('%s%s 여백 %s/%s 틀 안 %s 단추 %d 못 누름 %d' % (x['mode'], '·해설' if x.get('det') else '', x['gapL'], x['gapR'], x['inFrame'], x['btn'], len(x['bad']))) for x in m)), flush=True)
            if dv.errs:
                ok = False; out['오류 ' + subj] = dv.errs[:2]
        finally:
            dv.close()
    return bool(ok), out


# ══════════ B-5 서랍 줄 ══════════
NDJS = r"""()=>{const L=[...document.querySelectorAll('.ndrow')];let dot=0,dash=0;const other=[];
  /* ★ uid_unify 옛 잣대 고침 G-1(2026-10-04 · 근거 gigu/_task_jagwa_uid_unify.md §G-1 · 사용자 10/4 16:45 「uid 랑 중복되니까 nn회 n번 없애」) — 서랍 줄 .ndt 는 카드 층 기출(uid = ^[BG]\d\d-\d+-\d+$)에서 「번호 · 출처」 가 아니라 번호만(uid + 난이도 글자) ·
     확인문제 · 타기출 · 예상 · 물리 · 옛 판은 옛 「번호 · 출처」 그대로 — uid 줄 수는 uid 로 센다(기준은 이 하네스가 정규식으로 가린다 · 앱 ynUid 는 「새 판인가」 갈래에만 쓴다) */
  let uid=0;const NEWERA=typeof ynUid==='function',HB=typeof HASBOOK!=='undefined'&&!!HASBOOK;
  L.forEach(d=>{const r=rec(+d.dataset.no);if(!r)return;const t=d.querySelector('.ndt').textContent,p=String(r[F.CODE])+String(r[F.LV]==null?'':r[F.LV]);
    /* 옛: if(NEWERA&&HB&&/^[BG]\d\d-\d+-\d+$/.test(String(r[F.CODE]))){…} — 채팅 10/4 23:1x 판정 (가) 로 G-1 은 지학만(앱 ynUid = ^G) */
    if(NEWERA&&HB&&(typeof ynUid==='function'?ynUid(r):/^G\d\d-\d+-\d+$/.test(String(r[F.CODE])))){if(t===p)uid++;else other.push(t.slice(0,30));return}
    if(t.startsWith(p+' · '))dot++;else if(t.startsWith(p+'-'))dash++;else other.push(t.slice(0,30))});
  const e=document.querySelector('.ndrow .ndt'),cs=e?getComputedStyle(e):null;
  return {n:L.length,dot,dash,other:other.slice(0,4),sample:L.slice(0,2).map(d=>d.querySelector('.ndt').textContent),
    uid,   /* ★ uid_unify G-1 — 기출 uid 줄 수 */
    font:cs?cs.fontFamily.slice(0,30)+' '+cs.fontSize+' '+cs.fontWeight:null,ell:cs?cs.textOverflow+'/'+cs.whiteSpace+'/'+cs.overflow:null}}"""


def b5(br, eng, app):
    out = {}; ok = True
    for subj in ('bio', 'earth', 'phys'):
        dv = Dev(br, eng).load(app, SPD, subj, rec={'earth/기록.json': rec_old()} if subj == 'earth' else {})
        try:
            x = dv.ev(NDJS); out[subj] = x
            # 옛 줄: ok = ok and x['n'] > 0 and x['dash'] == 0 and x['dot'] == x['n']
            ok = ok and x['n'] > 0 and x['dash'] == 0 and x['dot'] + x.get('uid', 0) == x['n']   # ★ uid_unify §G-1 — 기출 uid 줄(번호만) + 「번호 · 출처」 줄 = 줄 수
        finally:
            dv.close()
    return bool(ok), out


# ══════════ B-6 폰 머리 접기 단추 ══════════
FOLDJS = r"""()=>{const b=document.getElementById('fFoldBtn'),g=document.getElementById('ndGrip');if(!b||!__R9.vis(b))return null;
  const R=b.getBoundingClientRect(),G=g&&__R9.vis(g)?g.getBoundingClientRect():null;
  let x0=1e9,x1=-1e9,y0=1e9,y1=-1e9,n=0,onGrip=0;
  for(let y=Math.floor(R.top-12);y<=Math.ceil(R.bottom+12);y++)for(let x=Math.max(0,Math.floor(R.left-14));x<=Math.ceil(R.right+16);x++){
    const e=document.elementFromPoint(x+0.5,y+0.5);if(e&&(e===b||b.contains(e))){n++;x0=Math.min(x0,x);x1=Math.max(x1,x+1);y0=Math.min(y0,y);y1=Math.max(y1,y+1);if(G&&x<G.right)onGrip++}}
  const nb=[...b.parentNode.children].filter(e=>e!==b&&__R9.vis(e)&&e.getBoundingClientRect().left>=R.right-1)[0]||null;
  let nbOk=null;if(nb){const r=nb.getBoundingClientRect(),e=document.elementFromPoint(r.left+1,r.top+r.height/2);nbOk=!!e&&(e===nb||nb.contains(e))}
  const up=b.parentNode.previousElementSibling;let upOk=null;if(up&&__R9.vis(up)){const r=up.getBoundingClientRect(),e=document.elementFromPoint(R.left+R.width/2,r.bottom-1);upOk=!(e&&(e===b||b.contains(e)))}
  return {btn:__R9.R(b),grip:G?{l:Math.round(G.left),r:Math.round(G.right)}:null,hit:{l:x0,r:x1,t:y0,b:y1,w:x1-x0,h:y1-y0},onGrip,
    next:nb?(nb.id||String(nb.className)).slice(0,20):null,nextOk:nbOk,upOk,fold:document.body.classList.contains('fold')}}"""


def b6(br, eng, app):
    out = {}; ok = True
    for subj in ('phys', 'earth', 'bio'):
        dv = Dev(br, eng, {'width': 390, 'height': 844}, mobile=True).load(app, SPD, subj, rec={'earth/기록.json': rec_old()} if subj == 'earth' else {})
        try:
            x = dv.ev(FOLDJS)
            if not x:
                out[subj] = '단추 없음'; ok = False; continue
            f0 = x['fold']; b = x['btn']
            dv.tap(b['l'] + b['w'] / 2, b['t'] + b['h'] / 2)
            QC.until(dv.pg, "f=>document.body.classList.contains('fold')!==f", 5000, 'revfix0929 b6 톡 가운데 → 접힘 바뀜(_task_qa_fix1 §A-3 · tap 안 고정 500ms 뒤 · 안 바뀌면 상한 뒤 그대로 잼)', arg=f0)
            f1 = dv.ev("()=>document.body.classList.contains('fold')")
            hx = x['hit']['r'] - 2; hy = (x['hit']['t'] + x['hit']['b']) / 2   # 누름 자리 오른쪽 끝(보이는 원 밖)
            x2 = dv.ev(FOLDJS)
            dv.tap(hx, hy)
            QC.until(dv.pg, "f=>document.body.classList.contains('fold')!==f", 5000, 'revfix0929 b6 톡 누름 자리 끝 → 접힘 바뀜(_task_qa_fix1 §A-3 · tap 안 고정 500ms 뒤)', arg=f1)
            f2 = dv.ev("()=>document.body.classList.contains('fold')")
            x['톡 가운데'] = [f0, f1]; x['톡 누름 자리 끝(%.0f,%.0f)' % (hx, hy)] = [x2['fold'] if x2 else None, f2]
            out[subj] = x
            ok = ok and x['grip'] is not None and b['l'] >= x['grip']['r'] and x['hit']['w'] >= 36 and x['hit']['h'] >= 36 and x['onGrip'] == 0 \
                and x['nextOk'] is not False and x['upOk'] is not False and f1 != f0 and f2 != f1
        finally:
            dv.close()
    return bool(ok), out


# ══════════ B-7 히트맵 갈래 칩 ══════════
def b7(br, eng, app):
    out = {}
    HEAT = "()=>document.querySelectorAll('#spec i[title]').length"
    CH = "()=>[...document.querySelectorAll('#eKind button')].map(b=>({t:__R9.tx(b),on:b.classList.contains('on'),r:__R9.R(b)}))"
    for subj in ('bio', 'earth'):
        dv = Dev(br, eng).load(app, SPD, subj, rec={'earth/기록.json': rec_old()} if subj == 'earth' else {})
        try:
            ch = dv.ev(CH); o = {'칩': [c['t'] for c in ch], '처음 켜짐': [c['t'] for c in ch if c['on']], '히트맵 처음': dv.ev(HEAT), '누름': []}
            for i in range(len(ch)):
                c = dv.ev(CH)[i]; r = c['r']
                dv.pg.mouse.click(r['l'] + r['w'] / 2, r['t'] + r['h'] / 2); dv.pg.wait_for_timeout(500)
                o['누름'].append({'칩': c['t'], '히트맵 칸': dv.ev(HEAT), '켜짐': [z['t'] for z in dv.ev(CH) if z['on']],
                                 'FL.types': dv.ev("()=>FL.types?[...FL.types].join(''):''"), 'FL.past': dv.ev("()=>FL.past")})
            out[subj] = o
        finally:
            dv.close()
    num = lambda t: int(re.sub(r'\D', '', t) or -1)
    bio = out['bio']; ea = out['earth']
    ok = bio['칩'] == ['기출 270', '타기출 342', '예상 134'] and all(p['히트맵 칸'] == num(p['칩']) for p in bio['누름']) \
        and ea['칩'] == ['기출 319', '확인문제 385'] and all(p['히트맵 칸'] == num(p['칩']) for p in ea['누름'])
    return bool(ok), out


# ══════════ B-8 화면 훑기(규칙 60) ══════════
SWEEPJS = r"""(touch)=>{const vw=innerWidth,vh=innerHeight,de=document.documentElement;
 const ACT='button,a[href],input,select,textarea,[onclick],[data-esq],[data-big],[data-past],[data-kind],.chip,.chchip,.ndrow,.item';
 const sig=e=>{let s=e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(e.classList.length?'.'+[...e.classList].slice(0,2).join('.'):'');
   const t=(e.textContent||'').replace(/\s+/g,' ').trim().replace(/\d+/g,'#').slice(0,14);
   return s+((e.tagName==='BUTTON'||e.classList.contains('chip')||e.classList.contains('chchip'))?'「'+t+'」':'')};
 const els=[...document.querySelectorAll(ACT)].filter(e=>{if(!__R9.vis(e))return false;const r=e.getBoundingClientRect();return r.bottom>0&&r.right>0&&r.top<vh&&r.left<vw});
 const over=[],clip=[],cover=[],small=[];
 for(const e of els){const r=e.getBoundingClientRect();
   if(r.right>vw+1)over.push(sig(e));
   let a=e.parentElement;while(a&&a!==document.body){const cs=getComputedStyle(a);if(/(hidden|clip|auto|scroll)/.test(cs.overflowX)){const ar=a.getBoundingClientRect();if(r.right>ar.right+1||r.left<ar.left-1)clip.push(sig(e));break}a=a.parentElement}
   const cx=Math.min(vw-1,Math.max(0,r.left+r.width/2)),cy=Math.min(vh-1,Math.max(0,r.top+r.height/2)),at=document.elementFromPoint(cx,cy);
   if(at&&!(at===e||e.contains(at)||at.contains(e)))cover.push(sig(e));
   if(Math.min(r.width,r.height)<(touch?24:14))small.push(sig(e))}
 const c=document.getElementById('card'),w=document.getElementById('cardwrap');
 return {docow:de.scrollWidth-de.clientWidth,n:els.length,over,clip,cover,small,card:(c&&w&&__R9.vis(w))?{tf:c.style.transform,w:Math.round(c.getBoundingClientRect().width),wrap:w.clientWidth}:null}}"""
VPS = [('PC', {'width': 1440, 'height': 900}, False), ('폰', {'width': 390, 'height': 844}, True), ('iPad', {'width': 820, 'height': 1180}, False)]
SW_Q = {'bio': ('DNA', 'B20-57-05'), 'earth': ('맨틀', 'G03-40-05'), 'phys': ('속력', None)}
# 뜻한 바뀜(새 판에만 있는 신호가 결함이 아님) — 신호 → 까닭
# 히트맵 머리 줄(#eKind)은 목록·검색 결과·문항 창 뒤에도 보인다 → 칸 「*」 = 그 과목 모든 화면
ACCEPT = {('bio', '*', 'button.chchip「타기출 #」'): 'A-7 생물 갈래 칩 — 바탕 「확인문제 0」 자리에 둘(타기출 · 예상) · 바탕 「기출」·「확인문제」 칩과 같은 chchip 꼴·크기(작은 누름·창 뒤 덮임도 바탕 칩과 같음)',
          ('bio', '*', 'button.chchip「예상 #」'): 'A-7 생물 갈래 칩 — 같은 chchip 꼴·크기'}


# ★ 2026-10-07 (_task_jagwa_phys_win §A-15 ⑧ · §A-33 · §A-27 ⑯㉝) — 같은 단추의 글자만 바뀐 신호(#vBack 「서재」→「✕」 · #tCard 「암기카드」→「🃏」 · #tAns 「정답 ▸」→「답풀」)
#   는 새 판 신호를 옛 글자로 맞춰 센다(새로 생긴 것으로 안 셈 · 그 단추의 넘침·잘림·덮임·작은 자리는 그대로 잰다 · 옛 판끼리는 안 탐)
_REN = {'button#vBack.iconbtn「✕」': 'button#vBack.iconbtn「서재」',
        'button#tCard.tl.wide「🃏」': 'button#tCard.tl.wide「암기카드」',
        'button#tAns.tl.wide「답풀」': 'button#tAns.tl.wide「정답 ▸」'}


def _ren(s):
    return _REN.get(s, s)


def accepted(subj, scr, sig):
    return ACCEPT.get((subj, scr, sig)) or ACCEPT.get((subj, '*', sig))


def sweep(br, eng, app):
    out = {}
    for vn, vp, mob in VPS:
        touch = vn != 'PC'
        for subj in ('bio', 'earth', 'phys'):
            dv = Dev(br, eng, vp, mobile=mob).load(app, SPD, subj, rec={'earth/기록.json': rec_old()} if subj == 'earth' else {})
            try:
                out[(vn, subj, '목록')] = dv.ev(SWEEPJS, touch)
                if dv.ev("()=>document.body.classList.contains('fold')&&!!document.getElementById('fFoldBtn')"):
                    b = dv.ev("()=>__R9.R(document.getElementById('fFoldBtn'))")
                    if b and b['w']:
                        dv.tap(b['l'] + b['w'] / 2, b['t'] + b['h'] / 2)
                if dv.ev("()=>{const s=document.getElementById('spec');return !!s&&!__R9.vis(s)}"):
                    dv.ev("()=>{const t=document.getElementById('hmTg');if(t)t.click()}"); dv.pg.wait_for_timeout(400)
                out[(vn, subj, '히트맵')] = dv.ev(SWEEPJS, touch)
                typeq(dv, SW_Q[subj][0])
                out[(vn, subj, '검색 결과')] = dv.ev(SWEEPJS, touch)
                typeq(dv, '')
                cd = SW_Q[subj][1]
                no = dv.ev("c=>__R9.noOf(c)", cd) if cd else dv.ev("()=>DATA[0][F.NO]")
                dv.ev("n=>__R9.open(n)", no)
                out[(vn, subj, '문항 창')] = dv.ev(SWEEPJS, touch)
                out[(vn, subj, '오류')] = dv.errs[:2]
            finally:
                dv.close()
    return out


def sweep_cmp(N, Bs):
    """새 판에만 있는 신호(넘침·잘림·덮임·작은 누름 자리) — 칸마다 여러 벌 셈의 차"""
    import collections
    rows, newonly, acc = [], [], []
    for key in N:
        if key[2] == '오류':
            continue
        n, b = N[key], Bs.get(key) or {}
        line = {'칸': '%s · %s · %s' % key, '쪽 넘침': [n['docow'], b.get('docow')]}
        for cat in ('over', 'clip', 'cover', 'small'):
            # 옛: cn, cb = collections.Counter(n[cat]), collections.Counter(b.get(cat) or [])
            cn, cb = collections.Counter(_ren(s) for s in n[cat]), collections.Counter(b.get(cat) or [])   # ★ 2026-10-07 (_task_jagwa_phys_win §A-15 · §A-33 · §A-27) — 글자만 바뀐 단추는 옛 글자로(_REN)
            d = cn - cb
            line[cat] = [len(n[cat]), len(b.get(cat) or [])]
            for s, k in d.items():
                why = accepted(key[1], key[2], s)
                (acc if why else newonly).append({'칸': line['칸'], '종류': cat, '신호': s, '수': k, **({'까닭': why} if why else {})})
        if n['docow'] > (b.get('docow') or 0):
            newonly.append({'칸': line['칸'], '종류': '쪽 넘침', '신호': '%d > %d' % (n['docow'], b.get('docow') or 0)})
        if n.get('card') or b.get('card'):
            line['카드'] = [n.get('card'), b.get('card')]
        rows.append(line)
    return rows, newonly, acc


# ══════════ 돌림 ══════════
GATES = [
    ('b1', 'B-1 A-1 옛 판 기기가 원격에서 지워진 crop|G47-07 값을 가진 채 새 판 → 새 열쇠 칸 0 · PUT 0 · gone[crop|G10-47-07] · 멱등(두 번째 옮김 0 · 바이트 같음)', b1a, 'fix'),
    ('b1', 'B-1 A-1 반대 — 도장이 묘비보다 새로우면 옮김', b1b, 'keep'),
    ('b1', 'B-1 A-1-1 이미 받은 옛 열쇠 묘비 → 새 열쇠에 같은 시각(옛 묘비 그대로)', b1c, 'fix'),
    ('b1', 'B-1 안전 — 이미 옮긴 원격(origin/main) 빈 기기: 새 칸 값 하나도 안 지움 · 옮김 묘비를 새 칸에 안 비춤', b1d, 'keep'),
    ('b2', 'B-2 A-2 빈 기기 첫 PUT — 옛 열쇠 0 · u 옛 0 · 옛 묘비 = 옮긴 칸 + 원래 · 차례 옮김 끝 → PUT', b2, 'fix'),
    ('b3', 'B-3 A-3 검색 — 지학 「맨틀」 42 · 표시 없는 줄 0 · G03-40-05 💬 본문 + mark · 생물 「DNA」 표시 없는 줄 0 · 「오답해설」 ⏎ 0 · 「자료해석 2탄」 1', b3, 'fix'),
    ('b4', 'B-4 A-4 폰 390 문항 창 카드 — 세 과목 표본 셋 · 창·펼친 해설·전체 화면 · 카드 right ≤ 틀 안쪽 right · 좌우 여백 같음 · 단추 elementFromPoint = 제 단추', b4, 'fix'),
    ('b5', 'B-5 A-5 서랍 줄 「번호 · 출처」 · 「-」로 붙은 줄 0(세 과목)', b5, 'fix'),
    ('b6', 'B-6 A-6 폰 ▾ — 손잡이 오른쪽 · 누름 자리 ≥ 36×36 · 손잡이·이웃 안 덮음 · 손가락 톡(가운데 · 누름 자리 끝) = 접힘/펼침(세 과목)', b6, 'fix'),
    ('b7', 'B-7 A-7 히트맵 갈래 칩 — 생물 270 · 342 · 134 · 누르면 히트맵 칸 = 그 수 · 지학 319 · 385 무변', b7, 'fix'),
]


def main():
    if QC.SMOKE:   # smoke — 이 하네스엔 smoke 칸이 없다(A-0 처리표 · _task_qa_slim2) · 앱을 띄우기 전에 끝낸다(결과 파일에도 같은 줄)
        print('INFO | smoke 칸 없음')
        with io.open(OUTF, 'a', encoding='utf-8') as f:
            f.write('\n==== %s · jagwa_revfix0929 · smoke ====\nINFO | smoke 칸 없음\n' % time.strftime('%Y-%m-%d %H:%M'))
        return
    APPS['NEW'] = app_src(NEWF)
    if QC.GATE:
        QC.sub('git:show-app')
        APPS['BASE'] = app_src(BASEF)
    base_rev = BASEF if not os.path.isfile(BASEF) else os.path.basename(BASEF)
    if QC.GATE:
        try:
            base_rev = JG.git_HU(GENIE, 'rev-parse', '--short', BASEF).decode().strip() or base_rev
        except Exception:
            pass
    else:
        base_rev = '(regress — 바탕 안 띄움 · 기준 = 스냅샷)'
    t0 = time.time(); TIMES = []
    lit = literal_rule() if QC.GATE else None   # INFO(글자 그대로 규칙) = 관문만 — origin/main git show 로만 재고 그 판(옮김 규칙을 정한 판)에만 뜻
    if lit:
        print('INFO | 글자 그대로 규칙(모든 옛 묘비 → 새 열쇠 max)이면 origin/main 원격에서 지워질 새 칸 값 | %s' % json.dumps(lit, ensure_ascii=False))
    with sync_playwright() as pw:
        for eng in ENGS:
            br = getattr(pw, eng).launch()
            try:
                for g, name, fn, kind in GATES:
                    if not want(g):
                        continue
                    ts = time.time()
                    res = {}
                    for who in (('NEW', 'BASE') if QC.GATE else ('NEW',)):   # regress — 바탕 열(헛잣대 · 판정 밖)은 안 잰다 → 「바탕 —」
                        try:
                            res[who] = fn(br, eng, APPS[who])
                        except Exception as e:
                            res[who] = (False, 'ERR ' + repr(e)[:400])
                    R(g, eng, name + ('  [바탕 = 기준]' if kind == 'keep' else ''), res['NEW'][0], res['BASE'][0] if QC.GATE else None,
                      {'NEW': res['NEW'][1], 'BASE': res['BASE'][1]} if QC.GATE else {'NEW': res['NEW'][1]})
                    TIMES.append((g, name[:40], round(time.time() - ts)))
                if want('b3'):
                    ts = time.time()
                    if QC.GATE:
                        pn, pb = b3p(br, eng, APPS['NEW']), b3p(br, eng, APPS['BASE'])
                        # ★ physprev(10/2 하위 에이전트 C) — _task_jagwa_physprev 57줄(A-2-3): 물리 t 로만 걸린 줄 · 조각이 t 인 줄 · 100줄 상한은 pv_same 이 가른다
                        cmp = {q: pv_same(pn.get(q), pb[q]) for q in pb}
                    else:   # regress — 기준 칸: 바탕 = 앞 인도판 NEW 결과 스냅샷(말마다 · 줄 HTML md5) · pv_same 그대로(뜻한 차 = 미리보기 t · 제목 tt)
                        pn = b3p(br, eng, APPS['NEW'])
                        pb = {q: QC.base(_rg_cid(eng, 'b3p', q), _rg_pv(pn[q])) for q in pn}
                        cmp = {q: pv_same(QC.norm(_rg_pv(pn[q])), pb[q]) for q in pb}
                    diff = [q for q in pb if not cmp[q][0]]
                    R('b3', eng, 'B-3 A-3-4 물리 %d말 — 걸린 집합 · 결과 상자 HTML = 바탕(무변)  [바탕 = 기준]' % len(pb), not diff and len(pb) >= 15, None,
                      {'말': list(pb), '다른 말': diff, '건': {q: len((pn.get(q) or {}).get('nos') or []) for q in pn}, 'physprev': {q: v[1] for q, v in cmp.items() if v[1]}} if QC.GATE else
                      {'말': list(pb), '다른 말': diff, '건': {q: len((pn.get(q) or {}).get('nos') or []) for q in pn}, 'physprev': {q: v[1] for q, v in cmp.items() if v[1]},
                       '기준': sorted({QC.base_note(_rg_cid(eng, 'b3p', q)) for q in pb})})
                    TIMES.append(('b3', '물리 말', round(time.time() - ts)))
                if want('b8'):
                    ts = time.time()
                    if QC.GATE:
                        sn, sb = sweep(br, eng, APPS['NEW']), sweep(br, eng, APPS['BASE'])
                    else:   # regress — 기준 칸: 바탕 훑기 = 앞 인도판 NEW 훑기 스냅샷(기기 · 과목 · 화면마다 신호 목록) · 이름 맞춤(_ren)은 두 쪽 다
                        sn = sweep(br, eng, APPS['NEW'])
                        sb = {k: _rg_ren_sig(QC.base(_rg_cid(eng, 'b8', *k), v)) for k, v in sn.items() if k[2] != '오류'}
                    rows, newonly, acc = sweep_cmp(sn, sb)
                    errs = {('%s · %s' % (k[0], k[1])): v for k, v in sn.items() if k[2] == '오류' and v}
                    R('b8', eng, 'B-8 화면 훑기 — 서재 목록·히트맵·검색 결과·문항 창 × PC 1440 · 폰 390 · iPad 820 × 세 과목 — 새로 생긴 넘침·잘림·덮임·작은 누름 자리 0',
                      not newonly and not errs, None, {'새로 생긴 것': newonly, '뜻한 바뀜': acc, '오류': errs, '표': rows} if QC.GATE else
                      {'새로 생긴 것': newonly, '뜻한 바뀜': acc, '오류': errs, '표': rows, '기준': sorted({QC.base_note(_rg_cid(eng, 'b8', *k)) for k in sn if k[2] != '오류'})})
                    TIMES.append(('b8', '화면 훑기', round(time.time() - ts)))
            finally:
                br.close()
    npass = sum(1 for r in ROWS if r[3]); nfail = sum(1 for r in ROWS if not r[3])
    vac = [r for r in ROWS if r[4] is True and '기준' not in r[2]]
    print('\n== PASS %d · FAIL %d · 헛잣대(바탕도 PASS · 기준 칸 밖) %d · %.0f초' % (npass, nfail, len(vac), time.time() - t0))
    print('단계 초: ' + ' · '.join('%s %s %ds' % t for t in TIMES))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · jagwa_revfix0929 · NEW %s · 바탕 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), os.path.basename(NEWF), base_rev, ','.join(ENGS)))
        if lit:
            f.write('INFO | 글자 그대로 규칙이면 지워질 새 칸 값 | %s\n' % json.dumps(lit, ensure_ascii=False))
        for g, eng, n, okn, okb, v in ROWS:
            f.write('%s | 바탕 %s | %s · %s · %s | %s\n' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, eng, n,
                    (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str))[:40000]))
        f.write('== PASS %d · FAIL %d · 헛잣대 %d · 단계 초 %s\n' % (npass, nfail, len(vac), TIMES))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
