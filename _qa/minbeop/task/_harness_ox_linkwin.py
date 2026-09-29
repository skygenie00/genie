# -*- coding: utf-8 -*-
"""_task_ox_linkwin §B 관문 — 본판 기출뷰 하네스(_harness_ox_exview_paper.py --only lw --base5 <앞 인도판>)가 불러 쓴다(서버·SEED·시험지·기록 틀을 같이 쓴다).

  NEW   = --app(linkwin 패치 결과) · BASE5 = genie 앞 인도 판 blob(exview_add3 · 카드 안 memo-panel · 저장하기) — 헛잣대
  판 = Chromium 책상(마우스 1280×900) · Chromium 아이패드(CDP 터치 r22 · 1024×768) · WebKit 책상(마우스)
  누름 = 진짜 포인터 · 글 = 진짜 키보드(page.keyboard.type) · 보임 = display ≠ none · 높이 > 0
"""
import json, os, time
import _harness_ox_exview_paper_add1 as A1
import _harness_ox_exview_paper_add2 as A2

BASE5_REV = None
DESK = {'width': 1280, 'height': 900}
IPAD = {'width': 1024, 'height': 768}
READY = "typeof buildQuizData==='function'&&!!window.__HZX&&!!window.__HZA&&!!window.__HZL"
J = A2.J
OWNER, PRE, Q5, Q68 = 'Q0134', 'Q0003', 'Q0005', 'Q0068'


def open_(M, br, tag, src, vw, touch, wk):
    if wk:
        s, ctx, errs = A2.open_wk(M, br, tag, src, vw, touch)
    else:
        s, ctx, errs = A1.open_page2(M, br, tag, src, vw, touch)
    s.pg.wait_for_function(READY, timeout=180000)
    return s, ctx, errs


def setup(s):
    s.js("__HZX.setup()")
    s.js("__HZB.prep()")
    return J(s.js("o=>__HZL.seed(o)", {OWNER: [PRE]}))


def st(s, k=OWNER):
    return J(s.js("k=>__HZL.state(k)", k))


def flow_new(M, br, tag, src, vw, touch, wk=False):
    s, ctx, errs = open_(M, br, tag, src, vw, touch, wk)
    R = {}
    try:
        R['seed'] = setup(s)
        R['go'] = J(s.js("k=>__HZL.goQ(k)", OWNER))
        R['open'] = s.at(J(s.js("k=>__HZL.lkBtn(k)", OWNER)), 700)
        R['s1'] = st(s)
        s.pg.keyboard.type(u'성년', delay=40)
        s.pg.wait_for_timeout(700)
        R['s2'] = st(s)
        R['noClick'] = s.at(J(s.js("([k,p])=>__HZL.rowAt(k,p)", [Q5, 'no'])), 900)
        R['qp5'] = J(s.js("k=>__HZL.qp(k)", Q5))
        R['lk_after_no'] = J(s.js("k=>__HZL.links(k)", OWNER))
        s.js("()=>{oxWinClose('q-%s');return 1}" % Q5)   # 문제 창이 연결 창을 덮지 않게(누름 관문 밖 · 창 닫기)
        R['rowClick'] = s.at(J(s.js("([k,p])=>__HZL.rowAt(k,p)", [Q5, 'tx'])), 900)
        R['lk_after_row'] = J(s.js("k=>__HZL.links(k)", OWNER))
        R['s3'] = st(s)
        A1.reload(s)
        s.js("__HZB.prep()")
        R['lk_reload'] = J(s.js("k=>__HZL.links(k)", OWNER))
        R['go2'] = J(s.js("k=>__HZL.goQ(k)", OWNER))
        s.at(J(s.js("k=>__HZL.lkBtn(k)", OWNER)), 700)
        R['xClick'] = s.at(J(s.js("k=>__HZL.curX(k)", Q5)), 700)
        R['lk_after_x'] = J(s.js("k=>__HZL.links(k)", OWNER))
        R['s4'] = st(s)
        s.at(J(s.js("()=>__HZL.inp()")), 200)
        s.pg.keyboard.type(Q68, delay=40)
        s.pg.wait_for_timeout(700)
        R['s5'] = st(s)
        R['q68Click'] = s.at(J(s.js("([k,p])=>__HZL.rowAt(k,p)", [Q68, 'tx'])), 900)
        R['lk_after_68'] = J(s.js("k=>__HZL.links(k)", OWNER))
        s.js("()=>__HZL.closeAll()")
        # 문항 팝업 안 「✏️ 연결」 → 같은 창(팝업 위) · 「↪ 이동」 글자만 · 누름 → 그 문제 자리
        s.js("k=>{showLinkedQuestion(k);return 1}", Q5)
        s.pg.wait_for_timeout(500)
        R['qpOpen'] = J(s.js("k=>__HZL.qp(k)", Q5))
        R['qpLk'] = s.at(J(s.js("k=>__HZL.qpLkBtn(k)", Q5)), 700)
        R['s6'] = st(s, Q5)
        R['qpAfter'] = J(s.js("k=>__HZL.qp(k)", Q5))
        s.js("()=>{const w=document.getElementById('oxwin-lk');if(w)w.remove();return 1}")
        go = (J(s.js("k=>__HZL.qp(k)", Q5)) or {}).get('go')
        R['goBtn'] = go
        R['goClick'] = s.at(go, 1500)
        R['goBox'] = J(s.js("k=>__HZL.boxVis(k)", Q5))
        R['errs'] = errs[:5]
        R['miss'] = s.miss[:6]
        return R
    finally:
        ctx.close()


