# -*- coding: utf-8 -*-
"""민법OX 댓글 「고치기」 · 인용 수 「↩ n」 셋 · 인용 문항 목록 창 — _task_ox_cs_edit_usecount §H.

  NEW  = genie 작업트리 minbeop/index.html (고친 판)
  HEAD = git HEAD 의 같은 파일 (헛잣대)
  실데이터 = studyplandata minbeop/기록.json(저장소 전부) · 문항마스터.json(5,548) · 정리OMR 자산은 쪽 빈 가짜(자리표 그림)
  CDP · 로컬 서버(같은 출처 fetch 만) · 서버·크롬 프로필은 N: 밖(%TEMP%) · 캡처는 minbeop/task/_shots_cs_edit_usecount/

쓰기 : python _harness_ox_cs_edit_usecount.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import http.server, socketserver, threading, subprocess, socket, json, base64, struct, urllib.request, urllib.parse
import hashlib, io, os, re, shutil, sys, tempfile, time
sys.stdout.reconfigure(encoding='utf-8')

GENIE = _roots.genie()
SPD = _roots.spd()
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(tempfile.gettempdir(), 'h_cs_edit_usecount')
SHOTS = os.path.join(HERE, '_shots_cs_edit_usecount')
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
REL = 'minbeop/index.html'
TESTS = io.open(os.path.join(HERE, '_harness_ox_cs_edit_usecount_tests.js'), encoding='utf-8').read()
SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__ALERTS=[];window.alert=function(m){__ALERTS.push(String(m));};
window.confirm=function(){return true;};window.prompt=function(){return null;};
(function(){var nf=window.fetch.bind(window);window.fetch=function(u,o){var s=String((u&&u.url)||u);
 if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));
 return nf(u,o);};})();
try{if(navigator.serviceWorker)navigator.serviceWorker.register=function(){return Promise.reject(new Error('sw blocked'));};}catch(e){}
localStorage.clear();
</script>"""


def git(*a):
    return subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


class WS:
    def __init__(self, url):
        u = urllib.parse.urlparse(url); self.s = socket.create_connection((u.hostname, u.port), timeout=600)
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
        return {'__exc': str(r['exceptionDetails'])[:1500]}
    return r.get('result', {}).get('value')


def step(ws, name):
    out = ev(ws, 'window.__HZT.%s()' % name)
    try:
        return json.loads(out) if isinstance(out, str) else {'__exc': out}
    except Exception as e:
        return {'__exc': str(e), 'raw': str(out)[:500]}


def serve(tag, src):
    OUT = os.path.join(WORK, 'srv_' + tag); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    b = src.index('<body'); bb = src.index('>', b) + 1
    html = src[:bb] + SEED + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + TESTS + '\n</script>\n' + html[e:]
    io.open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)
    MAP = {'/rec.json': os.path.join(SPD, 'minbeop', '기록.json'), '/master.json': os.path.join(SPD, 'minbeop', '문항마스터.json')}

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=OUT, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            return MAP.get(p) or super().translate_path(path)

        def log_message(self, *a, **k):
            pass
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    s = socket.socket(); s.bind(('127.0.0.1', 0)); dbg = s.getsockname()[1]; s.close()
    proc = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--hide-scrollbars', '--user-data-dir=' + os.path.join(OUT, 'prof'),
                             '--window-size=1300,900', '--remote-debugging-port=%d' % dbg, 'http://127.0.0.1:%d/index.html' % port],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    targets = None
    for _ in range(160):
        try:
            targets = json.loads(urllib.request.urlopen('http://127.0.0.1:%d/json' % dbg, timeout=2).read().decode())
            if any(t.get('type') == 'page' for t in targets):
                break
        except Exception:
            pass
        time.sleep(0.25)
    ws = WS(next(t for t in targets if t.get('type') == 'page')['webSocketDebuggerUrl']); ws.call('Page.enable')
    return ws, proc, srv


def shot(ws, name, rect, pad=8, maxh=1400):
    if not rect or rect.get('width', 0) <= 0:
        return None
    x = max(0, rect['x'] - pad); y = max(0, rect['y'] - pad)
    w = rect['width'] + 2 * pad; h = min(rect['height'] + 2 * pad, maxh)
    r = ws.call('Page.captureScreenshot', {'format': 'png', 'clip': {'x': x, 'y': y, 'width': w, 'height': h, 'scale': 1}, 'captureBeyondViewport': True})
    b = base64.b64decode(r['data']); p = os.path.join(SHOTS, name); open(p, 'wb').write(b)
    return [name, len(b), hashlib.md5(b).hexdigest()[:10]]


