# -*- coding: utf-8 -*-
r"""작은 고침 공용 관문 — 규칙 (96) ④(사용자 10/10 14:13 「작은 고침 10 분 안」) · 2026-10-13 채팅이 만듦

  판마다 관문 하네스를 새로 짜지 않는다. 지시서가 「명세 JSON」 하나를 주고 이 파일이 돈다.
  명세 = 채팅 시안(snap) 의 점검 칸을 그대로 옮긴 것 — 시안에서 진짜 마우스로 이미 잰 잣대를 클라우드가 두 엔진 · 바탕(헛잣대)으로 다시 잰다.

  python _qa/_qa_small_gate.py --spec <명세.json> [--new <앱 파일 | 판>] [--base <판>] [--eng chromium,webkit] [--only 칸이름앞머리,…]
         [--spd <studyplandata>] [--notes <notes>] [--vendor <cdnjs 사본>] [--res <결과 txt>] [--no-base] [--base-eng chromium]

  명세:
    {"app": "jagwa",                       ← 지금은 자과만(공용 _qa_jagwa_common.Pg_PP)
     "base": "d9961b8",                    ← --base 없을 때
     "settle_ms": 5000,                    ← 화면 setup 뒤 기다림
     "prelude": "화면마다 setup 앞에 돌릴 JS(문 · 도우미 함수 정의)",
     "screens": {"p1": {"subj": "earth", "dev": "pc"|"ph", "setup": "엔진에서 돌릴 JS(식 · async 가능)"}, …},
     "tests": [{"name", "screen",
                "act": "click"|"long"|"type"|"none",   ← click = PC 마우스 · 폰 손가락 톡 / long = 길게(hold ms · 기본 800) / type = 누르고 글 넣기
                "sel": CSS(엔진 기준), "nth": 0, "hold": 800, "text": "", "enter": false, "wait": 600,
                "expect": "엔진에서 참일 JS 식",
                "yard": true}]}                        ← 바탕에서 FAIL 이어야 하는 칸(헛잣대) · false = 바탕도 PASS 여야(무변 칸)
  칸은 명세 차례대로 · 같은 화면 칸은 같은 쪽에서 이어서(앞 칸이 바꾼 상태 위에서) 잰다.
  엔진: chromium = PC 마우스 · 폰 CDP 손가락 / webkit = PC 마우스 · 폰 touchscreen.tap · 길게 = 합성 touch 포인터(공용 WK_LONG).
  결과: 줄마다 「PASS|FAIL | 칸 · 엔진 · 바탕 …」 + 끝에 합계 · 종료 코드 = FAIL 수(바탕 칸은 yard 와 다르면 FAIL 로 셈).
"""
import os as _os_r, sys as _sys_r   # env_lanes — _roots.py 를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jagwa_common as JG   # noqa: E402
import json, os, sys, tempfile, time, traceback   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


SPEC_F = ARG('--spec')
if not SPEC_F:
    raise SystemExit('--spec <명세.json> 이 있어야 한다')
SPEC = json.load(open(SPEC_F, encoding='utf-8'))
NEWF = ARG('--new', _roots.genie('jagwa', 'index.html'))
BASE = ARG('--base', SPEC.get('base', 'origin/main'))
NOBASE = '--no-base' in sys.argv
BASE_ENGS = [x for x in (ARG('--base-eng', 'chromium') or '').split(',') if x]   # 헛잣대는 한 엔진이면 됨(시간) — 기본 chromium
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.strip() for x in (ARG('--only', '') or '').split(',') if x.strip()]
TMPD = os.path.join(tempfile.gettempdir(), 'h_small_gate')
OUTF = ARG('--res', os.path.join(TMPD, 'result_' + os.path.splitext(os.path.basename(SPEC_F))[0] + '.txt'))
SPD = ARG('--spd', _roots.spd())
NOTES = ARG('--notes', os.path.join(os.path.dirname(_roots.spd()), 'notes'))
VENDOR = ARG('--vendor', os.path.join(TMPD, 'vendor'))
JG.conf(VENDOR_PP=VENDOR, SPD_PP=SPD, NOTES=NOTES, SHOTS=os.path.join(TMPD, 'shots'))
SETTLE = int(SPEC.get('settle_ms', 5000))
DEV = {'pc': (1100, 800), 'ph': (384, 740)}
SRC = {'NEW': JG.app_src(NEWF)}
if not NOBASE:
    SRC['BASE'] = JG.app_src(BASE)
LINES, FAILS = [], [0]

LOC_JS = r"""([sel, nth]) => { const L = document.querySelectorAll(sel), e = L[nth || 0]; if (!e) return null;
  e.scrollIntoView({block: 'center', inline: 'nearest'}); const r = e.getBoundingClientRect();
  return {x: r.left + r.width / 2, y: r.top + r.height / 2, w: r.width, h: r.height} }"""


