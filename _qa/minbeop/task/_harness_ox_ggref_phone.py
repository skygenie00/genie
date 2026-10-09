# -*- coding: utf-8 -*-
r"""_task_cloud_batch_1010 클라우드 ① ③ 관문 — 민법OX 「연결한 근거」 줄 폰 꼴(ggRefRowHTML = ggPanelHTML 10/6 ox_gg_phone 꼴)

  python _harness_ox_ggref_phone.py [--new <앱>] [--base <판 = 7299ec3>] [--only R1,…] [--spd <studyplandata>] [--tw <Tailwind 사본>] [--res <결과>] [--shots <그림>]

  NEW = genie 작업트리 minbeop/index.html · BASE = 바탕 7299ec3(헛잣대 — 폰 글 폭 ≈ 반 · 누를 자리 = 글자 높이 → FAIL 이어야)
  데이터 = studyplandata 현행(문항 · 기록 · 가짜 GitHub · PUT 메모리 · OL = _ox_live.py) — 연결한 근거가 있는 문항 셋(댓글 많은 차례 · 쪽 안에서 고름)
  기기 = 폰 390×844(hasTouch · 모바일 · 톡 = CDP Input.dispatchTouchEvent) · PC 1100×800(마우스) · 엔진 = Chromium(WebKit 칸은 로컬 몫)
  펼침 = 문항 팝업(openQPopup) 근거 줄 「🔗 <uid>」 칩 진짜 누름 → 연결 상자(#qp-refgg-box-…)
  ⚠ 문항 · 근거 · 댓글 글은 출력하지 않는다(D11) — 문항 ID · 폭 · 자리 수만
  관문:
    R1 폰 — 줄마다(본문 줄 · 댓글 줄) 글 폭(줄 안쪽 왼끝 → 글 덩어리 오른끝) ≥ 줄 폭 90 % · 「✎ 여기서 고치기」 누를 자리(가운데서 같은 요소로 잡히는 폭 · 높이) ≥ 36 ·
       겹침 0(글 덩어리 ↔ 단추 네모 겹침 0 · 상자 안 누를 것마다 가운데가 제 것으로 잡힘) · 단추 = 줄 오른끝
    R2 PC — 넓으면 한 줄(단추가 글 첫 줄과 같은 줄 · 줄 오른끝) · 겹침 0 · 누를 자리 = INFO(마우스)
    R3 누름 = 고치기 칸 열림 — 본문 줄 · 댓글 줄 「✎」 진짜 누름 → 그 칸 보임 · 글 = 저장된 글 · 「취소」 진짜 누름 → 닫힘 · 폰은 단추 네모 밖(위로 13px · 넓힌 누를 자리)을 눌러도 열림
    R4 화면 훑기 — 연결 상자(폰 · PC) 가로 넘침 · 상자 밖 · 화면 밖 0 · 페이지 오류 0
  결과 = 화면 PASS/FAIL/INFO 줄 · --res(기본 = 임시 폴더 · _qa 에 결과를 쓰지 않는다)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402,F401 — --mode · --snap-in · --snap-out 을 뗀다
import json, os, sys, tempfile, time, traceback   # noqa: E402
_sys_r.path.append(_os_r.path.dirname(_os_r.path.abspath(__file__)))
import _ox_live as OL   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEWF = ARG('--new', _roots.genie('minbeop', 'index.html'))
BASE = ARG('--base', '7299ec3')
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
TMPD = os.path.join(tempfile.gettempdir(), 'h_ox_ggref_phone')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_ox_ggref_phone_result.txt'))
OL.conf(spd=ARG('--spd', _roots.spd()), tw=ARG('--tw'), shots=ARG('--shots', os.path.join(TMPD, 'shots')))
GATE = QC.GATE   # gate = 바탕을 띄워 헛잣대 · regress · smoke = 새 판만(바탕 풀기 · 띄우기 0)
if GATE:
    QC.sub('git:show-app')
SRC = {'NEW': OL.app_src(NEWF)}
if GATE:
    SRC['BASE'] = OL.app_src(BASE)
VERS = tuple(SRC)
OL.ON_LAUNCH = lambda tag: QC.launch('base' if tag == 'BASE' else 'new')
RES = []
STEP = {}
T0 = time.time()


def want(c):
    return (not ONLY or c in ONLY) and (not QC.SMOKE or c == 'R1')   # smoke = R1 폰 한 칸


def _s(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


def R(g, name, new, base=None, d='', yard=True):
    RES.append(dict(g=g, name=name, new=new, base=base, yard=yard, d=d))
    tag = 'INFO' if new is None else ('PASS' if new else 'FAIL')
    yb = '' if base is None else (' · 바탕 ' + (('PASS(바탕도 같음)' if yard else 'PASS') if base else 'FAIL'))
    print('%s | %s · %s%s | %s' % (tag, g, name, yb, _s(d)[:1000]), flush=True)


# 연결한 근거가 있는 문항 셋 — 연결 대상 근거의 댓글 많은 차례 · 근거 항목 많은 차례 · ID 차례
PICK_JS = r"""(()=>{const out=[];for(const q of quizData){let us=[];try{us=refOf(q.id,'geunge')}catch(e){us=[]}if(!us.length)continue;
  for(const u of us){if(refTextOf(u,'geunge')===null)continue;const L=ggOf(u).filter(Boolean);if(!L.length)continue;
    out.push([L.reduce((a,g)=>a+(Array.isArray(g.cs)?g.cs.filter(Boolean).length:0),0),L.length,String(q.id),String(u)])}}
  out.sort((a,b)=>b[0]-a[0]||b[1]-a[1]||(a[2]<b[2]?-1:a[2]>b[2]?1:0));const seen=new Set(),pick=[];
  for(const x of out){if(seen.has(x[2]))continue;seen.add(x[2]);pick.push(x);if(pick.length>=3)break}return pick})()"""

MEASURE_JS = r"""(sel)=>{const box=document.querySelector(sel);if(!box||!__H.vis(box))return null;const out={rows:[],over:[]};
 const rows=[...box.querySelectorAll('[data-gbbox] > div')].filter(r=>__H.vis(r)&&r.querySelector(':scope > button[onclick^="ggRefEdit"]'));
 rows.forEach(r=>{const cs=getComputedStyle(r),rb=r.getBoundingClientRect(),pl=parseFloat(cs.paddingLeft)||0,pr=parseFloat(cs.paddingRight)||0;
   const L=rb.left+(parseFloat(cs.borderLeftWidth)||0)+pl,W=r.clientWidth-pl-pr;const btn=r.querySelector(':scope > button[onclick^="ggRefEdit"]');
   const kids=[...r.children].filter(k=>k!==btn&&__H.vis(k));const right=Math.max(...kids.map(k=>k.getBoundingClientRect().right));const bb=btn.getBoundingClientRect();
   const inter=kids.some(k=>{const a=k.getBoundingClientRect();return Math.min(a.right,bb.right)-Math.max(a.left,bb.left)>0.5&&Math.min(a.bottom,bb.bottom)-Math.max(a.top,bb.top)>0.5});
   btn.scrollIntoView({block:'center'});const hb=__H.hitBox(btn);const b2=btn.getBoundingClientRect(),k0=kids[0].getBoundingClientRect(),rr=r.getBoundingClientRect();
   out.rows.push({kind:r.classList.contains('pl-3')?'댓글':'본문',ratio:+((right-L)/W).toFixed(3),W:Math.round(W),btn:[Math.round(bb.width),Math.round(bb.height)],hit:[hb.w,hb.h],
     sameLine:b2.top<k0.top+6,atRight:Math.abs((rr.right-pr-(parseFloat(cs.borderRightWidth)||0))-b2.right)<=1.5,inter})});
 [...box.querySelectorAll('button,[onclick]')].filter(__H.vis).forEach(e=>{e.scrollIntoView({block:'center'});const b=e.getBoundingClientRect(),x=b.left+b.width/2,y=b.top+b.height/2;
   const a=document.elementFromPoint(x,y);if(!(a&&(a===e||e.contains(a))))out.over.push((e.tagName+'.'+String(e.className).slice(0,18))+' → '+(a?a.tagName+'.'+String(a.className).slice(0,18):'null'))});
 return out}"""

SWEEP_JS = r"""(sel)=>{const out=[];const R=document.querySelector(sel);if(!R||!__H.vis(R))return ['(없음) '+sel];R.scrollIntoView({block:'center'});
 const rb=R.getBoundingClientRect();if(rb.left<-1||rb.right>innerWidth+1)out.push('상자 화면 밖 '+[Math.round(rb.left),Math.round(rb.right)]);
 if(document.scrollingElement.scrollWidth>innerWidth+1)out.push('page-hscroll');
 [R,...R.querySelectorAll('*')].forEach(e=>{if(!__H.vis(e))return;const cs=getComputedStyle(e),b=e.getBoundingClientRect();
   if((cs.overflowX==='auto'||cs.overflowX==='scroll'||cs.overflowX==='hidden')&&e.scrollWidth>e.clientWidth+1&&e.clientWidth>0)out.push('가로 넘침:'+e.tagName+'.'+String(e.className).slice(0,24));
   if(b.width>0&&(b.right>rb.right+1||b.left<rb.left-1))out.push('상자 밖:'+e.tagName+'.'+String(e.className).slice(0,24))});
 return [...new Set(out)].slice(0,8)}"""


def open_box(p, uid, u):
    """문항 팝업 → 근거 줄 「🔗 u」 칩 진짜 누름 → 연결 상자"""
    p.ev("(o)=>{openQPopup(o)}", uid)
    p.wait(800)
    chip = '#qp-gg-refchip-%s-%s' % (uid, u)
    at = p.ev("(s)=>__H.hit(document.querySelector(s))", chip)
    if at and at.get('on'):
        p.press(at['cx'], at['cy'])
    else:
        p.ev("([o,u])=>{ggRefToggle(o,u,'qp-')}", [uid, u])
    p.wait(500)
    box = '#qp-refgg-box-%s-%s' % (uid, u)
    return box, bool(at and at.get('on')), p.ev("(s)=>__H.vis(document.querySelector(s))", box)


ED_JS = r"""(sel)=>[...document.querySelectorAll(sel+' button[onclick^="ggRefEdit"]')].filter(b=>__H.vis(b)&&/고치기/.test(b.textContent))"""   # 「✎ 여기서 고치기」 만(칸 안 「취소」 도 ggRefEdit)
PRESS_JS = r"""(sel)=>{const box=document.querySelector(sel);if(!box)return [];return (""" + ED_JS + r""")(sel).map(b=>{
  const m=/ggRefEdit\(([^)]*)\)/.exec(b.getAttribute('onclick')||'');const a=m?m[1].split(',').map(x=>x.trim().replace(/^'|'$/g,'')):[];
  return {uid:a[0],u:a[1],k:a[2],ck:(a[3]&&a[3]!=='undefined')?a[3]:null}})}"""


def edit_box_sel(t):
    eid = '%s-%s-%s' % (t['uid'], t['u'], t['k']) + ('-' + t['ck'] if t['ck'] is not None else '')
    return ('#qp-refgg-cedit-' if t['ck'] is not None else '#qp-refgg-edit-') + eid, ('#qp-refgg-cein-' if t['ck'] is not None else '#qp-refgg-ein-') + eid


def press_test(p, box, dev):
    """✎ 진짜 누름 → 칸 열림 · 글 = 저장된 글 · 「취소」 → 닫힘 · (폰) 단추 네모 위 13px 누름 → 열림"""
    out = []
    targets = p.ev(PRESS_JS, box)
    nth = "([s,i])=>__H.hit((" + ED_JS + ")(s)[i])"
    for i, t in enumerate(targets[:3]):
        esel, isel = edit_box_sel(t)
        at = p.ev(nth, [box, i])
        if not at or not at.get('on'):
            out.append({'줄': '댓글' if t['ck'] is not None else '본문', '누름 → 열림': False, '글 = 저장된 글': None, '취소 → 닫힘': None, '네모 밖 13px': None, '까닭': '단추 누를 자리 없음 ' + _s(at)[:80]})
            continue
        p.press(at['cx'], at['cy'])
        p.wait(300)
        st = p.ev("""([e,i,u,k,ck])=>{const b=document.querySelector(e),inp=document.querySelector(i);const g=ggItem(u,k);const c=(g&&ck!==null)?ggCsOf(g,ck):null;
          return {open:!!b&&!b.classList.contains('hide')&&__H.vis(b),same:!!inp&&!!g&&inp.value===(ck!==null?((c&&c.t)||''):(g.t||''))}}""", [esel, isel, t['u'], t['k'], t['ck']])
        cancel = p.ev("(e)=>{const b=document.querySelector(e);const x=b?[...b.querySelectorAll('button')].find(z=>/취소/.test(z.textContent)):null;return x?__H.hit(x):null}", esel)
        closed = None
        if cancel and cancel.get('on'):
            p.press(cancel['cx'], cancel['cy'])
            p.wait(300)
            closed = p.ev("(e)=>{const b=document.querySelector(e);return !!b&&b.classList.contains('hide')}", esel)
        edge = None
        if dev['touch']:   # 넓힌 누를 자리 — 단추 네모 위 13px(글자 높이 밖 · 36px 안)
            at = p.ev(nth, [box, i])
            bh = at['h']
            p.press(at['cx'], at['cy'] - 13)
            p.wait(300)
            edge = {'단추 높이': bh, '열림': p.ev("(e)=>{const b=document.querySelector(e);return !!b&&!b.classList.contains('hide')}", esel)}
            if edge['열림']:
                p.ev("(e)=>{const b=document.querySelector(e);const x=b?[...b.querySelectorAll('button')].find(z=>/취소/.test(z.textContent)):null;if(x)x.click()}", esel)
                p.wait(200)
        out.append({'줄': '댓글' if t['ck'] is not None else '본문', '누름 → 열림': st['open'], '글 = 저장된 글': st['same'], '취소 → 닫힘': closed, '네모 밖 13px': edge})
    ok = bool(out) and all(x['누름 → 열림'] and x['글 = 저장된 글'] and x['취소 → 닫힘'] and (x['네모 밖 13px'] is None or x['네모 밖 13px']['열림']) for x in out)
    return ok, out


def run(br, v, dev, picks):
    p = OL.Live(br, v, SRC[v], dev)
    res = []
    try:
        for n, (ncs, ngg, uid, u) in enumerate(picks):
            box, chip_on, vis = open_box(p, uid, u)
            m = p.ev(MEASURE_JS, box) if vis else None
            p.ev("(s)=>{const b=document.querySelector(s);if(b)b.scrollIntoView({block:'center'})}", box)
            p.shot('ggref_%s_%s_%d' % (v, dev['name'], n + 1))
            sw = p.ev(SWEEP_JS, box) if vis else ['상자 안 펴짐']
            pr = press_test(p, box, dev) if vis else (False, [])
            res.append({'문항': uid, '연결': u, '댓글': ncs, '칩 누름 자리': chip_on, '펴짐': vis, '잼': m, '훑기': sw, '누름': pr})
            p.ev("(o)=>{try{oxWinClose('q-'+o)}catch(e){}const w=document.getElementById('oxwin-q-'+o);if(w)w.remove()}", uid)
            p.wait(300)
        errs = p.errors()[:3]
    finally:
        p.close()
    return res, errs


def main():
    os.makedirs(TMPD, exist_ok=True)
    R('R0', '판 · 자리', None, None, {'NEW': NEWF, 'md5(LF)': {k: OL.md5lf(v) for k, v in SRC.items()}, 'BASE': BASE, 'SPD': OL.CONF['spd'], 'tw': OL.CONF['tw']})
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        p = OL.Live(br, 'NEW', SRC['NEW'], OL.PC)
        picks = p.ev(PICK_JS)
        p.close()
        R('R0', '표본(연결한 근거가 있는 문항 셋 · 댓글 많은 차례)', None, None, [{'문항': x[2], '연결': x[3], '근거 항목': x[1], '댓글': x[0]} for x in picks])
        out = {}
        for dev in ((OL.PH,) if QC.SMOKE else (OL.PH, OL.PC)):
            t1 = time.time()
            for v in VERS:
                try:
                    out[(v, dev['name'])] = run(br, v, dev, picks)
                except Exception as e:
                    out[(v, dev['name'])] = ([], ['하네스 오류: ' + str(e)[:300], traceback.format_exc()[-400:]])
            STEP[dev['name']] = round((time.time() - t1) / 60, 1)
        br.close()

    def rows(v, d):
        return [(x['문항'], r) for x in out[(v, d)][0] for r in ((x['잼'] or {}).get('rows') or [])]

    def r1(v):
        rs = rows(v, '폰')
        res = out[(v, '폰')][0]
        bad = [(q, r['kind'], r['ratio'], r['hit'], r['inter'], r['atRight']) for q, r in rs if not (r['ratio'] >= 0.9 and min(r['hit']) >= 36 and not r['inter'] and r['atRight'])]
        over = [(x['문항'], x['잼']['over']) for x in res if x['잼'] and x['잼']['over']]
        ok = bool(rs) and len(res) == 3 and all(x['펴짐'] and x['칩 누름 자리'] for x in res) and not bad and not over and not out[(v, '폰')][1]
        d = {'줄': len(rs), '글 폭 / 줄 폭(최소)': min((r['ratio'] for _, r in rs), default=None), '누를 자리 폭 · 높이(최소)': [min((r['hit'][0] for _, r in rs), default=None), min((r['hit'][1] for _, r in rs), default=None)],
             '단추 네모(본문 첫 줄)': rs[0][1]['btn'] if rs else None, '줄 폭': sorted({r['W'] for _, r in rs}), '어긋난 줄': bad[:6], '가려진 누를 것': over[:4], '오류': out[(v, '폰')][1]}
        return ok, d

    def r2(v):
        rs = rows(v, 'PC')
        res = out[(v, 'PC')][0]
        bad = [(q, r['kind'], r['sameLine'], r['atRight'], r['inter']) for q, r in rs if not (r['sameLine'] and r['atRight'] and not r['inter'])]
        over = [(x['문항'], x['잼']['over']) for x in res if x['잼'] and x['잼']['over']]
        ok = bool(rs) and len(res) == 3 and all(x['펴짐'] for x in res) and not bad and not over and not out[(v, 'PC')][1]
        d = {'줄': len(rs), '한 줄': sum(1 for _, r in rs if r['sameLine']), '글 폭 / 줄 폭(최소)': min((r['ratio'] for _, r in rs), default=None),
             '누를 자리 폭 · 높이(INFO · 마우스)': [min((r['hit'][0] for _, r in rs), default=None), min((r['hit'][1] for _, r in rs), default=None)], '어긋난 줄': bad[:6], '가려진 누를 것': over[:4], '오류': out[(v, 'PC')][1]}
        return ok, d

    def r3(v):
        dd, ok = {}, True
        for dn in ('폰', 'PC'):
            res = out[(v, dn)][0]
            dd[dn] = [{'문항': x['문항'], '누름': x['누름'][1]} for x in res]
            ok = ok and bool(res) and all(x['누름'][0] for x in res)
        return ok, dd

    def r4(v):
        dd, ok = {}, True
        for dn in ('폰', 'PC'):
            res = out[(v, dn)][0]
            dd[dn] = {'훑기': [(x['문항'], x['훑기']) for x in res if x['훑기']], '오류': out[(v, dn)][1]}
            ok = ok and bool(res) and not dd[dn]['훑기'] and not dd[dn]['오류']
        return ok, dd

    for gid, name, fn, yard in (('R1', '폰 연결한 근거 펼침 — 글 폭 ≥ 줄 폭 90 % · 「✎ 여기서 고치기」 누를 자리 ≥ 36 · 겹침 0 · 단추 줄 오른끝', r1, True),
                                ('R2', 'PC 연결한 근거 펼침 — 넓으면 한 줄 · 단추 줄 오른끝 · 겹침 0', r2, False),
                                ('R3', '누름 = 고치기 칸 열림(본문 · 댓글 · 글 = 저장된 글 · 취소 = 닫힘 · 폰 넓힌 누를 자리)', r3, True),
                                ('R4', '화면 훑기 — 연결 상자 넘침 · 상자 밖 · 화면 밖 0 · 오류 0(폰 · PC)', r4, False)):
        if not want(gid):
            continue
        a = fn('NEW')
        b = fn('BASE') if GATE else (None, '바탕 안 띄움(regress · smoke)')
        R(gid, name, a[0], b[0], {'NEW': a[1], 'BASE': b[1]}, yard=yard)
    nf = [r for r in RES if r['new'] is False]
    yard = [r for r in RES if r['yard'] and r['base'] is not None and r['new'] is not None]
    R('합계', '합계', None, None, {'PASS': sum(1 for r in RES if r['new'] is True), 'FAIL': len(nf), 'FAIL 칸': [r['g'] + ' ' + r['name'][:24] for r in nf],
                                  '헛잣대(바탕 FAIL)': '%d/%d' % (sum(1 for r in yard if r['base'] is False), len(yard)), '단계(분)': STEP, '전체(분)': round((time.time() - T0) / 60, 1)})
    try:
        with open(OUTF, 'w', encoding='utf-8') as f:
            for r in RES:
                f.write(json.dumps(r, ensure_ascii=False, default=str) + '\n')
    except Exception:
        pass
    sys.exit(1 if nf else 0)


if __name__ == '__main__':
    main()
