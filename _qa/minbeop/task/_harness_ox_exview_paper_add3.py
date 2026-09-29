# -*- coding: utf-8 -*-
"""_task_ox_exview_paper_add3 §C 관문 — 본판 하네스(_harness_ox_exview_paper.py --only a3)가 불러 쓴다.

  NEW   = 본판 하네스 --app(add3 패치 결과)
  BASE4 = genie 앞 인도 판 blob(mbsame_add3 판 · ⑩ 띠 고침만 든 민법앱) — add3 헛잣대(C-1·C-2 가 FAIL 이어야)
  판마다 = Chromium 책상(마우스 1280×900) · Chromium 아이패드(CDP 터치 r22 · 1024×768) · WebKit 책상(마우스)
  필터 = 진짜 select(page.select_option — change 이벤트 → onchange="renderDashboard()")
"""
import json, re, time
import _harness_ox_exview_paper_add1 as A1
import _harness_ox_exview_paper_add2 as A2

BASE4_REV = None     # 본판 하네스가 --base4 로 준다(앞 인도 판 커밋)
DESK = {'width': 1280, 'height': 900}
IPAD = {'width': 1024, 'height': 768}
READY = "typeof buildQuizData==='function'&&!!window.__HZX&&!!window.__HZA&&!!window.__HZC"
J = A2.J


def open3(M, br, tag, src, vw, touch, wk):
    if wk:
        s, ctx, errs = A2.open_wk(M, br, tag, src, vw, touch)
    else:
        s, ctx, errs = A1.open_page2(M, br, tag, src, vw, touch)
    s.pg.wait_for_function(READY, timeout=180000)
    return s, ctx, errs


def pick(s, v):
    """진짜 select — playwright 가 고르고 input·change 를 쏜다(앱 onchange = renderDashboard)"""
    s.pg.select_option('#review-filter', v)
    s.pg.wait_for_timeout(500)
    return J(s.js("__HZC.filterVal()"))


def flow(M, br, tag, src, vw, touch, wk=False):
    s, ctx, errs = open3(M, br, tag, src, vw, touch, wk)
    R = {'has': None}
    try:
        R['setup'] = J(s.js("__HZX.setup()"))
        s.js("__HZB.prep()")
        R['has'] = J(s.js("__HZC.has()"))
        # ── C-1 서랍 해 차례 — 첫 화면 2026 줄 「N회독」 진짜 누름 → 기출뷰 → 서랍
        s.js("__HZX.home()")
        R['enter'] = s.press('[data-trrow*="2026년"] button[onclick^="startQuiz"]', 0, False, 1500)
        s.pg.wait_for_timeout(800)
        R['drQuiz'] = J(s.js("__HZC.drawer()"))
        # 첫 화면 — 서랍 머리 「변리사 기출」 진짜 누름 → 서랍 해 차례 · 첫 화면 해 차례
        s.js("__HZX.home()")
        s.pg.wait_for_timeout(400)
        R['dash'] = J(s.js("__HZC.dashYears()"))
        R['hbEx'] = s.at(J(s.js("n=>__HZC.headBtn(n)", '변리사 기출')), 400)
        R['drHome'] = J(s.js("__HZC.drawer()"))
        R['hbMin'] = s.at(J(s.js("n=>__HZC.headBtn(n)", '민법총칙')), 400)
        R['drMin'] = J(s.js("__HZC.drawer()"))
        # ── C-2 정리 창 거름
        R['seed'] = J(s.js("__HZC.seed()"))
        R['f1'] = pick(s, 'fake')
        b = J(s.js("([a,b])=>__HZC.jnBtnKey(a,b)", ['민법총칙', '1.1']))
        R['btnF'] = b
        R['openF'] = s.at(b, 700)
        R['winF'] = J(s.js("__HZC.win()"))
        R['f0'] = pick(s, 'all')                    # 떠 있는 창이 따라 바뀌는가
        R['win0'] = J(s.js("__HZC.win()"))
        R['fC'] = pick(s, 'concept')                # 1.1 묶음 💡 개념 0 → 빈 거름 글
        R['winC'] = J(s.js("__HZC.win()"))
        s.js("__HZC.closeWins()")
        # 기출 해 — 페이크 → 2026 📋(진짜 누름) → 「문제 N」 = 심은 한 문번
        R['f2'] = pick(s, 'fake')
        b2 = J(s.js("y=>__HZC.jnBtnYear(y)", '2026'))
        R['btnY'] = b2
        R['openY'] = s.at(b2, 900)
        R['winY'] = J(s.js("__HZC.win()"))
        R['f3'] = pick(s, 'all')
        R['winY0'] = J(s.js("__HZC.win()"))
        s.js("__HZC.closeWins()")
        # 필터를 안 건 채 연 창 = 옛 판과 같은가(1.1 · 행 · 머리)
        b3 = J(s.js("([a,b])=>__HZC.jnBtnKey(a,b)", ['민법총칙', '1.1']))
        R['open0'] = s.at(b3, 700)
        R['win00'] = J(s.js("__HZC.win()"))
        s.js("__HZC.closeWins()")
        R['errs'] = errs[:5]
        R['miss'] = s.miss[:6]
        return R
    finally:
        ctx.close()


