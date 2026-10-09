# _harness_jagwa_phys_win.py — 관문(시안 v50 시험 90 + 지학·생물 E1~E9) · 틀 = 같은 폴더 _harness_jagwa_physphone.py(serve · route · INIT · --vendor · --spd)
# 쓰는 법: python _harness_jagwa_phys_win.py <앱 html> <태그(new/base)> <결과 json> [--spd <studyplandata>] [--vendor <폴더>] [--only phys|e]
# 시험 = 이 파일 옆 _harness_jagwa_phys_win.rows.json · _harness_jagwa_phys_win.tests.json(지시서 §B 의 두 JSON 그대로)
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기 헬퍼(_task_qa_slim2 A-1-2 · 옛 남 하네스 import 를 갈음)
import sys, os, json, time, importlib.util
H = os.path.dirname(os.path.abspath(__file__))
GENIE = os.environ.get('GENIE_ROOT') or os.path.abspath(os.path.join(H, '..', '..', '..'))   # ★ Code 10/7 로컬 — N: 정본 자리(jagwa\moolri)에선 세 칸 위가 genie 가 아님 · 사슬 실행기가 GENIE_ROOT 를 넣어 줌
A = sys.argv[1:]
app_path, tag, outf = A[0], A[1], A[2]
def opt(k, d=None):
    return A[A.index(k)+1] if k in A else d
def _jp(nm):   # ★ 2026-10-08 — 시험 JSON 은 N: 에만(_qa_sync 는 .py·.js 만 옮김): 옆에 없으면 N: 정본 자리(_roots.n_root) · 그것도 없으면 「N: 필요」(종료 코드 3 · 클라우드)
    p = os.path.join(H, nm)
    if os.path.exists(p):
        return p
    d, nr = H, None
    for _ in range(6):
        if os.path.exists(os.path.join(d, '_roots.py')):
            sys.path.insert(0, d)
            import _roots
            nr = _roots.n_root()
            break
        d = os.path.dirname(d)
    q = os.path.join(nr, 'jagwa', 'moolri', nm) if nr else ''
    if q and os.path.exists(q):
        return q
    print('N: 필요 — 클라우드 불가(%s)' % nm, flush=True)
    sys.exit(3)
SPD = opt('--spd', os.environ.get('SPD_ROOT', os.path.join(GENIE, '..', 'studyplandata')))
VENDOR = opt('--vendor', os.path.join(H, 'vendor'))
ONLY = opt('--only', '')
os.environ['GENIE_ROOT'] = GENIE; os.environ['SPD_ROOT'] = SPD
JG.conf(VENDOR_PP=VENDOR, SPD_PP=SPD, NOTES=os.path.join(os.path.dirname(SPD), 'notes'))   # 옛 hp import 때 argv(--vendor · --spd)와 env SPD_ROOT=SPD 로 정해지던 값을 JG 에 넘김
from playwright.sync_api import sync_playwright
_RG_SYNCED = "()=>typeof recBusy!=='undefined'&&!recBusy&&(((lsObj(SMETA_KEY).lastSync||0)>=performance.timeOrigin)||!!recErr)"   # qa_slim2 regress 표지 = 앱 recBoot() 첫 syncRecords 끝(recBusy 거짓 · 이 쪽 열린 뒤 맞춘 시각 또는 recErr) · INIT_PP 가 토큰을 넣어 쪽마다 맞춤
_RG_SMOKE = (24, 32, 34, 52, 68)   # qa_slim2 smoke 칸(A-0 · 모두 PC 화면 p1)
src = open(app_path, encoding='utf-8').read()
port = JG.serve_PP(tag, src)
_G3 = 'window.G3=' in src   # ★ 2026-10-09 _task_jagwa_gg3 — 새 판 표지(g3.js · 패치 #35)
_G3_SUP = {24: '§A-4 서랍 · 🔍 오른쪽 깔때기 상/중/하(머리 줄 꼴 바뀜)',
           58: '§A-4 비교 창 · 서랍 번호 = 비교(본창 옆 그림 창 · 시안 v18 · 멈춘 창 자리)', 59: '§A-4 비교 창 · 서랍 번호 = 비교(그림 창 쌓임 · v52)', 62: '§A-4 비교 창 · 그림 창 ✕(v18 · 옛 멈춘 창 ✕ 자리 없음)',
           76: '§A-4 서랍 · O△X 작은 창 줄 누름 = 목차 말풍선 + <>(v29 · 옛 「창 닫힘 · 이은 문항 큰 창」)',
           78: '§A-4 근거 줄 · 「근거」 누름 = 작은 창(유형 글자 넷 · 토글 셋 · v29)', 79: '§A-4 근거 줄 · 작은 창 유형 글자 누름 = 켜고 끔(v29)', 80: '§A-4 근거 줄 · 작은 창 닫힘 = 바깥 누름(✕ 없음 · v29)'}
