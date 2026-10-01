# -*- coding: utf-8 -*-
r"""_task_jo_wonmun §B(9/27) 관문 하네스 — 원문 · 마크업 창 · 켜기·저장 · 필기 조 · ✎ 편집 · 새로 칠하기 · 정오문제 창 · 인용하는 조 창.

  python _harness_jo_wonmun.py --new <앱> --data <jo/data> [--exam <gichul/pdf>] [--only w1,w2,...] [--eng chromium,webkit] [--res <결과 파일>]

  NEW  = 이 판 앱 + 데이터 · BASE = genie HEAD(바로 앞 인도판 = jo_cardfix) 앱 + HEAD 데이터 — 칸마다 헛잣대(바탕에서 FAIL)
  누름 = 진짜 포인터(page.mouse · 손가락 = Chromium CDP 터치 r22 · WebKit touchscreen.tap) · 보임 = display ≠ none · 높이 > 0 · 자리 = elementFromPoint
  틀 = mbsame 하네스(_harness_jo_gaek_mbsame.py)의 serve·Pg·__HM · uidmbs2 도구(__UZ) · 이 판 도구(__WM).
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import io, json, os, re, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


_NEW, _DATA, _EXAM = ARG('--new'), ARG('--data'), ARG('--exam')
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_wonmun_result.txt'))
sys.argv = [sys.argv[0], '--new', _NEW, '--data', _DATA, '--base', '47b12e9'] + (['--exam', _EXAM] if _EXAM else [])   # A-6(d) 9/30 — 바탕 = 인도 때 HEAD 47b12e9(결정로그 9/28 00:18 「헛잣대 47b12e9」) · HEAD 로 두면 인도 뒤 헛잣대·바탕 대조가 새 판끼리 맞대 거꾸로 FAIL
sys.path.insert(0, HERE)
import _harness_jo_gaek_mbsame as M   # noqa: E402
from playwright.sync_api import sync_playwright   # noqa: E402
M.TESTS = (M.TESTS + '\n' + io.open(os.path.join(HERE, '_harness_jo_uidmbs2_tests.js'), encoding='utf-8').read()
           + '\n' + io.open(os.path.join(HERE, '_harness_jo_wonmun_tests.js'), encoding='utf-8').read())
M.WORK = M.WORK + '_wm'
RES = []
LAWS = ['특허법', '상표법', '디자인보호법', '민사소송법']
LOCKMSG = '필기가 있어 잠금 — 글 폭이 바뀌면 필기가 어긋난다'
EX107 = {'항 소제목': 13, '따옴표': 2, '지식재산처 → 지재처': 4, '개정 꼬리표': 4, '색 글자': 23, '형광': 7, '밑줄': 23, '각주': 12, '두문자·태그 줄': 2, '메모 줄': 4, '임베드': 1}
EX140 = {'색 글자': 24, '형광': 3, '밑줄': 1, '각주': 3, '개정 꼬리표': 2, '조 이름표': 4}


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


class Pg(M.Pg):
    def __init__(self, br, eng, tag, src, data, exam, W=1440, H=900, **k):
        self.eng = eng
        ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, has_touch=True)
        super().__init__(br, tag + '_' + eng, src, data, exam, ctx=ctx, **k)
        self.pg.on('dialog', lambda d: d.dismiss())

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

    def J(self, expr, arg=None):
        v = self.ev(expr, arg)
        try:
            return json.loads(v) if isinstance(v, str) else v
        except Exception:
            return v


def envs():
    return M.new_env(), M.base_env()


def fresh(q):
    """기록 비우기 — 켠 것 · 마크업 · 필기 · 창 깃발"""
    q.ev("()=>{['jopangi.mkon','jopangi.markup','jopangi.ink'].forEach(k=>localStorage.removeItem(k));try{recDropCache();}catch(e){}try{S.mkWin=false;S.ciWin='';S.joPanel=false;S.stick=false;S.ink=false;}catch(e){}return 1}")
    q.ev("()=>{try{closeAllPops(true)}catch(e){}return 1}")   # 새 판은 인자 true 라야 원문 창 셋까지 닫는다(옛 판은 인자를 안 본다)


def go(q, law, jo):
    q.ev("a=>__WM.go(a[0],a[1])", [law, jo])
    q.pg.wait_for_timeout(250)


def reload_keep(q):
    q.pg.goto('http://127.0.0.1:%d/index.html?tok=1&keep=1' % q.port, wait_until='load', timeout=180000)
    q.pg.wait_for_function(M.READY, timeout=180000); q.pg.wait_for_timeout(700)


def ws_dot(a, b):
    return re.sub(r'[\s.]', '', a or '') == re.sub(r'[\s.]', '', b or '')


# ══════════ §B-1 원문 ══════════
def g_w1(p, b, eng):
    G = 'w-1'
    for jo, n_want in (('제140조', 16), ('제107조', 26)):
        res = {}
        for who, q in (('NEW', p), ('BASE', b)):
            fresh(q); go(q, '특허법', jo)
            res[who] = {'body': q.J("()=>__WM.body()"), 'orig': q.J("a=>__WM.orig(a[0],a[1])", ['특허법', jo])}
        n = res['NEW']; orig = n['orig'] or []
        texts = [l['t'] for l in n['body']]
        same = sum(1 for i, t in enumerate(texts) if i < len(orig) and t == orig[i])
        deco = {k: sum(l[k] for l in n['body']) for k in ('col', 'mark', 'u', 'b', 'lbl', 'sup', 'jl')}
        revs = [r for l in n['body'] for r in l['rev']]
        ok = len(orig) == n_want and len(texts) == n_want and same == n_want and not any(deco.values())
        det = {'원본 줄': len(orig), '본문 줄': len(texts), '같음': same, '꾸밈': deco, '회색': revs[:6], '첫 다름': next(([i, texts[i][:40], (orig[i] if i < len(orig) else '')[:40]] for i in range(len(texts)) if i >= len(orig) or texts[i] != orig[i]), None)}
        if jo == '제140조':
            ok = ok and revs.count('<개정 2016.2.29>') == 2
            T(G, u'특허 제140조 본문 줄 글 = 원본[1:] 16/16 · 색·형광·밑줄·굵게 0 · 이름표 0 · 각주 번호 0 · 「<개정 2016.2.29>」 2개 회색', ok, det)
        else:
            T(G, u'특허 제107조 본문 줄 글 = 원본[1:] 26/26 · 꾸밈·이름표·각주 번호 0', ok, det)
        bb = res['BASE']['body']; bt = [l['t'] for l in bb]
        T(G + '-헛', u'헛잣대 바탕 %s — 본문 = 볼트 행 글(원본과 다름)' % jo, sum(1 for i, t in enumerate(bt) if i < len(orig) and t == orig[i]) < n_want, {'바탕 줄': len(bt), '같음': sum(1 for i, t in enumerate(bt) if i < len(orig) and t == orig[i])})
    if eng == 'chromium':
        allr = {}
        for law in LAWS:
            allr[law] = p.J("l=>__WM.allOff(l)", law)
        tot = sum((allr[l] or {}).get('n', 0) for l in LAWS); bad = sum((allr[l] or {}).get('bad', 99) for l in LAWS)
        T(G, u'네 법 전 조(%d) — 모두 끈 본문 줄 글 = 원본 줄 · 다름 0(렌더러 wmLineEl 그대로 · 창·기록 없이)' % tot, tot == 1273 and bad == 0, allr)
        bl = b.J("l=>__WM.allOff(l)", '특허법')
        T(G + '-헛', u'헛잣대 바탕 — 원문 렌더러 없음', (bl or {}).get('err') == 'no wm', bl)


# ══════════ §B-2 마크업 창 ══════════
def unfold(q, sub):
    """그 종류가 접혀 있으면 종류 머리(이름)를 진짜 포인터로 눌러 편다"""
    w = q.J("()=>__WM.mkWin()")
    ty = [x for x in (w.get('types') or []) if x['sub'] == sub]
    if ty and not ty[0]['open']:
        q.press(q.J("a=>__WM.mkAt(a[0],a[1])", ['type', sub]), 'mouse', 400)


def open_mk(q, how='mouse'):
    if q.J("()=>__WM.mkWin()").get('win'):
        return True
    q.press(q.J("()=>__WM.mkBtn()"), how, 700)
    return q.J("()=>__WM.mkWin()").get('win')


def types_of(w):
    return {t['sub']: int(re.match(r'\d+', t['n']).group(0)) for t in (w.get('types') or []) if re.match(r'\d+', t['n'] or '')}


def cmp_all_on(p, b, law, jo):
    """NEW 모두 켜기 본문 ↔ BASE(지금 화면 = 볼트 행) — 짝 볼트 행(ri)마다 글 · 꾸밈 도장 · 각주 번호 · 이름표"""
    nb = p.J("()=>__WM.body()"); ns = p.J("()=>__WM.sig()")
    bb = b.J("()=>__WM.body()"); bs = b.J("()=>__WM.sig()")
    nby = {}; nsy = {}
    for l, s in zip(nb, ns):
        if l['ri'] is not None:
            nby[l['ri']] = l; nsy[l['ri']] = s['s']
    only_new = [l['t'][:40] for l in nb if l['ri'] is None]
    miss, wsd, diff, sigd, cnt = [], [], [], [], []
    for l, s in zip(bb, bs):
        ri = l['ri']
        if ri not in nby:
            miss.append([ri, l['t'][:40]]); continue
        m = nby[ri]
        if m['t'] != l['t']:
            (wsd if ws_dot(m['t'], l['t']) else diff).append([ri, m['t'][:50], l['t'][:50]])
        elif nsy.get(ri) != s['s']:
            a, c = nsy.get(ri) or [], s['s']
            k = next((i for i in range(max(len(a), len(c))) if (a[i] if i < len(a) else None) != (c[i] if i < len(c) else None)), None)
            sigd.append([ri, k, (a[k] if k is not None and k < len(a) else None), (c[k] if k is not None and k < len(c) else None), l['t'][max(0, (k or 0) - 5):(k or 0) + 8]])
        if m['sup'] != l['sup'] or m['lbl'] != l['lbl']:
            cnt.append([ri, m['sup'], l['sup'], m['lbl'], l['lbl']])
    return {'law': law, 'jo': jo, 'new 줄': len(nb), 'base 줄': len(bb), '바탕에만': miss, '원문에만(짝 없는 원문 줄)': only_new, '빈칸·점 차이': wsd, '글 다름': diff, '꾸밈 다름': sigd[:6], '꾸밈 다름 수': len(sigd), '각주·이름표 수 다름': cnt}


def g_w2(p, b, eng):
    G = 'w-2'
    res = {}
    for jo, EX, tot in (('제107조', EX107, 95), ('제140조', EX140, 37)):
        fresh(p); go(p, '특허법', jo)
        bt = p.J("()=>__WM.mkBtn()")
        how = 'touch' if jo == '제140조' else 'mouse'
        open_mk(p, how)
        w = p.J("()=>__WM.mkWin()")
        ty = types_of(w)
        items = w.get('items') or []
        opened = [t['sub'] for t in (w.get('types') or []) if t['open']]
        want_open = [s for s, n in ty.items() if n <= 6]
        ok = w.get('vis') and len(items) == tot and ty == EX and sorted(opened) == sorted(want_open)
        T(G, u'%s 「✎ 마크업」(%s) → 창 · 항목 %d · 종류별 수 = §0 예시 · 6 이하 종류만 펼침' % (jo, '손가락' if how == 'touch' else '마우스', tot), ok,
          {'창': w.get('vis'), '항목': len(items), '종류': ty, '편 것': opened})
        if jo == '제107조':
            T(G, u'단추 「✎ 마크업 0/95」 · 수 11px #9ca3af', bt.get('n') == '0/95' and (bt.get('ncs') or {}).get('fs') == '11px' and (bt.get('ncs') or {}).get('col') == 'rgb(156, 163, 175)', bt)
            css = w.get('css') or {}
            # ★ jo_theme(10/1) fix1 #33(_task_jo_theme_fix1.md 28줄 · A-33) — 연결 창·원문 창(wm-mk)도 A-7 틀(머리 #f8fafc · 테 #cbd5e1)로 바뀜 → 색 두 칸을 짝으로 받는다(옛 틀 짝 또는 A-7 틀 짝)
            T(G, u'창 틀 = 연결 창(흰 머리 · 테 #e5e7eb · 둥근 12 · 몸 #f9fafb · 또는 A-7 틀 머리 #f8fafc · 테 #cbd5e1) · 제목 「✎ 마크업 · 제107조 통상실시권 설정의 재정」 · 첫 줄 「켠 것 0 / 95 · 모두 켜기 · 모두 끄기 … ✎ 편집」',
              ((css.get('hd') or {}).get('bg'), (css.get('p') or {}).get('bc')) in (('rgb(255, 255, 255)', 'rgb(229, 231, 235)'), ('rgb(248, 250, 252)', 'rgb(203, 213, 225)')) and (css.get('p') or {}).get('br') == '12px'
              and (css.get('bd') or {}).get('bg') == 'rgb(249, 250, 251)' and w.get('title') == u'✎ 마크업 · 제107조 통상실시권 설정의 재정'
              and re.sub(r'\s+', '', w.get('bar') or '') == u'켠것0/95모두켜기모두끄기✎편집', {'css': css, 'title': w.get('title'), 'bar': w.get('bar'), '자리': [w.get('x'), w.get('y'), w.get('w'), w.get('h')]})   # 단추 사이는 flex 틈이라 글자에 빈칸이 없다 — 빈칸을 다 빼고 맞댐
            mr = p.ev("()=>{const m=document.querySelector('#slot > .main').getBoundingClientRect();return [Math.round(m.left),Math.round(m.top),Math.round(m.right)]}")
            T(G, u'처음 자리 = 본문 오른쪽 위(폭 440 · 창 오른쪽 끝 ≤ 본문 오른쪽 끝)', w.get('w') == 440 and w.get('x') + w.get('w') <= mr[2] and w.get('y') < mr[1] + 200, {'창': [w.get('x'), w.get('y'), w.get('w')], '본문': mr})
            pv = {i['sub']: [i['pv'], i['k']] for i in items}
            T(G, u'항목 줄 미리보기·오른쪽 글 = 종류마다(더한 글자 「+」·켜면 넣음 · 개정 꼬리표·켜면 숨김 · 지재처 「지식재산처→지재처」·켜면 바꿈 · 메모 줄·켜면 줄 · 각주 · 색 글자)',
              pv.get('항 소제목', ['', ''])[0].startswith('+') and pv.get('항 소제목', ['', ''])[1] == '켜면 넣음' and pv.get('개정 꼬리표', ['', ''])[1] == '켜면 숨김'
              and pv.get('지식재산처 → 지재처', ['', ''])[0] == '지식재산처→지재처' and pv.get('지식재산처 → 지재처', ['', ''])[1] == '켜면 바꿈'
              and pv.get('메모 줄', ['', ''])[1] == '켜면 줄' and pv.get('각주', ['', ''])[1] == '각주' and pv.get('색 글자', ['', ''])[1] in ('빨강 글자', '파랑 글자', '보라 글자', '글자색 글자'), pv)
        # 모두 켜기 → 지금 화면(볼트 행)
        p.press(p.J("a=>__WM.mkAt(a)", 'all'), 'mouse', 900)
        fresh(b); go(b, '특허법', jo)
        c = cmp_all_on(p, b, '특허법', jo)
        res[jo] = c
        w2 = p.J("()=>__WM.mkWin()")
        T(G, u'%s 「모두 켜기」 → 본문 글 = 볼트 행 글(바탕 지금 화면) · 다름은 빈칸·점만(목록) · 꾸밈 도장·각주 번호·이름표 수 같음 · 켠 것 %d/%d' % (jo, tot, tot),
          not c['바탕에만'] and not c['글 다름'] and not c['꾸밈 다름 수'] and not c['각주·이름표 수 다름'] and re.search(u'켠 것 %d / %d' % (tot, tot), re.sub(r'\s+', ' ', w2.get('bar') or '')), c)
        p.press(p.J("a=>__WM.mkAt(a)", 'none'), 'mouse', 900)
        body = p.J("()=>__WM.body()"); orig = p.J("a=>__WM.orig(a[0],a[1])", ['특허법', jo])
        T(G, u'%s 「모두 끄기」 → 원문(줄 글 = 원본) · jopangi.mkon 칸 없음' % jo, [l['t'] for l in body] == orig and p.J("a=>__WM.mkon(a)", '특허법:' + jo) is None, {'줄': len(body), 'mkon': p.J("a=>__WM.mkon(a)", '특허법:' + jo)})
    # 다른 법·조 몇 — 모두 켜기 = 지금 화면
    more = []
    for law, jo in (('특허법', '제2조'), ('특허법', '제29조'), ('특허법', '제42조의3'), ('특허법', '제52조'), ('특허법', '제132조의10'), ('특허법', '제19조'),
                    ('상표법', '제120조'), ('상표법', '제2조'), ('디자인보호법', '제121조'), ('디자인보호법', '제68조'), ('민사소송법', '제1조'), ('민사소송법', '제103조')):
        fresh(p); go(p, law, jo); open_mk(p)
        if not p.J("()=>__WM.mkWin()").get('items'):
            more.append({'law': law, 'jo': jo, '항목': 0}); continue
        p.press(p.J("a=>__WM.mkAt(a)", 'all'), 'mouse', 900)
        fresh(b); go(b, law, jo)
        more.append(cmp_all_on(p, b, law, jo))
    bad = [m for m in more if m.get('바탕에만') or m.get('글 다름') or m.get('꾸밈 다름 수') or m.get('각주·이름표 수 다름')]
    T(G, u'표본 12 조(네 법) 「모두 켜기」 = 지금 화면 — 바탕에만 있는 줄 0 · 글 다름 0 · 꾸밈 다름 0', not bad, {'다름': bad[:3], '빈칸·점': [[m['jo'], len(m.get('빈칸·점 차이') or [])] for m in more], '원문에만': [[m['jo'], m.get('원문에만(짝 없는 원문 줄)')] for m in more if m.get('원문에만(짝 없는 원문 줄)')]})
    fresh(p); fresh(b)
    go(b, '특허법', '제107조')
    b.press(b.J("()=>__WM.mkBtn()"), 'mouse', 700)
    T(G + '-헛', u'헛잣대 바탕 — 「✎ 마크업」 = 스티커 편집 켜기(창 없음)', not b.J("()=>__WM.mkWin()").get('win'), {'창': b.J("()=>__WM.mkWin()").get('win'), 'S': b.J("()=>__WM.cur()")})
    fresh(b)


# ══════════ §B-3 켜기·저장 ══════════
def g_w3(p, b, eng):
    G = 'w-3'
    fresh(p); go(p, '특허법', '제107조'); open_mk(p)
    before = {'bold': p.J("a=>__WM.charStyle(a)", u'(불실시)'), '③': p.J("a=>__WM.lineHas(a)", u'③')}
    p.press(p.J("a=>__WM.mkAt(a[0],a[1])", ['typeOn', u'항 소제목']), 'mouse', 900)
    bold = p.J("a=>__WM.charStyle(a)", u'(불실시)')
    it3 = [i for i in p.J("a=>__WM.mkItems(a[0],a[1])", [u'지식재산처 → 지재처', u'③'])]
    at = p.J("a=>__WM.mkAt(a[0],a[1])", ['item', it3[0]['key']]) if it3 else None
    p.press(at, 'mouse', 900)
    l3 = [t for t in p.J("a=>__WM.lineHas(a)", u'③') if t.startswith(u'③')]
    st = p.J("a=>__WM.mkon(a)", u'특허법:제107조') or {}
    ok = bold and int((bold or {}).get('fw') or 0) >= 700 and 'STRONG' in ' '.join(bold.get('tags') or []) and l3 and u'지재처장' in l3[0] and u'지식재산처장' not in l3[0]
    T(G, u'제107조 「항 소제목」 켜기 → ①-1 「(불실시)」 굵게 · 「지식재산처 → 지재처」 ③ 한 항목 켜기 → ③ 「지재처장」', ok, {'굵게': bold, '③': (l3 or [''])[0][:70], '전 ③': [t[:40] for t in before['③'] if t.startswith(u'③')], '전 굵게': before['bold']})
    T(G, u'jopangi.mkon 「특허법:제107조」 = {s:[항 소제목], k:[③ 지재처 열쇠], x:[]}', st.get('s') == [u'항 소제목'] and len(st.get('k') or []) == 1 and not st.get('x'), st)
    # 손가락 — 개정 꼬리표 ③ 켜기(= 숨김)
    itr = p.J("a=>__WM.mkItems(a[0],a[1])", [u'개정 꼬리표', u'③'])
    p.press(p.J("a=>__WM.mkAt(a[0],a[1])", ['item', itr[0]['key']]) if itr else None, 'touch', 900)
    l3b = [t for t in p.J("a=>__WM.lineHas(a)", u'③') if t.startswith(u'③')]
    T(G, u'손가락 — 「개정 꼬리표」 ③ 켜기 → ③ 줄에서 「<개정 2025.10.1>」 숨김', bool(itr) and l3b and u'<개정' not in l3b[0], {'③': (l3b or [''])[0][-40:]})
    reload_keep(p)
    go(p, '특허법', '제107조')
    bold2 = p.J("a=>__WM.charStyle(a)", u'(불실시)'); l3c = [t for t in p.J("a=>__WM.lineHas(a)", u'③') if t.startswith(u'③')]
    T(G, u'새로고침 뒤에도 그대로(굵게 · 지재처장 · 개정 꼬리표 숨김)', bold2 and int(bold2.get('fw') or 0) >= 700 and l3c and u'지재처장' in l3c[0] and u'<개정' not in l3c[0], {'굵게': bold2, '③': (l3c or [''])[0][:60]})
    open_mk(p)
    p.press(p.J("a=>__WM.mkAt(a)", 'none'), 'mouse', 900)
    T(G, u'「모두 끄기」 → jopangi.mkon 칸 지움', p.J("a=>__WM.mkon(a)", u'특허법:제107조') is None and u'특허법:제107조' not in json.loads(p.ev("()=>__WM.mkonRaw()") or '{}'), p.ev("()=>__WM.mkonRaw()"))
    sk = p.J("()=>__WM.syncKeys()") or []   # SYNC_KEYS 는 앞머리 jopangi. 를 붙인 꼴
    T(G, u'SYNC_KEYS 에 jopangi.mkon(43번째 · 끝)', len(sk) >= 43 and sk[42] == 'jopangi.mkon', [len(sk)] + sk[-3:])   # ★ jo_markfix(9/29) — 44번째 jopangi.jomark 가 뒤에 붙음 · mkon 은 43번째 그대로
    T(G + '-헛', u'헛잣대 바탕 — SYNC_KEYS 에 jopangi.mkon 없음', 'jopangi.mkon' not in (b.J("()=>__WM.syncKeys()") or []), len(b.J("()=>__WM.syncKeys()") or []))


def g_w3s(br, eng):
    """두 기기(새 판 A → 새 판 B) 같음 · 옛 판(바탕) C 가 올리면 빠짐 → A 가 되살림 — 원격 = 메모리(SEED) · 시작값 = studyplandata 기록.json"""
    G = 'w-3s'
    (ns, nd, ne), (bs, bd, be) = envs()
    REC = _roots.spd(r'jopangi\기록.json')
    r0 = io.open(REC, encoding='utf-8').read()
    out = {}
    a = Pg(br, eng, 'wmSA', ns, nd, ne, remote=r0)
    try:
        a.ev("()=>__HM.home('특허법')"); a.ev("()=>__HM.sync()")
        go(a, '특허법', '제107조'); open_mk(a)
        a.press(a.J("a=>__WM.mkAt(a[0],a[1])", ['typeOn', u'항 소제목']), 'mouse', 900)
        va = a.J("a=>__WM.mkon(a)", u'특허법:제107조')
        a.ev("()=>__HM.sync()")
        t1 = a.ev("()=>__HM.remote()")
        d1 = json.loads(t1 or '{}').get('data', {})
        out['A 올림'] = 'jopangi.mkon' in d1
        bdev = Pg(br, eng, 'wmSB', ns, nd, ne, remote=t1)
        try:
            bdev.ev("()=>__HM.home('특허법')"); bdev.ev("()=>__HM.sync()")
            go(bdev, '특허법', '제107조')
            vb = bdev.J("a=>__WM.mkon(a)", u'특허법:제107조')
            out['B 받음'] = vb
            out['B 본문 굵게'] = bdev.J("a=>__WM.charStyle(a)", u'(불실시)')
        finally:
            bdev.close()
        c = Pg(br, eng, 'wmSC', bs, bd, be, remote=t1)
        try:
            c.ev("()=>__HM.home('특허법')"); c.ev("()=>__HM.sync()")
            t2 = c.ev("()=>__HM.remote()")
        finally:
            c.close()
        d2 = json.loads(t2 or '{}').get('data', {})
        out['C(옛 판) 올린 뒤'] = 'jopangi.mkon' in d2
        a.ev("t=>__HM.setRemote(t)", t2); a.ev("()=>__HM.sync()")
        d3 = json.loads(a.ev("()=>__HM.remote()") or '{}').get('data', {})
        out['A 다시 맞춘 뒤'] = 'jopangi.mkon' in d3
        out['A 값'] = a.J("a=>__WM.mkon(a)", u'특허법:제107조')
    finally:
        a.close()
    T(G, u'두 기기 같음 — 새 판 A 「항 소제목」 켜기 → 올림 → 새 판 B 받음 = 같은 값 · B 본문 「(불실시)」 굵게', out.get('A 올림') and out.get('B 받음') == va and int(((out.get('B 본문 굵게') or {}).get('fw')) or 0) >= 700, out)
    N(G, u'옛 판(바탕) 기기가 올리면 mkon 이 원격 data 에서 빠지는가(qfix·bktype 와 같은 창)', out.get('C(옛 판) 올린 뒤'))
    T(G, u'옛 판 C 가 뺀 뒤 새 판 A 가 다음 맞추기에서 되살려 올림 · A 값 그대로', out.get('A 다시 맞춘 뒤') and out.get('A 값') == va, out)


# ══════════ §B-4 필기 있는 조 ══════════
def g_w4(p, b, eng):
    G = 'w-4'
    K = u'jo|특허법:제107조'
    for q in (p, b):
        fresh(q); q.ev("k=>__WM.inkSeed(k)", K); go(q, '특허법', '제107조')
    nb, bb = p.J("()=>__WM.body()"), b.J("()=>__WM.body()")
    ng, bg = p.J("()=>__WM.geo()"), b.J("()=>__WM.geo()")
    same_t = [l['t'] for l in nb] == [l['t'] for l in bb]
    dm = set(p.ev("()=>{const b=[...document.querySelectorAll('#slot .main .box')].find(x=>!x.classList.contains('fold')&&!x.closest('.pop'));return b?[...b.querySelectorAll(':scope > .ln')].filter(l=>l.querySelector('.dmn.dmnbr')).map(l=>l.dataset.ri==null?null:+l.dataset.ri):[]}") or [])   # ★ 9/30 A-6 — markfix A-5-4: 「다만,」 새 줄은 필기 조에도 는다(그 줄만 높아진다) — 높이 맞대기에서 그 줄만 뺀다
    same_g = [g for g in ng if g['ri'] not in dm] == [g for g in bg if g['ri'] not in dm]
    T(G, u'필기 조 — 본문 = 지금(바탕) 볼트 행 그대로(줄 글 · 글자 수 · 줄 높이 무변(「다만,」 새 줄 뺌) · 모두 켠 모양)', same_t and same_g and len(nb) == len(bb),
      {'줄': [len(nb), len(bb)], '글 같음': same_t, '높이 같음': same_g, '첫 높이 다름': next(([a, c] for a, c in zip(ng, bg) if a != c), None)})
    open_mk(p)
    w = p.J("()=>__WM.mkWin()")
    items = w.get('items') or []
    lk = {i['sub']: i['lock'] for i in items}
    okl = w.get('lockMsg', '').find(LOCKMSG) >= 0 and all(lk.get(s) for s in (u'항 소제목', u'지식재산처 → 지재처', u'개정 꼬리표', u'각주', u'메모 줄')) \
        and not any(lk.get(s) for s in (u'색 글자', u'형광', u'밑줄')) and all(i['on'] for i in items)
    T(G, u'창 — 「%s」 · 꾸밈(색·형광·밑줄·굵게)만 풀림 · 나머지 묶음 흐림(잠금) · 기본 모두 켬(기록 없음)' % LOCKMSG, okl and p.J("a=>__WM.mkon(a)", u'특허법:제107조') is None,
      {'잠금': lk, '안내': w.get('lockMsg'), 'mkon': p.J("a=>__WM.mkon(a)", u'특허법:제107조')})
    sig0 = p.J("()=>__WM.sig()")
    col = [i for i in items if i['sub'] == u'색 글자']
    unfold(p, u'색 글자')
    p.press(p.J("a=>__WM.mkAt(a[0],a[1])", ['item', col[0]['key']]) if col else None, 'mouse', 900)
    sig1 = p.J("()=>__WM.sig()"); ng1 = p.J("()=>__WM.geo()")
    chg = sum(1 for a, c in zip(sig0, sig1) for x, y in zip(a['s'], c['s']) if x != y)
    st = p.J("a=>__WM.mkon(a)", u'특허법:제107조') or {}
    T(G, u'색 글자 한 항목 끄기 → 그 글자 색만 빠짐(글·줄 높이 무변) · 기록 = 꾸밈 종류 통째 켬 + 끈 열쇠 하나', chg > 0 and ng1 == ng and len(st.get('x') or []) == 1 and u'색 글자' in (st.get('s') or []),
      {'바뀐 글자': chg, '높이 같음': ng1 == ng, 'mkon': st})
    lkd = [i for i in items if i['sub'] == u'항 소제목']
    unfold(p, u'항 소제목')
    p.ev("()=>{document.querySelectorAll('#toasts .toast').forEach(t=>t.remove());return 1}")
    p.press(p.J("a=>__WM.mkAt(a[0],a[1])", ['item', lkd[0]['key']]) if lkd else None, 'mouse', 500)
    ts = p.J("()=>__WM.toasts()")
    st2 = p.J("a=>__WM.mkon(a)", u'특허법:제107조') or {}
    T(G, u'잠긴 항목(항 소제목) 누름 → toast 「%s」 · 기록 무변' % LOCKMSG, any(LOCKMSG in t for t in ts) and st2 == st, {'toast': ts, 'mkon': st2})
    for q in (p, b):
        q.ev("k=>__WM.inkClear(k)", K); fresh(q)


# ══════════ §B-5 ✎ 편집 ══════════
def g_w5(p, b, eng):
    G = 'w-5'
    for q in (p, b):
        fresh(q); q.ev("b=>__WM.orphanSeed(b)", u'특허법:제107조'); go(q, '특허법', '제107조')
    open_mk(p)
    p.press(p.J("a=>__WM.mkAt(a)", 'edit'), 'mouse', 900)
    b.press(b.J("()=>__WM.mkBtn()"), 'mouse', 900)   # 바탕 = ✎ 마크업 이 곧 스티커 편집
    nb, bb = p.J("()=>__WM.body()"), b.J("()=>__WM.body()")
    ns, bs = p.J("()=>__WM.stickBar()"), b.J("()=>__WM.stickBar()")
    T(G, u'✎ 편집 켜면 본문 = 볼트 행 전부(바탕 편집 모드와 줄 글 같음) · 스티커 수 같음 · 고아 기록 무변', [l['t'] for l in nb] == [l['t'] for l in bb] and ns.get('on') and ns.get('stk') == bs.get('stk') and ns.get('orphan') == bs.get('orphan') == u'고아 기록 1',
      {'줄': [len(nb), len(bb)], 'new 바': ns, 'base 바': bs})
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        q.press(q.J("i=>__WM.stkAt(i)", 0), 'mouse', 700)
        r0 = q.J("()=>__WM.stkPop()") or {}
        if r0.get('btns'):
            r0['btns'] = [x for x in r0['btns'] if x != u'모두 닫기']   # 떠 있는 창이 둘 이상이면 맨 위 창에 붙는 단추(마크업 창이 떠 있는 NEW 만) — 스티커 창 몫이 아니다
        res[who] = r0
        q.ev("()=>__WM.closePops()")
    T(G, u'스티커 누름 → 지우기·유형·색 창 무변(단추 같음)', (res['NEW'] or {}).get('on') and res['NEW'] == res['BASE'], res)
    w = p.J("()=>__WM.mkWin()")
    T(G, u'✎ 편집 켜진 동안 창은 그대로 뜬다 · 단추 「✎ 편집 켜짐」', w.get('win') and u'✎ 편집 켜짐' in (w.get('bar') or ''), w.get('bar'))
    p.press(p.J("a=>__WM.mkAt(a)", 'edit'), 'mouse', 900)
    nb2 = p.J("()=>__WM.body()")
    T(G, u'✎ 편집 끄면 다시 원문(모두 꺼짐)', all(l['wm'] for l in nb2) and not p.J("()=>__WM.stickBar()").get('on'), {'줄': len(nb2)})
    for q in (p, b):
        fresh(q)


# ══════════ §B-6 새로 칠하기 ══════════
def drag_sel(q, pts):
    if not pts:
        return False
    q.pg.mouse.move(pts['x1'], pts['y1']); q.pg.mouse.down()
    q.pg.mouse.move((pts['x1'] + pts['x2']) / 2, pts['y2'], steps=4); q.pg.mouse.move(pts['x2'], pts['y2'], steps=4)
    q.pg.mouse.up(); q.pg.wait_for_timeout(400)
    return True


def g_w6(p, b, eng):
    G = 'w-6'
    fresh(p); go(p, '특허법', '제107조')
    n0 = len(p.J("a=>__WM.mks(a)", u'특허법:제107조') or [])
    pts = p.J("a=>__WM.selPts(a[0],a[1])", [u'통상실시권', 0])
    drag_sel(p, pts)
    sel = p.ev("()=>__WM.selText()")
    bub = p.J("()=>__WM.bub()")
    p.click(bub, 700)
    att = p.J("()=>__WM.attPop()")
    p.click(att, 700)
    nb = p.J("a=>__WM.newPopBtn(a)", u'형광')
    p.click(nb, 900)
    mks = p.J("a=>__WM.mks(a)", u'특허법:제107조') or []
    st = p.J("a=>__WM.mkon(a)", u'특허법:제107조') or {}
    open_mk(p)
    w = p.J("()=>__WM.mkWin()")
    newit = [i for i in (w.get('items') or []) if i['on']]
    cs = p.J("a=>__WM.charStyle(a)", u'통상실시권')
    T(G, u'원문 글자 긁기(마우스) → 🏷 거품 → 다른 마크업 ▸ → 새 마크업 · 그 항목은 켠 채(mkon k) · 본문에 칠함', pts and sel == u'통상실시권' and len(mks) == n0 + 1 and len(st.get('k') or []) == 1 and len(newit) == 1
      and cs and any(t.startswith('MARK') or ('SPAN' in t) for t in (cs.get('tags') or [])),
      {'선택': sel, '거품': bub.get('on'), '붙이기 창': att, '새 창 단추': (nb or {}).get('all'), 'mk': mks[-1:] if mks else None, 'mkon': st, '켠 항목': newit[:1], '꼴': cs})
    p.ev("()=>__WM.closePops()")
    # 원문에만 있는 글자 — 지재처 항목 끔 상태의 「지식재산처」
    p.ev("()=>{document.querySelectorAll('#toasts .toast').forEach(t=>t.remove());return 1}")
    n1 = len(p.J("a=>__WM.mks(a)", u'특허법:제107조') or [])
    pts2 = p.J("a=>__WM.selPts(a[0],a[1])", [u'지식재산처장', 0])
    drag_sel(p, pts2)
    bub2 = p.J("()=>__WM.bub()")
    p.click(bub2, 700)
    ts = p.J("()=>__WM.toasts()")
    n2 = len(p.J("a=>__WM.mks(a)", u'특허법:제107조') or [])
    T(G, u'원문에만 있는 글자(「지식재산처장」 — 지재처 항목 꺼짐) 긁기 → 거품 누름 = 막음 · toast · 새 기록 0', pts2 and any(u'원문에만 있는 글자' in t for t in ts) and n2 == n1 and not p.J("()=>__WM.attPop()"),
      {'toast': ts, '기록': [n1, n2]})
    fresh(b); go(b, '특허법', '제107조')
    T(G + '-헛', u'헛잣대 바탕 — 본문에 원문 글자 「지식재산처장」 이 없다(볼트 글 「지재처장」)', not b.J("a=>__WM.selPts(a[0],a[1])", [u'지식재산처장', 0]), None)
    fresh(p); fresh(b)


# ══════════ §B-7 정오문제 창 ══════════
def g_w7(br, eng):
    G = 'w-7'
    (ns, nd, ne), (bs, bd, be) = envs()
    p = Pg(br, eng, 'wmJN', ns, nd, ne, W=1890, H=870)
    b = Pg(br, eng, 'wmJB', bs, bd, be, W=1890, H=870)
    try:
        res = {}
        for who, q in (('NEW', p), ('BASE', b)):
            fresh(q); go(q, '특허법', '제140조')
            res[who + '0'] = q.J("()=>__WM.jpWin()")
            q.press(q.J("()=>__WM.jpChip()"), 'mouse', 1200)
            res[who] = q.J("()=>__WM.jpWin()")
        n = res['NEW']
        T(G, u'칩 「☑ 정오문제 11」 → 떠 있는 창 보임 · 오른쪽 패널·손잡이 DOM 0 · 본문 폭 1665±2(1890×870)', n.get('vis') and not n.get('pane') and not n.get('handle') and abs((n.get('mainW') or 0) - 1665) <= 2,
          {'창': [n.get('x'), n.get('y'), n.get('w'), n.get('h')], '본문 폭': n.get('mainW'), '바탕 본문 폭': res['BASE'].get('mainW'), '열기 전': res['NEW0'].get('mainW')})
        bar = n.get('bar') or []
        on = [x for x in bar if x['on']]
        cs_on = (on[0]['cs'] if on else {}) or {}
        cs_off = next((x['cs'] for x in bar if not x['on']), {}) or {}
        T(G, u'머리 한 줄 「전체 11 · 해례 5 · 리담 6 · 1 2 3」 · 12px 700 · 켜진 것 #2563eb · 나머지 #9ca3af · 바탕·테 없음 · 「☑ 정오문제 N건」·「쪽」 글 없음',
          [x['t'] for x in bar] == [u'전체 11', u'해례 5', u'리담 6', '1', '2', '3'] and cs_on.get('fs') == '12px' and cs_on.get('fw') == '700' and cs_on.get('col') == 'rgb(37, 99, 235)'
          and cs_off.get('col') == 'rgb(156, 163, 175)' and cs_on.get('bg') in ('rgba(0, 0, 0, 0)', 'transparent') and cs_on.get('bw') == '0px' and not n.get('head') and u'쪽' not in (n.get('barText') or ''),
          {'머리': [x['t'] for x in bar], 'on': cs_on, 'off': cs_off})
        nav = n.get('nav') or {}
        arr = nav.get('arr') or []
        T(G, u'창 아래 「← 1 / 3 →」 가운데 · 13px 700 #6b7280 · 화살표 15px #2563eb · 첫 쪽 ← 흐림 #d1d5db · 「✅ 채점」·「← 이전 · 다음 →」 DOM 0 · 창 아래 안내 줄 없음',
          re.sub(r'\s+', '', nav.get('t') or '') == u'←1/3→' and (nav.get('cs') or {}).get('fs') == '13px' and (nav.get('cs') or {}).get('col') == 'rgb(107, 114, 128)'
          and len(arr) == 2 and arr[0]['dis'] and arr[0]['cs']['col'] == 'rgb(209, 213, 219)' and arr[1]['cs']['col'] == 'rgb(37, 99, 235)' and arr[1]['cs']['fs'] == '15px'
          and n.get('grade') == 0 and not n.get('foot'), nav)
        p.press(p.J("a=>__WM.jpAt(a)", 'next'), 'mouse', 700)
        n2 = p.J("()=>__WM.jpWin()")
        p.press(p.J("a=>__WM.jpAt(a[0],a[1])", ['bar', u'해례 5']), 'touch', 700)
        n3 = p.J("()=>__WM.jpWin()")
        p.press(p.J("a=>__WM.jpAt(a[0],a[1])", ['bar', u'전체 11']), 'mouse', 700)
        T(G, u'→ = 2쪽(머리 「2」 켜짐) · 손가락 「해례 5」 → 한 쪽뿐 = 쪽 번호·아래 줄 없음 · 카드 5', re.sub(r'\s+', '', (n2.get('nav') or {}).get('t') or '') == u'←2/3→'
          and [x['t'] for x in (n2.get('bar') or []) if x['on']] == [u'전체 11', '2'] and [x['t'] for x in (n3.get('bar') or [])] == [u'전체 11', u'해례 5', u'리담 6'] and not n3.get('nav') and len(n3.get('cards') or []) == 5,
          {'2쪽': (n2.get('nav') or {}).get('t'), '해례': [x['t'] for x in (n3.get('bar') or [])], '카드': len(n3.get('cards') or [])})
        keys = p.J("()=>__WM.jpKeys()") or []
        p.ev("k=>__WM.oxClearAll(k)", keys); b.ev("k=>__WM.oxClearAll(k)", keys)
        p.ev("()=>__WM.rr()")
        k1 = keys[0] if keys else None
        p.press(p.J("a=>__WM.jpAt(a[0],a[1])", ['ox', {'k': k1, 'v': 'O'}]), 'mouse', 1200)
        r1 = p.J("k=>__WM.rec(k)", k1) or {}
        c1 = p.J("k=>__WM.jpCard(k)", k1) or {}
        sel = [o for o in (c1.get('ox') or []) if ' sel' in o['cls']]
        want_bc = 'rgb(47, 111, 208)' if r1.get('ok') else 'rgb(217, 59, 59)'
        want_t = u'✓ 맞음' if r1.get('ok') else u'✗ 틀림 · 정답 X'
        T(G, u'창 안 O 한 번(마우스) → 그 지문 rec.p · 「%s」 · 고른 답 테 %s · 정답·해설 펴짐' % (want_t, '파랑' if r1.get('ok') else '빨강'),
          r1.get('p') == 'O' and c1.get('res') == want_t and c1.get('exp') and sel and sel[0]['bc'] == want_bc, {'rec': r1, '카드': c1})
        k2 = keys[1] if len(keys) > 1 else None
        p.press(p.J("a=>__WM.jpAt(a[0],a[1])", ['ox', {'k': k2, 'v': 'X'}]), 'touch', 1200)
        r2 = p.J("k=>__WM.rec(k)", k2) or {}
        T(G, u'창 안 X 손가락 → 곧바로 채점(rec.p = X)', r2.get('p') == 'X', r2)
        # 1차객 화면 — 같은 지문 기록
        M_go = go_key(p, k1)
        g1 = p.J("k=>__WM.gkCard(k)", k1)
        T(G, u'1차객 화면 같은 지문 기록 = 창과 같음(채점됨 · 같은 결과 글)', g1 and (g1.get('res') or '').startswith(u'✓ 맞음' if r1.get('ok') else u'✗ 틀림') and any(' sel' in o['cls'] for o in (g1.get('ox') or [])) and not g1.get('inst'), {'1차객': g1, 'sel': M_go})
        # 1차객 O/X = 마킹만
        k3 = keys[2] if len(keys) > 2 else None
        go_key(p, k3)
        p.press(p.J("a=>__WM.gkOx(a[0],a[1])", [k3, 'O']), 'mouse', 900)
        r3 = p.J("k=>__WM.rec(k)", k3) or {}
        T(G, u'1차객 O/X 는 여전히 마킹만(rec.m = O · rec.p 없음)', r3.get('m') == 'O' and not r3.get('p'), r3)
        # 조를 바꿔도 창이 따라간다 — 팝업 링크가 부르는 goJo(closeAllPops 를 거친다 · 옛 판 오른쪽 패널처럼)
        p.ev("()=>{goJo('특허법','제141조');return 1}"); p.pg.wait_for_timeout(1500)
        j9 = p.J("()=>__WM.jpWin()")
        T(G, u'조를 바꿔도(goJo — 팝업 링크 길 · closeAllPops 를 거침) 정오문제 창이 열린 채 그 조를 따라간다', bool(j9.get('win')) and u'제141조' in (j9.get('title') or ''), {'title': j9.get('title'), 'win': j9.get('win')})
        # 풀이 기록 × 두 번(창 안)
        go(p, '특허법', '제140조'); p.ev("()=>__WM.rr()")
        if not p.J("()=>__WM.jpWin()").get('win'):   # 1차객 화면을 다녀오면 창 깃발이 풀릴 수 있다 — 칩으로 다시 연다(진짜 포인터)
            p.press(p.J("()=>__WM.jpChip()"), 'mouse', 1200)
        p.press(p.J("a=>__WM.jpAt(a[0],a[1])", ['src', k1]), 'mouse', 700)
        p.press(p.J("a=>__WM.jpAt(a[0],a[1])", ['rgb', k1]), 'mouse', 600)
        x1 = p.J("a=>__WM.jpAt(a[0],a[1])", ['rgx', k1])
        p.press(x1, 'mouse', 500)
        p.press(p.J("a=>__WM.jpAt(a[0],a[1])", ['rgx', k1]), 'mouse', 900)
        r1b = p.J("k=>__WM.rec(k)", k1)
        T(G, u'창 안 풀이 기록 칸 × 두 번 → 지워짐(rec 없음 · 묘비)', (not r1b or not r1b.get('p')) and len(p.J("k=>__WM.recGone(k)", k1) or []) >= 1, {'rec': r1b, '묘비': p.J("k=>__WM.recGone(k)", k1), '×': x1})
        bb = res['BASE']
        T(G + '-헛', u'헛잣대 바탕 — 오른쪽 패널(창 없음) · 「✅ 채점」 있음', not bb.get('win') and bb.get('pane') and (bb.get('grade') or 0) >= 1, bb)
        p.ev("k=>__WM.oxClearAll(k)", keys)
        T('ERR', u'%s — 정오 창 NEW 앱 오류 0' % eng, not p.errs_all(), p.errs_all()[:6])
    finally:
        p.close(); b.close()


def go_key(q, k):
    q.ev("l=>__HM.home(l)", '특허법')
    if q.ev("()=>__UZ.has('UZGK')"):
        g = 'g' if q.ev("k=>{try{return uzGkPass?(UZGK='g',uzGkPass(k)):true}catch(e){return true}}", k) else 'x'
        q.ev("v=>__UZ.gk(v)", g)
    sel = q.ev("k=>__UZ.selOfKey(k)", k)
    if not sel:
        return None
    q.ev("s=>__HM.go(s)", sel)
    pg = q.ev("k=>{const P=(OXPOOL||{})[k];if(!P)return null;const d=P.dom;const c=[...document.querySelectorAll('.qb.id')].find(b=>b.textContent.trim()===k);return c?null:(OXDOMPG||{})[d]}", k)
    if pg:
        q.ev("n=>__HM.page(n)", pg)
    q.pg.wait_for_timeout(300)
    return sel


# ══════════ §B-8 인용하는 조 창 ══════════
def g_w8(p, b, eng):
    G = 'w-8'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        fresh(q); go(q, '특허법', '제140조')
        ch = q.J("()=>__WM.ciChip()")
        q.press(ch, 'mouse' if who == 'NEW' else 'mouse', 900)
        res[who] = {'chip': ch, 'win': q.J("()=>__WM.ciWin()")}
    n = res['NEW']; w = n['win']
    rows = w.get('rows') or []
    r1 = next((r for r in rows if r['k'] == u'제132조의3'), {})
    # ★ 9/30 A-6 — joscreen0929 A-3-1·2: 칩 「📜 인용하는 조 N」 → 「↩피N」(역인덱스 그대로) · 창 제목 「↩ 피인용 N · 본문에 「제N조」를 적은 조」
    T(G, u'「↩피5」(누름 가능) → 창 · 제목 「↩ 피인용 5 · 본문에 「제140조」를 적은 조」 · 5 줄(역인덱스 차례) · 폭 540',
      n['chip'].get('cur') == 'pointer' and w.get('vis') and w.get('title') == u'↩ 피인용 5 · 본문에 「제140조」를 적은 조'
      and [r['k'] for r in rows] == [u'제132조의3', u'제133조의2', u'제136조', u'제140조의2', u'제141조'] and w.get('w') == 540, {'칩': n['chip'], '제목': w.get('title'), '줄': [[r['cn'], r['ct']] for r in rows]})
    T(G, u'제132조의3 구절 — 「제140조제1항ㆍ제2항ㆍ제5항」 굵게 + #fef3c7 바탕 · 조사 「을」 뗌 · 조 번호 #2f6fd0',
      r1.get('b') == u'제140조제1항ㆍ제2항ㆍ제5항' and r1.get('bbg') == 'rgb(254, 243, 199)' and int(r1.get('bfw') or 0) >= 700 and (r1.get('cp') or '').find(u'제5항을 준용') >= 0, r1)
    N(G, u'구절 전부(원본[1:] · 앞 38자 · 뒤 28자)', [[r['k'], r['cp']] for r in rows])
    # ★ 9/30 A-6 — joscreen0929 A-3-4: 꼬리 줄 = 🔗인 목록과 같은 셈(원문 인용 · 앱 wmCiteOut · 옛 = 볼트 행 L 링크 「제135조 · 제136조 · 제138조」)
    ins = p.ev("()=>get('jo_특허법_본문.json').then(B=>wmCiteOut(B.조['제140조'],'제140조'))") or []
    nin = p.ev("()=>{const b=document.querySelector('#slot .conn .plgb.wmin');return b?+(b.textContent.replace(/[^0-9]/g,'')||-1):null}")
    T(G, u'창 아래 줄 「이 조가 적은 조 = 🔗인 목록 → 본문 속 조 링크」(🔗인 칩 수와 같은 셈)', w.get('foot') == u'이 조가 적은 조 = ' + (u' · '.join(ins) if ins else u'없음') + u' → 본문 속 조 링크' and nin == len(ins), {'꼬리': w.get('foot'), '🔗인': ins, '칩 수': nin})
    p.press(p.J("k=>__WM.ciAt(k)", u'제132조의3'), 'touch', 1200)
    cur = p.J("()=>__WM.cur()")
    pop = p.ev("()=>(typeof POPS!=='undefined'?POPS:[]).some(x=>x.isConnected&&x._pk==='jo|특허법|제132조의3')")   # ★ 9/30 A-6 — joscreen0929 A-3-3: 항목 누름 = 그 조 원문 팝업 · 목록 창 그대로(조 이동은 팝업 머리 「뷰로 이동 ↗」)
    T(G, u'손가락으로 제132조의3 줄 → 제132조의3 원문 팝업 · 인용 창·조문(S.jo) 그대로', pop and cur.get('jo') == u'제140조' and p.J("()=>__WM.ciWin()").get('win'), {'S': cur, '원문 팝업': pop})
    # N = 0 조 — 흐림 · 누름 없음
    z = p.ev("()=>{return get('jo_링크역인덱스.json').then(ix=>get('jo_특허법_본문.json').then(B=>Object.keys(B.조).find(k=>!(ix['특허법:'+k]||[]).length)))}")
    go(p, '특허법', z)
    ch0 = p.J("()=>__WM.ciChip()")
    p.press(ch0, 'mouse', 700)
    T(G, u'「↩피0」(%s) — 지금처럼 누름 없음(cursor default · 창 없음)' % z, ch0.get('cur') == 'default' and not p.J("()=>__WM.ciWin()").get('win'), ch0)   # ★ 9/30 A-6 — joscreen0929 A-3: 0 칩 = 「↩피0」(흐림 · cursor default · 누름 없음)
    T(G + '-헛', u'헛잣대 바탕 — 칩 누름 없음(cursor default · 창 없음)', res['BASE']['chip'].get('cur') == 'default' and not res['BASE']['win'].get('win'), res['BASE'])
    fresh(p); fresh(b)


BR = {}
PARTS = [('w1', g_w1), ('w2', g_w2), ('w3', g_w3), ('w4', g_w4), ('w5', g_w5), ('w6', g_w6), ('w8', g_w8)]


def run_engine(pw, eng):
    br = getattr(pw, eng).launch()
    BR[eng] = br
    (ns, nd, ne), (bs, bd, be) = envs()
    try:
        p = Pg(br, eng, 'wmN', ns, nd, ne)
        b = Pg(br, eng, 'wmB', bs, bd, be)
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
        for k, fn in (('w7', g_w7), ('w3s', g_w3s)):
            if ONLY and k not in ONLY:
                continue
            print('── %s · %s' % (eng, k), flush=True)
            try:
                fn(br, eng)
            except Exception as e:
                T('RUN', u'%s · %s 묶음이 멈춤' % (eng, k), False, repr(e)[:600])
    finally:
        br.close()


def main():
    os.makedirs(M.WORK, exist_ok=True)
    t0 = time.time()
    with sync_playwright() as pw:
        for eng in ENGS:
            RES.append(('ENG', eng, None, ''))
            print('INFO | ENG · %s |' % eng, flush=True)
            run_engine(pw, eng)
    npass = sum(1 for r in RES if r[2] is True); nfail = sum(1 for r in RES if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · %s · NEW %s · 데이터 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), 'wonmun', os.path.basename(_NEW), _DATA, ','.join(ENGS)))
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[ok], g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:600]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
