# -*- coding: utf-8 -*-
"""_task_ox_exview_paper_add2 §E 관문 — 본판 하네스(_harness_ox_exview_paper.py --only a2)가 불러 쓴다.

  NEW   = 본판 하네스 --app(add2 패치 결과)
  BASE3 = genie 9d367aa blob(add1 인도판 · md5 95066d3b) — add2 헛잣대(D-1~D-6 이 FAIL 이어야)
  원격 = SEED 의 __REMOTE_REC(sessionStorage '__hzrem') · 기록.json GET 늦춤 = '__hzdelay' · PUT = __PUTS
  누름 = page.mouse · 폰 = CDP 터치 r22(Chromium) · WebKit = touchscreen.tap
"""
import json, time
import _harness_ox_exview_paper_add1 as A1

BASE3_REV = '9d367aa'
BASE3_MD5 = '95066d3b'
Y1, Y2 = '2020', '2016'
PDF16 = '**/gichul/pdf/2016-1-minbeop.pdf'
DESK = {'width': 1280, 'height': 900}
READY = "typeof buildQuizData==='function'&&!!window.__HZX&&!!window.__HZA&&!!window.__HZB"


def J(x):
    try:
        return json.loads(x) if isinstance(x, str) else x
    except Exception:
        return {'__raw': str(x)[:300]}


def open_wk(M, br, tag, src, vw, touch):
    """WebKit — CDP 가 없다(M.S(pg, True) 가 new_cdp_session 에서 죽는다) · 톡은 pg.touchscreen.tap 으로 직접"""
    url = M.build(tag, src)
    kw = dict(viewport=vw, device_scale_factor=1)
    if touch:
        kw.update(is_mobile=True, has_touch=True, user_agent=M.IPAD_UA)
    ctx = br.new_context(**kw)
    ctx.route('**/*', M.route_filter)
    pg = ctx.new_page()
    pg.set_default_timeout(600000)
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
    pg.goto('http://127.0.0.1:%d%s' % (M.PORT, url), wait_until='load', timeout=180000)
    pg.wait_for_function(READY, timeout=180000)
    return M.S(pg, False), ctx, errs


def fresh(M, br, tag, src, vw=None, touch=False, wk=False):
    if wk:
        return open_wk(M, br, tag, src, vw or DESK, touch)
    s, ctx, errs = A1.open_page2(M, br, tag, src, vw or DESK, touch)
    s.pg.wait_for_function(READY, timeout=180000)
    return s, ctx, errs


def reboot(s):
    """심은 뒤 새로고침 — __hzkeep 이 서 있으니 SEED 가 localStorage 를 안 지운다 ·
       본판 하네스가 window.onload 를 끄므로 앱 onload 와 같은 차례를 __HZB.appBoot 가 부른다(문항 → gkeyBoot → 첫 화면 → recBoot · 뒤 둘은 안 기다림)"""
    s.pg.reload(wait_until='load', timeout=180000)
    s.pg.wait_for_function(READY, timeout=180000)
    return J(s.js("__HZB.appBoot()"))


def poll(s, expr, arg, ms, ok):
    t0 = time.time()
    v = None
    while time.time() - t0 < ms / 1000.0:
        v = J(s.js(expr, arg) if arg is not None else s.js(expr))
        if ok(v):
            return v, time.time() - t0
        s.pg.wait_for_timeout(250)
    return v, None


def d1_run(M, br, tag, src, delay):
    s, ctx, errs = fresh(M, br, tag + '_d1_%d' % delay, src)
    try:
        s.js("__HZB.prep()")
        seed = J(s.js("([y,d])=>__HZB.d1seed(y,d)", [Y1, delay * 1000]))
        boot = reboot(s)
        want = (seed or {}).get('want1')
        # 끝 상태까지 — 바로잡기가 돌고 · 바로잡은 R1 이 원격(마지막 PUT)에 올라갈 때까지(바로잡기 뒤 동기화도 GET 을 늦춘다)
        st, dt = poll(s, "y=>__HZB.d1state(y)", Y1, (2 * delay + 16) * 1000,
                      lambda v: bool(v and v.get('puts')) and bool(v.get('fix')) and (v.get('sync') is None or (v.get('sync') or {}).get('done'))
                      and any(x.get('date') == '2026. 9. 25.' and x.get('ok') == want for x in (v.get('remote') or [])))
        s.pg.wait_for_timeout(1500)
        st = J(s.js("y=>__HZB.d1state(y)", Y1))
        return {'seed': seed, 'boot': boot, 'st': st, 'settle': dt, 'errs': errs[:5], 'has': J(s.js("__HZB.has()"))}
    finally:
        ctx.close()


