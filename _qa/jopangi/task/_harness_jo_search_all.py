# -*- coding: utf-8 -*-
r"""_task_search_all §B 관문 — 조판기(jo) 검색 결과를 자르지 않고 다 보이기(2026-10-10 · 로컬 워크트리 하위 에이전트)

  자리(spot) 18 = 지시서 §0-3 넷(ggFindRun · mbSearchRun · c2EditWin · popJimun/H.slice) + 착수 grep 으로 더한 열넷(같은 꼴 · 검색 결과 목록만):
    gg  근거에서 찾기(ggFindRun · 옛 60)            mb  1차객 🔍 검색(mbSearchRun · 옛 200)       c2e ✎ 연결 카드 찾기(c2EditWin · 옛 30)
    sk.jo · sk.prec · sk.jimun · sk.memo · sk.claude · sk.omr · sk.stk  통합 검색(skRun) 갈래 일곱(옛 40 · 40 더 보기 · 30/60 · 30 · 30 · 30+40 · 30)
    pl  판례 링크 창 「찾아서 넣기」(plPrecSearchBox · 옛 30)   c2r 「+ 2차 잇기」 카드 찾기(옛 20)   c2q 2차 설문 「+ 잇기」(c2QlMenu · 옛 60)
    c2s 2차 🔍 검색 칸(c2SrPanel · 옛 80)            cf  1차객 🔗 연결 창(cfFind · 옛 30)
    cvl 정리캔버스 블록 「찾아서 잇기」(옛 20)        cvp 정리캔버스 판례 「🔍 찾아서 넣기」(precSearchAll · 옛 12)   cvb 교재 창 찾기(cvbFind · 옛 100쪽)
  잣대(자리마다 · §B-1~5 · 7) — 기대 수 = 하네스가 앱 거르기 식과 같은 식으로 데이터를 직접 거른 수(앱의 바뀐 그리기 길을 안 거침)
    A 셈 글 = 기대 수 · B 처음 줄 = min(기대, 처음 수) · 끝 표지 · C 진짜 굴림 → 다음 줄이 붙는다(끝 표지를 굴림 칸 아래 700px 에 두고
    PC 마우스 휠 / 폰 CDP Input.dispatchTouchEvent 손가락 끌기 — synthesizeScrollGesture 는 이 헤드리스에서 0px 이라 안 씀) · C2 붙인 뒤 굴림 자리 그대로(맨 위로 튀지 않음) ·
    D 끝까지 굴려 붙은 줄 = 기대 수 · 끝 표지 0 · E 검색어 바꾸기(긴 결과 굴리는 중) = 바로 min(기대2, 처음 수) · 700ms 뒤 그대로 · 끝까지 = 기대2(옛 줄 섞임 0) ·
    F 검색 칸(mb · sk.* · c2s · cvb) 첫 그림(입력 → 처음 줄 · 세 번 가운데 값) ≤ 바탕 × 1.2 또는 늘어난 것 ≤ 한 프레임 16.7ms · 찾기 창 여덟 = §A-5 「늘어난 시간을 잼」(INFO) ·
    G 화면 훑기(PC · 폰) — 문서 넘침 · 창 화면 밖 · 셈 줄 · 끝 줄 · 새로 넘친 것 0(줄 안 white-space:nowrap 글이 넘치는 옛 줄 꼴은 G2 INFO · 바탕 맞대기) ·
    H 마지막 줄 누름(mb · sk.jimun · gg · cf · 진짜 마우스) = 그 항목
  헛잣대 = 바탕(--base · 없으면 7299ec3 = 이 판 분기점 · 합친 뒤에도 같은 판) — 자리마다 D 가 FAIL 이어야 잣대다(자르던 수에서 멈춤).
  엔진 = Chromium PC 1100×800(마우스) + 폰 390×844 hasTouch(CDP 손가락 끌기) · WebKit = 폰 390 굴림 칸만(mb · sk.jimun · cf — playwright webkit 은 터치 끌기가 없어 휠)
  網 = 같은 출처만(SEED 가 fetch 를 돌린다 · 기록.json = 메모리 · 교재 = /__book/ ← MBPDF_ROOT · pdf.js = /__vendor/ ← cdnjs 3.11.174 자기 사본 · 그 밖 = 404)
  기록 심기(하네스 페이지 안에서만) — 근거 250 · 메모 250 · Claude 답 250 · 스티커 120(검색어 「하네스찾기」) · 「.gt」 잴 연결 근거 하나

  모드(_qa_jo_common): gate(인자 없음) = 바탕 띄움 · 헛잣대 · 빠르기 / regress = 새 판만(A~E · G · H) / smoke = 새 판 PC 의 mb · sk.jimun 만
쓰기: python _harness_jo_search_all.py [--new 파일] [--base 커밋] [--res 결과파일] [--only gg,mb,…] [--eng chromium,webkit] [--mode gate|regress|smoke]
"""
import os as _os_r, sys as _sys_r   # env_lanes — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402 — --mode · --snap-in · --snap-out 을 여기서 뗀다(gate = 인자 없음)
import http.server, io, json, os, shutil, socketserver, statistics, subprocess, sys, tempfile, threading, time, urllib.parse, urllib.request   # noqa: E402
from playwright.sync_api import sync_playwright   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


HERE = os.path.dirname(os.path.abspath(__file__))
GENIE = _roots.genie()
JOD = os.path.join(GENIE, 'jo')
DATA = os.path.join(JOD, 'data')
MB = _roots.mbpdf()
NEWF = ARG('--new', os.path.join(JOD, 'index.html'))
BASE_REV = ARG('--base', '') or '7299ec3'   # 헛잣대 판 = 이 판 바로 앞(워크트리 분기점 7299ec3 · jo/index.html LF md5 2f9de6af) — 합친 뒤 main 에서 _roots.base_rev() 는 HEAD(새 판)라 박아 둔다
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_search_all_result.txt'))
ONLY = [x.strip() for x in (ARG('--only', '') or '').split(',') if x.strip()]
ENGS = [x.strip() for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x.strip()]
SHOT = ARG('--shot', '')   # .gt 폰 그림을 둘 자리(없으면 안 찍음)
TMP0 = os.path.join(tempfile.gettempdir(), 'h_josearch')
WORK = os.path.join(TMP0, 'run%d' % os.getpid())
VENDOR = os.path.join(TMP0, 'vendor')
PDFJS = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/'
PC, PHONE = (1100, 800), (390, 844)
SPOTS = ['gg', 'mb', 'c2e', 'sk.jo', 'sk.prec', 'sk.jimun', 'sk.memo', 'sk.claude', 'sk.omr', 'sk.stk',
         'pl', 'c2r', 'c2q', 'c2s', 'cf', 'cvl', 'cvp', 'cvb']
SMOKE_SPOTS = ['mb', 'sk.jimun']
WK_SPOTS = ['mb', 'sk.jimun', 'cf']
FIRST = {'mb': 200}        # 처음 그릴 수 = max(옛 자르던 수, 100)
CAP = {'gg': 60, 'mb': 200, 'c2e': 30, 'sk.jo': 40, 'sk.prec': 40, 'sk.jimun': 60, 'sk.memo': 30, 'sk.claude': 30, 'sk.omr': 70, 'sk.stk': 30,
       'pl': 30, 'c2r': 20, 'c2q': 60, 'c2s': 80, 'cf': 30, 'cvl': 20, 'cvp': 12, 'cvb': 100}
LAST = ('mb', 'sk.jimun', 'gg', 'cf')
DEB = {'gg': '120ms', 'mb': '140ms', 'pl': '120ms', 'cf': '120ms', 'c2s': '120ms'}   # 입력 뒤 늦춤(앱 그대로) · sk.* = 300ms
SEARCHBOX = ('mb', 'sk.jo', 'sk.prec', 'sk.jimun', 'sk.memo', 'sk.claude', 'sk.omr', 'sk.stk', 'c2s', 'cvb')   # §B-5 「검색 칸 입력 → 첫 100 줄」 = 검색 칸 · 나머지(연결 · 근거 · 잇기 창 찾기)는 §A-5 「늘어난 시간을 잼」(INFO)
RES = []
SERVERS = {}


def first_of(s):
    return FIRST.get(s, 100)


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, d[:400]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('INFO | %s · %s | %s' % (grp, name, d[:600]), flush=True)


def git(*a):
    return subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a), capture_output=True)


def vendor():
    os.makedirs(VENDOR, exist_ok=True)
    ok = True
    for f in ('pdf.min.js', 'pdf.worker.min.js'):
        p = os.path.join(VENDOR, f)
        if os.path.isfile(p) and os.path.getsize(p) > 100000:
            continue
        try:
            with urllib.request.urlopen(PDFJS + f, timeout=60) as r:
                b = r.read()
            open(p, 'wb').write(b)
        except Exception as e:
            ok = False
            print('INFO | 준비 · pdf.js 사본 못 받음 | %s %s' % (f, e), flush=True)
    return ok


SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.alert=function(){};window.confirm=function(){return true;};window.prompt=function(){return null;};
(function(){var nf=window.fetch.bind(window);
window.fetch=function(u,o){o=o||{};var s=String((u&&u.url)||u);
 var bk=s.indexOf('api.github.com/repos/zzikkaplan/minbeoppdf/contents/');
 if(bk>=0){var rest=s.slice(bk+'api.github.com/repos/zzikkaplan/minbeoppdf/contents/'.length).split('?')[0];return nf(location.origin+'/__book/'+rest,{headers:{}});}
 if(/cdnjs\.cloudflare\.com\/ajax\/libs\/pdf\.js\/3\.11\.174\//.test(s))return nf(location.origin+'/__vendor/'+s.split('/pdf.js/3.11.174/')[1],o);
 if(/\/contents\/jopangi\/(%EA%B8%B0%EB%A1%9D|기록)\.json/.test(s)){var R=window.__REMOTE;
  if((o.method||'GET')==='PUT'){var b=JSON.parse(o.body||'{}');if(!R)R=window.__REMOTE={text:null,sha:null,puts:0};
   if(R.sha&&b.sha!==R.sha)return Promise.resolve(new Response('{"message":"conflict"}',{status:409}));
   R.text=decodeURIComponent(escape(atob(b.content)));R.puts=(R.puts||0)+1;R.sha='H'+R.puts+'_'+Date.now();
   return Promise.resolve(new Response(JSON.stringify({content:{sha:R.sha}}),{status:200,headers:{'Content-Type':'application/json'}}));}
  if(!R||R.text==null)return Promise.resolve(new Response('{"message":"Not Found"}',{status:404}));
  var acc=((o.headers||{}).Accept||'');
  if(acc.indexOf('raw')>=0)return Promise.resolve(new Response(R.text,{status:200}));
  return Promise.resolve(new Response(JSON.stringify({sha:R.sha}),{status:200,headers:{'Content-Type':'application/json'}}));}
 if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)return Promise.resolve(new Response('{"message":"Not Found"}',{status:404,headers:{'Content-Type':'application/json'}}));
 return nf(u,o);};
try{localStorage.clear();}catch(e){}
try{localStorage.setItem('tt.cfg',JSON.stringify({token:'harness-token',person:'꼬까'}));}catch(e){}
})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
</script>
<script src="/__vendor/pdf.min.js"></script>
<script>try{pdfjsLib.GlobalWorkerOptions.workerSrc=location.origin+'/__vendor/pdf.worker.min.js';}catch(e){__ERR.push('pdfjs vendor '+e);}</script>"""

TOOLS = r"""<script>
(function(){
const wait = ms => new Promise(r => setTimeout(r, ms));
const raf = () => new Promise(r => requestAnimationFrame(() => r()));
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); return { x: +r.left.toFixed(1), y: +r.top.toFixed(1), w: +r.width.toFixed(1), h: +r.height.toFixed(1), r: +r.right.toFixed(1), b: +r.bottom.toFixed(1), cx: +(r.left + r.width / 2).toFixed(1), cy: +(r.top + r.height / 2).toFixed(1) }; };
async function idle(){ for (let i = 0; i < 400 && (typeof busy !== 'undefined' && busy); i++) await wait(25); }
async function until(f, ms){ const t0 = Date.now(); while (Date.now() - t0 < (ms || 10000)){ try { const v = await f(); if (v) return v; } catch (e) {} await wait(40); } try { return await f(); } catch (e) { return null; } }
async function untilRaf(f, ms){ const t0 = performance.now(); while (performance.now() - t0 < (ms || 20000)){ let v = null; try { v = f(); } catch (e) {} if (v) return performance.now(); await raf(); } return null; }
const scs = el => { const out = []; for (let q = el; q && q !== document.body && q !== document.documentElement; q = q.parentElement){ const o = getComputedStyle(q).overflowY; if ((o === 'auto' || o === 'scroll') && q.scrollHeight > q.clientHeight + 1) out.push(q); } return out; };
const num = s => { const m = /(\d[\d,]*)/.exec(String(s || '')); return m ? +m[1].replace(/,/g, '') : null; };
const typeIn = (inp, q) => { try { inp.focus(); } catch (e) {} inp.value = q; inp.dispatchEvent(new Event('input', { bubbles: true })); };
const pops = () => (typeof POPS !== 'undefined' ? POPS : []);
const popBy = k => pops().find(p => p._pk === k) || null;
const closeAll = () => { try { closeAllPops(true); } catch (e) { try { closeAllPops(); } catch (e2) {} } try { closeSk(); } catch (e) {} document.querySelectorAll('.c2fly,.c2srp,.c2lkm').forEach(x => x.remove()); try { if (typeof C2SQ !== 'undefined') C2SQ.open = false; } catch (e) {} };
function hitOn(t){ if (!t) return null; try { t.scrollIntoView({ block: 'center', inline: 'nearest' }); } catch (e) {} const r = R(t); const at = document.elementFromPoint(r.cx, r.cy);
  const onScreen = r.cy > 0 && r.cy < innerHeight && r.cx > 0 && r.cx < innerWidth && r.w > 0 && r.h > 0; return Object.assign(r, { on: !!at && (at === t || t.contains(at)) && onScreen, onScreen }); }
async function home1(law){ closeAll(); S.law = law || '특허법'; S.tab = 'jimun'; S.jimunTab = 'ox'; S.mok = ''; S.oxQueue = ''; S.oxQ = ''; S.oxQMode = 'q';
  await idle(); await render(); await idle();
  await until(() => OXPOOL && Object.keys(OXPOOL).length > 1000 && typeof MBSR !== 'undefined' && MBSR && MBSR.box && MBSR.box.isConnected, 60000); await wait(150); }
async function lawTab(law, tab){ closeAll(); S.law = law; S.tab = tab; await idle(); await render(); await idle(); await wait(150); }
async function canvasUp(){ await lawTab('민사소송법', 'omr');
  await until(() => document.getElementById('cvStage') && document.querySelectorAll('#cvWorld .cv-pg').length && viewCanvas._cv && viewCanvas._cv().D, 60000); await wait(400); return viewCanvas._cv(); }
const btxt = (p, b) => b.ls.map(i => p.lines[i].r.map(r => r.t).join('')).join('\n');
const SEEDQ = '하네스찾기';
const SD = {};
async function seed(){ if (SD.done) return SD;
  await home1('특허법');
  const K = Object.keys(OXPOOL).sort();
  const G = K.slice(0, 250); SD.me = K[400]; SD.me2 = K[402]; SD.G = G;
  const pad = '가나다라마바사아자차카타파하'.repeat(3);
  G.forEach((k, i) => ggPutList(k, [{ k: 'gH' + i, i: 1, t: SEEDQ + ' 근거 ' + i + ' ' + pad, ok: '', ts: Date.now(), cs: [] }]));
  try { ggRefAdd(SD.me2, G[0]); } catch (e) { SD.refErr = String(e); }
  const A = lsRead(REC_PRE + 'postit') || {};
  for (let i = 0; i < 250; i++) A[pitKey('jo|특허법:제' + (i % 200 + 1) + '조', 'h', String(i), '하네스')] = { t: SEEDQ + ' 메모 ' + i, ts: nowIso(), who: '꼬까' };
  lsWrite(REC_PRE + 'postit', A, '하네스 메모');
  try { await stkdSeed('특허법'); } catch (e) {}
  for (let i = 0; i < 120; i++) stkdPut('hsk' + i, { name: SEEDQ + i, mean: '하네스 뜻 ' + i, kind: '두문자' });
  SD.K = K; SD.done = true; return SD; }
function claudeSeed(){ const ans = {}; const K = SD.K || Object.keys(OXPOOL || {}).sort();
  for (let i = 0; i < 250; i++) ans['T9' + String(i).padStart(3, '0')] = { uid: K[i], law: '특허', md: SEEDQ + ' 답 ' + i, core: '' };
  clSet({ v: 1, answers: ans }); return CL_STATE; }
/* ── 자리마다 ── */
const SP = {};
const rowsOf = (box, f) => box ? [...box.children].filter(f) : [];
const rpc = box => { const c = box && box.querySelector(':scope > .rpcnt'); return c ? num(txt(c)) : null; };
SP.gg = { async open(){ await seed(); await home1('특허법'); popCard(SD.me, { clientX: 40, clientY: 90 });
    const p = await until(() => popBy('q|📝 지문 ' + SD.me), 8000); if (!p) return { ok: false, why: 'popCard 안 뜸' };
    const fd = await until(() => p.querySelector('.ggbox .fd'), 6000); if (!fd) return { ok: false, why: '🔍 없음' };
    fd.click(); await until(() => p.querySelector('.ggfind.on input'), 4000); this.p = p; return { ok: true }; },
  inp(){ return this.p && this.p.querySelector('.ggfind input'); }, box(){ return this.p && this.p.querySelector('.ggfind .rs'); },
  rows(){ return rowsOf(this.box(), x => x.classList.contains('ggres') && !!x.querySelector('.l1')); }, cnt(){ return rpc(this.box()); },
  async exp(q){ const s = String(q || '').trim(), A = ggAll(), out = [];
    Object.keys(A).forEach(uid => { if (uid === SD.me) return; if (!(OXPOOL || {})[uid]) return; (A[uid] || []).forEach(g => { const t = ggFlat(g) + ' ' + ((g.cs || []).map(c => c.t || '').join(' ')); if (t.indexOf(s) >= 0) out.push(uid); }); });
    return { n: out.length, last: out[out.length - 1] }; },
  go(q){ typeIn(this.inp(), q); }, q: [SEEDQ], q2: [SEEDQ + ' 근거 1'], tgt: row => row.querySelector('.gl') || row.querySelector('.qq'),
  async lastCheck(e){ return { ok: ggRefOf(SD.me).indexOf(e.last) >= 0, v: ggRefOf(SD.me).slice(-3) }; } };
