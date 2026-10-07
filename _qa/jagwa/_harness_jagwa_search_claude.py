# -*- coding: utf-8 -*-
r"""_task_jagwa_search_claude §B 관문 — 자과 근거 검색에 Claude 풀이 · 분포 「C n」 · 목록 암기 상자(민법 꼴)

  python _harness_jagwa_search_claude.py [--new <앱>] [--base <앱 파일 | git rev>] [--eng chromium,webkit] [--only b1,b2,...] [--vendor <cdnjs 사본>] [--res <결과>]

  NEW = genie 작업트리 jagwa/index.html · BASE(헛잣대) = 착수 때 genie HEAD(기본 HEAD — 이 판을 커밋한 뒤에는 --base <앞 커밋>)
  데이터 = studyplandata 작업트리 · 기록 = 과목 기록.json 사본 + Claude 풀이(data.gpt):
    지학 84 · 149 = studyplandata origin/main earth/기록.json(읽기만 · 9/30 에 원격에 든 풀이) · 물리 72 = 작업트리 기록 그대로
    합성 셋 — 물리 97(p002 적재 전이라 원격에 없음 · 「④ 암기팁」 꼴) · 생물 하나(암기 절 없음) · 지학 근거 없는 문항 하나(Claude 풀이만)
    「C 0」 칸 = 같은 사본에서 gpt 를 비운 것
  PUT 은 앱 fetch 를 가로채 몸통만 모은다(밖으로 안 나감 · 기록 쓰기 0) · 기기 하나 = 문맥 하나(_harness_jagwa_uid 의 Srv · __J)
  관문마다 NEW 는 PASS · BASE 는 FAIL(헛잣대 열) — 바탕도 참이어야 하는 칸(무변 칸)은 「바탕 = 기준」
  --vendor = cdnjs.cloudflare.com/ajax/libs/… 사본 폴더(줄 때만 · cdnjs 가 막힌 곳)
  fix1(_task_jagwa_search_claude_fix1) = B-8 · B-9 — ID 로 찾으면 근거 줄 그대로(맨 바탕 cedc251 과 맞댐) · 풀이 본문 말은 e9de3b8 그대로(--base e9de3b8 로 헛잣대)
    기대 「Claude」 딱지·조각 = 풀이 md 에서 첫 줄 제 ID 머리를 뗀 글에 그 말이 있을 때(앱과 따로 파이썬으로 셈)
  ⚠ 자과앱 픽셀 게이트 없음(CLAUDE.md) — DOM 글자 · 자리 · 개수 · 실제 마우스·손가락 누름
"""
import io, json, os, re, sys, time, copy, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_ARGV = sys.argv; sys.argv = [sys.argv[0]]   # 두 하네스는 들어올 때 sys.argv 를 읽는다
import _harness_jagwa_uid as HU      # noqa: E402  Srv · INIT · JS(__J) · git
import _harness_jagwa_search as HS   # noqa: E402  SJS(__S) · typeq · st
sys.argv = _ARGV


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = HU.GENIE; SPD = HU.SPD
NEWF = ARG('--new', os.path.join(GENIE, 'jagwa', 'index.html'))
BASEF = ARG('--base', 'HEAD')
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
VENDOR = ARG('--vendor')
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_search_claude_result.txt'))
ROWS = []
APPS = {}
from playwright.sync_api import sync_playwright   # noqa: E402

# ★ uid_unify G-1(2026-10-04 · gigu/_task_jagwa_uid_unify.md §G-1 · 근거 = 사용자 10/4 16:45 「uid 랑 중복되니까 nn회 n번 없애」) — 통합 검색 줄(ggResRowHTML · esRowHTML)은 기출 uid 줄에서 .cd(uid) 바로 뒤 「NN회 N번」 <b> 를 안 그린다.
#   G-1 의 전제(uid 의 회·번 = 데이터 회차·문번)는 지학만 맞다 — 생물 기출 uid 270 중 260 은 뒷자리가 문번이 아니다(본 세션 10/4 23:05 · 예 B00-37-01 = 37회 21번) → 생물 갈래는 사용자 결정 전.
#   그래서 뜻한 차이로 받는 것은 지학 기출 uid(G..)뿐이다 · 생물(B..) 줄은 바탕과 같아야 한다(다르면 FAIL 이 그대로 보인다 = 「결정 대기 — 생물 G-1」).
#   결정이 (가) 생물도 걷음이면 G1_PFX = 'GB' · (다) 지학만이면 'G' 그대로. 새 판(앱 글에 ynUid)과 바탕이 같은 갈래면(옛 판끼리 · 새 판끼리) 아무것도 안 뗀다 = 옛 잣대 그대로.
G1_PFX = 'G'
STRIP = {'NEW': False, 'BASE': False}   # main() 이 앱 글로 채운다 — 「새 판에만 ynUid 가 있으면」 바탕 쪽 줄 HTML 에서 지학 기출 uid 줄의 <b>NN회 N번</b> 을 뗀 뒤 맞댄다(NEW = BASE − 회·번)
G1_N = {'떼어 낸 줄': 0}


def g1_strip(h):
    """줄 HTML 에서 기출 uid(G1_PFX) .cd 바로 뒤의 <b>NN회 N번</b>(<mark> 이 씌워졌어도)을 뗀다"""
    out = re.sub(r'(<span class="cd">(?:<mark>)?[%s]\d\d-\d+-\d+(?:</mark>)?</span>)<b>(?:<mark>)?\d+회 \d+번(?:</mark>)?</b>' % G1_PFX, r'\1', h)
    if out != h:
        G1_N['떼어 낸 줄'] += 1
    return out


def R(g, eng, name, okn, okb, val):
    ROWS.append((g, eng, name, okn, okb, val))
    print('%s | 바탕 %s | %s · %s · %s | %s' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, eng, name,
          (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str))[:700]), flush=True)


def want(g):
    return not ONLY or g in ONLY


OKNET = ('http://127.0.0.1', 'https://cdnjs.cloudflare.com/', 'https://cdn.jsdelivr.net/', 'https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')


def _route(rt):
    u = rt.request.url
    m = re.match(r'https://cdnjs\.cloudflare\.com/ajax/libs/(.+)$', u.split('?')[0]) if VENDOR else None
    if m:
        f = os.path.join(VENDOR, *m.group(1).split('/'))
        if os.path.isfile(f):
            return rt.fulfill(path=f, content_type='text/css' if f.endswith('.css') else ('font/woff2' if f.endswith('.woff2') else 'application/javascript'))
        return rt.abort()
    return rt.continue_() if u.startswith(OKNET) else rt.abort()