# ══════════ ★ revfix0928(9/28) A-2 — 받기 실패한 날(ox_exv_fixskip) ══════════
#   원격 흉내 표지(본판 SEED · sessionStorage): __hz500 = 기록.json GET 을 500 · __hzday = 기기 시계 +ms(Date) · __hzoff = navigator.onLine false
def rx_skip_run(M, br, tag, src, how='500', wk=False):
    s, ctx, errs = fresh(M, br, tag + '_rx' + how, src, wk=wk)
    R = {}
    done = lambda v: bool(v and (v.get('sync') or {}).get('done'))
    try:
        s.js("__HZB.prep()")
        R['seed'] = J(s.js("([y,d])=>__HZB.d1seed(y,d)", [Y1, 0]))
        s.js("h=>{sessionStorage.setItem(h==='500'?'__hz500':'__hzoff','1');return 1}", how)
        R['boot1'] = reboot(s)
        poll(s, "y=>__HZB.rxState(y)", Y1, 15000, done)
        s.pg.wait_for_timeout(3500)   # 기출키 뒤 1.5초 exvFixKick 도 지나게
        R['st1'] = J(s.js("y=>__HZB.rxState(y)", Y1))
        # 같은 날 새로고침 — 받기 성공(표지 걷음)
        s.js("()=>{sessionStorage.removeItem('__hz500');sessionStorage.removeItem('__hzoff');return 1}")
        R['boot2'] = reboot(s)
        poll(s, "y=>__HZB.rxState(y)", Y1, 15000, lambda v: done(v) and bool(v.get('puts') or (v.get('sync') or {}).get('ok')))
        s.pg.wait_for_timeout(3500)
        R['st2'] = J(s.js("y=>__HZB.rxState(y)", Y1))
        # 다음 날(기기 시계 +1일) — 돈다
        s.js("()=>{sessionStorage.setItem('__hzday','86400000');return 1}")
        R['boot3'] = reboot(s)
        want = (R['seed'] or {}).get('want1')
        v, dt = poll(s, "y=>__HZB.rxState(y)", Y1, 20000, lambda v: bool(v and v.get('fix')) and any(x.get('ok') == want for x in (v.get('local') or [])))
        s.pg.wait_for_timeout(1500)
        R['st3'] = J(s.js("y=>__HZB.rxState(y)", Y1))
        R['fixT'] = dt
        s.js("()=>{sessionStorage.removeItem('__hzday');return 1}")
        R['errs'] = errs[:5]
        return R
    finally:
        ctx.close()


def runs_skip(M, br, new, base6, say, wk=False):
    t0 = time.time()
    out = {('rxswk' if wk else 'rxs'): {'new': rx_skip_run(M, br, 'rxn', new, '500', wk), 'base': rx_skip_run(M, br, 'rxb', base6, '500', wk),
                                        'off': rx_skip_run(M, br, 'rxo', new, 'off', wk), 'offbase': rx_skip_run(M, br, 'rxob', base6, 'off', wk)}}
    say('  [rx 받기 실패 %s] %.0f초' % ('webkit' if wk else 'chromium', time.time() - t0))
    return out