SP.mb = { async open(){ await home1('특허법'); return { ok: !!this.inp() }; },
  inp(){ return document.querySelector('#slot .mbsr input'); }, box(){ return (typeof MBSR !== 'undefined' && MBSR) ? MBSR.box : null; },
  rows(){ return rowsOf(this.box(), x => x.classList.contains('rr') && !!x.querySelector('.m')); }, cnt(){ return MBSR && MBSR.cnt ? num(txt(MBSR.cnt)) : null; },
  async exp(q){ q = String(q).trim(); const P = OXPOOL || {}; const idk = uidSearchKeys(q, P);
    let hit = idk.concat(Object.keys(P).filter(k => { if (idk.indexOf(k) >= 0) return false; const c = P[k] || {}; return String(c.t || '').includes(q) || String(c.name || '').includes(q); }));
    hit = hit.filter(k => uzPass(k)); return { n: hit.length, last: hit[hit.length - 1] }; },
  go(q){ typeIn(this.inp(), q); }, q: ['특허', '청구', '발명'], q2: ['정정'], pt: true,
  async lastCheck(e){ const p = await until(() => popBy('q|📝 지문 ' + e.last), 4000); return { ok: !!p, v: p ? p._pk : pops().map(x => x._pk).slice(-2) }; } };
SP.c2e = { subj: '민소', async open(){ closeAll(); const I = await c2Idx(this.subj); this.u = Object.keys(I)[0]; c2EditWin(this.subj, this.u, { clientX: 60, clientY: 80 }, 1);
    this.p = await until(() => popBy('c2edit|' + this.subj + '|' + this.u), 6000); if (!this.p) return { ok: false, why: '창 안 뜸' };
    await until(() => this.p.querySelector('.c2wb input'), 6000); await wait(100); return { ok: true }; },
  inp(){ return this.p && this.p.querySelector('.c2wb input'); }, box(){ const w = this.p && this.p.querySelector('.c2wb'); return w ? w.lastElementChild : null; },
  rows(){ return rowsOf(this.box(), x => x.classList.contains('row')); }, cnt(){ return rpc(this.box()); },
  async exp(q){ const I = C2IDX[this.subj]; q = String(q).trim().toLowerCase(); const u = this.u;
    const h = Object.keys(I).filter(k => k !== u && (k.toLowerCase().includes(q) || c2QText(I[k].rec).toLowerCase().includes(q) || String((I[k].rec.fm || {})['쟁점'] || '').toLowerCase().includes(q)));
    return { n: h.length, last: h[h.length - 1] }; },
  go(q){ typeIn(this.inp(), q); }, q: ['법원', '소송', '판결', '청구'], q2: ['기판력'] };
const SKB = () => document.getElementById('skres');
const SKPRE = { jo: '📖 조문', prec: '⚖ 판례', jimun: '📝 지문', memo: '🗒 메모', claude: 'Claude', omr: '📖 정리', stk: '🏷 두문자' };
function skGroup(prefix){ const b = SKB(); const rows = []; let on = false, h = null; if (!b) return { h: null, rows: rows };
  for (const c of b.children){ if (c.classList.contains('grp')){ if (on) break; if (txt(c).indexOf(prefix) === 0){ on = true; h = c; } continue; } if (on && c.classList.contains('res')) rows.push(c); }
  return { h: h, rows: rows }; }
function skOpen(scope){ closeAll(); openSk(); Object.keys(SKON).forEach(k => { SKON[k] = (k === scope); }); try { skonSave(); } catch (e) {} LAWS.forEach(l => { SKLAW[l] = true; }); try { skPaint(); skLawPaint(); } catch (e) {} }
function skSpot(scope, qs, q2s, expf){ return { scope: scope, sk: true,
  async open(){ if (scope === 'claude'){ await seed(); claudeSeed(); } else if (scope === 'memo' || scope === 'stk') await seed(); skOpen(scope); await wait(60); return { ok: !!document.getElementById('skin') && document.getElementById('sk').style.display !== 'none' }; },
  inp(){ return document.getElementById('skin'); }, box(){ return SKB(); },
  rows(){ return skGroup(SKPRE[scope]).rows; },   /* 그 갈래 줄만(조문 범위엔 테마 갈래가 같이 뜬다) */
  cnt(){ const g = skGroup(SKPRE[scope]).h; return g ? num(txt(g).split('—')[1] || '') : null; },
  endEl(){ const rs = this.rows(), lr = rs[rs.length - 1], x = lr && lr.nextElementSibling; return (x && x.classList.contains('rpend')) ? x : null; },
  done(){ const b = SKB(); return !!b && [...b.querySelectorAll(':scope > .grp')].some(g => /↵ 열기/.test(txt(g))); },
  go(q){ const i = this.inp(); i.value = q; i.oninput({ target: i }); }, q: qs, q2: q2s, exp: expf }; }
const lawsOn = () => LAWS.filter(l => SKLAW[l]);
SP['sk.jo'] = skSpot('jo', ['특허', '청구', '출원'], ['정정'], async q => { let n = 0;
  for (const law of lawsOn()){ const L = await get('jo_' + law + '_목록.json'); const B = await get('jo_' + law + '_본문.json');
    for (const j of L.조){ if (j.k.includes(q) || (j.t || '').includes(q)){ n++; continue; } const body = B.조[j.k]; if (!body) continue; if (body.행.some(r => (r.t || '').indexOf(q) >= 0)) n++; } }
  return { n: n }; });
SP['sk.prec'] = skSpot('prec', ['특허', '무효', '청구'], ['신규성'], async q => { let n = 0;
  for (const law of lawsOn().filter(l => ['특허법', '상표법', '민사소송법'].indexOf(l) >= 0)){ const P = await get(PFL(law, '리스트')); const hit = await precSearch(P, q, law); if (!hit) continue; n += P.판례.filter(p => hit.has(p.id)).length; }
  return { n: n }; });
SP['sk.jimun'] = skSpot('jimun', ['특허', '출원', '청구'], ['정정'], async q => { const items = [];
  for (const law of lawsOn().filter(l => l !== '민사소송법')){ const subj = SHORT[law]; const JM = await get('jimun_' + subj + '.json');
    for (const qq of JM.문제){ for (const z of (qq.지문 || [])){ if (String(z.t || '').includes(q)){ items.push(qq.연도 + '년 ' + (qq.시험문번 || qq.문번) + '번 (' + z.n + ')'); break; } } } }
  let P7 = null; if (SKLAW['특허법']){ try { P7 = await get('jimun_7pan.json'); } catch (e) {} }
  if (P7) for (const z of P7.지문){ if (String(z.t || '').includes(q)) items.push(p8Is(z) ? 'H8 ' + z.태그 + ' p.' + z.판8.p8 : 'H7 ' + z.태그 + ' p.' + (z.쪽 || '—')); }
  if (SKLAW['상표법']){ let PB = null; try { PB = await get(gBook(SHORT['상표법']).j); } catch (e) {} if (PB) for (const z of PB.지문){ if (String(z.t || '').includes(q)) items.push(gEd(z) + ' ' + z.태그 + ' p.' + (z.쪽 || '—')); } }
  return { n: items.length, last: items[items.length - 1] }; });
SP['sk.jimun'].lastCheck = async e => { const p = await until(() => popBy('q|📝 ' + e.last), 4000); return { ok: !!p && document.getElementById('sk').style.display === 'none', v: p ? p._pk : pops().map(x => x._pk).slice(-2) }; };
SP['sk.memo'] = skSpot('memo', [SEEDQ], [SEEDQ + ' 메모 1'], async q => { const A = lsRead(REC_PRE + 'postit'); return { n: Object.keys(A).filter(k => String((A[k] || {}).t || '').indexOf(q) >= 0).length }; });
SP['sk.claude'] = skSpot('claude', [SEEDQ], [SEEDQ + ' 답 1'], async q => { if (CL_STATE !== 'ok') return { n: -1 };
  const A = (CL_DATA && CL_DATA.answers) || {}, ks = Object.keys(A).sort(); let n = 0;
  const lawOf = m => { const a = A[m] || {}; return String(a.law || (m.indexOf('MS') === 0 ? '민소' : ({ T: '특허', S: '상표', D: '디보' })[m[0]] || '')); };
  for (const m of ks){ const a = A[m] || {}, lw = lawOf(m), full = LAW_FULL[lw]; if (!full || !SKLAW[full]) continue; const u = String(a.uid || ''), ms = CL_MS_RX.test(u);
    const hay = clMdOf(m) + '\n' + String(a.core || '') + '\n' + m + '\n' + (ms ? clWho(u) : (ggWho(u) + '\n' + u)); if (hay.indexOf(q) >= 0) n++; }
  return { n: n }; });
