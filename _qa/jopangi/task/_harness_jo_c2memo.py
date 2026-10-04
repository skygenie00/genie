# -*- coding: utf-8 -*-
r"""_task_jo_c2memo §B 관문 — 2차 보드 줄(기출·GS)·사례 격자 칸 머리에 메모 칩 「🗒 N 사람」 → 메모 목록 → 전문

  python _harness_jo_c2memo.py [--new <앱>] [--base <앱 파일 | git rev>] [--eng chromium,webkit] [--only b1,b2,...] [--res <결과>]

  NEW = genie 작업트리 jo/index.html · BASE(헛잣대) = 착수 때 HEAD(기본 HEAD — 이 판을 커밋한 뒤에는 --base cedc251)
  데이터 = genie jo/data(실물 · 같은 출처) · 원격 기록(GitHub) = 404(밖으로 안 나감 · 기록 쓰기 0)
  B-0 합성 포스트잇 = localStorage jopangi.postit 주입(실제 기록 0) — 민소 기출 13-50-2 햄찌 1·꼬까 1 · 13-50-3 「미상」 1 · 특허 GS 카드 하나 햄찌 1 · 특허 사례 카드 하나 꼬까 1
  창 = PC 1440×900(마우스) · 아이패드 834×1194(터치) · 폰 390×844(터치)
  2차 보드 띄우기 = _harness_jo_hrail_list 와 같은 길(S.law · S.tab='cha2' · S.boardKind → render)
  ★ fix8(10/4 · ⑧ _task_jo_2cha_minso_board 뒤 옛 잣대 고침 · 결정로그 10/3 22:36 지시서) — B-0 13-50-2 두 칸 = 보드 본문에 보이는 제목 줄 낱말 · at = ISO ·
    b2 · b3 = 메모 창(목록 창 없음 A-6-2 · POPS 밖 A-7-6) · b4 누를 자리 = 코드 숫자(A-4-3 · A-5-3) · b10 = 메모 창 장면 · board() = 앱 render 잠금(busy) 풀릴 때까지 기다림(흔들림)
  ★ yard8(10/4 · ⑧ 합친 뒤) — fix8(3ce19765)을 qa_slim 꼴(fec856e0) 위에 다시 얹음: gate 갈래 = fix8 그대로 · regress 갈래(b2 · b3 · b4 · b10) = 같은 뜻의 ⑧ 뒤 길 앱 표지 기다림
    (칩 누름 → 메모 창 .pop.mpop.mb 가 문제 메모 수만큼 뜸 / 같은 칩 다시 → 0 / 코드 숫자 누름 → 카드 팝업 cell|🧾) · b5 · b6 웹킷 = 흔들림(_qa_flaky.json 10/4 00:34 · 다시 돌려 PASS) — 고치지 않음
"""
import os as _os_r, sys as _sys_r
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402 — _task_qa_slim(10/4) 실행 모드: --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같다) · 새 갈래는 모두 `if QJ.REGRESS:` / `if QJ.GATE:` 안
import http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse, collections
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = _roots.genie()
HERE = os.path.dirname(os.path.abspath(__file__))
NEWF = ARG('--new', os.path.join(GENIE, 'jo', 'index.html'))
BASEF = ARG('--base', 'HEAD')
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
if QJ.SMOKE:   # smoke: Chromium PC 만(smoke 칸 = b1 · b2)
    ENGS = [x for x in ENGS if x == 'chromium']
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_c2memo_result.txt'))
WORK = os.path.join(tempfile.gettempdir(), 'h_jo_c2memo')
JOD = os.path.join(GENIE, 'jo')
SEP = '\u001f'
ROWS = []
APPS = {}
SERVERS = {}


def R(g, eng, name, okn, okb, val):
    ROWS.append((g, eng, name, okn, okb, val))
    print('%s | 바탕 %s | %s · %s · %s | %s' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, eng, name,
          (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str))[:700]), flush=True)


def git(*a):
    return subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def app_src(x):
    if os.path.isfile(x):
        return open(x, 'rb').read().decode('utf-8').replace('\r\n', '\n')
    return git('show', '%s:jo/index.html' % x).decode('utf-8').replace('\r\n', '\n')


# ── B-0 합성 포스트잇(카드 이름은 jo/data/2cha_보드.json 에서) ──
def cards():
    b = json.load(open(os.path.join(JOD, 'data', '2cha_보드.json'), encoding='utf-8'))
    def first(ks):   # 격자 칸이 있는 첫 보드의 첫 카드 → (보드 열쇠, 파일) · 특허 GS 는 데이터에 보드가 없다(「폴더 없음」) — 있는 GS 로
        for k in ks:
            g = (b.get(k) or {}).get('격자') or {}
            for kk in sorted(g):
                for c in g[kk]:
                    f = c.get('파일') if isinstance(c, dict) else None
                    if f:
                        return k, f
            for c in ((b.get(k) or {}).get('미배치') or []):   # 사례 보드(「목록」)는 카드가 미배치 쪽에 있다
                f = c.get('파일') if isinstance(c, dict) else None
                if f:
                    return k, f
        return None, None
    gk, gf = first(['GS|특허', 'GS|민소', 'GS|상표'])
    sk, sf = first(['사례|특허', '사례|민소', '사례|상표'])
    LAW = {'특허': '특허법', '민소': '민사소송법', '상표': '상표법', '디보': '디자인보호법'}
    return {'ms': ['민기출 13-50-1', '민기출 13-50-2-사물관할', '민기출 13-50-3', '민기출 13-50-4-소송중사망,독당참'],
            'gs': gf, 'gs_law': LAW.get((gk or '|').split('|')[1]), 'gs_board': gk, 'sa': sf, 'sa_law': LAW.get((sk or '|').split('|')[1]), 'sa_board': sk}


def fixture(C):
    k = lambda tk, st, wi, w: tk + SEP + str(st) + SEP + str(wi) + SEP + w
    ms2 = 'card|기출|' + C['ms'][1]
    return {
        # 옛(fix8 전): k(ms2, 0, 3, '설문(1)'): {… 'who': '햄찌', 'at': '0', …} · k(ms2, 2, 7, '관할'): {… 'who': '꼬까', 'at': '0', …} — 행 0 = ⑦ 문제 줄(보드 본문에서 뺌) · 행 2 「1. 문제의 소재」엔 '관할' 없음(고아)
        k(ms2, 1, 2, '설문(1)'): {'t': '합성 햄찌 메모 — 설문(1) 사물관할은 지방법원 합의부부터 따져 본다(검산용 글 · 실제 기록 아님)', 'who': '햄찌', 'at': '2026-10-01T03:24:00.000Z', 'ts': '2026-10-01T03:24:00.000Z'},   # ★ fix8 — 행 1 「Ⅰ. 설문(1) (12점)」 · ⑧ A-4-4(보드 본문 ⑦ 뺌) · A-7-1·2(메모 창 = 보이는 낱말마다) · A-7-7(.mmeta 시각 = at) · 결정로그 10/3 22:36
        k(ms2, 3, 4, '이송'): {'t': '합성 꼬까 메모 — 관할 위반 이송 결정의 구속력(검산용)', 'who': '꼬까', 'at': '2026-10-01T03:30:00.000Z', 'ts': '2026-10-01T03:30:00.000Z'},   # ★ fix8 — 행 3 「2. 제34조 이송 가부」(pitWire 는 같은 줄에서만 낱말을 찾는다) · 근거 위와 같음
        k('card|기출|' + C['ms'][2], 0, 1, '청구'): {'t': '합성 메모 — 붙인 사람 없음(검산용)', 'at': '0', 'ts': '2026-09-30T01:00:00.000Z'},
        k('card|GS|' + C['gs'], 0, 2, '특허'): {'t': '합성 햄찌 메모 — 특허 GS(검산용)', 'who': '햄찌', 'at': '0', 'ts': '2026-09-30T02:00:00.000Z'},
        k('card|사례|' + C['sa'], 0, 2, '사례'): {'t': '합성 꼬까 메모 — 특허 사례(검산용)', 'who': '꼬까', 'at': '0', 'ts': '2026-09-30T03:00:00.000Z'},
    }


SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.alert=function(){};window.confirm=function(){return true;};window.prompt=function(){return null;};
(function(){var nf=window.fetch.bind(window);
window.fetch=function(u,o){o=o||{};var s=String((u&&u.url)||u);
 if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));
 return nf(u,o);};
try{localStorage.clear();}catch(e){}
try{localStorage.setItem('tt.cfg',JSON.stringify({token:'harness-token',person:'꼬까'}));}catch(e){}
try{if(window.name&&window.name.indexOf('PIT:')===0)localStorage.setItem('jopangi.postit',window.name.slice(4));}catch(e){}
})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
</script>"""


def serve(tag, src):
    if tag in SERVERS:
        return SERVERS[tag][1]
    out = os.path.join(WORK, 'srv_' + tag); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    b = src.index('<body'); bb = src.index('>', b) + 1
    io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n').write(src[:bb] + SEED + src[bb:])

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=out, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            if p.startswith('/data/'):
                return os.path.join(JOD, 'data', p[6:].replace('/', os.sep))
            if p in ('/index.html', '/'):
                return super().translate_path(path)
            f = os.path.join(JOD, p.lstrip('/').replace('/', os.sep))
            return f if os.path.exists(f) else super().translate_path(path)

        def log_message(self, *a, **k):
            pass
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


J = r"""
window.__CM={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 R(e){if(!e)return null;const r=e.getBoundingClientRect();return {l:Math.round(r.left*10)/10,t:Math.round(r.top*10)/10,w:Math.round(r.width*10)/10,h:Math.round(r.height*10)/10,r:Math.round(r.right*10)/10,b:Math.round(r.bottom*10)/10}},
 wrap(){if(window.__hw)return;window.__hw=1;   /* 하네스만 — 줄·칸에 카드 파일 이름 표(data-hfile) · 앱 동작 무변 */
   const r0=window.c2RowEl,c0=window.c2CellEl;window.c2RowEl=function(c){const e=r0.apply(this,arguments);try{e.dataset.hfile=c.file}catch(_){}return e};
   window.c2CellEl=function(c){const e=c0.apply(this,arguments);try{e.dataset.hfile=c.file}catch(_){}return e}},
 /* 옛(fix8 전): async board(law,kind){__CM.wrap();closeAllPops&&closeAllPops(true);S.law=law;S.tab='cha2';S.boardKind=kind;S.series='';S.yearFilter='';await render();await new Promise(r=>setTimeout(r,900)); */
 async board(law,kind){__CM.wrap();await __CM.idle();closeAllPops&&closeAllPops(true);S.law=law;S.tab='cha2';S.boardKind=kind;S.series='';S.yearFilter='';
   for(let k=0;k<3;k++){await __CM.idle();await render();await __CM.idle();if(__CM.on2(kind))break}   /* ★ fix8 — 앱 render(){if(busy)return;}(jo/index.html 17157 · cedc251·e21d368 도 같은 줄) = 부팅·다른 render 가 돌면 이 render 가 조용히 건너뜀 → 10/4 00:21·00:27 실행 b5·b6·b7 · 바탕 b4 「첫 보드 안 그려짐」 흔들림 · 잠금이 풀릴 때까지 기다리고 그 갈래 2차 보드가 아니면 다시(⑧ tests.js idle() 꼴) */
   await new Promise(r=>setTimeout(r,900));
   const m=document.querySelector('#slot .main');if(m){for(let i=0;i<40;i++){m.scrollTop=m.scrollHeight*i/40;await new Promise(r=>setTimeout(r,25))}m.scrollTop=0}return document.querySelectorAll('#slot .c2row,#slot .cell').length},
 rowOf(f){return [...document.querySelectorAll('#slot .c2row[data-hfile]')].find(r=>r.dataset.hfile===f&&!r.dataset.ckx)||null},
 cellOf(f){return [...document.querySelectorAll('#slot .cell[data-hfile]:not(.c2row)')].find(c=>c.dataset.hfile===f)||null},
 kids(r){const t=r&&(r.querySelector('.c2t1')||r.querySelector('.chd'));return t?[...t.children].map(e=>({cls:String(e.className),t:__CM.tx(e).slice(0,30)})):null},
 chip(r){const c=r&&r.querySelector('.chip.c-memo');return c?{t:__CM.tx(c),who:[...c.querySelectorAll('.who')].map(__CM.tx),unk:c.querySelectorAll('.who.unk').length,r:__CM.R(c)}:null},
 pops(){return (typeof POPS!=='undefined'?POPS:[]).filter(p=>p.isConnected).map(p=>({k:p._pk,t:__CM.tx(p.querySelector('.pt')),rows:[...p.querySelectorAll('.pb .res')].map(__CM.tx),body:__CM.tx(p.querySelector('.pb')).slice(0,200),badge:[...p.querySelectorAll('.pb .badge')].map(__CM.tx)}))},
 at(e){if(!e)return null;try{e.scrollIntoView({block:'center',inline:'nearest'})}catch(_){}const r=e.getBoundingClientRect();return {cx:r.left+r.width/2,cy:r.top+r.height/2,r:__CM.R(e)}},
 idle:async()=>{for(let i=0;i<600;i++){let b=false;try{b=!!busy}catch(_){}if(!b)return true;await new Promise(r=>setTimeout(r,25))}return false},   /* ★ fix8 — 앱 render 잠금(let busy) 풀림 기다림 */
 on2(kind){const P=[...document.querySelectorAll('#slot .pill')].map(__CM.tx);return S.tab==='cha2'&&P.some(t=>t.indexOf('사례')===0)&&[...document.querySelectorAll('#slot .pill.on')].some(b=>__CM.tx(b).indexOf(kind)===0)},   /* ★ fix8 — 지금 #slot 이 그 갈래 2차 보드인가 */
 mpops(){return [...document.querySelectorAll('.pop.mpop')].map(p=>({mode:p.classList.contains('mb')?'b':'c',t:__CM.tx(p.querySelector('.ph .pt')),text:__CM.tx(p.querySelector('.mtext')),meta:__CM.tx(p.querySelector('.mmeta')),r:__CM.R(p)}))},   /* ★ fix8 — ⑧ 메모 창(POPS 밖 · A-7-6) */
 bodyOf(f){const r=__CM.rowOf(f);return !!(r&&r.querySelector('.c2bw'))},   /* ★ fix8 — 그 줄 본문 펴짐(⑧ A-4 · A-6-2) */
 fmt(ts){try{return pitFmt(ts)}catch(_){return ''}},   /* ★ fix8 — 메모 창 시각 꼴(앱 pitFmt · 이 PC 시간대 그대로) */
 codeAt(f){const r=__CM.rowOf(f),c=r&&r.querySelector('.c2code');if(!c)return null;try{c.scrollIntoView({block:'center',inline:'nearest'})}catch(_){}const t=c.firstChild;if(t&&t.nodeType===3){const g=document.createRange();g.selectNodeContents(t);const b=g.getBoundingClientRect();return {cx:b.left+b.width/2,cy:b.top+b.height/2,r:__CM.R(c)}}return __CM.at(c)},   /* ★ fix8 — 코드 숫자 글 가운데(두루마리 .c2q1 비킴 · ⑧ A-5-3) */
 errs(){return (window.__ERR||[]).slice(0,6)}
};
"""


class P:
    def __init__(self, br, eng, tag, src, vp, touch, pit):
        self.eng, self.touch, self.vp = eng, touch, vp
        port = serve(tag, src)
        self.ctx = br.new_context(viewport=vp, device_scale_factor=1, is_mobile=bool(touch and eng == 'chromium'), has_touch=True)
        self.ctx.route('**/*', lambda rt: rt.continue_() if rt.request.url.startswith('http://127.0.0.1') else rt.abort())
        self.ctx.add_init_script('window.name=%s;' % json.dumps('PIT:' + json.dumps(pit, ensure_ascii=False)))
        self.pg = self.ctx.new_page(); self.pg.set_default_timeout(120000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append(str(e)[:200]))
        self.pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load')
        self.pg.wait_for_function("typeof render==='function'&&typeof popCard4==='function'&&typeof S==='object'", timeout=90000)
        self.pg.wait_for_timeout(1500)
        self.pg.evaluate(J)
        self.cdp = self.ctx.new_cdp_session(self.pg) if eng == 'chromium' else None

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def tap(self, at, wait=600):
        if not at:
            return False
        x, y = at['cx'], at['cy']
        if not self.touch:
            self.pg.mouse.click(x, y)
        elif self.cdp:
            pt = {'x': x, 'y': y, 'radiusX': 11, 'radiusY': 11, 'force': 1, 'id': 1}
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [pt]}); self.pg.wait_for_timeout(50)
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        else:
            self.pg.touchscreen.tap(x, y)
        self.pg.wait_for_timeout(wait)
        return True

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


VPS = {'PC': ({'width': 1440, 'height': 900}, False), 'iPad': ({'width': 834, 'height': 1194}, True), '폰': ({'width': 390, 'height': 844}, True)}


def page(br, eng, who, dn='PC'):
    vp, touch = VPS[dn]
    if QJ.REGRESS:   # A-2: (엔진 × 화면) 마다 앱 한 번 — 칸 사이는 reset(아래 RigP) · gate 는 칸마다 새 컨텍스트(P) 그대로
        return RIG.lease(br, eng, dn)
    QJ.launch('base' if who == 'BASE' else 'new')
    return P(br, eng, who + '_' + dn, APPS[who], vp, touch, PIT)


C = {}
PIT = {}

# ══════════ _task_qa_slim A-2 — regress: (엔진 × 화면) 마다 앱을 한 번 띄우고 칸 사이는 reset 으로 되돌려 잇는다 ══════════
# (gate 는 page() 의 P 그대로 — 칸마다 새 컨텍스트 · 고정 대기 그대로) · 쓴 표지 목록 = _qa_slim_out/_a2/_harness_jo_c2memo_표지.md
T_BOOT, T_UP = 30000, 6000   # 앱 표지 기다림 상한(ms) — 안 오면 until 이 False 로 돌아오고 칸은 그대로 읽어 FAIL 로 나온다(원본과 같은 모양)
JS_BOOT = ("()=>{const ns=[...document.querySelectorAll('#hrail b[data-n]')];"
           "return typeof busy!=='undefined'&&!busy&&ns.length>0&&ns.every(n=>String(n.textContent||'').trim()!=='')}")   # 첫 render 끝(busy 꺼짐 · 앱 16561) + 머리 탭 수 다 참(railCounts 끝 · 앱 2146–2173)
JS_IDLE = "()=>typeof busy!=='undefined'&&!busy"                                                             # render 끝(busy 꺼짐)
JS_POP_OPEN = "k=>!!POPS.find(p=>p.isConnected&&p._pk===k)"                                                  # 그 키의 팝업이 떠 있다(앱 popShell · popToggle 3197)
JS_POP_GONE = "k=>!POPS.find(p=>p.isConnected&&p._pk===k)"                                                   # 같은 칩 다시 = 닫힘(앱 popToggle)
JS_LIST_ROWS = ("()=>{const p=POPS.find(x=>x.isConnected&&x._pk&&String(x._pk).indexOf('pitlist|card|')===0);"
                "return !!p&&p.querySelectorAll('.pb .res').length>0}")                                       # 메모 목록 창 + 줄(.pb .res)이 참(앱 popPitListOf 8240 — 줄은 만들 때 한 번에 찬다)
JS_FULL_OPEN = (r"()=>!!POPS.find(p=>{const t=p.querySelector('.pt');"
                r"return p.isConnected&&!!t&&String(t.textContent||'').replace(/\s+/g,' ').trim().indexOf('🗒 포스트잇')===0})")   # 전문 창(제목 「🗒 포스트잇 …」)
JS_CARD_OPEN = "()=>!!POPS.find(p=>p.isConnected&&String(p._pk||'').indexOf('cell|🧾')===0)"                  # 카드 팝업 키(앱 popCard4 — 제목에 카드 이름)
# ★ yard8 — ⑧ 뒤 길 표지(위 JS_POP_OPEN · JS_POP_GONE · JS_LIST_ROWS 는 ⑧ 전 길 — 지우지 않고 둔다 · 목록 창 쪽 칸은 ⑧ 뒤 쓰지 않는다)
JS_MEMO_N = "n=>document.querySelectorAll('.pop.mpop.mb').length>=n"                                           # 보드 메모 창(.pop.mpop.mb · POPS 밖 · 앱 c2MemoWin 9530)이 n 개 이상 — render 끝 훅 c2AfterRender(setTimeout 0)가 c2MemoBoard 로 놓는다(앱 17222 · 9614)
JS_MEMO_NONE = "()=>!document.querySelector('.pop.mpop.mb')"                                                      # 같은 칩 다시 = 그 문제 메모 창 전부 닫힘(앱 c2MemoChipTog 9515 — render 없이 바로 지움)
JS_MEMO_TITLE = (r"t=>!![...document.querySelectorAll('.pop.mpop.mb .ph .pt')].find(x=>String(x.textContent||'').replace(/\s+/g,' ').trim()===t)")   # 메모 창 제목 「🗒 13-50-2 「설문(1)」」(앱 c2MemoWin 9533)
J_R = r"""
window.__RC={
 /* 두 프레임 + 안전 타이머 — 앱 showPop 다음 틱 vvFit · ResizeObserver → hdrFit 이 한 번 돈 뒤에 재기 */
 frames(){return new Promise(res=>{let d=false;const f=()=>{if(!d){d=true;res(true)}};try{requestAnimationFrame(()=>requestAnimationFrame(f))}catch(_){f()}setTimeout(f,300)})},
 railDone(){const ns=[...document.querySelectorAll('#hrail b[data-n]')];return typeof busy!=='undefined'&&!busy&&ns.length>0&&ns.every(n=>String(n.textContent||'').trim()!=='')},
 /* 앱 상태 S 첫 기록(부팅 끝 직후) — reset 이 이 값으로 되돌린다(JSON 으로 못 적는 값은 건드리지 않는다) */
 snap(){const o={};for(const k of Object.keys(S)){let v;try{v=JSON.stringify(S[k])}catch(e){v=undefined}o[k]=(typeof v==='string')?v:null}window.__S0=o;return Object.keys(o).length},
 /* 칸 사이 되돌림 — 팝업 닫기 · render 끝 · S 첫 값 · 굴림 0 · 합성 포스트잇(SEED 와 같은 첫 상태) · 메모 캐시 비움 · 오류 목록 */
 async reset(pit){
   try{closeAllPops&&closeAllPops(true)}catch(e){}
   try{for(let i=0;i<320&&busy;i++)await new Promise(r=>setTimeout(r,25))}catch(e){}
   try{const o=window.__S0;if(o){for(const k of Object.keys(S)){if(!(k in o))delete S[k]}for(const k of Object.keys(o)){if(o[k]!==null){try{S[k]=JSON.parse(o[k])}catch(e){}}}}}catch(e){}
   try{document.querySelectorAll('#slot .main,#slot .tree,#slot .plist').forEach(n=>{n.scrollTop=0});window.scrollTo(0,0)}catch(e){}
   try{localStorage.setItem('jopangi.postit',JSON.stringify(pit))}catch(e){}
   try{recDropCache()}catch(e){}
   try{if(window.__ERR)window.__ERR.length=0}catch(e){}
   return true}
};
/* __CM.board — render 뒤 고정 900ms + 40단계×25ms 굴림 대신 앱 표지(busy 꺼짐 · 머리 탭 수 다 참) — 기출·GS 목록(c2ListEl)·사례 격자 칸 머리는 render 안에서 한 번에 지어진다(앱 9014 · 9273: 느린 것은 본문 lazy 뿐) */
__CM.board=async function(law,kind){__CM.wrap();closeAllPops&&closeAllPops(true);
  const idle=async()=>{for(let i=0;i<320&&busy;i++)await new Promise(r=>setTimeout(r,25))};
  await idle();S.law=law;S.tab='cha2';S.boardKind=kind;S.series='';S.yearFilter='';await render();await idle();
  for(let i=0;i<160&&!__RC.railDone();i++)await new Promise(r=>setTimeout(r,25));
  const m=document.querySelector('#slot .main');if(m)m.scrollTop=0;
  return document.querySelectorAll('#slot .c2row,#slot .cell').length};
