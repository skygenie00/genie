# -*- coding: utf-8 -*-
r"""_task_jagwa_uid §B 관문 — 생물·지학 문항 번호 새 꼴 · 데이터 · 그림 · 기록 옮김 · 화면 · 차례 · 물리 무변

  python _harness_jagwa_uid.py [--new <앱>] [--eng chromium,webkit] [--only d1,m3,...] [--res <결과>]

  NEW 앱 = genie 작업트리 jagwa/index.html · BASE 앱 = genie HEAD(바로 앞 인도판 jagwa_phone_win fb89ad2)
  NEW 데이터 = studyplandata 작업트리(_uid_rename.py write 뒤) · BASE 데이터 = studyplandata HEAD(git archive)
  기록 = studyplandata 기록.json 사본(원격 44a39616 과 같음) 을 route 로 · PUT 은 가로채 몸통만 모은다(밖으로 안 나감)
  기기 하나 = 브라우저 문맥 하나(IndexedDB·localStorage 유지) — 같은 출처에서 앱·데이터를 갈아 끼워 「옛 판 → 새 판」을 잰다
  ⚠ 자과앱 픽셀 게이트 없음(CLAUDE.md) — DOM 글자 · 자리 · 개수로 잰다
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import io, json, os, re, sys, time, hashlib, subprocess, shutil, tarfile, http.server, socketserver, threading, urllib.parse, collections, tempfile
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _uid_rule as UR


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = _roots.genie()
SPD = _roots.spd()
NEWF = ARG('--new', os.path.join(GENIE, 'jagwa', 'index.html'))
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_uid_result.txt'))
WORK = os.path.join(tempfile.gettempdir(), 'h_jagwa_uid')
RES = []
KEYS = ['bogi', 'unit', 'bpg', 'crop', 'tfix', 'gg', 'ggref', 'pick']
from playwright.sync_api import sync_playwright   # noqa: E402


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    print('INFO | %s · %s | %s' % (grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def git(repo, *a):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def base_data():
    """studyplandata HEAD 를 풀어 둔다(bio · earth · phys) — 옛 번호·옛 그림 이름"""
    d = os.path.join(WORK, 'spd_base')
    if os.path.isdir(os.path.join(d, 'earth')):
        return d
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    tf = os.path.join(WORK, 'base.tar')
    open(tf, 'wb').write(git(SPD, 'archive', 'HEAD', 'bio', 'earth', 'phys'))
    with tarfile.open(tf) as t:
        t.extractall(d)
    return d


INIT = r"""
(()=>{
  try{localStorage.setItem('subj','__SUBJ__')}catch(e){}
  try{localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}))}catch(e){}
  window.__err=[];window.__PUTS=[];
  window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+(e.lineno||''))});
  window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
  const nf=window.fetch.bind(window);
  window.fetch=async function(url,opt){
    opt=opt||{};const u=String(url);
    const m=/api\.github\.com\/repos\/([^\/]+\/[^\/]+)\/contents\/([^?]+)/.exec(u);
    if(!m){ if(/^https?:/i.test(u)&&u.indexOf(location.origin)!==0&&!/cdnjs|jsdelivr|googleapis|gstatic/.test(u))
              return {ok:false,status:599,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
            return nf(url,opt) }
    const path=decodeURIComponent(m[2]);
    if((opt.method||'GET')==='PUT'){try{const b=JSON.parse(opt.body);window.__PUTS.push({path,text:decodeURIComponent(escape(atob(b.content)))})}catch(e){window.__PUTS.push({path,err:String(e)})}
      return {ok:true,status:200,json:async()=>({content:{sha:'x'}}),text:async()=>''}}
    const r=await nf('/data/'+encodeURI(path),{cache:'no-store'});
    if(!r.ok)return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
    const acc=(opt.headers||{}).Accept||'';
    if(acc.indexOf('raw')>=0)return r;
    return {ok:true,status:200,json:async()=>({sha:r.headers.get('X-Sha')||'sha'}),text:async()=>JSON.stringify({sha:r.headers.get('X-Sha')||'sha'})};
  };
})();
"""

JS = r"""
window.__J={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 vis(e){return !!e&&e.isConnected&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0},
 ready(){return typeof DATA!=='undefined'&&DATA.length>0&&(typeof GG_READY==='undefined'||GG_READY)},
 puts(){return (window.__PUTS||[]).map(p=>({path:p.path,len:(p.text||'').length}))},
 lastPut(path){const L=(window.__PUTS||[]).filter(p=>p.path===path);return L.length?L[L.length-1].text:null},
 async sync(){try{await syncRecords(true)}catch(e){return 'ERR '+e}await new Promise(r=>setTimeout(r,400));return (window.__PUTS||[]).length},
 mig(){return window.__JGMIG||0},
 u(){try{return JSON.parse(localStorage.getItem(U_KEY)||'{}')}catch(e){return {}}},
 gone(){try{return JSON.parse(localStorage.getItem(GONE_KEY)||'{}')}catch(e){return {}}},
 stores(keys){const o={};keys.forEach(k=>{const v=SYNC_REF[k]?SYNC_REF[k].g():undefined;o[k]=v?JSON.parse(JSON.stringify(v)):null});return o},
 rows(){return DATA.map(r=>[r[F.NO],r[F.CODE],r[F.OLDU]||'',typeof codeShow==='function'?codeShow(r):''])},
 list(){return [...document.querySelectorAll('#list .item')].filter(__J.vis).map(d=>({uid:d.dataset.uid||'',num:__J.tx(d.querySelector('.num'))}))},
 heat(){return [...document.querySelectorAll('[title]')].filter(e=>/회독|^\S+ /.test(e.title)&&e.onclick).slice(0,4000).map(e=>e.title.split(' ')[0])},
 async card(no){try{closeView()}catch(e){}await new Promise(r=>setTimeout(r,150));await openView(no);await new Promise(r=>setTimeout(r,1600));
   const c=document.getElementById('card');const h=document.getElementById('vT1');
   const img=c&&c.querySelector('img');
   return {head:__J.tx(h),card:__J.tx(c).replace(/\s+/g,' '),bogi:c?[...c.querySelectorAll('.bogi .row .ox button.on')].map(b=>b.closest('.row').dataset.k+b.dataset.v):[],
     tfix:c?c.querySelectorAll('.fx,.fixed').length:0,gg:__J.tx(c&&c.querySelector('.ggwrap')).length,img:!!img,imgOk:img?img.complete&&img.naturalWidth>0:null}},
 heatNos(){const m={};DATA.forEach(r=>m[String(codeShow(r))]=r[F.NO]);return [...document.querySelectorAll('#spec i')].filter(i=>i.title).map(i=>m[i.title.split(' ')[0]]||('?'+i.title.split(' ')[0]))},
 heatCodes(){return [...document.querySelectorAll('#spec i')].filter(i=>i.title).map(i=>i.title.split(' ')[0])},
 memoNos(){try{memoSheet()}catch(e){return 'ERR '+e}const b=document.getElementById('memoSheet');const a=b?[...b.querySelectorAll('.memor')].map(x=>+x.dataset.no):[];if(b)b.remove();return a},
 yearNos(){const ys=[...new Set(DATA.filter(r=>r[F.SRC]==='변리사').map(r=>r[F.YEAR]))].sort();const out=[];const m={};DATA.forEach(r=>m[r[F.CODE]]=r[F.NO]);
   for(const y of ys.slice(-3)){const n0=document.querySelectorAll('.sheet').length;try{yearSheet(y)}catch(e){return 'ERR '+e}const L=[...document.querySelectorAll('.sheet')];const b=L.length>n0?L[L.length-1]:null;
     out.push(b?[...b.querySelectorAll('.histrow .rn')].map(x=>m[x.textContent.trim()]||('?'+x.textContent.trim())):[]);if(b)b.remove()}return out},
 ggHeads(){return [...document.querySelectorAll('#esres [data-ggres] .cd')].map(e=>e.textContent.trim())},
 err(){return (window.__err||[]).slice(0,8)}
};
"""


class Srv:
    """같은 출처에서 앱·데이터 폴더·기록을 갈아 끼운다"""
    def __init__(self):
        self.app = b''; self.spd = SPD; self.rec = {}; self.static = {}
        me = self

        class Hh(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *a, **k):
                pass

            def do_GET(self):
                p = urllib.parse.unquote(self.path.split('?')[0])
                if p in ('/', '/app.html'):
                    b = me.app; ct = 'text/html; charset=utf-8'
                elif p.startswith('/data/'):
                    rel = p[6:]
                    if rel in me.rec:
                        b = me.rec[rel]
                    else:
                        f = os.path.join(me.spd, rel.replace('/', os.sep))
                        if not os.path.isfile(f):
                            self.send_response(404); self.end_headers(); return
                        b = open(f, 'rb').read()
                    ct = 'application/octet-stream'
                elif p.lstrip('/') in me.static:   # 앱 옆 파일(motion/…) — 없으면 404
                    b = me.static[p.lstrip('/')]
                    ct = 'text/html; charset=utf-8' if p.endswith('.html') else 'application/json' if p.endswith('.json') else 'application/octet-stream'
                else:
                    self.send_response(404); self.end_headers(); return
                self.send_response(200); self.send_header('Content-Type', ct); self.send_header('Content-Length', str(len(b)))
                self.send_header('X-Sha', hashlib.sha1(b).hexdigest()); self.send_header('Cache-Control', 'no-store'); self.end_headers(); self.wfile.write(b)
        self.srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), Hh); self.srv.daemon_threads = True
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.port = self.srv.server_address[1]


class Dev:
    """기기 하나(문맥 하나) — load(앱, 데이터 폴더, 과목) 로 같은 출처에서 다시 연다"""
    def __init__(self, br, eng, phone=False):
        self.eng = eng; self.S = Srv()
        vp = {'width': 390, 'height': 844} if phone else {'width': 1553, 'height': 900}
        self.ctx = br.new_context(viewport=vp, device_scale_factor=1, has_touch=True)
        OK = ('http://127.0.0.1', 'https://cdnjs.cloudflare.com/', 'https://cdn.jsdelivr.net/', 'https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')
        self.ctx.route('**/*', lambda rt: rt.continue_() if rt.request.url.startswith(OK) else rt.abort())
        self.pg = None; self.errs = []

    def load(self, app, spd, subj, rec=None, static=None):
        self.S.app = app; self.S.spd = spd; self.S.rec = dict(rec or {}); self.S.static = dict(static or {})
        if self.pg:
            self.pg.close()
        self.ctx.clear_cookies()
        self.pg = self.ctx.new_page(); self.pg.set_default_timeout(150000)
        self.pg.add_init_script(INIT.replace('__SUBJ__', subj))
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:200]))
        self.pg.goto('http://127.0.0.1:%d/app.html' % self.S.port, wait_until='load')
        self.pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=120000)
        self.pg.evaluate(JS)
        for _ in range(120):
            if self.ev("()=>__J.ready()"):
                break
            self.pg.wait_for_timeout(250)
        self.pg.wait_for_timeout(2500)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass
        try:
            self.S.srv.shutdown()
        except Exception:
            pass


# ══════════ 데이터 ══════════
def jl(b):
    if isinstance(b, str) and b.lstrip()[:1] in ('{', '['):
        return json.loads(b)   # 앱에서 받은 JSON 글
    return json.loads(b.decode('utf-8') if isinstance(b, bytes) else open(b, 'rb').read().decode('utf-8'))


def d1():
    G = 'd1'
    BD = base_data()
    ex = {('bio', 'G57-05'): 'B20-57-05', ('bio', 'G38-01'): 'B01-38-01', ('bio', 'T012'): 'B012T', ('bio', 'E001'): 'B001E', ('earth', 'G32-01'): 'G95-32-01', ('earth', 'C1-010'): 'G1-010C'}
    alln = set()
    for s, want in (('bio', 746), ('earth', 704)):
        new = jl(os.path.join(SPD, s, '문항.json')); old = jl(os.path.join(BD, s, '문항.json'))
        bad = [r['uid'] for r in new if UR.new_uid(s, r.get('옛uid', '')) != r['uid']] if len(new) == want else ['행 수']
        diff = [i for i, (a, b) in enumerate(zip(old, new)) if {k: v for k, v in a.items() if k not in ('uid', '그림')} != {k: v for k, v in b.items() if k not in ('uid', '옛uid', '그림')} or a['uid'] != b.get('옛uid')]
        keys = [list(b.keys())[:2] for b in new[:1]]
        dup = len(new) - len({r['uid'] for r in new}); cross = len({r['uid'] for r in new} & alln); alln |= {r['uid'] for r in new}
        exok = {o: next((r['uid'] for r in new if r.get('옛uid') == o), None) for (ss, o) in ex if ss == s}
        T(G, '%s 문항.json 행 %d — uid = 새 규칙(어긋남 %d) · 옛uid = 바탕 uid · 다른 칸·행 차례 무변(다른 행 %d) · 겹침 %d · 과목 사이 겹침 %d · 보기 값 %s' % (s, want, len(bad), len(diff), dup, cross, exok),
          not bad and not diff and dup == 0 and cross == 0 and all(exok[o] == ex[(s, o)] for o in exok) and keys == [['uid', '옛uid']], {'어긋남': bad[:5], '다른 행': diff[:5]})
        # 그림
        img = os.path.join(SPD, s, 'img'); bimg = os.path.join(BD, s, 'img')
        oldq = [f for f in os.listdir(bimg) if f.startswith('q')]
        miss, same = [], 0
        for f in oldq:
            o = f[1:-4]; n = UR.new_uid(s, o); p = os.path.join(img, 'q%s.jpg' % n)
            if not os.path.exists(p):
                miss.append(n); continue
            same += open(p, 'rb').read() == open(os.path.join(bimg, f), 'rb').read()
        oldleft = [f for f in os.listdir(img) if f.startswith('q') and re.fullmatch(r'q(G\d\d-\d\d|[TE]\d{3}|C\d-\d{3})\.jpg', f)]
        refs = sorted(f for f in os.listdir(img) if f.startswith('ref')); brefs = sorted(f for f in os.listdir(bimg) if f.startswith('ref'))
        T(G, '%s 그림 q<새uid>.jpg %d(바이트 = 옛 파일 %d) · 옛 이름 0 · 참고 그림 %d 무변' % (s, len(oldq) - len(miss), same, len(refs)),
          not miss and same == len(oldq) and not oldleft and refs == brefs and all(open(os.path.join(img, f), 'rb').read() == open(os.path.join(bimg, f), 'rb').read() for f in refs),
          {'없음': miss[:5], '옛 이름': oldleft[:5]})
    out = subprocess.run([sys.executable, os.path.join(HERE, '_uid_rename.py')], capture_output=True, text=True, encoding='utf-8').stdout
    T(G, '⚙ _uid_rename 한 번 더 = 문항.json 같음 · 그림 옮김 0(멱등)', out.count('문항.json 같음') == 2 and '그림 파일 옮김 0' in out, out.strip()[:300])
    T(G, '생물 146 = 196 · 지학 198 — 합 394', len([f for f in os.listdir(os.path.join(SPD, 'bio', 'img')) if f.startswith('q')]) + len([f for f in os.listdir(os.path.join(SPD, 'earth', 'img')) if f.startswith('q')]) == 394, '')


# ══════════ 기록 옮김 ══════════
def cnt(d):
    """기록 몸통 셈 — 칸 열쇠 · 옛·새 열쇠 · 값 속 uid"""
    D = d.get('data', {}); U = d.get('u', {}); Gn = d.get('gone', {})
    o = {}
    for k in KEYS:
        v = D.get(k) or {}
        o[k] = len(v)
    return o


def m3(br, eng):
    """지학 기기 하나 — 옛 판(BASE 앱 + BASE 데이터)으로 기록을 받아 둔 뒤 새 판(NEW 앱 + NEW 데이터)으로 연다 → 옮김 → 올린 몸통"""
    G = 'm3'
    BD = base_data()
    rec = open(os.path.join(SPD, 'earth', '기록.json'), 'rb').read()
    base_rec = jl(rec)
    O2N = {r['옛uid']: r['uid'] for r in jl(os.path.join(SPD, 'earth', '문항.json'))}
    dv = Dev(br, eng)
    try:
        dv.load(APPS['BASE'], BD, 'earth')
        dv.ev("()=>__J.sync()")
        before = {'stores': dv.ev("k=>__J.stores(k)", KEYS), 'u': dv.ev("()=>__J.u()")}
        dv.load(APPS['NEW'], SPD, 'earth')
        dv.ev("()=>__J.sync()"); dv.pg.wait_for_timeout(1500); dv.ev("()=>__J.sync()")
        mig = dv.ev("()=>__J.mig()")
        body = jl(dv.ev("p=>__J.lastPut(p)", 'earth/기록.json') or '{}')
        after = {'stores': dv.ev("k=>__J.stores(k)", KEYS), 'u': dv.ev("()=>__J.u()"), 'gone': dv.ev("()=>__J.gone()")}
        D = body.get('data', {}); U = body.get('u', {}); Gn = body.get('gone', {})
        rows = []
        for k in KEYS:
            b0 = before['stores'].get(k) or {}
            v = D.get(k) or {}
            rows.append({'칸': k, '바탕': len(b0), '올린': len(v), '옛 열쇠': sum(1 for c in v if c in O2N), '새 열쇠 = 옮긴 것': sorted(v.keys()) == sorted(O2N.get(c, c) for c in b0)})
        ok1 = all(r['바탕'] == r['올린'] and r['옛 열쇠'] == 0 and r['새 열쇠 = 옮긴 것'] for r in rows)
        T(G, '%s 지학 기기(옛 판에서 기록 받음) → 새 판 열림 → 옮김 %d → 올린 몸통: 칸마다 열쇠 수 = 바탕 · 옛 uid 열쇠 0' % (eng, mig), ok1 and mig > 0, rows)
        bu = before['u']
        pairs = [(x, '%s|%s' % (x.split('|', 1)[0], O2N[x.split('|', 1)[1]])) for x in bu if x.split('|', 1)[0] in KEYS and x.split('|', 1)[1] in O2N]
        same = sum(1 for o, n in pairs if U.get(n) == bu[o]); oldu = sum(1 for o, n in pairs if o in U); tomb = sum(1 for o, n in pairs if o in Gn)
        T(G, '%s 도장 — 「칸|새uid」 %d = 바탕 「칸|옛uid」 %d · 값 같음 %d · 옛 도장 남음 %d · 옛 열쇠 묘비 %d(= 옮긴 칸 수)' % (eng, sum(1 for o, n in pairs if n in U), len(pairs), same, oldu, tomb),
          same == len(pairs) and oldu == 0 and tomb == len(pairs) and len(pairs) > 0, {'표본': pairs[:3]})
        gr = D.get('ggref') or {}
        inval = sum(1 for c, a in gr.items() for x in (a or []) if x in O2N)
        T(G, '%s ggref 값 속 옛 uid 0(바탕 값 속 %d)' % (eng, sum(1 for c, a in (before['stores'].get('ggref') or {}).items() for x in (a or []) if x in O2N)), inval == 0, inval)
        # 멱등 — 두 번째 열림: 옮김 0 · 도장 새로 0 · 올린 몸통 = 첫 판
        u1 = dv.ev("()=>__J.u()")
        dv.load(APPS['NEW'], SPD, 'earth')
        dv.ev("()=>__J.sync()")
        u2 = dv.ev("()=>__J.u()"); mig2 = dv.ev("()=>__J.mig()")
        body2 = jl(dv.ev("p=>__J.lastPut(p)", 'earth/기록.json') or '{}')
        newst = [x for x in u2 if u2[x] != u1.get(x)]
        T(G, '%s 두 번째 열림 — 옮김 0 · 도장 새로 찍힘 0 · 올린 data = 첫 판(이 앱은 맞출 때마다 올린다 — PUT 자체는 늘 1)' % eng,
          mig2 == 0 and not newst and body2.get('data') == body.get('data'), {'옮김': mig2, '새 도장': newst[:5]})
        return body
    finally:
        dv.close()


def m5(br, eng, bodyA):
    """두 기기 — A 가 옮겨 올린 몸통 = 원격 · B = 옛 판으로 옛 기록을 가진 채 새 판 · 같은 결과 · 두 벌 0 · 옛·새 둘 다(새 도장이 늦으면 새 값)"""
    G = 'm5'
    if not bodyA:
        N(G, '%s A 몸통 없음' % eng, ''); return
    BD = base_data()
    O2N = {r['옛uid']: r['uid'] for r in jl(os.path.join(SPD, 'earth', '문항.json'))}
    dv = Dev(br, eng)
    try:
        dv.load(APPS['BASE'], BD, 'earth'); dv.ev("()=>__J.sync()")
        # B 가 옛 판에서 한 칸을 만짐(옛 열쇠 · 새 판 A 보다 앞선 도장) + A 가 새 열쇠로 더 늦게 만진 칸
        k0 = next(iter((bodyA['data'].get('unit') or {}).keys()))
        o0 = next(o for o, n in O2N.items() if n == k0)
        dv.ev("a=>{UN[a[0]]='9.9';put('kv','unit',UN);const u=JSON.parse(localStorage.getItem(U_KEY)||'{}');u['unit|'+a[0]]=1000;localStorage.setItem(U_KEY,JSON.stringify(u));const s=JSON.parse(localStorage.getItem(SHADOW_KEY)||'{}');(s.unit=s.unit||{})[a[0]]='9.9';localStorage.setItem(SHADOW_KEY,JSON.stringify(s));}", [o0])
        A = json.loads(json.dumps(bodyA)); A['data']['unit'][k0] = '8.8'; A['u']['unit|' + k0] = int(time.time() * 1000)
        dv.load(APPS['NEW'], SPD, 'earth', rec={'earth/기록.json': json.dumps(A, ensure_ascii=False).encode('utf-8')})
        dv.ev("()=>__J.sync()"); dv.pg.wait_for_timeout(1500); dv.ev("()=>__J.sync()")
        st = dv.ev("k=>__J.stores(k)", KEYS)
        dup = {k: sum(1 for c in (st.get(k) or {}) if c in O2N) for k in KEYS}
        same = {k: sorted((st.get(k) or {}).keys()) == sorted((A['data'].get(k) or {}).keys()) for k in KEYS}
        T(G, '%s 기기 B(옛 기록 가진 채 새 판 · 원격 = A 가 옮겨 올린 것) — 칸 열쇠 = A · 옛 열쇠 두 벌 0 · 옛·새 둘 다인 칸(%s)은 도장 늦은 새 값 8.8' % (eng, k0),
          all(v == 0 for v in dup.values()) and all(same.values()) and (st.get('unit') or {}).get(k0) == '8.8', {'옛 열쇠': dup, '열쇠 같음': same, k0: (st.get('unit') or {}).get(k0)})
    finally:
        dv.close()


# ★ uid_unify 옛 잣대 고침(2026-10-04 · 근거 gigu/_task_jagwa_uid_unify.md §A-1 · §A-2 · §B-1) ───────────────────────────────────────────────
#   카드 층(지학·생물) 기록 열쇠가 문항 차례 번호(F.NO)에서 uid 로 바뀌었다 — 번호가 열쇠였던 통(UID_STORES)은 **열 때** uid 로 옮겨 올라간다
#   (옛 칸 묘비는 gone 에 · 도장·값은 옛 칸 그대로). 그래서 「새 앱 + 옛 데이터」 의 올린 몸통 data 는 번호 열쇠 통만 열쇠가 바뀌고(§B-1 셈 무변 ·
#   값 그대로) 나머지 칸(bogi · unit · bpg · crop · tfix · gg · ggref …)은 바이트 그대로여야 한다. 옛 판(uid 열쇠 도입 앞)이면 옛 잣대 그대로.
UID_STORES = ['status', 'note', 'qtype', 'conc', 'gpt', 'twin', 'ansfix', 'frm', 'maskpos', 'omrpos', 'mcard', 'link', 'txt']   # 앱 UID_KEYS(§A-2) — txt 는 「card:<번호>」 칸만
_NUMK = re.compile(r'[1-9]\d*')
_CARDK = re.compile(r'card:([1-9]\d*)')


def uidk(app):
    """그 앱이 카드 층 기록 열쇠를 uid 로 쓰는 판인가(§A-1 의 qk(no) 한 함수가 있나) — 옛 판이면 False"""
    return b'function qk(no)' in (app or b'')


def n2u(spd_dir, subj):
    """문항.json 차례 → uid 표(번호 n = 차례 + 1 · 앱 buildData 의 F.NO · 그 기기가 읽은 문항.json 으로 만든다 — §A-2)"""
    items = json.loads(open(os.path.join(spd_dir, subj, '문항.json'), 'rb').read().decode('utf-8'))
    return {str(i + 1): it['uid'] for i, it in enumerate(items)}


def uidnorm(data, n2u_):
    """기록 data 의 번호 열쇠(UID_STORES) → uid 열쇠 · twin·link 값 속 번호도 uid(§A-2) — 표 밖 번호는 그대로 · 같은 칸이 번호·uid 둘이면 uid 칸을 둔다.
       번호 열쇠판과 uid 열쇠판의 올린 몸통을 같은 꼴로 맞대려는 것이다(값·도장은 안 건드린다)."""
    d = json.loads(json.dumps(data or {}))
    out = {}
    for k, v in d.items():
        if k in UID_STORES and isinstance(v, dict):
            cells, late = {}, []
            for c, x in v.items():
                nc, moved = c, False
                if k == 'txt':
                    m = _CARDK.fullmatch(c)
                    if m and m.group(1) in n2u_:
                        nc, moved = 'card:' + n2u_[m.group(1)], True
                elif _NUMK.fullmatch(c) and c in n2u_:
                    nc, moved = n2u_[c], True
                if k in ('twin', 'link') and isinstance(x, list):
                    x = [n2u_.get(str(y), y) if isinstance(y, (int, str)) and _NUMK.fullmatch(str(y)) else y for y in x]
                if moved:
                    late.append((nc, x))
                else:
                    cells[nc] = x
            for nc, x in late:
                cells.setdefault(nc, x)
            out[k] = cells
        else:
            out[k] = v
    return out


def numkeys(data):
    """UID_STORES 안에 번호 열쇠로 남은 칸 수(§A-1 — 새 판은 번호 열쇠를 쓰지 않는다)"""
    n = 0
    for k in UID_STORES:
        v = (data or {}).get(k)
        if isinstance(v, dict):
            n += sum(1 for c in v if (_CARDK.fullmatch(c) if k == 'txt' else _NUMK.fullmatch(c)))
    return n


def a8(br, eng):
    """새 앱 + 옛 데이터 = 바탕 앱과 같은 화면 · 올린 몸통 같음 · 옮김 0"""
    G = 'a8'
    BD = base_data()
    out = {}
    for who in ('NEW', 'BASE'):
        dv = Dev(br, eng)
        try:
            dv.load(APPS[who], BD, 'earth'); dv.ev("()=>__J.sync()")
            out[who] = {'rows': dv.ev("()=>__J.rows()"), 'list': dv.ev("()=>__J.list()"), 'data': jl(dv.ev("p=>__J.lastPut(p)", 'earth/기록.json') or '{}').get('data'), 'mig': dv.ev("()=>__J.mig()")}
        finally:
            dv.close()
    n, b = out['NEW'], out['BASE']
    # ★ uid_unify 옛 잣대 고침(§A-2 · §B-1) — 새 앱(uid 열쇠판)은 번호 열쇠 통을 uid 로 옮겨 올리니 `올린 data = 바탕` 은 「번호 열쇠 통만 열쇠가 다르고 값은 같다 · 번호 열쇠 0」 로 읽는다.
    #   (칸 이름은 그대로 — 옛 줄은 아래 주석 · 옛 판이면 갈래로 그대로 쓴다. 이 하네스는 NEW 앱 = 작업트리 · BASE 앱 = genie HEAD 인데 줄(워크트리)에서 HEAD = 후보라 둘이 같은 앱이면 uid 열쇠끼리 맞댄다)
    # 옛 줄:  T(G, '%s 새 앱 + 옛 데이터(옛uid 없음) — 보이는 번호·목록 = 바탕 · 올린 data = 바탕 · 옮김 0' % eng,
    #           [x[3] for x in n['rows']] == [x[3] for x in b['rows']] and n['list'] == b['list'] and n['data'] == b['data'] and n['mig'] == 0, {'목록 표본': n['list'][:3], '옮김': n['mig']})
    un = uidk(APPS['NEW'])
    if un:
        n2u_ = n2u(BD, 'earth')
        same_data = uidnorm(n['data'], n2u_) == uidnorm(b['data'], n2u_) and numkeys(n['data']) == 0
    else:
        same_data = n['data'] == b['data']
    T(G, '%s 새 앱 + 옛 데이터(옛uid 없음) — 보이는 번호·목록 = 바탕 · 올린 data = 바탕 · 옮김 0' % eng,
      [x[3] for x in n['rows']] == [x[3] for x in b['rows']] and n['list'] == b['list'] and same_data and n['mig'] == 0,
      {'목록 표본': n['list'][:3], '옮김': n['mig'], 'uid 열쇠판': un, '번호 열쇠 남음(새·바탕)': [numkeys(n['data']), numkeys(b['data'])]})


def a679(br, eng, phone=False):
    """화면 — 번호 표시 새 꼴 · 옛 꼴 0 · 카드 붙은 것 그대로(바탕 앱+바탕 데이터와 번호만 다름) · 목록 차례 = 바탕"""
    G = 'a679' + ('-폰' if phone else '')
    BD = base_data()
    res = {}
    for subj in ('earth', 'bio'):
        rows = jl(os.path.join(SPD, subj, '문항.json'))
        O2N = {r['옛uid']: r['uid'] for r in rows}
        for who, app, spd in (('NEW', APPS['NEW'], SPD), ('BASE', APPS['BASE'], BD)):
            dv = Dev(br, eng, phone)
            try:
                dv.load(app, spd, subj); dv.ev("()=>__J.sync()"); dv.pg.wait_for_timeout(800)
                ev = {'list': dv.ev("()=>__J.list()"), 'rows': dv.ev("()=>__J.rows()"), 'heat': dv.ev("()=>__J.heatNos()"), 'heatc': dv.ev("()=>__J.heatCodes()"),
                      'memo': dv.ev("()=>__J.memoNos()"), 'year': dv.ev("()=>__J.yearNos()")}
                try:
                    r0 = dv.ev("()=>{const e=document.querySelector('.seg2 [data-sm=\"g\"]');if(!e)return null;e.scrollIntoView({block:'nearest'});const b=e.getBoundingClientRect();return [b.x+b.width/2,b.y+b.height/2]}")
                    if r0:
                        (dv.pg.touchscreen.tap if phone else dv.pg.mouse.click)(r0[0], r0[1]); dv.pg.wait_for_timeout(600)
                    ev['gg'] = dv.ev("()=>__J.ggHeads()")
                except Exception as e:
                    ev['gg'] = 'ERR ' + repr(e)[:200]
                try:
                    dv.ev("()=>{if(typeof ggSearchMode==='function')ggSearchMode('q')}")
                except Exception:
                    pass
                if subj == 'earth':
                    rec = jl(os.path.join(SPD, 'earth', '기록.json'))['data']
                    pick = [u for u in (rec.get('bogi') or {}) if u in (rec.get('unit') or {}) and u in (rec.get('crop') or {})][:2] + [u for u in (rec.get('tfix') or {}) if u.startswith('G')][:1] + [u for u in (rec.get('gg') or {}) if u.startswith('C')][:1]
                else:
                    pick = ['G57-05', 'T012', 'E001']
                cards = {}
                for o in pick:
                    u = O2N[o] if who == 'NEW' else o
                    no = dv.ev("u=>{const r=DATA.find(x=>x[F.CODE]===u);return r?r[F.NO]:null}", u)
                    cards[o] = dv.ev("n=>__J.card(n)", no) if no else None
                ev['cards'] = cards
                res[(subj, who)] = ev
            finally:
                dv.close()
        n, b = res[(subj, 'NEW')], res[(subj, 'BASE')]
        oldform = [x for x in n['list'] if re.fullmatch(r'(G\d\d-\d\d-\d+|G\d\d-\d\d|[TE]\d{3}|C\d-\d{3})', x['num']) and not re.fullmatch(r'G\d\d-\d\d-\d\d', x['num'])]
        want = [O2N.get(x['uid'], x['uid']) for x in b['list']]
        T(G, '%s %s 목록 — 번호 = 새 uid(보이는 번호 = 속 uid) · 옛 꼴 0 · 줄 차례 = 바탕(옛→새 짝) · %d 줄' % (eng, subj, len(n['list'])),
          [x['uid'] for x in n['list']] == want and all(x['num'] == x['uid'] for x in n['list']) and not oldform and len(n['list']) > 0,
          {'표본': n['list'][:3], '옛 꼴': oldform[:3]})
        OLDF = r'(G\d\d-\d\d-\d{1,2}|G\d\d-\d\d|[TE]\d{3}|C\d-\d{3})'
        newf = (r'B\d\d-\d\d-\d\d|B\d{3}[TE]' if subj == 'bio' else r'G\d\d-\d\d-\d\d|G\d-\d{3}C')
        T(G, '%s %s 차례 — 히트맵 %d칸 · 📋 %s줄 · 연도 채점표 %s줄 = 바탕(문항 번호 차례)' % (eng, subj, len(n['heat']), len(n['memo']) if isinstance(n['memo'], list) else n['memo'],
          [len(x) for x in n['year']] if isinstance(n['year'], list) else n['year']),
          n['heat'] == b['heat'] and n['memo'] == b['memo'] and n['year'] == b['year'] and len(n['heat']) > 0,
          {'히트맵 다른 칸': [i for i, (x, y) in enumerate(zip(n['heat'], b['heat'])) if x != y][:5], '📋': [n['memo'][:5], b['memo'][:5]] if n['memo'] != b['memo'] else '같음'})
        hc_bad = [c for c in n['heatc'] if not re.fullmatch(newf, c)]
        gg = n['gg'] if isinstance(n['gg'], list) else []
        gg_bad = [c for c in gg if not re.fullmatch(newf, c)]
        T(G, '%s %s 번호 표시 — 히트맵 title %d · 근거 줄 머리 %d 가 새 꼴 · 옛 꼴 0(근거 줄 수 = 바탕 %s)' % (eng, subj, len(n['heatc']), len(gg), len(b['gg']) if isinstance(b['gg'], list) else b['gg']),
          not hc_bad and not gg_bad and len(gg) == (len(b['gg']) if isinstance(b['gg'], list) else -1),
          {'히트맵 옛 꼴': hc_bad[:5], '근거 옛 꼴': gg_bad[:5], '근거 표본': gg[:3]})
        shown = {x[1]: x[3] for x in n['rows']}
        T(G, '%s %s 모든 행 codeShow = 새 uid(%d)' % (eng, subj, len(shown)), all(k == v for k, v in shown.items()), [k for k, v in shown.items() if k != v][:3])
        for o, cn in n['cards'].items():
            cb = b['cards'].get(o)
            if not cn or not cb:
                T(G, '%s %s 카드 %s — 열림' % (eng, subj, o), False, {'NEW': cn, 'BASE': cb}); continue
            strip = lambda t, code: t.replace(code, '#')
            nb = O2N[o]
            showb = next((x[3] for x in b['rows'] if x[1] == o), o)
            ok = strip(cn['card'], nb) == strip(cb['card'], showb) and cn['bogi'] == cb['bogi'] and cn['tfix'] == cb['tfix'] and cn['gg'] == cb['gg'] and cn['imgOk'] == cb['imgOk'] and nb in cn['head']
            T(G, '%s %s 카드 %s → %s — 카드 글자(번호 뺌)·〈보기〉·글자 고침·근거·그림 = 바탕 · 머리 번호 새 꼴' % (eng, subj, o, nb), ok,
              {'머리': [cn['head'][:40], cb['head'][:40]], '보기': [cn['bogi'], cb['bogi']], 'gg': [cn['gg'], cb['gg']], '그림': [cn['imgOk'], cb['imgOk']]})


def nok(d):
    """근거 항목의 난수 열쇠 k 를 뺀다 — 물리 빈 기기는 열 때마다 ggRestoreNotes_f6cee06 이 새 난수 k 로 되살림을 만든다(판과 무관)"""
    d = json.loads(json.dumps(d or {}))
    for v in (d.get('gg') or {}).values():
        for g in (v or []):
            if isinstance(g, dict):
                g.pop('k', None)
    return d


def p10(br, eng):
    """물리 — 올린 몸통 = 바탕 · 화면 번호 무변"""
    G = 'p10'
    out = {}
    for who in ('NEW', 'BASE'):
        dv = Dev(br, eng)
        try:
            dv.load(APPS[who], SPD, 'phys'); dv.ev("()=>__J.sync()")
            out[who] = {'data': jl(dv.ev("p=>__J.lastPut(p)", 'phys/기록.json') or '{}').get('data'), 'rows': dv.ev("()=>__J.rows()"), 'mig': dv.ev("()=>__J.mig()")}
        finally:
            dv.close()
    T(G, '%s 물리 — 올린 data = 바탕 · 행 번호·보이는 번호 = 바탕 · 옮김 0' % eng,
      nok(out['NEW']['data']) == nok(out['BASE']['data']) and [x[1:] for x in out['NEW']['rows']] == [x[1:] for x in out['BASE']['rows']] and out['NEW']['mig'] == 0, {'옮김': out['NEW']['mig']})


def b11(br, eng):
    """생물 — 기록이 빈 채 → 옮김 0 · 올린 data = 바탕(빈 칸)"""
    G = 'b11'
    BD = base_data()
    out = {}
    for who, spd in (('NEW', SPD), ('BASE', BD)):
        dv = Dev(br, eng)
        try:
            dv.load(APPS[who], spd, 'bio'); dv.ev("()=>__J.sync()")
            out[who] = {'data': jl(dv.ev("p=>__J.lastPut(p)", 'bio/기록.json') or '{}').get('data'), 'mig': dv.ev("()=>__J.mig()")}
        finally:
            dv.close()
    T(G, '%s 생물 기록 빈 채 — 옮김 0 · 올린 data = 바탕' % eng, out['NEW']['mig'] == 0 and out['NEW']['data'] == out['BASE']['data'], {k: v['mig'] for k, v in out.items()})


APPS = {}


def main():
    os.makedirs(WORK, exist_ok=True)
    APPS['NEW'] = open(NEWF, 'rb').read().replace(b'\r\n', b'\n')
    APPS['BASE'] = git(GENIE, 'show', 'HEAD:jagwa/index.html')
    t0 = time.time()
    if not ONLY or 'd1' in ONLY:
        try:
            d1()
        except Exception as e:
            T('RUN', 'd1 멈춤', False, repr(e)[:500])
    with sync_playwright() as pw:
        for eng in ENGS:
            RES.append(('ENG', eng, None, ''))
            br = getattr(pw, eng).launch()
            try:
                bodyA = None
                for k, fn in (('m3', m3), ('m5', None), ('a8', a8), ('a679', a679), ('a679p', None), ('p10', p10), ('b11', b11)):
                    if ONLY and k not in ONLY:
                        continue
                    print('── %s · %s' % (eng, k), flush=True)
                    try:
                        if k == 'm3':
                            bodyA = m3(br, eng)
                        elif k == 'm5':
                            m5(br, eng, bodyA or m3(br, eng))
                        elif k == 'a679p':
                            a679(br, eng, True)
                        else:
                            fn(br, eng)
                    except Exception as e:
                        T('RUN', '%s · %s 멈춤' % (eng, k), False, repr(e)[:600])
            finally:
                br.close()
    npass = sum(1 for r in RES if r[2] is True); nfail = sum(1 for r in RES if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · jagwa_uid · NEW %s · 바탕 genie HEAD %s · studyplandata HEAD %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), os.path.basename(NEWF),
                git(GENIE, 'rev-parse', '--short', 'HEAD').decode().strip(), git(SPD, 'rev-parse', '--short', 'HEAD').decode().strip(), ','.join(ENGS)))
        for g, n, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[ok], g, n, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:900]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
