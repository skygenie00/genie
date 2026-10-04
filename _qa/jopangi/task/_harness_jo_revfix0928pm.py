# -*- coding: utf-8 -*-
r"""_task_jo_revfix0928pm §B 관문 하네스 — 머리 세모 줄 나뉨 · 판 이름 칩 H7/H8 · 8판 새 카드 이동 · P7-1153 · 좁은 서랍

  python _harness_jo_revfix0928pm.py --new <앱> [--data <jo/data>] [--exam <gichul/pdf>] [--res <결과>] [--eng chromium,webkit] [--only h1,h2,a2,a3,a4,a5]

  NEW  = 이 판 앱 + 이 판 데이터 · BASE = genie HEAD(바로 앞 인도판 = jo_gaek_uid_add3 e36829b) 앱 + 데이터 — 칸마다 헛잣대(바탕에서 FAIL)
  머리 줄 나뉨 잣대 = hdrfold 앞 판 d6cf661 의 앱(같은 새 데이터 · 레일 수가 같게) — 폭 320~1920 · 2px · 머리 높이 · 요소마다 줄 번호 · 배지 자리 · 본문 위 끝
  글꼴 둘 = 기본 + Gulim(지시서는 WenQuanYi Zen Hei — 이 PC 에 없다 · 글자 폭이 다른 둘째 글꼴로 대신 · 보고에 적음)
  누름 = 진짜 포인터(page.mouse · 손가락 = Chromium CDP 터치 r22 · WebKit touchscreen.tap) · 보임 = display ≠ none · 높이 > 0
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402 — _task_qa_slim(10/4) A-1·A-2·A-3: --mode gate|regress|smoke(인자 없으면 gate = 이 판 앞과 같음) · regress = NEW 만 띄움(바탕 HEAD · 머리 바탕 d6cf661 안 풀고 안 띄움) · 폭 표본 · 앱 표지 기다림
import io, json, os, re, sys, time, shutil, subprocess, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
JOP = os.path.dirname(HERE)


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


_NEW = ARG('--new')
_DATA = ARG('--data', _roots.genie(r'jo\data'))
_EXAM = ARG('--exam', _roots.genie(r'gichul\pdf'))
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_revfix0928pm_result.txt'))
STEP = int(ARG('--step', '2'))
_BASE = ARG('--base', 'HEAD')   # 헛잣대 = 바로 앞 인도판(9/28 20:23 ⚙ 자동 푸시 4e83e79 가 중간판을 HEAD 로 올려 --base e36829b 로 박을 수 있게)
sys.argv = [sys.argv[0], '--new', _NEW, '--data', _DATA, '--base', _BASE, '--exam', _EXAM]
sys.path.insert(0, HERE)
sys.path.insert(0, JOP)
import _harness_jo_gaek_mbsame as M   # noqa: E402
from playwright.sync_api import sync_playwright   # noqa: E402
M.TESTS = M.TESTS + '\n' + io.open(os.path.join(HERE, '_harness_jo_uidmbs2_tests.js'), encoding='utf-8').read() \
    + '\n' + io.open(os.path.join(HERE, '_harness_jo_revfix0928pm_tests.js'), encoding='utf-8').read()
M.WORK = M.WORK + '_rp'
RES = []
HDR_REV = 'd6cf661'
FONTS = [('기본', ''), ('Gulim', 'Gulim')]


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


class Pg(M.Pg):
    def __init__(self, br, eng, tag, src, data, exam, W=1553, H=900, **k):
        self.eng = eng
        ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, has_touch=True)
        super().__init__(br, tag + '_' + eng, src, data, exam, ctx=ctx, **k)

    def tap(self, at, wait=500):
        if not at or not at.get('on'):
            return False
        if self.eng == 'webkit':
            self.pg.touchscreen.tap(at['cx'], at['cy'])
            self.pg.wait_for_timeout(wait)
            return True
        return super().tap(at, wait)

    def press(self, at, how, wait=500):
        return self.tap(at, wait) if how == 'touch' else self.click(at, wait)


def _settle(q, wait, js=None, what='', arg=None, ms=None):
    """regress 의 기다림(_task_qa_slim A-2) — 앱 표지(js)가 서면 바로(못 서면 ms · 기본 max(2×옛 대기, 3초) 뒤 그대로 잰다) + 브라우저 두 프레임(ResizeObserver · rAF 로 미룬 자리 맞춤이 끝나는 한 박자 —
    시간이 아니라 프레임 · 앱 표지 아님 · 하네스 쪽) · 표지(js)가 없으면 QJ.sleep(옛 대기, 까닭, page) = 고정 대기를 남기고 까닭을 적는다(page 를 넘겨 그동안 route · 요청이 돈다) ·
    환경변수 QA_SLIM_FIXED=W3,W7 (또는 all) 이면 그 자리는 옛 고정 대기 그대로(흔들림 때 그 자리만 되돌리는 길 · what 첫 낱말 = Wn) · gate 는 안 부른다(호출 자리가 `원본 if QJ.GATE else _settle(…)` 꼴)"""
    fixed = [x for x in os.environ.get('QA_SLIM_FIXED', '').split(',') if x]
    if not js or 'all' in fixed or (what or '').split(' ')[0] in fixed:
        QJ.sleep(wait, what or '고정 대기 남김 — 앱 표지 없음', q.pg)
        return
    QJ.until(q.pg, js, ms or max(2 * wait, 3000), what, arg)
    try:
        q.pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
    except Exception:
        pass


def _press(q, at, how, wait, js=None, what='', arg=None, ms=None):
    """regress — q.press 와 같은 누름인데 뒤 기다림을 표지로(_settle)"""
    ok = q.tap(at, 0) if how == 'touch' else q.click(at, 0)
    if ok:
        _settle(q, wait, js, what, arg, ms)
    return ok


def _clk(q, at, wait, js=None, what='', arg=None, ms=None):
    """regress — q.click 과 같은 누름인데 뒤 기다림을 표지로(_settle)"""
    ok = q.click(at, 0)
    if ok:
        _settle(q, wait, js, what, arg, ms)
    return ok


def home(p, gk='g'):
    p.ev("l=>__HM.home(l)", '특허법')
    if p.ev("()=>__UZ.has('UZGK')"):
        p.ev("v=>__UZ.gk(v)", gk)


def go_key(p, k):
    home(p)
    gk = p.ev("k=>{try{return uzIsGi(k)?'g':'x'}catch(e){return 'g'}}", k)
    home(p, gk)
    sel = p.ev("k=>__UZ.selOfKey(k)", k)
    if not sel:
        return None
    p.ev("s=>__HM.go(s)", sel)
    pg = p.ev("k=>{const P=(OXPOOL||{})[k];if(!P)return null;const d=P.dom;const c=document.getElementById(d);return c?null:(OXDOMPG||{})[d]}", k)
    if pg:
        p.ev("n=>__HM.page(n)", pg)
    (p.pg.wait_for_timeout(300) if QJ.GATE else _settle(p, 300, "k=>{const P=(OXPOOL||{})[k];return !!P&&!!document.getElementById(P.dom)}", 'W1 그 카드 칸(OXPOOL[k].dom)이 섰다', k))
    return sel


# ══════════ 머리 ══════════
def heads(p, font):
    p.ev("f=>__RP.font(f)", font)
    out = {}
    for w in range(320, 1921, STEP):
        p.pg.set_viewport_size({'width': w, 'height': 900})
        p.pg.wait_for_timeout(15)
        out[w] = p.ev("()=>__RP.head()")
    p.pg.set_viewport_size({'width': 1553, 'height': 900})
    p.ev("()=>__RP.font('')")
    return out


def diff_heads(a, b):
    bad = []
    for w in a:
        x, y = a[w], b.get(w)
        if not x or not y or x['h'] != y['h'] or x['line'] != y['line'] or x['hb'] != y['hb'] or x['body'] != y['body']:
            bad.append(w)
    rng = []
    for w in bad:
        if rng and w - rng[-1][1] <= STEP:
            rng[-1][1] = w
        else:
            rng.append([w, w])
    return bad, rng


def heads_at(p, font, ws):
    """regress(A-3) — 폭 표본 ws 만 잰다(heads 와 같은 잼 · 폭 목록만 다르다)"""
    p.ev("f=>__RP.font(f)", font)
    out = {}
    for w in ws:
        p.pg.set_viewport_size({'width': w, 'height': 900})
        QJ.sleep(15, 'W2 폭을 바꾼 뒤 hdrFit(ResizeObserver) 한 박자 — 앱 표지 없음(옛 15ms 그대로 · 폭 표본이라 수십 번뿐)', p.pg)
        out[w] = p.ev("()=>__RP.head()")
    p.pg.set_viewport_size({'width': 1553, 'height': 900})
    p.ev("()=>__RP.font('')")
    return out


def _tail(detail, note, lim=420):
    """값 끝에 「(표본 n/N)」 — 출력은 lim 자에서 잘리니 앞을 줄여 꼬리를 남긴다(QJ 표본 규칙)"""
    s = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    return s[:max(0, lim - len(note))] + note


def h1_regress(p, eng):
    """regress — 머리 줄 나뉨 = 처리안 표본 + 기준: 폭 320~1920 을 QJ.widths(앱 꺾임 ±1 · 지난 FAIL 폭) + 40px 격자 + 샘플 폭만 잰다 ·
    d6cf661 앱(세모 없는 바탕)과 HEAD 는 안 풀고 안 띄운다 → d6cf661 잣대는 기준 스냅샷(이 판 앞 인도판이 d6cf661 과 맞대 통과한 값)과 맞댄다 ·
    헛잣대(HEAD 어긋남 있음)는 관문만"""
    G = 'h1'
    ws = QJ.widths(_NEW, lo=320, hi=1920, extra=tuple(range(320, 1921, 40)) + (834, 850, 1250))
    nw = len(range(320, 1921, STEP))
    for fname, font in FONTS:
        hn = heads_at(p, font, ws)
        snap = QJ.norm({str(w): ([hn[w]['h'], hn[w]['line'], hn[w]['hb'], hn[w]['body']] if hn.get(w) else None) for w in ws})
        bsnap = QJ.base('h1@%s/%s' % (eng, fname), snap)
        bad = [w for w in ws if not hn.get(w) or (str(w) in bsnap and snap[str(w)] != bsnap[str(w)])]
        note = '(표본 %d/%d · %s)' % (len(ws), nw, QJ.base_note('h1@%s/%s' % (eng, fname)))
        T(G, '%s 글꼴 %s — 폭 320~1920(%dpx 간격 %d 폭) 펼친 머리 높이 · 요소마다 줄 번호 · 배지 자리 · 본문 위 끝 = d6cf661(세모 없는 바탕)' % (eng, fname, STEP, nw),
          not bad, _tail({'어긋난 폭(표본)': bad[:10], '표본 834': [hn.get(834), bsnap.get('834')], '표본 1250': [hn.get(1250), bsnap.get('1250')]}, note))
        N(G, '%s 글꼴 %s 표본' % (eng, fname), {w: hn.get(w) for w in (834, 850, 1250)})


def h1(p, b, eng, br):
    """§B-1 머리 줄 나뉨 = d6cf661(세모 없는 바탕) · 글꼴 둘 · 헛잣대 = HEAD(세모가 흐름 안)"""
    G = 'h1'
    if QJ.REGRESS:   # regress — 폭 표본 · NEW 만 · d6cf661 은 기준 스냅샷(위 h1_regress)
        return h1_regress(p, eng)
    ns, nd, ne = M.new_env()
    QJ.sub('git:show-app')   # 셈(§B-4) — d6cf661 앱 풀기(gate 에서도 동작 무변)
    src0 = M.git('show', '%s:jo/index.html' % HDR_REV).decode('utf-8')
    z = Pg(br, eng, 'rpZ', src0, nd, ne)
    QJ.launch('base')   # 셈(§B-4) — 머리 바탕 d6cf661 띄움
    try:
        for fname, font in FONTS:
            hz = heads(z, font)
            hn = heads(p, font)
            hb = heads(b, font)
            bad, rng = diff_heads(hn, hz)
            T(G, '%s 글꼴 %s — 폭 320~1920(%dpx 간격 %d 폭) 펼친 머리 높이 · 요소마다 줄 번호 · 배지 자리 · 본문 위 끝 = d6cf661(세모 없는 바탕)' % (eng, fname, STEP, len(hn)),
              not bad, {'어긋난 폭 구간': rng[:10], '표본 834': [hn.get(834), hz.get(834)], '표본 1250': [hn.get(1250), hz.get(1250)]})
            badb, rngb = diff_heads(hb, hz)
            T(G + '-헛', '%s 글꼴 %s 헛잣대 바탕(HEAD · 세모가 흐름 안) — 어긋난 폭 있음' % (eng, fname), bool(badb), {'어긋난 폭 구간': rngb[:10]})
            N(G, '%s 글꼴 %s 표본' % (eng, fname), {w: hn.get(w) for w in (834, 850, 1250)})
    finally:
        z.close()


def h2(p, b, eng):
    """세모 — 자리(#laws 오른쪽 · 세로 가운데) · 크기 = HEAD · 누름(마우스 · iPad 손가락) → 접힘 · 다시 → 펼침"""
    G = 'h2'
    home(p)
    if QJ.GATE:
        home(b)
        fn, fb = p.ev("()=>__RP.fold()"), b.ev("()=>__RP.fold()")
    else:   # regress — 처리안 기준(h2 첫 칸): 바탕(HEAD) 세모 크기 = 기준 스냅샷(NEW 의 세모 가로·세로 · 스냅샷 없으면 첫 기록)
        fn = p.ev("()=>__RP.fold()")
        _bv = QJ.base('h2@%s/fold-wh' % eng, [fn['r']['w'], fn['r']['h']] if fn else None)
        if _bv is None:
            _bv = [fn['r']['w'], fn['r']['h']] if fn else [0, 0]
        fb = {'r': {'w': _bv[0], 'h': _bv[1]}}
    ok = fn and fn['pos'] == 'absolute' and 0 <= fn['dx'] <= 2 and abs(fn['dy']) <= 1 and abs(fn['r']['w'] - fb['r']['w']) < 0.5 and abs(fn['r']['h'] - fb['r']['h']) < 0.5 \
        and fn['t'] == '▴' and fn['hrailTxtX'] is not None and fn['r']['r'] <= fn['hrailTxtX'] + 0.5
    T(G, '%s 세모 — 흐름 밖 · #laws 오른쪽 끝 +1px(0~2) · 세로 가운데(±1) · 크기 = HEAD(%s×%s) · 탭 글자와 안 겹침' % (eng, fb['r']['w'], fb['r']['h']), ok, {'NEW': fn, 'HEAD': fb})
    for how, W, H in (('mouse', 1553, 900), ('touch', 834, 1194)):
        p.pg.set_viewport_size({'width': W, 'height': H}); (p.pg.wait_for_timeout(200) if QJ.GATE else _settle(p, 200, None, 'W3 폭을 바꾼 뒤 hdrFit · hdrFoldPos(ResizeObserver) 한 박자 — 앱 표지 없음'))
        a0 = p.ev("()=>__RP.fold()")
        (p.press(a0['at'], how, 500) if QJ.GATE else _press(p, a0['at'], how, 500, "()=>document.getElementById('app').classList.contains('hfold')", 'W4a 접힘(#app.hfold)이 섰다'))
        a1 = p.ev("()=>__RP.fold()")
        (p.press(a1['at'], how, 500) if QJ.GATE else _press(p, a1['at'], how, 500, "()=>!document.getElementById('app').classList.contains('hfold')", 'W4b 펼침(#app.hfold 없음)이 섰다'))
        a2 = p.ev("()=>__RP.fold()")
        T(G, '%s %s %d×%d — 누름 → 접힘(▾ · #app.hfold · 탭 줄 숨음 · 세모 자리 그대로) → 다시 → 펼침(▴)' % (eng, '마우스' if how == 'mouse' else '손가락', W, H),
          a1 and a1['hfold'] and a1['t'] == '▾' and not a1['hrailVis'] and abs(a1['dx'] - a0['dx']) < 0.6 and a2 and not a2['hfold'] and a2['t'] == '▴' and a2['hrailVis'],
          {'앞': {k: a0.get(k) for k in ('t', 'dx', 'dy')}, '접힘': a1 and {k: a1.get(k) for k in ('t', 'hfold', 'hrailVis', 'dx')}, '펼침': a2 and {k: a2.get(k) for k in ('t', 'hfold', 'hrailVis')}})
    p.pg.set_viewport_size({'width': 1553, 'height': 900})
    fs = p.ev("()=>{let u={};try{u=JSON.parse(localStorage.getItem('jopangi_ui')||'{}')}catch(e){}return u.hdr_fold}")
    T(G, '%s 기억 키 jopangi_ui.hdr_fold 그대로(펼침 = false)' % eng, fs is False, fs)


# ══════════ 판 이름 칩 ══════════
def a2(p, b, eng):
    G = 'a2'
    home(p)
    k7 = p.ev("()=>__RP.keyP7('P7-0118')")
    go_key(p, k7)
    c7 = p.ev("k=>__RP.card(k)", k7)
    qp7 = mb_pop(p, k7)
    p.ev("()=>__HM.closeAll()")
    T(G, '%s 7판 카드 P7-0118 — 머리 접기 칩 「H7」 · 지문 팝업 쪽 글 「H7 p.N」 · 「제7판」 칩 없음' % eng,
      bool(c7) and c7['qexp'] == ['H7'] and 'H7 p.' in (qp7 or {}).get('t', '') and '제7판 p.' not in (qp7 or {}).get('t', ''), {'칩': c7 and c7['qexp'], '팝업': (qp7 or {}).get('t', '')[:160]})
    if QJ.GATE:   # 헛잣대(처리안 관문만) — regress 에서 끔
        home(b)
        go_key(b, b.ev("()=>__RP.keyP7('P7-0118')"))
        cb = b.ev("k=>__RP.card(k)", b.ev("()=>__RP.keyP7('P7-0118')"))
        T(G + '-헛', '%s 헛잣대 바탕 — P7-0118 칩 「제7판」' % eng, bool(cb) and cb['qexp'] == ['제7판'], cb and cb['qexp'])
    if not QJ.want('a2-8판새'):   # smoke — a2-7판(카드 머리 칩 H7)까지만
        return
    keys = p.ev("()=>__RP.p8keys()")
    bad = {}
    first = None
    for k in keys:
        go_key(p, k)
        c = p.ev("k=>__RP.card(k)", k)
        if first is None:
            first = c
        if not c or '제7판' in c['t'] or 'H8' not in c['qexp'] or '8판 새' not in c['p8'] or not any(t.startswith('H8 p.') for t in [c['t']]) and 'H8 p.' not in c['t']:
            bad[k] = c and {'qexp': c['qexp'], 'p8': c['p8'], '제7판': '제7판' in c['t']}
    T(G, '%s 8판 새 카드 %d 장 — 머리 칩 「H8」 · 「H8 p.N N번」 · 「8판 새」 그대로 · DOM 전체에 「제7판」 0' % (eng, len(keys)), len(keys) == 19 and not bad, {'어긋남': bad, '표본': first and {k: first[k] for k in ('qexp', 'qbv', 'p8')}})
    k34 = p.ev("()=>__RP.keyLid('2026-63-B1', 4)") or None
    # 리담 34 표본 T2663014 — 7판 카드에 흡수돼 리담 카드는 없다 → 그 문항의 기출뷰 칸에 선다(p8up a7 과 같은 자리)
    cl = exv_p8(p, 'T2663014')
    T(G, '%s 리담 34 표본 T2663014 — 기출뷰 그 지문 줄 「H8 p.22 유제」' % eng, bool(cl) and 'H8 p.22 유제' in cl, cl)
    if QJ.GATE:   # 헛잣대(처리안 관문만) — regress 에서 끔
        cb2 = exv_p8(b, 'T2663014')
        T(G + '-헛', '%s 헛잣대 바탕 — 「8판 p.22 유제」' % eng, bool(cb2) and '8판 p.22 유제' in cb2 and 'H8' not in ' '.join(cb2), cb2)
    keep = {}
    for cat, want in (('문장', '8판 고침'), ('없음', '8판에 없음')):
        f = p.ev("c=>__RP.firstCat(c)", cat)
        go_key(p, f['k'])
        c = p.ev("k=>__RP.card(k)", f['k'])
        keep[cat] = {'id': f['id'], 'p8': c and c['p8'], 'qexp': c and c['qexp']}
    T(G, '%s 안 바꾸는 칩 — 「8판 고침」 · 「8판에 없음」 그대로(그 카드 판 칩은 H7)' % eng,
      '8판 고침' in (keep['문장']['p8'] or []) and '8판에 없음' in (keep['없음']['p8'] or []) and keep['문장']['qexp'] == ['H7'], keep)
    # 🔍 통합 검색 줄 · 지문 팝업
    t8 = p.ev("()=>{const z=Object.values(VJ.P7map).find(z=>z.판8&&z.판8.cat==='새'&&z.uid==='T8N0001');return z?String(z.t).replace(/\\s+/g,' ').slice(4,20):null}")
    res = sk_search(p, t8)
    T(G, '%s 🔍 통합 검색 「%s」 — 지문 줄 머리 「H8 …」 · 줄 끝 태그 「H8」 · 「제7판」 0' % (eng, t8),
      any(r['head'].startswith('H8 ') and r['tag'] == 'H8' for r in res) and not any('제7판' in r['head'] + r['tag'] for r in res), res[:4])
    p.pg.keyboard.press('Escape')
    if QJ.GATE:   # 헛잣대(처리안 관문만) — regress 에서 끔
        rb = sk_search(b, t8)
        T(G + '-헛', '%s 헛잣대 바탕 — 줄 머리 「8판 …」 · 태그 「제7판」' % eng, any(r['tag'] == '제7판' for r in rb), rb[:3])
        b.pg.keyboard.press('Escape')
    for k, want in (('T8N0001', 'H8'), (k7, 'H7')):
        qp = mb_pop(p, k)
        T(G, '%s 지문 팝업(1차객 🔍 %s → 줄 누름) — 보라 칩 qpc1 「%s」' % (eng, k, want), bool(qp) and qp['qpc1'] == want, qp)
        p.ev("()=>__HM.closeAll()")


def exv_p8(p, uid):
    """그 uid 가 든 문항의 해를 기출뷰로 열고(첫 화면 해 줄 누름 · 다음 쪽 누름) 그 문항 칸의 .p8c 글"""
    y = p.ev("u=>{const q=(VJ.qs||[]).find(q=>(q.지문||[]).some(z=>z.uid===u));return q?String(q.연도):null}", uid)
    qk = p.ev("u=>{const q=(VJ.qs||[]).find(q=>(q.지문||[]).some(z=>z.uid===u));return q?giKey(q):null}", uid)
    if not y:
        return None
    home(p)
    (p.click(p.ev("y=>{const r=document.querySelector('#slot .mbur[data-giy=\"'+y+'\"] .nm');if(!r)return null;r.scrollIntoView({block:'center'});const b=r.getBoundingClientRect();return {cx:b.left+b.width/2,cy:b.top+b.height/2,on:true}}", y), 2000) if QJ.GATE else _clk(p, p.ev("y=>{const r=document.querySelector('#slot .mbur[data-giy=\"'+y+'\"] .nm');if(!r)return null;r.scrollIntoView({block:'center'});const b=r.getBoundingClientRect();return {cx:b.left+b.width/2,cy:b.top+b.height/2,on:true}}", y), 2000, "()=>!!document.querySelector('#slot .exv-paper')", 'W7a 기출뷰 시험지(#slot .exv-paper)가 섰다'))
    for _ in range(5):
        got = p.ev("k=>{const q=document.querySelector('#slot .exv-q[data-exq=\"'+k+'\"]');return q?[...q.querySelectorAll('.p8c')].map(x=>x.textContent.trim()):null}", qk)
        if got is not None:
            return got
        nx = p.ev("()=>{const b=document.querySelector('#slot [data-uzexnext]');if(!b)return null;b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return {cx:r.left+r.width/2,cy:r.top+r.height/2,on:true}}")
        if not (p.click(nx, 1200) if QJ.GATE else _clk(p, nx, 1200, "k=>!!document.querySelector('#slot .exv-q[data-exq=\"'+k+'\"]')", 'W7b 다음 쪽 — 그 문항 칸(.exv-q)이 섰다(없으면 옛 대기만큼만 기다리고 다음 쪽)', qk, 1200)):
            break
    return None


def sk_search(p, q):
    """통합 검색 — 🔍 지문 범위 켜고 #skin 에 키보드로 친다(열기 = openSk · 치기 = 진짜 키보드)"""
    p.ev("()=>{try{closeAllPops()}catch(e){}openSk();SKON.jimun=true;try{skPaint()}catch(e){}}")
    (p.click(p.ev("()=>__RP.skin()"), 200) if QJ.GATE else _clk(p, p.ev("()=>__RP.skin()"), 200, "()=>document.activeElement===document.getElementById('skin')", 'W6a 검색 칸(#skin)에 초점'))
    p.pg.keyboard.type(q or '', delay=10)
    (p.pg.wait_for_timeout(1500) if QJ.GATE else _settle(p, 1500, "q=>{const i=document.getElementById('skin'),b=document.getElementById('skres'),g=b&&b.lastElementChild;return !!i&&i.value===q&&!!g&&/^↵ 열기/.test(g.textContent||'')}" if q else None, 'W6b 통합 검색 끝(#skres 맨 끝 줄 「↵ 열기 · Esc 닫기」 — skRun 이 마지막에 붙임)' if q else 'W6b 빈 검색어 — 끝 줄이 안 붙는다(표지 없음)', q))
    return p.ev("()=>__RP.skRows()") or []


def mb_pop(p, k, gk=None):
    """1차객 🔍(ID 찾기) → 줄 누름 → 지문 팝업 · 찾기 결과도 기출/기타 거름을 거친다(add3 §A-8) → 그 카드 쪽 거름에서 연다"""
    home(p)
    g0 = p.ev("k=>{try{return uzIsGi(k)?'g':'x'}catch(e){return 'g'}}", k)
    home(p, gk or g0)
    (p.click(p.ev("()=>__HM.at('#slot .mbsr input')"), 200) if QJ.GATE else _clk(p, p.ev("()=>__HM.at('#slot .mbsr input')"), 200, "()=>{const i=document.querySelector('#slot .mbsr input');return !!i&&document.activeElement===i}", 'W5a 1차객 검색 칸(.mbsr input)에 초점'))
    p.pg.keyboard.press('Control+A'); p.pg.keyboard.press('Delete')
    p.pg.keyboard.type(k, delay=10)
    (p.pg.wait_for_timeout(800) if QJ.GATE else _settle(p, 800, "k=>String(S.oxQ||'').trim()===k&&[...document.querySelectorAll('#slot .mbres .rr')].some(x=>typeof x.onclick==='function')", 'W5b 검색 결과 줄(.mbres .rr · onclick)이 섰다 — 140ms 디바운스 뒤 mbSearchRun', k))
    row = p.ev("()=>{const r=[...document.querySelectorAll('#slot .mbres .rr')].find(x=>typeof x.onclick==='function');if(!r)return null;r.scrollIntoView({block:'center'});"
               "const b=r.getBoundingClientRect(),at=document.elementFromPoint(b.left+b.width/2,b.top+b.height/2);return {cx:b.left+b.width/2,cy:b.top+b.height/2,on:!!at&&r.contains(at)};}")
    (p.click(row, 1200) if QJ.GATE else _clk(p, row, 1200, r"()=>(typeof POPS!=='undefined'?POPS:[]).some(x=>/^q\|📝 지문 /.test(x._pk||''))", 'W5c 지문 팝업(POPS · _pk q|📝 지문)이 섰다'))
    return p.ev("()=>__RP.qpop()")


# ══════════ 이동 ══════════
def landed(p, k):
    for _ in range(30):
        c = p.ev("k=>__RP.card(k)", k)
        if c and c['vis']:
            break
        p.pg.wait_for_timeout(100)
    (p.pg.wait_for_timeout(700) if QJ.GATE else _settle(p, 700, None, 'W8 도착한 카드의 smooth scroll(scrollIntoView behavior:smooth) 끝 — 앱이 끝 표지를 안 낸다'))
    c = p.ev("k=>__RP.card(k)", k)
    vh = p.ev("()=>innerHeight")
    toasts = p.ev("()=>__RP.toasts()")
    ok = bool(c) and c['vis'] and abs((c['r']['y'] + min(c['r']['h'], vh) / 2) - vh / 2) < vh * 0.35 and not any('거르기' in t or '찾지 못했다' in t for t in toasts)
    return ok, {'카드': c and {x: c[x] for x in ('vis', 'r', 'hit')}, '토스트': toasts}


def a3(p, b, eng):
    G = 'a3'
    t8 = p.ev("()=>{const z=Object.values(VJ.P7map).find(z=>z.uid==='T8N0001');return z?String(z.t).replace(/\\s+/g,' ').slice(4,20):null}")
    for gk in ('g', 'x'):
        for who, q in (('NEW', p), ('헛', b)) if QJ.GATE else (('NEW', p),):   # regress — NEW 만
            home(q, gk)
            q.ev("()=>__RP.toastClear()")
            rows = sk_search(q, t8)
            (q.click(q.ev("r=>__RP.skRowAt(r)", '^(H8|8판) '), 900) if QJ.GATE else _clk(q, q.ev("r=>__RP.skRowAt(r)", '^(H8|8판) '), 900, r"()=>(typeof POPS!=='undefined'?POPS:[]).some(x=>/^q\|📝 /.test(x._pk||'')&&[...x.querySelectorAll('button.tool')].some(b=>/그 지문으로 가기/.test(b.textContent||'')))", 'W11a 지문 팝업(「그 지문으로 가기」 단추)이 섰다'))
            jp = q.ev("()=>__RP.jpop()")
            (q.click(jp and jp['go'], 300) if QJ.GATE else _clk(q, jp and jp['go'], 300, "()=>true", 'W11b 눌렀다 — 뒤따르는 landed() 가 카드 보임을 기다린다(여기선 프레임만)'))
            ok, d = landed(q, 'T8N0001')
            if who == 'NEW':
                T(G, '%s 거름 %s — 🔍 「H8 …」 줄 → 「그 지문으로 가기 ↗」 → T8N0001 카드 화면 가운데 · 반짝임 · 토스트 없음' % (eng, '기출' if gk == 'g' else '기타'), ok and jp is not None, d)
            else:
                T(G + '-헛', '%s 거름 %s 헛잣대 바탕 — 닿지 않음(토스트 · 카드 없음)' % (eng, '기출' if gk == 'g' else '기타'), not ok, d)
        for who, q in (('NEW', p),):
            home(q, gk)
            q.ev("()=>__RP.toastClear()")
            qp = mb_pop(q, 'T8N0001')                       # 팝업 = 그 카드 쪽 거름(기타)에서 연다
            q.ev("v=>{UZGK=v}", gk)                          # 누르기 전 거름 = 이 칸의 거름(기출이면 카드가 걸린다)
            (q.click(qp and qp['go'], 300) if QJ.GATE else _clk(q, qp and qp['go'], 300, "()=>true", 'W11c 눌렀다 — 뒤따르는 landed() 가 카드 보임을 기다린다(여기선 프레임만)'))
            ok, d = landed(q, 'T8N0001')
            T(G, '%s 거름 %s — 지문 팝업 「↪ 이동」 → T8N0001 카드 화면 가운데 · 토스트 없음' % (eng, '기출' if gk == 'g' else '기타'), ok and qp is not None, {'팝업': qp and qp['qpc1'], **d})
    # TX0595 무변 — 두 판 같은 결과
    out = {}
    for who, q in (('NEW', p), ('HEAD', b)) if QJ.GATE else (('NEW', p),):   # regress — NEW 만
        home(q, 'g')
        q.ev("()=>__RP.toastClear()")
        qp = mb_pop(q, 'TX0595')
        (q.click(qp and qp['go'], 300) if QJ.GATE else _clk(q, qp and qp['go'], 300, "()=>true", 'W11d 눌렀다 — 뒤따르는 landed() 가 카드 보임을 기다린다(여기선 프레임만)'))
        out[who] = landed(q, 'TX0595')
    if QJ.REGRESS:   # 처리안 기준(a3-TX0595) — 바탕(HEAD)이 「닿았나」 = 기준 스냅샷(NEW 가 닿았나 · 스냅샷 없으면 첫 기록)
        out['HEAD'] = (QJ.base('a3-TX0595@%s' % eng, out['NEW'][0]), None)
    T(G, '%s TX0595(7판 기타) 「↪ 이동」 결과 = 바탕 그대로' % eng, out['NEW'][0] == out['HEAD'][0], {k: v[0] for k, v in out.items()})


# ══════════ P7-1153 ══════════
def a4(p, b, eng):
    G = 'a4'
    home(p)
    if QJ.GATE:
        home(b)
    cat = p.ev("()=>__RP.p8cat('P7-1153')")
    cnt = p.ev("()=>__RP.catCount()")
    k = p.ev("()=>__RP.keyP7('P7-1153')")
    go_key(p, k)
    c = p.ev("k=>__RP.card(k)", k)
    T(G, '%s P7-1153 — 판8.cat 자리(p.699 · pdf 709) · 카드에 「8판 고침」 칩 없음 · 셈 문장 23 · 자리 3' % eng,
      bool(cat) and cat.get('cat') == '자리' and cat.get('p8') == 699 and cat.get('pdf8') == 709 and c and not any('8판 고침' in x for x in c['p8'])
      and cnt.get('문장') == 23 and cnt.get('자리') == 3, {'판8': cat, '셈': cnt, '칩': c and c['p8']})
    if QJ.GATE:   # 헛잣대(처리안 관문만) — regress 에서 끔
        cb = b.ev("()=>__RP.p8cat('P7-1153')")
        T(G + '-헛', '%s 헛잣대 바탕 — P7-1153 판8.cat 문장' % eng, bool(cb) and cb.get('cat') == '문장', cb)


def d4():
    """⚙ — 얹은 데이터에 한 번 더 = 그대로(None) · 셈 WANT"""
    G = 'd4'
    import _p8up_apply as P
    objs = {f: json.loads(open(os.path.join(_DATA, f), 'rb').read().decode('utf-8')) for f in P.FILES}
    ref = json.loads(open(P.REF, 'rb').read().decode('utf-8')) if hasattr(P, 'REF') else None
    fill = json.loads(open(P.FILL, 'rb').read().decode('utf-8'))
    try:
        log, bad = P.apply(objs, ref, fill)
    except Exception as e:
        log, bad = repr(e), ['err']
    T(G, '⚙ _p8up_apply — 이 판 인도 데이터에 한 번 더 얹음 = 그대로(None) · WANT 문장 23 · 자리 3', log is None and not bad and P.WANT['문장'] == 23 and P.WANT['자리'] == 3, {'log': str(log)[:200], 'bad': bad})


# ══════════ 서랍 ══════════
def drawer(p, w, font):
    p.ev("f=>__RP.font(f)", font)
    p.ev("w=>{try{closeAllPops()}catch(e){}S.law='특허법';S.tab='jo';S.treeW=w;S.joStar=false;return render()}", w)
    (p.pg.wait_for_timeout(700) if QJ.GATE else _settle(p, 700, "w=>{const r=[...document.querySelectorAll('.tree .r')].filter(x=>x.querySelector('span.nm'));return r.length>50&&getComputedStyle(document.documentElement).getPropertyValue('--trw').trim()===(w+'px')}", 'W9 조 서랍(.tree .r) 줄이 섰고 폭(--trw)이 맞다 — render() 가 --trw 를 걸고 viewJo 가 줄을 짓는다', w))
    d = p.ev("()=>__RP.drawer()") or []
    p.ev("()=>__RP.font('')")
    return d


def a5(p, b, eng):
    G = 'a5'
    for fname, font in FONTS:
        d = drawer(p, 212, font)
        r2 = next((r for r in d if r['t'].startswith('제2조 ')), None)
        clip = [r['t'] for r in d if r['no'] and r['no']['clip']]
        st = r2 and r2['st']
        half = bool(st and st['sd'] and st['sd']['r'] > st['r']['r'] + 0.5 and st['sd']['y'] < st['r']['y'] + st['r']['h'] - 1)
        ok = bool(r2) and r2['tt'] and r2['tt']['to'] == 'ellipsis' and not clip and not half and len(d) > 50
        T(G, '%s 글꼴 %s 서랍 212 — 이름 칸 말줄임(ellipsis) · 조 번호 가려진 줄 0(%d 줄) · 「★ 2」 숫자가 반쯤 잘리지 않음(통째 보임 또는 통째 숨음)' % (eng, fname, len(d)),
          ok, {'제2조': r2, '번호 가림': clip[:6]})
        if QJ.GATE:   # 헛잣대(처리안 관문만) — regress 에서 끔
            db = drawer(b, 212, font)
            clipb = [r['t'] for r in db if r.get('no') and r['no']['clip']]
            halfb = [r['t'] for r in db if r.get('half')]
            T(G + '-헛', '%s 글꼴 %s 헛잣대 바탕 서랍 212 — 「★ 2…」 날짜 첫 숫자가 칩 끝에 반쯤 걸친 줄 있음(text-overflow clip)' % (eng, fname), bool(halfb), {'반쯤': halfb[:4], '번호 가림(이 글꼴에선 0 일 수 있음 · 지시서 §0 ⑤)': clipb[:4]})
        if QJ.GATE:
            w3n, w3b = drawer(p, 320, font), drawer(b, 320, font)
        else:   # regress — 처리안 기준(a5-320): 바탕 줄 = 기준 스냅샷(NEW 줄의 [글 · 이름 칸 폭] 목록 · 스냅샷 없으면 첫 기록)
            w3n = drawer(p, 320, font)
            _bv = QJ.base('a5-320@%s/%s' % (eng, fname), [[x['t'], x['nmw']] for x in w3n])
            w3b = [{'t': t_, 'nmw': w_} for t_, w_ in _bv]
        # ★ A-6(a) 둘째 바퀴 9/30 — joscreen0929 A-1-6 이 절(lv2) 머리 글 앞에 접기 표지(▾/▸)를 더했다(바탕 e36829b 「제1절 국제출원절차」 → 「▾ 제1절 국제출원절차」 · 특허 제10장 절 둘)
        #   → 새 쪽 글 앞 표지 하나만 빼고 맞댄다(장 머리는 두 판 다 표지가 있어 그대로 같음) · 폭 「좁아지지 않음」 조건 그대로
        # ★ A-6(a) 셋째 바퀴 9/30 — revfix0930 A-5 가 장 머리를 한 줄로 했다(이름 flex:1 1 auto · min-width 0 말줄임 · 범위 오른쪽 flex:none 늘 다 보임 · 「좁으면 이름이 먼저 줄어든다」)
        #   바탕 e36829b 장 머리 이름은 flexShrink 0(제 글 폭 그대로 · revfix0929b A-11 이 걷음)이라 긴 장 이름(특허 제10장)은 넓은 서랍 320 에서도 새 판이 좁다(245.84 → 205.03 = 그 판 관문 B7 PC320 long sw 246 · cw 205 · ellipsis · title)
        #   → 장 머리 줄(바탕 글 앞 ▾/▸)만: 바탕보다 좁으면 말줄임(text-overflow ellipsis · scrollWidth > clientWidth) + 툴팁(title = 이름 전체)일 때 PASS · 다른 줄 폭 조건 그대로
        head_ell = lambda x, y: bool(re.match(u'^[▾▸] ', y['t'])) and x.get('to') == 'ellipsis' and x.get('nmsw', 0) > x.get('nmcw', 0) and ' '.join((x.get('tip') or '').split()) == re.sub(u'^[▾▸] ', u'', x['t'])
        ok_row = lambda x, y: (x['t'] == y['t'] or re.sub(u'^[▾▸] ', u'', x['t']) == y['t']) and (x['nmw'] > y['nmw'] - 0.6 or head_ell(x, y))
        same = len(w3n) == len(w3b) and all(ok_row(x, y) for x, y in zip(w3n, w3b))   # ★ A-6(a) 9/30 — joscreen0929 A-1(줄 끝 ✏️·🔗 → 점+체크 · 179 → 195) · revfix0930 A-5(장 머리 이름 flex 78 → 184)로 이름 칸이 넓어짐 → 「바탕보다 좁아지지 않음」 · 줄 수 · 줄 글자 = 바탕 그대로
        T(G, '%s 글꼴 %s 넓은 서랍 320 — 줄 글자 = 바탕 · 이름 칸 폭 ≥ 바탕 − 0.5(장 머리가 좁아지면 말줄임 + 툴팁)' % (eng, fname), same,
          {'줄': [len(w3n), len(w3b)], '어긋난 줄(새 글 · 바탕 글 · 새 폭 · 바탕 폭)': [(x['t'], y['t'], x['nmw'], y['nmw']) for x, y in zip(w3n, w3b) if not ok_row(x, y)][:5]})
    p.ev("()=>{S.treeW=212;S.tab='jimun';return render()}")
    if QJ.GATE:
        b.ev("()=>{S.treeW=212;S.tab='jimun';return render()}")


BR = {}
PARTS = [('h1', h1), ('h2', h2), ('a2', a2), ('a3', a3), ('a4', a4), ('a5', a5)]
DPARTS = [('d4', d4)]
SMOKE_PARTS = {'h2': ('chromium', 'webkit'), 'a2': ('chromium',)}   # smoke(_task_qa_slim A-4) — h2(세모 자리 · 마우스/손가락 누름 · 기억 · WebKit 손가락도) · a2 첫 칸(카드 머리 칩 H7) · ERR(엔진마다) · 그 밖(h1 · a2 나머지 · a3 · a4 · a5 · d4)은 건넘


def run_engine(pw, eng):
    if QJ.SMOKE and not any(eng in v for v in SMOKE_PARTS.values()):   # smoke — 이 엔진에서 잴 smoke 칸이 없으면 브라우저도 안 띄운다
        return
    br = getattr(pw, eng).launch()
    BR[eng] = br
    ns, nd, ne = M.new_env()
    if QJ.GATE:   # regress — 바탕(HEAD) 앱·데이터를 풀지 않는다(git show · git archive 0)
        QJ.sub('git:show-app'); QJ.sub('git:archive')   # 셈(§B-4) — M.base_env 가 부르는 둘(gate 에서도 동작 무변)
        bs, bd, be = M.base_env()
    try:
        p = Pg(br, eng, 'rpN', ns, nd, ne)
        QJ.launch('new')
        if QJ.GATE:   # regress — 바탕 Pg 를 띄우지 않는다(b = None)
            b = Pg(br, eng, 'rpB', bs, bd, be)
            QJ.launch('base')
        else:
            b = None
        try:
            for k, fn in PARTS:
                if ONLY and k not in ONLY:
                    continue
                if QJ.SMOKE and eng not in SMOKE_PARTS.get(k, ()):
                    continue
                print('── %s · %s' % (eng, k), flush=True)
                try:
                    if QJ.GATE:
                        fn(p, b, eng, br) if k == 'h1' else fn(p, b, eng)
                    else:
                        with QJ.stage('%s·%s' % (eng, k)):
                            fn(p, b, eng, br) if k == 'h1' else fn(p, b, eng)
                except Exception as e:
                    T('RUN', u'%s · %s 묶음이 멈춤' % (eng, k), False, repr(e)[:600])
            T('ERR', u'%s — NEW 앱 오류 0' % eng, not p.errs_all(), p.errs_all()[:6])
        finally:
            p.close()
            if QJ.GATE:
                b.close()
    finally:
        br.close()


def main():
    shutil.rmtree(os.path.join(M.WORK, 'head'), ignore_errors=True)
    os.makedirs(M.WORK, exist_ok=True)
    t0 = time.time()
    for k, fn in DPARTS:
        if not QJ.want(k):   # smoke — 데이터 칸(d4)은 건넘
            continue
        if not ONLY or k in ONLY:
            try:
                fn()
            except Exception as e:
                T('RUN', u'%s 데이터 묶음이 멈춤' % k, False, repr(e)[:600])
    if not ONLY or any(k in ONLY for k, _ in PARTS):
        with sync_playwright() as pw:
            for eng in ENGS:
                RES.append(('ENG', eng, None, ''))
                run_engine(pw, eng)
    npass = sum(1 for r in RES if r[2] is True); nfail = sum(1 for r in RES if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · %s · NEW %s · 데이터 %s · 바탕 HEAD %s · 머리 바탕 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), 'revfix0928pm', os.path.basename(_NEW), _DATA,
                (M.git('rev-parse', '--short', 'HEAD').decode().strip() if QJ.GATE else '(regress — 바탕 안 띄움)'), HDR_REV, ','.join(ENGS)))
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[ok], g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:900]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
