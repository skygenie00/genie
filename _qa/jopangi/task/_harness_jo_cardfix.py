# -*- coding: utf-8 -*-
r"""_task_jo_cardfix §B(9/27) 관문 하네스 — 칩 줄 · 연결 창 · 카드 연결 표시 · 이동 글자 · 근거 「!」 · 정정 · 판례 줄 · 유제 · 미분류.

  python _harness_jo_cardfix.py --new <앱> --data <jo/data> [--exam <gichul/pdf>] [--only c1,c2,...] [--eng chromium,webkit] [--res <결과 파일>]

  NEW  = 이 판 앱 + 데이터 · BASE = genie HEAD(바로 앞 인도판 = uid_add2+mbsame_add2+add3 판) 앱 + HEAD 데이터 — 칸마다 헛잣대(바탕에서 FAIL)
  누름 = 진짜 포인터(page.mouse · 손가락 = Chromium CDP 터치 r22 · WebKit touchscreen.tap) · 보임 = display ≠ none · 높이 > 0 · 자리 = elementFromPoint
  틀 = mbsame 하네스(_harness_jo_gaek_mbsame.py)의 serve·Pg·__HM · uidmbs2 도구(__UZ) · 이 판 도구(__CF).
"""
import io, json, os, re, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


_NEW, _DATA, _EXAM = ARG('--new'), ARG('--data'), ARG('--exam')
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_cardfix_result.txt'))
sys.argv = [sys.argv[0], '--new', _NEW, '--data', _DATA, '--base', '6242678'] + (['--exam', _EXAM] if _EXAM else [])   # A-6(d) 9/30 — 바탕 = 인도 때 HEAD 6242678(결정로그 9/27 20:51 「헛잣대 6242678」) · HEAD 로 두면 인도 뒤 헛잣대·바탕 대조가 새 판끼리 맞대 거꾸로 FAIL
sys.path.insert(0, HERE)
import _harness_jo_gaek_mbsame as M   # noqa: E402
from playwright.sync_api import sync_playwright   # noqa: E402
M.TESTS = (M.TESTS + '\n' + io.open(os.path.join(HERE, '_harness_jo_uidmbs2_tests.js'), encoding='utf-8').read()
           + '\n' + io.open(os.path.join(HERE, '_harness_jo_cardfix_tests.js'), encoding='utf-8').read())
M.WORK = M.WORK + '_cf'
RES = []


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
        self.dialogs = []
        self.pg.on('dialog', lambda d: (self.dialogs.append(d.type + ':' + d.message[:40]), d.dismiss()))

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
    return M.new_env(), M.base_env()


def reload_keep(p):
    p.pg.goto('http://127.0.0.1:%d/index.html?tok=1&keep=1' % p.port, wait_until='load', timeout=180000)
    p.pg.wait_for_function(M.READY, timeout=180000); p.pg.wait_for_timeout(700)


def home(p, law='특허법', gk='g'):
    p.ev("l=>__HM.home(l)", law)
    if p.ev("()=>__UZ.has('UZGK')"):
        p.ev("v=>__UZ.gk(v)", gk)


def go_key(p, k, gk='g'):
    home(p, gk=gk)
    sel = p.ev("k=>__UZ.selOfKey(k)", k)
    if not sel:
        return None
    p.ev("s=>__HM.go(s)", sel)
    pg = p.ev("k=>{const P=(OXPOOL||{})[k];if(!P)return null;const d=P.dom;const c=[...document.querySelectorAll('.qb.id')].find(b=>b.textContent.trim()===k);return c?null:(OXDOMPG||{})[d]}", k)
    if pg:
        p.ev("n=>__HM.page(n)", pg)
    return sel


def gkOf(p, k):
    """그 열쇠가 기출/기타 어느 쪽인가(카드가 그 거름에서만 선다)"""
    return 'g' if p.ev("k=>{try{return uzGkPass?(UZGK='g',uzGkPass(k)):true}catch(e){return true}}", k) else 'x'


