# -*- coding: utf-8 -*-
"""조판기 판례탭 — 볼트 `연결판례`·`연결사례` 하네스 (2026-09-20 · `_task_prec_vault_link.md` §C)

  python _harness_prec_vault_link.py <앱.html> <데이터 폴더> [창 너비]

재는 것 = DOM 실물(있는가·몇 개인가·눌러서 무엇이 열리는가). 픽셀은 안 찍는다(CLAUDE.md 검산 게이트 절).
網은 막는다 — fetch 는 같은 서버 `data/` 만.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402 — _task_qa_slim(10/4) 실행 모드: --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같다) · 새 갈래는 모두 `if QJ.REGRESS:` / `if QJ.GATE:` 안
import http.server, os, socketserver, subprocess, sys, threading, time, socket, json, base64, struct, urllib.request, urllib.parse, shutil, hashlib
sys.stdout.reconfigure(encoding='utf-8')
APP = sys.argv[1]
DATA = sys.argv[2]
W = int(sys.argv[3]) if len(sys.argv) > 3 else 1400

# 앱 기록 씨앗 — G-2 「앱 1 + 볼트 1 = 2」 를 재려면 사용자 기록과 같은 항목이 하나 있어야 한다.
SEED_LINK = {"2023후11562": [{"t": 1789754513139, "law": "특허", "k": "prec", "to": "2023후11487", "why": ""}]}
SEED = ("""<script>try{localStorage.clear();localStorage.setItem('jopangi.preclink',%s);
window.__err=[];window.addEventListener('error',e=>window.__err.push(String(e.message)));
const __nf=window.fetch.bind(window);window.fetch=function(u,o){const s=String(u);
 if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)return Promise.reject(new Error('net blocked by harness'));return __nf(u,o);};}catch(e){}</script>"""
        % json.dumps(json.dumps(SEED_LINK, ensure_ascii=False)))


class WS:
    def __init__(self, url):
        u = urllib.parse.urlparse(url); self.s = socket.create_connection((u.hostname, u.port), timeout=300)
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.send(('GET %s HTTP/1.1\r\nHost: %s:%d\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: %s\r\nSec-WebSocket-Version: 13\r\n\r\n'
                     % (u.path, u.hostname, u.port, key)).encode())
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


def serve():
    tag = hashlib.md5((APP + '|' + DATA + '|%d' % W).encode()).hexdigest()[:8]
    OUT = os.path.join(os.environ['TEMP'], 'pvl_' + tag); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    html = open(APP, encoding='utf-8', newline='').read()
    i = html.find('<meta charset'); j = html.find('>', i) + 1
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8', newline='').write(html[:j] + SEED + html[j:])
    if QJ.GATE:
        shutil.copytree(DATA, os.path.join(OUT, 'data'))

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=OUT, **k)

        def log_message(self, *a, **k):
            pass
        if QJ.REGRESS:   # regress — data 폴더를 복사하지 않고 DATA 에서 바로 낸다(읽는 파일은 같다 · 128MB 복사 · 임시 폴더 잔재 0)
            def translate_path(self, path):
                p = urllib.parse.unquote(path.split('?', 1)[0].split('#', 1)[0])
                if p.startswith('/data/'):
                    return os.path.join(DATA, *[x for x in p[6:].split('/') if x and x not in ('.', '..')])
                return super().translate_path(path)
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    s = socket.socket(); s.bind(('127.0.0.1', 0)); dbg = s.getsockname()[1]; s.close()
    prof = os.path.join(OUT, 'prof')
    QJ.launch('new')
    proc = subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", '--headless=new', '--disable-gpu',
                             '--no-first-run', '--hide-scrollbars', '--user-data-dir=' + prof,
                             '--window-size=%d,900' % max(W, 500), '--remote-debugging-port=%d' % dbg,
                             'http://127.0.0.1:%d/index.html' % port], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    targets = None
    for _ in range(80 if QJ.GATE else 400):
        try:
            targets = json.loads(urllib.request.urlopen('http://127.0.0.1:%d/json' % dbg, timeout=2).read().decode())
            if any(t.get('type') == 'page' for t in targets):
                break
        except Exception:
            pass
        time.sleep(0.25 if QJ.GATE else 0.05)
    ws = WS(next(t for t in targets if t.get('type') == 'page')['webSocketDebuggerUrl']); ws.call('Page.enable')
    for _ in range(80 if QJ.GATE else 400):
        if ev(ws, "typeof precLinkGlyphs==='function'&&typeof vlPrec==='function'&&typeof S!=='undefined'&&!!S"):
            break
        time.sleep(0.5 if QJ.GATE else 0.1)
    if QJ.GATE:
        time.sleep(2)
    else:
        _boot_wait(ws, 2000)   # regress — 고정 2초 → 앱 표지(busy · #slot) · 최대 2초
    return ws, proc, srv


TEST = r"""var wait=ms=>new Promise(r=>setTimeout(r,ms));
var closeAll=()=>{try{closeAllPops()}catch(e){};document.querySelectorAll('.pop').forEach(x=>{try{x.remove()}catch(e){}});};
var openList=async(law,q)=>{closeAll();S.law=law;S.tab='prec';S.precQ=q;S.prec='';await render();await wait(700);
  const rows=[...document.querySelectorAll('.plist .row, .plist .prow, .plist > div')];return rows;};