SP['sk.omr'] = skSpot('omr', ['특허', '청구', '출원'], ['정정'], async q => { let n = 0;
  if (SKLAW['특허법']){ const W = await get('omr/특허/omr_words.json'); W.pages.forEach(ws => { for (const w of ws) if (String(w[4]).indexOf(q) >= 0) n++; }); }
  if (SKLAW['민사소송법']){ const H = await viewCanvas.find(q); n += (H || []).length; }
  return { n: n }; });
SP['sk.stk'] = skSpot('stk', [SEEDQ], [SEEDQ + '1'], async q => { await stkdSeed(S.law); const A = stkdAll(); let n = 0;
  for (const id of Object.keys(A)){ const d = A[id]; if ((d.name || '').indexOf(q) < 0 && (d.mean || '').indexOf(q) < 0) continue; n += 1 + stkdUses(id).length; }
  return { n: n }; });
SP.pl = { async open(){ await lawTab('특허법', 'prec'); const P = await get(PF('리스트')); const CITE = await get(PF('인용')).catch(() => ({})); this.P = P; this.cur = P.판례[0];
    precLinkWin('link', this.cur, CITE[this.cur.id] || {}, P, { clientX: 60, clientY: 60 }, 0, false);
    this.p = await until(() => { const b = document.querySelector('.plsb'); return b ? b.closest('.pop') : null; }, 6000); return { ok: !!this.p }; },
  inp(){ return this.p && this.p.querySelector('.plsb > input'); }, box(){ return this.p && this.p.querySelector('.plsr'); },
  rows(){ return rowsOf(this.box(), x => x.classList.contains('res')); }, cnt(){ return rpc(this.box()); },
  done(){ const b = this.box(); return !!b && txt(b).indexOf('찾는 중') < 0; },
  async exp(q){ const P = this.P, qn = precNorm(q), ex = this.cur.id, by = {}; (P.판례 || []).forEach(p => { by[p.id] = p; }); const R = new Set(); const add = id => { if (id && id !== ex && by[id]) R.add(id); };
    (P.판례 || []).forEach(p => { if (precNorm(p.id).indexOf(qn) >= 0 || precNorm(p.사건번호).indexOf(qn) >= 0) add(p.id); if (precNorm(p.사건명).indexOf(qn) >= 0 || precNorm(p.별칭).indexOf(qn) >= 0 || precNorm(p.설명별칭).indexOf(qn) >= 0) add(p.id); });
    const LR = plAll(); Object.keys(LR).forEach(a => (LR[a] || []).forEach(x => { if (!x || !x.why || precNorm(x.why).indexOf(qn) < 0) return; add(a); if ((x.k || 'prec') === 'prec') add(x.to); }));
    let H = null; try { H = await precSearch(P, q, PLAW()); } catch (e) {} if (H) H.forEach((r, id) => { if (r.n > 0) add(id); });
    return { n: R.size }; },
  go(q){ typeIn(this.inp(), q); }, q: ['특허', '청구', '진보성'], q2: ['신규성'] };
SP.c2r = { async open(){ await lawTab('민사소송법', 'prec'); const P = await get(PF('리스트')); this.pp = P.판례[0];
    await popCardList(this.pp, '사례', null, { clientX: 60, clientY: 60, __list: true }, 0);
    this.p = await until(() => pops().find(x => /^cards\|사례\|/.test(x._pk || '')), 6000); if (!this.p) return { ok: false, why: '목록 창 안 뜸' };
    const add = [...this.p.querySelectorAll('button.tool')].find(b => /2차 잇기/.test(txt(b))); if (!add) return { ok: false, why: '+ 2차 잇기 없음' };
    add.click(); await until(() => this.p.querySelector('.lkform input'), 4000); await wait(100); return { ok: true }; },
  inp(){ return this.p && this.p.querySelector('.lkform > input'); }, box(){ const f = this.p && this.p.querySelector('.lkform'); return f ? f.children[2] : null; },
  rows(){ return rowsOf(this.box(), x => x.classList.contains('res')); }, cnt(){ return rpc(this.box()); },
  async exp(q){ const CK = await get(CHF('사례')); const qn = precNorm(q); return { n: Object.keys(CK).filter(k => !qn || precNorm(k).indexOf(qn) >= 0 || precNorm((CK[k].fm || {}).별칭).indexOf(qn) >= 0).length }; },
  go(q){ typeIn(this.inp(), q); }, q: ['소', '의', '청구'], q2: ['기판력'] };
SP.c2q = { async open(){ await lawTab('민사소송법', 'cha2'); const I = await c2Idx(PLAW()); const f = Object.keys(I).find(k => I[k].kind === '기출' && ((I[k].rec && I[k].rec.행) || []).some(r => !r.co && r.h === 1));
    this.id = 'card|기출|' + f + '#0'; let b = document.getElementById('h_c2qbtn'); if (!b){ b = document.createElement('button'); b.id = 'h_c2qbtn'; b.textContent = '•'; b.style.cssText = 'position:fixed;left:24px;top:70px;width:20px;height:20px;z-index:1'; document.body.appendChild(b); }
    await c2QlMenu(b, this.id); this.m = await until(() => document.querySelector('.c2lkm .add input') && document.querySelector('.c2lkm'), 6000); return { ok: !!this.m }; },
  inp(){ return document.querySelector('.c2lkm .add input'); }, box(){ return document.querySelector('.c2lkm .al'); },
  rows(){ return rowsOf(this.box(), x => x.classList.contains('ai')); }, cnt(){ return rpc(this.box()); },
  async exp(q){ const I = await c2Idx(PLAW()); const T = String(q).toLowerCase().split(/\s+/).filter(Boolean); const ex = new Set([this.id].concat(c2QlOut(c2QlAll(), this.id).map(x => x.o))); let n = 0;
    for (const f of Object.keys(I)){ const it = I[f]; if (!it || (it.kind !== '기출' && it.kind !== 'GS')) continue; let k = 0;
      ((it.rec && it.rec.행) || []).forEach(r => { if (r.co || r.h !== 1) return; const qid = 'card|' + it.kind + '|' + f + '#' + k; k++; if (ex.has(qid)) return; const t = c2QlTextOf(r.t); if (T.every(x => (f + ' ' + t).toLowerCase().indexOf(x) >= 0)) n++; }); }
    return { n: n }; },
  go(q){ typeIn(this.inp(), q); }, q: ['소', '법원', '청구'], q2: ['기판력'] };
SP.c2s = { async open(){ await lawTab('민사소송법', 'cha2'); const i = await until(() => document.querySelector('#slot .c2srch'), 8000); return { ok: !!i }; },
  inp(){ return document.querySelector('#slot .c2srch'); }, box(){ return document.querySelector('body > .c2srp .srl'); },
  rows(){ return rowsOf(this.box(), x => x.classList.contains('srr')); }, cnt(){ const o = document.querySelector('body > .c2srp .srk.on'); return o ? num(txt(o)) : null; },
  async exp(q){ const L = await c2SrIdx(PLAW()); const T = String(q).trim().toLowerCase().split(/\s+/).filter(Boolean); const all = L.filter(x => T.every(t => x.low.indexOf(t) >= 0));
    return { n: (C2SQ.kind ? all.filter(x => x.kind === C2SQ.kind) : all).length }; },
  go(q){ const i = this.inp(); i.value = q; i.dispatchEvent(new Event('input', { bubbles: true })); }, q: ['법원', '소송', '판결'], q2: ['기판력'] };   /* 초점을 주지 않는다 — 초점이면 옛 검색어로 판을 먼저 한 번 그려(focus → c2SrPanel) 재기가 엇갈린다 */
SP.cf = { async open(){ await home1('특허법'); this.key = Object.keys(OXPOOL).sort()[10]; editPop(this.key, { clientX: 40, clientY: 70 });
    this.p = await until(() => { const i = document.querySelector('.cflw .cfq'); return i ? i.closest('.pop') : null; }, 6000); try { await cfLoadOthers(); } catch (e) {} await wait(200); return { ok: !!this.p }; },
  inp(){ return this.p && this.p.querySelector('.cfq'); }, box(){ return this.p && this.p.querySelector('.cfrs'); },
  rows(){ return rowsOf(this.box(), x => x.classList.contains('cfr')); }, cnt(){ return rpc(this.box()); },
  async exp(q){ const low = String(q).trim().toLowerCase(), key = this.key, out = []; const scan = rows => { for (const r of rows){ if (r.k === key) continue; if (r.hay.indexOf(low) >= 0) out.push(r.k); } };
    scan(cfRowsCur()); for (const law of LAWS3APP){ if (law === S.law) continue; scan(cfRowsOther(law)); } return { n: out.length, last: out[out.length - 1] }; },
  go(q){ typeIn(this.inp(), q); }, q: ['특허', '출원', '청구'], q2: ['정정'], tgt: row => row.querySelector('.cftx'),
  async lastCheck(e){ const ok = await until(() => lkOf(this.key).indexOf(e.last) >= 0, 3000); return { ok: !!ok, v: lkOf(this.key).slice(-3) }; } };