# ══════════ §B-1 칩 줄 ══════════
def g_c1(p, b, eng):
    G = 'c-1'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        res[who] = {}
        for k in ('T1249085', 'TJ080011'):
            go_key(q, k, gkOf(q, k))
            res[who][k] = q.ev("k=>__CF.chipRow(k)", k)
    n1 = res['NEW'].get('T1249085') or {}
    pan = n1.get('pan') or {}
    prev = pan.get('prev') or {}
    ok_pan = bool(pan) and pan.get('ml') == '0px' and prev.get('sameRow') and 3 <= (prev.get('gap') or -9) <= 5
    tg = n1.get('tags') or {}
    ok_tag = bool(tg) and abs((tg.get('r') or 0) - (tg.get('hdR') or 0)) < 2
    T(G, u'T1249085 머리 「🔗 판 2」 = 앞 칩 오른쪽 끝 + gap 4(±1) · margin-left 0 · 태그 묶음 오른쪽 끝', ok_pan and ok_tag, {'판': pan, '태그': tg, '줄': n1.get('flow')})
    n2 = res['NEW'].get('TJ080011') or {}
    T(G, u'TJ080011 머리 「📎 유제」 칩 없음(걷음) · 태그 묶음 오른쪽 끝', n2 and not n2.get('yj') and abs(((n2.get('tags') or {}).get('r') or 0) - ((n2.get('tags') or {}).get('hdR') or 0)) < 2, n2)
    b1 = ((res['BASE'].get('T1249085') or {}).get('pan') or {})
    T(G + '-헛', u'헛잣대 바탕 — 「🔗 판 2」 margin-left 가 큼(가운데 뜸)', bool(b1) and float(str(b1.get('ml') or '0').replace('px', '') or 0) > 50, b1)


# ══════════ §B-2 연결 창 · §B-3 카드 연결 표시 · §B-4 이동 글자 ══════════
K0 = 'TR06092'