def runs(M, br, new, base4, say):
    out = {}
    for tag, src in (('a3new', new), ('a3base', base4)):
        t0 = time.time()
        out[tag] = {'desk': flow(M, br, tag + '_desk', src, DESK, False), 'ipad': flow(M, br, tag + '_ipad', src, IPAD, True)}
        say('  [%s] %.0f초' % (tag, time.time() - t0))
    return out


def runs_wk(M, pw, new, base4, say):
    wk = pw.webkit.launch()
    out = {}
    try:
        for tag, src in (('a3wk', new), ('a3wkbase', base4)):
            t0 = time.time()
            out[tag] = {'desk': flow(M, wk, tag + '_desk', src, DESK, False, wk=True)}
            say('  [%s] %.0f초' % (tag, time.time() - t0))
    finally:
        wk.close()
    return out


def c1(r):
    """C-1 — 기출뷰 서랍 첫 해 줄 = 2026 제63회 · 서랍 해 차례 = 첫 화면 해 차례(최신부터) · 민법총칙 서랍 줄"""
    q, h, d = r.get('drQuiz') or {}, r.get('drHome') or {}, r.get('dash') or []
    first = dict(q.get('first') or {})
    first['t'] = re.sub(u'^[▾▸\\s]+', '', first.get('t') or '')   # 장 줄 글 앞 접기 화살표(▾/▸)는 빼고 맞댄다
    yrs = [int(x[:4]) for x in (q.get('it') or []) if x[:4].isdigit()]
    ok = (bool(r.get('enter')) and q.get('onQuiz') and q.get('subj') == '변리사 기출' and first.get('t', '').startswith('2026년 제63회') and first.get('vis')
          and yrs == sorted(yrs, reverse=True) and bool(yrs) and h.get('it') == d and q.get('it') == d)
    return ok, {'진입': r.get('enter'), '서랍 과목': q.get('subj'), '첫 줄': first, '서랍 해(앞 5)': (q.get('it') or [])[:5], '첫 화면 해(앞 5)': d[:5],
                '서랍 = 첫 화면': [q.get('it') == d, h.get('it') == d], '줄 수': [len(q.get('it') or []), len(d)], '최신부터': yrs == sorted(yrs, reverse=True)}


def c2(r, base=False):
    s_, wf, w0, wc, wy, wy0, w00 = (r.get(k) or {} for k in ('seed', 'winF', 'win0', 'winC', 'winY', 'winY0', 'win00'))
    in11 = s_.get('in11') or []
    n = s_.get('n')
    okF = (bool(r.get('openF')) and wf.get('vis') and sorted(wf.get('rows') or []) == sorted(in11) and ('거름 ⚠️ 페이크 %d' % len(in11)) in (wf.get('sub') or '')
           and ('%d문항' % n) in (wf.get('sub') or ''))
    ok0 = w0.get('vis') and w0.get('n') == n and '거름' not in (w0.get('sub') or '')
    okC = bool((wc.get('empty') or {}).get('vis')) and (wc.get('empty') or {}).get('t') == '이 거름에 맞는 문항이 없다' and wc.get('n') == 0 and '거름 💡 개념 0' in (wc.get('sub') or '')
    y26, nos = s_.get('y26') or [], s_.get('nos26') or []
    okY = (bool(r.get('openY')) and wy.get('vis') and bool(y26) and sorted(wy.get('rows') or []) == sorted(y26) and wy.get('jx') == nos
           and ('거름 ⚠️ 페이크 %d' % len(y26)) in (wy.get('sub') or '') and any(h.endswith('%d문항 · %d지문' % (len(nos), len(y26))) for h in (wy.get('heads') or [])))
    okY0 = wy0.get('vis') and (wy0.get('n') or 0) > 100 and len(wy0.get('jx') or []) == 40 and '거름' not in (wy0.get('sub') or '')
    ok00 = w00.get('n') == n and '거름' not in (w00.get('sub') or '') and not w00.get('empty')
    info = {'심음': s_.get('seeded'), '1.1 묶음': s_.get('per'), '📋 누름': [r.get('openF'), r.get('openY')],
            '페이크 창': {'행': wf.get('rows'), '부제': wf.get('sub'), '머리': wf.get('heads')}, '필터 없음 → 떠 있는 창': {'행 수': w0.get('n'), '부제': w0.get('sub')},
            '💡 개념 → 빈 거름': {'글': (wc.get('empty') or {}).get('t'), '부제': wc.get('sub')},
            '2026 페이크': {'행': wy.get('rows'), '문제 N': wy.get('jx'), '부제': wy.get('sub'), '머리': wy.get('heads')},
            '2026 필터 없음': {'행 수': wy0.get('n'), '문제 N 수': len(wy0.get('jx') or []), '부제': wy0.get('sub')},
            '필터 없이 연 창': {'행 수': w00.get('n'), '부제': w00.get('sub')}}
    return (okF, ok0, okC, okY, okY0, ok00), info