def rect_of(ws, sel):
    return ev(ws, "(()=>{const e=document.querySelector(%s);if(!e)return null;const r=e.getBoundingClientRect();return {x:r.left+scrollX,y:r.top+scrollY,width:r.width,height:r.height}})()" % json.dumps(sel))   # clip 은 문서 기준 — 화면 기준 사각형에 스크롤을 더한다


READY = "typeof ggLineHTML==='function'&&typeof buildQuizData==='function'&&typeof linkSearch==='function'&&!!window.oxCoord&&!!window.mbBook&&!!window.__HZT"


def run(tag, src, full):
    ws, proc, srv = serve(tag, src)
    D = {}
    try:
        for _ in range(240):
            if ev(ws, READY) is True:
                break
            time.sleep(0.5)
        D['ready'] = ev(ws, READY)
        D['setup'] = step(ws, 'setup')
        if not full:
            D['head'] = step(ws, 'head_probe')
        else:
            D['a'] = step(ws, 'a_card')
            D['shot_1_row'] = shot(ws, 'cs_1_row.png', rect_of(ws, '#gg-cs-%s-%s' % (D['a'].get('U'), D['a'].get('GK'))), pad=30)
            D['a_open'] = step(ws, 'a_card_open')
            D['shot_1_edit'] = shot(ws, 'cs_1_edit.png', rect_of(ws, '#gg-cs-%s-%s' % (D['a'].get('U'), D['a'].get('GK'))), pad=30)
            D['a_rules'] = step(ws, 'a_card_rules')
            D['a_save'] = step(ws, 'a_card_save')
            D['a_pop'] = step(ws, 'a_popup')
            D['b'] = step(ws, 'b_search')
            D['shot_2'] = shot(ws, 'cs_2_search.png', rect_of(ws, '#hz-search'))
            ev(ws, "document.querySelectorAll('.oxwin').forEach(w=>w.remove());['hz-card','hz-jn','hz-search'].forEach(i=>{const e=document.getElementById(i);if(e)e.remove();});1")
            D['d'] = step(ws, 'd_viewer')
            pr = ev(ws, "(()=>{const p=document.getElementById('cd-refpop'),t=document.getElementById('cd-reftag');if(!p)return null;const a=p.getBoundingClientRect(),b=t?t.getBoundingClientRect():a;const x=Math.min(a.left,b.left),y=Math.min(a.top,b.top);return {x:x+scrollX,y:y+scrollY,width:Math.max(a.right,b.right)-x,height:Math.max(a.bottom,b.bottom)-y}})()")
            D['shot_3'] = shot(ws, 'cs_3_refpop.png', pr, pad=24)
            D['d_click'] = step(ws, 'd_click')
            D['shot_4b'] = shot(ws, 'cs_4b_slotwin.png', rect_of(ws, '#' + (ev(ws, 'window.__HZ.winId') or 'nothing')), pad=4)
            D['d_row'] = step(ws, 'd_rowclick')
            D['d_close'] = step(ws, 'd_close')
            D['e'] = step(ws, 'e_pic')
            D['shot_4'] = shot(ws, 'cs_4_pic.png', rect_of(ws, '#hz-pic'))
            D['shot_4c'] = shot(ws, 'cs_4c_pic_slotwin.png', rect_of(ws, '#' + (ev(ws, 'window.__HZ.picWin') or 'nothing')), pad=4)
        D['err'] = ev(ws, 'window.__ERR')
        D['alerts'] = ev(ws, 'window.__ALERTS')
    finally:
        try:
            proc.terminate()
        except Exception:
            pass
        srv.shutdown()
    time.sleep(1)
    return D


