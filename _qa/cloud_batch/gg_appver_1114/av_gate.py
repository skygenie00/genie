# av_gate.py — 「새 판 스스로 받기」 관문(11/14 · gg_appver_1114)
# 앱 파일 하나를 「cache-control: max-age=600」 을 붙이는 작은 서버(GitHub Pages 흉내)로 띄우고, 서버 쪽 파일을 바꿔 가며
# 화면이 스스로 새 판으로 다시 열리는지 진짜 브라우저(크롬 · 웹킷)로 잰다. 바깥 주소는 다 막는다(기록 · CDN 없이 앱 끝의 조각만 잼).
#   python av_gate.py --app minbeop --file minbeop/index.html --mode new  --eng chromium,webkit
#   python av_gate.py --app minbeop --file <바탕 파일>        --mode base --eng chromium
# mode new = 모든 칸 PASS 여야 함 · mode base = 헛잣대 칸은 FAIL · 무변 칸은 PASS 여야 함(어긋난 수 = 합계 FAIL)
import sys, time, threading, argparse, hashlib
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from playwright.sync_api import sync_playwright

ST = {'body': b'', 'etag': '"0-0"', 'n': 0, 'log': []}
MAIN = ('/genie/app/', '/genie/app/index.html')

class H(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def log_message(self, *a): pass
    def do_GET(self): self._s(True)
    def do_HEAD(self): self._s(False)
    def _s(self, body):
        p = self.path.split('?')[0]
        if p not in MAIN:
            self.send_response(404); self.send_header('Content-Length', '0'); self.end_headers(); return
        ST['log'].append((self.command, self.path, self.headers.get('If-None-Match') or '', self.headers.get('Cache-Control') or ''))
        if (self.headers.get('If-None-Match') or '') == ST['etag']:
            self.send_response(304); self.send_header('ETag', ST['etag']); self.send_header('Cache-Control', 'max-age=600'); self.end_headers(); return
        b = ST['body']
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(b)))
        self.send_header('Cache-Control', 'max-age=600'); self.send_header('ETag', ST['etag'])
        self.send_header('Last-Modified', 'Fri, 13 Nov 2026 18:14:%02d GMT' % (ST['n'] % 60)); self.end_headers()
        if body: self.wfile.write(b)

def setver(src, v, etag_only=False):
    ST['n'] += 1
    if not etag_only:
        if v <= 1: ST['body'] = src.encode('utf-8')
        else:
            i = src.rindex('</body>'); ST['body'] = (src[:i] + '<script>window.__ver=%d</script>' % v + src[i:]).encode('utf-8')
    ST['etag'] = '"%x-%x"' % (ST['n'], len(ST['body']))