OUT = {'tag': tag, 'phys': [], 'e': [], 'errs': {}}
t0 = time.time()
if ONLY in ('', 'phys'):
    rows = json.load(open(_jp('_harness_jagwa_phys_win.rows.json'), encoding='utf-8'))
    tests = json.load(open(_jp('_harness_jagwa_phys_win.tests.json'), encoding='utf-8'))
    VIEWS = {'pc': (1100, 800), 'ph': (390, 780)}
    READY = "typeof DATA!=='undefined'&&DATA.length>0&&typeof HAVE!=='undefined'&&!!HAVE['111']"
    res = []
    with sync_playwright() as p:
        br = p.chromium.launch(args=['--no-sandbox'])
        ctx = br.new_context(viewport={'width': 1100, 'height': 800})
        ctx.route('**/*', JG.route_handler(JG.REMOTE))
        ctx.add_init_script(JG.INIT_PP.replace('__SUBJ__', 'phys').replace('__WHO__', '하네스'))
        P = {}
        for row in rows:
            for s in row['screens']:
                QC.launch('new')   # 셈(§B-4) — 이 하네스는 바탕 판을 안 띄운다(사슬 tag new)
                pg = ctx.new_page(); pg.set_default_timeout(90000)
                W, H = VIEWS[s['view']]; pg.set_viewport_size({'width': W, 'height': H})
                errs = []; pg.on('pageerror', lambda e, errs=errs: errs.append(str(e)[:200]))
                pg.goto('http://127.0.0.1:%d/app.html' % port, wait_until='load')
                pg.wait_for_function(READY, timeout=240000)
                if QC.GATE:
                    pg.wait_for_timeout(2500)
                else:   # regress — 고정 2.5 초 대신 표지(첫 기록 맞춤 끝 · 상한 = 같은 2.5 초)
                    QC.until(pg, _RG_SYNCED, 2500, 'phys_win 화면 %s 부팅 뒤 첫 syncRecords 끝' % s['id'])
                try: pg.evaluate(s['setup'])
                except Exception as e: print('SETUP ERR', s['id'], str(e)[:200])
                P[s['id']] = (pg, errs)
        print('setup', round(time.time() - t0), 's', flush=True)
        for i, t in enumerate(tests, 1):
            pg, errs = P[t['screen']]
            note = ''
            sel = t.get('click') or t.get('type')
            try:
                loc = pg.locator(sel).nth(t.get('nth', 0))
                try: loc.scroll_into_view_if_needed(timeout=3000)
                except Exception: pass
                loc.click(timeout=1500 if tag=='base' else 5000)
                if t.get('type'): pg.keyboard.type(t['text'], delay=30)
            except Exception as e:
                note = 'CLICKFAIL ' + str(e).split('\n')[0][:120]
            pg.wait_for_timeout(t.get('wait', 1000))
            try:
                v = pg.evaluate(t['expect'])
                ok = v is True or (v not in (False, None, 0, '') and not isinstance(v, dict))
                raw = repr(v)[:40]
            except Exception as e:
                ok = False; raw = 'ERR ' + str(e).split('\n')[0][:120]
            same = None
            if t.get('same'):
                try: same = pg.evaluate('s=>document.querySelectorAll(s).length', t['same'])
                except Exception: pass
            # ★ 2026-10-09 _task_jagwa_gg3 §A-4 — 시안 v57(gg3)이 갈음한 칸은 g3 판에서 INFO(시험은 그대로 돌려 뒤 칸 상태 지킴 · 새 잣대 = jagwa_gg3 관문 G1 시안 시험 109)
            if _G3 and i in _G3_SUP:
                res.append([i, t['name'], None, raw, note, same])
                if QC.want(str(i), smoke=i in _RG_SMOKE):
                    print('INFO | %d %s | gg3 갈음 — %s · 값 %s %s' % (i, t['name'][:60], _G3_SUP[i], raw, note), flush=True)
                continue
            res.append([i, t['name'], ok, raw, note, same])
            if QC.want(str(i), smoke=i in _RG_SMOKE):   # smoke — 시험은 차례 그대로 다 돌고(앞 상태 지킴) smoke 칸 줄만 찍음
                print(i, 'PASS' if ok else 'FAIL', t['name'][:60], raw if not ok else '', note, flush=True)
        OUT['errs'] = {k: v[1] for k, v in P.items()}
        br.close()
    OUT['phys'] = res

