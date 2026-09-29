# -*- coding: utf-8 -*-
"""폰 목록 단원 칩 넘침 고침 관문(2026-09-29 · _patch_jagwa_chipwrap.py)

  python _harness_jagwa_chipwrap.py [--new <앱>] [--eng chromium,webkit] [--res <결과>]

  NEW = genie 작업트리 jagwa/index.html · BASE(헛잣대) = genie HEAD(바로 앞 인도판 = jagwa_search)
  틀 = _harness_jagwa_phone_win 의 Pg(폰 390×844 손가락 · PC 1553×900 마우스 · 같은 출처 데이터 · 기록 PUT 가로챔)
  C1 폰 세 과목 — 머리 펼친 뒤 목록 안 가로 넘침 0 · 쪽 scrollWidth = clientWidth(바탕 생물 = 넘침)
  C2 폰 목록 글자(textContent) = 바탕
  C3 폰 생물 가장 긴 단원 칩 — 화면 안 · 칩 안 두 줄 이상 · 손가락 톡 → 그 단원으로 거름(FL.unit = data-unit)
  C4 PC 칩 자리·크기 = 바탕 · 목록 글자 = 바탕
  ⚠ 자과앱 픽셀 게이트 없음(CLAUDE.md) — 자리 = getBoundingClientRect · 가림 = elementFromPoint
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import io, json, os, sys, time, hashlib
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = _roots.genie()
NEWF = ARG('--new', os.path.join(GENIE, 'jagwa', 'index.html'))
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_chipwrap_result.txt'))
_argv = sys.argv; sys.argv = [sys.argv[0]]
import _harness_jagwa_phone_win as PW   # noqa: E402
sys.argv = _argv
from playwright.sync_api import sync_playwright   # noqa: E402
RES = []

CJS = """
window.__C={
 over(){const W=document.documentElement.clientWidth,L=document.getElementById('list'),bad=[];
   if(L)L.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();if(r.width>0&&r.right>W+0.5)bad.push(String(e.className||e.tagName).slice(0,24)+':'+Math.round(r.right))});
   return {W,sw:document.documentElement.scrollWidth,n:bad.length,first:bad.slice(0,4),items:L?L.querySelectorAll('.item').length:0}},
 text(){const L=document.getElementById('list');return L?String(L.textContent||''):''},
 tags(){return [...document.querySelectorAll('#list .item .meta .tag')].slice(0,600).map(e=>{const r=e.getBoundingClientRect();return [Math.round(r.left*10)/10,Math.round(r.top*10)/10,Math.round(r.width*10)/10,Math.round(r.height*10)/10]})},
 longest(){const t=[...document.querySelectorAll('#list .item .meta .tag.unit')];if(!t.length)return null;
   const e=t.reduce((a,b)=>(String(b.textContent).length>String(a.textContent).length?b:a));
   e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect(),cs=getComputedStyle(e);
   const lh=parseFloat(cs.lineHeight)||parseFloat(cs.fontSize)*1.4;
   const inner=r.height-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom)-parseFloat(cs.borderTopWidth)-parseFloat(cs.borderBottomWidth);
   return {txt:String(e.textContent),unit:e.dataset.unit||'',right:Math.round(r.right),h:Math.round(r.height*10)/10,lines:Math.round(inner/lh),W:document.documentElement.clientWidth,hit:__W.hit(e)}},
 unitNow(){return (typeof FL!=='undefined'&&FL)?String(FL.unit||''):null}
};
"""


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def md(t):
    return hashlib.md5(t.encode('utf-8')).hexdigest()[:8] + ':' + str(len(t))


def open_head(q):
    q.ev(CJS)
    fb = q.ev("()=>__W.at('#fFoldBtn')")
    if fb and q.ev("()=>document.body.classList.contains('fold')"):
        q.press(fb, 700)
    q.wait(500)


def phone(br, eng, subj):
    def f(q):
        open_head(q)
        o = {'over': q.ev("()=>__C.over()"), 'text': md(q.ev("()=>__C.text()")), 'fold': q.ev("()=>document.body.classList.contains('fold')")}
        if subj == 'bio':
            lg = q.ev("()=>__C.longest()")
            o['long'] = lg
            if lg and lg.get('hit') and lg['hit'].get('on'):
                q.press(lg['hit'], 900)
                o['unitAfter'] = q.ev("()=>__C.unitNow()")
        return o
    return PW.both(br, eng, subj, True, f)


def pc(br, eng, subj):
    def f(q):
        q.ev(CJS); q.wait(300)
        return {'tags': q.ev("()=>__C.tags()"), 'text': md(q.ev("()=>__C.text()")), 'over': q.ev("()=>__C.over()")}
    return PW.both(br, eng, subj, False, f)


def main():
    PW.APPS['NEW'] = io.open(NEWF, encoding='utf-8').read()
    PW.APPS['BASE'] = PW.git('show', 'HEAD:jagwa/index.html').decode('utf-8')
    t0 = time.time()
    with sync_playwright() as pw:
        for eng in ENGS:
            br = getattr(pw, eng).launch()
            try:
                for subj in ('phys', 'bio', 'earth'):
                    r = phone(br, eng, subj)
                    n, b = r['NEW'], r['BASE']
                    T('C1', '%s 폰 %s — 머리 펼친 뒤 목록 안 가로 넘침 0 · 쪽 scrollWidth = clientWidth' % (eng, subj),
                      n['over']['n'] == 0 and n['over']['sw'] <= n['over']['W'] and not n['fold'] and n['over']['items'] > 0,
                      {'NEW': n['over'], '바탕': b['over']})
                    if subj == 'bio':
                        T('C1-헛', '%s 헛잣대 바탕 — 폰 생물 목록이 가로로 넘침' % eng, b['over']['n'] > 0 and b['over']['sw'] > b['over']['W'], b['over'])
                    T('C2', '%s 폰 %s — 목록 글자 = 바탕' % (eng, subj), n['text'] == b['text'], [n['text'], b['text']])
                    if subj == 'bio':
                        lg, lb = n.get('long') or {}, b.get('long') or {}
                        T('C3', '%s 폰 생물 가장 긴 단원 칩 — 화면 안 · 칩 안 두 줄 이상 · 손가락 톡 → 그 단원으로 거름' % eng,
                          bool(lg) and lg['right'] <= lg['W'] and lg['lines'] >= 2 and lg['hit']['on'] and n.get('unitAfter') == lg['unit'] and lg['txt'] == lb.get('txt'),
                          {'NEW': {k: lg.get(k) for k in ('txt', 'right', 'h', 'lines', 'W')}, '톡 뒤 FL.unit': n.get('unitAfter'), '단원': lg.get('unit'),
                           '바탕': {k: lb.get(k) for k in ('right', 'h', 'lines')}, '바탕 톡': b.get('unitAfter')})
                    T('Z', '%s 폰 %s 오류 0' % (eng, subj), not r['NEW_err'], r['NEW_err'][:3])
                    rp = pc(br, eng, subj)
                    T('C4', '%s PC %s — 칩 자리·크기 = 바탕(%d 칩) · 목록 글자 = 바탕 · 넘침 0' % (eng, subj, len(rp['NEW']['tags'])),
                      rp['NEW']['tags'] == rp['BASE']['tags'] and rp['NEW']['text'] == rp['BASE']['text'] and rp['NEW']['over']['n'] == 0 and len(rp['NEW']['tags']) > 0,
                      {'다른 칩': [i for i, (x, y) in enumerate(zip(rp['NEW']['tags'], rp['BASE']['tags'])) if x != y][:5], '글자': [rp['NEW']['text'], rp['BASE']['text']]})
            finally:
                br.close()
    npass = sum(1 for x in RES if x[2]); nfail = sum(1 for x in RES if not x[2])
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as fo:
        fo.write('\n==== %s · chipwrap · NEW %s · 바탕 genie HEAD %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), os.path.basename(NEWF),
                 PW.git('rev-parse', '--short', 'HEAD').decode().strip(), ','.join(ENGS)))
        for g, nm, ok, d in RES:
            fo.write('%s | %s · %s | %s\n' % ('PASS' if ok else 'FAIL', g, nm, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:1200]))
        fo.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