var glyphRow=async(law,q,id)=>{await openList(law,q);
  /* 목록 행 중 그 판례 것 — .plg 를 품고 사건번호 글자가 든 행 */
  const cand=[...document.querySelectorAll('.plg')].map(g=>g.closest('div')).filter(Boolean);
  for(const c of cand){ let n=c; for(let k=0;k<5&&n;k++){ if((n.textContent||'').indexOf(id)>=0) return n.querySelector('.plg')||c.querySelector('.plg'); n=n.parentElement; } }
  return null;};
var glyphText=g=>g?[...g.querySelectorAll('.plgb')].map(b=>b.textContent.trim()):null;
(async()=>{const R=[];const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+(c?'':' | '+JSON.stringify(i===undefined?null:i)));
 try{
  /* ───── G-1 ───── */
  let g=await glyphRow('특허법','2024후11125','2024후11125');
  let gt=glyphText(g);
  T('G-1a 2024후11125 목록 행에 ↩링크1', !!gt&&gt.some(x=>x==='↩링크1'), gt);
  { const b=g?[...g.querySelectorAll('.plgb')].find(x=>/^↩링크/.test(x.textContent.trim())):null;
    if(!b) T('G-1b~d 링크 창', false, '↩링크 글자가 없다'); else {
    b.click(); await wait(600);
    const pop=[...document.querySelectorAll('.pop')].find(p=>(p.textContent||'').indexOf('↩ 링크')>=0);
    const rows=pop?[...pop.querySelectorAll('.plwl .res')]:[];
    const vt=rows.filter(r=>[...r.querySelectorAll('.badge')].some(x=>x.textContent.trim()==='볼트'));
    T('G-1b 링크 창에 볼트 줄 1 · 2025후10169', vt.length===1&&(vt[0].textContent||'').indexOf('2025후10169')>=0, [rows.length,vt.length,vt[0]&&vt[0].textContent.slice(0,80)]);
    T('G-1c 볼트 줄에 ✎·✕ 없음', vt.length===1&&vt[0].querySelectorAll('.tool').length===0, vt[0]?vt[0].querySelectorAll('.tool').length:-1);
    if(vt.length===1){ vt[0].click(); await wait(800);
      const pp=[...document.querySelectorAll('.pop')].filter(p=>(p.textContent||'').indexOf('2025후10169')>=0);
      T('G-1d 볼트 줄 클릭 = 2025후10169 판례 팝업', pp.length>0, pp.length); }
    closeAll(); } }
  g=await glyphRow('특허법','2025후10169','2025후10169'); gt=glyphText(g);
  /* ⚠ 지시서 G-1 은 「↩백링크1」 이라 적었으나 볼트 실측은 둘이다 — 2024후11125 와 2022후10524 가 이 판례를 건다(9/20 잼). */
  T('G-1e 2025후10169 에 ↩백링크2 (볼트 2 — 2024후11125 · 2022후10524)', !!gt&&gt.some(x=>x==='↩백링크2'), gt);
  { const b=g?[...g.querySelectorAll('.plgb')].find(x=>/^↩백링크/.test(x.textContent.trim())):null;
    if(b){ b.click(); await wait(600);
      const pop=[...document.querySelectorAll('.pop')].find(p=>(p.textContent||'').indexOf('↩ 백링크')>=0);
      const vt=pop?[...pop.querySelectorAll('.plwl .res')].filter(r=>[...r.querySelectorAll('.badge')].some(x=>x.textContent.trim()==='볼트')):[];
      T('G-1f 백링크 창 볼트 줄 2 · 2024후11125 있음', vt.length===2&&vt.some(r=>(r.textContent||'').indexOf('2024후11125')>=0), [vt.length,vt.map(x=>x.textContent.slice(0,40))]);
      closeAll(); }
    else T('G-1f 백링크 창', false, '↩백링크 글자가 없다'); }

  /* ───── G-2 ───── */
  g=await glyphRow('특허법','2023후11562','2023후11562'); gt=glyphText(g);
  T('G-2a 2023후11562 ↩링크2 (앱 1 + 볼트 1)', !!gt&&gt.some(x=>x==='↩링크2'), gt);
  { const b=g?[...g.querySelectorAll('.plgb')].find(x=>/^↩링크/.test(x.textContent.trim())):null;
    if(b){ b.click(); await wait(600);
    const pop=[...document.querySelectorAll('.pop')].find(p=>(p.textContent||'').indexOf('↩ 링크')>=0);
    const rows=pop?[...pop.querySelectorAll('.plwl .res')]:[];
    const vt=rows.filter(r=>[...r.querySelectorAll('.badge')].some(x=>x.textContent.trim()==='볼트'));
    T('G-2b 링크 창 줄 2 (앱 1 · 볼트 1 · 둘 다 2023후11487)', rows.length===2&&vt.length===1&&rows.every(r=>(r.textContent||'').indexOf('2023후11487')>=0), [rows.length,vt.length]);
    closeAll(); } }
  /* 사례 카드 — 3단 머리 🧾 칩 */
  { closeAll(); S.law='특허법';S.tab='prec';S.precQ='';S.prec='2023후11562';S.precTab='요약';await render();await wait(900);
    const chips=[...document.querySelectorAll('.chip')].map(c=>c.textContent.trim());
    const sarae=chips.find(c=>c.indexOf('🧾 사례')===0);
    T('G-2c 3단 머리 🧾 사례 2 (⚙ 추가사례3 + 볼트 특사례 2-3-2)', sarae==='🧾 사례 2', [sarae,chips.filter(c=>c.indexOf('🧾')===0)]);
    const el2=[...document.querySelectorAll('.chip')].find(c=>c.textContent.trim().indexOf('🧾 사례')===0);
    if(el2){ el2.click(); await wait(900);
      const pop=[...document.querySelectorAll('.pop')].find(p=>(p.textContent||'').indexOf('🧾 사례')>=0);
      const txt=pop?pop.textContent:'';
      T('G-2d 사례 목록에 특사례 2-3-2 · 추가사례3(A)', txt.indexOf('특사례 2-3-2')>=0&&txt.indexOf('추가사례3(A)')>=0, txt.slice(0,220));
      const grey=pop?[...pop.querySelectorAll('.res.plout')].map(r=>r.textContent.trim()):[];
      T('G-2e 「설(4)」 회색 한 줄', grey.some(x=>x.indexOf('설(4)')===0), grey);
      const vb=pop?[...pop.querySelectorAll('.res')].filter(r=>[...r.querySelectorAll('.badge')].some(x=>x.textContent.trim()==='볼트')):[];
      T('G-2f 볼트 배지 붙은 카드 줄 ≥1', vb.length>=1, vb.map(x=>x.textContent.slice(0,40)));
      closeAll(); } }

  /* ───── 무변 관문 — 볼트 링크가 없는 판례는 글자가 그대로 ───── */
  g=await glyphRow('특허법','2012후832','2012후832'); gt=glyphText(g);
  T('Z-1 2012후832 (볼트 링크 1 · 앱 0) = ↩링크1', !!gt&&gt.some(x=>x==='↩링크1'), gt);

  /* ───── 상표 — GS 카드 ───── */
  { closeAll(); S.law='상표법';S.tab='prec';S.precQ='';S.prec='';await render();await wait(700);
    const P=await get(PF('리스트'));
    const n=(P.판례||[]).reduce((a,p)=>a+((p.연결사례||[]).filter(x=>x.kind==='GS').length),0);
    T('Z-2 상표 연결사례 GS 25', n===25, n); }

  /* ───── E-4 · 기출 원천 볼트 이관 ───── */
  { closeAll(); S.law='상표법';S.tab='prec';S.precQ='';S.prec='2002후567(모나리자 굿모닝)';S.precTab='요약';await render();await wait(900);
    const gi=[...document.querySelectorAll('.pdesc .chip.c-gi')].map(c=>c.textContent.trim());
    const tag=[...document.querySelectorAll('.pdesc .chip.c-theme')].map(c=>c.textContent.trim());
    T('E-4a 2002후567 상표 카드 기출 칩 6 · 낱말 태그 0', gi.length===6&&tag.length===0, [gi,tag]);
    T('E-4b 2차-특-16-53-3 M 강조', gi.indexOf('2차-특-16-53-3 M')>=0 &&
      [...document.querySelectorAll('.pdesc .chip.c-gi.gimain')].map(c=>c.textContent.trim()).sort().join('|')==='2차-상-26-63-3 M|2차-특-16-53-3 M',
      [...document.querySelectorAll('.pdesc .chip.c-gi.gimain')].map(c=>c.textContent.trim()));
    const el3=[...document.querySelectorAll('.pdesc .chip.c-gi')].find(c=>c.textContent.trim()==='2차-특-16-53-3 M');
    if(el3){ el3.click(); await wait(1600);
      const pop=[...document.querySelectorAll('.pop')].find(p=>(p.textContent||'').indexOf('특기출 16-53-3')>=0);
      T('E-4c 그 칩 클릭 = 특기출 16-53-3 카드(법 옮겨서)', !!pop&&S.law==='특허법', [S.law, !!pop]);
      closeAll(); } else T('E-4c 그 칩 클릭', false, '칩 없음'); }
  { closeAll(); S.law='특허법';S.tab='prec';S.precQ='';S.prec='2002후567';await render();await wait(600);
    const P2=await get(PF('리스트'));
    T('E-4d 2002후567 이 특허 리스트에서 사라짐 · 특허 391 · 상표 315',
      !(P2.판례||[]).some(x=>x.id.indexOf('2002후567')>=0) && (P2.판례||[]).length===391,
      [(P2.판례||[]).length]); }
  { closeAll(); S.law='특허법';S.tab='prec';S.precQ='';S.prec='2023후11562';await render();await wait(800);
    const gi=[...document.querySelectorAll('.pdesc .chip.c-gi')].map(c=>c.textContent.trim());
    const tag=[...document.querySelectorAll('.pdesc .chip.c-theme')].map(c=>c.textContent.trim());
    T('E-4e 2023후11562 = 2차-특-26-63-4 M 한 줄 · 보라 중복 0',
      gi.filter(x=>x.indexOf('2차-')===0).join('|')==='2차-특-26-63-4 M' && tag.length===0, [gi,tag]); }
  { closeAll(); S.law='특허법';S.tab='prec';S.precQ='';S.prec='2012후832';await render();await wait(800);
    const gi=[...document.querySelectorAll('.pdesc .chip.c-gi')].map(c=>c.textContent.trim());
    T('E-4f 2012후832 1차 넷 그대로', gi.filter(x=>x.indexOf('1차-')===0).length===4, gi); }
  { closeAll(); S.law='상표법';S.tab='prec';S.precQ='';S.prec='2018도14446(METROCITY 권리소진)';await render();await wait(800);
    const gi=[...document.querySelectorAll('.pdesc .chip.c-gi')].map(c=>c.textContent.trim());
    const tag=[...document.querySelectorAll('.pdesc .chip.c-theme')].map(c=>c.textContent.trim());
    T('E-4g 2018도14446 = 2차-특-19-56-3 (M 없음) · 낱말 태그 둘',
      gi.indexOf('2차-특-19-56-3')>=0 && gi.indexOf('2차-특-19-56-3 M')<0 && tag.length===2, [gi,tag]); }
  { closeAll(); S.law='특허법';S.tab='prec';S.precQ='';S.prec='';await render();await wait(700);
    const P3=await get(PF('리스트'));
    const bad=(P3.판례||[]).filter(p=>('기출비고' in p));
    T('E-4h 기출비고 열 폐기', bad.length===0, bad.length); }
  /* ───── add2 · 1차 칩은 언제나 팝업 ───── */
  /* ⚠ 지시서 add2 는 2002후567 의 `1차-상-07-44-r7` 을 흐린 칩 보기로 들었으나 실측은 **진하다**
     (2007·2010 상표 문항이 JSON 에 있다). 실제 흐린 칩은 `1차-특-20-57-17`(원장짝없음 · 다른 법)이다. */
  { closeAll(); S.law='상표법';S.tab='prec';S.precQ='';S.prec='2002후567(모나리자 굿모닝)';S.precTab='요약';await render();await wait(900);
    const before=S.tab, lawBefore=S.law;
    const cs=[...document.querySelectorAll('.pdesc .chip.c-gi')];
    const c0=cs.find(c=>c.textContent.trim()==='1차-상-07-44-r7');
    T('A2-a 1차-상-07-44-r7 = 진한 칩(문항 있음)', !!c0 && c0.style.opacity!=='0.6', [!!c0, c0&&c0.style.opacity]);
    const c1=cs.find(c=>c.textContent.trim()==='1차-특-20-57-17');
    T('A2-b 1차-특-20-57-17 = 흐림 + 까닭 툴팁', !!c1 && c1.style.opacity==='0.6' && /원장 짝 없음/.test(c1.title||''), [c1&&c1.style.opacity, c1&&c1.title]);
    T('A2-c 흐림 범례 한 줄', !!document.querySelector('.pdesc .gilgd'), document.querySelector('.pdesc .gilgd')?document.querySelector('.pdesc .gilgd').textContent:'없음');
    if(c1){ c1.click(); await wait(1400);
      const pop=[...document.querySelectorAll('.pop')].find(p=>(p.textContent||'').indexOf('문항 카드가 없다')>=0);
      T('A2-d 흐린 칩 = 안내 팝업 · tab·법 무변', !!pop && S.tab===before && S.law===lawBefore, [!!pop,S.tab,S.law]);
      T('A2-e 안내에 까닭 + 「그 해 기출뷰로 ↗」 단추',
        !!pop && /원장 짝이 없다/.test(pop.textContent) && [...pop.querySelectorAll('button')].some(b=>/기출뷰로/.test(b.textContent)),
        pop?pop.textContent.slice(0,150):'');
      if(pop){ c1.click(); await wait(500);
        T('A2-f 같은 칩 다시 = 닫힘', ![...document.querySelectorAll('.pop')].some(p=>(p.textContent||'').indexOf('문항 카드가 없다')>=0), document.querySelectorAll('.pop').length); }
      closeAll(); }
    if(c0){ const b2=S.tab; c0.click(); await wait(1000);
      T('A2-g 진한 1차 칩 = 문항 카드 팝업 · tab 무변', document.querySelectorAll('.pop').length>0 && S.tab===b2, [document.querySelectorAll('.pop').length,S.tab]);
      closeAll(); } }
  { closeAll(); S.law='특허법';S.tab='prec';S.precQ='';S.prec='2012후832';await render();await wait(800);
    const before=S.tab;
    const c3=[...document.querySelectorAll('.pdesc .chip.c-gi')].find(c=>/^1차-특-12-49/.test(c.textContent.trim()));
    T('A2-h 2012후832 진한 1차 칩 클릭 = 팝업 · tab 무변',
      !!c3 && (c3.click(), await wait(1000), document.querySelectorAll('.pop').length>0 && S.tab===before), [document.querySelectorAll('.pop').length,S.tab]);
    closeAll(); }
  /* G-3 — 1차 칩 여러 개를 눌러도 S.tab 이 바뀌지 않는다 */
  { closeAll();
    let moved=0, n=0;
    for(const [law,id] of [['특허법','2012후832'],['특허법','2023후11562'],['특허법','78후3'],['특허법','84후19'],['상표법','2015후1997(더블유컨셉)']]){
      S.law=law;S.tab='prec';S.precQ='';S.prec=id; await render(); await wait(600);
      const cs=[...document.querySelectorAll('.pdesc .chip.c-gi')].filter(c=>/^1차-/.test(c.textContent.trim()));
      for(let k=0;k<cs.length;k++){ const b=S.tab; cs[k].click(); await wait(600); n++; if(S.tab!==b) moved++; closeAll();
        if(S.law!==law){ S.law=law; S.prec=id; await render(); await wait(400); } } }
    T('A2-i 1차 칩 '+n+'번 클릭 · S.tab 바뀐 횟수 0', n>0 && moved===0, [n,moved]); }
  /* ───── add1 §C — 특↔상 교차 링크 ───── */
  { closeAll(); S.law='상표법';S.tab='prec';S.precQ='';S.prec='';await render();await wait(700);
    const Ps=await get(PF('리스트'));
    const xs=(Ps.판례||[]).filter(p=>(p.연결판례||[]).some(y=>y.law==='특허'&&y.id));
    T('A1-a 상표 → 특허 교차 링크 있는 행 2', xs.length===2, xs.map(p=>p.id));
    const g=await glyphRow('상표법','2003허4191','2003허4191');
    const b=g&&[...g.querySelectorAll('.plgb')].find(z=>/^↩링크/.test(z.textContent.trim()));
    if(b){ b.click(); await wait(700);
      const pop=[...document.querySelectorAll('.pop')].find(p=>(p.textContent||'').indexOf('↩ 링크')>=0);
      const row=pop&&[...pop.querySelectorAll('.plwl .res')].find(r=>[...r.querySelectorAll('.lawtag')].some(z=>z.textContent.trim()==='[특]'));
      T('A1-b 링크 창에 [특] 표시 줄 (98후1921)', !!row && /98후1921/.test(row.textContent), pop?pop.textContent.slice(0,160):'창 없음');
      if(row){ row.click(); await wait(1800);
        T('A1-c 그 줄 클릭 = 특허법으로 옮겨 판례 팝업',
          S.law==='특허법' && [...document.querySelectorAll('.pop')].some(p=>(p.textContent||'').indexOf('98후1921')>=0),
          [S.law, document.querySelectorAll('.pop').length]); }
      closeAll(); }
    else T('A1-b 링크 창', false, '↩링크 글자 없음'); }
  { closeAll(); S.law='특허법';S.tab='prec';S.precQ='';S.prec='';await render();await wait(700);
    const Pp=await get(PF('리스트'));
    const xs=(Pp.판례||[]).filter(p=>(p.연결판례||[]).some(y=>y.law==='상표'&&y.id));
    T('A1-d 특허 → 상표 교차 링크 있는 행 8 (98후300 이 옮긴 요약본을 걸어 새로 이어짐)', xs.length===8, xs.map(p=>p.id));
    const bad=(Pp.판례||[]).flatMap(p=>(p.연결판례||[]).filter(x=>!x.id).map(x=>x.raw));
    T('A1-e 특허 id 못 뽑은 링크 1종(목차 노트만)', new Set(bad).size===1, [...new Set(bad)]); }
  { closeAll(); S.law='상표법';S.tab='prec';S.precQ='';S.prec='';await render();await wait(600);
    const Ps2=await get(PF('리스트'));
    const bad=[...new Set((Ps2.판례||[]).flatMap(p=>(p.연결판례||[]).filter(x=>!x.id).map(x=>x.raw)))];
    T('A1-f 상표 id 못 뽑은 링크 2종(평문 이름만)', bad.length===2, bad);
    const has=n=>(Ps2.판례||[]).some(p=>p.id===n);
    T('A1-g 연도폴더로 옮긴 요약본 셋이 리스트에 행으로 섰다 · 상표 318',
      (Ps2.판례||[]).length===318 && has('98후928') && has('99후628') && has('2023허13346'),
      [(Ps2.판례||[]).length, has('98후928'), has('99후628'), has('2023허13346')]); }
  /* ───── 0921 §E — 초록 🧾 기출 칩 삭제 ───── */
  { closeAll(); S.law='상표법';S.tab='prec';S.precQ='';S.prec='2002후567(모나리자 굿모닝)';S.precTab='요약';await render();await wait(900);
    const chips=[...document.querySelectorAll('.chip')].map(c=>c.textContent.trim());
    T('E-a 2002후567 머리에 「🧾 기출」 없음', !chips.some(c=>c.indexOf('🧾 기출')===0), chips.filter(c=>c.indexOf('🧾')===0));
    const gi=[...document.querySelectorAll('.pdesc .chip.c-gi')].map(c=>c.textContent.trim());
    T('E-b 하늘색 셋 그대로', gi.filter(x=>x.indexOf('2차-')===0).length===3, gi); }
  { closeAll(); S.law='특허법';S.tab='prec';S.precQ='';S.prec='2023후11562';await render();await wait(800);
    const chips=[...document.querySelectorAll('.chip')].map(c=>c.textContent.trim());
    T('E-c 2023후11562 「🧾 기출」 없음 · 「🧾 사례 2」 는 그대로',
      !chips.some(c=>c.indexOf('🧾 기출')===0) && chips.some(c=>c==='🧾 사례 2'), chips.filter(c=>c.indexOf('🧾')===0)); }
  { closeAll(); S.law='특허법';S.tab='prec';S.precQ='';S.prec='';await render();await wait(700);
    /* 초록이 세던 카드가 전부 하늘색에 있는지 — 앱이 읽는 배열로 직접 */
    let bad=0, n=0;
    for(const law of ['특허법','상표법']){ S.law=law; await render(); await wait(400);
      const P5=await get(PF('리스트'));
      (P5.판례||[]).forEach(p=>{ const sky=new Set((p.기출표시||[]).filter(x=>x.indexOf('2차-')===0));
        const seen=new Set();
        (p.이차카드||[]).forEach(x=>{ if(x.kind!=='기출'||!x.ck||seen.has(x.ck))return; seen.add(x.ck); n++;
          const m=/^([특상디민])기출 (\d\d)-(\d+)-(\d+)/.exec(String(x.ck));
          const code=m?('2차-'+m[1]+'-'+m[2]+'-'+m[3]+'-'+m[4]):'';
          if(!code||!sky.has(code)) bad++; }); }); }
    T('E-d ⚙ 이차카드 기출 '+n+'건 전부 하늘색 코드 안', bad===0, bad); }
  { closeAll(); S.law='특허법';S.tab='prec';S.precQ='';S.prec='2023후11562';await render();await wait(800);
    const P6=await get(PF('리스트'));
    const p=(P6.판례||[]).find(x=>x.id==='2023후11562');
    T('E-e 자동중요도 무변(17 · 2×이차카드 3 포함)', p && p.자동중요도===17, p&&p.자동중요도); }
  /* ───── 0921 §F — 교재 팝업 문구에 HTTP 코드 ───── */
  { T('F-a cvbWhy 토큰 없음', /🔑 토큰이 없다/.test(__jocvb.why('no-token')), __jocvb.why('no-token'));
    T('F-b cvbWhy 404', /^HTTP 404 — 토큰이 이 저장소\(zzikkaplan\/minbeoppdf\)를 못 본다/.test(__jocvb.why(404,'pdf/x.pdf')) && /pdf\/x\.pdf/.test(__jocvb.why(404,'pdf/x.pdf')), __jocvb.why(404,'pdf/x.pdf'));
    T('F-c cvbWhy 401·403 같은 꼴', /^HTTP 401 —/.test(__jocvb.why(401,'a')) && /^HTTP 403 —/.test(__jocvb.why(403,'a')), [__jocvb.why(401,'a'),__jocvb.why(403,'a')]);
    T('F-d cvbWhy 네트워크', /네트워크 오류/.test(__jocvb.why('net')), __jocvb.why('net'));
    T('F-e cvbWhy 그 밖 HTTP n', /^HTTP 500/.test(__jocvb.why(500,'a')), __jocvb.why(500,'a')); }
  { /* 실제 팝업 — 토큰을 가짜로 넣고 fetch 를 404 로 세워 책메타 단계를 태운다 */
    closeAll();
    try{ localStorage.setItem('tt.cfg', JSON.stringify({token:'ghp_fake_for_harness'})); }catch(e){}
    const _f=window.fetch; window.fetch=async(u,o)=>{ if(/api\.github\.com/.test(String(u))) return new Response('', {status:404}); return _f(u,o); };
    try{ __jocvb.C.meta={}; __jocvb.C.doc={}; __jocvb.C.stat={}; }catch(e){}
    let msg='';
    try{ await __jocvb.doc('minso_hs'); }catch(e){ msg=String(e&&e.message||e); }
    window.fetch=_f;
    T('F-f 책메타 404 = 문구에 HTTP 404 + 저장소 이름', /HTTP 404/.test(msg) && /minbeoppdf/.test(msg), msg.slice(0,160));
    T('F-g 「저장소에 없음」 뭉뚱그리기 사라짐', msg.indexOf('저장소에 없음')<0, msg.slice(0,160));
    try{ localStorage.removeItem('tt.cfg'); }catch(e){} }
  { closeAll();
    try{ localStorage.removeItem('tt.cfg'); __jocvb.C.meta={}; __jocvb.C.doc={}; __jocvb.C.stat={}; }catch(e){}
    let msg='';
    try{ await __jocvb.doc('minso_hs'); }catch(e){ msg=String(e&&e.message||e); }
    T('F-h 토큰 없으면 🔑 문구', /🔑 토큰이 없다/.test(msg), msg.slice(0,120)); }
  T('Z-9 콘솔 오류 0', (window.__err||[]).length===0, window.__err);
 }catch(e){ R.push('FAIL | 하네스 예외 | '+String(e&&e.stack||e)); }
 return R.join('\n');})()"""

# ── regress(_task_qa_slim A-2) — TEST 의 고정 대기 `await wait(N)` → 조건 기다림 `await WU(N,'표지')` ──────────────────
#   gate 의 TEST 는 위 문자열 그대로(한 글자도 안 바뀐다) — regress 에서만 _regress_test 가 실행 때 글을 바꿔 끼운다.
#   표지 = 앱이 이미 내놓는 것(busy · 요소 · 글 · 팝업) · 표지가 안 참이면 옛 ms 만큼 기다린 뒤 이어 간다(최대 = 옛 고정 대기 → 옛과 같은 시간 · 같은 값).
#   표지 목록 = _qa_slim_out\_a2\_harness_prec_vault_link_표지.md · 되돌리기 = 아래 표에서 그 줄을 지운다.
_REG_SITES = {
    # TEST 안 줄 번호(`var wait=…` 줄 = 1): (옛 고정 대기 ms, 표지 이름, 대기 뒤 한 박자 ms · None = 기본 80)
    3: (700, 'LIST', None),
    19: (600, 'LINKWIN', None),
    25: (800, 'VAULTPOP', None),
    33: (600, 'BACKWIN', None),
    44: (600, 'LINKWIN', None),
    51: (900, 'SARAE_CHIP', None),
    56: (900, 'SARAE_POP', None),
    71: (700, 'IDLE', None),
    77: (900, 'GI6', None),
    85: (1600, 'GIPOP', None),
    89: (600, 'IDLE', None),
    94: (800, 'GI_2301', None),
    99: (800, 'GI_1CHA4', None),
    102: (800, 'GI_METRO', None),
    107: (700, 'IDLE', None),
    114: (900, 'GI_A2', None),
    122: (1400, 'NOCARD_POP', None),
    128: (500, 'NOCARD_GONE', None),
    131: (1000, 'ANYPOP', None),
    134: (800, 'GI_1CHA_ROW', None),
    138: (1000, 'ANYPOP', None),
    144: (600, 'LOOP_1CHA', None),
    146: (600, 'ANYPOP', 200),
    147: (400, 'IDLE', None),
    150: (700, 'IDLE', None),
    156: (700, 'LINKWIN', None),
    160: (1800, 'LINKROW', None),
    166: (700, 'IDLE', None),
    172: (600, 'IDLE', None),
    181: (900, 'GI_SANGPYO3', None),
    186: (800, 'SARAE_CHIP', None),
    190: (700, 'IDLE', None),
    193: (400, 'IDLE', None),
    202: (800, 'IDLE', None),
}
_REG_JS = r"""
/* ── regress(_task_qa_slim A-2) 조건 기다림 — 앱이 이미 내놓는 표지(busy · 요소 · 글 · 팝업)가 참이 되면 바로 이어 간다 · 안 참이면 옛 고정 대기(ms)만큼 기다린 뒤 이어 간다 ── */
window.__uw=[];
var __Q=s=>document.querySelectorAll(s).length;
var __IDLE=()=>!(typeof busy!=='undefined'&&busy);
var __pops=()=>[...document.querySelectorAll('.pop')];
var __pt=p=>(p.textContent||'');
var __chips=()=>[...document.querySelectorAll('.pdesc .chip.c-gi')].map(c=>c.textContent.trim());
var __CONDS={
 LIST:()=>__Q('.plg .plgb')>0,
 LINKWIN:()=>__pops().some(p=>__pt(p).indexOf('↩ 링크')>=0&&p.querySelectorAll('.plwl .res').length>0),
 BACKWIN:()=>__pops().some(p=>__pt(p).indexOf('↩ 백링크')>=0&&p.querySelectorAll('.plwl .res').length>0),
 VAULTPOP:()=>__pops().some(p=>__pt(p).indexOf('2025후10169')>=0&&__pt(p).indexOf('↩ 링크')<0),
 SARAE_CHIP:()=>[...document.querySelectorAll('.chip')].some(c=>c.textContent.trim()==='🧾 사례 2'),
 SARAE_POP:()=>__pops().some(p=>{const t=__pt(p);return t.indexOf('🧾 사례')>=0&&t.indexOf('특사례 2-3-2')>=0&&t.indexOf('추가사례3(A)')>=0&&p.querySelectorAll('.res').length>0}),
 GI6:()=>__Q('.pdesc .chip.c-gi')===6,
 GIPOP:()=>S.law==='특허법'&&__pops().some(p=>__pt(p).indexOf('특기출 16-53-3')>=0),
 GI_2301:()=>__chips().indexOf('2차-특-26-63-4 M')>=0,
 GI_1CHA4:()=>__chips().filter(x=>/^1차-/.test(x)).length===4,
 GI_METRO:()=>__chips().indexOf('2차-특-19-56-3')>=0&&__Q('.pdesc .chip.c-theme')===2,
 GI_A2:()=>__chips().indexOf('1차-상-07-44-r7')>=0&&__chips().indexOf('1차-특-20-57-17')>=0&&!!document.querySelector('.pdesc .gilgd'),
 NOCARD_POP:()=>__pops().some(p=>{const t=__pt(p);return t.indexOf('문항 카드가 없다')>=0&&t.indexOf('원장 짝이 없다')>=0&&[...p.querySelectorAll('button')].some(b=>/기출뷰로/.test(b.textContent))}),
 NOCARD_GONE:()=>!__pops().some(p=>__pt(p).indexOf('문항 카드가 없다')>=0),
 ANYPOP:()=>__Q('.pop')>0,
 GI_1CHA_ROW:()=>__chips().some(x=>/^1차-특-12-49/.test(x)),
 LOOP_1CHA:()=>__chips().some(x=>/^1차-/.test(x)),
 LINKROW:()=>S.law==='특허법'&&__pops().some(p=>__pt(p).indexOf('98후1921')>=0),
 GI_SANGPYO3:()=>__chips().filter(x=>/^2차-/.test(x)).length===3,
 IDLE:()=>true
};
var WU=async(ms,tag,xtra)=>{
 const t0=performance.now(), f=__CONDS[tag]; let ok=false;
 for(;;){
  let v=false; try{ v=__IDLE()&&(f?!!f():true); }catch(e){}
  if(v){ ok=true; break; }
  if(performance.now()-t0>=ms) break;
  await wait(25);
 }
 if(ok) await wait(xtra===undefined?80:xtra);   /* 표지가 참인 뒤 한 박자 — 같은 틱에 이어 일어나는 그리기 · setTimeout 0 이 지나가게(누름 뒤 탭 무변 칸은 200) */
 window.__uw.push([tag,Math.round(performance.now()-t0),ok]);
};
"""


def _regress_test(t):
    import re as _re
    anchor = 'var wait=ms=>new Promise(r=>setTimeout(r,ms));'
    assert t.count(anchor) == 1, 'TEST 의 wait 정의를 못 찾음'
    seen = []

    def sub(m):
        rel = 1 + t.count('\n', 0, m.start())
        if rel not in _REG_SITES:
            return m.group(0)   # 표지 없는 자리 = 옛 고정 대기 그대로
        ms, tag, xtra = _REG_SITES[rel]
        assert ms == int(m.group(1)), 'TEST %d 줄 대기가 표와 다르다: %s' % (rel, m.group(0))
        seen.append(rel)
        return "await WU(%d,'%s'%s)" % (ms, tag, '' if xtra is None else ',%d' % xtra)
    q = _re.sub(r'await wait\((\d+)\)', sub, t)
    assert sorted(seen) == sorted(_REG_SITES), '표에 있는데 TEST 에 없는 자리: %s' % sorted(set(_REG_SITES) - set(seen))
    return q.replace(anchor, anchor + _REG_JS, 1)


def _boot_wait(ws, ms):
    """regress — 앱 부팅(첫 render)이 끝났다는 표지: 전역 busy 가 false 이고 #slot 에 화면이 있다(최대 ms)"""
    t0 = time.time()
    while time.time() - t0 < ms / 1000.0:
        if ev(ws, "!(typeof busy!=='undefined'&&busy)&&!!document.querySelector('#slot > *')") is True:
            time.sleep(0.1)
            return True
        time.sleep(0.05)
    return False


