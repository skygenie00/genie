# -*- coding: utf-8 -*-
r"""연결한 근거 줄 폰 꼴 관문(자과 · 2026-10-10 jagwa_batch ②) — `.ggrr` 본문 줄 · `.ggrc2 .ggrcl` 댓글 줄

  python _harness_jagwa_ggrr_phone.py [--new <앱>] [--base <git 판 | 파일>] [--only r1,r2,...] [--res <결과>] [--vendor <cdnjs 사본>] [--mode gate|regress|smoke]

  근거 = 사용자 10/6 02:32 「글이 왼쪽 반만 · 오른쪽 가운데 단추」 → 10/6 시안 v1 꼴(글 덩어리 18rem 이상 + 단추 ml-auto · flex-wrap) · 결정로그 10/10 00:36 [채팅] · 00:52 [채팅]
  잣대(민법 ggRefRowHTML 과 같음) — 폰 390 · PC 1100 「연결한 근거」 펼침:
    r1 글 폭(글 덩어리 = 줄 안 ✎ 단추 밖 자식들의 합친 상자) ≥ 줄 폭 90 %(폰 · 본문 줄 · 댓글 줄 전부)
    r2 ✎ 단추 누를 자리(가운데에서 elementFromPoint 로 위 · 아래 · 왼 · 오른 이어지는 데까지) ≥ 36(폰 = 손가락 기기 · PC 는 잰 값만 적음 — 마우스)
    r3 겹침 0 — ✎ 단추 상자 ∩ 글 덩어리 상자 · 상자 안 누를 것끼리
    r4 ✎ 누름(폰 = CDP 진짜 톡 · PC = 마우스) = 그 줄 고치기 칸 열림(지금과 같은 동작 — 바탕 = 기준)
    r5 PC 넓으면 한 줄(단추가 글 덩어리 오른쪽 같은 줄 — 바탕 = 기준) · r6 화면 훑기(상자) 넘침 · 잘림 · 겹침 새로 생김 0
  자리 = 지학(카드 · 실데이터 연결 G25-62-08 → G08-45-07 · 댓글 있는 근거) · 물리(문항 창 머리 근거 줄 · 연결을 메모리에 심음 — 물리 기록에 연결 0)
  ⚠ 지학 · 생물 카드 = #card 760px 고정 판을 배율로 줄여 보임(앱 1116 줄 · 폰 첫 열기 배율 0.45) → 그 안 연결 상자는 늘 넓은 꼴(한 줄)이라 폰 반 폭 결함 자리가 아님:
    카드 층은 r1 대신 r5(한 줄 · 바탕 = 기준) · r2 = 판 px(화면 px ÷ 배율 · 화면 px 도 적음) — 폰 반 폭 결함 자리 = 물리 문항 창 머리(배율 1)
  헛잣대 = 바탕 7299ec3(_roots.base_rev()) — 폰 글 폭 ≈ 반 · 단추 누를 자리 ≈ 16 → FAIL
  ⚠ 자과앱 픽셀 게이트 없음(CLAUDE.md) — getBoundingClientRect · elementFromPoint · 실제 누름
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기(Pg_PP · PHONE)
import io, json, os, sys, tempfile, time   # noqa: E402
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = _roots.genie()
NEWF = ARG('--new', os.path.join(GENIE, 'jagwa', 'index.html'))
BASEARG = ARG('--base', None)
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_ggrr_phone_result.txt'))
VENDOR = ARG('--vendor', os.path.join(tempfile.gettempdir(), 'h_jgbatch', 'vendor'))
JG.conf(VENDOR_PP=VENDOR)
PCDEV = (1100, 800)
ROWS = []
from playwright.sync_api import sync_playwright   # noqa: E402

GJS = r"""
window.__G={
 R(e){const r=e.getBoundingClientRect();return {l:r.left,t:r.top,r:r.right,b:r.bottom,w:r.width,h:r.height}},
 U(L){if(!L.length)return null;const a=L.map(__G.R);const l=Math.min(...a.map(x=>x.l)),t=Math.min(...a.map(x=>x.t)),r=Math.max(...a.map(x=>x.r)),b=Math.max(...a.map(x=>x.b));return {l,t,r,b,w:r-l,h:b-t}},
 X(p,q){if(!p||!q)return 0;const ix=Math.min(p.r,q.r)-Math.max(p.l,q.l),iy=Math.min(p.b,q.b)-Math.max(p.t,q.t);return ix>0.5&&iy>0.5?Math.round(ix*iy):0},
 hit(e){const r=e.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2;const on=(x,y)=>{const a=document.elementFromPoint(x,y);return !!a&&(a===e||e.contains(a))};
   if(!on(cx,cy))return {h:0,w:0,on:false,top:(document.elementFromPoint(cx,cy)||{}).className||null};let u=0,d=0,l=0,rt=0;
   while(u<80&&on(cx,cy-u-1))u++;while(d<80&&on(cx,cy+d+1))d++;while(l<200&&on(cx-l-1,cy))l++;while(rt<200&&on(cx+rt+1,cy))rt++;return {h:u+d+1,w:l+rt+1,on:true}},
 /* 연결한 근거 상자 하나를 잰다 — 줄마다 글 덩어리(✎ 밖 자식 합) · 줄 폭 · 단추 상자 · 누를 자리 · 겹침 */
 /* 카드 층(지학 · 생물) = #card 760px 고정 판을 배율로 줄여 보임(앱 1116 줄) → 그 안 자리는 판 단위(화면 px ÷ 배율)로도 적는다 */
 scale(e){const c=e&&e.closest?e.closest('#card'):null;if(!c||!c.offsetWidth)return 1;return Math.round(c.getBoundingClientRect().width/c.offsetWidth*1000)/1000},
 measure(id){const b=document.getElementById(id);if(!b||b.classList.contains('hide'))return {box:false};const SC=__G.scale(b);
   const rows=[...b.querySelectorAll('.ggrr'),...b.querySelectorAll('.ggrc2 .ggrcl')];const out=[];
   rows.forEach(row=>{const kids=[...row.children].filter(c=>!c.matches('.lk')&&c.getClientRects().length);const btn=row.querySelector(':scope>.lk');
     try{(btn||row).scrollIntoView({block:'center'})}catch(e){}
     const rr=__G.R(row),tb=__G.U(kids),br=btn?__G.R(btn):null;
     out.push({kind:row.classList.contains('ggrr')?'본문':'댓글',row:Math.round(rr.w*10)/10,text:tb?Math.round(tb.w*10)/10:0,ratio:tb?Math.round(tb.w/rr.w*1000)/1000:0,
       btn:br?{w:Math.round(br.w*10)/10,h:Math.round(br.h*10)/10}:null,hit:btn?__G.hit(btn):null,ov:btn?__G.X(br,tb):0,
       oneLine:br&&tb?(br.t<tb.b-1&&br.l>=tb.r-1):null,kk:btn?(btn.getAttribute('data-ggre')||btn.getAttribute('data-ggrce')):null})});
   const act=[...b.querySelectorAll('button,[data-ggbang]')].filter(e=>e.getClientRects().length);const pairs=[];
   for(let i=0;i<act.length;i++)for(let j=i+1;j<act.length;j++){if(act[i].contains(act[j])||act[j].contains(act[i]))continue;const v=__G.X(__G.R(act[i]),__G.R(act[j]));if(v>4)pairs.push([act[i].textContent.trim().slice(0,8),act[j].textContent.trim().slice(0,8),v])}
   return {box:true,rows:out,pairs:pairs,coarse:matchMedia('(pointer:coarse)').matches,scale:SC,cardW:(b.closest('#card')||{}).offsetWidth||null}},
 btnAt(id,i){const b=document.getElementById(id);const btn=b?b.querySelectorAll('.ggrr>.lk')[i]:null;if(!btn)return null;btn.scrollIntoView({block:'center'});const r=btn.getBoundingClientRect();
   return {x:r.left+r.width/2,y:r.top+r.height/2,kk:btn.getAttribute('data-ggre')}},
 edOpen(kk){const e=document.querySelector('[data-ggre-box="'+CSS.escape(kk)+'"]');return e?!e.classList.contains('hide'):null},
 errs(){return (window.__err||[]).slice(0,6)}
};
"""

# 자리 열기 — 지학 = 실데이터 연결(댓글 달린 근거로 가는 연결 먼저) · 물리 = 연결 하나를 메모리에 심음(GGREF · 저장 안 부름)
OPEN = {
    'earth': r"""async ()=>{
  const C=Object.keys(GGREF).flatMap(a=>(GGREF[a]||[]).map(u=>[a,u])).filter(([a,u])=>rowByUid(a)&&rowByUid(u)&&ggOf(u).length);
  C.sort((p,q)=>{const s=x=>ggOf(x[1]).some(g=>g&&Array.isArray(g.cs)&&g.cs.some(c=>c&&c.k))?0:1;return s(p)-s(q)});
  if(!C.length)return {err:'연결 없음'};const [a,u]=C[0];
  await openView(rowByUid(a)[F.NO]);return {a,u,sc:'qp-'}}""",
    'phys': r"""async ()=>{
  const W=DATA.filter(r=>ggOf(GGU(r)).length);if(W.length<2)return {err:'근거 문항 < 2'};
  const u=GGU((W.find(r=>ggOf(GGU(r)).some(g=>g&&Array.isArray(g.cs)&&g.cs.some(c=>c&&c.k)))||W[0]));
  const ar=DATA.find(r=>GGU(r)!==u&&!ggOf(GGU(r)).length);const a=GGU(ar);GGREF[a]=[u];
  await openView(ar[F.NO]);return {a,u,sc:'qp-',seeded:true}}""",
}
SHOW = r"""async ([a,u,sc])=>{const sl=ms=>new Promise(r=>setTimeout(r,ms));
  const v=document.getElementById('view');if(v&&v.classList.contains('g3off')){const f=document.getElementById('g3Fold');if(f)f.click();await sl(300)}
  const id=sc+'gg-refbox-'+a+'-'+u;let b=document.getElementById(id);
  if(b&&b.classList.contains('hide')){const ch=document.querySelector('[data-ggrt="'+CSS.escape(a+'|'+u+'|'+sc)+'"]');if(ch){ch.scrollIntoView({block:'center'});ch.click()}await sl(300)}
  b=document.getElementById(id);return {id,shown:!!b&&!b.classList.contains('hide'),how:b?'chip':'없음'}}"""


def R(g, dv, name, okn, okb, val):
    ROWS.append((g, dv, name, okn, okb, val))
    print('%s | 바탕 %s | %s · %s · %s | %s' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, dv, name,
          (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str))[:700]), flush=True)


APPS = {}


def one(br, who, subj, dev, touch):
    """한 판 · 한 과목 · 한 기기 → 잰 값"""
    QC.launch('new' if who == 'NEW' else 'base')
    p = JG.Pg_PP(br, 'chromium', 'gr_%s_%s_%dx%d' % (who, subj, dev[0], dev[1]), APPS[who], subj, dev, touch=touch, remote=JG.Remote())   # 문맥마다 새 가짜 원격
    try:
        p.ev(GJS)
        QC.until(p.pg, "s=>(typeof CARD_LAYER==='undefined'||!CARD_LAYER||(typeof DATA_V!=='undefined'&&DATA_V>0))&&(typeof GG_READY==='undefined'||GG_READY)&&(s!=='earth'||Object.keys(GGREF||{}).length>0)", 60000, '과목 문항(DATA_V) · 근거 · 연결 기록 읽힘(GG_READY · GGREF)', arg=subj)
        o = p.ev(OPEN[subj])
        if o.get('err'):
            return {'err': o['err']}
        QC.sleep(1500, '문항 창 열림 뒤 근거 줄 그림(openView 뒤 표지 없음)', p.pg)
        s = p.ev(SHOW, [o['a'], o['u'], o['sc']])
        if not s['shown']:
            return {'err': '연결 상자 못 폄', 'o': o, 's': s}
        m = p.ev("id=>__G.measure(id)", s['id'])
        # r6 훑기 — 상자 하나
        p.pg.evaluate(JG.TOOLS)
        sw = p.ev("([s,t])=>__H.sweep(s,t)", ['#' + s['id'], touch])
        # r4 ✎ 누름 — 첫 본문 줄
        bt = p.ev("([id,i])=>__G.btnAt(id,i)", [s['id'], 0])
        opened = None
        if bt:
            if touch:
                p.tap(bt['x'], bt['y'], wait=500)
            else:
                p.click(bt['x'], bt['y'], wait=500)
            opened = p.ev("kk=>__G.edOpen(kk)", bt['kk'])
        return {'open': o, 'm': m, 'sweep': sw, 'tap': opened, 'errs': p.ev("()=>__G.errs()") + p.errs[:3]}
    finally:
        p.close()


def judge(dname, v, phone):
    """잰 값 → 관문 넷(r1 · r2 · r3 · r5) 판정"""
    if not v or v.get('err') or not v['m'].get('box'):
        return {'r1': (False, v), 'r2': (False, v), 'r3': (False, v), 'r4': (False, v), 'r5': (False, v)}
    rows = v['m']['rows']
    SC = v['m'].get('scale') or 1
    card = SC < 0.99 or bool(v['m'].get('cardW'))   # 카드 층 = 760px 고정 판(늘 넓은 꼴) — 폰 반 폭 자리가 아님 → r1 대신 r5(한 줄) · r2 = 판 단위
    nb = [r for r in rows if r['kind'] == '본문']
    nc = [r for r in rows if r['kind'] == '댓글']
    lowr = [r for r in rows if r['ratio'] < 0.9]
    small = [r for r in rows if r['hit'] and (r['hit']['h'] / SC < 35.5 or r['hit']['w'] / SC < 35.5)]
    ovl = [r for r in rows if r['ov']]
    out = {}
    out['r1'] = (bool(nb) and not lowr if (phone and not card) else None, {'카드 판(760 고정 · 배율)': [card, SC, v['m'].get('cardW')], '본문 줄': len(nb), '댓글 줄': len(nc), '비 최소': min([r['ratio'] for r in rows] or [0]),
                                                         '90% 밑': [(r['kind'], r['ratio'], r['row'], r['text']) for r in lowr][:6]})
    out['r2'] = (bool(rows) and not small if phone else None, {'배율': SC, '누를 자리(높이×폭 · 화면 px)': [(r['kind'], r['hit']['h'] if r['hit'] else None, r['hit']['w'] if r['hit'] else None) for r in rows][:8],
                                                           '누를 자리(판 px = 화면 ÷ 배율)': [(r['kind'], round(r['hit']['h'] / SC, 1) if r['hit'] else None, round(r['hit']['w'] / SC, 1) if r['hit'] else None) for r in rows][:8],
                                                           '단추 상자': [r['btn'] for r in rows][:3], '손가락 기기': v['m']['coarse']})
    out['r3'] = (bool(rows) and not ovl and not v['m']['pairs'], {'단추∩글': [(r['kind'], r['ov']) for r in ovl][:6], '누를 것끼리': v['m']['pairs'][:6]})
    out['r4'] = (v['tap'] is True, {'✎ 누름 → 고치기 칸 열림': v['tap']})
    out['r5'] = (all(r['oneLine'] for r in rows if r['btn']) if (not phone or card) else None, {'한 줄': [(r['kind'], r['oneLine'], r['row']) for r in rows][:8]})
    if v.get('errs'):
        out['r1'] = (False, {'값': out['r1'][1], '페이지 오류': v['errs']})
    return out


def main():
    APPS['NEW'] = open(NEWF, 'rb').read().replace(b'\r\n', b'\n').decode('utf-8')
    base_rev = BASEARG or _roots.base_rev()
    if QC.GATE:
        if BASEARG and os.path.isfile(BASEARG):
            APPS['BASE'] = open(BASEARG, 'rb').read().replace(b'\r\n', b'\n').decode('utf-8')
        else:
            QC.sub('git:show-app')
            APPS['BASE'] = JG.app_src(base_rev)
    t0 = time.time()
    NAMES = {'r1': '글 폭 ≥ 줄 폭 90 %(폰 · 본문 · 댓글 줄)', 'r2': '✎ 누를 자리 ≥ 36(손가락 기기)', 'r3': '겹침 0(단추∩글 · 누를 것끼리)',
             'r4': '✎ 누름 = 고치기 칸 열림(지금과 같음 · 바탕 = 기준)', 'r5': 'PC 넓으면 한 줄(바탕 = 기준)'}
    plan = [('earth', '폰390', JG.PHONE, True), ('earth', 'PC1100', PCDEV, False), ('phys', '폰390', JG.PHONE, True), ('phys', 'PC1100', PCDEV, False)]
    if QC.SMOKE:
        plan = plan[:1]
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        try:
            for subj, dname, dev, touch in plan:
                with QC.stage('%s %s' % (subj, dname)):
                    vals = {}
                    for who in (('NEW', 'BASE') if QC.GATE else ('NEW',)):
                        try:
                            vals[who] = one(br, who, subj, dev, touch)
                        except Exception as e:
                            vals[who] = {'err': 'ERR ' + repr(e)[:300]}
                    jn = judge(dname, vals['NEW'], touch)
                    jb = judge(dname, vals.get('BASE'), touch) if QC.GATE else {}
                    tag = 'chromium·%s·%s' % (dname, subj)
                    for g in ('r1', 'r2', 'r3', 'r4', 'r5'):
                        if ONLY and g not in ONLY:
                            continue
                        okn, vn = jn[g]
                        if okn is None:
                            continue
                        okb = jb[g][0] if QC.GATE else None
                        if QC.REGRESS and g in ('r4', 'r5'):
                            okb = None
                        R(g, tag, NAMES[g], okn, okb, {'NEW': vn, 'BASE': jb[g][1] if QC.GATE else None})
                    if not ONLY or 'r6' in ONLY:
                        swn = [x for x in (vals['NEW'].get('sweep') or [])]
                        swb = set(vals.get('BASE', {}).get('sweep') or []) if QC.GATE else set(QC.base('r6.%s' % tag, swn))
                        newi = [x for x in swn if x not in swb]
                        R('r6', tag, '화면 훑기(연결 상자) — 넘침 · 잘림 · 겹침 · 작은 누름 새로 생김 0(바탕에 있던 것 빼고)', not newi, None,
                          {'새로 생김': newi, 'NEW': swn[:10], '바탕': sorted(swb)[:10], '바탕에서 없어짐': sorted(set(swb) - set(swn))[:10]})
        finally:
            br.close()
    npass = sum(1 for r in ROWS if r[3]); nfail = sum(1 for r in ROWS if not r[3])
    vac = [r for r in ROWS if r[4] is True and r[0] in ('r1', 'r2')]   # 바뀜 잣대(r1 · r2)만 — r3 · r4 · r5 = 바탕 = 기준(지금과 같음)
    print('\n== PASS %d · FAIL %d · 헛잣대(바탕도 PASS · 바뀜 잣대 r1 · r2) %d · %.0f초' % (npass, nfail, len(vac), time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · jagwa_ggrr_phone · NEW %s · 바탕 %s · 모드 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), os.path.basename(NEWF), base_rev if QC.GATE else '(regress)', QC.MODE))
        for g, dv, n, okn, okb, v in ROWS:
            f.write('%s | 바탕 %s | %s · %s · %s | %s\n' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, dv, n,
                    (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str))[:2500]))
        f.write('== PASS %d · FAIL %d · 헛잣대 %d\n' % (npass, nfail, len(vac)))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
