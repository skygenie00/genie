# -*- coding: utf-8 -*-
"""정리캔버스 교재 창 — 도구 막대(.cv-booknav)가 굴려도 팝업 머리(.ph) **아래**에 붙는가(사용자 「고쳐줘」 2026-09-24 03:2x ·
   _task_jo_ms_claude_editq 수행 결과 「관찰」 항목).

  NEW  = --new <파일>(없으면 genie 작업트리 jo/index.html) · BASE = genie 2e230f2 의 같은 파일(md5 fb8b383b · 이 판의 바탕)
         — 같은 잣대를 BASE 에 먼저 돌린다(헛잣대 · 규칙 ⑩) · 데이터 = genie jo/data(두 판 같은 것)
  교재 창 = _harness_canvas_jari 의 틀(SEED · /__book/ 로컬 교재 · pdf.js vendor · __HJ)을 모듈로 불러 그대로 쓴다
           (정리 탭 → 후보 블록 → 칩 「교재…」 → 자리 창 카드 누름 → bookShow)
  엔진 = chromium · webkit · 책상 1440×900(마우스) · 아이패드 768×1024 · 폰 390×844(진짜 터치 — chromium CDP 끌기 · webkit 톡)
  재는 것 = elementsFromPoint 맨 위(머리 세 점 · ✕ · 막대) · 막대 윗변 = 머리 아랫변 · 굴린 채 ✕ 누름 = 닫힘 · 굴린 채 머리 끌기 = 창 옮김 ·
           굴린 채 ▶ = 다음 쪽(무변) · 굴리기 전 막대 자리 = 바탕과 같음(무변)

쓰기 : python _harness_jo_book_nav.py [--new 파일] [--out 폴더] [--eng chromium|webkit] [--vp desk|ipad|phone]
"""
import hashlib, io, json, os, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
CJH = r'N:\개인\claude\jopangi\공통\_harness'
sys.path.insert(0, CJH)
import _harness_canvas_jari as CJ          # noqa: E402 — 틀(P · serve · ground · open_jari)
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


HERE = os.path.dirname(os.path.abspath(__file__))
OUT = ARG('--out', HERE)
NEWF = ARG('--new', os.path.join(CJ.GENIE, 'jo', 'index.html'))
BASE_REV, BASE_MD5 = '2e230f2', 'fb8b383b26aec7eead7da365cbfa9906'
VPS = [('desk', 1440, 900, False), ('ipad', 768, 1024, True), ('phone', 390, 844, True)]

BOOK = "POPS.find(x=>(x._pk||'').indexOf('cv|book|')===0)"
SETSC = "(sc)=>{const w=" + BOOK + ";if(!w)return null;const mx=w.scrollHeight-w.clientHeight;w.scrollTop=(sc==='max')?mx:Math.min(sc,mx);return {sc:w.scrollTop,max:mx};}"
MEAS = r"""()=>{const w=""" + BOOK + r""";if(!w)return null;
 const ph=w.querySelector(':scope > .ph'),nav=w.querySelector('.cv-booknav');
 const r=e=>{const q=e.getBoundingClientRect();return {x:+q.left.toFixed(2),y:+q.top.toFixed(2),w:+q.width.toFixed(2),h:+q.height.toFixed(2),b:+q.bottom.toFixed(2),r:+q.right.toFixed(2)};};
 const H=r(ph),N=nav?r(nav):null,W=r(w);
 const top=(x,y)=>{const a=document.elementsFromPoint(x,y);return a.length?a[0]:null;};
 const nm=e=>{if(!e)return null;const c=e.className;return String(c&&c.baseVal!==undefined?c.baseVal:(c||e.tagName)).slice(0,40)||e.tagName;};
 const hits=[0.25,0.5,0.75].map(f=>{const x=H.x+H.w*f,y=H.y+H.h/2;const e=top(x,y);return {x:+x.toFixed(1),y:+y.toFixed(1),in:!!e&&ph.contains(e),at:nm(e)};});
 const xb=ph.querySelector('button:not(.pall)');let xh=null;if(xb){const X=r(xb);const e=top(X.x+X.w/2,X.y+X.h/2);xh={in:!!e&&(e===xb||xb.contains(e)),at:nm(e)};}
 let nh=null;if(nav){const e=top(N.x+Math.min(30,N.w/2),N.y+N.h/2);nh={in:!!e&&nav.contains(e),at:nm(e)};}
 return {sc:w.scrollTop,max:w.scrollHeight-w.clientHeight,H,N,W,hits,xh,nh,cvph:getComputedStyle(w).getPropertyValue('--cvph').trim(),
   navTop:nav?getComputedStyle(nav).top:null,onScreen:H.y>=0&&H.b<=innerHeight,page:(w.querySelector('#cvBookP')||{}).value||null};}"""
