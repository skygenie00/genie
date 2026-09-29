# -*- coding: utf-8 -*-
"""민법OX 채점한 쪽에서도 「◀ 이전」 · 종합사례 원문 정정 · 원문 상자 필기 — _task_ox_prev_case_ink_fix17 §E.

  NEW  = genie 작업트리 minbeop/index.html (고친 판)
  HEAD = `a6f01d1` 의 같은 파일 (헛잣대 — 1·2·3 이 FAIL 이어야 한다)
  실데이터 = studyplandata minbeop/기록.json(저장소 전부) · 문항마스터.json(5,548)
  CDP · 로컬 서버(같은 출처 fetch 만) · 서버·크롬 프로필은 N: 밖(%TEMP%)

쓰기 : python _harness_ox_prev_case_ink_fix17.py
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
WORK = os.path.join(tempfile.gettempdir(), 'h_prev_case_ink')
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
REL = 'minbeop/index.html'
BASE_REV = 'a6f01d1'
TESTS = io.open(os.path.join(HERE, '_harness_ox_prev_case_ink_fix17_tests.js'), encoding='utf-8').read()
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


READY = "typeof buildQuizData==='function'&&typeof renderQuizPage==='function'&&typeof qiAfterRender==='function'&&typeof startQuiz==='function'&&!!window.__HZT"


def run(tag, src):
    ws, proc, srv = serve(tag, src)
    D = {}
    try:
        for _ in range(240):
            if ev(ws, READY) is True:
                break
            time.sleep(0.5)
        D['ready'] = ev(ws, READY)
        D['setup'] = step(ws, 'setup')
        for nm in ('a_prev_normal', 'a_prev_resume', 'a_prev_exam', 'probe23'):
            D[nm] = step(ws, nm)
        if tag == 'NEW':
            for nm in ('b_pull', 'b_edit', 'c_ink', 'c_ink_back', 'c_ink_merge', 'c_ink_clear', 'c_mark_probe'):
                D[nm] = step(ws, nm)
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
    os.makedirs(WORK, exist_ok=True)
    new = io.open(os.path.join(GENIE, REL), encoding='utf-8', newline='').read()
    head = git('show', BASE_REV + ':' + REL).decode('utf-8')
    t0 = time.time(); H = run('HEAD', head); print('HEAD  %.1fs' % (time.time() - t0))
    t0 = time.time(); N = run('NEW', new); print('NEW   %.1fs' % (time.time() - t0))
    json.dump({'HEAD': H, 'NEW': N}, io.open(os.path.join(WORK, 'raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    L = []
    T = lambda n, c, i=None: L.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c or i is None else ' | ' + json.dumps(i, ensure_ascii=False)[:800]))
    I = lambda n, v: L.append('INFO | ' + n + ' | ' + json.dumps(v, ensure_ascii=False)[:900])
    g = lambda d, k: (d.get(k) or {})

    # ══ 소스 · 파일
    hb, nb = head.encode('utf-8'), new.encode('utf-8')
    T('착수 %s = 지시서 §0 (1,051,722 B · e34c226b5010)' % BASE_REV,
      len(hb) == 1051722 and hashlib.md5(hb).hexdigest() == 'e34c226b50100c06cce65aa57b52c77f', [len(hb), hashlib.md5(hb).hexdigest()])
    T('NEW CRLF 0 · U+FFFD 0 (%d B · md5(LF) %s)' % (len(nb), hashlib.md5(nb).hexdigest()), b'\r\n' not in nb and '\ufffd' not in new)
    sk = lambda s: re.search(r'const SYNC_KEYS = \[(.+?)\];', s, re.S).group(1)
    T('§E-6 SYNC_KEYS 줄 무변', sk(new) == sk(head))
    ch = [l for l in git('status', '--porcelain').decode('utf-8').split('\n') if l.strip()]
    T('§G genie 작업트리 바뀐 파일 = minbeop/index.html 하나 %s' % ch, ch == [' M ' + REL], ch)
    T('§A 옛 줄(`if (allGraded) …exam-prev-bar…add(\'hide\')`)이 사라졌다',
      "if (allGraded) document.getElementById('exam-prev-bar').classList.add('hide');" in head
      and "if (allGraded) document.getElementById('exam-prev-bar').classList.add('hide');" not in new)
    T('§A `exam-prev-bar` 를 만지는 자리 = 셋 다 `currentPageIndex === 0` (HEAD 는 add(hide) 하나 + toggle 둘)',
      new.count("exam-prev-bar').classList.toggle('hide', currentPageIndex === 0)") == 3
      and "exam-prev-bar').classList.add('hide')" not in new,
      [new.count("exam-prev-bar').classList.toggle('hide', currentPageIndex === 0)"), head.count("exam-prev-bar').classList.toggle('hide', currentPageIndex === 0)")])
    T('§A 오른쪽 알약 규칙(`hideBar`) 무접촉',
      "const hideBar = !!allGraded && !!lastGradeResults;\n            document.getElementById('controls-container').classList.toggle('hide', hideBar);" in new)
    T('§C 필기 열쇠 꼴은 `ink:q:` 그대로 — `qiKey` 무변 · 새 통·새 접두 0',
      "function qiKey(uid) { return 'ink:q:' + uid; }" in new and new.count("'ink:q:'") == head.count("'ink:q:'"))

    for tag, d in (('HEAD', H), ('NEW', N)):
        s = g(d, 'setup')
        T('%s 부트 · 문항 %s · JS 오류 0' % (tag, s.get('q')), d.get('ready') is True and s.get('q') == 5548 and not d.get('err'),
          [d.get('ready'), s.get('q'), d.get('err'), s.get('__exc')])
    I('시험 단원', g(N, 'setup').get('pick'))
    pk = g(N, 'setup').get('pick') or {}
    T('시험 단원 고름 — 3쪽짜리(41~60문항) %s개 · 「◀ 이전」용 %s(%s문항) · 사례용 %s'
      % (pk.get('three'), pk.get('prevUnit'), pk.get('n'), (pk.get('caseUnit') or {}).get('k')),
      pk.get('three', 0) >= 2 and pk.get('prevUnit') and (pk.get('caseUnit') or {}).get('uids'), pk)
    T('두 판이 같은 단원·같은 사례 묶음을 골랐다(헛잣대가 같은 자리를 잰다)',
      g(N, 'setup').get('pick') == g(H, 'setup').get('pick'), [g(N, 'setup').get('pick'), g(H, 'setup').get('pick')])

    # ══ §E-1 「◀ 이전」
    an, ah = g(N, 'a_prev_normal'), g(H, 'a_prev_normal')
    I('§E-1 일반 모드 NEW', an); I('§E-1 일반 모드 HEAD', ah)
    T('E-1 일반 — 3쪽(%s문항)·1쪽 %s개 표시·2쪽 %s개 표시 · 두 쪽 다 채점됨' % (an.get('total'), an.get('marked0'), an.get('marked1')),
      an.get('pages') == 3 and an.get('marked0') == 20 and an.get('marked1') == 20 and an.get('allGraded1') is True, an)
    T('E-1 일반 — 첫 쪽은 채점 전에도 「◀ 이전」 없음', an.get('p0_prev_before') is False, an.get('p0_prev_before'))
    T('E-1 일반 — 채점 전 2쪽에는 옛 판도 「◀ 이전」이 있었다(두 판 같음)',
      an.get('p1_prev_ungraded') is True and ah.get('p1_prev_ungraded') is True, [an.get('p1_prev_ungraded'), ah.get('p1_prev_ungraded')])
    T('E-1 ★ 일반 — **채점한 2쪽**에 「◀ 이전」이 보이고 진짜 누름으로 눌린다(NEW)',
      an.get('p1_prev_graded') is True and an.get('p1_hit') == 'btn', [an.get('p1_prev_graded'), an.get('p1_hit')])
    T('E-5 헛잣대 ① — 옛 판(%s)은 채점한 2쪽에 「◀ 이전」이 없다' % BASE_REV,
      ah.get('p1_prev_graded') is False, [ah.get('p1_prev_graded'), ah.get('p1_hit')])
    T('E-1 일반 — 눌러서 1쪽으로(idx %s→%s) · 1쪽은 채점된 모습(카드 %s · 고른 답 %s) · 1쪽엔 「◀ 이전」 없음'
      % (an.get('idx1b'), an.get('idx0'), an.get('p0_cards'), an.get('p0_checked')),
      an.get('idx0') == 0 and an.get('p0_prev_after') is False and an.get('p0_cards') == 20 and an.get('p0_checked') == 20, an)
    T('E-1 일반 — 오른쪽 알약(`#controls-container`) 규칙 무접촉(두 판 같음 · %s)' % an.get('ctrl1'),
      an.get('ctrl1') == ah.get('ctrl1'), [an.get('ctrl1'), ah.get('ctrl1')])

    rn, rh = g(N, 'a_prev_resume'), g(H, 'a_prev_resume')
    I('§E-1 이어풀기 복귀 NEW', rn); I('§E-1 이어풀기 복귀 HEAD', rh)
    T('E-1 이어풀기 — 같은 쪽(%s)에서 목록으로 나갔다 다시 들어와 %s쪽(채점 %s개)으로 복귀 · 그 쪽은 전부 채점됨'
      % (rn.get('leaveIdx'), rn.get('idx'), rn.get('marks')),
      rn.get('leaveIdx') == 1 and rn.get('idx') == 1 and rn.get('allGraded') is True, rn)
    T('E-1 ★ 이어풀기 복귀 — 「◀ 이전」이 보이고 눌린다(NEW) / 옛 판은 없다(헛잣대)',
      rn.get('prev') is True and rn.get('hit') == 'btn' and rh.get('prev') is False, [rn.get('prev'), rn.get('hit'), rh.get('prev')])
    T('E-1 이어풀기 — 두 판의 복귀 자리·채점 수가 같다(다른 것은 「◀ 이전」뿐)',
      rn.get('idx') == rh.get('idx') and rn.get('marks') == rh.get('marks') and rn.get('ctrl') == rh.get('ctrl'), [rn, rh])

    en, eh = g(N, 'a_prev_exam'), g(H, 'a_prev_exam')
    I('§E-1 기출 NEW', en); I('§E-1 기출 HEAD', eh)
    T('E-1 기출 — %s년(문제 %s · 지문 %s) 2쪽에서 전체 채점 · 전부 채점됨' % (en.get('year'), en.get('nos'), en.get('total')),
      en.get('idx') == 1 and en.get('allGraded') is True and en.get('idxAfter') == 1, en)
    T('E-1 ★ 기출 — 채점 뒤 그 쪽에 「◀ 이전」이 보이고 눌린다(NEW) / 옛 판은 없다(헛잣대)',
      en.get('prev_after') is True and en.get('hit') == 'btn' and eh.get('prev_after') is False,
      [en.get('prev_after'), en.get('hit'), eh.get('prev_after')])
    T('E-1 기출 — 채점 전에는 두 판 다 보였다(바뀐 것은 채점 뒤뿐)',
      en.get('prev_before') is True and eh.get('prev_before') is True, [en.get('prev_before'), eh.get('prev_before')])

    # ══ §E-5 헛잣대 ②③
    pn, ph = g(N, 'probe23'), g(H, 'probe23')
    I('헛잣대 probe NEW', pn); I('헛잣대 probe HEAD', ph)
    T('E-5 헛잣대 ② — 옛 판 정정 패널은 칸 셋(%s) · 원문 칸·「가져오기」 없음' % ph.get('fields'),
      ph.get('panel') is True and ph.get('fields') == ['fixq', 'fixexp'] and ph.get('hasC') is False and ph.get('hasPull') is False, ph)
    T('E-5 헛잣대 ③ — 옛 판 [종합사례 원문] 상자(%s개)에 덮개 0 · `.case-box` 0' % ph.get('caseDivs'),
      ph.get('caseDivs', 0) >= 1 and ph.get('boxes') == 0 and ph.get('caseInk') == 0, ph)
    T('E-2·E-3 NEW — 같은 자리에 원문 칸(%s)·「가져오기」·`.case-box` %s개·상자 덮개 %s개'
      % (pn.get('fields'), pn.get('boxes'), pn.get('caseInk')),
      pn.get('fields') == ['fixq', 'fixexp', 'fixc'] and pn.get('hasC') is True
      and pn.get('boxes', 0) >= 1 and pn.get('caseInk', 0) >= 1 and pn.get('caseDivs') == ph.get('caseDivs'), pn)

    # ══ §E-2 정정 패널
    bp = g(N, 'b_pull'); I('§E-2 ① 가져오기', bp)
    T('E-2 ① 흉내 — %s개 묶음에서 `사례` 칸을 비운 지문 %s 가 상자 밖에 혼자(쪽의 상자 %s개 · 그 상자 지문 %s개)'
      % (bp.get('n'), bp.get('orphan'), bp.get('boxes0'), len((bp.get('box0') or {}).get('uids') or [])),
      bp.get('orphanOutside') is True and bp.get('n', 0) >= 3
      and len((bp.get('box0') or {}).get('uids') or []) == bp.get('n', 0) - 1, bp)
    T('E-2 ① 패널 원문 칸은 비어 있고 「%s」 단추가 있다' % bp.get('pullLabel'),
      bp.get('hasC') is True and bp.get('cVal0') == '' and bp.get('pullLabel') == bp.get('wantLabel'), bp)
    T('E-2 ① 「가져오기」 = 같은 번호 원문을 **한 글자도 안 바꾸고** 채운다', bp.get('pulledSame') is True, bp)
    T('E-2 ① 저장 → `ox_q_fix[uid]` 에 `c`(= 그 원문) · `c0` = 빈 칸 · 정답·문제·해설 칸 안 생김 · `done` false',
      (bp.get('rec') or {}).get('c') is True and (bp.get('rec') or {}).get('c0') == ''
      and (bp.get('rec') or {}).get('hasA') is False and (bp.get('rec') or {}).get('hasQ') == 'undefined'
      and (bp.get('rec') or {}).get('hasExp') == 'undefined' and (bp.get('rec') or {}).get('done') is False, bp.get('rec'))
    T('E-2 ① 빈 칸 채우기는 이웃에 안 번진다(이웃 도장 %s건)' % bp.get('peersStamped'), bp.get('peersStamped') == 0, bp)
    T('E-2 ① 다시 그리면 그 지문이 **앞 상자 안**으로 — 상자 수 %s→%s(−0) · 그 상자 지문 %s(+1) · 상자 밖 −1'
      % (bp.get('boxes0'), bp.get('boxes1'), len((bp.get('box1') or {}).get('uids') or [])),
      bp.get('boxes1') == bp.get('boxes0') and len((bp.get('box1') or {}).get('uids') or []) == bp.get('n')
      and bp.get('orphanInside') is True and bp.get('fixedChip') is True, bp)

    be = g(N, 'b_edit'); I('§E-2 ② 원문 글자 고침', be)
    T('E-2 ② 원문 글자를 고치면 **같은 상자 지문 %s개 전부**에 같은 `c` · 저마다 제 `c0`(%s)'
      % (be.get('stamped'), be.get('c0s')),
      be.get('cVal') is True and be.get('stamped') == be.get('n')
      and be.get('c0s') == ['empty'] + ['orig'] * (be.get('n', 1) - 1)
      and '같이 적용했습니다' in (be.get('status') or ''), be)
    T('E-2 ② 상자는 여전히 하나(%s) · 지문 %s · 화면 글자도 바뀌었다'
      % (be.get('boxes'), len((be.get('box') or {}).get('uids') or [])),
      be.get('boxes') == bp.get('boxes0') and len((be.get('box') or {}).get('uids') or []) == be.get('n') and be.get('textHas') is True, be)
    T('E-2 ③ 정정 목록에 「사례」 딱지·전/후 한 줄(§B-3)', be.get('listHasTag', 0) >= 1 and be.get('listHasLine') is True, be)

    # ══ §E-3 필기
    ci = g(N, 'c_ink'); I('§E-3 획', ci)
    T('E-2 ④ 「↩ 정정 해제」 → 정정이 남지 않았다(%s건) · 상자 %s개로 되돌아감' % (ci.get('fixLeft'), ci.get('boxes')),
      ci.get('fixLeft') == g(N, 'setup').get('fix0') and ci.get('boxes') == bp.get('boxes0'), ci)
    T('E-3 상자 덮개 = `svg.qink` 하나 · id `%s` · 열쇠 = 가장 작은 uid 앞에 `case:`(%s)' % (ci.get('svId'), ci.get('wantKey')),
      ci.get('sv') is True and ci.get('key') == ci.get('wantKey') and ci.get('svId') == 'ink-' + str(ci.get('wantKey')), ci)
    T('E-3 덮개는 **원문 글칸**(`%s` · position %s)에만 — 상자 안 지문 카드 덮개 %s개가 그대로 살아 있고, 보이는 자리(%s)에서 짚으면 카드 제 덮개(`%s`)가 맨 위다'
      % (ci.get('host'), ci.get('hostPos'), ci.get('cardInks'), ci.get('cardRect'), ci.get('cardTop')),
      ci.get('host') == 'case-text' and ci.get('hostPos') == 'relative'
      and ci.get('cardInks') == ci.get('n', 0) - 1
      and ci.get('cardOnScreen') is True and ci.get('cardTopIsOwn') is True, ci)
    T('E-3 빨강 한 획 → 메모리 %s획(%s) · 그려진 path %s · 저장 통 `%s` 에 %s획'
      % (ci.get('mem'), ci.get('memColor'), ci.get('paths'), ci.get('dbKey'), ci.get('db')),
      ci.get('penon') is True and ci.get('svOnScreen') is True and ci.get('under') is None and ci.get('mem') == 1
      and ci.get('memColor') == '#dc2626' and ci.get('paths') == 1 and ci.get('db') == 1, ci)

    cb = g(N, 'c_ink_back'); I('§E-3 쪽 넘겼다 돌아옴', cb)
    T('E-3 쪽을 넘기면 상자 덮개가 없어지고(%s) 돌아오면 그 획이 다시 그려진다(path %s · 메모리 %s)'
      % (cb.get('away'), cb.get('paths'), cb.get('mem')),
      cb.get('away') == 0 and cb.get('sv') is True and cb.get('paths') == 1 and cb.get('mem') == 1, cb)

    cm = g(N, 'c_ink_merge'); I('§E-3 지문을 들인 뒤', cm)
    T('E-3 ★ §B 로 지문을 상자에 들여 열쇠가 `%s`→`%s` 로 바뀌어도 그 획이 **보인다**(path %s)'
      % (cm.get('keyBefore'), cm.get('keyAfter'), cm.get('paths')),
      cm.get('keyChanged') is True and cm.get('paths') == 1 and cm.get('mem') == 1, cm)
    T('E-3 합친 뒤 지금 열쇠 하나로 모이고 옛 열쇠는 지워진다(새 %s · 옛 %s)' % (cm.get('dbNew'), cm.get('dbOld')),
      cm.get('dbNew') == 1 and cm.get('dbOld') in ('gone', 0, None), cm)
    T('E-3 지문 카드 필기 before/after 무변(%s)' % cm.get('cardInk1'), cm.get('cardSame') is True, cm)
    T('E-3 §C-4 폭 맞춤은 지문 카드와 같은 길(단위 좌표 viewBox `%s` · `%s`)' % (cm.get('vb'), cm.get('par')),
      cm.get('vb') == '0 0 1 1000' and cm.get('par') == 'xMinYMin slice', cm)

    cc = g(N, 'c_ink_clear'); I('§E-3 🗑 · §E-6 새 키', cc)
    T('E-3 🗑 「이 쪽 필기 모두 지우기」가 **획을 그은 그 상자**(`%s` · 지우기 전 메모리 %s · 통 %s)의 필기도 지운다(메모리 %s · 통 %s)'
      % (cc.get('key'), cc.get('before'), cc.get('dbBefore'), cc.get('mem'), cc.get('db')),
      cc.get('before') == 1 and cc.get('dbBefore') == 1 and cc.get('mem') == 0 and cc.get('db') in ('gone', 0), cc)
    T('E-6 새 열쇠 꼴 = `ink:q:case:*` 뿐(새 통·새 키 0) — 새로 생긴 열쇠 %s' % cc.get('newKeys'),
      all(str(k).startswith('ink:q:') for k in (cc.get('newKeys') or [])), cc)
    T('E-6 `SYNC_KEYS` 두 판 같음 · 시험 뒤에도 같음',
      cc.get('syncKeys') == g(N, 'setup').get('syncKeys') == g(H, 'setup').get('syncKeys'),
      [cc.get('syncKeys'), g(H, 'setup').get('syncKeys')])
    T('E-6 뒷정리 — `ox_q_fix` 를 시험 앞으로 되돌렸다', cc.get('fixRestored') is True, cc)

    mp = g(N, 'c_mark_probe')
    I('§C-3 「✏️ 표시」 모드에서 원문 글자의 형광펜·밑줄 — 재서 보고만(이번 판에서 만들지 않는다)', mp)

    for tag, d in (('HEAD', H), ('NEW', N)):
        T('%s JS 오류 0 · alert %s' % (tag, d.get('alerts')), not d.get('err'), d.get('err'))

    for l in L:
        print('   ' + l)
    p = sum(1 for l in L if l.startswith('PASS')); f = sum(1 for l in L if l.startswith('FAIL'))
    print('\n합계  PASS %d · FAIL %d' % (p, f))
    io.open(os.path.join(HERE, '_harness_ox_prev_case_ink_fix17_result.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n\n합계  PASS %d · FAIL %d\n' % (p, f))
    sys.exit(0 if not f else 1)


if __name__ == '__main__':
    main()