def gates_skip(RES, add, say):
    for eng in ('rxs', 'rxswk'):
        P = RES.get(eng)
        if not P:
            continue
        E = 'WebKit' if eng == 'rxswk' else 'Chromium'
        for how, nk, bk in ((u'GET 500', 'new', 'base'), (u'오프라인', 'off', 'offbase')):
            n, b = P[nk] or {}, P[bk] or {}
            want = (n.get('seed') or {}).get('want1')
            s1, s2, s3 = n.get('st1') or {}, n.get('st2') or {}, n.get('st3') or {}
            r1 = lambda st: [x for x in (st.get('local') or []) if x.get('date') == '2026. 9. 25.']
            unfixed = lambda st: bool(r1(st)) and all(x.get('ok') != want and not x.get('fixedAt') for x in r1(st)) and not st.get('fix')
            add('RX-2', s1.get('skip') == s1.get('today') and (s1.get('sync') or {}).get('done') and not (s1.get('sync') or {}).get('ok') and unfixed(s1),
                '[%s %s] 받기 실패 → ox_exv_fixskip = 이 기기 날짜(%s) · 바로잡기 안 돎 %s' % (E, how, s1.get('today'), json.dumps({'skip': s1.get('skip'), 'sync': s1.get('sync'), 'R1': r1(s1)}, ensure_ascii=False)))
            add('RX-2', (s2.get('sync') or {}).get('ok') and s2.get('skip') == s2.get('today') and unfixed(s2),
                '[%s %s] 같은 날 새로고침(받기 성공) → 바로잡기 여전히 안 돎 · 회독(R1) 무변 %s' % (E, how, json.dumps({'sync': s2.get('sync'), 'R1': r1(s2), 'fix': s2.get('fix')}, ensure_ascii=False)))
            add('RX-2', s3.get('today') != s1.get('today') and bool(s3.get('fix')) and any(x.get('ok') == want for x in r1(s3)),
                '[%s %s] 기기 날짜 다음 날(%s) → 돈다 · R1 ok = %s %s' % (E, how, s3.get('today'), want, json.dumps({'R1': r1(s3), 'T': n.get('fixT')}, ensure_ascii=False)))
            add('RX-2', s2.get('syncKeys') == -1 and not s2.get('skipInPut') and not s3.get('skipInPut'),
                '[%s %s] ox_exv_fixskip = SYNC_KEYS 밖 · 원격 기록 파일(PUT)에 안 나감 %s' % (E, how, json.dumps({'SYNC 자리': s2.get('syncKeys'), 'PUT 키': s3.get('putKeys')}, ensure_ascii=False)))
            b2 = b.get('st2') or {}
            add('RX-2-헛', bool(b2.get('fix')) or any(x.get('ok') == want for x in r1(b2)),
                '[%s %s] 헛잣대 바탕 — 같은 날 새로고침 뒤 돈다 %s' % (E, how, json.dumps({'R1': r1(b2), 'fix': bool(b2.get('fix'))}, ensure_ascii=False)))
            add('RX-2', not n.get('errs'), '[%s %s] pageerror %s' % (E, how, n.get('errs')))


