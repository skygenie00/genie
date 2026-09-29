# -*- coding: utf-8 -*-
"""_task_ox_exview_paper_add1 §F 관문 — 본판 하네스(_harness_ox_exview_paper.py)가 불러 쓴다(판 돌리기 · 게이트).

  NEW   = 본판 하네스 --app(add1 패치 결과)
  BASE2 = genie 0d4144c blob(본판 인도판 · md5 526d944d) — add1 헛잣대(A1~A8 이 FAIL 이어야 · A9 는 같아야)
  판 = 책상(1280×900 · page.mouse) · 아이패드(1024×768 · CDP 터치 r22) · 폰(390×844 · CDP 터치)
  새로고침 = sessionStorage '__hzkeep' → reload(SEED 가 localStorage 를 안 지운다) → __HZA.boot2()
"""
import json

BASE2_REV = '0d4144c'
BASE2_MD5 = '526d944d'
NOS20 = [3, 5, 23, 24, 27, 33, 37]   # 2020 조합형 Y(지시서 D2)


def open_page2(M, br, tag, src, vw, touch):
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
    pg.wait_for_function("typeof buildQuizData==='function'&&!!window.__HZX&&!!window.__HZA", timeout=180000)
    return M.S(pg, touch), ctx, errs


def reload(s):
    s.js("__HZA.keep()")
    s.pg.reload(wait_until='load', timeout=180000)
    s.pg.wait_for_function("typeof buildQuizData==='function'&&!!window.__HZX&&!!window.__HZA", timeout=180000)
    return s.js("__HZA.boot2()")


def close_wins(s):
    s.js("()=>{document.querySelectorAll('.oxwin').forEach(w=>w.remove());return 1}")


def find_page(s, no):
    for p in range(8):
        r = s.js("p=>__HZA.goPage(p)", p) or {}
        if no in (r.get('nos') or []):
            return p
    return None


def a1_flow(s, R, pre):
    """2020 1번 — 채점 전 ▸ → 해설 보임 · O·X 안 보임 · 「그 자리」를 눌러도 기록 0 · 채점 뒤 O → 기록 1"""
    W = s.pg.wait_for_timeout
    R[pre + 'clean'] = s.js("k=>__HZA.a1clean(k)", '2020:1')   # 실물 기록에 이미 있는 키를 비운다(없으면 새 키 셈이 거저 0)
    s.js("y=>__HZA.open(y)", '2020')
    R[pre + '0'] = s.js("k=>__HZA.a1(k)", '2020:1')
    R[pre + 'peek'] = s.press('#quiz-container .exv-q[data-exq="2020:1"] .exv-peek')
    W(300)
    R[pre + '1'] = s.js("k=>__HZA.a1(k)", '2020:1')
    ids = (R[pre + '1'] or {}).get('ids') or []
    x = ids[0] if ids else None
    R[pre + 'x'] = x
    if x:
        # 그 자리 — 새 판 = 「채점 전」 한 줄(O·X 줄 자리) · 바탕 = 보이는 O 단추
        R[pre + 'try'] = s.press('#q-box-%s .exv-pre' % x) or s.press('#ox-O-%s' % x)
        W(300)
        R[pre + '2'] = s.js("k=>__HZA.a1(k)", '2020:1')
    s.js("([y,a,b])=>__HZA.pickRight(y,a,b)", ['2020', 1, 5])
    s.press('button[onclick="openOmrPad()"]')
    W(300)
    R[pre + 'grade'] = s.press('#oxwin-omr .exv-omr-foot button')
    W(2600)   # 조합 선지 읽기 최대 2초 + 그리기
    close_wins(s)
    R[pre + '3'] = s.js("k=>__HZA.a1(k)", '2020:1')
    if x:
        R[pre + 'o'] = s.press('#ox-O-%s' % x)
        W(300)
        R[pre + '4'] = s.js("k=>__HZA.a1(k)", '2020:1')


