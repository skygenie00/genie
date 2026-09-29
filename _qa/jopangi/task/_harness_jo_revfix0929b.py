# -*- coding: utf-8 -*-
r"""_task_jo_revfix0929b §B 관문 — 교재 자리 창 · 기출뷰 발문·머리 · 누름 자리 · 폰 1차객 서랍 · 조문 팝업 자리 · 터치 누름 · 접기 글자 · 🔗인 · 서랍 머리 · 화면 훑기

  python _harness_jo_revfix0929b.py [--new <앱>] [--base <앱 파일 | genie git 판>] [--vendor <pdf.js 3.11.174 폴더>] [--eng chromium,webkit] [--only B1,B2,..] [--res <결과>] [--yardstick]

  NEW  = 이 판 앱(기본 genie jo/index.html) · BASE = 착수 때 HEAD(기본 genie git 판 ffafcb0 = cloud/jo_joscreen0929 끝) — --yardstick 이면 BASE 를 NEW 자리에 넣어 B-1~B-12 가 저마다 FAIL 해야 통과
    (B-1 = A-1 코드 무변 잠금이라 착수 판도 같은 코드 → 헛잣대는 jo_revfix0929 전 판 --yard1(기본 c3c33ca) · B-12 화면 훑기 = 새 판 흠 − 바탕 흠이라 헛잣대 해당 없음)
  회귀(규칙 57) — main 쪽 book8 · revfix0928night · revfix0929 · uid_add3 · 동기화 jo 는 N:(JOP · r'jo\data' 한 덩이 조각)라 「N: 필요 — 합칠 때 본 세션」으로 적는다
  자리 = _roots(GENIE_ROOT · MBPDF_ROOT) — 클라우드: GENIE_ROOT=/home/user/genie MBPDF_ROOT=/home/user/minbeoppdf
  서버 = 스스로(127.0.0.1 빈 포트) · /jo/index.html = 앱(+ SEED + 도구 __RB) · /jo/data · /gichul/pdf · /__book/ = 비공개 minbeoppdf 로컬 클론(토큰 없이 · SEED 가 fetch 를 돌린다) · /__vendor/ = pdf.js(앱이 cdnjs 에서 받는 3.11.174)
  누름 = 진짜 포인터(page.mouse · 손가락 = Chromium CDP 터치 · WebKit touchscreen.tap · WebKit 길게 누르기 = 같은 자리 합성 touch 포인터 + touchend) · 보임 = elementFromPoint · 누름 영역 = elementFromPoint 로 위아래·좌우를 더듬어 잰다
  WebKit 은 터치 칸(A-4 · A-6 · A-8)만 — 이 컴퓨터에 WebKit 이 없으면 「안 잼」
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import json, os, re, sys, time, subprocess, tempfile, threading, urllib.parse   # noqa: E402
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEW = ARG('--new', _roots.genie('jo', 'index.html'))
BASE = ARG('--base', 'ffafcb0')
DATA = ARG('--data', _roots.genie('jo', 'data'))
EXAM = ARG('--exam', _roots.genie('gichul', 'pdf'))
MBP = ARG('--mbpdf', _roots.mbpdf())
VENDOR = ARG('--vendor', os.path.join(tempfile.gettempdir(), 'h_gichul', 'vendor'))
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_revfix0929b_result.txt'))
YARD = '--yardstick' in sys.argv
PC = (1511, 1043)
PC2 = (1440, 900)
PHONE = (390, 844)
PAD = (834, 1194)


def git(*a):
    return subprocess.run(['git', '-C', _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def app_src(x):
    """앱 글 — 파일이면 그 파일 · 아니면 genie git 판의 jo/index.html"""
    if os.path.isfile(x):
        return open(x, 'rb').read().decode('utf-8')
    b = git('show', x + ':jo/index.html')
    if not b:
        raise SystemExit('바탕 앱을 못 읽었다: ' + x)
    return b.decode('utf-8')


# ── SEED — 몸 첫머리(앱 스크립트보다 먼저) · 바깥 주소는 안 나간다 ──
SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.alert=function(){};window.confirm=function(){return true;};window.prompt=function(){return null;};
(function(){var nf=window.fetch.bind(window);
window.__BOOKN=0;
window.fetch=function(u,o){o=o||{};var s=String((u&&u.url)||u);
 var bk=s.indexOf('api.github.com/repos/zzikkaplan/minbeoppdf/contents/');
 if(bk>=0){window.__BOOKN++;var rest=s.slice(bk+'api.github.com/repos/zzikkaplan/minbeoppdf/contents/'.length).split('?')[0];
  var hd={};try{var h=o.headers;var rg=h&&(typeof h.get==='function'?h.get('Range'):(h.Range||h.range));if(rg)hd.Range=rg;}catch(e){}
  return nf(location.origin+'/__book/'+rest,{headers:hd,signal:o.signal});}
 if(/cdnjs\.cloudflare\.com\/ajax\/libs\/pdf\.js\/3\.11\.174\//.test(s))return nf(location.origin+'/__vendor/'+s.split('/pdf.js/3.11.174/')[1],o);
 if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));
 return nf(u,o);};
})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
</script>
<script src="/__vendor/pdf.min.js"></script>
<script>try{pdfjsLib.GlobalWorkerOptions.workerSrc=location.origin+'/__vendor/pdf.worker.min.js';}catch(e){__ERR.push('pdfjs vendor '+e);}</script>"""