J9 = r"""
window.__C9={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 R(e){if(!e)return null;const r=e.getBoundingClientRect();return {l:Math.round(r.left*10)/10,r:Math.round(r.right*10)/10,t:Math.round(r.top*10)/10,b:Math.round(r.bottom*10)/10,w:Math.round(r.width*10)/10,h:Math.round(r.height*10)/10}},
 vis(e){if(!e||!e.isConnected)return false;const cs=getComputedStyle(e);if(cs.display==='none'||cs.visibility==='hidden')return false;const r=e.getBoundingClientRect();return r.width>0&&r.height>0},
 gmode(){const b=document.querySelector('.seg2 [data-sm="g"]');if(b)b.click()},
 rows(){return [...document.querySelectorAll('#esres [data-ggres]')].map(d=>({no:+d.dataset.ggres,cd:__C9.tx(d.querySelector('.cd')),tags:[...d.querySelectorAll('.clsrc')].map(__C9.tx),
   gl:d.querySelectorAll('.gl').length,glc:__C9.tx(d.querySelector('.glc')),glcMark:d.querySelectorAll('.glc mark').length,box:[...d.querySelectorAll('.gpbox')].map(b=>b.textContent),html:d.outerHTML}))},
 head(){const h=document.querySelector('#esres .esdh');if(!h)return null;const cs=getComputedStyle(h);const c=h.querySelector('.esc'),b=h.querySelector('.esb');
   return {t:__C9.tx(h),cls:h.className,bg:cs.backgroundColor,col:cs.color,c:c?{t:__C9.tx(c),off:c.classList.contains('off'),btn:c.hasAttribute('data-escl')}:null,b:b?{t:__C9.tx(b),off:b.classList.contains('off')}:null,
     units:[...document.querySelectorAll('#esres .esdr')].map(d=>({t:__C9.tx(d.querySelector('span')),n:d.querySelectorAll('.n').length,c:__C9.tx(d.querySelector('.gpn'))}))}},
 gp(){return Object.keys(GP).filter(k=>GP[k]).map(Number).sort((a,b)=>a-b)},
 ggN(){return DATA.filter(r=>!isC(r)&&ggOf(GGU(r)).length>0).length},
 /* 옛: unionN(){return DATA.filter(r=>!isC(r)&&(ggOf(GGU(r)).length>0||!!(GP[r[F.NO]]))).length}, */
 unionN(){return DATA.filter(r=>!isC(r)&&(ggOf(GGU(r)).length>0||!!(GP[typeof qk==='function'?qk(r[F.NO]):r[F.NO]]))).length},   /* ★ uid_unify A-1 — 카드 층 GP 열쇠 = uid(qk) · 옛 판(qk 없음) = 번호 */
 ggHay(){return DATA.filter(r=>!isC(r)).map(r=>ggOf(GGU(r)).map(g=>ggFlat(g)+' '+(g.cs||[]).map(c=>c.t).join(' ')).join(' ')+' '+GGU(r)+' '+codeShow(r)).join(' ').toLowerCase()},
 rowHay(no){const r=DATA[no-1];return r?ggOf(GGU(r)).map(g=>ggFlat(g)+' '+(g.cs||[]).map(c=>c.t).join(' ')).join(' ').toLowerCase():''},
 uidOf(no){const r=DATA[no-1];return r?GGU(r):''},
 /* 옛: noGg(){const r=DATA.find(x=>!isC(x)&&!ggOf(GGU(x)).length&&!GP[x[F.NO]]);return r?r[F.NO]:0} */
 noGg(){const r=DATA.find(x=>!isC(x)&&!ggOf(GGU(x)).length&&!GP[typeof qk==='function'?qk(x[F.NO]):x[F.NO]]);return r?r[F.NO]:0}   /* ★ uid_unify A-1 — 같은 까닭 */
};
"""


class Dev:
    def __init__(self, br, eng, vp=None, mobile=False):
        self.eng = eng; self.S = HU.Srv()
        self.vp = vp or {'width': 1553, 'height': 900}
        self.ctx = br.new_context(viewport=self.vp, device_scale_factor=1, has_touch=True, is_mobile=bool(mobile and eng == 'chromium'))
        self.ctx.route('**/*', _route)
        self.pg = None; self.errs = []; self.cdp = None

    def load(self, app, subj, rec, wait=2500):
        self.S.app = app; self.S.spd = SPD; self.S.rec = dict(rec or {}); self.S.static = {}
        if self.pg:
            self.pg.close()
        self.pg = self.ctx.new_page(); self.pg.set_default_timeout(150000)
        self.pg.add_init_script(HU.INIT.replace('__SUBJ__', subj))
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:200]))
        self.pg.goto('http://127.0.0.1:%d/app.html' % self.S.port, wait_until='load')
        self.pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=120000)
        self.pg.evaluate(HU.JS); self.pg.evaluate(HS.SJS); self.pg.evaluate(J9)
        for _ in range(120):
            if self.ev("()=>__J.ready()"):
                break
            self.pg.wait_for_timeout(250)
        self.pg.wait_for_timeout(wait)
        for _ in range(60):   # 기록 맞춤 끝(풀이 GP 가 들어온 뒤)
            if not self.ev("()=>typeof recBusy!=='undefined'&&recBusy"):
                break
            self.pg.wait_for_timeout(300)
        self.cdp = self.ctx.new_cdp_session(self.pg) if self.eng == 'chromium' else None
        return self

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def tap(self, x, y, wait=500):
        if self.vp['width'] > 1100:
            self.pg.mouse.click(x, y)
        elif self.cdp:
            pt = {'x': x, 'y': y, 'radiusX': 22, 'radiusY': 22, 'force': 1, 'id': 1}
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [pt]}); self.pg.wait_for_timeout(60)
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        else:
            self.pg.touchscreen.tap(x, y)
        self.pg.wait_for_timeout(wait)

    def click(self, sel, wait=500):
        r = self.ev("s=>{const e=document.querySelector(s);if(!e)return null;e.scrollIntoView({block:'nearest'});return __C9.R(e)}", sel)
        if not r:
            return False
        self.tap(r['l'] + r['w'] / 2, r['t'] + r['h'] / 2, wait)
        return True

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass
        try:
            self.S.srv.shutdown()
        except Exception:
            pass


# ══════════ 기록 사본 ══════════
SYN = {
    'phys97': '① 가장 빨리 푸는 방법\n- 합성 풀이(물리 97 꼴)\n④ 암기팁\n- **합성암기팁첫줄 물리** 둘째 말\n- 합성 암기팁 둘째 줄\n⑤ 같은 유형\n- 끝',
    'bio': '① 정리\n- **합성생물첫줄** 풀이 첫 줄\n- 합성 생물 둘째 줄\n② 연결\n- 합성 생물 연결',
    'earth_nogg': '① 정리\n- 합성 지학 정리 줄\n② 암기 (합성)\n- **합성갈매기섬** 근거 없는 문항 암기 첫 줄\n- 합성 지학 암기 둘째 줄\n③ 연결\n- 끝',
}


def rec_of(subj, gp_on=True, nogg_no=0, bio_no=0):
    rec = json.loads(open(os.path.join(SPD, subj, '기록.json'), 'rb').read().decode('utf-8'))
    D = rec.setdefault('data', {}); gp = dict(D.get('gpt') or {})
    if subj == 'earth':
        try:
            now = json.loads(HU.git(SPD, 'show', 'origin/main:earth/기록.json').decode('utf-8'))
            for k in ('84', '149'):
                v = ((now.get('data') or {}).get('gpt') or {}).get(k)
                if v:
                    gp[k] = v
        except Exception:
            pass
        if nogg_no:
            gp[str(nogg_no)] = SYN['earth_nogg']
    if subj == 'phys' and '97' not in gp:
        gp['97'] = SYN['phys97']
    if subj == 'bio' and bio_no:
        gp[str(bio_no)] = SYN['bio']
    D['gpt'] = gp if gp_on else {}
    return {'%s/기록.json' % subj: json.dumps(rec, ensure_ascii=False).encode('utf-8')}, (gp if gp_on else {})


