# -*- coding: utf-8 -*-
r"""_task_jo_2cha_unitall_1012 §3 관문 [클라우드] — 조판기 2차 「단원별」: 주단원 · 걸침 걷음 = 문제가 짚은 단원마다 그 문제 줄

  python _harness_jo_2cha_unitall.py [--new <앱 파일 | genie git 판>] [--base <판 = f67f747>] [--only U1,U2,..] [--eng chromium,webkit] [--res <결과 파일>]

  NEW  = genie 작업트리 jo/index.html · BASE = 바탕 main f67f747(jo/index.html LF md5 0fb5b4d3 · 헛잣대 — U1 · U2 · U3 · U4 · U6 · U8 바탕 FAIL · 나머지 바탕 값은 결과에)
  데이터 = genie jo/data(실물 · 읽기만) · 기록 = 빈 기록에서 시작(쪽마다 localStorage 비움 · tt.cfg person 만 · 토큰 없음 · 손값 칸만 하네스가 넣음) · 밖 주소 404
  기대값 = 하네스가 jo/data 셋(2cha_단원_민소 · note_민소 · note_backlink)과 2cha_보드.json 격자에서 스스로 셈(앱 값을 잣대로 안 씀):
           문제 단원 = 설문 단원 ∪ 「주」 ∪ 목차노트 인용(note_backlink 「노트#^블록」 기출 목록 · 민소 노트만 = 앱 mokCite 와 같은 셈을 파이썬으로)
  기기 = PC 1440×900 마우스 · 아이패드 820×1180 · 폰 390×844 터치(DSF 2 · Chromium = CDP Input.dispatchTouchEvent 손가락 · WebKit = touchscreen.tap · 길게 = 합성 touch 포인터)
         코드 숫자 누름 자리 = 글 오른쪽 끝 4px 안(코드 칸 아래 두루마리 .c2q1 가 크롬 모바일 손가락 자리 맞춤으로 가운데 누름을 가져감 — 바탕도 같은 꼴)
         넘침 훑기 = 1440 · 1024 · 834 · 390
  칸:
    U1 머리(.c2uh[data-unit]) 59 · 줄(.c2row) 280 · 「1.3.2. {합변}…」 머리 「문제 2」 · 그 아래 줄 = 24-61-2 · 14-51-1
    U2 머리마다 「문제 N」 = 데이터로 센 값 · 59/59 · 머리 아래 줄 수 = N
    U3 목차노트 창(#mokBtn) 줄 중 「기출 N」 칩(.ck-g) 있는 노트 = 다 단원별 머리 있음
    U4 .c2uh .ov 0 · .c2row.c2ov 0 · .c2ovt 0
    U5 .c2row[data-ck] 76 · 겹침 0 · 나머지 204 = data-ckx · 코드 숫자 누름(마우스 · 손가락) = 그 카드 창 · 같은 카드 둘째 줄에서 눌러도 같은 창 하나
    U6 1.3.1 머리 아래 24-61-2 「단원 N ▸」 톡 → 칩 셋(1.3.2 · 1.4 · 7.3) · 1.3.2 아래 같은 카드 = 셋(1.3.1 · 1.4 · 7.3) · 회차별 = 넷
    U7 「+」 → 고르개에서 그 문제에 없는 단원(문제 0 인 단원) → 그 단원 머리에 그 문제 줄 섬 · 칩 ✕ → 빠짐(머리 0 이면 머리도 없음)
    U8 「단원 N」 0.5 초 길게(마우스 · 손가락) = ✎ 창 · .c2w-main display none · 설문 칩 ✕ · 저장(되묻기 없음) → 그 머리에서 그 줄 빠짐 ·
       인용으로도 짚는 단원은 남음(정한 것 ②) · 「자동값으로 되돌리기」 → 처음 그대로
    U9 옛 판 손값({main:'7.3. …', s:{'(1)':['1.4. …']}} 지어낸 값)을 기록에 넣고 띄움 → 그 문제 = 1.4 · 7.3 · 인용 노트 머리에만
    U10 GS · 사례 보드 · 회차별 · 특허 2차 = 바탕과 같은 줄 수 · 오류 0
    U11 페이지 오류 0 · 가로 넘침 0(1440 · 1024 · 834 · 390) · 처음 뜬 새 창(✎ 창 · 고르개) 높이 ≤ innerHeight/3 · 단원별 그리기 시간(바탕 · 새 판 ms)
  모드 — gate = 바탕 f67f747 를 git show 로 풀어 같은 차례로 띄움(헛잣대 · U10 맞대기) · regress = 새 판만(U10 바탕 = 기준 스냅샷) · smoke = Chromium PC U1 · U4
  결과 = PASS|FAIL|INFO | 칸[엔진] · 이름 · 바탕 판정 | 값 · --res 파일(기본 = 임시 폴더 · _qa 에 결과를 쓰지 않는다)
"""
import os as _os_r, sys as _sys_r   # env_lanes — _roots.py(GENIE_ROOT · SPD_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402 — --mode gate|regress|smoke · --snap-in · --snap-out 을 import 때 뗀다(아래 ARG 보다 먼저)
import collections, hashlib, json, os, re, subprocess, sys, tempfile, threading, time, traceback, urllib.parse   # noqa: E402
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEW = ARG('--new', _roots.genie('jo', 'index.html'))
BASE = ARG('--base', 'f67f747')   # main 판 · jo/index.html LF md5 0fb5b4d3
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
if QJ.SMOKE:
    ONLY = ['U1', 'U4']
    ENGS = [x for x in ENGS if x == 'chromium']
TMPD = os.path.join(tempfile.gettempdir(), 'h_jo_2cha_unitall')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_jo_2cha_unitall_result.txt'))
DATA = _roots.genie('jo', 'data')
SUBJ, LAW = '민소', '민사소송법'
IPAD_UA = 'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
IPHONE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
DEV = {'pc': dict(W=1440, H=900, touch=False), 'pc1024': dict(W=1024, H=768, touch=False),
       'pad': dict(W=820, H=1180, touch=True, ua=IPAD_UA), 'pad834': dict(W=834, H=1194, touch=True, ua=IPAD_UA),
       'phone': dict(W=390, H=844, touch=True, ua=IPHONE_UA)}
U6_CODE = '24-61-2'                                   # 지시서 U6 · U1 의 카드
U9_CODE = '14-51-4'                                   # U9 — 인용으로만 더해지는 단원이 있는 카드(지시서 「14-51-4 → 6.1 · 9 재심」)
U9_T = 1760000000000                                  # 지어낸 시각(손값 꼴 · 사용자 값 아님)
RES = []    # dict(g · eng · name · new · base · yard · d)
T0 = time.time()


def want(c):
    return not ONLY or c in ONLY