SP.cvl = { async open(){ const c = await canvasUp(); this.c = c; this.pg = c.D.pages[0]; this.b = this.pg.blocks.find(x => !x.del && x.k !== '헤딩');
    c.openPop(this.pg, this.b, 'link', { clientX: 80, clientY: 90 }, []); const i = await until(() => document.querySelector('.cv-pop .cv-lfind input'), 6000); return { ok: !!i }; },
  inp(){ return document.querySelector('.cv-pop .cv-lfind input'); }, box(){ return document.querySelector('.cv-pop .cv-lres'); },
  rows(){ return rowsOf(this.box(), x => x.classList.contains('cv-lrow') && !!x.querySelector('b')); }, cnt(){ return rpc(this.box()); },
  async exp(q){ q = String(q).trim(); const D = this.c.D; let n = 0; for (const pp of D.pages){ for (const bb of pp.blocks){ if (bb === this.b || bb.k === '헤딩' || bb.del) continue; if (btxt(pp, bb).replace(/\n/g, '').indexOf(q) >= 0) n++; } } return { n: n }; },
  go(q){ typeIn(this.inp(), q); }, q: ['법원', '소송', '청구', '판결'], q2: ['기판력'] };
SP.cvp = { async open(){ const c = await canvasUp(); this.c = c; this.pg = c.D.pages[0]; this.b = this.pg.blocks.find(x => !x.del && x.k !== '헤딩'); return { ok: !!this.b }; },
  async prep(q){ document.querySelectorAll('.cv-pop').forEach(x => { const p = x.closest('.pop') || x; }); try { closeAllPops(true); } catch (e) { try { closeAllPops(); } catch (e2) {} }
    this.c.openPop(this.pg, this.b, 'case', { clientX: 80, clientY: 90 }, [q]);
    const bt = await until(() => document.querySelector('.cv-pop .cv-card[data-ci="0"] [data-q]'), 15000); this.bt = bt; return !!bt; },
  inp(){ return null; }, box(){ return document.querySelector('.cv-pop .cv-card[data-ci="0"] .cv-cres'); },
  rows(){ return rowsOf(this.box(), x => x.matches('.cv-lrow[data-id]')); }, cnt(){ const b = document.querySelector('.cv-pop .cv-card[data-ci="0"] .m button'); return b && /건/.test(txt(b)) ? num(txt(b)) : null; },
  async exp(q){ let n = 0; for (const L of LAWS){ let P = null; try { P = await get(PFL(L, '리스트')); } catch (e) { continue; } let hit = null; try { hit = await precSearch(P, q, L); } catch (e) { hit = null; } if (!hit) continue;
      hit.forEach((r, id) => { const p = (P.판례 || []).find(x => x.id === id); if (p && (r.num || r.name)) n++; }); } return { n: n }; },
  go(q){ if (this.bt) this.bt.click(); }, q: ['등록무효', '권리범위확인', '거절결정'], q2: [] };
SP.cvb = { async open(){ closeAll(); viewCanvas.jari.book8({ book: 'patent_hr8', page: 300 }, null);
    this.p = await until(() => popBy('cv|book|patent_hr8'), 20000); if (!this.p) return { ok: false, why: '교재 창 안 뜸' };
    const ok = await until(() => this.p.querySelector('.cv-bs input') && viewCanvas._cv().CVB.text && viewCanvas._cv().CVB.text['patent_hr8'], 60000); return { ok: !!ok, why: ok ? '' : '쪽 글 못 받음' }; },
  inp(){ return this.p && this.p.querySelector('.cv-bs input'); }, box(){ return this.p && this.p.querySelector('.cv-bsres .cv-bslist'); },
  rows(){ return rowsOf(this.box(), x => x.classList.contains('cv-bspg')); }, snips(){ return rowsOf(this.box(), x => x.classList.contains('cv-bssn')).length; },
  cnt(){ const h = this.p && this.p.querySelector('.cv-bsres .cv-bshd'); return h ? num((txt(h).split('총')[1] || '')) : null; },
  async exp(q){ const tx = viewCanvas._cv().CVB.text['patent_hr8']; const qq = String(q || '').replace(/\s+/g, ''); let np = 0, total = 0;
    (tx.t || []).forEach(t0 => { const s = String(t0 || '').replace(/\s+/g, ''); if (s.indexOf(qq) < 0) return; np++; let j = -1; while ((j = s.indexOf(qq, j + 1)) >= 0) total++; }); return { n: np, total: total }; },
  go(q){ const i = this.inp(); i.value = q; const g = this.p.querySelector('.cv-bs .cv-bsgo'); g.click(); }, q: ['특허', '출원', '청구'], q2: ['정정'] };