def memo(md):
    """암기 절(지시서 A-3-1 · 앱과 따로 지은 같은 규칙) → (all, first)"""
    L = md.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    H = [(i, (re.match(r'^\s*([①-⑩])\s*(.*)$', x).group(2) or '')) for i, x in enumerate(L) if re.match(r'^\s*([①-⑩])\s*(.*)$', x)]
    unb = lambda x: re.sub(r'\*\*([^*]+)\*\*', r'\1', x)
    one = lambda t: next((x.strip() for x in t.split('\n') if x.strip()), '')

    def body(k):
        a = H[k][0] + 1; b = H[k + 1][0] if k + 1 < len(H) else len(L)
        return '\n'.join(unb(x) for x in L[a:b]).strip('\n')
    mk = next((k for k, h in enumerate(H) if '암기' in h[1]), -1)
    if mk >= 0:
        a = body(mk)
        return a, one(a)
    f = one(body(0) if H else '\n'.join(unb(x) for x in L))
    return f, f


def typeq(dv, text):
    """검색 칸에 글 — 칸을 스크립트로 잡는다(iPad 폭에서 서랍이 칸 위를 덮어 마우스 누름이 칸에 안 닿음 · 칸 꼴·누름 잣대가 아니라 글 넣기만)"""
    dv.ev("()=>{const q=document.getElementById('q');if(q){q.focus();q.value='';q.dispatchEvent(new Event('input',{bubbles:true}))}}")
    if text:
        dv.pg.keyboard.type(text, delay=5)
    dv.pg.wait_for_timeout(250)
    # 앱 터치 막이(TAP_EAT · 진짜 누름 뒤 1.2초 안에 다시 그리면 다음 진짜 click 하나를 400ms 먹는다)가 풀린 뒤 — 칸을 스크립트로 잡아 그 click 이 없다
    dv.pg.wait_for_function("()=>typeof TAP_EAT==='undefined'||!TAP_EAT||Date.now()>TAP_EAT", timeout=5000)


def app_src(x):
    if os.path.isfile(x):
        return open(x, 'rb').read().replace(b'\r\n', b'\n')
    return HU.git(GENIE, 'show', '%s:jagwa/index.html' % x)


# ══════════ 관문 ══════════
W = {}   # 표본 말(NEW 기기에서 한 번 골라 바탕에도 같은 말)


def earth_dev(br, eng, app, gp_on=True, vp=None, mobile=False):
    """지학 기기 — 근거 없는 문항 하나에 합성 풀이를 넣은 기록 사본"""
    d0 = Dev(br, eng, vp, mobile)
    nog = W.get('nogg_no')
    if not nog:   # 근거·풀이 없는 첫 문항(데이터 차례) — 기록 사본 없이 한 번 연다
        d0.load(app, 'earth', {'earth/기록.json': open(os.path.join(SPD, 'earth', '기록.json'), 'rb').read()})
        nog = W['nogg_no'] = d0.ev("()=>__C9.noGg()")
    rec, gp = rec_of('earth', gp_on, nogg_no=nog)
    d0.load(app, 'earth', rec)
    return d0, gp


def pick_words(br, eng):
    """W_CL = 지학 149 암기 절에만(근거·댓글·uid·ID 어디에도 없음) · W_BOTH = 「심발」(149 풀이 + 근거) · W_GG = 근거에만(풀이 어디에도 없음)"""
    if W.get('cl'):
        return
    dv, gp = earth_dev(br, eng, APPS['NEW'])
    try:
        hay = dv.ev("()=>__C9.ggHay()"); gpall = ' '.join(gp.values()).lower()
        a, _ = memo(gp.get('149', ''))
        toks = [t for t in re.findall(r'[가-힣A-Za-z0-9]{2,}', a.replace('**', ''))]
        W['cl'] = next((t for t in toks if t.lower() not in hay and len(t) >= 2), None)
        W['both'] = '심발' if ('심발' in hay and '심발' in gp.get('149', '')) else next((t for t in toks if t.lower() in hay), None)
        W['both_own'] = W['both'] and W['both'].lower() in dv.ev("n=>__C9.rowHay(n)", 149)
        gtoks = re.findall(r'[가-힣]{3,}', hay)
        W['gg'] = next((t for t in gtoks if t not in gpall and len(t) >= 3), None)
        W['uid149'] = dv.ev("n=>__C9.uidOf(n)", 149)
    finally:
        dv.close()


def b1(br, eng, app):
    dv, gp = earth_dev(br, eng, app)
    try:
        dv.ev("()=>__C9.gmode()"); dv.pg.wait_for_timeout(300)
        out = {'말': {k: W.get(k) for k in ('cl', 'both', 'gg')}}
        typeq(dv, W['cl']); rc = dv.ev("()=>__C9.rows()")
        r149 = next((r for r in rc if r['no'] == 149), None)
        out['Claude 에만'] = {'줄': len(rc), '149': r149 and {k: r149[k] for k in ('cd', 'tags', 'gl', 'glc', 'glcMark')}}
        typeq(dv, W['both']); rb = dv.ev("()=>__C9.rows()")
        b149 = next((r for r in rb if r['no'] == 149), None)
        out['둘 다'] = {'줄': len(rb), '149': b149 and {k: b149[k] for k in ('tags', 'gl', 'glcMark')}, '딱지들': [r['tags'] for r in rb][:6]}
        typeq(dv, W['gg']); rg = dv.ev("()=>__C9.rows()")
        out['근거에만'] = {'줄': len(rg), '딱지들': sorted({','.join(r['tags']) for r in rg}), 'html': [r['html'] for r in rg]}
        ok = bool(r149 and r149['tags'] == ['Claude'] and r149['glcMark'] >= 1 and r149['gl'] == 0
                  and b149 and 'Claude' in b149['tags'] and (('근거' in b149['tags']) if W.get('both_own') else True)
                  and rg and all(r['tags'] in (['근거'], ['댓글'], ['근거', '댓글']) for r in rg) and not dv.errs)
        return ok, out
    finally:
        dv.close()


def b2(br, eng, app):
    dv, gp = earth_dev(br, eng, app)
    try:
        dv.ev("()=>__C9.gmode()"); typeq(dv, '')
        qc = dv.ev("()=>__C9.tx(document.getElementById('qCnt'))")
        ggN, uN = dv.ev("()=>__C9.ggN()"), dv.ev("()=>__C9.unionN()")
        dv.click('#qCnt'); h = dv.ev("()=>__C9.head()")
        m = re.match(r'근거 (\d+)건 · (\d+)개 단원', h['t'] if h else '')
        out = {'개수 칸': qc, '근거 문항': ggN, '근거 ∪ 풀이': uN, '분포 머리': h and h['t'], '풀이 문항(모집단 안)': len([k for k in gp if k])}
        ok = qc == '근거 %d개 ▸' % ggN and bool(m) and int(m.group(1)) == uN and uN > ggN
        return ok, out
    finally:
        dv.close()