def _uw_note(js):
    """regress — 조건 기다림 셈 한 줄(INFO · 판정 아님) — 시간 초과 표지가 어디인지"""
    try:
        uw = json.loads(js) if isinstance(js, str) else []
    except Exception:
        uw = []
    miss = {}
    for w in uw:
        if not w[2]:
            miss[w[0]] = miss.get(w[0], 0) + 1
    n_ok = sum(1 for w in uw if w[2])
    print('INFO | 기다림 표지(regress) | 조건 기다림 %d회 · 참 %d · 시간 초과 %d(옛 고정 대기만큼 기다림) · 걸린 시간 합 %.1f초 · 시간 초과 표지 %s'
          % (len(uw), n_ok, len(uw) - n_ok, sum(w[1] for w in uw) / 1000.0,
             ', '.join('%s×%d' % kv for kv in sorted(miss.items())) or '없음'))


def main():
    if QJ.SMOKE:
        # smoke 칸 없음 — 판례탭 볼트 링크 하네스는 한 쪽에서 앞 칸이 만든 목록 · 팝업 상태로 이어 도는 한 덩어리라 앞부분만 떼면 싸지도 않고 상태가 안 맞는다
        print('INFO | smoke 칸 없음 | 판례탭 볼트 링크 하네스는 한 쪽에서 이어 도는 한 덩어리', flush=True)
        return 0
    ws, proc, srv = serve()
    try:
        out = ev(ws, TEST if QJ.GATE else _regress_test(TEST))
        print(out if isinstance(out, str) else json.dumps(out, ensure_ascii=False))
        if QJ.REGRESS:
            _uw_note(ev(ws, "JSON.stringify(window.__uw || [])"))
        ok = isinstance(out, str) and 'FAIL' not in out
        print('\n=== %s ===' % ('PASS 전부' if ok else 'FAIL 있음'))
        return 0 if ok else 3
    finally:
        try:
            proc.kill()
        except Exception:
            pass
        srv.shutdown()


if __name__ == '__main__':
    sys.exit(main())