def d2_run(M, br, tag, src):
    """D-2 · D-3 · D-5 — 2016 PDF 404 → 켜기 → 셈·원격 · 정리 창 칸 → PDF 받음 → 다시 켜기 → 늘면 고침·줄면 목록 · 첫 화면 상자"""
    # 정답은 따로 연 창에서(시험지 색인이 IndexedDB 에 담기므로 시험 창은 PDF 를 한 번도 안 읽은 채 404 로 간다)
    s0, ctx0, _ = fresh(M, br, tag + '_d2ans', src)
    try:
        s0.js("__HZB.prep()")
        A = J(s0.js("y=>__HZB.answers(y)", Y2))
    finally:
        ctx0.close()
    s, ctx, errs = fresh(M, br, tag + '_d2', src)
    R = {'answers': A}
    try:
        s.js("__HZB.prep()")
        R['seed'] = J(s.js("([y,a])=>__HZB.d2seed(y,a)", [Y2, A]))
        ctx.route(PDF16, lambda r: r.fulfill(status=404, body='not found'))
        R['boot1'] = reboot(s)
        R['st1'], _ = poll(s, "y=>__HZB.d2state(y)", Y2, 20000, lambda v: bool(v and v.get('fix')))
        s.pg.wait_for_timeout(2500)
        R['st1'] = J(s.js("y=>__HZB.d2state(y)", Y2))
        R['dash1'] = J(s.js("y=>__HZB.dash(y)", Y2))   # D-3 헛잣대 — 바탕은 바로잡은(깎은) 뒤에도 첫 화면 상자가 옛 수 그대로
        # D-5 정리 창 — 2016 📋 → 1·14·16 칸
        s.js("__HZX.home()")
        btn = J(s.js("([a,b])=>__HZX.jnBtn(a,b)", ['변리사 기출', '2016년']))
        R['jn_open'] = s.at(btn, 900)
        R['cells'] = J(s.js("([y,n])=>__HZA.jxCells(y,n)", [Y2, [1, 14, 16]]))
        A1.close_wins(s)
        # PDF 받음 → 다시 켜기 → 셈(늘면 고침 · 줄면 목록) · 첫 화면 상자(D-3)
        ctx.unroute(PDF16)
        s.js("__HZA.keep()")
        R['boot2'] = reboot(s)
        s.js("__HZX.home()")
        v, dt = poll(s, "y=>__HZB.d2state(y)", Y2, 25000, lambda v: bool(v and v.get('fix')))
        R['st2'] = v
        R['fixT'] = dt
        t0 = time.time()
        d = None
        while time.time() - t0 < 2.5:
            d = J(s.js("y=>__HZB.dash(y)", Y2))
            if d and d.get('boxes') and d['boxes'][:3] == [str(x) for x in (R['seed'] or {}).get('want2', [])]:
                break
            s.pg.wait_for_timeout(150)
        R['dash'] = d
        R['dashT'] = round(time.time() - t0, 2)
        s.pg.wait_for_timeout(800)
        R['st2b'] = J(s.js("y=>__HZB.d2state(y)", Y2))
        R['errs'] = errs[:5]
        return R
    finally:
        ctx.close()


def d4_run(M, br, tag, src, wk=False):
    """D-4 — 전체 채점을 누른 뒤(조합 선지 1.2초 늦춤) 기다리는 동안 40번을 다른 번호로 → 저장된 고른 답"""
    s, ctx, errs = fresh(M, br, tag + '_d4', src, wk=wk)
    R = {}
    try:
        s.js("__HZX.setup()")
        s.js("__HZB.prep()")
        R['open'] = J(s.js("y=>__HZA.open(y)", Y1))
        s.js("([y,a,b])=>__HZA.pickRight(y,a,b)", [Y1, 1, 40])
        right = J(s.js("([y,n])=>__HZB.pickOf(y,n)", [Y1, 40]))
        alt = 2 if right != 2 else 3
        R['right'], R['alt'] = right, alt
        R['page'] = J(s.js("p=>__HZA.goPage(p)", 7))
        s.js("ms=>__HZA.slowIndex(ms)", 1200)
        s.js("y=>__HZA.comboForget(y)", Y1)
        R['press'] = s.press('#action-btn', 0, True, 250)
        at = J(s.js("([y,n,k])=>__HZB.optAt(y,n,k)", [Y1, 40, alt]))
        R['alt_at'] = at
        R['alt_click'] = s.at(at, 100)
        R['mid'] = J(s.js("([y,n])=>__HZB.pickOf(y,n)", [Y1, 40]))
        s.pg.wait_for_timeout(3500)
        R['saved'] = J(s.js("([y,n])=>__HZB.lastPick(y,n)", [Y1, 40]))
        s.js("__HZA.fastIndex()")
        R['errs'] = errs[:5]
        return R
    finally:
        ctx.close()


