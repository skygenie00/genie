# -*- coding: utf-8 -*-
"""조판기 채점 탭 세 구간 하네스 (2026-09-16 · _task_cha2_report.md §E G-4·G-5) — 로컬 앱 사본 + 데이터 사본 · CDP · 직렬로 돌릴 것
  python _harness_cha2_report.py g4 <앱.html> <픽스처 데이터 폴더(2인)> <픽스처 데이터 폴더(1인)> [W]   v2 레코드 카드 팝업 채점 탭
  python _harness_cha2_report.py g5 <앱.html> <출력.json> [W]                                         옛 레코드 카드 채점 탭 DOM(innerHTML) 덤프 — HEAD·NEW 둘을 떠서 맞댄다
데이터 = 클론 genie/jo/data 를 복사하고(g4 는 픽스처 JSON 을 덮는다) · 網은 막는다(fetch 는 같은 서버 data/ 만)"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import http.server, os, socketserver, subprocess, sys, threading, time, socket, json, base64, struct, urllib.request, urllib.parse, shutil, hashlib
sys.stdout.reconfigure(encoding='utf-8')
JO = _roots.genie(r'jo')
MODE = sys.argv[1]; APP = sys.argv[2]
W = int(sys.argv[5] if MODE == 'g4' and len(sys.argv) > 5 else (sys.argv[4] if MODE == 'g5' and len(sys.argv) > 4 else 1400))
SEED = """<script>try{localStorage.clear();localStorage.setItem('jopangi_c2fold','title');window.__err=[];window.addEventListener('error',e=>window.__err.push(String(e.message)));
const __nf=window.fetch.bind(window);window.fetch=function(u,o){const s=String(u);if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)return Promise.reject(new Error('net blocked by harness'));return __nf(u,o);};}catch(e){}</script>"""


class WS:
    def __init__(self, url):
        u = urllib.parse.urlparse(url); self.s = socket.create_connection((u.hostname, u.port), timeout=300)
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.send(('GET %s HTTP/1.1\r\nHost: %s:%d\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: %s\r\nSec-WebSocket-Version: 13\r\n\r\n' % (u.path, u.hostname, u.port, key)).encode())
        buf = b''
        while b'\r\n\r\n' not in buf:
            buf += self.s.recv(4096)
        self.n = 0

    def send(self, obj):
        data = json.dumps(obj).encode(); mask = os.urandom(4); L = len(data)
        head = bytes([0x81]) + (bytes([0x80 | L]) if L < 126 else (bytes([0x80 | 126]) + struct.pack('>H', L) if L < 65536 else bytes([0x80 | 127]) + struct.pack('>Q', L)))
        self.s.sendall(head + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def _recv(self, n):
        out = b''
        while len(out) < n:
            c = self.s.recv(n - len(out))
            if not c:
                raise IOError('closed')
            out += c
        return out

    def recv(self):
        msg = b''
        while True:
            h = self._recv(2); fin = h[0] & 0x80; L = h[1] & 0x7f
            if L == 126:
                L = struct.unpack('>H', self._recv(2))[0]
            elif L == 127:
                L = struct.unpack('>Q', self._recv(8))[0]
            msg += self._recv(L)
            if fin:
                return json.loads(msg.decode('utf-8'))

    def call(self, method, params=None):
        self.n += 1; self.send({'id': self.n, 'method': method, 'params': params or {}})
        while True:
            r = self.recv()
            if r.get('id') == self.n:
                return r.get('result', r)


def ev(ws, expr):
    r = ws.call('Runtime.evaluate', {'expression': expr, 'returnByValue': True, 'awaitPromise': True})
    if 'exceptionDetails' in r:
        return {'__exc': str(r['exceptionDetails'])[:800]}
    return r.get('result', {}).get('value')


def serve(app_html, data_over):
    tag = hashlib.md5((app_html + '|' + '|'.join(data_over) + '|%d' % W).encode()).hexdigest()[:8]
    OUT = os.path.join(os.environ['TEMP'], 'c2rh_' + MODE + '_' + tag); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    html = open(app_html, encoding='utf-8', newline='').read()
    i = html.find('<meta charset')
    j = html.find('>', i) + 1
    html = html[:j] + SEED + html[j:]
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    shutil.copytree(os.path.join(JO, 'data'), os.path.join(OUT, 'data'))
    for d in data_over:
        for f in os.listdir(d):
            if f.startswith('2cha_채점_') and f.endswith('.json'):
                shutil.copyfile(os.path.join(d, f), os.path.join(OUT, 'data', f))

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=OUT, **k)

        def log_message(self, *a, **k):
            pass
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    s = socket.socket(); s.bind(('127.0.0.1', 0)); dbg = s.getsockname()[1]; s.close()
    prof = os.path.join(OUT, 'prof')
    proc = subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", '--headless=new', '--disable-gpu', '--no-first-run', '--hide-scrollbars', '--user-data-dir=' + prof,
                             '--window-size=%d,900' % max(W, 500), '--remote-debugging-port=%d' % dbg, 'http://127.0.0.1:%d/index.html' % port], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    targets = None
    for _ in range(80):
        try:
            targets = json.loads(urllib.request.urlopen('http://127.0.0.1:%d/json' % dbg, timeout=2).read().decode())
            if any(t.get('type') == 'page' for t in targets):
                break
        except Exception:
            pass
        time.sleep(0.25)
    ws = WS(next(t for t in targets if t.get('type') == 'page')['webSocketDebuggerUrl']); ws.call('Page.enable')
    for _ in range(80):
        if ev(ws, "typeof popCard4==='function'&&typeof S!=='undefined'&&!!S&&typeof gradeOf==='function'"):
            break
        time.sleep(0.5)
    time.sleep(2)
    if W < 600:
        ws.call('Emulation.setDeviceMetricsOverride', {'width': W, 'height': 900, 'deviceScaleFactor': 2, 'mobile': True})
        ev(ws, '(async()=>{await render();await new Promise(r=>setTimeout(r,800));return innerWidth})()')
    return ws, proc, srv


LIB = r"""var wait=ms=>new Promise(r=>setTimeout(r,ms));
var closeAll=()=>{try{closeAllPops()}catch(e){};document.querySelectorAll('.pop').forEach(x=>{try{x.remove()}catch(e){}});};
var openGrade=async(law,subj,kind,pat)=>{S.law=law;S.tab='cha2';S.boardKind=kind;await render();await wait(300);
  const G=await gradeOf(subj);const ck=Object.keys(G).find(k=>k.indexOf('card|'+kind+'|')===0&&k.indexOf(pat)>=0);if(!ck)return {err:'카드키 없음 '+pat};
  const file=ck.split('|').slice(2).join('|');closeAll();await popCard4(kind,file,null,1,null,'채점');
  let pop=null;for(let i=0;i<60;i++){await wait(100);pop=[...document.querySelectorAll('.pop')].find(p=>p.querySelector('.gtabs')&&(p.textContent||'').indexOf(file.slice(0,20))>=0);
    if(pop){const c=pop.querySelector('.gtabs').nextElementSibling;if(c&&!/^…$/.test((c.textContent||'').trim())&&c.childNodes.length)break;}}
  await wait(300);return {ck,file,pop,cont:pop?pop.querySelector('.gtabs').nextElementSibling:null};};
