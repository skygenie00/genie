# -*- coding: utf-8 -*-
r"""_task_jo_popjo_fix §C 관문 — 조문 팝업 둘: 삭제 조 「본문을 찾지 못했다」 · 필기 조 꾸밈 기본 켜짐

  python _harness_jo_popjo_fix.py [--new <앱>] [--base <앱 파일 | genie git 판 = 83c230f>] [--data <jo/data>] [--base-data <git 판 = 83c230f>]
                                  [--spd <studyplandata>] [--res <결과>] [--shots <폴더>] [--eng chromium,webkit] [--only C1,C2,C3,C4] [--mode gate|regress|smoke]
  --mode(_task_qa_slim 10/4) — 없으면 gate(= 이 판 앞과 같음) · regress = NEW 만(바탕 앱 · 바탕 데이터 git 풀기 0 · 헛잣대 Y1~Y4 와 옛 앱 + 새 데이터 칸은 관문만 ·
    바탕이 기댓값인 칸(C1a 삭제 줄 칩 수 · C3 jomark 칠 수)은 기준 스냅샷) · smoke = regress 가운데 C2(T2461181 → 삭제 조 팝업) 만

  새 = --new 앱 + --data(새 데이터) · 헛잣대 = --base 앱 + 같은 데이터(지시서 「83c230f · 같은 데이터」) ·
  C1 은 바탕 앱 + 바탕 데이터(git --base-data 판 · 바뀐 파일만 덧판)도 센다(§0-3 「61 + α」)
  C1 세 법 1차객 카드(1차객 OX 풀 그대로 — 특허 = 7판 P 카드 · 리담 Z 카드 · 상표·디보 = 리담 문항 카드)를 앱 함수로 짓고 popJo 를 가로채
     jo 칩(근거 · ＋N 목록 줄)·유형 칩·7판 해설 조 칩을 다 눌러 (법 · 조)를 모은다 → 모은 (법 · 조)마다 진짜 popJo 를 열어
     「본문을 찾지 못했다」 칩 셈 = 0 (갈래별 · 조별 셈을 같이 적는다)
  C2 T2461181 카드 「유형? · 26」 진짜 누름(Chromium 폰 390 손가락 · PC 1440 마우스) → 제목 「특허법 제26조 (삭제)」 · 몸 = .ln.wml 한 줄
     「제26조 삭제 <날짜>」(날짜 = 목록 「삭제」 칸) · 「이동 ↗」 없음 · 글꼴(크기·글꼴·줄 높이·굵기) = 보통 조 팝업 원문 줄 · 폰 그림(--shots)
  C3 필기 있는 조 + mkon 없음 표본 3 → 팝업 꾸밈 0 · 글 = 필기 없을 때와 같음 · mkon 켠 조(특허 제55조 · 제132조의5 · 제16조 — studyplandata
     jopangi/기록.json 의 그 값) = 필기 있어도 없을 때와 같음(켠 것만 · 꾸밈 > 0) · jomark 칠 = 그대로(필기 · 앱 판과 상관없이 같은 수) ·
     여는 자리 다섯(유형 칩 · 근거 조 칩 · 2차 카드 조 링크 · 테마 · 본문 조 링크) 진짜 누름 → 꾸밈 0
  C4 §B-3 — 7판 6 곳(P7-0032 · 0033 · 0034 · 0035 · 1273 · 1825 · 「협정 제27조」·「협정 제31조」·「TRIPs협정 제31조」·「및 제48조」)
     카드 칩이 특허법 제27조 · 제31조 · 제48조로 잇는 것 = 0 · 바탕도 0 이면 「이미 막힘」(INFO · 막는 까닭 = joOtherLaw · JOKEY)
  꾸밈 = 팝업 몸 .ln 안 mark · u · strong · s · span[style](.jmk 뺌) · .lbl(조 이름표) · .stkanc(태그 칩) · sup.fn(각주) — 내 칠(.jmk)은 따로 센다
  도구 = 같은 폴더 _harness_jo_revfix0929b(SEED · __RB · Pg · 결과 줄) · 서버는 이 파일(쪽마다 데이터 자리 · 바탕 데이터 = 바뀐 파일만 덧판) ·
         WebKit 은 blob: · data: 를 route 끊기에서 뺀다
  D11 — 이 파일에 기록 값 0(studyplandata 기록은 돌 때 읽기만 · 결과 줄엔 수만)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402  _task_qa_slim(10/4) — --mode · --snap-in · --snap-out 을 sys.argv 에서 뗀다(이 줄은 다른 import · 인자 읽기보다 먼저)
import json, os, re, sys, time, shutil, subprocess, tempfile, threading, urllib.parse   # noqa: E402
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
DATA = ARG('--data', _roots.genie('jo', 'data'))
BDREV = ARG('--base-data', '83c230f')
SPD = ARG('--spd', _roots.spd())
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_popjo_fix_result.txt'))
SHOTS = ARG('--shots')
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
_argv = sys.argv
sys.argv = [sys.argv[0], '--new', NEW, '--data', DATA] + [x for k in ('--exam', '--mbpdf', '--vendor') if k in _argv for x in (k, _argv[_argv.index(k) + 1])]
sys.path.insert(0, HERE)
import _harness_jo_revfix0929b as H   # noqa: E402
sys.argv = _argv
T, N, RES = H.T, H.N, H.RES
PC, PHONE = (1440, 900), (390, 844)
TMP = os.path.join(tempfile.gettempdir(), 'h_popjo_fix', 'p%d' % os.getpid())
MKON3 = ['제55조', '제132조의5', '제16조']
P7SIX = ['P7-0032', 'P7-0033', 'P7-0034', 'P7-0035', 'P7-1273', 'P7-1825']
B3JO = ['제27조', '제31조', '제48조']
INK1 = {'s': [{'c': '#D93B3B', 'w': 2, 'p': [[0.1, 0.1, 1], [0.2, 0.15, 1]]}], 'ts': '2026-10-02T00:00:00.000Z'}


def git(*a):
    return subprocess.run(['git', '-C', _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def base_data_overlay(rev):
    """바탕 데이터 = 지금 DATA 위에 git 판 rev 의 jo/data 가운데 바이트가 다른 파일만 덧판(126MB 를 다 꺼내지 않는다)"""
    d = os.path.join(TMP, 'bdata_' + rev)
    os.makedirs(d, exist_ok=True)
    QJ.sub('git:archive')   # 셈만 — 바탕 데이터 git 풀기(regress · smoke 는 0 이어야 한다)
    names = [x for x in git('ls-tree', '--name-only', rev, 'jo/data/').decode('utf-8').splitlines() if x.endswith('.json')]
    got = []
    for nm in names:
        f = nm.split('/')[-1]
        old = git('show', rev + ':' + nm)
        cur = os.path.join(DATA, f)
        if not os.path.exists(cur) or open(cur, 'rb').read() != old:
            open(os.path.join(d, f), 'wb').write(old)
            got.append(f)
    return d, got


# ════════════════════════ 서버 · 쪽(데이터 자리를 쪽마다) ════════════════════════
SERVERS = {}


def serve(tag, src, roots):
    if tag in SERVERS:
        return SERVERS[tag][1]
    body = H.inject(src).encode('utf-8')

    class Hd(SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            p = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
            if p in ('/jo/', '/jo/index.html'):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                self.wfile.write(body)
                return
            return super().do_GET()

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
            if p.startswith('/jo/data/'):
                parts = [x for x in p[len('/jo/data/'):].split('/') if x]
                for r in roots:
                    f = os.path.join(r, *parts)
                    if os.path.exists(f):
                        return f
                return os.path.join(roots[-1], *parts)
            for pre, root in (('/gichul/pdf/', H.EXAM), ('/__book/', H.MBP)):
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


class Pg(H.Pg):
    """H.Pg 와 같은 쪽(누름·기다림 도구 그대로) — 서버만 이 파일 것(데이터 자리) · route 끊기에서 blob: · data: 뺌(WebKit)"""

    def __init__(self, br, tag, src, roots, dev, ls=None):
        eng = br.browser_type.name
        W, Hh = dev
        touch = dev == PHONE
        self.eng, self.touch = eng, touch
        kw = dict(viewport={'width': W, 'height': Hh}, device_scale_factor=2 if touch else 1)
        if touch:
            kw.update(has_touch=True)
            if eng != 'webkit':
                kw['is_mobile'] = True
        self.ctx = br.new_context(**kw)
        self.ctx.route(lambda u: not (u.startswith('http://127.0.0.1') or u.startswith('blob:') or u.startswith('data:')), lambda r: r.abort())
        init = {'tt.cfg': json.dumps({'token': 'harness-token', 'person': '하네스'})}
        for k, v in (ls or {}).items():
            init[k] = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
        self.ctx.add_init_script("if(!sessionStorage.getItem('__h')){sessionStorage.setItem('__h','1');const I=%s;for(const k in I)localStorage.setItem(k,I[k]);}" % json.dumps(init, ensure_ascii=False))
        self.pg = self.ctx.new_page()
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append(str(e)))
        port = serve(tag, src, roots)
        self.pg.goto('http://127.0.0.1:%d/jo/index.html' % port)
        self.pg.wait_for_function("typeof S!=='undefined' && typeof busy!=='undefined' && !busy && document.querySelector('#slot .main, #slot .mbdash') && window.__RB", timeout=90000)
        self.idle()


# ════════════════════════ 재기(쪽 안) ════════════════════════
# 팝업 하나의 몸 — 제목 · 「이동 ↗」 · 줄 · 꾸밈 · 내 칠 · 「본문을 찾지 못했다」
SIG = r"""(pk) => { const p = POPS.find(x => x._pk === pk); if (!p) return null;
  const b = p.querySelector(':scope > .pb') || p, lines = [...b.querySelectorAll('.ln')];
  const deco = [];
  lines.forEach((ln, i) => ln.querySelectorAll('mark, u, strong, s, span[style], .lbl, .stkanc, sup.fn').forEach(e => {
    if (e.classList.contains('jmk') || e.closest('.jmk') && e.closest('.jmk') !== e && e.tagName === 'SPAN' && !e.className) return;
    if (e.classList.contains('jmk')) return;
    deco.push([i, e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().replace(/\s+/g, '.') : ''), e.getAttribute('style') || '', (e.textContent || '').slice(0, 24)]); }));
  return { title: ((p.querySelector('.pt') || {}).textContent || ''), go: !!p.querySelector('.ptgo'), chip: ((p.querySelector('.ptchip') || {}).textContent || ''),
    n: lines.length, wml: b.querySelectorAll('.ln.wml').length, text: lines.map(l => l.textContent).join('\n'), deco: deco, jmk: b.querySelectorAll('.jmk').length,
    nf: /본문을 찾지 못했다/.test(b.textContent || ''), body: (b.textContent || '').slice(0, 120), loading: /불러오는 중/.test(((p.querySelector('.pt') || {}).textContent || '')) }; }"""
OPEN = r"""async ([law, k]) => { try{ closeAllPops(true); }catch(e){} await popJo(law, k, null, 1);
  const pk = 'jo|' + law + '|' + k; await __RB.until(() => { const p = POPS.find(x => x._pk === pk); return p && !/불러오는 중/.test((p.querySelector('.pt') || {}).textContent || '') ? 1 : 0; }, 8000);
  await __RB.wait(60); return pk; }"""
WAITPOP = r"""async (pk) => { await __RB.until(() => { const p = POPS.find(x => x._pk === pk); return p && !/불러오는 중/.test((p.querySelector('.pt') || {}).textContent || '') && (p.querySelector(':scope > .pb') || {}).childNodes.length ? 1 : 0; }, 10000);
  await __RB.wait(120); return !!POPS.find(x => x._pk === pk); }"""

# C1 — 1차객 OX 풀(render 와 같은 규칙) → 앱 카드 함수로 짓고 popJo 가로채 누름 → (갈래 · 법 · 조)
C1_JS = r"""async (law) => {
  const subj = {'특허법': '특허', '상표법': '상표', '디자인보호법': '디보'}[law];
  await __RB.home(law);
  const JM = await get('jimun_' + subj + '.json');
  const P7 = law === '특허법' ? await get('jimun_7pan.json') : null;
  const mln = law === '특허법' && typeof MLN !== 'undefined' && MLN && MLN.ok;
  const note = { mln: mln, jokey: law !== '특허법' || !!JOKEY, p7lid: law !== '특허법' || !!P7LID };
  const pool = [];
  if (mln){ P7.지문.forEach(z => pool.push({ k: oxKeyP7(z), kind: 'P', z: z }));
    Object.keys(MLN.obj).forEach(id => { const o = MLN.obj[id]; pool.push({ k: oxKeyP7(o), kind: 'O', o: o }); });
    JM.문제.filter(q => MLN.lidnode[q.id] != null).concat(JM.문제.filter(q => MLN.lidnode[q.id] == null)).forEach(q => (q.지문 || []).forEach(z => { const c = mlnClass(q, z); if (c === 'a') return;
      pool.push({ k: oxKeyLid(q, z), kind: 'L', q: q, z: z, ln: c }); })); }
  else { JM.문제.forEach(q => (q.지문 || []).forEach(z => pool.push({ k: oxKeyLid(q, z), kind: 'L', q: q, z: z })));
    if (P7) P7.지문.forEach(z => { if (z.병합) return; pool.push({ k: oxKeyP7(z), kind: 'P', z: z }); }); }
  const seen = new Set(), cells = pool.filter(c => { if (seen.has(c.k)) return false; seen.add(c.k); return true; });
  const rec = [], orig = popJo; let cur = '', nCard = { P: 0, L: 0 }, qDone = new Set();
  popJo = function(l, k){ rec.push([cur, l, k]); };
  try {
    for (const c of cells){
      let card = null, tag = '';
      if (c.kind === 'P'){ card = p7Card(c.z, 1); tag = '7판'; }
      else if (c.kind === 'L'){
        if (mln) card = mlnLidCard(c.q, c.z, 1, c.ln, MLN.lidnode[c.q.id]);
        else { if (qDone.has(c.q.id)) continue; qDone.add(c.q.id); card = qCard(c.q, null, 1); }
        tag = '리담'; }
      else continue;
      nCard[c.kind]++;
      card.querySelectorAll('.mbtype .seg.jo').forEach(b => { cur = tag + '·유형 칩'; b.click(); });
      card.querySelectorAll('.mbchips .c2jb').forEach(b => {
        if (/^＋\d+/.test((b.textContent || '').trim())){ cur = tag + '·근거 조 칩(＋N 목록)'; b.click();
          const pp = POPS[POPS.length - 1]; if (pp){ pp.querySelectorAll('.lnkrow').forEach(r => r.click()); closeOne(pp); } return; }
        cur = tag + (c.kind === 'P' ? '·해설 조 칩' : '·근거 조 칩'); b.click(); });
    }
  } finally { popJo = orig; }
  try{ closeAllPops(true); }catch(e){}
  return { note: note, cells: cells.length, cards: nCard, rec: rec }; }"""
CLASSIFY = r"""async (pairs) => { const out = {};
  for (const [law, k] of pairs){ try{ closeAllPops(true); }catch(e){}
    try { await popJo(law, k, null, 1); } catch(e){ out[law + '|' + k] = 'err:' + e; continue; }
    const pk = 'jo|' + law + '|' + k;
    await __RB.until(() => { const p = POPS.find(x => x._pk === pk); return p && !/불러오는 중/.test((p.querySelector('.pt') || {}).textContent || '') ? 1 : 0; }, 6000);
    const p = POPS.find(x => x._pk === pk), b = p && p.querySelector(':scope > .pb'), t = b ? (b.textContent || '') : '';
    out[law + '|' + k] = !p ? 'nopop' : /본문을 찾지 못했다/.test(t) ? 'nf' : (/^제\d+조(의\d+)? 삭제 </.test(t.trim()) && b.querySelectorAll('.ln.wml').length === 1) ? 'del' : /읽지 못했다/.test(t) ? 'err' : 'ok'; }
  try{ closeAllPops(true); }catch(e){}
  return out; }"""


def c1_count(p, law):
    r = p.ev(C1_JS, law)
    pairs = sorted(set((x[1], x[2]) for x in r['rec']))
    cls = {}
    for i in range(0, len(pairs), 80):
        cls.update(p.ev(CLASSIFY, [list(x) for x in pairs[i:i + 80]]))
    by = {}
    for src, l, k in r['rec']:
        c = cls.get(l + '|' + k, '?')
        by.setdefault(c, {}).setdefault(src, 0)
        by[c][src] += 1
    nf = [(src, l, k) for src, l, k in r['rec'] if cls.get(l + '|' + k) == 'nf']
    nfk = {}
    for src, l, k in nf:
        nfk[l + ' ' + k] = nfk.get(l + ' ' + k, 0) + 1
    dl = {}
    for src, l, k in r['rec']:
        if cls.get(l + '|' + k) == 'del':
            dl[l + ' ' + k] = dl.get(l + ' ' + k, 0) + 1
    return {'칸': r['cells'], '카드': r['cards'], '누름': len(r['rec']), '(법·조)': len(pairs), '갈래': by, '못찾음 칩': len(nf), '못찾음 조': nfk,
            '삭제 줄 칩': sum(dl.values()), '삭제 조': dl, 'note': r['note'], 'err': [k for k, v in cls.items() if v not in ('ok', 'nf', 'del')][:6]}


def run_c1(br, src_new, src_base, newroots, baseroots):
    G = 'C1'
    rows = {}
    for nm, src, roots in ((('새', src_new, newroots), ('바탕 앱 · 같은 데이터', src_base, newroots), ('바탕 앱 · 바탕 데이터', src_base, baseroots)) if QJ.GATE else (('새', src_new, newroots),)):   # regress · smoke — 바탕 앱 둘은 안 띄운다
        QJ.launch('new' if nm == '새' else 'base')
        p = Pg(br, 'c1' + nm, src, roots, PC)
        rows[nm] = {law: c1_count(p, law) for law in ('특허법', '상표법', '디자인보호법')}
        rows[nm]['JS 오류'] = p.errs[:3]
        p.close()
    tot = {nm: sum(rows[nm][law]['못찾음 칩'] for law in ('특허법', '상표법', '디자인보호법')) for nm in rows}
    for nm in rows:
        N(G, '%s — 법마다 칸 · 카드 · 누름 · 못찾음 · 삭제 줄' % nm, {law: {k: v for k, v in rows[nm][law].items() if k in ('칸', '카드', '누름', '(법·조)', '못찾음 칩', '못찾음 조', '삭제 줄 칩', '삭제 조', 'note', 'err')} for law in ('특허법', '상표법', '디자인보호법')})
        N(G, '%s — 갈래(결과 → 누른 자리 → 칩 수)' % nm, {law: rows[nm][law]['갈래'] for law in ('특허법', '상표법', '디자인보호법')})
    T(G, '세 법 1차객 카드 jo 칩·유형 칩·해설 조 칩 → popJo 「본문을 찾지 못했다」 칩 셈 = 0', tot['새'] == 0 and not rows['새']['JS 오류'],
      {'새': tot['새'], '못찾음 조(새)': {law: rows['새'][law]['못찾음 조'] for law in ('특허법', '상표법', '디자인보호법') if rows['새'][law]['못찾음 조']}, 'JS 오류': rows['새']['JS 오류']})
    if QJ.GATE:   # 관문만 — 헛잣대 Y1 · 옛 앱 + 새 데이터(바탕 앱을 띄워야 뜻이 있다)
        T('Y1', 'C1 헛잣대(바탕 앱 83c230f · 같은 데이터) = FAIL(물림)', tot['바탕 앱 · 같은 데이터'] > 0, {'바탕 앱 · 같은 데이터': tot['바탕 앱 · 같은 데이터'], '바탕 앱 · 바탕 데이터(§0-3 61 + α)': tot['바탕 앱 · 바탕 데이터']})
        T(G, '옛 앱(83c230f) + 새 데이터(목록 새 칸 「삭제」 · 디-331 뺀 jimun_디보) — 세 법 1차객 카드를 다 지어 눌러도 JS 오류 0(열어 둔 탭 · 옛 판 기기)',
          not rows['바탕 앱 · 같은 데이터']['JS 오류'] and all(rows['바탕 앱 · 같은 데이터'][law]['누름'] == rows['새'][law]['누름'] for law in ('특허법', '상표법', '디자인보호법')),
          {'JS 오류': rows['바탕 앱 · 같은 데이터']['JS 오류'], '누름(옛 앱 = 새 앱)': {law: [rows['바탕 앱 · 같은 데이터'][law]['누름'], rows['새'][law]['누름']] for law in ('특허법', '상표법', '디자인보호법')}})
    # 삭제 조 갈래 — 새 판에서 삭제 줄로 열린 칩 = 바탕(같은 데이터)에서 못 찾던 삭제 조 칩
    dl_new = sum(rows['새'][law]['삭제 줄 칩'] for law in ('특허법', '상표법', '디자인보호법'))
    DLK = {law: set(json.load(open(os.path.join(DATA, 'jo_%s_목록.json' % law), encoding='utf-8')).get('삭제') or {}) for law in ('특허법', '상표법', '디자인보호법')}
    nf_del_new = sum(v for law in DLK for lk, v in rows['새'][law]['못찾음 조'].items() if lk.split(' ', 1)[1] in DLK[law])
    nf_del_base = sum(v for law in DLK for lk, v in rows['바탕 앱 · 같은 데이터'][law]['못찾음 조'].items() if lk.split(' ', 1)[1] in DLK[law]) if QJ.GATE else None
    rest = {law: {lk: v for lk, v in rows['새'][law]['못찾음 조'].items() if lk.split(' ', 1)[1] not in DLK[law]} for law in DLK}
    if QJ.GATE:
        T(G, 'C1a 삭제 조 칩(§B-1 몫) — 「본문을 찾지 못했다」 0 · 모두 「제N조 삭제 <날짜>」 줄 · 디-331 칩 0(데이터에서 뺌)',
          nf_del_new == 0 and dl_new == nf_del_base and dl_new > 0 and not any('제331조' in lk for law in DLK for lk in rows['새'][law]['못찾음 조']),
          {'새 삭제 줄 칩': dl_new, '새 삭제 조 못찾음': nf_del_new, '바탕(같은 데이터) 삭제 조 못찾음': nf_del_base,
           '디-331(바탕 데이터 · 바탕 앱)': rows['바탕 앱 · 바탕 데이터']['디자인보호법']['못찾음 조'].get('디자인보호법 제331조', 0)})
    else:   # regress · smoke — 바탕 앱 값(nf_del_base) 대신 기준 스냅샷의 「삭제 줄 칩 수」(삭제 조 칩이 삭제 줄로 열리는 수 무변)
        dl_eq = QJ.same('C1a@삭제줄칩', dl_new)
        T(G, 'C1a 삭제 조 칩(§B-1 몫) — 「본문을 찾지 못했다」 0 · 모두 「제N조 삭제 <날짜>」 줄 · 디-331 칩 0(데이터에서 뺌)',
          nf_del_new == 0 and dl_eq and dl_new > 0 and not any('제331조' in lk for law in DLK for lk in rows['새'][law]['못찾음 조']),
          {'새 삭제 줄 칩': dl_new, '새 삭제 조 못찾음': nf_del_new, '기준(지난 판 삭제 줄 칩)': QJ.base('C1a@삭제줄칩', dl_new), '기준 출처': QJ.base_note('C1a@삭제줄칩')})
    N(G, 'C1 남은 못찾음(삭제 조 밖 · 이 판 자리 밖) — 갈래', {'조': {law: v for law, v in rest.items() if v},
      '까닭': {'施規': '7판 유형 칩(mbTypeChip)이 「施規 N」 조각도 popJo(S.law, \'施規\') 로 연다(해설 조 칩은 누름 없음)',
              '제267조': '7판 해설 「(民法267)」 → p7Jo 「法 N」 갈래(JOKEY 안 봄) → 특허법 제267조',
              '제22조의2': '7판 해설 「(法22의2①)」(실용신안법) → p7Jo 「法 N」 갈래 → 특허법 제22조의2'}})
    if QJ.GATE:
        N(G, '삭제 조 칩 — 새 판에서 「제N조 삭제 <날짜>」 로 열린 칩 · 바탕 데이터의 디-331 은 데이터에서 뺌', {'새 삭제 줄 칩': dl_new, '새 못찾음': tot['새'],
          '바탕(같은 데이터) 못찾음': tot['바탕 앱 · 같은 데이터'], '바탕(바탕 데이터) 못찾음': tot['바탕 앱 · 바탕 데이터']})
    else:
        N(G, '삭제 조 칩 — 새 판에서 「제N조 삭제 <날짜>」 로 열린 칩 · 바탕 데이터의 디-331 은 데이터에서 뺌', {'새 삭제 줄 칩': dl_new, '새 못찾음': tot['새']})
    return rows


# ════════════════════════ C2 — T2461181 「유형? · 26」 ════════════════════════
C2_AT = r"""async () => { const sel = await __RB.goKey('T2461181'); await __RB.wait(300);
  const card = document.getElementById('qb-T2461181'); if (!card) return { sel: sel, card: false };
  const seg = [...card.querySelectorAll('.mbtype .seg.jo')].find(b => (b.textContent || '').trim() === '26');
  const ty = card.querySelector('.mbtype .seg.ty');
  return { sel: sel, card: true, ty: ty ? (ty.textContent || '').trim() : null, at: seg ? __RB.hitOn(seg) : null }; }"""
FONT = r"""(pk) => { const p = POPS.find(x => x._pk === pk); const l = p && p.querySelector(':scope > .pb .ln.wml'); if (!l) return null; const cs = getComputedStyle(l);
  return [cs.fontSize, cs.fontFamily, cs.lineHeight, cs.fontWeight, cs.color]; }"""


def run_c2(br, src, roots, want_date, tag, shots=None):
    out = {}
    pk = 'jo|특허법|제26조'
    for dn, dev in (('폰390', PHONE), ('PC', PC)):
        p = Pg(br, 'c2' + tag + dn, src, roots, dev)
        a = p.ev(C2_AT)
        pressed = p.press(a.get('at') if a else None, 500)
        p.ev(WAITPOP, pk)
        s = p.ev(SIG, pk)
        f = p.ev(FONT, pk)
        if shots and dn == '폰390' and s:
            os.makedirs(shots, exist_ok=True)
            fn = os.path.join(shots, '_shot_popjo_fix_C2_%s_폰390.png' % tag)
            p.pg.screenshot(path=fn)
            out['그림'] = fn
        p.ev(OPEN, ['특허법', '제25조'])
        f0 = p.ev(FONT, 'jo|특허법|제25조')
        out[dn] = {'카드': a and a.get('card'), '유형 칩': a and a.get('ty'), '누름': pressed, '팝업': s, '글꼴': f, '보통 조(제25조) 글꼴': f0, 'JS 오류': p.errs[:3]}
        p.close()
    want_t, want_b = '특허법 제26조 (삭제)', '제26조 삭제 <%s>' % want_date
    ok = {}
    for dn in ('폰390', 'PC'):
        d = out[dn]
        s = d['팝업'] or {}
        ok[dn] = bool(d['누름'] and s and s.get('title') == want_t and not s.get('go') and s.get('n') == 1 and s.get('wml') == 1 and (s.get('text') or '').strip() == want_b
                      and not s.get('nf') and d['글꼴'] and d['글꼴'] == d['보통 조(제25조) 글꼴'] and not d['JS 오류'])
    return ok, out


# ════════════════════════ C3 — 필기 조 꾸밈 ════════════════════════
PICK = r"""async () => { await __RB.jo('특허법', '제1조', true);
  const L = await get('jo_특허법_목록.json'), B = await get('jo_특허법_본문.json');
  const pin = {}; for (const x of L.조){ const j = B.조[x.k]; if (!j) continue; try { const X = popWmCtx('특허법', x.k, j, L); pin[x.k] = X.b.items.filter(it => it.g === 'mk' && WM_PINOK[it.sub]).length; } catch(e){ pin[x.k] = -1; } }
  return pin; }"""
# 지도 누름 — 그 그릇 안 요소마다 popJo 를 가로채 한 번 눌러 (법 · 조)를 읽는다(누름 = 앱 손잡이 그대로 · 팝업은 안 뜬다)
MAP = r"""(A) => { const root = A.root === 'last' ? POPS[POPS.length - 1] : document.querySelector(A.root); if (!root) return [];
  const els = [...root.querySelectorAll(A.sel)].filter(e => !/^＋/.test((e.textContent || '').trim())); const orig = popJo, out = []; let last = null;
  popJo = function(l, k){ last = [l, k]; };
  try { els.forEach((e, i) => { last = null; try{ e.click(); }catch(x){} if (last) out.push([i, last[0], last[1], (e.textContent || '').trim().slice(0, 16)]); }); } finally { popJo = orig; }
  return out; }"""
MARKAT = r"""(A) => { const root = A.root === 'last' ? POPS[POPS.length - 1] : document.querySelector(A.root); if (!root) return null;
  const els = [...root.querySelectorAll(A.sel)].filter(e => !/^＋/.test((e.textContent || '').trim())); const e = els[A.i]; if (!e) return null; return __RB.hitOn(e); }"""
# 여는 자리 다섯의 과녁 — 유형·근거(리담 Z 카드 · z.jo 첫 코드) · 2차 카드(사례 · 기출 카드 팝업 .c2jb) · 테마(창 .wmlk) · 본문 조 링크(조문 화면 .wmlk)
TARGETS = r"""async (A) => { const pin = A.pin, skip = new Set(A.skip), ok = k => (pin[k] || 0) > 0 && !skip.has(k); const out = {};
  await __RB.home('특허법');
  const JM = await get('jimun_특허.json');
  for (const q of JM.문제){ if (MLN.lidnode[q.id] == null) continue; for (const z of (q.지문 || [])){ if (!z.uid || mlnClass(q, z) === 'a') continue; const c = (z.jo || [])[0];
      if (!c || c.split('-')[0] !== '특') continue; const k = joCode(c); if (ok(k)){ out.card = { uid: z.uid, k: k, code: c }; break; } } if (out.card) break; }
  const orig = popJo;
  for (const kind of ['사례', '기출']){ let CH = null; try{ CH = await get('2cha_본문_' + kind + '_특허.json'); }catch(e){ continue; }
    for (const nm of Object.keys(CH)){ try{ closeAllPops(true); }catch(e){} try{ await popCard4(kind, nm, null, 1); }catch(e){ continue; } await __RB.wait(120);
      const w = POPS[POPS.length - 1]; if (!w) continue; const els = [...w.querySelectorAll('.c2jb')]; let last = null;
      popJo = function(l, k){ last = [l, k]; };
      try { for (let i = 0; i < els.length; i++){ last = null; try{ els[i].click(); }catch(x){} if (last && last[0] === '특허법' && ok(last[1])){ out.c2 = { kind: kind, name: nm, k: last[1], i: i, txt: (els[i].textContent || '').trim() }; break; } } } finally { popJo = orig; }
      if (out.c2) break; }
    if (out.c2) break; }
  try{ closeAllPops(true); }catch(e){}
  await __RB.jo('특허법', '제1조', true);
  for (let i = 0; i < 200 && !(typeof TM === 'object' && TM && TM.d && TM.d.themes && TM.d.themes.length); i++) await __RB.wait(50);
  if (typeof TM === 'object' && TM && TM.d && TM.d.themes){ for (const t of TM.d.themes){ try{ closeAllPops(true); tmWin(t.id, null); }catch(e){ continue; }
      const w = await __RB.until(() => POPS.find(x => x._pk === 'theme|' + t.id), 3000); if (!w) continue; await __RB.wait(80);
      const a = [...w.querySelectorAll('.wmlk')].find(e => (e.dataset.law || TM_LAW) === '특허법' && ok(e.dataset.k || ''));
      if (a){ out.theme = { id: t.id, k: a.dataset.k, txt: (a.textContent || '').slice(0, 20) }; break; } }
    try{ closeAllPops(true); }catch(e){} }
  else out.themeNote = '테마 재료 없음';
  const L = await get('jo_특허법_목록.json'), B = await get('jo_특허법_본문.json');
  for (const x of L.조){ const j = B.조[x.k]; if (!j || skip.has(x.k)) continue; const ts = []; (j.행 || []).forEach(r => (r.e || []).forEach(e => { if (e.k === 'L' && e.j && e.j !== x.k && ok(e.j)) ts.push(e.j); }));
    if (ts.length){ out.body = { from: x.k, k: ts[0] }; break; } }
  return out; }"""


def seed(ink_keys, mkon=None, jomark=None):
    ls = {}
    if ink_keys:
        ls['jopangi.ink'] = {'jo|특허법:' + k: INK1 for k in ink_keys}
    if mkon:
        ls['jopangi.mkon'] = mkon
    if jomark:
        ls['jopangi.jomark'] = jomark
    return ls


def sig_of(p, k):
    p.ev(OPEN, ['특허법', k])
    return p.ev(SIG, 'jo|특허법|' + k)


def find_at(p, root, sel, k):
    """그릇 안 요소 가운데 (특허법 · k)를 여는 것을 지도 누름으로 찾아 그 자리(hitOn)"""
    m = p.ev(MAP, {'root': root, 'sel': sel})
    hit = [x for x in m if x[1] == '특허법' and x[2] == k]
    if not hit:
        return None, m
    return p.ev(MARKAT, {'root': root, 'sel': sel, 'i': hit[0][0]}), m


def press_place(p, place, tg):
    """여는 자리 하나를 진짜 누름 → 팝업 몸(SIG)"""
    k = tg['k']
    pk = 'jo|특허법|' + k
    p.ev("() => { try{ closeAllPops(true); }catch(e){} }")
    if place in ('유형 칩', '근거 조 칩'):
        p.ev("async u => { await __RB.goKey(u); await __RB.wait(250); }", tg['uid'])
        root = '#qb-' + tg['uid']
        if place == '유형 칩':
            at, m = find_at(p, root, '.mbtype .seg.jo', k)
        else:
            p.ev("r => { const c = document.querySelector(r); const b = c && c.querySelector('.mbpeek'); if (b && /▸/.test(b.textContent)) b.click(); }", root)
            p.wait(250)
            at, m = find_at(p, root, '.mbchips .c2jb', k)
    elif place == '2차 카드 조 링크':
        p.ev("async a => { S.law = '특허법'; S.tab = 'cha2'; await render(); await __RB.idle(); try{ closeAllPops(true); }catch(e){} await popCard4(a[0], a[1], null, 1); await __RB.wait(600); }", [tg['kind'], tg['name']])
        at, m = find_at(p, 'last', '.c2jb', k)
    elif place == '테마':
        p.ev("async () => { await __RB.jo('특허법', '제1조', true); for (let i = 0; i < 200 && !(typeof TM === 'object' && TM && TM.d && TM.d.themes && TM.d.themes.length); i++) await __RB.wait(50); }")
        p.ev("async id => { try{ closeAllPops(true); }catch(e){} tmWin(id, null); await __RB.until(() => POPS.find(x => x._pk === 'theme|' + id), 3000); await __RB.wait(150); }", tg['id'])
        at, m = find_at(p, 'last', '.wmlk', k)
    else:   # 본문 조 링크
        p.ev("async v => { await __RB.jo('특허법', v, true); }", tg['from'])
        at, m = find_at(p, '#slot .main .box', '.wmlk', k)
    p.ev("() => { [...POPS].filter(x => /^jo\\|/.test(x._pk || '')).forEach(x => closeOne(x)); }")
    pressed = p.press(at, 500)
    p.ev(WAITPOP, pk)
    s = p.ev(SIG, pk)
    return {'누름': pressed, '자리': (at or {}).get('t') if at else None, '지도': len(m or []), '팝업': s}


def run_c3(br, src_new, src_base, roots):
    G = 'C3'
    rec = {}
    try:
        R = json.load(open(os.path.join(SPD, 'jopangi', '기록.json'), encoding='utf-8'))
        rec = (R.get('data') or R).get('jopangi.mkon') or {}
    except Exception as e:
        N(G, 'studyplandata 기록 못 읽음', str(e)[:160])
    mkon = {('특허법:' + k): rec['특허법:' + k] for k in MKON3 if ('특허법:' + k) in rec}
    N(G, 'mkon 기록(studyplandata jopangi/기록.json · 읽기만)', {'켠 조': sorted(mkon), '열쇠 수': {k: sum(len(v.get(x) or []) for x in ('k', 's', 'x')) for k, v in mkon.items()}})
    QJ.launch('new')
    p = Pg(br, 'c3pick', src_new, roots, PC)
    pin = p.ev(PICK)
    cand = sorted([k for k, n in pin.items() if n > 0 and k not in MKON3], key=lambda k: (-pin[k], k))
    sample = cand[:3]
    tg = p.ev(TARGETS, {'pin': pin, 'skip': MKON3 + sample})
    rowk = p.ev("async k => { const B = await get('jo_특허법_본문.json'); const r = (B.조[k].행 || []).find(r => r.k[0] !== 'H' && (r.t || '').length > 6); return r ? rowKey(r) : null; }", sample[0]) if sample else None
    p.close()
    N(G, '표본 · 과녁', {'꾸밈 다섯 든 조(바탕이 켜던 수)': {k: pin[k] for k in sample}, '여는 자리 과녁': tg, '꾸밈 든 조 수': len([k for k, n in pin.items() if n > 0])})
    jm = {'특허법:%s|%s' % (sample[0], rowk): [[0, 4, 'y']]} if rowk else None
    places = [('유형 칩', tg.get('card')), ('근거 조 칩', tg.get('card')), ('2차 카드 조 링크', tg.get('c2')), ('테마', tg.get('theme')), ('본문 조 링크', tg.get('body'))]
    inkk = sorted(set(sample + MKON3 + [t['k'] for _, t in places if t]))
    S3 = {}
    for nm, src, ink in ((('새 · 필기', src_new, True), ('새 · 필기 없음', src_new, False), ('바탕 · 필기', src_base, True)) if QJ.GATE else (('새 · 필기', src_new, True), ('새 · 필기 없음', src_new, False))):   # regress · smoke — 바탕 앱 쪽은 안 띄운다
        QJ.launch('base' if nm.startswith('바탕') else 'new')
        q = Pg(br, 'c3' + nm, src, roots, PC, ls=seed(inkk if ink else [], mkon, jm))
        S3[nm] = {k: sig_of(q, k) for k in sample + MKON3}
        S3[nm]['__err'] = q.errs[:3]
        q.close()
    # ① 표본 3 — 필기 + 기록 없음 = 꾸밈 0 · 글 = 필기 없을 때
    if QJ.GATE:
        a = {k: {'꾸밈(새·필기)': len((S3['새 · 필기'][k] or {}).get('deco') or []), '꾸밈(바탕·필기)': len((S3['바탕 · 필기'][k] or {}).get('deco') or []),
                 '글 같음(필기 有無)': (S3['새 · 필기'][k] or {}).get('text') == (S3['새 · 필기 없음'][k] or {}).get('text'), '줄': (S3['새 · 필기'][k] or {}).get('n')} for k in sample}
    else:   # regress · smoke — 바탕·필기 칸이 없다
        a = {k: {'꾸밈(새·필기)': len((S3['새 · 필기'][k] or {}).get('deco') or []),
                 '글 같음(필기 有無)': (S3['새 · 필기'][k] or {}).get('text') == (S3['새 · 필기 없음'][k] or {}).get('text'), '줄': (S3['새 · 필기'][k] or {}).get('n')} for k in sample}
    T(G, '필기 있는 조 + mkon 없음 표본 3 — 팝업 꾸밈 0 · 글 = 필기 없을 때와 같음(원문 줄만)', len(sample) == 3 and all(v['꾸밈(새·필기)'] == 0 and v['글 같음(필기 有無)'] and (v['줄'] or 0) > 0 for v in a.values()), a)
    if QJ.GATE:   # 관문만 — 헛잣대 Y3(바탕 앱 · 같은 필기)
        T('Y3', 'C3 표본 헛잣대(바탕 앱 · 같은 필기) = 꾸밈 > 0(물림)', all(v['꾸밈(바탕·필기)'] > 0 for v in a.values()), {k: v['꾸밈(바탕·필기)'] for k, v in a.items()})
    # ② mkon 켠 조 — 필기 있어도 없을 때와 같은 꾸밈(켠 것만) · 꾸밈 > 0
    b = {}
    for k in MKON3:
        s1, s0, sb = S3['새 · 필기'][k] or {}, S3['새 · 필기 없음'][k] or {}, ((S3.get('바탕 · 필기') or {}).get(k) or {})   # regress · smoke 는 바탕·필기 칸이 없다 → {}
        b[k] = {'기록': ('특허법:' + k) in mkon, '꾸밈(새·필기)': len(s1.get('deco') or []), '꾸밈(새·필기 없음)': len(s0.get('deco') or []), '같음': s1.get('deco') == s0.get('deco') and s1.get('text') == s0.get('text'),
                '바탕 같음': sb.get('deco') == s1.get('deco'), '꼴': sorted(set(x[1] for x in (s1.get('deco') or [])))}
    if QJ.REGRESS:   # 바탕·필기 칸이 없어 「바탕 같음」(헛잣대 INFO 몫)은 뺀다
        for v in b.values():
            v.pop('바탕 같음', None)
    T(G, 'mkon 켠 조(특허 제55조 · 제132조의5 · 제16조) — 필기 있어도 없을 때와 같은 꾸밈(켠 것만 · > 0)', all(v['기록'] and v['같음'] and v['꾸밈(새·필기)'] > 0 for v in b.values()), b)
    if QJ.GATE:   # 관문만 — 헛잣대 Y3 INFO
        N('Y3', 'mkon 켠 조 헛잣대 — 기록 있는 조는 옛 판도 켠 것만이라 바탕 = 새(안 물림 · 무변 확인)', {k: v['바탕 같음'] for k, v in b.items()})
    # ③ jomark 칠 = 그대로
    if jm:
        k0 = sample[0]
        c = {nm: (S3[nm][k0] or {}).get('jmk') for nm in S3 if nm != '__err'}
        if QJ.GATE:
            T(G, 'jomark 칠 = 그대로(%s 첫 줄 · 새·필기 = 새·필기 없음 = 바탕·필기 · > 0)' % k0, len(set(c.values())) == 1 and list(c.values())[0] > 0, c)
        else:   # regress · smoke — 바탕·필기 값 = 기준 스냅샷(새·필기 = 새·필기 없음 = 기준 · > 0)
            vals = list(c.values())
            v0 = vals[0] if vals else None
            eq = QJ.same('C3@jomark', v0)
            c['기준'] = QJ.base_note('C3@jomark')
            T(G, 'jomark 칠 = 그대로(%s 첫 줄 · 새·필기 = 새·필기 없음 = 바탕·필기 · > 0)' % k0, len(set(vals)) == 1 and v0 is not None and v0 > 0 and eq, c)
    else:
        T(G, 'jomark 칠 — 칠할 줄 못 찾음', False, sample)
    # ④ 여는 자리 다섯 — 진짜 누름(PC 마우스)
    pl = {}
    for nm, src in ((('새', src_new), ('바탕', src_base)) if QJ.GATE else (('새', src_new),)):   # regress · smoke — 바탕 앱은 안 띄운다
        QJ.launch('base' if nm == '바탕' else 'new')
        q = Pg(br, 'c3pl' + nm, src, roots, PC, ls=seed(inkk, mkon, jm))
        for place, t in places:
            if not t:
                pl.setdefault(place, {})[nm] = {'과녁': None}
                continue
            try:
                r = press_place(q, place, t)
            except Exception as e:
                r = {'누름': False, 'err': str(e).splitlines()[0][:160]}
            s = r.get('팝업') or {}
            pl.setdefault(place, {})[nm] = {'과녁': t['k'], '누름': r.get('누름'), '꾸밈': len(s.get('deco') or []) if s else None, '줄': s.get('n') if s else None, '제목': s.get('title') if s else None, 'err': r.get('err')}
        pl.setdefault('__err', {})[nm] = q.errs[:3]
        q.close()
    good = all(pl[pc]['새'].get('누름') and pl[pc]['새'].get('꾸밈') == 0 and (pl[pc]['새'].get('줄') or 0) > 0 for pc, _ in places)
    T(G, '여는 자리 다섯(유형 칩 · 근거 조 칩 · 2차 카드 조 링크 · 테마 · 본문 조 링크) 진짜 누름 — 필기 조 팝업 꾸밈 0', good and not pl['__err']['새'], {pc: pl[pc]['새'] for pc, _ in places})
    if QJ.GATE:   # 관문만 — 헛잣대 Y3(바탕 앱)
        T('Y3', '여는 자리 다섯 헛잣대(바탕 앱) = 꾸밈 > 0(물림)', all((pl[pc]['바탕'].get('꾸밈') or 0) > 0 for pc, _ in places), {pc: pl[pc]['바탕'] for pc, _ in places})
    if S3['새 · 필기']['__err'] or S3['새 · 필기 없음']['__err']:
        T(G, 'JS 오류 0', False, [S3['새 · 필기']['__err'], S3['새 · 필기 없음']['__err']])
    return {'표본': a, 'mkon': b, '자리': pl}


# ════════════════════════ C4 — §B-3 7판 6 곳 ════════════════════════
C4_JS = r"""async (A) => { await __RB.home('특허법'); const P7 = await get('jimun_7pan.json'); const out = {};
  for (const id of A.ids){ const z = P7.지문.find(x => x.id === id); if (!z){ out[id] = null; continue; }
    const lk = (P7LID || {})[z.id], ex = lk ? (lk.z.jo || []) : [];
    const jos = p7Jo(z.sol, ex).map(x => (x.law ? '' : '×') + x.k);
    const rec = [], orig = popJo; popJo = function(l, k){ rec.push(l + ' ' + k); };
    try { const card = p7Card(z, 1); card.querySelectorAll('.mbtype .seg.jo, .mbchips .c2jb').forEach(b => { if (!/^＋/.test(b.textContent.trim())) b.click(); }); } finally { popJo = orig; }
    const s = joPrep(z.sol || '') + ' ' + joPrep(z.t || '');
    const sol = joPrep(z.sol || ''), chain = {};
    rec.forEach(x => { const k = x.replace(/^특허법 /, ''); if (chain[k]) return; const m = /^제(\d+)조(?:의(\d+))?$/.exec(k); if (!m) return;
      const rx = new RegExp('(?:제\\s?' + m[1] + '조' + (m[2] ? '의\\s?' + m[2] : '(?!\\s*의\\s*\\d)') + '|法\\s*' + m[1] + (m[2] ? '\\s*의\\s*' + m[2] : '(?![0-9의])') + ')'); const mm = rx.exec(sol);
      chain[k] = mm ? { 앞: sol.slice(Math.max(0, mm.index - 36), mm.index).replace(/\s+/g, ' '), 꼴: mm[0], wmAutoOther: wmAutoOther(sol.slice(Math.max(0, mm.index - 160), mm.index)) } : null; });
    out[id] = { jos: jos, clicks: rec, chain: chain, hit: rec.filter(x => A.bad.some(k => x === '특허법 ' + k)),
      why: A.bad.filter(k => s.indexOf(k) >= 0).map(k => [k, 'joOtherLaw ' + joOtherLaw(z.sol || '', k.replace(/^제/, '').replace(/조/, ''), '특허법'), 'JOKEY ' + !!(JOKEY && JOKEY[k])]) }; }
  try{ closeAllPops(true); }catch(e){} return out; }"""


def run_c4(br, src_new, src_base, roots):
    G = 'C4'
    res = {}
    for nm, src in ((('새', src_new), ('바탕', src_base)) if QJ.GATE else (('새', src_new),)):   # regress · smoke — 바탕 앱은 안 띄운다
        QJ.launch('base' if nm == '바탕' else 'new')
        p = Pg(br, 'c4' + nm, src, roots, PC)
        res[nm] = p.ev(C4_JS, {'ids': P7SIX, 'bad': B3JO})
        res[nm]['__err'] = p.errs[:3]
        p.close()
    hn = sum(len((v or {}).get('hit') or []) for k, v in res['새'].items() if k != '__err')
    hb = sum(len((v or {}).get('hit') or []) for k, v in res['바탕'].items() if k != '__err') if QJ.GATE else None
    T(G, '§B-3 7판 6 곳 — 카드 칩이 특허법 제27조 · 제31조 · 제48조로 잇는 것 0', hn == 0 and all(res['새'].get(i) for i in P7SIX) and not res['새']['__err'],
      {i: {'칩': (res['새'][i] or {}).get('clicks'), 'p7Jo': (res['새'][i] or {}).get('jos')} for i in P7SIX})
    if QJ.GATE:   # 관문만 — 헛잣대 Y4 INFO(바탕 앱)
        N('Y4', 'C4 바탕(83c230f) 도 %d — %s' % (hb, '「이미 막힘」(코드 무변)' if hb == 0 else '바탕은 이었다'), {i: (res['바탕'][i] or {}).get('why') for i in P7SIX})
    N(G, '6 곳 카드 칩 조마다 해설에 처음 나온 자리의 앞 글 · 앱 원문 줄 규칙(wmAutoOther · 다른 법 사슬) 판정 — 사람이 읽어 가를 재료(지시서 §B-3 밖은 사용자 결정)',
      {i: (res['새'][i] or {}).get('chain') for i in P7SIX if (res['새'][i] or {}).get('chain')})
    return res


# ════════════════════════ 돌림 ════════════════════════
def main():
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    os.makedirs(TMP, exist_ok=True)
    src_new = H.app_src(NEW)
    if QJ.GATE:
        src_base = H.app_src(BASE)
        QJ.sub('git:show-app')
        bd, changed = base_data_overlay(BDREV)
        newroots, baseroots = [DATA], [bd, DATA]
    else:   # regress · smoke — 바탕 앱 · 바탕 데이터(git 풀기 · 현재 데이터와 바이트 대조)는 안 푼다
        src_base, bd, changed = None, None, []
        newroots, baseroots = [DATA], None
    L = json.load(open(os.path.join(DATA, 'jo_특허법_목록.json'), encoding='utf-8'))
    want_date = (L.get('삭제') or {}).get('제26조')
    if QJ.GATE:
        N('C0', '재료', {'앱': NEW, '바탕 앱': BASE, '데이터': DATA, '바탕 데이터': '%s(바뀐 파일 %d 덧판: %s)' % (BDREV, len(changed), ', '.join(changed)),
                        '목록 삭제 칸': {law: len(json.load(open(os.path.join(DATA, 'jo_%s_목록.json' % law), encoding='utf-8')).get('삭제') or {}) for law in ('특허법', '상표법', '디자인보호법', '민사소송법')},
                        '제26조 날짜': want_date})
    else:   # regress · smoke — 바탕 앱 · 바탕 데이터 칸 없음
        N('C0', '재료', {'앱': NEW, '데이터': DATA,
                        '목록 삭제 칸': {law: len(json.load(open(os.path.join(DATA, 'jo_%s_목록.json' % law), encoding='utf-8')).get('삭제') or {}) for law in ('특허법', '상표법', '디자인보호법', '민사소송법')},
                        '제26조 날짜': want_date})
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        steps = [('C1', lambda: run_c1(br, src_new, src_base, newroots, baseroots)),
                 ('C2', lambda: None),
                 ('C3', lambda: run_c3(br, src_new, src_base, newroots)),
                 ('C4', lambda: run_c4(br, src_new, src_base, newroots))]
        for g, fn in steps:
            if ONLY and g not in ONLY:
                continue
            if not QJ.want(g, smoke=(g == 'C2')):   # smoke — T2461181 「유형? · 26」 → 삭제 조 팝업(10/2 83c230f 결함) 한 곳만
                continue
            print('── %s' % g, flush=True)
            t1 = time.time()
            _qs = QJ.stage(g)   # 단계 시간(§B-3) — launch.json stages
            _qs.__enter__()
            try:
                if g == 'C2':
                    QJ.launch('new', 2)
                    ok, out = run_c2(br, src_new, newroots, want_date, '새', SHOTS)
                    T('C2', 'T2461181 「유형? · 26」 진짜 누름 → 「특허법 제26조 (삭제)」 · 몸 「제26조 삭제 <%s>」 한 줄(.ln.wml) · 「이동 ↗」 없음 · 글꼴 = 보통 조 원문 줄 (폰 390 · PC)' % want_date,
                      all(ok.values()), {dn: {k: v for k, v in out[dn].items() if k != '팝업'} for dn in ('폰390', 'PC')} | {'몸': {dn: (out[dn]['팝업'] or {}).get('body') for dn in ('폰390', 'PC')},
                                                                                                                  '제목': {dn: (out[dn]['팝업'] or {}).get('title') for dn in ('폰390', 'PC')}, '그림': out.get('그림')})
                    if QJ.GATE:   # 관문만 — 헛잣대 Y2(바탕 앱 쪽 둘)
                        QJ.launch('base', 2)
                        okb, outb = run_c2(br, src_base, newroots, want_date, '바탕')
                        T('Y2', 'C2 헛잣대(바탕 앱 · 같은 데이터) = FAIL(물림)', not any(okb.values()), {dn: {'제목': (outb[dn]['팝업'] or {}).get('title'), '몸': (outb[dn]['팝업'] or {}).get('body')} for dn in ('폰390', 'PC')})
                else:
                    fn()
            except Exception as e:
                T(g, '돌다 멈춤', False, str(e).splitlines()[0][:300])
            _qs.__exit__(None, None, None)
            print('   (%s %.0f초)' % (g, time.time() - t1), flush=True)
        br.close()
        if 'webkit' in ENGS and (not ONLY or 'C2' in ONLY):
            wk = H.webkit_try(pw)
            if wk:
                print('── C2 WebKit(폰 390 · PC)', flush=True)
                try:
                    QJ.launch('new', 2)
                    ok, out = run_c2(wk, src_new, newroots, want_date, '새wk')
                    T('C2', 'WebKit — T2461181 「유형? · 26」 → 「특허법 제26조 (삭제)」 · 삭제 줄 한 줄 (폰 390 · PC)', all(ok.values()),
                      {dn: {'제목': (out[dn]['팝업'] or {}).get('title'), '몸': (out[dn]['팝업'] or {}).get('body'), '누름': out[dn]['누름'], 'JS 오류': out[dn]['JS 오류']} for dn in ('폰390', 'PC')})
                except Exception as e:
                    T('C2', 'WebKit 돌다 멈춤', False, str(e).splitlines()[0][:300])
                wk.close()
    nf = sum(1 for r in RES if r[2] is False)
    npass = sum(1 for r in RES if r[2] is True)
    with open(OUTF, 'w', encoding='utf-8', newline='\n') as f:
        for r in RES:
            d = r[3] if isinstance(r[3], str) else json.dumps(r[3], ensure_ascii=False, default=str)
            f.write('%s | %s · %s | %s\n' % ('INFO' if r[2] is None else ('PASS' if r[2] else 'FAIL'), r[0], r[1], d))
    print('\n══ PASS %d · FAIL %d (%.0f초) · 결과 → %s' % (npass, nf, time.time() - t0, OUTF))
    return nf


if __name__ == '__main__':
    rc = 1
    try:
        rc = 1 if main() else 0
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
    sys.exit(rc)
