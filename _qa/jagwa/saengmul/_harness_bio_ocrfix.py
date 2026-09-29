# -*- coding: utf-8 -*-
r"""_task_jagwa_bio_ocrfix §H·§J·§K 관문 — 대상 census · 정오·첫머리 대조 · 앱으로 확인 · 「참고」 칸(R) · 〈보기〉 설명 숨김(K) · 적용 스크립트 멱등

  데이터 = studyplandata bio/문항.json(옛 값) + 고침표 _ocrfix/ocrfix_bio.json 을 _ocrfix_bio.py 로 TEMP 사본에 입힌 것(새 값)
  앱 = genie 작업트리 jagwa/index.html(새 판) · 헛잣대 = genie HEAD 의 jagwa/index.html(고치기 전) — 로컬 띄움 · GitHub 요청은 로컬로 돌리고
       bio/문항.json 은 사본으로 · bio/img/ref*.jpg 는 _ocrfix/ref(인도 전) 또는 studyplandata 에서
  ⚠ 보임·숨김은 **화면 기준** — getComputedStyle(e).display!=='none' 그리고 getBoundingClientRect().height>0 (hidden 속성만 보지 않는다 · 지시서 §K)
  ⚠ 누름은 진짜 포인터(page.mouse.click)로 — 정답·해설 펼침(summary) · 탭 · 참고 그림

쓰기 : python _harness_bio_ocrfix.py        결과 = _harness_bio_ocrfix_result.txt · 스크린샷 = _ocrfix\shots\
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import hashlib, http.server, io, json, os, random, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
GENIE = _roots.genie()
SPDROOT = _roots.spd()
SRC = os.path.join(GENIE, 'jagwa', 'index.html')
QJ = os.path.join(SPDROOT, 'bio', '문항.json')
FIX = os.path.join(HERE, '_ocrfix', 'ocrfix_bio.json')
LISTS = os.path.join(HERE, '_ocrfix', 'ocrfix_bio_lists.json')
REFDIR = os.path.join(HERE, '_ocrfix', 'ref')
SHOTS = os.path.join(HERE, '_ocrfix', 'shots'); os.makedirs(SHOTS, exist_ok=True)
WORK = os.path.join(tempfile.gettempdir(), 'h_bio_ocrfix'); os.makedirs(WORK, exist_ok=True)
NEWQ = os.path.join(WORK, '문항_new.json')
OLDQ = os.path.join(WORK, '문항_old.json')
OLD_REV, OLD_MD5 = '550ee2e5~1', '8f99c582e009efd8ac53f0c90a5e7bce'   # 고치기 전 판 = studyplandata 인도(550ee2e5) 바로 앞
FIXED = ['G57-05', 'G44-01', 'G49-01', 'T001', 'E021']
RES = []


def T(name, ok, detail=''):
    RES.append(('PASS' if ok else 'FAIL', name, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('%s | %s | %s' % ('PASS' if ok else 'FAIL', name, d[:300]), flush=True)


def N(name, detail=''):
    RES.append(('NOTE', name, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('NOTE | %s | %s' % (name, d[:300]), flush=True)


INIT = r"""
(()=>{
  try{localStorage.setItem('subj','__SUBJ__')}catch(e){}
  try{localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}))}catch(e){}
  window.__err=[];
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
    if((opt.method||'GET')==='PUT')return {ok:true,status:200,json:async()=>({content:{sha:'x'}}),text:async()=>''};
    const r=await nf('/data/'+encodeURI(path),{cache:'no-store'});
    if(!r.ok)return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
    const acc=(opt.headers||{}).Accept||'';
    if(acc.indexOf('raw')>=0)return r;
    return {ok:true,status:200,json:async()=>({sha:r.headers.get('X-Sha')||'sha'}),text:async()=>JSON.stringify({sha:r.headers.get('X-Sha')||'sha'})};
  };
})();
"""


def serve(app_text, qjson, subj, tag):
    outdir = os.path.join(WORK, 'srv_' + tag); os.makedirs(outdir, exist_ok=True)
    io.open(os.path.join(outdir, 'app.html'), 'w', encoding='utf-8', newline='').write(app_text)
    spd = os.path.join(SPDROOT, subj)

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=outdir, **k)

        def log_message(self, *a, **k):
            pass

        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            if p.startswith('/data/'):
                rel = p[6:]
                if not rel.startswith(subj + '/'):
                    self.send_response(404); self.end_headers(); return
                sub = rel[len(subj) + 1:]
                if subj == 'bio' and sub == '문항.json' and qjson:
                    f = qjson
                elif subj == 'bio' and sub.startswith('img/ref') and os.path.isfile(os.path.join(REFDIR, sub[4:])):
                    f = os.path.join(REFDIR, sub[4:])
                else:
                    f = os.path.join(spd, sub.replace('/', os.sep))
                if not os.path.isfile(f):
                    self.send_response(404); self.end_headers(); return
                b = open(f, 'rb').read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', str(len(b)))
                self.send_header('X-Sha', hashlib.sha1(b).hexdigest())
                self.end_headers(); self.wfile.write(b); return
            return super().do_GET()

    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


JS_HELP = r"""
window.__h={
 vis:e=>{if(!e)return false;const cs=getComputedStyle(e);const r=e.getBoundingClientRect();return cs.display!=='none'&&cs.visibility!=='hidden'&&r.height>0},
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 row:u=>DATA.find(x=>x[F.CODE]===u),
 show:async u=>{const r=__h.row(u);if(!r)return false;
   try{FL.q=u;FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';if(CUR.KINDS)FL.types=new Set(['G','T','E']);else FL.past=isC(r)?'p':'';draw()}catch(e){}
   await new Promise(res=>setTimeout(res,250));return true},
 open:async u=>{const r=__h.row(u);if(!r)return false;try{await openView(r[F.NO])}catch(e){}await new Promise(res=>setTimeout(res,700));return true},
 card:()=>{const c=document.getElementById('card');const ch=[...c.querySelectorAll('.choices button')].map(b=>__h.tx(b).replace(/^[①②③④⑤⑥⑦⑧]\s*/,'').replace(/✎$/,'').trim());
   const bg={},be={},bv={};c.querySelectorAll('.bogi .row').forEach(el=>{const k=el.dataset.k;const t=el.querySelector('.t');if(!t)return;
     const cl=t.cloneNode(true);cl.querySelectorAll('.tfx,.bexp').forEach(x=>x.remove());bg[k]=__h.tx(cl);
     const e=t.querySelector('.bexp');be[k]=e?__h.tx(e):null;bv[k]=e?__h.vis(e):null});
   return {ch,bg,be,bv}},
 prev:u=>{const it=[...document.querySelectorAll('#list .item')].find(x=>x.dataset.uid===u||__h.tx(x.querySelector('.num'))===u);return it?__h.tx(it.querySelector('.prev')):null},
 sumRect:()=>{const s=document.querySelector('#cDet>summary');if(!s)return null;s.scrollIntoView({block:'center'});const r=s.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]},
 hiddenButVisible:()=>[...document.querySelectorAll('[hidden]')].filter(e=>__h.vis(e)).map(e=>(e.id?'#'+e.id:'')+'.'+String(e.className||'').split(' ').join('.')+' '+__h.tx(e).slice(0,30))
};
"""


def launch(pw, app_text, qjson, subj, tag):
    srv, port = serve(app_text, qjson, subj, tag)
    br = pw.chromium.launch()
    ctx = br.new_context(viewport={'width': 1440, 'height': 950})
    ctx.add_init_script(INIT.replace('__SUBJ__', subj))
    pg = ctx.new_page()
    pg.goto('http://127.0.0.1:%d/app.html' % port, wait_until='load')
    pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=90000)
    pg.wait_for_timeout(2500)
    pg.evaluate(JS_HELP)
    return srv, br, pg


def click_summary(pg):
    """정답·해설 펼치기 — 앱과 같은 길: 요약줄이 보이면 그것을 · 교재 모드(body[data-book] · 요약줄 숨김)면 선택지 하나를 진짜 포인터로 누른다
       (앱이 자동 O/X 를 찍으며 #cDet 를 연다 · 5576) · 선택지가 없으면 앱과 같은 값(#cDet.open=true)"""
    xy = pg.evaluate(r"""()=>{const s=document.querySelector('#cDet>summary');
      if(s&&getComputedStyle(s).display!=='none'){s.scrollIntoView({block:'center'});const r=s.getBoundingClientRect();if(r.height>0)return ['s',r.left+r.width/2,r.top+r.height/2]}
      const b=document.querySelector('#card .choices button');if(b){b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return ['c',r.left+r.width/2,r.top+r.height/2]}
      return null}""")
    if xy:
        pg.mouse.click(xy[1], xy[2]); pg.wait_for_timeout(500)
    if not pg.evaluate("!!document.querySelector('#cDet')&&document.querySelector('#cDet').open"):
        pg.evaluate("()=>{const d=document.querySelector('#cDet');if(d)d.open=true}"); pg.wait_for_timeout(300)
    return bool(xy)


def close_answer(pg):
    pg.evaluate("()=>{const d=document.querySelector('#cDet');if(d)d.open=false}"); pg.wait_for_timeout(300)


def probe_rows(pg, uids):
    out = {}
    for u in uids:
        pg.evaluate('u=>__h.show(u)', u)
        prev = pg.evaluate('u=>__h.prev(u)', u)
        pg.evaluate('u=>__h.open(u)', u)
        closed = pg.evaluate('__h.card()')
        opened = None
        if pg.evaluate("!!document.querySelector('#cDet')&&!document.querySelector('#cDet').open"):
            click_summary(pg); opened = pg.evaluate('__h.card()')
            close_answer(pg)   # 다시 접기
        reclosed = pg.evaluate('__h.card()')
        out[u] = {'prev': prev, 'closed': closed, 'opened': opened, 'reclosed': reclosed,
                  'tf': pg.evaluate("u=>(typeof TFIX!=='undefined'&&TFIX[u])?Object.keys(TFIX[u]):[]", u)}
        pg.evaluate("()=>{try{closeView()}catch(e){}}"); pg.wait_for_timeout(150)
    return out


def old_bytes():
    """고치기 전 bio/문항.json — 로컬 파일이 그 판(md5 8f99c582)이면 그것 · 아니면 studyplandata git 에서 꺼낸다.
       인도 뒤에는 로컬이 새 판이라 옛 값 자리에 새 값이 들어가 H-3 헛잣대가 새 값끼리 맞댄다(9/25 인도 뒤 재실행에서 겪음 · 어긋남 0 → FAIL)"""
    b = open(QJ, 'rb').read()
    if hashlib.md5(b).hexdigest() == OLD_MD5:
        return b
    b = subprocess.run(['git', '-C', SPDROOT, 'show', OLD_REV + ':bio/문항.json'], capture_output=True).stdout
    if hashlib.md5(b).hexdigest() != OLD_MD5:
        raise SystemExit('NG  고치기 전 문항.json(md5 %s)을 못 찾았다 — studyplandata 를 fetch 해 보라' % OLD_MD5)
    return b


def main():
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    raw = old_bytes(); open(OLDQ, 'wb').write(raw)
    now = open(QJ, 'rb').read()   # studyplandata 로컬 지금 판(인도 뒤면 새 판)
    FX = json.load(open(FIX, encoding='utf-8'))
    LS = json.load(open(LISTS, encoding='utf-8')) if os.path.exists(LISTS) else {}
    # ── H-5 적용 스크립트 — 사본에 두 번(멱등) · 왕복 무변 ──
    shutil.copy(OLDQ, NEWQ)
    env = dict(os.environ, PYTHONIOENCODING='utf-8', OCRFIX_QJ=NEWQ, OCRFIX_TABLE=FIX)
    r1 = subprocess.run([sys.executable, os.path.join(HERE, '_ocrfix_bio.py'), 'write'], capture_output=True, env=env).stdout.decode('utf-8', 'replace')
    b1 = open(NEWQ, 'rb').read()
    r2 = subprocess.run([sys.executable, os.path.join(HERE, '_ocrfix_bio.py'), 'write'], capture_output=True, env=env).stdout.decode('utf-8', 'replace')
    b2 = open(NEWQ, 'rb').read()
    T('H-4 적용 두 번 = 같은 결과(멱등) · 왕복 무변 · 검산 OK', b1 == b2 and 'OK  json 왕복 무변' in r1 and '검산 OK' in r1 and '바뀐 칸 0' in r2,
      {'1회': [x for x in r1.splitlines() if '칸' in x or 'md5' in x][:3], '2회': [x for x in r2.splitlines() if '칸' in x][:2]})
    T('H-4b 옛 판에 입힌 결과 = studyplandata 로컬 지금 bio/문항.json(인도 뒤면 같아야 · 인도 전이면 로컬 = 옛 판)', b1 == now or now == raw,
      {'옛': hashlib.md5(raw).hexdigest(), '입힌 결과': hashlib.md5(b1).hexdigest(), '로컬 지금': hashlib.md5(now).hexdigest()})
    D0 = json.loads(raw.decode('utf-8')); D1 = json.loads(b1.decode('utf-8'))
    by0 = {r['uid']: r for r in D0}; by1 = {r['uid']: r for r in D1}
    # ── H-1 census ──
    cen = lambda P: subprocess.run([sys.executable, os.path.join(HERE, '_ocrfix', 'ocr_census_bio.py'), P], capture_output=True,
                                   env=dict(os.environ, PYTHONIOENCODING='utf-8')).stdout.decode('utf-8', 'replace').splitlines()
    N('H-1 대상 census — 고치기 전', cen(QJ)[:3])
    N('H-1 대상 census — 고친 뒤(남은 것 · 까닭은 수행 결과)', cen(NEWQ)[:3])
    T('H-1 고침표 uid 는 모두 문항.json 안 · 참고 상자 수', all(u in by0 for u in FX), {'고침표': len(FX), '참고 행': sum(1 for r in D1 if '참고' in r),
                                                                    '참고 상자': sum(len(r['참고']) for r in D1 if '참고' in r)})
    # ── H-2 D-1 · D-2 · D-3 ──
    mr = subprocess.run([sys.executable, os.path.join(HERE, '_ocrfix', 'ocr_check_bio.py'), NEWQ], capture_output=True,
                        env=dict(os.environ, PYTHONIOENCODING='utf-8')).stdout.decode('utf-8', 'replace')
    try:
        CK = json.loads(mr.strip().splitlines()[-1])
    except Exception:
        CK = {'err': mr[-400:]}
    sus = sorted(x['uid'] for x in LS.get('정오_의심', []))
    bad1 = sorted(x[0] for x in CK.get('d1_bad') or [])
    T('H-2 D-1 정오 대조 — 정답 선택지가 조합형이고 정오가 다 찬 %s 문항 · 어긋남 = 정오 의심 목록 그대로' % CK.get('d1_n'),
      CK.get('d1_n', 0) > 0 and bad1 == sus, {'n': CK.get('d1_n'), '어긋남': len(bad1), '목록 밖': sorted(set(bad1) - set(sus)), '목록에만': sorted(set(sus) - set(bad1))})
    sus2 = sorted('%s %s' % (x['uid'], x['키']) for x in LS.get('첫머리_의심', []))
    bad2 = sorted('%s %s' % (x[0], x[1]) for x in CK.get('d2_bad') or [])
    T('H-2 D-2 설명 첫머리 O·/X· = 그 키 정오 — 어긋남 = 첫머리 의심 목록 그대로', bad2 == sus2, {'어긋남': len(bad2), '목록 밖': sorted(set(bad2) - set(sus2))[:10]})
    T('H-2 D-3 조합형 다섯 서로 다름 · 빈 선택지 = 원본 넷·그림 선택지뿐', not CK.get('d3_dup') and sorted(CK.get('d3_empty') or []) == sorted(LS.get('빈칸_원본', [])),
      {'dup': CK.get('d3_dup'), 'empty 목록 밖': sorted(set(CK.get('d3_empty') or []) - set(LS.get('빈칸_원본', [])))[:10]})
    # ── 앱 ──
    new_app = io.open(SRC, encoding='utf-8', newline='').read()
    head_app = subprocess.run(['git', '-C', GENIE, 'show', 'HEAD:jagwa/index.html'], capture_output=True).stdout.decode('utf-8')
    rnd = random.Random(20260925)
    withexp = sorted(u for u in FX if any(b.get('설명') for b in (by1[u].get('보기') or [])) and u not in FIXED)
    pool = sorted(u for u in FX if u not in FIXED)
    uids = FIXED + rnd.sample(pool, min(20, len(pool)))
    kset = ['G57-05'] + rnd.sample(withexp, min(20, len(withexp)))
    with sync_playwright() as pw:
        srv, br, pg = launch(pw, new_app, NEWQ, 'bio', 'new')
        A = probe_rows(pg, sorted(set(uids) | set(kset)))
        # R — G57-05 참고 칸
        pg.evaluate("u=>__h.show(u)", 'G57-05'); pg.evaluate("u=>__h.open(u)", 'G57-05')
        pg.screenshot(path=os.path.join(SHOTS, 'K_G57-05_닫힘.png'))
        click_summary(pg); pg.wait_for_timeout(1500)
        R = pg.evaluate(r"""()=>{const c=document.getElementById('card');const rb=[...c.querySelectorAll('.ocrref')];
          const tabs=[...c.querySelectorAll('.soltabs button')].map(b=>__h.tx(b));
          const syn=[...c.querySelectorAll('.soltx')].map(x=>__h.tx(x));
          const img=c.querySelector('.ocrref img');
          return {n:rb.length,vis:rb.map(__h.vis),head:rb.map(x=>__h.tx(x.querySelector('.rfh'))),
            lines:rb.map(x=>(x.querySelector('.rft')||{innerHTML:''}).innerHTML.split('<br>').length),
            last:rb.map(x=>{const h=(x.querySelector('.rft')||{innerHTML:''}).innerHTML.split('<br>');return h[h.length-1]}),
            img:img?[img.complete,img.naturalWidth]:null,tabs,syn}}""")
        pg.screenshot(path=os.path.join(SHOTS, 'K_G57-05_펼침.png'))
        bt = pg.evaluate(r"""()=>{const b=[...document.querySelectorAll('#card .soltabs button')].find(x=>/크리티컬/.test(x.textContent));
          if(!b)return null;b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}""")
        if bt:
            pg.mouse.click(bt[0], bt[1]); pg.wait_for_timeout(300)
        R2 = pg.evaluate("()=>[...document.querySelectorAll('#card .ocrref')].map(__h.vis)")
        # 그림 누르면 크게
        im = pg.evaluate(r"""()=>{const i=document.querySelector('#card .ocrref img');if(!i)return null;i.scrollIntoView({block:'center'});const r=i.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}""")
        zoom = None
        if im:
            pg.mouse.click(im[0], im[1]); pg.wait_for_timeout(300)
            zoom = pg.evaluate("()=>{const z=document.getElementById('ocrrfz');return z?__h.vis(z):false}")
            pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        # 📋 정리 창 줄 펼침
        J = pg.evaluate(r"""async()=>{try{closeView()}catch(e){}const r=__h.row('G57-05');const sec=(unitOf(r[F.NO])||'1.1').split('.').slice(0,2).join('.');
          jnOpen(sec);await new Promise(x=>setTimeout(x,900));const jr=[...document.querySelectorAll('#jnw .jnrow')].find(x=>+x.dataset.no===r[F.NO]);
          if(!jr)return {row:false};const b=jr.querySelector('[data-jnans]');b.scrollIntoView({block:'center'});const q=b.getBoundingClientRect();
          return {row:true,xy:[q.left+q.width/2,q.top+q.height/2]}}""")
        if J.get('xy'):
            pg.mouse.click(J['xy'][0], J['xy'][1]); pg.wait_for_timeout(1200)
        J2 = pg.evaluate(r"""()=>{const r=__h.row('G57-05');const jr=[...document.querySelectorAll('#jnw .jnrow')].find(x=>+x.dataset.no===r[F.NO]);
          if(!jr)return null;const rb=jr.querySelectorAll('.jnansb .ocrref');const img=jr.querySelector('.jnansb .ocrref img');
          return {n:rb.length,vis:[...rb].map(__h.vis),img:img?[img.complete,img.naturalWidth]:null}}""")
        pg.evaluate("()=>{const w=document.getElementById('jnw');if(w)w.remove()}")
        # K — 새는 숨김 전수(첫 화면 · 문항 닫힘 · 펼침 · 정리 창 · 교재 창)
        leak = {}
        pg.evaluate("()=>{try{closeView()}catch(e){}}"); pg.wait_for_timeout(200); leak['첫 화면'] = pg.evaluate('__h.hiddenButVisible()')
        pg.evaluate("u=>__h.open(u)", 'G57-05'); leak['문항 닫힘'] = pg.evaluate('__h.hiddenButVisible()')
        click_summary(pg); leak['문항 펼침'] = pg.evaluate('__h.hiddenButVisible()')
        pg.evaluate("async()=>{try{closeView()}catch(e){}const r=__h.row('G57-05');jnOpen((unitOf(r[F.NO])||'1.1').split('.').slice(0,2).join('.'));await new Promise(x=>setTimeout(x,900))}")
        leak['정리 창'] = pg.evaluate('__h.hiddenButVisible()')
        pg.evaluate("async()=>{const w=document.getElementById('jnw');if(w)w.remove();try{await bookOpen(11,true)}catch(e){}await new Promise(x=>setTimeout(x,2500))}")
        leak['교재 창'] = pg.evaluate('__h.hiddenButVisible()')
        errN = pg.evaluate('(window.__err||[]).slice(0,8)')
        nb = pg.evaluate('DATA.length')
        br.close(); srv.shutdown()
        # 헛잣대 · DOM = HEAD(참고 없는 문항)
        srv, br, pg = launch(pw, head_app, NEWQ, 'bio', 'head')
        B = probe_rows(pg, ['G57-05'] + [u for u in kset if u != 'G57-05'][:5])
        pg.evaluate("u=>__h.show(u)", 'G57-05'); pg.evaluate("u=>__h.open(u)", 'G57-05'); click_summary(pg); pg.wait_for_timeout(800)
        RH = pg.evaluate("()=>document.querySelectorAll('#card .ocrref').length")
        noref = [u for u in pool if '참고' not in by1[u]][:3]
        domH = {}
        for u in noref:
            pg.evaluate("u=>__h.show(u)", u); pg.evaluate("u=>__h.open(u)", u)
            domH[u] = pg.evaluate("()=>document.getElementById('card').innerHTML.replace(/blob:[^\"']+/g,'blob:')")
            pg.evaluate("()=>{try{closeView()}catch(e){}}")
        br.close(); srv.shutdown()
        srv, br, pg = launch(pw, new_app, NEWQ, 'bio', 'new2')
        domN = {}
        for u in noref:
            pg.evaluate("u=>__h.show(u)", u); pg.evaluate("u=>__h.open(u)", u)
            domN[u] = pg.evaluate("()=>document.getElementById('card').innerHTML.replace(/blob:[^\"']+/g,'blob:')")
            pg.evaluate("()=>{try{closeView()}catch(e){}}")
        br.close(); srv.shutdown()
        # 옛 데이터(헛잣대 — 고친 칸이 어긋나야)
        srv, br, pg = launch(pw, new_app, OLDQ, 'bio', 'old')
        O = probe_rows(pg, uids)
        br.close(); srv.shutdown()
        # 지학·물리 = HEAD(문항 창 · 첫 화면 DOM 글자)
        other = {}
        for subj in ('earth', 'phys'):
            got = []
            for app in (head_app, new_app):
                srv, br, pg = launch(pw, app, None, subj, subj + ('h' if app is head_app else 'n'))
                t = pg.evaluate(r"""async()=>{const L=document.getElementById('list');const a=L?String(L.textContent||'').replace(/\d+'\d{2}"/g,'').replace(/\s+/g,' ').slice(0,4000):'';
                  let c='';try{await openView(DATA[0][F.NO]);await new Promise(x=>setTimeout(x,900));const k=document.getElementById('card')||document.getElementById('view');c=k?String(k.textContent||'').replace(/\s+/g,' ').slice(0,3000):''}catch(e){c='(err '+e+')'}
                  return a+' ||| '+c}""")
                got.append(t); br.close(); srv.shutdown()
            other[subj] = got
    # ── 판정 ──
    good, bad = 0, []
    for u in uids:
        r = by1[u]; a = A.get(u) or {}; tf = set(a.get('tf') or [])
        cl = a.get('closed') or {}; op = a.get('opened') or cl
        want_ch = []   # 앱 expandChoices 와 같게 — 칸 안의 ⑥⑦⑧ 로 가르고 끝 빈칸을 뗀다
        for c in (r.get('선택지') or []):
            parts = [x.strip() for x in re.split(r'\s*[⑥⑦⑧]\s*', str(c or ''))]
            want_ch += parts[:1] + [x for x in parts[1:] if x]
        while want_ch and not want_ch[-1]:
            want_ch.pop()
        got_ch = cl.get('ch') or []
        ok_ch = (not any(want_ch)) and not got_ch or [c for i, c in enumerate(got_ch) if 'c%d' % (i + 1) not in tf] == [c for i, c in enumerate(want_ch) if 'c%d' % (i + 1) not in tf]
        wb = {b['키']: b.get('내용') for b in (r.get('보기') or []) if b.get('내용') and 'b' + b['키'] not in tf}
        ok_bg = all((cl.get('bg') or {}).get(k) == v for k, v in wb.items())
        we = {b['키']: b.get('설명') for b in (r.get('보기') or []) if b.get('설명')}
        ok_be = all(((op.get('be') or {}).get(k) or '').replace(' ', '') == v.replace(' ', '') for k, v in we.items())
        stem = str(r['문항']).split(' ⏎ ')[0]
        ok_pv = 'q' in tf or (a.get('prev') is not None and stem[:20].replace(' ', '') in (a.get('prev') or '').replace(' ', ''))
        if ok_ch and ok_bg and ok_be and ok_pv:
            good += 1
        else:
            bad.append({'u': u, 'ch': None if ok_ch else [got_ch, want_ch], 'bg': None if ok_bg else [cl.get('bg'), wb], 'be': None if ok_be else [op.get('be'), we], 'pv': None if ok_pv else [a.get('prev'), stem[:30]]})
    T('H-3 앱 — 표본 %d(무작위 20 + G57-05 · G44-01 · G49-01 · T001 · E021) 미리보기 · 선택지 · 〈보기〉 줄 · 〈보기〉 설명 = 새 값(손값 없는 칸)' % len(uids), not bad and nb == len(D1),
      {'good': good, 'bad': bad[:3], 'n': nb})
    g57 = ((A.get('G57-05') or {}).get('opened') or {}).get('be') or {}
    T('H-3 G57-05 ㄷ 설명 = 「X · 생장에 필수적인 유전자들은 … 생장에 필수적인 것은 아니다.」 에서 끝', str(g57.get('ㄷ') or '').startswith('X · 생장에 필수적인 유전자들은') and str(g57.get('ㄷ') or '').endswith('생장에 필수적인 것은 아니다.'), g57.get('ㄷ'))
    base_bad = sum(1 for u in uids if (O.get(u) or {}).get('closed') != (A.get(u) or {}).get('closed'))
    T('H-3 헛잣대 — 옛 문항.json 으로는 표본 대부분이 어긋난다', base_bad >= len(uids) // 2, {'어긋남': base_bad, '표본': len(uids)})
    T('H-3 페이지 오류 0', not errN, errN)
    # R
    T('R-1 G57-05 펼침 — 참고 칸 1 · 보임 · 제목 「📎 참고 · pBR322(1977년 제작) 플라스미드」',
      R.get('n') == 1 and all(R.get('vis') or [False]) and (R.get('head') or [''])[0] == '📎 참고 · pBR322(1977년 제작) 플라스미드', R)
    T('R-2 점 5 줄 · 마지막 「…세포내 도입과 DNA의 조작이 쉽다.」', (R.get('lines') or [0])[0] == 5 and str((R.get('last') or [''])[0]).endswith('세포내 도입과 DNA의 조작이 쉽다.'), [R.get('lines'), R.get('last')])
    T('R-3 SYNAPSE 탭 글이 「…필수적인 것은 아니다.」 에서 끝(상자 글 0)', any(s.endswith('필수적인 것은 아니다.') for s in (R.get('syn') or [])) and not any('pBR322' in s for s in (R.get('syn') or [])), [s[-60:] for s in (R.get('syn') or [])])
    T('R-4 참고 그림 1 로드됨 · 누르면 크게(#ocrrfz 보임)', bool(R.get('img')) and R['img'][0] and R['img'][1] > 0 and zoom is True, [R.get('img'), zoom])
    T('R-5 크리티컬 탭으로 바꿔도 참고 칸 보임(탭 밖)', bool(bt) and R2 == [True], [bt, R2])
    T('R-6 📋 정리 창 「정답·해설 ▸」 펼침에도 참고 칸 · 그림', bool(J2) and J2.get('n') == 1 and J2.get('vis') == [True] and bool(J2.get('img')) and J2['img'][1] > 0, J2)
    T('R-7 참고 없는 문항 문항 창 DOM = HEAD(같은 새 데이터)', bool(noref) and all(domH[u] == domN[u] for u in noref), {u: domH[u] == domN[u] for u in noref})
    T('R-0 헛잣대 — HEAD 앱에서 참고 칸 0', RH == 0, RH)
    # K
    kc = [(u, (A.get(u) or {}).get('closed') or {}) for u in kset]
    closed_vis = [(u, sum(1 for v in (c.get('bv') or {}).values() if v)) for u, c in kc]
    open_ok = [(u, sum(1 for v in (((A.get(u) or {}).get('opened') or {}).get('bv') or {}).values() if v), sum(1 for v in (c.get('be') or {}).values() if v)) for u, c in kc]
    recl = [(u, sum(1 for v in (((A.get(u) or {}).get('reclosed') or {}).get('bv') or {}).values() if v)) for u in kset]
    T('K-2 G57-05 + 무작위 설명 문항 20: 닫힘 보임 0', all(n == 0 for _, n in closed_vis), [x for x in closed_vis if x[1]][:5])
    T('K-2 펼침 보임 = 설명 수', all(a == b for _, a, b in open_ok), [x for x in open_ok if x[1] != x[2]][:5])
    T('K-2 다시 접기 0 · 다른 문항으로 넘어가도 0(문항마다 새로 열 때 닫힘)', all(n == 0 for _, n in recl), [x for x in recl if x[1]][:5])
    bh = (B.get('G57-05') or {}).get('closed') or {}
    T('K-1 헛잣대 — HEAD 앱에서 G57-05 닫힘인데 설명 보임 3/3(FAIL 이어야 할 옛 동작)', sum(1 for v in (bh.get('bv') or {}).values() if v) == 3, bh.get('bv'))
    T('K-3 새는 숨김 전수 — [hidden] 인데 화면 기준 보이는 요소 0(첫 화면 · 문항 닫힘·펼침 · 정리 창 · 교재 창)', all(not v for v in leak.values()), leak)
    T('K-4 지학·물리 첫 화면·문항 창 DOM 글자 = HEAD', all(v[0] == v[1] for v in other.values()), {k: [v[0][:80], v[1][:80]] if v[0] != v[1] else '같음' for k, v in other.items()})
    N('K-5 스크린샷(사람 눈 확인 · 게이트 아님)', [os.path.join(SHOTS, 'K_G57-05_닫힘.png'), os.path.join(SHOTS, 'K_G57-05_펼침.png')])
    lines = ['# _harness_bio_ocrfix — %s' % time.strftime('%Y-%m-%d %H:%M'),
             '옛 문항.json md5 %s · 새(사본) md5 %s · 앱 genie 작업트리 jagwa/index.html md5(LF) %s' % (
                 hashlib.md5(raw).hexdigest(), hashlib.md5(b1).hexdigest(), hashlib.md5(open(SRC, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()), '']
    for s, n, d in RES:
        dd = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)
        lines.append('%s | %s | %s' % (s, n, dd[:900]))
    nf = sum(1 for x in RES if x[0] == 'FAIL')
    lines += ['', '합계  PASS %d · FAIL %d · NOTE %d  (%.0f초)' % (sum(1 for x in RES if x[0] == 'PASS'), nf, sum(1 for x in RES if x[0] == 'NOTE'), time.time() - t0)]
    txt = '\n'.join(lines) + '\n'
    f = os.path.join(HERE, '_harness_bio_ocrfix_result.txt')
    for _ in range(3):
        io.open(f, 'w', encoding='utf-8', newline='\n').write(txt); time.sleep(0.5)
        if io.open(f, encoding='utf-8').read() == txt:
            break
    print(lines[-1])
    return nf


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
