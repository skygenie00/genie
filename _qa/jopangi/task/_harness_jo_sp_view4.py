# -*- coding: utf-8 -*-
r"""_task_jo_sp_view4_cloudD §C 관문 — 상표 1차객 책 카드(뷰객 4판) 앱 · 시험 데이터(_fx_sp_view4 · 지어낸 글)

  python _harness_jo_sp_view4.py [--new <앱 파일 | genie git 판>] [--base <판>] [--fx <시험 데이터 폴더>] [--eng chromium,webkit] [--only C1,C2-3,..] [--res <결과(기본 = 임시 폴더)>] [--yardstick] [--vendor <pdf.js>] [--exam <시험지 폴더>]

  본판 §E-3(앱) · add1 §B · add2 §B 1~6 · cloudD §C-2 를 시험 데이터로 잰다.
  시험 데이터 = 같은 폴더 _fx_sp_view4/(jimun_상표_뷰객.json · mokcha_상표.json · 표장 그림 webp) — add3 §B 꼴 · 책 글 0(D11).
    하네스가 jo/data 요청을 덧판(jo/data 링크 + 시험 파일 둘)으로 돌린다 · 표장 그림 = 가짜 원격(studyplandata jopangi/img_map.json · jopangi/img/)
  NEW = 이 판 앱(기본 genie jo/index.html) · BASE = 바탕 main 83c230f · --yardstick 이면 BASE 를 NEW 자리에 넣어 칸마다 FAIL 해야 통과(헛잣대 = 83c230f + 같은 시험 데이터)
  도구 = 같은 폴더 _harness_jo_revfix0929b(서버 · SEED · __RB 도구 · 기기 흉내 · 터치)
  자리 = _roots(GENIE_ROOT) — 클라우드: GENIE_ROOT=<genie 클론>
  WebKit = 터치 칸(C3 같은 uid 쌍 손가락 풀이)만 · 이 컴퓨터에 WebKit 이 없으면 「안 잼」
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import base64, hashlib, json, os, re, shutil, subprocess, sys, tempfile, threading, time, urllib.parse   # noqa: E402
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEW = ARG('--new', _roots.genie('jo', 'index.html'))
BASE = ARG('--base', '83c230f')
YARD = '--yardstick' in sys.argv
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
OUTF = ARG('--res', os.path.join(tempfile.gettempdir(), 'h_jospv4', '_harness_jo_sp_view4_result.txt'))   # 기본 = 임시 폴더(_qa 에 결과를 쓰지 않는다)
FX = ARG('--fx', os.path.join(HERE, '_fx_sp_view4'))
DATA0 = ARG('--data', _roots.genie('jo', 'data'))
TMP0 = os.path.join(tempfile.gettempdir(), 'h_jospv4')
TMP = os.path.join(TMP0, 'p%d' % os.getpid())
_argv = sys.argv
sys.argv = [sys.argv[0], '--new', NEW] + [x for k in ('--exam', '--vendor') if k in _argv for x in (k, _argv[_argv.index(k) + 1])]
sys.path.insert(0, HERE)
import _harness_jo_revfix0929b as H   # noqa: E402
sys.argv = _argv
T, N, RES = H.T, H.N, H.RES
PC, PHONE, PAD = (1440, 900), H.PHONE, H.PAD
DEVS = (('폰390', PHONE), ('iPad834', PAD), ('PC1440', PC))


def git(*a):
    return subprocess.run(['git', '-C', _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


# ════════════════════════ 덧판 — jo/data 링크 + 시험 파일 ════════════════════════
FX_FILES = ('jimun_상표_뷰객.json', 'mokcha_상표.json')
IMG_NAME = 'v4_B2-S18_1.webp'


def _ln(src, dst):
    try:
        os.symlink(src, dst)
    except OSError:
        if os.name != 'nt':
            raise
        if os.path.isdir(src):   # ★ 10/3 로컬(사용자 허용) — 윈도 symlink 권한 없음(WinError 1314) · 폴더(jo/data/omr)는 파일마다 hard link 로(안 되면 복사) · copy2 는 폴더를 못 연다
            try:
                shutil.copytree(src, dst, copy_function=os.link)
            except OSError:
                shutil.copytree(src, dst, dirs_exist_ok=True)
            return
        try:
            os.link(src, dst)
        except OSError:
            shutil.copy2(src, dst)


def build_data():
    d = os.path.join(TMP, 'data')
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for x in os.listdir(DATA0):
        if x in FX_FILES:
            continue
        _ln(os.path.join(DATA0, x), os.path.join(d, x))
    for x in FX_FILES:
        _ln(os.path.join(FX, x), os.path.join(d, x))
    return d


DATA = build_data()
FXJ = json.load(open(os.path.join(FX, FX_FILES[0]), encoding='utf-8'))
FXM = json.load(open(os.path.join(FX, FX_FILES[1]), encoding='utf-8'))
JMS = json.load(open(os.path.join(DATA0, 'jimun_상표.json'), encoding='utf-8'))
IMG = open(os.path.join(FX, IMG_NAME), 'rb').read()
IMG_P = 'jopangi/img/%s.webp' % hashlib.sha1(IMG).hexdigest()[:16]
IMG_MAP = {IMG_NAME: {'p': IMG_P, 'w': 240, 'h': 60, 'bytes': len(IMG)}}


# ════════════════════════ 가짜 원격(기록 · 그림) ════════════════════════
class Remote:
    def __init__(self):
        self.files, self.lock = {}, threading.Lock()
        self.clear()

    def clear(self):
        with self.lock:
            self.files = {'jopangi/img_map.json': json.dumps(IMG_MAP, ensure_ascii=False).encode('utf-8'), IMG_P: IMG}


REMOTE = Remote()
SEED_REC = r"""
 var sp=s.indexOf('api.github.com/repos/zzikkaplan/studyplandata/contents/');
 if(sp>=0){var rest2=s.slice(sp+'api.github.com/repos/zzikkaplan/studyplandata/contents/'.length).split('?')[0];
  var h2={};try{var hh=o.headers;var ac=hh&&(typeof hh.get==='function'?hh.get('Accept'):(hh.Accept||hh.accept));if(ac)h2['Accept']=ac;}catch(e){}
  if(o.body)h2['Content-Type']='application/json';
  return nf(location.origin+'/__rec/'+rest2,{method:o.method||'GET',headers:h2,body:o.body});}