PT = r"""(what)=>{const w=""" + BOOK + r""";if(!w)return null;const ph=w.querySelector(':scope > .ph');
 const t=what==='x'?ph.querySelector('button:not(.pall)'):what==='nx'?w.querySelector('.cv-booknav [data-nx]'):ph;if(!t)return null;
 const q=t.getBoundingClientRect();const cx=what==='head'?q.left+Math.min(40,q.width/4):q.left+q.width/2,cy=q.top+q.height/2;
 const e=document.elementFromPoint(cx,cy);const W=w.getBoundingClientRect();
 return {cx:+cx.toFixed(1),cy:+cy.toFixed(1),on:!!e&&(e===t||t.contains(e)),at:e?String(e.className||e.tagName).slice(0,40):null,wx:W.left,wy:W.top};}"""


def tap(p, x, y, wait=500):
    """자리 그대로 누른다(덮였어도 — 바탕에서 무엇이 눌리는지 보이게)."""
    if p.pad:
        p.pg.touchscreen.tap(x, y)
    else:
        p.pg.mouse.click(x, y)
    p.pg.wait_for_timeout(wait)


def scen(br, eng, tag, src, vp, W, H, pad):
    R = {'eng': eng, 'tag': tag, 'vp': vp}
    p = CJ.P(br, eng, 'NAV' + tag, src, W, H, pad=pad)
    try:
        G = GR
        R['boot'] = p.ev("__HJ.boot()")
        R['jari'] = CJ.open_jari(p, G, G['CAND'])
        at = p.ev("([b,w,i])=>__HJ.jariAt(b,w,i)", [G['CAND'], 'card', 0]); p.click(at, 700)
        R['book'] = p.ev("__HJ.bookReady()")
        if not R['book'].get('n'):
            R['exc'] = '교재 창이 안 열림'
            return R
        R['m'] = {}
        for sc in (0, 120, 400, 'max'):
            R['m'][str(sc)] = {'set': p.ev(SETSC, sc)}
            p.pg.wait_for_timeout(180)
            R['m'][str(sc)].update(p.ev(MEAS))
        # 굴린 채 ▶(무변 — 막대는 바탕에서도 눌린다)
        p.ev(SETSC, 300); p.pg.wait_for_timeout(180)
        a = p.ev(PT, 'nx'); p0 = p.ev(MEAS).get('page')
        tap(p, a['cx'], a['cy'], 700); p.ev("__HJ.bookReady()")
        R['nx'] = {'at': a, 'p0': p0, 'p1': p.ev(MEAS).get('page')}
        # 굴린 채 머리 끌기 — 창이 옮겨지는가
        p.ev(SETSC, 300); p.pg.wait_for_timeout(180)
        a = p.ev(PT, 'head')
        kind = p.drag(a['cx'], a['cy'], a['cx'] - 70, a['cy'] + 30); p.pg.wait_for_timeout(400)
        b = p.ev(PT, 'head')
        R['drag'] = {'at': a, 'kind': kind, 'dx': round((b or {}).get('wx', 0) - a['wx'], 1), 'dy': round((b or {}).get('wy', 0) - a['wy'], 1),
                     'page': p.ev(MEAS).get('page')}
        # 굴린 채 ✕ — 닫히는가
        p.ev(SETSC, 300); p.pg.wait_for_timeout(180)
        a = p.ev(PT, 'x'); n0 = p.ev("__HJ.book()").get('n')
        tap(p, a['cx'], a['cy'], 600)
        R['x'] = {'at': a, 'n0': n0, 'n1': p.ev("__HJ.book()").get('n')}
        R['errs'] = [x for x in (p.ev("__HJ.errs()") + p.errs) if not NOISE(x)]
    except Exception as e:
        R['exc'] = repr(e)[:400]
    finally:
        p.close()
    return R


def NOISE(x):
    return CJ.NOISE(x) if hasattr(CJ, 'NOISE') else False