# ── 도구 __RB — 몸 끝(앱 스크립트 뒤) · 누름은 안 한다(자리만 · 파이썬이 누른다) ──
TOOLS = r"""<script>
(function(){
const wait = ms => new Promise(r => setTimeout(r, ms));
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const vis = e => !!e && e.isConnected && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden' && e.getBoundingClientRect().height > 0;
const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); return { x: Math.round(r.left * 10) / 10, y: Math.round(r.top * 10) / 10, w: Math.round(r.width * 10) / 10, h: Math.round(r.height * 10) / 10, b: Math.round(r.bottom * 10) / 10, r: Math.round(r.right * 10) / 10, cx: r.left + r.width / 2, cy: r.top + r.height / 2 }; };
const vv = () => { const v = window.visualViewport; return v ? { x: v.offsetLeft, y: v.offsetTop, w: v.width, h: v.height } : { x: 0, y: 0, w: innerWidth, h: innerHeight }; };
const pops = () => (typeof POPS !== 'undefined' ? POPS : []);
const popOf = pre => pops().filter(x => (x._pk || '').indexOf(pre) === 0).pop();
const idle = async () => { for (let i = 0; i < 600; i++){ if (typeof busy === 'undefined' || !busy) return; await wait(25); } };
const until = async (f, ms) => { const t0 = Date.now(); while (Date.now() - t0 < (ms || 15000)){ try{ const v = f(); if (v) return v; }catch(e){} await wait(50); } return null; };
function scrollerOf(e){ let q = e && e.parentElement; while (q && q !== document.body){ const cs = getComputedStyle(q); if (/(auto|scroll)/.test(cs.overflowY) && q.scrollHeight > q.clientHeight + 1) return q; q = q.parentElement; } return document.scrollingElement; }
function atNow(t){ if (!t) return null; const r = R(t), at = document.elementFromPoint(r.cx, r.cy);
  return Object.assign(r, { on: !!at && (at === t || t.contains(at)) && r.cy > 0 && r.cy < innerHeight, vis: vis(t), t: txt(t).slice(0, 40) }); }
function hitOn(t){ if (!t) return null; try{ t.scrollIntoView({ block: 'center', inline: 'nearest' }); }catch(e){} return atNow(t); }
/* 누름 영역 — 가운데에서 위·아래·왼·오른으로 1px 씩 elementFromPoint 가 그 요소(또는 안)인 데까지 */
function hitBox(t){ if (!t) return null; const r = t.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2;
  const on = (x, y) => { const a = document.elementFromPoint(x, y); return !!a && (a === t || t.contains(a)); };
  if (!on(cx, cy)) return { h: 0, w: 0, on: false, rect: R(t) };
  let up = 0, dn = 0, lf = 0, rt = 0;
  while (up < 80 && on(cx, cy - up - 1)) up++; while (dn < 80 && on(cx, cy + dn + 1)) dn++;
  while (lf < 120 && on(cx - lf - 1, cy)) lf++; while (rt < 120 && on(cx + rt + 1, cy)) rt++;
  return { h: up + dn + 1, w: lf + rt + 1, on: true, rect: R(t), top: cy - up, bottom: cy + dn, left: cx - lf, right: cx + rt }; }
function findText(root, needle, nth){
  nth = nth || 0; if (!root) return null;
  const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT); const nodes = []; let n;
  while ((n = tw.nextNode())) nodes.push(n);
  const str = nodes.map(x => x.nodeValue).join('');
  let p = -1; for (let k = 0; k <= nth; k++){ p = str.indexOf(needle, p + 1); if (p < 0) return null; }
  const at = pos => { let acc = 0; for (const x of nodes){ const L = x.nodeValue.length; if (pos < acc + L) return [x, pos - acc]; acc += L; } const last = nodes[nodes.length - 1]; return [last, last.nodeValue.length]; };
  const [sn, so] = at(p), [en, eo] = at(p + needle.length - 1);
  const r = document.createRange(); r.setStart(sn, so); r.setEnd(en, eo + 1); return r; }
/* 누름 자리 재기 — 설계 = 같은 갈래 이웃을 끄고 더듬은 크기 · 실제 = 다 켜고 더듬은 크기 · 가운데 = 제 것 ·
   가로챔 = 제가 먹는 점(2px 격자) 가운데 둘레(::before·::after)를 끄면 다른 누를 것(단추·링크·조 번호 …)의 제 자리인 점 +
   빈틈 점인데 같은 갈래 이웃 쪽이 더 가까운 점(가까운 쪽이 이긴다) */
/* 누를 것 = 단추·링크·조 번호·입력 칸 + 교재 자리 창 대응표 줄·그림(작은 누를 것) — 서랍 줄·장 머리 줄·카드처럼 줄 전체가 누름 자리인 큰 그릇은 뺀다(작은 단추의 둘레가 그 위에서 넓어지는 것은 허용 · 결과에 적음) */
const ACT = 'button, a[href], [role=button], [role=menuitem], .wmlk, .jno, input, select, textarea, label, [tabindex], .mbbrow, .ncb-pic';
const actOf = u => (u && u.closest ? u.closest(ACT) : null);
function tgt(t, same){
  if (!t) return null;
  const sib = same ? [...document.querySelectorAll(same)].filter(x => x !== t) : [];
  const keep = sib.map(x => x.style.pointerEvents); sib.forEach(x => { x.style.pointerEvents = 'none'; });
  const d = hitBox(t); sib.forEach((x, i) => { x.style.pointerEvents = keep[i]; });
  const e = hitBox(t), r = t.getBoundingClientRect();
  const own = (x, y) => { const a = document.elementFromPoint(x, y); return !!a && (a === t || t.contains(a)); };
  const dist = (q, x, y) => { const dx = Math.max(q.left - x, 0, x - q.right), dy = Math.max(q.top - y, 0, y - q.bottom); return Math.hypot(dx, dy); };
  let steal = 0, near = 0, pts = 0; const ex = [];
  if (d.on){
    const T0 = d.top, B0 = d.bottom, L0 = d.left, R0 = d.right;
    const mine = [];
    for (let y = Math.floor(T0) - 2; y <= B0 + 2; y += 2) for (let x = Math.floor(Math.min(L0, r.left)) - 2; x <= Math.max(R0, r.right) + 2; x += 2) if (own(x, y)) mine.push([x, y]);
    document.documentElement.classList.add('__nh');
    const sibR = sib.filter(vis).map(x => x.getBoundingClientRect()), grow = q => { const w = Math.max(q.width, 36), h = Math.max(q.height, 36), cx = q.left + q.width / 2, cy = q.top + q.height / 2; return { left: cx - w / 2, right: cx + w / 2, top: cy - h / 2 - 1, bottom: cy + h / 2 + 1 }; };
    for (const [x, y] of mine){
      if (x >= r.left && x <= r.right && y >= r.top && y <= r.bottom) continue;
      pts++;
      const u = document.elementFromPoint(x, y), X = u ? actOf(u) : null;
      if (X && X !== t && !X.contains(t) && !t.contains(X)){ steal++; if (ex.length < 3) ex.push([Math.round(x), Math.round(y), (X.className || X.tagName) + ' ' + txt(X).slice(0, 10)]); continue; }
      const dm = dist(r, x, y); if (sibR.some(q => { const g = grow(q); return x >= g.left && x <= g.right && y >= g.top && y <= g.bottom && dist(q, x, y) + 1.25 < dm; })){ near++; if (ex.length < 3) ex.push([Math.round(x), Math.round(y), 'nearer-sib']); }
    }
    document.documentElement.classList.remove('__nh');
  }
  const c = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
  return { w: Math.round(r.width * 10) / 10, h: Math.round(r.height * 10) / 10, dw: d.w, dh: d.h, ew: e.w, eh: e.h, center: !!c && (c === t || t.contains(c)), pts, steal, near, ex, t: txt(t).slice(0, 14) }; }
(function(){ const s = document.createElement('style'); s.textContent = 'html.__nh *::before,html.__nh *::after{pointer-events:none!important}'; document.head.appendChild(s); })();
window.__RB = {
  txt, vis, R, vv, atNow, hitOn, hitBox, findText, idle, until, wait, scrollerOf, tgt,
  errs(){ return (window.__ERR || []).slice(); },
  async home(law){ try{ closeAllPops(true); }catch(e){}
    S.law = law || '특허법'; S.tab = 'jimun'; S.jimunTab = 'ox'; S.mok = ''; S.oxQueue = ''; S.year = ''; S.omr = false;
    await idle(); await render(); await idle();
    await until(() => (S.law !== '특허법' || (typeof OXPOOL !== 'undefined' && OXPOOL && Object.keys(OXPOOL).length > 300)) && document.querySelector('#slot .mbdash'), 40000);
    await wait(200); return { law: S.law, pool: Object.keys(OXPOOL || {}).length }; },
  selOfKey(k){ if (!(typeof MLN !== 'undefined' && MLN.ok)) return null; const M = VJ.M; for (let i = 0; i < M.length; i++) for (const ln of ['b', 'n', 'u', 'v']){ if (mlnKeys(M, i, ln, VJ.P7map, VJ.byId).indexOf(k) >= 0) return (typeof mlnSel === 'function' ? mlnSel(i, ln) : '__mg' + i); }
    return null; },
  async goKey(k){ await __RB.home('특허법');
    try{ if (typeof UZGK !== 'undefined'){ UZGK = uzIsGi(k) ? 'g' : 'x'; await idle(); await render(); await idle(); } }catch(e){}
    const sel = __RB.selOfKey(k); if (!sel) return null;
    try{ closeAllPops(); }catch(e){} S.jimunTab = 'ox'; S.oxQueue = ''; S.mok = sel; S.oxPage = null; await idle(); await render(); await idle(); await wait(250);
    const P = (OXPOOL || {})[k]; const d = P && P.dom; if (d && !document.getElementById(d) && typeof OXDOMPG !== 'undefined' && OXDOMPG[d] != null){ S.oxPage = OXDOMPG[d]; await render(); await idle(); await wait(200); }
    return sel; },
  pinSeed(u, p, r){ const A = JSON.parse(localStorage.getItem('jopangi.canvasjari') || '{}'); A['p8|' + u] = { by: 'hand', b: 'patent_hr8', p: p, r: r, t: Date.now() };
    localStorage.setItem('jopangi.canvasjari', JSON.stringify(A)); try{ recDropCache(); }catch(e){} return true; },
  wordsDelay(d){ const J = viewCanvas.jari; if (J.__wd) return 1; const f = J.words.bind(J); J.words = (...a) => new Promise(r => setTimeout(r, d)).then(() => f(...a)); J.__wd = 1; return 1; },
  idTo(k, y){ const c = [...document.querySelectorAll('.qb.id')].filter(vis).find(b => txt(b) === k) || [...document.querySelectorAll('.qb.id')].find(b => txt(b) === k);
    if (!c) return null; try{ c.scrollIntoView({ block: 'center' }); }catch(e){}
    for (let i = 0; i < 4; i++){ const r = c.getBoundingClientRect(), d = (r.top + r.height / 2) - y; if (Math.abs(d) < 2) break; const sc = scrollerOf(c); sc.scrollTop += d; }
    return atNow(c); },
  closeBox(){ pops().filter(x => /^(cell\|📚|cv\|book\|)/.test(x._pk || '')).forEach(x => { try{ closeOne(x); }catch(e){} }); return true; },
  box(){ const w = popOf('cell|📚 교재 자리'); if (!w) return null; const h = w.querySelector('.mbb8');
    const bt = re => { const b = h && [...h.querySelectorAll('.ncb-more')].find(x => new RegExp(re).test(txt(x))); return b ? atNow(b) : null; };
    const hb = re => { const b = h && [...h.querySelectorAll('.ncb-more')].find(x => new RegExp(re).test(txt(x))); return b ? hitBox(b) : null; };
    const rs = w.querySelector('.prsz');
    const full = re => { const b = h && [...h.querySelectorAll('.ncb-more')].find(x => new RegExp(re).test(txt(x))); if (!b) return null; const r = b.getBoundingClientRect(), cx = r.left + r.width / 2;
      const at = y => { const a = document.elementFromPoint(cx, y); return !!a && (a === b || b.contains(a)); }; return at(r.top + 2) && at(r.bottom - 2) && r.top >= 0 && r.bottom <= innerHeight; };
    return { rect: R(w), vv: vv(), pic: !!(h && h.querySelector('.ncb-pic canvas')), noPicMsg: !!(h && /그림이 아직 없습니다/.test(txt(h))), rv: bt('자동으로 되돌리기'), pk: bt('자리 직접 찍기'), rvHit: hb('자동으로 되돌리기'), pkHit: hb('자리 직접 찍기'),
      rvFull: full('자동으로 되돌리기'), pkFull: full('자리 직접 찍기'), sh: w.scrollHeight, ch: w.clientHeight,
      loading: !!(h && /받는 중/.test(txt(h))), rows: h ? [...h.querySelectorAll('.mbbrow')].map(r => ({ hd: txt(r.querySelector('.hd')), sn: txt(r.querySelector('.sn')) })) : [],
      sz: rs ? atNow(rs) : null }; },
  async jo(law, k, tree){ try{ closeAllPops(true); }catch(e){} S.tab = 'jo'; S.law = law; S.jo = k; S.treeHid = !tree; await idle(); await render(); await idle();
    await until(() => { const t = document.querySelector('#slot .main .jotitle'); return t && t.textContent.indexOf(k) === 0; }, 30000); await wait(250); return true; },
  async exvRow(y, pg){ await __RB.home('특허법'); S.exvPg = S.exvPg || {}; S.exvPg[PLAW() + ':' + y] = pg; const r = document.querySelector('#slot .mbur[data-giy="' + y + '"] .nm'); if (!r) return null; return hitOn(r); },
  /* 화면 훑기 — 넘침(가로 굴림 · 화면 밖) · 잘림(숨김인데 말줄임 없이 글이 넘침) · 겹침(누를 것끼리) · 작은 누름 자리(손가락만 · 실제 누름 < 24) — 이름표 = 태그.갈래:글 */
  sweep(sel, touch){ const out = []; const sig = e => e.tagName.toLowerCase() + '.' + String(e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className).split(' ').filter(x => x && !/^(on|cur|hid|z|sel|fold)$/.test(x)).slice(0, 2).join('.') + ':' + txt(e).replace(/\d+/g, '#').slice(0, 14);
    const se = document.scrollingElement; if (se.scrollWidth > innerWidth + 1) out.push('page-hscroll');
    const roots = [...document.querySelectorAll(sel)].filter(vis);
    const all = []; roots.forEach(r => { all.push(r); r.querySelectorAll('*').forEach(e => all.push(e)); });
    const V = all.filter(e => e.getClientRects().length && vis(e)).slice(0, 5000);
    V.forEach(e => { const cs = getComputedStyle(e), ox = cs.overflowX;
      if ((ox === 'auto' || ox === 'scroll') && e.scrollWidth > e.clientWidth + 1 && e.clientWidth > 0) out.push('hscroll:' + sig(e));
      if ((ox === 'hidden' || ox === 'clip') && e.scrollWidth > e.clientWidth + 1 && e.clientWidth > 0 && cs.textOverflow !== 'ellipsis' && e.children.length === 0 && txt(e)) out.push('clip:' + sig(e));
      const r = e.getBoundingClientRect(); if (r.width > 0 && (r.right > innerWidth + 1 || r.left < -1) && cs.position !== 'fixed' && !e.closest('.pop') && getComputedStyle(e.parentElement || e).overflowX === 'visible') out.push('offscreen:' + sig(e)); });
    const A = V.filter(e => e.matches(ACT) && !e.disabled && getComputedStyle(e).pointerEvents !== 'none');
    /* 떠 있는 층(fixed · sticky — 알약 · 막대 머리)은 굴러가는 글 위에 뜨는 것이 뜻이라 겹침에서 뺀다(굴림 자리마다 달라진다) */
    const fl = e => { for (let q = e; q && q !== document.body; q = q.parentElement){ const ps = getComputedStyle(q).position; if (ps === 'fixed' || ps === 'sticky') return !(roots.some(r => r === q)); } return false; };
    const AS = A.filter(e => !fl(e));
    for (let i = 0; i < AS.length; i++) for (let j = i + 1; j < AS.length; j++){ const a = AS[i], b = AS[j]; if (a.contains(b) || b.contains(a)) continue;
      const p = a.getBoundingClientRect(), q = b.getBoundingClientRect(); const ix = Math.min(p.right, q.right) - Math.max(p.left, q.left), iy = Math.min(p.bottom, q.bottom) - Math.max(p.top, q.top);
      if (ix > 2 && iy > 2) out.push('overlap:' + sig(a) + '|' + sig(b)); }
    /* 작은 누름 자리(손가락) — 굴림 자리와 상관없이 셈이 같게 요소마다 화면 가운데로 굴려 잰다(떠 있는 층에 가리면 안 센다) */
    if (touch) A.slice(0, 240).forEach(e => { if (!fl(e)) try{ e.scrollIntoView({ block: 'center', inline: 'nearest' }); }catch(x){} const h = hitBox(e), r = e.getBoundingClientRect();   // 1px 더듬기는 소수점 자리로 ±1 흔들린다 → 보이는 크기(반올림)와 같이 본다
      if (h.on && ((Math.round(r.height) < 24 && h.h < 25) || (Math.round(r.width) < 24 && h.w < 25))) out.push('small:' + sig(e)); });
    return [...new Set(out)]; },
  async boxReady(pic){ for (let i = 0; i < 400; i++){ const b = __RB.box(); if (b && !b.loading && b.rows.length && b.rows[0].sn && (!pic || b.pic || b.noPicMsg)){ await wait(pic ? 600 : 700); return __RB.box(); } await wait(50); } return __RB.box(); },
};
})();
</script>"""