def g_c2(p, b, eng):
    G = 'c-2'
    for who, q in (('NEW', p), ('BASE', b)):
        q.ev("o=>__CF.seedLk(o)", {K0: ['T2259185']})
    out = {}
    for how in ('mouse', 'touch'):
        for who, q in (('NEW', p), ('BASE', b)):
            q.ev("o=>__CF.seedLk(o)", {K0: ['T2259185']})
            go_key(q, K0, gkOf(q, K0))
            q.ev("()=>__CF.winClose()")
            e0 = len(q.errs_all())
            at = q.ev("k=>__CF.lkBtn(k)", K0)
            q.press(at, how, 700)
            w = q.ev("()=>__CF.win()")
            q.pg.keyboard.type(u'조문', delay=40)
            q.pg.wait_for_timeout(700)
            for _ in range(20):   # 다른 두 법 데이터가 붙으면 결과가 다시 그려진다
                w2 = q.ev("()=>__CF.win()")
                if who != 'NEW' or any(r['uid'] == 'S1855224' for r in (w2.get('rows') or [])):
                    break
                q.pg.wait_for_timeout(300)
            out[(who, how)] = {'btn': bool(at and at.get('on')), 'w': w, 'w2': w2, 'errs': q.errs_all()[e0:e0 + 3]}
        n, bb = out[('NEW', how)], out[('BASE', how)]
        w, w2 = n['w'] or {}, n['w2'] or {}
        rows = [r['uid'] for r in (w2.get('rows') or [])]
        T(G, u'TR06092 「✏️ 연결」(%s) → 떠 있는 창 440 · 제목 칩 「06 변리」「2006:?:②」「TR06092」 · 찾기 칸 초점 · 오류 0' % how,
          n['btn'] and w.get('vis') and w.get('w') == 440 and w.get('chips') == [u'06 변리', u'2006:?:②', 'TR06092'] and w.get('focus') and not n['errs'],
          {'창': {k: w.get(k) for k in ('vis', 'w', 'title', 'chips', 'focus', 'inTag')}, '오류': n['errs']})
        RW = {r['uid']: r for r in (w2.get('rows') or [])}
        t22, t07, s18 = RW.get('T2259185') or {}, RW.get('TR07023') or {}, RW.get('S1855224') or {}
        T(G, u'「조문」(%s) → 줄 셋 T2259185 · TR07023 · S1855224(세 법 · 풀 차례) · T2259185 흐림 + 「이미 넣음」 · 번호 = 책 번호 「25번」「13번」 · 리담 「22번(4)」 · 상표 줄 「상표법 · 2018 제55회」' % how,
          len(rows) == 3 and set(rows) == {'T2259185', 'TR07023', 'S1855224'} and t22.get('has') and float(t22.get('op') or 1) < 0.6 and not t07.get('has')
          and t22.get('no') == u'25번' and t07.get('no') == u'13번' and s18.get('no') == u'22번(4)' and (s18.get('wh') or '') == u'상표법 · 2018 제55회',
          {'줄': w2.get('rows'), '걸린': w2.get('cur')})
        bw, bw2 = bb['w'] or {}, bb['w2'] or {}
        T(G + '-헛', u'헛잣대 바탕(%s) — 제목 「✏ 메모 및 유사문제 연결 — 2006년 9번(2)」 · 찾기 칸 초점 없음(ta 오류) · 「조문」 = 지금 법 본문만(세 줄 못 됨)' % how,
          (u'2006년 9번(2)' in (bw.get('title') or '')) and len(bw2.get('rows') or []) < 3 and not bw.get('focus') and any(('ta is not defined' in e) or ("Can't find variable: ta" in e) for e in bb['errs']),
          {'제목': bw.get('title'), '줄': len(bw2.get('rows') or []), '초점': bw.get('focus'), '오류': bb['errs']})
    # 번호 누름 = 문제 창 · 연결 안 늘어남 → 줄 나머지 = 연결 → 새로고침 뒤 유지 → ✕ → 1 → 상표 연결 → ↩링크2 · 상표 번호 → 상표 문제 창
    q = p
    q.ev("o=>__CF.seedLk(o)", {K0: ['T2259185']})
    go_key(q, K0, gkOf(q, K0))
    q.ev("()=>__CF.winClose()")
    q.press(q.ev("k=>__CF.lkBtn(k)", K0), 'mouse', 700)
    q.pg.keyboard.type(u'조문', delay=40); q.pg.wait_for_timeout(700)
    q.press(q.ev("([u,p])=>__CF.winRowAt(u,p)", ['TR07023', 'no']), 'mouse', 900)
    qp = q.ev("k=>__CF.qp(k)", 'TR07023')
    lk1 = q.ev("k=>__CF.lk(k)", K0)
    T(G, u'「13번」(번호) 누름 → TR07023 문제 창 보임 · 연결 무변(1)', qp.get('vis') and (lk1 or {}).get('my') == ['T2259185'], {'문제 창': qp, '연결': lk1})
    at = q.ev("([u,p])=>__CF.winRowAt(u,p)", ['TR07023', 'tx'])
    q.press(at, 'mouse', 900)
    w3 = q.ev("()=>__CF.win()")
    lk2 = q.ev("k=>__CF.lk(k)", K0)
    T(G, u'TR07023 줄 나머지 누름 → 바로 연결(걸린 연결 2 · 저장 단추 없음 · 찾기 칸 비움 · 창 열린 채)', (lk2 or {}).get('my') == ['T2259185', 'TR07023'] and w3.get('vis') and w3.get('curN') == u'걸린 연결 2' and not w3.get('rows'),
      {'연결': lk2, '걸린': w3.get('curN'), '줄': w3.get('cur')})
    reload_keep(q)
    lk3 = q.ev("k=>__CF.lk(k)", K0)
    T(G, u'새로고침 뒤 유지', (lk3 or {}).get('my') == ['T2259185', 'TR07023'], lk3)
    go_key(q, K0, gkOf(q, K0))
    q.press(q.ev("k=>__CF.lkBtn(k)", K0), 'mouse', 700)
    q.press(q.ev("u=>__CF.winCurX(u)", 'TR07023'), 'mouse', 700)
    lk4 = q.ev("k=>__CF.lk(k)", K0)
    T(G, u'걸린 연결 ✕ → 1', (lk4 or {}).get('my') == ['T2259185'], lk4)
    q.press(q.ev("()=>__CF.winInp()"), 'mouse', 200)   # ✕ 를 누르면 초점이 찾기 칸을 떠난다(WebKit) — 칸을 다시 눌러 쓴다
    q.pg.keyboard.type(u'조문', delay=40); q.pg.wait_for_timeout(900)
    for _ in range(20):
        if q.ev("u=>__CF.winRowAt(u,'tx')", 'S1855224'):
            break
        q.pg.wait_for_timeout(300)
    q.press(q.ev("([u,p])=>__CF.winRowAt(u,p)", ['S1855224', 'tx']), 'mouse', 900)
    lk5 = q.ev("k=>__CF.lk(k)", K0)
    q.ev("()=>__CF.winClose()")
    go_key(q, K0, gkOf(q, K0))
    hc = q.ev("k=>__CF.headLkChip(k)", K0)
    T(G, u'S1855224(상표) 연결 → 머리 칩 「↩링크2」', (lk5 or {}).get('my') == ['T2259185', 'S1855224'] and hc and hc.get('t') == u'↩링크2', {'연결': lk5, '칩': hc and hc.get('t')})
    q.press(q.ev("k=>__CF.lkBtn(k)", K0), 'mouse', 900)
    q.pg.wait_for_timeout(600)
    wc = q.ev("()=>__CF.win()")
    at = q.ev("k=>{const w=[...POPS].filter(p=>p._cflw).pop();if(!w)return null;const r=[...w.querySelectorAll('.cfcur .cfcr')].find(x=>x.querySelector('.cfid')&&x.querySelector('.cfid').textContent.trim()===k);const n=r&&r.querySelector('.cfno');if(!n)return null;n.scrollIntoView({block:'center'});const b=n.getBoundingClientRect();const x=b.left+b.width/2,y=b.top+b.height/2;const at=document.elementFromPoint(x,y);return {cx:x,cy:y,on:!!at&&(at===n||n.contains(at))}}", 'S1855224')
    q.press(at, 'mouse', 1200)
    qs = q.ev("k=>__CF.qp(k)", 'S1855224')
    T(G, u'걸린 상표 줄 번호 누름 → 상표 문제 창 보임(상표 데이터로 · 「↪ 이동」 없음)', qs.get('vis') and u'상표법' in (qs.get('title') or '') and not qs.get('go'), {'걸린': wc.get('cur'), '문제 창': qs})
    q.ev("()=>__CF.winClose()")