def d6_run(M, br, tag, src, vw, touch, wk=False):
    s, ctx, errs = fresh(M, br, tag + '_d6_%d' % vw['width'], src, vw, touch, wk)
    R = {}
    try:
        s.js("__HZB.prep()")
        R['open'] = J(s.js("y=>__HZA.open(y)", Y1))
        R['page'] = A1.find_page(s, 24)
        s.pg.wait_for_timeout(400)
        R['sel'] = J(s.js("k=>__HZB.selInfo(k)", Y1 + ':24'))
        e = (R['sel'] or {}).get('empty')
        if e:
            before = J(s.js("([y,n])=>__HZB.pickOf(y,n)", [Y1, 24]))
            if wk:
                s.pg.touchscreen.tap(e['cx'], e['cy'])
                s.pg.wait_for_timeout(300)
                R['emptyTap'] = True
            else:
                R['emptyTap'] = s.at(e, 300)
            R['emptyPick'] = [before, J(s.js("([y,n])=>__HZB.pickOf(y,n)", [Y1, 24]))]
        R['errs'] = errs[:5]
        return R
    finally:
        ctx.close()


def runs(M, br, new, base3, say):
    from playwright.sync_api import sync_playwright   # noqa — 본판이 부른 playwright 안에서 WebKit 을 따로 연다
    out = {}
    for tag, src in (('a2new', new), ('a2base', base3)):
        t0 = time.time()
        r = {'d1': {}}
        for d in (0, 1, 2, 4, 8):
            r['d1'][d] = d1_run(M, br, tag, src, d)
        r['d2'] = d2_run(M, br, tag, src)
        r['d4'] = d4_run(M, br, tag, src)
        r['d6'] = {}
        for w in (390, 768, 1280):
            vw = {'width': w, 'height': 844 if w == 390 else 900}
            r['d6'][w] = d6_run(M, br, tag, src, vw, w == 390)
        out[tag] = r
        say('  [%s] %.0f초' % (tag, time.time() - t0))
    return out


def runs_wk(M, pw, new, base3, say):
    """WebKit — 폰 390(톡) · 책상 D-4"""
    wk = pw.webkit.launch()
    out = {}
    try:
        for tag, src in (('a2wk', new), ('a2wkbase', base3)):
            r = {'d6': d6_run(M, wk, tag, src, {'width': 390, 'height': 844}, True, wk=True), 'd4': d4_run(M, wk, tag, src, wk=True)}
            out[tag] = r
    finally:
        wk.close()
    return out