def inject(src):
    src = src.replace('\r\n', '\n')
    b = src.index('<body')
    bb = src.index('>', b) + 1
    html = src[:bb] + SEED + src[bb:]
    e = html.rindex('</body>')
    return html[:e] + TOOLS + '\n' + html[e:]


SERVERS = {}


def serve(tag, src):
    """tag 마다 서버 하나 · 앱 = 메모리(SEED + 도구를 넣은 글)"""
    if tag in SERVERS:
        return SERVERS[tag][1]
    body = inject(src).encode('utf-8')

    class H(SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            p = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
            if p in ('/jo/', '/jo/index.html'):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                self.wfile.write(body)
                return
            return super().do_GET()

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
            for pre, root in (('/jo/data/', DATA), ('/gichul/pdf/', EXAM), ('/__book/', MBP)):
                if p.startswith(pre):
                    return os.path.join(root, *[x for x in p[len(pre):].split('/') if x])
            if p.startswith('/__vendor/'):
                parts = [x for x in p[len('/__vendor/'):].split('/') if x]
                f = os.path.join(VENDOR, *parts)
                return f if os.path.exists(f) else os.path.join(VENDOR, 'build', *parts)
            return os.path.join(HERE, '__없음__')

    srv = ThreadingHTTPServer(('127.0.0.1', 0), H)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


class Pg:
    """쪽 하나 — 기기 흉내(PC 마우스 · 폰/아이패드 손가락) · 첫 기록(jopangi_ui 등)은 새 문맥에만 한 번 심는다"""

    def __init__(self, br, eng, tag, src, W, H, touch=False, ls=None, dsf=1):
        self.eng, self.touch = eng, touch
        kw = dict(viewport={'width': W, 'height': H}, device_scale_factor=dsf)
        if touch:
            kw.update(is_mobile=(eng != 'firefox' and W < 700), has_touch=True)
            if eng == 'webkit':
                kw.pop('is_mobile', None)
        self.ctx = br.new_context(**kw)
        self.ctx.route(lambda u: not u.startswith('http://127.0.0.1'), lambda r: r.abort())
        init = {'tt.cfg': json.dumps({'token': 'harness-token', 'person': '하네스'})}
        for k, v in (ls or {}).items():
            init[k] = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
        self.ctx.add_init_script("if(!sessionStorage.getItem('__h')){sessionStorage.setItem('__h','1');const I=%s;for(const k in I)localStorage.setItem(k,I[k]);}" % json.dumps(init, ensure_ascii=False))
        self.pg = self.ctx.new_page()
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append(str(e)))
        port = serve(tag, src)
        self.pg.goto('http://127.0.0.1:%d/jo/index.html' % port)
        self.pg.wait_for_function("typeof S!=='undefined' && typeof busy!=='undefined' && !busy && document.querySelector('#slot .main, #slot .mbdash') && window.__RB", timeout=90000)
        self.idle()

    def ev(self, js, arg=None):
        return self.pg.evaluate(js, arg)

    def idle(self, extra=150):
        self.pg.wait_for_function("typeof busy!=='undefined' && !busy", timeout=90000)
        self.pg.wait_for_timeout(extra)

    def wait(self, ms):
        self.pg.wait_for_timeout(ms)

    def click(self, x, y, wait=400):
        self.pg.mouse.click(x, y)
        self.pg.wait_for_timeout(wait)

    def tap(self, x, y, wait=400):
        if self.eng == 'webkit':
            self.pg.touchscreen.tap(x, y)
        else:
            cdp = self.ctx.new_cdp_session(self.pg)
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]})
            self.pg.wait_for_timeout(60)
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
            try:
                cdp.detach()
            except Exception:
                pass
        self.pg.wait_for_timeout(wait)

    def press(self, at, wait=400):
        """at = {cx, cy, on} — 손가락 문맥이면 탭 · 아니면 마우스"""
        if not at or not at.get('on'):
            return False
        (self.tap if self.touch else self.click)(at['cx'], at['cy'], wait)
        return True

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


