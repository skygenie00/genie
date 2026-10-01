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
 unionN(){return DATA.filter(r=>!isC(r)&&(ggOf(GGU(r)).length>0||!!(GP[r[F.NO]]))).length},
 ggHay(){return DATA.filter(r=>!isC(r)).map(r=>ggOf(GGU(r)).map(g=>ggFlat(g)+' '+(g.cs||[]).map(c=>c.t).join(' ')).join(' ')+' '+GGU(r)+' '+codeShow(r)).join(' ').toLowerCase()},
 rowHay(no){const r=DATA[no-1];return r?ggOf(GGU(r)).map(g=>ggFlat(g)+' '+(g.cs||[]).map(c=>c.t).join(' ')).join(' ').toLowerCase():''},
 uidOf(no){const r=DATA[no-1];return r?GGU(r):''},
 noGg(){const r=DATA.find(x=>!isC(x)&&!ggOf(GGU(x)).length&&!GP[x[F.NO]]);return r?r[F.NO]:0}
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
                res['%s %s' % (subj, q)] = [dv.ev("()=>ES_NOS.slice()"), dv.ev("()=>(document.getElementById('esres')||{}).innerHTML||''")]
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


def main():
    APPS['NEW'] = app_src(NEWF); APPS['BASE'] = app_src(BASEF)
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
                        hb = res['BASE'][1].get('근거에만', {}).get('html', [])
                        same = hn == hb and len(hb) > 0
                        res['NEW'] = (res['NEW'][0] and same, dict(res['NEW'][1], **{'근거에만 DOM = 바탕 + 딱지': same}))
                        for v in (res['NEW'][1], res['BASE'][1]):
                            v.get('근거에만', {}).pop('html', None)
                    R(g, eng, name, res['NEW'][0], res['BASE'][0], {'NEW': res['NEW'][1], 'BASE': res['BASE'][1]})
                    TIMES.append((g, round(time.time() - ts)))
                if want('b5'):
                    ts = time.time()
                    pn, pb = b5(br, eng, APPS['NEW']), b5(br, eng, APPS['BASE'])
                    diff = [q for q in pb if pn.get(q) != pb[q]]
                    R('b5', eng, 'B-5 기출 검색 무변 — 생물·지학·물리 말 다섯씩 · 걸린 집합 · 결과 상자 HTML = 바탕  [바탕 = 기준]', not diff and len(pb) == 15, None,
                      {'다른 말': diff, '건': {q: len(pn[q][0]) for q in pn}})
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