def main():
    os.makedirs(WORK, exist_ok=True); os.makedirs(SHOTS, exist_ok=True)
    new = io.open(os.path.join(GENIE, REL), encoding='utf-8', newline='').read()
    head = git('show', 'HEAD:' + REL).decode('utf-8')
    t0 = time.time()
    H = run('HEAD', head, False); print('HEAD  %.1fs' % (time.time() - t0))
    t0 = time.time()
    N = run('NEW', new, True); print('NEW   %.1fs' % (time.time() - t0))
    json.dump({'HEAD': H, 'NEW': N}, io.open(os.path.join(WORK, 'raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    L = []
    T = lambda n, c, i=None: L.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c or i is None else ' | ' + json.dumps(i, ensure_ascii=False)[:700]))
    I = lambda n, v: L.append('INFO | ' + n + ' | ' + json.dumps(v, ensure_ascii=False)[:900])
    # ── 소스 · 파일
    hb, nb = head.encode('utf-8'), new.encode('utf-8')
    T('착수 HEAD = 지시서 §0 (1,040,020 B · 544475326d4d)', len(hb) == 1040020 and hashlib.md5(hb).hexdigest().startswith('544475326d4d'), [len(hb), hashlib.md5(hb).hexdigest()])
    T('NEW CRLF 0 · U+FFFD 0 (%d B · %s)' % (len(nb), hashlib.md5(nb).hexdigest()), b'\r\n' not in nb and '\ufffd' not in new)
    sk = lambda s: re.search(r'const SYNC_KEYS = \[(.+?)\];', s, re.S).group(1)
    T('§G SYNC_KEYS 줄 무변', sk(new) == sk(head))
    ch = [l for l in git('status', '--porcelain').decode('utf-8').split('\n') if l.strip()]
    T('§G genie 작업트리 바뀐 파일 = minbeop/index.html 하나 %s' % ch, ch == [' M ' + REL], ch)
    for tag, d in (('HEAD', H), ('NEW', N)):
        T('%s 부트 · 시험 준비(문항 %s) · JS 오류 0 · alert 0' % (tag, (d.get('setup') or {}).get('q')), d.get('ready') is True and (d.get('setup') or {}).get('q') == 5548 and not d.get('err') and not d.get('alerts'),
          [d.get('ready'), (d.get('setup') or {}).get('q'), d.get('err'), d.get('alerts'), (d.get('setup') or {}).get('__exc')])
    T('§B 옛 useNumHTML 호출(연결 칩 · 문항 %s) 출력 HEAD = NEW' % (N.get('setup') or {}).get('chipOwners'), (N.get('setup') or {}).get('chips') == (H.get('setup') or {}).get('chips') and 'ERR' not in ((N.get('setup') or {}).get('chips') or 'ERR'))
    # ── 헛잣대
    h = H.get('head') or {}
    T('헛잣대 HEAD — 댓글 줄 단추 = [지우기]만 · 찾기 ↩ 0 · 그림 ↩ 0 · slotUsers 없음 · 자리 팝업 ↩ 0', h.get('btns') == ['지우기'] and h.get('searchI') == 0 and h.get('picUse') == 0 and h.get('slotUsers') is False and h.get('popI') == 0, h)
    # ── §A
    a, ao, ar, asv, ap = N.get('a') or {}, N.get('a_open') or {}, N.get('a_rules') or {}, N.get('a_save') or {}, N.get('a_pop') or {}
    I('§A 시험 문항', {k: a.get(k) for k in ('U', 'GK', 'CK', 'O', 'owners', 'T0')})
    T('A-1 댓글 줄 단추 = [고치기(파랑 · ml-auto) · 지우기(빨강 · ml-auto 없음)]', a.get('btns') == ['고치기|ml-auto|text-blue-600', '지우기||text-red-700'], a.get('btns'))
    T('A-2 고치기 → 편집 칸(textarea rows 2 · 값 = 원 댓글 · 근거 고치기 칸 클래스) + 저장 + 취소 · 날짜만 남음 · 초점', ao.get('open') and ao.get('rows') == 2 and ao.get('val') == a.get('T0') and 'border-blue-300' in (ao.get('cls') or '') and 'text-[12.5px]' in (ao.get('cls') or '')
      and ao.get('kids') == ['span', 'div[textarea:,button:저장,button:취소]'] and ao.get('focus'), ao)
    T('A-2 편집 칸 한도 = 댓글 한도(ggMaxOf → GG_CMAX %s)' % ao.get('CMAX'), ao.get('maxOf') == ao.get('CMAX') and ao.get('CMAX'), [ao.get('maxOf'), ao.get('CMAX'), ao.get('id')])
    T('D-2 빈 글 저장 안 됨 — 칸 그대로 · 테두리 빨강(%s) · 저장소 무변' % ar.get('emptyBorder'), ar.get('emptyKept') and ar.get('emptyBorder') == 'rgb(220, 38, 38)' and ar.get('emptyStore'), ar)
    T('D-2 Shift+Enter = 저장 안 함(칸 그대로 · 저장소 무변)', ar.get('shiftKept') and ar.get('shiftStore'), ar)
    T('D-2 Esc = 취소 — 원문 그대로 · 단추 [고치기 · 지우기] 되돌아옴 · 저장소 무변', ar.get('escClosed') and ar.get('escText') == ' '.join(a.get('T0', '').split()) and ar.get('escBtns') == ['고치기', '지우기'] and ar.get('escStore'), [ar.get('escText'), a.get('T0'), ar.get('escBtns')])
    T('D-1 카드 — Enter 저장 → 그 댓글 t 만 바뀜(ts·k 같음 · 저장소 나머지 글자까지 같음)', asv.get('onlyT') and asv.get('tsSame') and asv.get('kSame') and asv.get('newT', '').startswith('하네스 고친 글'), asv)
    T('D-1 카드 — 줄이 새 글 + [고치기 · 지우기] 로 다시 그려짐', asv.get('rowText', '').startswith('하네스 고친 글') and asv.get('rowBtns') == ['고치기', '지우기'], asv)
    T('D-1 문항 팝업(qp-) — 같은 단추 · Esc 가 팝업 창을 안 닫음 · 저장 → t 만 · 카드 줄에도 퍼짐', ap.get('win') and ap.get('btns') == ['고치기', '지우기'] and ap.get('open') and ap.get('winAfterEsc') and ap.get('escClosed') and ap.get('onlyT') and ap.get('cardFollows'), ap)
    T('A-4 · D-1 정리 창(jn-) — 「연결한 근거」 상자 댓글 줄엔 고치기 단추 없음(✎ 여기서 고치기 그대로) · 카드·팝업에서 고친 글이 그 상자에 따라옴', a.get('jnHasEditBtn') is False and a.get('jnHasRefEdit') and asv.get('jnHasT1') and ap.get('jnFollows'), [a.get('jnHasEditBtn'), a.get('jnHasRefEdit'), a.get('jnHasT0'), asv.get('jnHasT1'), ap.get('jnFollows')])
    # ── §B
    b = N.get('b') or {}
    T('B-1 근거 찾기 — Q4311(쓰임 %s) 줄 머리 = ID · 번호 · 단원 · 「↩%s」(단원 바로 뒤)' % (b.get('count'), b.get('count')), b.get('hasT') and b.get('iTxt') == '↩%s' % b.get('count') and b.get('iAfterWhere'), b)
    T('B-1 5 이상 빨강(%s) · 둘째 검색(%s · %s줄) — ↩ 없는 줄 %d 은 전부 쓰임 ≤1 · ↩ 있는 줄 %d 은 쓰임 ≥2 이고 글자 = ↩쓰임' % (b.get('iColor'), b.get('term2'), b.get('term2Rows'), len(b.get('noI') or []), len(b.get('withI') or [])),
      b.get('iColor') == 'rgb(220, 38, 38)' and b.get('noI') and b.get('withI') and all(x <= 1 for x in b.get('noI')) and all(w[1] >= 2 and w[2] == '↩%d' % w[1] for w in b.get('withI')), [b.get('noI'), b.get('withI')])
    T('B-2 · D-3 ↩ 누르면 넣기(addRefId) 안 함 — reflinks·넣은 목록 무변 · 쓰임 창 하나', b.get('reflSame') and b.get('pickSame') and len(b.get('newWins') or []) == 1, [b.get('reflSame'), b.get('pickSame'), b.get('newWins')])
    T('B-1 이미 넣은 줄(O2 가 Q4311 을 걸어 둠) = 「이미 넣음」 · ↩ 없음(시안 ②)', b.get('onRow') == [True, False], b.get('onRow'))
    T('D-8 ② 캡처 전 첫 검색 결과(법인책임 · ↩ 줄)가 그대로 남아 있다', b.get('firstIntact') is True, b.get('firstIntact'))
    # ── §C·§D·§F
    d, dc, dr = N.get('d') or {}, N.get('d_click') or {}, N.get('d_row') or {}
    T('D-4 pick 화면 상자 %s 전부 — 상자 그룹 g.list qid 집합 = slotUsers(V.qid, rc) (어긋남 %s)' % (d.get('boxes'), len(d.get('bad') or [])), d.get('wrap') and (d.get('boxes') or 0) > 0 and not d.get('bad'), d)
    T('D-4 겹침 있는 자리 %d곳 — 실데이터 Q4326·Q4327·Q4328 + 흉내 둘(Q5631 자리에 Q0001·Q0002 · Q4311 자리에 ref Q0003)' % len(d.get('multi') or []), len(d.get('multi') or []) >= 3 and any('Q4326' in m for m in d.get('multi') or []), d.get('multi'))
    T('D-5 자리 팝업 — 「이 문항에도 쓰기」 와 「여기서 새로 찍기」 사이 「↩%s」 · 줄 align-items center · 딱지 이름 수 %s 와 같음' % ((d.get('iTxt') or '')[1:], d.get('tagNames')), d.get('iBetween') and d.get('rowAlign') == 'center' and d.get('iTxt') == '↩%s' % d.get('tagNames'), [d.get('iTxt'), d.get('tagNames'), d.get('popFor'), d.get('rowAlign')])
    T('D-5 ↩ 누르면 refAdopt 안 함 — ox_q_coords 무변 · 목록 창 하나', dc.get('coordsSame') and len(dc.get('newWins') or []) == 1 and (dc.get('newWins') or [''])[0].startswith('oxwin-slotuse-'), dc)
    rows = dc.get('rows') or []
    T('D-7 목록 창 머리 「📍 이 자리를 찍어 둔 문항 %d」 · 줄 수 = n + 1(지금 문항)' % (len(rows) - 1), (dc.get('title') or '').startswith('📍 이 자리를 찍어 둔 문항 %d' % (len(rows) - 1)) and len(rows) == len(d.get('popFor') or []) + 1 and len(rows) >= 2, [dc.get('title'), len(rows)])
    T('D-7 첫 줄 = 지금 문항(노랑 · 클릭 없음) · 딱지 = ref 유무(Q4326 원본 · Q4327·Q4328 🔗 같이 씀)', rows and rows[0][0].endswith('지금 문항') and 'rgb(254, 252, 232)' in rows[0][1] and rows[0][2] == 0
      and any('Q4326' in r[0] and r[0].endswith('원본') for r in rows) and all(r[0].endswith('🔗 같이 씀') for r in rows if ('Q4327' in r[0] or 'Q4328' in r[0])), rows)
    T('D-7 줄 누르면 그 문항 팝업(%s) · 지금 문항 줄은 onclick 없음' % dr.get('q'), dr.get('q') and dr.get('opened') == ['oxwin-q-' + dr.get('q')] and dr.get('meRowClick') is None, dr)
    # ── §E
    e = N.get('e') or {}
    T('E-1 한 자리 그림(Q4327 · 🔗 Q4326 자리 · 칩 없음) — 아랫줄 새로 「↩2」(Q4326 원본 · Q4328 같이 씀)', e.get('b0') == [None, '↩2', None], e.get('b0'))
    T('E-1 여러 자리 그림 — 칩 다음 형제 「↩n」(Q5631 첫 자리 = 흉내 둘 → ↩2)', (e.get('b2') or [None])[0] == '자리 1 / 3 ▶' and e.get('b2')[1] == '↩2' and e.get('b2')[2] is True, e.get('b2'))
    T('D-6 칩 넘김에 수가 따라감 — Q4311 %s → %s' % (e.get('b1'), e.get('flip')), (e.get('b1') or [None])[0] == '자리 1 / 2 ▶' and e.get('flip') and e['flip'][0] == ['자리 2 / 2 ▶', '↩1'] and e['flip'][1][0] == '자리 1 / 2 ▶' and e['flip'][1][1] in ('', None), [e.get('b1'), e.get('flip')])
    T('D-6 ↩ 누르면(%s) 뷰어 안 열림(z 10000 겹 +%s) · 목록 창만(%s) · 줄 %s = n+1' % (e.get('clickedIn'), e.get('ovAfter'), e.get('newWins'), len(e.get('winRows') or [])), e.get('ovAfter') == 0 and len(e.get('newWins') or []) == 1 and len(e.get('winRows') or []) == 3, e)
    T('D-6 0 이면 없음 — 겹침 없는 한 자리 문항(%s) 그림에 ↩·아랫줄 0' % e.get('lone'), e.get('lone') and e.get('loneUse') == 0 and e.get('loneNav') == 0, [e.get('lone'), e.get('loneUse'), e.get('loneNav')])
    I('D-8 캡처', [N.get(k) for k in ('shot_1_row', 'shot_1_edit', 'shot_2', 'shot_3', 'shot_4b', 'shot_4', 'shot_4c')])
    T('D-8 캡처 ①~④-2 일곱 장 다 찍힘', all(N.get(k) for k in ('shot_1_row', 'shot_1_edit', 'shot_2', 'shot_3', 'shot_4b', 'shot_4', 'shot_4c')))
    for l in L:
        print('   ' + l)
    p = sum(1 for l in L if l.startswith('PASS')); f = sum(1 for l in L if l.startswith('FAIL'))
    print('\n합계  PASS %d · FAIL %d' % (p, f))
    io.open(os.path.join(HERE, '_harness_ox_cs_edit_usecount_result.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n\n합계  PASS %d · FAIL %d\n' % (p, f))
    sys.exit(0 if not f else 1)


if __name__ == '__main__':
    main()