RES = []


def T(g, name, ok, detail=''):
    RES.append((g, name, bool(ok), detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', g, name, d[:600]), flush=True)
    return ok


def N(g, name, detail=''):
    RES.append((g, name, None, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('INFO | %s · %s | %s' % (g, name, d[:900]), flush=True)


# ════════════════════════ 관문 ════════════════════════
U_PIN, PIN_P, PIN_R = 'T1552093', 500, [0.154, 0.674, 0.862, 0.7265]   # 찍어 둔 자리를 심는 지문(P7-1662) · 해례 8판 p.500
TOUCH_DEV = (('폰390', PHONE), ('iPad834', PAD))
SIX = [('체크', '.tree .r button.jck', '.tree .r button.jck', True), ('접기1', '.tree .jtbar .jstep', '', True),
       ('팔레트', '.jckpal .jcksw, .jckpal .jckclr', '.jckpal .jcksw, .jckpal .jckclr', True), ('거름 줄', '.jckmenu .jckmo', '.jckmenu .jckmo', False),
       ('모드 글자', '.jomt .plgb.jomd', '.jomt .plgb.jomd', True), ('막대 둘째 줄', '.mk9bar .mk9r2 button.m2, #c2mark .mk9r2 button.m2', '.mk9r2 button.m2', True)]
MEAS = r"""([sel, same, n]) => [...document.querySelectorAll(sel)].filter(__RB.vis).slice(0, n || 4).map(e => { e.scrollIntoView({block:'center'}); return __RB.tgt(e, same); })"""


def dev_page(br, tag, src, dev, eng=None, ls=None):
    eng = eng or br.browser_type.name   # 합치기(9/30 Code) — B4 · B8 이 WebKit 브라우저를 넘기며 엔진을 안 줘 크로미움(CDP) 길로 가 멈췄다
    W, Hh = dev
    touch = dev in (PHONE, PAD)
    return Pg(br, eng, tag, src, W, Hh, touch=touch, ls=ls, dsf=2 if touch else 1)


WK_LONG = r"""([x, y, ty]) => { const t = ty === 'pointerdown' ? document.elementFromPoint(x, y) : (window.__tlT || document.elementFromPoint(x, y));
  if (ty === 'pointerdown') window.__tlT = t;
  t.dispatchEvent(new PointerEvent(ty, {bubbles: true, cancelable: true, composed: true, pointerId: 7, pointerType: 'touch', isPrimary: true,
    clientX: x, clientY: y, button: 0, buttons: ty === 'pointerdown' ? 1 : 0}));
  if (ty === 'pointerup') t.dispatchEvent(new Event('touchend', {bubbles: true, cancelable: true, composed: true}));
  return t.tagName; }"""


def long_press(p, x, y, ms=700):
    if p.eng == 'webkit':
        # 합치기(9/30 Code) — Playwright WebKit 은 진짜 터치를 붙잡지 못한다(톡만 · CDP 없음). 옛 길(톡 한 번)은 길게 누르기가 아니라 막대가 안 떴다.
        # 앱 길게 누르기 = 줄 pointerdown 뒤 500ms 타이머 — 같은 자리에 합성 touch 포인터를 같은 시간 보내고, 손 뗄 때처럼 touchend 도 보낸다.
        p.pg.evaluate(WK_LONG, [x, y, 'pointerdown'])
        p.wait(ms)
        p.pg.evaluate(WK_LONG, [x, y, 'pointerup'])
        p.wait(350)
        return
    cdp = p.ctx.new_cdp_session(p.pg)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]})
    p.wait(ms)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    p.wait(350)
    try:
        cdp.detach()
    except Exception:
        pass


def open_box(p, uid, y, pic):
    p.ev("() => __RB.closeBox()")
    at = p.ev("a => __RB.idTo(a[0], a[1])", [uid, y])
    p.press(at, 700)
    p.ev("async p => await __RB.boxReady(p)", pic)
    p.wait(1000)
    return at, p.ev("() => __RB.box()")


def b1(br, src, tag):
    """A-1 폰 교재 자리 창 둘째 열기 = jo_revfix0929 자리(코드 무변 · 잠금) — 칩 y 300→420→600→420 · 창 = 칩+14 에 두고 아래 끝이 화면−8 을 넘으면 그만큼 올림 · 단추 둘 온전히 · 안쪽 굴림 없음"""
    G = 'B1'
    p = Pg(br, 'chromium', tag, src, 390, 844, touch=True, dsf=3)
    p.ev("async () => await __RB.home('특허법')")
    p.ev("a => __RB.pinSeed(a[0], a[1], a[2])", [U_PIN, PIN_P, PIN_R])
    p.ev("() => __RB.wordsDelay(400)")
    p.ev("async k => await __RB.goKey(k)", U_PIN)
    rows, ok = [], True
    for y in (300, 420, 600, 420):
        at, b = open_box(p, U_PIN, y, True)
        if not (at and b):
            ok = False
            rows.append((y, None))
            continue
        top, bot, h = b['rect']['y'], b['rect']['b'], b['rect']['h']
        want = min(at['cy'] + 14, 844 - 8 - h)
        good = abs(top - want) <= 2.5 and bot <= 836.5 and top >= 7.5 and b['rvFull'] and b['pkFull'] and b['sh'] <= b['ch'] + 1 and b['pic']
        ok = ok and good
        rows.append((y, round(top), round(bot), round(h), 'want top %d' % round(want), 'rv/pk 온전 %s/%s' % (b['rvFull'], b['pkFull']), '안쪽 굴림 %s' % (b['sh'] > b['ch'] + 1)))
    T(G, '폰 둘째 열기 자리 = 칩+14 · 넘치면 아래 끝 836 · 단추 둘 온전 · 안쪽 굴림 없음', ok, rows)
    N(G, '채팅 수치', '채팅 371–836 = 창 높이 465(채팅 글꼴) · 이 컨테이너(WenQuanYi) 창 높이 %s → 같은 규칙으로 둘째 열기 %s' % (rows[1][3] if rows[1][1] is not None else '?', rows[1][1:3]))
    T(G, 'JS 오류', not p.errs, p.errs[:3])
    p.close()
    return ok


def b2(br, src, tag):
    """A-2 그림 없는(찍어 둔 자리 없는) 교재 자리 창도 화면 안 — bottom ≤ 화면−8 · 크기 손잡이 보임"""
    G = 'B2'
    ok = True
    for (W, Hh, touch, ys) in ((1440, 900, False, (700, 500, 300)), (1511, 1043, False, (850,)), (390, 844, True, (600,)), (834, 1194, True, (900,))):
        p = Pg(br, 'chromium', tag, src, W, Hh, touch=touch, dsf=2 if touch else 1)
        p.ev("async () => await __RB.home('특허법')")
        p.ev("() => __RB.wordsDelay(400)")
        p.ev("async k => await __RB.goKey(k)", U_PIN)
        for y in ys:
            at, b = open_box(p, U_PIN, y, False)
            p.wait(400)
            b = p.ev("() => __RB.box()")
            good = bool(b) and not b['pic'] and b['rect']['b'] <= b['vv']['h'] - 8 + 0.5 and b['rect']['y'] >= 7.5 and bool(b['sz']) and b['sz']['on'] and bool(b['pk']) and b['pk']['on']
            ok = ok and good
            T(G, '%d×%d 칩 y %d' % (W, Hh, y), good, b and {'창': [b['rect']['y'], b['rect']['b']], '한도': b['vv']['h'] - 8, '손잡이': b['sz'] and b['sz']['on'], '📍': b['pk'] and b['pk']['on'], '그림': b['pic']})
        if p.errs:
            T(G, 'JS 오류 %d' % W, False, p.errs[:3])
            ok = False
        p.close()
    return ok


EXV_HEAD = r"""() => { const h = document.querySelector('#slot .mbsbar'); if (!h) return null; const es = [...h.querySelectorAll('.t1, .t2')];
  const e = es.find(x => /\d{4}년 제\d+회/.test(x.textContent)); return e ? {t: e.textContent, sw: e.scrollWidth, cw: e.clientWidth} : {t: es.map(x => x.textContent).join(' | '), sw: -1, cw: 0}; }"""


def exv_open(p, y, pg, direct=False):
    """기출뷰 그 해(쪽) — 첫 화면 해 줄을 누른다 · direct = 줄 누름과 같은 함수(mbGiGo)를 바로(훑기: 착수 판 폰은 서랍이 카드 칸을 118px 로 눌러 줄 누름이 빗나간다)"""
    at = p.ev("async a => await __RB.exvRow(a[0], a[1])", [y, pg])
    if direct:
        p.ev("y => mbGiGo(y)", y)
        p.wait(1500)
    else:
        p.press(at, 1500)
    p.pg.wait_for_function("() => document.querySelectorAll('#slot .exv-q').length > 0", timeout=30000)
    p.idle(300)


def b3(br, src, base_src, tag):
    """A-3 기출뷰 2013 12번 발문 = 데이터 줄 수 · 줄바꿈 없는 발문 셋 DOM 글 무변(바탕과 같은 outerHTML)"""
    G = 'B3'
    samp = [('2009', 0, '1'), ('2026', 0, '2'), ('2013', 0, '3')]
    outs = {}
    for which, s in (('new', src), ('base', base_src)):
        p = Pg(br, 'chromium', tag + which, s, 1440, 900)
        exv_open(p, '2013', 2)
        st = p.ev(r"""() => { const q = [...document.querySelectorAll('#slot .exv-q')].find(x => x.dataset.exno === '12'); if (!q) return null; const s = q.querySelector('.exv-stem');
          const d = (MBHEAD.list || []).find(x => String(giNo(x)) === '12'); return {dom: s.innerText.split('\n').length, data: d ? String(d.발문 || '').split('\n').length : -1, ws: getComputedStyle(s).whiteSpace}; }""")
        smp = []
        for y, pg, no in samp:
            exv_open(p, y, pg)
            smp.append(p.ev(r"""n => { const q = [...document.querySelectorAll('#slot .exv-q')].find(x => x.dataset.exno === n); if (!q) return null; const s = q.querySelector('.exv-stem'); const d = (MBHEAD.list || []).find(x => String(giNo(x)) === n);
              return {html: s.outerHTML, nl: d ? /\n/.test(d.발문 || '') : null}; }""", no))
        outs[which] = (st, smp)
        p.close()
    st, smp = outs['new']
    ok1 = bool(st) and st['data'] > 1 and st['dom'] == st['data']
    T(G, '2013 12번 발문 DOM 줄 = 데이터 줄', ok1, st)
    same = [bool(a) and bool(b) and a['nl'] is False and a['html'] == b['html'] for a, b in zip(smp, outs['base'][1])]
    T(G, '줄바꿈 없는 발문 셋(2009-1 · 2026-2 · 2013-3) DOM 무변', all(same), same)
    return ok1 and all(same)


def meas_six(p, which_only=None):
    """조문 화면 여섯 곳 누름 자리 — {이름: [tgt …]}"""
    out = {}
    p.ev("async () => await __RB.jo('특허법', '제6조', true)")
    for nm, sel, same, _ in SIX[:2]:
        out[nm] = p.ev(MEAS, [sel, same, 5])
    out['조 번호'] = p.ev(MEAS, ['.tree .r .jno', '.tree .r .jno', 3])
    p.ev("() => { const b = [...document.querySelectorAll('.tree .r button.jck')].filter(__RB.vis)[1]; b.click(); }")
    p.wait(300)
    out['팔레트'] = p.ev(MEAS, [SIX[2][1], SIX[2][2], 7])
    p.ev("() => { const q = document.querySelector('.jckpal'); if (q) q.remove(); document.querySelector('.tree .jtbar .jckf').click(); }")
    p.wait(300)
    out['거름 줄'] = p.ev(MEAS, [SIX[3][1], SIX[3][2], 8])
    p.ev("() => { const q = document.querySelector('.jckmenu'); if (q) q.remove(); }")
    p.ev("async () => await __RB.jo('특허법', '제6조', false)")
    out['모드 글자'] = p.ev(MEAS, [SIX[4][1], SIX[4][2], 5])
    pos = p.ev(r"""() => { const box = document.querySelector('#slot .main .box'); const r = __RB.findText(box, '대리인'); r.startContainer.parentElement.scrollIntoView({block:'center'}); const q = r.getBoundingClientRect(); return {x: q.left + q.width / 2, y: q.top + q.height / 2}; }""")
    if p.touch:
        long_press(p, pos['x'], pos['y'])
    else:
        p.pg.mouse.move(pos['x'] - 20, pos['y'])
        p.pg.mouse.down()
        p.pg.mouse.move(pos['x'] + 20, pos['y'])
        p.pg.mouse.up()
        p.wait(500)
    out['막대 둘째 줄'] = p.ev(MEAS, [SIX[5][1], SIX[5][2], 3])
    return out


def meas_book(p):
    """A-4 세 단추 — 1차객 「정답·해설 ▸」 · 교재 자리 창(그림 없는 창 📍 · 그림 창 자동으로 되돌리기 · 📍)"""
    out = {}
    p.ev("async () => await __RB.home('특허법')")
    p.ev("async k => await __RB.goKey(k)", U_PIN)
    out['정답·해설'] = p.ev(MEAS, ['#slot .mbpeek', '#slot .mbpeek', 3])
    open_box(p, U_PIN, 400, False)
    out['📍(그림 없음)'] = p.ev(MEAS, ['.pop .mbb8 .ncb-more', '.ncb-more', 3])
    p.ev("a => __RB.pinSeed(a[0], a[1], a[2])", [U_PIN, PIN_P, PIN_R])
    p.ev("async k => await __RB.goKey(k)", U_PIN)
    open_box(p, U_PIN, 400, True)
    out['되돌리기·📍(그림)'] = p.ev(MEAS, ['.pop .mbb8 .ncb-more', '.ncb-more', 3])
    return out


def touch_ok(nm, arr, need_w):
    """설계(같은 갈래 이웃 끔) 높이 ≥ 36(좁은 것은 폭도) · 가운데 = 제 것 · 가로챔 0 · 가까운 쪽이 이김 0"""
    bad = []
    for x in arr:
        if x['dh'] < 36 or (need_w and x['dw'] < 36) or not x['center'] or x['steal'] or x['near']:
            bad.append(x)
    return (bool(arr) and not bad), [('%s %sx%s 설계 %sx%s 실제 %sx%s 가로챔 %s 먼쪽 %s' % (x['t'], x['w'], x['h'], x['dw'], x['dh'], x['ew'], x['eh'], x['steal'], x['near'])) for x in (bad or arr[:2])]


def pc_same(a, b):
    """PC 마우스 = 바탕과 같은 크기(보이는 크기 · 누름 크기)"""
    ka = [(x['t'], x['w'], x['h'], x['dw'], x['dh']) for x in a]
    kb = [(x['t'], x['w'], x['h'], x['dw'], x['dh']) for x in b]
    return ka == kb, (ka[:3], kb[:3])


def b4(br, src, base_src, tag):
    G = 'B4'
    ok = True
    for dn, dev in TOUCH_DEV:
        p = dev_page(br, tag + dn, src, dev)
        m = meas_book(p)
        for k, arr in m.items():
            good, det = touch_ok(k, arr, False)
            ok = ok and good
            T(G, '%s %s 누름 높이 ≥ 36' % (dn, k), good, det)
        p.close()
    pn, pb = dev_page(br, tag + 'pcN', src, PC), dev_page(br, tag + 'pcB', base_src, PC)
    mn, mb = meas_book(pn), meas_book(pb)
    for k in mn:
        same, det = pc_same(mn[k], mb[k])
        ok = ok and same
        T(G, 'PC %s = 바탕' % k, same, det)
    pn.close()
    pb.close()
    return ok


def b5(br, src, tag):
    G = 'B5'
    p = Pg(br, 'chromium', tag, src, 390, 844, touch=True, dsf=2)
    ok = True
    for y, pg in (('2009', 0), ('2013', 2), ('2026', 0)):
        exv_open(p, y, pg, direct=True)   # 착수 판 폰은 1차객 서랍이 첫 화면을 118px 로 눌러 해 줄 누름이 빗나간다(A-6) → 줄 누름과 같은 함수로 연다
        h = p.ev(EXV_HEAD)
        good = bool(h) and h['sw'] >= 0 and h['sw'] <= h['cw'] and re.search(r'\d{4}년 제\d+회', h['t'] or '') is not None
        ok = ok and good
        T(G, '폰 390 기출뷰 %s 머리 「NNNN년 제NN회」 잘림 없음' % y, good, h)
    p.close()
    return ok


B6M = r"""() => { const m = document.querySelector('#slot .main') || document.querySelector('#slot > div:not(#jtree)'); const t = document.getElementById('jtree');
  const R = e => { const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; };
  const hb = document.querySelector('#slot .mbsbar');   /* 카드 쪽 머리 막대(← 목차 · 마디 이름 · 문제 N-M / 총 K · ✏️ 표시 · 📝 OMR) */
  const hd = hb ? [...hb.querySelectorAll('button, .pg, .t1, .t2, .tw, .r > *')].filter(e => __RB.vis(e) && e.getBoundingClientRect().width > 0) : [];
  let ov = 0; const pairs = [];
  for (let i = 0; i < hd.length; i++) for (let j = i + 1; j < hd.length; j++){ const a = hd[i], b = hd[j]; if (a.contains(b) || b.contains(a)) continue; const p = R(a), q = R(b);
    const ix = Math.min(p[2], q[2]) - Math.max(p[0], q[0]), iy = Math.min(p[3], q[3]) - Math.max(p[1], q[1]); if (ix > 1 && iy > 1){ ov++; if (pairs.length < 3) pairs.push(__RB.txt(a).slice(0, 10) + '×' + __RB.txt(b).slice(0, 10)); } }
  const jr = t ? t.getBoundingClientRect() : null, mr = m ? m.getBoundingClientRect() : null;
  return {mok: S.mok, head: hd.length, main: mr ? Math.round(mr.width) : null, mainL: mr ? Math.round(mr.left) : null, jt: t ? {w: Math.round(jr.width), fold: t.classList.contains('fold'), pos: getComputedStyle(t).position, disp: getComputedStyle(t).display} : null,
    cards: document.querySelectorAll('#slot .qwrap').length, ov, pairs}; }"""


def b6_flow(br, src, tag, eng='chromium'):
    """새로 열기 → 레일 1차객 → 첫 화면 → (접혀 있으면 손잡이로 펴고) 서랍 첫 마디 → 카드 쪽"""
    p = Pg(br, eng, tag, src, 390, 844, touch=True, dsf=2)
    at = p.ev("() => { const b = [...document.querySelectorAll('#hrail .rb, #hrail button')].find(x => /1차객/.test(x.textContent)); return b ? __RB.hitOn(b) : null; }")
    p.press(at, 2500)
    p.pg.wait_for_function("() => document.querySelector('#slot .mbdash')", timeout=60000)
    p.idle(400)
    first = p.ev(B6M)
    if first['jt'] and first['jt']['fold']:   # 접힌 채면 손잡이로 편다(사용자 손길)
        g = p.ev("() => __RB.hitOn(document.getElementById('jtgrip'))")
        p.press(g, 800)
    row = p.ev("() => { const r = [...document.querySelectorAll('#jtlist .jtit:not(.off)')].filter(__RB.vis)[0]; return r ? __RB.hitOn(r) : null; }")
    p.press(row, 2500)
    p.idle(500)
    p.pg.wait_for_function("() => document.querySelectorAll('#slot .qwrap').length > 0", timeout=60000)
    p.idle(400)
    card = p.ev(B6M)
    errs = p.errs[:]
    p.close()
    return first, card, errs


def b6(br, src, base_src, tag, eng='chromium'):
    """A-6 폰 1차객 문제 서랍 — 사용자 손길로 재현(바탕) · 재현되면 새 판 카드 칸 ≥ 374 · 겹침 0"""
    G = 'B6' if eng == 'chromium' else 'B6-wk'
    if base_src is not None:
        f0, c0, _ = b6_flow(br, base_src, tag + 'B', eng)
        rep = c0['main'] is not None and c0['main'] < 374
        N(G, '재현(착수 판 · 사용자 손길)', '%s — 첫 화면 카드 칸 %s · 서랍 %s → 서랍 마디 → 카드 칸 %s · 머리 겹침 %d(머리 요소 %d) %s' % ('재현됨' if rep else '재현 안 됨', f0['main'], f0['jt'], c0['main'], c0['ov'], c0['head'], c0['pairs']))
    first, card, errs = b6_flow(br, src, tag, eng)
    good = card['main'] is not None and card['main'] >= 374 and card['ov'] == 0 and card['cards'] > 0 and card['head'] >= 3
    T(G, '카드 칸 ≥ 374 · 머리 겹침 0', good, {'머리 요소': card['head'], '첫 화면': first['main'], '서랍(첫 화면)': first['jt'], '카드 칸': card['main'], '겹침': card['ov'], '예': card['pairs'], '서랍': card['jt'], '카드': card['cards']})
    T(G, 'JS 오류', not errs, errs[:3])
    return good and not errs


LINK = r"""(needle) => { const box = document.querySelector('#slot .main .box'); const r = __RB.findText(box, needle); if (!r) return null;
  const e = r.startContainer.parentElement, lk = e.closest('.wmlk'); (lk || e).scrollIntoView({block:'center'});
  const fs = [...(lk || e).getClientRects()].filter(x => x.width > 0), q = fs[0], bx = box.getBoundingClientRect();
  return {cx: q.left + Math.min(q.width, 30) / 2 + 1, cy: q.top + q.height / 2, on: true, lines: fs.map(f => [bx.left, f.top, bx.right, f.bottom]), wmlk: !!lk}; }"""
POPR = r"""() => { const p = POPS.filter(x => (x._pk || '').indexOf('jo|') === 0).pop(); if (!p) return null; const r = p.getBoundingClientRect(); const B = __RB.vv();
  return {rect: [r.left, r.top, r.right, r.bottom], vv: [B.w, B.h], title: (p.querySelector('.pt') || {}).textContent}; }"""


def ovl(a, b):
    return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))