def b3(br, eng, app):
    out = {}
    dv, gp = earth_dev(br, eng, app)
    try:
        dv.ev("()=>__C9.gmode()"); typeq(dv, ''); dv.click('#qCnt')
        h0 = dv.ev("()=>__C9.head()"); out['처음'] = h0
        n = len(gp)
        okc = bool(h0 and h0['c'] and h0['c']['t'] == 'C %d' % n and not h0['c']['off'])
        dv.click('#esres .esdh .esc'); h1 = dv.ev("()=>__C9.head()"); out['C 켬'] = h1
        units_cl = sorted({u['t'] for u in (h1 or {}).get('units', [])})
        okc = okc and h1 and 'cl' in h1['cls'] and h1['bg'] == 'rgb(255, 247, 237)' and h1['col'] == 'rgb(180, 83, 9)' \
            and ('C %d건' % n) in h1['t'] and 'Claude 풀이가 있는 것만 보는 중' in h1['t'] and all(u['n'] == 0 for u in h1['units']) and len(h1['units']) >= 1
        if h0 and h0['b'] and not h0['b']['off']:
            dv.click('#esres .esdh .esb'); h2 = dv.ev("()=>__C9.head()"); out['! 켬'] = {'cls': h2['cls'], 'c': h2['c']}
            dv.click('#esres .esdh .esc'); h3 = dv.ev("()=>__C9.head()"); out['다시 C'] = {'cls': h3['cls']}
            okc = okc and 'bang' in h2['cls'] and 'cl' not in h2['cls'] and 'cl' in h3['cls'] and 'bang' not in h3['cls']
        out['C 단원'] = units_cl
    finally:
        dv.close()
    dv, _ = earth_dev(br, eng, app, gp_on=False)
    try:
        dv.ev("()=>__C9.gmode()"); typeq(dv, ''); dv.click('#qCnt')
        z0 = dv.ev("()=>__C9.head()"); dv.click('#esres .esdh .esc'); z1 = dv.ev("()=>__C9.head()")
        out['C 0 사본'] = {'칩': z0 and z0['c'], '누른 뒤 머리': z1 and z1['cls']}
        okz = bool(z0 and z0['c'] and z0['c']['t'] == 'C 0' and z0['c']['off'] and not z0['c']['btn'] and z1 and 'cl' not in z1['cls'])
    finally:
        dv.close()
    return bool(okc and okz), out


def _unit_rows(dv, no):
    """그 문항 단원의 목록을 열어 줄 하나"""
    i = dv.ev("n=>{const u=(typeof unitOf==='function'?unitOf(n):'')||'';return (typeof ES_DK!=='undefined'?ES_DK:[]).indexOf(u)}", no)
    if i is None or i < 0:
        return None
    dv.click('#esres [data-esu="%d"]' % i)
    return next((r for r in dv.ev("()=>__C9.rows()") if r['no'] == no), None)


def b4(br, eng, app):
    out = {}; ok = True
    cases = []
    dv, gp = earth_dev(br, eng, app)
    try:
        nog = W['nogg_no']
        for no in (149, 84, nog):
            md = gp.get(str(no), ''); a, f = memo(md)
            for on in (False, True):
                dv.ev("()=>__C9.gmode()"); typeq(dv, ''); dv.click('#qCnt')
                if on:
                    dv.click('#esres .esdh .esc')
                r = _unit_rows(dv, no)
                want_t = ('Claude · ' + a) if on else ('C · ' + f)
                got = r and r['box']
                c = {'문항': no, 'C': on, '상자': got, '근거 줄': r and r['gl'], '맞음': bool(got) and got == [want_t]}
                if no == nog:
                    c['맞음'] = c['맞음'] and r['gl'] == 0
                if on:
                    c['줄 수'] = [len(got[0].split('\n')) if got else 0, len(want_t.split('\n'))]
                cases.append(c)
    finally:
        dv.close()
    for subj, nos in (('phys', (72, 97)), ('bio', None)):
        d2 = Dev(br, eng)
        try:
            if subj == 'bio':
                d2.load(app, 'bio', {})
                bno = d2.ev("()=>DATA.find(r=>!isC(r))[F.NO]")
                rec, gp2 = rec_of('bio', bio_no=bno); nos = (bno,)
            else:
                rec, gp2 = rec_of('phys')
            d2.load(app, subj, rec)
            for no in nos:
                a, f = memo(gp2.get(str(no), ''))
                for on in (False, True):
                    d2.ev("()=>__C9.gmode()"); typeq(d2, ''); d2.click('#qCnt')
                    if on:
                        d2.click('#esres .esdh .esc')
                    r = _unit_rows(d2, no)
                    want_t = ('Claude · ' + a) if on else ('C · ' + f)
                    got = r and r['box']
                    cases.append({'과목': subj, '문항': no, 'C': on, '상자': got, '근거 줄': r and r['gl'], '맞음': bool(got) and got == [want_t]})
        finally:
            d2.close()
    ok = all(c['맞음'] for c in cases) and len(cases) >= 10
    out['칸'] = cases
    return bool(ok), out


PVJS = r"""(q)=>{ /* ★ physprev(10/2) — _task_jagwa_physprev 57줄(A-2-3): 물리만 t 로만 걸린 줄(only) · 조각이 t 인 줄(kind) · 결과 줄을 번호마다(rows) · 나머지 글(rest) */
 const ph=typeof HASBOOK!=='undefined'&&!HASBOOK&&typeof pvHit==='function'&&typeof esHit==='function'&&typeof esPhysHit==='function';
 const only=[],kind=[];
 if(ph){ES_NOS.forEach(n=>{const r=DATA.find(x=>x[F.NO]===n);const h=r?esHit(r,q):null;if(h&&h.k==='prev')kind.push(n)});
   const keep=window.pvHit;try{window.pvHit=undefined;ES_NOS.forEach(n=>{const r=DATA.find(x=>x[F.NO]===n);if(r&&!esPhysHit(r,q))only.push(n)})}finally{window.pvHit=keep}}
 const box=document.getElementById('esres');
 const rows=box?[...box.children].filter(e=>e.dataset&&e.dataset.esq).map(e=>[+e.dataset.esq,e.outerHTML]):[];
 let rest='';if(box){const c=box.cloneNode(true);[...c.children].forEach(e=>{if(e.dataset&&e.dataset.esq)e.remove()});rest=c.innerHTML}
 /* ★ 2026-10-07 (_task_jagwa_phys_win §A-45) — 물리 위 검색이 보이는 제목(titleOf)·고친 제목(pnFix)도 찾음 → 그 둘로 걸리는 번호 tt(앱 esPhysHit 글에 titleOf(r) 가 있을 때만 · 옛 판은 빈 목록)
    옛 줄: return {nos:ES_NOS.slice(),only,kind,rows,rest}} */
 const tt=(ph&&String(esPhysHit).indexOf('titleOf(r)')>=0)?ES_NOS.filter(n=>{const r=DATA.find(x=>x[F.NO]===n);return !!r&&(String(titleOf(r)).includes(q)||String(pnFix(r)||'').includes(q))}):[];
 return {nos:ES_NOS.slice(),only,kind,rows,rest,tt}}"""
