# -*- coding: utf-8 -*-
r"""_task_search_all §B 관문 — 자과 몫(검색 결과를 자르지 않고 다 보이기 · 2026-10-10 jagwa_batch)

  python _harness_jagwa_search_all.py [--new <앱>] [--base <git 판 | 파일>] [--eng chromium,webkit] [--only s1,s2,...] [--res <결과>] [--vendor <cdnjs 사본>] [--mode gate|regress|smoke]

  NEW = genie(GENIE_ROOT) 작업트리 jagwa/index.html · BASE(헛잣대) = _roots.base_rev()(워크트리 = 분기점 · 판 7299ec3) 의 jagwa/index.html
  데이터 · 기록 = studyplandata(SPD_ROOT) 를 가짜 원격으로(JG.Pg_PP · PUT 은 가로채 밖으로 안 나감) · cdnjs = --vendor 사본(없는 글꼴만 진짜 cdnjs)
  자리(지시서 §0-3 + 착수 grep 더함) — es = 위 검색 칸 esSearch(생물 · 물리) · lk = 연결 시트 linkSheet(지학) · gf = 근거 찾기 ggFindRun(지학 · 실데이터 '' + 심은 근거 160) ·
        ns = 서랍 머리 검색 nsPop(물리 · 착수 grep 으로 더한 자리 · 옛 80 + 「… N건 더」)
  관문(§B): s1 셈 글 = 끝까지 굴려 붙은 줄 수 = 하네스가 같은 식으로 거른 수 · 차례 = 거른 차례 · 끝 표지 · 「상위 N건」 글 0 · 마지막 줄 누름 = 그 문항(그 일)
            s2 검색어 바꾸기(굴리는 중) = 옛 줄 0 · 새 첫 100 줄 · 끝까지 = 새 수   s3 첫 그림 빠르기(입력 → 첫 100 줄 · 세 번 가운데) ≤ 바탕 × 1.2
            s4 화면 훑기(결과 상자 · PC · 폰) 넘침 · 잘림 0(바탕에 있던 것 빼고)       s5 WebKit 폰 굴림(굴림 칸만)
  굴림 = 진짜 굴림 — PC 마우스 휠(page.mouse.wheel) · 폰 Chromium CDP Input.dispatchTouchEvent 손가락 끌기 · WebKit 휠
  ⚠ 자과앱 픽셀 게이트 없음(CLAUDE.md) — DOM 글자 · 개수 · 자리 · 실제 누름
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기(Pg_PP · route_handler · PHONE)
import io, json, os, re, sys, tempfile, time, statistics   # noqa: E402
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = _roots.genie()
NEWF = ARG('--new', os.path.join(GENIE, 'jagwa', 'index.html'))
BASEARG = ARG('--base', None)
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_search_all_result.txt'))
VENDOR = ARG('--vendor', os.path.join(tempfile.gettempdir(), 'h_jgbatch', 'vendor'))
JG.conf(VENDOR_PP=VENDOR)
PCDEV = (1100, 800)
ROWS = []   # (관문, 엔진·기기, 이름, NEW ok, BASE ok, 잰 값)
from playwright.sync_api import sync_playwright   # noqa: E402

# ── 쪽 안 도구 __R — 자리마다 상자 · 줄 · 셈 글 · 거른 수(앱과 같은 식) ──
RJS = r"""
window.__R={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 P:{es:{box:'#esres',row:'[data-esq]',id:e=>+e.getAttribute('data-esq'),cnt:'#qCnt'},
    lk:{box:'#lkres',row:'.lkhit',id:e=>+e.getAttribute('data-add'),cnt:'#lkres .rpcnt'},
    gf:{box:'.ggfind:not(.hide) .res',row:'[data-ggpick]',id:e=>String(e.getAttribute('data-ggpick')).split('|')[1],cnt:'.ggfind:not(.hide) .res .rpcnt'},
    ns:{box:'#nsPop .nsl',row:'.nsr',id:e=>+e.getAttribute('data-no'),cnt:'#nsPop .nsc'}},
 scroller(b){let s=b;while(s&&s!==document.body&&s!==document.documentElement){const o=getComputedStyle(s).overflowY;if((o==='auto'||o==='scroll'))return s;s=s.parentElement}return document.scrollingElement},
 /* 굴리는 상자의 보이는 자리 = 제 상자 ∩ 조상 가운데 넘침을 자르는 것(overflow ≠ visible) ∩ 화면 — 굴림 손짓은 그 가운데에 놓는다(연결 시트 = #lkres 320 · 판 266 이 잘라 보임) */
 clip(e){const r=e.getBoundingClientRect();let v={l:r.left,t:r.top,r:r.right,b:r.bottom};for(let a=e.parentElement;a&&a!==document.documentElement;a=a.parentElement){const c=getComputedStyle(a);
   if(c.overflowY!=='visible'||c.overflowX!=='visible'){const q=a.getBoundingClientRect();v={l:Math.max(v.l,q.left),t:Math.max(v.t,q.top),r:Math.min(v.r,q.right),b:Math.min(v.b,q.bottom)}}}
   return {l:Math.max(0,v.l),t:Math.max(0,v.t),r:Math.min(innerWidth,v.r),b:Math.min(innerHeight,v.b)}},
 st(k){const p=__R.P[k],b=document.querySelector(p.box);if(!b)return {box:false};
   const rows=[...b.querySelectorAll(p.row)],sc=__R.scroller(b);
   const vr=__R.clip(sc);
   return {box:true,n:rows.length,ids:rows.map(p.id),sent:b.querySelectorAll('.rpmore').length,cnt:__R.tx(document.querySelector(p.cnt)),
     tail:[...b.querySelectorAll('.bplnone,.rl0')].map(__R.tx),txt:__R.tx(b).slice(-80),
     sc:{top:sc.scrollTop,h:sc.clientHeight,sh:sc.scrollHeight,cx:(vr.l+vr.r)/2,cy:(vr.t+vr.b)/2,w:vr.r-vr.l,vh:vr.b-vr.t}}},
 /* 거른 수 = 앱과 같은 식(관문 §B-1) — es: esHit/esPhysHit(앱 그대로 · 데이터 차례) · lk: 시트 식을 글자 그대로 옮김 · gf: ggHits − 그 문항 · ns: esPhysHit ∪ ggHits(근거·댓글·Claude) 번호 차례 */
 want(k,q,me){
   if(k==='es')return DATA.filter(r=>HASBOOK?!!esHit(r,q):esPhysHit(r,q)).map(r=>r[F.NO]);
   if(k==='lk'){const q0=String(q).trim(),ql=q0.toLowerCase();return DATA.filter(r=>r[F.NO]!==me&&(String(r[F.CODE]).toLowerCase().includes(ql)||r[F.SUB].includes(q0)||String(r[F.BODY]).includes(q0)||String(r[F.NO])===ql)).map(r=>r[F.NO])}
   if(k==='gf')return ggHits(q).filter(h=>h.uid!==me).map(h=>h.uid);
   if(k==='ns'){const s=new Set(DATA.filter(r=>esPhysHit(r,q)).map(r=>r[F.NO]));try{ggHits(q,true).forEach(h=>{const x=h.src||{};if(x.gg||x.cm||x.cl)s.add(h.no)})}catch(e){}return [...s].sort((a,z)=>a-z)}
   return []},
 pick(k,cands,lo,me){let best=null;for(const q of cands){const n=__R.want(k,q,me).length;if(n>lo)return {q,n};if(!best||n>best.n)best={q,n}}return best},
 lastRect(k){const p=__R.P[k],b=document.querySelector(p.box);const rows=b?[...b.querySelectorAll(p.row)]:[];const e=rows[rows.length-1];if(!e)return null;
   e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect();const y=r.top+Math.min(r.height/2,10);
   let cx=r.left+Math.min(r.width/2,60);const t=k==='ns'?e.querySelector('.nst'):(k==='lk'?e.querySelector('small'):null);
   if(t){const q=t.getBoundingClientRect();cx=q.left+q.width/2;return {x:cx,y:q.top+q.height/2,id:p.id(e)}}
   return {x:cx,y:y,id:p.id(e),top:(document.elementFromPoint(cx,y)||{}).className}},
 seedGG(n,me){const out=[];const T=Date.now();for(const r of DATA){if(out.length>=n)break;if(isC(r))continue;const u=GGU(r);if(u===me||ggOf(u).length)continue;
   GG[u]=[{k:'g_hsall'+out.length,i:1,t:'하네스찾기말 '+out.length+' 근거',ok:null,ts:T,cs:[]}];out.push(u)}return out.length},
 errs(){return (window.__err||[]).slice(0,6)}
};
"""

READY_JS = "()=>(typeof CARD_LAYER==='undefined'||!CARD_LAYER||(typeof DATA_V!=='undefined'&&DATA_V>0))&&(typeof GG_READY==='undefined'||!!GG_READY)"
P_BOX = {'es': '#esres', 'lk': '#lkres', 'gf': '.ggfind:not(.hide) .res', 'ns': '#nsPop .nsl'}

TIMEJS = r"""async ([q,reps])=>{const inp=document.getElementById('q'),box=document.getElementById('esres');const ts=[];
  for(let k=0;k<reps;k++){inp.value='';esSearch();await new Promise(r=>setTimeout(r,30));
    const a=performance.now();inp.value=q;esSearch();void box.offsetHeight;box.querySelectorAll('[data-esq]').length;ts.push(performance.now()-a)}
  inp.value='';esSearch();return ts}"""


def R(g, dv, name, okn, okb, val):
    ROWS.append((g, dv, name, okn, okb, val))
    print('%s | 바탕 %s | %s · %s · %s | %s' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, dv, name,
          (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str))[:600]), flush=True)


class Dev(object):
    """기기 하나(문맥) = JG.Pg_PP + __R + CDP 굴림"""

    def __init__(self, br, eng, who, src, subj, dev, touch):
        QC.launch('new' if who == 'NEW' else 'base')
        self.eng, self.who, self.touch = eng, who, touch
        self.p = JG.Pg_PP(br, eng, 'sa_%s_%s_%s_%dx%d' % (who, eng, subj, dev[0], dev[1]), src, subj, dev, touch=touch, remote=JG.Remote())   # 문맥마다 새 가짜 원격(앞 문맥 PUT 이 안 샘)
        self.pg = self.p.pg
        # 카드 층(생물 · 지학) DATA 는 처음에 물리 인라인 행 → 문항.json 을 읽어 buildData 가 갈아 끼움(DATA_V +1) · 근거 = GG_READY — 둘 다 선 뒤에 잰다
        QC.until(self.pg, READY_JS, 60000, '과목 문항(DATA_V) · 근거(GG_READY) 읽힘')
        self.ev(RJS)

    def ev(self, js, arg=None):
        return self.pg.evaluate(js, arg) if arg is not None else self.pg.evaluate(js)

    def wait(self, ms, why):
        QC.sleep(ms, why, self.pg)

    def type_into(self, sel, text):
        loc = self.pg.locator(sel).first
        loc.scroll_into_view_if_needed()
        loc.click()
        loc.fill('')
        if text:
            self.pg.keyboard.type(text, delay=4)

    def scroll_once(self, st):
        s = st['sc']
        d = max(120, int(s['vh'] * 0.9))
        if self.eng == 'chromium' and self.touch and not getattr(self, 'wheel_only', False):
            # 손가락 끌기 = CDP Input.dispatchTouchEvent(touchStart → touchMove 열둘 → touchEnd) — 진짜 터치 굴림(앱 터치 처리 · 브라우저 굴림 그대로)
            # (Input.synthesizeScrollGesture(touch) 는 이 떠 있는 판 안 상자를 못 굴렸다 — 10/10 잼 · 끌기는 굴림)
            c = self.p._cdp()
            x, y0, y1 = int(s['cx']), int(s['cy'] + d / 2), int(s['cy'] - d / 2)
            c.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y0, 'radiusX': 11, 'radiusY': 11, 'id': 1}]})
            for i in range(1, 13):
                c.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x, 'y': int(y0 + (y1 - y0) * i / 12), 'radiusX': 11, 'radiusY': 11, 'id': 1}]})
                self.pg.wait_for_timeout(16)
            c.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        else:
            self.pg.mouse.move(s['cx'], s['cy'])
            self.pg.mouse.wheel(0, d * 2)

    def scroll_end(self, k, want, cap=300):
        """진짜 굴림으로 끝까지 — 줄 수가 넷 번 연달아 안 늘고 끝 표지가 없거나 · 거른 수에 닿을 때까지"""
        last, same, steps, moved, stuck = -1, 0, 0, 0, 0
        self.ev("k=>{const b=document.querySelector(__R.P[k].box);if(b)b.scrollIntoView({block:'start'})}", k)   # 상자 머리를 보이게(판 굴림) — 사람도 먼저 판을 굴려 목록을 연다
        for steps in range(cap):
            st = self.ev("k=>__R.st(k)", k)
            if not st.get('box'):
                return st, steps, moved
            if st['n'] >= want and st['sent'] == 0:
                break
            same = same + 1 if st['n'] == last else 0
            if same >= 4 and st['sc']['top'] + st['sc']['h'] >= st['sc']['sh'] - 2:
                break
            last = st['n']
            t0 = st['sc']['top']
            self.scroll_once(st)
            ch = QC.until(self.pg, "([k,t0,n])=>{const s=__R.st(k);return s.sc.top!==t0||s.n!==n}", 1500, '굴림 뒤 자리 · 줄 수 바뀜', arg=[k, t0, st['n']])
            self.pg.wait_for_timeout(60)
            moved += 1
            stuck = 0 if ch else stuck + 1
            if stuck >= 4:   # 굴림이 안 먹음(자리 · 줄 수 그대로 넷 번) — 더 돌지 않는다(값에 남음)
                break
        return self.ev("k=>__R.st(k)", k), steps, moved

    def tap(self, x, y):
        if self.touch and self.eng == 'chromium':
            self.p.tap(x, y, wait=0)
        elif self.touch:
            self.pg.touchscreen.tap(x, y)
        else:
            self.pg.mouse.click(x, y)

    def close(self):
        self.p.close()


# ── 자리마다 띄우기 · 검색 ──
def open_place(dv, k, q=None, seed=0):
    """k 자리를 열고 q 로 찾는다 → me(그 자리의 「나」) · seed = 찾기 상자를 연 뒤 심을 근거 수(gf)"""
    me = None
    if k == 'es':
        dv.ev("()=>{document.body.classList.remove('fold')}")   # 폰 = 위 검색 줄 접힘이면 결과 상자 숨음(옛 search g14 와 같이 폄)
        dv.type_into('#q', q)
        QC.until(dv.pg, "q=>{const b=document.getElementById('esres');return !!b&&!b.classList.contains('hide')&&b.querySelectorAll('[data-esq]').length>0}", 8000, '검색 결과 줄', arg=q)
        dv.wait(300, '검색 칸 입력 모으기 뒤 다시 그림 끝(표지 없음)')
    elif k == 'lk':
        me = dv.ev("()=>DATA.find(r=>!isC(r))[F.NO]")
        dv.ev("n=>{linkSheet(n)}", me)
        QC.until(dv.pg, "()=>!!document.getElementById('lkq')", 8000, '연결 시트 검색 칸')
        dv.type_into('#lkq', q)
        QC.until(dv.pg, "()=>document.querySelectorAll('#lkres .lkhit').length>0", 8000, '연결 검색 줄')
    elif k == 'gf':
        me = dv.ev("()=>{const r=DATA.find(r=>!isC(r)&&ggOf(GGU(r)).length===0);return r?GGU(r):null}")
        no = dv.ev("u=>rowByUid(u)[F.NO]", me)
        dv.ev("n=>openView(n)", no)
        QC.until(dv.pg, "u=>!!document.querySelector('[data-ggfind=\"'+u+'|qp-\"]')", 15000, '근거 🔍 단추', arg=me)
        dv.ev("u=>{const b=document.querySelector('[data-ggfind=\"'+u+'|qp-\"]');b.scrollIntoView({block:'center'});b.click()}", me)
        QC.until(dv.pg, "()=>!!document.querySelector('.ggfind:not(.hide) .res')", 5000, '찾기 상자 열림')
        if seed:
            dv.seeded = dv.ev("([n,me])=>__R.seedGG(n,me)", [seed, me])   # 메모리에만(저장 안 부름) · 상자를 연 뒤 = 그 사이 기록 맞춤이 덮을 틈 없음
        if q:
            dv.type_into('.ggfind:not(.hide) input', q)
        dv.wait(400, '찾기 칸 120ms 모으기(ggFindSoon) 뒤 그림')
    elif k == 'ns':
        dv.ev("()=>{const a=document.getElementById('ndHead')||document.body;nsPop(a)}")
        QC.until(dv.pg, "()=>!!document.querySelector('#nsPop .rlq')", 5000, '서랍 검색 작은 창')
        dv.type_into('#nsPop .rlq', q)
        QC.until(dv.pg, "()=>document.querySelectorAll('#nsPop .nsr').length>0", 8000, '서랍 검색 줄')
    return me


def s1_place(dv, k, subj, cands, lo, do_sweep=False):
    """§B-1·2 — 셈 글 · 끝까지 굴린 줄 = 거른 수 · 차례 · 표지 · 꼬리 글 · 마지막 줄 누름"""
    out = {}
    seed = 160 if cands == ['__seed__'] else 0
    if seed:
        q = '하네스찾기말'
    elif cands == ['']:
        q = ''
    else:
        me0 = dv.ev("()=>DATA.find(r=>!isC(r))[F.NO]") if k == 'lk' else None
        q = dv.ev("([k,c,lo,me])=>__R.pick(k,c,lo,me)", [k, cands, lo, me0])['q']
    me = open_place(dv, k, q, seed)
    if seed:
        out['심은 근거'] = getattr(dv, 'seeded', None)
    if k == 'gf' and dv.touch and dv.eng == 'chromium':
        # 카드 층 = #cardwrap touch-action:none + inkGuard 가 손가락 끌기를 카드 굴림으로 가져감 → 카드 안 찾기 상자(.res 220px)는 손가락으로 안 굴러감(바탕 같음 · 이 판 밖) —
        # 한 번 끌어 보고 적은 뒤 상자 굴림은 휠로(resPage 이어 붙임을 잼)
        a = dv.ev("k=>__R.st(k)", k)
        dv.ev("k=>{const b=document.querySelector(__R.P[k].box);if(b)b.scrollIntoView({block:'start'})}", k)
        a = dv.ev("k=>__R.st(k)", k)
        dv.scroll_once(a)
        dv.pg.wait_for_timeout(500)
        b = dv.ev("k=>__R.st(k)", k)
        out['손가락 끌기 → 상자 굴림'] = [a['sc']['top'], b['sc']['top']]
        dv.wheel_only = True
    want = dv.ev("([k,q,me])=>__R.want(k,q,me)", [k, q, me])
    st0 = dv.ev("k=>__R.st(k)", k)
    st, steps, moved = dv.scroll_end(k, len(want))
    out.update({'말': q, '거른 수': len(want), '첫 줄 수': st0['n'], '셈 글': st['cnt'], '끝 줄 수': st['n'], '굴림': moved, '표지': st['sent'], '꼬리': st['tail'][-1:]})
    want_s = [str(x) for x in want]
    ids_s = [str(x) for x in st['ids']]
    cnt_ok = st['cnt'] == '%d건' % len(want)
    order_ok = ids_s == want_s
    tail_ok = not any(('상위' in t) or ('건 더' in t) for t in st['tail'])
    first_ok = st0['n'] == min(100, len(want))
    if do_sweep:
        dv.pg.evaluate(JG.TOOLS)
        out['_sweep'] = [x for x in dv.ev("([s,t])=>__H.sweep(s,t)", [P_BOX[k], dv.touch]) if not x.startswith('small:')]
    lr = dv.ev("k=>__R.lastRect(k)", k)
    clicked = None
    if lr:
        dv.tap(lr['x'], lr['y'])
        dv.wait(700, '마지막 줄 누름 뒤 앱 일(문항 열기 · 잇기)')
        if k in ('es', 'ns'):
            clicked = dv.ev("()=>typeof VNO!=='undefined'?VNO:null")
            click_ok = str(clicked) == str(lr['id'])
        elif k == 'lk':
            clicked = dv.ev("([me,x])=>linksOf(me).includes(+x)", [me, lr['id']])
            click_ok = bool(clicked)
        else:
            clicked = dv.ev("([me,x])=>ggRefOf(me).includes(x)", [me, lr['id']])
            click_ok = bool(clicked)
    else:
        click_ok = False
    out.update({'차례 같음': order_ok, '셈 글 맞음': cnt_ok, '첫 100': first_ok, '마지막 줄': lr and lr['id'], '누름 뒤': clicked})
    ok = len(want) > lo and cnt_ok and order_ok and st['n'] == len(want) and st['sent'] == 0 and tail_ok and click_ok and first_ok
    if len(want) <= lo:
        out['표본'] = '거른 수 %d ≤ 자르던 수 %d — 헛패스 막음(FAIL)' % (len(want), lo)
        ok = False
    return ok, out


def s2_switch(dv):
    """§B-4 — 긴 결과 굴리는 중 검색어 바꿈 → 옛 줄 0 · 새 첫 100 줄 · 끝까지 = 새 수"""
    pk = dv.ev("()=>{const c=['다음','것은','옳은','설명','에서','있다','이다'];const L=c.map(q=>({q,n:__R.want('es',q).length})).filter(x=>x.n>150).sort((a,b)=>b.n-a.n);return L}")
    if len(pk) < 2:
        return False, {'표본': pk}
    q1, q2 = pk[0]['q'], pk[1]['q']
    open_place(dv, 'es', q1)
    st = dv.ev("()=>__R.st('es')")
    n1 = pk[0]['n']
    for _ in range(60):   # 둘째 묶음(≥ 200 줄)이 붙을 때까지 진짜 굴림 — 「굴리는 중」
        if st['n'] >= 200 or st['n'] >= n1:
            break
        dv.scroll_once(st)
        dv.pg.wait_for_timeout(150)
        st = dv.ev("()=>__R.st('es')")
    mid = st['n']
    dv.type_into('#q', q2)
    QC.until(dv.pg, "q=>{const n=DATA.filter(r=>HASBOOK?!!esHit(r,q):esPhysHit(r,q)).map(r=>r[F.NO]);const b=document.getElementById('esres');const r=[...b.querySelectorAll('[data-esq]')].map(e=>+e.getAttribute('data-esq'));return r.length>0&&r[0]===n[0]}", 8000, '새 검색어 결과', arg=q2)
    dv.wait(400, '옛 관찰자가 남았으면 붙을 틈(굴림 뒤 · 표지 없음)')
    w2 = dv.ev("q=>__R.want('es',q)", q2)
    a = dv.ev("()=>__R.st('es')")
    first_ok = a['ids'] == w2[:min(100, len(w2))]
    st2, steps, moved = dv.scroll_end('es', len(w2))
    end_ok = st2['ids'] == w2 and st2['sent'] == 0
    return (mid > 100 and first_ok and end_ok), {'말1': [q1, pk[0]['n']], '굴린 뒤 줄': mid, '말2': [q2, len(w2)], '바꾼 직후 줄': a['n'], '바꾼 직후 = 새 첫 100': first_ok,
                                                 '끝까지': [st2['n'], moved], '끝 = 새 결과 그대로(옛 줄 0)': end_ok}


APPS = {}


def run_dev(br, eng, devname, dev, touch):
    """한 기기(엔진 · 화면)에서 자리 다섯 + 바꾸기 + 빠르기 + 훑기"""
    tag = '%s·%s' % (eng, devname)
    plan = [('es', 'bio', ['다음', '것은', '옳은', '설명', '에서', '있다'], 100, 's1', '생물 위 검색 칸'),
            ('es', 'phys', ['물체', '그림', '속력', '다음', '것은', '에서'], 100, 's1', '물리 위 검색 칸'),
            ('lk', 'earth', ['것은', '다음', '옳은', '대한', '에서'], 40, 's1', '지학 연결 시트 검색'),
            ('gf', 'earth', [''], 40, 's1', '지학 근거 찾기 — 실데이터 빈 말(근거 있는 문항 전부)'),
            ('gf', 'earth', ['__seed__'], 40, 's1', '지학 근거 찾기 — 심은 근거 160'),
            ('ns', 'phys', ['물체', '그림', '속력', '다음', '것은', '에서'], 80, 's1', '물리 서랍 머리 검색(착수 grep 더함)')]
    if QC.SMOKE:
        plan = plan[:1]
    if eng == 'webkit':
        plan = [p for p in plan if p[0] == 'es' and p[1] == 'bio']   # WebKit = 굴림 터치 칸만
    for k, subj, cands, lo, g, name in plan:
        gid = '%s-%s-%s' % (g, k, subj) + ('-seed' if cands == ['__seed__'] else ('-real' if cands == [''] else ''))
        if ONLY and gid not in ONLY and g not in ONLY:
            continue
        res = {}
        for who in (('NEW', 'BASE') if QC.GATE else ('NEW',)):
            dv = Dev(br, eng, who, APPS[who], subj, dev, touch)
            try:
                dosw = eng == 'chromium' and not QC.SMOKE and cands != ['__seed__']
                res[who] = s1_place(dv, k, subj, cands, lo, dosw)
                if isinstance(res[who][1], dict) and '_sweep' in res[who][1]:
                    res[who + '_sweep'] = res[who][1].pop('_sweep')
                errs = dv.ev("()=>__R.errs()") + dv.p.errs[:3]
                if errs and who == 'NEW':
                    res[who] = (False, {'값': res[who][1], '페이지 오류': errs})
            except Exception as e:
                res[who] = (False, 'ERR ' + repr(e)[:300])
            finally:
                dv.close()
        okn, vn = res['NEW']
        okb, vb = res.get('BASE', (None, None))
        R(gid, tag, name, okn, okb, {'NEW': vn, 'BASE': vb})
        if 'NEW_sweep' in res:
            nb = set(res.get('BASE_sweep') or []) if QC.GATE else set(QC.base('s4.%s@%s' % (gid, tag), res['NEW_sweep']))   # regress — 바탕 훑기 = 기준 스냅샷
            newi = [x for x in res['NEW_sweep'] if x not in nb]
            R('s4-%s' % gid[3:], tag, '화면 훑기 — 결과 상자 넘침 · 잘림 · 겹침(바탕에 있던 것 빼고) 0', not newi, None if QC.REGRESS else (not res.get('BASE_sweep')),
              {'새로 생김': newi, 'NEW 전체': res['NEW_sweep'][:8], 'BASE': sorted(nb)[:8]})
    if eng != 'chromium' or QC.SMOKE:
        return
    # §B-4 바꾸기
    if not ONLY or 's2' in ONLY:
        res = {}
        for who in (('NEW', 'BASE') if QC.GATE else ('NEW',)):
            dv = Dev(br, eng, who, APPS[who], 'bio', dev, touch)
            try:
                res[who] = s2_switch(dv)
            except Exception as e:
                res[who] = (False, 'ERR ' + repr(e)[:300])
            finally:
                dv.close()
        R('s2-es-bio', tag, '검색어 바꾸기(굴리는 중) — 옛 줄 0 · 새 첫 100 · 끝까지 = 새 결과', res['NEW'][0], res.get('BASE', (None,))[0], {'NEW': res['NEW'][1], 'BASE': res.get('BASE', (None, None))[1]})
    # §B-5 첫 그림 빠르기(PC 만 · 같은 말 · 다섯 번씩 세 벌 → 벌마다 가운데 · 세 벌 가운데)
    if devname == 'PC' and (not ONLY or 's3' in ONLY):
        meas = {}
        for subj, q in (('bio', '다음'), ('phys', '물체')):
            for who in (('NEW', 'BASE') if QC.GATE else ('NEW',)):
                dv = Dev(br, eng, who, APPS[who], subj, dev, touch)
                try:
                    dv.ev("()=>{const i=document.getElementById('q');i.value='';}")
                    sets = []
                    for _ in range(3):
                        ts = dv.ev(TIMEJS, [q, 5])
                        sets.append(statistics.median(ts))
                    meas[(subj, who)] = round(statistics.median(sets), 2)
                finally:
                    dv.close()
            nv = meas[(subj, 'NEW')]
            bv = meas.get((subj, 'BASE'))
            if QC.REGRESS:
                bv = QC.base('s3.%s@%s' % (subj, tag), nv)   # regress — 바탕 = 앞 판 새 값(스냅샷)
            ratio = (nv / bv) if bv else None
            R('s3-%s' % subj, tag, '첫 그림 빠르기(입력 → 첫 100 줄) 가운데 값 ≤ 바탕 × 1.2', ratio is not None and ratio <= 1.2, None,
              {'말': q, 'NEW ms': nv, 'BASE ms': bv, '비': round(ratio, 3) if ratio else None, '기준': QC.base_note('s3.%s@%s' % (subj, tag)) if QC.REGRESS else '바탕 띄움'})


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
    with sync_playwright() as pw:
        for eng in ENGS:
            if QC.SMOKE and eng != 'chromium':
                continue
            br = getattr(pw, eng).launch()
            try:
                with QC.stage('%s PC' % eng):
                    if eng == 'chromium':
                        run_dev(br, eng, 'PC', PCDEV, False)
                with QC.stage('%s 폰' % eng):
                    if not QC.SMOKE:
                        run_dev(br, eng, '폰390', JG.PHONE, True)
            finally:
                br.close()
    npass = sum(1 for r in ROWS if r[3]); nfail = sum(1 for r in ROWS if not r[3])
    vac = [r for r in ROWS if r[4] is True and r[0].startswith(('s1', 's2'))]   # 바뀜 잣대(s1 · s2)만 — s4 훑기 = 바탕에 없던 흠 0(바탕도 PASS 가 맞음)
    print('\n== PASS %d · FAIL %d · 헛잣대(바탕도 PASS · 바뀜 잣대 s1 · s2) %d · %.0f초' % (npass, nfail, len(vac), time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · jagwa_search_all · NEW %s · 바탕 %s · 모드 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), os.path.basename(NEWF),
                base_rev if QC.GATE else '(regress · 스냅샷)', QC.MODE, ','.join(ENGS)))
        for g, dv, n, okn, okb, v in ROWS:
            f.write('%s | 바탕 %s | %s · %s · %s | %s\n' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, dv, n,
                    (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str))[:2000]))
        f.write('== PASS %d · FAIL %d · 헛잣대(바탕도 PASS) %d\n' % (npass, nfail, len(vac)))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