def b7(br, src, tag):
    """A-7 조문 팝업 자리 = 링크 아래 → 위 → 넓은 쪽 줄여서 → 가운데 · 누른 링크 줄과 겹침 0 · 화면 안"""
    G = 'B7'
    ok = True
    for (W, Hh) in ((1511, 1043), (1440, 900)):
        p = Pg(br, 'chromium', tag, src, W, Hh)
        for needle in ('제55조제1항', '제132조의17'):
            p.ev("async () => await __RB.jo('특허법', '제6조', true)")
            at = p.ev(LINK, needle)
            p.click(at['cx'], at['cy'], 900)
            q = p.ev(POPR)
            o = sum(ovl(q['rect'], L) for L in at['lines']) if q else -1
            good = bool(q) and at['wmlk'] and o == 0 and q['rect'][1] >= 0 and q['rect'][3] <= Hh + 0.5
            ok = ok and good
            T(G, '%d×%d 제6조 「%s」' % (W, Hh, needle), good, {'팝업': q and [round(v) for v in q['rect']], '링크 줄': [round(v) for v in at['lines'][0]], '겹침': o})
        for which in ('제1조', '제200조', 'last'):
            p.ev("async () => await __RB.jo('특허법', '제6조', true)")
            at = p.ev(r"""(k) => { const rows = [...document.querySelectorAll('.tree .r[data-jo]')]; const r = k === 'last' ? rows[rows.length - 1] : rows.find(x => x.dataset.jo === k); if (!r) return null;
               const no = r.querySelector('.jno'); const tr = document.querySelector('#slot > .tree'); if (k === 'last') tr.scrollTop = tr.scrollHeight; else no.scrollIntoView({block:'center'});
               const q = no.getBoundingClientRect(); return {cx: q.left + q.width / 2, cy: q.top + q.height / 2, on: true, rect: [q.left, q.top, q.right, q.bottom], k: r.dataset.jo}; }""", which)
            p.click(at['cx'], at['cy'], 900)
            q = p.ev(POPR)
            o = ovl(q['rect'], at['rect']) if q else -1
            good = bool(q) and o == 0 and q['rect'][1] >= 0 and q['rect'][3] <= Hh + 0.5
            ok = ok and good
            T(G, '%d×%d 서랍 조 번호 %s' % (W, Hh, at['k']), good, {'팝업': q and [round(v) for v in q['rect']], '조 번호': [round(v) for v in at['rect']], '겹침': o})
        if p.errs:
            ok = False
            T(G, 'JS 오류 %d' % W, False, p.errs[:3])
        p.close()
    return ok