CAPNOTE = '<div class="bplnone">상위 100건만 표시했습니다. 검색어를 더 좁혀보세요.</div>'


def pv_same(n, b):
    """★ physprev(10/2) — 근거 = _task_jagwa_physprev 57줄(A-2-3) · 말 하나의 새 판(n) · 바탕(b) 결과를 맞댄다 → (같음, 적을 값)
       집합 = 새 판 걸린 것 − t 로만 걸린 것 == 바탕 걸린 것 · 줄 HTML = 둘 다 보이는 줄 중 조각이 t 인 줄을 뺀 것끼리 같고 차례도 같음
       · 바탕에 보이는데 새 판에 안 보이는 줄은 새 판이 100줄 상한에 닿았을 때만(t 로 더 걸려 밀림) · 나머지 글은 「상위 100건」 꼬리를 빼고 같음"""
    if not isinstance(n, dict) or not isinstance(b, dict):
        return n == b, {}
    only, kind = set(n.get('only') or []), set(n.get('kind') or []) | set(b.get('kind') or [])
    nn = [x for x in n['nos'] if x not in only]
    bb = [x for x in b['nos'] if x not in set(b.get('only') or [])]
    rn = [(x, h) for x, h in n['rows'] if x not in kind]
    rb = [(x, h) for x, h in b['rows'] if x not in kind]
    hn, hb = dict(rn), dict(rb)
    common = [x for x, _ in rn if x in hb]
    html_bad = [x for x in common if hn[x] != hb[x]]
    order_ok = common == [x for x, _ in rb if x in hn]
    miss = [x for x, _ in rb if x not in hn]
    cap_ok = not miss or len(n['rows']) >= 100
    # ★ 2026-10-07 (_task_jagwa_phys_win §A-45) — 새 판 물리 위 검색이 보이는 제목·고친 제목도 찾음 → 바탕에 없고 tt 에 든 번호(tx)는 「제목으로 더 걸림」 = 뜻한 차 · 그 밖은 옛 잣대 그대로(옛 판은 tt 가 비어 tx 0)
    tt, bset = set(n.get('tt') or []), set(bb)
    tx = [x for x in nn if x not in bset and x in tt]
    # 옛 줄: extra = [x for x, _ in rn if x not in hb]
    extra = [x for x, _ in rn if x not in hb and x not in tx]
    extra_ok = not extra or len(b['rows']) >= 100
    rest_ok = n['rest'].replace(CAPNOTE, '') == b['rest'].replace(CAPNOTE, '') \
        and ((CAPNOTE in n['rest']) == (len(n['nos']) > 100)) and ((CAPNOTE in b['rest']) == (len(b['nos']) > 100))
    # 옛 줄: same = nn == bb and not html_bad and order_ok and cap_ok and extra_ok and rest_ok
    same = (nn == bb or (bool(tx) and [x for x in nn if x not in tx] == bb)) and not html_bad and order_ok and cap_ok and extra_ok and rest_ok   # ★ 2026-10-07 (_task_jagwa_phys_win §A-45) — 집합 = 바탕 + 제목으로 더 걸린 것(차례 그대로)
    info = {'t 로만': len(only), '조각 t': len(kind), '상한 밀림': len(miss)} if (only or kind or miss) else {}
    if tx:   # ★ 2026-10-07 (_task_jagwa_phys_win §A-45) — 제목으로 더 걸린 번호 수는 값에 남김
        info['제목으로 더 걸림'] = len(tx)
    if not same:
        info.update({'집합 같음': nn == bb, '줄 HTML 다름': html_bad[:5], '차례': order_ok, '상한': [len(n['rows']), len(b['rows']), miss[:5]], '더 보임': extra[:5], '나머지 글': rest_ok})
    return same, info


QW = {'earth': lambda: [W.get('cl'), '합성갈매기섬', '맨틀', '심발', 'G09-46-10'], 'bio': lambda: ['합성생물첫줄', 'DNA', '세포막', '효소', 'B20-57-05'],
      'phys': lambda: ['합성암기팁첫줄', 'PEM0101', '속력', '전기장', '가속도']}


def b5(br, eng, app):
    """기출(문제) 검색 — 말 다섯씩 · 걸린 집합 · 결과 상자 HTML(바탕과 견준다 · main 에서)"""
    res = {}
    for subj in ('bio', 'earth', 'phys'):
        if subj == 'earth':
            dv, _ = earth_dev(br, eng, app)
        else:
            dv = Dev(br, eng)
            if subj == 'bio':
                dv.load(app, 'bio', {}); bno = dv.ev("()=>DATA.find(r=>!isC(r))[F.NO]"); rec, _ = rec_of('bio', bio_no=bno)
            else:
                rec, _ = rec_of('phys')
            dv.load(app, subj, rec)
        try:
            for q in QW[subj]():
                typeq(dv, q)
                res['%s %s' % (subj, q)] = dv.ev(PVJS, q)   # ★ physprev(10/2) — 걸린 집합 · 결과 줄을 번호마다(옛 [ES_NOS, innerHTML] 대신 · 맞대기는 pv_same)
        finally:
            dv.close()
    return res


# ══════════ B-6 화면 훑기(규칙 60) · 「!」·「C」 터치 누름 높이 ══════════
SWEEPJS = r"""(touch)=>{const vw=innerWidth,vh=innerHeight,de=document.documentElement;
 const ACT='button,a[href],input,select,textarea,[onclick],[data-ggres],[data-esu],[data-esbang],[data-escl],[data-esback],.chip,.chchip';
 const sig=e=>{let s=e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(e.classList.length?'.'+[...e.classList].slice(0,2).join('.'):'');
   const t=(e.textContent||'').replace(/\s+/g,' ').trim().replace(/\d+/g,'#').slice(0,14);
   return s+((e.tagName==='BUTTON'||e.hasAttribute('data-esbang')||e.hasAttribute('data-escl')||e.classList.contains('chip')||e.classList.contains('chchip'))?'「'+t+'」':'')};
 const els=[...document.querySelectorAll(ACT.split(',').map(x=>'#esres '+x).join(','))].filter(e=>{if(!__C9.vis(e))return false;const r=e.getBoundingClientRect();return r.bottom>0&&r.right>0&&r.top<vh&&r.left<vw});   /* 이 판이 바꾸는 곳 = 결과 상자(#esres) 안 — 상자 밖 쪽 칸은 상자 길이에 따라 보였다 숨었다 할 뿐 */
 const over=[],clip=[],cover=[],small=[];
 for(const e of els){const r=e.getBoundingClientRect();
   if(r.right>vw+1)over.push(sig(e));
   let a=e.parentElement;while(a&&a!==document.body){const cs=getComputedStyle(a);if(/(hidden|clip|auto|scroll)/.test(cs.overflowX)){const ar=a.getBoundingClientRect();if(r.right>ar.right+1||r.left<ar.left-1)clip.push(sig(e));break}a=a.parentElement}
   const cx=Math.min(vw-1,Math.max(0,r.left+r.width/2)),cy=Math.min(vh-1,Math.max(0,r.top+r.height/2)),at=document.elementFromPoint(cx,cy);
   if(at&&!(at===e||e.contains(at)||at.contains(e)))cover.push(sig(e));
   if(Math.min(r.width,r.height)<(touch?36:14))small.push(sig(e))}
 const b=document.getElementById('esres');const bw=b?[...b.querySelectorAll('*')].filter(x=>x.getBoundingClientRect().right>b.getBoundingClientRect().right+1).length:0;
 return {docow:de.scrollWidth-de.clientWidth,boxow:bw,n:els.length,over,clip,cover,small}}"""