def run_desk(M, br, tag, src):
    s, ctx, errs = open_page2(M, br, tag, src, {'width': 1280, 'height': 900}, False)
    R = {'errs': errs}
    W = s.pg.wait_for_timeout
    R['setup'] = s.js("__HZX.setup()")
    R['ver'] = s.js("__HZA.ver()")
    # ── A1
    a1_flow(s, R, 'a1_')
    # ── A8 책상 무변 — 1280 에서 2020 24번 선지 다섯 자리(선지 줄 기준) · 바탕과 같아야 한다
    p24 = find_page(s, 24)
    R['a8d_page'] = p24
    R['a8d'] = s.js("k=>__HZA.a8(k)", ['2020:24'])
    # ── A2 전체 채점 새로고침 — 2020 40 문항 다 맞게(준비) → 새로고침 → 마지막 쪽만 → 「전체 채점 ✓」(진짜 클릭)
    s.js("([y,a,b])=>__HZA.pickRight(y,a,b)", ['2020', 1, 40])
    R['a2_boot'] = reload(s)
    s.js("y=>__HZA.open(y)", '2020')
    R['a2_forget'] = s.js("y=>__HZA.comboForget(y)", '2020')
    R['a2_page'] = s.js("p=>__HZA.goPage(p)", 7)
    R['a2_pill'] = s.js("__HZA.pill()")
    R['a2_press'] = s.press('#action-btn', 0, True, 600)
    W(2600)
    R['a2_rounds'] = s.js("y=>__HZA.rounds(y)", '2020')
    R['a2_null'] = s.js("y=>__HZA.resNull(y)", '2020')
    # ── A3 읽는 중 막기 — 시험지 색인 3초 늦춤 → 전체 채점 → 저장 0 · 토스트 → 3초 뒤 다시 → 저장 40
    s.js("y=>__HZA.regradeReady(y)", '2020')
    s.js("ms=>__HZA.slowIndex(ms)", 3000)
    s.js("y=>__HZA.comboForget(y)", '2020')
    R['a3_page'] = s.js("p=>__HZA.goPage(p)", 7)
    s.js("y=>__HZA.comboForget(y)", '2020')
    R['a3_r0'] = s.js("y=>__HZA.rounds(y)", '2020')
    R['a3_pill'] = s.js("__HZA.pill()")
    R['a3_press1'] = s.press('#action-btn', 0, True, 200)
    W(2300)
    R['a3_r1'] = s.js("y=>__HZA.rounds(y)", '2020')
    R['a3_toast'] = s.js("__HZA.toast()")
    W(3200)
    R['a3_press2'] = s.press('#action-btn', 0, True, 200)
    W(2600)
    R['a3_r2'] = s.js("y=>__HZA.rounds(y)", '2020')
    s.js("__HZA.fastIndex()")
    # ── A4 정리 창 칸 — 새 세션 · 2020 📋 → 조합형 Y 일곱 칸 O · 「정답」 tip · 24번 칸 누름 → 출처
    R['a4_boot'] = reload(s)
    s.js("__HZX.home()")
    R['a4_btn'] = s.js("([a,b])=>__HZX.jnBtn(a,b)", ['변리사 기출', '2020년'])
    R['a4_open'] = s.at(R['a4_btn'], 800)
    R['a4'] = s.js("([y,n])=>__HZA.jxCells(y,n)", ['2020', NOS20])
    ncell = s.js("()=>document.querySelectorAll('.jx-no[data-jxno=\"24\"] .jx-cell').length")
    R['a4_ncell'] = ncell
    R['a4_tap'] = s.press('.jx-no[data-jxno="24"] .jx-cell', max(0, (ncell if isinstance(ncell, int) else 1) - 1))
    R['a4_info'] = s.js("n=>__HZA.jxInfo(n)", 24)
    close_wins(s)
    # ── A5 옛 회독 바로잡기 — 34/40 으로 심음 → 켜기 → 40/40 · fixedAt → 다시 켜기 → 무변
    s.js("([y,o])=>__HZA.seedOld(y,o)", ['2020', 34])
    # add2(9/27) — 토큰 기기의 바로잡기는 첫 동기화가 끝난 뒤(add2 §A-1). 본판 하네스가 onload 를 꺼 「켜기」에 첫 동기화가 없었다 →
    #   앱 onload 처럼 recBoot(첫 syncRecords)까지 부른다(바탕 0d4144c 도 같은 길 · 바로잡기가 없어 34 그대로 = 헛잣대 무변)
    BOOTSYNC = "()=>{try{recBoot();}catch(e){}return 1}"
    R['a5_boot1'] = reload(s)
    s.js(BOOTSYNC)
    R['a5_fix1'] = s.js("__HZA.fixWait()")
    R['a5_r1'] = s.js("y=>__HZA.rounds(y)", '2020')
    R['a5_boot2'] = reload(s)
    s.js(BOOTSYNC)
    R['a5_fix2'] = s.js("__HZA.fixWait()")
    R['a5_r2'] = s.js("y=>__HZA.rounds(y)", '2020')
    # ── A6 × 동기화 — 2026 1번 ㄱ: 회독 두 칸(9/20 O · 9/25 X) · 원격 = 지금 기록 → 둘째 칸 × 두 번 → 동기화 한 바퀴
    s.js("y=>__HZA.open(y)", '2026')
    R['a6_prep'] = s.js("__HZA.a6prep()")
    X = (R['a6_prep'] or {}).get('X')
    s.js("([y,a,b])=>__HZA.pickRight(y,a,b)", ['2026', 1, 5])
    s.press('button[onclick="openOmrPad()"]')
    W(300)
    s.press('#oxwin-omr .exv-omr-foot button')
    W(2600)
    close_wins(s)
    if X:
        R['a6_open'] = s.press('#q-box-%s button[onclick^="recStripToggle"]' % X)
        R['a6_cell'] = s.press('#rec-strip-%s .rec-cell[data-kind="hist"][data-n="2"]' % X)
        R['a6_x1'] = s.press('#rec-strip-%s .rec-del' % X)
        R['a6_x2'] = s.press('#rec-strip-%s .rec-del' % X)
        R['a6'] = s.js("x=>__HZA.a6state(x)", X)
    # ── A7 시계(1280) — 0 · 흐름 · 멈춤(≠0)
    a7_flow(s, R, 'a7d_')
    # ── A9 기출뷰 밖 카드 — 단원 풀기 첫 카드 「정답·해설 ▸」 → O
    u = s.js("s=>__HZA.unitOpen(s)", '민법총칙')
    R['a9_u'] = u
    uid = (u or {}).get('id')
    if uid:
        R['a9_peek'] = s.press('#peek-btn-%s' % uid)
        W(300)
        R['a9_o'] = s.press('#ox-O-%s' % uid)
        W(300)
        R['a9'] = s.js("i=>__HZA.unitState(i)", uid)
    R['err'] = s.js("__HZX.err()")
    R['miss'] = s.miss
    ctx.close()
    return R