def b8(br, src, base_src, tag):
    G = 'B8'
    ok = True
    for dn, dev in TOUCH_DEV:
        p = dev_page(br, tag + dn, src, dev)
        m = meas_six(p)
        for nm, sel, same, need_w in SIX:
            good, det = touch_ok(nm, m[nm], need_w)
            ok = ok and good
            T(G, '%s %s 누름 ≥ 36' % (dn, nm), good, det)
        ck = all(x['center'] for x in m['체크']) and all(x['center'] for x in m['조 번호'])
        ok = ok and ck
        T(G, '%s 체크 가운데 = 체크 · 조 번호 가운데 = 조 번호' % dn, ck, [(x['t'], x['center']) for x in m['체크'][:3] + m['조 번호'][:2]])
        p.close()
    pn, pb = dev_page(br, tag + 'pcN', src, PC), dev_page(br, tag + 'pcB', base_src, PC)
    mn, mb = meas_six(pn), meas_six(pb)
    for nm, _, _, _ in SIX:
        same, det = pc_same(mn[nm], mb[nm])
        ok = ok and same
        T(G, 'PC %s = 착수 판' % nm, same, det)
    pn.close()
    pb.close()
    return ok


DEAD_CSS = ['.bjnote', '.hangchip', '.modebar .mode .mkn', '.modebar .mode.on .mkn']