def g_c3(p, b, eng):
    G = 'c-3'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        q.ev("o=>__CF.seedLk(o)", {K0: ['T2259185']})
        go_key(q, K0, gkOf(q, K0))
        res[who] = {'lines': q.ev("k=>__CF.lnkLines(k)", K0), 'chip': q.ev("k=>__CF.headLkChip(k)", K0)}
    n = res['NEW']; c = (n['chip'] or {}).get('cs') or {}
    T(G, u'카드 「🔗 관련 문제」 줄 DOM 0 · 머리 「↩링크1」 바탕 투명 · 테 0 · 색 #1e3a8a', n['lines'] == [] and (n['chip'] or {}).get('t') == u'↩링크1'
      and c.get('backgroundColor') in ('rgba(0, 0, 0, 0)', 'transparent') and c.get('borderTopWidth') == '0px' and c.get('color') == 'rgb(30, 58, 138)', n)
    bb = res['BASE']
    T(G + '-헛', u'헛잣대 바탕 — 「↩ 내가 연결한 1」 알약 · 「관련 문제」 줄', (bb['chip'] or {}).get('t') == u'↩ 내가 연결한 1' and bool(bb['lines']), bb)


def g_c4(p, b, eng):
    G = 'c-4'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        go_key(q, K0, gkOf(q, K0))
        q.ev("()=>__CF.winClose()")
        q.ev("k=>popCard(k,null)", 'TR07023')
        q.pg.wait_for_timeout(500)
        res[who] = q.ev("k=>__CF.qp(k)", 'TR07023')
    g = (res['NEW'].get('go') or {})
    c = g.get('cs') or {}
    ok = g.get('t') == u'↪ 이동' and c.get('backgroundColor') in ('rgba(0, 0, 0, 0)', 'transparent') and c.get('borderTopWidth') == '0px'
    p.press(g, 'mouse', 1200)
    moved = p.ev("k=>{const c=document.getElementById('qb-'+k)||[...document.querySelectorAll('.qb.id')].find(b=>b.textContent.trim()===k);if(!c)return null;const r=c.getBoundingClientRect();return {y:Math.round(r.top),vis:r.height>0&&r.top<innerHeight&&r.bottom>0}}", 'TR07023')
    T(G, u'문제 창 「↪ 이동」 = 글자만(바탕 투명 · 테 0 · #1d4ed8 12px 700) · 누름 → 그 지문 자리', ok and bool(moved and moved.get('vis')), {'이동': g, '자리': moved})
    gb = (res['BASE'].get('go') or {})
    T(G + '-헛', u'헛잣대 바탕 — 「↪ 이 지문으로 이동」 파란 단추', gb.get('t') == u'↪ 이 지문으로 이동' and ((gb.get('cs') or {}).get('backgroundColor') not in ('rgba(0, 0, 0, 0)', 'transparent')), gb)
    for q in (p, b):
        q.ev("()=>__CF.winClose()")


