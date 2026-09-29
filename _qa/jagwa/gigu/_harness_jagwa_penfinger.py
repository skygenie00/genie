# -*- coding: utf-8 -*-
r"""_task_jagwa_penfinger §D 관문 — 자과앱(지학·생물) 문제 창: 손가락 굴림 · 손바닥 · 펜 필기 · 펜 누르기 · 펜/손가락/마우스 길게 누르기 · 물리 무변

  NEW  = --new <파일>(없으면 genie 작업트리 jagwa/index.html) · BASE = --base <파일>(없으면 genie 72a65b3 = bio ocrfix 인도 판 · md5(LF) b988c9c8)
  입력 = **진짜 포인터**(지시서 ★) — 손가락 = CDP Input.dispatchTouchEvent(radiusX·radiusY 22 = 아이패드 손가락 굵기 · 1 도 잰다)
         펜 = CDP Input.dispatchMouseEvent pointerType 'pen' · 마우스 = page.mouse — el.click()·합성 이벤트로 PASS 하지 않는다
  헛잣대 = 같은 시나리오를 BASE 에 먼저 — 고친 칸은 BASE 에서 FAIL 이어야 잣대다
  데이터 = studyplandata(earth · bio · phys) 로컬 사본을 같은 출처로 — GitHub 요청은 로컬로 돌리고 바깥 網은 막는다
  표본 = 생물 G57-05 · 지학 G48-03(채팅 실측과 같음) · 정답·해설 펼침

쓰기 : python _harness_jagwa_penfinger.py [--new 파일] [--base 파일] [--only earth,bio,phys]   결과 = _harness_jagwa_penfinger_result.txt
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import hashlib, http.server, io, json, os, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


HERE = os.path.dirname(os.path.abspath(__file__))
GENIE = _roots.genie()
SPDROOT = _roots.spd()
NEWF = ARG('--new', os.path.join(GENIE, 'jagwa', 'index.html'))
BASEF = ARG('--base', '')
BASE_REV, BASE_MD5 = '72a65b3', 'b988c9c81546eaf1bcc3e250f4a2db92'
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
WORK = os.path.join(tempfile.gettempdir(), 'h_penfinger'); os.makedirs(WORK, exist_ok=True)
SAMPLE = {'bio': 'B20-57-05', 'earth': 'G11-48-03'}   # ★ jagwa_uid(9/29) — 옛 G57-05 · G48-03(문항 번호 새 꼴)
RES = []


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, d[:300]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('NOTE | %s · %s | %s' % (grp, name, d[:300]), flush=True)


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

JS = r"""
window.__P={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 row:u=>DATA.find(x=>x[F.CODE]===u),
 async open(u){const r=__P.row(u);if(!r)return false;
   try{FL.q=u;FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';if(CUR.KINDS)FL.types=new Set(['G','T','E']);else FL.past=isC(r)?'p':'';draw()}catch(e){}
   await new Promise(res=>setTimeout(res,250));try{await openView(r[F.NO])}catch(e){}await new Promise(res=>setTimeout(res,900));return !!document.getElementById('card')},
 async ans(){const d=document.getElementById('cDet');if(d&&!d.open){d.open=true;await new Promise(res=>setTimeout(res,400))}return !!(d&&d.open)},
 tool(m){try{if(m==='pen')setTool('pen','#16181B',document.querySelector('[data-pen="#16181B"]'));else setTool('view')}catch(e){return 'ERR '+e}
   return {mode:TOOL.mode,penon:document.getElementById('card').classList.contains('penon')}},
 st(){const w=document.getElementById('cardwrap'),c=document.getElementById('card');const sh=document.getElementById('tfxSheet');
   return {top:w?Math.round(w.scrollTop):null,sh:w?w.scrollHeight:null,ch:w?w.clientHeight:null,strokes:(QINK&&QINK.s||[]).length,
     sheet:sh?__P.tx(sh.querySelector('h2')):null,pick:[...c.querySelectorAll('.choices button.pick')].map(b=>+b.dataset.c),
     ox:[...c.querySelectorAll('.bogi .row .ox button.on')].map(b=>b.closest('.row').dataset.k+b.dataset.v),
     vox:[...c.querySelectorAll('.vox.on')].map(b=>b.dataset.vmark),det:!!(document.getElementById('cDet')||{}).open,
     gg:__P.tx(c.querySelector('.ggwrap')).length,mode:TOOL.mode}},
 top(v){const w=document.getElementById('cardwrap');w.scrollTop=v;return Math.round(w.scrollTop)},
 closeSheet(){const s=document.getElementById('tfxSheet');if(s)s.remove();return 1},
 /* 표적 자리 — 그 요소를 창 가운데로 굴린 뒤 안쪽 한 점(fx·fy) · 그 점의 맨 위 요소(덮개면 svg/path)와 덮개를 걷었을 때 밑 요소 */
 at(sel,fx,fy){const c=document.getElementById('card');const e=typeof sel==='string'?c.querySelector(sel):sel;if(!e)return null;
   const w=document.getElementById('cardwrap');e.scrollIntoView({block:'center'});
   const r=e.getBoundingClientRect(),x=Math.round(r.left+Math.min(r.width-4,Math.max(4,r.width*(fx==null?.3:fx)))),y=Math.round(r.top+Math.min(r.height-3,Math.max(3,r.height*(fy==null?.5:fy))));
   const top=document.elementFromPoint(x,y);const ink=c.querySelector('#qink');let under=null;
   if(ink){const k=ink.style.pointerEvents;ink.style.pointerEvents='none';under=document.elementFromPoint(x,y);ink.style.pointerEvents=k}
   const nm=q=>q?(q.id?'#'+q.id:'')+(q.tagName||'').toLowerCase()+'.'+String(q.className&&q.className.baseVal!=null?q.className.baseVal:q.className||'').split(' ').join('.'):null;
   return {x,y,top:nm(top),under:nm(under),inEl:!!under&&(under===e||e.contains(under)),w:Math.round(r.width),h:Math.round(r.height),scroll:Math.round(w.scrollTop)}},
 strokeAt(){const p=[...document.querySelectorAll('#qink path[data-j]')].pop();if(!p)return null;const b=p.getBoundingClientRect();return {x:Math.round(b.left+b.width/2),y:Math.round(b.top+b.height/2)}},
 wrapMid(){const w=document.getElementById('cardwrap').getBoundingClientRect();return {x:Math.round(w.left+w.width*.5),y:Math.round(w.top+w.height*.62)}},
 physDom(){const v=document.getElementById('view');return v?__P.tx(v).replace(/\d+'\d{2}"/g,'').slice(0,4000):''},
 sheets(){return document.querySelectorAll('#tfxSheet').length},
 errs(){return (window.__err||[]).slice(0,10)}
};
"""


def serve(app_text, subj, tag):
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
                f = os.path.join(spd, rel[len(subj) + 1:].replace('/', os.sep))
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
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


class P:
    """한 판(BASE·NEW) · 한 과목 — 1180×700(아이패드 가로 · 사파리 막대 뺀 높이쯤 — 지학 G48-03 카드가 820 창에선 76px 밖에 안 굴렀다) · 터치 켬"""
    def __init__(self, br, app, subj, tag):
        self.srv, port = serve(app, subj, tag)
        self.ctx = br.new_context(viewport={'width': 1180, 'height': 700}, device_scale_factor=1, has_touch=True)
        OKNET = ('http://127.0.0.1', 'https://cdnjs.cloudflare.com/', 'https://cdn.jsdelivr.net/', 'https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')
        self.ctx.route('**/*', lambda rt: rt.continue_() if rt.request.url.startswith(OKNET) else rt.abort())   # 앱 머리 pdf.js·pdf-lib·KaTeX(CDN)만 연다 · 그 밖 網은 막는다
        self.ctx.add_init_script(INIT.replace('__SUBJ__', subj))
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(120000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:200]))
        self.pg.goto('http://127.0.0.1:%d/app.html' % port, wait_until='load')
        self.pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=90000)
        self.pg.wait_for_timeout(2500)
        self.pg.evaluate(JS)
        self.cdp = self.ctx.new_cdp_session(self.pg)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def wait(self, ms):
        self.pg.wait_for_timeout(ms)

    # ── 손가락(CDP 진짜 터치 · 반지름) ──
    def _t(self, ty, pts, r):
        self.cdp.send('Input.dispatchTouchEvent', {'type': ty, 'touchPoints': [{'x': x, 'y': y, 'radiusX': r, 'radiusY': r, 'id': 1} for (x, y) in pts]})

    def fdrag(self, x, y, dx, dy, r=22, n=12):
        self._t('touchStart', [(x, y)], r)
        for i in range(1, n + 1):
            self._t('touchMove', [(x + dx * i / n, y + dy * i / n)], r); self.wait(16)
        for _ in range(3):   # 끝에서 멈춘 뒤 뗀다(움직이며 떼면 크롬이 다음 톡을 삼킨다)
            self._t('touchMove', [(x + dx, y + dy)], r); self.wait(30)
        self._t('touchEnd', [], r); self.wait(250)

    def fhold(self, x, y, ms, r=22):
        self._t('touchStart', [(x, y)], r); self.wait(ms)
        self._t('touchEnd', [], r); self.wait(300)

    # ── 펜(CDP 마우스 이벤트 pointerType pen) ──
    def _p(self, ty, x, y, btn='left', buttons=1):
        self.cdp.send('Input.dispatchMouseEvent', {'type': ty, 'x': x, 'y': y, 'button': btn, 'buttons': buttons, 'clickCount': 1 if ty != 'mouseMoved' else 0,
                                                   'pointerType': 'pen', 'force': 0.5})

    def pdrag(self, x0, y0, x1, y1, n=12):
        self._p('mouseMoved', x0, y0, 'none', 0); self._p('mousePressed', x0, y0)
        for i in range(1, n + 1):
            self._p('mouseMoved', x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n); self.wait(16)
        self._p('mouseReleased', x1, y1, 'left', 0); self.wait(350)

    def phold(self, x, y, ms):
        self._p('mouseMoved', x, y, 'none', 0); self._p('mousePressed', x, y)
        for k in range(int(ms / 50)):   # 2px 안에서 떨린다(사람 손)
            self._p('mouseMoved', x + (1 if k % 2 else 0), y + (1 if k % 3 == 0 else 0)); self.wait(50)
        self._p('mouseReleased', x, y, 'left', 0); self.wait(400)

    def ptap(self, x, y):
        self._p('mouseMoved', x, y, 'none', 0); self._p('mousePressed', x, y); self.wait(40)
        self._p('mouseReleased', x, y, 'left', 0); self.wait(450)

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass
        try:
            self.srv.shutdown()
        except Exception:
            pass


def scen(br, app, tag, subj, keep):
    g = '%s %s' % (tag, subj)
    u = SAMPLE[subj]
    p = P(br, app, subj, tag + subj)

    def fresh(tool='view'):
        p.ev("()=>__P.closeSheet()")
        ok = p.ev("u=>__P.open(u)", u); p.ev("()=>__P.ans()"); p.ev("m=>__P.tool(m)", tool); p.wait(250)
        # ★ 9/28 penfinger_add2 — 앞 관문의 마우스가 카드 글자 위에 남아 있으면, 도구를 펜으로 바꾼 뒤(덮개가 덮음) 크롬이 늦게 보내는
        #   마우스 hover 갱신(pointerleave)이 다음 손가락 길게 누르기 도중에 떨어져 tfixLong 시계를 끈다(tfixLong 은 어느 포인터의 leave 에도 끈다) —
        #   손가락 관문 앞에 마우스를 카드 밖 구석으로 치워 hover 를 매듭짓는다(마우스 관문은 제가 다시 옮긴다)
        p.pg.mouse.move(1, 1); p.wait(120)
        return ok

    try:
        ok = fresh()
        s0 = p.ev("()=>__P.st()")
        T(g, '0 %s 문제 창 · 정답·해설 펼침 · 창보다 150px 넘게 길다(굴림 잣대가 설 만큼)' % u, ok and s0['det'] and s0['sh'] > s0['ch'] + 150, s0)
        # ── 1 손가락 굴림 · 반지름 22 · 1 · 보기 도구 · 펜 도구 ──
        got = {}
        for tool in ('view', 'pen'):
            fresh(tool)
            for r in (22, 1):
                p.ev("v=>__P.top(v)", 0); m = p.ev("()=>__P.wrapMid()")
                p.fdrag(m['x'], m['y'], 0, -225, r)
                t = p.ev("()=>__P.st()"); got['%s r%d' % (tool, r)] = t['top']
                if t['sheet']:
                    got['창 %s r%d' % (tool, r)] = t['sheet']; p.ev("()=>__P.closeSheet()")
        T(g, '1 손가락 위로 225px(반지름 22 · 아이패드 손가락) → 굴림 ≥ 150 — 보기·펜 도구 둘 다(헛잣대: 바탕 0)', got['view r22'] >= 150 and got['pen r22'] >= 150, got)
        T(g, '1b 반지름 1 도 같다(≥ 150)', got['view r1'] >= 150 and got['pen r1'] >= 150, got)
        T(g, '1c 손가락으로 끄는 동안 글자 고치기 창이 안 뜬다(길게 누르기 시계는 움직이면 꺼진다)', not any(k.startswith('창') for k in got), got)
        # ── 2 손바닥(ⓑ 그대로) ──
        fresh('pen')
        q = p.ev("()=>__P.at('.q',.3,.5)")
        n0 = p.ev("()=>__P.st()")['strokes']
        p.pdrag(q['x'], q['y'], q['x'] + 60, q['y'] + 2)
        p.ev("v=>__P.top(v)", 40); m = p.ev("()=>__P.wrapMid()")
        p.fdrag(m['x'], m['y'], 0, -120, 22)
        a = p.ev("()=>__P.st()")['top']
        p.wait(1500); p.ev("v=>__P.top(v)", 40)
        p.fdrag(m['x'], m['y'], 0, -120, 22)
        b = p.ev("()=>__P.st()")['top']
        T(g, '2 펜 뗀 뒤 0.5초 안 손가락(반지름 22) → 굴림 0 · 1.5초 뒤 → 굴림(헛잣대: 바탕은 뒤도 0)', a == 40 and b > 40 + 60, {'0.5초 안': a, '1.5초 뒤': b, '획': n0})
        # ── 3 펜 필기 — 문제 글 · 〈보기〉 줄 글 · 〈보기〉 설명 ──
        fresh('pen')
        tg = [('문제 글', '.q', .25, .5), ('〈보기〉 ㄱ 줄 글', '.bogi .row .t', .15, .3)]
        if subj == 'bio':
            tg.append(('〈보기〉 ㄱ 설명', '.bogi .row .bexp', .2, .5))
        res3 = {}
        for nm, sel, fx, fy in tg:
            a = p.ev("([s,x,y])=>__P.at(s,x,y)", [sel, fx, fy])
            if not a:
                res3[nm] = '표적 없음'; continue
            s1 = p.ev("()=>__P.st()")
            p.pdrag(a['x'], a['y'], a['x'] + 60, a['y'] + 1)
            s2 = p.ev("()=>__P.st()")
            res3[nm] = {'획': [s1['strokes'], s2['strokes']], '굴림': [s1['top'], s2['top']], '밑': a['under'], '안': a['inEl']}
        ok3 = all(isinstance(v, dict) and v['안'] and v['획'][1] == v['획'][0] + 1 and v['굴림'][0] == v['굴림'][1] for v in res3.values())
        T(g, '3 펜 60px 긋기 → 획 +1씩 · 그동안 굴림 무변 — %s(헛잣대: 바탕 획 0)' % ' · '.join(res3), ok3, res3)
        keep.setdefault('stroke_on_q', {})[tag + subj] = res3.get('문제 글')
        # ── 4 펜 누르기 무변 — 선택지 · 〈보기〉 O/X(덮개 밑) · O/△/X 표시(근거 층) · 「정답·해설 ▸」 · 근거 ＋ ──
        fresh('pen')
        r4 = {}
        s = p.ev("()=>__P.st()")
        a = p.ev("()=>__P.at('.choices button[data-c=\"2\"]',.5,.5)")
        if a:
            p.ptap(a['x'], a['y']); t = p.ev("()=>__P.st()"); r4['선택지 ②'] = {'pick': t['pick'], '획': t['strokes'] - s['strokes'], '밑': a['under']}
        a = p.ev("()=>__P.at('.bogi .row .ox button[data-v=\"O\"]',.5,.5)")
        if a:
            s = p.ev("()=>__P.st()"); p.ptap(a['x'], a['y']); t = p.ev("()=>__P.st()"); r4['〈보기〉 O'] = {'ox': t['ox'], '획': t['strokes'] - s['strokes']}
        a = p.ev("()=>__P.at('.vox[data-vmark=\"Q\"]',.5,.5)")
        if a:
            s = p.ev("()=>__P.st()"); p.ptap(a['x'], a['y']); t = p.ev("()=>__P.st()"); r4['표시 △'] = {'vox': t['vox'], '획': t['strokes'] - s['strokes'], '위': a['top']}
        a = p.ev("()=>__P.at('#cDetBtn',.5,.5)")
        if a:
            s = p.ev("()=>__P.st()"); p.ptap(a['x'], a['y']); t = p.ev("()=>__P.st()"); r4['정답·해설 ▸'] = {'det': [s['det'], t['det']], '획': t['strokes'] - s['strokes']}
        a = p.ev("()=>__P.at('.ggwrap button[title=\"병렬 근거 줄 더하기\"]',.5,.5)")
        if a:
            s = p.ev("()=>__P.st()"); p.ptap(a['x'], a['y']); p.wait(300); t = p.ev("()=>__P.st()"); r4['근거 ＋'] = {'gg': [s['gg'], t['gg']], '획': t['strokes'] - s['strokes']}
        keep.setdefault('press', {})[tag + subj] = r4
        ok4 = all(v.get('획') == 0 for v in r4.values()) and r4.get('선택지 ②', {}).get('pick') == [2] and r4.get('정답·해설 ▸', {}).get('det') == [True, False] \
            and bool(r4.get('〈보기〉 O', {}).get('ox')) and 'Q' in (r4.get('표시 △', {}).get('vox') or [])
        T(g, '4 펜 톡 → 선택지 고름 · 〈보기〉 O 표시 · △ 표시 · 「정답·해설 ▸」 접힘 · 근거 ＋(바탕과 맞대기는 끝에) · 넷 다 획 0', ok4, r4)
        # ── 5 펜 길게 누르기 → 글자 고치기 · 획 무증가 · 이미 그은 획 위에서도 ──
        fresh('pen')
        r5 = {}
        for nm, sel, fx, want in (('문제 글', '.q', .25, '✎ 글자 고치기 — 문제'), ('〈보기〉 ㄱ', '.bogi .row .t', .12, '✎ 글자 고치기 — 〈보기〉 ㄱ')):
            a = p.ev("([s,x])=>__P.at(s,x,.4)", [sel, fx])
            if not a:
                r5[nm] = '표적 없음'; continue
            s = p.ev("()=>__P.st()"); p.phold(a['x'], a['y'], 750); t = p.ev("()=>__P.st()")
            r5[nm] = {'sheet': t['sheet'], 'want': want, '획': t['strokes'] - s['strokes']}
            p.ev("()=>__P.closeSheet()"); p.wait(150)
        # 이미 그은 획 위
        a = p.ev("()=>__P.at('.q',.55,.5)")
        s = p.ev("()=>__P.st()"); p.pdrag(a['x'], a['y'], a['x'] + 70, a['y']); t = p.ev("()=>__P.st()")
        sp = p.ev("()=>__P.strokeAt()")
        if t['strokes'] == s['strokes'] + 1 and sp:
            s2 = p.ev("()=>__P.st()"); p.phold(sp['x'], sp['y'], 750); t2 = p.ev("()=>__P.st()")
            r5['획 위'] = {'sheet': t2['sheet'], 'want': '✎ 글자 고치기 — 문제', '획': t2['strokes'] - s2['strokes']}
            p.ev("()=>__P.closeSheet()")
        else:
            # 바탕은 글자 위에 획이 안 그어져(3번) 그을 수 있는 빈 곳에 긋고 그 위에서 잰다 — 글자 위 획이 없으니 「획 위」 는 못 잰다
            r5['획 위'] = {'sheet': None, 'want': '✎ 글자 고치기 — 문제', '획': None, '까닭': '글자 위에 획을 못 그었다(바탕의 3번 증상)'}
        ok5 = all(isinstance(v, dict) and v.get('sheet') == v.get('want') and v.get('획') == 0 for v in r5.values())
        T(g, '5 펜 750ms(2px 안) → 「✎ 글자 고치기 — 문제 / 〈보기〉 ㄱ」 · 획 무증가 · 이미 그은 획 위에서도(헛잣대: 바탕은 획 위에서 안 열림)', ok5, r5)
        # ── 5b 펜 길게 누르기(창) 뒤에도 손가락 굴림 — 펜을 창 위에서 떼 penDown 이 안 풀리던 것 ──
        fresh('pen')   # 그 앞 펜 동작이 상자 안에서 떼며 penDown 을 풀어 두지 않게 — 펜 길게 누르기 하나만 하고 곧바로 잰다
        a = p.ev("()=>__P.at('.q',.25,.4)")
        p.phold(a['x'], a['y'], 750); sh5 = p.ev("()=>__P.st()")['sheet']
        p.ev("()=>__P.closeSheet()"); p.wait(1500)
        p.ev("v=>__P.top(v)", 0); m = p.ev("()=>__P.wrapMid()"); p.fdrag(m['x'] - 150, m['y'], 0, -225, 1)
        t5 = p.ev("()=>__P.st()")
        T(g, '5b 펜 길게 누르기로 창을 연 뒤 1.5초 — 손가락(반지름 1) 굴림 ≥ 150(헛잣대: 바탕 0 — 펜을 창 위에서 떼 penDown 이 참으로 남았다)', sh5 == '✎ 글자 고치기 — 문제' and t5['top'] >= 150, {'펜 길게 창': sh5, 'top': t5['top'], 'sheet': t5['sheet']})
        p.ev("()=>__P.closeSheet()")
        # ── 6 손가락·마우스 길게 누르기 → 글자 고치기 ──
        r6 = {}
        for tool in ('view', 'pen'):
            fresh(tool)
            a = p.ev("()=>__P.at('.q',.3,.5)")
            p.fhold(a['x'], a['y'], 800, 22); r6['손가락 ' + tool] = p.ev("()=>__P.st()")['sheet']; p.ev("()=>__P.closeSheet()")
        fresh('view')
        a = p.ev("()=>__P.at('.q',.3,.5)")
        p.pg.mouse.move(a['x'], a['y']); p.pg.mouse.down(); p.wait(800); p.pg.mouse.up(); p.wait(300)
        r6['마우스'] = p.ev("()=>__P.st()")['sheet']; p.ev("()=>__P.closeSheet()")
        keep.setdefault('mouse', {})[tag + subj] = r6['마우스']
        W6 = '✎ 글자 고치기 — 문제'
        T(g, '6 손가락(반지름 22 · 800ms) 문제 글 길게 → 「%s」 — 보기·펜 도구 둘 다 · 마우스도(헛잣대: 바탕은 손가락으로 안 열림 — 가드가 capture 에서 막았다)' % W6,
          r6.get('손가락 view') == W6 and r6.get('손가락 pen') == W6 and r6.get('마우스') == W6, r6)
        # 6b 선택지 단추(눌리는 것) 길게 — 창은 하나(가드 시계와 단추 제 tfixLong 이 겹치지 않는다) · 고르지 않는다
        fresh('view')
        a = p.ev("()=>__P.at('.choices button[data-c=\"4\"]',.5,.5)")
        s6 = p.ev("()=>__P.st()")
        p.fhold(a['x'], a['y'], 800, 22)
        n6, t6 = p.ev("()=>__P.sheets()"), p.ev("()=>__P.st()")
        p.ev("()=>__P.closeSheet()")
        T(g, '6b 선택지 ④ 손가락 길게 → 글자 고치기 창 1(겹침 없음) · ④ 는 안 골라진다', n6 == 1 and 4 not in (t6['pick'] or []) and t6['sheet'] == '✎ 글자 고치기 — 보기 ④',
          {'창': n6, 'sheet': t6['sheet'], 'pick': [s6['pick'], t6['pick']]})
        # 6c 손바닥 — 펜을 뗀 뒤 0.5초 안에 글자 위에 얹은 손가락(= 손바닥)은 길게 눌러도 안 연다
        fresh('pen')
        a = p.ev("()=>__P.at('.q',.3,.5)")
        b = p.ev("()=>__P.wrapMid()")
        p.pdrag(b['x'] - 200, b['y'] + 60, b['x'] - 140, b['y'] + 62)
        p.fhold(a['x'], a['y'], 800, 22)
        t6 = p.ev("()=>__P.st()"); p.ev("()=>__P.closeSheet()")
        T(g, '6c 펜 뗀 뒤 0.5초 안 글자 위 손가락(손바닥) 800ms → 창 안 뜸', not t6['sheet'], t6['sheet'])
        er = p.errs + (p.ev("()=>__P.errs()") or [])
        T(g, 'Z 페이지 오류 0', not er, er[:5])
    except Exception as ex:
        T(g, '묶음 예외', False, repr(ex)[:400])
    finally:
        p.close()


def scen_phys(br, app, tag, keep):
    g = '%s phys' % tag
    p = P(br, app, 'phys', tag + 'phys')
    try:
        no = p.ev("()=>DATA.find(r=>r[F.FILE]&&r[F.FILE]!=='IMG'||true)[F.NO]")
        p.ev("n=>openView(n)", no); p.wait(1500)
        dom = p.ev("()=>__P.physDom()")
        st = p.ev("()=>{const s=document.getElementById('stage');if(!s)return null;const r=s.getBoundingClientRect();return {x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height*.6),top:s.scrollTop,sh:s.scrollHeight,ch:s.clientHeight}}")
        mv = None
        if st:
            p.fdrag(st['x'], st['y'], 0, -200, 22)
            mv = p.ev("()=>{const s=document.getElementById('stage');return s?[s.scrollTop,s.scrollLeft]:null}")
        keep.setdefault('phys', {})[tag] = {'dom': hashlib.md5(dom.encode('utf-8')).hexdigest() + ':%d' % len(dom), 'stage': st, 'move': mv}
        N(g, '7 물리 문제 창 DOM · #stage 손가락(반지름 22) 끌기(바탕과 맞대기는 끝에)', keep['phys'][tag])
        er = p.errs + (p.ev("()=>__P.errs()") or [])
        T(g, 'Z 페이지 오류 0', not er, er[:5])
    except Exception as ex:
        T(g, '묶음 예외', False, repr(ex)[:400])
    finally:
        p.close()


def report(t0, newmd5, bmd5):
    lines = ['# _harness_jagwa_penfinger — %s' % time.strftime('%Y-%m-%d %H:%M'),
             'NEW = %s (md5(LF) %s) · BASE = %s (md5(LF) %s) · 데이터 = studyplandata 로컬' % (NEWF, newmd5, BASEF or BASE_REV, bmd5),
             '입력 = CDP 터치(반지름 22·1) · CDP 펜(pointerType pen) · page.mouse — 합성 이벤트·el.click 없음', '']
    for grp, name, ok, d in RES:
        dd = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)
        lines.append('%s | %s · %s | %s' % ('NOTE' if ok is None else 'PASS' if ok else 'FAIL', grp, name, dd[:700]))
    new = [x for x in RES if x[2] is not None and not x[0].startswith('BASE')]
    base = [x for x in RES if x[2] is not None and x[0].startswith('BASE')]
    np_, nf = sum(1 for x in new if x[2]), sum(1 for x in new if not x[2])
    bp, bf = sum(1 for x in base if x[2]), sum(1 for x in base if not x[2])
    lines += ['', '헛잣대(BASE) — PASS %d · FAIL %d (고친 칸 잣대는 FAIL 이어야 잣대 — 반지름 1 굴림·페이지 오류 같은 무변 잣대는 PASS)' % (bp, bf),
              '합계(NEW)  PASS %d · FAIL %d  (%.0f초)' % (np_, nf, time.time() - t0)]
    txt = '\n'.join(lines) + '\n'
    f = os.path.join(HERE, '_harness_jagwa_penfinger_result.txt')
    for _ in range(3):
        io.open(f, 'w', encoding='utf-8', newline='\n').write(txt); time.sleep(0.5)
        if io.open(f, encoding='utf-8').read() == txt:
            break
    print('\n'.join(lines[-3:]))
    return nf


def main():
    t0 = time.time()
    new = io.open(NEWF, encoding='utf-8', newline='').read()
    newmd5 = hashlib.md5(new.replace('\r\n', '\n').encode('utf-8')).hexdigest()
    base = io.open(BASEF, encoding='utf-8', newline='').read() if BASEF else subprocess.run(['git', '-C', GENIE, 'show', BASE_REV + ':jagwa/index.html'], capture_output=True).stdout.decode('utf-8')
    bmd5 = hashlib.md5(base.replace('\r\n', '\n').encode('utf-8')).hexdigest()
    T('땅값', 'BASE = bio ocrfix 인도 판(72a65b3 · b988c9c8)', bmd5 == BASE_MD5, bmd5)
    run = lambda x: not ONLY or x in ONLY
    keep = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for subj in ('bio', 'earth'):
            if run(subj):
                scen(br, base, 'BASE', subj, keep)
                scen(br, new, 'NEW', subj, keep)
        if run('phys'):
            scen_phys(br, base, 'BASE', keep)
            scen_phys(br, new, 'NEW', keep)
        br.close()
    for subj in ('bio', 'earth'):
        a, b = (keep.get('press') or {}).get('BASE' + subj), (keep.get('press') or {}).get('NEW' + subj)
        if a is not None and b is not None:
            ga, gb = (a.get('근거 ＋') or {}).get('gg'), (b.get('근거 ＋') or {}).get('gg')
            T('NEW ' + subj, '4b 펜 근거 ＋ = 바탕과 같은 결과 · 선택지·O/X·△·정답·해설 누름도 바탕과 같음',
              ga == gb and {k: {kk: vv for kk, vv in v.items() if kk not in ('밑', '위')} for k, v in a.items()} == {k: {kk: vv for kk, vv in v.items() if kk not in ('밑', '위')} for k, v in b.items()},
              {'BASE': a, 'NEW': b})
        la, lb = (keep.get('mouse') or {}).get('BASE' + subj), (keep.get('mouse') or {}).get('NEW' + subj)
        if la is not None and lb is not None:
            T('NEW ' + subj, '6m 마우스 길게 누르기 = 바탕 그대로(무변)', la == lb, {'BASE': la, 'NEW': lb})
    ph = keep.get('phys') or {}
    if 'BASE' in ph and 'NEW' in ph:
        T('NEW phys', '7 물리 문제 창 DOM · #stage 손가락 끌기 = 바탕', ph['BASE'] == ph['NEW'], ph)
    return report(t0, newmd5, bmd5)


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