def a7_flow(s, R, pre):
    W = s.pg.wait_for_timeout
    s.js("y=>__HZA.open(y)", '2026')
    s.js("([y,t,r])=>__HZA.timerSet(y,t,r)", ['2026', 0, False])
    s.press('button[onclick="openOmrPad()"]')
    W(400)
    R[pre + 'zero'] = s.js("__HZA.a7()")
    R[pre + 'go'] = s.press('#exv-timer .exv-t-go')
    W(1300)
    R[pre + 'run'] = s.js("__HZA.a7()")
    R[pre + 'stop'] = s.press('#exv-timer .exv-t-go')
    W(400)
    R[pre + 'stopped'] = s.js("__HZA.a7()")
    close_wins(s)


def run_ipad(M, br, tag, src):
    s, ctx, errs = open_page2(M, br, tag, src, {'width': 1024, 'height': 768}, True)
    R = {'errs': errs}
    R['setup'] = s.js("__HZX.setup()")
    a1_flow(s, R, 'a1t_')
    R['err'] = s.js("__HZX.err()")
    R['miss'] = s.miss
    ctx.close()
    return R


def run_phone(M, br, tag, src):
    s, ctx, errs = open_page2(M, br, tag, src, {'width': 390, 'height': 844}, True)
    R = {'errs': errs}
    R['setup'] = s.js("__HZX.setup()")
    a7_flow(s, R, 'a7p_')
    # ── A8 — 2020 조합형 일곱 문항 전부(쪽을 넘기며) · 선지 글 한 줄 · 겹침 0 · 선지 줄 밖 0 · 보임 · 가로 굴림 0
    s.js("y=>__HZA.open(y)", '2020')
    a8, pages = {}, {}
    for p in range(8):
        r = s.js("p=>__HZA.goPage(p)", p) or {}
        ks = ['2020:%d' % n for n in (r.get('nos') or []) if n in NOS20]
        if not ks:
            continue
        m = s.js("k=>__HZA.a8(k)", ks) or {}
        a8['__doc%d' % p] = m.pop('__doc', None)
        a8.update(m)
        pages[p] = ks
    R['a8'], R['a8_pages'] = a8, pages
    R['err'] = s.js("__HZX.err()")
    R['miss'] = s.miss
    ctx.close()
    return R