def b9(br, src, tag):
    G = 'B9'
    p = Pg(br, 'chromium', tag, src, 1511, 1043)
    step = "() => { const b = document.querySelector('.tree .jtbar .jstep'); return b ? b.textContent : null; }"
    p.ev("async () => { localStorage.removeItem('jopangi_ui_jofold'); await __RB.jo('특허법', '제2조', true); }")
    for _ in range(3):
        t = p.ev(step)
        p.ev("() => document.querySelector('.tree .jtbar .jstep').click()")
        p.idle(300)
        if t == '접기2':
            break
    st = p.ev(step)
    p.ev("async () => { S.jo = '제192조'; await render(); }")
    p.idle(300)
    t1 = p.ev(step)
    p.ev("async () => { await render(); }")
    p.idle(300)
    t2 = p.ev(step)
    ok1 = st == '펴기' and t1 == t2 and t1 is not None
    T(G, '접기2 → 제192조 첫 렌더 글자 = 그 상태의 다음 누름 글자', ok1, {'접기2 뒤': st, '첫 렌더': t1, '다시 그림(지금 상태로 센 글자)': t2})
    cnt = {c: src.count(c) for c in DEAD_CSS}
    ok2 = not any(cnt.values())
    T(G, '걷은 CSS 선택자 소스 0', ok2, cnt)
    p.close()
    return ok1 and ok2


AUTO_JS = r"""async (law) => {
  const L = await get('jo_' + law + '_목록.json'), B = await get('jo_' + law + '_본문.json'); const TT = {}; L.조.forEach(x => { TT[x.k] = x.t || ''; });
  const oldOut = (j, jo) => { const j2 = Object.assign({}, j, { 원본: wmOrig(j) }); const J2 = new Proxy({}, { get: (o, kk) => kk === jo ? j2 : undefined }); let b; try{ b = wmBuild(J2, jo); }catch(e){ return []; } const out = [];
    b.lines.forEach(Ln => { if (Ln.cls === 'tail' || Ln.cls === 'emb' || Ln.cls === 'fd') return; (Ln.L || []).forEach(l => { if (!l.j || l.j === jo || out.indexOf(l.j) >= 0) return; if ((Ln.ch || []).some(c => c[3] === 'b' && c[1] >= l.a && c[1] < l.b)) out.push(l.j); }); }); return out; };
  const changed = [], ctx = [], vault = [];
  for (const x of L.조){ const jo = x.k, j = B.조[jo]; if (!j) continue; const o = oldOut(j, jo), n = (typeof wmAutoLinks === 'function') ? wmCiteOut(j, jo, TT) : o;
    if (o.length !== n.length || o.some(k => n.indexOf(k) < 0)) changed.push([jo, o.length, n.length, n.filter(k => o.indexOf(k) < 0).join('·')]);
    if (typeof wmAutoLinks !== 'function') continue;
    const j2 = Object.assign({}, j, { 원본: wmOrig(j) }); const J2 = new Proxy({}, { get: (oo, kk) => kk === jo ? j2 : undefined }); let b; try{ b = wmBuild(J2, jo); }catch(e){ continue; }
    b.lines.forEach(Ln => { if (Ln.cls === 'tail' || Ln.cls === 'emb' || Ln.cls === 'fd') return; const ch = Ln.ch || [], os = ch.filter(c => c[3] !== 'r').map(c => c[0]).join('');
      if (!(Ln.L && Ln.L.length)) wmAutoLinks(os, jo, TT).forEach(a => ctx.push([jo, a.j, os.slice(Math.max(0, a.s - 160), a.s), os.slice(a.s, a.e)]));
      (Ln.L || []).forEach(l => { const pos = []; let oi = 0; ch.forEach(c => { if (c[3] !== 'r'){ if (c[1] >= l.a && c[1] < l.b) pos.push(oi); oi++; } }); if (pos.length) vault.push([jo, l.j, os.slice(Math.max(0, pos[0] - 160), pos[0]), os.slice(pos[0], pos[pos.length - 1] + 1)]); }); });
  }
  return { changed, ctx, vault }; }"""


def other_law(pre):
    """다른 법 인용인가(하네스 쪽 따로 짠 판정 · 앱 wmAutoOther 와 따로) — 앞에서 인용 연쇄를 한 토막씩 걷고 「…」 · 같은/동 + 법·조약·협정 … · 시행령·시행규칙으로 끝나면"""
    t = pre
    tok = re.compile(r'(?:\s+|ㆍ|·|,|및|또는|와|과|이나|부터|까지|내지|~|\(|\([^()]*\)|제\d+조(?:의\d+)?(?:제\d+항)?(?:제\d+호(?:의\d+)?)?(?:제\d+목)?(?:\(\d+\))?|제\d+(?:편|장|절|관|항|목)|제\d+호(?:의\d+)?)$')
    for _ in range(200):
        m = tok.search(t)
        if not m or m.start() == len(t):
            break
        t = t[:m.start()]
    return t.endswith('」') or re.search(r'(?:같은|동)\s*(?:법률|법|영|규칙|조약|협정|의정서|협약)$', t) is not None or re.search(r'(?:시행령|시행규칙)$', t) is not None


def b10(br, src, tag):
    G = 'B10'
    p = Pg(br, 'chromium', tag, src, 1511, 1043)
    p.ev("async () => await __RB.jo('특허법', '제217조', true)")
    d217 = p.ev(r"""async () => { const B = await get('jo_특허법_본문.json'); const lk = [...document.querySelectorAll('#slot .main .box .wmlk')].map(e => __RB.txt(e));
      return {chip: __RB.txt(document.querySelector('#slot .conn .plgb.wmin')), outs: wmCiteOut(B.조['제217조'], '제217조'), links: lk}; }""")
    ok1 = bool(d217) and '제164조의2' in d217['outs'] and any(t.startswith('제164조의2') for t in d217['links'])
    T(G, '특허 제217조 🔗인 에 제164조의2(셈 · 원문 링크)', ok1, d217)
    # 링크 누름 = 원문 팝업
    at = p.ev(r"""() => { const e = [...document.querySelectorAll('#slot .main .box .wmlk')].find(x => __RB.txt(x).startsWith('제164조의2')); return e ? __RB.hitOn(e) : null; }""")
    pop = None
    if at:
        p.press(at, 900)
        pop = p.ev(POPR)
    T(G, '제164조의2 링크 누름 = 원문 팝업', bool(pop) and '제164조의2' in (pop['title'] or ''), pop and pop['title'])
    p.ev("async () => await __RB.jo('특허법', '제6조', true)")
    c6 = p.ev("() => __RB.txt(document.querySelector('#slot .conn .plgb.wmin'))")
    T(G, '제6조 🔗인2 무변', c6 == '🔗인2', c6)
    ok3 = True
    oth_auto, oth_vault, chg = 0, {}, {}
    for law in ('특허법', '상표법', '디자인보호법', '민사소송법'):
        r = p.ev(AUTO_JS, law)
        chg[law] = r['changed']
        bad = [c for c in r['ctx'] if other_law(c[2])]
        oth_auto += len(bad)
        oth_vault[law] = [(c[0], c[3], '→' + c[1]) for c in r['vault'] if other_law(c[2])]
        N(G, '%s 바뀐 🔗인 셈 %d조' % (law, len(r['changed'])), ' · '.join('%s %d→%d(+%s)' % tuple(c) for c in r['changed']) or '없음')
        if bad:
            N(G, '%s 다른 법 자동 링크' % law, bad[:5])
    ok3 = oth_auto == 0
    T(G, '다른 법 인용에 새로 건 링크 0(네 법)', ok3, oth_auto)
    N(G, '볼트에 원래 있던 다른 법 링크(짝 맞은 줄 = 무변 규칙 · 바꾸지 않음)', {k: v for k, v in oth_vault.items() if v})
    T(G, 'JS 오류', not p.errs, p.errs[:3])
    p.close()
    return ok1 and c6 == '🔗인2' and ok3 and not p.errs, chg


B11Q = r"""() => { const t = document.querySelector('#slot > .tree'); if (!t) return null; const heads = [...t.querySelectorAll('.r.jhead')];
  const empty = heads.filter(h => { const r = h.querySelector('.jrange'); return r && /^\s*~?\s*$/.test(r.textContent); }).map(h => __RB.txt(h).slice(0, 20));
  const rng = {}; heads.forEach(h => { const n = __RB.txt(h.querySelector('.nm')).replace(/^[▾▸]\s*/, ''); const r = h.querySelector('.jrange'); rng[n.slice(0, 5)] = r ? r.textContent : null; });
  return { w: t.clientWidth, sw: t.scrollWidth, heads: heads.length, empty, rng }; }"""