def flow_base(M, br, tag, src, vw, touch, wk=False):
    s, ctx, errs = open_(M, br, tag, src, vw, touch, wk)
    R = {}
    try:
        R['has'] = s.js("()=>__HZL.has()")
        R['seed'] = setup(s)
        R['go'] = J(s.js("k=>__HZL.goQ(k)", OWNER))
        R['open'] = s.at(J(s.js("k=>__HZL.lkBtn(k)", OWNER)), 700)
        R['p1'] = J(s.js("k=>__HZL.oldPanel(k)", OWNER))
        R['s1'] = st(s)
        sp = (R['p1'] or {}).get('search')
        if sp:
            s.at(sp, 200)
            s.pg.keyboard.type(u'성년', delay=40)
            s.pg.wait_for_timeout(700)
            R['resClick'] = s.at(J(s.js("([k,q])=>__HZL.oldResAt(k,q)", [OWNER, Q5])), 600)
        R['p2'] = J(s.js("k=>__HZL.oldPanel(k)", OWNER))
        R['lk'] = J(s.js("k=>__HZL.links(k)", OWNER))
        R['qp'] = None
        s.js("k=>{showLinkedQuestion(k);return 1}", Q5)
        s.pg.wait_for_timeout(500)
        R['qp'] = J(s.js("k=>__HZL.qp(k)", Q5))
        R['errs'] = errs[:5]
        return R
    finally:
        ctx.close()


def runs(M, br, new, base5, say):
    out = {}
    t0 = time.time()
    out['lwnew'] = {'desk': flow_new(M, br, 'lw_desk', new, DESK, False), 'ipad': flow_new(M, br, 'lw_ipad', new, IPAD, True)}
    out['lwbase'] = {'desk': flow_base(M, br, 'lwb_desk', base5, DESK, False), 'ipad': flow_base(M, br, 'lwb_ipad', base5, IPAD, True)}
    say('  [lw chromium] %.0f초' % (time.time() - t0))
    return out


def runs_wk(M, pw, new, base5, say):
    wk = pw.webkit.launch()
    out = {}
    try:
        t0 = time.time()
        out['lwwk'] = {'desk': flow_new(M, wk, 'lww_desk', new, DESK, False, wk=True)}
        out['lwwkbase'] = {'desk': flow_base(M, wk, 'lwwb_desk', base5, DESK, False, wk=True)}
        say('  [lw webkit] %.0f초' % (time.time() - t0))
    finally:
        wk.close()
    return out


