# -*- coding: utf-8 -*-
"""자과앱 아이패드 터치 — `_task_jagwa_shell_bio_phys_add18` §B·§C 묶음 「TP」.

  왜 따로인가 — `_harness_earth_shell.py` 는 **크롬 CDP 하나**로만 잰다.
  아이패드 고장(ⓐ 서랍이 열리면 문제가 저절로 뜸 ⓑ 너비를 끌면 팝업 ⓒ 창이 안 닫힘)은
  **WebKit(사파리 엔진)의 유령 click** 이 원인이라는 짐작이라, 마우스 크롬으로는 하나도 못 잡는다.
  ⇒ playwright 로 **Chromium 터치 + WebKit 터치** 둘 다에서, **진짜 터치**(신뢰 이벤트)로 잰다.

  NEW  = genie 작업트리 jagwa/index.html
  BASE = `68216cf`(add9 까지 든 판 · md5(LF) 773962ce…) — 헛잣대
  실데이터 = studyplandata earth/ · phys 는 파일 안 DATA

쓰기 : python _harness_jagwa_touch_ipad.py            (넷 다)
       python _harness_jagwa_touch_ipad.py chromium   (한 엔진만)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기 헬퍼(_task_qa_slim2 A-1-2 · 옛 남 하네스 import 를 갈음)
import hashlib
import http.server
import importlib.util
import io
import json
import os
import socketserver
import subprocess
import sys
import threading
import urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
GENIE = _roots.genie()
SPDROOT = _roots.spd()
SRC = os.path.join(GENIE, 'jagwa', 'index.html')
BASE_MD5 = '773962ce59842d75d44d32ef3db34c16'      # 68216cf

# 부모 하네스의 `STUB`(과목 고르기·오류 모으기)을 그대로 쓴다 — 두 벌로 갈리지 않게
STUB = JG.STUB_ES

INIT = r"""
(()=>{
  try{localStorage.setItem('subj','__SUBJ__')}catch(e){}
  try{localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}))}catch(e){}
  ['jagwa.earth.coll','jagwa.view.win','jagwa.win.view','jagwa.win.mc','jagwa.win.jn',
   'jagwa.nd.fold.earth','jagwa.nd.fold.phys','jagwa.nd.w.earth','jagwa.nd.w.phys']
    .forEach(k=>{try{localStorage.removeItem(k)}catch(e){}});
  window.__err=[];
  window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+(e.lineno||''))});
  window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
  const nf=window.fetch.bind(window);
  window.fetch=async function(url,opt){
    opt=opt||{};const u=String(url);
    const m=/api\.github\.com\/repos\/([^\/]+\/[^\/]+)\/contents\/([^?]+)/.exec(u);
    if(!m){ if(/^https?:/i.test(u)&&u.indexOf(location.origin)!==0)
              return {ok:false,status:599,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
            return nf(url,opt) }
    const path=decodeURIComponent(m[2]);
    if((opt.method||'GET')==='PUT')return {ok:true,status:200,json:async()=>({content:{sha:'x'}}),text:async()=>''};
    const r=await nf('/data/'+encodeURI(path),{cache:'no-store'});
    if(!r.ok)return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
    const acc=(opt.headers||{}).Accept||'';
    if(acc.indexOf('raw')>=0)return r;
    return {ok:true,status:200,json:async()=>({sha:'sha'}),text:async()=>JSON.stringify({sha:'sha'})};
  };
})();
"""


def serve(subj, html, outdir):
    os.makedirs(outdir, exist_ok=True)
    io.open(os.path.join(outdir, 'app.html'), 'w', encoding='utf-8', newline='').write(html)
    spd = os.path.join(SPDROOT, subj)

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=outdir, **k)

        def log_message(self, *a, **k):
            pass

        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            if p.startswith('/data/'):
                rel, pre = p[6:], subj + '/'
                f = os.path.join(spd, rel[len(pre):].replace('/', os.sep)) if rel.startswith(pre) else ''
                if not f or not os.path.isfile(f):
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


def build(subj, src):
    html = src.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js',
                       STUB.replace('__SUBJ__', subj) + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    return html


# ── qa_slim2(2026-10-08) regress 도우미 — 이름이 `_rg` · `_RG` 로 시작 = gate 에서 안 쓰는 갈래
_RG_SYNCED = "()=>typeof recBusy!=='undefined'&&!recBusy&&(((lsObj(SMETA_KEY).lastSync||0)>=performance.timeOrigin)||!!recErr)"   # 표지 = 앱 recBoot() 첫 syncRecords 끝(recBusy 거짓 · 이 쪽 열린 뒤 맞춘 시각 또는 recErr) · INIT 이 토큰을 넣어 부팅마다 맞춤
_QF_DATA = "()=>typeof CARD_LAYER==='undefined'||!CARD_LAYER||typeof DATA_V==='undefined'||DATA_V>0"   # _task_qa_fix1 §A-3(10/9) — 카드 층(지학·생물) 문항.json 다 읽음(buildData 끝 · DATA_V) · 물리 · 옛 판(DATA_V 없음)은 바로 참 · gate · regress 둘 다
_RG_VIEW = "()=>{const v=document.getElementById('view');return !!v&&!v.classList.contains('hide')}"   # 표지 = 문항 창(#view) 열림
_RG_SMOKE = ('두 판 다 부팅했다', '★1 접힌 손잡이', 'JS 오류 0(새 판)')   # smoke 칸 글(A-0 smoke 칸 · 두판부팅 · ★1 · JS)


BOX = """(sel)=>{const e=document.querySelector(sel);if(!e)return null;
  const r=e.getBoundingClientRect();return {x:r.left,y:r.top,w:r.width,h:r.height,
  cx:r.left+r.width/2,cy:r.top+r.height/2}}"""


def probe(engine, tag, subj, src, out):
    """한 엔진·한 판에서 §B 를 잰다. 돌려주는 것 = 잰 값 사전."""
    from playwright.sync_api import sync_playwright
    R = {'engine': engine, 'tag': tag, 'subj': subj}
    QC.launch('base' if tag == 'BASE' else 'new')   # 셈(§B-4)
    srv, port = serve(subj, build(subj, src), os.path.join(out, tag + '_' + engine + '_' + subj))
    url = 'http://127.0.0.1:%d/app.html' % port
    with sync_playwright() as pw:
        br = getattr(pw, engine).launch()
        ctx = br.new_context(viewport={'width': 1024, 'height': 1180}, device_scale_factor=2,
                             is_mobile=True, has_touch=True,
                             user_agent='Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 '
                                        '(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
        ctx.add_init_script(INIT.replace('__SUBJ__', subj))
        pg = ctx.new_page()
        pg.goto(url, wait_until='load')
        try:
            pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>100', timeout=60000)
        except Exception as e:
            R['boot'] = 'NG ' + str(e)[:120]; br.close(); srv.shutdown(); return R
        QC.until(pg, _QF_DATA, 30000, 'touch_ipad 과목 문항 다 읽음(카드 층 DATA_V > 0 · _task_qa_fix1 §A-3 · 10/8 웹킷 지학 「r[F.CODE]」 거부 둘 = 문항을 다 읽기 전에 누름)')
        if QC.GATE:
            pg.wait_for_timeout(2500)
        else:   # regress — 고정 2.5 초 대신 표지(첫 기록 맞춤 끝) · 상한 = 같은 2.5 초
            # 옛 줄: QC.until(pg, _RG_SYNCED, 2500, 'touch_ipad 부팅 뒤 첫 syncRecords 끝(recBusy 거짓 · lastSync ≥ 쪽 열림 또는 recErr)')
            QC.until(pg, _RG_SYNCED, 15000, 'touch_ipad 부팅 뒤 첫 syncRecords 끝(recBusy 거짓 · lastSync ≥ 쪽 열림 또는 recErr) · _task_qa_fix1 §A-3 상한 15 초(부하에서 늦는 첫 동기화를 끝까지 · 표지가 오면 바로)')
        R['n'] = pg.evaluate('DATA.length')
        R['shell'] = pg.evaluate('typeof SHELL!=="undefined"&&SHELL')
        R['res'] = pg.evaluate('!!document.querySelector("#navdr.ndres")')
        R['boot'] = 'ok'
        R['err0'] = pg.evaluate('(window.__err||[]).slice(0,4)')
        tap = lambda b: pg.touchscreen.tap(b['cx'], b['cy'])

        # ── TP-1 접힌 손잡이 톡 → 서랍만 펴짐 · 문제 안 뜸 ──────────────
        try:
            pg.evaluate('ndResFold(true)'); pg.wait_for_timeout(500)
            R['t1_fold0'] = pg.evaluate('document.querySelector("#navdr").classList.contains("fold")')
            g = pg.evaluate(BOX, '#ndGrip')
            R['t1_grip'] = g
            if g:
                tap(g); pg.wait_for_timeout(1600)
                R['t1_fold1'] = pg.evaluate('document.querySelector("#navdr").classList.contains("fold")')
                R['t1_view'] = pg.evaluate('!document.getElementById("view").classList.contains("hide")')
                g2 = pg.evaluate(BOX, '#ndGrip')
                tap(g2); pg.wait_for_timeout(1600)
                R['t1_fold2'] = pg.evaluate('document.querySelector("#navdr").classList.contains("fold")')
                R['t1_view2'] = pg.evaluate('!document.getElementById("view").classList.contains("hide")')
            pg.evaluate('ndResFold(false)'); pg.wait_for_timeout(400)
        except Exception as e:
            R['t1_exc'] = str(e)[:160]
        if QC.SMOKE:   # smoke — 부팅 · ★1 · JS 오류 까지
            R['err'] = pg.evaluate('(window.__err||[]).slice(0,6)')
            br.close(); srv.shutdown(); return R

        # ── TP-2 손잡이를 끌어 너비를 바꾸고 줄 위에서 뗀다 → 문제 안 뜸 ──
        for who, sel in (('서랍 줄', '#ndList .ndrow'), ('첫 화면 목록 줄', '#list .item')):
            try:
                pg.evaluate('ndSetW(236)'); pg.wait_for_timeout(400)
                g = pg.evaluate(BOX, '#ndGrip'); t = pg.evaluate(BOX, sel)
                if not g or not t:
                    R['t2_' + who] = 'no-target'; continue
                ok = drag_touch(pg, engine, g['cx'], g['cy'], 380, t['cy'])
                pg.wait_for_timeout(1600)
                R['t2_' + who] = {'던짐': ok,
                                  'w': pg.evaluate('parseInt(getComputedStyle(document.documentElement).getPropertyValue("--ndw"))||0'),
                                  'view': pg.evaluate('!document.getElementById("view").classList.contains("hide")')}
                pg.evaluate('try{closeView()}catch(e){}'); pg.wait_for_timeout(300)
            except Exception as e:
                R['t2_' + who] = 'exc ' + str(e)[:140]

        # ── TP-3 서랍 줄 톡 → 그 문항이 열린다 · 쓸어내리다 뗌 → 안 열린다 ──
        try:
            pg.evaluate('try{closeView()}catch(e){}'); pg.wait_for_timeout(400)
            b = pg.evaluate(BOX, '#ndList .ndrow:nth-child(3)') or pg.evaluate(BOX, '#ndList .ndrow')
            want = pg.evaluate('(()=>{const e=document.querySelector("#ndList .ndrow:nth-child(3)")||document.querySelector("#ndList .ndrow");return e?+e.dataset.no:0})()')
            if b:
                tap(b)
                if QC.GATE:
                    pg.wait_for_timeout(1800)
                else:   # regress — 고정 1.8 초 대신 표지(문항 창 열림 · 상한 = 같은 1.8 초 · 안 열리면 gate 와 같은 시간 뒤 FAIL)
                    QC.until(pg, _RG_VIEW, 1800, 'touch_ipad TP-3 서랍 줄 톡 → 문항 창 열림')
                R['t3_open'] = pg.evaluate('!document.getElementById("view").classList.contains("hide")')
                R['t3_no'] = [pg.evaluate('typeof VNO!=="undefined"?VNO:null'), want]
            pg.evaluate('try{closeView()}catch(e){}'); pg.wait_for_timeout(400)
            b2 = pg.evaluate(BOX, '#ndList .ndrow')
            if b2:
                ok = drag_touch(pg, engine, b2['cx'], b2['cy'], b2['cx'], b2['cy'] - 180)
                pg.wait_for_timeout(1400)
                R['t3_scroll'] = {'던짐': ok,
                                  'view': pg.evaluate('!document.getElementById("view").classList.contains("hide")')}
            pg.evaluate('try{closeView()}catch(e){}'); pg.wait_for_timeout(300)
        except Exception as e:
            R['t3_exc'] = str(e)[:160]

        # ── TP-4 한 문항짜리 목록으로 열어도 서랍은 전체 ────────────────
        try:
            pg.evaluate('(()=>{const n=DATA[3][F.NO];return openView(n,[n])})()'); pg.wait_for_timeout(2000)
            R['t4'] = pg.evaluate("""(()=>({
              rows:document.querySelectorAll('#ndList .ndrow').length,
              secs:document.querySelectorAll('#ndList .ndsec').length,
              items:document.querySelectorAll('#list .item').length,
              vlist:(typeof VLIST!=='undefined'&&VLIST)?VLIST.length:-1,
              head:(document.getElementById('ndHead')||{}).textContent||''}))()""")
        except Exception as e:
            R['t4'] = 'exc ' + str(e)[:140]

        # ── TP-5 창이 톡으로 닫힌다 ────────────────────────────────────
        try:
            R['t5_backTag'] = pg.evaluate('(()=>{const b=document.getElementById("vBack");return b?b.tagName:"없음"})()')
            b = pg.evaluate(BOX, '#vBack')
            if b:
                # ★ 2026-10-07 (_task_jagwa_phys_win §B E5 · 점검표 13) — 펼친 서랍 머리가 #vBack(✕)을 가림 → 누를 자리 요소를 남기고 서랍(#navdr)이 가릴 때만 #ndGrip 톡으로 접고 다시 잰 자리를 톡(옛 판은 안 가려 옛 길 그대로)
                R['t5_at'] = pg.evaluate("""(p)=>{const a=document.elementFromPoint(p.cx,p.cy);const v=document.getElementById('vBack');
                  return a?{tag:a.tagName,id:a.id||'',cls:String(a.className||'').slice(0,30),self:!!v&&(a===v||v.contains(a)),dr:!!(a.closest&&a.closest('#navdr'))}:null}""", b)
                if R['t5_at'] and not R['t5_at'].get('self') and R['t5_at'].get('dr'):
                    g = pg.evaluate(BOX, '#ndGrip')
                    if g:
                        tap(g); pg.wait_for_timeout(700)
                        b = pg.evaluate(BOX, '#vBack') or b
                    R['t5_fold'] = bool(g)
                tap(b); pg.wait_for_timeout(1400)
                R['t5_closed'] = pg.evaluate('document.getElementById("view").classList.contains("hide")')
            # 📋 창(jnOpen) · 🃏 창 — ✕/닫기 를 톡
            R['t5_sheets'] = []
            for fn, close in (('jnOpen', '#jnwX'), ('mcwOpen', '.mcw .mcx, #mcw .mcx, #mcw button')):
                made = pg.evaluate("""(f)=>{try{const sec=Object.keys(TOC.sec)[0];
                  const r=window[f]&&window[f](sec);return !!document.querySelector('#jnw,.mcw,#mcw,.sheet')}catch(e){return 'exc '+e}}""", fn)
                pg.wait_for_timeout(1200)
                cb = pg.evaluate(BOX, close)
                if cb:
                    tap(cb); pg.wait_for_timeout(900)
                R['t5_sheets'].append([fn, made, bool(cb),
                                       pg.evaluate("document.querySelectorAll('#jnw,.mcw,#mcw').length")])
                pg.evaluate("document.querySelectorAll('#jnw,.mcw,#mcw,.sheet').forEach(x=>x.remove())")
            # 머리 빈 자리를 끌면 창이 옮겨진다
            pg.evaluate('try{localStorage.setItem("jagwa.view.win","1")}catch(e){}')
            pg.evaluate('(()=>openView(DATA[1][F.NO]))()'); pg.wait_for_timeout(2200)
            before = pg.evaluate(BOX, '#view')
            ttl = pg.evaluate(BOX, '#view .vtop .title')
            if before and ttl:
                drag_touch(pg, engine, ttl['cx'], ttl['cy'], ttl['cx'] + 60, ttl['cy'] + 40)
                pg.wait_for_timeout(700)
                after = pg.evaluate(BOX, '#view')
                R['t5_move'] = [round(before['x']), round(after['x']), round(before['y']), round(after['y'])]
            pg.evaluate('try{closeView()}catch(e){}'); pg.wait_for_timeout(300)
        except Exception as e:
            R['t5_exc'] = str(e)[:160]

        # ── TP-6 (물리) 분류 칩 셋 · 「기본」 집합 = SRC!=='변리사' ───────
        if subj == 'phys':
            try:
                pg.evaluate("FL.past='';FL.bigs=[];FL.subs=[];FL.unit='';FL.round='';FL.mark='';FL.q='';draw()")
                pg.wait_for_timeout(1200)
                R['t6_chips'] = pg.evaluate(
                    "[...document.querySelectorAll('#eKind .chchip')].map(b=>b.textContent.replace(/\\s+/g,' ').trim())")
                R['t6_tag'] = pg.evaluate(
                    "[...document.querySelectorAll('#list .meta .tag,#eKind .chchip,#specHd,#trTog')]"
                    ".filter(e=>/타기출/.test(e.textContent)).length")
                R['t6_tagWhere'] = pg.evaluate(
                    "[...document.querySelectorAll('*')].filter(e=>e.children.length===0&&/타기출/.test(e.textContent))"
                    ".slice(0,4).map(e=>(e.tagName+'.'+(e.className||'')).slice(0,40))")
                R['t6_basic'] = pg.evaluate("""(()=>{
                  const b=[...document.querySelectorAll('#eKind .chchip')].find(x=>/기본/.test(x.textContent));
                  if(!b)return null; b.click(); return 1})()""")
                pg.wait_for_timeout(1400)
                R['t6_set'] = pg.evaluate("""(()=>{
                  const got=[...document.querySelectorAll('#list .item .num')].map(e=>e.textContent.trim()).sort();
                  const want=DATA.filter(r=>r[F.SRC]!=='변리사').map(r=>codeShow(r)).sort();
                  return {got:got.length,want:want.length,same:got.join('|')===want.join('|'),
                          spec:document.querySelectorAll('#spec i').length}})()""")
                R['t6_tag2'] = pg.evaluate(
                    "[...document.querySelectorAll('#list .meta .tag,#eKind .chchip,#specHd,#trTog')]"
                    ".filter(e=>/타기출/.test(e.textContent)).length")
            except Exception as e:
                R['t6_exc'] = str(e)[:160]

        R['err'] = pg.evaluate('(window.__err||[]).slice(0,6)')
        br.close()
    srv.shutdown()
    return R


def drag_touch(pg, engine, x0, y0, x1, y1):
    """터치 끌기. Chromium 은 CDP 로 **진짜** 터치를, WebKit 은 합성 pointer 로 던진다(도구 한계)."""
    if engine == 'chromium':
        try:
            cdp = pg.context.new_cdp_session(pg)
            def ev(t, x, y):
                cdp.send('Input.dispatchTouchEvent', {'type': t,
                         'touchPoints': ([] if t == 'touchEnd' else [{'x': x, 'y': y, 'id': 1}])})
            ev('touchStart', x0, y0)
            for i in range(1, 9):
                ev('touchMove', x0 + (x1 - x0) * i / 8.0, y0 + (y1 - y0) * i / 8.0)
            ev('touchEnd', x1, y1)
            return 'cdp'
        except Exception as e:
            return 'cdp-ng ' + str(e)[:60]
    try:
        pg.evaluate("""([x0,y0,x1,y1])=>{
          const at=(x,y)=>document.elementFromPoint(x,y)||document.body;
          const mk=(t,x,y)=>{const e=new PointerEvent(t,{bubbles:true,cancelable:true,composed:true,
            pointerId:1,pointerType:'touch',isPrimary:true,clientX:x,clientY:y,button:0,buttons:1});return e};
          const el=at(x0,y0);
          el.dispatchEvent(mk('pointerdown',x0,y0));
          for(let i=1;i<=8;i++){const x=x0+(x1-x0)*i/8,y=y0+(y1-y0)*i/8;
            el.dispatchEvent(mk('pointermove',x,y))}
          el.dispatchEvent(mk('pointerup',x1,y1));
          /* iOS 가 보내는 유령 click 을 흉내 낸다 — **뗀 자리에 그때 있는 요소**로 간다 */
          const tgt=at(x1,y1);
          tgt.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,composed:true,
            clientX:x1,clientY:y1,detail:1}));
        }""", [x0, y0, x1, y1])
        return 'synth+ghost'
    except Exception as e:
        return 'synth-ng ' + str(e)[:60]


def main():
    engines = [a for a in sys.argv[1:] if a in ('chromium', 'webkit')] or ['chromium', 'webkit']
    cur = io.open(SRC, encoding='utf-8', newline='').read()
    if QC.GATE:
        QC.sub('git:show-app')
        b = subprocess.run(['git', '-C', GENIE, 'show', '68216cf:jagwa/index.html'], capture_output=True).stdout
        if not b or hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest() != BASE_MD5:
            for rev in ('HEAD', 'HEAD~1', 'HEAD~2', 'HEAD~3'):
                b2 = subprocess.run(['git', '-C', GENIE, 'show', rev + ':jagwa/index.html'], capture_output=True).stdout
                if b2 and hashlib.md5(b2.replace(b'\r\n', b'\n')).hexdigest() == BASE_MD5:
                    b = b2; break
        assert b and hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest() == BASE_MD5, '바탕(773962ce)을 못 찾았다'
        base = b.decode('utf-8')
    else:   # regress · smoke — 바탕(68216cf) 앱 풀기 0 · BASE probe 0
        base = None
    out = os.path.join(os.environ.get('TEMP', '.'), 'h_touch_ipad')
    D = {}
    for eng in engines:
        for tag, src in ((('NEW', cur), ('BASE', base)) if QC.GATE else (('NEW', cur),)):   # regress — 바탕 probe(헛잣대 · 증상 재현 INFO) 안 돎
            for subj in (('earth', 'phys') if not QC.SMOKE else ('earth',)):   # smoke — 지학 하나
                k = '%s/%s/%s' % (eng, tag, subj)
                print('… %s' % k, flush=True)
                try:
                    D[k] = probe(eng, tag, subj, src, out)
                except Exception as e:
                    D[k] = {'exc': str(e)[:300]}
    json.dump(D, io.open(os.path.join(out, 'raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    L = []
    T = lambda n, c, i=None: L.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c or i is None else ' | ' + json.dumps(i, ensure_ascii=False)[:600]))
    I = lambda n, v: L.append('INFO | ' + n + ' | ' + json.dumps(v, ensure_ascii=False)[:900])
    g = lambda k: D.get(k) or {}

    for eng in engines:
        for subj in (('earth', 'phys') if not QC.SMOKE else ('earth',)):
            n, o = g('%s/NEW/%s' % (eng, subj)), g('%s/BASE/%s' % (eng, subj))
            pre = 'TP[%s·%s] ' % (eng, subj)
            if QC.GATE:
                T(pre + '두 판 다 부팅했다(문항 %s/%s · 상주 서랍 %s/%s)' % (n.get('n'), o.get('n'), n.get('res'), o.get('res')),
                  n.get('boot') == 'ok' and o.get('boot') == 'ok' and n.get('res') and o.get('res'),
                  [n.get('boot'), o.get('boot'), n.get('res'), o.get('res'), n.get('err0'), o.get('err0')])
            else:   # regress — 새 판 부팅 조건만(바탕 조건 = 관문만 몫) · 칸 글의 바탕 자리 「—」(새id · 처리표)
                T(pre + '두 판 다 부팅했다(문항 %s/— · 상주 서랍 %s/—)' % (n.get('n'), n.get('res')),
                  n.get('boot') == 'ok' and n.get('res'), [n.get('boot'), n.get('res'), n.get('err0')])
            # 1 손잡이 톡
            T(pre + '★1 접힌 손잡이를 톡 → 서랍만 펴지고 **문제가 안 뜬다** · 다시 톡 → 접힘',
              n.get('t1_fold0') is True and n.get('t1_fold1') is False and n.get('t1_view') is False
              and n.get('t1_fold2') is True and n.get('t1_view2') is False,
              {k: n.get(k) for k in ('t1_fold0', 't1_fold1', 't1_view', 't1_fold2', 't1_view2', 't1_exc')})
            if QC.GATE:   # 바탕 판 INFO(증상 재현 표) — 관문만
                I(pre + '1 바탕 판(같은 손짓)', {k: o.get(k) for k in ('t1_fold0', 't1_fold1', 't1_view', 't1_fold2', 't1_view2', 't1_exc')})
            # 2 너비 끌기
            for who in ('서랍 줄', '첫 화면 목록 줄'):
                v = n.get('t2_' + who) or {}
                T(pre + '★2 손잡이를 끌어 너비를 바꾸고 「%s」 위에서 떼도 **문제가 안 뜬다**(너비 %s)' % (who, v.get('w') if isinstance(v, dict) else '?'),
                  isinstance(v, dict) and v.get('view') is False and (v.get('w') or 0) > 300, v)
                if QC.GATE:
                    I(pre + '2 바탕 판 「%s」' % who, o.get('t2_' + who))
            # 3 줄 톡
            T(pre + '★3 서랍 줄을 톡 → 그 문항이 열린다(%s)' % (n.get('t3_no')),
              n.get('t3_open') is True and n.get('t3_no') and n['t3_no'][0] == n['t3_no'][1],
              [n.get('t3_open'), n.get('t3_no'), n.get('t3_exc')])
            v3 = n.get('t3_scroll') or {}
            T(pre + '★3 서랍을 쓸어 스크롤하다 떼면 **안 열린다**', isinstance(v3, dict) and v3.get('view') is False, v3)
            if QC.GATE:
                I(pre + '3 바탕 판 쓸기', o.get('t3_scroll'))
            # 4 서랍 = 첫 화면 전체
            a4, b4 = n.get('t4') or {}, o.get('t4') or {}
            T(pre + '★4 한 문항짜리 목록(VLIST %s)으로 열어도 서랍은 **전체**(줄 %s = 첫 화면 %s · 머리 %s)'
              % (a4.get('vlist'), a4.get('rows'), a4.get('items'), a4.get('secs')),
              a4.get('vlist') == 1 and a4.get('rows') == a4.get('items') and (a4.get('rows') or 0) > 50
              and (a4.get('secs') or 0) > 0, a4)
            if QC.GATE:
                I(pre + '4 바탕 판', b4)
            # 5 창 닫기
            T(pre + '★5 문제 창 「서재」를 톡 → 닫힌다(%s)' % n.get('t5_backTag'),
              n.get('t5_closed') is True, [n.get('t5_backTag'), n.get('t5_closed'), n.get('t5_exc')]
              + ([{'누를 자리': n.get('t5_at'), '서랍 접음(§B E5 — 펼친 서랍 머리가 ✕ 를 가림)': n.get('t5_fold')}] if n.get('t5_fold') is not None else []))   # ★ 2026-10-07 (_task_jagwa_phys_win §B E5 · 점검표 13) 접었으면 값에 남김
            T(pre + '★5 떠 있는 창의 ✕·「닫기」를 톡 → 닫힌다',
              all((isinstance(x, list) and x[3] == 0) for x in (n.get('t5_sheets') or [[None, None, None, 1]])),
              n.get('t5_sheets'))
            mv = n.get('t5_move')
            T(pre + '5 창 머리 빈 자리를 끌면 창이 옮겨진다(끌기는 그대로 산다)',
              isinstance(mv, list) and (abs(mv[1] - mv[0]) > 10 or abs(mv[3] - mv[2]) > 10), mv)
            if subj == 'phys':
                T(pre + '★6 분류 칩 = 셋 %s' % (n.get('t6_chips')),
                  isinstance(n.get('t6_chips'), list) and len(n['t6_chips']) == 3
                  and n['t6_chips'][0].startswith('전체') and n['t6_chips'][1].startswith('기출')
                  and n['t6_chips'][2].startswith('기본'), n.get('t6_chips'))
                s6 = n.get('t6_set') or {}
                T(pre + '★6 「기본」 목록 집합 = `SRC!==변리사` 집합(전수 %s/%s · 히트맵 %s)'
                  % (s6.get('got'), s6.get('want'), s6.get('spec')),
                  s6.get('same') is True and s6.get('got') == s6.get('want') == s6.get('spec'), s6)
                T(pre + '★6 딱지·칩에 「타기출」 0(전체 %s · 기본 %s · 남은 자리 %s)'
                  % (n.get('t6_tag'), n.get('t6_tag2'), n.get('t6_tagWhere')),
                  n.get('t6_tag') == 0 and n.get('t6_tag2') == 0,
                  [n.get('t6_tag'), n.get('t6_tag2'), n.get('t6_tagWhere')])
                if QC.GATE:   # 헛잣대 = 관문만(바탕 probe)
                    # 헛잣대 — 바탕 판은 칩 넷 · 「타기출」 글자 ≥1
                    T(pre + '★헛잣대 6 — 바탕 판은 칩이 **넷**이고 「타기출」 글자가 있다 %s' % (o.get('t6_chips')),
                      isinstance(o.get('t6_chips'), list) and len(o['t6_chips']) == 4 and (o.get('t6_tag') or 0) > 0,
                      [o.get('t6_chips'), o.get('t6_tag')])
            T(pre + 'JS 오류 0(새 판)', not n.get('err'), n.get('err'))

    # 재현 여부 — 있는 그대로
    rep = {}
    for eng in engines:
        for subj in ('earth', 'phys'):
            o = g('%s/BASE/%s' % (eng, subj))
            rep['%s/%s' % (eng, subj)] = {
                '1 손잡이 톡에 문제가 떴나': o.get('t1_view'),
                '2 너비 끌고 서랍 줄에서 떼니 떴나': (o.get('t2_서랍 줄') or {}).get('view') if isinstance(o.get('t2_서랍 줄'), dict) else o.get('t2_서랍 줄'),
                '2 너비 끌고 목록 줄에서 떼니 떴나': (o.get('t2_첫 화면 목록 줄') or {}).get('view') if isinstance(o.get('t2_첫 화면 목록 줄'), dict) else o.get('t2_첫 화면 목록 줄'),
                '4 서랍이 한 줄이 됐나': (o.get('t4') or {}).get('rows'),
                '5 「서재」 톡으로 닫혔나': o.get('t5_closed')}
    if QC.GATE:   # 바탕 판 증상 재현 INFO — 관문만
        I('★ 바탕 판에서 아이패드 증상이 **재현됐는지** — 있는 그대로', rep)
    if QC.SMOKE:   # smoke — smoke 칸 줄만 남김(probe 가 TP-1 뒤 끝나 나머지 칸은 안 잼)
        L = [x for x in L if any(k in x for k in _RG_SMOKE)]

    for x in L:
        print('   ' + x)
    p = sum(1 for x in L if x.startswith('PASS')); f = sum(1 for x in L if x.startswith('FAIL'))
    print('\n합계  PASS %d · FAIL %d' % (p, f))
    io.open(os.path.join(HERE, '_harness_jagwa_touch_ipad_result.txt'), 'w', encoding='utf-8').write(
        '\n'.join(L) + '\n\n합계  PASS %d · FAIL %d\n' % (p, f))
    sys.exit(0 if not f else 1)


if __name__ == '__main__':
    main()