def runs(M, br, new, base2, say):
    import time
    out = {}
    for tag, src in (('a1new', new), ('a1base', base2)):
        for kind, fn in (('desk', run_desk), ('ipad', run_ipad), ('phone', run_phone)):
            t0 = time.time()
            out['%s_%s' % (tag, kind)] = fn(M, br, '%s_%s' % (tag, kind), src)
            r = out['%s_%s' % (tag, kind)]
            say('  [%s %s] %.0f초 · pageerror %d · 누름 못함 %d' % (tag, kind, time.time() - t0, len(r.get('errs') or []), len(r.get('miss') or [])))
    return out


# ══════════════════════════ 판정 ══════════════════════════
def _a1(R, pre):
    b1, b2, b3, b4 = (R.get(pre + k) or {} for k in ('1', '2', '3', '4'))
    it1 = (b1.get('items') or [{}])[0]
    it2 = (b2.get('items') or [{}])[0]
    it4 = (b4.get('items') or [{}])[0]
    ok_pre = bool(R.get(pre + 'peek')) and it1.get('exp') is True and it1.get('ox') is False and it1.get('pre') is True
    ok_zero = (R.get(pre + 'clean') or {}).get('left') == 0 and it1.get('qh') is False and b2.get('qhN') == b1.get('qhN') and it2.get('qh') is False
    ok_post = b3.get('res') not in ('undef', None) and ((b3.get('items') or [{}])[0]).get('ox') is True and bool(R.get(pre + 'o')) and it4.get('qh') is True and b4.get('qhN') == b3.get('qhN') + 1
    msg = ('▸ 뒤 해설 %s · O·X 줄 %s · 「채점 전」 %s → 그 자리 누름 뒤 새 기록 %s → 채점 %s → O 누름 → 기록 %s'
           % (it1.get('exp'), it1.get('ox'), it1.get('pre'), (b2.get('qhN') or 0) - (b1.get('qhN') or 0), b3.get('res'), (b4.get('qhN') or 0) - (b3.get('qhN') or 0)))
    return ok_pre and ok_zero and ok_post, ok_zero, msg


def _a7(R, pre):
    out, oks = {}, []
    for st in ('zero', 'run', 'stopped'):
        a = R.get(pre + st) or {}
        parts = [a.get('go'), a.get('v')] + ([a.get('rs')] if st == 'stopped' else [])
        ok = bool(a) and all(p and p.get('in') and p.get('vis') and p.get('hit') for p in parts) and a.get('inTitle') is False
        oks.append(ok)
        out[st] = {'state': a.get('state'), 'go': (a.get('go') or {}).get('hit'), 'v': (a.get('v') or {}).get('vis'), 'rs': (a.get('rs') or {}).get('hit') if a.get('rs') else None, 'inTitle': a.get('inTitle'), 'headW': a.get('headW')}
    return all(oks), oks, out


