# -*- coding: utf-8 -*-
r"""_task_jo_hdrfold §B(9/27) 관문 하네스 — 「민소」 칩 오른쪽 세모 · 접음(다섯 요소) · 펼침 · 기억 · 접은 동안 · PC 머리.

  python _harness_jo_hdrfold.py --new <앱> --data <jo/data> [--exam <gichul/pdf>] [--only h1,...] [--eng chromium,webkit] [--res <결과 파일>]

  NEW  = 이 판 앱 · BASE = genie HEAD(바로 앞 인도판) 앱 + HEAD 데이터 — 칸마다 헛잣대(바탕에서 FAIL)
  누름 = 진짜 포인터(page.mouse · 손가락 = Chromium CDP 터치 r22 · WebKit touchscreen.tap) · 보임 = display ≠ none · 높이 > 0
  틀 = mbsame 하네스(_harness_jo_gaek_mbsame.py)의 serve·Pg·__HM · 이 판 도구(__HF).
"""
import io, json, os, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


_NEW, _DATA, _EXAM = ARG('--new'), ARG('--data'), ARG('--exam')
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_hdrfold_result.txt'))
sys.argv = [sys.argv[0], '--new', _NEW, '--data', _DATA, '--base', '06b95c4'] + (['--exam', _EXAM] if _EXAM else [])   # A-6(d) 9/30 — 바탕 = 인도 때 HEAD 06b95c4(결정로그 9/28 11:48 「헛잣대 = 06b95c4 의 jo = d6cf661」) · HEAD 로 두면 인도 뒤 헛잣대·바탕 대조가 새 판끼리 맞대 거꾸로 FAIL
sys.path.insert(0, HERE)
import _harness_jo_gaek_mbsame as M   # noqa: E402
from playwright.sync_api import sync_playwright   # noqa: E402
M.TESTS = '\n'.join([M.TESTS] + [io.open(os.path.join(HERE, f), encoding='utf-8').read() for f in ('_harness_jo_uidmbs2_tests.js', '_harness_jo_hdrfold_tests.js')])
M.WORK = M.WORK + '_hf'
RES = []
PHONE, PC = (390, 844), (1553, 900)
FIVE = ['#hrail', '#hbadges', '#hsrow', '#slot .mbhd', '#slot .mbsr']


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:480]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:480]), flush=True)


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

    def size(self, W, H):
        self.pg.set_viewport_size({'width': W, 'height': H})
        self.pg.wait_for_timeout(400)


def envs():
    return M.new_env(), M.base_env()


def reload_keep(q):
    q.pg.goto('http://127.0.0.1:%d/index.html?tok=1&keep=1' % q.port, wait_until='load', timeout=180000)
    q.pg.wait_for_function(M.READY, timeout=180000); q.pg.wait_for_timeout(700)


def fold_to(q, want, how):
    """세모를 진짜 포인터로 눌러 접힘 = want 로(이미 그러면 그대로)"""
    st = q.ev("()=>__HF.state()")
    if bool(st.get('hfold')) == want:
        return True
    ok = q.press(q.ev("()=>__HF.btn()"), how, 700)
    q.pg.wait_for_timeout(300)
    return ok


def g_h1(p, b, eng):
    G = 'h-1'
    for vp, (W, H), how in ((u'폰', PHONE, 'touch'), ('PC', PC, 'mouse')):
        res = {}
        for who, q in (('NEW', p), ('BASE', b)):
            q.size(W, H)
            q.ev("l=>__HF.gaek(l)", u'특허법')
            res[who] = q.ev("()=>__HF.btn()")
        n = res['NEW']
        cs = n.get('cs') or {}
        T(G, u'%s %d — #hdrFold 가 #laws 바로 오른쪽(같은 줄 · 세로 가운데 ±4) · 글자 「▴」 · 13px #6b7280 · 테·바탕 없음 · 좌우 8px · title' % (vp, W),
          n.get('has') and n.get('prevId') == 'laws' and n.get('sameRow') and n.get('text') == u'▴' and n.get('title') == u'머리 접기 / 펴기' and n.get('on')
          and cs.get('fontSize') == '13px' and cs.get('color') == 'rgb(107, 114, 128)' and cs.get('backgroundColor') in ('rgba(0, 0, 0, 0)', 'transparent') and cs.get('borderTopWidth') == '0px'
          and cs.get('paddingLeft') == '8px' and cs.get('paddingRight') == '8px', n)
        T(G + '-헛', u'헛잣대 바탕 %s — 세모 없음' % vp, not res['BASE'].get('has'), res['BASE'])