def out(s):
    print(s, flush=True)
    LINES.append(s)


def want(t):
    return not ONLY or any(t['name'].startswith(o) for o in ONLY)


def run_screen(br, eng, ver, sid, tests):
    sc = SPEC['screens'][sid]
    touch = sc.get('dev', 'pc') == 'ph'
    p = JG.Pg_PP(br, eng, 'sg-%s-%s-%s-%s' % (ver, eng, sid, int(time.time() * 1000) % 100000), SRC[ver], sc.get('subj', 'phys'),
                 DEV[sc.get('dev', 'pc')], touch=touch, remote=JG.Remote())
    res = {}
    try:
        try:
            if SPEC.get('prelude'):
                p.ev('()=>{try{' + SPEC['prelude'] + '}catch(e){return "prelude ERR "+e}}')
            p.ev('async()=>{try{return await (async()=>(' + sc.get('setup', '0') + '))()}catch(e){return "setup ERR "+e}}')
        except Exception as e:
            res['__setup'] = 'ERR ' + str(e)[:160]
        p.wait(SETTLE)
        for t in tests:
            ok, why = False, ''
            try:
                act = t.get('act', 'none')
                if act != 'none':
                    at = p.ev(LOC_JS, [t['sel'], t.get('nth', 0)])
                    if not at:
                        raise RuntimeError('누를 것 없음: ' + t['sel'])
                    p.wait(150)
                    at = p.ev(LOC_JS, [t['sel'], t.get('nth', 0)]) or at
                    if act == 'long':
                        p.long_press(at['x'], at['y'], ms=int(t.get('hold', 800)), wait=0)
                    elif act in ('click', 'type'):
                        if touch:
                            p.tap(at['x'], at['y'], wait=0)
                        else:
                            p.click(at['x'], at['y'], wait=0)
                        if act == 'type':
                            p.pg.keyboard.type(t.get('text', ''), delay=20)
                            if t.get('enter'):
                                p.pg.keyboard.press('Enter')
                p.wait(int(t.get('wait', 600)))
                v = p.ev('()=>{try{return (' + t['expect'] + ')}catch(e){return "ERR "+e}}')
                ok = v is True
                why = '' if ok else str(v)[:200]
            except Exception as e:
                why = str(e)[:200]
            res[t['name']] = (ok, why)
        errs = list(p.errs) + (p.ev('()=>window.__err||[]') or [])
        res['__errs'] = errs[:5]
    finally:
        p.close()
    return res


def main():
    tests = [t for t in SPEC['tests'] if want(t)]
    order = []
    for t in tests:
        if t['screen'] not in order:
            order.append(t['screen'])
    t0 = time.time()
    out('작은 고침 관문 — 명세 %s · 새 = %s · 바탕 = %s · 엔진 %s · 칸 %d' % (os.path.basename(SPEC_F), NEWF, 'X' if NOBASE else BASE, ','.join(ENGS), len(tests)))
    with sync_playwright() as pw:
        for eng in ENGS:
            br = getattr(pw, eng).launch()
            try:
                for sid in order:
                    T = [t for t in tests if t['screen'] == sid]
                    rn = run_screen(br, eng, 'NEW', sid, T)
                    dob = (not NOBASE) and eng in BASE_ENGS
                    rb = run_screen(br, eng, 'BASE', sid, T) if dob else {}
                    if rn.get('__setup'):
                        out('INFO | %s · %s · setup %s' % (sid, eng, rn['__setup']))
                    if rn.get('__errs'):
                        out('FAIL | %s · %s · 페이지 오류 %s' % (sid, eng, json.dumps(rn['__errs'], ensure_ascii=False)[:300]))
                        FAILS[0] += 1
                    for t in T:
                        ok, why = rn.get(t['name'], (False, '안 돎'))
                        yb = ''
                        if dob:
                            bok, _ = rb.get(t['name'], (False, ''))
                            yard = t.get('yard', True)
                            good = (not bok) if yard else bok
                            yb = ' · 바탕 %s%s' % ('PASS' if bok else 'FAIL', '' if good else (' ← 헛잣대 아님' if yard else ' ← 바탕도 PASS 여야'))
                            if not good:
                                FAILS[0] += 1
                        if not ok:
                            FAILS[0] += 1
                        out('%s | %s · %s%s%s' % ('PASS' if ok else 'FAIL', t['name'], eng, yb, (' | ' + why) if why else ''))
            finally:
                br.close()
    out('합계: FAIL %d · %.1f 분' % (FAILS[0], (time.time() - t0) / 60))
    os.makedirs(os.path.dirname(OUTF), exist_ok=True)
    open(OUTF, 'w', encoding='utf-8').write('\n'.join(LINES) + '\n')
    sys.exit(min(FAILS[0], 99))


if __name__ == '__main__':
    main()