def git(*a):
    return subprocess.run(['git', '-C', _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def app_src(x):
    if os.path.isfile(x):
        return open(x, 'rb').read().decode('utf-8')
    b = git('show', x + ':jo/index.html')
    return b.decode('utf-8') if b else None


def md5lf(s):
    return hashlib.md5(s.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def _s(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


# ── 기대값(데이터에서 셈 · 앱 안 씀) ──────────────────────────────────────────────
RX = re.compile(r'^(\d+(?:\.\d+)*)\.?\s*')


def unum(n):
    m = RX.match(str(n or ''))
    return m.group(1) if m else ''


def upy(n):
    m = re.search(r'==(.+?)==', str(n or ''))
    return m.group(1).strip() if m else ''


def expect():
    jl = lambda f: json.load(open(os.path.join(DATA, f), encoding='utf-8'))
    U = jl('2cha_단원_' + SUBJ + '.json')['문제']
    N = jl('note_' + SUBJ + '.json')
    B = jl('note_backlink.json')
    BD = jl('2cha_보드.json')['기출|' + SUBJ]
    ids = collections.defaultdict(list)
    for k in B:
        i = k.find('#^')
        if i >= 0:
            ids[k[:i]].append(k[i + 2:])
    cite = collections.defaultdict(list)   # 카드 파일 → [민소 노트]
    for f, L in ids.items():
        if f not in N:
            continue
        for idd in L:
            for x in (B.get(f + '#^' + idd) or {}).get('기출', []) or []:
                if f not in cite[x]:
                    cite[x].append(f)
    cards = {}
    for k, xs in (BD.get('격자') or {}).items():
        r, c = k.split('|')
        for x in xs:
            yr = x.get('연도')
            cards[(str(yr)[2:] + '-' if yr else '') + r + '-' + str(int(c))] = x['파일']

    def touched(a):
        seen, out = set(), []
        for s in a.get('설문') or []:
            for u in s.get('단원') or []:
                n = u.get('n')
                if n and n not in seen:
                    seen.add(n); out.append(n)
        m = a.get('주') or ''
        if m and m not in seen:
            out.insert(0, m)
        return out
    per, by = {}, collections.defaultdict(list)
    for code, f in cards.items():
        us = touched(U[code]) if code in U else []
        for n in cite.get(f, []):
            if n not in us:
                us.append(n)
        per[code] = us
        for n in us:
            by[n].append(code)
    # U8 — X/u = 설문 한 줄에만 든 단원 · 주 아님 · 인용 아님(빼면 그 머리에서 빠져야) · Y/v = 설문 한 줄에만 · 주 아님 · 인용도 됨(빼도 남아야 · 정한 것 ②)
    xu = yv = None
    for code in sorted(cards, reverse=True):
        a = U.get(code)
        if not a:
            continue
        cs = cite.get(cards[code], [])
        for s in a.get('설문') or []:
            for u in s.get('단원') or []:
                v = u['n']
                rows = [x['no'] for x in a['설문'] if any(w['n'] == v for w in x.get('단원') or [])]
                if v == a.get('주') or len(rows) != 1:
                    continue
                if xu is None and v not in cs and len(per[code]) >= 2:
                    xu = (code, v, rows[0])
                if yv is None and v in cs:
                    yv = (code, v, rows[0])
    # U7 — Z = 번호 있는 노트 중 문제 0 인 단원(편 머리 아님 · 「+」 고르개에 있음) · K = U8 X 카드(그 단원 없음)
    zero = [n for n in N if unum(n) and n not in by and not (upy(n) and '.' not in unum(n))]
    kz = (xu[0], zero[0]) if (xu and zero) else None
    return dict(per=per, by={k: sorted(v) for k, v in by.items()}, heads=len(by), rows=sum(len(v) for v in by.values()),
                distinct=sum(1 for v in per.values() if v), cite={c: cite.get(f, []) for c, f in cards.items()}, xu=xu, yv=yv, kz=kz, ncards=len(cards))


EX = expect()


# ── 페이지 ────────────────────────────────────────────────────────────────────────
SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.alert=function(){};window.confirm=function(){window.__CONFIRM=(window.__CONFIRM||0)+1;return true;};window.prompt=function(){return null;};
(function(){var Q=new URLSearchParams(location.search);var nf=window.fetch.bind(window);
window.fetch=function(u,o){var s=String((u&&u.url)||u);
 if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));
 return nf(u,o);};
if(Q.get('keep')!=='1'){try{localStorage.clear();}catch(e){} try{localStorage.setItem('tt.cfg',JSON.stringify({person:'꼬까'}));}catch(e){}}
})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
</script>"""

# 페이지 도구(__UA) — 재는 것 = DOM 실물 · 누름은 파이썬이 진짜 마우스 · 손가락으로(길게 WebKit 터치만 합성 포인터)
TOOLS = r"""
(function(){
const W = ms => new Promise(r => setTimeout(r, ms));
const busyNow = () => { try { return !!busy; } catch (e) { return false; } };
const idle = async () => { for (let i = 0; i < 1200; i++){ if (!busyNow()) return true; await W(25); } return false; };
const live = () => { try { return POPS.filter(p => p.isConnected); } catch (e) { return [...document.querySelectorAll('.pop')]; } };
const vis = e => !!e && e.isConnected && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden' && getComputedStyle(e).display !== 'none';
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const hit = (e, tx) => { if (!e) return null; let r = e.getBoundingClientRect();
  if (tx){ const t = e.firstChild; if (t && t.nodeType === 3){ const g = document.createRange(); g.selectNodeContents(t); r = g.getBoundingClientRect(); } }
  const cx = r.left + r.width / 2, cy = r.top + r.height / 2, a = document.elementFromPoint(cx, cy);
  return { cx: +cx.toFixed(1), cy: +cy.toFixed(1), w: +r.width.toFixed(1), h: +r.height.toFixed(1), on: !!a && (a === e || e.contains(a)) && cy > 0 && cy < innerHeight && cx > 0 && cx < innerWidth }; };
const scrollHit = async (e, tx) => { if (!e) return null; try { e.scrollIntoView({ block: 'center', inline: 'nearest' }); } catch (x) {} await W(280); return hit(e, tx); };
const kids = () => { const w = document.querySelector('#slot .main .c2list'); return w ? [...w.children] : []; };
const codeOf = r => { const c = r && r.querySelector('.c2code'); if (!c) return ''; const t = c.firstChild; return String(t && t.nodeType === 3 ? t.nodeValue : txt(c)).trim(); };
const num = e => { const m = /\d+/.exec(txt(e)); return m ? +m[0] : -1; };
window.__UA = {
  idle, errs: () => (window.__ERR || []).slice(), confirms: () => window.__CONFIRM || 0,
  async go(o){ await idle(); try { closeAllPops(true); } catch (e) {}
    Object.assign(S, { law: '민사소송법', tab: 'cha2', boardKind: '기출', series: '', yearFilter: '', cha2Sel: null, cha2Filter: {} }, o || {});
    const t0 = performance.now(); await render(); await idle(); const ms = performance.now() - t0; await W(450); await idle();
    return { ms: Math.round(ms), ord: (typeof c2Ord === 'function') ? c2Ord() : null }; },
  unitRead(){ const out = { heads: [], none: -1, bands: 0, rows: 0, ck: 0, ckx: 0 }; let cur = null;
    kids().forEach(e => {
      if (e.classList.contains('c2band')){ out.bands++; return; }
      if (e.classList.contains('c2uh')){ if (e.classList.contains('c2unone')){ cur = null; out.none = num(e.querySelector('.n')); return; }
        cur = { unit: e.dataset.unit || '', n: num(e.querySelector('.n')), rows: [] }; out.heads.push(cur); return; }
      if (e.classList.contains('c2row')){ out.rows++; if (e.dataset.ck) out.ck++; if (e.dataset.ckx) out.ckx++; if (cur) cur.rows.push(codeOf(e)); } });
    out.ov = document.querySelectorAll('#slot .c2uh .ov').length; out.c2ov = document.querySelectorAll('#slot .c2row.c2ov').length; out.ovt = document.querySelectorAll('#slot .c2ovt').length;
    const cks = [...document.querySelectorAll('#slot .c2row[data-ck]')].map(r => r.dataset.ck); out.ckDup = cks.length - new Set(cks).size;
    return out; },
  rowEl(unit, code, nth){ let cur = null, k = 0;
    for (const e of kids()){ if (e.classList.contains('c2uh')){ cur = e.dataset.unit || ''; continue; }
      if (e.classList.contains('c2row') && (unit == null || cur === unit) && codeOf(e) === code){ if (k++ === (nth || 0)) return e; } }
    return null; },
  rowKinds(code){ return [...document.querySelectorAll('#slot .main .c2row')].filter(r => codeOf(r) === code).map(r => ({ ck: !!r.dataset.ck, ckx: !!r.dataset.ckx })); },
  async rowAt(unit, code, part, nth){ const r = this.rowEl(unit, code, nth); if (!r) return null; let t = null;
    if (part === 'code'){ const h = await scrollHit(r.querySelector('.c2code'), true); if (!h) return h;   /* 글 오른쪽 끝 4px 안 — 크롬 모바일 손가락 자리 맞춤이 코드 칸 안 아래 두루마리(.c2q1 = 문제 창)로 끌어가지 않게(가운데를 누르면 문제 창이 뜸) */
      const x = h.cx + h.w / 2 - 4, a = document.elementFromPoint(x, h.cy), c = r.querySelector('.c2code'); return Object.assign(h, { cx: +x.toFixed(1), on: h.on && !!a && (a === c || (c.contains(a) && !a.closest('.c2q1'))) }); }
    if (part === 'ue') t = r.querySelector('.c2r3 .c2ue'); else if (part === 'add') t = r.querySelector('.c2r3 .c2uadd');
    else if (part && part.indexOf('x:') === 0){ const n = part.slice(2); const c = [...r.querySelectorAll('.c2r3 .c2uc.added')].find(x => x.dataset.unit === n); t = c ? c.querySelector('.x') : null; }
    return scrollHit(t); },
  chips(unit, code){ const r = this.rowEl(unit, code); if (!r) return null;
    return { ue: txt(r.querySelector('.c2r3 .c2ue')), u: [...r.querySelectorAll('.c2r3 .c2uc')].map(c => c.dataset.unit), added: [...r.querySelectorAll('.c2r3 .c2uc.added')].map(c => c.dataset.unit) }; },
  /* 떠 있는 창 */
  pops(){ return live().map(p => { const r = p.getBoundingClientRect(); return { k: p._pk || '', cls: String(p.className), t: txt(p.querySelector('.ph .pt')).slice(0, 80), h: Math.round(r.height), top: Math.round(r.top), ih: innerHeight }; }); },
  cardPops(){ return live().filter(p => String(p._pk || '').indexOf('cell|🧾 기출') === 0).map(p => p._pk); },
  closePops(){ try { closeAllPops(true); } catch (e) {} try { if (typeof c2FlyClose === 'function') c2FlyClose(); } catch (e) {} return live().length; },
  /* 「+」 고르개 */
  pick(){ const m = document.querySelector('.c2upick'); if (!m || !vis(m)) return null; const r = m.getBoundingClientRect(); return { h: Math.round(r.height), top: Math.round(r.top), ih: innerHeight, n: m.querySelectorAll('.ui').length }; },
  async pickAt(n){ const m = document.querySelector('.c2upick'); if (!m) return null; const nu = c2uNum(n), nm = c2uName(n);
    const it = [...m.querySelectorAll('.ui')].find(x => txt(x.querySelector('b')) === nu && txt(x).indexOf(nm) >= 0); if (!it) return null;
    try { it.scrollIntoView({ block: 'nearest' }); } catch (e) {} await W(150); return Object.assign(hit(it), { have: it.classList.contains('on') }); },
  /* ✎ 단원 창 */
  win(){ const p = document.querySelector('.pop.c2uw'); if (!p) return null; const mr = p.querySelector('.c2w-main'), r = p.getBoundingClientRect();
    return { code: p.dataset.c2uwin, main: mr ? getComputedStyle(mr).display : null, mainVis: vis(mr), rows: [...p.querySelectorAll('.c2w-row')].map(x => ({ no: x.dataset.no, u: [...x.querySelectorAll('.c2uc')].map(c => c.dataset.n) })),
      msg: txt(p.querySelector('.c2w-msg')), h: Math.round(r.height), top: Math.round(r.top), bot: Math.round(r.bottom), ih: innerHeight }; },
  async winAt(kind, no, n){ const p = document.querySelector('.pop.c2uw'); if (!p) return null; let t = null;
    if (kind === 'x'){ const row = [...p.querySelectorAll('.c2w-row')].find(x => x.dataset.no === no); const c = row && [...row.querySelectorAll('.c2uc')].find(x => x.dataset.n === n); t = c && c.querySelector('.x'); }
    else if (kind === 'save') t = p.querySelector('.c2w-save'); else if (kind === 'rev') t = p.querySelector('.c2w-rev'); else if (kind === 'cls') t = p.querySelector('.c2w-cls');
    if (!t) return null; try { t.scrollIntoView({ block: 'nearest' }); } catch (e) {} await W(150); return hit(t); },
  hand(){ try { return JSON.parse(localStorage.getItem('jopangi.c2unit') || '{}'); } catch (e) { return {}; } },
  handReset(){ try { localStorage.removeItem('jopangi.c2unit'); } catch (e) {} S.c2uv = {}; return true; },
  /* 목차노트 창 */
  mokBtn(){ const b = document.getElementById('mokBtn'); return b ? hit(b) : null; },
  mokRead(){ const p = live().find(x => x.classList.contains('mkpop')); if (!p) return null; const rows = [...p.querySelectorAll('.mkr')];
    return { n: rows.length, g: rows.filter(r => r.querySelector('.ck-g')).map(r => r.dataset.note) }; },
  /* 가로 넘침 */
  over(){ const m = document.querySelector('#slot .main'), de = document.documentElement;
    return { main: m ? [m.scrollWidth, m.clientWidth] : null, doc: [de.scrollWidth, de.clientWidth], ok: (!m || m.scrollWidth <= m.clientWidth + 1) && de.scrollWidth <= de.clientWidth + 1 }; },
  /* 보드 줄 수(U10) */
  async count(o){ const g = await this.go(o); return { ord: g.ord, rows: document.querySelectorAll('#slot .c2row').length, cells: document.querySelectorAll('#slot .cell').length, heads: document.querySelectorAll('#slot .c2rh, #slot .c2uh').length }; },
  /* 길게(WebKit 터치) — 합성 touch 포인터(pointerdown → ms → pointerup · 같은 자리) */
  async holdSyn(x, y, ms){ const t = document.elementFromPoint(x, y); if (!t) return false; const o = { bubbles: true, cancelable: true, composed: true, pointerId: 7, pointerType: 'touch', isPrimary: true, clientX: x, clientY: y, button: 0, buttons: 1 };
    t.dispatchEvent(new PointerEvent('pointerdown', o)); await W(ms || 700); t.dispatchEvent(new PointerEvent('pointerup', Object.assign({}, o, { buttons: 0 }))); return true; }
};
})();
"""


def inject(src):
    src = src.replace('\r\n', '\n')
    b = src.index('<body'); bb = src.index('>', b) + 1
    html = src[:bb] + SEED + src[bb:]
    e = html.rindex('</body>')
    return html[:e] + '<script>\n' + TOOLS + '\n</script>\n' + html[e:]


SERVERS = {}


def serve(tag, src):
    if tag in SERVERS:
        return SERVERS[tag][1]
    body = inject(src).encode('utf-8')

    class Hd(SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, data, ct='application/json'):
            self.send_response(code)
            self.send_header('Content-Type', ct)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            p = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
            if p in ('/jo/', '/jo/index.html'):
                return self._send(200, body, 'text/html; charset=utf-8')
            if p.startswith('/jo/data/'):
                f = os.path.join(DATA, *[x for x in p[len('/jo/data/'):].split('/') if x])
                if os.path.isfile(f):
                    return self._send(200, open(f, 'rb').read())
            return self._send(404, b'{"message":"Not Found"}')

    srv = ThreadingHTTPServer(('127.0.0.1', 0), Hd)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


class P:
    """한 쪽 — 판(tag) · 기기(dev) · 엔진"""
    def __init__(self, br, eng, tag, src, dev):
        self.eng, self.tag, self.dev = eng, tag, dev
        self.ro_n = 0
        QJ.launch('base' if tag == 'BASE' else 'new')
        d = DEV[dev]
        self.touch = d['touch']
        self.port = serve(tag, src)
        kw = dict(viewport={'width': d['W'], 'height': d['H']})
        if d['touch']:
            kw.update(device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=d.get('ua'))
        self.ctx = br.new_context(**kw)
        self.ctx.route('**/*', lambda r: r.continue_() if r.request.url.startswith('http://127.0.0.1') else r.abort())
        self.pg = self.ctx.new_page()
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:300]))
        self.cdp = self.ctx.new_cdp_session(self.pg) if (eng == 'chromium' and d['touch']) else None
        self.load()

    def load(self, keep=False):
        self.pg.goto('http://127.0.0.1:%d/jo/index.html%s' % (self.port, '?keep=1' if keep else ''), wait_until='load', timeout=120000)
        self.pg.wait_for_function("!!window.__UA&&typeof render==='function'&&typeof popCard4==='function'&&!!document.querySelector('#slot')", timeout=120000)
        self.pg.wait_for_timeout(1200)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def idle(self, ms=300):
        self.pg.wait_for_timeout(ms)
        self.ev("()=>__UA.idle()")

    def unit(self):
        g = self.ev("()=>__UA.go({c2ord:'unit'})")
        return g

    def tap(self, at, wait=700):
        """한 번 누름 — 터치 = 손가락(Chromium CDP · WebKit touchscreen) · PC = 마우스"""
        if not at or not at.get('on'):
            return False
        self.pg.wait_for_timeout(150)
        x, y = at['cx'], at['cy']
        if self.cdp:
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'id': 1}]})
            self.pg.wait_for_timeout(40)
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        elif self.touch:
            self.pg.touchscreen.tap(x, y)
        else:
            self.pg.mouse.click(x, y)
        self.idle(wait)
        return True

    def hold(self, at, ms=700, wait=700):
        """0.5 초 넘게 길게 — PC = 마우스 down/up · Chromium 터치 = CDP 손가락 · WebKit 터치 = 합성 touch 포인터(Playwright 웹킷엔 길게 누르는 진짜 터치가 없음)"""
        if not at or not at.get('on'):
            return None
        self.pg.wait_for_timeout(150)
        x, y = at['cx'], at['cy']
        if self.cdp:
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'id': 1}]})
            self.pg.wait_for_timeout(ms)
            self.cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
            how = 'CDP 손가락'
        elif self.touch:
            self.ev("([x,y,ms])=>__UA.holdSyn(x,y,ms)", [x, y, ms])
            how = '합성 touch 포인터'
        else:
            m = self.pg.mouse
            m.move(x, y); m.down(); self.pg.wait_for_timeout(ms); m.up()
            how = '마우스'
        self.idle(wait)
        return how

    def errors(self):
        """페이지 오류 — 「ResizeObserver loop completed with undelivered notifications」 알림은 브라우저 알림일 뿐 앱 오류 아님(바탕도 냄 · revfix0930 · mok_popup_phone 와 같은 거름) → 따로 셈(ro_n)"""
        a = self.errs + self.ev("()=>__UA.errs()")
        self.ro_n = sum(1 for e in a if 'ResizeObserver loop' in e)
        return [e for e in a if 'ResizeObserver loop' not in e]

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


def counts(u):
    return {h['unit']: h['n'] for h in (u or {}).get('heads') or []}


def safe(o, k, fn):
    try:
        o[k] = fn()
    except Exception:
        o[k] = {'하네스 오류': traceback.format_exc()[-600:]}


# ── 흐름 ─────────────────────────────────────────────────────────────────────────
def flow_pc(br, eng, tag, src):
    """PC 1440×900 마우스 — U1~U8 · U10 · U11(넘침 1440 · 첫 창 높이 · 그리기 ms)"""
    o = {}
    p = P(br, eng, tag, src, 'pc')
    try:
        g1 = p.unit(); g2 = p.unit()
        o['ms'] = {'처음': g1['ms'], '다시': g2['ms'], 'ord': g2['ord']}
        u0 = p.ev("()=>__UA.unitRead()")
        o['U'] = u0
        o['over1440'] = p.ev("()=>__UA.over()")
        if QJ.SMOKE:
            return o
        # U3 목차노트 창
        def u3():
            p.ev("()=>__UA.closePops()")
            p.tap(p.ev("()=>__UA.mokBtn()"), 1500)
            m = p.ev("()=>__UA.mokRead()")
            p.ev("()=>__UA.closePops()")
            return m
        safe(o, 'U3', u3)
        # U5 코드 숫자 누름(마우스) — 첫 줄(data-ck) · 같은 카드 둘째 줄(data-ckx) · 열린 채 첫 줄 다시
        def u5():
            return u5_tap(p, u0)
        safe(o, 'U5', u5)
        # U6 「단원 N ▸」 톡 → 칩
        def u6():
            r = {}
            p.ev("()=>{S.c2uv={};return __UA.go({c2ord:'unit'})}")
            u1 = [h for h in counts(u0) if unum(h) == '1.3.1']
            u2 = [h for h in counts(u0) if unum(h) == '1.3.2']
            r['머리'] = {'1.3.1': u1[:1], '1.3.2': u2[:1]}
            at = p.ev("([u,c])=>__UA.rowAt(u,c,'ue')", [u1[0] if u1 else '', U6_CODE])
            r['톡'] = bool(p.tap(at, 900))
            r['1.3.1 아래'] = p.ev("([u,c])=>__UA.chips(u,c)", [u1[0] if u1 else '', U6_CODE])
            r['1.3.2 아래'] = p.ev("([u,c])=>__UA.chips(u,c)", [u2[0] if u2 else '', U6_CODE])
            p.ev("()=>__UA.go({c2ord:'round'})")
            r['회차별'] = p.ev("([c])=>__UA.chips(null,c)", [U6_CODE])
            p.ev("()=>{S.c2uv={};return __UA.go({c2ord:'unit'})}")
            return r
        safe(o, 'U6', u6)
        # U7 「+」 → 고르개 → 문제 0 인 단원 → 그 머리에 줄 · 칩 ✕ → 빠짐
        def u7():
            return u7_flow(p, u0)
        safe(o, 'U7', u7)
        # U8 길게 → ✎ 창 → 칩 ✕ → 저장 → 빠짐 · 정한 것 ② · 되돌리기
        def u8():
            return u8_flow(p, u0, full=True)
        safe(o, 'U8', u8)
        # U10 다른 보드 줄 수
        def u10():
            r = {}
            r['GS'] = p.ev("()=>__UA.count({boardKind:'GS',c2ord:'round'})")
            r['사례'] = p.ev("()=>__UA.count({boardKind:'사례'})")
            r['회차별'] = p.ev("()=>__UA.count({boardKind:'기출',c2ord:'round'})")
            r['특허 2차'] = p.ev("()=>__UA.count({law:'특허법',boardKind:'기출',c2ord:'round'})")
            p.ev("()=>__UA.go({law:'민사소송법',boardKind:'기출',c2ord:'unit'})")
            return r
        safe(o, 'U10', u10)
    finally:
        o['errs'] = p.errors()[:6]
        o['ro'] = p.ro_n
        o['confirm'] = p.ev("()=>__UA.confirms()") if not p.pg.is_closed() else None
        p.close()
    return o


def u5_tap(p, u0):
    r = {}
    p.ev("()=>__UA.closePops()")
    h132 = [h['unit'] for h in u0['heads'] if unum(h['unit']) == '1.3.2']
    unit = h132[0] if h132 else None
    kinds = p.ev("c=>__UA.rowKinds(c)", U6_CODE)
    r['줄'] = kinds
    i_ck = next((i for i, k in enumerate(kinds) if k['ck']), None)
    i_ckx = next((i for i, k in enumerate(kinds) if k['ckx']), None)
    at1 = p.ev("([c,n])=>__UA.rowAt(null,c,'code',n)", [U6_CODE, i_ck]) if i_ck is not None else None
    r['첫 줄 누름'] = bool(p.tap(at1, 1500)); r['첫 줄 창'] = p.ev("()=>__UA.cardPops()")
    p.ev("()=>__UA.closePops()"); p.idle(300)
    at2 = p.ev("([c,n])=>__UA.rowAt(null,c,'code',n)", [U6_CODE, i_ckx]) if i_ckx is not None else None
    r['둘째 줄 누름'] = bool(p.tap(at2, 1500)); r['둘째 줄 창'] = p.ev("()=>__UA.cardPops()")
    at1b = p.ev("([c,n])=>__UA.rowAt(null,c,'code',n)", [U6_CODE, i_ck]) if i_ck is not None else None
    r['열린 채 첫 줄'] = bool(p.tap(at1b, 1200)); r['열린 채 창'] = p.ev("()=>__UA.cardPops()")
    r['머리'] = unit
    p.ev("()=>__UA.closePops()")
    return r


def u7_flow(p, u0):
    r = {}
    if not EX['kz']:
        return {'건넘': 'K/Z 없음'}
    K, Z = EX['kz']
    r['K'], r['Z'] = K, Z
    p.ev("()=>{__UA.handReset();return __UA.go({c2ord:'unit'})}")
    at = p.ev("([c])=>__UA.rowAt(null,c,'add',0)", [K])
    r['+ 누름'] = bool(p.tap(at, 900))
    r['고르개'] = p.ev("()=>__UA.pick()")
    it = p.ev("n=>__UA.pickAt(n)", Z)
    r['고름'] = bool(p.tap(it, 1200))
    u1 = p.ev("()=>__UA.unitRead()")
    r['더한 뒤 Z 머리'] = next((h for h in u1['heads'] if h['unit'] == Z), None)
    r['더한 뒤 머리 수'] = len(u1['heads'])
    other = next((h['unit'] for h in u1['heads'] if h['unit'] != Z and K in h['rows']), None)
    r['✕ 줄 머리'] = other
    ch = p.ev("([u,c])=>__UA.chips(u,c)", [other, K]) if other else None
    r['그 줄 칩'] = ch
    atx = p.ev("([u,c,n])=>__UA.rowAt(u,c,'x:'+n)", [other, K, Z]) if other else None
    r['✕ 누름'] = bool(p.tap(atx, 1200))
    u2 = p.ev("()=>__UA.unitRead()")
    r['뺀 뒤 Z 머리'] = next((h for h in u2['heads'] if h['unit'] == Z), None)
    c0, c2 = counts(u0), counts(u2)
    r['뺀 뒤 = 처음'] = c0 == c2
    p.ev("()=>{__UA.handReset();return __UA.go({c2ord:'unit'})}")
    return r


def u8_flow(p, u0, full):
    r = {}
    if not EX['xu']:
        return {'건넘': 'X/u 없음'}
    X, u, no = EX['xu']
    r['X'], r['u'], r['설문'] = X, u, no
    p.ev("()=>{__UA.handReset();return __UA.go({c2ord:'unit'})}")
    c0 = counts(p.ev("()=>__UA.unitRead()"))
    at = p.ev("([c])=>__UA.rowAt(null,c,'ue',0)", [X])
    r['길게'] = p.hold(at)
    w = p.ev("()=>__UA.win()")
    r['창'] = w
    r['창 엶 뒤 칩 펴짐'] = (p.ev("([c])=>__UA.chips(null,c)", [X]) or {}).get('u')
    if not w:
        return r
    cf0 = p.ev("()=>__UA.confirms()")
    r['✕'] = bool(p.tap(p.ev("([a,b])=>__UA.winAt('x',a,b)", [no, u]), 500))
    r['✕ 뒤 창 줄'] = (p.ev("()=>__UA.win()") or {}).get('rows')
    r['저장'] = bool(p.tap(p.ev("()=>__UA.winAt('save')"), 1200))
    r['저장 뒤 창'] = p.ev("()=>__UA.win()")
    r['되묻기'] = p.ev("()=>__UA.confirms()") - cf0
    u1 = p.ev("()=>__UA.unitRead()")
    hu = next((h for h in u1['heads'] if h['unit'] == u), None)
    r['저장 뒤 u 머리'] = {'n': hu['n'], 'X 있음': X in hu['rows']} if hu else None
    r['u 머리 처음'] = c0.get(u)
    r['손값'] = p.ev("k=>__UA.hand()[k]||null", SUBJ + '|' + X)
    if full and EX['yv']:
        Y, v, no2 = EX['yv']
        r['Y'], r['v'], r['Y 설문'] = Y, v, no2
        at2 = p.ev("([c])=>__UA.rowAt(null,c,'ue',0)", [Y])
        p.hold(at2)
        p.tap(p.ev("([a,b])=>__UA.winAt('x',a,b)", [no2, v]), 500)
        p.tap(p.ev("()=>__UA.winAt('save')"), 1200)
        u2 = p.ev("()=>__UA.unitRead()")
        hv = next((h for h in u2['heads'] if h['unit'] == v), None)
        r['② 저장 뒤 v 머리'] = {'n': hv['n'], 'Y 있음': Y in hv['rows']} if hv else None
        r['② v 머리 처음'] = c0.get(v)
        # 되돌리기 Y
        p.hold(p.ev("([c])=>__UA.rowAt(null,c,'ue',0)", [Y]))
        r['② 되돌리기'] = bool(p.tap(p.ev("()=>__UA.winAt('rev')"), 1200))
    # 되돌리기 X
    p.hold(p.ev("([c])=>__UA.rowAt(null,c,'ue',0)", [X]))
    r['되돌리기'] = bool(p.tap(p.ev("()=>__UA.winAt('rev')"), 1200))
    c9 = counts(p.ev("()=>__UA.unitRead()"))
    r['되돌린 뒤 = 처음'] = c9 == c0
    r['되돌린 뒤 손값'] = p.ev("k=>__UA.hand()[k]||null", SUBJ + '|' + X)
    p.ev("()=>{__UA.handReset();return __UA.go({c2ord:'unit'})}")
    return r


def flow_touch(br, eng, tag, src, dev):
    """아이패드 820×1180 · 폰 390×844 손가락 — U5 코드 숫자 톡 · U8 길게 ✎ 창 · ✕ · 저장 · 되돌리기 · 넘침 · 첫 창 높이"""
    o = {}
    p = P(br, eng, tag, src, dev)
    try:
        p.unit()
        u0 = p.ev("()=>__UA.unitRead()")
        o['U'] = {'heads': len(u0['heads']), 'rows': u0['rows']}
        o['over'] = p.ev("()=>__UA.over()")
        safe(o, 'U5', lambda: u5_tap(p, u0))
        safe(o, 'U8', lambda: u8_flow(p, u0, full=False))
    finally:
        o['errs'] = p.errors()[:6]
        o['ro'] = p.ro_n
        p.close()
    return o


def flow_over(br, eng, tag, src, dev):
    p = P(br, eng, tag, src, dev)
    try:
        p.unit()
        return {'over': p.ev("()=>__UA.over()"), 'errs': p.errors()[:4], 'ro': p.ro_n}
    finally:
        p.close()


def flow_u9(br, eng, tag, src):
    """옛 판 손값을 기록에 넣고 띄움(keep=1 로 다시 열기 = 부팅 때 이미 있음)"""
    o = {}
    p = P(br, eng, tag, src, 'pc')
    try:
        per = EX['per'].get(U9_CODE) or []
        m73 = next((n for n in EX['by'] if unum(n) == '7.3'), None)
        m14 = next((n for n in EX['by'] if unum(n) == '1.4'), None)
        v = {'main': m73, 's': {'(1)': [m14]}, 't': U9_T, 'by': '하네스'}
        o['손값'] = {'열쇠': SUBJ + '|' + U9_CODE, 'main': unum(m73), 's': {'(1)': [unum(m14)]}}
        p.ev("([k,v])=>{const o=JSON.parse(localStorage.getItem('jopangi.c2unit')||'{}');o[k]=v;localStorage.setItem('jopangi.c2unit',JSON.stringify(o));return true}", [SUBJ + '|' + U9_CODE, v])
        p.load(keep=True)
        p.unit()
        u = p.ev("()=>__UA.unitRead()")
        o['머리'] = sorted(h['unit'] for h in u['heads'] if U9_CODE in h['rows'])
        o['기대'] = sorted(set([m73, m14] + (EX['cite'].get(U9_CODE) or [])))
        o['손값 없을 때(데이터)'] = len(per)
    finally:
        o['errs'] = p.errors()[:4]
        o['ro'] = p.ro_n
        p.close()
    return o


# ── 판정 ─────────────────────────────────────────────────────────────────────────
H132 = next((n for n in EX['by'] if unum(n) == '1.3.2'), None)


def judge(o, tch, ov, u9, base=None):
    J = {}
    pc = o or {}
    U = pc.get('U') or {}
    heads = U.get('heads') or []
    h132 = next((h for h in heads if h['unit'] == H132), None)
    J['U1'] = (len(heads) == EX['heads'] and U.get('rows') == EX['rows'] and bool(h132) and h132['n'] == 2 and h132['rows'] == ['24-61-2', '14-51-1'],
               {'머리': len(heads), '줄': U.get('rows'), '기대': [EX['heads'], EX['rows']], '1.3.2': {'n': h132['n'], '줄': h132['rows']} if h132 else None})
    bad = [h['unit'][:24] for h in heads if h['n'] != len(EX['by'].get(h['unit'], [])) or len(h['rows']) != h['n']]
    miss = [n[:24] for n in EX['by'] if n not in {h['unit'] for h in heads}]
    same = sum(1 for h in heads if h['n'] == len(EX['by'].get(h['unit'], [])) and len(h['rows']) == h['n'] and sorted(h['rows']) == EX['by'].get(h['unit']))
    J['U2'] = (not bad and not miss and same == EX['heads'] == len(heads), {'같음': '%d/%d' % (same, EX['heads']), '다름': bad[:5], '없는 머리': miss[:5]})
    m = pc.get('U3') or {}
    hs = {h['unit'] for h in heads}
    lack = [n[:24] for n in (m.get('g') or []) if n not in hs]
    J['U3'] = (bool(m.get('g')) and not lack, {'목차노트 줄': m.get('n'), '기출 칩 노트': len(m.get('g') or []), '머리 없음': lack[:6]})
    J['U4'] = (U.get('ov') == 0 and U.get('c2ov') == 0 and U.get('ovt') == 0 and bool(heads), {'.ov': U.get('ov'), '.c2ov': U.get('c2ov'), '.c2ovt': U.get('ovt')})
    def u5ok(x):
        if not isinstance(x, dict) or '하네스 오류' in x:
            return False
        a, b, c = x.get('첫 줄 창') or [], x.get('둘째 줄 창') or [], x.get('열린 채 창') or []
        return x.get('첫 줄 누름') and len(a) == 1 and x.get('둘째 줄 누름') and len(b) == 1 and b == a and len(c) <= 1
    t5 = {k: (v or {}).get('U5') for k, v in (tch or {}).items()}
    J['U5'] = (U.get('ck') == EX['distinct'] and U.get('ckDup') == 0 and U.get('ckx') == EX['rows'] - EX['distinct'] and u5ok(pc.get('U5')) and all(u5ok(v) for v in t5.values()),
               {'data-ck': U.get('ck'), '겹침': U.get('ckDup'), 'data-ckx': U.get('ckx'), '기대': [EX['distinct'], EX['rows'] - EX['distinct']],
                'PC 마우스': u5brief(pc.get('U5')), **{k + ' 손가락': u5brief(v) for k, v in t5.items()}})
    x6 = pc.get('U6') or {}
    per6 = EX['per'].get(U6_CODE) or []
    want1 = sorted(n for n in per6 if unum(n) != '1.3.1'); want2 = sorted(n for n in per6 if unum(n) != '1.3.2')
    g1, g2, g3 = (x6.get('1.3.1 아래') or {}).get('u'), (x6.get('1.3.2 아래') or {}).get('u'), (x6.get('회차별') or {}).get('u')
    J['U6'] = (g1 is not None and sorted(g1) == want1 and len(g1) == 3 and g2 is not None and sorted(g2) == want2 and g3 is not None and sorted(g3) == sorted(per6) and len(g3) == 4,
               {'1.3.1 아래': [unum(n) for n in g1 or []], '1.3.2 아래': [unum(n) for n in g2 or []], '회차별': [unum(n) for n in g3 or []],
                '단추': [(x6.get('1.3.1 아래') or {}).get('ue'), (x6.get('회차별') or {}).get('ue')]})
    x7 = pc.get('U7') or {}
    zh = x7.get('더한 뒤 Z 머리')
    J['U7'] = (bool(zh) and zh.get('rows') == [x7.get('K')] and zh.get('n') == 1 and x7.get('뺀 뒤 Z 머리') is None and x7.get('뺀 뒤 = 처음') is True,
               {'K': x7.get('K'), 'Z': unum(x7.get('Z')), '고르개': x7.get('고르개'), '더한 뒤 Z 머리': {'n': zh.get('n'), '줄': zh.get('rows')} if zh else None,
                '✕ 줄 머리': unum(x7.get('✕ 줄 머리')), '뺀 뒤 Z 머리': x7.get('뺀 뒤 Z 머리'), '뺀 뒤 = 처음': x7.get('뺀 뒤 = 처음'), '오류': x7.get('하네스 오류')})
    def u8ok(x, full):
        if not isinstance(x, dict) or '하네스 오류' in x or not x.get('창'):
            return False
        w = x['창']; hu = x.get('저장 뒤 u 머리')
        gone = (hu is None and x.get('u 머리 처음') == 1) or (hu is not None and not hu['X 있음'] and hu['n'] == (x.get('u 머리 처음') or 0) - 1)
        ok = w.get('main') == 'none' and x.get('✕') and x.get('저장') and not x.get('저장 뒤 창') and x.get('되묻기') == 0 and gone and x.get('되돌린 뒤 = 처음') is True
        if full and EX['yv']:
            hv = x.get('② 저장 뒤 v 머리')
            ok = ok and bool(hv) and hv['Y 있음'] and hv['n'] == x.get('② v 머리 처음')
        return ok
    t8 = {k: (v or {}).get('U8') for k, v in (tch or {}).items()}
    J['U8'] = (u8ok(pc.get('U8'), True) and all(u8ok(v, False) for v in t8.values()),
               {'PC 마우스': u8brief(pc.get('U8')), **{k + ' 손가락': u8brief(v) for k, v in t8.items()}})
    J['U9'] = (bool(u9) and u9.get('머리') == u9.get('기대'), {'손값(지어낸 값)': (u9 or {}).get('손값'), '머리': [unum(n) for n in (u9 or {}).get('머리') or []], '기대': [unum(n) for n in (u9 or {}).get('기대') or []]})
    x10 = pc.get('U10') or {}
    b10 = base.get('U10') if base else None
    eq = {k: (b10 or {}).get(k) == x10.get(k) for k in ('GS', '사례', '회차별', '특허 2차')} if b10 else None
    J['U10'] = (bool(x10) and '하네스 오류' not in x10 and (eq is None or all(eq.values())) and not pc.get('errs'),
                {'새 판': x10, '바탕': b10, '같음': eq, '오류': pc.get('errs')})
    errs = list(pc.get('errs') or []) + [e for v in (tch or {}).values() for e in ((v or {}).get('errs') or [])] + [e for v in (ov or {}).values() for e in ((v or {}).get('errs') or [])] + list((u9 or {}).get('errs') or [])
    ovs = {'1440': pc.get('over1440'), **{k: (v or {}).get('over') for k, v in (ov or {}).items()}}
    hts = {'PC ✎ 창': h3((pc.get('U8') or {}).get('창')), 'PC 고르개': h3((pc.get('U7') or {}).get('고르개')),
           **{k + ' ✎ 창': h3(((v or {}).get('U8') or {}).get('창')) for k, v in (tch or {}).items()}}
    ro = (pc.get('ro') or 0) + sum(((v or {}).get('ro') or 0) for v in list((tch or {}).values()) + list((ov or {}).values())) + ((u9 or {}).get('ro') or 0)
    J['U11'] = (not errs and all(x and x.get('ok') for x in ovs.values()) and all(x and x['ok'] for x in hts.values()),
                {'오류': errs[:4], 'ResizeObserver 알림(거름)': ro, '넘침': {k: (x or {}).get('main') for k, x in ovs.items()}, '넘침 0': {k: bool(x and x.get('ok')) for k, x in ovs.items()},
                 '첫 높이': hts, '그리기 ms': pc.get('ms')})
    return J


def h3(w):
    return None if not w else {'h': w.get('h'), 'ih': w.get('ih'), 'ok': w.get('h') is not None and w['h'] <= w['ih'] / 3 + 1}


def u5brief(x):
    if not isinstance(x, dict):
        return x
    if '하네스 오류' in x:
        return x
    return {'첫 줄': len(x.get('첫 줄 창') or []), '둘째 줄': len(x.get('둘째 줄 창') or []), '같은 창': (x.get('첫 줄 창') or [None]) == (x.get('둘째 줄 창') or [0]), '열린 채 다시': len(x.get('열린 채 창') or [])}


def u8brief(x):
    if not isinstance(x, dict):
        return x
    if '하네스 오류' in x:
        return x
    w = x.get('창') or {}
    return {'길게': x.get('길게'), '창': bool(w), '주단원 줄': w.get('main'), 'u': unum(x.get('u')), 'u 머리': [x.get('u 머리 처음'), x.get('저장 뒤 u 머리')],
            '되묻기': x.get('되묻기'), '② v 머리': [x.get('② v 머리 처음'), x.get('② 저장 뒤 v 머리')] if 'Y' in x else None, '되돌린 뒤 = 처음': x.get('되돌린 뒤 = 처음')}


NAMES = {
    'U1': '머리 59 · 줄 280 · 「1.3.2. {합변}…」 머리 「문제 2」 · 아래 줄 = 24-61-2 · 14-51-1',
    'U2': '머리마다 「문제 N」 = 데이터로 센 값(설문 ∪ 주 ∪ 인용) · 59/59 · 머리 아래 줄 수 = N',
    'U3': '목차노트 창 「기출 N」 칩 노트 = 다 단원별 머리 있음',
    'U4': '걸침 걷음 — .c2uh .ov 0 · .c2row.c2ov 0 · .c2ovt 0',
    'U5': 'data-ck 76 · 겹침 0 · data-ckx 204 · 코드 숫자 누름(마우스 · 손가락) = 그 카드 창 · 둘째 줄도 같은 창 하나',
    'U6': '1.3.1 아래 24-61-2 「단원 N ▸」 → 칩 셋(1.3.2 · 1.4 · 7.3) · 1.3.2 아래 셋(1.3.1 · 1.4 · 7.3) · 회차별 넷',
    'U7': '「+」 → 고르개 → 문제 0 인 단원 → 그 머리에 줄 · 칩 ✕ → 빠짐(머리도 없음)',
    'U8': '「단원 N」 길게(마우스 · 손가락) = ✎ 창 · 주단원 줄 숨김 · ✕ · 저장(되묻기 0) → 빠짐 · 인용 단원은 남음(②) · 되돌리기 = 처음',
    'U9': '옛 판 손값(지어낸 값 {main:7.3 · (1):[1.4]}) → 그 문제 = 1.4 · 7.3 · 인용 노트 머리에만',
    'U10': 'GS · 사례 · 회차별 · 특허 2차 = 바탕과 같은 줄 수 · 오류 0',
    'U11': '페이지 오류 0 · 가로 넘침 0(1440 · 1024 · 834 · 390) · 첫 창(✎ · 고르개) 높이 ≤ ih/3 · 그리기 ms',
}
YARD = {'U1', 'U2', 'U3', 'U4', 'U6', 'U8'}   # 바탕 FAIL 이어야 하는 칸 — 나머지는 바탕 값을 적기만


def R(g, name, new, base=None, d='', yard=True):
    RES.append({'g': g, 'name': name, 'new': new, 'base': base, 'd': d, 'yard': yard})
    tag = 'INFO' if new is None else ('PASS' if new else 'FAIL')
    print('%s | %s · %s | %s' % (tag, g, name, _s(d)[:300]), flush=True)


def run(br, eng, tag, src):
    pc = flow_pc(br, eng, tag, src)
    if QJ.SMOKE:
        return pc, {}, {}, None
    tch = {}
    if want('U5') or want('U8') or want('U11'):
        for dev in ('pad', 'phone'):
            try:
                tch[dev] = flow_touch(br, eng, tag, src, dev)
            except Exception:
                tch[dev] = {'하네스 오류': traceback.format_exc()[-600:]}
    ov = {}
    if want('U11'):
        for dev, k in (('pc1024', '1024'), ('pad834', '834')):
            try:
                ov[k] = flow_over(br, eng, tag, src, dev)
            except Exception:
                ov[k] = {'하네스 오류': traceback.format_exc()[-600:]}
        ov['390'] = {'over': (tch.get('phone') or {}).get('over'), 'errs': []}
    u9 = None
    if want('U9'):
        try:
            u9 = flow_u9(br, eng, tag, src)
        except Exception:
            u9 = {'하네스 오류': traceback.format_exc()[-600:]}
    return pc, tch, ov, u9


def main():
    os.makedirs(TMPD, exist_ok=True)
    SRC = {'NEW': app_src(NEW)}
    if QJ.GATE:
        QJ.sub('git:show-app')
        SRC['BASE'] = app_src(BASE)
    R('B0', '판 · 자리 · 기대값(데이터)', None, None, {'NEW': NEW, 'md5(LF)': {k: md5lf(v)[:8] for k, v in SRC.items() if v}, 'BASE': BASE if QJ.GATE else '(regress · smoke = 안 띄움)', '엔진': ENGS,
                                                    '기대': {'카드': EX['ncards'], '머리': EX['heads'], '줄': EX['rows'], 'data-ck': EX['distinct'], 'U8 X/u': [EX['xu'][0], unum(EX['xu'][1])] if EX['xu'] else None,
                                                           '② Y/v': [EX['yv'][0], unum(EX['yv'][1])] if EX['yv'] else None, 'U7 K/Z': [EX['kz'][0], unum(EX['kz'][1])] if EX['kz'] else None}})
    res = {}
    with sync_playwright() as pw:
        for eng in ENGS:
            br = getattr(pw, eng).launch()
            try:
                for tag in [k for k in ('NEW', 'BASE') if SRC.get(k)]:
                    t1 = time.time()
                    try:
                        res[(tag, eng)] = run(br, eng, tag, SRC[tag])
                    except Exception:
                        res[(tag, eng)] = ({'하네스 오류': traceback.format_exc()[-900:]}, {}, {}, None)
                    R('B0', '%s %s 돎' % (tag, eng), None, None, '%.1f 분' % ((time.time() - t1) / 60))
            finally:
                br.close()
    for eng in ENGS:
        n = res.get(('NEW', eng))
        b = res.get(('BASE', eng))
        jb = judge(*b) if b else {}
        bpc = b[0] if b else None
        if not QJ.GATE and n:   # regress — U10 바탕 = 기준 스냅샷(앞 인도판 새 판 값 · 없으면 이 판 값)
            bpc = {'U10': QJ.base('U10@%s' % eng, (n[0] or {}).get('U10'))}
        jn = judge(*n, base=bpc) if n else {}
        for c in NAMES:
            if not want(c) or c not in jn:
                continue
            ok, d = jn[c]
            bb = jb.get(c) if jb else None
            R('%s[%s]' % (c, eng), NAMES[c], bool(ok), None if bb is None else bool(bb[0]), {'새 판': d, '바탕': bb[1]} if bb is not None else d, yard=(c in YARD))
        if b and n:
            R('B9[%s]' % eng, '단원별 그리기 ms(처음 · 다시)', None, None, {'새 판': (n[0] or {}).get('ms'), '바탕': (b[0] or {}).get('ms')})
    newp = [x for x in RES if x['new'] is not None]
    yard = [x for x in RES if x['base'] is not None and x['yard']]
    other = [x for x in RES if x['base'] is not None and not x['yard']]
    R('B9', '합 — 새 판 PASS %d · FAIL %d · 헛잣대(바탕 FAIL 이어야 할 칸) %d/%d · 그 밖 칸 바탕 PASS %d/%d · %.1f 분' % (
        sum(1 for x in newp if x['new']), sum(1 for x in newp if not x['new']), sum(1 for x in yard if not x['base']), len(yard),
        sum(1 for x in other if x['base']), len(other), (time.time() - T0) / 60), None)
    os.makedirs(os.path.dirname(os.path.abspath(OUTF)), exist_ok=True)
    with open(OUTF, 'w', encoding='utf-8') as f:
        for x in RES:
            tag = 'INFO' if x['new'] is None else ('PASS' if x['new'] else 'FAIL')
            yb = '' if x['base'] is None else (' · 바탕 ' + ('PASS' if x['base'] else 'FAIL') + ('' if x['yard'] else '(적기만)'))
            f.write('%s | %s · %s%s | %s\n' % (tag, x['g'], x['name'], yb, _s(x['d'])[:900]))
    QJ.flush()
    return 0 if newp and all(x['new'] for x in newp) else 1


if __name__ == '__main__':
    sys.exit(main())