/* ── 재기 ── */
const endOf = s => s.endEl ? s.endEl() : (s.box() ? s.box().querySelector('.rpend') : null);
const tailOf = s => { const e = endOf(s); if (e) return e; const rs = s.rows(); return rs[rs.length - 1] || s.box(); };   /* 끝 표지(없으면 끝 줄) — 굴릴 과녁 */
window.__JS = {
  wait, R, hitOn, idle,
  errs(){ return (window.__ERR || []).filter(e => !/ResizeObserver loop/.test(e)).slice(0, 12); },
  ready(){ return typeof render === 'function' && typeof S !== 'undefined' && !!document.getElementById('slot'); },
  async boot(){ await until(() => typeof busy === 'undefined' || !busy, 30000); await wait(300); return { law: S.law, tab: S.tab }; },
  async seed(){ const s = await seed(); return { me: s.me, me2: s.me2, refErr: s.refErr || '', gg: Object.keys(ggAll()).length }; },
  async open(n){ const o = await SP[n].open(); return o; },
  async exp(n, q){ const e = await SP[n].exp(q); SP[n]._exp = e; return e; },
  hasQ2(n){ return !!(SP[n].q2 && SP[n].q2.length); },
  async pick(n, which, need){ const cands = which === 2 ? SP[n].q2 : SP[n].q; let best = null; for (const q of cands){ const e = await SP[n].exp(q); if (!best || e.n > best.e.n) best = { q: q, e: e }; if (e.n > need){ best = { q: q, e: e }; break; } }
    if (best) SP[n]._exp = best.e; return best; },
  nearEnd(n, gap){ const s = SP[n], tg = tailOf(s); const sc = scs(tg)[0]; SP[n]._sc = sc || null; if (!sc) return null;
    const d = tg.getBoundingClientRect().top - sc.getBoundingClientRect().bottom; sc.scrollTop = Math.max(0, sc.scrollTop + d + (gap || 700) * -1);
    return { st: Math.round(sc.scrollTop), sh: sc.scrollHeight, ch: sc.clientHeight, gap: Math.round(tg.getBoundingClientRect().top - sc.getBoundingClientRect().bottom), cls: String(sc.className || sc.id).slice(0, 30) }; },
  async run(n, q, tmo){ const s = SP[n]; if (s.prep){ const ok = await s.prep(q); if (!ok) return { ok: false, why: 'prep' }; }
    const b0 = s.box(); let mk = null; if (b0){ mk = document.createElement('i'); mk.className = 'h_mark'; mk.style.display = 'none'; b0.appendChild(mk); }
    const t0 = performance.now(); s.go(q);   /* 그림 끝 = 그릇이 비워졌다(표지 떨어짐 · 앱이 그 자리에서 처음 줄을 다 그림) · 줄 ≥ 1 · 갈래 끝 표지(통합 검색 「↵ 열기」 · 판례 창 「찾는 중」 없음) */
    const t1 = await untilRaf(() => (!mk || !mk.isConnected) && !!s.box() && s.rows().length >= 1 && (!s.done || s.done()), tmo || 30000);
    const r = { ok: t1 != null, ms: t1 == null ? null : +(t1 - t0).toFixed(1), n: s.rows().length, cnt: s.cnt(), pend: endOf(s) ? 1 : 0 };
    if (s.snips) r.snips = s.snips(); return r; },
  rowsN(n){ const s = SP[n]; return { n: s.rows().length, pend: endOf(s) ? 1 : 0, snips: s.snips ? s.snips() : null, cnt: s.cnt() }; },
  stNow(n){ const sc = SP[n]._sc; return sc ? Math.round(sc.scrollTop) : null; },
  scInfo(n){ const s = SP[n], lr = tailOf(s); const L = scs(lr); const sc = L[0] || document.scrollingElement; const r = sc === document.scrollingElement ? { x: 0, y: 0, w: innerWidth, h: innerHeight, r: innerWidth, b: innerHeight } : R(sc);
    const x0 = Math.max(4, r.x), x1 = Math.min(innerWidth - 4, r.r), y0 = Math.max(4, r.y), y1 = Math.min(innerHeight - 4, r.b);
    return { cx: Math.round((x0 + x1) / 2), cy: Math.round((y0 + y1) / 2), vh: Math.round(y1 - y0), left: Math.round(sc.scrollHeight - sc.clientHeight - sc.scrollTop), sh: sc.scrollHeight, ch: sc.clientHeight, cls: String(sc.className || sc.id || sc.tagName).slice(0, 40), nsc: L.length }; },
  async fill(n, maxMs){ const s = SP[n]; const t0 = Date.now(); let last = -1, same = 0;   /* 끝 표지(없으면 끝 줄)를 굴림 칸 아래 끝에 맞춰 굴린다 — 끝 표지가 200px 안에 들면 다음 100 줄 */
    while (Date.now() - t0 < (maxMs || 90000)){ const box = s.box(); if (!box) break; const tg = tailOf(s); try { tg.scrollIntoView({ block: 'end', inline: 'nearest' }); } catch (e) {}
      await raf(); await raf(); await wait(25); const n2 = s.rows().length;
      if (n2 === last){ if (++same >= (endOf(s) ? 25 : 6)) break; } else { same = 0; last = n2; } }
    return { n: s.rows().length, pend: endOf(s) ? 1 : 0, snips: s.snips ? s.snips() : null, ms: Date.now() - t0 }; },
  async partial(n){ const s = SP[n]; const n0 = s.rows().length; const tg = tailOf(s); try { tg.scrollIntoView({ block: 'end', inline: 'nearest' }); } catch (e) {}
    await until(() => s.rows().length > n0, 4000); return s.rows().length; },
  scan(n){ const s = SP[n], box = s.box(); if (!box) return null; const rs = s.rows(); const L = scs(rs[rs.length - 1] || box); const sc = L[0] || null;
    const win = box.closest('.pop, #sk, .c2srp, .c2lkm') || box; const wr = R(win), br = R(box), c = box.querySelector(':scope > .rpcnt'), cr = R(c);
    const lr = rs[rs.length - 1], lrr = R(lr), scr = sc ? R(sc) : null;
    return { vw: innerWidth, vh: innerHeight, docOver: +(document.documentElement.scrollWidth - innerWidth).toFixed(1), boxOver: box.scrollWidth - box.clientWidth, scOver: sc ? sc.scrollWidth - sc.clientWidth : 0,
      win: wr, winIn: !!wr && wr.x >= -1 && wr.r <= innerWidth + 1, cnt: cr, cntIn: !c || (cr.x >= br.x - 1 && cr.r <= br.r + 1 && cr.h > 0), cntTxt: c ? txt(c) : null,
      lastIn: !lr || !scr ? null : (lrr.b <= scr.b + 1.5 && lrr.t !== null), lastB: lrr ? lrr.b : null, scB: scr ? scr.b : null, sc: sc ? String(sc.className || sc.id).slice(0, 40) : 'doc',
      rowOver: rs.slice(0, 60).filter(x => x.scrollWidth > x.clientWidth + 1).length, rowsCut: rs.slice(0, 60).filter(x => { const r = x.getBoundingClientRect(); return r.right > (scr ? scr.r : innerWidth) + 1; }).length,
      over: (() => { const bw = box.getBoundingClientRect(), all = []; box.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (r.width > 0 && r.right > bw.right + 1) all.push(e); });
        const ROW = '.res, .row, .cfr, .srr, .ai, .ggres, .rr, .cv-lrow, .cv-bssn, .cv-bspg';
        const pre = all.filter(e => !e.closest('.rpcnt, .rpend') && e.closest(ROW) && getComputedStyle(e).whiteSpace === 'nowrap');   /* 줄 안 줄바꿈 없는 글(옛 판 줄 꼴 그대로) */
        const other = all.filter(e => pre.indexOf(e) < 0);
        return { pre: pre.length, preMax: pre.length ? Math.round(Math.max(...pre.map(e => e.getBoundingClientRect().right - bw.right))) : 0, preEx: pre.slice(0, 2).map(e => txt(e).slice(0, 40)),
          other: other.length, otherEx: other.slice(0, 3).map(e => String(e.tagName + '.' + e.className).slice(0, 30) + ':' + txt(e).slice(0, 30)) }; })() }; },
  lastHit(n){ const s = SP[n], rs = s.rows(), row = rs[rs.length - 1]; if (!row) return null; const t = (s.tgt && s.tgt(row)) || row; const h = hitOn(t);
    if (s.pt){ const r = row.getBoundingClientRect(), x = r.left + 40, y = r.bottom - 5, at = document.elementFromPoint(x, y);
      return Object.assign(h, { cx: x, cy: y, on: !!at && (at === row || (row.contains(at) && !at.closest('.m') && !at.closest('button'))) && y > 0 && y < innerHeight }); }
    return h; },
  async lastCheck(n){ const s = SP[n]; return s.lastCheck ? await s.lastCheck(s._exp || {}) : { ok: null }; },
  async gt(){ await seed(); await home1('특허법'); popCard(SD.me2, { clientX: 10, clientY: 70 }); const p = await until(() => popBy('q|📝 지문 ' + SD.me2), 6000); if (!p) return { ok: false, why: '창 안 뜸' };
    const gt = await until(() => p.querySelector('.ggrefbox .gt'), 6000); if (!gt) return { ok: false, why: '.gt 없음', ref: ggRefOf(SD.me2) };
    gt.scrollIntoView({ block: 'center' }); await wait(250); const r = R(gt), btn = gt.querySelector('button'), b = R(btn);
    const rg = document.createRange(); rg.setStartBefore(gt.firstChild); rg.setEndBefore(btn); const rects = [...rg.getClientRects()].filter(x => x.width > 0.5);
    const tl = Math.min(...rects.map(x => x.left)), tr = Math.max(...rects.map(x => x.right)); const tops = [...new Set(rects.map(x => Math.round(x.top)))];
    const lastL = rects.reduce((a, x) => (x.bottom > a.bottom ? x : a), rects[0]); const cs = getComputedStyle(gt);
    return { ok: true, vw: innerWidth, gtW: r.w, gtX: r.x, textL: +(tl - r.x).toFixed(1), textR: +(tr - r.x).toFixed(1), ratio: +((tr - tl) / r.w).toFixed(3), lines: tops.length,
      btn: b ? { x: +(b.x - r.x).toFixed(1), y: +(b.y - r.y).toFixed(1), w: b.w, h: b.h, gapRight: +(r.r - b.r).toFixed(1), t: txt(btn) } : null,
      btnAfterText: b && lastL ? (Math.abs(b.cy - (lastL.top + lastL.bottom) / 2) < 14 && b.x >= lastL.right - 2) : null, btnOwnLine: b && lastL ? b.y >= lastL.bottom - 2 : null, display: cs.display, ws: cs.whiteSpace, gtH: r.h }; }
};
})();
</script>"""

READY = "!!window.__JS && window.__JS.ready()"


def app_html(src):
    src = src.replace('\r\n', '\n')
    b = src.index('<body')
    bb = src.index('>', b) + 1
    html = src[:bb] + SEED + src[bb:]
    e = html.rindex('</body>')
    return html[:e] + TOOLS + '\n' + html[e:]


def serve(tag, src):
    if tag in SERVERS:
        return SERVERS[tag][1]
    out = os.path.join(WORK, 'srv_' + tag)
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n').write(app_html(src))

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=out, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            if p.startswith('/__vendor/'):
                return os.path.join(VENDOR, *[x for x in p[len('/__vendor/'):].split('/') if x])
            if p.startswith('/__book/'):
                return os.path.join(MB, *[x for x in p[len('/__book/'):].split('/') if x])
            if p.startswith('/data/'):
                return os.path.join(DATA, *[x for x in p[len('/data/'):].split('/') if x])
            if p in ('/index.html', '/'):
                return super().translate_path(path)
            f = os.path.join(JOD, *[x for x in p.split('/') if x])
            return f if os.path.exists(f) else super().translate_path(path)

        def log_message(self, *a, **k):
            pass
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


class Pg:
    def __init__(self, br, eng, tag, src, dev):
        self.eng, self.tag, self.dev = eng, tag, dev
        port = serve(tag, src)
        if dev == 'pc':
            self.ctx = br.new_context(viewport={'width': PC[0], 'height': PC[1]}, device_scale_factor=1)
        else:   # webkit 은 is_mobile 을 끈다 — 모바일 webkit 은 휠이 없고(playwright) 터치 끌기도 없어 굴림을 못 넣는다(폭 390 · 터치 켬은 같음)
            self.ctx = br.new_context(viewport={'width': PHONE[0], 'height': PHONE[1]}, device_scale_factor=2, is_mobile=(eng == 'chromium'), has_touch=True)
        self.ctx.route('**/*', lambda r: r.continue_() if r.request.url.startswith('http://127.0.0.1') else r.abort())
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(180000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:200]))
        self.cdp = self.ctx.new_cdp_session(self.pg) if eng == 'chromium' else None
        QJ.launch('base' if tag == 'base' else 'new')
        self.pg.goto('http://127.0.0.1:%d/index.html?tok=1&who=%s' % (port, urllib.parse.quote('꼬까')), wait_until='load', timeout=180000)
        self.pg.wait_for_function(READY, timeout=180000)
        self.ev('() => __JS.boot()')

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def wait(self, ms):
        self.pg.wait_for_timeout(ms)

    def click(self, at):
        if not at or not at.get('on'):
            return False
        if self.dev == 'pc':
            self.pg.mouse.click(at['cx'], at['cy'])
        else:
            self.pg.touchscreen.tap(at['cx'], at['cy'])
        return True

    def gesture(self, s):
        """진짜 굴림 — 끝 표지 700px 앞까지 scrollTop 으로 옮겨 두고(준비) 진짜 입력으로 넘긴다:
        PC · webkit = 마우스 휠 400px · 폰(chromium) = CDP Input.dispatchTouchEvent 손가락 끌기(synthesizeScrollGesture 는 이 헤드리스에서 안 굴러 0px — 10/10 잼)"""
        pre = self.ev('n => __JS.nearEnd(n, 700)', s)
        self.wait(300)
        info = self.ev('n => __JS.scInfo(n)', s)
        n0 = self.ev('n => __JS.rowsN(n)', s)['n']
        how = 'cdp-touch' if (self.dev == 'phone' and self.cdp) else 'wheel'
        n1, k, stb, sta = n0, 0, None, None
        for k in range(1, 7):
            stb = self.ev('n => __JS.stNow(n)', s)
            if how == 'cdp-touch':
                span = max(60, min(360, int(info.get('vh', 300) * 0.7)))
                x, y0, y1 = info['cx'], info['cy'] + span // 2, info['cy'] - span // 2

                def t(ty, yy):
                    self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': ([] if ty == 'touchEnd' else [{'x': x, 'y': yy, 'id': 1, 'radiusX': 11, 'radiusY': 11}])})
                t('touchStart', y0)
                for i in range(1, 13):
                    t('touchMove', y0 + (y1 - y0) * i / 12)
                    self.wait(16)
                for _ in range(4):
                    t('touchMove', y1)
                    self.wait(30)
                t('touchEnd', y1)
            else:
                self.pg.mouse.move(info['cx'], info['cy'])
                self.pg.mouse.wheel(0, 400)
            self.wait(450)
            n1 = self.ev('n => __JS.rowsN(n)', s)['n']
            if n1 > n0:
                self.wait(600)   # 붙인 뒤 창 다시 맞춤(ResizeObserver → rAF)까지 기다려 굴림 자리를 잰다
                sta = self.ev('n => __JS.stNow(n)', s)
                break
        return {'how': how, 'n0': n0, 'n1': n1, 'tries': k, 'st_before': stb, 'st_after': sta, 'pre': pre, 'sc': {kk: info.get(kk) for kk in ('cls', 'cx', 'cy', 'vh')}}

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(statistics.median(xs), 1) if xs else None


def measure(p, s, full):
    """한 자리 · 한 기기 — 처음 · (새 판) 진짜 굴림 · 끝까지 · 훑기 · (full) 빠르기 · 마지막 줄 · 바꿈"""
    out = {'spot': s}
    o = p.ev('n => __JS.open(n)', s)
    out['open'] = o
    if not o or not o.get('ok'):
        return out
    first = first_of(s)
    pk = p.ev('([n, k]) => __JS.pick(n, 1, k)', [s, first])
    out['q'] = pk['q']
    out['exp'] = pk['e']
    expn = pk['e']['n']
    r = p.ev('([n, q]) => __JS.run(n, q, 90000)', [s, pk['q']])   # 데우기(데이터 받기 · 캐시) 겸 첫 그림
    out['warm'] = r
    if full:
        ms = []
        for _ in range(3):
            r2 = p.ev('([n, q]) => __JS.run(n, q, 90000)', [s, pk['q']])
            ms.append(r2.get('ms'))
            r = r2
        out['ms'] = ms
        out['ms_med'] = med(ms)
    out['first'] = r
    n0 = r.get('n') or 0
    if p.tag == 'new' and expn > n0:
        out['gest'] = p.gesture(s)
    out['fill'] = p.ev('([n, t]) => __JS.fill(n, t)', [s, 150000])
    out['scan'] = p.ev('n => __JS.scan(n)', s)
    if full and s in LAST and p.tag == 'new':
        at = p.ev('n => __JS.lastHit(n)', s)
        okc = p.click(at)
        p.wait(600)
        out['last'] = {'at': at and {k: at.get(k) for k in ('cx', 'cy', 'on')}, 'clicked': okc, 'chk': p.ev('n => __JS.lastCheck(n)', s)}
    if full and p.tag == 'new' and p.ev('n => __JS.hasQ2(n)', s):
        o2 = p.ev('n => __JS.open(n)', s)
        if o2 and o2.get('ok'):
            r1 = p.ev('([n, q]) => __JS.run(n, q, 90000)', [s, pk['q']])
            mid = p.ev('n => __JS.partial(n)', s) if expn > first else r1.get('n')
            e2 = p.ev('([n, k]) => __JS.pick(n, 2, k)', [s, 0])
            e2n = e2['e']['n']
            r2 = p.ev('([n, q]) => __JS.run(n, q, 90000)', [s, e2['q']])
            p.wait(700)   # 옛 관찰자가 남아 있으면 이 사이에 옛 줄을 붙인다
            after = p.ev('n => __JS.rowsN(n)', s)
            f2 = p.ev('([n, t]) => __JS.fill(n, t)', [s, 90000])
            out['chg'] = {'q1': pk['q'], 'mid': mid, 'q2': e2['q'], 'exp2': e2n, 'now': r2.get('n'), 'after700': after['n'], 'end': f2['n'], 'pend': f2['pend']}
    out['errs'] = p.ev('() => __JS.errs()')
    return out


def judge_new(R, dev, eng, base=None):
    s = R['spot']
    g = '%s/%s/%s' % (s, eng[:2], dev)
    o = R.get('open') or {}
    if not o.get('ok'):
        T(g, '창 열기', False, o)
        return
    e = R['exp']
    expn = e['n']
    first = first_of(s)
    T(g, 'A 표본 · 기대 수(앱 식으로 직접 거름) > 옛 자르던 수(%d)' % CAP[s], expn > CAP[s], {'q': R['q'], 'exp': e})
    r = R['first']
    T(g, 'A 셈 글 = 기대 수', r.get('cnt') == expn, {'셈': r.get('cnt'), '기대': expn})
    T(g, 'B 처음 줄 = min(기대, %d) · 끝 표지 %s' % (first, '1' if expn > first else '0'),
      r.get('n') == min(expn, first) and r.get('pend') == (1 if expn > first else 0), {'줄': r.get('n'), '표지': r.get('pend')})
    if expn > first:
        gs = R.get('gest') or {}
        T(g, 'C 진짜 굴림(%s · 끝 표지 700px 앞에서) → 다음 줄이 붙는다' % gs.get('how'), gs.get('n1', 0) > gs.get('n0', 0), {k: gs.get(k) for k in ('n0', 'n1', 'tries', 'pre', 'sc')})
        sb, sa = gs.get('st_before'), gs.get('st_after')
        T(g, 'C2 붙인 뒤 굴림 자리 그대로(맨 위로 튀지 않음 · 50px 안)', sb is not None and sa is not None and sa >= sb - 50, {'붙이기 앞': sb, '붙인 뒤(600ms)': sa})
    f = R['fill']
    if s == 'cvb':
        T(g, 'D 끝까지 굴려 붙은 쪽 = 기대 쪽 · 곳 = 기대 곳 · 표지 0', f['n'] == expn and f.get('snips') == e.get('total') and f['pend'] == 0,
          {'쪽': f['n'], '곳': f.get('snips'), '기대': [expn, e.get('total')], '표지': f['pend'], 'ms': f['ms']})
    else:
        T(g, 'D 끝까지 굴려 붙은 줄 = 기대 수 · 표지 0', f['n'] == expn and f['pend'] == 0, {'줄': f['n'], '기대': expn, '표지': f['pend'], 'ms': f['ms']})
    sc = R.get('scan') or {}
    ov = sc.get('over') or {}
    okg = bool(sc) and sc.get('docOver', 9) <= 1 and sc.get('winIn') and sc.get('cntIn') and sc.get('lastIn') is not False and sc.get('rowsCut', 9) == 0 and ov.get('other', 9) == 0
    T(g, 'G 화면 훑기 — 넘침 · 잘림 0(문서 · 창 · 셈 줄 · 끝 줄 · 줄 밖으로 나간 새 것 0)', okg,
      {k: sc.get(k) for k in ('vw', 'docOver', 'boxOver', 'winIn', 'cntIn', 'cntTxt', 'lastIn', 'rowsCut', 'sc')} | {'새 넘침': ov.get('other'), '예': ov.get('otherEx')})
    if ov.get('pre'):
        bsc = ((base or {}).get('scan') or {}).get('over') or {}
        N(g, 'G2 줄 안 줄바꿈 없는 글(white-space:nowrap)이 그릇 밖으로 — 옛 판 줄 꼴 그대로(안 고침 · 결과 줄 꼴 그대로) · 끝까지 붙여 더 많이 보일 뿐',
          {'새 판': [ov.get('pre'), str(ov.get('preMax')) + 'px', ov.get('preEx')], '바탕(같은 기기 · 자르던 수만큼)': [bsc.get('pre'), str(bsc.get('preMax')) + 'px'] if bsc else '안 잼'})
    if 'last' in R:
        L = R['last']
        T(g, 'H 마지막 줄 누름(진짜 %s) = 그 항목' % ('마우스' if dev == 'pc' else '톡'), L['clicked'] and (L['chk'] or {}).get('ok'), L)
    if 'chg' in R:
        c = R['chg']
        T(g, 'E 검색어 바꾸기(굴린 뒤) = 바로 min(기대2, %d) · 700ms 뒤 그대로 · 끝까지 = 기대2(옛 줄 섞임 0)' % first,
          c['now'] == min(c['exp2'], first) and c['after700'] == c['now'] and c['end'] == c['exp2'] and c['pend'] == 0 and (c['mid'] > first if R['exp']['n'] > first else True), c)
    if 'ms_med' in R and base is not None:
        bm = base.get('ms_med')
        nm = R['ms_med']
        dd = {'새': R['ms'], '바탕': base.get('ms'), '비': (round(nm / bm, 2) if bm and nm else None), '차 ms': (round(nm - bm, 1) if bm is not None and nm is not None else None),
              '처음 줄': '%s → %s' % (min(CAP[s], R['exp']['n']), min(first, R['exp']['n']))}
        if s in SEARCHBOX:
            ok = bm is not None and nm is not None and (nm <= bm * 1.2 or nm - bm <= 16.7)
            T(g, 'F 첫 그림 빠르기(검색 칸 입력 → 처음 줄 · 세 번 가운데 값) ≤ 바탕 × 1.2 · 또는 늘어난 것이 한 프레임(16.7ms) 안', ok, dd)
        else:
            N(g, 'A-5 찾기 창 — 끝까지 찾으며 늘어난 시간(입력 → 처음 줄 · 세 번 가운데 값 · 디바운스 %s)' % DEB.get(s, '없음'), dd)
    errs = [x for x in (R.get('errs') or []) if 'Failed to load' not in x]
    if errs:
        N(g, '콘솔 오류', errs)


def judge_base(R):
    s = R['spot']
    g = '%s/바탕' % s
    o = R.get('open') or {}
    if not o.get('ok'):
        T(g, '헛잣대 — 바탕 창 열기', False, o)
        return
    expn = R['exp']['n']
    f = R['fill']
    cap_hit = f['n'] < expn
    T(g, '헛잣대 — 바탕은 끝까지 굴려도 기대 수에 못 미친다(자르던 수에서 멈춤 = D FAIL)', cap_hit,
      {'바탕 줄': f['n'], '기대': expn, '셈': (R.get('first') or {}).get('cnt'), 'snips': f.get('snips')})


def main():
    t00 = time.time()
    stages = []
    os.makedirs(WORK, exist_ok=True)
    spots = [x for x in SPOTS if (not ONLY or x in ONLY)]
    if QJ.SMOKE:
        spots = [x for x in spots if x in SMOKE_SPOTS]
    vok = vendor()
    if not vok and 'cvb' in spots:
        N('준비', 'cvb 뺌', 'pdf.js 사본이 없어 교재 창을 못 연다')
        spots = [x for x in spots if x != 'cvb']
    new_src = io.open(NEWF, encoding='utf-8').read()
    base_src = None
    if QJ.GATE:
        b = git('show', '%s:jo/index.html' % BASE_REV)
        QJ.sub('git:show-app')
        if b.returncode != 0:
            T('준비', '바탕 %s 풀기' % BASE_REV, False, b.stderr.decode('utf-8', 'replace')[:200])
        else:
            base_src = b.stdout.decode('utf-8')
    import hashlib
    N('준비', '판', {'new': NEWF, 'new_md5_lf': hashlib.md5(new_src.replace('\r\n', '\n').encode('utf-8')).hexdigest(), 'base': BASE_REV if base_src else None,
                    'base_md5_lf': hashlib.md5(base_src.encode('utf-8')).hexdigest() if base_src else None, 'mode': QJ.MODE, 'spots': len(spots)})
    B, BP, NEW_PC, NEW_PH, WK = {}, {}, {}, {}, {}
    with sync_playwright() as pw:
        if 'chromium' in ENGS:
            br = pw.chromium.launch(args=['--disable-gpu'])
            try:
                if base_src:
                    with QJ.stage('바탕 PC'):
                        p = Pg(br, 'chromium', 'base', base_src, 'pc')
                        p.ev('() => __JS.seed()')
                        for s in spots:
                            try:
                                B[s] = measure(p, s, True)
                            except Exception as e:
                                B[s] = {'spot': s, 'open': {'ok': False, 'why': 'harness: ' + str(e)[:200]}}
                            print('… 바탕', s, json.dumps({k: B[s].get(k) for k in ('q', 'exp', 'ms_med')}, ensure_ascii=False, default=str)[:200], flush=True)
                        p.close()
                    if not QJ.SMOKE:
                        with QJ.stage('바탕 폰(훑기 맞대기)'):
                            p = Pg(br, 'chromium', 'base', base_src, 'phone')
                            p.ev('() => __JS.seed()')
                            for s in spots:
                                try:
                                    o = p.ev('n => __JS.open(n)', s)
                                    if o and o.get('ok'):
                                        pk = p.ev('([n, k]) => __JS.pick(n, 1, k)', [s, first_of(s)])
                                        p.ev('([n, q]) => __JS.run(n, q, 90000)', [s, pk['q']])
                                        p.ev('([n, t]) => __JS.fill(n, t)', [s, 60000])
                                        BP[s] = {'scan': p.ev('n => __JS.scan(n)', s)}
                                except Exception as e:
                                    BP[s] = {'err': str(e)[:160]}
                            p.close()
                with QJ.stage('새 판 PC'):
                    p = Pg(br, 'chromium', 'new', new_src, 'pc')
                    sd = p.ev('() => __JS.seed()')
                    N('준비', '심은 기록', sd)
                    for s in spots:
                        try:
                            NEW_PC[s] = measure(p, s, True)
                        except Exception as e:
                            NEW_PC[s] = {'spot': s, 'open': {'ok': False, 'why': 'harness: ' + str(e)[:200]}}
                        print('… 새 PC', s, json.dumps({k: NEW_PC[s].get(k) for k in ('q', 'exp', 'ms_med')}, ensure_ascii=False, default=str)[:200], flush=True)
                    p.close()
                if not QJ.SMOKE:
                    with QJ.stage('새 판 폰'):
                        p = Pg(br, 'chromium', 'new', new_src, 'phone')
                        p.ev('() => __JS.seed()')
                        for s in spots:
                            try:
                                NEW_PH[s] = measure(p, s, False)
                            except Exception as e:
                                NEW_PH[s] = {'spot': s, 'open': {'ok': False, 'why': 'harness: ' + str(e)[:200]}}
                            print('… 새 폰', s, json.dumps({k: NEW_PH[s].get(k) for k in ('q', 'exp')}, ensure_ascii=False, default=str)[:200], flush=True)
                        gt = p.ev('() => __JS.gt()')
                        N('확인', '.gt 폰 390 — 연결한 근거 줄(글 폭 / 줄 폭 · ✎ 단추 자리) · 고치지 않음(결정로그 10/10 00:36)', gt)
                        if SHOT and gt and gt.get('ok'):
                            try:
                                os.makedirs(SHOT, exist_ok=True)
                                p.pg.locator('.ggrefbox').first.screenshot(path=os.path.join(SHOT, 'gt_phone390.png'))
                            except Exception as e:
                                N('확인', '.gt 그림 못 찍음', str(e)[:160])
                        p.close()
            finally:
                br.close()
        if 'webkit' in ENGS and not QJ.SMOKE:
            try:
                wk = pw.webkit.launch()
            except Exception as e:
                wk = None
                N('webkit', '띄우기', '이 컴퓨터에 WebKit 없음 — 안 잼 (%s)' % str(e)[:120])
            if wk:
                try:
                    with QJ.stage('새 판 webkit 폰'):
                        p = Pg(wk, 'webkit', 'new', new_src, 'phone')
                        p.ev('() => __JS.seed()')
                        for s in [x for x in spots if x in WK_SPOTS]:
                            try:
                                WK[s] = measure(p, s, False)
                            except Exception as e:
                                WK[s] = {'spot': s, 'open': {'ok': False, 'why': 'harness: ' + str(e)[:200]}}
                        p.close()
                finally:
                    wk.close()
    for srv, _ in SERVERS.values():
        try:
            srv.shutdown()
        except Exception:
            pass
    # ── 판정 ──
    for s in spots:
        if s in B:
            judge_base(B[s])
        if s in NEW_PC:
            judge_new(NEW_PC[s], 'pc', 'chromium', B.get(s))
        if s in NEW_PH:
            judge_new(NEW_PH[s], 'phone', 'chromium', BP.get(s))
        if s in WK:
            judge_new(WK[s], 'phone', 'webkit')
    raw = os.path.join(WORK, 'raw.json')
    try:
        json.dump({'B': B, 'PC': NEW_PC, 'PH': NEW_PH, 'WK': WK}, io.open(raw, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    except Exception:
        pass
    npass = sum(1 for x in RES if x[2] is True)
    nfail = sum(1 for x in RES if x[2] is False)
    sec = round(time.time() - t00, 1)
    lines = []
    for grp, name, ok, d in RES:
        dd = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str)
        lines.append('%s | %s · %s | %s' % ('INFO' if ok is None else ('PASS' if ok else 'FAIL'), grp, name, dd[:900]))
    lines.append('PASS %d · FAIL %d · %s초 · 모드 %s' % (npass, nfail, sec, QJ.MODE))
    try:
        io.open(OUTF, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    except Exception as e:
        print('결과 파일 못 씀', e)
    print('PASS %d · FAIL %d · %s초 · 모드 %s · 결과 %s' % (npass, nfail, sec, QJ.MODE, OUTF), flush=True)
    if '--keep' not in sys.argv:
        shutil.rmtree(WORK, ignore_errors=True)
    return 1 if nfail else 0


if __name__ == '__main__':
    sys.exit(main())
