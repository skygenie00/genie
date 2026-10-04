# -*- coding: utf-8 -*-
r"""_task_jo_revfix0928night §B 관문 하네스 — book8 교재 자리 창 · add3 기출뷰 고침

  python _harness_jo_revfix0928night.py --new <앱> [--data <jo/data>] [--exam <gichul/pdf>] [--res <결과>] [--eng chromium,webkit] [--only d1,b1,...]

  NEW  = 이 판 앱 + 이 판 데이터(⚙ --dry-run 산출) · BASE = genie HEAD(바로 앞 인도판 = jo_p8sol 6073142) 앱 + 데이터 — 칸마다 헛잣대(바탕에서 FAIL)
  교재 = 비공개 minbeoppdf 로컬 클론(book8 하네스 길 그대로 · 같은 출처 /__book/) · 기록 = 하네스 사본(route) · PUT 밖으로 안 나감
  누름 = 진짜 포인터(page.mouse · 손가락 = Chromium CDP 터치 r22 · WebKit touchscreen.tap) · 자리 = elementFromPoint
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402 — _task_qa_slim(10/4) 실행 모드: --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같다) · 새 갈래는 모두 `if QJ.REGRESS:` / `if QJ.GATE:` 안
import io, json, os, re, sys, time, shutil, subprocess, collections, csv
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
if QJ.SMOKE:   # smoke: Chromium 만
    ENGS = [x for x in ENGS if x == 'chromium']
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_revfix0928night_result.txt'))
sys.argv = [sys.argv[0], '--new', _NEW, '--data', _DATA, '--exam', _EXAM, '--eng', ','.join(ENGS)]
sys.path.insert(0, HERE)
sys.path.insert(0, JOP)
import _harness_jo_book8 as B8   # noqa: E402  (M · serve · /__book/ · __B8 도구)
M = B8.M
M.BASE_REV = '6073142'   # A-6(d) 9/30 — 바탕 = 인도 때 HEAD 6073142(결과 머리 「바탕 HEAD 6073142」) · book8 의 바탕을 물려받지 않는다
M.TESTS = M.TESTS + '\n' + io.open(os.path.join(HERE, '_harness_jo_uid_add3_tests.js'), encoding='utf-8').read() \
    + '\n' + io.open(os.path.join(HERE, '_harness_jo_revfix0928night_tests.js'), encoding='utf-8').read()
M.WORK = M.WORK + '_rn'
from playwright.sync_api import sync_playwright   # noqa: E402
RES = []
U_PIN = 'T2562011'            # 찍어 둔 자리를 심을 지문(book8 표본)
U_CAND = ['TJ0100001']         # 대응표 칸 넷(+ 착수 때 찾은 둘)
COMBO = {('2009', '10'): 4, ('2009', '17'): 3, ('2010', '13'): 2, ('2013', '3'): 2, ('2018', '13'): 3, ('2018', '10'): 2}   # 정답(큐넷) · 2018-10 = ㉠ 꼴 「몇 개」(A-5 로 새로 조합형)
ANS = {'2009-46-9': '4', '2011-48-12': '2', '2022-59-2': '3', '2018-55-1': '2'}
# ★ _task_qa_slim A-2(regress 에서만 · gate 는 옛 고정 대기 그대로): 앱이 이미 내놓는 표지를 기다린다. 자리마다 켜고 끄는 스위치 — 흔들림이 늘면 그 자리만 False 로 되돌린다.
#   표지 목록 = R\_qa_slim_out\_a2\_harness_jo_revfix0928night_표지.md
_A2 = {'win_a': True, 'b1_press': True, 'b4_press': True, 'open_year': True, 'to_q': True, 'g5_opt': True, 'g5_next': True, 'g5_grade': True, 'g6_peek': True, 'g8_next': True}
_PGSIG = "()=>[...document.querySelectorAll('#slot .exv-q')].map(q=>q.dataset.exq).join('|')"   # 기출뷰 쪽 표지 — 지금 쪽의 문항 열쇠 목록(▶ 다음 이 쪽을 갈면 바뀐다)
_SIGCHG = "s=>[...document.querySelectorAll('#slot .exv-q')].map(q=>q.dataset.exq).join('|')!==s"
_EXPOPEN = "k=>{const b=document.getElementById('exb-'+k);const e=b&&b.querySelector('.mbexp');return !!(e&&e.style.display!=='none')}"   # 「정답·해설 ▸」 누름 → 그 선지 해설 칸이 펼쳐짐(uzExvQ 다시 그림)


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def jl(b):
    return json.loads(b.decode('utf-8') if isinstance(b, bytes) else open(b, 'rb').read().decode('utf-8'))


def head(f):
    return jl(M.git('show', '6073142:jo/data/' + f))   # A-6(d) 바탕 데이터 = 인도 때 HEAD 6073142


def new(f):
    return jl(os.path.join(_DATA, f))


# ══════════ 데이터 ══════════
def d1():
    """바뀐 칸 = 할 일 칸만 · 없어진 id·uid 0 · uid_alias 무변 · 정답 = 큐넷 · 조합 선지 다섯 = 옮겨 적은 글"""
    G = 'd1'
    a, b = (head('jimun_특허.json') if QJ.GATE else None), new('jimun_특허.json')
    if QJ.GATE:
        QJ.sub('git:show-data', 4)
        b_d = jl(M.git('show', 'dfbb144:jo/data/jimun_특허.json'))   # A-6(d) 9/30 — 「jimun_특허 바뀐 칸」(인도 검산)만 새 쪽 = 인도 커밋 dfbb144(뒤 판 revfix0929 A-3 이 2013 정답 둘을 더함) · 아래 「정답 넷」(Bq)은 지금 데이터 그대로
        A, Bq, Bq_d = {q['id']: q for q in a['문제']}, {q['id']: q for q in b['문제']}, {q['id']: q for q in b_d['문제']}
        c = collections.Counter(); qch = []
        for i, qb in Bq_d.items():
            qa = A.get(i)
            if qa is None:
                c['새 문항'] += 1; continue
            for k in set(qa) | set(qb):
                if k != '지문' and qa.get(k) != qb.get(k):
                    c['문항.' + k] += 1; qch.append((i, k, qa.get(k), qb.get(k)))
            for za, zb in zip(qa['지문'], qb['지문']):
                for k in set(za) | set(zb):
                    if za.get(k) != zb.get(k):
                        c['선지.' + k] += 1
        gone = set(A) - set(Bq_d)
        ua = {z.get('uid') for q in a['문제'] for z in q['지문']} - {z.get('uid') for q in b_d['문제'] for z in q['지문']}
        ok = dict(c) == {'문항.정답': 4, '선지.sol': 65, '선지.sol7': 65} and not gone and not ua and all(ANS.get(i) == v for i, k, _, v in qch)
        T(G, 'jimun_특허 — 바뀐 칸 = 문항 정답 4(큐넷) · 선지 sol 65 + sol7 65(A-6) · 없어진 문항·uid 0', ok, {'셈': dict(c), '정답': qch, '없어짐': [len(gone), len(ua)]})
        p, q_d = head('jimun_7pan.json'), jl(M.git('show', 'dfbb144:jo/data/jimun_7pan.json'))   # A-6(d) 9/30 — 「jimun_7pan 바뀐 칸」(인도 검산)만 새 쪽 = 인도 커밋 dfbb144(뒤 판 revfix0929 A-1 이 16 줄 sol 을 되돌림) · 지금 원장은 g6·g9 가 잰다
        P, Q = {z['id']: z for z in p['지문']}, {z['id']: z for z in q_d['지문']}
        ch = collections.Counter(tuple(sorted(k for k in set(P[i]) | set(Q[i]) if P[i].get(k) != Q[i].get(k))) for i in Q if i in P and P[i] != Q[i])
        mg = [i for i in Q if i in P and Q[i].get('병합') == 'Y' and P[i].get('병합') != 'Y']
        T(G, 'jimun_7pan — 바뀐 칸 = 병합 67(A-9 · add3 시험지 줄과 같은 uid 인 7판 줄) · 다른 칸·줄 무변 · 지문 수 같음', dict(ch) == {('병합',): 67} and len(mg) == 67 and len(P) == len(Q),
          {'셈': {str(k): v for k, v in ch.items()}, '표본': mg[:5]})
    else:
        # regress: 바탕 데이터(6073142 · dfbb144 git show)를 안 푼다 — #1 #2 는 두 옛 커밋끼리 맞대는 인도 검산(gate 몫). 아래 「정답 넷」 칸이 쓰는 NEW 문항 표만 만든다
        Bq = {q['id']: q for q in b['문제']}
    if QJ.GATE:
        T(G, 'uid_alias.json 무변', open(os.path.join(_DATA, 'uid_alias.json'), 'rb').read() == M.git('show', 'HEAD:jo/data/uid_alias.json'), '')
    else:
        # 기준 칸 — uid_alias.json 무변: 바탕(HEAD) blob 을 안 푼다 · 저장된 바탕 스냅샷(md5)과 맞댄다
        import hashlib
        _hu = hashlib.md5(open(os.path.join(_DATA, 'uid_alias.json'), 'rb').read()).hexdigest()
        T(G, 'uid_alias.json 무변', QJ.norm(_hu) == QJ.base('d1#uid_alias', _hu), QJ.base_note('d1#uid_alias'))
    cb = new('exam_combo.json')['특허']
    want = {('2009', '10'): 'A: 30일 B: 1년 6월 C: 3년', ('2009', '17'): 'ㄱ, ㄴ, ㅁ', ('2010', '13'): 'ㄴ, ㄷ', ('2013', '3'): 'ㄱ, ㄹ', ('2018', '13'): 'ㄱ, ㄷ, ㄹ', ('2018', '10'): '1개'}
    got = {'%s-%s' % k: (cb.get(k[0], {}).get(k[1]) or [None] * 5) for k in want}
    ok = all(len(got['%s-%s' % k]) == 5 and got['%s-%s' % k][COMBO[k] - 1] == v for k, v in want.items())
    T(G, 'exam_combo — 2009-10·17 · 2010-13 · 2013-3 · 2018-13 다섯 줄 · 정답 번호 자리 글 = 정답 조합(2009-10 ④ = A 30일·B 1년 6월·C 3년 등)', ok, got)
    # 정답 = 큐넷 csv
    rd = list(csv.DictReader(io.open(os.path.join(JOP, '공통', '_재료', '_최종정답.csv'), encoding='utf-8-sig')))
    qn = {(r['연도'], r['법'], r['문번']): r['정답'] for r in rd}
    tab = {i: (Bq[i]['연도'], Bq[i]['시험문번'], Bq[i]['정답'], qn.get((str(Bq[i]['연도']), '특허', str(Bq[i]['시험문번'])))) for i in ANS}
    T(G, '정답 넷 = 큐넷 최종정답(2009 2번 ④ · 2013 3번 ② · 2018 13번 ③ · 2020 7번 ②)', all(v[2] == v[3] for v in tab.values()), tab)


# ══════════ 교재 자리 창 ══════════
def win_at(p, y, how):
    p.ev("()=>__B8.closeBox()")
    at = p.ev("a=>__RN.idTo(a[0],a[1])", [U_PIN, y])
    p.press(at, how, 700 if QJ.GATE or not _A2['win_a'] else 0)
    p.ev("()=>__B8.picReady()")
    # 남는 고정 대기(regress 에도 그대로 · page.wait_for_timeout 유지 — QJ.sleep 은 time.sleep 이라 그동안 Playwright route 가 안 돌아 선 요청이 멎는다): 그림 뒤 창 맞춤(ncPicFit · mbWinFit)의 늦은 패스 — 앱이 끝 표지를 안 내놓는다(revfix0929 probe 가 그 차례를 잼)
    p.pg.wait_for_timeout(700)
    return at, p.ev("()=>__RN.boxWin()")


def b1(p, b, eng, br):
    """A-1 — 찍어 둔 자리(심은 기록) · ID 칩 y 셋 · 그림 뒤 창 bottom ≤ 보이는 화면 − 8 · 단추 둘 elementFromPoint · 누름 동작 · 폰도"""
    G = 'b1'
    ns, nd, ne = M.new_env()
    if QJ.GATE:
        QJ.sub('git:show-app'); QJ.sub('git:archive', 2)
        bs, bd, be = M.base_env()
    for (W, H, how, ys) in ((1440, 900, 'mouse', (300, 500, 700)), (390, 844, 'touch', (300, 420, 600))):
        for tag, src, dd, ee in ((('NEW', ns, nd, ne), ('헛', bs, bd, be)) if QJ.GATE else (('NEW', ns, nd, ne),)):
            q = B8.Pg(br, eng, 'rnW%d%s' % (W, tag), src, dd, ee, W=W, H=H)
            QJ.launch('new' if tag == 'NEW' else 'base')   # 새 컨텍스트 유지: 열기 횟수 순서가 잣대(b1 · b4 의 창 위치 칸) — 앞 열기가 쌓인 페이지를 재쓰면 같은 결함이 다른 열기에서 난다
            try:
                B8.home(q)
                q.ev("a=>__RN.pinSeed(a[0],a[1],a[2])", [U_PIN, 70, [0.1, 0.3, 0.9, 0.4]])
                B8.go_key(q, U_PIN)
                res = {}
                for y in ys:
                    at, w = win_at(q, y, how)
                    res[y] = {'칩': at and at.get('cy'), '창': w and w['rect'], 'rv': w and w['rv'] and w['rv']['on'], 'pk': w and w['pk'] and w['pk']['on'], 'pic': w and w['pic']}
                lim = H - 8
                ok = all(r['창'] and r['창']['b'] <= lim + 0.5 and r['rv'] and r['pk'] and r['pic'] for r in res.values())
                if tag == 'NEW':
                    T(G, '%s %d×%d %s — ID 칩 y %s · 그림 들어온 뒤 창 bottom ≤ %d · 「자동으로 되돌리기」·「📍 자리 직접 찍기」 elementFromPoint = 그 단추' % (eng, W, H, '마우스' if how == 'mouse' else '손가락', '/'.join(map(str, ys)), lim), ok, res)
                    # 누름 동작 — 맨 아래 칩 자리에서 「📍 자리 직접 찍기」 → 8판 쪽 창(찍기) · 「자동으로 되돌리기」 → 칸 auto
                    _, w = win_at(q, ys[-1], how)
                    q.press(w and w['pk'], how, 900 if QJ.GATE or not _A2['b1_press'] else 0)
                    bk = q.ev("()=>__B8.bookReady()")
                    q.ev("()=>__B8.closeAll()")
                    _, w = win_at(q, ys[-1], how)
                    q.press(w and w['rv'], how, 900 if QJ.GATE or not _A2['b1_press'] else 0)
                    if QJ.REGRESS and _A2['b1_press']:   # 「자동으로 되돌리기」 핸들러가 localStorage jopangi.canvasjari 의 p8|<uid> 칸에 {auto:true} 를 적는다(jo/index.html 10687) — 그 표지를 기다린다(옛 900ms)
                        QJ.until(q.pg, "u=>{try{const x=JSON.parse(localStorage.getItem('jopangi.canvasjari')||'{}')['p8|'+u];return !!(x&&x.auto)}catch(e){return false}}", 5000, 'b1: 자동으로 되돌리기 → 칸 auto', arg=U_PIN)
                    pin = q.ev("u=>__B8.pin(u)", U_PIN)
                    T(G, '%s %d×%d %s — 칩 y %d 에서 단추 누름: 「📍 자리 직접 찍기」 → 8판 쪽 창(찍기 덮개) · 「자동으로 되돌리기」 → 칸 {auto}' % (eng, W, H, how, ys[-1]),
                      bool(bk and bk.get('n') and bk.get('ov')) and bool(pin and pin.get('auto')), {'쪽 창': bk and {k: bk.get(k) for k in ('n', 'ov', 'page')}, '칸': pin})
                else:
                    T(G + '-헛', '%s %d×%d 헛잣대 바탕 — 어느 칩 자리에서 창이 화면 밖으로 나가거나 단추가 안 잡힘' % (eng, W, H), not ok, res)
            finally:
                q.close()


def b1nc(p, b, eng):
    """A-1 정리캔버스 목차노트 「교재 자리」 창과 같은 ncPic — 창 하나(popShell · mbWinFrame)에 ncPic 을 넣어 같은 잣대(합성 · 그 창의 채움 길은 ncBookFill 그대로)"""
    G = 'b1nc'
    for tag, q in (('NEW', p), ('헛', b)):
        if tag == '헛' and QJ.REGRESS:   # regress: 바탕 판을 안 띄운다
            continue
        B8.home(q)
        r = q.ev("""async()=>{try{closeAllPops();}catch(e){}
          const J=viewCanvas.jari; try{await J.meta8();}catch(e){}
          const body=popShell('ncbook','교재 자리 — 하네스','ncbook|하네스|x|1'); const pop=body.parentNode; mbWinFrame(pop);
          const host=el('div','mbblist'); body.appendChild(host);
          host.appendChild(p8Row(J,P8B,{p:70,r:[0.1,0.3,0.9,0.4]},'찍어 둔 자리',()=>{}));
          host.appendChild(ncPic(J,P8B,{p:70,r:[0.1,0.3,0.9,0.4]},()=>{}));
          const rv=el('button','ncb-more','자동으로 되돌리기'); host.appendChild(rv);
          pop.style.left='500px'; pop.style.top=(innerHeight-200)+'px';
          for(let i=0;i<300&&!host.querySelector('.ncb-pic canvas');i++) await new Promise(r=>setTimeout(r,50));
          await new Promise(r=>setTimeout(r,500)); return __RN.ncWin();}""")
        ok = bool(r) and r['pic'] and r['rect']['b'] <= r['vv']['h'] - 7.5 and r['rv'] and r['rv']['on']
        if tag == 'NEW':
            T(G, '%s ncPic 창(아래 끝에서 열림) — 그림 뒤 창 bottom ≤ 보이는 화면 − 8 · 「자동으로 되돌리기」 잡힘' % eng, ok, r)
        else:
            T(G + '-헛', '%s 헛잣대 바탕 — 창이 화면 밖' % eng, not ok, r)
        q.ev("()=>__B8.closeAll()")


def b23(p, b, eng):
    """A-2 8판 줄 「p.」 · A-3 후보 2·3등"""
    G = 'b23'
    D = jl(os.path.join(B8.W8, '대응.json'))
    four = [u for u, L in D.items() if not u.startswith('_') and isinstance(L, list) and len(L) >= 4]
    sm = U_CAND + [u for u in four if u not in U_CAND][:2]
    for tag, q in (('NEW', p), ('헛', b)):
        if tag == '헛' and QJ.REGRESS:   # regress: 바탕 판을 안 띄운다
            continue
        out = {}
        for u in sm:
            B8.go_key(q, u) or B8.open_card(q, u)
            B8.open_box(q, u)
            q.ev("()=>__B8.snipReady()")
            m = q.ev("()=>__B8.btnAt('후보')")
            q.press(m, 'mouse', 500)
            w = q.ev("()=>__RN.boxWin()")
            out[u] = {'후보': [x for x in (w or {}).get('more', []) if x.startswith('후보')], '펼친 줄': (w or {}).get('moreRows'), '머리': [r['hd'] for r in (w or {}).get('rows', [])][:2],
                      'p': [r['p'] for r in (w or {}).get('rows', [])]}
        if tag == 'NEW':
            ok = all(v['후보'] == ['후보 2'] and v['펼친 줄'] == 2 for v in out.values())
            T(G, '%s A-3 대응표 칸 넷 이상 %d 개 중 표본 %s — 「후보 2」 · 펼친 줄 2(2·3등)' % (eng, len(four), '·'.join(sm)), ok, out)
            ok2 = all(all(x.startswith('p.') for x in v['p']) and not any(x.endswith('쪽') for x in v['p']) for v in out.values())
            T(G, '%s A-2 8판 줄 머리 「특허법 해례 8판 · p.N · PDF N · …」 — 「p.」 있음 · 「쪽」 0(8판 줄만)' % eng, ok2, {u: v['머리'] for u, v in out.items()})
            omr = q.ev("()=>{const w=(POPS||[]).filter(x=>/^cell\\|📚 교재 자리/.test(x._pk||'')).pop();const r=w&&[...w.querySelectorAll('.mbbrow')].find(r=>!r.closest('.mbb8'));return r?r.querySelector('.hd .p').textContent:null}")
            srcok = q.ev("()=>String(ncRow).indexOf(\"J.pr(bk, s.p) + '쪽'\")>=0 && String(mbbPop).indexOf(\"pin.page + '쪽'\")>=0")
            T(G, '%s A-2 민법·정리캔버스 교재 줄은 「N쪽」 그대로 — 같은 창 정리OMR 줄 %r · ncRow·mbbPop 글 틀 무변' % (eng, omr), srcok and (omr is None or omr.endswith('쪽') or omr == '아직 안 찍음'), {'정리OMR': omr})
        else:
            T(G + '-헛', '%s 헛잣대 바탕 — 「후보 3」 이상 · 머리 「N쪽」' % eng, any(v['후보'] and v['후보'] != ['후보 2'] for v in out.values()) and any(x.endswith('쪽') for v in out.values() for x in v['p']), out)
        q.ev("()=>__B8.closeAll()")


PH_BOOK = "()=>{const w=(POPS||[]).filter(x=>/^cv\\|book\\|/.test(x._pk||'')).pop();const h=w&&w.querySelector('.ph');return h?+h.getBoundingClientRect().height.toFixed(2):null}"   # ★ jo_theme(10/1) 쪽 창 머리 높이


def b4(p, b, eng, br):
    """A-4 폰 교재 쪽 창 높이 ≥ 0.6 × 보이는 높이 · 화면 안 · 민소 교재 창 같은 잣대 · PC·아이패드 창 크기 무변(바탕과 같음)"""
    G = 'b4'
    ns, nd, ne = M.new_env()
    if QJ.GATE:
        QJ.sub('git:show-app'); QJ.sub('git:archive', 2)
        bs, bd, be = M.base_env()
    sizes = {}
    for (W, H, how) in ((390, 844, 'touch'), (1440, 900, 'mouse'), (1024, 1366, 'touch')):
        for tag, src, dd, ee in ((('NEW', ns, nd, ne), ('BASE', bs, bd, be)) if QJ.GATE else (('NEW', ns, nd, ne),)):
            q = B8.Pg(br, eng, 'rnB%d%s' % (W, tag), src, dd, ee, W=W, H=H)
            QJ.launch('new' if tag == 'NEW' else 'base')   # 새 컨텍스트 유지: 열기 횟수 순서가 잣대
            try:
                B8.home(q)
                q.ev("u=>__RN.pinDel(u)", U_PIN)
                B8.go_key(q, U_PIN)
                r8 = []
                for y in ((300, 600, 780) if W == 390 else (300, 700)):
                    q.ev("()=>__B8.closeAll()")
                    at = q.ev("a=>__RN.idTo(a[0],a[1])", [U_PIN, y])
                    q.press(at, how, 700 if QJ.GATE or not _A2['b4_press'] else 0)
                    q.ev("()=>__B8.snipReady()")
                    ra = q.ev("()=>__B8.rowAt(0)")
                    q.press(ra, how, 900 if QJ.GATE or not _A2['b4_press'] else 0)
                    q.ev("()=>__B8.bookReady()")
                    w8 = q.ev("()=>__RN.bookWin()")
                    r8.append(dict(w8, press=(ra or {}).get('cy'), ph=q.ev(PH_BOOK)) if w8 else w8)   # ★ jo_theme(10/1) 머리 높이 ph 도 · A-6(a) 9/30 — 누른 8판 줄 자리도 적는다(revfix0930 A-6 bkPlace 로 📚 창이 칩 아래 +6 에 가서 이 자리가 옮겨짐)
                q.ev("()=>__B8.closeAll()")
                q.ev("()=>{try{viewCanvas.book({book:'핵심',page:5},{clientX:100,clientY:%d});}catch(e){}}" % int(H * 0.85))
                q.until("()=>{const w=(POPS||[]).filter(x=>/^cv\|book\|/.test(x._pk||'')).pop();return !!w&&(!!w.querySelector('.cv-bookpg canvas')||/받지 못했다/.test(w.textContent))}", ms=30000)   # 교재가 다 열린 뒤 잰다(받는 중 창은 낮다)
                # 남는 고정 대기(regress 에도 그대로 · page.wait_for_timeout 유지): 민소 교재 쪽 창 — 그림이 선 뒤 창 맞춤(bkPlace · mbWinFit)의 늦은 패스 · 앱이 끝 표지를 안 내놓는다
                q.pg.wait_for_timeout(500)
                rm = q.ev("()=>__RN.bookWin()")
                rm = dict(rm, ph=q.ev(PH_BOOK)) if rm else rm   # ★ jo_theme(10/1) 머리 높이
                sizes[(W, tag)] = {'8판': r8, '민소': rm}
            finally:
                q.close()
    n = sizes[(390, 'NEW')]
    chk = lambda w: bool(w) and w['rect']['h'] >= 0.6 * w['vv']['h'] - 0.5 and w['rect']['y'] >= w['vv']['y'] - 0.5 and w['rect']['b'] <= w['vv']['y'] + w['vv']['h'] + 0.5
    T(G, '%s 폰 390×844 손가락 — 8판 쪽 창(칩 y 300·600·780 에서 연 셋) 높이 ≥ 0.6×보이는 높이 · 창 전체 화면 안' % eng, all(chk(w) for w in n['8판']),
      [w and {'rect': w['rect'], 'vv': w['vv']} for w in n['8판']])
    T(G, '%s 폰 — 민소 교재 창(정리캔버스 · 같은 bookShow · 아래쪽에서 엶) 같은 잣대' % eng, chk(n['민소']), n['민소'] and n['민소']['rect'])
    if QJ.GATE:
        bb = sizes[(390, 'BASE')]
        T(G + '-헛', '%s 헛잣대 바탕 폰 — 8판 쪽 창 가운데 높이 < 0.6×보이는 높이인 것 있음' % eng, not all(chk(w) for w in bb['8판']), [w and w['rect'] for w in bb['8판']])
    for W in (1440, 1024):
        a1, a2 = sizes[(W, 'NEW')], (sizes[(W, 'BASE')] if QJ.GATE else QJ.base('b4@%s/%d' % (eng, W), sizes[(W, 'NEW')]))   # 기준 칸 — 바탕 창 크기·자리 = 이 판 앞 인도판 스냅샷
        # A-6(a) 9/30 — revfix0930 A-6(bkPlace): PC·아이패드 📚 창이 누른 칩 아래(칩 아래 +6)로 간다(옛 = 누른 자리 +14 · 칩 y 300 → 창 314 → 316) → 창 안 8판 줄 누름 자리도 그만큼 옮겨진다.
        #   쪽 창은 누른 자리에 뜨므로(showPop 누른 자리 +34) 바닥에 붙지 않은 쪽 창은 누른 자리 차이만큼 같이 옮겨지는 것이 무변 · 바닥에 붙은 창(PC 셋 · 아이패드 칩 y 700 · 민소)은 자리 그대로 · 높이·폭은 그대로 잰다
        dy = lambda x, y: 0 if abs(y['rect']['b'] - (y['vv']['y'] + y['vv']['h'] - 8)) < 0.6 else (x.get('press') or 0) - (y.get('press') or 0)
        # ★ jo_theme(10/1) A-7 팝업 틀 — 머리(.ph) 높이가 바뀌었다(chromium 31.44 → 39 · webkit 34.44 → 39 · _task_jo_theme.md 81·82줄 · B-9 는 폭·끌기·크기 조절만 바탕과 같게)
        #   → 높이 = 바탕 그대로(PC: 남은 자리로 정해짐) 또는 몸통(높이 − 머리) = 바탕(아이패드: 머리 + 내용) · 바닥에 붙은 창 위 끝 = 바탕 또는 머리 차만큼 위 · 폭 · 누른 줄 기준 자리는 그대로
        pin = lambda y: abs(y['rect']['b'] - (y['vv']['y'] + y['vv']['h'] - 8)) < 0.6
        dph = lambda x, y: (x.get('ph') or 0) - (y.get('ph') or 0)
        hok = lambda x, y: abs(x['rect']['h'] - y['rect']['h']) < 0.6 or abs((x['rect']['h'] - (x.get('ph') or 0)) - (y['rect']['h'] - (y.get('ph') or 0))) < 0.6
        yok = lambda x, y: abs(x['rect']['y'] - y['rect']['y'] - dy(x, y)) < 0.6 or (pin(y) and abs(x['rect']['y'] - y['rect']['y'] + dph(x, y)) < 0.6)
        same = all(x and y and hok(x, y) and abs(x['rect']['w'] - y['rect']['w']) < 0.6 and yok(x, y) for x, y in zip(a1['8판'] + [a1['민소']], a2['8판'] + [a2['민소']]))
        T(G, '%s %s 창 크기·자리 = 바탕(무변%s)' % (eng, 'PC 1440×900' if W == 1440 else '아이패드 1024×1366', '' if W == 1440 else ' · 쪽 창 자리 = 누른 8판 줄 기준 — revfix0930 A-6'), same,
          {'NEW': [x and dict(x['rect'], press=x.get('press'), ph=x.get('ph')) for x in a1['8판'] + [a1['민소']]], ('BASE' if QJ.GATE else '기준 스냅샷'): [x and dict(x['rect'], press=x.get('press'), ph=x.get('ph')) for x in a2['8판'] + [a2['민소']]]})


# ══════════ 기출뷰 ══════════
def open_year(p, y, how='mouse'):
    B8.home(p)
    p.ev("y=>{S.exvPg=S.exvPg||{};S.exvPg[PLAW()+':'+y]=0;}", str(y))   # 앱이 해마다 쪽 자리를 기억한다 — 첫 쪽부터(▶ 다음 만 누른다)
    at = p.ev("y=>__U3.yearRow(y)", str(y))
    ok = p.press(at, how, 2500 if QJ.GATE or not _A2['open_year'] else 0)
    if QJ.REGRESS and _A2['open_year']:   # 고정 2.5초 대신 — 그 해 시험지(.exv-paper[data-uzexv])와 머리(.mbsbar.uzexh .pg)가 서는 것을 기다린다(jo/index.html uzExv 18603~ · mbBackBar 13746 → uzExvHead 18789)
        QJ.until(p.pg, "y=>!!document.querySelector('#slot .exv-paper[data-uzexv=\"'+y+'\"]')&&!!document.querySelector('#slot .mbsbar.uzexh .pg')", 15000, 'open_year: 해 시험지 + 머리', arg=str(y))
    p.until("()=>document.querySelectorAll('#slot .exv-q').length>0", ms=15000)
    return ok


def to_q(p, k, how='mouse', most=5):
    for _ in range(most):
        q = p.ev("k=>__U3.exvQ(k)", k)
        if q and q['vis']:
            return q
        nx = p.ev("()=>__U3.next()")
        if QJ.REGRESS and _A2['to_q']:
            _sg = p.ev(_PGSIG)
        if not p.press(nx, how, 1200 if QJ.GATE or not _A2['to_q'] else 0):
            break
        if QJ.REGRESS and _A2['to_q']:   # 고정 1.2초 대신 — ▶ 다음 이 쪽을 갈면 문항 열쇠 목록이 바뀐다(uzExv 가 새로 그림)
            QJ.until(p.pg, _SIGCHG, 8000, 'to_q: ▶ 다음 → 문항 목록이 바뀜', arg=_sg)
    return p.ev("k=>__U3.exvQ(k)", k)


EXQ = """k=>{const q=document.querySelector('#slot .exv-q[data-exq="'+k+'"]');if(!q)return null;const t=e=>e?(e.textContent||'').replace(/\\s+/g,' ').trim():'';
  const opts=[...q.querySelectorAll('.exv-opt')].map(b=>t(b));
  const boxes=[...q.querySelectorAll('.question-box')].map(b=>{const ch=[...b.querySelectorAll('.jxec')].map(t);return {lab:t(b.querySelector('.uzexlab')),chips:ch,dup:ch.length-new Set(ch).size};});
  return {opts,wait:t(q.querySelector('.exv-wait')),miss:[...q.querySelectorAll('.exv-miss')].map(t),boxes};}"""
OPTAT = """a=>{const q=document.querySelector('#slot .exv-q[data-exq="'+a[0]+'"]');const b=q&&q.querySelector('.exv-opt[data-exn="'+a[1]+'"]');if(!b)return null;b.scrollIntoView({block:'center'});
  const r=b.getBoundingClientRect(),at=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return {cx:r.left+r.width/2,cy:r.top+r.height/2,on:!!at&&b.contains(at)};}"""


def g5(p, b, eng):
    """A-5 조합 선지 — 다섯 문항 선지 단추 5 · 「읽지 못했습니다」 0 · 「데이터에 없음」 0 · 보기 칩 겹침 0 · 정답 번호 누름 → 채점 O · 2009 전체 채점"""
    G = 'g5'
    for tag, q in (('NEW', p), ('헛', b)):
        if tag == '헛' and QJ.REGRESS:   # regress: 바탕 판을 안 띄운다
            continue
        B8.home(q)
        q.ev("()=>{window.confirm=()=>true;}")
        res = {}
        for (y, no), ans in COMBO.items():
            open_year(q, y)
            k = '특허:%s:%s' % (y, no)
            to_q(q, k)
            q.until("k=>{const q=document.querySelector('#slot .exv-q[data-exq=\"'+k+'\"]');return q&&!/읽는 중/.test(q.textContent)}", k, ms=15000)
            r = q.ev(EXQ, k)
            if tag == 'NEW' and r and len(r['opts']) == 5:
                q.press(q.ev(OPTAT, [k, ans]), 'mouse', 500 if QJ.GATE or not _A2['g5_opt'] else 0)
                if QJ.REGRESS and _A2['g5_opt']:   # 고정 0.5초 대신 — 선지 단추 누름은 giPut 으로 고른 답을 기억에 적는다(uzExvPick)
                    QJ.until(q.pg, "k=>!!((giAll()[k]||{}).p)", 3000, 'g5: 정답 번호 단추 → 고른 답 기록(giAll)', arg=k)
            res['%s-%s' % (y, no)] = dict(r or {}, 고름=q.ev("k=>(giAll()[k]||{}).p||null", k))
        if tag == 'NEW':
            ok = all(v.get('opts') and len(v['opts']) == 5 and not v['wait'] and not v['miss'] and all(x['dup'] == 0 for x in v['boxes']) and v['고름'] == str(COMBO[tuple(kk.split('-'))])
                     for kk, v in res.items())
            T(G, '%s 2009-10·17 · 2010-13 · 2013-3 · 2018-13 · 2018-10 — 선지 단추 5 · 「읽지 못했습니다」 0 · 「데이터에 없음」 0 · 보기 칩 겹침 0 · 정답 번호 단추 누름(마우스) → 고른 답 기록' % eng, ok, res)
            # 2009 전체 채점 — 모든 문항 답 고름(나머지는 심음) · 10·17 은 방금 누른 정답
            q.ev("()=>{const G=giAll();((VJ&&VJ.qs)||[]).filter(q=>String(q.연도)==='2009'&&giGradable(q)).forEach(q=>{const k=giKey(q);if(!(G[k]&&G[k].p))G[k]=Object.assign({},G[k]||{},{p:'1',ts:new Date().toISOString()});});GIREC=G;lsWrite(GI_KEY,G,'하네스');}")
            open_year(q, 2009)
            for _ in range(5):
                if q.ev("()=>__U3.grade()"):
                    break
                if QJ.REGRESS and _A2['g5_next']:
                    _sg = q.ev(_PGSIG)
                if not q.press(q.ev("()=>__U3.next()"), 'mouse', 1200 if QJ.GATE or not _A2['g5_next'] else 0):
                    break
                if QJ.REGRESS and _A2['g5_next']:   # 고정 1.2초 대신 — 쪽이 갈리면 문항 열쇠 목록이 바뀐다
                    QJ.until(q.pg, _SIGCHG, 8000, 'g5: ▶ 다음 → 문항 목록이 바뀜', arg=_sg)
            q.ev("()=>{window.__TOASTS&&(window.__TOASTS.length=0)}")
            q.press(q.ev("()=>__U3.grade()"), 'mouse', 1500 if QJ.GATE or not _A2['g5_grade'] else 0)
            if QJ.REGRESS and _A2['g5_grade']:   # 고정 1.5초 대신 — 전체 채점(uzExvGradeAll → giGrade)은 그 해 기록에 제출 시각(sub)을 적거나 「답을 안 고른 문제」 토스트를 낸다
                QJ.until(q.pg, "()=>{const r=__U3.yearOf(2009);return !!(r&&r.year&&r.year.sub)||__HM.toasts().length>0}", 8000, 'g5: 전체 채점 → 해 기록(sub) 또는 토스트')
            yr = q.ev("()=>__U3.yearOf(2009)")
            ok10 = q.ev("()=>({a:(giAll()['특허:2009:10']||{}).ok,b:(giAll()['특허:2009:17']||{}).ok})")
            toasts = q.ev("()=>__HM.toasts()")
            T(G, '%s 2009 「전체 채점 ✓」 — 「답을 안 고른 문제」 토스트 0 · 점수 뜸(분모 16) · 10·17 번 정답 = 맞음' % eng,
              not any('답을 안 고른' in t for t in toasts) and ((yr or {}).get('year') or {}).get('n') == 16 and ok10 == {'a': True, 'b': True}, {'기록': yr, '10·17': ok10, '토스트': toasts[-2:]})
            nc = q.ev("()=>['2005-42-2','2005-42-5','2005-42-10'].map(i=>{const x=((VJ&&VJ.qs)||[]).find(q=>q.id===i);return x?uzIsCombo(x):null})")
            T(G, '%s 시험지 없는 해 ㉠ 꼴 셋(2005-42-2·5·10) — 조합형 아님(무변 · 조합 선지를 못 읽으므로)' % eng, nc == [False, False, False], nc)
        else:
            T(G + '-헛', '%s 헛잣대 바탕 — 어느 문항이 「읽지 못했습니다」 또는 「데이터에 없음」 또는 칩 겹침' % eng,
              any((not v.get('opts')) or v.get('wait') or v.get('miss') or any(x['dup'] for x in v.get('boxes', [])) for v in res.values()), res)


def g6(p, b, eng):
    """A-6 해설 잇기 — 데이터 셈 = 기출뷰 해설 보이는 수 · 표본 셋 해설 글 = 7판 줄 sol · 짝 없는 선지 「해설 없음」 · 고친 해설(심은 기록)이 이김"""
    G = 'g6'
    J7 = {z['id']: z for z in new('jimun_7pan.json')['지문']}
    B = new('jimun_특허.json')
    lk = [(q, z) for q in B['문제'] for z in q['지문'] if z.get('sol7')]
    S = [('2017-54-B18', '1')] + [(q['id'], z['n']) for q, z in lk if q['id'] != '2017-54-B18'][:2]
    B8.home(p)
    vis = p.ev("()=>((VJ&&VJ.qs)||[]).reduce((n,q)=>n+(q.지문||[]).filter(z=>z.sol7&&(z.sol||'').trim()).length,0)")
    T(G, '%s 새 선지 중 7판 짝 해설 있는 것 = %d · 앱이 읽은 데이터에서 해설 서는 수 = %d' % (eng, len(lk), vis), len(lk) == 65 and vis == 65, '')
    out = {}
    for qid, n in S:
        qq = next(q for q in B['문제'] if q['id'] == qid); z = next(z for z in qq['지문'] if str(z['n']) == str(n))
        y, no = str(qq['연도']), str(qq['시험문번'])
        open_year(p, y); k = '특허:%s:%s' % (y, no); to_q(p, k)
        zk = p.ev("a=>__U3.keyOf(a[0],a[1])", [qid, n])
        pk = p.ev("k=>{const q=document.querySelector('#slot .exv-q[data-exq=\"'+k+'\"]');const b=q&&q.querySelector('.exv-peek');if(!b)return null;b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return {cx:r.left+r.width/2,cy:r.top+r.height/2,on:true}}", k)
        p.press(pk, 'mouse', 700 if QJ.GATE or not _A2['g6_peek'] else 0)
        if QJ.REGRESS and _A2['g6_peek']:   # 고정 0.7초 대신 — 「정답·해설 ▸」 누름은 그 문항을 열린 꼴로 다시 그린다(uzExvQ · .mbexp 보임)
            QJ.until(p.pg, _EXPOPEN, 3000, 'g6: 정답·해설 ▸ → 해설 칸 열림', arg=zk)
        box = p.ev("k=>{const b=document.getElementById('exb-'+k);if(!b)return null;const s=b.querySelector('.mbexp .sol,.mbexp .cdim');return s?s.textContent:null}", zk)
        out['%s ①' % qid if n == '1' else '%s %s' % (qid, n)] = {'dom': (box or '')[:50], 'p7': z['sol7'], 'same': re.sub(r'\s+', '', box or '') == re.sub(r'\s+', '', J7[z['sol7']]['sol'])}
    T(G, '%s 표본 셋(2017-18 ① 포함) — 기출뷰 「정답·해설 ▸」 누름 → 해설 글 = 같은 uid 7판 줄 sol(8판 해설로 올린 값)' % eng, all(v['same'] for v in out.values()), out)
    # 고친 해설이 이긴다 — 기억에만 심음(QFIXREC)
    qid, n = S[0]; zk = p.ev("a=>__U3.keyOf(a[0],a[1])", [qid, n])
    p.ev("k=>{const A=qfixAll();A[k]=Object.assign({},A[k]||{},{exp:'내가 고친 해설 표본'});QFIXREC=A;}", zk)
    open_year(p, '2017'); to_q(p, '특허:2017:18')
    pk = p.ev("()=>{const q=document.querySelector('#slot .exv-q[data-exq=\"특허:2017:18\"]');const b=q&&q.querySelector('.exv-peek');if(!b)return null;if(/▾/.test(b.textContent))return 'open';b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return {cx:r.left+r.width/2,cy:r.top+r.height/2,on:true}}")
    if isinstance(pk, dict):
        p.press(pk, 'mouse', 700 if QJ.GATE or not _A2['g6_peek'] else 0)
        if QJ.REGRESS and _A2['g6_peek']:
            QJ.until(p.pg, _EXPOPEN, 3000, 'g6: 정답·해설 ▸ → 해설 칸 열림', arg=zk)
    fx = p.ev("k=>{const b=document.getElementById('exb-'+k);const s=b&&b.querySelector('.mbexp .sol,.mbexp .cdim');return s?s.textContent:null}", zk)
    p.ev("k=>{const A=qfixAll();delete A[k];QFIXREC=A;}", zk)
    T(G, '%s 고친 해설(기억에만 심음) — 기출뷰 해설 = 고친 글' % eng, (fx or '').strip() == '내가 고친 해설 표본', fx)
    # 7판 짝 없는 새 선지 — 해설 없음 그대로
    nz = [(q, z) for q in B['문제'] if re.search(r'-B\d+$', q['id']) for z in q['지문'] if not (z.get('sol') or '').strip()][:1]
    if nz:
        q0, z0 = nz[0]
        open_year(p, str(q0['연도'])); to_q(p, '특허:%s:%s' % (q0['연도'], q0['시험문번']))
        zk = p.ev("a=>__U3.keyOf(a[0],a[1])", [q0['id'], z0['n']])
        pk = p.ev("k=>{const q=document.querySelector('#slot .exv-q[data-exq=\"'+k+'\"]');const b=q&&q.querySelector('.exv-peek');if(!b||/▾/.test(b.textContent))return null;b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return {cx:r.left+r.width/2,cy:r.top+r.height/2,on:true}}", '특허:%s:%s' % (q0['연도'], q0['시험문번']))
        p.press(pk, 'mouse', 700 if QJ.GATE or not _A2['g6_peek'] else 0)
        if QJ.REGRESS and _A2['g6_peek']:
            QJ.until(p.pg, _EXPOPEN, 3000, 'g6: 정답·해설 ▸ → 해설 칸 열림', arg=zk)
        e0 = p.ev("k=>{const b=document.getElementById('exb-'+k);const s=b&&b.querySelector('.mbexp .sol,.mbexp .cdim');return s?s.textContent:null}", zk)
        T(G, '%s 7판 짝 없는 새 선지 %s %s — 「해설 없음」 그대로' % (eng, q0['id'], z0['n']), (e0 or '').strip() == '해설 없음', e0)
    if QJ.GATE:
        B8.home(b)
        vb = b.ev("()=>((VJ&&VJ.qs)||[]).reduce((n,q)=>n+(q.지문||[]).filter(z=>z.sol7&&(z.sol||'').trim()).length,0)")
        T(G + '-헛', '%s 헛잣대 바탕 — 이은 해설 0' % eng, vb == 0, vb)


def g7(p, b, eng):
    """A-7 채점 분모 — 2009 16 · 2013·2018·2020 20"""
    G = 'g7'
    r = {}
    for tag, q in (('NEW', p), ('BASE', b)):
        if tag == 'BASE' and QJ.REGRESS:   # regress: 바탕 판을 안 띄운다
            continue
        B8.home(q)
        r[tag] = {y: q.ev("y=>__U3.gradable(y)", y) for y in (2009, 2013, 2018, 2020)}
    T(G, '%s 채점 분모(정답 있는 문항) — 2009 16 · 2013 20(12·6번 = revfix0929 A-3 큐넷 정답) · 2018 20 · 2020 20 · 정답 값 = 큐넷(d1 표)' % eng, r['NEW'] == {2009: 16, 2013: 20, 2018: 20, 2020: 20}, r)   # A-6(a) 9/30 — _task_jo_revfix0929.md A-3 · 결정로그 9/29 13:13 「2013 12번 ④ 6번 ② 분모 20」
    if QJ.GATE:
        T(G + '-헛', '%s 헛잣대 바탕 — 2009 15 · 2013 17 · 2018·2020 19' % eng, r['BASE'] == {2009: 15, 2013: 17, 2018: 19, 2020: 19}, r['BASE'])


def g8(p, b, eng):
    """A-8 — 2008~2026 특허 해마다 「총 20문제」 · 첫 화면 해 줄 20 · 2010·2020 「시험지에 없음」 칸 2·1 · 그 칸 카드 기록 열쇠 무변(심은 기록이 보임) · 상표·디보 수"""
    G = 'g8'
    heads, rows = {}, {}
    B8.home(p)
    for y in range(2008, 2027):
        rows[y] = p.ev("y=>{const r=document.querySelector('#slot .mbur[data-giy=\"'+y+'\"] .tot');return r?r.textContent:null}", str(y))
    for y in range(2008, 2027):
        open_year(p, y)
        heads[y] = p.ev("()=>{const h=document.querySelector('#slot .mbsbar');return h?h.textContent.replace(/\\s+/g,' '):null}")
    bad = {y: h for y, h in heads.items() if not h or '총 20문제' not in h}
    badr = {y: t for y, t in rows.items() if not t or not t.startswith('20문항')}
    T(G, '%s 2008~2026 기출뷰 머리 「총 20문제」 · 첫 화면 해 줄 「20문항」' % eng, not bad and not badr, {'머리 어긋남': bad, '해 줄 어긋남': badr, '표본': [heads.get(2010), rows.get(2010)]})
    off = {}
    for y, n_ in ((2010, 2), (2020, 1)):
        k_off = p.ev("y=>{const q=((VJ&&VJ.qs)||[]).find(q=>String(q.연도)===String(y)&&!q.시험문번);return q?giKey(q):null}", y)
        p.ev("k=>{const G=giAll();G[k]={p:'3',ts:new Date().toISOString()};GIREC=G;lsWrite(GI_KEY,G,'하네스');}", k_off)
        open_year(p, y)
        for _ in range(5):
            if p.ev("()=>!!document.querySelector('#slot .exv-off')"):
                break
            if QJ.REGRESS and _A2['g8_next']:
                _sg = p.ev(_PGSIG)
            if not p.press(p.ev("()=>__U3.next()"), 'mouse', 1200 if QJ.GATE or not _A2['g8_next'] else 0):
                break
            if QJ.REGRESS and _A2['g8_next']:   # 고정 1.2초 대신 — 쪽이 갈리면 문항 열쇠 목록이 바뀐다
                QJ.until(p.pg, _SIGCHG, 8000, 'g8: ▶ 다음 → 문항 목록이 바뀜', arg=_sg)
        o = p.ev("k=>{const w=document.querySelector('#slot .exv-off');if(!w)return null;const t=e=>e?(e.textContent||'').replace(/\\s+/g,' ').trim():'';const q=w.querySelector('.exv-q[data-exq=\"'+k+'\"]');"
                 "const sel=q?[...q.querySelectorAll('.sel')].length:0;return {h:t(w.querySelector('.exv-offh')),n:w.querySelectorAll('.exv-q').length,keys:[...w.querySelectorAll('.exv-q')].map(x=>x.dataset.exq),sel};}", k_off)
        off[y] = {'칸': o, '심은 열쇠': k_off}
        p.ev("k=>{const G=giAll();delete G[k];GIREC=G;lsWrite(GI_KEY,G,'하네스');}", k_off)
    ok = all(v['칸'] and v['칸']['n'] == n_ and v['칸']['h'].startswith('시험지에 없음') and v['심은 열쇠'] in v['칸']['keys'] and re.search(r':r\d+$', v['심은 열쇠']) and v['칸']['sel'] >= 1
             for (y, n_), v in zip(((2010, 2), (2020, 1)), off.values()))
    T(G, '%s 2010·2020 그 해 맨 끝 「시험지에 없음」 칸 — 2·1 문항 · 기록 열쇠 r<문번> 그대로 · 심은 기록(고른 답)이 그 칸에 보임' % eng, ok, off)
    if QJ.GATE:
        B8.home(b)
        hb = {}
        for y in (2010, 2020):
            open_year(b, y)
            hb[y] = b.ev("()=>{const h=document.querySelector('#slot .mbsbar');return h?h.textContent.replace(/\\s+/g,' '):null}")
        T(G + '-헛', '%s 헛잣대 바탕 — 2010 「총 22문제」 · 2020 「총 21문제」' % eng, '총 22문제' in (hb[2010] or '') and '총 21문제' in (hb[2020] or ''), hb)
    # 상표·디보 — 섞인 해 수(뜻한 차이)
    for law in ('상표', '디보'):
        J = new('jimun_%s.json' % law)
        by = collections.defaultdict(list)
        for qq in J['문제']:
            if str(qq.get('연도', '')).isdigit():
                by[str(qq['연도'])].append(qq)
        mixed = {y: [qq['id'] for qq in L if not qq.get('시험문번')] for y, L in by.items() if any(qq.get('시험문번') for qq in L) and any(not qq.get('시험문번') for qq in L)}
        N(G, '%s %s — 시험문번 있는 해에서 시험문번 없는 문항(= 「시험지에 없음」 칸으로 가는 것 · 뜻한 차이) %d' % (eng, law, sum(len(v) for v in mixed.values())), mixed)


def g9(p, b, eng):
    """A-9 — 흡수 줄 전부 카드 머리 「리담과 흡수됨 — 기록 공유」 · 「제7판 단독」 0 · 다른 7판 줄 무변"""
    G = 'g9'
    Pn, Pb = {z['id']: z for z in new('jimun_7pan.json')['지문']}, ({z['id']: z for z in head('jimun_7pan.json')['지문']} if QJ.GATE else None)
    ids = [i for i in Pn if Pn[i].get('병합') == 'Y' and (QJ.REGRESS or Pb.get(i, {}).get('병합') != 'Y')]
    # 카드 머리 글 = 앱 함수(7판 카드가 쓰는 조건 그대로) · 표본 셋은 화면에서
    heads = p.ev("ids=>{const out={};ids.forEach(i=>{const z=VJ.P7map[i];out[i]=z?(z.병합?'리담과 흡수됨 — 기록 공유':(z.리담?'리담과 글이 다름 — 기록 따로':(p8Is(z)?'해례 8판에만 있는 지문':'제7판 단독'))):null;});return out;}", ids)
    bad = {i: h for i, h in heads.items() if h != '리담과 흡수됨 — 기록 공유'}
    T(G, '%s 흡수 7판 줄 %d 전부 — 카드 머리 갈래 「리담과 흡수됨 — 기록 공유」 · 「제7판 단독」 0' % (eng, len(ids)), (len(ids) > 0 if QJ.REGRESS else len(ids) == 67) and not bad, {'어긋남': bad, '표본': ids[:4]})
    if QJ.SMOKE:   # smoke 칸 = g9 첫 칸(흡수 7판 줄 전부 카드 머리) — 표본 화면 · 병합 무변은 건넘
        return
    sh = {}
    for i in ['P7-0630'] + [x for x in ids if x != 'P7-0630'][:2]:
        k = p.ev("i=>oxKeyP7(VJ.P7map[i])", i)
        B8.go_key(p, k)
        sh[i] = p.ev("k=>{const c=document.getElementById('qb-'+k);return c?(c.textContent||'').replace(/\\s+/g,' ').match(/리담과 흡수됨 — 기록 공유|제7판 단독|리담과 글이 다름 — 기록 따로/g):'카드 없음(같은 마디 리담 문항 쪽에서 선다)'}", k)
    T(G, '%s 표본 화면(P7-0630 등 셋) — 카드에 「제7판 단독」 없음' % eng, all(not (isinstance(v, list) and '제7판 단독' in v) for v in sh.values()), sh)
    if QJ.GATE:
        other = sum(1 for i in Pn if i not in ids and Pn[i].get('병합') != Pb.get(i, {}).get('병합'))
        T(G, '다른 7판 줄 병합 무변', other == 0, other)
    else:
        # 기준 칸 — 병합(흡수) 줄 목록 = 바탕(이 판 앞 인도판) 스냅샷 · 바탕 jimun_7pan(6073142)을 안 푼다
        _by9 = QJ.base('g9@병합Y', sorted(ids))
        other = len(set(ids) ^ set(_by9))
        T(G, '다른 7판 줄 병합 무변', other == 0, other)
    if QJ.GATE:
        B8.home(b)
        hb = b.ev("i=>{const z=VJ.P7map[i];return z?(z.병합?'흡수':'단독'):null}", 'P7-0630')
        T(G + '-헛', '%s 헛잣대 바탕 — P7-0630 「제7판 단독」' % eng, hb == '단독', hb)


BR = {}
PARTS = [('b1', b1), ('b1nc', b1nc), ('b23', b23), ('b4', b4), ('g5', g5), ('g6', g6), ('g7', g7), ('g8', g8), ('g9', g9)]
DPARTS = [('d1', d1)]
WITH_BR = ('b1', 'b4')


def run_engine(pw, eng):
    br = getattr(pw, eng).launch()
    BR[eng] = br
    ns, nd, ne = M.new_env()
    if QJ.GATE:
        QJ.sub('git:show-app'); QJ.sub('git:archive', 2)
        bs, bd, be = M.base_env()
    try:
        p = B8.Pg(br, eng, 'rnN', ns, nd, ne)
        QJ.launch('new')
        b = B8.Pg(br, eng, 'rnB', bs, bd, be) if QJ.GATE else None
        if QJ.GATE:
            QJ.launch('base')
        try:
            for k, fn in PARTS:
                if ONLY and k not in ONLY:
                    continue
                if QJ.SMOKE and k not in ('g7', 'g9'):   # smoke 칸 = g7(채점 분모) · g9(흡수 줄 카드 머리)
                    continue
                print('── %s · %s' % (eng, k), flush=True)
                try:
                    with QJ.stage('%s:%s' % (eng, k)):
                        fn(p, b, eng, br) if k in WITH_BR else fn(p, b, eng)
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
        if QJ.SMOKE:   # smoke 는 데이터 칸(d1)을 건넘
            continue
        if not ONLY or k in ONLY:
            try:
                with QJ.stage('data:' + k):
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
        f.write('\n==== %s · %s · NEW %s · 데이터 %s · 바탕 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), 'revfix0928night', os.path.basename(_NEW), _DATA,
                M.git('rev-parse', '--short', M.BASE_REV).decode().strip(), ','.join(ENGS)))   # A-6(d) 적히는 바탕 = 실제 바탕
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[ok], g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:900]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