# ══════════ ★ revfix0928(9/28) A-1 — 연결 창 ✕ 크기(조판기 연결 창 ✕ = 22.9×17) · 나머지 22 종 무변 · ✕ 누름 → 닫힘 ══════════
PHONE = {'width': 390, 'height': 844}
XWANT = (22.9, 17.0)   # 조판기 b880a04 연결 창 ✕ (채팅 실측 · 지시서 §0 ①) — 채팅 환경 글꼴 값 · 관문은 같은 PC 의 조판기 실측(JOX)과 맞댄다
JOXF = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_ox_revfix0928_jox.json')   # _ox_revfix0928_jox.py 가 이 PC Chromium·WebKit 에서 잰 조판기 연결 창 ✕


def flow_x(M, br, tag, src, vw, touch, wk=False):
    s, ctx, errs = open_(M, br, tag, src, vw, touch, wk)
    R = {}
    try:
        setup(s)
        R['go'] = J(s.js("k=>__HZL.goQ(k)", OWNER))
        R['open'] = s.at(J(s.js("k=>__HZL.lkBtn(k)", OWNER)), 700)
        R['tries'] = 1
        if not st(s).get('win'):   # 창이 안 떴으면 한 번 더(몇 번 눌렀는지 적는다 · 두 번째에도 없으면 그대로 FAIL)
            s.pg.wait_for_timeout(600); R['open'] = s.at(J(s.js("k=>__HZL.lkBtn(k)", OWNER)), 900); R['tries'] = 2
        s.pg.keyboard.type(u'성년', delay=40)   # 결과 줄까지 그린 뒤 22 종을 잰다
        s.pg.wait_for_timeout(900)
        R['css'] = J(s.js("()=>__HZL.xcss()"))
        R['x'] = J(s.js("()=>__HZL.xAt()"))
        if wk and touch:
            x = R['x'] or {}
            if x.get('on') and x.get('hit'):
                s.pg.touchscreen.tap(x['cx'], x['cy']); s.pg.wait_for_timeout(700); R['xClick'] = True
            else:
                R['xClick'] = False
        else:
            R['xClick'] = s.at(R['x'], 700)
        R['after'] = st(s)
        R['errs'] = errs[:5]
        return R
    finally:
        ctx.close()


def runs_x(M, br, new, base6, say, wk=False):
    out = {}
    t0 = time.time()
    for nm, vw, touch in (('desk', DESK, False), ('ipad', IPAD, True), ('phone', PHONE, True)):
        out[('rxwk' if wk else 'rx') + '_' + nm] = {'new': flow_x(M, br, 'rx_%s_n' % nm, new, vw, touch, wk), 'base': flow_x(M, br, 'rx_%s_b' % nm, base6, vw, touch, wk)}
    say('  [rx ✕ %s] %.0f초' % ('webkit' if wk else 'chromium', time.time() - t0))
    return out


JOX = None