def g_h2(p, b, eng):
    G = 'h-2'
    W, H = PHONE
    s = {}
    for who, q in (('NEW', p), ('BASE', b)):
        q.size(W, H)
        q.ev("()=>{localStorage.removeItem('jopangi_ui');S.hdrFold=false;return 1}")
        if who == 'NEW':   # ★ 9/30 A-6 — revfix0929b A-6: 폰 부팅 = 1차객 서랍 접힌 채 · 펼친 폰 서랍 바깥 첫 누름은 접기만(DRAWER_EAT) → 안 접으면 세모 첫 누름이 먹혀 h-2~h-5 가 한 박자 밀린다
            q.ev("()=>{S.jtFold=true;return 1}")
        q.ev("l=>__HF.gaek(l)", u'특허법')
        s[who] = q.ev("()=>__HF.state()")
    q = p
    s0 = s['NEW']
    q.press(q.ev("()=>__HF.btn()"), 'touch', 900)
    s1 = q.ev("()=>__HF.state()"); b1 = q.ev("()=>__HF.btn()")
    T(G, u'폰 특허 1차객 — 손가락 누름 → 「▾」 · 다섯 요소 display none · 본문(#slot) 위 끝 ≤ 50 · 가로 넘침 0 · 로고·법 칩·세모 보임',
      all(v == 'vis' for v in s0['five'].values()) and b1.get('text') == u'▾' and all(v == 'none' for v in s1['five'].values()) and (s1.get('slotTop') or 999) <= 50 and s1.get('over') == 0
      and s1.get('logo') and s1.get('lawsVis') and s1.get('btnVis'), {'전': s0, '뒤': s1, '세모': b1.get('text')})
    T(G + '-헛', u'헛잣대 바탕 폰 — 본문 위 끝 > 50(채팅 290)', (s['BASE'].get('slotTop') or 0) > 50, s['BASE'])
    q.press(q.ev("()=>__HF.btn()"), 'touch', 900)
    s2 = q.ev("()=>__HF.state()")
    T('h-3', u'다시 누름 → 다섯 요소 되살아남 · 「▴」 · 본문 위 끝 = 바탕 값(±1)', all(v == 'vis' for v in s2['five'].values()) and q.ev("()=>__HF.btn()").get('text') == u'▴'
      and abs((s2.get('slotTop') or 0) - (s['BASE'].get('slotTop') or -99)) <= 1, {'뒤': s2, '바탕': s['BASE'].get('slotTop')})
    # 기억 — 접고 새로고침(다른 키 무변)
    q.ev("()=>{uiSave();return 1}")
    u0 = q.ev("()=>__HF.ui()") or {}
    q.press(q.ev("()=>__HF.btn()"), 'touch', 900)
    u1 = q.ev("()=>__HF.ui()") or {}
    reload_keep(q)
    q.ev("l=>__HF.gaek(l)", u'특허법')
    s3 = q.ev("()=>__HF.state()"); b3 = q.ev("()=>__HF.btn()")
    other = sorted(k for k in set(u0) | set(u1) if k != 'hdr_fold' and u0.get(k) != u1.get(k))
    T('h-4', u'새로고침 뒤 접힘 유지(jopangi_ui.hdr_fold = true) · 다른 키 무변', u1.get('hdr_fold') is True and u0.get('hdr_fold') is False and s3.get('hfold') and b3.get('text') == u'▾'
      and all(v == 'none' for v in s3['five'].values()) and not other, {'hdr_fold': [u0.get('hdr_fold'), u1.get('hdr_fold')], '바뀐 다른 키': other, '새로고침 뒤': s3})
    # 접은 동안 — Ctrl K · 법 칩 · 조문 갈래 작업 막대
    q.pg.keyboard.press('Control+k'); q.pg.wait_for_timeout(500)
    sk = q.ev("()=>__HF.sk()")
    q.pg.keyboard.press('Escape'); q.pg.wait_for_timeout(300); q.ev("()=>__HF.skClose()")
    q.press(q.ev("t=>__HF.lawAt(t)", u'상표'), 'touch', 1200)
    sl1 = q.ev("()=>__HF.state()")
    q.press(q.ev("t=>__HF.lawAt(t)", u'특허'), 'touch', 1200)
    sl2 = q.ev("()=>__HF.state()")
    T('h-5', u'접은 동안 — Ctrl K 검색 창 뜸 · 법 칩 상표(손가락) → 법만 바뀜(접힘 그대로) · 특허로 되돌림', sk.get('vis') and (sl1.get('S') or {}).get('law') == u'상표법' and sl1.get('hfold')
      and (sl2.get('S') or {}).get('law') == u'특허법' and sl2.get('hfold'), {'Ctrl K': sk, '상표': [(sl1.get('S') or {}).get('law'), sl1.get('hfold')], '특허': [(sl2.get('S') or {}).get('law'), sl2.get('hfold')]})
    fold_to(q, False, 'touch')
    q.press(q.ev("r=>__HF.railAt(r)", u'^조문'), 'touch', 1500)
    fold_to(q, True, 'touch')
    bars = q.ev("()=>__HF.bars()"); sj = q.ev("()=>__HF.state()")
    T('h-5', u'조문 갈래(펼쳐서 옮긴 뒤 다시 접음) — 작업 막대(.modebar · .jtbar) 보임 · 접힘', (bars.get('modebar') or bars.get('jtbar')) and sj.get('hfold') and (sj.get('S') or {}).get('tab') == 'jo', {'막대': bars, '상태': sj.get('S')})
    fold_to(q, False, 'touch')
    q.ev("()=>{localStorage.removeItem('jopangi_ui');S.hdrFold=false;return 1}")