HITJS = r"""(sel)=>{const e=document.querySelector(sel);if(!e||!__C9.vis(e))return null;e.scrollIntoView({block:'nearest'});const r=e.getBoundingClientRect(),x=r.left+r.width/2;
  let t=null,b=null;for(let y=Math.floor(r.top-30);y<=Math.ceil(r.bottom+30);y++){const a=document.elementFromPoint(x,y+0.5);if(a&&(a===e||e.contains(a))){if(t===null)t=y;b=y+1}}
  let l=null,rr=null;const y0=r.top+r.height/2;for(let xx=Math.floor(r.left-20);xx<=Math.ceil(r.right+20);xx++){const a=document.elementFromPoint(xx+0.5,y0);if(a&&(a===e||e.contains(a))){if(l===null)l=xx;rr=xx+1}}
  return {vis:{w:Math.round(r.width),h:Math.round(r.height)},hit:{h:t===null?0:b-t,w:l===null?0:rr-l},coarse:matchMedia('(pointer:coarse)').matches}}"""
VPS = [('PC', {'width': 1440, 'height': 900}, False), ('폰', {'width': 390, 'height': 844}, True), ('iPad', {'width': 820, 'height': 1180}, True)]
ACCEPT = {'span.esc「C #」': 'A-2 새 「C n」(보이는 글자 = 「! K」 와 같은 꼴 · 터치 누름 높이는 ::before 36 — 아래 「누름」 칸)'}


def sweep(br, eng, app):
    out = {}
    for vn, vp, mob in VPS:
        touch = vn != 'PC'
        dv, gp = earth_dev(br, eng, app, vp=vp, mobile=mob)
        try:
            if dv.ev("()=>document.body.classList.contains('fold')&&!!document.getElementById('fFoldBtn')"):
                dv.click('#fFoldBtn')
            dv.ev("()=>__C9.gmode()"); dv.pg.wait_for_timeout(300)
            typeq(dv, W['both']); out[(vn, '근거 검색 결과')] = dv.ev(SWEEPJS, touch)
            typeq(dv, ''); dv.click('#qCnt'); out[(vn, '분포')] = dv.ev(SWEEPJS, touch)
            if touch:
                out[(vn, '누름 !')] = dv.ev(HITJS, '#esres .esdh .esb'); out[(vn, '누름 C')] = dv.ev(HITJS, '#esres .esdh .esc')
            dv.click('#esres .esdh .esc'); out[(vn, '분포 C')] = dv.ev(SWEEPJS, touch)
            _unit_rows(dv, 149); out[(vn, '목록 C')] = dv.ev(SWEEPJS, touch)
            out[(vn, '오류')] = dv.errs[:2]
        finally:
            dv.close()
    return out


def sweep_cmp(N, Bs):
    rows, newonly, acc = [], [], []
    for key in N:
        if key[1] == '오류' or key[1].startswith('누름'):
            continue
        n, b = N[key], Bs.get(key) or {}
        line = {'칸': '%s · %s' % key, '쪽 넘침': [n['docow'], b.get('docow')], '상자 넘침': [n['boxow'], b.get('boxow')]}
        for cat in ('over', 'clip', 'cover', 'small'):
            cn, cb = collections.Counter(n[cat]), collections.Counter(b.get(cat) or [])
            line[cat] = [len(n[cat]), len(b.get(cat) or [])]
            for s, k in (cn - cb).items():
                if s in cb:   # 바탕에도 있는 꼴 — 줄이 늘었을 뿐(모집단 ∪ 로 단원 줄 하나 더 등) · 수만 적는다
                    line.setdefault('같은 꼴 늘어남', []).append('%s %s +%d' % (cat, s, k)); continue
                (acc if s in ACCEPT else newonly).append({'칸': line['칸'], '종류': cat, '신호': s, '수': k, **({'까닭': ACCEPT[s]} if s in ACCEPT else {})})
        for k in ('docow', 'boxow'):
            if n[k] > (b.get(k) or 0):
                newonly.append({'칸': line['칸'], '종류': k, '신호': '%d > %d' % (n[k], b.get(k) or 0)})
        rows.append(line)
    return rows, newonly, acc


# ══════════ 돌림 ══════════
GATES = [
    ('b1', 'B-1 A-1 찾기 — 암기 절에만 있는 말 → 149 딱지 「Claude」 · Claude 조각 <mark> · 근거 줄 0 · 둘 다 걸리면 딱지 둘 · 근거에만 = 딱지 「근거」(DOM 은 바탕 + 딱지)', b1),
    ('b2', 'B-2 모집단·개수 — 분포 머리 = 근거 ∪ Claude 문항 수 · 개수 칸 「근거 N개 ▸」 = 근거 문항 수', b2),
    ('b3', 'B-3 A-2 「C n」 — n = 풀이 문항 수 · 켜면 머리 글·색 · 단원 줄 풀이 단원만 · 「N건」 0 · 「!」↔「C」 배타 · C 0 사본 회색·못 누름', b3),
    ('b4', 'B-4 A-3 상자 — 평소 「C · 암기 절 첫 줄」 · C 켬 「Claude · 암기 절 전부」(줄 수 같음) · 암기 절 없는 합성 = 첫 절 첫 줄 · 근거 없는 문항 = 근거 줄 0 · 상자 1', b4),
]


# ══════════ fix1 — ID 검색 · 본문 말 ══════════
IDQ = ['G09-46-10', 'G0946 10', 'G03-40-05']                 # B-8 지학 근거 모드 — 문항 ID(하이픈·띄어쓰기 없이도)
BODYQ = {'earth': ['심발 = 섭입만', 'G01-38-04'],            # B-9 풀이 본문 말(149 본문이 G01-38-04 를 인용)
         'phys': ['가로는 고집', '합성 암기팁 둘째 줄']}      # 물리 72 본문 · 97(합성) 본문
VIS = {'earth': {84: 'G03-40-05', 149: 'G09-46-10'}, 'phys': {72: 'PA2502'}}   # 풀이 첫 줄 머리 = 「<보이는 ID> · <해> 변리사 … · 정답 …」(착수 때 잼)