# ══════════ §B-5 근거 「!」 ══════════
def g_c5(p, b, eng):
    G = 'c-5'
    res = {}
    for how in ('mouse', 'touch'):
        for who, q in (('NEW', p), ('BASE', b)):
            q.ev("([k,t])=>__CF.ggSeed(k,t)", [K0, u'제201조 제1항 국어번역문'])
            go_key(q, K0, gkOf(q, K0))
            q.press(q.ev("k=>__CF.ggNum(k)", K0), how, 500)
            s0 = q.ev("k=>__CF.ggPan(k)", K0)
            q.ev("([k,s])=>__CF.ggTypeCs(k,s)", [K0, u'쓰던 댓글'])
            q.pg.wait_for_timeout(200)
            bg = q.ev("k=>__CF.ggBang(k)", K0)   # 댓글 칸 초점으로 화면이 굴렀을 수 있다 — 누를 자리를 다시 잰다
            q.press(bg, how, 600)
            s1 = q.ev("k=>__CF.ggPan(k)", K0)
            nm = q.ev("k=>__CF.ggNum(k)", K0)
            bang1 = q.ev("k=>__CF.bangOf(k)", K0)
            s2 = None
            if who == 'NEW':
                q.press(q.ev("k=>__CF.ggBang(k)", K0), how, 600)
                s2 = q.ev("k=>__CF.ggPan(k)", K0)
            res[(who, how)] = {'s0': s0, 's1': s1, 'num': nm, 'bang': bang1, 's2': s2}
        n = res[('NEW', how)]; s1 = n['s1'] or {}; nc = ((n['num'] or {}).get('cs') or {})
        T(G, u'TR06092 근거 1 펴고 「!」 누름(%s) → 칸 그대로 보임 · 바탕 rgb(255,245,245) · 왼쪽 3px · 번호 칩 테 2.5px · 쓰던 댓글 그대로' % how,
          s1.get('vis') and (s1.get('cs') or {}).get('backgroundColor') == 'rgb(255, 245, 245)' and (s1.get('cs') or {}).get('borderLeftWidth') == '3px' and nc.get('borderTopWidth') in ('2.5px', '2px')
          and ((s1.get('ta') or {}).get('v') == u'쓰던 댓글') and n['bang'] is True, {'칸': s1, '번호': nc})
        s2 = n['s2'] or {}
        T(G, u'다시 누름(%s) → 되돌림(칸 보임 · 분홍 없음 · 기록 끔)' % how, s2.get('vis') and (s2.get('cs') or {}).get('backgroundColor') != 'rgb(255, 245, 245)', s2)
        bb = res[('BASE', how)]
        T(G + '-헛', u'헛잣대 바탕(%s) — 「!」 누르면 칸이 닫힘(display none)' % how, ((bb['s1'] or {}).get('disp') == 'none'), bb['s1'])