def g_h6(p, b, eng):
    G = 'h-6'
    W, H = PC
    hd = {}
    for who, q in (('NEW', p), ('BASE', b)):
        q.size(W, H)
        q.ev("()=>{S.hdrFold=false;return 1}")
        q.ev("l=>__HF.gaek(l)", u'특허법')
        hd[who] = q.ev("()=>__HF.head()")
    n, bb = hd['NEW'], hd['BASE']
    ids_n = [k['id'] for k in n['kids']]; ids_b = [k['id'] for k in bb['kids']]
    T(G, u'PC 1553 펼침 — 머리 = 바탕과 같음(세모만 더해짐 · 머리·검색줄 높이 같음)', [x for x in ids_n if x != 'hdrFold'] == ids_b and 'hdrFold' in ids_n and abs(n['h'] - bb['h']) <= 0.5 and abs((n['hs'] or 0) - (bb['hs'] or 0)) <= 0.5,
      {'NEW': ids_n, 'BASE': ids_b, '높이': [n['h'], bb['h'], n['hs'], bb['hs']]})
    q = p
    q.press(q.ev("()=>__HF.btn()"), 'mouse', 900)
    s1 = q.ev("()=>__HF.state()")
    T(G, u'PC 1553 접음 — 본문 위 끝 = 44(±2 · 시안) · 다섯 요소 없음 · 가로 넘침 0', abs((s1.get('slotTop') or 0) - 44) <= 2 and all(v == 'none' for v in s1['five'].values()) and s1.get('over') == 0, s1)
    q.press(q.ev("()=>__HF.btn()"), 'mouse', 900)
    q.ev("()=>{localStorage.removeItem('jopangi_ui');S.hdrFold=false;return 1}")


PARTS = [('h1', g_h1), ('h2', g_h2), ('h6', g_h6)]


def run_engine(pw, eng):
    br = getattr(pw, eng).launch()
    (ns, nd, ne), (bs, bd, be) = envs()
    try:
        p = Pg(br, eng, 'hfN', ns, nd, ne)
        b = Pg(br, eng, 'hfB', bs, bd, be)
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
        f.write('\n==== %s · %s · NEW %s · 데이터 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), 'hdrfold', os.path.basename(_NEW), _DATA, ','.join(ENGS)))
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[ok], g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:700]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
