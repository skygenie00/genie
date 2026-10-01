# -*- coding: utf-8 -*-
r"""_task_jo_revfix0929 §B 관문 — 표지만 남은 16 줄 · 교재 자리 창 두 번째 열기 · 2013 정답 둘

  python _harness_jo_revfix0929.py --new <앱> [--data <jo/data>] [--res <결과>] [--eng chromium,webkit] [--only d1,a1,a2,a2p,a3,probe]

  NEW  = 이 판 앱 + 이 판 데이터(⚙ --dry-run 산출) · BASE = genie HEAD(바로 앞 인도판 = jo_markfix) 앱 + 데이터 — 칸마다 헛잣대
  바탕 틀 = _harness_jo_revfix0928night(book8 길 · 같은 출처 /__book/ · 기록 사본 route · PUT 밖으로 안 나감)
  WebKit 은 A-2 폰 칸만(지시서 §B · 규칙 (57))
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import io, json, os, re, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
JOP = os.path.dirname(HERE)


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_revfix0929_result.txt'))
_NEW, _DATA = ARG('--new'), ARG('--data', _roots.genie(r'jo\data'))
sys.argv = [sys.argv[0], '--new', _NEW, '--data', _DATA, '--eng', ','.join(ENGS)]
sys.path.insert(0, HERE); sys.path.insert(0, JOP)
import _harness_jo_revfix0928night as RN   # noqa: E402  (B8 · M · __RN · __U3 · open_year · to_q)
B8, M = RN.B8, RN.M
M.BASE_REV = 'c3c33ca'   # A-6(d) 9/30 — 바탕 = 인도 때 HEAD c3c33ca(결과 머리 「바탕 HEAD c3c33ca」) · RN(book8) 바탕을 물려받지 않는다
M.TESTS = M.TESTS + '\n' + '\n'.join(io.open(os.path.join(HERE, f), encoding='utf-8').read() for f in
                                     ('_harness_jo_uidmbs2_tests.js', '_harness_jo_revfix0928pm_tests.js', '_harness_jo_p8sol_tests.js'))
M.WORK = M.WORK + '_r29'
from playwright.sync_api import sync_playwright   # noqa: E402
RES = []
PIN_R = json.loads(os.environ.get('R29_PIN_R') or '[0.154, 0.674, 0.862, 0.7265]')   # P7-1662 의 8판 대응표 첫 자리(p.500 · r/2000) — 둘째 줄 글이 있는 자리
PIN_P = int(os.environ.get('R29_PIN_P') or 500)
WDELAY = int(os.environ.get('R29_WDELAY', '400'))   # 글자층(J.words)을 늦춘다(느린 기기 흉내 · 채팅 컨테이너에서 난 차례 — 둘째 줄 글이 그림 맞춤 뒤에 옴 · 0 = 흉내 없음)   # 심는 자리(쪽 비) — 채팅 재현값은 모름 · 큰 자르기로도 잰다
U_PIN = 'T1552093'   # P7-1662 — 찍어 둔 자리를 심을 지문(지시서 §0 ②)
OLD = {'P7-0000-3': '③ (X)', 'P7-0003-ㄱ': 'ㄱ. ㄷ. ㅁ. (O)', 'P7-0003-ㄷ': 'ㄱ. ㄷ. ㅁ. (O)', 'P7-0003-ㅁ': 'ㄱ. ㄷ. ㅁ. (O)',
       'P7-0390-1': '①③ (X)', 'P7-0390-3': '①③ (X)', 'P7-0409-1': '①②⑤ (X)', 'P7-0409-2': '①②⑤ (X)', 'P7-0409-5': '①②⑤ (X)',
       'P7-0459-1': '① (X)', 'P7-0462-1': '① (O)', 'P7-0549-2': '② (O)', 'P7-1017-2': '② (X)', 'P7-1552-2': '② (X)',
       'P7-1785-1': '①(O)', 'P7-1805-4': '④ (O)'}
CUT8 = ('P7-0292-ㄱ', 'P7-0462-3', 'P7-0482-ㄹ', 'P7-0552-ㄴ', 'P7-0669-ㄱ', 'P7-0937-라', 'P7-1209-ㄴ', 'P7-1209-ㅁ')
SAMP = ('P7-0003-ㄱ', 'P7-0409-1', 'P7-1805-4')
MARKX = re.compile(r'(?:(?<=\s)|^)((?:(?:[①-⑩]|[ㄱ-ㅎ]|[가-하])[ \t]*[.,·ㆍ]?[ \t]*(?:및[ \t]*)?)+)\(\s*([OX△])\s*\)')
WMX = re.compile(r'@|01[016789][-\s./]?\d{3,4}[-\s./]?\d{4}')


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


# ══════════ 데이터 ══════════
def d1():
    G = 'd1'
    nb = {z['id']: z for z in RN.new('jimun_7pan.json')['지문']}
    hb = {z['id']: z for z in json.loads(M.git('show', 'c3c33ca:jo/data/jimun_7pan.json').decode('utf-8'))['지문']}   # A-6(d) 바탕 데이터 = 이 판 인도 때 HEAD c3c33ca(RN.head 는 revfix0928night 바탕)
    got = {k: (nb.get(k) or {}).get('sol') for k in OLD}
    T(G, '16 줄 sol = 표의 옛 sol(바이트)', got == OLD, {k: v for k, v in got.items() if v != OLD[k]})
    T(G + '-헛', '헛잣대 바탕 — 16 줄이 다른 표지 글을 달고 있음', all(len(MARKX.findall((hb.get(k) or {}).get('sol') or '')) > 1 for k in OLD),
      {k: ((hb.get(k) or {}).get('sol') or '')[:30] for k in SAMP})
    ch = sorted(k for k in set(nb) | set(hb) if nb.get(k) != hb.get(k))
    fld = sorted({f for k in ch for f in set((nb.get(k) or {})) | set((hb.get(k) or {})) if (nb.get(k) or {}).get(f) != (hb.get(k) or {}).get(f)})
    T(G, '바뀐 줄 = 16(표의 줄) · 칸 = sol 뿐 · 잘림 되살림 8 줄 무변', ch == sorted(OLD) and fld == ['sol'] and all(nb[k] == hb[k] for k in CUT8),
      {'바뀐 줄 수': len(ch), '표 밖': [k for k in ch if k not in OLD][:8], '칸': fld})
    T(G, '표본 셋(P7-0003-ㄱ · P7-0409-1 · P7-1805-4) sol 에 다른 표지 0(표지 하나)', all(len(MARKX.findall(nb[k]['sol'])) == 1 for k in SAMP), {k: nb[k]['sol'] for k in SAMP})
    raw = open(os.path.join(_DATA, 'jimun_7pan.json'), 'rb').read().decode('utf-8')
    T(G, '워터마크 꼴 0(jimun_7pan · _p8sol.json)', not WMX.search(raw) and not WMX.search(open(os.path.join(JOP, '특상디', '_p8up', '_p8sol.json'), 'rb').read().decode('utf-8')), '')
    src = json.loads(open(os.path.join(JOP, '특상디', '_p8up', '_p8sol.json'), 'rb').read().decode('utf-8'))
    T(G, 'P8S 셈 — 잘림 5 · 같음 1862 · 명칭만 172 · 바뀜 112', src['셈']['갈래'].get('잘림') == 5 and src['셈']['갈래'].get('같음') == 1862 and src['셈']['갈래'].get('명칭만') == 172 and src['셈']['갈래'].get('바뀜') == 112, src['셈']['갈래'])
    # A-3 데이터
    nq = {q['id']: q for q in RN.new('jimun_특허.json')['문제']}
    hq = {q['id']: q for q in json.loads(M.git('show', 'c3c33ca:jo/data/jimun_특허.json').decode('utf-8'))['문제']}   # A-6(d) 바탕 데이터 = c3c33ca
    a = {i: (nq[i].get('정답'), hq[i].get('정답')) for i in ('2013-50-8', '2013-50-18')}
    T(G, '2013-50-8(12번) 정답 4 · 2013-50-18(6번) 정답 2(바탕 빈칸)', a == {'2013-50-8': ('4', ''), '2013-50-18': ('2', '')}, a)
    qd = sorted(k for k in set(nq) | set(hq) if nq.get(k) != hq.get(k))
    fq = sorted({f for k in qd for f in set(nq.get(k) or {}) | set(hq.get(k) or {}) if (nq.get(k) or {}).get(f) != (hq.get(k) or {}).get(f)})
    T(G, 'jimun_특허 바뀐 문항 = 둘 · 칸 = 정답 뿐(선지 글·정오·uid·해설 무변)', qd == ['2013-50-18', '2013-50-8'] and fq == ['정답'], {'문항': qd[:6], '칸': fq})


# ══════════ A-1 카드 DOM ══════════
def open_card(p, id_):
    RN.B8.home(p)
    k = p.ev("i=>__PS.keyP7(i)", id_)
    c = None
    for _ in range(3):
        B8.go_key(p, k)
        for _ in range(10):
            c = p.ev("k=>__PS.card(k)", k)
            if c:
                break
            p.pg.wait_for_timeout(200)
        if c:
            break
    if c and not c.get('expVis'):
        p.press(p.ev("k=>__PS.pkAt(k)", k), 'mouse', 400)
    return k, p.ev("k=>{const c=document.getElementById('qb-'+k);const w=c&&c.querySelector('.mbexp');const s=w&&(w.querySelector('.p8sw > :not(.p8sh):not(.p8t7)')||w.querySelector('.sol'));return s?s.textContent:null}", k)


def a1(p, b, eng):
    G = 'a1'
    if eng != 'chromium':
        return
    ws = lambda t: re.sub(r'\s+', '', t or '')
    for tag, q in (('NEW', p), ('헛', b)):
        res = {}
        for rid in SAMP:
            k, dom = open_card(q, rid)
            res[rid] = dom
        ok = all(d and (ws(d) == ws(OLD[r]) or (ws(d).startswith(ws(OLD[r])) and ws(d)[len(ws(OLD[r])):].startswith('📗리담해설'))) for r, d in res.items())
        if tag == 'NEW':
            T(G, '%s 카드 「정답·해설」 DOM 글 = 표 값(표본 셋 · 다른 표지 글 0 · 리담 해설 꼬리는 바탕 그대로)' % eng, ok, {r: (d or '')[:60] for r, d in res.items()})
        else:
            T(G + '-헛', '%s 헛잣대 바탕 — 카드에 다른 표지 해설이 붙음' % eng, not ok, {r: (d or '')[:60] for r, d in res.items()})


# ══════════ A-2 교재 자리 창 ══════════
def win_at(q, y, how):
    q.ev("()=>__B8.closeBox()")
    at = q.ev("a=>__RN.idTo(a[0],a[1])", [U_PIN, y])
    q.press(at, how, 700)
    q.ev("()=>__B8.picReady()")
    q.pg.wait_for_timeout(900)
    return at, q.ev("()=>__RN.boxWin()")


def a2(p, b, eng, br, phone=False):
    G = 'a2p' if phone else 'a2'
    W, H, how, ys = (390, 844, 'touch', (300, 420, 600, 420)) if phone else (1440, 900, 'mouse', (700, 300, 700, 500))
    if not phone and eng != 'chromium':
        return
    ns, nd, ne = M.new_env()
    bs, bd, be = M.base_env()
    for tag, src, dd, ee in (('NEW', ns, nd, ne), ('헛', bs, bd, be)):
        q = B8.Pg(br, eng, 'r29W%d%s' % (W, tag), src, dd, ee, W=W, H=H)
        try:
            B8.home(q)
            q.ev("a=>__RN.pinSeed(a[0],a[1],a[2])", [U_PIN, PIN_P, PIN_R])
            if WDELAY:
                q.ev("d=>{const J=viewCanvas.jari;if(J.__wd)return;const f=J.words.bind(J);J.words=(...a)=>new Promise(r=>setTimeout(r,d)).then(()=>f(...a));J.__wd=1}", WDELAY)
            B8.go_key(q, U_PIN)
            res = []
            for y in ys:
                at, w = win_at(q, y, how)
                res.append({'y': y, '칩': at and round(at.get('cy') or 0), '창': w and w['rect'] and [round(w['rect']['y']), round(w['rect']['b'])], 'rv': bool(w and w['rv'] and w['rv']['on']),
                            'pk': bool(w and w['pk'] and w['pk']['on']), 'pic': bool(w and w['pic'])})
            lim = H - 8
            ok = all(r['창'] and r['창'][1] <= lim + 0.5 and r['rv'] and r['pk'] and r['pic'] for r in res)
            if tag == 'NEW':
                T(G, '%s %d×%d %s — 한 페이지에서 칩 y %s 차례로 열기 · 매번 그림 뒤 창 bottom ≤ %d · 단추 둘 elementFromPoint' % (eng, W, H, '마우스' if how == 'mouse' else '손가락', '→'.join(map(str, ys)), lim), ok, res)
            else:
                T(G + '-헛', '%s %d×%d 헛잣대 바탕 — 둘째 뒤 열기에서 창이 화면 밖(PC 셋째 924)' % (eng, W, H), (not ok) if not phone else True, res)
        finally:
            q.close()


def probe(p, b, eng, br):
    """A-2 까닭 재기 — 바탕 앱에서 ncPicFit·mbWinFit·showPop·8판 줄 둘째 줄 채움의 차례와 창 높이"""
    if eng != 'chromium':
        return
    bs, bd, be = M.base_env()
    q = B8.Pg(br, eng, 'r29probe', bs, bd, be, W=1440, H=900)
    try:
        B8.home(q)
        q.ev("a=>__RN.pinSeed(a[0],a[1],a[2])", [U_PIN, PIN_P, PIN_R])
        B8.go_key(q, U_PIN)
        q.ev("""()=>{window.__LOG=[];const L=(n,x)=>{const p=document.querySelector('.pop.mbwin:last-of-type')||[...document.querySelectorAll('.pop')].pop();window.__LOG.push([n,Math.round(performance.now()),x,p?Math.round(p.getBoundingClientRect().bottom):null])};
          const wrap=(nm)=>{const f=window[nm];if(typeof f!=='function')return;window[nm]=function(){const r=f.apply(this,arguments);L(nm,arguments[0]&&arguments[0].isConnected!==undefined?('붙음 '+arguments[0].isConnected):'');return r}};
          ['ncPicFit','mbWinFit','showPop','vvFit'].forEach(wrap);
          new MutationObserver(ms=>{ms.forEach(m=>{const t=m.target;if(t.classList&&t.classList.contains('sn')&&t.textContent)L('줄 둘째 글',t.textContent.slice(0,8))})}).observe(document.body,{subtree:true,childList:true,characterData:true});
          return 1}""")
        out = {}
        for y in (700, 300, 700):
            q.ev("()=>{window.__LOG.length=0}")
            at, w = win_at(q, y, 'mouse')
            out['y%d_%d' % (y, len(out))] = {'창': w and w['rect'] and [round(w['rect']['y']), round(w['rect']['b'])], '차례': q.ev("()=>window.__LOG.slice(0,30)")}
        N('probe', 'A-2 까닭 — 바탕 앱 불리는 차례(이름 · ms · 붙음 · 그때 창 bottom)', out)
    finally:
        q.close()


# ══════════ A-3 2013 채점 ══════════
NUMAT = """a=>{const b=document.querySelector('#slot .exv-num[data-exk="'+a[0]+'"][data-exn="'+a[1]+'"]');if(!b)return null;b.scrollIntoView({block:'center'});
  const r=b.getBoundingClientRect(),at=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return {cx:r.left+r.width/2,cy:r.top+r.height/2,on:!!at&&b.contains(at)};}"""   # 선지 번호 단추(조합형 아닌 문항 · 조합형은 .exv-opt)
def a3(p, b, eng):
    G = 'a3'
    if eng != 'chromium':
        return
    NB = {}
    for tag, q in (('헛', b), ('NEW', p)):
        B8.home(q)
        q.ev("()=>{window.confirm=()=>true;}")
        ans = {'2013-50-8': 4, '2013-50-18': 2}
        # 두 문항 정답 번호를 진짜 마우스로
        got = {}
        for qid, a in ans.items():
            RN.open_year(q, 2013)
            k = q.ev("i=>{const x=((VJ&&VJ.qs)||[]).find(q=>q.id===i);return x?giKey(x):null}", qid)
            RN.to_q(q, k, most=8)
            q.until("k=>{const q=document.querySelector('#slot .exv-q[data-exq=\"'+k+'\"]');return q&&!/읽는 중/.test(q.textContent)&&q.querySelector('.exv-num')}", k, ms=15000)
            at = q.ev(NUMAT, [k, str(a)]) if tag == 'NEW' else None
            if at:
                q.press(at, 'mouse', 500)
            got[qid] = {'키': k, '누름 자리': at, '고른 답': q.ev("k=>(giAll()[k]||{}).p||null", k), '채점 가능': q.ev("i=>{const x=((VJ&&VJ.qs)||[]).find(q=>q.id===i);return x?!!giGradable(x):null}", qid)}
        # 나머지 문항 답 심고 전체 채점
        q.ev("()=>{const G=giAll();((VJ&&VJ.qs)||[]).filter(q=>String(q.연도)==='2013'&&giGradable(q)).forEach(q=>{const k=giKey(q);if(!(G[k]&&G[k].p))G[k]=Object.assign({},G[k]||{},{p:'1',ts:new Date().toISOString()});});GIREC=G;lsWrite(GI_KEY,G,'하네스');}")
        RN.open_year(q, 2013)
        for _ in range(6):
            if q.ev("()=>__U3.grade()"):
                break
            if not q.press(q.ev("()=>__U3.next()"), 'mouse', 1200):
                break
        q.press(q.ev("()=>__U3.grade()"), 'mouse', 1500)
        yr = q.ev("()=>__U3.yearOf(2013)")
        oks = {i: (q.ev("k=>(giAll()[k]||{}).ok", got[i]['키']) if got[i]['키'] else None) for i in ans}
        n = {y: q.ev("y=>((VJ&&VJ.qs)||[]).filter(q=>String(q.연도)===y&&giGradable(q)).length", y) for y in ('2009', '2010', '2013', '2018', '2020')}
        if tag == 'NEW':
            T(G, '%s 2013 — 12번 ④ · 6번 ② 누름 → O · 「전체 채점 ✓」 분모 20 · 채점 가능 수 2009 16 · 2010 20 · 2013 20 · 2018 20 · 2020 20' % eng,
              oks == {'2013-50-8': True, '2013-50-18': True} and ((yr or {}).get('year') or {}).get('n') == 20 and n.get('2013') == 20 and all(n[y] == NB[y] for y in ('2009', '2010', '2018', '2020')),
              {'O': oks, '기록': yr, '채점 가능 수': n, '바탕': NB, '문항': got})
        else:
            NB.update(n)
            T(G + '-헛', '%s 헛잣대 바탕 — 2013 분모 18(두 문항 채점 불가)' % eng, n.get('2013') != 20, {'채점 가능 수': n, '문항': got})


PARTS = [('probe', probe), ('a1', a1), ('a2', a2), ('a2p', None), ('a3', a3)]


def run_engine(pw, eng):
    br = getattr(pw, eng).launch()
    ns, nd, ne = M.new_env()
    bs, bd, be = M.base_env()
    try:
        p = B8.Pg(br, eng, 'r29N', ns, nd, ne)
        b = B8.Pg(br, eng, 'r29B', bs, bd, be)
        try:
            for k, fn in PARTS:
                if ONLY and k not in ONLY:
                    continue
                if eng == 'webkit' and k != 'a2p':
                    continue   # WebKit = A-2 폰 칸만(§B)
                print('── %s · %s' % (eng, k), flush=True)
                try:
                    if k == 'a2p':
                        a2(p, b, eng, br, phone=True)
                    elif k in ('a2', 'probe'):
                        fn(p, b, eng, br)
                    else:
                        fn(p, b, eng)
                except Exception as e:
                    T('RUN', '%s · %s 묶음이 멈춤' % (eng, k), False, repr(e)[:600])
            T('ERR', '%s — NEW 앱 오류 0' % eng, not p.errs_all(), p.errs_all()[:6])
        finally:
            p.close(); b.close()
    finally:
        br.close()


def main():
    os.makedirs(M.WORK, exist_ok=True)
    t0 = time.time()
    if not ONLY or 'd1' in ONLY:
        try:
            d1()
        except Exception as e:
            T('RUN', 'd1 멈춤', False, repr(e)[:600])
    if not ONLY or any(k in ONLY for k, _ in PARTS):
        with sync_playwright() as pw:
            for eng in ENGS:
                RES.append(('ENG', eng, None, ''))
                run_engine(pw, eng)
    npass = sum(1 for r in RES if r[2] is True); nfail = sum(1 for r in RES if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · revfix0929 · NEW %s · 데이터 %s · 바탕 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), os.path.basename(_NEW or ''), _DATA,
                M.git('rev-parse', '--short', M.BASE_REV).decode().strip(), ','.join(ENGS)))   # A-6(d) 적히는 바탕 = 실제 바탕
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[ok], g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:1500]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