def gates_x(RES, add, say):
    global JOX
    try:
        JOX = json.load(open(JOXF, encoding='utf-8'))
    except Exception as e:
        add('RX-1', False, '조판기 ✕ 실측 파일 없음 — python _ox_revfix0928_jox.py 먼저(%s)' % e)
    for eng in ('rx', 'rxwk'):
        for nm, lab in (('desk', u'책상 1280(마우스)'), ('ipad', u'아이패드 1024(터치)'), ('phone', u'폰 390(터치)')):
            P = RES.get(eng + '_' + nm)
            if not P:
                continue
            E = 'WebKit' if eng == 'rxwk' else 'Chromium'
            n, b = P['new'] or {}, P['base'] or {}
            x, bx = n.get('x') or {}, b.get('x') or {}
            jx = (JOX or {}).get(('webkit' if eng == 'rxwk' else 'chromium') + '_' + nm) or {}
            add('RX-1', bool(jx) and abs((x.get('wf') or 0) - jx.get('w', -9)) <= 0.5 and abs((x.get('hf') or 0) - jx.get('h', -9)) <= 0.5 and x.get('cls') == 'cfx',
                '[%s %s] ✕ 크기 %s×%s = 조판기 연결 창 ✕ 같은 환경 실측 %s×%s(±0.5 · 채팅 22.9×17) · 여백 %s · 머리 오른쪽 끝 틈 %s' % (E, lab, x.get('wf'), x.get('hf'), jx.get('w'), jx.get('h'), (x.get('cs') or {}).get('paddingTop'), x.get('rightGap')))
            add('RX-1-헛', bool(jx) and bx.get('wf') is not None and abs((bx.get('wf') or 0) - jx.get('w', -9)) > 0.5, '[%s %s] 헛잣대 바탕 ✕ %s×%s(채팅 10.9×15)' % (E, lab, bx.get('wf'), bx.get('hf')))
            keep = ('fontSize', 'fontWeight', 'fontFamily', 'color', 'backgroundColor', 'borderTopWidth', 'cursor', 'marginLeft')
            add('RX-1', {k: (x.get('cs') or {}).get(k) for k in keep} == {k: (bx.get('cs') or {}).get(k) for k in keep},
                '[%s %s] ✕ 글꼴·색·바탕·테·커서·자리(margin-left auto) 무변 · 안쪽 여백만 %s → %s' % (E, lab, (bx.get('cs') or {}).get('paddingLeft'), (x.get('cs') or {}).get('paddingLeft')))
            nc, bc = n.get('css') or {}, b.get('css') or {}
            diff = {k: [nc.get(k), bc.get(k)] for k in set(nc) | set(bc) if nc.get(k) != bc.get(k)}
            add('RX-1', bool(nc) and len(nc) == 22 and not diff, '[%s %s] 나머지 22 종 계산값 = 바탕(다름 %d) %s' % (E, lab, len(diff), json.dumps(diff, ensure_ascii=False)[:300]))
            add('RX-1', bool(n.get('xClick')) and not (n.get('after') or {}).get('win') and not n.get('errs'), '[%s %s] ✕ 누름 → 창 닫힘 · 오류 %s · 연결 단추 누른 수 새 %s · 바탕 %s' % (E, lab, n.get('errs'), n.get('tries'), b.get('tries')))