"""

G4 = LIB + r"""(async()=>{const R=[];const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+(c?'':' | '+JSON.stringify(i===undefined?null:i)));
 try{
  const phone=innerWidth<=640;
  /* 1 · 특허 기출 63-2 (2인 · 해설 둘) */
  let o=await openGrade('특허법','특허','기출','특기출 26-63-2');
  const r=o.cont&&o.cont.querySelector('.c2r');
  T('G-4 v2 카드(특기출 26-63-2) 채점 탭에 .c2r 1 · section 3',!!r&&o.cont.querySelectorAll('.c2r').length===1&&r.querySelectorAll(':scope>section').length===3,[o.err,o.cont&&o.cont.querySelectorAll('.c2r').length,r&&r.querySelectorAll(':scope>section').length]);
  if(r){
   const sl=[...r.querySelectorAll('div.c2r-sl')];
   T('G-4 점수 표 설문 줄 div.c2r-sl '+sl.length+'개 전부 text-align:left(계산값) · 칸 td 는 right',sl.length>0&&sl.every(x=>getComputedStyle(x).textAlign==='left')&&getComputedStyle(sl[0].closest('td')).textAlign==='right',sl.slice(0,3).map(x=>getComputedStyle(x).textAlign));
   T('G-4 점수 표 = 사람 2행 · 열 = 문1~문4 + 합 · 이 카드 열(문2) 강조',r.querySelectorAll('table.c2r-st tr').length===3&&[...r.querySelectorAll('table.c2r-st tr:first-child th')].map(x=>x.textContent).join('|')==='|문1 (30)|문2 (20)|문3 (30)|문4 (20)|합 (100)'&&r.querySelector('table.c2r-st th.c2r-cur').textContent==='문2 (20)',[...r.querySelectorAll('table.c2r-st tr:first-child th')].map(x=>x.textContent));
   const sl1=sl.map(x=>x.textContent);
   T('G-4 설문 줄 글자꼴 설(n)(s)[-누락(조n판n사n?n)][-답틀]',sl1.every(t=>/^(설\S*\(\d+(\.\d+)?\)|설문 미배정)(-누락\((조\d+)?(판\d+)?(사\d+)?(\?\d+)?\))?(-답틀)?$/.test(t)),sl1.filter(t=>!/^(설\S*\(\d+(\.\d+)?\)|설문 미배정)(-누락\((조\d+)?(판\d+)?(사\d+)?(\?\d+)?\))?(-답틀)?$/.test(t)).slice(0,5));
   const tot=[...r.querySelectorAll('table.c2r-st td.c2r-tot')].map(x=>x.firstChild.textContent);
   T('G-4 합 = 설문 값 합(⚙ 계산) — 햄찌 56.5 · 꼬까 57',tot.join('/')==='56.5/57',tot);
   const qs=[...r.querySelectorAll('section.c2r-toc .c2r-col ol.c2r-ol>li>em')].map(x=>x.textContent);
   T('G-4 목차 구간 설문 제목 전부 (N점) — '+qs.length+'개',qs.length>0&&qs.every(t=>/\(\d+(\.\d+)?점\)/.test(t)),qs.filter(t=>!/\(\d+(\.\d+)?점\)/.test(t)));
   const tg=[...r.querySelectorAll('.c2r-tg b')];
   T('G-4 해설 둘(홍기석·한빛) → 단추 2 · 기본 = fm 첫째(홍기석)',tg.length===2&&tg[0].classList.contains('on')&&tg[0].textContent==='홍기석',tg.map(b=>b.textContent+(b.classList.contains('on')?'*':'')));
   const hae=r.querySelector('.c2r-hae');const ols=()=>[...hae.children].filter(x=>x.tagName==='OL').map(x=>x.style.display||'show');
   const before=ols();if(tg[1])tg[1].click();await wait(50);const after=ols();
   T('G-4 단추 누르면 해설 목차가 번갈아(홍기석 → 한빛)',before.join()==='show,none'&&after.join()==='none,show'&&tg[1].classList.contains('on'),[before,after]);
   T('G-4 사람 열 2 · 머리 = 이름 + 점수/배점',[...r.querySelectorAll('section.c2r-toc .c2r-cols>.c2r-col')].length===3&&/^햄찌 11 \/ 20$/.test(r.querySelectorAll('section.c2r-toc .c2r-cols>.c2r-col')[1].querySelector('.c2r-hd').textContent),[...r.querySelectorAll('section.c2r-toc .c2r-col .c2r-hd')].map(x=>x.textContent));
   T('G-4 누락 줄 = 붉은 li.c2r-miss(「— 안 씀」+ X 칩) · 목차 줄 판정 없음 = 회색 해설 밖',r.querySelectorAll('li.c2r-miss').length>0&&[...r.querySelectorAll('li.c2r-miss')].every(x=>/— 안 씀/.test(x.textContent)&&x.querySelector('.c2r-chip.c2r-x'))&&r.querySelectorAll('li.c2r-out').length>0,[r.querySelectorAll('li.c2r-miss').length,r.querySelectorAll('li.c2r-out').length]);
   T('G-4 답틀 칩(.c2r-rev) 있음 — 문2 설(1) 두 사람',r.querySelectorAll('section.c2r-toc .c2r-rev').length>=2,r.querySelectorAll('section.c2r-toc .c2r-rev').length);
   T('G-4 2인 = 코멘트 비교 표 .c2r-cmp 1 · 행 이름 차례',r.querySelectorAll('.c2r-cmp').length===1,[...r.querySelectorAll('.c2r-cmp tr td:first-child')].map(x=>x.textContent));
   const dt=r.querySelector('details.c2r-prose');
   T('G-4 산문 = details 기본 접힘 · 펼치면 판 4 줄(.ln) 렌더',!!dt&&!dt.open&&dt.querySelectorAll('.ln').length>10,[!!dt,dt&&dt.open,dt&&dt.querySelectorAll('.ln').length]);
   const cols=r.querySelector('section.c2r-toc .c2r-cols');const gtc=getComputedStyle(cols).gridTemplateColumns.trim().split(/\s+/).length;
   T((phone?'G-4 폰 '+innerWidth+' — .c2r-cols 세로(트랙 1)':'G-4 넓은 창 '+innerWidth+' — .c2r-cols 트랙 = 해설 + 사람 2 = 3')+' · 팝업 폭 '+Math.round(o.pop.getBoundingClientRect().width),phone?gtc===1:(gtc===3||Math.round(r.getBoundingClientRect().width)<=640),[gtc,Math.round(r.getBoundingClientRect().width)]);
  }
  /* 2 · 특허 사례 7-1-2 (해설 하나) */
  o=await openGrade('특허법','특허','사례','특사례 7-1-2');const r2=o.cont&&o.cont.querySelector('.c2r');
  T('G-4 사례 카드(7-1-2) 해설 하나 → 단추 0 · section 3 · 점수 열 = 사례 3(8-4-4a 카드 없음 → 알림)',!!r2&&r2.querySelectorAll('.c2r-tg b').length===0&&r2.querySelectorAll(':scope>section').length===3&&[...r2.querySelectorAll('table.c2r-st tr:first-child th')].length===5&&/카드 없는 문제 1개/.test(r2.textContent),[o.err,r2&&r2.querySelectorAll('.c2r-tg b').length,r2&&[...r2.querySelectorAll('table.c2r-st tr:first-child th')].map(x=>x.textContent)]);
  T('G-4 사례 카드 공통 통누락 .c2r-common 1(두 사람 다 X 인 해설 줄 = 증명책임 2017후844 포함)',!!r2&&r2.querySelectorAll('.c2r-common').length===1&&/2017후844/.test(r2.querySelector('.c2r-common').textContent),r2&&r2.querySelectorAll('.c2r-common').length);
  T('G-4 누락 줄 판례 칩(⚖) — 7-1-2 에 판례번호 든 해설 줄 맞대기',!!r2&&r2.querySelectorAll('li.c2r-miss .chip.c-prec').length>0,r2&&r2.querySelectorAll('li.c2r-miss .chip').length);
  if(r2){const lk=[...r2.querySelectorAll('table.c2r-cmp .chip.c-src')];const n0=document.querySelectorAll('.pop').length;if(lk[0])lk[0].click();await wait(900);const pops=[...document.querySelectorAll('.pop')];
   T('G-6 판 4 팝업 링크 — 보완 블록 링크 칩 '+lk.length+'개 · 첫 칩 누르면 노트 팝업(📄 '+(lk[0]?lk[0].textContent:'')+')',lk.length>0&&pops.length>n0&&pops.some(p=>/8\.1\./.test(p.textContent||'')),[lk.length,n0,pops.length,pops.slice(-1).map(p=>(p.textContent||'').slice(0,60))]);
   const pc=r2.querySelector('li.c2r-miss .chip.c-prec:not(.wait)');const n1=document.querySelectorAll('.pop').length;if(pc)pc.click();await wait(900);
   T('G-6 판 4 팝업 링크 — 누락 줄 판례 칩 누르면 판례 팝업('+(pc?pc.textContent:'칩 없음')+')',!!pc&&document.querySelectorAll('.pop').length>n1,[!!pc,n1,document.querySelectorAll('.pop').length]);}
  /* 3 · 민소 기출 2인(해설 못 찾음) — 1인 판은 아래 따로 */
  o=await openGrade('민사소송법','민소','기출','민기출 26-63-3');const r3=o.cont&&o.cont.querySelector('.c2r');
  T('G-4 민소 2인 카드(26-63-3) — section 3 · 해설 콜아웃 둘(정경대·곽준형 · 못 찾음) → 단추 2 · 줄 = (해설 목차 못 찾음 …) · 꼬까 열 = (목차 못 찾음 …)',!!r3&&r3.querySelectorAll(':scope>section').length===3&&r3.querySelectorAll('.c2r-tg b').length===2&&/해설 목차 못 찾음/.test(r3.querySelector('.c2r-hae').textContent)&&/목차 못 찾음/.test(r3.querySelectorAll('section.c2r-toc .c2r-cols>.c2r-col')[2].textContent),[o.err,r3&&r3.querySelectorAll('.c2r-tg b').length]);
  T('G-4 민소 2인 카드 코멘트 표 .c2r-cmp 1(잘된 점·고칠 점 행)',!!r3&&r3.querySelectorAll('.c2r-cmp').length===1&&/잘된 점/.test(r3.querySelector('.c2r-cmp').textContent),r3&&r3.querySelectorAll('.c2r-cmp').length);
  T('JS 오류 0',(window.__err||[]).length===0,window.__err);
 }catch(e){R.push('FAIL | 예외 | '+(e&&e.stack||e));}
 return R.join('\n');})()"""

G5 = LIB + r"""(async()=>{const out={};
 for(const [law,subj,kind,pat] of [['특허법','특허','기출','특기출 26-63-1'],['특허법','특허','기출','특기출 26-63-2'],['특허법','특허','사례','특사례 7-1-2'],['특허법','특허','사례','특사례 8-3-3'],['민사소송법','민소','기출','민기출 26-63-3'],['민사소송법','민소','기출','민기출 26-63-4']]){
  const o=await openGrade(law,subj,kind,pat);out[pat]={err:o.err||'',html:o.cont?o.cont.innerHTML:'',c2r:o.cont?o.cont.querySelectorAll('.c2r').length:-1,len:o.cont?o.cont.innerHTML.length:0};}
 out.__err=window.__err||[];return JSON.stringify(out);})()"""

if MODE == 'g4':
    fx2, fx1 = sys.argv[3], sys.argv[4]
    ws, proc, srv = serve(APP, [fx2])
    try:
        # 1인 판은 같은 창에서 민소 JSON 만 갈아 끼운다(서버 파일 교체 + 앱 캐시 C 비움)
        out = ev(ws, G4)
        # 민소 1인: 서버 data 의 민소 JSON 을 fx1 것으로 바꾸고 3 단계만 다시
        served = [d for d in os.listdir(os.environ['TEMP']) if d.startswith('c2rh_g4_')]
        root = max((os.path.join(os.environ['TEMP'], d) for d in served), key=os.path.getmtime)
        shutil.copyfile(os.path.join(fx1, '2cha_채점_민소.json'), os.path.join(root, 'data', '2cha_채점_민소.json'))
        ev(ws, "(()=>{for(const k of Object.keys(C))if(k.indexOf('2cha_채점_민소')===0)delete C[k];window.__ONE=1;return 1})()")
        one = ev(ws, LIB + r"""(async()=>{const R=[];const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+(c?'':' | '+JSON.stringify(i===undefined?null:i)));
          const o=await openGrade('민사소송법','민소','기출','민기출 26-63-3');const r3=o.cont&&o.cont.querySelector('.c2r');
          const who=r3?[...r3.querySelectorAll('table.c2r-st tr td:first-child')].map(x=>x.textContent):null;
          T('G-4 1인 카드(민소 사람=[햄찌]) → .c2r-cmp 0 · .c2r-common 0 · 산문 있음 · section 3 · 점수 행 1',!!r3&&who.join()==='햄찌'&&r3.querySelectorAll('.c2r-cmp').length===0&&r3.querySelectorAll('.c2r-common').length===0&&!!r3.querySelector('details.c2r-prose')&&r3.querySelectorAll(':scope>section').length===3,[o.err,who,r3&&r3.querySelectorAll('.c2r-cmp').length,r3&&r3.querySelectorAll('.c2r-common').length]);
          T('G-4 1인 카드 목차 열 = 해설 + 사람 1',!!r3&&r3.querySelectorAll('section.c2r-toc .c2r-cols>.c2r-col').length===2,r3&&r3.querySelectorAll('section.c2r-toc .c2r-cols>.c2r-col').length);
          T('JS 오류 0(1인 판 뒤)',(window.__err||[]).length===0,window.__err);return R.join('\n');})()""")
        text = (out if isinstance(out, str) else json.dumps(out, ensure_ascii=False)) + '\n' + (one if isinstance(one, str) else json.dumps(one, ensure_ascii=False))
        for ln in text.split('\n'):
            print(ln)
        print('== %d PASS / %d FAIL == (W %d)' % (text.count('PASS |'), text.count('FAIL |'), W))
    finally:
        proc.terminate(); srv.shutdown()
elif MODE == 'g5':
    ws, proc, srv = serve(APP, [])
    try:
        out = ev(ws, G5)
        open(sys.argv[3], 'w', encoding='utf-8').write(out if isinstance(out, str) else json.dumps(out, ensure_ascii=False))
        d = json.loads(out) if isinstance(out, str) else out
        print({k: (v['c2r'], v['len'], v['err']) for k, v in d.items() if k != '__err'}, 'err', d.get('__err') if isinstance(d, dict) else d)
    finally:
        proc.terminate(); srv.shutdown()