def gp_body_plain(md, vis):
    """앱 gpPlain(fix1)과 따로 지은 같은 규칙 — 글 있는 첫 줄이 제 ID 로 시작하면 떼고 · ** · # · 글머리 · --- · | 를 뺀 평문"""
    L = str(md or '').replace('\r\n', '\n').replace('\r', '\n').split('\n')
    i = next((j for j, x in enumerate(L) if x.strip()), -1)
    ns = lambda v: re.sub(r'[\s\-]+', '', str(v)).lower()
    if i >= 0 and vis and ns(re.sub(r'^[#*\s]+', '', L[i])).startswith(ns(vis)):
        L = L[i + 1:]
    t = '\n'.join(L).replace('**', '')
    t = re.sub(r'^#+\s*', '', t, flags=re.M); t = re.sub(r'^\s*-\s+', '', t, flags=re.M)
    t = re.sub(r'-{3,}', ' ', t).replace('|', ' ')
    return re.sub(r'\s+', ' ', t).strip()


def search_rows(br, eng, app, subj, queries):
    """근거 모드 검색 결과 줄(문항 · 딱지 · 근거 줄 수 · Claude 조각) · 그 줄 근거·댓글 글(딱지 기대 셈에 씀)"""
    if subj == 'earth':
        dv, gp = earth_dev(br, eng, app)
    else:
        rec, gp = rec_of(subj); dv = Dev(br, eng); dv.load(app, subj, rec)
    try:
        dv.ev("()=>__C9.gmode()"); dv.pg.wait_for_timeout(300)
        out, hay = {}, {}
        for q in queries:
            typeq(dv, q)
            out[q] = [{k: r[k] for k in ('no', 'cd', 'tags', 'gl', 'glc')} for r in dv.ev("()=>__C9.rows()")]
            for r in out[q]:
                if r['no'] not in hay:
                    hay[r['no']] = dv.ev("n=>__C9.rowHay(n)", r['no'])
        return out, gp, hay, dv.errs[:2]
    finally:
        dv.close()


def b8_check(RA, RC, gp, hay):
    """RA(새 판 · 바탕) 를 cedc251(RC) 와 맞댐 — cedc251 줄마다 근거 줄 수 같음 · 딱지 = 본문 걸림이면 「Claude」 하나 · 아니면 없음 · 조각 = 본문 걸림일 때만 · 더 걸린 줄 = 본문 걸림뿐"""
    bad = []
    for q in IDQ:
        a = {r['no']: r for r in RA.get(q, [])}; c = {r['no']: r for r in RC.get(q, [])}
        if not c:
            bad.append([q, 'cedc251 결과 0']); continue
        body = lambda no: gp_body_plain(gp.get(str(no), ''), VIS['earth'].get(no)) if str(no) in gp else ''
        for no, rc in c.items():
            ra = a.get(no)
            if not ra:
                bad.append([q, no, '줄 없음']); continue
            hitb = q.lower() in body(no).lower()
            if q.lower() in (hay.get(no) or ''):   # 근거·댓글에도 그 말 — 이 칸 잣대 밖(ID 검색에선 없음)
                bad.append([q, no, '근거·댓글에도 걸림(잣대 밖)']); continue
            if ra['gl'] != rc['gl']:
                bad.append([q, no, '근거 줄', ra['gl'], rc['gl']])
            if ra['tags'] != (['Claude'] if hitb else []):
                bad.append([q, no, '딱지', ra['tags'], ['Claude'] if hitb else []])
            if bool(ra['glc']) != hitb:
                bad.append([q, no, '조각', bool(ra['glc']), hitb])
        extra = [no for no in a if no not in c and not (q.lower() in body(no).lower())]
        if extra:
            bad.append([q, '본문 걸림 아닌데 더 걸린 줄', extra])
    return bad