def b11(br, src, tag):
    G = 'B11'
    ok = True
    for nm, dev, tw in (('폰390', PHONE, None), ('iPad834', PAD, None), ('PC212', PC, 212), ('PC276', PC, 276), ('PC320', PC, 320)):
        p = dev_page(br, tag + nm, src, dev)
        for law in ('특허법', '상표법', '디자인보호법', '민사소송법'):
            p.ev("async a => { localStorage.removeItem('jopangi_ui_jofold'); if (a[1]) { S.treeW = a[1]; document.documentElement.style.setProperty('--trw', a[1] + 'px'); } await __RB.jo(a[0], '제1조', true); }", [law, tw])
            q = p.ev(B11Q)
            good = bool(q) and q['sw'] <= q['w'] and not q['empty']
            extra = {}
            if law == '민사소송법':
                extra = {k: q['rng'].get(k) for k in ('제2편 제', '제3편 상')}
                good = good and all(v and re.match(r'^제\d+조(의\d+)?~제\d+조(의\d+)?$', v) for v in extra.values())
            ok = ok and good
            T(G, '%s %s 서랍' % (nm, law), good, {'폭': q and q['w'], '내용 폭': q and q['sw'], '빈 범위': q and q['empty'], **extra})
        p.close()
    return ok


def sweep_screens(br, src, tag, dev):
    """B-12 화면 훑기 한 기기 — {화면: [흠 이름표]}"""
    p = dev_page(br, tag, src, dev)
    touch = dev in (PHONE, PAD)
    out = {}
    sw = lambda sel: p.ev("a => __RB.sweep(a[0], a[1])", [sel, touch])
    p.ev("async () => await __RB.home('특허법')")
    p.ev("async k => await __RB.goKey(k)", U_PIN)
    out['1차객 카드'] = sw('#slot')
    open_box(p, U_PIN, 400, False)
    out['교재 자리 창(그림 없음)'] = sw('.pop.k-cell')
    p.ev("a => __RB.pinSeed(a[0], a[1], a[2])", [U_PIN, PIN_P, PIN_R])
    p.ev("async k => await __RB.goKey(k)", U_PIN)
    open_box(p, U_PIN, 400, True)
    out['교재 자리 창(그림)'] = sw('.pop.k-cell')
    p.ev("() => __RB.closeBox()")
    exv_open(p, '2013', 2, direct=True)
    out['기출뷰'] = sw('#slot')
    p.ev("async () => await __RB.jo('특허법', '제6조', true)")
    out['조문 화면(서랍)'] = sw('#slot > .tree')
    p.ev("async () => await __RB.jo('특허법', '제6조', false)")
    out['조문 화면(연결 줄·모드 줄·원문)'] = sw('#slot .main')
    at = p.ev(LINK, '제55조제1항')
    p.press(at, 900)
    out['조문 팝업'] = sw('.pop')
    p.ev("() => closeAllPops(true)")
    pos = p.ev(r"""() => { const box = document.querySelector('#slot .main .box'); const r = __RB.findText(box, '대리인'); r.startContainer.parentElement.scrollIntoView({block:'center'}); const q = r.getBoundingClientRect(); return {x: q.left + q.width / 2, y: q.top + q.height / 2}; }""")
    if touch:
        long_press(p, pos['x'], pos['y'])
    else:
        p.pg.mouse.move(pos['x'] - 20, pos['y'])
        p.pg.mouse.down()
        p.pg.mouse.move(pos['x'] + 20, pos['y'])
        p.pg.mouse.up()
        p.wait(500)
    out['칠 막대'] = sw('.mk9bar, #c2mark')
    errs = p.errs[:]
    p.close()
    return out, errs


def b12(br, src, base_src, tag):
    G = 'B12'
    ok = True
    for dn, dev in (('PC', PC), ('폰390', PHONE), ('iPad834', PAD)):
        n, en = sweep_screens(br, src, tag + 'N' + dn, dev)
        b, eb = sweep_screens(br, base_src, tag + 'B' + dn, dev)
        for scr in n:
            new = sorted(set(n[scr]) - set(b.get(scr, [])))
            gone = sorted(set(b.get(scr, [])) - set(n[scr]))
            good = not new
            ok = ok and good
            T(G, '%s %s 새로 생긴 흠 0' % (dn, scr), good, {'새로': new[:6], '없어짐': len(gone), '남은(바탕에도 있음)': len(set(n[scr]) & set(b.get(scr, [])))})
        if en:
            ok = False
            T(G, '%s JS 오류' % dn, False, en[:3])
    return ok


def webkit_try(pw):
    try:
        return pw.webkit.launch()
    except Exception as e:
        N('WK', 'WebKit 안 잼', str(e).splitlines()[0][:160])
        return None


def main():
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    if YARD:
        src = app_src(BASE)
        base_src = src
        print('헛잣대 — 앱 = %s(착수 판) · B-1~B-12 가 저마다 FAIL 해야 통과' % BASE)
    else:
        src, base_src = app_src(NEW), app_src(BASE)
        print('관문 _task_jo_revfix0929b · 앱 = %s · 바탕 = %s' % (NEW, BASE))
    got = {}
    extra = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        steps = [('B1', lambda: b1(br, app_src(ARG('--yard1', 'c3c33ca')) if YARD else src, 'b1')),
                 ('B2', lambda: b2(br, src, 'b2')),
                 ('B3', lambda: b3(br, src, base_src, 'b3')),
                 ('B4', lambda: b4(br, src, base_src, 'b4')),
                 ('B5', lambda: b5(br, src, 'b5')),
                 ('B6', lambda: b6(br, src, None if YARD else base_src, 'b6')),
                 ('B7', lambda: b7(br, src, 'b7')),
                 ('B8', lambda: b8(br, src, base_src, 'b8')),
                 ('B9', lambda: b9(br, src, 'b9')),
                 ('B10', lambda: b10(br, src, 'b10')),
                 ('B11', lambda: b11(br, src, 'b11')),
                 ('B12', lambda: b12(br, src, base_src, 'b12'))]
        for g, fn in steps:
            if ONLY and g not in ONLY:
                continue
            if YARD and g == 'B12':
                N(g, '헛잣대 해당 없음', '화면 훑기 = 새 판 흠 − 바탕 흠 · 바탕끼리 견주면 늘 0(잣대가 아니라 잠금)')
                continue
            print('── %s' % g, flush=True)
            t1 = time.time()
            try:
                r = fn()
                if isinstance(r, tuple):
                    extra[g] = r[1]
                    r = r[0]
                got[g] = bool(r)
            except Exception as e:
                got[g] = False
                T(g, '돌다 멈춤', False, str(e).splitlines()[0][:300])
            print('   (%s %.0f초)' % (g, time.time() - t1), flush=True)
        br.close()
        if 'webkit' in ENGS and not YARD and (not ONLY or 'WK' in ONLY):
            wk = webkit_try(pw)
            if wk:
                for g, fn in (('B4', lambda: b4(wk, src, base_src, 'wk4')), ('B6', lambda: b6(wk, src, None, 'wk6', 'webkit')), ('B8', lambda: b8(wk, src, base_src, 'wk8'))):
                    try:
                        fn()
                    except Exception as e:
                        T(g + '-wk', 'WebKit 돌다 멈춤', False, str(e).splitlines()[0][:200])
                wk.close()
    # 회귀(규칙 57) — main 쪽 하네스는 N:(JOP · r'jo\data' 한 덩이 조각)라 cloud 에서 못 돈다
    for h in ('_harness_jo_book8.py', '_harness_jo_revfix0928night.py', '_harness_jo_revfix0929.py', '_harness_jo_uid_add3.py', '동기화 jo'):
        N('회귀', h, 'N: 필요 — 합칠 때 본 세션')
    lines = []
    print('\n══ 요약 (%.0f초)%s' % (time.time() - t0, ' — 헛잣대' if YARD else ''))
    for g in sorted(got, key=lambda x: int(x[1:])):
        cells = [r for r in RES if r[0] == g and r[2] is not None]
        nf = sum(1 for r in cells if not r[2])
        if YARD:
            verdict = 'FAIL(헛잣대 통과)' if not got[g] else 'PASS(헛잣대 실패)'
            if g == 'B1':
                verdict += ' · 앱 = %s(jo_revfix0929 전 판 · A-1 은 코드 무변 잠금)' % ARG('--yard1', 'c3c33ca')
        else:
            verdict = 'PASS' if got[g] else 'FAIL'
        s = '  %-4s %s (%d 칸 중 FAIL %d)' % (g, verdict, len(cells), nf)
        print(s)
        lines.append(s)
    with open(OUTF, 'w', encoding='utf-8', newline='\n') as f:
        for r in RES:
            d = r[3] if isinstance(r[3], str) else json.dumps(r[3], ensure_ascii=False, default=str)
            f.write('%s | %s · %s | %s\n' % ('INFO' if r[2] is None else ('PASS' if r[2] else 'FAIL'), r[0], r[1], d))
        f.write('\n'.join(lines) + '\n')
    print('결과 → %s' % OUTF)


if __name__ == '__main__':
    main()