# ══════════ §B-6 정정 ══════════
K6 = 'TR06092'


def g_c6(p, b, eng):
    G = 'c-6'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        q.ev("()=>__CF.prep()")
        home(q)
        n0 = (q.ev("()=>__CF.headFixN()") or {}).get('n', 0)
        go_key(q, K6, gkOf(q, K6))
        q.press(q.ev("k=>__CF.peek(k)", K6), 'mouse', 400)
        d0 = len(q.dialogs)
        q.ev("()=>{window.__PROMPTS=0;window.prompt=(...a)=>{window.__PROMPTS++;return null};return 1}")   # 바탕 틀(SEED)이 prompt 를 스텁해 dialog 이벤트가 안 난다 — 부른 수를 센다
        q.press(q.ev("k=>__CF.fixBtn(k)", K6), 'mouse', 700)
        pan = q.ev("k=>__CF.fixPanel(k)", K6)
        res[who] = {'n0': n0, 'pan': pan, 'dlg': q.dialogs[d0:], 'prompt': q.ev("()=>window.__PROMPTS")}
    n = res['NEW']
    T(G, u'「✎ 정정」 → 해설 밑 노란 칸 보임(prompt 0 · dialog 0) · 문제·해설·종합사례 원문 글칸 셋 · 정답 O/X', (n['pan'] or {}).get('on') and not n['dlg'] and not n['prompt'] and (n['pan'] or {}).get('n') == 3, n)
    bb = res['BASE']
    T(G + '-헛', u'헛잣대 바탕 — prompt 를 부른다 · 노란 칸 없음', (bool(bb['dlg']) or (bb['prompt'] or 0) > 0) and not (bb['pan'] or {}).get('on'), bb)
    q = p
    raw = q.ev("k=>(OXPOOL[k]||{}).ans", K6)
    alt = 'X' if raw == 'O' else 'O'
    q.press(q.ev("([k,v])=>__CF.fixPick(k,v)", [K6, alt]), 'mouse', 300)
    q.ev("([k,s])=>__CF.fixExpSet(k,s)", [K6, u'정정한 해설 한 줄'])
    q.press(q.ev("k=>__CF.fixSave(k)", K6), 'mouse', 900)
    st = q.ev("k=>__CF.fixState(k)", K6)
    hd = q.ev("([k,w])=>__CF.fixDone(k,w)", [K6, 'head'])
    ex = q.ev("k=>__CF.expText(k)", K6)
    T(G, u'정답 %s · 해설 한 줄 고쳐 저장 → 카드 머리 「✎ 정정됨」 · 해설 = 고친 글 · 정오 = %s(FIX_KEY) · 글 칸 = jopangi.qfix' % (alt, alt),
      bool(hd) and (st or {}).get('ansfix') == alt and ((st or {}).get('qfix') or {}).get('exp') == u'정정한 해설 한 줄' and u'정정한 해설 한 줄' in ((ex or {}).get('t') or ''), {'상태': st, '머리': bool(hd), '해설': ex})
    # 정오 alt 로 채점 — 카드 O/X 누름 + 그 쪽 채점 단추(진짜 누름)
    q.press(q.ev("([k,v])=>__CF.oxBtn(k,v)", [K6, alt]), 'mouse', 400)
    mk = q.ev("k=>__CF.rec(k)", K6)
    # 쪽 채점 알약은 그 쪽 지문을 다 골라야 채점한다(옛 규칙) — 이 지문 한 칸만 채점기에 넘긴다(정오 = 정정 값인지만 본다)
    q.ev("([k,raw])=>{oxGrade([{k:k,ans:raw,dom:'qb-'+k}],null);return 1}", [K6, raw])
    q.pg.wait_for_timeout(600)
    rc = q.ev("k=>__CF.rec(k)", K6)
    T(G, u'카드 %s 누름(마킹) → 채점 = 정정 값 %s 로 맞음(원래 %s)' % (alt, alt, raw), (mk or {}).get('m') == alt and (rc or {}).get('p') == alt and (rc or {}).get('ok') is True, {'마킹': mk, '기록': rc})
    go_key(q, K6, gkOf(q, K6))
    q.press(q.ev("([k,w])=>__CF.fixDone(k,w)", [K6, 'act']) or q.ev("([k,w])=>__CF.fixDone(k,w)", [K6, 'head']), 'mouse', 500)
    ex2 = q.ev("k=>__CF.expText(k)", K6)
    T(G, u'「✎ 정정됨」 누름 → 원래 값(원래 해설) 상자', bool((ex2 or {}).get('orig')) and u'원래 값' in (ex2 or {}).get('orig', ''), ex2)
    home(q)
    hn = q.ev("()=>__CF.headFixN()") or {}
    q.press(hn, 'mouse', 700)
    fl = q.ev("()=>__CF.fixListWin()") or {}
    T(G, u'첫 화면 「✎ 정정 N」 +1(%s → %s) → 목록 창에 TR06092' % (res['NEW']['n0'], hn.get('n')), hn.get('n') == res['NEW']['n0'] + 1 and K6 in (fl.get('rows') or []), {'머리': hn, '목록': fl})
    q.ev("()=>__CF.winClose()")
    go_key(q, K6, gkOf(q, K6))
    if not q.ev("k=>__CF.expShown(k)", K6):   # 채점된 지문은 해설 칸이 이미 펴져 있다
        q.press(q.ev("k=>__CF.peek(k)", K6), 'mouse', 300)
    q.press(q.ev("k=>__CF.fixBtn(k)", K6), 'mouse', 700)
    q.press(q.ev("k=>__CF.fixUnset(k)", K6), 'mouse', 900)
    st2 = q.ev("k=>__CF.fixState(k)", K6)
    T(G, u'↩ 정정 해제 → 원래대로(FIX_KEY · qfix 칸 없음)', not (st2 or {}).get('ansfix') and not (st2 or {}).get('qfix'), st2)


