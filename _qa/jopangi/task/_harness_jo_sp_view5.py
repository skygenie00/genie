# -*- coding: utf-8 -*-
r"""_task_jo_sp_view5 §D 관문 — 상표 1차객 책 카드에 뷰객 5판 얹기(앱 · 시험 데이터) · p8up 앱 길을 법 갈래로(판8 · 판5)

  python _harness_jo_sp_view5.py [--new <앱 파일 | genie git 판>] [--base <판>] [--eng chromium,webkit] [--only E1,E2,..] [--res <결과(기본 = 임시 폴더)>] [--yardstick]
        [--vendor <pdf.js 3.11.174 폴더>] [--exam <시험지 폴더>] [--mode gate|regress|smoke]
  --mode(_task_qa_slim 10/4) — 없으면 gate(= 이 판 앞과 같음) · regress = NEW 만(바탕 판 풀기 · 띄우기 0 · E5 의 특허 8판 무변 칸 = 기준 스냅샷) · smoke = regress 가운데 E1 · E2-폰 · E2-wk 만

  시험 데이터 = sp_view4 시험 데이터(_fx_sp_view4 · 뷰객 4판 · 지어낸 글)를 하네스가 돌릴 때 5판 꼴로 바꾼 덧판(파일을 따로 두지 않는다):
    책 줄 판 「V4」→「V5」 · 판5 = { cat: 같음·글·답·없음·새, t4, a4, s4 }(원장 §C · p8up 판8 꼴) · 5판에 없음 줄 = 판 「V4」 그대로 · 새 줄 = 단원 1.1 끝(새 uid 머리)
    표본: 글 V4-A1-OX1 · 답 V4-A1-OX2(O→X) · 없음 V4-A1-OX3 · 해설만 V4-A1-OX4(같음 + s4) · 같음 V4-A1-OX5-a · 새 V5-A1-N1 · 문항째 글 V4-B2-S20
  관문(§D):
    E1 칩 — 표본마다 「5판 고침」(회색 단추) · 「5판 고침 · 답 O→X」(빨강 단추) · 「5판에 없음」(회색 글) · 「5판 새」(초록 글) · 같음·해설만 = 없음 ·
       꼴 = 특허 8판 칩 그대로(.p8c 11px 700 · 바탕 없음 · 테 0) · 자리 = 칩 줄 끝(🃏 바로 뒤 · 태그 칸 앞) · 문항째 카드도
    E2 누름 — 「5판 고침」·「답」 마우스 · 손가락 → 머리 바로 아래 흐린 줄 「4판 글 …」(= 판5.t4) · 한 번 더 → 접힘
    E3 해설 — 「5판 해설 고침」(카드 정답·해설 · 문제 창) → 「4판 해설 …」(= 판5.s4) · 한 번 더 → 접힘 · s4 없는 줄 = 단추 없음
    E4 판 칩 · 새 카드 — V5 줄 「V5」 · 없음 줄 「V4」 · 새 줄 = 단원 1.1 본편 카드(책번호 자리 「OX N」 · 출처 줄 「뷰객 5판에만 있는 지문」 = 특허 「해례 8판에만 있는 지문」 꼴) · 4판 uid 전부 남음
    E5 특허 무변 — 8판 표본 넷(고침 · 답 · 없음 · 새) 칩·제목·꼴 · 「8판 해설 고침」 · 칩 줄 글 = 바탕과 같음 · 특허 책 카드 전수(p7Card)·문항째 카드 전수 outerHTML = 바탕
  헛잣대 = --yardstick : 바탕 b152217(cloud/exam_wrong_mark 끝 커밋) + 같은 시험 데이터 → E1~E4 묶음마다 FAIL 해야 통과(5판 표시 칸 14 = 바탕 FAIL) · E5 = 바탕끼리라 해당 없음
         대조 칸 6 = 바탕도 PASS(같음 줄 칩 없음 둘 · s4 없는 줄 해설 단추 없음 · 판 칩 V5/V4 · 새 카드 본편 자리 · 4판 uid) — sp_view4 가 이미 하는 일 · 새 판이 깨지 않는지 보는 칸
  도구 = 같은 폴더 _harness_jo_sp_view4(+ revfix0929b 서버 · SEED · 기기 · 가짜 원격)
  자리 = _roots(GENIE_ROOT) — 클라우드: GENIE_ROOT=<genie 작업트리> · WebKit = 터치 칸(E2 손가락)만 · 없으면 「안 잼」
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402  _task_qa_slim(10/4) — --mode · --snap-in · --snap-out 을 sys.argv 에서 뗀다(이 줄은 다른 import · 인자 읽기보다 먼저)
import copy, hashlib, io, json, os, re, subprocess, sys, tempfile, time   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEW = ARG('--new', _roots.genie('jo', 'index.html'))
BASE = ARG('--base', 'b152217')   # cloud/exam_wrong_mark 끝 커밋(sp_view5 바탕)
YARD = '--yardstick' in sys.argv
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
OUTF = ARG('--res', os.path.join(tempfile.gettempdir(), 'h_jospv5', '_harness_jo_sp_view5_result.txt'))   # 기본 = 임시 폴더(_qa 에 결과를 쓰지 않는다)
TMP = os.path.join(tempfile.gettempdir(), 'h_jospv5', 'p%d' % os.getpid())
os.makedirs(TMP, exist_ok=True)
_argv = sys.argv[:]
sys.argv = [_argv[0]] + [x for k in ('--exam', '--vendor') if k in _argv for x in (k, _argv[_argv.index(k) + 1])]
sys.path.insert(0, HERE)
import _harness_jo_sp_view4 as SV   # noqa: E402
sys.argv = _argv
H = SV.H
PC, PHONE = (1440, 900), H.PHONE
GRAY, RED, GREEN = 'rgb(156, 163, 175)', 'rgb(220, 38, 38)', 'rgb(21, 128, 61)'


def git(*a):
    return subprocess.run(['git', '-C', _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def app_src(x):
    if os.path.isfile(x):
        return open(x, 'rb').read().decode('utf-8')
    b = git('show', x + ':jo/index.html')
    if not b:
        raise SystemExit('앱을 못 읽었다: ' + x)
    return b.decode('utf-8')


def md5lf(s):
    return hashlib.md5(s.replace('\r\n', '\n').encode('utf-8')).hexdigest()


RES = []


def T(g, name, ok, detail=''):
    RES.append((g, name, bool(ok), detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', g, name, d[:700]), flush=True)
    return bool(ok)


def N(g, name, detail=''):
    RES.append((g, name, None, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('INFO | %s · %s | %s' % (g, name, d[:1000]), flush=True)


# ════════════════════════ 시험 데이터 — sp_view4 시험 데이터를 5판 꼴로(지어낸 글) ════════════════════════
S_TXT, S_ANS, S_NONE, S_SOL, S_SAME, S_OBJ = 'V4-A1-OX1', 'V4-A1-OX2', 'V4-A1-OX3', 'V4-A1-OX4', 'V4-A1-OX5-a', 'V4-B2-S20'
S_NEW, U_NEW = 'V5-A1-N1', 'SV5N0001'


def five():
    fj = copy.deepcopy(SV.FXJ)
    fm = copy.deepcopy(SV.FXM)
    old = {r['id']: copy.deepcopy(r) for r in fj['지문'] + fj.get('객관식', [])}
    for r in fj['지문'] + fj.get('객관식', []):
        r['판'] = 'V5'   # 5판에 있는 줄
    by = {r['id']: r for r in fj['지문'] + fj.get('객관식', [])}
    r = by[S_TXT]
    r['t'] = r['t'] + ' (5판 고침 — 시험 낱말 바꿈)'
    r['판5'] = {'cat': '글', 't4': old[S_TXT]['t']}
    r = by[S_ANS]
    r['ox'] = 'X'
    r['t'] = r['t'].replace('구별하는', '구별하지 않는')
    r['판5'] = {'cat': '답', 't4': old[S_ANS]['t'], 'a4': old[S_ANS]['ox']}
    r = by[S_NONE]
    r['판'] = 'V4'
    r['판5'] = {'cat': '없음'}
    r = by[S_SOL]
    r['sol'] = '시험 해설(5판) — 고친 해설 글(지어낸 글).'
    r['판5'] = {'cat': '같음', 's4': old[S_SOL]['sol']}
    by[S_SAME]['판5'] = {'cat': '같음'}
    r = by[S_OBJ]
    r['t'] = r['t'].replace('차례대로', '차례대로(5판)')
    r['판5'] = {'cat': '글', 't4': old[S_OBJ]['t']}
    base = old[S_TXT]
    new = {'id': S_NEW, 'uid': U_NEW, 't': '시험 지문 5판 새 1 — 5판에만 있는 시험 낱말(지어낸 글)', 'sol': '시험 해설 — 5판 새 지문(지어낸 글).',
           '쪽': '13', 'pdf쪽': '23', '태그': base['태그'], '연도들': [], '책번호': 'A1-OX7', 'ox': 'O', '유제': False, '차례마디': base.get('차례마디'),
           '배지': base.get('배지'), '순': 99, '판': 'V5', '유형태그': ['이론'], '단원': base.get('단원'), '판5': {'cat': '새'}}
    fj['지문'].append(new)
    fj['건수'] = len(fj['지문'])
    fj['판'] = 'V5 시험 데이터(_task_jo_sp_view5 §D · sp_view4 시험 데이터에서 · 지어낸 글)'
    unit = next(n for n in fm['마디'] if base['id'] in n['지문'])
    unit['지문'].append(S_NEW)
    return fj, fm, old


FJ5, FM5, OLD4 = five()


def overlay():
    d = os.path.join(TMP, 'data5')
    if os.path.isdir(d):
        return d
    os.makedirs(d)
    for x in os.listdir(SV.DATA0):
        if x in SV.FX_FILES:
            continue
        SV._ln(os.path.join(SV.DATA0, x), os.path.join(d, x))
    io.open(os.path.join(d, SV.FX_FILES[0]), 'w', encoding='utf-8').write(json.dumps(FJ5, ensure_ascii=False))
    io.open(os.path.join(d, SV.FX_FILES[1]), 'w', encoding='utf-8').write(json.dumps(FM5, ensure_ascii=False))
    return d


_TAGN = [0]


def open_pg(br, src, dev=PC, kind='new'):
    QJ.launch(kind)   # 띄움 셈만('new' | 'base')
    _TAGN[0] += 1
    tag = 'v5_%d' % _TAGN[0]
    SV.DATA_FOR[tag] = overlay()
    p = SV.open_pg(br, src, dev, tag)
    p.ev(V5_JS)
    return p


V5_JS = r"""() => { if (window.__V5) return 1;
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const vis = e => !!e && e.isConnected && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden' && e.getBoundingClientRect().height > 0;
const at = e => { if (!e) return null; try { e.scrollIntoView({ block: 'center', inline: 'nearest' }); } catch (x) {} const r = e.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2, a = document.elementFromPoint(cx, cy);
  return { cx: cx, cy: cy, on: !!a && (a === e || e.contains(a)) }; };
window.__V5 = {
  go: async (kind, id, dom, law) => { const w = ms => new Promise(r => setTimeout(r, ms)); try{ closeAllPops(); }catch(e){} await gotoJimun(kind, id, dom, '', law); await w(600);
    for (let i = 0; i < 100 && typeof busy !== 'undefined' && busy; i++) await w(100);
    if (!document.getElementById(dom) && typeof UZGK !== 'undefined'){ UZGK = UZGK === 'g' ? 'x' : 'g'; S.oxPage = null; await render(); await w(300);   /* 기출/기타 거름에 걸린 카드 = 다른 쪽 거름 */
      const pg = (typeof OXDOMPG !== 'undefined' && OXDOMPG || {})[dom]; if (pg != null && pg !== S.oxPage){ S.oxPage = pg; await render(); await w(300); } }
    return !!document.getElementById(dom); },
  head: dom => { const c = document.getElementById(dom); if (!c) return null; const hd = c.querySelector(':scope > .mbqhd'); if (!hd) return null; const kids = [...hd.children];
    const iMc = kids.findIndex(x => x.classList.contains('mcchip')), iTags = kids.findIndex(x => x.classList.contains('mbtags'));
    const p8 = kids.map((x, i) => [x, i]).filter(a => a[0].classList.contains('p8c')).map(a => { const x = a[0], s = getComputedStyle(x);
      return { t: txt(x), cls: x.className, tag: x.tagName, color: s.color, fs: s.fontSize, fw: s.fontWeight, bg: s.backgroundColor, bw: s.borderTopWidth, idx: a[1], vis: vis(x), title: x.title || '' }; });
    return { p8: p8, iMc: iMc, iTags: iTags, qexp: txt(hd.querySelector('.qb.v.qexp')), book: txt(c.querySelector('.p7cash, .mbqlab')), sub: txt(c.querySelector(':scope > .qsub')), hdt: txt(hd) }; },
  chipAt: (dom, t) => { const c = document.getElementById(dom); const b = c ? [...c.querySelectorAll(':scope > .mbqhd .p8c')].find(x => txt(x) === t) : null; return at(b); },
  t7: dom => { const c = document.getElementById(dom); const d = c ? c.querySelector(':scope > .p8t7') : null; if (!d) return null;
    return { lab: txt(d.querySelector('b')), t: txt(d), afterHead: !!d.previousElementSibling && d.previousElementSibling.classList.contains('mbqhd'), color: getComputedStyle(d).color, vis: vis(d) }; },
  peek: dom => { const e = document.querySelector('#' + CSS.escape(dom) + ' .mbexp'); if (e && e.style.display === 'none'){ const b = document.querySelector('#' + CSS.escape(dom) + ' .mbpeek'); if (b) b.click(); } return 1; },
  solAt: sel => { const b = [...document.querySelectorAll(sel + ' .p8sw .p8sh .p8c')].find(vis); return b ? Object.assign(at(b), { t: txt(b) }) : null; },
  solBox: sel => { const w = [...document.querySelectorAll(sel + ' .p8sw')].find(vis); const d = w ? w.querySelector(':scope > .p8t7') : null; return d ? { lab: txt(d.querySelector('b')), t: txt(d), vis: vis(d) } : null; },
  row: uid => { const m = /^__mg(\d+)$/.exec(String(S.mok || '')); if (!m) return { mok: S.mok };   /* 새 카드 자리 — 본편(__mg) · (미수록) 줄 아님 */
    const i = +m[1], u = c => c.kind === 'P' ? c.z.uid : (c.kind === 'O' ? c.o.uid : '');
    return { mok: S.mok, no: (VJ.M[i] || {}).no, inB: mlnCardsDeep(i, 'b').map(u).includes(uid), inU: mlnCardsDeep(i, 'u').map(u).includes(uid) }; },
  hasUids: us => { const have = new Set(Object.values((VJ && VJ.P7map) || {}).concat(Object.values((MLN && MLN.obj) || {})).map(z => z.uid)); return us.filter(u => !have.has(u)); }
};
return 1; }"""


def v5(p):
    p.ev(V5_JS)


def go(p, rid, law='상표법'):
    r = (FJ5 if law == '상표법' else None)
    v5(p)
    if law == '상표법':
        z = next(x for x in FJ5['지문'] + FJ5.get('객관식', []) if x['id'] == rid)
        dom = 'qb-' + (z.get('uid') or 'P7:' + rid)
    else:
        z = P7BY[rid]
        dom = 'qb-' + (z.get('uid') or 'P7:' + rid)
    ok = p.ev("([k, i, d, l]) => __V5.go(k, i, d, l)", ['P', rid, dom, law])
    return dom if ok else None


def press(p, at, wait=600):
    if not at or not at.get('on'):
        return False
    (p.tap if p.touch else p.click)(at['cx'], at['cy'], wait)
    return True


def ws(s):
    return re.sub(r'\s+', ' ', str(s or '')).strip()


P7J = json.load(open(os.path.join(SV.DATA0, 'jimun_7pan.json'), encoding='utf-8'))
P7BY = {z['id']: z for z in P7J['지문'] + P7J.get('객관식', [])}
P8S = {'고침': 'P7-0118', '답': 'P7-0826', '없음': 'P7-0595', '새': 'P8-0001'}


# ════════════════════════ 관문 ════════════════════════
def e1(br, src, tag):
    ok = True
    p = open_pg(br, src)
    try:
        want = {S_TXT: [('5판 고침', 'p8c g', 'BUTTON', GRAY)], S_ANS: [('5판 고침 · 답 O→X', 'p8c r', 'BUTTON', RED)], S_NONE: [('5판에 없음', 'p8c g', 'SPAN', GRAY)],
                S_NEW: [('5판 새', 'p8c n', 'SPAN', GREEN)], S_SOL: [], S_SAME: [], S_OBJ: [('5판 고침', 'p8c g', 'BUTTON', GRAY)]}
        for rid, w in want.items():
            dom = go(p, rid)
            h = p.ev("(d) => __V5.head(d)", dom) if dom else None
            c = (h or {}).get('p8') or []
            good = bool(h) and [(x['t'], x['cls'], x['tag'], x['color']) for x in c] == w and all(x['fs'] == '11px' and x['fw'] == '700' and x['bg'] == 'rgba(0, 0, 0, 0)' and x['bw'] == '0px' and x['vis'] for x in c) \
                and all(h['iMc'] >= 0 and x['idx'] == h['iMc'] + 1 + n and (h['iTags'] < 0 or x['idx'] < h['iTags']) for n, x in enumerate(c))
            ok &= T('E1', '%s — %s · 11px 700 · 바탕 없음 · 테 0 · 칩 줄 끝(🃏 바로 뒤 · 태그 칸 앞)' % (rid, ' · '.join('「%s」' % x[0] for x in w) or '칩 없음(같음)'), good, h)
        return ok
    finally:
        p.close()


def e2(br, src, tag, dev=PC, g='E2'):
    ok = True
    p = open_pg(br, src, dev)
    try:
        for rid, t, t4 in ((S_TXT, '5판 고침', OLD4[S_TXT]['t']), (S_ANS, '5판 고침 · 답 O→X', OLD4[S_ANS]['t']), (S_OBJ, '5판 고침', OLD4[S_OBJ]['t'])):
            dom = go(p, rid)
            at = p.ev("([d, t]) => __V5.chipAt(d, t)", [dom, t]) if dom else None
            press(p, at)
            r1 = p.ev("(d) => __V5.t7(d)", dom) if dom else None
            at2 = p.ev("([d, t]) => __V5.chipAt(d, t)", [dom, t]) if dom else None
            press(p, at2)
            r2 = p.ev("(d) => __V5.t7(d)", dom) if dom else None
            good = bool(at and at.get('on') and r1 and r1['vis'] and r1['afterHead'] and r1['lab'] == '4판 글' and ws(t4)[:40] in ws(r1['t']) and r1['color'] == GRAY and r2 is None)
            ok &= T(g, '%s 「%s」 %s 누름 → 머리 바로 아래 흐린 줄 「4판 글 …」(= 판5.t4) · 한 번 더 → 접힘' % (rid, t, '손가락' if p.touch else '마우스'), good, {'누름': at, '펼침': r1, '다시 누른 뒤': r2})
        return ok
    finally:
        p.close()


def e3(br, src, tag):
    ok = True
    p = open_pg(br, src)
    try:
        s4 = OLD4[S_SOL]['sol']
        dom = go(p, S_SOL)
        p.ev("(d) => __V5.peek(d)", dom)
        p.wait(400)
        sel = '#' + dom
        at = p.ev("(s) => __V5.solAt(s)", sel)
        press(p, at)
        b1 = p.ev("(s) => __V5.solBox(s)", sel)
        press(p, p.ev("(s) => __V5.solAt(s)", sel))
        b2 = p.ev("(s) => __V5.solBox(s)", sel)
        ok &= T('E3', '%s 카드 정답·해설 — 「5판 해설 고침」 → 「4판 해설 …」(= 판5.s4) · 한 번 더 → 접힘' % S_SOL,
                bool(at and at.get('on') and at.get('t') == '5판 해설 고침' and b1 and b1['lab'] == '4판 해설' and ws(s4)[:30] in ws(b1['t']) and b2 is None), {'단추': at, '펼침': b1, '접힘': b2})
        # 문제 창 — 같은 지문 popCard · 정답·해설 보기
        p.ev("(k) => { try{ closeAllPops(); }catch(e){} popCard(k, null); return 1; }", dom[3:])
        p.wait(600)
        p.ev("() => { const b = document.querySelector('.qp2 .qpk'); if (b) b.click(); return 1; }")
        p.wait(300)
        at = p.ev("(s) => __V5.solAt(s)", '.qp2')
        press(p, at)
        b1 = p.ev("(s) => __V5.solBox(s)", '.qp2')
        ok &= T('E3', '%s 문제 창 — 「5판 해설 고침」 → 「4판 해설 …」' % S_SOL, bool(at and at.get('on') and at.get('t') == '5판 해설 고침' and b1 and b1['lab'] == '4판 해설' and ws(s4)[:30] in ws(b1['t'])), {'단추': at, '펼침': b1})
        p.ev("() => { try{ closeAllPops(); }catch(e){} return 1; }")
        dom2 = go(p, S_SAME)
        p.ev("(d) => __V5.peek(d)", dom2)
        p.wait(300)
        n0 = p.ev("(s) => __V5.solAt(s)", '#' + dom2)
        ok &= T('E3', '%s(s4 없음) — 「5판 해설 고침」 단추 없음' % S_SAME, n0 is None, n0)
        return ok
    finally:
        p.close()


def e4(br, src, tag):
    ok = True
    p = open_pg(br, src)
    try:
        heads = {}
        for rid in (S_TXT, S_SAME, S_NONE, S_NEW, S_OBJ):
            dom = go(p, rid)
            heads[rid] = p.ev("(d) => __V5.head(d)", dom) if dom else None
        q = {k: (v or {}).get('qexp') for k, v in heads.items()}
        ok &= T('E4', '판 칩 — 5판 줄 「V5」 · 5판에 없음 줄 「V4」', q == {S_TXT: 'V5', S_SAME: 'V5', S_NONE: 'V4', S_NEW: 'V5', S_OBJ: 'V5'}, q)
        hn = heads.get(S_NEW) or {}
        go(p, S_NEW)
        rw = p.ev("(u) => __V5.row(u)", U_NEW)
        ok &= T('E4', '새 카드 자리 — 단원 1.1 본편(특허 8판 새 카드처럼 (미수록) 줄로 안 감 · 5판 책번호·쪽이 있는 책 줄)', bool(rw) and rw.get('no') == '1.1' and rw.get('inB') is True and rw.get('inU') is False, rw)
        ok &= T('E4', '새 카드 — 단원 1.1 에 섬 · 책번호 자리 「OX 7」 · 출처 줄 「… 뷰객 5판에만 있는 지문」', bool(hn) and hn.get('book', '').startswith('OX 7') and hn.get('sub', '').endswith('뷰객 5판에만 있는 지문'),
                {'책번호 자리': hn.get('book'), '출처 줄': hn.get('sub')})
        miss = p.ev("(us) => __V5.hasUids(us)", sorted(set(r['uid'] for r in SV.FXJ['지문'] + SV.FXJ.get('객관식', []) if r.get('uid'))))
        ok &= T('E4', '4판 uid 전부 남음(기록 열쇠 무변)', miss == [], {'빠진 uid': miss})
        return ok
    finally:
        p.close()


SWEEP_JS = r"""async () => {   /* 특허 책 카드 전수 — 그 법 VJ.P7map 줄마다 p7Card · MLN.obj 마다 mlnObjCard 를 떼어 그려 outerHTML 해시(FNV-1a) */
  const fnv = s => { let h = 0x811c9dc5; for (let i = 0; i < s.length; i++){ h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; } return ('0000000' + h.toString(16)).slice(-8); };
  const P = {}, O = {}; let i = 0, eP = 0, eO = 0;
  const zs = Object.values((VJ && VJ.P7map) || {});
  for (const z of zs){ try{ P[z.id] = fnv(p7Card(z, ++i, {}).outerHTML); }catch(e){ eP++; P[z.id] = 'ERR ' + String(e && e.message).slice(0, 60); } }
  for (const [id, o] of Object.entries((MLN && MLN.obj) || {})){ try{ O[id] = fnv(mlnObjCard(o, 1).outerHTML); }catch(e){ eO++; O[id] = 'ERR ' + String(e && e.message).slice(0, 60); } }
  return { law: S.law, nP: zs.length, n8: zs.filter(z => z.판8).length, nO: Object.keys(O).length, eP: eP, eO: eO, P: P, O: O };
}"""


def e5(br, src, base_src, tag):
    ok = True
    got = {}
    for who, s in ((('new', src), ('base', base_src)) if QJ.GATE else (('new', src),)):   # regress · smoke — 바탕 판은 안 띄운다(특허 8판 무변 칸 = 기준 스냅샷)
        p = open_pg(br, s, kind=who)
        try:
            out = {}
            for nm, rid in P8S.items():
                dom = go(p, rid, '특허법')
                h = p.ev("(d) => __V5.head(d)", dom) if dom else None
                out[nm] = {'p8': (h or {}).get('p8'), 'qexp': (h or {}).get('qexp'), 'book': (h or {}).get('book'), 'hdt': (h or {}).get('hdt')} if dom else {'카드': '못 찾음'}
            dom = go(p, P8S['고침'], '특허법')
            if dom:
                p.ev("(d) => __V5.peek(d)", dom)
                p.wait(300)
                at = p.ev("(s) => __V5.solAt(s)", '#' + dom)
                press(p, at)
                out['해설'] = {'단추': (at or {}).get('t'), '상자': p.ev("(s) => __V5.solBox(s)", '#' + dom)}
            else:
                out['해설'] = {'카드': '못 찾음'}
            out['전수'] = p.ev(SWEEP_JS) if dom else None
            got[who] = out
        finally:
            p.close()
    n = got['new']
    if QJ.GATE:
        b = got['base']
    else:   # regress · smoke — 바탕 판은 안 띄운다: 특허 8판 표본 넷 · 「8판 해설 고침」 · 책 카드 전수 해시 = 기준 스냅샷(칸마다)
        b = {nm: QJ.base('E5@' + nm, n[nm]) for nm in P8S}
        b['해설'] = QJ.base('E5@해설', n['해설'])
        b['전수'] = QJ.base('E5@전수', n.get('전수'))
    for nm in P8S:
        ok &= T('E5', '특허 8판 %s(%s) — 칩 글·꼴·제목·자리 · 판 칩 · 책번호 자리 · 칩 줄 글 = 바탕' % (nm, P8S[nm]), n[nm] == b[nm] and bool(n[nm].get('p8')), {'새': n[nm].get('p8') or n[nm], '바탕': b[nm].get('p8') or b[nm]})
    ok &= T('E5', '특허 「8판 해설 고침」 → 「7판 해설」 = 바탕', n['해설'] == b['해설'] and n['해설'].get('단추') == '8판 해설 고침' and (n['해설'].get('상자') or {}).get('lab') == '7판 해설', n['해설'])
    sn, sb = n.get('전수') or {}, b.get('전수') or {}
    dP = sorted(k for k in set(sn.get('P') or {}) | set(sb.get('P') or {}) if (sn.get('P') or {}).get(k) != (sb.get('P') or {}).get(k))
    dO = sorted(k for k in set(sn.get('O') or {}) | set(sb.get('O') or {}) if (sn.get('O') or {}).get(k) != (sb.get('O') or {}).get(k))
    ok &= T('E5', '특허 책 카드 전수(p7Card outerHTML · 판8 줄 포함) · 문항째 카드 전수(mlnObjCard) = 바탕 — 다른 카드 0',
            bool(sn) and sn.get('law') == '특허법' and sn.get('nP', 0) > 1000 and sn.get('n8', 0) > 0 and not dP and not dO and sn.get('eP') == sb.get('eP') and sn.get('eO') == sb.get('eO'),
            {'법': sn.get('law'), '책 카드': sn.get('nP'), '판8 줄': sn.get('n8'), '문항째': sn.get('nO'), '그리기 오류(새/바탕 · 책/문항째)': [sn.get('eP'), sb.get('eP'), sn.get('eO'), sb.get('eO')],
             '다른 책 카드': len(dP), '다른 문항째': len(dO), '표본': (dP + dO)[:5]})
    return ok


def webkit_try(pw):
    try:
        return pw.webkit.launch()
    except Exception as e:
        N('WK', 'WebKit 안 잼', str(e).splitlines()[0][:160])
        return None


def main():
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    src = app_src(NEW)
    if QJ.GATE:
        base_src = app_src(BASE)
        QJ.sub('git:show-app')
    else:   # regress · smoke — 바탕 판은 안 푼다(특허 8판 무변 칸 = 기준 스냅샷)
        base_src = None
    if YARD and QJ.GATE:
        src = base_src
    print('══ sp_view5 §D %s · 바탕 %s · 앱 md5(LF) %s · 바탕 %s' % ('헛잣대' if YARD else '새 판', BASE, md5lf(src), md5lf(base_src) if base_src is not None else '-'))
    N('E0', '시험 데이터(5판 꼴)', {'줄': len(FJ5['지문']), '객관식': len(FJ5.get('객관식', [])), '판5': sorted((r['id'], r['판5']['cat']) for r in FJ5['지문'] + FJ5.get('객관식', []) if r.get('판5'))})
    got, times = {}, {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        steps = [('E1', lambda: e1(br, src, 'e1')), ('E2', lambda: e2(br, src, 'e2')), ('E2-폰', lambda: e2(br, src, 'e2p', PHONE, 'E2-폰')),
                 ('E3', lambda: e3(br, src, 'e3')), ('E4', lambda: e4(br, src, 'e4')), ('E5', lambda: e5(br, src, base_src, 'e5'))]
        for g, fn in steps:
            if ONLY and not any(g.upper() == o or g.upper().startswith(o) for o in ONLY):
                continue
            if not QJ.want(g, smoke=g in ('E1', 'E2-폰')):   # smoke — 칩 꼴(PC) · 「5판 고침」 누름(폰 손가락 · WebKit 폰은 아래 E2-wk)
                continue
            if YARD and g == 'E5':
                N(g, '헛잣대 해당 없음', '바탕 = 바탕(특허 무변 잠금은 새 판 칸에서 돎)')
                continue
            print('── %s' % g, flush=True)
            t1 = time.time()
            _qs = QJ.stage(g)   # 단계 시간(§B-3) — launch.json stages
            _qs.__enter__()
            try:
                got[g] = bool(fn())
            except Exception as e:
                got[g] = False
                T(g, '돌다 멈춤', False, str(e).splitlines()[0][:300])
            times[g] = round(time.time() - t1)
            _qs.__exit__(None, None, None)
            print('   (%s %d초)' % (g, times[g]), flush=True)
        br.close()
        if 'webkit' in ENGS and not YARD and (not ONLY or any(o.startswith('E2') for o in ONLY)):
            wk = webkit_try(pw)
            if wk:
                try:
                    got['E2-wk'] = bool(e2(wk, src, 'e2w', PHONE, 'E2-wk'))
                finally:
                    wk.close()
    lines = []
    print('\n══ 요약 (%.0f초)%s' % (time.time() - t0, ' — 헛잣대' if YARD else ''))
    for g in got:
        cells = [r for r in RES if r[0] == g and r[2] is not None]
        nf = sum(1 for r in cells if not r[2])
        verdict = (('FAIL(헛잣대 통과)' if not got[g] else 'PASS(헛잣대 실패)') if YARD else ('PASS' if got[g] else 'FAIL'))
        s = '  %-6s %s (%d 칸 중 FAIL %d · %s초)' % (g, verdict, len(cells), nf, times.get(g, '-'))
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