"""
_anchor = " if(/cdnjs\\.cloudflare\\.com"
if SEED_REC not in H.SEED:
    assert _anchor in H.SEED, 'revfix0929b SEED 모양이 바뀌었다'
    H.SEED = H.SEED.replace(_anchor, SEED_REC + _anchor, 1)
SERVERS = {}
DATA_FOR = {}   # tag → 덧판(2025 정답 칸 시험 등 · 없으면 DATA)


def serve_sv(tag, src):
    if tag in SERVERS:
        return SERVERS[tag][1]
    body = H.inject(src).encode('utf-8')

    class Hd(SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, data, ct='application/json'):
            self.send_response(code)
            self.send_header('Content-Type', ct)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            p = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
            if p in ('/jo/', '/jo/index.html'):
                return self._send(200, body, 'text/html; charset=utf-8')
            if p.startswith('/__rec/'):
                k = p[len('/__rec/'):]
                with REMOTE.lock:
                    b = REMOTE.files.get(k)
                if b is None:
                    return self._send(404, b'{"message":"Not Found"}')
                if 'raw' in (self.headers.get('Accept') or ''):
                    return self._send(200, b, 'application/octet-stream')
                return self._send(200, json.dumps({'sha': hashlib.sha1(b).hexdigest(), 'size': len(b)}).encode())
            return super().do_GET()

        def do_PUT(self):
            p = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
            if not p.startswith('/__rec/'):
                return self._send(405, b'{}')
            k = p[len('/__rec/'):]
            n = int(self.headers.get('Content-Length') or 0)
            try:
                j = json.loads(self.rfile.read(n).decode('utf-8') or '{}')
                data = base64.b64decode(j.get('content', ''))
            except Exception:
                return self._send(422, b'{}')
            with REMOTE.lock:
                REMOTE.files[k] = data
            return self._send(200, json.dumps({'content': {'sha': hashlib.sha1(data).hexdigest()}}).encode())

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
            for pre, root in (('/jo/data/', DATA_FOR.get(tag, DATA)), ('/gichul/pdf/', H.EXAM)):
                if p.startswith(pre):
                    return os.path.join(root, *[x for x in p[len(pre):].split('/') if x])
            if p.startswith('/__vendor/'):
                parts = [x for x in p[len('/__vendor/'):].split('/') if x]
                f = os.path.join(H.VENDOR, *parts)
                return f if os.path.exists(f) else os.path.join(H.VENDOR, 'build', *parts)
            return os.path.join(HERE, '__없음__')

    srv = ThreadingHTTPServer(('127.0.0.1', 0), Hd)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


H.serve = serve_sv


# ════════════════════════ 기대값(시험 데이터에서) ════════════════════════
ROWS = FXJ['지문']
OBJS = FXJ.get('객관식', [])
ROWBY = {r['id']: r for r in ROWS}
ROWBY.update({o['id']: o for o in OBJS})
MD = FXM['마디']
UNIT_OF = {}
for _i, _n in enumerate(MD):
    for _x in _n['지문']:
        UNIT_OF.setdefault(_x, _i)
LEAVES = [i for i, n in enumerate(MD) if n['지문'] or n['리담']]
UIDN = {}
for _r in ROWS:
    UIDN.setdefault(_r['uid'], []).append(_r['id'])
PAIRS = [(u, ids) for u, ids in UIDN.items() if len(ids) > 1]   # 같은 uid 쌍(배지 OX ↔ 같은 글 객관식 선지)
JMQ = {q['id']: q for q in JMS['문제']}
PLS = json.load(open(os.path.join(DATA0, 'prec_상표_리스트.json'), encoding='utf-8'))
PAN_IN = {str(p.get('사건번호') or p.get('id') or '').replace(' ', ''): p for p in PLS.get('판례', [])}
JOS_S = {x['k'] for x in json.load(open(os.path.join(DATA0, 'jo_상표법_목록.json'), encoding='utf-8'))['조']}


def lab_of(i):
    n = MD[i]
    return ((n['no'] + ('. ' if n['깊이'] == 1 else ' ')) if n.get('no') else '') + n['제목']


def kp(r):
    return r.get('uid') or ('P7:' + r['id'])


def dom_of(r):
    return 'qb-' + kp(r)


def rail_expect():
    """서랍(레일) 1차객 문제 수 = 리담 지문 + 책 O/X 지문 · uid 한 번(같은 uid 쌍 = 한 문제)"""
    ks, n = set(), 0
    for q in JMS['문제']:
        for z in q.get('지문', []):
            if z.get('병합'):
                continue
            u = z.get('uid')
            if not (u and u in ks):
                n += 1
            if u:
                ks.add(u)
    for z in ROWS:
        if z.get('ox') in ('O', 'X'):
            u = z.get('uid')
            if not (u and u in ks):
                n += 1
                if u:
                    ks.add(u)
    return n


OTHER_LAW = ('특허법', '디자인보호법', '민법', '부정경쟁방지법', '실용신안법')


def jo_expect(sol):
    """해설 글이 가리키는 상표법 조(add1 §A-1 규칙을 하네스가 따로 셈) — 「상표법 제N조」·법 이름 없는 「제N조」·「法N」 · 다른 법 이름 바로 뒤 조 = 뺌"""
    s, out = str(sol or ''), []
    for m in re.finditer(r'法\s*(\d+)', s):
        k = '제%s조' % m.group(1)
        if k not in out:
            out.append(k)
    for m in re.finditer(r'제\s?(\d+)조(?:의\s?(\d+))?', s):
        pre = s[max(0, m.start() - 9):m.start()]
        if any(re.search(re.escape(L) + r'\s*$', pre) for L in OTHER_LAW):
            continue
        k = '제%s조' % m.group(1) + ('의%s' % m.group(2) if m.group(2) else '')
        if k in JOS_S and k not in out:
            out.append(k)
    return out


def pan_expect(sol):
    return re.findall(r'(\d{2,4}\s?(?:재후|재다|카허|후|허|다|도|므|두|마)\s?\d{1,6})', str(sol or ''))


# ════════════════════════ 쪽 도구(앱 위 · 두 판 공통 이름만) ════════════════════════
SV_JS = r"""() => { if (window.__SV) return 1;
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const R = e => { const r = e.getBoundingClientRect(); return { l: r.left, r: r.right, t: r.top, b: r.bottom, w: r.width, h: r.height, cx: r.left + r.width / 2, cy: r.top + r.height / 2 }; };
function card(c){ const hd = c.querySelector('.mbqhd'); const q = s => hd ? hd.querySelector(s) : null; const box = c.closest('.p7case'); const im = c.querySelector('.vimg-img');
  return { id: c.id, src: txt(q(':scope > .qb.v:not(.qexp)') || q('.l > .qb.v')), ty: txt(hd && hd.querySelector('.mbtype .seg.ty')), tycls: ((hd && hd.querySelector('.mbtype')) || {}).className || '',
    tyjo: hd ? [...hd.querySelectorAll('.mbtype .seg.jo')].map(txt) : [], ed: txt(q(':scope > .qb.v.qexp')), bk: txt(q(':scope > .qb.id.mbbk')), uidc: txt(q(':scope > .qb.id:not(.mbbk)')),
    lab: txt(c.querySelector('.mbqlab')), box: !!box, bh: box ? txt(box.querySelector('.p7cash')) : '', c2: [...c.querySelectorAll('.c2jb')].map(txt), pan: [...c.querySelectorAll('.cfpan')].map(txt),
    hd: txt(hd), hasH7: [...c.querySelectorAll('.qb, .qpc1')].some(x => /^H[78]$/.test(txt(x))), img: im ? Object.assign(R(im), { nw: im.naturalWidth }) : null, vimg: !!c.querySelector('.vimg'),
    tx: txt(c.querySelector('.mbqtx')), txR: c.querySelector('.mbqtx') ? R(c.querySelector('.mbqtx')) : null, star: !!(hd && [...hd.querySelectorAll('.qtag.on')].some(x => txt(x) === '⭐')),
    pick: [...c.querySelectorAll('.mboxb.sel')].map(txt) }; }
window.__SV = {
  cards: () => [...document.querySelectorAll('#slot .qwrap')].map(card),
  nav: async (law, mok, gk, flt) => { if (law) S.law = law; S.tab = 'jimun'; S.jimunTab = 'ox'; S.oxQueue = ''; if (gk) UZGK = gk; if (flt != null) S.oxFilter = flt; S.mok = mok; S.oxPage = null;
    try{ closeAllPops(); }catch(e){} await render(); const sl = document.querySelector('#slot');
    return { law: S.law, mok: S.mok, n: document.querySelectorAll('#slot .qwrap').length, bad: !!sl && /읽지 못했다/.test(sl.innerText || '') }; },
  allCards: async () => { const out = []; const pg = new Set(Object.values(typeof OXDOMPG !== 'undefined' && OXDOMPG || {})); const n = Math.max(1, pg.size);
    for (let i = 0; i < n; i++){ if (n > 1){ S.oxPage = i; await render(); } out.push(...__SV.cards()); } return out; },
  wrap: () => { if (window.__PJ) return; window.__PJ = []; window.__PP = []; const o = popJo, o2 = popPan;
    window.popJo = function(law, k){ __PJ.push([law, k]); return o.apply(this, arguments); };
    window.popPan = function(c){ __PP.push(String(c)); return o2.apply(this, arguments); }; },
  rect: sel => { const e = document.querySelector(sel); if (!e) return null; e.scrollIntoView({ block: 'center' }); const r = R(e); const at = document.elementFromPoint(r.cx, r.cy); return Object.assign(r, { on: !!at && (at === e || e.contains(at)) }); },
  pops: () => (typeof POPS !== 'undefined' ? POPS : []).map(p => ({ k: p._pk || '', t: txt(p).slice(0, 400), r: R(p) })),
  txt: txt
};
return 1; }"""


def sv(p):
    p.ev(SV_JS)


def nav(p, law, mok, gk=None, flt=None):
    sv(p)
    r = p.ev("([a,b,c,d]) => __SV.nav(a,b,c,d)", [law, mok, gk, flt])
    p.idle(200)
    return r


def all_cards(p):
    sv(p)
    return p.ev("() => __SV.allCards()")


def open_pg(br, src, dev=PC, tag='x', ls=None):
    REMOTE.clear()   # 새 쪽 = 새 기기 — 가짜 원격(기록 동기화)을 비워 앞 칸 쪽이 올린 기록이 섞이지 않게
    p = H.dev_page(br, tag, src, dev, ls=ls)
    sv(p)
    return p


def press_sel(p, sel, wait=500):
    sv(p)
    r = p.ev("(s) => __SV.rect(s)", sel)
    if not r or not r.get('on'):
        return False
    (p.tap if p.touch else p.click)(r['cx'], r['cy'], wait)
    p.idle(150)
    return True


def go_law_click(p, short):
    """머리 법 칩을 손으로 누른다"""
    r = p.ev("(t) => { const b = [...document.querySelectorAll('#laws .pill')].find(x => x.textContent === t); if (!b) return null; b.scrollIntoView({block:'center'}); const q = b.getBoundingClientRect(); return {cx: q.left + q.width/2, cy: q.top + q.height/2}; }", short)
    if not r:
        return False
    (p.tap if p.touch else p.click)(r['cx'], r['cy'], 900)
    p.idle(300)
    return True


def go_tab_jimun(p):
    r = p.ev("() => { const b = [...document.querySelectorAll('#hrail .rb')].find(x => x.querySelector('b[data-n=jimun]')); if (!b) return null; b.scrollIntoView({block:'nearest', inline:'center'}); const q = b.getBoundingClientRect(); return {cx: q.left + q.width/2, cy: q.top + q.height/2, on: b.classList.contains('on')}; }")
    if not r:
        return False
    if not r['on']:
        (p.tap if p.touch else p.click)(r['cx'], r['cy'], 900)
        p.idle(300)
    return True


def go_saeng(p):
    """상표 · 1차객 첫 화면(손으로: 법 칩 → 1차객 탭)"""
    go_law_click(p, '상표')
    go_tab_jimun(p)
    p.ev("async () => { if (S.jimunTab !== 'ox' || S.mok || S.oxQueue){ S.jimunTab = 'ox'; S.mok = null; S.oxQueue = ''; await render(); } }")
    p.idle(400)


def drawer_rows(p):
    return p.ev("() => [...document.querySelectorAll('#jtlist > *')].map(e => ({ c: e.className, t: ((e.querySelector('.jtnm') || e.querySelector('.l1 .tx') || e.querySelector(':scope > span')) || e).textContent.replace(/\\s+/g, ' ').trim(), n: ((e.querySelector('.n')) || {}).textContent || '' }))")


def card_row_map(i, cards):
    """마디 i 화면의 카드 → 책 줄 id(같은 uid 쌍은 마디로 가린다)"""
    want = {}
    for x in MD[i]['지문']:
        want.setdefault(dom_of(ROWBY[x]), x)
    return [(c, want.get(c['id'])) for c in cards]


def unit_cards(p, i, gk, ln=''):
    r = nav(p, '상표법', '__mg%d%s' % (i, ln), gk)
    cs = all_cards(p) if r['n'] else []
    return r, cs


def collect_all(p):
    """단원마다 기출(g) · 기타(x) 두 거름의 카드 — {(i, gk): [card…]}"""
    got = {}
    for i in LEAVES:
        for gk in ('g', 'x'):
            got[(i, gk)] = unit_cards(p, i, gk)[1]
    return got


# ════════════════════════ C1 — 본판 §E-3(앱) ════════════════════════
def c1a(br, src, tag):
    """서랍 = OMR 단원(시험 목차 마디 전부 · 차례 그대로) + 맨 아래 「변리사 기출」(해 줄)"""
    p = open_pg(br, src, PC, tag)
    try:
        go_saeng(p)
        rows = drawer_rows(p)
        ts = [r['t'] for r in rows]
        want = [lab_of(i) for i in range(len(MD))]
        pos = []
        for w in want:
            k = next((j for j, t in enumerate(ts) if t == w or t.startswith(w + ' ')), -1)
            pos.append(k)
        gi = next((j for j, t in enumerate(ts) if '변리사 기출' in t), -1)
        yrs = [t for t in ts if re.match(r'^\d{4}년 제\d+회$', t)]
        ok = all(k >= 0 for k in pos) and pos == sorted(pos) and gi > max(pos) and len(yrs) >= 20
        return T('C1a', '서랍 OMR 단원 %d 줄 · 차례 그대로 · 맨 아래 「변리사 기출」(해 줄)' % len(want), ok,
                 {'단원 자리': dict(zip(want, pos)), '변리사 기출': gi, '해 줄': len(yrs), '첫 줄': ts[:4]})
    finally:
        p.close()


def c1b(got):
    """단원 카드 수 = 데이터(기출 + 기타 = 그 마디 책 줄 · 한 카드 한 거름) · 63회 리담만 = (미수록) 줄"""
    bad, info = [], {}
    for i in LEAVES:
        want = [dom_of(ROWBY[x]) for x in MD[i]['지문']]
        g = [c['id'] for c in got.get((i, 'g'), [])]
        x = [c['id'] for c in got.get((i, 'x'), [])]
        okk = sorted(g + x) == sorted(want)
        info[lab_of(i)] = '기출 %d + 기타 %d = %d (데이터 %d)' % (len(g), len(x), len(g) + len(x), len(want))
        if not okk:
            bad.append(lab_of(i))
    return T('C1b', '단원 카드 수 = 데이터(마디마다 기출 + 기타 = 책 줄 수 · 빠짐·덧붙음 0)', not bad and bool(info), {'단원': info, '어긋남': bad})


def c1b_u(br, src, tag):
    p = open_pg(br, src, PC, tag)
    try:
        go_saeng(p)
        res = {}
        okk = True
        for i in LEAVES:
            lids = MD[i]['리담']
            if not lids:
                continue
            n_u = sum(len(JMQ[q]['지문']) for q in lids if q in JMQ and not any(z.get('uid') in UIDN for z in JMQ[q]['지문']))
            r, cs = unit_cards(p, i, 'g', '~u')
            res[lab_of(i)] = '(미수록) %d · 기대 %d' % (len(cs), n_u)
            okk &= len(cs) == n_u
        okk &= any('(미수록) 5' in v for v in res.values())
        return T('C1b-u', '리담만 줄(63회 등 · 책에 없는 리담 선지) = 그 마디 (미수록) 줄 카드 · 흡수된 리담 선지는 책 카드로만', okk, res)
    finally:
        p.close()


def c1c(got, tag='C1c'):
    """객관식 선지 카드 = 늘 발문 상자 안 · 상자 머리 = 「[종합사례 원문] - N번」 · OX 카드는 상자 밖"""
    out, ox_in, heads, n = [], [], {}, 0
    for (i, gk), cs in got.items():
        for c, rid in card_row_map(i, cs):
            if not rid:
                continue
            r = ROWBY[rid]
            if r.get('문항'):
                n += 1
                if not c['box']:
                    out.append(rid)
                heads[r['문항']] = c['bh']
            elif c['box'] and r['id'] in ROWBY and not r['id'].startswith('V4-B2-S20'):
                ox_in.append(rid)
    okh = all(re.match(r'^\[종합사례 원문\] - \d+번$', h) for h in heads.values())
    return T(tag, '객관식 선지 카드 %d 중 발문 상자 밖 0 · 상자 머리 「[종합사례 원문] - N번」 · OX 카드 상자 안 0' % n,
             n > 0 and not out and not ox_in and okh, {'상자 밖': out, 'OX 상자 안': ox_in, '머리': heads})


def c1c_yard(br, src, tag):
    """좁은 헛잣대 — 새 판에서 「늘 상자」 한 줄만 걷으면(특허 mlnBoxy 그대로) 단순 발문 문항(시험 A1-S1 「옳지 않은 것은?」)이 상자 밖"""
    line = "  if (z.판) return true;   /* ★ sp_view4 §D-5"
    if line not in src:
        return N('C1c-헛', '좁은 헛잣대 해당 없음', '그 줄 없음(바탕 판)')
    s2 = src.replace(line, "  if (false) return true;   /* ★ sp_view4 §D-5", 1)
    p = open_pg(br, s2, PC, tag)
    try:
        r, cs = unit_cards(p, UNIT_OF['V4-A1-S1-1'], 'x')
        outn = sum(1 for c in cs if c['lab'].find('번 - ') >= 0 and not c['box'])
        return T('C1c-헛', '좁은 헛잣대(「늘 상자」 줄만 걷은 새 판) — 단순 발문 문항 선지가 상자 밖 > 0(관문이 잡는다)', outn > 0, {'상자 밖': outn})
    finally:
        p.close()


def pair_flow(p, uid, ids, val='O'):
    """같은 uid 쌍 — 한쪽 카드에서 O/X 누름 → 다른 단원 카드에 같은 기록 · 다시 눌러 풀면 양쪽 다 풀림"""
    ia, ib = UNIT_OF[ids[0]], UNIT_OF[ids[1]]
    gk = 'g' if re.search(r'\d{2}\s*변리', ROWBY[ids[0]].get('태그', '')) else 'x'
    sel = '#qb-%s .mboxb.%s' % (uid.replace('.', '\\.'), val)
    ra = nav(p, '상표법', '__mg%d' % ia, gk)
    a_has = p.ev("(i) => !!document.getElementById(i)", 'qb-' + uid)
    pressed = press_sel(p, sel, 600)
    a_sel = p.ev("([i,v]) => { const c = document.getElementById(i); return !!c && !!c.querySelector('.mboxb.' + v + '.sel'); }", ['qb-' + uid, val])
    rb = nav(p, '상표법', '__mg%d' % ib, gk)
    b_has = p.ev("(i) => !!document.getElementById(i)", 'qb-' + uid)
    b_sel = p.ev("([i,v]) => { const c = document.getElementById(i); return !!c && !!c.querySelector('.mboxb.' + v + '.sel'); }", ['qb-' + uid, val])
    rec = p.ev("(k) => (oxOf(k) || {}).m || ''", uid)
    press_sel(p, sel, 600)   # 다른 쪽에서 풀기
    nav(p, '상표법', '__mg%d' % ia, gk)
    a_un = p.ev("([i,v]) => { const c = document.getElementById(i); return !!c && !c.querySelector('.mboxb.' + v + '.sel'); }", ['qb-' + uid, val])
    ok = a_has and b_has and pressed and a_sel and b_sel and rec == val and a_un and ia != ib
    return ok, {'uid': uid, '단원': [lab_of(ia), lab_of(ib)], '두 카드': [a_has, b_has], '누름': pressed, '한쪽 표시': a_sel, '다른 쪽 표시': b_sel, '기록': rec, '다른 쪽에서 풀기 → 이쪽 풀림': a_un}


def c1d(br, src, tag, dev=PC, eng='chromium', g='C1d'):
    REMOTE.clear()
    p = H.dev_page(br, tag, src, dev, eng=eng)
    sv(p)
    try:
        go_saeng(p)
        rs = []
        for uid, ids in PAIRS[:5]:
            try:
                rs.append(pair_flow(p, uid, ids))
            except Exception as e:
                rs.append((False, {'uid': uid, '멈춤': str(e).splitlines()[0][:160]}))
        ok = len(rs) == 5 and all(r[0] for r in rs)
        return T(g, '같은 uid 쌍 표본 5(배지 OX ↔ 같은 글 객관식 선지) — 두 단원에 카드 둘 · 한쪽 O 누름 → 다른 쪽 같은 기록 · 다른 쪽에서 풀면 이쪽도 풀림(%s · %s)' % (eng, '손가락' if p.touch else '마우스'), ok, [r[1] for r in rs])
    finally:
        p.close()


def c1e(got):
    """칩 — 출처 셋(YY 변리 · 뷰객 창작 · 뷰객 OX) · 유형 = OX 책 태그 넷 · 객관식 = 조문형·판례형·혼합 · 판 칩 V4(H7 0) · 책번호 칩"""
    seen_src, seen_tag, bad, n = set(), set(), [], 0
    for (i, gk), cs in got.items():
        for c, rid in card_row_map(i, cs):
            if not rid:
                continue
            r, n = ROWBY[rid], n + 1
            src = c['src']
            kind = 'YY 변리' if re.match(r'^\d{2} 변리$', src) else src
            seen_src.add(kind)
            tags = r.get('유형태그') or []
            if src != r.get('태그'):
                bad.append((rid, '출처', src))
            if tags:
                if c['ty'] != '·'.join(tags):
                    bad.append((rid, '유형', c['ty']))
                for t in tags:
                    seen_tag.add(t)
            elif c['ty'] not in ('조문형', '판례형', '혼합', '유형?'):
                bad.append((rid, '객관식 유형', c['ty']))
            if c['ed'] != 'V4' or c['hasH7']:
                bad.append((rid, '판 칩', c['ed']))
            if c['bk'] != str(r.get('책번호', '')):
                bad.append((rid, '책번호', c['bk']))
    ok = n > 0 and not bad and seen_src >= {'YY 변리', '뷰객 창작', '뷰객 OX'} and seen_tag >= {'이론', '조문', '판례', '심사기준'}
    return T('C1e', '칩 — 출처 셋 · OX 태그 넷(이론·심사기준 포함) · 객관식 조문형/판례형/혼합 · 판 칩 「V4」(「H7」 0) · 책번호 칩 (카드 %d)' % n, ok,
             {'출처': sorted(seen_src), '태그': sorted(seen_tag), '어긋남': bad[:12]})


def c1f(br, src, tag):
    """짝 카드 해설 = 책 해설 + 「📗 리담 해설」(리담 해설이 비면 그 줄 없음) · 정오 = 책(리담으로 메우지 않음)"""
    p = open_pg(br, src, PC, tag)
    try:
        go_saeng(p)
        rows = [r for r in ROWS if r.get('리담')]
        bad, n_has, n_no, real = [], 0, 0, 0
        for i in sorted({UNIT_OF[r['id']] for r in rows}):
            gk = 'g'
            nav(p, '상표법', '__mg%d' % i, gk)
            for r in [r for r in rows if UNIT_OF[r['id']] == i]:
                d = dom_of(r)
                if real < 2:
                    ok_p = press_sel(p, '#%s .mbpeek' % d, 300)
                    real += 1 if ok_p else 0
                else:
                    p.ev("(i) => { const b = document.querySelector('#' + i + ' .mbpeek'); if (b) b.click(); }", d)
                t = p.ev("(i) => { const e = document.querySelector('#' + i + ' .mbexp'); return e ? e.innerText : null; }", d)
                ls = (r.get('리담해설') or '').strip()
                if t is None:
                    bad.append((r['id'], '해설 칸 없음'))
                    continue
                if ls:
                    n_has += 1
                    if '📗 리담 해설' not in t or ls[:12] not in t:
                        bad.append((r['id'], '리담 해설 빠짐'))
                else:
                    n_no += 1
                    if '📗 리담 해설' in t:
                        bad.append((r['id'], '빈 리담 해설인데 줄'))
                if r.get('sol', '')[:10] not in t:
                    bad.append((r['id'], '책 해설 빠짐'))
        ok1 = T('C1f', '짝 카드 해설 — 리담 해설 있음 %d = 「📗 리담 해설」 줄 · 빔 %d = 줄 없음 · 책 해설 먼저 (손 누름 %d)' % (n_has, n_no, real), n_has > 0 and n_no > 0 and not bad, bad[:10])
        # 정오 = 책만 — 책 정오가 빈 뷰객 줄(합성 · 리담 정오 O)을 그린 카드 = 「정오 없음 — 채점 불가」(리담으로 메우지 않음) · 특허 제7판 줄은 옛 길(리담 보강) 그대로
        m = p.ev("() => { const mk = (extra) => { const z = Object.assign({ id: 'V4-T-1', uid: 'SVT0001', t: '시험 정오 빈 줄', sol: '', 쪽: '1', 태그: '뷰객 OX', 책번호: 'T-OX1', ox: '', 리담: { 연도: '2010', 문항: '9', 선지: '1', ox: 'O' } }, extra); const c = p7Card(z, 1); return !!c.querySelector('.qb.warn'); };"
                 " return { v4: mk({ 판: 'V4', 유형태그: ['조문'] }), p7: mk({ id: 'P7-T-1', uid: 'TT0001', 태그: '10 변리' }) }; }")
        ok2 = T('C1f', '정오 = 책만 — 책 정오가 빈 뷰객 줄(리담 정오 있음) = 「정오 없음 — 채점 불가」 · 특허 제7판 줄 = 옛 리담 보강 그대로', m['v4'] and not m['p7'], m)
        return ok1 and ok2
    finally:
        p.close()


def c1g(br, src, tag):
    """표장 그림 = 지문 자리 그림(창 폭 맞춤 · 화면 밖 0 · 누르면 크게 · 남은 글자는 옆에) · 세 기기"""
    allok, info = True, {}
    rid = next(r['id'] for r in ROWS if r.get('img'))
    for nm, dev in DEVS:
        p = open_pg(br, src, dev, tag + nm)
        try:
            go_saeng(p)
            nav(p, '상표법', '__mg%d' % UNIT_OF[rid], 'x')
            d = dom_of(ROWBY[rid])
            p.pg.wait_for_function("(i) => { const e = document.querySelector('#' + i + ' .vimg-img'); return !!e && e.naturalWidth > 0; }", arg=d, timeout=15000)
            p.ev("(i) => document.getElementById(i).scrollIntoView({block:'center'})", d)
            p.idle(200)
            m = p.ev("(i) => { const c = document.getElementById(i), im = c.querySelector('.vimg-img'), t = c.querySelector('.mbqtx'); const a = im.getBoundingClientRect(), b = t.getBoundingClientRect(), cr = c.getBoundingClientRect();"
                     " return { nw: im.naturalWidth, l: a.left, r: a.right, w: a.width, vw: innerWidth, cardR: cr.right, beside: b.top < a.bottom - 2 && b.left >= a.right - 2, txw: b.width, txt: t.textContent, sw: document.scrollingElement.scrollWidth, cw: document.scrollingElement.clientWidth }; }", d)
            ok = m['nw'] > 0 and m['l'] >= 0 and m['r'] <= m['vw'] + 0.5 and m['r'] <= m['cardR'] + 0.5 and m['sw'] <= m['cw'] + 1 and m['txt'].strip() == ROWBY[rid]['t'] and m['txw'] >= 60
            big = None
            if nm == 'PC1440':
                press_sel(p, '#%s .vimg-img' % d, 600)
                big = p.ev("() => (POPS || []).some(x => (x._pk || '').indexOf('🖼 ') >= 0 && !!x.querySelector('.vimg-full'))")
                ok = ok and big
            info[nm] = dict(m, big=big)
            allok &= ok
        except Exception as e:
            allok = False
            info[nm] = '멈춤 ' + str(e).splitlines()[0][:160]
        finally:
            p.close()
    return T('C1g', '표장 그림 — 받아 보임 · 화면·카드 밖 0 · 남은 글자 「%s」(옆 · 자리 모자라면 아래 · 글자 폭 ≥ 60px = 짓눌림 0) · PC 누르면 크게(🖼 창) · 세 기기' % ROWBY[rid]['t'], allok, info)


def ty_expect(got, flt):
    """거르기 값마다 남을 카드 — OX 는 책 태그 · 객관식은 거르기 끈 화면의 유형 칩 글(배지와 거르기가 같은 값)"""
    want = {}
    for (i, gk), cs in got.items():
        for c, rid in card_row_map(i, cs):
            if not rid:
                continue
            tags, ty = ROWBY[rid].get('유형태그') or [], c['ty']
            hit = {'jo': ('조문' in tags) or ty in ('조문형', '혼합'), 'pan': ('판례' in tags) or ty in ('판례형', '혼합'),
                   'th': '이론' in tags, 'sg': '심사기준' in tags}[flt]
            if hit:
                want.setdefault((i, gk), []).append(c['id'])
    return want


def c1h(br, src, tag, got):
    """태그 거르기 넷(상표 = 조문·판례·이론·심사기준) — 펼침 목록에서 손으로 고르면 단원 카드가 그 값만 · 특허 목록 무변"""
    p = open_pg(br, src, PC, tag)
    try:
        go_saeng(p)
        if not got:
            got = collect_all(p)
            nav(p, '상표법', None, 'g', 'all')
        press_sel(p, '#slot .uzfb', 400)
        opts = p.ev("() => [...document.querySelectorAll('.uzfm .uzfo')].map(x => x.textContent)")
        p.ev("() => { const m = document.querySelector('.uzfm'); if (m) m.remove(); }")
        res, okk = {}, opts == ['전체', '조문', '판례', '이론', '심사기준', '미확정']
        for flt, nm in (('jo', '조문'), ('pan', '판례'), ('th', '이론'), ('sg', '심사기준')):
            nav(p, '상표법', None, 'g')
            press_sel(p, '#slot .uzfb', 400)
            press_sel(p, '.uzfm .uzfo[data-uzty="%s"]' % flt, 600)
            cur = p.ev("() => S.oxFilter")
            want = ty_expect(got, flt)
            gotf, bad = {}, []
            for i in LEAVES:
                for gk in ('g', 'x'):
                    ids = [c['id'] for c in unit_cards(p, i, gk)[1]]
                    if ids:
                        gotf[(i, gk)] = ids
                    if sorted(ids) != sorted(want.get((i, gk), [])):
                        bad.append((lab_of(i), gk, len(ids), len(want.get((i, gk), []))))
            n = sum(len(v) for v in want.values())
            res[nm] = {'S.oxFilter': cur, '카드': sum(len(v) for v in gotf.values()), '기대': n, '어긋남': bad[:6]}
            okk &= cur == flt and not bad and n > 0
        p.ev("async () => { S.oxFilter = 'all'; S.law = '특허법'; S.mok = null; await render(); }")
        p.idle(500)
        press_sel(p, '#slot .uzfb', 400)
        opts_t = p.ev("() => [...document.querySelectorAll('.uzfm .uzfo')].map(x => x.textContent)")
        okk &= opts_t == ['전체', '조문형', '판례형', '조문+판례', '미확정']
        return T('C1h', '태그 거르기 넷(손으로 고름) — 상표 목록 「전체·조문·판례·이론·심사기준·미확정」 · 값마다 단원 카드 = 기대 · 특허 목록 무변', okk, {'상표 목록': opts, '특허 목록': opts_t, '값마다': res})
    finally:
        p.close()


def exv_text(p, law, year):
    p.ev("async ([l, y]) => { S.law = l; S.tab = 'jimun'; S.jimunTab = 'gichul'; S.year = y; S.omr = false; S.giWrong = false; S.mok = null; await render(); }", [law, year])
    p.idle(600)
    return p.ev("() => (document.querySelector('#slot') || {}).innerText || ''")


def c1i(br, src, base_src, tag):
    """연도별 기출 보기 무변(상표 해 셋 · 바탕 = 83c230f) · 2025 62회 = 정답 칸이 차면 채점(시험 덧판)"""
    pn, pb = open_pg(br, src, PC, tag + 'n'), open_pg(br, base_src, PC, tag + 'b')
    try:
        same = {}
        for y in ('2024', '2016', '2010'):
            a, b = exv_text(pn, '상표법', y), exv_text(pb, '상표법', y)
            same[y] = (a == b, len(a))
        ok1 = all(v[0] and v[1] > 200 for v in same.values())
        T('C1i', '연도별 기출 보기 무변 — 상표 2024 · 2016 · 2010 기출뷰 글 = 바탕(83c230f)', ok1, same)
        t25 = exv_text(pn, '상표법', '2025')
        N('C1i', '2025 62회(지금 공개 데이터)', '「최종정답이 아직 없다」 %s · jimun_상표.json 2025 정답 칸 0(데이터 몫 — 로컬 원장)' % ('보임' if '최종정답이 아직 없다' in t25 else '안 보임'))
    finally:
        pn.close()
        pb.close()
    # 덧판 — 2025 문항 정답 칸을 채운 시험 jimun_상표.json(앱 무변 · 같은 함수 giGradable 이 채점한다)
    d25 = os.path.join(TMP, 'data25')
    shutil.rmtree(d25, ignore_errors=True)
    os.makedirs(d25)
    for x in os.listdir(DATA):
        if x != 'jimun_상표.json':
            _ln(os.path.realpath(os.path.join(DATA, x)), os.path.join(d25, x))
    J = json.loads(json.dumps(JMS))
    n25 = 0
    for q in J['문제']:
        if str(q.get('연도')) == '2025':
            q['정답'] = '1'
            n25 += 1
    json.dump(J, open(os.path.join(d25, 'jimun_상표.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    DATA_FOR[tag + '25'] = d25
    p = open_pg(br, src, PC, tag + '25')
    try:
        t = exv_text(p, '상표법', '2025')
        ng = p.ev("() => ((C['jimun_상표.json'] || {}).문제 || []).filter(q => String(q.연도) === '2025' && giGradable(q)).length")
        ok2 = '최종정답이 아직 없다' not in t and n25 > 0 and ng == n25
        return T('C1i-25', '2025 62회 채점 — 정답 칸 %d 문항을 채운 시험 덧판에서 「최종정답 아직 없다」 없음 · 채점되는 문항 %d(앱 무변 잠금 · 진짜 정답은 로컬 원장)' % (n25, ng), ok2, {'첫 글': t[:120]}) and ok1
    finally:
        p.close()


def c1j(br, src, tag):
    """특허 단원을 보던 상태에서 상표·디보로 바꿈 → 오류 0 · 그 법 첫 화면(「'마디' null」 0)"""
    out, okk = {}, True
    for to in ('상표', '디보'):
        p = open_pg(br, src, PC, tag + to)
        try:
            go_law_click(p, '특허')
            go_tab_jimun(p)
            r = nav(p, '특허법', '__mg3', 'g')
            go_law_click(p, to)
            m = p.ev("() => ({ law: S.law, mok: S.mok, err: (window.__ERR || []).filter(e => /마디|null/.test(e)), bad: /읽지 못했다|Cannot read/.test((document.querySelector('#slot') || {}).innerText || ''), head: ((document.querySelector('#slot') || {}).innerText || '').slice(0, 40) })")
            ok = r['n'] > 0 and not m['err'] and not m['bad'] and m['mok'] is None and not p.errs
            out[to] = dict(m, 특허카드=r['n'], pageerror=p.errs[:2])
            okk &= ok
        finally:
            p.close()
    return T('C1j', '특허 단원(카드 있음) → 상표 · 디보 법 칩 누름 — 「데이터를 읽지 못했다」·「reading 마디」 0 · 그 법 첫 화면', okk, out)


# ════════════════════════ C2 — add2 §B(add1 §B 겹침 한 번) ════════════════════════
S_OXJO = ['V4-A1-OX2', 'V4-A1-OX5-a', 'V4-A2-OX6', 'V4-A2-OX7', 'V4-A2-OX8']
S_OBJJO = ['V4-A1-S1-2', 'V4-A1-S1-4', 'V4-B2-S18-2', 'V4-B2-S18-3', 'V4-9-1-22-1']
S_PAN = [('V4-A1-OX3', '2011후1142'), ('V4-A1-OX5-b', '2017후1234'), ('V4-A2-OX29', '2002후765'), ('V4-B2-S4-4', '2003후1314'), ('V4-B2-S18-1', '2002후291')]
S_OTHER = [('V4-A1-OX4', '제33조', '디자인보호법'), ('V4-A2-OX6', '제29조', '특허법'), ('V4-B2-S18-3', '제750조', '민법')]


def gk_of(r):
    return 'g' if re.search(r'\d{2}\s*변리', r.get('태그', '')) else 'x'


def open_card(p, rid, peek=True):
    r = ROWBY[rid]
    nav(p, '상표법', '__mg%d' % UNIT_OF[rid], gk_of(r))
    d = dom_of(r)
    if peek:
        p.ev("(i) => { const e = document.querySelector('#' + i + ' .mbexp'); if (e && e.style.display === 'none'){ const b = document.querySelector('#' + i + ' .mbpeek'); if (b) b.click(); } }", d)
        p.idle(150)
    return d


def click_chips(p, d, sel, real):
    """카드 d 의 칩(sel)을 하나씩 누른다 — 손(real) 또는 쪽 안 click · 누른 뒤 뜬 창 키"""
    n = p.ev("([i, s]) => document.querySelectorAll('#' + i + ' ' + s).length", [d, sel])
    out = []
    for j in range(n):
        p.ev("() => { try{ closeAllPops(); }catch(e){} __PJ.length = 0; __PP.length = 0; }")
        if real:
            r = p.ev("([i, s, j]) => { const b = document.querySelectorAll('#' + i + ' ' + s)[j]; b.scrollIntoView({block:'center'}); const q = b.getBoundingClientRect(); const at = document.elementFromPoint(q.left + q.width/2, q.top + q.height/2); return {cx: q.left + q.width/2, cy: q.top + q.height/2, on: !!at && (at === b || b.contains(at)), t: b.textContent}; }", [d, sel, j])
            if r['on']:
                (p.tap if p.touch else p.click)(r['cx'], r['cy'], 900)
            else:
                p.ev("([i, s, j]) => document.querySelectorAll('#' + i + ' ' + s)[j].click()", [d, sel, j])
                p.wait(700)
        else:
            p.ev("([i, s, j]) => document.querySelectorAll('#' + i + ' ' + s)[j].click()", [d, sel, j])
            p.wait(250)
        out.append(p.ev("() => ({ pj: __PJ.slice(), pp: __PP.slice(), pops: (POPS || []).map(x => ({ k: x._pk || '', t: (x.innerText || '').replace(/\\s+/g, ' ').slice(0, 300) })) })"))
    return out


def jo_cells(br, src, tag, g='C2-1'):
    """조문·판례 링크 — 표본 15(손 누름) · 다른 법 인용 3 · 전수(상표 책 카드 칩 전부 · 쪽 안 누름)"""
    p = open_pg(br, src, PC, tag)
    try:
        go_saeng(p)
        p.ev("() => __SV.wrap()")
        res, okk = {'OX 조문': {}, '객관식 조문': {}, '판례': {}, '다른 법': {}}, True
        for grp, ids in (('OX 조문', S_OXJO), ('객관식 조문', S_OBJJO)):
            for rid in ids:
                d = open_card(p, rid)
                hits = click_chips(p, d, '.c2jb', True)
                laws = [h['pj'][-1][0] for h in hits if h['pj']]
                ks = [h['pj'][-1][1] for h in hits if h['pj']]
                popok = all(any(x['k'] == 'jo|상표법|' + h['pj'][-1][1] for x in h['pops']) for h in hits if h['pj'])
                want = jo_expect(ROWBY[rid]['sol'])
                ok = bool(hits) and all(L == '상표법' for L in laws) and sorted(ks) == sorted(want) and popok
                res[grp][rid] = {'칩': len(hits), '법': sorted(set(laws)), '조': ks, '해설 글 조': want, '창': popok}
                okk &= ok
        for rid, case in S_PAN:
            d = open_card(p, rid)
            n = p.ev("([i, c]) => [...document.querySelectorAll('#' + i + ' .cfpan')].findIndex(b => b.textContent.indexOf(c) >= 0)", [d, case])
            ok = n >= 0
            info = {'칩': n >= 0}
            if n >= 0:
                p.ev("() => { try{ closeAllPops(); }catch(e){} __PP.length = 0; }")
                r = p.ev("([i, j]) => { const b = document.querySelectorAll('#' + i + ' .cfpan')[j]; b.scrollIntoView({block:'center'}); const q = b.getBoundingClientRect(); return {cx: q.left + q.width/2, cy: q.top + q.height/2}; }", [d, n])
                p.click(r['cx'], r['cy'], 1200)
                p.idle(400)
                pop = p.ev("(c) => { const x = (POPS || []).find(y => (y._pk || '') === '|⚖ ' + c); return x ? (x.innerText || '').replace(/\\s+/g, ' ') : null; }", case)
                law = p.ev("() => (typeof PANIDX !== 'undefined' && PANIDX) ? PANIDX._law : null")
                inl = PAN_IN.get(case)
                if inl:
                    nm = inl.get('사건명') or inl.get('별칭') or ''
                    ok = bool(pop) and law == '상표법' and (nm[:6] in pop if nm else '원본·요약본에 없다' not in pop)
                else:
                    ok = bool(pop) and law == '상표법' and '원본·요약본에 없다' in pop
                info = {'창': (pop or '')[:80], '색인 법': law, '상표 판례 목록': bool(inl)}
            res['판례'][rid + ' ' + case] = info
            okk &= ok
        for rid, k, other in S_OTHER:
            d = open_card(p, rid)
            hits = click_chips(p, d, '.c2jb', False)
            ks = [h['pj'][-1][1] for h in hits if h['pj']]
            segs = p.ev("(i) => [...document.querySelectorAll('#' + i + ' .mbtype .seg.jo')].map(x => x.textContent)", d)
            ok = k not in ks and k.replace('제', '').replace('조', '') not in segs
            res['다른 법'][rid] = {'다른 법': other + ' ' + k, '칩 조': ks, '유형 칩 조': segs}
            okk &= ok
        T(g, '표본 15(손 누름) — OX 조문 5 · 객관식 조문 5 = 상표법 그 조 창(조 = 해설 글) · 판례 5 = 상표 판례 창(목록 밖 = 「원본·요약본에 없다」) · 다른 법 인용 3 = 링크 없음', okk, res)
        # 전수 — 상표 책 카드 칩 전부
        to_pat, nochip, n_card, n_chip = [], [], 0, 0
        for i in LEAVES:
            for gk in ('g', 'x'):
                nav(p, '상표법', '__mg%d' % i, gk)
                ids = [c for c in p.ev("() => [...document.querySelectorAll('#slot .qwrap')].map(c => c.id)")]
                for d in ids:
                    rid = next((x for x in MD[i]['지문'] if dom_of(ROWBY[x]) == d), None)
                    if not rid:
                        continue
                    n_card += 1
                    hits = click_chips(p, d, '.c2jb', False)
                    n_chip += len(hits)
                    for h in hits:
                        for L, k in h['pj']:
                            if L != '상표법':
                                to_pat.append((rid, L, k))
                    if re.search(r'상표법\s*제\s?\d+조', ROWBY[rid].get('sol', '')) and not hits:
                        nochip.append(rid)
        return T(g, '전수 — 상표 책 카드 %d · 조 칩 %d · 특허법(다른 법)으로 이은 칩 0 · 「상표법 제N조」 해설인데 칩 0 인 카드 0' % (n_card, n_chip),
                 okk and n_chip > 0 and not to_pat and not nochip, {'다른 법으로 이음': to_pat[:8], '칩 없는 카드': nochip})
    finally:
        p.close()


def jo_yard(br, src, tag):
    """좁은 헛잣대(add1 §B-3) — 새 판의 p7Jo·책 카드 법을 83c230f 처럼 특허법으로 되돌리면 「상표법 제N조」 칩 0 · 특허법 잘못 이음 > 0"""
    a, b = "LW=law||'특허법'", "const _lw=gLaw(z), JOS0"
    if a not in src or b not in src:
        return N('C2-1-헛', '좁은 헛잣대 해당 없음', '바탕 판')
    s2 = src.replace(a, "LW='특허법'", 1).replace(b, "const _lw='특허법', JOS0", 1)
    p = open_pg(br, s2, PC, tag)
    try:
        go_saeng(p)
        p.ev("() => __SV.wrap()")
        to_pat, nochip = [], []
        for i in LEAVES:
            for gk in ('g', 'x'):
                nav(p, '상표법', '__mg%d' % i, gk)
                for d in p.ev("() => [...document.querySelectorAll('#slot .qwrap')].map(c => c.id)"):
                    rid = next((x for x in MD[i]['지문'] if dom_of(ROWBY[x]) == d), None)
                    if not rid:
                        continue
                    hits = click_chips(p, d, '.c2jb', False)
                    to_pat += [(rid, L, k) for h in hits for L, k in h['pj'] if L != '상표법']
                    if re.search(r'상표법\s*제\s?\d+조', ROWBY[rid].get('sol', '')) and not hits:
                        nochip.append(rid)
        return T('C2-1-헛', '좁은 헛잣대(p7Jo·카드 법 = 특허법) — 특허법 잘못 이음 > 0 · 「상표법 제N조」 칩 0 카드 > 0 (관문이 잡는다)', bool(to_pat) and bool(nochip), {'특허법 잘못 이음': len(to_pat), '칩 0 카드': nochip[:6]})
    finally:
        p.close()


S_SEARCH = [('시험낱말 라온', 'V4-A1-S1-5'), ('시험낱말 바다', 'V4-B2-S18-2'), ('시험낱말 가람', 'V4-A1-OX1'), ('시험낱말 나루', 'V4-A1-OX3'), ('시험낱말 다솜', 'V4-A1-OX4')]


def sk_open(p):
    p.pg.keyboard.press('Control+k')
    p.wait(300)
    p.ev("() => { if (!document.querySelector('#skscope .scope[data-s=jimun].on')) document.querySelector('#skscope .scope[data-s=jimun]').click(); }")
    p.wait(200)


def sk_law(p, short, on=True):
    p.ev("([t, on]) => { const b = [...document.querySelectorAll('#skLaws .lawsc')].find(x => x.textContent === t); if (b && b.classList.contains('on') !== on) b.click(); }", [short, on])
    p.wait(200)


def sk_run(p, q):
    p.pg.fill('#skin', '')
    p.pg.type('#skin', q, delay=20)
    p.pg.wait_for_function("() => [...document.querySelectorAll('#skres .grp')].some(g => /📝 지문 — /.test(g.textContent))", timeout=15000)
    p.wait(300)
    return p.ev("() => [...document.querySelectorAll('#skres .res')].map(r => (r.innerText || '').replace(/\\s+/g, ' '))")


def c2_2(br, src, tag):
    """🔍 검색 — 책에만 있는 지문 표본 5(창작 2 · OX 3)의 글 조각 → 결과(판 칩 V4) → 눌러 지문 창 → 「그 지문으로 가기」 = 상표 그 카드 · 특허에서 찾아도 상표로"""
    p = open_pg(br, src, PC, tag)
    try:
        go_saeng(p)
        res, okk = {}, True
        for j, (q, rid) in enumerate(S_SEARCH):
            if j == 4:   # 마지막 표본은 특허 화면에서(법 칩 둘 켬) — 가기 = 상표로 바뀜
                p.ev("async () => { S.law = '특허법'; S.mok = null; await render(); }")
                p.idle(400)
            sk_open(p)
            sk_law(p, '상표', True)
            rows = sk_run(p, q)
            hit = next((k for k, t in enumerate(rows) if t.startswith('V4 ') or ' V4' in t), -1)
            info = {'결과': rows[:3], 'V4 줄': hit}
            ok = hit >= 0
            if ok:
                p.ev("(k) => { const r = [...document.querySelectorAll('#skres .res')].filter(x => /V4/.test(x.innerText))[0]; r.click(); }", hit)
                p.wait(500)
                pop = p.ev("() => { const x = (POPS || []).filter(y => /^q\\|📝 V4/.test(y._pk || '')).pop(); return x ? (x.innerText || '').replace(/\\s+/g, ' ').slice(0, 160) : null; }")
                info['지문 창'] = pop
                p.ev("() => { const x = (POPS || []).filter(y => /^q\\|📝 V4/.test(y._pk || '')).pop(); const g = x && [...x.querySelectorAll('button')].find(b => /그 지문으로 가기/.test(b.textContent)); if (g) g.click(); }")
                p.wait(1500)
                p.idle(400)
                d = dom_of(ROWBY[rid])
                got = p.ev("(i) => ({ law: S.law, mok: S.mok, card: !!document.getElementById(i), toast: ((document.querySelector('#toast') || {}).textContent || '') })", d)
                info['가기'] = got
                ok = bool(pop) and got['law'] == '상표법' and got['card']
            res[q] = info
            okk &= ok
            p.ev("() => { const s = document.querySelector('#sk'); if (s) s.style.display = 'none'; }")
        return T('C2-2', '🔍 검색 표본 5(창작 2 · OX 3 · 마지막은 특허 화면에서) — 결과 「V4 …」 줄 · 지문 창 · 「그 지문으로 가기」 = 상표 그 카드(기타 거름이면 기타로)', okk, res)
    finally:
        p.close()


S_WIN = ['V4-A1-OX1', 'V4-A1-S1-5', 'V4-B2-S18-1', 'V4-A2-OX6', 'V4-9-1-22-3']   # 책에만 있는 줄(같은 uid 쌍 열쇠는 문제 창·다른 법 찾기에서 리담 줄이 먼저 — 특허 병합 줄과 같은 차례 · 아래 따로 잼)
S_PAIRW = 'V4-A2-OX29'


def c2_3(br, src, tag):
    """서랍 문제 수 = 데이터(uid 한 번) · 문제 창 · ✏️ 연결(찾기) 창 · 📋 정리 창 = 책 줄 표본 5 · 판 칩 V4(H7 0)"""
    p = open_pg(br, src, PC, tag)
    try:
        go_saeng(p)
        p.wait(800)
        rail = p.ev("() => (document.querySelector('[data-n=jimun]') || {}).textContent || ''")
        want = rail_expect()
        ok_rail = rail.replace(',', '') == str(want)
        T('C2-3', '서랍(레일) 1차객 문제 수 = 데이터 %d(리담 + 책 O/X · uid 한 번 = 같은 uid 쌍 한 문제)' % want, ok_rail, {'레일': rail, '기대': want})
        # 문제 창 — 1차객 첫 화면 검색 줄에 uid → Enter = 그 지문 창
        win = {}
        okw = True
        for rid in S_WIN:
            r = ROWBY[rid]
            nav(p, '상표법', None, gk_of(r))
            p.ev("() => { try{ closeAllPops(); }catch(e){} }")
            inp = p.ev("() => { const i = document.querySelector('#slot .mbsr input'); if (!i) return null; i.scrollIntoView({block:'center'}); const q = i.getBoundingClientRect(); return {cx: q.left + 20, cy: q.top + q.height/2}; }")
            if not inp:
                win[rid] = '검색 줄 없음'
                okw = False
                continue
            p.click(inp['cx'], inp['cy'], 200)
            p.pg.keyboard.press('Control+a')
            p.pg.keyboard.type(kp(r), delay=10)
            p.pg.keyboard.press('Enter')
            p.wait(900)
            m = p.ev("(k) => { const x = (POPS || []).find(y => y._pk === 'q|📝 지문 ' + k); if (!x) return null; const c1 = x.querySelector('.qpc1'); return { ed: c1 ? c1.textContent : '', t: (x.innerText || '').replace(/\\s+/g, ' ').slice(0, 200), h7: /\\bH[78]\\b/.test(x.innerText || '') }; }", kp(r))
            ok = bool(m) and m['ed'] == 'V4' and not m['h7'] and r['t'][:12] in m['t']
            win[rid] = m
            okw &= ok
        T('C2-3', '문제 창(첫 화면 검색 줄 uid → Enter) 책 줄 표본 5 — 열림 · 판 칩 「V4」 · 「H7」 0', okw, win)
        # ✏️ 연결(찾기) 창 — 특허 카드에서 열어 상표 책 줄을 글 조각으로 찾음(다른 법 = 책 지문 파일을 읽어야 걸림)
        nav(p, '특허법', '__mg3', 'g')
        p.ev("() => { const b = document.querySelector('#slot .qwrap .mblink'); if (b) b.click(); }")
        p.wait(600)
        cf, okc = {}, True
        for rid in S_WIN:
            r = ROWBY[rid]
            q = r['t'][:14]
            p.ev("(q) => { const i = document.querySelector('.cflw .cfq'); i.value = q; i.dispatchEvent(new Event('input', {bubbles: true})); }", q)
            p.wait(1200)
            rows = p.ev("() => [...document.querySelectorAll('.cflw .cfrs .cfr')].map(b => ({ id: (b.querySelector('.cfid') || {}).textContent || '', wh: (b.querySelector('.cfwh') || {}).textContent || '', no: (b.querySelector('.cfno') || {}).textContent || '' }))")
            hit = next((x for x in rows if x['id'] == kp(r)), None)
            ok = bool(hit) and ('V4 p.' in hit['wh'] or '상표법 · ' in hit['wh']) and 'H7' not in hit['wh'] and 'H8' not in hit['wh']
            if hit:
                p.ev("(k) => { const b = [...document.querySelectorAll('.cflw .cfrs .cfr')].find(x => (x.querySelector('.cfid') || {}).textContent === k); const n = b.querySelector('.cfno'); n.click(); }", kp(r))
                p.wait(700)
                pc = p.ev("(k) => { const x = (POPS || []).find(y => y._pk === 'q|📝 지문 ' + k); return x ? ((x.querySelector('.qpc1') || {}).textContent || '') : null; }", kp(r))
                ok = ok and pc == 'V4'
                hit['문제 창 판 칩'] = pc
                p.ev("(k) => { const x = (POPS || []).find(y => y._pk === 'q|📝 지문 ' + k); if (x) closeOne(x); }", kp(r))
            cf[rid] = hit or {'결과': rows[:3]}
            okc &= ok
        T('C2-3', '✏️ 연결(찾기) 창 — 특허 카드에서 상표 책 줄 표본 5 를 글 조각으로 찾음 · 자리 「상표법 · V4 p.N」(H7 0) · 번호 → 문제 창 V4', okc, cf)
        # 같은 uid 쌍 — 상표 카드에서 연 연결 창은 책 글로 찾힘(풀 = 책 줄 먼저) · 문제 창 = 리담 문항째(특허 병합 줄과 같은 규칙) · H7 0
        p.ev("() => { try{ closeAllPops(); }catch(e){} }")
        r = ROWBY[S_PAIRW]
        nav(p, '상표법', '__mg%d' % UNIT_OF['V4-A1-OX1'], 'x')
        p.ev("() => { const b = document.querySelector('#slot .qwrap .mblink'); if (b) b.click(); }")
        p.wait(600)
        p.ev("(q) => { const i = document.querySelector('.cflw .cfq'); i.value = q; i.dispatchEvent(new Event('input', {bubbles: true})); }", r['t'][:14])
        p.wait(1000)
        rows = p.ev("() => [...document.querySelectorAll('.cflw .cfrs .cfr')].map(b => ({ id: (b.querySelector('.cfid') || {}).textContent || '', wh: (b.querySelector('.cfwh') || {}).textContent || '', no: (b.querySelector('.cfno') || {}).textContent || '' }))")
        hitp = next((x for x in rows if x['id'] == kp(r)), None)
        p.ev("() => { try{ closeAllPops(); }catch(e){} }")
        p.ev("(k) => popCard(k)", kp(r))
        p.wait(700)
        pw_ = p.ev("(k) => { const x = (POPS || []).find(y => y._pk === 'q|📝 지문 ' + k); return x ? { ed: (x.querySelector('.qpc1') || {}).textContent || '', h7: /\\bH[78]\\b/.test(x.innerText || '') } : null; }", kp(r))
        okp = bool(hitp) and hitp['no'] == 'OX 29' and bool(pw_) and not pw_['h7']
        T('C2-3', '같은 uid 쌍 줄(A2-OX29) — 상표 카드 연결 창에서 책 글로 찾힘(번호 「OX 29」) · 문제 창 = 리담 문항째(특허 병합 줄과 같은 규칙 · 「H7」 0)', okp, {'찾기': hitp, '문제 창': pw_})
        okc = okc and okp
        # 📋 정리 창 — 단원 📋(첫 화면 단원 줄) · 책 줄 표본 5
        p.ev("() => { try{ closeAllPops(); }catch(e){} }")
        jn, okj = {}, True
        for rid in S_WIN:
            r = ROWBY[rid]
            i = UNIT_OF[rid]
            nav(p, '상표법', None, gk_of(r))
            jb = p.ev("([lab]) => { try{ closeAllPops(); }catch(e){} const r = [...document.querySelectorAll('#slot .mbdash .mbur')].find(e => ((e.querySelector('.l .nm') || {}).textContent || '') === lab); const b = r && r.querySelector('.mbchip.jn'); if (!b) return null; b.scrollIntoView({block:'center'}); const q = b.getBoundingClientRect(); return {cx: q.left + q.width/2, cy: q.top + q.height/2}; }", [lab_of(i)])
            if jb:
                p.click(jb['cx'], jb['cy'], 900)
            p.wait(300)
            m = p.ev("(k) => { const x = (POPS || []).filter(y => /^q\\|📋 정리/.test(y._pk || '')).pop(); if (!x) return null; const t = x.innerText || ''; return { has: t.indexOf(k) >= 0, h7: /\\bH[78]\\b/.test(t), k: x._pk }; }", kp(r))
            ok = bool(m) and m['has'] and not m['h7']
            jn[rid] = m
            okj &= ok
        return T('C2-3', '📋 정리 창(첫 화면 단원 📋) 책 줄 표본 5 — 줄 있음 · 「H7」 0', okj, jn) and ok_rail and okw and okc
    finally:
        p.close()


S_STAR = ['S1047292', 'S1148214', 'S1249244', 'S1350212r', 'S0845265']


def c2_4(br, src, base_src, tag):
    """⭐ 정답 선지 자동 중요 — 상표 정답표 지목 선지 표본 5 = 처음 열 때 켜짐(책 카드에 ⭐) · 끈 뒤 새로고침해도 꺼진 채 · 플래그 법마다 · 특허 ⭐ 무변
    새 기기 = 빈 기록 — 가짜 원격(기록 동기화)도 쪽마다 비운다(앞 칸 쪽이 올린 기록이 섞이지 않게)"""
    REMOTE.clear()
    p = open_pg(br, src, PC, tag)
    try:
        go_saeng(p)
        st = p.ev("(ks) => { const A = oxAll(); return ks.map(k => !!(((A[k] || {}).tg) || {}).important); }", S_STAR)
        on_card = {}
        for k in S_STAR:
            rid = next(x for x in UIDN[k] if ROWBY[x].get('문항'))
            nav(p, '상표법', '__mg%d' % UNIT_OF[rid], 'g')
            on_card[k] = p.ev("(i) => { const c = document.getElementById(i); return !!c && [...c.querySelectorAll('.mbqhd .qtag.on')].some(x => x.textContent === '⭐'); }", 'qb-' + k)
        flag = p.ev("() => [localStorage.getItem('jopangi_auto_상표'), localStorage.getItem('jopangi_auto')]")
        k0 = S_STAR[1]
        rid0 = next(x for x in UIDN[k0] if ROWBY[x].get('문항'))
        nav(p, '상표법', '__mg%d' % UNIT_OF[rid0], 'g')
        b = p.ev("(i) => { const c = document.getElementById(i); const b = c && [...c.querySelectorAll('.mbqhd .qtag')].find(x => x.textContent === '⭐'); if (!b) return null; b.scrollIntoView({block:'center'}); const q = b.getBoundingClientRect(); return {cx: q.left + q.width/2, cy: q.top + q.height/2}; }", 'qb-' + k0)
        if b:
            p.click(b['cx'], b['cy'], 600)
        off1 = p.ev("(k) => !(((oxAll()[k] || {}).tg) || {}).important", k0)
        p.pg.reload()
        p.pg.wait_for_function("typeof S!=='undefined' && typeof busy!=='undefined' && !busy && document.querySelector('#slot .main, #slot .mbdash')", timeout=90000)
        p.idle(300)
        sv(p)
        go_saeng(p)
        st2 = p.ev("(ks) => { const A = oxAll(); return ks.map(k => !!(((A[k] || {}).tg) || {}).important); }", S_STAR)
        ok = all(st) and all(on_card.values()) and bool(flag[0]) and off1 and (not st2[1]) and all(st2[j] for j in (0, 2, 3, 4))
        T('C2-4', '⭐ 상표 정답 선지 표본 5 — 처음 열 때 켜짐(책 카드 ⭐ 보임) · 하나 끔 → 새로고침 뒤 꺼진 채 · 플래그 jopangi_auto_상표(특허 키 따로)', ok,
          {'처음': dict(zip(S_STAR, st)), '카드 ⭐': on_card, '플래그': flag, '끔': off1, '새로고침 뒤': dict(zip(S_STAR, st2))})
    finally:
        p.close()
    # 특허 ⭐ 무변 — 새 기기(빈 기록)에서 특허 1차객을 처음 열 때 켜지는 열쇠 = 바탕과 같음
    sets = {}
    for nm, s in (('새', src), ('바탕', base_src)):
        REMOTE.clear()
        q = open_pg(br, s, PC, tag + nm)
        try:
            go_law_click(q, '특허')
            go_tab_jimun(q)
            q.idle(500)
            sets[nm] = q.ev("() => { const A = oxAll(); return [Object.keys(A).filter(k => ((A[k] || {}).tg || {}).important).sort(), !!localStorage.getItem('jopangi_auto'), localStorage.getItem('jopangi_auto_상표')]; }")
        finally:
            q.close()
    ok2 = sets['새'][0] == sets['바탕'][0] and sets['새'][1] == sets['바탕'][1] and len(sets['새'][0]) > 0 and sets['새'][2] is None
    return T('C2-4', '특허 ⭐ 무변 — 특허 1차객을 처음 열 때 켜지는 열쇠 %d = 바탕 %d(같은 목록) · 특허 플래그 같음 · 상표 플래그 안 생김' % (len(sets['새'][0]), len(sets['바탕'][0])), ok2,
             {'새': [len(sets['새'][0]), sets['새'][1], sets['새'][2]], '바탕': [len(sets['바탕'][0]), sets['바탕'][1]]}) and ok


# ════════════════════════ C2-5 — 전수 표(add2 §A-6 · §0 일곱 무리 · 83c230f 글자 그대로 · 주석 줄 뺌) ════════════════════════
W, X = '넓힘', '해당 없음'
VJW = (X, '법 무관 — VJ·MLN(그 법 책 지문·목차)을 읽는다 · 상표 VJ 가 뷰객 4판을 실으면 같은 길(C1 실측) · 고칠 것 없음')
NAMEX = (X, '법 이름·짧은 이름 표(상표 줄 이미 있음)')
VERDICT = {
    '(최상위 LAWS)': NAMEX, '(최상위 SHORT)': NAMEX, '(최상위 SIHAENG)': (X, '시행령 이름 표(네 법)'), '(최상위 S)': (X, '처음 상태 S.law 기본값(특허법) — 상표 화면 무관'),
    '(최상위 GI_LAWOF)': NAMEX, '(최상위 LAWS3APP)': (X, '세 법 표(상표 들어 있음)'), '(최상위 LAW_FULL)': NAMEX, '(최상위 LAW_SHORT)': NAMEX,
    '(최상위 C2LAWP)': (X, '2차·칩 머리 글자 표(상표 줄 있음 · 상표 책 카드 칩이 c2JoText(상표법) 로 씀)'), '(최상위 C2LAWP2)': (X, '2차 칩 머리 글자 표(상표 줄 있음)'),
    '(최상위 C2JO_LAWP)': (X, '2차 조문 낱말 법 머리 표(상 = 상표법 있음)'), '(최상위 JOSH_LAW)': NAMEX, '(최상위 JXE_LAWF)': (X, '시험지 파일 법 표(상표 sangpyo 있음)'),
    '(최상위 JXE_LAWL)': (X, 'uid 머리 → 법(S = 상표법 있음)'), '(최상위 JO_OTH_SRC)': (X, '다른 법 이름 목록(상표법 있음 · p7Jo 가 그 카드의 법을 selfLaw 로 넘김)'),
    '(최상위 CF_LAWC)': (X, 'uid 머리 → 법(S = 상표법 · 새 상표 책 uid SV… 도 S)'), '(최상위 TM_PATH)': (X, '테마 = 특허 정리OMR 테마(add2 §0 해당 없음)'),
    '(최상위 TM_LAWNM)': (X, '테마 법 이름 판정(add2 §0 해당 없음)'), '(최상위 TM_LAWOF)': (X, '테마 법(add2 §0 해당 없음)'),
    'PLAW': (X, '법 짧은 이름 함수(네 법 공통)'),
    'drawRail': (X, '레일 탭 — 정리OMR 탭 = 특허·민소(상표 정리OMR 자료 없음 · add2 §0)'), 'railCounts': (W, '서랍 문제 수 = 책 지문 갈래 표(gBook) · 상표 = 뷰객 4판 · uid 한 번 · 정리OMR 쪽 수는 특허 그대로'),
    'eqFileOf': (X, '2차 eq 파일 고르기(법별 이미)'), 'eqNorm': (X, '2차 조문 낱말 법 이름'), 'eqCurText': (X, '2차 지금 글'), 'popCard4': (X, '2차 카드 팝업(add2 §0 「2차 자료 고르기」 해당 없음)'),
    'precJoChipEl': (X, '판례 탭 조문 칩(법별 이미)'), 'precJoChip': (X, '판례 탭 조문 칩(법별 이미)'), 'joPrecIdx': (X, '조문↔판례 색인(법별 이미)'), 'precMemoGo': (X, '판례 메모 이동(법별 이미)'), 'viewPrec': (X, '판례 탭(법별 이미)'),
    'inkGo': (W, '필기 「보기」 — 책 카드 열쇠 q7|V4-… = 상표법 그 단원(옛: 늘 특허법 · 표에 없던 자리 → 같은 원칙으로 넓힘) · 이름표 inkKeyLabel 「뷰객 지문」'),
    'cha2ReportEl': (X, '2차 보고'), 'c2ChapName': (X, '2차 단원 이름'), 'view2cha': (X, '2차 탭'),
    'pinTag': (X, '📍 좌표기억 = 정리OMR(특허만 · add2 §0)'), 'mbbPop': (X, '📚 교재 자리 창 = 정리OMR(특허만 · 「정리OMR 은 특허만 있다」 그대로)'),
    'joPanelIdx': (W, '조문 탭 정오문제 창(JOPANE) — 상표 = 뷰객 4판 지문 · 그 법 조 목록(gJoLoad) · p7Jo(그 법)'),
    'p7Jo': (W, '조 칩 = 그 카드의 법(조 목록 jo_<법>_목록 · joOtherLaw(…, 그 법) · 「法N」 = 그 법 · 리담 jo 물려받기 그대로 · 施規 배지만) · 특허 = 옛 값 그대로'),
    'p7Card': (W, '책 카드 — 조 칩·누름 = 그 카드의 법 · 판 칩 = 줄의 판(V4) · 책번호 칩 · 정오 = 책만 · 표장 그림 · 「뷰객 4판 단독」 · 📍 = 특허만 그대로'),
    'viewOmr': (X, '정리OMR 탭(특허만)'), 'omrPins': (X, '정리OMR 핀(특허만)'), 'pinPop': (X, '정리OMR 핀 창(특허만)'), 'omrJump': (X, '정리OMR 이동(특허만)'), 'omrTiles': (X, '정리OMR 쪽 그림(특허만)'),
    'omrKeyIdx': (X, '정리OMR 핀 → 카드 색인(핀은 특허 정리OMR 에만 찍힘 · 상표 정리OMR 자료 없음)'), 'sfDraw': (X, '정리 검색 그림(특허 정리OMR)'), 'sfWire': (X, '정리 검색 줄(특허 정리OMR)'),
    'jpMlnReady': (W, '조문 탭 → 1차객 준비부 = 책이 있는 법(특허 · 상표) · 파일 = 책 갈래 표 · 정리OMR 맵은 특허만'),
    'viewJimun': (W, '1차객 = 상표면 뷰객 4판 책 지문 + OMR 단원 목차(mokcha_상표) + 상표법 조 목록 · 발문 상자 조건 · 다른 법 마디 값 = 첫 화면(「\'마디\' null」 고침)'),
    'skRun': (W, '🔍 검색 — 상표 책 지문(뷰객 4판) 줄 · 판 칩 = 줄의 판(V4) · 가기 = 그 법으로(popJimun → gotoJimun law) · 정리 검색·Claude 법 표는 그대로'),
    'viewCanvas': (X, '민소 정리캔버스'), 'mlnLidCard': (X, '리담 선지 카드 — 📍 조건(특허만)뿐 · 카드 꼴 법 무관'),
    'mlnObjCard': (W, '문항째 책 카드 — 판 칩 둘(출처 빈 칸 · 접기 단추) = 줄의 판(V4) · 책번호 칩 · 📍 = 특허만 그대로'),
    'jxeParseUid': (X, '출제연도 칩 — uid 머리 S = 상표 시험지(법 무관 이미 · 상표 책 카드에 「2010:29:②」 실측)'), 'jxeSpLoad': (X, '출제연도 칩 시험지 목록(법별 이미)'), 'jxeChips': (X, '출제연도 칩(법 무관 이미)'),
    'uzExvBox': (X, '연도별 기출 보기(법별 이미 · 무변 = C1i)'), 'cfLoad': (W, '✏️ 연결·문제 창 행 찾기 — 책 지문 파일 = 책 갈래 표(상표 = 뷰객 4판)'),
    'autoImportant': (W, '⭐ 정답표 지목 선지 1회 = 책이 있는 법(특허 · 상표) · 플래그 법마다(특허 jopangi_auto 그대로 · 상표 jopangi_auto_상표)'),
    'mlnBuild': (W, 'MLN.ok = 책이 있는 법(특허 제7판 · 상표 뷰객 4판)'),
    'sidFind': VJW, 'p8Guess': (X, '해례 8판 짐작(특허 8판만)'), 'mokCards': VJW, 'mgRoll': VJW, 'mgKeys': VJW, 'mgKeys0': VJW, 'qlColumn': (X, '옛 가운데 목차 열(그리지 않음)'),
    'mbDash': (X, '첫 화면 과목 카드 — VJ 기반 · 상표 목차(MG)가 실리면 같은 길 · 「목차 없음 — 특허만 있다」 는 목차 없는 디보에 그대로'), 'jtPaint': VJW, 'jnHitIdx': VJW, 'mbHmTops': VJW,
    'vjPrep': (X, 'P7 = 그 법 책 지문(법 무관) · 주석 한 줄만'), 'gotoJimun': (W, '목차 색인 = 그 법(mokIndex(subj)) · 다른 법 책 지문 = 그 법으로 · 상표 책 카드가 기출/기타 거름에 걸리면 그 쪽으로'),
    'uidSearchKeys': VJW, 'mlnCardOf': VJW, 'mlnDirect': VJW, 'mlnKeys': VJW, 'mlnCardsDeep': VJW, 'mlnYujeChip': VJW, 'mlnBestBon': VJW, 'mdpHeadSel': VJW, 'mdpOwnRows': VJW, 'jtOwnRows': VJW,
    'uzHmTops': VJW, 'uzIdx': VJW, 'uzSub': VJW, 'cfHitCur': VJW, 'cfCardKeySet': VJW, 'cfCaseOf': VJW,
    'qpBody': (W, '문제 창 판 칩 = 줄의 판(V4)'), 'qCard': (X, '리담 문항 출처 칩 「제7판」→H7 — 상표 리담 출처에 제7판 없음'), 'uzJnInfo': (W, '📋 정리 창 줄 출처 = 태그 · 없으면 줄의 판'),
    'cfRow': (W, '✏️ 연결 창 줄 출처 = 태그 · 없으면 줄의 판 · 자리 = 「상표법 · V4 p.N」(p7PageLab)'), 'mokIndex': (W, '목차 색인 = 그 법 책 목차(상표 mokcha_상표 · 특허·그 밖 = 옛 병합 그대로)'),
}
EXTRA = [('drawTop(법 칩)', W, '법을 바꾸면 1차객 마디·큐를 비운다 → 그 법 첫 화면(본판 §D-7)'), ('tyDraftP', W, '상표 OX = 책 태그 그대로 · 객관식 = 8/23 규칙(그 카드의 법 p7Jo)'),
         ('TY_NAME 곁(tyTagCode·tyHas·tyLabel·tyCls)', W, '책 태그 넷 값·글자·색 갈래(특허 값 jo·mix·pan 그대로)'), ('mbTypeChip', W, '유형 칩 글자 = 책 태그(「이론」·「조문·판례」) · 확정 창에 그 값'),
         ('typePop', W, 'OX 책 카드 = 태그 넷 고르기 · 특허·객관식 = 옛 셋'), ('oxKeep', W, '거르기 「조문」·「판례」 = 태그 포함 · 「이론」·「심사기준」 · 다른 법 값 = 전체'),
         ('UZ_TY·uzFilterLabel·uzFilterMenu', W, '상표 목록 = 전체·조문·판례·이론·심사기준·미확정 · 특허 목록 그대로'), ('uzCards(uzV4Pass)', W, '상표 책 카드 = 제 카드 초안으로 거름(같은 uid 쌍이 서로 안 숨김)'),
         ('uzBkSeg', W, '빈칸 종류 글자 = 상표 OX 「조문」 태그에도'), ('mlnBoxP', W, '상표 객관식 선지 = 늘 발문 상자(특허·디보 mlnBoxy 그대로)'), ('p7CaseBox', W, '상자 머리 번호 = 뷰객 책번호 수(「B2-S6」 → 6)'),
         ('mlnBookLab', W, '「OX 5 (a)」·「6번 - ②」(아티팩트 v7)'), ('p7PageLab', W, '「V4 p.N」'), ('qpAnsSol', W, '정오 = 책만(상표 리담 보강 없음)'), ('popJimun', W, '「그 지문으로 가기」 = 그 법으로'),
         ('inkKeyLabel', W, '필기 목록 이름 「뷰객 지문」'), ('새 함수 gBook·gEd·gLaw·gJoKey·gJoLoad·gV4Num·gCirc·gV4Lab', W, '책 갈래 표 · 판 칩 · 책 줄 법 · 법별 조 목록 · 뷰객 번호 글')]


def scan_groups(src):
    src = src.replace('\r\n', '\n')
    a = src.index('<script>', src.index('<body'))
    b = src.rindex('</script>')
    L = src.split('\n')
    start, end = src[:a].count('\n'), src[:b].count('\n')
    PAT = [('특허', r"'특허'"), ('특허법', r'특허법'), ('jimun_7pan', r'jimun_7pan'), ('omr/특허', r'omr/특허'), ('mokcha_병합', r'mokcha_병합'), ('P7map', r'P7map'), ('H7/H8', r"'H[78]'")]
    TOP = re.compile(r'^(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(')
    TOPV = re.compile(r'^(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=(.*)')
    cur, out, incmt = '(최상위)', {}, False
    for i in range(start, end + 1):
        ln = L[i]
        m, mv = TOP.match(ln), TOPV.match(ln)
        if m:
            cur = m.group(1)
        elif mv:
            cur = mv.group(1) if re.match(r'\s*(?:async\s*)?(?:\(|[A-Za-z_$][\w$]*\s*=>|function\b)', mv.group(2)) else '(최상위 %s)' % mv.group(1)
        s = ln.strip()
        if incmt:
            if '*/' in s:
                incmt = False
            continue
        if s.startswith('//') or s.startswith('*'):
            continue
        if s.startswith('/*'):
            if '*/' not in s:
                incmt = True
            continue
        code = re.sub(r'(?<![:\'"\\])//.*$', '', re.sub(r'/\*.*?\*/', '', ln))
        for g, rx in PAT:
            if re.search(rx, code):
                out.setdefault(g, {}).setdefault(cur, []).append(i + 1)
    return out


def c2_5(base_src):
    G = scan_groups(base_src)
    keys = []
    for g in G:
        for k in G[g]:
            if k not in keys:
                keys.append(k)
    miss = [k for k in keys if k not in VERDICT]
    extra = [k for k in VERDICT if k not in keys]
    nW = sum(1 for k in keys if VERDICT.get(k, ('',))[0] == W)
    rows = ['%s | %s | %s | %s' % (k, ' · '.join(g for g in G if k in G[g]), VERDICT.get(k, ('?', '?'))[0], VERDICT.get(k, ('?', '?'))[1]) for k in keys]
    N('C2-5', '무리별 자리 수(83c230f · 주석 줄 뺌)', {g: len(G[g]) for g in G})
    N('C2-5', '전수 표(자리 | 무리 | 판정 | 까닭)', rows)
    N('C2-5', '표에 없던 자리(같은 원칙으로 고침)', ['%s | %s | %s' % x for x in EXTRA])
    return T('C2-5', '전수 표 줄 수 %d = 일곱 무리 자리 수(겹침 뺌) %d · 판정 빠짐 0 · 남는 줄 0 · 넓힘 %d · 해당 없음 %d' % (len(VERDICT), len(keys), nW, len(keys) - nW),
             not miss and not extra and len(VERDICT) == len(keys), {'빠짐': miss, '남음': extra})


# ════════════════════════ C2-6 · C5 — 특허 1차객 무변(바탕 83c230f 와 맞댐) ════════════════════════
PAT_UNITS = ('__mg3', '__mg12', '__mg30', '__mg47')


def pat_snapshot(p):
    sv(p)
    out = {}
    go_law_click(p, '특허')
    go_tab_jimun(p)
    p.wait(600)
    out['레일'] = p.ev("() => [...document.querySelectorAll('[data-n]')].map(b => b.dataset.n + '=' + b.textContent)")
    out['첫 화면'] = p.ev("() => ((document.querySelector('#slot') || {}).innerText || '').slice(0, 1500)")
    for u in PAT_UNITS:
        for gk in ('g', 'x'):
            r = nav(p, '특허법', u, gk)
            out['카드 %s %s' % (u, gk)] = [{k: c[k] for k in ('id', 'src', 'ty', 'tyjo', 'ed', 'bk', 'lab', 'box', 'bh', 'c2', 'pan', 'hd')} for c in all_cards(p)]
    out['정오문제 창'] = p.ev("async () => { S.law = '특허법'; JOPANE = null; const J = await joPanelIdx(); return ['제2조', '제29조', '제33조', '제42조', '제94조'].map(k => [k, ((J[k] || {}).L || []).length, ((J[k] || {}).P || []).map(z => z.id).slice(0, 8)]); }")
    out['유형 거르기 조문형 셈'] = p.ev("async () => { S.oxFilter = 'jo'; UZGK = 'g'; S.mok = null; await render(); const t = ((document.querySelector('#slot') || {}).innerText || '').slice(0, 400); S.oxFilter = 'all'; await render(); return t; }")
    sk_open(p)
    sk_law(p, '특허', True)
    out['검색'] = sk_run(p, '신규성')[:60]
    p.ev("() => { const s = document.querySelector('#sk'); if (s) s.style.display = 'none'; }")
    return out


def c2_6(br, src, base_src, tag):
    a, b = {}, {}
    for d, s, nm in ((a, src, 'n'), (b, base_src, 'b')):
        p = open_pg(br, s, PC, tag + nm)
        try:
            d.update(pat_snapshot(p))
        finally:
            p.close()
    diff = [k for k in a if a.get(k) != b.get(k)]
    ncard = sum(len(v) for k, v in a.items() if k.startswith('카드'))
    return T('C2-6', '특허 1차객 무변 — 레일 수 · 첫 화면 · 단원 %d 곳 카드 %d(출처·유형 칩·조 칩·판례 칩·판 칩·이름표·상자) · 정오문제 창 · 거르기 셈 · 검색 = 바탕' % (len(PAT_UNITS), ncard),
             not diff and ncard > 0, {'다름': diff[:6], '검색 줄': len(a.get('검색', []))})


def c5(br, src, base_src, tag):
    """특허 1차객 화면 무변 — 세 기기 · 첫 화면 · 단원 화면 · 서랍 글 = 바탕"""
    allok, info = True, {}
    for nm, dev in DEVS:
        snap = {}
        for who, s in (('n', src), ('b', base_src)):
            p = open_pg(br, s, dev, tag + nm + who)
            try:
                go_law_click(p, '특허')
                go_tab_jimun(p)
                p.wait(500)
                h = p.ev("() => ((document.querySelector('#slot') || {}).innerText || '')")
                nav(p, '특허법', '__mg3', 'g')
                u = p.ev("() => ((document.querySelector('#slot') || {}).innerText || '')")
                dr = p.ev("() => ((document.querySelector('#jtlist') || {}).innerText || '')")
                snap[who] = (h, u, dr, p.ev("() => document.querySelectorAll('#slot .qwrap').length"))
            finally:
                p.close()
        same = [snap['n'][k] == snap['b'][k] for k in range(4)]
        info[nm] = {'첫 화면': same[0], '단원': same[1], '서랍': same[2], '카드 수': snap['n'][3]}
        allok &= all(same) and snap['n'][3] > 0
    return T('C5', '특허 1차객 화면 무변 — 폰 390 · iPad 834 · PC 1440 첫 화면·단원 화면·서랍 글 = 바탕(83c230f)', allok, info)


# ════════════════════════ C4 — 화면 훑기(규칙 60) · 세 기기 ════════════════════════
SWEEP_JS = r"""() => { const vw = innerWidth, sw = document.scrollingElement.scrollWidth, cw = document.scrollingElement.clientWidth;
  const off = [...document.querySelectorAll('#slot .qwrap, #slot .p7case, #slot .mbur, #jtlist > *, .pop')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && (r.right > vw + 1 || r.left < -1); }).map(e => e.className.split(' ')[0] + ':' + (e.id || (e.textContent || '').slice(0, 20)));
  return { sw: sw, cw: cw, off: off.slice(0, 6), n: off.length }; }"""


def c4(br, src, tag, shots=None):
    allok, info = True, {}
    for nm, dev in DEVS:
        p = open_pg(br, src, dev, tag + nm)
        rec = {}
        try:
            go_saeng(p)
            if p.touch:
                p.ev("async () => { S.jtFold = false; await render(); }")
                p.idle(300)
            m1 = p.ev(SWEEP_JS)
            rec['서랍·첫 화면'] = m1
            dn = p.ev("() => document.querySelectorAll('#jtlist .jtit, #jtlist .jtch').length")
            if shots:
                p.pg.screenshot(path=os.path.join(shots, 'c4_%s_home.png' % nm))
            if p.touch:   # 폰·아이패드 — 서랍 덮개를 접고 카드·OMR 창을 잰다(서랍에서 단원을 고르면 접히는 앱 길과 같음)
                p.ev("async () => { S.jtFold = true; await render(); }")
                p.idle(300)
            nav(p, '상표법', '__mg%d' % UNIT_OF['V4-B2-S18-1'], 'x')
            p.idle(800)
            m2 = p.ev(SWEEP_JS)
            m2['카드'] = p.ev("() => document.querySelectorAll('#slot .qwrap').length")
            rec['단원 카드'] = m2
            if shots:
                p.pg.screenshot(path=os.path.join(shots, 'c4_%s_unit.png' % nm), full_page=True)
            ob = p.ev("() => { const b = [...document.querySelectorAll('#slot .mbsbar button, #slot button')].find(x => /📝/.test(x.textContent) && /OMR/.test(x.textContent)); if (!b) return null; b.scrollIntoView({block:'center'}); const q = b.getBoundingClientRect(); return {cx: q.left + q.width/2, cy: q.top + q.height/2}; }")
            if ob:
                (p.tap if p.touch else p.click)(ob['cx'], ob['cy'], 700)
            m3 = p.ev("() => { const x = (POPS || []).filter(y => /OMR/.test((y.querySelector('.pt') || y).textContent || '')).pop() || (POPS || [])[(POPS || []).length - 1]; if (!x) return null; const r = x.getBoundingClientRect(), v = window.visualViewport; const W = v ? v.width : innerWidth, H = v ? v.height : innerHeight; return { l: r.left, t: r.top, r: r.right, b: r.bottom, in: r.left >= -1 && r.top >= -1 && r.right <= W + 1 && r.bottom <= H + 1, k: x._pk || '' }; }")
            rec['OMR 창'] = m3
            if shots:
                p.pg.screenshot(path=os.path.join(shots, 'c4_%s_omr.png' % nm))
            p.ev("() => { try{ closeAllPops(); }catch(e){} }")
            exv_text(p, '상표법', '2024')
            m4 = p.ev(SWEEP_JS)
            rec['연도별 보기'] = m4
            if shots:
                p.pg.screenshot(path=os.path.join(shots, 'c4_%s_exv.png' % nm))
            ok = all(m['sw'] <= m['cw'] + 1 and m['n'] == 0 for m in (m1, m2, m4)) and m2['카드'] > 0 and dn > 0 and bool(m3) and m3['in']
            rec['서랍 줄'] = dn
        except Exception as e:
            ok = False
            rec['멈춤'] = str(e).splitlines()[0][:200]
        finally:
            p.close()
        info[nm] = rec
        allok &= ok
    return T('C4', '화면 훑기 — 상표 서랍·첫 화면 · 단원 카드 · 📝 OMR 창 · 연도별 보기 × 폰 390 · iPad 834 · PC 1440 — 옆 넘침 0 · 화면 밖 0 · OMR 창 화면 안', allok, info)


def webkit_try(pw):
    try:
        return pw.webkit.launch()
    except Exception as e:
        N('C3', 'WebKit 안 잼', str(e).splitlines()[0][:160])
        return None


# ════════════════════════ 돌림 ════════════════════════
def main():
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    base_src = H.app_src(BASE)
    src = base_src if YARD else H.app_src(NEW)
    print('%s _task_jo_sp_view4_cloudD · 앱 = %s · 바탕 = %s · 시험 데이터 = %s(줄 %d · 객관식 %d · 마디 %d)' % ('헛잣대 —' if YARD else '관문', BASE if YARD else NEW, BASE, FX, len(ROWS), len(OBJS), len(MD)), flush=True)
    shots = os.path.join(os.path.dirname(os.path.abspath(OUTF)), 'shots_sp_view4') if not YARD else None
    if shots:
        os.makedirs(shots, exist_ok=True)
    got, times = {}, {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        shared = {}

        def c1_core():
            p = open_pg(br, src, PC, 'core')
            try:
                go_saeng(p)
                shared['got'] = collect_all(p)
            finally:
                p.close()
            a = c1b(shared['got'])
            b = c1c(shared['got'])
            c = c1e(shared['got'])
            return a and b and c

        steps = [('C1a', lambda: c1a(br, src, 'c1a')), ('C1b', c1_core), ('C1b-u', lambda: c1b_u(br, src, 'c1bu')),
                 ('C1c-헛', lambda: True if YARD else (c1c_yard(br, src, 'c1cy') is not False)),
                 ('C1d', lambda: c1d(br, src, 'c1d')), ('C1f', lambda: c1f(br, src, 'c1f')), ('C1g', lambda: c1g(br, src, 'c1g')),
                 ('C1h', lambda: c1h(br, src, 'c1h', shared.get('got', {}))), ('C1i', lambda: c1i(br, src, base_src, 'c1i')), ('C1j', lambda: c1j(br, src, 'c1j')),
                 ('C2-1', lambda: jo_cells(br, src, 'c21')), ('C2-1-헛', lambda: True if YARD else (jo_yard(br, src, 'c21y') is not False)),
                 ('C2-2', lambda: c2_2(br, src, 'c22')), ('C2-3', lambda: c2_3(br, src, 'c23')), ('C2-4', lambda: c2_4(br, src, base_src, 'c24')),
                 ('C2-5', lambda: c2_5(base_src)), ('C2-6', lambda: c2_6(br, src, base_src, 'c26')),
                 ('C3', lambda: c1d(br, src, 'c3', PHONE, 'chromium', 'C3')), ('C4', lambda: c4(br, src, 'c4', shots)), ('C5', lambda: c5(br, src, base_src, 'c5'))]
        SAME = ('C1i', 'C2-5', 'C2-6', 'C5', 'C1c-헛', 'C2-1-헛')   # 바탕끼리 맞대면 늘 같음 · 좁은 헛잣대 = 새 판 쪽 칸
        for g, fn in steps:
            if ONLY and not any(g.upper() == o or g.upper().startswith(o) for o in ONLY):
                continue
            if YARD and g in SAME:
                N(g, '헛잣대 해당 없음', '바탕 = 바탕(무변 잠금 · 좁은 헛잣대는 새 판 칸에서 돎)')
                continue
            print('── %s' % g, flush=True)
            t1 = time.time()
            try:
                got[g] = bool(fn())
            except Exception as e:
                got[g] = False
                T(g, '돌다 멈춤', False, str(e).splitlines()[0][:300])
            times[g] = round(time.time() - t1)
            print('   (%s %d초)' % (g, times[g]), flush=True)
        br.close()
        if 'webkit' in ENGS and not YARD and (not ONLY or 'C3' in ONLY):
            wk = webkit_try(pw)
            if wk:
                try:
                    c1d(wk, src, 'wk3', PHONE, 'webkit', 'C3-wk')
                except Exception as e:
                    T('C3-wk', 'WebKit 돌다 멈춤', False, str(e).splitlines()[0][:200])
                wk.close()
    lines = []
    print('\n══ 요약 (%.0f초)%s' % (time.time() - t0, ' — 헛잣대' if YARD else ''))
    for g in got:
        cells = [r for r in RES if r[0] == g and r[2] is not None]
        nf = sum(1 for r in cells if not r[2])
        verdict = (('FAIL(헛잣대 통과)' if not got[g] else 'PASS(헛잣대 실패)') if YARD else ('PASS' if got[g] else 'FAIL'))
        s = '  %-8s %s (%d 칸 중 FAIL %d · %s초)' % (g, verdict, len(cells), nf, times.get(g, '-'))
        print(s)
        lines.append(s)
    os.makedirs(os.path.dirname(os.path.abspath(OUTF)), exist_ok=True)
    with open(OUTF, 'w', encoding='utf-8', newline='\n') as f:
        for r in RES:
            d = r[3] if isinstance(r[3], str) else json.dumps(r[3], ensure_ascii=False, default=str)
            f.write('%s | %s · %s | %s\n' % ('INFO' if r[2] is None else ('PASS' if r[2] else 'FAIL'), r[0], r[1], d))
        f.write('\n'.join(lines) + '\n')
    print('결과 → %s' % OUTF)


if __name__ == '__main__':
    main()