# ══════════ §B-7 판례 줄 · §B-8 유제 · §B-9 미분류 ══════════
def g_c7(p, b, eng):
    G = 'c-7'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        k = 'T1249085'
        go_key(q, k, gkOf(q, k))
        q.press(q.ev("k=>__CF.peek(k)", k), 'mouse', 400)
        res[who] = q.ev("k=>__CF.panLine(k)", k)
    n = res['NEW'] or {}; c = n.get('cs') or {}
    T(G, u'T1249085 해설 펼침 → 「🏛 2009다19093」 둥근 0 · 바탕 투명 · 「같은 지문」 글자 0', n.get('t') == u'🏛 2009다19093' and c.get('borderTopLeftRadius') == '0px'
      and c.get('backgroundColor') in ('rgba(0, 0, 0, 0)', 'transparent') and not n.get('same'), n)
    bb = res['BASE'] or {}
    T(G + '-헛', u'헛잣대 바탕 — 알약(둥근 · 바탕) · 「같은 지문 N」', ((bb.get('cs') or {}).get('borderTopLeftRadius') not in ('0px', None)) and bb.get('same'), bb)


def g_c8(p, b, eng):
    G = 'c-8'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        k = 'TJ080011'
        sel = go_key(q, k, gkOf(q, k))
        seq = q.ev("s=>__CF.cardSeq(s)", sel) or []
        i = seq.index(k) if k in seq else -1
        yj = {}
        for gk in ('g', 'x'):
            go_key(q, k, gk)
            yj[gk] = q.ev("()=>__CF.yjChip()")
        res[who] = {'next': seq[i + 1] if 0 <= i < len(seq) - 1 else None, 'yj': yj, 'sel': sel}
    n = res['NEW']
    T(G, u'1.2 국제조약 — 단원 카드 차례 TJ080011(8번) 바로 다음 T0946093r(8-유제) 그대로 · 「📎 유제」 DOM 0(기출·기타 둘 다)', n['next'] == 'T0946093r' and not any(n['yj'].values()), n)
    T(G + '-헛', u'헛잣대 바탕 — 「📎 유제」 칩 있음', any((v or 0) > 0 for v in res['BASE']['yj'].values()), res['BASE'])