def gates(RES, add, say):
    N_, B_ = RES.get('a2new') or {}, RES.get('a2base') or {}

    def d1ok(r):
        st = (r or {}).get('st') or {}
        loc = st.get('local') or []
        rem = st.get('remote')
        want = ((r or {}).get('seed') or {}).get('want1')
        has2L = any(x.get('date') == '2026. 9. 26.' for x in loc)
        has2R = rem is not None and any(x.get('date') == '2026. 9. 26.' for x in rem)
        r1 = [x for x in loc if x.get('date') == '2026. 9. 25.']
        fixed = bool(r1) and r1[0].get('ok') == want
        fixedR = rem is not None and any(x.get('date') == '2026. 9. 25.' and x.get('ok') == want for x in rem)
        sa = st.get('syncAt')
        fa = r1[0].get('fixedAt') if r1 else None
        try:
            import datetime
            fam = datetime.datetime.fromisoformat(fa.replace('Z', '+00:00')).timestamp() * 1000 if fa else None
        except Exception:
            fam = None
        after = (sa is None) or (fam is not None and fam >= sa)   # 바탕은 첫 동기화 끝 표시가 없다(차례는 R2 로 가른다)
        return has2L and has2R and fixed and fixedR and after, {'로컬': [(x.get('date'), x.get('ok')) for x in loc], '원격(마지막 PUT)': rem and [(x.get('date'), x.get('ok')) for x in rem],
                                                             'PUT': st.get('puts'), 'R1 바로잡힘(로컬·원격)': [fixed, fixedR], '바로잡은 시각 - 첫 동기화 끝(ms)': (round(fam - sa) if (fam is not None and sa) else None)}

    dn = {d: d1ok(v) for d, v in (N_.get('d1') or {}).items()}
    db = {d: d1ok(v) for d, v in (B_.get('d1') or {}).items()}
    add('D1', dn and all(v[0] for v in dn.values()),
        'D-1 — 원격 [R1, R2] · 이 기기 [R1] · 기록.json GET 0·1·2·4·8초 늦춤 → 로컬·원격 R2 남음 · R1 바로잡힘은 동기화 뒤 %s' % {d: v[1] for d, v in dn.items()})
    add('D1-헛', db and not all(v[0] for v in db.values()),
        '헛잣대(9d367aa) — 늦춤마다 %s' % {d: (v[0], v[1]['로컬'], v[1]['원격(마지막 PUT)']) for d, v in db.items()})
    # D-2
    def d2(r):
        s1, s2 = (r or {}).get('st1') or {}, (r or {}).get('st2') or {}
        return s1, s2
    n1, n2 = d2(N_.get('d2'))
    b1, b2 = d2(B_.get('d2'))
    seed = (N_.get('d2') or {}).get('seed') or {}
    oks0 = seed.get('oks') or []
    ok1 = [x.get('ok') for x in (n1.get('local') or [])] == oks0 and not any(x.get('fixedAt') for x in (n1.get('local') or []))
    rem1 = [[x.get('ok') for x in p] for p in (n1.get('puts') or [])]
    ok1r = all(p == oks0 for p in rem1 if p)
    add('D2', ok1 and ok1r,
        'D-2 — 2016 PDF 404 → 회독 ok %s 그대로 · fixedAt 없음 · 원격(PUT %d 번) 무변 %s · 조합 %s' % (oks0, len(rem1), rem1[-1:] if rem1 else '올림 없음', (n1.get('combos') or [])[:3]))
    L2 = n2.get('local') or []
    want2 = [oks0[0], seed.get('n'), oks0[2]] if len(oks0) == 3 else None
    fix2 = (n2.get('fix') or {})
    want2 = seed.get('want2') or want2
    ok2 = bool(L2) and [x.get('ok') for x in L2] == want2 and L2[1].get('fv') == 2 and not L2[2].get('fixedAt') and len(fix2.get('down') or []) >= 1
    add('D2', ok2, 'D-2 — PDF 받은 뒤 새로고침 → 다시 셈: 늘면 고침(%s → %s · fv 2) · 줄면 목록만(%s) · 셋 = %s' % (oks0[1:2], [x.get('ok') for x in L2][1:2], fix2.get('down'), [x.get('ok') for x in L2]))
    b1L = [x.get('ok') for x in (b1.get('local') or [])]
    add('D2-헛', b1L != oks0, '헛잣대(9d367aa) — PDF 404 에서 %s → %s · fixedAt %s' % (oks0, b1L, [bool(x.get('fixedAt')) for x in (b1.get('local') or [])]))
    # D-3
    d3 = (N_.get('d2') or {}).get('dash') or {}
    add('D3', bool(d3.get('home')) and d3.get('boxes', [])[:3] == [str(x) for x in (want2 or [])] and (N_.get('d2') or {}).get('dashT', 9) <= 2.5,
        'D-3 — 바로잡은 뒤 %s초 안 첫 화면 상자 %s(기대 %s)' % ((N_.get('d2') or {}).get('dashT'), d3.get('boxes'), want2))
    d3b = (B_.get('d2') or {}).get('dash') or {}
    d31 = (B_.get('d2') or {}).get('dash1') or {}
    stale = [str(x) for x in b1L][:3] != (d31.get('boxes') or [])[:3]   # 바탕이 첫 켜기에서 고친 수 ↔ 그때 첫 화면 상자
    add('D3-헛', stale and not (d3b.get('boxes', [])[:3] == [str(x) for x in (want2 or [])]),
        '헛잣대 — 바탕 첫 켜기(PDF 404): 바로잡은 뒤 저장 %s ↔ 2.5초 뒤 첫 화면 상자 %s(옛 수 그대로) · 둘째 켜기 상자 %s' % (b1L, d31.get('boxes'), d3b.get('boxes')))
    # D-4
    d4, d4b = N_.get('d4') or {}, B_.get('d4') or {}
    add('D4', bool(d4.get('press')) and bool(d4.get('alt_click')) and (d4.get('saved') or {}).get('p') == d4.get('alt'),
        'D-4 — 전체 채점 누름 → 기다리는 동안 40번 %s → %s(진짜 누름) → 저장 %s' % (d4.get('right'), d4.get('alt'), d4.get('saved')))
    add('D4-헛', (d4b.get('saved') or {}).get('p') != d4b.get('alt'), '헛잣대 — 바탕 저장 %s(바꾼 답 %s)' % (d4b.get('saved'), d4b.get('alt')))
    # D-5
    c5 = (N_.get('d2') or {}).get('cells') or {}
    ok5 = all(c5.get(str(n)) and c5[str(n)].get('t') == '?' and '정답 조합 선지 못 읽음' in c5[str(n)].get('tip', '') and c5[str(n)].get('vis') for n in (1, 14, 16))
    add('D5', ok5, 'D-5 — PDF 404 · 2016 정리 창 1·14·16 칸 「?」 보임 · tip %s' % {n: (c5.get(str(n)) or {}).get('t') for n in (1, 14, 16)})
    c5b = (B_.get('d2') or {}).get('cells') or {}
    add('D5-헛', not all((c5b.get(str(n)) or {}).get('t') == '?' for n in (1, 14, 16)), '헛잣대 — 바탕 칸 %s' % {n: (c5b.get(str(n)) or {}).get('t') for n in (1, 14, 16)})
    # D-6
    def d6ok(r):
        s_ = (r or {}).get('sel') or {}
        ws = [o['w'] for o in s_.get('opts') or []]
        same = bool(ws) and max(ws) - min(ws) < 1.0
        emp = (r or {}).get('emptyPick')
        return same and s_.get('rows', 0) > 1 and bool(emp) and emp[0] == emp[1], {'폭': ws, '줄': s_.get('rows'), '빈 곳 누름 전후': emp}
    o390 = d6ok((N_.get('d6') or {}).get(390))
    add('D6', o390[0], 'D-6 — 390 · 2020 24번 선지 폭 같음 · 둘째 줄 빈 곳 누름 → 고름 없음 %s' % o390[1])
    b390 = d6ok((B_.get('d6') or {}).get(390))
    add('D6-헛', not b390[0], '헛잣대 — 바탕 390 %s' % b390[1])
    for w in (768, 1280):
        a_ = (((N_.get('d6') or {}).get(w) or {}).get('sel') or {}).get('opts')
        b_ = (((B_.get('d6') or {}).get(w) or {}).get('sel') or {}).get('opts')
        add('D6', bool(a_) and a_ == b_, 'D-6 — %d 폭 24번 선지 자리 = 바탕(한 줄 · 무변) %s' % (w, [(o['x'], o['w']) for o in (a_ or [])]))
    wk, wkb = RES.get('a2wk') or {}, RES.get('a2wkbase') or {}
    if wk:
        o = d6ok(wk.get('d6'))
        add('D6', o[0], 'D-6 WebKit 390 톡 — %s' % o[1])
        add('D6-헛', not d6ok(wkb.get('d6'))[0], '헛잣대 WebKit 바탕 %s' % d6ok(wkb.get('d6'))[1])
        d4w = wk.get('d4') or {}
        add('D4', bool(d4w.get('press')) and bool(d4w.get('alt_click')) and (d4w.get('saved') or {}).get('p') == d4w.get('alt'),
            'D-4 WebKit — 전체 채점 누름 → 기다리는 동안 40번 %s → %s(진짜 누름) → 저장 %s' % (d4w.get('right'), d4w.get('alt'), d4w.get('saved')))
        d4wb = wkb.get('d4') or {}
        add('D4-헛', (d4wb.get('saved') or {}).get('p') != d4wb.get('alt'), '헛잣대 WebKit 바탕 저장 %s(바꾼 답 %s)' % (d4wb.get('saved'), d4wb.get('alt')))
    errs = {k: [(v.get('errs') if isinstance(v, dict) else None)] for k, v in N_.items() if isinstance(v, dict) and 'errs' in v}
    say('       add2 pageerror: %s' % json.dumps(errs, ensure_ascii=False)[:600])