def main():
    APPS['NEW'] = app_src(NEWF); APPS['BASE'] = app_src(BASEF)
    _yn = lambda a: re.search(rb'\bynUid\s*=', a) is not None   # ★ uid_unify G-1 — 앱 글에 ynUid(기출 uid 판별)가 있나 · 새 판에만 있으면 바탕 쪽 줄에서 회·번 <b> 를 뗀 뒤 맞댄다
    STRIP['BASE'] = _yn(APPS['NEW']) and not _yn(APPS['BASE']); STRIP['NEW'] = _yn(APPS['BASE']) and not _yn(APPS['NEW'])
    base_rev = BASEF
    try:
        base_rev = HU.git(GENIE, 'rev-parse', '--short', BASEF).decode().strip() or BASEF
    except Exception:
        pass
    t0 = time.time(); TIMES = []
    with sync_playwright() as pw:
        for eng in ENGS:
            br = getattr(pw, eng).launch()
            try:
                pick_words(br, eng)
                print('INFO | 표본 말 | %s' % json.dumps({k: W.get(k) for k in ('cl', 'both', 'both_own', 'gg', 'nogg_no', 'uid149')}, ensure_ascii=False), flush=True)
                for g, name, fn in GATES:
                    if not want(g):
                        continue
                    ts = time.time(); res = {}
                    for who in ('NEW', 'BASE'):
                        try:
                            res[who] = fn(br, eng, APPS[who])
                        except Exception as e:
                            res[who] = (False, 'ERR ' + repr(e)[:400])
                    if g == 'b1' and isinstance(res['NEW'][1], dict) and isinstance(res['BASE'][1], dict):
                        hn = [re.sub(r'<span class="clsrc[^"]*">[^<]*</span>', '', h) for h in res['NEW'][1].get('근거에만', {}).get('html', [])]
                        hb = [re.sub(r'<span class="clsrc[^"]*">[^<]*</span>', '', h) for h in res['BASE'][1].get('근거에만', {}).get('html', [])]   # fix1 — 바탕이 e9de3b8(딱지 있음)이어도 같은 잣대
                        # ★ uid_unify G-1 — 새 판에만 ynUid 가 있으면 옛 쪽 줄에서 지학 기출 uid 줄의 <b>NN회 N번</b> 을 뗀 뒤 맞댄다(새 판 줄에 그 <b> 가 남아 있으면 안 떼므로 여전히 FAIL)
                        if STRIP['NEW']:
                            hn = [g1_strip(h) for h in hn]
                        if STRIP['BASE']:
                            hb = [g1_strip(h) for h in hb]
                        same = hn == hb and len(hb) > 0
                        res['NEW'] = (res['NEW'][0] and same, dict(res['NEW'][1], **{'근거에만 DOM = 바탕 + 딱지': same}))
                        for v in (res['NEW'][1], res['BASE'][1]):
                            v.get('근거에만', {}).pop('html', None)
                    R(g, eng, name, res['NEW'][0], res['BASE'][0], {'NEW': res['NEW'][1], 'BASE': res['BASE'][1]})
                    TIMES.append((g, round(time.time() - ts)))
                if want('b5'):
                    ts = time.time()
                    pn, pb = b5(br, eng, APPS['NEW']), b5(br, eng, APPS['BASE'])
                    # ★ physprev(10/2 하위 에이전트 C) — _task_jagwa_physprev 57줄(A-2-3): 물리 t 로만 걸린 줄 · 조각이 t 인 줄 · 100줄 상한은 pv_same 이 가른다
                    # 옛 줄: cmp = {q: pv_same(pn.get(q), pb[q]) for q in pb}
                    def _g1(v, on):   # ★ uid_unify G-1 — 줄 HTML 에서 지학 기출 uid 줄의 <b>NN회 N번</b> 을 뗀 사본(on 이 거짓이면 그대로)
                        if not on or not isinstance(v, dict):
                            return v
                        return dict(v, rows=[[x, g1_strip(h)] for x, h in v['rows']])
                    G1_N['떼어 낸 줄'] = 0
                    cmp = {q: pv_same(_g1(pn.get(q), STRIP['NEW']), _g1(pb[q], STRIP['BASE'])) for q in pb}
                    diff = [q for q in pb if not cmp[q][0]]
                    # 옛 줄: R('b5', eng, 'B-5 기출 검색 무변 — 생물·지학·물리 말 다섯씩 · 걸린 집합 · 결과 상자 HTML = 바탕  [바탕 = 기준]', not diff and len(pb) == 15, None,
                    # 옛 줄: {'다른 말': diff, '건': {q: len((pn.get(q) or {}).get('nos') or []) for q in pn}, 'physprev': {q: v[1] for q, v in cmp.items() if v[1]}})
                    R('b5', eng, 'B-5 기출 검색 무변 — 생물·지학·물리 말 다섯씩 · 걸린 집합 · 결과 상자 HTML = 바탕  [바탕 = 기준]', not diff and len(pb) == 15, None,
                      {'다른 말': diff, '건': {q: len((pn.get(q) or {}).get('nos') or []) for q in pn}, 'physprev': {q: v[1] for q, v in cmp.items() if v[1]},
                       'G-1(지학 기출 uid 회·번 <b> 걷음만 받음 · 생물은 결정 대기)': {'갈래': STRIP, '받은 접두': G1_PFX, '뗀 줄 수': G1_N['떼어 낸 줄'], '생물 다른 말': [q for q in diff if q.startswith('bio ')]}})
                    TIMES.append(('b5', round(time.time() - ts)))
                if want('b6'):
                    ts = time.time()
                    sn, sb = sweep(br, eng, APPS['NEW']), sweep(br, eng, APPS['BASE'])
                    rows, newonly, acc = sweep_cmp(sn, sb)
                    hits = {('%s %s' % k): v for k, v in sn.items() if k[1].startswith('누름')}
                    hok = all(v and v['hit']['h'] >= 36 and v['coarse'] for v in hits.values()) and len(hits) == 4
                    errs = {k[0]: v for k, v in sn.items() if k[1] == '오류' and v}
                    R('b6', eng, 'B-6 화면 훑기 — 근거 결과·분포·분포 C·목록 C × PC 1440 · 폰 390 · iPad 820 — 새로 생긴 넘침·잘림·덮임 0 · 「!」·「C」 터치 누름 높이 ≥ 36',
                      not newonly and not errs and hok, None, {'새로 생긴 것': newonly, '뜻한 바뀜': acc, '누름': hits, '오류': errs, '표': rows})
                    TIMES.append(('b6', round(time.time() - ts)))
                if want('b8'):   # fix1 B-8 — ID 검색 = cedc251(근거 줄 · 딱지 · 조각) · 본문 걸림만 「Claude」
                    ts = time.time()
                    C0 = app_src('cedc251')
                    rn, gpn, hn, en = search_rows(br, eng, APPS['NEW'], 'earth', IDQ)
                    rb, _, hb, eb = search_rows(br, eng, APPS['BASE'], 'earth', IDQ)
                    rc, _, hc, ec = search_rows(br, eng, C0, 'earth', IDQ)
                    badn, badb = b8_check(rn, rc, gpn, {**hc, **hn}), b8_check(rb, rc, gpn, {**hc, **hb})
                    R('b8', eng, 'B-8 지학 근거 모드 「G09-46-10」·「G0946 10」·「G03-40-05」 → 결과 줄·근거 줄·딱지 = cedc251(근거 줄 1 · 본문에 없으면 딱지·조각 0)',
                      not badn and not en, not badb, {'틀린 것(새)': badn, '틀린 것(바탕)': badb, '새': rn, '바탕': rb, 'cedc251': rc,
                                                   '본문 걸림(머리 뗀 풀이 글)': {q: [no for no in VIS['earth'] if q.lower() in gp_body_plain(gpn.get(str(no), ''), VIS['earth'][no]).lower()] for q in IDQ},
                                                   '머리 줄': {no: str(gpn.get(str(no), '')).split('\n')[0][:60] for no in VIS['earth']}})
                    TIMES.append(('b8', round(time.time() - ts)))
                if want('b9'):   # fix1 B-9 — 풀이 본문 말 = e9de3b8 그대로(지학 · 물리 72 · 97)
                    ts = time.time()
                    E9 = app_src('e9de3b8')
                    out, ok9 = {}, True
                    for subj in ('earth', 'phys'):
                        rn, gpn, _, en = search_rows(br, eng, APPS['NEW'], subj, BODYQ[subj])
                        re9, _, _, _ = search_rows(br, eng, E9, subj, BODYQ[subj])
                        nm = lambda X: {q: sorted([r['no'], r['tags'], r['gl'], bool(r['glc'])] for r in X[q]) for q in X}
                        hit = {q: [r for r in rn[q] if 'Claude' in r['tags'] and r['glc']] for q in rn}
                        oks = nm(rn) == nm(re9) and all(hit[q] for q in rn) and not en
                        out[subj] = {'새': rn, 'e9de3b8': re9, '같음': nm(rn) == nm(re9), '조각 글 같음': {q: [r['glc'] for r in rn[q]] == [r['glc'] for r in re9[q]] for q in rn}}
                        ok9 = ok9 and oks
                    R('b9', eng, 'B-9 풀이 본문 말(「심발 = 섭입만」 · 「G01-38-04」 · 물리 72 · 97 본문 말) → 결과 줄·딱지·근거 줄·조각 = e9de3b8  [바탕 = 기준]', ok9, None, out)
                    TIMES.append(('b9', round(time.time() - ts)))
            finally:
                br.close()
    npass = sum(1 for r in ROWS if r[3]); nfail = sum(1 for r in ROWS if not r[3])
    vac = [r for r in ROWS if r[4] is True and '기준' not in r[2]]
    print('\n== PASS %d · FAIL %d · 헛잣대(바탕도 PASS · 기준 칸 밖) %d · %.0f초 · 단계 초 %s' % (npass, nfail, len(vac), time.time() - t0, TIMES))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · jagwa_search_claude · NEW %s · 바탕 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), os.path.basename(NEWF), base_rev, ','.join(ENGS)))
        f.write('INFO | 표본 말 | %s\n' % json.dumps({k: W.get(k) for k in ('cl', 'both', 'both_own', 'gg', 'nogg_no', 'uid149')}, ensure_ascii=False))
        for g, eng, n, okn, okb, v in ROWS:
            f.write('%s | 바탕 %s | %s · %s · %s | %s\n' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, eng, n,
                    (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str))[:40000]))
        f.write('== PASS %d · FAIL %d · 헛잣대 %d · 단계 초 %s\n' % (npass, nfail, len(vac), TIMES))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