def ev(pg, js, a=None):
    try: return pg.evaluate(js, a) if a is not None else pg.evaluate(js)
    except Exception as e: return 'ERR ' + str(e).split('\n')[0][:150]

def clk(pg, sel, nth=0):
    try:
        pg.locator(sel).nth(nth).click(timeout=5000); return ''
    except Exception as e: return 'CLICKFAIL(' + sel + ')'

if ONLY in ('', 'e') and not QC.SMOKE:   # smoke — E1~E9(지학 · 생물)는 smoke 칸이 아님
    with sync_playwright() as p:
        br = p.chromium.launch(args=['--no-sandbox'])
        for subj in ('earth', 'bio'):
            ctx = br.new_context(viewport={'width': 1100, 'height': 800})
            ctx.route('**/*', JG.route_handler(JG.REMOTE))
            ctx.add_init_script(JG.INIT_PP.replace('__SUBJ__', subj).replace('__WHO__', '하네스'))
            QC.launch('new')   # 셈(§B-4)
            pg = ctx.new_page(); pg.set_default_timeout(90000)
            pg.goto('http://127.0.0.1:%d/app.html?subj=%s' % (port, subj), wait_until='load')
            pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0&&typeof draw==="function"', timeout=120000)
            if QC.GATE:
                pg.wait_for_timeout(2500)
            else:   # regress — 고정 2.5 초 대신 표지(첫 기록 맞춤 끝 · 상한 = 같은 2.5 초)
                QC.until(pg, _RG_SYNCED, 2500, 'phys_win %s 부팅 뒤 첫 syncRecords 끝' % subj)
            out = []
            # E1
            ev(pg, 'ndResFold(false);openView(DATA[0][F.NO],navList())'); pg.wait_for_timeout(2500)
            v0 = ev(pg, 'VNO')
            n2 = ev(pg, "(()=>{const r=[...document.querySelectorAll('#ndList .ndrow')].filter(x=>+x.dataset.no!==VNO);return +r[0].dataset.no})()")
            n = clk(pg, '#ndList .ndrow[data-no="%s"] .ndno' % n2); pg.wait_for_timeout(2500)
            out.append(('E1', ev(pg, "a=>VNO===a[1]&&document.querySelectorAll('.vpin').length===1&&!!document.querySelector('.vpin[data-no=\"'+a[0]+'\"]')", [v0, n2]), n, 'v0=%s n2=%s' % (v0, n2)))
            # E2
            n3 = ev(pg, "(()=>{const pins=[...document.querySelectorAll('.vpin')].map(x=>+x.dataset.no);const r=[...document.querySelectorAll('#ndList .ndrow')].filter(x=>+x.dataset.no!==VNO&&!pins.includes(+x.dataset.no));return +r[0].dataset.no})()")
            n = clk(pg, '#ndList .ndrow[data-no="%s"] .ndt' % n3); pg.wait_for_timeout(2500)
            out.append(('E2', ev(pg, "a=>VNO===a&&document.querySelectorAll('.vpin').length===1", n3), n, 'n3=%s' % n3))
            for _ in range(6):
                if not ev(pg, "document.querySelectorAll('.vpin .shx').length"): break
                clk(pg, '.vpin .shx'); pg.wait_for_timeout(400)
            # E3
            ev(pg, "QINK.s=[{c:'#000',w:2,p:[0.1,0.1,0.2,0.2],r:QR},{c:'#000',w:2,p:[0.3,0.3,0.4,0.4],r:QR},{c:'#000',w:2,p:[0.5,0.5,0.6,0.6],r:QR+1}];qPaint()")
            n = clk(pg, '#tErase'); pg.wait_for_timeout(500); n += clk(pg, '#tErase'); pg.wait_for_timeout(500)
            a1 = ev(pg, "!!document.getElementById('erPop')")
            n += clk(pg, '#erPop #eL'); pg.wait_for_timeout(600)
            a2 = ev(pg, "QINK.s.length===1&&qRoundOf(QINK.s[0])!==QR")
            n += clk(pg, '#tErase'); pg.wait_for_timeout(500)
            if not ev(pg, "!!document.getElementById('erPop')"): n += clk(pg, '#tErase'); pg.wait_for_timeout(500)
            n += clk(pg, '#erPop #eA'); pg.wait_for_timeout(500); n += clk(pg, '#erPop #eA'); pg.wait_for_timeout(800)
            a3 = ev(pg, "QINK.s.length===0&&QR===1")
            out.append(('E3', a1 is True and a2 is True and a3 is True, n, 'a=%s,%s,%s' % (a1, a2, a3)))
            # E4
            n = clk(pg, '#tHist'); pg.wait_for_timeout(800)
            out.append(('E4', ev(pg, "!!document.getElementById('hsPop')"), n, ''))
            # E5
            n = clk(pg, '#vWinTg'); pg.wait_for_timeout(600); n += clk(pg, '#ndGrip'); pg.wait_for_timeout(400); n += clk(pg, '#vBack'); pg.wait_for_timeout(600)
            ev(pg, 'ndResFold(false);openView(DATA[1][F.NO],navList())'); pg.wait_for_timeout(1500)
            out.append(('E5', ev(pg, "document.getElementById('view').classList.contains('win')&&VWFULL===false"), n, ''))
            # E6
            ev(pg, "(()=>{const el=document.getElementById('ndHead'),r=el.getBoundingClientRect();el.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,clientX:r.left+3,clientY:r.top+3}))})()")
            pg.wait_for_timeout(300)
            out.append(('E6', ev(pg, "+getComputedStyle(document.getElementById('navdr')).zIndex>+getComputedStyle(document.getElementById('view')).zIndex"), '', ev(pg, "[getComputedStyle(document.getElementById('navdr')).zIndex,getComputedStyle(document.getElementById('view')).zIndex]")))
            # E7
            d6 = ev(pg, 'DATA[6][F.NO]')
            ev(pg, 'linkSet(VNO,DATA[6][F.NO],true);showProblem()'); pg.wait_for_timeout(1500)
            v7 = ev(pg, 'VNO')
            n = clk(pg, '.lkchip [data-go="%s"], .lkchip[data-go="%s"]' % (d6, d6)); pg.wait_for_timeout(2500)
            out.append(('E7', ev(pg, "a=>VNO===a[0]&&!!document.querySelector('.vpin[data-no=\"'+a[1]+'\"]')", [d6, v7]), n, 'd6=%s v7=%s' % (d6, v7)))
            # E8
            out.append(('E8', ev(pg, "['tLayer','tLayerEye','tLayerAdd'].every(i=>{const x=document.getElementById(i);return !x||x.offsetParent===null})&&document.getElementById('tCard').textContent.trim()==='🃏'&&getComputedStyle(document.getElementById('stage')||document.body).scrollbarWidth==='none'"), '', ''))
            # E9
            pass  # print('E9 pre', ev(pg, "(()=>{const b=document.getElementById('vBack'),r=b.getBoundingClientRect();const e=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return [document.getElementById('view').className,e&&(e.id||e.className),JSON.stringify(r)]})()"))
            n = clk(pg, '#vBack'); pg.wait_for_timeout(800)
            out.append(('E9', ev(pg, "document.querySelectorAll('#ndList .ndv').length===0&&document.querySelectorAll('#ndList .ndno.ph').length===0&&document.querySelectorAll('#list .item .tag.tg').length===document.querySelectorAll('#list .item').length&&!document.querySelector('#navdr .ndhead .pwchip')"), n, ev(pg, "[document.querySelectorAll('#list .item .tag.tg').length,document.querySelectorAll('#list .item').length]")))
            for o in out:
                print(tag, subj, *o, flush=True)
                print('%s | %s · %s · %s' % ('PASS' if o[1] is True else 'FAIL', o[0], subj, ' '.join(str(x) for x in o[2:])[:300]), flush=True)   # ★ 10/8 — 사슬 받개(RX_PIPE)가 E 칸을 읽게(옛 줄은 위에 그대로)
            OUT['e'] += [[subj] + [x if isinstance(x,(bool,str,int,float)) or x is None else repr(x) for x in o] for o in out]
            ctx.close()
        br.close()

OUT['sec'] = round(time.time() - t0)
json.dump(OUT, open(outf, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# 옛 줄: print('phys PASS', sum(1 for r in OUT['phys'] if r[2]), '/', len(OUT['phys']), '· E', sum(1 for r in OUT['e'] if r[2] is True), '/', len(OUT['e']), '· sec', OUT['sec'])
print('INFO | phys %d / %d · E %d / %d · sec %s' % (sum(1 for r in OUT['phys'] if r[2]), len(OUT['phys']), sum(1 for r in OUT['e'] if r[2] is True), len(OUT['e']), OUT['sec']))   # ★ 10/8 — 합계는 INFO(받개가 「phys PASS」 를 늘 PASS 한 칸으로 셈하던 것 · 칸 판정은 위 줄마다)