def run(app, src, eng, mode, W):
    out = []
    def cell(name, ok, yard, info=''):
        if mode == 'new': st = 'PASS' if ok else 'FAIL'; tail = 'NEW'
        else:
            good = (not ok) if yard else ok
            st = 'PASS' if good else 'FAIL'; tail = 'BASE · ' + ('바탕 FAIL(헛잣대)' if yard and not ok else '바탕 PASS(무변)' if ok and not yard else '바탕 ' + ('PASS' if ok else 'FAIL') + ' = 어긋남')
        out.append(st); print('%s | %s %s · %s · %s%s' % (st, app, name, eng, tail, (' · ' + info) if info and st == 'FAIL' else '')); sys.stdout.flush()
    with sync_playwright() as p:
        br = getattr(p, eng).launch(proxy={'server': 'http://127.0.0.1:9', 'bypass': '127.0.0.1'})
        ctx = br.new_context(viewport={'width': 1100, 'height': 800}); page = ctx.new_page()
        nav = {'n': 0}
        page.on('framenavigated', lambda f: nav.__setitem__('n', nav['n'] + (1 if f == page.main_frame else 0)))
        url = 'http://127.0.0.1:%d/genie/app/' % PORT
        ver = lambda: page.evaluate('window.__ver||1')
        trig = lambda: page.evaluate("document.dispatchEvent(new Event('visibilitychange'))")
        def waitver(v, ms=9000):
            t0 = time.time()
            while time.time() - t0 < ms / 1000:
                try:
                    if ver() == v: return True
                except Exception: pass
                time.sleep(0.25)
            return False
        t0 = time.time()
        setver(src, 1); page.goto(url, wait_until='load'); time.sleep(3)
        n0 = nav['n']; trig(); time.sleep(2)
        cell('열어 둔 화면 · 서버 그대로 → 다시 안 열림', nav['n'] == n0 and ver() == 1, False, 'nav %d→%d' % (n0, nav['n']))
        setver(src, 2); time.sleep(W); n1 = nav['n']; trig(); ok = waitver(2)
        cell('서버에 새 판 → 돌아오면(보이게 되면) 새 판으로 다시 열림', ok, True, 'ver %s' % ver())
        time.sleep(3); n2 = nav['n']; time.sleep(W); trig(); time.sleep(2.5)
        cell('한 번만 다시 열림(더 안 돎) · 주소 그대로', nav['n'] == n2 and n2 == n1 + 1 and '?v=' not in page.url and ver() == 2, True, 'nav %d→%d→%d url %s' % (n1, n2, nav['n'], page.url))
        setver(src, 2, etag_only=True); time.sleep(W); n3 = nav['n']; v3 = ver(); trig(); time.sleep(3)
        cell('다른 앱만 올라간 배포(파일 같고 ETag 만 바뀜) → 다시 안 열림', nav['n'] == n3 and ver() == v3, False, 'nav %d→%d' % (n3, nav['n']))
        foc = page.evaluate("(()=>{const t=document.createElement('textarea');t.id='__avt';t.style.cssText='position:fixed;left:0;top:0;width:80px;height:30px;z-index:2147483647';document.body.appendChild(t);t.focus();return document.activeElement===t})()")
        setver(src, 3); time.sleep(W); n4 = nav['n']; v4 = ver(); trig(); time.sleep(3.5)
        cell('글 칸에 커서(적는 중) → 새 판이 있어도 다시 안 열림', foc and nav['n'] == n4 and ver() == v4, False, 'foc %s nav %d→%d ver %s' % (foc, n4, nav['n'], ver()))
        page.evaluate("(()=>{const t=document.getElementById('__avt');if(t){t.blur();t.remove()}})()"); time.sleep(W); trig(); ok = waitver(3)
        cell('커서를 뺀 뒤 돌아오면 새 판으로 다시 열림', ok, True, 'ver %s' % ver())
        time.sleep(1.5); setver(src, 4); L0 = len(ST['log'])
        page.goto(url, wait_until='load'); v0 = ver(); ok = waitver(4)
        gets = [x for x in ST['log'][L0:] if x[0] == 'GET']
        cell('앱을 새로 엶(10 분 캐시 안) → 곧 새 판', ok, True, '처음 뜬 판 %s · 끝 %s' % (v0, ver()))
        print('INFO | %s · %s · %s · 새로 열 때 처음 뜬 판 = %s(3 = 캐시의 옛 판 · 4 = 바로 새 판) · 그 뒤 서버 GET %d · 주소 %s · %.1f 초' % (app, eng, mode.upper(), v0, len(gets), page.url.replace(url, '…/'), time.time() - t0)); sys.stdout.flush()
        br.close()
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--app', required=True); ap.add_argument('--file', required=True)
    ap.add_argument('--mode', default='new', choices=['new', 'base']); ap.add_argument('--eng', default='chromium,webkit'); ap.add_argument('--gap', type=float, default=5.6)
    a = ap.parse_args()
    src = open(a.file, encoding='utf-8', newline='').read()
    print('%s %s md5 %s · %d B' % (a.app, a.mode.upper(), hashlib.md5(src.replace('\r\n', '\n').encode()).hexdigest()[:8], len(src.encode())))
    srv = ThreadingHTTPServer(('127.0.0.1', 0), H); PORT = srv.server_address[1]; threading.Thread(target=srv.serve_forever, daemon=True).start()
    res = []
    for e in [x for x in a.eng.split(',') if x]:
        ST['log'].clear(); res += run(a.app, src, e, a.mode, a.gap)
    f = res.count('FAIL'); print('합계 FAIL %d' % f); sys.exit(1 if f else 0)