def gates(RES, add, say):
    N_, B_ = RES.get('a1new_desk') or {}, RES.get('a1base_desk') or {}
    NI, BI = RES.get('a1new_ipad') or {}, RES.get('a1base_ipad') or {}
    NP, BP = RES.get('a1new_phone') or {}, RES.get('a1base_phone') or {}
    say('— add1(§F) · NEW = 패치 · BASE2 = %s(%s)' % (BASE2_REV, BASE2_MD5))
    say('       NEW 판 %s · BASE2 판 %s' % (N_.get('ver'), B_.get('ver')))
    # A1
    ok, _, msg = _a1(N_, 'a1_')
    add('A1', ok, '[책상] 2020 1번 「정답·해설 ▸」 page.mouse — ' + msg)
    ok, _, msg = _a1(NI, 'a1t_')
    add('A1', ok, '[아이패드 · 손가락] 같은 흐름 — ' + msg)
    okb, okz, msg = _a1(B_, 'a1_')
    bi1 = ((B_.get('a1_1') or {}).get('items') or [{}])[0]
    bi2 = ((B_.get('a1_2') or {}).get('items') or [{}])[0]
    nb = ((B_.get('a1_2') or {}).get('qhN') or 0) - ((B_.get('a1_1') or {}).get('qhN') or 0)
    add('A1', bi1.get('qh') is False and bi2.get('qh') is True and nb == 1,   # 헛패스 막기 — 「안 막힘」을 양(+)으로 본다(키 없음 → 채점 전 누름 → 키 1)
        '헛잣대 — 바탕(%s): 채점 전 ▸ 뒤 O 누름 → ox_q_history 새 키 %s(그 지문 %s → %s) — %s' % (BASE2_REV, nb, bi1.get('qh'), bi2.get('qh'), msg))
    # A2
    def last(rs):
        return (rs or [{}])[-1] if isinstance(rs, list) and rs else {}
    la = last(N_.get('a2_rounds'))
    add('A2', la.get('ok') == 40 and la.get('n') == 40 and N_.get('a2_null') == [] and bool(N_.get('a2_press')),
        '2020 40 다 맞게 → 새로고침 → 마지막 쪽만(그 해 조합 선지 비움) → 「전체 채점 ✓」 page.mouse → 회독 %s/%s · 「정답 못 정함」 %s · 알약 %s'
        % (la.get('ok'), la.get('n'), N_.get('a2_null'), (N_.get('a2_pill') or {}).get('txt')))
    lb = last(B_.get('a2_rounds'))
    add('A2', lb.get('ok') != 40, '헛잣대 — 바탕 회독 %s/%s · 못 정함 %s' % (lb.get('ok'), lb.get('n'), B_.get('a2_null')))
    # A3
    r0, r1, r2 = (len(N_.get(k) or []) for k in ('a3_r0', 'a3_r1', 'a3_r2'))
    t = N_.get('a3_toast') or {}
    add('A3', bool(N_.get('a3_press1')) and r1 == r0 and t.get('vis') and '조합 선지 읽는 중' in (t.get('txt') or '')
        and bool(N_.get('a3_press2')) and r2 == r0 + 1 and last(N_.get('a3_r2')).get('ok') == 40,
        '시험지 색인 3초 늦춤 → 전체 채점 → 저장 %d · 토스트 「%s」 %s → 3초 뒤 다시 → 저장 %d · %s/40' % (r1 - r0, t.get('txt'), t.get('vis'), r2 - r1, last(N_.get('a3_r2')).get('ok')))
    b0, b1 = (len(B_.get(k) or []) for k in ('a3_r0', 'a3_r1'))
    add('A3', b1 != b0, '헛잣대 — 바탕은 첫 누름에 바로 저장(%d) · %s/40' % (b1 - b0, last(B_.get('a3_r1')).get('ok')))
    # A4
    c = N_.get('a4') or {}
    okc = {n: (c.get(str(n)) or {}) for n in NOS20}
    info = (N_.get('a4_info') or {})
    tip24 = (okc.get(24) or {}).get('tip') or ''
    add('A4', bool(N_.get('a4_open')) and all(v.get('t') == 'O' and '정답' in (v.get('tip') or '') and v.get('vis') for v in okc.values())
        and bool(N_.get('a4_tap')) and info.get('vis') is True and '정답' in (info.get('txt') or '') and info.get('txt') == tip24,
        '새 세션 2020 📋 → 조합형 Y 칸 %s · 24번 마지막 칸(%s칸) 누름 → 출처 보임 %s 「%s」(칸 tip 과 같음 %s)'
        % ({n: v.get('t') for n, v in okc.items()}, N_.get('a4_ncell'), info.get('vis'), info.get('txt'), info.get('txt') == tip24))
    cb = B_.get('a4') or {}
    add('A4', any(((cb.get(str(n)) or {}).get('t')) != 'O' for n in NOS20), '헛잣대 — 바탕 칸 %s' % {n: (cb.get(str(n)) or {}).get('t') for n in NOS20})
    # A5
    f1, r5a, r5b, f2 = N_.get('a5_fix1') or {}, (N_.get('a5_r1') or [{}])[0], (N_.get('a5_r2') or [{}])[0], N_.get('a5_fix2') or {}
    add('A5', r5a.get('ok') == 40 and bool(r5a.get('fixedAt')) and f1.get('fixed') == 1 and r5b.get('ok') == 40 and r5b.get('fixedAt') == r5a.get('fixedAt') and f2.get('fixed') == 0,
        '34/40 으로 심은 회독 → 켜기 → %s/40 · fixedAt %s · 고친 %s → 두 번째 켜기 → %s · 고친 %s' % (r5a.get('ok'), bool(r5a.get('fixedAt')), f1.get('rows'), r5b.get('ok'), f2.get('fixed')))
    add('A5', ((B_.get('a5_r2') or [{}])[0]).get('ok') == 34, '헛잣대 — 바탕 켜기 두 번 뒤 %s/40' % ((B_.get('a5_r2') or [{}])[0]).get('ok'))
    # A6
    a6, b6 = N_.get('a6') or {}, B_.get('a6') or {}
    add('A6', bool(N_.get('a6_x2')) and a6.get('qh') is True and a6.get('put') is True and a6.get('weak') is False and (a6.get('puts') or 0) >= 1,
        '2026 1번 ㄱ 회독 두 칸(9/20 O · 9/25 X) · 원격 = 지금 기록 → 둘째 칸 × 두 번 → 동기화 뒤 ox_q_history %s · 원격 사본 %s · 약점 큐 %s · 도장 %s → %s'
        % (a6.get('qh'), a6.get('put'), a6.get('weak'), (N_.get('a6_prep') or {}).get('stamp'), a6.get('stamp')))
    add('A6', b6.get('qh') is False, '헛잣대 — 바탕은 옛 값 되돌아옴 ox_q_history %s · 원격 %s' % (b6.get('qh'), b6.get('put')))
    # A7
    okd, _, od = _a7(N_, 'a7d_')
    okp, _, op = _a7(NP, 'a7p_')
    add('A7', okd, '[1280] 시계 ▶·숫자·↺ 가 창 제목 줄 안 · 안 잘림 · 그 자리 맨 위 = 그 단추(0 · 흐름 · 멈춤) %s' % od)
    add('A7', okp, '[390] 같은 것 %s' % op)
    _, oksd, bd = _a7(B_, 'a7d_')
    _, oksp, bp = _a7(BP, 'a7p_')
    add('A7', not oksd[2] or not oksp[2], '헛잣대 — 바탕 멈춤 상태 [1280] %s · [390] %s' % (bd.get('stopped'), bp.get('stopped')))
    # A8 — 첫 판은 높이만 쟀다: 높이는 한 줄인데 글이 5칸 격자 칸(58px)을 넘어 ④⑤ 가 겹친 것을 못 잡았다(9/27 탐침 · nowrap 만 건 판)
    def _a8(a):
        qs = {k: v for k, v in (a or {}).items() if not k.startswith('__') and isinstance(v, dict)}
        docs = [v for k, v in (a or {}).items() if k.startswith('__doc') and isinstance(v, dict)]
        return (qs, {k: v.get('lines') for k, v in qs.items() if any(l != 1 for l in (v.get('lines') or [0]))},
                {k: v.get('ov') for k, v in qs.items() if v.get('ov')}, {k: v.get('out') for k, v in qs.items() if v.get('out')},
                {k: v.get('vis') for k, v in qs.items() if not all(v.get('vis') or [False])}, [d for d in docs if d.get('sw', 0) > d.get('cw', 0)])
    qs, lb, ov, ot, iv, dw = _a8(NP.get('a8'))
    add('A8', sorted(qs) == sorted('2020:%d' % n for n in NOS20) and all(v.get('n') == 5 for v in qs.values()) and not lb and not ov and not ot and not iv and not dw,
        '[390] 2020 조합형 %d문항 × 선지 5: 글이 두 줄 이상 %s · 옆 선지와 겹침 %s · 선지 줄 밖 %s · 안 보임 %s · 가로 굴림 %s · 24번 자리 %s'
        % (len(qs), lb or 0, ov or 0, ot or 0, iv or 0, dw or 0, (qs.get('2020:24') or {}).get('pos')))
    qb, lbb, _, _, _, _ = _a8(BP.get('a8'))
    add('A8', bool(lbb), '헛잣대 — 바탕 선지 글 줄 수 %s' % {k: v.get('lines') for k, v in sorted(qb.items())})
    d8n, d8b = (N_.get('a8d') or {}).get('2020:24') or {}, (B_.get('a8d') or {}).get('2020:24') or {}
    same = bool(d8n.get('pos')) and len(d8n.get('pos')) == len(d8b.get('pos') or []) and all(
        all(abs(x - y) <= 0.5 for x, y in zip(p, q)) for p, q in zip(d8n.get('pos'), d8b.get('pos')))
    add('A8', same and d8n.get('lines') == [1] * 5, '[1280] 무변 — 2020 24번 선지 자리(선지 줄 기준 x·y·폭·높이) 새 판 %s = 바탕 %s · 줄 %s'
        % (d8n.get('pos'), d8b.get('pos'), d8n.get('lines')))
    p8n, p8b = (qs.get('2020:24') or {}).get('pos') or [], (qb.get('2020:24') or {}).get('pos') or []
    add('A8', p8n != p8b, '헛잣대(자리 잣대) — [390] 에선 새 판·바탕 자리가 갈린다 %s ≠ %s' % (p8n, p8b))
    # A9 — 기출뷰 밖 카드 무변
    a9, b9 = N_.get('a9') or {}, B_.get('a9') or {}
    add('A9', bool(N_.get('a9_o')) and a9 == b9 and bool(a9), '단원 풀기 %s 첫 카드 「정답·해설 ▸」 → O page.mouse — 새 판 %s = 바탕 %s' % ((N_.get('a9_u') or {}).get('label'), a9, b9))
    for k, R in (('책상', N_), ('아이패드', NI), ('폰', NP)):
        add('A9', not R.get('errs') and not ((R.get('err') or {}).get('err')), '[%s] pageerror %s · onerror %s' % (k, (R.get('errs') or [])[:2], ((R.get('err') or {}).get('err') or [])[:2]))
    say('       누름 못함 NEW 책상 %s' % (N_.get('miss') or [])[:4])