L, CNT, NULL = [], {'PASS': 0, 'FAIL': 0}, {}


def T(name, ok, info=None, tag='NEW'):
    ok = bool(ok)
    if tag == 'BASE':
        NULL.setdefault(name, []).append(ok)
        return
    CNT['PASS' if ok else 'FAIL'] += 1
    L.append('%s | %s%s' % ('PASS' if ok else 'FAIL', name, '' if ok else ' | ' + json.dumps(info, ensure_ascii=False, default=str)[:600]))


def gates(R, tag, BASER=None):
    pre = '[%s %s] ' % (R['eng'], R['vp'])
    if R.get('exc'):
        T(pre + '교재 창 열고 재기', False, R.get('exc'), tag)
        return
    m = R['m']
    m0 = m['0']
    T(pre + '굴리기 전 — 머리 세 점·✕ 맨 위 = 머리 · 막대 맨 위 = 막대', all(h['in'] for h in m0['hits']) and (m0['xh'] or {}).get('in') and (m0['nh'] or {}).get('in'), m0, tag)
    for k in ('120', '400', 'max'):
        x = m[k]
        if not x.get('sc') or x['sc'] < 30:
            T(pre + '굴림 %s — 굴릴 거리 있음' % k, False, x, tag)
            continue
        T(pre + '굴림 %s(scrollTop %d) — 머리 세 점 맨 위 = 머리 · ✕ 맨 위 = ✕' % (k, x['sc']), all(h['in'] for h in x['hits']) and (x['xh'] or {}).get('in'), {'hits': x['hits'], 'xh': x['xh']}, tag)
        T(pre + '굴림 %s — 막대 윗변 = 머리 아랫변(±1) · 막대 맨 위 = 막대' % k,
          x.get('N') and abs(x['N']['y'] - x['H']['b']) <= 1 and (x['nh'] or {}).get('in'), {'N': x.get('N'), 'H': x.get('H'), 'nh': x.get('nh'), 'navTop': x.get('navTop'), 'cvph': x.get('cvph')}, tag)
    T(pre + '굴린 채 ▶ → 다음 쪽(무변)', R['nx'].get('p0') and R['nx'].get('p1') and int(R['nx']['p1']) == int(R['nx']['p0']) + 1, R['nx'], tag)
    T(pre + '굴린 채 머리 끌기 → 창이 옮겨짐(|Δx|+|Δy| ≥ 20) · 쪽 번호 그대로', abs(R['drag']['dx']) + abs(R['drag']['dy']) >= 20 and R['drag'].get('page') == R['nx'].get('p1'), R['drag'], tag)
    T(pre + '굴린 채 ✕ → 교재 창 닫힘', R['x'].get('n0') == 1 and R['x'].get('n1') == 0, R['x'], tag)
    if tag == 'NEW':
        T(pre + '콘솔 오류 0', not R.get('errs'), R.get('errs'))
        x = m['400'] if m['400'].get('N') else m['120']
        T(pre + '--cvph = 머리 높이(±0.5) · 막대 top 계산값 = 그 값', x.get('cvph', '').endswith('px') and abs(float(x['cvph'][:-2]) - x['H']['h']) <= 0.5 and x.get('navTop') == x.get('cvph').replace(' ', ''),
          {'cvph': x.get('cvph'), 'H': x.get('H'), 'navTop': x.get('navTop')})
        if BASER and not BASER.get('exc'):
            b0 = BASER['m']['0']
            T(pre + '굴리기 전 막대 자리 = 바탕(±0.5 · 쉬는 자리 무변)', b0.get('N') and m0.get('N') and all(abs(b0['N'][k] - m0['N'][k]) <= 0.5 for k in ('x', 'y', 'w', 'h')) and abs(b0['H']['h'] - m0['H']['h']) <= 0.5,
              {'base': b0.get('N'), 'new': m0.get('N')})