def gates(RES, add, say):
    rows = [('Chromium 책상', 'a3new', 'desk', 'a3base'), ('Chromium 아이패드(터치 r22)', 'a3new', 'ipad', 'a3base'), ('WebKit 책상', 'a3wk', 'desk', 'a3wkbase')]
    for nm, tn, k, tb in rows:
        N_ = (RES.get(tn) or {}).get(k)
        B_ = (RES.get(tb) or {}).get(k)
        if not N_:
            add('X3', False, 'add3 %s 판 없음' % nm)
            continue
        ok, info = c1(N_)
        add('X3-1', ok, '[%s] 서랍 해 차례 — 기출뷰 2026 서랍 첫 줄 「2026년 제63회」 보임 · 서랍 해 = 첫 화면 해(최신부터) %s' % (nm, json.dumps(info, ensure_ascii=False)))
        mn = (N_.get('drMin') or {}).get('it')
        mb = ((B_ or {}).get('drMin') or {}).get('it')
        add('X3-1', bool(N_.get('hbMin')) and bool(mn) and mn == mb, '[%s] 민법총칙 서랍 줄 차례 = 바탕(무변) %d줄 · 첫 줄 %s' % (nm, len(mn or []), (mn or [None])[0]))
        if B_:
            okb, infob = c1(B_)
            fb = ((B_.get('drQuiz') or {}).get('first') or {}).get('t')
            add('X3-1-헛', not okb, '[%s] 헛잣대 바탕 — 서랍 첫 줄 %s · 서랍 해(앞 5) %s' % (nm, fb, infob.get('서랍 해(앞 5)')))
        oks, info2 = c2(N_)
        lab = ('1.1 페이크 창 = 심은 둘 · 부제 「거름 ⚠️ 페이크 2」', '필터 없음 → 떠 있는 창 묶음 전부', '💡 개념 → 「이 거름에 맞는 문항이 없다」',
               '2026 📋 페이크 → 심은 한 지문 · 「문제 N」 하나', '2026 필터 없음 → 40 문번', '필터 없이 연 창 = 묶음 전부(옛 판과 같음)')
        for o, l in zip(oks, lab):
            add('X3-2', bool(o), '[%s] %s' % (nm, l))
        say('       [%s] add3 정리 창 %s' % (nm, json.dumps(info2, ensure_ascii=False)[:1500]))
        if B_:
            w0n, w0b = N_.get('win00') or {}, B_.get('win00') or {}
            add('X3-2', bool(w0n.get('rows')) and w0n.get('rows') == w0b.get('rows') and w0n.get('heads') == w0b.get('heads') and w0n.get('sub') == w0b.get('sub'),
                '[%s] 필터 없이 연 1.1 창 = 바탕과 같음(행 %s · 머리 %s · 부제 「%s」)' % (nm, w0n.get('n'), w0n.get('heads'), w0n.get('sub')))
            ob, infob2 = c2(B_, True)
            wf = (B_.get('winF') or {})
            add('X3-2-헛', not ob[0] and not ob[3], '[%s] 헛잣대 바탕 — 페이크 창 행 %s(심은 것 %s) · 부제 %s · 2026 페이크 창 행 %s' % (
                nm, wf.get('n'), len((B_.get('seed') or {}).get('in11') or []), wf.get('sub'), (B_.get('winY') or {}).get('n')))
        add('X3', not N_.get('errs'), '[%s] pageerror %s · 누름 못함 %s' % (nm, N_.get('errs'), N_.get('miss')))