def g_c9(p, b, eng):
    G = 'c-9'
    res = {}
    for who, q in (('NEW', p), ('BASE', b)):
        r = {}
        for gk in ('g', 'x'):
            home(q, gk=gk)
            r[gk] = {'chip': q.ev("()=>__CF.unkChip()"), 'drawer': q.ev("()=>__CF.unkDrawer()"), 'card': q.ev("()=>__CF.unkCard()"), 'keys': q.ev("()=>__CF.unk()")}
        home(q)
        r['raw'] = q.ev("()=>__CF.unkRaw()")
        res[who] = r
    n = res['NEW']; g = n['g']
    want = (g['keys'] or {}).get('n')
    T(G, u'특허 첫 화면 칩 = 서랍 = 첫 화면 카드 「미분류 (리담)」 = 미분류 열쇠 수(%s) · 미분류 열쇠 ∩ 마디 카드 열쇠 = 0 · 기타 = 0(리담 = 기출)' % want,
      bool(want) and (g['chip'] or {}).get('n') == want and (g['drawer'] or {}).get('n') == want and g['card'] == want and (g['keys'] or {}).get('both') == 0
      and not (n['x']['chip'] or {}).get('n'), n)
    bb = res['BASE']['g']
    T(G + '-헛', u'헛잣대 바탕 — 마디 카드에 선 열쇠를 미분류에서도 셈(칩 > 새 칩 · 교집합 > 0)', ((bb['chip'] or {}).get('n') or 0) > (want or 0) and ((bb['keys'] or {}).get('both') or 0) > 0, bb)


BR = {}
PARTS = [('c1', g_c1), ('c2', g_c2), ('c3', g_c3), ('c4', g_c4), ('c5', g_c5), ('c6', g_c6), ('c7', g_c7), ('c8', g_c8), ('c9', g_c9)]


def run_engine(pw, eng):
    br = getattr(pw, eng).launch()
    BR[eng] = br
    (ns, nd, ne), (bs, bd, be) = envs()
    try:
        p = Pg(br, eng, 'cfN', ns, nd, ne)
        b = Pg(br, eng, 'cfB', bs, bd, be)
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
    with sync_playwright() as pw:
        for eng in ENGS:
            RES.append(('ENG', eng, None, ''))
            print('INFO | ENG · %s |' % eng, flush=True)
            run_engine(pw, eng)
    npass = sum(1 for r in RES if r[2] is True); nfail = sum(1 for r in RES if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · %s · NEW %s · 데이터 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), 'cardfix', os.path.basename(_NEW), _DATA, ','.join(ENGS)))
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[ok], g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:600]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