def gates(RES, add, say):
    rows = [('Chromium 책상', 'lwnew', 'lwbase', 'desk'), ('Chromium 아이패드(터치 r22)', 'lwnew', 'lwbase', 'ipad'), ('WebKit 책상', 'lwwk', 'lwwkbase', 'desk')]
    for nm, tn, tb, k in rows:
        N_ = (RES.get(tn) or {}).get(k)
        B_ = (RES.get(tb) or {}).get(k)
        if not N_:
            add('LW', False, '[%s] 판 없음' % nm)
            continue
        s1 = N_.get('s1') or {}
        add('LW-1', bool(N_.get('open')) and s1.get('vis') and s1.get('w') == 440 and not s1.get('memoPanel') and s1.get('chips') == [u'변리사 16', u'2016:2:④', u'ID Q0134'] and s1.get('focus'),
            '[%s] Q0134 「✏️ 연결」 → 떠 있는 창 440 · 카드 안 memo-panel DOM 0 · 제목 칩 「변리사 16」「2016:2:④」「ID Q0134」 · 찾기 칸 초점 %s' % (nm, json.dumps({k2: s1.get(k2) for k2 in ('vis', 'w', 'memoPanel', 'chips', 'focus')}, ensure_ascii=False)))
        if B_:
            p1 = B_.get('p1') or {}
            add('LW-1-헛', p1.get('vis') and not (B_.get('s1') or {}).get('win'), '[%s] 헛잣대 바탕 — 카드 안 패널이 펼쳐짐(떠 있는 창 없음) %s' % (nm, json.dumps(p1, ensure_ascii=False)[:200]))
        s2 = N_.get('s2') or {}
        R0 = {r['id']: r for r in s2.get('rows') or []}
        r3, r5 = R0.get('ID ' + PRE) or {}, R0.get('ID ' + Q5) or {}
        add('LW-2', bool(r3) and r3.get('has') and float(r3.get('op') or 1) < 0.6 and bool(r5) and r5.get('no') == u'4번' and not r5.get('has'),
            '[%s] 「성년」 → 결과 줄(ID · N번 · 과목·단원 · 본문 70자) · Q0003(걸어 둠) 흐림 + 「이미 넣음」 · Q0005 「4번」 %s' % (nm, json.dumps(s2.get('rows')[:5], ensure_ascii=False)[:420]))
        add('LW-2', bool(N_.get('noClick')) and (N_.get('qp5') or {}).get('vis') and N_.get('lk_after_no') == [PRE],
            '[%s] Q0005 「4번」 누름 → Q0005 문항 팝업 보임 · 연결 수 무변 %s' % (nm, json.dumps({'팝업': (N_.get('qp5') or {}).get('vis'), '연결': N_.get('lk_after_no')}, ensure_ascii=False)))
        s3 = N_.get('s3') or {}
        add('LW-2', bool(N_.get('rowClick')) and N_.get('lk_after_row') == [PRE, Q5] and s3.get('save') == 0 and u'↩링크2' in (s3.get('lkChips') or []) and N_.get('lk_reload') == [PRE, Q5],
            '[%s] Q0005 줄 나머지 누름 → ox_q_links.Q0134 = [Q0003, Q0005](저장 단추 0) · 머리 「↩링크2」 · 새로고침 뒤 유지 %s' % (nm, json.dumps({'연결': N_.get('lk_after_row'), '칩': s3.get('lkChips'), '새로고침': N_.get('lk_reload')}, ensure_ascii=False)))
        if B_:
            p2 = B_.get('p2') or {}
            add('LW-2-헛', B_.get('lk') == [PRE] and Q5 in (p2.get('input') or ''), '[%s] 헛잣대 바탕 — 결과 누름 = ID 칸에만(저장 안 됨) %s' % (nm, json.dumps({'연결': B_.get('lk'), 'ID 칸': p2.get('input')}, ensure_ascii=False)))
        s4 = N_.get('s4') or {}
        add('LW-3', bool(N_.get('xClick')) and N_.get('lk_after_x') == [PRE] and u'↩링크1' in (s4.get('lkChips') or []),
            '[%s] 걸린 연결 Q0005 ✕ → [Q0003] · 머리 「↩링크1」 %s' % (nm, json.dumps({'연결': N_.get('lk_after_x'), '칩': s4.get('lkChips')}, ensure_ascii=False)))
        s5 = N_.get('s5') or {}
        first = ((s5.get('rows') or [{}])[0]).get('id')
        add('LW-4', first == 'ID ' + Q68 and bool(N_.get('q68Click')) and Q68 in (N_.get('lk_after_68') or []),
            '[%s] 찾기 칸 「Q0068」 → 첫 줄 Q0068 · 누름 → 연결 %s' % (nm, json.dumps({'첫 줄': first, '연결': N_.get('lk_after_68')}, ensure_ascii=False)))
        s6, qo, qa = N_.get('s6') or {}, N_.get('qpOpen') or {}, N_.get('qpAfter') or {}
        add('LW-5', bool(N_.get('qpLk')) and s6.get('vis') and s6.get('z', 0) > qo.get('z', 0) and s6.get('chips', [])[-1:] == [u'ID ' + Q5],
            '[%s] 문항 팝업 안 「✏️ 연결」 → 같은 창(팝업 위 z %s > %s) · 제목 칩 %s' % (nm, s6.get('z'), qo.get('z'), s6.get('chips')))
        gb = N_.get('goBtn') or {}
        c = gb.get('cs') or {}
        add('LW-5', gb.get('t') == u'↪ 이동' and c.get('backgroundColor') in ('rgba(0, 0, 0, 0)', 'transparent') and c.get('borderTopWidth') == '0px' and bool(N_.get('goClick')) and (N_.get('goBox') or {}).get('vis'),
            '[%s] 문항 팝업 「↪ 이동」 = 글자만(바탕 투명 · 테 0) · 누름 → 그 문제 자리 %s' % (nm, json.dumps({'이동': {'t': gb.get('t'), 'cs': c}, '자리': N_.get('goBox')}, ensure_ascii=False)))
        if B_:
            bg = ((B_.get('qp') or {}).get('go') or {})
            add('LW-5-헛', bg.get('t') == u'↪ 이 문제로 이동' and (bg.get('cs') or {}).get('backgroundColor') not in ('rgba(0, 0, 0, 0)', 'transparent'), '[%s] 헛잣대 바탕 — 「↪ 이 문제로 이동」 파란 단추 %s' % (nm, bg.get('t')))
        add('LW', not N_.get('errs'), '[%s] pageerror %s · 누름 못함 %s' % (nm, N_.get('errs'), N_.get('miss')))