def main():
    base_b = subprocess.run(['git', '-C', CJ.GENIE, 'show', BASE_REV + ':jo/index.html'], capture_output=True).stdout
    new_raw = open(NEWF, 'rb').read()
    RES = {'src': {'base': [len(base_b), hashlib.md5(base_b).hexdigest()],
                   'new': [len(new_raw), hashlib.md5(new_raw.replace(b'\r\n', b'\n')).hexdigest(), new_raw.count(b'\r\n'), NEWF]}}
    global GR
    GR = CJ.ground()
    RES['CAND'] = GR['CAND']
    t00 = time.time()
    os.makedirs(CJ.WORK, exist_ok=True)
    srcs = {'BASE': base_b.decode('utf-8'), 'NEW': new_raw.decode('utf-8')}
    with sync_playwright() as pw:
        brs = {e: getattr(pw, e).launch() for e in ('chromium', 'webkit')}
        try:
            for eng in [e for e in ('chromium', 'webkit') if ARG('--eng') in (None, e)]:
                for vp, W, H, pad in [v for v in VPS if ARG('--vp') in (None, v[0])]:
                    for tag in ('BASE', 'NEW'):
                        t0 = time.time(); print('… %s %s %s %s' % (eng, vp, tag, time.strftime('%H:%M:%S')), flush=True)
                        RES['%s/%s/%s' % (eng, vp, tag)] = r = scen(brs[eng], eng, tag, srcs[tag], vp, W, H, pad)
                        print('   %.1fs %s' % (time.time() - t0, r.get('exc', '')), flush=True)
        finally:
            for b in brs.values():
                b.close()
            for srv, _ in CJ.SERVERS.values():
                srv.shutdown()
    RES['sec'] = round(time.time() - t00, 1)
    os.makedirs(os.path.join(CJ.WORK, 'nav'), exist_ok=True)
    json.dump(RES, io.open(os.path.join(CJ.WORK, 'nav', 'raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    report(RES)


def report(RES):
    L.append('INFO | 바탕 BASE = %s:jo/index.html | %d B · md5 %s' % (BASE_REV, RES['src']['base'][0], RES['src']['base'][1]))
    T('바탕 md5 = %s…(genie 2e230f2 · ms_claude_editq 인도 판)' % BASE_MD5[:8], RES['src']['base'][1] == BASE_MD5, RES['src']['base'])
    L.append('INFO | 새 판 NEW | %d B · md5(LF) %s · CRLF %d · %s' % tuple(RES['src']['new']))
    L.append('INFO | 후보 블록(자리 창 → 카드 0 → 교재 창) | %s' % RES.get('CAND'))
    L.append('INFO | 시간(초) | %s' % RES.get('sec'))
    for eng in ('chromium', 'webkit'):
        for vp, W, H, pad in VPS:
            B = RES.get('%s/%s/BASE' % (eng, vp)) or {}
            N = RES.get('%s/%s/NEW' % (eng, vp)) or {}
            if B:
                gates(B, 'BASE')
            if N:
                gates(N, 'NEW', B)
            if N.get('m'):
                x = N['m'].get('400') or {}
                L.append('INFO | [%s %s] 굴림 400 — 머리 %s · 막대 %s · --cvph %s · 막대 top %s · 창 %s' % (eng, vp, x.get('H'), x.get('N'), x.get('cvph'), x.get('navTop'), x.get('W')))
            if B.get('m'):
                x = B['m'].get('400') or {}
                L.append('INFO | [%s %s] 바탕 굴림 400 — 머리 가운데 점 맨 위 = %s · ✕ 자리 맨 위 = %s' % (eng, vp, [h.get('at') for h in x.get('hits') or []], (x.get('xh') or {}).get('at')))
    tot = sum(len(v) for v in NULL.values()); fails = sum(1 for v in NULL.values() for x in v if not x)
    L.append('')
    L.append('── 헛잣대(규칙 ⑩) — 같은 잣대를 바탕 %s 에 돌린 결과: %d 중 FAIL %d · PASS %d ──' % (BASE_REV, tot, fails, tot - fails))
    for n in NULL:
        v = NULL[n]
        L.append('BASE | %s | %s' % (n, 'FAIL' if not all(v) else 'PASS'))
    body = '\n'.join(L) + '\n\n합계  PASS %d · FAIL %d  (%s초)\n' % (CNT['PASS'], CNT['FAIL'], RES.get('sec'))
    print(body[-4000:])
    p = os.path.join(OUT, '_harness_jo_book_nav_result.txt')
    b = body.encode('utf-8')
    for _ in range(3):
        open(p, 'wb').write(b); time.sleep(0.5)
        if open(p, 'rb').read() == b:
            break


GR = None
if __name__ == '__main__':
    if '--report' in sys.argv:
        report(json.load(io.open(os.path.join(CJ.WORK, 'nav', 'raw.json'), encoding='utf-8')))
    else:
        main()