0;   /* 마지막 값이 함수면 Playwright evaluate 가 그 함수를 불러 버린다 — 함수 아닌 값으로 끝낸다 */
"""


class RigP(P):
    """regress 전용 — P 와 같은 맥락(서버 · 화면 · route · 합성 기록 · goto · READY)을 한 번만 만들고 칸 사이는 reset 으로 되돌려 쓴다.
    P 와 다른 점 둘 — ① 끝의 고정 1.5초 → 앱 표지(첫 render 끝 + 머리 탭 수 다 참) ② close() = 닫지 않고 되돌림(진짜 닫기는 shut)"""

    def __init__(self, br, eng, tag, src, vp, touch, pit):
        self.eng, self.touch, self.vp = eng, touch, vp
        self.dead = False
        port = serve(tag, src)
        self.ctx = br.new_context(viewport=vp, device_scale_factor=1, is_mobile=bool(touch and eng == 'chromium'), has_touch=True)
        self.ctx.route('**/*', lambda rt: rt.continue_() if rt.request.url.startswith('http://127.0.0.1') else rt.abort())
        self.ctx.add_init_script('window.name=%s;' % json.dumps('PIT:' + json.dumps(pit, ensure_ascii=False)))
        self.pg = self.ctx.new_page(); self.pg.set_default_timeout(120000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append(str(e)[:200]))
        self.pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load')
        self.pg.wait_for_function("typeof render==='function'&&typeof popCard4==='function'&&typeof S==='object'", timeout=90000)
        QJ.until(self.pg, JS_BOOT, T_BOOT, '앱 첫 render 끝(busy 꺼짐) + 머리 탭 수 다 참(railCounts 끝)')   # P 의 고정 1.5초 자리
        self.pg.evaluate(J)
        self.pg.evaluate(J_R)
        self.pg.evaluate("()=>__RC.snap()")
        self.cdp = self.ctx.new_cdp_session(self.pg) if eng == 'chromium' else None

    def press(self, at):
        """P.tap 에서 누르기만(뒤 고정 대기 없음)"""
        x, y = at['cx'], at['cy']
        if not self.touch:
            self.pg.mouse.click(x, y)
        elif self.cdp:
            pt = {'x': x, 'y': y, 'radiusX': 11, 'radiusY': 11, 'force': 1, 'id': 1}
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [pt]})
            QJ.sleep(50, 'CDP 터치 누름 길이(손가락이 닿아 있는 시간 — 앱 표지가 아니라 입력 모양)', page=self.pg)
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        else:
            self.pg.touchscreen.tap(x, y)

    def reset(self):
        try:
            self.pg.evaluate("p=>__RC.reset(p)", PIT)
            self.errs[:] = []
        except Exception:
            self.dead = True

    def close(self):
        """관문 함수들의 finally: q.close() — 닫지 않고 되돌린다"""
        self.reset()

    def shut(self):
        P.close(self)


class Rig(object):
    """regress — (엔진, 화면) 마다 RigP 하나"""

    def __init__(self):
        self.pool = {}

    def lease(self, br, eng, dn):
        key = (eng, dn)
        q = self.pool.get(key)
        if q is not None and (q.dead or q.pg.is_closed()):
            self.pool.pop(key, None)
            try:
                q.shut()
            except Exception:
                pass
            q = None
        if q is None:
            vp, touch = VPS[dn]
            QJ.launch('new')
            q = RigP(br, eng, 'NEW_' + dn, APPS['NEW'], vp, touch, PIT)
            self.pool[key] = q
        return q

    def shut(self):
        for q in list(self.pool.values()):
            try:
                q.shut()
            except Exception:
                pass
        self.pool.clear()


RIG = Rig()


def rtap(q, at, js, arg, what):
    """regress 누르기 — 누른 뒤 고정 wait 대신 앱 표지(js)가 참이 될 때까지(+ 두 프레임) · gate 는 호출 자리의 `q.tap(at, wait)` 그대로(원본 줄)"""
    if not at:
        return False
    q.press(at)
    QJ.until(q.pg, js, T_UP, what, arg)
    q.ev("()=>__RC.frames()")
    return True



def g1(br, eng, who):
    q = page(br, eng, who)
    try:
        q.ev("()=>__CM.board('민사소송법','기출')")
        out = {}
        for i, f in enumerate(C['ms']):
            r = "t=>__CM.rowOf(t)"
            out[f] = {'칩': q.ev("t=>__CM.chip(__CM.rowOf(t))", f), '차례': q.ev("t=>__CM.kids(__CM.rowOf(t))", f)}
        k2 = out[C['ms'][1]]['차례'] or []
        cls = [x['cls'] for x in k2]
        ix = lambda pred: next((i for i, c in enumerate(cls) if pred(c)), -1)
        iscore, imemo = ix(lambda c: 'c-score' in c), ix(lambda c: 'c-memo' in c)
        ipdf = ix(lambda c: 'c-pdf' in c)
        c2 = out[C['ms'][1]]['칩'] or {}; c3 = out[C['ms'][2]]['칩'] or {}
        ok = (c2.get('t', '').startswith('🗒 2') and c2.get('who') == ['햄찌', '꼬까'] and 0 < iscore < imemo and (ipdf < 0 or imemo < ipdf)
              and out[C['ms'][0]]['칩'] is None and out[C['ms'][3]]['칩'] is None and c3.get('t', '').startswith('🗒 1') and c3.get('who') == ['미상'] and c3.get('unk') == 1
              and (k2[iscore]['t'] if iscore >= 0 else '') == '미채점')
        return ok, {'13-50-2 차례': [x['t'] for x in k2], '칩': {f[4:12]: out[f]['칩'] and {'t': out[f]['칩']['t'], 'who': out[f]['칩']['who']} for f in C['ms']}, '오류': q.errs[:2] + q.ev("()=>__CM.errs()")}
    finally:
        q.close()


def g2(br, eng, who):
    q = page(br, eng, who)
    try:
        q.ev("()=>__CM.board('민사소송법','기출')")
        at = q.ev("t=>__CM.at(__CM.rowOf(t)&&__CM.rowOf(t).querySelector('.chip.c-memo'))", C['ms'][1])
        n_memo = len([k for k in PIT if k.startswith('card|기출|' + C['ms'][1] + SEP)])   # ★ yard8 — 그 문제 메모 수(합성 기록 · 2) = 뜰 메모 창 수
        if QJ.GATE:
            q.tap(at)
        else:   # regress(★ fix8 — ⑧ 뒤 길): 칩 누름 → 목록 창(pitlist · POPS) 대신 그 문제 메모 창 전부(.pop.mpop.mb · POPS 밖)가 .main 안에 놓임 — 앱 표지 = 그 창이 문제 메모 수(2)만큼 뜸(앱 c2MemoChipTog → render → c2AfterRender → c2MemoBoard 9615 · ⑧ A-6-2 · A-7-6 · 사용자 10/3 09:19)
            rtap(q, at, JS_MEMO_N, n_memo, '메모 칩 누름 → 메모 창(.pop.mpop.mb) %d 개' % n_memo)
        p1 = q.ev("()=>__CM.pops()")
        m1, b1 = q.ev("()=>__CM.mpops()"), q.ev("t=>__CM.bodyOf(t)", C['ms'][1])   # ★ fix8 — ⑧ 메모 창(POPS 밖) · 본문 펴짐
        key = 'pitlist|card|기출|' + C['ms'][1]
        if QJ.GATE:
            q.tap(q.ev("t=>__CM.at(__CM.rowOf(t)&&__CM.rowOf(t).querySelector('.chip.c-memo'))", C['ms'][1]))
        else:   # regress(★ fix8 — ⑧ 뒤 길): 같은 칩 다시 = 그 문제 메모 창 전부 닫힘(앱 c2MemoChipTog 가 바로 지움 — render 없음) · 옛 길(popToggle 로 목록 창 닫힘) 표지는 JS_POP_GONE
            rtap(q, q.ev("t=>__CM.at(__CM.rowOf(t)&&__CM.rowOf(t).querySelector('.chip.c-memo'))", C['ms'][1]), JS_MEMO_NONE, None, '같은 칩 다시 누름 = 메모 창(.pop.mpop.mb) 0')
        p2 = q.ev("()=>__CM.pops()")
        m2 = q.ev("()=>__CM.mpops()")   # ★ fix8
        mine = [p for p in p1 if p['k'] == key]
        # 옛(fix8 전 · ⑧ 전 동작 = 목록 창): ok = len(p1) == 1 and len(mine) == 1 and mine[0]['t'] == '🗒 메모 — ' + C['ms'][1] and len(mine[0]['rows']) == 2 and not [p for p in p2 if p['k'] == key]
        ok = (not [p for p in p1 if str(p['k'] or '').startswith('pitlist|')] and not [p for p in p1 if str(p['k'] or '').startswith('cell|')] and b1
              and len([x for x in m1 if x['mode'] == 'b']) == 2 and not [x for x in m2 if x['mode'] == 'b'])   # ★ fix8 — ⑧ A-6-2(칩 = 목록 창 대신 그 문제 메모 창 전부 열기/닫기 · 접혀 있으면 본문 펴고) · A-7-6(메모 창 POPS 밖) · §B-6 「목록 창 0」 · 사용자 10/3 09:19 · 결정로그 10/3 22:36
        # 옛(fix8 전): return ok, {'누른 뒤 창': [(p['k'], p['t'], p['rows']) for p in p1], '다시 누른 뒤': [p['k'] for p in p2]}
        return ok, {'누른 뒤 창': [(p['k'], p['t'], p['rows']) for p in p1], '다시 누른 뒤': [p['k'] for p in p2], '본문 펴짐': b1,
                    '메모 창': [x['t'] for x in m1 if x['mode'] == 'b'], '다시 누른 뒤 메모 창': len([x for x in m2 if x['mode'] == 'b'])}   # ★ fix8
    finally:
        q.close()


def g3(br, eng, who):
    q = page(br, eng, who)
    try:
        q.ev("()=>__CM.board('민사소송법','기출')")
        if QJ.GATE:
            q.tap(q.ev("t=>__CM.at(__CM.rowOf(t)&&__CM.rowOf(t).querySelector('.chip.c-memo'))", C['ms'][1]))
        else:   # regress(★ yard8 — ⑧ 뒤 길): 칩 누름 → 메모 창 「🗒 13-50-2 「설문(1)」」(.pop.mpop.mb)이 뜸 — 목록 창 + 줄(옛 표지 JS_LIST_ROWS)은 ⑧ 뒤 안 뜬다(⑧ A-6-2)
            rtap(q, q.ev("t=>__CM.at(__CM.rowOf(t)&&__CM.rowOf(t).querySelector('.chip.c-memo'))", C['ms'][1]), JS_MEMO_TITLE, '🗒 %s 「설문(1)」' % re.search(r'\d\d-\d\d-\d+', C['ms'][1]).group(0), '메모 칩 누름 → 메모 창 「🗒 코드 「설문(1)」」')
        at = q.ev("()=>{const p=POPS.find(x=>x._pk&&x._pk.indexOf('pitlist|card|')===0);const r=p&&[...p.querySelectorAll('.pb .res')].find(x=>x.textContent.indexOf('설문(1)')>=0);return __CM.at(r)}")
        if QJ.GATE:
            q.tap(at)
        else:   # regress: ⑧ 뒤 = 목록 창이 없어 at=None → rtap 이 바로 False(안 누름 · 안 기다림 · 옛 길 그대로 둠)
            rtap(q, at, JS_FULL_OPEN, None, '목록 줄 누름 → 전문 창(🗒 포스트잇) — ⑧ 뒤 목록 창 없음')
        ps = q.ev("()=>__CM.pops()")   # ⑧ 뒤 = 목록 창이 없어 at=None → 안 누름(옛 길 그대로 둠)
        full = [p for p in ps if p['t'].startswith('🗒 포스트잇')]
        want = PIT[[k for k in PIT if k.endswith('설문(1)')][0]]['t']
        # 옛(fix8 전 · ⑧ 전 = 목록 줄 → 전문 창): ok = bool(full) and '[햄찌]' in full[0]['t'] and full[0]['badge'][:1] == ['「설문(1)」'] and want in full[0]['body']
        # 옛(fix8 전): return ok, {'전문 창': full[:1]}
        k1 = [k for k in PIT if k.endswith('설문(1)')][0]   # ★ fix8
        tm = q.ev("s=>__CM.fmt(s)", PIT[k1]['at'])   # ★ fix8 — 앱 pitFmt(at) 꼴 그대로(시간대 무관)
        tt = '🗒 %s 「설문(1)」' % re.search(r'\d\d-\d\d-\d+', C['ms'][1]).group(0)   # ★ fix8 — 「🗒 13-50-2 「설문(1)」」
        mw = [x for x in q.ev("()=>__CM.mpops()") if x['mode'] == 'b' and x['t'] == tt]   # ★ fix8
        ok = bool(mw) and mw[0]['text'] == want and '햄찌' in mw[0]['meta'] and bool(tm) and tm in mw[0]['meta']   # ★ fix8 — ⑧ A-7-6(창 제목 「🗒 코드 「낱말」」) · A-7-7(몸 .mtext = 메모 글 그대로 · .mmeta = 사람 칩 + MM.DD HH:MM) · A-6-2(칩 = 그 문제 메모 창 전부) · 사용자 10/3 06:28·06:42·09:19 · 결정로그 10/3 22:36
        return ok, {'전문 창': full[:1], '메모 창': mw[:1], '제목': tt, '시각': tm}   # ★ fix8
    finally:
        q.close()


def g4(br, eng, who):
    q = page(br, eng, who)
    try:
        q.ev("()=>__CM.board('민사소송법','기출')")
        # 옛(fix8 전 · ⑧ 전 = 제목 누름 → 카드 창): at = q.ev("t=>__CM.at(__CM.rowOf(t)&&__CM.rowOf(t).querySelector('.c2t2'))", C['ms'][1])
        at = q.ev("t=>__CM.codeAt(t)", C['ms'][1])   # ★ fix8 — ⑧ A-4-3(제목 누름 = 본문 펴기 · 카드 창 안 뜸 · 사용자 10/3 07:19) · A-5-3·4(코드 숫자 = 카드 창 · 07:30 바로잡음) · 결정로그 10/3 22:36 — 바탕(줄 누름)·새 판(코드) 둘 다 카드 창 → 「바탕 = 기준」 그대로
        if QJ.GATE:
            q.tap(at, 1200)
        else:   # regress: 카드 팝업(cell|🧾 …)이 뜸 — popCard4 가 데이터를 읽은 뒤 짓는다(코드 숫자 누름 = 앱 c2RowEl 의 cd.onclick → popCard4)
            rtap(q, at, JS_CARD_OPEN, None, '코드 숫자 누름 → 카드 팝업(cell|🧾 …)')
        ps = q.ev("()=>__CM.pops()")
        sel = q.ev("()=>[...document.querySelectorAll('#slot .c2row.sel')].map(r=>__CM.tx(r.querySelector('.c2t2')))")
        return any(p['k'] and str(p['k']).startswith('card') or 'card' in str(p['k']) for p in ps) or any(C['ms'][1][:12] in (p['t'] or '') for p in ps), {'창': [(p['k'], p['t'][:40]) for p in ps], 'sel': sel}
    finally:
        q.close()


def g5(br, eng, who):
    q = page(br, eng, who)
    try:
        q.ev("l=>__CM.board(l,'GS')", C['gs_law'])
        gs = q.ev("t=>__CM.chip(__CM.rowOf(t))", C['gs'])
        q.ev("l=>__CM.board(l,'사례')", C['sa_law'])
        sa = q.ev("t=>__CM.chip(__CM.cellOf(t))", C['sa'])
        sak = q.ev("t=>__CM.kids(__CM.cellOf(t))", C['sa'])
        cls = [x['cls'] for x in (sak or [])]
        isc = next((i for i, c in enumerate(cls) if 'c-score' in c), -1); imc = next((i for i, c in enumerate(cls) if 'c-memo' in c), -1)
        ok = bool(gs) and gs['t'].startswith('🗒 1') and gs['who'] == ['햄찌'] and bool(sa) and sa['t'].startswith('🗒 1') and sa['who'] == ['꼬까'] and 0 <= isc < imc == isc + 1
        return ok, {'GS': gs, '사례': sa, '사례 머리 차례': [x['t'] for x in (sak or [])]}
    finally:
        q.close()


def g6(br, eng, who):
    q = page(br, eng, who)
    try:
        q.ev("()=>__CM.board('민사소송법','기출')")
        c0 = q.ev("t=>__CM.chip(__CM.rowOf(t))", C['ms'][1])
        keys = [k for k in PIT if k.startswith('card|기출|' + C['ms'][1])]
        q.ev("k=>{pitPut(k,null);return render()}", keys[1])
        if QJ.GATE:
            q.pg.wait_for_timeout(700)
        else:   # regress: render 끝(busy 꺼짐) — 위 evaluate 가 render() 약속을 기다렸다
            QJ.until(q.pg, JS_IDLE, T_UP, 'pitPut 뒤 render 끝(busy 꺼짐)')
        c1 = q.ev("t=>__CM.chip(__CM.rowOf(t))", C['ms'][1])
        q.ev("k=>{pitPut(k,null);return render()}", keys[0])
        if QJ.GATE:
            q.pg.wait_for_timeout(700)
        else:
            QJ.until(q.pg, JS_IDLE, T_UP, 'pitPut 뒤 render 끝(busy 꺼짐)')
        c2 = q.ev("t=>__CM.chip(__CM.rowOf(t))", C['ms'][1])
        ok = bool(c0) and c0['t'].startswith('🗒 2') and bool(c1) and c1['t'].startswith('🗒 1') and c1['who'] == ['햄찌'] and c2 is None
        return ok, {'처음': c0 and c0['t'], '하나 지움': c1 and c1['t'], '다 지움': c2}
    finally:
        q.close()


WJ = r"""()=>{const vw=innerWidth,de=document.documentElement;const rows=[...document.querySelectorAll('#slot .c2row,#slot .cell[data-ck]')];
  const over=rows.filter(r=>{const t=r.querySelector('.c2t1,.chd');if(!t)return false;return t.scrollWidth>t.clientWidth+1}).length;
  const chips=[...document.querySelectorAll('#slot .chip.c-memo')].map(c=>c.getBoundingClientRect());
  const out=chips.filter(r=>r.right>vw+0.5||r.left<-0.5).length;
  return {docow:de.scrollWidth-de.clientWidth,rowOver:over,chips:chips.length,chipOut:out,chipH:chips.length?Math.round(chips[0].height*10)/10:null}}"""


def g7(br, eng, who):
    out = {}; ok = True
    for dn in ('PC', 'iPad', '폰'):
        q = page(br, eng, who, dn)
        try:
            q.ev("()=>__CM.board('민사소송법','기출')")
            m = q.ev(WJ)
            r = q.ev("t=>{const c=__CM.rowOf(t)&&__CM.rowOf(t).querySelector('.chip.c-memo');if(!c)return null;c.scrollIntoView({block:'center'});const b=c.getBoundingClientRect(),x=b.left+b.width/2;let h=0;for(let y=Math.floor(b.top-20);y<=Math.ceil(b.bottom+20);y++){const a=document.elementFromPoint(x,y+0.5);if(a&&(a===c||c.contains(a)))h++}return {vis:[Math.round(b.width),Math.round(b.height*10)/10],hitH:h}}", C['ms'][1])
            m['칩 누름'] = r
            out[dn] = m
            ok = ok and m['docow'] <= 0 and m['chipOut'] == 0 and m['chips'] >= 2
        finally:
            q.close()
    return ok, out


SWJ = r"""()=>{const vw=innerWidth,vh=innerHeight,de=document.documentElement;
  const pops=(typeof POPS!=='undefined'?POPS:[]).filter(p=>p.isConnected).map(p=>{const r=p.getBoundingClientRect();return {k:String(p._pk||'').slice(0,40),out:r.left<-0.5||r.right>vw+0.5||r.top<-0.5||r.bottom>vh+0.5,ow:Math.max(0,p.scrollWidth-p.clientWidth),box:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]}});
  const rows=[...document.querySelectorAll('#slot .c2t1,#slot .chd')].filter(t=>t.scrollWidth>t.clientWidth+1).length;
  const mp=[...document.querySelectorAll('.pop.mpop')].map(p=>{const r=p.getBoundingClientRect();return {t:String((p.querySelector('.ph .pt')||{}).textContent||'').slice(0,30),out:r.left<-0.5||r.right>vw+0.5||r.top<-0.5||r.bottom>vh+0.5,box:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]}});   /* ★ fix8 — ⑧ 메모 창(POPS 밖 · A-7-6) */
  /* 옛(fix8 전): return {docow:de.scrollWidth-de.clientWidth,rowOver:rows,pops}} */
  return {docow:de.scrollWidth-de.clientWidth,rowOver:rows,pops,mp}}"""


def g8(br, eng, who):
    """B-10 화면 훑기 — 기출·GS·사례 보드 · 메모 목록 창 · 전문 창 × PC · 아이패드 · 폰 — 쪽·줄 넘침 0 · 창 화면 밖 0"""
    out = {}; ok = True
    for dn in ('PC', 'iPad', '폰'):
        q = page(br, eng, who, dn)
        try:
            for law, kind, f in (('민사소송법', '기출', C['ms'][1]), (C['gs_law'], 'GS', C['gs']), (C['sa_law'], '사례', C['sa'])):
                q.ev("a=>__CM.board(a[0],a[1])", [law, kind])
                out['%s %s 보드' % (dn, kind)] = m = q.ev(SWJ)
                ok = ok and m['docow'] <= 0 and m['rowOver'] == 0
            q.ev("()=>__CM.board('민사소송법','기출')")
            if QJ.GATE:
                q.tap(q.ev("t=>__CM.at(__CM.rowOf(t)&&__CM.rowOf(t).querySelector('.chip.c-memo'))", C['ms'][1]))
            else:   # regress(★ yard8 — ⑧ 뒤 길): 칩 누름 → 메모 창(.pop.mpop.mb)이 문제 메모 수만큼 뜸 → 두 프레임(창 자리를 잰다) — 목록 창 + 줄(JS_LIST_ROWS)은 ⑧ 뒤 안 뜬다(⑧ A-6-2)
                rtap(q, q.ev("t=>__CM.at(__CM.rowOf(t)&&__CM.rowOf(t).querySelector('.chip.c-memo'))", C['ms'][1]), JS_MEMO_N, len([k for k in PIT if k.startswith('card|기출|' + C['ms'][1] + SEP)]), '메모 칩 누름 → 메모 창(.pop.mpop.mb) 둘')
            out['%s 목록 창' % dn] = m1 = q.ev(SWJ)
            if QJ.GATE:
                q.tap(q.ev("()=>{const p=POPS.find(x=>x._pk&&x._pk.indexOf('pitlist|card|')===0);return __CM.at(p&&p.querySelector('.pb .res'))}"))
            else:   # regress: 전문 창이 뜸
                rtap(q, q.ev("()=>{const p=POPS.find(x=>x._pk&&x._pk.indexOf('pitlist|card|')===0);return __CM.at(p&&p.querySelector('.pb .res'))}"), JS_FULL_OPEN, None, '목록 줄 누름 → 전문 창(🗒 포스트잇)')
            out['%s 전문 창' % dn] = m2 = q.ev(SWJ)
            for m in (m1, m2):
                # 옛(fix8 전 · ⑧ 전 = 목록 창·전문 창이 POPS): ok = ok and m['docow'] <= 0 and all(not p['out'] for p in m['pops']) and len(m['pops']) >= 1
                ok = ok and m['docow'] <= 0 and all(not p['out'] for p in m['pops']) and all(not p['out'] for p in m['mp']) and len(m['mp']) >= 1   # ★ fix8 — ⑧ A-6-2(칩 = 그 문제 메모 창 전부 · 목록 창 없음 → 「전문 창」 장면도 메모 창 그대로) · A-7-6·정한 것 13(메모 창 = POPS 밖 자체 요소) · 사용자 10/3 09:19 · 결정로그 10/3 22:36
            # 창 안 가로 굴림 — 목록 창 = popPitListOf 그대로(지시서 A-2) · 그 줄 <b> 가 nowrap 이라 긴 메모는 창 안에서 옆으로 굴러간다 = 판례 메모 목록도 같은 바탕 흠 → 값만(같은 함수로 판례 꼴 목록을 바탕에서도 연다)
            out['%s 같은 창 판례 꼴(긴 글)' % dn] = q.ev("""()=>{closeAllPops(true);popPitListOf('pitlist|h','🗒 메모 — 시험',[{key:'k',tk:'prec|1',struct:'0',wi:'1',word:'낱말',t:'가나다라마바사아자차카타파하 '.repeat(4),who:'햄찌',ts:'2026-10-01T03:24:00.000Z'}],null);
              const p=POPS.find(x=>x._pk==='pitlist|h');const r={w:p.clientWidth,sw:p.scrollWidth};closeAllPops(true);return r}""")
        finally:
            q.close()
    return ok, out


GATES = [('b1', 'B-1 민소 기출 13-50-2 줄 차례 = 제목 → 미채점 → 「🗒 2 햄찌 꼬까」 → (Claude) → PDF · 13-50-1·4 칩 0 · 13-50-3 「🗒 1 미상」(회색)', g1, 'fix'),
         # 옛 칸 글(fix8 전): b2 'B-2 칩 누름 → 창 하나(pitlist|card|기출|…) · 제목 「🗒 메모 — 민기출 13-50-2-사물관할」 · 줄 2 · 카드 팝업 0 · 다시 누름 = 닫힘'
         #   b3 'B-3 목록 줄 누름 → 전문 창(머리 [햄찌] 시각 · 「설문(1)」 딱지 · 전문 = 주입 값)' · b4 'B-4 줄의 다른 곳(제목) 누름 → 카드 팝업 = 바탕과 같음'
         ('b2', 'B-2 칩 누름 → 목록 창 0 · 카드 팝업 0 · 13-50-2 본문 펴짐 · 메모 창 2(.pop.mpop · POPS 밖) · 다시 누름 = 메모 창 0', g2, 'fix'),   # ★ fix8 — ⑧ A-6-2 · A-7-6 · §B-6 · 사용자 10/3 09:19 · 결정로그 10/3 22:36
         ('b3', 'B-3 목록 줄 누름 → (⑧ 뒤 목록 창 없음) 칩 누름 → 메모 창 「🗒 13-50-2 「설문(1)」」 · 글 = 주입 값 · 햄찌 · 시각', g3, 'fix'),   # ★ fix8 — ⑧ A-6-2 · A-7-6 · A-7-7 · 사용자 10/3 06:28·06:42·09:19 · 결정로그 10/3 22:36
         ('b4', 'B-4 줄의 다른 곳(코드 숫자) 누름 → 카드 팝업 = 바탕과 같음', g4, 'keep'),   # ★ fix8 — 누를 자리만(제목 → 코드 숫자) · ⑧ A-4-3 · A-5-3·4 · 사용자 10/3 07:19·07:30 · 결정로그 10/3 22:36
         ('b5', 'B-5 GS 보드 줄 · 사례 격자 칸 머리 — 칩 · 수 · 사람(점수 칩 바로 뒤) · 특허 GS 는 데이터에 보드가 없어 있는 GS 보드로', g5, 'fix'),
         ('b6', 'B-6 메모 지움(pitPut null) → render 뒤 칩 2 → 1 · 다 지우면 칩 0', g6, 'fix'),
         ('b7', 'B-7 폭 PC 1440 · 아이패드 834 · 폰 390 — 줄 넘침·쪽 넘침 0 · 칩 화면 밖 0 · 칩 누름 높이 값', g7, 'keep'),
         # 옛 칸 글(fix8 전): b10 'B-10 화면 훑기 — 기출·GS·사례 보드 · 메모 목록 창 · 전문 창 × PC·아이패드·폰 — 쪽·줄 넘침 0 · 창 화면 밖 0 · (창 안 가로 굴림 = popPitListOf 바탕 흠 · 값만)'
         ('b10', 'B-10 화면 훑기 — 기출·GS·사례 보드 · 메모 창(⑧ — 목록 창·전문 창 자리) × PC·아이패드·폰 — 쪽·줄 넘침 0 · 창 화면 밖 0 · 메모 창 1 이상 · (창 안 가로 굴림 = popPitListOf 바탕 흠 · 값만)', g8, 'keep')]   # ★ fix8 — ⑧ A-6-2 · A-7-6 · 정한 것 13 · 결정로그 10/3 22:36


def main():
    APPS['NEW'] = app_src(NEWF)
    if QJ.GATE:   # regress · smoke: 바탕(헛잣대 · 「바탕 = 기준」 표시)을 안 푼다 — git show 0 · 바탕 띄움 0
        QJ.sub('git:show-app')
        APPS['BASE'] = app_src(BASEF)
    C.update(cards()); PIT.update(fixture(C))
    base_rev = BASEF
    if QJ.GATE:
        try:
            base_rev = git('rev-parse', '--short', BASEF).decode().strip() or BASEF
        except Exception:
            pass
    t0 = time.time(); TIMES = []
    print('INFO | B-0 합성 카드 | %s' % json.dumps(C, ensure_ascii=False), flush=True)
    with sync_playwright() as pw:
        for eng in ENGS:
            br = getattr(pw, eng).launch()
            try:
                for g, name, fn, kind in GATES:
                    if ONLY and g not in ONLY:
                        continue
                    if QJ.SMOKE and g not in ('b1', 'b2'):   # smoke 칸 = b1(칩 · 줄 차례) · b2(칩 누름 → 목록 창)
                        continue
                    ts = time.time(); res = {}
                    for who in (('NEW',) if QJ.REGRESS else ('NEW', 'BASE')):   # regress: NEW 만 — 바탕은 「바탕 —」
                        try:
                            res[who] = fn(br, eng, who)
                        except Exception as e:
                            res[who] = (False, 'ERR ' + repr(e)[:400])
                    if QJ.REGRESS:
                        res['BASE'] = (None, None)
                    R(g, eng, name + ('  [바탕 = 기준]' if kind == 'keep' else ''), res['NEW'][0], res['BASE'][0], {'NEW': res['NEW'][1], 'BASE': res['BASE'][1]})
                    TIMES.append((g, round(time.time() - ts)))
            finally:
                if QJ.REGRESS:
                    RIG.shut()
                br.close()
    npass = sum(1 for r in ROWS if r[3]); nfail = sum(1 for r in ROWS if not r[3])
    vac = [r for r in ROWS if r[4] is True and '기준' not in r[2]]
    print('\n== PASS %d · FAIL %d · 헛잣대(바탕도 PASS · 기준 칸 밖) %d · %.0f초 · 단계 초 %s' % (npass, nfail, len(vac), time.time() - t0, TIMES))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · jo_c2memo · NEW %s · 바탕 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), os.path.basename(NEWF), base_rev, ','.join(ENGS)))
        for g, eng, n, okn, okb, v in ROWS:
            f.write('%s | 바탕 %s | %s · %s · %s | %s\n' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, eng, n,
                    (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str))[:20000]))
        f.write('== PASS %d · FAIL %d · 헛잣대 %d · 단계 초 %s\n' % (npass, nfail, len(vac), TIMES))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
