# -*- coding: utf-8 -*-
r"""uid_add2 §E + mbsame_add2 §C + mbsame_add3 §B — 한 판(9/27) 관문 하네스.

  python _harness_jo_uidmbs2.py --new <앱> --data <jo/data> [--exam <gichul/pdf>] [--only a3,a2,u,...] [--eng chromium,webkit]

  NEW  = 이 판 앱 + 새 데이터 · BASE = genie HEAD(539131a jo = 바로 앞 인도판) 앱 + HEAD 데이터 — 칸마다 헛잣대(바탕에서 FAIL)
  누름 = 진짜 포인터(page.mouse · 손가락 = Chromium CDP 터치 r22 · WebKit touchscreen.tap) · 보임 = display ≠ none · 높이 > 0 · 자리 = elementFromPoint
  바탕 틀은 mbsame 하네스(_harness_jo_gaek_mbsame.py)의 serve·Pg·__HM 을 그대로 쓰고 이 판 도구(__UZ)를 뒤에 붙인다.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import io, json, os, re, sys, time, subprocess, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


_NEW, _DATA, _EXAM = ARG('--new'), ARG('--data'), ARG('--exam')
_MBREF, _MBREFWK = ARG('--mbref', ''), ARG('--mbrefwk', '')   # 민법 Q0275 칩 기준값(_uidmbs2_mb_chipref.py)
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_uidmbs2_result.txt'))
sys.argv = [sys.argv[0], '--new', _NEW, '--data', _DATA, '--base', '539131a'] + (['--exam', _EXAM] if _EXAM else [])   # A-6(d) 9/30 — 바탕 = 인도 때 HEAD 539131a(docstring 「539131a jo = 바로 앞 인도판」) · HEAD 로 두면 인도 뒤 헛잣대·바탕 대조가 새 판끼리 맞대 거꾸로 FAIL
sys.path.insert(0, HERE)
import _harness_jo_gaek_mbsame as M   # noqa: E402
from playwright.sync_api import sync_playwright   # noqa: E402
M.TESTS = M.TESTS + '\n' + io.open(os.path.join(HERE, '_harness_jo_uidmbs2_tests.js'), encoding='utf-8').read()
M.WORK = M.WORK + '_uz'
RES = []


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


class Pg(M.Pg):
    """엔진 이름을 들고 다닌다 — 손가락 = Chromium CDP r22 · WebKit touchscreen.tap"""
    def __init__(self, br, eng, tag, src, data, exam, W=1440, H=900, **k):
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


def envs():
    ns, nd, ne = M.new_env()
    bs, bd, be = M.base_env()
    return (ns, nd, ne), (bs, bd, be)


def reload_keep(p):
    """새로고침 흉내 — 저장소를 안 비운다(?keep=1 · CJ.SEED)"""
    p.pg.goto('http://127.0.0.1:%d/index.html?tok=1&keep=1' % p.port, wait_until='load', timeout=180000)
    p.pg.wait_for_function(M.READY, timeout=180000); p.pg.wait_for_timeout(700)


def go_key(p, k):
    sel = p.ev("k=>__UZ.selOfKey(k)", k)
    if not sel:
        return None
    p.ev("s=>__HM.go(s)", sel)
    pg = p.ev("k=>{const P=(OXPOOL||{})[k];if(!P)return null;const d=P.dom;const c=[...document.querySelectorAll('.qb.id')].find(b=>b.textContent.trim()===k);return c?null:(OXDOMPG||{})[d]}", k)
    if pg:
        p.ev("n=>__HM.page(n)", pg)
    return sel


def home(p, law='특허법', gk='g'):
    p.ev("l=>__HM.home(l)", law)
    if p.ev("()=>__UZ.has('UZGK')"):
        p.ev("v=>__UZ.gk(v)", gk)


# ══════════ mbsame_add3 §B-8 기출/기타 · §B-6 필터 · §B-8 접기·정렬·「필터」 ══════════
def g_a8(p, b, eng):
    G = 'a3-8'
    home(p); home(b)
    h = p.ev("()=>__UZ.hm()")
    chips = {c['t'].split(' ')[0]: c for c in h['chips']}
    gi, gx = [c for c in h['chips'] if c['gk'] == 'g'], [c for c in h['chips'] if c['gk'] == 'x']
    num = lambda s: int(re.sub(r'[^\d]', '', s.split(' ')[-1]) or -1)
    ng, nx = (num(gi[0]['t']) if gi else -1), (num(gx[0]['t']) if gx else -1)
    sep = p.ev("()=>__UZ.sepInRow()")
    anhp = next((int(re.sub(r'[^\d]', '', x)) for x in h['legend'] if x.startswith('안 품')), -1)
    c1, d1, k1 = p.ev("()=>__UZ.hmChip('^1\\\\. 특허제도')"), p.ev("()=>__UZ.cardTot(1)"), p.ev("()=>__UZ.drawerHead('1. 특허제도')")
    r11 = p.ev("()=>__UZ.rowTot('1.1 목적')")
    T(G, u'히트맵 머리 「│ 기출 N · 기타 M」 — 대목차 칩 뒤 같은 줄 흐름 · 처음 기출 켜짐 · 범례 「안 품」 = 기출 · 머리 「기출 · 기타 · 문항」',
      bool(gi and gx and gi[0]['on'] and not gx[0]['on'] and sep and sep['order'] and anhp == ng and re.match(u'기출 [\\d,]+ · 기타 [\\d,]+ · 문항', h['head'] or '')),
      {'기출': ng, '기타': nx, '범례 안 품': anhp, '구분': sep, '머리': h['head']})
    T(G, u'기출 — 1 특허제도 칩 = 카드 「총 N문제」 = 서랍 머리(한 함수) · 1.1 목적 「문항 없음」·📋 없음',
      bool(c1 and c1['n'] == d1 == k1 and r11 and r11['none'] and not r11['jn']), {'칩': c1, '카드': d1, '서랍': k1, '1.1 목적': r11})
    hb = b.ev("()=>__UZ.hm()")
    T(G + '-헛', u'헛잣대 바탕 — 기출/기타 칩 없음 · 1 특허제도 칩 68', not [c for c in hb['chips'] if c['gk']] and (b.ev("()=>__UZ.hmChip('^1\\\\. 특허제도')") or {}).get('n') == 68,
      {'바탕 칩': [c['t'] for c in hb['chips']][:4]})
    for how in ('mouse', 'touch'):
        at = p.ev("()=>__UZ.gkAt('x')")
        p.press(at, how, 1500)
        c1x, d1x, k1x = p.ev("()=>__UZ.hmChip('^1\\\\. 특허제도')"), p.ev("()=>__UZ.cardTot(1)"), p.ev("()=>__UZ.drawerHead('1. 특허제도')")
        hx = p.ev("()=>__UZ.hm()")
        on = [c['gk'] for c in hx['chips'] if c['on'] and c['gk']]
        anhx = next((int(re.sub(r'[^\d]', '', x)) for x in hx['legend'] if x.startswith('안 품')), -1)
        unk, gic, dgi = p.ev("()=>__UZ.unkCard()"), p.ev("()=>__UZ.giCardN()"), p.ev("()=>__UZ.drawerGi()")
        r11x = p.ev("()=>__UZ.rowTot('1.1 목적')")
        jn = None
        if r11x and r11x['jn']:
            p.press(p.ev("()=>__UZ.rowAt('1.1 목적','.mbchip.jn')"), how, 1200)
            jn = p.ev("()=>__UZ.jn()")
            p.ev("()=>__HM.closeAll()")
        T(G, u'「기타」 누름(%s) → 기타 %d · 칩 = 카드 = 서랍 · 미분류·변리사 기출 카드·서랍 줄 DOM 0 · 1.1 목적 📋 12 줄' % (how, nx),
          bool(on == ['x'] and anhx == nx and c1x and c1x['n'] == d1x == k1x and not unk and gic == 0 and dgi == 0 and jn and jn['rows'] == 12),
          {'켜짐': on, '안 품': anhx, '칩': c1x, '카드': d1x, '서랍': k1x, '미분류': unk, '기출 줄': gic, '서랍 해 줄': dgi, '📋': jn and jn['rows']})
        at = p.ev("()=>__UZ.gkAt('g')")
        p.press(at, how, 1500)
        r11g = p.ev("()=>__UZ.rowTot('1.1 목적')")
        T(G, u'「기출」 되돌림(%s) → 1.1 목적 「문항 없음」·📋 없음' % how, bool(r11g and r11g['none'] and not r11g['jn']), r11g)
    # 새로고침 = 기출 · 저장 안 함(기록 키 무변)
    p.ev("()=>__UZ.gk('x')")
    ui = p.ev("()=>__UZ.ls('jopangi_ui')") or {}
    reload_keep(p)
    p.ev("l=>__HM.home(l)", '특허법')
    h2 = p.ev("()=>__UZ.hm()")
    on2 = [c['gk'] for c in h2['chips'] if c['on'] and c['gk']]
    T(G, u'새로고침 → 기출(기기 값 · jopangi_ui·기록 키에 기출/기타 칸 없음)', on2 == ['g'] and not any('gk' in k or 'uzgk' in k.lower() for k in ui), {'켜짐': on2, 'ui 칸': sorted(ui)[:40]})
    # 상표·디보 — 리담 = 기출 · 기타 0
    for law in ('상표법', '디자인보호법'):
        home(p, law)
        hl = p.ev("()=>__UZ.hm()")
        gl = [c['t'] for c in hl['chips'] if c['gk']]
        N(G, u'%s — 기출/기타 칩(리담 전부 = 기출 · 제7판 없음)' % law, {'칩': gl, '머리': hl['head']})
    home(p)


def g_a6(p, b, eng):
    G = 'a3-6'
    home(p); home(b)
    fb = p.ev("()=>__UZ.fbtn()")
    lab = p.ev("()=>__UZ.label()")
    T(G, u'「거르기」 → 「필터」 · 고르개 = 단추(네이티브 select 아님)', bool(fb and fb['kind'] == 'btn' and lab == u'필터'), {'단추': fb and fb.get('t'), '글자': lab})
    T(G + '-헛', u'헛잣대 바탕 — select · 「거르기」', (b.ev("()=>__UZ.fbtn()") or {}).get('kind') == 'select' and b.ev("()=>__UZ.label()") == u'거르기', b.ev("()=>__UZ.label()"))
    for how in ('mouse', 'touch'):
        home(p)
        p.press(p.ev("()=>__UZ.fbtn()"), how, 500)
        m0 = p.ev("()=>__UZ.fmenu()")
        p.press(p.ev("()=>__UZ.fopt('jo')"), how, 1200)
        m1 = p.ev("()=>__UZ.fmenu()")
        p.press(p.ev("()=>__UZ.fbtn()"), how, 500)
        m2 = p.ev("()=>__UZ.fmenu()")
        p.press(p.ev("()=>__UZ.fbk('주체')"), how, 1500)
        m3 = p.ev("()=>__UZ.fmenu()")
        r23 = p.ev("()=>__UZ.rowTot('2.3 기일기간-절차수행')")
        p.press(p.ev("()=>__UZ.fbk('기간')"), how, 1500)
        btn = (p.ev("()=>__UZ.fbtn()") or {}).get('t')
        tot2 = p.ev("()=>{let n=0;document.querySelectorAll('#slot .mbdash > .mbsj').forEach(c=>{if(c.querySelector('.mbur[data-giy]')||/미분류/.test((c.querySelector(':scope > .hd h2')||{}).textContent||''))return;const t=c.querySelector(':scope > .hd .tot');const m=t&&/총 (\\d+)/.exec(t.textContent);if(m)n+=+m[1]});return n}")   # 「변리사 기출」 카드(문항 수)는 뺀다
        T(G, u'필터 단추 누름(%s) → 목록(유형 다섯 · 점선) · 조문형 고르면 닫힘 · 다시 열면 점선 아래 내용·주체·기간(색 = BK_COLOR) · 조문형 아니면 안내 한 줄' % how,
          bool(m0 and m0['vis'] and len(m0['opts']) == 5 and m0['sep'] and not m0['bk'] and m0['note'] and m1 is None and m2 and len(m2['bk']) == 3 and all(x['vis'] for x in m2['bk'])),
          {'처음': m0, '고른 뒤': m1, '다시': m2 and m2['bk']})
        T(G, u'「주체」 켬(%s) → 2.3 기일기간 셈 = OMR 표시 주체 두 줄(TH000128·TH000131) · 목록 열린 채 · 「+기간」 → 단추 「조문형 · 주체·기간 ▾」 · 머리 합 14' % how,
          bool(r23 and r23['tot'] == 2 and m3 and m3['vis'] and btn == u'조문형 · 주체·기간 ▾' and tot2 == 14), {'2.3': r23, '열린 채': bool(m3), '단추': btn, '편 머리 합': tot2})
        # 체크 끄기 · 조문형만 · 기타(1.1 목적 12 줄 = 제7판)
        p.press(p.ev("()=>__UZ.fbk('주체')"), how, 1200); p.press(p.ev("()=>__UZ.fbk('기간')"), how, 1200)
        p.pg.mouse.click(5, 5); p.pg.wait_for_timeout(300)
        p.ev("()=>__UZ.gk('x')")
        r11 = p.ev("()=>__UZ.rowTot('1.1 목적')")
        dw = p.ev("()=>__UZ.drawerLeaf('1.1 목적')")
        jn = None
        if r11 and r11['jn']:
            p.press(p.ev("()=>__UZ.rowAt('1.1 목적','.mbchip.jn')"), how, 1200)
            jn = p.ev("()=>__UZ.jn()"); p.ev("()=>__HM.closeAll()")
        p.press(p.ev("()=>__UZ.fbtn()"), how, 500)
        p.press(p.ev("()=>__UZ.fopt('all')"), how, 1200)
        r11a = p.ev("()=>__UZ.rowTot('1.1 목적')")
        T(G, u'조문형만(%s · 기타) → 1.1 목적 셈 = 서랍 = 📋 행 · 부제 「거름 조문형」 · 「전체」 → 12' % how,
          bool(r11 and dw and jn and r11['tot'] == int(dw['n']) == jn['rows'] and u'거름 조문형' in jn['sub'] and r11a and r11a['tot'] == 12),
          {'1.1 셈': r11 and r11['tot'], '서랍': dw, '📋': jn and [jn['rows'], jn['sub']], '전체': r11a})
        p.ev("()=>{S.oxFilter='all';S.oxBk=[];}")
    # 헛잣대 — 바탕 다섯 값 모두 12
    vals = []
    for v in ('all', 'jo', 'pan', 'mix', 'untype'):
        b.ev("v=>{S.oxFilter=v}", v); b.ev("()=>render()"); b.pg.wait_for_timeout(700)
        vals.append((b.ev("()=>__UZ.rowTot('1.1 목적')") or {}).get('tot'))
    b.ev("()=>{S.oxFilter='all'}")
    T(G + '-헛', u'헛잣대 바탕 — 첫 화면 1.1 목적 다섯 값 모두 12(필터가 첫 화면에 안 걸림)', vals == [12] * 5, vals)
    home(p)


def g_a8b(p, b, eng):
    G = 'a3-8b'
    home(p); home(b)
    for how in ('mouse', 'touch'):
        a = p.ev("()=>__UZ.topArrow(1)")
        p.press(a, how, 1200)
        c1 = p.ev("()=>__UZ.cardBody(1)")
        dh = p.ev("()=>__UZ.drawerTopArrow('1. 특허제도')")
        p.press(p.ev("()=>__UZ.topArrow(1)"), how, 1200)
        c2 = p.ev("()=>__UZ.cardBody(1)")
        T(G, u'편 머리 ▾ 누름(%s) → 그 편 단원 줄 보임 0 · 서랍 같은 편 ▸ · 다시 누르면 폄' % how,
          bool(a and c1 and c1['rows'] == 0 and c1['arrow'] == u'▸' and dh == u'▸' and c2 and c2['rows'] > 0 and c2['arrow'] == u'▾'), {'▾': a and a.get('t'), '접힘': c1, '서랍': dh, '폄': c2})
    T(G + '-헛', u'헛잣대 바탕 — 편 머리 ▾ 없음', b.ev("()=>__UZ.topArrow(1)") is None, None)
    seq, st0 = [], p.ev("()=>__UZ.step()")
    vis_ = []
    for i in range(4):
        s = p.ev("()=>__UZ.step()")
        seq.append(s and s['t'])
        p.press(s, 'mouse' if i % 2 == 0 else 'touch', 1200)
        vis_.append({'편1': (p.ev("()=>__UZ.cardBody(1)") or {}).get('rows'), '편2': p.ev("()=>__UZ.depthVis(2)")})
    seq.append((p.ev("()=>__UZ.step()") or {}).get('t'))
    T(G, u'⚡ 줄 단계 글자 하나 — 누를 때마다 「접기1 → 접기2 → 접기3 → 펴기 → 접기1」 · 테·바탕 없음(11px · 700 · 회색)',
      bool(st0 and st0['n'] == 1 and seq == [u'접기1', u'접기2', u'접기3', u'펴기', u'접기1'] and st0['bs'] in ('none', 'hidden') or (st0 and st0['bw'] == '0px')) and st0['bg'] in ('rgba(0, 0, 0, 0)', 'transparent') and st0['fs'] == '11px' and st0['fw'] == '700',
      {'글자': seq, '꼴': st0 and {k: st0[k] for k in ('bw', 'bs', 'bg', 'fs', 'fw', 'color')}})
    T(G, u'첫 누름 → 편 카드 몸 0 · 둘째 → 깊이 3↑ 보임 0 · 깊이 2 보임 · 넷째(펴기) → 되돌림',
      bool(vis_[0]['편1'] == 0 and vis_[1]['편2']['d3'] == 0 and vis_[1]['편2']['d4'] == 0 and vis_[1]['편2']['d2'] > 0 and vis_[3]['편2']['d3'] > 0), vis_)
    T(G + '-헛', u'헛잣대 바탕 — 단계 글자 없음', b.ev("()=>__UZ.step()") is None, None)
    p.ev("()=>{S.mbCh={};S.jtCh={};}"); home(p)
    x11, x12, x221 = p.ev("()=>__UZ.nameX('1.1 목적')"), p.ev("()=>__UZ.nameX('1.2 국제조약')"), p.ev("()=>__UZ.nameX('2.2.1 주체 능력')")
    T(G, u'줄 정렬 — 1.1 목적 · 1.2 국제조약 이름 x 같음 · 2.2.1 = +14', bool(x11 is not None and x11 == x12 and x221 is not None and abs(x221 - x11 - 14) < 0.6), {'1.1': x11, '1.2': x12, '2.2.1': x221})
    bx11, bx12 = b.ev("()=>__UZ.nameX('1.1 목적')"), b.ev("()=>__UZ.nameX('1.2 국제조약')")
    T(G + '-헛', u'헛잣대 바탕 — 1.2 국제조약 이름이 22px 밀림', bool(bx11 is not None and bx12 is not None and abs(bx12 - bx11 - 22) < 1.5), {'1.1': bx11, '1.2': bx12})


BK_WANT = {'TH000128': ['주체'], 'TH000131': ['주체'], 'T1855025h': ['주체'], 'TH000144': ['주체'], 'TH000149': ['주체'], 'TH000152': ['주체'],
           'T1855062': ['주체'], 'T1350042': ['주체'], 'T185510ㅂ': ['기간'], 'T225914ㄴ': ['주체'], 'T225914ㄹ': ['주체'], 'T0946145': ['주체'],
           'T2057035': ['주체'], 'T2562154': ['주체']}


def d_a7():
    """§B-7 데이터 — bktype_omr.json = 표 14 · 다시 돌려도 같음 · 헛잣대 = 옛 omr_map 으로 맞대면 다름"""
    G = 'a3-7d'
    J = json.load(io.open(os.path.join(_DATA, 'bktype_omr.json'), encoding='utf-8'))
    T(G, u'bktype_omr.json = 9/27 사용자 확인 14(uid · 값) 그대로', J == BK_WANT, {'다름': {k: [J.get(k), v] for k, v in BK_WANT.items() if J.get(k) != v}, '더': [k for k in J if k not in BK_WANT]})
    env = dict(os.environ, JOPANGI_APPDATA=_DATA, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    code = ("import sys,json;sys.path.insert(0,r'%s');import _omr_bktype as OB;r,rep=OB.extract();"
            "print(json.dumps({'res':r,'marks':[[m['page'],list(m['rect']),m['uid'],m['val']] for m in rep['marks']]},ensure_ascii=False))") % os.path.dirname(HERE)
    out = subprocess.run([sys.executable, '-c', code], capture_output=True, env=env, timeout=900)
    try:
        X = json.loads(out.stdout.decode('utf-8').strip().splitlines()[-1])
    except Exception as e:
        X = {'res': None, 'marks': [], 'err': out.stderr.decode('utf-8', 'replace')[-400:]}
    T(G, u'다시 돌려도 같음(⚙ _omr_bktype 한 번 더 · 멱등)', X.get('res') == J, X.get('err', ''))
    OM = json.load(io.open(os.path.join(_DATA, 'omr', u'특허', 'omr_map.json'), encoding='utf-8'))['map']
    diff = []
    for pg, (x0, y0, x1, y1), uid, val in X.get('marks', []):
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        hit = [k for k, b in OM.items() if b['page'] == pg and b['y'] - 1 <= cy <= b['y'] + b['h'] + 1 and b['x'] - 10 <= cx <= b['x'] + b['w']]
        if hit != [uid]:
            diff.append((uid, hit[:2]))
    T(G + '-헛', u'헛잣대 — 옛 기계 표 omr_map.json 으로 같은 자리를 맞대면 14 중 다름(쓰지 않는 까닭)', len(diff) > 0, {'다름': len(diff), '보기': diff[:6]})


def g_a7(p, b, eng):
    G = 'a3-7'
    home(p); home(b)
    p.ev("()=>__UZ.bkLoad()")
    res = {}
    for k in ('TH000128', 'T185510ㅂ', 'T2562154', 'T2562153'):
        go_key(p, k)
        res[k] = (p.ev("k=>__UZ.chipRow(k)", k) or {}).get('bk')
    ok = (res.get('TH000128') or {}).get('t') == u'주체' and ' q' not in (res.get('TH000128') or {}).get('cls', ' q') and (res.get('T185510ㅂ') or {}).get('t') == u'기간' \
        and (res.get('T2562154') or {}).get('t') == u'주체' and (res.get('T2562153') or {}).get('t') == u'빈칸?'
    T(G, u'OMR 표시 값 — TH000128 「조문형 · 주체」(밑줄 없음) · T185510ㅂ 「기간」 · T2562154 만 「주체」(P7-1887 다른 선지 「빈칸?」)', ok, res)
    # T2663011 — 유형 칩 안 「조문형」 바로 오른쪽 글자 · 따로 칩 0 · 누름 → 창 · 내용·기간 켬
    for how in ('mouse', 'touch'):
        p.ev("()=>__UZ.lsPut('jopangi.bktype',{})")
        home(p)
        go_key(p, 'T2663011')
        row0 = p.ev("k=>__UZ.chipRow(k)", 'T2663011')
        p.press(p.ev("k=>__UZ.bkAt(k)", 'T2663011'), how, 800)
        pop = p.ev("()=>__HM.popKeys().find(x=>/빈칸 종류 확정/.test(x))")
        p.press(p.ev("v=>__UZ.bkPopBtn(v)", u'내용'), how, 900)
        p.press(p.ev("v=>__UZ.bkPopBtn(v)", u'기간'), how, 900)
        row1 = p.ev("k=>__UZ.chipRow(k)", 'T2663011')
        p.ev("()=>__HM.closeAll()")
        T(G, u'T2663011 — 「조문형」 오른쪽 글자 「빈칸?」(점선 · 초안 없음) · 누름(%s) → 「🏷 빈칸 종류 확정」 창 · 내용·기간 켬 → 「조문형·내용·기간·7의2」 밑줄 없음' % how,
          bool(row0 and row0['bk'] and row0['bk']['t'] == u'빈칸?' and row0['bk']['deco'] == 'dotted' and pop and row1 and row1['bk'] and row1['bk']['t'] == u'내용·기간' and ' q' not in row1['bk']['cls'] and row1['typeT'].startswith(u'조문형·내용·기간')),
          {'전': row0 and row0['bk'], '창': pop, '뒤': row1 and [row1['typeT'], row1['bk']]})
    rec = p.ev("k=>__UZ.bkRec(k)", 'T2663011')
    reload_keep(p)
    home(p); p.ev("()=>__UZ.bkLoad()")
    go_key(p, 'T2663011')
    row2 = p.ev("k=>__UZ.chipRow(k)", 'T2663011')
    T(G, u'새로고침 뒤 유지(기록 jopangi.bktype · SYNC_KEYS 에 · uid 옮기기 목록에)', bool(row2 and row2['bk'] and row2['bk']['t'] == u'내용·기간' and 'jopangi.bktype' in (p.ev("()=>__UZ.syncKeys()") or [])),
      {'기록': rec, '뒤': row2 and row2['bk'], 'SYNC': len(p.ev("()=>__UZ.syncKeys()") or [])})
    # 지우기 → 빈칸?
    p.press(p.ev("k=>__UZ.bkAt(k)", 'T2663011'), 'mouse', 800)
    p.press(p.ev("v=>__UZ.bkPopBtn(v)", u'지우기'), 'mouse', 900)
    row3 = p.ev("k=>__UZ.chipRow(k)", 'T2663011'); p.ev("()=>__HM.closeAll()")
    go_key(p, 'TH000128')
    p.press(p.ev("k=>__UZ.bkAt(k)", 'TH000128'), 'mouse', 800)
    p.press(p.ev("v=>__UZ.bkPopBtn(v)", u'지우기'), 'mouse', 900)
    row4 = p.ev("k=>__UZ.chipRow(k)", 'TH000128'); p.ev("()=>__HM.closeAll()")
    T(G, u'「지우기」 → 「빈칸?」 · OMR 표시 지문(TH000128)도 기록 빈 값이 덮어 「빈칸?」', bool(row3 and row3['bk']['t'] == u'빈칸?' and row4 and row4['bk']['t'] == u'빈칸?'), {'T2663011': row3 and row3['bk'], 'TH000128': row4 and row4['bk']})
    p.ev("()=>__UZ.lsPut('jopangi.bktype',{})")
    # 초안 0 — 찍기 전 모든 지문 = 「빈칸?」(OMR 표시 14 밖)
    home(p)
    cen = p.ev("""async()=>{const M=VJ.M;let n=0,bad=[];for(let i=0;i<Math.min(M.length,40);i++){for(const ln of ['b','u']){const ks=mlnKeys(M,i,ln,VJ.P7map,VJ.byId);if(!ks.length)continue;
      await __HM.go(mlnSel(i,ln));document.querySelectorAll('#slot .mbtype .seg.bk').forEach(b=>{n++;const k=b.dataset.bk;const want=(BKTOMR||{})[k];if(b.textContent!==(want?want.join('·'):'빈칸?'))bad.push([k,b.textContent]);});}}return {n,bad:bad.slice(0,6)}}""")
    T(G, u'찍기 전 모든 지문 = 「빈칸?」(초안 0 · OMR 표시 14 만 값) — 마디 40 줄 전수', bool(cen and cen['n'] > 100 and not cen['bad']), cen)
    T(G + '-헛', u'헛잣대 바탕 — 유형 칩 안 빈칸 종류 글자 없음', not b.ev("()=>document.querySelectorAll('.mbtype .seg.bk').length") and not b.ev("()=>__UZ.has('bkOf')"), None)
    home(p)


def g_a7s(p, b, eng):
    """§B-7 「다른 기기 흉내(원격 기록)로 옮겨짐」 — 원격 기록.json 에 jopangi.bktype 칸을 심고 동기화 → 이 기기 칩 · 헛잣대 = 바탕 앱(그 키를 모른다)"""
    G = 'a3-7'
    REC = subprocess.run(['git', '-C', _roots.spd(), 'show', 'origin/main:jopangi/기록.json'], capture_output=True).stdout.decode('utf-8')
    d = json.loads(REC)
    d['data']['jopangi.bktype'] = {'T2663011': {'v': [u'주체'], 'ts': '2026-09-27T05:00:00.000Z'}}
    d.setdefault('u', {})['jopangi.bktype|T2663011'] = int(time.time() * 1000)
    txt = json.dumps(d, ensure_ascii=False)
    (ns, nd, ne), (bs, bd, be) = envs()
    res = {}
    for who, env in (('NEW', (ns, nd, ne)), ('BASE', (bs, bd, be))):
        q = Pg(BR[eng], eng, 'bks' + who, env[0], env[1], env[2], remote=txt)
        try:
            home(q, gk='g')
            q.ev("()=>__HM.sync()")
            q.ev("()=>{try{recDropCache()}catch(e){}}")
            home(q, gk='g')
            go_key(q, 'T2663011')
            r = q.ev("k=>__UZ.chipRow(k)", 'T2663011') or {}
            res[who] = {'bk': r.get('bk'), '기록': q.ev("()=>__UZ.ls('jopangi.bktype')")}
        finally:
            q.close()
    T(G, u'다른 기기 흉내 — 원격 기록.json 의 jopangi.bktype(T2663011 주체) → 동기화 → 이 기기 칩 「조문형·주체」(밑줄 없음)', bool(res['NEW']['bk'] and res['NEW']['bk']['t'] == u'주체' and ' q' not in res['NEW']['bk']['cls']), res['NEW'])
    T(G + '-헛', u'헛잣대 바탕 — 그 키를 모른다(칩 안 글자 없음)', not res['BASE']['bk'], res['BASE'])


def g_a1(p, b, eng):
    G = 'a3-1'
    home(p); home(b)
    for who, q in (('NEW', p), ('BASE', b)):
        q.ev("()=>__UZ.seedGi('2026',{sub:'2026-09-03T04:42:00Z',n:10,right:0},(()=>{const o={};for(let i=21;i<=30;i++)o['특허:2026:'+i]={ok:false,g:1,ts:'2026-09-03T04:42:00Z'};return o})())")
        home(q)
    rn, rb = p.ev("()=>__UZ.grRow('2026')"), b.ev("()=>__UZ.grRow('2026')")
    T(G, u'원격 기록 흉내(gi.year 특허:2026 n10 right0 + gi 21~30 {ok:false,g:1}) → 2026 줄 회독 상자 0 · 「1회독」 단추', bool(rn and not rn['boxes'] and rn['go'] == u'1회독'), rn)
    T(G + '-헛', u'헛잣대 바탕 — 「1회독 0/10 X10」 상자 보임', bool(rb and rb['boxes'] and '0/10' in rb['boxes'][0]['t']), rb)
    # 회독 상자 = 단추 → 비교 창 · 기출뷰 안 열림(마우스·손가락)
    rec = [{'date': '2026-09-20', 'ts': '2026-09-20T01:00:00Z', 'ok': 16, 'n': 20, 'ms': 2280000, 'picks': {str(i): '1' for i in range(1, 21)}, 'st': {'cf': 2, 'fk': 1, 'x': 9, 'n': 98}}]
    for who, q in (('NEW', p), ('BASE', b)):
        q.ev("r=>__UZ.seedGround('2026',r)", rec); home(q)
    for how in ('mouse', 'touch'):
        home(p)
        at = p.ev("()=>__UZ.grBoxAt('2026',0)")
        p.press(at, how, 1000)
        cm, tab = p.ev("()=>__UZ.cmp()"), p.ev("()=>S.jimunTab")
        p.ev("()=>__HM.closeAll()")
        T(G, u'회독 상자 누름(%s) → 회독 비교 창 보임(문항 × 회독) · 기출뷰 안 열림' % how, bool(at and at.get('tag') == 'BUTTON' and cm and cm['vis'] and cm['rounds'] == 1 and cm['chips'] >= 20 and tab == 'ox'), {'상자': at and at.get('tag'), '창': cm, '탭': tab})
    home(b)
    at = b.ev("()=>__UZ.grBoxAt('2026',0)")
    b.click(at, 1200)
    T(G + '-헛', u'헛잣대 바탕 — 상자 누름 → 기출뷰가 열림(줄 누름으로 샘)', b.ev("()=>S.jimunTab") == 'gichul', b.ev("()=>S.jimunTab"))
    b.ev("()=>{S.jimunTab='ox'}")
    # 아랫줄 = 제출 때 스냅숏(스냅숏 있는 회독 · 그 뒤 지문 X 를 바꿔도 무변) · 옛 회독(스냅숏 없음) = 비움
    home(p)
    r1 = p.ev("()=>__UZ.grRow('2026')")
    k0 = p.ev("()=>{const q=(VJ.qs||[]).find(q=>String(q.연도)==='2026');return q?oxKeyLid(q,q.지문[0]):null}")
    p.ev("k=>{const A=oxAll();A[k]=Object.assign({},A[k]||{},{p:'O',ok:false,ts:nowIso(),uv:1});OXREC=A;lsWrite(OX_KEY,A,'하네스')}", k0)
    home(p)
    r2 = p.ev("()=>__UZ.grRow('2026')")
    p.ev("r=>__UZ.seedGround('2026',r)", [dict(rec[0], st=None)]); home(p)
    r3 = p.ev("()=>__UZ.grRow('2026')")
    T(G, u'아랫줄 = 제출 때 스냅숏 「🌀2 ⚠1 X9 /98」 · 그 뒤 지문 X 를 바꿔도 무변 · 스냅숏 없는 옛 회독 = 아랫줄 비움',
      bool(r1 and r1['boxes'] and r1['boxes'][0]['l2'][1:] == [u'🌀2 ⚠1 X9 /98'] and r2['boxes'][0]['l2'] == r1['boxes'][0]['l2'] and r3 and len(r3['boxes'][0]['l2']) == 1),
      {'처음': r1 and r1['boxes'], '지문 X 뒤': r2 and r2['boxes'], '옛 회독': r3 and r3['boxes']})
    p.ev("k=>{const A=oxAll();delete A[k];OXREC=A;lsWrite(OX_KEY,A,'하네스')}", k0)
    for q in (p, b):
        q.ev("()=>{const G=giAll();Object.keys(G).filter(k=>k.indexOf('특허:2026:')===0).forEach(k=>delete G[k]);GIREC=G;lsWrite(GI_KEY,G,'하네스');const Y=giYAll();delete Y['특허:2026'];GIYREC=Y;lsWrite(GIY_KEY,Y,'하네스');const A=grndAll();delete A['특허:2026'];GRNDREC=A;lsWrite(GRND_KEY,A,'하네스');}")


def g_a2(p, b, eng):
    G = 'a3-2'
    for how in ('mouse', 'touch'):
        home(p)
        p.press(p.ev("()=>__UZ.rowAt ? __HM.at('#slot .mbur[data-giy=\"2026\"] .nm') : null"), how, 2500)
        p.until("()=>document.querySelectorAll('#slot .exv-q').length>0", ms=15000)
        e = p.ev("()=>__UZ.exv()")
        dy = p.ev("()=>__UZ.drawerYears()")
        q1 = (e['qs'] or [{}])[0]
        at = p.ev("()=>__UZ.exvNum('1',1)")
        p.press(at, how, 600)
        s1 = p.ev("()=>__UZ.exvNumState('1',1)")
        p.until("()=>{const q=document.querySelector('#slot .exv-q[data-exno=\"5\"] .exv-sel');return q&&/③/.test(q.textContent)}", ms=20000)
        e5 = p.ev("()=>__UZ.exv()")
        s5 = next((q['sel'] for q in e5['qs'] if q['no'] == '5'), '')
        p.press(p.ev("()=>__UZ.exvNext()"), how, 1500)
        e6 = p.ev("()=>__UZ.exv()")
        T(G, u'2026 특허 열기(%s) → 서랍 첫 줄 「2026년 제63회」 · 머리 「1~5번 / 총 20문제」 · 모드바 0 · 1번 머리 「1.」 굵게(15px 800) · 지문 칸 5 · 칩 줄 보임 · ⭐ 0 · ① 누름 → 고름(바탕 파랑) · 5번 「③ ㄱ, ㄷ, ㄹ」 · 「다음 5문제 ▶」 → 6번' % how,
          bool(dy and dy[0]['t'] == u'2026년 제63회' and dy[0]['now'] and u'1~5번 / 총 20문제' in e['head'] and e['modebar'] == 0 and q1.get('head', '').startswith('1.') and (q1.get('noStyle') or {}).get('fontWeight') == '800'
               and q1.get('boxes') == 5 and q1.get('chipRows') == 5 and sum(q['stars'] for q in e['qs']) == 0 and s1 and s1['sel'] and s1['bg'] == 'rgb(29, 78, 216)' and u'③ㄱ, ㄷ, ㄹ' in s5.replace(' ', ' ')
               and e6['qs'] and e6['qs'][0]['no'] == '6'),
          {'서랍': dy[:2], '머리': e['head'], '모드바': e['modebar'], '1번': q1, '①': s1, '5번': s5, '다음': e6['qs'][0]['no'] if e6['qs'] else None, '알약': e['pill']})
        p.ev("()=>{const G=giAll();Object.keys(G).filter(k=>k.indexOf('특허:2026:')===0).forEach(k=>delete G[k]);GIREC=G;lsWrite(GI_KEY,G,'하네스');S.exvPg={};}")
    home(b)
    b.ev("()=>__HM.gi('2026')")
    eb = b.ev("()=>__UZ.exv()")
    T(G + '-헛', u'헛잣대 바탕 — 모드바 있음 · 옛 선지 상자(gich·ginum)', eb['modebar'] > 0 and eb['oldBoxes'] > 0, {'모드바': eb['modebar'], '옛 상자': eb['oldBoxes']})
    home(b)


def g_a3(p, b, eng, mb_ref):
    G = 'a3-3'
    home(p); home(b)
    for q in (p, b):
        if not go_key(q, 'T2663011'):
            q.ev("s=>__HM.go(s)", '__미분류')
    n, o = p.ev("k=>__UZ.chipRow(k)", 'T2663011'), b.ev("k=>__UZ.chipRow(k)", 'T2663011')
    keys = ['fontSize', 'fontWeight', 'color', 'backgroundColor', 'borderTopColor', 'borderTopStyle', 'borderTopWidth', 'paddingTop', 'paddingLeft', 'borderTopLeftRadius', 'h']
    same = lambda a, r: {k: (a or {}).get(k) for k in keys if (a or {}).get(k) != (r or {}).get(k)}
    dt, dy, dm = same(n and n['type'], mb_ref['typeJo']), same(n and n['year'], mb_ref['year']), same(n and n['mc'], mb_ref['mc'])
    T(G, u'T2663011 유형·출제연도·🃏 칩 computed = 민법 Q0275(글자 크기·굵기·색·바탕·테·여백·높이 · 유형 색은 같은 유형끼리)', bool(n and not dt and not dy and not dm), {'유형 다름': dt, '연도 다름': dy, '🃏 다름': dm, '민법': mb_ref.get('_src')})
    T(G, u'출처 칩·ID 칩 = 바탕 판과 같음(무변) · 글 「26 변리」·「T2663011」·「조문형·빈칸?·7의2」', bool(n and o and n['src'] == o['src'] and n['id'] == o['id'] and n['srcT'] == u'26 변리' and n['idT'] == 'T2663011' and n['typeT'].startswith(u'조문형') and u'7의2' in n['typeT']),
      {'출처': [n and n['src'], o and o['src']], '글': [n and n['srcT'], n and n['typeT']]})
    T(G + '-헛', u'헛잣대 바탕 — 유형·연도·🃏 칩이 민법과 다름', bool(o and (same(o['type'], mb_ref['typeJo']) or same(o['year'], mb_ref['year']) or same(o['mc'], mb_ref['mc']))),
      {'유형': same(o and o['type'], mb_ref['typeJo']), '연도': same(o and o['year'], mb_ref['year']), '🃏': same(o and o['mc'], mb_ref['mc'])})


def g_a45(p, b, eng):
    G = 'a3-4'
    home(p, gk='x'); home(b)
    for how in ('mouse', 'touch'):
        home(p, gk='x')
        p.press(p.ev("()=>__UZ.rowAt('1.1 목적','.mbchip.jn')"), how, 1500)
        w, r0 = p.ev("()=>__UZ.jn()"), p.ev("()=>__UZ.jnFirstRow()")
        order = [k['c'].split(' ')[0] for k in (r0 or {}).get('kids', [])]
        T(G, u'1.1 목적 📋(%s · 기타) → 창 600×720 · 첫 줄 = 「TJ0100001 · 1번 · 01 사법 … 기록 없음(오른쪽 끝)」 · ✏️ 표시 켜짐 = 주황' % how,
          bool(w and w['w'] == 600 and w['h'] == 720 and r0 and order[:3] == ['qb', 'jnno', 'jnsrc'] and r0['kids'][0]['t'] == 'TJ0100001' and r0['kids'][1]['t'] == u'1번' and r0['kids'][2]['t'] == u'01 사법'
               and r0['recText'] == u'기록 없음' and r0['recRight'] == 0 and (w['tg'] or {}).get('color') == 'rgb(146, 64, 14)' and (w['tg'] or {}).get('backgroundColor') == 'rgb(255, 251, 235)'),
          {'창': w and [w['w'], w['h'], w['sub']], '첫 줄': r0 and r0['kids'], '기록 칸 오른쪽 끝': r0 and r0['recRight'], '✏️': w and w['tg']})
        s1, s2, s3 = p.ev("k=>__UZ.jnStem('정리',k)", 'TJ0100001'), p.ev("k=>__UZ.jnStem('정리',k)", 'TJ0100002'), p.ev("k=>__UZ.jnStem('정리',k)", 'TJ150003ㄱ')
        oxs = p.ev("()=>{const p=POPS.filter(x=>/정리/.test(x._pk||'')).pop();return p?[...p.querySelectorAll('.jnr')].map(r=>{const pr=r.previousElementSibling;return [r.dataset.jnrow,!!(pr&&pr.classList.contains('jnstem'))]}):null}")
        noStem = [k for k, st in (oxs or []) if not st and not re.match(r'TJ0100\d+|TJ150003', k)]
        T('a3-5', u'발문 줄(%s) — 첫 줄 「1번 · 우리나라 특허법의 기본원칙이 아닌 것은?」 · 그 아래 TJ0100001~05(발문 줄 한 번) · TJ150003ㄱ 앞 「4번 · …모두 고른 것은?」 · 발문 없는 줄 앞엔 없음 · 꼴 = 민법 「문제 N」 줄' % how,
          bool(s1 and s1['stem'] and s1['stem'].startswith(u'1번') and u'기본원칙이 아닌 것은?' in s1['stem'] and s1['vis'] and s2 and s2['stem'] is None and s3 and s3['stem'] and s3['stem'].startswith(u'4번') and u'모두 고른 것은?' in s3['stem']
               and (s1['style'] or {}).get('fontWeight') == '900' and (s1['style'] or {}).get('color') == 'rgb(55, 48, 163)'),
          {'TJ0100001': s1, 'TJ0100002': s2 and s2['stem'], 'TJ150003ㄱ': s3 and s3['stem'], '발문 없는 줄': noStem[:4]})
        p.ev("()=>__HM.closeAll()")
    home(b)
    b.click(b.ev("()=>__UZ.rowAt('1.1 목적','.mbchip.jn')"), 1500)
    wb, rb0 = b.ev("()=>__UZ.jn()"), b.ev("()=>__UZ.jnFirstRow()")
    T(G + '-헛', u'헛잣대 바탕 — 첫 줄 「제7판 p.2」 · 창 440 폭 · 발문 줄 0', bool(wb and wb['w'] == 440 and rb0 and rb0['kids'][0]['t'].startswith(u'제7판 p.') and not any(k['c'] == 'jnstem' for k in wb['kids'])),
      {'창': wb and [wb['w'], wb['h']], '첫 줄': rb0 and rb0['kids'][:3]})
    b.ev("()=>__HM.closeAll()")
    home(p)


# ══════════ mbsame_add2 §C ══════════
def g_c1(p, b, eng):
    G = 'a2-1'
    home(p, gk='x')
    go_key(p, 'TH181394ㄴ')
    card = p.ev("()=>{const c=document.getElementById('qb-TH181394ㄴ');if(!c)return null;const bx=c.closest('.p7case');return {vis:!!c&&c.getBoundingClientRect().height>0,box:bx?bx.textContent.slice(0,40):null}}")
    pk = p.ev("()=>{const c=document.getElementById('qb-TH181394ㄴ');const b=c&&c.querySelector('.mbpeek');if(!b)return null;b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();const at=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return {cx:r.left+r.width/2,cy:r.top+r.height/2,on:!!at&&(at===b||b.contains(at))}}")
    p.click(pk, 500)
    ans = p.ev("()=>{const c=document.getElementById('qb-TH181394ㄴ');const e=c&&c.querySelector('.mbexp');return e&&getComputedStyle(e).display!=='none'?e.textContent.slice(0,60):null}")
    P7d = json.load(io.open(os.path.join(_DATA, 'jimun_7pan.json'), encoding='utf-8'))
    ob = next(({u'답': o.get(u'답')} for o in P7d[u'객관식'] if o['id'] == 'P7-1394'), {})   # 쪼갠 문항은 MLN.obj 에 없다 — 데이터 값
    z0069 = [p.ev("id=>__UZ.p7(id)", 'P7-0069-' + c) for c in u'ㄱㄴㄷㄹㅁㅂ']
    p.ev("()=>__UZ.gk('g')")   # P7-1394 = 18 변리 2차(기타) · P7-0069 = 02 변리(기출)
    cards = []
    for c in u'ㄱㄴㄷㄹㅁㅂ':   # 쪽(20 카드)을 넘을 수 있어 줄마다 그 쪽으로
        go_key(p, 'TH020069' + c)
        cards.append(p.ev("k=>{const e=document.getElementById('qb-'+k);return e?e.getBoundingClientRect().height>0:false}", 'TH020069' + c))
    T(G, u'P7-1394 답 ⑤(데이터) · ㄴ 카드 「정답·해설 ▸」(마우스) → 「ㄴ (O)」 해설 보임(빨간 추록) · P7-0069 여섯 줄 카드 보임 · 정오 ㄱO ㄴO ㄷX ㄹX ㅁO ㅂO',
      bool(card and card['vis'] and ans and (u'정답 O' in ans or ans.lstrip().startswith(u'ㄴ (O)')) and ob.get(u'답') == u'⑤' and all(cards) and ''.join((z or {}).get('ox', '?') for z in z0069) == 'OOXXOO'),
      {'ㄴ 카드': card, '해설 칸': ans, '객관식 답': ob, '0069 정오': ''.join((z or {}).get('ox', '?') for z in z0069), '0069 카드': cards})
    home(b)
    bP = json.load(io.open(os.path.join(M.base_env()[1], 'jimun_7pan.json'), encoding='utf-8'))
    bans = next((o.get(u'답') for o in bP[u'객관식'] if o['id'] == 'P7-1394'), None)
    T(G + '-헛', u'헛잣대 바탕 — P7-1394 답 ④ · ㄴ X · P7-0069 여섯 줄 없음', bans != u'⑤' and (b.ev("id=>__UZ.p7(id)", 'P7-1394-ㄴ') or {}).get('ox') == 'X' and not b.ev("id=>__UZ.p7(id)", 'P7-0069-ㄱ'),
      {'답': b.ev("id=>__UZ.obj(id)", 'P7-1394'), 'ㄴ': b.ev("id=>__UZ.p7(id)", 'P7-1394-ㄴ')})


def g_c2(p, b, eng):
    G = 'a2-2'
    for q in (p, b):
        home(q)
    r = p.ev("()=>{const rs=[...document.querySelectorAll('#slot .mbur')].filter(x=>/^12 실용신안/.test((x.querySelector('.nm')||{}).textContent||''));return rs.map(x=>({t:x.querySelector('.nm').textContent.trim(),tot:(/총 (\\d+)/.exec(x.textContent)||[])[1],vis:x.getBoundingClientRect().height>0}))}")
    u = [x for x in (r or []) if u'(미수록)' in x['t']]
    at = p.ev("()=>__UZ.rowAt('12 실용신안 (미수록)')")
    p.tap(at, 1500)
    mok = p.ev("()=>S.mok")
    rb = b.ev("()=>[...document.querySelectorAll('#slot .mbur')].filter(x=>/^12 실용신안/.test((x.querySelector('.nm')||{}).textContent||'')).map(x=>x.querySelector('.nm').textContent.trim())")
    T(G, u'첫 화면 「12 실용신안」 → (미수록) 15 줄 보임 · 손가락 톡 → 그 줄(~u) · 머리 셈 = 줄 넷 합', bool(u and u[0]['tot'] == '15' and u[0]['vis'] and mok and mok.endswith('~u')), {'줄': r, '톡': mok})
    T(G + '-헛', u'헛잣대 바탕 — (미수록) 줄 없음', not any(u'(미수록)' in x for x in (rb or [])), rb)


def g_c3(p, b, eng):
    G = 'a2-3'
    for q, who in ((p, 'NEW'), (b, 'BASE')):
        home(q); go_key(q, 'T1350065h')
    res = {}
    for q, who in ((p, 'NEW'), (b, 'BASE')):
        bb = q.ev("([k,r])=>__HM.btnIn(k,r)", ['T1350065h', u'^📖'])
        q.click(bb, 1200)
        pw = q.ev("()=>{const p=(POPS||[]).find(x=>/📝 지문 T1350065$/.test(x._pk||''));if(!p)return null;const h=(p.querySelector('.ph')||{}).textContent||'';const s=sidFind('T1350065');return {vis:p.getBoundingClientRect().height>0,head:h.slice(0,80),q:s&&s.q?s.q.id:null,unk:/미분류/.test(h)}}")
        res[who] = pw
        q.ev("()=>__HM.closeAll()")
    T(G, u'pdf 18 · 29번 T1350065h 「📖 원 기출」 → 리담 2013-50-18 ⑤ 팝업(찾은 문항 2013-50-18 · 제목 단원 = 붙은 마디 (미수록) · 미분류 아님)', bool(res['NEW'] and res['NEW']['vis'] and res['NEW']['q'] == '2013-50-18' and not res['NEW']['unk']), res['NEW'])
    T(G + '-헛', u'헛잣대 바탕 — 2004-41-15(미분류)가 뜬다', bool(res['BASE'] and (res['BASE']['q'] == '2004-41-15' or res['BASE']['unk'])), res['BASE'])


def g_c4(p, b, eng):
    G = 'a2-4'
    home(p); home(b)
    nb, bb = p.ev("q=>__UZ.boxOf(q)", '2023-60-18'), b.ev("q=>__UZ.boxOf(q)", '2023-60-18')
    cn, cb = p.ev("()=>__UZ.boxes()"), b.ev("()=>__UZ.boxes()")
    T(G, u'리담 2023-60-18(시험 13번) · T2360131 상자 아님(발문 끝 「(다툼이 있는 경우 판례에 의함)」 걷고 판정) · 상자 수 보고', nb is False and cb and cn['boxy'] < cb['boxy'], {'NEW': cn, '바탕': cb})
    T(G + '-헛', u'헛잣대 바탕 — 2023-60-18 상자', bb is True, bb)


def g_c56(p, b, eng, br):
    G = 'a2-5'
    (ns, nd, ne), (bs, bd, be) = envs()
    for W in (820, 390):
        for who, env in (('NEW', (ns, nd, ne)), ('BASE', (bs, bd, be))):
            q = Pg(br, eng, 'rec%d%s' % (W, who), env[0], env[1], env[2], W=W, H=900)
            try:
                home(q, gk='g')
                sel = go_key(q, 'T2057183')
                q.ev("([s,k,o,d])=>__HM.rndFake(s,k,o,d)", ['mok|특허|' + (sel or ''), 'T2057183', False, '2026-09-20'])
                go_key(q, 'T2057183')
                q.tap(q.ev("k=>__HM.stripOpen(k)", 'T2057183'), 700)
                q.tap(q.ev("([k,i])=>__HM.stripCellAt(k,i)", ['T2057183', 0]), 700)
                x = q.ev("k=>__HM.stripXAt(k)", 'T2057183')
                info = q.ev("k=>{const c=document.getElementById('qb-'+k);const i=c&&c.querySelector('.mbrecw .rgi');const t=i&&i.querySelector('.rgt');const last=c&&c.querySelector('.mbrecw .last');return i?{t:(i.textContent||'').trim(),color:getComputedStyle(t||i).color,lastColor:last?getComputedStyle(last).color:null}:null}", 'T2057183')
                ok1 = bool(x and x.get('on'))
                gone = None
                if ok1:
                    q.tap(x, 500); q.tap(q.ev("k=>__HM.stripXAt(k)", 'T2057183'), 900)
                    gone = q.ev("s=>__HM.rndOf(s)", 'mok|특허|' + (sel or ''))
                if who == 'NEW':
                    T(G, u'%dpx 손가락 · T2057183 기록 칸 톡 → 출처 「9/20 · 마디 번호+이름 · 1회독째」 · × 줄 안에 보임 · 두 번 톡 = 지움' % W,
                      bool(ok1 and info and re.match(r'^9/20 · \d', info['t']) and gone is not None and gone[-1]['all'] == 0), {'×': x, '출처': info, '지운 뒤': gone})
                    T('a2-6', u'%dpx — 날짜 「9/20」(앞 0 없음) · 출처 글 색 = 「마지막」 글 색' % W, bool(info and info['t'].startswith('9/20') and (info['lastColor'] is None or info['color'] == info['lastColor'])), info)
                else:
                    T(G + '-헛', u'%dpx 헛잣대 바탕 — × 가 줄 밖(안 보임) 또는 출처 글이 목차 경로 전체' % W, bool(not ok1 or (info and len(info['t']) > 40)), {'×': x, '출처': info})
            finally:
                q.close()


def g_c7(p, b, eng):
    G = 'a2-7'
    home(p); home(b)
    n = p.ev("()=>__UZ.band('특허법','2020',18,3)")
    o = b.ev("()=>__UZ.band('특허법','2020',18,3)")
    def inside(r):
        if not r or not r.get('band'):
            return True
        y4 = [y0 for m, y0, y1 in r['opts'] if m == u'④']
        return (r['band']['y1'] <= y4[0] + 0.001) if y4 else (r['band']['y1'] - r['band']['y0'] <= 0.08)   # ④ 를 못 잡으면 띠 높이(선지 하나 ≤ 0.08)
    T(G, u'2020 18번 ③ 띠 = ③ 선지만(④ 줄 위에서 끝) 또는 띠 없음', inside(n), n)
    T(G + '-헛', u'헛잣대 바탕 — ③ 띠가 ④·⑤·쪽 꼬리까지 덮음', not inside(o), o)
    tot = {'NEW': [0, 0], 'BASE': [0, 0]}
    per = {}
    for y in ('2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026'):
        for who, q in (('NEW', p), ('BASE', b)):
            truth = q.ev("""async y=>{const rec=await jxeIndex(JXE_LAWF['특허법'],jxeFile('특허법',y));const out={};Object.keys(rec.no).forEach(n=>{const h=rec.no[n],L=rec.lines,end=h.nx>=0?h.nx:L.length;let cont=false;
              for(let i=h.i;i<end;i++){const l=L[i];if(l.p>h.p&&!(l.t.replace(/\\s/g,'').length<=8&&(l.y0>0.93||l.y0<0.07)))cont=true;}out[n]=cont;});return out}""", y)
            cuts = q.ev("y=>__UZ.cutAll('특허법',y)", y) or {}
            fp = [k for k, v in cuts.items() if v['cut'] and not truth.get(k)]
            tot[who][0] += len(fp); tot[who][1] += len([k for k, v in cuts.items() if truth.get(k) and not v['cut']])
            per.setdefault(y, {})[who] = len(fp)
    T(G, u'「다음 쪽에 이어짐」 거짓 0(2019~2026 특허 · 참 = 그 문항 글줄이 다음 쪽까지 감)', tot['NEW'][0] == 0, {'해마다 거짓': per, '놓침': tot['NEW'][1]})
    T(G + '-헛', u'헛잣대 바탕 — 거짓 이어짐 있음', tot['BASE'][0] > 0, tot['BASE'])


def g_c9(p, b, eng):
    G = 'a2-9'
    for who, q in (('NEW', p), ('BASE', b)):
        home(q, gk='g'); go_key(q, 'TH0211521')
        q.ev("()=>__UZ.toastClear()")
        at = q.ev("k=>__HM.chipAt(k,'^2002')", 'TH0211521')
        q.click(at, 1200)
        ts = q.ev("()=>__UZ.toasts()")
        pops = q.ev("()=>__HM.popKeys()")
        q.ev("()=>__HM.closeAll()")
        if who == 'NEW':
            T(G, u'TH0211521 「2002:?:①」 칩 누름 → 토스트 0(그 해 리담에 같은 글 없음 · 칩 흐림 · 무반응)', bool(at and not [t for t in ts if u'시험지' in t]), {'칩': at and at.get('t'), '토스트': ts, '창': pops})
        else:
            T(G + '-헛', u'헛잣대 바탕 — 「그 해 시험지가 없습니다」 토스트', any(u'시험지가 없' in t for t in ts), ts)


def g_c10(p, b, eng):
    G = 'a2-10'
    home(p)
    sel = go_key(p, 'T2057183')
    sc = 'mok|특허|' + (sel or '')
    p.ev("([s,k,o,d])=>__HM.rndFake(s,k,o,d)", [sc, 'T2057183', True, '2026-09-10'])
    p.ev("([s,k,o,d])=>__HM.rndFake(s,k,o,d)", [sc, 'T2057183', False, '2026-09-20'])
    p.ev("k=>{const A=oxAll();A[k]=Object.assign({},A[k]||{},{p:'O',ok:true,ts:nowIso(),uv:1});OXREC=A;lsWrite(OX_KEY,A,'하네스')}", 'T2057183')
    go_key(p, 'T2057183')
    before = p.ev("k=>__HM.oxRec(k)", 'T2057183')
    p.click(p.ev("k=>__HM.stripOpen(k)", 'T2057183'), 600)
    p.click(p.ev("([k,i])=>__HM.stripCellAt(k,i)", ['T2057183', 1]), 600)
    x = p.ev("k=>__HM.stripXAt(k)", 'T2057183'); p.click(x, 400); p.click(p.ev("k=>__HM.stripXAt(k)", 'T2057183'), 900)
    after_hist = p.ev("k=>__HM.oxRec(k)", 'T2057183')
    rn = p.ev("s=>__HM.rndOf(s)", sc)
    go_key(p, 'T2057183'); p.click(p.ev("k=>__HM.stripOpen(k)", 'T2057183'), 600)
    cells = p.ev("k=>__HM.stripCells(k)", 'T2057183')
    p.click(p.ev("([k,i])=>__HM.stripCellAt(k,i)", ['T2057183', len((cells or {}).get('cells', [])) - 1]), 600)
    x2 = p.ev("k=>__HM.stripXAt(k)", 'T2057183'); p.click(x2, 400); p.click(p.ev("k=>__HM.stripXAt(k)", 'T2057183'), 900)
    after_cur = p.ev("k=>__HM.oxRec(k)", 'T2057183')
    sw1, sw2 = p.ev("()=>__HM.sweep()"), p.ev("()=>__HM.sweep()")
    T(G, u'× 지움 — 회독 칸(9/20 X)을 지워도 지금 판 기록(O) 무변 · 지금 칸을 지우면 지금 판 기록만 빔(마감한 회독 결과로 되살리지 않음 · 조판기 회독 규칙 · 「다르게 한 것」) · 쓸기 멱등',
      bool(before and before.get('p') == 'O' and after_hist and after_hist.get('p') == 'O' and rn and rn[-1]['all'] == 0 and after_cur is not None and not after_cur.get('p') and sw2 == 0),
      {'전': before and before.get('p'), '회독 칸 지운 뒤': after_hist and after_hist.get('p'), '회독': rn, '지금 칸 지운 뒤': after_cur, '쓸기': [sw1, sw2]})
    home(p)


def g_c11(p, b, eng, mb_ref):
    G = 'a2-11'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        home(q, gk='g'); go_key(q, 'T2663011')
        q.ev("()=>{S.popCfg=S.popCfg||{};delete S.popCfg.bookpg;delete S.popCfg.canvas}")
        at = q.ev("k=>__HM.chipAt(k,'^2026')", 'T2663011')
        cs0 = q.ev("k=>{const idc=[...document.querySelectorAll('.qb.id')].find(b=>b.textContent.trim()===k);const hd=idc&&(idc.closest('.mbqhd')||idc.closest('.qhd'));const c=hd&&hd.querySelector('.jxec');if(!c)return null;const s=getComputedStyle(c);return {pt:s.paddingTop,pl:s.paddingLeft,h:Math.round(c.getBoundingClientRect().height*10)/10}}", 'T2663011')
        if not at:
            at = q.ev("k=>{const idc=[...document.querySelectorAll('.qb.id')].find(b=>b.textContent.trim()===k);const hd=idc&&(idc.closest('.mbqhd')||idc.closest('.qhd'));const c=hd&&hd.querySelector('.jxec');if(!c)return null;c.scrollIntoView({block:'center'});const r=c.getBoundingClientRect();const e=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return {cx:r.left+r.width/2,cy:r.top+r.height/2,on:!!e&&(e===c||c.contains(e)),t:c.textContent}}", 'T2663011')
        q.click(at, 2500)
        w = q.ev("()=>{const p=(POPS||[]).find(x=>/📄/.test((x.querySelector('.ph')||{}).textContent||''));if(!p)return null;const hd=p.querySelector(':scope > .ph');return {w:Math.round(p.getBoundingClientRect().width),navInHead:!!(hd&&hd.querySelector('.jxe-nav')),navBody:!!p.querySelector('.pb .jxe-nav, .jxe-nav:not(.ph .jxe-nav)')}}")
        res[who] = {'칩': cs0, '창': w}
        q.ev("()=>__HM.closeAll()")
    n = res['NEW']
    T(G, u'시험지 창 = 민법(폭 560 · ◀ ▶ 창 머리) · 출제연도 칩 여백 2px 8px = 민법 실물(Q0275)',
      bool(n['창'] and n['창']['w'] == 560 and n['창']['navInHead'] and n['칩'] and n['칩']['pt'] == mb_ref['year']['paddingTop'] and n['칩']['pl'] == mb_ref['year']['paddingLeft']), n)
    o = res['BASE']
    T(G + '-헛', u'헛잣대 바탕 — 폭 440 · ◀ ▶ 본문 위 · 칩 여백 1px 7px', bool(o['창'] and o['창']['w'] == 440 and not o['창']['navInHead'] and o['칩'] and o['칩']['pl'] == '7px'), o)


def g_c12(p, b, eng):
    G = 'a2-12'
    for who, q in (('NEW', p), ('BASE', b)):
        home(q, gk='x')
        i = q.ev("()=>__HM.nodeByTitle('^목적$')")
        q.ev("s=>__HM.go(s)", '__mg%d' % i)
        u = q.ev("()=>{const cs=[...document.querySelectorAll('#slot .qwrap')];const nos=new Set(cs.map(c=>(c.querySelector('.mlnbk, .oxseq')||{}).textContent||'').map(t=>(/^(\\d+)/.exec(t.trim())||[])[1]).filter(Boolean));return {n:cs.length,nos:[...nos],p0000:!!document.getElementById('qb-TJ0100001')}}")
        j = q.ev("()=>__HM.nodeByTitle('^실용신안$')")
        q.ev("s=>__HM.go(s)", '__mg%d' % j)
        pg2 = q.ev("()=>(OXDOMPG||{})['qb-TJ0920121']")
        if pg2:
            q.ev("n=>__HM.page(n)", pg2)
        u['p2012'] = q.ev("()=>{const c=document.getElementById('qb-TJ0920121');return !!c&&c.getBoundingClientRect().height>0}")
        if who == 'NEW':
            T(G, u'uid add1 §E-4 — 1.1 목적(기타) 카드 4 문항 · P7-0000 카드 · P7-2012(12 실용신안 · pdf 565 · 기타) 카드 보임', bool(u and len(u['nos']) == 4 and u['p0000'] and u['p2012']), u)
        else:
            N(G + '-헛', u'바로 앞 인도판(539131a) 수 보고 — 지시서 헛잣대 17094a5 = 2 문항', u)


# ══════════ uid_add2 §E ══════════
SEP = '\u001f'
PIT_OLD = 'q|T0845101' + SEP + '' + SEP + '0' + SEP + u'A회사의'


def d_u():
    """§E-3·4·5·7 데이터"""
    G = 'u-d'
    A = json.load(io.open(os.path.join(_DATA, 'uid_alias.json'), encoding='utf-8'))
    keys = set()
    for f in (u'jimun_특허.json', u'jimun_상표.json', u'jimun_디보.json'):
        J = json.load(io.open(os.path.join(_DATA, f), encoding='utf-8'))
        for q in J[u'문제']:
            for z in q.get(u'지문') or []:
                if z.get('uid'):
                    keys.add(z['uid'])
    P = json.load(io.open(os.path.join(_DATA, 'jimun_7pan.json'), encoding='utf-8'))
    for z in P[u'지문'] + P.get(u'객관식', []):
        if z.get('uid'):
            keys.add(z['uid'])
    tg = [v for v in A['map'].values() if v] + list(A['split'].values()) + [x for L in (A.get('multi') or {}).values() for x in L]
    orph = sorted({v for v in tg if v not in keys})
    nul = sorted(k for k, v in A['map'].items() if v is None)
    T(G, u'별칭표 가장자리 — 고아 목표 0(P7:P7-2058 → %s) · 걷은 조합 옛 uid 10 = map 빈 값(uidIsOrphan)' % A['map'].get('P7:P7-2058'), not orph and len(nul) == 10 and A['map'].get('P7:P7-2058') in keys,
      {'고아 목표': orph[:6], '빈 값': nul, 'multi': len(A.get('multi') or {}), 'split': len(A['split']), 'map': len(A['map'])})
    B = json.load(io.open(os.path.join(_DATA, u'jimun_특허.json'), encoding='utf-8'))
    ids = {q['id']: q for q in B[u'문제']}
    want = ['1998-35-5', '2016-53-B3', '2016-53-B4', '2016-53-B11', '2018-55-B4', '--0506']
    have = [k for k in want if k in ids]
    rows = sum(len(ids[k][u'지문']) for k in have)
    us = [z['uid'] for k in have for z in ids[k][u'지문']]
    allu = [z['uid'] for q in B[u'문제'] for z in q[u'지문'] if z.get('uid')]
    bad = [u for u in us if not re.match(r'^(T\d{7}[a-zㄱ-ㅎ㉠-㉯]?[hr]?\d?|T\d{6}[ㄱ-ㅎ][hr]?\d?|TR\d{4,5}[1-5ㄱ-ㅎ][a-z]?|TRU\d{4}[ㄱ-ㅎ1-5]|TH\d+[ㄱ-ㅎ]?|TJ\d+[ㄱ-ㅎ]?|TX\d+)$', u)]
    T(G, u'새 문항(지시서 9 중 넣은 것) — 1998-35-5(PM-0311) · 2016 3·4·11 · 2018 4 · PM-0506(연도 모름 TRU) · 선지 행 · uid 꼴 · 한 파일 안 유일',
      len(have) == 6 and rows == 28 and not bad and len(us) == len(set(us)), {'문항': have, '선지 행': rows, 'uid 꼴 밖': bad, '겹침': len(us) - len(set(us))})
    N(G, u'넣지 않은 것 — PM-1107(2000-37-1 · 선지 차례 모름) · PM-1103(2016 11번 기출변형 · 리담 선지 둘) → 크롬 GET 지시문(보고) · 2016 13번 = 이미 2016-53-4(시험문번 13)', '')
    T7 = P[u'지문']
    tail = [z['id'] for z in T7 if re.search(u'-\\s*\\d{3}\\s*-\\s*◈', z.get('t') or '')]
    z52 = next((z for z in T7 if z['id'] == 'P7-2052'), {})
    T('u-5', u'쪽 머리글 — 모아보기 쪽 번호 꼴(「- 563 -◈」) 0 · P7-2052 글 끝 「미기출 판례 모아보기」 없음', not tail and u'모아보기' not in (z52.get('t') or '')[-40:], {'남음': tail[:5], 'P7-2052 끝': (z52.get('t') or '')[-50:]})


def g_u1(p, b, eng):
    G = 'u-1'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        q.ev("([k,v])=>{const P=JSON.parse(localStorage.getItem('jopangi.postit')||'{}');P[k]=v;localStorage.setItem('jopangi.postit',JSON.stringify(P));}", [PIT_OLD, {'t': u'하네스 포스트잇', 'who': u'나', 'ts': '2026-09-01T00:00:00Z'}])
        reload_keep(q)
        q.until("()=>typeof UIDMIG_LAST==='undefined'||!!UIDMIG_LAST", ms=15000)
        q.pg.wait_for_timeout(800)
        home(q, gk='g'); go_key(q, 'T084510ㄱr')
        fl = q.ev("k=>__UZ.pitFlag(k)", u'T084510ㄱr')
        old = q.ev("p=>__UZ.pitKeys(p)", 'q|T0845101' + SEP)
        newk = q.ev("p=>__UZ.pitKeys(p)", u'q|T084510ㄱr' + SEP)
        reload_keep(q); q.until("()=>typeof UIDMIG_LAST==='undefined'||!!UIDMIG_LAST", ms=15000); q.pg.wait_for_timeout(600)
        mig2 = q.ev("()=>__UZ.migLast()")
        res[who] = {'깃발': bool(fl and fl.get('vis')), '옛 열쇠': len(old or []), '새 열쇠': len(newk or []), '두 번째 옮김': (mig2 or {}).get('moved', {}).get('postit', 0) if mig2 else None}
    n = res['NEW']
    T(G, u'포스트잇 — 옛 열쇠 q|T0845101… 심고 켬 → 리담 2008-45-10 ㉠(T084510ㄱr) 카드에 포스트잇 보임 · 옛 열쇠 0 · 두 번째 켜기 옮김 0', bool(n['깃발'] and n['옛 열쇠'] == 0 and n['새 열쇠'] == 1 and not n['두 번째 옮김']), n)
    T(G + '-헛', u'헛잣대 바탕 — 안 보임(옛 열쇠 그대로)', not res['BASE']['깃발'] and res['BASE']['옛 열쇠'] == 1, res['BASE'])


def g_u2(p, b, eng):
    G = 'u-2'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        q.ev("()=>{const O=JSON.parse(localStorage.getItem('jopangi.ox')||'{}');O['T0138611']={tg:{important:1},p:'O',ok:true,ts:'2026-09-01T00:00:00Z'};localStorage.setItem('jopangi.ox',JSON.stringify(O));}")
        reload_keep(q)
        q.until("()=>typeof UIDMIG_LAST==='undefined'||!!UIDMIG_LAST", ms=15000); q.pg.wait_for_timeout(800)
        home(q, gk='g')
        r = {}
        for k in ('TR01044', 'TH011518'):
            go_key(q, k)
            st = q.ev("k=>__UZ.star(k)", k)
            rec = q.ev("k=>__HM.oxRec(k)", k) or {}
            r[k] = {'⭐': bool(st and st['on'] and st['vis']), '풀이': rec.get('p') or ''}
        res[who] = r
    n = res['NEW']
    T(G, u'split ⭐ — T0138611 ⭐ → TR01044 · TH011518 두 카드 ⭐ 켜짐 보임 · 풀이 기록은 한쪽만', bool(n['TR01044']['⭐'] and n['TH011518']['⭐'] and [n['TR01044']['풀이'], n['TH011518']['풀이']].count('O') == 1), n)
    T(G + '-헛', u'헛잣대 바탕 — TH011518 ⭐ 꺼짐', not res['BASE']['TH011518']['⭐'], res['BASE'])


def g_u3(p, b, eng):
    G = 'u-3'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        home(q, gk='g')
        inp = q.ev("()=>__HM.at('#slot .mbsr input')")
        q.click(inp, 200)
        q.pg.keyboard.type('T0845075'); q.pg.wait_for_timeout(700)   # 진짜 글쇠 — oninput → 검색
        rows = q.ev("()=>[...document.querySelectorAll('#slot .mbres .rr')].map(r=>({t:r.textContent.replace(/\\s+/g,' ').trim().slice(0,80),badge:[...r.querySelectorAll('.srcb')].map(b=>b.textContent.trim())}))")
        q.pg.keyboard.press('Enter'); q.pg.wait_for_timeout(1500)
        n1 = [k for k in (q.ev("()=>__HM.popKeys()") or []) if k.startswith(u'q|📝 지문')]
        q.ev("()=>__HM.closeAll()")
        res[who] = {'줄': rows, '팝업': n1}
    n = res['NEW']
    T(G, u'🔍 split 옛 uid T0845075 → 두 줄 모두 「옛 uid · 갈라짐」 딱지(「ID」 딱지 0) · Enter → 팝업 둘',
      bool(n['줄'] and len(n['줄']) >= 2 and all(any(u'갈라짐' in x for x in r['badge']) for r in n['줄'][:2]) and not any('ID' == x for r in n['줄'] for x in r['badge']) and len(n['팝업']) == 2), n)
    T(G + '-헛', u'헛잣대 바탕 — 첫 줄 「ID」 딱지 · Enter 팝업 없음', bool(res['BASE']['줄'] and any('ID' == x for r in res['BASE']['줄'] for x in r['badge']) and not res['BASE']['팝업']), res['BASE'])


def g_u4(p, b, eng):
    G = 'u-4'
    home(p, gk='g')
    z = p.ev("()=>{const z=Object.values(VJ.P7map).find(z=>String(z.pdf쪽)==='504'&&String(z.책번호)==='3');return z?{id:z.id,uid:z.uid,key:oxKeyP7(z)}:null}")
    chips = None
    if z:
        go_key(p, z['key'])
        chips = p.ev("k=>__HM.chips(k)", z['key'])
    N(G, u'pdf 504 · 3번 카드 출제연도 칩 — 같은 해 리담과 글이 똑같지 않아(닮음 ≥0.95 · 똑같음 0) 합치지 않음 → 2025 칩 없음(보고)', {'줄': z, '칩': chips})


def un_pool(law):
    """★ sp_view4(10/3 · _task_jo_sp_view4 §C-1 목차 · add3 §B mokcha_상표.json) — u-6 「칩 = 서랍 = 풀」 의 풀(OXPOOL)은 상표 · 디보에 목차가 없어 리담 전부가 미분류이던 때 잣대다.
    목차(mokcha_<법>.json 마디)가 생긴 법은 미분류 = 어느 마디 리담 목록에도 없는 문항의 지문 수(앱 셈과 따로 데이터로) · 10/3 잼: 상표 = 2003-40-7 · 9 · 10 세 문항 15 = 칩 15 · 목차 파일이 없으면 None(옛 잣대)"""
    sh = {u'상표법': u'상표', u'디자인보호법': u'디보'}.get(law)
    f = os.path.join(M.DATA, u'mokcha_%s.json' % sh) if sh else ''
    if not sh or not os.path.isfile(f):
        return None
    placed = set(x for n in (json.load(io.open(f, encoding='utf-8')).get(u'마디') or []) for x in (n.get(u'리담') or []))
    J = json.load(io.open(os.path.join(M.DATA, u'jimun_%s.json' % sh), encoding='utf-8'))
    return sum(len(q.get(u'지문') or []) for q in (J.get(u'문제') or []) if q.get('id') not in placed)


def g_u6(p, b, eng):
    G = 'u-6'
    for law in ('상표법', '디자인보호법'):
        home(p, law)
        c = p.ev("()=>__UZ.hmChip('^미분류')")
        dl = p.ev("()=>__UZ.drawerLeaf('미분류 (리담)')")
        pool = un_pool(law)   # ★ sp_view4(10/3) — 목차가 생긴 법(상표)은 미분류 풀 = 어느 마디에도 없는 리담 문항의 지문 수(데이터로 셈) · 목차 없는 법은 옛 잣대(OXPOOL)
        if pool is None:
            pool = p.ev("()=>Object.keys(OXPOOL||{}).length")
        home(b, law)
        cb = b.ev("()=>__UZ.hmChip('^미분류')")
        T(G, u'%s 히트맵 「미분류 (리담)」 칩 = 서랍(레일) = 풀' % law, bool(c and dl and c['n'] == int(dl['n']) == pool), {'칩': c, '서랍': dl, '풀': pool})
        T(G + '-헛', u'%s 헛잣대 바탕 — 칩 ≠ 풀(겹친 열쇠)' % law, bool(cb and cb['n'] != b.ev("()=>Object.keys(OXPOOL||{}).length")), cb)
    home(p); home(b)


def g_u7(p, b, eng):
    G = 'u-7'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        home(q)
        out = {}
        for y, nos in (('2016', ['3', '4', '11', '13']), ('2018', ['4'])):
            q.ev("y=>{S.exvPg={};return __HM.gi(y)}", y)
            q.pg.wait_for_timeout(800)
            seen = set()
            for pg in range(4):
                seen |= set(q.ev("()=>[...document.querySelectorAll('#slot .exv-q')].map(q=>q.dataset.exno)") or [])
                seen |= set(q.ev("()=>[...document.querySelectorAll('[id^=\"gi-\"]')].map(c=>(c.querySelector('.qb.n')||{}).textContent||'').map(t=>t.replace('번',''))") or [])
                nb = q.ev("()=>__UZ.exvNext()")
                if not nb:
                    break
                q.click(nb, 1200)
            out[y] = [n for n in nos if n in seen]
        q.ev("()=>{S.jimunTab='ox';S.exvPg={}}")
        out['1998'] = q.ev("()=>(VJ.qs||[]).some(q=>String(q.연도)==='1998'&&/A와 B가 특허권을 공유한/.test(q.발문||''))")
        res[who] = out
    n = res['NEW']
    T(G, u'새 문항 앱 — 기출뷰 2016 → 3·4·11·13번 · 2018 → 4번 보임 · 1998 「A와 B가 특허권을 공유한」 문항', n['2016'] == ['3', '4', '11', '13'] and n['2018'] == ['4'] and n['1998'], n)
    T(G + '-헛', u'헛잣대 바탕 — 2016 3·4·11 · 2018 4 없음', res['BASE']['2016'] != ['3', '4', '11', '13'] and res['BASE']['2018'] != ['4'], res['BASE'])
    # 조문 패널 — 특허법 제99조에 1998-35-5 선지(★ jo_wonmun 뒤로는 오른쪽 패널 대신 떠 있는 정오문제 창 · 두 꼴 다 읽는다)
    pans = {}
    for who, q in (('NEW', p), ('BASE', b)):
        pans[who] = q.ev("""async()=>{try{closeAllPops();}catch(e){}S.tab='jo';S.law='특허법';S.jo='제99조';S.joPanel=true;S.joPanelP=0;await render();
          const w=ms=>new Promise(r=>setTimeout(r,ms));for(let i=0;i<100&&!(document.querySelector('#slot .jopane')||document.querySelector('.pop.wm-jp'));i++)await w(100);
          const ids=new Set();for(let pg=0;pg<12;pg++){S.joPanelP=pg;await render();await w(300);const cs=[...document.querySelectorAll('#slot .jopane > [id^="jp-"], .pop.wm-jp .jpcards > [id^="jp-"]')].map(c=>c.id.slice(3));const n0=ids.size;cs.forEach(x=>ids.add(x));if(ids.size===n0&&pg>0)break;}
          let y98=null;for(let pg=0;pg<12&&y98===null;pg++){S.joPanelP=pg;await render();await w(300);const c=document.getElementById('jp-TR89031');if(c)y98=[...c.querySelectorAll('.jxec')].map(b=>b.textContent.trim());}
          S.joPanelP=0;const a=[...ids];return {n:a.length,tr:a.filter(x=>/^TR8903/.test(x)),chips:y98,y1998:!!(y98||[]).some(t=>/^1998/.test(t))}}""")
        q.ev("()=>{S.tab='jimun';S.jimunTab='ox';S.joPanel=false;render()}"); q.pg.wait_for_timeout(1200)
    T(G, u'조문 패널 — 특허법 제99조 정오문제에 1998-35-5(PM-0311 · 1989 3번과 같은 글 = TR8903x 한 uid) 선지 보임 · 카드에 1998 출제연도 칩', bool(pans['NEW'] and len(pans['NEW']['tr']) >= 4 and pans['NEW']['y1998']), pans['NEW'])
    T(G + '-헛', u'헛잣대 바탕 — 같은 선지(1989 3번)는 있으나 1998 칩 없음', not (pans['BASE'] or {}).get('y1998'), pans['BASE'])


MBREF = {'chromium': _MBREF, 'webkit': _MBREFWK}


def g_a3w(p, b, eng):
    f = MBREF.get(eng) or MBREF.get('chromium')
    if not f or not os.path.exists(f):
        T('a3-3', u'민법 기준값 파일 없음(--mbref)', False, f); return
    g_a3(p, b, eng, json.load(io.open(f, encoding='utf-8')))


def g_c56w(p, b, eng):
    g_c56(p, b, eng, BR[eng])


def g_c11w(p, b, eng):
    f = MBREF.get(eng) or MBREF.get('chromium')
    g_c11(p, b, eng, json.load(io.open(f, encoding='utf-8')))


def g_a28(p, b, eng):
    """mbsame_add2 §C-8 — 히트맵 대목차 칩 = 첫 화면 편 카드 「총 N」 = 서랍 편 머리 · 편 전부 · 기출·기타 둘 다 · 헛잣대 = 바탕에서 어긋난 편"""
    G = 'a2-8'

    def triple(q):
        h = q.ev("()=>__UZ.hm()") or {}
        out = {}
        for c in h.get('chips') or []:
            m = re.match(u'^(\\d+)\\. (.+?) ([\\d,]+)$', c.get('t') or '')
            if not m or c.get('gk'):
                continue
            no = m.group(1)
            dh = q.ev("n=>__UZ.drawerHead(n)", no + '. ' + m.group(2))
            if dh is None:
                dh = q.ev("n=>__UZ.drawerTop(n)", int(no))   # 한 줄 편(12 실용신안)은 서랍에서 .jtit
            out[no] = [int(m.group(3).replace(',', '')), q.ev("n=>__UZ.cardTot(n)", int(no)), dh]
        return out
    res = {}
    for gk in ('g', 'x'):
        home(p, gk=gk)
        res[gk] = triple(p)
    bad = {gk: {k: v for k, v in r.items() if not (v[0] == v[1] == v[2])} for gk, r in res.items()}
    T(G, u'히트맵 대목차 칩 = 첫 화면 편 카드 「총 N」 = 서랍 편 머리 — 편 전부 · 기출 %d 편 · 기타 %d 편' % (len(res['g']), len(res['x'])),
      bool(res['g']) and bool(res['x']) and not bad['g'] and not bad['x'], {'기출 [칩, 카드, 서랍]': res['g'], '기타': res['x'], '어긋남': bad})
    home(b)
    rb = triple(b)
    badb = {k: v for k, v in rb.items() if not (v[0] == v[1] == v[2])}
    T(G + '-헛', u'헛잣대 바탕 — 칩 · 카드 · 서랍이 어긋난 편 있음', bool(badb), {'어긋남 [칩, 카드, 서랍]': badb})


BR = {}
PARTS = [('a8', g_a8), ('a6', g_a6), ('a8b', g_a8b), ('a7', g_a7), ('a7s', g_a7s), ('a28', g_a28), ('a1', g_a1), ('a2', g_a2), ('a3', g_a3w), ('a45', g_a45),
         ('c1', g_c1), ('c2', g_c2), ('c3', g_c3), ('c4', g_c4), ('c56', g_c56w), ('c7', g_c7), ('c9', g_c9), ('c10', g_c10), ('c11', g_c11w), ('c12', g_c12),
         ('u1', g_u1), ('u2', g_u2), ('u3', g_u3), ('u4', g_u4), ('u6', g_u6), ('u7', g_u7)]
DPARTS = [('a7d', d_a7), ('ud', d_u)]


def run_engine(pw, eng):
    br = getattr(pw, eng).launch()
    BR[eng] = br
    (ns, nd, ne), (bs, bd, be) = envs()
    try:
        p = Pg(br, eng, 'uzN', ns, nd, ne)
        b = Pg(br, eng, 'uzB', bs, bd, be)
        try:
            for k, fn in PARTS:
                if ONLY and k not in ONLY:
                    continue
                print('── %s · %s' % (eng, k), flush=True)
                try:
                    fn(p, b, eng)
                except Exception as e:
                    T('RUN', u'%s · %s 묶음이 멈춤' % (eng, k), False, repr(e)[:600])
            T('ERR', u'%s — NEW 앱 오류 0' % eng, not p.errs_all(), p.errs_all()[:6])
        finally:
            p.close(); b.close()
    finally:
        br.close()


def main():
    os.makedirs(M.WORK, exist_ok=True)
    t0 = time.time()
    for k, fn in DPARTS:
        if not ONLY or k in ONLY:
            try:
                fn()
            except Exception as e:
                T('RUN', u'%s 데이터 묶음이 멈춤' % k, False, repr(e)[:600])
    with sync_playwright() as pw:
        for eng in ENGS:
            RES.append(('ENG', eng, None, ''))
            run_engine(pw, eng)
    npass = sum(1 for r in RES if r[2] is True); nfail = sum(1 for r in RES if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · %s · NEW %s · 데이터 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), 'uidmbs2', os.path.basename(_NEW), _DATA, ','.join(ENGS)))
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[ok], g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:600]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
