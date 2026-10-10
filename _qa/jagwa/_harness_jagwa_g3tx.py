# -*- coding: utf-8 -*-
r"""_task_jg_g3tx_1010 §B 관문 [클라우드] — 자과 물리 근거 줄(트리거 · 공식·개념 · 주의점): Shift+Enter 로 나눈 문단이 보일 때도 줄이 나뉘게

  python _harness_jagwa_g3tx.py [--new <앱>] [--base <판 = 4ce28d0>] [--only T1,T2,T3,T4,T5]
                                [--spd <studyplandata>] [--notes <notes>] [--vendor <cdnjs 사본>] [--res <결과>] [--shots <그림>] [--png <캡처 넷 폴더>]

  NEW  = genie 작업트리 jagwa/index.html · BASE = 바탕 4ce28d0(헛잣대 — 문단이 한 줄로 붙음 → T1 · T3 FAIL 이어야)
  엔진 = Chromium · PC 1100×800(마우스) · 폰 390×844(hasTouch · 모바일 · DPR 2 · 톡 · 길게 누름 = CDP Input.dispatchTouchEvent) · WebKit 칸은 [로컬]
  데이터 = studyplandata 현행(--spd · 가짜 GitHub = JG.route_handler · PUT 은 메모리 · 밖으로 안 나감) · cdnjs = --vendor 사본(클라우드는 cdn 막힘)
  문항 = 근거 · 이은 개념 · 연결 칩이 없는 물리 문항 둘(쪽 안에서 처음부터 고름 — 개인 근거 글이 화면 · 캡처에 안 섞이게)
  문항 열기 = openView(번호)(목록 줄 누름과 같은 함수) · 근거 줄 펴기 = ▾(#g3Fold) 진짜 누름 · 칸 고르기 = g3Sel(앱 함수 · 칸 토글 창 대신) · 글 = 진짜 타자 · Shift+Enter · Enter
  ⚠ 개인 문항 · 해설 · 근거 글을 출력 · 캡처에 옮기지 않는다(D11) — 출력 = 시험 글 · 칸 · 수 · 자리만 · 캡처 = 근거 줄 상자만 잘라(문항 지문 · 제목 밖)
  관문:
    T1 세 칸 각각 「첫 문단」 Shift+Enter 「둘째 문단」 → Enter 저장 → 저장 글 = 「첫 문단\n둘째 문단」 · 보이는 근거 줄 글 상자 줄 수 ≥ 2 · 둘째 문단 top > 첫 문단 top(Range) ·
       단추(! · 쓰인 수 · 댓 · ✕) = 첫 줄 자리 · 서랍 작은 창(g3PopToggle) · 찾기 목록(다른 문항 트리거 칸에 「첫」 → 이 글 · .g3s .bt1) 같은 글도 두 줄
    T2 한 줄 글(세 칸 글 셋 + 공식 블록 칩 하나 · 다른 문항) = 바탕과 항목 높이 · 글 상자 · 단추(! · 쓰인 수 · 댓 · ✕) 자리 같음(±1px)
    T3 고치기 칸 다시 열기(항목 길게 누름 = 진짜 누름) = textarea 글 = 저장 글(줄바꿈 그대로 · 바탕도 같음) → Shift+Enter 「셋째 문단」 Enter → 저장 글 세 문단 · 보이는 줄 셋
    T4 원격 PUT 막음 — T1 뒤 동기화 칩(#recChip) 진짜 누름 → PUT 은 가짜 원격(JG.route_handler · 메모리)만 받음 · 그 기록에 시험 글 · studyplandata 사본 파일 무변
    T5 캡처 PNG 넷 — 폰 390 · PC 1100 × 바탕(붙어 보임) · 새 판(나뉘어 보임) · 근거 줄 상자 가운데로 굴려 그 상자만 잘라 → --png(인도 = _qa/cloud_batch/shots_g3tx/ · 없으면 --shots)
  모드 — gate = 바탕 띄움(헛잣대) · regress · smoke = 새 판만(바탕 풀기 · 띄우기 0 · T2 「= 바탕」 = 기준 스냅샷 · smoke = T1 폰)
  결과 = 화면 PASS/FAIL/INFO 줄 · --res(기본 = 임시 폴더 · _qa 에 결과를 쓰지 않는다)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402,F401 — --mode · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음
import _qa_jagwa_common as JG   # noqa: E402
import hashlib, json, os, sys, tempfile, time, traceback   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEWF = ARG('--new', _roots.genie('jagwa', 'index.html'))
BASE = ARG('--base', '4ce28d0')
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
TMPD = os.path.join(tempfile.gettempdir(), 'h_jagwa_g3tx')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_jagwa_g3tx_result.txt'))
SHOTS = ARG('--shots', os.path.join(TMPD, 'shots'))
PNG = ARG('--png')   # 인도 캡처 넷 폴더(주면 거기 · 안 주면 SHOTS) — 사슬 regress 가 저장소를 더럽히지 않게 기본은 _qa 밖
SPD = ARG('--spd', _roots.spd())
NOTES = ARG('--notes', os.path.join(os.path.dirname(_roots.spd()), 'notes'))
VENDOR = ARG('--vendor', os.path.join(TMPD, 'vendor'))
JG.conf(VENDOR_PP=VENDOR, SPD_PP=SPD, NOTES=NOTES, SHOTS=SHOTS)
GATE = QC.GATE
if GATE:
    QC.sub('git:show-app')
SRC = {'NEW': JG.app_src(NEWF)}
if GATE:
    SRC['BASE'] = JG.app_src(BASE)
VERS = tuple(SRC)
DEVS = [('폰', (390, 844), True), ('PC', (1100, 800), False)]
P1, P2 = '첫 문단', '둘째 문단'
P3 = '셋째 문단'
ONE = '한 줄 시험 글'
FIELDS = [('t', '트리거'), ('c', '공식·개념'), ('w', '주의점')]
RES = []
STEP = {}
T0 = time.time()


def want(c):
    return (not ONLY or c in ONLY) and (not QC.SMOKE or c == 'T1')


def _s(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


def R(g, name, new, base=None, d='', yard=True):
    RES.append(dict(g=g, name=name, new=new, base=base, yard=yard, d=d))
    tag = 'INFO' if new is None else ('PASS' if new else 'FAIL')
    yb = '' if base is None else (' · 바탕 ' + (('PASS(바탕도 같음)' if yard else 'PASS') if base else 'FAIL'))
    print('%s | %s · %s%s | %s' % (tag, g, name, yb, _s(d)[:900]), flush=True)


def md5lf(s):
    return hashlib.md5(s.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def md5f(f):
    try:
        return hashlib.md5(open(f, 'rb').read()).hexdigest()
    except Exception:
        return None


# 근거 · 이은 개념 · 연결 칩이 없는 물리 문항 — 쪽 안에서 처음부터(열어 봐서 근거 줄이 빈 것만)
PICK_JS = r"""(skip)=>{const out=[];for(const r of DATA){const no=r[F.NO],u=GGU(r);if(skip.indexOf(no)>=0)continue;
  if((ggOf(u)||[]).length)continue;if(typeof ggRefOf==='function'&&ggRefOf(u).length)continue;out.push([no,u]);if(out.length>=12)break}return out}"""
EMPTY_JS = r"""(()=>{const b=document.querySelector('#view .g3box');return {box:!!b,items:b?b.querySelectorAll('.g3it').length:-1,ref:b?b.querySelectorAll('.refchips *').length:-1}})()"""
# 항목 잼 — 항목 왼끝 · 위 기준 자리(글 상자 · ! · 쓰인 수 · 댓 · ✕) · 글 상자 줄 수 · 문단 첫 글자 top(Range)
MEAS_JS = r"""()=>[...document.querySelectorAll('#view .g3list .g3it.g3r[data-g3k]')].map(it=>{const r=it.getBoundingClientRect(),tx=it.querySelector('.g3tx');
  const rel=e=>{if(!e||!__H.vis(e))return null;const b=e.getBoundingClientRect();return [+(b.left-r.left).toFixed(1),+(b.top-r.top).toFixed(1),+b.width.toFixed(1),+b.height.toFixed(1)]};
  const tops={};if(tx){const w=document.createTreeWalker(tx,NodeFilter.SHOW_TEXT);let n;while((n=w.nextNode())){for(const k of ['첫 문단','둘째 문단','셋째 문단','한 줄 시험 글']){const i=n.data.indexOf(k);
    if(i>=0&&!(k in tops)){const g=document.createRange();g.setStart(n,i);g.setEnd(n,i+1);tops[k]=+g.getBoundingClientRect().top.toFixed(1)}}}}
  const t=tx?tx.getBoundingClientRect():null,lh=tx?parseFloat(getComputedStyle(tx).lineHeight):0;
  return {f:it.dataset.f,
    it:[+r.width.toFixed(1),+r.height.toFixed(1)],tx:rel(tx),lines:(t&&lh)?Math.round(t.height/lh):null,tops,
    bang:rel(it.querySelector('.g3bg')),use:rel(it.querySelector('.gguse')),cm:rel(it.querySelector('.g3cm')),del:rel(it.querySelector('.g3del')),
    txt:tx?tx.textContent:null}})"""


def open_q(p, no, touch):
    """문항 열기 · 근거 줄 펴기(▾ 진짜 누름)"""
    p.ev("(no)=>openView(no)", no)
    p.wait(2200)
    if not p.ev("typeof __H!=='undefined'"):
        p.ev(JG.TOOLS)
    if p.ev("document.getElementById('view').classList.contains('g3off')"):
        a = p.ev("(()=>__H.hit(document.getElementById('g3Fold')))()")
        p.press(a, wait=700)
    return not p.ev("document.getElementById('view').classList.contains('g3off')")


def type_item(p, uid, f, parts):
    """칸 f 고르고(g3Sel) 적는 칸 진짜 누름 → 문단마다 진짜 타자 · 문단 사이 Shift+Enter → Enter 저장(공식 칸은 블록 찾기 목록이 떠 있으면 Esc 로 닫고)"""
    p.ev("([u,f])=>g3Sel(u,f)", [uid, f])
    p.wait(300)
    a = p.ev("(()=>__H.hit(document.querySelector('#view .g3box .g3f .ggrows .txt')))()")
    if not p.press(a, wait=200):
        p.ev("(()=>document.querySelector('#view .g3box .g3f .ggrows .txt').focus())()")
    for i, t in enumerate(parts):
        if i:
            p.pg.keyboard.down('Shift')
            p.pg.keyboard.press('Enter')
            p.pg.keyboard.up('Shift')
        p.pg.keyboard.type(t, delay=12)
    p.wait(250)
    sug = p.ev("(()=>{const s=document.querySelector('#view .g3box .g3sug');return s?{on:!s.classList.contains('hide'),n:document.querySelectorAll('#view .g3box .g3sug .g3s').length}:null})()")
    if f == 'c' and sug and sug['on'] and sug['n']:
        p.pg.keyboard.press('Escape')
        p.wait(150)
    p.pg.keyboard.press('Enter')
    p.wait(900)
    return sug


def saved(p, uid):
    return p.ev("(u)=>ggOf(u).filter(Boolean).map(g=>({f:g.f||'t',t:String(g.t||''),parts:!!g.parts,ref:g.ref||null}))", uid)


def capture(p, name):
    """근거 줄 상자를 가운데로 굴려 그 상자만(± 8px · 화면 안) 잘라 찍음"""
    r = p.ev("""(()=>{const b=document.querySelector('#view .g3box');if(!b)return null;b.scrollIntoView({block:'center'});const x=b.getBoundingClientRect();
      return {x:x.left,y:x.top,w:x.width,h:x.height,W:innerWidth,H:innerHeight}})()""")
    if not r:
        return None
    p.wait(300)
    x0, y0 = max(0, r['x'] - 8), max(0, r['y'] - 8)
    x1, y1 = min(r['W'], r['x'] + r['w'] + 8), min(r['H'], r['y'] + r['h'] + 2)   # 아래는 2px — 그 밑은 문항 그림 칸
    d = PNG or SHOTS
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, name + '.png')
    p.pg.screenshot(path=f, clip={'x': x0, 'y': y0, 'width': x1 - x0, 'height': y1 - y0}, animations='disabled')
    return {'file': f, 'clip': [round(x0), round(y0), round(x1 - x0), round(y1 - y0)]}


POP_JS = r"""(no)=>{const x=document.querySelector('#ndList .ndrow[data-no="'+no+'"] .ndox');if(!x)return null;try{x.scrollIntoView({block:'center'})}catch(e){}g3PopToggle(no,x);return true}"""
POPM_JS = r"""()=>{const P=document.getElementById('g3Pop');if(!P||!__H.vis(P))return null;return [...P.querySelectorAll('.g3pf .it')].filter(e=>/첫 문단/.test(e.textContent)).map(e=>{
  const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT);let n,a=null,b=null;while((n=w.nextNode())){const i=n.data.indexOf('첫 문단'),j=n.data.indexOf('둘째 문단');
    if(i>=0&&a==null){const g=document.createRange();g.setStart(n,i);g.setEnd(n,i+1);a=g.getBoundingClientRect().top}if(j>=0&&b==null){const g=document.createRange();g.setStart(n,j);g.setEnd(n,j+1);b=g.getBoundingClientRect().top}}
  return {f:e.closest('.g3pf').dataset.f,t1:a,t2:b}})}"""
SUGM_JS = r"""()=>[...document.querySelectorAll('#view .g3box .g3sug .g3s .bt1')].filter(e=>/첫 문단/.test(e.textContent)).map(e=>{const n=e.firstChild;if(!n||n.nodeType!==3)return null;
  const i=n.data.indexOf('첫 문단'),j=n.data.indexOf('둘째 문단');if(i<0||j<0)return null;const g=document.createRange();g.setStart(n,i);g.setEnd(n,i+1);const a=g.getBoundingClientRect().top;
  g.setStart(n,j);g.setEnd(n,j+1);return {t1:a,t2:g.getBoundingClientRect().top}})"""


def run_dev(br, ver, dname, size, touch, picks):
    """한 기기 · 한 판 — T1(세 칸 두 문단) · T5(캡처) · T3(고치기 다시 열기) · T2(한 줄 · 다른 문항) · T4(PUT)"""
    out = {'ver': ver, 'dev': dname}
    spd_rec = os.path.join(SPD, 'phys', '기록.json')
    md0 = md5f(spd_rec)
    QC.launch('base' if ver == 'BASE' else 'new')
    rem = JG.Remote()
    p = JG.Pg_PP(br, 'chromium', 'g3tx-' + ver, SRC[ver], 'phys', size, touch=touch, remote=rem)
    try:
        # 문항 둘 — 열어서 근거 줄이 빈 것만
        use = []
        for no, uid in picks:
            if not open_q(p, no, touch):
                continue
            e = p.ev(EMPTY_JS)
            if e['box'] and e['items'] == 0 and e['ref'] == 0:
                use.append((no, uid))
            if len(use) >= 2:
                break
        out['문항'] = [u for _, u in use]
        (no1, u1), (no2, u2) = use[0], use[1]
        # ── T1 ──
        open_q(p, no1, touch)
        sug = {}
        for f, _ in FIELDS:
            sug[f] = type_item(p, u1, f, [P1, P2])
        sv = saved(p, u1)
        m = p.ev(MEAS_JS)
        pop = None
        if p.ev(POP_JS, no1):
            p.wait(900)
            pop = p.ev(POPM_JS)
            p.ev("(()=>{const P=document.getElementById('g3Pop');if(P&&typeof g3PopClose==='function')g3PopClose();else if(P)P.remove()})()")
            p.wait(300)
        out['T1'] = {'저장': sv, '잼': m, '찾기 목록(Esc 전 · 공식 칸)': sug.get('c'), '서랍 작은 창': pop}
        # ── T4 동기화 칩 진짜 누름 → 저장 PUT = 가짜 원격(메모리)만 ──
        n0 = len(rem.puts)
        a = p.ev("(()=>__H.hit(document.getElementById('recChip')))()")
        pressed = p.press(a, wait=300)
        if not pressed:
            p.ev("(()=>syncRecords(true))()")
        for _ in range(40):
            if len(rem.puts) > n0 and not p.ev("typeof recBusy!=='undefined'&&recBusy"):
                break
            p.wait(250)
        body = rem.files.get('zzikkaplan/studyplandata:phys/기록.json') or b''
        out['T4'] = {'동기화 칩 누름': pressed, '누른 뒤 PUT(가짜 원격 · 메모리)': [(k.split(':', 1)[1], n) for k, n, _ in rem.puts[n0:]],
                     'PUT 기록에 시험 글(두 문단)': json.dumps(P1 + '\n' + P2, ensure_ascii=False)[1:-1].encode('utf-8') in body}
        # ── T5 캡처 ──
        open_q(p, no1, touch)
        out['T5'] = capture(p, 'g3tx_%s_%s' % ({'폰': 'ph390', 'PC': 'pc1100'}[dname], 'new' if ver == 'NEW' else 'base'))
        # ── T3 고치기 다시 열기 ──
        p.ev("(()=>{const it=document.querySelector('#view .g3list .g3it.g3r[data-f=\"t\"]');if(it)it.scrollIntoView({block:'center'})})()")
        p.wait(300)
        at = p.ev("""(()=>{const it=document.querySelector('#view .g3list .g3it.g3r[data-f="t"]');if(!it)return null;const tx=it.querySelector('.g3tx').getBoundingClientRect();
          return {x:tx.left+Math.min(30,tx.width/3),y:tx.top+9}})()""")
        ed = None
        if at:
            p.long_press(at['x'], at['y'], ms=900, wait=500)
            ed = p.ev("(()=>{const t=document.querySelector('#view .g3list .g3ed textarea');return t?{val:t.value,act:document.activeElement===t,h:Math.round(t.getBoundingClientRect().height)}:null})()")
            if ed:
                p.pg.keyboard.press('End')
                p.pg.keyboard.down('Control')
                p.pg.keyboard.press('End')
                p.pg.keyboard.up('Control')
                p.pg.keyboard.down('Shift')
                p.pg.keyboard.press('Enter')
                p.pg.keyboard.up('Shift')
                p.pg.keyboard.type(P3, delay=12)
                p.pg.keyboard.press('Enter')
                p.wait(900)
        sv3 = saved(p, u1)
        m3 = [x for x in p.ev(MEAS_JS) if x['f'] == 't']
        out['T3'] = {'다시 연 칸': ed, '저장(트리거)': [x for x in sv3 if x['f'] == 't'], '잼(트리거)': m3}
        # ── T2 한 줄 · 다른 문항 ── (먼저 T1 찾기 목록 — 다른 문항(no1)이 트리거 · 주의점 칸에 쓴 두 문단 글이 이 문항 트리거 칸 찾기 목록에)
        open_q(p, no2, touch)
        p.ev("([u])=>g3Sel(u,'t')", [u2])
        p.wait(300)
        a = p.ev("(()=>__H.hit(document.querySelector('#view .g3box .g3f .ggrows .txt')))()")
        if not p.press(a, wait=200):
            p.ev("(()=>document.querySelector('#view .g3box .g3f .ggrows .txt').focus())()")
        p.pg.keyboard.type('첫', delay=20)
        p.wait(600)
        out['T1']['찾기 목록 두 문단'] = p.ev(SUGM_JS)
        p.pg.keyboard.press('Escape')
        p.ev("(()=>{const t=document.querySelector('#view .g3box .g3f .ggrows .txt');if(t){t.value='';t.blur()}})()")
        p.wait(300)
        open_q(p, no2, touch)
        for f, _ in FIELDS:
            type_item(p, u2, f, [ONE])
        p.ev("""(u)=>{const b=G3.blocks()[0];if(b)return G3.push(u,'c',{t:b.text,ref:b.key})}""", u2)
        p.wait(900)
        open_q(p, no2, touch)
        p.ev("(()=>{const b=document.querySelector('#view .g3box');if(b)b.scrollIntoView({block:'center'})})()")
        p.wait(300)
        out['T2'] = {'저장': [{'f': x['f'], '한 줄': x['t'] == ONE, 'ref': bool(x['ref'])} for x in saved(p, u2)], '잼': p.ev(MEAS_JS)}
        # ── T4 ──
        out['T4']['모든 PUT(가짜 원격)'] = len(rem.puts)
        out['T4']['사본 기록 파일 무변'] = md5f(spd_rec) == md0
        out['오류'] = (p.errs or []) + (p.ev('window.__err||[]') or [])
    finally:
        p.close()
    return out


def lines_ok(m, n):
    """보이는 근거 줄 — 문단 n 개가 다른 줄(글 상자 줄 수 ≥ n · 문단 첫 글자 top 차례로 커짐)"""
    ks = [P1, P2, P3][:n]
    tp = [m['tops'].get(k) for k in ks]
    return m['lines'] is not None and m['lines'] >= n and all(t is not None for t in tp) and all(tp[i + 1] > tp[i] + 2 for i in range(n - 1))


def main():
    os.makedirs(TMPD, exist_ok=True)
    R('T0', '판 · 자리', None, None, {'NEW': NEWF, 'md5(LF)': {k: md5lf(v) for k, v in SRC.items()}, 'BASE': BASE if GATE else '(regress · smoke = 안 띄움)',
                                     'SPD': SPD, '캡처': PNG or SHOTS})
    res = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pq = JG.Pg_PP(br, 'chromium', 'g3tx-pick', SRC['NEW'], 'phys', (1100, 800), touch=False, remote=JG.Remote())
        picks = pq.ev(PICK_JS, [])
        pq.close()
        for dname, size, touch in (DEVS[:1] if QC.SMOKE else DEVS):
            t1 = time.time()
            for v in VERS:
                try:
                    res[(v, dname)] = run_dev(br, v, dname, size, touch, picks)
                except Exception as e:
                    res[(v, dname)] = {'하네스 오류': str(e)[:300], 'tb': traceback.format_exc()[-600:]}
            STEP[dname] = round((time.time() - t1) / 60, 1)
        br.close()

    def t1(v, dn):
        o = res.get((v, dn)) or {}
        T = o.get('T1')
        if not T:
            return False, o
        sv = [x for x in T['저장'] if x['t'] == P1 + '\n' + P2]
        ms = [x for x in T['잼'] if x['txt'] == P1 + '\n' + P2]
        per = {x['f']: {'줄 수': x['lines'], '둘째 top − 첫 top': round((x['tops'].get(P2) or 0) - (x['tops'].get(P1) or 0), 1),
                        '단추 = 첫 줄': all(b is not None and b[1] < (x['tx'][1] + 14) for b in (x['bang'], x['cm'], x['del']))} for x in ms}
        pop = T['서랍 작은 창'] or []
        sg = [x for x in (T['찾기 목록 두 문단'] or []) if x]
        d = {'문항': o.get('문항'), '저장(세 칸 = 두 문단 \\n)': sorted(x['f'] for x in sv), '근거 줄': per,
             '서랍 작은 창(칸 · 둘째 top − 첫 top)': [(x['f'], round((x['t2'] or 0) - (x['t1'] or 0), 1)) for x in pop],
             '찾기 목록(둘째 top − 첫 top)': [round(x['t2'] - x['t1'], 1) for x in sg], '공식 칸 블록 목록(Esc 전)': T['찾기 목록(Esc 전 · 공식 칸)'], '오류': o.get('오류', [])[:3]}
        ok = (sorted(x['f'] for x in sv) == ['c', 't', 'w'] and len(ms) == 3 and all(lines_ok(x, 2) for x in ms) and all(v2['단추 = 첫 줄'] for v2 in per.values())
              and len(pop) == 3 and all(x['t2'] and x['t1'] and x['t2'] > x['t1'] + 2 for x in pop)
              and len(sg) >= 1 and all(x['t2'] > x['t1'] + 2 for x in sg) and not o.get('오류'))
        return ok, d

    def t2_rows(v, dn):
        o = res.get((v, dn)) or {}
        T = o.get('T2') or {}
        return [{k: x[k] for k in ('f', 'it', 'tx', 'lines', 'bang', 'use', 'cm', 'del')} for x in (T.get('잼') or [])], T, [x.get('txt') for x in (T.get('잼') or [])]

    def close(a, b, tol=1.0):
        if a is None or b is None:
            return a is None and b is None
        if isinstance(a, list):
            return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return abs(a - b) <= tol
        return a == b

    def t3(v, dn):
        o = res.get((v, dn)) or {}
        T = o.get('T3')
        if not T:
            return (False, o), (False, o)
        ed = T['다시 연 칸'] or {}
        a_ok = bool(ed) and ed.get('val') == P1 + '\n' + P2
        sv = T['저장(트리거)']
        m = T['잼(트리거)']
        b_ok = len(sv) == 1 and sv[0]['t'] == P1 + '\n' + P2 + '\n' + P3 and len(m) == 1 and lines_ok(m[0], 3)
        return (a_ok, {'다시 연 칸 글 = 저장 글(두 문단)': a_ok, '칸 높이': ed.get('h'), '초점': ed.get('act')}), \
               (b_ok, {'저장 = 세 문단': len(sv) == 1 and sv[0]['t'].count('\n') == 2, '보이는 줄 수': m[0]['lines'] if m else None,
                       '문단 top': [m[0]['tops'].get(k) for k in (P1, P2, P3)] if m else None})

    for dname, _, _ in (DEVS[:1] if QC.SMOKE else DEVS):
        if want('T1'):
            a = t1('NEW', dname)
            b = t1('BASE', dname) if GATE else (None, None)
            R('T1', '%s 세 칸 「첫 문단」 Shift+Enter 「둘째 문단」 저장 → 근거 줄 두 줄(줄 수 ≥ 2 · 둘째 top > 첫 top · 단추 첫 줄) · 서랍 작은 창 · 찾기 목록도 두 줄' % dname,
              a[0], b[0], {'NEW': a[1], 'BASE': b[1]})
        if want('T2'):
            ra, Ta, txa = t2_rows('NEW', dname)
            if GATE:
                rb = t2_rows('BASE', dname)[0]
                QC.base('T2@' + dname, ra)   # 다음 regress 의 기준(스냅샷)
            else:   # regress — 바탕 안 띄움 · 기준 스냅샷(앞 인도판에서 잰 자리)
                rb = QC.base('T2@' + dname, ra)
            diff = [(x['f'], k, x[k], y[k]) for x, y in zip(ra, rb) for k in ('it', 'tx', 'lines', 'bang', 'use', 'cm', 'del') if not close(x[k], y[k])]
            one = [x for x, t in zip(ra, txa) if t == ONE and x['lines'] == 1]   # 공식 블록 칩은 첫 줄이 길면 제 폭에서 감김(바탕도 같음) — 한 줄 잣대는 시험 글 셋만
            ok = len(ra) == 4 and len(rb) == 4 and not diff and len(one) == 3 and not (res.get(('NEW', dname)) or {}).get('오류')
            R('T2', '%s 한 줄 글(세 칸 + 공식 블록 칩) = 바탕과 항목 높이 · 글 상자 · 단추 자리 같음(±1px)' % dname, ok, None,
              {'항목': len(ra), '한 줄': len(one), '어긋남': diff[:6], '새 판 자리(칸 · 항목 높이 · 글 상자 · ✕)': [(x['f'], x['it'][1], x['tx'], x['del']) for x in ra],
               '저장': Ta.get('저장')}, yard=False)
        if want('T3'):
            (a1, d1), (a2, d2) = t3('NEW', dname)
            if GATE:
                (b1, e1), (b2, e2) = t3('BASE', dname)
            else:
                (b1, e1), (b2, e2) = (None, None), (None, None)
            R('T3', '%s 고치기 칸 다시 열기(길게 누름) = 줄바꿈 그대로' % dname, a1, b1, {'NEW': d1, 'BASE': e1}, yard=False)   # 바탕도 같아야(고치기 칸은 ggFlat 그대로)
            R('T3', '%s 고치기 칸에서 Shift+Enter 「셋째 문단」 → 저장 세 문단 · 보이는 줄 셋' % dname, a2, b2, {'NEW': d2, 'BASE': e2})
        if want('T4'):
            ok, d = True, {}
            for v in VERS:
                T = (res.get((v, dname)) or {}).get('T4') or {}
                good = (bool(T.get('누른 뒤 PUT(가짜 원격 · 메모리)')) and T.get('PUT 기록에 시험 글(두 문단)') is True
                        and T.get('사본 기록 파일 무변') is True)   # PUT 은 route(JG.route_handler)가 받아 메모리에 — 밖(GitHub)으로 안 나감
                ok = ok and good
                d[v] = T
            R('T4', '%s 원격 PUT 막음 — 동기화 칩 진짜 누름 → PUT = 가짜 원격(메모리)만 · 그 기록에 시험 글 · studyplandata 사본 파일 무변' % dname, ok, None, d, yard=False)
        if want('T5') and GATE:
            fs = {v: (res.get((v, dname)) or {}).get('T5') for v in VERS}
            ok = all(x and os.path.isfile(x['file']) and os.path.getsize(x['file']) > 2000 for x in fs.values())
            R('T5', '%s 캡처 — 바탕(붙어 보임) · 새 판(나뉘어 보임) · 근거 줄 상자만' % dname, ok, None,
              {v: (x and {'파일': os.path.relpath(x['file'], _roots.genie()) if PNG else os.path.basename(x['file']), '잘라 낸 자리': x['clip']}) for v, x in fs.items()}, yard=False)
    nf = [r for r in RES if r['new'] is False]
    yard = [r for r in RES if r['yard'] and r['base'] is not None and r['new'] is not None]
    R('합계', '합계', None, None, {'PASS': sum(1 for r in RES if r['new'] is True), 'FAIL': len(nf), 'FAIL 칸': [r['g'] + ' ' + r['name'][:24] for r in nf],
                                  '헛잣대(바탕 FAIL)': '%d/%d' % (sum(1 for r in yard if r['base'] is False), len(yard)), '단계(분)': STEP, '전체(분)': round((time.time() - T0) / 60, 1)})
    try:
        with open(OUTF, 'w', encoding='utf-8') as f:
            for r in RES:
                f.write(json.dumps(r, ensure_ascii=False, default=str) + '\n')
    except Exception:
        pass
    sys.exit(1 if nf else 0)


if __name__ == '__main__':
    main()
